import json
import os
import boto3
from datetime import datetime
import uuid

# Initialize AWS clients
dynamodb = boto3.resource('dynamodb', region_name=os.environ.get('AWS_REGION', 'us-west-2'))
s3_client = boto3.client('s3', region_name=os.environ.get('AWS_REGION', 'us-west-2'))
bedrock_client = boto3.client('bedrock-runtime', region_name=os.environ.get('AWS_REGION', 'us-west-2'))

# Environment variables
DYNAMODB_TABLE_NAME = os.environ.get('DYNAMODB_TABLE_NAME', 'bloom-ai-data')
S3_RESEARCH_BUCKET = os.environ.get('S3_RESEARCH_BUCKET', 'bloom-ai-research-1772798279')
BEDROCK_MODEL_ID = os.environ.get('BEDROCK_MODEL_ID', 'anthropic.claude-3-5-sonnet-20241022-v2:0')

# Get DynamoDB table
table = dynamodb.Table(DYNAMODB_TABLE_NAME)


def lambda_handler(event, context):
    """Main entry point for API Gateway requests"""
    try:
        # Parse the request
        http_method = event.get('httpMethod', '')
        path = event.get('path', '')
        body = json.loads(event.get('body', '{}')) if event.get('body') else {}
        
        # Route the request
        if path == '/conversation/start' and http_method == 'POST':
            return start_conversation(body)
        elif path == '/conversation/message' and http_method == 'POST':
            return send_message(body)
        elif path.startswith('/conversation/') and http_method == 'GET':
            session_id = path.split('/')[-1]
            return get_conversation_history(session_id)
        else:
            return response(404, {'error': 'Not found'})
            
    except Exception as e:
        print(f"Error in lambda_handler: {str(e)}")
        return response(500, {'error': 'Internal server error', 'message': str(e)})


def start_conversation(body):
    """Initialize new conversation session"""
    try:
        user_id = body.get('userId')
        initial_prompt = body.get('initialPrompt', '')
        
        if not user_id:
            return response(400, {'error': 'userId is required'})
        
        # Generate session ID
        session_id = f"sess_{uuid.uuid4().hex[:12]}"
        
        # Get user profile
        user_profile = get_user_profile(user_id)
        if not user_profile:
            return response(404, {'error': 'User not found'})
        
        # Create session record
        timestamp = datetime.utcnow().isoformat() + 'Z'
        session_item = {
            'PK': f"USER#{user_id}",
            'SK': f"SESSION#{timestamp}",
            'entityType': 'conversation_session',
            'sessionId': session_id,
            'userId': user_id,
            'status': 'active',
            'startedAt': timestamp,
            'lastMessageAt': timestamp,
            'conversationState': 'greeting',
            'collectedInfo': {}
        }
        table.put_item(Item=session_item)
        
        # Generate initial AI response
        system_prompt = build_system_prompt(user_profile)
        messages = []
        if initial_prompt:
            messages.append({'role': 'user', 'content': initial_prompt})
        
        ai_response = call_bedrock(messages, system_prompt)
        
        # Store initial message if provided
        if initial_prompt:
            store_message(session_id, 'user', initial_prompt, timestamp)
        
        # Store AI response
        ai_timestamp = datetime.utcnow().isoformat() + 'Z'
        store_message(session_id, 'assistant', ai_response, ai_timestamp)
        
        return response(200, {
            'sessionId': session_id,
            'message': {
                'role': 'assistant',
                'content': ai_response,
                'timestamp': ai_timestamp
            },
            'conversationState': 'greeting'
        })
        
    except Exception as e:
        print(f"Error in start_conversation: {str(e)}")
        return response(500, {'error': str(e)})


def send_message(body):
    """Process user message and generate AI response"""
    try:
        session_id = body.get('sessionId')
        user_message = body.get('message')
        
        if not session_id or not user_message:
            return response(400, {'error': 'sessionId and message are required'})
        
        # Validate message
        user_message = validate_message(user_message)
        
        # Get conversation history
        messages = get_conversation_messages(session_id)
        
        # Get session info to retrieve user profile
        session_info = get_session_info(session_id)
        if not session_info:
            return response(404, {'error': 'Session not found'})
        
        user_profile = get_user_profile(session_info['userId'])
        
        # Add new user message
        timestamp = datetime.utcnow().isoformat() + 'Z'
        messages.append({'role': 'user', 'content': user_message})
        store_message(session_id, 'user', user_message, timestamp)
        
        # Generate AI response
        system_prompt = build_system_prompt(user_profile)
        ai_response = call_bedrock(messages, system_prompt)
        
        # Store AI response
        ai_timestamp = datetime.utcnow().isoformat() + 'Z'
        store_message(session_id, 'assistant', ai_response, ai_timestamp)
        
        # Update session last message time
        update_session_timestamp(session_id, ai_timestamp)
        
        return response(200, {
            'sessionId': session_id,
            'message': {
                'role': 'assistant',
                'content': ai_response,
                'timestamp': ai_timestamp
            }
        })
        
    except Exception as e:
        print(f"Error in send_message: {str(e)}")
        return response(500, {'error': str(e)})


def get_user_profile(user_id):
    """Retrieve user banking data from DynamoDB"""
    try:
        result = table.get_item(
            Key={
                'PK': f"USER#{user_id}",
                'SK': 'PROFILE'
            }
        )
        return result.get('Item')
    except Exception as e:
        print(f"Error getting user profile: {str(e)}")
        return None


def get_session_info(session_id):
    """Get session information"""
    try:
        # Query for session by sessionId
        response = table.query(
            IndexName='GSI1',  # We'll need to add this
            KeyConditionExpression='sessionId = :sid',
            ExpressionAttributeValues={':sid': session_id}
        )
        items = response.get('Items', [])
        return items[0] if items else None
    except:
        # Fallback: scan for session (not efficient but works for demo)
        response = table.scan(
            FilterExpression='sessionId = :sid',
            ExpressionAttributeValues={':sid': session_id}
        )
        items = response.get('Items', [])
        return items[0] if items else None


def get_conversation_messages(session_id):
    """Retrieve conversation history"""
    try:
        response = table.query(
            KeyConditionExpression='PK = :pk AND begins_with(SK, :sk)',
            ExpressionAttributeValues={
                ':pk': f"SESSION#{session_id}",
                ':sk': 'MSG#'
            }
        )
        
        messages = []
        for item in sorted(response.get('Items', []), key=lambda x: x['timestamp']):
            messages.append({
                'role': item['role'],
                'content': item['content']
            })
        
        return messages
    except Exception as e:
        print(f"Error getting conversation messages: {str(e)}")
        return []


def store_message(session_id, role, content, timestamp):
    """Store a message in DynamoDB"""
    try:
        item = {
            'PK': f"SESSION#{session_id}",
            'SK': f"MSG#{timestamp}",
            'entityType': 'message',
            'sessionId': session_id,
            'role': role,
            'content': content,
            'timestamp': timestamp
        }
        table.put_item(Item=item)
    except Exception as e:
        print(f"Error storing message: {str(e)}")


def update_session_timestamp(session_id, timestamp):
    """Update session's last message timestamp"""
    # This would require knowing the session's PK/SK, skipping for MVP
    pass


def build_system_prompt(user_profile):
    """Create system prompt with user profile"""
    return f"""You are Bloom AI, a compassionate financial advisor specializing in family planning guidance. 
You help banking customers understand the financial aspects of starting a family.

User Profile:
- Age: {user_profile.get('age')}
- Income: ${user_profile.get('income')}/year
- Location: {user_profile.get('location')}
- Gender: {user_profile.get('gender')}

Your responsibilities:
1. Ask thoughtful questions about family planning goals
2. Provide accurate cost estimates based on research data
3. Recommend appropriate financial products (savings, investments, loans)
4. Create personalized action plans with timelines
5. Maintain an empathetic, supportive tone

Available family planning methods: IVF, Adoption, Natural Conception, Surrogacy

Guidelines:
- Be empathetic when discussing sensitive topics
- Provide specific numbers and timelines when possible
- Reference user's banking data naturally
- Acknowledge limitations when uncertain
- Focus on actionable next steps
"""


def call_bedrock(messages, system_prompt):
    """Invoke Bedrock Claude model"""
    try:
        # Prepare the request
        request_body = {
            'anthropic_version': 'bedrock-2023-05-31',
            'max_tokens': 2000,
            'system': system_prompt,
            'messages': messages if messages else [{'role': 'user', 'content': 'Hello'}]
        }
        
        # Call Bedrock
        response = bedrock_client.invoke_model(
            modelId=BEDROCK_MODEL_ID,
            body=json.dumps(request_body)
        )
        
        # Parse response
        response_body = json.loads(response['body'].read())
        return response_body['content'][0]['text']
        
    except Exception as e:
        print(f"Error calling Bedrock: {str(e)}")
        return "I apologize, but I'm having trouble responding right now. Please try again in a moment."


def validate_message(message):
    """Validate user message"""
    if not message or not message.strip():
        raise ValueError("Message cannot be empty")
    if len(message) > 2000:
        raise ValueError("Message too long (max 2000 characters)")
    return message.strip()


def get_conversation_history(session_id):
    """Retrieve full conversation history"""
    try:
        messages = get_conversation_messages(session_id)
        return response(200, {'sessionId': session_id, 'messages': messages})
    except Exception as e:
        print(f"Error getting conversation history: {str(e)}")
        return response(500, {'error': str(e)})


def response(status_code, body):
    """Format API Gateway response"""
    return {
        'statusCode': status_code,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Methods': 'GET,POST,OPTIONS'
        },
        'body': json.dumps(body)
    }

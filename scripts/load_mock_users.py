import json
import boto3
from datetime import datetime

# Load mock users
with open('data/mock-users.json', 'r') as f:
    data = json.load(f)

# Initialize DynamoDB client
dynamodb = boto3.resource('dynamodb', region_name='us-west-2')
table = dynamodb.Table('bloom-ai-data')

# Load each user into DynamoDB
for user in data['users']:
    item = {
        'PK': f"USER#{user['userId']}",
        'SK': 'PROFILE',
        'entityType': 'user_profile',
        'userId': user['userId'],
        'age': user['age'],
        'income': user['income'],
        'location': user['location'],
        'gender': user['gender'],
        'createdAt': user['createdAt'],
        'updatedAt': datetime.utcnow().isoformat() + 'Z'
    }
    
    table.put_item(Item=item)
    print(f"Loaded user: {user['userId']}")

print(f"\nSuccessfully loaded {len(data['users'])} users into DynamoDB")

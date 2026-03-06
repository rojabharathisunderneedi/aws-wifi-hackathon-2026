# Bloom AI Backend

## AWS Resources Created

### S3 Bucket
- **Name**: `bloom-ai-research-1772798279`
- **Region**: us-west-2
- **Contents**:
  - `family-planning-costs.json` - Cost data for IVF, adoption, surrogacy, natural conception
  - `financial-products.json` - Bank products (savings, investments, loans)

### DynamoDB Table
- **Name**: `bloom-ai-data`
- **Region**: us-west-2
- **Schema**: Single-table design with PK/SK
- **Data**: 5 mock users loaded

### Lambda Function
- **Name**: `bloom-ai-conversation-handler`
- **Runtime**: Python 3.12
- **Memory**: 512 MB
- **Timeout**: 30 seconds
- **Handler**: `lambda_function.lambda_handler`

### IAM Role
- **Name**: `bloom-ai-lambda-role`
- **Permissions**:
  - Bedrock: InvokeModel
  - DynamoDB: GetItem, PutItem, UpdateItem, Query, Scan
  - S3: GetObject
  - CloudWatch: Logs

## Environment Variables

The Lambda function uses these environment variables:
- `DYNAMODB_TABLE_NAME`: bloom-ai-data
- `S3_RESEARCH_BUCKET`: bloom-ai-research-1772798279

## API Endpoints (To be configured via API Gateway)

### POST /conversation/start
Start a new conversation session.

**Request**:
```json
{
  "userId": "user_001",
  "initialPrompt": "I'm thinking about starting a family"
}
```

**Response**:
```json
{
  "sessionId": "sess_abc123",
  "message": {
    "role": "assistant",
    "content": "AI response...",
    "timestamp": "2024-01-15T14:30:15Z"
  },
  "conversationState": "greeting"
}
```

### POST /conversation/message
Send a message in an existing conversation.

**Request**:
```json
{
  "sessionId": "sess_abc123",
  "message": "Tell me about IVF costs"
}
```

**Response**:
```json
{
  "sessionId": "sess_abc123",
  "message": {
    "role": "assistant",
    "content": "AI response...",
    "timestamp": "2024-01-15T14:32:30Z"
  }
}
```

### GET /conversation/{sessionId}
Retrieve conversation history.

**Response**:
```json
{
  "sessionId": "sess_abc123",
  "messages": [
    {"role": "user", "content": "..."},
    {"role": "assistant", "content": "..."}
  ]
}
```

## Testing Locally

You can test the Lambda function locally using the AWS SAM CLI or by invoking it directly:

```bash
aws lambda invoke \
  --function-name bloom-ai-conversation-handler \
  --payload '{"httpMethod":"POST","path":"/conversation/start","body":"{\"userId\":\"user_001\",\"initialPrompt\":\"Hello\"}"}' \
  --region us-west-2 \
  response.json
```

## Next Steps

1. **Enable Bedrock Access**: Ensure Bedrock model access is enabled in your AWS account
2. **Create API Gateway**: Set up API Gateway to expose Lambda endpoints
3. **Test Integration**: Test the complete flow from API Gateway to Lambda
4. **Add Error Handling**: Enhance error handling and validation
5. **Implement Remaining Features**: Add cost calculation, recommendations, etc.

## Mock Users Available

- user_001: Female, 32, $85k, Seattle, WA
- user_002: Male, 28, $72k, Austin, TX
- user_003: Non-binary, 35, $95k, Boston, MA
- user_004: Female, 29, $68k, Denver, CO
- user_005: Male, 38, $110k, San Francisco, CA

#!/bin/bash

# Configuration
FUNCTION_NAME="bloom-ai-conversation-handler"
REGION="us-west-2"
ROLE_NAME="bloom-ai-lambda-role"
S3_BUCKET="bloom-ai-research-1772798279"
TABLE_NAME="bloom-ai-data"

echo "Creating Lambda deployment package..."
cd backend
pip3 install -r requirements.txt -t package/
cp lambda_function.py package/
cd package
zip -r ../lambda_function.zip .
cd ..
rm -rf package

echo "Deployment package created: lambda_function.zip"
echo ""
echo "To deploy, run:"
echo "aws lambda create-function \\"
echo "  --function-name $FUNCTION_NAME \\"
echo "  --runtime python3.12 \\"
echo "  --role arn:aws:iam::\$(aws sts get-caller-identity --query Account --output text):role/$ROLE_NAME \\"
echo "  --handler lambda_function.lambda_handler \\"
echo "  --zip-file fileb://lambda_function.zip \\"
echo "  --timeout 30 \\"
echo "  --memory-size 512 \\"
echo "  --environment Variables={DYNAMODB_TABLE_NAME=$TABLE_NAME,S3_RESEARCH_BUCKET=$S3_BUCKET,AWS_REGION=$REGION} \\"
echo "  --region $REGION"

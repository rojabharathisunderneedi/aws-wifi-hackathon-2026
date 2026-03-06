#!/bin/bash

ROLE_NAME="bloom-ai-lambda-role"
REGION="us-west-2"

echo "Creating IAM role for Lambda..."

# Create trust policy
cat > /tmp/trust-policy.json << EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
EOF

# Create the role
aws iam create-role \
  --role-name $ROLE_NAME \
  --assume-role-policy-document file:///tmp/trust-policy.json

# Create policy document
cat > /tmp/lambda-policy.json << EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "bedrock:InvokeModel",
        "bedrock:InvokeModelWithResponseStream"
      ],
      "Resource": "arn:aws:bedrock:*::foundation-model/anthropic.claude-3-5-sonnet-*"
    },
    {
      "Effect": "Allow",
      "Action": [
        "dynamodb:GetItem",
        "dynamodb:PutItem",
        "dynamodb:UpdateItem",
        "dynamodb:Query",
        "dynamodb:Scan"
      ],
      "Resource": "arn:aws:dynamodb:$REGION:*:table/bloom-ai-data"
    },
    {
      "Effect": "Allow",
      "Action": [
        "s3:GetObject"
      ],
      "Resource": "arn:aws:s3:::bloom-ai-research-*/*"
    },
    {
      "Effect": "Allow",
      "Action": [
        "logs:CreateLogGroup",
        "logs:CreateLogStream",
        "logs:PutLogEvents"
      ],
      "Resource": "arn:aws:logs:*:*:*"
    }
  ]
}
EOF

# Attach the policy
aws iam put-role-policy \
  --role-name $ROLE_NAME \
  --policy-name bloom-ai-lambda-policy \
  --policy-document file:///tmp/lambda-policy.json

echo "IAM role created: $ROLE_NAME"
echo "Waiting 10 seconds for role to propagate..."
sleep 10

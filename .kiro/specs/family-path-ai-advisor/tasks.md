# Implementation Plan: Bloom AI

## Overview

This implementation plan breaks down the Bloom AI family planning financial advisor into discrete coding tasks optimized for a 4-hour hackathon delivery. The plan follows the AWS serverless architecture with Lambda, API Gateway, DynamoDB, S3, and Bedrock. Tasks are organized to enable parallel development across team members while ensuring incremental validation of core functionality.

The implementation uses Python 3.12 for Lambda functions and focuses on delivering one complete user journey: landing page → conversation → cost estimates → financial recommendations.

## Tasks

- [ ] 1. Set up AWS infrastructure and data preparation
  - [ ] 1.1 Create and configure DynamoDB table with schema
    - Create table `bloom-ai-data` with PK/SK structure
    - Enable encryption at rest
    - Add sample user banking data (3-5 mock users)
    - _Requirements: 2.1, 2.2, 2.3, 2.4, 11.3_
  
  - [ ] 1.2 Prepare and upload research data to S3
    - Create S3 bucket `bloom-ai-research`
    - Upload `family-planning-costs.json` with IVF, adoption, natural, surrogacy data
    - Upload `financial-products.json` with savings accounts, investments, loans
    - Verify file accessibility from Lambda
    - _Requirements: 4.1, 4.2, 4.3, 5.2_
  
  - [ ] 1.3 Configure IAM roles and Bedrock access
    - Create Lambda execution role with DynamoDB, S3, Bedrock, CloudWatch permissions
    - Enable Bedrock model access for Claude 3.5 Sonnet
    - Test Bedrock API connectivity
    - _Requirements: 11.1, 13.2_

- [ ] 2. Implement core Lambda conversation handler
  - [ ] 2.1 Create Lambda function structure and routing
    - Set up Python 3.12 Lambda function with handler
    - Implement request routing for `/conversation/start`, `/conversation/message`, `/conversation/{sessionId}`
    - Add environment variable configuration (table name, bucket name, model ID)
    - Configure 512MB memory and 30s timeout
    - _Requirements: 13.1_
  
  - [ ] 2.2 Implement user profile retrieval from DynamoDB
    - Write `get_user_profile(user_id)` function
    - Query DynamoDB for user banking data (age, income, location, gender)
    - Return complete User_Profile object
    - Handle missing user gracefully
    - _Requirements: 2.1, 2.2, 2.3, 2.4, 2.5_
  
  - [ ]* 2.3 Write property test for complete user profile creation
    - **Property 2: Complete User Profile Creation**
    - **Validates: Requirements 2.1, 2.2, 2.3, 2.4, 2.5**
    - Generate random valid user data (age 18-100, positive income, valid locations, genders)
    - Verify User_Profile contains all four banking fields
    - Run 100 iterations with hypothesis
  
  - [ ] 2.3 Implement research data retrieval from S3
    - Write `get_research_data(method_type=None)` function
    - Load and parse JSON from S3 bucket
    - Filter by method type if specified
    - Cache data in Lambda memory for performance
    - _Requirements: 4.1, 4.2, 4.4_
  
  - [ ]* 2.4 Write property test for research data retrieval
    - **Property 4: Research Data Retrieval for Recommendations**
    - **Validates: Requirements 4.1, 4.2, 4.4**
    - Test with all family planning methods (IVF, adoption, natural, surrogacy)
    - Verify both timeline and cost data are retrieved
    - Verify method-specific data is correctly filtered

- [ ] 3. Implement conversation session management
  - [ ] 3.1 Implement conversation start endpoint
    - Write `start_conversation(user_id, initial_prompt)` function
    - Generate unique session ID
    - Create session record in DynamoDB
    - Load user banking profile
    - Return session ID and initial context
    - _Requirements: 1.2, 7.1_
  
  - [ ]* 3.2 Write property test for prompt selection initiates conversation
    - **Property 1: Prompt Selection Initiates Conversation**
    - **Validates: Requirements 1.2**
    - Generate random conversation prompts
    - Verify session is created with prompt in context
    - Verify session ID is returned
  
  - [ ] 3.3 Implement conversation context storage and retrieval
    - Write `update_conversation_context(session_id, new_data)` function
    - Store conversation messages in DynamoDB with timestamps
    - Write `get_conversation_context(session_id)` function
    - Maintain conversation state (greeting, discovery, recommendation, action_plan)
    - _Requirements: 7.1, 7.2, 7.3_
  
  - [ ]* 3.4 Write property test for conversation context persistence
    - **Property 8: Conversation Context Persistence**
    - **Validates: Requirements 7.1, 7.2, 7.3**
    - Generate random conversation sequences
    - Verify all previous messages are maintained in context
    - Verify context is accessible across multiple message exchanges
  
  - [ ]* 3.5 Write property test for conversation context updates profile
    - **Property 3: Conversation Context Updates Profile**
    - **Validates: Requirements 3.2, 3.3, 3.4, 3.5**
    - Generate random user-provided information (relationship status, life changes, location)
    - Verify User_Profile is updated with all collected data
    - Verify updates persist in DynamoDB

- [ ] 4. Integrate Amazon Bedrock for AI conversations
  - [ ] 4.1 Implement Bedrock API integration
    - Write `call_bedrock(messages, system_prompt)` function
    - Configure boto3 Bedrock client
    - Implement message formatting for Claude API
    - Handle streaming vs non-streaming responses
    - Add retry logic with exponential backoff (3 retries)
    - _Requirements: 12.1, 12.2, 13.2_
  
  - [ ] 4.2 Create system prompt template with user profile injection
    - Write `build_system_prompt(user_profile, research_summary, product_summary)` function
    - Include user age, income, location, gender in prompt
    - Add empathetic tone instructions
    - Include available family planning methods
    - Add research data summary and product catalog summary
    - _Requirements: 12.2, 12.3_
  
  - [ ] 4.3 Implement message handling endpoint
    - Write `send_message(session_id, user_message)` function
    - Validate session ID and message content
    - Retrieve conversation history
    - Build complete message array for Bedrock
    - Call Bedrock with system prompt and messages
    - Store AI response in conversation context
    - Return formatted response
    - _Requirements: 3.1, 12.1, 12.3_
  
  - [ ]* 4.4 Write property test for limitation acknowledgment
    - **Property 15: Limitation Acknowledgment**
    - **Validates: Requirements 12.4**
    - Generate random out-of-domain questions (weather, sports, politics)
    - Verify AI response acknowledges limitations
    - Verify response doesn't provide false information

- [ ] 5. Checkpoint - Test core conversation flow
  - Ensure all tests pass, ask the user if questions arise.

- [ ] 6. Implement financial recommendation generation
  - [ ] 6.1 Implement product catalog retrieval and filtering
    - Write `get_product_catalog(user_profile)` function
    - Load financial products from S3
    - Filter products by user income and age eligibility
    - Return relevant savings accounts, investments, loans
    - _Requirements: 5.2_
  
  - [ ] 6.2 Implement recommendation generation logic
    - Write `generate_recommendations(user_profile, conversation_context)` function
    - Analyze user timeline and family planning method
    - Match products to user needs (savings for short-term, investments for long-term, loans for high costs)
    - Calculate monthly savings targets based on costs and timeline
    - Create recommendation objects with rationale
    - Store recommendations in DynamoDB
    - _Requirements: 5.1, 5.3, 5.4, 5.5, 5.6_
  
  - [ ]* 6.3 Write property test for recommendation generation from complete profiles
    - **Property 5: Recommendation Generation from Complete Profiles**
    - **Validates: Requirements 5.1, 5.2**
    - Generate random complete user profiles with sufficient data
    - Verify at least one financial recommendation is generated
    - Verify product catalog is queried
    - Verify recommendations reference actual products
  
  - [ ]* 6.4 Write property test for contextual product recommendations
    - **Property 6: Contextual Product Recommendations**
    - **Validates: Requirements 5.3, 5.4, 5.5, 5.6**
    - Generate random user profiles with varying timelines and financial situations
    - Verify savings accounts recommended for short/medium timelines
    - Verify investments recommended for long timelines
    - Verify loans recommended for high costs with qualifying income
    - Verify recommendations match user context

- [ ] 7. Implement cost estimation and localization
  - [ ] 7.1 Implement cost calculation with location factors
    - Write `calculate_localized_cost(method_type, location)` function
    - Retrieve base cost range from research data
    - Apply location factor (urban 1.2x, suburban 1.0x, rural 0.85x)
    - Calculate total cost including additional expenses
    - Return cost estimate with currency and timeline
    - _Requirements: 6.1, 6.2, 6.3, 6.4_
  
  - [ ]* 7.2 Write property test for localized cost estimates
    - **Property 7: Localized Cost Estimates**
    - **Validates: Requirements 6.1, 6.2, 6.3**
    - Generate random family planning methods and locations
    - Verify location factor is applied to base cost
    - Verify timeline information is included
    - Verify cost is in correct currency format
  
  - [ ] 7.3 Implement multi-method comparison
    - Write `compare_methods(methods_list, user_location)` function
    - Calculate costs for multiple methods
    - Compare timelines across methods
    - Format comparison data for AI response
    - _Requirements: 9.1, 9.2, 9.3_
  
  - [ ]* 7.4 Write property test for multi-method comparison data
    - **Property 10: Multi-Method Comparison Data**
    - **Validates: Requirements 9.1, 9.2, 9.3**
    - Generate random method combinations
    - Verify cost ranges provided for each method
    - Verify timeline information provided for each method
    - Verify comparison includes multiple methods
  
  - [ ]* 7.5 Write property test for exploratory information for undecided users
    - **Property 11: Exploratory Information for Undecided Users**
    - **Validates: Requirements 9.4**
    - Test conversations without specified method preference
    - Verify information covers all four methods (IVF, adoption, natural, surrogacy)
    - Verify exploratory tone in responses

- [ ] 8. Implement action plan generation
  - [ ] 8.1 Create action plan generation logic
    - Write `generate_action_plan(user_profile, conversation_context, recommendations)` function
    - Include financial recommendations with product details
    - Calculate timeline milestones based on family planning method
    - Calculate savings targets from cost data and user income
    - Format action plan for AI to present
    - _Requirements: 8.1, 8.2, 8.3, 8.4_
  
  - [ ]* 8.2 Write property test for complete action plan generation
    - **Property 9: Complete Action Plan Generation**
    - **Validates: Requirements 8.1, 8.2, 8.3, 8.4**
    - Generate random user profiles with sufficient data
    - Verify action plan includes financial recommendations
    - Verify action plan includes timeline milestones
    - Verify action plan includes savings targets
    - Verify savings targets calculated from cost and income

- [ ] 9. Implement API Gateway integration
  - [ ] 9.1 Create API Gateway REST API
    - Create REST API named `bloom-ai-api`
    - Configure CORS for web access
    - Set up regional endpoint
    - _Requirements: 10.1, 10.2_
  
  - [ ] 9.2 Configure API Gateway endpoints and Lambda integration
    - Create POST `/conversation/start` endpoint with Lambda proxy integration
    - Create POST `/conversation/message` endpoint with Lambda proxy integration
    - Create GET `/conversation/{sessionId}` endpoint with Lambda proxy integration
    - Configure request/response models
    - Add API key authentication for MVP
    - Deploy API to stage
    - _Requirements: 1.2, 11.1_
  
  - [ ] 9.3 Update Lambda handler for API Gateway event format
    - Parse API Gateway event structure
    - Extract path, HTTP method, body, and path parameters
    - Route requests to appropriate functions
    - Format responses with proper HTTP status codes and headers
    - Add CORS headers to responses
    - _Requirements: 10.1, 10.2_

- [ ] 10. Checkpoint - Test backend integration
  - Ensure all tests pass, ask the user if questions arise.

- [ ] 11. Build frontend landing page and conversation UI
  - [ ] 11.1 Create landing page HTML structure
    - Create `index.html` with landing page layout
    - Add header with Bloom AI branding
    - Create section for suggested conversation prompts
    - Add free-form text input area
    - Create conversation display area
    - _Requirements: 1.1, 1.3, 1.4, 10.3_
  
  - [ ] 11.2 Style landing page with CSS
    - Create `styles.css` for landing page
    - Style conversation prompts as clickable cards
    - Style conversation messages (user vs AI)
    - Add responsive design for mobile compatibility
    - Match banking app branding colors
    - _Requirements: 1.3, 10.1, 10.2, 10.3_
  
  - [ ] 11.3 Implement frontend JavaScript for API integration
    - Create `app.js` for frontend logic
    - Implement prompt selection handler
    - Implement conversation start API call
    - Implement message sending API call
    - Implement conversation display rendering
    - Add loading indicators during API calls
    - Handle API errors gracefully
    - _Requirements: 1.2, 1.4, 7.2_
  
  - [ ]* 11.4 Write unit test for landing page displays three prompts
    - Test that landing page HTML contains at least 3 prompt elements
    - Verify prompts are visible and clickable
    - _Requirements: 1.1_
  
  - [ ]* 11.5 Write unit test for free-form input option
    - Test that landing page provides text input field
    - Verify input field is functional
    - _Requirements: 1.4_

- [ ] 12. Implement session resumption and context preservation
  - [ ] 12.1 Implement conversation history retrieval endpoint
    - Write `get_conversation_history(session_id)` function
    - Query DynamoDB for all messages in session
    - Return messages in chronological order
    - Include conversation state and collected info
    - _Requirements: 7.1, 10.4_
  
  - [ ]* 12.2 Write property test for session resumption preserves context
    - **Property 12: Session Resumption Preserves Context**
    - **Validates: Requirements 10.4**
    - Generate random conversation sessions
    - Simulate navigation away and return
    - Verify all conversation context is preserved
    - Verify messages are retrievable after resumption

- [ ] 13. Add error handling and validation
  - [ ] 13.1 Implement input validation
    - Write `validate_message(message)` function for empty/long messages
    - Write `validate_session_id(session_id)` function for format checking
    - Write `validate_user_profile(profile)` function for required fields
    - Add validation to all API endpoints
    - Return user-friendly error messages
    - _Requirements: 12.4_
  
  - [ ] 13.2 Implement error handling for AWS services
    - Add try-catch blocks for DynamoDB operations
    - Add try-catch blocks for S3 operations
    - Add try-catch blocks for Bedrock API calls
    - Implement graceful degradation for data unavailability
    - Add CloudWatch logging for all errors
    - _Requirements: 12.4_
  
  - [ ] 13.3 Implement retry logic and circuit breaker
    - Add exponential backoff retry for Bedrock (3 retries)
    - Add retry with jitter for DynamoDB (2 retries)
    - Add retry for S3 reads (2 retries)
    - Implement circuit breaker for Bedrock failures (5 failures in 60s)
    - Add fallback responses when circuit breaker opens
    - _Requirements: 13.1_
  
  - [ ]* 13.4 Write unit tests for error handling
    - Test empty message validation
    - Test invalid session ID handling
    - Test missing user profile handling
    - Test Bedrock API timeout handling
    - Test S3 data unavailability handling
    - Verify user-friendly error messages

- [ ] 14. Add security and encryption
  - [ ] 14.1 Configure encryption for data at rest
    - Enable DynamoDB encryption with KMS
    - Verify S3 bucket encryption settings
    - _Requirements: 11.3_
  
  - [ ] 14.2 Configure encryption for data in transit
    - Verify API Gateway uses HTTPS
    - Verify Lambda to AWS services uses TLS
    - Add HTTPS enforcement to API Gateway
    - _Requirements: 11.2_
  
  - [ ]* 14.3 Write unit tests for security configuration
    - Test DynamoDB encryption is enabled
    - Test HTTPS is enforced on API Gateway
    - _Requirements: 11.2, 11.3_
  
  - [ ] 14.4 Implement secure conversation context storage
    - Write `store_conversation_securely(session_id, context)` function
    - Encrypt sensitive data before storing in DynamoDB
    - Add data retention policy logic
    - _Requirements: 11.4_
  
  - [ ]* 14.5 Write property test for authenticated data access
    - **Property 13: Authenticated Data Access**
    - **Validates: Requirements 11.1**
    - Test all banking data access calls
    - Verify authentication credentials are included
    - Verify unauthorized access is rejected

- [ ] 15. End-to-end integration and testing
  - [ ] 15.1 Deploy complete system to AWS
    - Deploy Lambda function with all code
    - Deploy API Gateway with all endpoints
    - Upload frontend to S3 static hosting (or test locally)
    - Verify all AWS service connections
    - _Requirements: 13.1, 13.2_
  
  - [ ] 15.2 Run end-to-end user journey test
    - Test landing page loads with prompts
    - Test prompt selection starts conversation
    - Test AI responds with personalized information
    - Test cost estimates are displayed
    - Test financial recommendation is generated
    - Test complete flow from start to action plan
    - _Requirements: 13.4_
  
  - [ ]* 15.3 Write integration test for complete user journey
    - Test full flow: landing page → conversation → cost → recommendation
    - Verify all components work together
    - Verify data flows correctly through all services
    - _Requirements: 13.4_
  
  - [ ] 15.4 Run all property-based tests with full iterations
    - Execute all 15 property tests with 100 iterations each
    - Review test results and fix any failures
    - Generate test coverage report
    - Verify all correctness properties hold

- [ ] 16. Final checkpoint and demo preparation
  - Ensure all tests pass, ask the user if questions arise.

- [ ] 17. Prepare demo materials and documentation
  - [ ] 17.1 Create demo script and test scenarios
    - Write step-by-step demo script for presentation
    - Prepare 2-3 test user scenarios (IVF, adoption, comparison)
    - Document expected outputs for each scenario
    - _Requirements: 13.4_
  
  - [ ] 17.2 Create architecture diagram
    - Create visual diagram of AWS services and data flow
    - Document API endpoints and request/response formats
    - Document DynamoDB schema and S3 structure
  
  - [ ] 17.3 Write deployment and setup documentation
    - Document AWS service configuration steps
    - Document environment variables and secrets
    - Document how to run tests locally
    - Document API usage examples

## Notes

- Tasks marked with `*` are optional property-based and unit tests that can be skipped for faster MVP delivery
- Each task references specific requirements for traceability
- Checkpoints ensure incremental validation at critical integration points
- Property tests validate universal correctness properties across randomized inputs
- Unit tests validate specific examples, edge cases, and configuration
- The plan is optimized for parallel development across 5 team members during a 4-hour hackathon
- Focus on tasks 1-11 for core demo functionality; tasks 12-17 add polish and robustness
- All 15 correctness properties from the design document are covered by property-based tests

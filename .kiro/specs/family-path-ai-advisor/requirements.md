# Requirements Document

## Introduction

Bloom AI is an agentic AI tool that helps personal banking users make informed decisions about their personalized next steps to create a family. The system integrates research data on family planning methods, personal banking data, and conversational information to provide tailored financial guidance. The tool is delivered as a conversational interface within the mobile/online banking app, accessible via a landing page with suggested conversation prompts.

This is an MVP designed for a 4-hour hackathon delivery timeframe, focusing on demonstrating core concept viability using AWS services.

## Glossary

- **Bloom_AI**: The complete agentic AI system that provides family planning financial guidance
- **Conversation_Agent**: The AI component that conducts natural language conversations with users
- **Data_Integration_Service**: The service that retrieves and combines data from multiple sources
- **Banking_Repository**: The system storing user banking data (gender, age, location, income)
- **Research_Database**: Third-party data source containing family planning information and costs
- **Product_Catalog**: The repository of bank financial products and services
- **User_Profile**: The combined data representation of a user including banking and conversational data
- **Landing_Page**: The entry interface displaying suggested conversation prompts
- **Family_Planning_Method**: A specific approach to starting a family (IVF, adoption, natural, surrogacy)
- **Financial_Recommendation**: A suggested financial product or savings strategy tailored to user goals
- **Conversation_Context**: The accumulated information collected during a chat session

## Requirements

### Requirement 1: Display Landing Page with Conversation Prompts

**User Story:** As a banking user, I want to see a landing page with suggested prompts, so that I can easily start a conversation about family planning.

#### Acceptance Criteria

1. WHEN a user accesses the Bloom AI feature, THE Landing_Page SHALL display at least 3 suggested conversation prompts
2. WHEN a user selects a prompt, THE Conversation_Agent SHALL initiate a conversation using that prompt as context
3. THE Landing_Page SHALL display within the mobile or online banking app interface
4. THE Landing_Page SHALL provide an option to start a free-form conversation without selecting a prompt

### Requirement 2: Retrieve User Banking Data

**User Story:** As the system, I want to retrieve user banking data, so that I can provide personalized recommendations.

#### Acceptance Criteria

1. WHEN a conversation is initiated, THE Data_Integration_Service SHALL retrieve the user's gender from the Banking_Repository
2. WHEN a conversation is initiated, THE Data_Integration_Service SHALL retrieve the user's age from the Banking_Repository
3. WHEN a conversation is initiated, THE Data_Integration_Service SHALL retrieve the user's location from the Banking_Repository
4. WHEN a conversation is initiated, THE Data_Integration_Service SHALL retrieve the user's income from the Banking_Repository
5. THE Data_Integration_Service SHALL create a User_Profile combining all retrieved banking data

### Requirement 3: Collect Personal Information Through Conversation

**User Story:** As a user, I want to share my family planning goals through conversation, so that I receive relevant guidance.

#### Acceptance Criteria

1. WHEN a conversation begins, THE Conversation_Agent SHALL ask about the user's family planning goal
2. THE Conversation_Agent SHALL collect information about whether the user is single or with partner(s)
3. THE Conversation_Agent SHALL collect information about big life changes affecting family planning
4. THE Conversation_Agent SHALL collect information about current living location if different from Banking_Repository data
5. THE Conversation_Agent SHALL update the User_Profile with all collected Conversation_Context

### Requirement 4: Access Research Data on Family Planning

**User Story:** As the system, I want to access third-party research data, so that I can provide accurate family planning information.

#### Acceptance Criteria

1. WHEN generating recommendations, THE Data_Integration_Service SHALL retrieve family planning timeline data from the Research_Database
2. WHEN generating recommendations, THE Data_Integration_Service SHALL retrieve cost data for the relevant Family_Planning_Method from the Research_Database
3. THE Research_Database SHALL contain information on IVF, adoption, natural conception, and surrogacy methods
4. WHEN a specific Family_Planning_Method is discussed, THE Data_Integration_Service SHALL retrieve method-specific information

### Requirement 5: Provide Financial Product Recommendations

**User Story:** As a user, I want to receive personalized financial product recommendations, so that I can prepare financially for starting a family.

#### Acceptance Criteria

1. WHEN the Conversation_Agent has sufficient User_Profile data, THE Conversation_Agent SHALL generate at least one Financial_Recommendation
2. THE Conversation_Agent SHALL retrieve available products from the Product_Catalog
3. THE Conversation_Agent SHALL recommend saving accounts when appropriate for the user's timeline
4. THE Conversation_Agent SHALL recommend investment opportunities when appropriate for the user's timeline
5. THE Conversation_Agent SHALL recommend loans when appropriate for the user's financial situation
6. WHEN generating recommendations, THE Conversation_Agent SHALL consider the user's income, age, and family planning goal

### Requirement 6: Calculate Cost Estimates

**User Story:** As a user, I want to understand the costs associated with my chosen family planning method, so that I can plan my finances accordingly.

#### Acceptance Criteria

1. WHEN a user specifies a Family_Planning_Method, THE Conversation_Agent SHALL provide cost estimates for that method
2. THE Conversation_Agent SHALL combine Research_Database cost data with the user's location to provide localized estimates
3. WHEN providing cost estimates, THE Conversation_Agent SHALL include a timeline for expected expenses
4. THE Conversation_Agent SHALL present cost information in the user's local currency

### Requirement 7: Maintain Conversation Context

**User Story:** As a user, I want the system to remember what I've shared during our conversation, so that I don't have to repeat myself.

#### Acceptance Criteria

1. WHILE a conversation is active, THE Conversation_Agent SHALL maintain all Conversation_Context
2. WHEN a user provides information, THE Conversation_Agent SHALL reference previously shared information in subsequent responses
3. THE Conversation_Agent SHALL update the User_Profile as new information is collected during the conversation

### Requirement 8: Generate Personalized Action Plans

**User Story:** As a user, I want to receive a personalized action plan, so that I know what steps to take next.

#### Acceptance Criteria

1. WHEN sufficient User_Profile data is collected, THE Conversation_Agent SHALL generate a personalized action plan
2. THE Conversation_Agent SHALL include specific Financial_Recommendation items in the action plan
3. THE Conversation_Agent SHALL include timeline milestones based on the user's family planning goal
4. THE Conversation_Agent SHALL include estimated savings targets based on cost data and user income

### Requirement 9: Handle Multiple Family Planning Methods

**User Story:** As a user exploring options, I want to compare different family planning methods, so that I can make an informed decision.

#### Acceptance Criteria

1. WHEN a user requests comparison information, THE Conversation_Agent SHALL provide data on multiple Family_Planning_Method options
2. THE Conversation_Agent SHALL compare costs across different Family_Planning_Method options
3. THE Conversation_Agent SHALL compare timelines across different Family_Planning_Method options
4. WHERE a user has not yet decided on a method, THE Conversation_Agent SHALL provide exploratory information on all available methods

### Requirement 10: Integrate with Banking App Interface

**User Story:** As a user, I want to access FamilyPath AI within my banking app, so that I have a seamless experience.

#### Acceptance Criteria

1. THE Bloom_AI SHALL be accessible from within the mobile banking app
2. THE Bloom_AI SHALL be accessible from within the online banking app
3. THE Bloom_AI SHALL maintain consistent branding with the banking app interface
4. WHEN a user navigates away from the conversation, THE Conversation_Agent SHALL preserve the Conversation_Context for later resumption

### Requirement 11: Handle Sensitive Data Securely

**User Story:** As a user, I want my personal and financial data to be handled securely, so that my privacy is protected.

#### Acceptance Criteria

1. WHEN accessing Banking_Repository data, THE Data_Integration_Service SHALL use authenticated and authorized connections
2. THE Bloom_AI SHALL encrypt all User_Profile data in transit
3. THE Bloom_AI SHALL encrypt all User_Profile data at rest
4. WHEN a conversation ends, THE Conversation_Agent SHALL store Conversation_Context securely in accordance with data retention policies

### Requirement 12: Provide Natural Language Responses

**User Story:** As a user, I want to have natural conversations with the AI, so that the experience feels helpful and human.

#### Acceptance Criteria

1. WHEN responding to user input, THE Conversation_Agent SHALL generate natural language responses
2. THE Conversation_Agent SHALL adapt its tone to be empathetic and supportive when discussing family planning
3. WHEN a user asks a question, THE Conversation_Agent SHALL provide relevant answers based on available data sources
4. IF the Conversation_Agent cannot answer a question, THEN THE Conversation_Agent SHALL clearly communicate its limitations

### Requirement 13: Support MVP Delivery Timeline

**User Story:** As a hackathon team, we want to deliver a working demo in 4 hours, so that we can demonstrate the core concept.

#### Acceptance Criteria

1. THE Bloom_AI SHALL implement core conversational capabilities sufficient for demonstration
2. THE Bloom_AI SHALL integrate with at least one AWS service for AI capabilities
3. THE Bloom_AI SHALL use mock or simplified data sources where full integration is not feasible within 4 hours
4. THE Bloom_AI SHALL demonstrate at least one complete user journey from landing page to financial recommendation


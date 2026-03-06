// Bloom AI Configuration
const CONFIG = {
    // API Configuration
    API_BASE_URL: 'https://eczxb4xbrjcadh7v5ojujd3m5y0moefz.lambda-url.us-west-2.on.aws',
    API_KEY: '', // Not needed for Lambda Function URLs
    
    // User Configuration
    DEFAULT_USER_ID: 'user_001', // Using our mock user from DynamoDB
    
    // Feature Flags
    ENABLE_MOCK_MODE: false, // Using real Lambda backend
    ENABLE_DEBUG_LOGGING: true,
    
    // UI Configuration
    MAX_MESSAGE_LENGTH: 500,
    TYPING_INDICATOR_DELAY: 1000,
    ERROR_MESSAGE_DURATION: 5000,
    
    // Conversation Settings
    MAX_CONVERSATION_HISTORY: 50,
    AUTO_SCROLL_ENABLED: true,
    
    // Timeouts
    API_TIMEOUT: 30000,
    RETRY_ATTEMPTS: 3,
    RETRY_DELAY: 1000
};

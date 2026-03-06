// Configuration Example
// Copy this file to config.js and update with your actual values

const CONFIG = {
    // API Configuration
    API_BASE_URL: 'https://your-api-gateway-url.amazonaws.com/prod',
    API_KEY: 'your-api-key-here',
    
    // User Configuration (in production, get from auth system)
    DEFAULT_USER_ID: 'demo-user-123',
    
    // Feature Flags
    ENABLE_MOCK_MODE: false, // Set to true to use mock responses
    ENABLE_DEBUG_LOGGING: false,
    
    // UI Configuration
    MAX_MESSAGE_LENGTH: 500,
    TYPING_INDICATOR_DELAY: 1000, // ms
    ERROR_MESSAGE_DURATION: 5000, // ms
    
    // Conversation Settings
    MAX_CONVERSATION_HISTORY: 50, // messages
    AUTO_SCROLL_ENABLED: true,
    
    // Timeouts
    API_TIMEOUT: 30000, // 30 seconds
    RETRY_ATTEMPTS: 3,
    RETRY_DELAY: 1000 // ms
};

// Export for use in app.js
if (typeof module !== 'undefined' && module.exports) {
    module.exports = CONFIG;
}

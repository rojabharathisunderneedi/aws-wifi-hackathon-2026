// Configuration
const API_BASE_URL = 'https://api.bloom-ai.example.com/v1'; // Update with actual API Gateway URL
const API_KEY = 'your-api-key-here'; // Update with actual API key

// State management
let currentSessionId = null;
let currentUserId = 'demo-user-123'; // In production, this would come from authentication

// DOM Elements
const landingPage = document.getElementById('landingPage');
const conversationPage = document.getElementById('conversationPage');
const conversationMessages = document.getElementById('conversationMessages');
const messageInput = document.getElementById('messageInput');
const sendButton = document.getElementById('sendButton');
const backButton = document.getElementById('backButton');
const customPromptInput = document.getElementById('customPromptInput');
const customPromptButton = document.getElementById('customPromptButton');
const loadingIndicator = document.getElementById('loadingIndicator');

// Initialize app
document.addEventListener('DOMContentLoaded', () => {
    setupEventListeners();
});

// Event Listeners
function setupEventListeners() {
    // Prompt card clicks (using new class name)
    document.querySelectorAll('.starter-card').forEach(card => {
        card.addEventListener('click', () => {
            const prompt = card.getAttribute('data-prompt');
            startConversation(prompt);
        });
    });

    // Custom prompt button
    customPromptButton.addEventListener('click', () => {
        const prompt = customPromptInput.value.trim();
        if (prompt) {
            startConversation(prompt);
        }
    });

    // Custom prompt input - Enter key
    customPromptInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            const prompt = customPromptInput.value.trim();
            if (prompt) {
                startConversation(prompt);
            }
        }
    });

    // Send message button
    sendButton.addEventListener('click', sendMessage);

    // Message input - Enter key
    messageInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });

    // Back button
    backButton.addEventListener('click', () => {
        showLandingPage();
    });
}

// Start a new conversation
async function startConversation(initialPrompt) {
    try {
        showLoading(true);

        const response = await fetch(`${API_BASE_URL}/conversation/start`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'x-api-key': API_KEY
            },
            body: JSON.stringify({
                userId: currentUserId,
                initialPrompt: initialPrompt
            })
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        currentSessionId = data.sessionId;

        // Clear conversation and show conversation page
        conversationMessages.innerHTML = '';
        showConversationPage();

        // Add user message
        addMessage('user', initialPrompt);

        // Add AI response
        if (data.message && data.message.content) {
            addMessage('assistant', data.message.content);
        }

        showLoading(false);
    } catch (error) {
        console.error('Error starting conversation:', error);
        showError('Failed to start conversation. Please try again.');
        showLoading(false);
    }
}

// Send a message in existing conversation
async function sendMessage() {
    const message = messageInput.value.trim();
    
    if (!message || !currentSessionId) {
        return;
    }

    try {
        // Add user message to UI immediately
        addMessage('user', message);
        messageInput.value = '';
        
        showLoading(true);
        disableInput(true);

        const response = await fetch(`${API_BASE_URL}/conversation/message`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'x-api-key': API_KEY
            },
            body: JSON.stringify({
                sessionId: currentSessionId,
                message: message
            })
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();

        // Add AI response
        if (data.message && data.message.content) {
            addMessage('assistant', data.message.content);
        }

        showLoading(false);
        disableInput(false);
        messageInput.focus();
    } catch (error) {
        console.error('Error sending message:', error);
        showError('Failed to send message. Please try again.');
        showLoading(false);
        disableInput(false);
    }
}

// Add message to conversation UI
function addMessage(role, content) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${role}`;

    const avatar = document.createElement('div');
    avatar.className = 'message-avatar';
    avatar.textContent = role === 'user' ? '👤' : '🤖';

    const messageContent = document.createElement('div');
    messageContent.className = 'message-content';
    messageContent.textContent = content;

    messageDiv.appendChild(avatar);
    messageDiv.appendChild(messageContent);

    conversationMessages.appendChild(messageDiv);
    
    // Scroll to bottom
    conversationMessages.scrollTop = conversationMessages.scrollHeight;
}

// Show/hide pages
function showConversationPage() {
    landingPage.classList.add('hidden');
    conversationPage.classList.remove('hidden');
    messageInput.focus();
}

function showLandingPage() {
    conversationPage.classList.add('hidden');
    landingPage.classList.remove('hidden');
    currentSessionId = null;
    customPromptInput.value = '';
}

// Show/hide loading indicator
function showLoading(show) {
    if (show) {
        loadingIndicator.classList.remove('hidden');
    } else {
        loadingIndicator.classList.add('hidden');
    }
}

// Enable/disable input
function disableInput(disabled) {
    messageInput.disabled = disabled;
    sendButton.disabled = disabled;
}

// Show error message
function showError(message) {
    const errorDiv = document.createElement('div');
    errorDiv.className = 'error-message';
    errorDiv.textContent = message;
    
    conversationMessages.appendChild(errorDiv);
    
    // Remove error after 5 seconds
    setTimeout(() => {
        errorDiv.remove();
    }, 5000);
    
    conversationMessages.scrollTop = conversationMessages.scrollHeight;
}

// Mock API for testing without backend
// Comment this section when connecting to real backend
async function startConversation(initialPrompt) {
    showLoading(true);
    
    currentSessionId = 'mock-session-' + Date.now();
    conversationMessages.innerHTML = '';
    showConversationPage();
    
    addMessage('user', initialPrompt);
    
    // Simulate API delay
    await new Promise(resolve => setTimeout(resolve, 1000));
    
    const mockResponse = `That's wonderful that you're planning ahead! Starting a family is an exciting journey. I'd love to help you understand the financial aspects and create a personalized plan. 

Based on your profile, I can see you're in a great position to start planning. Could you tell me a bit more about your situation? Are you planning this journey with a partner, or are you considering this on your own?`;
    
    addMessage('assistant', mockResponse);
    showLoading(false);
}

async function sendMessage() {
    const message = messageInput.value.trim();
    
    if (!message || !currentSessionId) {
        return;
    }
    
    addMessage('user', message);
    messageInput.value = '';
    
    showLoading(true);
    disableInput(true);
    
    // Simulate API delay
    await new Promise(resolve => setTimeout(resolve, 1500));
    
    const mockResponses = [
        "Thank you for sharing that. Based on what you've told me, I can provide some personalized guidance. Let me look into the costs and options available for your situation.",
        "That's a great question! The costs can vary depending on several factors including your location and specific circumstances. Let me break down the typical expenses you might expect.",
        "I understand this is an important decision. Based on your income and timeline, I can recommend some financial products that might help you prepare. Would you like to hear about savings accounts or investment options?"
    ];
    
    const randomResponse = mockResponses[Math.floor(Math.random() * mockResponses.length)];
    addMessage('assistant', randomResponse);
    
    showLoading(false);
    disableInput(false);
    messageInput.focus();
}

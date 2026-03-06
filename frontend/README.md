# Bloom AI Frontend

A conversational AI interface for family planning financial guidance.

## Features

- Landing page with suggested conversation prompts
- Real-time chat interface
- Responsive design for mobile and desktop
- Clean, banking-app aesthetic
- API integration ready

## Setup

### Quick Start (Mock Mode)

To test the frontend without a backend:

1. Open `app.js` and uncomment the mock API section at the bottom
2. Open `index.html` in a web browser
3. Click on any prompt or type your own message

### Production Setup

1. Update the API configuration in `app.js`:
   ```javascript
   const API_BASE_URL = 'https://your-api-gateway-url.com/v1';
   const API_KEY = 'your-api-key';
   ```

2. Deploy the frontend:
   - **Option 1**: Upload to S3 static website hosting
   - **Option 2**: Serve with any web server (nginx, Apache, etc.)
   - **Option 3**: Use a local development server

### Local Development Server

Using Python:
```bash
cd frontend
python -m http.server 8000
```

Using Node.js:
```bash
cd frontend
npx http-server -p 8000
```

Then open http://localhost:8000 in your browser.

## File Structure

```
frontend/
├── index.html      # Main HTML structure
├── styles.css      # Styling and responsive design
├── app.js          # JavaScript logic and API integration
└── README.md       # This file
```

## API Integration

The frontend expects the following API endpoints:

### POST /conversation/start
Start a new conversation session.

**Request:**
```json
{
  "userId": "string",
  "initialPrompt": "string"
}
```

**Response:**
```json
{
  "sessionId": "string",
  "message": {
    "role": "assistant",
    "content": "string",
    "timestamp": "string"
  },
  "conversationState": "string"
}
```

### POST /conversation/message
Send a message in an existing conversation.

**Request:**
```json
{
  "sessionId": "string",
  "message": "string"
}
```

**Response:**
```json
{
  "sessionId": "string",
  "message": {
    "role": "assistant",
    "content": "string",
    "timestamp": "string"
  },
  "conversationState": "string"
}
```

## Customization

### Branding

Update colors in `styles.css`:
```css
/* Primary gradient */
background: linear-gradient(135deg, #6B4CE6 0%, #8B5CF6 100%);

/* Change to your brand colors */
background: linear-gradient(135deg, #YOUR_COLOR_1 0%, #YOUR_COLOR_2 100%);
```

### Conversation Prompts

Edit prompts in `index.html`:
```html
<button class="prompt-card" data-prompt="Your custom prompt here">
    <span class="prompt-icon">🎯</span>
    <span class="prompt-text">Your custom prompt here</span>
</button>
```

### User Authentication

In production, replace the mock user ID in `app.js`:
```javascript
// Get from your authentication system
let currentUserId = getUserIdFromAuth();
```

## Browser Support

- Chrome/Edge (latest)
- Firefox (latest)
- Safari (latest)
- Mobile browsers (iOS Safari, Chrome Mobile)

## Accessibility

- Semantic HTML structure
- Keyboard navigation support
- ARIA labels (can be enhanced further)
- Responsive text sizing
- High contrast ratios

## Performance

- Minimal dependencies (vanilla JavaScript)
- Optimized CSS animations
- Lazy loading ready
- Mobile-first responsive design

## Security Notes

- Always use HTTPS in production
- Store API keys securely (use environment variables)
- Implement proper authentication
- Sanitize user inputs on the backend
- Enable CORS only for trusted domains

## Future Enhancements

- [ ] Conversation history persistence
- [ ] Export conversation to PDF
- [ ] Voice input support
- [ ] Multi-language support
- [ ] Dark mode
- [ ] Typing indicators
- [ ] Message reactions
- [ ] File attachments

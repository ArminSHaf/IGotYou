# 💬 Chat Interface Documentation

## Overview

The IGotYou frontend now includes a **conversational chat interface** where users can have natural conversations with the agent, similar to ChatGPT or the ADK web interface.

## Features

✅ **Natural Conversation** - Chat back-and-forth with the agent
✅ **Intent Understanding** - Agent asks clarifying questions to understand your needs
✅ **Message History** - See full conversation thread
✅ **Real-time Responses** - Get agent responses as you chat
✅ **White Theme** - Consistent with your existing UI design
✅ **Mobile Responsive** - Works on all devices

## How to Use

### 1. Start the Backend

```bash
cd backend
python main.py
```

The backend will run at http://localhost:8000

### 2. Start the Frontend

```bash
cd frontend
npm run dev
```

The frontend will run at http://localhost:3000

### 3. Navigate to Chat

- **Option A**: Click "Chat with Agent" button on the home page
- **Option B**: Navigate directly to http://localhost:3000/chat

### 4. Start Chatting!

Type your message and press Send. The agent will respond and may ask follow-up questions.

## Example Conversation

```
You: Find me a hidden gem in Munich

Agent: I'd love to help you find a hidden gem in Munich! To give you the perfect recommendation, I have a few questions:

1. What type of outdoor experience are you looking for?
   - Peaceful & relaxing (gardens, quiet parks)
   - Active & adventurous (hiking, climbing)
   - Cultural & scenic (historical sites with views)
   - Water-based (lakes, rivers)

2. Who will you be with?
   - Solo
   - Couple
   - Family with kids
   - Friends group

3. Do you have any timing preferences?

You: I'm going solo and want something peaceful and relaxing. I'll be there next weekend.

Agent: Perfect! Let me find some hidden peaceful spots in Munich for a solo visitor...

[Agent searches and provides recommendations]
```

## Architecture

### Frontend
- **Page**: `/frontend/app/chat/page.tsx` - Main chat UI component
- **API Route**: `/frontend/app/api/chat/route.ts` - Next.js API endpoint
- **Features**:
  - Message history state management
  - Auto-scroll to latest message
  - Loading states
  - Error handling

### Backend
- **Endpoint**: `POST /api/chat`
- **Request**:
  ```json
  {
    "message": "Find me a hidden gem in Munich",
    "history": [
      {"role": "user", "content": "previous message"},
      {"role": "assistant", "content": "previous response"}
    ]
  }
  ```
- **Response**:
  ```json
  {
    "response": "I'd love to help you find a hidden gem...",
    "timestamp": "2025-11-29T20:30:00Z"
  }
  ```

### Agent Integration
- Uses the existing `IGotYou/agent.py` root agent
- Agent maintains conversation state through `InMemoryRunner`
- Full multi-agent workflow:
  - Intent Understanding Loop → asks clarifying questions
  - Hidden Gem Finder → searches and filters
  - Recommendation Agent → generates insights
  - Weather MCP → provides real-time weather

## UI Components

### Message Display
- **User messages**: Green bubble on the right
- **Agent messages**: Gray bubble on the left
- **Timestamps**: Small text below each message
- **Loading indicator**: Shows "Agent is thinking..."

### Input Area
- Text input field with placeholder
- Send button (disabled when loading)
- Helpful tip about clarifying questions

### Header
- "Chat with IGotYou Agent" title
- Back to Home link
- Backend status banner

## Comparison: Chat vs Discovery Pages

| Feature | Chat Interface | Discovery Page |
|---------|---------------|----------------|
| **Interaction** | Conversational | Form-based |
| **Agent Flow** | Full workflow with intent clarification | Direct search |
| **Output** | Text responses | Structured gem cards |
| **Best For** | Exploratory conversations | Quick targeted searches |
| **Questions** | Agent asks follow-ups | One-time input |

## Tips for Users

1. **Be conversational** - Talk naturally, as if chatting with a travel guide
2. **Answer the questions** - The agent asks to understand your needs better
3. **Be specific** - More details = better recommendations
4. **Ask follow-ups** - Continue the conversation to refine results

## Technical Notes

### State Management
- Frontend maintains message history in React state
- Backend uses ADK `InMemoryRunner` for conversation state
- Each user has their own conversation thread (session-based)

### Performance
- Messages sent individually (not batched)
- Agent responses typically take 10-30 seconds
- Loading indicator keeps user informed

### Error Handling
- Backend connection errors shown gracefully
- Failed messages display error message in chat
- Users can retry by sending another message

## Future Enhancements

Potential improvements for the chat interface:

- [ ] Session persistence (save conversation history)
- [ ] Multiple conversations (thread management)
- [ ] Typing indicators
- [ ] Message editing/deletion
- [ ] Export conversation
- [ ] Rich media in messages (images, maps)
- [ ] Voice input
- [ ] Suggested responses/quick replies

## Troubleshooting

### "Backend server not available" error
**Solution**: Make sure the backend is running:
```bash
cd backend && python main.py
```

### Agent not responding
**Check**: Terminal output from backend for error logs

### Slow responses
**Normal**: Agent responses take 10-30 seconds due to:
- Google Places API calls
- Review analysis
- Weather data fetching
- AI processing

---

**Ready to chat?** Visit http://localhost:3000/chat and start discovering hidden gems! 🗺️✨

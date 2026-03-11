# sp.constitution.md
## Phase III – Todo AI Chatbot

**Project**  
Todo Full-Stack Web Application – Phase III

**Objective**  
Build a natural-language AI chatbot that manages todos via conversation using MCP tools.

**Development Approach**  
Agentic Dev Stack workflow only:  
spec → plan → tasks → Claude Code implementation  
No manual coding allowed.

**Technology Stack**

- Frontend: OpenAI ChatKit (embeddable chat UI)  
- Backend: FastAPI (Python)  
- AI Agent: OpenAI Agents SDK  
- MCP Tools: Official MCP SDK (Python)  
- ORM: SQLModel  
- Database: Neon Serverless PostgreSQL  
- Authentication: Better Auth + JWT  
- LLM: gpt-4o-mini / claude-3.5-sonnet (env configurable)

**Core Architecture**

- Stateless FastAPI server  
- Single endpoint: POST /api/{user_id}/chat  
- Conversation state stored in DB (Conversation + Message models)  
- AI agent uses MCP tools to perform task operations  
- Strict user isolation via JWT in every tool call

**Database Models**

- Task (reused from Phase II)  
- Conversation: user_id, id, created_at, updated_at  
- Message: user_id, conversation_id, role (user/assistant), content, created_at

**Chat Endpoint**

POST /api/{user_id}/chat

Request:
```json
{
  "conversation_id": integer?,  // optional
  "message": string
}
```
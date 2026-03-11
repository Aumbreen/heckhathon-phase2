# Implementation Plan: AI Chatbot for Todo Management

**Feature**: 001-ai-chatbot-todos
**Created**: 2026-02-09
**Status**: Draft

## Technical Context

The AI Chatbot for Todo Management will transform the existing Phase II todo app into a conversational AI experience. Users will interact with the system using natural language to create, list, update, complete, and delete tasks. The system will maintain statelessness at the server level while persisting conversation history in the database.

### Technology Stack

- **Frontend**: OpenAI ChatKit (embeddable chat UI)
- **Backend**: FastAPI (Python)
- **AI Agent**: OpenAI Agents SDK
- **MCP Tools**: Official MCP SDK (Python)
- **ORM**: SQLModel
- **Database**: Neon Serverless PostgreSQL
- **Authentication**: Better Auth + JWT
- **LLM**: gpt-4o-mini / claude-3.5-sonnet (environment configurable)

### Architecture Overview

- Stateless FastAPI server
- Single endpoint: POST /api/{user_id}/chat
- Conversation state stored in DB (Conversation + Message models)
- AI agent uses MCP tools to perform task operations
- Strict user isolation via JWT in every tool call

### Key Components

1. **Authentication Layer**: JWT-based user validation
2. **AI Agent**: Natural language processing and task interpretation
3. **MCP Tools**: Todo management operations (create, read, update, delete)
4. **Data Layer**: Conversation and message persistence
5. **API Gateway**: Chat endpoint handling

## Constitution Check

This implementation plan adheres to the principles outlined in the project constitution:

- **Agentic Development**: Following the Agentic Dev Stack workflow: spec → plan → tasks → Claude Code implementation
- **Natural Language Interface**: Providing a conversational interface for todo management
- **MCP-First Architecture**: All todo operations performed through MCP tools
- **User Isolation**: Strict user data isolation via JWT authentication
- **State Management**: Conversation state persisted in the database
- **Security-First**: Authentication required for all endpoints

## Gates & Compliance

- [x] All components use the technology stack defined in the constitution
- [x] Implementation follows the Agentic Dev Stack workflow (no manual coding)
- [x] User isolation maintained through JWT validation in every tool call
- [x] MCP tools used for all data operations
- [x] Frontend and backend logically separated
- [x] No new API endpoints beyond `/api/{user_id}/chat`

## Phase 0: Research & Resolution

### Research Areas

1. **OpenAI ChatKit Integration**: How to embed ChatKit in the frontend and configure domain allowlist
2. **MCP SDK Implementation**: How to properly implement MCP tools for todo operations
3. **JWT Validation in Tools**: How to ensure user_id validation in every tool call
4. **Conversation State Management**: How to maintain conversation context across multiple interactions
5. **FastAPI Integration with OpenAI Agent**: How to connect the AI agent with the FastAPI backend

### Expected Outcomes

- Clear understanding of ChatKit domain allowlist configuration
- Proper MCP tool implementation patterns
- Secure JWT validation approach
- Conversation persistence strategy
- Agent-backend integration approach

## Phase 1: Design & Contracts

### Data Model

Based on the feature requirements, the following entities will be implemented:

#### Task (reused from Phase II)
- id: Unique identifier
- title: Task title
- description: Task description
- completed: Boolean indicating completion status
- due_date: Optional due date
- user_id: Foreign key linking to user
- created_at: Timestamp of creation
- updated_at: Timestamp of last update

#### Conversation
- id: Unique identifier
- user_id: Foreign key linking to user
- created_at: Timestamp of creation
- updated_at: Timestamp of last update

#### Message
- id: Unique identifier
- user_id: Foreign key linking to user
- conversation_id: Foreign key linking to conversation
- role: Role of the message sender (user/assistant)
- content: Content of the message
- created_at: Timestamp of creation

### API Contract

#### Endpoint: POST /api/{user_id}/chat

##### Request Body
```json
{
  "conversation_id": "integer (optional)",
  "message": "string (required)"
}
```

##### Response
```json
{
  "conversation_id": "integer",
  "response": "string",
  "timestamp": "datetime"
}
```

##### Authentication
- JWT token required in header
- User ID in token must match the user_id in the path

## Phase 2: Implementation Strategy

### Approach
- Implement the solution in phases following the user story priorities
- Start with core functionality (natural language todo creation)
- Progress to advanced features (conversation history, updates)
- Maintain security and user isolation throughout

### MVP Scope
- Basic natural language processing for todo creation
- Simple task creation functionality
- JWT-based authentication
- Basic conversation persistence

### Incremental Delivery
- Phase 1: Natural language todo creation
- Phase 2: Todo listing functionality
- Phase 3: Todo update and deletion
- Phase 4: Conversation history and context

## Phase 3: Actual Implementation

### Backend Implementation

The backend has been implemented with the following components:

#### Models (`backend/models.py`)
- Task, Conversation, and Message models defined with proper relationships
- SQLAlchemy/SQLModel ORM mappings
- Proper indexing for performance

#### Database (`backend/database.py`)
- Database connection setup
- Session management
- Engine configuration

#### Authentication (`backend/auth.py`)
- JWT token creation and validation
- Password hashing utilities
- User verification mechanisms

#### Endpoints (`backend/endpoints.py`)
- API endpoint definitions
- Chat endpoint implementation
- Conversation management endpoints
- Request/response validation

#### MCP Tools (`tools/todo_tools.py`)
- Create, read, update, delete operations for tasks
- User isolation enforcement
- Error handling and validation

#### AI Agent (`agents/todo_agent.py`)
- OpenAI API integration
- Function calling for task operations
- Natural language processing

#### Main Application (`backend/main.py`)
- FastAPI application setup
- Router inclusion for endpoints
- Application configuration

### Frontend Implementation

#### UI (`frontend/index.html`)
- Chat interface with message display
- User input field
- Responsive design
- JavaScript for API communication

#### Endpoints (`frontend/endpoint.js`)
- API communication management
- JWT token handling
- Request/response formatting
- Error handling

### Specialized Agents

#### Frontend Agents
- `agents/frontend/ui_agent.py`: Handles UI creation and user interactions
- `agents/frontend/integration_agent.py`: Manages backend communication and JWT tokens

#### Backend Agents
- `agents/backend/api_agent.py`: Manages API endpoints and request validation
- `agents/backend/data_agent.py`: Handles database operations and data integrity

### Documentation
- `frontend/docs/frontend_docs.md`: Frontend architecture and components
- `backend/docs/backend_docs.md`: Backend architecture and components

### Configuration

#### Environment Variables (`.env`)
- Database connection settings
- JWT secret key
- OpenAI API key
- LLM model selection

## Phase 4: Testing & Validation

### Unit Tests
- Individual component testing
- API endpoint validation
- Authentication flow verification

### Integration Tests
- End-to-end conversation flow
- User isolation validation
- Data persistence verification

### User Acceptance Tests
- Natural language processing validation
- Task management functionality
- Conversation history preservation
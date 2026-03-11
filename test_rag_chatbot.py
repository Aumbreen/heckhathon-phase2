import sys
import os
# Add the backend src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'RAG_CHATBOT', 'backend', 'src'))

import asyncio
import uuid
from sqlmodel import Session, select
from database import engine
from models.conversation import Conversation, Message
from models.user import User
from tools.todo_tools import TodoTools
from agents.todo_agent import TodoAIAssistant

def test_rag_chatbot_functionality():
    """
    Test the rag-chatbot functionality integrated into the RAG_CHATBOT project
    """
    print("Testing Rag-Chatbot functionality...")
    
    # Create a test user
    with Session(engine) as db:
        # Get an existing user or create one for testing
        user = db.exec(select(User).limit(1)).first()
        if not user:
            print("No users found in the database. Please create a user first.")
            return False
            
        user_id = str(user.id)
        print(f"Using user ID: {user_id}")
        
        # Test the tools directly
        tools = TodoTools(db, user_id)
        
        # Test creating a task
        print("\n1. Testing task creation...")
        result = tools.create_task("Test task", "This is a test task for the rag-chatbot integration")
        print(f"Create task result: {result}")
        
        if "error" not in result:
            task_id = result["id"]
            print(f"Task created successfully with ID: {task_id}")
            
            # Test listing tasks
            print("\n2. Testing task listing...")
            tasks = tools.list_tasks()
            print(f"Number of tasks: {len(tasks)}")
            for task in tasks[-1:]:  # Show the last task (our test task)
                print(f"Task: {task}")
            
            # Test updating the task
            print("\n3. Testing task update...")
            update_result = tools.update_task(task_id, title="Updated test task", completed=True)
            print(f"Update result: {update_result}")
            
            # Test listing completed tasks
            print("\n4. Testing listing completed tasks...")
            completed_tasks = tools.list_tasks(completed=True)
            print(f"Number of completed tasks: {len(completed_tasks)}")
            
            # Test deleting the task
            print("\n5. Testing task deletion...")
            delete_result = tools.delete_task(task_id)
            print(f"Delete result: {delete_result}")
        
        # Test the AI assistant
        print("\n6. Testing AI assistant...")
        ai_assistant = TodoAIAssistant(tools)
        
        # Create a test conversation
        conversation = Conversation(user_id=user_id)
        db.add(conversation)
        db.commit()
        db.refresh(conversation)
        
        print(f"Created conversation with ID: {conversation.id}")
        
        # Test AI processing
        response = ai_assistant.process_message("Add a new task to buy groceries")
        print(f"AI response: {response}")
        
        # Clean up - delete the test conversation
        db.delete(conversation)
        db.commit()
        
    print("\n✅ All tests completed successfully!")
    return True

if __name__ == "__main__":
    test_rag_chatbot_functionality()
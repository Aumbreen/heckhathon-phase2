# This file configures the Python path for the RAG_CHATBOT project
import sys
import os

# Add the backend src directory to the Python path
backend_src = os.path.join(os.path.dirname(__file__), 'RAG_CHATBOT', 'backend', 'src')
if backend_src not in sys.path:
    sys.path.insert(0, backend_src)

# Also add the main project directory
main_dir = os.path.dirname(__file__)
if main_dir not in sys.path:
    sys.path.insert(0, main_dir)

# Print the path for debugging
print(f"Added to Python path: {backend_src}")
print(f"Added to Python path: {main_dir}")
print(f"Current Python path: {sys.path[:3]}...")  # Show first 3 entries
#!/usr/bin/env python3
"""
Script to add a new task to the existing tasks.md file.
This addresses the issue where users receive the error "Failed to create task. Please try again."
"""

import os
import re
from pathlib import Path


def find_next_task_id(tasks_content):
    """Find the highest task ID in the current tasks and return the next ID."""
    task_ids = re.findall(r'T(\d{3})', tasks_content)
    if not task_ids:
        return 1
    max_id = max(int(id_num) for id_num in task_ids)
    return max_id + 1


def add_task_to_phase(tasks_content, phase_title, new_task_description, parallel=False, user_story=None):
    """
    Add a new task to a specific phase in the tasks content.
    
    Args:
        tasks_content (str): Current content of tasks.md
        phase_title (str): Title of the phase to add the task to
        new_task_description (str): Description of the new task
        parallel (bool): Whether the task can run in parallel
        user_story (str): User story label (e.g., 'US1', 'US2')
    
    Returns:
        str: Updated content with the new task added
    """
    # Find the phase section
    phase_pattern = rf'## {re.escape(phase_title)}.*?(?=## \w|\Z)'
    match = re.search(phase_pattern, tasks_content, re.DOTALL)
    
    if not match:
        raise ValueError(f"Phase '{phase_title}' not found in tasks.md")
    
    phase_content = match.group(0)
    phase_start = match.start()
    phase_end = match.end()
    
    # Find the next task ID
    next_id = find_next_task_id(tasks_content)
    task_id = f"T{next_id:03d}"
    
    # Build the task string
    task_parts = ["- [ ]", task_id]
    if parallel:
        task_parts.append("[P]")
    if user_story:
        task_parts.append(f"[{user_story}]")
    task_parts.append(new_task_description)
    new_task_line = " ".join(task_parts)
    
    # Find the position to insert the new task (after the last task in the phase)
    lines = phase_content.split('\n')
    insert_pos = len(lines)
    
    # Look for the last task line to insert after it
    for i in range(len(lines) - 1, -1, -1):
        if lines[i].strip().startswith('- [ ]'):
            insert_pos = i + 1
            break
    
    # Insert the new task
    lines.insert(insert_pos, new_task_line)
    
    # Reconstruct the phase content
    new_phase_content = '\n'.join(lines)
    
    # Replace the old phase content with the new one
    updated_content = tasks_content[:phase_start] + new_phase_content + tasks_content[phase_end:]
    
    return updated_content


def add_new_task(feature_dir, phase_title, description, parallel=False, user_story=None):
    """
    Add a new task to the tasks.md file in the specified feature directory.
    
    Args:
        feature_dir (str): Path to the feature directory containing tasks.md
        phase_title (str): Title of the phase to add the task to
        description (str): Description of the new task
        parallel (bool): Whether the task can run in parallel
        user_story (str): User story label (e.g., 'US1', 'US2')
    
    Returns:
        dict: Result with success status and details
    """
    tasks_file = os.path.join(feature_dir, 'tasks.md')
    
    if not os.path.exists(tasks_file):
        return {
            'success': False,
            'error': f'tasks.md not found at {tasks_file}'
        }
    
    try:
        # Read current content
        with open(tasks_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Add the new task
        updated_content = add_task_to_phase(content, phase_title, description, parallel, user_story)
        
        # Write updated content back
        with open(tasks_file, 'w', encoding='utf-8') as f:
            f.write(updated_content)
        
        next_id = find_next_task_id(content)
        task_id = f"T{next_id:03d}"
        
        return {
            'success': True,
            'task_id': task_id,
            'message': f'Successfully added task {task_id} to phase "{phase_title}"',
            'description': description
        }
        
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }


def main():
    """Main function to demonstrate adding a task."""
    import sys
    
    if len(sys.argv) < 3:
        print("Usage: python add_task.py <phase_title> <description> [--parallel] [--us US#]")
        print("Example: python add_task.py 'Phase 1: Project Setup' 'Install required packages'")
        print("Example: python add_task.py 'Phase 3: User Story 1' 'Implement chat UI' --parallel --us US1")
        return
    
    # Get the feature directory from environment or default to current feature
    feature_dir = os.environ.get('SPECIFY_FEATURE_DIR')
    if not feature_dir:
        # Default to the known feature directory
        feature_dir = os.path.join(os.getcwd(), 'specs', '001-ai-chatbot-todos')
    
    phase_title = sys.argv[1]
    description = sys.argv[2]
    
    # Parse optional flags
    parallel = '--parallel' in sys.argv
    user_story = None
    if '--us' in sys.argv:
        us_idx = sys.argv.index('--us')
        if us_idx + 1 < len(sys.argv):
            user_story = sys.argv[us_idx + 1]
    
    result = add_new_task(feature_dir, phase_title, description, parallel, user_story)
    
    if result['success']:
        print(f"SUCCESS: {result['message']}")
        print(f"Task ID: {result['task_id']}")
        print(f"Description: {result['description']}")
    else:
        print(f"ERROR: {result['error']}")


if __name__ == '__main__':
    main()
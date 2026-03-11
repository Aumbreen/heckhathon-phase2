# Claude Skills Package

Reusable components and utilities for Claude agents in the Spec-Driven Development (SDD) workflow.

## Overview

The `skills/claude/` directory contains Python modules that provide core functionality for:

- **PHR Management**: Creating and managing Prompt History Records
- **File Operations**: Utility functions for file handling
- **Configuration**: Loading and managing project configuration
- **Command Execution**: Managing .specify workflow commands
- **Agent Management**: Loading and orchestrating agents

## Modules

### `phr_manager.py` - Prompt History Record Manager

Handles creation, routing, and validation of PHR files for knowledge capture and traceability.

```python
from skills.claude import PHRManager

phr_manager = PHRManager(repo_root="/path/to/repo")

# Create a PHR
phr_path = phr_manager.create_phr(
    title="User implements feature X",
    stage="implementation",
    prompt_text="User's input...",
    response_text="Assistant's output...",
    feature="feature-name",
    model="claude-sonnet-4-5-20250929",
    files_created=["src/new_file.py"],
    labels=["feature", "implementation"]
)

# List PHRs
phrs = phr_manager.list_phrs(stage="implementation")
```

**Key Methods:**
- `create_phr()`: Create a new PHR
- `list_phrs()`: List PHRs with optional filtering
- `determine_route()`: Calculate the correct directory for a PHR
- `generate_slug()`: Convert title to filename slug

### `file_utils.py` - File Utilities

Provides helper functions for file operations and project structure management.

```python
from skills.claude import FileUtils

# Read file
content = FileUtils.read_file("path/to/file.py")

# Write file
FileUtils.write_file("path/to/output.py", content)

# Find files
py_files = FileUtils.find_files("src/", "*.py")

# JSON operations
data = FileUtils.load_json("config.json")
FileUtils.save_json("output.json", data)

# Directory operations
FileUtils.ensure_directory("build/")
contents = FileUtils.list_directory("src/")
```

**Key Methods:**
- `read_file()`: Read file contents
- `write_file()`: Write to file
- `load_json()`, `save_json()`: JSON operations
- `find_files()`: Find files by glob pattern
- `ensure_directory()`: Create directory if needed

### `config_loader.py` - Configuration Loader

Loads and manages configuration for Claude agents.

```python
from skills.claude import ConfigLoader

config = ConfigLoader(repo_root="/path/to/repo")

# Get configuration values
log_level = config.get_config("LOG_LEVEL")

# Get provider info
gemini = config.get_provider("gemini")

# Get router configuration
default_router = config.get_router_config("default")

# Get agent definition
arch_agent = config.get_agent("architecture-agent")

# List projects paths
paths = config.get_project_paths()
```

**Key Methods:**
- `get_config()`: Get configuration value
- `get_provider()`: Get provider configuration
- `get_router_config()`: Get router configuration
- `get_agent()`: Get agent definition
- `list_agents()`: List available agents
- `get_project_paths()`: Get common project paths

### `command_executor.py` - Command Executor

Handles execution and management of SDD workflow commands.

```python
from skills.claude.command_executor import CommandExecutor

executor = CommandExecutor(repo_root="/path/to/repo")

# List available commands
commands = executor.list_commands()

# Get command help
help_text = executor.get_command_help("sp.phr")

# Load command content
command = executor.load_command("sp.phr")

# Extract command metadata
metadata = executor.extract_command_metadata("sp.specify")
```

**Available Commands:**
- `sp.phr`: Record AI exchange as a PHR
- `sp.specify`: Create feature specification
- `sp.plan`: Create implementation plan
- `sp.tasks`: Break down work into tasks
- `sp.implement`: Execute implementation
- `sp.adr`: Create Architectural Decision Record
- `sp.checklist`: Create verification checklist
- And more...

### `agent_manager.py` - Agent Manager

Manages agent loading and orchestration.

```python
from skills.claude.agent_manager import AgentManager

agent_mgr = AgentManager(repo_root="/path/to/repo")

# Get agent
agent = agent_mgr.get_agent("architecture-agent")

# List agents
all_agents = agent_mgr.list_agents()

# Get agents by type
backend_agents = agent_mgr.get_agents_by_type("backend")

# Get description
desc = agent_mgr.get_agent_description("database-engineer")
```

## Usage in SDD Workflow

### Creating a PHR After Work

```python
from skills.claude import PHRManager

phr_mgr = PHRManager(repo_root="/project/root")

phr_mgr.create_phr(
    title="Implement user authentication",
    stage="implementation",
    prompt_text="User's original request...",
    response_text="Work completed summary...",
    feature="auth",
    model="claude-sonnet-4-5-20250929",
    files_created=[
        "src/auth/models.py",
        "src/auth/routes.py"
    ],
    branch="feature/user-auth",
    user="developer@example.com",
    command="implement",
    labels=["auth", "backend"]
)
```

### Loading Configuration for Agent

```python
from skills.claude import ConfigLoader

config = ConfigLoader()
paths = config.get_project_paths()
agent = config.get_agent("fastapi-backend-dev")
router = config.get_router_config("default")
```

## Installation

The Claude skills are already integrated into the project structure. To use them in your Python code:

```python
from skills.claude import PHRManager, FileUtils, ConfigLoader
```

## Routing Rules

PHRs are automatically routed based on stage and feature context:

- **Constitution** → `history/prompts/constitution/`
- **General** → `history/prompts/general/`
- **Feature-specific** (spec, plan, tasks, implementation, etc.) → `history/prompts/<feature-name>/`

## Naming Convention

PHR filenames follow this pattern:
```
{ID}-{slug}.{stage}.prompt.md
```

Examples:
- `001-user-authentication.implementation.prompt.md`
- `002-add-websocket-support.plan.prompt.md`
- `001-project-principles.constitution.prompt.md`

## Development

To extend Claude skills with new utilities:

1. Create a new module in `skills/claude/`
2. Add imports to `__init__.py`
3. Follow existing module patterns

## Testing

Skills can be tested with:

```bash
python -m pytest skills/claude/tests/
```

## Contributing

When adding new skills or utilities:

1. Include comprehensive docstrings
2. Add type hints
3. Create unit tests
4. Update this README with examples

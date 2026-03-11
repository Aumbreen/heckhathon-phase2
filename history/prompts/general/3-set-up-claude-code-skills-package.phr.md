---
id: 3
title: Set up Claude code skills package
stage: general
date: 2026-02-07
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: master
user: unknown
command: setup
labels: ["setup", "claude-code", "infrastructure"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
- skills/claude/__init__.py
- skills/claude/phr_manager.py
- skills/claude/file_utils.py
- skills/claude/config_loader.py
- skills/claude/command_executor.py
- skills/claude/agent_manager.py
- skills/claude/README.md
tests:
- No tests run or added
---

## Prompt

meine kaam shuru kerna har abhi tak claude code setup nahi hua

(Translation: "I want to start work. Claude code setup hasn't been done yet.")

## Response

Initialized the Claude code skills package with reusable components for the Spec-Driven Development (SDD) workflow.

## Created Skills Package

The `skills/claude/` directory now contains:

### Core Modules

1. **PHRManager** - Creates and manages Prompt History Records (PHRs)
   - Routing based on stage and feature
   - ID generation and slug creation
   - YAML frontmatter management

2. **FileUtils** - File operation utilities
   - Read/write files and JSON
   - Directory management
   - File discovery and manipulation

3. **ConfigLoader** - Configuration management
   - Loads config from `.claude/config.json`
   - Agent definition loading
   - Router and provider configuration access

4. **CommandExecutor** - SDD workflow command management
   - Lists available commands (sp.phr, sp.specify, sp.plan, etc.)
   - Loads command content and metadata
   - Executes .specify workflow

5. **AgentManager** - Agent loading and orchestration
   - Loads agents from `.claude/agents/`
   - Filters agents by type
   - Retrieves agent descriptions

### Usage

```python
from skills.claude import PHRManager, FileUtils, ConfigLoader

# Create a PR
phr_mgr = PHRManager(repo_root=".")
phr_mgr.create_phr(
    title="Feature implementation complete",
    stage="implementation",
    prompt_text="...",
    response_text="..."
)
```

## What's Ready

✅ Claude code environment configured  
✅ Skills package with reusable modules  
✅ PHR management system  
✅ Configuration and agent loading  
✅ File utilities and command execution  
✅ Comprehensive documentation  

## Next Steps

You can now:
1. Start working on features using Claude and agents
2. Use `sp.phr` command to record work as PHRs
3. Use agent managers to orchestrate multi-agent workflows
4. Reference the README in `skills/claude/README.md` for detailed API documentation


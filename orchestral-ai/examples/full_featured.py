"""
Full-Featured Orchestral Example
=================================

Production-ready configuration with tools, hooks, and custom settings.
This example shows best practices for deploying Orchestral in production.

Run with:
    python examples/full_featured.py

Features demonstrated:
- Custom workspace directory
- Comprehensive tool set
- Multi-layered security with hooks
- Custom LLM and system prompt
"""

import os
from orchestral import Agent
from orchestral.tools import (
    RunCommandTool, RunPythonTool, WebSearchTool,
    WriteFileTool, ReadFileTool, EditFileTool,
    FileSearchTool, FindFilesTool, TodoWrite, TodoRead,
    DisplayImageTool
)
from orchestral.tools.hooks import (
    TruncateLinesHook, DangerousCommandHook,
    SafeguardHook, UserApprovalHook
)
from orchestral.llm import Claude
from orchestral.prompts import BASIC_APP_PROMPT
import app.server as app_server

# Set up workspace
base_directory = "workspace"
os.makedirs(base_directory, exist_ok=True)

# Configure tools
tools = [
    RunCommandTool(base_directory=base_directory),
    RunPythonTool(base_directory=base_directory),
    WriteFileTool(base_directory=base_directory),
    ReadFileTool(base_directory=base_directory, show_line_numbers=True),
    EditFileTool(base_directory=base_directory),
    FindFilesTool(base_directory=base_directory),
    FileSearchTool(base_directory=base_directory),
    WebSearchTool(),
    TodoRead(),
    TodoWrite(),
    DisplayImageTool,
]

# Add safety hooks
hooks = [
    UserApprovalHook(),     # Require approval for sensitive operations
    DangerousCommandHook(), # Block dangerous patterns
    TruncateLinesHook(),    # Limit output size
]

# Create agent
llm = Claude()
agent = Agent(
    llm=llm,
    tools=tools,
    tool_hooks=hooks,
    system_prompt=BASIC_APP_PROMPT
)

# Launch web interface
app_server.run_server(agent, host="127.0.0.1", port=8000, open_browser=True)

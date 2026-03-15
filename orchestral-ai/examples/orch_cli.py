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
from dotenv import load_dotenv
load_dotenv()
import os
import asyncio
import inspect
from typing import Any

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

# Set up workspace
base_directory = "workspace"
os.makedirs(base_directory, exist_ok=True)

def maybe_make_tool(tool_cls_or_obj, **kwargs):
    """
    Some libraries expose tools as classes that need instantiation,
    others may expose ready-made objects. This helper handles both.
    """
    try:
        if inspect.isclass(tool_cls_or_obj):
            return tool_cls_or_obj(**kwargs)
        return tool_cls_or_obj
    except TypeError:
        # Fallback if the tool does not accept kwargs or is already an instance
        return tool_cls_or_obj

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
    maybe_make_tool(DisplayImageTool),
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

# ----------------------------
# Helpers
# ----------------------------
def extract_text(result: Any) -> str:
    """
    Best-effort extraction of text from different possible result shapes.
    """
    if result is None:
        return ""

    if isinstance(result, str):
        return result

    for attr in ("content", "text", "output", "message", "response"):
        if hasattr(result, attr):
            value = getattr(result, attr)
            if isinstance(value, str):
                return value
            if isinstance(value, list):
                return "\n".join(str(x) for x in value)

    if isinstance(result, dict):
        for key in ("content", "text", "output", "message", "response"):
            if key in result:
                return str(result[key])

    return str(result)

async def call_agent_async(user_message: str) -> str:
    """
    Tries several common programmatic APIs because the public quickstart
    examples do not show the non-server method explicitly.
    """
    candidate_calls = [
        ("run", lambda fn: fn(user_message)),
        ("invoke", lambda fn: fn(user_message)),
        ("chat", lambda fn: fn(user_message)),
        ("respond", lambda fn: fn(user_message)),
        ("ask", lambda fn: fn(user_message)),

        ("run", lambda fn: fn(prompt=user_message)),
        ("invoke", lambda fn: fn(prompt=user_message)),
        ("chat", lambda fn: fn(prompt=user_message)),
        ("respond", lambda fn: fn(prompt=user_message)),

        ("run", lambda fn: fn(input=user_message)),
        ("invoke", lambda fn: fn(input=user_message)),

        (
            "run",
            lambda fn: fn(messages=[{"role": "user", "content": user_message}]),
        ),
        (
            "invoke",
            lambda fn: fn(messages=[{"role": "user", "content": user_message}]),
        ),
        (
            "chat",
            lambda fn: fn(messages=[{"role": "user", "content": user_message}]),
        ),
    ]
    errors = []

    for method_name, builder in candidate_calls:
        if not hasattr(agent, method_name):
            continue

        fn = getattr(agent, method_name)

        try:
            result = builder(fn)

            if inspect.isawaitable(result):
                result = await result

            text = extract_text(result).strip()
            if text:
                return text

            return str(result)

        except Exception as e:
            errors.append(f"{method_name}: {type(e).__name__}: {e}")

    available = [m for m in dir(agent) if not m.startswith("_")]
    raise RuntimeError(
        "Could not find a working programmatic call on Agent.\n"
        f"Tried common methods and failed.\n\n"
        f"Available public attributes/methods:\n{available}\n\n"
        f"Errors:\n" + "\n".join(errors)
    )

def main():
    print("Orchestral CLI")
    print("Type 'exit' or 'quit' to stop.")
    print(f"Workspace: {base_directory}\n")

    while True:
        try:
            user_message = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye.")
            break

        if not user_message:
            continue

        if user_message.lower() in {"exit", "quit"}:
            print("Goodbye.")
            break

        try:
            reply = asyncio.run(call_agent_async(user_message))
            print(f"\nAgent: {reply}\n")
        except Exception as e:
            print(f"\n[ERROR] {type(e).__name__}: {e}\n")


if __name__ == "__main__":
    main()



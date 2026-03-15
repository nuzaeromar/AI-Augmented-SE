<div align="center">
  <img src="https://orchestral-ai.com/logo.png" alt="Orchestral AI" width="120">
  <h1>Orchestral AI</h1>
  <p><strong>Quickstart Guide & Examples</strong></p>
  <p>Production-ready AI framework for building LLM-powered applications</p>
</div>

---

## 🚀 Quick Start

This repository contains examples and quickstart guides for Orchestral AI. The framework itself is installed via pip.

### Installation

```bash
pip install orchestral-ai
```

### Setup API Keys

Create a `.env` file in your project directory:

```env
ANTHROPIC_API_KEY=sk-ant-...     # Get from https://console.anthropic.com/
OPENAI_API_KEY=sk-proj-...       # Get from https://platform.openai.com/api-keys
GOOGLE_API_KEY=AIza...           # Get from https://aistudio.google.com/app/apikey
GROQ_API_KEY=gsk_...             # Get from https://console.groq.com/
```

At least one API key is required. We recommend starting with Anthropic's Claude.

---

## 💡 Minimal Example

The absolute minimum to get started:

```python
from orchestral import Agent
import app.server as app_server

agent = Agent()
app_server.run_server(agent)
```

That's it! This creates an agent with default settings and launches a web interface at `http://127.0.0.1:8000`.

**See:** [`examples/minimal.py`](examples/minimal.py)

---

## 🛠️ Full-Featured Example

For production use, you'll want to configure tools, hooks, and LLM settings:

```python
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
    UserApprovalHook(),      # Require approval for sensitive operations
    DangerousCommandHook(),  # Block dangerous patterns
    TruncateLinesHook(),     # Limit output size
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
```

**See:** [`examples/full_featured.py`](examples/full_featured.py)

⚠️ **Security Note:** By default, agents can execute code on your computer. Only use in trusted environments or enable approval hooks.

---

## 📚 Examples

Browse the [`examples/`](examples/) directory for runnable code:

### Web Interface Examples
- **[`minimal.py`](examples/minimal.py)** - Absolute minimum (5 lines!)
- **[`full_featured.py`](examples/full_featured.py)** - Production setup with tools, hooks, and prompts
- **[`multi_provider.py`](examples/multi_provider.py)** - Switch between Claude, GPT, Gemini, etc.
- **[`custom_tool_example.py`](examples/custom_tool_example.py)** - Build domain-specific tools

### Programmatic Usage Examples
- **[`programmatic_usage.py`](examples/programmatic_usage.py)** - Call agents from code (scripts, notebooks)
- **[`streaming_responses.py`](examples/streaming_responses.py)** - Stream responses for real-time feedback
- **[`multi_turn_conversation.py`](examples/multi_turn_conversation.py)** - Agent-to-agent conversations

Each example is fully runnable after `pip install orchestral-ai`.

---

## 🔧 Key Concepts

### Agents

An `Agent` orchestrates conversations between users, LLMs, and tools:

```python
from orchestral import Agent
from orchestral.llm import Claude, GPT, Gemini

# Switch providers by changing one line
agent = Agent(llm=Claude(model='claude-sonnet-4-0'))
# agent = Agent(llm=GPT(model='gpt-4'))
# agent = Agent(llm=Gemini(model='gemini-2.0-flash-exp'))
```

### Tools

Tools enable LLMs to interact with external systems. Use built-in tools or create your own:

```python
from orchestral import define_tool

@define_tool()
def calculate_energy(mass: float, c: float = 299792458.0):
    """Calculate relativistic energy E=mc²

    Args:
        mass: Mass in kilograms
        c: Speed of light in m/s (default: exact value)
    Returns:
        Energy in joules
    """
    return mass * c ** 2
```

### Hooks

Hooks intercept tool execution for safety, logging, or modification:

```python
from orchestral.tools.hooks import UserApprovalHook, DangerousCommandHook

hooks = [
    UserApprovalHook(),      # Ask user before dangerous operations
    DangerousCommandHook(),  # Block rm -rf, eval(), etc.
]

agent = Agent(llm=llm, tools=tools, tool_hooks=hooks)
```

### Context Management

Save and load conversations across sessions:

```python
# Save conversation
agent.context.save_json("conversation.json")

# Load and continue with different provider
from orchestral.context import Context
context = Context.load_json("conversation.json")
agent = Agent(llm=GPT(model='gpt-4'), tools=tools, context=context)
```

---

## ✨ Features

### Multi-Provider Support
- **Anthropic** (Claude Sonnet, Haiku, Opus)
- **OpenAI** (GPT-4, GPT-4o, GPT-3.5)
- **Google** (Gemini Pro, Flash)
- **Groq** (Llama, Mixtral)
- **Mistral AI**
- **AWS Bedrock**
- **Ollama** (local models)

### Built-in Tools
- **Filesystem**: Read, write, edit, search files
- **Execution**: Run shell commands, Python code
- **Web**: Search the web, fetch arXiv papers
- **Utilities**: Todo lists, image display

### Safety & Security
- Multi-layered approval system
- Pattern-based dangerous command blocking
- Read-before-edit file safety
- Sandboxed workspace operations

### Developer Experience
- Type-safe tool definition from Python type hints
- Streaming support for real-time responses
- Automatic cost tracking across providers
- Conversation persistence and undo
- LaTeX export for research papers

---

## 📖 Documentation

- **Full Documentation**: [orchestral-ai.com/docs](https://orchestral-ai.com/docs)
- **API Reference**: [orchestral-ai.com/docs/api](https://orchestral-ai.com/docs/api)
- **Tutorials**: [orchestral-ai.com/docs/tutorials](https://orchestral-ai.com/docs/tutorials)

---

## 🛠 Requirements

- **Python 3.13** or higher
- At least one LLM provider API key (or use Ollama locally for free)
- Operating System: macOS, Linux, or Windows

> **Note:** Python 3.12 is not currently supported due to compatibility issues. Please use Python 3.13+.

---

## 🤝 Support

- **Documentation**: [orchestral-ai.com/docs](https://orchestral-ai.com/docs)
- **Issues**: Report issues at [orchestral-ai.com/support](https://orchestral-ai.com/support)
- **Email**: [alex@orchestral-ai.com](mailto:alex@orchestral-ai.com)

---

## 📝 License

**Proprietary - All Rights Reserved**

Copyright © 2024 Orchestral AI. All rights reserved.

This software is proprietary and confidential. Unauthorized copying, distribution, modification, or use of this software, in whole or in part, is strictly prohibited without prior written permission from Orchestral AI.

For licensing inquiries, contact: [alex@orchestral-ai.com](mailto:alex@orchestral-ai.com)

---

<div align="center">
  <p>Built with ❤️ by the Orchestral AI team</p>
</div>

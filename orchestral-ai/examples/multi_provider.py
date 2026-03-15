"""
Multi-Provider Example
======================

Demonstrates switching between different LLM providers.
Shows how easy it is to change providers in Orchestral.

Run with:
    python examples/multi_provider.py

Make sure you have the corresponding API keys in your .env file.
"""

from orchestral import Agent
from orchestral.llm import Claude, GPT, Gemini, Ollama, Groq
from orchestral.tools import WebSearchTool
import app.server as app_server

# Choose your provider by uncommenting one line:

# Anthropic Claude (recommended)
# llm = Claude(model='claude-sonnet-4-0')

# OpenAI GPT
llm = GPT(model='gpt-4o')

# Google Gemini
# llm = Gemini(model='gemini-2.0-flash-exp')

# Groq (fast inference)
# llm = Groq(model='llama-3.1-70b-versatile')

# Ollama (local models - free!)
# llm = Ollama(model='llama3.1:70b')

# Create agent with your chosen provider
agent = Agent(
    llm=llm,
    tools=[WebSearchTool()],  # Add tools as needed
)

print(f"Running with {llm.__class__.__name__}: {llm.model}")
app_server.run_server(agent, host="127.0.0.1", port=8000, open_browser=True)

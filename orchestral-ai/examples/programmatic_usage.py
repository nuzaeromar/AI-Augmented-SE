"""
Programmatic Usage Example
===========================

Demonstrates calling agents programmatically without the web UI.
Useful for automation, notebooks, scripts, and research workflows.

Run with:
    python examples/programmatic_usage.py
"""

from orchestral import Agent
from orchestral.llm import Claude

# Create a simple agent
agent = Agent(
    llm=Claude(model='claude-sonnet-4-0'),
    system_prompt="You are a helpful assistant specializing in Python programming."
)

# Call the agent programmatically
print("Asking agent to explain list comprehensions...\n")
response = agent.run("Explain Python list comprehensions in 2-3 sentences.")

print(response.text)
print(f"\nCost: ${response.usage.cost:.4f}")
print(f"Tokens: {response.usage.input_tokens} in, {response.usage.output_tokens} out")

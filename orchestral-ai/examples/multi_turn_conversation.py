"""
Multi-Turn Conversation Example
================================

Demonstrates programmatic multi-turn conversations between agents.
This example recreates a philosophical debate between two agents.

Run with:
    python examples/multi_turn_conversation.py
"""


from dotenv import load_dotenv
load_dotenv()

from orchestral import Agent
from orchestral.llm import Ollama


# Create two agents with different personas
philosopher_A = "Quine"
philosopher_B = "Carnap"

agent_A = Agent(
    system_prompt=f"""You are the philosopher {philosopher_A}.
    Respond in the style of {philosopher_A}. Keep answers concise.
    You are having a debate with {philosopher_B}.""",
    llm=GPT(model="gpt-4o")
)

agent_B = Agent(
    system_prompt=f"""You are the philosopher {philosopher_B}.
    Respond in the style of {philosopher_B}. Keep answers concise.
    You are having a debate with {philosopher_A}.""",
    llm=GPT(model="gpt-4o")
)

# Start the debate
print(f"=== Philosophical Debate: {philosopher_A} vs {philosopher_B} ===\n")

response = agent_A.run(
    f"Hello Mr. {philosopher_A}, it's me, {philosopher_B}. "
    "What are your thoughts on the analytic-synthetic distinction?"
)
print(f"{philosopher_A}: {response.text}\n")

# Continue for 3 rounds
for round_num in range(3):
    print(f"--- Round {round_num + 1} ---\n")

    # B responds to A
    response = agent_B.run(response.text)
    print(f"{philosopher_B}: {response.text}\n")

    # A responds to B
    response = agent_A.run(response.text)
    print(f"{philosopher_A}: {response.text}\n")

# Show total cost
total_cost = agent_A.get_total_cost() + agent_B.get_total_cost()
print(f"Total cost: ${total_cost:.4f}")

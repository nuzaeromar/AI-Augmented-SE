"""
Custom Tool Example
===================

Shows how to create domain-specific tools for your agents.
This example creates a physics calculator tool.

Run with:
    python examples/custom_tool_example.py
"""

from orchestral import Agent, define_tool
from orchestral.llm import Claude
import app.server as app_server


@define_tool()
def calculate_energy(mass: float, c: float = 299792458.0):
    """Calculate relativistic energy using E=mc²

    Args:
        mass: Mass in kilograms
        c: Speed of light in m/s (default: exact value)

    Returns:
        Energy in joules
    """
    energy = mass * c ** 2
    return f"E = mc² = ({mass} kg) × ({c} m/s)² = {energy:.3e} joules"


@define_tool()
def convert_temperature(value: float, from_unit: str, to_unit: str):
    """Convert between temperature scales

    Args:
        value: Temperature value to convert
        from_unit: Input unit ('C', 'F', or 'K')
        to_unit: Output unit ('C', 'F', or 'K')

    Returns:
        Converted temperature with units
    """
    # Convert to Celsius first
    if from_unit == 'F':
        celsius = (value - 32) * 5/9
    elif from_unit == 'K':
        celsius = value - 273.15
    else:
        celsius = value

    # Convert to target unit
    if to_unit == 'F':
        result = celsius * 9/5 + 32
    elif to_unit == 'K':
        result = celsius + 273.15
    else:
        result = celsius

    return f"{value}°{from_unit} = {result:.2f}°{to_unit}"


# Create agent with custom tools
agent = Agent(
    llm=Claude(),
    tools=[calculate_energy, convert_temperature],
    system_prompt="You are a helpful physics assistant with specialized calculation tools."
)

print("Agent ready with custom physics tools!")
print("\nTry asking:")
print("  - 'What is the energy of 1kg of matter?'")
print("  - 'Convert 100°F to Celsius'")
print()

# Launch web interface
app_server.run_server(agent, host="127.0.0.1", port=8000, open_browser=True)

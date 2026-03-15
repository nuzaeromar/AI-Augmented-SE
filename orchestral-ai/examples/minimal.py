"""
Minimal Orchestral Example
==========================

This is the absolute minimum code needed to run Orchestral.
Creates an agent with default settings and launches a web interface.

Run with:
    python examples/minimal.py

Then open http://127.0.0.1:8000 in your browser.
"""
from dotenv import load_dotenv
load_dotenv()

from orchestral import Agent
from orchestral.llm import Ollama
from orchestral.ui.app import server as app_server

agent = Agent(llm=Ollama(model="gpt-oss:120b-cloud"))
app_server.run_server(agent)
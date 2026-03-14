"""
config.py
All configuration for the GitHub Agent.
Edit values here or set as environment variables.
"""
import os


class Config:
    # ── Ollama ────────────────────────────────────────────────────────────────
    OLLAMA_BASE_URL: str = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    OLLAMA_MODEL:    str = os.getenv("OLLAMA_MODEL",    "llama3.2:3b")

    # ── GitHub ────────────────────────────────────────────────────────────────
    # Personal Access Token with repo scope
    # Create at: https://github.com/settings/tokens
    GITHUB_TOKEN:  str = os.getenv("GITHUB_TOKEN", "")
    GITHUB_OWNER:  str = os.getenv("GITHUB_OWNER", "nuzaeromar")   # e.g. "nuzaer"
    GITHUB_REPO:   str = os.getenv("GITHUB_REPO",  "AI-Augmented-SE")   # e.g. "my-project"

    # ── Git ───────────────────────────────────────────────────────────────────
    # Absolute path to the local repo you want to review
    REPO_PATH: str = os.getenv("REPO_PATH", "/Users/nuzaer/Downloads/SP-26/CS-5001-AI-Augmented-SE")

    # ── Agent behaviour ───────────────────────────────────────────────────────
    DRY_RUN:        bool = True    # True = show drafts, never call GitHub API
    AUTO_APPROVE:   bool = False   # True = skip human approval gate
    MAX_DIFF_CHARS: int  = 8000    # truncate large diffs before sending to LLM

    # ── Web dashboard ─────────────────────────────────────────────────────────
    DASHBOARD_HOST:  str  = "127.0.0.1"
    DASHBOARD_PORT:  int  = 8002
    DASHBOARD_DEBUG: bool = False

    # ── Persistence ───────────────────────────────────────────────────────────
    STATE_FILE:  str = ".agent_state.json"
    LOG_FILE:    str = "agent.log"
    LOG_LEVEL:   str = "INFO"

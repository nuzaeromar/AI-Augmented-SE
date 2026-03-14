"""
agents/base.py
Base agent — shared Ollama HTTP call + JSON extraction.
All agents inherit from this.
"""
import json
import re
import requests
from typing import List, Optional
from config import Config


class BaseAgent:
    """Shared Ollama client used by all 4 agents."""

    def __init__(self, cfg: Config, name: str):
        self.cfg  = cfg
        self.name = name

    def chat(
        self,
        messages: List[dict],
        temperature: float = 0.3,
        max_tokens:  int   = 2048,
    ) -> str:
        """Send messages to Ollama and return raw text response."""
        payload = {
            "model":   self.cfg.OLLAMA_MODEL,
            "messages": messages,
            "stream":  False,
            "options": {
                "temperature": temperature,
                "num_predict": max_tokens,
            },
        }
        try:
            resp = requests.post(
                f"{self.cfg.OLLAMA_BASE_URL}/api/chat",
                json=payload,
                timeout=180,
            )
            resp.raise_for_status()
            return resp.json()["message"]["content"].strip()
        except requests.exceptions.ConnectionError:
            raise RuntimeError(
                "Cannot reach Ollama. Start it with: ollama serve"
            )
        except requests.exceptions.Timeout:
            raise RuntimeError("Ollama request timed out (180s).")
        except Exception as e:
            raise RuntimeError(f"Ollama error: {e}")

    def parse_json(self, text: str) -> dict:
        """
        Extract JSON from LLM output — three fallback strategies.
        Strategy 1: fenced code block ```json ... ```
        Strategy 2: entire text is valid JSON
        Strategy 3: largest { ... } substring
        """
        # Strategy 1
        m = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", text, re.DOTALL)
        if m:
            try:
                return json.loads(m.group(1))
            except json.JSONDecodeError:
                pass

        # Strategy 2
        try:
            return json.loads(text.strip())
        except json.JSONDecodeError:
            pass

        # Strategy 3 — largest {...} block
        best, depth, start = "", 0, -1
        for i, ch in enumerate(text):
            if ch == "{":
                if depth == 0:
                    start = i
                depth += 1
            elif ch == "}" and depth > 0:
                depth -= 1
                if depth == 0:
                    candidate = text[start: i + 1]
                    if len(candidate) > len(best):
                        best = candidate
        if best:
            try:
                return json.loads(best)
            except json.JSONDecodeError:
                pass

        return {}

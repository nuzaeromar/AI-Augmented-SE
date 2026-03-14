"""
tools/github_tools.py
GitHub REST API client — called by Python, NOT by the LLM.
All writes are gated behind DRY_RUN and human approval.
"""
import requests
from typing import Optional, List, Dict, Any
from config import Config


GITHUB_API = "https://api.github.com"


class GitHubClient:
    """Thin wrapper around GitHub REST API."""

    def __init__(self, cfg: Config):
        self.cfg     = cfg
        self.owner   = cfg.GITHUB_OWNER
        self.repo    = cfg.GITHUB_REPO
        self.headers = {
            "Authorization": f"Bearer {cfg.GITHUB_TOKEN}",
            "Accept":        "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
        }

    def _url(self, path: str) -> str:
        return f"{GITHUB_API}/repos/{self.owner}/{self.repo}{path}"

    def _get(self, path: str, params: Optional[dict] = None) -> Any:
        resp = requests.get(self._url(path), headers=self.headers,
                            params=params, timeout=15)
        resp.raise_for_status()
        return resp.json()

    def _post(self, path: str, data: dict) -> Any:
        resp = requests.post(self._url(path), headers=self.headers,
                             json=data, timeout=15)
        resp.raise_for_status()
        return resp.json()

    def _patch(self, path: str, data: dict) -> Any:
        resp = requests.patch(self._url(path), headers=self.headers,
                              json=data, timeout=15)
        resp.raise_for_status()
        return resp.json()

    # ── Read ──────────────────────────────────────────────────────────────────

    def get_issue(self, number: int) -> dict:
        """Fetch a single issue by number."""
        return self._get(f"/issues/{number}")

    def get_pr(self, number: int) -> dict:
        """Fetch a single pull request by number."""
        return self._get(f"/pulls/{number}")

    def list_issues(self, state: str = "open", limit: int = 10) -> List[dict]:
        data = self._get("/issues", params={"state": state, "per_page": limit})
        return data if isinstance(data, list) else []

    def list_prs(self, state: str = "open", limit: int = 10) -> List[dict]:
        data = self._get("/pulls", params={"state": state, "per_page": limit})
        return data if isinstance(data, list) else []

    def get_repo_info(self) -> dict:
        resp = requests.get(
            f"{GITHUB_API}/repos/{self.owner}/{self.repo}",
            headers=self.headers, timeout=10,
        )
        resp.raise_for_status()
        return resp.json()

    # ── Write (gated by DRY_RUN) ──────────────────────────────────────────────

    def create_issue(self, title: str, body: str,
                     labels: Optional[List[str]] = None) -> dict:
        if self.cfg.DRY_RUN:
            return {"html_url": "[DRY RUN — no issue created]", "number": 0}
        payload: Dict[str, Any] = {"title": title, "body": body}
        if labels:
            payload["labels"] = labels
        return self._post("/issues", payload)

    def create_pr(self, title: str, body: str,
                  head: str, base: str = "main",
                  labels: Optional[List[str]] = None) -> dict:
        if self.cfg.DRY_RUN:
            return {"html_url": "[DRY RUN — no PR created]", "number": 0}
        payload: Dict[str, Any] = {
            "title": title,
            "body":  body,
            "head":  head,
            "base":  base,
        }
        result = self._post("/pulls", payload)
        if labels and result.get("number"):
            self._post(f"/issues/{result['number']}/labels", {"labels": labels})
        return result

    def update_issue(self, number: int, title: str, body: str) -> dict:
        if self.cfg.DRY_RUN:
            return {"html_url": "[DRY RUN — no update made]", "number": number}
        return self._patch(f"/issues/{number}", {"title": title, "body": body})

    def update_pr(self, number: int, title: str, body: str) -> dict:
        if self.cfg.DRY_RUN:
            return {"html_url": "[DRY RUN — no update made]", "number": number}
        return self._patch(f"/pulls/{number}", {"title": title, "body": body})

    # ── Validation ────────────────────────────────────────────────────────────

    def is_configured(self) -> bool:
        return bool(self.cfg.GITHUB_TOKEN and self.owner and self.repo)

    def check_connection(self) -> bool:
        try:
            self.get_repo_info()
            return True
        except Exception:
            return False

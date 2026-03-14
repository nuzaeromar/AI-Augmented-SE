"""
tools/git_tools.py
Git command wrappers — called by Python, NOT by the LLM.
Context-gather pattern: Python collects all data first.
"""
import subprocess
from typing import List, Tuple
from pathlib import Path


def _run(cmd: List[str], cwd: str) -> Tuple[str, str, int]:
    """Run a shell command and return (stdout, stderr, returncode)."""
    result = subprocess.run(
        cmd, cwd=cwd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    return result.stdout, result.stderr, result.returncode


def get_current_branch(repo_path: str) -> str:
    """Return the name of the current git branch."""
    stdout, _, rc = _run(["git", "rev-parse", "--abbrev-ref", "HEAD"], repo_path)
    return stdout.strip() if rc == 0 else "unknown"


def get_diff(repo_path: str, base: str = "main") -> str:
    """
    Return unified diff between current branch and base.
    Falls back to staged changes if branch diff is empty.
    """
    stdout, _, rc = _run(
        ["git", "diff", f"{base}...HEAD"],
        repo_path,
    )
    if rc == 0 and stdout.strip():
        return stdout

    # Fallback: uncommitted changes
    stdout, _, rc = _run(["git", "diff", "HEAD"], repo_path)
    if rc == 0 and stdout.strip():
        return stdout

    # Fallback: staged
    stdout, _, _ = _run(["git", "diff", "--cached"], repo_path)
    return stdout


def get_diff_range(repo_path: str, commit_range: str) -> str:
    """Return diff for a specific commit range e.g. HEAD~3..HEAD"""
    stdout, stderr, rc = _run(
        ["git", "diff", commit_range],
        repo_path,
    )
    if rc != 0:
        return f"[Error getting diff: {stderr.strip()}]"
    return stdout


def get_changed_files(repo_path: str, base: str = "main") -> List[str]:
    """Return list of files changed vs base branch."""
    stdout, _, rc = _run(
        ["git", "diff", "--name-only", f"{base}...HEAD"],
        repo_path,
    )
    if rc != 0 or not stdout.strip():
        # Fallback to working tree changes
        stdout, _, _ = _run(["git", "diff", "--name-only", "HEAD"], repo_path)
    return [f.strip() for f in stdout.splitlines() if f.strip()]


def get_diff_stat(repo_path: str, base: str = "main") -> Tuple[int, int]:
    """Return (insertions, deletions) summary."""
    stdout, _, rc = _run(
        ["git", "diff", "--shortstat", f"{base}...HEAD"],
        repo_path,
    )
    if rc != 0 or not stdout.strip():
        stdout, _, _ = _run(["git", "diff", "--shortstat", "HEAD"], repo_path)

    insertions = deletions = 0
    import re
    m = re.search(r"(\d+) insertion", stdout)
    if m:
        insertions = int(m.group(1))
    m = re.search(r"(\d+) deletion", stdout)
    if m:
        deletions = int(m.group(1))
    return insertions, deletions


def get_recent_commits(repo_path: str, n: int = 5) -> str:
    """Return last N commit messages."""
    stdout, _, rc = _run(
        ["git", "log", f"-{n}", "--oneline"],
        repo_path,
    )
    return stdout.strip() if rc == 0 else ""


def get_commit_range_files(repo_path: str, commit_range: str) -> List[str]:
    """Files changed in a commit range."""
    stdout, _, _ = _run(
        ["git", "diff", "--name-only", commit_range],
        repo_path,
    )
    return [f.strip() for f in stdout.splitlines() if f.strip()]


def read_file(repo_path: str, file_path: str, max_chars: int = 4000) -> str:
    """Read a file from the repo (capped at max_chars)."""
    full_path = Path(repo_path) / file_path
    try:
        text = full_path.read_text(encoding="utf-8", errors="replace")
        if len(text) > max_chars:
            text = text[:max_chars] + f"\n... [truncated at {max_chars} chars]"
        return text
    except FileNotFoundError:
        return f"[File not found: {file_path}]"
    except Exception as e:
        return f"[Error reading {file_path}: {e}]"


def is_git_repo(repo_path: str) -> bool:
    """Check if the path is a git repository."""
    _, _, rc = _run(["git", "rev-parse", "--git-dir"], repo_path)
    return rc == 0

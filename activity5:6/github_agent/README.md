# 🤖 GitHub Repository Agent
A personalized AI agent that reviews code, drafts Issues and PRs, and improves existing ones — using local Ollama LLMs, real git tools, and the GitHub API.

---

## Architecture — 4 Agentic Patterns

```
┌─────────────────────────────────────────────────────────┐
│                      Orchestrator                       │
│                                                         │
│  ┌──────────┐  ┌──────────┐  ┌────────┐  ┌──────────┐  │
│  │ Reviewer │→ │ Planner  │→ │ Writer │→ │Gatekeeper│  │
│  └──────────┘  └──────────┘  └────────┘  └──────────┘  │
│  Tool Use      Planning       Multi-agent  Reflection   │
└─────────────────────────────────────────────────────────┘
```

| Pattern | Agent | What it does |
|---|---|---|
| **Tool Use** | Reviewer | Python runs `git diff`, reads files — LLM only reasons |
| **Planning** | Planner | Structured decision step before any drafting |
| **Multi-agent** | Writer | Separate drafting role: Issue vs PR vs Improve |
| **Reflection** | Gatekeeper | Critiques draft before human approval gate |

---

## Project Structure

```
github-agent/
├── agents/
│   ├── base.py          ← Ollama HTTP client + JSON extractor
│   ├── reviewer.py      ← Analyzes git diff
│   ├── planner.py       ← Decides action
│   ├── writer.py        ← Drafts Issue / PR / improvements
│   └── gatekeeper.py   ← Reflection + approval gate
├── tools/
│   ├── git_tools.py     ← git diff, log, file reads
│   └── github_tools.py  ← GitHub REST API client
├── models/
│   └── schemas.py       ← Typed dataclasses
├── web/
│   ├── main.py          ← FastAPI app
│   ├── routes.py        ← API endpoints + SSE stream
│   └── static/
│       └── index.html   ← Dashboard UI
├── orchestrator.py      ← Pipeline runner
├── cli.py               ← Click CLI
├── config.py            ← All settings
└── requirements.txt
```

---

## Quickstart

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Start Ollama
```bash
ollama pull llama3.2:3b
ollama serve
```

### 3. Configure
Edit `config.py`:
```python
REPO_PATH     = "/path/to/your/repo"
GITHUB_TOKEN  = "ghp_xxxx"    # github.com/settings/tokens
GITHUB_OWNER  = "your-username"
GITHUB_REPO   = "your-repo"
DRY_RUN       = True           # set False to write to GitHub
```

Or set environment variables:
```bash
export GITHUB_TOKEN=ghp_xxxx
export GITHUB_OWNER=nuzaer
export GITHUB_REPO=my-project
export REPO_PATH=/path/to/repo
```

---

## CLI Usage

```bash
# Review current branch vs main
python cli.py review --base main

# Review a specific commit range
python cli.py review --range HEAD~3..HEAD

# Draft a GitHub Issue
python cli.py draft issue --instruction "Add rate limiting to login endpoint"

# Draft a Pull Request
python cli.py draft pr --instruction "Refactor duplicated pricing logic"

# Approve and create on GitHub
python cli.py approve --yes

# Reject
python cli.py approve --no

# Improve an existing issue
python cli.py improve issue --number 42

# Improve an existing PR
python cli.py improve pr --number 17

# Use a live repo (disable dry-run)
python cli.py --live review --base main
```

### Expected CLI Output
```
[Orchestrator] · Starting review pipeline…
[Orchestrator] · [tool] git diff main...HEAD

──── Reviewer ─────────────────────────────────
  ▸ Analyzing diff — 3 file(s) changed
  ▸ [tool] diff stats: +47 -12 lines
  ▸ Calling LLM for code analysis…
  ▸ Review complete — category: bugfix | risk: high | action: create_issue

──── Planner ──────────────────────────────────
  ▸ Building action plan…
  ▸ Plan validated — action: create_issue | scope: …

──── Writer ───────────────────────────────────
  ▸ Drafting GitHub Issue…
  ▸ Issue draft ready: "Missing input validation in login API"

──── Gatekeeper ───────────────────────────────
  ▸ Running reflection on Issue draft…
  ▸ Reflection verdict: PASS

[Gatekeeper] Awaiting human approval…

python cli.py approve --yes
[Gatekeeper] Creating Pull Request...
[tool] GitHub API: create issue
Issue created: https://github.com/owner/repo/issues/43
```

---

## Web UI

```bash
uvicorn web.main:app --reload --port 8002
```

Open `http://localhost:8002`

Features:
- Live pipeline visualization with animated agent nodes
- SSE stream shows real-time agent activity
- Review, draft, improve — all from the browser
- One-click approve/reject with GitHub URL confirmation
- Settings panel for live config changes

---

## Three Core Tasks

### Task 1: Review Changes
```bash
agent review --base main
agent review --range HEAD~3..HEAD
```
- Runs git diff (Python tool, not LLM)
- Reviewer categorizes + assesses risk
- Planner justifies recommended action with diff evidence

### Task 2: Draft Issue or PR
```bash
agent draft issue --instruction "..."
agent draft pr    --instruction "..."
```
- Writer creates structured draft with all required fields
- Gatekeeper runs reflection (PASS/FAIL)
- Human must explicitly approve before GitHub write

### Task 3: Improve Existing
```bash
agent improve issue --number 42
agent improve pr    --number 17
```
- Fetches existing from GitHub API
- Writer critiques first, then rewrites
- Gatekeeper reflects, human approves

---

## Patterns Implementation

### Context-Gather (same as code-review-orchestra)
```python
# Python gathers all context first
diff_text = get_diff(repo_path, base)        # Python tool
files     = get_changed_files(repo_path, base)  # Python tool

# Then one LLM call with format="json"
result = agent.chat([{"role": "user", "content": prompt}])
data   = agent.parse_json(result)
```

### Human Approval Gate
Nothing reaches GitHub without passing:
1. Gatekeeper reflection (PASS/FAIL verdict)
2. Explicit `approve --yes` CLI command or dashboard button

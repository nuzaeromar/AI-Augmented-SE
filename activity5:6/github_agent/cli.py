"""
GitHub Agent — CLI

Usage:
  agent review --base main
  agent review --range HEAD~3..HEAD
  agent draft issue --instruction "Add rate limiting to login endpoint"
  agent draft pr    --instruction "Refactor duplicated pricing logic"
  agent approve --yes
  agent approve --no
  agent improve issue --number 42
  agent improve pr    --number 17
"""
import sys
import click
from rich.console import Console
from rich.panel   import Panel
from rich.rule    import Rule
from rich.table   import Table
from rich.text    import Text
from rich import box

from config      import Config
from orchestrator import Orchestrator, _load_state

console = Console()

AGENT_COLORS = {
    "Reviewer":     "#58a6ff",
    "Planner":      "#bc8cff",
    "Writer":       "#3fb950",
    "Gatekeeper":   "#e3b341",
    "Orchestrator": "dim white",
}

_current_agent = {"name": None}


def _emit(agent: str, message: str) -> None:
    color   = AGENT_COLORS.get(agent, "white")
    is_tool = message.startswith("[tool]")

    if agent in AGENT_COLORS and agent != "Orchestrator":
        if agent != _current_agent["name"]:
            _current_agent["name"] = agent
            console.print()
            console.rule(f"[bold {color}] {agent} [/]", style=color, align="left")
            console.print()

    if is_tool:
        console.print(f"    [dim italic]⟳ {message[6:].strip()}[/]")
    elif agent == "Orchestrator":
        console.print(f"  [dim]· {message}[/]")
    else:
        console.print(f"  [{color}]▸[/] {message}")


def _banner(cfg: Config) -> None:
    console.print()
    console.print(
        Panel.fit(
            "[bold white]🤖  GitHub Repository Agent[/]\n"
            "[dim]Planning · Tool Use · Reflection · Multi-agent[/]",
            border_style="bright_blue",
        )
    )
    console.print(
        f"  [dim]Repo:[/]  {cfg.REPO_PATH}\n"
        f"  [dim]Model:[/] {cfg.OLLAMA_MODEL}\n"
        f"  [dim]Mode:[/]  {'[yellow]DRY RUN[/]' if cfg.DRY_RUN else '[green]LIVE[/]'}"
    )
    console.print()


# ── CLI group ──────────────────────────────────────────────────────────────────

@click.group()
@click.option("--repo",  default=".", show_default=True, help="Path to local git repo")
@click.option("--model", default=None, help="Ollama model override")
@click.option("--live",  is_flag=True, default=False, help="Disable dry-run (writes to GitHub)")
@click.pass_context
def cli(ctx, repo, model, live):
    """GitHub Repository Agent — AI-powered code review and issue/PR management."""
    cfg = Config()
    if repo  != ".": cfg.REPO_PATH    = repo
    if model:        cfg.OLLAMA_MODEL = model
    if live:         cfg.DRY_RUN      = False
    ctx.ensure_object(dict)
    ctx.obj["cfg"]         = cfg
    ctx.obj["orchestrator"] = Orchestrator(cfg)
    _current_agent["name"] = None


# ── review ────────────────────────────────────────────────────────────────────

@cli.command()
@click.option("--base",  default="main", show_default=True, help="Base branch to diff against")
@click.option("--range", "commit_range", default="", help="Commit range e.g. HEAD~3..HEAD")
@click.pass_context
def review(ctx, base, commit_range):
    """Analyze git diff and recommend an action."""
    cfg   = ctx.obj["cfg"]
    orch  = ctx.obj["orchestrator"]
    _banner(cfg)
    console.rule("Pipeline", style="dim")

    try:
        report = orch.review(base=base, commit_range=commit_range, emit=_emit)
    except RuntimeError as e:
        console.print(f"\n[bold red]Error:[/] {e}")
        sys.exit(1)

    _print_review(report)
    console.print()
    console.print(
        f"  [dim]Run [bold]agent draft issue[/] or [bold]agent draft pr[/] to proceed.[/]"
    )


# ── draft ─────────────────────────────────────────────────────────────────────

@cli.command()
@click.argument("kind", type=click.Choice(["issue", "pr"]))
@click.option("--instruction", "-i", default="", help="Natural language instruction")
@click.option("--base", default="main", show_default=True)
@click.pass_context
def draft(ctx, kind, instruction, base):
    """Draft a GitHub Issue or PR with AI, then show for approval."""
    cfg  = ctx.obj["cfg"]
    orch = ctx.obj["orchestrator"]
    _banner(cfg)
    console.rule("Pipeline", style="dim")

    try:
        report = orch.draft(kind=kind, instruction=instruction, base=base, emit=_emit)
    except RuntimeError as e:
        console.print(f"\n[bold red]Error:[/] {e}")
        sys.exit(1)

    console.print()
    console.rule("Draft", style="bright_blue")
    console.print()

    if report.draft_issue:
        _print_issue_draft(report.draft_issue)
    elif report.draft_pr:
        _print_pr_draft(report.draft_pr)

    if report.reflection:
        _print_reflection(report.reflection)

    if report.reflection and report.reflection.verdict == "FAIL":
        console.print(
            "\n[bold red]Reflection verdict: FAIL[/] — "
            "revision required before approval."
        )
    else:
        console.print(
            "\n[dim]Run [bold]agent approve --yes[/] to create on GitHub, "
            "or [bold]agent approve --no[/] to abort.[/]"
        )


# ── approve ───────────────────────────────────────────────────────────────────

@cli.command()
@click.option("--yes", "decision", flag_value=True,  help="Approve and create on GitHub")
@click.option("--no",  "decision", flag_value=False, help="Reject and abort")
@click.pass_context
def approve(ctx, decision):
    """Approve or reject the pending draft."""
    cfg  = ctx.obj["cfg"]
    orch = ctx.obj["orchestrator"]
    _banner(cfg)

    # Load pending state for preview
    pending = _load_state(cfg)
    if not pending:
        console.print("[yellow]No pending draft. Run `agent draft` first.[/]")
        sys.exit(1)

    if decision:
        console.print()
        console.rule("Creating on GitHub", style="bright_blue")
        try:
            report = orch.approve(approved=True, emit=_emit)
        except RuntimeError as e:
            console.print(f"\n[bold red]Error:[/] {e}")
            sys.exit(1)

        if report.error:
            console.print(f"\n[bold red]GitHub Error:[/] {report.error}")
        elif report.github_url:
            console.print(
                Panel(
                    f"[bold green]✓ Created successfully[/]\n\n"
                    f"[link={report.github_url}]{report.github_url}[/link]",
                    border_style="green",
                )
            )
        else:
            console.print(
                "[yellow]DRY RUN — nothing was created. "
                "Set DRY_RUN=False in config.py or use --live.[/]"
            )
    else:
        orch.approve(approved=False, emit=_emit)
        console.print(
            Panel("[bold red]✗ Draft rejected. No changes made.[/]", border_style="red")
        )


# ── improve ───────────────────────────────────────────────────────────────────

@cli.command()
@click.argument("kind", type=click.Choice(["issue", "pr"]))
@click.option("--number", "-n", required=True, type=int, help="Issue or PR number")
@click.pass_context
def improve(ctx, kind, number):
    """Fetch an existing Issue/PR and suggest an improved version."""
    cfg  = ctx.obj["cfg"]
    orch = ctx.obj["orchestrator"]
    _banner(cfg)
    console.rule("Pipeline", style="dim")

    try:
        report = orch.improve(kind=kind, number=number, emit=_emit)
    except RuntimeError as e:
        console.print(f"\n[bold red]Error:[/] {e}")
        sys.exit(1)

    console.print()
    console.rule("Improvement", style="bright_blue")
    console.print()
    _print_improvement(report.improvement)

    if report.reflection:
        _print_reflection(report.reflection)

    if report.reflection and report.reflection.safe_to_proceed:
        console.print(
            "\n[dim]Run [bold]agent approve --yes[/] to apply the improvement.[/]"
        )


# ── Rich renderers ─────────────────────────────────────────────────────────────

def _print_review(report) -> None:
    r = report.review
    p = report.plan
    if not r:
        return

    risk_color = {"low": "green", "medium": "yellow", "high": "red"}.get(r.risk, "white")

    console.print()
    console.rule("Review Result", style="bright_blue")
    console.print()
    console.print(
        Panel(
            f"{r.summary}\n\n"
            f"[bold]Category:[/] {r.category}   "
            f"[bold]Risk:[/] [{risk_color}]{r.risk}[/{risk_color}]   "
            f"[bold]Action:[/] {r.recommended_action}",
            title="[bold #58a6ff]Code Analysis[/]",
            border_style="bright_blue",
        )
    )

    if r.issues_found:
        console.print("\n[bold]Issues Found[/]")
        for issue in r.issues_found:
            console.print(f"  [red]●[/] {issue}")

    if p:
        console.print()
        console.print(
            Panel(
                f"[bold]Action:[/] {p.action}\n"
                f"[bold]Scope:[/]  {p.scope}\n\n"
                f"{p.rationale}",
                title="[bold #bc8cff]Planner Decision[/]",
                border_style="magenta",
            )
        )


def _print_issue_draft(draft) -> None:
    risk_color = {"low": "green", "medium": "yellow", "high": "red"}.get(
        draft.risk_level, "white"
    )
    evidence_md  = "\n".join(f"  [dim]·[/] {e}" for e in draft.evidence)
    criteria_md  = "\n".join(f"  [green]☐[/] {c}" for c in draft.acceptance_criteria)

    console.print(
        Panel(
            f"[bold white]{draft.title}[/]\n\n"
            f"{draft.problem_description}\n\n"
            f"[bold]Evidence:[/]\n{evidence_md}\n\n"
            f"[bold]Acceptance Criteria:[/]\n{criteria_md}\n\n"
            f"[bold]Risk:[/] [{risk_color}]{draft.risk_level}[/{risk_color}]   "
            f"[bold]Labels:[/] {', '.join(draft.labels)}",
            title="[bold]📋 Issue Draft[/]",
            border_style="bright_blue",
        )
    )


def _print_pr_draft(draft) -> None:
    risk_color = {"low": "green", "medium": "yellow", "high": "red"}.get(
        draft.risk_level, "white"
    )
    files_md = "\n".join(f"  [dim]·[/] {f}" for f in draft.files_affected)

    console.print(
        Panel(
            f"[bold white]{draft.title}[/]\n\n"
            f"{draft.summary}\n\n"
            f"[bold]Files Affected:[/]\n{files_md}\n\n"
            f"[bold]Behavior Change:[/]\n  {draft.behavior_change}\n\n"
            f"[bold]Test Plan:[/]\n  {draft.test_plan}\n\n"
            f"[bold]Risk:[/] [{risk_color}]{draft.risk_level}[/{risk_color}]   "
            f"[bold]Base:[/] {draft.base_branch}   "
            f"[bold]Labels:[/] {', '.join(draft.labels)}",
            title="[bold]🔀 PR Draft[/]",
            border_style="bright_blue",
        )
    )


def _print_reflection(reflection) -> None:
    verdict_color = "green" if reflection.verdict == "PASS" else "red"
    verdict_icon  = "✓" if reflection.verdict == "PASS" else "✗"

    content_parts = [
        f"[bold {verdict_color}]{verdict_icon} {reflection.verdict}[/bold {verdict_color}]"
    ]
    if reflection.issues:
        content_parts.append("\n[bold]Issues:[/]")
        for i in reflection.issues:
            content_parts.append(f"  [red]✗[/] {i}")
    if reflection.suggestions:
        content_parts.append("\n[bold]Suggestions:[/]")
        for s in reflection.suggestions:
            content_parts.append(f"  [yellow]→[/] {s}")
    if reflection.missing_fields:
        content_parts.append(
            f"\n[bold]Missing:[/] {', '.join(reflection.missing_fields)}"
        )

    console.print()
    console.print(
        Panel(
            "\n".join(content_parts),
            title="[bold #e3b341]🔍 Gatekeeper Reflection[/]",
            border_style="yellow",
        )
    )


def _print_improvement(improvement) -> None:
    if not improvement:
        return

    console.print("[bold]Critique:[/]")
    for c in improvement.critique:
        console.print(f"  [red]✗[/] {c}")

    console.print()
    console.print(
        Panel(
            f"[bold white]{improvement.improved_title}[/]\n\n"
            f"{improvement.improved_body[:1500]}"
            + ("\n[dim]... (truncated)[/]" if len(improvement.improved_body) > 1500 else ""),
            title=f"[bold]Improved {improvement.kind.upper()} #{improvement.original_number}[/]",
            border_style="green",
        )
    )

    if improvement.changes_made:
        console.print("\n[bold]Changes Made:[/]")
        for c in improvement.changes_made:
            console.print(f"  [green]✓[/] {c}")


if __name__ == "__main__":
    cli(obj={})

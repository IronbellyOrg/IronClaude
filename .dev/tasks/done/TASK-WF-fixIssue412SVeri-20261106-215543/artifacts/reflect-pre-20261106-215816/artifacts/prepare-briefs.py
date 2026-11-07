"""Materialize verbatim grounding and coverage slices for the three reviewers."""
import json
from pathlib import Path

OUT = Path(__file__).resolve().parents[1]
PACKAGE = OUT.parents[1]
ROOT = next(p for p in OUT.parents if (p / "src/superclaude/cli/install_user_setup.py").is_file())
card = (OUT / "t1-card.md").read_text()
assert "RF_PLACEHOLDER" not in card
matrix = json.loads((OUT / "artifacts/coverage-matrix.json").read_text())

def hunk(path, start, end):
    text = "\n".join((ROOT / path).read_text().splitlines()[start - 1:end])
    return f"### {path}:{start}-{end}\n```text\n{text}\n```\n"

root_state = f"codegraph run state: index_state=fresh checked_at=2026-11-06T21:59:00Z worktree_root={ROOT} projectPath={ROOT}\n"
plan_rel = str((PACKAGE / (PACKAGE.name + ".md")).relative_to(ROOT))
spec_rel = str((PACKAGE / "source.md").relative_to(ROOT))
brief_dir = OUT / "reviewer-briefs"
brief_dir.mkdir(exist_ok=True)
for n, persona, low, high in [(1, "analyzer", 1, 7), (2, "qa", 8, 15), (3, "refactorer", 16, 21)]:
    path = brief_dir / f"reviewer-{n}.md"
    assert not path.exists()
    path.write_text("## T1 card excerpt\n{{RF_PLACEHOLDER:card}}\n\n## Grounding hunks\n{{RF_PLACEHOLDER:grounding}}\n\n## Coverage slice\n{{RF_PLACEHOLDER:coverage}}\n")
    content = path.read_text()
    content = content.replace("{{RF_PLACEHOLDER:card}}", "```text\n" + card + "```\n")
    grounding = root_state + f"\nPersona: {persona}. UC-1 proposed plan review only, not a completed-work audit. No shell, git, writes, execution or remediation. Return findings to parent for persistence. Assume errors; report PASS or FAIL, blocking versus minor, plus Self-Audit if no blocking findings. Do not treat a speculative execution mistake as an actual plan contradiction.\n\n"
    grounding += hunk(plan_rel, 1, 52)
    grounding += hunk("src/superclaude/cli/install_user_setup.py", 230, 263)
    grounding += hunk("src/superclaude/cli/install_user_setup.py", 434, 444)
    if persona == "qa":
        grounding += hunk(spec_rel, 1, 1)
        grounding += "Audit the matrix against this entire spec body. Surface any requirement-bearing span absent from the matrix.\n"
        grounding += "Verification: existing installer + matching tests lint passed; no pytest, red/green, UI launch, guide install or dry-run executed in this pre-review. Evidence: ../verify-logs/invocations.yaml.\n"
    grounding += "Read-only Orca discovery (artifacts/orca-discovery.md): version-matched guide names agent launch/worktree create --agent as agent routes and terminal create as shells/commands; explicit surface selects chat or terminal. Installed installer help states only Orca-owned unmodified copies update; edited/foreign copies are skipped and reported unless external --force is used. No actual installation was invoked.\n"
    if persona == "refactorer":
        grounding += "The two main CLI callers pass install_user_setup(force=force) for install and force=True for update. No new component or abstraction is proposed. Core CLAUDE.md already has a byte-equal routing-table test; proposed edits must not disturb that block. No global install is authorized to test it.\n"
    content = content.replace("{{RF_PLACEHOLDER:grounding}}", grounding)
    rows = [r for r in matrix["rows"] if low <= int(r["id"].split("-")[1]) <= high]
    coverage = "| Requirement | Verbatim source quote | Deterministic match | Ratio |\n|---|---|---|---|\n"
    for row in rows:
        coverage += f"| {row['id']} | {row['quote']} | {','.join(row['matched_task_ids']) or 'none'} | {row['containment_ratio']} |\n"
    coverage += "\n13/21 lexical matches overall. Zero parsed IDs, 21 inferred rows; parsed-sparse. Shared constraints are outside the task-only matcher. Lexical misses are not by themselves proven missing requirements. Inspect original source and constraints before grading a gap.\n"
    content = content.replace("{{RF_PLACEHOLDER:coverage}}", coverage)
    assert "RF_PLACEHOLDER" not in content
    assert content.count("\n## Grounding hunks") == 1
    path.write_text(content)
print("Materialized 3 reviewer briefs from on-disk source; no input modified.")

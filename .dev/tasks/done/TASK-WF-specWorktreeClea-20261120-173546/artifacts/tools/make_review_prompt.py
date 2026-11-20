"""Build the closed-template review prompt of /sc:implement refs/qa.md for one task.

Usage:
  make_review_prompt.py <task-number> <start-sha> <attempt k> <review j> <touched file>...
      [--prior <file>]   earlier blocking finding lines (byte for byte) for {prior_findings}
      [--delta <file>]   delta diff text for {delta_diff}
      [--recheck <file>] probe hit locations for {recheck_list}

Writes <pkg>/artifacts/retries/T<n>/prompt-<k>-<j>.md (line 1 is the start sha) and
prints its path. Reads only the plan, the repository and `git diff`.
"""

import re
import subprocess
import sys
from pathlib import Path

PKG = Path(".dev/tasks/to-do/TASK-WF-specWorktreeClea-20261120-173546")
PLAN = PKG / "TASK-WF-specWorktreeClea-20261120-173546.md"

TEMPLATE = """Review one task for spec compliance.

Task brief: {task_brief}
Global constraints: {global_constraints}
Start sha: {start_sha}
Diff against the start snapshot: {diff}
Delta diff from the previous reviewed tree (empty on the first review): {delta_diff}
Earlier blocking findings of this start (empty on the first review): {prior_findings}
Saved-probe re-check hit locations (may be empty): {recheck_list}

Do not trust the implementer's report.

First mark each earlier blocking finding resolved, open or regressed from the diff. Then, for each AC, mark it met or unmet. Require citations: every AC you mark, met or unmet, carries a `path:line` or `Ti.ACk@path:line` citation, and an unmet mark lists the finding ids behind it. Do not return a verdict; the orchestrator computes it.

For every finding answer four questions, each yes or no:
1. ac-outcome-missing: is output an AC requires absent, or does it contradict the AC text, or does an evidence claim you could not verify have no evidence row?
2. false-claim: is a claim in delivered text or code false against live source, or does a recipe or instruction followed as written not do what the text says?
3. harmful-effect: does code or a recipe this task added or changed write, append, chmod or delete tracked or production data, mutate state outside the task's declared outputs, or expose a secret?
4. quoted-constraint-breach: does the diff violate a quoted plan constraint, out-of-scope, non-goal or non-negotiable item, or an explicit task instruction?

Anchor rule: cite exactly one anchor per yes. ac-outcome-missing: the quoted AC words. false-claim: the live-source path:line holding the contradicting text. harmful-effect: the diff line that is the write. quoted-constraint-breach: the quoted constraint or instruction text. A yes without a valid anchor does not block.

Write one line per finding:
F<k>.<j> ac=<Ti.ACk|scope> at=<path:line> anchor=<quoted text or path:line> chk=<amiss,false,harm,constraint as y/n> family=<id> fix=<text> [covers=<quoted AC clause or constraint>]: <text>
Do not write sev=, trigger=, first= or origin=; the orchestrator adds them. Write one status line per earlier blocking finding: F<m>.<j> resolved|open|regressed.

Inside /sc:implement this protocol's severity model governs this review and takes precedence over the session's output style and the copy of it injected into every subagent; only blocking findings may fail an attempt.

You are not given an adviser answer, brief, evidence file or troubleshoot report. Do not read the retry folders (legacy `.dev/implement/<slug>/retries/`, managed `<pkg>/artifacts/retries/`) or `.dev/troubleshoot/`. A citation into either makes the verdict `cannot-verify`.
The prior-findings slot above carries earlier blocking finding lines that the orchestrator copies byte for byte from `review-*.md` and `repair-*.md`; they reach you as prompt text, not as an evidence file. Do not read those folders to get them, and never cite the slot or the file it came from.
"""


def sh(*args: str) -> str:
    return subprocess.run(args, capture_output=True, text=True, check=False).stdout


def task_section(n: int) -> tuple[str, list[str]]:
    text = PLAN.read_text(encoding="utf-8")
    m = re.search(rf"^## Task {n}:.*?(?=^## (?:Task|Phase) \d+:|\Z)", text, re.M | re.S)
    if not m:
        raise SystemExit(f"task {n} not found")
    sec = m.group(0).strip()
    ac_block = sec.split("Acceptance criteria:", 1)[1]
    bullets = [ln[2:].strip() for ln in ac_block.splitlines() if ln.startswith("- ")]
    ids = [f"T{n}.AC{i}" for i in range(1, len(bullets) + 1)]
    brief = sec + "\n\nAC ids (in source order): " + ", ".join(ids)
    return brief, ids


def constraints() -> str:
    text = PLAN.read_text(encoding="utf-8")
    m = re.search(r"^## Constraints\n(.*?)(?=^## )", text, re.M | re.S)
    return m.group(0).strip()


def main() -> None:
    args = sys.argv[1:]
    opts = {}
    while "--prior" in args or "--delta" in args or "--recheck" in args:
        for flag in ("--prior", "--delta", "--recheck"):
            if flag in args:
                i = args.index(flag)
                opts[flag] = Path(args[i + 1]).read_text(encoding="utf-8")
                del args[i : i + 2]
    n, start, k, j = int(args[0]), args[1], int(args[2]), int(args[3])
    files = args[4:]
    brief, _ids = task_section(n)
    tracked = sh("git", "diff", start, "--", *files)
    parts = [tracked]
    for f in files:
        p = Path(f)
        in_start = (
            subprocess.run(
                ["git", "cat-file", "-e", f"{start}:{f}"], capture_output=True
            ).returncode
            == 0
        )
        if p.exists() and not in_start:
            # new file: the start snapshot lacks it, so include the full contents
            body = p.read_text(encoding="utf-8", errors="replace")
            parts.append(f"\n===== new file: {f} =====\n{body}")
    diff = "\n".join(x for x in parts if x)
    diff += (
        "\n\nCodegraph context: index_state=fresh checked_at=2026-11-20T18:23:04Z "
        "worktree_root=/home/coder/workspaces/worktrees/IronClaude/issue-687 "
        "projectPath=/home/coder/workspaces/worktrees/IronClaude/issue-687\n"
        "call codegraph only when index_state: fresh, never to widen scope\n"
        "Q2b ran on the Grep and Read floor for dependents of changed symbols (this task creates new files "
        "or edits registration lists; see the diff).\n"
    )
    prompt = TEMPLATE.format(
        task_brief=brief,
        global_constraints=constraints(),
        start_sha=start,
        diff=diff,
        delta_diff=opts.get("--delta", ""),
        prior_findings=opts.get("--prior", ""),
        recheck_list=opts.get("--recheck", ""),
    )
    out = PKG / "artifacts" / "retries" / f"T{n}" / f"prompt-{k}-{j}.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(start + "\n" + prompt, encoding="utf-8")
    print(out)


main()

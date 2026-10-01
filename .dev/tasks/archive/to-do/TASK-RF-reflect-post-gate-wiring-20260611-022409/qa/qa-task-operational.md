# QA — Agent D: Operational-Correctness Lens (relayed from inline return)

VERDICT: FAIL (raw) — 1 finding ACCEPTED + fixed, 1 REJECTED.

## Confirmed PASSes
1. Flag reality — `superclaude reflect run --help` exposes `--promote/--no-promote`, `--depth [standard|deep]`, `--output`, `--fix/--no-fix`, `--base` (cross-checked `commands.py:89-145`). No invented flags.
2. O2 `--output` preserves the declared `**Reflect Report Path:** TASKLIST_ROOT/validation/reflect-post/phase-<PP>/REPORT.md` + its AC (default would orphan it).
3. Path tokens — wrapper Click-resolves the positional (`commands.py:76-80 resolve_path=True`); O1 emits `{TASK_FILE}`, O2 emits `TASKLIST_ROOT/phase-<PP>-tasklist.md`; no fabricated generation-time SHA/abspath.
4. O2 `--base <PHASE_N_START_SHA>` single-ref runtime resolution present in both files; Step-1 `[VERIFICATION]` documented.
5. O1 omits `--base`; frontmatter `start_commit` seeded from `git merge-base HEAD <integration-branch>`; precedence correct.

## Findings
- **D1 (IMPORTANT) — ACCEPTED + FIXED.** SKILL:100 + struct-check #5 permitted frontmatter OMISSION ("when no frontmatter is present…"), but the wrapper returns `frontmatter-missing` → BLOCKED (exit 2) on a frontmatter-less phase file (`runner.py:146-148`). Fix: both assertions now state the block is REQUIRED when reflect gating is enabled (the O2 writeback target), omittable only under `--no-reflect`.
- **D2 (MINOR) — REJECTED.** "Remove the xfail decorator now that it XPASSes" contradicts OQ-1 (operator chose to KEEP `strict=False` → XPASS). Agent D lacked OQ-1 context.

Commands run by the agent: `reflect run --help` (PASS), dry-run `--print-command` against the task file (PASS — confirms O1 `--base`-omission → frontmatter `start_commit` resolution), `pytest tests/cli/reflect/ -q` (77 passed, 1 xpassed), `make verify-sync` (PASS).

See `qa-task-consolidated.md` for the full triage + re-verification.

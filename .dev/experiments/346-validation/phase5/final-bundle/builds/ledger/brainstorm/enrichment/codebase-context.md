# Codebase context: ledger theme (issue 346)

Source tier: `fallback_1` (native Grep/Read in this worktree; the auggie MCP tool is not available in this session's tool list, codegraph not needed for prose files). Every line below was read in this worktree on 2026-11-08 unless marked as from another worktree.

## 1. Current spec-panel contract (PR 427 + master)
- `src/superclaude/commands/spec-panel.md:22` Usage carries `[--re-review <prior-findings-file> --baseline <saved-copy>]`; file is 486 lines on master (427 itself was 472).
- `src/superclaude/commands/spec-panel.md:256` `## Review Loop`, 7 one-line bullets: Mode, Grading (CRITICAL and FR-8/FR-9 blocking; MAJOR blocking only with a concrete wrong outcome), Verdict (last line `verdict: PASS|FAIL`), Cap (`review: N of 3`, at review 3 with FAIL: HALT and escalate), Re-review output (prior-blocking table `resolved|open|regressed`, then findings on lines changed vs baseline with `origin=changed|unchanged`), Reviser contract (`Reviser brief` above verdict; revise only named text; add no mechanism), Precedence (a brief may narrow, not widen).
- `docs/designs/spec-panel-review-loop.md:143`: "every rule here is prose read by a model. The tests prove the text is present and in the right order, not that a reviewer obeys it." `:162`: "nothing enforces the count".
- Test: `tests/skills/test_spec_panel_review_loop.py` (text-presence T1-T10); pins in `tests/skills/test_review_severity_rule.py` (canonical cap text, `AT_CAP_CLAUSES`).

## 2. Prior art for a computed verdict and a mechanical origin
- `/sc:implement` (`src/superclaude/skills/sc-implement-protocol/refs/qa.md`):
  - `:97`, `:334`: the reviewer returns per-AC met/unmet with citations "and no verdict"; "Do not return a verdict; the orchestrator computes it."
  - `:135-144`: one finding per line `F<k>.<j> sev=... ac=... at=<path:line> anchor=<quoted text> ... origin=...`; the parent, not the reviewer, writes `sev=`, `trigger=`, `first=`, `origin=`; one status line per prior blocking finding `F<m>.<j> resolved|open|regressed`.
  - `:150-166`: origin `inherited|late|fix-induced|new|unknown` is decided by the parent from exact line text; inherited findings are "capped at note, mechanically from the `git diff "$start"` hunk headers".
  - `:191`: re-review = full audit plus delta diff; prior blocking marked resolved/open/regressed.
  - Lesson: implement already separates "reviewer reports" from "orchestrator decides", but still lets every re-review raise new blockers anywhere in task-owned text (`:186`).
- rf-qa (`src/superclaude/agents/rf-qa.md:379-416`): Fix Cycle re-verifies only prior blocking issues (steps 1-5), "Do not recheck minor findings"; a monotonicity rule `|F_{n+1}| < |F_n|` else HALT `[HALT-MONOTONICITY] |F|=<n>`; regression detection first. These are prose, executed by the agent itself.
- Scripts bundled in skills are run as `uv run --no-project python "<skill base>/scripts/<name>.py"` (`src/superclaude/skills/sc-implement-protocol/refs/managed-workspace.md:54`), tested under `tests/skills/` (`test_workflow_archive.py`). `superclaude install` copies a whole skill directory (`src/superclaude/cli/install_skill.py:52`, `shutil.copytree`), so a script inside a skill reaches `~/.claude/skills/<skill>/scripts/`. A command file alone cannot carry a script.

## 3. Observed reviewer and reviser behaviour (other worktrees, read-only)
- `exp346-ab-flg-r2/.dev/orca-command-refactor/review/spec-panel-round3.md`: Part 1 is already a per-finding resolution table (N1-N11 + citation notes: status, evidence, note); all 6 prior blocking resolved; new N12 (MAJOR, blocking, origin=changed) was created by the N5 fix, which added a new "record the agent command" step; 3 new minor notes. Verdict FAIL at review 3, escalated.
- `exp346-ab-flg-r2/.dev/orca-command-refactor/review/disposition-round2.md`: one row per finding (blocking yes/no, verified, disposition, where in revised spec); 15/15 applied, including all 9 minor; "Related defects found while applying" (E5, AC-1.2) fixed in the same pass: reviser widens scope beyond named rows. Reviser tagged each change with the finding id (grep-able).
- Brief text still says "any finding of any severity is FAIL" (round-3 report, Decisions table), so the command's grading competes with the brief.
- The round-3 reviewer computed changed lines itself with `git diff --no-index -w -U0` and listed hunk lines: the changed-line set is already mechanically derivable.

## 4. Reach
- `/sc:reflect` (`src/superclaude/skills/sc-reflect-protocol/SKILL.md`): Tier 1/Tier 2 reviewer fan-out, evidence-validator gate, no loop counter or prior-findings input of its own; loop is driven by the caller.
- `/sc:implement` final review (`refs/qa.md:311`): FINAL is one fresh subagent per archive attempt, returns `pass` or `issues` with `path:line` per AC.
- rf-qa: Fix Cycle above; used by task-builder, tech-research, prd/tdd gates.

## 5. Implications for the ledger theme
- A ledger row schema can reuse implement's finding-line keys (`anchor=`, `at=`, `origin=`, status line) instead of inventing one.
- The verdict can be computed by a script from the ledger, as implement already does in prose; spec-panel would be the first place where a script, not a model, does it.
- The changed-line set per round is derivable by `git diff --no-index -U0` between saved copies, so "is this new finding on a changed line" and "which rows did the fix touch" can be computed.
- Freezing severity at review 1 is a data rule (the script refuses a severity change on an existing row unless a `reopened` transition carries a reason), which addresses upward drift.

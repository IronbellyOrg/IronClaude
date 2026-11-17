# A.10.5 Qualitative Validation: Consolidated Findings (cycle 1)

Sources: `qa/qa-qualitative-operational-report.md` (VERDICT: FAIL, 3 blocking, 9 minor), `qa/qa-qualitative-sufficiency-report.md` (VERDICT: FAIL, 1 blocking, 3 minor). Agent counts per gate all meet minimums (research 10, synthesis 10, report 13, fidelity 4, anti-omission 4).

Orchestrator action already taken: `RUN2-QUEUED.md` (it named the run-2 commit) was moved out of the run-1 task folder to `.dev/tasks/to-do/REVIEW-PANEL-UNIFY-RUN2-QUEUED.md`; no file referenced it. Operational minor note on it is closed.

## Blocking findings (fix all)

| ID | Severity | Where | Defect | Fix |
|---|---|---|---|---|
| Q-B1 | CRITICAL | Step 5.2 debate item (~line 290) | `/sc:adversarial --compare` takes comma-separated paths (`~/.claude/commands/sc/adversarial.md`); the item passes two space-separated paths, so the protocol sees one file and stops. Every debate would fail. | Use `--compare <dir>/proposal-a.md,<dir>/proposal-b.md` (no space). Also correct the same form in BUILD-REQUEST.md line ~42 for consistency. |
| Q-B2 | CRITICAL | Step 5.2 (~290) and `### Phase 5 Adversarial Sub-Checklist` (~531-533) | Run-time `- [ ]` items are added outside `<!-- DYNAMIC CONTENT START -->` / `<!-- DYNAMIC CONTENT END -->` markers; the /task executor forbids adding checklist items elsewhere (task SKILL.md; template 02 rule I6), so it would stop at Step 5.2. | Put the two markers inside the `### Phase 5 Adversarial Sub-Checklist` section and tell the Step 5.2 items to add entries only between them. |
| Q-B3 | IMPORTANT | Step 5.2 completion check (~294) | The pattern `Adversarial result:** pending` is a regex in which `**` is not literal; it matches nothing, so a missed write-back passes. | Escape it (`Adversarial result:\*\* pending`) or use fixed-string matching, and state the expected count 0. |
| Q-B4 | IMPORTANT | Step 7.1 hash-mismatch path (~446), with items ~386, ~392, ~394, ~396 | On a hash change, Step 7.1 re-runs the Step 6.6 verifiers, which skip themselves when no fix agent ran this cycle, so the decision item records PASS without the 13-lens report gate seeing the changed report; line 386 expects 7.1 to come through Step 6.5, which line 446 bypasses. | On a hash mismatch, route through Step 6.5 first: record the change as a blocking finding (`report changed after final validation`) in `qa/qa-consolidated-findings-phase6.md`, run the single fix agent and both verifiers, then 6.7, 6.7b, 6.8 as already written, each within its own cap. |

## Minor notes promoted to fix in this pass (real weaknesses, cheap)

| ID | Where | Fix |
|---|---|---|
| Q-M1 | synthesis-gate reviewer items (~308, ~316) | Change "C01-C13 at minimum" to "C01-C14 at minimum". |
| Q-M2 | items that run `uv run python scripts/reflect_shadow_exit.py` | State that exit code 1 is expected (Stage 2 exit currently FAIL, 13 of 20 runs) and the agent records the output rather than treating the non-zero exit as a tool failure. |
| Q-M3 | Execution Context / Phase 1 | State the absolute repository root `/home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel` once in Phase 1 and in each agent prompt that runs commands. |
| Q-M4 | Step 7.3 "no `.claude/` path staged" check | Scope the check to the repository-root `.claude/` directory (`git diff --cached --name-only | grep '^\.claude/'` must be empty except `.claude/settings.json`); paths under `.dev/tasks/` (including any `agent-memory` subfolder) are part of `.dev/tasks` staging and allowed. |

## Minor notes (record only)

- `tests/cli/reflect` holds 38 test files, not 12; `_ID_TOKEN` is at `telemetry.py:23` (not :22).
- Phase 3 decision item says "five" items above it; there are four.
- New fix cycles re-run items already marked done; mid-cycle resume is not clean.
- Step 6.1 `[CONTRADICTION:` grep pattern is rejected as invalid regex (loud failure; use fixed-string).
- Web research phase has no own gate (by BUILD-REQUEST design).
- >3000-line report: 5 lenses split in 2 instead of 6 per type (allowed by BUILD-REQUEST cap).

VERDICT (consolidated, cycle 1): FAIL — 4 blocking + 4 promoted fixes.

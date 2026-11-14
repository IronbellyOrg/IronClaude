# Fix log, contract gate cycle 1 (item 12.14)

Date: 2026-11-12. Fix agent: single fix agent, `fix_authorization: true`. Findings in scope: CON-F1 and CON-F2 (|F_0| = 2) from `qa/contract/consolidated-findings-cycle0.md`. Owner decision record: `phase-outputs/plans/OQ-3-addendum-wc16-wait-timeout-decision.md` (status RESOLVED, "Approve both fixes").

## Files edited

| File | Edit | Line after the change |
|---|---|---|
| `src/superclaude/commands/sweep.md` | the Triggers sentence (CON-F1) | `src/superclaude/commands/sweep.md:20` |
| `src/superclaude/core/WORKER-CONTRACT.md` | WC-16 first words (CON-F2) | `src/superclaude/core/WORKER-CONTRACT.md:277` |
| `docs/designs/orchestrator-mode.md` | the same WC-16 words in the section 8 "Final text" fenced block (CON-F2) | `docs/designs/orchestrator-mode.md:679` |
| `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/phase-outputs/test-results/step-1.17-checks.md` | appended the dated section "Re-run after the cycle-1 fix" (no existing text rewritten) | appended after the former last line, "Overall: all checks PASS." |
| `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/qa/contract/fix-log-cycle1.md` | this log | n/a |

Every edit to the three owner-approved places was anchored by quoted text (Edit with the exact old sentence), not by line number.

## CON-F1

Status: FIXED.

Change: in `src/superclaude/commands/sweep.md`, "Explicit only: the coordinator runs `/sc:sweep` on every wake, or a person types it." became "Explicit only: the coordinator runs `/sc:sweep` inside its liveness sweep pass, at most once every 5 minutes (WC-16 in `~/.claude/WORKER-CONTRACT.md`), or a person types it." The sentence holds no stop, retry, release, merge or removal word and no em dash (a case-insensitive grep of the whole line for `stop|retry|release|merge|removal` and the em dash printed 0 matches).

After the change: `src/superclaude/commands/sweep.md:20`. `grep -n 'every wake' src/superclaude/commands/sweep.md` prints no line (exit 1).

Not done, as instructed: `make sync-dev` (a later plan step copies the file to `.claude/`).

## CON-F2

Status: FIXED.

Change: in the WC-16 paragraph, "On every coordinator wake, at most once every 5 minutes, the coordinator runs "The sweep."" became "On every coordinator wake or wait timeout, at most once every 5 minutes, the coordinator runs "The sweep."". Nothing else in WC-16 changed. The same words changed in the DESIGN section 8 "Final text" fenced block. DESIGN row R2 (line 716) and every other DESIGN line were not touched. The pinned phrase "On every coordinator wake" is still a substring, so no test pin changed.

After the change: `src/superclaude/core/WORKER-CONTRACT.md:277` and `docs/designs/orchestrator-mode.md:679`.

Byte comparison (check 5 of the step 1.17 checks file): the command as written prints `differ: byte 1, line 1` (exit 1) because the contract diff against HEAD now also holds the line-23 hunk from item 12.2, which was not in the diff when the check was first run (3 added non-blank lines against the DESIGN block's 2). With that one line filtered out the comparison prints `identical` (exit 0), and a full byte compare of `WORKER-CONTRACT.md` lines 275 to 277 against the whole DESIGN fenced block, blank lines included, prints `identical-with-blank-lines` (exit 0). So the contract paragraph and the DESIGN block are byte-identical. The as-written check 5 now reports FAIL for the line-23 reason only; the record is in the "Re-run after the cycle-1 fix" section of `phase-outputs/test-results/step-1.17-checks.md`. A later reader who re-runs check 5 unchanged will see the same difference.

## Re-check commands and results

Run in this order after the edits, from the repository root.

| # | Command | Exit | Last lines of output | Result |
|---|---|---|---|---|
| 1 | `uv run ruff check tests/skills/test_worker_contract.py` | 0 | `All checks passed!` | PASS |
| 2 | `uv run ruff format --check tests/skills/test_worker_contract.py` | 0 | `1 file already formatted` | PASS |
| 3 | `uv run pytest tests/skills tests/core tests/commands tests/recommend -v` | 0 | `============================ 2641 passed in 57.46s =============================` (0 lines with FAILED or ERROR) | PASS |
| 4 | `grep -c 'src/superclaude' src/superclaude/core/WORKER-CONTRACT.md` against `git show HEAD:src/superclaude/core/WORKER-CONTRACT.md \| grep -c 'src/superclaude'` | 0 | `now=0 head=0` | PASS (same count, 0) |
| 5 | `grep -n 'every wake' src/superclaude/commands/sweep.md` | 1 (no match) | no output | PASS (expected no hit) |
| 6 | `git diff -U0 -- src/superclaude/core/WORKER-CONTRACT.md` | 0 | hunks `@@ -23 +23 @@` (1 changed line, the never-as-worker list from item 12.2) and `@@ -274,0 +275,4 @@` (4 added lines: the `### WC-16. Coordinator loop` heading, a blank line, the WC-16 paragraph, a blank line); `git diff --stat` says `1 file changed, 5 insertions(+), 1 deletion(-)` | PASS (5 added lines and 1 changed line as before; the only text changed in this cycle is inside the WC-16 paragraph) |

Checks 1 to 6 of `phase-outputs/test-results/step-1.17-checks.md` were re-run, and the output is appended there. Checks 1, 2, 4 and 6 PASS. Check 3 PASS for the WC-16 hunk (whole-file totals now include the line-23 hunk). Check 5 as written FAILS only because of the line-23 hunk and both adjusted comparisons PASS (see CON-F2 above).

Not run here on purpose: `make sync-dev` and `make verify-sync` (a later plan step does them).

## Files not touched

I did not touch: `WORKER-CONTRACT.md` lines 110 and 151, any other WC-16 sentence, any existing WC-14 reference, DESIGN row R2 (line 716) or any other DESIGN line, `tests/` and every test pin, the revision folder, any OQ record, any QA report, `consolidated-findings-cycle0.md`, the cycle ledger, the plan file, `src/superclaude/cli/sweep/`, `src/superclaude/skills/sc-sweep-protocol/SKILL.md`, `src/superclaude/output-styles/pragmatic.md`, and any `.claude/` or installed HOME path. The 18 MINOR findings (CON-F3 to CON-F20) were left as notes. I staged nothing and committed nothing. No live Orca, ccsession or Claude command was run.

## Executor re-run of the item 12.5 commands (after the fix agent returned)

- `uv run ruff check tests/skills/test_worker_contract.py`: exit 0, last line: All checks passed!
- `uv run ruff format --check tests/skills/test_worker_contract.py`: exit 0, last line: 1 file already formatted
- `uv run pytest tests/skills tests/core -v`: exit 0, last line: ============================ 2008 passed in 52.45s =============================
- `grep -c 'src/superclaude' src/superclaude/core/WORKER-CONTRACT.md`: exit 1, last line: 0
- `uv run pytest tests/commands tests/recommend -q`: last line: ============================= 633 passed in 5.36s ==============================
- `grep -n 'every wake' src/superclaude/commands/sweep.md`: 0 hits

The executor also confirmed with sha256sum -c that none of the 63 protected files changed (baseline taken at the T274 start, before the fix agent ran), that WC-16 line 277 of the contract is byte-identical to the DESIGN section 8 block paragraph, and that only the four allowed files changed.

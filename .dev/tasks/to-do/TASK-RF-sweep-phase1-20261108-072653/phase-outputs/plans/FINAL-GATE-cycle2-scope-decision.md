# Final gate, fix cycle 2: owner decision (2026-11-12)

Status: RESOLVED by the owner. Chosen: option 1.

## Context

Item 14.28 (re-evaluated on the re-check reports) ended with F_1 = {FIN-F5, FIN-F7} and the outcome "Continue to fix cycle 2". Both findings need an edit the fix agent may not make. The orchestrator recommended fixing FIN-F5 in cycle 2 and ruling on FIN-F7 at item 14.32: FIN-F5 touches 5 places; FIN-F7 would mean rewriting the output-style exception (7 sites in `pragmatic.md`), the revision addendum, DESIGN 7.6 and the tests, for a limitation that the report at the printed path already states. Making an Orca outage exit non-zero would break DESIGN section 5 (partial data still publishes and exits 0).

## Owner's words

"Option 1" (answering: 1 fix FIN-F5 only and rule on FIN-F7 at 14.32; 2 fix both; 3 skip cycle 2 and take both findings to a ruling).

## What is approved

- FIN-F5 only, including the edit of DESIGN `docs/designs/orchestrator-mode.md` line 614: the header banner keeps its current text only when Orca really was unavailable; when Orca answered but `orca worktree ps` is unscanned (list truncated, call failed, budget), it reads `[child worktrees not discovered: orca worktree ps unscanned (<reason>); worktree count is a lower bound]`, with `<reason>` the sanitized `unscanned` text of the `orca worktree ps` source row. The code (`report.py`) and the two test pins (`test_report.py`, `test_cli_contract.py`) move together with the DESIGN line.
- FIN-F7 is NOT fixed in cycle 2. It stays OPEN; item 14.32 will hit its two-cycle cap if FIN-F7 is still open, and the open finding is then escalated to the owner for a ruling (documented limitation, filed in the follow-up issue) instead of a third fix cycle.
- DESIGN section 13 is not changed.

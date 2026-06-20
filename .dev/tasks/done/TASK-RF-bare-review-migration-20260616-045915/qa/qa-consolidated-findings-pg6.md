# PG6 Consolidated Findings (WS-D OPS docs QA — M3 + M4)

**Status: In progress**
**Initial verdict: FAIL (2 CRITICAL + minors)** → fix cycle 1 dispatched
**Date:** 2026-06-16

## Agent verdicts (8 agents: 6 M3 lens + 2 M4 fidelity, all report-only)
| # | lens/agent | verdict | report |
|---|-----------|---------|--------|
| 1 | ops-completeness | PASS | `qa-structural-ops-completeness-report.md` |
| 2 | cross-reference-integrity | PASS | `qa-structural-crossref-integrity-report.md` |
| 3 | evidence-quality | **FAIL** | `qa-structural-ops-evidence-quality-report.md` |
| 4 | deferred-capability-honesty | PASS | `qa-content-deferred-capability-report.md` |
| 5 | halt-discipline | PASS | `qa-content-halt-discipline-report.md` |
| 6 | operational-actionability | **FAIL** | `qa-content-operational-actionability-report.md` |
| 7 | source-fidelity-1 (OPS-001..003) | PASS | `qa-source-fidelity-report-1.md` |
| 8 | source-fidelity-2 (OPS-004..006) | PASS | `qa-source-fidelity-report-2.md` |

## Issues to fix (verified independently by the orchestrator)
**C1 (CRITICAL, evidence-quality):** `--custom-prompt-dir` is cited as a `swarm run` CLI flag in `docs/swarm/operator-runbook.md` (propagated from `docs/swarm/command-reference.md:48`), but it is NOT a registered Click option on `swarm run` (confirmed absent from `swarm run --help`; it is the JobSpec field `custom_prompt_dir`). FIX: correct/remove the `--custom-prompt-dir` flag citation in `operator-runbook.md` AND `command-reference.md:48`.

**C2 (IMPORTANT, evidence-quality):** `docs/swarm/command-reference.md` OMITS the 4 real WS-0 `swarm run` flags `--reviewers`/`--target-line-cap`/`--timeout-sec`/`--label` (all present in `run --help`). This is a WS-0-completeness gap in the flag authority. FIX: add the 4 flags to `command-reference.md` (necessary deviation — keeps the doc authority accurate for the WS-0 flags this migration added).

**C3 (MINOR, evidence-quality):** `post-release-metrics.md` calls the EventRecord field `worker` where it is `worker_index`. FIX: correct the field name.

**C4 (CRITICAL, operational-actionability):** `docs/swarm/rollback-procedure.md` has a FACTUALLY WRONG git model — it claims the 5 legacy files were "deleted via `git rm` by MIG-003 (T08.07)" and that `b0de1479` is the pre-migration parent. GIT REALITY (verified): the legacy files EXIST in HEAD `2355bfe1` (no commit ever deleted them; the WS-C deletions are STAGED-only in this task and will be committed as part of the M8/M9 migration); `b0de1479` is 28 commits back; the parent of HEAD is `00576c43`. The Option A (`git revert 2355bfe1`) and Option B (`git checkout b0de1479 -- ...`) recovery commands would NOT restore the legacy path. FIX: rewrite the git-recovery section to the accurate model — the legacy files are in commit `2355bfe1` (current HEAD, before this migration's deletion is committed); rollback = revert the M8/M9 migration commit(s) once landed; individual-file restore = `git checkout 2355bfe1 -- <legacy path>` (or robustly find the deletion commit via `git log --oneline --diff-filter=D -- <path>` and check out its parent). Do NOT hardcode `b0de1479`.

## Non-blocking observations (no fix required)
- O1 (crossref): `post-release-metrics.md` cites sibling docs as bare backtick paths (not clickable links) — paths resolve; informational.
- O2 (fidelity-2): the `complete/` vs live `current/` tasklist disagree on OPS-004 rigor; the rollback doc satisfies the stricter bar (documents + retains PENDING appendix).
- O3 (halt-discipline): the follow-up + pending record cite the appendix as `:162-169` (the heading+warning) while the literal table is `:171-178` — accurate target, citation-precision only.
- O4 (completeness): OPS-004 rehearsal unstamped is an EXECUTION gap (tracked as the HIGH HALT follow-up), not a doc-completeness gap.

## Fix
1 fix cycle dispatched (serialized rf-qa fix agent, `fix_authorization: true`). Counter: `phase-outputs/plans/pg6-cycle-count.md` = 1.

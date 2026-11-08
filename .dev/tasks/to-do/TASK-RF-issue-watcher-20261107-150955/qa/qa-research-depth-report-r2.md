# QA Report: research-depth, gap-fill re-check round 1 (rf-qa-qualitative)

**Date:** 2026-11-07. **Fix cycle:** 1. **fix_authorization:** false.
**Provenance note:** the reviewing agent is barred from writing report files and returned the report in its message; the orchestrator saved the findings here (condensed).

## Overall Verdict: FAIL

File 06 closes four of the six earlier depth findings (POST `{BASE}` via DF-07, gate sizes via DF-08, gate commands via DF-05/DF-09, five commands via DF-06). It does not close the crash-recipe finding or the merged-register finding, introduces an ordering error in the gate map, and leaves the stub protocol unable to express AC-19.

## Issues (all IMPORTANT, blocking)

| # | Location | Issue | Required fix |
|---|---|---|---|
| I-1 | 06 Table 1.6 and P9 row | M4 fidelity gate is placed before the Final gate; template M4/I21 and SKILL.md lines 1150, 1181-1183 require M4 after the M3 gate | Order: final M3 gate (7 agents) first, then M4 (2 agents). Note that M4 is intentionally 2 agents per SKILL.md line 1151 and I22 so the sufficiency lens does not apply the line-2140 rule to it |
| I-2 | 06 DF-15, Table 1.3 | (a) the C2 `os.replace` patch is not disarmed before the five reruns, so each rerun's pending save raises again; (b) the C3 trigger is unimplementable as written (no Store call sits between `save(pending)` and `launch()`), and the rationale "k-th write cannot express C3 or C4" is false; (c) the lock-release requirement is missing: `SystemExit` passes through `with store.lock()`, reruns work only if `FileStore.lock` releases in a `finally` | (a) the C2 fake fires once or `monkeypatch.undo()` runs before reruns; (b) C1 raise before delegating save 1; C3 delegate save 1 then raise in the same call; C4 raise at save 2 before delegating, after the FakeLauncher recorded; C5 delegate save 2 then raise; delete the false rationale; (c) state that `lock()` releases in a `finally` in the `record.py` item and the crash test items |
| I-3 | 06 header, DF-40, DF-21 | No disposition for research-05 G-06 (REASONS kind/exit mapping, `re-approved`), G-07, G-09 (`fail` from `failed` is not a T-row but attempts must reach 3), G-10, G-11, G-12, G-13 (account-rename test), G-14, G-15, G-17, G-21, spec-vs-design deviations X1 to X5 (S1, C20, C22, `last_completed_cycle_at`, `status` exit 1) and owner questions Q1 to Q4 (design line 866); DF-40 says 06 is the only decision source; DF-21 says "dual surface" without a path (`.claude/skills/sc-issue-protocol/refs/claim.md` is missing in this worktree and exists in CI only after `make sync-dev`) | Add DF rows or one row carrying each 05 treatment unchanged; add Q1 to Q4 and X1 to X5 to the Open Questions; pin `test_marker_contract` to `src/superclaude/skills/sc-issue-protocol/{refs/claim.md,templates/claim-comment.md}` |
| I-4 | 06 Table 1.4, DF-34, P8 | Table 1.4 cannot express AC-19 (design line 892, a sleeping stub ends with `gh_timeout`): no `sleep` field; in subprocess mode the 20 s timeout cannot be shrunk; the log has no flag for the "unscripted argv fails at teardown" rule; the stub-orca snapshot of `dispatch.json` (research 05 section 3) is absent | Add an optional `sleep` field and a `matched` flag; decide AC-19 explicitly (for example call `SubprocessRunner` against a sleeping stub with a shrunk timeout, cover exit 3 and the 120 s cutoff in-process with FakeRunner timed-out replies and FakeClock) and record the departure from design line 892 as a deviation; add a state-dir env var for the stub-orca snapshot or drop that e2e assertion |

## Minor notes (non-blocking)

M-1 the G-7 grep misses `from datetime import UTC`; M-2 G-3 wrongly says xdist is untested (it resolves offline, xdist 3.8.0) so drop the SKIP allowance; M-3 record the expected item count (about 160) and paged-Read cost; M-4 assign agent types to the lenses (3 rf-qa, 3 rf-qa-qualitative per gate) and note the SKILL size-scaling and the `standard` source (research-notes); M-5 DF-07 "owner-authorized" has no quoted source, the commit carries the 83 pre-staged `.dev/tasks` files, later task-file edits need a fresh `git add .dev/tasks`, `git rev-parse HEAD` is a more exact BASE than the merge-base, no local hook exists; M-6 DF-03 `operator_reset` kind skip versus a warning line: state the rule; M-7 `linkbin/env` symlink unnecessary, G-2 claim "every test that can see the change" overstated.

VERDICT: FAIL

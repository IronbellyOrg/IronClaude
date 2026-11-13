# T1 reflection card (UC-1, pre-execution)

- spec: `.dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md` (378 lines, design spec v3, issue #375)
- plan: `.dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/TASK-WF-designSpec-20261107-075614.md` (200 lines, 13 tasks, 5 phases)
- attribution note: the plan was already executed (PR #428, commit 0b8a5801d is the only commit that touches `merge_guard.py`). A defect is a plan or spec defect only if it existed at plan time; post-implementation HEAD state is evidence of what execution found, not a plan failure.

## Coverage (Step 1B.0, deterministic script `artifacts/coverage-map.py`)

- Pass 1 (ID_REGEX `R-/REQ-/SPEC-/T-`): 0 parsed ids in the spec and 0 in the tasklist. The spec labels its requirements FR-n, F-n, G-n, O-n, which the regex does not match.
- Pass 2: 90 inferred rows, each quote-pinned to one spec line (0 dropped). Containment match (>= 0.6 of content words in one task item): 74 matched, 16 unmatched.
- `coverage_pct` null (parsed total 0). `coverage_pct_union` 0.8222. `coverage_degraded: parsed-sparse` (90 inferred > 0 parsed), which forbids a Tier-1 stop.
- `S_dev_density` = (16 + 0) / 90 = 0.1778 (mechanical, union denominator). Below 0.20, so rule 5 alone would not escalate.
- Manual read of the 16 unmatched rows: all 16 have a covering task. INF-004, 010, 013, 023, 034, 044, 045, 046, 052, 075, 081 map to Tasks 3, 4, 7, 11. INF-048, 049 map to Tasks 6 and 12. INF-078, 079, 080 are tasklist constraints with no task of their own. The unmatched count is a limit of word-overlap matching, not a plan gap.
- Method limit: tasks are 150 to 500 words each, so containment of a short quote is easy to satisfy. 16 matches fall between 0.60 and 0.75 and deserve a human look (listed in `artifacts/coverage-matrix.json`, key `thin_matches_lt_0.75`).

## Findings

### Deviation / root-cause slice (analyzer lens)

- T1-F1 (MAJOR, not blocking): the guard record's `cycle_id` is never defined as updated. The fold field list names `cycle_id` (source.md:190) but no row of the effect table sets or changes it after the first request. `held_cycle_published` and resume row 4 key on it (source.md:108, 166). Engage row 7 returns `NOOP(already_held)` for any later cycle that finds the guard HELD (source.md:139), so a second cycle reusing a held draft leaves `guard.cycle_id` stale and the release or the resume check is judged against the earlier cycle's push. The plan has no acceptance criterion for it (plan:61 covers only `guard_status`; Tasks 3 and 4 list no cycle rebinding case). The shipped code added a `REBIND` action for exactly this (`src/superclaude/pr_submit/merge_guard.py:438-442`), so execution had to discover it.
- T1-F2 (MAJOR, not blocking): Task 8 narrows the spec's source sections. The spec says the protocol ref carries "sections 3 and 4.1 to 4.4" (source.md:240); the plan builds it "from ./source.md sections 3, 4.1, 4.5, 4.6 and 5" (plan:124). Sections 4.2 (event fields, `timeline_baseline`, `original_is_draft`, the `guard:<run_id>:<cycle_id>:<to>:a<k>` key), 4.3 (flag) and 4.4 (the `--read` JSON that feeds `GuardRead`) are left out, and no acceptance criterion asks the ref to state the event fields. The shipped ref does carry them, so the executor compensated.
- T1-F3 (MINOR): `guard_status` and the unavailable halt disagree. The spec says a halt with reason `draft_guard_unavailable` reports `unavailable` (source.md:112), but the read-failed and timeline-unreadable engage halts (source.md:135, 140) happen before any `requested` event, so the log has no guard record and the first-match mapping returns `released`. Plan:61 pins "no record at ordinal 3 (released)"; the engage-failure scenario test of plan:166 covers only the `--to draft` failure path.

### Coverage / acceptance slice (qa lens)

- T1-F4 (MINOR): "once per cycle id" has no decision-table home. Engage rows compare `cycle_id` only against conflict prefixes (source.md:133); a RELEASED guard with the same cycle id gets `ENGAGE` again (row 11). The spec test `test_guard_engages_at_routed_finding_once_per_cycle` and plan Task 10's criterion assert the behaviour without saying which function enforces it.
- T1-F5 (MINOR): the release-gate statement "the PR body states the gate plainly" (source.md:326) appears only as text recorded by Task 1 (plan:33) and mentioned in Task 12 (plan:182). No task writes the PR body and no acceptance criterion checks it.
- T1-F6 (MINOR): the spec wants one cycle id shared by the guard events, the push key and `rereview_requested` (source.md:251). The acceptance-trace test checks event order only (plan:170); nothing asserts the three ids are equal.

### Structural / tech-debt slice (refactorer lens)

- T1-F7 (MINOR): Task 2's grep criterion ("shows no remaining claim that the enum has 43 members", plan:49) is a judgment call, not a mechanical check; `models.py` keeps a legitimate comment "the 42nd-43rd" for the conflict events, so a literal "no `43`" reading fails and a loose reading cannot fail.

## Refuted candidates (not findings)

- No task grants `Bash(scripts/set-draft-state.sh *)` in the `SKILL.md` front matter: refuted, `test_allowed_tools_cover_every_program` adds `scripts/` words to a separate set and only checks the files exist.
- Import cycle `run_log` -> `merge_guard` -> `conflicts`: refuted, `fsm.py` and `conflicts.py` do not import `run_log`; Task 5 also runs a fresh-interpreter import check.

## Grounding gaps

- Live GitHub behaviour (gates G1 live part, G2 live part, G4, G5, G6) is out of reach by design (source.md:326) and recorded as OPEN, not checked.
- Facts F1 to F13 describe master `e8db2fe6` on 2026-11-07; HEAD now has 45 `EventType` members (the plan's own target), so they were not re-verified against the pre-execution tree.

# Merged reflection verdict: v3 plan (UC-1 pre-execution)

<!-- Source: Variant 3 (base) - verdict line and structure -->
Plan file: /home/coder/workspaces/worktrees/IronClaude/claim-handoff-planb/.dev/tasks/to-do/TASK-WF-requirements-20261119-012839/TASK-WF-requirements-20261119-012839.md (`plan:N` is a line of it; `source.md:N` is a line of source.md next to it; `guard` is src/superclaude/hooks/scripts/launch-level-guard.sh).
Verdict: FAIL as advice. 3 blocking (Q-1, Q-3, Q-4), 1 owner decision on an unverified safety claim (Q-2, kept open), 3 medium (Q-5 to Q-7), 3 notes (Q-8 to Q-10). Corrected after the evidence-validator gate (see the last section).

<!-- Source: Variant 3 (base), Variant 1, Variant 2 - confirmed-fixed line -->
Confirmed fixed: all earlier findings P-1 to P-11 were found fixed by all three reviewers (V1, V2, V3). V3 adds a caveat on P-4 (see Q-3).

## Findings (register Q-1 to Q-10)

<!-- Source: Variant 3 F-1 (base), Variant 2 QA-1, Variant 1 A-4; refactor plan Q-1 -->
### Q-1 BLOCKING (Safety)
- Task: Task 10 and Constraints (R24, R25), as cited by V3 F-1; the plan cites plan:23 and plan:158.
- Evidence: the guard classifies `gh issue create`, `issue edit` and `issue comment` as SUBMIT (guard:653) and allows SUBMIT at Full Submit (guard:790). plan:23 says the guard keeps refusing issue comments at Worktree, Full and Full Submit; plan:158 tests only Worktree and Full. A Full Submit agent runs under the watcher's login, which is in the approvers file (source.md:64) and is not excluded by approval_of (predicates.py:216-223), so it can post issue comments (solid) and, by inference, apply the approval label to another issue the owner already set to Full Submit (this needs a trigger label on that issue first, predicates.py:228, and an agent running `gh issue edit --add-label`).
- Fix: move the `issue` verbs out of SUBMIT into a class refused at every level (keep the `pr` verbs for /sc:pr-submit; check that /sc:pr-submit needs no issue verb), add Full Submit refusal tests, and name the coordinator-only pattern (guard:444) with must-refuse cases (verb form, module form) and must-allow cases (plan-hash and check-approval, named in the comment at guard:442-443; where `stage-status` is allowed is not established).

<!-- Source: Variant 3 F-2; refactor plan Q-2 -->
### Q-2 OWNER DECISION (Safety claim not verified; plan:25 is an explicit owner decision and plan:28 forbids real claims, so it is not graded blocking, and it stays open)
- Task: Tasks 17 and 7, Constraints (plan:25), R25 (V3 F-2).
- Evidence: claim.md:133 sets a ship gate: no `worktree` or `full` claim on a real issue until OB-H1 item 1, OB-H2 and OB-H3 pass; the launch-level design (docs/designs/sc-issue-launch-level-hook.md) also requires item 1 before `full` or `--submit`. The plan neither checks nor mentions it, while Task 17 enables repos automatically and R25 launches those levels. Whether the gates have passed was not read.
- Fix: a task checks a recorded gate result and the watcher refuses non-None Pipeline values until it is recorded as passed, or the owner waives it explicitly. See "Decisions needed from the owner".

<!-- Source: Variant 3 F-3 (fail-open half), Variant 1 A-3; refactor plan Q-3 -->
### Q-3 BLOCKING (Decision)
- Task: Tasks 3 and 4, R31 (plan:55, plan:58, plan:65).
- Evidence: Task 3 proves only that `updatedAt` exists. R31 needs that a Pipeline or Status change moves the Project item's updatedAt (otherwise the rule fails open and the provenance hole stays) and that applying the approval label does not (a label bumps the issue, probably not the item; unverified). A field change is a write, so the agent may not run it.
- Fix: Task 3 adds an observation the owner runs on a test issue; if wrong, the R31 fallback (level-specific approval label) goes back to the owner. See "Decisions needed from the owner".

<!-- Source: Variant 1 A-1, Variant 2 QA-2; refactor plan Q-4 -->
### Q-4 BLOCKING (Decision)
- Task: Task 4 (plan:71) and Task 6 (plan:108).
- Evidence: Task 4 gives `edited_after_approval` and Task 6 gives `revalidation_failed` for the same reread; `_revalidate` raises `revalidation_failed` for every failure (cycle.py:1007-1016).
- Fix: name which reason wins and test the overlapping case.

<!-- Source: Variant 2 QA-3; refactor plan Q-5 -->
### Q-5 MEDIUM
- Task: Task 9.
- Evidence: Task 9 takes repo and issue number but no configured Project id, so an issue on several Projects may get its Status moved on the wrong item (predicates.py:268 selects by project id).
- Fix: pass the configured Project id, select the exact live item, refuse ambiguous or missing targets before any mutation.

<!-- Source: Variant 1 A-7 and notes; refactor plan Q-6 -->
### Q-6 MEDIUM
- Task: Task 9 (marker comment).
- Evidence: the marker comment counts the watcher's own login, which equals the coordinator's login on this host.
- Fix: say so in the design note.

<!-- Source: Variant 1 A-2; refactor plan Q-7 -->
### Q-7 MEDIUM
- Task: Task 6 (with Task 7, plan:114).
- Evidence: Task 6 acceptance (plan:109) requires test_security_invariants.py (and test_no_shell.py) to pass, but test_security_invariants.py pins the old single prompt (reviewer-read at test_security_invariants.py:5-6; the checker did not re-read it) and only Task 7 (plan:114) rewrites it.
- Fix: Task 6 rewrites them or drops them from its acceptance.

<!-- Source: Variant 1 A-5, Variant 3 F-6; refactor plan Q-8 -->
### Q-8 NOTE
- Task: Task 11 (plan:166).
- Evidence: Task 11 rewrites lines 911-919 of test_security_invariants.py; line 919 asserts "String!" not in query (DF-14).
- Fix: say how it is restated.

<!-- Source: Variant 3 F-5 (downgraded); refactor plan Q-9 -->
### Q-9 NOTE
- Task: Task 10 (plan:23, plan:158).
- Evidence: the level-None claim session has no level record (claim.md:118, 122: the governed-launch step runs only for non-none levels); the guard reads a level from a session's record and treats an unrecognised record as W (guard:262-268), and its not-governed handling is at guard:257-258; bound workers are governed by the TAMPER class (guard:441-444). plan:23 names only Worktree, Full, Full Submit.
- Fix: state which sessions are governed.

<!-- Source: Variant 1 A-6, Variant 3 F-7, F-8; refactor plan Q-10 -->
### Q-10 NOTE
- Task: Tasks 1, 4, 6, 8, 9, 11, 15.
- Evidence and fix, as the plan states: Task 4 depends only on Task 3 (plan:67; Task 6 at plan:104 already orders it after Task 1); Tasks 4, 6, 12 and 18 edit cycle.py, so state the order (Task 1 leaves cycle.py unchanged, plan:34); Task 15 relies on an argv scan Task 9 extends (plan:216) but does not list Task 9 in its dependencies; a retry after the coordinator mirrors the Status needs a fresh approval; the WORKER-CONTRACT.md:245 sentence must not let the coordinator push worker commits, since at Full Submit the launched agent pushes.

Not adopted (per the plan): V2 blanket Blocking labels; V3 F-5 as medium; the "every approval voided" half of F-3 as a confirmed defect.

## Decisions needed from the owner

<!-- Source: refactor plan Q-2 and Q-3 options; Variant 3 F-2, F-3 -->
### Q-2 Ship gate (claim.md:133)
- Option A: a task checks a recorded gate result (OB-H1 item 1, OB-H2, OB-H3), and the watcher refuses non-None Pipeline values until it is recorded as passed.
- Option B: the owner waives the gate explicitly.

### Q-3 Does a field change or a label move the Project item's updatedAt (R31)
- Option A: Task 3 adds an observation the owner runs on a test issue (a field change is a write, which the agent may not run).
- Option B: if the observation shows the rule would fail open or void approvals, the R31 fallback (level-specific approval label) goes back to the owner.

## No-finding list

<!-- Source: Variant 1 Checked line -->
- V1 checked about 30 symbols, lines and files and found them matching: predicates.py 105-275, cycle.py 905-1130, cli.py 30-137, guard 784-803, WORKER-CONTRACT.md 21-24 and 236-305, issue.md 40-60, test_security_invariants.py 1-30, 705-735, 905-925.
<!-- Source: Variant 3 fixed-line citations -->
- V3 confirmed the earlier-finding fixes at plan:23, 114, 141, 152, 166, 172, 254, 259, 55, 65, 81, 179, 289, 146, 82, 133, 147, 274, 279 (P-4 carries the Q-3 caveat).
- V3 found no source that writes a Status today, so the claim itself does not trip the rule; a move to In review fails project_check anyway (from F-7).

## Corrections after the gate

The evidence-validator found: Q-1's must-allow list cited guard:442-443 for the pattern (the pattern is line 444) and named `stage-status`, which the guard does not mention (fixed); the label half of Q-1 is inference (marked); Q-2 was graded blocking though its gate status was never read (changed to an owner decision, kept open); Q-7 named test_no_text.py in Task 6's acceptance (it names test_no_shell.py; fixed); Q-9's lines 262-268 show the opposite of "not governed" (restated with guard:257-258); Q-10's list of cycle.py editors was wrong (fixed). docs/designs/sc-issue-launch-level-hook.md was not read by the checker.

## Not checked

<!-- Source: Variant 3 and Variant 1 not-checked lines -->
- V3: tests/hooks bodies; the H3 handling of `gh project item-edit` (assumed UNKNOWN); the DF-14 rationale; the grounding artifact; full launch.py and github.py.
- V1: tests/hooks bodies; test_module_boundaries.py; conftest.py.
- Whether OB-H1, OB-H2 and OB-H3 have passed (V3 F-2, inferred).
- GitHub behaviour of updatedAt on field and label changes (unverified until the Q-3 observation).

# Round 2 rebuttal, advocate for Variant 2

## Response to criticisms

- **Resume inputs (F1); "the SKILL can supply target_sha" (V1 R1).** Rejected. Spec 109 gives `resume_decision` no `target_sha` or `applied_edits`. The fold keys at spec 189-191 hold neither, and `held_cycle_published` returns only a bool (spec 108). The SKILL would need a source the spec never names. The defect is real; its origin is the spec.
- **F3 and F4 over-flagged (V1 R1, V3).** Conceded. Both move to non-blocking.
- **F9 (flag inertness).** Conceded and withdrawn. Plan 73 returns NOOP at ordinal 2 and with `off`; plan 172 forbids any `pr ready` there.
- **F11 (fold rows).** Defended. Plan 60 lists `settled(draft, failed)` but not `settled(ready, failed)`, `settled(draft, confirmed, changed)`, `settled(ready, confirmed, changed)` or `settled(any, skipped, user_override)`. "Covers every row" cannot be checked against that list. MINOR.
- **F2 wording.** Partly conceded. Spec 205 does contain the `settled(ready, failed)` fold row, so the gap is in the plan's criteria, not the spec's fold. The spec gap is that the release table (spec 147-157) has no retry row or cap, and spec 315 names a retry test without a rule. "already_in_state" is not script output; spec 231 prints `changed:false`.
- **F5 (Wave 0).** Conceded. Plan 137 bans "`L3 only` or `draft` gate wording"; plan 140 bans "an L3 or `draft` condition", which a correct "at L3 with off" bullet fails. Spec 241 contradicts itself, so the origin is the spec.
- **F7 (case list).** Narrowed. V1 F5 is the stronger version of the same gap.

## Updated assessment of V1 and V3

- **V1:** The best card on the failed-release path and the unique scope items: the PR body and the opening run's `--merge-guard off` (spec 326), and the `not_applied` ready branch (spec 201). Its F4 survives only as the resume row 8 HOLD, which is real and spec-origin. Its F1 severity was wrong, as it concedes.
- **V3:** The best plan-hygiene card (C-007, C-011, C-013 to C-016). Its C-006 MAJOR holds only if the existing S5a and pre-push pins are prefix-only. If they are full sentences, V2 F6 is right. It missed C-002, C-003, C-004 and C-010, as it concedes.

## New evidence

1. Spec 189-191 (folded keys) confirms F1 is spec-origin.
2. Plan 153's parenthetical says an unconditional engage fails, but the test checks for two phrases only, so an unconditional sentence containing both passes.
3. Plan 37 accepts "no id minted today" for O1, while spec section 1, fact F4, states that nothing in code or protocol text mints a fix or CI id. The deferral is by design; the missing equality check is not.

## Points still split

- **C-005 (Task 11 strength): V1 superior.** The stub gap is real. Decisive line: plan 169 requires only that the twelve names be defined, and plan 170 to 172 attach behavioural assertions to the trace, crash and forbidden-call checks, not to the named tests. The engage-once, exit-hold, engage-failure, release-retry, toggle, timeline and script-contract tests carry no assertion requirement.
- **C-020 (flag inertness): V1 and V3 superior.** Withdraw F9. Decisive line: plan 73 returns NOOP at ordinal 2 and with `off`, and plan 172 forbids any `pr ready` at ordinal 2 or with `off`.
- **X-004 (do empty stubs pass?): V1 superior.** Yes, for the names-only tests, so V1's MAJOR is right, but non-blocking. Decisive line: plan 169's only requirement for those tests is that their names exist.

Overall: V2 is still the only card whose blocking findings stop a build as written (F1, F2). It is not the best card on the Task 11 or flag questions.

## Revised findings (severity, blocking, origin)

| Finding | Severity | Blocking | Origin |
|---|---|---|---|
| F1 resume inputs | MAJOR | yes | spec-origin (spec 107, 109, 166, 189-191) |
| F2 retry rule | MAJOR | yes | spec-origin (spec 147-157 has no retry row or cap); plan adds the missing case |
| F3 shared cycle id | MAJOR | no | plan-origin (no equality or off-invariance check); O1 deferral is by design |
| F4 Wave 3 test | MAJOR | no | plan-origin (plan 153 overclaims) |
| F5 Wave 0 wording | MINOR | no | spec-origin (spec 241) |
| F6 byte-identical | MINOR | no | plan-origin (plan 154); MAJOR only if the pins are prefixes |
| F7 Task 11 cases | MINOR | no | plan-origin; folded into V1 F5 |
| F8 autoMergeRequest | MINOR | no | spec-origin (spec 230 shows a boolean; gh's shape unverified here) |
| F9 flag inertness | withdrawn | no | covered by plan 73 and 172 |
| F10 Depends-on | MINOR | no | plan-origin; V3 F6 is the fuller list |
| F11 fold rows | MINOR | no | plan-origin (plan 60) |
| F12 settled(draft, failed) | MINOR | no | spec-origin (spec 150, 199) |

The blocking count falls from four to two.

Not checked: gh's live `autoMergeRequest` shape (offline).

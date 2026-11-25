# Diff Analysis: position paper comparison (D01 trigger and approval gate)

## Metadata
- Generated: 2026-11-20 (UTC)
- Variants compared: 2 (Variant A = OURS `variant-1-original.md`, Variant B = CLAY `variant-2-original.md`)
- Total differences found: 19 (S 2 + C 11 + X 2 + A 4)
- Categories: structural (2), content (11), contradictions (2), unique (8 listed, not counted in the denominator), shared assumptions (4: 3 UNSTATED promoted, 1 STATED)
- Taxonomy tags per point: L1 surface, L2 structural, L3 state-mechanics (assigned by auto-tag rule, highest level wins)

## Structural Differences

| # | Area | Variant A (OURS) | Variant B (CLAY) | Severity | Level |
|---|---|---|---|---|---|
| S-001 | Mechanism section | Describes the kept master code (`approval_of`, `unchanged_since`, `project_check`, ship gate) | Describes the new PR 686 flow (R1, DQ1, search, hold, bounded automation) | Low | L1 |
| S-002 | Closing rule | Five-condition start rule (assignment, approval unedited, Status allow-list, no `hold:backlog`, `plan_check` ok) | One-condition start rule (assignment) plus plan check and `hold:backlog` | Medium | L2 |

## Content Differences

| # | Topic | Variant A approach | Variant B approach | Severity | Level |
|---|---|---|---|---|---|
| C-001 | Is assignment sufficient to start work? | No: necessary, never sufficient; assignment is an ownership act and is itself an effect of `/sc:issue --claim` (SKILL.md:87) | Yes: a person who assigns has decided; a second act defeats the purpose | High | L2 |
| C-002 | Who can assign versus who can approve | Same three accounts (ironbelly admin, clayphi, IB-JonathanB maintain), so the gate adds a deliberate act, not narrower trust | Same three accounts, so removing the approval narrows nothing | Medium | L2 |
| C-003 | The "only triage or write can assign" premise | Unproven: marked UNVERIFIED in issue 655; design OQ6 lists two gaps (read-only self-assign, bots/apps) | Accepts the premise, contained by the repo allow-list and day cap | Medium | L2 |
| C-004 | Worth of the approval given same-login agents (L-1) | Gate proves a deliberate act by an approved login; weakness is shared by any login-based signal | A gate the same login can pass is a speed bump, not a person | Medium | L3 |
| C-005 | Plan check as the readiness signal | Presence-only (`hold.py:131`: "does not say whether the plan is good"); no replacement for a decision | Real new signal the approval never gave; cheap | Medium | L2 |
| C-006 | Binding approval to issue content (edit after approval) | `unchanged_since` is the only code binding "what a person said yes to" to "what the worker reads"; PR 686 has no equal | Not silent (corrected after verification, `orchestrator.md:488`, AD-A3 / ruling 23): edits before the claim are "fine"; wave 1 re-runs `plan_check` and `hold:backlog` live; after the claim an edit is one report line; `body_sha` is "a record, not a check" and the hourly check names a non-user editor. So B decided deliberately not to bind content to a person's reading | High | L3 |
| C-007 | Consequence profile of the trigger | Same assignment now ends in a worker, a push and an orchestrator merge, on an unprotected `master`, with no guard (DQ7, DQ8) | Safety moves to bounded automation: repo allow-list, day cap, 3 in flight, 62 audit reasons, merge conditions with `--match-head-commit` | High | L3 |
| C-008 | What the owner's records say | R19, R35 and "Gates that stay manual" keep the approval; R36 withdraws only R31 | Owner trend is fewer gates (R35 label to field, R36, Q36 "for now", #339 "no manual sessions") | Medium | L2 |
| C-009 | Timeline and consent | Owner confirmed the gate in chat 2026-11-18; no GitHub answer to Clay's proposal exists | Proposal posted to the owner (#450, 17:00:32, "What do you think?") before the build | Low | L1 |
| C-010 | Code and failure-mode surface | Costs about 30 functions in `github.py`, three reads per candidate; keeps them | PR 686 removes them and their failure reasons; fewer reasons to skip a correct issue | Low | L2 |
| C-011 | Live-run status | Neither ran live (conceded) | Never ran live, so removing an untested protection | Low | L1 |

## Contradictions

| # | Point of conflict | Variant A position | Variant B position | Impact | Level |
|---|---|---|---|---|---|
| X-001 | Meaning of R35 and R36 (REQ lines 61-62) | R36 withdrew only the void-after-change rule R31; the approval stays (REQ line 62) | R36 and R35 show the owner moving toward fewer gates | Medium | L2 |
| X-002 | Same trust set, opposite inference (C-002 sharpened) | Same set means the gate protects against accident and stale content | Same set means the gate protects against nothing | Medium | L3 |

## Unique Contributions

| # | Variant | Contribution | Value |
|---|---|---|---|
| U-001 | A | `/sc:issue --claim` itself assigns, so assignment cannot mean "go" | High |
| U-002 | A | `master` unprotected, rulesets 0 (read 2026-11-20) | High |
| U-003 | A | Edit-after-approval content binding (`unchanged_since`) | High |
| U-004 | A | Closed ship gate: only Pipeline None launches today (REQ R33) | Medium |
| U-005 | A | FULL-REPORT mis-reads R36 as withdrawing the Status gate | Low |
| U-006 | B | #450 comment timing and addressee | Medium |
| U-007 | B | `plan_check` and `hold:backlog` as new capabilities (fill a gap) | High |
| U-008 | B | Fewer failure reasons (`events_incomplete`, `approval_before_trigger`, `project_mismatch`, `approvers_invalid`) | Low |

## Shared Assumptions

| A-NNN | Assumption | Source agreement | Classification | Impact | Level |
|---|---|---|---|---|---|
| A-001 | The trigger rule can be judged independently of what the started work may do (merge, push, guard); both papers argue it, but the consequence profile (C-007) depends on topics D05 and D06 | Both papers accept that the watcher or orchestrator starts a worker | UNSTATED | High: a guarded, claim-only flow makes gate removal cheap; a merging flow makes it costly | L3 |
| A-002 | The `Approved` issue field (R35) can be read as a timeline event by the watcher and gives the same guarantees as the label | OURS builds on it; CLAY never tests it | UNSTATED (R35 is "built" but its GitHub timeline events were read through `_assumed_shape` fixtures, UNVERIFIED live) | Medium | L3 |
| A-003 | The window between assignment and the poll's wake is short enough that issue content cannot change materially | Both rely on the live re-read before wake | UNSTATED | Medium | L3 |
| A-004 | Each person's watcher acts only for its own login; the issue is assigned to that login | Both quote `is_intended_owner` | STATED in both (promoted only as a guard-condition check, no debate needed beyond ACCEPT) | Low | L3 |

## Summary
- Total structural differences: 2
- Total content differences: 11
- Total contradictions: 2
- Total unique contributions: 8
- Total shared assumptions surfaced: 4 (UNSTATED: 3, STATED: 1, CONTRADICTED: 0)
- total_diff_points (S + C + X + A) = 19
- Highest-severity items: C-001, C-006, C-007, A-001
- Taxonomy coverage: L1 (S-001, C-009, C-011), L2 (S-002, C-001, C-002, C-003, C-005, C-008, C-010, X-001), L3 (C-004, C-006, C-007, X-002, A-001 to A-004)

# Spec panel follow-up candidates (Medium and Note findings not fixed in the review loop)

Spec: /home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/spec/SPEC.md. Review rule: a Medium finding is a warning; it never fails a review, never triggers a fix pass and never goes into a reviser brief. Both reviews ran unattended, so no person was asked whether to open issues; nothing was filed. Reports: review 1 /home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/spec/panel/review-1/spec-panel-report.md (verdict FAIL, 1 blocking F1, fixed; 13 Medium; 11 Note), review 2 /home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/spec/panel/review-2/spec-panel-report.md (verdict PASS scoped, 0 blocking; 5 Medium; 4 Note). The Note findings (N1 to N15) are wording points and are listed only in the two reports.

The first four rows below touch the owner's five rules and should be fixed before any build starts. "Suggested fix" is the coordinator's reading, not a panel verdict.

## Review 1 Medium findings (spec as of candidate-1)
| ID | Section | Finding | Suggested fix | Touches owner rules |
|---|---|---|---|---|
| F4 | rules, SEC-15 | "A typed go precedes every push" is not reconciled with the fix-round pushes of `/sc:pr-submit --monitor 3` or with the Full Submit per-issue go | State which pushes the go covers (the first push and PR) and that fix-round pushes by the same session fall under the same go, or require a go per round | yes (typed go) |
| F6 | revert, L-07, FR-29 | The revert restores old contract duties (lines 296-300) that read approval from GitHub and mirror the label and Status. L-07 edits lines 298 and 300 with no requirement saying how. A second adoption record exists beside FR-29's | Add a requirement that names the edited text and the single adoption record; choose one of the two records | yes (approvals in chat) |
| F10 | S17 | The S17 pass list needs the trigger-label check green while the label step is read-only. One go is said to cover label creation for later repos | Split the pass list: read-only check first; label creation as a separate go | yes (poll writes nothing) |
| F14 | FR-07 | The fixture line FR-07 cites also lists `pr.merge`, which SEC-06 says to refuse | Cite the fixture without that entry or require the fixture to drop it | yes (no standing merge grant) |
| F2 | FR-52 | Says the Pipeline field is unread, but planb reads it and skips on `level_gated` | Reword to "ignored for launch level while the gate is closed; read only to skip" | no |
| F3 | NFR-02, interface row 6 | No requirement says which session performs the merge or writes the go entry; NFR-02 and the interface row disagree on the writer | Name the session (the coordinator, after the person's typed go) in one requirement; fix both places | related (merge go) |
| F5 | FR-34, FR-27 | FR-34 restarts a coordinator without the autostart consent FR-27 requires for any script start | Make the restart conditional on the same consent | no |
| F7 | S15a, S11 | S15a (wake pull) has no precondition on S11, the stage that writes wakes | Add the precondition | no |
| F8 | section 8, FR-75 to FR-78 | The process package has no stage row, rollback or owner gate | Add a stage row (S0 neighbour) with owner gate and rollback | no |
| F9 | section 2, S5 | Section 2 is titled "Binding decisions" but says all are recommendations. S5 treats OA-9 as settled though the cited verdict says the owner decides | Retitle or reword; mark OA-9 owner-confirmed in S5 | no |
| F11 | cap | The cap is unclear in three ways: "key default 3, first build enforces 1", what 0 means, and the phase that frees a store entry | Define all three in one requirement with a test | no |
| F12 | acceptance column | About 25 rows have a bare `NEW` as the acceptance check | Replace each with a named check | no |
| F13 | S17, SEC | Rotating the exposed Orca token has no stage and is not a precondition of S17 | Add an owner action and a precondition | safety |

## Review 2 Medium findings (changed surface of candidate-2)
| ID | Section | Finding | Status |
|---|---|---|---|
| G1 | X-1, OD-11 | They still say three standing grants while SEC-07 and OA-11 say four | Touch-up requested after the PASS (not re-reviewed) |
| G2 | FR-83, S9, S14 | FR-83's refusal without a grant has no stage that builds or tests it; S9 lands the verb but the grants machinery arrives at S14 | Open |
| G3 | FR-82 | "the only code that may write" reads repo-wide; the merge verb and the claim session also write (the check column scopes it correctly) | Open |
| G4 | 8.3, section 10 | If PR 682 stands, the owner must name a home for `complete.py`; no owner-action row records it and the "unchanged" scan test cannot pass there | Open |
| G5 | 23 hunks | The reviser narrowed three stage or row texts and one pointer | Restoration requested after the PASS (not re-reviewed) |

## Third pass and review 3 (2026-11-20, owner said "yes" to fixing the four rule-touching findings)
Fixed in SPEC.md and confirmed resolved by review 3: F4 (new SEC-22, decided by debate Q04), F6 (new FR-84), F10 (per-repo chat OK for label creation; X-18), F14 (FR-07), plus G1 and G5. Review 3 (the last allowed review; report /home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/spec/panel/review-3/spec-panel-report.md): verdict PASS (scoped), 0 blocking, 8 Medium, 5 Note. Process note from the reviewer: the third pass edited text that no blocking finding named (F4, F6, F10 and F14 were Medium) and added FR-84 and SEC-22; this was done at the owner's request.

| ID | Section | Finding (review 3, Medium; not fixed) |
|---|---|---|
| H1 | FR-32, SEC-22 | The run line is the go for the first push, but nothing ties it to FR-32's duty to show the worker commits first |
| H2 | SEC-22 | The fence and count bound miss CI, sync and merge-commit pushes, so a run can make 4 pushes against a stated bound of 3 |
| H3 | SEC-22, S14 | The five new checks have no stage and no component that could refuse a push made by `/sc:pr-submit` |
| H4 | 3.1, Q04, SEC-22 | The Full Submit field is stated as a go without condition; only SEC-15 says it waits on the owner |
| H5 | FR-82, S9 | The label-create step has no named entry point, and nothing at S9 can read the owner's OK |
| H6 | 8.2 S17 | Section 8.2 says S17 excludes label writes, but the S17 pass list includes the throwaway repo's label created on the owner's OK |
| H7 | FR-07 | The new fixture check needs a grants loader that does not exist at S11 |
| H8 | FR-29, FR-84 | The "only the creator may start a worker" rule and the replay case of a wake are not carried over |

Open from earlier: F2, F3, F5, F7, F8, F9, F11, F12, F13 (review 1) and G2, G3, G4 (review 2). The four rows H1 to H4 touch the typed-go rule and should be fixed before any build.

## Coordinator note
The spec is not a plan of record until the owner confirms the owner actions in section 10 of the spec. No fourth review is allowed by the review rule; any further fix is a spec edit by the owner's choice and carries no new PASS.

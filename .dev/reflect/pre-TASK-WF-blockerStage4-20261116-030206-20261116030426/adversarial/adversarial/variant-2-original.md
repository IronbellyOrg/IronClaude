persona: qa
model_class: haiku
model: claude-gw-tier2
model_observed: reviewer self-reported "GPT-5" (identity mismatch suspected; the class was passed explicitly on the Agent call)

<!-- Saved by the orchestrator from the reviewer's final message. Text, line numbers and quotes unchanged; markdown links and absolute path prefixes were shortened to repo-relative paths (P4 = .dev/tasks/to-do/TASK-WF-blockerStage4-20261116-030206/TASK-WF-blockerStage4-20261116-030206.md). The reviewer used the deviation-table format instead of the F-line format; each row below is one finding, numbered D1 to D4. -->

# Reflect Reviewer — Deviation Findings

**Reviewer persona**: qa
**Grounding root**: repository root
**Diff scope**: Explicit changeset: stage 4 plan, Tasks 1–7, compared with the stage 4 request and base Tasks 41–46
**Total deviations**: 4

## Verdict

The plan needs revision before execution: its entry check requires evidence that the preceding package does not produce, and the package was generated without the required recorded go.

## Deviations

D1 | Drift | MAJOR; blocking true | Location: P4:20 | Who: plan generator and owner. Wrong result: a prerequisite for generating this package has been postponed until execution. The request says "Generate it only after" the preceding stage, audit window and recorded owner go; the plan instead says "It runs only after". The ledger has no stage 3 package or stage 4 go recorded. | Evidence: .dev/tasks/to-do/TASK-WF-blockerStage4-20261116-030206/source.md:3 "Generate it only after the stage 3 package is done"; .dev/tasks/to-do/BLOCKER-CLASSIFICATION-PROGRAM-20261115/stage-requests/README.md:20 stage 3 and stage 4 package/go cells are empty. | Table severity: MEDIUM

D2 | Drift | MAJOR; blocking true | Location: P4:37 | Who: stage 4 executor. Wrong result: Task 1 rejects the stage 3 summary produced according to its own contract. It requires that summary to state an audit window has already passed. Stage 3 produces the summary before that window and explicitly says the window runs afterward. Neither package assigns a later update that supplies the statement this check demands. The audit may genuinely pass while this acceptance line still fails. | Evidence: P4:37 "exists and states that one audit window has passed with no revert trigger tripped"; .dev/tasks/to-do/TASK-WF-blockerStage3-20261116-030158/TASK-WF-blockerStage3-20261116-030158.md:158 "State that the audit window runs after this package"; same file:162 "no revert trigger can be judged until the audit window has run". | Table severity: MEDIUM

D3 | Drift | MINOR; blocking false | Location: P4:53-55 | Who: Task 2 executor and reviewer. Wrong result: the rule-prompt acceptance checks do not verify the requested preservation of their cap sentences by content. They check digests, registry states, the pointer-only row, named tests and zero-finding wording, but provide no cap-content pin. The global no-cap-change constraint remains, so this is incomplete checking rather than an instruction to change the cap. | Evidence: .dev/tasks/to-do/TASK-WF-blockerStage4-20261116-030206/source.md:12 "the cap sentences kept by content"; P4:55 "the zero-finding and \"no minimum count\" sentences still exist". | Table severity: LOW

D4 | Drift | MINOR; blocking false | Location: artifacts/coverage-matrix.yaml:10-12 | Who: coverage reviewer. Wrong result: a requirement-bearing sentence is absent from both parsed and inferred coverage. INF-002 quotes the reuse instruction but stops before the separate package-id evidence instruction; no other row includes it. The plan itself implements that instruction, so this is a matrix omission, not missing implementation scope. | Evidence: .dev/tasks/to-do/TASK-WF-blockerStage4-20261116-030206/source.md:7 "Earlier stages' evidence is read by package id."; P4:19 "Evidence of earlier stages is read from their packages by package id". | Table severity: LOW

## Adherence summary

- Spec units audited: 17 — the matrix's 16 inferred units plus the omitted package-id evidence instruction.
- Fully adherent across plan and coverage evidence: 14.
- Authorized expansion: 0 | Necessary deviation: 0 | Drift: 4 findings affecting 3 units | Regression: 0.
- Findings D1 and D2 concern the same entry-prerequisite unit. This is a pre-execution review; no runtime regression is asserted.

## Notes

### Base Tasks 41–46 comparison

Compared the complete base task block (OLD:486-552) against the current task bodies.

- 41 -> 1: Removed the cross-package Task 40 dependency; added owner-go and audit-evidence acceptance lines; changed five digest templates to four plus merge-only analysis; added the 11-row invariant; renamed the scan reference to the stage 3 scan. Requested changes are preserved. The new audit-evidence line has Finding D2.
- 42 -> 2: Only task/dependency numbering changed. The additional cap-preservation acceptance requested for this stage is absent: Finding D3.
- 43 -> 3: Removed the cross-package dependency and changed "allow-list of Task 40" to "allow-list of the stage 3 scan test". Remaining instructions and acceptance lines are unchanged.
- 44 -> 4: Only task/dependency numbering changed; consumer-line and cap requirements remain.
- 45 -> 5: Renumbered task/dependency and added the requested existing-example-path preservation acceptance line. Remaining text is unchanged.
- 46 -> 6: Renumbered dependencies; moved canonical registration and path-only allow-list addition before copying; added recopy if the registry changes; added the merge-rule scan to the combined acceptance run and named both scan routes. These changes follow the request and earlier review.
- Task 7: Adds the requested owner summary, carrier states, tests, results and per-row revert commands. It also requests observed pass counts and open items. Its wording does not require the audit-window sentence to be the final sentence, as the request specifies; this is a minor ordering ambiguity, not a blocking missing result.

### Earlier stage-4 findings checked

- F3 / F9: Resolved prospectively by the registration -> allow-list -> copy -> combined-test order in P4:99-102.
- F4: Resolved by four digest templates, merge-only analysis and exactly 11 digest rows in P4:33-39.
- F5 / F12: Stage 4 preserves the pointer-only treatment and existing example path in P4:50 and P4:87. Actual T3 implementation remains an earlier-stage prerequisite, not verified completed behavior.
- F6: The endpoint rule is present in P4:24. No later task here falsifies an earlier task's stated acceptance line.
- F13: Task 6 explicitly prevents merge-rule phrases in the new allow-list entry. The earlier canonical-rule wording repair remains an upstream prerequisite.

No files changed and no tests were run. Execution results and completed upstream-stage repairs were not available for verification.

## Self-report
confidence: 0.91
reviewer_model_self_report: GPT-5

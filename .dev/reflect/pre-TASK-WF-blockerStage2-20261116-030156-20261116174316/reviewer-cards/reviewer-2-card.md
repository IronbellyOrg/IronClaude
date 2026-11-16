# Reviewer card 2 (persona qa, model class haiku) - persisted by the orchestrator (the "Checked, no defect" bullets are condensed; every finding is unchanged)

reviewer: 2
persona: qa
model_class: haiku

## Findings

id: R2-1
severity: blocking
claim: Task 8 cannot unambiguously associate safety confirmations with findings across multiple runs. Its confirmation file contains only row ids, but the ledger contract makes those ids run-scoped.
citations: .dev/tasks/to-do/TASK-WF-blockerStage2-20261116-030156/TASK-WF-blockerStage2-20261116-030156.md:138; .dev/tasks/to-do/TASK-WF-blockerStage2-20261116-030156/TASK-WF-blockerStage2-20261116-030156.md:141; .dev/tasks/to-do/BLOCKER-CLASSIFICATION-PROGRAM-20261115/02-brainstorm/merged-requirements.md:352
quote: "one row id per line that a later review or the owner confirmed as a safety risk"; "`FU-000001` upward, run-scoped, never reassigned or recycled"
consequence: Two valid runs can both contain FU-000001. A confirmation for that id cannot identify which run's finding was confirmed; matching all occurrences overcounts, while choosing one can miss the confirmed unrouted risk. The required safety-miss result therefore cannot be reliably computed for the multi-run input Task 8 specifies. The fixture acceptance does not require a repeated-id case across runs.
confirms_t1: none
confidence: 0.99

id: R2-2
severity: blocking
claim: Task 7 requires the answering agents to see only the blind table, excluding the code-supplied context needed for the intended classifier evaluation. Running the supplier afterwards cannot make previously recorded, text-only answers into code-informed answers.
citations: .dev/tasks/to-do/TASK-WF-blockerStage2-20261116-030156/TASK-WF-blockerStage2-20261116-030156.md:28; .dev/tasks/to-do/TASK-WF-blockerStage2-20261116-030156/TASK-WF-blockerStage2-20261116-030156.md:126; .dev/tasks/to-do/TASK-WF-blockerStage2-20261116-030156/TASK-WF-blockerStage2-20261116-030156.md:130; .dev/tasks/to-do/BLOCKER-CLASSIFICATION-PROGRAM-20261115/04-historical/blind-table-1.md:3-5; .dev/tasks/to-do/BLOCKER-CLASSIFICATION-PROGRAM-20261115/02-brainstorm/merged-requirements.md:501; .dev/tasks/to-do/BLOCKER-CLASSIFICATION-PROGRAM-20261115/02-brainstorm/merged-requirements.md:512-516
quote: "The agents see only the blind table"; "they were given the blind table only"; "| ID | Category | Description brief | Context |"; "code does every exact check first ... and passes the result in as state"
consequence: For rows where the supplier can provide a required-item list, constraint lines or verified evidence, the agents still cannot receive those inputs under the stated acceptance criterion. The evaluation would repeat the text-only limitation the plan expressly identifies, rather than measure the code-informed classifier. Blinding labels and consensus is compatible with supplying evidence, but the plan does not permit that enriched input packet.
confirms_t1: none
confidence: 0.94

id: R2-3
severity: minor
claim: The supplied coverage matrix omits requirement-bearing spans rather than accounting for the whole source body. This is a traceability defect; several omitted obligations are nevertheless present in the plan.
citations: reviewer-briefs/reviewer-2.md:175-210; source.md:3; source.md:11-14; source.md:28-30; source.md:36-37; source.md:53
quote: "Generate it only after ... has been read and the owner has said go in chat"; "split by deliverable kind, the count of rows that had each code-supplied input, and the limits"; "Registry counts are not touched by this package."; "the tier comes from `refs/scale-map.md`"
consequence: The matrix needs explicit accounting for these unrepresented clauses: the source line 3 pre-generation prerequisite; the line 11 minimum of five observed runs produced outside this package; the line 13 population membership, independence from question authorship, deliverable-kind splits, input-availability counts and limits; the line 14 seven exit measurements, classifier headline, actual script output, allowed zero-run result and chat-only owner approval (INF-007 to INF-009 primarily cover file creation and fixture testing); the line 28 offer ownership and recorded hash comparisons in Tasks 1, 3 and 8; the line 30 unchanged registry counts; the lines 36-37 command-ownership split and safety-route record-without-waiting behavior; the line 53 scale-map source of tier translation. This omission alone does not establish that those plan behaviors are missing.
confirms_t1: none
confidence: 0.97

## Refuted T1 findings
- F5: Not confirmed. The body describes the meaning of the sentence, not mandatory literal wording. The acceptance explicitly says "the one sentence that says there is no sweep avoids the word." Both requirements can be satisfied together (plan:88-92).
- F7: Not confirmed as an execution-blocking contradiction. Revision 2 explicitly moves the carrier and drops the earlier halt-offer instructions; those are identifiable amendments, not two equally current instructions (source.md:27-29).
- F3: The narrower explicit import check is confirmed, but the claimed late-failure sequence is overstated: Task 2 already checks that command help lists `classify`, before the carrier edits. Retained as an entry-check weakness below (plan:39-44,59).
- F4: The missing explicit producer-to-parser fixture is confirmed as a coverage weakness, but "every real run becoming partial" is not established; Task 2 leaves implementation choices open (plan:56-62,88).

## Checked, no defect (condensed)
- Read all eight task bodies and acceptance lists against the complete source request including Revision 2.
- Task 1: explicit import check before edits, stops for the owner's Ruling; absent stage 1 modules are dependencies, not a stage 2 duty; record-only defaults, unchanged ledger bytes, no Note processing, corrected-row behaviour, skipped-kind counts, gate-equivalence test.
- Task 3: one read-only call per carrier file, no promotion or ledger writing, no added question, unchanged archive outcome, protected QA hashes, byte-equal plugin twins.
- Task 5: exactly three keys, incomplete maps to partial, producer named, unattended no-network/no-question test; absence of live emitters is disclosed.
- Task 6: testable mutation checks for both reviewer fields, paragraph placement, promotion flags, questions; legacy-text pin has a state-based endpoint.
- Task 7: names all three populations and sources, three agents x three replicates, per-agent figures, no pooling, agreement, kappa, confusion matrix, blocker recall, flip rate, kind splits, input counts, UNSET/NA handling, no authority.
- Task 8: all seven source-line-14 measurements named; judge/version splits, unavailable counts, exclusion of reviewer-label agreement, writer-generated fixtures, failure cases, actual output over available runs, stated zero-run result, wiring headlines, limits, protected-file checks, chat-only approval sentence.
- No later task found to invalidate an earlier acceptance line without an endpoint.
- These conclusions concern the written plan; nothing was run.

## Follow-up candidates
- Entry-check completeness (F3): the import acceptance names only three modules; command registration is checked in Task 2 instead of before the first edit; scale-map and registry are not checked (plan:20,39-44,59,113).
- Producer/parser integration (F4): require one fixture derived from the actual edited reviewer output format to pass through `write` (plan:56-62,88-91,113-118).
- Summary arithmetic coverage: the mandatory fixture cases do not assert nonzero offers, consumer-unknown numerator/denominator, per-run volumes or empty-run arithmetic (plan:138-142).
- No commands or tests were run; stage 0/1 execution evidence and future stage 2 outputs do not establish runtime correctness.

verdict: NEEDS-REVISION
self_confidence: 0.95

## Calibration (blind, confidence-calibrator, class opus; calibrator_diversity: degraded)
dims: citation 0.90, coverage 0.84, clarity 0.88, risk 0.85, actionability 0.76
C: 0.85
per_finding: R2-1=0.88, R2-2=0.74, R2-3=0.82

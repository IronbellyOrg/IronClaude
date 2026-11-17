persona: qa
model_class: haiku
reviewer_model_self_report: unavailable (exact runtime model identifier not exposed)
plan: .dev/tasks/to-do/TASK-WF-blockerStage2-20261116-030156/TASK-WF-blockerStage2-20261116-030156.md
path-note: citation paths below were written by the reviewer as absolute paths under /home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel/; they are shortened to repository-relative paths here, nothing else is changed. `plan` = the path above; `spec` = .dev/tasks/to-do/BLOCKER-CLASSIFICATION-PROGRAM-20261115/02-brainstorm/merged-requirements.md

# Reviewer 2 card (qa)

## Findings

### R2-1
severity: blocking
claim: Task 4 does not connect recorded classifier S answers to the live safety route. It requires a safety call over the ledger and separately permits classification with recorded answers, but never requires passing those answers to safety or routing S = Y/U before the gate passes.
citations: plan:57; plan:64; plan:95; plan:99; spec:658
quote: "then runs `superclaude review follow-ups safety` over the ledger without `--unattended`"; "One added line says the classifier is called in shadow mode only when the run owner holds a recorded judge-answers file"; "when the GR1 scan hits a non-blocking row, or a judge answers S = Y or S = U".
consequence: A non-blocking finding with no vocabulary hit but a recorded S = Y/U can remain an ordinary follow-up. The required person prompt is then missed, despite GR12 being live during shadow mode. The specified command test exercises vocabulary hits, and Task 4's acceptance checks the attended mode, not this classifier-to-safety connection; both can pass with the connection absent.
fix direction: Require the recorded answers to reach `follow-ups safety` before gate passage, and add a no-vocabulary-hit fixture for each of S = Y and S = U.

### R2-2
severity: medium
claim: Task 7's enriched-input fix does not explicitly preserve the complete supplier result: its enumerated packet and reporting counts omit decision-basis excerpts and the M `absent-by-name` precheck. In particular, D can appear in the returned question ids without its required excerpts being explicitly required in the agent packet; the decision-basis availability count required by the spec is also missing.
citations: plan:135; plan:139; plan:142; spec:512; spec:516; spec:615
quote: "the count of rows that had each code-supplied input (required-item list, constraint lines, verified evidence excerpt)"; "each input file lists, for every row, the question ids"; "report how many table rows had a decision basis."
consequence: An implementation can satisfy the enumerated packet/count checks while omitting D's supporting material and its availability figure. That weakens the evaluation and leaves the owner unable to distinguish missing decision bases from judge disagreement. The broader phrase "write what it returned" permits a complete implementation, so this is an acceptance-contract weakness rather than an unavoidable failure.
fix direction: Require serialization and agent delivery of the complete supplier result, including the M precheck and D excerpts, with D availability counts and a positive-D packet fixture.

### R2-3
severity: medium
claim: Task 7 names agreement, Cohen's kappa, recall and flip rate but does not define how SHOW_USER enters the binary comparison with panel blockers, or whether a flip means any verdict change or a blocker-call change. The numerical fixture is required to cover these metrics without fixing those choices.
citations: plan:135; plan:138; plan:140; .dev/tasks/to-do/BLOCKER-CLASSIFICATION-PROGRAM-20261115/08-test/results.md:5; results.md:7; results.md:13
quote: "covering agreement, kappa, recall and flip rate on a small fixture"; "Accuracy (SHOW_USER = not blocker)"; "Accuracy (SHOW_USER = blocker)"; "Findings whose blocker call flips between runs".
consequence: Different implementations can produce materially different, passing headline figures from the same answers. The existing run-1 results illustrate the size of the difference: agreement is 59.1% or 31.1%, and recall is 91.5% or 100%, depending on SHOW_USER treatment. Without a stated convention, comparison with the earlier experiment is unreliable.
fix direction: Define the binary projection or report both SHOW_USER treatments, define the flip event and denominator, and pin exact expected values on a fixture containing SHOW_USER.

### R2-4
severity: medium
claim: Task 8 does not define whether a supplied folder without a ledger counts as an observed shadow run, an excluded input, or a capture failure. Its acceptance distinguishes zero runs and an existing empty ledger, but does not assign an outcome to a supplied folder whose ledger is absent.
citations: plan:30; plan:148; plan:151; plan:152
quote: "reads a list of shadow-run folders and their follow-up ledgers"; "the count of runs observed"; "zero runs and a ledger with no non-blocking rows".
consequence: Counting input folders and counting readable ledgers can yield different observation totals and capture-failure totals. The owner's five-run entry evidence is therefore not reproducible for this case. This does not invalidate the expressly allowed zero-run summary or the stated limitation that implement runs currently produce no ledger.
fix direction: Define observed runs using validated, distinct run ids, state the treatment of missing ledgers, and pin the resulting counts in a supplied-folder-without-ledger fixture.

## Earlier findings
- MB-1: fixed. Run-qualified matching is explicit at plan:148; acceptance at plan:151 requires two runs sharing `FU-000001`, exactly one counted miss, bare-id rejection and unmatched-confirmation handling. That check can fail an implementation that matches ids across runs.
- MB-2: partly fixed. Supplier-first ordering and delivery of M/C/E inputs are explicit at plan:135, with packet and absent-input acceptance at plan:139 and plan:142; the complete supplier-packet contract remains under-specified as described in R2-2.
- MB-3: fixed. Producer output is required and tested at plan:57 and plan:64; WC-4 consumes it at plan:110; acceptance at plan:115 explicitly fails removal of the mapping and tests the unattended producer. R2-1 concerns a separate missing path into that producer.
- MB-4: fixed. The four active prompts, analyst table and both dispatch-step additions are specified at plan:95; acceptance at plan:98 and mutation-sensitive tests at plan:122-125 cover removal of either field or either dispatch line.

## Checked, no defect
- Stage 0 artifact names and producers match. The sample is produced by Task 2, held-out ids by Task 5, fresh findings and sample consensus by Task 6, and input availability by Task 8 (.dev/tasks/to-do/TASK-WF-blockerStage0-20261116-021044/TASK-WF-blockerStage0-20261116-021044.md:44,82,96,116; plan:40,135). These are future prerequisites, not artifacts falsely claimed to exist now.
- Safety-miss definition matches the stage 0 draft. Later confirmation and absence of GR12 routing are required; Task 8 does not pretend ledger vocabulary alone establishes a confirmed miss (stage 0 plan:130; plan:29,148,151).
- Empty confirmation files cannot establish zero misses. The review statement, run-qualified entries, missing-review cases and reviewed-no-misses case have distinct acceptance outcomes. Empty classifier populations, missing panel blockers and one-class kappa also have explicit non-computable outcomes (plan:135,140,148,151).
- M13 handling in the shadow summary is explicit. Agreement is split by judge id and version, unavailable rows are counted, and reviewer-label judges contribute no agreement evidence (plan:148,151).
- The two manual coverage dispositions are justified. INF-009 is satisfied by the retired-carrier constraint; INF-022 is satisfied by sticky incomplete capture and its later-write test (plan:22,57,66; source.md:89).
- The revised carrier limits are deliberate, not additional defects. Record-and-print-only implement behavior, no tech-research offer, excluded fidelity/anti-omission gates, no live worker-contract emitter, and observation runs supplied over time are stated limitations. The plan does not claim completing its eight tasks establishes the five-run entry minimum (plan:20-26,95,110,148,152).
- Pins and task-local acceptance lifetimes are sound within this package. Sweep insertion is anchored outside the FINAL fence and before archive step 6; mutation checks protect that placement. The legacy-style assertion has a registry-state endpoint. No later task in this package was found to invalidate an earlier acceptance condition, and no operational command uses an absolute checkout path or a to-do package prefix (plan:31,78,83-89,122-127,140,151,153).

verdict: NEEDS-REVISION (1 blocking)

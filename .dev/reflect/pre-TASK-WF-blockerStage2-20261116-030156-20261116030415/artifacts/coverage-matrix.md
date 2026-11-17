# Coverage matrix (Step 1B.0 / 1B.0 matching)

parsed_count: 0   inferred_count: 16   inferred_invalid_dropped: 0
coverage_pct (parsed-only): null   coverage_pct_union: 0.75   (matched 12 of 16)
coverage_degraded: parsed-sparse
input_tree_sha256: c870fc18b1feb5b778fd46f6ba15998652a19c6f35bded479e324b4df97e6587   file_count: 9

| id | spec line | source | containment match | best task ratio | constraints ratio | quote |
|---|---|---|---|---|---|---|
| INF-001 | source.md:3 | inferred | Task 1 | 0.8 (Task 1) | 0.867 | Generate it only after the stage 1 package's `./artifacts/stage1-summary-for-owner.md` has been read and the owner has said go in chat |
| INF-002 | source.md:3 | inferred | Task 2 | 1.0 (Task 2) | 1.0 | The old definition still decides every gate outcome in this stage. |
| INF-003 | source.md:7 | inferred | none | 0.28 (Task 2) | 0.56 | Reuse Tasks 26 to 30 of the revised 46-task plan `TASK-WF-loosenBlockerRev-20261115-210254` (Phase 3, stage 2; found by that folder name under `.dev/tasks/to-do/`), renumbered 1 onward, with its `## Constraints` (stage 2 parts). |
| INF-004 | source.md:7 | inferred | Task 6 | 1.0 (Task 6) | 1.0 | Stage 0 and stage 1 evidence is read by package id. |
| INF-005 | source.md:11 | inferred | Task 2 | 0.792 (Task 2) | 0.958 | State this is stage 2: the sweep only records (`promote` off), the classifier has no authority, the one sweep call and one offer sit in the task skill's "Post-Completion Validation (Final Phase Only)", tech-research gets neither. |
| INF-006 | source.md:11 | inferred | Task 7 | 0.696 (Task 7) | 1.0 | Stage 3 starts only after the owner reads this package's summary and says go; the stage 3 entry also needs at least 5 observed shadow runs, which the owner or operator produces over time and no task here can produce. |
| INF-007 | source.md:12 | inferred | Task 2 | 0.684 (Task 2) | 0.684 | The halt-offer text goes beside each cap sentence in the task skill and in tech-research only; the two `rf-qa.md` cap sites are not touched here (stage 3). |
| INF-008 | source.md:12 | inferred | Task 2 | 0.842 (Task 2) | 0.684 | Acceptance quotes the cap sentence "After 2 fix cycles (3 reviews), HALT and escalate to the user with the open blocking findings" and names no line numbers. |
| INF-009 | source.md:13 | inferred | Task 6 | 0.944 (Task 6) | 0.389 | Run the classifier of the stage 1 modules (`classify` command, `classifier_inputs.py` supplier, the question set v1, recorded fixture answers produced by three blind agents that did not write the questions, no Jev) on the three sets built in stage 0: the fresh-findings set, the held-out half of the 318 rows, and the reviewer-called-minor set |
| INF-010 | source.md:13 | inferred | Task 6 | 1.0 (Task 6) | 0.414 | Write `./artifacts/stage2-classifier-eval.md`: agreement with the panel consensus, Cohen's kappa, confusion matrix, recall on the panel's blockers, flip rate over three replicates, split by deliverable kind, the count of rows that had each code-supplied input, and the limits. |
| INF-011 | source.md:13 | inferred | Task 6 | 1.0 (Task 6) | 0.75 | State that it is not an authority test (OD4). |
| INF-012 | source.md:14 | inferred | Task 7 | 1.0 (Task 7) | 0.565 | Write `./artifacts/shadow_summary.py` (run with `uv run python`) that reads a list of shadow-run folders and their `qa/follow-ups.md` ledgers and prints the stage 2 exit numbers the spec defines (ledger volume per run, share of `consumer-unknown` rows, offers made and answered, shadow agreement, count of runs observed, count of safety misses by the stage 0 definition, capture failures), with a test over fixture ledgers. |
| INF-013 | source.md:14 | inferred | Task 7 | 1.0 (Task 7) | 0.593 | Then write `./artifacts/stage2-summary-for-owner.md`: the classifier evaluation headline, the script's output over the shadow runs that exist so far (zero is a valid and stated result), and the sentence that the owner's go for stage 3 is given in chat and not by this file. |
| INF-014 | source.md:15 | inferred | none | 0.333 (Task 1) | 0.778 | that a later task of the same package makes false get an end point. |
| INF-015 | source.md:19 | inferred | none | 0.312 (Task 2) | 0.312 | No edit of `pragmatic.md`, `rf-qa.md`, `rf-qa-qualitative.md`, `rf-analyst.md`, templates, rule prompts, builders or researchers, and no promotion of swept rows to Blocking. |
| INF-016 | source.md:19 | inferred | none | 0.333 (Task 3) | 1.0 | Do not change `sc-implement-protocol/refs/qa.md`, the own-scale primitives, the cap of 2 fix cycles or the 35 percent target. No Jev call, key or account. |

# Stage 2 plan request: shadow beside the old rule (issue #552)

Third of five plan packages (see `stage-requests/README.md`). Generate it only after the stage 1 package's `./artifacts/stage1-summary-for-owner.md` has been read and the owner has said go in chat; the stage ledger rows for stages 0 and 1 hold their package ids. The old definition still decides every gate outcome in this stage.

## Base text

Reuse Tasks 26 to 30 of the revised 46-task plan `TASK-WF-loosenBlockerRev-20261115-210254` (Phase 3, stage 2; found by that folder name under `.dev/tasks/to-do/`), renumbered 1 onward, with its `## Constraints` (stage 2 parts). Stage 0 and stage 1 evidence is read by package id.

## Changes to apply

- **Constraints.** State this is stage 2: the sweep only records (`promote` off), the classifier has no authority, the one sweep call and one offer sit in the task skill's "Post-Completion Validation (Final Phase Only)", tech-research gets neither. Stage 3 starts only after the owner reads this package's summary and says go; the stage 3 entry also needs at least 5 observed shadow runs, which the owner or operator produces over time and no task here can produce.
- **Cap-site offers (base Tasks 27 and 28).** The halt-offer text goes beside each cap sentence in the task skill and in tech-research only; the two `rf-qa.md` cap sites are not touched here (stage 3). Acceptance quotes the cap sentence "After 2 fix cycles (3 reviews), HALT and escalate to the user with the open blocking findings" and names no line numbers.
- **New task: classifier evaluation on the stage 0 populations (finding F7).** Run the classifier of the stage 1 modules (`classify` command, `classifier_inputs.py` supplier, the question set v1, recorded fixture answers produced by three blind agents that did not write the questions, no Jev) on the three sets built in stage 0: the fresh-findings set, the held-out half of the 318 rows, and the reviewer-called-minor set (read by the stage 0 package's id, its `./artifacts/fresh-findings.md`, `stage0-heldout-ids.json`, `stage0b-sample.md`). Write `./artifacts/stage2-classifier-eval.md`: agreement with the panel consensus, Cohen's kappa, confusion matrix, recall on the panel's blockers, flip rate over three replicates, split by deliverable kind, the count of rows that had each code-supplied input, and the limits. State that it is not an authority test (OD4).
- **New task: shadow summary script and stage 2 exit summary (finding F8).** Write `./artifacts/shadow_summary.py` (run with `uv run python`) that reads a list of shadow-run folders and their `qa/follow-ups.md` ledgers and prints the stage 2 exit numbers the spec defines (ledger volume per run, share of `consumer-unknown` rows, offers made and answered, shadow agreement, count of runs observed, count of safety misses by the stage 0 definition, capture failures), with a test over fixture ledgers. Then write `./artifacts/stage2-summary-for-owner.md`: the classifier evaluation headline, the script's output over the shadow runs that exist so far (zero is a valid and stated result), and the sentence that the owner's go for stage 3 is given in chat and not by this file.
- **Acceptance lines inside this package** that a later task of the same package makes false get an end point.

## Not to be done by the plan

No edit of `pragmatic.md`, `rf-qa.md`, `rf-qa-qualitative.md`, `rf-analyst.md`, templates, rule prompts, builders or researchers, and no promotion of swept rows to Blocking. Do not change `sc-implement-protocol/refs/qa.md`, the own-scale primitives, the cap of 2 fix cycles or the 35 percent target. No Jev call, key or account.

# Reviewer 2 (qa) card, pinned model class haiku
reviewer_model_self_report: "OpenAI ChatGPT (exact model identifier unavailable)"  -> does NOT match the haiku pin; identity_mismatch_suspected: true (gateway alias behind the Agent tool model override; matches spec UNVERIFIED item at lines 587-589)
Saved by the orchestrator from the reviewer's return. Wording shortened, citations kept. Plan = TASK-WF-...-202912.md, Spec = merged-requirements.md.

R2-F1 blocking contradiction (1.00): plan 26 says never use Opus in any new template, but Task 11 (plan 142-146) requires parity templates to resolve to Opus; spec 235 ("Opus uses") permits it. Fix: restrict the prohibition to the Opus uses the spec allows.
R2-F2 blocking ordering (0.99): human cluster labels are postponed (plan 27), Task 5 accepts a blank sheet (78-82), Task 8 depends only on Task 7 (102-108); spec 408-409 requires the completed 50-pair check before Stage 1. Fix: owner-input checkpoint before Task 8.
R2-F3 blocking coverage (0.98): the "lint test design" is a Stage 0 deliverable (spec 408) but no Stage 0 task produces it; Task 15 builds the checker later (plan 184-194); Task 7 exit checklist omits it (97-102). Fix: add the design to Task 7.
R2-F4 blocking ordering (1.00): same as R1-F2 (Task 10 acceptance needs Task 11's template; plan 135-142).
R2-F5 medium acceptance (0.97): "clean git status" for the probe window is not reliable (plan 177-182; spec 263). Fix: before/after comparison.
R2-F6 blocking coverage (0.99): Task 20 finds shadow runs by `t2_engine_effective` in each manifest, but no task writes it into the manifest (Task 17 fields omit it, plan 212; Task 18 writes tier_decision.yaml, 222-233; Task 20 at 247; spec 120). Fix: Task 17 manifest persists requested and effective engine; Task 19 passes them at init.
R2-F7 blocking acceptance (0.98): Task 20 can report PASS without running the contract lint on the shadow outputs (spec 410, 470-472; plan 190-194, 247-250). Fix: Task 20 invokes the Task 15 checker per shadow run, with a synthetic extra-key run proving it cannot PASS.
R2-F8 blocking coverage (0.97): forbidden-model filter is not applied to calibrator pick or recorded judge identity, and the REPORT note for a judge-class collision is missing (spec 185, 240; plan 121, 233).
R2-F9 blocking coverage (0.96): Task 19 adds `identity_mismatch_suspected` but not the comparison, the diversity degradation, or the restricted REPORT wording when identity is unverified or executor unknown (spec 255-258, 263; plan 177, 233-239).
R2-F10 medium acceptance (0.95): no explicit wiring of the validator's kept ids into the second `clusters_kept` pass in Task 19 (spec 347; plan 155-158, 233-239).

Coverage: Tasks 1-4, 6, 8, 9, 12, 13, 15, 16, 18 covered; 5, 7, 10, 11, 14, 17, 19, 20 partial. Spans with no task or partly unassigned: spec 408-409, 408 (lint design), 120 (engine in manifest), 185/240, 255/258/263, 410/470, 347.
Lead verdicts: all unverifiable (lead text was not in this reviewer's brief slice; brief for qa carried the card matrix only).

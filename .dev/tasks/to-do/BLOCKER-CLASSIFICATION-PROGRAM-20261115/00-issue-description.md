Review gates classify too many findings as "blocking". Every blocking finding stops the run, forces a fix cycle and a re-review, even when the finding changes no decision. The framework should instead record non-decisive findings, offer to file them as follow-up issues, and let the user choose to resolve them or file them, rather than halting everything and forcing re-reviews.

## What was observed (research run 2, 2026-11-14)

- **One rule, copied into 21 source files (109 occurrences)** plus the installed copies under `~/.claude`: output style `pragmatic.md`; agents `rf-qa`, `rf-qa-qualitative`, `rf-task-builder`; skills `task`, `tech-research`, `task-builder`, `tech-reference`, `operational-guide`, `roadmap`, `readme`; MDTM templates 01 and 02; `agent_template_qa.md`; `skill_template.md`; four `rules/prompts/*qa_prompt.md`. `spec-panel.md` and `cli/review/card_convert.py` have their own scales.
- **The rule says a false claim is blocking regardless of consequence.** A wrong docstring label, a miscounted "four versus six meanings" and two one-character table-pipe defects each failed a gate. `spec-panel.md` already uses a stricter test: a finding blocks only when it names a concrete wrong outcome someone would act on.
- **Measured on the Gate 1 sample** (11 blocking findings, my own re-grade under the proposed rule): blocking findings 11 to 6 (minus 45 percent); average severity score (critical 3, important 2, minor 1) 2.09 to 1.64 (minus 22 percent). With the two cycle-2 table-formatting findings: 13 to 6, minus 54 percent blocking and minus 26 percent score. The 35 percent score target was not reached and the rule was not tuned to reach it.
- **Gate 2:** the 15 reviewers' own blocking counts summed to 23; after the override and merging duplicates the consolidation counted 8.
- **Cost:** Gate 1 needed a third review and a second fix cycle (about 25 minutes) for two table-formatting findings.
- **Later gates under the stricter rule:** Gate 3 had 110 findings, 2 blocking and 108 minor; Gates 4 and 5 and the final validation had no blocking finding.

The stricter rule used for run 2 (owner decision A) is in `.dev/tasks/to-do/TASK-RESEARCH-review-panel-run2-20261114-075454/qa/grading-override.md` (branch `ironbelly/shadow-runs`, commit `ad8f57560`). Blocking only if (1) a decision, recommendation, destination, outcome or number the deliverable rests on would be wrong or unsupported, (2) a required deliverable or section is missing, or (3) a security, data-loss or safety-boundary risk (never downgraded). Everything else is a minor note on a follow-up list.

The owner's direction: it is still right to find blocking issues, and the 35 percent target does not need to be strictly met.

## What this issue should deliver

1. **A spec for the framework-wide revision** (via `/sc:brainstorm`): loosen the classification of blockers; record non-blocking findings as follow-ups; offer the user to resolve them or file an issue instead of halting and forcing re-reviews. Needs a written plan (`/sc:workflow`) before any edit, because the change touches more than five source files.
2. **A blocker classifier** that scores whether a finding is a blocker, with a confidence score, usable every time an issue is raised. Candidate engine: the TypeSafe Jev model (a System One decision model that answers typed questions with calibrated probabilities), with the decision logic kept in code. A later version scores the severity itself, not only blocker or not.
3. **Evidence base:** at least 30 past blocking findings from tasklist reviews and spec reviews, categorised as tasklist or spec, scored blind 1 to 5 by three independent agents, averaged, with a minimum blocking threshold; then the generic characteristics of a blocker; then five test runs of the classifier against the scored table.

## Acceptance

- The proposed rule and the blocker characteristics are written down with the evidence table and the threshold.
- The classifier is tested in 5 runs against the validated table; the agreement with the validated blocker labels is reported.
- The spec is reviewed and a `/sc:workflow` plan exists before any framework file changes.

Related: sub-issue work on the Review Panel unification (#549) is where this rule was first applied.

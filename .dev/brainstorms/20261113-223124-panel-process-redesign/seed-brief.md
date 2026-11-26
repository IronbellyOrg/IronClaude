---
topic: "Redesign how the tasklist review panel operates (agent instructions and processes) so cheap-model panels consistently find the issues they missed, in a way that generalises beyond these packages"
domain: architecture
strategy: systematic
depth: deep
proposals_target: 3
handoff_target: none
created: 2026-11-13T22:31:24Z
---

# Seed Brief: panel-process-redesign

Dialogue mode: non-interactive; the answers below come from the owner's request and the study record. This is the second brainstorm on the panel. The first (`.dev/brainstorms/20261113-163248-panel-collaboration/`) asked for five designs in which reviewers exchange messages during a run. This one asks for **two** redesigns of how the panel operates, judged on whether they would have led reviewers to find the issues they missed **consistently**, and on whether they are **broadly applicable**. Messaging between reviewers is allowed but not required: changing agent instructions or processes counts.

## Problem Statement

Reviewer panels of ember, luna and haiku find about 2 of 14 known defects per run on the two defect-rich packages. Across 30 valid-era runs made only of those three models, ten of the sixteen known issues were never found (B1, B2, B5, B6, B8, I1, I4, I5, I6, I7); four (B1, B2, I5, I6) were never found by any of 76 valid-era runs. The panel is a set of isolated reviewers given one brief; nothing in the process forces a reviewer to do the kinds of checks that find these issues. The owner wants two redesigns that would have caught them reliably, that are not tuned to the three packages, and that cost at most 35% more elapsed time than the isolated panel.

## Known Context

- Evidence base: `.dev/eval-workspaces/tasklist-review-panel/20261111-a1/` (COMBO-REPORT.md final sections, ground-truth.json per package, reviewer reports, analysis tables) and the hand-offs `.dev/eval-workspaces/tasklist-review-panel/HANDOFF-review-panel-unification-run2.md` and `HANDOFF-run1-vs-run2.md`.
- Reused enrichment from the first brainstorm (copies in `enrichment/reused/`): `investigation-designspec.md`, `investigation-alias-control.md`, `investigation-patterns.md` (699 runs), `research-light.md`. Its three theories are in the table below and may be accepted, refined or replaced.
- Baselines (isolated, valid era): ember + 2x luna 1.83/14 found, about 348 s elapsed over 3 packages, 64k output tokens; sonnet + 2x luna 2.33/14, 821 s, 139k tokens; haiku + 2x luna 2.2/14, 715 s, 191k tokens. Per-package slowest-reviewer medians: ember + 2x luna 100-122 s, haiku + 2x luna 220-238 s, sonnet + 2x luna 259-302 s. Panel elapsed time is set by the slowest reviewer; faster reviewers idle.
- Model patterns (medians per run): ember 41 s, 7.1k thinking tokens, greps the lines the plan cites, 46% local single-section findings; luna 102 s, 3.6k thinking tokens, reads named files whole, almost never searches; haiku 233 s, 45.8k thinking tokens, searches inside files the plan names; sonnet and grok search the whole repo and open unnamed dependents.
- Harness confounds that depress every number: the merge drops findings with anchors over 200 or claims over 300 characters; the brief never names source.md (156 of 665 runs never opened it); the reviewer sandbox is a checkout taken after the plans were implemented (it already contains the fixes for GT5, GT6, GT9 and part of B8); a reflect report naming I7 sits in the sandbox. Four harness fixes are specified in the first brainstorm (H1 to H4: name source.md in the brief, truncate instead of drop, pre-implementation checkout, remove the leak).
- The review brief (`src/superclaude/rules/prompts/document_review_loop_prompts.md`, copied into `tools/run-reviewer.sh`) grades a requirement the plan never states as Medium (non-blocking), has no missing-task category, defines no severity levels and does not name any driving document.
- Existing study ground truth is only 3 plan packages, 16 known issues, from one repository.

## Three theories from the first investigation (to accept, refine or replace)

| # | Theory | Key evidence |
|---|---|---|
| T1 | Plan-bounded search: cheap reviewers only verify what the plan names; no reverse-dependency or universal-claim sweep | `test_worker_contract.py` opened in 0 of 176 cheap control runs; 7 of the 8 runs that opened it (sonnet, grok) found I7; 0 of 225 others did |
| T2 | Right place, wrong question: one local question per anchor, no enumeration, no satisfiability or stopping-rule check, no other-direction check | 16 cheap findings on the exact I5 sentence all asked "does the grep match too much"; no reviewer ever challenged the unbounded "complete inventory" criterion (B1, B2) |
| T3 | The evidence environment and grading rules hide or suppress defects | post-implementation checkout masks B5, I1, I4; Medium rule and no missing-task category suppress "unstated requirement" findings; ember skipped source.md in 39% of runs |

## Constraints

- Exactly **two** final redesigns. Each is a change to agent instructions, the process around a run, or both; a deterministic (non-model) pre-pass or helper is allowed.
- **Broad applicability**: each redesign must be specified as generic mechanisms keyed to defect classes and to document structure (for example "sentences that quantify over a set", "criteria that embed a command", "a value consumed but never produced"), not to these packages, task numbers or ground-truth wording. Each must show evidence of generality (recurrence of the defect classes in other plans and in other review targets) and a validation plan that does not reuse the data the design was derived from (hold-out packages, leave-one-out).
- **Time**: at most +35% elapsed against the named isolated baseline panel, shown with arithmetic from the measured per-package medians, with the critical path (slowest reviewer) identified; where the redesign reallocates idle time of the faster reviewers, say so.
- Cheap models only for reviewers (ember, luna, haiku; sonnet only as a comparison panel); no Qwen, glm; Opus only as the blind judge; reviewers stay read-only and never see ground truth; the findings-v1 merge contract keeps working.
- Instruction text must not contain ground-truth quotes or issue-specific hints (that would overfit).

## Success Criteria

- Two distinct redesigns, each with: mechanism and instruction or process changes (quoted draft wording where instructions change), model roles, the order of steps and what each step costs in seconds, time arithmetic showing at most +35%, a defect-class coverage matrix naming which of the ten missed issues each class-level mechanism would have triggered and which it would not (and why), a contamination or overfitting safeguard, an estimate of issues found per run with low and high range, failure modes.
- Three theories stated with evidence, and each redesign mapped to at least one.
- A broad-applicability case: defect classes abstracted from the ten issues, evidence they recur outside these packages, and how the redesign applies to other review targets (specs, other plan formats, documentation).
- A validation experiment on hold-out material, and numbered testable requirements.

## Open Questions

- Which defect classes behind the ten missed issues are general (recur in many plans) and which are artefacts of these three packages?
- Can an instruction change alone (a class-keyed checklist or a map-then-verify pipeline inside one run) get cheap models to perform the missing checks, or does the model need the check done for it by a script?
- How much of the gap closes with the four harness fixes alone, before any redesign?
- Is a deterministic structural pre-pass (extract quantifier sentences, criteria with commands, mappings, edited-file lists, reverse-dependency grep results) a general mechanism for any markdown plan or spec?
- Where does the model's own judgement have to stay in the loop, and what stops the pre-pass from becoming a second source of false positives?

## Enrichment Context

Full artifacts: `enrichment/reused/*.md` (first brainstorm), `enrichment/investigation-generality.md` (new, repo-wide recurrence of defect classes), `enrichment/research-external.md` (new, outside evidence). Summary:

### Eight defect classes behind the ten missed issues (investigation-generality.md section 1)

| Class | Definition (no package or task names) | Missed issues | Other documents with a recorded instance | Verdict |
|---|---|---|---|---|
| C1 | Completeness criterion over a set with no stopping rule, or criterion scope differs from the instruction's scope | designSpec GT1, GT2 | 3 (symptoms only) | supported, symptoms only |
| C2 | A rule stated in the source is not carried into the plan | designSpec GT5 | 6 | general |
| C3 | A value read by one component that no row or task writes | designSpec GT6 | 3 | weak |
| C4 | A criterion's literal command or pattern cannot match or pass against the text the same plan orders | designSpec GT9 | 9 | general |
| C5 | After a change, a count, claim or copy in a second location is left stale | designSpec GT10 | 9 | general |
| C6 | "all", "only", "never" sentence contradicted by an inventory, the plan's other tasks, or the enforcing test's scope | alias GT1, GT3 | 12 | general |
| C7 | Dictated text omits a clause of a constraint stated elsewhere in the plan | alias GT4 | 5 (broad form), 1 (narrow form) | general in the broad form only |
| C8 | Plan edits what a test elsewhere pins, with no task to update or run that test | control GT1 | 6 | general |

Seven further classes recur in the other material but are not among the ten (for example tests that pass on old code, stale citations, conflicting source statements); several are about as frequent as the ten, so the ten are not special. Caveats: all material is one repository, one owner and one plan pipeline; counts are phrase-search lower bounds; the records show a class exists, not that cheap panels miss it (only a hold-out run shows that).

**Hold-out candidates (investigation-generality.md section 4):** six other plan packages or documents with recorded defects; cheapest to turn into ground truth are `workerContractFo`, `implementIronbel` and `scIssueClaimPipe` (about 25 items in 3 to 4 hours); a validated 44-defect spec ledger exists but was tuned on across the whole #346 series.

### Outside evidence on instruction and process levers (research-external.md; adjacent evidence only, several items UNVERIFIED snippets)

- A generic checklist did no better than ad hoc reading in human inspections; scenario or perspective-based reading (a concrete detection recipe per defect class) found about 35% more (secondhand figure, replication mixed). Each class needs a recipe, not a "watch for" list.
- Best-supported shape: a script narrows the question and the model judges one item (a static-tool plus model hybrid removed 94-98% of false positives at 2-110 s per alarm). Free-roaming tool use by weaker models was mixed; small models suffer from too much context.
- Parallel same-model passes plus one aggregator raised recall at acceptable cost (5 runs of a small model beat 1 run of a larger one; gains flatten near 5 runs); majority voting can backfire on small models, so use union then verify each finding with an evidence quote. Sequential multi-turn decomposition cost +187% compute in one study, which would break the +35% limit.
- Requirements engineering confirms the classes are general: ISO/IEC/IEEE 29148 quality characteristics (verifiable, feasible, complete, consistent, singular) and the requirements-smell literature; smell detectors ran at 59% precision and 82% recall, so detector output needs filtering. No catalogue entry was found for "universal claim unchecked against the corpus".
- Showing a model another model's conclusions causes anchoring and herding (answer-flip rate up about 10 points, 29-34% of agents conformed); keep lenses blind to each other, give verifiers only the claim and its evidence, randomise item order.

### Implications for the two redesigns

- A class-keyed recipe per defect class (C1 to C8) is the unit of generality; the recipes must be written once, generically, and must not quote any ground truth.
- Where a class needs a repository sweep (C5, C6, C8) or a mechanical run (C4), a deterministic helper can do the sweep and a cheap model judges each hit; where a class is reading-only (C1, C2, C3, C7), the model needs the recipe and a forced enumeration step.
- Parallel lenses fit the +35% limit; sequential passes do not. Idle time of the fast reviewers (ember about 41 s against luna 102-122 s and haiku 220-240 s) is the free budget.
- Generality claims for C1 and C3 are weak and must be stated as such; the validation experiment must use hold-out packages.

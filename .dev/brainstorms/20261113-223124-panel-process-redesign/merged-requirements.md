---
adversarial_status: pass
convergence_score: 0.9756
source: nested/adversarial-1/merged-spec.md
---

# Requirements specification: class-keyed redesigns of how the tasklist review panel operates

<!-- Provenance: This document was produced by /sc:adversarial -->
<!-- Base: Variant 2 (sonnet:analyzer) -->
<!-- Merge date: 2026-11-14 -->

<!-- Source: Base (original, modified) - V2 header lines 1-9, with the conventions block of Variant 1 (lines 3-12) and the label rules of the debate (labels must not clash) -->
Conventions used throughout.
- Paths: `EVAL` = `.dev/eval-workspaces/tasklist-review-panel/20261111-a1`. `BR` = `.dev/brainstorms/20261113-223124-panel-process-redesign`. `HO2` = `.dev/eval-workspaces/tasklist-review-panel/HANDOFF-review-panel-unification-run2.md`. `MR` = `.dev/brainstorms/20261113-163248-panel-collaboration/merged-requirements.md` (the first brainstorm).
- Evidence files: seed = `BR/seed-brief.md`; IG = `BR/enrichment/investigation-generality.md`; EXT = `BR/enrichment/research-external.md`; DS = `BR/enrichment/reused/investigation-designspec.md`; AC = `BR/enrichment/reused/investigation-alias-control.md`; PAT = `BR/enrichment/reused/investigation-patterns.md`; plus HO2 and MR above.
- Issue ids B1-B8 and I1-I7 are the labels in `EVAL/COMBO-REPORT.md` lines 401-417. That legend also lists I8, which is not one of the ten missed issues and is not used here. Never use ground-truth (GT) labels.
- Nine of the ten missed issues (B1, B2, B5, B6, B8, I1, I4, I5, I6) lie inside the "14" known issues of the two defect-rich packages. I7 sits on the control package, which is scored out of 2. I7 is analysed below but is outside every "found out of 14" sum.
- Class ids C1-C8 are the defect classes of section 2. X1-X7 are the other recurring classes. Extractor ids are E1-E7. Sheet item ids are S1, S2 and so on.
- Harness fixes are H1-H4 (the four fixes of the seed). Brief edits are CB-1 to CB-5. Hold-out sets are HO-1 to HO-6 (never H1-H6, which would clash with the harness fixes).
- The two redesigns are named **Redesign 1: Sweep Sheet** and **Redesign 2: Recipe Ledger**. No other name is used for them.
- Arms: Z0-raw (current harness, no fixes), Z0 (the control to beat), K (plain-words checklist), SS (Redesign 1 plus fixes), RL (Redesign 2 plus fixes).
- Z0 = the isolated panel (ember + 2x luna; haiku + 2x luna; sonnet + 2x luna) with H1-H4 and CB-1 to CB-5, run in the same randomised block and on the same day as the arm it is compared with. b = Z0's per-package median of the slowest reviewer.
- "Per run" means one panel run on one package. All probabilities, selection factors and time figures are planning values built from the cited counts. Section 5 replaces each with a measured value. None is a result.

---

<!-- Source: Base (original, modified) - V2 section 1 (table, issue-to-cause map, rejected rival), with the number tables and "explains / does not explain" lines of Variant 1 section 1 -->
## 1. Theories

All three seed theories are kept. Each is sharpened against the numbers. One rival is rejected.

| # | Theory (refined) | Evidence | Instruction or process change it implies |
|---|---|---|---|
| T1 | Reviewers verify what the plan names. Nobody sweeps for what the plan does not name (reverse dependencies, other copies of a claim, other members of a quantified set). Search volume is not the variable; search direction is. | Runs that touched an unnamed test file: sonnet 35%, grok 33%, ember 8%, luna 1%, haiku 0% (PAT section 1). The unnamed test file was opened in 0 of 176 cheap control runs. 7 of the 8 runs that opened it found I7; 0 of 225 that did not (PAT section 4). Haiku searches `tests/` in 81% of runs yet 0 of 25 left the test file the plan names (PAT section 1). Ember searches `tests/` in 49% of runs and opened 0 unnamed test files. The changelog was touched in 1 of 233 designSpec runs and I5 was found 0 times. The one reviewer that saw the stale claim (grok) dropped it as "minor" (DS section 3). | The reverse sweep must be done for the model (a script) or forced as a written step with a literal command template. "Be thorough" does nothing: the sweep never runs without a unit of work. |
| T2 | Right place, wrong question (T2a), or never reached (T2b). The root cause is that nothing in the process gives a reviewer a structural unit of coverage. Attention goes to salient text and asks one local question there. | T2a: 16 cheap findings anchor the exact I5 sentence and all ask the same over-match question (DS section 2c). 3 findings anchor the B5 mapping and analyse only one input case. 1 finding anchors the I1 row and asks a different question. T2b: 0 cheap findings on I4's criterion. 0 findings anchor B1 or B2 in any of 98 cheap reports, and 3 reviewers wrote that those items were "deferred". Attention is concentrated: a model's top-3 tasks take 38-91% of its anchors (PAT section 3). Luna reaches the B1/B2 task in 10% of runs, the I5 task in 6%, the I4 task in 2%. Its run-to-run Jaccard on designSpec is 0.12. Ember reaches the B1/B2 task in 52% of runs but matches B1 in 3%. | Replace salience with an enumerated item list built from document structure (sentences that quantify, criteria with commands, constraints, dictated text, edited files). Give each item a class-keyed question that includes satisfiability and the opposite direction. Make the answer a written ledger line. |
| T3 | The evidence environment and the reporting filters hide or suppress defects. This is a confound on every measured number. T3a is environment. T3b is suppression. | T3a: the sandbox is a post-implementation checkout that already repairs B5, I1, I4 and part of B8 (DS top, AC section 1). 44 of 98 alias reviewers saw the narrowed sentence and did not compare it. Source.md went unread in 156 of 665 runs (ember 39%, luna 22%). T3b: the merge drops findings over 200/300 characters (80 reviewer-level cases, 49 blocking findings lost, HO2 R20). The Medium rule and the lack of a missing-task category push stated-claim staleness to "minor", and all 7 true I7 finds were non-blocking (PAT section 4). | Harness fixes H1-H4 (seed). Plus one brief rule: every defect found must be listed as a finding, with severity graded separately (CB-2). H1-H4 alone are worth about +0.14 of 14 (0.03-0.34); see 3.0.1. |

Key numbers behind each theory, with what each theory does and does not explain.

**T1 (reviews stop at the surface the plan names)**
- Files touched that the plan never names, per run: ember 0.8, luna 0.3, haiku 0.9, sonnet 3.1 (PAT section 1).
- Runs that touched a test file the plan never names: ember 8%, luna 1%, haiku 0%, sonnet 35%, grok 33% (PAT section 1).
- The control package's unnamed test file was opened in 0 of 176 cheap runs. 7 of the 8 runs that opened it found I7 (sonnet and grok).
- The one run that found B8 began with two repository-wide inventory greps (AC section 3).
- Explains I5, I7 and B8 fully, and B6 partly. Does not explain B1, B2 and I6, which sit inside the plan text.
- Implication: "look wider" will not work. The sweep must be handed over as a concrete search, either run by a script or given as a recipe with the exact search form.

**T2 (right place, one local question, no enumeration stage)**
- 16 findings (15 ember, 1 haiku) sit on the one I5 sentence. All 16 ask whether a search matches too much. None asks where else the claim lives (DS section 2c).
- Anchors on the B1 and B2 criterion: 0 in every cheap and non-cheap panel (DS sections 2c and 3).
- I4 area findings: 0. The one ember that searched the real file saw the repaired text and got a pass.
- B6: luna read the right file and graded the leftover as "unclear exemption" (AC section 3).
- The I1 finders succeeded by tabulating row by row, but spent 190-1005 s against ember's 34 s median (DS section 3).
- Explains B1, B2, B5, I1, I4, I5, I6, and B6 partly. Implication: an enumeration must be forced and made cheap. Tabulation works only when someone narrows it first: a script extracts the rows, or a short recipe confines the model to one class.

**T3 (environment and grading rules suppress findings)**
- Treated as an enabler that explains part of the zeros, not the main cause.
- A leak file sat in the sandbox: 2 of the 9 I7 credits came after reading it (AC section 3).
- B1, B2, B6 and I6 are never anchored and need no repository evidence, so no environment change reaches them. That is why the harness share is small (3.0.1).

**Rejected rival: reasoning budget.** More thinking is not the lever for these ten issues.
- Across 7 models, median thinking tokens correlate with hits (rho 0.64).
- Inside ember and luna, hard-issue hits do not rise with thinking (ember 0.25 to 0.22, luna 0.09 to 0.09 per run).
- Haiku thinks 45.8k tokens and still never opens the unnamed test file (PAT section 6, theory A).
- Implication: do not buy the fix with longer thinking or more passes of the same prompt. Spend the idle seconds on distinct items and distinct classes.

<!-- Source: Base (original) - V2 section 1 issue-to-cause table (I1-I8 label range corrected to I1-I7) -->
Mapping of the ten missed issues to the theories. This drives the coverage matrices.

| Issue | Class | Main cause | Secondary |
|---|---|---|---|
| B1 | C1 | T2b (never anchored) | |
| B2 | C1 | T2b | T3a (source unread; the source's scope is narrower than the plan's) |
| B5 | C2 | T2a (one input case only) | T3a (masked by the repaired checkout; source unread) |
| B6 | C6 | T1 (other tasks and the enforcing test's scope) | T2a (luna reached the evidence and graded it "unclear exemption") |
| B8 | C6 | T1 (no inventory) | T3a (narrowed sentence visible and not compared) |
| I1 | C3 | T2a | T3a (repaired code) |
| I4 | C4 | T2b | T3a (repaired heading makes the check pass) |
| I5 | C5 | T1 | T2a (16 inverted questions), T3b (dropped as minor) |
| I6 | C7 | T2a (the sibling comparison was made once, then stopped) | |
| I7 | C8 | T1 | T3b (non-blocking), leak in other panels |

<!-- Source: Variant 1 section 1 (mapping of redesigns to theories), reworked for the two merged redesigns per Change 2 -->
Mapping of redesigns to theories.

| Redesign | T1 | T2 | T3a | T3b |
|---|---|---|---|---|
| Redesign 1: Sweep Sheet | primary: the script runs the reverse sweeps | primary: one forced item question per anchor | depends on H1-H4 | CB-2 (every confirmed defect is listed) and the demotion and promotion rules of 3.0.5 |
| Redesign 2: Recipe Ledger | partly: recipes give named search forms to the search lenses | primary: forced enumeration, in the other direction | depends on H1-H4 | CB-2 and the same rules of 3.0.5 |

---

<!-- Source: Base (original, modified) - V2 section 2 table, with the strength column and target types of Variant 1 section 2 and the issue instances of Variant 3 section 2 -->
## 2. Defect classes and generality

Class statements contain no package, task, file or ground-truth wording. Recurrence counts are distinct other documents outside the three study packages (IG sections 2 and 5). Caveats that apply to every row (IG section 5.4): one repository, one owner, one plan pipeline; phrase-search lower bounds; the records show that the class exists, not that cheap panels miss it.

| Class | Definition (target-neutral) | Ten-issue instances | Recurrence outside the three packages | Strength (IG section 5) | Review targets it applies to |
|---|---|---|---|---|---|
| C1 | A criterion asks for a complete or exhaustive result over a set with no bounded method or stopping rule, or the criterion's scope differs from the scope of the instruction it checks. | B1, B2 | 3 documents (plans and a spec), all symptoms: new items each review round, a closed list used against an open set | Supported with a caveat, symptom-level only. No other criterion worded as a provable inventory was found. Claim only the weaker form. | Plans, specs ("shall list all"), test plans, documentation ("covers every case") |
| C2 | A rule stated in the driving document is not carried into the plan's task text or criterion. | B5 | 6 plans, all with a source line against a plan line | General | Any derived document: plan vs source, spec vs parent requirement, docs vs code behavior |
| C3 | A value, field or state is read, mapped or required by one component and no row, task or step writes it for that case. | I1 | 3 documents: 1 blocking, 1 inferred, 1 low. The exact lookup-table shape was not found elsewhere. | Weak. Plausible only. | Specs with state tables, plans that implement them, data-flow docs |
| C4 | A criterion embeds a command, pattern or test selector whose literal form cannot match or cannot pass against the text or state the same plan orders. | I4 | 9 documents, 8 plans: a search returning nothing on ordered text, a regex that never matches, a selector that skips checks | General | Plans, test plans, runbooks, CI docs, documented commands, specs with verification rows |
| C5 | After a change, a count, claim or copy in a second location is left stale because no task enumerates that location. | I5 | 9 documents (3 plans, 6 delivered texts) | General | Plans, changelogs, release notes, mirrored copies, docs, comments |
| C6 | A sentence says "all", "only", "never" or "outside X nothing", and an inventory, the plan's other tasks or the scope of the enforcing test contradict it. | B6, B8 | 12 documents (4 plans, 8 delivered docs) | General, mostly delivered docs | Any text with universal claims: plans, docs, specs, guides |
| C7 | Verbatim text the plan dictates omits a clause of a constraint stated elsewhere, or contradicts the plan's own criterion. | I6 | 5 plans in the broad form, 1 in the narrow one-clause form | Broad form general; narrow form weak. Claim only the broad form. | Plans with templates, specs with message formats, docs with required wording, policy-bound text |
| C8 | A plan edits files or behavior that a test elsewhere pins, with no task that updates or runs that test. | I7 (control package, of 2) | 6 documents, 5 plans | General | Plans, change specs, refactor proposals, refactoring specs |

The ten are not special. Seven further classes recur about as often (X1-X7 in IG section 3): X1 tests that pass on old code (4 documents), X2 wrong or aged citation (4), X3 two source statements that conflict (3), X4 task ordering or a gate with no consumer (3), X5 criterion that depends on an uncaptured baseline (3), X6 failure path with no route (3), X7 count broken by a forced step (2, weak). Both redesigns are built so that a new class is added as one more class card (3.0.3) and, for Redesign 1, an optional extractor, with no change to the harness.

External support that the classes are general (EXT section 2):
- ISO/IEC/IEEE 29148 quality characteristics (verifiable, feasible, complete, consistent, singular) map onto C1-C8. An unsatisfiable criterion is "feasible" and "verifiable". A criterion with no stopping rule is "verifiable" and "complete". A universal claim contradicted elsewhere is "consistent". A missing task is "complete" for the set. A stale duplicate is "consistent" and "singular". A value read but never written is "complete", "consistent" and a traceability gap.
- The requirements-smell literature has an "open-ended, non-verifiable term" smell next to C1.
- No catalogue entry was found for "universal claim unchecked against the corpus" (C6). Its check is therefore not backed by a published smell and must be shown empirically.
- Smell detectors ran at 59% precision and 82% recall, so detector output needs a model filter (EXT section 1.5).

External support for the levers (EXT section 5; adjacent evidence only, several snippets UNVERIFIED):
- A tool narrows the question and the model judges one item (a static tool plus model hybrid removed 94-98% of false alarms, at 2-110 s per alarm).
- A checklist alone does no better than ad hoc reading in human inspections; a detection recipe per class is what helped (scenario reading about +35%, replication mixed).
- Parallel same-model passes raise recall and plateau near 5 passes. Majority voting can backfire on small models, so use a union and verify with a quote.
- Sequential multi-turn decomposition cost +187% compute in one study, so neither redesign uses it.
- Showing a reviewer another model's conclusions causes herding, so reviewers stay blind to each other in both redesigns.

Limits the specification carries forward:
- Every document is from one repository and one plan pipeline.
- The records show that a class exists, not that cheap panels miss it elsewhere. Only a hold-out run shows that (section 5).
- C1 and C3 are claimed only in the weaker forms above. C7 is claimed only in the broad form.

<!-- Source: Base (original, modified) - hold-out key added per Change 3; sizes from the validation material of the plan's Appendix A9; investigation labels from IG section 4 -->
Hold-out set labels. The brackets give the label the same material has in IG section 4. Those bracketed labels are used only in this key. None of this material comes from the three study packages.

| Label | Material | Size | Investigation label |
|---|---|---|---|
| HO-1 | docs-only plan | 11 items, about 1 hour to write ground truth | [IG H5] |
| HO-2 | plan | 4-8 items | [IG H2] |
| HO-3 | plan | 12 items | [IG H4] |
| HO-4 | larger plan | 9 important findings, about half a day | [IG H3] |
| HO-5 | spec with a validated 44-defect ledger (use the 20 blocking rows) | 20 rows | [IG H1] |
| HO-6 | sanity set | 3 items, in no decision | [IG H6] |

HO-5 was tuned on by earlier work, not by these designs. Section 5 states how each set is used.

---

<!-- Source: Base (original, modified) - V2 section 3 intro, rewritten for the merged scope; distinctness statement and open-question answer new per Change 8 (debate Q1 and Q5) -->
## 3. The two redesigns

Both redesigns keep reviewers read-only and keep the findings-v1 merge contract. Each reviewer writes a ledger in its final message directly above the findings block, and the merge reads only the findings block (3.0.4). Neither redesign exposes ground truth. Both apply on top of the harness fixes H1-H4 from the seed. The fixes and their gain table come from the first brainstorm (`MR` lines 311-352). Justification: the fixes are given in the seed brief itself, they are independent of any redesign, and their estimate rests on counts (the 49 blocking findings lost, the 39% and 22% source skips) that this brainstorm also uses. Nothing else is reused from the first brainstorm. Reviewer-to-reviewer messaging is not used (3.0.10).

Exactly two redesigns are specified. They answer the seed's open question, whether an instruction change alone is enough or a script must do the check, from opposite sides. Redesign 1 puts the sweep in a script and leaves only the judgement to the model. Redesign 2 puts the sweep in written recipes and leaves the model to run it. Neither answer is assumed. Section 5 tests both, together with a plain-words checklist arm (K) that shows what the recipe wording adds.

| What differs | Redesign 1: Sweep Sheet | Redesign 2: Recipe Ledger |
|---|---|---|
| Who runs the sweep | A script (a non-model, read-only pre-pass) | The reviewing model, following a written recipe |
| Unit of coverage | A typed item (at most 12, each with tool output attached) | A recipe row (at most 14 rows per lens) |
| Code added | A pre-pass with extractors E1-E7, item selection and assignment | No pre-pass and no extractors; the shared scaffolding of 3.0 plus a small lens table in the launcher |

What is shared: everything in 3.0 (harness fixes, brief edits CB-1 to CB-5, class cards, the `ledger-v1` ledger, the checks and promotion rules, telemetry, fallback, reach logging, anti-overfitting rules).

These four things are NOT redesigns and are not counted as one:
- the optional blind claim-only verifier (3.0.9), which sits off the critical path and cannot add claims;
- a second fresh ember session;
- a rewrite of the grading rule's Medium sentence (a rubric edit, not to be confused with the brief edit CB-2), which would mix a rubric change into the judged effect and is allowed only as its own later arm;
- one shared list of up to 60 items given to every reviewer.

---

<!-- Source: Variant 1 section 3.0 (shared scaffolding), rebuilt for the merge per Change 4 -->
### 3.0 Shared scaffolding (not a redesign; both redesigns use it)

The unit of generality is the defect-class card. Cards are written once, generically, and rendered by two different consumers: question templates for Redesign 1 and recipes for Redesign 2. Adding a class, a target type or a reviewer model must not require editing the dispatcher. 3.0.1 to 3.0.10 are built first (section 4 recommendation).

<!-- Source: Base (original, modified) - H1-H4 from the seed brief and MR lines 311-352; fix wording from Variant 1 3.0 and Variant 3 section 3.3; INV-013 for the snapshot rule -->
#### 3.0.1 Harness fixes H1-H4 and their gain

| Fix | What changes | Why both redesigns need it |
|---|---|---|
| H1 | The brief names the absolute path of the source document next to the candidate path, and asks the reviewer to read both. Rendered only when a source file exists (CB-1). | Source-dependent defects (C2) cannot fire if the source is never read |
| H2 | Before the merge, truncate `anchor` and `anchor2` to 200 characters and `claim` to 300 (a prefix of an exact quote is still an exact quote). Validate the block with the real findings parser (`src/superclaude/cli/review/findings.py`). | Item-forced anchors are longer; the merge dropped 49 blocking findings in the first study |
| H3 | Review each package in a sandbox built at the plan's base commit, before implementation. For a document with no commit, use the recorded working tree. | A post-implementation checkout repairs or hides B5, I1, I4 and part of B8 |
| H4 | Remove `.dev/reflect/`, `artifacts/`, `progress.md` and every report about the package from the sandbox. | A reflect report leaked I7 (2 of 9 credits) |

Expected gain of H1-H4 alone, out of 14 per run (bottom-up table of `MR` lines 342-350; planning values):

| Fix | Mechanism and assumption | Central | Low-high |
|---|---|---|---|
| H3 pre-implementation checkout | removes false reassurance on B5, I1, I4 and B8 and the "feature already exists" distraction findings; +0.02 on each of 4 issues | +0.08 | 0.02-0.16 |
| H1 source named in the brief | the 39% of ember and 22% of luna runs that never read it become readers; B5, I1 and B2 need the source | +0.03 | 0.01-0.08 |
| H2 anchor and claim normalizer | 49 blocking findings lost to the merge; assume 2% of the dropped findings match a not-yet-found hard issue | +0.03 | 0.00-0.10 |
| H4 remove `.dev/reflect/` | does nothing for cheap panels (I7 is 0 in 30 runs); it lowers measured I7 for sonnet panels, a measurement correction reported on the control package | 0 | 0 |
| **Total (cheap panels)** | | **+0.14** | **0.03-0.34** |

The grading rule (an unstated requirement is graded Medium), the six findings categories and the blind judge are held constant in every arm (REQ-05). The experiment therefore never mixes a rubric change with a redesign. A rewrite of the Medium sentence may only be run as its own later arm.

The H share is reported as its own number: Z0 minus Z0-raw replaces the +0.14 (section 5). It is never summed with a redesign share in a headline.

<!-- Source: Base (original, modified) - V2 "Shared brief changes" CB-1..CB-3 (wording kept, CB-2 reworded for the ledger-v1 verdicts); CB-4 from Variant 1 CB4 with the single-block and id rules; CB-5 from INV-014 -->
#### 3.0.2 Brief edits CB-1 to CB-5

These edits go into the review brief of every arm that is not Z0-raw, Z0 included. They change the brief file `src/superclaude/rules/prompts/document_review_loop_prompts.md` and the study copy in `tools/run-reviewer.sh`. The six findings categories stay as they are.

CB-1 (source named; purpose: H1, fixes source-blind runs). It is rendered only when a source file exists. Otherwise the harness logs `no_source` and C2 is not applicable for that document (INV-013).

> "Driving document: {{SOURCE_ABS}}. Read it in full before you review the candidate. A rule it states that the candidate does not carry is a finding."

CB-2 (every confirmed defect listed; purpose: removes suppression, T3b). The grading rule itself is unchanged, so blocker precision is not moved by a rubric edit. Low harm is a reason for MINOR, never a reason to omit.

> "Every defect you confirm must appear as a line in the findings block, including every ledger row you marked PROBLEM. Set its severity with the grading check. A defect that is not blocking is still listed, as MAJOR or MINOR with blocking false. Do not leave a defect out because it looks small."

CB-3 (blocker sentence; purpose: keeps wrong blockers from growing).

> "A tool line or a recipe step is a fact or a question about the text. It becomes a blocking finding only if you can write the sentence 'An implementer who follows the stated text as written builds X, and X is wrong because Y.'"

CB-4 (merge limits; purpose: no finding is lost to a format rule).

> "The merge enforces these limits. Each finding id is unique and has at most 16 characters. The anchor is 12 to 200 characters. The claim is at most 300 characters. Refs are at most 8. Write one findings-v1 block only. Copy the shortest part of the text that identifies the problem."

CB-5 (free-review floor; purpose: shared item attention must not displace free review, INV-014).

> "The checks you were given do not replace your own review. Keep at least half of your time for your own review of the plan."

<!-- Source: Variant 1 section 3.0 (card schema, block kinds) without the adapter interface, per Change 4; anti-overfitting rules AO-1..AO-8 are the union of Variant 1 AO1-AO8, Variant 2 AO-1..AO-8 and Variant 3 four rules, per Change 14 -->
#### 3.0.3 Class cards, block kinds and anti-overfitting rules

**Class cards as data.** One card per class, validated against a schema. There is no adapter code in version 1: the extractors of Redesign 1 are flat, and the block kinds below are a checklist, not an interface, until a second target type exists.

| Field | Meaning |
|---|---|
| `id`, `name`, `version` | identity and version (the registry version is recorded in every run) |
| `definition` | target-neutral definition, as in section 2 |
| `recipe_text` | at most 120 words, imperative; used by Redesign 2 (3.2) |
| `question_template` | one question with placeholders; used by Redesign 1 (3.1) |
| `extractor` | name of a deterministic extractor, or null |
| `route` | `search` or `read`: which reviewer type suits the class |
| `replicas` | 1 or 2 reviewers get each item or lens |
| `applies_to` | list of target kinds: plan, spec, doc |
| `instances` | at least 2 citations from material outside the study packages |
| `severity_guidance` | one line |
| `known_weakness` | one line, shown to maintainers, never to reviewers |

**Block kinds as the re-derive checklist.** Each target type is read as typed blocks. For a new target type, a maintainer writes down how each kind is recognised.

| Block kind | What it holds |
|---|---|
| `task` | an instruction unit |
| `criterion` | an acceptance or verification statement |
| `constraint` | a rule that binds other text |
| `dictated_text` | text the document orders to be written word for word |
| `edit_target` | a path the document says to change |
| `gate` | the checks the document runs at the end |

Besides the block patterns, the maintainer re-derives: the command dialect, the test and root-document paths, the severity guidance, and the location of truth (source, code or parent spec). The registry README lists this per target type (REQ-38). Recipes and questions are target-neutral; only the block patterns and extractor patterns change for a new target.

**Anti-overfitting rules AO-1 to AO-8.** They apply to every card, recipe, question template, extractor and regex. Referenced from (e) of both redesigns.
- AO-1: a machine lint fails any 4-word sequence taken from a `ground-truth.json` description or plan quote, and any package, task or file name (REQ-07).
- AO-2: the swap test: a recipe or question still reads correctly when its domain nouns are replaced by placeholders. A second author who has not seen the ground truth reviews each card (REQ-08).
- AO-3: every card cites at least 2 instances from outside the study packages. Every extractor is justified by at least 3 recorded instances, except the C3 extractor E6, which is marked "plausible only".
- AO-4: each extractor is tested on at least 3 plans that were not used to write it (REQ-21).
- AO-5: recipes, cards, extractors and regexes are frozen by git tag and hash before the hold-out ground truth is written (REQ-33).
- AO-6: ground truth is never in the sandbox. The pre-pass reads only the candidate, the source if any, and the pre-implementation snapshot (REQ-34).
- AO-7: leave-one-class-out ablation: removing one class moves the other classes' reach by at most 15 points (REQ-35).
- AO-8: a recipe never states an expected outcome, and no worked example comes from the three study packages.

<!-- Source: Base (original, modified) - V2 ledger idea; carrier changed to a ledger-v1 JSON-lines block in the final message per INV-002 and INV-007 (debate/round3-V2.md, round3-V3.md); parse-check rule from Variant 3 section 3.3 -->
#### 3.0.4 Ledger carrier: `ledger-v1`

Two facts about the launcher shape this carrier (read by the orchestrator). It keeps only the final result message of a run as the report (`.dev/eval-workspaces/tasklist-review-panel/20261111-a1/tools/run-reviewer.sh` line 50, and the lines 61-63 retry loop). Its block check only tests that a line starts with the `findings-v1` fence opener (line 57); it does not parse the block. A ledger written in an earlier message of the same run is therefore lost, and a grep cannot tell a good block from a broken one.

The ledger therefore sits in the FINAL message, as a fenced block with info string `ledger-v1`. The heading `## Ledger` comes directly above it. The `## Findings block` heading and the single `findings-v1` block come directly after it. The ledger block has this shape:

````text
```ledger-v1
{"item":"S3","verdict":"OK|PROBLEM|UNSURE","quote_plan":"<exact quote, 12-200 chars, or empty>","quote_other":"<exact quote or tool line, or empty>","problem":"<the defect in one sentence, at most 300 chars; empty for OK>","ran":"<what you ran or read, at most 15 words>"}
```
````

One JSON object per line, one line per assigned item.

| Field | Meaning | Limit |
|---|---|---|
| `item` | the sheet item id (Redesign 1) or the row id the recipe prints (Redesign 2) | a string |
| `verdict` | `OK`, `PROBLEM` or `UNSURE` | one of the three |
| `quote_plan` | an exact quote from the candidate | 12-200 characters, or empty |
| `quote_other` | an exact quote from the source, or a tool line | a string, or empty |
| `problem` | the defect in one sentence; empty for `OK` | at most 300 characters |
| `ran` | what the reviewer ran or read | at most 15 words |

Quoted draft wording for the ledger rule (shared by both redesigns; each redesign adds its own block in 3.1 and 3.2):

> "Only your FINAL message is kept, so put everything in it. Write the heading `## Ledger`, then one fenced block with info string `ledger-v1`. Write one JSON object per line, one line for each item assigned to you, with the keys item, verdict, quote_plan, quote_other, problem and ran. The verdict is OK, PROBLEM or UNSURE. Copy each quote exactly. Then write the heading `## Findings block` and the single `findings-v1` block. A ledger written in an earlier message is lost."

Parsing rules:
- Both blocks are read by a real parser, never by the fence-opener grep (REQ-13). A line that is not valid JSON is a format error and is counted.
- The `findings-v1` rule is untouched: more than one `findings-v1` block makes the parse fail (`ok=False`), so the ledger uses its own info string.
- The text of earlier assistant messages is read for diagnosis only. It never feeds promotion and never changes the `ledger_missing` verdict.
- `ledger_missing` means that the final message has no parseable `ledger-v1` block directly above the findings block. Its rate is reported per arm and must be at most 10% in the compliance spike before any arm runs (REQ-17).

<!-- Source: debate/invariant resolutions INV-005 and INV-007 (debate/round3-V2.md amendments (a) and INV-005 line; round3-V3.md INV-005); validation rules from src/superclaude/cli/review/findings.py lines 90-158 -->
#### 3.0.5 Checks and promotion

**What `findings.py` requires** (read at `src/superclaude/cli/review/findings.py` lines 90-158). A finding id must match `^[A-Za-z0-9][A-Za-z0-9._-]{0,15}$` and be unique. The anchor is 12-200 characters after flattening. The claim is at most 300. Refs are at most 8. A MINOR finding cannot be blocking. More than one `findings-v1` block sets `ok=False`. Unknown keys are not rejected.

**Checks (a post-run script, no model).**
1. Every item assigned to the reviewer has a ledger line. A missing line is flagged. There is no re-ask (time).
2. Substring tests are flattened. They use the same normalisation as `findings.py` (`flat` and `locate`), so a quote that wraps a plan line still matches (REQ-14). `quote_plan` must be a flattened substring of the candidate. `quote_other` must be a flattened substring of the source or of a printed tool line.
3. A PROBLEM row with a failed quote check is unsupported. A finding linked to it is demoted to non-blocking. A finding is blocking only if it carries the CB-3 sentence and two quotes or one search result (REQ-16).
4. The share of demotions caused by the format (a quote that does not match, a line that does not parse) rather than by a wrong defect is reported, because 0.914 squared is 0.835: only about 84% of true rows would pass two quote tests if each quote were copied exactly 91.4% of the time (INV-007).

**Linking.** A findings line is linked to a ledger row by its `probe` key (the item id), or when the row's `quote_plan` lies inside the finding's anchor. The blocks of 3.1 and 3.2 tell the reviewer to set `probe`.

**Promotion.** A PROBLEM row with no linked findings line is promoted by the harness. The harness never writes a claim of its own.
- `claim`: the reviewer's own `problem` text, copied unchanged.
- `anchor`: the row's `quote_plan` (the plan-side quote). A row with an empty `quote_plan` is not promoted.
- Severity MINOR, blocking false, tagged `src=ledger`.
- The line is validated by the same checks as `findings.py` lines 90-121 (`_check_finding`): unique id of at most 16 characters, anchor 12-200, claim at most 300, refs at most 8, MINOR not blocking, valid category (REQ-15).
- It is inserted inside the single existing `findings-v1` block, never as a second block.
- On any failure the line is logged and skipped.
- Promoted findings are counted and reported separately from findings the reviewer wrote, so credit from promotion is never mixed into reviewer yield.

<!-- Source: Base (original, modified) - telemetry keys per Variant 1 section 3.0 (class, probe) with src added for INV-005; unknown-key acceptance per HO2 line 346 -->
#### 3.0.6 Telemetry

Every `findings-v1` line may carry the extra keys `class` (C1-C8 or null), `probe` (item id or null) and `src` (`ledger` for a promoted line, otherwise null). `findings.py` does not reject unknown keys, and the hand-off records the same (HO2 line 346). A test with the real merge must still confirm it before the keys are relied on (REQ-11). The merge contract is otherwise unchanged. For every run the harness writes a per-class yield table: found, wrong blockers, and time.

<!-- Source: Base (original, modified) - graceful degradation from Variant 1 section 3.0; guard rows are new per Change 15 (invariant-probe.md INV-008, INV-012, INV-013 and the plan's risk review RK4) -->
#### 3.0.7 Graceful degradation and guard rows

If the pre-pass or the lens render fails, the harness falls back to the isolated panel with H1-H4 and CB-1 to CB-5, and records `fallback=true` (REQ-12). The fallback decision is taken before any reviewer starts. That is why the pre-pass of Redesign 1 is serial (INV-012): a running reviewer's brief cannot be changed by a later kill. A parallel build is a separate later arm. A ledger check that fails after the reviewers have finished skips demotion and promotion for that run, merges the findings block as the reviewers wrote it, and records `check_skipped=true` (a different flag from `fallback=true`, which means the isolated brief was run).

Guard rows. Probabilities are low, medium or high planning values.

| Guard condition | Effect | Probability | Handling and recovery |
|---|---|---|---|
| Gateway or model unavailable, so a reviewer is killed or retried | The run has fewer reviewers or a late one | Low | The hang guard is 1.5 x (b + expected overhead) from launch (INV-008). A killed or retried reviewer is scored as zero findings (intention-to-treat). Kills and retries are reported per arm (REQ-30). |
| Judge API error | A run is scored without a judgement, which reads as a miss | Low | Errors are listed in a per-batch audit log (REQ-43), so they are not read as misses. |
| Repository search is slow on a large tree (Redesign 1 pre-pass) | The pre-pass eats the time budget | Medium | The search scope is tests, root documents and named paths, with `.dev/` excluded. The pre-pass is killed at min(15 s, 0.10 x b) and the panel falls back to the isolated brief (REQ-18, REQ-24). |
| Missing source or missing base commit (specs and documentation) | CB-1 would render an empty path; the C2 extractor has nothing to read | Medium | CB-1 and the C2 extractor run only when a source exists. The harness logs `no_source`, counts C2 as not applicable, and records the working-tree identity used as the snapshot (INV-013, REQ-01, REQ-03). |
| Empty sheet (no extractor fires) | Redesign 1 adds nothing | Medium | The brief equals Z0's, checked by hash (REQ-23). The run is reported as a no-trigger run. |
| Only one class triggered | The sheet holds items of one class only | Medium | The sheet is filled from that class by ranked trigger strength, up to 12 items. Reach is reported for that class alone and not averaged with multi-class runs. |
| All 12 items would come from one class | One class crowds out the rest | Low | The quota of 1 to 2 items per triggered class prevents it. If it is ever observed, it is a test failure (REQ-19). |
| Only two reviewers left after a failure | The "2 of 3 reviewers per item" rule cannot hold | Low | Assignment drops to replica 1 and never raises the survivors' load (REQ-20). The run is flagged and still counted (intention-to-treat). |

<!-- Source: debate points A-001 and A-006 (reach decomposition; found-any vs found-blocking) and INV-004 (debate/round3-V1.md, round3-V2.md, round3-V3.md); stage list from the refactoring plan Change 4 -->
#### 3.0.8 Reach is decomposed and logged by stage

Reach is not one number. Each stage is logged separately, per item and per class (REQ-41).

| Stage | Question | Redesign 1 | Redesign 2 |
|---|---|---|---|
| Extraction | Does a mechanism produce a candidate that holds the trigger? | An extractor emits it | Not applicable: no extractor |
| Selection | Is the candidate inside the reviewer's work? | It is inside the at most 12 items | The model chose to ledger that sentence within the row budget |
| Act | Does the reviewer write PROBLEM with quotes? | Yes or no | Yes or no |
| Merge survival | Does the finding survive the checks, demotions and the merge? | Yes or no | Yes or no |
| Judge credit | Does the blind judge credit it as the issue? | Yes or no | Yes or no |

The planning matrices in 3.1 and 3.2 use reach = act x s, where s is the selection factor and act covers the later stages. Measured stage rates replace both columns. The per-class band of the act rate is pre-registered before the first arm (REQ-41, INV-004). Found-any and found-blocking are reported as separate numbers, never merged into one.

<!-- Source: Variant 3 (blind verification step, kept only as an off-path audit per the debate: Q1, unanimous) -->
#### 3.0.9 Optional blind claim-only verifier (not a redesign)

A verifier may be added as an audit. It is never on the critical path.
- It runs only when measured spare time remains after the panel, and its time is excluded from every time figure (REQ-46).
- It receives only a claim and its evidence quote, never the plan's other findings.
- It cannot add claims. A claim that it cannot confirm, or rejects, goes to a follow-up list. It is never a blocker.
- It is not an arm in section 5. Its value is reported only as an audit of wrong blockers.

<!-- Source: Base (original, modified) - V2 section 3 statement on messaging, with Variant 1 section 3.0 numbers and EXT section 4 -->
#### 3.0.10 Messaging between reviewers is not used

Showing one model's conclusions to another causes herding (29-34% of agents conformed, about +10 points in answer flips; EXT section 4). Both redesigns keep reviewers blind to each other. The idle seconds of the fast reviewer are spent on distinct items, not on a message exchange. An optional claims-only exchange is a documented extension seam (the telemetry key `class` already tags which class produced a finding). It is out of scope for the first test.

---

<!-- Source: Base (original, modified) - V2 Redesign 1 steps S0-S5, rebuilt per refactoring plan Change 5: serial pre-pass (INV-012), quota selection, 24-slot assignment (INV-011), ledger-v1 carrier (INV-002); determinism and seed from Variant 3 section 3.1(a) -->
### 3.1 Redesign 1: Sweep Sheet (a script extracts typed items, a cheap model judges one item at a time)

Redesign 1 answers the seed's open question from the script side. A non-model script finds the places to check and attaches the tool output. The cheap model judges one item at a time and writes one ledger line for it. The model keeps all judgement. The script never writes a claim.

#### (a) Mechanism, wording and order of steps

Steps S0 to S6, in this order.

**S0. Harness fixes H1-H4.** The sandbox is built at the plan's base commit, leak files are removed, the source is named in the brief when a source file exists, and the anchor and claim normaliser runs before the merge (3.0.1). This is the same setup step as Z0 and adds no time.

**S1. Serial pre-pass.** A script reads the candidate, the source if there is one, and the pre-implementation snapshot. It reads nothing else (AO-6). It uses no model and writes nothing outside its own output folder.
- Deterministic: the same input and the same seed give byte-identical output (REQ-18).
- It finishes before any reviewer starts. A parallel build is a separate later arm (INV-012, 3.0.7).
- Search scope: tests, root documents and the paths the plan names. `.dev/` is excluded (REQ-24).
- It is killed at min(15 s, 0.10 x b). On a kill or an error the panel runs the isolated brief (Z0's brief) and the run records `fallback=true` (REQ-12).
- One panel clock starts before the pre-pass and reports mean and median (REQ-29).

**S2. Selection.** The extractors E1-E7 (table below) emit candidate items.
- Quota: 1 to 2 items for each triggered class. The remaining slots are filled by ranked trigger strength.
- At most 12 items in total.
- ALL candidates and every dropped item are logged, together with the shuffle seed (REQ-19). The rank function is part of the extractor code, is published, and is frozen with it (AO-5).

**S3. Assignment over 24 slots.** 12 items, each given to 2 of the 3 blind reviewers, make 24 slots (INV-011).
- Caps sum to 24. Primary panel: ember 8, luna 1 at most 8, luna 2 at most 8. Haiku panel: haiku at most 6, each luna 9. Sonnet panel: sonnet at most 6, each luna 9. The reviewer that sets the critical path carries the smaller share.
- Routing (A4 roles in (b)): search items to the search reviewer first, reading items to the lunas.
- An item with an empty `evidence` list (no tool output attached) gets replica 1.
- If a reviewer fails, assignment drops to replica 1 for the items it held. It never raises the load of the survivors (REQ-20).
- Item order is shuffled per reviewer with the logged seed, to reduce order bias (EXT section 4, anchoring).

**S4. Reviewers.** All three run in parallel and stay blind to each other. Each gets Z0's brief (baseline plus CB-1 to CB-5) plus the sheet block below. Order inside a reviewer: (1) read the candidate and the driving document; (2) judge the assigned items in the order shown; (3) review freely for the time that remains (CB-5); (4) write the final message: `## Ledger`, the `ledger-v1` block, `## Findings block`, the single `findings-v1` block (3.0.4).

**S5. Checks and promotion.** A post-run script applies 3.0.5: ledger present, flattened quote tests, demotion of unsupported PROBLEM rows, promotion of PROBLEM rows that have no findings line. There is no re-ask (time). If this step fails after the reviewers have finished, demotion and promotion are skipped, the findings block is merged as written, and the run records `check_skipped=true` (3.0.7).

**S6. Merge.** The normal merge, unchanged (H2 normaliser, then `superclaude review merge`).

One-glance step table (primary panel, seconds per package; arithmetic and the other panels are in (c)).

| Step | Who runs it | Seconds (expected) | Bound | On the critical path |
|---|---|---|---|---|
| S0 sandbox | harness | 0 added | none | no |
| S1 pre-pass | script | 8 | kill at min(15 s, 0.10 b) | yes |
| S2-S3 selection, assignment, brief render | script | 1 | none | yes |
| S4 ember (search items) | ember | about 60 in total (41 baseline + 19: 3 s sheet + 8 items x 2 s) | hang guard | no (idle slack 60-90 s) |
| S4 luna 1 and luna 2 (reading items) | luna | b + 19 | hang guard | yes |
| S5 checks and promotion | script | 1 | none | yes |
| S6 merge | harness | same as Z0 | none | no |

<!-- Source: Base (original, modified) - Variant 1 section 3.1(a) extractor table (lines 192-202) and item format, merged with the "tool output attached" column of V2 Redesign 1 step S1; E1 covers C1 and C6 per refactoring plan Change 5 -->
**Extractors E1-E7.** Flat code, one function each, no adapter layer (3.0.3). Every extractor is justified by at least 3 recorded instances outside the study packages, except E6 (AO-3). E6 is experimental and its output is labelled so.

| Id | Class | What it extracts | Tool output attached | Known blind spot |
|---|---|---|---|---|
| E1 | C1 and C6 | Sentences in criteria, in dictated text and in goal lines that contain set words (every, all, each, complete, exhaustive, found, covers, no remaining; only, never, no other, outside X nothing). The task's named scope (paths and globs the task body names, or NONE). Whether the sentence names a closed list, a glob or a count. | The instruction sentence of the same task and both sets side by side. For a universal sentence: scope-limiting phrases elsewhere in the plan that mention the same path or test (skip, ignore, exempt, allow-list, only), the enforcing test the plan names and its listed assertions. | A set word with no bound that the model must judge as bounded elsewhere. Contradicting tasks are not scripted. |
| E2 | C4 | The literal pattern or selector inside each backticked command in a criterion. The strings the same task and earlier tasks order to be written (double-quoted names, headings). Strings that match after lowercasing and collapsing hyphens, spaces and underscores but not literally. | The literal pattern tried case-sensitively against each ordered string (MATCH or NO MATCH). For a test selector: tests collected out of the tests in the named file. The hit count of the command on the base checkout (information only). | Commands with computed patterns. |
| E3 | C8 | Existing paths that carry an edit verb in a task (edited or created). | `git grep -l` of each path and its distinctive strings (the stem) over tests, scripts and docs. The referencing files the plan never names. Whether the plan's gate names them. | Dependents that refer to the file only by an indirect name. |
| E4 | C5 | From negative criteria ("no remaining", "none", "zero hits") and from "N to M" or count changes: the phrase or the number plus noun. | Whole-tree `git grep -F` hits, root-level documents, changelogs and mirrors included, split into plan-named and plan-unnamed files. | Stale claims that use different wording than the plan. |
| E5 | C2 | Rule sentences of the source sections each task cites (modal or universal verbs, or a backticked identifier next to a report, return, halt or set verb). Runs only when a source file exists (INV-013). | The source rules whose own identifiers appear in no citing task, ranked by the number of missing identifiers. | Rules carried in words and not in identifiers. High identifier overlap. |
| E6 (experimental) | C3 | Backticked literals in a read position ("keys on", "when", "==", "returns for") with no occurrence in a write position ("sets", "=", "gives") in the same document. | The read-position quote and the result of the search for the literal in write positions. | High false-positive rate. Low trust. Class support is weak (section 2). |
| E7 | C7 | Constraint clauses (split on semicolons, "and", commas). Dictated-text blocks. Distinctive tokens per clause. Blocks that share two or more tokens with one clause and none with another clause of the same constraint. | A clause-by-text grid for the highest-overlap constraint. | Clauses with no distinctive token. Only the narrow one-clause form is seen. |

**Item format.** The script writes the items as JSON and renders one sheet per reviewer at `{{SHEET_PATH}}`. One item has these fields:

| Field | Content | Limit |
|---|---|---|
| `item_id` | `S<n>` (S1, S2 and so on) | unique in the run |
| `class` | C1-C8 | one class |
| `anchor_text` | the trigger text, copied exactly from the candidate | at most 200 characters |
| `location` | where the anchor sits (task and line) | a string |
| `evidence` | a list of `{path, line, text}`: the attached tool output | `text` at most 160 characters; may be empty |
| `question` | the printed question of the class (next table) | a string |
| `priority` | the rank value used in S2 | a number |

<!-- Source: Base (original) - V2 Redesign 1 "Question templates" (kinds Q, U, M, R, S, K, X mapped to class ids); the C3 row from Variant 1 question template C3 (V2 has no printed C3 question) -->
**Question templates.** Eight questions, one for each class, printed under each item. The answer is OK, PROBLEM or UNSURE. The wording is target-neutral (AO-2, AO-8).

| Class | Extractor | Printed question |
|---|---|---|
| C1 | E1 | "What finite check would let a reviewer say yes to this criterion, and when does it stop? Do the instruction line and the criterion cover the same set?" |
| C2 | E5 | "Does the candidate carry this rule, including each condition and failure path? Quote the carrying sentence, or answer PROBLEM." |
| C3 | E6 | "This text reads or returns on the value «value». Does any row or task write that value? Quote it. PROBLEM if none does." |
| C4 | E2 | "Apply the criterion's literal pattern to the text this task orders. Does it pass on that text? Do not use the current file as evidence; it may already contain the finished work." |
| C5 | E4 | "Is each plan-unnamed hit false after the change? Does any task edit or check it?" |
| C6 | E1 | "Name the set this sentence covers. Find one member it leaves out or contradicts: look at the plan's other tasks, at what the enforcing test skips, and run one count or listing command over the tree." |
| C7 | E7 | "Does each dictated text carry every clause of this constraint? Tick each clause." |
| C8 | E3 | "Open the referencing file the plan never names. Does it pin the text or behavior being changed? Does any task update or run it?" |

<!-- Source: Base (original, modified) - V2 Redesign 1 "SWEEP SHEET" block; the table wording is replaced by the ledger-v1 carrier of 3.0.4 (INV-002, INV-007), the `probe` key (3.0.6) and the free-review floor CB-5 (INV-014) -->
**Quoted draft wording for the sheet block.** It is appended to Z0's brief, after CB-1 to CB-5, and sits next to the ledger rule of 3.0.4. It holds no ground-truth text, no task number and no package name.

> "SWEEP SHEET. A script, not a model, built {{SHEET_PATH}} from the candidate and the repository. Each item has an id, a location, the literal text, a question and tool output. The tool output is a fact about text. Your job is to judge it. Read the candidate and the driving document first, then the sheet. For each item assigned to you, in the order shown, write one line in the `ledger-v1` block: set `item` to the item id, set `verdict` to OK, PROBLEM or UNSURE, and copy each quote exactly. For OK, say in `ran` what you looked at. Do not skip an item. A sheet item is a question, not a finding. Most items are fine. Answer PROBLEM only when you can quote the two texts, or the search result, that prove it. When you write a findings line for a PROBLEM or UNSURE item, set the findings key `probe` to the item id. Keep at least half of your time for your own review of the plan. The sheet does not replace it. Put the ledger under the heading `## Ledger`, directly above the findings block, in your final message."

An empty sheet (no extractor fires) writes no sheet block. The brief is then equal to Z0's, checked by hash (REQ-23).

<!-- Source: Debate/invariant source - INV-001 (invariant-probe.md; debate/round3-V1.md, round3-V2.md, round3-V3.md: 3 of 3 accept), refactoring plan Change 5 -->
**Offline selection-recall gate (INV-001).** Extraction is deterministic, so a selection miss repeats in every run on that document. Crude counts on two defect-rich plans gave 34, 34 and 20 candidate lines per class. A blind pick of 12 from them hits a true line only 6-10% of the time. The gate runs before any model arm and has two parts (REQ-22):
1. The share of hold-out and planted defects whose trigger item is inside the 12 reaches a floor that is pre-registered before the first arm.
2. The rank function beats a random pick on the three derivation plans.

If either part fails, SS does not run. The selection stage is also logged per run (3.0.8), so a selection miss is never read as a model miss.

<!-- Source: Base (original, modified) - V2 Redesign 1 (b), with the slot counts of Appendix A4 of the refactoring plan (INV-011) -->
#### (b) Model roles

Only cheap models review. Sonnet appears as a comparison panel. Every item has 2 reviewers, and replica 1 applies to items with no attached tool output.

| Panel | Roles | Why |
|---|---|---|
| Primary: ember + 2x luna | Ember takes the search-routed items (E2, E3, E4 and the E1 counting items): 8 items under the cap, and the time model uses the same 8. Each luna takes the reading-routed items (the E1 C1 part, E5, E7, E6): 8 items each. | Ember runs recursive searches (78% of runs) and opens files in a grep-first way. It finishes in about 41 s and idles about 60-90 s, so its items are paid for by idle time. Luna reads whole files and almost never searches, so it gets items where the text is on the sheet. Luna sets the critical path, so its share stays at 8. |
| haiku + 2x luna | Haiku takes at most 6 items, only items with attached tool output (E2, E3, E4). Each luna takes 9 items. | Haiku searches in 81% of runs but thinks 45.8k tokens and sets the critical path (220-238 s), so its load is capped. Luna runs about 121 s and stays off the path, so the extra 1 item is free. |
| sonnet + 2x luna | Sonnet takes at most 6 items. Each luna takes 9 items. | Sonnet sets the critical path (259-302 s) and already opens unnamed files (35% of runs). It keeps its unlisted extra sweeping. The lunas have idle time. |

Where the fast reviewer's idle time goes: to the evidence-heavy items. This is the only reallocation of time in the design. Ember's items do not lengthen the panel, because ember finishes about 40-60 s before the slowest luna.

<!-- Source: Base (original, modified) - V2 Redesign 1 (c), recomputed per refactoring plan Appendix A1-A2 (INV-003, INV-008, INV-012); named baseline Z0 -->
#### (c) Time budget

**Named baseline.** Z0 is the isolated panel with H1-H4 and CB-1 to CB-5, run in the same randomised block and on the same day as the arm it is compared with. b is Z0's per-package median of the slowest reviewer. Gate D1 uses these measured medians. For planning only, the first-study medians stand in: ember + 2x luna b = 100-122 s per package (the 348 s figure is a per-run mean summed over the three packages), haiku + 2x luna 220-238 s, sonnet + 2x luna 259-302 s. The cap is 1.35 b: 135.0 s at b = 100 and 164.7 s at b = 122; 297-321 s for haiku; 350-408 s for sonnet.

Cost model (UNVERIFIED): a ledger row is about 75-90 tokens. At 48 tokens/s (derived from luna's 4.9k tokens in 102 s) that is 1.6-1.9 s. Planning value c = 2 s per item for luna, 4 s for haiku, 3 s for sonnet, about 0.4 s for ember.

**Per-step table, primary panel (ember + 2x luna).**

| Step | Actor | Baseline | Redesign 1 | Bound | Critical path |
|---|---|---|---|---|---|
| S0 sandbox build (base commit) | harness | same | same | none | no |
| S1 pre-pass | script | 0 | 8 expected | kill at min(15 s, 0.10 b): 10 s at b = 100, 12.2 s at b = 122 | yes |
| S2-S3 selection, assignment, brief render | script | 0 | 1 | none | yes |
| S4 ember (8 items, search items) | ember | 41 | about 60 (41 + 3 s sheet + 8 items x 2 s) | hang guard | no (slack 60-90 s) |
| S4 luna 1 and luna 2 (8 items each) | luna | b | b + 3 + 8 x 2 = b + 19 | hang guard | yes |
| S5 ledger check and promotion | script | 0 | 1 | none | yes |

Critical path = 8 + 1 + (b + 19) + 1 = b + 29.

| b | Expected (b + 29) | Increase | Pre-pass at its kill limit | Increase | At break-even per item | Cap |
|---|---|---|---|---|---|---|
| 100 | 129 | +29.0% | 10 + 1 + 119 + 1 = 131 | +31.0% | 8 + 1 + 100 + 3 + 8 x 2.75 + 1 = 135 | 135.0 |
| 122 | 151 | +23.8% | 12.2 + 1 + 141 + 1 = 155.2 | +27.2% | 8 + 1 + 122 + 3 + 8 x 3.71 + 1 = 164.7 | 164.7 |
| mean 116 | 145 | +25.0% | | | | 156.6 |
| three-package sum 348 | 348 + 87 = 435 | +25.0% | | | | 469.8 |

The tightest cell is 131 s against a cap of 135.0 s (pre-pass at its kill limit, b = 100).

**Break-evens at b = 100.** The pre-pass may take up to 14 s (135 - 1 - 119 - 1) before the cap is reached. The cost per item may be up to 2.75 s with 8 items (8 x 2.75 = 22 s). Break-even at b = 122 is 3.71 s per item.

**Fallback.** If the 5-run luna timing spike (REQ-32) shows more than 2.75 s per item, each luna's share drops to 6 items and ember takes the remainder (24 slots: 6 + 6 + 12). In this fallback only, ember's cap is raised from 8 to 12: ember then ends at about 41 + 3 + 12 x 2 = 68 s, still well below luna's b of 100 or more, so its extra items stay off the critical path. The critical path becomes b + 25 (8 + 1 + 3 + 6 x 2 + 1 + b = b + 25). If the measured pre-pass exceeds its kill limit, the panel falls back to Z0's brief (S1). The sheet is never built in parallel with the reviewers' first reads in this specification (INV-012).

**Other panels.**

| Panel | Critical path reviewer | Arithmetic | Elapsed |
|---|---|---|---|
| haiku + 2x luna | haiku (luna about 121 s, off the path) | b + 8 + 1 + 3 + 6 x 4 + 1 = b + 37 | 257 s (+16.8%) at 220; 275 s (+15.5%) at 238; cap 297-321 s |
| sonnet + 2x luna | sonnet | b + 8 + 1 + 3 + 6 x 3 + 1 = b + 31 | 290 s (+12.0%) at 259; 333 s (+10.3%) at 302; cap 350-408 s |

**Enforced by structure.**
- The pre-pass kill at min(15 s, 0.10 b).
- The 12-item cap.
- The hang guard at 1.5 x (b + expected overhead) from launch (INV-008). A killed or retried reviewer is scored as zero findings (intention-to-treat). Kills and retries are reported per arm (REQ-30).

**Only expected.** The per-item cost, the pre-pass seconds and the median elapsed. They are measured against same-day Z0 (REQ-29). The +35% requirement is judged on per-package medians, not on one run, because the natural run-to-run spread of one reviewer is larger than 35%.

<!-- Source: Base (original, modified) - V2 Redesign 1 (d), recomputed once from the consensus design with the selection factor as its own column (refactoring plan Appendix A5a; INV-004, INV-006); reach definition per 3.0.8 -->
#### (d) Defect-class coverage matrix

Per run, primary panel (ember + 2x luna), with H1-H4 applied. **act** is the probability that the item is extracted, the model acts on it and the finding survives. **s** is the selection factor: the chance that the trigger item is inside the 12. **reach = act x s** (low x low, high x high). Every value is a planning value built from the cited counts. Each is replaced by the measured stage rates of 3.0.8 (extraction, selection, act, merge survival, judge credit), and the per-class act band is pre-registered before the first arm (REQ-41).

| Issue | Class | Trigger item (class-level) | act | s | reach | Reviewer slot | Why a cheap model then reaches it / why not |
|---|---|---|---|---|---|---|---|
| B1 | C1 | E1: criterion with a set word beside its task's named scope, asks for the finite check | .10-.35 | .35-.70 | 0.04-0.25 | luna x2 | One-step question; never anchored before (0 anchors in 98 cheap reports). Lexical rank on 34 candidate lines is the weak step |
| B2 | C1 | E1 same item, scope of criterion differs from the instruction's | .15-.40 | .35-.70 | 0.05-0.28 | luna x2 | Two scopes side by side is a read, not a search |
| B5 | C2 | E5: source rule whose identifiers are missing from the citing task | .20-.45 | .40-.70 | 0.08-0.32 | luna x2 | Gives the rule so the 39% source skip no longer matters; misses when identifier overlap is high or the rule is carried in words |
| I1 | C3 | E6 (experimental): read value with no write occurrence | .03-.15 | .25-.50 | 0.01-0.08 | luna | Weak extractor, weak class; not expected to be reached |
| I4 | C4 | E2: pattern vs ordered text, NO MATCH printed | .50-.75 | .80-.95 | 0.40-0.71 | ember + luna | Mechanical; H3 removes the repaired text that gave a false pass |
| I5 | C5 | E4: negative criterion or number phrase with whole-tree hits in an unnamed root document | .35-.60 | .65-.90 | 0.23-0.54 | ember + luna (hits attached) | The hit is handed over; the 16 earlier findings asked the opposite question |
| B6 | C6 | E1: universal sentence plus the task that defines the enforcing test | .05-.20 | .40-.70 | 0.02-0.14 | ember + luna | Contradicting tasks are not scripted; reach depends on the model |
| B8 | C6 | E1: universal sentence over a class of files; asks for one counting search | .10-.30 | .35-.65 | 0.04-0.20 | ember + luna | Ember runs the search it is asked for, but the search form is the model's |
| I6 | C7 | E7: clause with no token overlap in a block that overlaps another clause | .15-.35 | .40-.65 | 0.06-0.23 | luna x2 | Narrow form, weak support |
| **Sum, nine issues in the 14** | | | | | **0.92-2.73** (central 1.83) | | |
| I7 (control, of 1) | C8 | E3: unnamed test file that references an edited path | .40-.65 | .85-.95 | 0.34-0.62 | ember + luna | 7 of 8 runs that opened the file found it; the item makes opening it an instruction |

Notes on the table.
- The sum row covers the nine issues inside the 14. I7 sits on the control package, which is scored out of 2. Its row gives the chance of finding the one issue I7 (row label "of 1"), and it is outside every "of 14" sum.
- The central value 1.83 is the midpoint of 0.92 and 2.73. The per-row reach values are rounded to two places and the sum is taken from the unrounded products, so the printed rows add to about 0.93-2.75.
- The matrix uses the consensus design only (cap 12, quota, 24 slots). It is not a mean of the two original variants' matrices (INV-006).

**Not reached, and why.**
- I1 (C3): there is no reliable trigger shape and E6 is experimental. The reach 0.01-0.08 is not expected to be seen.
- I6 (C7): only the narrow one-clause form is seen, and the claim is limited to the broad form (section 2).
- B6 and B8 (C6): they need counting searches whose form the model must invent, and the contradicting task is not extractable.
- "Consistent" (reach at least 0.6 in at least 60% of runs) is expected only for the mechanical classes: I4 at 0.40-0.71 and I7 at 0.34-0.62. It is not claimed for any other issue (INV-004, REQ-45). The upper ends of both ranges are optimistic.

<!-- Source: Base (original, modified) - V2 Redesign 1 (e), extractor letters renamed to E1-E7; block kinds and re-derive list from Variant 1 section 3.0 (kept as 3.0.3); anti-overfitting rules by reference to AO-1..AO-8 (refactoring plan Change 14) -->
#### (e) Broad applicability and anti-overfitting

**Other plans.** The extractors key on sentence shapes and on backticks, quotes, paths and tables, not on any package. A new plan format needs a section map (where instructions, criteria, constraints and dictated text live) and an "edited object" detector.

**Specifications.**
- E1 reads `shall` and `must` lines and the scope they name.
- E2 reads examples and message formats.
- E7 reads normative constraints.
- E5 compares a requirement to its parent requirement. It runs only when a parent document exists.
- E3 reads "affects" lists.
- E4 reads cross-references.

**Documentation reviews.** E1 (the C6 part) and E4 carry the load: 8 delivered-document instances of C6 and 6 of C5 are recorded (IG). The "source" is the code or the changelog. E2 applies to documented commands.

**What to re-derive per target.** Each target type is read as typed blocks. The block kinds of 3.0.3 are the checklist: `task`, `criterion`, `constraint`, `dictated_text`, `edit_target`, `gate`. For a new target type the maintainer writes down how each kind is recognised, and re-derives:
- the section map and the edited-object detector;
- the command dialect;
- the test and root-document paths (the search scope of S1);
- the severity guidance;
- the location of truth (source, code or parent specification);
- a pre-change snapshot of the repository (H3), or the recorded working tree for a document with no commit.

The registry README lists this per target type (REQ-38). Fixtures exist for a specification and a documentation target (REQ-37: E1, E2 and E5 produce items on a specification fixture; E4 and E1 on a documentation fixture). A new class is one card plus an optional extractor, with no change to the dispatcher (REQ-10).

**Anti-overfitting.** AO-1 to AO-8 of 3.0.3 all apply, as follows.

| Rule | How it applies to Redesign 1 |
|---|---|
| AO-1 | The lint runs over the extractor regexes, the question templates and the sheet block (REQ-07). |
| AO-2 | Each question template passes the swap test. A second author who has not seen the ground truth reviews each card (REQ-08). |
| AO-3 | Each extractor is backed by at least 3 recorded instances outside the study packages. E6 is marked "plausible only". |
| AO-4 | Each extractor is tested on at least 3 plans that were not used to write it. E1-E4 and E7 reach recall 0.8 or more there, and precision is reported (REQ-21). |
| AO-5 | The extractors, the rank function, the regexes and the cards are frozen by git tag and hash before the hold-out ground truth is written (REQ-33). |
| AO-6 | The pre-pass reads only the candidate, the source and the pre-implementation snapshot. A grep check proves that no ground truth or review output is in the sandbox (REQ-34). |
| AO-7 | Leave-one-class-out ablation: removing one class's extractor moves the other classes' reach by at most 15 points (REQ-35). This also tests whether the quota prevents crowding. |
| AO-8 | A question template never states an expected outcome. No worked example comes from the three study packages. |

<!-- Source: Base (original, modified) - V2 Redesign 1 (f), recomputed per refactoring plan Appendix A6: harness share and redesign share kept apart; displacement range 0.1-0.9 (INV-014) -->
#### (f) Expected gain

Issues found out of 14 per run, primary panel (ember + 2x luna). All values are planning values. The harness share (H) and the redesign share are kept apart.

| Block | Low | Central | High | Basis |
|---|---|---|---|---|
| Baseline Z0-raw (isolated ember + 2x luna) | 1.83 | 1.83 | 1.83 | measured (seed) |
| Harness fixes H1-H4 (share H) | +0.03 | +0.14 | +0.34 | MR lines 342-350 bottom-up table (H3 +0.08, H1 +0.03, H2 +0.03, H4 0); replaced by Z0 minus Z0-raw |
| Redesign 1, gross (nine issues) | +0.92 | +1.83 | +2.73 | sums of the matrix in (d) |
| Displacement of easy finds (shared item attention, ledger time) | -0.90 | -0.50 | -0.10 | planning range (INV-014), measured as non-probe findings per run |
| **Redesign 1 net share** | **+0.02** | **+1.33** | **+2.63** | low pairs the worst of each term |
| **Total found, Redesign 1** | **1.9** | **3.3** | **4.8** | |

The total is the sum of the baseline, the H share and the net share: low 1.83 + 0.03 + 0.02 = 1.88 (1.9); central 1.83 + 0.14 + 1.33 = 3.30 (3.3); high 1.83 + 0.34 + 2.63 = 4.80 (4.8).

**Control package.** I7: +0.34 to +0.62 of 1 (the one issue I7). It is not part of any total above.

**Optimism note.** The best single panel run recorded is 4 of 14, so the high end (4.8) is optimistic. The central total (3.3) is a planning value and not a claim.

**Reporting rule.** The H share and the redesign share are reported as separate numbers (Z0 minus Z0-raw, and SS minus Z0). They are never summed in a headline (REQ-40). The 0.1 overlap on I4, I1 and B5, where H3 also masks the issue, is not removed. Gain is worded as "raises the per-run found fraction" (REQ-45).

<!-- Source: Base (original, modified) - V2 Redesign 1 (g), token figures from refactoring plan Appendix A7 -->
#### (g) Overhead

- **Elapsed.** Expected +23.8% (b = 122) to +29.0% (b = 100) on the primary panel. With the pre-pass at its kill limit: +27.2% to +31.0%. Haiku panel +15.5% to +16.8%. Sonnet panel +10.3% to +12.0%. The arithmetic is in (c).
- **Output tokens.** Baseline output is 21.3k per package for ember + 2x luna (63.7k haiku panel, 46.3k sonnet panel). Redesign 1 adds +6k to +9k output (+28% to +42%): about 8 ledger rows of 40-90 tokens per luna, plus ember's extra tool use. Haiku and sonnet panels: +6k (about +9% and +13%).
- **Input tokens.** +1.2-2.5k per reviewer for the sheet.
- **Model tokens in the pre-pass.** None.
- **Judge cost.** Unchanged.
- All figures are unmeasured.

<!-- Source: Base (original, modified) - V2 Redesign 1 (h), lines from refactoring plan Appendix A8 (adapter code dropped) -->
#### (h) Implementation effort

Lines are rough and unmeasured.

| Item | Where | Rough lines |
|---|---|---|
| Shared scaffolding (cards as data and loader, lint, `ledger-v1` parser and checks, promotion function, H2 truncation, telemetry) | shared with Redesign 2, built first | about 450 |
| Extractors E1-E7 and the item model | new pre-pass tool | 450-600 |
| CLI and assignment (S1-S3) | new pre-pass tool, launcher call and kill | about 90 |
| Tests and fixtures (fixtures for non-study plans about 250; tests up to about 150 more) | tests | 250-400 |
| **Redesign 1 specific** | | **about 790-1,090** |
| **Total with the shared scaffolding** | | **about 1,240-1,540** |

The specific subtotal is the sum of the three item lines: 450-600 + 90 + 250-400 = 790-1,090. Adding the shared scaffolding of about 450 gives 1,240-1,540. Both are unmeasured planning values (UNVERIFIED).

<!-- Source: Base (original, modified) - union of V1 and V2 Redesign 1 (i) rows and V3 (i) rows, with the probability column and recovery path added (refactoring plan Change 13) and the rows of INV-001, 002, 005, 007, 008, 014 (Change 6) -->
#### (i) Failure modes

Probabilities are low, medium or high planning values. The guard rows of 3.0.7 (gateway down, judge error, large tree, missing source, empty sheet, one class only, one class crowding, two reviewers left) apply to this redesign as well and are not repeated.

| Failure | Effect | Probability | Mitigation and recovery |
|---|---|---|---|
| Extractor misses the trigger (a shape the regexes do not know) | The class is lost silently for that document | Medium | Extractor recall is measured on planted and non-study plans (REQ-21). Recovery: the free review (CB-5) still runs. A new shape is added as one more extractor under the registry, then re-frozen (AO-5). |
| Over-extraction crowds the true item out of the 12 | Same loss as a miss | Medium | The quota of 1-2 per triggered class stops one class taking all slots. Candidates and dropped items are logged (REQ-19). Recovery: revise the rank function before the hold-out freeze. |
| Rubber-stamp: the model answers OK to every item. About 41% of smell-detector items are non-defects, so OK is often right. | Gain near zero while time rises | Medium | OK-rate is measured on planted items. Gate D2 and the K arm (D7) show whether the sheet adds anything. Recovery: if D2 fails, keep Z0. |
| Selection miss repeats in every run on that document (INV-001) | A true issue is never on the sheet, so the act rate is irrelevant | Medium | Offline selection-recall gate G0 before any model arm. Selection is logged apart from act (3.0.8), so the miss is not read as a model miss. Recovery: revise the rank function and the quota before the freeze. If the floor is not met, SS does not run. |
| Ledger lost: it was written in an earlier message and not in the final one (INV-002) | The checks have nothing to read. No demotion and no promotion for that reviewer. | Medium until the compliance spike | The brief requires the `ledger-v1` block in the final message. `ledger_missing` is at most 10% before any arm (REQ-17). Recovery: the findings block is merged as the reviewer wrote it, and the run records `ledger_missing`. |
| Promoted line rejected by the parser (INV-005) | A PROBLEM row with no findings line earns no credit | Low | The line is validated by the same checks as `findings.py` lines 90-121 and inserted inside the single block (REQ-15). On any failure it is logged and skipped. Promoted lines are counted apart from reviewer findings. |
| Format-induced demotions (INV-007): a quote that does not match, or a line that does not parse | A true row is demoted although the defect is real. If each quote is exact 91.4% of the time, only about 84% of true rows pass two quote tests (0.914 squared = 0.835). | Medium | Flattened substring tests (REQ-14). The share of demotions caused by format is reported. Recovery: the finding stays in the report as non-blocking. |
| Wrong blockers grow (tool lines look authoritative) | More wrong blockers than Z0 | Medium | CB-3; UNSURE is non-blocking; a blocker needs two quotes or one search result (REQ-16). Gate D4: wrong blockers at most Z0 + 1.0 per run, and blocking findings on clean twins at most Z0 + 0.7. |
| Displacement of easy finds (INV-014): item attention replaces independent salience | Findings that Z0 gets for free fall. Planning range 0.1-0.9 of 14. | Medium | CB-5 (half of the time for free review). Non-probe findings per run are measured. Gate D6 (non-regression) is blocking (REQ-42). Recovery: cut the sheet to fewer items. |
| Pre-pass time on a large tree | The cap is broken (break-even 14 s at b = 100) | Medium | Search scope is tests, root documents and named paths, `.dev/` excluded. Kill at min(15 s, 0.10 b). Recovery: fall back to Z0's brief with `fallback=true` (REQ-18, REQ-24). |
| The sheet anchors reviewers on the items only | Reviewers stop looking beyond the sheet | Medium | The brief says the sheet does not replace free review. The item count is at most 12. The non-probe findings per run are the measure. |
| Dictation-blind classes C3 and C7 stay narrow | I1 and I6 are not reached. E6 is weak and E7 sees only the one-clause form. | High | The claim is limited to the broad form of C7 and the weak form of C3 (section 2). E6 is labelled experimental. Both are reported per class, never in a headline. |
| Kill or retry at the hang guard (intention-to-treat) | A reviewer is lost, so the run has fewer findings | Low | Guard 1.5 x (b + expected overhead) from launch (INV-008). A killed or retried reviewer is scored as zero findings and counted per arm (REQ-30). |
| The sheet sees the wrong snapshot | Tool lines are wrong (a repaired checkout gives a false pass) | Low | H3 is a precondition of the pre-pass (REQ-03). The snapshot identity is logged. |
| The sheet becomes a leak path for ground truth | The study is invalid | Low | AO-6 and a grep check on the sandbox and the sheet (REQ-34). |

<!-- Source: Base (original, modified) - V2 Redesign 2 (a) steps R0-R5, renumbered R0-R4 per refactoring plan Change 7; ledger-v1 carrier (INV-002, INV-007); no luna re-ask (INV-010) -->
### 3.2 Redesign 2: Recipe Ledger (written class recipes and a forced enumerate-then-judge ledger, no pre-pass)

Redesign 2 answers the seed's open question from the instruction side. No script finds the places to check. Each reviewer gets a lens of two to four written class recipes, runs them step by step, and writes one ledger row for each step. The model runs the sweep and the model judges. There is no pre-pass and no extractor.

#### (a) Mechanism, wording and order of steps

**R0. Harness fixes H1-H4.** The same setup as Z0 and the same as S0 of Redesign 1 (3.0.1). It adds no time.

**R1. Lens assignment.** The launcher gives each reviewer a lens: two to four class recipes, chosen from that model's measured habits (table below). Short prompts per reviewer avoid context collapse in small models (EXT section 1.4). At most 4 recipes per reviewer. On the primary panel C2 and C4 are given to two reviewers; on the haiku panel C1 is, and on the sonnet panel C1 and C7 are (lens table below). The lens table lives in the launcher and is rendered in under 1 s.

**R2. Reviewers.** All three run in parallel and stay blind to each other. Each gets Z0's brief (baseline plus CB-1 to CB-5), its recipe block and the ledger rule below. Order inside a reviewer: (1) read the candidate and the driving document; (2) run each assigned recipe step by step, writing ledger rows; (3) review freely for the time that remains (CB-5); (4) write the final message: `## Ledger`, the `ledger-v1` block, `## Findings block`, the single `findings-v1` block (3.0.4). Every PROBLEM or UNSURE row becomes a findings line, and the reviewer sets the findings key `probe` to the row id.

**R3. Ledger check.** A post-run script applies 3.0.5 in under 1 s. It checks that the ledger exists and that every assigned recipe has at least one row. It checks the row budget (below), the flattened quote tests, the demotion of unsupported PROBLEM rows and the promotion of PROBLEM rows that have no findings line.
- **No luna re-ask.** The condition `now + 30 s <= 1.35 b` can never hold for luna: its report ends at about b + 22 s, so b + 22 + 30 = b + 52 exceeds 1.35 b for every b below 148 s (INV-010).
- **Ember re-ask** happens only if `now + 30 s <= 1.35 b` (REQ-27). Otherwise the run records `ledger_missing`.
- If the check fails after the reviewers have finished, demotion and promotion are skipped, the findings block is merged as written, and the run records `check_skipped=true` (3.0.7).

**R4. Merge.** The normal merge, unchanged.

**Lens table per panel (A4).** Each class sits in at least one lens. C2 and C4 are duplicated in the primary panel; C1 is duplicated in the haiku panel; C1 and C7 are duplicated in the sonnet panel.

| Panel | Reviewer | Lens (classes) | Row limit | Reason |
|---|---|---|---|---|
| Primary | ember | C4, C5, C6, C8 | 14 (the four recipes allow 16, the lens cap applies) | Search lens. Ember runs greps (78% recursive search) and has idle seconds after 41 s. |
| Primary | luna 1 | C1, C2, C3 | 14 (4 + 6 + 4) | Reading lens. Luna reads whole files and rarely searches. |
| Primary | luna 2 | C2, C4, C7 | 14 (6 + 4 + 4) | Reading lens. C2 and C4 are duplicated for redundancy. |
| haiku + 2x luna | haiku | C5, C6, C8 | at most 6 rows | Search lens. Haiku searches in 81% of runs but is the critical path, so its load is capped. |
| haiku + 2x luna | luna 1 | C1, C2, C3 | 14 | As the primary panel. |
| haiku + 2x luna | luna 2 | C1, C4, C7 | 12 (4 + 4 + 4) | Reading lens. |
| sonnet + 2x luna | sonnet | C5, C6, C8, C2 | at most 8 rows | Sonnet already opens unnamed files (35% of runs), so it takes the sweeps. |
| sonnet + 2x luna | luna 1 | C1, C3, C7 | 12 | Reading lens. |
| sonnet + 2x luna | luna 2 | C4, C7, C1 | 12 | Reading lens. |

**Row budget per recipe.** The budget is the last sentence of each recipe quoted below ("Write at most N rows."). The check script enforces it (REQ-26).

| Recipe | C1 | C2 | C3 | C4 | C5 | C6 | C7 | C8 |
|---|---|---|---|---|---|---|---|---|
| Rows at most | 4 | 6 | 4 | 4 | 4 | 4 | 4 | 4 |

- Never more than 14 rows in a lens, whatever the recipes add up to.
- A recipe that finds nothing to check may write `NONE FOUND` with what was searched (see the ledger rule).
- C2 needs the larger budget because it can govern up to 10 rules (INV-010).

One-glance step table (primary panel, seconds per package; arithmetic and the other panels are in (c)).

| Step | Who runs it | Seconds (expected) | Bound | On the critical path |
|---|---|---|---|---|
| R0 sandbox | harness | 0 added | none | no |
| R1 lens render | script | 1 | none | yes |
| R2 ember (4 recipes) | ember | about 81 in total (41 baseline + 40) | hang guard | no |
| R2 luna 1 and luna 2 (3 recipes each) | luna | b + 4 + 2 x rows: expected b + 26 (11 rows), worst b + 32 (14 rows) | hang guard | yes |
| R3 ledger check and promotion | script | 1 | none | yes |
| R4 merge | harness | same as Z0 | none | no |

<!-- Source: Base (original, modified) - V2 Redesign 2 "RECIPES AND LEDGER" block; the pipe-table row wording is replaced by the ledger-v1 JSON lines of 3.0.4, row ids and the `probe` key per 3.0.6 (INV-002, INV-007), CB-5 free-review floor (INV-014) -->
**Quoted draft wording of the ledger rule.** It sits next to the ledger rule of 3.0.4. It holds no ground-truth text, no task number and no package name.

> "RECIPES AND LEDGER. Before you review freely, run the recipes below that are assigned to you, in order. For each recipe step, write one row in the `ledger-v1` block. The row id is the recipe id and a row number, for example `C4.1`, then `C4.2`. Set `item` to the row id, `verdict` to OK, PROBLEM or UNSURE, and copy each quote exactly. In `ran`, say in at most 15 words what you ran or read. If a recipe finds nothing to check in this document, write one row for it with verdict OK, an empty `quote_plan`, and the words NONE FOUND and what you searched in `ran`. Each recipe has a row limit, and you never write more than 14 rows. A recipe row is a question about the text, not a finding. When you write a findings line for a PROBLEM or UNSURE row, set the findings key `probe` to the row id. Keep at least half of your time for your own review of the plan. The recipes do not replace it. Put the ledger under the heading `## Ledger`, directly above the findings block, in your final message."

<!-- Source: Base (original, modified) - V2 Redesign 2 R-C1..R-C8 wording (DEFECT replaced by PROBLEM to match the ledger-v1 verdicts); R-C5 step 2 widened with the root-document, changelog and mirror wording of Variant 1 recipe C5 (lines 167-176) -->
**Quoted draft wording of the eight recipes.** Each is a detection procedure, not a "watch for" list. Each recipe is stored once, in one file, and quoted by lens (REQ-25). No recipe states an expected outcome (AO-8).

> **R-C1.** "For each acceptance criterion or requirement that says every, all, each, complete, exhaustive, found, covers or no remaining: (1) write the finite check that would let a reviewer say yes, with its stopping rule; (2) copy the instruction sentence the criterion checks and write what set each of the two covers; (3) if you cannot write a finite check, or the two sets differ, mark PROBLEM. Write at most 4 rows."
>
> **R-C2.** "Split the driving document into rules: one per sentence that contains must, shall, never, only, halts, reports or returns, or per table row. Take up to 10 rules, preferring those that govern a failure, an exit or a special case. For each, quote the candidate sentence that carries it. For the three with the most conditions, trace each failure path through the candidate's tasks to the output the rule governs. No carrying sentence, or a path that ends in a different output, is PROBLEM. Write at most 6 rows."
>
> **R-C3.** "List every value, field or state that a task reads, maps or requires as the input to a decision (lookup tables, status mappings, conditions). For each, find the row, task or step that writes it, for every case the reader handles. A value with no writer in some case is PROBLEM. Write at most 4 rows."
>
> **R-C4.** "For each criterion that embeds a command, pattern, selector or test name: write the exact text the same task tells the implementer to write or create. Apply the literal pattern to that text, case included (you may run it on a scratch string with Bash). Then ask what the command selects or matches on the current tree. A pattern that cannot match the ordered text, or a selector that picks fewer or other checks than the criterion needs, is PROBLEM. Do not use the current file as proof; it may already contain finished work. Write at most 4 rows."
>
> **R-C5.** "For each change that alters a number, name, count, behavior or default that the repository may also state elsewhere: (1) write the old literal; (2) run one search of the whole tree for it, including root-level documents (changelogs, readmes, guides), mirrored copies and comments, not only the files the plan names; (3) list every hit the plan neither edits nor checks. A hit that would be false after the change is PROBLEM. Grade it with the grading check; never drop it. Write at most 4 rows."
>
> **R-C6.** "For each sentence the plan states or dictates that says all, only, never, every, no other, or outside X nothing: (1) name the set it covers; (2) run one count or listing command for that set over the tree; (3) compare with the plan's other tasks and with the scope of the test or check said to enforce it (what does that test skip or not read?). A member outside the claim, a task that does the opposite, or a test scope narrower than the claim is PROBLEM. Write at most 4 rows."
>
> **R-C7.** "List every constraint, one clause per line (split at semicolons and 'and'). List every piece of text the plan dictates word for word. For each text and each constraint on its topic, tick each clause. A text that omits or contradicts a clause is PROBLEM. Write at most 4 rows."
>
> **R-C8.** "For each file the plan edits or creates, search the tests, scripts and docs for its path and distinctive strings: `git grep -l -F '<string>' -- tests scripts docs`. For each referencing file the plan never names, open it and decide whether it pins the text or behavior being changed. If it does and no task updates or runs it, mark PROBLEM. Write at most 4 rows."

<!-- Source: Base (original) - Variant 1 section 3.2 (line 378), search-form line for search lenses -->
**Search-form line for search lenses.** The launcher adds this line to the lens of every search reviewer (ember on the primary panel, haiku and sonnet on the others). It is a generic form with placeholders only.

> "Search forms you may adapt: `grep -rlF '<path>' <test dirs>`; `grep -rlF '<name without extension>' .`; `grep -rnF '<old value>' . --include='*.md'` (include root files); `printf '%s' '<ordered text>' | grep -c '<pattern>'`."

The recipes cost about 300 tokens per lens and about 800 for all eight (A7). Each recipe has a card in the registry (3.0.3); the recipe text is at most 120 words and is the `recipe_text` field of the card.

<!-- Source: Base (original) - V2 Redesign 2 (b), with the lens sets of refactoring plan Appendix A4 -->
#### (b) Model roles

Only cheap models review. Sonnet appears as a comparison panel. The lens sets of (a) are the roles.

| Panel | Lens assignment | Why (measured model habits) |
|---|---|---|
| Primary: ember + 2x luna | Ember {C4, C5, C6, C8}. Luna 1 {C1, C2, C3}. Luna 2 {C2, C4, C7}. | Ember runs greps (78% recursive search) and finishes in about 41 s, so it has about 60-90 s of idle time that pays for its four recipes (about 81 s in total). Luna reads whole files and rarely searches, so it gets the reading classes. C2 and C4 are duplicated for redundancy. |
| haiku + 2x luna | Haiku {C5, C6, C8} with at most 6 ledger rows. Luna 1 {C1, C2, C3}. Luna 2 {C1, C4, C7}. | Haiku searches in 81% of runs but sets the critical path (220-238 s) and thinks 45.8k tokens, so its load is capped. The lunas have about 120 s of idle time. |
| sonnet + 2x luna | Sonnet {C5, C6, C8, C2} with at most 8 rows. Luna 1 {C1, C3, C7}. Luna 2 {C4, C7, C1}. | Sonnet is the only model that already opens unnamed files (35% of runs), so it takes the sweeps. It sets the critical path (259-302 s). |

Idle time of the fast reviewer is used for searches that the slow reviewers skip (C5, C6, C8). The slow reviewers keep the reading classes. No reviewer sees another's ledger (3.0.10).

<!-- Source: Base (original, modified) - V2 Redesign 2 (c), recomputed per refactoring plan Appendix A3 (INV-003, INV-008, INV-010); named baseline Z0 -->
#### (c) Time budget

**Named baseline.** Z0 and b are as defined in 3.1 (c): Z0 is the isolated panel with H1-H4 and CB-1 to CB-5, run in the same randomised block and on the same day. b is its per-package median of the slowest reviewer. Gate D1 uses the measured medians. For planning, ember + 2x luna b = 100-122 s per package (the 348 s figure is a per-run mean summed over three packages), haiku + 2x luna 220-238 s, sonnet + 2x luna 259-302 s. Cap = 1.35 b: 135.0 s at b = 100, 164.7 s at b = 122, 297-321 s (haiku), 350-408 s (sonnet). The cost model is the same as in 3.1 (c): luna 2 s per row, haiku 4 s, sonnet 3 s, ember about 0.4 s (UNVERIFIED).

**Per-step table, primary panel (ember + 2x luna).**

| Step | Actor | Baseline | Redesign 2 | Bound | Critical path |
|---|---|---|---|---|---|
| R1 lens render | script | 0 | 1 | none | yes |
| R2 ember (4 recipes: 4 searches x 3 s + up to 14 rows x 0.4 s + thinking) | ember | 41 | about 81 | hang guard | no |
| R2 luna 1 and luna 2 (3 recipes each, rows at about 2 s) | luna | b | b + 4 + rows x 2: expected 11 rows b + 26, worst 14 rows b + 32 | hang guard | yes |
| R3 ledger check | script | 0 | 1 | none | yes |

Critical path = 1 + (b + 4 + 2 x rows) + 1. Expected (11 rows): 1 + b + 4 + 22 + 1 = b + 28. Worst (14 rows): 1 + b + 4 + 28 + 1 = b + 34.

| b | Expected (b + 28) | Increase | Worst, 14 rows (b + 34) | Increase | Cap |
|---|---|---|---|---|---|
| 100 | 128 | +28.0% | 134 | +34.0% | 135.0 |
| 122 | 150 | +23.0% | 156 | +27.9% | 164.7 |
| mean 116 | 144 | +24.1% | 150 | +29.3% | 156.6 |
| three-package sum 348 | 348 + 84 = 432 | +24.1% | 348 + 102 = 450 | +29.3% | 469.8 |

The tightest cell is the worst case at b = 100: 134 s against a cap of 135.0 s (+34.0%, slack 1 s).

**Break-even at b = 100.** 2.07 s per row at 14 rows (29 / 14). The 29 s is 135 - 1 - 100 - 4 - 1.

**Fallback.** If the 5-run luna timing spike (REQ-32) shows more than 2 s per row, the lens cap drops to 12 rows (break-even 2.42 s, 29 / 12). There is no re-ask for luna. The ember re-ask runs only if `now + 30 s <= 1.35 b` (REQ-27).

**Other panels.**

| Panel | Critical path reviewer | Arithmetic | Elapsed |
|---|---|---|---|
| haiku + 2x luna | haiku {C5, C6, C8}, at most 6 rows | 6 x 4 + 4 + 2 = b + 30 | 250 s (+13.6%) at 220; 268 s (+12.6%) at 238; cap 297-321 s |
| sonnet + 2x luna | sonnet {C5, C6, C8, C2}, at most 8 rows | 8 x 3 + 4 + 2 = b + 30 | 289 s (+11.6%) at 259; 332 s (+9.9%) at 302; cap 350-408 s |

**Enforced by structure.**
- The row cap of 14 per lens and the row budget per recipe, checked by the script (REQ-26).
- The ember re-ask condition (REQ-27); no luna re-ask.
- The hang guard at 1.5 x (b + expected overhead) from launch (INV-008). A killed or retried reviewer is scored as zero findings (intention-to-treat). Kills and retries are reported per arm (REQ-30).

**Only expected.** The per-row cost, the number of rows a luna actually writes (11 expected) and the median elapsed. They are measured against same-day Z0 (REQ-29). Redesign 2 has no pre-pass on the critical path, but its expected path (b + 28) is within 1 s of Redesign 1's (b + 29) and its worst case (b + 34) is the larger. Its remaining risk is compliance: the models must actually do the steps.

<!-- Source: Base (original, modified) - V2 Redesign 2 (d), recomputed once from the consensus design with the self-selection factor as its own column (refactoring plan Appendix A5b; INV-004, INV-006); reach definition per 3.0.8 -->
#### (d) Defect-class coverage matrix

Same convention as 3.1 (d). Per run, primary panel (ember + 2x luna), with H1-H4 applied. **act** is the probability that the model runs the recipe step, writes PROBLEM with quotes and the finding survives. **s** is self-selection within the row budget: the model chooses which sentences to ledger, because no script picks them. **reach = act x s** (low x low, high x high). There is no extraction stage in this redesign (3.0.8). Every value is a planning value. Each is replaced by the measured stage rates of 3.0.8, and the per-class act band is pre-registered before the first arm (REQ-41).

| Issue | Class | Recipe step (class-level) | act | s | reach | Reviewer slot | Why / why not |
|---|---|---|---|---|---|---|---|
| B1 | C1 | R-C1 step 1: write the finite check for each set-word criterion | .10-.30 | .50-.85 | 0.05-0.26 | luna 1 | A written stopping rule is a new move; models may accept a vague rule |
| B2 | C1 | R-C1 step 2: copy the instruction sentence, write both sets | .10-.30 | .50-.85 | 0.05-0.26 | luna 1 | Short comparison, no search |
| B5 | C2 | R-C2: rule by rule carry and one failure-path trace | .15-.35 | .50-.80 | 0.08-0.28 | luna 1, luna 2 | Up to 10 rules, 6 rows; terse luna may leave rules unrecorded |
| I1 | C3 | R-C3: table of read values against writers | .05-.20 | .40-.70 | 0.02-0.14 | luna 1 | Models tabulate when told; weak class |
| I4 | C4 | R-C4: apply the literal pattern to the ordered text | .40-.70 | .60-.90 | 0.24-0.63 | ember, luna 2 | Pure reading and a one-line `printf` test; the model must choose the criteria |
| I5 | C5 | R-C5: whole-tree search for the old literal incl. root documents | .20-.45 | .50-.80 | 0.10-0.36 | ember | Ember greps; the weak step is choosing which changed claim to search |
| B6 | C6 | R-C6 step 3: what does the enforcing test skip, what do other tasks say | .05-.20 | .40-.70 | 0.02-0.14 | ember | Key evidence sits in other tasks |
| B8 | C6 | R-C6 step 2: one count command over the set | .10-.30 | .35-.65 | 0.04-0.20 | ember | Ember has never run an inventory unprompted; the recipe gives the command shape |
| I6 | C7 | R-C7: clause by text tick table | .10-.30 | .40-.70 | 0.04-0.21 | luna 2 | A matrix over many blocks is hard for a terse model |
| **Sum, nine issues in the 14** | | | | | **0.63-2.47** (central 1.55) | | |
| I7 (control, of 1) | C8 | R-C8: `git grep -l` of each edited path over tests, scripts, docs; open unnamed hits | .20-.45 | .55-.85 | 0.11-0.38 | ember | Opening an unnamed test file is the step luna and haiku skip |

Notes on the table.
- The sum row covers the nine issues inside the 14. I7 sits on the control package, which is scored out of 2. Its row gives the chance of finding the one issue I7 (row label "of 1"), and it is outside every "of 14" sum.
- The central value 1.55 is the midpoint of 0.63 and 2.47. The per-row reach values are rounded to two places and the sum is taken from the unrounded products, so the printed rows add to about 0.64-2.48.
- The matrix uses the consensus design only (one session, at most 4 recipes per reviewer, the lens sets of (a)). It is not a mean of the original variants' matrices (INV-006).

**Not reached, and why.**
- I1 (C3): no reliable trigger shape. A reader must notice a missing write without an extractor.
- I6 (C7): the narrow one-clause form is not claimed (section 2), and a tick table over many blocks is hard for a terse model.
- B6 and B8 (C6): they need counting searches whose form the model must invent. The contradicting task is not extractable and not scripted.
- "Consistent" (reach at least 0.6 in at least 60% of runs) is not expected for Redesign 2: the best cell is I4 at 0.24-0.63. It is expected only for Redesign 1's mechanical classes (I4 0.40-0.71, I7 0.34-0.62). The claim for Redesign 2 is limited to a higher per-run found fraction (INV-004, REQ-45).

<!-- Source: Base (original, modified) - V2 Redesign 2 (e); block kinds and the re-derive list from Variant 1 section 3.0 (kept as 3.0.3); anti-overfitting rules by reference to AO-1..AO-8 (refactoring plan Change 14) -->
#### (e) Broad applicability and anti-overfitting

**Other plans.** The recipes mention no document. Moving to a new plan format needs only a note on where instructions, criteria and constraints live.

**Specifications.** C1, C2, C3, C4 and C7 read directly. For C5, C6 and C8 the "tests" become the checks the specification names.

**Documentation reviews.** C2 and C4 compare the document to the code. C5 and C6 carry most of the load: 8 delivered-document instances of C6 and 6 of C5 are recorded (section 2).

**What to re-derive per target.** Each target type is read as typed blocks. The block kinds of 3.0.3 are the checklist: `task`, `criterion`, `constraint`, `dictated_text`, `edit_target`, `gate`. For a new target type the maintainer re-derives:
- the meaning of "edits", "tests" and "source" for that target;
- the command dialect in the recipes and in the search-form line;
- the test and root-document paths;
- the severity guidance and the location of truth (source, code or parent specification);
- the lens assignment, from the reviewing model's measured habits.

The registry README lists this per target type (REQ-38). A new class is one card with a recipe text of at most 120 words, with no change to the dispatcher (REQ-06, REQ-10).

**Anti-overfitting.** AO-1 to AO-8 of 3.0.3 apply to the recipe text, except where noted.

| Rule | How it applies to Redesign 2 |
|---|---|
| AO-1 | The lint runs over each recipe, the ledger rule and the search-form line (REQ-07). |
| AO-2 | Each recipe passes the swap test: it still reads correctly with its domain nouns replaced by placeholders. A second author who has not seen the ground truth reviews each recipe for issue-specific words (REQ-08). |
| AO-3 | Each card cites at least 2 instances outside the study packages (REQ-06). There are no extractors, so the extractor part does not apply. |
| AO-4 | Not applicable: there are no extractors. The recipes are tested instead by the compliance spike and on the hold-out sets. |
| AO-5 | The recipes and the cards are frozen by git tag and hash before the hold-out ground truth is written (REQ-33). |
| AO-6 | The recipes read nothing themselves. Ground truth is never in the sandbox (REQ-34), checked by grep. |
| AO-7 | Leave-one-class-out ablation: removing one recipe moves the other classes' reach by at most 15 points (REQ-35). |
| AO-8 | A recipe never states an expected outcome. No worked example comes from the three study packages. Any worked example is written from a class definition. |

<!-- Source: Base (original, modified) - V2 Redesign 2 (f), recomputed per refactoring plan Appendix A6: harness share and redesign share kept apart; displacement range 0.1-0.9 (INV-014) -->
#### (f) Expected gain

Issues found out of 14 per run, primary panel (ember + 2x luna). All values are planning values. The harness share (H) and the redesign share are kept apart. The displacement row is the same planning range as for Redesign 1, because the ledger time is the same kind of cost.

| Block | Low | Central | High | Basis |
|---|---|---|---|---|
| Baseline Z0-raw (isolated ember + 2x luna) | 1.83 | 1.83 | 1.83 | measured (seed) |
| Harness fixes H1-H4 (share H) | +0.03 | +0.14 | +0.34 | MR lines 342-350 bottom-up table (H3 +0.08, H1 +0.03, H2 +0.03, H4 0); replaced by Z0 minus Z0-raw |
| Redesign 2, gross (nine issues) | +0.63 | +1.55 | +2.47 | sums of the matrix in (d) |
| Displacement of easy finds (shared item attention, ledger time) | -0.90 | -0.50 | -0.10 | planning range (INV-014), measured as non-probe findings per run |
| **Redesign 2 net share** | **-0.27** | **+1.05** | **+2.37** | low pairs the worst of each term |
| **Total found, Redesign 2** | **1.6** | **3.0** | **4.5** | |

The total is the sum of the baseline, the H share and the net share: low 1.83 + 0.03 - 0.27 = 1.59 (1.6); central 1.83 + 0.14 + 1.05 = 3.02 (3.0); high 1.83 + 0.34 + 2.37 = 4.54 (4.5).

**Control package.** I7: +0.11 to +0.38 of 1 (the one issue I7). It is not part of any total above.

**Optimism note.** The best single panel run recorded is 4 of 14, so the high end (4.5) is optimistic. The low end is a net loss (-0.27): at the worst pairing the ledger time costs more easy finds than the recipes win.

**Reporting rule.** The H share and the redesign share are reported as separate numbers (Z0 minus Z0-raw, and RL minus Z0). They are never summed in a headline (REQ-40). The 0.1 overlap on I4, I1 and B5 is not removed. Redesign 2 is below Redesign 1 on the sweep classes (C5, C6, C8) because the model has to run the sweep itself, and cheap models have shown no habit of it. It is close on the reading classes.

<!-- Source: Base (original, modified) - V2 Redesign 2 (g), token figures from refactoring plan Appendix A7 -->
#### (g) Overhead

- **Elapsed.** Expected +23.0% (b = 122) to +28.0% (b = 100) on the primary panel. Worst case at 14 rows: +27.9% to +34.0%. Haiku panel +12.6% to +13.6%. Sonnet panel +9.9% to +11.6%. The arithmetic is in (c).
- **Output tokens.** Baseline output is 21.3k per package for ember + 2x luna (63.7k haiku panel, 46.3k sonnet panel). Redesign 2 adds +5k to +8.5k output (+23% to +40%). Haiku and sonnet panels: +6k (about +9% and +13%).
- **Input tokens.** The recipes cost about 300 tokens per lens and about 800 for all eight.
- **Judge cost.** Unchanged.
- All figures are unmeasured.

<!-- Source: Base (original, modified) - V2 Redesign 2 (h), lines from refactoring plan Appendix A8 (no extractor code) -->
#### (h) Implementation effort

Lines are rough and unmeasured. There is no extractor code and no pre-pass.

| Item | Where | Rough lines |
|---|---|---|
| Shared scaffolding (cards as data and loader, lint, `ledger-v1` parser and checks, promotion function, H2 truncation, telemetry) | shared with Redesign 1, built first | about 450 |
| Recipe text | one recipes file | about 120 |
| Launcher lens table and row-budget rule | launcher | about 70 |
| Brief additions | brief template | about 40 |
| Tests | tests | about 80 |
| **Redesign 2 specific** | | **about 310** |
| **Total with the shared scaffolding** | | **about 760** |

The specific subtotal is the sum of the four item lines: 120 + 70 + 40 + 80 = 310. Adding the shared scaffolding of about 450 gives about 760. Both are unmeasured planning values (UNVERIFIED).

<!-- Source: Base (original, modified) - union of V1 and V2 Redesign 2 (i) rows and V3 (i) rows, with the probability column and recovery path added (refactoring plan Change 13); single-point-of-failure and row-budget rows from Change 7, INV-010, INV-002, INV-007, INV-014 -->
#### (i) Failure modes

Probabilities are low, medium or high planning values. The guard rows of 3.0.7 that concern reviewers (gateway down, judge error, missing source, two reviewers left) apply here too and are not repeated.

| Failure | Effect | Probability | Mitigation and recovery |
|---|---|---|---|
| Compliance: a terse luna writes OK rows without doing the steps. Luna quotes an anchor exactly in only 91.4% of cases, and ember skipped the source in 39% of runs. | Gain near zero while time rises | High | The quote check (3.0.5). The `ran` field is cross-checked against the transcript's tool calls in the analysis (REQ-28). The 5-run compliance spike must show `ledger_missing` at most 10% before any arm (REQ-17). Recovery: if the spike fails, RL does not run. |
| Prompt length hurts small models | Lower base performance | Medium | Two to four recipes per lens, never all eight. At most 4 recipes per reviewer (REQ-25). Arm K (plain words) shows whether the recipe wording adds anything (D7). |
| Single point of failure per class: C5, C6 and C8 live only in ember; C1 and C3 only in luna 1; C7 only in luna 2 (primary panel). C2 and C4 are duplicated on the primary panel. | If that reviewer fails or is killed, the class is lost for the run | Medium | The loss is reported by class. A killed reviewer is scored as zero findings (intention-to-treat). Recovery: where ember has idle time and evidence is attached, a class may be given to a second reviewer (INV-010). No re-ask for luna. |
| The row budget forces a choice by salience | The model ledgers the sentences that stand out and skips the true one. This is the T2 cause again, inside a smaller space. | Medium | Per-recipe budgets are sized for the class (C2 gets 6, the others 4). `NONE FOUND` with what was searched lets a reviewer say a recipe found nothing. The self-selection factor s is measured (3.0.8). |
| Ember's own sweeps give false hits | Wrong blockers | Medium | CB-3; UNSURE is non-blocking; a blocker needs two quotes or one search result (REQ-16). |
| Wrong blockers grow | More wrong blockers than Z0. Earlier 2x ember panels added 2.75-3.25 wrong blockers. | Medium | Gate D4: wrong blockers at most Z0 + 1.0 per run, and blocking findings on clean twins at most Z0 + 0.7. |
| Ledger lost: written in an earlier message and not in the final one (INV-002) | No demotion and no promotion for that reviewer | Medium until the compliance spike | The brief requires the `ledger-v1` block in the final message. `ledger_missing` is reported per arm (REQ-13, REQ-17). Recovery: the findings block is merged as written. |
| No repair path for luna (no re-ask) | A luna with a missing or malformed ledger is not repaired | High | The re-ask cannot fit the cap for luna (3.2 (a), R3). The run records `ledger_missing`. Recovery: only an ember re-ask is allowed, under `now + 30 s <= 1.35 b`. The compliance spike sets the expected rate. |
| Promoted line rejected by the parser (INV-005) | A PROBLEM row with no findings line earns no credit | Low | The same checks as `findings.py` lines 90-121, inserted inside the single block; logged and skipped on failure (REQ-15). |
| Format-induced demotions (INV-007) | A true row is demoted although the defect is real (0.914 squared = 0.835 of true rows pass two quote tests) | Medium | Flattened substring tests (REQ-14). The share of demotions caused by format is reported. The finding stays in the report as non-blocking. |
| Displacement of easy finds (INV-014) | Findings that Z0 gets for free fall. Planning range 0.1-0.9 of 14. | Medium | CB-5. Non-probe findings per run are measured. Gate D6 is blocking (REQ-42). |
| Time at b = 100, worst case: 14 rows | +34.0% (134 s against a cap of 135.0 s), with 1 s of slack | Medium | Break-even is 2.07 s per row at 14 rows. If the timing spike shows more than 2 s per row, the lens cap drops to 12 rows (break-even 2.42 s) (REQ-32). The median, not one run, is judged (REQ-29). |
| Kill or retry at the hang guard (intention-to-treat) | A reviewer is lost, so the run has fewer findings | Low | Guard 1.5 x (b + expected overhead) from launch (INV-008). A killed or retried reviewer is scored as zero findings and counted per arm (REQ-30). |

---

<!-- Source: Base (original, modified) - V2 section 4 property table, with the rows of Variant 1 section 4 (core mechanism, who finds the trigger text, I7, issues at "consistent", deterministic component, portability, maintainability seam, wrong-blocker risk). Every value comes from the refactoring plan's Appendix A (A1-A8), not from the variants -->
## 4. Comparison of the two redesigns

All figures are planning values from 3.1 and 3.2. "Found of 14" counts the nine missed issues that sit inside the 14 known issues of the two defect-rich packages. I7 sits on the control package, is scored out of 1 on its own row, and is outside every "of 14" sum. The harness share and the redesign share have separate rows and are never added in a headline (REQ-40).

| Property | Redesign 1: Sweep Sheet | Redesign 2: Recipe Ledger |
|---|---|---|
| Core mechanism | A script extracts at most 12 typed items with tool output attached. Each item goes to 2 blind reviewers, who judge one item at a time and write one ledger line each. | Each reviewer gets a lens of 2 to 4 written class recipes, runs them step by step and writes one ledger row per step. No script finds anything. |
| Who runs the sweep | A non-model, read-only pre-pass (serial, deterministic) | The reviewing model |
| Who finds the trigger text | The script (extractors E1-E7) | The model, from the recipe and its search forms |
| Theories addressed | T1 (the script runs the reverse sweeps) and T2 (one forced item question per anchor) with T3b; depends on H1-H4 for T3a | T2 (forced enumeration, other direction) and T1 partly (named search forms) with T3b; depends on H1-H4 for T3a |
| Strong classes | C4, C5, C8 (mechanical triggers) | C4 (reading); below Redesign 1 on C5, C6 and C8 because the model must run the sweep itself |
| Weak classes | C3 (I1), C1 (B1, B2), C6 (B6, B8), narrow C7 (I6) | The same: C3, C1, C6, narrow C7 |
| Found of 14, low / central / high | 1.9 / 3.3 / 4.8 | 1.6 / 3.0 / 4.5 |
| Harness share (H1-H4), same in both | +0.14 (range 0.03-0.34), replaced by Z0 minus Z0-raw | +0.14 (range 0.03-0.34), replaced by Z0 minus Z0-raw |
| Redesign share, gross (nine issues) | +0.92 / +1.83 / +2.73 | +0.63 / +1.55 / +2.47 |
| Redesign share, net of displacement (-0.90 / -0.50 / -0.10) | +0.02 / +1.33 / +2.63 | -0.27 / +1.05 / +2.37 |
| Control package I7 (of 1, outside every "of 14" sum) | +0.34 to +0.62 | +0.11 to +0.38 |
| Issues at "consistent" (reach at least 0.6) | Expected only for mechanical classes: I4 (0.40-0.71) and I7 (0.34-0.62), at the high end only | None expected (best cell I4 at 0.24-0.63) |
| Elapsed, primary panel, b = 100 (cap 135.0 s) | +29.0% expected (129 s); +31.0% with the pre-pass at its kill limit (131 s); +35% only at break-even (135 s) | +28.0% expected (128 s); +34.0% worst case at 14 rows (134 s, 1 s under the cap) |
| Elapsed, primary panel, b = 122 (cap 164.7 s) | +23.8% expected (151 s); +27.2% with the pre-pass at its kill limit (155.2 s) | +23.0% expected (150 s); +27.9% worst case (156 s) |
| Elapsed, haiku panel (b = 220 / 238) | +16.8% / +15.5% | +13.6% / +12.6% |
| Elapsed, sonnet panel (b = 259 / 302) | +12.0% / +10.3% | +11.6% / +9.9% |
| Output tokens, primary panel | +6k to +9k (+28% to +42%) | +5k to +8.5k (+23% to +40%) |
| Implementation effort (lines, unmeasured) | About 790-1,090 specific; about 1,240-1,540 including the shared scaffolding of about 450 | About 310 specific; about 760 including the shared scaffolding |
| Needs a deterministic component | Yes: the pre-pass, extractors E1-E7, item selection and assignment | No: only the shared ledger check of 3.0.5 and a small lens table in the launcher |
| Portability to a target with no adapter | Falls back to the isolated brief (an empty sheet equals Z0 by hash); a new target needs its block patterns and extractor patterns re-derived (3.0.3) | Works with a prompt-only change plus the re-derive list of 3.0.3 |
| Maintainability seam | Extractor functions E1-E7 with fixtures, one card per class | One recipes file and the launcher lens table; one card per class, no code per class |
| Main risk | Selection miss repeats in every run on a document; rubber-stamp OK answers | Compliance: terse reviewers write OK rows without doing the steps; a class lives in one reviewer only |
| Wrong-blocker risk | Medium: tool lines look authoritative | Medium: the reviewer's own sweeps give false hits |
| What it tests of the seed's open question | That the model needs the check done for it by a script | That an instruction change alone is enough |

### 4.1 Answers to the seed's open questions

These are answers from the planning evidence. Section 5 turns each into a measurement.

1. **Which defect classes are general and which are artefacts of the three packages?** C2, C4, C5, C6, C8 and C7 in its broad form recur in other documents and are treated as general (section 2). C1 and C3 are weak: C1 is supported by symptoms only and C3 is "plausible only". C7 is claimed in the broad form only. The records show that a class exists, not that cheap panels miss it. Only the hold-out and planted runs show that (section 5).
2. **Can an instruction change alone get cheap models to perform the missing checks?** Untested. Redesign 2 tests exactly this, and arm K (plain words, no recipes) shows what the recipe wording adds. The expectation is lower reach than Redesign 1 on the mechanical classes (I4 0.24-0.63 against 0.40-0.71, I7 0.11-0.38 against 0.34-0.62).
3. **How much of the gap do the four harness fixes close?** About 0.14 of 14 (range 0.03-0.34). That is small, and it is a planning value. It is measured as Z0 minus Z0-raw and reported on its own (section 5, REQ-40).
4. **Is a deterministic structural pre-pass a general mechanism for any markdown plan or spec?** The extractors are keyed to sentence shapes and block kinds, not to a package. A new target type is ported by re-deriving the list in 3.0.3 (REQ-38). Generality is shown only by the planted and hold-out results (REQ-21, REQ-37, D5).
5. **Where does model judgement stay, and what stops the pre-pass becoming a second source of false positives?** The model keeps every OK, PROBLEM or UNSURE call and every claim. The script never writes a claim. OK is the default. PROBLEM needs two quotes or a search result. Unsupported PROBLEM rows are demoted to non-blocking. A blocking finding needs the CB-3 sentence (3.0.2, 3.0.5, REQ-16). Gate D4 limits wrong blockers.

### Recommendation

Run both redesigns in the section 5 experiment. Build the shared scaffolding of 3.0 first, because both need it. Adopt by the pre-registered rule of section 5. If neither redesign passes, keep Z0.

---

<!-- Source: Base (original, modified) - V2 section 5 (hold-out, cautions, gates), with the arms, consistency definition and gates of Variant 1 section 5, the statistics of Variant 3 section 4, and the refactoring plan's Appendix A9 (arms, runs, gates verbatim); INV-001, 003, 004, 009, 013 -->
## 5. Validation experiment

The design was derived from the three study packages. **The three study packages are never evidence for adoption.** They are re-run once as a derivation-set check, reported and never used for a decision. Every decision below uses hold-out material, planted material and the documentation arm.

<!-- Source: Base (original, modified) - V2 section 5 material table, relabelled HO-1..HO-6 (key in section 2); investigation labels from IG section 4 in brackets; planted set per INV-009; documentation arm per Variant 1 section 5 -->
### 5.1 Hold-out material

None of this material comes from the three study packages.

| Label | Material | Size | Use |
|---|---|---|---|
| HO-1 [IG H5] | docs-only plan | 11 items, about 1 hour | Stage 1, decision |
| HO-2 [IG H2] | plan | 4-8 items | Stage 1, decision |
| HO-3 [IG H4] | plan | 12 items | Stage 1, decision |
| HO-4 [IG H3] | larger plan | 9 important findings, about half a day | Stage 1, decision |
| HO-5 [IG H1] | spec with a validated 44-defect ledger (use the 20 blocking rows); tuned on by earlier work, not by these designs | 20 rows | Stage 2, spec target |
| HO-6 [IG H6] | sanity set | 3 items | In no decision |
| Planted set | 6 full-size real plans with at least 8 competing candidates per class, and one planted defect per class (C1-C8) written by an author who has not seen the recipes or extractors | up to 8 planted defects per plan | Stage 2, fresh-material generality and detector recall (INV-009) |
| Clean twins | The same 6 plans without the planted defects | 0 defects | Stage 2, false-positive rate |
| Documentation arm | About 8 delivered documents that carried a false universal sentence and a recorded retry finding, reviewed at the commit before the fix. Recoverability of that text from git is checked first. | about 8 documents | Stage 2, documentation target |

Ground truth for HO-1 to HO-5 is written from existing review reports and plan quotes, by someone who has not seen the recipes or extractors. It is written and hashed before the first arm runs and is never placed in a sandbox (REQ-34, REQ-36). A recorded implementation outcome sets the `blocking` flag.

### 5.2 Cautions

- Remove `.dev/reflect/`, `artifacts/` and `progress.md` from every sandbox, so no reflect report remains (REQ-04).
- Verify that the reviewed plan equals the plan in the package (sha256 against the ledger line). This is UNVERIFIED and must be checked before the first arm.
- Ground truth taken from Tier-2 reviewers is capped at what those reviewers found. "Missed by cheap panels" is therefore measured by running the cheap panels, not read from the reports.
- Recipes, cards, extractors and regexes are frozen by git tag before the hold-out ground truth is written, and authors never copy report wording (REQ-33).
- All arms in a stage run in block-randomised order, one block per replicate, to cancel gateway load drift.

### 5.3 Arms

| Arm | Description |
|---|---|
| **Z0-raw** | Current harness, no fixes. HO-1 to HO-3 only. Measures the harness share. |
| **Z0** | The isolated ember + 2x luna panel with H1-H4 and CB-1 to CB-5. The control to beat and the named time baseline. |
| **K** | Z0 plus one paragraph naming the eight checks in plain words. No recipes, no sheet, no ledger. Tests whether recipe or script machinery beats a plain checklist. |
| **SS** | Redesign 1 (Sweep Sheet) plus the fixes. |
| **RL** | Redesign 2 (Recipe Ledger) plus the fixes. |
| Zh, SSh, RLh | The same Z0, SS and RL arms on haiku + 2x luna (adaptation). |
| Zs, SSs, RLs | The same arms on sonnet + 2x luna (comparison only). |

### 5.4 Runs

One run is one panel run on one package. Each panel run has 3 reviewer runs.

| Stage | Set | Arms | Per document | Runs |
|---|---|---|---|---|
| 1 (decision) | HO-1 to HO-4 (4 documents) | Z0, K, SS, RL (4 arms) | 5 | 4 x 4 x 5 = 80 |
| 1 | HO-1 to HO-3 (3 documents) | Z0-raw | 5 | 3 x 5 = 15 |
| **Stage 1 total** | | | | **95** |
| 2 (only for arms that pass D1, D2 or D3 on Stage 1) | Planted, 6 plans | Z0, SS, RL | 3 | 6 x 3 x 3 = 54 |
| 2 | Clean twins, 6 plans | Z0, SS, RL | 2 | 6 x 3 x 2 = 36 |
| 2 | Spec, HO-5 | Z0, SS, RL | 5 | 1 x 3 x 5 = 15 |
| 2 | Documentation, 8 documents | Z0, SS, RL | 3 | 8 x 3 x 3 = 72 |
| 2 | Haiku, 4 documents | Zh, SSh, RLh | 3 | 4 x 3 x 3 = 36 |
| 2 | Sonnet, 3 documents | Zs, SSs, RLs | 2 | 3 x 3 x 2 = 18 |
| **Stage 2 total** | | | | **231** (54 + 36 + 15 + 72 + 36 + 18) |
| **Grand total** | | | | **326 panel runs** (95 + 231), about 980 reviewer runs (326 x 3 = 978) |

The Stage 2 count is the maximum, for the case where both redesigns continue. One blind Opus judge scores each run-package against a frozen rubric. A second judge scores a 15% sample (REQ-43).

### 5.5 Pre-experiment checks (no arm)

1. A 5-run timing spike on luna. It measures the cost per item and per row and sets the fallbacks (6 items per luna; 12 rows per lens) (REQ-32).
2. A 5-run compliance spike per redesign: the `ledger_missing` rate and the quote validity (REQ-17).
3. The offline selection-recall measurement (SS only; gate G0).
4. Z0-raw against Z0, to replace the +0.14 harness estimate with a measured value.

### 5.6 How consistency is measured

- Reach rate per item = runs that found it divided by runs.
- **Consistent** = reached in at least 60% of runs (3 of 5).
- Primary metric: the share of hold-out items that are consistent, per arm.
- Secondary: found fraction per run; share of runs that find at least half the items; run-to-run Jaccard of the found sets; stable-hit rate; wrong blockers per run; found-any against found-blocking; non-probe findings per run; elapsed; tokens; kills; retries; fallbacks; per-class reach with Wilson intervals.
- The bootstrap resamples packages first, then runs.
- Planning probabilities are replaced by the measured stage rates of 3.0.8.

### 5.7 Pre-registered gates

Arms, run counts, the consistency definition, the gates, the selection-recall floor and the per-class act bands are committed before the first hold-out run (REQ-41, REQ-44). All gates compare with Z0, pooled over HO-1 to HO-4 unless stated.

| Gate | Applies to | Criterion versus Z0 |
|---|---|---|
| **G0 offline** | SS: selection | Selection recall at or above the pre-registered floor, and the rank function beats a random pick on the derivation plans |
| **G0 offline** | Both: ledger and time | `ledger_missing` at most 10%, and the luna cost per item or row below its break-even |
| **D1 time** | Primary and haiku panels | Per-package median elapsed at most 1.35 x Z0's median; 90th percentile at most 1.50 x; kills at most 10%; intention-to-treat |
| **D2 effect** | Pooled | Mean found fraction at least Z0 + 0.12 absolute, with the 90% bootstrap lower bound above Z0 + 0.04 |
| **D3 consistency** | Pooled | Consistent items at least Z0's count + 3 |
| **D4 precision** | Pooled | Wrong blockers per run at most Z0 + 1.0, and blocking findings on clean twins at most Z0 + 0.7 |
| **D5 generality** | Planted set, documentation arm, HO-5 | Planted detection at least 0.40 on at least 3 of the 5 general classes (C2, C4, C5, C6, C8) in plans. Spec generality rests on HO-5 and on the spec fixtures of REQ-37; no planted spec is run. On the documentation arm and HO-5, D2 holds with the lower bound above 0, or the claim is withdrawn to plans only. |
| **D6 non-regression** | Pooled; blocking gate | Items Z0 reaches at 0.5 or more stay within 0.10 of Z0 |
| **D7 beats the checklist** | Against arm K | Gain over K at least 0.04 absolute on D2's metric, otherwise K wins |

### 5.8 Outcomes

| Result | Action |
|---|---|
| Neither redesign passes | Keep Z0. Report per-class results. |
| One passes | Adopt it. |
| Both pass | Adopt the one with the higher found fraction. If the difference is under 0.05, adopt Redesign 2 (Recipe Ledger), because it has no script to maintain. |
| K within 0.03 of RL | Report that recipe wording adds nothing over plain words, and adopt the cheaper form. |
| Z0 minus Z0-raw | Replaces the +0.14 harness estimate. |
| Measured act rate per class | Replaces every planning probability in 3.1 (d) and 3.2 (d). |

### 5.9 Power note and derivation-set note

- **Power is low.** The Stage 1 decision sets hold about 36-40 items (HO-1 11, HO-2 4-8, HO-3 12, HO-4 9), with 5 runs per document and 4 packages. A pass is evidence, not proof.
- **Derivation set.** The three study packages are re-run once as a derivation-set check. The result is reported and never used as evidence for adoption.

---

<!-- Source: Base (original, modified) - V2 section 6 grouped tables, with the Test column and grouping of Variant 1 section 6, the determinism and parse tests of Variant 3 section 5, and the refactoring plan's Appendix A10 (REQ-01..REQ-46 verbatim) -->
## 6. Numbered testable requirements

There are 46 requirements, REQ-01 to REQ-46, in eight groups. Each has a test.

### 6.1 Harness and brief

| # | Requirement | Test |
|---|---|---|
| REQ-01 | The brief names the source only when a source file exists; otherwise it logs `no_source` and C2 is not applicable. | Render with and without a source |
| REQ-02 | The merge truncates anchor and anchor2 to 200 and claim to 300 characters (a prefix of an exact quote) and validates with the real parser. | A 250-character anchor survives |
| REQ-03 | The sandbox is built at the plan's base commit, or the recorded working tree for documents without a commit. | A file created by the implementation is absent |
| REQ-04 | The sandbox holds no `.dev/reflect/`, `artifacts/`, `progress.md`, no report about the package and no ground truth. | `find` and `grep -r` |
| REQ-05 | CB-1 to CB-5 are present verbatim; the grading rule, the six findings categories and the judge are unchanged. | String match, set equality, sha256 |

### 6.2 Registry and ledger

| # | Requirement | Test |
|---|---|---|
| REQ-06 | The eight cards validate against the schema; each recipe is at most 120 words; each card has at least 2 instances outside the study packages. | Schema check and word count |
| REQ-07 | The lint fails on any 4-word sequence from a ground-truth description or plan quote, and on any package, task or file name. | A real run and a seeded leak |
| REQ-08 | The swap test and a second-author review are recorded per card. | Review record |
| REQ-09 | Rendered briefs hold no `src/superclaude/` path. | `grep` |
| REQ-10 | A new class is one card plus an optional extractor, with no dispatcher change. | A fixture card |
| REQ-11 | Findings may carry `class`, `probe` and `src`; the existing merge tests pass. | The suite run with extra keys |
| REQ-12 | (a) On failure of the pre-pass or the lens render, the harness runs the isolated brief and records `fallback=true`. (b) On failure of the post-run ledger check, the harness merges the findings block as written and records `check_skipped=true`. | A forced exception in each of the three components; assert the isolated brief for (a) and the as-written merge for (b) |
| REQ-13 | The ledger is a `ledger-v1` JSON-lines block in the final message, directly above the single findings block; both blocks are parsed by a real parser, not by the fence-opener grep. | Reports with misplaced, duplicated or truncated blocks |
| REQ-14 | Substring checks use the same flattening as `findings.py`. | A quote that wraps a plan line |
| REQ-15 | The promotion function copies the reviewer's own `problem`, takes the plan-side anchor, validates with `_check_finding`, inserts inside the single block, tags `src=ledger`, MINOR and non-blocking, and logs and skips on failure. | Ids over 16 characters, short anchors, duplicate ids |
| REQ-16 | Unsupported PROBLEM rows are demoted to non-blocking; blocking needs the grading sentence plus two quotes or a search result. | Unit test |
| REQ-17 | The `ledger_missing` rate from the compliance spike is at most 10% before any arm. | Spike report |

### 6.3 Redesign 1: Sweep Sheet

| # | Requirement | Test |
|---|---|---|
| REQ-18 | The pre-pass is a non-model, read-only script, byte-identical for the same input and seed, run serially, and killed at min(15 s, 0.10 b) with fallback. | Run twice and compare bytes; a sleeping stub |
| REQ-19 | The sheet has at most 12 items; quota 1-2 per triggered class with ranked fill; all candidates and dropped items are logged with the seed. | A fixture with 200 set-word sentences |
| REQ-20 | Assignment runs over 24 slots with caps summing to 24, replica 1 for items without attached tool output, no growth in the survivors' load on failure, and order shuffled per reviewer. | Assignment unit test |
| REQ-21 | Extractors E1-E4 and E7 reach recall of 0.8 or more on at least 3 non-study plans with seeded defects, with precision reported; E6 is labelled experimental. | Fixture suite |
| REQ-22 | The offline selection-recall gate is met, and the rank function beats a random pick on the derivation plans. | Gate script |
| REQ-23 | An empty sheet leaves the brief equal to Z0's. | Hash |
| REQ-24 | Search scope is tests, root documents and named paths, with `.dev/` excluded and a time bound. | Timing on the largest tree |

### 6.4 Redesign 2: Recipe Ledger

| # | Requirement | Test |
|---|---|---|
| REQ-25 | The eight recipes live in one file and are quoted verbatim by lens; at most 4 per reviewer; the duplicated classes are C2 and C4 on the primary panel, C1 on the haiku panel, and C1 and C7 on the sonnet panel (lens table of 3.2(a)). | Parse the generated briefs of each panel and compare the duplicated classes with the lens table |
| REQ-26 | There is a row budget per recipe and at most 14 rows per lens; `NONE FOUND` is allowed. | Ledger check |
| REQ-27 | There is no luna re-ask; an ember re-ask runs only if `now + 30 s <= 1.35 b`. | Fake clock |
| REQ-28 | The `ran` field is cross-checked against transcript tool calls in the analysis. | Analysis script |

### 6.5 Time

| # | Requirement | Test |
|---|---|---|
| REQ-29 | The +35% limit is judged on per-package medians against same-day Z0 in the same randomised block, with one panel clock from before the pre-pass; mean and median are reported. | Timing log |
| REQ-30 | The hang guard is 1.5 x (b + expected overhead) from launch; kills and retries are reported per arm; killed or retried reviewers are scored as zero findings. | Sleeping stub; analysis |
| REQ-31 | The break-even values (pre-pass 14 s and 2.75 s per item at b = 100; row cost 2.07 s) are in the report with the measured values. | Report check |
| REQ-32 | A 5-run luna timing spike precedes every arm and sets the fallbacks (6 items per luna; 12 rows). | Spike record |

### 6.6 Contamination and overfitting

| # | Requirement | Test |
|---|---|---|
| REQ-33 | Recipes, cards, extractors and regexes are frozen by git tag before the hold-out ground truth is written. | Tag date earlier than the ground-truth commit |
| REQ-34 | Reviewers never receive ground truth; hold-out sandboxes exclude reflect reports. | `grep` |
| REQ-35 | Leave-one-class-out ablation changes the other classes' reach by at most 15 points. | Ablation report |
| REQ-36 | Hold-out ground truth is written and hashed before the first arm; planted defects are authored by someone who has not seen the recipes or extractors; every planted plan has a clean twin. | Hash times; attestation |

### 6.7 Applicability

| # | Requirement | Test |
|---|---|---|
| REQ-37 | Spec and documentation fixtures exist: E1, E2 and E5 produce items on a spec fixture; E4 and E1 on a documentation fixture. | Fixtures |
| REQ-38 | The registry README lists, per target type, what must be re-derived (block patterns, command dialect, test and root-document paths, severity guidance, the location of truth). | Document review |

### 6.8 Reporting and validation

| # | Requirement | Test |
|---|---|---|
| REQ-39 | All metrics come from one script over the run folders. | Fixture |
| REQ-40 | Gains are reported as H share, prompting share (K minus Z0) and redesign share, never summed in a headline. | Report check |
| REQ-41 | Reach is logged per stage (extraction, selection, act, merge survival, judge credit), and the per-class act-rate bands are pre-registered. | Log schema |
| REQ-42 | Displacement is measured as non-probe findings per run, and D6 is a blocking gate. | Analysis |
| REQ-43 | The judge is a blind Opus with a frozen rubric, a second judge on 15%, and an API-error audit per batch. | Audit log |
| REQ-44 | Arms, run counts, the consistency definition and the gates are committed before the first hold-out run. | Commit order |
| REQ-45 | Claims are worded "raises the per-run found fraction; consistency is expected only for I4 and I7 (classes C4 and C8), and only for Redesign 1 at the high end of its range". | Report review |
| REQ-46 | The optional verifier never sits on the critical path, cannot add claims, and its time is excluded from every figure. | Timing log |

---

<!-- Source: Base (original, modified) - closing paragraphs of Variant 1, Variant 2 and Variant 3 merged per refactoring plan Change 12; facts from invariant-probe.md -->
## Not checked and unverified

- All probabilities, act ranges and selection factors in 3.1 (d) and 3.2 (d) are planning values built from cited counts. None is a result. Section 5 replaces each with a measured rate.
- The speed of 48 tokens per second is derived from one luna run (4.9k tokens in 102 s) and is unconfirmed.
- The cost of 2 s per item or row, the pre-pass time of 8 s, the ledger compliance rate and the implementation line counts are unmeasured.
- The launcher facts (only the final result message is kept; the block check tests only the fence opener) and the `findings.py` rules (id length, anchor and claim limits, one block, MINOR not blocking) were read in the source and are cited with line numbers.
- That unknown telemetry keys (`class`, `probe`, `src`) are accepted by the merge comes from the hand-off table. A test with the real merge must confirm it (REQ-11).
- That the reviewed plan equals the plan in each package (sha256) is unchecked (section 5.2).
- The 348 s figure is a per-run mean summed over three packages (COMBO-REPORT final table). The gate uses per-package medians of a same-day Z0 arm, so the planning values of 3.1 (c) and 3.2 (c) are stand-ins only.
- The harness share of +0.14 (0.03-0.34) is a bottom-up estimate from the first brainstorm. The 0.1 overlap on I4, I1 and B5 is not removed.
- The best single panel run recorded is 4 of 14, so the high ends of both gain ranges (4.8 and 4.5) are optimistic.
- None of the wording of CB-1 to CB-5, the ledger rule, the sheet block, the question templates or the recipes has been run on any model.
- The power of the experiment is low. A pass is evidence, not proof.

---

<!-- Source: Base (original) - provenance summary written by the merge executor from the refactoring plan (Changes 1-16) and invariant-probe.md -->
## Provenance summary

| Section | Base | Incorporated sources |
|---|---|---|
| Frame and conventions | Variant 2 header | Variant 1 conventions block; debate label rules (HO-1..HO-6, SS, RL, Z0, K) |
| 1. Theories | Variant 2 section 1 (table, issue-to-cause map, rejected rival) | Variant 1 section 1 number tables and mapping of redesigns to theories |
| 2. Defect classes and generality | Variant 2 section 2 table | Variant 1 section 2 (strength, review targets); Variant 3 section 2 (issue instances); IG section 4 (HO key) |
| 3 head (distinctness, open question) | Variant 2 section 3 intro | Debate Q1 and Q5 |
| 3.0 Shared scaffolding | Variant 1 section 3.0 | Variant 2 shared brief changes (CB-1 to CB-3); Variant 3 section 3.3 and parse rule; INV-001, 002, 004, 005, 007, 008, 012, 013, 014; anti-overfitting union (Variant 1, 2, 3) |
| 3.1 Redesign 1: Sweep Sheet | Variant 2 Redesign 1 | Variant 1 extractors E1-E7, failure rows and AO list; Variant 3 determinism and shuffle seed; Appendix A2, A4, A5a, A6-A8; INV-001, 003, 004, 006, 008, 011, 012, 013, 014 |
| 3.2 Redesign 2: Recipe Ledger | Variant 2 Redesign 2 | Variant 1 recipes and search-form line; Appendix A3, A4, A5b, A6-A8; INV-002, 007, 010, 014 |
| 4. Comparison | Variant 2 section 4 | Variant 1 section 4 rows; Appendix A values (recomputed, not copied from the variants) |
| 5. Validation experiment | Variant 2 section 5 | Variant 1 arms, gates and consistency; Variant 3 statistics; Appendix A9; INV-001, 003, 004, 009, 013 |
| 6. Numbered testable requirements | Variant 1 section 6 (grouped tables with a Test column) | Variant 2 section 6; Variant 3 section 5; Appendix A10 (REQ-01..REQ-46) |

Invariant findings: 14 of 14 are resolved in this document. Each row gives where the resolution lives.

| Finding | Resolution lives in |
|---|---|
| INV-001 selection recall | 3.0.8, 3.1(a) offline selection-recall gate, 5.7 (G0), 6 (REQ-22) |
| INV-002 ledger in the final message | 3.0.4, 6 (REQ-13, REQ-17) |
| INV-003 time arithmetic and break-evens | 3.1(c), 3.2(c), 5.7 (D1), 6 (REQ-29, REQ-31, REQ-32) |
| INV-004 consistency claim narrowed | 3.0.8, 3.1(d), 3.2(d), 6 (REQ-41, REQ-45) |
| INV-005 promotion rules | 3.0.5, 6 (REQ-15) |
| INV-006 matrices recomputed once | 3.1(d), 3.2(d) |
| INV-007 format-induced demotions | 3.0.4, 3.0.5, 6 (REQ-14) |
| INV-008 hang guard | 3.0.7, 3.1(c), 3.2(c), 5.7 (D1), 6 (REQ-30) |
| INV-009 planted defects in full-size plans | 5.1, 5.7 (D5), 6 (REQ-36) |
| INV-010 row budget, no luna re-ask | 3.2(a), 6 (REQ-26, REQ-27) |
| INV-011 assignment over 24 slots | 3.1(a) step S3, 6 (REQ-20) |
| INV-012 serial pre-pass | 3.0.7, 3.1(a) step S1, 6 (REQ-18) |
| INV-013 no source or no base commit | 3.0.1, 3.0.2 (CB-1), 3.0.7, 6 (REQ-01, REQ-03) |
| INV-014 displacement and free-review floor | 3.0.2 (CB-5), 3.1(f), 3.2(f), 5.7 (D6), 6 (REQ-42) |

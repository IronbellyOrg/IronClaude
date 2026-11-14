# Requirements specification: class-keyed redesigns of how the tasklist review panel operates

Variant 2 of 3. Persona: analyzer. Lens: root cause and evidence for architecture.

Conventions. `EVAL` = `.dev/eval-workspaces/tasklist-review-panel/20261111-a1`. `BR` = `.dev/brainstorms/20261113-223124-panel-process-redesign`. Evidence files: `BR/seed-brief.md` (seed), `BR/enrichment/investigation-generality.md` (GEN), `BR/enrichment/research-external.md` (EXT), `BR/enrichment/reused/investigation-designspec.md` (DS), `.../investigation-alias-control.md` (AC), `.../investigation-patterns.md` (PAT). Issue ids B1-B8 and I1-I8 are the labels in `EVAL/COMBO-REPORT.md` lines 401-417. Nine of the ten missed issues (B1, B2, B5, B6, B8, I1, I4, I5, I6) lie inside the "14". I7 sits on the control package (scored out of 2). It is analysed below but kept out of every "found out of 14" sum.

Out of scope for this file: nothing is edited or created. All probabilities are planning values built from the cited counts. Every one is replaced by a measured value in section 5. None is a result.

---

## 1. Theories

I accept all three seed theories, sharpen each against the numbers, and reject one alternative.

| # | Theory (refined) | Evidence | Instruction or process change it implies |
|---|---|---|---|
| T1 | Reviewers verify what the plan names. Nobody sweeps for what the plan does not name (reverse dependencies, other copies of a claim, other members of a quantified set). Search volume is not the variable; search direction is. | Runs that touched an unnamed test file: sonnet 35%, grok 33%, ember 8%, luna 1%, haiku 0% (PAT §1). The unnamed test file was opened in 0 of 176 cheap control runs. 7 of the 8 runs that opened it found I7; 0 of 225 that did not (PAT §4). Haiku searches `tests/` in 81% of runs yet 0 of 25 left the test file the plan names (PAT §1). Ember searches `tests/` in 49% of runs and opened 0 unnamed test files. The changelog was touched in 1 of 233 designSpec runs and I5 was found 0 times. The one reviewer that saw the stale claim (grok) dropped it as "minor" (DS §3). | The reverse sweep must be done for the model (a script) or forced as a written step with a literal command template. "Be thorough" does nothing: the sweep never runs without a unit of work. |
| T2 | Right place, wrong question (T2a), or never reached (T2b). The root cause is that nothing in the process gives a reviewer a structural unit of coverage. Attention goes to salient text and asks one local question there. | T2a: 16 cheap findings anchor the exact I5 sentence and all ask the same over-match question (DS §2c). 3 findings anchor the B5 mapping and analyse only one input case. 1 finding anchors the I1 row and asks a different question. T2b: 0 cheap findings on I4's criterion. 0 findings anchor B1 or B2 in any of 98 cheap reports, and 3 reviewers wrote that those items were "deferred". Attention is concentrated: a model's top-3 tasks take 38-91% of its anchors (PAT §3). Luna reaches the B1/B2 task in 10% of runs, the I5 task in 6%, the I4 task in 2%. Its run-to-run Jaccard on designSpec is 0.12. Ember reaches the B1/B2 task in 52% of runs but matches B1 in 3%. | Replace salience with an enumerated item list built from document structure (sentences that quantify, criteria with commands, constraints, dictated text, edited files). Give each item a class-keyed question that includes satisfiability and the opposite direction. Make the answer a written ledger line. |
| T3 | The evidence environment and the reporting filters hide or suppress defects. This is a confound on every measured number. T3a is environment. T3b is suppression. | T3a: the sandbox is a post-implementation checkout that already repairs B5, I1, I4 and part of B8 (DS top, AC §1). 44 of 98 alias reviewers saw the narrowed sentence and did not compare it. Source.md went unread in 156 of 665 runs (ember 39%, luna 22%). T3b: the merge drops findings over 200/300 characters (80 reviewer-level cases, 49 blocking findings lost, HANDOFF run2 R20). The Medium rule and the lack of a missing-task category push stated-claim staleness to "minor", and all 7 true I7 finds were non-blocking (PAT §4). | Harness fixes H1-H4 (seed). Plus one brief rule: every defect found must be listed as a finding, severity graded separately. H1-H4 alone are worth about +0.14 of 14 (0.03-0.34); see 3(f). |
| Rejected: reasoning budget | More thinking is not the lever for these ten issues. | Across 7 models, median thinking tokens correlate with hits (rho 0.64). Inside ember and luna, hard-issue hits do not rise with thinking (ember 0.25 to 0.22, luna 0.09 to 0.09 per run). Haiku thinks 45.8k tokens and still never opens the unnamed test file (PAT §6 Theory A). | Do not buy the fix with longer thinking or more passes of the same prompt. Spend the idle seconds on distinct items and distinct classes. |

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

---

## 2. Defect classes and generality

Class statements contain no package, task, file or ground-truth wording. Recurrence counts are distinct other documents outside the three eval packages (GEN §2, §5). Caveats that apply to all rows (GEN §5.4): one repository, one owner, one plan pipeline; phrase-search lower bounds; the records show the class exists, not that cheap panels miss it.

| Class | Definition | Recurrence outside the eval | Strength | Review targets it applies to |
|---|---|---|---|---|
| C1 | A criterion asks for a complete or exhaustive result over a set with no bounded method or stopping rule, or the criterion's scope differs from the scope of the instruction it checks. | 3 documents (plans and a spec), all symptoms: new items each review round, a closed list used against an open set (GEN §2 C1). | Supported, symptom-level. No other criterion worded as a provable inventory was found. | Plans, specs ("shall list all"), documentation ("covers every case"). |
| C2 | A rule stated in the driving document is not carried into the plan's task text or criterion. | 6 plans, all with a source line against a plan line (GEN §2 C2). | General | Plan vs source; spec vs parent requirement; docs vs code behavior. |
| C3 | A value, field or state is read, mapped or required by one component and no row, task or step writes it for that case. | 3 documents: 1 blocking, 1 inferred, 1 low. The exact lookup-table shape was not found elsewhere (GEN §2 C3). | Weak. Plausible only. | Specs with state tables, plans that implement them, data-flow docs. |
| C4 | A criterion embeds a command, pattern or test selector whose literal form cannot match or cannot pass against the text or state the same plan orders. | 9 documents, 8 plans: a grep returning nothing on ordered text, a regex that never matches, a selector that skips checks (GEN §2 C4). | General | Plans, test plans, runbooks, documented commands. |
| C5 | After a change, a count, claim or copy in a second location is left stale because no task enumerates that location. | 9 documents (3 plans, 6 delivered texts) (GEN §2 C5). | General | Plans, changelogs, mirrored copies, docs, comments. |
| C6 | A sentence says "all", "only", "never" or "outside X nothing", and an inventory, the plan's other tasks or the scope of the enforcing test contradict it. | 12 documents (4 plans, 8 delivered docs) (GEN §2 C6). | General, mostly delivered docs | Any text with universal claims: plans, docs, specs. |
| C7 | Verbatim text the plan dictates omits a clause of a constraint stated elsewhere, or contradicts the plan's own criterion. | 5 plans in the broad form. 1 in the narrow one-clause form (GEN §2 C7). | General broad, weak narrow | Plans with templates, specs with message formats, docs with required wording. |
| C8 | A plan edits files or behavior that a test elsewhere pins, with no task that updates or runs that test. | 6 documents, 5 plans (GEN §2 C8). | General | Plans, change specs, refactor proposals. |

The ten are not special. Seven further classes recur about as often (X1-X7 in GEN §3: tests that pass on old code, stale citations, conflicting source statements, task ordering, missing baseline, no failure route, count broken by a forced step). Both redesigns are built so a new class is added as one more recipe or one more extractor, with no change to the harness.

External support that the classes are general (EXT §2): ISO/IEC/IEEE 29148 quality characteristics (verifiable, feasible, complete, consistent, singular) map onto C1-C8. The requirements-smell literature has an "open-ended, non-verifiable term" smell next to C1. No catalogue entry was found for "universal claim unchecked against the corpus" (C6). Smell detectors ran at 59% precision and 82% recall, so detector output needs a model filter (EXT §1.5).

External support for the levers (EXT §5; adjacent evidence only, several snippets UNVERIFIED):
- A tool narrows the question and the model judges one item (static tool plus model hybrid removed 94-98% of false alarms, 2-110 s per alarm).
- A checklist alone does no better than ad hoc reading in human inspections; a detection recipe per class is what helped (scenario reading about +35%, replication mixed).
- Parallel same-model passes raise recall and plateau near 5 passes. Majority voting can backfire on small models, so use a union and verify with a quote.
- Sequential multi-turn decomposition cost +187% compute in one study, so neither redesign uses it.
- Showing a reviewer another model's conclusions causes herding, so reviewers stay blind to each other in both redesigns.

---

## 3. The two redesigns

Both redesigns keep reviewers read-only, keep the findings-v1 merge contract (ledger lines sit in the report body above the findings block; the merge reads only the block), never expose ground truth, and apply to every arm after the harness fixes H1-H4 from the seed. I reuse H1-H4 and their gain table from the first brainstorm (`.dev/brainstorms/20261113-163248-panel-collaboration/merged-requirements.md` lines 311-350). Justification: the fixes are given in the seed brief itself, are independent of any redesign, and their estimate rests on counts (92 dropped findings, 39% and 22% source skips) that this brainstorm also uses. I reuse nothing else from the first brainstorm. Reviewer-to-reviewer messaging is not used. External evidence on herding argues against it, and the idle-time budget is spent on distinct items instead.

The two redesigns answer the seed's open question from opposite sides:
- Redesign 1 puts the sweep in a script and leaves the model judgement only.
- Redesign 2 puts the sweep in written recipes and leaves the model to run it.

### Shared brief changes (both redesigns, quoted)

| ID | Draft wording | Purpose |
|---|---|---|
| CB-1 | "Driving document: {{SOURCE_ABS}}. Read it in full before you review the candidate. A rule it states that the candidate does not carry is a finding." | H1; fixes source-blind runs (T3a) |
| CB-2 | "Every ledger line you mark DEFECT or UNSURE must also appear in the findings block. Set its severity with the grading check. A finding that is not blocking is still listed, as MAJOR or MINOR with blocking false. Do not leave a defect out because it looks small." | Removes suppression (T3b). The grading rule itself is unchanged, so blocker precision is not moved by a rubric edit. |
| CB-3 | "A tool line or a recipe step is a fact or a question about the text. It becomes a blocking finding only if you can write the sentence 'An implementer who follows the stated text as written builds X, and X is wrong because Y.'" | Keeps wrong blockers from growing |

---

### Redesign 1: Sweep Sheet (a script does the sweeps, the model judges items)

**(a) Mechanism and exact order of steps.**

Step S0. Harness fixes H1-H4 (pre-implementation sandbox, no leak, source named, anchor normalizer). Unchanged cost.

Step S1. A deterministic pre-pass script reads the candidate and the sandbox repository and writes `sheet.md`. It uses no model and no ground truth. It has six extractors:

| Extractor | Class | What it extracts (generic) | Tool output attached |
|---|---|---|---|
| Q | C1 | Criterion lines containing every, all, each, complete, exhaustive, found, covers, no remaining. | The instruction sentence in the same task, and both sets of named paths or items side by side. |
| U | C6 | Sentences containing all, only, never, no other, outside X nothing, in dictated text or Goal. | Scope-limiting phrases elsewhere in the plan that mention the same path or test (skip, ignore, exempt, allow-list, only), plus the enforcing test the plan names. |
| M | C4 | Criteria with a backticked command, pattern or selector, and each double-quoted name or heading the same task orders. | The literal pattern tried, case-sensitively, against each ordered string (MATCH or NO MATCH). For a test selector: tests collected out of tests in the named file. |
| R | C8 | Paths the plan edits or creates. | `git grep -l` of each path and its distinctive strings over `tests/`, scripts and docs; the referencing files the plan never names; whether the plan's gate names them. |
| S | C5 | A number, name or quoted claim the plan says will change or must "no longer" appear. | Whole-tree `git grep -F` hits, including root-level documents, changelogs and mirrors, split into plan-named and plan-unnamed files. |
| K and X | C7, C2, C3 | K: each constraint split into clauses, matched to dictated text on the same topic. X: source sentences with must, shall, never, only, halts, reports, returns, or a table row, matched to candidate sentences in the same task. | K: a clause-by-text grid for the highest-overlap constraint. X: the source rules with the lowest co-occurrence of their own identifiers inside one task. |

Caps and order: at most 12 items in total (Q 2, U 2, M 2, R 2, S 2, K 1, X 1). Item order is shuffled per reviewer (EXT §4 anchoring). A script that finds nothing writes an empty sheet, and the panel then equals the isolated baseline.

Step S2. The harness splits items so that each item goes to two of the three reviewers (blind to each other), about 8 per reviewer, with at most 6 for the slowest model. Tool-heavy items go first to the model that reads tool lines best, and reading-heavy ones (Q, K, X, M) to reviewers that read whole files (luna).

Step S3. The reviewers run in parallel with the baseline brief plus the sheet block below. Each writes `## Check ledger` first, then reviews freely for the time left, then the findings block.

Step S4. A post-run script checks the report: every sheet item assigned to that reviewer has a ledger line, every DEFECT or UNSURE line has a finding, and every quote is an exact substring of the candidate or of a tool line. A missing or fake line is flagged. There is no re-ask (time).

Step S5. The normal merge (anchor and claim normalizer from H2, then `superclaude review merge`).

Quoted draft wording for the sheet block (appended to the baseline brief, after CB-1 to CB-3):

> "SWEEP SHEET. A script, not a model, built {{SHEET_PATH}} from the candidate and the repository. Each item has an id, a location, the literal text, and tool output. The tool output is a fact about text. Your job is to judge it. Read the candidate and the driving document first, then the sheet. For each item assigned to you, in the order shown, write one ledger line: `S<id> | OK or DEFECT or UNSURE | <12 words: what you checked> | <exact quote from the candidate or the tool line>`. For OK, say what you looked at. Do not skip an item. When the ledger is done, review the candidate as you normally would with the time that remains. Put the ledger under the heading `## Check ledger` above the findings block."

Question templates the script prints under each item (generic):

| Kind | Printed question |
|---|---|
| Q | "What finite check would let a reviewer say yes to this criterion, and when does it stop? Do the instruction line and the criterion cover the same set?" |
| U | "Name the set this sentence covers. Find one member it leaves out or contradicts: look at the plan's other tasks, at what the enforcing test skips, and run one count or listing command over the tree." |
| M | "Apply the criterion's literal pattern to the text this task orders. Does it pass on that text? Do not use the current file as evidence; it may already contain the finished work." |
| R | "Open the referencing file the plan never names. Does it pin the text or behavior being changed? Does any task update or run it?" |
| S | "Is each plan-unnamed hit false after the change? Does any task edit or check it?" |
| K | "Does each dictated text carry every clause of this constraint? Tick each clause." |
| X | "Does the candidate carry this rule, including each condition and failure path? Quote the carrying sentence, or mark DEFECT." |

**(b) Model roles.**

| Panel | Roles |
|---|---|
| Primary: ember + 2x luna | Ember (fast, a grep-checker): items R, S, U, and M with tool lines; 9 items. Each luna (reads whole files, almost no search): Q, K, X, M; 8 items each. Every item is judged by two reviewers. Ember's idle seconds fund its 9 items. |
| haiku + 2x luna | Haiku is the critical path (220-238 s) and thinks 45.8k tokens, so it gets the fewest items (6, tool-line items R and S only). Each luna takes 9 items. Luna is idle about 120 s, so the extra load is free. |
| sonnet + 2x luna | Sonnet is the critical path (259-302 s). It gets 6 items and does the unlisted extra sweeping it already does. Lunas get 9 each. |

**(c) Time budget per package.** Baselines from the seed: ember + 2x luna slowest-reviewer median 100-122 s per package (mean 116 s; 348 s over 3 packages); haiku + 2x luna 220-238 s (715 s over 3); sonnet + 2x luna 259-302 s (821 s over 3). Cap = 1.35 x baseline.

Primary panel, ember + 2x luna, critical path = pre-pass then slowest luna:

| Step | Seconds | Note |
|---|---|---|
| S1 pre-pass (script) | 8 (kill at 15) | On the critical path, before launch |
| S2 split and brief assembly | 1 | Script |
| S3 ember | 41 baseline + 3 + 9 items x 2 = about 62 | Under the critical path; idle time absorbs it |
| S3 luna | 100-122 baseline + 3 + 8 items x 2 = +19 | Critical path |
| S4 post-run check | 1 | Script |
| Critical path total | 128-150 s | |
| Elapsed increase | 150/122 = +23%; 128/100 = +28% | Cap is 135-165 s, so slack is 7-15 s |

The tightest cell is 128 s against a cap of 135 s. If the measured pre-pass exceeds 8 s, the sheet is cut to 10 items, or the sheet is built in parallel with each reviewer's first reads (the brief then says "the sheet appears at {{SHEET_PATH}} within 15 s; read the candidate first"), which removes the pre-pass from the critical path.

haiku + 2x luna: critical path haiku. Pre-pass 8 + sheet reading 3 + 6 items x 4 s (haiku's thinking makes lines slower) = +35 s. 220 + 35 = 255 s (+16%); 238 + 35 = 273 s (+15%). Cap 297-321 s.

sonnet + 2x luna: 8 + 3 + 6 items x 3 = +29 s. 259 + 29 = 288 s (+11%); 302 + 29 = 331 s (+10%). Cap 350-408 s.

Enforced versus expected:
- Enforced by a timer or structure: the pre-pass kill at 15 s; the 12-item cap; a harness panel deadline at 1.6 x baseline (a reviewer still running is killed and the merge proceeds without it, and the loss is reported).
- Only expected: the per-item judging seconds and the median elapsed. The +35% requirement is measured on medians over runs (section 5), because the natural run-to-run spread of one reviewer exceeds 35%, so a kill at exactly 1.35 x median would discard 25-40% of reports.

**(d) Defect-class coverage matrix.** Per-run probability that the issue appears in the merged ledger, with H1-H4 applied. Values are planning values (low-high). They already include two blind judges per item.

| Issue | Trigger (class mechanism) | Why a cheap model then reaches it | Per run |
|---|---|---|---|
| B1 (C1) | Q item shows the criterion with "every ... found" and asks for the finite check. Always extracted when the criterion carries the quantifier word. | Forced to write a finite check or admit none. Cheap models read the task as a strength unprompted (DS §2b); a question that needs a written stopping rule is a different move. Risk: bounded "every" criteria also trigger and cost false alarms. | 0.10-0.35 |
| B2 (C1) | Q item prints the task's instruction scope and the criterion's scope side by side. X may add the source's narrower scope. | A visual two-column comparison needs no search. | 0.15-0.40 |
| B5 (C2) | X item: a source rule whose own identifiers never co-occur in one task. | Sonnet found it with exactly the rule-by-rule move (DS §3). The sheet hands luna the rule, so the 39% source skip no longer matters. Misses if the identifier overlap is high. | 0.20-0.45 |
| B6 (C6) | U item: the "only X" sentence plus plan phrases about skips and exemptions, and the enforcing test's scope. | Luna already read the shared file and noticed the leftover lines (AC §3). The prompt names the test-scope comparison. The script cannot count the other selectors. | 0.05-0.20 |
| B8 (C6) | U item: the "all other" sentence plus the skip rule found elsewhere in the same plan. | The contradiction sits inside the candidate (AC §1). An inventory command stays with the model (one grep -c). | 0.10-0.30 |
| I1 (C3) | X item, only if a source table row is flagged. The extractor is weak. | The cross-table check is a move cheap models make only when handed both rows. | 0.03-0.15 |
| I4 (C4) | M item prints NO MATCH for the case-sensitive pattern against the ordered heading. Deterministic. | Reading a printed NO MATCH is easy. The script ignores the repaired checkout, and H3 removes it. | 0.50-0.75 |
| I5 (C5) | S item: the claim literal found in an unnamed root document. | The 15 ember findings that anchored this sentence already ran a grep. They asked the wrong direction. The sheet answers the other direction in tool output, and CB-2 forbids dropping it. | 0.35-0.60 |
| I6 (C7) | K item: constraint clauses against every dictated text on the topic. | Cheap models already made the sibling comparison on one task (AC §2) and stopped; the grid covers the other tasks. | 0.15-0.35 |
| I7 (C8, control) | R item lists the referencing test the plan never names. Always extracted. | Ember opens the file; haiku already saw the name in grep output 5 of 11 times. The sheet forces the open step. | 0.40-0.65 (of 1 on control) |

**(e) Broad applicability.**
- Other plans: the extractors key on sentence shapes and on backticks, quotes, paths and tables, not on any package. A new plan format needs a section map (where instructions, criteria, constraints and dictated text live) and an "edited object" detector.
- Specifications: Q reads `shall`/`must` lines; M reads examples and formats; K reads normative constraints; X compares a requirement to its parent requirement; R reads "affects" lists; S reads cross-references.
- Documentation reviews: U and S carry the load (8 delivered-document instances of C6 and 6 of C5 in GEN §2). The "source" is code or the changelog. M applies to documented commands.
- Re-derive per new target: section map, edited-object detector, location of truth (source, code, parent spec), command dialect, a pre-change snapshot of the repository.
- Anti-overfitting rules: AO-1, no sentence, identifier or file name from any ground-truth item appears in the script, its tests or the printed questions. AO-2, every question template must still read correctly after the domain nouns are replaced by placeholders (the swap test). AO-3, each extractor is justified by at least 3 recorded other-document instances (GEN §2); C3's is marked "plausible only". AO-4, extractor regexes and templates are frozen and hashed before the hold-out ground truth is read by the designer. AO-5, unit tests use synthetic fixtures written from the class definitions, not the three packages. AO-6, the script reads only the candidate and the pre-implementation sandbox, never ground truth or review output.

**(f) Expected gain out of 14 per run.**

| Block | Low | High | Basis |
|---|---|---|---|
| Baseline, isolated ember + 2x luna | 1.83 | 1.83 | Measured (seed) |
| Four harness fixes H1-H4 | +0.03 | +0.34 | Central +0.14 (first brainstorm table) |
| Redesign, gross, nine in-14 issues | +1.63 | +3.55 | Sum of section (d) rows B1 to I6, excluding I7 |
| Displacement of easy issues (B3, I2, B7) | -0.30 | 0.00 | Luna spends time on the ledger |
| Total | 3.2 | 5.7 | |
| Share from the redesign | 1.3 | 3.55 | The rest is H |

The high end exceeds every run observed (best single run 4/14). A measured total under 3.0 means the redesign failed its premise. About 55% of the gross gain comes from I4, I5 and B5, the classes with a mechanical trigger.

**(g) Overhead.**
- Elapsed: +23% to +28% on the primary panel (arithmetic in (c)).
- Output tokens: baseline 64k over 3 packages, about 21k per package. The ledger adds 8 lines x about 40 tokens per reviewer, plus more thinking; estimate +6-9k per package (+28% to +42%). Sheet input is about 3k tokens per reviewer. The script costs 0 model tokens.
- Judge cost unchanged.

**(h) Implementation effort.**
- New `tools/sweep-sheet.py`: about 400 lines (six extractors, caps, shuffle, split).
- Tests for it: about 250 lines on synthetic fixtures.
- Edit `tools/run-reviewer.sh`: about +30 lines (pre-pass call and kill, per-reviewer brief, post-run check).
- Post-run check `tools/ledger-check.py`: about 90 lines.
- Brief template in `src/superclaude/rules/prompts/document_review_loop_prompts.md`: about +25 lines for CB-1 to CB-3 and the sheet block.

**(i) Failure modes.**

| Failure | Effect | Control |
|---|---|---|
| Rubber-stamp: models answer OK to every item. About 41% of smell-detector items are non-defects, so OK is the right answer for many. | Gain near zero while time rises | Hold-out measures OK-rate on planted items; decision rule D2 |
| Extractor misses the item. | Class lost silently | Extractor recall measured on planted documents |
| Extractor over-extracts and the 12-item cap crowds out the real item. | Same | Rank by overlap; log dropped items |
| False-positive growth. Tool lines look authoritative. | More wrong blockers (baseline 1.83 per run) | CB-3, UNSURE is non-blocking, decision rule limit +1.0 wrong blockers per run |
| Pre-pass too slow on a large repository. | Time cap broken | Kill at 15 s and fall back to baseline brief |
| The sheet sees the wrong snapshot. | Wrong tool lines | H3 is a precondition (R-04) |
| Sheet becomes a leak path for ground truth. | Invalid study | AO-6 and a grep check in R-14 |

---

### Redesign 2: Recipe Ledger (written class recipes and a forced enumerate-then-judge ledger, no pre-pass)

**(a) Mechanism and exact order of steps.**

Step R0. Harness fixes H1-H4.

Step R1. The harness assigns each reviewer a lens: two to four class recipes, chosen by that model's measured habits. Shorter prompts per reviewer avoid context collapse in small models (EXT §1.4). Redundancy: C2 and C4 go to two reviewers.

Step R2. Reviewers run in parallel with the baseline brief plus CB-1 to CB-3 plus their recipe block and the ledger rule below. Order inside the reviewer: (1) read the candidate and the driving document; (2) run each assigned recipe step by step, writing ledger lines; (3) review freely for the time left; (4) write the findings block; every DEFECT or UNSURE ledger line becomes a finding.

Step R3. `ledger-check.py` runs on each report in under 1 s. It checks the ledger exists, has at least one line per assigned recipe, and every quote is an exact substring of the candidate or of a tool result in the transcript. It checks every DEFECT or UNSURE line has a finding.

Step R4. If a ledger is missing or malformed, one resume re-ask runs only if `now + 30 s <= 1.35 x baseline`. Otherwise it is skipped and recorded as `ledger_missing`.

Step R5. Normal merge.

Quoted draft wording of the ledger rule:

> "RECIPES AND LEDGER. Before you review freely, run the recipes below that are assigned to you, in order. For each recipe step, write one ledger line: `L<n> | <recipe id> | OK or DEFECT or UNSURE or SKIPPED | <quote from the candidate, 12 to 200 characters> | <what you ran or read, at most 15 words>`. If a recipe finds nothing to check in this document, write one SKIPPED line that says what you searched for. Write at most 12 lines. Put them under `## Check ledger` above the findings block. Ledger lines are not findings until you mark them DEFECT or UNSURE; then they must also appear in the findings block."

Quoted draft wording of the eight recipes (each is a detection procedure, not a "watch for" list):

> **R-C1.** "For each acceptance criterion or requirement that says every, all, each, complete, exhaustive, found, covers or no remaining: (1) write the finite check that would let a reviewer say yes, with its stopping rule; (2) copy the instruction sentence the criterion checks and write what set each of the two covers; (3) if you cannot write a finite check, or the two sets differ, mark DEFECT."
>
> **R-C2.** "Split the driving document into rules: one per sentence that contains must, shall, never, only, halts, reports or returns, or per table row. Take up to 10 rules, preferring those that govern a failure, an exit or a special case. For each, quote the candidate sentence that carries it. For the three with the most conditions, trace each failure path through the candidate's tasks to the output the rule governs. No carrying sentence, or a path that ends in a different output, is DEFECT."
>
> **R-C3.** "List every value, field or state that a task reads, maps or requires as the input to a decision (lookup tables, status mappings, conditions). For each, find the row, task or step that writes it, for every case the reader handles. A value with no writer in some case is DEFECT."
>
> **R-C4.** "For each criterion that embeds a command, pattern, selector or test name: write the exact text the same task tells the implementer to write or create. Apply the literal pattern to that text, case included (you may run it on a scratch string with Bash). Then ask what the command selects or matches on the current tree. A pattern that cannot match the ordered text, or a selector that picks fewer or other checks than the criterion needs, is DEFECT. Do not use the current file as proof; it may already contain finished work."
>
> **R-C5.** "For each change that alters a number, name, count, behavior or default that the repository may also state elsewhere: (1) write the old literal; (2) run one search of the whole tree for it, including root-level documents, changelogs, mirrored copies and comments, not only the files the plan names; (3) list every hit the plan neither edits nor checks. A hit that would be false after the change is DEFECT. Grade it with the grading check; never drop it."
>
> **R-C6.** "For each sentence the plan states or dictates that says all, only, never, every, no other, or outside X nothing: (1) name the set it covers; (2) run one count or listing command for that set over the tree; (3) compare with the plan's other tasks and with the scope of the test or check said to enforce it (what does that test skip or not read?). A member outside the claim, a task that does the opposite, or a test scope narrower than the claim is DEFECT."
>
> **R-C7.** "List every constraint, one clause per line (split at semicolons and 'and'). List every piece of text the plan dictates word for word. For each text and each constraint on its topic, tick each clause. A text that omits or contradicts a clause is DEFECT."
>
> **R-C8.** "For each file the plan edits or creates, search the tests, scripts and docs for its path and distinctive strings: `git grep -l -F '<string>' -- tests scripts docs`. For each referencing file the plan never names, open it and decide whether it pins the text or behavior being changed. If it does and no task updates or runs it, mark DEFECT."

**(b) Model roles.**

| Panel | Lens assignment | Why |
|---|---|---|
| Primary: ember + 2x luna | Ember {C4, C5, C6, C8}. Luna-1 {C1, C2, C3}. Luna-2 {C2, C4, C7}. | Ember runs greps (78% recursive search) and has idle seconds after 41 s. Luna reads whole files and rarely searches, so it gets reading classes. C2 and C4 are duplicated for redundancy. |
| haiku + 2x luna | Haiku {C5, C6, C8} with at most 6 ledger lines. Luna-1 {C1, C2, C3}. Luna-2 {C2, C4, C7}. | Haiku searches (81% of runs) but is the critical path, so its load is capped. Lunas have about 120 s idle. |
| sonnet + 2x luna | Sonnet {C5, C6, C8, C2}. Luna-1 {C1, C3, C7}. Luna-2 {C4, C7, C1}. | Sonnet is the only model that already opens unnamed files (35%), so it takes the sweeps. |

**(c) Time budget per package.** Same baselines and caps as Redesign 1.

| Step | Seconds | Note |
|---|---|---|
| R1 lens assembly | <1 | Script |
| R2 ember | 41 baseline + 4 recipes (about 4 greps x 3 s + 12 ledger lines x 2 s + thinking) = +40, about 81 | Under the critical path |
| R2 luna-1 | 100-122 + 3 recipes (reading the source in full, 10 ledger lines) = +22 | Critical path |
| R2 luna-2 | 100-122 + 18 | |
| R3 check | <1 | Script |
| R4 re-ask | 0 in most runs; 6 s start + about 20 s when it runs | Allowed only if it fits under the cap |
| Critical path | 122-144 s | |
| Elapsed increase | 122/100 = +22%; 144/122 = +18% | Cap 135-165 s, slack 13-21 s |

Haiku panel: haiku lens {C5, C6, C8} cap 6 lines adds about +35 s: 255-273 s, +16% and +15%; the lunas stay under 160 s. Sonnet panel: sonnet {C5, C6, C8, C2} adds about +30 s: 289-332 s, +12% and +10%.

Enforced: the re-ask condition `now + 30 s <= 1.35 x baseline`; the 12-line ledger cap in the check script; the same 1.6 x baseline panel deadline. Only expected: the recipe seconds and the median elapsed.

Redesign 2 has more slack than Redesign 1 because it has no pre-pass on the critical path. It spends its slack on compliance risk (the models must actually do the steps).

**(d) Defect-class coverage matrix.** Same convention as Redesign 1.

| Issue | Trigger (class mechanism) | Why a cheap model then reaches it | Per run |
|---|---|---|---|
| B1 (C1) | R-C1 step 1 forces the finite check on each "every ... found" criterion. | Luna reads Task text whole. Writing a stopping rule is a new move; no run has written one. Models may accept a vague rule. | 0.10-0.30 |
| B2 (C1) | R-C1 step 2: copy the instruction sentence and write both sets. | Same. A short comparison, no search. | 0.10-0.30 |
| B5 (C2) | R-C2 path trace for rules that govern an exit or a failure. | Luna reads source.md in 78% of runs; the recipe forces rule-by-rule carry and one path trace. Three near-misses already traced a neighbouring path. | 0.15-0.35 |
| B6 (C6) | R-C6 step 3 asks what the enforcing test skips and what other tasks do. | Ember can run the count command. The key evidence sits in other tasks and in a file nobody names. | 0.05-0.20 |
| B8 (C6) | R-C6 step 2: one count command over the set. | Ember is a grep-checker, but has never run an inventory on a claim; the recipe gives the command shape. | 0.10-0.30 |
| I1 (C3) | R-C3 table of read values against writers. | Models tabulate well when told to (grok did, with 33 turns). Cheap models have not been asked. | 0.05-0.20 |
| I4 (C4) | R-C4 apply the literal pattern to the ordered text. | A pure reading task. Ember or luna can run `echo ... | grep` in a second. | 0.40-0.70 |
| I5 (C5) | R-C5 whole-tree search for the old literal, other direction from the 16 over-match findings. | Ember runs greps; the recipe names the root-level and changelog locations as a class. CB-2 stops the drop. | 0.20-0.45 |
| I6 (C7) | R-C7 clause-by-text tick table. | Models already did the comparison on one task. The recipe makes the sweep a list. | 0.10-0.30 |
| I7 (C8, control) | R-C8 grep template over edited files. | Ember runs the command; opening an unfamiliar test file is the step luna and haiku skip. | 0.20-0.45 (of 1 on control) |

**(e) Broad applicability.**
- Other plans: the recipes mention no document. Moving to a new plan format needs only a note on where instructions, criteria and constraints live.
- Specifications: C1, C2, C3, C4 and C7 read directly. For C5, C6 and C8 the "tests" become the checks the spec names.
- Documentation reviews: C2 and C4 compare doc to code. C5 and C6 carry most of the load.
- Re-derive per target: the meaning of "edits", "tests" and "source"; the command dialect; the lens assignment from the reviewing model's measured habits.
- Anti-overfitting rules AO-1 to AO-3 and AO-5 from Redesign 1 apply to the recipe text. Additionally AO-7: each recipe has at least one worked example in the repository docs written from a class definition, never from the three packages. AO-8: the designer writes recipes from the class definitions and the recurrence evidence only, and a second author who has not seen any ground truth reviews each recipe for issue-specific words.

**(f) Expected gain out of 14 per run.**

| Block | Low | High |
|---|---|---|
| Baseline | 1.83 | 1.83 |
| H1-H4 | +0.03 | +0.34 |
| Redesign, gross | +1.25 | +3.10 |
| Displacement of B3, I2, B7 | -0.40 | -0.10 |
| Total | 2.7 | 5.2 |
| Share from the redesign | 0.85 | 3.0 |

Redesign 2 is lower than Redesign 1 on the sweep classes (C5, C6, C8) because the model has to run the sweep itself, and cheap models have shown no habit of it. It is equal on reading classes.

**(g) Overhead.**
- Elapsed: +18% to +22% on the primary panel.
- Output tokens: ledger plus ember's extra tool use gives +5-9k per package (+25% to +40%). Recipe prompt is about 300 tokens per lens, about 800 for all eight. Re-ask adds about 1.5k in 15-25% of runs.

**(h) Implementation effort.**
- New `recipes.md`: about 120 lines.
- New `tools/ledger-check.py`: about 100 lines, plus tests about 80 lines.
- Edit `tools/run-reviewer.sh`: about +30 lines (lens table by model, re-ask rule).
- Brief template: about +40 lines.
- No extractor code.

**(i) Failure modes.**

| Failure | Effect | Control |
|---|---|---|
| Compliance: luna writes a short ledger of OK lines without doing the steps (luna quotes anchors exactly in only 91.4% of cases; ember skipped source.md in 39%). | Gain near zero | The quote check; the `what you ran` field is cross-checked against the transcript's tool calls in the hold-out analysis |
| Prompt length hurts small models. | Lower base performance | Two to four recipes per lens, not eight |
| Lens split leaves a blind spot if one reviewer fails or is killed. | A class is lost | C2 and C4 are duplicated; the loss is reported by class |
| Ember's sweeps produce false hits. | Wrong blockers | CB-3, UNSURE non-blocking |
| False-positive growth. | Wrong blockers up (2x ember panels added 2.75-3.25 wrong blockers in earlier rows) | Decision rule limit +1.0; separate FP measurement on clean twins |
| The re-ask pushes elapsed over the cap. | Time | Enforced condition in R4 |

---

## 4. Comparison of the two redesigns

| Property | Redesign 1: Sweep Sheet | Redesign 2: Recipe Ledger |
|---|---|---|
| Who runs the sweeps | A script; the model judges tool output | The model, from written recipes |
| New code | about 400 lines of extractors plus tests | about 100 lines of checker plus recipe text |
| Theories answered | T1 directly (script sweep), T2 (item-level questions), T3b | T2 (forced ledger), T1 partly (command templates), T3b |
| Model roles (primary panel) | Ember: tool-line items; lunas: reading items; items judged by two reviewers | Ember: sweep recipes; lunas: reading recipes; C2 and C4 duplicated |
| Elapsed on the primary panel | +23% to +28% (tightest cell 128 s vs cap 135 s) | +18% to +22% |
| Elapsed on haiku, sonnet panels | +15%-16% ; +10%-11% | +15%-16% ; +10%-12% |
| Output tokens per package | +28% to +42% | +25% to +40% |
| Found out of 14 (total) | 3.2-5.7 | 2.7-5.2 |
| Of which redesign | 1.3-3.55 | 0.85-3.0 |
| Strongest classes | C4, C5, C8 (mechanical) | C4 (reading) |
| Weakest classes | C3, C6, C1 | C3, C6, C1 |
| Port to a new target | Extractors need a section map and an edited-object detector | Recipes need the meaning of "edits" and "tests" |
| Main risk | Rubber-stamp OK; extractor miss | Compliance; false hits from ember's own sweeps |
| Wrong-blocker risk | Medium | Medium to high |
| Answers the open question | "The model needs the check done for it" | "Instruction change alone is enough" |

---

## 5. Validation experiment

The design was derived from the three eval packages, so no decision uses them. They are run once, as a reported derivation-set check only.

**Material (hold-out).** From GEN §4:

| Set | Content | Items | Use |
|---|---|---|---|
| Real-1 | H5 (workerContractFo), H2 (implementIronbel), H4 (scIssueClaimPipe) plans with their `source.md` | about 25-30 ground-truth items, derived from each package's reflect report plus implement-time retry findings | Primary |
| Real-2 | H3 (phase3CodegraphA) | 9 important findings | Volume |
| Spec | H1 (worker-contract spec ledger, 20 blocking defects) | 20 | Spec-target generality. Caveat: the whole #346 series was tuned on it. |
| Sanity | H6 (designSpec #441) | 3 | Not in any decision |
| Planted | 6 documents (3 plans, 2 specs, 1 documentation set) x 1 planted defect per class (C1-C8) | up to 8 per document | Fresh-material generality and detector recall |
| Clean twins | The same 6 documents unplanted | 0 | False-positive rate |

Honest limit: the Real sets were used in GEN to show that classes recur, so they test "does the mechanism find known instances in text it was not tuned on", not unseen generality. The Planted set tests unseen text. Planted defects are written by a person who has not seen the recipes or extractors, from the class definitions and in each document's own vocabulary. Ground truth for the Real sets is written before any arm runs, hashed, and never shown to a reviewer. The `.dev/reflect/`, `artifacts/` and `progress.md` of each package are removed from every sandbox. Each sandbox is built from the commit the plan was written against (the plan sha equals the reviewed plan; GEN says this comparison is UNVERIFIED and must be done first).

**Arms.**

| Arm | Description |
|---|---|
| Z0 | The isolated panel, ember + 2x luna, with H1-H4. This is the named baseline for time and effect. |
| Z0-raw | The same panel without H1-H4, on Real-1 only, to measure H. |
| P | Placebo: Z0 plus a one-line list of the class names with no recipe and no sheet. Tests "named classes alone". |
| A | Redesign 1 on ember + 2x luna. |
| B | Redesign 2 on ember + 2x luna. |
| Zh, Ah, Bh | The same three arms on haiku + 2x luna. |
| Zs, As, Bs | The same three on sonnet + 2x luna; Real-1 only, comparison panel. |

**Runs.**

| Set | Arms | Runs per arm per document | Panel runs |
|---|---|---|---|
| Real-1 + Real-2 (4 documents) | Z0, P, A, B | 5 | 80 |
| Real-1 only | Z0-raw | 5 | 15 |
| Planted (6 documents) | Z0, A, B | 3 | 54 |
| Clean twins (6 documents) | Z0, A, B | 2 | 36 |
| Spec (H1) | Z0, A, B | 5 | 15 |
| Haiku (4 documents) | Zh, Ah, Bh | 3 | 36 |
| Sonnet (3 documents) | Zs, As, Bs | 2 | 18 |
| Total | | | about 254 panel runs, about 760 reviewer runs |

All arms in a stage run concurrently, in block-randomised order, one block per replicate, to cancel gateway load drift. The blind judge is Opus with the frozen rubric. The three original packages: one run per arm as a derivation-set report.

**Consistency metrics.**
1. Reach rate per item: runs finding it divided by runs. An item is consistent if reach is at least 0.6 (3 of 5).
2. Consistency index: the share of Real items that are consistent in the arm.
3. Found fraction: found items divided by items, averaged over documents, with a bootstrap interval clustered by document.
4. Run-to-run Jaccard of the found sets for one document.
5. Class reach: planted-defect detection rate per class and per document type.
6. Wrong blockers per run, blocking findings per run on clean twins.
7. Ledger audit: OK-rate on planted items, ledger-line quote validity, `what you ran` checked against tool calls.
8. Time: slowest-reviewer elapsed per package, medians, with kill counts.

**Pre-registered decision rule.** Fixed before the first run. A design passes only if all of D1-D6 hold.

| # | Condition |
|---|---|
| D1 Time | Median per-package elapsed at most 1.35 x the Z0 median of the same panel type, for the primary and the haiku panel. A design that fails is disqualified for that panel. |
| D2 Effect | Mean found fraction on Real-1 + Real-2 is at least Z0 + 0.12 absolute, and the lower bound of the 90% bootstrap interval is above Z0 + 0.04. |
| D3 Consistency | Number of Real items with reach at least 0.6 is at least Z0's count + 3. |
| D4 Precision | Wrong blockers per run at most Z0 + 1.0, and blocking findings per run on clean twins at most Z0 + 0.7. |
| D5 Generality | On the Planted set, detection rate at least 0.40 on at least 3 of the 5 general classes (C2, C4, C5, C6, C8) in plans, and the same on at least 2 classes in specs. The documentation set is reported, not gated. A design that fails D5 is claimed for plans only. |
| D6 Non-regression | Items that Z0 reaches at least 0.5 stay within 0.10 of Z0's reach. |

Outcomes:

| Result | Action |
|---|---|
| Neither passes | Keep H1-H4 only. Stop. |
| One passes | Adopt it. |
| Both pass | Take the higher found fraction. If the difference is under 0.05, take Redesign 2 (no script to maintain). |
| P within 0.03 of B | Report that recipe wording adds nothing over class names, and adopt the cheaper form. |
| Z0 versus Z0-raw difference | Report as the measured value of H1-H4, replacing +0.14. |
| Act-rate readout | The measured share of planted items turned into DEFECT lines replaces every planning probability in 3(d). |

Power is low: about 25-30 items and 5 runs per document. D2 and D3 are the weakest tests. A pass is evidence, not proof.

---

## 6. Numbered, testable requirements

**Harness and shared**

| # | Requirement | Test |
|---|---|---|
| R-01 | The brief names the absolute path of the driving document and carries CB-1, CB-2 and CB-3 word for word. | grep the generated brief; assert the three strings |
| R-02 | Before the merge, `anchor` and `anchor2` are truncated to 200 characters and `claim` to 300 (an exact prefix). The block is validated with the real findings parser. | Fixture with a 250-character anchor is kept, not dropped |
| R-03 | The findings-v1 block format and the merge contract are unchanged; ledger lines are outside the block. | Merge of a report with a ledger gives the same rows as without |
| R-04 | Each package sandbox is built from the commit the plan was written against, with `.dev/reflect/`, `artifacts/` and `progress.md` removed. | Absent repair line in the sandbox; `ls` fails on the removed paths |
| R-05 | Reviewers keep `--disallowedTools Edit Write NotebookEdit` and never receive ground truth. | grep the launcher; grep transcripts for the ground-truth hash |
| R-06 | No instruction, recipe, template, extractor or fixture contains text copied from any ground-truth item of the three eval packages or of the hold-out sets. | n-gram check (8-word shingles) of all instruction text against the ground-truth files; zero hits |
| R-07 | Every recipe or extractor cites at least 3 recorded other-document instances, or is labelled "plausible only". | Review of the cited list against GEN |
| R-08 | The swap test: each recipe sentence and question template stays correct after domain nouns are replaced by placeholders. | Second-author review; checklist in the repo |
| R-09 | Instruction text, extractors and templates are frozen and hashed before hold-out ground truth is read by the designer. | Hash recorded before ground-truth files exist in the working tree |
| R-10 | All reports record `elapsed_s`, `reask_s`, `killed`, `dropped_lines` and tool counts. | Schema check on each meta file |

**Redesign 1 (Sweep Sheet)**

| # | Requirement | Test |
|---|---|---|
| R-11 | The pre-pass is a non-model script that reads only the candidate and the sandbox, writes `sheet.md`, and is killed at 15 s, after which the baseline brief runs. | Unit test with a sleeping fixture; the panel still runs |
| R-12 | The sheet has at most 12 items (Q2, U2, M2, R2, S2, K1, X1), shuffled per reviewer, each judged by two reviewers, at most 6 items for the critical-path model. | Parse `sheet.md` and the assignment table |
| R-13 | An M item prints MATCH or NO MATCH for each ordered quoted string, case-sensitive; an S item splits hits into plan-named and plan-unnamed; an R item lists referencing files the plan never names. | Synthetic fixtures with known answers |
| R-14 | The script and its fixtures contain no ground-truth text (R-06) and the sheet contains no review output. | n-gram check; grep |
| R-15 | `ledger-check.py` verifies one ledger line per assigned item, a finding for each DEFECT or UNSURE line, and exact-substring quotes. | Fixture reports: missing line, fake quote, missing finding each flagged |
| R-16 | The median elapsed with the sheet is at most 1.35 x Z0 for each panel type; the pre-pass median is at most 8 s. | Section 5 D1; the S0 spike |
| R-17 | An empty sheet leaves the panel equal to Z0 (same brief hash apart from CB-1 to CB-3). | Hash comparison |

**Redesign 2 (Recipe Ledger)**

| # | Requirement | Test |
|---|---|---|
| R-18 | The eight recipes are stored in one file and quoted verbatim into the brief by lens assignment; no reviewer receives more than 4 recipes. | Parse the generated briefs |
| R-19 | Lens assignment follows the table in 3(b) for each panel type, with C2 and C4 duplicated. | Unit test of the assignment function |
| R-20 | Each report carries `## Check ledger` with at least one line per assigned recipe and at most 12 lines. | `ledger-check.py` |
| R-21 | Every ledger quote is an exact substring of the candidate or of a transcript tool result; the `what you ran` field is checked against tool calls in the analysis. | Fixture; analysis script |
| R-22 | A re-ask runs only if `now + 30 s <= 1.35 x baseline` and at most once per reviewer. | Timer test with a fake clock |
| R-23 | The median elapsed is at most 1.35 x Z0 for each panel type. | Section 5 D1 |

**Experiment and decision**

| # | Requirement | Test |
|---|---|---|
| R-24 | Hold-out ground truth is written and hashed before the first arm runs and is never placed in a sandbox. | Hash timestamps; sandbox grep |
| R-25 | The Planted set is written by an author who has not seen the recipes or extractors; each document has a clean twin. | Author attestation recorded in the manifest |
| R-26 | The arms Z0, Z0-raw, P, A, B (primary), Zh, Ah, Bh and Zs, As, Bs are run with the counts in section 5, in block-randomised order. | Run manifest |
| R-27 | Metrics 1-8 of section 5 are computed by one script from the run folders. | Script test on a fixture |
| R-28 | The decision rule D1-D6 and the outcome table are stored before the first run and applied unchanged. | Commit hash earlier than the first run |
| R-29 | The judge, rubric and the grading text are sha256-pinned and identical in all arms. | Hash compare |
| R-30 | Results are reported by arm for H share and redesign share separately, never summed in a headline; time is reported by panel type with kill counts. | Report check |
| R-31 | Per-class reach, OK-rate on planted items and measured act rate replace the planning probabilities in 3(d). | Updated tables |
| R-32 | Every claim of breadth names its target type (plan, spec, documentation) and the evidence for it; C3 and C1 are claimed only as supported by the hold-out result. | Review against D5 |

Final note on what remains unproven: none of the gain ranges has been measured. The wording of CB-1 to CB-3, the ledger rule, the recipes and the item questions has not been run on any model. The two redesigns are tested only by the experiment in section 5.

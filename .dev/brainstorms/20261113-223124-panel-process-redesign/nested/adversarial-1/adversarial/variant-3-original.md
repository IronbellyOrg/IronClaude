# Variant 3 (backend lens): Requirements Specification for Redesigning the Tasklist Review Panel

Lens: API contracts, data integrity, idempotency, operations. Evidence paths are relative to `.dev/`. Estimates are marked as estimates. Nothing here is measured unless a source is cited.

## 1. Theories

Three theories explain why ember + 2x luna, haiku + 2x luna and sonnet + 2x luna missed the ten issues. Two were accepted with refinement and one was refined into a sharper form. A reasoning-budget theory was tested and rejected as the main cause.

| # | Theory | Evidence (numbers) | Implied instruction or process change |
|---|---|---|---|
| T1 | **Plan-bounded search.** Cheap reviewers verify only the files and lines the plan names. Nobody runs a reverse-dependency sweep ("which other files and tests reference what this plan edits?"). | Runs that opened a test file the plan did not name: sonnet 35%, grok 33%, ember 8%, luna 1%, haiku 0% (`analysis` pattern file, `investigation-patterns.md` section 1). Of 8 DE runs that touched `test_worker_contract.py`, 7 reported the missing-task finding (I7). 0 of 225 other DE runs did. Haiku searched as often as sonnet (81% vs 94% of runs search tests/) but only inside the named test file, so search volume is not the variable. | A forced reverse-dependency step: for each edited path, list every referencing file in the tree, then open each unnamed hit. |
| T2 | **One-axis questions with no enumeration (refined from "right place, wrong question").** Reviewers anchor the correct sentence but ask one question about it and never check the other direction, another input case, or the complete set. | GT10 anchored by 16 cheap reports, all 16 asked whether the grep over-matches. None asked where else the claim appears (`investigation-designspec.md` section 2c). GT5: 3 reviewers traced only the mode-off case, none traced the halt path. GT6: 1 reviewer tabulated fold rows against mapping inputs. GT1 and GT2: zero anchors in any panel. | A per-class recipe that forces enumeration: an item list the reviewer must answer, including the "other direction" item for each count or universal claim. |
| T3 | **Environment and grading rules hide or suppress defects.** The post-implementation checkout repairs some defects, and Medium grading drops missing-requirement findings. | The sandbox already contains the repaired code for GT5, GT6 and GT9 (`investigation-designspec.md` line 14 onward). 14 of 39 ember runs never opened `source.md` (`investigation-designspec.md` section 2a). Luna reports 72% blocking and terra 82%; Medium findings rarely reach the block (`investigation-patterns.md` theory C). Grok saw the stale CHANGELOG line and dropped it as minor (`investigation-designspec.md` section 3). | Harness fixes H1 to H4 (section 3), plus a rule that a stale second location is a finding, not a note. |

**Rejected as the main cause: reasoning budget (theory A in `investigation-patterns.md`).** Thinking tokens correlate with total hits across models (Spearman rho 0.64). Within ember and luna, though, the hard classes do not rise with thinking (ember 0.25 to 0.22 per run, luna 0.09 to 0.09). Budget explains haiku's variance, not the ceiling of the primary panel.

Evidence files: `.dev/brainstorms/20261113-223124-panel-process-redesign/enrichment/reused/investigation-patterns.md`, `investigation-designspec.md`, `investigation-alias-control.md`.

## 2. Defect classes and generality

Classes are stated without package, task, file or ground-truth wording. Class IDs follow `enrichment/investigation-generality.md` section 1.

| Class | Abstract definition | Issues it covers (investigation labels) | Other documents with a recorded instance | Verdict (generality file, section 5) | Review targets it applies to |
|---|---|---|---|---|---|
| C1 | A criterion asks for a complete result over a set with no bounded method or stopping rule, or the criterion's scope differs from its instruction's scope | designSpec GT1, GT2 | 3 (symptom level only) | Supported with a caveat | Plans, specs, criteria |
| C2 | A rule stated in the source is not carried into the plan text or check | designSpec GT5 | 6 (all plans) | General | Plans, specs, source-to-plan traceability |
| C3 | A value read by one component is written by no row or task | designSpec GT6 | 3 | Weak | Mapping tables, specs |
| C4 | A check's literal command or pattern cannot match, or passes vacuously, against the text the same plan orders | designSpec GT9 | 9 (8 plans) | General | Any document with commands or grep criteria |
| C5 | A count, claim or copy in a second location goes stale because no task enumerates it | designSpec GT10 | 9 (3 plans, 6 delivered) | General | Plans, changelogs, docs, mirrors |
| C6 | An "all", "only" or "never" sentence is contradicted by an inventory, a later task, or the scope of the test that enforces it | alias GT1, GT3 | 12 | General | Plans, specs, user guides |
| C7 | Dictated text drops a clause of a constraint stated elsewhere | alias GT4 | 5 broad, 1 narrow | Broad form general; narrow form weak | Plans with constraint lists |
| C8 | A plan edits behaviour or text that a test elsewhere pins, with no task updating or running that test | control GT1 | 6 (5 plans) | General | Plans, specs |

Recurring classes outside the ten (X1 to X7 in `investigation-generality.md` section 3) are about as frequent as the ten. Examples: X1 vacuous checks (4 documents), X3 conflicting source statements (3), X6 edge path with no route (3). The ten are not a special set.

**Generality evidence, and its limits.**
- `investigation-generality.md` section 2 lists the instances per class. Its section 4 lists six hold-out candidates. Its section 5 gives the verdicts.
- `research-external.md` section 2 maps the classes onto ISO/IEC/IEEE 29148 characteristics: verifiable, complete, consistent, feasible. Smell detectors reached 59% precision at 82% recall (Femmer et al.), so detector output needs a filter.
- Caveats: one repository, one owner, one plan pipeline. Counts are phrase-search lower bounds. The records show that a class exists, not that cheap panels miss it in other documents. Only a hold-out run shows that (section 5).

**Per-class recipe.** Each class gets one concrete detection move (investigation section 1, "review move" column). Recipes are written once, generically, and quote no ground truth. Research on checklists (`research-external.md` section 1.3) found that a generic checklist does no better than ad hoc reading, while a class-specific procedure does. So every class has a recipe, not a "watch for" line.

## 3. Redesigns

Both redesigns keep the findings-v1 merge contract. They keep the schema bounds: anchor 12 to 200 characters, claim 300 or fewer, refs 8 or fewer, id 16 characters or fewer, severity CRITICAL, MAJOR or MINOR. Extra output goes in a separate fenced block (`coverage-v1`), which the merge ignores. Both redesigns depend on harness fixes H1 to H4 (section 3.3), so the comparison is taken on top of those fixes.

### 3.1 Redesign A: Class Recipe Sweep (CRS)

**(a) Mechanism and steps.** A deterministic helper runs once per package before any reviewer starts. It turns the candidate and `source.md` into a numbered item list. Every reviewer gets the same list in its brief. Each reviewer must answer every item, then write findings for the defects it confirmed.

Exact order:
1. **Helper (orchestrator, no model).** `tools/panel_prepass.py` (new) runs under `uv run python -I`. It reads `candidate.md` and `source.md`. It emits items P1 to Pn (cap 60, brief size 10 KB at most), in this class order:
   - C6: every sentence with a universal word (all, every, each, only, never, none, outside, any).
   - C4: every backticked command or quoted search string inside a criterion. It records whether the quoted string occurs in the candidate text (literal occurs: yes or no).
   - C8 and C2: every path the plan says to create or edit, plus the repository-wide hits for its basename under `tests/` and the root, excluding `.dev/` and sandbox folders. Cap 12 hits per path, with the total count shown.
   - C5: every number attached to a noun ("N members", "N files"), plus the repository-wide hits for that exact phrase, root documents included.
   - C7: every constraint line, split on semicolons and "but/until/once" clauses. One item per clause.
   - C2 (source present only): every source sentence containing must, never, reports, only, when.
   - C1: every criterion with every, all, complete, each. Item: "name the finite check that proves it".
   - C3: every backticked field name a mapping or status sentence reads. Item: "name the row that writes it".
2. **Stage 1, parallel.** Each panel member gets the identical brief, with the item list inline. The members are ember, luna and luna in the primary panel. Each runs with the existing `run-reviewer.sh` launch, with the timeout in section 3.1(c).
3. **Coverage block.** Before the findings block, each reviewer writes one line per item in a fence with info string `coverage-v1`: `{"id":"P7","verdict":"ok|defect|na|unchecked","evidence":"<file:line or command and its result>"}`. A verdict of defect also needs a findings-v1 line with the anchor copied from the candidate.
4. **Merge.** The existing `superclaude review merge` runs unchanged on the findings-v1 blocks. The coverage blocks are archived per reviewer for audit. An item left `unchecked` is recorded in the loop summary, not hidden.

Draft brief wording added to the first-review brief (appended after the existing paragraph in `run-reviewer.sh` line 15):

> "Before you write findings, answer every item P1 to Pn in the list below. Write one line per item inside a fenced block with info string coverage-v1, using verdict ok, defect, na or unchecked, and an evidence field that names a file and line or a command you ran and its result. Run the command or search each item names when you can. Do not answer from memory. An item you did not check is unchecked, with the reason. Every defect verdict must also appear as a finding with an anchor copied exactly from the candidate. Source items are read against the source file named in the brief. Do not edit any file."

Draft wording for the per-item instruction, one template per class (the helper fills the bracketed slots):

- C1: "[criterion text]. Name the finite check that proves this. If no bounded check exists, the verdict is defect."
- C4: "The literal string [quoted] does not occur in the candidate text where the task orders it. Confirm by running the grep. If it does not match, the verdict is defect."
- C6: "[universal sentence]. Test it against the list of files in the item's evidence and the enforcing test's scope. Name one case that breaks it, or ok."
- C8: "[test path] is not named in the plan and references [edited path]. Open it and name the lines it pins. Verdict defect if the gate does not run it."
- C5: "[phrase] appears at [hits] outside the plan's edit list. Verdict defect for each hit the plan does not update."

**(b) Model roles.**
- ember + 2x luna (primary): each member answers the full list. ember takes the mechanical items (C4, C5, C8) by running them. Each luna takes the reading items (C1, C2, C3, C6, C7) and reads named files whole. Both luna members get the full list, so their answers can overlap. That overlap is a cross-check, not a vote.
- haiku + 2x luna: haiku replaces ember. Haiku's search volume is adequate for the mechanical items, but its output is long (haiku 233 s, 45.8k thinking tokens), so the stage-1 timer is the constraint.
- sonnet + 2x luna: the same as haiku. Sonnet's 35% test-file rate is the main gain over the primary panel (comparison arm only, section 5).

**(c) Time budget.** Baseline per package is the isolated ember + 2x luna slowest reviewer, median 100 to 122 s (seed brief). Worst case uses 122 s. The +35% ceiling is 165 s per package.

| Step | ember + 2x luna (s) | haiku + 2x luna (s) | sonnet + 2x luna (s) |
|---|---|---|---|
| Helper (deterministic, reverse-dependency grep capped at 15 s) | 6 | 6 | 6 |
| Stage 1 critical path (slowest reviewer): luna 102 + 18 for the item list | 120 | haiku 233 + 18 = 251 | sonnet 302 + 18 = 320 |
| Merge | 3 | 3 | 3 |
| **Critical path** | **129** | **260** | **329** |
| Baseline (isolated panel, same model set) | 122 | 238 | 302 |
| **Increase** | **+6%** | **+9%** | **+9%** |

Three packages in aggregate, primary panel: baseline 348 s; CRS about 348 + 3 × 24 = 420 s, which is +21%.

Critical path: the slowest luna reviewer (reading whole named files plus answering 40 to 60 items). The fast ember reviewer is idle for about 80 s and is the cheapest free capacity.

Enforced by a kill timer: each stage-1 reviewer gets `timeout 165` (the per-package ceiling). A reviewer killed by the timer produces no valid findings block, so the existing 2-attempt retry is disabled for that member. Expected, not enforced: the 122 s and 18 s estimates. These come from the seed brief medians and from the added-tokens estimate in (g), and the validation run (section 5) measures them.

**(d) Coverage matrix (per run, estimates).** Probabilities are my estimates from the investigation records. They are priors for the validation run, not measurements. The mechanism is the class-level trigger. The cheap-model reason is why a model that had missed the issue would now reach it.

| Issue (investigation label) | Class | Class-level mechanism that triggers it in CRS | Why a cheap model reaches it | P(reach) low | P(reach) high |
|---|---|---|---|---|---|
| designSpec GT1 (unbounded inventory AC) | C1 | Item for every "every/complete" criterion: name the finite check | The item forces a yes or no on the check, not a reading of the criterion as good practice | 0.25 | 0.55 |
| designSpec GT2 (scope of AC differs from task body) | C1 | Item pairs each AC with its own task body's scope | Forced pairing; no need to read the source | 0.20 | 0.45 |
| designSpec GT5 (dropped halt rule) | C2 | Source-sentence items with "reports" and "never", each traced to a halt path | Forced sentence-by-sentence walk, not a sampled read | 0.30 | 0.60 |
| designSpec GT6 (fold value never written) | C3 | Item per field read by a mapping sentence: name the writing row | Enumeration exposes the mismatch; the repaired code does not hide it because the item cites the source | 0.20 | 0.40 |
| designSpec GT9 (grep cannot match ordered text) | C4 | Literal-occurs check of each quoted string against the candidate | Mechanical; ember and luna can run it in seconds, and the helper already reports "no occurrence" | 0.60 | 0.85 |
| designSpec GT10 (CHANGELOG count stale) | C5 | Repository-wide hits for the count phrase, root included | The hit list is printed; the reviewer only has to judge it, and the other-direction item asks for it | 0.50 | 0.75 |
| alias GT1 (aliases-only claim vs test scope) | C6 | Universal sentence tested against the enforcing test's scope and later tasks | The item names the test the sentence cites; the reviewer must say what the test can fail on | 0.30 | 0.55 |
| alias GT3 (all other primitives use aliases) | C6 | Inventory count of files quantified by the universal, with and without the enforced attribute | The helper gives the counts; the model compares two numbers | 0.40 | 0.70 |
| alias GT4 (dictated text drops a constraint clause) | C7 | Clause-by-clause item per constraint | Narrow form is weakly supported, so the reach is low | 0.20 | 0.40 |
| control GT1 (test pins edited lines, not in gate) | C8 | Reverse-dependency hit list lists the unnamed test file; item says open it | The file name is in the printed list; the item forces opening it, which haiku and luna never did unprompted | 0.55 | 0.80 |

Expected sum over the ten: 3.6 to 6.6 of 10 issues reached per run, midpoint about 5. Reaching an issue here is not the same as a blocking finding in the merged output. The merge and the blocker rule still decide the verdict. The findings-v1 contract allows at most one line per defect, so the expected yield is discounted in (f).

**(e) Broad applicability.**
- Porting to other plans: the same helper runs on any markdown plan. Its extractors use generic syntax only: universal words, backticked commands, quoted strings, paths, numbers next to nouns, constraint lists.
- Porting to specifications: the source-sentence items use the same keyword set. The C1 item fires on "every" and "complete" in any requirement. Re-derive the list of quantifier words for the document language, not for the repository.
- Porting to documentation reviews: C5 (stale copy) and C6 (universal claim against an inventory) are the classes most common in user guides and changelogs (`investigation-generality.md` section 2, C6 delivered-document cases). The items are unchanged; the repository-wide search covers the doc tree.
- What must be re-derived for each new target: the list of universal words, the path rules for what counts as an edit (for docs, the list of mirrored files), and the exclusion list for the reverse-dependency search (generated and sandbox folders).
- Anti-overfitting rules:
  1. No item text may contain a quote from ground truth, a task number, a file name taken from a single package, or an issue-specific hint. Templates use bracketed slots filled from the candidate at run time.
  2. The helper's regexes are written before any hold-out package is opened, and they are frozen (hash recorded) for the validation run.
  3. Recipes must read the same for a document with no tests. A recipe that names `tests/` is parameterised by a repository setting, not hard-coded.
  4. A recipe never tells the model the answer ("the file X is missing a row"). It tells the model the check to run.

**(f) Expected gain (issues found out of 14 per run).** Baseline ember + 2x luna: 1.83 of 14 (seed brief).

| Share | Low | High | Basis |
|---|---|---|---|
| Harness fixes H1 to H4 (section 3.3) | +0.4 | +0.9 | H1 alone unlocks source-dependent defects for the 36% of ember runs that skipped `source.md`. H3 unmasks defects the repaired checkout hides. H4 removes the leak that gave 2 of 9 I7 credits. Estimate, not measured. |
| Redesign A (CRS) on top of fixes | +1.2 | +2.3 | Discounted from the coverage sum in (d) for overlap, for the merge's one-line-per-defect rule, and for the blocker rule (section 3.1(d)). |
| **Total ember + 2x luna** | **3.4** | **5.0** | Shares are not additive. The estimate is an upper bound on the share from each source. |

**(g) Token and elapsed overhead.** Baseline output for the three packages with ember + 2x luna: about 64k tokens (seed brief). CRS adds the coverage block (about 40 short lines per reviewer) and the longer brief. Estimate: +20k output tokens across the three packages (about +30%). Input overhead: item list about 10 KB per reviewer, per package. Elapsed: +21% (section 3.1(c)).

**(h) Implementation effort against the existing harness.**
- `tools/panel_prepass.py`: new, about 180 lines, stdlib only, with unit tests of about 120 lines.
- `tools/run-reviewer.sh`: about 25 added lines. The item list is passed as an inline file, and the coverage fence is added to the brief. The timer is set per package.
- `tools/coverage.py`: new, about 60 lines, parses `coverage-v1` for audit and counts `unchecked`.
- Brief template in the eval tools: about 30 lines added.
- Product code: none for the eval. A product version would extend `superclaude review panel` by about 150 lines. Not included in the estimate.
- Tests: the helper's extractors each get one fixture and one negative case (the rule in section 3 of the seed brief about regression checks).

**(i) Failure modes.**
- False-positive growth: forced items produce "defect" verdicts on weak evidence. Estimate: +2 to +4 findings per run, with a lower precision (the Tencent static-plus-model result suggests a filter is needed; `research-external.md` section 1.5). Mitigation: a defect verdict without a command result is downgraded to a note by the merge step.
- Wrong blockers: the literal-occurs check fires on quoted text that is an example, not an acceptance criterion. Mitigation: the helper only emits C4 items for quoted strings inside criterion lines.
- Reverse-dependency flood: a common basename returns many hits. Mitigation: cap 12 per path, print the total, and say so.
- Prompt length: 10 KB of items can hurt luna (small-context weakness, `research-external.md` section 4). Mitigation: section 3.1(d) item count cap 60, and the stage timer.
- Haiku ignores the list: haiku may answer "ok" without running the command. Mitigation: the coverage verdict `ok` without an evidence command is counted in the audit.

### 3.2 Redesign B: Blind Lenses then Verify (BLV)

**(a) Mechanism and steps.** Stage 1 runs three blind lenses in parallel. Each lens gets its own class packet, and no lens sees another lens's output. The orchestrator unions the claims with deterministic code. A verifier then checks each claim against the file, without learning which lens found it.

Exact order:
1. **Helper** (same as CRS step 1, but split into two packets):
   - Packet S (sweep): C4, C5, C8, C6-inventory items. These need repository-wide searches.
   - Packet R (reading): C1, C2, C3, C6-scope, C7 items. These need reading.
   The helper randomises item order within each packet, using a seed recorded in the audit log, to reduce order bias.
2. **Stage 1, parallel and blind.**
   - Lens S: ember gets packet S.
   - Lens R-1: luna gets packet R, items in the first randomised order.
   - Lens R-2: luna gets packet R in a second randomised order, plus the C6 and C8 items again, read from the other end of the candidate.
   Each lens writes a findings-v1 block only. No lens gets a coverage block. A lens does not see the others' outputs.
3. **Union (deterministic code, no model).** `tools/coverage.py` (new) collects the claims. Two claims are the same when their anchors overlap by at least 12 characters after whitespace flattening. Blocking claims and MAJOR claims go to the verifier, capped at 8 claims. Claims over the cap go into follow-up candidates.
4. **Stage 2, verifier.** One reviewer (ember in the primary panel) gets only the claim text, the anchor, the anchor2 and the refs, plus the candidate and the named source. It returns CONFIRMED or REJECTED for each claim, with a quoted evidence line. It cannot add new findings. A verifier note of "other" is written to follow-up candidates.
5. **Merge.** The existing merge runs on the confirmed claims in findings-v1. Rejected claims are archived with the reason.

Draft wording for the lens brief (appended, same for ember and luna):

> "You are one of three blind lenses. Your packet below lists items to check. For each item, run the check it names, write a findings-v1 line for each confirmed defect, and do not write about anything outside the packet unless it is a severe defect you cannot place in an item. Do not read or assume the work of any other reviewer. Do not edit any file."

Draft wording for the verifier brief:

> "You are verifying claims made by another review. Each claim below is a candidate defect with its anchor. For each claim, open the anchor in the candidate, check the claim against the exact text and any named file, and return CONFIRMED with an evidence line, or REJECTED with the reason. You may not add a claim. Do not edit any file. You do not know who made any claim, and you should not try to find out."

**(b) Model roles.**
- ember + 2x luna: ember runs Lens S, then (after the union) the verifier. Lens R-1 and R-2 are luna. The verifier is the only sequential step.
- haiku + 2x luna: haiku replaces ember in Lens S. Verifier is luna (full reading of the candidate, a shorter task than a full review).
- sonnet + 2x luna: sonnet runs Lens S. Verifier is luna. The sonnet time, 302 s, is the Lens S critical path.

**(c) Time budget.**

| Step | ember + 2x luna (s) | haiku + 2x luna (s) | sonnet + 2x luna (s) |
|---|---|---|---|
| Helper (two packets) | 6 | 6 | 6 |
| Stage 1 critical path (slowest lens): luna R-1 at 102 + 10 | 112 | haiku 233 (Lens S) | sonnet 302 (Lens S) |
| Union (code) | 2 | 2 | 2 |
| Stage 2 verifier (estimate; ember 25 s, luna 30 s) | 25 | 30 | 30 |
| Merge | 3 | 3 | 3 |
| **Critical path** | **148** | **274** | **343** |
| Baseline | 122 | 238 | 302 |
| **Increase** | **+21%** | **+15%** | **+14%** |

Ceilings: 165 s (ember + 2x luna), 321 s (haiku + 2x luna), 408 s (sonnet + 2x luna). All three fit.

Three packages in aggregate, primary panel: 348 + 3 × 26 = 426 s, +22%.

Critical path: stage 1 (Lens S or R-1), then the verifier. Both are sequential.

Enforced by a kill timer: stage 1 reviewers have `timeout 150` and the verifier has `timeout 45`. A verifier killed by the timer marks its claims "unverified" and puts them in follow-up candidates, not in blockers. A lens killed by the timer contributes no claims. Expected, not enforced: the 25 s verifier estimate and the 10 s lens increment. The validation run measures both.

**(d) Coverage matrix (per run, estimates).**

| Issue (investigation label) | Class | Class-level mechanism that triggers it in BLV | Why a cheap model reaches it | P(reach) low | P(reach) high |
|---|---|---|---|---|---|
| designSpec GT1 | C1 | Lens R item on every complete criterion; a second luna lens reads the same item from the other end | Two independent lenses on one item raise recall without a vote (union, then verify) | 0.30 | 0.60 |
| designSpec GT2 | C1 | Lens R scope-pairing item | Same as CRS | 0.25 | 0.50 |
| designSpec GT5 | C2 | Lens R source-sentence item, then the verifier confirms the halt path | Verifier only needs the claim and the file, which lowers the cost of the trace | 0.30 | 0.55 |
| designSpec GT6 | C3 | Lens R field-to-writer item | Same as CRS; the verifier is less likely to be swayed by the repaired code | 0.20 | 0.45 |
| designSpec GT9 | C4 | Lens S literal-occurs check | Mechanical; the verifier re-runs the check | 0.55 | 0.80 |
| designSpec GT10 | C5 | Lens S repository-wide count search | Printed hits; other-direction item | 0.45 | 0.70 |
| alias GT1 | C6 | Lens R scope item on the enforcing test; verifier checks the claim against the test | Verifier catches a contradiction the lens overstated (fewer false positives) | 0.30 | 0.55 |
| alias GT3 | C6 | Lens S inventory count | Same as CRS | 0.35 | 0.65 |
| alias GT4 | C7 | Lens R clause item, read by a second luna in reverse order | Reverse order is the only real change from one luna pass; the item may still be missed | 0.20 | 0.40 |
| control GT1 | C8 | Lens S reverse-dependency hit list, opening unnamed test files | Same as CRS | 0.50 | 0.75 |

Expected sum: 3.3 to 6.2 of 10, midpoint about 4.8. Versus CRS, BLV adds verification (fewer false positives) and loses some coverage per lens (fewer items per reviewer).

**(e) Broad applicability.** The same as CRS. The verifier step is the most portable part, because it needs only a claim and an anchor. It also transfers to specifications: a verifier checks a requirement claim against the requirement text. Re-derive the lens packet split for each document type (the S-or-R split is about "needs a search" versus "needs a reading", which is general). Anti-overfitting rules are those of 3.1(e), plus: the verifier never sees the lens name or the claim's origin.

**(f) Expected gain.**

| Share | Low | High | Basis |
|---|---|---|---|
| Harness fixes H1 to H4 | +0.4 | +0.9 | Same as CRS (3.1(f)) |
| Redesign B (BLV) on top of fixes | +1.1 | +2.1 | Lower coverage per lens, offset by union and verification |
| **Total ember + 2x luna** | **3.3** | **4.8** | Upper bound on each share |

**(g) Token and elapsed overhead.** Stage 2 adds one verifier call over at most 8 claims (estimate: +6k output tokens across three packages). Stage 1 adds two lens packets instead of one brief (estimate: +10k output tokens). Total about +16k (about +25%). Elapsed: +22% (section 3.2(c)).

**(h) Implementation effort.**
- `tools/panel_prepass.py`: about 200 lines (two packets, seeded shuffle, audit log), plus about 120 lines of tests.
- `tools/coverage.py`: new, about 140 lines for the union and claim comparison. Its anchor overlap rule and its cap are unit-tested with an exact-length fixture (anchor 12 and 200 characters).
- `tools/run-reviewer.sh`: about 35 added lines for the lens packets, the verifier call and the timers.
- Verifier brief and lens brief: about 40 lines of template.
- Product code: as CRS, about 220 lines if promoted to `superclaude review panel`.

**(i) Failure modes.**
- Verifier rejects a true defect: a verifier that reads the claim and the file alone can reject a correct claim with a narrow anchor. Mitigation: the verifier may read the named source and cited files. Rejected claims are archived; a sample is reviewed by a human in the validation run.
- Union drops a defect: two lenses with the same anchor but different claims are merged. Mitigation: merge keeps both claims if the category differs.
- Verifier anchoring on the claim wording: the verifier is told the claim is a candidate, not a fact. This is weaker than the blind design in the research note, because the verifier reads the claim text (`research-external.md` section 4). Mitigation: the claim is shown without its severity label.
- Stage-2 timeout leaves claims unverified: they are not blockers. Mitigation: the loop summary lists them, so the user sees them.
- Two luna lenses share a bias: agreement across two luna runs is correlated (`research-external.md` section 4, self-agreement). Mitigation: the second lens gets the reverse order, and the validation run reports the overlap.

### 3.3 Harness fixes (common to both redesigns)

These are the four fixes from the first brainstorm (seed brief, H1 to H4). Each redesign depends on them and the comparison is taken after them.

| Fix | Change | Why needed for these redesigns | Source |
|---|---|---|---|
| H1 | Name `source.md` in the brief | C2 items cannot fire if the reviewer does not read the source | `run-reviewer.sh` line 11 and line 13 brief; `investigation-designspec.md` section 2a |
| H2 | Truncate anchors and claims over the limits instead of dropping the finding | Item-forced anchors are longer; D1 dropped 49 blocking findings in the prior study | `HANDOFF-review-panel-unification-run2.md` line 162 (D1); master's `findings_v2.py` keeps 12 to 200 and 300 |
| H3 | Review a pre-implementation checkout | Post-implementation trees hide C4, C5 and C2 defects | `investigation-designspec.md` line 14; `investigation-alias-control.md` line 9 |
| H4 | Remove `.dev/reflect/` and the package's `artifacts/` and `progress.md` from the sandbox | Reflect reports leak I7 (2 of 9 credits) | `investigation-alias-control.md` section 3, LEAK paragraph; `HANDOFF` line 209 (H4 BLOCK_OK check) |

H4 in the handoff (line 209) is a separate fix: `BLOCK_OK` only checks the fence opener, it does not parse the block. That is the parse-check gap both redesigns need closed, so the coverage block and the findings block are both validated by a parser, not a grep.

### 3.4 Comparison of the two redesigns

| Criterion | Redesign A: CRS | Redesign B: BLV |
|---|---|---|
| Mechanism | One shared item list; every reviewer answers all items | Three blind lenses, union, verifier |
| Stages | 1 parallel stage | 2 stages (one sequential verifier) |
| Critical path, primary panel | 129 s (+6%) | 148 s (+21%) |
| Critical path, haiku panel | 260 s (+9%) | 274 s (+15%) |
| Critical path, sonnet panel | 329 s (+9%) | 343 s (+14%) |
| Expected gain on top of fixes (issues of 14) | +1.2 to +2.3 | +1.1 to +2.1 |
| Coverage sum over ten issues (per run) | 3.6 to 6.6 | 3.3 to 6.2 |
| False-positive risk | Higher (every item can yield a defect verdict) | Lower (verifier filters) |
| Effort (new lines, approximate) | About 240 | About 350 |
| Coverage per reviewer | Full list, may dilute attention | Narrower packets, more focus |
| Reliance on a second model call | No | Yes (verifier) |
| Best use | When cost and simplicity matter most | When wrong blockers are the main concern (haiku's blocking rate was 0.65 wrong per run, `investigation-patterns.md` section 5) |

## 4. Validation experiment (hold-out, not the derivation data)

**Hold-out material.** Use the fast trio from `investigation-generality.md` section 4, none of which the redesigns were derived from:
- H5: worker-contract spec plan, docs-only, 11 advisory findings (`R/pre-TASK-WF-workerContractFo-20261106-214402-20261106214804/REPORT.md` lines 18 to 48).
- H2: implement-Ironbelly plan, 4 blocking findings B-1 to B-4 (`R/pre-TASK-WF-implementIronbel-20261104-130647-20261104130837/REPORT.md` lines 42 to 60).
- H4: scIssueClaimPipe plan, 6 blocking and 6 medium (`R/pre-TASK-WF-scIssueClaimPipe-20261107-063237-20261107063558/REPORT.md`).

Target about 25 ground-truth items in total. Optional depth check: H1 (44-defect spec ledger, `X346/p17/ledger.json`). It was tuned across the #346 series, so it is a hold-out for the three eval packages only.

**Contamination controls.**
- Ground truth for the hold-out is written before any arm runs, from the reflect reports and the ledger, not from any panel output. A second person (or Opus as blind judge) checks each item against the quote in the plan.
- `.dev/reflect/`, `artifacts/` and `progress.md` are removed from the sandbox for every arm (H4).
- The sandbox is a pre-implementation checkout (H3).
- Regexes and recipes are frozen (hashed) before arm runs.

**Arms.**

| Arm | Panel | Redesign | Runs per package |
|---|---|---|---|
| A0 | ember + 2x luna | None (harness fixes only) | 8 |
| A1 | ember + 2x luna | CRS | 8 |
| A2 | ember + 2x luna | BLV | 8 |
| A3 | sonnet + 2x luna | None (comparison only, not a candidate for adoption) | 8 |

Total: 3 packages × 8 runs × 4 arms = 96 panel runs.

**Consistency measure.** For each package and arm:
- Mean items found per run out of the ground-truth count for that package.
- Stable hit rate: the share of ground-truth items found in at least 6 of 8 runs. Higher is more consistent.
- Run-to-run Jaccard of the set of found items, averaged over pairs of runs.
- Blocking false positives per run (findings the blind judge marks wrong and blocking).
- Elapsed median per run, and the 90th percentile.

**Pre-registered decision rule.** Stated before the runs.
1. Pooled hold-out mean items found per run for the redesign is at least 1.0 higher than A0. The 95% bootstrap confidence interval (resampling packages, not runs) has a lower bound above 0.
2. Stable hit rate is at least 0.15 higher than A0.
3. Blocking false positives per run are at most 1.0 higher than A0.
4. Elapsed median is at most 1.35 × A0 median, in each package.
5. No package has a mean at least 1 item lower than A0.

If both CRS and BLV pass, adopt the one with the higher pooled mean. If the two differ by less than 0.3, adopt CRS (simpler, one stage). If neither passes, adopt neither; report the harness-only result. A run killed by the timer counts as an elapsed failure, not as a missed item.

**Power note.** Eight runs per package is small. A difference of 1 item per run across three packages is detectable only if the run-to-run SD is near 0.6. The validation report says so if the interval is wide.

## 5. Numbered, testable requirements

1. The redesigns must not contain ground-truth quotes, task numbers, or package-specific file names in any instruction text. Test: a grep of the brief templates for the names of the eight hold-out and derivation packages returns no hits.
2. Each defect class in section 2 must map to exactly one recipe template. Test: the helper emits at least one item for each class when given a fixture that has that class.
3. The helper must be deterministic: the same candidate and seed produce the same item list (byte-identical). Test: two runs on one fixture compare equal.
4. The item list must be capped at 60 items and 10 KB. Test: a fixture with 200 universal sentences yields at most 60 items and reports the count dropped.
5. Reviewers must remain read-only. Test: the launch line keeps `--disallowedTools Edit Write NotebookEdit`, and a reviewer that writes to the candidate is recorded as a failed run.
6. Findings must keep the findings-v1 schema: anchor 12 to 200 characters, claim 300 or fewer, refs 8 or fewer, id 16 characters or fewer. Test: the existing `findings.py` fixtures pass unchanged.
7. The coverage block must be ignored by the merge step. Test: a report with a coverage block and a findings block merges to the same result as the findings block alone.
8. Every item must receive a verdict or `unchecked`. An item without any verdict is an error in the loop summary. Test: a fixture with a missing item line produces the error.
9. A defect verdict in coverage must have a matching findings line, or the audit flags it. Test: a fixture with a defect verdict and no finding is flagged.
10. Stage-1 timers: each reviewer is killed at 165 s (primary) and the kill is logged. Test: a sleep-stub reviewer is killed at the set time and the run continues.
11. BLV's verifier is blind to the lens name. Test: the verifier brief contains no lens name, reviewer id, or model name for the claim.
12. BLV's verifier cannot add claims. Test: a verifier output with a new claim is rejected by the merge.
13. The union in BLV must be deterministic. Test: the same input claims in any order produce the same union.
14. H1 to H4 must hold for every arm. Test: the arm manifest records the sandbox hash, the presence of `source.md` in the brief, and the absence of `.dev/reflect/`.
15. The validation must use hold-out packages only. Test: the arm manifest lists no package from the derivation set.
16. Ground truth must be frozen before arm runs. Test: the ground-truth file's hash is recorded before the first arm run, and it does not change.
17. Elapsed time must be measured from the helper start to the merge end, per package. Test: the timing log has one entry per run with the stage boundaries.
18. The decision rule in section 4 is applied as written. Test: the report states each of the five checks as pass or fail with its numbers.
19. Anti-overfitting: a recipe that cannot be expressed without a package name is not admitted. Test: a review of each recipe template by someone who did not write it finds no package-specific wording.
20. Wrong blockers must be counted separately from missed items in every arm. Test: the scoring table has separate columns for missed items and blocking false positives.

## Sources cited
- `.dev/brainstorms/20261113-223124-panel-process-redesign/seed-brief.md`
- `.dev/brainstorms/20261113-223124-panel-process-redesign/enrichment/investigation-generality.md` (sections 1 to 5)
- `.dev/brainstorms/20261113-223124-panel-process-redesign/enrichment/research-external.md` (sections 1 to 6)
- `.dev/brainstorms/20261113-223124-panel-process-redesign/enrichment/reused/investigation-designspec.md`, `investigation-alias-control.md`, `investigation-patterns.md`, `research-light.md`
- `.dev/eval-workspaces/tasklist-review-panel/20261111-a1/tools/run-reviewer.sh` (lines 13 to 17, 48, 57)
- `src/superclaude/rules/prompts/document_review_loop_prompts.md` (lines 31, 60, 70)
- `.dev/eval-workspaces/tasklist-review-panel/HANDOFF-review-panel-unification-run2.md` (lines 162, 209, 320 to 341)
- `.dev/eval-workspaces/tasklist-review-panel/20261111-a1/COMBO-REPORT.md` (section index only; final decision at line 289)

UNVERIFIED: the per-model medians for the timing table come from the seed brief and were not re-derived from the transcripts. The verifier time (25 to 30 s), the lens increment (10 s), and the brief-length overhead (18 s) are estimates. The `findings_v2.py` behaviour is taken from the handoff's grep-level note and was not opened.

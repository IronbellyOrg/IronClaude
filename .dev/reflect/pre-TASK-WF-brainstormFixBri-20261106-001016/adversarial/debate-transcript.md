# Adversarial Debate Transcript

## Metadata

- Pipeline: /sc:adversarial, Mode A (compare), Step 2 (debate) close-out by the debate-orchestrator
- Subject: three reviewer cards (variant-1/2/3-original.md) auditing the plan `TASK-WF-brainstormFixBri-20261106-001016` against its brief
- Depth: standard
- Rounds completed: 1 (advocate statements), 2 (rebuttals), 2.5 (invariant probe). Round 3 does not run at --depth standard.
- Convergence achieved: 100% (24 of 24 scored points agreed after Round 2; 87.5% after Round 1)
- Convergence threshold: 80%
- Focus areas: correctness, coverage, deviation-classification
- Advocate count: 3 (Variant 1 analyzer / sonnet; Variant 2 qa / haiku slot; Variant 3 refactorer / opus)
- Scored diff points (denominator): 24 (S-001..S-002, C-001..C-013, X-001..X-005, A-001..A-004)
- Final status: BLOCKED_BY_INVARIANTS (see Convergence Assessment)

## Round 1: Advocate Statements

### Variant 1 Advocate (sonnet)

# Round 1 - Advocate for Variant 1 (reviewer-1, analyzer, sonnet)

Paths below are relative to the repo root unless marked. "plan:N" is line N of `.dev/tasks/to-do/TASK-WF-brainstormFixBri-20261106-001016/TASK-WF-brainstormFixBri-20261106-001016.md`. Every file:line cited was Read in this round.

## Position summary

V1 has the widest coverage (11 of 13 content points, and the only card that touches all three of the unpassable Task 7 bullet, the unpinned owner rule and the `primary`/analyze wording), and its remedies are the ones that survive a changing tree (before/after diffs, scoped tests). Its weaknesses are real: it over-rated one finding (R1-1, wrongly stretched to Task 1), under-rated two (R1-4, R1-5), and its R1-2 overcounts untracked folders. V3 wins on the severity of the `primary` wording, V2 wins on the exact diagnosis of Task 7, and every card's remedy for the `primary` problem is incomplete.

## Steelman

### Variant 2 (qa, haiku slot)

Strongest version: V2 is the best guard-condition auditor. It shows that Task 7's third acceptance bullet (plan:98) fails twice on a correct run: the baseline already holds 950 staged `A` entries and 3 `R` entries under the archived P1 package (`artifacts/diagnostics.txt:3-4`), so "only the six files plus this package among tracked paths" is false before any edit, and the `done/` clause is at best arguable. That is the one acceptance bullet whose failure halts the run: `/sc:implement` marks an output that "contradicts the AC text" as `ac-outcome-missing` (`src/superclaude/skills/sc-implement-protocol/refs/qa.md:49`), which gives verdict `missing` (`qa.md:114`) and, after one fix pass, `E-HALT-QA` (`qa.md:245-247`). V2 also states exactly which task pins what (plan:33,60,74,84) to show the owner's conditional sentence is pinned nowhere in the primitives, verifies the brief's anchors (line 39 not 37, phrases list at 288), and supplies the concrete baseline (17, implying 18, `diagnostics.txt:11`). It uses no INFERRED tags, so every claim is checkable.

Critique: V2 is silent on the `primary`/analyze wording (C-007), which is the High item that would recreate the lc10 false FAIL in reverse. R2-1 gives no remedy. "Doubly unpassable" overreaches on the second clause: the staged entries are `A` and `R` (`diagnostics.txt:3-4`), not modifications, so only the first clause is certain. Rating R2-2 as P1 is arguable: the pinned phrase `write no nested directory` already pins the half the owner said the skill "must say" (`source.md:3`: "the auggie tier and the fallback_1 tier write no nested folder"); the converse ("only when /sc:analyze ran") is a restatement. R2-4 says the brief's placement procedure was "not evaluated" but does not decide whether the plan's choice is wrong. The hard-coded 17 is only valid if the tree stays as it is today (see A-004).

### Variant 3 (refactorer, opus)

Strongest version: R3-1 is the most consequential finding in the debate. Task 6's live-check sentence (plan:81) decides "no nested folder" by `quality_tier` ("a `primary` or `fallback_1` scan ... with no nested folder"). The skill defines `primary` as "first-choice source ran cleanly" (`SKILL.md:198`) and its codebase row's first choice is `/sc:analyze` OR auggie (`SKILL.md:187`). So a correct `/sc:analyze` run is also `primary`, and a future live plan copying that sentence would fail a correct analyze run: the same class of error the whole task exists to remove. The brief's own wording says "auggie primary scan" (`source.md:9`); the plan dropped "auggie" in the second sentence. V3 also pins down the Task 4 hole precisely (R3-3: the `fallback_1` assertion passes on old text and Task 1's clause is unpinned), and correctly catches that line 142 is in section 3.1 (spec:136-142), not section 6 (spec:215).

Critique: (a) The remedy is unimplementable. V3 says to decide by the `source` field of `enrichment_used`, but the contract defines `source: codebase | research-light | research-deep` (`SKILL.md:371-373`). It names the enrichment kind, not the tool, so it cannot tell analyze from auggie from codegraph. V3 tagged this Grounded. (b) R3-2 as P1 is overstated: the slice test (`tests/skills/test_codegraph_adoption.py:75-82`) asserts only that `codegraph_files`, `codegraph_search` and the "Glob for files matching topic keywords" line are in the Tier 2 block; an added bullet leaves all three intact. (c) R3-8 mischaracterises plan:21, which says no test *requires the two files to match*; `test_codegraph_adoption.py` reads the plugin file only for its `mcp-servers:` line (parametrized list at lines 115-132). (d) R3-6 proposes the shorter shared phrase "no nested directory", which would weaken the pin; that contradicts R3-3's own request for tighter scoping. (e) V3 never mentions Task 7's bullet 3 (C-001), the one criterion that cannot pass, so its "fix R3-1 and R3-2 first" list would still stop at Task 7.

## Strengths claimed

1. Widest coverage. V1 raised 11 of 13 content points (C-001 to C-010 and C-013; only C-011 and C-012 are missed). V2 raised 9, V3 raised 9. It is the only card with all of: Task 7 bullet (R1-2), unpinned owner rule (R1-4), `primary`/analyze conflict (R1-5). Evidence: variant-1-original.md R1-1 to R1-10.
2. Robust remedy for the Task 7 bullet. R1-2 says to compare `git status` before and after instead of asserting an absolute list. That works whatever the baseline holds; V2's finding has no remedy, and absolute numbers (950 entries, 17 cases) break if the tree changes (A-004). The baseline is real: `diagnostics.txt:3-7`.
3. Honest tagging. R1-5 is tagged INFERRED because "a checker would misread this" is a prediction, not a quote. V3 tagged R3-1 Grounded although its remedy is contradicted by `SKILL.md:371-373`. V1's tagging was the better calibrated of the two on this point.
4. Calibrated on the test-run omission (C-003/X-002). `test_codegraph_adoption.py:75-82` and `test_tier2_tavily_consistency.py:40-53` cannot be broken by the planned edits (see A-001), so P2 ("add to the run list") is right; V3's P1 is not.
5. Scoped-pin remedy with a ready pattern. R1-3 points to the `_section(text, start, end_pattern)` helper (`test_codegraph_adoption.py:56-59`) and the Tier 2 slice (`:75-82`). Task 4's file-wide `writes no nested directory` count (plan:60) is satisfied by two copies anywhere in `handoff-routing.md`, e.g. both in one tier.
6. Verified the coupling points. R1-9: line 711 is a lambda on a synthetic section (`test_worker_contract.py:704-711`, section at 667-677), so it needs no change; the real coupling is `UNATTENDED_EXPECT["brainstorm"]` at 286-297, which `_removals()` (519-527) and the parametrized test (559-568) pick up on their own. That confirms Task 5's "do not add a mutation by hand".
7. The Tier 2 list ends with the Activation bullet (`handoff-routing.md:31`), not the `quality_tier` line (`:30`), contrary to plan:39 (R1-10, shared with V2).

## Weaknesses identified

1. R1-1 is partly wrong. It says Task 1's first acceptance clause also passes on the old text. Plan:33 scopes that clause to the `Under --unattended` paragraph (`SKILL.md:195`), and that paragraph contains neither `fallback_1` nor `write no nested directory`, so it fails on old text. The only true part is that the Task 4 assertion on the whole Wave 2A section is vacuous (`SKILL.md:199` is inside Wave 2A, lines 175-208). V3's version ("Task 1's clause stays untested") is the accurate one.
2. R1-1 is over-rated at P1. Plan:65 says the pre-change text fails "them"; the test as a whole still fails on old text because of `write no nested directory`. The defect is a false sentence in an acceptance criterion plus a weak pin, so P2 (as V2 and V3 rated it).
3. R1-2 lists "untracked .dev/reflect/pre-* folders" as an obstacle. The clause says "among tracked paths" (plan:98) and those entries are `??` (`diagnostics.txt:5-7`). V1 also did not separate the first clause (certainly false) from the `done/` clause (arguable); V2 did.
4. R1-4 (owner rule unpinned) was rated P2 although the orchestrator scores it High. The finding and remedy are right; the rating is low next to V2.
5. R1-5 (`primary` wording) was rated P2 INFERRED although it is the item that repeats lc10 in reverse. Its remedy ("say an auggie scan (tier primary)") restores the brief's qualifier (`source.md:9`) but does not give a checker a way to tell analyze from auggie, since both record `primary`.
6. Padding. R1-9 is a "plan is silent" note about a line that needs no change, and R1-10 bundles two unrelated nits (the "do not edit any file" wording and the "ends with" wording). V1 missed C-011 (wrong section label) and C-012 (verb-form fragility).
7. No test was run by V1 or anyone else; every test-behaviour claim is read from source.

## Concessions

- V3 is right that the `primary`/analyze wording is a serious defect (C-007, X-003), and right on C-011 (line 142 is in section 3.1, spec:136-142) and on the missing Task 1 pin (C-002). V1 under-rated the first.
- V2 is right that Task 7's first clause fails by itself (X-005) and right that the failure should be stated per clause; V1's R1-2 was less exact and overcounted untracked paths.
- V1 was wrong on Task 1's clause (X-001) and over-rated R1-1.
- The fix for C-007 is not what any card said. A fallback_1 scan is recorded `fallback_1` and writes no nested folder, which is safe to state. A `primary` scan may be analyze or auggie, so the live-check wording must not tie "no folder" to `primary`. It should say: the nested folder is never required; if it is present it must hold its own contract and be listed in `artifacts`; whether `/sc:analyze` ran is read from the worker session file (spec 7.2 step 5, spec:292-299), not from `quality_tier` or `source`.

## Shared assumptions

- A-001: ACCEPT. I read both tests. `test_codegraph_adoption.py:75-82` slices from `**Tier 2 (fallback_1)**: codegraph` to `^\*\*Final fallback` and asserts `codegraph_files`, `codegraph_search` and "Glob for files matching topic keywords"; a bullet added inside Tier 2 keeps all three. `test_tier2_tavily_consistency.py:40-53` only forbids `tavily-extract/map/crawl` in SKILL.md; the planned text names none. Caveat: the bullet must go inside the Tier 2 list (before `**Final fallback**`, `handoff-routing.md:33`) and must not touch the Glob line. Not executed; still cheap to add to Task 7's run list.
- A-002: QUALIFY. `/sc:implement` uses an LLM reviewer against each AC (`SKILL.md:9`; `qa.md:49`), not a mechanical checker, so a bullet that contradicts the tree will most likely be marked `ac-outcome-missing` and lead to the retry ladder and `E-HALT-QA` (`qa.md:114,245-247`), but a reviewer could read it semantically and pass it. Either way it is a P1 process risk (an owner Ruling path exists, `qa.md:219`), not a data risk.
- A-003: ACCEPT. Exact-substring phrase pins are this repo's convention (`test_worker_contract.py:508-509`: `assert phrase in text`) and `_remove` is a plain `str.replace` (`:530-531`). Limit: a substring proves presence, not meaning, so the pin must be scoped to the right section (C-005) and cover the conditional clause (C-004).
- A-004: QUALIFY. The baseline moves: sibling sessions stage and archive in this tree, and `diagnostics.txt` was captured at one instant (00:14Z). Baseline-dependent checks should capture their own before-state at the start of Task 7 (and the collect-only count before Task 5's edit) rather than assume today's numbers (950 entries, 17 cases).

## Diff-point positions

| Point | Superior position | One-line evidence |
|---|---|---|
| S-001 | split | V1 has the widest coverage (11/13 content points); V2's two P1s are the best calibrated; V1's R1-1 and V3's R3-2 are over-rated. |
| S-002 | V1 | V1's INFERRED on R1-5 was honest; V3 tagged R3-1 Grounded while its remedy (decide by `source`) is contradicted by `SKILL.md:371-373`. |
| C-001 | split | V2 diagnoses it more exactly (first clause false on its own, `diagnostics.txt:3-4`); V1 gives the working remedy (before/after diff) but wrongly counts untracked `??` (`diagnostics.txt:5-7`). |
| C-002 | V3 | V3 sees both the vacuous `fallback_1` assertion (`SKILL.md:199` is in Wave 2A) and the unpinned Task 1 clause, at P2; V1's P1 and its Task 1 claim are wrong (plan:33 scopes to `SKILL.md:195`). |
| C-003 | split | V1 and V2 rate it P2, which is right (the test cannot break, A-001); the omission is a verification gap, not a failure risk. V3's P1 is over-rated. |
| C-004 | split | V2 states exactly which tasks pin what (plan:33,60,74,84); V1 gives the concrete remedy (a second exact phrase); the sentence is a restatement of the pinned half, so P1 vs P2 is arguable. |
| C-005 | split | V1 and V3 are equal: the `grep -c` and the "at least twice" test are file-wide (plan:42,60); scope with `_section` (`test_codegraph_adoption.py:56-59`). |
| C-006 | V1 | Defensible: spec spec:376 maps the nested propagation rule (2.1) to AC-2.1; 7.2 has no per-command extras table (spec:281-286). A pointer from 7.2 step 4 is the cheap addition. Concede source.md:9 names two other destinations. |
| C-007 | split | V3 right on severity (`SKILL.md:187,198`: analyze is also `primary`); V1 right that it needs the qualifier "auggie" (`source.md:9`); neither remedy works (`source` is the enrichment kind, `SKILL.md:371-373`). |
| C-008 | split | V1 and V2 both say record the before-count (V1: "adds exactly one id"; V2: 17 -> 18, `diagnostics.txt:11`); capturing it at run time is the robust version. |
| C-009 | split | V1 and V2 equal: Tier 2 ends with the Activation bullet (`handoff-routing.md:31`), Tier 1 with `quality_tier` (`:22`). |
| C-010 | split | V1 and V2 equal on the line offsets (test at 39 not 37, `test_brainstorm_protocol.py:39`; phrases list at 288, `test_worker_contract.py:286-292`); V1 adds that 711 is a synthetic mutation (`:704-711`). |
| C-011 | V3 | Line 142 is in `### 3.1` (spec:136-142); the section 6 table starts at spec:215. Only V3 saw it. |
| C-012 | none | Plan names each file's own verb form (plan:30,39,47); V3's shorter shared phrase would loosen the pin and contradicts its own R3-3. |
| C-013 | V1 | V1 and V2 name the two extra test files correctly; V3's R3-8 misreads plan:21 (it says no test *requires the two to match*; `test_codegraph_adoption.py` reads the plugin file only for `mcp-servers:`, lines 115-132). |
| X-001 | V3 | Task 1's clause is not vacuous (`SKILL.md:195` lacks `fallback_1`), but nothing pins it; V3's "stays untested" is accurate, V2 is narrowly right, V1 is wrong. |
| X-002 | V1 | P2: an added bullet inside Tier 2 cannot break `test_codegraph_adoption.py:75-82`. |
| X-003 | V3 | Real and serious: it would reproduce the lc10 false FAIL for an analyze run (`SKILL.md:187,198`); V2 missed it; V1 under-rated it. |
| X-004 | V1 | Defensible (spec:376 maps 2.1 to AC-2.1) but undocumented in the plan; V3's "wrong spot" overstates, V2 never decides. |
| X-005 | V2 | The first clause fails by itself (staged `A`/`R` entries are tracked, `diagnostics.txt:3-4`); the `done/` clause depends on how "modified" is read, so V2's "doubly" overreaches slightly. |
| A-001 | ACCEPT | Slice test and Tavily test read; planned edits keep every asserted string (`test_codegraph_adoption.py:75-82`, `test_tier2_tavily_consistency.py:40-53`). |
| A-002 | QUALIFY | `/sc:implement` uses an LLM reviewer (`qa.md:49,114`), so literal reading is likely but not guaranteed; halt path at `qa.md:245-247`. |
| A-003 | ACCEPT | Repo convention is `assert phrase in text` (`test_worker_contract.py:508-509`); scope and coverage still need care. |
| A-004 | QUALIFY | `diagnostics.txt` is one instant (00:14Z); capture before-state at run time instead of hard-coding 950 or 17. |

### Variant 2 Advocate (haiku slot)

# Round 1 — Advocate for Variant 2 (reviewer-2, qa persona, haiku slot)

## Position summary

V2 is the precision card: all 8 of its findings re-verified on disk with zero overclaims, it holds the two strongest coverage findings (C-004 at P1 — the brief's core sentence pinned by no test; C-001 — Task 7's third AC unpassable), and it is the only card that drew the Task 1 / Task 4 vacuity boundary correctly. Its cost is real: the all-Grounded discipline left the one High-severity wording bug (C-007/X-003) unreported, and two of its findings stop at diagnosis without a remedy.

## Steelman

**V1 (analyzer).** V1 is the broadest card and the only one that touched every defect class: plan mechanics (baseline R1-6, line anchors R1-9, artifacts wording R1-10), the test-set omission (R1-7, both files named), the routing-ref scoping remedy (R1-3 — the best C-005 fix: one bullet per tier, scoped to the codebase section, with the helper pattern in test_codegraph_adoption.py:56-59 as the model), and — via R1-5 — the first sighting anywhere of the tier-wording conflict that V3 later proved is a P1 bug. A reader of V1 alone would have been told to fix the primary/analyze wording, the unpassable AC, and the missing tests. That is genuine coverage. Critique: R1-1 overclaims. It asserts Task 1's first acceptance clause is also vacuous, but plan:33 scopes that clause to "the Wave 2A paragraph under `--unattended`" (SKILL.md:195), which does not contain `fallback_1`; only the section-wide Wave 2A view (which includes the quality-tier legend at SKILL.md:199) does. The diff analysis (X-001) confirms this. The overclaim matters: it inflates the vacuity finding and would send an implementer to "fix" a clause that already discriminates. R1-5 is also tagged INFERRED on a fact that was fully groundable by reading SKILL.md:187 and 198 — and its P2 undercalls what V3 showed is a checker-breaking wording bug.

**V3 (refactorer).** V3 found the single most important correctness issue in the debate: R3-1 shows Task 6's own new wording ("a `primary` or `fallback_1` scan is recorded as the tier used, with no nested folder") fails a correct `/sc:analyze` run, because `primary` means "first-choice source ran cleanly" (SKILL.md:198) and the codebase row's first choice is `/sc:analyze` OR auggie (SKILL.md:187); the remedy — decide by the `source` field of `enrichment_used`, not `quality_tier` — is exactly right, and note the brief itself says "auggie primary" (source.md:9) and the plan dropped the qualifier. V3 is also the only card to catch the spec-142 section mislabel (R3-4) and to propose the structurally correct placement split for Task 6 (R3-5). This is the only card that found a defect in the plan's new text rather than only in its checks. Critique: V3 missed C-001 entirely — the unpassable Task 7 AC is a P1 blocker under any literal reading and V3 is silent on it. It rated C-003/X-002 P1, but reading test_codegraph_adoption.py:75-82 shows the Tier 2 slice test asserts presence of `codegraph_files`, `codegraph_search` and the Glob sentence — none removed by adding a bullet — so P1 overstates (the calibrator's own note agrees). It also missed C-009, and R3-9 is INFERRED drift speculation about a clause the plan does carry elsewhere (plan:30).

## Strengths claimed

1. **100% verification rate.** Every V2 finding checks out against the files: R2-1 (diagnostics.txt:3-4; plan:98), R2-2 (plan:33 "states" with no pinned substring; plan:60; plan:74), R2-3 (SKILL.md:199 sits inside the Wave 2A section the test slices), R2-4 (spec lines 321-322 AC-1.5/1.6, line 376 maps the 2.1 rule to AC-2.1), R2-5 (test_codegraph_adoption.py:20-23; test_tier2_tavily_consistency.py:19,49), R2-6 (handoff-routing.md:30-31), R2-7 (diagnostics.txt:11 "17/394"), R2-8 (all anchors re-confirmed: test_brainstorm_protocol.py:39,44; test_worker_contract.py:286-292,711; SKILL.md:195; brainstorm.md:157; spec:62,142). Neither opposing card is clean: V1 carries the R1-1 error, V3 carries the X-002 overrating.
2. **The unique high-value contribution (U-001).** R2-2 is the only finding that states the plan's central coverage hole: the brief's core requirement — the nested folder exists only when `/sc:analyze` ran — is pinned by no exact-substring test in any primitive (Task 1's AC says the paragraph "states" it, plan:33; Task 4 pins `fallback_1`/`write no nested directory`, plan:60; Task 5 pins `writes no nested directory`, plan:74). The diff analysis scores C-004 High, matching V2's P1, not V1's P2.
3. **Correct severity and precision on C-001/X-005.** R2-1 identifies that both clauses fail: staged `A` entries under `.dev/tasks/done/` are tracked paths, so "only the six files plus this package among tracked paths" fails on its own, independent of how "modified" is read. V1 said "cannot pass" without isolating the operative clause; V3 said nothing.
4. **The only card with the right vacuity boundary (X-001).** V2 restricted the vacuity claim to Task 4's section-wide assertion and did not extend it to Task 1's paragraph-scoped clause — the exact distinction SKILL.md:195 vs 199 draws, and the one V1 got wrong.
5. **Concrete where others were abstract (C-008).** V2 is the only card citing the actual collect-only baseline (17, diagnostics.txt:11), turning "needs a baseline" into "expect 18 after the edit".
6. **R2-5's inversion is the sharpest framing of the test-set gap (C-013).** The one test the plan runs that is not an edited file's guard — test_routing_plugin_parity.py — reads none of the edited files, while two tests that do read them are not run. That inversion, not the file list alone, is what makes the omission visible.
7. **R2-8 cleared the brief's anchors.** By verifying 44, 292, 711, SKILL 195, command 157 and spec 62/142, V2 prevented false-positive line-number findings (line 711 is a synthetic mutation, correctly needing no change) — pruning matters as much as adding.

## Weaknesses identified

1. **Silent on C-007/X-003 — the biggest miss in the debate.** Task 6's proposed sentence decides by `quality_tier`, but a `/sc:analyze` run is also `primary` (SKILL.md:187 OR-row plus SKILL.md:198's definition), and source.md:9's own wording ("a fallback_1 or auggie primary scan") shows the plan dropped the "auggie" qualifier. A QA card whose focus is correctness should have caught a checker that fails a correct run; the zero-INFERRED discipline explains (the issue needs one inferential step from two file reads) but does not excuse it.
2. **Missed C-011.** R2-8 verified that spec line 142 is the brainstorm row but never checked the plan's label for it; plan:81 calls it "the section 6 table" while line 142 is in section 3.1 (spec:136) and section 6 starts at 215 (its brainstorm text is the P2 row at 222). V3 caught it.
3. **R2-4 diagnoses without prescribing.** "The plan never records that the brief's procedure was considered" is true and evidenced, but V1's pointer-from-7.2 remedy and V3's split (general rule in 2.1, live-check sentence in section 7) are actionable; V2's is not.
4. **R2-2's P1 is borderline.** Task 1's "and states that the nested directory exists only when /sc:analyze ran" is an acceptance criterion the implement protocol does read (per-task compliance QA); the unpinned-ness is therefore a post-implementation drift hole more than an implement-time hole. P1 is defensible (the diff analysis scores C-004 High, and the plan's whole purpose is that sentence) but should be argued as drift risk, not as "every plan check passes" unqualified.
5. **R2-1's "doubly unpassable" overstates clause 2.** Staged `A` entries are additions; whether they count as "nothing under `.dev/tasks/done/` is modified" is reading-dependent (the diff analysis's own X-005 note). The first clause is decisive and sufficient; claiming both adds rhetorical weight, not correctness.
6. **R2-6 confirms F-2 but offers no fix** for the grep -c detection gap it itself names (a per-list scoped check would close it — V1's R1-3 remedy applies).

## Concessions

- V3 is superior on C-007, X-003, C-011 and X-004: it found the only defect in the plan's new wording, the only section-label error, and the best placement remedy. If the merge takes one thing from V3, it is the `source`-field rule.
- V1 is superior on C-005's remedy (scope the routing-ref pin to the codebase section, one per tier) and on breadth: its R1-5, though mis-tagged and undercalled, saw the C-007 issue before anyone else.
- V2's card is narrower than both: 8 findings versus 10 and 9, no INFERRED extrapolations, and two findings (R2-4, R2-6) that stop at diagnosis.
- V2's two P1 ratings are each arguable down one notch (R2-2 as above; R2-1's clause-2 certainty), though both remain substantively correct.

## Shared assumptions

- **A-001: ACCEPT.** I read both tests. test_codegraph_adoption.py:75-82 asserts presence of `codegraph_files`, `codegraph_search` and "Glob for files matching topic keywords" in the Tier 2 slice — an added bullet removes none; its other brainstorm assertions hit the `mcp-servers:` frontmatter line (131) and a `mcp__serena` scan (141-143), untouched because Task 1/2/3 say "change nothing else". test_tier2_tavily_consistency.py:49-53 forbids `tavily-extract/map/crawl` in SKILL.md — the planned sentences contain none. The assumption holds for the planned wording; it would break only on out-of-scope edits, which is precisely why Task 7 should still run them (R2-5).
- **A-002: QUALIFY.** Per-task compliance QA does read each bullet literally, so an unpassable bullet blocks completion and C-001 is a P1 blocker. But "lists, among tracked paths, only the six files ... plus this package" admits a charitable reading that treats the staged prior package as outside "this change", which would demote C-001 toward P2; the finding's severity rides on the literal reading being the operative one.
- **A-003: ACCEPT.** Exact-substring pinning is the house style for these drift guards (test_brainstorm_protocol.py:44; test_worker_contract.py:508-509), so the remedy shape "add a phrase" is right. V3's verb-variant note (C-012) tunes which phrase, not whether the method is correct.
- **A-004: QUALIFY.** The staged archive is one commit away from vanishing (recent commit 0b443745 already landed the prior package's plan; the 950 staged entries are its pending archive move), so every absolute baseline — including V2's own R2-1 and the 17-count in R2-7 — is time-dependent. Plans here should capture before/after state, not assume today's tree.

## Diff-point positions

| Point | Superior position | One-line evidence |
|---|---|---|
| S-001 | none | All three cards carry 2 P1; the count difference is bundling (V1's R1-10 merges two findings), not coverage. |
| S-002 | V2 | V2's 8/8 findings re-verified here; V1's one INFERRED (R1-5) undercalled a groundable bug, V3's (R3-9) is Low drift speculation. |
| C-001 | V2 | diagnostics.txt:3-4: 950 staged `A` entries are tracked paths, so the first clause fails before the done/ clause is even read; V3 silent. |
| C-002 | split (V2/V3) | V2 correctly limits vacuity to Task 4's section-wide assertion (SKILL.md:195 lacks `fallback_1`, :199 has it); V3 adds that Task 1's paragraph-level pin never materializes. |
| C-003 | split (V1/V2) | Both name both missing files at P2, matching the A-001 read; V3's P1 overstates — the Tier 2 slice test asserts presence, which an added bullet keeps. |
| C-004 | V2 | plan:33 "states" with no pinned substring, plan:60/74 pin only the tier phrases; P1 matches the diff analysis's High severity, V1's P2 undercalls, V3 absent. |
| C-005 | split (V1/V3) | V1's R1-3 scoping remedy is the fix; V2's R2-6 contains the detection-gap half ("grep -c cannot detect a bullet placed in the wrong list") but no remedy. |
| C-006 | split (V1/V3) | V3's split (general 2.1 rule, live-check sentence in section 7) and V1's pointer are actionable; V2's R2-4 is true (plan never evaluates the brief's procedure, source.md:9) but prescribes nothing. |
| C-007 | V3 | plan:81 decides by `quality_tier`, but `primary` covers `/sc:analyze` runs (SKILL.md:187 OR-row, :198 definition); source.md:9 says "auggie primary" and the plan dropped the qualifier; V2 silent — its largest miss. |
| C-008 | V2 | Only V2 cites the concrete baseline: diagnostics.txt:11 "17/394 tests collected", so the post-edit expectation is 18. |
| C-009 | split (V1/V2) | Both ground it (handoff-routing.md:30-31, Activation after quality_tier); V2 adds the grep -c detection-gap framing; V3 missed it. |
| C-010 | V2 | V2 confirms both offsets (test at :39 not 37; phrases list at :288 with the entry at :286) and clears the remaining anchors including synthetic line 711; V1 covers only 711; V3 silent. |
| C-011 | V3 | spec:136 (section 3.1) contains line 142; section 6 starts at 215 with its brainstorm text at 222 — V2's R2-8 verified the line anchor but not the plan's section label. |
| C-012 | V3 | Only raiser; "write" is not a substring of "writes" (plan:30 vs plan:39), a real if Low fragility inside the accepted method. |
| C-013 | V2 | V2's inversion — the run test (test_routing_plugin_parity.py) reads none of the edited files while the two not-run tests read them — is sharper than V3's plugin-copy subset or V1's file list. |
| X-001 | V2 | Task 1's clause is scoped to the SKILL.md:195 paragraph, which lacks `fallback_1`, so only V2's boundary (Task 4 vacuous, Task 1 not) is correct; V1 wrong, V3 vague. |
| X-002 | split (V1/V2) | P2 is right: test_codegraph_adoption.py:75-82 asserts presence of strings an added bullet preserves, so a break requires an out-of-scope edit — V3's P1 overstates. |
| X-003 | V3 | V2 was silent; V1 saw the tension as P2 INFERRED; only V3 grounded it and gave the `source`-field remedy. |
| X-004 | V3 | The brainstorm-specific live-check sentence is per-command material (AC rows replace 7.2 steps 3-4, spec:321-323); V3's split beats V1's pointer and V2's remedy-less "unevaluated". |
| X-005 | V2 | V2 nails the operative first clause (staged entries are tracked paths); its clause-2 certainty is reading-dependent, which V2's own "doubly" phrasing slightly overstates. |
| A-001 | ACCEPT | Both tests read; planned sentences add no forbidden token and touch no frontmatter, and the Tier 2 slice asserts presence only. |
| A-002 | QUALIFY | Literal per-bullet QA makes C-001 a blocker, but a charitable "outside this change" reading would demote it to P2. |
| A-003 | ACCEPT | Exact-substring pinning is house style (test_brainstorm_protocol.py:44; test_worker_contract.py:508-509); C-012 tunes the phrase, not the method. |
| A-004 | QUALIFY | The staged archive is one commit from vanishing (0b443745 already landed the prior plan); absolute baselines, including V2's, are time-dependent — use before/after captures. |

### Variant 3 Advocate (opus)

# Round 1, Advocate for Variant 3 (reviewer-3, refactorer, opus)

## Position summary (1-3 sentences)

V3 is the only card that caught the defect that would repeat the lc10 failure in reverse: the live-check sentence in Task 6 says a `primary` scan writes no nested folder, but an `/sc:analyze` run is also `primary`. That makes V3 strongest on correctness and on classifying the deviation (the plan dropped the brief's "auggie" qualifier). V3 is weakest on Task 7's git-status bullet, which it missed entirely, and it over-rated the missing `test_codegraph_adoption.py` run as P1.

## Steelman (one block per opposing variant)

**V1 (analyzer, sonnet).** The strongest form of V1's case is that it covers the most ground. It is the only card that raises both of the problems that block completion (the empty `fallback_1` assertion, R1-1, and the Task 7 status bullet that cannot pass, R1-2). It also spots the tier-wording conflict, R1-5, and proposes the smallest fix: write "an auggie scan (tier primary)". That fix stays closest to the brief, which itself says "a fallback_1 or auggie primary scan" (source.md:9). V1 also checks peripheral facts correctly: line 711 is a synthetic mutation, `COMMANDS_DIR` points at `src/`, and Task 7's "do not edit any file" conflicts with saving logs.
*Critique.* R1-1 is wrong on half its claim. It says Task 1's first acceptance clause is also vacuous, but plan:33 scopes that clause to "The Wave 2A paragraph under `--unattended`", and that paragraph (SKILL.md:195) does not contain `fallback_1`. Only Task 4's assertion is vacuous, because it checks the whole Wave 2A section (`_wave2a_section`, test_brainstorm_protocol.py:24-29), and line 199 of that section already holds `fallback_1`. V1 also rates R1-5 as INFERRED P2. The conflict is in fact Grounded: SKILL.md:187 offers `/sc:analyze` OR auggie as the first choice, SKILL.md:198 defines `primary` as "first-choice source ran cleanly", and plan:81 tells checkers that a `primary` scan has no nested folder. A checker that follows that text would fail a correct run, so the problem is P1.

**V2 (qa, haiku slot).** The strongest form of V2's case is that it alone treats the owner's core rule as unpinned (R2-2). Task 1's acceptance criterion only requires that the paragraph "states" that the nested directory exists only when `/sc:analyze` ran (plan:33). No task pins a substring for that clause in any primitive; Task 4 pins `fallback_1` and `write no nested directory` (plan:60), and Task 5 pins only `writes no nested directory` (plan:71). An implementer could therefore drop the actual owner decision and every check would stay green. V2 is also the most exact on Task 7: staged `A` entries are tracked paths, so the bullet's first clause fails as well (R2-1). Its baseline figure of 17 is the real number (diagnostics.txt:11).
*Critique.* V2 says nothing about the `primary`/analyze contradiction, which is the one defect that would make a future live check fail a correct worker. R2-2 is right that the rule is unpinned, but its remedy is the same shape as V1 R1-4 and V3 R3-6 (add an exact phrase), so U-001 is a matter of severity, not a unique insight. "Doubly unpassable" also depends on reading the staged `R` and `A` entries under `.dev/tasks/done/` as "modified". That reading is reasonable but not certain (X-005).

## Strengths claimed (numbered, with evidence)

1. **R3-1 is a real P1 correctness defect, and it is Grounded.** SKILL.md:187 sets the codebase row's first choice as "`/sc:analyze` ... OR `mcp__auggie__codebase-retrieval`". SKILL.md:198 defines `primary` as "first-choice source ran cleanly", and SKILL.md:201 records `enrichment_used: [{source, quality_tier}, ...]`. A clean `/sc:analyze` run is therefore `{source: analyze, quality_tier: primary}`. The second sentence of Task 6 (plan:81) reads "a `primary` or `fallback_1` scan is recorded as the tier used, with no nested folder". A P2 plan author who copies that sentence as a pass/fail extra would fail a correct analyze run that wrote `nested/analyze-1/`. That is the lc10 error with the direction flipped. The routing ref's Tier 1 is auggie only (handoff-routing.md:16-22), but the skill's matrix is what runs.
2. **Deviation classification: Drift, not a wording nit.** The brief says "a fallback_1 or auggie primary scan is recorded as the tier used" (source.md:9). The plan's copied extra drops "auggie" (plan:81). The first sentence of Task 6 keeps the qualifier ("on `quality_tier` `primary` through `mcp__auggie__codebase-retrieval`"), but the quoted extra, the text a live plan copies, does not. That is unauthorized loss of a constraint the brief named, which is Drift. Only V3 links this to the `source` field that actually tells the two cases apart (SKILL.md:201).
3. **R3-3 and X-001: V3 is the precise card on vacuity.** V3 says Task 4's `fallback_1` assertion proves nothing, and that Task 1's paragraph-scoped claim "stays untested". Both are true. Task 4 checks the whole section, and SKILL.md:199 already contains `fallback_1`. Task 1's acceptance criterion is scoped to the paragraph (plan:33), which lacks it at SKILL.md:195, so that criterion is not vacuous, but no test pins it at paragraph scope. V1 overstates the point and V2 understates it.
4. **R3-4 is a unique, checked label error.** Plan:81 calls line 142 "the `brainstorm` row of the section 6 table". In the spec, line 142 is under `### 3.1 Ready with brief constraints (12)` (line 136), and `## 6. Phased rollout` begins at line 215. No other card caught this.
5. **R3-5 makes the strongest placement argument.** The brief asks for "the live-check section ... if that is where per-command extras are defined, otherwise as a note in the P1 section" (source.md:9). Section 7.2 (spec:281) defines no per-command extras table, so the brief's fallback is a P1 note. The plan instead puts a brainstorm-specific live-plan instruction into the general 2.1 term definition (spec:62). Splitting the general rule (2.1) from the live-check sentence (7.2 step 4 or 7.3, spec:306) follows the brief's own procedure. V1 and V2 call the 2.1 placement "defensible" without testing it against source.md:9.
6. **R3-8 corrects the plan's stated reasoning.** Plan:21 implies that no test reads `plugins/superclaude/commands/brainstorm.md`. `test_codegraph_adoption.py:23,39,121` reads it (`_BS_PLUGIN_CMD`, both in `_ALL` and in `test_mcp_servers_gain_codegraph`). Nothing breaks, because the plugin file is not edited, but the premise is incomplete.

## Weaknesses identified (numbered, with evidence)

1. **V3 missed Task 7's third bullet (C-001 / X-005).** This is V3's largest omission. Today's `git status --porcelain` holds 950 staged `A` entries and 3 `R` entries under `.dev/tasks/done/TASK-WF-p1LivePlanBrief-` (diagnostics.txt:3-4, re-checked today with the same counts). These are tracked paths, so "lists, among tracked paths, only the six files ... plus this package" (plan:98) fails on a correct run. Also, the package itself is still `??` (untracked), so "plus this package" does not even describe it.
2. **V3 rated R3-2 too high.** I read both tests (see A-001). Adding a bullet inside the Tier 2 list keeps every assertion of `test_brainstorm_tier2_names_codegraph_files_and_search` true (test_codegraph_adoption.py:75-82). The edit cannot break `test_tavily_consistency` either (test_tier2_tavily_consistency.py:40-53). The omission is a coverage gap against the brief's "find every test that pins this wording" (source.md:7). It is not a missed break, so P2 is correct.
3. **V3 missed C-009 and C-010.** V1 and V2 both confirm that the Tier 2 list ends with the Activation bullet (handoff-routing.md:30-31) and that the plan's line numbers are stale (test at test_brainstorm_protocol.py:39, not 37). V3 said nothing about either.
4. **R3-9 is weak.** The command bullet's existing sentence "`adversarial_artifacts_dir` and the nested contracts are listed in `artifacts`" (brainstorm.md:157) is not contradicted once the appended clause says the auggie and fallback scans write no nested contract. The plural "the nested contracts" naturally means the ones that exist. Drift is possible but not shown, so the INFERRED tag fits and its Low value stands.
5. **V3's remedy for R3-1 is heavier than needed.** Deciding by `source` is robust, but `source` values are not enumerated anywhere I read (SKILL.md:201 gives only the shape). The brief's own wording, "auggie primary" (source.md:9), restored in plan:81, fixes the contradiction with a one-word change. V1's remedy (R1-5) is the smaller fix. Either is acceptable.

## Concessions

- C-001 belongs to V2 (most exact) and then V1. V3 has no position on it.
- The P1 on C-003 should come down to P2 (see A-001).
- U-001 (the unpinned core rule) is V2's. V3's R3-6 shared-phrase idea addresses the verb-form fragility, not the missing pin.
- V1 R1-5 found the same contradiction as R3-1, though it under-graded it.

## Shared assumptions (A-001 to A-004: ACCEPT/REJECT/QUALIFY + reason)

- **A-001: ACCEPT.** I tested this by reading both test files. `test_codegraph_adoption.py` slices from `**Tier 2 (fallback_1)**: codegraph` to `^\*\*Final fallback` and asserts only `codegraph_files`, `codegraph_search` and `Glob for files matching topic keywords` (lines 75-82). It asserts the `mcp-servers:` lines, which are unchanged (115-132), and no `mcp__serena` (141-143). `test_tier2_tavily_consistency.py:40-53` forbids only `tavily-extract/map/crawl` in SKILL.md. None of the planned texts touches these tokens, so the edits leave both passing. Consequence: C-003 / X-002 is P2, not P1. This conclusion comes from reading the tests, not running them; Task 7 should still run both.
- **A-002: QUALIFY.** `/sc:implement` does not judge semantically and let the bullet pass. Its retry adviser returns `dispute` "when the AC is contradictory or infeasible" (sc-implement-protocol/refs/retry.md:72), and a dispute naming the AC halts with `E-HALT-QA` for the operator (retry.md:107; qa.md:281). An unpassable bullet therefore blocks automatic completion through a halt rather than a literal fail. Either way the C-001 finding is a real blocker (P1).
- **A-003: QUALIFY.** Exact-substring pins are right for this repo's style (test_worker_contract.py:508-509 and `_removals`, 519-527). They are not enough when scoped to a whole section or file (C-002, C-005), and they fix verb forms (C-012). The remedy is substring pins plus correct scope plus one shared phrase for the owner's rule.
- **A-004: QUALIFY.** It holds right now: I re-ran `git status --porcelain` and got the same 950 `A` / 3 `R` / 4 `??` as diagnostics.txt:3-7. But nothing guarantees it at execution time, so the remedy for C-001 and C-008 should record the baseline inside Task 7 and Task 5 themselves (a before/after diff and a before-count) rather than depend on a figure captured earlier.

## Diff-point positions

| Point | Superior position | One-line evidence |
|---|---|---|
| S-001 | none | Count differences reflect scope, not quality; each card has 2 P1s. |
| S-002 | split (V1, V3) | V1 marks R1-5 INFERRED where it is Grounded; V3 marks R3-9 INFERRED correctly (brainstorm.md:157 shows no contradiction). |
| C-001 | V2 | Staged `A` entries are tracked paths, so plan:98's first clause fails too (diagnostics.txt:3-4; re-checked today). |
| C-002 | V3 | Task 4 scope is the whole section (test_brainstorm_protocol.py:24-29), with `fallback_1` at SKILL.md:199; the Task 1 paragraph at :195 lacks it. |
| C-003 | V2 | Both files named, P2 grade; A-001 shows no break (test_codegraph_adoption.py:75-82). |
| C-004 | V2 | Owner rule unpinned in every primitive: plan:33 "states", plan:60 and :71 pin other phrases only. |
| C-005 | split (V1, V3) | grep -c / ">= 2" is file-wide (plan:42,60); scope to the codebase section via `_section` (test_codegraph_adoption.py:56-59). |
| C-006 | V3 | source.md:9's fallback is "a note in the P1 section"; 7.2 (spec:281) has no extras table; 2.1 (spec:62) is a term definition. |
| C-007 | V3 | SKILL.md:187+198 make analyze `primary`; plan:81 says `primary` means no nested folder; source.md:9 said "auggie primary". |
| C-008 | V2 | Gives the actual baseline of 17 (diagnostics.txt:11); V1 and V3 only say it is missing. |
| C-009 | split (V1, V2) | Tier 2 ends with the Activation bullet (handoff-routing.md:31), not `quality_tier` (:30). |
| C-010 | V2 | Confirms test at test_brainstorm_protocol.py:39 and phrases at test_worker_contract.py:288. |
| C-011 | V3 | Line 142 is under `### 3.1` (spec:136); `## 6.` starts at spec:215. |
| C-012 | V3 | `write` vs `writes` are distinct substrings (plan:30 vs :39,:47); one shared phrase lowers the risk. |
| C-013 | V3 | test_codegraph_adoption.py:23,39,121 read the plugin brainstorm.md, contradicting plan:21's premise. |
| X-001 | V3 | plan:33 scopes Task 1 to the SKILL.md:195 paragraph, which lacks `fallback_1`; V1 wrong that it is vacuous. |
| X-002 | V1/V2 (P2) | A-001 read: no assertion in either test touches the new text. |
| X-003 | V3 | Contradiction is Grounded in SKILL.md:187,198,201 and plan:81; it reproduces lc10 in reverse, so P1. |
| X-004 | V3 | Plan never applies source.md:9's procedure; 2.1 is not the live-check home. |
| X-005 | V2 | First clause fails regardless of how "modified" is read; package is `??`, so "plus this package" is also off. |
| A-001 | ACCEPT | test_codegraph_adoption.py:75-82,115-143 and test_tier2_tavily_consistency.py:40-53 unaffected by planned text. |
| A-002 | QUALIFY | Infeasible AC leads to `dispute`, then `E-HALT-QA` (retry.md:72,107): blocks completion through a halt, so still P1. |
| A-003 | QUALIFY | Substring pins fit the repo, but need correct scope and one shared phrase. |
| A-004 | QUALIFY | Holds today (same 950/3/4 counts); record baselines inside Tasks 5 and 7. |

## Round 2: Rebuttals

### Variant 1 Advocate (sonnet)

# Round 2 - Advocate for Variant 1 (reviewer-1, analyzer, sonnet): rebuttal

Paths are relative to the repo root. "plan:N" is line N of `.dev/tasks/to-do/TASK-WF-brainstormFixBri-20261106-001016/TASK-WF-brainstormFixBri-20261106-001016.md`. "src:N" is `source.md` in the same folder. Every file:line below was Read or run this round unless marked "(round 1)".

## Response to criticisms

Criticisms of V1 made by Advocate 2 (A2) and Advocate 3 (A3), each answered.

| # | Criticism | From | Answer |
|---|---|---|---|
| 1 | R1-1 wrongly says Task 1's first clause is also vacuous | A2, A3 | CONCEDE. plan:33 scopes the clause to the `Under --unattended` paragraph, and `SKILL.md:195` has no `fallback_1`. The `fallback_1` string at `SKILL.md:199` is inside Wave 2A (lines 175-208), so only Task 4's section-wide assertion (plan:60) is vacuous. Task 1's clause fails on the old text but nothing pins it at paragraph scope (V3's wording). |
| 2 | R1-1 is rated too high at P1 | A2 | CONCEDE. The Task 4 test as a whole still fails on the old text because of `write no nested directory`, so the defect is a false sentence at plan:65 plus one dead assertion: P2. |
| 3 | R1-5 (`primary`/analyze wording) is under-rated at P2 and mis-tagged INFERRED | A2, A3 | CONCEDE the severity. `SKILL.md:187` offers `/sc:analyze` OR auggie, `SKILL.md:198` defines `primary` as "first-choice source ran cleanly", and plan:81's quoted extra says "a `primary` or `fallback_1` scan ... with no nested folder". That is a checker-breaking sentence in the text a live plan will copy: P1. PARTIAL on the tag: the premise is groundable, but what a checker would do with the sentence is a prediction. The tag should have been Grounded for the premise and INFERRED for the effect. |
| 4 | R1-4 (owner rule unpinned) is under-rated at P2 | A2 | CONCEDE, with a sharper reason than A2 gave (see New evidence 4): `src:6` asks that the fallback "lists no nested contract in artifacts", and no planned pin covers the contract half. |
| 5 | R1-2 (Task 7 bullet 3) counts untracked `??` folders and does not separate the two clauses | A2 (implied), A3 | CONCEDE. The clause says "among tracked paths" (plan:98) and the `.dev/reflect/pre-*` entries are `??`. V2 isolated the first clause better. The remedy (before/after diff of `git status`) stands. |
| 6 | V1 missed C-011 (section label of spec line 142) | A2, A3 | CONCEDE. Spec line 142 is in `### 3.1`; plan:81 says "section 6 table". |
| 7 | V1 missed C-012 (`write` vs `writes`) | A3 | CONCEDE and flip my round-1 position. See the C-012 row below. |
| 8 | C-006/X-004: V1 and V2 call the 2.1 placement "defensible" without testing it against `src:9` | A3 | PARTIAL. R1-8 did test it: 7.2 has no per-command extras table. I now also read spec 281-305 (7.2) and 306-327 (7.3): 7.3 holds per-phase AC rows, not per-command extras. So `src:9`'s first branch ("if that is where per-command extras are defined") is false and its second branch ("a note in the P1 section") applies. The 2.1 bullet is still defensible, because `spec:376` maps the nested propagation rule to AC-2.1 and `spec:325` names brainstorm's nested call. It is not the destination `src:9` names, and V3's split (general rule in 2.1, live-check sentence in 7.2 step 4 or the P1 rows) is the better answer. I move from V1 to split. |
| 9 | C-013: R3-8 shows `test_codegraph_adoption.py` reads the plugin `brainstorm.md`, contradicting plan:21 | A3 | REBUT (this is A3's claim, not a criticism of V1, but I rely on the answer). plan:21 says "no test requires the two to match". `test_codegraph_adoption.py:23,39,121` reads the plugin file only for the `mcp-servers:` line (`:131`) and the `mcp__serena` scan (`:143`). Both are untouched because the plugin file is not edited. R3-8 misreads the premise. |
| 10 | C-010: "V1 covers only 711" | A2 | REBUT in part. V1's card confirms the F-4 line numbers (`variant-1-original.md:60`) and names the coupling point at `test_worker_contract.py:286-297` (R1-9). It did not give the two offsets (39, 288) as precisely as V2. Equal enough: split. |
| 11 | C-008: only V2 cites the concrete baseline (17) | A2 | PARTIAL. 17 is a real number (`diagnostics.txt:11`), but all four advocates say A-004 is QUALIFY: baselines move. V1's remedy (record the before-count at run time) is the one that survives a changed tree. V2 gives the number, V1 the safe method: split. |
| 12 | S-002: V2's zero INFERRED tags is the better discipline | A2 | REBUT. V2's R2-1 tags "doubly unpassable" Grounded though its second clause depends on how "modified" is read (A2 concedes this). Tagging was imperfect on all three cards. See S-002 below. |
| 13 | C-001: V2 is the most exact on Task 7 bullet 3 | A2, A3 | CONCEDE on the first clause (see Updated assessment (b)). The remedy is V1's. |
| 14 | X-001: V1 is wrong that Task 1's clause is vacuous | A2, A3 | CONCEDE (same as 1). |

## Updated assessment

Variant 2 (qa). Its diagnoses are the most precise of the three: C-001's first clause, the Task 4 versus Task 1 boundary (X-001), the stale offsets. Its R2-2 is better than I rated it, because the unpinned piece is the "no nested contract / artifacts" half that `src:6` asks for (New evidence 4). Its weaknesses stand: silent on C-007, which is the one defect that reverses lc10; "doubly unpassable" overreaches on the `done/` clause; R2-1 and R2-4 give no remedy.

Variant 3 (refactorer). R3-1 is the most important diagnosis in the debate, and I now rate it P1 as V3 did. Its remedy fails: `SKILL.md:371-373` defines `source: codebase | research-light | research-deep`, so `source` cannot tell `/sc:analyze` from auggie, and V3's Grounded tag on the remedy is wrong. R3-2 at P1 is overrated (confirmed again, New evidence (c)). R3-8 misreads plan:21. R3-4, R3-5 and R3-6 are valid and the last two change my positions. V3 never mentions Task 7 bullet 3, which is the item that halts execution.

My own card. Widest coverage, and its remedies for C-001, C-005 and C-008 are the ones that survive a changing tree. It was wrong on Task 1's clause, under-rated R1-4 and R1-5, and missed C-011 and C-012.

## New evidence

(a) What the `source` field can hold. `SKILL.md:371-373` reads `enrichment_used: - source: codebase | research-light | research-deep` and `quality_tier: primary | fallback_1 | skipped`. `/sc:analyze` and auggie are both `source: codebase`, and a clean run of either is `quality_tier: primary` (`SKILL.md:187,198`). No field in `enrichment_used` can tell them apart, and the Wave 2A rows (`SKILL.md:183-191`) never record the tool. The routing ref names only auggie as Tier 1 (`handoff-routing.md:16`), so the product text itself does not say which tier an analyze run records. V3's remedy (decide by `source`) and V1's remedy (say "an auggie scan (tier primary)") both fail as a checker rule: the first has no discriminating value, the second names a tool the checker cannot read from the contract. The only record of which tool ran is the worker's session file (spec 7.2 step 5, `spec:291-300`, which records `tool_use` blocks with a `name`, `spec:302`), or the presence of `nested/analyze-<n>/` itself, which is the thing under test.

A refinement nobody raised (INFERRED, from `SKILL.md:199` "`fallback_1` - primary failed"): if `/sc:analyze` was the first choice, ran, and failed, the run records `fallback_1` and `nested/analyze-1/` may exist. So "a `fallback_1` scan has no nested folder" is also over-broad as a live-check rule. The fallback tier writes none itself; the folder depends on whether analyze was tried.

(b) Staged `A` entries and plan:98's first clause. Run today: `git status --porcelain` gives 950 `A`, 3 `R`, 4 `??`; `git ls-files .dev/tasks/done/TASK-WF-p1LivePlanBrief-20261105-164506` prints 953, which is 950 + 3 and means those paths are in the index and so are tracked. `git ls-files` on this plan's package prints 0, so the package is untracked (`??`), which also differs from CLAUDE.md's "`.dev/tasks/` is always staged". Result: the first clause ("lists, among tracked paths, only the six files ... plus this package") fails on today's tree under any literal reading, because 953 other tracked paths are listed. The second clause ("nothing under `.dev/tasks/done/` is modified") is reading-dependent: the codes are `A `/`R `, not ` M`. So X-005: V2 is right on the first clause, and "doubly" overreaches. The failure also depends on the tree at execution time (A-004): once the staged archive is committed, the first clause passes. A before/after diff of `git status --porcelain` is correct in both states. Consequence if left as written: `ac-outcome-missing` (`qa.md:49`), the retry ladder, and `E-HALT-QA` (`qa.md:247`, `retry.md:107`).

(c) Can the planned edits break `tests/skills/test_codegraph_adoption.py`? No. Read in full. The Tier 2 slice test (`:75-82`) splits the routing ref at the first `**Tier 2 (fallback_1)**: codegraph` (heading at `handoff-routing.md:24`; the research tiers' headings read `Tier 2 (fallback_1)**: Direct WebSearch`, so no earlier match) up to `^\*\*Final fallback` (`handoff-routing.md:33`) and asserts only `codegraph_files`, `codegraph_search` and `Glob for files matching topic keywords` (all in lines 26-27). A bullet added inside lines 25-31 keeps all three; a bullet placed after line 33 is outside the slice. The other brainstorm tests there check the `mcp-servers:` line (`:131`) and the absence of `mcp__serena` (`:143`) in SKILL.md, the routing ref, and both command files. Task 1-3 add neither. The one way to break the slice test is for an implementer to edit line 26 or 27 or the heading, which Task 2 forbids by "do not touch" scope. A-001 holds, and C-003/X-002 is P2.

One further existing guard that both other cards missed: `test_brainstorm_protocol.py:50-54` forbids `search_depth:`, `extract_depth:`, `max_results:`, `tavily-map` and `tavily-crawl` anywhere in the Wave 2A section (`_FORBIDDEN`, `:15-21`). Task 1's text adds none, and the file is already in Task 7's run list.

(d) `src:6` and C-004. `src:6` says the skill must "also write no nested folder and list no nested contract in artifacts". The only new pin on the skill is `write no nested directory` (plan:60); the command file pins `writes no nested directory` (plan:74). Neither covers "no nested contract" or the `artifacts` listing. Task 1's `artifacts` clause ("a nested contract is listed in `artifacts` only for a nested command that ran") appears in plan:30 but is in no AC substring. So V2's C-004 is real for the contract half, not only for the "exists only when /sc:analyze ran" sentence (which is logically implied by the pinned negative plus the existing `nested/analyze-` pin).

## Fix for C-007

Given (a), no field in the contract identifies the tool, so the live-check wording must not tie "no folder" to `primary`, `fallback_1` or `source`. Replace the second sentence of Task 6 (plan:81) with wording of this shape:

"A live-check extra for brainstorm therefore reads: for the codebase-enrichment wave, `nested/analyze-<n>/` is required only when the worker's session file shows that `/sc:analyze` was invoked for the scan (spec 7.2 step 5); when it was, the folder exists, holds its own `return-contract.yaml` and is listed in `artifacts`. When the scan ran through `mcp__auggie__codebase-retrieval` or through codegraph, Glob and Grep, no nested analyze folder is expected and none is listed in `artifacts`. `enrichment_used` records `source: codebase` with the tier (`primary` or `fallback_1`) but does not say which tool ran, so it is not the test; a live plan must not expect the folder from `quality_tier` alone (P1 check lc10 is the origin of this rule)."

Consequences for the plan, none of which adds scope beyond Task 6 and its AC:
1. Keep the phrases Task 6's AC already pins (`only for a nested command that actually ran`, `lc10`) and add one more exact phrase to that AC, `session file`, so the tool-based rule is pinned.
2. Also fix the first sentence's parenthetical so it does not claim a `fallback_1` scan never has a folder; say "the `fallback_1` tier itself writes none".
3. Do not add a tool field to `enrichment_used`; that changes the stable contract (`SKILL.md:360-377`) and is the owner's decision, not this plan's.
4. Optionally move this sentence to the P1 section or 7.2 step 4 with a pointer from 2.1 (see C-006).

## Final diff-point positions

| Point | Final superior position | Changed since Round 1? | One-line evidence |
|---|---|---|---|
| S-001 | none | yes (was split) | Each card has 2 P1; counts reflect bundling (V1's R1-10 merges two findings) and the over-rated R1-1 and R3-2 offset V1's breadth. |
| S-002 | none | yes (was V1) | R1-5 INFERRED hid a groundable premise (`SKILL.md:187,198`); R3-1 Grounded has a wrong remedy (`SKILL.md:372`); R3-9 INFERRED is right; R2-1 Grounded overreaches on clause 2. |
| C-001 | split (V2 diagnosis, V1 remedy) | no | 953 tracked paths under `done/` today (`git ls-files`), so the first clause fails; before/after `git status` diff works in either tree state. |
| C-002 | V3 | no | `SKILL.md:199` inside Wave 2A makes Task 4's assertion vacuous; `SKILL.md:195` lacks `fallback_1`, so Task 1's clause is untested, not vacuous (plan:33). |
| C-003 | split (V1/V2) | no | P2: `test_codegraph_adoption.py:75-82` keeps all three asserted strings when a bullet is added inside lines 25-31; V3's P1 overrates. |
| C-004 | V2 | yes (was split) | `src:6` requires "lists no nested contract in artifacts"; no planned pin covers the contract/`artifacts` half (plan:60,74); V1 supplied the remedy. |
| C-005 | split (V1/V3) | no | `grep -c` (plan:42) and "at least twice" (plan:60) are file-wide; scope with `_section` (`test_codegraph_adoption.py:56-59`), one bullet per codebase tier. |
| C-006 | split (V1 defensible, V3 better placement) | yes (was V1) | 7.2/7.3 define no per-command extras (`spec:281-327`), so `src:9`'s fallback is a P1 note; 2.1 is still mapped to AC-2.1 (`spec:325,376`), so it is defensible but unevaluated in the plan. |
| C-007 | V3 on severity; no variant's remedy works | no | `SKILL.md:187,198` make analyze `primary`; `source` is only `codebase|research-light|research-deep` (`SKILL.md:372`), so see "Fix for C-007". |
| C-008 | split (V2 number, V1/V3 method) | no | 17 is real (`diagnostics.txt:11`) but baselines move (A-004); record the before-count inside Task 5. |
| C-009 | split (V1/V2) | no | Tier 2 list ends with the Activation bullet (`handoff-routing.md:31`), Tier 1 with `quality_tier` (`:22`). |
| C-010 | split (V1/V2) | no | Test at `test_brainstorm_protocol.py:39` not 37, phrases at `test_worker_contract.py:288`; V1 confirmed F-4 (`variant-1-original.md:60`) and 711 is synthetic. |
| C-011 | V3 | no | Line 142 is in `### 3.1` (`spec:136-142`); the section 6 table is at `spec:215`. |
| C-012 | V3 (Low) | yes (was none) | `write no nested directory` is not a substring of `writes no nested directory` (plan:30 vs 39,47); `no nested directory` is a substring of both and keeps the negation, so my "weakens the pin" claim was wrong. |
| C-013 | split (V1/V2) | yes (was V1) | V1 and V2 name the two missing tests; V2's "the one run test reads none of the edited files" is the sharper framing; V3's R3-8 misreads plan:21 (`test_codegraph_adoption.py:131,143`). |
| X-001 | V2/V3 (V1 wrong) | yes (was V3) | Task 1's clause is not vacuous (`SKILL.md:195` lacks `fallback_1`) but is pinned by no test; only Task 4's assertion is vacuous (`SKILL.md:199`). |
| X-002 | V1/V2 (P2) | no | An added bullet cannot break `test_codegraph_adoption.py:75-82` or `test_tier2_tavily_consistency.py:40-53`. |
| X-003 | V3 on severity (P1); remedy none | no | Real and serious, reproduces lc10 in reverse; both `source` (`SKILL.md:372`) and "auggie scan" fixes fail as a checker rule (New evidence (a)). |
| X-004 | split (V1 defensible, V3 placement) | yes (was V1) | Same evidence as C-006: `src:9` second branch applies; `spec:376` keeps 2.1 defensible. |
| X-005 | V2 (first clause), "doubly" overreaches | no | `git ls-files` shows 953 tracked paths; codes `A`/`R` are not ` M`, so the `done/` clause is reading-dependent. |
| A-001 | ACCEPT | no | Read both tests in full; planned text keeps every asserted string and adds no forbidden token (`test_codegraph_adoption.py:75-82,131,143`; `test_brainstorm_protocol.py:15-21,50-54`). |
| A-002 | QUALIFY | no | LLM reviewer (`qa.md:49,336`), so literal reading is likely, not certain; an infeasible AC reaches `E-HALT-QA` (`qa.md:247,281`; `retry.md:72,107`). |
| A-003 | ACCEPT | no | `assert phrase in text` is the repo style (`test_worker_contract.py:508-509`); scope (C-005), coverage (C-004) and verb form (C-012) are tuning of the method, not a rejection. |
| A-004 | QUALIFY | no | Verified today: 950 `A` / 3 `R`; baselines move once the staged archive is committed, so capture before/after at run time. |

### Variant 2 Advocate (haiku slot)

# Round 2 — Advocate for Variant 2 (reviewer-2, qa persona, haiku slot): rebuttal

Paths are relative to the repo root. "plan:N" is line N of `.dev/tasks/to-do/TASK-WF-brainstormFixBri-20261106-001016/TASK-WF-brainstormFixBri-20261106-001016.md`; "src:N" is `source.md` in the same folder; "spec:N" is `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`. Every file:line cited below was Read this round unless marked "(round 1)".

## Response to criticisms

Every criticism aimed at V2 in Round 1 (A1, A3) and V1's Round 2, each answered.

| # | Criticism | From | Answer |
|---|---|---|---|
| 1 | V2 is silent on C-007/X-003, the defect that would recreate the lc10 false FAIL in reverse | A1 R1, A1 R2, A3 R1 | CONCEDE, unchanged. My Round 1 weakness list named this as V2's largest miss and it stays the largest. The zero-INFERRED discipline explains but does not excuse it: the premise needed only two Reads (`SKILL.md:187,198`), both of which I made for other findings (R2-3 cites SKILL.md:199, four lines below). |
| 2 | R2-1 gives no remedy | A1 R2 | CONCEDE. R2-1 names the defect and the operative clause but prescribes nothing; V1's before/after `git status --porcelain` diff (round1-advocate-1, R1-2) is the correct remedy and works in both tree states. My Round 1 weakness list admitted R2-4 and R2-6 as remedy-less; R2-1 belongs on that list too. |
| 3 | "Doubly unpassable" overreaches on the `done/` clause (staged `A`/`R` are not modifications) | A1 R1, A1 R2, A3 R1 | CONCEDE the word, hold the substance. Re-verified today: `git status --porcelain` gives 950 `A`, 3 `R`, 4 `??`; `git ls-files .dev/tasks/done/TASK-WF-p1LivePlanBrief-20261105-164506` prints 953 tracked paths. The first clause ("lists, among tracked paths, only the six files ... plus this package", plan:98) fails under any reading — 953 other tracked paths are listed, and the package itself is untracked (`git ls-files` on it prints 0), so "plus this package" misdescribes it too. The `done/` clause is reading-dependent (`A`/`R` codes, not ` M`). "Doubly" claimed certainty the second clause does not have; the finding's core stands on the first clause alone. |
| 4 | R2-2's P1 is arguable: `write no nested directory` already pins the half the owner asked for, and the converse is a restatement | A1 R1 | REBUT, now with V1's own Round 2 on my side. `src:6` asks the skill to say the fallback tier "also writes no nested folder **and lists no nested contract in artifacts**" — two clauses. The plan pins `write no nested directory` (plan:60) and `writes no nested directory` (plan:74) and nothing for the contract/`artifacts` half; Task 1's AC (plan:33) pins `fallback_1`, `write no nested directory`, `nested/analyze-` only. V1's Round 2 New evidence (d) reaches the same conclusion and moved C-004 from split to V2. P1 stands, argued as post-implementation drift risk (the implement-time AC does read the "states that ..." clause semantically; no test pins it). |
| 5 | R2-4 diagnoses without prescribing | A1 R1, A3 R1, A1 R2 | CONCEDE, unchanged from Round 1. |
| 6 | The hard-coded 17 is valid only if the tree stays as it is (A-004) | A1 R1 | CONCEDE the dependency, defend the finding's shape. R2-7 cited 17 as the recorded baseline with the post-edit expectation of 18 (`diagnostics.txt:11`), not as a permanent constant, and my A-004 QUALIFY said baselines move. V1's capture-the-before-count-inside-Task-5 method is the robust complement; split is the right final position on C-008. |
| 7 | R2-8 verified the spec-142 line anchor but never checked the plan's label for it, so V2 missed C-011 | A1 R1, A3 R1 | CONCEDE, unchanged. Having Read the line, checking the plan's name for it was one step further; V3 took it. |
| 8 | R2-6 confirms the grep -c detection gap but offers no fix | A1 R1 (implied by "R2-6 contains the detection-gap half ... but no remedy") | CONCEDE. The fix exists in V1's R1-3 (`_section` helper, `test_codegraph_adoption.py:56-59`); V2's contribution is the framing that a file-wide count cannot detect a bullet placed in the wrong list. |
| 9 | U-001 (R2-2) is a matter of severity, not insight, because its remedy has the same add-a-phrase shape as R1-4 and R3-6 | A3 R1 | PARTIAL REBUT. The remedy shape converges because A-003 (exact-substring pins) is the accepted method — the critique would deflate C-004 for every card and proves too much. What was unique in R2-2 is the audit: naming which task pins what (plan:33 "states" with no substring, plan:60, plan:74) across all three primitives, which is what established the hole exists at all. A3's own Round 1 concession grants "U-001 is V2's". |
| 10 | S-002: V2's R2-1 tags "doubly unpassable" Grounded though its second clause is reading-dependent, so no card's tagging discipline wins | A1 R2 | CONCEDE the conclusion, REBUT the framing. The Grounded tag is correct for the finding's core (the first clause, verified twice on disk); the defect is one adverb inside the claim, not the tag's basis. But V1's aggregate point stands: R1-5's INFERRED hid a groundable premise, R3-1's Grounded card carries a sub-claim its own evidence disproves, and my "doubly" overstated inside a Grounded tag. S-002 moves to none. |
| 11 | V2's Round 1 steelman endorsed V3's `source`-field remedy as "exactly right" | self (adversarial duty) | CONCEDE and RETRACT. `SKILL.md:371-373` defines `source: codebase | research-light | research-deep` — the enrichment kind, not the tool. Both `/sc:analyze` and `mcp__auggie__codebase-retrieval` record `source: codebase`; no field in `enrichment_used` names the tool, and the Wave 2A rows (`SKILL.md:183-191`) never record it. My Round 1 sentence "the remedy ... is exactly right" and my concession "if the merge takes one thing from V3, it is the `source`-field rule" were wrong and, if merged, would have installed a second unworkable checker rule — the exact failure class this plan exists to remove. This is the most serious error in my Round 1 statement; V1's Round 2 New evidence (a) is correct and I verified it independently. |

## Updated assessment

### (a) V1's claim about `source` and its Task 6 replacement sentence

**The `source` claim is correct.** `SKILL.md:371-373` (Read this round): `enrichment_used:` holds `- source: codebase | research-light | research-deep` and `quality_tier: primary | fallback_1 | skipped`. That is the stable contract (`SKILL.md:360-377`). `source` names the enrichment kind; it cannot distinguish `/sc:analyze` from auggie from codegraph, and no other contract field records the tool. V3's original card asserted the rule must decide "by the `source` field of `enrichment_used` (analyze vs auggie vs codegraph/Grep)" — `analyze` is not a legal value of that field, so the card's remedy was wrong inside a Grounded tag. My Round 1 endorsement of it (criticism 11) is retracted.

**The replacement sentence is correct in mechanism, testable, and consistent with the owner decision — with two caveats.**

- Correct in mechanism: spec 7.2 step 5 (`spec:291-302`) defines the worker's session file as the primary source for behavioural checks and states tool calls are recorded there "as `tool_use` blocks with a `name`" (`spec:302`). So "the session file shows `/sc:analyze` was invoked" is a checkable rule, which neither `quality_tier` nor `source` can express.
- Testable: keep the two phrases Task 6's AC already pins (`only for a nested command that actually ran`, `lc10`, plan:84) and add `session file` as one more exact substring. That is the same check style as every other pin in the plan (A-003).
- Consistent with the owner decision: `src:3` and the archived decision (`p1-owner-decisions-20261105.md`, lc10 row) both state the rule tool-wise — "the nested analyze folder applies only when `/sc:analyze` was used". V1's sentence implements exactly that. It deliberately does not copy the sketch sentence in `src:9` ("a `fallback_1` or auggie primary scan is recorded as the tier used with no nested folder") — correctly so, because that sketch is itself falsified by the analyze-failed edge case (see (b)); the plan's author copied it into plan:81 and imported the bug. The one gap: V1 does not say out loud that it is declining the brief's literal sketch, and a plan fix should, so a reviewer does not read the divergence as drift.
- Caveat 1 (clause overlap): in the analyze-invoked-and-failed case, BOTH clauses of V1's sentence apply — clause 1 ("/sc:analyze was invoked ... the folder exists") and clause 2 ("when the scan ran through ... codegraph, Glob and Grep, no nested analyze folder is expected"). A failed `/sc:analyze` is followed by the codegraph fallback, so the run satisfies both descriptions and the sentence contradicts itself there. Patch: scope clause 2 to "when `/sc:analyze` was not invoked". V1's consequence 2 fixes the first sentence's `fallback_1` parenthetical but not this second-sentence overlap.
- Caveat 2: V1's item 3 (do not add a tool field to `enrichment_used`) is right — that changes the stable contract (`SKILL.md:360-377`) and is the owner's call, not this plan's.

### (b) V1's new point: a `fallback_1` run can leave a nested analyze folder

**Grounded — and stronger than V1 stated.** The chain, all Read this round: `SKILL.md:187` offers `/sc:analyze` OR `mcp__auggie__codebase-retrieval` as the codebase row's action (no fixed order); `SKILL.md:195` invokes `/sc:analyze` with `--report-dir <report-dir>/nested/analyze-<n>/`; `SKILL.md:199` defines `fallback_1` as "primary failed, used codegraph and native Glob/Grep"; `handoff-routing.md:31` activates Tier 2 when Tier 1 "returns error OR empty result". So a worker that tries `/sc:analyze` first, fails, and falls back records `fallback_1` — after an invocation that already carried the nested report dir. My addition: the leftover directory is not a fluke but the rule, because WC-4 (`spec:72`) requires the contract to be written "on success, failure, blocked and partial outcomes, including stops before any other output exists", and analyze is a P1 command (`spec:159`, `spec:231`) — a failed nested `/sc:analyze` writes `nested/analyze-1/return-contract.yaml`. The current skill text already lists it ("The nested contract is listed in `artifacts`", `SKILL.md:195`).

**Does the planned wording become wrong?** Split by task:

- Task 6 (plan:81): YES. "a `primary` or `fallback_1` scan is recorded as the tier used, with no nested folder" describes the run by its resulting tier. In this case the scan is recorded `fallback_1` and a nested folder exists. The sentence is wrong in both directions: it denies the folder to a clean analyze run (`primary`, C-007) and denies it to a fallback run that tried analyze first. The owner's own sketch in `src:9` carries the same defect, which is the strongest argument for V1's session-file rewrite over verbatim copying.
- Tasks 1-3 (plan:30, 39, 47): literally still TRUE but incomplete. Their subject is the tier or tool ("the `fallback_1` tier ... writes no nested directory and no nested contract"), and the fallback scan itself writes none. What is missing is one clause acknowledging that a failed `/sc:analyze` attempt leaves its nested contract behind — without it, a reader takes the tier-scoped sentence as run-level guidance and recreates lc10 at the next live check. Cheapest patch, inside Task 1's existing sentence budget: a nested contract stays listed in `artifacts` for a nested command that was invoked, including a failed attempt. Note also that plan:30's qualifier "only for a nested command that ran" is ambiguous for a failed run — an implementer reading "ran" as "succeeded" would unlist the failed attempt's contract, contradicting WC-4.

### The other variants, updated

**Variant 1.** Steelman first: V1's Round 2 is the strongest statement in the debate so far. It conceded its two real errors (R1-1's Task 1 overclaim, the R1-5 under-rating) without hedging, produced the two pieces of new evidence that change positions (`source` cannot discriminate; `src:6`'s unpinned contract half), and its C-007 fix is the only proposed remedy grounded in a mechanism a checker can actually operate (the session file, `spec:291-302`). Its before/after remedies for C-001 and C-008 are the ones that survive a changing tree. Critique: its replacement sentence carries the clause-overlap defect (above) and does not flag its deliberate divergence from `src:9`'s sketch; and its Round 2 still does not name the cheapest guard for the analyze-failed leftover (one clause in Task 1), leaving Tasks 1-3's wording "true but misleading".

**Variant 3.** Steelman first: R3-1 remains the single most consequential diagnosis — nobody else found a defect in the plan's new text rather than in its checks, and the finding survives every rebuttal. R3-4 (section label) and R3-5 (placement split) both stood up, and V3's Round 1 self-correction on X-002 (conceding P2) was honest. Critique: R3-1's remedy is refuted by the contract it cites — `SKILL.md:371-373` — so the card's Grounded tag covers a finding whose prescribed test cannot be executed; V3's Round 1 weakness 5 half-saw this ("`source` values are not enumerated anywhere I read") and still did not check the four lines that enumerate them. R3-2's P1 was over-rated (all three cards now agree P2). R3-8 misreads plan:21. V3 has still said nothing about C-001, the criterion that halts execution first.

**My own card.** V2's diagnoses held up: every R2 finding re-verified this round (R2-1's baseline re-run identical; R2-3's SKILL.md:199 in Wave 2A; R2-5's inversion confirmed — `test_routing_plugin_parity.py:16` reads only the sc-recommend skill; R2-7's 17 confirmed at `diagnostics.txt:11`; R2-8's anchors re-Read). Its costs also stand: silent on the High item, two-and-a-half findings without remedies, and a Round 1 endorsement of V3's broken remedy that this round retracts.

## New evidence

1. `src:6` (Read this round): the brief asks the skill to say the fallback tier "also writes no nested folder **and lists no nested contract in artifacts**". The plan pins no substring for the contract/`artifacts` half anywhere (plan:33 pins `fallback_1`, `write no nested directory`, `nested/analyze-`; plan:60 and plan:74 pin only the directory phrases). Confirms C-004 at P1 independently of V1's Round 2 (d).
2. The analyze-failed leftover is expected, not anomalous: WC-4 (`spec:72`, "written on success, failure, blocked and partial outcomes, including stops before any other output exists") plus analyze's P1 status (`spec:159`, `spec:231`) means a failed nested `/sc:analyze` writes `nested/analyze-1/return-contract.yaml`. Grounds V1's Round 2 refinement and extends it: after a failed analyze attempt, a `fallback_1` run legitimately holds a nested analyze contract listed in `artifacts` (`SKILL.md:195` current text). Consequence: `src:9`'s sketch sentence ("a `fallback_1` ... scan is recorded as the tier used with no nested folder") is falsified by this case, so the plan was right to need different wording and wrong to copy the sketch into plan:81.
3. V1's replacement sentence contradicts itself in that same case: clause 1 fires ("/sc:analyze was invoked ... the folder exists") and clause 2 fires ("when the scan ran through ... codegraph, Glob and Grep, no nested analyze folder is expected"). Scope clause 2 to "when `/sc:analyze` was not invoked".
4. `test_routing_plugin_parity.py:16` (Read this round): the file reads only `src/superclaude/skills/sc-recommend` — none of the six edited files. Confirms R2-5's inversion: the one extra test Task 7 runs guards nothing this plan edits, while two tests that read the edited files (`test_codegraph_adoption.py:20-23`, `test_tier2_tavily_consistency.py:19,49`) are not run.
5. Baseline re-run today (Bash, read-only): `git status --porcelain` = 950 `A`, 3 `R`, 4 `??`; `git ls-files` on the archived P1 package = 953 tracked paths; on this plan's package = 0 (untracked). Plan:98's first clause fails today under any reading, and its "plus this package" phrase misdescribes an untracked package.
6. `test_worker_contract.py:704-732` (Read this round): the line-711 lambda mutates `_SYNTHETIC_SECTION`, a synthetic fixture, not the brainstorm file — confirming R2-8's note that it needs no change and that Task 5's automatic `_removals` pickup (`:519-527`, parametrized at `:559-562`) is the real coupling.

## Final diff-point positions

| Point | Final superior position | Changed since Round 1? | One-line evidence |
|---|---|---|---|
| S-001 | none | no | Each card carries 2 P1; count differences are bundling (V1's R1-10 merges two findings) and offsetting over-ratings. |
| S-002 | none | yes (was V2) | R1-5 INFERRED hid a groundable premise (`SKILL.md:187,198`); R3-1 Grounded asserts `source: analyze`, a value `SKILL.md:372` forbids; my "doubly" overstated inside a Grounded tag. |
| C-001 | split (V2 diagnosis, V1 remedy) | yes (was V2) | 953 tracked paths under `done/` (re-run today) fail plan:98's first clause; V1's before/after status diff works once the archive is committed. |
| C-002 | V3 | yes (was split V2/V3) | Task 4's section-wide assertion vacuous (`SKILL.md:199` in Wave 2A); Task 1's clause not vacuous (`SKILL.md:195`) but pinned nowhere — V3's "stays untested" covers both halves. |
| C-003 | split (V1/V2) | no | P2: an added bullet keeps every asserted string (`test_codegraph_adoption.py:75-82`); all three cards now agree P2. |
| C-004 | V2 | no | plan:33 "states" pins nothing; `src:6` demands "lists no nested contract in artifacts" and no planned pin covers that half (plan:33,60,74). |
| C-005 | split (V1/V3) | no | File-wide `grep -c` and "at least twice" (plan:42,60); scope with `_section` (`test_codegraph_adoption.py:56-59`), one bullet per codebase tier. |
| C-006 | split (V1 defensible, V3 placement) | no | 7.2/7.3 define no per-command extras (`spec:281-327`), so `src:9`'s P1-note branch applies; `spec:376` still maps 2.1 to AC-2.1. |
| C-007 | V3 on diagnosis; no remedy as proposed (V1 R2 fix closest, needs the clause-2 carve-out) | yes (my remedy endorsement retracted) | Analyze is `primary` (`SKILL.md:187,198`); `source` is only `codebase\|research-light\|research-deep` (`SKILL.md:372`), so V3's remedy fails and my Round 1 backing of it was wrong. |
| C-008 | split (V2 number, V1/V3 method) | no | 17 today (`diagnostics.txt:11`), 18 after the edit; record the before-count inside Task 5 (A-004). |
| C-009 | split (V1/V2) | no | Tier 2 list ends with the Activation bullet (`handoff-routing.md:31`), not `quality_tier` (`:30`). |
| C-010 | split (V1/V2) | yes (was V2) | Test at `test_brainstorm_protocol.py:39`, phrases at `test_worker_contract.py:288`; V1 confirmed F-4 and that line 711 is synthetic (`:704-732`); V2 cleared every anchor. |
| C-011 | V3 | no | Line 142 is under `### 3.1` (`spec:136-142`); `## 6` starts at `spec:215`. |
| C-012 | V3 | no | `write` is not a substring of `writes` (plan:30 vs 39,47); `no nested directory` is a substring of both. |
| C-013 | split (V1/V2) | yes (was V2) | Both name both missing test files at P2; the run test reads only sc-recommend (`test_routing_plugin_parity.py:16`); V3's R3-8 misreads plan:21 (plugin file read only for `mcp-servers:`, `test_codegraph_adoption.py:131`). |
| X-001 | split (V2/V3) | yes (was V2) | Only Task 4's assertion is vacuous (`SKILL.md:199`); Task 1's clause fails on old text (`SKILL.md:195`) but nothing pins it — V3's phrasing completes V2's boundary. |
| X-002 | V1/V2 (P2) | no | Planned text breaks no assertion in either test (`test_codegraph_adoption.py:75-82`; `test_tier2_tavily_consistency.py:40-53`). |
| X-003 | V3 on severity (P1); remedy none (V1 R2 closest) | yes (remedy retracted) | Reproduces lc10 in reverse (`SKILL.md:187,198` vs plan:81); deciding by `source` is impossible (`SKILL.md:372`); the session file is the only workable record (`spec:291-302`). |
| X-004 | split (V1 defensible, V3 placement) | yes (was V3) | `src:9`'s first branch is false (`spec:281-327`); 2.1 remains mapped to AC-2.1 (`spec:376`); V3's split is the better home for the live-check sentence. |
| X-005 | V2 (first clause); "doubly" overreaches | no | 950 `A` + 3 `R` re-verified today; the first clause fails under any reading, the `done/` clause is reading-dependent. |
| A-001 | ACCEPT | no | Both tests Read; the planned sentences add no forbidden token and touch no asserted string; the parity test is irrelevant by construction. |
| A-002 | QUALIFY | no | Contradictory output gives `ac-outcome-missing` (`qa.md:49`), verdict `missing` (`qa.md:114`), then `E-HALT-QA` (`qa.md:247`; `retry.md:72,107`) — but the reviewer is an LLM, so a charitable pass is possible. |
| A-003 | ACCEPT | no | `assert phrase in text` is the house style (`test_worker_contract.py:508-509`); scope (C-005), coverage (C-004) and verb form (C-012) tune the method. |
| A-004 | QUALIFY | no | 950 `A` / 3 `R` / 4 `??` re-run today; baselines move once the staged archive commits, so Tasks 5 and 7 must capture their own before-state. |

### Variant 3 Advocate (opus)

# Round 2 - Advocate for Variant 3 (reviewer-3, refactorer, opus): rebuttal (last in sequence)

Paths are relative to the repo root. "plan:N" is line N of `.dev/tasks/to-do/TASK-WF-brainstormFixBri-20261106-001016/TASK-WF-brainstormFixBri-20261106-001016.md`; "src:N" is `source.md` in the same folder; "spec:N" is `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`; "SKILL.md" is `src/superclaude/skills/sc-brainstorm-protocol/SKILL.md`; "routing" is its `refs/handoff-routing.md`; "cmd" is `src/superclaude/commands/brainstorm.md`; "lc10" is `.dev/tasks/done/TASK-WF-p1LivePlanBrief-20261105-164506/artifacts/lc10-result.md`. Every file:line below was Read (or run, read-only) this round.

## Response to criticisms

Every criticism of V3 made by Advocate 1 (A1) and Advocate 2 (A2) in Rounds 1 and 2.

| # | Criticism | From | Answer |
|---|---|---|---|
| 1 | R3-1's remedy ("decide by the `source` field of `enrichment_used`") cannot work: `source` is only `codebase \| research-light \| research-deep` | A1 R1, A1 R2, A2 R2 | **CONCEDE, plainly: they are right.** SKILL.md:371-373 reads `enrichment_used: - source: codebase \| research-light \| research-deep` / `quality_tier: primary \| fallback_1 \| skipped`. `analyze` is not a legal value. `/sc:analyze` and auggie both record `source: codebase`, and a clean run of either records `primary` (SKILL.md:187,198). No field of the stable contract (SKILL.md:360-377) names the tool. The remedy in my card would have installed a second checker rule with nothing to read, which is the failure class this plan exists to remove. The diagnosis (decide by which tool ran, not by tier) stands; the mechanism I named is wrong. |
| 2 | R3-1 was tagged Grounded although its remedy is refuted by the file it cites | A1 R1, A1 R2, A2 R2 | CONCEDE for the remedy. The premise (SKILL.md:187,198 against plan:81) is Grounded; the prescribed test was asserted without reading four lines that were 170 lines below the ones I cited. S-002 moves to none. |
| 3 | V3's Round 1 weakness 5 said "`source` values are not enumerated anywhere I read" and still did not check them | A2 R2 | CONCEDE. That sentence was false; they are at SKILL.md:372. I flagged the doubt and did not resolve it with one Read. |
| 4 | R3-2 (Task 7 skips `test_codegraph_adoption.py`) is over-rated at P1 | A1 R1, A2 R1, A1 R2, A2 R2 | CONCEDE (already in my Round 1). Re-read: the Tier 2 slice test (`tests/skills/test_codegraph_adoption.py:75-82`) asserts only `codegraph_files`, `codegraph_search` and `Glob for files matching topic keywords`; the other brainstorm checks read the `mcp-servers:` line (`:131`) and the absence of `mcp__serena` (`:143`). A bullet added inside routing lines 25-31 keeps all of them. P2: a coverage gap against src:7, not a missed break. |
| 5 | R3-8 misreads plan:21: the plan says no test requires the src and plugin copies to *match*, not that no test reads the plugin copy | A1 R1, A1 R2, A2 R2 | CONCEDE. plan:21: "no test requires the two to match (`tests/commands/test_routing_plugin_parity.py` covers only the `sc-recommend` skill)". `test_codegraph_adoption.py:23,39,121` reads the plugin `brainstorm.md` only for its own `mcp-servers:` line and the serena scan, each file on its own; nothing compares the two. R3-8 attacked a claim the plan did not make. I withdraw it. |
| 6 | R3-6's shared phrase "no nested directory" would weaken the pin | A1 R1 | REBUT; A1 retracted this in Round 2 (C-012 row). `no nested directory` is a substring of both `write no nested directory` and `writes no nested directory` and keeps the negation. Still Low. |
| 7 | V3 missed C-001 (Task 7 bullet 3 cannot pass) | A1 R1, A2 R1, A1 R2, A2 R2 | CONCEDE. Re-run today: `git status --porcelain` gives 950 `A `, 3 `R `, 4 `??`; `git ls-files` on this plan's package prints 0. The first clause of plan:98 fails on any reading; "plus this package" describes an untracked package. It is the first criterion that halts execution, and V3 said nothing. |
| 8 | V3 missed C-009 and C-010 | A2 R1, A1 R2 | CONCEDE. routing:30 is `quality_tier`, routing:31 is the Activation bullet, so the Tier 2 list does not end with its `quality_tier` line (plan:39). |
| 9 | R3-5 "wrong spot" overstates; 2.1 is defensible | A1 R1 | PARTIAL. spec:376 maps the 2.1 rule to AC-2.1, so the general sentence belongs in 2.1. The brainstorm live-check sentence is per-command material; spec 7.2 (spec:281-304) and 7.3 (spec:306-327) define no per-command extras, so src:9's second branch ("a note in the P1 section") applies. Both A1 and A2 moved to split; I move to split too. |
| 10 | R3-9 is INFERRED drift speculation about a clause the plan carries elsewhere | A2 R1 | PARTIAL REBUT, with new support from A2 R2. The drift risk is real but runs the other way from my card: plan:30's new clause "a nested contract is listed in `artifacts` only for a nested command that ran" is ambiguous for a failed `/sc:analyze` call (A2 R2), while cmd:157's unconditional "the nested contracts are listed in `artifacts`" is the correct reading under WC-4. The two files can disagree on exactly that clause. Kept as Low, reframed (see Proposed wording). |
| 11 | X-001: V3's "stays untested" was vague | A2 R1 | REBUT; A1 R2 and A2 R2 now both use V3's phrasing. plan:33 scopes Task 1 to the SKILL.md:195 paragraph, which lacks `fallback_1`; SKILL.md:199 is in Wave 2A, so only Task 4's section-wide assertion is vacuous. |
| 12 | My Round 1 claim that V1's "auggie primary" one-word fix was "the smaller fix ... either is acceptable" | self (adversarial duty) | WITHDRAW. Restoring "auggie" fixes the `primary` half only. The `fallback_1` half of plan:81 ("a `primary` or `fallback_1` scan ... with no nested folder") is false at run level when `/sc:analyze` was tried first and failed (New evidence 1). Neither one-word fix is acceptable. |

## Updated assessment

**Variant 1.** Steelman: V1's Round 2 is the most useful statement before this one. It found the `source` refutation, the analyze-failed refinement, and the only remedy that names a record which can tell analyze from auggie (the session file, spec:291-302). Its before/after remedies for C-001 and C-008 survive a changing tree. Critique: (a) its replacement sentence contradicts itself in the analyze-failed case, as A2 showed: both "`/sc:analyze` was invoked, the folder exists" and "the scan ran through codegraph, Glob and Grep, no nested analyze folder is expected" fire on the same run. (b) It is not checkable from the worker's output folder; it needs the session file for every run, including the common auggie and fallback runs where the folder answer is already visible. (c) It reads the session file as one file. Wave 2A runs its enrichment "in parallel via `Task` agents" (SKILL.md:183), and spec 7.2 step 5 puts each subagent's calls in its own file under `subagents/` (spec:292). lc10's analysis lists "two top-level Skill calls" (lc10:13); a top-level-only search would miss an `/sc:analyze` call made inside a Task agent and pass a run whose nested folder is missing.

**Variant 2.** Steelman: V2's Round 2 grounded the analyze-failed case in WC-4 (spec:72, contract "written on success, failure, blocked and partial outcomes") and gave the cheapest Tasks 1-3 patch: say "invoked", including a failed attempt. It also retracted its endorsement of my broken remedy without hedging. I confirm its WC-4 chain from the analyze side: cmd `analyze.md:98` says "`<report-dir>/return-contract.yaml` is written on every outcome ... failed otherwise". Critique: its clause-2 carve-out ("when `/sc:analyze` was not invoked") still leaves the check dependent on the session file for every run; and "the folder exists when invoked" has one narrow exception it did not state: `analyze.md:97` refuses a report directory "that cannot be created or written" and prints in chat only, so an invoked analyze can leave no folder. That edge is rare (brainstorm builds the path, and `<n>` is never reused, cmd:157) but a pass/fail sentence must not claim more than WC-4 gives.

**Variant 3 (own card).** The diagnosis in R3-1 survives every round: plan:81 decides the folder by tier, and tier does not determine the folder. Everything I prescribed for it was wrong (the `source` field) or insufficient (the "auggie" qualifier). V3's other durable contributions are C-002/X-001 phrasing, C-011 and C-012. Its misses (C-001, C-009, C-010) and its two misfires (R3-2's P1, R3-8) stand.

**My Round 1 P1 claims:**

| Claim | Decision | Why |
|---|---|---|
| R3-1 diagnosis: plan:81 fails a correct `/sc:analyze` run because analyze is also `primary` | KEEP at P1, and widen | SKILL.md:187,198 against plan:81. Widened: the same sentence also fails a correct analyze-failed-then-`fallback_1` run (New evidence 1), so both tiers in it are wrong, not only `primary`. |
| R3-1 remedy: decide by `source` | WITHDRAW | SKILL.md:372 (criticism 1). |
| Round 1 strength 2: the dropped "auggie" qualifier is Drift | DOWNGRADE | Dropping the word is still unauthorized loss of a brief constraint, but restoring it does not make the sentence true. The correct fix must knowingly depart from src:9's own sketch ("a fallback_1 or auggie primary scan is recorded as the tier used with no nested folder"), and the plan should record that departure as a Necessary deviation so a reviewer does not read it as drift. |
| R3-2: missing `test_codegraph_adoption.py` run is P1 | DOWNGRADE to P2 | test_codegraph_adoption.py:75-82,131,143 (criticism 4). |

## New evidence

1. **A `fallback_1` run can legitimately hold a nested analyze folder, and the planned "no folder" wording is false at run level.** SKILL.md:187 offers `/sc:analyze` OR auggie for the codebase row; SKILL.md:195 says the analyze call carries `--report-dir <report-dir>/nested/analyze-<n>/`; SKILL.md:199 defines `fallback_1` as "primary failed, used codegraph and native Glob/Grep"; `analyze.md:98` writes the contract "on every outcome", failed included. So: analyze tried, failed, codegraph/Grep used, `enrichment_used` = `{source: codebase, quality_tier: fallback_1}`, and `nested/analyze-1/return-contract.yaml` exists. The run-level table is:

   | What happened | `quality_tier` | `nested/analyze-<n>/` |
   |---|---|---|
   | `/sc:analyze` ran cleanly | `primary` | present |
   | auggie ran cleanly | `primary` | absent |
   | `/sc:analyze` tried, failed, codegraph/Grep used | `fallback_1` | present (failed contract) |
   | auggie tried, failed, codegraph/Grep used (lc10) | `fallback_1` | absent |
   | not invoked | `skipped` | absent |

   Both `primary` and `fallback_1` map to present and absent. No tier rule can be right. The routing ref does not show this because its Tier 1 is auggie only (routing:16) and Tier 2 activates "if Tier 1 returns error OR empty result" (routing:31); `/sc:analyze` appears only in the skill's matrix.

2. **The folder-based check is complete from the output folder in one direction.** In every row above, a present folder holds its own contract and the skill lists it in `artifacts` (SKILL.md:195 today; WC-4 nested rule spec:62). So "every `nested/analyze-<n>/` that exists holds `return-contract.yaml` and is listed in `artifacts`, and every listed one exists" is true for every correct run and needs nothing outside the report directory. What the folder cannot show is a missing folder after an invocation; only the session files can.

3. **The session-file converse must include subagent files.** SKILL.md:183 ("apply in parallel via `Task` agents") plus spec:292 (subagent files under `~/.claude/projects/<dir>/<session id>/subagents/`). lc10:13 recorded only top-level Skill calls ("both with sidechain False"). A live plan that copies lc10's method would not see an analyze call made inside a Task agent. (INFERRED: the exact `tool_use` shape of the call, a `Skill` call naming `sc:analyze`, has not been observed in a run; `analyze.md` names no protocol skill, so `sc:analyze` is the expected name.)

4. **WC-4 has one gap that the converse must allow.** `analyze.md:97`: a report directory "that cannot be created or written, counts as no report directory known (refusal printed in chat only)". So "invoked implies folder" holds except for that refusal. The proposed sentence says so in a few words.

5. **The C-004 half that is unpinned is the contract half.** src:6 asks the skill to say the fallback tier "also writes no nested folder and lists no nested contract in artifacts". plan:33, plan:60 and plan:74 pin only directory phrases. Pinning `write no nested directory and no nested contract` (skill) and `writes no nested directory and no nested contract` (routing, cmd) as single phrases covers both halves with no new test helper.

6. **Baseline re-run (read-only), A-004.** `git status --porcelain`: 950 `A `, 3 `R `, 4 `??`; `git ls-files .dev/tasks/to-do/TASK-WF-brainstormFixBri-20261106-001016` prints 0. Identical to A1 R2 and A2 R2.

## Proposed wording

### Task 6 live-check sentence (replaces the second sentence of plan:81)

> A live-check extra for brainstorm therefore reads: "for the codebase-enrichment wave, every `nested/analyze-<n>/` directory in the report directory holds its own `return-contract.yaml` that is listed in `artifacts`, and every `nested/analyze-` path listed in `artifacts` exists; no such directory is required, because neither `quality_tier` nor `source` in `enrichment_used` shows whether `/sc:analyze` was invoked (a scan that tried `/sc:analyze`, failed and fell back is recorded `fallback_1` and keeps the folder), so the directory is required only when the worker's session file or one of its subagent files (7.2 step 5) shows a call to `/sc:analyze` and the chat shows no refused report directory" (P1 check lc10 is the origin of this rule).

Why this form: the first clause is checked from the output folder alone (`ls`, then the `artifacts` list in `return-contract.yaml`) and is true for all five rows of New evidence 1. The second clause forbids the tier-based inference that caused lc10 and its reverse. The third clause is the only way to catch a missing folder; it names the subagent files and the `analyze.md:97` refusal so it claims no more than WC-4 gives. It has no clause overlap: nothing in it says "no folder" for any tier.

Companion edits inside Task 6 (no new files): change the first sentence's "exists only for a nested command that actually ran" to "exists only for a nested command that actually ran, including one that ran and failed" (keeps the pinned phrase, plan:84), and say "the auggie scan and the codegraph/Grep scan themselves write no nested directory" instead of tying "no nested directory" to `primary` or `fallback_1`. Add `session file` to Task 6's pinned phrases. Note in the plan that this departs from src:9's sketch on purpose, citing New evidence 1. Placement: per C-006, the general first sentence stays in 2.1; the live-check sentence may go in the P1 section with a pointer from 2.1 (src:9 second branch).

### Wording rule for Tasks 1-3 (true at run level)

> **Rule:** a "no nested directory" statement takes a tool or tier as its writer (the `mcp__auggie__codebase-retrieval` scan, the `fallback_1` tier), never a run or a recorded `quality_tier`; and the folder's condition is written as invocation, not success: "a nested `analyze` directory exists only when `/sc:analyze` was invoked, also when it failed and the scan fell back to `fallback_1`", and every nested contract written is listed in `artifacts`.

Applied:

- **Task 1** (SKILL.md:195, after "(`<n>` starts at 1)"): "; the `mcp__auggie__codebase-retrieval` alternative and the `fallback_1` tier (codegraph, then native Glob and Grep, `refs/handoff-routing.md` Tier 2) are unchanged and write no nested directory and no nested contract. A nested `analyze` directory exists only when `/sc:analyze` was invoked, also when it failed and the scan fell back to `fallback_1`, so `enrichment_used` does not show whether it exists. Each nested contract written is listed in `artifacts`." This replaces plan:30's "only for a nested command that ran", which is ambiguous for a failed call (criticism 10). No `src/superclaude/` path, no Orca command (plan:22).
- **Task 2** (routing): the planned bullet ("this tier writes no nested directory and no nested contract; the scan is recorded in `enrichment_used` with this tier's `quality_tier`") already obeys the rule: its writer is the tier. Keep it; place each bullet after the tier's `quality_tier` line (C-009) and scope the test per tier (C-005).
- **Task 3** (cmd:157): change "the nested `analyze` directory exists only when `/sc:analyze` ran" to "exists only when `/sc:analyze` was invoked, also when it failed and the scan fell back to `fallback_1`". Leave "`adversarial_artifacts_dir` and the nested contracts are listed in `artifacts`" as it is; it is already correct.
- **Pins (Tasks 4-5):** in Task 4, slice the `**Under `--unattended`**` paragraph (not the whole Wave 2A section, which makes `fallback_1` vacuous through SKILL.md:199) and assert `write no nested directory and no nested contract` and `` only when `/sc:analyze` was invoked ``; in Task 5, add `writes no nested directory and no nested contract` and `` only when `/sc:analyze` was invoked `` to `UNATTENDED_EXPECT["brainstorm"]["phrases"]`. This closes C-002, both halves of C-004 and the run-level gap, with the existing helpers.

Self-critique of this proposal: the folder clause alone cannot catch a missing folder after an invocation; the session-file clause is needed for that and inherits step 5's "not verifiable" outcome when the file is missing (spec:300). The `sc:analyze` call name is INFERRED (New evidence 3). The sentence is long; a shorter one that drops the third clause would be checkable from the folder but blind to the missing-folder case.

## Final diff-point positions

| Point | Final superior position | Changed since Round 1? | One-line evidence |
|---|---|---|---|
| S-001 | none | no | Each card has 2 P1; R1-1 and R3-2 were over-rated and R1-10 bundles two findings, so counts do not rank the cards. |
| S-002 | none | yes (was split V1/V3) | R1-5 INFERRED hid a groundable premise (SKILL.md:187,198); R3-1 Grounded carried a remedy SKILL.md:372 refutes; R2-1 "doubly" overreached. |
| C-001 | split (V2 diagnosis, V1 remedy) | yes (was V2) | 950 `A` + 3 `R` tracked today and the package is untracked (`git ls-files` = 0), so plan:98's first clause fails; a before/after status diff works in either tree state. |
| C-002 | V3 | no | Task 4 slices all of Wave 2A, where SKILL.md:199 already has `fallback_1`; Task 1's paragraph (SKILL.md:195) lacks it but nothing pins it. |
| C-003 | split (V1/V2, P2) | yes (was V2) | An added bullet keeps every string `test_codegraph_adoption.py:75-82,131,143` asserts; both missing files should still be run. |
| C-004 | V2 | no | src:6 asks for "lists no nested contract in artifacts"; plan:33,60,74 pin only directory phrases; pin `... no nested directory and no nested contract`. |
| C-005 | split (V1/V3) | no | `grep -c` (plan:42) and "at least twice" (plan:60) are file-wide; slice per tier with `_section` (`test_codegraph_adoption.py:56-59`). |
| C-006 | split (V1 defensible, V3 placement) | yes (was V3) | spec:376 keeps the general rule in 2.1; 7.2/7.3 hold no per-command extras (spec:281-327), so src:9's P1-note branch fits the live-check sentence. |
| C-007 | V3 on diagnosis; remedy is this round's folder-plus-session-file sentence (no card's original remedy works) | yes (V3 remedy withdrawn) | Analyze is `primary` (SKILL.md:187,198); `source` cannot name the tool (SKILL.md:372); a failed analyze leaves a folder under `fallback_1` (SKILL.md:199, analyze.md:98). |
| C-008 | split (V2 number, V1/V3 method) | yes (was V2) | 17 is the recorded baseline (diagnostics.txt:11) but A-004 moves; record the before-count inside Task 5. |
| C-009 | split (V1/V2) | no | routing:30 is `quality_tier`, routing:31 the Activation bullet; V3 missed it. |
| C-010 | split (V1/V2) | yes (was V2) | Test at `test_brainstorm_protocol.py:39`, phrases at `test_worker_contract.py:288`; line 711 is synthetic; V3 silent. |
| C-011 | V3 | no | spec line 142 is under `### 3.1` (spec:136); `## 6` starts at spec:215. |
| C-012 | V3 (Low) | no | `write` is not a substring of `writes` (plan:30 vs 39,47); `no nested directory` is in both; A1 R2 withdrew "weakens the pin". |
| C-013 | split (V1/V2) | yes (was V3) | R3-8 misread plan:21 ("no test requires the two to match"); the plugin file is read only per file (`test_codegraph_adoption.py:121,131,143`). |
| X-001 | split (V2/V3) | yes (was V3) | Only Task 4's assertion is vacuous (SKILL.md:199); Task 1's clause fails on old text (SKILL.md:195) but is unpinned. |
| X-002 | V1/V2 (P2) | no | No assertion in either test touches the new text (`test_codegraph_adoption.py:75-82`; `test_tier2_tavily_consistency.py:40-53` per A1/A2). |
| X-003 | V3 on severity (P1, wider than claimed); remedy: this round's sentence | yes (remedy withdrawn) | plan:81 is wrong for both tiers: analyze-clean is `primary` with folder, analyze-failed is `fallback_1` with folder (New evidence 1). |
| X-004 | split (V1 defensible, V3 placement) | yes (was V3) | Same as C-006. |
| X-005 | V2 (first clause); "doubly" overreaches | no | Staged `A`/`R` are tracked (first clause fails); `A`/`R` are not ` M`, so the `done/` clause depends on reading. |
| A-001 | ACCEPT | no | Re-read `test_codegraph_adoption.py:75-82,115-143`; planned text touches no asserted string; run both tests anyway. |
| A-002 | QUALIFY | no | An LLM reviewer judges each AC (`qa.md:49`, per A1/A2); an infeasible AC reaches `dispute` then `E-HALT-QA` (`retry.md:72,107`), so C-001 still blocks. |
| A-003 | QUALIFY | no | Substring pins are house style (`test_worker_contract.py:508-509`) but prove presence, not run-level truth; they need paragraph/tier scope and phrases written to the run-level rule above. |
| A-004 | QUALIFY | no | Re-run today: 950 `A` / 3 `R` / 4 `??`, package untracked; Tasks 5 and 7 must capture their own before-state. |

## Round 2.5: Invariant Probe

Embedded verbatim from `invariant-probe.md`.

# Invariant Probe Results

## Round 2.5 — Fault-Finder Analysis

Paths are relative to the repo root. "plan:N" = `.dev/tasks/to-do/TASK-WF-brainstormFixBri-20261106-001016/TASK-WF-brainstormFixBri-20261106-001016.md`; "spec:N" = `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`; "SKILL" = `src/superclaude/skills/sc-brainstorm-protocol/SKILL.md`; "routing" = its `refs/handoff-routing.md`; "cmd" = `src/superclaude/commands/brainstorm.md`; "p1plan" / "p1src" = the archived `.dev/tasks/done/TASK-WF-p1LivePlanBrief-20261105-164506/` plan and `source.md`; "r2a1" / "r2a2" / "r2a3" = `rounds/round2-advocate-1/2/3.md`. Every file:line was Read for this probe.

| ID | Category | Assumption | Status | Severity | Evidence |
|---|---|---|---|---|---|
| INV-001 | state_variables | The consensus remedy for Task 7 bullet 3 ("before/after diff of `git status --porcelain`") assumes a stable "before" snapshot. No capture point is named. `/sc:implement` itself runs `git add .dev/tasks` during the run, so this package flips from untracked (`git ls-files` = 0) to staged `A`. A "before" taken at Task 7 start already holds the six edits, so it cannot prove "only the six files". A "before" taken before Task 1 shows the package flip as diff noise that the AC does not exempt. | UNADDRESSED | MEDIUM | `src/superclaude/skills/sc-implement-protocol/refs/managed-workspace.md:36`; r2a1:40 (package untracked today); plan:91-98 (Task 7 is the last task, and nothing earlier records a snapshot) |
| INV-002 | state_variables | The claim that "the next live plan" sees the fix assumes the edits outlive this worktree. The plan forbids commits (plan:24) and does not install (plan:23). 7.2 builds every disposable worktree from a committed git base and installs from the phase branch (spec:282). The spec sentence lives in this worktree's uncommitted `.dev/`. A P2 author working from another branch sees neither the spec sentence nor the new skill text unless someone commits and merges them. The consensus does not mention this. | UNADDRESSED | MEDIUM | plan:23-24; spec:282 |
| INV-003 | state_variables | A-004: the tree state at execution equals today's tree (950 `A`, 3 `R`, collect-only 17). The consensus says to capture each baseline at run time inside Tasks 5 and 7. | ADDRESSED | LOW | r2a1:87; r2a2:90; r2a3:115; `.dev/reflect/pre-TASK-WF-brainstormFixBri-20261106-001016/artifacts/diagnostics.txt:11` |
| INV-004 | guard_conditions | Task 4's section-wide `fallback_1` assertion is vacuous because SKILL:199 (inside Wave 2A) already holds `fallback_1`. The consensus fix slices the `**Under --unattended**` paragraph instead of `_wave2a_section`. | ADDRESSED | MEDIUM | SKILL:195,199; `tests/skills/test_brainstorm_protocol.py:24-29`; r2a3:84 |
| INV-005 | guard_conditions | plan:65 says "the pre-change text fails" the new pins, but nothing checks it mechanically. `test_brainstorm_protocol.py` has no removed-token or mutation test, unlike `test_worker_contract.py`. So a paragraph slicer that silently returns the whole section, which brings the vacuity back, would still pass. The consensus adds pins but no negative test for them. | UNADDRESSED | LOW | `tests/skills/test_brainstorm_protocol.py:1-57`; `tests/skills/test_worker_contract.py:559-568` |
| INV-006 | guard_conditions | plan:50 requires `writes no nested directory` inside the `**Nested invocations.**` bullet. `_check_unattended_section` only checks `phrase in text` over the whole `## Unattended mode` section, so the phrase placed under the Research bullet (cmd:156) passes. The C-005 per-tier scoping was applied to the routing ref only, not to the command file. | UNADDRESSED | LOW | `tests/skills/test_worker_contract.py:499-509`; cmd:156-157; plan:50,74 |
| INV-007 | guard_conditions | The proposed live-check sentence (r2a3 "Proposed wording") requires nothing when there is no folder and no `/sc:analyze` call. It drops the P1 extra's clause "a wave that did not run is recorded as not run with the reason from the contract". With `--codebase` forced in the brief, a run whose codebase wave silently never ran (no `codebase` entry, or `skipped` with no reason) now passes the extra. A guard that used to catch this now lets it through. | UNADDRESSED | MEDIUM | p1plan:275,284; r2a3:69; r2a1:52 |
| INV-008 | count_divergence | The consensus records the collect-only count as 17, then 18 after the edit. The 17 breaks down as 1 section-content case + 12 removals (4 flags + 6 phrases + 2 nested) + 2 AC-1.4 cases + 1 nested-propagation case + 1 only-brainstorm case. r2a3's Task 5 proposal adds two phrases (`writes no nested directory and no nested contract`, `only when /sc:analyze was invoked`), which gives 19, not 18. The plan's own AC ("more cases") survives either way; any hard-coded 18 does not. | UNADDRESSED | LOW | `tests/skills/test_worker_contract.py:286-296,519-527,554-568,901-906,955-983`; r2a2:76; r2a3:84; diagnostics.txt:11 |
| INV-009 | count_divergence | Task 2's AC `grep -c ... prints 2` counts matching lines across the whole file, not occurrences per tier. The consensus moves the pytest pin to per-tier slices (Tier 1 = routing:16-23, Tier 2 = routing:24-32). The longer C-004 phrase `writes no nested directory and no nested contract` still contains the grep string once per bullet, so 2 still holds. | ADDRESSED | LOW | plan:42,60; routing:16-33; r2a1:70; r2a3:82 |
| INV-010 | count_divergence | Stale offsets: Task 4 says "line 37" (actually 39), Task 5 says "line 286" (the phrase list is at 288), and Task 6 calls spec line 142 a "section 6 table" row (it is in 3.1). The consensus corrects all three. | ADDRESSED | LOW | `tests/skills/test_brainstorm_protocol.py:39`; `tests/skills/test_worker_contract.py:288`; spec:142,215 |
| INV-011 | collection_boundaries | r2a3's five-row run table, and its Task 1 wording "also when it failed and the scan fell back to `fallback_1`", assume a defined step from a failed `/sc:analyze` to `fallback_1`. The product text defines fallback only from auggie: routing Tier 1 is auggie only, Tier 2 activates when "Tier 1 returns error OR empty", and SKILL:424 says "fails (Auggie down)". The table also has no row for "analyze failed, then auggie succeeded" (`primary` plus a failed-analyze folder). The consensus would write undefined tier behaviour into an installed primitive. | UNADDRESSED | MEDIUM | routing:16,31; SKILL:187,199,424; r2a3:45-51,81 |
| INV-012 | collection_boundaries | When an enrichment source hits its 120 s timeout, the run records `quality_tier: skipped`. An `/sc:analyze` Task agent cut off by that timeout can leave `nested/analyze-<n>/` without a `return-contract.yaml`: analyze.md:98's "every outcome" cannot run after a kill, and nothing would be listed in `artifacts`. r2a3's folder clause ("every `nested/analyze-<n>/` holds its own `return-contract.yaml` listed in `artifacts`") then FAILS a correct run, a new false FAIL. Its table maps `skipped` to absent. | UNADDRESSED | MEDIUM | routing:77; `src/superclaude/commands/analyze.md:98`; r2a3:51,69 |
| INV-013 | collection_boundaries | Several nested analyze folders (retries, `<n>` above 1). The proposed folder clause quantifies over every `nested/analyze-<n>/`, so the check handles them. Residual risk, not covered by any proposal: only the adversarial F1 retry is told to use a new number (cmd:157), and analyze does not refuse a directory that already holds a contract (unlike brainstorm, cmd:153), so an analyze retry into `analyze-1` would overwrite the failed contract. | ADDRESSED | LOW | r2a3:69; cmd:153,157; `src/superclaude/commands/analyze.md:97` |
| INV-014 | collection_boundaries | A run with no codebase enrichment at all (non-code domain without `--codebase`, or `--no-codebase`) has no folder and no call, so the proposed clause holds trivially and does not misfire. | ADDRESSED | LOW | SKILL:187-191; r2a3:69 |
| INV-015 | collection_boundaries | `/sc:analyze` can be invoked and still create no folder, when it refuses an unusable report directory and prints the refusal in chat only. The proposed sentence carves this out ("the chat shows no refused report directory"). | ADDRESSED | LOW | `src/superclaude/commands/analyze.md:97`; r2a3:59,69 |
| INV-016 | interaction_effects | After Task 2, both codebase tiers of the routing ref say "writes no nested directory", and the ref never mentions `/sc:analyze` (Tier 1 is auggie). Wave 2A loads only that ref's §Enrichment-Sources. The run-level rule (folder only when `/sc:analyze` ran or was invoked) lives in SKILL and cmd only. A worker or checker reading the ref concludes that codebase enrichment never nests, which contradicts SKILL:195 and cmd:157. r2a1 saw the gap but proposed no fix. | UNADDRESSED | MEDIUM | routing:9-33; SKILL:179,187,195; cmd:157; r2a1:36 |
| INV-017 | interaction_effects | Two fixes collide. (a) r2a1 adds `session file` as a pinned Task 6 phrase, but the spec already contains "session file" 14 times (spec:291-302,312,323,336,464-466), so the pin proves nothing unless it is scoped to the bullet. (b) The consensus "split" placement (C-006) moves the live-check sentence out of the 2.1 bullet. Then plan:84's bullet scope no longer finds that sentence, and plan:85's "`git diff --stat` shows one line changed" fails because two places change. | UNADDRESSED | MEDIUM | plan:84-85; spec:62,291-302; r2a1:55,58; r2a3:73 |
| INV-018 | interaction_effects | Wording drift between the spec ("only for a nested command that actually ran", pinned) and the primitives (r2a3: "only when `/sc:analyze` was invoked"). r2a3's companion edit appends "including one that ran and failed" to the spec phrase, so the two mean the same thing. | ADDRESSED | LOW | plan:84; r2a3:73,77 |
| INV-019 | interaction_effects | Ordering: Task 4 depends on Tasks 1-2 and Task 5 on Task 3. The new pin phrases must match the primitive text byte for byte, backticks included. r2a3 states each phrase per task with the same spelling. | ADDRESSED | LOW | plan:58,69; r2a3:81-84 |
| INV-020 | sufficiency_challenge | The claim "the next live plan will not repeat lc10" fails at P2. From P2, brainstorm's research enrichment passes `--unattended` and a nested report directory (spec:142, spec:222). The research tiers break the "fallback writes no folder" rule: research-deep `fallback_1` is `Skill sc:research-protocol`, which is itself a nested command (routing:69); deep's final fallback "inherits" the tier (routing:73); research-light `fallback_1` is plain WebSearch (routing:48-52). The corrected live-check sentence covers only the codebase wave. The Task 1 wording puts "`fallback_1` ... write no nested directory" in the same paragraph as the research `skipped` text, which invites a reader to apply it to research too. P2 is also the next phase that edits brainstorm's Unattended section. | UNADDRESSED | HIGH | spec:142,222; routing:42-73; SKILL:195,199; `tests/skills/test_worker_contract.py:981-983` |
| INV-021 | sufficiency_challenge | The faulty lc10 extra came from the P1 live-plan brief and from decision D-P1-4, both worded "when the ... wave ran". Both are archived and read-only (plan:19). Spec 7.2 step 4 defines no extras (spec:286-290), so extras are written fresh per live plan. The only binding fix is a sentence appended in spec 2.1, and the 7.2 or P1-section placement is optional ("Optionally" in r2a1; "may" in r2a3). Nothing sends the next brief author to the new sentence instead of copying the archived pattern. | UNADDRESSED | MEDIUM | p1src:62; p1plan:34,275; spec:62,286-290; r2a1:58; r2a3:73 |
| INV-022 | sufficiency_challenge | Making the folder conditional also hides the opposite error, a false PASS. SKILL:187 lets the worker pick `/sc:analyze` OR auggie, and no flag forces analyze. In lc10 no analyze call was made. Under the corrected wording, no live check can show that the D-P1-4 nested analyze route works, so a broken analyze propagation passes every future check. | UNADDRESSED | MEDIUM | SKILL:187; `.dev/tasks/done/TASK-WF-p1LivePlanBrief-20261105-164506/artifacts/lc10-result.md:8,13`; p1plan:34 |
| INV-023 | sufficiency_challenge | The missing-folder half of the proposed extra depends on the 7.2 step 5 session-file analysis. When that file is missing or ambiguous, step 5 is "not verifiable" and needs the owner's written acceptance. r2a3 states this limit openly in its self-critique and accepts it. | ADDRESSED | LOW | spec:292,300; r2a3:86 |
| INV-024 | sufficiency_challenge | The session-file clause assumes an `/sc:analyze` call shows up as a named `tool_use`. `analyze.md` names no protocol skill (the `sc:analyze` name is INFERRED). A Task subagent could also Read the command file and run it inline, with no Skill call at all. In that case a missing folder after a real analyze run cannot be detected. lc10's method looked only at top-level Skill calls. | UNADDRESSED | LOW | r2a3:57; spec:292,302; lc10-result.md:13; SKILL:183 |

## Summary

- **Total findings**: 24
- **ADDRESSED**: 10
- **UNADDRESSED**: 14
  - HIGH: 1
  - MEDIUM: 9
  - LOW: 4

## Scoring Matrix

Citations: "a1:N", "a2:N", "a3:N" are lines of `rounds/round2-advocate-1.md`, `-2.md`, `-3.md` (each advocate's FINAL Round 2 table row, or the prose line named). Winner notation: a single variant (V1/V2/V3); `none` when the advocates agreed that no variant is superior; `split (Va+Vb)` when the advocates AGREED on a joint verdict that names both variants for different halves of the point (agreed=true, not an unresolved split); for A- points the agreed verdict (ACCEPT/REJECT/QUALIFY) is given. Confidence: unanimous 90-99, majority 60-89, unresolved split 50; never 100.

| Point | Level | Winner | Agreement | Confidence | Evidence summary (Round 2) |
|---|---|---|---|---|---|
| S-001 | L2 | none | unanimous | 92% | All three hold that each card carries 2 P1s and the count gap is bundling plus offsetting over-ratings (R1-1, R3-2) (a1:64, a2:67, a3:92). Counts do not rank the cards. |
| S-002 | L2 | none | unanimous | 93% | Each advocate conceded a tagging flaw in its own card: R1-5 INFERRED hid a groundable premise, R3-1 Grounded carried a remedy refuted by SKILL.md:372, R2-1 "doubly" overreached inside a Grounded tag (a1:65, a2:68, a3:93). |
| C-001 | L3 | split (V2 diagnosis + V1 remedy) | unanimous | 95% | All three re-ran the baseline (950 `A`, 3 `R`, 953 tracked paths, package untracked) and agree plan:98's first clause fails; V2 named the operative clause, V1's before/after `git status` diff is the remedy (a1:66, a2:69, a3:94). |
| C-002 | L3 | V3 | unanimous | 96% | Task 4's section-wide `fallback_1` assertion is vacuous because SKILL.md:199 is inside Wave 2A, while Task 1's paragraph clause (SKILL.md:195) is not vacuous but unpinned; V3's "stays untested" covers both halves (a1:67, a2:70, a3:95). |
| C-003 | L2 | split (V1+V2) | unanimous | 96% | P2 is correct: an added bullet keeps every string `test_codegraph_adoption.py:75-82` asserts; V3 conceded its P1 (a1:68, a2:71, a3:96; a3:14). |
| C-004 | L3 | V2 | unanimous | 94% | src:6 requires "lists no nested contract in artifacts" and no planned pin covers that half (plan:33,60,74); V1 and V3 moved to V2 (a1:69, a2:72, a3:97). |
| C-005 | L3 | split (V1+V3) | unanimous | 95% | `grep -c` (plan:42) and "at least twice" (plan:60) are file-wide; slice per codebase tier with `_section` (`test_codegraph_adoption.py:56-59`) (a1:70, a2:73, a3:98). |
| C-006 | L2 | split (V1 defensible + V3 placement) | unanimous | 90% | 7.2/7.3 define no per-command extras (spec:281-327), so src:9's P1-note branch applies to the live-check sentence while spec:376 keeps the general rule defensible in 2.1 (a1:71, a2:74, a3:99). |
| C-007 | L3 | V3 | unanimous | 92% | All three hold V3's diagnosis: a clean `/sc:analyze` run is also `primary` (SKILL.md:187,198), and no original remedy works because `source` cannot name the tool (SKILL.md:372) (a1:72, a2:75, a3:100). The replacement wording is NOT agreed: V1's session-file sentence (a1:52), V2's carve-out to it (a2:34), V3's folder-plus-session-file sentence (a3:69). |
| C-008 | L3 | split (V2 number + V1/V3 method) | unanimous | 93% | 17 is the recorded baseline (diagnostics.txt:11) but A-004 moves, so Task 5 records its own before-count (a1:73, a2:76, a3:101). |
| C-009 | L1 | split (V1+V2) | unanimous | 96% | Tier 2 ends with the Activation bullet (routing:31), not `quality_tier` (routing:30); V3 conceded the miss (a1:74, a2:77, a3:102; a3:18). |
| C-010 | L1 | split (V1+V2) | unanimous | 94% | Test at `test_brainstorm_protocol.py:39`, phrase list at `test_worker_contract.py:288`, line 711 synthetic; V1 and V2 equal, V3 silent (a1:75, a2:78, a3:103). |
| C-011 | L1 | V3 | unanimous | 98% | Spec line 142 is under `### 3.1` (spec:136-142) and `## 6` starts at spec:215; uncontested in both rounds (a1:76, a2:79, a3:104). |
| C-012 | L1 | V3 | unanimous | 91% | `write` is not a substring of `writes` (plan:30 vs 39,47) and `no nested directory` is a substring of both; V1 withdrew "weakens the pin" (a1:77, a2:80, a3:105). |
| C-013 | L2 | split (V1+V2) | unanimous | 93% | V1 and V2 name both missing test files; V3 withdrew R3-8 as a misreading of plan:21 (a1:78, a2:81, a3:106; a3:15). |
| X-001 | L3 | split (V2+V3) | unanimous | 95% | Only Task 4's assertion is vacuous (SKILL.md:199); Task 1's clause fails on old text (SKILL.md:195) but is unpinned; V1 conceded it was wrong (a1:79, a2:82, a3:107; a1:11). |
| X-002 | L2 | split (V1+V2) | unanimous | 97% | P2: no assertion in `test_codegraph_adoption.py:75-82` or `test_tier2_tavily_consistency.py:40-53` touches the new text; V3 conceded (a1:80, a2:83, a3:108). |
| X-003 | L3 | V3 | unanimous | 92% | Severity P1 agreed by all three; V3 widened it: plan:81 is wrong for both tiers, since an analyze-failed run is `fallback_1` with a folder (a3:43-53, a3:109; a1:81, a2:84). Remedy not agreed (same as C-007). |
| X-004 | L2 | split (V1 defensible + V3 placement) | unanimous | 90% | Same evidence as C-006; all three moved from a single winner to the joint verdict (a1:82, a2:85, a3:110). |
| X-005 | L3 | V2 | unanimous | 95% | The first clause fails under any reading (staged `A`/`R` are tracked); the `done/` clause is reading-dependent, so "doubly" overreaches, which V2 conceded (a1:83, a2:86, a3:111; a2:13). |
| A-001 | L3 | ACCEPT | unanimous | 95% | All three read both tests in full; planned text touches no asserted string (a1:84, a2:87, a3:112). Not executed; Task 7 should still run both. |
| A-002 | L3 | QUALIFY | unanimous | 93% | An LLM reviewer judges each AC, so literal reading is likely, not certain; an infeasible AC reaches `E-HALT-QA` (qa.md:49,247; retry.md:72,107) (a1:85, a2:88, a3:113). |
| A-003 | L2 | ACCEPT | majority (2 of 3) | 78% | V1 and V2 ACCEPT substring pins as house style with scope/coverage/verb-form tuning (a1:86, a2:89); V3 QUALIFY: pins prove presence, not run-level truth (a3:114). |
| A-004 | L3 | QUALIFY | unanimous | 96% | Baseline re-run by all three (950 `A` / 3 `R` / 4 `??`); baselines move once the staged archive commits, so Tasks 5 and 7 capture their own before-state (a1:87, a2:90, a3:115). |

## Per-Point Tracking

**Agreement rule used (applied identically to every point).**

1. Each advocate's position is taken from the "Superior position" column of its Round 1 table and the "Final superior position" column of its Round 2 FINAL table, normalised to a verdict label: a single variant (V1/V2/V3); `none`; or a named joint verdict `split (Va+Vb)` where the advocate names which variants are superior on which half. Severity or remedy qualifiers after the variant label (for example "V3 on severity; remedy none") do not change the label.
2. Two positions are the same only if their normalised labels are identical (same single variant; both `none`; or the same named set of variants in a joint verdict). A bare `split` that names different variants is a different label.
3. Unanimous = all three labels identical. Majority = exactly two identical. Otherwise unresolved (agreed=false). For A- points the label is ACCEPT/REJECT/QUALIFY with the same rule.
4. Agreed = unanimous or majority. Winner = the agreed label. Convergence = agreed points / 24.

| Point | Level | R1 Adv-1 | R1 Adv-2 | R1 Adv-3 | R1 result | R2 Adv-1 | R2 Adv-2 | R2 Adv-3 | R2 result | Agreed | Winner |
|---|---|---|---|---|---|---|---|---|---|---|---|
| S-001 | L2 | split | none | none | majority none | none | none | none | unanimous | true | none |
| S-002 | L2 | V1 | V2 | split (V1+V3) | unresolved | none | none | none | unanimous | true | none |
| C-001 | L3 | split (V2+V1) | V2 | V2 | majority V2 | split (V2 diag + V1 remedy) | same | same | unanimous | true | split (V2+V1) |
| C-002 | L3 | V3 | split (V2+V3) | V3 | majority V3 | V3 | V3 | V3 | unanimous | true | V3 |
| C-003 | L2 | split (V1+V2) | split (V1+V2) | V2 | majority split (V1+V2) | split (V1+V2) | same | same | unanimous | true | split (V1+V2) |
| C-004 | L3 | split (V2+V1) | V2 | V2 | majority V2 | V2 | V2 | V2 | unanimous | true | V2 |
| C-005 | L3 | split (V1+V3) | split (V1+V3) | split (V1+V3) | unanimous | split (V1+V3) | same | same | unanimous | true | split (V1+V3) |
| C-006 | L2 | V1 | split (V1+V3) | V3 | unresolved | split (V1 defensible + V3 placement) | same | same | unanimous | true | split (V1+V3) |
| C-007 | L3 | split (V3+V1) | V3 | V3 | majority V3 | V3 (remedy none) | V3 (remedy: V1 R2 closest) | V3 (remedy: own R2 sentence) | unanimous on V3 | true | V3 |
| C-008 | L3 | split (V1+V2) | V2 | V2 | majority V2 | split (V2 number + V1/V3 method) | same | same | unanimous | true | split (V2+V1/V3) |
| C-009 | L1 | split (V1+V2) | split (V1+V2) | split (V1+V2) | unanimous | split (V1+V2) | same | same | unanimous | true | split (V1+V2) |
| C-010 | L1 | split (V1+V2) | V2 | V2 | majority V2 | split (V1+V2) | same | same | unanimous | true | split (V1+V2) |
| C-011 | L1 | V3 | V3 | V3 | unanimous | V3 | V3 | V3 | unanimous | true | V3 |
| C-012 | L1 | none | V3 | V3 | majority V3 | V3 | V3 | V3 | unanimous | true | V3 |
| C-013 | L2 | V1 | V2 | V3 | unresolved | split (V1+V2) | same | same | unanimous | true | split (V1+V2) |
| X-001 | L3 | V3 | V2 | V3 | majority V3 | split (V2+V3) | same | same | unanimous | true | split (V2+V3) |
| X-002 | L2 | V1 | split (V1+V2) | split (V1+V2) | majority split (V1+V2) | split (V1+V2) | same | same | unanimous | true | split (V1+V2) |
| X-003 | L3 | V3 | V3 | V3 | unanimous | V3 (remedy none) | V3 (remedy none; V1 R2 closest) | V3 (remedy: own R2 sentence) | unanimous on V3 | true | V3 |
| X-004 | L2 | V1 | V3 | V3 | majority V3 | split (V1 defensible + V3 placement) | same | same | unanimous | true | split (V1+V3) |
| X-005 | L3 | V2 | V2 | V2 | unanimous | V2 | V2 | V2 | unanimous | true | V2 |
| A-001 | L3 | ACCEPT | ACCEPT | ACCEPT | unanimous | ACCEPT | ACCEPT | ACCEPT | unanimous | true | ACCEPT |
| A-002 | L3 | QUALIFY | QUALIFY | QUALIFY | unanimous | QUALIFY | QUALIFY | QUALIFY | unanimous | true | QUALIFY |
| A-003 | L2 | ACCEPT | ACCEPT | QUALIFY | majority ACCEPT | ACCEPT | ACCEPT | QUALIFY | majority | true | ACCEPT |
| A-004 | L3 | QUALIFY | QUALIFY | QUALIFY | unanimous | QUALIFY | QUALIFY | QUALIFY | unanimous | true | QUALIFY |

Round totals: Round 1 agreed 21 of 24 (87.5%; unresolved S-002, C-006, C-013). Round 2 agreed 24 of 24 (100%; 23 unanimous, 1 majority: A-003). Agreement was at or above 80% in both rounds (stable majority). Oscillation check: no point returned to an earlier winner; the Round 1 to Round 2 changes (C-001, C-006, C-008, C-010, C-013, X-001, X-004 and S-001/S-002) all moved to a joint or `none` verdict that every advocate signed.

Open item that is not a scored point: the replacement wording for C-007/X-003 is not agreed. Three different sentences were proposed (a1:52; a2:34 carve-out to a1's; a3:69), and Round 2.5 rows INV-007, INV-011, INV-012 and INV-024 attack the a3 proposal. This carries into Step 3 and the refactor plan as unagreed remedy text.

### Shared assumptions

| A-NNN | Assumption (short) | R1 Adv-1 | R1 Adv-2 | R1 Adv-3 | R2 Adv-1 | R2 Adv-2 | R2 Adv-3 | Verdict |
|---|---|---|---|---|---|---|---|---|
| A-001 | Planned edits leave `test_codegraph_adoption.py` and `test_tier2_tavily_consistency.py` passing | ACCEPT (read both; bullet must go inside the Tier 2 list) | ACCEPT (read both; breaks only on out-of-scope edits) | ACCEPT (read both; C-003/X-002 is P2) | ACCEPT (read in full; adds the `_FORBIDDEN` guard at `test_brainstorm_protocol.py:15-21,50-54`) | ACCEPT (no forbidden token, no asserted string touched) | ACCEPT (re-read 75-82,115-143; run both anyway) | ACCEPT, unanimous. Read-only evidence; no advocate ran the tests. |
| A-002 | `/sc:implement` judges each AC literally, so an unpassable bullet blocks completion | QUALIFY (LLM reviewer; likely literal; `E-HALT-QA` path) | QUALIFY (literal per-bullet QA; a charitable reading would demote C-001 to P2) | QUALIFY (infeasible AC leads to `dispute`, then `E-HALT-QA`) | QUALIFY | QUALIFY | QUALIFY | QUALIFY, unanimous: C-001 is a blocker in practice through the halt path, not certain through a literal fail. |
| A-003 | Exact-substring tests are the right way to pin the wording | ACCEPT (house style; needs scope and coverage) | ACCEPT (house style; C-012 tunes the phrase) | QUALIFY (needs scope and one shared phrase) | ACCEPT | ACCEPT | QUALIFY (pins prove presence, not run-level truth) | ACCEPT, majority 2 of 3; V3's qualification (presence is not run-level truth) is recorded. |
| A-004 | Tree state at execution equals today's state | QUALIFY (capture before-state at run time) | QUALIFY (staged archive one commit from vanishing) | QUALIFY (holds today; record baselines in Tasks 5 and 7) | QUALIFY | QUALIFY | QUALIFY | QUALIFY, unanimous: Tasks 5 and 7 capture their own baselines. |

## Taxonomy Coverage

Tagging rule: the skill's auto-tagging (`debate_topic_taxonomy`): L3 for state, guard, boundary, invariant, validation-rule, transition or concurrency signals; L2 for architecture, API, component, module, interface, dependency or organization signals; L1 for naming, formatting, wording or style; priority L3 > L2 > L1; default L2; A- points with state/guard/boundary terms are L3. Signals were matched on each point's substance as stated in `diff-analysis.md` and the debate. An acceptance criterion or test assertion that admits or blocks a run is treated as a validation rule (guard), and a slice scope as a boundary.

| Level | Count | Points |
|---|---|---|
| L3 state mechanics | 12 | C-001 (AC vs tree state), C-002 (vacuous guard), C-004 (core rule has no guard), C-005 (pin boundary file-wide vs per tier), C-007 (tier-to-folder validation rule), C-008 (baseline state for a count check), X-001 (guard vacuity), X-003 (same rule as C-007), X-005 (AC clause vs staged state), A-001 ("invariant of the edited Tier 2 block"), A-002 ("guard-condition (validation rule)"), A-004 ("tree state") |
| L2 structural | 8 | S-001, S-002 (no signal, default), C-003, C-013, X-002 (test-set dependency/coverage), C-006, X-004 (placement/organization), A-003 (pinning method, no state/guard term) |
| L1 surface | 4 | C-009 (list-ending description), C-010 (stale line numbers), C-011 (section label), C-012 (verb-form wording) |
| Total | 24 | |

Departures from the Level column in `diff-analysis.md`: C-002, C-004, C-005 and C-007 move from L2 to L3 (guard, boundary and validation-rule signals outrank L2), and C-008 moves from L1 to L3 (baseline state). The diff-analysis gave no level for S-, X- or A- points.

Coverage gate: every level has at least one point that all three advocates addressed in both rounds (L3 12, L2 8, L1 4). Result: PASS. No forced round.

## Convergence Assessment

- Points resolved: 24 of 24
- Alignment: 100% (Round 1: 87.5%)
- Threshold: 80%

| Gate | Result | Detail |
|---|---|---|
| Score | PASS | 24 / 24 = 1.00 >= 0.80; stable over two rounds (0.875, then 1.00) |
| Taxonomy | PASS | L1 4, L2 8, L3 12; no level at zero |
| Invariants | FAIL | UNADDRESSED: HIGH 1, MEDIUM 9, LOW 4 (of 24 probe rows; 10 ADDRESSED) |

- Blocking (HIGH + UNADDRESSED): INV-020. The sufficiency claim that the next live plan will not repeat lc10 fails at P2: from P2 the research enrichment passes `--unattended` and a nested report directory (spec:142, spec:222), research-deep `fallback_1` is itself a nested command (routing:69), and the corrected live-check sentence covers only the codebase wave.
- Warnings (MEDIUM + UNADDRESSED, not blocking): INV-001, INV-002, INV-007, INV-011, INV-012, INV-016, INV-017, INV-021, INV-022.
- LOW + UNADDRESSED (no action): INV-005, INV-006, INV-008, INV-024.
- Unresolved diff points: none.
- Not agreed and carried forward: the C-007/X-003 replacement wording (three competing proposals; INV-007, INV-011, INV-012 and INV-024 apply to them).
- Round 3: not run (--depth standard).

**Final status: BLOCKED_BY_INVARIANTS.** CONVERGENCE BLOCKED: 1 HIGH-severity UNADDRESSED invariant detected. Blocking items: INV-020. It must be addressed in a later debate round or accepted as a risk before convergence can be declared.

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

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

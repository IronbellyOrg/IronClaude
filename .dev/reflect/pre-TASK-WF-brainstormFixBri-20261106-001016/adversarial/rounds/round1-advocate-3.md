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

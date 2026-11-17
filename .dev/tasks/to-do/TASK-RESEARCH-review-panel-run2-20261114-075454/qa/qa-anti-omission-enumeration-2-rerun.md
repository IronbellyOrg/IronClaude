# Anti-Omission Enumeration (Gate 5, agent 2, rerun)

Report reviewed: RESEARCH-REPORT-review-panel-unification-run2.md
Date: 2026-11-14
Status: Complete

One numbered list of distinct findings per assigned file; each list ends with `COUNT <file name>: <n>`.

Coverage method (stated once): files 1-6 (research 06-11) and 9-10 (web-03, web-04) were judged by meaning with Grep probes of the report, then reading the report subsection that carries the source (2.1, 2.2, 2.3, 2.7, 5.3, 5.4, 5.5); items not found in the report body were searched in Appendix A (synthesis/synth-08-value-inventory.md, part of the report package). Files 7-8 (ledgers 21 and 20) were checked row by row by a read-only script: every ledger row id was located in Appendix A AND its Statement, Kind and Source were compared as text, AND its destination was compared (same destination, or a `moved from <old>` reason, or a `DROP[duplicate]` chain to a kept row); the script also looked for each Statement anywhere in Appendix A independent of id. Files 11-13 (synth-04, synth-09, synth-10): a read-only `grep -Fxv -f <report> <file>` shows every non-blank line of each file is present verbatim in the report except 4, 16 and 5 heading or title lines (headings with changed levels, all located). Rows below the ledger sections are therefore REPRESENTED unless a Section 3 note in the report file says otherwise. Statuses per row of files 1-6 and 9-10 are in the report (qa-anti-omission-report-2-rerun.md), exceptions only.

## File 1: research/06-reflect-two-engines.md

1. HEAD 50d4d2b9d on branch ironbelly/shadow-runs; line counts of reflect modules (runner 834, ensemble 895, contract 420, panel_lint 366, SKILL 2033)
2. reflect_shadow_exit.py is read-only without --out (writes only with --out)
3. Exit script at HEAD: 13 of 20 runs, MALFORMED 0, EV-1 shadow 8/13=0.615 vs legacy 3/39=0.077, parity fails 6/13, lint 9/13, replay 0 new reasons, 2-of-3 shortfalls 0, compliance 0.704, OVERALL FAIL
4. pytest tests/cli/reflect: 352 passed, 1 xpassed
5. Second run on combo runs root: 15 of 20, EV-1 3/15, legacy 0/0 n/a, 29 new degraded reasons (artifact of empty baseline)
6. contract.py is the single verdict map, pure, order blocked->degraded->halted->pass, first-match-wins
7. parse_contract tolerates unknown top-level keys (NFR-8 read-and-ignore); only panel_lint rejects them
8. derive_verdict BLOCKED gating list (timeout 124, child-crash, contract-missing, version-missing, unknown-major, malformed degraded_components, malformed bool)
9. 14 DEGRADED trigger slugs in order (degraded-components set, tier1, model-diversity, single-vendor, adversarial-unavailable, single-reviewer-fallback, null-convergence, subrun-partial, low-convergence, verification-skipped + exemptions, citations-dropped, input-drift)
10. HALTED reasons and tier-mismatch; PASS only when success AND tier_reached == expected
11. Convergence threshold 0.80 in code (contract.py:321) vs skill 0.75/0.60; incident 0.75; code is stricter, unreconciled
12. 19 fields derive_verdict reads; 6 more copied by _make_result; fields never read (merged-verdict.yaml, reviewer_cards, evidence_validator_ran ...)
13. classify_fix: human-required / auto-fixable / none; docstring cites stale SKILL.md:754
14. 36-test verdict matrix test_verdict_mapping.py (what "verdict map frozen" means)
15. Engine A data flow (run_tier2_ensemble, t2-swarm dir, preflight manifest, stub transport pool, dispatch_wave1, normalize passthrough, optional T1 fallback ladder, reduce, adversarial child ClaudeProcess, parse adversarial contract, build_reflect_contract, unlink on zero workers)
16. Engine A hard-codes contract_version 1.0 (not 1.8.0), status success, mode post, tier_reached/merge_method derived from reviewer COUNT even if adversarial child failed
17. Engine A verification_ran False + no-verification-stage (exempt, never DEGRADED even under --promote)
18. Engine A deviation signal all zero, regression_present False by construction; PASS means "no more than 0.20 apart and nothing crashed", not "no deviation found"
19. reviewers_verified and benign reviewer-shortfall token not in halt set: 2-of-3 stays PASS-eligible
20. Swarm reviewers see only tasklist body + base header (no diff, no spec); full git-diff materialization is a logged follow-up
21. Swarm lens file/template content not opened [UNVERIFIED]
22. Key probe: swarm contract 32 keys, 10 keys outside frozen lists (named), 89 of 110 stable names absent, single-vendor and one-worker behaviours
23. _diversity.py: full/insufficient vocabulary vs skill full/degraded; vendor table "o1" substring edge case; order of markers
24. Diversity from SERVED model ids (engine A) vs REQUESTED rotation (engine B)
25. panel_lint constants: STABLE_FIELDS_1_8_0 110, TELEMETRY_FIELDS 27, PARITY_FIELDS 5, LEGAL_MERGE_METHODS, CONTRACT_VERSION, lists copied from SKILL 9.1/9.2 with drift test
26. lint assertion map L0-L7 + B (file, version, unknown key, merge_method, float score, load-bearing bools, EV-1, parity)
27. _ev1 rule: required=max(2,resolved), pass 1 merged-verdict + cards regex, pass 2 loud fallback with audit.log F2|F3; ev1_failures use_manifest
28. Lint does not cover --unattended nested/adversarial-<n> layout
29. Lint is called only from exit script and tests; runner/commands/ensemble never import it; swarm contract fails lint at L1, L2, L7 (lint-hostile)
30. reviewer_briefs_materialized: emitted per refs/reviewer-spec.md but in neither lint list nor SKILL 9.1/9.2; fails lint (5 of 15 combo runs)
31. Production wiring: _audit_once runs engine A for standard/deep when ClaudeProcess is the production class; skill /sc:reflect child reachable only from test double; quick floored to standard
32. Tier-1 child prompt never passes --t2-engine
33. Grep: reflect package has no shadow/panel/manifest/cluster/findings-v2 logic; no import of superclaude.cli.review
34. Callers of wrapper: sc-tasklist L1133-1165 + phase-template, task-builder CLI_MODE; shadow engine reached only by /sc:reflect --mode pre (sc:workflow Wave 4, sc-tasklist Stage 10.5)
35. --fix has no producer in production (no remediation_* in swarm contract); HALTED exit 10 and auto-fix loop structurally dormant; sc-tasklist gate passes --fix anyway
36. Executor-class exclusion not applied by engine A (executor_model only reaches the Tier-1 prompt); sc-tasklist L1141/1152/1165 and task-builder L2247 claims are STALE/CODE-CONTRADICTED
37. Two diversity vocabularies and two EV-1 notions simultaneously live; nothing in runner/contract reads merged-verdict.yaml
38. Promotion default drift: Click default --promote True vs runner comment "--no-promote is the hard default"; affects derive_verdict exemptions
39. cli/reflect/__init__.py docstring stale (claude --print subprocess; five modules)
40. config.py facts: reviewers clamp [2,4], 1 = negative witness, stub transport fallback OFF, quick floored, default output path, .claude output rejected, timeout/max_turns constants
41. Engine A model choice via T2Model0N/T1Model0N env slots = a THIRD model registry
42. fallback.py: pure planner functions then run_fallback_ladder; FALLBACK_ELIGIBLE_STATUSES, TERMINAL_REASONS 8, TIER2_CERTIFICATION_BASES; QuorumState Tier-2 gate (>=2 reviewers, >=2 model ids, not single-vendor); no skill-side code equivalent
43. Engine A value list: fail-closed exit codes, atomic write-back, recursion breaker, reviewer-isolation snapshot, bounded fallback ladder (independent of reviewer engine)
44. Engine B = prose Wave 0-7 pipeline; grounding chain; reuse-auditor, verification, reachability gate; none exist in engine A
45. Deviation taxonomy: 4 classes, precedence Regression > Drift > Necessary > Authorized, Grounding Gaps separate, modifiers map onto classes; only place regression_present decided from evidence
46. Shadow path flag --t2-engine legacy|shadow default legacy, panel rejected "ships in Stage 3", rules D1-D5, UC-1 only, ten steps under <output>/panel/ performed by orchestrator LLM
47. Ten shadow steps classification table (deterministic vs LLM, observed failure class); 7 of 10 deterministic, all observed failures in deterministic steps
48. Convergence thresholds skill vs code; 0.75-0.7999 band PASS in skill, DEGRADED in wrapper; null handling; promotion gate condition 9
49. Six skill-vs-code vocabulary conflicts table (diversity enum, single vendor severity, contract_version, merge_method meaning, skill version 3 strings, reviewer_briefs_materialized, growth rule)
50. Stale citation SKILL.md:754 in classify_fix (invariant at L1155-L1159)
51. Byte-identity tests compare to current HEAD (re-baseline after commit); only frozen link is test_pinned_field_lists_match_skill_md
52. Stage 2 exit state: three independent reasons (count, EV-1 rate, parity/lint); INSUFFICIENT-RUNS exit 3; clean gates (MALFORMED, replay, 2-of-3)
53. cluster_agreement 1.000 vacuous (1.0 by definition without blocking cluster)
54. Failure arithmetic: "no contract" label means unparseable YAML at line 103 (unquoted [1m] aliases) in runs 04/08/09, merged-verdict absent 4, empty cards 1, parity 4+2
55. Mechanical vs judgment: every failure is a presence/name/equality check; table of failure classes and where code would go (serializer, merge finalizer, card writer, header writer)
56. reviewer-cards naming: lint counts only reviewer-<N>-card.*, cards named reviewer-N.md; 51 of 59 dirs use -card, 2 use reviewer-N.md
57. Parity failure classes (alias header, free-text rotation model, missing rotation keys, header lacks persona/model_class/model); recorded panel_parity true but recomputed false 6 of 28
58. L2 key leaks 7 of 28 runs (2 pilot + 5 combo), invented keys zero_drop_flag/memory_status/notes/run_started/run_finished; 5 from skill's own reviewer_briefs_materialized
59. Compliance mean 0.704 pilot / 0.867 combos: format drift fixed in prose by commits 9874d63fb, c2e3347d3; code-computable
60. Exit script measures orchestrator hygiene not review quality; pilot-design quality measurement never run; no review-content failure found
61. Gate-design defect: empty legacy baseline treated as 0.0 (L313); replay counts all as new
62. Exit docstring: lint L7 parity trivially equal; parity recomputed
63. Corpus bias: all runs forced --tier 2 on parsed-sparse input; exit says nothing about tier selection
64. EV-1 per engine: skill prompt rule vs code post hoc; swarm EV-1 inapplicable (count-derived merge_method); 0.75-vs-0.80 incident is swarm's
65. Side-by-side table of engine A vs engine B (17 properties: reached by, reviewers, calibration, evidence gate, merge, deviation classes, contract, diversity evidence, executor exclusion, verdict/exit, isolation, resilience, failure mode, panel kernel)
66. (a) Must stay byte-identical: 6 items (1.8.0 field lists + consumer map 9.3, merge_method values, verdict map + 36 tests, four deviation keys, brief structure + findings grammar limits, EV-1 layout)
67. Not inherently byte-identical: literal 1.8.0 (1.9.0 additive bump path and what it needs); byte tests vs HEAD; engine A's 10 keys not consumed outside reflect (outside-src consumers UNVERIFIED)
68. (b) All failures mechanical; reusable existing code (panel_lint._ev1, recompute_parity, ensemble extractors, review kernel commands); deterministic steps 1,2,5,6,7,8,10
69. Additional deterministic prose logic candidates (Wave 7 9-condition promotion gate, convergence routing, verification-command envelope, executor exclusion + calibrator disjoint rule, memory retention trim) and what must stay LLM judgment
70. (c) Shared code is contract.parse_contract/derive_verdict only (online for A, offline replay for B; panel_lint imports bool list)
71. (d) Which engine to absorb: what is lost each way; composition: B data model + kernel as core inside A's execution shell; --fix precondition
72. Gaps list: wrapper vs engine-B intended design question (Q1); lens template unread; outside-src consumers of 10 keys; test behaviour inferred from names; inherited slice-11 items; unread runner/commands/config/fallback ranges; unread SKILL ranges; reviewer_briefs_materialized fix choice; why EV-1 jumped 3/39 -> 8/13; 28-run denominator; which of 0.75/0.80 intended
73. Stale-doc table extras: refs/reflection-rubric.md class vocabulary mismatch (Aligned/Refinement vs Authorized/Necessary); PLAN.md/combos.json "designed, NOT run" vs 15 runs; SKILL.md L1815 skill_version 1.7.0 sample

COUNT 06-reflect-two-engines.md: 73

## File 2: research/07-e1-evidence-grading.md

1. Strength scale and run naming (strong/moderate/weak/anecdotal; pilot = 15 shadow dirs, combo = 5x3)
2. Recount: 15 of 15 combo published, 3 of 3 reviewers, merge_method adversarial, leak false; pilot 13 of 15 counted (shadow01 legacy, shadow02 clustered)
3. 4,119,747 output tokens, USD 478.40 name-based estimate, 489.2 min wall
4. 216 clusters, 255 members, 203 single, 13 multi (6 chained, 7 unchained: wording correction "7 unchained"); pre-gate 234/273
5. AI-labelled 50-pair check TP21 FP4 FN1 TN24, precision 0.84 recall 0.9545; labels are AI labels
6. FINDINGS.md medians match results.jsonl; first-pass compliance 10 of 15 at 1.0, mean 0.867
7. parity False 4 of 15 combo (A1,A2,A3,C2); lint_clean False 8 of 15
8. Exit script on .dev/reflect numbers (13/20, 8/13=0.615 vs 3/39, replay 42 runs 0 new, compliance 0.704, FAIL) and on combo root (3/15, 0/0, 29 new, FAIL) both from empty baseline
9. verdict replay: 42 replayed, 49 skipped, 0 differences, self-replay cannot find a difference by construction
10. Stage 0a: committed 479/712=67.28% and 24/358=6.70%; rerun 495/781=63.38%, 24/379=6.33%; dated snapshot, drifts
11. consumer inventory: 472 of 4464 vs committed 320 of 3423 (drift, not stable)
12. git status unchanged after runs (scripts wrote nothing)
13. Orchestrator token share recount (per-run values; min 0.385, median 0.588, max 0.867); upper bound in B/C/D because orchestrator alias = sonnet class; clean only A and E (0.385-0.806, median 0.568)
14. Raw-log recount of tokens (max total_cost_usd per log, cumulative series safe; checked 3 logs); requested class vs served model per call: 15 runs 0 differences
15. E1-F1 pipeline completes (strong; ends, not right)
16. E1-F2 cost per run (min 93,616 A3, max 367,381 E3); T-4 p95 65k kill line is in a different unit
17. E1-F3 orchestrator share of tokens (moderate)
18. E1-F4 dispatch collapse A3 (no class to 3 reviewers/3 calibrators, all served claude-sonnet-5-5), 0 of 12 tier1b collapsed; pilot 6/9 not re-derivable
19. E1-F5 calibrator dispatched without class in 6 of 15 runs (named counts)
20. E1-F6 served model differs from recorded class (haiku slot served by gpt-6.1-sol in A1,A2,B1-B3; sonnet slot by claude-haiku-5-5 in E1-E3); gateway-window bound
21. E1-F7 contract diversity/identity telemetry blind to served model (A3 values; t2_vendor_diversity single for A,B,C; identity_source requested-pinned 14/15, observed 1)
22. E1-F8 orchestrator not review quality decides Stage 2 gates (EV-1 8/13: 3 unparseable YAML, 4 merged-verdict absent, 1 empty cards; combo EV-1 3/15 reviewer-N.md; parity 6/13 + 4/15)
23. E1-F9 verify-citations/clusterer blind: 0 resolved citations in 7/15 combo and 4/13 pilot; totals 373/360 and 192/108; A1 62 of 62 not-in-snapshot; snapshot path prefix + --root cause; pre-check totals 372/2/26
24. E1-F10 cross-reviewer overlap low; cluster_agreement vacuous (1.0 by definition; A2,B1,B3,C3; others 0.143-0.540); split by citation resolution (113/0 vs 103/13 = 12.6%); pilot 71 clusters/19 multi; W-1..W-3 unfixed
25. E1-F11 model-combination leads weak (speed A 64/68 vs B 23-39, confidence D/E below A, compliance A 0.667 vs 1.0); "leads, not findings" rule; A3 confound
26. E1-F12 first-pass compliance pilot 0.704 over 9 / combo 0.867 over 15; definition mixed; skill text changed in 9874d63fb
27. E1-F13 Stage 2 exit OVERALL FAIL 13 of 20; L313 empty baseline defect; 29 new degraded
28. E1-F14 Stage 0a: 689 findings, 0 per-finding calibration, 479/712; owner redefined gate 2026-11-12; rerun 713 of 713 because 45 new unlisted cards; replay cannot read panel/cards
29. E1-F15 AI-labelled 50-pair strata (merged same-file 25: 21/4; apart same-file 13; apart cross-file 12), 24 runs, apart pool 4031 vs 41 merged; labels AI not human
30. E1-F16 combo runs used lagging installed skill (reviewer-spec.md b1032d61 vs src 177db4a7, SKILL e200313b); deliberate freeze
31. E1-F17 15 runs shared one memory file; B2 notes: script error truncated deviation-patterns file to 0 bytes
32. E1-F18 qualitative lessons in deviation-patterns memory (anecdotal); lesson that clusterer ignores fenced yaml contradicted by cluster_cmd.py
33. E1-F19 troubleshoot report names three root causes (parity string, missing merged-verdict write step, first-pass metric definition), two prompt-only fixes (9874d63fb, c2e3347d3); tier-1 quick pass over 5 runs; effect not isolated
34. N-1 no quality measurement for any of 30 runs; FINDINGS.md says nothing on which combination finds more REAL defects; seeded-defect pilot never run
35. N-2 shadow is non-interference not quality; rests on LLM following prose; L2 key leaks
36. N-3 60 seeded defects (12 plans x 5) never planted or scored
37. N-4 single-vendor posture (A,B,C 9 of 15); no --allow-single-vendor in combo prompt; --env anthropic-only; gateway refused by resolver; gateway models reached via class aliases
38. N-5 dispatch collapse under tier3 vs tier1b: one verifiable; calibrator lost class in 5 of 12 tier1b runs; confounds (run order, concurrency of 5 at once, chance)
39. N-6 one input (TASK-WF-designSpec-20261107-075614, already landed); no run reviews a diff, spec alone, or PR
40. N-7 forced Tier 2 (--tier 2 pinned; 28 of 30 parsed-sparse); nothing learned about tier selection
41. N-8 no --t2-engine panel run
42. N-9 citation-resolution faults limit structural findings
43. N-10 no independent identity (requested-pinned 14/15)
44. N-11 statistical power (n=3; plan rule: 1-item gap, confidence gap < 0.10, 2/3 vs 1/3 not meaningful)
45. N-12 cost units (USD estimate; 65k kill line unit differs)
46. Thresholds T-1..T-10 and stop rule S-0..S-5: no approval record; merged-requirements.md draft-for-owner-review; only T-9 redefined by owner 2026-11-12; S-0 needs written owner approval before run 1; Stage 0 exit PENDING
47. Key Takeaways grading summary (strong / weak / moderate lists) and the two findings the slice did not carry (calibrator class loss, verify-citations resolved nothing)
48. Gaps G-1..G-9 (snapshot/--root cause untraced; pilot 6/9 irrecoverable; chained/unchained not read for correctness, E1 7 reviewer-agent calls unexplained; approval negative result; pilot tier decision not re-derived; slice figures not re-derived; token recount 3 logs only; drift of .dev/reflect; "no contract" correction)
49. Questions Q-1..Q-5 (build snapshot/root/card layout in code; record served model + calibrator without class an error; which ground truth; approve/redefine/drop stop rule and T-1..T-10; empty baseline = no baseline)
50. Stale docs: combos.json:4 "designed, not run"; FINDINGS.md:38 "all combinations"; FINDINGS.md:9/results.md only A3 collapsed; stage0a report and consumer inventory drift; slice 11 L95/L97 "no contract"
51. Summary: pipeline runs end to end, cost measured, Stage 2 exit fails 13 of 20, no quality measurement, design lessons from failures, E1 = evidence for what kernel must enforce in code

COUNT 07-e1-evidence-grading.md: 51

## File 3: research/08-e2-evidence-grading.md

1. Conventions and grade scale S3/S2/S1/S0; study tree extracted via git archive (9,312 files)
2. Pilot cells recomputed per package x arm table (designSpec/alias/design control; any, judge-blocking, real blocking, ledger rows, wrong blockers) and arm keys (blind arm assignment)
3. Pilot totals: any/16 A2 B3 C4; real blocking 0 in every arm; wrong blockers A0 B1 C3; defect-rich any/14 A1 B1 C2; equals PR:46-50
4. Control's "GT blocking" cells are judge-blocking (control GT has 0 blocking_in_implement): same judge-semantics flaw
5. Pilot "Wall s" column is a SUM of reviewer walls (2,355 s designSpec arm C), not elapsed; COMBO-REPORT elapsed is a different unit
6. Arms B and C excluded Qwen but kept luna slots; luna t4-2 reports quarantined; luna "refused without source.md (25/25 empty)" so arm C may have carried an empty luna reviewer [UNVERIFIED]; pilot arms pre-source.md era
7. Pilot takeaways: S3 arithmetic reproducible; S1 inference (n=3, 1 judge, decision rule "C passes exactly (2>=2x1)" rests on ONE defect GT7); panels B/C not nominal @default/@live7
8. combos/ count reconciliation: 96 dirs / 97 entries / 106 scored runs (3 pilot + 103 rows) / 319 score.json* blobs; "106 row folders" CODE-CONTRADICTED; "107 entries" UNVERIFIED
9. RESULT.md files 19 under combos/ vs 29 in the study (10 under quarantine)
10. Quarantine files 417 tracked (breakdown); "428 reviewer files" not a tracked-file count; "9 luna-bearing rows" vs 10
11. Qwen count: 3 timeouts of 4 Qwen runs; 4th finished at 2,913 s (97% of timeout), 93,701 output tokens; owner's disqualification basis
12. Counts takeaways: 428 and "107 entries" must not be carried
13. Alias numbering: B1..B8/I1..I8 legend mapping; per-issue found/credited counts over 106 runs (B3 95/26, B7 28/25, I2 71/33, I8 76/37 ...); never found B1,B2,I5,I6
14. Run-1 claim "alias GT3 found once" CODE-CONTRADICTED (GT3 twice; once-found is alias GT1 by b4-terra-luna-muse; B8 by g2-sonnet-ember-r3 and n2-muse-haiku-grok)
15. Concentration: 306 catches in 106 runs; control holds 92; B3+I2+B7 = 194 of 214 (91%); "/14" metric measures three easy defects
16. final-table.py/three-way.py re-run method (5 hard-coded paths patched) and hard-coded path list
17. final-table.py header (71 valid-era rows, 213 row-packages, 69 with EXCLUDE flag) and byte-identical final-table.md
18. three-way.py figures: sonnet+2x luna (n=6) 2.33/0.33/1.83/1.33/139,113/821 s; ember+2x luna 1.83/0.17/1.83/0.83/63,644/348 s; sonnet+luna+ember (n=5); h2 (n=4); permutation p values; reviewer-level luna dropped/nosrc 4/9 vs 1/1
19. fullpkg() bug in final-table.py (control package mapped to designSpec; 41/25/3 split); AUDIT-CLEAN table wrong; AS-SCORED unaffected; corrected clean table not recomputed
20. three-way.py:19 prints p[:8]=TASK-WF- (flagged package column unreadable)
21. Reproducibility takeaways: only after patching 5 paths; judge and reviewer sessions not reproducible (0 judge.json, 0 attempt json; raw transcripts not committed)
22. The unit behind 92/80/49: 92 findings dropped (all severities; by model luna 30, ember 33, wonder 14, glm 7, haiku 7, grok 1; by reason 56/18/14/3/1); 80 = reviewer-package runs with block ok false (raw 335 vs ledger 229 = 106 missing); 49 blocking (24/14/10/1; 44 reviewer-runs); per-model list is the 92 not the 49
23. 111/109 net findings missing by conservation: 17-19 dropped with no rule-based reason (haiku 23 net vs 7 explained); hypothesis D15 audit.py vs audit2.py
24. "Four verdict flips" CODE-CONTRADICTED: 3 flips (g3 alias, g5 alias, n5-sonnet-ember control); total-loss merges did not flip (verdict FAIL/REVISE with brief_ids)
25. "discarded with no error" CODE-CONTRADICTED: ledger.py:122-134 emits one first-error warning per reviewer; findings.py:90-121; true residue (no itemised list, 45 merges without merge-stdout.txt, merge exits 0); wording to use
26. "16 empty terra reviews" CODE-CONTRADICTED: 51 1-incomplete (sol 12, terra 26, haiku 11, luna 2); valid-era terra 14 + luna 2 = 16
27. Corrected sentence for the report ("merge dropped 92 findings (49 blocking) in 80 reviewer runs, flipping 3 verdicts, first-error warning")
28. Batch j1 (45 runs, in no audit): hand-audit (model_ok 45/45, no run under 1,000 tokens, no attempt>1, 2 of 15 merges luna block-ok-false, non-blocking, no flip); 2 luna INCOMPLETE refusals (j1-r2, j1-r4 designSpec t4-1); 2 legitimate empty-block PASS (j1-r1 t4-1, r5 t3-1)
29. j1 sensitivity table S0..S4 (found/14, real blocking/8, wrong blockers, control/2, tokens) and permutation p values
30. Control GT1 (I7) hits: sonnet-bearing 5/10 vs 0/11, Fisher p 0.0124 uncorrected (Bonferroni x16 = 0.20)
31. Decision: j1 unaudited does NOT invalidate "not confirmed"; "not confirmed" is a power statement; original 4/14 was an outlier (S2: j1 runs 2,1,3,2,2); new finding: 2 of 10 luna designSpec j1 runs refused because source.md names a requirements input missing from the sandbox; grade S2
32. G1 pilot arms graded S3 arithmetic / S1 as evidence
33. G2 ceiling: no valid-era row above 4/14; 43 of 71 at exactly 2/14; distribution 0:3,1:9,2:43,3:12,4:4; 147 defect-rich catches
34. G3 "/14" dominated by three defects (GT3 63 + GT7 50 + alias GT2 18 = 131 of 147, 89%); GT1, GT2, GT10, alias GT4 never caught
35. G4 judge-blocking overstates blocking: 65 vs 38 over 71 valid-era rows
36. G5 merge drop graded (92/49/80/3; S0 for "four flips", "no error", by-model attribution)
37. G6 source.md never referenced in 156 of 665 valid-era runs (per-model counts); S2, detection needs raw JSON
38. G7 refusals: 51 incomplete; valid-era 16 = 14 terra + 2 luna; luna anchor fidelity 91.4%
39. G8 replicated family means (n=4-6) S2, pseudo-replication on same 3 packages, 48 tests, perm p floor 0.029
40. G9 surviving significant effects (second luna raises control found +0.83 p 0.048; 2x luna + 2x ember +2.75-3.25 wrong blockers; ember+terra worse -1.75 p 0.029; 6 of 48 tests p<0.05)
41. G10 default ember + 2x luna (64k tokens, 1.83/14, 0.17 real blocking, control 0.83); ember skipped source.md in 9 of 18 runs, dropped 2 findings blocks; partly source-blind
42. G11 sonnet + 2x luna optional tier (control GT1 5/10 vs 0/11), S1 post hoc
43. G12 single-run leaders (grok+haiku+haiku+sonnet 4.00/14 594k tokens; haiku+sonnet+wonder 4.00) S1 anecdotes; sonnet+2x luna 4/14 outlier
44. G13 merge defects measured by audit: 195 of 1,398 multi-member rows are chains, 83 rows >=8 members or >=4 sections, 46 span-null rows (13 blocking); replay is a copy of findings.py logic
45. G14 model identity: 2 b4-muse-luna2 "wonder" runs served terra; gateway identity bleed under load; expected_model overwrite flaw (MODEL="$NEXT")
46. G15 blind-judge reliability (294 judge outputs clean; blind re-judge of 12 rows 12/12; 19/19 catches; GT8 borderline): S0, no artifact
47. G16 retracted/non-reusable claims (n2-sonnet-src 8/14, 5/8; "second run adds nothing"; "ember weaker than wonder"; ember x r2 composition; "0/8 blocking everywhere")
48. What the study does NOT show (9 points): no product-panel result; GT 16 defects in 3 packages (10/5, 4/3, 2/0) implementation-derived; no gate-accuracy measurement; no multi-round loop evidence; one judge; no audited-clean evidence; no dollar/input-token cost; reviewer isolation not auditable (25 X-sibling WARN); no test of the harness fixes
49. Audits A-F evidence table (ground truth sha256, 319 score blobs, judge sessions not committed 2,916 files 1.48 GB; audit A summary disagrees with flags.tsv: E2 54 vs 59, E11 1 vs 9, 930 vs 890 runs; B 51 flags; C runs.json 890; D recount; E no re-judge artifact, 294 = non-j1 rows; F fullpkg bug)
50. Takeaway: only audits A and D have summaries; E's re-judge weakest link
51. Gaps 1-8 (428 basis; 107 entries; 17-19 findings; re-judge and judge identity; pilot arm C composition; corrected AUDIT-CLEAN; CR:298 statistics; tokens columns and audit-A 57 vs 54)
52. Questions 9-10: should central design treat ember + 2x luna as evidence at all; is "NOT CONFIRMED" acceptable with 2 unaudited luna refusals
53. Stale docs: manifest.md:5 "never pushed"; COMBO-REPORT lines 1-288 retracted figures; CODE-CONTRADICTED list; PR:12 "all 3 slots timed out"
54. Summary: strong on counts, weak on inference; central design may rely on E2 for defect list (no silent drops, itemised rejects, refusals as status, source delivery, real vs judge blocking, identity checks) and as regression fixture, not for default model combination

COUNT 08-e2-evidence-grading.md: 54

## File 4: research/09-collaboration-designs.md

1. Method: slices re-derived against E2 tip blobs; MR line numbers = slice + 6; tag legend; pytest not run; H1-H4 naming note (harness fixes vs transport R-21/R-22/seal/board)
2. Slate F1/F4/F3/F6/F7 = r3/r2/r1/r5/r4; arms A0, A1, A2 (kit M1-M10), A3-A6, Stage 2 SL2 arms; F2/F5 evicted by distinctness rule; 25-proposal table unopened; transport tally (JSON board 17, between-phase 5, SendMessage 3, Orca mail 0, A2A 0); rejection table for Orca mail/A2A/cross-session at MR:245-253
3. Mechanism per package table (content exchanged, author, delivery for r1-r5)
4. Only F1 needs no hook; only F4/F7 need model-side write; panel-msg/1 envelope with three incompatible kinds (challenge/card/coverage + move/fact; C-07)
5. Shared hook skeleton (8 items: args baked R-21, exit 0 fail-open R-22, agent_id skip, flock counter, finish signal, no delivery before 6th call, seal + sha256 fail closed, exact JSON output) with line cites
6. Skeleton differences: r1 seals at checkpoint vs r2/r4/r5 before delivery (X8); r4 forgery check (post_accepted); lock scopes differ (r5 holds flock to exit, r4 separate delivery lock, r2 one critical section)
7. Takeaway: one shared hook library would replace four copies; parallel-tool-call race found by smoke runs in r2 and r4
8. E2 commit contents: file counts r1 107, r2 321, r3 130, r4 70, r5 274; zero /lib/ paths; .gitignore:13 lib/, :79 *.log
9. Tracked code depending on missing lib/ (r2 launch-panel.sh:6, receiver-hook.sh:10/85, r3 launch-panel.sh:5/55, r4 r4-hook:10); r2, r3, r4 (and r5 per IMPLEMENTATION.md) cannot run from the commit; r1 values/ and runs/ untracked (collab-1 launch exits 2)
10. runs/ absent for r3/r4/r5 so smoke rows not re-derivable beyond summary JSON
11. Claimed vs static test counts (138/103, 358/163, 89/89, 106/90, 108/82; parametrize 5/10/0/5/4); r5 last-run.txt "108 passed in 97.06s"; claims are self-reports
12. r1 measured rows: gate0.json (G-BASE, G-PINS, S0, S2 pass; S3 and Spike 4 missing); el2-c0-r0.json (107.105 s, 21,127 tokens, reask 1); collab-1 row provisional
13. r2 spikes/RESULTS.md (H3 FAIL then PASS; S0 p95 73/81 ms; S2 4 models; REQ-S3 probes; S3 FAIL x3 then "PASS" re-grading with no new model runs); six smoke rows (collab vs iso elapsed pairs; noise)
14. r3 smoke.jsonl 4 rows (A3 158.8 s twice, A1 95.2/154.8 s; tokens; control_found2 0; wrong blockers; phase2_timeout 1 in both A3); +30% cannot be read as design effect
15. r4 act-rates.json (haiku 0/0, sonnet 0.6/1, luna 0/0.4, ember 0/0; sessions 5,5,5,4); manifest.json base trees with empty first_commit; F7 gate "non-zero luna act rate" would block the arm
16. r5 results.jsonl 5 rows; kit alone +59% elapsed (281.567 vs 176.9175), +55% tokens (46,018 vs 29,655); NOTES.md REQ-S3 (sonnet 5/5, haiku 0/5, luna 1/5 and 3/5); Spike 4 pilot k 0 budget_ok false; diagnostic row proves chain delivered one card then hang guard
17. No design has measured effect on the 14 known defects (found_14 null/0); MR:1128 plan cannot detect central gain at n=12
18. Evidence-status takeaways (built partly, gate-0 partly passed, single smoke rows, no quality/cost)
19. Per-design requirement table (session persistence ON, per-session --settings, model-side write, --resume pass, extra model session, baseline timing, role map)
20. Direction-of-flow contradiction for strong model (r3 sends+receives, r4 sends only, r5 receives only): role must be per-use-case table
21. Nine capabilities the five designs demand of a core (headless runtime + hang guard + identity check + no fallback ladder; session persistence ON; hook points; resume; board path outside tree; seal; message-kind registry + forbidden keys; budget math Spike 4 never run; alarms + PANEL_COLLAB kill switch)
22. HEAD Tier-1 reflect child launched with --no-session-persistence (runner.py:503-505)
23. reflect-reviewer hosting limits (tools, model sonnet, maxTurns 50, permissionMode plan, no hooks key, "you do not coordinate", brief MUST NOT instruct to run anything); F4/F7 instructions not executable by no-Bash agent
24. Hosting by family: F4/F7 receiver only; F3/F6/F1 need delivery path; hook documentation says hooks fire for subagent calls but E2 hooks skip agent_id; additionalContext reaching a subagent UNVERIFIED
25. Radar classifier signatures M1/M2/M4/M7 are Bash patterns; Grep/Glob/codegraph reviewer leaves different trace
26. HEAD CLI Tier-2 swarm has no tool loop (openai_compat.py:384-388): no hook point, no session to resume; only between-phase exchange expressible
27. reflect --resume means skip launch when prior pass on HEAD (name collision with claude --resume)
28. create_review_snapshot (config.py:155-210), pinned off (models.py:94); plays role of H3/H4
29. Resolution (a): optional exchange capability with three implementations (between-phase, hook-delivered, Bash-authored board); F1 expressible everywhere but no clean measured success (phase2_timeout, --resume for gateway ids UNVERIFIED); reflect-reviewer can host only receiver-side delivery after unverified check
30. H1-H4 verdicts: H1 unconditional (name driving document by path and hash), H2 unconditional pre-merge normaliser, H3 conditional (per-module base rule), H4 principle unconditional list per module
31. Transport rules (R-21/R-22/seal/board) NOT unconditional; always-on pieces: session-persistence choice, transcript capture, fail-open, per-kind validators, kill switch byte-comparable (argv-diff test)
32. X1-X17 conflict table with class (E/E-partial/D/N) and evidence per row (X1 ember act rate N; X2 luna N; X3 finish signal D; X4 k E-partial; X5 turn measurement E; X6 gateway lock D; X7 session files D; X8 seal timing E; X9 thresholds D; X10 catalogue hash E; X11 origin tag E-partial; X12 smoke honesty E; X13 hand-off claims E; X14 contract shape D; X15 stale DESIGN status E; X16 planning numbers E (-7.67%, -33.25%); X17 Opus use D)
33. C-01..C-19 conflict table with class and evidence (C-01 H3 base D; C-02 origin placement D; C-03 hang-killed transcript E-partial; C-04 admission D; C-05 judge location D; C-06 direction N; C-07 schema kinds D; C-08 12-char rule vs exact-quote anchors E logic; C-09 re-ask without identity check E; C-10 k rounding E; C-11 r5 git add -A without -f E; C-12 cleanup D; C-13 only r5 builds A2 E-partial; C-14 act rate N; C-15 hook latency E; C-16 sealed judging D; C-17 reviewer ids D; C-18 orchestrator rule drift D; C-19 ledger outcome E)
34. Count: 36 conflicts = 13 E, 4 E-partial, 4 N, 15 D (members listed)
35. E2's own statement MR:917 static kit may beat every exchange design; MR:396 F3 share near 0; MR:909 A2 about +29% elapsed (UNVERIFIED); MR:1117 kit cost unmeasured
36. Conclusion: kit-beats-exchange neither confirmed nor refuted; core should ship harness fixes + per-module catalogue unconditionally, exchange optional behind kill switch, no hook transport in core until an exchange arm beats A2
37. Gaps 1-10 (no pytest; r2-r5 engines unreadable; unopened result rows; additionalContext to subagent; downstream consumers of origin key; H1-H4 naming ambiguity; which common act-rate probe; is exchange worth a core interface; brainstorm debate artifacts unopened; scratch cleanup)
38. Stale docs (r1/r2 DESIGN status; r2 IMPLEMENTATION lib/ listed built; r3/r4/r5 cited logs absent; slice 07 X2 "compatible" weakened; slice 05 line-number offset)
39. Summary

COUNT 09-collaboration-designs.md: 39

## File 5: research/10-process-redesign.md

1. Tag legend ([GIT-VERIFIED] etc.), MR2 = process-redesign merged-requirements.md (1254 lines)
2. U1 verify-citations: review-precheck/1, inputs, _check flags (missing-file, out-of-range, quote-not-found), _norm, per-citation single-file check, output precheck.json, docstring "drops nothing; the validator alone decides drops"; no demote/promote; reads coverage only to pass to parse_block
3. U1 takeaway: citation-quote part already implemented; flag set is a strict subset of MR2 REQ-14/16
4. U2 findings-v2: imports from v1; V1_FIELDS/ROLES/LENSES/CHANNELS/DEVIATION_CLASSES/REFLECT_CATEGORIES; rejects only calibrated_confidence (extra keys class/probe/src accepted); docstring accurate (retracted stale label, fix cycle 1); resolves slice-06 K6
5. U2 coverage_rows/coverage_context and empty-block rule (complete only if every assigned row observed); no per-row verdict, no quote per row, no probe key (grep = 0)
6. U3 two "ledgers": shipped review-ledger/1 (STATUSES, CLI group ledger with revise/defer/verdict/capture, brief line 70, tests) vs proposed ledger-v1 (per-reviewer row block; 0 occurrences in src/tests)
7. U3 naming convention: fence info strings <noun>-v<N> (findings-v1, fixmap-v1, findings-v2) vs persisted schemas review-<noun>/<N> (review-ledger/1, review-capture/1, review-precheck/1, review-panel-manifest/1, review-telemetry/1, review-panel/1, review-tiers/1, review-panel-resolution/1)
8. U3 resolution (a): core keeps review-ledger/1; E2 row block must be renamed (rows-v1, checks-v1, check-ledger-v1, sweep-rows); naming recommendation is DESIGN
9. U3 installed #346 variants sc-review-ledger, sc-spec-panel-stoprule-protocol, sc-diffgate not in src/superclaude/skills (word "ledger" used a third time)
10. U4 E1 coverage slice prose contract (reviewer-spec.md:61-74), grounding hunks, D13 spec-body hunk for qa persona
11. U4 row production: Wave 1B Step 1B.0 two-pass extraction (ID_REGEX, INF-NNN rows with verbatim quote + file:line, containment threshold 0.6), prose not Python; 12 grep files none in cli/review (matcher UNVERIFIED)
12. U4 assignment lands only as sidecar panel/coverage.json {reviewer-N:{assigned,observed}} read by cluster --coverage and verify-citations --coverage; no partition/ranking code in cli/review
13. U4 activation: coverage-sidecar/cluster/verify-citations flow dormant by default (--t2-engine legacy; shadow UC-1 only; UC-2 ignored until Stage 5)
14. U4 "observed" meaning (caller-supplied; only decides empty-block acceptance); Wave 1A evidence chain (search, codegraph_node, callers, impact, referrer Grep) is model-driven grounding for all reviewers
15. U4 takeaways: E1 has container + prose row producer for UC-1 but no producers for C1, C3-C8 and no per-row verdict; C8 reverse-dependency sweep partly present as Wave 1A chain
16. U5 seed-brief claims (seed-brief.md:26)
17. U5 class table C1-C8 (MR2:99-108), strength column (C1 symptom-level only, C2/C4/C5/C6/C8 General, C3 Weak, C7 broad general/narrow weak), X1-X7 at MR2:110
18. U5 class cards schema (id, name, version, definition, recipe_text <=120 words, question_template, extractor, route, replicas, applies_to, instances >=2, severity_guidance, known_weakness); block kinds "a checklist, not an interface"
19. U5 anti-overfitting AO-1..AO-8 (4-word-sequence lint, swap test, >=2 outside instances per card/>=3 per extractor except E6, extractors tested on >=3 unused plans, freeze by git tag before hold-out, ground truth never in sandbox, leave-one-class-out ablation <=15 points, no worked example from study packages)
20. U5 Sweep Sheet (S0-S6: deterministic pre-pass REQ-18, search scope, 15 s kill, extractors E1-E7, <=12 items, 24 slots = 12 x 2 of 3, caps ember 8 luna <=8, shuffle seed, script never writes a claim)
21. U5 Recipe Ledger (no pre-pass; lens of 2-4 class recipes per reviewer bound to MODEL NAMES; row budgets; no luna re-ask; ember re-ask only if now+30s <= 1.35 b; recipes R-C1..R-C8; R-C4 uses Bash, R-C8 git grep)
22. U5 tool-assumption conflict: recipes assume a shell; reflect-reviewer has no Bash (needs Grep/Glob/codegraph recipes or a script)
23. U5 launcher facts: run-reviewer.sh keeps first result message, tests only fence opener; "ledger in final message" is a study-launcher property; study directory does not exist at HEAD
24. U5 carrier ledger-v1 (MR2:268-297) and checks/promotion (MR2:300-319): demote linked finding of failed PROBLEM row; promote unlinked PROBLEM row as MINOR src=ledger
25. U5 gates G0 and D1-D7 (thresholds: 1.35 x Z0, p90 1.50, kills <=10%; D2 +0.12 with 90% bootstrap lower bound > Z0+0.04; D3 +3; D4 +1.0/+0.7; D5 0.40 on 3 of 5 classes; D6 within 0.10; D7 +0.04 vs checklist arm K); outcomes
26. U5 arithmetic: D2 0.12 x 14 = 1.68 items vs central shares +1.33 and +1.05 (0.095, 0.075): gate stricter than central case (K14); planning values; MR2:24 "All probabilities ... planning values"
27. U5 takeaways: E2 brainstorm design-only; two mechanisms in tension with HEAD (promotion writes a finding the reviewer did not write; quote_other can be a printed tool line which verify_cmd cannot check)
28. U6 answer: container and normaliser exist; producers, per-row verdict, demote/promote do not; building Sweep Sheet/Recipe Ledger as separate modules would duplicate the first two
29. U6 comparison table (8 rows: row producer, assignment container, observation, finding-to-row link probe=coverage_rows, quote normalisation identical, quote check overlap, effect of failed check, tool evidence); only C2 extractor E5 duplicates E1 Wave 1B
30. U6 negative-evidence searches (3) and takeaways (one capability for C2; avoid duplicating assignment and normalisation)
31. U7 spot-check of 10 .dev/reflect REPORT.md cites (10 exist, one classification doubt C6 vs C5), #346 evidence files (phase1/REPORT.md 314 lines, p17 ledger.json 1188 lines, p13 catalog 123 lines); .dev/tasks/done not opened; recurrence counts lower bounds
32. U7 decidability table (C1-C8, X1-X7, G0, G0 ledger_missing, D1-D7 with (M) mechanical and (R) re-readable and design-choice columns; C4 and C8 fully mechanical; C1, C3, C7, X3-X6 judgment; X7 weak)
33. U7 takeaways: gates are design choices no recorded run can evaluate; class list = evidence about one repo/owner, hold classes as module data not core constants
34. U8 seed claims vs code: Medium is outside the enum (brief lines 31-32); "no missing-task category" CODE-CONTRADICTED in part (missing-requirement exists; brief and schema disagree on blocking for it); "no severity levels" CODE-CONTRADICTED (SEVERITIES; brief gives no CRITICAL vs MAJOR definition; severity does not change verdict: _brief_ids/_decision; reflect severity coupling); "does not name any driving document" verified (placeholders list)
35. U8 corrected statement for the report; slice 06 line cites two lines off (findings.py:14, :15-22)
36. U8 takeaways: correct gap = no CRITICAL vs MAJOR definition, Medium outside enum, nothing names driving document, brief/schema disagree on blocking for missing-requirement; CB-2 interacts with brief lines 31-32 (REQ-05 unreconciled)
37. U9 destination table (19 ideas: H1 CORE brief builder; H2 CORE parser; H3/H4 CORE concept MODULE implements; CB-3 EXISTS; CB-2 HOLD; CB-5 CORE brief text; class cards CORE schema + MODULE files; container EXISTS; extractors E1-E7 per module; recipes/lens table closed slot keys; row block CORE optional renamed; quote tests extend precheck; demote/promote HOLD default off; telemetry keys counts-only; fallback EXISTS; blind verifier EXISTS; AO rules STUDY; gates STUDY; no reviewer messaging CORE principle)
38. U9 takeaways: core absorbs card schema, sidecar container, flat-based quote checks, optional renamed row block, H1/H2, telemetry restriction; not absorbed: promotion/demotion, study gates and arms, 326-run protocol
39. U10 recorded E1 sidecars: 13 coverage.json files, free-form row ids, range token, duplicates, 2 of 13 observed empty, 11 of 13 overlapping assignment
40. U10 precheck totals: shadow 275 checked/110 flagged (40.0%), combo 772/400 (51.8%), combined 1,047/510 (48.7%), 472 not-in-snapshot (92.5%), 7 out-of-range, 31 quote-not-found (3.0% of all); card block states 77 complete, 10 invalid (11.5%)
41. U10 reading: precheck mostly flags paths outside the snapshot; E2's 0.914 x 0.914 = 0.835 assumption has no comparable number; takeaway snapshot boundary matters more than quote exactness
42. U11 relation to collaboration brainstorm: ten issues -> moves M1-M10 and classes C1-C8; each move lands in exactly one class (M1->C8, M2->C6, M3->C1, M4->C4, M5->C2, M6->C3, M7->C5, M8->C7, M9->C1, M10->C6); class cards subsume move catalogue
43. Gaps 1-8 (seed claims resolved; docstring retraction; unread MR2 sections; recurrence counts; 12 Python files unread; --isolate-reviewers not code-read; open design questions Q1-Q9; negative searches)
44. Q1-Q9: findings container v2 vs v1; rename row block; demote/promote allowed?; where lens-to-reviewer binding lives; recipes for Grep/Glob/codegraph vs script; CB-2 vs Medium routing; telemetry counts only vs study log; +35% product vs study constraint; X1-X7 in first registry
45. Stale docs (seed-brief wrong as written; MR assumes findings-v1 and study launcher; slice 06 line cite; INV-004 vs REQ-45 wording; verify_cmd docstring OK)
46. Summary (a)-(d) and what core absorbs

COUNT 10-process-redesign.md: 46

## File 6: research/11-consumers-tasklist-workflow.md

1. Conventions; workflow-plan call = /sc:reflect --mode pre (UC-1); tasklist post gate = superclaude reflect run (UC-2 wrapper)
2. Workflow Wave 4 order (Wave 3 gate E-GATE, Wave 4 Reflect, Wave 5 contract) pinned by test_workflow_command.py:251-261 (exact call string, reflect_status/reflect_report_path in return-contract.md, call in _CMD)
3. Wave 4 advisory pre-check writes `## Pre-check` into artifacts/codegraph-grounding.md; never edits <id>.md or status
4. The one reflect call at :89 (defaults for every other flag incl. --t2-engine legacy; no --remediate); unattended variant :91 with nested/reflect-<n>/ pinned by test (:243-248)
5. Advisory rule :93; Will/Will Not :105/:107 (task fan-out is Will Not); return contract refs/return-contract.md:16-21 (contract 1.1, additive advisory keys); worker contract lists nested reflect files
6. No review loop/fix agent/cap in workflow; no superclaude review call and no --t2-engine in sc-workflow-protocol (8-file Grep)
7. Where a panel plugs at Wave 4: replaces/wraps :89; interface to keep (reflect_status, reflect_report_path, --unattended --output, never-edit rule, skipped|failed + null mapping); no new workflow hook if entering through reflect; --t2-engine panel rejected ("ships in Stage 3"); workflow-side change touches :89/:93 and test pins and plugin mirror
8. Five tasklist review mechanisms T1-T5 table (Stage 6 self-check 20 checks blocking pre-write; Stage 7 2N parallel Task agents, 5 dimensions, severity fields, some-vs-zero branch with synthetic-dnsp; Stages 8-10 patch loop with sc:task, 2-pass cap, halt strings, High+Medium blocking; Stage 10.5 pre-reflect sign-off; terminal Post-Execution Reflection task)
9. Advisory vs blocking: T1 and T3 blocking; Stage 10.5 advisory (bundle ships; "advisory-blocking" hybrid, one blocking edge = needs_human_decision HALT); T5 blocking per phase (exit 0 only); wording inconsistency "non-blocking" (:1640) vs "advisory-blocking" (:1646)
10. What a failing review does: Stage 10.5 changes no phase file, writes index "Pre-Reflect Sign-off" column and reflect_pre_summary {pass,partial,fail}; failing Stage 7-10 changes files only through sc:task
11. Stage 10.5 anatomy: runs after P2 loop (Non-overlap invariant R-8, pinned by test_tasklist_cli.py:573-580); one agent per phase file; call syntax with --remediate --depth --tier --output; no --t2-engine so legacy
12. Depth input COMPLEXITY_SCORE formula (3*n_strict + 3*n_cpo + 2*n_high_risk + ceil(n_tasks/5) + ceil(n_R/5)); mapping 0-3 quick tier 1, 4-9 standard auto, 10+ deep tier 2; override n_cpo>=1 or n_strict>=2; n_tasks==0 skips; audit file validation/reflect-pre/depth-map.yaml; quick phase never reads --t2-engine (rule D1)
13. Skip flags --no-reflect/--dry-run; outputs the panel must keep or alias: per-phase reflect_pre PASS|PARTIAL|FAIL (depth, coverage) index column, reflect_pre_summary, directories validation/reflect-pre/phase-<P>/ or nested/reflect-<n>/
14. Call replaced is :1630; tasklist-side alternative (replace T2+T3 by one panel with five Stage 7 dimensions as lenses) is a larger separate change; T3's 2-pass cap vs 3-review cap
15. T5 per-phase post gate: appended when reflect gating on; Tier EXEMPT; recursion breaker SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE; command (--depth deep --fix --no-promote --base <PHASE_N_START_SHA>); executor class from frontmatter
16. T5 pass rule: exit 0 only; also fail at exit 0 if reflect_post.verdict not pass, subrun partial/failed, tier_reached 2 with convergence < 0.80, or drift/regression > 0
17. T5 does not go through SKILL prose engine (runner.py:456 builds /sc:reflect --mode post; Tier 2 = in-process swarm; no --t2-engine); plug-in point is a different code path from Stage 10.5/Wave 4; outside UC-1 and shadow
18. superclaude tasklist validate: files, one step tasklist-fidelity, one reviewer (600 s, retry_limit 1), gate high_severity_count==0, exits 1 on HIGH, missing/unparseable count = failure; no loop/fix/diversity; mentioned once in skill as example (SKILL.md:226); sixth review shape with own vocabulary; prompts.py has no panel call
19. Section 2 takeaways: advisory at Stage 10.5; blocking at Stage 6, 8-10, T5, tasklist validate; Stage 10.5 skill-level UC-1 panel-capable vs T5 CLI wrapper no panel; no consumer passes --t2-engine so no run reaches panel code
20. Reflect UC-1: flags :75-98; mode rule 1 literal; waves 0-7; UC-1 outputs (status values, coverage_pct, tier_reached), partial examples (zero-task, validator unavailable, dropped citations, all T2 reviewers failing); UC-1 verdict citing zero files legitimate
21. Panel state in UC-1: legacy default, panel rejected, shadow (UC-1 only Stage 2; outputs under <output>/panel/); UC-2 flag ignored until Stage 5; panel called only after final tier is 2; rules D1-D5 (N_eff = min(--reviewers, alias count, 3)); ten shadow steps; legacy writers keep contract 1.8.0
22. Consequence: consumers always take legacy path; panel reachable only via manual --t2-engine shadow; commands/reflect.md has 0 matches for t2-engine
23. Skill edit fence tests (test_shadow_skill_contract.py:42-49, :52-75 allow-list 3.1/4.3a/5.4/9.2, :78-98 no new src/superclaude strings): bind only uncommitted edits; moving panel from shadow to engine panel must edit outside allow-list and update test
24. Executor-disjoint/reviewer-pool rules reflect supplies: Stage 10.5 passes no --executor-model; post gate from frontmatter; §7.1 pool exclusion (below N=2 degrades to T1 with executor_exclusion_degraded, executor_class_source, fail-open when unknown, default rotation); wrapper passes executor_model only to Tier-1 prompt
25. Section 3 takeaways (one flag set; panel only as shadow; contract stays 1.8.0 with panel fields nested under telemetry:)
26. 36-test matrix: docstring, count 36, test_runner_e2e adds 10 end-to-end tests, 25 YAML fixtures (pass.yaml contract_version 1.3.0 ...)
27. Verdict triggers table (BLOCKED/DEGRADED/HALTED/PASS lists with code lines and test names)
28. Constraint the matrix puts on a panel: panel-produced contract must carry the keys with same meaning (convergence >= 0.80, merge_method, diversity values, bool types); panel replacing adversarial merge needs defined meaning of adversarial_convergence_score and merge_method or derive_verdict degrades (inference)
29. Wrapper gate stricter than skill prose (0.75 vs 0.80; T5 and matrix use 0.80); matrix does not test UC-1 (runner builds only --mode post; reflect_verdict_replay.py replays pre-* 1.8.0 contracts offline)
30. Code-driven Tier 2 independent of skill's panel (runner.py:538-545; ensemble emits 1.0; any major 1 accepted); contract.py never reads merged-verdict.yaml/reviewer_cards/evidence_validator_ran: EV-1 is prompt-level + panel_lint
31. Section 4 takeaways (36 tests pin UC-2 map; a panel behind reflect run must emit same fields or T5 degrades; any change = pinned test + T5 acceptance bullets :1171/:1179)
32. DO4 as stated by E2 (HANDOFF line 301 decider "Owner plus the unification session"; line 406; U11 line 436 Must; Q7 line 457); cross-check at HEAD (E2 cites base-branch line numbers :60/:76; HEAD :89/:105; :1630 exact)
33. DO4 options mapped: (1) keep: panel enters through reflect Tier 2 and call sites unchanged; (2) move: replace :89 and :1630 with a direct panel kind needing new flag set, new contract keys beside reflect_status, rewrites of test pins
34. "Reaches no reflect panel" claim: run-1 D14 "No tasklist review step exists" CODE-CONTRADICTED (both call reflect UC-1); narrower fact (no superclaude review / review ledger / spec-panel loop) verified; third reading "reaches the panel" false (--t2-engine legacy)
35. Other readers of reflect_* keys: return-contract.md:16-21 pinned by test_workflow_vs_task_builder_companion.py:574-599 (closed enum, skipped only with null path); sc-troubleshoot refs; sc-auggie-review SKILL:348; reflect refs/remediation-handoff (reuses Wave 4 result; self-review fallback); no Python reads reflect_status; reflect SKILL §9.3 consumer map
36. Plugin mirror reach: plugins hold confidence-check, sc-implement-protocol, sc-recommend, sc-workflow-protocol only; no sc-reflect-protocol/sc-tasklist-protocol; commands/reflect.md differs; consequence: plugin Wave 4 ends skipped|failed (inference)
37. Section 5 takeaways (DO4/U11 correct; run-1 claim split; reflect_status enum is stable interface)
38. Gaps 1-5 (tier chosen by rubric for standard auto; --no-reflect practice; §9.3 sprint readers; fence test on clean tree; slice 10 numbers) and questions 6-8 (DO4 owner decision; should T5 be in panel scope; tasklist validate absorbed?) and negative evidence 9
39. Stale docs: §9.3 sc:tasklist generator gate row (coverage_undefined etc. absent); cli/reflect/__init__.py; runner.py:457 comment vs Click default; E2 line cites; run-1 D14; wording inconsistency; 0.75 vs 0.80
40. Summary

COUNT 11-consumers-tasklist-workflow.md: 40

## File 7: research/21-value-ledger-brainstorms.md (one entry per ledger row; format: n. id | ledger dest -> inventory dest | status | statement head)

1. VL-21-001 | KNOWLEDGE -> KNOWLEDGE | REPRESENTED same-dest | E2 brainstorm identity (S1.1): topic "reviewer models communicate and collaborate DURING t
2. VL-21-002 | KNOWLEDGE -> KNOWLEDGE | REPRESENTED same-dest | Dialogue ran non-interactive (S1.2): Clarify/Validate/Probe answers came from the owner re
3. VL-21-003 | HARNESS -> HARNESS | REPRESENTED same-dest | launch-variants.sh (S1.3) runs 5 headless `claude -p` sessions in parallel (timeout 3000, 
4. VL-21-004 | KNOWLEDGE -> KNOWLEDGE | REPRESENTED same-dest | Owner decision 2026-11-13 (S1.3): each proposal runs in its own session with its own budge
5. VL-21-005 | KNOWLEDGE -> KNOWLEDGE | REPRESENTED same-dest | Variant prompt schema (S1.4) has 5 sections: theories; five redesigns with 8 elements (a-h
6. VL-21-006 | EVAL -> EVAL | REPRESENTED same-dest | Variant rule (S1.4): hints exchanged must be generic investigative moves, never issue-spec
7. VL-21-007 | KNOWLEDGE -> KNOWLEDGE | REPRESENTED same-dest | Variant session wall times in seconds (S1.5): v1 630, v2 839, v3 538, v4 659, v5 910
8. VL-21-008 | KNOWLEDGE -> KNOWLEDGE | REPRESENTED same-dest | Debate session 1 (S1.6: `/sc:adversarial --compare 5 files --depth deep --convergence 0.75
9. VL-21-009 | KNOWLEDGE -> KNOWLEDGE | REPRESENTED same-dest | Debate resumed from on-disk artifacts (S1.7; timeout 7200, wall 3262 s); rounds 1, 2, 2.5 
10. VL-21-010 | KNOWLEDGE -> KNOWLEDGE | REPRESENTED same-dest | Merge instruction (S1.8): keep 5-section structure, end with exactly FIVE distinct redesig
11. VL-21-011 | KNOWLEDGE -> KNOWLEDGE | REPRESENTED same-dest | Orchestrator deviation 1 (S1.9): token-budget gate (Wave 2B) not applied as one budget, pe
12. VL-21-012 | KNOWLEDGE -> KNOWLEDGE | REPRESENTED same-dest | Orchestrator deviation 2 (S1.10): resume chosen instead of the F1 quick 3-proposal retry, 
13. VL-21-013 | KNOWLEDGE -> KNOWLEDGE | REPRESENTED same-dest | Enrichment tiers (S1.11): codebase primary (3 parallel investigation agents), research-lig
14. VL-21-014 | KNOWLEDGE -> KNOWLEDGE | REPRESENTED same-dest | Top-level contract (S1.12): status success, convergence_score 1.0, proposal_count 5, hando
15. VL-21-015 | KNOWLEDGE -> KNOWLEDGE | REPRESENTED same-dest | Adversarial contract (S1.13): base opus:devops won 0.978 vs 0.946 (V5) and 0.945 (V1), mar
16. VL-21-016 | CORE -> CORE | REPRESENTED same-dest | Return contract stores ABSOLUTE worktree-specific paths (`/home/coder/workspaces/worktrees
17. VL-21-017 | KNOWLEDGE -> KNOWLEDGE | REPRESENTED same-dest | Worker contract (S1.14: worker_contract_version "1", worker_status succeeded) lists 41 art
18. VL-21-018 | EVAL -> EVAL | REPRESENTED same-dest | Resume reply (S1.15a) admits some gain numbers are estimates the merge chose, not figures 
19. VL-21-019 | EVAL -> EVAL | REPRESENTED same-dest | Coverage Deflection gain re-estimated 0.07-0.53 (1 message) and 0.13-1.06 (2 messages) on 
20. VL-21-020 | KNOWLEDGE -> KNOWLEDGE | REPRESENTED same-dest | Merge adapted three details (S1.15c): one move numbered M8 instead of M7; M2 and M4 given 
21. VL-21-021 | KNOWLEDGE -> KNOWLEDGE | REPRESENTED same-dest | Debate-resume stderr (S1.16) shows two `unrecognized_model` notices (`claude-gw-tier2[1m]`
22. VL-21-022 | HARNESS -> HARNESS | REPRESENTED same-dest | launch-*.sh hardcode REPO=`/home/coder/workspaces/worktrees/IronClaude/eval-tasklist-revie
23. VL-21-023 | EVAL -> EVAL | REPRESENTED same-dest | Brainstorm variants ran on Claude models only (S1.18: opus-5-5, haiku-5-5, sonnet-5-5) whi
24. VL-21-024 | KNOWLEDGE -> KNOWLEDGE | REPRESENTED same-dest | merged-requirements.md (1130 lines) is the merged spec (1124 lines) plus a 6-line front-ma
25. VL-21-025 | EVAL -> EVAL | REPRESENTED same-dest | Problem (S2.1): reviewers run in isolation and a deterministic script merges afterwards; o
26. VL-21-026 | EVAL -> EVAL | REPRESENTED same-dest | Evidence base (S2.2): `.dev/eval-workspaces/tasklist-review-panel/20261111-a1/` (COMBO-REP
27. VL-21-027 | EVAL -> EVAL | REPRESENTED same-dest | Never found by cheap panels (S2.3): B1, B2, B5, B6, B8, I1, I4, I5, I6, I7 over sets S01, 
28. VL-21-028 | EVAL -> EVAL | REPRESENTED same-dest | Easy issues (S2.4): B3 found in 68 of 76 runs, I8 in 56, I2 in 52
29. VL-21-029 | CORE -> CORE | REPRESENTED same-dest | Harness defect (S2.5): the merge drops findings with anchors over 200 or claims over 300 c
30. VL-21-030 | MODULE-tasklist -> MODULE-tasklist | REPRESENTED same-dest | Harness defect (S2.5): 156 of 665 runs never opened source.md
31. VL-21-031 | CORE -> CORE | REPRESENTED same-dest | Harness defect (S2.5): terra and sol often return empty reviews
32. VL-21-032 | EVAL -> EVAL | REPRESENTED same-dest | Timing baselines (S2.6): ember + 2x luna about 348 s, ember + luna 300 s, haiku + 2x luna 
33. VL-21-033 | CORE -> CORE | REPRESENTED same-dest | Reviewer runtime (S2.7): headless `claude -p --model <raw gateway id>` via `tools/run-revi
34. VL-21-034 | MODULE-tasklist -> MODULE-tasklist | REPRESENTED same-dest | Constraint (S2.8): panel elapsed time at most +35% versus the isolated baseline
35. VL-21-035 | MODULE-tasklist -> MODULE-tasklist | REPRESENTED same-dest | Constraint (S2.8): evaluate transports Orca agent mail, Claude Code SendMessage/teams, A2A
36. VL-21-036 | MODULE-tasklist -> MODULE-tasklist | REPRESENTED same-dest | Constraint (S2.8): each redesign states when and how often agents communicate and shows co
37. VL-21-037 | EVAL -> EVAL | REPRESENTED same-dest | Constraint (S2.8): gain estimates are grounded in study data
38. VL-21-038 | CORE -> CORE | REPRESENTED same-dest | Constraint (S2.8): reviewers are read-only, none sees ground truth, and the findings-v1 co
39. VL-21-039 | CORE -> CORE | REPRESENTED same-dest | Constraint (S2.8): model roster is ember, luna, haiku (cheap core), sonnet, grok; Qwen and
40. VL-21-040 | KNOWLEDGE -> KNOWLEDGE | REPRESENTED same-dest | Success criterion (S2.9): five distinct redesigns, each with schedule, transport, time ari
41. VL-21-041 | KNOWLEDGE -> KNOWLEDGE | REPRESENTED same-dest | Success criterion (S2.9): three evidence-based theories, each redesign mapping to at least
42. VL-21-042 | EVAL -> EVAL | REPRESENTED same-dest | Success criterion (S2.9): a recommended first experiment runnable on the existing three pa
43. VL-21-043 | EVAL -> EVAL | REPRESENTED same-dest | Open question Q1 (S2.10): do missed issues need cross-document reasoning (plan vs source.m
44. VL-21-044 | HARNESS -> HARNESS | REPRESENTED same-dest | Open question Q2 (S2.11): can headless `claude -p` gateway sessions poll a file or mailbox
45. VL-21-045 | EVAL -> EVAL | REPRESENTED same-dest | Open question Q3 (S2.12): is a mid-run message more valuable as a challenge ("prove Task 1
46. VL-21-046 | EVAL -> EVAL | REPRESENTED same-dest | Open question Q4 (S2.13): how much does fixing the harness (source.md named, anchor limit)
47. VL-21-047 | KNOWLEDGE -> KNOWLEDGE | REPRESENTED same-dest | Model profile (S2.14) ember: 41 s wall, 7.1k thinking tokens, greps lines the plan cites, 
48. VL-21-048 | KNOWLEDGE -> KNOWLEDGE | REPRESENTED same-dest | Model profile (S2.14) luna: 102 s, 3.6k thinking, reads named files whole, searches tests/
49. VL-21-049 | KNOWLEDGE -> KNOWLEDGE | REPRESENTED same-dest | Model profile (S2.14) haiku: 233 s, 45.8k thinking, searches tests/ in 81% of runs but onl
50. VL-21-050 | KNOWLEDGE -> KNOWLEDGE | REPRESENTED same-dest | Model profile (S2.14) sonnet: 228 s, 22.9k thinking, greps the whole repo, 3.1 unnamed fil
51. VL-21-051 | KNOWLEDGE -> KNOWLEDGE | REPRESENTED same-dest | Model profile (S2.14) grok: 790 s, 48.5k thinking, saw CHANGELOG.md:166 (GT10) and dropped
52. VL-21-052 | KNOWLEDGE -> KNOWLEDGE | REPRESENTED same-dest | Thinking tokens track issues found across models (S2.15): Spearman 0.64
53. VL-21-053 | DROP -> DROP | REPRESENTED same-dest | Seed claim (S2.15): "within every model the higher-thinking half finds more"
54. VL-21-054 | KNOWLEDGE -> KNOWLEDGE | REPRESENTED same-dest | Transport (S2.18): Orca agent mail rejected because bash-launched reviewers have no mailbo
55. VL-21-055 | HARNESS -> HARNESS | REPRESENTED same-dest | Transport (S2.18): Claude Code cross-session messaging is "possible; UNVERIFIED": arrival 
56. VL-21-056 | KNOWLEDGE -> KNOWLEDGE | REPRESENTED same-dest | Transport (S2.18): A2A rejected (no way to inject into a running turn, one server per revi
57. VL-21-057 | MODULE-tasklist -> CORE | REPRESENTED moved(documented) | Transport (S2.18): JSON board plus PostToolUse hook `additionalContext` plus Stop hook, "a
58. VL-21-058 | MODULE-tasklist -> CORE | REPRESENTED moved(documented) | Transport (S2.18): between phases, use a harness digest or `claude -p --resume <session_id
59. VL-21-059 | KNOWLEDGE -> KNOWLEDGE | REPRESENTED same-dest | Time facts (S2.19): panel elapsed equals the slowest reviewer; +35% on ember + 2x luna is 
60. VL-21-060 | EVAL -> EVAL | REPRESENTED same-dest | Confounds (S2.20): 200/300-char merge drop (49 blocking lost), source.md not named (156 of
61. VL-21-061 | EVAL -> EVAL | REPRESENTED same-dest | Rule (S2.20): a redesign's gain estimate must state which part is collaboration and which 
62. VL-21-062 | KNOWLEDGE -> KNOWLEDGE | REPRESENTED same-dest | Merged-spec title and path aliases (S3.1): EVAL, BS, CR, HO2, RR aliases for the eval work
63. VL-21-063 | EVAL -> EVAL | REPRESENTED same-dest | Issue-label key (S3.2): B1-B5 and I1-I5 are designSpec GT1-GT10 (GT6 = I1); B6-B8 and I6 a
64. VL-21-064 | MODULE-tasklist -> MODULE-tasklist | REPRESENTED same-dest | Devops framing (S3.3): each redesign is a change to a running service with elapsed target 
65. VL-21-065 | MODULE-tasklist -> MODULE-tasklist | REPRESENTED same-dest | Devops framing (S3.3): one-setting kill switch (R-05)
66. VL-21-066 | CORE -> CORE | REPRESENTED same-dest | Devops framing (S3.3): audit trail, every message is logged
67. VL-21-067 | EVAL -> EVAL | REPRESENTED same-dest | Devops framing (S3.3): named alarms per failure mode
68. VL-21-068 | MODULE-tasklist -> MODULE-tasklist | REPRESENTED same-dest | Devops framing (S3.3): runbook entries per failure mode
69. VL-21-069 | EVAL -> EVAL | REPRESENTED same-dest | Slate (S3.4): Slot 1 F1 between-phase cross-examination = Redesign 3 Axis-Flip Challenge; 
70. VL-21-070 | EVAL -> EVAL | REPRESENTED same-dest | Experiment arm A0 (S3.5): ember + 2x luna on today's harness fresh (no fixes)
71. VL-21-071 | EVAL -> EVAL | REPRESENTED same-dest | Experiment arm A1 (S3.5): A0 plus harness fixes H1-H4, the isolated baseline (the base doc
72. VL-21-072 | EVAL -> EVAL | REPRESENTED same-dest | Experiment arm A2 (S3.5): A1 plus the static move kit M1-M10 in every brief, no communicat
73. VL-21-073 | EVAL -> EVAL | REPRESENTED same-dest | Experiment arm A3 (S3.5): Redesign 3 (F1), between-phase cross-examination
74. VL-21-074 | EVAL -> EVAL | REPRESENTED same-dest | Experiment arm A4 (S3.5): Redesign 2 (F4), searcher-to-reader fact relay
75. VL-21-075 | EVAL -> EVAL | REPRESENTED same-dest | Experiment arm A5 (S3.5): Redesign 4 (F7), directed challenge
76. VL-21-076 | EVAL -> EVAL | REPRESENTED same-dest | Experiment arm A6 (S3.5): Redesign 1 (F3), content-free coverage steering
77. VL-21-077 | EVAL -> EVAL | REPRESENTED same-dest | Stage 2 arms (S3.5): A1-SL2, A2-SL2, F6-SL2 (Redesign 5) on sonnet + 2x luna
78. VL-21-078 | EVAL -> EVAL | REPRESENTED same-dest | Symbols (S3.6): B baseline (EL2 116 s, HL2 238 s, SL2 273.7 s = CR 3-package elapsed divid
79. VL-21-079 | EVAL -> EVAL | REPRESENTED same-dest | Three-share rule (S3.7, merged-spec 68, 326-334): H, P and C are always reported in separa
80. VL-21-080 | EVAL -> EVAL | REPRESENTED same-dest | "C is conditional on H" (S3.7): every collaboration estimate assumes H applied in both arm
81. VL-21-081 | EVAL -> EVAL | REPRESENTED same-dest | Theory T1 refined (S3.8): the missing capability has two halves in different cheap models,
82. VL-21-082 | EVAL -> EVAL | REPRESENTED same-dest | T1 evidence (S3.8): unnamed files per run sonnet 3.1, grok 1.2, haiku 0.9, ember 0.8, luna
83. VL-21-083 | EVAL -> EVAL | REPRESENTED same-dest | T1 evidence (S3.8): `tests/skills/test_worker_contract.py` opened in 0 of 176 ember/luna/h
84. VL-21-084 | EVAL -> EVAL | REPRESENTED same-dest | T1 evidence (S3.8): haiku 5.2 recursive searches/run, 5 of 11 cheap control runs had the c
85. VL-21-085 | EVAL -> EVAL | REPRESENTED same-dest | T1 evidence (S3.8): CHANGELOG.md touched by 1 of 233 designSpec runs; 44 of 98 cheap alias
86. VL-21-086 | EVAL -> EVAL | REPRESENTED same-dest | Theory T2 refined (S3.9): NOT a thinking-budget ceiling: ember hard-issue hits 0.25 to 0.2
87. VL-21-087 | EVAL -> EVAL | REPRESENTED same-dest | T2a "right place, one question" (S3.9; B5, I1, I5, B6 framing): 16 cheap findings anchor t
88. VL-21-088 | EVAL -> EVAL | REPRESENTED same-dest | T2b "region never reached" (S3.9; B1, B2, I4, I6): ember anchors Task 1 in 52% of designSp
89. VL-21-089 | HARNESS -> HARNESS | REPRESENTED same-dest | T3(a) cannot see (S3.10): the sandbox is a post-implementation checkout with repairs (refs
90. VL-21-090 | EVAL -> EVAL | REPRESENTED same-dest | T3(a) (S3.10): 14 of 39 ember designSpec reports never opened source.md (investigation-des
91. VL-21-091 | CORE -> CORE | REPRESENTED same-dest | T3(b) seen and dropped (S3.10): a missing requirement is graded Medium and the findings ca
92. VL-21-092 | EVAL -> EVAL | REPRESENTED same-dest | T3(b) (S3.10): all 7 true I7 findings were non-blocking, grok dropped CHANGELOG.md:166 as 
93. VL-21-093 | DROP -> DROP | REPRESENTED same-dest | T3(b) merge drop (S3.10): long anchors/claims dropped, 49 blocking findings lost (luna 30,
94. VL-21-094 | EVAL -> EVAL | REPRESENTED same-dest | T3 leak (S3.10): `.dev/reflect/pre-design-20261108041729/REPORT.md` names I7, and 2 of 9 I
95. VL-21-095 | EVAL -> EVAL | REPRESENTED same-dest | Gate funnel (S3.11): three gates, exposure, question, survival; each hard issue fails at a
96. VL-21-096 | EVAL -> EVAL | REPRESENTED same-dest | "The survival gate is closed only by the harness fixes H1-H4, never by collaboration" (S3.
97. VL-21-097 | EVAL -> EVAL | REPRESENTED same-dest | B1 (S3.11, S3.12): fails exposure at AC3/O3 (Task 1 anchored in 52% ember and 92% haiku de
98. VL-21-098 | EVAL -> EVAL | REPRESENTED same-dest | B2 (S3.11, S3.12): needs source.md:341; theory T2b/T3a; move M9 scope compare; targeted by
99. VL-21-099 | EVAL -> EVAL | REPRESENTED same-dest | B5 (S3.11, S3.12): passes exposure (3 findings; needs source.md:112), fails question, fail
100. VL-21-100 | EVAL -> EVAL | REPRESENTED same-dest | B6 (S3.11, S3.12): theory T1/T2a; move M10 claim against enforcing test; targeted by F4, F
101. VL-21-101 | EVAL -> EVAL | REPRESENTED same-dest | B8 (S3.11, S3.12): theory T1/T3a; move M2 universal-claim count; targeted by F4 (count fac
102. VL-21-102 | EVAL -> EVAL | REPRESENTED same-dest | I1 (S3.11, S3.12): needs the source.md:200 versus :206 table pair; theory T2a/T3a; move M6
103. VL-21-103 | EVAL -> EVAL | REPRESENTED same-dest | I4 (S3.11, S3.12): 0 cheap findings on Task 12 AC1; theory T2b/T3a; move M4 literal AC che
104. VL-21-104 | EVAL -> EVAL | REPRESENTED same-dest | I5 (S3.11, S3.12): CHANGELOG touched in 1 of 233 runs; theory T1/(T2a,T3b); move M7 other-
105. VL-21-105 | EVAL -> EVAL | REPRESENTED same-dest | I6 (S3.11, S3.12): theory T2b; move M8 constraint sweep across tasks; targeted by F1 (`con
106. VL-21-106 | EVAL -> EVAL | REPRESENTED same-dest | I7 (S3.11, S3.12): theory T1/(T3b, leak); move M1 reverse-dependency sweep; targeted by F4
107. VL-21-107 | MODULE-tasklist -> MODULE-tasklist | REPRESENTED same-dest | Move M1 (S3.13): reverse-dependency sweep; observable as a recursive grep over `tests/` wi
108. VL-21-108 | MODULE-tasklist -> MODULE-tasklist | REPRESENTED same-dest | Move M2 (S3.13): universal-claim count; observable as a listing or count across a director
109. VL-21-109 | MODULE-tasklist -> MODULE-tasklist | REPRESENTED same-dest | Move M3 (S3.13): stopping rule (state the finite check that proves it); unobservable; c ce
110. VL-21-110 | MODULE-tasklist -> MODULE-tasklist | REPRESENTED same-dest | Move M4 (S3.13): literal acceptance-criterion check; observable as a grep whose pattern eq
111. VL-21-111 | MODULE-tasklist -> MODULE-tasklist | REPRESENTED same-dest | Move M5 (S3.13): branch trace (what does the mapping return after each halt reason); unobs
112. VL-21-112 | MODULE-tasklist -> MODULE-tasklist | REPRESENTED same-dest | Move M6 (S3.13): producer/consumer pair check against source.md; unobservable; c ceiling 0
113. VL-21-113 | MODULE-tasklist -> MODULE-tasklist | REPRESENTED same-dest | Move M7 (S3.13): other-direction sweep; observable as a repo-wide search including root fi
114. VL-21-114 | MODULE-tasklist -> MODULE-tasklist | REPRESENTED same-dest | Move M8 (S3.13): constraint sweep across tasks; unobservable; c ceiling 0.140 (G8, shared 
115. VL-21-115 | MODULE-tasklist -> MODULE-tasklist | REPRESENTED same-dest | Move M9 (S3.13): scope compare; unobservable; c ceiling 0.050 (G2)
116. VL-21-116 | MODULE-tasklist -> MODULE-tasklist | REPRESENTED same-dest | Move M10 (S3.13): claim checked against its enforcing test; unobservable; no c ceiling
117. VL-21-117 | MODULE-tasklist -> MODULE-tasklist | REPRESENTED same-dest | Two observable non-move checks (S3.13): source.md opened; an unnamed test file opened
118. VL-21-118 | EVAL -> EVAL | REPRESENTED same-dest | c-ceiling semantics (S3.14): c is V5's chance that a cheap model which does the move on th
119. VL-21-119 | EVAL -> EVAL | REPRESENTED same-dest | Several gain-row highs exceed c (S3.14): F3 B5 0.15 vs M5 0.125; I1 0.10 vs M6 0.075; F7 B
120. VL-21-120 | EVAL -> EVAL | REPRESENTED same-dest | "Every gain row is a planning value and is replaced by the arm's measured reach" (S3.14)
121. VL-21-121 | EVAL -> EVAL | REPRESENTED same-dest | For never-found issues (B1, B2, I5, I6) no cheap-model rate exists; the low end is 0 when 
122. VL-21-122 | MODULE-tasklist -> CORE | REPRESENTED moved(documented) | Message schema panel-msg/1 (S3.15): one JSON object per line, at most 600 bytes, reader re
123. VL-21-123 | MODULE-tasklist -> CORE | REPRESENTED moved(documented) | panel-msg/1 fields (S3.15): v, id, run, from, to, t, kind (move/fact/challenge/card/covera
124. VL-21-124 | MODULE-tasklist -> CORE | REPRESENTED moved(documented) | panel-msg/1 forbidden keys (S3.15): claim, verdict, blocking, severity, category, note, an
125. VL-21-125 | MODULE-tasklist -> MODULE-tasklist | REPRESENTED same-dest | panel-msg/1 exception and cap (S3.15): only F7 `kind:"card"` posted by ember may carry `ca
126. VL-21-126 | MODULE-tasklist -> CORE | REPRESENTED moved(documented) | Board substrate (S3.16): `$BOARD/<row>/<pkg>/` outside the sandbox repo; model-authored li
127. VL-21-127 | MODULE-tasklist -> CORE | REPRESENTED moved(documented) | Delivery (S3.16): a `PostToolUse` hook prints new peer lines as `additionalContext` of at 
128. VL-21-128 | MODULE-tasklist -> CORE | REPRESENTED moved(documented) | Hook configuration (S3.16): hooks passed per reviewer via `--settings '<json>'` with the a
129. VL-21-129 | KNOWLEDGE -> KNOWLEDGE | REPRESENTED same-dest | Board rationale (S3.16): chosen because delivery is CLI-side, durable, gives an audit log,
130. VL-21-130 | MODULE-tasklist -> CORE | REPRESENTED moved(documented) | Independence seal (S3.17), F1: sealed by process exit (the phase-1 report file exists afte
131. VL-21-131 | MODULE-tasklist -> DROP | REPRESENTED dedup->VL-22-017 | Independence seal (S3.17), mid-run designs: hook-side transcript snapshot written before t
132. VL-21-132 | EVAL -> EVAL | REPRESENTED same-dest | A snapshot seals only a partial first pass (luna writes one findings block at the end), so
133. VL-21-133 | MODULE-tasklist -> CORE | REPRESENTED moved(documented) | Mechanical peer tag (S3.17): a finding line gets `"origin":"peer"` when its anchor overlap
134. VL-21-134 | EVAL -> EVAL | REPRESENTED same-dest | Alarms on "own sealed findings per run" cannot be computed from a transcript snapshot and 
135. VL-21-135 | EVAL -> EVAL | REPRESENTED same-dest | CONVERGENCE alarm (S3.18): mean pairwise Jaccard of Task sets anchored by reviewers over `
136. VL-21-136 | EVAL -> EVAL | REPRESENTED same-dest | ECHO share (S3.18): restating peer content, alarm above 30% for F1 and above 60% for F4
137. VL-21-137 | EVAL -> EVAL | REPRESENTED same-dest | F7 overlap alarm (S3.18): `flag_finding_overlap` above 50% stops the arm and is reported
138. VL-21-138 | DROP -> DROP | REPRESENTED same-dest | Transports rejected (S3.19): Orca mail, A2A, cross-session messaging (no durable audit; ga
139. VL-21-139 | CORE -> CORE | REPRESENTED same-dest | Read-only rule (S3.20): `--disallowedTools Edit Write NotebookEdit` unchanged; `panel-post
140. VL-21-140 | EVAL -> EVAL | REPRESENTED same-dest | "Because Bash is unrestricted, this is enforced by audit (section 5.5)" (S3.20): read-only
141. VL-21-141 | MODULE-tasklist -> MODULE-tasklist | REPRESENTED same-dest | Kill switch details (S3.21): `PANEL_COLLAB=0` means no hooks, helpers or phase 2; it resto
142. VL-21-142 | EVAL -> EVAL | REPRESENTED same-dest | Seconds per turn (S3.22): ember 41 s/13 turns = 3.2; luna 102 s/16 = 6.4; haiku 233 s/10 =
143. VL-21-143 | HARNESS -> HARNESS | REPRESENTED same-dest | One move costs about 2 turns; resumed `claude -p` start about 6 s, fresh-session fallback 
144. VL-21-144 | HARNESS -> HARNESS | REPRESENTED same-dest | Hooks cost about 2 s per package (about 16 calls x 0.1 s, UNVERIFIED)
145. VL-21-145 | EVAL -> EVAL | REPRESENTED same-dest | Named baseline EL2 (S3.23; S07 ember + 2x luna): planning B 116 s (348/3), phase-2 deadlin
146. VL-21-146 | EVAL -> EVAL | REPRESENTED same-dest | Named baseline HL2 (S3.23; S24 haiku + 2x luna): 238 s (715/3), cap 309.4, 321.3, 357, 63.
147. VL-21-147 | EVAL -> EVAL | REPRESENTED same-dest | Named baseline SL2 (S3.23; sonnet + 2x luna): 273.7 s (821/3), 355.8, 369.5, 410.6, 46.4k 
148. VL-21-148 | EVAL -> EVAL | REPRESENTED same-dest | "Spread inside one package (alias 98-171 s on EL2) is larger than any design's added time,
149. VL-21-149 | MODULE-tasklist -> CORE | REPRESENTED moved(documented) | Timing rule 1 (S3.24): `PANEL_FINISH_AT = T0 + 1.35 B_f - turn_p90 - T_report_p90` (T0+143
150. VL-21-150 | MODULE-tasklist -> MODULE-tasklist | REPRESENTED same-dest | Timing rule 2 (S3.24): `k = max(0, min(2, floor((0.35 B_A1 - hooks - turn_p90 - T_report_p
151. VL-21-151 | MODULE-tasklist -> CORE | REPRESENTED moved(documented) | Timing rule 3 (S3.24): three numbers per mid-run design: planned end, finish-signal bound 
152. VL-21-152 | MODULE-tasklist -> MODULE-tasklist | REPRESENTED same-dest | Timing rule 4 (S3.24): for F4, F3, F6, F7 the +35% cap is AUDITED (R-24 SLO budget, error 
153. VL-21-153 | EVAL -> EVAL | REPRESENTED same-dest | Timing rule 5 (S3.24): baseline rule parts a-e including per-slot slowdown limits s <= (0.
154. VL-21-154 | EVAL -> EVAL | REPRESENTED same-dest | Timing rule 6 (S3.24): a values file per package is committed with sha256 before the first
155. VL-21-155 | EVAL -> EVAL | REPRESENTED same-dest | Timing rule 7 (S3.24): `finish_would_fire` counterfactual logged in A1 and A2
156. VL-21-156 | MODULE-tasklist -> CORE | REPRESENTED moved(documented) | Timing rule 8 (S3.24): hook settings are baked per reviewer (R-21)
157. VL-21-157 | EVAL -> EVAL | REPRESENTED same-dest | Timing rule 9 (S3.24): every "+x%" is valid only at its stated B and k
158. VL-21-158 | MODULE-tasklist -> DROP | REPRESENTED dedup->DR-023 | Harness fix H1 (S3.25): name the absolute source.md path in the reviewer brief
159. VL-21-159 | CORE -> CORE | REPRESENTED same-dest | Harness fix H2 (S3.25): truncate `anchor`/`anchor2` to 200 and `claim` to 300 chars before
160. VL-21-160 | HARNESS -> HARNESS | REPRESENTED same-dest | Harness fix H3 (S3.25): build the sandbox from the commit the plan was written against (pa
161. VL-21-161 | HARNESS -> HARNESS | REPRESENTED same-dest | Harness fix H4 (S3.25): remove `.dev/reflect/` and other leak directories (R-03) from the 
162. VL-21-162 | EVAL -> EVAL | REPRESENTED same-dest | "The grading rule (an unstated requirement is graded Medium) and the blind judge are held 
163. VL-21-163 | MODULE-tasklist -> CORE | REPRESENTED moved(documented) | Lifecycle (S3.26): one phase-2 deadline T0+1.30 B_A1; a re-ask is logged as `reask_s`; pha
164. VL-21-164 | MODULE-tasklist -> CORE | REPRESENTED moved(documented) | Lifecycle (S3.26): every arm drops `--no-session-persistence` (`RR:48`)
165. VL-21-165 | CORE -> CORE | REPRESENTED same-dest | Lifecycle (S3.26): retry loop `RR:61-64` re-runs a whole review on attempt 2 and `NOFALLBA
166. VL-21-166 | CORE -> CORE | REPRESENTED same-dest | Lifecycle (S3.26): a common hang guard kills a reviewer at T0 + 1.5 B_A1 (`hang_kill`) in 
167. VL-21-167 | EVAL -> EVAL | REPRESENTED same-dest | Largest historical alias run was 171 s against a hang guard of 1.5 x 120 = 180 s (S3.26)
168. VL-21-168 | EVAL -> EVAL | REPRESENTED same-dest | Bottom-up H estimate (S3.27): H3 +0.08 /14 per cheap run (range 0.02-0.16)
169. VL-21-169 | EVAL -> EVAL | REPRESENTED same-dest | H1 (S3.27): +0.03 (0.01-0.08), because 39% of ember and 22% of luna runs never read source
170. VL-21-170 | EVAL -> EVAL | REPRESENTED same-dest | H2 (S3.27): +0.03 (0.00-0.10); "92 findings dropped over 264 merges, 49 of them blocking; 
171. VL-21-171 | EVAL -> EVAL | REPRESENTED same-dest | H4 (S3.27): 0 in 30 runs, lowers measured I7 for sonnet panels by about 2 of 9 credits
172. VL-21-172 | EVAL -> EVAL | REPRESENTED same-dest | Total H for EL2 +0.14 per run, range 0.03-0.34; SL2 H share "+0.1 to +0.4 per run, UNVERIF
173. VL-21-173 | EVAL -> EVAL | REPRESENTED same-dest | Spike 5 (S3.27) re-scores the raw findings of the 30 cheap historical runs with the normal
174. VL-21-174 | EVAL -> EVAL | REPRESENTED same-dest | Act-rate caveat (S3.28): every gain chain multiplies by an act rate (0.5-0.85); "No measur
175. VL-21-175 | EVAL -> EVAL | REPRESENTED same-dest | Distinctness criterion (S3.29): a slot is the triple (content source, content form, delive
176. VL-21-176 | KNOWLEDGE -> KNOWLEDGE | REPRESENTED same-dest | Slate triples (S3.29): F1 finished findings / peer anchor + move / between phases; F4 help
177. VL-21-177 | KNOWLEDGE -> KNOWLEDGE | REPRESENTED same-dest | Closest slate pairs (S3.29): F1/F6, F3/F6, F4/F7; F3/F6 distinct only because F3 names a m
178. VL-21-178 | DROP -> DROP | REPRESENTED same-dest | Family F5 (structural index / source-rule witness) dropped: differs from F4 in 0 of 3 and 
179. VL-21-179 | DROP -> DROP | REPRESENTED same-dest | Family F2 (mid-run method relay) dropped: differs from F7 in at most 1 of 3; I6 keeps its 
180. VL-21-180 | DROP -> DROP | REPRESENTED same-dest | Seed theory T1 (S2.16): plan-bounded search scope; control test file opened 0 of 176 cheap
181. VL-21-181 | DROP -> DROP | REPRESENTED same-dest | Seed theory T2 (S2.16): right place, wrong question; 16 cheap findings on the exact GT10 s
182. VL-21-182 | DROP -> DROP | REPRESENTED same-dest | Seed theory T3 (S2.16): evidence environment and grading rules; post-implementation checko
183. VL-21-183 | DROP -> DROP | REPRESENTED same-dest | Seed hint B1/B2 (S2.17): "state the finite check that proves it"
184. VL-21-184 | DROP -> DROP | REPRESENTED same-dest | Seed hint B5 (S2.17): "what does the mapping return after each halt reason?"
185. VL-21-185 | DROP -> DROP | REPRESENTED same-dest | Seed hint I1 (S2.17): "check producer/consumer pairs against source.md, not the code"
186. VL-21-186 | DROP -> DROP | REPRESENTED same-dest | Seed hint I4 (S2.17): "run each grep criterion against the exact text the task tells you t
187. VL-21-187 | DROP -> DROP | REPRESENTED same-dest | Seed hint I5 (S2.17): "where else in the repo is this claim stated?"
188. VL-21-188 | DROP -> DROP | REPRESENTED same-dest | Seed hint B6/B8 (S2.17): "count the files an all/only sentence covers and how many break i
189. VL-21-189 | DROP -> DROP | REPRESENTED same-dest | Seed hint I6 (S2.17): "apply the same check to Tasks 3 and 7" (untested; nobody found I6)
190. VL-21-190 | DROP -> DROP | REPRESENTED same-dest | Seed hint I7 (S2.17): "grep tests/ for the files the plan edits; open test files the plan 
191. VL-21-191 | MODULE-tasklist -> MODULE-tasklist | REPRESENTED same-dest | Redesign 1 Move Radar mechanism (S4.1.1): a `PostToolUse` hook logs each tool call (name +
192. VL-21-192 | MODULE-tasklist -> MODULE-tasklist | REPRESENTED same-dest | Radar injection policy (S4.1.1): ONE move per checkpoint by reviewer style: ember (searche
193. VL-21-193 | EVAL -> EVAL | REPRESENTED same-dest | Radar (S4.1.1): "No model writes anything"; "F3's collaboration share may be near 0"; arm 
194. VL-21-194 | MODULE-tasklist -> MODULE-tasklist | REPRESENTED same-dest | Radar schedule (S4.1.2): first k checkpoints, ember after tool calls 6 and 10, luna after 
195. VL-21-195 | MODULE-tasklist -> MODULE-tasklist | REPRESENTED same-dest | Radar transport (S4.1.3): board + hooks, "the only transport where the model takes no acti
196. VL-21-196 | EVAL -> EVAL | REPRESENTED same-dest | Radar time (S4.1.4): ember +6.4 s (k=1) or 12.8 s, ending 47.4/53.8 s off the critical pat
197. VL-21-197 | MODULE-tasklist -> MODULE-tasklist | REPRESENTED same-dest | Radar contamination (S4.1.5): shares only move ids and the source.md check; withholds ever
198. VL-21-198 | EVAL -> EVAL | REPRESENTED same-dest | Radar leak check (S4.1.5) reduces to a lookup; any injected line that is not a catalogue m
199. VL-21-199 | EVAL -> EVAL | REPRESENTED same-dest | Radar gain, ember rows (S4.1.6; act rate 50-80% planning; gross k=2 / k=1): I4 0.05-0.20/0
200. VL-21-200 | EVAL -> EVAL | REPRESENTED same-dest | Radar C /14 net of static kit: 0-0.48 (k=2), 0-0.24 (k=1) (S4.1.6)
201. VL-21-201 | EVAL -> EVAL | REPRESENTED same-dest | Radar P rows, luna (S4.1.6): B1/B2 0-0.05 each; B5 0.05-0.15; I1 0.03-0.10; I6 0-0.05; P /
202. VL-21-202 | EVAL -> EVAL | REPRESENTED same-dest | Radar I7 (control /2, S4.1.6): M1 to ember 0.10-0.40 (k=2), 0.05-0.20 (k=1)
203. VL-21-203 | HARNESS -> HARNESS | REPRESENTED same-dest | Radar effort (S4.1.7): board substrate about 100 lines, `radar-classify.sh` about 60, gap 
204. VL-21-204 | EVAL -> EVAL | REPRESENTED same-dest | Radar failure (S4.1.8): classifier mislabels a call; gaps always the same moves (measures 
205. VL-21-205 | EVAL -> EVAL | REPRESENTED same-dest | Radar failure (S4.1.8): reviewer ignores the injection (gain falls to A2)
206. VL-21-206 | EVAL -> EVAL | REPRESENTED same-dest | Radar failure (S4.1.8): any injection other than a move id or the source.md check is a har
207. VL-21-207 | HARNESS -> HARNESS | REPRESENTED same-dest | Radar failure (S4.1.8): hooks may not fire on gateway models (`hook_calls = 0`, Spike S0 g
208. VL-21-208 | MODULE-tasklist -> MODULE-tasklist | REPRESENTED same-dest | Radar failure (S4.1.8): luna ignores "finish now" (`finish_signal_t`, `hang_kill`, SLO err
209. VL-21-209 | MODULE-tasklist -> MODULE-tasklist | REPRESENTED same-dest | Idle-Shift Sweeper mechanism (S4.2.1): ember finishes at about 41 s (sealed by process exi
210. VL-21-210 | MODULE-tasklist -> MODULE-tasklist | REPRESENTED same-dest | Sweeper witness fact (S4.2.1): one place may hold a "witness" fact (a source.md line with 
211. VL-21-211 | MODULE-tasklist -> MODULE-tasklist | REPRESENTED same-dest | Sweeper harvest (S4.2.1): a harvest hook adds paths from sweeper tool output that nobody o
212. VL-21-212 | EVAL -> EVAL | REPRESENTED same-dest | Sweeper audience (S4.2.1): lunas are "read-driven followers: they open every file they are
213. VL-21-213 | MODULE-tasklist -> MODULE-tasklist | REPRESENTED same-dest | Sweeper rule NO CLEARANCE (S4.2.1): a count n=0 is never delivered as a count, only as a c
214. VL-21-214 | MODULE-tasklist -> MODULE-tasklist | REPRESENTED same-dest | Sweeper rule FIRST-HAND EVIDENCE (S4.2.1): every fact carries its command string and is ci
215. VL-21-215 | MODULE-tasklist -> MODULE-tasklist | REPRESENTED same-dest | Sweeper schedule (S4.2.2): trigger 1 ember exit starts the sweeper (about 41 s); trigger 2
216. VL-21-216 | MODULE-tasklist -> MODULE-tasklist | REPRESENTED same-dest | Sweeper limits (S4.2.2): at most 2k facts, each luna acts on at most k; 600 bytes per fact
217. VL-21-217 | MODULE-tasklist -> MODULE-tasklist | REPRESENTED same-dest | Sweeper transport (S4.2.3): board + hooks; "A between-phase digest would add a full luna p
218. VL-21-218 | EVAL -> EVAL | REPRESENTED same-dest | Sweeper time (S4.2.4): sweeper starts about 41 s, 6 s start + 10 turns x 3.2 s = 38 s, end
219. VL-21-219 | MODULE-tasklist -> MODULE-tasklist | REPRESENTED same-dest | Sweeper contamination (S4.2.5): shares repo facts with the command string; withholds ember
220. VL-21-220 | EVAL -> EVAL | REPRESENTED same-dest | "Ember's habit of asking whether a grep over-matches (the I5 inversion) cannot be passed o
221. VL-21-221 | EVAL -> EVAL | REPRESENTED same-dest | Sweeper gain, C rows (S4.2.6): I5 0.06-0.24 (k=2)/0.03-0.12 (k=1) (sweep lists the CHANGEL
222. VL-21-222 | EVAL -> EVAL | REPRESENTED same-dest | Sweeper totals (S4.2.6): C /14 0.14-0.67 (k=2), 0.07-0.34 (k=1); P none; H 0.03-0.34
223. VL-21-223 | EVAL -> EVAL | REPRESENTED same-dest | Sweeper I7 (control /2, S4.2.6): 0.17-0.50 (k=2), 0.09-0.25 (k=1) via chain 0.7-0.9 x 0.6-
224. VL-21-224 | HARNESS -> HARNESS | REPRESENTED same-dest | Sweeper effort (S4.2.7): board about 100 + sweeper brief about 25 + launcher hook about 15
225. VL-21-225 | EVAL -> EVAL | REPRESENTED same-dest | Sweeper failure (S4.2.8): snapshot not written (`SNAPSHOT` alarm above 50% of luna runs; f
226. VL-21-226 | MODULE-tasklist -> MODULE-tasklist | REPRESENTED same-dest | Sweeper failure (S4.2.8): sweeper floods trivial facts; facts arrive after luna finished (
227. VL-21-227 | EVAL -> EVAL | REPRESENTED same-dest | Sweeper failure (S4.2.8): the A1 ember run ends late (H1 makes it read source.md) so the s
228. VL-21-228 | EVAL -> EVAL | REPRESENTED same-dest | Sweeper failure (S4.2.8): wrong blockers rising more than A1 + 1.0 fails the arm
229. VL-21-229 | CORE -> CORE | REPRESENTED same-dest | Sweeper failure (S4.2.8): sweeper misrouted (`model_ok` check); luna hangs (`hang_kill`, S
230. VL-21-230 | MODULE-tasklist -> MODULE-tasklist | REPRESENTED same-dest | Axis-Flip Challenge phase 1 (S4.3.1): isolated review of A1, sealed as `<rid>.p1.md` after
231. VL-21-231 | MODULE-tasklist -> MODULE-tasklist | REPRESENTED same-dest | Axis-Flip selection (S4.3.1): the harness parses findings-v1 blocks of finished peers and 
232. VL-21-232 | MODULE-tasklist -> MODULE-tasklist | REPRESENTED same-dest | Axis-Flip routing (S4.3.1): sends ONLY the anchor (never the claim) plus an axis-flip move
233. VL-21-233 | MODULE-tasklist -> MODULE-tasklist | REPRESENTED same-dest | Axis-Flip phase 2 (S4.3.1): `claude -p --resume <session_id> "<digest>"` returns an addend
234. VL-21-234 | EVAL -> EVAL | REPRESENTED same-dest | Internal inconsistency (S4.3.1): "ember anchored the I5 sentence 15 times and the B5 mappi
235. VL-21-235 | MODULE-tasklist -> MODULE-tasklist | REPRESENTED same-dest | Gap card (S4.3.2): each challenge slot holds a gap card instead of a peer anchor with p=1/
236. VL-21-236 | EVAL -> EVAL | REPRESENTED same-dest | Gap card odds (S4.3.2): P(no gap card)=4/9, P(both)=1/9 for 2 slots; findings from gap slo
237. VL-21-237 | MODULE-tasklist -> MODULE-tasklist | REPRESENTED same-dest | Axis-Flip roles (S4.3.3): luna x2 receive reading flips on ember's anchors (ember 4.19 fin
238. VL-21-238 | KNOWLEDGE -> KNOWLEDGE | REPRESENTED same-dest | HL2 shadow variant V5-D5 (S4.3.4): haiku isolated canary never gets a digest; when both lu
239. VL-21-239 | MODULE-tasklist -> MODULE-tasklist | REPRESENTED same-dest | Axis-Flip schedule (S4.3.5): trigger is each reviewer's phase-1 exit; ember waits for both
240. VL-21-240 | MODULE-tasklist -> MODULE-tasklist | REPRESENTED same-dest | Axis-Flip limits (S4.3.5): digest at most 1,800 chars (3 x 600 bytes); schema `kind:"chall
241. VL-21-241 | MODULE-tasklist -> MODULE-tasklist | REPRESENTED same-dest | Axis-Flip transport (S4.3.6): the digest is a plain file (temp file then move = atomic); t
242. VL-21-242 | HARNESS -> HARNESS | REPRESENTED same-dest | Axis-Flip resume (S4.3.6): resume from the same cwd `/tmp/evalsb/repo`; if resume fails fo
243. VL-21-243 | MODULE-tasklist -> MODULE-tasklist | REPRESENTED same-dest | Axis-Flip stream capture (S4.3.6): phase-2 and re-ask sessions run `--output-format stream
244. VL-21-244 | EVAL -> EVAL | REPRESENTED same-dest | Axis-Flip time (S4.3.7): luna A (first finisher about 95 s) box 35 s n=2: 6 + 2 x 2 x 6.4 
245. VL-21-245 | MODULE-tasklist -> MODULE-tasklist | REPRESENTED same-dest | Axis-Flip bound (S4.3.7): the enforced phase-2 bound 150.8 s (+30.0%) is "the only bound i
246. VL-21-246 | MODULE-tasklist -> MODULE-tasklist | REPRESENTED same-dest | Axis-Flip contamination (S4.3.8): shares exact candidate quotes plus a catalogue move; wit
247. VL-21-247 | EVAL -> EVAL | REPRESENTED same-dest | Axis-Flip measurement (S4.3.8): decoys fill 1 slot in 3; CONVERGENCE on `origin:"own"` lin
248. VL-21-248 | EVAL -> EVAL | REPRESENTED same-dest | Axis-Flip gain model (S4.3.9): P(peer anchors the right sentence) x P(challenge selected a
249. VL-21-249 | EVAL -> EVAL | REPRESENTED same-dest | Axis-Flip C rows (S4.3.9): B5 0.04-0.15 (Task 8 33%); I1 0.02-0.08; I5 0-0.15 (Task 2 46%)
250. VL-21-250 | EVAL -> EVAL | REPRESENTED same-dest | Axis-Flip other shares (S4.3.9): P from the gap-card route to B1, B2, I4 is 0-0.10 /14; H 
251. VL-21-251 | HARNESS -> HARNESS | REPRESENTED same-dest | Axis-Flip effort (S4.3.10): run-reviewer.sh about 5; phase2-digest.sh about 70; launcher a
252. VL-21-252 | MODULE-tasklist -> MODULE-tasklist | REPRESENTED same-dest | Axis-Flip failure (S4.3.11): `--resume` fails on a gateway model (fresh fallback `resume_f
253. VL-21-253 | MODULE-tasklist -> MODULE-tasklist | REPRESENTED same-dest | Axis-Flip failure (S4.3.11): phase 2 rewrites phase 1 (phase-1 lines immutable); phase-2 b
254. VL-21-254 | CORE -> CORE | REPRESENTED same-dest | Axis-Flip failure (S4.3.11): no qualifying peer anchor; two findings blocks in one report 
255. VL-21-255 | HARNESS -> HARNESS | REPRESENTED same-dest | Axis-Flip failure (S4.3.11): session storage grows on the host (delete only the session id
256. VL-21-256 | MODULE-tasklist -> MODULE-tasklist | REPRESENTED same-dest | Flag-and-Adjudicate mechanism (S4.4.1): one-way on EL2; ember (flagger) is told to FLAG, n
257. VL-21-257 | MODULE-tasklist -> MODULE-tasklist | REPRESENTED same-dest | Flag card form (S4.4.1): a card is anchor + reading move (M3, M4, M5, M6, M9) + `category`
258. VL-21-258 | MODULE-tasklist -> MODULE-tasklist | REPRESENTED same-dest | Adjudicators (S4.4.1): luna x2 answer each card with a finite check and its result in thei
259. VL-21-259 | MODULE-tasklist -> MODULE-tasklist | REPRESENTED same-dest | Deal and form (S4.4.2): card i goes to luna (i + r) mod 2; rendered in challenge form (anc
260. VL-21-260 | EVAL -> EVAL | REPRESENTED same-dest | Seed Q3 answered within F7 (S4.4.2) by conversion by form; "Arm A5 against arm A4 does not
261. VL-21-261 | MODULE-tasklist -> MODULE-tasklist | REPRESENTED same-dest | Flag schedule (S4.4.3): ember posts from the 3rd tool call, at most 2k cards, over cap `ov
262. VL-21-262 | EVAL -> EVAL | REPRESENTED same-dest | Flag per-slot log (S4.4.3): form, recipient, card Task, conversion (receiver's line overla
263. VL-21-263 | MODULE-tasklist -> MODULE-tasklist | REPRESENTED same-dest | Flag transport (S4.4.4): board + hooks; cross-session `SendMessage` is a named fallback on
264. VL-21-264 | EVAL -> EVAL | REPRESENTED same-dest | Flag time (S4.4.5): ember +6.4 s (k=1)/12.8 s (k=2) ending 47.4/53.8 s off the path; luna 
265. VL-21-265 | MODULE-tasklist -> MODULE-tasklist | REPRESENTED same-dest | Flag contamination (S4.4.6): shares an anchor + move (challenge form) or anchor + enum cat
266. VL-21-266 | EVAL -> EVAL | REPRESENTED same-dest | Flag agreement alarm (S4.4.6): the adjudicator raises a finding on more than 90% of cards 
267. VL-21-267 | EVAL -> EVAL | REPRESENTED same-dest | Flag overlap stop (S4.4.6): `flag_finding_overlap` above 50% stops the arm and the treatme
268. VL-21-268 | EVAL -> EVAL | REPRESENTED same-dest | Flag gain model (S4.4.7): P(flagger posts a card on the sentence: compliance 0.6-0.8 x sen
269. VL-21-269 | EVAL -> EVAL | REPRESENTED same-dest | Flag C rows (S4.4.7; k=2 / k=1): B1 0-0.16/0-0.08 (T2b, M3 card); B2 0-0.08/0-0.04; I4 0.0
270. VL-21-270 | EVAL -> EVAL | REPRESENTED same-dest | Flag feasibility (S4.4.7): needs k >= 1 on designSpec, where the median 100 s allows k >= 
271. VL-21-271 | EVAL -> EVAL | REPRESENTED same-dest | Flag falsification (S4.4.7): the B5 (Task 8), I1 and I4 (Task 12) rows are falsified if 2k
272. VL-21-272 | EVAL -> EVAL | REPRESENTED same-dest | Flag form-contrast analysis (S4.4.7): pre-registered, at most 144 cards, about 72 per form
273. VL-21-273 | EVAL -> EVAL | REPRESENTED same-dest | Note (S4.4.7): the flagging step could be replaced by a deterministic sentence extractor (
274. VL-21-274 | HARNESS -> HARNESS | REPRESENTED same-dest | Flag effort (S4.4.8): board about 100 + deal/form renderer about 40 + card validator about
275. VL-21-275 | EVAL -> EVAL | REPRESENTED same-dest | Flag failure (S4.4.9): ember never posts (`cards_sent = 0`; in more than 50% of runs the d
276. VL-21-276 | EVAL -> EVAL | REPRESENTED same-dest | Flag failure (S4.4.9): cards spent on early Tasks; flags behave like findings
277. VL-21-277 | EVAL -> EVAL | REPRESENTED same-dest | Flag failure (S4.4.9): card overload (`ledger_rows` more than 20% below A1); snapshot not 
278. VL-21-278 | EVAL -> EVAL | REPRESENTED same-dest | Flag failure (S4.4.9): wrong blockers above A1 + 1.0 fails the arm; luna past the finish-s
279. VL-21-279 | EVAL -> EVAL | REPRESENTED same-dest | Coverage Deflection premise (S4.5.1): "Every panel converges on the easy issues: B3 is fou
280. VL-21-280 | EVAL -> EVAL | REPRESENTED same-dest | Coverage Deflection roles (S4.5.1): on SL2 the lunas finish at about 102-110 s versus sonn
281. VL-21-281 | MODULE-tasklist -> MODULE-tasklist | REPRESENTED same-dest | Deflection watcher (S4.5.1): a harness watcher parses each luna findings block into (Task,
282. VL-21-282 | MODULE-tasklist -> MODULE-tasklist | REPRESENTED same-dest | Deflection instruction (S4.5.1): "apply catalogue moves M1-M10 to these Tasks first; finis
283. VL-21-283 | MODULE-tasklist -> MODULE-tasklist | REPRESENTED same-dest | Deflection card content (S4.5.1): carries NO counts, categories or covered list ("a covere
284. VL-21-284 | MODULE-tasklist -> MODULE-tasklist | REPRESENTED same-dest | Deflection schedule (S4.5.2): trigger each luna exit (about 102-110 s); delivery on sonnet
285. VL-21-285 | EVAL -> EVAL | REPRESENTED same-dest | Deflection run condition (S4.5.2): the arm runs only if Spike 4 gives sonnet T_report_p90 
286. VL-21-286 | MODULE-tasklist -> MODULE-tasklist | REPRESENTED same-dest | Surface filter (S4.5.3): surface findings do not count as coverage, else luna's Task 12 ar
287. VL-21-287 | MODULE-tasklist -> MODULE-tasklist | REPRESENTED same-dest | Deflection transport (S4.5.4): board + a hook in sonnet only; harness-generated cards; "So
288. VL-21-288 | EVAL -> EVAL | REPRESENTED same-dest | Deflection time (S4.5.5): luna scouts unchanged; sonnet k=1 hooks 2 s + 1 x 2 x 14 = 30 s 
289. VL-21-289 | EVAL -> EVAL | REPRESENTED same-dest | "Sonnet's final report turn is output-heavy (about 30k output tokens per run), so this is 
290. VL-21-290 | MODULE-tasklist -> MODULE-tasklist | REPRESENTED same-dest | Deflection contamination (S4.5.6): shares uncovered Task ids only; withholds anchors, clai
291. VL-21-291 | EVAL -> EVAL | REPRESENTED same-dest | Deflection alarm (S4.5.6): sonnet's anchored Tasks overlap lunas' covered Tasks above 50%,
292. VL-21-292 | EVAL -> EVAL | REPRESENTED same-dest | Sonnet isolated reach per run (S4.5.7): I4 4 of 26, B5 2, I1 1, I7 7 of 26 clean (investig
293. VL-21-293 | EVAL -> EVAL | REPRESENTED same-dest | Deflection gain derivation (S4.5.7): for SL2, high = base rows at k=2 (base low 0.26, high
294. VL-21-294 | EVAL -> EVAL | REPRESENTED same-dest | Deflection C rows (S4.5.7; k=2 / k=1): I4 0.025-0.20/0.0125-0.10; I5 0.015-0.15/0.0075-0.0
295. VL-21-295 | EVAL -> EVAL | REPRESENTED same-dest | Deflection H and I7 (S4.5.7): H /14 SL2 +0.1 to +0.4 UNVERIFIED (no bottom-up SL2 table); 
296. VL-21-296 | HARNESS -> HARNESS | REPRESENTED same-dest | Deflection effort (S4.5.8): hook in sonnet about 60 lines; coverage watcher (poll every 2 
297. VL-21-297 | EVAL -> EVAL | REPRESENTED same-dest | Deflection failure (S4.5.9): deflection pushes sonnet off a Task where a peer's wrong bloc
298. VL-21-298 | EVAL -> EVAL | REPRESENTED same-dest | Deflection failure (S4.5.9): sonnet ignores the cards (gain 0, no harm); sonnet past the f
299. VL-21-299 | EVAL -> EVAL | REPRESENTED same-dest | Deflection failure (S4.5.9): if T_report_p90 exceeds 51.8 s the F6 arm is not run
300. VL-21-300 | EVAL -> EVAL | REPRESENTED same-dest | Deflection cost (S4.5.9): needs a sonnet panel "(2.2x tokens of ember + 2x luna)"; "Use on
301. VL-21-301 | KNOWLEDGE -> KNOWLEDGE | REPRESENTED same-dest | "Grok is used in no design: its median of 790 s per review, and 2,109-3,897 s elapsed in i
302. VL-21-302 | EVAL -> EVAL | REPRESENTED same-dest | Comparison row Slot 1, Redesign 3 Axis-Flip (S5.1): 134.8 s (+16.2%) / 147.6 s (+27.2%) at
303. VL-21-303 | EVAL -> EVAL | REPRESENTED same-dest | Comparison row Slot 2, Redesign 2 Sweeper (S5.1): 130.8 (+12.8%) / 143.6 (+23.8%); C 0.07-
304. VL-21-304 | EVAL -> EVAL | REPRESENTED same-dest | Comparison row Slot 3, Redesign 1 Radar (S5.1): same time as F4; C 0-0.24 / 0-0.48; P 0.04
305. VL-21-305 | EVAL -> EVAL | REPRESENTED same-dest | Comparison row Slot 4, Redesign 5 Deflection SL2 (S5.1): 303.7 (+11.0%) / 331.7 (+21.2%); 
306. VL-21-306 | EVAL -> EVAL | REPRESENTED same-dest | Comparison row Slot 5, Redesign 4 Flag-Adjudicate (S5.1): same time as F4; C 0.04-0.39 / 0
307. VL-21-307 | EVAL -> EVAL | REPRESENTED same-dest | Comparison control row A2 static kit (S5.1): about +29% elapsed (V5 estimate, UNVERIFIED);
308. VL-21-308 | EVAL -> EVAL | REPRESENTED same-dest | Comparison baseline A1 isolated with H on EL2 (S5.1): B_A1 (planning 116 s); 0 on C, P, I7
309. VL-21-309 | EVAL -> EVAL | REPRESENTED same-dest | Comparison baseline A1-SL2 (S5.1): +136% elapsed vs EL2 (821 vs 348 s three packages); his
310. VL-21-310 | MODULE-tasklist -> MODULE-tasklist | REPRESENTED same-dest | KEY finding (S5.1 notes, merged-spec line 911): the static kit (A2) may beat every exchang
311. VL-21-311 | EVAL -> EVAL | REPRESENTED same-dest | First-experiment choice (S5.2.1): one pre-registered plan; four EL2 designs (F1, F4, F7, F
312. VL-21-312 | HARNESS -> HARNESS | REPRESENTED same-dest | Gate 0 spike S0 (S5.2.2): hooks fire in `claude -p` for `muse-ember-1.0` and `gpt-6-luna`;
313. VL-21-313 | HARNESS -> HARNESS | REPRESENTED same-dest | Gate 0 spike S1 (S5.2.2), only if F7 needs the fallback: cross-session `SendMessage` works
314. VL-21-314 | HARNESS -> HARNESS | REPRESENTED same-dest | Gate 0 spike S2 (S5.2.2): `--resume` works for gateway models once `--no-session-persisten
315. VL-21-315 | HARNESS -> HARNESS | REPRESENTED same-dest | Gate 0 spike S3 (S5.2.2): full-chain smoke test (reviewer, combiner, `superclaude review m
316. VL-21-316 | HARNESS -> HARNESS | REPRESENTED same-dest | Gate 0 REQ-S3 (S5.2.2): act-rate probe (inject "run `ls /tmp/panel-probe`"; the next tool 
317. VL-21-317 | HARNESS -> HARNESS | REPRESENTED same-dest | Gate 0 Spike 4 (S5.2.2): per-package B_A1, turn_p90, T_report_p90, PANEL_FINISH_AT and k r
318. VL-21-318 | DROP -> DROP | REPRESENTED same-dest | Gate 0 Spike 5 (S5.2.2): re-score the raw findings of the 30 cheap historical runs with th
319. VL-21-319 | EVAL -> EVAL | REPRESENTED same-dest | Arms and run counts (S5.2.3): block-randomised, concurrent; A0 4 runs (plus 6 historical S
320. VL-21-320 | EVAL -> EVAL | REPRESENTED same-dest | Size (S5.2.4): stage 1 at most 4 + 12 + 12 + 4x12 = 76 panel runs, 52 if every exchange ar
321. VL-21-321 | HARNESS -> HARNESS | REPRESENTED same-dest | Conduct (S5.2.5): `NOFALLBACK=1`; at most 10 concurrent runs and at most 4 ember (`HO2:236
322. VL-21-322 | EVAL -> EVAL | REPRESENTED same-dest | Conduct (S5.2.5): the same blind judge `EVAL/tools/tmp-scripts/judge-one.sh`, sha256-pinne
323. VL-21-323 | EVAL -> EVAL | REPRESENTED same-dest | Conduct (S5.2.5): anonymised merged reports with `origin` keys and board refs stripped; th
324. VL-21-324 | EVAL -> EVAL | REPRESENTED same-dest | Primary endpoint (S5.2.6): target reach = at least 1 credit on B1, B2, B5, B6, B8, I1, I4,
325. VL-21-325 | EVAL -> EVAL | REPRESENTED same-dest | Decision rule 1 (S5.2.7): beats A1 by one-sided Fisher p < 0.05: A1 reach 0 needs 4/12 (p 
326. VL-21-326 | EVAL -> EVAL | REPRESENTED same-dest | Decision rule 2 (S5.2.7): beats A2 by at least 4 reach runs at n=12
327. VL-21-327 | EVAL -> EVAL | REPRESENTED same-dest | Decision rule 3 (S5.2.7): mean found /14 >= A1 - 0.25; wrong blockers <= A1 + 1.0; control
328. VL-21-328 | EVAL -> EVAL | REPRESENTED same-dest | Decision rule 4 (S5.2.7): time median <= 1.35 B_A1 within R-24 (1 in 12), none above 1.5 B
329. VL-21-329 | EVAL -> EVAL | REPRESENTED same-dest | Decision rule 5 (S5.2.7): independence: CONVERGENCE in at most 2 of 12 runs, zero audit vi
330. VL-21-330 | EVAL -> EVAL | REPRESENTED same-dest | Interim look (S5.2.8): at 6 runs, futility only: stop if hard-issue credits <= A1's, or me
331. VL-21-331 | EVAL -> EVAL | REPRESENTED same-dest | Multiplicity (S5.2.9): four arms each at 0.05, familywise at most 0.20 (Bonferroni); accep
332. VL-21-332 | EVAL -> EVAL | REPRESENTED same-dest | Stage-2 screen F6 (S5.2.10): SL2 already reached I7 in 3 of 6 historical runs; at A1-SL2 6
333. VL-21-333 | EVAL -> EVAL | REPRESENTED same-dest | Detectability (S5.2.11): H 0.03-0.34 /14 per run mostly on reach issues, so A1's own reach
334. VL-21-334 | EVAL -> EVAL | REPRESENTED same-dest | Outcomes (S5.2.12): X passes means a 12-run confirmation on at least 2 new packages; no ex
335. VL-21-335 | EVAL -> EVAL | REPRESENTED same-dest | Abort rules (S5.2.12): futility, R-24 budget spent, `flag_finding_overlap` above 50% (A5),
336. VL-21-336 | EVAL -> EVAL | REPRESENTED same-dest | Pre-registration (S5.2.12): decision rule, values file and analysis script committed befor
337. VL-21-337 | MODULE-tasklist -> CORE | REPRESENTED moved(documented) | R-01 (S5.3, harness precondition H1): source.md path named in the brief; verify 0 of 12 A1
338. VL-21-338 | CORE -> CORE | REPRESENTED same-dest | R-02 (H2): truncate, validate with the real parser, re-ask once; unit test fixture with a 
339. VL-21-339 | HARNESS -> HARNESS | REPRESENTED same-dest | R-03 (H3/H4): sandbox is a `git archive` of the commit the plan was written against minus 
340. VL-21-340 | CORE -> CORE | REPRESENTED same-dest | R-04: findings-v1 and `superclaude review merge` stay unchanged; merge arguments as `EVAL/
341. VL-21-341 | MODULE-tasklist -> MODULE-tasklist | REPRESENTED same-dest | R-05: `PANEL_COLLAB=0` launch command is byte-identical to `RR:48` except R-01, R-03, no `
342. VL-21-342 | MODULE-tasklist -> MODULE-tasklist | REPRESENTED same-dest | R-06: panel-msg/1 at most 600 bytes, forbidden keys, ember card exception; validator test 
343. VL-21-343 | MODULE-tasklist -> MODULE-tasklist | REPRESENTED same-dest | R-07: move field M1-M10 only; catalogue frozen with sha256; no `plan_quote` substring of 1
344. VL-21-344 | MODULE-tasklist -> CORE | REPRESENTED moved(documented) | R-08: anchor is an exact substring of 12-200 chars; items exist in the sandbox
345. VL-21-345 | CORE -> CORE | REPRESENTED same-dest | R-09: `--disallowedTools Edit Write NotebookEdit`; helpers write only `$BOARD` outside the
346. VL-21-346 | EVAL -> EVAL | REPRESENTED same-dest | R-10: origin tags; hook-side snapshot sha256; the anonymiser strips `origin`; a grep of `m
347. VL-21-347 | MODULE-tasklist -> MODULE-tasklist | REPRESENTED same-dest | R-11 (F1): `p1.md` sealed after the re-ask
348. VL-21-348 | MODULE-tasklist -> MODULE-tasklist | REPRESENTED same-dest | R-12 (F1): the digest selects only `unpassable-check`/`contradiction`/`missing-requirement
349. VL-21-349 | MODULE-tasklist -> MODULE-tasklist | REPRESENTED same-dest | R-13 (F1): routing table; a challenge never goes back to the anchor's author
350. VL-21-350 | MODULE-tasklist -> MODULE-tasklist | REPRESENTED same-dest | R-14 (F1): resume, else fresh-session fallback `resume_fallback`
351. VL-21-351 | MODULE-tasklist -> MODULE-tasklist | REPRESENTED same-dest | R-15 (F1): n formula and one deadline, stream-json, salvage; test values n=2 (6.4 s), 1 (7
352. VL-21-352 | MODULE-tasklist -> MODULE-tasklist | REPRESENTED same-dest | R-16 (F1): exactly one findings-v1 block per report; phase-2 ids `P2-F<n>`
353. VL-21-353 | MODULE-tasklist -> MODULE-tasklist | REPRESENTED same-dest | R-17 (F4): sweeper session runs M1, M2, M7 plus at most one witness fact, never receives e
354. VL-21-354 | MODULE-tasklist -> MODULE-tasklist | REPRESENTED same-dest | R-18 (F4): at most 2k facts, command string, at most 8 items, n=0 rendered as a command on
355. VL-21-355 | MODULE-tasklist -> MODULE-tasklist | REPRESENTED same-dest | R-19 (F4): luna hook delivers after the 6th tool call and the snapshot
356. VL-21-356 | MODULE-tasklist -> MODULE-tasklist | REPRESENTED same-dest | R-20 (F4): balanced deal, at most k facts, first-hand citation; more than 10% mismatch sto
357. VL-21-357 | MODULE-tasklist -> CORE | REPRESENTED moved(documented) | R-21: per-reviewer `--settings` with an env-cleared test
358. VL-21-358 | MODULE-tasklist -> CORE | REPRESENTED moved(documented) | R-22: hooks never fail the reviewer (`hook_error`)
359. VL-21-359 | CORE -> CORE | REPRESENTED same-dest | R-23: `collab.json` field list: arm, msgs_sent, msgs_received, first_delivery_t, seal_t, r
360. VL-21-360 | MODULE-tasklist -> MODULE-tasklist | REPRESENTED same-dest | R-24: elapsed target <= 1.35 B_A1, error budget 1 in 12, hang guard `SLO_BREACH`
361. VL-21-361 | EVAL -> EVAL | REPRESENTED same-dest | R-25: alarms CONVERGENCE, ECHO (30% / 60%), SNAPSHOT (above 50%), `flag_finding_overlap`
362. VL-21-362 | CORE -> CORE | REPRESENTED same-dest | R-26: the board directory is never deleted, and on contamination it is quarantined in plac
363. VL-21-363 | HARNESS -> HARNESS | REPRESENTED same-dest | R-27: Gate 0 spike results recorded
364. VL-21-364 | HARNESS -> HARNESS | REPRESENTED same-dest | R-28: arms and counts as planned, `NOFALLBACK=1`, at most 10 concurrent, at most 4 ember, 
365. VL-21-365 | EVAL -> EVAL | REPRESENTED same-dest | R-29: one judge call per (arm, run, package), per-batch API-error audit
366. VL-21-366 | EVAL -> EVAL | REPRESENTED same-dest | R-30: decision rule, analysis script and values file with sha256 committed before the firs
367. VL-21-367 | MODULE-tasklist -> MODULE-tasklist | REPRESENTED same-dest | R-31 (F3): the classifier works only through observable signatures
368. VL-21-368 | MODULE-tasklist -> MODULE-tasklist | REPRESENTED same-dest | R-32 (F3): one move id per injection, at most k at checkpoints, none after T0 + 1.35 B_A1 
369. VL-21-369 | EVAL -> EVAL | REPRESENTED same-dest | R-33 (F3): luna reading-move injections carry `slot_type` "static" and are booked to P; A6
370. VL-21-370 | MODULE-tasklist -> MODULE-tasklist | REPRESENTED same-dest | R-34 (F7): ember cards from the 3rd tool call, at most 2k
371. VL-21-371 | MODULE-tasklist -> MODULE-tasklist | REPRESENTED same-dest | R-35 (F7): deal and form unit test (r=c=0, i=0..3 gives recipients A,B,A,B and forms C,F,F
372. VL-21-372 | EVAL -> EVAL | REPRESENTED same-dest | R-36 (F7): per-slot log; secondary analysis pre-registered
373. VL-21-373 | EVAL -> EVAL | REPRESENTED same-dest | R-37 (F7): overlap above 50% stops the arm; `cards_sent = 0` in more than 50% of runs stop
374. VL-21-374 | MODULE-tasklist -> MODULE-tasklist | REPRESENTED same-dest | R-38 (F6): watcher semantics
375. VL-21-375 | MODULE-tasklist -> MODULE-tasklist | REPRESENTED same-dest | R-39 (F6): at most k requests; runs only if T_report_p90 <= 51.8 s; brief line "peer cover
376. VL-21-376 | EVAL -> EVAL | REPRESENTED same-dest | R-40 (F6): deflection alarm
377. VL-21-377 | DROP -> DROP | REPRESENTED same-dest | R-41 (timing): PANEL_FINISH_AT baked in
378. VL-21-378 | MODULE-tasklist -> MODULE-tasklist | REPRESENTED same-dest | R-42 (timing): k-formula test: B=116 gives 2; T_report_p90 11.0 gives 1; B=100 gives 1 onl
379. VL-21-379 | DROP -> DROP | REPRESENTED same-dest | R-43 (timing): the hang guard applies in every arm
380. VL-21-380 | DROP -> DROP | REPRESENTED same-dest | R-44 (timing): retry loop accounting
381. VL-21-381 | DROP -> DROP | REPRESENTED same-dest | R-45 (timing): slowdown limit s and drift band [0.963, 1.10]
382. VL-21-382 | HARNESS -> HARNESS | REPRESENTED same-dest | R-46 (timing): session cleanup deletes only that run's ids; test with two concurrent runs
383. VL-21-383 | DROP -> DROP | REPRESENTED same-dest | R-47 (timing): act rates replaced by REQ-S3 measured act rates
384. VL-21-384 | EVAL -> EVAL | REPRESENTED same-dest | Spec's own "not checked" list (S5.4), timing inputs: T_report_p90 (6.4 s luna, none for so
385. VL-21-385 | DROP -> DROP | REPRESENTED same-dest | "Not checked" list: act rates (0.5-0.85) and the act rate on "finish now"
386. VL-21-386 | EVAL -> EVAL | REPRESENTED same-dest | "Not checked" list, gain side: k=1 rows (each k=2 row halved); F6 gain for SL2 (low = base
387. VL-21-387 | HARNESS -> HARNESS | REPRESENTED same-dest | "The base commit for each package's sandbox: not recorded in an obvious file for any of th
388. VL-21-388 | EVAL -> EVAL | REPRESENTED same-dest | Risk (S5.4, lines 1122-1124): "a single strong run regresses to the mean (`CR:424`)"
389. VL-21-389 | DROP -> DROP | REPRESENTED same-dest | Risk (S5.4): the plan cannot detect the central gain estimates
390. VL-21-390 | DROP -> DROP | REPRESENTED same-dest | Risk (S5.4): the move catalogue was abstracted from the same 3 packages, so in-sample gain
391. VL-21-391 | DROP -> DROP | REPRESENTED same-dest | Variant files `variants/variant-N-*.md` are byte-identical to `adversarial/variant-N-origi
392. VL-21-392 | KNOWLEDGE -> KNOWLEDGE | REPRESENTED same-dest | Variant V1 opus:architect (681 lines): maintainability + extension scaffolding; Coverage b
393. VL-21-393 | KNOWLEDGE -> KNOWLEDGE | REPRESENTED same-dest | Variant V2 opus:analyzer (584 lines): root-cause, evidence-based; Frontier Relay, Axis-Fli
394. VL-21-394 | KNOWLEDGE -> KNOWLEDGE | REPRESENTED same-dest | Variant V3 haiku:backend (191 lines): API contracts, data integrity; Sweep Relay, Move-Hin
395. VL-21-395 | KNOWLEDGE -> KNOWLEDGE | REPRESENTED same-dest | Variant V4 opus:devops (759 lines): deploy/observability/SLO; Move Radar, Idle-Shift Sweep
396. VL-21-396 | KNOWLEDGE -> KNOWLEDGE | REPRESENTED same-dest | Variant V5 sonnet:performance (545 lines): bottlenecks, cost-to-serve; Claim-Index Relay, 
397. VL-21-397 | KNOWLEDGE -> KNOWLEDGE | REPRESENTED same-dest | Diff analysis groups all 25 redesigns into 7 families: F1 between-phase cross-examination,
398. VL-21-398 | KNOWLEDGE -> KNOWLEDGE | REPRESENTED same-dest | F1 is "the only family that four variants converged on independently with near-identical m
399. VL-21-399 | KNOWLEDGE -> KNOWLEDGE | REPRESENTED same-dest | "F3 is over-represented (7 of 25)" (diff analysis)
400. VL-21-400 | KNOWLEDGE -> KNOWLEDGE | REPRESENTED same-dest | Transport tally across 25 designs: JSON board 17, between-phase digest + `--resume` 5, cro
401. VL-21-401 | EVAL -> EVAL | REPRESENTED same-dest | Panels used across designs: EL2 x3 (V1), EL2 x2 + HL2 + SL2 + S14 (V2), EL2 x5 (V3; R3 add
402. VL-21-402 | DROP -> DROP | REPRESENTED same-dest | F1 member V1-R3 Cross-examination round (V1:298-319; ember+2x luna; up to 3 cards plus 1 g
403. VL-21-403 | DROP -> DROP | REPRESENTED same-dest | F1 member V2-D2 Axis-Flip Cross-Examination (V2:219-245; decoy 1 of 3)
404. VL-21-404 | DROP -> DROP | REPRESENTED same-dest | F1 member V4-3 Axis-Flip Challenge (V4:343-384; skips surface findings, routes by anchor t
405. VL-21-405 | DROP -> DROP | REPRESENTED same-dest | F1 member V5-D5 Shadow Resume (V5:353-374; HL2, haiku isolated canary)
406. VL-21-406 | DROP -> DROP | REPRESENTED same-dest | F2 member V5-D2 Axis-Flip Relay (V5:201-230): model-authored "I used axis X at ref R" turn
407. VL-21-407 | DROP -> DROP | REPRESENTED same-dest | F2 member V2-D3 Pattern Propagation Relay (V2:293-308; haiku + 2x luna; SendMessage; "the 
408. VL-21-408 | DROP -> DROP | REPRESENTED same-dest | F3 member V1-R1 Coverage board (V1:148-170): which task x move cells have been run, gaps a
409. VL-21-409 | DROP -> DROP | REPRESENTED same-dest | F3 member V2-D4 Coverage-Matrix Steering (V2:355-375; SL2): Task x move cells
410. VL-21-410 | DROP -> DROP | REPRESENTED same-dest | F3 member V3-R1 Sweep Relay
411. VL-21-411 | DROP -> DROP | REPRESENTED same-dest | F3 member V3-R2 Move-Hint Board
412. VL-21-412 | DROP -> DROP | REPRESENTED same-dest | F3 member V3-R5 Coverage Claims
413. VL-21-413 | DROP -> DROP | REPRESENTED same-dest | F3 member V4-1 Move Radar (V4:188-217; telemetry)
414. VL-21-414 | DROP -> DROP | REPRESENTED same-dest | F3 member V5-D4 Exit Ticket (V5:313-332), with a Stop block
415. VL-21-415 | DROP -> DROP | REPRESENTED same-dest | F4 member V1-R2 Evidence trail (V1:235-256; haiku + 2x luna; automatic harvest)
416. VL-21-416 | DROP -> DROP | REPRESENTED same-dest | F4 member V2-D1 Frontier Relay (V2:151-172)
417. VL-21-417 | DROP -> DROP | REPRESENTED same-dest | F4 member V3-R3 Capped Sweep Specialist (extra sonnet, 130 s timeout)
418. VL-21-418 | DROP -> DROP | REPRESENTED same-dest | F4 member V4-2 Idle-Shift Sweeper (V4:274-293)
419. VL-21-419 | DROP -> DROP | REPRESENTED same-dest | F4 member V5-D3 Sweep Desk (V5:267-286; ember kept alive by a Stop poll until 95 s)
420. VL-21-420 | DROP -> DROP | REPRESENTED same-dest | F5 member V1-R4 Scout and split (V1:380-402): fact-only inventory of plan and source sente
421. VL-21-421 | DROP -> DROP | REPRESENTED same-dest | F5 member V5-D1 Claim-Index Relay (V5:157-175)
422. VL-21-422 | DROP -> DROP | REPRESENTED same-dest | F5 member V2-D5 Source-Rule Witness (V2:422-436; ember + luna + sonnet S14 225 s; aimed at
423. VL-21-423 | DROP -> DROP | REPRESENTED same-dest | F6 member V1-R5 Sentinel requests (V1:448-467; SendMessage)
424. VL-21-424 | DROP -> DROP | REPRESENTED same-dest | F6 member V4-5 Coverage Deflection (V4:539-565; harness-generated counts from finished blo
425. VL-21-425 | DROP -> DROP | REPRESENTED same-dest | F7 member V3-R4 Challenge Pair (SendMessage)
426. VL-21-426 | DROP -> DROP | REPRESENTED same-dest | F7 member V4-4 Flag-and-Adjudicate (V4:461-485; ember + luna S13 100 s; Stop hold)
427. VL-21-427 | KNOWLEDGE -> KNOWLEDGE | REPRESENTED same-dest | Diff analysis found 16 arithmetic or internal-consistency errors: 8 gain tables, 1 time bu
428. VL-21-428 | DROP -> DROP | REPRESENTED same-dest | E1 (V1-R2): I7 control high 0.35 exceeds the stated chain 0.45 x 0.7 x 0.85 = 0.27; hash-s
429. VL-21-429 | DROP -> DROP | REPRESENTED same-dest | E2 (V1-R3): the cap is 1.35 x T1 of the same run (V1:323), not 1.35 x the named S07 baseli
430. VL-21-430 | DROP -> DROP | REPRESENTED same-dest | E3 (V1-R4): rows sum low 0.12 minus displacement 0.10 = 0.02, high 0.60, not the stated C 
431. VL-21-431 | DROP -> DROP | REPRESENTED same-dest | E4 (V2-D1): "luna stops at 135 s or later gets none" but the formula gives 0 from t=128 s;
432. VL-21-432 | DROP -> DROP | REPRESENTED same-dest | E5 (V2-D2): I5 row high 0.25 needs both lunas to receive the same ember anchor (single lun
433. VL-21-433 | DROP -> DROP | REPRESENTED same-dest | E6 (V2-D5): B5 chain 0.2-0.4 x 0.3-0.6 = 0.06-0.24, stated 0.04-0.20 (diff-analysis.md:84)
434. VL-21-434 | DROP -> DROP | REPRESENTED same-dest | E7 (V3-R1..R4): gains do not follow inputs: R1 5 x 0.6-0.9 x 0.15-0.4 = 0.45-1.8 stated 0.
435. VL-21-435 | KNOWLEDGE -> KNOWLEDGE | REPRESENTED same-dest | E8 (V4-2): typical "142 s" omits the 6 s seal turn: 116+6+26 = 148 s (+27.6%); worst case 
436. VL-21-436 | EVAL -> EVAL | REPRESENTED same-dest | E9 (V5 adoption rule): "at least 4 runs against at most 1 for A2 (Fisher p <= 0.10)" recom
437. VL-21-437 | KNOWLEDGE -> KNOWLEDGE | REPRESENTED same-dest | Grid totals (diff analysis): time arithmetic correct and against a named baseline in 19 of
438. VL-21-438 | KNOWLEDGE -> KNOWLEDGE | REPRESENTED same-dest | Structural difference S-001 (read from diff-analysis.md at the tip, not enumerated in the 
439. VL-21-439 | KNOWLEDGE -> KNOWLEDGE | REPRESENTED same-dest | Structural difference S-002 (diff-analysis.md, not enumerated in the slice): the shared sc
440. VL-21-440 | KNOWLEDGE -> KNOWLEDGE | REPRESENTED same-dest | Structural difference S-003 (diff-analysis.md): theory section layout differs (V2 three-ga
441. VL-21-441 | EVAL -> EVAL | REPRESENTED same-dest | Structural difference S-004 (diff-analysis.md): comparison table columns differ; only V2 a
442. VL-21-442 | KNOWLEDGE -> KNOWLEDGE | REPRESENTED same-dest | Structural difference S-005 (diff-analysis.md): requirement format and count differ (V1 ab
443. VL-21-443 | KNOWLEDGE -> KNOWLEDGE | REPRESENTED same-dest | Structural difference S-006 (diff-analysis.md): closing "not checked" list present in V1, 
444. VL-21-444 | KNOWLEDGE -> KNOWLEDGE | REPRESENTED same-dest | C-001 (T1 refinement positions): V1 two halves held by different models, so searcher-to-re
445. VL-21-445 | KNOWLEDGE -> KNOWLEDGE | REPRESENTED same-dest | C-002 (T2/T3 positions): V5 splits T2a/T2b (changes which designs can reach B1/B2/I4); V4 
446. VL-21-446 | KNOWLEDGE -> KNOWLEDGE | REPRESENTED same-dest | C-003 (harness-fix bundle positions): V1 H1-H4 (truncate 200/300 + parser + re-ask once); 
447. VL-21-447 | KNOWLEDGE -> KNOWLEDGE | REPRESENTED same-dest | C-004 (move catalogue numbering): same moves, different ids (M1 = stopping rule in V1/V3, 
448. VL-21-448 | KNOWLEDGE -> KNOWLEDGE | REPRESENTED same-dest | C-005 (schema positions): `panel-msg/1` in V1/V2/V4; V3 per-design JSON 240-char lines; V5
449. VL-21-449 | KNOWLEDGE -> KNOWLEDGE | REPRESENTED same-dest | C-006 (independent first pass): V1 6 tool calls AND own first card; V2 natural seal at fir
450. VL-21-450 | EVAL -> EVAL | REPRESENTED same-dest | C-007 (convergence alarm positions): V1 J > ref + 0.15 OR distinct tasks -20% OR echo > 50
451. VL-21-451 | EVAL -> EVAL | REPRESENTED same-dest | C-008 (gain method positions): V5 sum over moves of P(executed) x c with low = 0.25 x cent
452. VL-21-452 | KNOWLEDGE -> KNOWLEDGE | REPRESENTED same-dest | C-009 (gain split positions): V1 collaboration + harness; V2 C + H + within-run C (final m
453. VL-21-453 | KNOWLEDGE -> KNOWLEDGE | REPRESENTED same-dest | C-010 (first-experiment positions): V1 A1-A4 6 runs each = 24 panel runs (216 reviewer run
454. VL-21-454 | EVAL -> EVAL | REPRESENTED same-dest | C-011 (endpoint and adoption positions): V1 found /14 +0.5 (permutation p<=0.10) OR reach 
455. VL-21-455 | KNOWLEDGE -> KNOWLEDGE | REPRESENTED same-dest | C-013 (+35% enforcement positions): V1 finish signal T0 + 1.20 x B and kill phase 2 at 1.3
456. VL-21-456 | EVAL -> EVAL | REPRESENTED same-dest | X-001 (harness-fix share, found /14 per run, cheap panel): V1 +0.2 to +0.5 (H1 +0.0 to 0.1
457. VL-21-457 | DROP -> DROP | REPRESENTED same-dest | X-002 (effect of removing the `.dev/reflect` leak): V3 counts it as a "+0 to +0.1" gain ag
458. VL-21-458 | DROP -> DROP | REPRESENTED same-dest | X-003 (which defect `merge_guard.py:256` repairs): V1, V2, V4, V5 say GT6 = I1; V3 wrongly
459. VL-21-459 | KNOWLEDGE -> KNOWLEDGE | REPRESENTED same-dest | X-004 (whether haiku may be used): V3 excludes haiku ("break the +35% cap") yet adds sonne
460. VL-21-460 | DROP -> DROP | REPRESENTED same-dest | X-005 (116 s baseline decomposition): V3 says luna is 102 s so about 14 s is "fixed harnes
461. VL-21-461 | CORE -> CORE | REPRESENTED same-dest | X-006 (where collaboration findings go for the merge): V3 requirement 6 puts them "outside
462. VL-21-462 | DROP -> DROP | REPRESENTED same-dest | X-007 (free text in messages): V1/V2/V3/V4 forbid it; V5 allows `note` up to 120 chars fil
463. VL-21-463 | DROP -> DROP | REPRESENTED same-dest | X-008 (changing grading or judge in every arm): V5 H-4 (MINOR notes) and H-6 are rubric/ju
464. VL-21-464 | DROP -> DROP | REPRESENTED same-dest | X-009 (anchor/claim length-drop fix): V1 truncate 200/300 + validate + re-ask; V2 normaliz
465. VL-21-465 | EVAL -> EVAL | REPRESENTED same-dest | X-010 (value of exchange over a static move list): V3 has no static arm and R1 worth 0.4-1
466. VL-21-466 | EVAL -> EVAL | REPRESENTED same-dest | X-011 (can anchor-based designs reach B1/B2): same data (52% task-level vs 0% AC-level anc
467. VL-21-467 | DROP -> DROP | REPRESENTED same-dest | X-012 (I7 counted on /14): V3 lists I7 as a target of "issues of 14 per run" in R1, R3, R5
468. VL-21-468 | EVAL -> EVAL | REPRESENTED same-dest | X-013 (statistical thresholds): V1 "3 of 6 vs 0 of 6" p<=0.10 recomputed 0.091 holds; V2 "
469. VL-21-469 | DROP -> DROP | REPRESENTED same-dest | U-001 (V1): panel-wide deadline `PANEL_FINISH_AT = T0 + 1.20 x B`, after which the hook in
470. VL-21-470 | EVAL -> EVAL | REPRESENTED same-dest | U-002 (V1): fully automatic evidence trail (send and receive need no model action; paths h
471. VL-21-471 | DROP -> DROP | REPRESENTED same-dest | U-003 (V1): kill phase 2 at 1.35 x T1 - 2 s and fall back to the phase-1 report; Medium
472. VL-21-472 | DROP -> DROP | REPRESENTED same-dest | U-004 (V2): three-gate funnel with a per-issue gate table; Medium
473. VL-21-473 | DROP -> DROP | REPRESENTED same-dest | U-005 (V2): decoy challenges (1 of 3 at a place no peer flagged) so a receiver cannot infe
474. VL-21-474 | DROP -> DROP | REPRESENTED same-dest | U-006 (V2): within-run attribution by judging the merged sealed phase-1 reports separately
475. VL-21-475 | DROP -> DROP | REPRESENTED same-dest | U-007 (V2): pointer-following evidence: luna read source.md in 48/48 control runs vs 11/48
476. VL-21-476 | DROP -> DROP | REPRESENTED same-dest | U-008 (V2): propagation design D3, the only peer-discovered trigger for I6; Medium
477. VL-21-477 | DROP -> DROP | REPRESENTED same-dest | U-009 (V3): 12-character substring leak check (no board line may contain a 12+ char substr
478. VL-21-478 | EVAL -> EVAL | REPRESENTED same-dest | U-010 (V3): extension rule (10 to 20 runs when the effect is +0.5 to +1.0) and second-judg
479. VL-21-479 | DROP -> DROP | REPRESENTED same-dest | U-011 (V4): kill switch `PANEL_COLLAB=0` with a byte-identical launch command, per-package
480. VL-21-480 | DROP -> DROP | REPRESENTED same-dest | U-012 (V4): Move Radar, moves inferred from tool-call telemetry with zero model authoring 
481. VL-21-481 | DROP -> DROP | REPRESENTED same-dest | U-013 (V4): absolute board path and reviewer id baked into hook command strings so nothing
482. VL-21-482 | DROP -> DROP | REPRESENTED same-dest | U-014 (V4): surface-finding filter so luna's Task 12 artifact objection does not mark Task
483. VL-21-483 | DROP -> DROP | REPRESENTED same-dest | U-015 (V5): per-move credit probability c (sum 1.04, a ceiling set to SL2's measured hard 
484. VL-21-484 | DROP -> DROP | REPRESENTED same-dest | U-016 (V5): haiku kept isolated as an in-run canary with phase 2 run in the slow member's 
485. VL-21-485 | DROP -> DROP | REPRESENTED same-dest | U-017 (V5): first-hand evidence rule: a peer fact is citable only if the receiver's own tr
486. VL-21-486 | DROP -> DROP | REPRESENTED same-dest | U-018 (V5): Spike 5, re-score the 30 cheap runs with the normalizer (judge calls only) to 
487. VL-21-487 | HARNESS -> HARNESS | REPRESENTED same-dest | U-018 detail (diff-analysis.md at the tip): V5 verified `--max-turns` is absent and `--inc
488. VL-21-488 | DROP -> DROP | REPRESENTED same-dest | A-001: hook-injected `additionalContext` or Stop reasons change what a gateway model does 
489. VL-21-489 | EVAL -> EVAL | REPRESENTED same-dest | A-002: idle time of faster reviewers is free capacity; CONTRADICTED by V5: the static kit 
490. VL-21-490 | EVAL -> EVAL | REPRESENTED same-dest | A-003: the blind Opus judge is comparable across arms; UNSTATED; no variant controls "more
491. VL-21-491 | DROP -> DROP | REPRESENTED same-dest | A-004: harness and collaboration shares add linearly; CONTRADICTED by V4's own dependency 
492. VL-21-492 | DROP -> DROP | REPRESENTED same-dest | A-005: per-package baseline = three-package total / 3; STATED (V2, V5) / UNSTATED (V1, V4)
493. VL-21-493 | EVAL -> EVAL | REPRESENTED same-dest | A-006: content-free pointers carry no conclusion; CONTRADICTED: only V2 defends against th
494. VL-21-494 | DROP -> DROP | REPRESENTED same-dest | A-007: `--resume` restores phase-1 context and keeps the gateway model; STATED (spikes); M
495. VL-21-495 | DROP -> DROP | REPRESENTED same-dest | A-008: reviewers stay read-only although board designs write via a Bash helper; UNSTATED i
496. VL-21-496 | DROP -> DROP | REPRESENTED same-dest | A-009: the move catalogue generalises beyond three packages; STATED; Medium; landed as 2 n
497. VL-21-497 | MODULE-tasklist -> MODULE-tasklist | REPRESENTED same-dest | A-010: ember + 2x luna is the right base panel; STATED by all five; Low
498. VL-21-498 | DROP -> DROP | REPRESENTED same-dest | A-011: cheap-model conversion rates for never-executed moves lie between near-miss rates a
499. VL-21-499 | KNOWLEDGE -> KNOWLEDGE | REPRESENTED same-dest | Diff-analysis summary (S6.8): structural 6, content 13, contradictions 13, shared assumpti
500. VL-21-500 | KNOWLEDGE -> KNOWLEDGE | REPRESENTED same-dest | Merge implication (S6.8): take one design per family (F1, F3, F4, F5 or F2, F6 or F7), eac
501. VL-21-501 | KNOWLEDGE -> KNOWLEDGE | REPRESENTED same-dest | Debate round 1 (S7.1.1, round1-tally.md:1): 5 advocates, need 4 of 5, agreed 37/43, conver
502. VL-21-502 | KNOWLEDGE -> KNOWLEDGE | REPRESENTED same-dest | Round 1 base vote (S7.1.2, round2-agenda.md:4): "Base document: all five advocates propose
503. VL-21-503 | KNOWLEDGE -> KNOWLEDGE | REPRESENTED same-dest | Round 2 (S7.1.3, round2-tally.md:1): 43/43 convergence 1.000, with X-011, A-007 and A-011 
504. VL-21-504 | KNOWLEDGE -> KNOWLEDGE | REPRESENTED same-dest | Round 2.5 invariant probe (S7.1.4, invariant-probe.md:1-84): "CONVERGENCE BLOCKED_BY_INVAR
505. VL-21-505 | KNOWLEDGE -> KNOWLEDGE | REPRESENTED same-dest | Round 3 (S7.1.5, round3-tally.md:1, 51-62): 43/43 = 1.000; all 8 HIGH closed (INV-001 5/5 
506. VL-21-506 | DROP -> DROP | REPRESENTED same-dest | Round 3 open point (S7.1.6): central k for F3/F4/F7 rows: V1 k=2, V2..V5 k=1; settled "k =
507. VL-21-507 | DROP -> DROP | REPRESENTED same-dest | Round 3 open point (S7.1.6): F3 injections name a move only (adopted 4/5; V1 did not objec
508. VL-21-508 | KNOWLEDGE -> KNOWLEDGE | REPRESENTED same-dest | Round 3 open point (S7.1.6): keep F6 versus replace it with F2: keep F6, 5/5
509. VL-21-509 | KNOWLEDGE -> KNOWLEDGE | REPRESENTED same-dest | Round 3 open point (S7.1.6): V4's run-reviewer.sh rules (elapsed sums attempts, attempt 2 
510. VL-21-510 | DROP -> DROP | REPRESENTED same-dest | Debate wall time (S7.1.7): first session 5400 s timeout in Round 3; resume 3262 s
511. VL-21-511 | KNOWLEDGE -> KNOWLEDGE | REPRESENTED same-dest | Round 2 slate dispute (1): Slot 5 F5 structural index/source-rule witness (V1, V2, V5) ver
512. VL-21-512 | KNOWLEDGE -> KNOWLEDGE | REPRESENTED same-dest | Round 2 dispute (2): F1 core V4-3 (V1, V2, V3, V5) versus V2-D2 (V4); grafts V2-D2 decoys,
513. VL-21-513 | KNOWLEDGE -> KNOWLEDGE | REPRESENTED same-dest | Round 2 dispute (3): F4 core and worst-case fix: V1 153.6 s (+32.4%, natural seal at first
514. VL-21-514 | KNOWLEDGE -> KNOWLEDGE | REPRESENTED same-dest | Round 2 dispute (4): F3 grafts: V2-D4 Task x move cells versus V1-R1 region x move; V5-D4 
515. VL-21-515 | KNOWLEDGE -> KNOWLEDGE | REPRESENTED same-dest | Round 2 dispute (5): F6 re-based to sonnet + 2x luna (unanimous); disputed whether the har
516. VL-21-516 | KNOWLEDGE -> KNOWLEDGE | REPRESENTED same-dest | Round 2 dispute (6): experiment comparator and sizes
517. VL-21-517 | KNOWLEDGE -> KNOWLEDGE | REPRESENTED same-dest | Round 2 dispute (7): harness share figure and the H-4 exclusion
518. VL-21-518 | KNOWLEDGE -> KNOWLEDGE | REPRESENTED same-dest | Round 2 dispute (8): idle-time budgets versus assumption A-002
519. VL-21-519 | EVAL -> EVAL | REPRESENTED same-dest | Orchestrator-measured elapsed (S7.1.9, round3-agenda.md:7-18): source is `.dev/eval-worksp
520. VL-21-520 | EVAL -> EVAL | REPRESENTED same-dest | Ember + 2x luna (g1-*, e2-ember-luna2-rep): designSpec 5 runs median 100 s (92-123), alias
521. VL-21-521 | EVAL -> EVAL | REPRESENTED same-dest | Ember + luna (g9-*): designSpec 4 runs median 79 s (61-121), alias 4 runs 114 (103-130), c
522. VL-21-522 | EVAL -> EVAL | REPRESENTED same-dest | Haiku + 2x luna (g7-*): designSpec 4 runs 220 s (159-305), alias 4 runs 238 (230-285), con
523. VL-21-523 | EVAL -> EVAL | REPRESENTED same-dest | "The designSpec median (100 s) and single runs (86-98 s) sit near or below the 97.1 s floo
524. VL-21-524 | EVAL -> EVAL | REPRESENTED same-dest | INV-001 (HIGH): the consensus said "worst 150.0 s" for F4/F7 and F3 "worst = expected" ass
525. VL-21-525 | DROP -> DROP | REPRESENTED same-dest | INV-002 (HIGH): the H2 re-ask is inside no time bound (resume after the report is written;
526. VL-21-526 | EVAL -> EVAL | REPRESENTED same-dest | INV-003 (HIGH): F1 n uses the MEAN luna turn 6.4 s which leaves 3.2 s slack, a timeout dis
527. VL-21-527 | DROP -> DROP | REPRESENTED same-dest | INV-004 (HIGH): the shared relative convergence alarm is biased against F1/F7 because in F
528. VL-21-528 | EVAL -> EVAL | REPRESENTED same-dest | INV-005 (HIGH): "A5 (F7) vs A4 (F4) differs in message content only" is FALSE: F4's sender
529. VL-21-529 | DROP -> DROP | REPRESENTED same-dest | INV-006 (HIGH): F6 and F3 are one mechanism on two panels (the test used to evict F5 appli
530. VL-21-530 | DROP -> DROP | REPRESENTED same-dest | INV-007 (HIGH): the F3 classifier observes only tool-call signatures (M1, M7, source.md op
531. VL-21-531 | DROP -> DROP | REPRESENTED same-dest | INV-008 (HIGH): F3/F4/F7 add FIXED costs (2 x 2 turns + 2 s hooks + 6.4 s slip); the cap h
532. VL-21-532 | DROP -> DROP | REPRESENTED same-dest | INV-009 (MEDIUM): A1 launch command is byte-identical to today's `RR:48` but the H2 re-ask
533. VL-21-533 | DROP -> DROP | REPRESENTED same-dest | INV-010 (MEDIUM): `<rid>.p1.md` is hashed at phase-1 exit but the H2 re-ask happens after 
534. VL-21-534 | DROP -> DROP | REPRESENTED same-dest | INV-011 (MEDIUM): the shared sandbox `/tmp/evalsb/<pkg>/repo` across up to 10 concurrent r
535. VL-21-535 | DROP -> DROP | REPRESENTED same-dest | INV-012 (MEDIUM): the snapshot holds no findings lines (luna writes one block at the end),
536. VL-21-536 | DROP -> DROP | REPRESENTED same-dest | INV-013 (MEDIUM): F1 zero-anchor digest versus gap card p=1/3 undefined; if every trigger-
537. VL-21-537 | DROP -> DROP | REPRESENTED same-dest | INV-014 (MEDIUM): the gap card is harness extraction, i.e. a prompting share, not collabor
538. VL-21-538 | DROP -> DROP | REPRESENTED same-dest | INV-015 (MEDIUM): the F4 sweeper starts at about 41 s with an absolute timeout T0+85 s; H1
539. VL-21-539 | EVAL -> EVAL | REPRESENTED same-dest | INV-016 (MEDIUM): a count fact n=0 acts as clearance; luna makes about 1 Bash call per run
540. VL-21-540 | DROP -> DROP | REPRESENTED same-dest | INV-017 (MEDIUM): the F7 gain factor "sentence among ember's 4 cards 0.3-0.5" has no selec
541. VL-21-541 | DROP -> DROP | REPRESENTED same-dest | INV-018 (MEDIUM): an F7 alarm action that adds a gap-card decoy mid-arm changes the treatm
542. VL-21-542 | DROP -> DROP | REPRESENTED same-dest | INV-019 (MEDIUM): decision rules assume A1 reach 0 but H is 0.03-0.34 /14 so A1 reach is a
543. VL-21-543 | DROP -> DROP | REPRESENTED same-dest | INV-020 (MEDIUM): stage 2 F6 on SL2 with the same reach endpoint saturates (SL2 reached I7
544. VL-21-544 | DROP -> DROP | REPRESENTED same-dest | INV-021 (MEDIUM): the F6 gain 0.26-1.06 was derived on S14 (ember + luna scouts, covered-c
545. VL-21-545 | DROP -> DROP | REPRESENTED same-dest | INV-022 (LOW): F1 n is unclamped (can be negative)
546. VL-21-546 | DROP -> DROP | REPRESENTED same-dest | INV-023 (LOW): a hash split of 4 items over 2 lunas can be 3/1; use a balanced seeded deal
547. VL-21-547 | DROP -> DROP | REPRESENTED same-dest | INV-024 (ADDRESSED): hook env inheritance replaced by per-reviewer `--settings` JSON
548. VL-21-548 | DROP -> DROP | REPRESENTED same-dest | INV-025 (ADDRESSED): witness content only in F4
549. VL-21-549 | DROP -> DROP | REPRESENTED same-dest | INV-026 (ADDRESSED): luna ends before delivery, so late items are dropped
550. VL-21-550 | DROP -> DROP | REPRESENTED same-dest | INV-027 (ADDRESSED): HL2 variant timing mislabel (290 s, +21.8% was V4's haiku-challenge s
551. VL-21-551 | DROP -> DROP | REPRESENTED same-dest | INV-028 (ADDRESSED): H and C additive (conceded; separate columns)
552. VL-21-552 | DROP -> DROP | REPRESENTED same-dest | INV-029 (ADDRESSED): four arms each at p<0.05 give familywise 0.20; confirmation on two ne
553. VL-21-553 | DROP -> DROP | REPRESENTED same-dest | INV-030 (ADDRESSED): baseline per package versus per three packages
554. VL-21-554 | DROP -> DROP | REPRESENTED same-dest | INV-031 (ADDRESSED): seals fail closed, hooks fail open
555. VL-21-555 | DROP -> DROP | REPRESENTED same-dest | INV-032 (ADDRESSED): F1 C is a single value 0.06-0.73 (C-002 + X-011: B1, B2, I4 only thro
556. VL-21-556 | KNOWLEDGE -> KNOWLEDGE | REPRESENTED same-dest | INV-033 (ADDRESSED): arithmetic recomputed, all match
557. VL-21-557 | EVAL -> EVAL | REPRESENTED same-dest | Probe sufficiency note (invariant-probe.md:84): the +35% claims for F3, F4, F6 and F7 have
558. VL-21-558 | KNOWLEDGE -> KNOWLEDGE | REPRESENTED same-dest | Quant layer (S7.4.1, 50% weight): 36 brief requirements matched by regex in `scoring/quant
559. VL-21-559 | KNOWLEDGE -> KNOWLEDGE | REPRESENTED same-dest | Qual layer (S7.4.2, 50%): additive binary rubric, 30 criteria in 6 dimensions (CP, CR, ST,
560. VL-21-560 | KNOWLEDGE -> KNOWLEDGE | REPRESENTED same-dest | Combined scores (S7.4.3): V1 0.9445 (debate points won 12 of 43), V2 0.9355 (8), V3 0.8357
561. VL-21-561 | KNOWLEDGE -> KNOWLEDGE | REPRESENTED same-dest | Tiebreak (S7.4.4): margin V4 vs V5 = 0.033, under the 5% threshold, so the tiebreaker appl
562. VL-21-562 | KNOWLEDGE -> KNOWLEDGE | REPRESENTED same-dest | V4 weaknesses repaired in the debate (S7.4.5): planned-path figures labelled "worst", addi
563. VL-21-563 | KNOWLEDGE -> KNOWLEDGE | REPRESENTED same-dest | Strengths preserved or incorporated (S7.4.6): from V4 the (a)-(h) layout with runbooks, bo
564. VL-21-564 | KNOWLEDGE -> KNOWLEDGE | REPRESENTED same-dest | Rubric weakness (S7.4.7): RK1 (3 risks with probability and impact) NOT MET for all five v
565. VL-21-565 | HARNESS -> HARNESS | REPRESENTED same-dest | Scoring scripts (S7.4.8): `scoring/quant.py` (3962 B), `reconcile.py` (1344 B), `final_qua
566. VL-21-566 | DROP -> DROP | REPRESENTED same-dest | Merge-review verdict history (S7.5.1, merge-review.md:6, 81, 89): FAIL (2 blocking), re-re
567. VL-21-567 | KNOWLEDGE -> KNOWLEDGE | REPRESENTED same-dest | Merge-review checks R1-R8 (S7.5.2): R1-R6 and R8 PASS; R7 (no internal contradiction in a 
568. VL-21-568 | EVAL -> EVAL | REPRESENTED same-dest | Blocking 1 (S7.5.3): L194 "No gain row in this specification exceeds it" was false: F7 B1 
569. VL-21-569 | DROP -> DROP | REPRESENTED same-dest | Blocking 2 (S7.5.4): the F6 slowdown limit used W = 56 s (omits 2 s hooks); the correct W 
570. VL-21-570 | KNOWLEDGE -> KNOWLEDGE | REPRESENTED same-dest | Minor note M1 (not applied, S7.5.5): F3 and F6 lack the inline "theory addressed" line
571. VL-21-571 | EVAL -> EVAL | REPRESENTED same-dest | Minor note M2 (not applied): "4 of the 9 target issues masked" versus ten missed issues (9
572. VL-21-572 | KNOWLEDGE -> KNOWLEDGE | REPRESENTED same-dest | Minor note M3 (not applied): "only bound enforced by a kill" should read "only +35%-relate
573. VL-21-573 | KNOWLEDGE -> KNOWLEDGE | REPRESENTED same-dest | Minor note M4 (not applied): the brief's "at most 35%" is met on the planned path only; mi
574. VL-21-574 | EVAL -> EVAL | REPRESENTED same-dest | Minor note M5 (not applied): "1 package in 12" has an ambiguous denominator (12 runs x 3 p
575. VL-21-575 | EVAL -> EVAL | REPRESENTED same-dest | Minor note M6 (not applied): F3's B6 route uses M2 (L437) but the issue-to-theory table ma
576. VL-21-576 | KNOWLEDGE -> KNOWLEDGE | REPRESENTED same-dest | Minor note M7 (not applied): redesign numbers (1-5) differ from slot order (3, 2, 1, 5, 4)
577. VL-21-577 | EVAL -> EVAL | REPRESENTED same-dest | Minor note M8 (not applied): CONVERGENCE for F1 cannot detect phase-2 convergence (ECHO co
578. VL-21-578 | KNOWLEDGE -> KNOWLEDGE | REPRESENTED same-dest | Arithmetic reconfirmed by the merge review (S7.5.6): 348/3 = 116 s; 821/3 = 273.7; 715/3 =
579. VL-21-579 | DROP -> DROP | REPRESENTED same-dest | Brief constraint check R8 (S7.5.7): "No Opus reviewer: 'opus' appears only in provenance c
580. VL-21-580 | DROP -> DROP | REPRESENTED same-dest | Debate transcript metadata (S7.6.1): depth deep; 3 rounds plus the Round 2.5 probe; conver
581. VL-21-581 | KNOWLEDGE -> KNOWLEDGE | REPRESENTED same-dest | V1 advocate position (S7.6.2): one shared substrate (board, digest, catalogue, schema, dea
582. VL-21-582 | DROP -> DROP | REPRESENTED same-dest | V1 concessions (S7.6.3): V1-R2 I7 high end 0.35 stated vs chain 0.268 (correct 0.16-0.27);
583. VL-21-583 | KNOWLEDGE -> KNOWLEDGE | REPRESENTED same-dest | V2 advocate position (S7.6.4): supplies the theory spine (three-gate funnel), decoys, attr
584. VL-21-584 | DROP -> DROP | REPRESENTED same-dest | V3 advocate concessions (S7.6.5): V3 "is the weakest scaffold of the five"; concedes 10 po
585. VL-21-585 | KNOWLEDGE -> KNOWLEDGE | REPRESENTED same-dest | V3 integrity controls the others adopted (S7.6.5): sealed first-pass artifact, cross-revie
586. VL-21-586 | KNOWLEDGE -> KNOWLEDGE | REPRESENTED same-dest | V4 advocate position (S7.6.6): supplies scaffolding (kill switch, board path baked into ho
587. VL-21-587 | KNOWLEDGE -> KNOWLEDGE | REPRESENTED same-dest | V5 advocate position (S7.6.7): "V5's lasting contribution is... the accounting: each gain 
588. VL-21-588 | KNOWLEDGE -> KNOWLEDGE | REPRESENTED same-dest | Debate coverage (S7.6.8, debate-transcript.md:880-932): round-1 tally block; Round 2 rebut
589. VL-21-589 | DROP -> DROP | REPRESENTED same-dest | Refactor-plan decision (1) (S7.6.9, refactor-plan.md:11-18): the slate is exactly five, on
590. VL-21-590 | DROP -> DROP | REPRESENTED same-dest | Decision (2): V4's "A0" renamed A1; A0 = fresh current-harness arm; EL2 = ember + 2x luna 
591. VL-21-591 | DROP -> DROP | REPRESENTED same-dest | Decision (3): central k = 1, k = 2 optimistic (4/5); "V3's objection to plain halving, R3-
592. VL-21-592 | DROP -> DROP | REPRESENTED same-dest | Decision (4): F6 gain re-derivation: high = V4 rows 1.06 at k=2, low = V4 low x 0.5 = 0.13
593. VL-21-593 | DROP -> DROP | REPRESENTED same-dest | Decision (5): F3 C from ember search-move rows only (I4 0.05-0.20, I5 0.02-0.10, B8 0.03-0
594. VL-21-594 | DROP -> DROP | REPRESENTED same-dest | Decision (6): F4 C 0.14-0.67 becomes 0.07-0.34 at k=1; I7 0.17-0.50 becomes 0.09-0.25; F7 
595. VL-21-595 | DROP -> DROP | REPRESENTED same-dest | Changes NOT made (S7.6.10, refactor-plan.md:176-197), formats and schema: S-005 other vari
596. VL-21-596 | DROP -> DROP | REPRESENTED same-dest | Changes NOT made, independence and alarms: C-006 call-count gate rejected (no auditable ar
597. VL-21-597 | DROP -> DROP | REPRESENTED same-dest | Changes NOT made, estimates and arms: X-001 V3 0.8-2.1 rejected; X-006 V3 findings outside
598. VL-21-598 | EVAL -> EVAL | REPRESENTED same-dest | Changes NOT made, X-008: V5 H-4 and H-6 rejected, but "H-6 may be reported as a secondary 
599. VL-21-599 | DROP -> DROP | REPRESENTED same-dest | Changes NOT made, slate: slot 5 F5 rejected; INV-006 replace F6 with F2 rejected ("F2 diff
600. VL-21-600 | KNOWLEDGE -> KNOWLEDGE | REPRESENTED same-dest | Id mismatch: refactor-plan.md says `contradiction` to M7 but the merged spec says M8; the 
601. VL-21-601 | EVAL -> EVAL | REPRESENTED same-dest | Changes NOT made, INV-001 probe's `min(1.20 B, ...)` finish signal rejected: "Fires on the
602. VL-21-602 | DROP -> DROP | REPRESENTED same-dest | Changes NOT made, free text and mid-arm changes: INV-005 probe's finding form with ember's
603. VL-21-603 | DROP -> DROP | REPRESENTED same-dest | Changes NOT made, variant schedules: R2-V4:21 haiku-anchor variant rejected (+21.8%); R2-V
604. VL-21-604 | KNOWLEDGE -> KNOWLEDGE | REPRESENTED same-dest | Refactor risk summary (S7.6.11, refactor-plan.md:199-217): Change 8 (timing) and Change 11
605. VL-21-605 | KNOWLEDGE -> KNOWLEDGE | REPRESENTED same-dest | Merge log (S7.6.12, merge-log.md:1-10, 227-272): 22 of 22 changes applied (order 1, 8, 3, 
606. VL-21-606 | KNOWLEDGE -> KNOWLEDGE | REPRESENTED same-dest | Merge-log contradiction re-scan of key numbers: 116 s x39 always EL2 B; 143.6 s x10 always
607. VL-21-607 | KNOWLEDGE -> KNOWLEDGE | REPRESENTED same-dest | Merge-log: 4 new contradictions found and fixed (F6 Task-id items vs the path rule; F6 pee
608. VL-21-608 | EVAL -> EVAL | REPRESENTED same-dest | Investigation dataset (S8, investigation-patterns.md:3-9): 76 rows with era `source.md` fr
609. VL-21-609 | KNOWLEDGE -> KNOWLEDGE | REPRESENTED same-dest | Package short names: DS = `TASK-WF-designSpec-20261107-075614`, AL = `TASK-WF-makeTheAlias
610. VL-21-610 | EVAL -> EVAL | REPRESENTED same-dest | The sandbox exposes Read and Bash but NO Grep or Glob tool (`system/init` tool list in eve
611. VL-21-611 | EVAL -> EVAL | REPRESENTED same-dest | Tool-use profile, ember (S8.1 medians): 12 tool calls, 2 Read, 8 Bash, 0.0 MCP, 15 files t
612. VL-21-612 | EVAL -> EVAL | REPRESENTED same-dest | Tool-use profile, luna: 14 calls, 11 Read, 1 Bash, 1.6 MCP, 8 files, source.md 78%, test f
613. VL-21-613 | EVAL -> EVAL | REPRESENTED same-dest | Tool-use profile, haiku: 9 calls, 2 Read, 5 Bash, 0.0 MCP, 16 files, source.md 69%, test f
614. VL-21-614 | EVAL -> EVAL | REPRESENTED same-dest | Tool-use profile, sonnet: 15 calls, 2 Read, 12 Bash, 0.0 MCP, 17 files, source.md 99%, tes
615. VL-21-615 | EVAL -> EVAL | REPRESENTED same-dest | Tool-use profile, grok: 31 calls, 11.5 Read, 10 Bash, 8.8 MCP, 16 files, source.md 83%, te
616. VL-21-616 | EVAL -> EVAL | REPRESENTED same-dest | Tool-use profile, terra: 11.5 calls, 9 Read, 2 Bash, 0.5 MCP, 7 files, source.md 100%, tes
617. VL-21-617 | EVAL -> EVAL | REPRESENTED same-dest | Tool-use profile, wonder: 18 calls, 8.5 Read, 9.5 Bash, 0.0 MCP, 17.5 files, source.md 75%
618. VL-21-618 | EVAL -> EVAL | REPRESENTED same-dest | Method markers (S8.1): called the sc:spec-panel Skill: ember 1%, luna 84%, others 0% excep
619. VL-21-619 | EVAL -> EVAL | REPRESENTED same-dest | Method markers: recursive repo search ember 78%, luna 23%, haiku 92%, sonnet 96%, grok 92%
620. VL-21-620 | KNOWLEDGE -> KNOWLEDGE | REPRESENTED same-dest | Method markers: ran pytest ember 11%, luna 2%, haiku 20%, sonnet 22%; ran code/make/ruff e
621. VL-21-621 | EVAL -> EVAL | REPRESENTED same-dest | Plan-named versus unnamed files (S8.1, lines 41-49): unnamed files per run ember 0.8, luna
622. VL-21-622 | EVAL -> EVAL | REPRESENTED same-dest | Observation (S8.1, lines 51-55): luna "calls the sc:spec-panel Skill in 84% of runs; Skill
623. VL-21-623 | EVAL -> EVAL | REPRESENTED same-dest | Observation: haiku searches tests/ in 81% yet opened `test_worker_contract.py` in 0 of 25 
624. VL-21-624 | EVAL -> EVAL | REPRESENTED same-dest | Report profile, volume (S8.2): findings/run mean ember 4.19, luna 1.75, haiku 8.35, sonnet
625. VL-21-625 | EVAL -> EVAL | REPRESENTED same-dest | Report profile, blocking share: ember 14%, luna 72%, haiku 17%, sonnet 4%, grok 33%, terra
626. VL-21-626 | EVAL -> EVAL | REPRESENTED same-dest | Report profile, citation and shape: findings citing source.md ember 14%, luna 25%, haiku 9
627. VL-21-627 | CORE -> CORE | REPRESENTED same-dest | "Only 1% to 9% of findings put a repo file in `refs`" (line 71)
628. VL-21-628 | EVAL -> EVAL | REPRESENTED same-dest | Surface/process findings share: ember 21%, luna 23%, terra 18%, haiku 12%, wonder 13%, gro
629. VL-21-629 | EVAL -> EVAL | REPRESENTED same-dest | "On DE, 72 of luna's 212 findings (34%) are the Task 12 'artifact outside the edit scope' 
630. VL-21-630 | EVAL -> EVAL | REPRESENTED same-dest | Pairwise Jaccard of anchored Task sets (S8.3, lines 79-93; pairs, mean, zero-overlap): emb
631. VL-21-631 | EVAL -> EVAL | REPRESENTED same-dest | Run-to-run Jaccard of one model per package DS/AL/DE (line 95): ember 0.30/0.46/0.42; luna
632. VL-21-632 | EVAL -> EVAL | REPRESENTED same-dest | Concentration (lines 97-105): ember DS top-3 39% (T9 74%, T4 58%, T1 52%, T7 52%), DE 55% 
633. VL-21-633 | EVAL -> EVAL | REPRESENTED same-dest | Anchoring at ground-truth sites (lines 109-115): ember DS T1 52%, T9 74%, T8 33%, T4 58%, 
634. VL-21-634 | DROP -> DROP | REPRESENTED same-dest | "ember visits the right Tasks often (DS T1 52%, DS T2 46%) but on a different point; luna 
635. VL-21-635 | DROP -> DROP | REPRESENTED same-dest | Baselines ember+luna 0.25 and luna+luna 0.33 are the numbers behind the CONVERGENCE thresh
636. VL-21-636 | EVAL -> EVAL | REPRESENTED same-dest | Ground-truth proxy (S8.4, gtproxy.py): precision 0.71, recall 0.89 against 46 judged rows 
637. VL-21-637 | EVAL -> EVAL | REPRESENTED same-dest | Per-model proxy hit rates (S8.4): B3 DS T9 ember 65%, luna 10%, haiku 88%, sonnet 100%, gr
638. VL-21-638 | EVAL -> EVAL | REPRESENTED same-dest | I7 hand check (S8.4): 8 DE runs touched `test_worker_contract.py` (7 sonnet, 1 grok); 7 of
639. VL-21-639 | DROP -> DROP | REPRESENTED same-dest | I5 found by no reviewer of any model; `CHANGELOG.md` touched by 1 of 233 DS runs (line 134
640. VL-21-640 | EVAL -> EVAL | REPRESENTED same-dest | Judge-based attribution on the older subset (`EVAL/analysis/attrib.out`), GT items per run
641. VL-21-641 | EVAL -> EVAL | REPRESENTED same-dest | Theory A reasoning budget (S8.5): ember and luna stop early; Spearman 0.64 between median 
642. VL-21-642 | DROP -> DROP | REPRESENTED same-dest | Theory B search scope (S8.5): unnamed files touched sonnet 3.1, grok 1.2, haiku 0.9, ember
643. VL-21-643 | EVAL -> EVAL | REPRESENTED same-dest | Theory C report shape and grading (S8.5): the review prompt grades an unstated requirement
644. VL-21-644 | CORE -> CORE | REPRESENTED same-dest | Rubric location (S8.5 note): the review rubric lives in `~/.claude/rules/prompts/document_
645. VL-21-645 | KNOWLEDGE -> KNOWLEDGE | REPRESENTED same-dest | Reading of the theories (S8.5, line 167): luna B and C hold; ember C plus a flat A ceiling
646. VL-21-646 | EVAL -> EVAL | REPRESENTED same-dest | Investigation limits (S8.5, lines 169-174): "files touched" counts paths in Bash commands,
647. VL-21-647 | EVAL -> EVAL | REPRESENTED same-dest | designSpec scope (S9.1.1, investigation-designspec.md:5-12): candidate `EVAL/TASK-WF-desig
648. VL-21-648 | EVAL -> EVAL | REPRESENTED same-dest | Checkout-repaired confound (S9.1.2): the reviewers' repo `/tmp/evalsb/repo` HEAD `8c93e1d 
649. VL-21-649 | EVAL -> EVAL | REPRESENTED same-dest | GT1/B1 detail (S9.1.3): plan quote "The file lists every exact-text pin and line-content r
650. VL-21-650 | EVAL -> EVAL | REPRESENTED same-dest | GT2/B2 detail (S9.1.4): Task 1 names four target files for O3 (candidate.md:33) while AC3 
651. VL-21-651 | EVAL -> EVAL | REPRESENTED same-dest | GT5/B5 detail (S9.1.5): candidate.md:124 (Task 8 Exit report), :61 (Task 3 AC "no record a
652. VL-21-652 | EVAL -> EVAL | REPRESENTED same-dest | GT6/I1 detail (S9.1.6): candidate.md:56, :60, :61; source.md:200 (`settled(draft, skipped,
653. VL-21-653 | EVAL -> EVAL | REPRESENTED same-dest | GT9/I4 detail (S9.1.7): candidate.md:182 section named "Merge guard" versus the AC grep `m
654. VL-21-654 | EVAL -> EVAL | REPRESENTED same-dest | GT10/I5 detail (S9.1.8): candidate.md:49 (Task 2 AC3 grep limited to `models.py`, `run_log
655. VL-21-655 | EVAL -> EVAL | REPRESENTED same-dest | Effort profile designSpec (S9.1.9): ember n=39: 12 turns, 34 s, 11 tool calls, opened sour
656. VL-21-656 | EVAL -> EVAL | REPRESENTED same-dest | The 14 ember reports that never opened source.md are listed by id (line 79); e3-ember2-lun
657. VL-21-657 | DROP -> DROP | REPRESENTED same-dest | Near-miss census, GT10 area (S9.1.10): 16 findings (15 ember, 1 haiku g7-r4 F6) anchor the
658. VL-21-658 | EVAL -> EVAL | REPRESENTED same-dest | Near-miss census, GT1/GT2: "no finding in any row of any panel anchors O3 or AC3"; cheap a
659. VL-21-659 | EVAL -> EVAL | REPRESENTED same-dest | Near-miss census, GT5/GT6/GT9: GT5 area 3 findings (luna g6-r2/t4-1, luna g5-r4/t4-1, embe
660. VL-21-660 | EVAL -> EVAL | REPRESENTED same-dest | Who found GT5/GT6/GT9 (S9.1.11): GT5 by sonnet b4-sonnet-luna2 (S06) t1b-1 F7 (plan-vs-sou
661. VL-21-661 | EVAL -> EVAL | REPRESENTED same-dest | Finders spent 190-1005 s versus the cheap-panel median 34 s (ember) and 84 s (luna) (S9.1.
662. VL-21-662 | EVAL -> EVAL | REPRESENTED same-dest | GT10 was seen and DROPPED by grok n3-muse-luna-grok-src/t4-2 (S23) via `rg -n "len\(EventT
663. VL-21-663 | DROP -> DROP | REPRESENTED same-dest | "GT1 and GT2 were never approached by any reviewer in any row" (S9.1.11)
664. VL-21-664 | DROP -> DROP | REPRESENTED same-dest | GT1 hint (S9.1.12): move = stopping-rule test; hint "For each AC that says every/all/compl
665. VL-21-665 | DROP -> DROP | REPRESENTED same-dest | GT2 hint: compare Task 1's body (4 files) with AC3 and source O3 (2 files, source.md:341);
666. VL-21-666 | DROP -> DROP | REPRESENTED same-dest | GT5 hint: "trace another input", "highly plausible", "the strongest hint candidate in the 
667. VL-21-667 | DROP -> DROP | REPRESENTED same-dest | GT6 hint: "Check that every value guard_status reads is written by some row of the source 
668. VL-21-668 | DROP -> DROP | REPRESENTED same-dest | GT9 hint: a mechanical method hint, "highly plausible and cheap", "ember and luna can run 
669. VL-21-669 | DROP -> DROP | REPRESENTED same-dest | GT10 hint: a direction-flip hint
670. VL-21-670 | EVAL -> EVAL | REPRESENTED same-dest | NOTE (S9.1.12): several hints name tasks and files ("Task 1's open items O1 to O4", "sourc
671. VL-21-671 | CORE -> CORE | REPRESENTED same-dest | "Even if it is found, the severity rule in the prompt (Minor = note) may still drop it, as
672. VL-21-672 | EVAL -> EVAL | REPRESENTED same-dest | Cross-cutting cause 1 (S9.1.13): repo contamination: "Haiku and luna spent findings on 'th
673. VL-21-673 | DROP -> DROP | REPRESENTED same-dest | Cross-cutting cause 2: shallow source use by ember: "36% of ember reports never opened sou
674. VL-21-674 | DROP -> DROP | REPRESENTED same-dest | Cross-cutting cause 3: right anchor, wrong question: GT10 16x, GT5 3x, GT6 1x
675. VL-21-675 | CORE -> CORE | REPRESENTED same-dest | Cross-cutting cause 4: rubric framing: "'Implementer builds X wrong' does not surface unbo
676. VL-21-676 | EVAL -> EVAL | REPRESENTED same-dest | Alias/control scope and sandbox (S9.2.1, investigation-alias-control.md:3-9): cheap sets S
677. VL-21-677 | EVAL -> EVAL | REPRESENTED same-dest | B6 detail (S9.2.2; alias GT1; contradiction, blocking in implement, cost extra attempts 3 
678. VL-21-678 | EVAL -> EVAL | REPRESENTED same-dest | B8 detail (S9.2.3; alias GT3): Task 7 line 109 mandates the tiers.md sentence "issue worke
679. VL-21-679 | EVAL -> EVAL | REPRESENTED same-dest | I6 detail (S9.2.4; alias GT4; ambiguity, not blocking; "never found by any of 106 runs"): 
680. VL-21-680 | EVAL -> EVAL | REPRESENTED same-dest | I7 detail (S9.2.5; control GT1; missing task, not blocking, human acceptance): Tasks 2, 3 
681. VL-21-681 | EVAL -> EVAL | REPRESENTED same-dest | Aggregate tool use, cheap panels, per package, mean (S9.2.6): alias ember n=39 turns 16.8,
682. VL-21-682 | KNOWLEDGE -> KNOWLEDGE | REPRESENTED same-dest | Style summary (S9.2.6): luna is a Read-driven follower ("opens every file the candidate na
683. VL-21-683 | EVAL -> EVAL | REPRESENTED same-dest | Exposure without follow-up, I7 (S9.2.7): 6 of 98 cheap control reviewers had `test_worker_
684. VL-21-684 | EVAL -> EVAL | REPRESENTED same-dest | Exposure without follow-up, B8: 44 of 98 cheap alias reviewers saw the repaired `refs/tier
685. VL-21-685 | EVAL -> EVAL | REPRESENTED same-dest | Exposure without follow-up, B6: luna `g6-luna2-ember2-r3/t4-1` F2 graded MAJOR non-blockin
686. VL-21-686 | DROP -> DROP | REPRESENTED same-dest | Exposure without follow-up, I6: the sibling GT2 was raised by luna h1-r2 t4-1 (blocking), 
687. VL-21-687 | EVAL -> EVAL | REPRESENTED same-dest | Pattern (S9.2.8): "cheap reviewers check the plan line by line against the files and lines
688. VL-21-688 | EVAL -> EVAL | REPRESENTED same-dest | B6 finders (S9.2.9): 1 run `b4-terra-luna-muse` (S28, luna + terra + wonder): luna t4-1 F1
689. VL-21-689 | EVAL -> EVAL | REPRESENTED same-dest | B8 finder (S9.2.9): 1 run `g2-sonnet-ember-r3` (S16, ember + sonnet; ember block failed): 
690. VL-21-690 | EVAL -> EVAL | REPRESENTED same-dest | I7 finders (S9.2.9): 9 source.md-era runs, 8 sonnet + 1 grok (r3-luna2-grok-src S19); tabl
691. VL-21-691 | EVAL -> EVAL | REPRESENTED same-dest | Leak detail (S9.2.10): the sandbox is a `git archive` of HEAD minus `.dev/tasks/done`, `.d
692. VL-21-692 | CORE -> CORE | REPRESENTED same-dest | Cross-effort relevance (E1), S9.2.10: the reflect `.dev/reflect/` output directory is the 
693. VL-21-693 | DROP -> DROP | REPRESENTED same-dest | B6 hint (S9.2.11): "The Goal and Task 6 state an 'only X' rule and say a test enforces it.
694. VL-21-694 | DROP -> DROP | REPRESENTED same-dest | B8 hint: "For each such sentence ['only', 'all other'], list the files it quantifies over 
695. VL-21-695 | DROP -> DROP | REPRESENTED same-dest | I6 hint: "Someone found Task 6's mapping text conflicts with the Constraints. Check every 
696. VL-21-696 | DROP -> DROP | REPRESENTED same-dest | I7 hint: "Task 12 gates on a single test file. Grep `tests/` for the files Tasks 2, 3 and 
697. VL-21-697 | EVAL -> EVAL | REPRESENTED same-dest | Cross-cutting (S9.2.11, lines 157-160): "Three of four misses (B6, B8, I7) need the review
698. VL-21-698 | DROP -> DROP | REPRESENTED same-dest | "Reviewing against the plan's base commit would change what plan-vs-repo checks can find" 
699. VL-21-699 | KNOWLEDGE -> KNOWLEDGE | REPRESENTED same-dest | Transport option Orca agent mail (S10.1.1, research-light.md:14-66): a run is a durable na
700. VL-21-700 | KNOWLEDGE -> KNOWLEDGE | REPRESENTED same-dest | Transport option Claude Code agent teams (S10.1.2, research-light.md:73-80): experimental 
701. VL-21-701 | KNOWLEDGE -> KNOWLEDGE | REPRESENTED same-dest | Transport option subagents inside one session (S10.1.3, research-light.md:82-87): one lead
702. VL-21-702 | HARNESS -> HARNESS | REPRESENTED same-dest | Transport option cross-session SendMessage (S10.1.4, research-light.md:89-130): inbox sock
703. VL-21-703 | KNOWLEDGE -> KNOWLEDGE | REPRESENTED same-dest | Transport option A2A (S10.1.5, research-light.md:132-155): spec v1.0.0 "Latest Released Ve
704. VL-21-704 | MODULE-tasklist -> CORE | REPRESENTED moved(documented) | JSON board + PostToolUse hook detail (S10.1.6, research-light.md:157-207): board dir outsi
705. VL-21-705 | DROP -> DROP | REPRESENTED same-dest | Between-phase detail (S10.1.7, research-light.md:235-240): the harness collects each revie
706. VL-21-706 | KNOWLEDGE -> KNOWLEDGE | REPRESENTED same-dest | Transport comparison table (S10.1.8, research-light.md:211-221): 9 rows x 4 options (works
707. VL-21-707 | CORE -> CORE | REPRESENTED same-dest | Cross-effort note (S10.1): all transport design is for headless `claude -p` gateway review
708. VL-21-708 | HARNESS -> HARNESS | REPRESENTED same-dest | `pc-patterns/collect.py` (S10.2.1, 12,128 B): collects per-reviewer-run tool-use and repor
709. VL-21-709 | HARNESS -> HARNESS | REPRESENTED same-dest | `pc-patterns/analyze.py` (S10.2.2, 11,241 B): aggregates `records.json` into per-model tab
710. VL-21-710 | DROP -> DROP | REPRESENTED same-dest | `pc-patterns/gtproxy.py` (S10.2.3, 6,710 B): regex keyword proxy for per-reviewer ground-t
711. VL-21-711 | EVAL -> EVAL | REPRESENTED same-dest | gtproxy calibration (S10.2.3, `gt.md:1-20`): TP=116 FP=47 FN=14 (precision 0.71, recall 0.
712. VL-21-712 | EVAL -> EVAL | REPRESENTED same-dest | `pc-patterns/theory.py` (S10.2.4, 5,717 B) defect, [CODE-VERIFIED] by the slice at `theory
713. VL-21-713 | EVAL -> EVAL | REPRESENTED same-dest | theory.md:27 (S10.2.4): DE runs touching `test_worker_contract.py` 8, I7 proxy hit 7/8 ver
714. VL-21-714 | HARNESS -> HARNESS | REPRESENTED same-dest | `pc-patterns/rev.py` (S10.2.5, 2,126 B): recursive-search marker regexes `REC`, `DIRARG` (
715. VL-21-715 | EVAL -> EVAL | REPRESENTED same-dest | The merged M1 signature ("recursive grep over tests/ whose pattern is a path or key string
716. VL-21-716 | EVAL -> EVAL | REPRESENTED same-dest | `pc-patterns/how.py` (S10.2.6, 1,744 B): finds the first tool call containing `worker_cont
717. VL-21-717 | DROP -> DROP | REPRESENTED same-dest | `pc-patterns/sample.py` (S10.2.7, 907 B): seeded sample (`random.seed(1)`) of 2 runs per m
718. VL-21-718 | EVAL -> EVAL | REPRESENTED same-dest | Tables `surf.md` (414 B), `rev.md` (407 B), `gt.md` (2,331 B), `theory.md` (3,604 B), `out
719. VL-21-719 | EVAL -> EVAL | REPRESENTED same-dest | Skill-invocation table (S10.2.9, `theory.md:53-58`): luna called the sc:spec-panel Skill i
720. VL-21-720 | HARNESS -> HARNESS | REPRESENTED same-dest | Verified at the E2 tip (S10.3): `RR:48` is `cd /tmp/evalsb/repo && timeout 3000 claude -p 
721. VL-21-721 | CORE -> CORE | REPRESENTED same-dest | Verified at the E2 tip: `RR:50-52` filters (`select(.type=="result")`, `model_ok`, tokens;
722. VL-21-722 | DROP -> DROP | REPRESENTED same-dest | Verified at the E2 tip: `RR:61-64` retry loop re-runs the whole review on attempt 2 (`whil
723. VL-21-723 | CORE -> CORE | REPRESENTED same-dest | Verified at the E2 tip (`findings.py` lines 79-121, anchor lines 104-110): findings-v1 par
724. VL-21-724 | DROP -> DROP | REPRESENTED same-dest | Verified (`COMBO-REPORT.md:433`, `:498` ALL-src row, 76 runs): B1 0, B2 0, B3 68, B4 3, B5
725. VL-21-725 | EVAL -> EVAL | REPRESENTED same-dest | Verified (`COMBO-REPORT.md:373`): 156 of 665 valid-era runs never referenced source.md (em
726. VL-21-726 | EVAL -> EVAL | REPRESENTED same-dest | Merge-drop figures checked (`COMBO-REPORT.md:292`, `HANDOFF-...run2.md:135` R20): "80 revi
727. VL-21-727 | DROP -> DROP | REPRESENTED same-dest | Timing baselines verified (`COMBO-REPORT.md:331`, `:319`, `:320`, `:314`, `:325`, `:424`):
728. VL-21-728 | EVAL -> EVAL | REPRESENTED same-dest | Verified (`COMBO-REPORT.md:428`, `:424`): sonnet panel verdict "NOT CONFIRMED ... at 2.2x 
729. VL-21-729 | DROP -> DROP | REPRESENTED same-dest | Verified (`HO2:288`): DM14 default panel guidance "ember + 2x luna; optional quality tier 
730. VL-21-730 | DROP -> DROP | REPRESENTED same-dest | Verified: the hardcoded absolute REPO in `launch-*.sh` and the pc-patterns scripts; the sc
731. VL-21-731 | CORE -> CORE | REPRESENTED same-dest | Verified: the local E1 branch has `findings_v2.py`, `card_convert.py`, `cluster.py`, `mani
732. VL-21-732 | CORE -> CORE | REPRESENTED same-dest | Verified on the E1 branch: `review-panel/1` panel schema and tier aliases (default templat
733. VL-21-733 | DROP -> DROP | REPRESENTED same-dest | Decision D-1 (S11.1, `merged-spec.md:354-371`): slate = five redesigns, one per family: F1
734. VL-21-734 | DROP -> DROP | REPRESENTED same-dest | Decision D-2: base document V4 (opus:devops), score 0.978 (`base-selection.md:128-144`)
735. VL-21-735 | DROP -> DROP | REPRESENTED same-dest | Decision D-3: transport = JSON board + PostToolUse hook (mid-run) and between-phase digest
736. VL-21-736 | DROP -> DROP | REPRESENTED same-dest | Decision D-4: harness fixes H1-H4 in every arm except A0; grading rule and judge held cons
737. VL-21-737 | DROP -> DROP | REPRESENTED same-dest | Decision D-5: gains reported as three separate shares H, P, C, never summed; C conditional
738. VL-21-738 | DROP -> DROP | REPRESENTED same-dest | Decision D-6: no free text in any message; located content only; one exception (F7 card en
739. VL-21-739 | DROP -> DROP | REPRESENTED same-dest | Decision D-7: collaboration findings are lines inside ONE findings-v1 block (phase-2 ids `
740. VL-21-740 | DROP -> DROP | REPRESENTED same-dest | Decision D-8: time rules: PANEL_FINISH_AT formula, k formula, one phase-2 deadline T0 + 1.
741. VL-21-741 | DROP -> DROP | REPRESENTED same-dest | Decision D-9: central k = 1, optimistic k = 2 (`round3-tally.md:70`)
742. VL-21-742 | DROP -> DROP | REPRESENTED same-dest | Decision D-10: seals: process exit (F1), hook-side transcript snapshot sha256 fail-closed 
743. VL-21-743 | DROP -> DROP | REPRESENTED same-dest | Decision D-11: first experiment = pre-registered screen: stage 1 four EL2 designs (76 pane
744. VL-21-744 | DROP -> DROP | REPRESENTED same-dest | Decision D-12: models: ember, luna (cheap core), sonnet for F6; grok used in no design; ha
745. VL-21-745 | DROP -> DROP | REPRESENTED same-dest | Decision D-13: kill switch `PANEL_COLLAB=0` restores the isolated panel WITH harness fixes
746. VL-21-746 | DROP -> DROP | REPRESENTED same-dest | Decision D-14: if no exchange arm beats the static kit, adopt harness fixes + static kit a
747. VL-21-747 | DROP -> DROP | REPRESENTED same-dest | Decision D-15: read-only is enforced by audit, not by the tool list (Bash unrestricted)
748. VL-21-748 | DROP -> DROP | REPRESENTED same-dest | Open item O-1 (S11.2, `merged-spec.md:974`): whether the collaboration line is worth build
749. VL-21-749 | DROP -> DROP | REPRESENTED same-dest | Open item O-2: hooks (`--settings` PostToolUse) fire in `claude -p` for `muse-ember-1.0` a
750. VL-21-750 | DROP -> DROP | REPRESENTED same-dest | Open item O-3: gateway models call `SendMessage` reliably; a `-p` session receives mid-run
751. VL-21-751 | DROP -> DROP | REPRESENTED same-dest | Open item O-4: `--resume` works for both gateway models once `--no-session-persistence` is
752. VL-21-752 | DROP -> DROP | REPRESENTED same-dest | Open item O-5: act rates of gateway models on injected or delivered items (planning 0.5-0.
753. VL-21-753 | DROP -> DROP | REPRESENTED same-dest | Open item O-6: turn_p90, T_report_p90 (luna, sonnet), per-package B_A1, k, slowdown s of e
754. VL-21-754 | DROP -> DROP | REPRESENTED same-dest | Open item O-7: the H2 share; re-score the 30 cheap historical runs with the normalizer (Sp
755. VL-21-755 | DROP -> DROP | REPRESENTED same-dest | Open item O-8: the base commit for each package's H3 sandbox "not recorded in an obvious f
756. VL-21-756 | DROP -> DROP | REPRESENTED same-dest | Open item O-9: the SL2 harness share (+0.1 to +0.4) has no bottom-up table (`merged-spec.m
757. VL-21-757 | DROP -> DROP | REPRESENTED same-dest | Open item O-10: F6 and F7 token overheads not re-derived; F6 gain re-derived by halving, n
758. VL-21-758 | DROP -> DROP | REPRESENTED same-dest | Open item O-11: whether hook env inheritance holds (the design avoids it by baking setting
759. VL-21-759 | DROP -> DROP | REPRESENTED same-dest | Open item O-12: whether a luna-class reviewer completes its final-report turn within T_rep
760. VL-21-760 | DROP -> DROP | REPRESENTED same-dest | Open item O-13: whether a static move kit alone costs about +29% elapsed (V5 estimate) (Sp
761. VL-21-761 | DROP -> DROP | REPRESENTED same-dest | Open item O-14: whether a catalogue abstracted from three packages generalises (in-sample 
762. VL-21-762 | DROP -> DROP | REPRESENTED same-dest | Open item O-15: whether collaboration findings inflate judge credit by volume ("more findi
763. VL-21-763 | DROP -> DROP | REPRESENTED same-dest | Open item O-16: 8 merge-review minor notes not applied (including the B6 route M2 versus M
764. VL-21-764 | KNOWLEDGE -> KNOWLEDGE | REPRESENTED same-dest | Hand-off claim H-1 (S11.3): "convergence_score: 1.0 ... unresolved_conflicts: []" and fron
765. VL-21-765 | EVAL -> EVAL | REPRESENTED same-dest | Hand-off claim H-2: "Nothing was run for this variant; every number comes from the study f
766. VL-21-766 | KNOWLEDGE -> KNOWLEDGE | REPRESENTED same-dest | Hand-off claim H-3: the merge reply says "Nothing was staged or committed" (`sessions/deba
767. VL-21-767 | DROP -> DROP | REPRESENTED same-dest | Hand-off claim H-4: "Some gain numbers are estimates I chose, not figures the advocates ag
768. VL-21-768 | DROP -> DROP | REPRESENTED same-dest | Hand-off claim H-5: the merge executor produced `merged-spec.md` by copying V4 then applyi
769. VL-21-769 | DROP -> DROP | REPRESENTED same-dest | Hand-off claim H-6: the return contract's artifacts list names 41 artifacts under `nested/
770. VL-21-770 | DROP -> DROP | REPRESENTED same-dest | Hand-off claim H-7: absolute paths inside contracts point to `/home/coder/workspaces/workt
771. VL-21-771 | CORE -> CORE | REPRESENTED same-dest | Slice value item V-1 (S12): findings-v1 block + `superclaude review merge` + ledger as the
772. VL-21-772 | DROP -> DROP | REPRESENTED same-dest | V-2: H2 anchor/claim normaliser + parser validation + one re-ask (R-02); High, +0.03 (0.00
773. VL-21-773 | CORE -> CORE | REPRESENTED same-dest | V-3: H1 name the source or spec path in the brief and ask to read both (R-01); High, +0.03
774. VL-21-774 | HARNESS -> HARNESS | REPRESENTED same-dest | V-4: H3 base-commit review sandbox (R-03); High for plan review, +0.08 (0.02-0.16); slice 
775. VL-21-775 | DROP -> DROP | REPRESENTED same-dest | V-5: H4 leak-directory exclusion (`.dev/reflect/` etc.) (R-03); integrity; slice suggests 
776. VL-21-776 | CORE -> CORE | REPRESENTED same-dest | V-6: model-identity check `model_ok` per session (`RR:51-56`), `NOFALLBACK`, retry-loop ac
777. VL-21-777 | DROP -> DROP | REPRESENTED same-dest | V-7: panel timing rules (PANEL_FINISH_AT, k, hang guard, drift band, values file, SLO budg
778. VL-21-778 | CORE -> CORE | REPRESENTED same-dest | V-8: kill switch `PANEL_COLLAB=0`, `collab.json` telemetry ("47 fields, R-23"), alarms CON
779. VL-21-779 | DROP -> DROP | REPRESENTED same-dest | V-9: `panel-msg/1` schema + validator (<= 600 B, forbidden keys, located anchors); Medium;
780. VL-21-780 | DROP -> DROP | REPRESENTED same-dest | V-10: board substrate (`panel-post`, PostToolUse hook, per-reviewer `--settings`, baked pa
781. VL-21-781 | DROP -> DROP | REPRESENTED same-dest | V-11: between-phase digest + `--resume` + stream-json salvage (F1); Medium-High, "highest 
782. VL-21-782 | MODULE-tasklist -> MODULE-tasklist | REPRESENTED same-dest | V-12: move catalogue M1-M10 (frozen, generic, with style and observable signature); High (
783. VL-21-783 | EVAL -> EVAL | REPRESENTED same-dest | V-13: three theories + gate funnel (exposure/question/survival) + issue-to-theory-to-move 
784. VL-21-784 | EVAL -> EVAL | REPRESENTED same-dest | V-14: three-share accounting H/P/C and the static-kit control arm A2 ("the kit may win"); 
785. VL-21-785 | DROP -> DROP | REPRESENTED same-dest | V-15: pre-registered decision rule, Fisher thresholds, block randomisation, sealed-report 
786. VL-21-786 | DROP -> DROP | REPRESENTED same-dest | V-16: blind Opus judge `judge-one.sh` unchanged, sha256-pinned, anonymised reports (origin
787. VL-21-787 | DROP -> DROP | REPRESENTED same-dest | V-17: six cheap-model behaviour profiles (699 runs, per-model tool use, report shape, Jacc
788. VL-21-788 | DROP -> DROP | REPRESENTED same-dest | V-18: "cheap models verify only what the plan names": reverse-dependency and universal-cla
789. VL-21-789 | DROP -> DROP | REPRESENTED same-dest | V-19: sandbox confound (post-implementation checkout masks GT5, GT6, GT9, B8) plus 14 of 3
790. VL-21-790 | DROP -> DROP | REPRESENTED same-dest | V-20: grading-rule effect: unstated requirement = Medium (non-blocking, "follow-up candida
791. VL-21-791 | KNOWLEDGE -> KNOWLEDGE | REPRESENTED same-dest | V-21: transport research (Orca mail, Claude Code teams/subagents/cross-session, A2A, JSON 
792. VL-21-792 | DROP -> DROP | REPRESENTED same-dest | V-22: `pc-patterns` collector/analyzer scripts (`collect.py`, `analyze.py`, `rev.py`, `how
793. VL-21-793 | DROP -> DROP | REPRESENTED same-dest | V-23: `gtproxy.py` regex ground-truth proxy; Low; DROP or XP scratch; overfit to ground tr
794. VL-21-794 | DROP -> DROP | REPRESENTED same-dest | V-24: `theory.py` HARD-set bug (includes B3, B7; excludes B5, I1, B6); defect; fix before 
795. VL-21-795 | DROP -> DROP | REPRESENTED same-dest | V-25: `launch-variants.sh`, `launch-debate.sh`, `launch-debate-resume.sh`; Low (one-off); 
796. VL-21-796 | KNOWLEDGE -> KNOWLEDGE | REPRESENTED same-dest | V-26: adversarial pipeline artifacts (`diff-analysis.md` 43 diff points, `invariant-probe.
797. VL-21-797 | DROP -> DROP | REPRESENTED same-dest | V-27: unmeasured-items table (18 rows); High; XP backlog (spikes S0, S1, S2, S3, REQ-S3, S
798. VL-21-798 | DROP -> DROP | REPRESENTED same-dest | V-28: HL2 shadow-resume (haiku canary, +0%); Medium, gain not carried; DOC / later experim
799. VL-21-799 | DROP -> DROP | REPRESENTED same-dest | V-29: F6 Coverage Deflection; conditional (sonnet panel only; runs only if T_report_p90 <=
800. VL-21-800 | DROP -> DROP | REPRESENTED same-dest | V-30: F3 Move Radar telemetry classifier (jq/regex over tool calls); Medium; C may be abou
801. VL-21-801 | DROP -> DROP | REPRESENTED same-dest | V-31: F4 Idle-Shift Sweeper and F7 Flag-and-Adjudicate; Medium (experimental); M-T optiona
802. VL-21-802 | DROP -> DROP | REPRESENTED same-dest | V-32: Variants V3 designs, V5 designs 1-4, V1-R1/R2/R4/R5, V2-D1/D3/D4/D5 not selected; Lo
803. VL-21-803 | KNOWLEDGE -> KNOWLEDGE | REPRESENTED same-dest | V-33: variant arithmetic-error catalogue E1-E9 (S6.3); Medium (QA pattern); DOC; shows 16 
804. VL-21-804 | DROP -> DROP | REPRESENTED same-dest | V-34: `sessions/*.err`, `sessions/debate-reply.md` (0 B), `debate-resume-reply.md`; Low; D
805. VL-21-805 | DROP -> DROP | REPRESENTED same-dest | Overlap-matrix input, roster and addressing (S13): E2 uses raw names ember, luna, haiku, s
806. VL-21-806 | DROP -> DROP | REPRESENTED same-dest | Overlap-matrix input, reviewer runtime (S13): E2 headless `claude -p --model <raw id>` by 
807. VL-21-807 | DROP -> DROP | REPRESENTED same-dest | Overlap-matrix input, findings contract (S13): E2 findings-v1 + `superclaude review merge`
808. VL-21-808 | CORE -> CORE | REPRESENTED same-dest | Overlap-matrix input, independence model (S13): E2 exchange DURING the run (five redesigns
809. VL-21-809 | CORE -> CORE | REPRESENTED same-dest | Overlap-matrix input, rubric (S13): `src/superclaude/rules/prompts/document_review_loop_pr
810. VL-21-810 | EVAL -> EVAL | REPRESENTED same-dest | Overlap-matrix input, judge and eval (S13): E2 blind Opus judge `judge-one.sh` with three 
811. VL-21-811 | CORE -> CORE | REPRESENTED same-dest | Overlap-matrix input, merge and dedupe (S13): E2 a deterministic merge script plus ledger;
812. VL-21-812 | DROP -> DROP | REPRESENTED same-dest | Overlap-matrix input, telemetry (S13): E2 `collab.json` (47 fields), alarms CONVERGENCE/EC
813. VL-21-813 | KNOWLEDGE -> KNOWLEDGE | REPRESENTED same-dest | Overlap-matrix input, use case covered (S13): E2 tasklist (plan) review with candidate.md 
814. VL-21-814 | DROP -> DROP | REPRESENTED same-dest | Conflict seed C-1 (S14): findings contract: E2 findings-v1 and merge unchanged (R-04) vers
815. VL-21-815 | DROP -> DROP | REPRESENTED same-dest | Conflict seed C-2: reviewer addressing: E2 raw model names and gateway ids in briefs, hook
816. VL-21-816 | DROP -> DROP | REPRESENTED same-dest | Conflict seed C-3: independence versus exchange: E2 says exchange mid-run or between phase
817. VL-21-817 | DROP -> DROP | REPRESENTED same-dest | Conflict seed C-4: exchange value versus static kit: spec recommends five exchange designs
818. VL-21-818 | DROP -> DROP | REPRESENTED same-dest | Conflict seed C-5: thinking-budget claim: `seed-brief.md:65` (within every model the highe
819. VL-21-819 | DROP -> DROP | REPRESENTED same-dest | Conflict seed C-6: "hard issues" definition: script `HARD` = I5, I7, B7, B8, I6, B1, B2, B
820. VL-21-820 | DROP -> DROP | REPRESENTED same-dest | Conflict seed C-7: B6 route: `merged-spec.md:158` issue-to-move table says B6 = M10; `merg
821. VL-21-821 | DROP -> DROP | REPRESENTED same-dest | Conflict seed C-8: redesign numbering 1-5 versus slot order 3, 2, 1, 5, 4 (documented `mer
822. VL-21-822 | DROP -> DROP | REPRESENTED same-dest | Conflict seed C-9: "only bound enforced by a kill" (`merged-spec.md:291, 633`) versus the 
823. VL-21-823 | DROP -> DROP | REPRESENTED same-dest | Conflict seed C-10: +35% cap met only on the planned path: brief "at most 35%" (`seed-brie
824. VL-21-824 | HARNESS -> HARNESS | REPRESENTED same-dest | Conflict seed C-11: hooks versus project hooks: the spec injects hooks via per-reviewer `-
825. VL-21-825 | CORE -> CORE | REPRESENTED same-dest | Conflict seed C-12: `missing-task`: seed and spec T3b say "the brief has no missing-task c
826. VL-21-826 | DROP -> DROP | REPRESENTED same-dest | Conflict seed C-13: source of truth for planning baselines: the spec measures per-package 
827. VL-21-827 | DROP -> DROP | REPRESENTED same-dest | Conflict seed C-14: transport scope: the spec rejects Orca agent mail for bash-launched `c
828. VL-21-828 | DROP -> DROP | REPRESENTED same-dest | Conflict seed C-15: estimates versus measurements: gain tables to 2-3 decimals while the s
829. VL-21-829 | EVAL -> EVAL | REPRESENTED same-dest | Conflict seed C-16: hint specificity: the spec says only catalogue move text may be sent w
830. VL-21-830 | DROP -> DROP | REPRESENTED same-dest | Conflict seed C-17: A0 naming: V4 base called the isolated harness-fixed arm "A0"; the mer
831. VL-21-831 | DROP -> DROP | REPRESENTED same-dest | Conflict seed C-18: `contradiction` to M7 (`refactor-plan.md:191`, `round3-V1.md:30`, V2 i
832. VL-21-832 | CORE -> CORE | REPRESENTED same-dest | Architecture contribution A-1 (S15): reviewer runner with identity check, retry accounting
833. VL-21-833 | CORE -> CORE | REPRESENTED same-dest | A-2: sandbox and evidence builder: base-commit `git archive` minus leak dirs, named drivin
834. VL-21-834 | DROP -> DROP | REPRESENTED same-dest | A-3: findings normaliser + parser gate + merge + ledger (H2, R-02, R-04, `findings.py`); k
835. VL-21-835 | MODULE-tasklist -> CORE | REPRESENTED moved(documented) | A-4: exchange layer as an optional plug-in: `panel-msg/1` schema, board, hooks, digest/res
836. VL-21-836 | DROP -> DROP | REPRESENTED same-dest | A-5: runtime control: `PANEL_FINISH_AT`, k, hang guard, kill switch, values file, drift ba
837. VL-21-837 | CORE -> CORE | REPRESENTED same-dest | A-6: integrity and telemetry: `collab.json`, CONVERGENCE (own-line Jaccard), ECHO, SNAPSHO
838. VL-21-838 | EVAL -> EVAL | REPRESENTED same-dest | A-7: experiment harness: arms, A0/A1/A2 controls, H/P/C shares, blind judge, pre-registere
839. VL-21-839 | DROP -> DROP | REPRESENTED same-dest | A-8: review-lens content (thin module input): move catalogue M1-M10 + brief text (section 
840. VL-21-840 | CORE -> CORE | REPRESENTED same-dest | A-9: rubric prompt file (shared, E3-owned) `document_review_loop_prompts.md:31,60`: the si
841. VL-21-841 | MODULE-pr-review -> MODULE-pr-review | REPRESENTED same-dest | A-10: thin-module differences found: tasklist = candidate.md + source.md with Task ids and
842. VL-21-842 | DROP -> DROP | REPRESENTED same-dest | Defect DEF-1 (S16): the merged spec has 8 unapplied minor review notes including the B6 ro
843. VL-21-843 | DROP -> DROP | REPRESENTED same-dest | DEF-2: `theory.py:8` HARD set includes B3 (easy) and B7 and excludes B5, I1, B6; "hard hit
844. VL-21-844 | DROP -> DROP | REPRESENTED same-dest | DEF-3: `gtproxy.py` per-model hit rates for target issues are regex noise (B1 TP 0/FP 4; B
845. VL-21-845 | DROP -> DROP | REPRESENTED same-dest | DEF-4: "92 findings dropped over 264 merges" mixes units (the source says "80 reviewer-lev
846. VL-21-846 | HARNESS -> HARNESS | REPRESENTED same-dest | DEF-5: hardcoded absolute REPO/E paths in all launch scripts and pc-patterns scripts; `rec
847. VL-21-847 | DROP -> DROP | REPRESENTED same-dest | DEF-6: `how.py` output not stored: "7 of 26 DE sonnet runs did a reverse-dependency search
848. VL-21-848 | DROP -> DROP | REPRESENTED same-dest | DEF-7: planning values presented to 2-3 decimals (e.g. 0.13-1.06) rest on act rates with "
849. VL-21-849 | DROP -> DROP | REPRESENTED same-dest | DEF-8: debate session 1 timed out at 5400 s in Round 3 (`return-contract.yaml:25`); proces
850. VL-21-850 | DROP -> DROP | REPRESENTED same-dest | DEF-9: variants' own arithmetic: 16 errors in 25 designs (8 gain tables, 1 time budget ove
851. VL-21-851 | DROP -> DROP | REPRESENTED same-dest | DEF-10: the 12-run adoption design cannot detect the central estimates (A1 reach 3-29% per
852. VL-21-852 | MODULE-tasklist -> MODULE-tasklist | REPRESENTED same-dest | DEF-11: the review sandbox exposes Read + Bash only; the Move Radar signatures (M1, M2, M7
853. VL-21-853 | DROP -> DROP | REPRESENTED same-dest | DEF-12: F3 Move Radar's own text concedes "with almost no luna search signatures, ember's 
854. VL-21-854 | DROP -> DROP | REPRESENTED same-dest | Exposure F-1 (S17): the two-document model (candidate.md + source.md) is hard-wired in H1,
855. VL-21-855 | CORE -> CORE | REPRESENTED same-dest | F-2: anchors are exact 12-200 char substrings of `candidate.md` after whitespace flattenin
856. VL-21-856 | EVAL -> EVAL | REPRESENTED same-dest | F-3: the catalogue M1-M10 was abstracted from three tasklist packages (10 hard issues); in
857. VL-21-857 | DROP -> DROP | REPRESENTED same-dest | F-4: the H3 base-commit sandbox presumes a plan reviewed against a repo that has since bee
858. VL-21-858 | DROP -> DROP | REPRESENTED same-dest | F-5: reports written into the repo (`.dev/reflect/`, task folders) leak into later review 
859. VL-21-859 | DROP -> DROP | REPRESENTED same-dest | F-6: the reviewer tool surface differs by runtime (Read + Bash headless sandbox versus Age
860. VL-21-860 | EVAL -> EVAL | REPRESENTED same-dest | F-7: timing constants (3.2/6.4/23/14 s per turn; 116/238/273.7 s baselines) are gateway- a
861. VL-21-861 | DROP -> DROP | REPRESENTED same-dest | F-8: the model roster and gateway ids (`muse-ember-1.0`, `gpt-6-luna`, `grok-4.7`) are tim
862. VL-21-862 | DROP -> DROP | REPRESENTED same-dest | F-9: hooks and `--resume` are untested for gateway models; Agent-tool reviewers may not su
863. VL-21-863 | DROP -> DROP | REPRESENTED same-dest | F-10: rubric grading (Medium for an unstated requirement) suppresses missing-task findings
864. VL-21-864 | DROP -> DROP | REPRESENTED same-dest | F-11: the judge is Opus-only, blind and sha256-pinned; a central panel in production has n
865. VL-21-865 | EVAL -> EVAL | REPRESENTED same-dest | F-12: the elapsed budget +35% and per-package k are computed from historical medians; no e
866. VL-21-866 | MODULE-pr-review -> MODULE-pr-review | REPRESENTED same-dest | F-13: the collaboration designs add 26-45% output tokens (F1 +34%, F4 +45%, F3 +26%, stati
867. VL-21-867 | DROP -> DROP | REPRESENTED same-dest | F-14: judge-visible markers (`origin` keys, board references) must be stripped to keep the
868. VL-21-868 | HARNESS -> HARNESS | REPRESENTED same-dest | Script `debate/convergence.py` (S18.1; 60 lines, 2,435 B): docstring `uv run python conver
869. VL-21-869 | HARNESS -> HARNESS | REPRESENTED same-dest | Script `debate/transcript.py` (S18.2; 64 lines): assembles `debate-transcript.md` from rou
870. VL-21-870 | KNOWLEDGE -> KNOWLEDGE | REPRESENTED same-dest | Script `scoring/quant.py` (S18.3; 79 lines): RC = 36 brief requirements each matched by ON
871. VL-21-871 | HARNESS -> HARNESS | REPRESENTED same-dest | Scripts `scoring/reconcile.py` (33 lines) and `final_qual.py` (47 lines) (S18.4): compare 
872. VL-21-872 | KNOWLEDGE -> KNOWLEDGE | REPRESENTED same-dest | Artifacts `scoring/qual-pass1.md` (18,322 B) and `qual-pass2.md` (22,615 B) (S18.5): two i
873. VL-21-873 | DROP -> DROP | REPRESENTED same-dest | Round files (S18.6) `debate/round{1,2,3}-V{1..5}.md` (15 files, 11-22 KB each) plus `round
874. VL-21-874 | KNOWLEDGE -> KNOWLEDGE | REPRESENTED same-dest | Position-bias and fault-finding structure (S18.7, `base-selection.md:109-126`, `invariant-
875. VL-21-875 | KNOWLEDGE -> KNOWLEDGE | REPRESENTED same-dest | Slice summary (S-summary): inventoried `.dev/brainstorms/20261113-163248-panel-collaborati
876. VL-21-876 | DROP -> DROP | REPRESENTED same-dest | Headline 1: the output is a REQUIREMENTS spec only; nothing was run; all gains are plannin
877. VL-21-877 | DROP -> DROP | REPRESENTED same-dest | Headline 2: V4 base, 0.978 vs 0.946 (V5) vs 0.945 (V1); margin 3.3 points under 5% so the 
878. VL-21-878 | DROP -> DROP | REPRESENTED same-dest | Headline 3: the debate converged 37/43 (0.860), then 43/43, then 43/43 after closing 8 HIG
879. VL-21-879 | DROP -> DROP | REPRESENTED same-dest | Headline 4: five final redesigns F1 (~165 LOC, highest reliability), F4 (~180), F3 (~230, 
880. VL-21-880 | DROP -> DROP | REPRESENTED same-dest | Headline 5: a static move kit (A2, about 25 LOC, about +29% elapsed est.) "may beat every 
881. VL-21-881 | DROP -> DROP | REPRESENTED same-dest | Headline 6: empirical base (699 reviewer runs, 76 valid-era rows; 16 known issues; 10 neve
882. VL-21-882 | DROP -> DROP | REPRESENTED same-dest | Headline 7: verified against code: `run-reviewer.sh:48,50-56,61-64`; `findings.py:79-121`;
883. VL-21-883 | DROP -> DROP | REPRESENTED same-dest | Headline 8: defects found: theory.py HARD set (CODE-CONTRADICTED as applied); gtproxy.py F
884. VL-21-884 | DROP -> DROP | REPRESENTED same-dest | Headline 9: cross-effort exposures: findings-v1 held fixed vs E1's findings_v2; raw model 
885. VL-21-885 | KNOWLEDGE -> KNOWLEDGE | REPRESENTED same-dest | Slice count line: 25 redesigns / 7 families / 5 final; 43 diff points; 33 invariants; 47 r
886. VL-21-886 | KNOWLEDGE -> KNOWLEDGE | REPRESENTED same-dest | Coverage gap (S-gaps): `debate/round1-V*.md`, `round2-V*.md`, `round3-V2..V5.md` not read 
887. VL-21-887 | KNOWLEDGE -> KNOWLEDGE | REPRESENTED same-dest | Coverage gap: the five variants' 25 design bodies were inventoried through `diff-analysis.
888. VL-21-888 | KNOWLEDGE -> KNOWLEDGE | REPRESENTED same-dest | Coverage gap: `.dev/eval-workspaces/tasklist-review-panel/20261111-a1/` (COMBO-REPORT, HAN
889. VL-21-889 | DROP -> DROP | REPRESENTED same-dest | Unverified carried: all gain, act-rate, turn_p90, T_report_p90, hook cost (about 0.1 s/cal
890. VL-21-890 | DROP -> DROP | REPRESENTED same-dest | Unverified carried: hooks fire in `claude -p` for gateway ids; `--resume` works for gatewa
891. VL-21-891 | DROP -> DROP | REPRESENTED same-dest | Unverified carried: external doc claims in `research-light.md` (Claude Code cross-session 
892. VL-21-892 | DROP -> DROP | REPRESENTED same-dest | Unverified carried: `investigation-patterns.md:157` "sonnet did this in only 7 of 26 DE ru
893. VL-21-893 | DROP -> DROP | REPRESENTED same-dest | Unverified carried: which unit the "92 findings dropped" refers to (DEF-4)
894. VL-21-894 | DROP -> DROP | REPRESENTED same-dest | Unverified carried: whether E1 `reflect-reviewer` agents and E3 installed variants can hos
895. VL-21-895 | DROP -> DROP | REPRESENTED same-dest | Unverified carried: whether the final committed brainstorm folder matches what the orchest
896. VL-21-896 | CORE -> CORE | REPRESENTED same-dest | Question Q1 (S-questions): is the unified panel meant to include any mid-run or inter-phas
897. VL-21-897 | CORE -> CORE | REPRESENTED same-dest | Question Q2: which findings contract survives, findings-v1 (E2 R-04) or findings-v2 on thi
898. VL-21-898 | CORE -> CORE | REPRESENTED same-dest | Question Q3: reviewer addressing, raw gateway ids (E2) or tier aliases (E1)? Does the exch
899. VL-21-899 | CORE -> CORE | REPRESENTED same-dest | Question Q4: is the rubric file (`document_review_loop_prompts.md`, E3-owned) allowed to c
900. VL-21-900 | CORE -> CORE | REPRESENTED same-dest | Question Q5: should H1-H4 be promoted to unconditional central-core requirements now (chea
901. VL-21-901 | HARNESS -> HARNESS | REPRESENTED same-dest | Question Q6: the base commit per package for H3 is "not recorded in an obvious file" (O-8)
902. VL-21-902 | MODULE-pr-review -> MODULE-pr-review | REPRESENTED same-dest | Question Q7: for PR code review and rf-qa replacement, is the M1-M10 catalogue to be re-de
903. VL-21-903 | EVAL -> EVAL | REPRESENTED same-dest | Question Q8: does the E1 model-combination experiment (5x3) use the same three packages an
904. VL-21-904 | CORE -> CORE | REPRESENTED same-dest | Question Q9: should the leak class (`.dev/reflect/` and task folders written into the repo
905. VL-21-905 | KNOWLEDGE -> KNOWLEDGE | REPRESENTED same-dest | Question Q10: the refactor plan said C-18 `contradiction` to M7 while the spec says M8; co
906. VL-21-906 | KNOWLEDGE -> KNOWLEDGE | REPRESENTED same-dest | File tree (S1), top level: seed-brief.md 12,770 B; merged-requirements.md 136,728 B; retur
907. VL-21-907 | KNOWLEDGE -> KNOWLEDGE | REPRESENTED same-dest | File tree, new enrichment: `enrichment/investigation-generality.md` 31,216 B and `enrichme
908. VL-21-908 | DROP -> DROP | REPRESENTED same-dest | File tree, `enrichment/reused/`: investigation-alias-control.md 24,649 B, investigation-de
909. VL-21-909 | KNOWLEDGE -> KNOWLEDGE | REPRESENTED same-dest | File tree, variants: variant-1-sonnet-architect.md 61,742 B; variant-2-sonnet-analyzer.md 
910. VL-21-910 | KNOWLEDGE -> KNOWLEDGE | REPRESENTED same-dest | File tree, sessions: debate-reply.md 2,850 B; debate.err 112 B; variant-{1,2,3}.err 0 B ea
911. VL-21-911 | KNOWLEDGE -> KNOWLEDGE | REPRESENTED same-dest | File tree, nested adversarial run: merged-spec.md 136,624 B; return-contract.yaml 5,165 B;
912. VL-21-912 | KNOWLEDGE -> KNOWLEDGE | REPRESENTED same-dest | File tree, `scoring/`: convergence.py, convergence-output.txt, final-qual-table.md, final_
913. VL-21-913 | KNOWLEDGE -> KNOWLEDGE | REPRESENTED same-dest | Tree totals: 58 blobs, 1,055,384 bytes; merged-requirements.md and merged-spec.md differ b
914. VL-21-914 | KNOWLEDGE -> KNOWLEDGE | REPRESENTED same-dest | Seed-brief front matter (S2): topic "redesign how the tasklist review panel operates (agen
915. VL-21-915 | DROP -> DROP | REPRESENTED same-dest | Seed problem: panels of ember, luna, haiku find about 2 of 14 known defects per run on the
916. VL-21-916 | KNOWLEDGE -> KNOWLEDGE | REPRESENTED same-dest | Owner ask: two redesigns, catch the missed issues reliably, not tuned to the three package
917. VL-21-917 | KNOWLEDGE -> KNOWLEDGE | REPRESENTED same-dest | Evidence base: `.dev/eval-workspaces/tasklist-review-panel/20261111-a1/` (COMBO-REPORT.md,
918. VL-21-918 | EVAL -> EVAL | REPRESENTED same-dest | Isolated baselines (valid era): ember + 2x luna 1.83/14, about 348 s over 3 packages, 64k 
919. VL-21-919 | DROP -> DROP | REPRESENTED same-dest | Model patterns (medians/run): ember 41 s, 7.1k thinking tokens, greps cited lines, 46% loc
920. VL-21-920 | DROP -> DROP | REPRESENTED same-dest | Harness confounds and fixes: merge drops findings with anchors over 200 or claims over 300
921. VL-21-921 | CORE -> CORE | REPRESENTED same-dest | Brief defects: the rubric `src/superclaude/rules/prompts/document_review_loop_prompts.md` 
922. VL-21-922 | EVAL -> EVAL | REPRESENTED same-dest | Ground-truth size: 3 plan packages, 16 known issues, one repository
923. VL-21-923 | DROP -> DROP | REPRESENTED same-dest | Theories T1-T3 from the first investigation: T1 plan-bounded search (`test_worker_contract
924. VL-21-924 | KNOWLEDGE -> KNOWLEDGE | REPRESENTED same-dest | Constraint: exactly TWO redesigns (instructions and/or process; a deterministic pre-pass i
925. VL-21-925 | MODULE-tasklist -> MODULE-tasklist | REPRESENTED same-dest | Constraint: broad applicability: redesigns are keyed to defect classes and document struct
926. VL-21-926 | EVAL -> EVAL | REPRESENTED same-dest | Constraint: evidence of generality plus validation on hold-out or leave-one-out data
927. VL-21-927 | DROP -> DROP | REPRESENTED same-dest | Constraint: time at most +35% versus a named isolated baseline, with arithmetic and critic
928. VL-21-928 | KNOWLEDGE -> KNOWLEDGE | REPRESENTED same-dest | Success criteria (S2), per redesign: mechanism with quoted wording, model roles, step orde
929. VL-21-929 | EVAL -> EVAL | REPRESENTED same-dest | Success criterion: a hold-out validation experiment
930. VL-21-930 | EVAL -> EVAL | REPRESENTED same-dest | Open question (S2): which defect classes are general?
931. VL-21-931 | EVAL -> EVAL | REPRESENTED same-dest | Open question: does an instruction change alone work, or is a script check needed?
932. VL-21-932 | DROP -> DROP | REPRESENTED same-dest | Open question: how much of the gap do H1-H4 alone close?
933. VL-21-933 | EVAL -> EVAL | REPRESENTED same-dest | Open question: is a deterministic structural pre-pass a general mechanism?
934. VL-21-934 | EVAL -> EVAL | REPRESENTED same-dest | Open question: where must judgement stay in the loop, and what stops the pre-pass from bei
935. VL-21-935 | MODULE-tasklist -> MODULE-tasklist | REPRESENTED same-dest | Class C1 (S2/S3): completeness criterion with no stopping rule (designSpec GT1, GT2; 3 oth
936. VL-21-936 | MODULE-tasklist -> MODULE-tasklist | REPRESENTED same-dest | Class C2: source rule not carried into the plan (GT5; 6 plans); general
937. VL-21-937 | MODULE-tasklist -> MODULE-tasklist | REPRESENTED same-dest | Class C3: value read but never written (GT6; 3 documents); weak (the exact lookup-table sh
938. VL-21-938 | MODULE-tasklist -> MODULE-tasklist | REPRESENTED same-dest | Class C4: criterion command cannot match or pass (GT9; 9 documents, 8 plans); general
939. VL-21-939 | MODULE-tasklist -> MODULE-tasklist | REPRESENTED same-dest | Class C5: stale count, claim or copy (GT10; 9 documents: 3 plans, 6 delivered texts); gene
940. VL-21-940 | MODULE-tasklist -> MODULE-tasklist | REPRESENTED same-dest | Class C6: "all/only/never" contradicted (alias GT1, GT3; 12 documents: 4 plans, 8 delivere
941. VL-21-941 | MODULE-tasklist -> MODULE-tasklist | REPRESENTED same-dest | Class C7: dictated text omits a clause (alias GT4); the broad form is general (5 plans), t
942. VL-21-942 | MODULE-tasklist -> MODULE-tasklist | REPRESENTED same-dest | Class C8: the plan edits what a test pins (control GT1; 6 documents, 5 plans); general
943. VL-21-943 | EVAL -> EVAL | REPRESENTED same-dest | Generality caveats: seven further classes recur (X1-X7), several as frequent as the ten; a
944. VL-21-944 | EVAL -> EVAL | REPRESENTED same-dest | Hold-out candidates: six other packages or documents; cheapest `workerContractFo`, `implem
945. VL-21-945 | MODULE-tasklist -> MODULE-tasklist | REPRESENTED same-dest | Class X1 (S3): tests that pass on old code (4 documents)
946. VL-21-946 | MODULE-tasklist -> MODULE-tasklist | REPRESENTED same-dest | Class X2: wrong or aged citation (4 documents)
947. VL-21-947 | MODULE-tasklist -> MODULE-tasklist | REPRESENTED same-dest | Class X3: two source statements conflict (3 documents)
948. VL-21-948 | MODULE-tasklist -> MODULE-tasklist | REPRESENTED same-dest | Class X4: task ordering or a gate with no consumer (3 documents)
949. VL-21-949 | MODULE-tasklist -> MODULE-tasklist | REPRESENTED same-dest | Class X5: criterion depends on an uncaptured baseline (3 documents)
950. VL-21-950 | MODULE-tasklist -> MODULE-tasklist | REPRESENTED same-dest | Class X6: failure path with no route (3 documents)
951. VL-21-951 | MODULE-tasklist -> MODULE-tasklist | REPRESENTED same-dest | Class X7: count broken by a forced step (2 documents, weak)
952. VL-21-952 | KNOWLEDGE -> KNOWLEDGE | REPRESENTED same-dest | External evidence (seed, secondhand): a checklist alone is no better than ad hoc review; p
953. VL-21-953 | KNOWLEDGE -> KNOWLEDGE | REPRESENTED same-dest | External evidence: a static-tool + model hybrid removed 94-98% of false positives at 2-110
954. VL-21-954 | KNOWLEDGE -> KNOWLEDGE | REPRESENTED same-dest | External evidence: parallel same-model passes plateau near 5; majority voting can backfire
955. VL-21-955 | KNOWLEDGE -> KNOWLEDGE | REPRESENTED same-dest | External evidence: herding, answer-flip +10 points, 29-34% of reviewers conformed
956. VL-21-956 | MODULE-tasklist -> MODULE-tasklist | REPRESENTED same-dest | Design consequence (S3 external support): majority voting backfires on small models, so th
957. VL-21-957 | EVAL -> EVAL | REPRESENTED same-dest | ISO/IEC/IEEE 29148 is mapped onto C1-C8 (merged-requirements line 113) and an "open-ended 
958. VL-21-958 | MODULE-tasklist -> MODULE-tasklist | REPRESENTED same-dest | Implication (seed): the class-keyed recipe is the unit of generality
959. VL-21-959 | MODULE-tasklist -> MODULE-tasklist | REPRESENTED same-dest | Implication: script sweeps for C5, C6, C8 and a mechanical run for C4; reading-only classe
960. VL-21-960 | MODULE-tasklist -> MODULE-tasklist | REPRESENTED same-dest | Implication: parallel lenses fit the +35% budget, sequential ones do not
961. VL-21-961 | EVAL -> EVAL | REPRESENTED same-dest | Implication: fast-reviewer idle time (ember about 41 s versus luna 102-122, haiku 220-240)
962. VL-21-962 | DROP -> DROP | REPRESENTED same-dest | Implication: C1 and C3 generality is weak
963. VL-21-963 | DROP -> DROP | REPRESENTED same-dest | Note: "dialogue mode: non-interactive" (line 13): answers came from the owner's request an
964. VL-21-964 | KNOWLEDGE -> KNOWLEDGE | REPRESENTED same-dest | Merged-requirements part A file facts (S3): `merged-requirements.md` 1254 lines, 136,728 B
965. VL-21-965 | KNOWLEDGE -> KNOWLEDGE | REPRESENTED same-dest | Conventions (S3): paths EVAL, BR, HO2, MR; evidence abbreviations seed, IG (investigation-
966. VL-21-966 | DROP -> DROP | REPRESENTED same-dest | Counting rule (S3): nine of ten missed issues (B1, B2, B5, B6, B8, I1, I4, I5, I6) lie ins
967. VL-21-967 | EVAL -> EVAL | REPRESENTED same-dest | Arm Z0-raw (S3): the current harness with no fixes
968. VL-21-968 | EVAL -> EVAL | REPRESENTED same-dest | Arm Z0 (S3): the control to beat: isolated panel + H1-H4 + CB-1..CB-5
969. VL-21-969 | EVAL -> EVAL | REPRESENTED same-dest | Arm K (S3): a plain-words checklist
970. VL-21-970 | EVAL -> EVAL | REPRESENTED same-dest | Arm SS (S3): Redesign 1 (Sweep Sheet) plus fixes
971. VL-21-971 | EVAL -> EVAL | REPRESENTED same-dest | Arm RL (S3): Redesign 2 (Recipe Ledger) plus fixes
972. VL-21-972 | EVAL -> EVAL | REPRESENTED same-dest | Baseline symbol b (S3): Z0's per-package median of the slowest reviewer
973. VL-21-973 | DROP -> DROP | REPRESENTED same-dest | Status of numbers (S3): "All probabilities, selection factors and time figures are plannin
974. VL-21-974 | DROP -> DROP | REPRESENTED same-dest | Theory T1 refined (S3): reviewers verify what the plan names; the search DIRECTION matters
975. VL-21-975 | EVAL -> EVAL | REPRESENTED same-dest | Theory T2 refined (S3), extras: top-3 tasks take 38-91% of a model's anchors (PAT s3); lun
976. VL-21-976 | DROP -> DROP | REPRESENTED same-dest | Theory T3 refined (S3): T3a environment, T3b suppression; sandbox post-implementation repa
977. VL-21-977 | DROP -> DROP | REPRESENTED same-dest | Rejected rival (S3): the reasoning budget is not the lever: across 7 models median thinkin
978. VL-21-978 | EVAL -> EVAL | REPRESENTED same-dest | Issue-to-cause map (S3): B1 C1 T2b; B2 C1 T2b (+T3a source narrower than plan); B5 C2 T2a 
979. VL-21-979 | EVAL -> EVAL | REPRESENTED same-dest | Redesign-to-theory map (S3): Redesign 1 Sweep Sheet: T1 primary (script runs reverse sweep
980. VL-21-980 | KNOWLEDGE -> KNOWLEDGE | REPRESENTED same-dest | Target-neutral class definitions exist at merged-requirements lines 101-108 (not quoted in
981. VL-21-981 | EVAL -> EVAL | REPRESENTED same-dest | Limits carried forward (S3): one repo and one pipeline; the records show a class exists, n
982. VL-21-982 | EVAL -> EVAL | REPRESENTED same-dest | Hold-out HO-1: a docs-only plan with 11 items (about 1 h of ground-truth work) [IG H5]
983. VL-21-983 | EVAL -> EVAL | REPRESENTED same-dest | Hold-out HO-2: a plan with 4-8 items [IG H2]
984. VL-21-984 | EVAL -> EVAL | REPRESENTED same-dest | Hold-out HO-3: a plan with 12 items [IG H4]
985. VL-21-985 | EVAL -> EVAL | REPRESENTED same-dest | Hold-out HO-4: a larger plan with 9 important findings (about half a day) [IG H3]
986. VL-21-986 | EVAL -> EVAL | REPRESENTED same-dest | Hold-out HO-5: a spec with a validated 44-defect ledger (use 20 blocking rows) [IG H1], "t
987. VL-21-987 | EVAL -> EVAL | REPRESENTED same-dest | Hold-out HO-6: a sanity set of 3 items, in no decision [IG H6]
988. VL-21-988 | MODULE-tasklist -> MODULE-tasklist | REPRESENTED same-dest | Section 3 intro: both redesigns keep reviewers read-only and the findings-v1 merge contrac
989. VL-21-989 | EVAL -> EVAL | REPRESENTED same-dest | Instruction-change versus script, "from opposite sides": Redesign 1 puts the sweep in a sc
990. VL-21-990 | KNOWLEDGE -> KNOWLEDGE | REPRESENTED same-dest | Difference table (S3): who runs the sweep (script versus model); unit (typed item, at most
991. VL-21-991 | DROP -> DROP | REPRESENTED same-dest | NOT a redesign: an optional blind claim-only verifier (3.0.9)
992. VL-21-992 | KNOWLEDGE -> KNOWLEDGE | REPRESENTED same-dest | NOT a redesign: a second fresh ember session
993. VL-21-993 | CORE -> CORE | REPRESENTED same-dest | NOT a redesign: rewriting the grading-rule Medium sentence (a rubric edit); allowed only a
994. VL-21-994 | KNOWLEDGE -> KNOWLEDGE | REPRESENTED same-dest | NOT a redesign: one shared list of up to 60 items given to every reviewer
995. VL-21-995 | DROP -> DROP | REPRESENTED same-dest | 3.0.1 H1 and H2 (S3): H1 the brief names the absolute source path (CB-1), rendered only if
996. VL-21-996 | HARNESS -> HARNESS | REPRESENTED same-dest | H3 variant (S3 3.0.1): the sandbox is built at the plan's base commit, or "no commit: reco
997. VL-21-997 | HARNESS -> HARNESS | REPRESENTED same-dest | H4 variant (S3 3.0.1): remove `.dev/reflect/`, `artifacts/`, `progress.md` and every repor
998. VL-21-998 | DROP -> DROP | REPRESENTED same-dest | "The H share is reported as its own number: Z0 minus Z0-raw replaces the +0.14... never su
999. VL-21-999 | DROP -> DROP | REPRESENTED same-dest | Held constant (S3, REQ-05): the grading rule (unstated requirement = Medium), the six find
1000. VL-21-1000 | CORE -> CORE | REPRESENTED same-dest | Brief edit CB-1 (3.0.2; target `src/superclaude/rules/prompts/document_review_loop_prompts
1001. VL-21-1001 | CORE -> CORE | REPRESENTED same-dest | Brief edit CB-2: every confirmed defect is listed (severity graded separately); removes th
1002. VL-21-1002 | CORE -> CORE | REPRESENTED same-dest | Brief edit CB-3: blocker sentence "An implementer who follows the stated text as written b
1003. VL-21-1003 | CORE -> CORE | REPRESENTED same-dest | Brief edit CB-4: merge limits stated in the brief (id unique, at most 16 chars; anchor 12-
1004. VL-21-1004 | MODULE-tasklist -> MODULE-tasklist | REPRESENTED same-dest | Brief edit CB-5: a free-review floor "Keep at least half of your time for your own review"
1005. VL-21-1005 | MODULE-tasklist -> CORE | REPRESENTED moved(documented) | Class card schema (3.0.3): id/name/version, definition, `recipe_text` (at most 120 words, 
1006. VL-21-1006 | MODULE-tasklist -> MODULE-tasklist | REPRESENTED same-dest | Block kinds (3.0.3): task, criterion, constraint, dictated_text, edit_target, gate
1007. VL-21-1007 | MODULE-tasklist -> CORE | REPRESENTED moved(documented) | Per-target re-derivation (3.0.3): the maintainer re-derives per target the command dialect
1008. VL-21-1008 | EVAL -> EVAL | REPRESENTED same-dest | AO-1 (anti-overfit rule): a machine lint fails any 4-word sequence from `ground-truth.json
1009. VL-21-1009 | EVAL -> EVAL | REPRESENTED same-dest | AO-2: a swap test plus a second author reviews each card (REQ-08)
1010. VL-21-1010 | EVAL -> EVAL | REPRESENTED same-dest | AO-3: each card needs at least 2 instances outside the study packages, each extractor at l
1011. VL-21-1011 | EVAL -> EVAL | REPRESENTED same-dest | AO-4: each extractor is tested on at least 3 plans not used to write it (REQ-21)
1012. VL-21-1012 | EVAL -> EVAL | REPRESENTED same-dest | AO-5: freeze the cards by git tag and hash before hold-out ground truth is written (REQ-33
1013. VL-21-1013 | EVAL -> EVAL | REPRESENTED same-dest | AO-6: ground truth is never in the sandbox (REQ-34)
1014. VL-21-1014 | EVAL -> EVAL | REPRESENTED same-dest | AO-7: leave-one-class-out ablation: removing a class moves other classes' reach by at most
1015. VL-21-1015 | EVAL -> EVAL | REPRESENTED same-dest | AO-8: a recipe never states the expected outcome and has no worked example from the study 
1016. VL-21-1016 | HARNESS -> HARNESS | REPRESENTED same-dest | `ledger-v1` carrier, launcher facts (3.0.4): `run-reviewer.sh` line 50 keeps only the fina
1017. VL-21-1017 | MODULE-tasklist -> CORE | REPRESENTED moved(documented) | `ledger-v1` format (3.0.4): heading `## Ledger`, a fenced block with info string `ledger-v
1018. VL-21-1018 | CORE -> CORE | REPRESENTED same-dest | Real parser, never a fence-opener grep (REQ-13)
1019. VL-21-1019 | EVAL -> EVAL | REPRESENTED same-dest | `ledger_missing` rate must be at most 10% in the compliance spike before any arm runs (REQ
1020. VL-21-1020 | CORE -> CORE | REPRESENTED same-dest | `findings.py` lines 90-158 (3.0.5): id `^[A-Za-z0-9][A-Za-z0-9._-]{0,15}$` unique, anchor 
1021. VL-21-1021 | MODULE-tasklist -> CORE | REPRESENTED moved(documented) | Post-run checks (3.0.5): every item has a ledger line (no re-ask); flattened substring tes
1022. VL-21-1022 | EVAL -> EVAL | REPRESENTED same-dest | Demotion arithmetic (3.0.5, INV-007): report the share of format-caused demotions because 
1023. VL-21-1023 | CORE -> CORE | REPRESENTED same-dest | PROMOTION (3.0.5): a PROBLEM row with no linked finding is promoted by the harness: claim 
1024. VL-21-1024 | CORE -> CORE | REPRESENTED same-dest | Telemetry keys (3.0.6): extra keys on findings-v1 lines `class`, `probe`, `src`; `findings
1025. VL-21-1025 | EVAL -> EVAL | REPRESENTED same-dest | Per-class yield table per run (3.0.6)
1026. VL-21-1026 | MODULE-tasklist -> MODULE-tasklist | REPRESENTED same-dest | Fallback (3.0.7): fall back to the isolated panel + H1-H4 + CB-1..CB-5 with `fallback=true
1027. VL-21-1027 | MODULE-tasklist -> MODULE-tasklist | REPRESENTED same-dest | `check_skipped=true` (3.0.7): a ledger check failure after the reviewers finish skips the 
1028. VL-21-1028 | CORE -> CORE | REPRESENTED same-dest | Guard row 1 (3.0.7): gateway or model unavailable: hang guard 1.5 x (b + expected overhead
1029. VL-21-1029 | EVAL -> EVAL | REPRESENTED same-dest | Guard row 2: judge API error: audit log (REQ-43)
1030. VL-21-1030 | MODULE-tasklist -> MODULE-tasklist | REPRESENTED same-dest | Guard row 3: slow repo search: the pre-pass is killed at min(15 s, 0.10 x b), scope tests/
1031. VL-21-1031 | MODULE-tasklist -> MODULE-tasklist | REPRESENTED same-dest | Guard row 4: missing source or base commit: `no_source`, C2 N/A (INV-013, REQ-01, REQ-03)
1032. VL-21-1032 | MODULE-tasklist -> MODULE-tasklist | REPRESENTED same-dest | Guard row 5: empty sheet: the brief equals Z0 by hash (REQ-23)
1033. VL-21-1033 | MODULE-tasklist -> MODULE-tasklist | REPRESENTED same-dest | Guard row 6: only one class triggered
1034. VL-21-1034 | MODULE-tasklist -> MODULE-tasklist | REPRESENTED same-dest | Guard row 7: all 12 items from one class: quota of 1-2 per class (REQ-19)
1035. VL-21-1035 | MODULE-tasklist -> MODULE-tasklist | REPRESENTED same-dest | Guard row 8: only two reviewers left: replica 1 (REQ-20)
1036. VL-21-1036 | EVAL -> EVAL | REPRESENTED same-dest | Reach by stage (3.0.8): stages Extraction, Selection, Act, Merge survival, Judge credit; p
1037. VL-21-1037 | EVAL -> EVAL | REPRESENTED same-dest | Per-class act-rate band pre-registered before the first arm (REQ-41, INV-004)
1038. VL-21-1038 | EVAL -> EVAL | REPRESENTED same-dest | Found-any and found-blocking reported separately (A-001, A-006)
1039. VL-21-1039 | MODULE-tasklist -> MODULE-tasklist | REPRESENTED same-dest | Blind claim-only verifier (3.0.9): off the critical path, runs only if measured spare time
1040. VL-21-1040 | DROP -> DROP | REPRESENTED same-dest | No messaging (3.0.10): herding (29-34% conformed, about +10 points flips, EXT s4); reviewe
1041. VL-21-1041 | MODULE-tasklist -> MODULE-tasklist | REPRESENTED same-dest | Redesign 1 "Sweep Sheet" positioning (S4): a script finds places to check and attaches too
1042. VL-21-1042 | DROP -> DROP | REPRESENTED same-dest | Sweep Sheet step S0: H1-H4 setup (0 s added)
1043. VL-21-1043 | MODULE-tasklist -> MODULE-tasklist | REPRESENTED same-dest | Step S1, serial pre-pass: reads only the candidate, the source if any, the pre-implementat
1044. VL-21-1044 | MODULE-tasklist -> MODULE-tasklist | REPRESENTED same-dest | Step S2, selection: quota 1-2 items per triggered class, at most 12 items; ALL candidates 
1045. VL-21-1045 | MODULE-tasklist -> MODULE-tasklist | REPRESENTED same-dest | Step S3, assignment: 24 slots = 12 items x 2 of 3 blind reviewers (INV-011)
1046. VL-21-1046 | MODULE-tasklist -> MODULE-tasklist | REPRESENTED same-dest | Step S4, reviewers in parallel and blind: read the candidate and the source, judge the ass
1047. VL-21-1047 | MODULE-tasklist -> MODULE-tasklist | REPRESENTED same-dest | Step S5, post-run checks and promotion (no re-ask; failure gives `check_skipped=true`); st
1048. VL-21-1048 | MODULE-tasklist -> MODULE-tasklist | REPRESENTED same-dest | Slot caps (S4): primary ember 8, luna1 up to 8, luna2 up to 8; haiku panel haiku up to 6 a
1049. VL-21-1049 | MODULE-tasklist -> MODULE-tasklist | REPRESENTED same-dest | Per-reviewer shuffle with a logged seed (EXT s4, anchoring)
1050. VL-21-1050 | MODULE-tasklist -> MODULE-tasklist | REPRESENTED same-dest | Extractor E1 (C1+C6): set-word sentences (every, all, each, complete, exhaustive, found, c
1051. VL-21-1051 | MODULE-tasklist -> MODULE-tasklist | REPRESENTED same-dest | Extractor E2 (C4): the literal pattern or selector in backticked criterion commands tried 
1052. VL-21-1052 | MODULE-tasklist -> MODULE-tasklist | REPRESENTED same-dest | Extractor E3 (C8): existing paths with an edit verb, `git grep -l` of path and stem over t
1053. VL-21-1053 | MODULE-tasklist -> MODULE-tasklist | REPRESENTED same-dest | Extractor E4 (C5): negative criteria ("no remaining", "none", "zero hits") and "N to M" co
1054. VL-21-1054 | MODULE-tasklist -> MODULE-tasklist | REPRESENTED same-dest | Extractor E5 (C2): the rule sentences of the source sections each task cites; runs only wh
1055. VL-21-1055 | MODULE-tasklist -> MODULE-tasklist | REPRESENTED same-dest | Extractor E6 (C3, experimental): backticked literals in read position without a write-posi
1056. VL-21-1056 | MODULE-tasklist -> MODULE-tasklist | REPRESENTED same-dest | Extractor E7 (C7): constraint clauses against dictated-text blocks, token overlap grid
1057. VL-21-1057 | MODULE-tasklist -> MODULE-tasklist | REPRESENTED same-dest | Item format (S4): JSON fields `item_id` (`S<n>`), class, `anchor_text` (up to 200), locati
1058. VL-21-1058 | MODULE-tasklist -> MODULE-tasklist | REPRESENTED same-dest | Question template C1: "What finite check would let a reviewer say yes to this criterion, a
1059. VL-21-1059 | MODULE-tasklist -> MODULE-tasklist | REPRESENTED same-dest | Question template C2: "Does the candidate carry this rule, including each condition and fa
1060. VL-21-1060 | MODULE-tasklist -> MODULE-tasklist | REPRESENTED same-dest | Question template C3: "...Does any row or task write that value?..."
1061. VL-21-1061 | MODULE-tasklist -> MODULE-tasklist | REPRESENTED same-dest | Question template C4: "Apply the criterion's literal pattern to the text this task orders.
1062. VL-21-1062 | MODULE-tasklist -> MODULE-tasklist | REPRESENTED same-dest | Question template C5: "Is each plan-unnamed hit false after the change? Does any task edit
1063. VL-21-1063 | MODULE-tasklist -> MODULE-tasklist | REPRESENTED same-dest | Question template C6: "Name the set this sentence covers. Find one member it leaves out or
1064. VL-21-1064 | MODULE-tasklist -> MODULE-tasklist | REPRESENTED same-dest | Question template C7: "Does each dictated text carry every clause of this constraint? Tick
1065. VL-21-1065 | MODULE-tasklist -> MODULE-tasklist | REPRESENTED same-dest | Question template C8: "Open the referencing file the plan never names. Does it pin the tex
1066. VL-21-1066 | MODULE-tasklist -> MODULE-tasklist | REPRESENTED same-dest | Sweep sheet block (quoted draft): "SWEEP SHEET. A script, not a model, built {{SHEET_PATH}
1067. VL-21-1067 | EVAL -> EVAL | REPRESENTED same-dest | Offline selection-recall gate G0 (INV-001), finding: crude counts on two defect-rich plans
1068. VL-21-1068 | EVAL -> EVAL | REPRESENTED same-dest | Gate G0 rule: before any model arm (1) the share of hold-out or planted defects whose trig
1069. VL-21-1069 | MODULE-tasklist -> MODULE-tasklist | REPRESENTED same-dest | Model roles, primary (S4): ember takes search-routed items (E2, E3, E4, E1 counting items)
1070. VL-21-1070 | MODULE-tasklist -> MODULE-tasklist | REPRESENTED same-dest | Model roles, other panels: haiku up to 6 items only with tool output attached (searches in
1071. VL-21-1071 | EVAL -> EVAL | REPRESENTED same-dest | Sweep Sheet cost model (S4, UNVERIFIED): ledger row 75-90 tokens at 48 tokens/s (luna 4.9k
1072. VL-21-1072 | EVAL -> EVAL | REPRESENTED same-dest | Time baseline (S4): b = the per-package median slowest reviewer; ember+2xluna b = 100-122 
1073. VL-21-1073 | EVAL -> EVAL | REPRESENTED same-dest | Critical path, primary panel: 8 + 1 + (b + 19) + 1 = b + 29: b=100 gives 129 s (+29.0%), k
1074. VL-21-1074 | EVAL -> EVAL | REPRESENTED same-dest | Break-even (S4): pre-pass up to 14 s at b=100; per item up to 2.75 s (8 items), 3.71 s at 
1075. VL-21-1075 | MODULE-tasklist -> MODULE-tasklist | REPRESENTED same-dest | Fallback (S4): if the 5-run luna timing spike (REQ-32) shows more than 2.75 s/item, each l
1076. VL-21-1076 | EVAL -> EVAL | REPRESENTED same-dest | Other panels (S4): haiku b + 37 = 257 s (+16.8%) at 220 and 275 s (+15.5%) at 238; sonnet 
1077. VL-21-1077 | EVAL -> EVAL | REPRESENTED same-dest | Coverage matrix B1 (C1), Redesign 1: act .10-.35, s .35-.70, reach 0.04-0.25
1078. VL-21-1078 | EVAL -> EVAL | REPRESENTED same-dest | Coverage matrix B2 (C1): .15-.40 / .35-.70 / 0.05-0.28
1079. VL-21-1079 | EVAL -> EVAL | REPRESENTED same-dest | Coverage matrix B5 (C2): .20-.45 / .40-.70 / 0.08-0.32
1080. VL-21-1080 | EVAL -> EVAL | REPRESENTED same-dest | Coverage matrix I1 (C3, E6): .03-.15 / .25-.50 / 0.01-0.08
1081. VL-21-1081 | EVAL -> EVAL | REPRESENTED same-dest | Coverage matrix I4 (C4): .50-.75 / .80-.95 / 0.40-0.71
1082. VL-21-1082 | EVAL -> EVAL | REPRESENTED same-dest | Coverage matrix I5 (C5): .35-.60 / .65-.90 / 0.23-0.54
1083. VL-21-1083 | EVAL -> EVAL | REPRESENTED same-dest | Coverage matrix B6 (C6): .05-.20 / .40-.70 / 0.02-0.14
1084. VL-21-1084 | EVAL -> EVAL | REPRESENTED same-dest | Coverage matrix B8 (C6): .10-.30 / .35-.65 / 0.04-0.20
1085. VL-21-1085 | EVAL -> EVAL | REPRESENTED same-dest | Coverage matrix I6 (C7): .15-.35 / .40-.65 / 0.06-0.23
1086. VL-21-1086 | EVAL -> EVAL | REPRESENTED same-dest | Coverage matrix I7 (C8, control, "of 1"): .40-.65 / .85-.95 / 0.34-0.62
1087. VL-21-1087 | EVAL -> EVAL | REPRESENTED same-dest | Coverage-matrix sum, nine issues: 0.92-2.73 (central 1.83) while the printed rows add 0.93
1088. VL-21-1088 | EVAL -> EVAL | REPRESENTED same-dest | Applicability of the extractors (S4): they key on sentence shapes, backticks, quotes, path
1089. VL-21-1089 | MODULE-tasklist -> CORE | REPRESENTED moved(documented) | Re-derive per target (S4): section map, edited-object detector, command dialect, test and 
1090. VL-21-1090 | EVAL -> EVAL | REPRESENTED same-dest | Fixtures and extractor gates (S4): REQ-37 spec fixture (E1, E2, E5) and doc fixture (E4, E
1091. VL-21-1091 | EVAL -> EVAL | REPRESENTED same-dest | Expected gain, Redesign 1 (found of 14 per run, primary): baseline 1.83 measured; H share 
1092. VL-21-1092 | EVAL -> EVAL | REPRESENTED same-dest | I7 for Redesign 1: +0.34 to +0.62 of 1, outside the totals; "best single panel run recorde
1093. VL-21-1093 | EVAL -> EVAL | REPRESENTED same-dest | Reporting rule (S4): H share and redesign share are reported separately, never summed in t
1094. VL-21-1094 | EVAL -> EVAL | REPRESENTED same-dest | Overhead, Redesign 1: elapsed +23.8% (b=122) to +29.0% (b=100); kill-limit +27.2% to +31.0
1095. VL-21-1095 | EVAL -> EVAL | REPRESENTED same-dest | Token overhead, Redesign 1: output baseline 21.3k per package for the ember panel (63.7k h
1096. VL-21-1096 | HARNESS -> HARNESS | REPRESENTED same-dest | Implementation effort, Redesign 1 (unmeasured): shared scaffolding about 450 lines (cards 
1097. VL-21-1097 | EVAL -> EVAL | REPRESENTED same-dest | Redesign 1 failure: extractor miss (Medium)
1098. VL-21-1098 | EVAL -> EVAL | REPRESENTED same-dest | Redesign 1 failure: over-extraction crowds out items (Medium)
1099. VL-21-1099 | EVAL -> EVAL | REPRESENTED same-dest | Redesign 1 failure: rubber-stamp OK-all (Medium; "About 41% of smell-detector items are no
1100. VL-21-1100 | EVAL -> EVAL | REPRESENTED same-dest | Redesign 1 failure: a selection miss repeats in every run (INV-001; G0)
1101. VL-21-1101 | EVAL -> EVAL | REPRESENTED same-dest | Redesign 1 failure: the ledger is lost in an earlier message (INV-002; REQ-17)
1102. VL-21-1102 | EVAL -> EVAL | REPRESENTED same-dest | Redesign 1 failure: a promoted line is rejected by the parser (INV-005; REQ-15)
1103. VL-21-1103 | EVAL -> EVAL | REPRESENTED same-dest | Redesign 1 failure: format-induced demotions (INV-007; 0.914^2 = 0.835; REQ-14)
1104. VL-21-1104 | EVAL -> EVAL | REPRESENTED same-dest | Redesign 1 failure: wrong blockers grow (CB-3, UNSURE non-blocking, gate D4: wrong blocker
1105. VL-21-1105 | EVAL -> EVAL | REPRESENTED same-dest | Redesign 1 failure: displacement of easy finds (INV-014, 0.1-0.9 of 14; CB-5; gate D6 non-
1106. VL-21-1106 | EVAL -> EVAL | REPRESENTED same-dest | Redesign 1 failure: pre-pass time on a large tree (break-even 14 s)
1107. VL-21-1107 | EVAL -> EVAL | REPRESENTED same-dest | Redesign 1 failure: the sheet anchors reviewers on items only
1108. VL-21-1108 | EVAL -> EVAL | REPRESENTED same-dest | Redesign 1 failure: dictation-blind classes C3 and C7 stay narrow (High)
1109. VL-21-1109 | EVAL -> EVAL | REPRESENTED same-dest | Redesign 1 failure: kill/retry at the hang guard (REQ-30)
1110. VL-21-1110 | EVAL -> EVAL | REPRESENTED same-dest | Redesign 1 failure: wrong snapshot (H3 precondition, REQ-03)
1111. VL-21-1111 | EVAL -> EVAL | REPRESENTED same-dest | Redesign 1 failure: the sheet as a ground-truth leak path (AO-6, REQ-34)
1112. VL-21-1112 | MODULE-tasklist -> MODULE-tasklist | REPRESENTED same-dest | Redesign 2 "Recipe Ledger" positioning (S5): the instruction-side answer; no pre-pass and 
1113. VL-21-1113 | DROP -> DROP | REPRESENTED same-dest | Recipe Ledger step R0: H1-H4 (0 s)
1114. VL-21-1114 | MODULE-tasklist -> MODULE-tasklist | REPRESENTED same-dest | Step R1, lens assignment: a launcher lens table, under 1 s, at most 4 recipes per reviewer
1115. VL-21-1115 | MODULE-tasklist -> MODULE-tasklist | REPRESENTED same-dest | Step R2: reviewers in parallel and blind (read the candidate and the driving doc, run each
1116. VL-21-1116 | MODULE-tasklist -> MODULE-tasklist | REPRESENTED same-dest | Step R3: ledger check under 1 s (ledger exists, every assigned recipe has at least 1 row, 
1117. VL-21-1117 | DROP -> DROP | REPRESENTED same-dest | Step R4: normal merge
1118. VL-21-1118 | MODULE-tasklist -> MODULE-tasklist | REPRESENTED same-dest | Re-ask rule, luna (INV-010): NO luna re-ask: the report ends about b + 22 s so b + 52 exce
1119. VL-21-1119 | MODULE-tasklist -> MODULE-tasklist | REPRESENTED same-dest | Re-ask rule, ember (REQ-27): re-ask only if `now + 30 s <= 1.35 b`, else `ledger_missing`;
1120. VL-21-1120 | MODULE-tasklist -> MODULE-tasklist | REPRESENTED same-dest | Lens table, primary panel: ember {C4, C5, C6, C8} 14 rows (four recipes allow 16, the lens
1121. VL-21-1121 | MODULE-tasklist -> MODULE-tasklist | REPRESENTED same-dest | Lens table, haiku panel: haiku {C5, C6, C8} up to 6 rows; luna1 {C1, C2, C3} 14; luna2 {C1
1122. VL-21-1122 | MODULE-tasklist -> MODULE-tasklist | REPRESENTED same-dest | Lens table, sonnet panel: sonnet {C5, C6, C8, C2} up to 8 rows; luna1 {C1, C3, C7} 12; lun
1123. VL-21-1123 | MODULE-tasklist -> MODULE-tasklist | REPRESENTED same-dest | Per-recipe row budget: C1 4, C2 6, C3 4, C4 4, C5 4, C6 4, C7 4, C8 4; never more than 14 
1124. VL-21-1124 | MODULE-tasklist -> MODULE-tasklist | REPRESENTED same-dest | Ledger rule (quoted draft): "RECIPES AND LEDGER. Before you review freely, run the recipes
1125. VL-21-1125 | MODULE-tasklist -> MODULE-tasklist | REPRESENTED same-dest | Recipe R-C1 (quoted draft wording, lines 738-752): finite check plus an instruction-versus
1126. VL-21-1126 | MODULE-tasklist -> MODULE-tasklist | REPRESENTED same-dest | Recipe R-C2: split the driving doc into rules (must/shall/never/only/halts/reports/returns
1127. VL-21-1127 | MODULE-tasklist -> MODULE-tasklist | REPRESENTED same-dest | Recipe R-C3: list read, mapped and required values and find the writer per case, at most 4
1128. VL-21-1128 | MODULE-tasklist -> MODULE-tasklist | REPRESENTED same-dest | Recipe R-C4: the exact text the task orders plus the literal pattern including case, "Do n
1129. VL-21-1129 | MODULE-tasklist -> MODULE-tasklist | REPRESENTED same-dest | Recipe R-C5: the old literal plus one whole-tree search including root docs, mirrors and c
1130. VL-21-1130 | MODULE-tasklist -> MODULE-tasklist | REPRESENTED same-dest | Recipe R-C6: name the set, one count or listing command, compare with the plan's other tas
1131. VL-21-1131 | MODULE-tasklist -> MODULE-tasklist | REPRESENTED same-dest | Recipe R-C7: list the constraint clauses and the dictated texts, tick each clause, at most
1132. VL-21-1132 | MODULE-tasklist -> MODULE-tasklist | REPRESENTED same-dest | Recipe R-C8: `git grep -l -F '<string>' -- tests scripts docs` for each edited file, open 
1133. VL-21-1133 | MODULE-tasklist -> MODULE-tasklist | REPRESENTED same-dest | Recipe storage (REQ-25): each recipe at most 120 words, stored once in one file and quoted
1134. VL-21-1134 | MODULE-tasklist -> MODULE-tasklist | REPRESENTED same-dest | Search-form line (S5): "Search forms you may adapt: `grep -rlF '<path>' <test dirs>`; `gre
1135. VL-21-1135 | MODULE-tasklist -> MODULE-tasklist | REPRESENTED same-dest | Model roles (S5): the same lens sets; ember's idle 60-90 s pays for 4 recipes (about 81 s 
1136. VL-21-1136 | EVAL -> EVAL | REPRESENTED same-dest | Recipe Ledger time budget, formula: same b and caps as Redesign 1 (135.0 at b=100; 164.7 a
1137. VL-21-1137 | EVAL -> EVAL | REPRESENTED same-dest | Recipe Ledger time numbers: b=100: 128 (+28.0%), worst 134 (+34.0%), cap 135.0; b=122: 150
1138. VL-21-1138 | EVAL -> EVAL | REPRESENTED same-dest | Recipe Ledger break-even and fallback: break-even 2.07 s per row at 14 rows (29/14; 29 = 1
1139. VL-21-1139 | EVAL -> EVAL | REPRESENTED same-dest | Recipe Ledger other panels: haiku b + 30 = 250 s (+13.6%) at 220 and 268 s (+12.6%) at 238
1140. VL-21-1140 | EVAL -> EVAL | REPRESENTED same-dest | Recipe Ledger coverage, B1 (C1): act .10-.30, s .50-.85, reach 0.05-0.26; B2 (C1) .10-.30 
1141. VL-21-1141 | EVAL -> EVAL | REPRESENTED same-dest | Recipe Ledger coverage, B5 (C2): .15-.35 / .50-.80 / 0.08-0.28; I1 (C3): .05-.20 / .40-.70
1142. VL-21-1142 | EVAL -> EVAL | REPRESENTED same-dest | Recipe Ledger coverage, I4 (C4): .40-.70 / .60-.90 / 0.24-0.63; I5 (C5): .20-.45 / .50-.80
1143. VL-21-1143 | EVAL -> EVAL | REPRESENTED same-dest | Recipe Ledger coverage, B6 (C6): .05-.20 / .40-.70 / 0.02-0.14; B8 (C6): .10-.30 / .35-.65
1144. VL-21-1144 | EVAL -> EVAL | REPRESENTED same-dest | Recipe Ledger sum and I7: SUM 0.63-2.47 (central 1.55; printed rows add 0.64-2.48); I7 (C8
1145. VL-21-1145 | EVAL -> EVAL | REPRESENTED same-dest | Recipe Ledger applicability: recipes mention no document; specs: C1, C2, C3, C4, C7 read d
1146. VL-21-1146 | MODULE-tasklist -> CORE | REPRESENTED moved(documented) | Recipe Ledger re-derive list: meaning of edits/tests/source, command dialect in recipes an
1147. VL-21-1147 | EVAL -> EVAL | REPRESENTED same-dest | Recipe Ledger expected gain (found of 14, primary): baseline 1.83; H +0.03/+0.14/+0.34; gr
1148. VL-21-1148 | EVAL -> EVAL | REPRESENTED same-dest | Recipe Ledger I7 +0.11 to +0.38 of 1; below Redesign 1 on the sweep classes C5, C6, C8 "be
1149. VL-21-1149 | EVAL -> EVAL | REPRESENTED same-dest | Recipe Ledger overhead: elapsed +23.0% (b=122) to +28.0% (b=100); worst +27.9% to +34.0%; 
1150. VL-21-1150 | HARNESS -> HARNESS | REPRESENTED same-dest | Recipe Ledger implementation effort (unmeasured): shared scaffolding about 450; recipe tex
1151. VL-21-1151 | EVAL -> EVAL | REPRESENTED same-dest | Recipe Ledger failure, compliance (High): terse luna writes OK rows without doing the step
1152. VL-21-1152 | EVAL -> EVAL | REPRESENTED same-dest | Recipe Ledger failure: prompt length hurts small models (arm K, D7)
1153. VL-21-1153 | EVAL -> EVAL | REPRESENTED same-dest | Recipe Ledger failure: a single point of failure per class (C5, C6, C8 only in ember; C1, 
1154. VL-21-1154 | EVAL -> EVAL | REPRESENTED same-dest | Recipe Ledger failure: the row budget forces a salience choice (T2 again in a smaller spac
1155. VL-21-1155 | EVAL -> EVAL | REPRESENTED same-dest | Recipe Ledger failure: ember false hits
1156. VL-21-1156 | EVAL -> EVAL | REPRESENTED same-dest | Recipe Ledger failure: wrong blockers grow ("Earlier 2x ember panels added 2.75-3.25 wrong
1157. VL-21-1157 | EVAL -> EVAL | REPRESENTED same-dest | Recipe Ledger failure: the ledger is lost; no repair path for luna (High); a promoted line
1158. VL-21-1158 | EVAL -> EVAL | REPRESENTED same-dest | Recipe Ledger failure: displacement (D6, REQ-42); time at the worst case +34.0% (1 s slack
1159. VL-21-1159 | KNOWLEDGE -> KNOWLEDGE | REPRESENTED same-dest | Comparison (S5a), mechanism: Redesign 1 extracts at most 12 typed items with tool output a
1160. VL-21-1160 | EVAL -> EVAL | REPRESENTED same-dest | Comparison, classes: strong classes R1 C4, C5, C8; R2 C4 (reading) and below R1 on C5, C6,
1161. VL-21-1161 | DROP -> DROP | REPRESENTED same-dest | Comparison numbers: found of 14 low/central/high 1.9/3.3/4.8 versus 1.6/3.0/4.5; shares gr
1162. VL-21-1162 | EVAL -> EVAL | REPRESENTED same-dest | Comparison, deterministic component and portability: R1 deterministic (pre-pass E1-E7, sel
1163. VL-21-1163 | EVAL -> EVAL | REPRESENTED same-dest | Comparison, main risk: R1 a selection miss repeats per document and rubber-stamp OK; R2 co
1164. VL-21-1164 | EVAL -> EVAL | REPRESENTED same-dest | Comparison, tests of the seed question: R1 "model needs a script"; R2 "instruction change 
1165. VL-21-1165 | DROP -> DROP | REPRESENTED same-dest | Seed answer (1): C2, C4, C5, C6, C8 and broad C7 are general; C1 and C3 weak
1166. VL-21-1166 | DROP -> DROP | REPRESENTED same-dest | Seed answer (2): instruction-only is untested; Redesign 2 tests it, arm K shows the value 
1167. VL-21-1167 | DROP -> DROP | REPRESENTED same-dest | Seed answer (3): harness fixes about 0.14 of 14 (0.03-0.34), measured as Z0 minus Z0-raw
1168. VL-21-1168 | DROP -> DROP | REPRESENTED same-dest | Seed answer (4): pre-pass generality shown only by planted plus hold-out results (REQ-21, 
1169. VL-21-1169 | DROP -> DROP | REPRESENTED same-dest | Seed answer (5): the model keeps every OK/PROBLEM/UNSURE call and claim; the script never 
1170. VL-21-1170 | MODULE-tasklist -> MODULE-tasklist | REPRESENTED same-dest | Recommendation (S5a, lines 991-993): "Run both redesigns in the section 5 experiment. Buil
1171. VL-21-1171 | EVAL -> EVAL | REPRESENTED same-dest | Validation principle (S6a): "The three study packages are never evidence for adoption." Th
1172. VL-21-1172 | DROP -> DROP | REPRESENTED same-dest | Hold-out sets HO-1..HO-6 restated (S6a): HO-1 docs-only plan 11 items (Stage 1 decision); 
1173. VL-21-1173 | EVAL -> EVAL | REPRESENTED same-dest | Planted set: 6 full-size real plans, at least 8 competing candidates per class, one plante
1174. VL-21-1174 | EVAL -> EVAL | REPRESENTED same-dest | Clean twins: the same 6 plans without planted defects, for the false-positive rate
1175. VL-21-1175 | EVAL -> EVAL | REPRESENTED same-dest | Documentation arm: about 8 delivered docs that carried a false universal sentence and a re
1176. VL-21-1176 | EVAL -> EVAL | REPRESENTED same-dest | Ground-truth process (S6a): GT for HO-1..5 written from existing review reports and plan q
1177. VL-21-1177 | DROP -> DROP | REPRESENTED same-dest | Caution: remove `.dev/reflect/`, `artifacts/`, `progress.md` from sandboxes (REQ-04)
1178. VL-21-1178 | EVAL -> EVAL | REPRESENTED same-dest | Caution: "Verify that the reviewed plan equals the plan in the package (sha256 against the
1179. VL-21-1179 | EVAL -> EVAL | REPRESENTED same-dest | Caution: GT from Tier-2 reviewers is capped at what those reviewers found ("Missed by chea
1180. VL-21-1180 | EVAL -> EVAL | REPRESENTED same-dest | Arms (S6a): Z0-raw (HO-1..3 only; harness share), Z0 (control and time baseline), K (Z0 pl
1181. VL-21-1181 | EVAL -> EVAL | REPRESENTED same-dest | Panel-variant arms: Zh/SSh/RLh (haiku + 2x luna) and Zs/SSs/RLs (sonnet + 2x luna, compari
1182. VL-21-1182 | EVAL -> EVAL | REPRESENTED same-dest | Run counts: Stage 1 = 4 docs x 4 arms x 5 = 80, plus Z0-raw 3 x 5 = 15, = 95; Stage 2 (onl
1183. VL-21-1183 | EVAL -> EVAL | REPRESENTED same-dest | Judging: one blind Opus judge per run-package, a second judge on 15% (REQ-43)
1184. VL-21-1184 | HARNESS -> HARNESS | REPRESENTED same-dest | Pre-experiment checks: a 5-run luna timing spike (REQ-32; sets fallbacks 6 items per luna,
1185. VL-21-1185 | EVAL -> EVAL | REPRESENTED same-dest | Consistency (S6a): consistent = reached in at least 60% of runs (3 of 5); primary metric =
1186. VL-21-1186 | EVAL -> EVAL | REPRESENTED same-dest | Gate G0 (offline): SS selection recall >= a pre-registered floor and beats random; both re
1187. VL-21-1187 | EVAL -> EVAL | REPRESENTED same-dest | Gate D1 (time): per-package median <= 1.35 x Z0, p90 <= 1.50 x, kills <= 10%, intention-to
1188. VL-21-1188 | EVAL -> EVAL | REPRESENTED same-dest | Gate D2 (effect): mean found fraction >= Z0 + 0.12 absolute, 90% bootstrap lower bound > Z
1189. VL-21-1189 | EVAL -> EVAL | REPRESENTED same-dest | Gate D3 (consistency): at least Z0's count + 3 consistent items
1190. VL-21-1190 | EVAL -> EVAL | REPRESENTED same-dest | Gate D4 (precision): wrong blockers <= Z0 + 1.0 per run; blocking on clean twins <= Z0 + 0
1191. VL-21-1191 | EVAL -> EVAL | REPRESENTED same-dest | Gate D5 (generality): planted detection >= 0.40 on at least 3 of 5 general classes (C2, C4
1192. VL-21-1192 | EVAL -> EVAL | REPRESENTED same-dest | Gate D6 (non-regression): items Z0 reaches at >= 0.5 stay within 0.10; blocking gate
1193. VL-21-1193 | EVAL -> EVAL | REPRESENTED same-dest | Gate D7 (beats the checklist): gain over K >= 0.04 absolute, else K wins
1194. VL-21-1194 | EVAL -> EVAL | REPRESENTED same-dest | Outcomes (S6a): neither passes, keep Z0; one passes, adopt; both pass, take the higher fou
1195. VL-21-1195 | EVAL -> EVAL | REPRESENTED same-dest | Power (S6a): low; Stage 1 decision sets hold about 36-40 items (HO-1 11, HO-2 4-8, HO-3 12
1196. VL-21-1196 | DROP -> DROP | REPRESENTED same-dest | REQ-01 (S6b, 6.1 harness and brief): the source is named only if it exists, else `no_sourc
1197. VL-21-1197 | DROP -> DROP | REPRESENTED same-dest | REQ-02: truncate anchor/anchor2 to 200 and claim to 300, with the real parser
1198. VL-21-1198 | DROP -> DROP | REPRESENTED same-dest | REQ-03: the sandbox at the base commit (or a recorded working tree)
1199. VL-21-1199 | DROP -> DROP | REPRESENTED same-dest | REQ-04: the sandbox has no `.dev/reflect/`, `artifacts/`, `progress.md`, no package report
1200. VL-21-1200 | DROP -> DROP | REPRESENTED same-dest | REQ-05: CB-1..CB-5 verbatim; grading rule, six categories and judge unchanged
1201. VL-21-1201 | MODULE-tasklist -> MODULE-tasklist | REPRESENTED same-dest | REQ-06 (6.2 registry and ledger): the eight cards validate, each recipe is at most 120 wor
1202. VL-21-1202 | DROP -> DROP | REPRESENTED same-dest | REQ-07: the lint (4-word sequences, names)
1203. VL-21-1203 | DROP -> DROP | REPRESENTED same-dest | REQ-08: swap test plus second-author review
1204. VL-21-1204 | CORE -> CORE | REPRESENTED same-dest | REQ-09: rendered briefs hold no `src/superclaude/` path (grep)
1205. VL-21-1205 | DROP -> DROP | REPRESENTED same-dest | REQ-10: a new class = one card plus an optional extractor
1206. VL-21-1206 | DROP -> DROP | REPRESENTED same-dest | REQ-11: findings may carry class/probe/src and the existing merge tests pass
1207. VL-21-1207 | DROP -> DROP | REPRESENTED same-dest | REQ-12: fallback (a) a pre-pass or lens failure gives the isolated brief with `fallback=tr
1208. VL-21-1208 | DROP -> DROP | REPRESENTED same-dest | REQ-13: ledger-v1 in the final message above a single findings block, real parser
1209. VL-21-1209 | CORE -> CORE | REPRESENTED same-dest | REQ-14: the quote tests use the same flattening as `findings.py`
1210. VL-21-1210 | DROP -> DROP | REPRESENTED same-dest | REQ-15: the promotion function
1211. VL-21-1211 | DROP -> DROP | REPRESENTED same-dest | REQ-16: an unsupported PROBLEM is demoted; blocking needs the grading sentence plus two qu
1212. VL-21-1212 | DROP -> DROP | REPRESENTED same-dest | REQ-17: `ledger_missing` <= 10%
1213. VL-21-1213 | DROP -> DROP | REPRESENTED same-dest | REQ-18 (6.3 Redesign 1): a non-model, read-only, byte-identical serial pre-pass killed at 
1214. VL-21-1214 | DROP -> DROP | REPRESENTED same-dest | REQ-19: at most 12 items, quota 1-2 per class, log candidates, dropped items and the seed 
1215. VL-21-1215 | DROP -> DROP | REPRESENTED same-dest | REQ-20: 24-slot assignment with caps summing to 24
1216. VL-21-1216 | DROP -> DROP | REPRESENTED same-dest | REQ-21: E1-E4 and E7 reach recall >= 0.8 on at least 3 non-study plans; E6 experimental
1217. VL-21-1217 | DROP -> DROP | REPRESENTED same-dest | REQ-22: offline selection-recall gate
1218. VL-21-1218 | DROP -> DROP | REPRESENTED same-dest | REQ-23: an empty sheet equals the Z0 brief (hash)
1219. VL-21-1219 | DROP -> DROP | REPRESENTED same-dest | REQ-24: search scope and time bound
1220. VL-21-1220 | DROP -> DROP | REPRESENTED same-dest | REQ-25 (6.4 Redesign 2): eight recipes in one file, at most 4 per reviewer, duplicated cla
1221. VL-21-1221 | DROP -> DROP | REPRESENTED same-dest | REQ-26: row budget, at most 14 rows per lens, `NONE FOUND`
1222. VL-21-1222 | DROP -> DROP | REPRESENTED same-dest | REQ-27: no luna re-ask; ember re-ask iff `now + 30 s <= 1.35 b`
1223. VL-21-1223 | MODULE-tasklist -> MODULE-tasklist | REPRESENTED same-dest | REQ-28: the `ran` field is cross-checked with the transcript tool calls
1224. VL-21-1224 | EVAL -> EVAL | REPRESENTED same-dest | REQ-29 (6.5 time): the +35% is judged on per-package medians against the same-day Z0 in th
1225. VL-21-1225 | DROP -> DROP | REPRESENTED same-dest | REQ-30: hang guard 1.5 x (b + expected overhead), kills and retries counted per arm, inten
1226. VL-21-1226 | DROP -> DROP | REPRESENTED same-dest | REQ-31: the break-evens (pre-pass 14 s; 2.75 s per item at b=100; row 2.07 s) are reported
1227. VL-21-1227 | DROP -> DROP | REPRESENTED same-dest | REQ-32: the 5-run luna timing spike
1228. VL-21-1228 | DROP -> DROP | REPRESENTED same-dest | REQ-33 (6.6 contamination): freeze by git tag before GT
1229. VL-21-1229 | DROP -> DROP | REPRESENTED same-dest | REQ-34: reviewers never get ground truth (grep)
1230. VL-21-1230 | DROP -> DROP | REPRESENTED same-dest | REQ-35: leave-one-class-out within 15 points
1231. VL-21-1231 | DROP -> DROP | REPRESENTED same-dest | REQ-36: GT hashed before the first arm; planted defects by someone who has not seen the re
1232. VL-21-1232 | DROP -> DROP | REPRESENTED same-dest | REQ-37 (6.7 applicability): spec and doc fixtures (E1, E2, E5 on spec; E4, E1 on doc)
1233. VL-21-1233 | DROP -> DROP | REPRESENTED same-dest | REQ-38: the registry README holds the per-target re-derive list
1234. VL-21-1234 | EVAL -> EVAL | REPRESENTED same-dest | REQ-39 (6.8 reporting): all metrics come from one script over the run folders
1235. VL-21-1235 | DROP -> DROP | REPRESENTED same-dest | REQ-40: gains reported as H share, prompting share (K minus Z0) and redesign share, never 
1236. VL-21-1236 | DROP -> DROP | REPRESENTED same-dest | REQ-41: reach per stage plus pre-registered per-class act bands
1237. VL-21-1237 | EVAL -> EVAL | REPRESENTED same-dest | REQ-42: displacement = non-probe findings per run; D6 blocking
1238. VL-21-1238 | DROP -> DROP | REPRESENTED same-dest | REQ-43: blind Opus judge, frozen rubric, second judge 15%, API-error audit
1239. VL-21-1239 | DROP -> DROP | REPRESENTED same-dest | REQ-44: arms, run counts and gates committed before the first hold-out run
1240. VL-21-1240 | DROP -> DROP | REPRESENTED same-dest | REQ-45: claim wording "raises the per-run found fraction; consistency is expected only for
1241. VL-21-1241 | DROP -> DROP | REPRESENTED same-dest | REQ-46: the optional verifier runs off the critical path and cannot add claims
1242. VL-21-1242 | DROP -> DROP | REPRESENTED same-dest | Unverified list (S6c) 1: all probabilities, act rates and selection factors s are planning
1243. VL-21-1243 | DROP -> DROP | REPRESENTED same-dest | Unverified 2: 48 tokens/s comes from one luna run (4.9k tokens in 102 s) and is unconfirme
1244. VL-21-1244 | DROP -> DROP | REPRESENTED same-dest | Unverified 3: 2 s per item or row, the 8 s pre-pass, ledger compliance and the line counts
1245. VL-21-1245 | EVAL -> EVAL | REPRESENTED same-dest | Unverified 4: launcher facts and `findings.py` rules were "read in the source and cited wi
1246. VL-21-1246 | DROP -> DROP | REPRESENTED same-dest | Unverified 5: that unknown telemetry keys are accepted comes from the hand-off table; REQ-
1247. VL-21-1247 | DROP -> DROP | REPRESENTED same-dest | Unverified 6: equality of the reviewed plan and the package plan (sha256) is unchecked
1248. VL-21-1248 | DROP -> DROP | REPRESENTED same-dest | Unverified 7: 348 s is a per-run mean summed over three packages
1249. VL-21-1249 | EVAL -> EVAL | REPRESENTED same-dest | Unverified 8: the harness +0.14 (0.03-0.34) is bottom-up, and a 0.1 overlap on I4, I1, B5 
1250. VL-21-1250 | DROP -> DROP | REPRESENTED same-dest | Unverified 9: the best single panel run recorded is 4 of 14, so the high ends are optimist
1251. VL-21-1251 | EVAL -> EVAL | REPRESENTED same-dest | Unverified 10: no wording (CB-1..5, ledger rule, sheet block, question templates, recipes)
1252. VL-21-1252 | DROP -> DROP | REPRESENTED same-dest | Unverified 11: statistical power is low
1253. VL-21-1253 | KNOWLEDGE -> KNOWLEDGE | REPRESENTED same-dest | Provenance (S6d): base = Variant 2 for most sections; Variant 1 for the 3.0 shared scaffol
1254. VL-21-1254 | KNOWLEDGE -> KNOWLEDGE | REPRESENTED same-dest | "Invariant findings: 14 of 14 are resolved in this document" (line 1237)
1255. VL-21-1255 | DROP -> DROP | REPRESENTED same-dest | INV-001 (S6d): selection recall, resolved in 3.0.8, G0, REQ-22
1256. VL-21-1256 | DROP -> DROP | REPRESENTED same-dest | INV-002: the ledger must be in the final message (3.0.4, REQ-13/17)
1257. VL-21-1257 | DROP -> DROP | REPRESENTED same-dest | INV-003: time arithmetic (D1, REQ-29/31/32)
1258. VL-21-1258 | DROP -> DROP | REPRESENTED same-dest | INV-004: the consistency claim narrowed (REQ-41/45)
1259. VL-21-1259 | DROP -> DROP | REPRESENTED same-dest | INV-005: promotion rules (REQ-15)
1260. VL-21-1260 | KNOWLEDGE -> KNOWLEDGE | REPRESENTED same-dest | INV-006: matrices recomputed once
1261. VL-21-1261 | DROP -> DROP | REPRESENTED same-dest | INV-007: format-induced demotions (REQ-14)
1262. VL-21-1262 | DROP -> DROP | REPRESENTED same-dest | INV-008: hang guard (REQ-30)
1263. VL-21-1263 | DROP -> DROP | REPRESENTED same-dest | INV-009: planted defects in full-size plans (D5, REQ-36)
1264. VL-21-1264 | DROP -> DROP | REPRESENTED same-dest | INV-010: row budget and no luna re-ask (REQ-26/27)
1265. VL-21-1265 | DROP -> DROP | REPRESENTED same-dest | INV-011: assignment over 24 slots (REQ-20)
1266. VL-21-1266 | DROP -> DROP | REPRESENTED same-dest | INV-012: a serial pre-pass (REQ-18)
1267. VL-21-1267 | DROP -> DROP | REPRESENTED same-dest | INV-013: no source or no base commit (REQ-01/03)
1268. VL-21-1268 | DROP -> DROP | REPRESENTED same-dest | INV-014: displacement and the free-review floor (CB-5, D6, REQ-42)
1269. VL-21-1269 | EVAL -> EVAL | REPRESENTED same-dest | Investigation-generality (IG; S7; 170 lines, 31,216 B; date 2026-11-14): read-only; questi
1270. VL-21-1270 | EVAL -> EVAL | REPRESENTED same-dest | Cross-effort link (S7): the IG evidence base is E1's artefact class (143 `R/` = `.dev/refl
1271. VL-21-1271 | EVAL -> EVAL | REPRESENTED same-dest | IG method limits: phrase-based Grep over REPORT.md, merged-*.md, reviewer cards, merged-ve
1272. VL-21-1272 | EVAL -> EVAL | REPRESENTED same-dest | IG searched material: all 48 `D/` packages, all 143 `R/` folders, `E346/phase1/REPORT.md` 
1273. VL-21-1273 | EVAL -> EVAL | REPRESENTED same-dest | IG ledger scan: only 5 non-eval packages have `blocked` lines (designSpec-20261108-165559 
1274. VL-21-1274 | DROP -> DROP | REPRESENTED same-dest | IG class definitions and the move per class: C1 ask a finite check plus equal scope; C2 wa
1275. VL-21-1275 | EVAL -> EVAL | REPRESENTED same-dest | IG instance counts (other docs / P): C1 3 (+1 borderline) / 3; C2 6 / 6; C3 3 / 3 (weak: 1
1276. VL-21-1276 | EVAL -> EVAL | REPRESENTED same-dest | C1 instances: review-severity-rule plan `D/TASK-WF-removeTheAnyIssu-20261102-053741` (thre
1277. VL-21-1277 | EVAL -> EVAL | REPRESENTED same-dest | C2 instances (6, all P): reflect reports `pre-phase3CodegraphA-20261029205359` (M-17), `pr
1278. VL-21-1278 | EVAL -> EVAL | REPRESENTED same-dest | C3 instances (3, weak): worker-contract spec ledger D11 (blocking; `X346/p17/ledger.json`,
1279. VL-21-1279 | EVAL -> EVAL | REPRESENTED same-dest | C4 instances (9 docs; 8 P): reflect reports for workflowSource (D-002), refactorIronClau, 
1280. VL-21-1280 | EVAL -> EVAL | REPRESENTED same-dest | C5 instances (9; 3 P): `scIssueClaimPipe` M-3; `writeTheP1Static` merged card; `workerCont
1281. VL-21-1281 | EVAL -> EVAL | REPRESENTED same-dest | C6 instances (12; 4 P): `workerContractFo` M-3; `writeTheP2Static` (line 307); `brainstorm
1282. VL-21-1282 | EVAL -> EVAL | REPRESENTED same-dest | C7 instances: `implementIronbel` (B-2), `implementGitHubI` (M-F2 blocking, PLAN:36 vs 39),
1283. VL-21-1283 | EVAL -> EVAL | REPRESENTED same-dest | C8 instances (6; 5 P): `phase3CodegraphA` (M-03, `tests/core/test_how_we_work_routing_tabl
1284. VL-21-1284 | EVAL -> EVAL | REPRESENTED same-dest | Class X8 (not among the ten): environment flake (1 instance, I only, `fixIronbellyOrgI-202
1285. VL-21-1285 | EVAL -> EVAL | REPRESENTED same-dest | X-class details: X3 conflicting source statements (3; designSpec-20261108-165559 SD-1 `spe
1286. VL-21-1286 | EVAL -> EVAL | REPRESENTED same-dest | Observation (S7): C4, C5, C6 and C8 each have more distinct docs than X3-X6
1287. VL-21-1287 | EVAL -> EVAL | REPRESENTED same-dest | Hold-out H1 (IG; = HO-5): worker-contract spec `X346/p17/spec-original.md`, `ledger.json` 
1288. VL-21-1288 | EVAL -> EVAL | REPRESENTED same-dest | Hold-out H2 (= HO-2): plan `D/TASK-WF-implementIronbel-20261104-130647` (134 lines), 4 blo
1289. VL-21-1289 | EVAL -> EVAL | REPRESENTED same-dest | Hold-out H3 (= HO-4): plan `D/TASK-WF-phase3CodegraphA-20261029-204913` (236 lines): 19 fi
1290. VL-21-1290 | EVAL -> EVAL | REPRESENTED same-dest | Hold-out H4 (= HO-3): plan `D/TASK-WF-scIssueClaimPipe-20261107-063237` (163 lines): 6 blo
1291. VL-21-1291 | EVAL -> EVAL | REPRESENTED same-dest | Hold-out H5 (= HO-1): plan `D/TASK-WF-workerContractFo-20261106-214402` (89 lines, docs-on
1292. VL-21-1292 | EVAL -> EVAL | REPRESENTED same-dest | Hold-out H6 (= HO-6): `D/TASK-WF-designSpec-20261108-165559` (#441): SD-1..3, found by bui
1293. VL-21-1293 | EVAL -> EVAL | REPRESENTED same-dest | Spares and suggested set: spares `R/pre-TASK-WF-writeTheP1Static-...` (8 blocking MF-01..0
1294. VL-21-1294 | DROP -> DROP | REPRESENTED same-dest | Hold-out cautions: remove `.dev/reflect/`, `artifacts/`, `progress.md` from the sandbox (i
1295. VL-21-1295 | DROP -> DROP | REPRESENTED same-dest | IG conclusion: general = at least 3 other docs; weak = 1-2 (or 3 mostly low-grade); verdic
1296. VL-21-1296 | EVAL -> EVAL | REPRESENTED same-dest | IG claim guidance: C1 only "list-every-site / closed-list-for-open-set" (3 docs); C3 only 
1297. VL-21-1297 | DROP -> DROP | REPRESENTED same-dest | IG limits: one repo, one owner, one pipeline (`/sc:workflow` markdown + prompt plans); phr
1298. VL-21-1298 | EVAL -> EVAL | REPRESENTED same-dest | IG UNVERIFIED (line 170): each `D/` plan equals the plan reflect reviewed (no sha comparis
1299. VL-21-1299 | EVAL -> EVAL | REPRESENTED same-dest | Naming drift (S7 note): the seed-brief table uses "GT" labels while the merged spec forbid
1300. VL-21-1300 | KNOWLEDGE -> KNOWLEDGE | REPRESENTED same-dest | External research (EXT; S8; 105 lines, 26,037 B; date 2026-11-13): "All queries were gener
1301. VL-21-1301 | KNOWLEDGE -> KNOWLEDGE | REPRESENTED same-dest | EXT 1.1 narrow single-question passes: SEI/CMU blog (LLMs "perform much better when given 
1302. VL-21-1302 | KNOWLEDGE -> KNOWLEDGE | REPRESENTED same-dest | EXT 1.2 multi-pass ensembles: Multi-Review / SWR-Bench (Gemini-2.5-Flash Self-Agg n=10 F1 
1303. VL-21-1303 | KNOWLEDGE -> KNOWLEDGE | REPRESENTED same-dest | EXT 1.3 one lens per pass / reading techniques: Porter/Votta/Basili scenario readers beat 
1304. VL-21-1304 | KNOWLEDGE -> KNOWLEDGE | REPRESENTED same-dest | EXT 1.4 tool-augmented versus reading: CBSoft 2026 (144 PRs): neither static concat nor ag
1305. VL-21-1305 | KNOWLEDGE -> KNOWLEDGE | REPRESENTED same-dest | EXT 1.5 deterministic pre-pass: Tencent static analysis + LLM triage (433 alarms): basic p
1306. VL-21-1306 | KNOWLEDGE -> KNOWLEDGE | REPRESENTED same-dest | EXT 1.6 structured output with evidence: retrieve-then-verify (verbatim quote); StrictCita
1307. VL-21-1307 | KNOWLEDGE -> KNOWLEDGE | REPRESENTED same-dest | EXT 2 RE evidence classes are general: ISO/IEC/IEEE 29148:2018 clause 5 (secondary source)
1308. VL-21-1308 | KNOWLEDGE -> KNOWLEDGE | REPRESENTED same-dest | EXT 3 cost and latency: Multi-Review plateau n=5-10, cheap x5 beats expensive x1 (OPENED);
1309. VL-21-1309 | KNOWLEDGE -> KNOWLEDGE | REPRESENTED same-dest | EXT 4 cautions: checklist alone no better than ad hoc; Datadog: tuned-to-catch prompts mis
1310. VL-21-1310 | KNOWLEDGE -> KNOWLEDGE | REPRESENTED same-dest | EXT lever: narrow single-question passes: moderate
1311. VL-21-1311 | KNOWLEDGE -> KNOWLEDGE | REPRESENTED same-dest | EXT lever: generic checklist: weak
1312. VL-21-1312 | KNOWLEDGE -> KNOWLEDGE | REPRESENTED same-dest | EXT lever: deterministic pre-pass + the model judges each item: moderate for "tool narrows
1313. VL-21-1313 | KNOWLEDGE -> KNOWLEDGE | REPRESENTED same-dest | EXT levers: agentic free-roaming tools weak/mixed; same-model passes + aggregator moderate
1314. VL-21-1314 | KNOWLEDGE -> KNOWLEDGE | REPRESENTED same-dest | EXT levers: a separate verify pass per finding with an evidence quote moderate; structured
1315. VL-21-1315 | KNOWLEDGE -> KNOWLEDGE | REPRESENTED same-dest | EXT levers: redact-and-retry weak-moderate; debate or showing conclusions negative; a blin
1316. VL-21-1316 | EVAL -> EVAL | REPRESENTED same-dest | EXT gaps (S8 section 6): no controlled LLM study of scenario-per-class vs checklist for sp
1317. VL-21-1317 | KNOWLEDGE -> KNOWLEDGE | REPRESENTED same-dest | External-evidence note (overlap matrix): EXT is the only OUTSIDE evidence in this brainsto
1318. VL-21-1318 | KNOWLEDGE -> KNOWLEDGE | REPRESENTED same-dest | Debate run command (S9, `return-contract.yaml` line 3): `/sc:adversarial --compare variant
1319. VL-21-1319 | KNOWLEDGE -> KNOWLEDGE | REPRESENTED same-dest | Adversarial return contract (S9, 11 lines): `convergence_score: 0.9756` ("strict: 40 of 41
1320. VL-21-1320 | KNOWLEDGE -> KNOWLEDGE | REPRESENTED same-dest | Variant V1 sonnet:architect (61,742 B, S9a): highest raw score; class cards as data, extra
1321. VL-21-1321 | KNOWLEDGE -> KNOWLEDGE | REPRESENTED same-dest | Variant V2 sonnet:analyzer (52,788 B): BASE of the merge; sourced harness share +0.14, iss
1322. VL-21-1322 | KNOWLEDGE -> KNOWLEDGE | REPRESENTED same-dest | Variant V3 haiku:backend (39,846 B): lowest; blind claim-only verifier, real-parser check,
1323. VL-21-1323 | KNOWLEDGE -> KNOWLEDGE | REPRESENTED same-dest | Launch scripts: `launch-variants.sh` (6,090 B), `launch-debate.sh` (2,566 B), `sessions/de
1324. VL-21-1324 | KNOWLEDGE -> KNOWLEDGE | REPRESENTED same-dest | Scoring method (S9b, `base-selection.md` 219 lines): quant 50% (regex counts, `scoring/qua
1325. VL-21-1325 | KNOWLEDGE -> KNOWLEDGE | REPRESENTED same-dest | Quant scores (S9b): requirement_coverage V1 1.0000 (28/28 seed-brief patterns), V2 1.0000,
1326. VL-21-1326 | KNOWLEDGE -> KNOWLEDGE | REPRESENTED same-dest | Qual scores (S9b): Completeness V1 5/5, V2 5/5, V3 3/5; Correctness 3/5, 2/5, 1/5; Structu
1327. VL-21-1327 | DROP -> DROP | REPRESENTED same-dest | Criterion finding CR1 (S9b): arithmetic: V2 stated 128-150 s but its table sums 129-151; 2
1328. VL-21-1328 | DROP -> DROP | REPRESENTED same-dest | Criterion finding CR2: V3 not feasible within +35% (timeout 165 + 6 + 3 exceeds the cap)
1329. VL-21-1329 | KNOWLEDGE -> KNOWLEDGE | REPRESENTED same-dest | Criterion finding CR3 (terminology): V1/V2 hold-out H2/H5 collide with harness fixes H1-H4
1330. VL-21-1330 | DROP -> DROP | REPRESENTED same-dest | Criterion finding CR4: V1 luna +1.5k tokens at 48 tok/s is about 31 s versus the stated +1
1331. VL-21-1331 | DROP -> DROP | REPRESENTED same-dest | Criterion finding RK1: risks without probability (all variants NOT MET; fixed in the merge
1332. VL-21-1332 | KNOWLEDGE -> KNOWLEDGE | REPRESENTED same-dest | Combined scores (S9b): V1 0.4973 + 0.4500 = 0.9473; V2 0.4991 + 0.4000 = 0.8991; V3 0.4784
1333. VL-21-1333 | KNOWLEDGE -> KNOWLEDGE | REPRESENTED same-dest | Selected base (S9b): V2 (sonnet:analyzer): all three advocates conceded to V2 on the sourc
1334. VL-21-1334 | KNOWLEDGE -> KNOWLEDGE | REPRESENTED same-dest | Preserved from V2 (6): the sourced harness share and three-share reporting never summed; t
1335. VL-21-1335 | KNOWLEDGE -> KNOWLEDGE | REPRESENTED same-dest | Incorporated from V1: class cards as data, block-kind list, extractor blind spots, quote v
1336. VL-21-1336 | KNOWLEDGE -> KNOWLEDGE | REPRESENTED same-dest | Incorporated from V3: blind claim-only verifier as an off-path audit only, real-parser che
1337. VL-21-1337 | KNOWLEDGE -> KNOWLEDGE | REPRESENTED same-dest | Incorporated from the debate: quota 1-2 per class with ranked fill (Q3), one session per r
1338. VL-21-1338 | KNOWLEDGE -> KNOWLEDGE | REPRESENTED same-dest | Invariant probe summary (S9c, `invariant-probe.md` 252 lines): 14 findings, 6 HIGH, 8 MEDI
1339. VL-21-1339 | DROP -> DROP | REPRESENTED same-dest | Probe INV-001 (HIGH, sufficiency): assumption "an item exists whenever its trigger shape i
1340. VL-21-1340 | DROP -> DROP | REPRESENTED same-dest | Probe INV-002 (HIGH, state_variables): assumption "a ledger written first ends up in the r
1341. VL-21-1341 | EVAL -> EVAL | REPRESENTED same-dest | Probe INV-003 (HIGH, count_divergence): assumption "Redesign A fits +35% at about 2 s/item
1342. VL-21-1342 | EVAL -> EVAL | REPRESENTED same-dest | Probe INV-004 (HIGH, sufficiency): assumption "designs make cheap panels find missed issue
1343. VL-21-1343 | DROP -> DROP | REPRESENTED same-dest | Probe INV-005 (HIGH, interaction_effects): assumption "a ledger row without a finding can 
1344. VL-21-1344 | DROP -> DROP | REPRESENTED same-dest | Probe INV-006 (HIGH, state_variables): assumption "planning gain can be the mean of the V1
1345. VL-21-1345 | DROP -> DROP | REPRESENTED same-dest | Probe INV-007 (MEDIUM, guard_conditions): assumption "the quote check is a safe filter and
1346. VL-21-1346 | DROP -> DROP | REPRESENTED same-dest | Probe INV-008 (MEDIUM, interaction_effects): assumption "the 1.5x hang guard doesn't disca
1347. VL-21-1347 | DROP -> DROP | REPRESENTED same-dest | Probe INV-009 (MEDIUM, sufficiency): assumption "planted-defect documents show detection o
1348. VL-21-1348 | DROP -> DROP | REPRESENTED same-dest | Probe INV-010 (MEDIUM, collection_boundaries): assumption "lenses fit a 12-line ledger and
1349. VL-21-1349 | DROP -> DROP | REPRESENTED same-dest | Probe INV-011 (MEDIUM, count_divergence): assumption "12 items x 2 reviewers / 3 = about 8
1350. VL-21-1350 | DROP -> DROP | REPRESENTED same-dest | Probe INV-012 (MEDIUM, state_variables): assumption "a pre-pass off the critical path can 
1351. VL-21-1351 | DROP -> DROP | REPRESENTED same-dest | Probe INV-013 (MEDIUM, guard_conditions): assumption "every target has a driving document 
1352. VL-21-1352 | DROP -> DROP | REPRESENTED same-dest | Probe INV-014 (MEDIUM, interaction_effects): assumption "displacement is a flat 0.1-0.4 of
1353. VL-21-1353 | KNOWLEDGE -> KNOWLEDGE | REPRESENTED same-dest | Diff analysis of the second brainstorm (S10a, `diff-analysis.md` 114 lines; 2026-11-13T23:
1354. VL-21-1354 | KNOWLEDGE -> KNOWLEDGE | REPRESENTED same-dest | Diff C-001 (line 26): V1 "Probe Sheet" with 7 extractors E1-E7, at most 12 items per revie
1355. VL-21-1355 | KNOWLEDGE -> KNOWLEDGE | REPRESENTED same-dest | Diff C-002 (line 27): V1 "Lens Ledger" (an ember second lens in idle time); V2 "Recipe Led
1356. VL-21-1356 | KNOWLEDGE -> KNOWLEDGE | REPRESENTED same-dest | Diff S-001 (second brainstorm; read from diff-analysis.md at the tip, not enumerated in th
1357. VL-21-1357 | KNOWLEDGE -> KNOWLEDGE | REPRESENTED same-dest | Diff S-002: placement of shared material: V1 3.0 first (registry, adapter interface, H1-H4
1358. VL-21-1358 | KNOWLEDGE -> KNOWLEDGE | REPRESENTED same-dest | Diff S-003: redesign sub-structure: all three use (a)-(i) lettered blocks, identical for b
1359. VL-21-1359 | KNOWLEDGE -> KNOWLEDGE | REPRESENTED same-dest | Diff S-004: requirements numbering and form: V1 REQ-01..37 in 8 grouped tables with a Test
1360. VL-21-1360 | KNOWLEDGE -> KNOWLEDGE | REPRESENTED same-dest | Diff S-005: theory presentation: V1 per-theory evidence table + "explains / does not expla
1361. VL-21-1361 | KNOWLEDGE -> KNOWLEDGE | REPRESENTED same-dest | Diff C-003 (line 28), routing and replication: variant approaches to which reviewer gets w
1362. VL-21-1362 | KNOWLEDGE -> KNOWLEDGE | REPRESENTED same-dest | Diff C-004: where answers are written: V1 a table in the report body; V2 a `## Check ledge
1363. VL-21-1363 | KNOWLEDGE -> KNOWLEDGE | REPRESENTED same-dest | Diff C-005: verifying and promoting: V1 promote to MINOR; V2 flags only; V3 a blind verifi
1364. VL-21-1364 | KNOWLEDGE -> KNOWLEDGE | REPRESENTED same-dest | Diff C-006 recipe granularity; C-007 brief edits (V1 CB1-CB4 including a missing-requireme
1365. VL-21-1365 | KNOWLEDGE -> KNOWLEDGE | REPRESENTED same-dest | Diff C-008 pre-pass timeline: V1 6 s with `timeout 12`; V2 8 s with kill at 15 s; V3 6 s w
1366. VL-21-1366 | KNOWLEDGE -> KNOWLEDGE | REPRESENTED same-dest | Diff C-009 time enforcement: V1 kill at D = floor(1.35 b); V2 1.6 x deadline; V3 `timeout 
1367. VL-21-1367 | DROP -> DROP | REPRESENTED same-dest | Diff C-010 baseline b: V1 and V2 use 100 or 122; V3 mixes luna's 102 s with 122
1368. VL-21-1368 | DROP -> DROP | REPRESENTED same-dest | Diff C-011 (line 36): harness-fix gain: V1 +0.2 to +0.7 (estimate), V2 +0.03 to +0.34 cent
1369. VL-21-1369 | KNOWLEDGE -> KNOWLEDGE | REPRESENTED same-dest | Diff C-012 (line 37): total found of 14: V1 A 3.4-6.1, B 2.8-5.5; V2 R1 3.2-5.7, R2 2.7-5.
1370. VL-21-1370 | DROP -> DROP | REPRESENTED same-dest | Diff C-013 (line 38): per-issue reach examples: V1 A I4 .45-.80, I5 .40-.75, B5 .10-.30, B
1371. VL-21-1371 | KNOWLEDGE -> KNOWLEDGE | REPRESENTED same-dest | Diff C-014..C-017 (lines 39-42): anti-overfitting (V1 AO1-AO8 with a 4-word n-gram lint; V
1372. VL-21-1372 | KNOWLEDGE -> KNOWLEDGE | REPRESENTED same-dest | Diff C-018 wrong-blocker control; C-019 theory refinements (V2 T2a/T2b, T3a/T3b)
1373. VL-21-1373 | DROP -> DROP | REPRESENTED same-dest | Diff C-020 implementation effort: V1 A about 1,300-1,500 lines, B about 700-950; V2 R1 abo
1374. VL-21-1374 | DROP -> DROP | REPRESENTED same-dest | Diff C-021 model roles; C-022 output-token overhead (V1 A +26%, B +42%; V2 R1 +28-42%, R2 
1375. VL-21-1375 | KNOWLEDGE -> KNOWLEDGE | REPRESENTED same-dest | Diff C-023 failure-mode rows; C-024 broad-applicability mechanism: V1 a registry with targ
1376. VL-21-1376 | DROP -> DROP | REPRESENTED same-dest | Diff X-001 (line 57, second brainstorm): H1-H4 gain: the source table `MR` lines 342-350 g
1377. VL-21-1377 | DROP -> DROP | REPRESENTED same-dest | X-002 (line 58): V1 CB2 rewrites the Medium sentence and adds a missing-requirement rule t
1378. VL-21-1378 | DROP -> DROP | REPRESENTED same-dest | X-003 (line 59): critical-path cost per item: V1 about 1.5-2 s (8 items about +12 s; 0.65k
1379. VL-21-1379 | DROP -> DROP | REPRESENTED same-dest | X-004 (line 60): V3 baseline inconsistency: on b=122 A = 6+122+18+3 = 149 s (+22%, not +6%
1380. VL-21-1380 | EVAL -> EVAL | REPRESENTED same-dest | X-005 (line 61): kill at 1.35 x baseline: V1 kill (kill rate at most 10%); V2 rejects it (
1381. VL-21-1381 | DROP -> DROP | REPRESENTED same-dest | X-006 (line 62): V3 matrix rows sum 3.5-6.05 versus the stated 3.6-6.6
1382. VL-21-1382 | DROP -> DROP | REPRESENTED same-dest | X-007 (line 63): ember source skip 39% (81 of 209 valid runs) versus V3's 36% (14 of 39, o
1383. VL-21-1383 | DROP -> DROP | REPRESENTED same-dest | X-008 (line 64): V1 expected +15% but modelled worst +36% (A) and +42% at b=100 "kill-limi
1384. VL-21-1384 | EVAL -> EVAL | REPRESENTED same-dest | Shared assumption A-001 (second brainstorm): "reach" = the chance that a finding survives 
1385. VL-21-1385 | EVAL -> EVAL | REPRESENTED same-dest | A-002: per-issue probabilities are additive (UNSTATED)
1386. VL-21-1386 | DROP -> DROP | REPRESENTED same-dest | A-003: harness and redesign gains are additive
1387. VL-21-1387 | EVAL -> EVAL | REPRESENTED same-dest | A-004: a pre-implementation sandbox exists and a whole-tree search finishes in 6-8 s (UNST
1388. VL-21-1388 | EVAL -> EVAL | REPRESENTED same-dest | A-005: cheap reviewers complete the ledger honestly (STATED)
1389. VL-21-1389 | EVAL -> EVAL | REPRESENTED same-dest | A-006: MINOR or non-blocking still counts as "found" for the study score and the 1.83 base
1390. VL-21-1390 | EVAL -> EVAL | REPRESENTED same-dest | A-007: per-package baseline medians are stable
1391. VL-21-1391 | DROP -> DROP | REPRESENTED same-dest | A-008: the classes are representative (one repo)
1392. VL-21-1392 | EVAL -> EVAL | REPRESENTED same-dest | A-009: each extra item costs about 2 s or less (CONTRADICTED)
1393. VL-21-1393 | DROP -> DROP | REPRESENTED same-dest | Unique U-001 (V1): class registry plus adapter interface
1394. VL-21-1394 | DROP -> DROP | REPRESENTED same-dest | U-002 (V1): telemetry keys `class`/`probe` (HO2:346)
1395. VL-21-1395 | DROP -> DROP | REPRESENTED same-dest | U-003 (V1): quote verifier plus promotion
1396. VL-21-1396 | DROP -> DROP | REPRESENTED same-dest | U-004 (V1): arm A4 generic checklist plus gate G5
1397. VL-21-1397 | DROP -> DROP | REPRESENTED same-dest | U-005 (V1): documentation arm
1398. VL-21-1398 | DROP -> DROP | REPRESENTED same-dest | U-006 (V1): E1-E7 with blind spots
1399. VL-21-1399 | DROP -> DROP | REPRESENTED same-dest | U-007 (V1): a second ember session launched only if the first ended before 0.45 x D
1400. VL-21-1400 | DROP -> DROP | REPRESENTED same-dest | U-008 (V1): Stage 2 haiku and sonnet
1401. VL-21-1401 | DROP -> DROP | REPRESENTED same-dest | U-009 (V2): the issue-to-cause map
1402. VL-21-1402 | DROP -> DROP | REPRESENTED same-dest | U-010 (V2): the option to build the sheet while reviewers do their first reads
1403. VL-21-1403 | DROP -> DROP | REPRESENTED same-dest | U-011 (V2): shuffle plus two blind reviewers per item
1404. VL-21-1404 | DROP -> DROP | REPRESENTED same-dest | U-012 (V2): planted defects plus clean twins
1405. VL-21-1405 | DROP -> DROP | REPRESENTED same-dest | U-013 (V2): placebo arm P
1406. VL-21-1406 | DROP -> DROP | REPRESENTED same-dest | U-014 (V2): swap test plus 8-word shingles
1407. VL-21-1407 | DROP -> DROP | REPRESENTED same-dest | U-015 (V2): Z0-raw plus the act-rate readout
1408. VL-21-1408 | DROP -> DROP | REPRESENTED same-dest | U-016 (V2): `ran`-field audit plus the empty-sheet == baseline hash test
1409. VL-21-1409 | DROP -> DROP | REPRESENTED same-dest | U-017 (V2): resume re-ask only if `now + 30 s <= 1.35 x baseline`
1410. VL-21-1410 | DROP -> DROP | REPRESENTED same-dest | U-018 (V3): blind verifier
1411. VL-21-1411 | MODULE-tasklist -> MODULE-tasklist | REPRESENTED same-dest | U-019 (V3): union by anchor overlap (12 chars after flattening) plus a seeded shuffle
1412. VL-21-1412 | DROP -> DROP | REPRESENTED same-dest | U-020 (V3): real parser; "the current block-OK check only tests the fence opener, HO2:209"
1413. VL-21-1413 | DROP -> DROP | REPRESENTED same-dest | U-021 (V3): byte-identical determinism, an item cap and an arm manifest with a sandbox has
1414. VL-21-1414 | DROP -> DROP | REPRESENTED same-dest | U-022 (V3): stable-hit rate plus a package bootstrap
1415. VL-21-1415 | KNOWLEDGE -> KNOWLEDGE | REPRESENTED same-dest | Debate metadata (S10b, `debate-transcript.md` 567 lines): depth deep; rounds R1 parallel s
1416. VL-21-1416 | KNOWLEDGE -> KNOWLEDGE | REPRESENTED same-dest | V1 advocate, Round 1: positions A script-built Probe Sheet + B prompt-only Recipe/Lens Led
1417. VL-21-1417 | KNOWLEDGE -> KNOWLEDGE | REPRESENTED same-dest | V2 advocate, Round 1: Sweep Sheet + Recipe Ledger from opposite sides; concessions: 3(f) a
1418. VL-21-1418 | KNOWLEDGE -> KNOWLEDGE | REPRESENTED same-dest | V3 advocate, Round 1: finalise exactly two: a bounded Sweep Sheet and blind Recipe Lenses 
1419. VL-21-1419 | DROP -> DROP | REPRESENTED same-dest | Round 2 question Q1 (all three converge): the blind verifier stays OFF the critical path (
1420. VL-21-1420 | DROP -> DROP | REPRESENTED same-dest | Q2: data cards + flat extractors + a block-kind checklist, no adapter code before a second
1421. VL-21-1421 | DROP -> DROP | REPRESENTED same-dest | Q3: at most 12 items, each to exactly 2 blind reviewers, 1-2 per triggered class, the rest
1422. VL-21-1422 | DROP -> DROP | REPRESENTED same-dest | Q4: a MINOR non-blocking finding built from the reviewer's own row, tagged `src=ledger`, r
1423. VL-21-1423 | DROP -> DROP | REPRESENTED same-dest | Q5: one session per reviewer, at most 4 recipes (V1 wanted a second fresh ember session la
1424. VL-21-1424 | DROP -> DROP | REPRESENTED same-dest | Q6: one generic-checklist arm K plus Z0-raw
1425. VL-21-1425 | DROP -> DROP | REPRESENTED same-dest | Q7: labels B1..I7, I7 outside every "of 14"
1426. VL-21-1426 | DROP -> DROP | REPRESENTED same-dest | Q8: matrices as planning values, replaced by the measured act rate
1427. VL-21-1427 | DROP -> DROP | REPRESENTED same-dest | Q9: +35% on per-package medians, a 1.5x hang guard, a pre-pass kill at 15 s with an isolat
1428. VL-21-1428 | DROP -> DROP | REPRESENTED same-dest | Q10: D1-D6 plus G5 and G7 plus a package-level bootstrap, consistent = reached in at least
1429. VL-21-1429 | KNOWLEDGE -> KNOWLEDGE | REPRESENTED same-dest | Round 3 (S10b, lines 427-512): all 14 INV findings ACCEPT or QUALIFY by all three advocate
1430. VL-21-1430 | KNOWLEDGE -> KNOWLEDGE | REPRESENTED same-dest | Residual disagreements (S10b, line 567): Q5 (second ember session) and the INV-005 / INV-0
1431. VL-21-1431 | KNOWLEDGE -> KNOWLEDGE | REPRESENTED same-dest | Scoring matrix (S10b, 41 rows, lines 518-560): winners with confidence: S-001 V1 70%; S-00
1432. VL-21-1432 | KNOWLEDGE -> KNOWLEDGE | REPRESENTED same-dest | Scoring matrix, contradictions and assumptions: X-001 V2 98%; X-002 V2 98%; X-003 V2 90%; 
1433. VL-21-1433 | EVAL -> EVAL | REPRESENTED same-dest | Debate outcome in one line (S10b): no variant wins whole; base = V2 by tiebreaker (V1 0.94
1434. VL-21-1434 | KNOWLEDGE -> KNOWLEDGE | REPRESENTED same-dest | Round 2.5 fault-finder scope (S11, `round2.5-faultfinder.md` 152 lines): checks the consen
1435. VL-21-1435 | DROP -> DROP | REPRESENTED same-dest | Fault-finder matrix recomputation: sums V1-A 1.70-3.70, V2-A 1.63-3.55, V1-B 1.05-3.10, V2
1436. VL-21-1436 | EVAL -> EVAL | REPRESENTED same-dest | Fault-finder crude regex counts on the two defect-rich candidates (designSpec candidate.md
1437. VL-21-1437 | HARNESS -> HARNESS | REPRESENTED same-dest | Fault-finder launcher check: `EVAL/tools/run-reviewer.sh:50` and the collab harness `20261
1438. VL-21-1438 | EVAL -> EVAL | REPRESENTED same-dest | Fault-finder timing facts: `COMBO-REPORT.md:204` the 348 s baseline is a sum of per-packag
1439. VL-21-1439 | EVAL -> EVAL | REPRESENTED same-dest | Fault-finder score facts: `COMBO-REPORT.md:306-309` best single-run panel 4.00 of 14; A mi
1440. VL-21-1440 | CORE -> CORE | REPRESENTED same-dest | `findings.py` rules with line refs (S11): a second findings-v1 block sets ok=False (`FIND:
1441. VL-21-1441 | CORE -> CORE | REPRESENTED same-dest | A short anchor pattern (under 12 chars) flips ok=False for the WHOLE report
1442. VL-21-1442 | CORE -> CORE | REPRESENTED same-dest | A promoted ledger row for C2/C5/C8 quotes source, a root doc or a test file, whose natural
1443. VL-21-1443 | EVAL -> EVAL | REPRESENTED same-dest | Luna quotes anchors exactly in only 91.4% of cases (`D/variant-2-original.md:336`); ledger
1444. VL-21-1444 | EVAL -> EVAL | REPRESENTED same-dest | Fault-finder time facts: `MR:329` "the largest alias run was 171 s against 1.5 x 120 = 180
1445. VL-21-1445 | DROP -> DROP | REPRESENTED same-dest | Fault-finder: `D/variant-2-original.md:379-382` planted set is 6 documents with one defect
1446. VL-21-1446 | HARNESS -> HARNESS | REPRESENTED same-dest | Fault-finder: H3 is defined as "the parent of its first implementing commit" (`MR:317`); `
1447. VL-21-1447 | EVAL -> EVAL | REPRESENTED same-dest | Fault-finder: luna run-to-run Jaccard 0.12 on one package (`D/variant-2-original.md:18`); 
1448. VL-21-1448 | KNOWLEDGE -> KNOWLEDGE | REPRESENTED same-dest | Merge log metadata (S12a, `merge-log.md` 63 lines): base V2 by tiebreaker (35/41 diff poin
1449. VL-21-1449 | KNOWLEDGE -> KNOWLEDGE | REPRESENTED same-dest | Merge change table 1-16: frame/conventions; s1 theories; s2 classes; 3.0 shared scaffoldin
1450. VL-21-1450 | KNOWLEDGE -> KNOWLEDGE | REPRESENTED same-dest | Executor deviations (line 32): arm names from the brief (`RS` not used); ledger-row to fin
1451. VL-21-1451 | EVAL -> EVAL | REPRESENTED same-dest | Post-merge checks (S12a, line 40): 0 em/en dashes; 0 "Redesign A/B", GT labels or H1-H6 ho
1452. VL-21-1452 | KNOWLEDGE -> KNOWLEDGE | REPRESENTED same-dest | Review 1 (`merge-review.md`): FAIL: 7 blocking, 11 medium, 13 minor; blocking B-1 ember ca
1453. VL-21-1453 | KNOWLEDGE -> KNOWLEDGE | REPRESENTED same-dest | Fix cycle 1: B-1 ember 8 (fallback only 12); B-2 +23% to +40%; B-3 D5 spec clause removed 
1454. VL-21-1454 | KNOWLEDGE -> KNOWLEDGE | REPRESENTED same-dest | Review 2 (`merge-review-2.md`): PASS: 0 blocking, 3 medium, 5 minor; "every recomputed num
1455. VL-21-1455 | EVAL -> EVAL | REPRESENTED same-dest | Open follow-up M-1: the D2 threshold (+0.12 absolute) sits above the central planned gain 
1456. VL-21-1456 | EVAL -> EVAL | REPRESENTED same-dest | M-2: the Stage 2 entry rule and "passes" are undefined (an arm passing D1 only would enter
1457. VL-21-1457 | HARNESS -> HARNESS | REPRESENTED same-dest | M-3: the ember re-ask has no working mechanism because the launcher uses `--no-session-per
1458. VL-21-1458 | CORE -> CORE | REPRESENTED same-dest | M-4: promotion leaves the `category` and `id` scheme unspecified (while `_check_finding` r
1459. VL-21-1459 | MODULE-tasklist -> MODULE-tasklist | REPRESENTED same-dest | M-5: the ledger wording does not tell models to JSON-escape quotes
1460. VL-21-1460 | MODULE-tasklist -> MODULE-tasklist | REPRESENTED same-dest | M-6: R-C2 asks for more row-steps than its 6-row budget (up to 13 row-steps)
1461. VL-21-1461 | MODULE-tasklist -> MODULE-tasklist | REPRESENTED same-dest | M-7: the pre-pass search scope differs between S1, E3 and E4
1462. VL-21-1462 | EVAL -> EVAL | REPRESENTED same-dest | M-8: two word-level hints ("found" in set-word lists, "changelogs" in recipes) that a 4-wo
1463. VL-21-1463 | EVAL -> EVAL | REPRESENTED same-dest | M-9: REQ-40 names a prompting share that the reports do not give
1464. VL-21-1464 | KNOWLEDGE -> KNOWLEDGE | REPRESENTED same-dest | M-10: label clashes (S1 step versus item id; "A4"/"A7" appendix refs of the plan)
1465. VL-21-1465 | EVAL -> EVAL | REPRESENTED same-dest | M-11: "retried reviewer scored as zero" conflicts with the launcher's retry loop, which re
1466. VL-21-1466 | MODULE-tasklist -> MODULE-tasklist | REPRESENTED same-dest | M-12: the fallback cap raise (ember 12) is stated only in 3.1(c), not in S3, REQ-20, REQ-3
1467. VL-21-1467 | EVAL -> EVAL | REPRESENTED same-dest | M-13: the "consistent" threshold is uneven; M-14: spec generality for Redesign 2 rests on 
1468. VL-21-1468 | KNOWLEDGE -> KNOWLEDGE | REPRESENTED same-dest | Merge-review-2 verdict (S12b): PASS, 0 blocking, 3 medium, 5 minor; independent reviewer, 
1469. VL-21-1469 | DROP -> DROP | REPRESENTED same-dest | Merge-review-2 recomputed values (all matched): R1 b+29 129 (+29.0%), 151 (+23.77%); kill-
1470. VL-21-1470 | DROP -> DROP | REPRESENTED same-dest | New medium M-N1: the ember cap raise in the fallback is not carried into S3, REQ-20, REQ-3
1471. VL-21-1471 | DROP -> DROP | REPRESENTED same-dest | M-N2: the consistency threshold is uneven (Redesign 1 I7 0.34-0.62 "expected at high end",
1472. VL-21-1472 | DROP -> DROP | REPRESENTED same-dest | M-N3: spec generality for Redesign 2 rests on HO-5 alone (REQ-37 fixtures are for extracto
1473. VL-21-1473 | KNOWLEDGE -> KNOWLEDGE | REPRESENTED same-dest | Minor (merge-review-2): (1) unrounded R1 mid = 1.8238 gives 1.82 not 1.83; (2) "Strong cla
1474. VL-21-1474 | DROP -> DROP | REPRESENTED same-dest | Still open after review 2: M-3 (ember re-ask mechanism), M-4 (promotion category/id), M-10
1475. VL-21-1475 | DROP -> DROP | REPRESENTED same-dest | Lineage note (S12): invariant-probe INV-004 resolution reads "consistency expected only fo
1476. VL-21-1476 | KNOWLEDGE -> KNOWLEDGE | REPRESENTED same-dest | Refactor plan overview (S13, `refactor-plan.md` 291 lines): base V2; risk Medium; shape fi
1477. VL-21-1477 | KNOWLEDGE -> KNOWLEDGE | REPRESENTED same-dest | Refactor change 1: frame and conventions (label rules: HO-1..HO-6 not H1-H6; SS/RL; `Redes
1478. VL-21-1478 | KNOWLEDGE -> KNOWLEDGE | REPRESENTED same-dest | Refactor changes 2-3: theories; classes (+ the hold-out key)
1479. VL-21-1479 | KNOWLEDGE -> KNOWLEDGE | REPRESENTED same-dest | Refactor change 4: shared scaffolding 3.0.1-3.0.10 (the largest, Medium risk)
1480. VL-21-1480 | KNOWLEDGE -> KNOWLEDGE | REPRESENTED same-dest | Refactor changes 5-7: 3.1(a); 3.1(b)-(i) copying A2, A5a, A6, A7, A8 verbatim; 3.2
1481. VL-21-1481 | KNOWLEDGE -> KNOWLEDGE | REPRESENTED same-dest | Refactor changes 8-10: the section 3 head (what differs, what is shared, NOT redesigns); t
1482. VL-21-1482 | KNOWLEDGE -> KNOWLEDGE | REPRESENTED same-dest | Refactor changes 11-16: REQ-01..46 (A10 verbatim); the not-checked note; failure-mode unio
1483. VL-21-1483 | DROP -> DROP | REPRESENTED same-dest | Change NOT made 1: V1's CB2 rewrite of the Medium sentence plus a blocking missing-require
1484. VL-21-1484 | DROP -> DROP | REPRESENTED same-dest | Changes NOT made 2-3: V1's second fresh ember session; V3's shared 60-item list (cost per 
1485. VL-21-1485 | DROP -> DROP | REPRESENTED same-dest | Change NOT made 4: V3's "Blind Lenses then Verify" as a redesign (B = 168 s (+37.7%) at b=
1486. VL-21-1486 | DROP -> DROP | REPRESENTED same-dest | Changes NOT made 5-6: a kill at D = 1.35 x baseline (V1, V3) and a 1.6 x deadline (V2), re
1487. VL-21-1487 | DROP -> DROP | REPRESENTED same-dest | Changes NOT made 7-10: V1's target adapter classes; V2's fixed per-class caps Q2/U2/M2/R2/
1488. VL-21-1488 | DROP -> DROP | REPRESENTED same-dest | Changes NOT made 11-15: V2's resume re-ask for luna (INV-010); the mean of the V1+V2 matri
1489. VL-21-1489 | KNOWLEDGE -> KNOWLEDGE | REPRESENTED same-dest | Refactor risk summary: Change 4 Medium (parser checks; rollback = revert 3.0.4-3.0.5 to V2
1490. VL-21-1490 | KNOWLEDGE -> KNOWLEDGE | REPRESENTED same-dest | Refactor plan Appendix A1-A10: authoritative numbers (A1 baseline/cap; A2 R1 time; A3 R2 t
1491. VL-21-1491 | KNOWLEDGE -> KNOWLEDGE | REPRESENTED same-dest | Errata table (lines 278-291): A8 effort (R1 specific 650-800 to 790-1,090; totals 1,100-1,
1492. VL-21-1492 | KNOWLEDGE -> KNOWLEDGE | REPRESENTED same-dest | Merge review 1 setup (S14, `merge-review.md` 240 lines): independent reviewer, document re
1493. VL-21-1493 | CORE -> CORE | REPRESENTED same-dest | Code read by the merge reviewer: `findings.py` lines 1-158 and launcher lines 45-66; id re
1494. VL-21-1494 | DROP -> DROP | REPRESENTED same-dest | Promotion rule does not say which `category` or `id` the harness assigns while `_check_fin
1495. VL-21-1495 | DROP -> DROP | REPRESENTED same-dest | Merge review 1 arithmetic: all time, matrix, gain, run-count, token and effort sums recomp
1496. VL-21-1496 | EVAL -> EVAL | REPRESENTED same-dest | Leak check (S14): an automated 4-word-sequence comparison of every quoted draft instructio
1497. VL-21-1497 | KNOWLEDGE -> KNOWLEDGE | REPRESENTED same-dest | Other merge checks (S14): REQ ids exactly REQ-01..46; group sizes 5+12+7+4+4+4+2+8; no thi
1498. VL-21-1498 | DROP -> DROP | REPRESENTED same-dest | Review 1 blocking findings B-1..B-7 (all fixed in cycle 1): B-1 ember item count/caps (9 v
1499. VL-21-1499 | DROP -> DROP | REPRESENTED same-dest | Medium findings in detail (S14): M-1 D2 threshold 0.12 absolute above the central net gain
1500. VL-21-1500 | KNOWLEDGE -> KNOWLEDGE | REPRESENTED same-dest | Minor notes N-2..N-6 (S14): ember idle "60-90 s" vs "40-60 s"; ember 2 s/item in the R1 ta
1501. VL-21-1501 | KNOWLEDGE -> KNOWLEDGE | REPRESENTED same-dest | Minor notes N-7..N-13: D7 gain 0.04 vs K within 0.03 leaves a 0.03-0.04 gap; Stage 2 haiku
1502. VL-21-1502 | KNOWLEDGE -> KNOWLEDGE | REPRESENTED same-dest | Invariant map (S14): all 14 INV resolutions found; flagged defects: B-1 in INV-011/003 fal
1503. VL-21-1503 | EVAL -> EVAL | REPRESENTED same-dest | Status of the defects in the final merged text (S14): B-1..B-7 fixed (REQ-45 at line 1199,
1504. VL-21-1504 | EVAL -> EVAL | REPRESENTED same-dest | Provenance (S15, git): the whole brainstorm dir arrived in ONE commit `d561461fa` (2026-11
1505. VL-21-1505 | EVAL -> EVAL | REPRESENTED same-dest | Not implemented anywhere: `git grep -l -e 'ledger-v1' -e 'Sweep Sheet' -e 'Recipe Ledger'`
1506. VL-21-1506 | DROP -> DROP | REPRESENTED same-dest | Reused file investigation-patterns.md (174 lines, S15): 699 reviewer runs over 76 `source.
1507. VL-21-1507 | DROP -> DROP | REPRESENTED same-dest | Reused file investigation-designspec.md (145 lines): why cheap panels missed GT1, GT2, GT5
1508. VL-21-1508 | DROP -> DROP | REPRESENTED same-dest | Reused file investigation-alias-control.md (163 lines): why cheap panels miss alias GT1/GT
1509. VL-21-1509 | DROP -> DROP | REPRESENTED same-dest | Reused file research-light.md (242 lines): transport research from the FIRST brainstorm (O
1510. VL-21-1510 | EVAL -> EVAL | REPRESENTED same-dest | Contamination note (S15): investigation-designspec.md and investigation-alias-control.md q
1511. VL-21-1511 | DROP -> DROP | REPRESENTED same-dest | Script `launch-variants.sh` (S16; 42 lines): one headless `claude -p` session per proposal
1512. VL-21-1512 | DROP -> DROP | REPRESENTED same-dest | Script `launch-debate.sh` (S16; 18 lines): debate and merge in one session `/sc:adversaria
1513. VL-21-1513 | DROP -> DROP | REPRESENTED same-dest | Sessions (S16): `debate-reply.md` (26 lines; "Decide which of the 14 to turn into fixes be
1514. VL-21-1514 | KNOWLEDGE -> KNOWLEDGE | REPRESENTED same-dest | Brainstorm contract (S16, `return-contract.yaml` 19 lines): status success; `convergence_s
1515. VL-21-1515 | DROP -> DROP | REPRESENTED same-dest | Nested `return-contract.yaml` (5,165 B, lists 42 artifacts): the `sc:adversarial` worker c
1516. VL-21-1516 | HARNESS -> HARNESS | REPRESENTED same-dest | `scoring/quant.py`: deterministic quantitative layer with 5 metrics weighted 0.30/0.25/0.1
1517. VL-21-1517 | HARNESS -> HARNESS | REPRESENTED same-dest | `scoring/convergence.py`: per-point convergence from the advocates' position tables (stric
1518. VL-21-1518 | HARNESS -> HARNESS | REPRESENTED same-dest | `scoring/reconcile.py`, `final_table.py`, `qual-pass1.md`, `qual-pass2.md`, `resolved.json
1519. VL-21-1519 | HARNESS -> HARNESS | REPRESENTED same-dest | `scoring/lint_groundtruth.py` (1,454 B) + `lint-groundtruth-output.txt`: a REQ-07 lint: an
1520. VL-21-1520 | KNOWLEDGE -> KNOWLEDGE | REPRESENTED same-dest | `scoring/quant-run1-regex-bug.json`: the first quant run kept as evidence of two regex bug
1521. VL-21-1521 | KNOWLEDGE -> KNOWLEDGE | REPRESENTED same-dest | Process facts (S16): the three advocates + the fault-finder + the merge executor + two rev
1522. VL-21-1522 | CORE -> CORE | REPRESENTED same-dest | Verified at the tip (S17): the launcher keeps only the first `result` message (`run-review
1523. VL-21-1523 | CORE -> CORE | REPRESENTED same-dest | Verified (S17): `findings.py` `_check_finding` lines 90-121 as stated; `len(blocks) > 1` g
1524. VL-21-1524 | CORE -> CORE | REPRESENTED same-dest | Verified (S17, `document_review_loop_prompts.md` at HEAD): line 31 holds the "Grading chec
1525. VL-21-1525 | EVAL -> EVAL | REPRESENTED same-dest | Verified (S17, `HANDOFF-review-panel-unification-run2.md` lines 209, 346): H4 row "run-rev
1526. VL-21-1526 | DROP -> DROP | REPRESENTED same-dest | Verified (S17, `COMBO-REPORT.md` lines 401-417): B1..B5 = designSpec GT1..GT5, I1..I5 = de
1527. VL-21-1527 | EVAL -> EVAL | REPRESENTED same-dest | Verified partly (S17): `COMBO-REPORT.md:204` states "elapsed = per package the slowest rev
1528. VL-21-1528 | DROP -> DROP | REPRESENTED same-dest | Verified (S17, `MR` lines 320, 329, 342-350): line 320 grading rule held constant; line 32
1529. VL-21-1529 | DROP -> DROP | REPRESENTED same-dest | Verified (S17): no implementation of any design: `git grep -l -e 'ledger-v1' -e 'Sweep She
1530. VL-21-1530 | DROP -> DROP | REPRESENTED same-dest | Verified (S17): the brainstorm is absent from the run-1 commit, HEAD and origin/master (0 
1531. VL-21-1531 | CORE -> CORE | REPRESENTED same-dest | Package fact (S17b): the `src/superclaude/cli/review/` package has 10 entries at the tip (
1532. VL-21-1532 | CORE -> CORE | REPRESENTED same-dest | NAME CLASH (S17b): `ledger.py` ("Typed finding ledger (review-ledger/1): rows, statuses an
1533. VL-21-1533 | CORE -> CORE | REPRESENTED same-dest | `panel.py` (S17b): "Reviewer panel template, tier aliases and deterministic resolution ...
1534. VL-21-1534 | CORE -> CORE | REPRESENTED same-dest | `telemetry.py` (S17b): "Review telemetry (review-telemetry/1): append-only JSONL records, 
1535. VL-21-1535 | CORE -> CORE | REPRESENTED same-dest | `findings_v2.py` (HEAD only, S17b): fence info string `findings-v2`; `V1_FIELDS = (id, sev
1536. VL-21-1536 | CORE -> CORE | REPRESENTED same-dest | `verify_cmd.py` (HEAD): `superclaude review verify-citations`, a deterministic advisory pr
1537. VL-21-1537 | CORE -> CORE | REPRESENTED same-dest | `sc-reflect-protocol/refs/reviewer-spec.md:61-74` `## Coverage slice`: "the coverage-matri
1538. VL-21-1538 | CORE -> CORE | REPRESENTED same-dest | Rubric addendum (S17b, byte-identical at tip and HEAD): `document_review_loop_prompts.md` 
1539. VL-21-1539 | DROP -> DROP | REPRESENTED same-dest | Conflict K1: INV-004 wording "consistency expected only for C4, C5, C8" (invariant-probe l
1540. VL-21-1540 | CORE -> CORE | REPRESENTED same-dest | Conflict K2: the seed says the brief "has no missing-task category, defines no severity le
1541. VL-21-1541 | DROP -> DROP | REPRESENTED same-dest | Conflict K3: CB-2 "every confirmed defect ... listed as a line in the findings block ... M
1542. VL-21-1542 | DROP -> DROP | REPRESENTED same-dest | Conflict K4: telemetry: brainstorm 3.0.6/REQ-41 logs per-class yield, extractor candidates
1543. VL-21-1543 | DROP -> DROP | REPRESENTED same-dest | Conflict K5: `ledger-v1` versus the existing `review-ledger/1` in `ledger.py` and the `sc-
1544. VL-21-1544 | DROP -> DROP | REPRESENTED same-dest | Conflict K6: finding schema: findings-v1 + extra keys `class`, `probe`, `src` accepted (RE
1545. VL-21-1545 | MODULE-tasklist -> MODULE-tasklist | REPRESENTED same-dest | Conflict K7: reviewer tools: brainstorm recipes and search forms use Bash (`grep -rlF`, `p
1546. VL-21-1546 | DROP -> DROP | REPRESENTED same-dest | Conflict K8: lost-findings provenance: "80 reviewer-level cases, 49 blocking findings lost
1547. VL-21-1547 | DROP -> DROP | REPRESENTED same-dest | Conflict K9: ember skipped source.md 39% (81 of 209 valid runs) versus 36% (14 of 39 in on
1548. VL-21-1548 | DROP -> DROP | REPRESENTED same-dest | Conflict K10: the 348 s baseline is a sum of per-package slowest-reviewer MEANS (`COMBO-RE
1549. VL-21-1549 | EVAL -> EVAL | REPRESENTED same-dest | Conflict K11: the luna report end "about b + 22 s" (R3, line 689) versus "b + 26" for 11 r
1550. VL-21-1550 | DROP -> DROP | REPRESENTED same-dest | Conflict K12: the ember fallback cap is 8 in S3/REQ-20/REQ-32 but 12 in the fallback sente
1551. VL-21-1551 | DROP -> DROP | REPRESENTED same-dest | Conflict K13: `fallback=true` double meaning fixed by B-7; `check_skipped=true` not in the
1552. VL-21-1552 | DROP -> DROP | REPRESENTED same-dest | Conflict K14: D2 threshold "Z0 + 0.12 absolute" found fraction (0.12 x 14 = 1.68 issues of
1553. VL-21-1553 | DROP -> DROP | REPRESENTED same-dest | Conflict K15: "Retried reviewer scored as zero" (REQ-30) versus the launcher's retry loop 
1554. VL-21-1554 | DROP -> DROP | REPRESENTED same-dest | Conflict K16: the Redesign 1 pre-pass scope: S1/REQ-24 "tests, root documents and named pa
1555. VL-21-1555 | DROP -> DROP | REPRESENTED same-dest | Conflict K17: per-issue versus per-run totals: gain totals 1.9/3.3/4.8 and 1.6/3.0/4.5 exc
1556. VL-21-1556 | KNOWLEDGE -> KNOWLEDGE | REPRESENTED same-dest | Conflict K18: debate convergence label: `debate-reply.md` line 13 "98% after Round 2" and 
1557. VL-21-1557 | DROP -> DROP | REPRESENTED same-dest | Conflict K19: two copies of the final spec (merged-requirements.md and nested/adversarial-
1558. VL-21-1558 | DROP -> DROP | REPRESENTED same-dest | Conflict K20: the hard-coded worktree path `/home/coder/workspaces/worktrees/IronClaude/ev
1559. VL-21-1559 | DROP -> DROP | REPRESENTED same-dest | Slice value item F-01 (S19a): eight defect classes C1-C8 with target-neutral definitions a
1560. VL-21-1560 | DROP -> DROP | REPRESENTED same-dest | F-02: seven non-ten recurring classes X1-X7 (X8 not general); slice suggests CORE candidat
1561. VL-21-1561 | DROP -> DROP | REPRESENTED same-dest | F-03: ten missed issues mapped to main and secondary theories (T1/T2a/T2b/T3a/T3b)
1562. VL-21-1562 | DROP -> DROP | REPRESENTED same-dest | F-04: T1 plan-bounded search, direction not volume (0 of 176; 7 of 8 openers; 0 of 225); s
1563. VL-21-1563 | DROP -> DROP | REPRESENTED same-dest | F-05: T2 right place, wrong question; no structural unit of coverage (16 findings on the I
1564. VL-21-1564 | DROP -> DROP | REPRESENTED same-dest | F-06: T3 environment and suppression; slice suggests CORE harness requirements H1-H4
1565. VL-21-1565 | DROP -> DROP | REPRESENTED same-dest | F-07: rejected rival: reasoning budget; EVID / DROP as lever
1566. VL-21-1566 | DROP -> DROP | REPRESENTED same-dest | F-08: H1-H4 harness fixes and the gain +0.14 (0.03-0.34); slice suggests CORE (sandbox: ba
1567. VL-21-1567 | DROP -> DROP | REPRESENTED same-dest | F-09: model behaviour profiles; slice suggests CORE routing policy (route search versus re
1568. VL-21-1568 | DROP -> DROP | REPRESENTED same-dest | F-10: cheap-model coverage concentration (top-3 tasks 38-91% of anchors; luna Jaccard 0.12
1569. VL-21-1569 | DROP -> DROP | REPRESENTED same-dest | F-11: the sandbox leak (a reflect report in `.dev/reflect/` gave 2 of 9 I7 credits); slice
1570. VL-21-1570 | DROP -> DROP | REPRESENTED same-dest | F-12: the peer-hint idea per issue (kind of check, not answer); DROP for the process redes
1571. VL-21-1571 | DROP -> DROP | REPRESENTED same-dest | F-13: grok saw the stale claim in CHANGELOG and dropped it as "minor"; slice suggests the 
1572. VL-21-1572 | DROP -> DROP | REPRESENTED same-dest | F-14: outside evidence (narrow single-question passes; script narrows + model judges; reci
1573. VL-21-1573 | DROP -> DROP | REPRESENTED same-dest | F-15: smell detectors precision 59% recall 82% (Femmer), so extractor output needs a model
1574. VL-21-1574 | DROP -> DROP | REPRESENTED same-dest | F-16: fault-finder numbers: candidate lines per class 34, 34, 20 (C6/C1); blind pick 6-10%
1575. VL-21-1575 | DROP -> DROP | REPRESENTED same-dest | F-17: quote exactness 91.4% gives a two-quote pass of 0.835; CORE (flattened substring tes
1576. VL-21-1576 | DROP -> DROP | REPRESENTED same-dest | F-18: best single panel run 4.00 of 14; high ends 4.8/4.5 optimistic
1577. VL-21-1577 | DROP -> DROP | REPRESENTED same-dest | F-19: time arithmetic method (critical path = slowest reviewer; b + overhead; break-evens;
1578. VL-21-1578 | DROP -> DROP | REPRESENTED same-dest | F-20: displacement of easy finds 0.1-0.9 of 14; free-review floor CB-5; D6 non-regression;
1579. VL-21-1579 | DROP -> DROP | REPRESENTED same-dest | F-21: 14 invariants INV-001..014 and their resolutions; CORE requirements list
1580. VL-21-1580 | DROP -> DROP | REPRESENTED same-dest | F-22: 7 blocking + 11 medium + 13 minor review defects; 14 follow-ups never fixed; carry a
1581. VL-21-1581 | DROP -> DROP | REPRESENTED same-dest | Slice value item S-01 (S19b): class card schema (id/name/version, definition, recipe_text 
1582. VL-21-1582 | DROP -> DROP | REPRESENTED same-dest | S-02: block kinds (task, criterion, constraint, dictated_text, edit_target, gate) as a re-
1583. VL-21-1583 | DROP -> DROP | REPRESENTED same-dest | S-03: anti-overfitting rules AO-1..AO-8 plus REQ-07/08/33/34/35/36; CORE governance (lint,
1584. VL-21-1584 | DROP -> DROP | REPRESENTED same-dest | S-04: harness-level brief edits CB-1 to CB-5; CORE brief fragments; CB-2 conflicts with K3
1585. VL-21-1585 | DROP -> DROP | REPRESENTED same-dest | S-05: the `ledger-v1` carrier (heading + JSON-lines block, real parser, `ledger_missing` <
1586. VL-21-1586 | DROP -> DROP | REPRESENTED same-dest | S-06: checks and promotion (flattened quote tests, demote unsupported PROBLEM, promote a l
1587. VL-21-1587 | DROP -> DROP | REPRESENTED same-dest | S-07: telemetry keys class/probe/src, per-class yield, reach by stage; CORE; conflicts wit
1588. VL-21-1588 | DROP -> DROP | REPRESENTED same-dest | S-08: graceful degradation (`fallback=true`, `check_skipped=true`) and guard rows; CORE
1589. VL-21-1589 | MODULE-tasklist -> CORE | REPRESENTED moved(documented) | S-09: Redesign 1 Sweep Sheet (serial deterministic pre-pass, extractors E1-E7, quota 1-2 p
1590. VL-21-1590 | DROP -> DROP | REPRESENTED same-dest | S-10: the offline selection-recall gate G0 plus a rank function that must beat random on d
1591. VL-21-1591 | DROP -> DROP | REPRESENTED same-dest | S-11: Redesign 2 Recipe Ledger (lens per reviewer of 2-4 recipes, row budgets, no luna re-
1592. VL-21-1592 | DROP -> DROP | REPRESENTED same-dest | S-12: the blind claim-only verifier (off the critical path, cannot add claims, unconfirmed
1593. VL-21-1593 | CORE -> CORE | REPRESENTED same-dest | S-13: model routing by habit (search lens to ember/haiku/sonnet, read lens to luna) with p
1594. VL-21-1594 | DROP -> DROP | REPRESENTED same-dest | S-14: arms and gates (Z0-raw, Z0, K, SS, RL, Zh/SSh/RLh, Zs/SSs/RLs; G0, D1-D7; consistenc
1595. VL-21-1595 | DROP -> DROP | REPRESENTED same-dest | S-15: hold-out strategy HO-1..HO-6 + planted set + clean twins + documentation arm; STUDY 
1596. VL-21-1596 | DROP -> DROP | REPRESENTED same-dest | S-16: the two-pass judged rubric with position-bias mitigation and re-evaluation (`scoring
1597. VL-21-1597 | DROP -> DROP | REPRESENTED same-dest | S-17: a same-day Z0 arm in block-randomised order, one panel clock from before the pre-pas
1598. VL-21-1598 | DROP -> DROP | REPRESENTED same-dest | Decision D-01 (S19c): DECIDED (debate Q1-Q10, 97.6% strict): blind verifier off the critic
1599. VL-21-1599 | DROP -> DROP | REPRESENTED same-dest | D-02: DECIDED: grading rule and judge held constant in every arm; the CB2 rubric edit only
1600. VL-21-1600 | DROP -> DROP | REPRESENTED same-dest | D-03: DECIDED: the serial pre-pass is the only mode (a parallel build is a later arm)
1601. VL-21-1601 | DROP -> DROP | REPRESENTED same-dest | D-04: DECIDED: no messaging between reviewers (herding); an optional claims-only exchange 
1602. VL-21-1602 | DROP -> DROP | REPRESENTED same-dest | D-05: DECIDED: no luna re-ask (the condition can never hold for b under 148 s)
1603. VL-21-1603 | DROP -> DROP | REPRESENTED same-dest | D-06: OPEN decision: which redesign wins ("Run both ... if neither passes keep Z0"; tie ru
1604. VL-21-1604 | DROP -> DROP | REPRESENTED same-dest | D-07: OPEN: 14 follow-ups M-1..M-14 unfixed (merge-log.md:52-55); backlog
1605. VL-21-1605 | DROP -> DROP | REPRESENTED same-dest | D-08: OPEN: D2 threshold, Stage 2 entry rule and the meaning of "passes" (M-1, M-2)
1606. VL-21-1606 | DROP -> DROP | REPRESENTED same-dest | D-09: OPEN: the ember re-ask mechanism (the launcher uses `--no-session-persistence`, veri
1607. VL-21-1607 | DROP -> DROP | REPRESENTED same-dest | D-10: OPEN: the promotion `category` and `id` scheme (M-4); v1 requires a valid category f
1608. VL-21-1608 | DROP -> DROP | REPRESENTED same-dest | D-11: OPEN: JSON-escape of quotes in the ledger (M-5); the compliance spike must measure t
1609. VL-21-1609 | HARNESS -> HARNESS | REPRESENTED same-dest | D-12: OPEN: single-word hints ("found", "changelogs") bypass the 4-word lint (M-8); slice 
1610. VL-21-1610 | DROP -> DROP | REPRESENTED same-dest | D-13: unmeasured numbers: 48 tokens/s; 2 s per item or row; 8 s pre-pass; 75-90 tokens per
1611. VL-21-1611 | DROP -> DROP | REPRESENTED same-dest | D-14: wrong-blocker risk: earlier 2x ember panels added 2.75-3.25 wrong blockers; luna abo
1612. VL-21-1612 | DROP -> DROP | REPRESENTED same-dest | Slice item A-01 (S19d): `lint_groundtruth.py` (4-word shingle lint versus ground-truth.jso
1613. VL-21-1613 | DROP -> DROP | REPRESENTED same-dest | A-02: `quant.py`, `convergence.py`, `reconcile.py`, `final_table.py` (deterministic scorin
1614. VL-21-1614 | DROP -> DROP | REPRESENTED same-dest | A-03: `launch-variants.sh`, `launch-debate.sh`; DROP (study-local, hard-coded path); keep 
1615. VL-21-1615 | DROP -> DROP | REPRESENTED same-dest | A-04: `run-reviewer.sh` (E2 study launcher, referenced; lines 48-64 verified); STUDY harne
1616. VL-21-1616 | DROP -> DROP | REPRESENTED same-dest | A-05: the `investigation-patterns` scripts `collect.py analyze.py gtproxy.py theory.py rev
1617. VL-21-1617 | EVAL -> EVAL | REPRESENTED same-dest | A-06: the REQ-01..REQ-46 test list (each REQ with a Test column); CORE test backlog (46 te
1618. VL-21-1618 | DROP -> DROP | REPRESENTED same-dest | A-07: ground-truth, ledger and hold-out files referenced but not in this slice: `X346/p17/
1619. VL-21-1619 | DROP -> DROP | REPRESENTED same-dest | A-08: merged-requirements.md + merged-spec.md (duplicate); KEEP merged-requirements.md, DR
1620. VL-21-1620 | DROP -> DROP | REPRESENTED same-dest | A-09: variant originals (V1 61,742 B, V2 52,788 B, V3 39,846 B; two copies each); EVID, DR
1621. VL-21-1621 | KNOWLEDGE -> KNOWLEDGE | REPRESENTED same-dest | A-10: `debate-transcript.md` + debate round files + diff-analysis.md + base-selection.md; 
1622. VL-21-1622 | DROP -> DROP | REPRESENTED same-dest | Layer L0 evidence environment (S20): H1 source named in the brief; H2 truncate before merg
1623. VL-21-1623 | CORE -> CORE | REPRESENTED same-dest | Layer L1 class registry (data) (S20): cards with definition, recipe_text, question_templat
1624. VL-21-1624 | DROP -> DROP | REPRESENTED same-dest | Layer L2 target adapters (S20): NOT code in v1: a block-kinds checklist plus a re-derive l
1625. VL-21-1625 | DROP -> DROP | REPRESENTED same-dest | Layer L3 item/lens generation (S20): Redesign 1 deterministic pre-pass (E1-E7, quota, 24 s
1626. VL-21-1626 | DROP -> DROP | REPRESENTED same-dest | Layer L4 carrier (S20): `ledger-v1` in the FINAL message above the single findings block; 
1627. VL-21-1627 | DROP -> DROP | REPRESENTED same-dest | Layer L5 post-run checks (S20): parse, flattened substring tests (same `flat`/`locate` as 
1628. VL-21-1628 | DROP -> DROP | REPRESENTED same-dest | Layer L6 merge (S20): unchanged, findings-v1 kept; `superclaude review merge` (`merge_cmd.
1629. VL-21-1629 | DROP -> DROP | REPRESENTED same-dest | Layer L7 telemetry (S20): per-class yield, reach by stage, kills, retries, fallbacks, `led
1630. VL-21-1630 | DROP -> DROP | REPRESENTED same-dest | Layer L8 governance (S20): AO-1..AO-8, lint, git-tag freeze before hold-out GT, leave-one-
1631. VL-21-1631 | DROP -> DROP | REPRESENTED same-dest | Layer L9 evaluation protocol (S20): arms, hold-out sets, gates G0 and D1-D7, requirements 
1632. VL-21-1632 | MODULE-tasklist -> MODULE-tasklist | REPRESENTED same-dest | Design decision 1 (S20): one card, two renderings (a question for pre-pass items; a recipe
1633. VL-21-1633 | DROP -> DROP | REPRESENTED same-dest | Design decision 2: the script never writes a claim; the model keeps every OK/PROBLEM/UNSUR
1634. VL-21-1634 | DROP -> DROP | REPRESENTED same-dest | Design decision 3: the fallback is always the isolated panel brief (`fallback=true`, decid
1635. VL-21-1635 | DROP -> DROP | REPRESENTED same-dest | Design decision 4: reviewers are mutually blind; the fast reviewer's idle time pays for ev
1636. VL-21-1636 | CORE -> CORE | REPRESENTED same-dest | Design decision 5: the ledger lives in the final message only because the launcher keeps o
1637. VL-21-1637 | DROP -> DROP | REPRESENTED same-dest | Design decision 6: findings-v1 unchanged; new information rides in a separate block plus o
1638. VL-21-1638 | DROP -> DROP | REPRESENTED same-dest | Use case sc:workflow tasklist review (S21): the whole design; classes C1-C8 derived from 3
1639. VL-21-1639 | MODULE-spec -> MODULE-spec | REPRESENTED same-dest | Use case spec review (S21): applicability notes (E1 shall/must + scope; E2 examples and me
1640. VL-21-1640 | MODULE-reflect -> MODULE-reflect | REPRESENTED same-dest | Use case sc:reflect UC-1/UC-2 (S21): classes map onto reflect work (C2 rule not carried is
1641. VL-21-1641 | MODULE-pr-review -> MODULE-pr-review | REPRESENTED same-dest | Use case PR code review, later (S21): reverse-dependency sweep (E3/R-C8), stale second loc
1642. VL-21-1642 | MODULE-rfqa -> MODULE-rfqa | REPRESENTED same-dest | Use case rf-qa replacement (S21): classes about "claim vs corpus" (C5, C6), "source rule n
1643. VL-21-1643 | MODULE-spec -> MODULE-spec | REPRESENTED same-dest | Use case documentation review (S21): the documentation arm (about 8 delivered docs reviewe
1644. VL-21-1644 | DROP -> DROP | REPRESENTED same-dest | Use case other model sets (S21): adaptation arms haiku+2xluna and sonnet+2xluna; per-model
1645. VL-21-1645 | DROP -> DROP | REPRESENTED same-dest | Use case adding a new class (S21): one card (+ optional extractor), no dispatcher change (
1646. VL-21-1646 | DROP -> DROP | REPRESENTED same-dest | Use case future reviewer-to-reviewer exchange (S21): a documented seam (telemetry key `cla
1647. VL-21-1647 | DROP -> DROP | REPRESENTED same-dest | Use case verifier stage, claim-only blind (S21): an optional off-path audit, not an arm; i
1648. VL-21-1648 | DROP -> DROP | REPRESENTED same-dest | Overlap input, finding schema (S22): E2 findings-v1 + extra keys `class`, `probe`, `src`; 
1649. VL-21-1649 | DROP -> DROP | REPRESENTED same-dest | Overlap input, per-reviewer coverage partition: E2 24 slots over at most 12 items or the l
1650. VL-21-1650 | DROP -> DROP | REPRESENTED same-dest | Overlap input, quote/citation check: E2 flattened substring tests + demotion; E1 `verify_c
1651. VL-21-1651 | DROP -> DROP | REPRESENTED same-dest | Overlap input, finding status ledger: E2 `ledger-v1` (enumeration rows, NOT a status ledge
1652. VL-21-1652 | DROP -> DROP | REPRESENTED same-dest | Overlap input, heterogeneous reviewers: E2 cheap model slots with route search/read and on
1653. VL-21-1653 | CORE -> CORE | REPRESENTED same-dest | Overlap input, deterministic pre-pass: E2 E1-E7 extractors (not built); E1 grounding hunks
1654. VL-21-1654 | DROP -> DROP | REPRESENTED same-dest | Overlap input, class-keyed checks: E2 C1-C8 cards/recipes; E1 persona lenses; E3 variant s
1655. VL-21-1655 | DROP -> DROP | REPRESENTED same-dest | Overlap input, evaluation harness: E2 arms Z0..RL, gates D1-D7, hold-out registry, planted
1656. VL-21-1656 | DROP -> DROP | REPRESENTED same-dest | Overlap input, sandbox hygiene: E2 H3/H4; E1 `--isolate-reviewers` snapshot; E3 n/a
1657. VL-21-1657 | DROP -> DROP | REPRESENTED same-dest | Overlap input, telemetry: E2 class/probe/src + reach by stage; E1 `telemetry.py` forbids d
1658. VL-21-1658 | DROP -> DROP | REPRESENTED same-dest | Slice summary item 1 (S-summary): a design-only requirements spec (`merged-requirements.md
1659. VL-21-1659 | DROP -> DROP | REPRESENTED same-dest | Summary item 2: exactly two redesigns: Sweep Sheet (deterministic pre-pass, at most 12 typ
1660. VL-21-1660 | DROP -> DROP | REPRESENTED same-dest | Summary item 3: the debate did not choose between the redesigns; run both, adopt by pre-re
1661. VL-21-1661 | DROP -> DROP | REPRESENTED same-dest | Summary item 4: generality: eight classes with recurrence outside the three packages (3, 6
1662. VL-21-1662 | DROP -> DROP | REPRESENTED same-dest | Summary item 5: open: 14 follow-ups (M-1..M-14) plus 13 minor notes never fixed; unmeasure
1663. VL-21-1663 | DROP -> DROP | REPRESENTED same-dest | Summary item 6: verified against code: launcher lines 48/50/57/61-64, `findings.py:90-121,
1664. VL-21-1664 | DROP -> DROP | REPRESENTED same-dest | Summary item 7: biggest cross-effort exposures: name clash `ledger-v1` vs `review-ledger/1
1665. VL-21-1665 | KNOWLEDGE -> KNOWLEDGE | REPRESENTED same-dest | Slice count line (S6): 58 blobs (1,055,384 B) listed; 22 findings/lessons (F-01..F-22), 17
1666. VL-21-1666 | KNOWLEDGE -> KNOWLEDGE | REPRESENTED same-dest | Coverage gap (S6): the three variant files and the duplicate `variant-N-original.md` were 
1667. VL-21-1667 | KNOWLEDGE -> KNOWLEDGE | REPRESENTED same-dest | Coverage gap: individual `debate/round{1,2,3}-V{1,2,3}.md` not read (content taken from `d
1668. VL-21-1668 | KNOWLEDGE -> KNOWLEDGE | REPRESENTED same-dest | Coverage gap: `enrichment/reused/research-light.md` read only at head and recommendation; 
1669. VL-21-1669 | DROP -> DROP | REPRESENTED same-dest | Unverified carried (S6): 48 tokens/s, 2 s per ledger row, 8 s pre-pass, 75-90 tokens per r
1670. VL-21-1670 | DROP -> DROP | REPRESENTED same-dest | Unverified carried: the IG phrase-search counts (6 / 9 / 12 other documents etc.); IG itse
1671. VL-21-1671 | DROP -> DROP | REPRESENTED same-dest | Unverified carried: all EXT effect sizes except those marked OPENED in EXT; many are snipp
1672. VL-21-1672 | DROP -> DROP | REPRESENTED same-dest | Unverified carried: "80 reviewer-level cases / 49 blocking findings lost (HO2 R20)" versus
1673. VL-21-1673 | DROP -> DROP | REPRESENTED same-dest | Unverified carried: `code-merge.md:38` ("unknown keys accepted silently") not opened; `fin
1674. VL-21-1674 | HARNESS -> HARNESS | REPRESENTED same-dest | Unverified carried: whether the study's `run-reviewer.sh` or the 20261111-a1 harness exist
1675. VL-21-1675 | EVAL -> EVAL | REPRESENTED same-dest | Unverified carried: `d561461fa` introduced "five collaboration harnesses" (commit subject)
1676. VL-21-1676 | DROP -> DROP | REPRESENTED same-dest | Question Q1 (S6 questions): which finding schema is the central panel's contract, findings
1677. VL-21-1677 | DROP -> DROP | REPRESENTED same-dest | Question Q2: rename `ledger-v1` (per-reviewer rows) to avoid `review-ledger/1`? Who owns t
1678. VL-21-1678 | DROP -> DROP | REPRESENTED same-dest | Question Q3: does CB-2 ("list every defect incl. non-blocking in the findings block") chan
1679. VL-21-1679 | DROP -> DROP | REPRESENTED same-dest | Question Q4: can study telemetry carry anchors and quotes given `telemetry.py` forbids doc
1680. VL-21-1680 | DROP -> DROP | REPRESENTED same-dest | Question Q5: reflect-reviewer has no Bash: should recipes use Grep/Glob/codegraph tools, o
1681. VL-21-1681 | CORE -> CORE | REPRESENTED same-dest | Question Q6: the brainstorm assumes ember/luna/haiku/sonnet gateway ids and a launcher kee
1682. VL-21-1682 | EVAL -> EVAL | REPRESENTED same-dest | Question Q7: is the 326-run validation (about 978 reviewer runs) going to run? The owner w
1683. VL-21-1683 | EVAL -> EVAL | REPRESENTED same-dest | Question Q8: HO-5 (the worker-contract spec ledger from the #346 series) is the only spec 
1684. VL-21-1684 | MODULE-tasklist -> MODULE-tasklist | REPRESENTED same-dest | Question Q9: should X1-X7 be added to the first registry release? IG says several are as f
1685. VL-21-1685 | CORE -> CORE | REPRESENTED same-dest | Question Q10: is the +35% elapsed budget a product requirement for a central panel or a st

COUNT 21-value-ledger-brainstorms.md: 1685

## File 8: research/20-value-ledger-e2-study.md (one entry per ledger row; format: n. id | ledger dest -> inventory dest | status | statement head)

1. VL-20-001 | EVAL -> EVAL | REPRESENTED same-dest | E2 study tree A1 holds 9,312 committed files at tip 6c09843 (reviewer reports, meta, cost,
2. VL-20-002 | KNOWLEDGE -> KNOWLEDGE | REPRESENTED same-dest | Sibling handoff docs (HANDOFF-review-panel-unification*.md, HANDOFF-run1-vs-run2.md, hando
3. VL-20-003 | EVAL -> EVAL | REPRESENTED same-dest | Three study packages (design, designSpec, makeTheAliasOnly) each carry candidate.md, groun
4. VL-20-004 | EVAL -> EVAL | REPRESENTED same-dest | arms/ A, B, C hold per package ledger.json, merge-stdout.txt, merged-1.md, resolution.json
5. VL-20-005 | EVAL -> EVAL | REPRESENTED same-dest | combos/ holds 95 combo row directories (12 files each, c2-haiku-grok has 10)
6. VL-20-006 | HARNESS -> HARNESS | REPRESENTED same-dest | combos/SPEC.md (152 lines) is the operations log of the combo runs
7. VL-20-007 | EVAL -> EVAL | REPRESENTED same-dest | quarantine-pre-src-luna/ holds 417 files while COMBO-REPORT:107 says 428 reviewer files an
8. VL-20-008 | HARNESS -> HARNESS | REPRESENTED same-dest | tools/run-reviewer.sh (8,089 B) with two variants .bad-launch and .unpassable-ac preserved
9. VL-20-009 | HARNESS -> HARNESS | REPRESENTED same-dest | probe/probe.json is the Stage 0 model identity probe output
10. VL-20-010 | EVAL -> EVAL | REPRESENTED same-dest | Kind counts over A1: score.json 318 (2 invalid), meta.json 1,263, cost.json 1,263, *.err 1
11. VL-20-011 | EVAL -> EVAL | REPRESENTED same-dest | Per-package reviews/ layout mixes bulk combos/ with pilot reviewer files (t1b-1, t2-1, t2b
12. VL-20-012 | CORE -> CORE | REPRESENTED same-dest | About 1.48 GB of raw claude -p JSON transcripts and every judge.json (2,916 files) were no
13. VL-20-013 | EVAL -> EVAL | REPRESENTED same-dest | Because raw transcripts are missing, judge and reviewer sessions cannot be re-audited from
14. VL-20-014 | KNOWLEDGE -> KNOWLEDGE | REPRESENTED same-dest | RAW-TRANSCRIPTS-NOT-COMMITTED.md:4 says start with COMBO-REPORT.md section FINAL RESULTS A
15. VL-20-015 | DROP -> DROP | REPRESENTED same-dest | manifest.md says the branch is local and never pushed, but the branch exists on origin at 
16. VL-20-016 | EVAL -> EVAL | REPRESENTED same-dest | Study base: HEAD sha equals origin/master sha ec259f1b718ccdb9f08bba0237bfa47b2b7601a2 (Pr
17. VL-20-017 | MODULE-tasklist -> CORE | REPRESENTED moved(documented) | superclaude review --help works, T2bModel01=gpt-6.1-terra, and @live7 resolves 7 reviewers
18. VL-20-018 | CORE -> CORE | REPRESENTED same-dest | Reviewer sandbox is a git archive of HEAD minus .dev/tasks/done, .dev/eval-workspaces, .de
19. VL-20-019 | CORE -> CORE | REPRESENTED same-dest | Dispatch uses Bash claude -p --model with the raw gateway model id and records the observe
20. VL-20-020 | EVAL -> EVAL | REPRESENTED same-dest | Ground-truth sha256 pinned per package (designSpec 3e56551d..., makeTheAliasOnly 79e32057.
21. VL-20-021 | EVAL -> EVAL | REPRESENTED same-dest | The whole eval used raw model ids on harness run-reviewer.sh; product code did not run the
22. VL-20-022 | EVAL -> EVAL | REPRESENTED same-dest | Pilot packages: designSpec 10 GT defects (5 blocking in implement), makeTheAliasOnly 4 GT 
23. VL-20-023 | EVAL -> EVAL | REPRESENTED same-dest | Pilot arms: A = Tier 1b reviewer alone (claude-sonnet-5-5), B = @default panel minus Qwen3
24. VL-20-024 | MODULE-tasklist -> CORE | REPRESENTED moved(documented) | Qwen3.8-max was disqualified after all 3 slots timed out (attempts=2, 0 output tokens, 300
25. VL-20-025 | MODULE-tasklist -> DROP | FLAG DEDUP-CHAIN-BROKEN | dedup->BROKEN-CHAIN:VL-20-025 | Category label defect: reports used unpassable-ac while merges needed unpassable-check; 9 
26. VL-20-026 | EVAL -> EVAL | REPRESENTED same-dest | Scoring: 9 blind Opus subagents (one per package x label), random X/Y/Z labels in arm-key.
27. VL-20-027 | EVAL -> EVAL | REPRESENTED same-dest | score.json measures GT coverage, blocking coverage and wrong blockers (blocking ledger row
28. VL-20-028 | EVAL -> EVAL | REPRESENTED same-dest | Pilot per-arm results table: verdict, GT any, GT blocking, ledger rows, wrong blockers, wa
29. VL-20-029 | EVAL -> EVAL | REPRESENTED same-dest | Pilot totals: A 2/16 caught, 0/8 blocking, 702 s, 93,098 tokens, 2.15 catches/100k; B 3/16
30. VL-20-030 | EVAL -> EVAL | REPRESENTED same-dest | Pilot judging cost 9 Opus subagents, 1,034,575 output tokens, about 139 s summed wall
31. VL-20-031 | EVAL -> EVAL | REPRESENTED same-dest | Fixed decision rule: recommend a panel only if on defect-rich packages it catches at least
32. VL-20-032 | EVAL -> EVAL | REPRESENTED same-dest | Rule outcome: A=1, B=1, C=2 defect-rich catches; only C passes, exactly and marginally
33. VL-20-033 | EVAL -> EVAL | REPRESENTED same-dest | Paired sign tests: B vs A p=0.5, C vs A p=0.25
34. VL-20-034 | EVAL -> EVAL | REPRESENTED same-dest | B costs 4.2x arm A's tokens, C 6.5x
35. VL-20-035 | EVAL -> EVAL | REPRESENTED same-dest | All three arms had 0/8 blocking recall; single reviewer A PASSED both defect-rich packages
36. VL-20-036 | EVAL -> EVAL | REPRESENTED same-dest | Bigger panels helped only on non-blocking defects (4/4 vs 2/4 on control; GT7 on designSpe
37. VL-20-037 | EVAL -> EVAL | REPRESENTED same-dest | Stated pilot limits: n=3 packages, one Opus judge per (package, label), judge variance unm
38. VL-20-038 | EVAL -> EVAL | REPRESENTED same-dest | Ground-truth structural bias: a true novel defect scores as a wrong blocker if the reviewe
39. VL-20-039 | CORE -> CORE | REPRESENTED same-dest | c1 designSpec haiku block missed the Findings block heading so 15 findings were ignored (r
40. VL-20-040 | EVAL -> EVAL | REPRESENTED same-dest | Six remaining packages were staged for the same pipeline only after approval; 15 owner-ord
41. VL-20-041 | EVAL -> EVAL | REPRESENTED same-dest | Slice recomputed all 9 pilot (arm, package) cells from committed score.json plus arm-key.j
42. VL-20-042 | CORE -> CORE | REPRESENTED same-dest | Control package scores gt_covered_blocking GT1/GT2 although neither GT is blocking_in_impl
43. VL-20-043 | EVAL -> EVAL | REPRESENTED same-dest | Arm A/B/C numbers were produced without source.md in the reviewer sandbox and were never r
44. VL-20-044 | HARNESS -> HARNESS | REPRESENTED same-dest | Batch 1-2 setup: 15 owner-ordered Tier 3/4 combos via run-reviewer.sh, raw ids, claude -p,
45. VL-20-045 | EVAL -> EVAL | REPRESENTED same-dest | Defect-rich set = designSpec (10 GT, 5 blocking) + alias (4 GT, 3 blocking) = 14 GT any an
46. VL-20-046 | EVAL -> EVAL | REPRESENTED same-dest | Batch 1-2 scoring: 45 merged reports anonymised (R1..Rn, paths redacted), one Opus judge p
47. VL-20-047 | CORE -> CORE | REPRESENTED same-dest | r2 haiku alias block with a claim over 300 characters was dropped by merge (reviewer-side 
48. VL-20-048 | EVAL -> EVAL | REPRESENTED same-dest | Master table anchors: best any-catch 4/14 (n5-muse-glm-luna), best blocking 2/8, worst r4-
49. VL-20-049 | EVAL -> EVAL | REPRESENTED same-dest | No combo beats arm A's efficiency (combos 0-1.06 catches/100k vs A 2.15, B 0.76, C 0.66)
50. VL-20-050 | EVAL -> EVAL | REPRESENTED same-dest | Blocking recall bad everywhere in batch 1-2: best 2/8, 8 of 14 combos caught 0 or 1, 5 com
51. VL-20-051 | EVAL -> EVAL | REPRESENTED same-dest | luna is fast and thin (30-295 s, 1.4k-14k tokens)
52. VL-20-052 | EVAL -> EVAL | REPRESENTED same-dest | haiku appears in 11 combos; grok is slow (600-980 s, 41-63k tokens); muse-wonder-1.0 149-1
53. VL-20-053 | DROP -> DROP | REPRESENTED same-dest | Wrong blockers 2-3 per combo on defect-rich packages because ground truth penalises novel-
54. VL-20-054 | DROP -> DROP | REPRESENTED same-dest | Verdict "no configuration reached even 30% blocking recall"
55. VL-20-055 | MODULE-tasklist -> CORE | REPRESENTED moved(documented) | glm-5.3 added cost without catches in every combo it appeared in (408-615k tokens); owner 
56. VL-20-056 | HARNESS -> HARNESS | REPRESENTED same-dest | The catfix (.catfix.md) restores the category label but not findings that merge already sk
57. VL-20-057 | CORE -> CORE | REPRESENTED same-dest | Batch 3 first attempt (12 concurrent workers) was torn down for gateway model-identity ble
58. VL-20-058 | EVAL -> EVAL | REPRESENTED same-dest | gpt-6.1-terra returned thin incomplete reports (407-598 tokens, 0 findings, citing a missi
59. VL-20-059 | EVAL -> EVAL | REPRESENTED same-dest | Batch 3 per-row results (for example r2-terra 3/14 + 2/8 + 3 wrong blockers at 487,442 tok
60. VL-20-060 | EVAL -> EVAL | REPRESENTED same-dest | Batch 3 summary: sonnet was the only added reviewer that contributed findings; terra and s
61. VL-20-061 | KNOWLEDGE -> KNOWLEDGE | REPRESENTED same-dest | Gateway misrouting hit muse (22:40 UTC Nov 11) and glm (08:25 UTC Nov 12) under load and r
62. VL-20-062 | DROP -> DROP | REPRESENTED same-dest | Batch 3 recommendation n5-sonnet 4-reviewer panel
63. VL-20-063 | HARNESS -> HARNESS | REPRESENTED same-dest | Parser bug: blocking counts used grep for "blocking":true without a space while several mo
64. VL-20-064 | EVAL -> EVAL | REPRESENTED same-dest | Corrected source.md-run blocking totals over 84 valid runs: muse 21/18 runs, haiku 19/16, 
65. VL-20-065 | CORE -> CORE | REPRESENTED same-dest | Lesson: structured model output must be parsed only through one schema validator, never ad
66. VL-20-066 | EVAL -> EVAL | REPRESENTED same-dest | Owner ordered luna pre-source.md data quarantined to quarantine-pre-src-luna/ (428 reviewe
67. VL-20-067 | MODULE-tasklist -> CORE | REPRESENTED moved(documented) | From batch 4 the reviewer harness ships source.md beside candidate.md; b4-muse-luna2 await
68. VL-20-068 | EVAL -> EVAL | REPRESENTED same-dest | Batch 4/5 results (n2-sonnet-src, r2-sonnet-src 4/14 + 4/8, n4-sonnet-src 4/14 + 2/8 at 31
69. VL-20-069 | DROP -> DROP | REPRESENTED same-dest | Claim "source.md changed the picture completely; 0/8 blocking recall everywhere was an art
70. VL-20-070 | HARNESS -> HARNESS | REPRESENTED same-dest | n2-sonnet-src designSpec judge died with an Opus API error but left a plausible-looking sc
71. VL-20-071 | CORE -> CORE | REPRESENTED same-dest | Lesson: a failed judge can leave a plausible score file, so verdict artifacts need a compl
72. VL-20-072 | EVAL -> EVAL | REPRESENTED same-dest | Corrected n2-sonnet-src result 2/14, 0/8, 1 wrong blocker; the 8-of-10 / "source.md fixed 
73. VL-20-073 | EVAL -> EVAL | REPRESENTED same-dest | Batch 6 replaced muse-wonder-1.0 (weekly limit) with muse-ember-1.0: 60 runs all model_ok,
74. VL-20-074 | EVAL -> EVAL | REPRESENTED same-dest | Batch 6 rows: r2-sonnet-ember 2/14 + 1/8, n4-sonnet-ember 0/14, terra-muse-haiku-ember 2/1
75. VL-20-075 | EVAL -> EVAL | REPRESENTED same-dest | Batch 6 findings "ember is weaker than wonder" and "ember shifts toward precision on clean
76. VL-20-076 | EVAL -> EVAL | REPRESENTED same-dest | Correction: r2 never contained muse (haiku x2 + grok + sonnet), batch 6 added ember as a 5
77. VL-20-077 | CORE -> CORE | REPRESENTED same-dest | Lesson: row names (c/r/n/b4/e/g/h/j prefixes) hid composition, so composition must be read
78. VL-20-078 | EVAL -> EVAL | REPRESENTED same-dest | Batch 7: 45 runs all model_ok, 15 merges rc=0, 15 blind judges, API-error audit bad=0; emb
79. VL-20-079 | EVAL -> EVAL | REPRESENTED same-dest | Batch 7 rows e1 2/14 + 1/8 + 4 wrong blockers (240,961 tokens, 4,401 s), e2 2/14 + 1/8 + 2
80. VL-20-080 | EVAL -> EVAL | REPRESENTED same-dest | All five batch-7 rows tie at 2/14 any and 1/8 blocking; e2 replicates b4-muse-ember-luna2 
81. VL-20-081 | DROP -> DROP | REPRESENTED same-dest | Doubling analysis: "second run adds nothing", haiku overlap 8 of 8, per-reviewer yields (e
82. VL-20-082 | HARNESS -> HARNESS | REPRESENTED same-dest | analysis/attrib.py credits every reviewer on a merged ledger row rather than the judge-cit
83. VL-20-083 | EVAL -> EVAL | REPRESENTED same-dest | Independent keyword check of control GT2 over 83 src-era runs: grok 7/8, muse-wonder 8/9, 
84. VL-20-084 | EVAL -> EVAL | REPRESENTED same-dest | Lesson: single runs are coin flips, do not rank rows on 1-defect differences; decisions ne
85. VL-20-085 | EVAL -> EVAL | REPRESENTED same-dest | Batch 8 replicate study: 8 combos x 4 reps (+1x baseline), 300 reviewer runs, 108 merges r
86. VL-20-086 | EVAL -> EVAL | REPRESENTED same-dest | Batch 8 means: ember+luna 2.2/14 and 0.5 blocking at 52,398 tokens, ember+2luna 1.8/14, 2e
87. VL-20-087 | EVAL -> EVAL | REPRESENTED same-dest | Doubling-impact table: each effect within noise except "second luna raises control found +
88. VL-20-088 | EVAL -> EVAL | REPRESENTED same-dest | Independent proxy on control GT2: luna 1x panels 1/4 vs 2x panels 5/6; ember 2/4 vs 3/5
89. VL-20-089 | EVAL -> EVAL | REPRESENTED same-dest | Efficiency: ember+luna 4.2 catches/100k tokens, ember+2luna 2.8, sonnet+ember 1.7
90. VL-20-090 | EVAL -> EVAL | REPRESENTED same-dest | Nothing found beats about 2.2/14 except sonnet + ember at 2.5
91. VL-20-091 | HARNESS -> HARNESS | REPRESENTED same-dest | Batch 9: 24 merges and 24 blind judges; 20 judges first failed rc=127 because the claude b
92. VL-20-092 | HARNESS -> HARNESS | REPRESENTED same-dest | INCIDENT: during the 22:17-22:19 claude binary replacement the cyclic fallback ladder spun
93. VL-20-093 | CORE -> CORE | REPRESENTED same-dest | The model_ok check would have passed both bad slots because expected_model is overwritten 
94. VL-20-094 | HARNESS -> HARNESS | REPRESENTED same-dest | Fix: run-reviewer.sh never revisits a model, never uses glm or Qwen3.8-max, and honours NO
95. VL-20-095 | EVAL -> EVAL | REPRESENTED same-dest | Batch 9 rows: g6 1.8/14 with 4.8 wrong blockers; h1 haiku+2luna+2ember 2.2/14, 1.8 judge-b
96. VL-20-096 | EVAL -> EVAL | REPRESENTED same-dest | Add-one-reviewer effect table; adding haiku moved blocking 0.5 to 1.8/8 (later 1.00 real)
97. VL-20-097 | EVAL -> EVAL | REPRESENTED same-dest | Over 71 scored valid rows (32 distinct sets): 2/14 in 43 rows, 3/14 in 12, 4/14 in 4, neve
98. VL-20-098 | EVAL -> EVAL | REPRESENTED same-dest | Model presence effects (confounded): grok 2.62 vs 2.00 found, wonder 2.75 vs 1.98 (n=8), s
99. VL-20-099 | DROP -> DROP | REPRESENTED same-dest | Candidate batch-10 tests (grok+sonnet, haiku+sonnet) were dropped by the owner (:290)
100. VL-20-100 | MODULE-tasklist -> MODULE-tasklist | REPRESENTED same-dest | The five defects no valid row ever caught point at the review brief, the packages or the g
101. VL-20-101 | EVAL -> EVAL | REPRESENTED same-dest | Judge gt_covered_blocking counts a defect matched by a blocking-flagged row; over 71 rows 
102. VL-20-102 | CORE -> CORE | REPRESENTED same-dest | Merge keeps only well-formed finding lines and silently discards anchors over 200 chars (5
103. VL-20-103 | EVAL -> EVAL | REPRESENTED same-dest | Blocking findings lost by model: luna 30, ember 33, wonder 14, glm 7, haiku 7, grok 1, son
104. VL-20-104 | EVAL -> EVAL | REPRESENTED same-dest | Four verdicts flipped FAIL to PASS through dropped findings [CODE-CONTRADICTED, fix cycle 
105. VL-20-105 | CORE -> CORE | REPRESENTED same-dest | 83 merged rows lump unrelated findings into one row (chaining)
106. VL-20-106 | HARNESS -> HARNESS | REPRESENTED same-dest | Stale merges: n2-terra and r2-sol merged before their reports were re-run; n5-sol and n5-t
107. VL-20-107 | MODULE-tasklist -> CORE | REPRESENTED moved(documented) | 156 of 665 valid-era runs never referenced source.md (ember 81/209 = 39%, luna 49/222 = 22
108. VL-20-108 | EVAL -> EVAL | REPRESENTED same-dest | No run read ground truth, resolution files, other reviewers' reports or the report; old-er
109. VL-20-109 | EVAL -> EVAL | REPRESENTED same-dest | Terra and sol still produce incomplete reports (51 say incomplete, 16 empty terra reviews 
110. VL-20-110 | CORE -> CORE | REPRESENTED same-dest | luna anchor fidelity 91.4% verbatim vs 98-100% for other models
111. VL-20-111 | EVAL -> EVAL | REPRESENTED same-dest | Model identity audit A: 2 b4-muse-luna2 t2b-1 wonder runs served terra (row quarantined), 
112. VL-20-112 | EVAL -> EVAL | REPRESENTED same-dest | Audit E scoring: 294 judge outputs clean, blind re-judge of 12 rows agreed 12/12, 19/19 re
113. VL-20-113 | KNOWLEDGE -> KNOWLEDGE | REPRESENTED same-dest | Audit F also lists retracted lines still printed earlier in the append-only COMBO-REPORT (
114. VL-20-114 | EVAL -> EVAL | REPRESENTED same-dest | Statistics (Welch + permutation, n=4-6): second luna raises control found +0.83 (p 0.004 W
115. VL-20-115 | EVAL -> EVAL | REPRESENTED same-dest | Statistics: 2x luna + 2x ember has 2.75-3.25 more wrong blockers than every comparator (pe
116. VL-20-116 | EVAL -> EVAL | REPRESENTED same-dest | Statistics: ember + terra is worse by -1.75 found (permutation p 0.029)
117. VL-20-117 | EVAL -> EVAL | REPRESENTED same-dest | Valid-era rows 71, row-packages scored 213, row-packages with an audit EXCLUDE flag (A, B 
118. VL-20-118 | EVAL -> EVAL | REPRESENTED same-dest | AS SCORED leaders by found: grok+haiku+haiku+sonnet 4.00/14, 3.00 real blocking (n=1), 594
119. VL-20-119 | EVAL -> EVAL | REPRESENTED same-dest | Replicated leaders: ember+sonnet 2.50, ember+luna 2.25 at 52,398 tokens, haiku+luna+luna 2
120. VL-20-120 | EVAL -> EVAL | REPRESENTED same-dest | AUDIT-CLEAN table is a robustness check only and drops about one third of the data
121. VL-20-121 | EVAL -> EVAL | REPRESENTED same-dest | Reading guide: rows with 1/1/1 runs are anecdotes and only rows with 4+ runs per package s
122. VL-20-122 | MODULE-tasklist -> MODULE-tasklist | REPRESENTED same-dest | Decision: cost champion ember + luna (52k tokens, about 5 min, 2.25/14, control 0.00 wrong
123. VL-20-123 | MODULE-tasklist -> MODULE-tasklist | REPRESENTED same-dest | Decision: recommended default ember + 2x luna (64k tokens, about 6 min elapsed, 1.83/14 fo
124. VL-20-124 | MODULE-tasklist -> MODULE-tasklist | REPRESENTED same-dest | Decision: high-assurance haiku + 2x luna (191k tokens, 1.2/8 real blocking) and best preci
125. VL-20-125 | MODULE-tasklist -> MODULE-tasklist | REPRESENTED same-dest | Do-not-use list: ember+terra, 2x ember + 2x luna (4.75 wrong blockers), terra or sol alone
126. VL-20-126 | EVAL -> EVAL | REPRESENTED same-dest | Single-run high scores are unconfirmed (r2 family 4/14 with 3 real blocking at 594k tokens
127. VL-20-127 | CORE -> CORE | REPRESENTED same-dest | Pre-requisite fix 1: raise or truncate the 200-character anchor limit at merge, or instruc
128. VL-20-128 | MODULE-tasklist -> DROP | REPRESENTED dedup->DR-023 | Pre-requisite fix 2: name the source.md path explicitly in the reviewer brief (156-161 run
129. VL-20-129 | HARNESS -> HARNESS | REPRESENTED same-dest | Pre-requisite fix 3: keep the fallback-ladder fix and the model-identity audit in the runn
130. VL-20-130 | DROP -> DROP | REPRESENTED same-dest | No panel catches designSpec GT1, GT2, GT10 or alias GT4, so model choice cannot lift the c
131. VL-20-131 | EVAL -> EVAL | REPRESENTED same-dest | Timeline: candidates fixed 2026-11-11 17:35 and byte-identical to the sandbox copies; sour
132. VL-20-132 | EVAL -> EVAL | REPRESENTED same-dest | Three-way compare (analysis/three-way.py): sonnet+2luna n=1 (b4-sonnet-luna2) 4 found, 0 r
133. VL-20-133 | EVAL -> EVAL | REPRESENTED same-dest | Permutation tests p 0.54-1.0 except h2 vs ember+2luna wrong blockers 3.50 vs 1.83 (p 0.073
134. VL-20-134 | EVAL -> EVAL | REPRESENTED same-dest | Reliability: sonnet dropped 0 findings and read source.md every run; ember skipped source.
135. VL-20-135 | DROP -> DROP | REPRESENTED same-dest | Revised recommendation (sonnet + 2x luna as standard)
136. VL-20-136 | EVAL -> EVAL | REPRESENTED same-dest | Batch 11 (batch j1): sonnet+2luna replicated 5 times (j1-r1..r5), 45 runs, NOFALLBACK=1, o
137. VL-20-137 | HARNESS -> HARNESS | REPRESENTED same-dest | Batch 11: 5 runs failed when the claude binary was replaced at 13:48:51, were quarantined 
138. VL-20-138 | EVAL -> EVAL | REPRESENTED same-dest | Batch j1 per-run: b4 4,0,3,2 at 139,660 tokens and 793 s; j1-r1 2,0,2,1 at 148,599; j1-r2 
139. VL-20-139 | EVAL -> EVAL | REPRESENTED same-dest | Family n=6: found 2.33 (sd 0.94, range 1-4), real blocking 0.33, wrong blockers 1.83, cont
140. VL-20-140 | EVAL -> EVAL | REPRESENTED same-dest | Batch j1 permutations vs ember+2luna: found p=0.51, tokens and elapsed p=0.003
141. VL-20-141 | EVAL -> EVAL | REPRESENTED same-dest | Control GT1 (I7, no task updates the gh-api classification table) was reached in 3 of 6 so
142. VL-20-142 | EVAL -> EVAL | REPRESENTED same-dest | Batch j1 reliability: 2 of 30 luna findings blocks dropped at merge vs sonnet 0 of 15; 3 o
143. VL-20-143 | MODULE-tasklist -> MODULE-tasklist | REPRESENTED same-dest | Final guidance: default ember + 2x luna; optional quality tier sonnet + 2x luna (about +75
144. VL-20-144 | DROP -> DROP | REPRESENTED same-dest | All panels sit at about 2-2.5 of 14, so the harness fixes (anchor limit, source.md path in
145. VL-20-145 | EVAL -> EVAL | REPRESENTED same-dest | Issue-by-panel table: 10 parallel agents wrote analysis/issue-table/issue-NN.json; indepen
146. VL-20-146 | EVAL -> EVAL | REPRESENTED same-dest | B1 = designSpec GT1: Task 1 AC3 demands a provably complete inventory with no bounded meth
147. VL-20-147 | EVAL -> EVAL | REPRESENTED same-dest | B2 = designSpec GT2: Task 1 names 4 target files while AC3 says only "found for O3" (scope
148. VL-20-148 | EVAL -> EVAL | REPRESENTED same-dest | B3 = designSpec GT3: Task 9 tests the L3/draft condition without defining "condition"; two
149. VL-20-149 | EVAL -> EVAL | REPRESENTED same-dest | B4 = designSpec GT4: Task 8 vs Task 4 contradiction on the "unreadable" timeline
150. VL-20-150 | EVAL -> EVAL | REPRESENTED same-dest | B5 = designSpec GT5: Task 8 exit-report field drops the draft_guard_unavailable to unavail
151. VL-20-151 | EVAL -> EVAL | REPRESENTED same-dest | I1 = designSpec GT6: guard_status user_override issue
152. VL-20-152 | EVAL -> EVAL | REPRESENTED same-dest | I2 = designSpec GT7: resume_decision signature lacks target_sha and applied_edits
153. VL-20-153 | EVAL -> EVAL | REPRESENTED same-dest | I3 = designSpec GT8: place where the cycle id is minted is unspecified
154. VL-20-154 | EVAL -> EVAL | REPRESENTED same-dest | I4 = designSpec GT9: heading "Merge guard" vs case-sensitive grep "merge-guard"
155. VL-20-155 | EVAL -> EVAL | REPRESENTED same-dest | I5 = designSpec GT10: 43-member enum with no CHANGELOG edit
156. VL-20-156 | EVAL -> EVAL | REPRESENTED same-dest | B6 = alias GT1: aliases-only rule vs slot variables
157. VL-20-157 | EVAL -> EVAL | REPRESENTED same-dest | B7 = alias GT2: present-tense statement vs a defaults file that exports real model ids (ha
158. VL-20-158 | EVAL -> EVAL | REPRESENTED same-dest | B8 = alias GT3: tiers.md falsely states that all other primitives use aliases
159. VL-20-159 | EVAL -> EVAL | REPRESENTED same-dest | I6 = alias GT4: omitted half of the mapping constraint
160. VL-20-160 | EVAL -> EVAL | REPRESENTED same-dest | I7 = control GT1: no task updates tests/skills/test_worker_contract.py gh-api classificati
161. VL-20-161 | EVAL -> EVAL | REPRESENTED same-dest | I8 = control GT2: Complexity read-back match rule (numeric option id vs single_select_opti
162. VL-20-162 | EVAL -> EVAL | REPRESENTED same-dest | B1, B2, B6, I5 and I6 were never found by any top-10 panel; B3, I2 and I8 carry almost all
163. VL-20-163 | EVAL -> EVAL | REPRESENTED same-dest | Issue table scope: 106 runs (3 pilot arms + 103 scored combo rows, batch 10 dropped) in 62
164. VL-20-164 | EVAL -> EVAL | REPRESENTED same-dest | ALL row over 106 runs: B3 95, B4 3, B5 4, B6 1, B7 28, B8 2, I1 4, I2 71, I3 2, I4 4, I5 0
165. VL-20-165 | EVAL -> EVAL | REPRESENTED same-dest | Never found in 106 runs: B1, B2, I5, I6; B6 found once (luna+terra+wonder)
166. VL-20-166 | EVAL -> EVAL | REPRESENTED same-dest | Reach: widest sonnet+2luna (7 distinct issues over 6 runs); ember+sonnet and h2 6 each ove
167. VL-20-167 | EVAL -> EVAL | REPRESENTED same-dest | Sonnet was in 13 of 16 runs that reached I7: an association across non-random sets, not a 
168. VL-20-168 | EVAL -> EVAL | REPRESENTED same-dest | Caveats: S18 B5 credit is loose; S60 findings block failed to parse so its zeros partly re
169. VL-20-169 | DROP -> DROP | REPRESENTED same-dest | No result on the product superclaude review panel code (T2b tiers, @default/@live7 resolut
170. VL-20-170 | EVAL -> EVAL | REPRESENTED same-dest | Only 3 packages (2 defect-rich, 1 control), 16 GT defects of which 5 are never caught, no 
171. VL-20-171 | EVAL -> EVAL | REPRESENTED same-dest | No measurement of PASS/FAIL gate accuracy beyond GT coverage; verdict-vs-implement agreeme
172. VL-20-172 | EVAL -> EVAL | REPRESENTED same-dest | Judge is a single Opus pass per (combo, package); the 12-row re-judge (audit E) is the onl
173. VL-20-173 | EVAL -> EVAL | REPRESENTED same-dest | The hypothesis "name source.md in the brief" is untested (inference only); effect of the p
174. VL-20-174 | EVAL -> EVAL | REPRESENTED same-dest | No cost data for the Tier 1 reviewer vs the Opus judge in the same units beyond PILOT:52 (
175. VL-20-175 | CORE -> CORE | REPRESENTED same-dest | Wall time and tokens are reviewer output tokens only (COMBO-REPORT:204), not input or cach
176. VL-20-176 | HARNESS -> HARNESS | REPRESENTED same-dest | combos/SPEC.md procedure for a supervised worker is a reusable runbook pattern
177. VL-20-177 | DROP -> DROP | REPRESENTED same-dest | SPEC.md names a hard-coded Orca worktree path for EVAL and 3 package names
178. VL-20-178 | HARNESS -> HARNESS | REPRESENTED same-dest | Step 1: run run-reviewer.sh per reviewer; the script checks observed model and findings-v1
179. VL-20-179 | CORE -> CORE | REPRESENTED same-dest | Concurrency rule: at most 2 reviewers at once per worker because the gateway is untested a
180. VL-20-180 | HARNESS -> HARNESS | REPRESENTED same-dest | Step 2: per-package resolution built with jq from resolution-live7.json, selecting reviewe
181. VL-20-181 | HARNESS -> HARNESS | REPRESENTED same-dest | Step 3: superclaude review merge --ledger ... --doc <pkg>/candidate.md --round 1 --report 
182. VL-20-182 | HARNESS -> HARNESS | REPRESENTED same-dest | Step 4: RESULT.md table per package (reviewer, model, observed model, attempts, wall s, ou
183. VL-20-183 | HARNESS -> HARNESS | REPRESENTED same-dest | Hard limits for workers: read-only repo, do not open ground-truth*.json, other combos' fol
184. VL-20-184 | CORE -> CORE | REPRESENTED same-dest | Reviewer ids are only labels so the merge accepts them; the model per id lives only in the
185. VL-20-185 | DROP -> DROP | REPRESENTED same-dest | Correction 2026-11-11: brief listed category unpassable-ac but the merge validator accepts
186. VL-20-186 | EVAL -> EVAL | REPRESENTED same-dest | Speed-weighted rationale: gpt-6-luna 61-148 s (2.4k-6.7k tokens), claude-haiku-5-5 185-610
187. VL-20-187 | EVAL -> EVAL | REPRESENTED same-dest | Qwen3.8-max wording differs: SPEC says timed out twice (2 x 3000 s) on 3 of 4 runs, PILOT-
188. VL-20-188 | EVAL -> EVAL | REPRESENTED same-dest | Batch 1 combos c1-c5 (SPEC:8-14)
189. VL-20-189 | EVAL -> EVAL | REPRESENTED same-dest | Batch 2 rows r1-r5 and n1-n5 (muse-wonder-1.0 added by owner, pilot 153 s, about 17k token
190. VL-20-190 | EVAL -> EVAL | REPRESENTED same-dest | Batch 3 has 12 rows with ids t1b-1 (sonnet), t2b-1 (muse or terra), t2-1 (sol or terra) (S
191. VL-20-191 | CORE -> CORE | REPRESENTED same-dest | Re-run rules: waves of at most 4 workers, 1 concurrent reviewer each; if any reviewer fail
192. VL-20-192 | CORE -> CORE | REPRESENTED same-dest | Muse outage about 22:40 UTC 2026-11-11: requests return init model and billing as muse-won
193. VL-20-193 | KNOWLEDGE -> KNOWLEDGE | REPRESENTED same-dest | Owner decision 22:43 UTC: 60 minute cooldown after the muse outage
194. VL-20-194 | KNOWLEDGE -> KNOWLEDGE | REPRESENTED same-dest | glm outage about 08:25 UTC 2026-11-12: probe returned turns as qwen3.8-max, unrecognized_m
195. VL-20-195 | CORE -> CORE | REPRESENTED same-dest | Batch 4 root cause of terra/sol "incomplete": candidates reference ./source.md but the san
196. VL-20-196 | HARNESS -> HARNESS | REPRESENTED same-dest | Batch 4 amendment 14:42 UTC: all glm removed (owner: massive delays); 10 concurrent, muse 
197. VL-20-197 | EVAL -> EVAL | REPRESENTED same-dest | luna refused to review without source.md (25/25 empty on affected packages); luna data qua
198. VL-20-198 | EVAL -> EVAL | REPRESENTED same-dest | SPEC says 9 luna-bearing combo rows were quarantined while COMBO-REPORT:107 says 10 combo-
199. VL-20-199 | EVAL -> EVAL | REPRESENTED same-dest | Batch 5: owner's 7 shortlist combos mapped to rows; 5 new rows = 42 reviewer runs
200. VL-20-200 | DROP -> DROP | REPRESENTED same-dest | Muse misroute recurrence about 15:46 UTC; 2 runs quarantined in place with model_ok=false
201. VL-20-201 | HARNESS -> HARNESS | REPRESENTED same-dest | Batch 6 adds muse-ember-1.0 (owner adds it as "Tier 04 Model 02") with fallback ladder v1 
202. VL-20-202 | HARNESS -> HARNESS | REPRESENTED same-dest | Fallback ladder v2: tier-ordered succession (02 to 03 to 04, T3 to T4, T2 to T2b, T1 to T2
203. VL-20-203 | KNOWLEDGE -> KNOWLEDGE | REPRESENTED same-dest | muse-spark-1.3 and muse-wonder-full-1.0 misroute on the gateway (spark to sol, wonder-full
204. VL-20-204 | HARNESS -> HARNESS | REPRESENTED same-dest | Opus guard: T1a / Tier 0 Opus is never auto-selected by the ladder (owner-only)
205. VL-20-205 | EVAL -> EVAL | REPRESENTED same-dest | Batch 7: six rows, 54 runs, e4-haiku2-ember cancelled at 19:41 leaving 5 rows
206. VL-20-206 | EVAL -> EVAL | REPRESENTED same-dest | Batch 8: "9 combos x 4 replicates x 3 packages" (g1-g8 plus worker-added g9 baseline), 36 
207. VL-20-207 | CORE -> CORE | REPRESENTED same-dest | A second same-model reviewer in a panel takes the id t3-1
208. VL-20-208 | HARNESS -> HARNESS | REPRESENTED same-dest | Batch 9 incident quarantine dirs quarantine-haiku-fallback-20261112 and quarantine-qwen-fa
209. VL-20-209 | DROP -> DROP | REPRESENTED same-dest | Batch 10 (i1-grok-sonnet r1-r4, i2-haiku-sonnet r1-r4, 48 runs) dropped by owner 2026-11-1
210. VL-20-210 | HARNESS -> HARNESS | REPRESENTED same-dest | Batch 11: five replicates, one runner each at -P2 for 10 concurrent, NOFALLBACK=1; session
211. VL-20-211 | CORE -> CORE | REPRESENTED same-dest | Concurrency lesson: 12 concurrent workers caused identity bleed; 10 concurrent with muse c
212. VL-20-212 | HARNESS -> HARNESS | REPRESENTED same-dest | tools/run-reviewer.sh (87 lines, 8,089 B): usage run-reviewer.sh <EVAL abs> <pkg id> <revi
213. VL-20-213 | HARNESS -> HARNESS | REPRESENTED same-dest | run-reviewer.sh:6-8 copies candidate.md to a per-package sandbox copy /tmp/evalsb/cand/<pk
214. VL-20-214 | HARNESS -> HARNESS | REPRESENTED same-dest | run-reviewer.sh:10-11 ships source.md from the hard-coded absolute path of the E2 worktree
215. VL-20-215 | CORE -> CORE | REPRESENTED same-dest | run-reviewer.sh silently skips source.md when the file is absent (an "or true" guard) and 
216. VL-20-216 | HARNESS -> HARNESS | REPRESENTED same-dest | Brief (run-reviewer.sh:13-17) = /sc:spec-panel @<cand> --mode critique + first-review brie
217. VL-20-217 | DROP -> DROP | REPRESENTED same-dest | The brief does not name source.md anywhere (CODE-VERIFIED by the slice reading run-reviewe
218. VL-20-218 | CORE -> CORE | REPRESENTED same-dest | The brief says "If an input is missing or unreadable, return incomplete" and terra/sol too
219. VL-20-219 | HARNESS -> HARNESS | REPRESENTED same-dest | FALLBACK map (13 entries, :23-43): glm-5.3 to Qwen3.8-max to gpt-6-luna to muse-ember-1.0 
220. VL-20-220 | HARNESS -> HARNESS | REPRESENTED same-dest | run_attempt (:45-60): timeout 3000 claude -p --model "$MODEL" --output-format json --no-se
221. VL-20-221 | CORE -> CORE | REPRESENTED same-dest | Per-attempt meta: OBS = unique assistant message.model (parent_tool_use_id null), TOK, TOK
222. VL-20-222 | DROP -> DROP | REPRESENTED same-dest | The model identity check is sound only while $MODEL is not mutated; after fallback expecte
223. VL-20-223 | CORE -> CORE | REPRESENTED same-dest | BLOCK_OK checks only that the findings-v1 fence is present, not that it parses, so a block
224. VL-20-224 | HARNESS -> HARNESS | REPRESENTED same-dest | Two attempts per model before escalation (:61-64)
225. VL-20-225 | DROP -> DROP | REPRESENTED same-dest | Fallback escalation unless NOFALLBACK is set (:66-83), EXCLUDE_MODELS default "glm-5.3 Qwe
226. VL-20-226 | HARNESS -> HARNESS | REPRESENTED same-dest | Final output (:85-87): last attempt copied to <id>.md and <id>.meta.json; <id>.cost.json =
227. VL-20-227 | CORE -> CORE | REPRESENTED same-dest | Reviewer isolation is weak: --permission-mode bypassPermissions with only Edit, Write and 
228. VL-20-228 | DROP -> DROP | REPRESENTED same-dest | Audit C found no run read ground truth or other reviewers' reports, but old-era runs brows
229. VL-20-229 | MODULE-tasklist -> MODULE-tasklist | REPRESENTED same-dest | The source.md copy path is .dev/tasks/done/<pkg>/source.md in the E2 worktree: the input e
230. VL-20-230 | HARNESS -> HARNESS | REPRESENTED same-dest | .bad-launch:19 used the variadic --disallowedTools option which consumed the prompt (error
231. VL-20-231 | DROP -> DROP | REPRESENTED same-dest | reviews-failed-launch-1 directories hold the failed launches (56 files design, 49 designSp
232. VL-20-232 | DROP -> DROP | REPRESENTED same-dest | .unpassable-ac differs from .bad-launch only by the stdin fix and a cmp -s skip-copy (diff
233. VL-20-233 | DROP -> DROP | REPRESENTED same-dest | Harness defect (a): variadic CLI flag swallowed the prompt (bad-launch)
234. VL-20-234 | DROP -> DROP | REPRESENTED same-dest | Harness defect (b): brief category typo unpassable-ac vs validator unpassable-check
235. VL-20-235 | DROP -> DROP | REPRESENTED same-dest | Harness defect (c): brief never ships source.md until batch 4 (2026-11-12 about 12:59)
236. VL-20-236 | DROP -> DROP | REPRESENTED same-dest | Harness defect (d): cyclic fallback ladder with overwritten expected_model (batch 9)
237. VL-20-237 | HARNESS -> HARNESS | REPRESENTED same-dest | Harness defect (e): claude binary replaced mid-run (exit 127; batches 9, 10, 11) is handle
238. VL-20-238 | CORE -> CORE | REPRESENTED same-dest | Harness defect (f): Qwen and glm exclusions are an env default (EXCLUDE_MODELS), not a per
239. VL-20-239 | CORE -> CORE | REPRESENTED same-dest | Slice states CODE-VERIFIED at HEAD that document_review_loop_prompts.md:60 and findings.py
240. VL-20-240 | HARNESS -> HARNESS | REPRESENTED same-dest | tools/tmp-scripts/README.md (4 lines, 728 B): helper scripts that lived only in /tmp, copi
241. VL-20-241 | HARNESS -> DROP | REPRESENTED dedup->DR-086 | README names checks-gate8 but it is not in the 55-file list (UNVERIFIED missing)
242. VL-20-242 | HARNESS -> HARNESS | REPRESENTED same-dest | tools/tmp-scripts/anon-arms.sh: arm label pool X/Y/Z random per package, key arm-key.json;
243. VL-20-243 | HARNESS -> HARNESS | REPRESENTED same-dest | tools/tmp-scripts/anon-b7.sh (batch-7 anonymiser scaling the anon-combos pattern)
244. VL-20-244 | HARNESS -> HARNESS | REPRESENTED same-dest | tools/tmp-scripts/anon-b8.sh (batch-8 anonymiser)
245. VL-20-245 | HARNESS -> HARNESS | REPRESENTED same-dest | tools/tmp-scripts/anon-b9.sh (batch-9 anonymiser)
246. VL-20-246 | HARNESS -> HARNESS | REPRESENTED same-dest | tools/tmp-scripts/anon-b11.sh (batch-11 anonymiser)
247. VL-20-247 | HARNESS -> HARNESS | REPRESENTED same-dest | tools/tmp-scripts/anon-combos.sh: combo label pool Q..V (label-key.json), uniqueness per (
248. VL-20-248 | EVAL -> EVAL | REPRESENTED same-dest | Anonymisation is regex-based, only tier-shaped reviewer ids are mapped, and the combo labe
249. VL-20-249 | EVAL -> EVAL | REPRESENTED same-dest | Leak check at tip: 54 of 319 merged-anon.md files contain a model-id string; sampled hits 
250. VL-20-250 | HARNESS -> HARNESS | REPRESENTED same-dest | tools/tmp-scripts/arm-merges.sh (pilot arm merges)
251. VL-20-251 | HARNESS -> HARNESS | REPRESENTED same-dest | tools/tmp-scripts/merge-b6.sh: builds resolution JSON by hand (reviewer_id, model, alias, 
252. VL-20-252 | HARNESS -> HARNESS | REPRESENTED same-dest | merge-b6.sh skip rule [ -f merged-1.md ] && skip (:18) is why stale merges survived (n2-te
253. VL-20-253 | HARNESS -> HARNESS | REPRESENTED same-dest | tools/tmp-scripts/merge-src-rows.sh (merge of -src rows)
254. VL-20-254 | HARNESS -> HARNESS | REPRESENTED same-dest | tools/tmp-scripts/b4-job-one.sh: per-row cancel sentinel /tmp/cancel-<combo> (:5), START/E
255. VL-20-255 | HARNESS -> HARNESS | REPRESENTED same-dest | tools/tmp-scripts/b4-luna-muse.sh (batch-4 runner)
256. VL-20-256 | HARNESS -> HARNESS | REPRESENTED same-dest | tools/tmp-scripts/b4-luna-muse-gated.sh (batch-4 runner, gated)
257. VL-20-257 | HARNESS -> HARNESS | REPRESENTED same-dest | tools/tmp-scripts/b4-luna-nomuse.sh (batch-4 runner)
258. VL-20-258 | HARNESS -> HARNESS | REPRESENTED same-dest | tools/tmp-scripts/b4-par-launch.sh (batch-4 parallel launcher)
259. VL-20-259 | HARNESS -> HARNESS | REPRESENTED same-dest | tools/tmp-scripts/b4-par.sh (batch-4 parallel runner)
260. VL-20-260 | HARNESS -> HARNESS | REPRESENTED same-dest | tools/tmp-scripts/b4-run-noglm.sh (batch-4 runner without glm)
261. VL-20-261 | HARNESS -> HARNESS | REPRESENTED same-dest | tools/tmp-scripts/b4-run.sh (batch-4 runner)
262. VL-20-262 | HARNESS -> HARNESS | REPRESENTED same-dest | tools/tmp-scripts/b4-terra-alone.sh (batch-4 terra-alone runner)
263. VL-20-263 | HARNESS -> HARNESS | REPRESENTED same-dest | tools/tmp-scripts/b5-jobs-gen.sh (batch-5 job generator)
264. VL-20-264 | HARNESS -> HARNESS | REPRESENTED same-dest | tools/tmp-scripts/b6-launch.sh (batch-6 launcher)
265. VL-20-265 | HARNESS -> HARNESS | REPRESENTED same-dest | tools/tmp-scripts/b10-rerun-one.sh (batch-10 single-row rerun)
266. VL-20-266 | HARNESS -> HARNESS | REPRESENTED same-dest | tools/tmp-scripts/c1-driver.sh (batch-1 driver)
267. VL-20-267 | HARNESS -> HARNESS | REPRESENTED same-dest | tools/tmp-scripts/c2-run.sh (batch-1 runner)
268. VL-20-268 | HARNESS -> HARNESS | REPRESENTED same-dest | tools/tmp-scripts/c3-run.sh (batch-1 runner)
269. VL-20-269 | HARNESS -> HARNESS | REPRESENTED same-dest | tools/tmp-scripts/c5-chain.sh (batch-1 chained runner)
270. VL-20-270 | HARNESS -> HARNESS | REPRESENTED same-dest | tools/tmp-scripts/n2sonnet-run.sh (n2 sonnet runner)
271. VL-20-271 | HARNESS -> HARNESS | REPRESENTED same-dest | tools/tmp-scripts/n2terra-run.sh (n2 terra runner)
272. VL-20-272 | HARNESS -> HARNESS | REPRESENTED same-dest | tools/tmp-scripts/n2terra-wait.sh (n2 terra wait helper)
273. VL-20-273 | HARNESS -> HARNESS | REPRESENTED same-dest | tools/tmp-scripts/n3-run.sh (n3 runner)
274. VL-20-274 | HARNESS -> HARNESS | REPRESENTED same-dest | tools/tmp-scripts/n4terra-run.sh (n4 terra runner)
275. VL-20-275 | HARNESS -> HARNESS | REPRESENTED same-dest | tools/tmp-scripts/n5-driver.sh (n5 driver)
276. VL-20-276 | HARNESS -> HARNESS | REPRESENTED same-dest | tools/tmp-scripts/n5-finish.sh (n5 finisher)
277. VL-20-277 | HARNESS -> HARNESS | REPRESENTED same-dest | tools/tmp-scripts/n5s-run.sh (n5 sonnet runner)
278. VL-20-278 | HARNESS -> HARNESS | REPRESENTED same-dest | tools/tmp-scripts/n5sol-run.sh (n5 sol runner)
279. VL-20-279 | HARNESS -> HARNESS | REPRESENTED same-dest | tools/tmp-scripts/n5sol-run2.sh (n5 sol second runner)
280. VL-20-280 | HARNESS -> HARNESS | REPRESENTED same-dest | tools/tmp-scripts/n5terra-jobs.sh (n5 terra job list)
281. VL-20-281 | HARNESS -> HARNESS | REPRESENTED same-dest | tools/tmp-scripts/n5terra-run.sh (n5 terra runner)
282. VL-20-282 | HARNESS -> HARNESS | REPRESENTED same-dest | tools/tmp-scripts/r2-sonnet-driver.sh (r2 sonnet driver)
283. VL-20-283 | HARNESS -> HARNESS | REPRESENTED same-dest | tools/tmp-scripts/r2s-run.sh (r2 sonnet runner)
284. VL-20-284 | HARNESS -> HARNESS | REPRESENTED same-dest | tools/tmp-scripts/r2sol-run.sh (r2 sol runner)
285. VL-20-285 | HARNESS -> HARNESS | REPRESENTED same-dest | tools/tmp-scripts/r2terra-run.sh (r2 terra runner)
286. VL-20-286 | HARNESS -> HARNESS | REPRESENTED same-dest | tools/tmp-scripts/r3-run.sh (r3 runner)
287. VL-20-287 | HARNESS -> HARNESS | REPRESENTED same-dest | tools/tmp-scripts/r5-run.sh (r5 runner)
288. VL-20-288 | HARNESS -> HARNESS | REPRESENTED same-dest | tools/tmp-scripts/startcombo.sh (combo starter)
289. VL-20-289 | HARNESS -> HARNESS | REPRESENTED same-dest | tools/tmp-scripts/startcombo2.sh (combo starter v2)
290. VL-20-290 | HARNESS -> HARNESS | REPRESENTED same-dest | tools/tmp-scripts/startcombo3.sh (combo starter v3)
291. VL-20-291 | EVAL -> EVAL | REPRESENTED same-dest | tools/tmp-scripts/judge-one.sh (2,307 B): claude -p --model claude-opus-5-5 --output-forma
292. VL-20-292 | HARNESS -> HARNESS | REPRESENTED same-dest | tools/tmp-scripts/gen-judge-list.sh (558 B) generates the judge job list
293. VL-20-293 | HARNESS -> HARNESS | REPRESENTED same-dest | tools/tmp-scripts/run-combo-judges.sh (2,771 B) runs the judges; line 2 comment says 39 ju
294. VL-20-294 | HARNESS -> HARNESS | REPRESENTED same-dest | tools/tmp-scripts/brief_c1.py (6,373 B)
295. VL-20-295 | HARNESS -> HARNESS | REPRESENTED same-dest | tools/tmp-scripts/drift-b3.py:2 reads .dev/eval-workspaces/shadow-model-combos/input/TASK-
296. VL-20-296 | HARNESS -> HARNESS | REPRESENTED same-dest | tools/tmp-scripts/snap.py:4 writes an E1 run's artifacts/input-snapshot.yaml with input_tr
297. VL-20-297 | HARNESS -> HARNESS | REPRESENTED same-dest | tools/tmp-scripts/stats.sh greps "blocking" *: *true (space-tolerant, :14), the post-corre
298. VL-20-298 | HARNESS -> HARNESS | REPRESENTED same-dest | tools/tmp-scripts/rlog-r3.sh (r3 run log helper)
299. VL-20-299 | HARNESS -> HARNESS | REPRESENTED same-dest | Judge defect 1: [ -f "$D/score.json" ] && SKIP (judge-one.sh:7, run-combo-judges.sh:11) me
300. VL-20-300 | HARNESS -> HARNESS | REPRESENTED same-dest | Judge defect 2: success test is rc 0 and valid judge.json (:28), not that score.json was w
301. VL-20-301 | DROP -> DROP | REPRESENTED same-dest | Judge defect 3: judge gt_covered_blocking ignores the GT field blocking_in_implement (brie
302. VL-20-302 | DROP -> DROP | REPRESENTED same-dest | Judge defect 4: "wrong blocker" = blocking row with no GT correspondence (:20), structural
303. VL-20-303 | HARNESS -> HARNESS | REPRESENTED same-dest | Judge defect 5: judge runs on claude-opus-5-5 with bypassPermissions and is only told "Do 
304. VL-20-304 | HARNESS -> HARNESS | REPRESENTED same-dest | Judge defect 6: run-combo-judges.sh:2 hard-codes 39 judges (13 combos x 3)
305. VL-20-305 | EVAL -> EVAL | REPRESENTED same-dest | Package TASK-WF-designSpec-20261107-075614: candidate.md 200 lines, 10 GT items (5 blockin
306. VL-20-306 | EVAL -> EVAL | REPRESENTED same-dest | Package TASK-WF-makeTheAliasOnly-20261105-051649: candidate.md 134 lines, 4 GT items (3 bl
307. VL-20-307 | EVAL -> EVAL | REPRESENTED same-dest | Package TASK-WF-design-20261108-041415: candidate.md 173 lines, 2 GT items (0 blocking), a
308. VL-20-308 | EVAL -> EVAL | REPRESENTED same-dest | Totals re-derived by slice: 16 GT items, 8 blocking, matching PILOT-REPORT:7 and COMBO-REP
309. VL-20-309 | EVAL -> EVAL | REPRESENTED same-dest | GT classes (unpassable-ac, missing-task, ambiguity, contradiction) differ from findings-v1
310. VL-20-310 | EVAL -> EVAL | REPRESENTED same-dest | GT provenance: defects observed in past /sc:implement runs; blocking_in_implement means th
311. VL-20-311 | EVAL -> EVAL | REPRESENTED same-dest | designSpec GT1 and GT2 describe two plan defects behind the same Task 1 failure (5 attempt
312. VL-20-312 | EVAL -> EVAL | REPRESENTED same-dest | designSpec GT6 comes from the advisory plan review in executor-guidance.md; the referenced
313. VL-20-313 | EVAL -> EVAL | REPRESENTED same-dest | alias dropped GT5 (stale commands.py citations, evidence_ok false) and GT6 (executor's own
314. VL-20-314 | EVAL -> EVAL | REPRESENTED same-dest | design: every task T1-T12 finished compliant on its first attempt (FINAL pass), so no item
315. VL-20-315 | EVAL -> EVAL | REPRESENTED same-dest | The control is not a clean plan: it has 2 real non-blocking GT defects, so a FAIL there is
316. VL-20-316 | CORE -> CORE | REPRESENTED same-dest | Per-package resolution-default.json and resolution-live7.json (schema review-panel-resolut
317. VL-20-317 | EVAL -> EVAL | REPRESENTED same-dest | Verified panel compositions: designSpec default = t1b sonnet, t2 muse-spark-1.3, t3 glm-5.
318. VL-20-318 | MODULE-tasklist -> CORE | REPRESENTED moved(documented) | Product templates at HEAD (slice marks CODE-VERIFIED): review-panel.live7.json = t1b(fixed
319. VL-20-319 | MODULE-tasklist -> DROP | REPRESENTED dedup->DR-016 | review-tiers.default.json at HEAD: tier3 = [glm-5.3, Qwen3.8-max], tier4 = [gpt-6-luna, cl
320. VL-20-320 | MODULE-tasklist -> CORE | REPRESENTED moved(documented) | Study excluded glm-5.3 and Qwen3.8-max, the only Tier 3 models in the product tiers file, 
321. VL-20-321 | DROP -> DROP | REPRESENTED same-dest | Qwen3.8-max reviewer ids in resolutions: designSpec t3-2, alias t3-1, design t2-1 and desi
322. VL-20-322 | EVAL -> EVAL | REPRESENTED same-dest | E1 shadow-model-combos input plan TASK-WF-designSpec-20261107-075614.md (sha256 044809e3..
323. VL-20-323 | EVAL -> EVAL | REPRESENTED same-dest | E1 source.md sha256 a865f397... equals .dev/tasks/done/TASK-WF-designSpec-20261107-075614/
324. VL-20-324 | EVAL -> EVAL | REPRESENTED same-dest | source.md sha256 prefixes at HEAD for the other packages: alias 9c7df653062887a4, design 1
325. VL-20-325 | EVAL -> EVAL | REPRESENTED same-dest | analysis/final-table.md (6,375 B, 59 lines), same content as COMBO-REPORT:303-359
326. VL-20-326 | EVAL -> EVAL | REPRESENTED same-dest | analysis/b8-final.md (2,891 B, 27 lines)
327. VL-20-327 | EVAL -> EVAL | REPRESENTED same-dest | analysis/b9-final.md (2,149 B, 17 lines)
328. VL-20-328 | EVAL -> EVAL | REPRESENTED same-dest | analysis/final-all.json (9,540 B)
329. VL-20-329 | EVAL -> EVAL | REPRESENTED same-dest | analysis/final-clean.json (5,641 B)
330. VL-20-330 | DROP -> DROP | REPRESENTED same-dest | analysis/attrib.out (2,415 B)
331. VL-20-331 | DROP -> DROP | REPRESENTED same-dest | analysis/doubles.out (1,824 B)
332. VL-20-332 | EVAL -> EVAL | REPRESENTED same-dest | analysis/untried.out (4,052 B)
333. VL-20-333 | EVAL -> EVAL | REPRESENTED same-dest | analysis/gt2-hits.txt (362 B)
334. VL-20-334 | DROP -> DROP | REPRESENTED same-dest | analysis/combo-est-A.md (5,612 B, 51 lines): analyst estimate of the top-5 untried combos,
335. VL-20-335 | DROP -> DROP | REPRESENTED same-dest | analysis/combo-est-B.md (7,918 B, 66 lines): second independent estimate of the same combo
336. VL-20-336 | DROP -> DROP | REPRESENTED same-dest | analysis/combo-est-self.md (2,062 B, 25 lines): third estimate of the same combos
337. VL-20-337 | EVAL -> EVAL | REPRESENTED same-dest | combo-est-self.md:3-12 per-model stats (source.md era, 3 packages): sonnet 27 runs, 29.4k 
338. VL-20-338 | EVAL -> EVAL | REPRESENTED same-dest | combo-est-self.md:23: arm A was never re-run with source.md, so COMBO-REPORT:59/67 compare
339. VL-20-339 | EVAL -> EVAL | REPRESENTED same-dest | combo-est-B.md:3-26 per-model GT hits: sonnet catches designSpec GT3 in about 7 of 8 rows,
340. VL-20-340 | EVAL -> EVAL | REPRESENTED same-dest | combo-est-A.md:11 per-model total tokens (3 packages): terra about 7k, sol 12k, luna 25k, 
341. VL-20-341 | DROP -> DROP | REPRESENTED same-dest | analysis/attrib.py (78 lines): "Approximate: parses judge prose", wrong blockers credited 
342. VL-20-342 | DROP -> DROP | REPRESENTED same-dest | analysis/doubles.py (1,374 B)
343. VL-20-343 | HARNESS -> HARNESS | REPRESENTED same-dest | analysis/untried.py (46 lines)
344. VL-20-344 | HARNESS -> HARNESS | REPRESENTED same-dest | analysis/three-way.py (63 lines): three-way panel comparison with permutation tests
345. VL-20-345 | HARNESS -> HARNESS | REPRESENTED same-dest | three-way.py:4 executes /tmp/final-table.py, a file not in the commit
346. VL-20-346 | HARNESS -> HARNESS | REPRESENTED same-dest | analysis/final-table.py (83 lines): valid(r) by row-name pattern (-src, b4-*, -ember, [egh
347. VL-20-347 | HARNESS -> HARNESS | REPRESENTED same-dest | analysis/b8-table.py (88 lines) with family definitions FAM
348. VL-20-348 | HARNESS -> HARNESS | REPRESENTED same-dest | analysis/b9-table.py (3,241 B)
349. VL-20-349 | HARNESS -> HARNESS | REPRESENTED same-dest | Reproducibility defect: the analysis scripts hard-code /home/coder/workspaces/worktrees/Ir
350. VL-20-350 | HARNESS -> HARNESS | REPRESENTED same-dest | The valid-era selector is a row-NAME pattern while composition is read from meta.json else
351. VL-20-351 | HARNESS -> HARNESS | REPRESENTED same-dest | analysis/b7-launch.sh (batch-7 launcher)
352. VL-20-352 | HARNESS -> HARNESS | REPRESENTED same-dest | analysis/b8-launch.sh (batch-8 launcher)
353. VL-20-353 | HARNESS -> HARNESS | REPRESENTED same-dest | analysis/b9-launch.sh (batch-9 launcher)
354. VL-20-354 | DROP -> DROP | REPRESENTED same-dest | analysis/b10-launch.sh (batch-10 launcher)
355. VL-20-355 | HARNESS -> HARNESS | REPRESENTED same-dest | analysis/b11-launch.sh (batch-11 launcher)
356. VL-20-356 | HARNESS -> HARNESS | REPRESENTED same-dest | analysis/b11-rerun-one.sh (batch-11 single-row rerun)
357. VL-20-357 | HARNESS -> HARNESS | REPRESENTED same-dest | analysis/merge-b7.sh (batch-7 merge, pattern of merge-b6.sh)
358. VL-20-358 | HARNESS -> HARNESS | REPRESENTED same-dest | analysis/merge-b8.sh (batch-8 merge)
359. VL-20-359 | HARNESS -> HARNESS | REPRESENTED same-dest | analysis/merge-b9.sh (batch-9 merge)
360. VL-20-360 | DROP -> DROP | REPRESENTED same-dest | analysis/merge-b10.sh (batch-10 merge)
361. VL-20-361 | HARNESS -> HARNESS | REPRESENTED same-dest | analysis/merge-b11.sh (batch-11 merge)
362. VL-20-362 | HARNESS -> HARNESS | REPRESENTED same-dest | analysis/b7-judge.tsv (832 B) judge job list
363. VL-20-363 | HARNESS -> HARNESS | REPRESENTED same-dest | analysis/b8-judge.tsv (6,168 B) judge job list
364. VL-20-364 | HARNESS -> HARNESS | REPRESENTED same-dest | analysis/b9-judge.tsv (1,516 B) judge job list
365. VL-20-365 | HARNESS -> HARNESS | REPRESENTED same-dest | analysis/b11-judge.tsv (850 B) judge job list
366. VL-20-366 | DROP -> DROP | REPRESENTED same-dest | analysis/b10-fix.txt (578 B)
367. VL-20-367 | HARNESS -> HARNESS | REPRESENTED same-dest | analysis/b11-fix.txt (358 B)
368. VL-20-368 | DROP -> DROP | REPRESENTED same-dest | analysis/attrib.json exists in the tree but slice 03 section 8.1 does not name it
369. VL-20-369 | HARNESS -> HARNESS | REPRESENTED same-dest | Audit A (model identity and attempts) scripts: audit.py (12,976 B), flags.tsv, stats.json,
370. VL-20-370 | EVAL -> EVAL | REPRESENTED same-dest | Audit A: 890 reviewer runs in 70 rows (batch 10 excluded); 1 root-cause EXCLUDE = 2 runs (
371. VL-20-371 | KNOWLEDGE -> KNOWLEDGE | REPRESENTED same-dest | unrecognized_model in 744 attempt .err files is a benign client warning for non-Claude mod
372. VL-20-372 | EVAL -> EVAL | REPRESENTED same-dest | 57 of 59 modelUsage extra keys are an auxiliary call to alias claude-gw-tier2[1m] (about 5
373. VL-20-373 | KNOWLEDGE -> KNOWLEDGE | REPRESENTED same-dest | 10 retries (glm x7 where attempt1 observed glm-5.3 and qwen3.8-max)
374. VL-20-374 | HARNESS -> HARNESS | REPRESENTED same-dest | 5 runs have stale attempt2 leftovers that over-count cost (:15)
375. VL-20-375 | EVAL -> EVAL | REPRESENTED same-dest | 8 earlier-attempt model differences (:25) and terra short reports under 400 tokens: 2 WARN
376. VL-20-376 | HARNESS -> HARNESS | REPRESENTED same-dest | Audit B (report validity, incomplete reports) scripts: audit.py (14,375 B), flags.tsv (28,
377. VL-20-377 | DROP -> DROP | REPRESENTED same-dest | Audit B stats: 51 reports say incomplete, 16 empty terra reviews valid-era [CODE-CONTRADIC
378. VL-20-378 | HARNESS -> HARNESS | REPRESENTED same-dest | Audit C (inputs, timing, source.md references) scripts: audit.py (14,724 B), flags.tsv (45
379. VL-20-379 | DROP -> DROP | REPRESENTED same-dest | Audit C result: 156 of 665 valid-era runs never referenced source.md; no GT or other-repor
380. VL-20-380 | HARNESS -> HARNESS | REPRESENTED same-dest | Audit D (merge and ledger integrity) scripts: audit.py, audit2.py, mk.py, anch.py, bok.py,
381. VL-20-381 | EVAL -> EVAL | REPRESENTED same-dest | Audit D scope: 89 rows x 3 packages = 264 merged-1.md examined (:3), counts C1-C6 (:5-12);
382. VL-20-382 | EVAL -> EVAL | REPRESENTED same-dest | Audit D drop reasons: anchor over 200 chars 56, anchor2 over 200 18, claim over 300 14, ba
383. VL-20-383 | DROP -> DROP | REPRESENTED same-dest | Audit D dropped findings by model: luna 30, ember 33, wonder 14, glm 7, haiku 7, grok 1, s
384. VL-20-384 | EVAL -> EVAL | REPRESENTED same-dest | Audit D kept/raw ledger counts: haiku 1085/1108, sonnet 446/446, glm 86/93, luna 356/386, 
385. VL-20-385 | DROP -> DROP | REPRESENTED same-dest | Audit D: 49 dropped findings were blocking (:8, :19)
386. VL-20-386 | EVAL -> EVAL | REPRESENTED same-dest | Audit D lists 3 explicit verdict flips (g3-sonnet-luna-ember-r3 alias t4-1 F1; g5-ember2-l
387. VL-20-387 | EVAL -> EVAL | REPRESENTED same-dest | Total-loss merges listed by audit D: g1-ember-luna2-r4 alias t3-1; g7-haiku-luna2-r4 desig
388. VL-20-388 | CORE -> CORE | REPRESENTED same-dest | X1 clustering: findings.py cluster() union-find; 195 of 1398 rows with 3 or more members a
389. VL-20-389 | CORE -> CORE | REPRESENTED same-dest | A merged row's anchor and claim = first member only, so a row can match the wrong defect a
390. VL-20-390 | CORE -> CORE | REPRESENTED same-dest | X2: 46 rows have a null span (anchor not found in the candidate), 13 of them blocking
391. VL-20-391 | EVAL -> EVAL | REPRESENTED same-dest | X3 reviewer/fid mapping 0 mismatches and X5 0 verdict/row logic violations
392. VL-20-392 | DROP -> DROP | REPRESENTED same-dest | Stale merges: n2-terra (3 packages t2-1+t4-1), r2-sol design t2-1+t4-2 (16 EXCLUDE) (:10);
393. VL-20-393 | HARNESS -> HARNESS | REPRESENTED same-dest | 45 merges lack merge-stdout.txt, so merge warnings are unverifiable (:26)
394. VL-20-394 | HARNESS -> HARNESS | REPRESENTED same-dest | Audit E (scoring integrity) scripts: check.py (11,228 B), check2.py, by.json, rows.json, f
395. VL-20-395 | DROP -> DROP | REPRESENTED same-dest | Audit E result: 294 judge outputs clean, 12/12 re-judge agreement, 19/19 catches confirmed
396. VL-20-396 | HARNESS -> HARNESS | REPRESENTED same-dest | Audit F (aggregation, stale text) scripts: recompute.py (17,857 B), extra.py, extra2.py, n
397. VL-20-397 | DROP -> DROP | REPRESENTED same-dest | Audit F result: blocking-definition finding (65 vs 38) and Welch/permutation statistics
398. VL-20-398 | EVAL -> EVAL | REPRESENTED same-dest | Only audits A and D ship a summary.md; the headlines of B, C, E, F are known from COMBO-RE
399. VL-20-399 | EVAL -> EVAL | REPRESENTED same-dest | analysis/issue-table (28 files): issue-01..10.json/.tsv, issue-legend.json/.tsv, issue-tab
400. VL-20-400 | HARNESS -> HARNESS | REPRESENTED same-dest | issue-table scripts: issue-setup.py, issue-compare.py, issue-table.py
401. VL-20-401 | EVAL -> EVAL | REPRESENTED same-dest | analysis/allsets (29 files): allsets-chunks/chunk-01..10.json, allsets-out/chunk-01..10.js
402. VL-20-402 | HARNESS -> HARNESS | REPRESENTED same-dest | allsets scripts: chunk05_script.py, build03.py, c10.py, allsets-setup.py, allsets-table.py
403. VL-20-403 | CORE -> CORE | REPRESENTED same-dest | Pattern "agents propose, script confirms": agent-built tables cross-checked by an independ
404. VL-20-404 | DROP -> DROP | REPRESENTED same-dest | C1: the merge validator accepts only unpassable-check (findings.py:15-22 CATEGORIES; check
405. VL-20-405 | DROP -> DROP | REPRESENTED same-dest | C2: product rule document_review_loop_prompts.md:60 lists unpassable-check, identical at t
406. VL-20-406 | CORE -> CORE | REPRESENTED same-dest | C3: findings.py:90-121 _check_finding limits: anchor 12..200 (:104), anchor2 12..200 (:107
407. VL-20-407 | CORE -> DROP | FLAG DEDUP-CHAIN-BROKEN | dedup->BROKEN-CHAIN:VL-20-407 | C4: the drop is not silent as COMBO-REPORT:292 says: ledger.py:130-134 appends a warning p
408. VL-20-408 | CORE -> CORE | REPRESENTED same-dest | C5: the verdict is "FAIL" if the brief of open or regressed blocking rows is non-empty els
409. VL-20-409 | CORE -> CORE | REPRESENTED same-dest | C6: the merge refuses a round only when no reviewer produced a valid block (ledger.py:150-
410. VL-20-410 | CORE -> CORE | REPRESENTED same-dest | C7: clustering is transitive union-find over same_defect (findings.py:367-407; same finger
411. VL-20-411 | CORE -> CORE | REPRESENTED same-dest | C8: an anchor not found in the candidate gives span None and is kept but not clustered by 
412. VL-20-412 | CORE -> CORE | REPRESENTED same-dest | C9: a stale ledger gives LedgerError "round {n} cannot be merged: the ledger expects round
413. VL-20-413 | DROP -> DROP | REPRESENTED same-dest | C10: resolution JSON fields strategy, stand_in, fallback_depth, fallbacks, launch, seed, s
414. VL-20-414 | DROP -> DROP | REPRESENTED same-dest | C11: @live7 resolves 7 reviewers and tier2b models are [gpt-6.1-terra, glm-5.3, Qwen3.8-ma
415. VL-20-415 | CORE -> CORE | REPRESENTED same-dest | C12: review-tiers.default.json:26,29 gateway environment has note "dispatch mechanism per 
416. VL-20-416 | CORE -> CORE | REPRESENTED same-dest | C13: reflect panel profiles cap Claude-launched reviewers (panel.py:71-73 _REFLECT_PREFIX 
417. VL-20-417 | CORE -> CORE | REPRESENTED same-dest | C14: findings-v2 is a superset container (findings_v2.py:9-43 V1_FIELDS, ROLES, LENSES, CH
418. VL-20-418 | EVAL -> EVAL | REPRESENTED same-dest | C15: judge and arm numbers (all score tables) are not code; scripts and raw judge sessions
419. VL-20-419 | DROP -> DROP | REPRESENTED same-dest | C16: "brief never names source.md" is CODE-VERIFIED (run-reviewer.sh:13-17 has no source.m
420. VL-20-420 | CORE -> CORE | REPRESENTED same-dest | C17: run-reviewer.sh:17 and rules file :60 both state "anchor = 12 to 200 chars copied exa
421. VL-20-421 | KNOWLEDGE -> KNOWLEDGE | REPRESENTED same-dest | Not checked against code by the slice: claude -p behaviours (variadic --disallowedTools), 
422. VL-20-422 | DROP -> DROP | REPRESENTED same-dest | Decision D1: raw gateway model ids via Bash claude -p --model, not tier aliases (manifest.
423. VL-20-423 | DROP -> DROP | REPRESENTED same-dest | Decision D2: reviewer sandbox = git archive of HEAD without .dev/tasks/done, .dev/eval-wor
424. VL-20-424 | DROP -> DROP | REPRESENTED same-dest | Decision D3: fixed decision rule set BEFORE scoring (PILOT-REPORT:56), applied and superse
425. VL-20-425 | DROP -> DROP | REPRESENTED same-dest | Decision D4: Qwen3.8-max disqualified for 3000 s timeouts (PILOT:12), in force
426. VL-20-426 | DROP -> DROP | REPRESENTED same-dest | Decision D5: glm-5.3 excluded for delays and outages (SPEC.md:98, run-reviewer.sh:69), in 
427. VL-20-427 | DROP -> DROP | REPRESENTED same-dest | Decision D6: pre-source.md luna data quarantined, only -src luna may be cited (COMBO-REPOR
428. VL-20-428 | DROP -> DROP | REPRESENTED same-dest | Decision D7: muse-wonder replaced by muse-ember-1.0 (Tier 04 Model 02) because wonder hit 
429. VL-20-429 | DROP -> DROP | REPRESENTED same-dest | Decision D8: fallback ladder v2 to v3 (tier-ordered, never revisit, EXCLUDE_MODELS, NOFALL
430. VL-20-430 | DROP -> DROP | REPRESENTED same-dest | Decision D9: batch 10 dropped and testing closed ("we're done testing, we're going to deci
431. VL-20-431 | EVAL -> EVAL | REPRESENTED same-dest | Decision D10: six read-only audits A-F of all valid-era runs (COMBO-REPORT:290), done
432. VL-20-432 | DROP -> DROP | REPRESENTED same-dest | Decision D11: final guidance default ember + 2x luna, optional quality tier sonnet + 2x lu
433. VL-20-433 | DROP -> DROP | REPRESENTED same-dest | Decision D12: concurrency caps (12 workers identity bleed, 10 concurrent with muse capped 
434. VL-20-434 | DROP -> DROP | REPRESENTED same-dest | Decision D13: judge = claude-opus-5-5 single pass per (combo, package) on the anonymised m
435. VL-20-435 | DROP -> DROP | REPRESENTED same-dest | Open O1: harness fixes (anchor limit, source.md in brief, ladder fix and identity audit) a
436. VL-20-436 | MODULE-tasklist -> MODULE-tasklist | REPRESENTED same-dest | Open O2: which of ember+2luna, sonnet+2luna, haiku+2luna to standardise; guidance given bu
437. VL-20-437 | DROP -> DROP | REPRESENTED same-dest | Open O3: remaining 6 packages staged (PILOT-REPORT:83) never ran in A1 (UNVERIFIED in the 
438. VL-20-438 | EVAL -> EVAL | REPRESENTED same-dest | Open O4: five GT defects never caught: designSpec GT1, GT2, GT10, alias GT4 (plus alias GT
439. VL-20-439 | DROP -> DROP | REPRESENTED same-dest | Open O5: whether an explicit source.md path in the brief lifts ember and luna (inference o
440. VL-20-440 | DROP -> DROP | REPRESENTED same-dest | Open O6: replicate r2-sonnet-src (haiku x2 + grok + sonnet) 4 reps was untried candidate #
441. VL-20-441 | EVAL -> EVAL | REPRESENTED same-dest | Open O7: arm A (sonnet alone) re-baseline with source.md (combo-est-self.md:23) was never 
442. VL-20-442 | DROP -> DROP | REPRESENTED same-dest | Open O8: judge variance for the pilot arms A/B/C (PILOT:76)
443. VL-20-443 | DROP -> DROP | REPRESENTED same-dest | Product defect P1: merge drops invalid finding LINES (anchor over 200, anchor2 over 200, c
444. VL-20-444 | DROP -> DROP | REPRESENTED same-dest | Product defect P2: the warning gives only the first error per reviewer, dropped ids are no
445. VL-20-445 | DROP -> DROP | REPRESENTED same-dest | Product defect P3: transitive clustering (union-find within 3 lines when refs intersect or
446. VL-20-446 | DROP -> DROP | REPRESENTED same-dest | Product defect P4: anchors not in the candidate are kept with null span (46 rows, 13 block
447. VL-20-447 | DROP -> DROP | REPRESENTED same-dest | Product defect P5: superclaude review merge is not re-runnable for a round (existing ledge
448. VL-20-448 | DROP -> DROP | REPRESENTED same-dest | Product defect P6: merge refuses only when NO reviewer has a valid block, so a 7-reviewer 
449. VL-20-449 | DROP -> DROP | REPRESENTED same-dest | Product defect P7: the gateway environment has no dispatch mechanism for any model beyond 
450. VL-20-450 | DROP -> DROP | REPRESENTED same-dest | Product defect P8: product tier3 = [glm-5.3, Qwen3.8-max] (both excluded by owner order in
451. VL-20-451 | CORE -> DROP | REPRESENTED dedup->DR-080 | Product defect P9: two vocabularies GT class vs findings category, and the reflect categor
452. VL-20-452 | DROP -> DROP | REPRESENTED same-dest | Product defect P10: findings.py limits (200/300) are shared by findings-v2 (E1) through th
453. VL-20-453 | DROP -> DROP | REPRESENTED same-dest | Harness defect H1: variadic --disallowedTools swallowed the positional prompt, every launc
454. VL-20-454 | DROP -> DROP | REPRESENTED same-dest | Harness defect H2: brief category typo unpassable-ac; fixed 2026-11-11 after c1 reported; 
455. VL-20-455 | DROP -> DROP | REPRESENTED same-dest | Harness defect H3: source.md not shipped (terra/sol incomplete, luna 25/25 empty); fixed 1
456. VL-20-456 | DROP -> DROP | REPRESENTED same-dest | Harness defect H4: expected_model overwritten by fallback so model_ok passes after a silen
457. VL-20-457 | DROP -> DROP | REPRESENTED same-dest | Harness defect H5: claude binary replaced or missing mid-run (exit 127 "native binary not 
458. VL-20-458 | DROP -> DROP | REPRESENTED same-dest | Harness defect H6: gateway identity bleed under load (muse-wonder-1.0 served as gpt-6.1-te
459. VL-20-459 | DROP -> DROP | REPRESENTED same-dest | Harness defect H7: blocking-count parser grep "blocking":true without a space undercounted
460. VL-20-460 | DROP -> DROP | REPRESENTED same-dest | Harness defect H8: judge API error left a plausible score.json (8 rows, 6 blocking, 8-of-1
461. VL-20-461 | DROP -> DROP | REPRESENTED same-dest | Harness defect H9: judge "blocking" ignores blocking_in_implement (65 judge vs 38 real ove
462. VL-20-462 | DROP -> DROP | REPRESENTED same-dest | Harness defect H10: attrib.py credited every reviewer on a merged row; doubling conclusion
463. VL-20-463 | DROP -> DROP | REPRESENTED same-dest | Harness defect H11: stale merges because merge scripts skip when merged-1.md exists (merge
464. VL-20-464 | DROP -> DROP | REPRESENTED same-dest | Harness defect H12: row naming hides composition (r2 treated as a muse row); valid-era cho
465. VL-20-465 | DROP -> DROP | REPRESENTED same-dest | Harness defect H13: cost.json over-counts 5 runs (stale attempt2 leftovers) and counts the
466. VL-20-466 | DROP -> DROP | REPRESENTED same-dest | Harness defect H14: BLOCK_OK is a fence-presence grep only (run-reviewer.sh:57); a block w
467. VL-20-467 | DROP -> DROP | REPRESENTED same-dest | Harness defect H15: hard-coded absolute paths (E2 worktree, /tmp/evalsb, /tmp/*.tsv) and s
468. VL-20-468 | DROP -> DROP | REPRESENTED same-dest | Harness defect H16: reviewer brief states the anchor limit but not the 300-char claim cap 
469. VL-20-469 | DROP -> DROP | REPRESENTED same-dest | Harness defect H17: reviewer isolation relies on snapshot content; bypassPermissions + Bas
470. VL-20-470 | EVAL -> EVAL | REPRESENTED same-dest | Harness defect H18: pilot arms use a random-drawn composition per package (arm B designSpe
471. VL-20-471 | DROP -> DROP | FLAG ORIG-REASON-NOT-CONTAINED | same-dest | Harness defect H19: README lists checks-gate8 as a key script but the file is absent from 
472. VL-20-472 | EVAL -> EVAL | REPRESENTED same-dest | terra and sol returned "incomplete" reports even after source.md shipped (51 incomplete, 1
473. VL-20-473 | DROP -> DROP | REPRESENTED same-dest | luna: thin (30-295 s, 1.4k-14k tokens pre-src; 4.7k average src era), anchor fidelity 91.4
474. VL-20-474 | DROP -> DROP | REPRESENTED same-dest | ember: 81 of 209 runs (39%) never referenced source.md; 33 findings dropped at merge
475. VL-20-475 | DROP -> DROP | REPRESENTED same-dest | wonder: 14 findings dropped at merge; exhausted its weekly limit
476. VL-20-476 | EVAL -> EVAL | REPRESENTED same-dest | haiku: workhorse, 1085 of 1108 findings kept; noisy at 8.3-8.6 findings/run
477. VL-20-477 | EVAL -> EVAL | REPRESENTED same-dest | grok: slow (600-980 s, 845 s average wall), about 54k tokens/run, the only source of desig
478. VL-20-478 | EVAL -> EVAL | REPRESENTED same-dest | sonnet: highest coverage per run, rarely marks blocking (0.26-0.28 claims/run), 0 findings
479. VL-20-479 | DROP -> DROP | REPRESENTED same-dest | glm-5.3: slow (805-1435 s), mixed glm-5.3 and qwen3.8-max observed in 7 attempt1s; exclude
480. VL-20-480 | DROP -> DROP | REPRESENTED same-dest | Qwen3.8-max: 0 output tokens, 3000 s timeouts in the pilot; excluded
481. VL-20-481 | DROP -> DROP | REPRESENTED same-dest | E2 and E1 reviewed the same designSpec plan (candidate.md sha256 044809e3..., 200 lines; E
482. VL-20-482 | DROP -> DROP | REPRESENTED same-dest | E2 source.md copied from .dev/tasks/done/<pkg>/source.md equals E1's input source.md (sha2
483. VL-20-483 | EVAL -> EVAL | REPRESENTED same-dest | E1 combos.json input.ground_truth points at git show b4db265a8:.../ground-truth.json (sha2
484. VL-20-484 | EVAL -> EVAL | REPRESENTED same-dest | Run volumes: E2 890 reviewer runs in 70 rows (audit-A:3) plus pilot arms on 3 packages; E1
485. VL-20-485 | DROP -> DROP | REPRESENTED same-dest | Dispatch: E2 raw ids via claude -p --model in a sandbox repo; E1 /sc:reflect --mode pre pi
486. VL-20-486 | DROP -> DROP | REPRESENTED same-dest | Findings schema: E2 findings-v1 via /sc:spec-panel brief; E1 findings-v2 container reusing
487. VL-20-487 | CORE -> CORE | REPRESENTED same-dest | Verdict logic differs: E2 superclaude review merge ledger (ledger.py), E1 reflect kernel (
488. VL-20-488 | CORE -> CORE | REPRESENTED same-dest | Common failure class in E1 and E2: brief lacks heading or limits so the reviewer block is 
489. VL-20-489 | EVAL -> EVAL | REPRESENTED same-dest | A1 is byte-identical at run-1 commit 4a22d74 and tip 6c09843 (git diff --stat empty, 9,312
490. VL-20-490 | EVAL -> EVAL | REPRESENTED same-dest | git merge-base HEAD 6c09843 = ec259f1b7 (= origin/master sha in manifest.md:6): both effor
491. VL-20-491 | EVAL -> EVAL | REPRESENTED same-dest | b4db265a8 is the first E2 push ("docs(eval): tasklist review panel model-combination study
492. VL-20-492 | HARNESS -> HARNESS | REPRESENTED same-dest | E1 combos.json carries "status":"designed, not run" although results.jsonl holds 15 publis
493. VL-20-493 | CORE -> CORE | REPRESENTED same-dest | Lesson L1: a panel's result is dominated by input delivery, not model choice (missing sour
494. VL-20-494 | DROP -> DROP | REPRESENTED same-dest | Lesson L2: verify "model ran" by the OBSERVED assistant model, not init, billing or alias;
495. VL-20-495 | CORE -> CORE | REPRESENTED same-dest | Lesson L3: a fallback ladder needs a visited set, an exclude list and a no-fallback switch
496. VL-20-496 | CORE -> CORE | REPRESENTED same-dest | Lesson L4: silent normalisation hides data loss; the merged report must show per-reviewer 
497. VL-20-497 | CORE -> CORE | REPRESENTED same-dest | Lesson L5: treat reviewer findings limits as a contract the reviewer is told AND the parse
498. VL-20-498 | DROP -> DROP | REPRESENTED same-dest | Lesson L6: single-run rows are noise (same nominal panel 4/14 then 2/14, judge corrupted o
499. VL-20-499 | DROP -> DROP | REPRESENTED same-dest | Lesson L7: never read a metric's definition from a column name: judge "blocking" is not bl
500. VL-20-500 | DROP -> DROP | REPRESENTED same-dest | Lesson L8: mechanical checks (parser, attribution, count regex) need independent re-deriva
501. VL-20-501 | KNOWLEDGE -> KNOWLEDGE | REPRESENTED same-dest | Lesson L9: publish retractions in place with a supersedes pointer; COMBO-REPORT has 4 head
502. VL-20-502 | DROP -> DROP | REPRESENTED same-dest | Lesson L10: a judge mid-run failure may leave a plausible output; validate completion mark
503. VL-20-503 | CORE -> CORE | REPRESENTED same-dest | Lesson L11: quarantine, never delete (*-contaminated-20261111, quarantine-*, *.invalid-api
504. VL-20-504 | DROP -> DROP | REPRESENTED same-dest | Lesson L12: read composition from meta.json, not row names (r2 mislabelled as muse)
505. VL-20-505 | DROP -> DROP | REPRESENTED same-dest | Lesson L13: concurrency: 8 parallel verified in probe (max_parallel_tested), 12 workers br
506. VL-20-506 | MODULE-tasklist -> MODULE-tasklist | REPRESENTED same-dest | Lesson L14: cheap reviewers (luna, terra, sol, ember) are noisy blockers (3-4 wrong blocke
507. VL-20-507 | DROP -> DROP | REPRESENTED same-dest | Lesson L15: second same-model reviewer: only supported effect is luna x2 raising control G
508. VL-20-508 | DROP -> DROP | REPRESENTED same-dest | Lesson L16: defects no model reached (B1, B2, I5, I6; B6 once) point at the brief, package
509. VL-20-509 | DROP -> DROP | REPRESENTED same-dest | Lesson L17: the strongest pilot signal was negative: single arm A PASSED both defect-rich 
510. VL-20-510 | EVAL -> EVAL | REPRESENTED same-dest | Lesson L18: row-name-based filters ("valid-era") are fragile; keep an explicit manifest of
511. VL-20-511 | DROP -> DROP | REPRESENTED same-dest | Lesson L19: owner ordered unusual constraints mid-study (exclude glm and Qwen, no Fable/Ti
512. VL-20-512 | CORE -> CORE | REPRESENTED same-dest | Lesson L20: panel wall time is the slowest reviewer (grok 600-980 s, glm 805-1435 s), toke
513. VL-20-513 | DROP -> DROP | REPRESENTED same-dest | Not shown 1: anything about the product superclaude review panel as shipped; all panels we
514. VL-20-514 | EVAL -> EVAL | REPRESENTED same-dest | Not shown 2: any result for more than 3 packages, any held-out package, any package type o
515. VL-20-515 | EVAL -> EVAL | REPRESENTED same-dest | Not shown 3: real gate accuracy; GT = defects observed in past implement runs by one obser
516. VL-20-516 | DROP -> DROP | REPRESENTED same-dest | Not shown 4: cost in money (only reviewer output tokens and wall; input, cache and per-com
517. VL-20-517 | DROP -> DROP | REPRESENTED same-dest | Not shown 5: effect of the harness fixes (source.md named in brief, anchor truncation) on 
518. VL-20-518 | DROP -> DROP | REPRESENTED same-dest | Not shown 6: sonnet alone with source.md (arm A re-baseline) is unrun, so "no panel beats 
519. VL-20-519 | EVAL -> EVAL | REPRESENTED same-dest | Not shown 7: no inter-judge agreement; one judge model (claude-opus-5-5) for all rows; rel
520. VL-20-520 | DROP -> DROP | REPRESENTED same-dest | Not shown 8: whether panel PASS/FAIL agrees with the implement outcome beyond qualitative 
521. VL-20-521 | DROP -> DROP | REPRESENTED same-dest | Not shown 9: statistical power: 4-6 replicates per replicated panel, most rows n=1; after 
522. VL-20-522 | EVAL -> EVAL | REPRESENTED same-dest | Not shown 10: re-review rounds (round 2/3), reviser loop and ledger convergence: every led
523. VL-20-523 | DROP -> DROP | REPRESENTED same-dest | Not shown 11: adversarial/debate merge vs ledger merge not compared (E1 uses adversarial M
524. VL-20-524 | EVAL -> EVAL | REPRESENTED same-dest | Not shown 12: reflect-style deviation findings (E1 UC-2 taxonomy) and findings-v2 channels
525. VL-20-525 | DROP -> DROP | REPRESENTED same-dest | Not shown 13: whether reviewers could write to disk or use the web: audit-A shows WebFetch
526. VL-20-526 | EVAL -> EVAL | REPRESENTED same-dest | Not shown 14: order and seed effects of random tier draws in product templates; resolution
527. VL-20-527 | DROP -> DROP | REPRESENTED same-dest | V1: source-input omission explains terra/sol/luna "incomplete"; with source.md panels are 
528. VL-20-528 | DROP -> DROP | REPRESENTED same-dest | V2: 156 of 665 valid-era runs never referenced source.md (ember 81/209, luna 49/222, wonde
529. VL-20-529 | DROP -> DROP | REPRESENTED same-dest | V3: 92 dropped findings (anchor over 200 56, anchor2 over 200 18, claim over 300 14, sever
530. VL-20-530 | DROP -> DROP | REPRESENTED same-dest | V4: 83 megacluster rows; 195 of 1398 chain rows
531. VL-20-531 | DROP -> DROP | REPRESENTED same-dest | V5: 46 rows with null span, 13 blocking
532. VL-20-532 | DROP -> DROP | REPRESENTED same-dest | V6: real blocking 38 of 65 judge-blocking over 71 rows
533. VL-20-533 | DROP -> DROP | REPRESENTED same-dest | V7: final panel guidance (default ember+2luna 64k tokens 1.83/14 0.17 real blocking contro
534. VL-20-534 | DROP -> DROP | REPRESENTED same-dest | V8: statistics surviving audit: luna x2 control +0.83; 2luna+2ember more wrong blockers; e
535. VL-20-535 | DROP -> DROP | REPRESENTED same-dest | V9: ceiling and reach: B1, B2, I5, I6 never caught in 106 runs; B3 95, I8 76, I2 71 of 106
536. VL-20-536 | DROP -> DROP | REPRESENTED same-dest | V10: pilot arms A/B/C 2/16, 3/16, 4/16 with 0/8 blocking recall; A passed both defect-rich
537. VL-20-537 | DROP -> DROP | REPRESENTED same-dest | V11: efficiency table (catches/100k) and ranking tables of batches 1-3, 4/5, 6, 7
538. VL-20-538 | DROP -> DROP | REPRESENTED same-dest | V12: per-model profile (tokens/run, findings/run, blocking claims/run) (combo-est-self:3-1
539. VL-20-539 | DROP -> DROP | REPRESENTED same-dest | V13: per-model identity risks (muse served as terra, glm as qwen, wonder/spark/wonder-full
540. VL-20-540 | DROP -> DROP | REPRESENTED same-dest | V14: gateway concurrency limits (8 tested, 12 broke, 10 with muse cap 4)
541. VL-20-541 | DROP -> DROP | REPRESENTED same-dest | V15: Qwen3.8-max 3000 s timeouts with 0 tokens, glm 805-1435 s, grok 600-980 s
542. VL-20-542 | DROP -> DROP | REPRESENTED same-dest | V16: terra/sol "incomplete" even with source (51 reports, 16 empty terra [CODE-CONTRADICTE
543. VL-20-543 | DROP -> DROP | REPRESENTED same-dest | V17: judge process (blind Opus, anonymised, label key, API-error audit, 12-row re-judge 12
544. VL-20-544 | DROP -> DROP | REPRESENTED same-dest | V18: fixed decision rule written before scoring (PILOT:56)
545. VL-20-545 | EVAL -> EVAL | REPRESENTED same-dest | V19: statistical conventions used (permutation, Welch, Fisher; "beyond noise" flagged; ran
546. VL-20-546 | DROP -> DROP | REPRESENTED same-dest | V20: control package GT2 per-reviewer hit rates (grok 7/8 ... ember 4/13), a keyword proxy
547. VL-20-547 | CORE -> CORE | REPRESENTED same-dest | T1: re-implement tools/run-reviewer.sh in product Python code keeping its contract (expect
548. VL-20-548 | DROP -> DROP | REPRESENTED same-dest | T2: the brief text in run-reviewer.sh:13-17 should have the rules file (document_review_lo
549. VL-20-549 | DROP -> DROP | REPRESENTED same-dest | T3: run-reviewer.sh.bad-launch and .unpassable-ac kept as evidence of H1 and H2
550. VL-20-550 | EVAL -> EVAL | REPRESENTED same-dest | T4: keep the judge and anonymiser design (blind label, anonymise ids, paths and model name
551. VL-20-551 | DROP -> DROP | REPRESENTED same-dest | T5: merge-b6.sh and merge-b7..b11.sh (hand-built resolution, review merge, stale-r1 retry)
552. VL-20-552 | CORE -> CORE | REPRESENTED same-dest | T6: keep the concepts of the per-row cancel sentinel (b4-job-one.sh) and xargs -P concurre
553. VL-20-553 | DROP -> DROP | REPRESENTED same-dest | T7: keep final-table.py logic (real vs judge blocking, exclude flags); drop attrib.py and 
554. VL-20-554 | CORE -> CORE | REPRESENTED same-dest | T8: make audits A (identity), C (input referenced) and D (merge integrity) runtime or CI c
555. VL-20-555 | DROP -> DROP | REPRESENTED same-dest | T9: analysis/issue-table and analysis/allsets agent-built tables with an independent scrip
556. VL-20-556 | DROP -> DROP | REPRESENTED same-dest | T10: combo-est-A/B/self.md untried-combo estimates are unverified predictions with no run
557. VL-20-557 | CORE -> CORE | REPRESENTED same-dest | T11: probe/probe.json (alias findings, 8 parallel, sandbox_write): adopt a zero-load assis
558. VL-20-558 | CORE -> CORE | REPRESENTED same-dest | T12: snap.py and drift-b3.py hash the input tree (input_tree_sha256), a pattern shared wit
559. VL-20-559 | EVAL -> EVAL | REPRESENTED same-dest | T13: GT files (ground-truth.json x3, ground-truth-draft.json, verification block quote_gre
560. VL-20-560 | DROP -> DROP | REPRESENTED same-dest | T14: resolution-default.json and resolution-live7.json per package (schema review-panel-re
561. VL-20-561 | EVAL -> EVAL | REPRESENTED same-dest | T15: combos/<row>/{ledger.json, merged-1.md, resolution.json, merge-stdout.txt} x 95 rows;
562. VL-20-562 | EVAL -> EVAL | REPRESENTED same-dest | T16: reviews/combos reviewer reports (*.md), meta.json and cost.json (1,263 each), a sampl
563. VL-20-563 | EVAL -> EVAL | REPRESENTED same-dest | T17: quarantine-pre-src-luna (417 files), *-contaminated-20261111 (592 paths), *-supersede
564. VL-20-564 | CORE -> CORE | REPRESENTED same-dest | T18: RAW-TRANSCRIPTS-NOT-COMMITTED.md (1.48 GB, 2,916 files off-repo); policy: transcripts
565. VL-20-565 | KNOWLEDGE -> KNOWLEDGE | REPRESENTED same-dest | T19: COMBO-REPORT.md, PILOT-REPORT.md, manifest.md and combos/SPEC.md are archive; extract
566. VL-20-566 | CORE -> CORE | REPRESENTED same-dest | X1: tests/review/test_review_findings.py:113,117 pin that anchor 201 chars and claim 301 c
567. VL-20-567 | CORE -> CORE | REPRESENTED same-dest | X2: tests/review/test_review_findings_v2.py:199-200,241 pin v2 anchor 200/201 and claim 30
568. VL-20-568 | CORE -> CORE | REPRESENTED same-dest | X3: tests/review/test_review_ledger.py:364-373 pin that the merge is refused when no revie
569. VL-20-569 | CORE -> CORE | REPRESENTED same-dest | X4: tests/review/test_review_ledger.py:376-385 test_one_valid_block_is_enough_and_the_inva
570. VL-20-570 | CORE -> CORE | REPRESENTED same-dest | X5: tests/review/test_review_ledger.py:388-393 pin that a round cannot be merged twice or 
571. VL-20-571 | MODULE-tasklist -> CORE | REPRESENTED moved(documented) | X6: tests/review/test_review_panel_live7.py, test_review_panel.py, test_review_panel_exclu
572. VL-20-572 | CORE -> CORE | REPRESENTED same-dest | X7: tests/review/test_review_rules_text.py:67-68 pin the rules prompt wording of the findi
573. VL-20-573 | MODULE-reflect -> MODULE-reflect | REPRESENTED same-dest | X8: tests/review/test_review_card_convert.py:426 pins the reflect category map acceptance 
574. VL-20-574 | CORE -> CORE | REPRESENTED same-dest | Missing test: no test pins the dropped-finding report content
575. VL-20-575 | CORE -> CORE | REPRESENTED same-dest | Missing test: no test pins the model-identity gate
576. VL-20-576 | CORE -> CORE | REPRESENTED same-dest | Missing test: no test pins the fallback visited set
577. VL-20-577 | CORE -> CORE | REPRESENTED same-dest | Missing test: no test pins input-manifest presence
578. VL-20-578 | EVAL -> EVAL | REPRESENTED same-dest | Missing test: no test pins judge completion
579. VL-20-579 | MODULE-reflect -> MODULE-reflect | REPRESENTED same-dest | Use case sc:reflect (UC-1/UC-2 Tier 2): findings-v2 reuses the 200/300 limits so silent dr
580. VL-20-580 | MODULE-tasklist -> MODULE-tasklist | REPRESENTED same-dest | Use case sc:workflow tasklist review: source.md must be shipped and named; first-round onl
581. VL-20-581 | MODULE-spec -> MODULE-spec | REPRESENTED same-dest | Use case spec review: the E2 brief starts with /sc:spec-panel @<cand> --mode critique so r
582. VL-20-582 | MODULE-pr-review -> MODULE-pr-review | REPRESENTED same-dest | Use case PR code review (later): diff anchors may exceed 200 chars (luna/ember/wonder lost
583. VL-20-583 | MODULE-rfqa -> MODULE-rfqa | REPRESENTED same-dest | Use case rf-qa replacement: agent-built tables plus an independent script cross-check (0 m
584. VL-20-584 | HARNESS -> HARNESS | REPRESENTED same-dest | Use case model-combination experiments (E1 follow-ups): harness defects H1-H19 will recur,
585. VL-20-585 | CORE -> CORE | REPRESENTED same-dest | Cost governance: reviewer tokens only; ember+luna 52k tokens vs sonnet+ember 143k vs r2 59
586. VL-20-586 | CORE -> CORE | REPRESENTED same-dest | Security and isolation: bypassPermissions + Bash + WebFetch in reviewers, sandbox = archiv
587. VL-20-587 | EVAL -> EVAL | REPRESENTED same-dest | Evaluation governance: pre-registered decision rule, blind labels, replicates of at least 
588. VL-20-588 | DROP -> DROP | REPRESENTED same-dest | Slice summary 1 (scope read): reports, SPEC, tools (3 harness files + 55 tmp-scripts), ana
589. VL-20-589 | DROP -> DROP | REPRESENTED same-dest | Slice summary 2 (study design): 3 packages, 16 GT defects (8 blocking), 106 scored runs in
590. VL-20-590 | DROP -> DROP | REPRESENTED same-dest | Slice summary 3 (headline): all panels at about 2-2.5 of 14, real blocking recall 0.17-1.2
591. VL-20-591 | DROP -> DROP | REPRESENTED same-dest | Slice summary 4 (biggest finding): input delivery and parse contract dominated model choic
592. VL-20-592 | DROP -> DROP | REPRESENTED same-dest | Slice summary 5 (code cross-check, 17 items): unpassable-ac was a harness typo; silent dro
593. VL-20-593 | DROP -> DROP | REPRESENTED same-dest | Slice summary 6 (cross-effort): E1 and E2 reviewed the byte-identical designSpec plan with
594. VL-20-594 | DROP -> DROP | REPRESENTED same-dest | Slice summary 7: pilot table recomputed from score.json, 9/9 cells match; COMBO-REPORT mas
595. VL-20-595 | DROP -> DROP | REPRESENTED same-dest | Slice summary 8 (counts): 17 code claims, 13 decisions, 8 open, 10 product-code defects, 1
596. VL-20-596 | DROP -> DROP | REPRESENTED same-dest | Slice gap 1: audits B, C, E, F headline numbers UNVERIFIED (only A and D have summary.md)
597. VL-20-597 | EVAL -> EVAL | REPRESENTED same-dest | Slice gap 2: COMBO-REPORT master tables (:17-43, :114-130, :303-337, :388-399, :433-498) n
598. VL-20-598 | DROP -> DROP | REPRESENTED same-dest | Slice gap 3: whether muse-ember-1.0 exists in the product tiers file after HEAD is UNVERIF
599. VL-20-599 | DROP -> DROP | REPRESENTED same-dest | Slice gap 4: which Qwen count is right (4 reviewer ids vs 3 slots vs 3 of 4 runs)
600. VL-20-600 | DROP -> DROP | REPRESENTED same-dest | Slice gap 5: quarantine counts differ (428 reviewer files and 10 merge sets vs 428 plus 9 
601. VL-20-601 | DROP -> DROP | REPRESENTED same-dest | Slice gap 6: verdict flip count 3 enumerated (audit-D:20) vs "Four" (COMBO-REPORT:292)
602. VL-20-602 | DROP -> DROP | REPRESENTED same-dest | Slice gap 7: whether the 54 of 319 merged-anon.md files naming model ids leak reviewer ide
603. VL-20-603 | DROP -> DROP | REPRESENTED same-dest | Slice gap 8: tmp-scripts/checks-gate8 named in README but absent from the 55-file list
604. VL-20-604 | DROP -> DROP | REPRESENTED same-dest | Slice gap 9: E1 dispatch internals (combos.json common.prompt truncated) not read in slice
605. VL-20-605 | DROP -> DROP | REPRESENTED same-dest | Slice gap 10: a grep scope slip by the slice author printed file names under a forbidden r
606. VL-20-606 | DROP -> DROP | REPRESENTED same-dest | Slice gap 11: not read per task: raw transcripts, 29 per-combo RESULT.md, per-reviewer rep
607. VL-20-607 | CORE -> CORE | REPRESENTED same-dest | Q1: should the core keep the product limits (anchor at most 200, anchor2 at most 200, clai
608. VL-20-608 | CORE -> CORE | REPRESENTED same-dest | Q2: is block_ok false + kept findings + "one valid block is enough" (pinned by test_review
609. VL-20-609 | CORE -> CORE | REPRESENTED same-dest | Q3: which dispatch mechanism will the gateway environment use for non-first-slot models (r
610. VL-20-610 | MODULE-tasklist -> CORE | REPRESENTED moved(documented) | Q4: are glm-5.3 and Qwen3.8-max permanently excluded for panels (D4/D5), given product tie
611. VL-20-611 | DROP -> DROP | REPRESENTED same-dest | Q5: should the arm-A (sonnet alone, with source.md) baseline be re-run before any panel is
612. VL-20-612 | EVAL -> EVAL | REPRESENTED same-dest | Q6: is E2's GT (16 defects from past implement runs, one observer) accepted as the shared 
613. VL-20-613 | CORE -> CORE | REPRESENTED same-dest | Q7: should the brief name every shipped input and the harness verify the reviewer opened i
614. VL-20-614 | HARNESS -> HARNESS | REPRESENTED same-dest | Q8: do the E2 harness files (run-reviewer.sh, judge/anon scripts, audits A, C, D) become p
615. VL-20-615 | DROP -> DROP | REPRESENTED same-dest | Q9: the wording "discarded with no error" (COMBO-REPORT:292) is [CODE-CONTRADICTED]: corre
616. VL-20-616 | DROP -> DROP | REPRESENTED same-dest | 1.1 Run folder top level: COMBO-REPORT.md, PILOT-REPORT.md, manifest.md, 3 package dirs, a
617. VL-20-617 | DROP -> DROP | REPRESENTED same-dest | 1.2 Raw transcripts (about 1.48 GB, 2,916 files) are not committed
618. VL-20-618 | DROP -> DROP | REPRESENTED same-dest | 1.3 Committed derived set: reviewer reports, meta/cost.json, merge outputs, blind scores, 
619. VL-20-619 | DROP -> DROP | REPRESENTED same-dest | 1.4 Entry pointer: start with COMBO-REPORT.md section FINAL RESULTS AND DECISION (2026-11-
620. VL-20-620 | EVAL -> EVAL | REPRESENTED same-dest | 1.5 Audit A "jq on the final attempt's raw JSON" and the judge-session checks cannot be re
621. VL-20-621 | DROP -> DROP | REPRESENTED same-dest | 1.6 Ground-truth files ground-truth.json and ground-truth-draft.json for DS, AL, DE (6 fil
622. VL-20-622 | EVAL -> EVAL | REPRESENTED same-dest | 1.7 Score files: 9 base-arm score.json (arms/scoring/<pkg>/{X,Y,Z}) + 309 combo score.json
623. VL-20-623 | EVAL -> EVAL | REPRESENTED same-dest | 1.7a Scored combo rows (b4-*, c1-c5, e1-e6, g1..g9 x r1-r4 = 36 rows, h1/h2 x r1-r4 = 8, j
624. VL-20-624 | EVAL -> EVAL | REPRESENTED same-dest | 1.7b combos/ has 97 entries = 96 row dirs + SPEC.md; 3 named contaminated or superseded (n
625. VL-20-625 | EVAL -> EVAL | REPRESENTED same-dest | Combo row directory count: slice 03 says 95 row dirs + SPEC.md (03:22), slice 04 says 96 r
626. VL-20-626 | DROP -> DROP | REPRESENTED same-dest | 1.8 Score JSON keys used by the scripts: gt_covered_any (list), gt_covered_blocking (list)
627. VL-20-627 | DROP -> DROP | REPRESENTED same-dest | 1.9 DEFECT hard-coded environment paths: final-table.py L7, attrib.py L4, untried.py L3 re
628. VL-20-628 | DROP -> DROP | REPRESENTED same-dest | 1.10 Analysis top-level files (attrib.{py,out,json}, doubles, untried, gt2-hits.txt, final
629. VL-20-629 | EVAL -> EVAL | REPRESENTED same-dest | 1.11 Reproducibility test by slice 04: git archive of RUN to /tmp, final-table.py and thre
630. VL-20-630 | DROP -> DROP | REPRESENTED same-dest | 2.1 GT schema: keys package, items, dropped, verification; item keys id, class, plan_quote
631. VL-20-631 | DROP -> DROP | REPRESENTED same-dest | 2.2 GT sizes: DS 10 items (GT1-GT5 blocking), AL 4 items (GT1-GT3 blocking), DE 2 items (0
632. VL-20-632 | DROP -> DROP | REPRESENTED same-dest | 2.3 GT provenance: defects that showed up while the plan was implemented (cites T2/notes.m
633. VL-20-633 | DROP -> DROP | REPRESENTED same-dest | 2.4 GT legend labels B1-B8, I1-I8 (issue-legend.tsv L2-L17)
634. VL-20-634 | EVAL -> EVAL | REPRESENTED same-dest | 2.5 Score JSON keys label, combo, package, gt_total, gt_covered_any, gt_covered_blocking, 
635. VL-20-635 | EVAL -> EVAL | REPRESENTED same-dest | 2.6 Blind judge reads merged-anon.md (ledger table with reviewer and model names stripped,
636. VL-20-636 | DROP -> DROP | REPRESENTED same-dest | 2.7 Judge semantics flaw: 26 x 1-blocking-semantics flags (audit-F flags L15-L40); judge c
637. VL-20-637 | CORE -> CORE | REPRESENTED same-dest | 2.8 Blocking-flag recall (DERIVED by slice 04): 89 real-blocking GT catches by any ledger 
638. VL-20-638 | EVAL -> EVAL | REPRESENTED same-dest | 2.9 GT catch distribution over 71 valid-era rows: DS GT3 63, GT7 50, GT4 3, GT5 3, GT6 3, 
639. VL-20-639 | EVAL -> EVAL | REPRESENTED same-dest | 2.10 ALL-src (76 runs) catches: B3 68, B4 3, B5 3, B6 1, B7 20, B8 1, I1 3, I2 52, I3 2, I
640. VL-20-640 | EVAL -> EVAL | REPRESENTED same-dest | 2.11 Pilot arms A/B/C mapped to labels by arm-key.json (allsets-setup.py L12-19); pilot ar
641. VL-20-641 | EVAL -> EVAL | REPRESENTED same-dest | 2.12 The fabricated n2-sonnet-src score: audit-E flags 1.labeldirs (n2-sonnet-src DS has 2
642. VL-20-642 | DROP -> DROP | REPRESENTED same-dest | 3.1 final-table.py (83 lines): FINAL table of valid-era rows grouped by reviewer-model mul
643. VL-20-643 | HARNESS -> DROP | REPRESENTED dedup->DR-091 | DEFECT in final-table.py: fullpkg() L15-18 (12-char prefix test) resolves the control pack
644. VL-20-644 | HARNESS -> DROP | REPRESENTED dedup->DR-091 | DEFECT in final-table.py: 11 further selected flags (3-dropped-blocking x4 with makeTheAli
645. VL-20-645 | HARNESS -> DROP | REPRESENTED dedup->DR-102 | final-table.py valid() L11-13 excludes j1, c*, n*, r* non-src rows, so batch-11 j1 replica
646. VL-20-646 | DROP -> DROP | REPRESENTED same-dest | final-table.py has a dead variable sd_any at L65
647. VL-20-647 | HARNESS -> HARNESS | REPRESENTED same-dest | final-table.py exclusion list BAD_CHECKS (L20) per slice 04: A all, B only 1-incomplete/1-
648. VL-20-648 | DROP -> DROP | REPRESENTED same-dest | 3.2 final-table.md (59 lines): header "valid-era rows: 71; row-packages scored: 213; row-p
649. VL-20-649 | DROP -> DROP | REPRESENTED same-dest | 3.3 final-all.json (9,540 B) and final-clean.json (5,641 B): per-panel stats dicts of the 
650. VL-20-650 | DROP -> DROP | REPRESENTED same-dest | 3.4 three-way.py (63 lines): per-run detail and permutation tests (20000 shuffles, seed 1)
651. VL-20-651 | HARNESS -> DROP | REPRESENTED dedup->DR-104 | DEFECT in three-way.py: prints "audit-flagged pkgs" as p[:8] = 'TASK-WF-' for every packag
652. VL-20-652 | EVAL -> EVAL | REPRESENTED same-dest | The three-way permutation test uses run-level sums over two packages with pseudo-replicati
653. VL-20-653 | DROP -> DROP | REPRESENTED same-dest | 3.5 attrib.py (78 lines) + attrib.out (78 lines) + attrib.json (14,471 B): per-model GT at
654. VL-20-654 | DROP -> DROP | REPRESENTED same-dest | 3.6 doubles.py / doubles.out (24 lines): inherits the attrib flaw; output luna panels=10 a
655. VL-20-655 | HARNESS -> HARNESS | REPRESENTED same-dest | 3.7 untried.py (46 lines) / untried.out (35 lines): per-model presence effect, top rows, u
656. VL-20-656 | EVAL -> EVAL | REPRESENTED same-dest | 3.8 gt2-hits.txt (15 lines): no script in the tree generates it, semantics UNVERIFIED (con
657. VL-20-657 | DROP -> DROP | REPRESENTED same-dest | 3.9 combo-est files disagree: sonnet blocking-claim rate "2 in 11 runs" (A L8) vs "0.28 cl
658. VL-20-658 | DROP -> DROP | REPRESENTED same-dest | 3.10 batch harness scripts b7..b11 launch/merge/judge/final files: reviewers launched with
659. VL-20-659 | HARNESS -> HARNESS | REPRESENTED same-dest | Merge scripts hard-code reviewer-id to model/tier/alias maps (merge-b8.sh L5-37) and rebui
660. VL-20-660 | EVAL -> EVAL | REPRESENTED same-dest | 3.11 b8-final.md (27 lines) and b9-final.md (17 lines): their "Blocking /8" column is the 
661. VL-20-661 | EVAL -> EVAL | REPRESENTED same-dest | 3.12 issue-table (10 issue-NN.json/tsv, legend, setup, compare, table, top10.json, direct 
662. VL-20-662 | EVAL -> EVAL | REPRESENTED same-dest | 3.13 allsets: 62 sets (S01-S62) by (era, model multiset), 106 runs, era src vs pre-src; va
663. VL-20-663 | DROP -> DROP | REPRESENTED same-dest | 3.14 RAW-TRANSCRIPTS-NOT-COMMITTED.md (4 lines)
664. VL-20-664 | HARNESS -> DROP | REPRESENTED dedup->DR-102 | 3.15 Six different valid-era predicates (final-table.py L11-13, untried.py L7-8, attrib.py
665. VL-20-665 | EVAL -> EVAL | REPRESENTED same-dest | 4.1 Population 71 valid-era rows, 213 row-packages (71 x 3), 69 excluded (32%); with the c
666. VL-20-666 | EVAL -> EVAL | REPRESENTED same-dest | 4.2 Replicated panels (>=4 runs) AS SCORED (found /14, real blocking /8, wrong blockers, t
667. VL-20-667 | DROP -> DROP | REPRESENTED same-dest | 4.3 Single-run leaders never replicated: grok+haiku+haiku+sonnet 4.00 found, 3.00 real blo
668. VL-20-668 | EVAL -> EVAL | REPRESENTED same-dest | 4.4 Efficiency outliers: terra alone 1.00 found at 7,241 tokens = 13.81 found per 100k; so
669. VL-20-669 | DROP -> DROP | REPRESENTED same-dest | 4.5 Ceiling: DR any per row max = 4; distribution [(0,3),(1,9),(2,43),(3,12),(4,4)]; 43/71
670. VL-20-670 | DROP -> DROP | REPRESENTED same-dest | 4.6 Model presence effect (found /14): sonnet n=21 2.43 vs n=50 1.92; haiku 2.26 (n=23) vs
671. VL-20-671 | DROP -> DROP | REPRESENTED same-dest | 4.7 Untried model sets from the pool sonnet, haiku, grok, luna, terra, sol, ember: 16 untr
672. VL-20-672 | DROP -> DROP | REPRESENTED same-dest | 4.8 Per-reviewer-run GT attribution (RETRACTED): ember 26 runs 0.65 GT/run, grok 16 runs 1
673. VL-20-673 | DROP -> DROP | REPRESENTED same-dest | 4.9 "Doubling gives nothing": luna panels=10 avg_single 0.25 avg_union 0.40 gain 0; ember 
674. VL-20-674 | EVAL -> EVAL | REPRESENTED same-dest | 4.10-4.13 Replicate families (DR found mean (sd), real blk, wrong blk, control found, toke
675. VL-20-675 | EVAL -> EVAL | REPRESENTED same-dest | Permutation p (two-sided, 20000 shuffles): sonnet+2x luna vs ember+2x luna found p=0.512, 
676. VL-20-676 | EVAL -> EVAL | REPRESENTED same-dest | Reviewer-level (dropped by merge / never referenced source.md): sonnet+2x luna: sonnet 18 
677. VL-20-677 | DROP -> DROP | REPRESENTED same-dest | Slice 04 reproduced the family numbers and COMBO-REPORT L428 verdict "NOT CONFIRMED" for s
678. VL-20-678 | DROP -> DROP | REPRESENTED same-dest | 4.14 ember+2x luna vs ember+luna, control found (n 6 vs 4): delta +0.83, Welch p 0.004, pe
679. VL-20-679 | DROP -> DROP | REPRESENTED same-dest | 4.15 2x luna+2x ember vs ember+luna, DR wrong blockers: +2.75, Welch 0.002, permutation 0.
680. VL-20-680 | DROP -> DROP | REPRESENTED same-dest | 4.16 2x luna+2x ember vs ember+2x luna, wrong blockers: +2.92, Welch 0.000, permutation 0.
681. VL-20-681 | DROP -> DROP | REPRESENTED same-dest | 4.17 2x luna+2x ember vs 2x ember+luna, wrong blockers: +2.95, Welch 0.005, permutation 0.
682. VL-20-682 | DROP -> DROP | REPRESENTED same-dest | 4.18 h2 vs sonnet+ember, wrong blockers: +3.25, Welch 0.010, permutation 0.029 (L37)
683. VL-20-683 | DROP -> DROP | REPRESENTED same-dest | 4.19 ember+terra vs ember+luna, DR found: -1.75, Welch 0.004, permutation 0.029 (L42)
684. VL-20-684 | EVAL -> EVAL | REPRESENTED same-dest | 4.20 h1 vs g6 (adding haiku), DR blocking (judge): +1.25, Welch 0.076, permutation 0.171 (
685. VL-20-685 | EVAL -> EVAL | REPRESENTED same-dest | 4.21 audit-F caveat (flags.tsv L56): about 48 tests in 12 comparisons x 4 metrics so 2-3 f
686. VL-20-686 | EVAL -> EVAL | REPRESENTED same-dest | 4.22 fam.tsv family table with sd: ember+2x luna n=6 DR 1.83 sd 0.41, blk 1.00 (judge) sd 
687. VL-20-687 | EVAL -> EVAL | REPRESENTED same-dest | 4.23 b8/b9 "beyond noise" labels (se rule: absolute difference at least 2 se) were too lib
688. VL-20-688 | EVAL -> EVAL | REPRESENTED same-dest | 4.24 Tokens per package-run (x3 in brackets): sonnet 29.4k (88k), haiku 57.5k (173k), grok
689. VL-20-689 | EVAL -> EVAL | REPRESENTED same-dest | 4.25 Blocking claims per run: terra 1.92, sol 2.00, luna 1.12, haiku 1.00, grok 1.29, wond
690. VL-20-690 | DROP -> DROP | REPRESENTED same-dest | 4.26 Claim "alias GT3 and GT4 never caught by any src row, so alias recall capped near 1-2
691. VL-20-691 | DROP -> DROP | REPRESENTED same-dest | 4.27 Attribution assumes the judge's R1..Rn labels are the reviewer ids sorted alphabetica
692. VL-20-692 | EVAL -> EVAL | REPRESENTED same-dest | Audit letter mapping inferred from order: A identity, B report validity, C inputs/timing, 
693. VL-20-693 | EVAL -> EVAL | REPRESENTED same-dest | Audit A: summary.md yes; audit.py 12,976 B, tbl.py; stats.json 5,623 B, flags.tsv 18,995 B
694. VL-20-694 | EVAL -> EVAL | REPRESENTED same-dest | Audit B: no summary.md; audit.py 14,375 B, patch.py, patch2.py, peek.py, sumry.py; stats.j
695. VL-20-695 | EVAL -> EVAL | REPRESENTED same-dest | Audit C: no summary.md; audit.py 14,724 B, candwrites.py, leakdbg.py; runs.json 231,656 B 
696. VL-20-696 | EVAL -> EVAL | REPRESENTED same-dest | Audit D: summary.md yes (8,267 B); audit.py 12,710 B, audit2.py 9,347 B, anch.py, bok.py, 
697. VL-20-697 | EVAL -> EVAL | REPRESENTED same-dest | Audit E: no summary.md; check.py 11,228 B, check2.py 4,193 B; by.json, rows.json 63,358 B 
698. VL-20-698 | EVAL -> EVAL | REPRESENTED same-dest | Audit F: no summary.md (stats.tsv, fam.tsv, presence.txt, recomputed.tsv act as output); r
699. VL-20-699 | DROP -> DROP | REPRESENTED same-dest | Only 2 of 6 audits (A, D) have a summary; B, C, E, F are known only second-hand from COMBO
700. VL-20-700 | EVAL -> EVAL | REPRESENTED same-dest | Audit A flag counts: 1b-name-derived-mismatch EXCLUDE 2 / WARN 6; 5-retry WARN 10; 5-stale
701. VL-20-701 | EVAL -> EVAL | REPRESENTED same-dest | Audit B flag counts: 1-incomplete EXCLUDE 51; 1-missing-input WARN 11; 1-short EXCLUDE 2 /
702. VL-20-702 | EVAL -> EVAL | REPRESENTED same-dest | Audit C flag counts: 1-era EXCLUDE 24 / WARN 201; 2-nosrc WARN 156; X-leak WARN 1; X-other
703. VL-20-703 | EVAL -> EVAL | REPRESENTED same-dest | Audit D flag counts: 1-panel WARN 6; 1-path EXCLUDE 10; 2-blockok EXCLUDE 80; 3-conserve E
704. VL-20-704 | EVAL -> EVAL | REPRESENTED same-dest | Audit E flag counts: 1.judgeread WARN 19; 1.labeldirs 1; 1.noscore 1; 3.anonledger EXCLUDE
705. VL-20-705 | EVAL -> EVAL | REPRESENTED same-dest | Audit F flag counts: 1-blocking-semantics WARN 26; 1-mismatch WARN 3; 3-completeness EXCLU
706. VL-20-706 | EVAL -> EVAL | REPRESENTED same-dest | A1 Audit A scope "890 reviewer runs (batch 10 excluded), 3 packages, 70 non-contaminated r
707. VL-20-707 | DROP -> DROP | REPRESENTED same-dest | A2 EXCLUDE 2 runs with 1 root cause: b4-muse-luna2/t2b-1 in alias and design asked muse-wo
708. VL-20-708 | EVAL -> EVAL | REPRESENTED same-dest | A3 Check 1 (intended = expected = observed in 828 runs, 0 mismatches; 102 runs derived fro
709. VL-20-709 | DROP -> DROP | REPRESENTED same-dest | A4 Check 2: fallback.log present in 0 runs; caveat that the known overwrite flaw means a s
710. VL-20-710 | DROP -> DROP | REPRESENTED same-dest | A5 Check 4: jq on raw attempt JSON 0 differences (not recomputable, raw JSON not committed
711. VL-20-711 | DROP -> DROP | REPRESENTED same-dest | A6 Check 5: cost.json equals sums of attemptN.meta.json in "all 930 runs"; 10 retries (glm
712. VL-20-712 | DROP -> DROP | REPRESENTED same-dest | A7 Check 6: unrecognized_model in 744 attempt .err files is a benign warning; under 400 to
713. VL-20-713 | EVAL -> EVAL | REPRESENTED same-dest | A8 E2 modelUsage extra keys: summary says 59 WARN (57 an auxiliary call to alias claude-gw
714. VL-20-714 | EVAL -> EVAL | REPRESENTED same-dest | A9 E11 "run present in sibling packages but missing here: 9 WARN" but flags.tsv has 1 E11 
715. VL-20-715 | KNOWLEDGE -> KNOWLEDGE | REPRESENTED same-dest | A10 E8 self-identification 6 WARN are all false positives ("as GPT" meaning the file under
716. VL-20-716 | DROP -> DROP | REPRESENTED same-dest | A11 Batch 10 (i1-grok-sonnet-r*, i2-haiku-sonnet-r*) dropped by owner order; earlier snaps
717. VL-20-717 | EVAL -> EVAL | REPRESENTED same-dest | A12 Audit A snapshot (2026-11-13 about 01:12 UTC, "eval is still being rerun by others") p
718. VL-20-718 | EVAL -> EVAL | REPRESENTED same-dest | B1 Audit B: 890 runs scanned, 51 incomplete refusals (sol 12, terra 26, haiku 11, luna 2, 
719. VL-20-719 | CORE -> CORE | REPRESENTED same-dest | B2 The 39 2-verdict-inconsistent reports are "blocking=0 verdict=FAIL" (all also in inc.tx
720. VL-20-720 | EVAL -> EVAL | REPRESENTED same-dest | B3 Anchor fidelity per model (anchors / whitespace-normalised verbatim / exact): ember 878
721. VL-20-721 | EVAL -> EVAL | REPRESENTED same-dest | B4 3-anchors EXCLUDE 10: every anchor of a run absent from the candidate (b4-muse-ember-lu
722. VL-20-722 | DROP -> DROP | REPRESENTED same-dest | B5 3-anchor-length WARN 52 (anchor over 200 chars), same cause as audit D's dropped findin
723. VL-20-723 | DROP -> DROP | REPRESENTED same-dest | B6 2-schema WARN 10: category unpassable-ac in c1-c5 rows and severity MEDIUM in g4-haiku-
724. VL-20-724 | CORE -> CORE | REPRESENTED same-dest | B7 X-truncated WARN 11: the report does not end with the verdict line (truncated output)
725. VL-20-725 | KNOWLEDGE -> KNOWLEDGE | REPRESENTED same-dest | B7 X-verdict-not-last 8, 2-noverdict 8, 2-firstline 8: reviewer prompt-compliance noise, v
726. VL-20-726 | HARNESS -> HARNESS | REPRESENTED same-dest | B8 patch.py and patch2.py edit audit.py in place (regex fixes such as (not, n't, no or nev
727. VL-20-727 | EVAL -> EVAL | REPRESENTED same-dest | C1 Slice 04 recomputed from runs.json that 156 of 665 valid-era runs never referenced sour
728. VL-20-728 | EVAL -> EVAL | REPRESENTED same-dest | C2 The source.md detection is "tool_use input or assistant text or report body contains so
729. VL-20-729 | DROP -> DROP | REPRESENTED same-dest | C3 Timeline: candidates fixed 2026-11-11 17:35 and byte-identical to sandbox copies; sourc
730. VL-20-730 | EVAL -> EVAL | REPRESENTED same-dest | C4 Isolation flags: X-leak 1 WARN (r5-glm-haiku2 DS t3-1 peeked at /tmp/evalsb/jobs*.tsv r
731. VL-20-731 | DROP -> DROP | REPRESENTED same-dest | C5 1-era EXCLUDE 24 are old-era sol/terra rows (n2/n4/n5/r2 x sol/terra x 3 packages), not
732. VL-20-732 | EVAL -> EVAL | REPRESENTED same-dest | C6 3-sha, 4-xpkg and 5-dupbody checks give no flags: no run quoted another package's sha, 
733. VL-20-733 | DROP -> DROP | REPRESENTED same-dest | C7 Audit C opens /tmp/evalsb/cand/<pkg>/source.md for KNOWN shas and raw attempt*.json (au
734. VL-20-734 | EVAL -> EVAL | REPRESENTED same-dest | D1 Audit D examined 89 rows x 3 packages = 264 merged-1.md, all ledger round 1 only; 264/3
735. VL-20-735 | EVAL -> EVAL | REPRESENTED same-dest | D2 C2 "block ok false": 80 EXCLUDE at reviewer level = 80 reviewer-package runs (335 raw f
736. VL-20-736 | EVAL -> EVAL | REPRESENTED same-dest | D3 Dropped findings by model and reason (audit2.json drop_model): luna 30 (27/2/1), ember 
737. VL-20-737 | EVAL -> EVAL | REPRESENTED same-dest | D4 Net dropped per model from kept/raw = 23 + 0 + 7 + 30 + 0 + 0 + 2 + 33 + 14 = 109 (re-d
738. VL-20-738 | DROP -> DROP | REPRESENTED same-dest | D5 "49 dropped findings were BLOCKING": flags 3-dropped-blocking 4 EXCLUDE + 45 WARN = 49 
739. VL-20-739 | EVAL -> EVAL | REPRESENTED same-dest | D6 Verdict flips are 3 package-rows with 4 findings (g3-sonnet-luna-ember-r3/alias t4-1 F1
740. VL-20-740 | DROP -> DROP | REPRESENTED same-dest | D7 C4: 0 row/verdict inconsistencies inside ledger.json and merged-1.md; X5: 0 violations 
741. VL-20-741 | EVAL -> EVAL | REPRESENTED same-dest | D8 C5 stale "16 EXCLUDE" flags are 8 reviewer-package runs counted twice (path-newer-than-
742. VL-20-742 | DROP -> DROP | REPRESENTED same-dest | D9 n5-sol and n5-terra (3 packages each): merged-1.md lists t4-1 but there is no t4-1.md i
743. VL-20-743 | CORE -> CORE | REPRESENTED same-dest | D10 .catfix.md: c2-haiku-grok (alias t4-1, t4-2) and c5-glm-haiku (alias and designSpec t4
744. VL-20-744 | DROP -> DROP | REPRESENTED same-dest | D11 45 merges (c2, c5, n2-*, n4-*, r2-*, r5) have no merge-stdout.txt and all 264 are merg
745. VL-20-745 | CORE -> CORE | REPRESENTED same-dest | D12 Clustering quality: rows with mixed categories 463, mixed blocking members 305, multip
746. VL-20-746 | HARNESS -> HARNESS | REPRESENTED same-dest | D13 audit2.py L40-L94 is a COPY of the findings.py logic (same_defect L367-L380, cluster L
747. VL-20-747 | DROP -> DROP | REPRESENTED same-dest | D14 Resolution model equals meta expected_model everywhere; 51 WARN t4-2 observed grok-4.7
748. VL-20-748 | HARNESS -> HARNESS | REPRESENTED same-dest | D15 audit.py parses findings only from the last fenced block while audit2.py requires a "F
749. VL-20-749 | EVAL -> EVAL | REPRESENTED same-dest | D16 EXCLUDE list: exclude-list.txt (54 rows with reviewer[cause:pkgs] codes B/P/S/C/V); su
750. VL-20-750 | EVAL -> EVAL | REPRESENTED same-dest | E1 294 judge outputs checked (rows.json 294, by.json 294); the scoring tree has 309 combo 
751. VL-20-751 | EVAL -> EVAL | REPRESENTED same-dest | E2 EXCLUDE 4.quarantined_source 30: merged-1.md exists only under quarantine-pre-src-luna 
752. VL-20-752 | EVAL -> EVAL | REPRESENTED same-dest | E2 r2-sonnet x 3 packages: 3.anonledger, 4.stale_vs_merged1 (score.json older than merged-
753. VL-20-753 | EVAL -> EVAL | REPRESENTED same-dest | E3 WARN 23: 1.judgeread 19 (judge Read of its own tool-results spill files, benign), 1.lab
754. VL-20-754 | EVAL -> EVAL | REPRESENTED same-dest | E4 check2.py (judge model, judge inputs, cross-package, cross-row, score written after jud
755. VL-20-755 | EVAL -> EVAL | REPRESENTED same-dest | E5 The "independent blind re-judge of 12 rows (12/12 exact, 19/19 catches, one borderline 
756. VL-20-756 | DROP -> DROP | REPRESENTED same-dest | E6 Checks needing uncommitted data (judge.json, judge.err size, mtimes; check.py L63-L82, 
757. VL-20-757 | DROP -> DROP | REPRESENTED same-dest | F1 Blocking semantics: 26 rows WARN where judge gt_covered_blocking exceeds the number of 
758. VL-20-758 | DROP -> DROP | REPRESENTED same-dest | F2 Recomputed table vs report: n2-sonnet-src any 8 vs 2, blocking 5 vs 0, wrong blockers 2
759. VL-20-759 | EVAL -> EVAL | REPRESENTED same-dest | F3 3-completeness: b4-muse-luna2 and e4-haiku2-ember have no scores (EXCLUDE x6); i1-/i2- 
760. VL-20-760 | EVAL -> EVAL | REPRESENTED same-dest | F4 cost.json counts retried attempts (g9-ember-luna-r1 AL t2b-1 tokens_all 23,280 vs final
761. VL-20-761 | DROP -> DROP | REPRESENTED same-dest | F5 11 stale-claim flags on COMBO-REPORT text (n2-sonnet-src 8/14 and 5/8 at L114, L132-133
762. VL-20-762 | EVAL -> EVAL | REPRESENTED same-dest | F6 Pitfalls: elapsed = sum over packages of the slowest reviewer (assumes full parallelism
763. VL-20-763 | EVAL -> EVAL | REPRESENTED same-dest | F7 2-family and other checks in recompute.py L88-L113 compare report model lists with meta
764. VL-20-764 | DROP -> DROP | REPRESENTED same-dest | 7.1 [RECOMPUTED] fullpkg() in A/final-table.py L15-L18 resolves TASK-WF-design-20261108-04
765. VL-20-765 | EVAL -> EVAL | REPRESENTED same-dest | 7.1 effect: excluded row-packages 69 (script) vs 71 (fixed by exact/keyword resolution); p
766. VL-20-766 | EVAL -> EVAL | REPRESENTED same-dest | 7.1 fixed clean table (committed values in brackets): ember+luna DS/AL/ctl 4/2/3 gives 2.2
767. VL-20-767 | EVAL -> DROP | REPRESENTED dedup->DR-092 | 7.2 Batch 11 (j1-sonnet-luna2-r1..r5, 45 reviewer runs, 15 merges, 15 judges, launched 202
768. VL-20-768 | DROP -> DROP | REPRESENTED same-dest | 7.3 audit-A summary vs data: E2 "59 WARN" (L22) vs 54 in flags.tsv, E11 "9 WARN" (L30) vs 
769. VL-20-769 | DROP -> DROP | REPRESENTED same-dest | 7.4 audit-D: 92 findings explained by validity rules vs 109 net dropped (haiku 7 vs 23, gr
770. VL-20-770 | DROP -> DROP | REPRESENTED same-dest | 7.5 [CODE-CONTRADICTED] COMBO-REPORT L292 "Four verdicts flipped FAIL->PASS": audit2.json 
771. VL-20-771 | DROP -> DROP | REPRESENTED same-dest | 7.6 [RECOMPUTED] COMBO-REPORT L294 "16 empty terra reviews in valid-era rows": valid-era r
772. VL-20-772 | EVAL -> EVAL | REPRESENTED same-dest | 7.7 Claim conflation: COMBO-REPORT L298 "2x luna + 2x ember has 2.75-3.25 more wrong block
773. VL-20-773 | DROP -> DROP | REPRESENTED same-dest | 7.8 Statistics: 48 tests (12 comparisons x 4 metrics), 6 with permutation p below 0.05, no
774. VL-20-774 | EVAL -> EVAL | REPRESENTED same-dest | 7.8 The permutation minimum p for 4 vs 4 runs is 0.029, so the p = 0.029 rows (ember+terra
775. VL-20-775 | DROP -> DROP | REPRESENTED same-dest | 7.9 [CODE-VERIFIED] superclaude review merge --round 1 fails with "the ledger expects roun
776. VL-20-776 | DROP -> DROP | REPRESENTED same-dest | 7.10 [CODE-VERIFIED] rules and [PARTLY CODE-CONTRADICTED] "no error": findings.py _check_f
777. VL-20-777 | EVAL -> EVAL | REPRESENTED same-dest | 7.11 Clustering defect: union-find over same_defect creates chains (195 of 1398, 83 rows w
778. VL-20-778 | MODULE-pr-review -> MODULE-pr-review | REPRESENTED same-dest | 7.12 46 rows have a null span (anchor not found in the candidate after flatten), 13 blocki
779. VL-20-779 | DROP -> DROP | REPRESENTED same-dest | 7.13 Hygiene: .catfix.md hand-edited reviewer outputs merged instead of the originals; aud
780. VL-20-780 | DROP -> DROP | REPRESENTED same-dest | 7.14 Hygiene: stale attempt files make highest attemptN wrong for 5 runs and inflate cost.
781. VL-20-781 | DROP -> DROP | REPRESENTED same-dest | 7.15 Hygiene: cost.json total_output_tokens_all includes a about 512-token auxiliary claud
782. VL-20-782 | DROP -> DROP | REPRESENTED same-dest | 7.16 Hygiene: elapsed = sum over packages of the slowest reviewer, excludes quarantined re
783. VL-20-783 | DROP -> DROP | REPRESENTED same-dest | 7.17 Defect class: a refusal is recorded as FAIL with an empty findings block (39 of 51 in
784. VL-20-784 | DROP -> DROP | REPRESENTED same-dest | 7.18 Scoring definition drift: judge gt_covered_blocking counts blocking-flagged-row match
785. VL-20-785 | DROP -> DROP | REPRESENTED same-dest | 7.19 Measurement limit: 89 real-blocking GT catches by any ledger row vs 38 in a blocking 
786. VL-20-786 | DROP -> DROP | REPRESENTED same-dest | 7.20 Benchmark limit: /14 is dominated by DS GT3 (63 rows), DS GT7 (50), AL GT2 (18) = 131
787. VL-20-787 | DROP -> DROP | REPRESENTED same-dest | 7.21 Recomputation limit: judge.json, raw attempt JSON, mtimes and /tmp/evalsb sandbox fil
788. VL-20-788 | DROP -> DROP | REPRESENTED same-dest | 7.22 [UNVERIFIED] The COMBO-REPORT L296 blind re-judge of 12 rows (12/12 exact, 19/19 catc
789. VL-20-789 | DROP -> DROP | REPRESENTED same-dest | 7.23 [UNVERIFIED] audit-E check2.py outputs (judge model counts, turns, strictness drift b
790. VL-20-790 | DROP -> DROP | REPRESENTED same-dest | 7.24 Six valid-era predicates give different populations (71 rows in final-table, untried 
791. VL-20-791 | DROP -> DROP | REPRESENTED same-dest | 7.25 COMBO-REPORT lines above L289 still show retracted numbers (n2-sonnet-src 8/14-5/8, "
792. VL-20-792 | DROP -> DROP | REPRESENTED same-dest | 7.26 three-way.py prints p[:8] (= TASK-WF-) for the flagged package list (L19; tw.out), so
793. VL-20-793 | DROP -> DROP | REPRESENTED same-dest | V1 findings-v1 schema and validation rules (audit2.py L8-L30): id, severity CRITICAL/MAJOR
794. VL-20-794 | CORE -> CORE | REPRESENTED same-dest | V2 No-silent-loss invariant: conservation check raw findings = kept + rejected-with-reason
795. VL-20-795 | DROP -> DROP | REPRESENTED same-dest | V3 Anchor limit 200 chars and per-model anchor fidelity (luna 91.4%, ember 97.9% = 860/878
796. VL-20-796 | CORE -> CORE | REPRESENTED same-dest | V4 Replace the union-find chaining of same_defect by bounded clustering or a per-pair rule
797. VL-20-797 | CORE -> CORE | REPRESENTED same-dest | V5 Blocking policy: the real gap is blocking classification (65 vs 38; 89 caught vs 38 in 
798. VL-20-798 | DROP -> DROP | REPRESENTED same-dest | V6 Refusal as FAIL/empty block (39 of 51): add an explicit incomplete outcome and never co
799. VL-20-799 | DROP -> DROP | REPRESENTED same-dest | V7 Model identity verification (expected, observed, init, model_ok, fallback.log; per-run 
800. VL-20-800 | DROP -> DROP | REPRESENTED same-dest | V8 The fallback ladder overwrote meta expected_model (A summary L12, L34), said fixed at C
801. VL-20-801 | CORE -> CORE | REPRESENTED same-dest | V9 Cost accounting rules: use the final-attempt meta (not summed stale attempts) and exclu
802. VL-20-802 | DROP -> DROP | REPRESENTED same-dest | V10 source.md not opened in 156 of 665 runs (ember 39%, luna 22%): assert the source was r
803. VL-20-803 | EVAL -> EVAL | REPRESENTED same-dest | V11 Isolation checks as a harness contract (no GT read, no candidate write, no cross-packa
804. VL-20-804 | CORE -> CORE | REPRESENTED same-dest | V12 Stale-merge detection: the ledger stores report_sha256 and doc_sha256 (my check: ledge
805. VL-20-805 | CORE -> CORE | REPRESENTED same-dest | V13 Idempotent re-merge: design the re-merge path for a round explicitly (7.9 "expects rou
806. VL-20-806 | EVAL -> EVAL | REPRESENTED same-dest | V14 Blind judge plus GT scoring (score.json schema, merged-anon.md, label-key.json, arm-ke
807. VL-20-807 | DROP -> DROP | REPRESENTED same-dest | V15 GT files (DS 10 items, AL 4, DE 2; blocking_in_implement; draft/final workflow with ve
808. VL-20-808 | DROP -> DROP | REPRESENTED same-dest | V16 Audit scripts A-F: port to repo-relative paths, fix hard-coded /tmp, keep as post-run 
809. VL-20-809 | HARNESS -> HARNESS | REPRESENTED same-dest | V17 final-table.py and three-way.py: fix the 7.1 bug, take paths as arguments, exclude by 
810. VL-20-810 | EVAL -> EVAL | REPRESENTED same-dest | V18 Statistical protocol: require replicates over different packages, not only reviewer sa
811. VL-20-811 | KNOWLEDGE -> KNOWLEDGE | REPRESENTED same-dest | V19 Per-model behaviour numbers (combo-est tables, untried.out presence effects, attrib/do
812. VL-20-812 | DROP -> DROP | REPRESENTED same-dest | V20 Panel results (final-table.md L1-L59) are the decision evidence for the default taskli
813. VL-20-813 | EVAL -> EVAL | REPRESENTED same-dest | V21 Decision update: sonnet+2x luna vs ember+2x luna not distinguishable on found, real bl
814. VL-20-814 | DROP -> DROP | REPRESENTED same-dest | V22 issue-table and allsets show which defects any panel can find; B1, B2, I5, I6 never ca
815. VL-20-815 | DROP -> DROP | REPRESENTED same-dest | V23 Batch scripts b7-b11 launch/merge/judge are one-off, rebuilt per batch with hard-coded
816. VL-20-816 | DROP -> DROP | REPRESENTED same-dest | V24 combo-est-A/B/self are pre-final hypotheses; keep one line about the independent-estim
817. VL-20-817 | DROP -> DROP | REPRESENTED same-dest | V25 gt2-hits.txt: unlabelled counts, no generator script, semantics unverified
818. VL-20-818 | DROP -> DROP | REPRESENTED same-dest | V26 RAW-TRANSCRIPTS-NOT-COMMITTED.md records 1.48 GB / 2,916 files off-repo; decide storag
819. VL-20-819 | CORE -> CORE | REPRESENTED same-dest | V27 Reviewer slot ids and tiers (t1b-1, t2-1, t2b-1, t3-1, t4-1, t4-2 with tier aliases cl
820. VL-20-820 | DROP -> DROP | REPRESENTED same-dest | V28 Verdict rules: merged verdict FAIL iff any blocking row; ledger rows render as L1 ... 
821. VL-20-821 | DROP -> DROP | REPRESENTED same-dest | V29 Owner-closed decision: no more combos, batch 10 dropped
822. VL-20-822 | DROP -> DROP | REPRESENTED same-dest | V30 COMBO-REPORT recommendations (default ember+2x luna 64k tokens; high-assurance haiku+2
823. VL-20-823 | DROP -> DROP | REPRESENTED same-dest | O1 Reviewer panel of heterogeneous models merged into one ledger (superclaude review merge
824. VL-20-824 | DROP -> DROP | REPRESENTED same-dest | O2 Model-combination experiment: E2 g1-g9, h1/h2, j1 (3 packages, 4-6 replicates) vs E1 "5
825. VL-20-825 | EVAL -> EVAL | REPRESENTED same-dest | O3 Blind judge against GT (arms/scoring, 319 files = 318 score.json + 1 invalid) vs E1 sha
826. VL-20-826 | EVAL -> EVAL | REPRESENTED same-dest | O4 Model identity audit (audit A): does E1 troubleshoot/shadow-run tooling have the same f
827. VL-20-827 | CORE -> CORE | REPRESENTED same-dest | O5 Finding schema findings-v1 vs the reflect findings YAML schema (merged-verdict.yaml)
828. VL-20-828 | CORE -> CORE | REPRESENTED same-dest | O7 Shared kernel code: git diff --stat 6c0984326 HEAD -- findings.py ledger.py is empty (m
829. VL-20-829 | CORE -> CORE | REPRESENTED same-dest | O8 E1 cluster.py keeps union-find but marks a cluster chained when two members do not matc
830. VL-20-830 | MODULE-spec -> MODULE-spec | REPRESENTED same-dest | O6 Stoprule/diffgate/ledger spec-panel variants are not in this slice; E3 installed varian
831. VL-20-831 | DROP -> DROP | REPRESENTED same-dest | T1 Finding intake: machine-checked schema with an explicit reject list and the conservatio
832. VL-20-832 | CORE -> CORE | REPRESENTED same-dest | T2 Reviewer status outcomes: ok, incomplete (refusal), invalid-block, wrong-model, retried
833. VL-20-833 | DROP -> DROP | REPRESENTED same-dest | T3 Provenance: per run expected, observed and init model, attempt, aux calls, cost split b
834. VL-20-834 | DROP -> DROP | REPRESENTED same-dest | T4 Input delivery: assert that source material was read; sandbox without sibling plans or 
835. VL-20-835 | DROP -> DROP | REPRESENTED same-dest | T5 Clustering and rows: bounded clustering; row text from all members or from the blocking
836. VL-20-836 | DROP -> DROP | REPRESENTED same-dest | T6 Blocking policy: separate "reviewer says blocking" from "verified blocking"; EVAL repor
837. VL-20-837 | DROP -> DROP | REPRESENTED same-dest | T7 Round semantics: explicit re-merge or new-round API; ledger stores report and doc hashe
838. VL-20-838 | DROP -> DROP | REPRESENTED same-dest | T8 Evaluation harness: GT + blind judge + exact-package exclusion + repo-relative paths + 
839. VL-20-839 | MODULE-tasklist -> MODULE-tasklist | REPRESENTED same-dest | T9 Module thinness: module-specific parts observed here are the reviewer brief (plan/taskl
840. VL-20-840 | MODULE-pr-review -> MODULE-pr-review | REPRESENTED same-dest | X1 PR code review: the 200-char anchor limit and markdown-heading section clustering (sect
841. VL-20-841 | MODULE-rfqa -> MODULE-rfqa | REPRESENTED same-dest | X2 rf-qa replacement: E2 GT derives from implementation outcomes of 3 plans, there is no G
842. VL-20-842 | MODULE-spec -> MODULE-spec | REPRESENTED same-dest | X3 Spec review (brainstorm/design): the DE control has only 2 GT items and 0 blocking, con
843. VL-20-843 | MODULE-reflect -> MODULE-reflect | REPRESENTED same-dest | X4 reflect UC-1/UC-2: the blocking boolean and categories differ from the 4-category devia
844. VL-20-844 | DROP -> DROP | REPRESENTED same-dest | X5 Multi-round loops: all 264 ledgers are round 1 only (D X4), round-2/3 verification not 
845. VL-20-845 | EVAL -> EVAL | REPRESENTED same-dest | X6 Cost/latency budgets: output tokens only, elapsed assumes parallelism; ember+luna 52,39
846. VL-20-846 | DROP -> DROP | REPRESENTED same-dest | X7 Model availability: wonder exhausted (COMBO-REPORT L369), glm excluded, spark never tes
847. VL-20-847 | DROP -> DROP | REPRESENTED same-dest | Slice 04 summary 1: analysis/ has about 130 files, 6 audit directories, only A and D with 
848. VL-20-848 | DROP -> DROP | REPRESENTED same-dest | Slice 04 summary 2: after patching paths, final-table.py reproduces the committed final-ta
849. VL-20-849 | DROP -> DROP | REPRESENTED same-dest | Slice 04 summary 3 (hard numbers): 71 rows, 213 row-packages, 69 excluded (script) / 71 (c
850. VL-20-850 | DROP -> DROP | REPRESENTED same-dest | Slice 04 summary 4 (new defects): fullpkg() mis-assigns every DE exclusion to designSpec (
851. VL-20-851 | DROP -> DROP | REPRESENTED same-dest | Slice 04 summary 5 (code verified at tip): v1 validation rules and union-find clustering e
852. VL-20-852 | DROP -> DROP | REPRESENTED same-dest | Slice 04 summary 6: V1-V30 map to CORE, CORE-RUN, EVAL or DROP
853. VL-20-853 | DROP -> DROP | REPRESENTED same-dest | Gap G1: not read: COMBO-REPORT outside L286-L375 and L386-L433 samples, PILOT-REPORT, mani
854. VL-20-854 | DROP -> DROP | REPRESENTED same-dest | Gap G2: not opened individually: allsets chunk files and outputs, issue-NN.json, b7/b9/b10
855. VL-20-855 | DROP -> DROP | REPRESENTED same-dest | Gap G3: judge-run claims (E5 re-judge, check2.py outputs, judge model identity) have no co
856. VL-20-856 | DROP -> DROP | REPRESENTED same-dest | Gap G4: gt2-hits.txt semantics unknown
857. VL-20-857 | DROP -> DROP | REPRESENTED same-dest | Gap G5: the 1b-name-derived-mismatch, E2 and 5-retry flag lists were counted but not re-de
858. VL-20-858 | EVAL -> EVAL | REPRESENTED same-dest | Gap G6: the corrected exclusion mapping (diag2.py) maps flags to packages by keyword; not 
859. VL-20-859 | DROP -> DROP | REPRESENTED same-dest | Gap G7: g*/h*/n*/r* score.json used only through the committed analysis scripts; individua
860. VL-20-860 | DROP -> DROP | REPRESENTED same-dest | Gap G8: /tmp/s04-e2 holds the slice's extraction and diagnostic scripts (not part of the r
861. VL-20-861 | EVAL -> EVAL | REPRESENTED same-dest | Slice 04 Q1: should the unified benchmark keep blocking_in_implement GT semantics, and how
862. VL-20-862 | DROP -> DROP | REPRESENTED same-dest | Slice 04 Q2: which 70 rows does audit A's header refer to (summary L3), given 71/88/89 els
863. VL-20-863 | DROP -> DROP | REPRESENTED same-dest | Slice 04 Q3: where do the 17 haiku/grok findings dropped without a validity-rule reason co
864. VL-20-864 | DROP -> DROP | REPRESENTED same-dest | Slice 04 Q4: does E1's shadow/5x3 experiment reuse the same three packages and GT; if so E
865. VL-20-865 | DROP -> DROP | REPRESENTED same-dest | Slice 04 Q5: should the j1 batch be audited before the "NOT CONFIRMED" decision update is 
866. VL-20-866 | DROP -> DROP | REPRESENTED same-dest | Slice 04 Q6: should merge raise a hard error or an explicit rejected-findings list for ove
867. VL-20-867 | DROP -> DROP | REPRESENTED same-dest | Slice 04 Q7: is the refusal-as-FAIL encoding (7.17) handled by E1's reviewer status or by 
868. VL-20-868 | DROP -> DROP | REPRESENTED same-dest | Slice 04 Q8: should audits A-F ship as a reusable verify-run command and who owns it

COUNT 20-value-ledger-e2-study.md: 868

## File 9: research/web-03-git-branch-hierarchy-stacked-prs.md

1. A1 git check-ref-format rule list (10 rules); does NOT state leaf-versus-prefix constraint; validates a name in isolation
2. B1 loose refs one file per ref, packed-refs flat fallback; inference: feat/review-panel file vs directory; same rule across loose and packed
3. B2 exact error text (parent after child / child after parent), prefix depends on command, Git 2.39.3 community reproductions, same phrase also for stale .lock files
4. B3 TRANSACTION_NAME_CONFLICT; conflict enforced against packed refs; git fetch hints git remote prune; stale remote-tracking ref needs fetch --prune
5. B4 same constraint for remote-tracking refs after remote rename; fetch --prune / remote prune origin
6. B5 reftable alternative backend (default for new repos in Git 3.0 per blog; experimental per gitperf); whether it removes the leaf-vs-prefix restriction UNVERIFIED
7. C1 slashes group branches but group name cannot also be a branch; four derived practical rules (no prefix leaf; hyphenated sibling or leaf umbrella /main /base; decide before first push; no bare numbers); repo one-slash layout cannot hit conflict
8. D1 GitHub native stacked PRs GA (2026-10-06): each PR targets below, protection and CI on every PR, bottom-up merge, Rebase stack keeps approvals, merge methods, merge queue aware, gh stack, same-repository limitation (no cross-fork), not in GitHub Desktop; /sc:pr-submit capability unchecked
9. D2 community rough edges (a)-(e) single-source; conflicts with GA docs on squash; prefer docs
10. E1 git rebase --onto recipe after squash-merge, --force-with-lease, plain rebase duplicates reason, auto-retarget per blog unverified, "Automatically delete head branches" recommendation, force-push under pr-submit needs own check
11. E2 rebase.updateRefs / --update-refs (LOW, UNVERIFIED)
12. F1 gh stack tool (install, requires gh 2.0+/Git 2.36+, commands, submit base, init adopts branches, release notes disagree on prefix flags; literal branch names)
13. F2 Graphite (gt submit atomic, temporary base branch, requires dismiss-stale-approvals Disabled, price list unverified, multiple trunks, CI blocks merge before lower PRs)
14. F3 ghstack (three branches per change gh/<user>/<n>/{base,head,orig}, never force-pushed, cannot use merge button, ghstack land, stale branches; no leaf-vs-prefix conflict by construction; negative fit with /sc:pr-submit)
15. F4 git-branchless and related commit-stack tools (git-pr, Remote-Ref, related tools)
16. G1 reviews and approvals (per-layer diff, Rebase stack retains approvals, hand-built stacks dismiss approvals, advice to disable; bottom-to-top review, drafts); stack as way to land multi-piece panel in dependency order
17. G2 CI behaviour (default-branch PR CI for all PRs; protection against stack base; CircleCI rerun across stack, path filtering, keep change together if cost exceeds; diffox hand-built checks did not re-run); UNVERIFIED branches: filter / base-branch trigger; 404 on GitHub optimize-CI page
18. G3 source conflicts (pullnotifier squash/merge queue vs GA docs)
19. Key External Findings 1-8
20. Recommendations 1-6 (name branches; stack vs sequential PRs; CI branches filter check; avoid ghstack/Graphite; bottom-up gate and CI cost; items left open)
21. Summary/provenance (tavily, no fallback; no run-1 read; no git command run)

COUNT web-03-git-branch-hierarchy-stacked-prs.md: 21

## File 10: research/web-04-finding-schemas-review-bots.md

1. 1.1 SARIF result (kind vs level, identity fields guid/correlationGuid/fingerprints/partialFingerprints/baselineState, location region, absent region = whole file)
2. 1.2 GitHub code scanning SARIF subset (rules properties, security-severity, partialFingerprints primaryLocationLineHash, relative URIs SRCROOT)
3. 1.3 SARIF limitations (fingerprint appendix; state layered on top of finding)
4. 1.4 GitLab ingestion (requires ruleId + location; severity default medium; identity; silent collapse without region)
5. 2.1 reviewdog rdjson/rdjsonl (diagnostic shape, severity, code, suggestions, reporters)
6. 3.1 GitHub PR review comment API (comments endpoint params, position closing down, reviews endpoint, commit_id)
7. 3.2 practical constraints (older position shape, 422 on single-comment, out-of-diff rejection, no append to pending review, no file+line mix)
8. 4.1 GitHub code scanning two severity ideas (level + security-severity bands, check failure defaults, configurable thresholds)
9. 4.2 CodeRabbit four independent axes (type, severity, category, effort; p1-p4; acceptance rate)
10. 4.3 Greptile per-PR 0-5 confidence score and severity threshold
11. 4.4 observed bot re-review behaviour (Copilot unstable set; Greptile summary-only; vendor precision figures unverified)
12. 4.5 Codex review P0-P3, only P0/P1 shown, overall correctness verdict, issue 27691 SHA binding gap, third-party action dedup
13. 5.1 review threads resolved state on thread; GraphQL resolveReviewThread; thread node id; token limitations
14. 5.2 code scanning alert state open/dismissed, dismissed_reason closed vocabulary, rule vs instance split
15. 5.3 SARIF suppressions and baselineState; dismiss-alerts action mapping
16. 5.4 cross-round dedup and carry-forward in bots
17. 6 minimal interoperable finding record (11 field rows: stable id; location; side+commit SHA; content anchor; message; severity ordinal + vendor label; category/lens separate; tool identity; suggested fix; state outside finding; confidence at verdict level)
18. 6 not found in any source: standard per-finding confidence field; standard quote-anchor location type (own extensions)
19. 7 discrepancies and caveats (no contradiction with code; Augment format not researched; forum-sourced API behaviours + API version header; vendor stats not used; SARIF value tables partly visible)
20. Key External Findings 1-7
21. Recommendations 1-7 (one shared record; ledger holds disposition; confidence at verdict; export adapters + postable check; severity router as configuration; do not adopt full SARIF; look up Augment's format)
22. Summary/provenance

COUNT web-04-finding-schemas-review-bots.md: 22

## File 11: synthesis/synth-04-external-findings.md

1. Preamble: all findings are EXTERNAL context; provenance; discrepancies with code-verified facts (none recorded)
2. Tension table / merge-verdict comparison / open items / source conflicts / vocabulary comparison / web-04 caveats headings carried as text blocks (see table rows below)
3. Statement on precedence (external never overrides code-verified facts)
4. [5. External Research Findings] web-02-claude-code-hooks-headless.md | provider=tavily (Tavily returned passages, not full pag
5. [5. External Research Findings] web-03-git-branch-hierarchy-stacked-prs.md | provider=tavily (default); no fallback fired
6. [5. External Research Findings] web-04-finding-schemas-review-bots.md | provider=tavily; no fallback used
7. [5.1.1 LLM-as-judge biases (position, verbosity, self-prefere] Finding: [EXTERNAL] [A1] Zheng et al. (MT-Bench / Chatbot Arena) name four judge limits: positio
8. [5.1.1 LLM-as-judge biases (position, verbosity, self-prefere] Finding: [EXTERNAL] [A2] Panickssery, Bowman and Feng: LLM evaluators recognise their own output
9. [5.1.1 LLM-as-judge biases (position, verbosity, self-prefere] Finding: [EXTERNAL] [A3] Chen et al. 2025: self-preference appears in both pre-trained and post-
10. [5.1.1 LLM-as-judge biases (position, verbosity, self-prefere] Finding: [EXTERNAL] [A4] Ye et al., CALM: defines 12 judge biases (position, verbosity, compassi
11. [5.1.2 Panels of diverse models, and correlated errors] Finding: [EXTERNAL] [B1] Verga et al. (Cohere), PoLL: a panel of smaller judges from disjoint fa
12. [5.1.2 Panels of diverse models, and correlated errors] Finding: [EXTERNAL] [B2] Kim, Garg, Peng and Garg, "Correlated Errors in LLMs": across over 350 
13. [5.1.2 Panels of diverse models, and correlated errors] Finding: [EXTERNAL] [B3] Kohli, "Nine Judges, Two Effective Votes" (Apple ML Research; arXiv 260
14. [5.1.2 Panels of diverse models, and correlated errors] Merge keeps only findings flagged by 2 of 3 reviewers | D3 Entelligence golden-set rule
15. [5.1.2 Panels of diverse models, and correlated errors] Independent review plus merge is a sound default | C1
16. [5.1.3 Debate versus independent review plus aggregation] Finding: [EXTERNAL] [C1] "Debate or Vote" (NeurIPS 2025): across seven NLP benchmarks, majority 
17. [5.1.3 Debate versus independent review plus aggregation] Finding: [EXTERNAL] [C2] An explainer states the voting lift depends on independent errors (same
18. [5.1.4 Code-review-specific evidence on ensembles and merge r] Finding: [EXTERNAL] [D1] SWR-Bench: 1,000 manually verified PRs, LLM-based evaluation of whether
19. [5.1.4 Code-review-specific evidence on ensembles and merge r] Finding: [EXTERNAL] [D2] GitHub ReviewBench: 219 PRs from 187 repositories in 19 languages (vend
20. [5.1.4 Code-review-specific evidence on ensembles and merge r] Finding: [EXTERNAL] [D3] LangChain's ReviewBench (a different artifact from GitHub's, a 59-task 
21. [5.1.4 Code-review-specific evidence on ensembles and merge r] Finding: [EXTERNAL] [D4] c-CRAB code review benchmark: automated review tools pass 20.1% to 32.1
22. [5.1.4 Code-review-specific evidence on ensembles and merge r] Finding: [EXTERNAL] [D5] A practitioner note suggests self-consistency over N samples as a cheap
23. [5.1.5 Measuring agreement and judge reliability] Finding: [EXTERNAL] [AE-1] Raw agreement overstates reliability. "Reliability without Validity" 
24. [5.1.5 Measuring agreement and judge reliability] Finding: [EXTERNAL] [AE-2] Position bias is judge-dependent and task-dependent. A systematic pos
25. [5.1.6 Verification of reviewer findings (grounding and citat] Finding: [EXTERNAL] [G1] "Citation-Grounded Code Comprehension": a mechanical check that every c
26. [5.1.6 Verification of reviewer findings (grounding and citat] Finding: [EXTERNAL] [G2] Two-pass detect-then-filter patterns and "AI opinion is not evidence". 
27. [5.1.7 Quorum, verdict and aggregation rules] Finding: [EXTERNAL] [F1] "Vibe Coding on Trial" (unanimous LLM juries): 15 open models benchmark
28. [5.1.7 Quorum, verdict and aggregation rules] Finding: [EXTERNAL] [F2] Practitioner guidance on verdict rules: Splunk suggests majority vote f
29. [5.1.7 Quorum, verdict and aggregation rules] Finding: [EXTERNAL] [F3] Aggregation cannot fix correlated judges. CARE (Confounder-Aware Aggreg
30. [5.1.7 Quorum, verdict and aggregation rules] 2-of-3 majority on findings | Entelligence golden set (D3)
31. [5.1.7 Quorum, verdict and aggregation rules] Unanimous (AND) acceptance | Ullah and Serwadda (F1)
32. [5.1.7 Quorum, verdict and aggregation rules] Any-pass / max pooling | Splunk guidance (F2)
33. [5.1.7 Quorum, verdict and aggregation rules] Weighted / dependence-aware | CARE, SkillAggregation, Dawid-Skene, Ising (F3)
34. [5.2.1 Hook events and when PostToolUse fires] Finding: [EXTERNAL] PostToolUse fires only after a tool call SUCCEEDS; a failed call fires Po
35. [5.2.2 Hooks inside `claude -p` and `--bare`] Finding: [EXTERNAL] --output-format values: text (default), json, stream-json. The headl
36. [5.2.3 stream-json shape, `--resume`, `--fork-session`, cost] Finding: [EXTERNAL] stream-json needs --verbose (documented example: claude -p "..." --outp
37. [5.2.4 Tool restriction flags] Finding: [EXTERNAL] --allowedTools / --allowed-tools lists tools that run WITHOUT a permissi
38. [5.2.5 Subagent definitions] Finding: [EXTERNAL] Subagent frontmatter has tools (allowlist) and disallowedTools (denylist
39. [5.2.6 Settings precedence and `--settings`] Finding: [EXTERNAL] Managed (organization) settings are top level and cannot be overridden by us
40. [5.2.7 `--model` with non-Anthropic gateway ids] Finding: [EXTERNAL] ANTHROPIC_CUSTOM_MODEL_OPTION adds one custom id to the /model picker an
41. [5.2.8 Field reports on hooks and resume in `claude -p`] Finding: [EXTERNAL] Issue 79702 (opened 2026-07-21, Claude Code v2.1.216, macOS): in print mode 
42. [5.2.8 Field reports on hooks and resume in `claude -p`] Finding: [EXTERNAL] Issue 10373 (date not shown, older): the reporter notes "PreToolUse and Post
43. [5.2.8 Field reports on hooks and resume in `claude -p`] Finding: [EXTERNAL] Issue 37559 (Mar 2026 per the thread): a user reported no hooks fired in -p
44. [5.2.8 Field reports on hooks and resume in `claude -p`] Finding: [EXTERNAL] Issue 9630 (date not shown): a response states "It is intentional that we do
45. [5.2.8 Field reports on hooks and resume in `claude -p`] Finding: [EXTERNAL] Issues 18311 and 22724 (early 2026): --resume problems when sessions-inde
46. [5.2.9 Hooks inside subagents and hook input fields] Finding: [EXTERNAL] "Hooks from settings files, managed policy settings, and plugins also run in
47. [5.2.10 `--session-id`, `--settings`, `--restricted`] Finding: [EXTERNAL] --session-id <uuid> uses a specific session id (must be a valid UUID), so 
48. [5.2.10 `--session-id`, `--settings`, `--restricted`] Hook merge behaviour across settings sources | Not confirmed
49. [5.2.10 `--session-id`, `--settings`, `--restricted`] Gateway model id behaviour for hooks, --resume, --sessi | Not documented in any source reviewed
50. [5.2.10 `--session-id`, `--settings`, `--restricted`] Dates of issues 9630 and 10373 | Not shown; statements may be outdated
51. [5.2.10 `--session-id`, `--settings`, `--restricted`] Wildcard globs in code spans | Stripped by the extractor; check source pages
52. [5.2.10 `--session-id`, `--settings`, `--restricted`] Official docs content | Passages only, not full pages
53. [5.3.1 Ref naming rules and the leaf-versus-prefix conflict] Finding: [EXTERNAL] [A1] git check-ref-format rules: slash-separated components may not begin 
54. [5.3.1 Ref naming rules and the leaf-versus-prefix conflict] Finding: [EXTERNAL] [B1] Loose refs are one file per ref in a (sub)directory under $GIT_DIR/ref
55. [5.3.1 Ref naming rules and the leaf-versus-prefix conflict] Finding: [EXTERNAL] [B2] Exact error text for the directory/file conflict, creating the parent a
56. [5.3.1 Ref naming rules and the leaf-versus-prefix conflict] Finding: [EXTERNAL] [B3] TRANSACTION_NAME_CONFLICT is Git's internal error code for failing to
57. [5.3.1 Ref naming rules and the leaf-versus-prefix conflict] Finding: [EXTERNAL] [B4] The same constraint applies to remote-tracking refs: after a remote bra
58. [5.3.1 Ref naming rules and the leaf-versus-prefix conflict] Finding: [EXTERNAL] [B5] --ref-format=files (loose files plus packed-refs) is the default; re
59. [5.3.2 Naming conventions that avoid the conflict] Finding: [EXTERNAL] [C1] Slashes group branches, but a group name cannot also be a branch. Stack
60. [5.3.3 GitHub native stacked pull requests] Finding: [EXTERNAL] [D1] GitHub stacked PRs (generally available per a changelog dated 2026-10-0
61. [5.3.3 GitHub native stacked pull requests] Finding: [EXTERNAL] [D2] Community reports on rough edges (single-source, unverified): (a) a sta
62. [5.3.4 Manual stacked-branch practice] Finding: [EXTERNAL] [E1] After feature1 is squash-merged into master as a new commit S, f
63. [5.3.4 Manual stacked-branch practice] Finding: [EXTERNAL] [E2] rebase.updateRefs / --update-refs for stacks: pullnotifier.com reco
64. [5.3.5 Stacking tools: naming and where they push] Finding: [EXTERNAL] [F1] gh stack (GitHub CLI extension): install with gh extension install g
65. [5.3.5 Stacking tools: naming and where they push] Finding: [EXTERNAL] [F2] Graphite (gt CLI): gt submit pushes every branch of the stack atomi
66. [5.3.5 Stacking tools: naming and where they push] Finding: [EXTERNAL] [F3] ghstack: every local commit becomes its own PR, pushed to three branche
67. [5.3.5 Stacking tools: naming and where they push] Finding: [EXTERNAL] [F4] git-branchless is a suite of tools (git undo, smartlog, git restack
68. [5.3.6 How reviews and CI treat stacked PRs] Finding: [EXTERNAL] [G1] Reviewers see only the diff of their own layer (stack map in the merge 
69. [5.3.6 How reviews and CI treat stacked PRs] Finding: [EXTERNAL] [G2] CI: GitHub docs say CI checks triggered by PRs on the default branch ru
70. [5.3.6 How reviews and CI treat stacked PRs] Squash or rebase default merge settings break stack ide | AlphaSignal (preview-period blog, D2c)
71. [5.4.1 SARIF 2.1.0] Finding: [EXTERNAL] [web-04 1.1] A SARIF result carries ruleId, message, locations[], op
72. [5.4.1 SARIF 2.1.0] Finding: [EXTERNAL] [web-04 1.2] GitHub code scanning consumes a SARIF subset. Example: tool.dr
73. [5.4.1 SARIF 2.1.0] Finding: [EXTERNAL] [web-04 1.3] The SARIF spec calls for stable fingerprints and has an appendi
74. [5.4.1 SARIF 2.1.0] Finding: [EXTERNAL] [web-04 1.4] GitLab ingestion: requires ruleId and a physical location (fi
75. [5.4.2 reviewdog rdjson] Finding: [EXTERNAL] [web-04 2.1] rdjson top level: source {name, url}, severity (default for
76. [5.4.3 GitHub pull-request review comment API] Finding: [EXTERNAL] [web-04 3.1] POST /repos/{owner}/{repo}/pulls/{pull_number}/comments takes
77. [5.4.3 GitHub pull-request review comment API] Finding: [EXTERNAL] [web-04 3.2] User-reported constraints (not official statements): the create
78. [5.4.4 Severity models in code scanning and review bots] Finding: [EXTERNAL] [web-04 4.1] GitHub code scanning has two severity ideas. All alerts have a 
79. [5.4.4 Severity models in code scanning and review bots] Finding: [EXTERNAL] [web-04 4.2] CodeRabbit labels a finding with four independent closed vocabu
80. [5.4.4 Severity models in code scanning and review bots] Finding: [EXTERNAL] [web-04 4.3] Greptile assigns a 0-5 confidence score per pull request (5 pro
81. [5.4.4 Severity models in code scanning and review bots] Finding: [EXTERNAL] [web-04 4.4] One evaluation reports GitHub Copilot review surfacing new comm
82. [5.4.4 Severity models in code scanning and review bots] Finding: [EXTERNAL] [web-04 4.5] Codex review (a third-party reviewer already used by pr_submit
83. [5.4.5 Resolution, suppression and dedup vocabularies] Finding: [EXTERNAL] [web-04 5.1] Resolved state lives on the review thread, not the comment. Use
84. [5.4.5 Resolution, suppression and dedup vocabularies] Finding: [EXTERNAL] [web-04 5.2] GitHub code scanning alert state is open or dismissed; dis
85. [5.4.5 Resolution, suppression and dedup vocabularies] Finding: [EXTERNAL] [web-04 5.3] A SARIF suppression object has a kind (inSource, a syntac
86. [5.4.5 Resolution, suppression and dedup vocabularies] Finding: [EXTERNAL] [web-04 5.4] Cross-round dedup and carry-forward in bots: a third-party acti
87. [5.4.5 Resolution, suppression and dedup vocabularies] location: repo-relative path, start line, optional end  | SARIF region; rdjson range; PR API path/line/start_line
88. [5.4.5 Resolution, suppression and dedup vocabularies] location side and commit SHA (only for PR posting) | PR API side, commit_id; Codex issue about SHA binding
89. [5.4.5 Resolution, suppression and dedup vocabularies] content anchor or fingerprint (survives line drift) | SARIF partialFingerprints.primaryLocationLineHash; v1 a
90. [5.4.5 Resolution, suppression and dedup vocabularies] message | present in every format
91. [5.4.5 Resolution, suppression and dedup vocabularies] severity as a small ordinal (3-4 levels) plus optional  | SARIF level; rdjson ERROR/WARNING/INFO; Codex P0-P3; Co
92. [5.4.5 Resolution, suppression and dedup vocabularies] category/lens kept separate from severity | CodeRabbit four independent axes; SARIF rule tags
93. [5.4.5 Resolution, suppression and dedup vocabularies] tool/reviewer identity | SARIF tool.driver; rdjson source; alert tool
94. [5.4.5 Resolution, suppression and dedup vocabularies] optional suggested fix | rdjson suggestions; GitHub suggestion blocks
95. [5.4.5 Resolution, suppression and dedup vocabularies] state/disposition outside the finding (ledger): status  | SARIF baselineState/suppressions; code scanning dismiss
96. [5.4.5 Resolution, suppression and dedup vocabularies] confidence at verdict level, not per finding | Greptile PR-level 0-5 score; Codex overall correctness 
97. [5.4.5 Resolution, suppression and dedup vocabularies] reviewdog rdjson | ERROR, WARNING, INFO
98. [5.4.5 Resolution, suppression and dedup vocabularies] CodeRabbit | critical, major, minor, trivial (plus info, none); p1-p
99. [5.4.5 Resolution, suppression and dedup vocabularies] Codex on GitHub | P0, P1, P2, P3 (numeric priority 0-3)
100. [5.4.5 Resolution, suppression and dedup vocabularies] Greptile | per-PR confidence 0-5; inline severity levels
101. [5.4.5 Resolution, suppression and dedup vocabularies] Augment | not researched
102. [Key takeaways (external context only)] 2 | Cross-family panels beat a single large judge on QA-sty
103. [Key takeaways (external context only)] 3 | Independent review plus aggregation is a sound default;
104. [Key takeaways (external context only)] 4 | For code review, aggregating several independent review
105. [Key takeaways (external context only)] 5 | Merge and verdict rules in use are opposed (union, 2-of
106. [Key takeaways (external context only)] 6 | Agreement must be reported chance-corrected; judge stab
107. [Key takeaways (external context only)] 7 | Cheap non-LLM verification (mechanical citation check) 
108. [Key takeaways (external context only)] 8 | PostToolUse fires only on success; hooks load in claude
109. [Key takeaways (external context only)] 9 | Field reports: PostToolUse, Stop, SessionStart command 
110. [Key takeaways (external context only)] 10 | Hooks also run inside Agent-tool subagents with agent_i
111. [Key takeaways (external context only)] 11 | --allowedTools only pre-approves; availability uses --t
112. [Key takeaways (external context only)] 12 | Gateway model ids: --model is per-process; hooks, --res
113. [Key takeaways (external context only)] 13 | feat/review-panel and feat/review-panel/<name> pass che
114. [Key takeaways (external context only)] 14 | GitHub native stacked PRs are generally available (2026
115. [Key takeaways (external context only)] 15 | SARIF, rdjson and the GitHub PR comment API share a min
116. [Coverage of every web file's Key External Findings and Recom] web-01 | Key finding 2 (diverse panel beats single judge)
117. [Coverage of every web file's Key External Findings and Recom] web-01 | Key finding 3 (correlated errors, at most 11% gap close
118. [Coverage of every web file's Key External Findings and Recom] web-01 | Key finding 4 (independent review plus aggregation; deb
119. [Coverage of every web file's Key External Findings and Recom] web-01 | Key finding 5 (SWR-Bench recall gain, union merge)
120. [Coverage of every web file's Key External Findings and Recom] web-01 | Key finding 6 (opposed merge rules; no evidence on whic
121. [Coverage of every web file's Key External Findings and Recom] web-01 | Key finding 7 (chance-corrected agreement; stability is
122. [Coverage of every web file's Key External Findings and Recom] web-01 | Key finding 8 (non-LLM verification; citation limit)
123. [Coverage of every web file's Key External Findings and Recom] web-01 | Key finding 9 (union still short of human review)
124. [Coverage of every web file's Key External Findings and Recom] web-01 | Rec 1 (keep independent per-model review plus merge; no
125. [Coverage of every web file's Key External Findings and Recom] web-01 | Rec 2 (measure diversity; fix collapse or repeat runs; 
126. [Coverage of every web file's Key External Findings and Recom] web-01 | Rec 3 (agreement as prioritisation, not proof; citation
127. [Coverage of every web file's Key External Findings and Recom] web-01 | Rec 4 (choose verdict rule by measurement; TPR/FPR/Youd
128. [Coverage of every web file's Key External Findings and Recom] web-01 | Rec 5 (state the one-valid-reviewer-passes rule as perm
129. [Coverage of every web file's Key External Findings and Recom] web-01 | Rec 6 (randomise or swap order; hide majority or author
130. [Coverage of every web file's Key External Findings and Recom] web-01 | Rec 7 (down-weight a reviewer from the code author's mo
131. [Coverage of every web file's Key External Findings and Recom] web-01 | Rec 8 (do not claim replacement of human or test-based 
132. [Coverage of every web file's Key External Findings and Recom] web-01 | Rec 9 (defer weighted aggregation until labelled data e
133. [Coverage of every web file's Key External Findings and Recom] web-02 | Key finding 1 (PostToolUse success only)
134. [Coverage of every web file's Key External Findings and Recom] web-02 | Key finding 2 (--bare drops hooks)
135. [Coverage of every web file's Key External Findings and Recom] web-02 | Key finding 3 (field reports)
136. [Coverage of every web file's Key External Findings and Recom] web-02 | Key finding 4 (hooks in subagents; SubagentStop fields)
137. [Coverage of every web file's Key External Findings and Recom] web-02 | Key finding 5 (--allowedTools vs --tools; subagent allo
138. [Coverage of every web file's Key External Findings and Recom] web-02 | Key finding 6 (per-process --model; custom ids)
139. [Coverage of every web file's Key External Findings and Recom] web-02 | Key finding 7 (LiteLLM picker filter)
140. [Coverage of every web file's Key External Findings and Recom] web-02 | Key finding 8 (--session-id, resume, stream-json, cost)
141. [Coverage of every web file's Key External Findings and Recom] web-02 | Key finding 9 (--settings precedence; hooks merge uncon
142. [Coverage of every web file's Key External Findings and Recom] web-02 | Rec 1 (do not mark hooks-in-claude -p verified for gate
143. [Coverage of every web file's Key External Findings and Recom] web-02 | Rec 2 (never launch hook-dependent reviewers with --bar
144. [Coverage of every web file's Key External Findings and Recom] web-02 | Rec 3 (hook on both PostToolUse and PostToolUseFailure;
145. [Coverage of every web file's Key External Findings and Recom] web-02 | Rec 4 (prefer Agent dispatch with a SubagentStop comman
146. [Coverage of every web file's Key External Findings and Recom] web-02 | Rec 5 (keep the reviewer allowlist; board writes via ho
147. [Coverage of every web file's Key External Findings and Recom] web-02 | Rec 6 (hooks-merge question blocks only layered --setti
148. [Coverage of every web file's Key External Findings and Recom] web-02 | Rec 7 (codebase precedence reminder)
149. [Coverage of every web file's Key External Findings and Recom] web-03 | Key finding 1 (ref storage; check-ref-format does not f
150. [Coverage of every web file's Key External Findings and Recom] web-03 | Key finding 2 (error text)
151. [Coverage of every web file's Key External Findings and Recom] web-03 | Key finding 3 (packed and remote-tracking refs; prune)
152. [Coverage of every web file's Key External Findings and Recom] web-03 | Key finding 4 (naming rule; layout before first push)
153. [Coverage of every web file's Key External Findings and Recom] web-03 | Key finding 5 (GitHub native stacks; same-repo limit)
154. [Coverage of every web file's Key External Findings and Recom] web-03 | Key finding 6 (git rebase --onto; auto-retarget unverif
155. [Coverage of every web file's Key External Findings and Recom] web-03 | Key finding 7 (Graphite, ghstack, git-branchless)
156. [Coverage of every web file's Key External Findings and Recom] web-03 | Key finding 8 (reviews and CI; source conflicts)
157. [Coverage of every web file's Key External Findings and Recom] web-03 | Rec 1 (name branches so none is a prefix of another; de
158. [Coverage of every web file's Key External Findings and Recom] web-03 | Rec 2 (GitHub-native stack if /sc:pr-submit can create 
159. [Coverage of every web file's Key External Findings and Recom] web-03 | Rec 3 (check CI branches: filters for hand-built stacks
160. [Coverage of every web file's Key External Findings and Recom] web-03 | Rec 4 (avoid ghstack; avoid Graphite unless settings ac
161. [Coverage of every web file's Key External Findings and Recom] web-03 | Rec 5 (treat bottom-up merge order as a gate; plan CI c
162. [Coverage of every web file's Key External Findings and Recom] web-03 | Rec 6 (items left open: reftable, official --onto and -
163. [Coverage of every web file's Key External Findings and Recom] web-04 | Key finding 1 (SARIF kind/level/identity; absent region
164. [Coverage of every web file's Key External Findings and Recom] web-04 | Key finding 2 (GitHub SARIF subset; severity and gate)
165. [Coverage of every web file's Key External Findings and Recom] web-04 | Key finding 3 (rdjson closest to a PR-review finding)
166. [Coverage of every web file's Key External Findings and Recom] web-04 | Key finding 4 (PR review API location type; out-of-diff
167. [Coverage of every web file's Key External Findings and Recom] web-04 | Key finding 5 (bot severity/category axes; verdict-leve
168. [Coverage of every web file's Key External Findings and Recom] web-04 | Key finding 6 (closed resolution vocabulary; thread id)
169. [Coverage of every web file's Key External Findings and Recom] web-04 | Key finding 7 (dedup keys; silent collapse in GitLab)
170. [Coverage of every web file's Key External Findings and Recom] web-04 | Rec 1 (one shared record: id, category, path, start lin
171. [Coverage of every web file's Key External Findings and Recom] web-04 | Rec 2 (disposition, status, thread id, dismissal reason
172. [Coverage of every web file's Key External Findings and Recom] web-04 | Rec 3 (confidence on verdict or cluster, not per findin
173. [Coverage of every web file's Key External Findings and Recom] web-04 | Rec 4 (export adapters to rdjson, GitHub comments[], op
174. [Coverage of every web file's Key External Findings and Recom] web-04 | Rec 5 (severity router as configuration over the intern
175. [Coverage of every web file's Key External Findings and Recom] web-04 | Rec 6 (do not adopt full SARIF internally; export targe
176. [Coverage of every web file's Key External Findings and Recom] web-04 | Rec 7 (look up Augment's comment format or read pr_subm

COUNT synth-04-external-findings.md: 176

## File 12: synthesis/synth-09-sequence-and-gates.md

1. Scope statement (input for later /sc:workflow plan; no roadmap, branch plan, PR plan, risk register, estimate or schedule)
2. Source key table (R18, R06, R16, R13, W03) and tag rules ([CODE-VERIFIED], [CARRIED], [CODE-CONTRADICTED], [UNVERIFIED], [WEB])
3. (d) status paragraph: R16 Part 4 conditions are research conclusions not repository policy
4. (d) evidence tiers S, Q, G (R16 s4.2)
5. [8.2 Sequence and Gates] R06 | 06-reflect-two-engines.md (reflect contract, verdict ma
6. [8.2 Sequence and Gates] R16 | 16-eval-governance.md (evaluation governance, acceptanc
7. [8.2 Sequence and Gates] R13 | 13-future-pr-review-and-rfqa.md (PR code review and rf-
8. [8.2 Sequence and Gates] W03 | web-03-git-branch-hierarchy-stacked-prs.md (external we
9. [(a) Binding constraints] C2 | The ### 9.1 YAML block of sc-reflect-protocol/SKILL.md 
10. [(a) Binding constraints] C3 | The reflect verdict map is frozen by a 36-test matrix. 
11. [(a) Binding constraints] C4 | A branch name cannot also be a path-prefix of another b
12. [(a) Binding constraints] C5 | src/superclaude/{skills,agents,commands,hooks,templates
13. [(a) Binding constraints] C6 | make lint-architecture pairs commands and protocol skil
14. [(a) Binding constraints] C7 | Installed primitives never tell an agent to read or inv
15. [(a) Binding constraints] C8 | plugins/superclaude/ is a hand-maintained, partial copy
16. [(a) Binding constraints] C9 | PRs go only to the fork IronbellyOrg/IronClaude, only t
17. [(a) Binding constraints] C10 | Project worktrees are created only through Orca, with a
18. [(a) Binding constraints] C11 | .claude/{skills,agents,commands,hooks,templates}/* is n
19. [(a) Binding constraints] C12 | Python work is UV only, runs on Python 3.10, and is for
20. [(a) Binding constraints] C13 | Review-rule wording in tracked primitive text is scanne
21. [(a) Binding constraints] C14 | A command file with a ## Unattended mode heading must b
22. [(a) Binding constraints] C15 | Constraints required by the adjudicated winners (rows C
23. [(a) Binding constraints] C16 | "No change to cli/reflect" holds in the weak reading on
24. [(a) Binding constraints] C17 | The repair step is reachable only through a repair=Fals
25. [(a) Binding constraints] C18 | Tests that assert the old clearing, verdict and verdict
26. [(a) Binding constraints] C19 | Reflect keeps shortfall: visible, contract.derive_verdi
27. [(a) Binding constraints] C20 | The packaged gateway.launch map stays {}; no packaged t
28. [(a) Binding constraints] C21 | One guard test compares the ordered ids of aliases.<tie
29. [(a) Binding constraints] C22 | Run-record edits to the reflect skill stay inside ### 4
30. [(a) Binding constraints] C23 | PR review module: the converter is pure (dict in and ou
31. [(a) Binding constraints] C24 | Tasklist and workflow keep the single call /sc:reflect 
32. [(a) Binding constraints] C25 | rf-qa first change: the standard lens dimensions at /ta
33. [(a) Binding constraints] C26 | Tasklist Medium: the label map is module data (Form 1 o
34. [(a) Binding constraints] C27 | Process-redesign parts built now are optional: a module
35. [(a) Binding constraints] C28 | Evaluation: generic harness code lives in scripts/ with
36. [(a) Binding constraints] C29 | Collaboration off state: no new file under ~/.claude/ho
37. [(b) No-regression gates] G2 | Reflect contract lint pins
38. [(b) No-regression gates] G3 | Reflect SKILL.md pins
39. [(b) No-regression gates] G4 | Whole reflect test directory
40. [(b) No-regression gates] G5 | Production wiring of reflect Tier 2
41. [(b) No-regression gates] G6 | Consumer-read contract field names
42. [(b) No-regression gates] G7 | Stage 2 exit script baseline
43. [(b) No-regression gates] G8 | Review kernel tests and golden fixtures
44. [(b) No-regression gates] G9 | Mirror, architecture and lint gates
45. [(b) No-regression gates] G10 | Installed-path baseline
46. [(b) No-regression gates] G11 | Review-rule text scanner
47. [(b) No-regression gates] G12 | Spec-panel Review Loop and plugin parity
48. [(b) No-regression gates] G13 | Worker-contract registry
49. [(b) No-regression gates] G14 | PR-review code surface left as is
50. [(b) No-regression gates] G15 | rf-qa static pins
51. [(b) No-regression gates] G16 | Contract-constant and generator-constraint gates
52. [(b) No-regression gates] G17 | Review-kernel pins under the C-01 shape (gate required 
53. [(b) No-regression gates] G18 | Clearing, quorum and merge-policy replay (source: revie
54. [(b) No-regression gates] G19 | Reflect write-side helpers and the grounded lane (sourc
55. [(b) No-regression gates] G20 | Engine switch behind reflect (source: reviews/adversari
56. [(b) No-regression gates] G21 | Limits repair measurements and kill lines (source: revi
57. [(b) No-regression gates] G22 | Dispatch gates and shape tests (source: reviews/adversa
58. [(b) No-regression gates] G23 | Run-record measurements (source: reviews/adversarial/ru
59. [(b) No-regression gates] G24 | PR review measurements (source: reviews/adversarial/pr-
60. [(b) No-regression gates] G25 | Process-redesign gates, in the order the debate fixed (
61. [(b) No-regression gates] G26 | Evaluation acceptance tiers and offline tests (source: 
62. [(b) No-regression gates] G27 | Tasklist Medium measurements and containment test (sour
63. [(c) Dependency facts] D2 | src/superclaude/commands/<x>.md containing ## Activatio
64. [(c) Dependency facts] D3 | A field must be listed in SKILL.md 9.1 or 9.2 and in bo
65. [(c) Dependency facts] D4 | A contract with contract_version 1.8.0 and only listed 
66. [(c) Dependency facts] D5 | A producer of deviation signals and remediation_task_pa
67. [(c) Dependency facts] D6 | Code that writes the artifact layout the lint reads mus
68. [(c) Dependency facts] D7 | One card file-name convention must exist before the lin
69. [(c) Dependency facts] D8 | A serialization of the contract that quotes bracketed m
70. [(c) Dependency facts] D9 | A locator-agnostic annotate and citation-keyed ledger r
71. [(c) Dependency facts] D10 | Module-declared category, lens and severity sets must e
72. [(c) Dependency facts] D11 | A per-slot lens (or brief id) key in panel templates mu
73. [(c) Dependency facts] D12 | A panel finding with a positive integer line must exist
74. [(c) Dependency facts] D13 | A mechanically read-only reviewer must exist before "re
75. [(c) Dependency facts] D14 | A checklist output mode with a computed confidence must
76. [(c) Dependency facts] D15 | A behavioural replay oracle must exist before an rf-qa 
77. [(c) Dependency facts] D16 | A superclaude CLI subcommand must exist before a skill 
78. [(c) Dependency facts] D17 | Run-time records (served model per reviewer call, tool-
79. [(c) Dependency facts] D18 | Raw, kept and rejected counts in the ledger entry must 
80. [(c) Dependency facts] D19 | The E2 ground-truth files must be reachable before any 
81. [(c) Dependency facts] D20 | A review-kernel subcommand module must be named in the 
82. [(c) Dependency facts] D21 | A one-directional import (reflect imports review) must 
83. [(c) Dependency facts] D22 | A main-session caller must exist before a panel fan-out
84. [(c) Dependency facts] D23 | A normalizing adapter from panel findings to pr_submit.
85. [(c) Dependency facts] D24 | One definition of the "reviewer failed" finding must ex
86. [(c) Dependency facts] D25 | The rf-qa Fix Cycle text is not a hard dependency of th
87. [(c) Dependency facts] D26 | The Stage 2 exit script's empty-baseline comparison is 
88. [(d) Acceptance evidence a panel design needs] AE-2 | Each use case has its own ground truth. Tasklist review
89. [(d) Acceptance evidence a panel design needs] AE-3 | The decision rule, the values file and the analysis scr
90. [(d) Acceptance evidence a panel design needs] AE-4 | Judge integrity is checked in code: judge model equals 
91. [(d) Acceptance evidence a panel design needs] AE-5 | Replicates vary the package, not only the reviewer draw
92. [(d) Acceptance evidence a panel design needs] AE-6 | An executable run verifier (R16 calls it verify-run) pa
93. [(d) Acceptance evidence a panel design needs] AE-7 | Tier S checks run in code and pass: (1) no silent loss 
94. [(d) Acceptance evidence a panel design needs] AE-8 | A held-out set is declared before the first run, never 
95. [(d) Acceptance evidence a panel design needs] AE-9 | E1 and E2 are treated as one evidence family and a pack
96. [(d) Acceptance evidence a panel design needs] AE-10 | AI-produced labels are used only as a smoke test and te
97. [(d) Acceptance evidence a panel design needs] AE-11 | Where natural GT does not exist (PR review, rf-qa repla
98. [(d) Acceptance evidence a panel design needs] AE-12 | An isolation check covers tool calls and transcripts, n
99. [(d) Acceptance evidence a panel design needs] AE-13 | The metric of record is named per gate: GT items found 
100. [(d) Acceptance evidence a panel design needs] AE-14 | If the E1 Stage 2 exit is kept as a Tier S gate, it pas
101. [(d) Acceptance evidence a panel design needs] AE-15 | Acceptance for a use case names who owns each layer: ke
102. [Core (shared review kernel, `src/superclaude/cli/review/`, 2] src/superclaude/cli/review/findings.py (457 lines) | v1 vocabularies SEVERITIES, CATEGORIES (:14-24); annota
103. [Core (shared review kernel, `src/superclaude/cli/review/`, 2] src/superclaude/cli/review/findings_v2.py (304 lines) | ROLES, LENSES (:35-36), CHANNELS, DEVIATION_CLASSES; ch
104. [Core (shared review kernel, `src/superclaude/cli/review/`, 2] src/superclaude/cli/review/ledger.py (494 lines) | merge_round calls annotate (:127-138); keeps only the f
105. [Core (shared review kernel, `src/superclaude/cli/review/`, 2] src/superclaude/cli/review/panel.py (707 lines) | _KINDS (:36); resolve_slot with hard_exclude and strict
106. [Core (shared review kernel, `src/superclaude/cli/review/`, 2] src/superclaude/cli/review/manifest.py, cluster.py, ver | Used by the shadow steps; manifest_cmd.py names --t2-en
107. [Core (shared review kernel, `src/superclaude/cli/review/`, 2] src/superclaude/cli/review/data/*.json (nine templates) | Slot keys slot_id, tier, count, strategy; no lens key; 
108. [Core (shared review kernel, `src/superclaude/cli/review/`, 2] src/superclaude/cli/main.py:568-570 (review), :559-561  | Registers both groups
109. [Core (shared review kernel, `src/superclaude/cli/review/`, 2] src/superclaude/contracts/__init__.py and src/superclau | Own the reserved contract-constant names and the lint t
110. [Core (shared review kernel, `src/superclaude/cli/review/`, 2] tests/review/ (19 test files plus fixtures/) | Covers cli/review; new core tests land here by the repo
111. [Core (shared review kernel, `src/superclaude/cli/review/`, 2] Possible new core location for run verification (kernel | Placement is undecided; skills reach package behaviour 
112. [Module: reflect (`src/superclaude/cli/reflect/`, scripts, sk] src/superclaude/cli/reflect/panel_lint.py (366 lines) | The 1.8.0 shape gate; lists :33, :146; lint_panel_contr
113. [Module: reflect (`src/superclaude/cli/reflect/`, scripts, sk] src/superclaude/cli/reflect/ensemble.py (895 lines), _d | Engine A, the production Tier-2 swarm engine; emits con
114. [Module: reflect (`src/superclaude/cli/reflect/`, scripts, sk] src/superclaude/cli/reflect/runner.py (834), config.py  | Wrapper: engine selection runner.py:538-545, verdict :5
115. [Module: reflect (`src/superclaude/cli/reflect/`, scripts, sk] src/superclaude/skills/sc-reflect-protocol/SKILL.md (20 | Engine B prose; shadow steps L340-L349; routing L703; c
116. [Module: reflect (`src/superclaude/cli/reflect/`, scripts, sk] src/superclaude/agents/reflect-reviewer.md | Read-only reviewer (permissionMode: plan, no Bash, Edit
117. [Module: reflect (`src/superclaude/cli/reflect/`, scripts, sk] scripts/reflect_shadow_exit.py (410 lines), reflect_ver | Post-run checks, each with a test; exit-script defects 
118. [Module: reflect (`src/superclaude/cli/reflect/`, scripts, sk] tests/cli/reflect/ (38 test files plus conftest.py, __i | Contract, verdict, skill and isolation pins (G1 to G4)
119. [Module: reflect (`src/superclaude/cli/reflect/`, scripts, sk] Files that name the wrapper: src/superclaude/skills/sc- | Callers of reflect; the "executor-disjoint ensemble" cl
120. [Module: reflect (`src/superclaude/cli/reflect/`, scripts, sk] src/superclaude/cli/reflect/__init__.py docstring | Stale: describes a claude --print subprocess and five m
121. [Module: PR code review (`src/superclaude/pr_submit/`, `sc-pr] src/superclaude/skills/sc-pr-submit-protocol/SKILL.md ( | Main-session rule :47-49; Wave 2 to Wave 6b at :303-310
122. [Module: PR code review (`src/superclaude/pr_submit/`, `sc-pr] src/superclaude/skills/sc-auggie-review-protocol/SKILL. | file:line grounding contract :22; --revagent accepts fo
123. [Module: PR code review (`src/superclaude/pr_submit/`, `sc-pr] tests/pr_submit/ (50 test files) | Pins Finding, router, codex reviews, troubleshoot seed
124. [Module: PR code review (`src/superclaude/pr_submit/`, `sc-pr] New adapter from panel findings to Finding | Location not determined by the research
125. [Module: rf-qa replacement (`/task` phase gate and the rf-* a] src/superclaude/agents/rf-qa.md (551), rf-qa-qualitativ | Read-write agents with permissionMode: bypassPermission
126. [Module: rf-qa replacement (`/task` phase gate and the rf-* a] 44 structured subagent_type: rf-* lines in 8 SKILL.md f | Call-site census, a lower bound
127. [Module: rf-qa replacement (`/task` phase gate and the rf-* a] tests/audit/ (17 rf-qa files), tests/skills/ (5), tests | Static pins (G15)
128. [Module: rf-qa replacement (`/task` phase gate and the rf-* a] src/superclaude/commands/spec-panel.md (:22, :256-268), | The master review loop and its plugin twin; the loop re
129. [Module: rf-qa replacement (`/task` phase gate and the rf-* a] src/superclaude/cli/swarm/lenses/ (8 populated lenses p | The only existing "lens as data"; no coupling to cli/re
130. [Repository-wide files] plugins/superclaude/ (125 tracked files) | Hand-maintained mirror; copy is optional for CI
131. [Repository-wide files] src/superclaude/core/HOW-WE-WORK.md and plugins/supercl | Must be byte-equal (test_routing_plugin_parity.py:38) i
132. [Repository-wide files] E2 evidence tree on branch ironbelly/eval-tasklist-revi | Harness files absent from HEAD, hard-coded absolute pat
133. [Repository-wide files] E1 package .dev/eval-workspaces/shadow-model-combos/ (P | E1 experiment and the 13 counted pilot runs; the leak c
134. [Corrected claims carried by this section ([CODE-CONTRADICTED] CLAUDE.md:18: .claude/settings.json is the only tracked | git ls-files .claude also lists .claude/cache/sc-recomm
135. [Corrected claims carried by this section ([CODE-CONTRADICTED] CLAUDE.md:292-299: branches master from integration, a  | No integration ref exists locally or as origin/integrat
136. [Corrected claims carried by this section ([CODE-CONTRADICTED] sc-tasklist-protocol/SKILL.md L1141, L1152, L1165 and t | In production the wrapper runs the swarm engine and app
137. [Corrected claims carried by this section ([CODE-CONTRADICTED] Pilot EV-1 "no contract file" for runs 04, 08, 09 | The file exists and fails YAML parsing at line 103 (D8)
138. [Corrected claims carried by this section ([CODE-CONTRADICTED] E2 COMBO-REPORT.md AUDIT-CLEAN view (:339-359) and "69  | Computed with the fullpkg() prefix mis-mapping; reprodu
139. [Corrected claims carried by this section ([CODE-CONTRADICTED] "Findings anchor on text only" (slice-level statement) | True for findings-v1 and for the ledger and merge path 
140. [Corrected claims carried by this section ([CODE-CONTRADICTED] spec-panel Review Loop has a hard dependency on rf-qa F | Not a hard dependency (D25)
141. [Corrected claims carried by this section ([CODE-CONTRADICTED] docs/designs/spec-panel-review-loop.md:3: "Design only  | spec-panel.md:22 carries --re-review and :256 has ## Re
142. [Coverage check of the research files' key findings (rule 7)] R18 | lint-architecture checks, contract-constant names, *_va
143. [Coverage check of the research files' key findings (rule 7)] R18 | pre-commit blocks only five .claude/ dirs and one skill
144. [Coverage check of the research files' key findings (rule 7)] R18 | Ref rule, exact error text, both orders, dash sibling a
145. [Coverage check of the research files' key findings (rule 7)] R18 | Installed-path rule has no global scanner, 148-line bas
146. [Coverage check of the research files' key findings (rule 7)] R18 | Contract pins 1.8.0, 110 and 27, byte-identical block, 
147. [Coverage check of the research files' key findings (rule 7)] R18 | Plugin mirror partial and hand-kept
148. [Coverage check of the research files' key findings (rule 7)] R18 | Naive-layout failure table F1 to F18
149. [Coverage check of the research files' key findings (rule 7)] R18 | Package and test layout (cli/review 25 files, registrat
150. [Coverage check of the research files' key findings (rule 7)] R18 | Stale docs S1 to S7
151. [Coverage check of the research files' key findings (rule 7)] R06 | Two engines, only contract.py shared; wrapper uses engi
152. [Coverage check of the research files' key findings (rule 7)] R06 | What must stay byte-identical (six items)
153. [Coverage check of the research files' key findings (rule 7)] R06 | Stage 2 failures are mechanical; 0.75 vs 0.80, vocabula
154. [Coverage check of the research files' key findings (rule 7)] R06 | Which engine to absorb (composition direction)
155. [Coverage check of the research files' key findings (rule 7)] R16 | Acceptance evidence matrix, three tiers
156. [Coverage check of the research files' key findings (rule 7)] R16 | E2 harness defects, audits A to F, fullpkg(), j1
157. [Coverage check of the research files' key findings (rule 7)] R16 | E1 and E2 not independent, package hash
158. [Coverage check of the research files' key findings (rule 7)] R16 | Ownership options O1 to O3
159. [Coverage check of the research files' key findings (rule 7)] R16 | verify-run audit-to-check mapping
160. [Coverage check of the research files' key findings (rule 7)] R13 | PR review blockers P1 to P15, rf-qa blockers R1 to R12
161. [Coverage check of the research files' key findings (rule 7)] R13 | Minimum core shape M1 to M14
162. [Coverage check of the research files' key findings (rule 7)] R13 | Lens-name collision (swarm registry vs /task QA lenses)
163. [Coverage check of the research files' key findings (rule 7)] W03 | git check-ref-format does not forbid either name; confl
164. [Coverage check of the research files' key findings (rule 7)] W03 | GitHub stacked PRs same-repository limit, bottom-up mer
165. [Open Questions (items tagged [UNVERIFIED] or undecided in th] OQ2 | Remote-side behaviour of the ref rule was not tested (n
166. [Open Questions (items tagged [UNVERIFIED] or undecided in th] OQ3 | Can /sc:pr-submit --monitor 3 create stacked PRs or set
167. [Open Questions (items tagged [UNVERIFIED] or undecided in th] OQ4 | make verify-sync, make lint-architecture, pytest and ru
168. [Open Questions (items tagged [UNVERIFIED] or undecided in th] OQ5 | Completeness of the per-file installed-path pins is unk
169. [Open Questions (items tagged [UNVERIFIED] or undecided in th] OQ6 | Is a plugin copy of a new panel skill wanted? No test r
170. [Open Questions (items tagged [UNVERIFIED] or undecided in th] OQ7 | The E2 branch tip 6c0984326 was not read by R18 for col
171. [Open Questions (items tagged [UNVERIFIED] or undecided in th] OQ8 | Which convergence threshold is intended, 0.75 (SKILL.md
172. [Open Questions (items tagged [UNVERIFIED] or undecided in th] OQ9 | Five further skill-versus-code vocabulary conflicts wit
173. [Open Questions (items tagged [UNVERIFIED] or undecided in th] OQ10 | Add reviewer_briefs_materialized to SKILL.md 9.2 and th
174. [Open Questions (items tagged [UNVERIFIED] or undecided in th] OQ11 | Should the wrapper switch to engine B, or should engine
175. [Open Questions (items tagged [UNVERIFIED] or undecided in th] OQ12 | Contents of the swarm lens template reflect-review-outp
176. [Open Questions (items tagged [UNVERIFIED] or undecided in th] OQ13 | What does tests/review/test_reflect_consumer_inventory.
177. [Open Questions (items tagged [UNVERIFIED] or undecided in th] OQ14 | Findings-v2 KeyError 'anchor' on the ledger path: re-re
178. [Open Questions (items tagged [UNVERIFIED] or undecided in th] OQ15 | Which metric of record gates a panel (GT items found, r
179. [Open Questions (items tagged [UNVERIFIED] or undecided in th] OQ16 | Is the E2 GT acceptable as the tasklist-review GT once 
180. [Open Questions (items tagged [UNVERIFIED] or undecided in th] OQ17 | Where does verify-run live (kernel CLI, tested script, 
181. [Open Questions (items tagged [UNVERIFIED] or undecided in th] OQ18 | Keep E1's Stage 2 exit as a Tier S gate after fixing it
182. [Open Questions (items tagged [UNVERIFIED] or undecided in th] OQ19 | Is a formal six-audit-method audit of batch j1 needed? 
183. [Open Questions (items tagged [UNVERIFIED] or undecided in th] OQ20 | Who approves spend for blind scoring of the 15 E1 runs 
184. [Open Questions (items tagged [UNVERIFIED] or undecided in th] OQ21 | rf-qa replacement: is the /task phase gate the first ta
185. [Open Questions (items tagged [UNVERIFIED] or undecided in th] OQ22 | Should findings-v2 become the single wire format with m
186. [Open Questions (items tagged [UNVERIFIED] or undecided in th] OQ23 | Cost of a local multi-model panel per PR round is not m
187. [Open Questions (items tagged [UNVERIFIED] or undecided in th] OQ24 | auggie-review.md and pr-submit.md command files and the

COUNT synth-09-sequence-and-gates.md: 187

## File 13: synthesis/synth-10-questions-evidence.md

1. Section 9 how-to-read paragraph (Impact, Suggested Resolution, Source columns)
2. Section 10 path-prefix paragraph (every path starts with the task folder; checked with Glob)
3. Section 10 research planning note (research-notes.md is not one of the 24 files)
4. [9.1 Finding contract, severity, verdict and ledger] Q-02 | Which finding location type is the default: quoted anch
5. [9.1 Finding contract, severity, verdict and ledger] Q-03 | Do unknown finding keys stay open (v1/v2, E2 in-line or
6. [9.1 Finding contract, severity, verdict and ledger] Q-04 | Which severity scale is canonical: blocking plus CRITIC
7. [9.1 Finding contract, severity, verdict and ledger] Q-05 | Who owns the verdict: reviewer-typed line, ledger boole
8. [9.1 Finding contract, severity, verdict and ledger] Q-06 | What is the quorum for PASS (all dispatched, 2 of 3, ma
9. [9.1 Finding contract, severity, verdict and ledger] Q-07 | One ledger schema and status vocabulary (resolved_check
10. [9.1 Finding contract, severity, verdict and ledger] Q-08 | Which reflect convergence threshold (0.75 or 0.80) and 
11. [9.1 Finding contract, severity, verdict and ledger] Q-09 | Is the intended Stage-3+ design that the reflect wrappe
12. [9.2 Dispatch, identity, tiers, input delivery and runtime] Q-11 | Is served_model a first-class field (sidechain message.
13. [9.2 Dispatch, identity, tiers, input delivery and runtime] Q-12 | Does muse-ember-1.0 get served by the gateway today, an
14. [9.2 Dispatch, identity, tiers, input delivery and runtime] Q-13 | Should the core own a per-module roster and exclusion r
15. [9.2 Dispatch, identity, tiers, input delivery and runtime] Q-14 | Does naming source.md and every shipped input in the br
16. [9.2 Dispatch, identity, tiers, input delivery and runtime] Q-15 | Should the central panel build and verify the snapshot,
17. [9.2 Dispatch, identity, tiers, input delivery and runtime] Q-16 | Which deadline rule applies without a per-input baselin
18. [9.3 Collaboration designs] Q-18 | Do PostToolUse additionalContext and --settings reach a
19. [9.3 Collaboration designs] Q-19 | Can the E2 collaboration harnesses be reproduced? [UNVE
20. [9.4 Process redesign (E2 brainstorms)] Q-21 | [UNVERIFIED] reading gaps of the process-redesign and b
21. [9.5 Consumers, PR code review and rf-qa replacement] Q-23 | Spec, brainstorm, design and plugin consumers. Who fixe
22. [9.5 Consumers, PR code review and rf-qa replacement] Q-24 | PR code review and rf-qa replacement. Is the panel a th
23. [9.6 Evaluation governance, E2 evidence and harness ownership] Q-26 | Is the Stage 2 exit (20 shadow runs, EV-1 vs legacy bas
24. [9.6 Evaluation governance, E2 evidence and harness ownership] Q-27 | Where does verify-run live (kernel CLI vs tested script
25. [9.6 Evaluation governance, E2 evidence and harness ownership] Q-28 | [UNVERIFIED] E2 evidence that cannot be re-derived or i
26. [9.7 E3 variants, repository constraints, telemetry, memory a] Q-30 | Repository constraints. Should lib/ stay gitignored (.g
27. [9.7 E3 variants, repository constraints, telemetry, memory a] Q-31 | Telemetry and memory. Should the unified panel write de
28. [9.7 E3 variants, repository constraints, telemetry, memory a] Q-32 | Which single destination does each ambiguous ledger row
29. [9.7 E3 variants, repository constraints, telemetry, memory a] Q-33 | Minor reading gaps and doc defects in the code-side res
30. [9.8 Unresolved [CODE-CONTRADICTED] follow-up and owner decis] Q-35 | OWNER-DECISION: may this run's .dev/tasks output be com
31. [9.8 Unresolved [CODE-CONTRADICTED] follow-up and owner decis] Q-36 | OWNER-DECISIONS carried from the rows above, to be put 
32. [9.10 Debate-derived open questions (added by the adjudicatio] Q-39 | [POST-BASELINE] Do the later commits of the tasklist br
33. [9.10 Debate-derived open questions (added by the adjudicatio] Q-40 | OWNER-DECISION: the owner approved "one shared Review P
34. [9.10 Debate-derived open questions (added by the adjudicatio] Q-41 | What does "no change to cli/reflect" allow? H1 for refl
35. [9.10 Debate-derived open questions (added by the adjudicatio] Q-42 | Where does the per-round requested count come from? C-0
36. [9.10 Debate-derived open questions (added by the adjudicatio] Q-43 | Does the shared repair step keep every existing pin? C-
37. [9.10 Debate-derived open questions (added by the adjudicatio] Q-44 | What does acceptance mean while the identity check read
38. [9.10 Debate-derived open questions (added by the adjudicatio] Q-45 | Does the CRITICAL floor cover MAJOR? C-02's floor appli
39. [9.10 Debate-derived open questions (added by the adjudicatio] Q-46 | Which caller makes gateway panels reachable? The ship-n
40. [9.10 Debate-derived open questions (added by the adjudicatio] Q-47 | C-01 shape details: how anchor status reaches the ### L
41. [9.10 Debate-derived open questions (added by the adjudicatio] Q-48 | Where does a regressed non-blocking row appear? A valid
42. [9.10 Debate-derived open questions (added by the adjudicatio] Q-49 | Which signal do exit-code-only callers use? Empty brief
43. [9.10 Debate-derived open questions (added by the adjudicatio] Q-50 | C-02 specification gaps: the pending_new_sha256 wedge w
44. [9.10 Debate-derived open questions (added by the adjudicatio] Q-51 | Do findings of a reviewer whose block is invalid count 
45. [9.10 Debate-derived open questions (added by the adjudicatio] Q-52 | C-03 specification gaps: a refusal records nothing, the
46. [9.10 Debate-derived open questions (added by the adjudicatio] Q-53 | C-04 helper and shadow details (15 MEDIUM invariants: w
47. [9.10 Debate-derived open questions (added by the adjudicatio] Q-54 | Does the C-05 effect rule survive Stage 10.5? Stage 10.
48. [9.10 Debate-derived open questions (added by the adjudicatio] Q-55 | How is reach measured and the replay scored? The only a
49. [9.10 Debate-derived open questions (added by the adjudicatio] Q-56 | Which fields does an engine switch change, and what do 
50. [9.10 Debate-derived open questions (added by the adjudicatio] Q-57 | C-05 details: a call-site depth flag is not "pin-safe" 
51. [9.10 Debate-derived open questions (added by the adjudicatio] Q-58 | Can a blocking line be lost silently across rounds unde
52. [9.10 Debate-derived open questions (added by the adjudicatio] Q-59 | Can the re-ask run in reflect as written? cluster_cmd a
53. [9.10 Debate-derived open questions (added by the adjudicatio] Q-60 | C-06 details and unresolved points: the manifest comple
54. [9.10 Debate-derived open questions (added by the adjudicatio] Q-61 | Does the ship-now dispatch set close the A-r3 collapse 
55. [9.10 Debate-derived open questions (added by the adjudicatio] Q-62 | C-07 details and unresolved points: a class-word bindin
56. [9.10 Debate-derived open questions (added by the adjudicatio] Q-63 | Is the transcript adapter of C-08 workable on real tran
57. [9.10 Debate-derived open questions (added by the adjudicatio] Q-64 | Are the C-08 gates and consumers wired in the right ord
58. [9.10 Debate-derived open questions (added by the adjudicatio] Q-65 | Does the C-08 hybrid close refusal rows and cost? The r
59. [9.10 Debate-derived open questions (added by the adjudicatio] Q-66 | C-08 details and open points: stale orchestrator_snapsh
60. [9.10 Debate-derived open questions (added by the adjudicatio] Q-67 | C-09 details: the process env against the workspace vie
61. [9.10 Debate-derived open questions (added by the adjudicatio] Q-68 | Where does the PR panel standing live across --resume? 
62. [9.10 Debate-derived open questions (added by the adjudicatio] Q-69 | Can the PR standing ever read present correctly? "Reque
63. [9.10 Debate-derived open questions (added by the adjudicatio] Q-70 | How are PR findings converted per cluster? AM-1 splits 
64. [9.10 Debate-derived open questions (added by the adjudicatio] Q-71 | C-10 details and unresolved points: no stale standing v
65. [9.10 Debate-derived open questions (added by the adjudicatio] Q-72 | How is a lens identity and a report path made unique in
66. [9.10 Debate-derived open questions (added by the adjudicatio] Q-73 | Are the C-11 hash and lens-line checks early enough? Th
67. [9.10 Debate-derived open questions (added by the adjudicatio] Q-74 | Does the C-11 oracle compare like with like? Arm 0 and 
68. [9.10 Debate-derived open questions (added by the adjudicatio] Q-75 | C-11 details and unresolved points: the oracle's permis
69. [9.10 Debate-derived open questions (added by the adjudicatio] Q-76 | C-12 design-note and trigger details: a home for the pr
70. [9.10 Debate-derived open questions (added by the adjudicatio] Q-77 | Who computes observed in the process-redesign row block
71. [9.10 Debate-derived open questions (added by the adjudicatio] Q-78 | When does the built-now process-redesign set examine an
72. [9.10 Debate-derived open questions (added by the adjudicatio] Q-79 | X-13 details and open points: the orchestrator-assemble
73. [9.10 Debate-derived open questions (added by the adjudicatio] Q-80 | Is the X-14 rule pre-registered in a way that binds? A 
74. [9.10 Debate-derived open questions (added by the adjudicatio] Q-81 | Can the X-14 verifier and judge be gamed or fooled by a
75. [9.10 Debate-derived open questions (added by the adjudicatio] Q-82 | What is the unit of analysis of the X-14 metric? The 71
76. [9.10 Debate-derived open questions (added by the adjudicatio] Q-83 | How does the verifier read the C-06 keys? C-06 adds rep
77. [9.10 Debate-derived open questions (added by the adjudicatio] Q-84 | What is the acceptance metric for use cases other than 
78. [9.10 Debate-derived open questions (added by the adjudicatio] Q-85 | Does any X-14 gate bite the failure classes it names? A
79. [9.10 Debate-derived open questions (added by the adjudicatio] Q-86 | X-14 details and open points: ledgers before and after 
80. [9.10 Debate-derived open questions (added by the adjudicatio] Q-87 | Is H+ behaviour-preserving, and is the Stage 7 boundary
81. [9.10 Debate-derived open questions (added by the adjudicatio] Q-88 | X-15 details and unresolved points: ValidationReport.md
82. [9.10 Debate-derived open questions (added by the adjudicatio] Q-89 | OWNER-DECISION: does Medium block in the tasklist modul
83. [9.10 Debate-derived open questions (added by the adjudicatio] Q-90 | OWNER-DECISION: may panel findings drive a push in PR r
84. [9.10 Debate-derived open questions (added by the adjudicatio] Q-91 | OWNER-DECISION: Q3 of the rf-qa first change: are the /
85. [9.10 Debate-derived open questions (added by the adjudicatio] Q-92 | OWNER-DECISION: harness and Tier G ownership: who owns 
86. [9.10 Debate-derived open questions (added by the adjudicatio] Q-93 | OWNER-DECISION: plugin delivery for the panel, reflect,
87. [Codebase Research] .dev/tasks/to-do/TASK-RESEARCH-review-panel-run2-202611 | Finding contract: v1 anchor quotes, v2 path:line citati
88. [Codebase Research] .dev/tasks/to-do/TASK-RESEARCH-review-panel-run2-202611 | Merge, ledger and verdict semantics
89. [Codebase Research] .dev/tasks/to-do/TASK-RESEARCH-review-panel-run2-202611 | Dispatch, model identity and tiers
90. [Codebase Research] .dev/tasks/to-do/TASK-RESEARCH-review-panel-run2-202611 | Input delivery and reviewer brief (what the core must e
91. [Codebase Research] .dev/tasks/to-do/TASK-RESEARCH-review-panel-run2-202611 | Reflect's two Tier-2 engines (swarm engine vs skill pan
92. [Codebase Research] .dev/tasks/to-do/TASK-RESEARCH-review-panel-run2-202611 | E1 evidence, graded (15 pilot and 15 combo shadow runs,
93. [Codebase Research] .dev/tasks/to-do/TASK-RESEARCH-review-panel-run2-202611 | E2 evidence, graded (tasklist review-panel study)
94. [Codebase Research] .dev/tasks/to-do/TASK-RESEARCH-review-panel-run2-202611 | Collaboration designs F1-F7 and r1-r5
95. [Codebase Research] .dev/tasks/to-do/TASK-RESEARCH-review-panel-run2-202611 | Process redesign (Sweep Sheet, Recipe Ledger, class car
96. [Codebase Research] .dev/tasks/to-do/TASK-RESEARCH-review-panel-run2-202611 | Consumers sc:tasklist, sc:workflow and reflect UC-1
97. [Codebase Research] .dev/tasks/to-do/TASK-RESEARCH-review-panel-run2-202611 | Consumers for spec review (Review Loop, brainstorm, des
98. [Codebase Research] .dev/tasks/to-do/TASK-RESEARCH-review-panel-run2-202611 | Future uses: PR code review and rf-qa replacement
99. [Codebase Research] .dev/tasks/to-do/TASK-RESEARCH-review-panel-run2-202611 | E3 variants and experiments (the #346 loop, installed-o
100. [Codebase Research] .dev/tasks/to-do/TASK-RESEARCH-review-panel-run2-202611 | Telemetry, manifest, run record, cost and memory policy
101. [Codebase Research] .dev/tasks/to-do/TASK-RESEARCH-review-panel-run2-202611 | Evaluation governance (acceptance evidence for a unifie
102. [Codebase Research] .dev/tasks/to-do/TASK-RESEARCH-review-panel-run2-202611 | De-duplicated defect register
103. [Codebase Research] .dev/tasks/to-do/TASK-RESEARCH-review-panel-run2-202611 | Repository constraints and branching
104. [Codebase Research] .dev/tasks/to-do/TASK-RESEARCH-review-panel-run2-202611 | Value ledger for scope slices 01 and 02
105. [Codebase Research] .dev/tasks/to-do/TASK-RESEARCH-review-panel-run2-202611 | Value ledger for scope slices 03 and 04 (E2 study repor
106. [Codebase Research] .dev/tasks/to-do/TASK-RESEARCH-review-panel-run2-202611 | Value ledger for scope slices 05 and 06 (the two E2 bra
107. [Codebase Research] .dev/tasks/to-do/TASK-RESEARCH-review-panel-run2-202611 | Value ledger for scope slices 07 and 08 (E2 collaborati
108. [Codebase Research] .dev/tasks/to-do/TASK-RESEARCH-review-panel-run2-202611 | Value ledger for scope slices 09 and 10 (review package
109. [Codebase Research] .dev/tasks/to-do/TASK-RESEARCH-review-panel-run2-202611 | Value ledger for scope slices 11 and 12 (E1 evidence ar
110. [Scope Slices] .dev/tasks/to-do/TASK-RESEARCH-review-panel-run2-202611 | Run1-vs-run2 comparison and per-run notes
111. [Scope Slices] .dev/tasks/to-do/TASK-RESEARCH-review-panel-run2-202611 | E2 original study: reports and tooling
112. [Scope Slices] .dev/tasks/to-do/TASK-RESEARCH-review-panel-run2-202611 | E2 original study: analyses and audits
113. [Scope Slices] .dev/tasks/to-do/TASK-RESEARCH-review-panel-run2-202611 | Panel-collaboration brainstorm
114. [Scope Slices] .dev/tasks/to-do/TASK-RESEARCH-review-panel-run2-202611 | Panel-process-redesign brainstorm
115. [Scope Slices] .dev/tasks/to-do/TASK-RESEARCH-review-panel-run2-202611 | Collaboration packages r1-move-radar and r2-idle-shift-
116. [Scope Slices] .dev/tasks/to-do/TASK-RESEARCH-review-panel-run2-202611 | Collaboration packages r3-axis-flip-challenge, r4-flag-
117. [Scope Slices] .dev/tasks/to-do/TASK-RESEARCH-review-panel-run2-202611 | Review package code (E3 base plus E1 additions)
118. [Scope Slices] .dev/tasks/to-do/TASK-RESEARCH-review-panel-run2-202611 | The reflect side (E1)
119. [Scope Slices] .dev/tasks/to-do/TASK-RESEARCH-review-panel-run2-202611 | E1 evidence artifacts (shadow-run and model-combination
120. [Scope Slices] .dev/tasks/to-do/TASK-RESEARCH-review-panel-run2-202611 | E3 loop, installed-only variants, consumers
121. [Web Research] .dev/tasks/to-do/TASK-RESEARCH-review-panel-run2-202611 | Claude Code headless and hook semantics (hooks in claud
122. [Web Research] .dev/tasks/to-do/TASK-RESEARCH-review-panel-run2-202611 | Git branch-name hierarchy (ref path conflicts) and stac
123. [Web Research] .dev/tasks/to-do/TASK-RESEARCH-review-panel-run2-202611 | Finding-schema standards (SARIF, reviewdog) and review-
124. [Synthesis Files] .dev/tasks/to-do/TASK-RESEARCH-review-panel-run2-202611 | Overlap matrix
125. [Synthesis Files] .dev/tasks/to-do/TASK-RESEARCH-review-panel-run2-202611 | Target and gaps
126. [Synthesis Files] .dev/tasks/to-do/TASK-RESEARCH-review-panel-run2-202611 | External findings
127. [Synthesis Files] .dev/tasks/to-do/TASK-RESEARCH-review-panel-run2-202611 | Options
128. [Synthesis Files] .dev/tasks/to-do/TASK-RESEARCH-review-panel-run2-202611 | Conflict log
129. [Synthesis Files] .dev/tasks/to-do/TASK-RESEARCH-review-panel-run2-202611 | Recommendation and architecture
130. [Synthesis Files] .dev/tasks/to-do/TASK-RESEARCH-review-panel-run2-202611 | Value inventory (Section 8.1)
131. [Synthesis Files] .dev/tasks/to-do/TASK-RESEARCH-review-panel-run2-202611 | Sequence and gates
132. [Synthesis Files] .dev/tasks/to-do/TASK-RESEARCH-review-panel-run2-202611 | Open Questions and Evidence Trail (this file)
133. [Conflict Debates] ledger-clearing-and-verdict-authority (C-02) | .dev/tasks/to-do/TASK-RESEARCH-review-panel-run2-202611
134. [Conflict Debates] merge-verdict-policy-and-quorum (C-03) | .dev/tasks/to-do/TASK-RESEARCH-review-panel-run2-202611
135. [Conflict Debates] reflect-tier2-engine-composition (C-04) | .dev/tasks/to-do/TASK-RESEARCH-review-panel-run2-202611
136. [Conflict Debates] consumer-entry-effect-and-delivery (C-05) | .dev/tasks/to-do/TASK-RESEARCH-review-panel-run2-202611
137. [Conflict Debates] limits-repair-policy (C-06) | .dev/tasks/to-do/TASK-RESEARCH-review-panel-run2-202611
138. [Conflict Debates] dispatch-and-launch-mechanism (C-07) | .dev/tasks/to-do/TASK-RESEARCH-review-panel-run2-202611
139. [Conflict Debates] run-record-and-served-model-capture (C-08) | .dev/tasks/to-do/TASK-RESEARCH-review-panel-run2-202611
140. [Conflict Debates] panel-resolution-and-tier-source (C-09) | .dev/tasks/to-do/TASK-RESEARCH-review-panel-run2-202611
141. [Conflict Debates] pr-review-wire-format-and-slot (C-10) | .dev/tasks/to-do/TASK-RESEARCH-review-panel-run2-202611
142. [Conflict Debates] rfqa-first-step-and-readonly-scope (C-11) | .dev/tasks/to-do/TASK-RESEARCH-review-panel-run2-202611
143. [Conflict Debates] collaboration-exchange-capability (C-12) | .dev/tasks/to-do/TASK-RESEARCH-review-panel-run2-202611
144. [Conflict Debates] process-redesign-modules (X-13 = C-13) | .dev/tasks/to-do/TASK-RESEARCH-review-panel-run2-202611
145. [Conflict Debates] eval-acceptance-and-harness-owner (X-14 = C-14) | .dev/tasks/to-do/TASK-RESEARCH-review-panel-run2-202611
146. [Conflict Debates] tasklist-medium-and-fidelity-vocab (X-15 = C-15) | .dev/tasks/to-do/TASK-RESEARCH-review-panel-run2-202611
147. [Conflict debate artifacts] ledger-clearing-and-verdict-authority/ | ADJUDICATION-RESULT.md, merged-ledger-clearing-and-verd
148. [Conflict debate artifacts] merge-verdict-policy-and-quorum/ | ADJUDICATION-RESULT.md, merged-output.md, proposal-a.md
149. [Conflict debate artifacts] reflect-tier2-engine-composition/ | ADJUDICATION-RESULT.md, merged-output.md, proposal-a.md
150. [Conflict debate artifacts] consumer-entry-effect-and-delivery/ | ADJUDICATION-RESULT.md, merged-output.md, proposal-a.md
151. [Conflict debate artifacts] limits-repair-policy/ | ADJUDICATION-RESULT.md, merged-output.md, proposal-a.md
152. [Conflict debate artifacts] dispatch-and-launch-mechanism/ | ADJUDICATION-RESULT.md, merged-dispatch-and-launch-mech
153. [Conflict debate artifacts] run-record-and-served-model-capture/ | ADJUDICATION-RESULT.md, merged-run-record-and-served-mo
154. [Conflict debate artifacts] panel-resolution-and-tier-source/ | ADJUDICATION-RESULT.md, merged-panel-resolution-and-tie
155. [Conflict debate artifacts] pr-review-wire-format-and-slot/ | ADJUDICATION-RESULT.md, merged-output.md, proposal-a.md
156. [Conflict debate artifacts] rfqa-first-step-and-readonly-scope/ | ADJUDICATION-RESULT.md, merged-output.md, proposal-a.md
157. [Conflict debate artifacts] collaboration-exchange-capability/ | ADJUDICATION-RESULT.md, merged-collaboration-exchange-c
158. [Conflict debate artifacts] process-redesign-modules/ | ADJUDICATION-RESULT.md, merged-output.md, proposal-a.md
159. [Conflict debate artifacts] eval-acceptance-and-harness-owner/ | ADJUDICATION-RESULT.md, merged-output.md, proposal-a.md
160. [Conflict debate artifacts] tasklist-medium-and-fidelity-vocab/ | ADJUDICATION-RESULT.md, merged-output.md, proposal-a.md
161. [QA Reports] .dev/tasks/to-do/TASK-RESEARCH-review-panel-run2-202611 | Severity grading override (owner decision A, 2026-11-14
162. [QA Reports] .dev/tasks/to-do/TASK-RESEARCH-review-panel-run2-202611 | Phase 2 output inventory (Step 3.1)
163. [QA Reports] .dev/tasks/to-do/TASK-RESEARCH-review-panel-run2-202611 | Gate 1 completeness verification, partition A
164. [QA Reports] .dev/tasks/to-do/TASK-RESEARCH-review-panel-run2-202611 | Gate 1 completeness verification, partition B
165. [QA Reports] .dev/tasks/to-do/TASK-RESEARCH-review-panel-run2-202611 | Gate 1 completeness verification, partition C
166. [QA Reports] .dev/tasks/to-do/TASK-RESEARCH-review-panel-run2-202611 | Gate 1 cross-validation, partition A (research files 01
167. [QA Reports] .dev/tasks/to-do/TASK-RESEARCH-review-panel-run2-202611 | Gate 1 cross-validation, partition B (research files 09
168. [QA Reports] .dev/tasks/to-do/TASK-RESEARCH-review-panel-run2-202611 | Gate 1 cross-validation, partition C
169. [QA Reports] .dev/tasks/to-do/TASK-RESEARCH-review-panel-run2-202611 | Research gate, evidence-quality lens, partition A
170. [QA Reports] .dev/tasks/to-do/TASK-RESEARCH-review-panel-run2-202611 | Research gate, evidence-quality lens, partition B
171. [QA Reports] .dev/tasks/to-do/TASK-RESEARCH-review-panel-run2-202611 | Research gate, evidence-quality lens, partition C
172. [QA Reports] .dev/tasks/to-do/TASK-RESEARCH-review-panel-run2-202611 | Research gate, gap-detection lens, partition A
173. [QA Reports] .dev/tasks/to-do/TASK-RESEARCH-review-panel-run2-202611 | Research gate, gap-detection lens, partition B
174. [QA Reports] .dev/tasks/to-do/TASK-RESEARCH-review-panel-run2-202611 | Research gate, gap-detection lens, partition C
175. [QA Reports] .dev/tasks/to-do/TASK-RESEARCH-review-panel-run2-202611 | Research qualitative review, research-depth lens, parti
176. [QA Reports] .dev/tasks/to-do/TASK-RESEARCH-review-panel-run2-202611 | Research qualitative review, research-depth lens, parti
177. [QA Reports] .dev/tasks/to-do/TASK-RESEARCH-review-panel-run2-202611 | Research qualitative review, research-depth lens, parti
178. [QA Reports] .dev/tasks/to-do/TASK-RESEARCH-review-panel-run2-202611 | Gate 1 review 1, consolidated findings
179. [QA Reports] .dev/tasks/to-do/TASK-RESEARCH-review-panel-run2-202611 | Gate 1 fix log, fix cycle 1
180. [QA Reports] .dev/tasks/to-do/TASK-RESEARCH-review-panel-run2-202611 | Gate 1 fix verification, content, cycle 1
181. [QA Reports] .dev/tasks/to-do/TASK-RESEARCH-review-panel-run2-202611 | Gate 1 fix verification, structural, cycle 1
182. [QA Reports] .dev/tasks/to-do/TASK-RESEARCH-review-panel-run2-202611 | Gate 1 review 2, consolidated findings (fix cycle 2 inp
183. [QA Reports] .dev/tasks/to-do/TASK-RESEARCH-review-panel-run2-202611 | Gate 1 fix log, fix cycle 2
184. [QA Reports] .dev/tasks/to-do/TASK-RESEARCH-review-panel-run2-202611 | Gate 1 fix verification, content, cycle 2
185. [QA Reports] .dev/tasks/to-do/TASK-RESEARCH-review-panel-run2-202611 | Gate 1 fix verification, structural, cycle 2
186. [QA Reports] .dev/tasks/to-do/TASK-RESEARCH-review-panel-run2-202611 | Task integrity, phase-structure lens
187. [QA Reports] .dev/tasks/to-do/TASK-RESEARCH-review-panel-run2-202611 | Task integrity, b2-self-containment lens
188. [QA Reports] .dev/tasks/to-do/TASK-RESEARCH-review-panel-run2-202611 | Task-file validation (A.10), cycle 1, consolidated find
189. [QA Reports] .dev/tasks/to-do/TASK-RESEARCH-review-panel-run2-202611 | Task-file validation, fix log, cycle 1
190. [QA Reports] .dev/tasks/to-do/TASK-RESEARCH-review-panel-run2-202611 | Task-file validation, fix verification, cycle 1
191. [QA Reports] .dev/tasks/to-do/TASK-RESEARCH-review-panel-run2-202611 | Task integrity, task-research-alignment lens
192. [QA Reports] .dev/tasks/to-do/TASK-RESEARCH-review-panel-run2-202611 | A.10.25 research-alignment fix log
193. [QA Reports] .dev/tasks/to-do/TASK-RESEARCH-review-panel-run2-202611 | A.10.25 alignment fix verification
194. [QA Reports] .dev/tasks/to-do/TASK-RESEARCH-review-panel-run2-202611 | Task qualitative, qa-gate-sufficiency lens
195. [QA Reports] .dev/tasks/to-do/TASK-RESEARCH-review-panel-run2-202611 | Task qualitative, operational-correctness lens
196. [QA Reports] .dev/tasks/to-do/TASK-RESEARCH-review-panel-run2-202611 | A.10.5 qualitative fix log, cycle 1
197. [QA Reports] .dev/tasks/to-do/TASK-RESEARCH-review-panel-run2-202611 | A.10.5 qualitative fix log, cycle 2 (last cycle)
198. [QA Reports] .dev/tasks/to-do/TASK-RESEARCH-review-panel-run2-202611 | A.10.5 fix verification, structure and regression, cycl
199. [QA Reports] .dev/tasks/to-do/TASK-RESEARCH-review-panel-run2-202611 | A.10.5 fix verification, operational and gate semantics
200. [QA Reports] .dev/tasks/to-do/TASK-RESEARCH-review-panel-run2-202611 | A.10.5 fix verification, structure and regression, cycl
201. [QA Reports] .dev/tasks/to-do/TASK-RESEARCH-review-panel-run2-202611 | A.10.5 fix verification, operational and gate semantics

COUNT synth-10-questions-evidence.md: 201


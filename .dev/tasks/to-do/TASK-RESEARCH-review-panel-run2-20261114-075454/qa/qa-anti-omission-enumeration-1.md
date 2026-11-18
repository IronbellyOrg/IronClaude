# Anti-omission enumeration 1 (Gate 5, agent 1)

Report checked: RESEARCH-REPORT-review-panel-unification-run2.md (5,098 lines)
Date: 2026-11-14
Grading: qa/grading-override.md applies.
Status: Complete

Format: one numbered list of distinct findings per assigned file; each list ends with `COUNT <file name>: <n>`.

## research/01-overlap-capability-matrix.md
Method: each finding was searched in the report by key terms (not by id); representation is mostly in Section 2.9 (report lines 830-1110), 2.1, 4.x and 6.x. Hits counted by case-insensitive fixed-string grep over the report.

1. E2 changed no product code (src/tests diff empty 4a22d74..6c09843 and ec259f1..tip; 4 commits 0 files) -> REPRESENTED (report 2.2, 4.x; "#518"/E2-no-code hits, line 148, 1009).
2. snap.py writes into E1's evidence tree (comboD-r1 input-snapshot.yaml; hash formula identical, inference [UNVERIFIED]) -> REPRESENTED (lines 278, 339).
3. drift-b3.py read-only and rlog-r3.sh write into E1 tree; exactly three files reference brainstorm-reflect-panel; owner decision on removal open -> REPRESENTED (278, 341).
4. #519 changes 17 cli/review + 22 tests/review files; #518 changes 0 + 1; E2 "#519 + #518" attribution CODE-CONTRADICTED; 40 files check -> REPRESENTED (147-148, 1009).
5. cli/reflect Python consumes no tier JSON/panel code (only main.py:568 hit); panel_lint reads merged-verdict.yaml -> REPRESENTED (186, 195, 51 panel_lint hits).
6. SKILL.md shadow engine: --t2-engine legacy|shadow, `panel` rejected "ships in Stage 3", 10 shadow steps, UC-1 only -> REPRESENTED (164-167, 718).
7. E2 contrast "reflect has no panel/tier code": CODE-CONTRADICTED for the product, verified for the code-driven path; Q9 three registries -> REPRESENTED (Section 4.3 / 2.1).
8. Reflect profile accepts launch sonnet/opus/haiku only; gateway `launch: {}`; non-Claude dispatch absent in shadow path -> REPRESENTED (matrix row Dispatch, C-8).
9. Two E1 Tier 2 execution paths (prompt vs code) share nothing; kernel wired only to prompt path; panel_lint L1/L2 would fail a code-path contract -> REPRESENTED (1255).
10. Probe P-a: findings.annotate KeyError 'anchor' on citation-only findings -> REPRESENTED (545, 940).
11. Probe P-b: calibrated_confidence valid in v1, rejected in v2 -> REPRESENTED (384, 406; 22 hits).
12. Probe P-c: 200/300/200 whole-finding drop in v2 as in v1 -> REPRESENTED (matrix rows, shared defects).
13. Probe P-d: refs_norm loses T01.02 task ids; cluster.py inherits -> REPRESENTED (506, 518, 545, 871).
14. Probe P-e: snapshot hash formula identity -> REPRESENTED (339).
15. _REF_TOKEN regex scope and "limits inherited" imprecision (mechanism inherited, numbers restated as literals) -> REPRESENTED (Section 2.5 / corrected claims, line 3055+).
16. v1 anchor-only findings parse in v2 but get fp None and only singleton clusters -> REPRESENTED (cluster rows, 874).
17. Matrix of 15 capabilities x E1/E2/E3s/E3i with classes (identical cells few: id regex, v1 grammar, cap 3, E2 uses merge unchanged) -> REPRESENTED (Section 2.9, lines 830-1110).
18. "absent" label added as fifth class; E3 split into E3s/E3i -> REPRESENTED (2.9 legend).
19. Finding schema: E1 v2 superset (+7 fields), conflicts C-1/C-2; E2 uses v1 and unknown-key acceptance for class/probe/src/origin; E3i three more grammars -> REPRESENTED (2.9 rows 1, 868-871).
20. Ids/fingerprint: v1 fp vs v2 fp conflict; E2 served-model audit OBS/MODEL_OK; bug H2 expected_model overwritten after ladder step -> REPRESENTED (286, 312, 738).
21. E3s telemetry model_observed has no producer; only append_record caller is manual CLI -> REPRESENTED (2.9 row 12).
22. E3i ids R<N>.<j>, SCHEMA=1 int, body_sha256 tamper check -> REPRESENTED (516, 871-872).
23. Merge: E1 shadow merge is legacy Mode A debate; cluster/verify-citations telemetry only -> REPRESENTED (2.1, 2.9 row 3).
24. E2 audit-D measured merge drops (92 dropped, 49 blocking) -> REPRESENTED (873, 1027).
25. merge_round semantics (first-row break, blocking=any, severity max, refuse only when no valid block) -> REPRESENTED (2.5, 2.9).
26. E1 cluster_v2: SPAN_TOLERANCE 3, chained flag, resolved citations only; E2 83 mega-clusters, 195 of 1,398 chained -> REPRESENTED (874).
27. v1 same_defect union-find with no chain guard -> REPRESENTED (2.9 row 4).
28. Citation verification: review-precheck/1, never drops, quote-not-found advisory; E2 anchor fidelity 91.4% (46 rows/13 blocking missing); E3s first-occurrence locate; anchor_status read by nothing; E3i anchor once -> REPRESENTED (875, 339, 1177).
29. Verdict models: 0.75/0.60 convergence vs derive_verdict 0.80 degrade (C-6); E3 any-blocking-row fails; exit codes 0/10/11; E3i script verdict -> REPRESENTED (184-192, 881, 1151).
30. Ledger/rounds: E1 has none; `reflect run --fix` loop dormant (engine A emits no remediation_* pointer); E3 review-ledger/1 statuses cap 3; E3i second ledger different statuses -> REPRESENTED (147, 183, 199, 882).
31. Panel/tier: E1 reflect profile superset; E2 EXCLUDE_MODELS glm-5.3 Qwen3.8-max and ladder in script; tiers file lists both models, no muse-ember; distinct_across_slots re-admits duplicates; anthropic-only stand-in -> REPRESENTED (883, 944, 598, 1032).
32. Dispatch: E2 `claude -p` raw ids, 3000 s timeout, 2 attempts then ladder, aliases serve only first model; E3 product does not dispatch -> REPRESENTED (884).
33. Brief: three-section reviewer-spec; E3 prompts file; E2 wrapper; E3i variants on pre-#478/#479 base (PR #427) -> REPRESENTED (478, 885).
34. Calibration: blind confidence-calibrator, 6-vs-5 dimension rubric mismatch; E3i finding-grader -> REPRESENTED (891, 1033).
35. Run record: review-panel-manifest/1, contract telemetry, review-telemetry/1 strata hard-coded sonnet/haiku, E2 meta/cost/score -> REPRESENTED (2.9 row 12; C-10).
36. Memory: per-project expiring memory; shadow runs append deviation-patterns (contamination channel) -> REPRESENTED (249, 270, 893, 1040).
37. Eval harness: E1 5x3 combos no ground truth, shared fixture sha; E2 ground truth/blind judge, 96 combo dirs, r1-r5 py counts; E3s tests only; E3i phase5 bundle 7,909 lines -> REPRESENTED (894, 300; "19 RESULT.md" count itself not in report, immaterial).
38. Collaboration: E1 3.2% unchained multi-reviewer clusters; E2 five collab redesigns (F1/F3/F4/F6/F7) + two process redesigns 46 REQs; E3 sequential loop -> REPRESENTED (895, 356, 390, 412).
39. Conflict register C-1..C-12 -> REPRESENTED (2.9 + 4.3).
40. Shared defects: whole-finding drop, T01.02, lint_cmd/estimate_cmd registered but absent -> REPRESENTED (488, 960).
41. Installed variants re-implement stdlib-only, sizes 2668/2050/1740/1131, not installable -> REPRESENTED (847, 987).
42. Stale documentation list (9 entries) -> REPRESENTED in part (SKILL.md:592->640, manifest.md "never pushed", PLAN.md "designed, NOT run", docstring, plugin spec-panel) -> see report 9.x and 2.x; minor if any single entry absent.
43. Slice 03 "95 combo dirs" vs 96 -> REPRESENTED (337 vs 300).
44. Design questions for the core (location type, verdict owner, one ledger, raw-model dispatch) -> REPRESENTED (Section 6 axes).
COUNT 01-overlap-capability-matrix.md: 44

## research/02-finding-contract.md
1. v1 findings-v1 closed vocabularies (SEVERITIES, 6 CATEGORIES), id grammar `^[A-Za-z0-9][A-Za-z0-9._-]{0,15}$`, `_check_flat` unit = characters after whitespace flattening -> REPRESENTED (report 2.5, 2.9 rows; 12..200 hits 538, 870, 940).
2. `_check_finding` rule order; anchor 12..200 required, anchor2, refs <= 8, claim <= 300 no minimum -> REPRESENTED (2.9 / 6.2).
3. No unknown-key check in v1; parse_block carries whole obj -> REPRESENTED (384, 186; 34 "unknown key" hits).
4. Drop contract: one finding line lost, block `ok` False; heading missing / >1 block / unclosed also not ok -> REPRESENTED (2.5, 6.2).
5. `_REF_TOKEN`, `_HEAD_FINDINGS`, `_FENCE` definitions -> REPRESENTED (545, 3055 area).
6. v2 shares one id grammar, category list, `_check_flat` with v1; limits restated as literals -> REPRESENTED (2.5, corrected claims 3055).
7. v2 `citations[]` object rules (ROLES plan/spec/source/test/diff/artifact; repo-relative path; `1<=line_start<=line_end`; optional quote 12..200) -> REPRESENTED (538, 2249).
8. finding needs anchor OR citations -> REPRESENTED (2.9).
9. `lens` (spec/reflect-pre/reflect-post) must match block lens; `deviation_class` required for reflect-post -> REPRESENTED (2.1/2.5).
10. `reflect_category` forces category and `blocking == (severity != MINOR)`; deviation needs deviation_class -> REPRESENTED (C-2 blocking rule, 2.9).
11. `coverage_rows`, `self_confidence`, `channel` validated; `calibrated_confidence` only rejected extra key -> REPRESENTED (384, 406).
12. v2 parse_block: no `prior` lines; complete/truncated/invalid; empty closed block complete only with coverage evidence -> REPRESENTED (2.5).
13. `V1_FIELDS` declared but unused (docstring + tests only) -> REPRESENTED (1372, 1415).
14. Open item (a): v2 does not reject `origin`/unknown keys (executed); only calibrated_confidence; function named `check_finding` not `_check_finding` -> REPRESENTED (384, 396).
15. No test asserts unknown-key acceptance; docstring more cautious than code -> REPRESENTED in part (docstring caution and "test pins calibrated_confidence only" at 384/2278); the "no test for origin" detail is MINOR.
16. `origin` carried but read by no cli/review module; a whitelist would break E2 tools -> REPRESENTED (2278, 384).
17. Open item (c): `T01.01` legal `_ID` but not `_REF_TOKEN`; executed findall result; `T1-2`, `T01-01` also missed -> REPRESENTED (545, 871; 15 hits).
18. `refs_norm` mechanics (anchor, anchor2, claim, refs; `_SECTION_REF` bare numbers; SHA- filter) -> REPRESENTED in part (SHA- 422, 545); `_SECTION_REF` detail not named (MINOR, no decision).
19. v1 effect: fingerprint disabled, span path within 3 lines when both ref sets empty -> REPRESENTED (874, 986).
20. v2 effect: cluster.annotate inherits loss; fingerprint ignores line numbers => same path + ref one defect at any distance -> REPRESENTED (545, 1239, 2193).
21. telemetry `_ID_TOKEN` is a plain string; `_ID_RE` compiles same pattern; ids_defined/cross_refs undercount; no SHA- filter -> REPRESENTED (506, 545, 1240, 1273).
22. Tasklist `T<PP>.<TT>` grammar source (sc-tasklist-protocol SKILL.md:340); no test exercises task ids -> REPRESENTED (545, 871).
23. Open item (b) unit table: 264 merges, 80 reviewer-level cases, 92 dropped lines (by reason 56/18/14/3/1 and per model), 49 blocking (24/14/10/1; 44 triples), 4 verdicts flipped vs verdict_flip 3 + 5 total-loss merges -> REPRESENTED (308, 329, 1242, 1516, 2322, 2323).
24. Unit mismatch 80 vs 92 (DEF-4) -> REPRESENTED (308, 547).
25. raw-minus-kept = 109 vs drop_model 92 (haiku 23 vs 7, grok 2 vs 1), cause [UNVERIFIED] -> REPRESENTED (339, 482).
26. Option table: truncate recovers <= 88/92 (95.7%) and 48/49 (98.0%); 4 non-length lines (3 bad severity, 1 refs-bad) not recoverable; prefix still locates; luna anchor fidelity 91.4% -> REPRESENTED (2225, 2334).
27. Reject-and-re-ask recovery unmeasured (Spike 5 not run; needs --resume; adds wall clock) -> REPRESENTED (547, 2382).
28. Keep-and-warn recovers nothing; today's warning is first-error-only stdout; ledger stores only block_ok -> REPRESENTED (2334, 2363).
29. v1 ledger keeps other lines, refuses only when no block ok; v2 cluster path skips whole reviewer (`invalid_reviewers`) so one bad line costs a reviewer; verify-citations still iterates invalid blocks -> REPRESENTED (543, 547: "whole reviewer").
30. Repair policy must sit before parse_block or parse_block made repair-aware -> REPRESENTED (2334/2363, 6.2).
31. E2 R-02 truncates as exact prefix and re-asks once vs E1 "orchestrator never edits/normalizes" with one bounded re-ask -> REPRESENTED (2363-2365).
32. Card format: reviewer-<N>.md, header lines persona/model_class/model, findings-v2 block, fenced yaml `calibration: per_finding`; `--calibration` sidecar overrides; calibration outside the line -> REPRESENTED (1134, 2250, 2288; `_embedded_calibration`/`--calibration` identifiers not named, MINOR).
33. Brief line (reviewer-spec.md:39) omits the 12..200 quote limit and reflect fields; v1 brief states only the anchor limit; findings_block_compliance_rate metric; shadow_exit reads `compliance` -> REPRESENTED (215, 243, 641 "compliance"; metric id name absent, MINOR).
34. card_convert: shapes, `refs` always [], no quote, claim cut to 297+`...`, id replaced by F<index>, MAX_REF_TEXT 200, 90% reference value with no gate, severity word map -> REPRESENTED (147-149, 697, 954, 2250; MAX_REF_TEXT/F<index> literal details absent, MINOR).
35. Citation roles have no task-row/AC/PR-hunk role; PR review has `diff` but no in_diff/original_line/thread id -> REPRESENTED (707, 1141).
36. Variant ledger comparison table (review_ledger/diffgate/stoprule: finding form, anchor length, uniqueness, unknown keys REJECTED in ledger and diffgate, who decides blocking, id grammars, location type) -> REPRESENTED (870-872, 2252, 441).
37. Ledger row fields (make_row), FROZEN_FIELDS includes `origin`, LIVE_STATUSES open/fixed/reopened vs v1, VERDICT_EXIT PASS 0/CONTINUE 10/ESCALATE 11/PENDING 12 vs v1 0/10/11, cap 3 both -> REPRESENTED in part (statuses, exit codes 881/1151); `FROZEN_FIELDS`/`PENDING 12` literals absent (MINOR).
38. NAME COLLISION `origin` (E2 own/peer vs ledger find/changed/outside/sweep vs diffgate full/changed/unchanged) -> REPRESENTED (384, 1243, 1340).
39. `panel-msg/1`: transport not finding, keys, kinds, 600 bytes, anchor exact substring, unknown keys rejected, forbidden keys, ember card exception -> REPRESENTED (384, 1169).
40. `origin` is a findings-line key, not a panel-msg key; r2 tagger, r3 combiner, r1 none, r4/r5 sidecar; anonymiser strips it -> REPRESENTED (384, 396, 398).
41. E2 own/peer tag lost at merge unless member record extended (ledger stores round, reviewer_id, fid, blocking) -> REPRESENTED (384, 2256, 2278).
42. E2 phase-2 id grammar P2-F<n>/P2X-F<n> fits _ID -> REPRESENTED (3742).
43. Three validators for three panel-msg kinds (C-07) -> REPRESENTED in part ([UNVERIFIED] by source; report 384/1169).
44. panel-msg 12..200 anchor same number, different contract (exact substring at post time) -> REPRESENTED (384).
45. Consolidated contract comparison table (limits, refs, citations, id grammar, unknown keys, violation cost) -> REPRESENTED (2.9, 6.2).
46. Gaps 1-9 ([UNVERIFIED] items: per-model split of 49 blocking drops mislabel, four flips, 109 vs 92, truncated anchor locate, re-ask recovery, stoprule unknown keys, r4/r5 D-1/D7, pr_submit models.py, task_variables) -> REPRESENTED in part (9.x gap lists; per-model-split mislabel at 308/329).
47. Design questions 11-13 (repair policy location; unknown keys open vs whitelist; fingerprint ignores line numbers) -> REPRESENTED (6.2 axis, 9.1).
48. Stale-doc list (findings_v2.py:15-22 anchor, `_check_finding` name in slices, X11 "seen to 135", slice 09 "not read", per-model drop figures unit, R-04 single contract) -> REPRESENTED in part (3055 corrected claims; rest minor tags).
COUNT 02-finding-contract.md: 48

## research/03-merge-ledger-verdict.md
1. Numbering: slice 09 "D-n" vs slice 01 "Dn" are different numberings -> REPRESENTED (549, 1379, 1441).
2. D-1 reproduced: resolved_check row cleared by absence (ledger.py:254-258), even by a reviewer who never saw it; variant A (3 of 3 finders, one empty-block newcomer clears) -> REPRESENTED (553, 647, 1247).
3. D-1 variant B: merge_round does not check doc_text equals apply_revision output; no new-text hash stored -> REPRESENTED (553, 1250, 3231).
4. D-1 variant C: invalid-block reviewer does not stop clearing; block_ok not read in clearing loop; ledger.py:112 docstring CODE-CONTRADICTED -> REPRESENTED (553, 1247, 1270).
5. Re-review panel resolves ONE reviewer (apply_to ["first"] on all 8 templates) -> REPRESENTED (561, 1247, 2399).
6. Test pins for D-1 (test_review_ledger.py:193-217, test_review_cli.py:274-292) -> REPRESENTED (1179, 1247, 1253).
7. Only evidence for "fixed" is a hunk touching the span plus silence; variant uses explicit per-row verify -> REPRESENTED (444, 882, 1138).
8. D-2 reproduced: one valid of N passes, exit 0; refusal only at 0 valid; round record has no quorum/completion field; ledger never reads manifest -> REPRESENTED (554, 1180, 1248).
9. Reviewer-typed blocking decides; CRITICAL with blocking=false passes; typed `verdict:` line is dead input; confidence never read -> REPRESENTED (555, 689, 939, 249).
10. Test pin test_one_valid_block_is_enough -> REPRESENTED (1179).
11. "no valid block anywhere" fail-closed vs "some valid" fail-open; findings_v2 COMPLETION_STATES -> REPRESENTED (554, 578, 1133).
12. D-11 reproduced: deferred row re-found as blocking stays deferred, PASS; defer has no status guard/owner/expiry; defer at cap flips ESCALATE to PASS -> REPRESENTED (556, 1165, 1181).
13. No test re-finds a deferred row (negative evidence) -> REPRESENTED in part (882, 942; test-gap fact MINOR).
14. D-13 stored verdict not derived; stale after revise; CLI exit 10 -> REPRESENTED (448, 557, 1137).
15. Three ways to leave the loop without a clean re-review (silence, lone reviewer, defer) -> REPRESENTED (1165, 1180).
16. X1: round 4 accepted after ESCALATE at round 3 (only n == len(rounds)+1 checked) -> REPRESENTED (558, 1165, 1182).
17. X2: row with missing anchor has span None, cannot reach resolved_check, stays blocking until escalation -> REPRESENTED (559, 875, 1254).
18. X3: `prior` line inert (prior_note only), silence still clears -> REPRESENTED (152, 560, 883).
19. Tests that encode defects (table of ~11 rows incl. D-3/D-4, D-6, reviewer re-classification, D-5 soft distinctness live7 = 1 Sonnet + 6 Haiku) -> REPRESENTED (1179, 1247, 1253; live7 6 Haiku see 2.6/2.8 hits).
20. Test-pin summary: 6 of 8 pins assert defect behaviour; fixes must rewrite tests together -> REPRESENTED (1253, 1179).
21. Defects were designed in (Codex P1 refusal comment, "an invalid review must never certify PASS") -> REPRESENTED in part (1247, 553); the comment origin is MINOR.
22. Installed variants re-implement, stdlib only, no cli/review reference, no shared vocabulary strings, only cap 3 shared -> REPRESENTED (847, 987, 1344).
23. Variant source of truth: installed-only + frozen bundle copies; `cmp`-identical per slice 12 [UNVERIFIED] -> REPRESENTED in part (Section 2.4).
24. Schema/grammar/locator/state-store table (CLI vs review_ledger vs stoprule vs diffgate; fcntl lock; body_sha256 tamper check; exit 6 replay mismatch) -> REPRESENTED (872, 3746, 448).
25. None of the variants is a multi-reviewer panel merge; value is verification discipline; port semantics, cannot import -> REPRESENTED (1138, 445).
26. CLI status machine table (open/resolved_check/resolved/regressed/deferred transitions) vs variant machine (open/fixed/verified/reopened/deferred) incl. cannot-verify, unanswered row forces ESCALATE -> REPRESENTED (443, 882, 942, 2394).
27. Variant deferred terminal for machine; headline_raw = U3 + W + O owner counting rule keeps deferred CRITICAL/MAJOR as open -> REPRESENTED (448, 454, 1165).
28. Verdict-authority table across 6 mechanisms (spec-panel prose fail-closed rule, CLI ledger, review_ledger decide/verdict_of, stoprule compute_verdict "silence never passes", diffgate prior blockers default open, reflect derive_verdict) -> REPRESENTED (445, 2395, 2440).
29. reflect derive_verdict: 4 states PASS 0/HALTED 10/DEGRADED 11/BLOCKED 2, 14 degraded triggers, reads contract fields not findings; DEGRADED concept fits partial-panel hole; reusable verdict shell fed from ledger -> REPRESENTED (160-203; 46 derive_verdict hits).
30. Threshold inconsistency 0.75 vs 0.80; code engine hard-codes merge_method by reviewer count, verification_ran False so PASS rests on defaults -> REPRESENTED (180, 196, 203, 184-192).
31. Design implications I-1..I-7 (explicit per-row answer, quorum over completion states, derive on read, deferred needs owner/reason/expiry, blocking authority, refuse round after ESCALATE and store new-text hash, rewrite pinned tests) -> REPRESENTED (1137-1139, 1165, 2399+, Section 6.4).
32. Gaps 1-10 (cmp not re-run, variant tests only in bundle, stoprule verify-transcript failed on real run, ensemble.py values from slice 10, quorum count undefined, who may defer, not reproduced D-3/D-4/D-12/D-28/D-30, pytest not run, numbering hazard) -> REPRESENTED in part (448, 480, 4706, 1133, 549).
33. Stale docs: ledger.py:112 docstring, ledger.py:351 defer docstring, contract.py header cites SKILL.md:754 (now 761/858), variant commands disjoint from master loop -> REPRESENTED (1270, 1288, 3304, 3420).
COUNT 03-merge-ledger-verdict.md: 33

## research/04-dispatch-identity-tiers.md
1. review-tiers.default.json content: 6 alias lists, 13 model ids / 9 classes, gateway `available all`, `stand_ins {}`, `launch {}`; anthropic-only stand-ins haiku; launch class words -> REPRESENTED (598-599, 610).
2. No `tier0` alias and no muse-ember in tier file; tier0 rule in validate_reflect_profile inert -> REPRESENTED (152, 598, 610).
3. Fable present in classes/anthropic-only, forbidden only by reflect profile -> REPRESENTED (152, 467, 599).
4. validate_reflect_profile and _check_reflect_resolution rules (tier0, Fable, classes entry, round_robin needs --sequence, <=3 slots/reviewers, launch in sonnet/opus/haiku) -> REPRESENTED (149, 152, 883).
5. `panel validate --kind panel` does not run reflect profile (bad template passes validate, fails resolve) -> REPRESENTED (152, 883, 1261).
6. Runtime: `--env gateway` refused with launch None error; anthropic-only resolves t1b/t4/t1a -> REPRESENTED (598-603, 884).
7. 3-reviewer cap means @live7 (7) must not reuse reflect profile -> REPRESENTED (883, 1060).
8. Product package only resolves, never launches (only subprocess is git rev-parse); alias strings data only -> REPRESENTED (603, 884, 1061).
9. E1 Claude-orchestrated dispatch by class word on Agent call; rotation N=2/N=3; shadow step 3 "dispatch is the legacy dispatch" -> REPRESENTED (621-635).
10. Agent frontmatter default `model: sonnet` for reflect-reviewer, confidence-calibrator, evidence-validator; rf-qa has no `model:` key -> REPRESENTED (201, 376, 621, 635).
11. Agent tool model enum only sonnet/opus/haiku/fable; cannot name tier2b/3/4 or non-first slot models -> REPRESENTED (635, 653, 884).
12. ccsession exports ANTHROPIC_DEFAULT_*_MODEL tier ids; shim serves first non-cooling model; haiku class -> gpt-6.1-sol (not Claude Haiku) -> REPRESENTED (615, 622, 629-631).
13. comboA-r1 stream log: sidechain served opus 58, sonnet 11, gpt-6.1-sol 16 -> REPRESENTED (598, 631, 640).
14. docs/reference/model-aliases.md:51 same-family edge case "not verified" -> REPRESENTED (649-655).
15. E1 code-driven engine: raw model ids over HTTP (OpenAICompatTransport, T2Model0N/T1Model0N pools); WorkerResult.model_id = requested id; response model never read -> REPRESENTED (181, 186, 259, 376).
16. _diversity: t2_model_class_diversity over requested ids; vendor table -> REPRESENTED (181, 193-194, 240).
17. Code engine has no tier-alias step / no executor-class exclusion [UNVERIFIED by me] -> REPRESENTED in part (Section 2.6; minor).
18. E2 harness `claude -p --model <raw id>` flags, timeout 3000, OBS/MODEL_OK, ladder overwrites $MODEL so a silent swap passes -> REPRESENTED (286, 312, 884, 738).
19. Tier aliases serve only first model; probe.json alias_findings (tier2->sol, tier2b->terra, tier3->glm, tier4->luna) -> REPRESENTED (598, 615, 630).
20. Raw ids still pass through shim named_fallback (serves later model on error); only claude -p identity check catches it -> REPRESENTED (632, 884, 2496).
21. Side-by-side dispatch table (unit named, reach non-first, tools, served model recorded, unit of model) -> REPRESENTED (2.6, 2.9 row 9).
22. Requested-side records: resolution JSON, card header model:, reviewer_models, panel_parity requested-vs-requested (never reads model_observed) -> REPRESENTED (211, 226, 240).
23. Served side: nothing in product code writes model_observed (telemetry SQL view only); prose-level model_observed header and identity_source observed vs requested-pinned -> REPRESENTED (638-639, 872).
24. Counts: identity_source observed in 1 of 15 combo contracts (C-r2), 13 of 13 pilot requested-pinned; 69 card files with model_observed over 11 of 15 dirs; S11 "every contract requested-pinned" CODE-CONTRADICTED -> REPRESENTED (639, 19 hits; "69 files" at 639).
25. comboE-r3 pin differs from served (sonnet class served haiku by design) -> REPRESENTED (278, 894).
26. resolvedModel in Agent result is the resolved request string not served; collapse detector but not identity proof -> REPRESENTED (639, 653, 1035).
27. E2 OBS check judged against overwritten $MODEL, fallback judged against itself -> REPRESENTED (286, 738).
28. E1 extract.py reviewer_requested_served pairing (logs untracked) -> REPRESENTED (270, 575, 588).
29. Dispatch-collapse counts: A-r3 only (3 reflect-reviewer calls with no model arg), 1 of 3 tier3-orchestrated, 0 of 12 tier1b; pilot 6 of 9 not re-derivable (/tmp/shadow-logs gone) -> REPRESENTED (238, 265, 640).
30. Pin-vs-served differences by design (haiku->sol x5, opus->luna D/E, sonnet->haiku E) -> REPRESENTED (638-640).
31. A-r3 contract reports calibrator_diversity full, identity_mismatch_suspected false while single model served: collapse invisible in every contract field -> REPRESENTED (238, 249, 265).
32. Tier data chain: Coder env aienv.d/defaults.sh, ccsession-models.json (181 lines, models_env slot names only), MODEL-TIERS.md, review-tiers.default.json, shim; only a COUNT test (test_review_panel_live7.py:92-98) ties them -> REPRESENTED (883, 953, 1063).
33. T2Model0N order dependence (test fixture order differs from live) -> REPRESENTED in part (643); minor.
34. muse-ember: T4Model04 in live env and CCSESSION_MODEL_ORDER but ccsession-models.json lists only T4Model01-03 so shim/tier walk cannot see it; owner order said slot 02 -> REPRESENTED (615, 647).
35. Tier 2b "Review-panel and fallback tier" is first dispatch slot of issue-worker-t3 and implement retry ladder, not cli/review -> REPRESENTED (645, 649, 1063).
36. T2bModel01 18 occurrences in 11 files (11 in 8 inside scope); definition ccsession-models.json:107; read generically + by name in retry.md:162,172; no panel code reads it; E2 run-2 note CODE-CONTRADICTED -> REPRESENTED (645, 883, 1011; per-file table not reproduced, immaterial).
37. panel.py select_env reads $T3Model01 only -> REPRESENTED (580, 615, 645).
38. muse-ember absent at HEAD in src/tests/docs/scripts/plugins/CHANGELOG/ccsession-models.json; present in E1 PLAN.md (absence note), E2 evidence, runtime env; E2 default panel "ember + 2x luna" names a model the tier file cannot resolve -> REPRESENTED (311, 314, 337, 647, 653).
39. CCSESSION_MODEL_ORDER only orders /model picker, not tier membership -> REPRESENTED (647).
40. Three class vocabularies (tier file classes 9; vendor substring table; SKILL.md {opus,sonnet,haiku,qwen,kimi,deepseek}); kimi/deepseek in no tier list; one owner for class/vendor needed -> REPRESENTED (194, 643, 952, 1262).
41. "Class diversity" defined three ways, all on requested values -> REPRESENTED (193-194, 240).
42. tier1a and tier1b both list claude-sonnet-5-5; failover could collapse opus-class and sonnet-class silently -> REPRESENTED (580, 598, 643).
43. E3 loop dispatch unspecified (document_review_loop_prompts.md:70); reflect scripts dispatch nothing -> REPRESENTED (635, 884, 1259; 169, 186, 229).
44. Resolution table (a)-(e) -> REPRESENTED (883-884 and Section 2.6).
45. Gaps 1-9 (pilot 6 of 9, r1/r2 launch models, Claude Code behaviour not in repo, ember slot, S10 facts, no pytest) -> REPRESENTED in part (640, 653, 4712 area).
46. Stale docs: MODEL-TIERS.md:44 wording changed; model-aliases.md:56 and :26-28; PLAN.md "NOT run"; tiers.json:26 note; README.md:447 moved +2 -> REPRESENTED in part (649, 1063, 1270; line-shift entries MINOR).
COUNT 04-dispatch-identity-tiers.md: 46

## research/05-input-delivery-brief.md
1. Review-loop brief has exactly five placeholders (CANDIDATE, BASELINE, PRIOR, N, IDS); no placeholder/role for a driving document; "against the requirements it states" -> REPRESENTED (402, 423, 1271 G-36).
2. Grading check welded into brief (Medium rule, "requirement the document never states" demoted to follow-up candidates) -> REPRESENTED (422, 436, 1272 G-37).
3. Findings block text in brief states only the anchor limit; no claim 300, refs 8, id 16, MINOR-not-blocking (B-2) -> REPRESENTED (1272).
4. "The verdict line stays the reviewer's verdict" - reviewers not told one blocking row fails the round (B-7) -> REPRESENTED (424, 565, 1272).
5. Review panel paragraph (panel resolve, merge, ledger revise); same brief per reviewer; never-clause narrowing -> REPRESENTED (635, 1259).
6. findings.py constants/regexes/_check_finding/parse_block recap; refs_norm probe: FR-8/AC-0.4/NFR-004/REQ-014/D-0012/R-001/P1 recognised; T03.02, T03.02.1, I7, B3, GT10, P12, S2.3, FR-RSR.9 not -> REPRESENTED (545, 3335, 1273).
7. findings_v2 shares vocabulary by import; ROLES include `source`; LENSES; REFLECT_CATEGORIES third vocabulary; PRIMARY_ROLES per lens table -> REPRESENTED (1273, 2212, 2275).
8. `_REF_TOKEN` duplicated as `telemetry._ID_TOKEN`; must be per-module pattern list -> REPRESENTED (506, 1240, 1273).
9. E2 run-reviewer.sh: candidate copied to /tmp/evalsb; source.md copied via hard-coded absolute SRC_EVAL with `|| true` (silent miss); BRIEF = /sc:spec-panel + first-review brief + rules paragraph; source.md never named in BRIEF -> REPRESENTED (285, 1271, 565).
10. Harness constants (sandbox path, source origin) -> input documents by role as data -> REPRESENTED (1273 row 12, 1271).
11. Defect table B-1..B-7 status at HEAD (B-1 open, B-2 open, B-3 open, B-4 open low, B-5 open, B-6 fixed in harness only, B-7 open) -> REPRESENTED (561, 565, 1272).
12. CB-1..CB-5 and collab H1-H4 status (CB-3 present; CB-2, CB-5 open; collab-H2 truncate open; H3/H4 not core) -> REPRESENTED (565, 1272).
13. No redesign brief wording or ledger-v1/panel-msg exists in shipped code (negative Grep) -> REPRESENTED (1272).
14. (e1) `unpassable-ac` is a harness-brief typo never shipped; survives as E2 ground-truth class name (mapping problem) -> REPRESENTED (292, 565, 1272, 1273).
15. Typo cost 15 dropped findings in one combo run [SLICE-ONLY] -> REPRESENTED in part (Section 2.2 audit figures); minor.
16. (e2) theory.py HARD set = {I5,I7,B7,B8,I6,B1,B2,B3,I4}; by-kind definition; includes B3/B7, excludes B5/I1/B6; uses gtproxy regex not blind judge -> REPRESENTED (1276, 565).
17. theory.md numbers (ember 0.25->0.22, luna flat, haiku 0.29->0.70, sonnet 0.46->0.74, grok 0.08->0.50; Spearman 0.64) -> PARTIALLY REPRESENTED: conclusion "unproven for ember/luna, contradicted for haiku/sonnet/grok" at 1276; the per-model figures and Spearman 0.64 not reproduced. Not decision-bearing (thinking-budget lever explicitly taken as no fact). MINOR (minor under grading override).
18. records_gt.json not committed so recomputation impossible; gtproxy.py hard-codes E2 worktree path -> REPRESENTED (1276, 4754; gtproxy name absent, minor).
19. Five brief families (review loop, E2 harness, reflect shadow, reflect code engine build_worker_prompt, tasklist fidelity prompt) and how each delivers input / whether a driving doc is delivered -> REPRESENTED (1271, 1274, 565).
20. Code-driven engine reviews tasklist without the spec; config.spec_path only reaches Tier-1 command line, ensemble.py never references it -> REPRESENTED (1271, 565, 4159).
21. Tasklist fidelity prompt: VALIDATION LAYERING GUARD, HIGH/MEDIUM/LOW, DEV-NNN, YAML frontmatter, no findings-v1; decide adopt vs leave outside -> REPRESENTED (1274, 3369).
22. card_convert resolves roles by file name (<id>.md/TASK-, source.md); "spec" vs "source.md" bridged only there -> REPRESENTED (1273 row 11, 2296).
23. Reflect brief line reviewer-spec.md:39 and citation roles narrowed to plan|spec vs six in v2 -> REPRESENTED (538, 2249).
24. panel.py has no brief/placeholder -> REPRESENTED in part (1152-1162); minor.
25. Spec-shape hard-codings table (12 rows: ref regex, section-ref, categories, placeholders, grading paragraph, telemetry strata, review kinds, doc metrics rfc2119, PRIMARY_ROLES, reflect cap, filename roles, E2 paths) -> REPRESENTED (1273 G-38, all 12 enumerated).
26. "One fact two copies" failure mode removed by generation (rows 1,3,7, placeholders) -> REPRESENTED (1272, 1152).
27. Core exposes per module (input manifest, missing-input rule, brief assembler with named blocks, category map, reference syntax, lens+role table, panel template caps, hash-frozen snapshot, schema choice, strata/doc metric hooks, reviewer-side effort record) -> REPRESENTED (1152, 1162, 1244, 1400, 1275).
28. Future consumers: PR code review roles diff/test and reflect-post-like lens; rf-qa replacement needs artifact role -> REPRESENTED (2936-3003, Section 6.11).
29. Reviewer-side effort record (observed model, thinking tokens, role opened; 161 of 665 source-blind) -> REPRESENTED (1275, 309, 339).
30. Gaps 1-9 (naming source.md effect unverified, D1 merge side, ledger.py:273, .claude mirror, thinking-budget recomputation, slice counts, tasklist fidelity decision, H1-H4 ambiguity, unread files) -> REPRESENTED in part (1271, 1274, 1276; ".claude mirror not searched" minor).
31. Stale doc: manifest.md "never pushed" and run-reviewer.sh comment vs brief anomaly -> REPRESENTED (276, 1269, 285).
COUNT 05-input-delivery-brief.md: 31

## research/web-01-multi-model-review-evidence.md
Located in report Section 5.1 (lines 1555-1697) and 5.5 (2038-2137); keyed by source ids and terms, not by source ids alone.
1. A1 MT-Bench judge: position, verbosity, self-enhancement, limited reasoning; swap-consistency; >80% human agreement; mitigations (swap, reference-guided) -> REPRESENTED (1559-1562, 1576).
2. A2 Panickssery self-preference / self-recognition causal link; include a reviewer from a different family than the author -> REPRESENTED (1566; author precaution 165, 203, 353).
3. A3 Chen 2025 DBG score, reasoning models not less biased, mitigations incl. activation steering -> REPRESENTED (1571-1572).
4. A4 CALM 12 biases, attack-and-detect, authority/bandwagon risk for "2 of 3 agree" display -> REPRESENTED (1576-1577).
5. B1 PoLL panel of diverse smaller judges beat GPT-4, kappa 0.763 vs 0.627, 7x cheaper, limits (QA task, transfer unverified) -> REPRESENTED (1583-1584, 1602).
6. B2 Correlated Errors: 60% agree when both wrong; judges inflate less-accurate models; heterogeneity necessary not sufficient -> REPRESENTED (1581, 1588-1589).
7. B3 Nine Judges, Two Effective Votes: n_eff ~2 (1.93), panel 8-22 pts short of independent ideal, best single judge matches panel, aggregation closes <=11% -> REPRESENTED (1593-1594, 1602).
8. C1 Debate or Vote: majority voting accounts for most gain; debate adds little; supports independent review + merge -> REPRESENTED (1608-1609, 2567).
9. C2 datarekha explainer (independence, conformity) -> REPRESENTED (1613-1614).
10. D1 SWR-Bench: Multi-Agg/Self-Agg, F1 +43.67%, recall +118.83%, low overlap (36 vs 27) supports union merge; Self-Agg substitute for model diversity -> REPRESENTED (1603, 1620-1623, 2076).
11. D2 GitHub ReviewBench golden set, dedup without agreement inflation, grounded/augmented metrics -> REPRESENTED (1625-1630).
12. D3 LangChain ReviewBench / Entelligence 2-of-3 filter discarding single-reviewer findings (conflicts with union) -> REPRESENTED (1351, 1579, 390).
13. D4 c-CRAB union of four tools passes 41.5% of tests; not a replacement for human review -> REPRESENTED (1635-1638, 2050).
14. D5 practitioner note (self-consistency, disagreement as signal, three-tier labels) -> REPRESENTED (1640-1641).
15. AE-1 agreement metrics: raw agreement overstates by 33-41 pts (21 judges), test-retest != correctness, Rating Roulette alpha, report kappa/alpha -> REPRESENTED (1647-1650, 2829).
16. AE-2 position bias judge/task-dependent; code-judge biases paper; order swap in merge/judge prompts; verbosity guard cheap -> REPRESENTED (1653, 1576).
17. F1 unanimous juries (Youden's J, TPR/FPR, composition matters) -> REPRESENTED (1671-1672, 1692).
18. F2 Splunk practitioner rule options (majority, max pooling, mean, 3 judges min) -> REPRESENTED (1676-1679).
19. F3 CARE / SkillAggregation / Dawid-Skene / Ising: weighted aggregation needs labelled data -> REPRESENTED (1653, 1681-1682).
20. G1 citation-overlap mechanical check (8% flagged, 97% genuine; proves existence not correctness) -> REPRESENTED (245, 1296, 1312).
21. G2 two-pass detect-then-filter; AI opinion not evidence; MegaLens sample (44% false positives among agreed) -> REPRESENTED (779, 1620, 1640).
22. Discrepancies/gaps: no external source contradicts verified code; PoLL vs Kim/Kohli tension; Entelligence vs SWR-Bench tension; no peer-reviewed study comparing quorum rules on findings; second-hand numbers flagged -> REPRESENTED (2060-2129, 2138+).
23. Key External Findings 1-9 -> REPRESENTED (2060, 2129).
24. Recommendations 1-9 (keep independent + merge, measure diversity, no k-of-n as validation, choose verdict rule by measurement TPR/FPR/Youden, state one-valid-passes as permissive default, randomise order and blind judge, exclude same-family author, no human-replacement claim, defer weighted aggregation) -> REPRESENTED in 5.5 and Section 6.4/7 rationale (2076, 1692, 2050; no heading "Recommendations from External Research" but substance present).
COUNT web-01-multi-model-review-evidence.md: 24

## research/web-02-claude-code-hooks-headless.md
Located in report Section 5.2 (lines 1698-1804).
1. Hook events; PostToolUse fires only after success, PostToolUseFailure on failure; PostToolBatch; board-writer must hook both -> REPRESENTED (1704, 2095, 2600).
2. Decision pattern `decision: block` for PostToolUse/Stop/SubagentStop; SubagentStop block keeps subagent running -> REPRESENTED (1704, 1782).
3. Inject into parent after subagent via PostToolUse on Agent tool (not SubagentStop) -> REPRESENTED (363, 376, 895).
4. Command hooks receive event JSON on stdin; handler types -> REPRESENTED in part (1704); minor.
5. Hooks load in `claude -p` unless `--bare`; in bare mode hooks via --settings/plugin flags do NOT run -> REPRESENTED (1709-1714).
6. stream-json needs --verbose; hook_started/hook_progress/hook_response events; system/init with `capabilities` array -> REPRESENTED (1711, 1718).
7. `--output-format json` total_cost_usd, per-model breakdown, client-side estimate; resume totals -> REPRESENTED (1718).
8. --resume/--continue in print mode; --fork-session; piped stdin 10MB cap; background-work wait; deleted cwd warning -> REPRESENTED in part (1716-1718); background-work and deleted-cwd details MINOR.
9. Gateway ids with --resume unverified -> REPRESENTED (1718, 380, 410).
10. --allowedTools only pre-approves; --tools/--disallowedTools/--restricted restrict availability -> REPRESENTED (1725-1728, 1787-1792).
11. --fallback-model comma-separated chain -> REPRESENTED (1725).
12. Subagent frontmatter tools/disallowedTools order; disallowedTools specifier removes whole tool in subagent vs CLI scoped rule; Agent omitted -> cannot spawn; permissionMode ignored for plugin subagents -> REPRESENTED (1732, 884, 1376, 1529).
13. Subagent `model` field accepts sonnet/opus/haiku/fable, full Anthropic ID, inherit; gateway ids not documented -> REPRESENTED (871, 1732).
14. Reviewer needing board write conflicts with read-only allowlist; write from hook/orchestrator -> REPRESENTED (363, 376, 683).
15. Settings precedence: managed top, --settings above files, non-merging keys; hooks replace-vs-add unconfirmed -> REPRESENTED (1081, 1306, 1739, 1740; open Q recorded).
16. --model gateway ids: ANTHROPIC_CUSTOM_MODEL_OPTION skip validation, availableModels filter, per-process --model, modelOverrides unrecognized_model diagnostic, CLAUDE_CODE_MAX_CONTEXT_TOKENS, GATEWAY_MODEL_DISCOVERY + /v1/models, LiteLLM picker keeps ids containing claude/anthropic -> REPRESENTED (1739-1749).
17. Field reports: #79702 SessionEnd not firing, #10373, #37559 prompt-type hooks unreliable, #9630 UserPromptSubmit unsupported, #18311/#22724 resume by explicit id -> REPRESENTED (1755-1778).
18. Hooks run inside subagents with agent_id/agent_type; SubagentStop exposes last_assistant_message, agent_transcript_path; SubagentStop transport recommendation -> REPRESENTED (1782-1785, 2053).
19. Agent SDK streaming: token events main session only; parent_tool_use_id attribution; session id on result/init -> REPRESENTED (1782, 4098).
20. --session-id UUID; --settings file/inline, 2 MiB; --setting-sources; --restricted (v2.1.248+) -> REPRESENTED (1787-1800).
21. Key External Findings 1-9 -> REPRESENTED (1800+, 2038-2137).
22. Recommendations 1-7 (local probe command shape, never --bare for hook-dependent reviewers, hook both events, SubagentStop matcher reflect-reviewer, keep read-only allowlist, hooks merge as blocker only if layered, code wins) -> REPRESENTED (380, 410, 508, 2053-2054).
23. Gaps (full event list, hook merge, gateway behaviour, issue dates, extractor stripped globs, passages only) -> REPRESENTED in part (1800-1804); the "wildcards stripped" caveat is MINOR.
COUNT web-02-claude-code-hooks-headless.md: 23

## synthesis/synth-06-conflict-log.md
Entries = every heading and every non-header table row (conflict, exposure, invariant, DATA, DOC, RX, CL rows, adjudication slots and outcomes). Mechanical check: all 329 table rows of synth-06 are verbatim lines of the report (grep -F -x); the report line is the locator, the match is by full row text (meaning), not by id.
1. [src L10] ## 6.12 Conflict log -> REPRESENTED (report L62)
2. [src L12] ### 6.12.0 How to read this section -> REPRESENTED (report L3137)
3. [src L18] `rNN:L` | `research/NN-*.md`, line L (01 overlap matrix, 02 finding contract, 03 merge/led -> REPRESENTED (report L3143)
4. [src L19] `S02:L` | `research/scope/02-run-comparison-and-notes.md`, line L (conflicts C-S1..C-S16 a -> REPRESENTED (report L3144)
5. [src L20] `RN:L` | `research/research-notes.md`, line L (AMBIGUITIES_FOR_USER at 234-267) | -> REPRESENTED (report L3145)
6. [src L21] `GQ-n` | row n of `gaps-and-questions.md` | -> REPRESENTED (report L3146)
7. [src L22] `path:line` | code or document line as quoted by the research file (HEAD `50d4d2b9d` unles -> REPRESENTED (report L3147)
8. [src L28] `C-S1..C-S16` | conflicts of the run-1 versus run-2 comparison | S02:531-546 | -> REPRESENTED (report L3153)
9. [src L29] `FX-1..FX-22` | future-use exposures | S02:574-595 | -> REPRESENTED (report L3154)
10. [src L30] `CL-X1..CL-X17` | collaboration conflicts X1-X17 (r1 versus r2) | r09:150-166 | -> REPRESENTED (report L3155)
11. [src L31] `CL-C01..CL-C19` | collaboration conflicts C-01..C-19 (r3 to r5) | r09:170-189 | -> REPRESENTED (report L3156)
12. [src L32] `SV-`, `VM-`, `LG-`, `CV-`, `RE-` | severity vocabulary, verdict model, ledger, convergenc -> REPRESENTED (report L3157)
13. [src L33] `CO-` | core-design conflicts between research files 01-18 (finding contract, limits, disp -> REPRESENTED (report L3158)
14. [src L34] `DATA-` | disagreeing numbers whose unit or source decides them | r02, r07, r08 | -> REPRESENTED (report L3159)
15. [src L35] `DOC-1..DOC-13` | the 13 [CODE-CONTRADICTED] documentation claims of `research-notes.md` A -> REPRESENTED (report L3160)
16. [src L36] `RX-` | contradictions between two research files, and other documentation-versus-code con -> REPRESENTED (report L3161)
17. [src L37] `C-01..C-15` | adjudication slots of the second table (not conflict ids of the first table -> REPRESENTED (report L3162)
18. [src L43] DECIDED-BY-EVIDENCE | code, data or a reproduced run decides it, or only one side is [CODE -> REPRESENTED (report L3168)
19. [src L44] UNDECIDABLE-BY-EVIDENCE | the evidence is genuinely absent (no run, no measurement) or the -> REPRESENTED (report L3169)
20. [src L54] INV-A | Contract 1.8.0 consumer-read field names (110 stable and 27 telemetry names) and t -> REPRESENTED (report L3179)
21. [src L55] INV-B | `derive_verdict` first-match map blocked, degraded, halted, pass; exit codes 0/10/ -> REPRESENTED (report L3180)
22. [src L56] INV-C | findings-v1 line grammar and `review merge` unchanged for the spec-panel loop and  -> REPRESENTED (report L3181)
23. [src L57] INV-D | `review-ledger/1` and its `ledger` command group, named in the shipped brief; `led -> REPRESENTED (report L3182)
24. [src L58] INV-E | `pr_submit` `Finding`, `Severity`, FSM, the fork-only checks, and "no `gh` or `git -> REPRESENTED (report L3183)
25. [src L59] INV-F | Installed-path rule: no installed primitive tells an agent to read or invoke anoth -> REPRESENTED (report L3184)
26. [src L60] INV-G | Reviewers are mutually blind and mechanically read-only (tool allowlist, plan mode -> REPRESENTED (report L3185)
27. [src L61] INV-H | Telemetry carries no document text (a convention today, enforced only for `context -> REPRESENTED (report L3186)
28. [src L62] INV-I | Fail-closed: a review that did not happen never certifies PASS (merge refuses zero -> REPRESENTED (report L3187)
29. [src L63] INV-J | Repo review rule S1-S5: binary blocking or minor, Medium is a non-blocking warning -> REPRESENTED (report L3188)
30. [src L64] INV-K | `make sync-dev` / `verify-sync` / `lint-architecture` gates and the layout traps ( -> REPRESENTED (report L3189)
31. [src L65] INV-L | Shadow mode changes no verdict; the legacy rotation and the Wave 4 debate stay aut -> REPRESENTED (report L3190)
32. [src L66] INV-M | `reflect_status` / `reflect_report_path` closed enum and the headless output direc -> REPRESENTED (report L3191)
33. [src L67] INV-N | Plugin mirror parity pins (`spec-panel` loop bullets, `sc-implement-protocol`, rou -> REPRESENTED (report L3192)
34. [src L69] ### 6.12.1 Table A: run-1 versus run-2 conflicts C-S1..C-S16 -> REPRESENTED (report L3194)
35. [src L73] C-S1 | Finding location and limits: anchor-as-text versus citation-as-path:lines, and whol -> REPRESENTED (report L3198)
36. [src L74] C-S2 | E2 folder writes into E1's evidence tree | `snap.py:4` opens `.../shadow-model-comb -> REPRESENTED (report L3199)
37. [src L75] C-S3 | Blocking rule defined four ways, plus reflect legacy HIGH/MEDIUM/LOW | `spec-panel. -> REPRESENTED (report L3200)
38. [src L76] C-S4 | Merge and verdict policy | Deterministic any-blocking union (panel kernel and ledge -> REPRESENTED (report L3201)
39. [src L77] C-S5 | Three model registries | Reflect skill aliases (`ANTHROPIC_DEFAULT_*_MODEL`), refle -> REPRESENTED (report L3202)
40. [src L78] C-S6 | Launch restriction for reflect profiles | `_REFLECT_LAUNCH = (sonnet, opus, haiku)` -> REPRESENTED (report L3203)
41. [src L79] C-S7 | Tasklist review today versus the panel verdict | Stage 10.5 and Wave 4 call reflect -> REPRESENTED (report L3204)
42. [src L80] C-S8 | Input contract: the panel brief names only the candidate | Reflect briefs carry the -> REPRESENTED (report L3205)
43. [src L81] C-S9 | Ledger implementations | `cli/review/ledger.py` (`review-ledger/1`) | Installed `sc -> REPRESENTED (report L3206)
44. [src L82] C-S10 | Telemetry strata and model vocabulary | `review-telemetry/1` strata hard-coded `so -> REPRESENTED (report L3207)
45. [src L83] C-S11 | Report ending | `spec-panel.md:260, 263`: last line `verdict:` and Reviser brief | -> REPRESENTED (report L3208)
46. [src L84] C-S12 | Tasklist skill names Tier-3 task-builder remediation | `sc-tasklist-protocol/SKILL -> REPRESENTED (report L3209)
47. [src L85] C-S13 | Run-2 hand-off internal errors | HO recommends run 2 as main hand-off | Run-2 note -> REPRESENTED (report L3210)
48. [src L86] C-S14 | HO row 1 attribution and stale-citation claim | HO attributes 40 files and +8,026  -> REPRESENTED (report L3211)
49. [src L87] C-S15 | Cause of source-blind reviews | HO:58 states it as fact | `COMBO-REPORT.md:373` ca -> REPRESENTED (report L3212)
50. [src L88] C-S16 | Tier 2b policy text and tier data drift | `MODEL-TIERS.md:44` (owner 2026-11-12) | -> REPRESENTED (report L3213)
51. [src L90] ### 6.12.2 Table B: future-use exposures FX-1..FX-22 -> REPRESENTED (report L3215)
52. [src L96] FX-1 | Text-anchor limit and whole-line drop | PR review, rf-qa and tasklist need code hun -> REPRESENTED (report L3221)
53. [src L97] FX-2 | Exact-substring anchors over whitespace-flattened text | Markdown escapes, backtick -> REPRESENTED (report L3222)
54. [src L98] FX-3 | Line-number model | Files with `\r`, form feeds or U+2028 shift spans | `locate` co -> REPRESENTED (report L3223)
55. [src L99] FX-4 | Id grammar | Tasklist ids `T01.02`, PR numbers, issue ids, `file:line` | `_ID` acce -> REPRESENTED (report L3224)
56. [src L100] FX-5 | Category enum is spec-shaped | A code review needs bug, security and test-gap class -> REPRESENTED (report L3225)
57. [src L101] FX-6 | Severity and blocking semantics inconsistent | Consumers expect one meaning | `SP:2 -> REPRESENTED (report L3226)
58. [src L102] FX-7 | Brief names only the candidate | PR review needs the diff base, ticket and tests; t -> REPRESENTED (report L3227)
59. [src L103] FX-8 | Reviewers are generic sessions without a read-only allowlist | Untrusted diffs and  -> REPRESENTED (report L3228)
60. [src L104] FX-9 | Single-reviewer re-review | rf-qa fix loops and spec loops need a quorum | All 8 pa -> REPRESENTED (report L3229)
61. [src L105] FX-10 | Any-blocking verdict, no calibrator | A weak model must not decide alone | The ver -> REPRESENTED (report L3230)
62. [src L106] FX-11 | Multi-round behaviour never exercised with real panels | rf-qa replacement and spe -> REPRESENTED (report L3231)
63. [src L107] FX-12 | No locking, non-atomic `--out`, `merge` exit 0, relative doc path | Concurrent CI  -> REPRESENTED (report L3232)
64. [src L108] FX-13 | Launch undefined for gateway models | muse, gpt, glm panels | `launch {}` under ga -> REPRESENTED (report L3233)
65. [src L109] FX-14 | Environment detection by `T3Model01` only | Portability to other workspaces | `sel -> REPRESENTED (report L3234)
66. [src L110] FX-15 | Silent duplicate models by default | Diverse panels | Soft distinctness re-admits  -> REPRESENTED (report L3235)
67. [src L111] FX-16 | Telemetry unwired, strata two values, document metrics spec-shaped | PR review of  -> REPRESENTED (report L3236)
68. [src L112] FX-17 | Benchmarks rest on three plan packages | Spec and PR review | 16 ground-truth item -> REPRESENTED (report L3237)
69. [src L113] FX-18 | Benchmark regeneration depends on `/tmp` and raw transcripts not in git | Every re -> REPRESENTED (report L3238)
70. [src L114] FX-19 | Gateway behaviour silently changes which model reviews | All non-Claude panels | N -> REPRESENTED (report L3239)
71. [src L115] FX-20 | rf-qa replacement: cap text copied into many files that call no script | rf-qa fix -> REPRESENTED (report L3240)
72. [src L116] FX-21 | Panel and ledger wired into no skill other than spec-panel and reflect shadow | An -> REPRESENTED (report L3241)
73. [src L117] FX-22 | Dead registrations `lint_cmd`, `estimate_cmd` | CLI surface | Names listed in `__i -> REPRESENTED (report L3242)
74. [src L119] ### 6.12.3 Table C: collaboration conflicts CL-X1..CL-X17 and CL-C01..CL-C19 -> REPRESENTED (report L3244)
75. [src L125] CL-X1 | Ember act rate on injected text | r1: item acted on next call in 3 of 3 sessions,  -> REPRESENTED (report L3250)
76. [src L126] CL-X2 | Luna act rates | r1: 0.33 next call, 1.00 later, finish 1.00 | r2: 4/5 and 5/5; r4 -> REPRESENTED (report L3251)
77. [src L127] CL-X3 | Which reviewers get the finish signal | r1: all three | r2: receivers only | r09:1 -> REPRESENTED (report L3252)
78. [src L128] CL-X4 | k on HL2 | Planning thresholds by arithmetic | Measured k needs Spike 4, which no  -> REPRESENTED (report L3253)
79. [src L129] CL-X5 | Turn measurement for Spike 4 | r1 `values.py:89-100`: group by `message.id`, skip  -> REPRESENTED (report L3254)
80. [src L130] CL-X6 | Gateway lock | r1 kept to 3 sessions | r2 used `flock /tmp/collab-gateway.lock` an -> REPRESENTED (report L3255)
81. [src L131] CL-X7 | Session files kept or deleted | r2 reducer reads transcripts | r1 reads kept attem -> REPRESENTED (report L3256)
82. [src L132] CL-X8 | Seal timing | r1 seals at the checkpoint before choosing an item (`radar-hook.sh:5 -> REPRESENTED (report L3257)
83. [src L133] CL-X9 | Retry and re-ask time thresholds | r1: 30 s | r2: 10 s | r09:158 | UNDECIDABLE-BY- -> REPRESENTED (report L3258)
84. [src L134] CL-X10 | Catalogue artifact hash | Same M1-M10 text, wrapper `r1-cat/1` | Wrapper `moves/1 -> REPRESENTED (report L3259)
85. [src L135] CL-X11 | `origin` tag in the findings line | In-line `origin: own/peer` (r2 `tagger.py:82` -> REPRESENTED (report L3260)
86. [src L136] CL-X12 | Smoke honesty | r1 labels its collab-1 row provisional, S3 "missing" | r2 reports -> REPRESENTED (report L3261)
87. [src L137] CL-X13 | Hand-off claims versus files | r2 lists `bin/lib/*` as built; r1 claims 138 tests -> REPRESENTED (report L3262)
88. [src L138] CL-X14 | Contract shape: "succeeded" over a FAIL | Return contract says succeeded | A `las -> REPRESENTED (report L3263)
89. [src L139] CL-X15 | DESIGN says "not implemented" beside an IMPLEMENTATION.md | `r1 DESIGN.md:7`, `r2 -> REPRESENTED (report L3264)
90. [src L140] CL-X16 | Planning numbers versus real | Planning baseline B | r1 collab-0 107.105 s versus -> REPRESENTED (report L3265)
91. [src L141] CL-X17 | Opus used outside the judge | Rule: Opus only as judge | r1 `IMPLEMENTATION.md` s -> REPRESENTED (report L3266)
92. [src L142] CL-C01 | H3 base for the sandbox | r3 and r5: the parent commit | r4: the T1-start tree (` -> REPRESENTED (report L3267)
93. [src L143] CL-C02 | Peer/own tag in-line or sidecar | In-line | Sidecar | r09:172 | UNDECIDABLE-BY-EV -> REPRESENTED (report L3268)
94. [src L144] CL-C03 | Transcript of a hang-killed reviewer | r5: no copy exists for a killed receiver,  -> REPRESENTED (report L3269)
95. [src L145] CL-C04 | Admission and concurrency counting | Three mechanisms across the packages | One s -> REPRESENTED (report L3270)
96. [src L146] CL-C05 | Judge output location | Per-package wrappers | One location | r09:175 | UNDECIDAB -> REPRESENTED (report L3271)
97. [src L147] CL-C06 | Direction of flow for the strong model on SL2/HL2 | r3 searcher (sends and receiv -> REPRESENTED (report L3272)
98. [src L148] CL-C07 | One schema, three message kinds | `panel-msg/1` with `challenge`, `card`, `covera -> REPRESENTED (report L3273)
99. [src L149] CL-C08 | The 12-character rule versus exact-quote anchors | A rule that no phase-2 text sh -> REPRESENTED (report L3274)
100. [src L150] CL-C09 | Re-ask without a model identity check | Re-ask accepted | Re-ask needs the identi -> REPRESENTED (report L3275)
101. [src L151] CL-C10 | k test-vector rounding | 23.8 | 23.795 | r09:180 | DECIDED-BY-EVIDENCE (class E,  -> REPRESENTED (report L3276)
102. [src L152] CL-C11 | r5 snapshot flag | r5 `bin/sandbox-build.sh:25` runs `git add -A` without `-f` |  -> REPRESENTED (report L3277)
103. [src L153] CL-C12 | Session cleanup | Delete session ids | Keep them | r09:182 | UNDECIDABLE-BY-EVIDE -> REPRESENTED (report L3278)
104. [src L154] CL-C13 | Only r5 builds the static kit A2 | Exchange designs without A2 cannot be separate -> REPRESENTED (report L3279)
105. [src L155] CL-C14 | Act rate measured twice with different results | `act-rates.json` | `NOTES.md:36- -> REPRESENTED (report L3280)
106. [src L156] CL-C15 | Hook latency versus the 0.1 s design budget | Budget 0.1 s per call | Measured p9 -> REPRESENTED (report L3281)
107. [src L157] CL-C16 | Sealed judging | Seal the judge input | No seal | r09:186 | UNDECIDABLE-BY-EVIDEN -> REPRESENTED (report L3282)
108. [src L158] CL-C17 | Reviewer id conventions | `t4-1` is luna in r3 and r4 | `t4-1` is haiku in r5 `hl -> REPRESENTED (report L3283)
109. [src L159] CL-C18 | Orchestrator rule drift | Process | Product | r09:188 | UNDECIDABLE-BY-EVIDENCE ( -> REPRESENTED (report L3284)
110. [src L160] CL-C19 | Ledger outcome differs between packages | r2 ledger `blocked` | r1 `complete` | r -> REPRESENTED (report L3285)
111. [src L164] ### 6.12.4 Table D: severity vocabulary, verdict model, ledger, convergence and reflect-en -> REPRESENTED (report L3289)
112. [src L168] SV-1 | How many meanings "Medium" has | Slice 12 I1: four meanings | Research/12: at least -> REPRESENTED (report L3293)
113. [src L169] SV-2 | How many severity vocabularies | Slice 12 I3: seven (in E3 alone) | Research/12: si -> REPRESENTED (report L3294)
114. [src L170] SV-3 | Category sets 6 versus 18 versus reflect versus ground-truth classes | Spec and CLI -> REPRESENTED (report L3295)
115. [src L171] SV-4 | `card_convert` downgrades `important` | `important` is blocking under the CRITICAL/ -> REPRESENTED (report L3296)
116. [src L172] SV-5 | "Review caps differ" | Slice 12 I2: caps differ across consumers | In the repo's ow -> REPRESENTED (report L3297)
117. [src L173] SV-6 | Tasklist Medium: blocking or not | Tasklist skill: High and Medium block and are pa -> REPRESENTED (report L3298)
118. [src L174] SV-7 | Plugin mirror of the loop: softened or extended | Slice 12 A1 and B11: plugin `spec -> REPRESENTED (report L3299)
119. [src L175] SV-8 | spec-panel loop depends on rf-qa Fix Cycle | Slice 12 B10, I10, G2.9, and the first -> REPRESENTED (report L3300)
120. [src L176] VM-1 | Reviewer-typed versus script-computed verdict | Prompts file `:62`: "the verdict li -> REPRESENTED (report L3301)
121. [src L177] VM-2 | Who decides `blocking` | CLI ledger: the reviewer types it (MINOR cannot be blockin -> REPRESENTED (report L3302)
122. [src L178] VM-3 | Stored verdict versus derived verdict | `ledger.verdict()` returns the stored last- -> REPRESENTED (report L3303)
123. [src L179] VM-4 | `defer` semantics and its docstring | Docstring (`ledger.py:351`): the stored decis -> REPRESENTED (report L3304)
124. [src L180] VM-5 | Partial panel: fail-closed at zero valid blocks, fail-open at one | `ledger.py:150- -> REPRESENTED (report L3305)
125. [src L181] VM-6 | Cap enforced by a label only | `_decision` returns ESCALATE at the cap | `merge_rou -> REPRESENTED (report L3306)
126. [src L182] LG-1 | Two ledger status machines and clearing evidence | CLI `review-ledger/1`: `open, re -> REPRESENTED (report L3307)
127. [src L183] LG-2 | `ledger-v1` (E2) versus `review-ledger/1` | The E2 per-reviewer row block (item, ve -> REPRESENTED (report L3308)
128. [src L184] LG-3 | Docstring versus code for clearing | `ledger.py:112`: a reviewer with an invalid bl -> REPRESENTED (report L3309)
129. [src L185] LG-4 | Tests pin defects as intended behaviour | Fix the defects | 8 of the 9 pins read as -> REPRESENTED (report L3310)
130. [src L186] CV-1 | Convergence threshold 0.75 versus 0.80 | `SKILL.md:703, 1317`: PASS from 0.75, PART -> REPRESENTED (report L3311)
131. [src L187] CV-2 | Single-vendor posture | `SKILL.md:839, 1481`: warn-only | `contract.py:287-288` deg -> REPRESENTED (report L3312)
132. [src L188] CV-3 | `t2_model_class_diversity` vocabulary | Skill: `full` or `degraded` | Engine A emit -> REPRESENTED (report L3313)
133. [src L189] CV-4 | `contract_version` 1.0 versus 1.8.0 | Engine A emits `1.0` (`ensemble.py:74, 788`)  -> REPRESENTED (report L3314)
134. [src L190] CV-5 | Meaning of `merge_method: adversarial` | Skill EV-2: set only after a real merge, c -> REPRESENTED (report L3315)
135. [src L191] CV-6 | `reviewer_briefs_materialized` | `refs/reviewer-spec.md:51, 57, 78` instructs the c -> REPRESENTED (report L3316)
136. [src L192] CV-7 | `--promote` default | `runner.py:457` comment: `--no-promote` is the hard default | -> REPRESENTED (report L3317)
137. [src L193] CV-8 | Executor-disjoint ensemble claim | `sc-tasklist-protocol/SKILL.md:1141, 1152, 1165` -> REPRESENTED (report L3318)
138. [src L194] CV-9 | Exit-script gate defects | Shadow EV-1 rate must be no higher than the legacy basel -> REPRESENTED (report L3319)
139. [src L195] RE-1 | Reflect's two Tier-2 engines | Engine A (`superclaude reflect run`): in-process swa -> REPRESENTED (report L3320)
140. [src L196] RE-2 | Shadow non-interference enforced by LLM prose | Ten shadow steps performed by the o -> REPRESENTED (report L3321)
141. [src L197] RE-3 | `--fix` auto-fix loop | `sc-tasklist-protocol` passes `--fix` | Engine A emits no ` -> REPRESENTED (report L3322)
142. [src L198] RE-4 | Reflect reviewer and calibrator vocabularies | `refs/reflection-rubric.md:39`: Alig -> REPRESENTED (report L3323)
143. [src L200] ### 6.12.5 Table E: core-design conflicts found in research files 01-18 -> REPRESENTED (report L3325)
144. [src L204] CO-1 | Finding location type and the ledger path | findings-v1: quoted `anchor`, required  -> REPRESENTED (report L3329)
145. [src L205] CO-2 | Line grammar versions | v1 accepts `calibrated_confidence` and carries `prior` line -> REPRESENTED (report L3330)
146. [src L206] CO-3 | Fingerprint and clustering | v1: 16-hex-character sha256 over the tag `v1`, the sec -> REPRESENTED (report L3331)
147. [src L207] CO-4 | Unknown keys: open or closed | findings-v1 and v2 accept any unknown key except `ca -> REPRESENTED (report L3332)
148. [src L208] CO-5 | Over-limit policy | Keep drop-and-warn (today); E1 `SKILL.md:343`: the orchestrator -> REPRESENTED (report L3333)
149. [src L209] CO-6 | Unit of loss | v1 ledger: one bad line costs one finding; other lines kept | v2 clu -> REPRESENTED (report L3334)
150. [src L210] CO-7 | Reference grammar for tasklist ids | `_REF_TOKEN` and `telemetry._ID_TOKEN` (the sa -> REPRESENTED (report L3335)
151. [src L211] CO-8 | Brief limits not stated | The brief states only the anchor limit | The parser limit -> REPRESENTED (report L3336)
152. [src L212] CO-9 | Spec-shaped hard-codings | One shared regex, category set, placeholders, strata, re -> REPRESENTED (report L3337)
153. [src L213] CO-10 | Dispatch mechanisms | E1 prompt path: class word on the Agent `model` argument (en -> REPRESENTED (report L3338)
154. [src L214] CO-11 | Served model versus requested model | Contract and parity fields record requested  -> REPRESENTED (report L3339)
155. [src L215] CO-12 | Three "class" vocabularies | Tier file `classes` (9 names) | `_vendor_from_model_i -> REPRESENTED (report L3340)
156. [src L216] CO-13 | `muse-ember-1.0` | Absent from `src`, `tests`, `docs`, `scripts`, `plugins` and `c -> REPRESENTED (report L3341)
157. [src L217] CO-14 | Are E1 and E2 results independent | E1 confirms E2 | E1's package is byte-identica -> REPRESENTED (report L3342)
158. [src L218] CO-15 | Acceptance: the metric of record | Ground-truth items found at any severity | Item -> REPRESENTED (report L3343)
159. [src L219] CO-16 | Ground truth for non-plan use cases | Seeded defects with a clean twin (E1 pilot d -> REPRESENTED (report L3344)
160. [src L220] CO-17 | Who owns the harness files | Kernel CLI (`review verify-run`, served-model and con -> REPRESENTED (report L3345)
161. [src L221] CO-18 | Default panel composition from E2 | E2 guidance: default `ember + 2x luna` (64k to -> REPRESENTED (report L3346)
162. [src L222] CO-19 | Run record: where and what | Append-only per-run `events.jsonl` (one row per agent -> REPRESENTED (report L3347)
163. [src L223] CO-20 | Memory write policy | One LLM `Read` plus `Write` of a whole tracked file at Wave  -> REPRESENTED (report L3348)
164. [src L224] CO-21 | Cost accounting and D-17 | Reviewer-only cost | All-stages cost; `model_scores` ad -> REPRESENTED (report L3349)
165. [src L225] CO-22 | Two evidence gates for one job | `review verify-citations`: deterministic, advisor -> REPRESENTED (report L3350)
166. [src L226] CO-23 | Process redesign: modules and promotion | Sweep Sheet (script-built typed items) v -> REPRESENTED (report L3351)
167. [src L227] CO-24 | CB-2 versus Medium routing | E2 CB-2: list every defect, non-blocking too, in the  -> REPRESENTED (report L3352)
168. [src L228] CO-25 | Consumer entry for tasklist and workflow (DO4) | Keep reflect UC-1 as the only ent -> REPRESENTED (report L3353)
169. [src L229] CO-26 | Is the panel reachable by consumers today | Workflow and tasklist call reflect UC- -> REPRESENTED (report L3354)
170. [src L230] CO-27 | PR review wire format | One wire format: findings-v2 with module-declared vocabula -> REPRESENTED (report L3355)
171. [src L231] CO-28 | PR review: grounding and category rules | `is_groundable` drops any finding withou -> REPRESENTED (report L3356)
172. [src L232] CO-29 | PR panel as a third reviewer name or a separate pre-step | Third name in `REVIEWER -> REPRESENTED (report L3357)
173. [src L233] CO-30 | rf-qa replacement: first step | Start at the `/task` phase gate (8 lenses, report- -> REPRESENTED (report L3358)
174. [src L234] CO-31 | Reviewers read-only | `reflect-reviewer`, `evidence-validator`: plan mode, no Bash -> REPRESENTED (report L3359)
175. [src L235] CO-32 | Two "eight lens" sets | Swarm registry: 8 populated lenses (`bare-review`, `reflec -> REPRESENTED (report L3360)
176. [src L236] CO-33 | Naive layouts versus repo gates | A shared-core skill directory, shared constants  -> REPRESENTED (report L3361)
177. [src L237] CO-34 | Branch layout | `feat/review-panel` as an umbrella and `feat/review-panel/<name>`  -> REPRESENTED (report L3362)
178. [src L238] CO-35 | Plugin delivery of a new panel | Ship a plugin copy | No test requires one; `plugi -> REPRESENTED (report L3363)
179. [src L239] CO-36 | Fate of the five installed-only variants | Keep installed, archive, or fold the id -> REPRESENTED (report L3364)
180. [src L240] CO-37 | Is #479 the outcome of the refactor spec | #479 plus #478 are the shipped substitu -> REPRESENTED (report L3365)
181. [src L241] CO-38 | Vintage of the variants' base | Slice 12 C8: built on the PR 427 base; install log -> REPRESENTED (report L3366)
182. [src L242] CO-39 | Panel template validation gap | `review panel validate` is expected to check a `re -> REPRESENTED (report L3367)
183. [src L243] CO-40 | Telemetry and manifest as designed versus as written | `telemetry.py:3`: no docume -> REPRESENTED (report L3368)
184. [src L244] CO-41 | Tasklist fidelity prompt: core module or separate gate | `cli/tasklist/prompts.py` -> REPRESENTED (report L3369)
185. [src L246] ### 6.12.6 Table F: disagreeing numbers decided by unit or source (DATA) -> REPRESENTED (report L3371)
186. [src L250] DATA-1 | The "92 / 80 / 49" figures | One unit assumed ("92 findings dropped over 264 merg -> REPRESENTED (report L3375)
187. [src L251] DATA-2 | Verdict flips | "Four verdicts flipped FAIL to PASS" | `audit2.json` `verdict_fli -> REPRESENTED (report L3376)
188. [src L252] DATA-3 | Size of `combos/` | 106 scored runs, 96 directories, 97 tracked entries, "107 ent -> REPRESENTED (report L3377)
189. [src L253] DATA-4 | `RESULT.md` files | 19 | 29 | r08:40 | DECIDED-BY-EVIDENCE [CODE-VERIFIED] | Both -> REPRESENTED (report L3378)
190. [src L254] DATA-5 | Quarantine files and luna-bearing rows | 428 reviewer files; "9 luna-bearing comb -> REPRESENTED (report L3379)
191. [src L255] DATA-6 | Qwen reviewer count | 3 (`PILOT-REPORT.md:12`) | 4 (`SPEC.md:3`) | r08:42 | DECID -> REPRESENTED (report L3380)
192. [src L256] DATA-7 | Multi-reviewer clusters | "7 of 216 multi-reviewer clusters" | 13 clusters have t -> REPRESENTED (report L3381)
193. [src L257] DATA-8 | Dispatch collapse counts | Pilot: 6 of 9 tier3-orchestrated runs | Re-derived for -> REPRESENTED (report L3382)
194. [src L258] DATA-9 | Calibrator class loss | Only A3 collapsed (FINDINGS.md, results.md) | The calibra -> REPRESENTED (report L3383)
195. [src L259] DATA-10 | `identity_source` | Slice 11: every contract records `requested-pinned` | 1 of 1 -> REPRESENTED (report L3384)
196. [src L260] DATA-11 | Duplicate-model resolutions | 26 of 40 `@live7` (run ids `r1..r40`) | 30 of 40 ` -> REPRESENTED (report L3385)
197. [src L261] DATA-12 | Test-function counts | E2: "159 functions"; run-2 and run-1 claimed 138 / 358 /  -> REPRESENTED (report L3386)
198. [src L262] DATA-13 | rf-* spawn-line census | Slice 12: 185 prose spawn lines over 7 skills | 175 lin -> REPRESENTED (report L3387)
199. [src L263] DATA-14 | Source-blind runs | 161 of 665 (research/05 Unit 8, pre-correction) | 156 of 665 -> REPRESENTED (report L3388)
200. [src L264] DATA-15 | AUDIT-CLEAN exclusion count | Committed header: 69 row-packages carry an EXCLUDE -> REPRESENTED (report L3389)
201. [src L266] ### 6.12.7 Table G: the 13 [CODE-CONTRADICTED] claims of `research-notes.md` AMBIGUITIES_F -> REPRESENTED (report L3391)
202. [src L272] DOC-1 | Who changed `cli/review` | E2 run-2 and `HANDOFF-run1-vs-run2.md:22`: #519 plus #5 -> REPRESENTED (report L3397)
203. [src L273] DOC-2 | "Tasklist review reaches no reflect panel" (run-1 D14, first half) | "No tasklist  -> REPRESENTED (report L3398)
204. [src L274] DOC-3 | "Reflect has no panel/tier code" (run-2 5.6, Q4, Q9) | E2 contrast row taken from  -> REPRESENTED (report L3399)
205. [src L275] DOC-4 | "Alias GT3 found once" (run-1) | Alias GT3 | Alias GT1 (= B6) was found by exactly -> REPRESENTED (report L3400)
206. [src L276] DOC-5 | "Discarded with no error" at merge (`COMBO-REPORT.md:292`) | No error | `ledger.py -> REPRESENTED (report L3401)
207. [src L277] DOC-6 | "Four verdict flips" | Four | Three (see DATA-2) | r08:82 | DECIDED-BY-EVIDENCE [C -> REPRESENTED (report L3402)
208. [src L278] DOC-7 | "16 empty terra reviews" | 16 terra | 14 terra plus 2 luna | r08:84 | DECIDED-BY-E -> REPRESENTED (report L3403)
209. [src L279] DOC-8 | Harness brief category `unpassable-ac` | The harness brief | Rules file, `CATEGORI -> REPRESENTED (report L3404)
210. [src L280] DOC-9 | "`T2bModel01` is not referenced anywhere in `src/` or `tests/`" | Run-2 note | 18  -> REPRESENTED (report L3405)
211. [src L281] DOC-10 | "159 functions" of tests | Run-2 notes | The per-file column sums to 179 (111 in  -> REPRESENTED (report L3406)
212. [src L282] DOC-11 | Seed brief: "no missing-task category and no severity levels" | `seed-brief.md:26 -> REPRESENTED (report L3407)
213. [src L283] DOC-12 | `theory.py` HARD set as applied | "Ten missed issues" definition | `HARD = {I5, I -> REPRESENTED (report L3408)
214. [src L284] DOC-13 | Memory lesson (memory line 64): "fenced yaml calibration not parsed by cluster" | -> REPRESENTED (report L3409)
215. [src L285] RX-1 | Is the unaudited batch j1 a hole for the "not confirmed" decision | research/16 (fi -> REPRESENTED (report L3410)
216. [src L286] RX-2 | Is location type a core blocker | research/13 (first text): not a blocker, only the -> REPRESENTED (report L3411)
217. [src L287] RX-3 | Reflect has no fix loop | research/01 (first text) | `runner.py:474-478, 748-793` h -> REPRESENTED (report L3412)
218. [src L288] RX-4 | "No contract" in three pilot EV-1 failures | Slice 11 and the first texts of resear -> REPRESENTED (report L3413)
219. [src L289] RX-5 | How many reasons make the Stage 2 exit FAIL | research/06 first text: "three indepe -> REPRESENTED (report L3414)
220. [src L290] RX-6 | Which hooks skip subagent calls | research/09 Summary: `reflect-reviewer` "is skipp -> REPRESENTED (report L3415)
221. [src L291] RX-7 | Brief families and `check_finding` range | research/05 Summary: four briefs; resear -> REPRESENTED (report L3416)
222. [src L292] RX-8 | Test pins read in research/03 | "6 of the 8 pins I read assert the defect" | Its ta -> REPRESENTED (report L3417)
223. [src L293] RX-9 | Findings module size | research/02: `findings_v2.py` is 305 lines | The file is 304 -> REPRESENTED (report L3418)
224. [src L294] RX-10 | Telemetry and manifest invariants as stated | `telemetry.py:3`, `manifest.py:3`, S -> REPRESENTED (report L3419)
225. [src L295] RX-11 | Reflect documentation against code | `cli/reflect/__init__.py` docstring (a `claud -> REPRESENTED (report L3420)
226. [src L296] RX-12 | Repo documentation against repo configuration | `CLAUDE.md:18` and `sync-disciplin -> REPRESENTED (report L3421)
227. [src L297] RX-13 | E3 and experiment documentation against files | `FINAL-REPORT.md:226-240`: evidenc -> REPRESENTED (report L3422)
228. [src L298] RX-14 | E1 and E2 experiment documentation against artifacts | E1 `PLAN.md:1, 3` and `comb -> REPRESENTED (report L3423)
229. [src L299] RX-15 | Is engine A's diversity computed from SERVED or REQUESTED worker `model_id` values -> REPRESENTED (report L3424)
230. [src L301] ### 6.12.8 Coverage check and the unverified residue -> REPRESENTED (report L3426)
231. [src L307] r01 | C-1 line grammar, C-2 blocking rule, C-3 location type, C-4 fingerprint, C-5 two led -> REPRESENTED (report L3432)
232. [src L308] r02 | Unknown keys, 200/300 limits, `T01.01`, truncate or re-ask or warn, variants disagre -> REPRESENTED (report L3433)
233. [src L309] r03 | D-1, D-2, D-11, D-13, tests pin defects, variants re-implement, authority spectrum,  -> REPRESENTED (report L3434)
234. [src L310] r04 | Three dispatch mechanisms, served versus requested, three tier-list copies, `T2bMode -> REPRESENTED (report L3435)
235. [src L311] r05 | Brief families, B-1..B-7, `unpassable-ac`, `theory.py`, spec-shaped hard-codings, ta -> REPRESENTED (report L3436)
236. [src L312] r06 | Two engines, 0.75 versus 0.80, 1.0 versus 1.8.0, vocabulary conflicts, exit failures -> REPRESENTED (report L3437)
237. [src L313] r07 | Weak E1 leads, dispatch collapse, calibrator class loss, served-model blindness, clu -> REPRESENTED (report L3438)
238. [src L314] r08 | 92/80/49 units, flips, counts, j1, `fullpkg()`, default panel, what the study does n -> REPRESENTED (report L3439)
239. [src L315] r09 | X1-X17, C-01..C-19, H1-H4 unconditional or not, exchange versus static kit | CL-X1.. -> REPRESENTED (report L3440)
240. [src L316] r10 | `ledger-v1` versus `review-ledger/1`, E1 coverage and precheck versus E2, gates, see -> REPRESENTED (report L3441)
241. [src L317] r11 | Advisory or blocking, entry point, 36-test matrix, run-1 D14, plugin reach | C-S7, C -> REPRESENTED (report L3442)
242. [src L318] r12 | Medium meanings, vocabularies, caps, plugin mirror, brief text, severity and cap pol -> REPRESENTED (report L3443)
243. [src L319] r13 | PR blockers, rf-qa blockers, `is_groundable`, location type, read-only reviewers, le -> REPRESENTED (report L3444)
244. [src L320] r14 | Variants, #479 outcome, install state, shadowing, numeric claims | CO-36..CO-38, RX- -> REPRESENTED (report L3445)
245. [src L321] r15 | Telemetry shapes, D-17, D-23, anchors in telemetry, memory policy, cost bases | CO-1 -> REPRESENTED (report L3446)
246. [src L322] r16 | E1 and E2 independence, metric of record, ground truth, harness ownership, audits, j -> REPRESENTED (report L3447)
247. [src L323] r17 | Crosswalk of the numbering schemes, pinned tests, open owner questions (limits polic -> REPRESENTED (report L3448)
248. [src L324] r18 | Naive layouts versus gates, ref rule, stale repository docs, installed-path rule | C -> REPRESENTED (report L3449)
249. [src L330] OQ-1 | Tasklist skill names Tier-3 task-builder remediation while reflect's default route  -> REPRESENTED (report L3455)
250. [src L331] OQ-2 | Cause of source-blind reviews and the effect of naming `source.md` | An inference;  -> REPRESENTED (report L3456)
251. [src L332] OQ-3 | The +8,026-line figure and the wrong-blocker rate "4.75 per row" | Slice figures ne -> REPRESENTED (report L3457)
252. [src L333] OQ-4 | Cause of the 17 to 19 findings dropped with no rule-based reason | No committed bre -> REPRESENTED (report L3458)
253. [src L334] OQ-5 | Pilot dispatch-collapse rate 6 of 9 and whether the tier3 effect is real | `/tmp/sh -> REPRESENTED (report L3459)
254. [src L335] OQ-6 | The corrected AUDIT-CLEAN table | Not recomputed | Robustness of the E2 decision |  -> REPRESENTED (report L3460)
255. [src L336] OQ-7 | Whether a truncated anchor still locates; re-ask recovery rate | Spike 5 not run; f -> REPRESENTED (report L3461)
256. [src L337] OQ-8 | External readers of engine A's ten extra keys and `contract_version 1.0` | Searched -> REPRESENTED (report L3462)
257. [src L338] OQ-9 | Approval of thresholds T-1..T-10 and the pilot stop rule S-0..S-5 | Only the owner' -> REPRESENTED (report L3463)
258. [src L339] OQ-10 | Whether the gateway serves `muse-ember-1.0` today; Tier 4 slot 02 or 04 | No gatew -> REPRESENTED (report L3464)
259. [src L340] OQ-11 | #346 phase-5 numeric claims and all control label counts | Six control `metrics.js -> REPRESENTED (report L3465)
260. [src L341] OQ-12 | All collaboration estimates, act rates, hook cost, `--resume` and hooks for gatewa -> REPRESENTED (report L3466)
261. [src L342] OQ-13 | Quarantine count 428 and combo-size "107 entries" | Not reproducible | Quoting onl -> REPRESENTED (report L3467)
262. [src L343] OQ-14 | Whether `additionalContext` from a PostToolUse hook reaches a subagent's own model -> REPRESENTED (report L3468)
263. [src L344] OQ-15 | Whether the owner accepts #479 plus #478 as closing the refactor-spec request | No -> REPRESENTED (report L3469)
264. [src L345] OQ-16 | Who wrote the E2 ground truth; the 12-row blind re-judge | No authorship field; no -> REPRESENTED (report L3470)
265. [src L346] OQ-17 | Pre-registration ordering of the E1 `PLAN.md` and E2 pilot decision rules | mtimes -> REPRESENTED (report L3471)
266. [src L347] OQ-18 | Cost of a local panel per PR round | Never measured | C-10 | GQ-177 | -> REPRESENTED (report L3472)
267. [src L348] OQ-19 | How the master loop's "reviewer model actually used" is filled | A model's self-re -> REPRESENTED (report L3473)
268. [src L349] OQ-20 | Reflect rubric class vocabulary and the 5- versus 6-dimension calibrator | Carried -> REPRESENTED (report L3474)
269. [src L350] OQ-21 | Where the transcript adapter lives given INV-F | Design placement | C-08 | GQ-215  -> REPRESENTED (report L3475)
270. [src L351] OQ-22 | Remote-side behaviour of the ref rule; whether the Orca and pre-commit hooks are i -> REPRESENTED (report L3476)
271. [src L352] OQ-23 | Whether a real two-process race has ever lost a manifest attempt | Only a determin -> REPRESENTED (report L3477)
272. [src L353] OQ-24 | Whether the tasklist P2 loop needs a third full Stage 7 review after the second pa -> REPRESENTED (report L3478)
273. [src L354] OQ-25 | Whether `v2` line-insensitive fingerprint is intended | Question in research/02 ga -> REPRESENTED (report L3479)
274. [src L356] ### 6.12.9 Undecidable conflicts for adjudication -> REPRESENTED (report L3481)
275. [src L362] C-01 | core-shape-and-finding-contract | C-S1, CO-1, CO-2, CO-3, CO-4, CL-X11 (placement), -> REPRESENTED (report L3487)
276. [src L363] C-02 | ledger-clearing-and-verdict-authority | LG-1, VM-2, VM-4 (policy), C-S9 (semantics) -> REPRESENTED (report L3488)
277. [src L364] C-03 | merge-verdict-policy-and-quorum | C-S4, VM-5, FX-9, FX-10 | Deterministic any-block -> REPRESENTED (report L3489)
278. [src L365] C-04 | reflect-tier2-engine-composition | RE-1, RE-4, CV-8 (intent), CV-4, CV-5 | Engine B -> REPRESENTED (report L3490)
279. [src L366] C-05 | consumer-entry-effect-and-delivery | C-S7, CO-25, CO-35 | Reflect UC-1 stays the on -> REPRESENTED (report L3491)
280. [src L367] C-06 | limits-repair-policy | C-S1 (repair), CO-5, CO-6, FX-1 | Normalise before the parse -> REPRESENTED (report L3492)
281. [src L368] C-07 | dispatch-and-launch-mechanism | C-S6, CO-10, FX-13 | The core defines per-environme -> REPRESENTED (report L3493)
282. [src L369] C-08 | run-record-and-served-model-capture | CO-19, CO-20, CO-11 (adapter), C-S10, FX-16,  -> REPRESENTED (report L3494)
283. [src L370] C-09 | panel-resolution-and-tier-source | C-S5, C-S16, CO-12, CO-13, FX-14, FX-15 | One pa -> REPRESENTED (report L3495)
284. [src L371] C-10 | pr-review-wire-format-and-slot | CO-27, CO-29 | Adapter now: panel findings (findin -> REPRESENTED (report L3496)
285. [src L372] C-11 | rfqa-first-step-and-readonly-scope | CO-30, CO-31 (first change), FX-8, FX-20 | Sta -> REPRESENTED (report L3497)
286. [src L373] C-12 | collaboration-exchange-capability | CL-X1, CL-X2, CL-X3, CL-X4, CL-X6, CL-X7, CL-X9 -> REPRESENTED (report L3498)
287. [src L374] C-13 (debate slot name X-13) | process-redesign-modules | CO-23, CO-24 | Sweep-Sheet-shape -> REPRESENTED (report L3499)
288. [src L375] C-14 (debate slot name X-14) | eval-acceptance-and-harness-owner | CO-15, CO-16, CO-17, FX -> REPRESENTED (report L3500)
289. [src L376] C-15 (debate slot name X-15) | tasklist-medium-and-fidelity-vocab | SV-6, CO-41, C-S3 (tas -> REPRESENTED (report L3501)
290. [src L380] ### 6.12.9.1 Adjudication outcomes (added by the adjudication fold, item 5.50) -> REPRESENTED (report L3505)
291. [src L386] C-01 | core-shape-and-finding-contract | Variant B as base, with one engine-local change f -> REPRESENTED (report L3511)
292. [src L387] C-02 | ledger-clearing-and-verdict-authority | Variant B (explicit per-row verification) a -> REPRESENTED (report L3512)
293. [src L388] C-03 | merge-verdict-policy-and-quorum | Variant A as base, merged as the hybrid the debat -> REPRESENTED (report L3513)
294. [src L389] C-04 | reflect-tier2-engine-composition | Variant 1 (A) as base, merged as H-C04: a code-o -> REPRESENTED (report L3514)
295. [src L390] C-05 | consumer-entry-effect-and-delivery | Variant A as base, merged as the hybrid: entry -> REPRESENTED (report L3515)
296. [src L391] C-06 | limits-repair-policy | Variant B as base, hybrid: itemised drop record with a `bloc -> REPRESENTED (report L3516)
297. [src L392] C-07 | dispatch-and-launch-mechanism | Variant 2 (B) as base, hybrid: the core launches no -> REPRESENTED (report L3517)
298. [src L393] C-08 | run-record-and-served-model-capture | Variant 1 (A) as base, hybrid: per-agent obse -> REPRESENTED (report L3518)
299. [src L394] C-09 | panel-resolution-and-tier-source | Variant B as base, hybrid: the Coder env slots t -> REPRESENTED (report L3519)
300. [src L395] C-10 | pr-review-wire-format-and-slot | Variant A as base, resolution C10-R: a separate ma -> REPRESENTED (report L3520)
301. [src L396] C-11 | rfqa-first-step-and-readonly-scope | Variant B as base, hybrid: a lens-level first  -> REPRESENTED (report L3521)
302. [src L397] C-12 | collaboration-exchange-capability | A staged hybrid on Variant A: core now = H1, H2 -> REPRESENTED (report L3522)
303. [src L398] C-13 (X-13) | process-redesign-modules | Variant A (Sweep-Sheet-shaped) as base, hybrid: b -> REPRESENTED (report L3523)
304. [src L399] C-14 (X-14) | eval-acceptance-and-harness-owner | Variant A as base, hybrid: A's three acc -> REPRESENTED (report L3524)
305. [src L400] C-15 (X-15) | tasklist-medium-and-fidelity-vocab | Variant B as base, hybrid: the module-d -> REPRESENTED (report L3525)
306. [src L404] ### 6.12.10 Summary of the conflict log -> REPRESENTED (report L3529)
307. [src L408] A: C-S1..C-S16 | 16 | 10 | 6 (C-S1, C-S4, C-S5, C-S6, C-S7, C-S16) | -> REPRESENTED (report L3533)
308. [src L409] B: FX-1..FX-22 | 22 | 21 | 1 (FX-15: the default for distinctness) | -> REPRESENTED (report L3534)
309. [src L410] C: CL-X1..CL-X17, CL-C01..CL-C19 | 36 | 14 | 22 | -> REPRESENTED (report L3535)
310. [src L411] D: SV, VM, LG, CV, RE | 31 | 25 | 6 (SV-6, VM-2, VM-4 policy, VM-5 quorum, LG-1, RE-1) | -> REPRESENTED (report L3536)
311. [src L412] E: CO-1..CO-41 | 41 | 21 | 20 | -> REPRESENTED (report L3537)
312. [src L413] F: DATA-1..DATA-15 | 15 | 15 | 0 | -> REPRESENTED (report L3538)
313. [src L414] G: DOC-1..DOC-13, RX-1..RX-15 | 28 | 28 | 0 | -> REPRESENTED (report L3539)
314. [src L415] Total | 189 | 134 | 55 (15 adjudication slots) | -> REPRESENTED (report L3540)
315. [src L421] MINOR is never blocking (both parsers); two blocking rules are shipped and selected by len -> REPRESENTED (report L3546)
316. [src L422] Category, lens, severity and reference grammars are module-declared inputs validated by th -> REPRESENTED (report L3547)
317. [src L423] Review caps agree at 2 fix cycles (3 reviews) in the loop, rf-qa, `/task` and pr-submit's  -> REPRESENTED (report L3548)
318. [src L424] The verdict is derived from rows on every read and never stored; a round after ESCALATE is -> REPRESENTED (report L3549)
319. [src L425] The enforced convergence threshold is 0.80; the wrapper degrades on single vendor; the lin -> REPRESENTED (report L3550)
320. [src L426] Deterministic shadow steps (contract, card and verdict-file writers, parity) move into cod -> REPRESENTED (report L3551)
321. [src L427] The input is a manifest by role with a hash and an "opened" record; H1 and H2 are uncondit -> REPRESENTED (report L3552)
322. [src L428] The served model is recorded from the transcript, never from the orchestrator; cost sits o -> REPRESENTED (report L3553)
323. [src L429] Reviewers are mechanically read-only and the reviser is a separate role | FX-8, CO-31 | -> REPRESENTED (report L3554)
324. [src L430] E1 and E2 are one derivation set; no E2 default panel composition enters the core; E2 data -> REPRESENTED (report L3555)
325. [src L431] Documentation that the code contradicts is decided for the code (the 13 claims and 15 rese -> REPRESENTED (report L3556)
COUNT synthesis/synth-06-conflict-log.md: 325

## synthesis/synth-05-options.md
Entries = every non-blank line (heading, paragraph, table data row; table header and separator rows excluded). Mechanical check: of 783 non-blank lines, 704 are verbatim lines of the report (grep -F -x); 75 are headings whose "#" level differs and whose text is found in the report; 4 are title/metadata lines of the synthesis file. Report line is the locator; the match is by whole-line text (meaning), not by id.
1. [src L1] # Synthesis 05: Options Analysis -> not a content line (title/metadata) [no report line]
2. [src L3] **Date:** 2026-11-14 -> REPRESENTED (report L3)
3. [src L4] **Status:** Complete -> not a content line (title/metadata) [no report line]
4. [src L5] **Report sections produced:** 6.1 to 6.11 (one block per decision axis) of the T -> not a content line (title/metadata) [no report line]
5. [src L6] **Research question context:** which ONE unified central Review Panel design cap -> not a content line (title/metadata) [no report line]
6. [src L7] **Rule of this file:** options and evidence only. No winner is picked here (the  -> REPRESENTED (report L2144)
7. [src L9] ## Reading guide -> REPRESENTED (report L44)
8. [src L13] Citation keys | `R01` to `R18` = `research/01-*.md` to `research/18-*.md` (R01 o -> REPRESENTED (report L2150)
9. [src L14] Line cites | `path:line` is at HEAD `50d4d2b9d` (branch `ironbelly/shadow-runs`) -> REPRESENTED (report L2151)
10. [src L15] Fact status | Only claims the research files tagged [CODE-VERIFIED] (read, re-ru -> REPRESENTED (report L2152)
11. [src L16] Effort (XS, S, M, L, XL) | Qualitative size of the option as the evidence shows  -> REPRESENTED (report L2153)
12. [src L17] Risk (Low, Medium, High) | Per-option attribute: how likely, on the evidence, th -> REPRESENTED (report L2154)
13. [src L18] "Blocks future PR review or rf-qa replacement" | yes / no / how: whether the opt -> REPRESENTED (report L2155)
14. [src L19] Web evidence | External context only (W01 to W04). It never overrides a code-ver -> REPRESENTED (report L2156)
15. [src L21] ## 6.1 Core shape -> REPRESENTED (report L45)
16. [src L23] **Description:** which structure carries the unified Review Panel. The four cand -> REPRESENTED (report L2160)
17. [src L25] **How it works:** -> REPRESENTED (report L2162)
18. [src L29] A: v2 kernel core | `findings_v2.py` + `cluster.py` + `verify_cmd.py` + `manifes -> REPRESENTED (report L2166)
19. [src L30] B: v1 package core | `findings.py`, `ledger.py`, `merge_cmd.py`, `panel.py` stay -> REPRESENTED (report L2167)
20. [src L31] C: thin shared contract | The core is a contract: finding schema with module-dec -> REPRESENTED (report L2168)
21. [src L32] D: fix and defer | Only the harness fixes (H1 to H4), the whole-finding drop D1  -> REPRESENTED (report L2169)
22. [src L34] **Shared facts that bear on all four options (R-cited, all [CODE-VERIFIED]):** -> REPRESENTED (report L2171)
23. [src L38] E2 changed no product code at any commit; E2 = data, harness and designs. A unif -> REPRESENTED (report L2175)
24. [src L39] `findings.py`, `ledger.py`, `merge_cmd.py` are byte-identical in E1 HEAD, E2 tip -> REPRESENTED (report L2176)
25. [src L40] v1 and v2 share only the block container, `refs_norm`, `_ID`, `_check_flat` and  -> REPRESENTED (report L2177)
26. [src L41] E1 (v2 kernel) is a superset of E3s (v1) for panel resolution and the line gramm -> REPRESENTED (report L2178)
27. [src L42] `cli/review` and `cli/reflect` are independent packages at HEAD (no import in ei -> REPRESENTED (report L2179)
28. [src L43] Reflect has two Tier-2 engines that share only `contract.py` (`derive_verdict`,  -> REPRESENTED (report L2180)
29. [src L44] The installed-only E3 variants re-implement the loop in stdlib-only scripts (no  -> REPRESENTED (report L2181)
30. [src L45] The CLI ledger is the only multi-reviewer merge in the codebase; the variants ar -> REPRESENTED (report L2182)
31. [src L47] ### Option A: v2 kernel as the core, v1 loop as a thin module -> REPRESENTED (report L2184)
32. [src L51] Effort | L (basis: the ledger and merge path must accept citation-only findings; -> REPRESENTED (report L2188)
33. [src L52] Risk | Medium (basis: six of eight pins read in R03 section 2 encode the fail-op -> REPRESENTED (report L2189)
34. [src L53] Reuse of existing code | `findings_v2.py` (304 lines; parser already accepts `an -> REPRESENTED (report L2190)
35. [src L54] Files and systems affected | `src/superclaude/cli/review/{findings,findings_v2,l -> REPRESENTED (report L2191)
36. [src L55] Pros | The kernel was built for reflect and already has the pieces a panel needs -> REPRESENTED (report L2192)
37. [src L56] Cons | v2 has no ledger, rounds or reviser (R01 row 7); one bad line makes a v2  -> REPRESENTED (report L2193)
38. [src L58] ### Option B: v1 package as the core, reflect as a module -> REPRESENTED (report L2195)
39. [src L62] Effort | M to L; rated M (basis: the loop engine, ledger, merge, spec brief and  -> REPRESENTED (report L2199)
40. [src L63] Risk | Medium (basis: the reflect shadow path consumes `findings-v2`, `cluster`, -> REPRESENTED (report L2200)
41. [src L64] Reuse of existing code | v1 `findings.py` (457), `ledger.py` (494), `merge_cmd.p -> REPRESENTED (report L2201)
42. [src L65] Files and systems affected | v1 files above; reflect adapter in `src/superclaude -> REPRESENTED (report L2202)
43. [src L66] Pros | The shipped consumer is spec-panel (loop bullets identical in src and plu -> REPRESENTED (report L2203)
44. [src L67] Cons | v1 has one location type: quoted `anchor` 12..200 characters, required (` -> REPRESENTED (report L2204)
45. [src L69] ### Option C: thin shared contract, per-module engines -> REPRESENTED (report L2206)
46. [src L73] Effort | M (basis: contract-level work only; engines are not merged; R13 section -> REPRESENTED (report L2210)
47. [src L74] Risk | Medium (basis: contract-constant names are reserved under `cli/` and a du -> REPRESENTED (report L2211)
48. [src L75] Reuse of existing code | `_ID` and `_check_flat` (`findings.py:26`, `:79-87`); ` -> REPRESENTED (report L2212)
49. [src L76] Files and systems affected | a new contract surface in `src/superclaude/cli/revi -> REPRESENTED (report L2213)
50. [src L77] Pros | Few cells are identical across E1, E2, E3 (id regex, findings-v1 grammar, -> REPRESENTED (report L2214)
51. [src L78] Cons | Duplicates survive: two ledgers with different statuses (C-5; R03 section -> REPRESENTED (report L2215)
52. [src L80] ### Option D: fix the harness and the two parsers only, defer unification -> REPRESENTED (report L2217)
53. [src L84] Effort | S (basis: H1 to H4, D1 in `findings.py` and `findings_v2.py`, B-1; R09  -> REPRESENTED (report L2221)
54. [src L85] Risk | Low for breakage; Medium for leaving verified defects in the path of the  -> REPRESENTED (report L2222)
55. [src L86] Reuse of existing code | `findings.py:104,118` and `findings_v2.py:80,111,126,13 -> REPRESENTED (report L2223)
56. [src L87] Files and systems affected | `findings.py`, `findings_v2.py`, the parse step bef -> REPRESENTED (report L2224)
57. [src L88] Pros | Smallest change on the evidenced largest loss: 92 finding lines dropped,  -> REPRESENTED (report L2225)
58. [src L89] Cons | Leaves open, all verified at HEAD: a citation-only finding crashes the v1 -> REPRESENTED (report L2226)
59. [src L91] ### Options comparison table (6.1) -> REPRESENTED (report L2228)
60. [src L95] Maintainability | One pipeline for loop and reflect; v1 stays as a module with i -> REPRESENTED (report L2232)
61. [src L96] Integration complexity | High: ledger/merge/annotate become locator-agnostic (R1 -> REPRESENTED (report L2233)
62. [src L97] Reuse potential | Highest for kernel pieces (manifest, cluster, verify, reflect  -> REPRESENTED (report L2234)
63. [src L98] Evidence strength | Code-verified assets and blockers (R01 P-a to P-e, R02 secti -> REPRESENTED (report L2235)
64. [src L99] Blocks future PR review or rf-qa replacement | Partly: file:line is representabl -> REPRESENTED (report L2236)
65. [src L101] **Axis status: UNDECIDABLE-BY-EVIDENCE between A, B and C.** Reason: no run comp -> REPRESENTED (report L2238)
66. [src L103] ## 6.2 Finding contract -> REPRESENTED (report L46)
67. [src L105] **Description:** the line-level record every reviewer returns and every downstre -> REPRESENTED (report L2242)
68. [src L107] **How it works (the contracts that exist at HEAD or in E2/E3; all [CODE-VERIFIED -> REPRESENTED (report L2244)
69. [src L111] `findings-v1` (`findings.py`) | quoted `anchor` 12..200 characters, required; `a -> REPRESENTED (report L2248)
70. [src L112] `findings-v2` (`findings_v2.py`) | `citations[{role, path, line_start, line_end, -> REPRESENTED (report L2249)
71. [src L113] Reflect card (E1 shadow) | markdown card with `persona:`, `model_class:`, `model -> REPRESENTED (report L2250)
72. [src L114] `reflect-reviewer` agent output | markdown Deviations table, `file:line` locatio -> REPRESENTED (report L2251)
73. [src L115] Installed variants | `review_ledger.py` rows `{grade, rule, wrong_outcome, ancho -> REPRESENTED (report L2252)
74. [src L116] E2 `panel-msg/1` | message, not a finding: `anchor` 12..200 exact substring, `it -> REPRESENTED (report L2253)
75. [src L117] `pr_submit.Finding` | `path`, one integer `line`, `in_diff`, `original_line` | 1 -> REPRESENTED (report L2254)
76. [src L119] Facts that bear on every option: the two parsers cannot feed each other's downst -> REPRESENTED (report L2256)
77. [src L121] ### Option 1: keep two grammars and add adapters (status quo plus) -> REPRESENTED (report L2258)
78. [src L125] Effort | XS (basis: no parser change; adapters only, R13 M11, P1) | -> REPRESENTED (report L2262)
79. [src L126] Risk | Medium (basis: the verified incompatibilities stay: P-a, P-b, C-2, C-4 in -> REPRESENTED (report L2263)
80. [src L127] Reuse of existing code | both parsers as they are; `card_convert.py`; `pr_submit -> REPRESENTED (report L2264)
81. [src L128] Files and systems affected | adapter modules per consumer; no change to `finding -> REPRESENTED (report L2265)
82. [src L129] Pros | No pinned test or contract changes (R12 section 2.1; R06 section 8(a)). O -> REPRESENTED (report L2266)
83. [src L130] Cons | A line valid in v1 can be invalid in v2 (`calibrated_confidence`, probe P -> REPRESENTED (report L2267)
84. [src L132] ### Option 2: one open superset grammar, vocabularies declared by each module -> REPRESENTED (report L2269)
85. [src L136] Effort | M (basis: R13 M1 to M3 and R05 Unit 8: location list with optional anch -> REPRESENTED (report L2273)
86. [src L137] Risk | Medium (basis: tests pin the closed sets and the limits; one fact has two -> REPRESENTED (report L2274)
87. [src L138] Reuse of existing code | `findings_v2.check_finding` structure (`:84-187`), `_ch -> REPRESENTED (report L2275)
88. [src L139] Files and systems affected | `findings.py`, `findings_v2.py`, `ledger.py` (locat -> REPRESENTED (report L2276)
89. [src L140] Pros | Both existing grammars become projections of one record; v2 already accep -> REPRESENTED (report L2277)
90. [src L141] Cons | A later whitelist would be a breaking change to every E2 tool that tags l -> REPRESENTED (report L2278)
91. [src L143] ### Option 3: one closed, versioned contract with a registered extension namespa -> REPRESENTED (report L2280)
92. [src L147] Effort | L (basis: new schema id, key whitelist, validators, migration of every  -> REPRESENTED (report L2284)
93. [src L148] Risk | Medium (basis: breaks E2's in-line tags and the research-time tolerance o -> REPRESENTED (report L2285)
94. [src L149] Reuse of existing code | the variants' reject-unknown-keys patterns (`review_led -> REPRESENTED (report L2286)
95. [src L150] Files and systems affected | new schema module in `cli/review/`; every producer  -> REPRESENTED (report L2287)
96. [src L151] Pros | The record projects onto export formats: SARIF (`ruleId`, relative path,  -> REPRESENTED (report L2288)
97. [src L152] Cons | Breaks every tool that adds keys today (R02 section 3). The E3 variants s -> REPRESENTED (report L2289)
98. [src L154] ### Sub-decision 6.2.b: input and brief contract (what the reviewer is told and  -> REPRESENTED (report L2291)
99. [src L158] (a) per-module briefs as today | five brief families deliver input four ways: pa -> REPRESENTED (report L2295)
100. [src L159] (b) core brief assembler with an input manifest by role | ordered roles `{role,  -> REPRESENTED (report L2296)
101. [src L160] (c) patch the loop brief only | name the driving document, state parser limits,  -> REPRESENTED (report L2297)
102. [src L162] ### Options comparison table (6.2) -> REPRESENTED (report L2299)
103. [src L166] Maintainability | Two grammars and two fingerprints stay (R01 C-1 to C-4). | One -> REPRESENTED (report L2303)
104. [src L167] Integration complexity | Lowest for existing consumers; every new consumer write -> REPRESENTED (report L2304)
105. [src L168] Reuse potential | Keeps both parsers. | Reuses v2 structure and the lens/role ta -> REPRESENTED (report L2305)
106. [src L169] Evidence strength | Code-verified incompatibilities (R01 probes). | Code-verifie -> REPRESENTED (report L2306)
107. [src L170] Blocks future PR review or rf-qa replacement | Partly: PR works through its own  -> REPRESENTED (report L2307)
108. [src L172] **Axis status:** `UNDECIDABLE-BY-EVIDENCE` for open versus closed unknown-key po -> REPRESENTED (report L2309)
109. [src L174] ## 6.3 Limits policy -> REPRESENTED (report L47)
110. [src L176] **Description:** what the pipeline does with a finding line that breaks a parser -> REPRESENTED (report L2313)
111. [src L178] **How it works (today and per option):** today both parsers drop the whole line  -> REPRESENTED (report L2315)
112. [src L182] merges examined (merge = row x package) | 264 (89 rows x 3 packages) | R02 secti -> REPRESENTED (report L2319)
113. [src L183] finding lines dropped, all severities ("92") | 92: anchor over 200 = 56, anchor2 -> REPRESENTED (report L2320)
114. [src L184] reviewer-package runs with `block ok false` ("80") | 80 (a count of reviewer run -> REPRESENTED (report L2321)
115. [src L185] blocking finding lines dropped ("49") | 49: anchor over 200 = 24, anchor2 over 2 -> REPRESENTED (report L2322)
116. [src L186] verdicts flipped FAIL to PASS | 3 (`audit2.json` `verdict_flip`), plus 5 total-l -> REPRESENTED (report L2323)
117. [src L187] the per-model list (luna 30, ember 33, wonder 14, glm 7, haiku 7, grok 1) | sums -> REPRESENTED (report L2324)
118. [src L189] ### Option 1: truncate (E2 "H2 normaliser") -> REPRESENTED (report L2326)
119. [src L193] Effort | S (basis: one pre-parse step; cut `anchor` and `anchor2` to 200 and `cl -> REPRESENTED (report L2330)
120. [src L194] Risk | Medium (basis: recovery is an upper bound; luna's measured verbatim ancho -> REPRESENTED (report L2331)
121. [src L195] Reuse of existing code | `card_convert.py:199-201` (the only truncation in the p -> REPRESENTED (report L2332)
122. [src L196] Files and systems affected | a pre-parse repair step before `findings_v2.parse_b -> REPRESENTED (report L2333)
123. [src L197] Pros | Addresses up to 88 of 92 dropped lines (95.7 percent) and 48 of 49 blocki -> REPRESENTED (report L2334)
124. [src L198] Cons | Cannot address 4 lines (3 bad severity, 1 bad refs; 1 of them blocking) ( -> REPRESENTED (report L2335)
125. [src L200] ### Option 2: reject and re-ask once -> REPRESENTED (report L2337)
126. [src L204] Effort | M (basis: needs the reviewer session to persist or a second prompt that -> REPRESENTED (report L2341)
127. [src L205] Risk | Medium (basis: recovery rate unmeasured; the E2 spike for it was not run, -> REPRESENTED (report L2342)
128. [src L206] Reuse of existing code | E1's one bounded re-ask and the first-pass metric (`SKI -> REPRESENTED (report L2343)
129. [src L207] Files and systems affected | the dispatch layer (session persistence, `--session -> REPRESENTED (report L2344)
130. [src L208] Pros | All 92 lines are re-askable in principle, including the 4 that truncation -> REPRESENTED (report L2345)
131. [src L209] Cons | Adds wall-clock time for each affected reviewer: 44 reviewer-runs held a  -> REPRESENTED (report L2346)
132. [src L211] ### Option 3: keep drop-and-warn (today) and add visibility -> REPRESENTED (report L2348)
133. [src L215] Effort | XS (basis: stop keeping only the first error; store dropped counts and  -> REPRESENTED (report L2352)
134. [src L216] Risk | High (basis: recovers nothing; the 3 flipped verdicts and 5 total-loss me -> REPRESENTED (report L2353)
135. [src L217] Reuse of existing code | `ledger.py:127-134` (warning keeps the error count and  -> REPRESENTED (report L2354)
136. [src L218] Files and systems affected | `ledger.py`, `merge_cmd.py`; an audit-style conserv -> REPRESENTED (report L2355)
137. [src L219] Pros | No behaviour change and no model call. It is the form E2 reported against -> REPRESENTED (report L2356)
138. [src L220] Cons | Recovers 0 of 92 and 0 of 49 (R02 section 5.2). Under findings-v2 cluster -> REPRESENTED (report L2357)
139. [src L222] ### Option 4: truncate length violations, then one re-ask for the rest (E2 R-02) -> REPRESENTED (report L2359)
140. [src L226] Effort | M (basis: both components plus `dropped_lines` accounting) | -> REPRESENTED (report L2363)
141. [src L227] Risk | Medium (basis: inherits the unmeasured parts of options 1 and 2) | -> REPRESENTED (report L2364)
142. [src L228] Reuse of existing code | as options 1 and 2; E2's one real row recorded `reask:  -> REPRESENTED (report L2365)
143. [src L229] Files and systems affected | as options 1 and 2; E2 requirement text `merged-req -> REPRESENTED (report L2366)
144. [src L230] Pros | Truncation covers the 88 length lines without calls and re-ask covers the -> REPRESENTED (report L2367)
145. [src L231] Cons | The E1 "never normalizes" rule conflicts with the truncation step (R02 se -> REPRESENTED (report L2368)
146. [src L233] **Related levers (not alternatives):** generate the limits in the brief from the -> REPRESENTED (report L2370)
147. [src L235] ### Options comparison table (6.3) -> REPRESENTED (report L2372)
148. [src L239] Maintainability | One deterministic step; must cover every limited field. | Need -> REPRESENTED (report L2376)
149. [src L240] Integration complexity | Low: before `parse_block`. | High: sessions or a second -> REPRESENTED (report L2377)
150. [src L241] Reuse potential | `card_convert` truncation (`:199-201`). | E1 re-ask text and m -> REPRESENTED (report L2378)
151. [src L242] Evidence strength | Recovery upper bound from recounted reasons (R02 section 5.2 -> REPRESENTED (report L2379)
152. [src L243] Blocks future PR review or rf-qa replacement | No: the step is parser-level; it  -> REPRESENTED (report L2380)
153. [src L245] **Axis status:** `UNDECIDABLE-BY-EVIDENCE` between truncate, re-ask and the comb -> REPRESENTED (report L2382)
154. [src L247] ## 6.4 Quorum and verdict -> REPRESENTED (report L48)
155. [src L249] **Description:** how many valid reviewers a round needs, who decides what is blo -> REPRESENTED (report L2386)
156. [src L251] **How it works (verdict authority today, [CODE-VERIFIED], R03 section 4.2):** -> REPRESENTED (report L2388)
157. [src L255] Master Review Loop (prose, `spec-panel.md:260`) | reviewer types `verdict:` last -> REPRESENTED (report L2392)
158. [src L256] CLI ledger (`ledger.py`) | reviewer types `severity` and `blocking` per line; th -> REPRESENTED (report L2393)
159. [src L257] Variant ledger (`review_ledger.py`) | reviewer proposes grade, rule, `wrong_outc -> REPRESENTED (report L2394)
160. [src L258] Variant stoprule (`stoprule.py`) | reviewer types claims only; a blind `finding- -> REPRESENTED (report L2395)
161. [src L259] Variant diffgate (`diffgate.py`) | reviewer types `FINDING`/`PRIOR` lines | scri -> REPRESENTED (report L2396)
162. [src L260] Reflect `contract.derive_verdict` (`contract.py:138-260`) | orchestrator or engi -> REPRESENTED (report L2397)
163. [src L262] **Reproduced at HEAD (R03 section 1, [CODE-VERIFIED] by execution):** D-1 a row  -> REPRESENTED (report L2399)
164. [src L264] ### Option 1: keep the CLI ledger rule (reviewer-typed `blocking`, any one valid -> REPRESENTED (report L2401)
165. [src L268] Effort | XS | -> REPRESENTED (report L2405)
166. [src L269] Risk | Medium (basis: three reproduced fail-open paths; whether they are bugs or -> REPRESENTED (report L2406)
167. [src L270] Reuse of existing code | `ledger.py`, `ledger_cmd.py` (exit codes 0/10/11, `:13` -> REPRESENTED (report L2407)
168. [src L271] Files and systems affected | none beyond documentation; the loop brief and ledge -> REPRESENTED (report L2408)
169. [src L272] Pros | Fail-closed at the 0-valid boundary is intentional and tested (R03 sectio -> REPRESENTED (report L2409)
170. [src L273] Cons | One valid reviewer of N passes (D-2), silence clears rows (D-1), a human  -> REPRESENTED (report L2410)
171. [src L275] ### Option 2: ledger-derived verdict with a recorded quorum and explicit clearin -> REPRESENTED (report L2412)
172. [src L279] Effort | L (basis: R03 section 5 lists seven implications I-1 to I-7; six of the -> REPRESENTED (report L2416)
173. [src L280] Risk | Medium (basis: pinned tests are named as features, for example `test_clea -> REPRESENTED (report L2417)
174. [src L281] Reuse of existing code | variant semantics to port, not import (`review_ledger.p -> REPRESENTED (report L2418)
175. [src L282] Files and systems affected | `ledger.py`, `ledger_cmd.py`, `merge_cmd.py`, `mani -> REPRESENTED (report L2419)
176. [src L283] Pros | Unanswered means open, the inverse of the CLI rule (R03 section 4.1). The -> REPRESENTED (report L2420)
177. [src L284] Cons | The variants have no valid repeated result and no measured effect (R14 se -> REPRESENTED (report L2421)
178. [src L286] ### Option 3: reflect `derive_verdict` as the shared verdict shell, fed from led -> REPRESENTED (report L2423)
179. [src L290] Effort | M (basis: the function is pure and exists; a mapper from ledger and man -> REPRESENTED (report L2427)
180. [src L291] Risk | Medium (basis: the 36-test verdict matrix and contract 1.8.0 pins bind an -> REPRESENTED (report L2428)
181. [src L292] Reuse of existing code | `contract.py:138-382` (4-state map, 14 degraded trigger -> REPRESENTED (report L2429)
182. [src L293] Files and systems affected | `cli/reflect/contract.py` becomes shared; a ledger- -> REPRESENTED (report L2430)
183. [src L294] Pros | Supplies the missing DEGRADED state for partial panels: three of four rev -> REPRESENTED (report L2431)
184. [src L295] Cons | It reads orchestrator-typed contract fields, not findings or ledger rows  -> REPRESENTED (report L2432)
185. [src L297] ### Option 4: a separate blind grader decides blocking; the reviewer never types -> REPRESENTED (report L2434)
186. [src L301] Effort | L (basis: 14 subcommands and 11 coordinator steps in the stoprule proto -> REPRESENTED (report L2438)
187. [src L302] Risk | High (basis: installed-only, no valid live run; the integrity check retur -> REPRESENTED (report L2439)
188. [src L303] Reuse of existing code | `finding-grader` agent (35 lines, tool Read), `stoprule -> REPRESENTED (report L2440)
189. [src L304] Files and systems affected | new product skill and agent; a CLI subcommand set;  -> REPRESENTED (report L2441)
190. [src L305] Pros | Strongest fail-closed rule of the four: "silence never passes"; a hand-ty -> REPRESENTED (report L2442)
191. [src L306] Cons | A grader decides blocking per claim; it is not a multi-reviewer merge (R0 -> REPRESENTED (report L2443)
192. [src L308] **Cap policy (sub-axis, [CODE-VERIFIED] R12 section 4):** the master loop, rf-qa -> REPRESENTED (report L2445)
193. [src L310] **External evidence (W01, context only):** no peer-reviewed study compares any-p -> REPRESENTED (report L2447)
194. [src L312] ### Options comparison table (6.4) -> REPRESENTED (report L2449)
195. [src L316] Maintainability | Defects stay; pins named as features. | One ledger with derive -> REPRESENTED (report L2453)
196. [src L317] Integration complexity | None. | High: ledger, manifest, CLI, brief text. | Medi -> REPRESENTED (report L2454)
197. [src L318] Reuse potential | Existing ledger. | Variant discipline plus CLI clustering. | ` -> REPRESENTED (report L2455)
198. [src L319] Evidence strength | Reproduced defects and pins (R03 section 1, 2). | Reproduced -> REPRESENTED (report L2456)
199. [src L320] Blocks future PR review or rf-qa replacement | How: the panel verdict is ignored -> REPRESENTED (report L2457)
200. [src L322] **Axis status:** `UNDECIDABLE-BY-EVIDENCE`. Reasons: (1) the quorum count (all,  -> REPRESENTED (report L2459)
201. [src L324] ## 6.5 Dispatch -> REPRESENTED (report L49)
202. [src L326] **Description:** how a resolved reviewer is launched and how the model that actu -> REPRESENTED (report L2463)
203. [src L328] **How it works (four mechanisms that exist, [CODE-VERIFIED], R04 sections 3.1 to -> REPRESENTED (report L2465)
204. [src L332] Unit named at dispatch | class word on the Agent `model` argument, or agent fron -> REPRESENTED (report L2469)
205. [src L333] Reaches a non-first model of a tier | no: class word to `ANTHROPIC_DEFAULT_*_MOD -> REPRESENTED (report L2470)
206. [src L334] Reviewer tools | read-only agent (`reflect-reviewer.md:5-8`) | none (plain compl -> REPRESENTED (report L2471)
207. [src L335] Served model recorded by | transcript only (`message.model` of the sidechain) |  -> REPRESENTED (report L2472)
208. [src L337] Product facts: `launch` is empty under the `gateway` environment (`review-tiers. -> REPRESENTED (report L2474)
209. [src L339] ### Option 1: dispatch by class word through the orchestrator Agent call -> REPRESENTED (report L2476)
210. [src L343] Effort | XS (exists in the reflect legacy rotation and shadow mode) | -> REPRESENTED (report L2480)
211. [src L344] Risk | Medium (basis: collapse and class drift below) | -> REPRESENTED (report L2481)
212. [src L345] Reuse of existing code | `agents/reflect-reviewer.md` (tools Read, Grep, Glob, s -> REPRESENTED (report L2482)
213. [src L346] Files and systems affected | `src/superclaude/skills/sc-reflect-protocol/` (edit -> REPRESENTED (report L2483)
214. [src L347] Pros | Reviewers are mechanically read-only (`reflect-reviewer.md:5-8`). Officia -> REPRESENTED (report L2484)
215. [src L348] Cons | The Agent `model` enum is sonnet, opus, haiku, fable; it cannot name tier -> REPRESENTED (report L2485)
216. [src L350] ### Option 2: raw model id per reviewer process (`claude -p --model <id>`) -> REPRESENTED (report L2487)
217. [src L354] Effort | M (basis: the E2 launcher `run-reviewer.sh` (87 lines) and its judge an -> REPRESENTED (report L2491)
218. [src L355] Risk | Medium (basis: not read-only by construction; fallback overwrite; hooks a -> REPRESENTED (report L2492)
219. [src L356] Reuse of existing code | `E2@6c09843:.../tools/run-reviewer.sh` identity check ( -> REPRESENTED (report L2493)
220. [src L357] Files and systems affected | a new launcher in the product (none exists, R04 sec -> REPRESENTED (report L2494)
221. [src L358] Pros | Reaches every gateway model, which tier aliases do not (`probe.json` alia -> REPRESENTED (report L2495)
222. [src L359] Cons | A raw-id request still passes the shim's tier failover (`local-gateway-al -> REPRESENTED (report L2496)
223. [src L361] ### Option 3: in-process HTTP transport by raw id (swarm) -> REPRESENTED (report L2498)
224. [src L365] Effort | M (basis: `cli/swarm` transports and `cli/reflect/ensemble.py` exist; t -> REPRESENTED (report L2502)
225. [src L366] Risk | Medium (basis: no tool loop; requested id recorded; tasklist text only) | -> REPRESENTED (report L2503)
226. [src L367] Reuse of existing code | `swarm/transports/openai_compat.py`, `ensemble.py:276-2 -> REPRESENTED (report L2504)
227. [src L368] Files and systems affected | `cli/swarm/`, `cli/reflect/{ensemble,fallback,_dive -> REPRESENTED (report L2505)
228. [src L369] Pros | Runs headless without the Agent tool; `T2Model0N` reaches non-first model -> REPRESENTED (report L2506)
229. [src L370] Cons | Workers get one user message and no session (`openai_compat.py:384-388`), -> REPRESENTED (report L2507)
230. [src L372] ### Option 4: resolution as the dispatch contract (the tier file's `launch` map  -> REPRESENTED (report L2509)
231. [src L376] Effort | L (basis: no launcher exists; the `launch` map would need values for ga -> REPRESENTED (report L2513)
232. [src L377] Risk | Medium (basis: three hand-kept tier lists with only a count test; `muse-e -> REPRESENTED (report L2514)
233. [src L378] Reuse of existing code | resolution fields `alias`, `launch`, `model`, `fallback -> REPRESENTED (report L2515)
234. [src L379] Files and systems affected | `review-tiers.default.json`, `panel.py`, `panel_cmd -> REPRESENTED (report L2516)
235. [src L380] Pros | Data-driven: `launch` and `alias` are already printed per reviewer; one o -> REPRESENTED (report L2517)
236. [src L381] Cons | Not implemented anywhere. The reflect profile caps `launch` at sonnet, op -> REPRESENTED (report L2518)
237. [src L383] ### Sub-decision 6.5.b: the run record that carries served model, usage and stag -> REPRESENTED (report L2520)
238. [src L387] (a) per-run `events.jsonl` + manifest state machine + `review-telemetry` export  -> REPRESENTED (report L2524)
239. [src L388] (b) extend `review-telemetry/1` to `/2` only | add an `agent_run` kind, value ty -> REPRESENTED (report L2525)
240. [src L389] (c) manifest gains `usage` per attempt | store the attempt payload instead of it -> REPRESENTED (report L2526)
241. [src L390] (d) keep the five E2 result schemas | none | none | five schemas, keys and units -> REPRESENTED (report L2527)
242. [src L392] The memory write is a third lock-free LLM read-modify-write store (`SKILL.md:585 -> REPRESENTED (report L2529)
243. [src L394] ### Options comparison table (6.5) -> REPRESENTED (report L2531)
244. [src L398] Maintainability | Depends on workspace env state; class not reproducible across  -> REPRESENTED (report L2535)
245. [src L399] Integration complexity | Lowest (exists). | Medium: product launcher, session ha -> REPRESENTED (report L2536)
246. [src L400] Reuse potential | `reflect-reviewer`, `panel resolve`. | E2 identity check and l -> REPRESENTED (report L2537)
247. [src L401] Evidence strength | Observed collapse and class drift in 15 combo runs (R07 E1-F -> REPRESENTED (report L2538)
248. [src L402] Blocks future PR review or rf-qa replacement | How: class words cannot reach non -> REPRESENTED (report L2539)
249. [src L404] **Axis status:** `UNDECIDABLE-BY-EVIDENCE` between mechanisms: the choice depend -> REPRESENTED (report L2541)
250. [src L406] ## 6.6 Collaboration -> REPRESENTED (report L50)
251. [src L408] **Description:** whether reviewers exchange anything before the merge, and in wh -> REPRESENTED (report L2545)
252. [src L410] **How it works (the five E2 packages, [CODE-VERIFIED], R09 sections 1 to 3):** -> REPRESENTED (report L2547)
253. [src L414] F3 Move Radar (r1) | one catalogue move text or a "source.md not opened" check | -> REPRESENTED (report L2551)
254. [src L415] F4 Sweeper (r2) | repo facts (paths, counts, `path:line`, the command) | a helpe -> REPRESENTED (report L2552)
255. [src L416] F1 Axis-Flip (r3) | a peer anchor or a gap-card line plus one move, in a digest  -> REPRESENTED (report L2553)
256. [src L417] F7 Flag-Adjudicate (r4) | a card (anchor plus move) | a flagger model via `panel -> REPRESENTED (report L2554)
257. [src L418] F6 Deflection (r5) | task ids not covered by any finished scout (`kind: "coverag -> REPRESENTED (report L2555)
258. [src L420] Only F1 needs no hook; four hook scripts implement one skeleton four times (bake -> REPRESENTED (report L2557)
259. [src L422] ### Option 1: no collaboration in the core (independent blind reviewers) -> REPRESENTED (report L2559)
260. [src L426] Effort | XS (exists) | -> REPRESENTED (report L2563)
261. [src L427] Risk | Low (basis: nothing new is added; the central gain of exchange is simply  -> REPRESENTED (report L2564)
262. [src L428] Reuse of existing code | E1 shadow reviewers are mutually blind (`reviewer-spec. -> REPRESENTED (report L2565)
263. [src L429] Files and systems affected | none | -> REPRESENTED (report L2566)
264. [src L430] Pros | Consistent with the E1 design and the E2 process-redesign principle of no -> REPRESENTED (report L2567)
265. [src L431] Cons | Recorded reviewer overlap is sparse: 7 unchained multi-reviewer clusters  -> REPRESENTED (report L2568)
266. [src L433] ### Option 2: a static move kit or class-recipe text in every brief (no communic -> REPRESENTED (report L2570)
267. [src L437] Effort | S (basis: brief text per module; no transport) | -> REPRESENTED (report L2574)
268. [src L438] Risk | Medium (basis: the only measured cost is large on sonnet, +59 percent ela -> REPRESENTED (report L2575)
269. [src L439] Reuse of existing code | class cards `recipe_text` and `question_template` (R10  -> REPRESENTED (report L2576)
270. [src L440] Files and systems affected | the briefs (`document_review_loop_prompts.md`, `rev -> REPRESENTED (report L2577)
271. [src L441] Pros | The cheapest design if no exchange beats it: "the harness fixes plus the  -> REPRESENTED (report L2578)
272. [src L442] Cons | The effect on found defects is unmeasured. Both catalogues were induced f -> REPRESENTED (report L2579)
273. [src L444] ### Option 3: an optional between-phase exchange capability (F1 style) -> REPRESENTED (report L2581)
274. [src L448] Effort | M (basis: two prompts and a seal by process exit; no hook; the engine o -> REPRESENTED (report L2585)
275. [src L449] Risk | Medium (basis: no clean measured success in any runtime) | -> REPRESENTED (report L2586)
276. [src L450] Reuse of existing code | `panel-msg/1` kinds and the digest design (R02 section  -> REPRESENTED (report L2587)
277. [src L451] Files and systems affected | a second-pass step in the dispatch layer (6.5); a m -> REPRESENTED (report L2588)
278. [src L452] Pros | The only family that needs neither a hook nor a model-side write, so the  -> REPRESENTED (report L2589)
279. [src L453] Cons | Both r3 A3 smoke rows record `phase2_timeout: 1`; the A1 baseline alone s -> REPRESENTED (report L2590)
280. [src L455] ### Option 4: optional in-flight exchange through hooks (F3, F4, F6, F7) behind  -> REPRESENTED (report L2592)
281. [src L459] Effort | XL (basis: a shared hook library replacing four copies, board, seal, me -> REPRESENTED (report L2596)
282. [src L460] Risk | High (basis: no measured gain; hooks bind to main-thread `claude -p` sess -> REPRESENTED (report L2597)
283. [src L461] Reuse of existing code | the hook skeleton (R09 section 1.3); `reflect --resume` -> REPRESENTED (report L2598)
284. [src L462] Files and systems affected | the dispatch layer (persistence on, per-session `-- -> REPRESENTED (report L2599)
285. [src L463] Pros | The most mature designs: five packages with partial gate-0 results and a  -> REPRESENTED (report L2600)
286. [src L464] Cons | The packages' own hooks skip subagent calls (`r1 radar-hook.sh:24-28`, `r -> REPRESENTED (report L2601)
287. [src L466] ### Options comparison table (6.6) -> REPRESENTED (report L2603)
288. [src L470] Maintainability | Nothing to maintain. | Per-module card text. | A second-pass s -> REPRESENTED (report L2607)
289. [src L471] Integration complexity | None. | Brief only. | Dispatch layer. | Dispatch layer  -> REPRESENTED (report L2608)
290. [src L472] Reuse potential | Existing. | Class cards, brief builder. | `panel-msg/1`, r3 de -> REPRESENTED (report L2609)
291. [src L473] Evidence strength | E1 and E2 independent-reviewer data; no exchange measured. | -> REPRESENTED (report L2610)
292. [src L474] Blocks future PR review or rf-qa replacement | No. | No; recipes need a Grep/Glo -> REPRESENTED (report L2611)
293. [src L476] **Axis status:** `UNDECIDABLE-BY-EVIDENCE`. Reason: no measurement compares any  -> REPRESENTED (report L2613)
294. [src L478] ## 6.7 Process redesign -> REPRESENTED (report L51)
295. [src L480] **Description:** whether the panel gets a written process in front of the free r -> REPRESENTED (report L2617)
296. [src L482] **How it works (E2 process-redesign brainstorm, design only, [CODE-VERIFIED] as  -> REPRESENTED (report L2619)
297. [src L486] Pre-pass | serial deterministic script, no model, byte-identical for the same in -> REPRESENTED (report L2623)
298. [src L487] What a reviewer gets | up to 12 typed items from extractors E1 to E7, each assig -> REPRESENTED (report L2624)
299. [src L488] What a reviewer returns | normal findings block | findings block plus a per-revi -> REPRESENTED (report L2625)
300. [src L489] Post-run | script checks and promotion, no re-ask | quote checks; a PROBLEM row  -> REPRESENTED (report L2626)
301. [src L490] Binding to reviewers | items assigned by the script | lens table bound to model  -> REPRESENTED (report L2627)
302. [src L492] Both rest on class cards C1 to C8 (`id, name, definition, recipe_text, question_ -> REPRESENTED (report L2629)
303. [src L494] **What E1 already has that either redesign would otherwise duplicate (R10 Unit 6 -> REPRESENTED (report L2631)
304. [src L496] **What is decidable about the classes (R10 Unit 7):** recorded instances of C2,  -> REPRESENTED (report L2633)
305. [src L498] ### Option 1: Sweep Sheet (script pre-pass assigns typed items) -> REPRESENTED (report L2635)
306. [src L502] Effort | XL (basis: extractors E1 to E7 have 0 code; hold-out ground truth and p -> REPRESENTED (report L2639)
307. [src L503] Risk | High (basis: nothing implemented; extractor E6 is "experimental ... high  -> REPRESENTED (report L2640)
308. [src L504] Reuse of existing code | the sidecar container, `findings.flat`, `verify_cmd._ch -> REPRESENTED (report L2641)
309. [src L505] Files and systems affected | a new pre-pass module; `verify_cmd.py`, `findings_v -> REPRESENTED (report L2642)
310. [src L506] Pros | Deterministic and model-free; "the script never writes a claim" (`merged- -> REPRESENTED (report L2643)
311. [src L507] Cons | C1, C3, C7 extractors are candidate listers only (R10 Unit 7); the gate D -> REPRESENTED (report L2644)
312. [src L509] ### Option 2: Recipe Ledger (written recipes by lens, per-reviewer row block) -> REPRESENTED (report L2646)
313. [src L513] Effort | XL (basis: recipes, lens table, row block, post-run checks, promotion;  -> REPRESENTED (report L2650)
314. [src L514] Risk | High (basis: recipes assume a shell and `reflect-reviewer` has none; the  -> REPRESENTED (report L2651)
315. [src L515] Reuse of existing code | recipe texts R-C1 to R-C8 (`merged-requirements.md:738- -> REPRESENTED (report L2652)
316. [src L516] Files and systems affected | briefs, panel slot data (slot keys are closed: `_SL -> REPRESENTED (report L2653)
317. [src L517] Pros | No pre-pass and no extractor. Needs no extra process before the review. | -> REPRESENTED (report L2654)
318. [src L518] Cons | R-C4 says "run it on a scratch string with Bash" and R-C8 uses `git grep  -> REPRESENTED (report L2655)
319. [src L520] ### Option 3: neither now; keep the isolated panel with the harness and brief fi -> REPRESENTED (report L2657)
320. [src L524] Effort | S (basis: H1, H2 and brief items B-1 to B-5, B-7, all open at HEAD in s -> REPRESENTED (report L2661)
321. [src L525] Risk | Medium (basis: no valid-era E2 row exceeds 4 of 14 defects, and three of  -> REPRESENTED (report L2662)
322. [src L526] Reuse of existing code | the existing briefs and parsers | -> REPRESENTED (report L2663)
323. [src L527] Files and systems affected | the loop and reflect briefs, parser limit step (6.3 -> REPRESENTED (report L2664)
324. [src L528] Pros | Smallest change; every redesign number is a planning value and no arm has -> REPRESENTED (report L2665)
325. [src L529] Cons | Leaves the recurring recorded classes C2, C4, C5, C6, C8 to chance (R10 U -> REPRESENTED (report L2666)
326. [src L531] ### Option 4: the core absorbs only the reusable pieces, without choosing either -> REPRESENTED (report L2668)
327. [src L535] Effort | M (basis: card schema as data, the existing sidecar, flat-based quote c -> REPRESENTED (report L2672)
328. [src L536] Risk | Medium (basis: promotion and demotion stay on HOLD; the row block's name  -> REPRESENTED (report L2673)
329. [src L537] Reuse of existing code | `coverage.json` container, `findings.flat`, `verify_cmd -> REPRESENTED (report L2674)
330. [src L538] Files and systems affected | `cli/review/` (card loader, optional block parser), -> REPRESENTED (report L2675)
331. [src L539] Pros | Avoids building a second assignment container and a second normaliser (R1 -> REPRESENTED (report L2676)
332. [src L540] Cons | A card schema without extractors has no producer. The row block's rename  -> REPRESENTED (report L2677)
333. [src L542] ### Options comparison table (6.7) -> REPRESENTED (report L2679)
334. [src L546] Maintainability | Extractors per class and module. | Recipes per class; row bloc -> REPRESENTED (report L2683)
335. [src L547] Integration complexity | New pre-pass step and assignment. | Lens binding and a  -> REPRESENTED (report L2684)
336. [src L548] Reuse potential | Sidecar, `flat`, `_check`, Wave 1B for C2. | Sidecar, `_check` -> REPRESENTED (report L2685)
337. [src L549] Evidence strength | Design only; 0 code; planning numbers (R10 Unit 5). | Design -> REPRESENTED (report L2686)
338. [src L550] Blocks future PR review or rf-qa replacement | How: classes are plan-review evid -> REPRESENTED (report L2687)
339. [src L552] **Axis status:** `UNDECIDABLE-BY-EVIDENCE` between Sweep Sheet and Recipe Ledger -> REPRESENTED (report L2689)
340. [src L554] ## 6.8 Reflect engine -> REPRESENTED (report L52)
341. [src L556] **Description:** what to do with reflect's two Tier-2 implementations and the St -> REPRESENTED (report L2693)
342. [src L558] **How it works (the two engines, [CODE-VERIFIED], R06 section 7):** -> REPRESENTED (report L2695)
343. [src L562] Reached by | `ReflectRunner._audit_once` for every production `standard` or `dee -> REPRESENTED (report L2699)
344. [src L563] Reviewers | external proxy models in `T2Model0N` slots, text in and out; tasklis -> REPRESENTED (report L2700)
345. [src L564] Calibration and evidence gate | none | blind `confidence-calibrator` and a manda -> REPRESENTED (report L2701)
346. [src L565] Deviation classes | all zero and `regression_present: False` by construction (`e -> REPRESENTED (report L2702)
347. [src L566] Contract | `contract_version 1.0`, 32 keys, 10 outside the frozen lists, 89 of 1 -> REPRESENTED (report L2703)
348. [src L567] Diversity evidence | from the requested model id stamped by the transport (`Work -> REPRESENTED (report L2704)
349. [src L568] Executor exclusion | none in production (`executor_model` reaches only the Tier- -> REPRESENTED (report L2705)
350. [src L569] Verdict | `derive_verdict` 0/10/11/2; HALTED and the `--fix` loop are structural -> REPRESENTED (report L2706)
351. [src L571] Stage 2 exit at HEAD: `OVERALL: FAIL (shadow runs 13 of 20)`, EV-1 failure rate  -> REPRESENTED (report L2708)
352. [src L573] **Must stay byte-identical (R06 section 8(a)):** the consumer-read 1.8.0 field n -> REPRESENTED (report L2710)
353. [src L575] ### Option 1: keep both engines and reconcile vocabulary only -> REPRESENTED (report L2712)
354. [src L579] Effort | S (basis: one decision per vocabulary point plus doc fixes; R06 section -> REPRESENTED (report L2716)
355. [src L580] Risk | Medium (basis: the production wrapper and the skill stay two producers of -> REPRESENTED (report L2717)
356. [src L581] Reuse of existing code | everything as is; `contract.py`, `panel_lint.py`, `runn -> REPRESENTED (report L2718)
357. [src L582] Files and systems affected | `SKILL.md` (edit fence `test_shadow_skill_contract. -> REPRESENTED (report L2719)
358. [src L583] Pros | No pins change if the vocabulary decisions go the way the pins already re -> REPRESENTED (report L2720)
359. [src L584] Cons | Documents claim the wrapper "spawns an executor-disjoint reflect ensemble -> REPRESENTED (report L2721)
360. [src L586] ### Option 2: the swarm engine gains calibrator, evidence validator, executor ex -> REPRESENTED (report L2723)
361. [src L590] Effort | XL (basis: transports are plain completions with no tool loop, so groun -> REPRESENTED (report L2727)
362. [src L591] Risk | High (basis: 89 of 110 stable contract names are absent from engine A's c -> REPRESENTED (report L2728)
363. [src L592] Reuse of existing code | `ensemble.py`, `fallback.py`, `_diversity.py`, `runner. -> REPRESENTED (report L2729)
364. [src L593] Files and systems affected | `cli/reflect/*`, `cli/swarm/*`, the `reflect-review -> REPRESENTED (report L2730)
365. [src L594] Pros | Keeps the code-driven, headless, credit-free (`--transport stub`) path as -> REPRESENTED (report L2731)
366. [src L595] Cons | The missing capabilities are exactly what engine B has: grounding chain,  -> REPRESENTED (report L2732)
367. [src L597] ### Option 3: retire the swarm engine; the wrapper runs the skill panel -> REPRESENTED (report L2734)
368. [src L601] Effort | L (basis: the production path reaches the skill only from a test double -> REPRESENTED (report L2738)
369. [src L602] Risk | High (basis: the loss list below) | -> REPRESENTED (report L2739)
370. [src L603] Reuse of existing code | the skill panel, `panel_lint`, `reflect_shadow_exit.py` -> REPRESENTED (report L2740)
371. [src L604] Files and systems affected | `runner.py` Tier-2 branch, `ensemble.py`, `fallback -> REPRESENTED (report L2741)
372. [src L605] Pros | One engine with grounded reviewers, calibration, validation and deviation -> REPRESENTED (report L2742)
373. [src L606] Cons | Loses, per R06 section 8(d): headless operation without the Claude Code A -> REPRESENTED (report L2743)
374. [src L608] ### Option 4: engine B's data model and kernel as the shared core inside engine  -> REPRESENTED (report L2745)
375. [src L612] Effort | L (basis: a contract serializer, a card writer that owns file names, a  -> REPRESENTED (report L2749)
376. [src L613] Risk | Medium (basis: the byte-identical set above must hold; R06 labels this co -> REPRESENTED (report L2750)
377. [src L614] Reuse of existing code | `panel_lint._ev1` and `lint_panel_contract`, `reflect_s -> REPRESENTED (report L2751)
378. [src L615] Files and systems affected | `cli/reflect/{runner,contract,panel_lint,ensemble}. -> REPRESENTED (report L2752)
379. [src L616] Pros | All observed Stage 2 failures are deterministic file, copy or key-set def -> REPRESENTED (report L2753)
380. [src L617] Cons | Precondition: engine A's contract has no producer for `remediation_*` or  -> REPRESENTED (report L2754)
381. [src L619] ### Sub-decision 6.8.b: where the panel enters for workflow and tasklist (DO4, R -> REPRESENTED (report L2756)
382. [src L623] (a) keep reflect UC-1 as the only entry | the panel is selected inside reflect ( -> REPRESENTED (report L2760)
383. [src L624] (b) direct panel call replacing `:89` and `:1630` | new flag set and new contrac -> REPRESENTED (report L2761)
384. [src L626] ### Sub-decision 6.8.c: one convergence threshold and one single-vendor posture -> REPRESENTED (report L2763)
385. [src L630] convergence score routing | skill: at least 0.75 PASS, at least 0.60 PARTIAL, be -> REPRESENTED (report L2767)
386. [src L631] single vendor | skill: "warn-only in v1.0" (`SKILL.md:839`, `:1481`) | code: DEG -> REPRESENTED (report L2768)
387. [src L633] ### Options comparison table (6.8) -> REPRESENTED (report L2770)
388. [src L637] Maintainability | Two producers, two contract shapes. | One engine, large new ma -> REPRESENTED (report L2774)
389. [src L638] Integration complexity | Low. | Very high. | High. | Medium to high. | -> REPRESENTED (report L2775)
390. [src L639] Reuse potential | Everything. | `ensemble`, `fallback`. | Skill, lint, exit scri -> REPRESENTED (report L2776)
391. [src L640] Evidence strength | Verified code and doc conflicts (R06 sections 4, 5). | Verif -> REPRESENTED (report L2777)
392. [src L641] Blocks future PR review or rf-qa replacement | No by itself; neither engine is a -> REPRESENTED (report L2778)
393. [src L643] **Axis status:** `DECIDED-BY-EVIDENCE` for the convergence threshold (0.80) and  -> REPRESENTED (report L2780)
394. [src L645] ## 6.9 Evaluation -> REPRESENTED (report L53)
395. [src L647] **Description:** what counts as acceptance evidence that a unified panel design  -> REPRESENTED (report L2784)
396. [src L649] **How it works (what exists, [CODE-VERIFIED] or recomputed unless marked, R07, R -> REPRESENTED (report L2786)
397. [src L653] Ground truth | none for the 15 combo or 13 pilot runs (`FINDINGS.md:3`, `:42`);  -> REPRESENTED (report L2790)
398. [src L654] Judge | none; AI-labelled 50 cluster pairs (three labelers; TP 21, FP 4, FN 1, T -> REPRESENTED (report L2791)
399. [src L655] Pre-set rule | code gate `scripts/reflect_shadow_exit.py` (13 of 20 runs); thres -> REPRESENTED (report L2792)
400. [src L656] Audits and gates | exit script defects: an empty legacy baseline counts as 0.0 ( -> REPRESENTED (report L2793)
401. [src L657] Metric definitions | structural and cost signals only | judge-blocking 65 versus -> REPRESENTED (report L2794)
402. [src L659] **Independence (R16 section 6):** the E1 package is byte-identical to the E2 des -> REPRESENTED (report L2796)
403. [src L661] ### Option 1: E2 ground truth and blind judge as the acceptance set (tasklist re -> REPRESENTED (report L2798)
404. [src L665] Effort | M (basis: the GT and judge scripts live only on the E2 branch; they mus -> REPRESENTED (report L2802)
405. [src L666] Risk | Medium (basis: small, concentrated, single-judge, one-run-derived GT; E1  -> REPRESENTED (report L2803)
406. [src L667] Reuse of existing code | `ground-truth.json` (3 files), 319 `score.json*` files  -> REPRESENTED (report L2804)
407. [src L668] Files and systems affected | a tracked fixture set and judge wrapper (`.dev/eval -> REPRESENTED (report L2805)
408. [src L669] Pros | The only ground truth with mechanical checks and a written drop reason pe -> REPRESENTED (report L2806)
409. [src L670] Cons | Sixteen items from three plans, one implement run each, so a true novel d -> REPRESENTED (report L2807)
410. [src L672] ### Option 2: seeded defects with clean twins (E1 pilot design, E2 planted-set d -> REPRESENTED (report L2809)
411. [src L676] Effort | L (basis: 12 plans x 5 seeded defects designed, never planted; hold-out -> REPRESENTED (report L2813)
412. [src L677] Risk | Medium (basis: thresholds and stop rule were never approved; seeding auth -> REPRESENTED (report L2814)
413. [src L678] Reuse of existing code | `pilot-design.md` (defect kinds: ordering, missing acce -> REPRESENTED (report L2815)
414. [src L679] Files and systems affected | a seeded-plan generator and manifest (hash before t -> REPRESENTED (report L2816)
415. [src L680] Pros | The only route to a ground truth where no implement outcome exists: refle -> REPRESENTED (report L2817)
416. [src L681] Cons | Designed and never run; thresholds T-1 to T-10 are `draft-for-owner-revie -> REPRESENTED (report L2818)
417. [src L683] ### Option 3: a pre-registered hold-out protocol (hash before run, new packages, -> REPRESENTED (report L2820)
418. [src L687] Effort | L (basis: rule, values file and analysis script committed before the fi -> REPRESENTED (report L2824)
419. [src L688] Risk | Medium (basis: design only; both source designs state low power: "The pla -> REPRESENTED (report L2825)
420. [src L689] Reuse of existing code | the two brainstorm designs' rules (collaboration `merge -> REPRESENTED (report L2826)
421. [src L690] Files and systems affected | commit ordering discipline, hold-out store, analysi -> REPRESENTED (report L2827)
422. [src L691] Pros | Proves rule-before-data by `git log` instead of mtime (R16 section 4.1 ro -> REPRESENTED (report L2828)
423. [src L692] Cons | A second judge on 15 percent of run-packages is the same Opus family, so  -> REPRESENTED (report L2829)
424. [src L694] ### Option 4: structural acceptance only (executable `verify-run`, Tier S), qual -> REPRESENTED (report L2831)
425. [src L698] Effort | M (basis: audits B, D, F re-run today from committed data; A, C, E need -> REPRESENTED (report L2835)
426. [src L699] Risk | Low (basis: structural checks only; but see Cons) | -> REPRESENTED (report L2836)
427. [src L700] Reuse of existing code | the uniform `flags.tsv` layout of audits A to F, `repor -> REPRESENTED (report L2837)
428. [src L701] Files and systems affected | the ledger entry (raw, kept, rejected counts: `ledg -> REPRESENTED (report L2838)
429. [src L702] Pros | Removes the verified classes: exact-key lookups, judge completion checked -> REPRESENTED (report L2839)
430. [src L703] Cons | It measures orchestration and structure, not review quality: the Stage 2  -> REPRESENTED (report L2840)
431. [src L705] ### Sub-decision 6.9.b: who owns judge, ground-truth registry and `verify-run` -> REPRESENTED (report L2842)
432. [src L709] O1 kernel-owned invariants and a `superclaude review verify-run` command | serve -> REPRESENTED (report L2846)
433. [src L710] O2 repo-relative `scripts/` plus tests | judge, anonymiser, table builder, GT re -> REPRESENTED (report L2847)
434. [src L711] O3 stay under `.dev/` | everything as is with paths fixed | matches `.dev/README -> REPRESENTED (report L2848)
435. [src L713] ### Options comparison table (6.9) -> REPRESENTED (report L2850)
436. [src L717] Maintainability | Fixture and scripts with paths as arguments. | Generator plus  -> REPRESENTED (report L2854)
437. [src L718] Integration complexity | Medium (import from the E2 branch). | High. | High. | M -> REPRESENTED (report L2855)
438. [src L719] Reuse potential | Highest (data exists). | E1 pilot design, E2 planted-set desig -> REPRESENTED (report L2856)
439. [src L720] Evidence strength | Recomputed counts; weak inference (R08 section 7). | Design  -> REPRESENTED (report L2857)
440. [src L721] Blocks future PR review or rf-qa replacement | How: no GT for PR review or rf-qa -> REPRESENTED (report L2858)
441. [src L723] **Axis status:** `UNDECIDABLE-BY-EVIDENCE` on the metric of record (GT items fou -> REPRESENTED (report L2860)
442. [src L725] ## 6.10 Variants -> REPRESENTED (report L54)
443. [src L727] **Description:** what to do with the installed-only E3 variants (five `spec-pane -> REPRESENTED (report L2864)
444. [src L729] **How it works (state at 2026-11-14, [CODE-VERIFIED], R14 sections 3, 4, 7):** -> REPRESENTED (report L2866)
445. [src L733] 17 installed files (5 commands: armb 472, ponytail 483, diffgate 481, ledger 475 -> REPRESENTED (report L2870)
446. [src L734] They are not in `src/`, not in `.claude/`, not in `tests/`, and `superclaude ins -> REPRESENTED (report L2871)
447. [src L735] The variant commands lack `follow-up candidates` and the prompts hard gate; only -> REPRESENTED (report L2872)
448. [src L736] They re-implement the loop in stdlib-only scripts and share no code, schema stri -> REPRESENTED (report L2873)
449. [src L737] Phase-5 FINAL-REPORT states "Convergence not proven; no validated winner" (`FINA -> REPRESENTED (report L2874)
450. [src L738] PR #479 with #478 is the shipped prose-only substitute for the never-written ref -> REPRESENTED (report L2875)
451. [src L739] Personal-over-project shadowing: D9 measured that `~/.claude/commands/sc/spec-pa -> REPRESENTED (report L2876)
452. [src L741] **The six values and their evidence (R14 section 7.1):** -> REPRESENTED (report L2878)
453. [src L745] c1 owner counting rule (deferred, demoted, outside CRITICAL/MAJOR stays counted  -> REPRESENTED (report L2882)
454. [src L746] c2 scoped-PASS coverage statement | the fixed string `scoped PASS: changed lines -> REPRESENTED (report L2883)
455. [src L747] c3 fail-closed parsing | report level (`spec-panel.md:260`) | quorum is absent i -> REPRESENTED (report L2884)
456. [src L748] c4 provenance of the actual model | a self-reported header line (`:258`) | obser -> REPRESENTED (report L2885)
457. [src L749] c5 fix map per hunk | prose (`:263`); `fixmap-v1` exists in the CLI | the hunk-c -> REPRESENTED (report L2886)
458. [src L750] c6 computed re-review surface | prose only | `begin` hunk building (`diffgate.py -> REPRESENTED (report L2887)
459. [src L752] ### Option 1: keep the variants installed-only (status quo) -> REPRESENTED (report L2889)
460. [src L756] Effort | XS | -> REPRESENTED (report L2405)
461. [src L757] Risk | Medium (basis: private machine state that cannot be rebuilt from `src/`;  -> REPRESENTED (report L2894)
462. [src L758] Reuse of existing code | the installed scripts as they were measured (17 of 17 h -> REPRESENTED (report L2895)
463. [src L759] Files and systems affected | `~/.claude/commands/sc/spec-panel-*.md`, `~/.claude -> REPRESENTED (report L2896)
464. [src L760] Pros | Keeps the measured instruments runnable; nothing to do. | -> REPRESENTED (report L2897)
465. [src L761] Cons | They add five command names and four skill names to every session on this -> REPRESENTED (report L2898)
466. [src L763] ### Option 2: archive them (remove from `~/.claude/`, keep the `.dev/` archives) -> REPRESENTED (report L2900)
467. [src L767] Effort | XS (basis: a manual removal under `~/.claude/`, because the installer d -> REPRESENTED (report L2904)
468. [src L768] Risk | Low | -> REPRESENTED (report L2905)
469. [src L769] Reuse of existing code | the archives under `.dev/experiments/346-validation/pha -> REPRESENTED (report L2906)
470. [src L770] Files and systems affected | the same 17 installed files, removed; `docs/referen -> REPRESENTED (report L2907)
471. [src L771] Pros | No variant has a valid repeated result and none is recommended by the fin -> REPRESENTED (report L2908)
472. [src L772] Cons | The ponytail audit depends on an external plugin skill (`ponytail:ponytai -> REPRESENTED (report L2909)
473. [src L774] ### Option 3: fold the ideas into the core and modules (contracts, not scripts) -> REPRESENTED (report L2911)
474. [src L778] Effort | L (basis: the six values above; scripts total 7,589 lines and are not r -> REPRESENTED (report L2915)
475. [src L779] Risk | Medium (basis: each value is a design hypothesis; two have incident evide -> REPRESENTED (report L2916)
476. [src L780] Reuse of existing code | `fixmap-v1` and `ledger revise` (CLI), `review-capture/ -> REPRESENTED (report L2917)
477. [src L781] Files and systems affected | `ledger.py` (a status that records why a finding is -> REPRESENTED (report L2918)
478. [src L782] Pros | Carries what has incident evidence: provenance from the transcript (3 of  -> REPRESENTED (report L2919)
479. [src L783] Cons | The value of each fold is untested; "which status machine" (`resolved_che -> REPRESENTED (report L2920)
480. [src L785] **Not offered by the evidence:** promoting a variant script as a product path. N -> REPRESENTED (report L2922)
481. [src L787] ### Options comparison table (6.10) -> REPRESENTED (report L2924)
482. [src L791] Maintainability | Private state outside any checkout. | Nothing to maintain. | C -> REPRESENTED (report L2928)
483. [src L792] Integration complexity | None. | None. | Medium: ledger statuses, transcript rea -> REPRESENTED (report L2929)
484. [src L793] Reuse potential | Instruments only. | Archive only. | Highest for the six values -> REPRESENTED (report L2930)
485. [src L794] Evidence strength | 17 of 17 hashes verified (R14 section 3.1). | Final report:  -> REPRESENTED (report L2931)
486. [src L795] Blocks future PR review or rf-qa replacement | No: shadows nothing (R14 section  -> REPRESENTED (report L2932)
487. [src L797] **Axis status:** `UNDECIDABLE-BY-EVIDENCE` between keep and archive: it is a mac -> REPRESENTED (report L2934)
488. [src L799] ## 6.11 Future modules (PR code review and rf-qa / rf-qa-qualitative replacement -> REPRESENTED (report L55)
489. [src L801] **Description:** how the design treats the two future uses so neither is blocked -> REPRESENTED (report L2938)
490. [src L803] **How it works (blockers per use case, [CODE-VERIFIED], R13 section 7):** -> REPRESENTED (report L2940)
491. [src L807] PR | `pr_submit` needs one integer `line` per finding and drops findings without -> REPRESENTED (report L2944)
492. [src L808] PR | categories: findings-v2 accepts 6 spec categories, the router knows 18; an  -> REPRESENTED (report L2945)
493. [src L809] PR | lens vocabulary closed to spec, reflect-pre, reflect-post | `findings_v2.py -> REPRESENTED (report L2946)
494. [src L810] PR | 5 severity tiers with floors and ceilings against 3 labels plus `blocking`; -> REPRESENTED (report L2947)
495. [src L811] PR | two named third-party reviewers, bot identities, completion markers; `Outpu -> REPRESENTED (report L2948)
496. [src L812] PR | skill must run in the main session; fork-only rule is code (`pr_target_ok`, -> REPRESENTED (report L2949)
497. [src L813] rf-qa | rf-qa reviews and edits (`fix_authorization`); `/task` lens agents are " -> REPRESENTED (report L2950)
498. [src L814] rf-qa | checklist plus computed confidence gate `VERIFIED / (TOTAL - UNVERIFIABL -> REPRESENTED (report L2951)
499. [src L815] rf-qa | lens pack and floors: 8 standard lenses, 3+3 to 6+6 agents by output siz -> REPRESENTED (report L2952)
500. [src L816] rf-qa | 44 structured `subagent_type: rf-*` lines in 8 SKILL.md files and 175 pr -> REPRESENTED (report L2953)
501. [src L818] The minimum exposure R13 section 8 derives (M1 to M14): M1 finding location as a -> REPRESENTED (report L2955)
502. [src L820] ### Option 1: exposure-first (the core ships M1 to M14 now; no consumer is porte -> REPRESENTED (report L2957)
503. [src L824] Effort | M (basis: M1 to M4 touch the parser, ledger and template; M5 to M14 are -> REPRESENTED (report L2961)
504. [src L825] Risk | Medium (basis: closed sets and limits are pinned by tests; templates have -> REPRESENTED (report L2962)
505. [src L826] Reuse of existing code | `findings_v2` citations and roles; `reflect-reviewer`'s -> REPRESENTED (report L2963)
506. [src L827] Files and systems affected | `findings.py`, `findings_v2.py`, `ledger.py`, `pane -> REPRESENTED (report L2964)
507. [src L828] Pros | Cheap now and expensive to retrofit once E1, E2, E3 consumers pin the for -> REPRESENTED (report L2965)
508. [src L829] Cons | Ships interface for consumers that do not use it yet; M13 adds a behaviou -> REPRESENTED (report L2966)
509. [src L831] ### Option 2: consumer-first through adapters (PR via an adapter to `pr_submit.F -> REPRESENTED (report L2968)
510. [src L835] Effort | L (basis: an adapter and a completion rule for a local panel; the `/tas -> REPRESENTED (report L2972)
511. [src L836] Risk | Medium (basis: 50 test files pin `Finding`, the severity router and the F -> REPRESENTED (report L2973)
512. [src L837] Reuse of existing code | `reviewers.py` ("Everything after a normalized Finding  -> REPRESENTED (report L2974)
513. [src L838] Files and systems affected | a new adapter module (no `gh` or `git` in it), `pr_ -> REPRESENTED (report L2975)
514. [src L839] Pros | Smallest blast radius: `Finding`, `Severity` and the FSM stay untouched ( -> REPRESENTED (report L2976)
515. [src L840] Cons | A local panel has no completion marker, so its own completion rule is nee -> REPRESENTED (report L2977)
516. [src L842] ### Option 3: defer both (build neither exposure nor adapter; add on demand) -> REPRESENTED (report L2979)
517. [src L846] Effort | XS | -> REPRESENTED (report L2405)
518. [src L847] Risk | High (basis: location type, vocabularies and lens are hard-coded and pinn -> REPRESENTED (report L2984)
519. [src L848] Reuse of existing code | n/a | -> REPRESENTED (report L2985)
520. [src L849] Files and systems affected | none now; each later consumer retrofits the parser, -> REPRESENTED (report L2986)
521. [src L850] Pros | Scope discipline: R13 lists porting `auggie-review` or `pr_submit`, touch -> REPRESENTED (report L2987)
522. [src L851] Cons | Every later consumer retrofits after the formats are pinned (R13 section  -> REPRESENTED (report L2988)
523. [src L853] **External context (W04, W01; not evidence of repo behaviour):** a finding recor -> REPRESENTED (report L2990)
524. [src L855] ### Options comparison table (6.11) -> REPRESENTED (report L2992)
525. [src L859] Maintainability | One contract surface with module inputs. | Adapters per consum -> REPRESENTED (report L2996)
526. [src L860] Integration complexity | Medium: parser, ledger, templates. | Medium to high: ad -> REPRESENTED (report L2997)
527. [src L861] Reuse potential | `findings_v2` roles, `persona_lens`, `evidence-validator`. | ` -> REPRESENTED (report L2998)
528. [src L862] Evidence strength | Blockers verified (R13 section 7); the M-list is an interfac -> REPRESENTED (report L2999)
529. [src L863] Blocks future PR review or rf-qa replacement | No: it removes M1 to M4. | PR: no -> REPRESENTED (report L3000)
530. [src L865] **Axis status:** `UNDECIDABLE-BY-EVIDENCE` between exposure-first and consumer-f -> REPRESENTED (report L3002)
531. [src L867] ## Axis status summary (for the conflict log; no option is ranked) -> REPRESENTED (report L56)
532. [src L871] 6.1 Core shape | `UNDECIDABLE-BY-EVIDENCE` (A, B, C); D decided as "defers, leav -> REPRESENTED (report L3008)
533. [src L872] 6.2 Finding contract | `UNDECIDABLE-BY-EVIDENCE` (open versus closed keys; one w -> REPRESENTED (report L3009)
534. [src L873] 6.3 Limits policy | `UNDECIDABLE-BY-EVIDENCE` (truncate, re-ask, combination); k -> REPRESENTED (report L3010)
535. [src L874] 6.4 Quorum and verdict | `UNDECIDABLE-BY-EVIDENCE` | no quorum rule in code, no  -> REPRESENTED (report L3011)
536. [src L875] 6.5 Dispatch | `UNDECIDABLE-BY-EVIDENCE` (mechanism); served-model-from-transcri -> REPRESENTED (report L3012)
537. [src L876] 6.6 Collaboration | `UNDECIDABLE-BY-EVIDENCE` | no exchange arm measured against -> REPRESENTED (report L3013)
538. [src L877] 6.7 Process redesign | `UNDECIDABLE-BY-EVIDENCE` (Sweep Sheet versus Recipe Ledg -> REPRESENTED (report L3014)
539. [src L878] 6.8 Reflect engine | `UNDECIDABLE-BY-EVIDENCE` (engine choice); threshold (0.80) -> REPRESENTED (report L3015)
540. [src L879] 6.9 Evaluation | `UNDECIDABLE-BY-EVIDENCE` (metric of record, GT acceptability); -> REPRESENTED (report L3016)
541. [src L880] 6.10 Variants | `UNDECIDABLE-BY-EVIDENCE` (keep versus archive); "no variant val -> REPRESENTED (report L3017)
542. [src L881] 6.11 Future modules | `UNDECIDABLE-BY-EVIDENCE` (exposure-first versus consumer- -> REPRESENTED (report L3018)
543. [src L883] ## Adjudicated winners by axis (added by the adjudication fold, item 5.50) -> REPRESENTED (report L57)
544. [src L885] The rule at the top of this file (no winner is picked here) holds for every sect -> REPRESENTED (report L3022)
545. [src L889] 6.1 Core shape | C-01 `core-shape-and-finding-contract` | Option C: thin shared  -> REPRESENTED (report L3026)
546. [src L890] 6.2 Finding contract | C-01 (keys, locator) and C-10 `pr-review-wire-format-and- -> REPRESENTED (report L3027)
547. [src L891] 6.3 Limits policy | C-06 `limits-repair-policy` | Option 4 as modified: cut of t -> REPRESENTED (report L3028)
548. [src L892] 6.4 Quorum and verdict | C-02 `ledger-clearing-and-verdict-authority` and C-03 ` -> REPRESENTED (report L3029)
549. [src L893] 6.5 Dispatch | C-07 `dispatch-and-launch-mechanism` | Option 1 (class word on th -> REPRESENTED (report L3030)
550. [src L894] 6.5.b Run record | C-08 `run-record-and-served-model-capture` | Option (a) (per- -> REPRESENTED (report L3031)
551. [src L895] 6.6 Collaboration | C-12 `collaboration-exchange-capability` | Option 2 (static  -> REPRESENTED (report L3032)
552. [src L896] 6.7 Process redesign | X-13 (synth-06 C-13) `process-redesign-modules` | Option  -> REPRESENTED (report L3033)
553. [src L897] 6.8 Reflect engine | C-04 `reflect-tier2-engine-composition` | Option 1 (keep bo -> REPRESENTED (report L3034)
554. [src L898] 6.8.b Entry for workflow and tasklist | C-05 `consumer-entry-effect-and-delivery -> REPRESENTED (report L3035)
555. [src L899] 6.8.c Threshold and single vendor | none (decided by the code, synth-06 CV-1, CV -> REPRESENTED (report L3036)
556. [src L900] 6.9 Evaluation | X-14 (synth-06 C-14) `eval-acceptance-and-harness-owner` | A co -> REPRESENTED (report L3037)
557. [src L901] 6.9.b Harness owner | X-14 | Judge, ground-truth registry and `verify-run` as a  -> REPRESENTED (report L3038)
558. [src L902] 6.10 Variants | none (no debate slot) | not adjudicated | none | Open owner mach -> REPRESENTED (report L3039)
559. [src L903] 6.11 Future modules | C-10 and C-11 `rfqa-first-step-and-readonly-scope` | Optio -> REPRESENTED (report L3040)
560. [src L904] Tasklist Medium (6.2 sub-question) | X-15 (synth-06 C-15) `tasklist-medium-and-f -> REPRESENTED (report L3041)
561. [src L906] ## Interactions between axes (shared prerequisites, not an order) -> REPRESENTED (report L58)
562. [src L910] a locator-agnostic `annotate` and citation-keyed ledger rows (M1) | 6.1 A and B, -> REPRESENTED (report L3047)
563. [src L911] a repair step before `findings_v2.parse_block` | 6.3 options 1, 2, 4; 6.2 option -> REPRESENTED (report L3048)
564. [src L912] served model taken from the transcript | 6.5 all options and 6.5.b, 6.9 option 4 -> REPRESENTED (report L3049)
565. [src L913] the verdict function and its inputs | 6.4 option 3, 6.8 options 1 and 4, 6.8.c | -> REPRESENTED (report L3050)
566. [src L914] mechanically read-only reviewers | 6.5 option 1, 6.6 option 4, 6.7 option 2, 6.1 -> REPRESENTED (report L3051)
567. [src L915] the `blocking` boolean, label maps and the "Medium" token | 6.2, 6.4 cap policy, -> REPRESENTED (report L3052)
568. [src L916] one owner for class, vendor and tier lists | 6.5 option 4, 6.8 | R04 sections 5, -> REPRESENTED (report L3053)
569. [src L918] ## Corrected claims (the [CODE-CONTRADICTED] items met while writing; the correc -> REPRESENTED (report L59)
570. [src L922] E2 run-2: the `cli/review` change is "#519 + #518" | #519 alone changed 17 `cli/ -> REPRESENTED (report L3059)
571. [src L923] E2 run-2: "reflect has no panel/tier code" | true only for the code-driven wrapp -> REPRESENTED (report L3060)
572. [src L924] E2 run-1 D14: "No tasklist review step exists" | `sc-workflow-protocol/SKILL.md: -> REPRESENTED (report L3061)
573. [src L925] E2 run-1: "alias GT3 found once" | alias GT1 was found once; GT3 twice | R08 sec -> REPRESENTED (report L3062)
574. [src L926] `COMBO-REPORT.md:292`: dropped lines are "discarded with no error" | merge emits -> REPRESENTED (report L3063)
575. [src L927] `COMBO-REPORT.md:292`: "four verdicts flipped" | 3 flips plus 5 total-loss merge -> REPRESENTED (report L3064)
576. [src L928] the per-model list (luna 30, ember 33, ...) as the "49 blocking" breakdown | it  -> REPRESENTED (report L3065)
577. [src L929] "16 empty terra reviews" | 14 terra plus 2 luna | R08 section 5 | -> REPRESENTED (report L3066)
578. [src L930] slice 12: Medium "has four meanings" | at least six; seven severity vocabularies -> REPRESENTED (report L3067)
579. [src L931] slice 12: "185 spawn lines over 7 skills" | 175 prose spawn lines in 7 skills (2 -> REPRESENTED (report L3068)
580. [src L932] E2 run-2: `T2bModel01` "not referenced anywhere in src/ or tests/" | 18 line occ -> REPRESENTED (report L3069)
581. [src L933] E2 seed: "no missing-task category, defines no severity levels" | `missing-requi -> REPRESENTED (report L3070)
582. [src L934] E2 hand-off: "159 functions" | the notes' table sums to 179 | R17 open item (e)  -> REPRESENTED (report L3071)
583. [src L935] memory lesson: "fenced yaml calibration not parsed by cluster" | `cluster_cmd.py -> REPRESENTED (report L3072)
584. [src L936] pilot EV-1: "no `return-contract.yaml`" in runs 04, 08, 09 | the file exists and -> REPRESENTED (report L3073)
585. [src L937] "every shadow and combo contract records `requested-pinned`" | 1 of 15 combo con -> REPRESENTED (report L3074)
586. [src L938] `sc-tasklist-protocol` and `task-builder`: the wrapper spawns an executor-disjoi -> REPRESENTED (report L3075)
587. [src L939] slice 12: spec-panel depends on the rf-qa Fix Cycle and the plugin copy "softens -> REPRESENTED (report L3076)
588. [src L940] E1 FINDINGS: only A3 collapsed | the calibrator also lost its class in 6 of 15 c -> REPRESENTED (report L3077)
589. [src L941] E1 "7 multi-reviewer clusters among 216" | 13 clusters have 2 or more reviewers, -> REPRESENTED (report L3078)
590. [src L943] ## Open questions raised by the options analysis ([UNVERIFIED] items; none carri -> REPRESENTED (report L60)
591. [src L947] OQ-1 | whether `stoprule.py` rejects unknown keys; `fix_audit.py` and the archiv -> REPRESENTED (report L3084)
592. [src L948] OQ-2 | whether hooks and `--resume` behave the same for gateway model ids: only  -> REPRESENTED (report L3085)
593. [src L949] OQ-3 | whether a transcript adapter can supply per-agent usage and served model  -> REPRESENTED (report L3086)
594. [src L950] OQ-4 | all collaboration and process-redesign planning values (reach and act pro -> REPRESENTED (report L3087)
595. [src L951] OQ-5 | whether any decision record exists for the 0.75 in the skill prose (none  -> REPRESENTED (report L3088)
596. [src L952] OQ-6 | authorship of the E2 ground truth; whether T-1 to T-10 were approved beyo -> REPRESENTED (report L3089)
597. [src L953] OQ-7 | the six control and 427-arm measurement files of the phase-5 report are a -> REPRESENTED (report L3090)
598. [src L954] OQ-8 | whether the owner formally accepted #479 as the outcome of the refactor s -> REPRESENTED (report L3091)
599. [src L955] OQ-9 | the cost of a local panel per PR round | 6.11 | R13 P15 | -> REPRESENTED (report L3092)
600. [src L956] OQ-10 | the unit behind the gap between 109 raw-minus-kept findings and 92 dropp -> REPRESENTED (report L3093)
601. [src L957] OQ-11 | whether a truncated anchor still locates, and the re-ask recovery rate ( -> REPRESENTED (report L3094)
602. [src L958] OQ-12 | the pilot dispatch-collapse rate "6 of 9" cannot be re-derived (logs gon -> REPRESENTED (report L3095)
603. [src L959] OQ-13 | whether the gateway lists `muse-ember-1.0` today and whether it is tier- -> REPRESENTED (report L3096)
604. [src L960] OQ-14 | a common act-rate probe for the collaboration designs | 6.6 | R09 gap 7  -> REPRESENTED (report L3097)
605. [src L961] OQ-15 | how `hooks` blocks merge across settings sources (replace or add) | 6.6  -> REPRESENTED (report L3098)
606. [src L963] ## Coverage of the research files' Summary and Key Takeaways -> REPRESENTED (report L61)
607. [src L967] R01 overlap matrix | E2 changed no product code, shared core cells, conflicts C- -> REPRESENTED (report L3104)
608. [src L968] R02 finding contract | v1/v2 limits, `origin`, `T01.02`, 92/49 figures, truncate -> REPRESENTED (report L3105)
609. [src L969] R03 merge, ledger, verdict | D-1, D-2, D-11, D-13, pins, variants versus CLI led -> REPRESENTED (report L3106)
610. [src L970] R04 dispatch and tiers | four dispatch paths, served versus requested, `muse-emb -> REPRESENTED (report L3107)
611. [src L971] R05 input and brief | brief families, hard-codings, per-module exposures: 6.2.b, -> REPRESENTED (report L3108)
612. [src L972] R06 reflect two engines | engines, Stage 2 failures, byte-identical set, thresho -> REPRESENTED (report L3109)
613. [src L973] R07 E1 evidence | collapse, calibrator class loss, citation resolution faults, o -> REPRESENTED (report L3110)
614. [src L974] R08 E2 evidence | 92/80/49 units, 3 flips, GT concentration, j1, `fullpkg()`: 6. -> REPRESENTED (report L3111)
615. [src L975] R09 collaboration | five families, evidence status, H1 to H4, conflict classes,  -> REPRESENTED (report L3112)
616. [src L976] R10 process redesign | Sweep Sheet, Recipe Ledger, E1 container, classes, gates, -> REPRESENTED (report L3113)
617. [src L977] R11 tasklist and workflow | entry points, interfaces to keep, 36-test matrix: 6. -> REPRESENTED (report L3114)
618. [src L978] R12 spec-review consumers | canonical binary rule, Medium meanings, caps, brief  -> REPRESENTED (report L3115)
619. [src L979] R13 PR review and rf-qa | blockers, M1 to M14, call-site census: 6.11 | none | -> REPRESENTED (report L3116)
620. [src L980] R14 E3 variants | installed state, six values, #479 mapping, model-change recoun -> REPRESENTED (report L3117)
621. [src L981] R15 telemetry and run record | run-record options, D-17, D-23, memory: 6.5.b | n -> REPRESENTED (report L3118)
622. [src L982] R16 evaluation governance | acceptance tiers, independence, harness ownership, ` -> REPRESENTED (report L3119)
623. [src L983] R17 defect register | used as evidence rows (D-1 to D-13 numbering, reproduction -> REPRESENTED (report L3120)
624. [src L984] R18 repo constraints and branching | pins and gates named in Files-affected rows -> REPRESENTED (report L3121)
625. [src L985] W01 multi-model evidence | quorum and merge rules, diversity limits, bias, indep -> REPRESENTED (report L3122)
626. [src L986] W02 hooks and headless | hooks in subagents, `--bare`, `--restricted`, gateway i -> REPRESENTED (report L3123)
627. [src L987] W03 branch hierarchy and stacked PRs | none | the whole file: branch names, stac -> REPRESENTED (report L3124)
628. [src L988] W04 finding schemas and review bots | minimal record, export adapters, severity  -> REPRESENTED (report L3125)
629. [src L990] **Status: Complete** -> REPRESENTED (report L3127)
COUNT synthesis/synth-05-options.md: 629

## synthesis/synth-07-recommendation-architecture.md
Entries = every non-blank line (heading, paragraph, table data row incl. the 262 Debate Invariants rows; table header and separator rows excluded). Mechanical check: of 601 non-blank lines, 596 are verbatim lines of the report (grep -F -x); the 5 others are the title, the date, the 7.0.1 heading (found, heading level differs) and the end-of-file marker.
1. [src L1] # Synthesis 07: Recommendation and Architecture -> not a content line (title/metadata) [no report line]
2. [src L3] Date: 2026-11-14 -> not a content line (title/metadata) [no report line]
3. [src L4] Status: Complete -> REPRESENTED (report L2135)
4. [src L6] Source: research files 01 to 18 in `.dev/tasks/to-do/TASK-RESEARCH-review-panel- -> REPRESENTED (report L3571)
5. [src L8] Citation form: `rNN §x` = research file `NN-*.md`, section x. `HEAD` = commit 5 -> REPRESENTED (report L3573)
6. [src L10] E1 = reflect Tier 2 kernel, shadow mode and the model-combination experiment. E2 -> REPRESENTED (report L3575)
7. [src L12] --- -> REPRESENTED (report L8)
8. [src L14] ## 7. Recommendation -> REPRESENTED (report L3567)
9. [src L16] **Recommended approach:** **One Shared Review Panel Core: a Thin Shared Contract -> REPRESENTED (report L3578)
10. [src L18] #### 7.0.1 Name, owner wording and how the 15 outcomes combine -> REPRESENTED (report L64)
11. [src L20] Name and owner wording. The owner approved the wording "one shared Review Panel  -> REPRESENTED (report L3582)
12. [src L22] How the 15 outcomes combine into one design (every row is the outcome of the deb -> REPRESENTED (report L3586)
13. [src L26] C-01 core shape | Thin shared contract now; per-module engines (spec = v1, refle -> REPRESENTED (report L3590)
14. [src L27] C-06 limits repair | One repair step inside both `parse_block` functions behind  -> REPRESENTED (report L3591)
15. [src L28] C-02 ledger clearing | In the v1 engine: quorum-gated explicit clearing, silence -> REPRESENTED (report L3592)
16. [src L29] C-03 merge policy | In the v1 engine: any-blocking union (pluggable policy), quo -> REPRESENTED (report L3593)
17. [src L30] C-09 tier source | One reviewed tier file held in step with the env slot lists b -> REPRESENTED (report L3594)
18. [src L31] C-07 dispatch | The core launches nothing; Agent class word shipped; raw-id `cla -> REPRESENTED (report L3595)
19. [src L32] C-08 run record | Per-run `events.jsonl`, transcript adapter gated by M1, manife -> REPRESENTED (report L3596)
20. [src L33] C-04 reflect engine | No engine moves now; engine A stays production Tier 2; cod -> REPRESENTED (report L3597)
21. [src L34] C-05 consumer entry | Reflect UC-1 stays the only tasklist and workflow entry; a -> REPRESENTED (report L3598)
22. [src L35] X-15 (C-15) tasklist Medium | Label map as module data; fidelity prompt outside  -> REPRESENTED (report L3599)
23. [src L36] C-10 PR wire format | Separate pre-step, pure converter on the `pr_submit` side, -> REPRESENTED (report L3600)
24. [src L37] C-11 rf-qa first step | Lens-level first change: one new read-only lens agent an -> REPRESENTED (report L3601)
25. [src L38] C-12 collaboration | H1, H2, H3, H4 principle and the static kit (`kit: off`) no -> REPRESENTED (report L3602)
26. [src L39] X-13 (C-13) process redesign | Optional card format, row block, advisory rowchec -> REPRESENTED (report L3603)
27. [src L40] X-14 (C-14) evaluation | Three-tier acceptance, metric of record, tested script  -> REPRESENTED (report L3604)
28. [src L42] Where two outcomes pull against each other, the combination the results themselv -> REPRESENTED (report L3606)
29. [src L46] CT-1 | C-01 (thin contract, "no change to `cli/reflect`") against C-12 (H1 needs -> REPRESENTED (report L3610)
30. [src L47] CT-2 | C-01 (a repair step inside both parsers, all pins unmodified) against C-0 -> REPRESENTED (report L3611)
31. [src L48] CT-3 | C-02 (need = `min(Q, requested)`), C-03 (floor `min(2, requested)`), C-06 -> REPRESENTED (report L3612)
32. [src L49] CT-4 | X-14 (identity check reports `unrecorded` until a writer exists) against  -> REPRESENTED (report L3613)
33. [src L50] CT-5 | X-15 (H+ keeps MAJOR non-blocking rows droppable) against C-02 (CRITICAL  -> REPRESENTED (report L3614)
34. [src L51] CT-6 | C-07 (class-word dispatch only ships) against C-09 (distinct gateway pane -> REPRESENTED (report L3615)
35. [src L53] The design stays ONE coherent design under these tensions because each is a ques -> REPRESENTED (report L3617)
36. [src L55] Verified facts that bound the design to ONE shape. They rule out the E3i scripts -> REPRESENTED (report L3619)
37. [src L59] F-1 | The `cli/review` kernel is the one engine E1 and E3s already share; E1 is  -> REPRESENTED (report L3623)
38. [src L60] F-2 | The package exists (25 tracked files, optional-module registration through -> REPRESENTED (report L3624)
39. [src L61] F-3 | E2 changed no file under `src/` or `tests/` on its whole branch; it contri -> REPRESENTED (report L3625)
40. [src L62] F-4 | E3i (`review_ledger.py`, `stoprule.py`, `diffgate.py`, `fix_audit.py`, 7,5 -> REPRESENTED (report L3626)
41. [src L63] F-5 | In production `superclaude reflect run` uses the swarm ensemble (engine A) -> REPRESENTED (report L3627)
42. [src L64] F-6 | The defects that decide verdicts (clearing by silence, one valid reviewer  -> REPRESENTED (report L3628)
43. [src L66] ### Rationale: the 11 decision axes -> REPRESENTED (report L3630)
44. [src L68] For each axis: the options found in the evidence, what is chosen, why, and the t -> REPRESENTED (report L3632)
45. [src L72] 1 | Core shape | The four candidates of synth-05 6.1 and `research-notes.md` "De -> REPRESENTED (report L3636)
46. [src L73] 2 | Finding contract | The contracts at HEAD, E2 and E3 (synth-05 6.2): findings -> REPRESENTED (report L3637)
47. [src L74] 3 | Limits policy | drop the whole line (today: v1 ledger keeps the reviewer's o -> REPRESENTED (report L3638)
48. [src L75] 4 | Quorum and verdict | CLI ledger today (typed `blocking` decides; one valid b -> REPRESENTED (report L3639)
49. [src L76] 5 | Dispatch | class word on the Agent `model` argument (E1 prompt path); raw mo -> REPRESENTED (report L3640)
50. [src L77] 6 | Collaboration | F1 axis-flip (between-phase resume), F3 move radar, F4 sweep -> REPRESENTED (report L3641)
51. [src L78] 7 | Process redesign | Sweep Sheet (script-built items), Recipe Ledger (written  -> REPRESENTED (report L3642)
52. [src L79] 8 | Reflect engine | engine A (swarm ensemble) as the base; engine B (skill pane -> REPRESENTED (report L3643)
53. [src L80] 9 | Evaluation | E1 structural exit script; E2 ground truth plus blind judge; E1 -> REPRESENTED (report L3644)
54. [src L81] 10 | Variants (E3i) | adopt the scripts; port the contracts; drop | Port contrac -> REPRESENTED (report L3645)
55. [src L82] 11 | Future modules | PR code review as a third reviewer inside pr-submit, or an -> REPRESENTED (report L3646)
56. [src L84] ### Choices the evidence cannot decide (adjudication-dependent) -> REPRESENTED (report L3648)
57. [src L86] Each of the 18 rows (labels A-3 to A-20) was a choice the evidence could not dec -> REPRESENTED (report L3650)
58. [src L90] A-3 | Quorum value | The code gives no rule: `ledger.py` never reads `reviewers_ -> REPRESENTED (report L3654)
59. [src L91] A-4 | Who owns `blocking` | Reviewer-typed boolean (CLI today, r03 §1.2); scrip -> REPRESENTED (report L3655)
60. [src L92] A-5 | Limits policy | Truncation ceiling is verified arithmetic; re-ask recovery -> REPRESENTED (report L3656)
61. [src L93] A-6 | Strict distinctness default | Soft distinctness silently re-admits duplica -> REPRESENTED (report L3657)
62. [src L94] A-7 | Gateway dispatch lane | The raw-id `claude -p` lane reaches every gateway  -> REPRESENTED (report L3658)
63. [src L95] A-8 | Reflect engine composition | Evidence-supported composition in r06 §8 d i -> REPRESENTED (report L3659)
64. [src L96] A-9 | Ledger status machine | CLI `review-ledger/1`: open / resolved_check / res -> REPRESENTED (report L3660)
65. [src L97] A-10 | Run record | Append-only per-run events plus manifest state machine plus  -> REPRESENTED (report L3661)
66. [src L98] A-11 | `verify-run` owner | Kernel CLI for run-time invariants (any consumer inh -> REPRESENTED (report L3662)
67. [src L99] A-12 | Tasklist `Medium` | Tasklist skill: Medium is blocking (`SKILL.md:1537,15 -> REPRESENTED (report L3663)
68. [src L100] A-13 | Tasklist review entry point | Keep reflect UC-1 (`/sc:reflect --mode pre` -> REPRESENTED (report L3664)
69. [src L101] A-14 | PR finding wire format | One v2 wire format with module-declared vocabula -> REPRESENTED (report L3665)
70. [src L102] A-15 | Core shape (axis 1) | Options A to D of synth-05 6.1 and 7 axis 1: (A) v2 -> REPRESENTED (report L3666)
71. [src L103] A-16 | Unknown-key policy and `prior` lines (axis 2) | Open (v1, v2 accept unkno -> REPRESENTED (report L3667)
72. [src L104] A-17 | rf-qa first step and read-only scope (axis 11, 7.2.2) | Start at the `/ta -> REPRESENTED (report L3668)
73. [src L105] A-18 | Collaboration exchange capability (axis 6) | H1 and H2 plus a per-module  -> REPRESENTED (report L3669)
74. [src L106] A-19 | Process-redesign modules (axis 7) | Sweep-Sheet-shaped (scripts build typ -> REPRESENTED (report L3670)
75. [src L107] A-20 | Evaluation metric of record (axis 9) | Ground-truth items found at any se -> REPRESENTED (report L3671)
76. [src L109] Decided by evidence, so not pending (formerly the labels A-1 and A-2): the conve -> REPRESENTED (report L3673)
77. [src L111] ### 7.1 Target Architecture -> REPRESENTED (report L3675)
78. [src L113] Shared core and thin modules. The core is one package reached through one CLI. I -> REPRESENTED (report L3677)
79. [src L115] ``` -> REPRESENTED (report L156)
80. [src L116]  CONSUMERS (installed prose: skills / commands; they reach the core only through -> REPRESENTED (report L3680)
81. [src L118]   /sc:reflect --mode pre|post   /sc:workflow Wave 4   /sc:tasklist Stage 10.5    -> REPRESENTED (report L3682)
82. [src L119]   Tier 2 engine: legacy |       (advisory, one         (per phase, parallel,     -> REPRESENTED (report L3683)
83. [src L120]   shadow | panel                reflect call)          advisory + HALT item)     -> REPRESENTED (report L3684)
84. [src L121]                                                                                  -> REPRESENTED (report L3685)
85. [src L122]         |                            |                        |                  -> REPRESENTED (report L3686)
86. [src L123]   +-----+--------+       +-----------+------------------------+--+         +---- -> REPRESENTED (report L3687)
87. [src L124]   | REFLECT      |       | TASKLIST / WORKFLOW MODULE            |         | SPE -> REPRESENTED (report L3688)
88. [src L125]   | MODULE       |       | enters through reflect UC-1 Tier 2    |         | anc -> REPRESENTED (report L3689)
89. [src L126]   | templates,   |       | profile: T<PP>.<TT> refs, 5 Stage-7   |         | cat -> REPRESENTED (report L3690)
90. [src L127]   | lenses,      |       | dimensions, label map                 |         | CAN -> REPRESENTED (report L3691)
91. [src L128]   | deviation    |       |                                       |         | BAS -> REPRESENTED (report L3692)
92. [src L129]   | classes      |       |                                       |         | PRI -> REPRESENTED (report L3693)
93. [src L130]   +-----+--------+       +-----------+---------------------------+         +---- -> REPRESENTED (report L3694)
94. [src L131]         |                            |                                           -> REPRESENTED (report L3695)
95. [src L132]         +----------------------------+------------------------+----------------- -> REPRESENTED (report L3696)
96. [src L133]                                                               | -> REPRESENTED (report L3697)
97. [src L134]                                             MODULE PROFILE INTERFACE  (data + ho -> REPRESENTED (report L3698)
98. [src L135]                                             lens / role table, cap, brief blocks -> REPRESENTED (report L3699)
99. [src L136]  =============================================================================== -> REPRESENTED (report L3700)
100. [src L137]   REVIEW PANEL CORE      src/superclaude/cli/review/      CLI: superclaude revie -> REPRESENTED (report L3701)
101. [src L138]   (one package)                                           verify-citations | rec -> REPRESENTED (report L3702)
102. [src L139]   SHARED THIN CONTRACT (both engines import it; debates C-01, C-06, C-09, C-08,  -> REPRESENTED (report L3703)
103. [src L140]   [1 ids, limits constants,  [2 panel, tier and      [3 run record: events.jsonl -> REPRESENTED (report L3704)
104. [src L141]      one repair step (cut of   resolution: one          manifest lock, cross-run -> REPRESENTED (report L3705)
105. [src L142]      location fields, drop     reviewed tier file,      export with strict mode, -> REPRESENTED (report L3706)
106. [src L143]      record), one refs list,   soft distinctness,       transcript adapter behin -> REPRESENTED (report L3707)
107. [src L144]      hash and identity]        requested_slots]         measurement M1] -> REPRESENTED (report L3708)
108. [src L145]  ------------------------------------------------------------------------------- -> REPRESENTED (report L3709)
109. [src L146]   ENGINE v1  (spec-review module)                    ENGINE v2 KERNEL  (reflect  -> REPRESENTED (report L3710)
110. [src L147]   findings.py (text anchor)  ledger.py               findings_v2.py (citations w -> REPRESENTED (report L3711)
111. [src L148]   review-ledger/1; v1 clustering                     chain flag, support weights -> REPRESENTED (report L3712)
112. [src L149]   merge: any-blocking union, quorum refusal (exit 12) card_convert.py; the verdi -> REPRESENTED (report L3713)
113. [src L150]   clearing: quorum-gated explicit `prior`, CRITICAL   in cli/reflect (not in the -> REPRESENTED (report L3714)
114. [src L151]   floor, defer terminal; verdict derived on read      output to pr_submit.Findin -> REPRESENTED (report L3715)
115. [src L152]  =============================================================================== -> REPRESENTED (report L3700)
116. [src L153]           |                                   |                                  -> REPRESENTED (report L3717)
117. [src L154]   DISPATCH CONTRACT (the core launches         EXECUTION SHELL (reflect)         -> REPRESENTED (report L3718)
118. [src L155]   nothing)                                     src/superclaude/cli/reflect/      -> REPRESENTED (report L3719)
119. [src L156]   Agent class word = the `launch` word         engine A ensemble stays productio -> REPRESENTED (report L3720)
120. [src L157]   (Claude classes, ships now)                  Tier 2 (C-04); runner,            -> REPRESENTED (report L3721)
121. [src L158]   claude -p raw model id: GATED (G1-G3),       contract.derive_verdict, write-ba -> REPRESENTED (report L3722)
122. [src L159]   not built; swarm HTTP stays in engine A      isolation, fallback ladder; exit  -> REPRESENTED (report L3723)
123. [src L160]   + served-model record from the transcript    0 / 10 / 11 / 2; code-owned write -> REPRESENTED (report L3724)
124. [src L161]     (message.model), gated by M1               helpers write comparison siblings -> REPRESENTED (report L3725)
125. [src L162] ``` -> REPRESENTED (report L156)
126. [src L164] Modules at a glance (what each supplies, what it must keep): -> REPRESENTED (report L3728)
127. [src L168] Reflect (Tier 2 shadow, then panel) | `/sc:reflect --mode pre\|post`; `--t2-engi -> REPRESENTED (report L3732)
128. [src L169] Tasklist and workflow review | `/sc:workflow` Wave 4 (`src/superclaude/skills/sc -> REPRESENTED (report L3733)
129. [src L170] Spec review (spec-panel loop, `sc:brainstorm`, `sc:design`) | `/sc:spec-panel -- -> REPRESENTED (report L3734)
130. [src L171] PR code review (later) | `src/superclaude/pr_submit/` (12 modules, 6,511 lines)  -> REPRESENTED (report L3735)
131. [src L172] rf-qa / rf-qa-qualitative replacement (later) | `/task` phase-gate QA (`src/supe -> REPRESENTED (report L3736)
132. [src L174] Core contract elements (where each comes from, what the core provides, what a mo -> REPRESENTED (report L3738)
133. [src L178] 1 | Finding record and identity | E3: `src/superclaude/cli/review/findings.py` ( -> REPRESENTED (report L3742)
134. [src L179] 2 | Merge and cluster | E3: `ledger.py` `merge_round`, `findings.py` `cluster` ( -> REPRESENTED (report L3743)
135. [src L180] 3 | Citation verification | E1: `src/superclaude/cli/review/verify_cmd.py` (`rev -> REPRESENTED (report L3744)
136. [src L181] 4 | Verdict | E3: `ledger.py` `_decision`, `_brief_ids`, `verdict()`. E1 and ref -> REPRESENTED (report L3745)
137. [src L182] 5 | Ledger and rounds | E3: `ledger.py`, `ledger_cmd.py` (`review-ledger/1`). E3 -> REPRESENTED (report L3746)
138. [src L183] 6 | Panel, tier, dispatch | E1 and E3: `src/superclaude/cli/review/panel.py`, `d -> REPRESENTED (report L3747)
139. [src L184] 7 | Brief hooks | E3: `src/superclaude/rules/prompts/document_review_loop_prompt -> REPRESENTED (report L3748)
140. [src L185] 8 | Run record and telemetry | E3: `src/superclaude/cli/review/telemetry.py` (`r -> REPRESENTED (report L3749)
141. [src L186] 9 | Evaluation hooks | E1: `scripts/reflect_shadow_exit.py`, `src/superclaude/cl -> REPRESENTED (report L3750)
142. [src L188] Invariants the core must keep: -> REPRESENTED (report L3752)
143. [src L192] I-1 | Contract 1.8.0 byte-identical for reflect: the `### 9.1` block of `src/sup -> REPRESENTED (report L3756)
144. [src L193] I-2 | The 36-test verdict matrix: `contract.derive_verdict` signature, order blo -> REPRESENTED (report L3757)
145. [src L194] I-3 | findings-v1 lines stay parseable; `fixmap-v1` stays | `src/superclaude/cli -> REPRESENTED (report L3758)
146. [src L195] I-4 | Review-rule text: S1-S5 copied verbatim into ten primitives; cap text "at  -> REPRESENTED (report L3759)
147. [src L196] I-5 | Repository rules: `src/superclaude/` is the source of truth and `.claude/{ -> REPRESENTED (report L3760)
148. [src L197] I-6 | Layout traps the core must respect: a skill directory needs a `SKILL.md` ( -> REPRESENTED (report L3761)
149. [src L198] I-7 | Purity: no `gh` call, no network, no push, comment or resolve action, no r -> REPRESENTED (report L3762)
150. [src L199] I-8 | Package independence: `cli/review` and `cli/reflect` import each other now -> REPRESENTED (report L3763)
151. [src L200] I-9 | The plugin tree `plugins/superclaude/` is hand-kept and partial (4 skills; -> REPRESENTED (report L3764)
152. [src L202] Which defects the core fixes and which the modules own (register of r17: 171 row -> REPRESENTED (report L3766)
153. [src L206] Verdict, clearing, partial panel, deferral, stale verdict | 002, 003, 008, 009,  -> REPRESENTED (report L3770)
154. [src L207] Silent drop, anchor and cluster family | 001, 004, 005, 006, 056-058, 060, 061,  -> REPRESENTED (report L3771)
155. [src L208] Task-id reference gap (`T01.01`, `T01.02`) | 007 | MODULE-tasklist | REPRODUCED  -> REPRESENTED (report L3772)
156. [src L209] Panel resolution | 014-018, 020, 071, 109, 111, 115, 125 | CORE | 014, 015, 016, -> REPRESENTED (report L3773)
157. [src L210] Brief and parser contract | 023, 024, 025, 027, 029 | CORE | TRACED; 025 REPRODU -> REPRESENTED (report L3774)
158. [src L211] Report ending conflict (`verdict:` line vs findings block last) | 026 | MODULE-s -> REPRESENTED (report L3775)
159. [src L212] Persistence and CLI | 011, 012, 013, 043, 053-055, 059, 079, 126 | CORE | 011 RE -> REPRESENTED (report L3776)
160. [src L213] Telemetry | 021, 022, 110, 116, 117, 127 | CORE | 117 REPRODUCED in r15 §2 (400 -> REPRESENTED (report L3777)
161. [src L214] E1 kernel additions | 118-121, 124, 146, 159, 162, 168, 171 | CORE | 120 REPRODU -> REPRESENTED (report L3778)
162. [src L215] Reflect engine A and shadow protocol | 062, 063, 122, 128-132, 135-145, 147, 149 -> REPRESENTED (report L3779)
163. [src L216] Policy conflicts that touch both engines | 133 (threshold), 134 (single vendor)  -> REPRESENTED (report L3780)
164. [src L217] Study harness, evaluation, ops, dropped | HARNESS 14, EVAL 36, OPS 2, DROP 11 |  -> REPRESENTED (report L3781)
165. [src L219] Key tests that change a contract when a defect is fixed (all read in r03, r17):  -> REPRESENTED (report L3783)
166. [src L221] ### 7.2 Future-Use Exposure Check -> REPRESENTED (report L3785)
167. [src L223] Test applied to every candidate (derived in r13 §9 from the verified code): (1) -> REPRESENTED (report L3787)
168. [src L225] #### 7.2.1 PR code review -> REPRESENTED (report L3789)
169. [src L229] `pr_submit` needs one integer `line` per finding and deletes any finding without -> REPRESENTED (report L3793)
170. [src L230] Closed category and lens sets: v2 accepts six spec categories and three lenses,  -> REPRESENTED (report L3794)
171. [src L231] Severity: five tiers with category floors and ceilings and a count-based recomme -> REPRESENTED (report L3795)
172. [src L232] Round counting: pr-submit counts remediation rounds (default 2, hard cap 5) and  -> REPRESENTED (report L3796)
173. [src L233] Reviewer plumbing: `REVIEWERS = ("augment", "codex")`, bot identities, completio -> REPRESENTED (report L3797)
174. [src L234] Fork-only rule and outward actions (comment, push, resolve) | A core with no out -> REPRESENTED (report L3798)
175. [src L235] pr-submit runs in the main orchestrating session, not inside a subagent that spa -> REPRESENTED (report L3799)
176. [src L236] Two evidence gates for one job: the `evidence-validator` agent (Wave 3) and `ver -> REPRESENTED (report L3800)
177. [src L237] The ledger holds one document (`doc` path, line-range spans); a PR diff or taskl -> REPRESENTED (report L3801)
178. [src L238] Reviewer agents: `auggie-reviewer` has Bash, no plan mode and a pinned `model: o -> REPRESENTED (report L3802)
179. [src L239] `--revagent` accepts only the four native aliases | The panel path is separate f -> REPRESENTED (report L3803)
180. [src L240] Test surface and distribution: 50 test files under `tests/pr_submit/`; `plugins/ -> REPRESENTED (report L3804)
181. [src L241] No ground truth for PR review in any effort | Tier G seeded defects with clean t -> REPRESENTED (report L3805)
182. [src L243] **Verdict, PR code review: the final shape does NOT block it (NO).** Condition:  -> REPRESENTED (report L3807)
183. [src L245] #### 7.2.2 rf-qa / rf-qa-qualitative replacement -> REPRESENTED (report L3809)
184. [src L249] rf-qa reviews and edits (`fix_authorization`); the `/task` lens agents are told  -> REPRESENTED (report L3813)
185. [src L250] Checklist plus a computed confidence gate: `VERIFIED / (TOTAL - UNVERIFIABLE) *  -> REPRESENTED (report L3814)
186. [src L251] Lens pack and agent-count floors: 8 standard lenses, minimum 6 / 8 / 10 / 12 age -> REPRESENTED (report L3815)
187. [src L252] "Reviewer failed" finding defined in five files (rf-analyst, rf-qa-qualitative,  -> REPRESENTED (report L3816)
188. [src L253] Regression and monotonicity halts with byte-exact strings (`[HALT-MONOTONICITY]  -> REPRESENTED (report L3817)
189. [src L254] No behavioural oracle: the tests are static text pins and test-side re-implement -> REPRESENTED (report L3818)
190. [src L255] Coupling: the spec-panel loop reuses rf-qa Fix Cycle steps 1-5; the claim that t -> REPRESENTED (report L3819)
191. [src L256] Eight document types in rf-qa-qualitative, five gate phases in rf-qa, five analy -> REPRESENTED (report L3820)
192. [src L257] Distribution: rf-* agents are absent from `plugins/superclaude/` | Shipping form -> REPRESENTED (report L3821)
193. [src L259] **Verdict, rf-qa / rf-qa-qualitative replacement: the final shape does NOT block -> REPRESENTED (report L3823)
194. [src L261] #### 7.2.3 Later reviewers -> REPRESENTED (report L3825)
195. [src L265] `auggie-reviewer` (agent) | Bash tool, no plan mode, pinned opus; JSON finding f -> REPRESENTED (report L3829)
196. [src L266] `reflect-reviewer` (agent) | Output is a deviation table, not a findings block;  -> REPRESENTED (report L3830)
197. [src L267] `evidence-validator` (agent) | Used as a gate by pr-submit and reflect; not a re -> REPRESENTED (report L3831)
198. [src L268] Swarm lens registry (`src/superclaude/cli/swarm/lenses/`, 9 entries, 8 populated -> REPRESENTED (report L3832)
199. [src L269] Tasklist Stage 7 and patch loop | 2N homogeneous agents split by task range; own -> REPRESENTED (report L3833)
200. [src L270] `sc:brainstorm`, `sc:design` | No review step; brainstorm's convergence score (0 -> REPRESENTED (report L3834)
201. [src L271] `superclaude tasklist validate` | Own HIGH / MEDIUM / LOW vocabulary and a one-r -> REPRESENTED (report L3835)
202. [src L272] `sc-bare-review` | The claim that five commands call it is [CODE-CONTRADICTED] ( -> REPRESENTED (report L3836)
203. [src L273] E3i spec-panel variants | Installed-only, built on the 472-line PR 427 text; no  -> REPRESENTED (report L3837)
204. [src L274] `sc-validate-roadmap-protocol`, `sc-review-translation-protocol`, `sc-validate-t -> REPRESENTED (report L3838)
205. [src L276] **Verdict, later reviewers: the final shape does NOT block them (NO).** Every ve -> REPRESENTED (report L3840)
206. [src L278] #### 7.2.4 Verdicts -> REPRESENTED (report L3842)
207. [src L282] PR code review | NO | The v2 engine's citations, module-declared category / lens -> REPRESENTED (report L3846)
208. [src L283] rf-qa / rf-qa-qualitative replacement | NO | Mechanically read-only reviewer con -> REPRESENTED (report L3847)
209. [src L284] Later reviewers | NO | Profile interface and the six-condition contract test; fi -> REPRESENTED (report L3848)
210. [src L286] ### Adjudication register (slugs and adjudicated outcomes; the full results sit  -> REPRESENTED (report L3850)
211. [src L288] Each slug below is the slug of the synth-06 6.12.9 slot named in the third colum -> REPRESENTED (report L3852)
212. [src L292] A-3 | `merge-verdict-policy-and-quorum` | C-03 | any-blocking union; quorum floo -> REPRESENTED (report L3856)
213. [src L293] A-4 | `ledger-clearing-and-verdict-authority` | C-02 | typed `blocking` plus CRI -> REPRESENTED (report L3857)
214. [src L294] A-5 | `limits-repair-policy` | C-06 | cut of the three location fields to 200 be -> REPRESENTED (report L3858)
215. [src L295] A-6 | `panel-resolution-and-tier-source` | C-09 | soft distinctness stays the de -> REPRESENTED (report L3859)
216. [src L296] A-7 | `dispatch-and-launch-mechanism` | C-07 | Agent class-word lane ships, the  -> REPRESENTED (report L3860)
217. [src L297] A-8 | `reflect-tier2-engine-composition` | C-04 | no engine moves now; code-owne -> REPRESENTED (report L3861)
218. [src L298] A-9 | `ledger-clearing-and-verdict-authority` | C-02 | keep `review-ledger/1`; q -> REPRESENTED (report L3862)
219. [src L299] A-10 | `run-record-and-served-model-capture` | C-08 | per-run events, manifest l -> REPRESENTED (report L3863)
220. [src L300] A-11 | `eval-acceptance-and-harness-owner` | C-14 (X-14) | verifier, judge and r -> REPRESENTED (report L3864)
221. [src L301] A-12 | `tasklist-medium-and-fidelity-vocab` | C-15 (X-15) | label map as module  -> REPRESENTED (report L3865)
222. [src L302] A-13 | `consumer-entry-effect-and-delivery` | C-05 | reflect UC-1 stays the entr -> REPRESENTED (report L3866)
223. [src L303] A-14 | `pr-review-wire-format-and-slot` | C-10 | pure converter to `pr_submit.Fi -> REPRESENTED (report L3867)
224. [src L304] A-15 | `core-shape-and-finding-contract` | C-01 | thin shared contract, per-modu -> REPRESENTED (report L3868)
225. [src L305] A-16 | `core-shape-and-finding-contract` | C-01 | open unknown keys in both pars -> REPRESENTED (report L3869)
226. [src L306] A-17 | `rfqa-first-step-and-readonly-scope` | C-11 | lens-level first change: ne -> REPRESENTED (report L3870)
227. [src L307] A-18 | `collaboration-exchange-capability` | C-12 | H1-H4 and static kit now (`k -> REPRESENTED (report L3871)
228. [src L308] A-19 | `process-redesign-modules` | C-13 (X-13) | optional cards, row block and  -> REPRESENTED (report L3872)
229. [src L309] A-20 | `eval-acceptance-and-harness-owner` | C-14 (X-14) | metric of record per  -> REPRESENTED (report L3873)
230. [src L311] Slot coverage: C-01 (A-15, A-16), C-02 (A-4, A-9), C-03 (A-3), C-04 (A-8), C-05  -> REPRESENTED (report L3875)
231. [src L313] ### Contradictions between research files (stronger side named) -> REPRESENTED (report L3877)
232. [src L317] C-1 | Status of D-17 (cost fan-out) and D-23 (manifest lost update) | r17 lists  -> REPRESENTED (report L3881)
233. [src L318] C-2 | Is the finding location type a core blocker | r13 original text: not a blo -> REPRESENTED (report L3882)
234. [src L319] C-3 | Core purity | r13 M10: no `git` in the core | r04 §3.1: the only subproce -> REPRESENTED (report L3883)
235. [src L320] C-4 | Is batch j1 an unexamined hole | r16 §2.3 original: j1 is in none of the  -> REPRESENTED (report L3884)
236. [src L321] C-5 | Spec-panel dependency on rf-qa Fix Cycle | scope slice: hard coupling | r1 -> REPRESENTED (report L3885)
237. [src L322] C-6 | Cross-reviewer overlap in E1 | scope slice 11 as carried in the hand-offs: -> REPRESENTED (report L3886)
238. [src L323] C-7 | `identity_source` in recorded contracts | scope slice 11: all `requested-p -> REPRESENTED (report L3887)
239. [src L324] C-8 | Cause of the 3 "no contract" EV-1 failures | scope slice 11: no `return-co -> REPRESENTED (report L3888)
240. [src L325] C-9 | "Reflect has no panel / tier code" (E2 hand-off) | E2 section 5.6 | r01 § -> REPRESENTED (report L3889)
241. [src L326] C-10 | `cli/review` change attributed to "#519 + #518" | E2 hand-offs | r01 §1. -> REPRESENTED (report L3890)
242. [src L327] C-11 | Meanings of `Medium` | scope slice 12: four | r12 §3: at least six | r12 -> REPRESENTED (report L3891)
243. [src L328] C-12 | rf-* spawn lines | scope slice 12: 185 over 7 skills | r13 §4.2: 175 per -> REPRESENTED (report L3892)
244. [src L329] C-13 | Plugin `spec-panel.md` | scope slice 12: hard gate "softened", 25-line di -> REPRESENTED (report L3893)
245. [src L330] C-14 | Merge-drop wording and counts (`COMBO-REPORT.md:292`) | "discarded with n -> REPRESENTED (report L3894)
246. [src L331] C-15 | `T2bModel01` | E2 run-2: not referenced in `src/` or `tests/` | r04 §6:  -> REPRESENTED (report L3895)
247. [src L332] C-16 | Duplicate-model rate for `@live7` | scope slices: 26/40 | r17 DR-014: 30/ -> REPRESENTED (report L3896)
248. [src L333] C-17 | Convergence threshold | `SKILL.md:703`: 0.75 PASS | `contract.py:310-326` -> REPRESENTED (report L3897)
249. [src L334] C-18 | Exchange "works in every runtime" | r09 original wording | r09 fix cycle  -> REPRESENTED (report L3898)
250. [src L335] C-19 | Does engine A compute diversity from SERVED or REQUESTED worker `model_id -> REPRESENTED (report L3899)
251. [src L337] ### Evidence excluded from the recommendation (with reason) -> REPRESENTED (report L3901)
252. [src L341] E2's recommended default panel "ember + 2x luna" and any model-combination ranki -> REPRESENTED (report L3905)
253. [src L342] E1 model-combination leads (orchestrator speed, calibrated confidence, complianc -> REPRESENTED (report L3906)
254. [src L343] The E2 "not a thinking-budget ceiling" conclusion | `theory.py` HARD set counts  -> REPRESENTED (report L3907)
255. [src L344] AI-labelled cluster precision 0.84 and recall 0.9545 | Labels are AI labels, "NO -> REPRESENTED (report L3908)
256. [src L345] `snap.py` and `rlog-r3.sh` writing into E1's evidence tree | Provenance of evide -> REPRESENTED (report L3909)
257. [src L346] Exchange arms F1-F7 as measured improvements | No arm has a measured effect on t -> REPRESENTED (report L3910)
258. [src L347] The six control files of the phase-5 report and every number that depends on the -> REPRESENTED (report L3911)
259. [src L349] ### Items marked [UNVERIFIED] in the research files that do not carry the recomm -> REPRESENTED (report L3913)
260. [src L351] 1. Quorum value: the code has no rule (`ledger.py` never reads the manifest); ch -> REPRESENTED (report L3915)
261. [src L352] 2. Re-ask recovery rate and whether a truncated anchor still `locate`s: E2 Spike -> REPRESENTED (report L3916)
262. [src L353] 3. Whether PostToolUse `additionalContext` reaches a subagent's own model (r09 G -> REPRESENTED (report L3917)
263. [src L354] 4. Availability of a transcript adapter for per-agent usage in every harness, an -> REPRESENTED (report L3918)
264. [src L355] 5. Whether the gateway serves `muse-ember-1.0` today and which Tier 4 slot it ho -> REPRESENTED (report L3919)
265. [src L356] 6. The pilot dispatch-collapse figure "6 of 9 tier3-orchestrated runs": the logs -> REPRESENTED (report L3920)
266. [src L357] 7. PR module `blocking` rule (no tier-to-verdict function exists); whether tests -> REPRESENTED (report L3921)
267. [src L358] 8. rf-qa confidence-gate details beyond `rf-qa.md:505`, the line numbers of rf-q -> REPRESENTED (report L3922)
268. [src L359] 9. 59 of the 171 defect rows of r17 are UNVERIFIED (E2 audit bodies, `COMBO-REPO -> REPRESENTED (report L3923)
269. [src L360] 10. Owner decisions: whether the wrapper switches to engine B or engine A gains  -> REPRESENTED (report L3924)
270. [src L361] 11. E3i grammar, status and exit-code details beyond constants and imports (scop -> REPRESENTED (report L3925)
271. [src L362] 12. Whether any E2 collaboration harness r1-r5 ran end to end; claimed test coun -> REPRESENTED (report L3926)
272. [src L363] 13. Whether naming `source.md` in the brief changes how often it is read (r05 Ga -> REPRESENTED (report L3927)
273. [src L364] 14. Judge model identity per E2 score and the 12-row blind re-judge (no artifact -> REPRESENTED (report L3928)
274. [src L365] 15. Whether the tasklist P2 loop needs a third full Stage 7 review after its sec -> REPRESENTED (report L3929)
275. [src L366] 16. Whether pre-commit hooks and the Orca hook are installed on a given machine; -> REPRESENTED (report L3930)
276. [src L367] 17. Cost of a local multi-model panel per PR round (r13 P15). -> REPRESENTED (report L3931)
277. [src L369] ### Coverage check: key findings of each research file -> REPRESENTED (report L3933)
278. [src L371] Each research file's Summary and Key Takeaways were read before finalizing. Ever -> REPRESENTED (report L3935)
279. [src L375] r01 overlap matrix | E2 changed no product code; #519 alone changed `cli/review` -> REPRESENTED (report L3939)
280. [src L376] r02 finding contract | Unknown keys accepted by v1 and v2 except v2 `calibrated_ -> REPRESENTED (report L3940)
281. [src L377] r03 merge, ledger, verdict | D-1, D-2, D-11, D-13 reproduced; tests pin them as  -> REPRESENTED (report L3941)
282. [src L378] r04 dispatch, identity, tiers | Reflect profile limits; four dispatch mechanisms -> REPRESENTED (report L3942)
283. [src L379] r05 input delivery and brief | Five brief families; the shared loop brief and E2 -> REPRESENTED (report L3943)
284. [src L380] r06 reflect two engines | `contract.py` single verdict map and 36 tests; engine  -> REPRESENTED (report L3944)
285. [src L381] r07 E1 evidence graded | Pipeline completes (15/15, 13/15); costs; served model  -> REPRESENTED (report L3945)
286. [src L382] r08 E2 evidence graded | Pilot cells reproduce; per-issue table; 3 easy defects  -> REPRESENTED (report L3946)
287. [src L383] r09 collaboration designs | Five designs, one hook skeleton written four times;  -> REPRESENTED (report L3947)
288. [src L384] r10 process redesign | Design-only; `review-ledger/1` stays and the row block is -> REPRESENTED (report L3948)
289. [src L385] r11 consumers: tasklist, workflow, reflect UC-1 | Wave 4 advisory and read-only; -> REPRESENTED (report L3949)
290. [src L386] r12 consumers: spec review | Loop bullets identical in plugin and pinned; binary -> REPRESENTED (report L3950)
291. [src L387] r13 future PR review and rf-qa | PR blockers P1-P15; rf-qa blockers R1-R12; swar -> REPRESENTED (report L3951)
292. [src L388] r14 E3 variants and experiments | FINAL-REPORT numbers recompute exactly; varian -> REPRESENTED (report L3952)
293. [src L389] r15 telemetry, manifest, run record | No shipped telemetry writer; D-17 and D-23 -> REPRESENTED (report L3953)
294. [src L390] r16 evaluation governance | Acceptance in tiers S, Q, G (derived); E1 and E2 are -> REPRESENTED (report L3954)
295. [src L391] r17 defect register | 171 rows, 170 distinct; owners CORE 75, MODULE-reflect 29, -> REPRESENTED (report L3955)
296. [src L392] r18 repo constraints and branching | `verify-sync` and `sync-dev` trap for a ski -> REPRESENTED (report L3956)
297. [src L394] Rules check: report only (no roadmap, branch plan, PR plan, risk register or eff -> REPRESENTED (report L3958)
298. [src L396] ### 7.3 Debate Invariants -> REPRESENTED (report L3960)
299. [src L398] Every invariant that a debate's invariant probe (Round 2.5) or return contract l -> REPRESENTED (report L3962)
300. [src L402] C-01 | `core-shape-and-finding-contract` | 1 / 14 / 1 | 9 of 25 findings | -> REPRESENTED (report L3966)
301. [src L403] C-02 | `ledger-clearing-and-verdict-authority` | 3 / 12 / 1 | 6 of 22 | -> REPRESENTED (report L3967)
302. [src L404] C-03 | `merge-verdict-policy-and-quorum` | 2 / 8 / 2 | 5 of 17 (INV-008, 011, 01 -> REPRESENTED (report L3968)
303. [src L405] C-04 | `reflect-tier2-engine-composition` | 0 / 15 / 2 | 3 of 20 (INV-004, 018,  -> REPRESENTED (report L3969)
304. [src L406] C-05 | `consumer-entry-effect-and-delivery` | 7 / 5 / 0 | 3 of 15 (INV-009, 012, -> REPRESENTED (report L3970)
305. [src L407] C-06 | `limits-repair-policy` | 4 / 12 / 4 | 6 of 26 | -> REPRESENTED (report L3971)
306. [src L408] C-07 | `dispatch-and-launch-mechanism` | 1 / 12 / 3 | 3 of 19 (INV-008, 013, 019 -> REPRESENTED (report L3972)
307. [src L409] C-08 | `run-record-and-served-model-capture` | 13 / 7 / 0 | 2 of 22 (INV-014, 01 -> REPRESENTED (report L3973)
308. [src L410] C-09 | `panel-resolution-and-tier-source` | 0 / 8 / 5 | 13 of 26 | -> REPRESENTED (report L3974)
309. [src L411] C-10 | `pr-review-wire-format-and-slot` | 5 / 9 / 0 | 6 of 20 (probe INV-004, 00 -> REPRESENTED (report L3975)
310. [src L412] C-11 | `rfqa-first-step-and-readonly-scope` | 6 / 9 / 1 | 2 of 18 (INV-005, 011) -> REPRESENTED (report L3976)
311. [src L413] C-12 | `collaboration-exchange-capability` | 2 / 12 / 0 | 2 of 16 (INV-001, 012) -> REPRESENTED (report L3977)
312. [src L414] X-13 (synth-06 C-13) | `process-redesign-modules` | 2 / 13 / 1 | 4 of 20 (INV-00 -> REPRESENTED (report L3978)
313. [src L415] X-14 (synth-06 C-14) | `eval-acceptance-and-harness-owner` | 12 / 13 / 0 | 4 of  -> REPRESENTED (report L3979)
314. [src L416] X-15 (synth-06 C-15) | `tasklist-medium-and-fidelity-vocab` | 2 / 12 / 3 | 3 of  -> REPRESENTED (report L3980)
315. [src L417] Total | 15 debates | 60 / 161 / 23 (244 rows) | | -> REPRESENTED (report L3981)
316. [src L419] Status key. OPEN = a HIGH or MEDIUM invariant that the recommended design does n -> REPRESENTED (report L3983)
317. [src L423] C-01 INV-001: anchor status can be surfaced for every blocking row from data `re -> REPRESENTED (report L3987)
318. [src L424] C-01 INV-002: adding `T<PP>.<TT>` to the shared token list leaves ledgers alread -> REPRESENTED (report L3988)
319. [src L425] C-01 INV-003: a repair step inside both `parse_block` functions can rescue over- -> REPRESENTED (report L3989)
320. [src L426] C-01 INV-004: the same repair gives the same benefit in the v2 parser (any error -> REPRESENTED (report L3990)
321. [src L427] C-01 INV-009: the 3-line clustering tolerance means the same thing in both engin -> REPRESENTED (report L3991)
322. [src L428] C-01 INV-010: the two parsers hold the only copies of the limits and one repair  -> REPRESENTED (report L3992)
323. [src L429] C-01 INV-014: a round whose only reviewer has only a repaired line merges like a -> REPRESENTED (report L3993)
324. [src L430] C-01 INV-015: a stuck row is one row, so surfacing its status once is enough (em -> REPRESENTED (report L3994)
325. [src L431] C-01 INV-016: the merged T2 gate catches every shared-contract change (a `refs_n -> REPRESENTED (report L3995)
326. [src L432] C-01 INV-017: adding the token once in `refs_norm` updates every reference-token -> REPRESENTED (report L3996)
327. [src L433] C-01 INV-018: shared helpers can move into a new module without touching pinned  -> REPRESENTED (report L3997)
328. [src L434] C-01 INV-020: "no change to `cli/reflect`" means the reflect results do not chan -> REPRESENTED (report L3998)
329. [src L435] C-01 INV-021: the merged T2 has committed v1 ledger fixtures to replay | MEDIUM  -> REPRESENTED (report L3999)
330. [src L436] C-01 INV-022: whatever repair policy C-06 picks leaves locating and clustering o -> REPRESENTED (report L4000)
331. [src L437] C-01 INV-024: the consensus alone resolves FX-1 and leaves C-06 free to choose t -> REPRESENTED (report L4001)
332. [src L438] C-01 INV-008: one constant per limit is safe when equal numbers mean different t -> REPRESENTED (report L4002)
333. [src L439] C-02 INV-001: `need = min(Q, requested)` can be 0 if `--resolution` carries an e -> REPRESENTED (report L4003)
334. [src L440] C-02 INV-002: a valid `prior open` plus a same-round non-blocking re-find leaves -> REPRESENTED (report L4004)
335. [src L441] C-02 INV-003: empty `brief_ids` with non-empty `verify_ids` stays REVISE (exit 1 -> REPRESENTED (report L4005)
336. [src L442] C-02 INV-004: `--resolution` absent: either fallback fails (one bypasses Q, one  -> REPRESENTED (report L4006)
337. [src L443] C-02 INV-005: `pending_new_sha256` can wedge the loop; no force path | MEDIUM |  -> REPRESENTED (report L4007)
338. [src L444] C-02 INV-006: the derived VM-6 pre-check must not fail on an empty ledger and mu -> REPRESENTED (report L4008)
339. [src L445] C-02 INV-007: `refound_deferred` is unreachable in the one-row D-11 shape (held- -> REPRESENTED (report L4009)
340. [src L446] C-02 INV-008: no undefer command; `--owner ""` satisfies "required" | MEDIUM | C -> REPRESENTED (report L4010)
341. [src L447] C-02 INV-009: an invalid-block reviewer's `prior open` is collected but ignored; -> REPRESENTED (report L4011)
342. [src L448] C-02 INV-010: dissent does not re-anchor the row; `apply_revision` still needs a -> REPRESENTED (report L4012)
343. [src L449] C-02 INV-011: prior ids are ledger ids `L<n>` while reviewers see `F<n>`; whethe -> REPRESENTED (report L4013)
344. [src L450] C-02 INV-013: an unexamined `prior resolved` clears; the quote is recorded, not  -> REPRESENTED (report L4014)
345. [src L451] C-02 INV-014: the text hash exists only if `revise` ran | MEDIUM | C-02 | synth- -> REPRESENTED (report L4015)
346. [src L452] C-02 INV-016: the CRITICAL floor keys on reviewer-typed severity; a re-classific -> REPRESENTED (report L4016)
347. [src L453] C-02 INV-018: older binaries read `last["verdict"]` and fail; stored per-round v -> REPRESENTED (report L4017)
348. [src L454] C-02 INV-020: a non-blocking `resolved_check` row is outside `verify_ids` and st -> REPRESENTED (report L4018)
349. [src L455] C-03 INV-006: the union merges every parsable finding including those of a revie -> REPRESENTED (report L4019)
350. [src L456] C-03 INV-007: `requested = max(len(resolution.reviewers), len(--report))` can co -> REPRESENTED (report L4020)
351. [src L457] C-03 INV-001: a refusal records nothing, so refusal rate, retries and reviews-to -> REPRESENTED (report L4021)
352. [src L458] C-03 INV-002: after exit 12, `ledger verdict` shows the previous round's stored  -> REPRESENTED (report L4022)
353. [src L459] C-03 INV-003: which layer owns the profile, `min_complete` and the `requested` d -> REPRESENTED (report L4023)
354. [src L460] C-03 INV-004: `--resolution` is not checked for kind or run (a first-kind resolu -> REPRESENTED (report L4024)
355. [src L461] C-03 INV-005: `complete` is not checked for distinct, current reviewers (unknown -> REPRESENTED (report L4025)
356. [src L462] C-03 INV-009: between the floor and `requested` the shortfall is silent; the mer -> REPRESENTED (report L4026)
357. [src L463] C-03 INV-010: the N=1..5 by five-state test matrix distinguishes only three inpu -> REPRESENTED (report L4027)
358. [src L464] C-03 INV-016: the union runs over rows that may already hold a `same_defect` mis -> REPRESENTED (report L4028)
359. [src L465] C-03 INV-012: `defer` is the only non-quorate route to a stored PASS and is reac -> REPRESENTED (report L4029)
360. [src L466] C-03 INV-013: `make verify-sync` does not cover the loop-prompt copies; installe -> REPRESENTED (report L4030)
361. [src L467] C-04 INV-001: a helper writes a comparison sibling, not the legacy file, in shad -> REPRESENTED (report L4031)
362. [src L468] C-04 INV-002: `calibrated` as a helper-owned stage: `SKILL.md:345` has the orche -> REPRESENTED (report L4032)
363. [src L469] C-04 INV-003: Arm A and M-B cannot each be read off the exit script as a clean 2 -> REPRESENTED (report L4033)
364. [src L470] C-04 INV-005: name-only validation over the stable and telemetry lists; `degrade -> REPRESENTED (report L4034)
365. [src L471] C-04 INV-006: "helper refuses", "helper advances its own stage" and shadow's "co -> REPRESENTED (report L4035)
366. [src L472] C-04 INV-007: M-A's "every recorded run yields a lint-clean contract" fails for  -> REPRESENTED (report L4036)
367. [src L473] C-04 INV-008: "exactly one verdict-read key outside the frozen lists": A counts  -> REPRESENTED (report L4037)
368. [src L474] C-04 INV-009: D1's CV-8 and CV-1 line lists may be incomplete (`executor-disjoin -> REPRESENTED (report L4038)
369. [src L475] C-04 INV-011: M-B cannot require zero parity failures over 20 runs (a 2-of-3 sho -> REPRESENTED (report L4039)
370. [src L476] C-04 INV-012: D1's fix at `reflect_shadow_exit.py:313` does not close all of CV- -> REPRESENTED (report L4040)
371. [src L477] C-04 INV-013: the presence rule and a refusing finalizer do not cover every run  -> REPRESENTED (report L4041)
372. [src L478] C-04 INV-014: the exit rule and `reflect_verdict_replay.py` read fixed paths and -> REPRESENTED (report L4042)
373. [src L479] C-04 INV-015: the card writer's target differs between the two advocates' texts; -> REPRESENTED (report L4043)
374. [src L480] C-04 INV-017: "helpers that advance their own stage make skipping detectable": t -> REPRESENTED (report L4044)
375. [src L481] C-04 INV-019: "comparison siblings let promotion be decided without risk": the a -> REPRESENTED (report L4045)
376. [src L482] C-04 INV-010: the reviewer-count value 1 and the I2 witness (`test_ensemble_stub -> REPRESENTED (report L4046)
377. [src L483] C-04 INV-016: widening the fence is not only bookkeeping: `SKILL.md:703` and `:1 -> REPRESENTED (report L4047)
378. [src L484] C-05 INV-001: "advisory at Wave 4 and Stage 10.5": Stage 10.5 halts on `needs_hu -> REPRESENTED (report L4048)
379. [src L485] C-05 INV-002: Stage 10.5 always passes `--remediate`, a write path that can nest -> REPRESENTED (report L4049)
380. [src L486] C-05 INV-003: the depth-policy remedy changes the remediation route and forces T -> REPRESENTED (report L4050)
381. [src L487] C-05 INV-005: the reach share has no working instrument (the only aggregator glo -> REPRESENTED (report L4051)
382. [src L488] C-05 INV-007: "only `status`, `coverage_pct`, `tier_reached`" is too narrow; two -> REPRESENTED (report L4052)
383. [src L489] C-05 INV-013: the replay that decides every disputed point has no ground-truth s -> REPRESENTED (report L4053)
384. [src L490] C-05 INV-014: the consensus does not show consumers receive the panel's benefit  -> REPRESENTED (report L4054)
385. [src L491] C-05 INV-004: a call-site depth flag is not "pin-safe": both workflow trees need -> REPRESENTED (report L4055)
386. [src L492] C-05 INV-006: the reach-share denominator is undefined (no-run populations, `--b -> REPRESENTED (report L4056)
387. [src L493] C-05 INV-008: a default flip reaches every UC-1 caller (task-builder PRE gate, a -> REPRESENTED (report L4057)
388. [src L494] C-05 INV-010: "one reflect-side switch" is prose in three places with no staged  -> REPRESENTED (report L4058)
389. [src L495] C-05 INV-011: a contract-compat test against the 36-test matrix does not cover t -> REPRESENTED (report L4059)
390. [src L496] C-06 INV-001: the dropped-blocking refusal sees only the current round's drops;  -> REPRESENTED (report L4060)
391. [src L497] C-06 INV-017: a 200-character prefix can locate at more than one place while the -> REPRESENTED (report L4061)
392. [src L498] C-06 INV-018: in reflect, `cluster_cmd` and `verify_cmd` run at step 6, after th -> REPRESENTED (report L4062)
393. [src L499] C-06 INV-023: cut plus itemise plus refusal does not alone close the PASS-by-los -> REPRESENTED (report L4063)
394. [src L500] C-06 INV-002: the manifest `completion` value is a third first-pass carrier the  -> REPRESENTED (report L4064)
395. [src L501] C-06 INV-003: a refused v1 merge records nothing, so the refusal-driven re-ask l -> REPRESENTED (report L4065)
396. [src L502] C-06 INV-005: `blocking_state` from the line's own `blocking` flag is untrusted  -> REPRESENTED (report L4066)
397. [src L503] C-06 INV-006: the acknowledgement is not bound to the dropped item ids or hashes -> REPRESENTED (report L4067)
398. [src L504] C-06 INV-007: a dropped `prior` line (a lost veto) has no stated `blocking_state -> REPRESENTED (report L4068)
399. [src L505] C-06 INV-008: both checkers return the first fault only; a line with two faults  -> REPRESENTED (report L4069)
400. [src L506] C-06 INV-010: a cut can invent a reference token (`FR-12` cut to `FR-1`) and cha -> REPRESENTED (report L4070)
401. [src L507] C-06 INV-016: a rescued line whose prefix does not locate becomes a kept row wit -> REPRESENTED (report L4071)
402. [src L508] C-06 INV-019: the unchanged Normalize text and the additive sentence use "invali -> REPRESENTED (report L4072)
403. [src L509] C-06 INV-024: the cut removes the v2 loss unit only for the length share | MEDIU -> REPRESENTED (report L4073)
404. [src L510] C-06 INV-025: a truncated block loses its tail with no line to itemise; truncati -> REPRESENTED (report L4074)
405. [src L511] C-06 INV-026: after the cut the refusal fires on 0 of 264, so K5 passes triviall -> REPRESENTED (report L4075)
406. [src L512] C-06 INV-004: additive keys carry no parser or policy version; `block_ok` change -> REPRESENTED (report L4076)
407. [src L513] C-06 INV-011: `original_chars`, `kept_chars` and `repaired_lines_rate` have no s -> REPRESENTED (report L4077)
408. [src L514] C-06 INV-020: two refusals can occur in sequence (quorum, then `dropped_blocking -> REPRESENTED (report L4078)
409. [src L515] C-06 INV-022: `card_convert.py` has its own claim cut; two implementations if a  -> REPRESENTED (report L4079)
410. [src L516] C-07 INV-017: the ship-now set does not close the A-r3 collapse: calibrator Agen -> REPRESENTED (report L4080)
411. [src L517] C-07 INV-001: a class-word binding written as data is not compared with the sess -> REPRESENTED (report L4081)
412. [src L518] C-07 INV-003: S5 is stated in two forms (`find_path` override against `--tiers`) -> REPRESENTED (report L4082)
413. [src L519] C-07 INV-005: S1 does not govern calibrator calls; a replay over every Agent row -> REPRESENTED (report L4083)
414. [src L520] C-07 INV-006: S4 passes if the model declines in prose; no effective-tool-list s -> REPRESENTED (report L4084)
415. [src L521] C-07 INV-007: G2 has no "reads its inputs and returns a valid findings block" cr -> REPRESENTED (report L4085)
416. [src L522] C-07 INV-009: three reviewers on three class words leave no class for a disjoint -> REPRESENTED (report L4086)
417. [src L523] C-07 INV-010: S6's "same panel for any run id" is false for the `x2` templates;  -> REPRESENTED (report L4087)
418. [src L524] C-07 INV-011: the transcript reader's key (reviewer id or attempt id) is not sta -> REPRESENTED (report L4088)
419. [src L525] C-07 INV-014: executor-class exclusion expands through model-id classes, not cla -> REPRESENTED (report L4089)
420. [src L526] C-07 INV-015: S1 and the shadow fence: applied to shadow dispatch it stops shado -> REPRESENTED (report L4090)
421. [src L527] C-07 INV-016: once `claude-p` is a permitted `launch` value the reflect check te -> REPRESENTED (report L4091)
422. [src L528] C-07 INV-018: the ship-now set does not change behaviour in a gateway workspace: -> REPRESENTED (report L4092)
423. [src L529] C-07 INV-002: a static fixture copy of the tier file tests its own aliases, not  -> REPRESENTED (report L4093)
424. [src L530] C-07 INV-004: S1's "`launch: null` is a dispatch error" contradicts D4's legacy- -> REPRESENTED (report L4094)
425. [src L531] C-07 INV-012: `resolve` prints a launch word for the primary pick only; a fallba -> REPRESENTED (report L4095)
426. [src L532] C-08 INV-001: a torn final line from a killed writer is not handled; one torn or -> REPRESENTED (report L4096)
427. [src L533] C-08 INV-002: `ingest` is called idempotent but a row for an unfinished sidechai -> REPRESENTED (report L4097)
428. [src L534] C-08 INV-005: the interactive layout stores sub-agent messages in separate `suba -> REPRESENTED (report L4098)
429. [src L535] C-08 INV-006: neither join works as written: the Agent-call `description` equall -> REPRESENTED (report L4099)
430. [src L536] C-08 INV-009: per-event usage summation over-counts 2.0x to 2.6x (one event per  -> REPRESENTED (report L4100)
431. [src L537] C-08 INV-010: M1(c) measured at 0 of 15 runs within 2 percent on the E1 logs; th -> REPRESENTED (report L4101)
432. [src L538] C-08 INV-011: a non-Anthropic sidechain reports `output_tokens` 0 and no cache k -> REPRESENTED (report L4102)
433. [src L539] C-08 INV-013: `record_absent` is printed by `export` only; a skipped `ingest` is -> REPRESENTED (report L4103)
434. [src L540] C-08 INV-016: the `refused` row composes with C-03's quorum refusal only if rais -> REPRESENTED (report L4104)
435. [src L541] C-08 INV-017: SKILL step 9 (identity) precedes step 10 (`ingest`); at step 9 no  -> REPRESENTED (report L4105)
436. [src L542] C-08 INV-020: the hybrid alone does not close the A3 identity gap: `model_reques -> REPRESENTED (report L4106)
437. [src L543] C-08 INV-021: the hybrid alone does not close C-03 INV-001: the refused row exis -> REPRESENTED (report L4107)
438. [src L544] C-08 INV-022: the hybrid alone does not close cost under-reporting: `cost_per_co -> REPRESENTED (report L4108)
439. [src L545] C-08 INV-003: the last `orchestrator_snapshot` by events-file order can be a sta -> REPRESENTED (report L4109)
440. [src L546] C-08 INV-004: one run is assumed to be one transcript file; resumes and restarts -> REPRESENTED (report L4110)
441. [src L547] C-08 INV-007: `init` has no manifest yet for the lock; one `lock_timeout` cascad -> REPRESENTED (report L4111)
442. [src L548] C-08 INV-008: what `export` does when `strict` refuses one record is unstated; t -> REPRESENTED (report L4112)
443. [src L549] C-08 INV-012: the events-side `attempt` and the manifest `attempt_id` are number -> REPRESENTED (report L4113)
444. [src L550] C-08 INV-015: a served id is not normalised (`qwen3.8-max` against `Qwen3.8-max` -> REPRESENTED (report L4114)
445. [src L551] C-08 INV-018: deterministic `record_id` makes `export` idempotent per id only; a -> REPRESENTED (report L4115)
446. [src L552] C-09 INV-001: the environment is detected once from the process env alone (`$T3M -> REPRESENTED (report L4116)
447. [src L553] C-09 INV-005: "the packaged file is the file `panel resolve` reads" fails when a -> REPRESENTED (report L4117)
448. [src L554] C-09 INV-009: "Coder slot first, then the repo edits" has no gate; merging the ` -> REPRESENTED (report L4118)
449. [src L555] C-09 INV-010: `requested_slots` follows `apply_to`, not the kind name; no test t -> REPRESENTED (report L4119)
450. [src L556] C-09 INV-012: the ascending-count sort key; the agreed tests cannot tell the two -> REPRESENTED (report L4120)
451. [src L557] C-09 INV-019: scarcest-first with two excluded classes on `live7` falls below th -> REPRESENTED (report L4121)
452. [src L558] C-09 INV-021: the spec loop does not hand the resolution to merge, so `requested -> REPRESENTED (report L4122)
453. [src L559] C-09 INV-026: "the loop gains distinct gateway panels" is true of requested ids  -> REPRESENTED (report L4123)
454. [src L560] C-09 INV-003: library and CLI orders differ without a trace in the artifact | LO -> REPRESENTED (report L4124)
455. [src L561] C-09 INV-004: statistics cover `fixed` and `random` slots only; a `round_robin`  -> REPRESENTED (report L4125)
456. [src L562] C-09 INV-011: a fixed anchor with count above 1 can resolve two reviewers to one -> REPRESENTED (report L4126)
457. [src L563] C-09 INV-017: the ember insertion index changes `fallback_depth` of Haiku | LOW  -> REPRESENTED (report L4127)
458. [src L564] C-09 INV-018: the ember edit list omits the `profiles` and `picker` entries that -> REPRESENTED (report L4128)
459. [src L565] C-10 INV-002: panel standing, reviewed SHA and dropped list have no durable home -> REPRESENTED (report L4129)
460. [src L566] C-10 INV-007: "requested" is defined as the dispatched count, so a slot that fai -> REPRESENTED (report L4130)
461. [src L567] C-10 INV-008: a reviewer with an empty findings block is invalid unless a non-em -> REPRESENTED (report L4131)
462. [src L568] C-10 INV-011: "present when every requested reviewer is complete" is vacuously t -> REPRESENTED (report L4132)
463. [src L569] C-10 INV-012: AM-1 splits by category only; a same-category cluster still pairs  -> REPRESENTED (report L4133)
464. [src L570] C-10 INV-001: the standing enum has no stale value; after a fix push the report  -> REPRESENTED (report L4134)
465. [src L571] C-10 INV-003: the checkout the reviewers see is not shown to equal the PR head t -> REPRESENTED (report L4135)
466. [src L572] C-10 INV-006: missing `changed_ranges` degrading to `in_diff` unset (True) is pe -> REPRESENTED (report L4136)
467. [src L573] C-10 INV-009: the unit of "dropped" differs from the unit of "cluster", so a CRI -> REPRESENTED (report L4137)
468. [src L574] C-10 INV-010: `blocking_clusters` counts the reviewer-typed boolean, so a run ca -> REPRESENTED (report L4138)
469. [src L575] C-10 INV-014: no rule excludes panel Findings from `dedup_groups` input, so a pa -> REPRESENTED (report L4139)
470. [src L576] C-10 INV-015: the "not clean" wording rule covers the run summary only, not the  -> REPRESENTED (report L4140)
471. [src L577] C-10 INV-018: the converter's inputs cannot be produced by existing machinery (` -> REPRESENTED (report L4141)
472. [src L578] C-10 INV-019: `finding_from_comment` needs a positive int `comment_id`; a key ma -> REPRESENTED (report L4142)
473. [src L579] C-11 INV-002: the lens-identity check is undefined when a report's first line na -> REPRESENTED (report L4143)
474. [src L580] C-11 INV-009: "the dispatched slot's path" is not unique for partition instances -> REPRESENTED (report L4144)
475. [src L581] C-11 INV-012: the hash and lens-line checks sit in step 10, after consolidation  -> REPRESENTED (report L4145)
476. [src L582] C-11 INV-015: the sha256 is taken over the executor's own write, proving later n -> REPRESENTED (report L4146)
477. [src L583] C-11 INV-016: arm 0 and arm 1a differ in more than the tool list (content lenses -> REPRESENTED (report L4147)
478. [src L584] C-11 INV-017: pre-computed counts exist in the oracle but no changed gate step a -> REPRESENTED (report L4148)
479. [src L585] C-11 INV-001: the oracle's parent permission mode, installed hook set and model  -> REPRESENTED (report L4149)
480. [src L586] C-11 INV-003: the tree-hash scope is unspecified: excluding `qa/` blinds it to N -> REPRESENTED (report L4150)
481. [src L587] C-11 INV-004: the subset guard checks the source file; runtime resolves project  -> REPRESENTED (report L4151)
482. [src L588] C-11 INV-007: "the standard eight lens dimensions" does not map one-to-one onto  -> REPRESENTED (report L4152)
483. [src L589] C-11 INV-008: the audit misses nested spawns and renamed tool names; its counts  -> REPRESENTED (report L4153)
484. [src L590] C-11 INV-010: the Confidence Gate formula is undefined at TOTAL = UNVERIFIABLE a -> REPRESENTED (report L4154)
485. [src L591] C-11 INV-013: `test_c_s1_s3_copied_verbatim` iterates a fixed 10-file tuple and  -> REPRESENTED (report L4155)
486. [src L592] C-11 INV-014: the `rf-qa.md` body and the installed SubagentStart hook tell agen -> REPRESENTED (report L4156)
487. [src L593] C-11 INV-018: the conditional switch does not name the other spawn sites in `tas -> REPRESENTED (report L4157)
488. [src L594] C-11 INV-006: the reflect-reviewer allowlist refused 7 calls across 517 runs, no -> REPRESENTED (report L4158)
489. [src L595] C-12 INV-005: H1 reaches reflect through the reflect brief with no call-site cha -> REPRESENTED (report L4159)
490. [src L596] C-12 INV-009: H2 (a repair, possibly a re-ask) is core now and compatible with C -> REPRESENTED (report L4160)
491. [src L597] C-12 INV-002: the served-model and act-rate probe record has a home | MEDIUM | C -> REPRESENTED (report L4161)
492. [src L598] C-12 INV-003: a reserved `exchange` key is "a pin, not an implementation" (`pane -> REPRESENTED (report L4162)
493. [src L599] C-12 INV-004: the off-state byte test coexists with H1 shipping unconditionally  -> REPRESENTED (report L4163)
494. [src L600] C-12 INV-006: a single kit cost figure can gate `kit: on` (elapsed against token -> REPRESENTED (report L4164)
495. [src L601] C-12 INV-007: a hold-out of at least 4 unseen defects is satisfiable on the 16-i -> REPRESENTED (report L4165)
496. [src L602] C-12 INV-008: a sidecar keyed by reviewer id and finding id is unambiguous acros -> REPRESENTED (report L4166)
497. [src L603] C-12 INV-010: one catalogue source per module, rendered from the installed form, -> REPRESENTED (report L4167)
498. [src L604] C-12 INV-011: "quorum counts over own-origin lines only" is a quantity C-02 and  -> REPRESENTED (report L4168)
499. [src L605] C-12 INV-013: the A-layer alone gives mutually blind reviewers (the reflect isol -> REPRESENTED (report L4169)
500. [src L606] C-12 INV-014: the enable trigger can be met on a lane that can host exchange (ta -> REPRESENTED (report L4170)
501. [src L607] C-12 INV-015: the A-layer alone is cost-safe (H2 re-ask spend is not priced or c -> REPRESENTED (report L4171)
502. [src L608] C-12 INV-016: the premise "no exchange arm has been measured against the static  -> REPRESENTED (report L4172)
503. [src L609] X-13 INV-001: `observed` is said to have one writer (the new entry point) but `S -> REPRESENTED (report L4173)
504. [src L610] X-13 INV-019: the built-now set alone cannot make process-catchable defects get  -> REPRESENTED (report L4174)
505. [src L611] X-13 INV-002: in reflect the file the entry point would parse is the orchestrato -> REPRESENTED (report L4175)
506. [src L612] X-13 INV-004: step 4 parses the card before the sidecar is written at step 6; a  -> REPRESENTED (report L4176)
507. [src L613] X-13 INV-005: the entry point writes fixed paths with no round or review-kind ar -> REPRESENTED (report L4177)
508. [src L614] X-13 INV-006: no row-id grammar or type rule; recorded ids include slugs, a `/`  -> REPRESENTED (report L4178)
509. [src L615] X-13 INV-007: the check rules need a path and a quote kind that no row field car -> REPRESENTED (report L4179)
510. [src L616] X-13 INV-009: `assigned`, `observed`, `rows_total`, the module row cap and the 1 -> REPRESENTED (report L4180)
511. [src L617] X-13 INV-010: row quote boundaries disagree (12-character minimum against C4/C8  -> REPRESENTED (report L4181)
512. [src L618] X-13 INV-011: compliance feeds quorum arithmetic only through the empty-block ru -> REPRESENTED (report L4182)
513. [src L619] X-13 INV-014: what `assigned` holds per card, what the loader does with a bad ca -> REPRESENTED (report L4183)
514. [src L620] X-13 INV-015: the v1 loop edit is the rules file plus its plugin byte copy, not  -> REPRESENTED (report L4184)
515. [src L621] X-13 INV-016: in shadow mode the card body still reaches the legacy debate; the  -> REPRESENTED (report L4185)
516. [src L622] X-13 INV-017: `review-telemetry/1` reviewer records are closed; new counters fit -> REPRESENTED (report L4186)
517. [src L623] X-13 INV-020: advisory checks need a reader and a route to the fix (the v1 merge -> REPRESENTED (report L4187)
518. [src L624] X-13 INV-008: UNSURE counts as observed, so an all-UNSURE clean report passes th -> REPRESENTED (report L4188)
519. [src L625] X-14 INV-001: a rule committed after C-02 lands can still be measuring a kernel  -> REPRESENTED (report L4189)
520. [src L626] X-14 INV-002: git commit order is not execution order, nothing stamps the rule c -> REPRESENTED (report L4190)
521. [src L627] X-14 INV-003: re-parse conservation can give false flags when parser or policy v -> REPRESENTED (report L4191)
522. [src L628] X-14 INV-005: no expected-cells manifest exists in any adjudicated output or E2  -> REPRESENTED (report L4192)
523. [src L629] X-14 INV-006: a verifier record that is all `unrecorded`, or a truncated `flags. -> REPRESENTED (report L4193)
524. [src L630] X-14 INV-007: the judge writes its own three counts and `gt_covered_blocking` ha -> REPRESENTED (report L4194)
525. [src L631] X-14 INV-013: the unit of analysis is not named (the 71 rows hold 32 multisets;  -> REPRESENTED (report L4195)
526. [src L632] X-14 INV-019: the adjudicated C-06 hybrid already adds `repaired` and `dropped`  -> REPRESENTED (report L4196)
527. [src L633] X-14 INV-021: the verifier reports `unrecorded` where C-08's identity gate maps  -> REPRESENTED (report L4197)
528. [src L634] X-14 INV-025: the metric of record and the conservation law are defined on `revi -> REPRESENTED (report L4198)
529. [src L635] X-14 INV-026: the answer-key and tool-use defect class has no component; if C-08 -> REPRESENTED (report L4199)
530. [src L636] X-14 INV-027: inline enumeration: an identity swap, a dispatch-skipped cell, a j -> REPRESENTED (report L4200)
531. [src L637] X-14 INV-004: ledgers written before and after C-02 are read differently (stored -> REPRESENTED (report L4201)
532. [src L638] X-14 INV-008: the single severity policy file decides the audit-clean population -> REPRESENTED (report L4202)
533. [src L639] X-14 INV-011: "71" is not one population and the denominators 8 and 14 ignore th -> REPRESENTED (report L4203)
534. [src L640] X-14 INV-012: part of the 89 against 38 gap may be rejected blocking lines (C-06 -> REPRESENTED (report L4204)
535. [src L641] X-14 INV-015: the expected cell has no attempt component; an empty manifest pass -> REPRESENTED (report L4205)
536. [src L642] X-14 INV-016: the headline and "control found" are undefined for a package with  -> REPRESENTED (report L4206)
537. [src L643] X-14 INV-017: M-6 may not show the gate bites: on real data the repaired gate ca -> REPRESENTED (report L4207)
538. [src L644] X-14 INV-018: one run per cell and one judge pass per (package, label) leave the -> REPRESENTED (report L4208)
539. [src L645] X-14 INV-020: "ledger row typed blocking" is not one stable field after C-02's C -> REPRESENTED (report L4209)
540. [src L646] X-14 INV-022: `.gitignore:13` (`lib/`, `build/`, `dist/`, `parts/`, `var/`) can  -> REPRESENTED (report L4210)
541. [src L647] X-14 INV-023: path-less CI `pytest -n auto --maxfail=3` collecting harness tests -> REPRESENTED (report L4211)
542. [src L648] X-14 INV-028: the 16-item ground truth has unrecorded authorship and one impleme -> REPRESENTED (report L4212)
543. [src L649] X-14 INV-029: a post-run verifier finds a bad run after the judge cost is paid;  -> REPRESENTED (report L4213)
544. [src L650] X-15 INV-017: "nothing loosens before measurement, so H+ is behaviour-preserving -> REPRESENTED (report L4214)
545. [src L651] X-15 INV-018: "grading block + tie-break-up + dedup-highest makes the boundary s -> REPRESENTED (report L4215)
546. [src L652] X-15 INV-001: `ValidationReport.md` is written once from the first Stage 7 merge -> REPRESENTED (report L4216)
547. [src L653] X-15 INV-003: no CRITICAL floor exists in code yet and it covers CRITICAL only;  -> REPRESENTED (report L4217)
548. [src L654] X-15 INV-004: `SK:1410` leaves "the same issue on the same task" to the model; k -> REPRESENTED (report L4218)
549. [src L655] X-15 INV-005: the containment test T2(a) and (b) cannot pass as written; a stati -> REPRESENTED (report L4219)
550. [src L656] X-15 INV-007: `F_k` counts post-dedup findings while the loop works on task ids; -> REPRESENTED (report L4220)
551. [src L657] X-15 INV-008: `SK:1703, :1705, :1716, :1766` and the totals line `SK:1462` state -> REPRESENTED (report L4221)
552. [src L658] X-15 INV-010: (A+ only) the clean template has a slot for Low notes only; a Medi -> REPRESENTED (report L4222)
553. [src L659] X-15 INV-011: F1 to F3 rest on two archived bundles and per-finding thresholds;  -> REPRESENTED (report L4223)
554. [src L660] X-15 INV-013: tie-break-up enlarges the blocking set; a Low-graded PASS item re- -> REPRESENTED (report L4224)
555. [src L661] X-15 INV-014: H+ keeps `SK:1421-1422` MEDIUM while the adopted block calls omiss -> REPRESENTED (report L4225)
556. [src L662] X-15 INV-019: eleven filters sit between a Stage 7 finding and the verdict; seve -> REPRESENTED (report L4226)
557. [src L663] X-15 INV-020: F1 cannot fail H+ by construction and cannot test the High/Medium  -> REPRESENTED (report L4227)
558. [src L664] X-15 INV-002: the byte-equal fixture guard skips when the plan copy is absent an -> REPRESENTED (report L4228)
559. [src L665] X-15 INV-009: the "76 lines in 10 files" against "88 lines in 14 files" count is -> REPRESENTED (report L4229)
560. [src L666] X-15 INV-012: a one-task phase has one grader, so dedup and tie-break-up cannot  -> REPRESENTED (report L4230)
561. [src L668] Row counts of this table: 244 (C-01 16, C-02 16, C-03 12, C-04 17, C-05 12, C-06 -> REPRESENTED (report L4232)
562. [src L670] End of synthesis 07. -> not a content line (title/metadata) [no report line]
563. [src L672] End of synthesis 07. -> not a content line (title/metadata) [no report line]
COUNT synthesis/synth-07-recommendation-architecture.md: 563

## reviews/adversarial/*/ADJUDICATION-RESULT.md (15 files)
Per file: entries = every non-blank line of the sections Winner, Rationale, Conditions, Unresolved / Open items, Return contract, plus every unaddressed-invariant item. Outcome / rationale / conditions are represented in condensed form by the 6.12.9.1 row of the slot (report L3511-L3525) and by 7.0.1 (report L3580-3625) and the Section 7 choices table; every unaddressed invariant is a row in 7.3 (report L3985-4233, matched by slot+id and by assumption text, 218 of 218 table-form items plus the prose-form items of C-02 and C-09, 244 rows in total). Token coverage x/y = share of the line's code tokens, ids and numbers found anywhere in the report.

### collaboration-exchange-capability (C-12)
1. [L7] **A named hybrid that the debate itself produced: a staged resolution on the Proposal A ba -> REPRESENTED (condensed, 6.12.9.1 row C-12, report L3522; tokens 0/0)
2. [L9] The debate's own base selection (`adversarial/base-selection.md`): -> REPRESENTED (condensed, 6.12.9.1 row C-12, report L3522; tokens 0/1)
3. [L11] | Variant | Quant (mean of two passes) | Qual (after re-evaluation) | Combined | -> REPRESENTED (condensed, 6.12.9.1 row C-12, report L3522; tokens 0/0)
4. [L13] | A (Proposal A) | 0.9729 | 26/30 = 0.8667 | **0.9198** | -> REPRESENTED (condensed, 6.12.9.1 row C-12, report L3522; tokens 3/5)
5. [L14] | B (Proposal B) | 0.9493 | 24/30 = 0.8000 | **0.8747** | -> REPRESENTED (condensed, 6.12.9.1 row C-12, report L3522; tokens 3/5)
6. [L16] Margin 4.51%, below the 5% threshold, so the tiebreaker applied. Level 1 (debate performan -> REPRESENTED (condensed, 6.12.9.1 row C-12, report L3522; tokens 8/11)
7. [L20] - The evidence does not support building the exchange transport now. At HEAD the gateway l -> REPRESENTED (condensed, 6.12.9.1 row C-12, report L3522; tokens 5/7)
8. [L21] - Proposal A's gate ("not built until an exchange arm beats the kit") was also wrong as wr -> REPRESENTED (condensed, 6.12.9.1 row C-12, report L3522; tokens 0/0)
9. [L22] - Points where the debate favoured Proposal B and which the merged position keeps: C-010 ( -> REPRESENTED (condensed, 6.12.9.1 row C-12, report L3522; tokens 10/17)
10. [L23] - Scoring-matrix result: A 12, B 5, Merge 2, Tie 2, Unresolved 1 (C-002, open only on its  -> REPRESENTED (condensed, 6.12.9.1 row C-12, report L3522; tokens 13/14)
11. [L27] 1. Core now: H1, H2, H3, H4 principle, a per-module catalogue ("static kit") with `kit: of -> REPRESENTED (condensed, 6.12.9.1 row C-12, report L3522; tokens 7/7)
12. [L28] 2. Build trigger (all three): slot C-07 adjudicated to a launcher with session persistence -> REPRESENTED (condensed, 6.12.9.1 row C-12, report L3522; tokens 7/7)
13. [L29] 3. Enable trigger (lifts `exchange: off`): a pre-registered two-sided gain-and-cost rule a -> REPRESENTED (condensed, 6.12.9.1 row C-12, report L3522; tokens 8/8)
14. [L30] 4. Design note (binding preconditions, not code): `panel-msg/1` per-kind keys, forbidden k -> REPRESENTED (condensed, 6.12.9.1 row C-12, report L3522; tokens 6/8)
15. [L31] 5. Stricter off-state test: no new file under `~/.claude/hooks/`, no `hooks.json` or merge -> REPRESENTED (condensed, 6.12.9.1 row C-12, report L3522; tokens 3/3)
16. [L58] - **[POST-BASELINE] premise check.** The research pins the tasklist-study tip `6c0984326cb -> REPRESENTED (condensed, 6.12.9.1 row C-12, report L3522; tokens 9/9)
17. [L59] - Unresolved diff point C-002 (label only), and the question whether the reserved `exchang -> REPRESENTED (condensed, 6.12.9.1 row C-12, report L3522; tokens 3/3)
18. [L60] - Cross-slot dependencies the result rests on: C-06 (H2 policy), C-07 (launcher), C-08 (se -> REPRESENTED (condensed, 6.12.9.1 row C-12, report L3522; tokens 6/6)
19. [invariant] C-12 INV-005 | INV-005 | HIGH | UNADDRESSED | H1 reaches reflect through the reflect brief wi -> REPRESENTED (7.3 row, report L4159)
20. [invariant] C-12 INV-009 | INV-009 | HIGH | UNADDRESSED | H2 (a repair, possibly a re-ask) is core now an -> REPRESENTED (7.3 row, report L4160)
21. [invariant] C-12 INV-002 | INV-002 | MEDIUM | UNADDRESSED | the served-model and act-rate probe record ha -> REPRESENTED (7.3 row, report L4161)
22. [invariant] C-12 INV-003 | INV-003 | MEDIUM | UNADDRESSED | a reserved `exchange` key is "a pin, not an i -> REPRESENTED (7.3 row, report L4162)
23. [invariant] C-12 INV-004 | INV-004 | MEDIUM | UNADDRESSED | the off-state byte test coexists with H1 ship -> REPRESENTED (7.3 row, report L4163)
24. [invariant] C-12 INV-006 | INV-006 | MEDIUM | UNADDRESSED | a single kit cost figure can gate `kit: on` ( -> REPRESENTED (7.3 row, report L4164)
25. [invariant] C-12 INV-007 | INV-007 | MEDIUM | UNADDRESSED | a hold-out of at least 4 unseen defects is sa -> REPRESENTED (7.3 row, report L4165)
26. [invariant] C-12 INV-008 | INV-008 | MEDIUM | UNADDRESSED | a sidecar keyed by reviewer id and finding id -> REPRESENTED (7.3 row, report L4166)
27. [invariant] C-12 INV-010 | INV-010 | MEDIUM | UNADDRESSED | one catalogue source per module, rendered fro -> REPRESENTED (7.3 row, report L4167)
28. [invariant] C-12 INV-011 | INV-011 | MEDIUM | UNADDRESSED | "quorum counts over own-origin lines only" is -> REPRESENTED (7.3 row, report L4168)
29. [invariant] C-12 INV-013 | INV-013 | MEDIUM | UNADDRESSED | the A-layer alone gives mutually blind review -> REPRESENTED (7.3 row, report L4169)
30. [invariant] C-12 INV-014 | INV-014 | MEDIUM | UNADDRESSED | the enable trigger can be met on a lane that  -> REPRESENTED (7.3 row, report L4170)
31. [invariant] C-12 INV-015 | INV-015 | MEDIUM | UNADDRESSED | the A-layer alone is cost-safe (H2 re-ask spe -> REPRESENTED (7.3 row, report L4171)
32. [invariant] C-12 INV-016 | INV-016 | MEDIUM | UNADDRESSED | the premise "no exchange arm has been measure -> REPRESENTED (7.3 row, report L4172)
COUNT collaboration-exchange-capability/ADJUDICATION-RESULT.md: 32

### consumer-entry-effect-and-delivery (C-05)
1. [L7] **Variant A (Proposal A) as the base, merged as the hybrid the debate itself produced.** T -> REPRESENTED (condensed, 6.12.9.1 row C-05, report L3515; tokens 7/7)
2. [L9] The merged resolution, as the debate produced it: -> REPRESENTED (condensed, 6.12.9.1 row C-05, report L3515; tokens 0/0)
3. [L10] - **Entry (C-001, Variant A wins, 90%).** Workflow Wave 4 and tasklist Stage 10.5 keep the -> REPRESENTED (condensed, 6.12.9.1 row C-05, report L3515; tokens 4/5)
4. [L11] - **Effect (C-002, Hybrid, 90%).** Advisory at Wave 4. Stage 10.5 is "advisory-blocking" b -> REPRESENTED (condensed, 6.12.9.1 row C-05, report L3515; tokens 10/10)
5. [L12] - **Delivery (C-003, Variant A wins, 93%).** No panel-only plugin copy; plugin delivery is -> REPRESENTED (condensed, 6.12.9.1 row C-05, report L3515; tokens 0/2)
6. [L13] - Structure and measurement taken from Variant B: the three separable parts (S-002), per-r -> REPRESENTED (condensed, 6.12.9.1 row C-05, report L3515; tokens 2/3)
7. [L17] - Quantitative layer: A 0.9789, B 0.9808 (requirement coverage A 1.0000, B 1.0000; interna -> REPRESENTED (condensed, 6.12.9.1 row C-05, report L3515; tokens 1/6)
8. [L18] - Qualitative layer (30 criteria, two position-bias passes, 3 of 60 pairs re-evaluated, th -> REPRESENTED (condensed, 6.12.9.1 row C-05, report L3515; tokens 8/10)
9. [L19] - Combined: A 0.8728, B 0.8904. "Margin: 0.0176 (1.76%), below the 5% threshold. Variant B -> REPRESENTED (condensed, 6.12.9.1 row C-05, report L3515; tokens 8/11)
10. [L20] - The debate's stated reason: the combined score does not select a base on its own; both v -> REPRESENTED (condensed, 6.12.9.1 row C-05, report L3515; tokens 9/9)
11. [L21] - Both layers are reported: the quantitative layer and the qualitative layer each favoured -> REPRESENTED (condensed, 6.12.9.1 row C-05, report L3515; tokens 0/0)
12. [L22] - Convergence: 24 of 24 diff points agreed (100%) against an 80% threshold. Status BLOCKED -> REPRESENTED (condensed, 6.12.9.1 row C-05, report L3515; tokens 3/3)
13. [L26] 1. It holds while the C-01 to C-03 outcomes stand (reflect keeps its own engine and `short -> REPRESENTED (condensed, 6.12.9.1 row C-05, report L3515; tokens 4/4)
14. [L27] 2. It reopens if the replay shows the direct path catches materially more blocking ground- -> REPRESENTED (condensed, 6.12.9.1 row C-05, report L3515; tokens 3/3)
15. [L28] 3. The engine switch is released only after the replay, a contract-compat test against the -> REPRESENTED (condensed, 6.12.9.1 row C-05, report L3515; tokens 4/4)
16. [L29] 4. Reach behind reflect is limited and unsized: workflow reaches a panel only on rubric es -> REPRESENTED (condensed, 6.12.9.1 row C-05, report L3515; tokens 4/4)
17. [L30] 5. Advisory first; any blocking use waits for a replay. A zero-success blocking feed must  -> REPRESENTED (condensed, 6.12.9.1 row C-05, report L3515; tokens 2/2)
18. [L31] 6. Additive keys at `contract_version` "1.1" are safe at the three consumer-side readers;  -> REPRESENTED (condensed, 6.12.9.1 row C-05, report L3515; tokens 5/5)
19. [L32] 7. Nothing was run: no test, no headless call, no replay. The plugin CLI availability, `ve -> REPRESENTED (condensed, 6.12.9.1 row C-05, report L3515; tokens 4/4)
20. [L33] 8. No Round 3 ran (depth standard) and no second pass of the 24-point matrix ran after the -> REPRESENTED (condensed, 6.12.9.1 row C-05, report L3515; tokens 3/3)
21. [L60] Status `partial`; convergence score 1.00 (24 of 24 diff points agreed; status BLOCKED_BY_I -> REPRESENTED (condensed, 6.12.9.1 row C-05, report L3515; tokens 5/6)
22. [invariant] C-05 INV-001 | INV-001 | HIGH | guard_conditions | "Advisory at Wave 4 and Stage 10.5": Stage -> REPRESENTED (7.3 row, report L4048)
23. [invariant] C-05 INV-002 | INV-002 | HIGH | interaction_effects | Stage 10.5 always passes `--remediate`, -> REPRESENTED (7.3 row, report L4049)
24. [invariant] C-05 INV-003 | INV-003 | HIGH | interaction_effects | The depth-policy remedy changes the rem -> REPRESENTED (7.3 row, report L4050)
25. [invariant] C-05 INV-005 | INV-005 | HIGH | collection_boundaries | The reach share has no working instru -> REPRESENTED (7.3 row, report L4051)
26. [invariant] C-05 INV-007 | INV-007 | HIGH | count_divergence | "Only `status`, `coverage_pct`, `tier_reac -> REPRESENTED (7.3 row, report L4052)
27. [invariant] C-05 INV-013 | INV-013 | HIGH | sufficiency_challenge | The replay that decides every dispute -> REPRESENTED (7.3 row, report L4053)
28. [invariant] C-05 INV-014 | INV-014 | HIGH | sufficiency_challenge | The consensus does not show consumers -> REPRESENTED (7.3 row, report L4054)
29. [invariant] C-05 INV-004 | INV-004 | MEDIUM | guard_conditions | A call-site depth flag is not "pin-safe" -> REPRESENTED (7.3 row, report L4055)
30. [invariant] C-05 INV-006 | INV-006 | MEDIUM | collection_boundaries | The reach-share denominator is unde -> REPRESENTED (7.3 row, report L4056)
31. [invariant] C-05 INV-008 | INV-008 | MEDIUM | count_divergence | A default flip reaches every UC-1 caller -> REPRESENTED (7.3 row, report L4057)
32. [invariant] C-05 INV-010 | INV-010 | MEDIUM | state_variables | "One reflect-side switch" is prose in thr -> REPRESENTED (7.3 row, report L4058)
33. [invariant] C-05 INV-011 | INV-011 | MEDIUM | guard_conditions | A contract-compat test against the 36-te -> REPRESENTED (7.3 row, report L4059)
COUNT consumer-entry-effect-and-delivery/ADJUDICATION-RESULT.md: 33

### core-shape-and-finding-contract (C-01)
1. [L8] A named hybrid that the debate itself produced, with Variant B as the selected base (`base -> REPRESENTED (condensed, 6.12.9.1 row C-01, report L3511; tokens 3/3)
2. [L10] What the hybrid contains, as both advocates left it after Round 2 (`merged-core-shape-and- -> REPRESENTED (condensed, 6.12.9.1 row C-01, report L3511; tokens 2/2)
3. [L11] - Shared now: finding id grammar `_ID`; one limits-constants module imported by both parse -> REPRESENTED (condensed, 6.12.9.1 row C-01, report L3511; tokens 5/5)
4. [L12] - Engines per module: spec loop stays on v1 `findings.py`, `ledger.py`, `review-ledger/1`  -> REPRESENTED (condensed, 6.12.9.1 row C-01, report L3511; tokens 6/6)
5. [L13] - Withdrawn from Variant A: locator-agnostic `annotate`, `citations` in ledger rows, the c -> REPRESENTED (condensed, 6.12.9.1 row C-01, report L3511; tokens 4/4)
6. [L14] - Unknown keys open in both parsers; ledger passthrough keys deferred; `prior` lines uncha -> REPRESENTED (condensed, 6.12.9.1 row C-01, report L3511; tokens 3/3)
7. [L15] - Convergence to one engine only on a trigger: T-a (a module needs re-review rounds over c -> REPRESENTED (condensed, 6.12.9.1 row C-01, report L3511; tokens 2/2)
8. [L19] Quoted from `adversarial/base-selection.md`: -> REPRESENTED (condensed, 6.12.9.1 row C-01, report L3511; tokens 0/1)
9. [L20] - Quantitative layer: Variant A 0.985, Variant B 0.936. -> REPRESENTED (condensed, 6.12.9.1 row C-01, report L3511; tokens 0/2)
10. [L21] - Qualitative layer (two independent passes, five disagreements re-evaluated): Variant A 2 -> REPRESENTED (condensed, 6.12.9.1 row C-01, report L3511; tokens 6/7)
11. [L22] - Combined: Variant A 0.8760, Variant B 0.8515. "Margin: 2.45 percent (below the 5 percent -> REPRESENTED (condensed, 6.12.9.1 row C-01, report L3511; tokens 10/12)
12. [L23] - Selection rationale in the debate's words: the debate moved toward B's shape after both  -> REPRESENTED (condensed, 6.12.9.1 row C-01, report L3511; tokens 9/9)
13. [L27] As recorded in the debate (Round 2 hybrids of both advocates, `merged-core-shape-and-findi -> REPRESENTED (condensed, 6.12.9.1 row C-01, report L3511; tokens 5/5)
14. [L28] 1. The convergence triggers T-a, T-b, T-c have not fired. If one fires, the debate's recor -> REPRESENTED (condensed, 6.12.9.1 row C-01, report L3511; tokens 1/1)
15. [L29] 2. The pre-registered location-reliability measurement (merged T3 and 5.3) is run only aft -> REPRESENTED (condensed, 6.12.9.1 row C-01, report L3511; tokens 4/4)
16. [L30] 3. Tests: T1 (all existing pins pass unmodified, with `test_review_cluster.py:279-293` and -> REPRESENTED (condensed, 6.12.9.1 row C-01, report L3511; tokens 12/12)
17. [L31] 4. Anchor status is surfaced in the per-row `### Lx` block of `## Blocking findings`, not  -> REPRESENTED (condensed, 6.12.9.1 row C-01, report L3511; tokens 4/4)
18. [L32] 5. The shared repair step must not invent an anchor for a citation-only line, and its poli -> REPRESENTED (condensed, 6.12.9.1 row C-01, report L3511; tokens 4/4)
19. [L33] 6. Two disputes between the advocates were not reconciled and are recorded in the merged d -> REPRESENTED (condensed, 6.12.9.1 row C-01, report L3511; tokens 3/3)
20. [L34] 7. Clearing rules (clearing ignores block validity; how an unlocated row may clear) are de -> REPRESENTED (condensed, 6.12.9.1 row C-01, report L3511; tokens 3/3)
21. [invariant] C-01 INV-003 | INV-003 | HIGH | guard_conditions | A repair step inside both `parse_block` fu -> REPRESENTED (7.3 row, report L3989)
22. [invariant] C-01 INV-001 | INV-001 | MEDIUM | state_variables | Anchor status can be surfaced for every b -> REPRESENTED (7.3 row, report L3987)
23. [invariant] C-01 INV-002 | INV-002 | MEDIUM | state_variables | Adding `T<PP>.<TT>` to the shared token l -> REPRESENTED (7.3 row, report L3988)
24. [invariant] C-01 INV-004 | INV-004 | MEDIUM | guard_conditions | The same repair gives the same benefit i -> REPRESENTED (7.3 row, report L3990)
25. [invariant] C-01 INV-009 | INV-009 | MEDIUM | count_divergence | The 3-line clustering tolerance means th -> REPRESENTED (7.3 row, report L3991)
26. [invariant] C-01 INV-010 | INV-010 | MEDIUM | count_divergence | The two parsers hold the only copies of  -> REPRESENTED (7.3 row, report L3992)
27. [invariant] C-01 INV-014 | INV-014 | MEDIUM | collection_boundaries | A round whose only reviewer has onl -> REPRESENTED (7.3 row, report L3993)
28. [invariant] C-01 INV-015 | INV-015 | MEDIUM | collection_boundaries | A stuck row is one row, so surfacin -> REPRESENTED (7.3 row, report L3994)
29. [invariant] C-01 INV-016 | INV-016 | MEDIUM | interaction_effects | The merged T2 gate catches every shar -> REPRESENTED (7.3 row, report L3995)
30. [invariant] C-01 INV-017 | INV-017 | MEDIUM | interaction_effects | Adding the token once in `refs_norm`  -> REPRESENTED (7.3 row, report L3996)
31. [invariant] C-01 INV-018 | INV-018 | MEDIUM | interaction_effects | Shared helpers can move into a new mo -> REPRESENTED (7.3 row, report L3997)
32. [invariant] C-01 INV-020 | INV-020 | MEDIUM | interaction_effects | "No change to `cli/reflect`" means th -> REPRESENTED (7.3 row, report L3998)
33. [invariant] C-01 INV-021 | INV-021 | MEDIUM | interaction_effects | The merged T2 has committed v1 ledger -> REPRESENTED (7.3 row, report L3999)
34. [invariant] C-01 INV-022 | INV-022 | MEDIUM | interaction_effects | Whatever repair policy C-06 picks lea -> REPRESENTED (7.3 row, report L4000)
35. [invariant] C-01 INV-024 | INV-024 | MEDIUM | sufficiency_challenge | The consensus alone resolves FX-1 a -> REPRESENTED (7.3 row, report L4001)
36. [invariant] C-01 INV-008 | INV-008 | LOW | count_divergence | One constant per limit is safe when equal n -> REPRESENTED (7.3 row, report L4002)
COUNT core-shape-and-finding-contract/ADJUDICATION-RESULT.md: 36

### dispatch-and-launch-mechanism (C-07)
1. [L7] **Variant 2 (Proposal B) as the base, merged as the hybrid the debate itself produced.** T -> REPRESENTED (condensed, 6.12.9.1 row C-07, report L3517; tokens 7/7)
2. [L11] - Quantitative layer: Variant 1 0.8773, Variant 2 0.9800 (requirement coverage 0.8000 agai -> REPRESENTED (condensed, 6.12.9.1 row C-07, report L3517; tokens 3/10)
3. [L12] - Qualitative layer (30 criteria, two position-bias passes, 8 of 60 pairs re-evaluated): V -> REPRESENTED (condensed, 6.12.9.1 row C-07, report L3517; tokens 10/12)
4. [L13] - Combined: Variant 1 0.8053, Variant 2 0.9233. "Margin: 11.80% (above the 5% threshold)". -> REPRESENTED (condensed, 6.12.9.1 row C-07, report L3517; tokens 7/8)
5. [L14] - The debate's stated reason: Variant 1 lost Correctness on two intra-variant contradictio -> REPRESENTED (condensed, 6.12.9.1 row C-07, report L3517; tokens 4/10)
6. [L15] - Convergence: 21 of 26 diff points agreed (80.77%) against an 80% threshold; Round 1 agre -> REPRESENTED (condensed, 6.12.9.1 row C-07, report L3517; tokens 5/7)
7. [L19] 1. The scores rate the two documents as written. The gated hybrid was not scored. -> REPRESENTED (condensed, 6.12.9.1 row C-07, report L3517; tokens 1/1)
8. [L20] 2. What both advocates agreed ships now: the dispatch rule (S1), no packaged tier, resolve -> REPRESENTED (condensed, 6.12.9.1 row C-07, report L3517; tokens 10/10)
9. [L21] 3. The `claude-p` launcher is gated, not built: it needs G1 (identity and reach under the  -> REPRESENTED (condensed, 6.12.9.1 row C-07, report L3517; tokens 6/6)
10. [L22] 4. Read-only by construction is a static pin for the agent-file path only; the dynamic no- -> REPRESENTED (condensed, 6.12.9.1 row C-07, report L3517; tokens 1/1)
11. [L23] 5. A class-word binding is correct only for the session binding it states; a mismatch is f -> REPRESENTED (condensed, 6.12.9.1 row C-07, report L3517; tokens 3/3)
12. [L24] 6. Claude Code behaviours the repo does not pin (the Agent enum, `resolvedModel`, `message -> REPRESENTED (condensed, 6.12.9.1 row C-07, report L3517; tokens 6/6)
13. [L25] 7. Two things the debate left split between the advocates, recorded side by side in the me -> REPRESENTED (condensed, 6.12.9.1 row C-07, report L3517; tokens 11/11)
14. [L54] Status `partial`; convergence score 0.81 (21 of 26 = 0.8077); base variant `variant-2 (Pro -> REPRESENTED (condensed, 6.12.9.1 row C-07, report L3517; tokens 11/14)
15. [invariant] C-07 INV-017 | INV-017 | HIGH | sufficiency_challenge | The ship-now set does not by itself c -> REPRESENTED (7.3 row, report L4080)
16. [invariant] C-07 INV-001 | INV-001 | MEDIUM | state_variables | A class-word binding written as data is n -> REPRESENTED (7.3 row, report L4081)
17. [invariant] C-07 INV-003 | INV-003 | MEDIUM | state_variables | S5 is stated in two forms (`find_path` ov -> REPRESENTED (7.3 row, report L4082)
18. [invariant] C-07 INV-005 | INV-005 | MEDIUM | guard_conditions | S1 does not govern calibrator calls; a r -> REPRESENTED (7.3 row, report L4083)
19. [invariant] C-07 INV-006 | INV-006 | MEDIUM | guard_conditions | S4 passes if the model declines in prose -> REPRESENTED (7.3 row, report L4084)
20. [invariant] C-07 INV-007 | INV-007 | MEDIUM | guard_conditions | G2 has no "reads its inputs and returns  -> REPRESENTED (7.3 row, report L4085)
21. [invariant] C-07 INV-009 | INV-009 | MEDIUM | count_divergence | Three reviewers on three class words lea -> REPRESENTED (7.3 row, report L4086)
22. [invariant] C-07 INV-010 | INV-010 | MEDIUM | count_divergence | S6's "same panel for any run id" is fals -> REPRESENTED (7.3 row, report L4087)
23. [invariant] C-07 INV-011 | INV-011 | MEDIUM | count_divergence | The transcript reader's key (reviewer id -> REPRESENTED (7.3 row, report L4088)
24. [invariant] C-07 INV-014 | INV-014 | MEDIUM | interaction_effects | Executor-class exclusion expands thro -> REPRESENTED (7.3 row, report L4089)
25. [invariant] C-07 INV-015 | INV-015 | MEDIUM | interaction_effects | S1 and the shadow fence: applied to s -> REPRESENTED (7.3 row, report L4090)
26. [invariant] C-07 INV-016 | INV-016 | MEDIUM | interaction_effects | Once `claude-p` is a permitted `launc -> REPRESENTED (7.3 row, report L4091)
27. [invariant] C-07 INV-018 | INV-018 | MEDIUM | sufficiency_challenge | The ship-now set does not change be -> REPRESENTED (7.3 row, report L4092)
28. [invariant] C-07 INV-002 | INV-002 | LOW | state_variables | A static fixture copy of the tier file tests -> REPRESENTED (7.3 row, report L4093)
29. [invariant] C-07 INV-004 | INV-004 | LOW | guard_conditions | S1's "`launch: null` is a dispatch error" c -> REPRESENTED (7.3 row, report L4094)
30. [invariant] C-07 INV-012 | INV-012 | LOW | collection_boundaries | `resolve` prints a launch word for the -> REPRESENTED (7.3 row, report L4095)
COUNT dispatch-and-launch-mechanism/ADJUDICATION-RESULT.md: 30

### eval-acceptance-and-harness-owner (X-14)
1. [L7] **Variant A (Proposal A) as the base, merged as the hybrid the debate itself produced.** T -> REPRESENTED (condensed, 6.12.9.1 row X-14, report L3524; tokens 6/7)
2. [L11] - Quantitative layer: A 0.9980, B 0.9787 (requirement coverage 1.0000 each; internal consi -> REPRESENTED (condensed, 6.12.9.1 row X-14, report L3524; tokens 0/6)
3. [L12] - Qualitative layer (30 criteria, two position-bias passes, 4 of 60 criterion-variant pair -> REPRESENTED (condensed, 6.12.9.1 row X-14, report L3524; tokens 9/10)
4. [L13] - Combined: A 0.9157, B 0.9060. "Margin: 0.0097 (0.97%) (below the 5% threshold)". "Tiebre -> REPRESENTED (condensed, 6.12.9.1 row X-14, report L3524; tokens 12/17)
5. [L14] - The debate's stated reasons for the base: A won the points that decide a base for this s -> REPRESENTED (condensed, 6.12.9.1 row X-14, report L3524; tokens 0/0)
6. [L15] - Honest limits stated in the base selection: the qualitative totals tie and the margin is -> REPRESENTED (condensed, 6.12.9.1 row X-14, report L3524; tokens 8/9)
7. [L16] - Convergence: 40 of 44 diff points agreed (90.9%; Round 1 was 28 of 44, 63.6%; counting o -> REPRESENTED (condensed, 6.12.9.1 row X-14, report L3524; tokens 14/17)
8. [L20] 1. The acceptance status wording: a use case is "accepted" only with Tier S, a pre-registe -> REPRESENTED (condensed, 6.12.9.1 row X-14, report L3524; tokens 2/2)
9. [L21] 2. E1 and E2 are one evidence family and the 16-item ground truth is a derivation set, so  -> REPRESENTED (condensed, 6.12.9.1 row X-14, report L3524; tokens 3/3)
10. [L22] 3. The kernel `verify-run` command is deferred, not rejected. The flip condition both advo -> REPRESENTED (condensed, 6.12.9.1 row X-14, report L3524; tokens 4/4)
11. [L23] 4. The metric of record is reported per item, with unmatched blocking rows (not "wrong blo -> REPRESENTED (condensed, 6.12.9.1 row X-14, report L3524; tokens 5/5)
12. [L24] 5. Timing: the rule, analysis script and values file are committed after slot C-02 lands a -> REPRESENTED (condensed, 6.12.9.1 row X-14, report L3524; tokens 6/6)
13. [L25] 6. The identity check reports `unrecorded` until a writer of `model.observed` exists (noth -> REPRESENTED (condensed, 6.12.9.1 row X-14, report L3524; tokens 5/5)
14. [L26] 7. One kernel touch stays open: conservation needs the raw text of a rejected line, which  -> REPRESENTED (condensed, 6.12.9.1 row X-14, report L3524; tokens 5/5)
15. [L27] 8. The dispatch-time expected-cells manifest (written before `panel.resolve` drops skipped -> REPRESENTED (condensed, 6.12.9.1 row X-14, report L3524; tokens 2/2)
16. [L28] 9. The import of the E2 harness into the main line needs a named owner and a `.gitignore`  -> REPRESENTED (condensed, 6.12.9.1 row X-14, report L3524; tokens 10/10)
17. [L29] 10. The two reflect-gate repairs (`scripts/reflect_shadow_exit.py:313` and `:59`) and the  -> REPRESENTED (condensed, 6.12.9.1 row X-14, report L3524; tokens 5/5)
18. [L30] 11. Slot C-06 and slot C-08 have been adjudicated since the proposals were written and are -> REPRESENTED (condensed, 6.12.9.1 row X-14, report L3524; tokens 3/3)
19. [L68] Diff points C-005, C-007, C-008 and X-004: the two Round 2 calls differ (A against TIE) wh -> REPRESENTED (condensed, 6.12.9.1 row X-14, report L3524; tokens 6/6)
20. [invariant] X-14 INV-001 | INV-001 | HIGH | state_variables | A rule committed after C-02 lands can still -> REPRESENTED (7.3 row, report L4189)
21. [invariant] X-14 INV-002 | INV-002 | HIGH | state_variables | Git commit order is not execution order, no -> REPRESENTED (7.3 row, report L4190)
22. [invariant] X-14 INV-003 | INV-003 | HIGH | state_variables | Re-parse conservation can give false flags  -> REPRESENTED (7.3 row, report L4191)
23. [invariant] X-14 INV-005 | INV-005 | HIGH | state_variables | No expected-cells manifest exists in any ad -> REPRESENTED (7.3 row, report L4192)
24. [invariant] X-14 INV-006 | INV-006 | HIGH | guard_conditions | A verifier record that is all `unrecorded` -> REPRESENTED (7.3 row, report L4193)
25. [invariant] X-14 INV-007 | INV-007 | HIGH | guard_conditions | The judge writes its own three counts and  -> REPRESENTED (7.3 row, report L4194)
26. [invariant] X-14 INV-013 | INV-013 | HIGH | count_divergence | The unit of analysis is not named: the 71  -> REPRESENTED (7.3 row, report L4195)
27. [invariant] X-14 INV-019 | INV-019 | HIGH | interaction_effects | The adjudicated C-06 hybrid already add -> REPRESENTED (7.3 row, report L4196)
28. [invariant] X-14 INV-021 | INV-021 | HIGH | interaction_effects | The verifier reports `unrecorded` where -> REPRESENTED (7.3 row, report L4197)
29. [invariant] X-14 INV-025 | INV-025 | HIGH | sufficiency_challenge | The metric of record and the conserva -> REPRESENTED (7.3 row, report L4198)
30. [invariant] X-14 INV-026 | INV-026 | HIGH | sufficiency_challenge | The answer-key and tool-use defect cl -> REPRESENTED (7.3 row, report L4199)
31. [invariant] X-14 INV-027 | INV-027 | HIGH | sufficiency_challenge | Inline enumeration: an identity swap, -> REPRESENTED (7.3 row, report L4200)
32. [invariant] X-14 INV-004 | INV-004 | MEDIUM | state_variables | Ledgers written before and after C-02 are -> REPRESENTED (7.3 row, report L4201)
33. [invariant] X-14 INV-008 | INV-008 | MEDIUM | guard_conditions | The single severity policy file decides  -> REPRESENTED (7.3 row, report L4202)
34. [invariant] X-14 INV-011 | INV-011 | MEDIUM | count_divergence | "71" is not one population and the denom -> REPRESENTED (7.3 row, report L4203)
35. [invariant] X-14 INV-012 | INV-012 | MEDIUM | count_divergence | Part of the 89 against 38 gap may be rej -> REPRESENTED (7.3 row, report L4204)
36. [invariant] X-14 INV-015 | INV-015 | MEDIUM | collection_boundaries | The expected cell has no attempt co -> REPRESENTED (7.3 row, report L4205)
37. [invariant] X-14 INV-016 | INV-016 | MEDIUM | collection_boundaries | The headline and "control found" ar -> REPRESENTED (7.3 row, report L4206)
38. [invariant] X-14 INV-017 | INV-017 | MEDIUM | collection_boundaries | M-6 may not show the gate bites: on -> REPRESENTED (7.3 row, report L4207)
39. [invariant] X-14 INV-018 | INV-018 | MEDIUM | collection_boundaries | One run per cell and one judge pass -> REPRESENTED (7.3 row, report L4208)
40. [invariant] X-14 INV-020 | INV-020 | MEDIUM | interaction_effects | "Ledger row typed blocking" is not on -> REPRESENTED (7.3 row, report L4209)
41. [invariant] X-14 INV-022 | INV-022 | MEDIUM | interaction_effects | `.gitignore:13` (`lib/`, also `build/ -> REPRESENTED (7.3 row, report L4210)
42. [invariant] X-14 INV-023 | INV-023 | MEDIUM | interaction_effects | Path-less CI `pytest -n auto --maxfai -> REPRESENTED (7.3 row, report L4211)
43. [invariant] X-14 INV-028 | INV-028 | MEDIUM | sufficiency_challenge | The 16-item ground truth has unreco -> REPRESENTED (7.3 row, report L4212)
44. [invariant] X-14 INV-029 | INV-029 | MEDIUM | sufficiency_challenge | A post-run verifier finds a bad run -> REPRESENTED (7.3 row, report L4213)
COUNT eval-acceptance-and-harness-owner/ADJUDICATION-RESULT.md: 44

### ledger-clearing-and-verdict-authority (C-02)
1. [L7] A named hybrid that the debate itself produced, built on Variant B as the selected base: * -> REPRESENTED (condensed, 6.12.9.1 row C-02, report L3512; tokens 1/1)
2. [L9] Base selection (quoted from `adversarial/base-selection.md`): "Selected Base: Variant B (e -> REPRESENTED (condensed, 6.12.9.1 row C-02, report L3512; tokens 1/2)
3. [L11] | | quant_score | qual_score | Final score | Correctness criteria MET | -> REPRESENTED (condensed, 6.12.9.1 row C-02, report L3512; tokens 0/0)
4. [L13] | Variant A | 1.000 | 24/30 = 0.800 | 0.9000 | 2 of 5 | -> REPRESENTED (condensed, 6.12.9.1 row C-02, report L3512; tokens 6/7)
5. [L14] | Variant B | 0.996 | 25/30 = 0.833 | 0.9148 | 3 of 5 | -> REPRESENTED (condensed, 6.12.9.1 row C-02, report L3512; tokens 5/7)
6. [L16] Margin 1.48 percentage points, below the 5% threshold, so the tiebreaker applied: Level 1  -> REPRESENTED (condensed, 6.12.9.1 row C-02, report L3512; tokens 11/11)
7. [L20] From `base-selection.md` and the Round 2 final positions in `debate-transcript.md`: the on -> REPRESENTED (condensed, 6.12.9.1 row C-02, report L3512; tokens 11/11)
8. [L22] - Clearing (C-001, X-003): quorum gate over distinct `block_ok`-true reviewers typing `pri -> REPRESENTED (condensed, 6.12.9.1 row C-02, report L3512; tokens 5/7)
9. [L23] - Evidence quote (C-002, X-002): optional bounded `evidence` key, recorded only with `quot -> REPRESENTED (condensed, 6.12.9.1 row C-02, report L3512; tokens 2/4)
10. [L24] - Text binding (C-003): `pending_new_sha256`; `merge_round` refuses on mismatch; `revise`  -> REPRESENTED (condensed, 6.12.9.1 row C-02, report L3512; tokens 3/4)
11. [L25] - Blocking authority (C-004, X-004): typed `blocking` stays the authority, plus a CRITICAL -> REPRESENTED (condensed, 6.12.9.1 row C-02, report L3512; tokens 4/5)
12. [L26] - Prior-line rule (C-005, X-001): a prior moves only a `resolved_check` row; the pinned te -> REPRESENTED (condensed, 6.12.9.1 row C-02, report L3512; tokens 4/4)
13. [L27] - `defer` (C-006, C-007): owner and reason required, terminal and counted open, no expiry  -> REPRESENTED (condensed, 6.12.9.1 row C-02, report L3512; tokens 5/5)
14. [L28] - Verdict surface (C-008, C-009): `brief_ids`, `verify_ids`, `held_ids` derived on read, ` -> REPRESENTED (condensed, 6.12.9.1 row C-02, report L3512; tokens 10/11)
15. [L29] - Measurement (C-010): A's three-arm replay plus B's M2 and M3. -> REPRESENTED (condensed, 6.12.9.1 row C-02, report L3512; tokens 2/3)
16. [L31] Debate tally (scoring matrix): A wins 5, B wins 5, hybrid 6, tie 1, qualified or independe -> REPRESENTED (condensed, 6.12.9.1 row C-02, report L3512; tokens 5/5)
17. [L35] Taken from the debate, not added: -> REPRESENTED (condensed, 6.12.9.1 row C-02, report L3512; tokens 0/0)
18. [L36] - C-03 sets `Q(re-review) = 1`, or the `min(Q, requested)` rule is used, so a one-reviewer -> REPRESENTED (condensed, 6.12.9.1 row C-02, report L3512; tokens 7/8)
19. [L37] - The `--resolution`-absent fallback is still OPEN: Variant A says requested = the reports -> REPRESENTED (condensed, 6.12.9.1 row C-02, report L3512; tokens 2/2)
20. [L38] - Reviewers type one `prior` line per prior blocking row at an acceptable rate. This is un -> REPRESENTED (condensed, 6.12.9.1 row C-02, report L3512; tokens 5/5)
21. [L39] - The false-affirmation residue is accepted: a `prior resolved` is a self-report, the quot -> REPRESENTED (condensed, 6.12.9.1 row C-02, report L3512; tokens 2/2)
22. [L40] - "No effect on reflect" holds for this slot only (A-004, QUALIFY); it reopens if the unif -> REPRESENTED (condensed, 6.12.9.1 row C-02, report L3512; tokens 1/1)
23. [L41] - Round-1 partial panel (D-2, one valid block of N) stays with slot C-03. -> REPRESENTED (condensed, 6.12.9.1 row C-02, report L3512; tokens 3/3)
24. [L42] - The pins asserting the old behaviour are rewritten together with the change (`tests/revi -> REPRESENTED (condensed, 6.12.9.1 row C-02, report L3512; tokens 5/5)
25. [invariant] C-02 INV-001 | INV-001 | HIGH | collection_boundaries | `need = min(Q, requested)` can be 0 i -> REPRESENTED (7.3 row, report L4003)
26. [invariant] C-02 INV-002 | INV-002 | HIGH | interaction_effects | a valid `prior open` plus a same-round  -> REPRESENTED (7.3 row, report L4004)
27. [invariant] C-02 INV-003 | INV-003 | HIGH | sufficiency_challenge | empty `brief_ids` with non-empty `ver -> REPRESENTED (7.3 row, report L4005)
28. [invariant, prose form in source] C-02 INV-004 -> REPRESENTED (7.3 row, report L4006)
29. [invariant, prose form in source] C-02 INV-005 -> REPRESENTED (7.3 row, report L4007)
30. [invariant, prose form in source] C-02 INV-006 -> REPRESENTED (7.3 row, report L4008)
31. [invariant, prose form in source] C-02 INV-007 -> REPRESENTED (7.3 row, report L4009)
32. [invariant, prose form in source] C-02 INV-008 -> REPRESENTED (7.3 row, report L4010)
33. [invariant, prose form in source] C-02 INV-009 -> REPRESENTED (7.3 row, report L4011)
34. [invariant, prose form in source] C-02 INV-010 -> REPRESENTED (7.3 row, report L4012)
35. [invariant, prose form in source] C-02 INV-011 -> REPRESENTED (7.3 row, report L4013)
36. [invariant, prose form in source] C-02 INV-013 -> REPRESENTED (7.3 row, report L4014)
37. [invariant, prose form in source] C-02 INV-014 -> REPRESENTED (7.3 row, report L4015)
38. [invariant, prose form in source] C-02 INV-016 -> REPRESENTED (7.3 row, report L4016)
39. [invariant, prose form in source] C-02 INV-018 -> REPRESENTED (7.3 row, report L4017)
40. [invariant, prose form in source] C-02 INV-020 -> REPRESENTED (7.3 row, report L4018)
COUNT ledger-clearing-and-verdict-authority/ADJUDICATION-RESULT.md: 40

### limits-repair-policy (C-06)
1. [L7] **Hybrid, with Variant B (Proposal B) as the base.** The debate's own base selection (`bas -> REPRESENTED (condensed, 6.12.9.1 row C-06, report L3516; tokens 16/16)
2. [L11] - Quantitative layer (`quant-score.py`, run twice with identical output): A 0.9598, B 0.99 -> REPRESENTED (condensed, 6.12.9.1 row C-06, report L3516; tokens 1/7)
3. [L12] - Qualitative layer (30 criteria, two position-bias passes, 4 of 60 pairs re-evaluated): A -> REPRESENTED (condensed, 6.12.9.1 row C-06, report L3516; tokens 9/10)
4. [L13] - Combined: A 0.8466, B 0.9474. "Margin: 10.08 percentage points ... above the 5% threshol -> REPRESENTED (condensed, 6.12.9.1 row C-06, report L3516; tokens 4/4)
5. [L14] - The debate's stated reasons: B scores higher on Completeness (A declines the fail-closed -> REPRESENTED (condensed, 6.12.9.1 row C-06, report L3516; tokens 9/10)
6. [L15] - The debate's caveat: "the two proposals are not what the debate converged on", so the ba -> REPRESENTED (condensed, 6.12.9.1 row C-06, report L3516; tokens 1/1)
7. [L16] - Convergence: 24 of 28 diff points agreed (85.7%) against an 80% threshold. Status BLOCKE -> REPRESENTED (condensed, 6.12.9.1 row C-06, report L3516; tokens 5/6)
8. [L20] | Points | Position A | Position B | -> REPRESENTED (condensed, 6.12.9.1 row C-06, report L3516; tokens 0/0)
9. [L22] | C-001 (claim part) and C-009: is the claim cut | Cut to 297 plus `...` with a marker, a  -> REPRESENTED (condensed, 6.12.9.1 row C-06, report L3516; tokens 8/9)
10. [L23] | C-002: which eligibility rule decides clearing and quorum | `ok`/`complete` stays the pa -> REPRESENTED (condensed, 6.12.9.1 row C-06, report L3516; tokens 6/7)
11. [L24] | C-012: provenance of a stored member that is not a byte copy | Derived copy with `origin -> REPRESENTED (condensed, 6.12.9.1 row C-06, report L3516; tokens 2/3)
12. [L28] 1. The cut of the three location fields rests on replays on single-line tasklist rows: 70  -> REPRESENTED (condensed, 6.12.9.1 row C-06, report L3516; tokens 8/8)
13. [L29] 2. The policy depends on the C-02 and C-03 `block_ok` semantics (A-004): today's bare `ok` -> REPRESENTED (condensed, 6.12.9.1 row C-06, report L3516; tokens 10/10)
14. [L30] 3. The `SKILL.md:343` sentence is reflect-only and pinned; the text adds one sentence and  -> REPRESENTED (condensed, 6.12.9.1 row C-06, report L3516; tokens 6/6)
15. [L31] 4. The dropped-blocking refusal is insurance: it fires on 3 of 264 merges without the cut  -> REPRESENTED (condensed, 6.12.9.1 row C-06, report L3516; tokens 9/9)
16. [L32] 5. Re-ask recovery is unmeasured on gateway models: E1 shows four confirmed re-asks of fiv -> REPRESENTED (condensed, 6.12.9.1 row C-06, report L3516; tokens 4/4)
17. [L33] 6. The audit-D and P273 populations differ (264/92/49/80 against 273/90/46/79) and are ade -> REPRESENTED (condensed, 6.12.9.1 row C-06, report L3516; tokens 10/10)
18. [L34] 7. The shadow-mode safety argument holds only while shadow lasts; leaving shadow requires  -> REPRESENTED (condensed, 6.12.9.1 row C-06, report L3516; tokens 1/2)
19. [L35] 8. The raise-the-limits lever is a claim-only raise to 450, a separate owner decision that -> REPRESENTED (condensed, 6.12.9.1 row C-06, report L3516; tokens 3/3)
20. [L36] 9. The kill lines K1-K5 and the pre-registered measurements are proposals; the owner may c -> REPRESENTED (condensed, 6.12.9.1 row C-06, report L3516; tokens 3/3)
21. [L69] Status `partial`; convergence score 0.8571 (24 of 28); base variant `variant-2 (Proposal B -> REPRESENTED (condensed, 6.12.9.1 row C-06, report L3516; tokens 9/11)
22. [invariant] C-06 INV-001 | INV-001 | HIGH | state_variables | The dropped-blocking refusal sees only the  -> REPRESENTED (7.3 row, report L4060)
23. [invariant] C-06 INV-017 | INV-017 | HIGH | interaction_effects | A 200-character prefix can locate at mo -> REPRESENTED (7.3 row, report L4061)
24. [invariant] C-06 INV-018 | INV-018 | HIGH | interaction_effects | In reflect, `cluster_cmd` and `verify_c -> REPRESENTED (7.3 row, report L4062)
25. [invariant] C-06 INV-023 | INV-023 | HIGH | sufficiency_challenge | Cut plus itemise plus refusal does no -> REPRESENTED (7.3 row, report L4063)
26. [invariant] C-06 INV-002 | INV-002 | MEDIUM | state_variables | The manifest `completion` value is a thir -> REPRESENTED (7.3 row, report L4064)
27. [invariant] C-06 INV-003 | INV-003 | MEDIUM | state_variables | A refused v1 merge records nothing, so th -> REPRESENTED (7.3 row, report L4065)
28. [invariant] C-06 INV-005 | INV-005 | MEDIUM | guard_conditions | `blocking_state` from the line's own `bl -> REPRESENTED (7.3 row, report L4066)
29. [invariant] C-06 INV-006 | INV-006 | MEDIUM | guard_conditions | The acknowledgement is not bound to the  -> REPRESENTED (7.3 row, report L4067)
30. [invariant] C-06 INV-007 | INV-007 | MEDIUM | guard_conditions | A dropped `prior` line (a lost veto) has -> REPRESENTED (7.3 row, report L4068)
31. [invariant] C-06 INV-008 | INV-008 | MEDIUM | guard_conditions | Both checkers return the first fault onl -> REPRESENTED (7.3 row, report L4069)
32. [invariant] C-06 INV-010 | INV-010 | MEDIUM | count_divergence | A cut can invent a reference token (`FR- -> REPRESENTED (7.3 row, report L4070)
33. [invariant] C-06 INV-016 | INV-016 | MEDIUM | collection_boundaries | A rescued line whose prefix does no -> REPRESENTED (7.3 row, report L4071)
34. [invariant] C-06 INV-019 | INV-019 | MEDIUM | interaction_effects | The unchanged Normalize text and the  -> REPRESENTED (7.3 row, report L4072)
35. [invariant] C-06 INV-024 | INV-024 | MEDIUM | sufficiency_challenge | The cut removes the v2 loss unit on -> REPRESENTED (7.3 row, report L4073)
36. [invariant] C-06 INV-025 | INV-025 | MEDIUM | sufficiency_challenge | A truncated block loses its tail wi -> REPRESENTED (7.3 row, report L4074)
37. [invariant] C-06 INV-026 | INV-026 | MEDIUM | sufficiency_challenge | After the cut the refusal fires on  -> REPRESENTED (7.3 row, report L4075)
38. [invariant] C-06 INV-004 | INV-004 | LOW | state_variables | Additive keys carry no parser or policy vers -> REPRESENTED (7.3 row, report L4076)
39. [invariant] C-06 INV-011 | INV-011 | LOW | count_divergence | `original_chars`, `kept_chars` and `repaire -> REPRESENTED (7.3 row, report L4077)
40. [invariant] C-06 INV-020 | INV-020 | LOW | interaction_effects | Two refusals can occur in sequence (quor -> REPRESENTED (7.3 row, report L4078)
41. [invariant] C-06 INV-022 | INV-022 | LOW | interaction_effects | `card_convert.py` has its own claim cut; -> REPRESENTED (7.3 row, report L4079)
COUNT limits-repair-policy/ADJUDICATION-RESULT.md: 41

### merge-verdict-policy-and-quorum (C-03)
1. [L7] **Variant A (Proposal A) as the base, merged as the hybrid the debate itself produced.** T -> REPRESENTED (condensed, 6.12.9.1 row C-03, report L3513; tokens 8/8)
2. [L11] - Quantitative layer: A 0.9680, B 0.9846 (requirement coverage A 0.9091, B 1.0000; interna -> REPRESENTED (condensed, 6.12.9.1 row C-03, report L3513; tokens 3/8)
3. [L12] - Qualitative layer (30 criteria, two position-bias passes, 2 of 60 pairs re-evaluated): A -> REPRESENTED (condensed, 6.12.9.1 row C-03, report L3513; tokens 9/11)
4. [L13] - Combined: A 0.9007, B 0.8590. "Margin: 4.17% (below the 5% threshold)". "Tiebreaker appl -> REPRESENTED (condensed, 6.12.9.1 row C-03, report L3513; tokens 6/7)
5. [L14] - The debate's stated reason: B's Correctness losses are three code-checked defects (the E -> REPRESENTED (condensed, 6.12.9.1 row C-03, report L3513; tokens 2/2)
6. [L15] - Both layers are reported: the quantitative layer favoured B, the qualitative layer favou -> REPRESENTED (condensed, 6.12.9.1 row C-03, report L3513; tokens 0/0)
7. [L16] - Convergence: 25 of 26 diff points agreed (96%) against an 80% threshold. Status BLOCKED_ -> REPRESENTED (condensed, 6.12.9.1 row C-03, report L3513; tokens 3/4)
8. [L20] 1. The default rests on fail-closed asymmetry and on the absence of any measurement, not o -> REPRESENTED (condensed, 6.12.9.1 row C-03, report L3513; tokens 2/2)
9. [L21] 2. The union is the cheap-error side only while a Reviser-rejected row has a non-human exi -> REPRESENTED (condensed, 6.12.9.1 row C-03, report L3513; tokens 4/4)
10. [L22] 3. Fail-closed is claimed only in profiles that set `degrade` (spec review). Reflect keeps -> REPRESENTED (condensed, 6.12.9.1 row C-03, report L3513; tokens 5/5)
11. [L23] 4. The quorum floor (`min(2, requested)`) is an unmeasured parameter. The refusal closes t -> REPRESENTED (condensed, 6.12.9.1 row C-03, report L3513; tokens 6/7)
12. [L24] 5. Independence (distinct served model ids, vendor) is recorded data "requested, not serve -> REPRESENTED (condensed, 6.12.9.1 row C-03, report L3513; tokens 3/3)
13. [L25] 6. The default does not satisfy FX-10 ("a weak model must not decide alone"); it prices it -> REPRESENTED (condensed, 6.12.9.1 row C-03, report L3513; tokens 2/2)
14. [L26] 7. Support and disputed flags exist only in the v2 kernel; v1 ledger rows cannot feed an r -> REPRESENTED (condensed, 6.12.9.1 row C-03, report L3513; tokens 4/4)
15. [L27] 8. Four mechanism points inside the two Round 2 hybrids were chosen on B's code evidence w -> REPRESENTED (condensed, 6.12.9.1 row C-03, report L3513; tokens 5/5)
16. [L54] Status `partial`; convergence score 0.96 (25 of 26 = 0.9615); base variant `variant-1 (Pro -> REPRESENTED (condensed, 6.12.9.1 row C-03, report L3513; tokens 6/8)
17. [invariant] C-03 INV-006 | INV-006 | HIGH | guard_conditions | The consensus text says "any complete revi -> REPRESENTED (7.3 row, report L4019)
18. [invariant] C-03 INV-007 | INV-007 | HIGH | count_divergence | `requested = max(len(resolution.reviewers) -> REPRESENTED (7.3 row, report L4020)
19. [invariant] C-03 INV-001 | INV-001 | MEDIUM | state_variables | A refusal records nothing, so refusal rat -> REPRESENTED (7.3 row, report L4021)
20. [invariant] C-03 INV-002 | INV-002 | MEDIUM | state_variables | After exit 12, `ledger verdict` shows the -> REPRESENTED (7.3 row, report L4022)
21. [invariant] C-03 INV-003 | INV-003 | MEDIUM | state_variables | Which layer owns the profile, `min_comple -> REPRESENTED (7.3 row, report L4023)
22. [invariant] C-03 INV-004 | INV-004 | MEDIUM | guard_conditions | `--resolution` is not checked for kind o -> REPRESENTED (7.3 row, report L4024)
23. [invariant] C-03 INV-005 | INV-005 | MEDIUM | guard_conditions | `complete` is not checked for distinct,  -> REPRESENTED (7.3 row, report L4025)
24. [invariant] C-03 INV-009 | INV-009 | MEDIUM | count_divergence | Between the floor and `requested` the sh -> REPRESENTED (7.3 row, report L4026)
25. [invariant] C-03 INV-010 | INV-010 | MEDIUM | collection_boundaries | The N=1..5 x five-state test matrix -> REPRESENTED (7.3 row, report L4027)
26. [invariant] C-03 INV-016 | INV-016 | MEDIUM | sufficiency_challenge | The union is deterministic but runs -> REPRESENTED (7.3 row, report L4028)
27. [invariant] C-03 INV-012 | INV-012 | LOW | interaction_effects | `defer` is the only non-quorate route to -> REPRESENTED (7.3 row, report L4029)
28. [invariant] C-03 INV-013 | INV-013 | LOW | interaction_effects | `make verify-sync` does not cover the lo -> REPRESENTED (7.3 row, report L4030)
COUNT merge-verdict-policy-and-quorum/ADJUDICATION-RESULT.md: 28

### panel-resolution-and-tier-source (C-09)
1. [L7] A named hybrid that the debate itself produced: the hybrid both advocates converged on in  -> REPRESENTED (condensed, 6.12.9.1 row C-09, report L3519; tokens 2/2)
2. [L9] Base selection, as the debate concluded it (`adversarial/base-selection.md`): **Variant B  -> REPRESENTED (condensed, 6.12.9.1 row C-09, report L3519; tokens 0/1)
3. [L10] - Quantitative (mean of the two scoring passes): A 0.9605, B 0.9533. -> REPRESENTED (condensed, 6.12.9.1 row C-09, report L3519; tokens 0/2)
4. [L11] - Qualitative after the position-bias re-evaluation (6 of 60 criterion-variant pairs disag -> REPRESENTED (condensed, 6.12.9.1 row C-09, report L3519; tokens 6/8)
5. [L12] - Combined: A 0.8969, B 0.8767; margin 0.0202, below the 5% threshold, so the tiebreaker a -> REPRESENTED (condensed, 6.12.9.1 row C-09, report L3519; tokens 15/21)
6. [L14] Contents of the hybrid (from the section 6 texts of both Round 2 files, as carried in the  -> REPRESENTED (condensed, 6.12.9.1 row C-09, report L3519; tokens 2/2)
7. [L15] 1. Ownership wording: the Coder env slots that `ccsession-models.json` names, described by -> REPRESENTED (condensed, 6.12.9.1 row C-09, report L3519; tokens 10/11)
8. [L16] 2. Guard: one test replaces `_assert_tiers_match_ccsession_slots`: the ordered ids of `ali -> REPRESENTED (condensed, 6.12.9.1 row C-09, report L3519; tokens 10/10)
9. [L17] 3. Distinctness: soft stays the default in the library and the CLI; `--strict-distinct` st -> REPRESENTED (condensed, 6.12.9.1 row C-09, report L3519; tokens 3/3)
10. [L18] 4. Order: scarcest tier first as the CLI's slot order for soft and strict, `panel.resolve` -> REPRESENTED (condensed, 6.12.9.1 row C-09, report L3519; tokens 4/4)
11. [L19] 5. Record: the CLI always writes `requested_slots` and `distinct_models`; the library outp -> REPRESENTED (condensed, 6.12.9.1 row C-09, report L3519; tokens 3/3)
12. [L20] 6. The spec loop prompt is not edited. 7. Class and vendor: one parity test, no vocabulary -> REPRESENTED (condensed, 6.12.9.1 row C-09, report L3519; tokens 17/17)
13. [L24] Both advocates conceded most of their own over-claims before Round 2 ended. Variant A's ad -> REPRESENTED (condensed, 6.12.9.1 row C-09, report L3519; tokens 17/21)
14. [L28] Each condition is one the debate itself stated or the invariant probe recorded: -> REPRESENTED (condensed, 6.12.9.1 row C-09, report L3519; tokens 0/0)
15. [L29] - The CLI-layer placement holds only while the keys and the order are applied in the CLI a -> REPRESENTED (condensed, 6.12.9.1 row C-09, report L3519; tokens 6/6)
16. [L30] - The gateway benefit (no repeated model, full panels of 4 and 7 in 1000 of 1000 runs) hol -> REPRESENTED (condensed, 6.12.9.1 row C-09, report L3519; tokens 8/9)
17. [L31] - In anthropic-only, strict gives 2 reviewers in 1000 of 1000 runs, which is a count and n -> REPRESENTED (condensed, 6.12.9.1 row C-09, report L3519; tokens 6/6)
18. [L32] - The soft default stands until Variant A's M1 (soft versus strict versus a hand-chosen re -> REPRESENTED (condensed, 6.12.9.1 row C-09, report L3519; tokens 4/4)
19. [L33] - The guard compares the package with `MODEL-TIERS.md` and the slot counts, not with the w -> REPRESENTED (condensed, 6.12.9.1 row C-09, report L3519; tokens 2/3)
20. [L34] - The ember change is one change over several files and needs the Coder slot first; the sl -> REPRESENTED (condensed, 6.12.9.1 row C-09, report L3519; tokens 3/3)
21. [L38] - C-007, the sort key of the scarcest-first order: Variant A's `len(aliases[tier].models)` -> REPRESENTED (condensed, 6.12.9.1 row C-09, report L3519; tokens 9/11)
22. [L39] - Also open and unanswered by A: B's `slot_order` key, B's library helper functions (insid -> REPRESENTED (condensed, 6.12.9.1 row C-09, report L3519; tokens 2/4)
23. [L40] - Deferred by both Round 2 hybrids: the env leg of the guard, the E2 ladder as a function  -> REPRESENTED (condensed, 6.12.9.1 row C-09, report L3519; tokens 1/1)
24. [invariant, prose form in source] C-09 INV-001 -> REPRESENTED (7.3 row, report L4116)
25. [invariant, prose form in source] C-09 INV-005 -> REPRESENTED (7.3 row, report L4117)
26. [invariant, prose form in source] C-09 INV-009 -> REPRESENTED (7.3 row, report L4118)
27. [invariant, prose form in source] C-09 INV-010 -> REPRESENTED (7.3 row, report L4119)
28. [invariant, prose form in source] C-09 INV-012 -> REPRESENTED (7.3 row, report L4120)
29. [invariant, prose form in source] C-09 INV-019 -> REPRESENTED (7.3 row, report L4121)
30. [invariant, prose form in source] C-09 INV-021 -> REPRESENTED (7.3 row, report L4122)
31. [invariant, prose form in source] C-09 INV-026 -> REPRESENTED (7.3 row, report L4123)
32. [invariant, prose form in source] C-09 INV-003 -> REPRESENTED (7.3 row, report L4124)
33. [invariant, prose form in source] C-09 INV-004 -> REPRESENTED (7.3 row, report L4125)
34. [invariant, prose form in source] C-09 INV-011 -> REPRESENTED (7.3 row, report L4126)
35. [invariant, prose form in source] C-09 INV-017 -> REPRESENTED (7.3 row, report L4127)
36. [invariant, prose form in source] C-09 INV-018 -> REPRESENTED (7.3 row, report L4128)
COUNT panel-resolution-and-tier-source/ADJUDICATION-RESULT.md: 36

### pr-review-wire-format-and-slot (C-10)
1. [L7] **A hybrid on Variant A (Proposal A) as the base: the resolution the debate named C10-R, " -> REPRESENTED (condensed, 6.12.9.1 row C-10, report L3520; tokens 13/13)
2. [L9] What C10-R is, as the debate produced it (A-R2 section 5, overall confidence 70%): the pan -> REPRESENTED (condensed, 6.12.9.1 row C-10, report L3520; tokens 17/20)
3. [L13] - Quantitative layer (re-evaluation scorer, one counting rule per metric applied to both v -> REPRESENTED (condensed, 6.12.9.1 row C-10, report L3520; tokens 3/15)
4. [L14] - Qualitative layer (30 criteria, two position-bias passes, 7 of 60 pairs re-evaluated): A -> REPRESENTED (condensed, 6.12.9.1 row C-10, report L3520; tokens 9/11)
5. [L15] - Combined: A 0.8452, B 0.8679. "Margin: 2.27% (0.0227; below the 5% threshold)". "Tiebrea -> REPRESENTED (condensed, 6.12.9.1 row C-10, report L3520; tokens 9/12)
6. [L16] - Both layers are reported: the weighted layers favour B inside the 5% tie band (the lead  -> REPRESENTED (condensed, 6.12.9.1 row C-10, report L3520; tokens 5/5)
7. [L17] - The debate's stated reasons: B conceded the slot axis (S-002 to S-004, C-004, C-005) and -> REPRESENTED (condensed, 6.12.9.1 row C-10, report L3520; tokens 11/17)
8. [L18] - Convergence: label agreement 49 of 49 (100%), content-adjusted 44 of 49 (0.90) against a -> REPRESENTED (condensed, 6.12.9.1 row C-10, report L3520; tokens 12/12)
9. [L22] 1. First release is report-only: panel findings are converted, remapped, routed and listed -> REPRESENTED (condensed, 6.12.9.1 row C-10, report L3520; tokens 5/5)
10. [L23] 2. The converter is pure (dict in and out), imports nothing from `cli/review`, `cli/reflec -> REPRESENTED (condensed, 6.12.9.1 row C-10, report L3520; tokens 7/7)
11. [L24] 3. Field rules: `body` is the representative's `claim` verbatim; `reviewer = "panel"` set  -> REPRESENTED (condensed, 6.12.9.1 row C-10, report L3520; tokens 9/9)
12. [L25] 4. Standing: `present` when every requested reviewer is `complete` (requested ids minus `c -> REPRESENTED (condensed, 6.12.9.1 row C-10, report L3520; tokens 4/5)
13. [L26] 5. Prerequisites owned elsewhere: FX-5 category parameters on `check_finding` (the core's  -> REPRESENTED (condensed, 6.12.9.1 row C-10, report L3520; tokens 8/8)
14. [L27] 6. Prose and test constraints: no new python fence in `SKILL.md` (pinned in four test file -> REPRESENTED (condensed, 6.12.9.1 row C-10, report L3520; tokens 3/3)
15. [L28] 7. On promotion, thread-less panel findings get one PR conversation follow-up and the skil -> REPRESENTED (condensed, 6.12.9.1 row C-10, report L3520; tokens 2/2)
16. [L29] 8. Per-round panel cost is unmeasured (GQ-177, OQ-18); M1 is needed by both positions befo -> REPRESENTED (condensed, 6.12.9.1 row C-10, report L3520; tokens 4/4)
17. [L31] Contested and not answered by Variant A (recorded as contested in `merged-output.md` secti -> REPRESENTED (condensed, 6.12.9.1 row C-10, report L3520; tokens 18/21)
18. [L33] What would change the resolution (A-R2 and B-R2): the converter's PR keys move toward the  -> REPRESENTED (condensed, 6.12.9.1 row C-10, report L3520; tokens 6/6)
19. [L62] Status `partial`; convergence score 0.90 (44 of 49 by content = 0.898; 49 of 49 by label); -> REPRESENTED (condensed, 6.12.9.1 row C-10, report L3520; tokens 11/13)
20. [invariant] C-10 INV-002 | INV-002 | HIGH | state_variables | Panel standing, reviewed SHA and dropped li -> REPRESENTED (7.3 row, report L4129)
21. [invariant] C-10 INV-007 | INV-007 | HIGH | count_divergence | "Requested" is defined as the dispatched c -> REPRESENTED (7.3 row, report L4130)
22. [invariant] C-10 INV-008 | INV-008 | HIGH | count_divergence | A reviewer with an empty findings block is -> REPRESENTED (7.3 row, report L4131)
23. [invariant] C-10 INV-011 | INV-011 | HIGH | collection_boundaries | The rule "present when every requeste -> REPRESENTED (7.3 row, report L4132)
24. [invariant] C-10 INV-012 | INV-012 | HIGH | collection_boundaries | AM-1 splits by category only; a same- -> REPRESENTED (7.3 row, report L4133)
25. [invariant] C-10 INV-001 | INV-001 | MEDIUM | state_variables | The standing enum has no stale value, so  -> REPRESENTED (7.3 row, report L4134)
26. [invariant] C-10 INV-003 | INV-003 | MEDIUM | state_variables | The checkout the reviewers see is not sho -> REPRESENTED (7.3 row, report L4135)
27. [invariant] C-10 INV-006 | INV-006 | MEDIUM | guard_conditions | Missing `changed_ranges` degrading to `i -> REPRESENTED (7.3 row, report L4136)
28. [invariant] C-10 INV-009 | INV-009 | MEDIUM | count_divergence | The unit of "dropped" (cluster, category -> REPRESENTED (7.3 row, report L4137)
29. [invariant] C-10 INV-010 | INV-010 | MEDIUM | count_divergence | `blocking_clusters` counts the reviewer- -> REPRESENTED (7.3 row, report L4138)
30. [invariant] C-10 INV-014 | INV-014 | MEDIUM | interaction_effects | No rule excludes panel Findings from  -> REPRESENTED (7.3 row, report L4139)
31. [invariant] C-10 INV-015 | INV-015 | MEDIUM | interaction_effects | The "not clean" wording rule covers t -> REPRESENTED (7.3 row, report L4140)
32. [invariant] C-10 INV-018 | INV-018 | MEDIUM | sufficiency_challenge | The converter's inputs (parsed bloc -> REPRESENTED (7.3 row, report L4141)
33. [invariant] C-10 INV-019 | INV-019 | MEDIUM | sufficiency_challenge | `finding_from_comment` needs a posi -> REPRESENTED (7.3 row, report L4142)
COUNT pr-review-wire-format-and-slot/ADJUDICATION-RESULT.md: 33

### process-redesign-modules (X-13)
1. [L7] **Variant A (Proposal A, Sweep-Sheet-shaped) as the base, merged as the hybrid the debate  -> REPRESENTED (condensed, 6.12.9.1 row X-13, report L3523; tokens 10/10)
2. [L9] The hybrid, as the two Round 2 advocate files state it and `merged-output.md` records it: -> REPRESENTED (condensed, 6.12.9.1 row X-13, report L3523; tokens 2/2)
3. [L10] - Built now, all optional for a module (with no cards declared the run equals today's run  -> REPRESENTED (condensed, 6.12.9.1 row X-13, report L3523; tokens 10/10)
4. [L11] - Reserved in the document only, nothing built, no schema key: slot-keyed binding (not nam -> REPRESENTED (condensed, 6.12.9.1 row X-13, report L3523; tokens 7/7)
5. [L12] - Not built: demotion, promotion, overlay, profile value, CB-2 in the core, additive item- -> REPRESENTED (condensed, 6.12.9.1 row X-13, report L3523; tokens 9/9)
6. [L13] - Placement of the row block: before the findings block in the v1 spec loop, after it in v -> REPRESENTED (condensed, 6.12.9.1 row X-13, report L3523; tokens 5/5)
7. [L17] - Quantitative layer: A 0.9370, B 0.9516 (requirement coverage 1.0000 each; internal consi -> REPRESENTED (condensed, 6.12.9.1 row X-13, report L3523; tokens 0/6)
8. [L18] - Qualitative layer (30 criteria, two position-bias passes, 7 of 60 pairs re-evaluated): A -> REPRESENTED (condensed, 6.12.9.1 row X-13, report L3523; tokens 9/11)
9. [L19] - Combined: A 0.8685, B 0.8591. "Margin: 0.94 percentage points ... below the 5% threshold -> REPRESENTED (condensed, 6.12.9.1 row X-13, report L3523; tokens 9/10)
10. [L20] - The debate's stated reason: Variant A leads on Correctness, where the debate verified fe -> REPRESENTED (condensed, 6.12.9.1 row X-13, report L3523; tokens 10/18)
11. [L21] - Both layers are reported: the quantitative layer favoured B (driven by section coverage, -> REPRESENTED (condensed, 6.12.9.1 row X-13, report L3523; tokens 3/3)
12. [L22] - Convergence: 28 of 29 diff points agreed (96.55%) against an 80% threshold (after Round  -> REPRESENTED (condensed, 6.12.9.1 row X-13, report L3523; tokens 10/12)
13. [L26] 1. The base was selected by the tiebreaker, not by a clear score margin (0.94%); the two s -> REPRESENTED (condensed, 6.12.9.1 row X-13, report L3523; tokens 1/2)
14. [L27] 2. The resolution is the hybrid of the two Round 2 advocate files, not Proposal A as writt -> REPRESENTED (condensed, 6.12.9.1 row X-13, report L3523; tokens 2/2)
15. [L28] 3. Every gate and threshold stays a design choice that no recorded run can evaluate. The g -> REPRESENTED (condensed, 6.12.9.1 row X-13, report L3523; tokens 15/15)
16. [L29] 4. The rows give a hard consequence only for an empty findings block (`findings_v2.py:291- -> REPRESENTED (condensed, 6.12.9.1 row X-13, report L3523; tokens 4/4)
17. [L30] 5. Quote exactness is measured by the advocates on recorded findings-v2 citations (31 of 3 -> REPRESENTED (condensed, 6.12.9.1 row X-13, report L3523; tokens 7/9)
18. [L31] 6. The built-now set is dormant until a module declares cards and the prose wiring exists  -> REPRESENTED (condensed, 6.12.9.1 row X-13, report L3523; tokens 6/6)
19. [L32] 7. The v1 loop has no snapshot, sidecar, cluster or precheck step anywhere (verified by ab -> REPRESENTED (condensed, 6.12.9.1 row X-13, report L3523; tokens 3/3)
20. [L33] 8. Open and not resolved by the debate: S-004 (format of the consistency and invariant pre -> REPRESENTED (condensed, 6.12.9.1 row X-13, report L3523; tokens 15/15)
21. [L64] Status `partial`; convergence score 0.9655 (28 of 29); base variant `variant-1 (Proposal A -> REPRESENTED (condensed, 6.12.9.1 row X-13, report L3523; tokens 5/7)
22. [invariant] X-13 INV-001 | INV-001 | HIGH | state_variables | `observed` is said to have one writer (the  -> REPRESENTED (7.3 row, report L4173)
23. [invariant] X-13 INV-019 | INV-019 | HIGH | sufficiency_challenge | The built-now set alone cannot make p -> REPRESENTED (7.3 row, report L4174)
24. [invariant] X-13 INV-002 | INV-002 | MEDIUM | state_variables | In reflect the file the entry point would -> REPRESENTED (7.3 row, report L4175)
25. [invariant] X-13 INV-004 | INV-004 | MEDIUM | state_variables | Step 4 parses the card (and decides the o -> REPRESENTED (7.3 row, report L4176)
26. [invariant] X-13 INV-005 | INV-005 | MEDIUM | state_variables | The entry point writes fixed paths with n -> REPRESENTED (7.3 row, report L4177)
27. [invariant] X-13 INV-006 | INV-006 | MEDIUM | guard_conditions | No row-id grammar or type rule; recorded -> REPRESENTED (7.3 row, report L4178)
28. [invariant] X-13 INV-007 | INV-007 | MEDIUM | guard_conditions | The check rules need a path and a quote  -> REPRESENTED (7.3 row, report L4179)
29. [invariant] X-13 INV-009 | INV-009 | MEDIUM | count_divergence | `assigned`, `observed`, `rows_total`, th -> REPRESENTED (7.3 row, report L4180)
30. [invariant] X-13 INV-010 | INV-010 | MEDIUM | count_divergence | Row quote boundaries disagree: the 12-ch -> REPRESENTED (7.3 row, report L4181)
31. [invariant] X-13 INV-011 | INV-011 | MEDIUM | count_divergence | The consensus does not state that compli -> REPRESENTED (7.3 row, report L4182)
32. [invariant] X-13 INV-014 | INV-014 | MEDIUM | collection_boundaries | What `assigned` holds per card, wha -> REPRESENTED (7.3 row, report L4183)
33. [invariant] X-13 INV-015 | INV-015 | MEDIUM | interaction_effects | The v1 loop edit is the rules file pl -> REPRESENTED (7.3 row, report L4184)
34. [invariant] X-13 INV-016 | INV-016 | MEDIUM | interaction_effects | In shadow mode the card body still re -> REPRESENTED (7.3 row, report L4185)
35. [invariant] X-13 INV-017 | INV-017 | MEDIUM | interaction_effects | `review-telemetry/1` reviewer records -> REPRESENTED (7.3 row, report L4186)
36. [invariant] X-13 INV-020 | INV-020 | MEDIUM | sufficiency_challenge | Advisory checks are safe but need a -> REPRESENTED (7.3 row, report L4187)
37. [invariant] X-13 INV-008 | INV-008 | LOW | guard_conditions | UNSURE counts as observed, so an all-UNSURE -> REPRESENTED (7.3 row, report L4188)
COUNT process-redesign-modules/ADJUDICATION-RESULT.md: 37

### reflect-tier2-engine-composition (C-04)
1. [L7] **Variant 1 (Proposal A) as the base, merged as the hybrid the debate itself produced.** T -> REPRESENTED (condensed, 6.12.9.1 row C-04, report L3514; tokens 15/15)
2. [L11] - Quantitative layer: Variant 1 0.9938, Variant 2 0.9889 (requirement coverage 1.0000 and  -> REPRESENTED (condensed, 6.12.9.1 row C-04, report L3514; tokens 3/10)
3. [L12] - Qualitative layer (30 criteria, two position-bias passes, 8 of 60 criterion-variant pair -> REPRESENTED (condensed, 6.12.9.1 row C-04, report L3514; tokens 10/12)
4. [L13] - Combined: Variant 1 0.9302, Variant 2 0.8611. "Margin: 6.91% (above the 5% threshold)".  -> REPRESENTED (condensed, 6.12.9.1 row C-04, report L3514; tokens 6/7)
5. [L14] - The debate's stated reason (`base-selection.md`): "The qualitative layer decides it: 26/ -> REPRESENTED (condensed, 6.12.9.1 row C-04, report L3514; tokens 14/20)
6. [L15] - "The selection is a choice of base text, not of position" (`base-selection.md`): Variant -> REPRESENTED (condensed, 6.12.9.1 row C-04, report L3514; tokens 7/7)
7. [L16] - Both layers favoured Variant 1. The debate's scoring matrix does not favour Variant 1 by -> REPRESENTED (condensed, 6.12.9.1 row C-04, report L3514; tokens 4/4)
8. [L17] - Convergence: 42 of 45 points agreed (93.33%; Round 1 was 36 of 45 = 80.00%) against an 8 -> REPRESENTED (condensed, 6.12.9.1 row C-04, report L3514; tokens 9/11)
9. [L21] 1. No capability moves now. Production Tier 2 stays engine A's ensemble (`runner.py:540` r -> REPRESENTED (condensed, 6.12.9.1 row C-04, report L3514; tokens 10/10)
10. [L22] 2. The write-side helpers make a skipped step detectable, not prevented. Fail-closed holds -> REPRESENTED (condensed, 6.12.9.1 row C-04, report L3514; tokens 2/2)
11. [L23] 3. Helper output is a comparison artifact until promoted (INV-L). Promotion is a separate  -> REPRESENTED (condensed, 6.12.9.1 row C-04, report L3514; tokens 3/3)
12. [L24] 4. CV-5 is "acknowledged non-conforming, change deferred", with release conditions: the st -> REPRESENTED (condensed, 6.12.9.1 row C-04, report L3514; tokens 3/3)
13. [L25] 5. The decided document and script fixes (D1: CV-1, CV-2, CV-3, CV-6, CV-8, CV-9) are done -> REPRESENTED (condensed, 6.12.9.1 row C-04, report L3514; tokens 10/11)
14. [L26] 6. The headless lane, its lens and its layout are unchanged, and the production T5 PASS is -> REPRESENTED (condensed, 6.12.9.1 row C-04, report L3514; tokens 2/2)
15. [L27] 7. The single-engine decision is named, not scheduled: one decision with a fork (Option 3, -> REPRESENTED (condensed, 6.12.9.1 row C-04, report L3514; tokens 2/2)
16. [L28] 8. The hybrid is an analysis, not an observation: no run has used a code-written contract, -> REPRESENTED (condensed, 6.12.9.1 row C-04, report L3514; tokens 6/8)
17. [L29] 9. Items from the Variant 2 advocate's Round 2 (R-1..R-7, E-1..E-8) were not answered by t -> REPRESENTED (condensed, 6.12.9.1 row C-04, report L3514; tokens 6/7)
18. [L30] 10. The adjudicated slots stay valid on the readings the debate fixed: "no change to `cli/ -> REPRESENTED (condensed, 6.12.9.1 row C-04, report L3514; tokens 7/7)
19. [L31] 11. Three S/C/X labels and six sub-disputes inside the hybrid are OPEN and carried two-sid -> REPRESENTED (condensed, 6.12.9.1 row C-04, report L3514; tokens 21/21)
20. [L61] Status `partial`; convergence score 0.9333 (42 of 45); base variant `Variant 1 (Proposal A -> REPRESENTED (condensed, 6.12.9.1 row C-04, report L3514; tokens 8/10)
21. [invariant] C-04 INV-001 | INV-001 | MEDIUM | state_variables | A helper writes a comparison sibling, not -> REPRESENTED (7.3 row, report L4031)
22. [invariant] C-04 INV-002 | INV-002 | MEDIUM | state_variables | `calibrated` as a helper-owned stage: `SK -> REPRESENTED (7.3 row, report L4032)
23. [invariant] C-04 INV-003 | INV-003 | MEDIUM | state_variables | Arm A and M-B cannot each be read off the -> REPRESENTED (7.3 row, report L4033)
24. [invariant] C-04 INV-005 | INV-005 | MEDIUM | guard_conditions | Name-only validation over the stable and -> REPRESENTED (7.3 row, report L4034)
25. [invariant] C-04 INV-006 | INV-006 | MEDIUM | guard_conditions | "Helper refuses", "helper advances its o -> REPRESENTED (7.3 row, report L4035)
26. [invariant] C-04 INV-007 | INV-007 | MEDIUM | guard_conditions | M-A's "every recorded run yields a lint- -> REPRESENTED (7.3 row, report L4036)
27. [invariant] C-04 INV-008 | INV-008 | MEDIUM | count_divergence | "Exactly one verdict-read key lies outsi -> REPRESENTED (7.3 row, report L4037)
28. [invariant] C-04 INV-009 | INV-009 | MEDIUM | count_divergence | D1's CV-8 and CV-1 line lists may be inc -> REPRESENTED (7.3 row, report L4038)
29. [invariant] C-04 INV-011 | INV-011 | MEDIUM | collection_boundaries | M-B cannot require zero parity fail -> REPRESENTED (7.3 row, report L4039)
30. [invariant] C-04 INV-012 | INV-012 | MEDIUM | collection_boundaries | D1's fix at `reflect_shadow_exit.py -> REPRESENTED (7.3 row, report L4040)
31. [invariant] C-04 INV-013 | INV-013 | MEDIUM | collection_boundaries | The presence rule and a refusing fi -> REPRESENTED (7.3 row, report L4041)
32. [invariant] C-04 INV-014 | INV-014 | MEDIUM | interaction_effects | The exit rule and `reflect_verdict_re -> REPRESENTED (7.3 row, report L4042)
33. [invariant] C-04 INV-015 | INV-015 | MEDIUM | interaction_effects | The card writer's target differs betw -> REPRESENTED (7.3 row, report L4043)
34. [invariant] C-04 INV-017 | INV-017 | MEDIUM | sufficiency_challenge | "Helpers that advance their own sta -> REPRESENTED (7.3 row, report L4044)
35. [invariant] C-04 INV-019 | INV-019 | MEDIUM | sufficiency_challenge | "Comparison siblings let promotion  -> REPRESENTED (7.3 row, report L4045)
36. [invariant] C-04 INV-010 | INV-010 | LOW | count_divergence | The reviewer-count value 1 and the I2 witne -> REPRESENTED (7.3 row, report L4046)
37. [invariant] C-04 INV-016 | INV-016 | LOW | interaction_effects | Widening the fence is not only bookkeepi -> REPRESENTED (7.3 row, report L4047)
COUNT reflect-tier2-engine-composition/ADJUDICATION-RESULT.md: 37

### rfqa-first-step-and-readonly-scope (C-11)
1. [L7] **Variant B (Proposal B) as the base, merged as the hybrid the debate itself produced: a l -> REPRESENTED (condensed, 6.12.9.1 row C-11, report L3521; tokens 17/18)
2. [L11] - Quantitative layer: A 0.9284, B 1.0000 (requirement coverage A 0.7692 [10 of 13], B 1.0  -> REPRESENTED (condensed, 6.12.9.1 row C-11, report L3521; tokens 3/7)
3. [L12] - Qualitative layer (30 criteria, two position-bias passes, 1 of 60 pairs re-evaluated): A -> REPRESENTED (condensed, 6.12.9.1 row C-11, report L3521; tokens 7/8)
4. [L13] - Combined: A 0.8809, B 0.9167. "Margin: 3.58% (below the 5% threshold)". "Tiebreaker appl -> REPRESENTED (condensed, 6.12.9.1 row C-11, report L3521; tokens 6/7)
5. [L14] - The debate's stated reasons: the quantitative layer favours B and the qualitative layer  -> REPRESENTED (condensed, 6.12.9.1 row C-11, report L3521; tokens 6/7)
6. [L15] - What each side gave up in Round 2: Advocate A withdrew the per-slot `lens` key, the chec -> REPRESENTED (condensed, 6.12.9.1 row C-11, report L3521; tokens 6/9)
7. [L16] - Convergence: 25 of 30 diff points agreed at text level (83.3%) against an 80% threshold; -> REPRESENTED (condensed, 6.12.9.1 row C-11, report L3521; tokens 5/7)
8. [L20] 1. The switch at `/task` steps 3-4 lands only if arm 1a passes the pre-registered rule for -> REPRESENTED (condensed, 6.12.9.1 row C-11, report L3521; tokens 4/4)
9. [L21] 2. The debate rests on structure and on one audit finding, not on measured recall: no beha -> REPRESENTED (condensed, 6.12.9.1 row C-11, report L3521; tokens 8/8)
10. [L22] 3. The only observed class-(b) event occurred at a task-file gate item of a non-standard l -> REPRESENTED (condensed, 6.12.9.1 row C-11, report L3521; tokens 4/4)
11. [L23] 4. No gate engine swap in the first change. Any later swap waits for the M-B4 anchor probe -> REPRESENTED (condensed, 6.12.9.1 row C-11, report L3521; tokens 6/6)
12. [L24] 5. Skill-embedded and task-file gate items, executing lenses and verifiers keep their agen -> REPRESENTED (condensed, 6.12.9.1 row C-11, report L3521; tokens 1/1)
13. [L25] 6. Five points carry the same label but contradicting hybrid texts and are not decided: C- -> REPRESENTED (condensed, 6.12.9.1 row C-11, report L3521; tokens 8/8)
14. [L26] 7. The default does not satisfy INV-G for the skill-embedded and task-file gate items wher -> REPRESENTED (condensed, 6.12.9.1 row C-11, report L3521; tokens 2/2)
15. [L57] Status `partial`; convergence score 0.83 (25 of 30 = 0.8333); base variant `variant-2 (Pro -> REPRESENTED (condensed, 6.12.9.1 row C-11, report L3521; tokens 11/13)
16. [invariant] C-11 INV-002 | INV-002 | HIGH | guard_conditions | The lens-identity check is undefined when  -> REPRESENTED (7.3 row, report L4143)
17. [invariant] C-11 INV-009 | INV-009 | HIGH | collection_boundaries | "The dispatched slot's path" is not u -> REPRESENTED (7.3 row, report L4144)
18. [invariant] C-11 INV-012 | INV-012 | HIGH | interaction_effects | The hash and lens-line checks sit in st -> REPRESENTED (7.3 row, report L4145)
19. [invariant] C-11 INV-015 | INV-015 | HIGH | sufficiency_challenge | The sha256 is taken over the executor -> REPRESENTED (7.3 row, report L4146)
20. [invariant] C-11 INV-016 | INV-016 | HIGH | sufficiency_challenge | Arm 0 and arm 1a differ in more than  -> REPRESENTED (7.3 row, report L4147)
21. [invariant] C-11 INV-017 | INV-017 | HIGH | sufficiency_challenge | Pre-computed counts exist in the orac -> REPRESENTED (7.3 row, report L4148)
22. [invariant] C-11 INV-001 | INV-001 | MEDIUM | state_variables | The oracle's parent permission mode, inst -> REPRESENTED (7.3 row, report L4149)
23. [invariant] C-11 INV-003 | INV-003 | MEDIUM | guard_conditions | The tree-hash scope is unspecified: excl -> REPRESENTED (7.3 row, report L4150)
24. [invariant] C-11 INV-004 | INV-004 | MEDIUM | guard_conditions | The subset guard checks the source file; -> REPRESENTED (7.3 row, report L4151)
25. [invariant] C-11 INV-007 | INV-007 | MEDIUM | count_divergence | "The standard eight lens dimensions" doe -> REPRESENTED (7.3 row, report L4152)
26. [invariant] C-11 INV-008 | INV-008 | MEDIUM | count_divergence | The audit misses nested spawns (a lens t -> REPRESENTED (7.3 row, report L4153)
27. [invariant] C-11 INV-010 | INV-010 | MEDIUM | collection_boundaries | The Confidence Gate formula is unde -> REPRESENTED (7.3 row, report L4154)
28. [invariant] C-11 INV-013 | INV-013 | MEDIUM | interaction_effects | `test_c_s1_s3_copied_verbatim` iterat -> REPRESENTED (7.3 row, report L4155)
29. [invariant] C-11 INV-014 | INV-014 | MEDIUM | interaction_effects | The `rf-qa.md` body and the installed -> REPRESENTED (7.3 row, report L4156)
30. [invariant] C-11 INV-018 | INV-018 | MEDIUM | sufficiency_challenge | The conditional switch does not nam -> REPRESENTED (7.3 row, report L4157)
31. [invariant] C-11 INV-006 | INV-006 | LOW | guard_conditions | The reflect-reviewer allowlist refused 7 ca -> REPRESENTED (7.3 row, report L4158)
COUNT rfqa-first-step-and-readonly-scope/ADJUDICATION-RESULT.md: 31

### run-record-and-served-model-capture (C-08)
1. [L7] **Variant 1 (Proposal A) as the base, merged as the hybrid the debate itself produced.** T -> REPRESENTED (condensed, 6.12.9.1 row C-08, report L3518; tokens 11/11)
2. [L9] The hybrid the debate produced (merged file sections 1 and 2): per-agent observation, refu -> REPRESENTED (condensed, 6.12.9.1 row C-08, report L3518; tokens 19/20)
3. [L13] - Quantitative layer: Variant 1 0.9605, Variant 2 0.9579 (requirement coverage 0.9667 each -> REPRESENTED (condensed, 6.12.9.1 row C-08, report L3518; tokens 3/9)
4. [L14] - Qualitative layer (30 criteria, two position-bias passes, 8 of 60 pairs re-evaluated): V -> REPRESENTED (condensed, 6.12.9.1 row C-08, report L3518; tokens 8/9)
5. [L15] - Combined: Variant 1 0.8969, Variant 2 0.8956. "Margin: 0.0013 (0.13%, below the 5% thres -> REPRESENTED (condensed, 6.12.9.1 row C-08, report L3518; tokens 7/9)
6. [L16] - The debate's stated reason: both advocates named Proposal A's per-run events file as the -> REPRESENTED (condensed, 6.12.9.1 row C-08, report L3518; tokens 7/11)
7. [L17] - Convergence: 28 of 31 diff points agreed (0.9032) against an 80% threshold. Status BLOCK -> REPRESENTED (condensed, 6.12.9.1 row C-08, report L3518; tokens 3/4)
8. [L21] 1. Every served-id and usage field depends on the transcript adapter, which is an unverifi -> REPRESENTED (condensed, 6.12.9.1 row C-08, report L3518; tokens 8/8)
9. [L22] 2. M1(c) as written (per-agent `tokens_out` plus orchestrator snapshot equals run-level `m -> REPRESENTED (condensed, 6.12.9.1 row C-08, report L3518; tokens 10/10)
10. [L23] 3. The non-reviewer and orchestrator rows are gated by M3 (reviewer-only tokens within 10  -> REPRESENTED (condensed, 6.12.9.1 row C-08, report L3518; tokens 6/6)
11. [L24] 4. Refusal rows exist only when `review merge` is run with `--events`, only for the causes -> REPRESENTED (condensed, 6.12.9.1 row C-08, report L3518; tokens 7/10)
12. [L25] 5. The memory writer move and study switch are deferred; trigger: an observed lost update, -> REPRESENTED (condensed, 6.12.9.1 row C-08, report L3518; tokens 4/4)
13. [L26] 6. All SKILL edits stay inside `### 4.3a`, add no `src/superclaude` string, and carry one  -> REPRESENTED (condensed, 6.12.9.1 row C-08, report L3518; tokens 4/4)
14. [L27] 7. Points the two advocates did not settle and the merged file marks OPEN, with each side  -> REPRESENTED (condensed, 6.12.9.1 row C-08, report L3518; tokens 13/15)
15. [L28] 8. Advocate B's Round 2 corrections to A's 15-item resolution (telemetry lock dropped, app -> REPRESENTED (condensed, 6.12.9.1 row C-08, report L3518; tokens 7/8)
16. [L29] 9. The 28 of 31 count is by label: C-001 and X-006 are label splits with converged substan -> REPRESENTED (condensed, 6.12.9.1 row C-08, report L3518; tokens 6/6)
17. [L30] 10. Merge-executor judgments recorded in `merge-log.md` (none changes a plan decision): th -> REPRESENTED (condensed, 6.12.9.1 row C-08, report L3518; tokens 7/7)
18. [L65] Status `partial`; convergence score 0.90 (28 of 31 = 0.9032); base variant `variant-1 (Pro -> REPRESENTED (condensed, 6.12.9.1 row C-08, report L3518; tokens 10/12)
19. [invariant] C-08 INV-001 | INV-001 | HIGH | state_variables | A torn final line from a killed writer is n -> REPRESENTED (7.3 row, report L4096)
20. [invariant] C-08 INV-002 | INV-002 | HIGH | state_variables | `ingest` is called idempotent because "a fi -> REPRESENTED (7.3 row, report L4097)
21. [invariant] C-08 INV-005 | INV-005 | HIGH | guard_conditions | The interactive layout stores sub-agent me -> REPRESENTED (7.3 row, report L4098)
22. [invariant] C-08 INV-006 | INV-006 | HIGH | guard_conditions | Neither join works as written: the Agent-c -> REPRESENTED (7.3 row, report L4099)
23. [invariant] C-08 INV-009 | INV-009 | HIGH | count_divergence | Per-event usage summation over-counts 2.0x -> REPRESENTED (7.3 row, report L4100)
24. [invariant] C-08 INV-010 | INV-010 | HIGH | count_divergence | M1(c) measured at 0 of 15 runs within 2 pe -> REPRESENTED (7.3 row, report L4101)
25. [invariant] C-08 INV-011 | INV-011 | HIGH | count_divergence | A non-Anthropic sidechain reports `output_ -> REPRESENTED (7.3 row, report L4102)
26. [invariant] C-08 INV-013 | INV-013 | HIGH | collection_boundaries | `record_absent` is printed by `export -> REPRESENTED (7.3 row, report L4103)
27. [invariant] C-08 INV-016 | INV-016 | HIGH | interaction_effects | The `refused` row composes with C-03's  -> REPRESENTED (7.3 row, report L4104)
28. [invariant] C-08 INV-017 | INV-017 | HIGH | interaction_effects | SKILL step 9 (identity) precedes step 1 -> REPRESENTED (7.3 row, report L4105)
29. [invariant] C-08 INV-020 | INV-020 | HIGH | sufficiency_challenge | The hybrid alone does not close the A -> REPRESENTED (7.3 row, report L4106)
30. [invariant] C-08 INV-021 | INV-021 | HIGH | sufficiency_challenge | The hybrid alone does not close C-03  -> REPRESENTED (7.3 row, report L4107)
31. [invariant] C-08 INV-022 | INV-022 | HIGH | sufficiency_challenge | The hybrid alone does not close cost  -> REPRESENTED (7.3 row, report L4108)
32. [invariant] C-08 INV-003 | INV-003 | MEDIUM | state_variables | The last `orchestrator_snapshot` by event -> REPRESENTED (7.3 row, report L4109)
33. [invariant] C-08 INV-004 | INV-004 | MEDIUM | state_variables | One run is assumed to be one transcript f -> REPRESENTED (7.3 row, report L4110)
34. [invariant] C-08 INV-007 | INV-007 | MEDIUM | guard_conditions | `init` has no manifest yet for the lock; -> REPRESENTED (7.3 row, report L4111)
35. [invariant] C-08 INV-008 | INV-008 | MEDIUM | guard_conditions | What `export` does when `strict` refuses -> REPRESENTED (7.3 row, report L4112)
36. [invariant] C-08 INV-012 | INV-012 | MEDIUM | count_divergence | The events-side `attempt` and the manife -> REPRESENTED (7.3 row, report L4113)
37. [invariant] C-08 INV-015 | INV-015 | MEDIUM | collection_boundaries | A served id is not normalised (`qwe -> REPRESENTED (7.3 row, report L4114)
38. [invariant] C-08 INV-018 | INV-018 | MEDIUM | interaction_effects | Deterministic `record_id` makes `expo -> REPRESENTED (7.3 row, report L4115)
COUNT run-record-and-served-model-capture/ADJUDICATION-RESULT.md: 38

### tasklist-medium-and-fidelity-vocab (X-15)
1. [L7] **Variant B (Proposal B) as the base, merged as the hybrid the debate itself produced.** T -> REPRESENTED (condensed, 6.12.9.1 row X-15, report L3525; tokens 4/4)
2. [L9] Neither proposal won as written. After two rounds the advocates agreed on 32 of 37 diff po -> REPRESENTED (condensed, 6.12.9.1 row X-15, report L3525; tokens 5/6)
3. [L13] - Quantitative layer: A 0.9943, B 0.9328 (requirement coverage A 1.0000, B 0.9167; interna -> REPRESENTED (condensed, 6.12.9.1 row X-15, report L3525; tokens 1/8)
4. [L14] - Qualitative layer (30 criteria, two position-bias passes, 7 of 60 pairs re-evaluated): A -> REPRESENTED (condensed, 6.12.9.1 row X-15, report L3525; tokens 8/10)
5. [L15] - Combined: A 0.9138, B 0.8664. "Margin: 4.74% (below the 5% threshold)". "Tiebreaker appl -> REPRESENTED (condensed, 6.12.9.1 row X-15, report L3525; tokens 7/8)
6. [L16] - Both layers are reported: the quantitative layer and the qualitative layer both favoured -> REPRESENTED (condensed, 6.12.9.1 row X-15, report L3525; tokens 0/0)
7. [L17] - The debate's stated reason: on the points that carry correctness and risk weight Advocat -> REPRESENTED (condensed, 6.12.9.1 row X-15, report L3525; tokens 6/8)
8. [L18] - Convergence: 32 of 37 diff points agreed (86.5%) against an 80% threshold. Status BLOCKE -> REPRESENTED (condensed, 6.12.9.1 row X-15, report L3525; tokens 3/4)
9. [L19] - Matrix tally: Variant A 4 points, Variant B 12, Hybrid 6, Neither 4, Unresolved 5 (C-001 -> REPRESENTED (condensed, 6.12.9.1 row X-15, report L3525; tokens 9/9)
10. [L23] 1. The choice between H+ and A+ rests on measurements that have not been run (F1: blind gr -> REPRESENTED (condensed, 6.12.9.1 row X-15, report L3525; tokens 6/6)
11. [L24] 2. The basis is the consequence test of `pragmatic.md:225` and `:231` applied by analogy.  -> REPRESENTED (condensed, 6.12.9.1 row X-15, report L3525; tokens 5/5)
12. [L25] 3. The shared core gets nothing: no `Medium` token, no new field, no parse-edge hook. The  -> REPRESENTED (condensed, 6.12.9.1 row X-15, report L3525; tokens 7/7)
13. [L26] 4. The fidelity prompt stays outside the core while no core code consumes the vocabulary ( -> REPRESENTED (condensed, 6.12.9.1 row X-15, report L3525; tokens 2/2)
14. [L27] 5. The only data about what the skill's Medium finds is two archived reports (six findings -> REPRESENTED (condensed, 6.12.9.1 row X-15, report L3525; tokens 2/2)
15. [L28] 6. The C-02 CRITICAL floor covers High (CRITICAL) and not Medium (MAJOR); under H+ a revie -> REPRESENTED (condensed, 6.12.9.1 row X-15, report L3525; tokens 5/5)
16. [L29] 7. Under H+ the skill and the CLI disagree on one class (a criterion dropped or weakened:  -> REPRESENTED (condensed, 6.12.9.1 row X-15, report L3525; tokens 2/3)
17. [L30] 8. Pin inventory: the pinned phrase "the unresolved High or Medium HALT resolves as blocke -> REPRESENTED (condensed, 6.12.9.1 row X-15, report L3525; tokens 6/6)
18. [L60] Status `partial`; convergence score 0.86 (32 of 37 = 0.8649); base variant `variant-2 (Pro -> REPRESENTED (condensed, 6.12.9.1 row X-15, report L3525; tokens 11/13)
19. [invariant] X-15 INV-017 | INV-017 | HIGH | sufficiency_challenge | "Nothing loosens before measurement,  -> REPRESENTED (7.3 row, report L4214)
20. [invariant] X-15 INV-018 | INV-018 | HIGH | sufficiency_challenge | "Grading block + tie-break-up + dedup -> REPRESENTED (7.3 row, report L4215)
21. [invariant] X-15 INV-001 | INV-001 | MEDIUM | state_variables | `ValidationReport.md` is written once fro -> REPRESENTED (7.3 row, report L4216)
22. [invariant] X-15 INV-003 | INV-003 | MEDIUM | guard_conditions | No CRITICAL floor exists in code yet and -> REPRESENTED (7.3 row, report L4217)
23. [invariant] X-15 INV-004 | INV-004 | MEDIUM | guard_conditions | SK:1410 leaves "the same issue on the sa -> REPRESENTED (7.3 row, report L4218)
24. [invariant] X-15 INV-005 | INV-005 | MEDIUM | guard_conditions | The containment test T2(a) and (b) canno -> REPRESENTED (7.3 row, report L4219)
25. [invariant] X-15 INV-007 | INV-007 | MEDIUM | count_divergence | `F_k` counts post-dedup findings while t -> REPRESENTED (7.3 row, report L4220)
26. [invariant] X-15 INV-008 | INV-008 | MEDIUM | count_divergence | SK:1703, :1705, :1716, :1766 and the tot -> REPRESENTED (7.3 row, report L4221)
27. [invariant] X-15 INV-010 | INV-010 | MEDIUM | collection_boundaries | (A+ only) the clean template has a  -> REPRESENTED (7.3 row, report L4222)
28. [invariant] X-15 INV-011 | INV-011 | MEDIUM | collection_boundaries | F1 to F3 rest on two archived bundl -> REPRESENTED (7.3 row, report L4223)
29. [invariant] X-15 INV-013 | INV-013 | MEDIUM | interaction_effects | Tie-break-up enlarges the blocking se -> REPRESENTED (7.3 row, report L4224)
30. [invariant] X-15 INV-014 | INV-014 | MEDIUM | interaction_effects | H+ keeps SK:1421-1422 MEDIUM while th -> REPRESENTED (7.3 row, report L4225)
31. [invariant] X-15 INV-019 | INV-019 | MEDIUM | sufficiency_challenge | Eleven filters sit between a Stage  -> REPRESENTED (7.3 row, report L4226)
32. [invariant] X-15 INV-020 | INV-020 | MEDIUM | sufficiency_challenge | F1 cannot fail H+ by construction a -> REPRESENTED (7.3 row, report L4227)
33. [invariant] X-15 INV-002 | INV-002 | LOW | state_variables | The byte-equal fixture guard skips when the  -> REPRESENTED (7.3 row, report L4228)
34. [invariant] X-15 INV-009 | INV-009 | LOW | count_divergence | The "76 lines in 10 files" against "88 line -> REPRESENTED (7.3 row, report L4229)
35. [invariant] X-15 INV-012 | INV-012 | LOW | collection_boundaries | A one-task phase has one grader, so de -> REPRESENTED (7.3 row, report L4230)
COUNT tasklist-medium-and-fidelity-vocab/ADJUDICATION-RESULT.md: 35

## research/19-value-ledger-handoffs.md (moved to this agent; one entry per ledger row)
Method: every ledger row is matched to its row in Appendix A (synthesis/synth-08-value-inventory.md, the 5,950-row inventory that Section 8.1.2 and Appendix A name; report 8.1.0 reconciliation row 'Ledger 19' L4252) by row id as locator AND by meaning: the Statement and Kind cells are compared character for character, and the Destination cell is compared with the ledger's. Result: 886 of 886 rows present, 886 of 886 statements identical, 828 destinations identical, 58 destinations moved to DROP with a recorded 'DROP[duplicate]: duplicate of <kept row>; was <old destination>' reason (all 58 targets exist in Appendix A). Each entry: n. ledger id [ledger line, Appendix A line] short statement | ledger destination -> inventory destination.
1. VL-19-001 [ledger L12, App.A L3646] Run-2 hand-off is `.dev/eval-workspaces/tasklist-review-panel/HANDOFF-... | same destination KNOWLEDGE -> REPRESENTED
2. VL-19-002 [ledger L13, App.A L3647] Run-1 hand-off is `HANDOFF-review-panel-unification.md`, 315 lines, ad... | same destination KNOWLEDGE -> REPRESENTED
3. VL-19-003 [ledger L14, App.A L3648] E2's own `HANDOFF-run1-vs-run2.md` (67 lines) gives the verdict "Use r... | same destination KNOWLEDGE -> REPRESENTED
4. VL-19-004 [ledger L15, App.A L1806] The E2 comparison recommends re-checking run-2 D1-D13 and P1-P7 agains... | same destination EVAL -> REPRESENTED
5. VL-19-005 [ledger L16, App.A L1807] Raw notes behind both hand-offs live in `handoff-notes/run1/{code-merg... | same destination EVAL -> REPRESENTED
6. VL-19-006 [ledger L17, App.A L3649] Later E2 commits not covered by the slice: tip 6c0984326 untracks 96 r... | same destination KNOWLEDGE -> REPRESENTED
7. VL-19-007 [ledger L18, App.A L3650] Run-2 was written by one writer agent from three fresh notes plus own ... | same destination KNOWLEDGE -> REPRESENTED
8. VL-19-008 [ledger L19, App.A L3651] All agents were pinned to Opus 5.5 and the orchestrator was Tier 1a Op... | same destination KNOWLEDGE -> REPRESENTED
9. VL-19-009 [ledger L20, App.A L3652] Run-2 header date is 2026-11-13 and its body uses "2026-11-14" to mean... | same destination KNOWLEDGE -> REPRESENTED
10. VL-19-010 [ledger L21, App.A L3653] Run-2 was written in worktree `eval-tasklist-review-panel` at HEAD 4a2... | same destination KNOWLEDGE -> REPRESENTED
11. VL-19-011 [ledger L22, App.A L3654] The E2 branch is 11 commits behind origin/master (run-2 and re-check a... | same destination KNOWLEDGE -> REPRESENTED
12. VL-19-012 [ledger L23, App.A L3655] #519 changed 40 files, +8,026/-15, under `src/superclaude/cli/review` ... | same destination KNOWLEDGE -> REPRESENTED
13. VL-19-013 [ledger L24, App.A L3656] Structure map of the run-2 hand-off: header and terms, 1 inventory, 2 ... | same destination KNOWLEDGE -> REPRESENTED
14. VL-19-014 [ledger L25, App.A L3657] Run-2 self-declared limits: single-author spot-verified draft; reflect... | same destination KNOWLEDGE -> REPRESENTED
15. VL-19-015 [ledger L26, App.A L4066] F1: run-1 is 315 lines, run-2 543 lines (cmp says 544) | same destination DROP -> REPRESENTED
16. VL-19-016 [ledger L27, App.A L3658] F2: run-1 was written by the orchestrator with whole session context p... | same destination KNOWLEDGE -> REPRESENTED
17. VL-19-017 [ledger L28, App.A L4067] F3: both hand-offs carry an honest-scope note (no task-file machinery,... | same destination DROP -> REPRESENTED
18. VL-19-018 [ledger L29, App.A L3659] F4: run-1 has a section-0 one-paragraph summary; run-2 has none and en... | same destination KNOWLEDGE -> REPRESENTED
19. VL-19-019 [ledger L30, App.A L3660] F5: status vocabulary differs (run-1 C-P / UNCOM / LOCAL-ONLY and a G/... | same destination KNOWLEDGE -> REPRESENTED
20. VL-19-020 [ledger L31, App.A L3661] F6: citation style differs (run-1 `RV/<file>:n`, `CR:n`, `PR:n`; run-2... | same destination KNOWLEDGE -> REPRESENTED
21. VL-19-021 [ledger L32, App.A L3662] F7: run-1 never mentions that master moved; run-2 pins code to base ec... | same destination KNOWLEDGE -> REPRESENTED
22. VL-19-022 [ledger L33, App.A L3663] F8: run-1 lists files read (COMBO-REPORT lines 1-12, 47-116, 286-435 o... | same destination KNOWLEDGE -> REPRESENTED
23. VL-19-023 [ledger L34, App.A L1808] F9: run-1 has a 10-row model-by-role table (run1:84-97); run-2 has no ... | same destination EVAL -> REPRESENTED
24. VL-19-024 [ledger L35, App.A L4068] F10: run-2 uses "2026-11-14" 9 times on 8 lines meaning 2026-11-13 | same destination DROP -> REPRESENTED
25. VL-19-025 [ledger L36, App.A L4069] F11: E2's comparison verdict "Use run 2 as the main hand-off" | same destination DROP -> REPRESENTED
26. VL-19-026 [ledger L37, App.A L4070] C1 numbers: master moved, #519 plus #518 changed 40 files, +8,026 unde... | same destination DROP -> REPRESENTED
27. VL-19-027 [ledger L38, App.A L4071] C1 attribution: only d2d8a2d16 (#519) touches `src/superclaude/cli/rev... | moved KNOWLEDGE -> DROP (recorded: DROP[duplicate]: duplicate of DR-045; was KNOWLEDGE: the def) -> REPRESENTED
28. VL-19-028 [ledger L39, App.A L1283] C2 (run-2 correct): tasklist review runs today inside reflect; `sc-wor... | same destination MODULE-tasklist -> REPRESENTED
29. VL-19-029 [ledger L40, App.A L4072] C2 (run-1 wrong): run-1 D14 claim "No tasklist review step exists in `... | same destination DROP -> REPRESENTED
30. VL-19-030 [ledger L41, App.A L1809] C3: only audits A and D hold `summary.md`; audits B, C, E, F hold scri... | same destination EVAL -> REPRESENTED
31. VL-19-031 [ledger L42, App.A L3175] C4: helper scripts `snap.py`, `drift-b3.py`, `rlog-r3.sh` reference a ... | same destination HARNESS -> REPRESENTED
32. VL-19-032 [ledger L43, App.A L3176] C5/H2: in `run-reviewer.sh` the `expected_model` meta is overwritten w... | same destination HARNESS -> REPRESENTED
33. VL-19-033 [ledger L44, App.A L3177] C5/H3: in `run-reviewer.sh` the attempt counter is reset to 0 on fallb... | same destination HARNESS -> REPRESENTED
34. VL-19-034 [ledger L45, App.A L3178] C5/H4: `BLOCK_OK` in `run-reviewer.sh` only greps the fence line (`:57... | same destination HARNESS -> REPRESENTED
35. VL-19-035 [ledger L46, App.A L4073] C6: raw-file count 3,041 untracked (1,380 + 1,352 + 309) conflicts wit... | moved HARNESS -> DROP (recorded: DROP[duplicate]: duplicate of DR-051; was HARNESS: the defec) -> REPRESENTED
36. VL-19-036 [ledger L47, App.A L3179] C7/H10: analysis scripts read or exec `/tmp` copies (`final-table.py:2... | same destination HARNESS -> REPRESENTED
37. VL-19-037 [ledger L48, App.A L1810] C8: test count differs, run-1 "299 passed in 7.1 s" with 5 skills file... | same destination EVAL -> REPRESENTED
38. VL-19-038 [ledger L49, App.A L1811] C8 at HEAD: the same 13 test files collect 309 tests (cli 9 to 13, liv... | same destination EVAL -> REPRESENTED
39. VL-19-039 [ledger L50, App.A L3664] C9: run-2 splits run-1's single D1 "over-length drop" into D2 (partial... | same destination KNOWLEDGE -> REPRESENTED
40. VL-19-040 [ledger L51, App.A L4074] C10: the brief-versus-parser conflict list grows from run-1 D8 (no sou... | same destination DROP -> REPRESENTED
41. VL-19-041 [ledger L52, App.A L4075] C11/P3: model `muse-ember` is absent from the tier data (no `muse-embe... | moved CORE -> DROP (recorded: DROP[duplicate]: duplicate of DR-016; was CORE: the defect r) -> REPRESENTED
42. VL-19-042 [ledger L53, App.A L4076] C11/P4: Qwen3.8-max and glm-5.3 are still listed in the tier lists (5 ... | moved CORE -> DROP (recorded: DROP[duplicate]: duplicate of DR-017; was CORE: the defect r) -> REPRESENTED
43. VL-19-043 [ledger L54, App.A L4077] C11/P2: the gateway `launch` map in `review-tiers.default.json` is emp... | moved CORE -> DROP (recorded: DROP[duplicate]: duplicate of DR-015; was CORE: the defect r) -> REPRESENTED
44. VL-19-044 [ledger L55, App.A L49] C12/T1: `append_record` has no automatic product caller (only the manu... | same destination CORE -> REPRESENTED
45. VL-19-045 [ledger L56, App.A L4078] C12/T2: telemetry strata are hard-coded to `("sonnet","haiku")` (`tele... | moved CORE -> DROP (recorded: DROP[duplicate]: duplicate of DR-022; was CORE: the defect r) -> REPRESENTED
46. VL-19-046 [ledger L57, App.A L4079] C13/D7: `refs_norm` drops task-id refs; a direct call with `['T01.02',... | moved CORE -> DROP (recorded: DROP[duplicate]: duplicate of DR-007; was CORE: the defect r) -> REPRESENTED
47. VL-19-047 [ledger L58, App.A L50] C14/P5: the panel environment is guessed from `SUPERCLAUDE_REVIEW_ENV`... | same destination CORE -> REPRESENTED
48. VL-19-048 [ledger L59, App.A L4080] C15: per-model drop counts (luna 30, ember 33, wonder 14, glm 7, haiku... | moved EVAL -> DROP (recorded: DROP[duplicate]: duplicate of DR-046; was EVAL: the defect r) -> REPRESENTED
49. VL-19-049 [ledger L60, App.A L4081] L1 (run-1 D13): `lint_cmd` and `estimate_cmd` are registered in `RV/__... | moved CORE -> DROP (recorded: DROP[duplicate]: duplicate of DR-042; was CORE: the defect r) -> REPRESENTED
50. VL-19-050 [ledger L61, App.A L1627] L2 (run-1 D14 second half, Q7): the review-ledger skill, `spec-panel-l... | same destination MODULE-spec -> REPRESENTED
51. VL-19-051 [ledger L62, App.A L4082] L3a (run-1 D16): `ledger.py:114` checks only `n == len(rounds)+1`, so ... | moved CORE -> DROP (recorded: DROP[duplicate]: duplicate of DR-043; was CORE: the defect r) -> REPRESENTED
52. VL-19-052 [ledger L63, App.A L4083] L3b: `--cap` is ignored on an existing ledger (`merge_cmd.py:101-104` ... | moved CORE -> DROP (recorded: DROP[duplicate]: duplicate of DR-043; was CORE: the defect r) -> REPRESENTED
53. VL-19-053 [ledger L64, App.A L4084] L3c: verify-only rounds are enforced by the prompt only, not by code | moved CORE -> DROP (recorded: DROP[duplicate]: duplicate of DR-043; was CORE: the defect r) -> REPRESENTED
54. VL-19-054 [ledger L65, App.A L51] L4 (run-1 D9): the brief says "Grade it Medium when ... the finding is... | same destination CORE -> REPRESENTED
55. VL-19-055 [ledger L66, App.A L1812] L5: pilot decision-rule outcome: arms A 2/16, B 3/16, C 4/16 found; bl... | same destination EVAL -> REPRESENTED
56. VL-19-056 [ledger L67, App.A L52] L6 (run-1 requirement 1): the panel must accept both finding shapes or... | same destination CORE -> REPRESENTED
57. VL-19-057 [ledger L68, App.A L53] L7 (run-1 requirement 9): reviewer isolation (fresh context, sandbox t... | same destination CORE -> REPRESENTED
58. VL-19-058 [ledger L69, App.A L1001] L8/Q5: is reflect's rotation table (sonnet, haiku, qwen/kimi/deepseek ... | same destination MODULE-reflect -> REPRESENTED
59. VL-19-059 [ledger L70, App.A L1628] L8/Q7: status of the stoprule experiment; run-2 dropped the question | same destination MODULE-spec -> REPRESENTED
60. VL-19-060 [ledger L71, App.A L54] L8/Q3: does calibrator disjointness conflict with `distinct_across_slo... | same destination CORE -> REPRESENTED
61. VL-19-061 [ledger L72, App.A L3180] L9a: run-1 section 5.4 file layout of per-run and per-judge outputs; r... | same destination HARNESS -> REPRESENTED
62. VL-19-062 [ledger L73, App.A L3181] L9b: run-1 1.3 list of `/tmp` scripts NOT copied (`checks-gate8.sh`, `... | same destination HARNESS -> REPRESENTED
63. VL-19-063 [ledger L74, App.A L1813] L10-A: audit A found 2 b4-muse-luna2 "wonder" runs served terra, and g... | same destination EVAL -> REPRESENTED
64. VL-19-064 [ledger L75, App.A L1814] L10-C: audit C found no run read ground truth | same destination EVAL -> REPRESENTED
65. VL-19-065 [ledger L76, App.A L1815] L10-E: audit E found 12/12 and 19/19 matches with borderline GT8 (CR:2... | same destination EVAL -> REPRESENTED
66. VL-19-066 [ledger L77, App.A L1816] L11: no result validates the packaged `@default` (4 reviewers t1b/t2/t... | same destination EVAL -> REPRESENTED
67. VL-19-067 [ledger L78, App.A L4085] L12 (run-1 D11 effect): anthropic-only `@live7` gives 6 identical haik... | same destination DROP -> REPRESENTED
68. VL-19-068 [ledger L79, App.A L3665] 3.4 inventory of what run-2 adds over run-1: definitions (9 terms), re... | same destination KNOWLEDGE -> REPRESENTED
69. VL-19-069 [ledger L80, App.A L1817] Crosswalk D1 over-length drop: run-2 adds bad severity (3) and bad ref... | same destination EVAL -> REPRESENTED
70. VL-19-070 [ledger L81, App.A L4086] Crosswalk run-1 D2 "dropped re-report clears a blocker" maps to run-2 ... | same destination DROP -> REPRESENTED
71. VL-19-071 [ledger L82, App.A L4087] Crosswalk run-1 D3 "merge passes with one valid reviewer" is reframed ... | same destination DROP -> REPRESENTED
72. VL-19-072 [ledger L83, App.A L4088] Crosswalk run-1 D4 "one blocking flag decides" maps to run-2 D8 (+ B-7... | same destination DROP -> REPRESENTED
73. VL-19-073 [ledger L84, App.A L1818] Crosswalk run-1 D5 "missing anchors kept silently" maps to run-2 D6, w... | same destination EVAL -> REPRESENTED
74. VL-19-074 [ledger L85, App.A L1819] Crosswalk run-1 D6 "clustering over/under-merge" maps to run-2 D4 (cha... | same destination EVAL -> REPRESENTED
75. VL-19-075 [ledger L86, App.A L4089] Crosswalk run-1 D7 ref regex maps to run-2 D7, now directly verified | same destination DROP -> REPRESENTED
76. VL-19-076 [ledger L87, App.A L4090] Crosswalk run-1 D8 "brief has no source" maps to run-2 B-1 (+ R14, DO1... | same destination DROP -> REPRESENTED
77. VL-19-077 [ledger L88, App.A L4091] Crosswalk run-1 D9 "missing-requirement Medium vs blocking" is only pa... | same destination DROP -> REPRESENTED
78. VL-19-078 [ledger L89, App.A L4092] Crosswalk run-1 D10 `unpassable-ac` label maps to run-2 B-6 and is FIX... | same destination DROP -> REPRESENTED
79. VL-19-079 [ledger L90, App.A L4093] Crosswalk run-1 D11 `distinct_across_slots` duplicates maps to run-2 P... | same destination DROP -> REPRESENTED
80. VL-19-080 [ledger L91, App.A L4094] Crosswalk run-1 D12 "env keys on `$T3Model01`" maps to run-2 P5 | same destination DROP -> REPRESENTED
81. VL-19-081 [ledger L92, App.A L4095] Crosswalk run-1 D13 lint/estimate missing has no run-2 counterpart | same destination DROP -> REPRESENTED
82. VL-19-082 [ledger L93, App.A L4096] Crosswalk run-1 D14 "no tasklist review step / experiment copies" has ... | same destination DROP -> REPRESENTED
83. VL-19-083 [ledger L94, App.A L4097] Crosswalk run-1 D15 telemetry strata and no writers maps to run-2 T1 a... | same destination DROP -> REPRESENTED
84. VL-19-084 [ledger L95, App.A L4098] Crosswalk run-1 D16 round 4 / `--cap` has no run-2 counterpart (test g... | same destination DROP -> REPRESENTED
85. VL-19-085 [ledger L96, App.A L4099] Defects new in run-2: D9 refound row takes current call, D10 first-mat... | same destination DROP -> REPRESENTED
86. VL-19-086 [ledger L97, App.A L4100] Number check, tests: run-1 299 passed in 7.1 s versus run-2 304 passed... | same destination DROP -> REPRESENTED
87. VL-19-087 [ledger L98, App.A L4101] Number check, `tools/tmp-scripts`: run-1 "54 scripts plus a README" is... | moved KNOWLEDGE -> DROP (recorded: DROP[duplicate]: duplicate of DR-049; was KNOWLEDGE: the def) -> REPRESENTED
88. VL-19-088 [ledger L99, App.A L4102] Number check, combos: run-2's "106 row folders" (run2:69) is [CODE-CON... | moved EVAL -> DROP (recorded: DROP[duplicate]: duplicate of DR-047; was EVAL: the defect r) -> REPRESENTED
89. VL-19-089 [ledger L100, App.A L1820] audit-D:3 examined 89 rows x 3 = 264 merges | same destination EVAL -> REPRESENTED
90. VL-19-090 [ledger L101, App.A L4103] Number check, verdict flips: both hand-offs say 4 FAIL-to-PASS flips p... | moved EVAL -> DROP (recorded: DROP[duplicate]: duplicate of DR-048; was EVAL: the defect r) -> REPRESENTED
91. VL-19-091 [ledger L102, App.A L1821] Number check, alias issue: run-1 "alias GT3 found once" is wrong; run-... | same destination EVAL -> REPRESENTED
92. VL-19-092 [ledger L103, App.A L1822] Number check, valid-era start: run-1 "source.md first shipped 12:59:34... | same destination EVAL -> REPRESENTED
93. VL-19-093 [ledger L104, App.A L3666] Number check, current section of CR: run-1 says lines 289-373 current ... | same destination KNOWLEDGE -> REPRESENTED
94. VL-19-094 [ledger L105, App.A L1823] Number check, audit C skipped-source count: 156 of 665 runs (earlier 1... | same destination EVAL -> REPRESENTED
95. VL-19-095 [ledger L106, App.A L1824] Number check, pilot: run-1 claim "sonnet alone PASSED both defect-rich... | same destination EVAL -> REPRESENTED
96. VL-19-096 [ledger L107, App.A L1825] Agreed point: the ceiling is about 2-2.5 of 14 defects found per run (... | same destination EVAL -> REPRESENTED
97. VL-19-097 [ledger L108, App.A L1826] Agreed point: default ember plus 2x luna; sonnet plus 2x luna optional... | same destination EVAL -> REPRESENTED
98. VL-19-098 [ledger L109, App.A L4104] Agreed point: merge drop loses 49 blocking findings and 4 flips | same destination DROP -> REPRESENTED
99. VL-19-099 [ledger L110, App.A L4105] Agreed point: 156 of 665 runs are source-blind (CR:373) | same destination DROP -> REPRESENTED
100. VL-19-100 [ledger L111, App.A L4106] Agreed point: one reviewer's `blocking` decides and the panel has no c... | same destination DROP -> REPRESENTED
101. VL-19-101 [ledger L112, App.A L4107] Agreed point: `T01.02` is lost by ref normalisation | same destination DROP -> REPRESENTED
102. VL-19-102 [ledger L113, App.A L4108] Agreed point: `distinct_across_slots` silently duplicates models | same destination DROP -> REPRESENTED
103. VL-19-103 [ledger L114, App.A L4109] Agreed point: telemetry is never written automatically | same destination DROP -> REPRESENTED
104. VL-19-104 [ledger L115, App.A L3667] Agreed point: the E2 branch changes no product code (`git diff --stat ... | same destination KNOWLEDGE -> REPRESENTED
105. VL-19-105 [ledger L116, App.A L3668] Files unchanged between base ec259f1b7 and HEAD, so run-2 line numbers... | same destination KNOWLEDGE -> REPRESENTED
106. VL-19-106 [ledger L117, App.A L55] Files changed by #519: `__init__.py` +3, `panel.py` 525 to 707, `panel... | same destination CORE -> REPRESENTED
107. VL-19-107 [ledger L118, App.A L3669] `git diff --stat ec259f1b7 HEAD` over `panel.py`, `data/`, `ledger.py`... | same destination KNOWLEDGE -> REPRESENTED
108. VL-19-108 [ledger L119, App.A L4110] D1: a finding whose `anchor` or `anchor2` is over 200 chars after whit... | moved CORE -> DROP (recorded: DROP[duplicate]: duplicate of DR-001; was CORE: the defect r) -> REPRESENTED
109. VL-19-109 [ledger L120, App.A L4111] D1 (master): `findings_v2.py` keeps the same limits (citation quote 12... | moved CORE -> DROP (recorded: DROP[duplicate]: duplicate of DR-001; was CORE: the defect r) -> REPRESENTED
110. VL-19-110 [ledger L121, App.A L4112] D2: partial-panel failure is invisible; merge refuses only when no rev... | moved CORE -> DROP (recorded: DROP[duplicate]: duplicate of DR-002; was CORE: the defect r) -> REPRESENTED
111. VL-19-111 [ledger L122, App.A L4113] D3: docstring at `ledger.py:112` says a reviewer with an invalid block... | moved CORE -> DROP (recorded: DROP[duplicate]: duplicate of DR-003; was CORE: the defect r) -> REPRESENTED
112. VL-19-112 [ledger L123, App.A L4114] D4: union-find over `same_defect` with a 3-line tolerance chains disti... | moved CORE -> DROP (recorded: DROP[duplicate]: duplicate of DR-004; was CORE: the defect r) -> REPRESENTED
113. VL-19-113 [ledger L124, App.A L4115] D5: a ref mismatch splits one defect and refs are scraped from free te... | moved CORE -> DROP (recorded: DROP[duplicate]: duplicate of DR-005; was CORE: the defect r) -> REPRESENTED
114. VL-19-114 [ledger L125, App.A L4116] D6: a missing anchor is kept with span None and section "none"; `ancho... | moved CORE -> DROP (recorded: DROP[duplicate]: duplicate of DR-006; was CORE: the defect r) -> REPRESENTED
115. VL-19-115 [ledger L126, App.A L4117] D7: `T01.02` is not a ref token (`_REF_TOKEN` `findings.py:29`; same i... | same destination DROP -> REPRESENTED
116. VL-19-116 [ledger L127, App.A L4118] D8: any single blocking finding fails the round; `confidence` is compu... | moved CORE -> DROP (recorded: DROP[duplicate]: duplicate of DR-008; was CORE: the defect r) -> REPRESENTED
117. VL-19-117 [ledger L128, App.A L4119] D9: a refound row takes the current round's blocking call, so a one-re... | moved CORE -> DROP (recorded: DROP[duplicate]: duplicate of DR-009; was CORE: the defect r) -> REPRESENTED
118. VL-19-118 [ledger L129, App.A L4120] D10: a cluster matches only the first existing row because of `break` ... | moved CORE -> DROP (recorded: DROP[duplicate]: duplicate of DR-010; was CORE: the defect r) -> REPRESENTED
119. VL-19-119 [ledger L130, App.A L4121] D11: `ledger revise` can run twice and remap spans twice; the new text... | moved CORE -> DROP (recorded: DROP[duplicate]: duplicate of DR-011; was CORE: the defect r) -> REPRESENTED
120. VL-19-120 [ledger L131, App.A L4122] D12: `merge` always exits 0 while `ledger verdict` maps PASS 0, REVISE... | moved CORE -> DROP (recorded: DROP[duplicate]: duplicate of DR-012; was CORE: the defect r) -> REPRESENTED
121. VL-19-121 [ledger L132, App.A L4123] D13: a `--report` id missing from `--resolution` gets model None and a... | moved CORE -> DROP (recorded: DROP[duplicate]: duplicate of DR-013; was CORE: the defect r) -> REPRESENTED
122. VL-19-122 [ledger L133, App.A L4124] P1: `distinct_across_slots` silently falls back to duplicates when exc... | moved CORE -> DROP (recorded: DROP[duplicate]: duplicate of DR-014; was CORE: the defect r) -> REPRESENTED
123. VL-19-123 [ledger L134, App.A L56] P1 (master): #519 adds `hard_exclude` and `strict_distinct` (`panel.py... | same destination CORE -> REPRESENTED
124. VL-19-124 [ledger L135, App.A L4125] P2: the gateway environment has an empty `launch` map (`review-tiers.d... | same destination DROP -> REPRESENTED
125. VL-19-125 [ledger L136, App.A L4126] P3: `muse-ember-1.0` is not in the tier data (no file under `src tests... | same destination DROP -> REPRESENTED
126. VL-19-126 [ledger L137, App.A L4127] P4: excluded Qwen and glm are still in tier lists (`:7-9`; classes map... | same destination DROP -> REPRESENTED
127. VL-19-127 [ledger L138, App.A L4128] P5: environment guessed from `$T3Model01`; HEAD `select_env` `panel.py... | same destination DROP -> REPRESENTED
128. VL-19-128 [ledger L139, App.A L4129] P6: re-review resolves to the single fixed anchor because all 8 packag... | moved CORE -> DROP (recorded: DROP[duplicate]: duplicate of DR-019; was CORE: the defect r) -> REPRESENTED
129. VL-19-129 [ledger L140, App.A L4130] P7: `round_robin` uses today's date as the sequence when `--sequence` ... | moved CORE -> DROP (recorded: DROP[duplicate]: duplicate of DR-020; was CORE: the defect r) -> REPRESENTED
130. VL-19-130 [ledger L141, App.A L4131] T1 check: no automatic caller of `append_record` (one manual CLI calle... | same destination DROP -> REPRESENTED
131. VL-19-131 [ledger L142, App.A L4132] T2 check: `STRATA = ("sonnet","haiku")` at `telemetry.py:112-115`; `:2... | same destination DROP -> REPRESENTED
132. VL-19-132 [ledger L143, App.A L4133] B-1: the brief never names the source or driving document (`document_r... | moved CORE -> DROP (recorded: DROP[duplicate]: duplicate of DR-023; was CORE: the defect r) -> REPRESENTED
133. VL-19-133 [ledger L144, App.A L4134] B-2: parser limits (claim at most 300, refs at most 8, id at most 16, ... | moved CORE -> DROP (recorded: DROP[duplicate]: duplicate of DR-024; was CORE: the defect r) -> REPRESENTED
134. VL-19-134 [ledger L145, App.A L4135] B-3: `spec-panel.md:259` "CRITICAL is blocking; a MAJOR ... is blockin... | moved CORE -> DROP (recorded: DROP[duplicate]: duplicate of DR-025; was CORE: the defect r) -> REPRESENTED
135. VL-19-135 [ledger L146, App.A L4136] B-4: report-ending conflict: `spec-panel.md:260` "a critique-mode repo... | moved MODULE-spec -> DROP (recorded: DROP[duplicate]: duplicate of DR-026; was MODULE-spec: the d) -> REPRESENTED
136. VL-19-136 [ledger L147, App.A L4137] B-5: no guidance on what to anchor for `missing-requirement`, anchor u... | moved CORE -> DROP (recorded: DROP[duplicate]: duplicate of DR-027; was CORE: the defect r) -> REPRESENTED
137. VL-19-137 [ledger L148, App.A L4138] B-6: harness category `unpassable-ac` versus parser `unpassable-check`... | moved HARNESS -> DROP (recorded: DROP[duplicate]: duplicate of DR-028; was HARNESS: the defec) -> REPRESENTED
138. VL-19-138 [ledger L149, App.A L4139] B-7: reviewers are not told that one blocking row from any reviewer fa... | moved CORE -> DROP (recorded: DROP[duplicate]: duplicate of DR-029; was CORE: the defect r) -> REPRESENTED
139. VL-19-139 [ledger L150, App.A L3670] Line counts in run-2 1.3 (findings 457, ledger 494, merge_cmd 118, led... | same destination KNOWLEDGE -> REPRESENTED
140. VL-19-140 [ledger L151, App.A L57] findings-v1 location rules: any heading level, case-insensitive, first... | same destination CORE -> REPRESENTED
141. VL-19-141 [ledger L152, App.A L58] Unknown keys in a finding are accepted silently (`_check_finding` `:90... | same destination CORE -> REPRESENTED
142. VL-19-142 [ledger L153, App.A L59] Ledger contract `review-ledger/1`: schema (`ledger.py:17`), statuses (... | same destination CORE -> REPRESENTED
143. VL-19-143 [ledger L154, App.A L60] Resolution contract `review-panel-resolution/1` (`panel.py:27`): revie... | same destination CORE -> REPRESENTED
144. VL-19-144 [ledger L155, App.A L61] Tier table (6 aliases) and environments (gateway, anthropic-only with ... | same destination CORE -> REPRESENTED
145. VL-19-145 [ledger L156, App.A L62] Packaged templates: `@default` is t1b x1 fixed plus t2 x1 random plus ... | same destination CORE -> REPRESENTED
146. VL-19-146 [ledger L157, App.A L3182] Run-2 proposes three harness fixes (anchor limit, source path, keep id... | same destination HARNESS -> REPRESENTED
147. VL-19-147 [ledger L158, App.A L4140] `git diff --stat origin/master...HEAD -- src tests` is empty on the E2... | same destination DROP -> REPRESENTED
148. VL-19-148 [ledger L159, App.A L1827] Test run at HEAD: `uv run pytest tests/review` plus 6 skills files giv... | same destination EVAL -> REPRESENTED
149. VL-19-149 [ledger L160, App.A L1828] Test gap (run2 8.2): exact length boundaries are not tested; `test_rev... | same destination EVAL -> REPRESENTED
150. VL-19-150 [ledger L161, App.A L1829] Test gap (run2 8.2): no test that prompt limits equal parser constants... | same destination EVAL -> REPRESENTED
151. VL-19-151 [ledger L162, App.A L1830] Test gap (run2 8.2): task-id refs such as `T01.02` are untested (`grep... | same destination EVAL -> REPRESENTED
152. VL-19-152 [ledger L163, App.A L1831] Master adds 12 test files under `tests/review`: `test_reflect_cluster_... | same destination EVAL -> REPRESENTED
153. VL-19-153 [ledger L164, App.A L1832] Run-1 claim "the accepted category `unpassable-check` is not covered b... | same destination EVAL -> REPRESENTED
154. VL-19-154 [ledger L165, App.A L1002] Reflect contrast: `reflect-reviewer` is the UC-2 reviewer (base `SKILL... | same destination MODULE-reflect -> REPRESENTED
155. VL-19-155 [ledger L166, App.A L63] Reflect model selection is a separate registry: skill aliases `ANTHROP... | same destination CORE -> REPRESENTED
156. VL-19-156 [ledger L167, App.A L1003] At HEAD reflect already uses the panel kernel in shadow mode: `SKILL.m... | same destination MODULE-reflect -> REPRESENTED
157. VL-19-157 [ledger L168, App.A L64] Reflect contrast "no loop; finding unit = markdown table plus file:lin... | same destination CORE -> REPRESENTED
158. VL-19-158 [ledger L169, App.A L65] Q1 (does `findings_v2` replace findings-v1 or run beside, and does it ... | same destination CORE -> REPRESENTED
159. VL-19-159 [ledger L170, App.A L1004] Q4 (reflect dispatch of non-Claude models; is `reflect-reviewer` pinne... | same destination MODULE-reflect -> REPRESENTED
160. VL-19-160 [ledger L171, App.A L1005] Calibrator and validator agents exist: `src/superclaude/agents/{confid... | same destination MODULE-reflect -> REPRESENTED
161. VL-19-161 [ledger L172, App.A L1833] Artifact: commit b4db265a8 "docs(eval): tasklist review panel model-co... | same destination EVAL -> REPRESENTED
162. VL-19-162 [ledger L173, App.A L1834] Artifact: commit 2d06a4382 "batch 11 plus issue tables" (445 files inc... | same destination EVAL -> REPRESENTED
163. VL-19-163 [ledger L174, App.A L1835] Artifact: commit 4a22d7421 adds the hand-off and `tools/tmp-scripts` (... | same destination EVAL -> REPRESENTED
164. VL-19-164 [ledger L175, App.A L4141] Artifact: "untracked 3,041 files, 1,380 + 1,352 + 309, about 1.5 GB" (... | same destination DROP -> REPRESENTED
165. VL-19-165 [ledger L176, App.A L1836] Artifact: `COMBO-REPORT.md` is 506 lines (tip `wc -l`); lines 289-506 ... | same destination EVAL -> REPRESENTED
166. VL-19-166 [ledger L177, App.A L1837] Artifact: `PILOT-REPORT.md` is 83 lines at tip (run-1 also says 83); m... | same destination EVAL -> REPRESENTED
167. VL-19-167 [ledger L178, App.A L1838] Artifact: `manifest.md` (16 lines) line 5 "Worktree branch: ironbelly/... | same destination EVAL -> REPRESENTED
168. VL-19-168 [ledger L179, App.A L3183] Artifact: `combos/SPEC.md` (152 lines): run procedure at lines 18-36 p... | same destination HARNESS -> REPRESENTED
169. VL-19-169 [ledger L180, App.A L1839] Artifact: three `TASK-WF-*` package folders with ground truth and cand... | same destination EVAL -> REPRESENTED
170. VL-19-170 [ledger L181, App.A L1840] Artifact: `arms/` holds the pilot arms and the blind-scoring layout; n... | same destination EVAL -> REPRESENTED
171. VL-19-171 [ledger L182, App.A L1841] Only 19 `combos/` rows have `RESULT.md` (19 files at the tip, slice VE... | same destination EVAL -> REPRESENTED
172. VL-19-172 [ledger L183, App.A L66] Artifact: `probe/probe.json` (Stage 0 probe) shows aliases serve only ... | same destination CORE -> REPRESENTED
173. VL-19-173 [ledger L184, App.A L4142] Artifact: `quarantine-pre-src-luna/` is audit-only material (CR:107) | same destination DROP -> REPRESENTED
174. VL-19-174 [ledger L185, App.A L3184] Artifact: `tools/run-reviewer.sh` (87 lines); line 10 hard-codes `SRC_... | same destination HARNESS -> REPRESENTED
175. VL-19-175 [ledger L186, App.A L4143] Artifact: `run-reviewer.sh.bad-launch` and `.unpassable-ac` (audit cop... | same destination DROP -> REPRESENTED
176. VL-19-176 [ledger L187, App.A L3185] Artifact: in `tools/tmp-scripts/` (55 files) `judge-one.sh` and `anon-... | same destination HARNESS -> REPRESENTED
177. VL-19-177 [ledger L188, App.A L4144] Artifact: the rest of `tools/tmp-scripts/` is not reusable, incl. `sna... | same destination DROP -> REPRESENTED
178. VL-19-178 [ledger L189, App.A L1842] Artifact: `analysis/*.py`, `final-table.md`, `issue-table/`, `allsets/... | same destination EVAL -> REPRESENTED
179. VL-19-179 [ledger L190, App.A L1843] Artifact: `analysis/audits/audit-A..F/` are six audits; only A and D h... | same destination EVAL -> REPRESENTED
180. VL-19-180 [ledger L191, App.A L4145] Artifact: `analysis/RAW-TRANSCRIPTS-NOT-COMMITTED.md` lines 1-4 (2,916... | same destination DROP -> REPRESENTED
181. VL-19-181 [ledger L192, App.A L3186] Artifact: `/tmp/evalsb/repo`, `/tmp/audit-*/`, `/tmp/final-table.py`, ... | same destination HARNESS -> REPRESENTED
182. VL-19-182 [ledger L193, App.A L4146] Branch freshness: 11 commits behind origin/master (run2:55), VERIFIED | same destination DROP -> REPRESENTED
183. VL-19-183 [ledger L194, App.A L4147] Source/test changes on the E2 branch: none (run2:54), [UNVERIFIED] | same destination DROP -> REPRESENTED
184. VL-19-184 [ledger L195, App.A L1844] Metric definitions: "real blocking /8" = judge credited through a bloc... | same destination EVAL -> REPRESENTED
185. VL-19-185 [ledger L196, App.A L1845] Judge-blocking overcounts real blocking: 65 versus 38 over 71 rows (CR... | same destination EVAL -> REPRESENTED
186. VL-19-186 [ledger L197, App.A L1846] "Wrong blockers" is biased by novel real finds (CR:75 per run-1; "know... | same destination EVAL -> REPRESENTED
187. VL-19-187 [ledger L198, App.A L1847] Candidate pre-registered metric list: found /14, real blocking /8, jud... | same destination EVAL -> REPRESENTED
188. VL-19-188 [ledger L199, App.A L4148] Valid era versus src era and quarantine rules: era boundary ship 2026-... | same destination DROP -> REPRESENTED
189. VL-19-189 [ledger L200, App.A L1848] B1-B8 and I1-I8 ground-truth labels map to GT ids through the CR legen... | same destination EVAL -> REPRESENTED
190. VL-19-190 [ledger L201, App.A L4149] R1: every panel finds about 2-2.5 of 14; no row above 4/14; n=71 rows ... | same destination DROP -> REPRESENTED
191. VL-19-191 [ledger L202, App.A L1849] R2: never found by any of 106 runs: B1, B2, I5, I6; B6 once (CR:431, :... | same destination EVAL -> REPRESENTED
192. VL-19-192 [ledger L203, App.A L1850] R3: B3 found 95/106, I8 76, I2 71 (CR:502); these dominate scores | same destination EVAL -> REPRESENTED
193. VL-19-193 [ledger L204, App.A L1851] R4: ember + 2x luna finds 1.83/14, real blocking 0.17/8, wrong blocker... | same destination EVAL -> REPRESENTED
194. VL-19-194 [ledger L205, App.A L1852] R5: sonnet + 2x luna finds 2.33/14, real blocking 0.33, control 1.33, ... | same destination EVAL -> REPRESENTED
195. VL-19-195 [ledger L206, App.A L1853] R6: haiku + 2x luna gives 1.2/8 real blocking, 2.2/14, 3.0 wrong block... | same destination EVAL -> REPRESENTED
196. VL-19-196 [ledger L207, App.A L1854] R7: ember + sonnet finds 2.5/14, 0.25 wrong blockers, 0.25 real blocki... | same destination EVAL -> REPRESENTED
197. VL-19-197 [ledger L208, App.A L1855] R8: only three effects survive audit F: second luna adds +0.83 control... | same destination EVAL -> REPRESENTED
198. VL-19-198 [ledger L209, App.A L67] R9: five-reviewer panels give no catch gain for 2-4x the cost (n=4 eac... | same destination CORE -> REPRESENTED
199. VL-19-199 [ledger L210, App.A L68] R10: sonnet is associated with rare issues: all 3 sets reaching I4, 3 ... | same destination CORE -> REPRESENTED
200. VL-19-200 [ledger L211, App.A L4150] R11: single-run highs never replicated (grok + 2x haiku + sonnet 4/14 ... | same destination DROP -> REPRESENTED
201. VL-19-201 [ledger L212, App.A L4151] R12: pilot found sonnet alone 2.15 catches per 100k tokens and 0/8 blo... | same destination DROP -> REPRESENTED
202. VL-19-202 [ledger L213, App.A L69] R13: without `source.md` sol and terra were "incomplete" with 0 findin... | same destination CORE -> REPRESENTED
203. VL-19-203 [ledger L214, App.A L4152] R14: 156 of 665 valid-era runs never referenced `source.md`: ember 81/... | same destination DROP -> REPRESENTED
204. VL-19-204 [ledger L215, App.A L70] R15: terra and sol produced 51 incomplete reports, incl. 16 empty terr... | same destination CORE -> REPRESENTED
205. VL-19-205 [ledger L216, App.A L71] R16: luna quotes anchors verbatim in 91.4% versus 98-100% for the othe... | same destination CORE -> REPRESENTED
206. VL-19-206 [ledger L217, App.A L3671] R17: presence effects (grok 2.62 vs 2.00; wonder 2.75 vs 1.98; sonnet ... | same destination KNOWLEDGE -> REPRESENTED
207. VL-19-207 [ledger L218, App.A L3672] R18 operational: Qwen timeout (3 x 3000 s in the pilot); glm slow at 8... | same destination KNOWLEDGE -> REPRESENTED
208. VL-19-208 [ledger L219, App.A L4153] R19: tier aliases serve only the first model of a tier, so dispatch mu... | same destination DROP -> REPRESENTED
209. VL-19-209 [ledger L220, App.A L1856] R20: merge drops 80 reviewer-level cases, 49 blocking findings lost an... | same destination EVAL -> REPRESENTED
210. VL-19-210 [ledger L221, App.A L1857] R21: judging is reliable: 294 clean judge outputs; blind re-judge 12/1... | same destination EVAL -> REPRESENTED
211. VL-19-211 [ledger L222, App.A L4154] Retraction (1): "n2-sonnet-src 8/14 and 5/8" came from a judge that di... | same destination DROP -> REPRESENTED
212. VL-19-212 [ledger L223, App.A L4155] Retraction (2): early per-model blocking counts came from a grep witho... | same destination DROP -> REPRESENTED
213. VL-19-213 [ledger L224, App.A L4156] Retraction (3): "r2-sonnet-src is a muse-wonder row" | same destination DROP -> REPRESENTED
214. VL-19-214 [ledger L225, App.A L4157] Retraction (4): "ember weaker than wonder" | same destination DROP -> REPRESENTED
215. VL-19-215 [ledger L226, App.A L4158] Retraction (5): "second run of the same model adds nothing" and "haiku... | same destination DROP -> REPRESENTED
216. VL-19-216 [ledger L227, App.A L4159] Retraction (6): judge-blocking over denominator 8 (65 versus 38, CR:29... | same destination DROP -> REPRESENTED
217. VL-19-217 [ledger L228, App.A L4160] Retraction (7): "second luna adds +0.5 blocking" is reversed (0.50 to ... | same destination DROP -> REPRESENTED
218. VL-19-218 [ledger L229, App.A L4161] Retraction (8): skipped-source count 161 corrected to 156 (CR:293 vers... | same destination DROP -> REPRESENTED
219. VL-19-219 [ledger L230, App.A L4162] Retraction (9): "sonnet + 2x luna as standard" rejected (CR:383 versus... | same destination DROP -> REPRESENTED
220. VL-19-220 [ledger L231, App.A L4163] Retraction (10): batch-10 outage runs "not moved" is wrong, they were ... | same destination DROP -> REPRESENTED
221. VL-19-221 [ledger L232, App.A L4164] Retraction (11): all earlier tables are superseded (CR:289, :297 VERIF... | same destination DROP -> REPRESENTED
222. VL-19-222 [ledger L233, App.A L4165] D1 destination: CORE parser should repair or truncate over-length fiel... | same destination DROP -> REPRESENTED
223. VL-19-223 [ledger L234, App.A L4166] D2 destination: CORE merge; partial-panel failure invisible; OPEN | same destination DROP -> REPRESENTED
224. VL-19-224 [ledger L235, App.A L4167] D3 destination: CORE ledger; clearing ignores `block_ok`; OPEN | same destination DROP -> REPRESENTED
225. VL-19-225 [ledger L236, App.A L72] D4 status: OPEN in `findings.cluster` (used by the ledger); `cluster_v... | same destination CORE -> REPRESENTED
226. VL-19-226 [ledger L237, App.A L73] D5 status: OPEN in v1; `same_defect_v2` keeps the refs-intersect-or-bo... | same destination CORE -> REPRESENTED
227. VL-19-227 [ledger L238, App.A L4168] D6 destination: CORE anchor; 46 unanchored rows (13 blocking); OPEN in... | same destination DROP -> REPRESENTED
228. VL-19-228 [ledger L239, App.A L1284] D7 destination: ref syntax must be per target (tasklist task ids versu... | same destination MODULE-tasklist -> REPRESENTED
229. VL-19-229 [ledger L240, App.A L4169] D8 destination: OPEN decision on a quorum or calibrator for blocking; ... | same destination DROP -> REPRESENTED
230. VL-19-230 [ledger L241, App.A L4170] D9 status: CORE loop; re-review downgrade by a single reviewer; OPEN a... | same destination DROP -> REPRESENTED
231. VL-19-231 [ledger L242, App.A L4171] D10 status: CORE ledger; first-match `break`; OPEN | same destination DROP -> REPRESENTED
232. VL-19-232 [ledger L243, App.A L4172] D11 status: CORE ledger; revise twice; OPEN (read-verified) | same destination DROP -> REPRESENTED
233. VL-19-233 [ledger L244, App.A L4173] D12 status: CORE CLI; merge exit 0; OPEN, low severity | same destination DROP -> REPRESENTED
234. VL-19-234 [ledger L245, App.A L4174] D13 status: CORE CLI; missing report/resolution cross-check; OPEN, low | same destination DROP -> REPRESENTED
235. VL-19-235 [ledger L246, App.A L4175] P1 status: silent duplicates OPEN by default; `--strict-distinct` is o... | same destination DROP -> REPRESENTED
236. VL-19-236 [ledger L247, App.A L4176] P2 status: empty gateway `launch` map OPEN (CORE dispatch) | same destination DROP -> REPRESENTED
237. VL-19-237 [ledger L248, App.A L4177] P3 status: ember absent from tier data OPEN, and the tier list is owne... | same destination DROP -> REPRESENTED
238. VL-19-238 [ledger L249, App.A L4178] P4 status: excluded models in tier lists OPEN in data; `--hard-exclude... | same destination DROP -> REPRESENTED
239. VL-19-239 [ledger L250, App.A L4179] P5 status: environment guessed from `T3Model01` OPEN | same destination DROP -> REPRESENTED
240. VL-19-240 [ledger L251, App.A L4180] P6 status: re-review collapses to one anchor is by design and the same... | same destination DROP -> REPRESENTED
241. VL-19-241 [ledger L252, App.A L4181] P7 status: `round_robin` depends on the date, OPEN, low | same destination DROP -> REPRESENTED
242. VL-19-242 [ledger L253, App.A L4182] T1 and T2 status: telemetry unwired and strata hard-coded, OPEN (CORE ... | same destination DROP -> REPRESENTED
243. VL-19-243 [ledger L254, App.A L4183] B-1 status: brief has no source placeholder, OPEN (CORE brief contract... | same destination DROP -> REPRESENTED
244. VL-19-244 [ledger L255, App.A L74] B-2 lesson: limits stated in the prompt alone did not hold, so limits ... | same destination CORE -> REPRESENTED
245. VL-19-245 [ledger L256, App.A L4184] B-3 status: blocking semantics have a triple conflict and must be deci... | same destination DROP -> REPRESENTED
246. VL-19-246 [ledger L257, App.A L4185] B-4 status: report-ending conflict, SPEC, OPEN, low | same destination DROP -> REPRESENTED
247. VL-19-247 [ledger L258, App.A L4186] B-5 status: anchor guidance missing, CORE brief, OPEN | same destination DROP -> REPRESENTED
248. VL-19-248 [ledger L259, App.A L4187] B-6 status: `unpassable-ac` label FIXED in the harness | same destination DROP -> REPRESENTED
249. VL-19-249 [ledger L260, App.A L4188] B-7 status: merge consequence not told to reviewers, CORE brief, OPEN | same destination DROP -> REPRESENTED
250. VL-19-250 [ledger L261, App.A L4189] H1: cyclic fallback ladder in the harness, FIXED (ladder guard at `run... | moved HARNESS -> DROP (recorded: DROP[duplicate]: duplicate of DR-030; was HARNESS: the defec) -> REPRESENTED
251. VL-19-251 [ledger L262, App.A L4190] H2, H3, H4 status: meta overwrite, attempt overwrite and presence-only... | same destination DROP -> REPRESENTED
252. VL-19-252 [ledger L263, App.A L1858] H5: stale attempt files inflate the cost of 5 runs; disclosed | same destination EVAL -> REPRESENTED
253. VL-19-253 [ledger L264, App.A L4191] H6: stale merges in n2-terra, r2-sol, n5-sol, n5-terra; disclosed (VER... | moved EVAL -> DROP (recorded: DROP[duplicate]: duplicate of DR-035; was EVAL: the defect r) -> REPRESENTED
254. VL-19-254 [ledger L265, App.A L1859] H7: an API-error judge left a plausible score; FIXED by procedure | same destination EVAL -> REPRESENTED
255. VL-19-255 [ledger L266, App.A L4192] H8 and H9: grep without the space and `attrib.py` membership credit; F... | same destination DROP -> REPRESENTED
256. VL-19-256 [ledger L267, App.A L4193] H10: `/tmp` analysis scripts, OPEN (VERIFIED) | same destination DROP -> REPRESENTED
257. VL-19-257 [ledger L268, App.A L3673] H11: identity bleed across a 12-worker batch; mitigated | same destination KNOWLEDGE -> REPRESENTED
258. VL-19-258 [ledger L269, App.A L3674] H12: the `claude` binary was replaced mid-run; mitigated | same destination KNOWLEDGE -> REPRESENTED
259. VL-19-259 [ledger L270, App.A L1860] Worked lesson 1: ground truth from the implement history | same destination EVAL -> REPRESENTED
260. VL-19-260 [ledger L271, App.A L1861] Worked lesson 2: a control package | same destination EVAL -> REPRESENTED
261. VL-19-261 [ledger L272, App.A L1862] Worked lesson 3: blind scoring | same destination EVAL -> REPRESENTED
262. VL-19-262 [ledger L273, App.A L4194] Worked lesson 4: reviewer sandbox | same destination DROP -> REPRESENTED
263. VL-19-263 [ledger L274, App.A L75] Worked lesson 5: model identity taken from the transcript, not from wh... | same destination CORE -> REPRESENTED
264. VL-19-264 [ledger L275, App.A L3187] Worked lesson 6: quarantine in place | same destination HARNESS -> REPRESENTED
265. VL-19-265 [ledger L276, App.A L1863] Worked lesson 7: replicates of 4-6 per combination | same destination EVAL -> REPRESENTED
266. VL-19-266 [ledger L277, App.A L1864] Worked lesson 8: six independent audits (A-F) | same destination EVAL -> REPRESENTED
267. VL-19-267 [ledger L278, App.A L1865] Worked lesson 9: two views, AS-SCORED and AUDIT-CLEAN | same destination EVAL -> REPRESENTED
268. VL-19-268 [ledger L279, App.A L1866] Worked lesson 10: dual independent counting (10 agents plus a script; ... | same destination EVAL -> REPRESENTED
269. VL-19-269 [ledger L280, App.A L1867] Worked lesson 11: permutation tests | same destination EVAL -> REPRESENTED
270. VL-19-270 [ledger L281, App.A L3188] Worked lesson 12: run scheduling with caps and cooldowns | same destination HARNESS -> REPRESENTED
271. VL-19-271 [ledger L282, App.A L3189] Worked lesson 13: an append-only operations log | same destination HARNESS -> REPRESENTED
272. VL-19-272 [ledger L283, App.A L3675] Failed lesson 1: ranking single runs | same destination KNOWLEDGE -> REPRESENTED
273. VL-19-273 [ledger L284, App.A L4195] Failed lesson 2: ledger-membership attribution | same destination DROP -> REPRESENTED
274. VL-19-274 [ledger L285, App.A L4196] Failed lesson 3: literal grep for counting | same destination DROP -> REPRESENTED
275. VL-19-275 [ledger L286, App.A L4197] Failed lesson 4: trusting a judge file without checking it | same destination DROP -> REPRESENTED
276. VL-19-276 [ledger L287, App.A L3190] Failed lesson 5: starting before an end-to-end harness check | same destination HARNESS -> REPRESENTED
277. VL-19-277 [ledger L288, App.A L4198] Failed lesson 6: cyclic fallback ladder | same destination DROP -> REPRESENTED
278. VL-19-278 [ledger L289, App.A L3676] Failed lesson 7: high concurrency | same destination KNOWLEDGE -> REPRESENTED
279. VL-19-279 [ledger L290, App.A L4199] Failed lesson 8: tier aliases | same destination DROP -> REPRESENTED
280. VL-19-280 [ledger L291, App.A L1868] Failed lesson 9: one metric name for two things | same destination EVAL -> REPRESENTED
281. VL-19-281 [ledger L292, App.A L4200] Failed lesson 10: `/tmp` analysis, and superseded text left in place | same destination DROP -> REPRESENTED
282. VL-19-282 [ledger L293, App.A L3191] Next-time lesson 1: a one-package smoke test of reviewer to merge to j... | same destination HARNESS -> REPRESENTED
283. VL-19-283 [ledger L294, App.A L76] Next-time lesson 2: validate reports with the real parser at run time | same destination CORE -> REPRESENTED
284. VL-19-284 [ledger L295, App.A L77] Next-time lesson 3: name every input in the brief and check from the t... | same destination CORE -> REPRESENTED
285. VL-19-285 [ledger L296, App.A L1869] Next-time lesson 4: pre-register metrics and the decision rule | same destination EVAL -> REPRESENTED
286. VL-19-286 [ledger L297, App.A L1870] Next-time lesson 5: plan replicates and power | same destination EVAL -> REPRESENTED
287. VL-19-287 [ledger L298, App.A L78] Next-time lesson 6: keep raw identity evidence in committed meta | same destination CORE -> REPRESENTED
288. VL-19-288 [ledger L299, App.A L1871] Next-time lesson 7: double-score a sample with a second judge family | same destination EVAL -> REPRESENTED
289. VL-19-289 [ledger L300, App.A L4201] Next-time lesson 8: self-contained analysis scripts | same destination DROP -> REPRESENTED
290. VL-19-290 [ledger L301, App.A L1872] Next-time lesson 9: score the raw union of reviewer findings as well a... | same destination EVAL -> REPRESENTED
291. VL-19-291 [ledger L302, App.A L4202] DM1: Qwen3.8-max excluded everywhere (Owner, 2026-11-11; PILOT:12) | same destination DROP -> REPRESENTED
292. VL-19-292 [ledger L303, App.A L4203] DM2: dispatch by raw model id with `claude -p`, not by tier alias (coo... | same destination DROP -> REPRESENTED
293. VL-19-293 [ledger L304, App.A L4204] DM3: sandbox without implement history (coordinator; `manifest.md:10` ... | same destination DROP -> REPRESENTED
294. VL-19-294 [ledger L305, App.A L4205] DM4: `.catfix.md` normalisation (SPEC:38-39) | same destination DROP -> REPRESENTED
295. VL-19-295 [ledger L306, App.A L3677] DM5: tear down 12-worker batch 3, quarantine it, rerun serially (Owner... | same destination KNOWLEDGE -> REPRESENTED
296. VL-19-296 [ledger L307, App.A L4206] DM6: ship `source.md` next to the candidate (Owner request 2026-11-12;... | same destination DROP -> REPRESENTED
297. VL-19-297 [ledger L308, App.A L4207] DM7: glm excluded from batch 4 on (Owner, 2026-11-12 14:42; SPEC:97-98... | same destination DROP -> REPRESENTED
298. VL-19-298 [ledger L309, App.A L1873] DM8: quarantine all pre-source luna data (Owner, 2026-11-12 15:16; CR:... | same destination EVAL -> REPRESENTED
299. VL-19-299 [ledger L310, App.A L4208] DM9: muse-ember replaces wonder; the owner is adding it as Tier 04 Mod... | same destination DROP -> REPRESENTED
300. VL-19-300 [ledger L311, App.A L79] DM10: fallback ladder v2 then v3 guards (Owner then coordinator; SPEC:... | same destination CORE -> REPRESENTED
301. VL-19-301 [ledger L312, App.A L1874] DM11: replicate study with 4 runs per combination (Owner, 2026-11-12 2... | same destination EVAL -> REPRESENTED
302. VL-19-302 [ledger L313, App.A L3678] DM12: testing closed and batch 10 dropped (Owner, 2026-11-13 01:09; qu... | same destination KNOWLEDGE -> REPRESENTED
303. VL-19-303 [ledger L314, App.A L4209] DM13: "real blocking" is the metric (coordinator after audit F; CR:291... | same destination DROP -> REPRESENTED
304. VL-19-304 [ledger L315, App.A L1285] DM14: final panel guidance: default ember + 2x luna; quality tier sonn... | same destination MODULE-tasklist -> REPRESENTED
305. VL-19-305 [ledger L316, App.A L4210] DM15: fix the harness before more model testing (anchor limit, source ... | same destination DROP -> REPRESENTED
306. VL-19-306 [ledger L317, App.A L4211] DM16: raw transcripts left out of commits (Owner, 2026-11-13; note lin... | same destination DROP -> REPRESENTED
307. VL-19-307 [ledger L318, App.A L4212] DM17: never stage `.claude/`; change nothing under `.dev/tasks/` (Owne... | same destination DROP -> REPRESENTED
308. VL-19-308 [ledger L319, App.A L4213] DM18: no PR, push the research branch to the fork only (Owner, 2026-11... | same destination DROP -> REPRESENTED
309. VL-19-309 [ledger L320, App.A L80] DO1: how to stop the D1 whole-finding drop (raise the limits, truncate... | same destination CORE -> REPRESENTED
310. VL-19-310 [ledger L321, App.A L81] DO2: does one broken reviewer invalidate the round or is the break onl... | same destination CORE -> REPRESENTED
311. VL-19-311 [ledger L322, App.A L82] DO3: keep any-single-blocking, or move to quorum, calibrator or valida... | same destination CORE -> REPRESENTED
312. VL-19-312 [ledger L323, App.A L1286] DO4: how tasklist review runs: the spec-panel loop plus `superclaude r... | same destination MODULE-tasklist -> REPRESENTED
313. VL-19-313 [ledger L324, App.A L83] DO5: put the decided panels into product data: add ember, templates fo... | same destination CORE -> REPRESENTED
314. VL-19-314 [ledger L325, App.A L4214] DO6: define gateway dispatch for named models (P2, R19) | same destination DROP -> REPRESENTED
315. VL-19-315 [ledger L326, App.A L1875] DO7: re-run the decided panels after the harness fixes before adopting... | same destination EVAL -> REPRESENTED
316. VL-19-316 [ledger L327, App.A L3192] DO8: raw transcripts: commit (LFS), archive or delete; reconcile 2,916... | same destination HARNESS -> REPRESENTED
317. VL-19-317 [ledger L328, App.A L4215] DO9: replicate the muse-wonder rows when quota returns (new study, CR:... | same destination DROP -> REPRESENTED
318. VL-19-318 [ledger L329, App.A L4216] DO10: wire telemetry (T1) | same destination DROP -> REPRESENTED
319. VL-19-319 [ledger L330, App.A L4217] DO11: source/driving-document placeholder in the brief (B-1, R14) | same destination DROP -> REPRESENTED
320. VL-19-320 [ledger L331, App.A L84] Product code the study exercised (`findings.py`, `ledger.py`, `merge_c... | same destination CORE -> REPRESENTED
321. VL-19-321 [ledger L332, App.A L1629] The reviewer brief is spec-shaped and scoped to `/sc:spec-panel --mode... | same destination MODULE-spec -> REPRESENTED
322. VL-19-322 [ledger L333, App.A L85] Category `unpassable-check` (`findings.py:17`) fits plan acceptance cr... | same destination CORE -> REPRESENTED
323. VL-19-323 [ledger L334, App.A L4218] Harness `run-reviewer.sh` is mostly generic but has a hard-coded path ... | same destination DROP -> REPRESENTED
324. VL-19-324 [ledger L335, App.A L4219] Panel recommendations (DM14) rest on plan packages only; transfer to s... | same destination DROP -> REPRESENTED
325. VL-19-325 [ledger L336, App.A L4220] Q1 (does `findings_v2` replace v1 or run beside, does it still drop wh... | same destination DROP -> REPRESENTED
326. VL-19-326 [ledger L337, App.A L86] Q2 (does `cluster.py` replace `findings.cluster`; chain or split on re... | same destination CORE -> REPRESENTED
327. VL-19-327 [ledger L338, App.A L4221] Q3 (do `hard_exclude` and `strict_distinct` remove silent duplicates a... | same destination DROP -> REPRESENTED
328. VL-19-328 [ledger L339, App.A L4222] Q4 (dispatch of non-Claude models while `reflect-reviewer` is pinned t... | same destination DROP -> REPRESENTED
329. VL-19-329 [ledger L340, App.A L87] Q5 (which finding unit wins, exact-quote anchor or file:line): `findin... | same destination CORE -> REPRESENTED
330. VL-19-330 [ledger L341, App.A L1876] Q6 (does the reflect calibrator plus validator reduce wrong blockers o... | same destination EVAL -> REPRESENTED
331. VL-19-331 [ledger L342, App.A L4223] Q7 (does tasklist review stay on reflect UC-1 or move to the unified p... | same destination DROP -> REPRESENTED
332. VL-19-332 [ledger L343, App.A L88] Q8 (is the review loop with cap 3, revise and `resolved_check` kept fo... | same destination CORE -> REPRESENTED
333. VL-19-333 [ledger L344, App.A L4224] Q9 (which model registry wins: tier JSON, `ANTHROPIC_DEFAULT_*_MODEL`,... | same destination DROP -> REPRESENTED
334. VL-19-334 [ledger L345, App.A L4225] Q10 (muse-ember in gateway lists; should the tier JSON follow ccsessio... | same destination DROP -> REPRESENTED
335. VL-19-335 [ledger L346, App.A L1006] Q11 (calibrator 6-dimension rubric versus reflect 5-dimension): not ch... | same destination MODULE-reflect -> REPRESENTED
336. VL-19-336 [ledger L347, App.A L4226] K1: branch is 11 behind and code cites describe the base; this worktre... | same destination DROP -> REPRESENTED
337. VL-19-337 [ledger L348, App.A L4227] K2: adopting the `findings_v2` limits carries D1 (limits identical, VE... | same destination DROP -> REPRESENTED
338. VL-19-338 [ledger L349, App.A L1877] K3: recommendations rest on 3 packages, n of 4-6 and the ceiling | same destination EVAL -> REPRESENTED
339. VL-19-339 [ledger L350, App.A L1878] K4: only round 1 was scored; D3 and D9-D11 are untested with real pane... | same destination EVAL -> REPRESENTED
340. VL-19-340 [ledger L351, App.A L4228] K5: the product panel cannot launch the decided models (empty launch, ... | same destination DROP -> REPRESENTED
341. VL-19-341 [ledger L352, App.A L89] K6: gateway behaviour silently changes the reviewer (U6) | same destination CORE -> REPRESENTED
342. VL-19-342 [ledger L353, App.A L4229] K7: 1.5 GB of raw evidence exists on one machine only; the tip later u... | same destination DROP -> REPRESENTED
343. VL-19-343 [ledger L354, App.A L4230] K8: analysis scripts depend on `/tmp` (VERIFIED) | same destination DROP -> REPRESENTED
344. VL-19-344 [ledger L355, App.A L4231] K9: the two hand-offs may disagree; now compared in section 3 | same destination DROP -> REPRESENTED
345. VL-19-345 [ledger L356, App.A L4232] K10: blocking semantics differ across files (B-3, VERIFIED) | same destination DROP -> REPRESENTED
346. VL-19-346 [ledger L357, App.A L4233] K11: telemetry strata hard-coded (VERIFIED) | same destination DROP -> REPRESENTED
347. VL-19-347 [ledger L358, App.A L4234] Four of the 14 run-2 test-gap rows were spot-checked at HEAD and are s... | same destination DROP -> REPRESENTED
348. VL-19-348 [ledger L359, App.A L1879] Test gap: malformed resolution file untested; not re-checked at HEAD [... | same destination EVAL -> REPRESENTED
349. VL-19-349 [ledger L360, App.A L1880] Test gap: report id absent from the resolution untested (D13) [UNVERIF... | same destination EVAL -> REPRESENTED
350. VL-19-350 [ledger L361, App.A L1881] Test gap: duplicate reviewer id untested; the code exists (`ledger.py:... | same destination EVAL -> REPRESENTED
351. VL-19-351 [ledger L362, App.A L4235] Test gap: all seven `@live7` models distinct is untested (P1); #519's ... | moved EVAL -> DROP (recorded: DROP[duplicate]: duplicate of DR-073; was EVAL: the defect r) -> REPRESENTED
352. VL-19-352 [ledger L363, App.A L1882] Test gap: round 4+ and non-default `--cap` untested (L3) | same destination EVAL -> REPRESENTED
353. VL-19-353 [ledger L364, App.A L1883] Test gap: broken-reviewer report text untested | same destination EVAL -> REPRESENTED
354. VL-19-354 [ledger L365, App.A L1884] Test gap: a valid-JSON-but-over-limit line versus clearing untested (D... | same destination EVAL -> REPRESENTED
355. VL-19-355 [ledger L366, App.A L1885] Test gap: partial-panel verdict flip untested (D2) | same destination EVAL -> REPRESENTED
356. VL-19-356 [ledger L367, App.A L1886] Test gap: mega-cluster, ref-split and missing-anchor rows untested (D4... | same destination EVAL -> REPRESENTED
357. VL-19-357 [ledger L368, App.A L1887] Test gap: `ledger revise` run twice untested (D11) | same destination EVAL -> REPRESENTED
358. VL-19-358 [ledger L369, App.A L1888] Test gap: no end-to-end multi-round run exists | same destination EVAL -> REPRESENTED
359. VL-19-359 [ledger L370, App.A L3193] Test gap: `run-reviewer.sh` itself is untested | same destination HARNESS -> REPRESENTED
360. VL-19-360 [ledger L371, App.A L3679] Run-2 says nothing about the E3 installed variants (only run-1 D14b an... | same destination KNOWLEDGE -> REPRESENTED
361. VL-19-361 [ledger L372, App.A L90] Overlap, finding wire format: E1 `findings_v2.py` (304 lines) adds `ci... | same destination CORE -> REPRESENTED
362. VL-19-362 [ledger L373, App.A L4236] Overlap, length limits: same in v1 and v2 (`:80, :111, :126, :132, :13... | same destination DROP -> REPRESENTED
363. VL-19-363 [ledger L374, App.A L4237] Overlap, clustering: E1 `cluster_v2` is path-aware with a chain flag, ... | same destination DROP -> REPRESENTED
364. VL-19-364 [ledger L375, App.A L91] Overlap, verdict and blocking rule: legacy reflect cards carry no bloc... | same destination CORE -> REPRESENTED
365. VL-19-365 [ledger L376, App.A L92] Overlap, calibration and validation: E1 has `confidence-calibrator` an... | same destination CORE -> REPRESENTED
366. VL-19-366 [ledger L377, App.A L4238] Overlap, panel template, tier and environment: E1 has `panel.py` (707 ... | same destination DROP -> REPRESENTED
367. VL-19-367 [ledger L378, App.A L4239] Overlap, model registry: tier JSON (shadow), `ANTHROPIC_DEFAULT_*_MODE... | same destination DROP -> REPRESENTED
368. VL-19-368 [ledger L379, App.A L93] Overlap, dispatch of non-Claude models: E1 `reflect-reviewer.md` is pi... | same destination CORE -> REPRESENTED
369. VL-19-369 [ledger L380, App.A L94] Overlap, model identity capture (conflict candidate C-5): E1 shadow co... | same destination CORE -> REPRESENTED
370. VL-19-370 [ledger L381, App.A L95] Overlap, telemetry: `telemetry.py` and `telemetry_cmd.py` unchanged; `... | same destination CORE -> REPRESENTED
371. VL-19-371 [ledger L382, App.A L1630] Overlap, review loop (revise, re-review, cap 3, `resolved_check`): not... | same destination MODULE-spec -> REPRESENTED
372. VL-19-372 [ledger L383, App.A L96] Overlap, brief contract: reflect shadow adds one findings-block line t... | same destination CORE -> REPRESENTED
373. VL-19-373 [ledger L384, App.A L4240] Overlap, today's tasklist review entry points: reflect UC-1 `--mode pr... | same destination DROP -> REPRESENTED
374. VL-19-374 [ledger L385, App.A L1889] Overlap, benchmark and regression set: E1 has the shadow-model-combos ... | same destination EVAL -> REPRESENTED
375. VL-19-375 [ledger L386, App.A L97] U1 (Must): no silent finding loss; per-reviewer drop counts; HEAD stor... | same destination CORE -> REPRESENTED
376. VL-19-376 [ledger L387, App.A L98] U2 (Must): over-long anchors handled, the same policy in v1 and v2; a ... | same destination CORE -> REPRESENTED
377. VL-19-377 [ledger L388, App.A L99] U3 (Must): an invalid reviewer is visible in the verdict and not count... | same destination CORE -> REPRESENTED
378. VL-19-378 [ledger L389, App.A L100] U4 (Must for plan/tasklist): the brief names every input by role and r... | same destination CORE -> REPRESENTED
379. VL-19-379 [ledger L390, App.A L101] U5 (Should): limits in the brief plus a test that pins prompt against ... | same destination CORE -> REPRESENTED
380. VL-19-380 [ledger L391, App.A L102] U6 (Must): observed model identity captured and a mismatch invalidates... | same destination CORE -> REPRESENTED
381. VL-19-381 [ledger L392, App.A L103] U7 (Must for non-anchor tiers): a real dispatch path for named gateway... | same destination CORE -> REPRESENTED
382. VL-19-382 [ledger L393, App.A L104] U8 (Must if DM14 is adopted): data can express the decided panels (emb... | same destination CORE -> REPRESENTED
383. VL-19-383 [ledger L394, App.A L1287] U9 (Should): plan and tasklist ids count as refs, or are configurable ... | same destination MODULE-tasklist -> REPRESENTED
384. VL-19-384 [ledger L395, App.A L1631] U10 (Must): keep the loop guarantees (cap 3, Reviser brief only for bl... | same destination MODULE-spec -> REPRESENTED
385. VL-19-385 [ledger L396, App.A L1288] U11 (Must): keep today's entry-point semantics (reflect `--mode pre` a... | same destination MODULE-tasklist -> REPRESENTED
386. VL-19-386 [ledger L397, App.A L105] U12 (Should): a documented verdict rule told to reviewers; quorum vers... | same destination CORE -> REPRESENTED
387. VL-19-387 [ledger L398, App.A L106] U13 (Should): clustering must not chain unrelated findings and must ke... | same destination CORE -> REPRESENTED
388. VL-19-388 [ledger L399, App.A L107] U14 (Should): a missing anchor is reported and handled | same destination CORE -> REPRESENTED
389. VL-19-389 [ledger L400, App.A L108] U15 (Should): a verdict-bearing exit code for merge | same destination CORE -> REPRESENTED
390. VL-19-390 [ledger L401, App.A L109] U16 (Should): telemetry written by the product (requested and observed... | same destination CORE -> REPRESENTED
391. VL-19-391 [ledger L402, App.A L110] U17 (Should): a per-reviewer model override at resolve time (SPEC:26 j... | same destination CORE -> REPRESENTED
392. VL-19-392 [ledger L403, App.A L1890] U18 (Should): regression benchmark of 3 packages plus ground truth plu... | same destination EVAL -> REPRESENTED
393. VL-19-393 [ledger L404, App.A L4241] Gap: finding-shape coexistence or mapping; run-1 requirement 1 dropped... | same destination DROP -> REPRESENTED
394. VL-19-394 [ledger L405, App.A L4242] Gap: reviewer isolation; run-1 requirement 9 dropped (L7) | same destination DROP -> REPRESENTED
395. VL-19-395 [ledger L406, App.A L4243] Gap: position of the calibration and validation gate in the shared pip... | same destination DROP -> REPRESENTED
396. VL-19-396 [ledger L407, App.A L111] Gap: target-specific lens, ref and category sets (plan, tasklist, spec... | same destination CORE -> REPRESENTED
397. VL-19-397 [ledger L408, App.A L4244] Conflict C-1: length-limit policy; E2 requires no whole-finding drop (... | same destination DROP -> REPRESENTED
398. VL-19-398 [ledger L409, App.A L4245] Conflict C-2: run-1 D14 "tasklist review does not exist in the workflo... | same destination DROP -> REPRESENTED
399. VL-19-399 [ledger L410, App.A L4246] Conflict C-3: where tasklist review should run: the spec-panel loop pl... | same destination DROP -> REPRESENTED
400. VL-19-400 [ledger L411, App.A L112] Conflict C-4: blocking semantics: reviewer-asserted `blocking` (any si... | same destination CORE -> REPRESENTED
401. VL-19-401 [ledger L412, App.A L4247] Conflict C-5: model identity source: E1 shadow copies `model:` from th... | same destination DROP -> REPRESENTED
402. VL-19-402 [ledger L413, App.A L4248] Conflict C-6: model registry: tier JSON versus `ANTHROPIC_DEFAULT_*_MO... | same destination DROP -> REPRESENTED
403. VL-19-403 [ledger L414, App.A L113] Conflict C-7: panel defaults: E2 DM14 recommends cheap non-Claude pane... | same destination CORE -> REPRESENTED
404. VL-19-404 [ledger L415, App.A L4249] Conflict C-8: run-2 and cmp:22 attribute the 40-file change to #519 pl... | same destination DROP -> REPRESENTED
405. VL-19-405 [ledger L416, App.A L4250] Conflict C-9: per-model drop counts presented as blocking-finding loss... | same destination DROP -> REPRESENTED
406. VL-19-406 [ledger L417, App.A L3680] Conflict C-10: `HANDOFF-run1-vs-run2.md` says run-2 "catches four fact... | same destination KNOWLEDGE -> REPRESENTED
407. VL-19-407 [ledger L418, App.A L4251] Conflict C-11: evidence retention: DM16 raw transcripts left out versu... | same destination DROP -> REPRESENTED
408. VL-19-408 [ledger L419, App.A L4252] Conflict C-12: E2 workers "change nothing under `.dev/tasks/`" (DM17) ... | same destination DROP -> REPRESENTED
409. VL-19-409 [ledger L420, App.A L1632] Exposure, spec review: the brief and loop are spec-native (`prompts:3`... | same destination MODULE-spec -> REPRESENTED
410. VL-19-410 [ledger L421, App.A L4253] Exposure, tasklist or plan review: D7 task ids lost, B-1 no source, re... | same destination DROP -> REPRESENTED
411. VL-19-411 [ledger L422, App.A L1700] Exposure, PR code review: v2 `citations` has `diff` and `test` roles a... | same destination MODULE-pr-review -> REPRESENTED
412. VL-19-412 [ledger L423, App.A L1701] Exposure, PR code review: exact-quote anchors flatten whitespace, so c... | same destination MODULE-pr-review -> REPRESENTED
413. VL-19-413 [ledger L424, App.A L4254] Exposure, PR code review: the reviewer-isolation sandbox pattern (`man... | same destination DROP -> REPRESENTED
414. VL-19-414 [ledger L425, App.A L1702] Exposure, PR code review: there is no calibrator in the v1 loop, and 1... | same destination MODULE-pr-review -> REPRESENTED
415. VL-19-415 [ledger L426, App.A L1749] Exposure, rf-qa replacement: the review loop's re-check defers to the ... | same destination MODULE-rfqa -> REPRESENTED
416. VL-19-416 [ledger L427, App.A L1750] Exposure, rf-qa replacement: re-review collapses to one anchor reviewe... | same destination MODULE-rfqa -> REPRESENTED
417. VL-19-417 [ledger L428, App.A L114] Exposure, any new target: ref syntax (`_REF_TOKEN`, `telemetry.py:23`)... | same destination CORE -> REPRESENTED
418. VL-19-418 [ledger L429, App.A L4255] Exposure, any new target: model recommendations (DM14) do not transfer... | same destination DROP -> REPRESENTED
419. VL-19-419 [ledger L430, App.A L4256] Exposure, any new target: telemetry strata are hard-coded to sonnet an... | same destination DROP -> REPRESENTED
420. VL-19-420 [ledger L431, App.A L4257] Summary: run-2 (543 lines) is a single-author, independently written, ... | same destination DROP -> REPRESENTED
421. VL-19-421 [ledger L432, App.A L4258] Summary counts: 11 form differences, 15 corrections, 12 dropped run-1 ... | same destination DROP -> REPRESENTED
422. VL-19-422 [ledger L433, App.A L4259] Code verdict at HEAD: all of D1-D13, P1-P7, T1-T2 and B-1..B-7 are VER... | same destination DROP -> REPRESENTED
423. VL-19-423 [ledger L434, App.A L4260] Hand-off error (1): run-2 and cmp:22 attribute the `RV` changes to #51... | same destination DROP -> REPRESENTED
424. VL-19-424 [ledger L435, App.A L4261] Hand-off error (2): run-2 "106 row folders" under `combos/` versus 96 ... | same destination DROP -> REPRESENTED
425. VL-19-425 [ledger L436, App.A L4262] Hand-off error (3): run-2 "55 files + README" versus 55 files includin... | same destination DROP -> REPRESENTED
426. VL-19-426 [ledger L437, App.A L4263] Hand-off error (4): "4 verdict flips" not reproduced by audit-D:20 (3 ... | same destination DROP -> REPRESENTED
427. VL-19-427 [ledger L438, App.A L4264] Hand-off error (5): per-model drop counts shown next to "49 blocking l... | same destination DROP -> REPRESENTED
428. VL-19-428 [ledger L439, App.A L4265] Hand-off error (6): run-1 "alias GT3 found once" is wrong (B6 = alias ... | same destination DROP -> REPRESENTED
429. VL-19-429 [ledger L440, App.A L4266] Hand-off error (7): run-1 D14 first half is contradicted by `sc-workfl... | same destination DROP -> REPRESENTED
430. VL-19-430 [ledger L441, App.A L4267] Hand-off error (8): run-2's reflect contrast (5.6) and Q4/Q9 are STALE... | same destination DROP -> REPRESENTED
431. VL-19-431 [ledger L442, App.A L4268] Architecture signal: both hand-offs agree the generic merge/ledger/pan... | same destination DROP -> REPRESENTED
432. VL-19-432 [ledger L443, App.A L4269] Gap G1: the raw notes `handoff-notes/run1/*.md` and `run2/*.md` (118 K... | same destination DROP -> REPRESENTED
433. VL-19-433 [ledger L444, App.A L4270] Gap G2: `ledger revise` double-apply (D11) verified by reading, not ex... | same destination DROP -> REPRESENTED
434. VL-19-434 [ledger L445, App.A L1891] Gap G3: `findings_v2.py` bodies beyond lines 1-149, `cluster.py` bodie... | same destination EVAL -> REPRESENTED
435. VL-19-435 [ledger L446, App.A L4271] Gap G4: run-2's "26 of 40 `@live7` run ids hold a duplicate" not repro... | same destination DROP -> REPRESENTED
436. VL-19-436 [ledger L447, App.A L1892] Gap G5: E2 data claims only spot-checked (COMBO-REPORT lines 105-107, ... | same destination EVAL -> REPRESENTED
437. VL-19-437 [ledger L448, App.A L4272] Gap G6: "branch changes no product code" for E2 was not re-run on the ... | same destination DROP -> REPRESENTED
438. VL-19-438 [ledger L449, App.A L3681] Gap G7: run-2 session-record claims (DM1, DM7, DM12 quote, DM16, DM18;... | same destination KNOWLEDGE -> REPRESENTED
439. VL-19-439 [ledger L450, App.A L4273] Gap G8: orchestrator and model claims in cmp:8-9 (Tier 1b Sonnet versu... | same destination DROP -> REPRESENTED
440. VL-19-440 [ledger L451, App.A L4274] Gap G9: E3 is nearly absent from run-2; the slice confirmed placement ... | same destination DROP -> REPRESENTED
441. VL-19-441 [ledger L452, App.A L4275] Gap G10: the "tasklist-specific?" verdicts (run2:395-406) were not re-... | same destination DROP -> REPRESENTED
442. VL-19-442 [ledger L453, App.A L3682] Question Q-A: treat run-2 as the baseline hand-off with the 3.2 and 3.... | same destination KNOWLEDGE -> REPRESENTED
443. VL-19-443 [ledger L454, App.A L4276] Question Q-B: is the E2 tip's post-hand-off material (`panel-process-r... | same destination DROP -> REPRESENTED
444. VL-19-444 [ledger L455, App.A L115] Question Q-C: should the report assert D1 as already present in E1's f... | same destination CORE -> REPRESENTED
445. VL-19-445 [ledger L456, App.A L4277] Question Q-D: is a like-for-like run of reflect UC-1 (calibrator plus ... | same destination DROP -> REPRESENTED
446. VL-19-446 [ledger L457, App.A L4278] Question Q-E: identity policy (C-5): should the shared core record bot... | same destination DROP -> REPRESENTED
447. VL-19-447 [ledger L458, App.A L4279] Question Q-F: who owns `muse-ember-1.0` in tier data (the owner said "... | same destination DROP -> REPRESENTED
448. VL-19-448 [ledger L459, App.A L3683] Question Q-G: should the 3.2 corrections (C1, C15) and the 3.6 rows (8... | same destination KNOWLEDGE -> REPRESENTED
449. VL-19-449 [ledger L460, App.A L4280] Slice-02 tip read: `6c0984326cbb8fb06c4a36065de58b171d3f8175`, 2026-11... | same destination DROP -> REPRESENTED
450. VL-19-450 [ledger L461, App.A L3684] Commits after run-1 commit 4a22d7421: c2ddeb1b4 (2026-11-13 16:17:36, ... | same destination KNOWLEDGE -> REPRESENTED
451. VL-19-451 [ledger L462, App.A L3685] Material sizes at the tip: HO 67 lines; R1CM 66; R1CP 100; R1TT 13; R2... | same destination KNOWLEDGE -> REPRESENTED
452. VL-19-452 [ledger L463, App.A L4281] Run reports: run-1 is 315 lines (HO says 315); run-2 is 543 by `wc -l`... | same destination DROP -> REPRESENTED
453. VL-19-453 [ledger L464, App.A L3686] The E2 files exist only at the tip; `ls .dev/eval-workspaces/tasklist-... | same destination KNOWLEDGE -> REPRESENTED
454. VL-19-454 [ledger L465, App.A L3687] Merge-base of HEAD and the E2 tip is `ec259f1b718ccdb9f08bba0237bfa47b... | same destination KNOWLEDGE -> REPRESENTED
455. VL-19-455 [ledger L466, App.A L4282] Master relation: `git rev-list --count ec259f1b7..origin/master` = 11 ... | same destination DROP -> REPRESENTED
456. VL-19-456 [ledger L467, App.A L3688] Dates inside the notes: R1CM and R1CP "Read 2026-11-13"; R2CM "verifie... | same destination KNOWLEDGE -> REPRESENTED
457. VL-19-457 [ledger L468, App.A L4283] Independence statements: R2CM:6 and R2CP:5 say neither opened `/tmp/ha... | same destination DROP -> REPRESENTED
458. VL-19-458 [ledger L469, App.A L3689] HO H1: the same brief both times (the `/tech-research` hand-off prompt... | same destination KNOWLEDGE -> REPRESENTED
459. VL-19-459 [ledger L470, App.A L4284] HO H2: run 1 was a Sonnet 5.5 Tier 1b orchestrator writing with the wh... | same destination DROP -> REPRESENTED
460. VL-19-460 [ledger L471, App.A L4285] HO H3: run 2 was an Opus 5.5 Tier 1a orchestrator with all agents pinn... | same destination DROP -> REPRESENTED
461. VL-19-461 [ledger L472, App.A L4286] HO H4: neither run used the full tech-research task-file machinery [UN... | same destination DROP -> REPRESENTED
462. VL-19-462 [ledger L473, App.A L4287] HO H5: lengths 315 and 544 lines | same destination DROP -> REPRESENTED
463. VL-19-463 [ledger L474, App.A L3690] HO H6: "Use run 2 as the main hand-off", run 2 catches four facts run ... | same destination KNOWLEDGE -> REPRESENTED
464. VL-19-464 [ledger L475, App.A L3691] HO H7: "Each claim below was checked against the source" is partly fal... | same destination KNOWLEDGE -> REPRESENTED
465. VL-19-465 [ledger L476, App.A L4288] HO row 1 "master has moved": the same `git diff --stat ec259f1b7 origi... | same destination DROP -> REPRESENTED
466. VL-19-466 [ledger L477, App.A L4289] HO row 1 code facts at HEAD [V]: `findings_v2.py` anchor/anchor2/citat... | same destination DROP -> REPRESENTED
467. VL-19-467 [ledger L478, App.A L4290] HO row 1 impact "run 1's defect list cites stale line numbers": `git d... | same destination DROP -> REPRESENTED
468. VL-19-468 [ledger L479, App.A L3692] HO row 1 attribution: R2CP:121 says only "#519 ... may overlap the uni... | same destination KNOWLEDGE -> REPRESENTED
469. VL-19-469 [ledger L480, App.A L4291] HO row 2 where tasklist review runs: at HEAD workflow Wave 4 heading `... | same destination DROP -> REPRESENTED
470. VL-19-470 [ledger L481, App.A L1289] A narrow grep (`superclaude review`, `review_ledger`, `review loop`) i... | same destination MODULE-tasklist -> REPRESENTED
471. VL-19-471 [ledger L482, App.A L4292] HO row 3 audit summaries: only audit-A and audit-D have `summary.md`; ... | same destination DROP -> REPRESENTED
472. VL-19-472 [ledger L483, App.A L3194] HO row 4 helper scripts: `snap.py:4` is `open("/home/coder/workspaces/... | same destination HARNESS -> REPRESENTED
473. VL-19-473 [ledger L484, App.A L3195] HO says 3 scripts reference the other eval; R2TT:67 names 4, adding `b... | same destination HARNESS -> REPRESENTED
474. VL-19-474 [ledger L485, App.A L4293] HO row 5 harness bugs [V] at the tip: `run-reviewer.sh:76` `MODEL="$NE... | same destination DROP -> REPRESENTED
475. VL-19-475 [ledger L486, App.A L3693] HO claims run 1 "described the ladder as fixed"; R1TT:9 describes the ... | same destination KNOWLEDGE -> REPRESENTED
476. VL-19-476 [ledger L487, App.A L3196] HO row 6 raw-file count: R1TT:11 and R2TT:125-128 agree on 1380 `*.att... | same destination HARNESS -> REPRESENTED
477. VL-19-477 [ledger L488, App.A L3197] At the tip `git ls-tree -r <tip>` finds 0 files matching `attempt[0-9]... | same destination HARNESS -> REPRESENTED
478. VL-19-478 [ledger L489, App.A L4294] HO row 7 reproducibility: `final-table.py:23` reads `/tmp/audit-{k}/fl... | same destination DROP -> REPRESENTED
479. VL-19-479 [ledger L490, App.A L4295] HO row 8 test count: 299 + 5 (`test_review_brief_placement` has 5 test... | same destination DROP -> REPRESENTED
480. VL-19-480 [ledger L491, App.A L4296] HO H8 retractions: the run-2 report's table lists numbers that must no... | same destination DROP -> REPRESENTED
481. VL-19-481 [ledger L492, App.A L3694] HO H9: merge defects split finer (D4, D5 separate; 46 rows with 13 blo... | same destination KNOWLEDGE -> REPRESENTED
482. VL-19-482 [ledger L493, App.A L116] HO H10 re-run at HEAD: `review panel resolve --template @live7 --env g... | same destination CORE -> REPRESENTED
483. VL-19-483 [ledger L494, App.A L4297] HO H11 brief versus parser: `RP:60` at HEAD states anchor "12 to 200 c... | same destination DROP -> REPRESENTED
484. VL-19-484 [ledger L495, App.A L4298] HO H12: 18 requirements U1-U18 with must/should [UNVERIFIED]; regressi... | same destination DROP -> REPRESENTED
485. VL-19-485 [ledger L496, App.A L4299] HO H13: decision log DM1-DM18 with dates and 11 open decisions with ow... | same destination DROP -> REPRESENTED
486. VL-19-486 [ledger L497, App.A L4300] HO H14: Q1-Q3 aimed at #519; answered at HEAD: Q1 yes, `findings_v2` s... | same destination DROP -> REPRESENTED
487. VL-19-487 [ledger L498, App.A L4301] HO H15: `lint_cmd` and `estimate_cmd` are registered but missing; `Mod... | same destination DROP -> REPRESENTED
488. VL-19-488 [ledger L499, App.A L4302] HO H16: review-ledger skill, `spec-panel-ledger`/`-stoprule` commands ... | same destination DROP -> REPRESENTED
489. VL-19-489 [ledger L500, App.A L4303] HO H17: keep the one-table model-by-role summary (tier part `R1CP:22-3... | same destination DROP -> REPRESENTED
490. VL-19-490 [ledger L501, App.A L1893] HO H18 overstatement: `COMBO-REPORT.md:373` says "The cause (the brief... | same destination EVAL -> REPRESENTED
491. VL-19-491 [ledger L502, App.A L4304] HO H18 other agreement items: ceiling about 2-2.5/14; default ember + ... | same destination DROP -> REPRESENTED
492. VL-19-492 [ledger L503, App.A L3198] HO H19 recommended action: give the other session run 2 plus HO sectio... | same destination HARNESS -> REPRESENTED
493. VL-19-493 [ledger L504, App.A L4305] X1 tasklist review today: run-1 notes say "NO tasklist review step in ... | same destination DROP -> REPRESENTED
494. VL-19-494 [ledger L505, App.A L4306] X2 `T2bModel01`: R2CP:56 "NOT referenced anywhere in src/ or tests/ ..... | same destination DROP -> REPRESENTED
495. VL-19-495 [ledger L506, App.A L117] X3 anchor-not-found severity: R1CM:52 MED and :58 LOW versus R2CM D4 H... | same destination CORE -> REPRESENTED
496. VL-19-496 [ledger L507, App.A L4307] X4 docstring versus clearing: docstring `L:112` is false, loop `L:253-... | same destination DROP -> REPRESENTED
497. VL-19-497 [ledger L508, App.A L4308] X5 severity of silent drops: R1CM:51 HIGH and R1CM:19 "Not silent in c... | same destination DROP -> REPRESENTED
498. VL-19-498 [ledger L509, App.A L118] X6 ref-mismatch split: `_REF_TOKEN` (`F:29`) scrapes tokens such as "U... | same destination CORE -> REPRESENTED
499. VL-19-499 [ledger L510, App.A L4309] X7 revise integrity: `apply_revision` (`L:301-347`) records no revisio... | same destination DROP -> REPRESENTED
500. VL-19-500 [ledger L511, App.A L3695] X8 number of code defects: R1CM 13, R1CP 16, R1TT none versus R2CM 23 ... | same destination KNOWLEDGE -> REPRESENTED
501. VL-19-501 [ledger L512, App.A L1007] X9 `reflect-reviewer.md` frontmatter at HEAD (file unchanged vs base):... | same destination MODULE-reflect -> REPRESENTED
502. VL-19-502 [ledger L513, App.A L4310] X10 run-1 quote of `MODEL-TIERS.md:42` "if Terra returns 429 retried o... | same destination DROP -> REPRESENTED
503. VL-19-503 [ledger L514, App.A L3696] Current Tier 2b rule at HEAD (`MODEL-TIERS.md:44`, "owner, 2026-11-12"... | same destination KNOWLEDGE -> REPRESENTED
504. VL-19-504 [ledger L515, App.A L1008] X11 reflect SKILL line cites: `SKILL.md` has +68 lines at HEAD (shadow... | same destination MODULE-reflect -> REPRESENTED
505. VL-19-505 [ledger L516, App.A L119] X12 panel resolve outputs: random slots depend on the run id; at HEAD ... | same destination CORE -> REPRESENTED
506. VL-19-506 [ledger L517, App.A L120] X13 slot variables: HEAD `P:486-492` `select_env` reads `T3Model01`; t... | same destination CORE -> REPRESENTED
507. VL-19-507 [ledger L518, App.A L4311] A1 (agreed by both note sets): the parser accepts exactly a `findings-... | same destination DROP -> REPRESENTED
508. VL-19-508 [ledger L519, App.A L4312] A2: drop rules drop one line and set the reviewer `ok=False`; merge re... | same destination DROP -> REPRESENTED
509. VL-19-509 [ledger L520, App.A L4313] A3: the verdict uses only the reviewer `blocking` flag; no quorum; `co... | same destination DROP -> REPRESENTED
510. VL-19-510 [ledger L521, App.A L4314] A4a: `--cap` is ignored on an existing ledger (`M:62-69, 100-108` [V]) | same destination DROP -> REPRESENTED
511. VL-19-511 [ledger L522, App.A L121] A4b: `--round` has no upper bound: the help says "1, 2 or 3" but the o... | same destination CORE -> REPRESENTED
512. VL-19-512 [ledger L523, App.A L4315] A5: `unpassable-ac` is not an accepted category, only `unpassable-chec... | same destination DROP -> REPRESENTED
513. VL-19-513 [ledger L524, App.A L4316] A6: `T01.02`-style task ids are not extracted as refs (run 1 inferred,... | same destination DROP -> REPRESENTED
514. VL-19-514 [ledger L525, App.A L4317] A7: telemetry is written by nothing in the product | same destination DROP -> REPRESENTED
515. VL-19-515 [ledger L526, App.A L4318] A8: the brief has no source or driving-document placeholder, only `{{C... | same destination DROP -> REPRESENTED
516. VL-19-516 [ledger L527, App.A L4319] A9: `distinct_across_slots` silently falls back to duplicates | same destination DROP -> REPRESENTED
517. VL-19-517 [ledger L528, App.A L4320] A10: there is no calibrator in the review panel; reflect has the blind... | same destination DROP -> REPRESENTED
518. VL-19-518 [ledger L529, App.A L4321] A11: the gateway `launch` map is empty and dispatch is undefined (note... | same destination DROP -> REPRESENTED
519. VL-19-519 [ledger L530, App.A L4322] A12: telemetry strata are hard-coded `sonnet`/`haiku` (`T:111-115`, `T... | same destination DROP -> REPRESENTED
520. VL-19-520 [ledger L531, App.A L4323] A13: re-review resolves to the single fixed anchor (`apply_to ["first"... | same destination DROP -> REPRESENTED
521. VL-19-521 [ledger L532, App.A L4324] A14: nothing in `cli/review` is tasklist-specific; `grep tasklist` has... | same destination DROP -> REPRESENTED
522. VL-19-522 [ledger L533, App.A L4325] A15: untracked counts 1380 attempt json + 1352 meta + 309 judge/other ... | same destination DROP -> REPRESENTED
523. VL-19-523 [ledger L534, App.A L3199] A16: `run-reviewer.sh` has a ladder map with 2 attempts per model, `EX... | same destination HARNESS -> REPRESENTED
524. VL-19-524 [ledger L535, App.A L4326] K-1: run-1 tests note said "no dedicated boundary test" and "no claim ... | same destination DROP -> REPRESENTED
525. VL-19-525 [ledger L536, App.A L4327] K-2: R1CP:6 `lint_cmd`/`estimate_cmd` "DO NOT EXIST" and R1CP:82 "docs... | same destination DROP -> REPRESENTED
526. VL-19-526 [ledger L537, App.A L4328] K-3: R2TT:47 notes the `manifest.md` line "Worktree branch: ... (local... | same destination DROP -> REPRESENTED
527. VL-19-527 [ledger L538, App.A L4329] K-4: the `T01.02` regex gap, marked UNVERIFIED by run 1, is upgraded t... | same destination DROP -> REPRESENTED
528. VL-19-528 [ledger L539, App.A L122] K-5: R2CP:56 observed live that with `T3Model01=glm-5.3` the `@default... | same destination CORE -> REPRESENTED
529. VL-19-529 [ledger L540, App.A L4330] Numbering hazard: HO cites D-, P-, B-, K-, Q-, U-, DM-, DO- numbers of... | same destination DROP -> REPRESENTED
530. VL-19-530 [ledger L541, App.A L4331] Number map: partial-panel failure invisible is R2CM D1 and report D2 | same destination DROP -> REPRESENTED
531. VL-19-531 [ledger L542, App.A L4332] Number map: docstring says skipped for clearing is R2CM D2 and report ... | same destination DROP -> REPRESENTED
532. VL-19-532 [ledger L543, App.A L4333] Number map: ref mismatch splits one defect is R2CM D3 and report D5 | same destination DROP -> REPRESENTED
533. VL-19-533 [ledger L544, App.A L4334] Number map: anchor not found and never refound is R2CM D4 and report D... | same destination DROP -> REPRESENTED
534. VL-19-534 [ledger L545, App.A L4335] Number map: over-merging or chaining is R2CM D5 and report D4 | same destination DROP -> REPRESENTED
535. VL-19-535 [ledger L546, App.A L4336] Number map: first-row-only match (`break`) is R2CM D6 and report D10 | same destination DROP -> REPRESENTED
536. VL-19-536 [ledger L547, App.A L4337] Number map: revise twice and new-text hash are R2CM D7, D8 and report ... | same destination DROP -> REPRESENTED
537. VL-19-537 [ledger L548, App.A L4338] Number map: drop for limits not in prompt is R2CM D9 and folded into r... | same destination DROP -> REPRESENTED
538. VL-19-538 [ledger L549, App.A L4339] Number map: `merge` exit code always 0 is R2CM D11 and report D12 | same destination DROP -> REPRESENTED
539. VL-19-539 [ledger L550, App.A L4340] Number map: refound row takes the current round's blocking is R2CP def... | same destination DROP -> REPRESENTED
540. VL-19-540 [ledger L551, App.A L4341] Number map: task ids not refs is R2CP defect 2 and report D7 | same destination DROP -> REPRESENTED
541. VL-19-541 [ledger L552, App.A L4342] Number map: any single blocker fails is R2CP defect 5 and report D8 | same destination DROP -> REPRESENTED
542. VL-19-542 [ledger L553, App.A L3697] Rule from the hazard: cite a defect by file:line, or by (document, id)... | same destination KNOWLEDGE -> REPRESENTED
543. VL-19-543 [ledger L554, App.A L4343] Base check: `findings.py` (457 lines), `ledger.py` (494), `ledger_cmd.... | same destination DROP -> REPRESENTED
544. VL-19-544 [ledger L555, App.A L123] F1: `SEVERITIES = (CRITICAL, MAJOR, MINOR)`, case-sensitive; no MEDIUM... | same destination CORE -> REPRESENTED
545. VL-19-545 [ledger L556, App.A L124] F2: `CATEGORIES` = contradiction, unpassable-check, data-loss, safety,... | same destination CORE -> REPRESENTED
546. VL-19-546 [ledger L557, App.A L1290] F2 note: the tasklist module needs its own categories (coverage, trace... | same destination MODULE-tasklist -> REPRESENTED
547. VL-19-547 [ledger L558, App.A L125] F3: `PRIOR_STATUSES` resolved/open/regressed and `ACTIONS` applied/rej... | same destination CORE -> REPRESENTED
548. VL-19-548 [ledger L559, App.A L126] F4: id regex `^[A-Za-z0-9][A-Za-z0-9._-]{0,15}$`, 16 characters maximu... | same destination CORE -> REPRESENTED
549. VL-19-549 [ledger L560, App.A L4344] F5: `_FENCE` takes a single-token info string; `~~~` and triple-backti... | moved CORE -> DROP (recorded: DROP[duplicate]: duplicate of DR-057; was CORE: the defect r) -> REPRESENTED
550. VL-19-550 [ledger L561, App.A L4345] F6: `_HEAD_FINDINGS` is `^#{1,6}\s+Findings block\s*$`, any heading le... | same destination DROP -> REPRESENTED
551. VL-19-551 [ledger L562, App.A L127] F7: block scan runs from the line after the heading to EOF, collects e... | same destination CORE -> REPRESENTED
552. VL-19-552 [ledger L563, App.A L4346] F8: no heading gives ok False; heading but no block gives ok False; mo... | same destination DROP -> REPRESENTED
553. VL-19-553 [ledger L564, App.A L128] F9: one JSON object per line; blank lines skipped; non-JSON or non-dic... | same destination CORE -> REPRESENTED
554. VL-19-554 [ledger L565, App.A L4347] F10: finding checks run in order id, duplicate id, severity, bool bloc... | same destination DROP -> REPRESENTED
555. VL-19-555 [ledger L566, App.A L4348] F10 detail (R2CM D22): the claim has no minimum length, so an empty cl... | moved CORE -> DROP (recorded: DROP[duplicate]: duplicate of DR-060; was CORE: the defect r) -> REPRESENTED
556. VL-19-556 [ledger L567, App.A L4349] F11: unknown extra keys are accepted silently and a reviewer-supplied ... | same destination DROP -> REPRESENTED
557. VL-19-557 [ledger L568, App.A L129] F12: `prior` lines need a non-empty id and a status in `PRIOR_STATUSES... | same destination CORE -> REPRESENTED
558. VL-19-558 [ledger L569, App.A L130] F13: length is counted after whitespace flattening (`flat()`), so a lo... | same destination CORE -> REPRESENTED
559. VL-19-559 [ledger L570, App.A L131] F14: `locate` is a whitespace-flattened exact substring match over all... | same destination CORE -> REPRESENTED
560. VL-19-560 [ledger L571, App.A L4350] F15: `anchor_status` and `anchor_ambiguous` are read by nothing in `sr... | same destination DROP -> REPRESENTED
561. VL-19-561 [ledger L572, App.A L4351] F16: a missing anchor gives `span None`, `section "none"`, the finding... | same destination DROP -> REPRESENTED
562. VL-19-562 [ledger L573, App.A L4352] F17: `refs_norm` matches `_REF_TOKEN` in anchor, anchor2, claim and re... | moved CORE -> DROP (recorded: DROP[duplicate]: duplicate of DR-061; was CORE: the defect r) -> REPRESENTED
563. VL-19-563 [ledger L574, App.A L132] F18: the fingerprint is `fp = sha256("v1\|section\|refs")[:16]` (`F:34... | same destination CORE -> REPRESENTED
564. VL-19-564 [ledger L575, App.A L4353] F19: `same_defect` says same when the fingerprint is equal and `refs_n... | same destination DROP -> REPRESENTED
565. VL-19-565 [ledger L576, App.A L133] F20: `fixmap-v1` is JSON lines `{id, action, reason}`; the fallback ta... | same destination CORE -> REPRESENTED
566. VL-19-566 [ledger L577, App.A L4354] F21: line-model mismatch: `locate` counts `\n` (`F:295-296`) and `_blo... | moved CORE -> DROP (recorded: DROP[duplicate]: duplicate of DR-056; was CORE: the defect r) -> REPRESENTED
567. VL-19-567 [ledger L578, App.A L1291] R-1: `_REF_TOKEN` needs `LETTERS-DIGITS(.DIGITS)*` or `P<digit>`; task... | same destination MODULE-tasklist -> REPRESENTED
568. VL-19-568 [ledger L579, App.A L1292] R-2: a direct call at HEAD of `annotate(...)` with refs `["T01.02","R-... | same destination MODULE-tasklist -> REPRESENTED
569. VL-19-569 [ledger L580, App.A L134] R-3: telemetry has the same regex shape (`T:23-24` `_ID_TOKEN`), so `i... | same destination CORE -> REPRESENTED
570. VL-19-570 [ledger L581, App.A L4355] R-4: consequence: tasklist findings fall back to span-proximity cluste... | same destination DROP -> REPRESENTED
571. VL-19-571 [ledger L582, App.A L135] Design destination: CORE must take the id grammar from a document-type... | same destination CORE -> REPRESENTED
572. VL-19-572 [ledger L583, App.A L4356] G1: each failed rule drops ONLY that line (`continue`) and sets the wh... | same destination DROP -> REPRESENTED
573. VL-19-573 [ledger L584, App.A L136] G2: rules that drop a line: not JSON; not object; bad prior; id over 1... | same destination CORE -> REPRESENTED
574. VL-19-574 [ledger L585, App.A L4357] G3: one warning per reviewer carries the error count and ONLY the firs... | same destination DROP -> REPRESENTED
575. VL-19-575 [ledger L586, App.A L137] G4: valid findings of a reviewer with a bad block are still merged (`L... | same destination CORE -> REPRESENTED
576. VL-19-576 [ledger L587, App.A L4358] G5: merge refuses only when NO reviewer has `ok=True`; the ledger is l... | same destination DROP -> REPRESENTED
577. VL-19-577 [ledger L588, App.A L4359] G6: a reviewer whose only blocking finding is dropped for length can s... | same destination DROP -> REPRESENTED
578. VL-19-578 [ledger L589, App.A L4360] G7: the docstring `L:112` ("skipped for clearing") is false and the cl... | same destination DROP -> REPRESENTED
579. VL-19-579 [ledger L590, App.A L4361] G8: drop evidence at study scale: 80 reviewer-level cases, "49 blockin... | same destination DROP -> REPRESENTED
580. VL-19-580 [ledger L591, App.A L4362] G9: `missing-requirement` is Medium (non-blocking) by instruction `RP:... | same destination DROP -> REPRESENTED
581. VL-19-581 [ledger L592, App.A L138] L1: `merge` options are `--ledger` (created at round 1), `--doc`, `--r... | same destination CORE -> REPRESENTED
582. VL-19-582 [ledger L593, App.A L4363] L2: a reviewer missing from the resolution gets `model None` silently;... | same destination DROP -> REPRESENTED
583. VL-19-583 [ledger L594, App.A L139] L3: a malformed resolution raises a ClickException "`{resolution} is n... | same destination CORE -> REPRESENTED
584. VL-19-584 [ledger L595, App.A L4364] L4: `merge_round` requires round = `len(rounds)+1`, refuses duplicate ... | same destination DROP -> REPRESENTED
585. VL-19-585 [ledger L596, App.A L4365] L5: `merge_round` clusters all findings of all reviewers; each cluster... | same destination DROP -> REPRESENTED
586. VL-19-586 [ledger L597, App.A L4366] L6: a new row takes fp, anchor, span, claim and category from the FIRS... | same destination DROP -> REPRESENTED
587. VL-19-587 [ledger L598, App.A L4367] L7: a refound row appends members; `blocking` is THIS round's classifi... | same destination DROP -> REPRESENTED
588. VL-19-588 [ledger L599, App.A L4368] L8: because a refound `blocking` is the current round's call, a review... | same destination DROP -> REPRESENTED
589. VL-19-589 [ledger L600, App.A L140] L9: `resolved_check` rows not refound this round become `resolved` wit... | same destination CORE -> REPRESENTED
590. VL-19-590 [ledger L601, App.A L141] L10: `prior` lines only append history `prior_note`; an unknown prior ... | same destination CORE -> REPRESENTED
591. VL-19-591 [ledger L602, App.A L142] L11: `brief_ids` = rows with `blocking` AND status in (open, regressed... | same destination CORE -> REPRESENTED
592. VL-19-592 [ledger L603, App.A L4369] L12: severity does not affect the verdict (only MINOR plus blocking is... | same destination DROP -> REPRESENTED
593. VL-19-593 [ledger L604, App.A L4370] L13: `--out` is written first (not atomic: `makedirs` then plain `open... | moved CORE -> DROP (recorded: DROP[duplicate]: duplicate of DR-059; was CORE: the defect r) -> REPRESENTED
594. VL-19-594 [ledger L605, App.A L4371] L14: `merge` always exits 0; only `ledger verdict` maps decisions to e... | same destination DROP -> REPRESENTED
595. VL-19-595 [ledger L606, App.A L4372] L15: the merged report has the header `review: n of cap`, reviewers wi... | moved CORE -> DROP (recorded: DROP[duplicate]: duplicate of DR-055; was CORE: the defect r) -> REPRESENTED
596. VL-19-596 [ledger L607, App.A L4373] L16: `ledger revise` needs a merged round; `--old` sha256 must match t... | same destination DROP -> REPRESENTED
597. VL-19-597 [ledger L608, App.A L4374] L17: `defer` sets any status to `deferred` and removes the lid from th... | moved CORE -> DROP (recorded: DROP[duplicate]: duplicate of DR-053; was CORE: the defect r) -> REPRESENTED
598. VL-19-598 [ledger L609, App.A L4375] L18: `verdict` returns the last round's stored verdict, decision and b... | same destination DROP -> REPRESENTED
599. VL-19-599 [ledger L610, App.A L143] L19: `capture` exports `review-capture/1` (defects by reviewers, `capt... | same destination CORE -> REPRESENTED
600. VL-19-600 [ledger L611, App.A L4376] L20: ledger schema `review-ledger/1` {schema, doc, cap_reviews, rounds... | same destination DROP -> REPRESENTED
601. VL-19-601 [ledger L612, App.A L4377] L21: a missing-anchor blocking row stays open until a human defers and... | same destination DROP -> REPRESENTED
602. VL-19-602 [ledger L613, App.A L4378] L22: "verify-only" rounds 2-3 are not a code mode: any report in any r... | same destination DROP -> REPRESENTED
603. VL-19-603 [ledger L614, App.A L4379] Generic-versus-specific: all of `cli/review` (findings, merge, ledger,... | same destination DROP -> REPRESENTED
604. VL-19-604 [ledger L615, App.A L144] Spec-shaped assumptions in the code: category names, `REVISER_RULES` t... | same destination CORE -> REPRESENTED
605. VL-19-605 [ledger L616, App.A L145] The only coupling of the code to documents is the findings-v1 and fixm... | same destination CORE -> REPRESENTED
606. VL-19-606 [ledger L617, App.A L4380] HEAD differs from the runs' base: `panel.py` 525 to 707 (+194/-12), `p... | same destination DROP -> REPRESENTED
607. VL-19-607 [ledger L618, App.A L146] P-1: three schema ids `review-panel/1`, `review-tiers/1`, `review-pane... | same destination CORE -> REPRESENTED
608. VL-19-608 [ledger L619, App.A L147] P-2: panel template keys are a closed set {schema, template_id, versio... | same destination CORE -> REPRESENTED
609. VL-19-609 [ledger L620, App.A L148] P-3: tier file schema: `aliases.<tierN>` {alias, models[], placeholder... | same destination CORE -> REPRESENTED
610. VL-19-610 [ledger L621, App.A L149] P-4: HEAD adds `classes` (model id to class: opus, sonnet, haiku, fabl... | same destination CORE -> REPRESENTED
611. VL-19-611 [ledger L622, App.A L150] P-5a: lookup precedence: explicit path, then `$SUPERCLAUDE_REVIEW_PANE... | same destination CORE -> REPRESENTED
612. VL-19-612 [ledger L623, App.A L151] P-5b: a project or user file silently overrides the packaged default; ... | same destination CORE -> REPRESENTED
613. VL-19-613 [ledger L624, App.A L4381] P-6: no model ids are hard-coded in `panel.py`, only env names `gatewa... | same destination DROP -> REPRESENTED
614. VL-19-614 [ledger L625, App.A L4382] E-1: `select_env` order is `--env`, `$SUPERCLAUDE_REVIEW_ENV`, `gatewa... | same destination DROP -> REPRESENTED
615. VL-19-615 [ledger L626, App.A L152] E-2: `T2bModel01` is never read by panel code; `@live7` needs the `cla... | same destination CORE -> REPRESENTED
616. VL-19-616 [ledger L627, App.A L153] E-3: resolution order is fixed slots first, then others in template or... | same destination CORE -> REPRESENTED
617. VL-19-617 [ledger L628, App.A L154] E-4: `resolve_slot`: candidates are tier models in `available`, none g... | same destination CORE -> REPRESENTED
618. VL-19-618 [ledger L629, App.A L4383] E-5: silent duplicate fallback: when exclusion empties the pool `pool ... | same destination DROP -> REPRESENTED
619. VL-19-619 [ledger L630, App.A L4384] E-6: a fixed slot ignores `exclude` (HEAD: still true unless `strict_d... | moved CORE -> DROP (recorded: DROP[duplicate]: duplicate of DR-071; was CORE: the defect r) -> REPRESENTED
620. VL-19-620 [ledger L631, App.A L4385] E-7: `@live7` gateway duplicates occur in 26 of 40 run ids r1..r40 [V ... | same destination DROP -> REPRESENTED
621. VL-19-621 [ledger L632, App.A L4386] E-8: the gateway `launch` map is empty (note "dispatch mechanism per m... | same destination DROP -> REPRESENTED
622. VL-19-622 [ledger L633, App.A L4387] E-9: `anthropic-only` has available opus, sonnet, haiku, fable 5.x, st... | same destination DROP -> REPRESENTED
623. VL-19-623 [ledger L634, App.A L4388] E-10: `claude-fable-5-1` is in `names`, `available` and `launch` but i... | moved CORE -> DROP (recorded: DROP[duplicate]: duplicate of DR-064; was CORE: the defect r) -> REPRESENTED
624. VL-19-624 [ledger L635, App.A L155] E-11: model-by-tier table: tier1a opus-5-5, sonnet-5-5; tier1b sonnet-... | same destination CORE -> REPRESENTED
625. VL-19-625 [ledger L636, App.A L4389] E-12a: `muse-ember-1.0` (the recommended default panel model) is missi... | same destination DROP -> REPRESENTED
626. VL-19-626 [ledger L637, App.A L4390] E-12b: `run-reviewer.sh` carries a hand-kept ladder map that includes ... | moved HARNESS -> DROP (recorded: DROP[duplicate]: duplicate of DR-070; was HARNESS: the defec) -> REPRESENTED
627. VL-19-627 [ledger L638, App.A L4391] E-13: owner-excluded models (Qwen3.8-max, glm from batch 4) still sit ... | same destination DROP -> REPRESENTED
628. VL-19-628 [ledger L639, App.A L1009] E-14: `cli/reflect/ensemble.py` still reads `T2Model0N` at HEAD (`:7, ... | same destination MODULE-reflect -> REPRESENTED
629. VL-19-629 [ledger L640, App.A L4392] T-1: `@default` has 4 reviewers: t1b x1 fixed, t2 x1 random, t3 x2 ran... | same destination DROP -> REPRESENTED
630. VL-19-630 [ledger L641, App.A L4393] T-2: `@live7` has 7 reviewers (t1b x1 fixed, t2 x1, t2b x1, t3 x2, t4 ... | same destination DROP -> REPRESENTED
631. VL-19-631 [ledger L642, App.A L4394] T-3: the gateway `@live7` `run1` and `@default` `run1` outputs recorde... | same destination DROP -> REPRESENTED
632. VL-19-632 [ledger L643, App.A L3698] T-4: recorded hashes `template_sha256` default `fd2ef963...146ba`, liv... | same destination KNOWLEDGE -> REPRESENTED
633. VL-19-633 [ledger L644, App.A L1010] T-5: HEAD adds `reflect-pre`, `reflect-pre-x2`, `reflect-post`, `refle... | same destination MODULE-reflect -> REPRESENTED
634. VL-19-634 [ledger L645, App.A L156] Y-1: telemetry schema `review-telemetry/1` with kinds `reviewer_run` a... | same destination CORE -> REPRESENTED
635. VL-19-635 [ledger L646, App.A L157] Y-2: `reviewer_run` groups panel{template_id/version/sha256, tiers_ver... | same destination CORE -> REPRESENTED
636. VL-19-636 [ledger L647, App.A L158] Y-3: `outcome` keys reviewer_record_id, truth_basis (catalog-v1, theme... | same destination CORE -> REPRESENTED
637. VL-19-637 [ledger L648, App.A L4395] Y-4: `stratum` is limited to {sonnet, haiku} and "never pooled" (owner... | same destination DROP -> REPRESENTED
638. VL-19-638 [ledger L649, App.A L159] Y-5: SQLite tables `reviewer_runs` and `outcomes`; view `model_scores`... | same destination CORE -> REPRESENTED
639. VL-19-639 [ledger L650, App.A L160] Y-6: files `<dir>/records/YYYY/MM/<run_id>.jsonl` and `.outcomes.jsonl... | same destination CORE -> REPRESENTED
640. VL-19-640 [ledger L651, App.A L3200] Y-7: nobody in the product writes telemetry (`merge_cmd` imports only ... | same destination HARNESS -> REPRESENTED
641. VL-19-641 [ledger L652, App.A L4396] Y-8: `model.observed` has no producer, so `model_scores` is empty with... | same destination DROP -> REPRESENTED
642. VL-19-642 [ledger L653, App.A L161] Y-9: `task_variables` is regex-based; `doc_format` is always "markdown... | same destination CORE -> REPRESENTED
643. VL-19-643 [ledger L654, App.A L162] Y-10: at HEAD `cluster.py` computes the `cluster_agreement` telemetry ... | same destination CORE -> REPRESENTED
644. VL-19-644 [ledger L655, App.A L4397] TS-1: run-1 test command `tests/review` plus 5 skills files = 299 pass... | same destination DROP -> REPRESENTED
645. VL-19-645 [ledger L656, App.A L4398] TS-2: run-2 says 13 files and "159 def test_" with 304 collected; the ... | moved EVAL -> DROP (recorded: DROP[duplicate]: duplicate of DR-074; was EVAL: the defect r) -> REPRESENTED
646. VL-19-646 [ledger L657, App.A L4399] TS-3: 299 (run 1) + 5 (`test_review_brief_placement.py`) = 304 (run 2)... | same destination DROP -> REPRESENTED
647. VL-19-647 [ledger L658, App.A L1894] TS-4a: at HEAD `tests/review` has 19 test files; def counts of the 7 o... | same destination EVAL -> REPRESENTED
648. VL-19-648 [ledger L659, App.A L163] TS-4b: #518 added 24 lines to `test_review_panel_live7.py`: a test tha... | same destination CORE -> REPRESENTED
649. VL-19-649 [ledger L660, App.A L3699] TS-5: `tests/cli` has no file for `cli/review`; `tests/cli/reflect/*` ... | same destination KNOWLEDGE -> REPRESENTED
650. VL-19-650 [ledger L661, App.A L4400] TS-6: not covered by tests: exact boundaries (anchor 12 and 200, claim... | moved EVAL -> DROP (recorded: DROP[duplicate]: duplicate of DR-073; was EVAL: the defect r) -> REPRESENTED
651. VL-19-651 [ledger L662, App.A L4401] TS-7: not covered by tests: prompt-versus-code drift (the prompt's cat... | moved EVAL -> DROP (recorded: DROP[duplicate]: duplicate of DR-073; was EVAL: the defect r) -> REPRESENTED
652. VL-19-652 [ledger L663, App.A L4402] TS-8: the `@live7` gateway test asserts only pairwise t2 != t2b, t3-1 ... | same destination DROP -> REPRESENTED
653. VL-19-653 [ledger L664, App.A L4403] TS-9: dropped-finding reporting is tested only as `assert res["warning... | moved CORE -> DROP (recorded: DROP[duplicate]: duplicate of DR-073; was CORE: the defect r) -> REPRESENTED
654. VL-19-654 [ledger L665, App.A L4404] TS-10: telemetry tests are the only callers of `append_record` and `ta... | same destination DROP -> REPRESENTED
655. VL-19-655 [ledger L666, App.A L1633] TS-11: prompt and skill tests: `test_review_prompt_overrides.py` lints... | same destination MODULE-spec -> REPRESENTED
656. VL-19-656 [ledger L667, App.A L3201] RR-1: `run-reviewer.sh <EVAL abs> <pkg id> <reviewer_id> <model> [subd... | same destination HARNESS -> REPRESENTED
657. VL-19-657 [ledger L668, App.A L4405] RR-2: hard-coded paths `/tmp/evalsb/{repo,cand}` and `SRC_EVAL=/home/c... | moved HARNESS -> DROP (recorded: DROP[duplicate]: duplicate of DR-069; was HARNESS: the defec) -> REPRESENTED
658. VL-19-658 [ledger L669, App.A L4406] RR-3: brief text (R2TT:96-100) is `/sc:spec-panel @CAND --mode critiqu... | same destination DROP -> REPRESENTED
659. VL-19-659 [ledger L670, App.A L164] RR-4: per-attempt files `.attemptN.{json,md,err,meta.json}`; meta {rev... | same destination CORE -> REPRESENTED
660. VL-19-660 [ledger L671, App.A L4407] RR-5: `BLOCK_OK` is presence only (`grep -q '^```findings-v1'`, no par... | same destination DROP -> REPRESENTED
661. VL-19-661 [ledger L672, App.A L3202] RR-6: 2 attempts per model with no backoff (`:61-64` [V]) | same destination HARNESS -> REPRESENTED
662. VL-19-662 [ledger L673, App.A L4408] RR-7: ladder `FALLBACK` glm-5.3, Qwen3.8-max, gpt-6-luna, muse-ember-1... | same destination DROP -> REPRESENTED
663. VL-19-663 [ledger L674, App.A L4409] RR-8: the ladder is a hand-kept map, not read from `review-tiers.defau... | same destination DROP -> REPRESENTED
664. VL-19-664 [ledger L675, App.A L4410] RR-9: the ladder never fires for an APIERR-only failure: entry conditi... | moved HARNESS -> DROP (recorded: DROP[duplicate]: duplicate of DR-067; was HARNESS: the defec) -> REPRESENTED
665. VL-19-665 [ledger L676, App.A L3203] RR-10: besides the attempt-counter reset and the `expected_model` over... | same destination HARNESS -> REPRESENTED
666. VL-19-666 [ledger L677, App.A L4411] RR-11: variants kept `.bad-launch` (4,302 B; brief as positional argv;... | same destination DROP -> REPRESENTED
667. VL-19-667 [ledger L678, App.A L4412] RR-12: `SPEC.md` (152 lines) is an append-only ops log (procedure, har... | same destination DROP -> REPRESENTED
668. VL-19-668 [ledger L679, App.A L4413] W-1: `COMBO-REPORT.md` is 83,296 B and 506 lines; "FINAL RESULTS AND D... | same destination DROP -> REPRESENTED
669. VL-19-669 [ledger L680, App.A L4414] W-2: `PILOT-REPORT.md` is 6,835 B and `manifest.md` 1,271 B | same destination DROP -> REPRESENTED
670. VL-19-670 [ledger L681, App.A L1895] W-3: three packages `TASK-WF-design-20261108-041415`, `TASK-WF-designS... | same destination EVAL -> REPRESENTED
671. VL-19-671 [ledger L682, App.A L4415] W-4: `combos/` "107 entries = SPEC.md + 106 row dirs" and "only 19 of ... | same destination DROP -> REPRESENTED
672. VL-19-672 [ledger L683, App.A L1896] W-5: per-row content is `<pkg>/{ledger.json, merge-stdout.txt, merged-... | same destination EVAL -> REPRESENTED
673. VL-19-673 [ledger L684, App.A L4416] W-6: `quarantine-pre-src-luna/` holds pre-source.md luna-era data quar... | same destination DROP -> REPRESENTED
674. VL-19-674 [ledger L685, App.A L4417] W-7: `analysis/` scripts `attrib.py`, `doubles.py`, `b8-table.py`, `b9... | same destination DROP -> REPRESENTED
675. VL-19-675 [ledger L686, App.A L1897] W-8: audit purposes A model identity (890 runs), B incomplete or short... | same destination EVAL -> REPRESENTED
676. VL-19-676 [ledger L687, App.A L4418] W-9: `tools/tmp-scripts/` has 55 files (README: verbatim copies from `... | same destination DROP -> REPRESENTED
677. VL-19-677 [ledger L688, App.A L3204] W-10: blind scoring: `anon-*.sh` anonymise merged ledgers; `judge-one.... | same destination HARNESS -> REPRESENTED
678. VL-19-678 [ledger L689, App.A L4419] W-11: `startcombo*.sh` use `orca orchestration worker-start`; `r2-sonn... | same destination DROP -> REPRESENTED
679. VL-19-679 [ledger L690, App.A L4420] W-12: E1 interplay: `snap.py` (writes `input-snapshot.yaml` into this ... | same destination DROP -> REPRESENTED
680. VL-19-680 [ledger L691, App.A L4421] GS-1: branch `ironbelly/eval-tasklist-review-panel` was at `4a22d7421`... | same destination DROP -> REPRESENTED
681. VL-19-681 [ledger L692, App.A L4422] GS-2: `git diff --stat origin/master...<tip> -- src tests` is empty [V... | same destination DROP -> REPRESENTED
682. VL-19-682 [ledger L693, App.A L4423] GS-3: origin/master is 11 commits ahead of the branch base (`d2d8a2d16... | same destination DROP -> REPRESENTED
683. VL-19-683 [ledger L694, App.A L3205] GS-4: the 3041 untracked files (about 1.5 GB) are all under `20261111-... | same destination HARNESS -> REPRESENTED
684. VL-19-684 [ledger L695, App.A L4424] GS-5: the project CLAUDE.md rule ".dev/tasks/ is always staged" does n... | same destination DROP -> REPRESENTED
685. VL-19-685 [ledger L696, App.A L4425] GS-6: `manifest.md:5` "(local, never pushed)" is stale | same destination DROP -> REPRESENTED
686. VL-19-686 [ledger L697, App.A L4426] GS-7: after run 2 the commit `6c0984326` untracks 96 raw transcripts "... | same destination DROP -> REPRESENTED
687. VL-19-687 [ledger L698, App.A L3700] Section 6 validity map: `RP` (74 lines), `SP`, `reflect-reviewer.md`, ... | same destination KNOWLEDGE -> REPRESENTED
688. VL-19-688 [ledger L699, App.A L4427] BR-1: the only reviewer brief in `src` is `RP` (74 lines), installed t... | same destination DROP -> REPRESENTED
689. VL-19-689 [ledger L700, App.A L4428] BR-2: values to fill `RP:17-21` are `{{CANDIDATE}}`, `{{BASELINE}}`, `... | same destination DROP -> REPRESENTED
690. VL-19-690 [ledger L701, App.A L1634] BR-3: first-review brief `RP:32` reviews the candidate "against the re... | same destination MODULE-spec -> REPRESENTED
691. VL-19-691 [ledger L702, App.A L165] BR-4: grading check `RP:31`: "An implementer who follows the stated te... | same destination CORE -> REPRESENTED
692. VL-19-692 [ledger L703, App.A L166] BR-5: findings-block contract `RP:58-62`: last section `## Findings bl... | same destination CORE -> REPRESENTED
693. VL-19-693 [ledger L704, App.A L4429] BR-6: anchor guidance is only "12 to 200 characters copied exactly fro... | same destination DROP -> REPRESENTED
694. VL-19-694 [ledger L705, App.A L4430] BR-7: the brief has no severity definitions (CRITICAL/MAJOR/MINOR are ... | same destination DROP -> REPRESENTED
695. VL-19-695 [ledger L706, App.A L4431] BR-8: report-ending conflict `SP:260` ("last line is `verdict: PASS` o... | same destination DROP -> REPRESENTED
696. VL-19-696 [ledger L707, App.A L4432] BR-9: reviewers are not told the consequence of `blocking` (one blocki... | same destination DROP -> REPRESENTED
697. VL-19-697 [ledger L708, App.A L167] BR-10a: not in the brief: panel, tier or model identity; persona or le... | same destination CORE -> REPRESENTED
698. VL-19-698 [ledger L709, App.A L1293] BR-10b: there is no tasklist-specific rubric (task-ID, traceability, A... | same destination MODULE-tasklist -> REPRESENTED
699. VL-19-699 [ledger L710, App.A L1635] BR-11: re-review brief `RP:48` (evidence block `diff -w BASELINE CANDI... | same destination MODULE-spec -> REPRESENTED
700. VL-19-700 [ledger L711, App.A L168] BR-12: the review-panel paragraph `RP:68-70`: run reviewers printed by... | same destination CORE -> REPRESENTED
701. VL-19-701 [ledger L712, App.A L1636] BR-13a: `SP:256-268` Review Loop has 7 bullets (mode, grading, verdict... | same destination MODULE-spec -> REPRESENTED
702. VL-19-702 [ledger L713, App.A L1751] BR-13b: the cap sentence "at most 2 fix cycles" is text only, with no ... | same destination MODULE-rfqa -> REPRESENTED
703. VL-19-703 [ledger L714, App.A L169] BR-14: `sc-cli-eval-protocol/SKILL.md:85` says "Fold the panel's findi... | same destination CORE -> REPRESENTED
704. VL-19-704 [ledger L715, App.A L1637] Role, orchestrator or coordinator: the main session following `SP:256-... | same destination MODULE-spec -> REPRESENTED
705. VL-19-705 [ledger L716, App.A L170] Role, panel resolver: `superclaude review panel resolve` (`PC` to `P`)... | same destination CORE -> REPRESENTED
706. VL-19-706 [ledger L717, App.A L171] Role, reviewer: `RP:31-33` (first) and `:37-49` (re-review); the agent... | same destination CORE -> REPRESENTED
707. VL-19-707 [ledger L718, App.A L4433] Role, calibrator: NONE in this loop; `confidence` single/overlap is co... | same destination DROP -> REPRESENTED
708. VL-19-708 [ledger L719, App.A L4434] Role, merge or judge: the deterministic script `superclaude review mer... | same destination DROP -> REPRESENTED
709. VL-19-709 [ledger L720, App.A L1638] Role, reviser: `RP:53` plus `REVISER_RULES` (`L:22-26`) restated in th... | same destination MODULE-spec -> REPRESENTED
710. VL-19-710 [ledger L721, App.A L172] Role, revision recorder: `superclaude review ledger revise` (`LC:36-71... | same destination CORE -> REPRESENTED
711. VL-19-711 [ledger L722, App.A L173] Role, human: escalation at review 3 (`RP:13`; merged report `## Escala... | same destination CORE -> REPRESENTED
712. VL-19-712 [ledger L723, App.A L4435] Role, telemetry writer: NONE in the product [V] | same destination DROP -> REPRESENTED
713. VL-19-713 [ledger L724, App.A L174] Data contracts of the panel: findings-v1 (reviewer to merge), fixmap-v... | same destination CORE -> REPRESENTED
714. VL-19-714 [ledger L725, App.A L4436] Exit codes: `ledger verdict` returns 0 PASS, 10 REVISE, 11 ESCALATE [V... | same destination DROP -> REPRESENTED
715. VL-19-715 [ledger L726, App.A L1011] RV-1 purpose: reflect is UC-1 pre-execution coverage of a tasklist aga... | same destination MODULE-reflect -> REPRESENTED
716. VL-19-716 [ledger L727, App.A L4437] RV-2 reviewer agent: all reflect reviewers spawn as the fixed read-onl... | same destination DROP -> REPRESENTED
717. VL-19-717 [ledger L728, App.A L1012] RV-3 count and rotation: `--reviewers N` 2-3, default 3 (`SKILL.md:86`... | same destination MODULE-reflect -> REPRESENTED
718. VL-19-718 [ledger L729, App.A L4438] RV-4 model registry: the "three independent registries" claim is [CODE... | same destination DROP -> REPRESENTED
719. VL-19-719 [ledger L730, App.A L1013] RV-5a legacy reflect finding format: a markdown Deviations table (#, C... | same destination MODULE-reflect -> REPRESENTED
720. VL-19-720 [ledger L731, App.A L175] RV-5b findings-v2 field set at HEAD: container `findings-v2`, `V1_FIEL... | same destination CORE -> REPRESENTED
721. VL-19-721 [ledger L732, App.A L4439] RV-6 grounding unit: reflect uses `file:line` citations, the panel an ... | same destination DROP -> REPRESENTED
722. VL-19-722 [ledger L733, App.A L1014] RV-7 brief: reflect writes a per-reviewer file `<output>/reviewer-brie... | same destination MODULE-reflect -> REPRESENTED
723. VL-19-723 [ledger L734, App.A L1015] RV-8 calibration: reflect runs a blind `confidence-calibrator` per car... | same destination MODULE-reflect -> REPRESENTED
724. VL-19-724 [ledger L735, App.A L1016] RV-9 merge: reflect uses `sc-adversarial-protocol` Mode A with the jud... | same destination MODULE-reflect -> REPRESENTED
725. VL-19-725 [ledger L736, App.A L1017] RV-10 final gate: reflect's evidence-validator re-Reads every citation... | same destination MODULE-reflect -> REPRESENTED
726. VL-19-726 [ledger L737, App.A L1018] RV-11 loop: reflect has no fix loop and Tier 3 remediation is opt-in (... | same destination MODULE-reflect -> REPRESENTED
727. VL-19-727 [ledger L738, App.A L1019] RV-12: `confidence-calibrator.md` is troubleshoot-shaped (description ... | same destination MODULE-reflect -> REPRESENTED
728. VL-19-728 [ledger L739, App.A L1020] RV-13: `reflect-reviewer` is UC-2-shaped (`:3, :15`; output is the UC-... | same destination MODULE-reflect -> REPRESENTED
729. VL-19-729 [ledger L740, App.A L1294] RV-14: `sc-tasklist-protocol/SKILL.md:1640` says reflect "offers a Tie... | same destination MODULE-tasklist -> REPRESENTED
730. VL-19-730 [ledger L741, App.A L4440] RV-15: how the non-Claude rotation classes (qwen/kimi/deepseek) run as... | same destination DROP -> REPRESENTED
731. VL-19-731 [ledger L742, App.A L4441] Answer to Q1 at HEAD: `findings_v2` runs beside v1 (`findings.py` unch... | same destination DROP -> REPRESENTED
732. VL-19-732 [ledger L743, App.A L176] Answer to Q2 at HEAD: `ledger.merge_round` still calls `fnd.cluster` (... | same destination CORE -> REPRESENTED
733. VL-19-733 [ledger L744, App.A L4442] Answer to Q3 at HEAD: `hard_exclude` and `strict_distinct` work only w... | same destination DROP -> REPRESENTED
734. VL-19-734 [ledger L745, App.A L1898] V-1 ceiling: about 2-2.5 of 14 defects for every panel; five defects n... | same destination EVAL -> REPRESENTED
735. VL-19-735 [ledger L746, App.A L4443] V-2 panel guidance: default ember + 2x luna (1.83/14 found, 0.17/8 rea... | same destination DROP -> REPRESENTED
736. VL-19-736 [ledger L747, App.A L4444] V-3: 49 blocking findings lost to the 200/300 limits and 4 verdict fli... | same destination DROP -> REPRESENTED
737. VL-19-737 [ledger L748, App.A L4445] V-4: source-blind reviews, 156 of 665 valid-era runs (ember 81/209, lu... | same destination DROP -> REPRESENTED
738. VL-19-738 [ledger L749, App.A L4446] V-5: one reviewer's `blocking` flag decides the verdict; no calibrator... | same destination DROP -> REPRESENTED
739. VL-19-739 [ledger L750, App.A L4447] V-6: judge-counted blocking is not real blocking: over 71 rows the jud... | same destination DROP -> REPRESENTED
740. VL-19-740 [ledger L751, App.A L4448] V-7: terra and sol refusals: 51 reports say incomplete; 16 empty terra... | same destination DROP -> REPRESENTED
741. VL-19-741 [ledger L752, App.A L4449] V-8 model identity: 2 `b4-muse-luna2` t2b-1 "wonder" runs were served ... | same destination DROP -> REPRESENTED
742. VL-19-742 [ledger L753, App.A L4450] V-9 surviving statistics: second luna +0.83 found (Welch p 0.004, perm... | same destination DROP -> REPRESENTED
743. VL-19-743 [ledger L754, App.A L4451] V-10 retractions: n2-sonnet-src "8/14, 5/8" (corrupted judge), "second... | same destination DROP -> REPRESENTED
744. VL-19-744 [ledger L755, App.A L4452] V-11 pilot decision rule: only arm C passes, by one defect; efficiency... | same destination DROP -> REPRESENTED
745. VL-19-745 [ledger L756, App.A L1899] V-12: never-run models (muse-spark, muse-wonder-full) get at most a on... | same destination EVAL -> REPRESENTED
746. VL-19-746 [ledger L757, App.A L4453] V-13: testing closed by owner order 2026-11-13; batch 10 (grok + sonne... | same destination DROP -> REPRESENTED
747. VL-19-747 [ledger L758, App.A L4454] V-20: silent drop of whole findings for limits (anchor/anchor2 over 20... | same destination DROP -> REPRESENTED
748. VL-19-748 [ledger L759, App.A L4455] V-21: partial-panel failure invisible; merge refuses only if NO review... | same destination DROP -> REPRESENTED
749. VL-19-749 [ledger L760, App.A L4456] V-22: clearing ignores `block_ok`; docstring `L:112` false; a test pin... | same destination DROP -> REPRESENTED
750. VL-19-750 [ledger L761, App.A L4457] V-23: missing-anchor rows kept, never refound, never `resolved_check`,... | same destination DROP -> REPRESENTED
751. VL-19-751 [ledger L762, App.A L4458] V-24: ref-token scraping: free-text tokens ("UTF-8", "ISO-8601", "CVE-... | same destination DROP -> REPRESENTED
752. VL-19-752 [ledger L763, App.A L4459] V-25: over-merge: 3-line tolerance plus transitive union-find chain di... | same destination DROP -> REPRESENTED
753. VL-19-753 [ledger L764, App.A L4460] V-26: a refound row takes the current round's blocking call; the re-re... | same destination DROP -> REPRESENTED
754. VL-19-754 [ledger L765, App.A L177] V-27: besides revise-twice and the missing new-text hash, fix-map rows... | same destination CORE -> REPRESENTED
755. VL-19-755 [ledger L766, App.A L178] V-29: besides `--cap` ignored, `--round` unbounded and rounds past the... | same destination CORE -> REPRESENTED
756. VL-19-756 [ledger L767, App.A L4461] V-28: `defer` rewrites the last verdict to PASS with no precondition, ... | same destination DROP -> REPRESENTED
757. VL-19-757 [ledger L768, App.A L4462] V-30: `merge` exits 0 always; only `ledger verdict` maps to 0/10/11; n... | same destination DROP -> REPRESENTED
758. VL-19-758 [ledger L769, App.A L179] V-31: besides the line-model mismatch and the two-token fence, a quote... | same destination CORE -> REPRESENTED
759. VL-19-759 [ledger L770, App.A L4463] V-32: brief versus parser: limits not in the brief; "MEDIUM" rejected;... | same destination DROP -> REPRESENTED
760. VL-19-760 [ledger L771, App.A L4464] V-33: `distinct_across_slots` silently duplicates by default; a fixed ... | same destination DROP -> REPRESENTED
761. VL-19-761 [ledger L772, App.A L4465] V-34: tier data gaps: no muse-ember-1.0; excluded models still listed;... | same destination DROP -> REPRESENTED
762. VL-19-762 [ledger L773, App.A L4466] V-35: telemetry unwired (no product caller), `model.observed` has no p... | same destination DROP -> REPRESENTED
763. VL-19-763 [ledger L774, App.A L4467] V-36: `lint_cmd` and `estimate_cmd` registered but absent, `ModuleNotF... | same destination DROP -> REPRESENTED
764. VL-19-764 [ledger L775, App.A L4468] V-37: harness bugs: `expected_model` overwritten on fallback, attempt ... | same destination DROP -> REPRESENTED
765. VL-19-765 [ledger L776, App.A L4469] V-38: untested: exact limits, 4 of 6 categories in the parser, malform... | same destination DROP -> REPRESENTED
766. VL-19-766 [ledger L777, App.A L4470] V-39: reflect-side mismatches: `confidence-calibrator` troubleshoot-sh... | same destination DROP -> REPRESENTED
767. VL-19-767 [ledger L778, App.A L4471] V-50: strata never pooled; every telemetry record may carry a stratum ... | same destination DROP -> REPRESENTED
768. VL-19-768 [ledger L779, App.A L4472] V-51: anthropic-only: Haiku 5.5 stands in for tier 2/2b/3 (owner 2026-... | same destination DROP -> REPRESENTED
769. VL-19-769 [ledger L780, App.A L4473] V-52: Tier 2b is the review-panel and fallback tier; 429 policy (owner... | same destination DROP -> REPRESENTED
770. VL-19-770 [ledger L781, App.A L4474] V-53: fallback ladder = next model in the same tier, then the head of ... | same destination DROP -> REPRESENTED
771. VL-19-771 [ledger L782, App.A L4475] V-54: quarantine pre-source.md luna-era data (owner order 2026-11-12 1... | same destination DROP -> REPRESENTED
772. VL-19-772 [ledger L783, App.A L4476] V-55: raw transcripts not committed (1.48 GB, 2,916 files per the note... | same destination DROP -> REPRESENTED
773. VL-19-773 [ledger L784, App.A L4477] V-56: reflect Tier 2 default `--t2-engine legacy`; `shadow` measures o... | same destination DROP -> REPRESENTED
774. VL-19-774 [ledger L785, App.A L180] V-57: which blocking rule is canonical (`SP:259`, `RP:31`, `F:100`, or... | same destination CORE -> REPRESENTED
775. VL-19-775 [ledger L786, App.A L4478] V-58: whether the unified panel replaces reflect UC-1's advisory revie... | same destination DROP -> REPRESENTED
776. VL-19-776 [ledger L787, App.A L4479] V-59: whether to adopt reflect's findings_v2 limits as-is, which carri... | same destination DROP -> REPRESENTED
777. VL-19-777 [ledger L788, App.A L4480] V-60: commit or delete the 3 foreign scripts; deletion waits for the o... | same destination DROP -> REPRESENTED
778. VL-19-778 [ledger L789, App.A L4481] V-61: panel dispatch by raw gateway model ids via `claude -p --model <... | same destination DROP -> REPRESENTED
779. VL-19-779 [ledger L790, App.A L4482] V-70: keep `tools/run-reviewer.sh` ideas (identity check, attempt meta... | same destination DROP -> REPRESENTED
780. VL-19-780 [ledger L791, App.A L4483] V-71: `.bad-launch` and `.unpassable-ac` variants and the 20 `*.catfix... | same destination DROP -> REPRESENTED
781. VL-19-781 [ledger L792, App.A L4484] V-72: `analysis/*.py` (`attrib`, `doubles`, `b8/b9-table`, `final-tabl... | same destination DROP -> REPRESENTED
782. VL-19-782 [ledger L793, App.A L4485] V-73: `tools/tmp-scripts/` 55 files: keep the `judge-one.sh` protocol ... | same destination DROP -> REPRESENTED
783. VL-19-783 [ledger L794, App.A L4486] V-74: `snap.py`, `drift-b3.py`, `rlog-r3.sh`, `brief_c1.py` (E1's eval... | same destination DROP -> REPRESENTED
784. VL-19-784 [ledger L795, App.A L4487] V-75: keep as evidence `combos/SPEC.md` (152-line ops log), `COMBO-REP... | same destination DROP -> REPRESENTED
785. VL-19-785 [ledger L796, App.A L4488] V-76: keep and extend `tests/review/test_review_{cli,findings,ledger,p... | same destination DROP -> REPRESENTED
786. VL-19-786 [ledger L797, App.A L4489] V-77: the notes R1CM, R1CP, R2CM, R2CP, R2TT are evidence; their line ... | same destination DROP -> REPRESENTED
787. VL-19-787 [ledger L798, App.A L4490] V-78: HO itself is evidence: verdict, section 4 "keep from run 1", rec... | same destination DROP -> REPRESENTED
788. VL-19-788 [ledger L799, App.A L4491] Overlap, finding schema: E1 findings-v2 is a superset of v1 (lens spec... | same destination DROP -> REPRESENTED
789. VL-19-789 [ledger L800, App.A L4492] Overlap, anchor and limit policy: E1 same 12-200 and 300 limits, drops... | same destination DROP -> REPRESENTED
790. VL-19-790 [ledger L801, App.A L4493] Overlap, clustering: E1 `cluster_v2` with chain flag, support values a... | same destination DROP -> REPRESENTED
791. VL-19-791 [ledger L802, App.A L4494] Overlap, ledger and loop: E1 `ledger.py` unchanged and reflect uses no... | same destination DROP -> REPRESENTED
792. VL-19-792 [ledger L803, App.A L1639] Overlap, verdict policy: E1 shadow only with no verdict change (the le... | same destination MODULE-spec -> REPRESENTED
793. VL-19-793 [ledger L804, App.A L4495] Overlap, panel templates and resolution: E1 `reflect-pre`, `-pre-x2`, ... | same destination DROP -> REPRESENTED
794. VL-19-794 [ledger L805, App.A L4496] Overlap, model registry: E1 tier JSON with `classes` while the reflect... | same destination DROP -> REPRESENTED
795. VL-19-795 [ledger L806, App.A L4497] Overlap, launch and dispatch: E1 gateway `launch {}` (null), anthropic... | same destination DROP -> REPRESENTED
796. VL-19-796 [ledger L807, App.A L4498] Overlap, calibration: E1 blind `confidence-calibrator` plus a per-find... | same destination DROP -> REPRESENTED
797. VL-19-797 [ledger L808, App.A L4499] Overlap, evidence and citation verification: E1 `verify_cmd.py` and th... | same destination DROP -> REPRESENTED
798. VL-19-798 [ledger L809, App.A L4500] Overlap, telemetry: E1 `review-telemetry/1` plus `manifest` plus panel... | same destination DROP -> REPRESENTED
799. VL-19-799 [ledger L810, App.A L1900] Overlap, benchmark and ground truth: E1 `.dev/eval-workspaces/shadow-m... | same destination EVAL -> REPRESENTED
800. VL-19-800 [ledger L811, App.A L4501] Overlap, brief: E1 `refs/reviewer-spec.md` with 3 sections plus a find... | same destination DROP -> REPRESENTED
801. VL-19-801 [ledger L812, App.A L4502] Overlap, integration point: E1 `sc:reflect` Tier 2 (UC-1 shadow, UC-2 ... | same destination DROP -> REPRESENTED
802. VL-19-802 [ledger L813, App.A L1021] Overlap, document types: E1 tasklist/plan (UC-1) and code diff (UC-2);... | same destination MODULE-reflect -> REPRESENTED
803. VL-19-803 [ledger L814, App.A L4503] Conflict C-S1: anchor-as-text (findings-v1, E2/E3) versus citation-as-... | same destination DROP -> REPRESENTED
804. VL-19-804 [ledger L815, App.A L4504] Conflict C-S2: E2's folder holds a script that writes into E1's eviden... | same destination DROP -> REPRESENTED
805. VL-19-805 [ledger L816, App.A L4505] Conflict C-S3: the blocking rule is defined four ways (`SP:259`, `RP:3... | same destination DROP -> REPRESENTED
806. VL-19-806 [ledger L817, App.A L181] Conflict C-S4: merge policy: deterministic any-blocking (panel) versus... | same destination CORE -> REPRESENTED
807. VL-19-807 [ledger L818, App.A L4506] Conflict C-S5: three model registries (reflect skill aliases, reflect ... | same destination DROP -> REPRESENTED
808. VL-19-808 [ledger L819, App.A L182] Conflict C-S6: reflect profile validation allows launch only for `sonn... | same destination CORE -> REPRESENTED
809. VL-19-809 [ledger L820, App.A L4507] Conflict C-S7: tasklist review today is reflect UC-1: advisory, the bu... | same destination DROP -> REPRESENTED
810. VL-19-810 [ledger L821, App.A L4508] Conflict C-S8: input contract: reflect briefs carry the spec or source... | same destination DROP -> REPRESENTED
811. VL-19-811 [ledger L822, App.A L1640] Conflict C-S9: ledger implementations: `cli/review/ledger.py` versus t... | same destination MODULE-spec -> REPRESENTED
812. VL-19-812 [ledger L823, App.A L4509] Conflict C-S10: strata `sonnet`/`haiku` in `review-telemetry/1` versus... | same destination DROP -> REPRESENTED
813. VL-19-813 [ledger L824, App.A L4510] Conflict C-S11: report ending `SP:260/263` versus `RP:58`; one wording | same destination DROP -> REPRESENTED
814. VL-19-814 [ledger L825, App.A L4511] Conflict C-S12: `sc-tasklist-protocol/SKILL.md:1640` (Tier-3 task-buil... | same destination DROP -> REPRESENTED
815. VL-19-815 [ledger L826, App.A L4512] Conflict C-S13: HO recommends run 2 as the main hand-off but run-2 not... | same destination DROP -> REPRESENTED
816. VL-19-816 [ledger L827, App.A L4513] Conflict C-S14: HO row 1 attributes the 40-file / +8,026 findings to r... | same destination DROP -> REPRESENTED
817. VL-19-817 [ledger L828, App.A L4514] Conflict C-S15: HO:58 states the source-blind cause as fact while `COM... | same destination DROP -> REPRESENTED
818. VL-19-818 [ledger L829, App.A L4515] Conflict C-S16: Tier 2b policy text (#518, owner 2026-11-12) versus th... | same destination DROP -> REPRESENTED
819. VL-19-819 [ledger L830, App.A L4516] Target component CORE, finding schema: findings-v2 as the superset wit... | same destination DROP -> REPRESENTED
820. VL-19-820 [ledger L831, App.A L4517] Target component CORE, anchor and citation locator with an explicit po... | same destination DROP -> REPRESENTED
821. VL-19-821 [ledger L832, App.A L4518] Target component CORE, id grammar and document-type profile (ref regex... | same destination DROP -> REPRESENTED
822. VL-19-822 [ledger L833, App.A L183] Target component CORE, clustering: v2 same-defect with chain flag and ... | same destination CORE -> REPRESENTED
823. VL-19-823 [ledger L834, App.A L4519] Target component CORE, ledger state machine (`review-ledger/1`): keep ... | same destination DROP -> REPRESENTED
824. VL-19-824 [ledger L835, App.A L4520] Target component CORE, verdict policy plug point: any-blocking (curren... | same destination DROP -> REPRESENTED
825. VL-19-825 [ledger L836, App.A L184] Target component CORE, panel config and resolution with `classes`, str... | same destination CORE -> REPRESENTED
826. VL-19-826 [ledger L837, App.A L4521] Target component CORE, model identity check (observed versus requested... | same destination DROP -> REPRESENTED
827. VL-19-827 [ledger L838, App.A L185] Target component CORE, brief generator: limits and enums read from the... | same destination CORE -> REPRESENTED
828. VL-19-828 [ledger L839, App.A L4522] Target component CORE, telemetry wired into merge and resolve, `model.... | same destination DROP -> REPRESENTED
829. VL-19-829 [ledger L840, App.A L4523] Target component CORE, evidence and citation verification and calibrat... | same destination DROP -> REPRESENTED
830. VL-19-830 [ledger L841, App.A L4524] Target component CORE, CLI exit codes and a report contract usable fro... | same destination DROP -> REPRESENTED
831. VL-19-831 [ledger L842, App.A L1295] Target component M-TL, tasklist profile: ids `T<PP>.<TT>`, `R-###`, `D... | same destination MODULE-tasklist -> REPRESENTED
832. VL-19-832 [ledger L843, App.A L1022] Target component M-RF, reflect profile: `reflect-*` templates, deviati... | same destination MODULE-reflect -> REPRESENTED
833. VL-19-833 [ledger L844, App.A L1641] Target component M-SP, spec-review profile: `RP` rubric, `SP` Review L... | same destination MODULE-spec -> REPRESENTED
834. VL-19-834 [ledger L845, App.A L1703] Target component M-PR (later), PR and code review: diff citations and ... | same destination MODULE-pr-review -> REPRESENTED
835. VL-19-835 [ledger L846, App.A L1752] Target component M-PR (later), rf-qa replacement: the "at most 2 fix c... | same destination MODULE-rfqa -> REPRESENTED
836. VL-19-836 [ledger L847, App.A L3206] Target component HARNESS, benchmark kit: blind judge, anonymiser, grou... | same destination HARNESS -> REPRESENTED
837. VL-19-837 [ledger L848, App.A L186] FX-1: the text-anchor limit of 12-200 chars with whole-line drop break... | same destination CORE -> REPRESENTED
838. VL-19-838 [ledger L849, App.A L4525] FX-2: exact-substring anchors over whitespace-flattened text: markdown... | same destination DROP -> REPRESENTED
839. VL-19-839 [ledger L850, App.A L4526] FX-3: the line-number model (`\n` versus `splitlines`): files with `\r... | same destination DROP -> REPRESENTED
840. VL-19-840 [ledger L851, App.A L1704] FX-4: the id grammar is fixed to `XX-n.n`, `P<digit>` and numeric sect... | same destination MODULE-pr-review -> REPRESENTED
841. VL-19-841 [ledger L852, App.A L1705] FX-5: the category enum is spec-shaped (`unpassable-check`, `missing-r... | same destination MODULE-pr-review -> REPRESENTED
842. VL-19-842 [ledger L853, App.A L4527] FX-6: severity and blocking semantics are inconsistent across `SP:259`... | same destination DROP -> REPRESENTED
843. VL-19-843 [ledger L854, App.A L1706] FX-7: the brief names only the candidate, with no source or baseline r... | same destination MODULE-pr-review -> REPRESENTED
844. VL-19-844 [ledger L855, App.A L4528] FX-8: reviewers are generic sessions with no read-only allowlist; only... | same destination DROP -> REPRESENTED
845. VL-19-845 [ledger L856, App.A L4529] FX-9: single-reviewer re-review (`apply_to ["first"]`) lets one review... | same destination DROP -> REPRESENTED
846. VL-19-846 [ledger L857, App.A L4530] FX-10: any-blocking verdict with no calibrator means the weakest model... | same destination DROP -> REPRESENTED
847. VL-19-847 [ledger L858, App.A L4531] FX-11: multi-round behaviour never exercised with real panels (the stu... | same destination DROP -> REPRESENTED
848. VL-19-848 [ledger L859, App.A L4532] FX-12: no locking, non-atomic `--out`, `merge` exit 0 and a relative d... | same destination DROP -> REPRESENTED
849. VL-19-849 [ledger L860, App.A L4533] FX-13: launch is undefined for gateway models, panel templates cannot ... | same destination DROP -> REPRESENTED
850. VL-19-850 [ledger L861, App.A L4534] FX-14: environment detection by `T3Model01` only, `T2bModel01` unread,... | same destination DROP -> REPRESENTED
851. VL-19-851 [ledger L862, App.A L4535] FX-15: silent duplicate models by default, exclusion only by flag (26 ... | same destination DROP -> REPRESENTED
852. VL-19-852 [ledger L863, App.A L4536] FX-16: telemetry unwired, strata `sonnet`/`haiku` only, `doc_format` m... | same destination DROP -> REPRESENTED
853. VL-19-853 [ledger L864, App.A L4537] FX-17: benchmarks rest on 3 plan packages, n of 4-6, ceiling about 2-2... | same destination DROP -> REPRESENTED
854. VL-19-854 [ledger L865, App.A L4538] FX-18: benchmark regeneration depends on `/tmp` copies, raw transcript... | same destination DROP -> REPRESENTED
855. VL-19-855 [ledger L866, App.A L4539] FX-19: gateway behaviour (misrouting under load, quotas, binary replac... | same destination DROP -> REPRESENTED
856. VL-19-856 [ledger L867, App.A L4540] FX-20: the cap "at most 2 fix cycles (3 reviews)" text is copied into ... | same destination DROP -> REPRESENTED
857. VL-19-857 [ledger L868, App.A L1753] FX-20 tension: rf-qa fixes in place while panel reviewers are read-onl... | same destination MODULE-rfqa -> REPRESENTED
858. VL-19-858 [ledger L869, App.A L4541] FX-21: the panel and ledger are wired into no skill other than `/sc:sp... | same destination DROP -> REPRESENTED
859. VL-19-859 [ledger L870, App.A L4542] FX-22: dead registrations `lint_cmd` and `estimate_cmd` on the CLI sur... | same destination DROP -> REPRESENTED
860. VL-19-860 [ledger L871, App.A L4543] Summary: material read in full at tip `6c0984326`: HO (67 lines) and t... | same destination DROP -> REPRESENTED
861. VL-19-861 [ledger L872, App.A L4544] Summary, what HEAD changed: `findings.py`, `ledger.py`, `ledger_cmd.py... | same destination DROP -> REPRESENTED
862. VL-19-862 [ledger L873, App.A L4545] Summary, HO's own claims: rows 1-8 hold in substance; contradicted or ... | same destination DROP -> REPRESENTED
863. VL-19-863 [ledger L874, App.A L4546] Summary, run 1 versus run 2 notes: 16 agreements, 13 disagreements or ... | same destination DROP -> REPRESENTED
864. VL-19-864 [ledger L875, App.A L4547] Summary, HEAD answers to Q1-Q3: findings-v2 still drops whole lines wi... | same destination DROP -> REPRESENTED
865. VL-19-865 [ledger L876, App.A L4548] Summary, new facts not in any note: findings-v2 is E1's superset and a... | same destination DROP -> REPRESENTED
866. VL-19-866 [ledger L877, App.A L4549] Summary, inventory size: about 360 coded entries (HO claims, 13 disagr... | same destination DROP -> REPRESENTED
867. VL-19-867 [ledger L878, App.A L4550] Gap 1: the two run reports are outside the slice; report-only numbers ... | same destination DROP -> REPRESENTED
868. VL-19-868 [ledger L879, App.A L4551] Gap 2: the untracked-file state (3,041 files, about 1.5 GB, 1380/1352/... | same destination DROP -> REPRESENTED
869. VL-19-869 [ledger L880, App.A L4552] Gap 3: `/tmp` state (70 `/tmp/*.sh`, 12 repo / 58 not; `/tmp/evalsb/*`... | same destination DROP -> REPRESENTED
870. VL-19-870 [ledger L881, App.A L4553] Gap 4: which commit added the 96 raw transcripts that `6c0984326` untr... | same destination DROP -> REPRESENTED
871. VL-19-871 [ledger L882, App.A L4554] Gap 5: pytest was not re-run at HEAD; 304 passed is the base result; H... | same destination DROP -> REPRESENTED
872. VL-19-872 [ledger L883, App.A L4555] Gap 6: `combos/` tracked entries are 97 at the tip versus run 2's "107... | moved EVAL -> DROP (recorded: DROP[duplicate]: duplicate of DR-076; was EVAL: the defect r) -> REPRESENTED
873. VL-19-873 [ledger L884, App.A L4556] Gap 7: `r19` having `glm-5.3` three times (R2TT:37) was not re-run ind... | same destination DROP -> REPRESENTED
874. VL-19-874 [ledger L885, App.A L1023] Gap 8: how `validate_reflect_profile` (`panel.py:80-136`) constrains `... | same destination MODULE-reflect -> REPRESENTED
875. VL-19-875 [ledger L886, App.A L4557] Gap 9: the relation between E3's installed ledger, stoprule and diffga... | same destination DROP -> REPRESENTED
876. VL-19-876 [ledger L887, App.A L4558] Gap 10: whether `findings_v2`/`cluster_v2` are meant to replace the v1... | same destination DROP -> REPRESENTED
877. VL-19-877 [ledger L888, App.A L4559] Gap 11: HO row 5's attribution ("run 1 described the ladder as fixed")... | same destination DROP -> REPRESENTED
878. VL-19-878 [ledger L889, App.A L4560] Gap 12: the brief shared by both runs (H1) and the process claims abou... | same destination DROP -> REPRESENTED
879. VL-19-879 [ledger L890, App.A L4561] Question Q-A: which defect numbering will the final report use? Recomm... | same destination DROP -> REPRESENTED
880. VL-19-880 [ledger L891, App.A L4562] Question Q-B: is "clear a `resolved_check` row when its reviewer's blo... | same destination DROP -> REPRESENTED
881. VL-19-881 [ledger L892, App.A L187] Question Q-C: should the unified findings schema keep a text `anchor` ... | same destination CORE -> REPRESENTED
882. VL-19-882 [ledger L893, App.A L4563] Question Q-D: does the unified verdict replace reflect UC-1's advisory... | same destination DROP -> REPRESENTED
883. VL-19-883 [ledger L894, App.A L4564] Question Q-E: does the E2 owner agree to remove `snap.py`, `drift-b3.p... | same destination DROP -> REPRESENTED
884. VL-19-884 [ledger L895, App.A L4565] Question Q-F: is the "brief never names source.md" hypothesis (HO:58) ... | same destination DROP -> REPRESENTED
885. VL-19-885 [ledger L896, App.A L4566] Question Q-G: are gateway models launched by raw model id (`claude -p ... | same destination DROP -> REPRESENTED
886. VL-19-886 [ledger L897, App.A L3701] Question Q-H: should the notes' stale line cites be re-based before th... | same destination KNOWLEDGE -> REPRESENTED
COUNT 19-value-ledger-handoffs.md: 886

### Non-row sections of research/19-value-ledger-handoffs.md (checked, not counted in the COUNT line above)
The file also holds a tag convention, a 19-line re-derivation addendum (L903-923), a summary (L927-958: destination table 179/23/13/16/7/5/104/38/58/443 = 886, 411 duplicate DROPs, items-in versus rows-out, highest-value CORE list), Gaps G1-G10 (L966-975) and Questions Q1-Q6 (L981-986). They restate or qualify rows, they are not rows. Their substance: the destination table is superseded by the reconciled counts in report 8.1.0 (L4252: 139/23/13/15/7/5/95/32/56/501 = 886, equal to the actual Appendix A counts, recomputed by script); G2-G5 corrections (30/40 vs 26/40, three versus four flips, 92 versus 49, 159 versus 179) are in the report (hits at L329, L339, L1010-1016, Corrected claims); G8 destination-dependent rows keep their ledger destination in Appendix A; Q1-Q6 are the design axes 6.1, 6.2, 6.4, 6.8.b, 6.5 and 6.9 and the Section 9 questions. Low-level items only in the ledger addendum (panel.py +206 vs +194/-12, 309 tests collected at HEAD, sizes of run-1/run-2 hand-offs) are carried by their Appendix A rows (for example VL-19-038 at Appendix A L1811). No blocking omission.

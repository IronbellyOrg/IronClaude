# QA Report — Research Gate (Evidence-Quality Lens, Partition 1 of 2)

**Topic:** Unified Review Panel (E1 reflect Tier 2 panel / E2 tasklist review-panel study at 4a22d742 / E3 #346 review loop)
**Date:** 2026-11-13
**Phase:** research-gate
**Fix cycle:** N/A
**Lens:** evidence-quality (checklist items 1-4)
**assigned_files:** research/01-finding-contract.md, 02-ledger-merge-verdict.md, 03-clustering.md, 04-panel-resolution-identity.md, 05-blocking-calibration.md, 06-input-contract-briefs.md
**fix_authorization:** false (report only)

[PARTITION NOTE: Cross-file checks limited to assigned subset. Full cross-file verification requires merging all partition reports.]

## Analyst reports

At the time this review started, `qa/analyst-completeness-report-1.md` and `qa/analyst-cross-validation-report-1.md` existed only as headers (in progress, verdict "PENDING"). No analyst findings were available to verify; full verification was performed independently.

---

## Per-file verification

### File 01 — `research/01-finding-contract.md` (475 lines)

- **Inventory:** `**Status:** Complete` (line 5); `## Summary` present (line 472); Gaps and Questions (445) and Stale Documentation (463) present. PASS.
- **Evidence density:** Dense (nearly every bullet carries `file:line`). Every cited source path checked exists.
- **Re-verified claims (17), each by opening the cited source:**

| # | Claim in 01 | Source opened | Result |
|---|---|---|---|
| 1 | `SEVERITIES` findings.py:14, `CATEGORIES` :15-22, `_ID` :26, `_REF_TOKEN` :29, `_HEAD_FINDINGS` :31 | `sed -n 14,31p findings.py` | Exact |
| 2 | v1 validator `_check_finding` :90-121, rule order, anchor 12-200 via `_check_flat`, claim <=300 at :118, refs <=8 | `sed -n 90,121p findings.py` | Exact |
| 3 | v2-0 `calibrated_confidence` reject :96-97; v2-15 deviation_class required under reflect-post :147-149; v2-19 blocking label rule :161-162 | `findings_v2.py` 94-100, 145-165 | Exact |
| 4 | v2 prior lines rejected :279-283; empty-block rule :291-298; state truncated/invalid/complete :299-303 | `findings_v2.py` 276-304 | Exact |
| 5 | `cluster.py:221` valid = state complete; `:256-257` skip non-valid reviewer | `cluster.py` 218-224, 252-260 | Exact |
| 6 | card_convert `BLOCKING_WORDS` :71-80, `MINOR_WORDS` :81-83 incl. `important` :82, `MAX_REF_TEXT=200` :85, `MAX_CLAIM=300` :86, truncation :199-201, `counts` :303-311 has no truncation counter [CODE-CONTRADICTED premise] | `card_convert.py` 71-90, 196-202, 300-312 | Exact; contradiction of the prompt premise confirmed |
| 7 | `bar.py@base:17` not path-shaped (`_EXT` needs alnum-only suffix, no `/`) | `card_convert.py` 88-132 (`_TOKEN`, `_EXT`, `_path_shaped`) | Confirmed |
| 8 | PR `Severity` enum models.py:106-113; `Finding` :168-207, field list; `fix_key` :196-207 sha256(path\nline\nbody) | `models.py` 104-114, 166-210 | Exact |
| 9 | Brief placeholders :17-21; grading check :31 (prose "Medium"); findings line :60 omits 300 and 8 limits; empty block :58; merge refusal :70 | `document_review_loop_prompts.md` 15-72 | Exact |
| 10 | `ledger.merge_round` warns with count and only `errors[0]` :130-134; keeps valid lines :135-138; `block_ok` :129/:147; raises only when no reviewer valid :150-157 | `ledger.py` 125-160 | Exact |
| 11 | Experiment ledger `GRADES_SPEC_PANEL` :38, `_blocking_spec_panel` :41-49, `PROFILES` :53-59, `ROW_INPUT_KEYS` :64, `ANSWER_ACTIONS` :65 | `~/.claude/skills/sc-review-ledger/scripts/review_ledger.py` 36-66 | Exact |
| 12 | `_CATEGORY_TABLE` severity_router.py:34-52 incl. `security-latent` :36; low-confidence drop :174-175 unconditional; in_diff:false step :178-189 | `severity_router.py` 30-54, 168-192 | Confirmed (see note N1-1, N1-2) |
| 13 | rf-qa "Review severity rule" :106-111, same text rf-qa-qualitative :111; report table rf-qa :448, qualitative :883; verdict rf-qa :170, :183; Items Reviewed :846-848; axis vocabulary :650 | Grep on both agent files | Exact |
| 14 | reflect-reviewer taxonomy :21-26 (two-word labels :23-24), severity scale :71, table header :84, `bar.py@base:17` :87, correctness-gap table :110 has no severity column | `reflect-reviewer.md` 19-28, 69-90, 106-112 | Exact |
| 15 | Shadow brief appended instruction reviewer-spec.md:39 states claim <=300, citations 1-8, omits quote 12-200 and refs <=8 | `reviewer-spec.md:39` | Exact |
| 16 | E2 `run-reviewer.sh:17` brief lists v1 fields without 300/8 limits; `:9-11` ships source.md, `:15` names only the candidate; `:57` `BLOCK_OK` = fence grep | `git show 4a22d742:.../tools/run-reviewer.sh` | Exact |
| 17 | E2 `COMBO-REPORT.md:292` (56/18/14 over-length, 80 cases, 49 blocking lost), `:11` and `:72` catfix, `:371` recommendation (1) | `git show 4a22d742:.../COMBO-REPORT.md` lines 11, 72, 289-293, 371 | Exact |

- **Scope coverage:** EXISTING_FILES for this topic (findings.py, findings_v2.py, card_convert.py, pr_submit/models.py, Auggie refs, rf-qa/rf-qa-qualitative/reflect-reviewer agents, document_review_loop_prompts.md, review_ledger.py row schema) — all examined. PASS.
- **Doc cross-validation:** doc-sourced claims tagged ([CODE-VERIFIED] / [CODE-CONTRADICTED] / [UNVERIFIED]); the load-bearing [CODE-VERIFIED] claims (limits, blocking rules, merge acceptance, brief's missing limits) re-verified above. PASS.
- **Notes (MINOR, non-blocking):**
  - N1-1: `_CATEGORY_TABLE` closes at severity_router.py:53, not :52 (entries 35-52). Moved line, true claim.
  - N1-2: §1.2/§8.2 "code :178-189 drops one tier for every `in_diff is False`" is imprecise: for `architecture`/`layering`/`coupling` the code sets `Severity.LOW` directly and clears the floor (severity_router.py:180-187) rather than dropping one tier. The point being made (no affected-callsite test, contrary to rubric :95) still holds.

### File 02 — `research/02-ledger-merge-verdict.md` (330 lines)

- **Inventory:** `**Status:** Complete` (line 5); `## Summary` (line 327); Gaps (303) and Stale Documentation (319) present. PASS.
- **Evidence density:** Dense. All cited source paths opened exist (src, `~/.claude/...` installed variants, E2 audit-D via `git show`, bundle files).
- **Re-verified claims (14):**

| # | Claim in 02 | Source opened | Result |
|---|---|---|---|
| 1 | `_confidence` :86-90, `_decision` :93-96 (REVISE if n < cap else ESCALATE), `_brief_ids` :99-104 reads only blocking + status | `ledger.py` 86-104 | Exact |
| 2 | D2: docstring :112 "skipped for clearing" vs clearing loop :254-258 that never reads `block_ok` [CODE-CONTRADICTED] | `ledger.py` 108-114, 252-259 | Exact; contradiction confirmed |
| 3 | Round check :114-118 only `n == len(rounds)+1` (D16a) | `ledger.py` 114-118 | Exact |
| 4 | New row `blocking = any(...)` :187; matched row `current` overwrite :213-218 (one reviewer can un-block) | `ledger.py` 185-188, 211-219 | Exact |
| 5 | Verdict :273-275 FAIL iff brief ids | `ledger.py` 273-275 | Exact |
| 6 | `merge_cmd.py:40-41` `IntRange(min=1)` vs help "1, 2 or 3" [STALE DOC]; `--cap` help :69; `new_ledger` only on missing file + round 1 :101-104 | `merge_cmd.py` 38-42, 64-70, 99-112 | Exact |
| 7 | `EXIT_BY_DECISION` 0/10/11 `ledger_cmd.py:13` | `ledger_cmd.py:13` | Exact |
| 8 | `test_review_ledger.py:376-385` pins D3 and D2 (:385 asserts L1 `resolved` with t2-1 invalid); :408-417 pins D5; :544 one reviewer un-blocks | `test_review_ledger.py` 376-385, 408-417, 540-544 | Exact; the "also pins D2" observation is correct |
| 9 | `findings.annotate` dereferences `finding["anchor"]` at :349 (citation-only v2 finding would `KeyError`) | `findings.py` 346-352 | Exact |
| 10 | Audit D `summary.md:8` 49 blocking dropped; `:16` reasons 56/18/14/3/1; `:17` per-model; `:20` names three verdict flips; `:26` 45 merges lack merge-stdout; X1 :29, X5 :33, X6 :34 | `git show 4a22d742:.../audit-D/summary.md` | Exact |
| 11 | `flags.tsv` has 49 `3-dropped-blocking` lines: anchor>200 24, anchor2>200 14, claim>300 10, refs-bad 1; 4 EXCLUDE lines | `git show .../audit-D/flags.tsv` + grep counts | Exact (49; 24/14/10/1; 4 EXCLUDE) — the "3 not 4 flips" correction is supported |
| 12 | Experiment ledger `make_row` blocking at :889; `E-CAP` refusal :1300-1311 | `review_ledger.py` 889, 1300-1311 | Exact |
| 13 | Stoprule cap refusal :423-429 (EXIT_HALT); "silence never passes" :1185-1189 | `stoprule.py` 423-429, 1185-1191 | Exact |
| 14 | `finding-grader.md:4-7` tools Read / model sonnet / maxTurns 10 / permissionMode plan; :12 cannot read files; bundle `SNAPSHOT-STATE.txt:1,3` and `FINAL-REPORT.md:42, :75, :105-106, :109` | the three files | Exact |

- **Scope coverage:** EXISTING_FILES for this topic (ledger.py, merge_cmd.py, ledger_cmd.py, review_ledger.py, stoprule.py, finding-grader, audit-D, bundle state) — all examined. PASS.
- **Doc cross-validation:** tags present; the load-bearing D2/D3/D4/D16 [CODE-VERIFIED] claims and the [CODE-CONTRADICTED] docstring and flip count re-verified. PASS.
- **Notes:** none blocking. (Gap 7 correctly self-labels the 65-vs-38 figure [UNVERIFIED]; it is in fact present at E2 `COMBO-REPORT.md:291`, verified under file 01 claim 17 — MINOR note N2-1: the tag could be upgraded.)

### File 03 — `research/03-clustering.md` (397 lines)

- **Inventory:** `**Status:** Complete` (line 5); `## Summary` (line 394); Gaps (368) and Stale Documentation (384) present. PASS.
- **Evidence density:** Dense. All cited source paths opened exist.
- **Re-verified claims (13):**

| # | Claim in 03 | Source opened | Result |
|---|---|---|---|
| 1 | v1 `same_defect` :367-379 (fp+non-empty refs :371-372; refs-intersect-or-both-empty + spans within 3 :373-378) | `findings.py` 367-379 | Exact |
| 2 | v1 `cluster` :382-407 union-find, path halving, smaller root wins (:398), no chain/size/same-reviewer guard | `findings.py` 382-407 | Exact |
| 3 | `PRIMARY_ROLES` cluster.py:67-71, `SPAN_TOLERANCE=3` :72; fp `v2|role|path||refs|class` with empty section :119-123 | `cluster.py` 67-72, 119-123 | Exact |
| 4 | `same_defect_v2` :161-181: rule 1 fp equality at any distance (the "section always empty" over-merge), class compatibility, any resolved citation pair on same path within 3 | `cluster.py` 161-181 | Exact; over-merge reasoning follows from the code |
| 5 | `cluster_agreement` None with <2 complete, 1.0 with no blocking cluster, else mean support of unchained clusters (:403-412) | `cluster.py` 403-412 | Exact |
| 6 | `cluster_cmd.py:138` cards sorted by file name; `:151` `parse_block` with no `lens`; `:161` per-card `errors` persisted (answers file 01's open question) | `cluster_cmd.py` 136-162 | Exact |
| 7 | `verify_cmd.py:66-67` out-of-range check exists; `:68-72` quote-not-found; `:139` no block-state check | `verify_cmd.py` 62-72, 136-142 | Exact (this also resolves file 01 Gap 2 and file 02 Gap 8 as "yes, line_end is checked") |
| 8 | `telemetry.py:23` `_ID_TOKEN` duplicate of `_REF_TOKEN`; line 22 is `_TS` | `telemetry.py` 22-24 | Exact |
| 9 | `refs_norm` probe table (T01.02 -> [], AC-0.4 matched, AC-T01.02-3 -> [], ABCDE-1 -> [], D-P1 -> ['P1'], P12 -> [], R1-F1 -> [], S-3/S-6 matched, SHA-256 -> []) | re-ran `uv run python -c` calling `findings.refs_norm` | Exact on all 10 inputs re-run |
| 10 | [CODE-CONTRADICTED] "195 of 1398 rows with >=3 members": `audit2.py` increments `rows_total` before the `< 3` filter | `git show 4a22d742:.../audit-D/audit2.py` 136-156 | Confirmed: `rows_total += 1` precedes `if len(mem) < 3: continue` |
| 11 | Stage 0a replay totals `stage0a-report.md:243` (689 / 461 / 392 / 55 / 29 chained); `:249` 27 -> 7; `:253` 28 -> 28; `cluster_agreement` 1.0000 at `:251`, `:252`, `:261` [CODE-CONTRADICTED vs slice 04 "null everywhere"] | `stage0a-report.md` 243, 249-253, 261 | Exact |
| 12 | Pair result `pair-labels/README.md:18` TP 21 / FP 4 / FN 1 / TN 24, precision 0.84, recall 0.9545; AI labels, same model family (:22) | README 1-31 | Exact |
| 13 | Sampler skips same-reviewer and in-chain pairs `reflect_cluster_pairs.py:183`; tests `test_review_cluster.py:279` (anchor-only alone) and `:556` (invalid-block not clustered) | script 181-186; grep of test defs | Exact |

- **Scope coverage:** findings.py, cluster.py, cluster_cmd.py, verify_cmd.py, telemetry token, E1 weaknesses/pair-labels/stage0a artifacts, `reflect_cluster_pairs.py`, E2 audit-D `anch.py`/`audit2.py`, COMBO-REPORT — all examined. PASS.
- **Doc cross-validation:** tags present; W-3 correctly left [UNVERIFIED] with reason; the [CODE-CONTRADICTED] items re-verified. PASS.
- **Notes:** none.

### File 04 — `research/04-panel-resolution-identity.md` (319 lines)

- **Inventory:** `**Status:** Complete` (line 5); `## Summary` (line 316); Gaps (287) and Stale Documentation (304) present. PASS.
- **Evidence density:** Dense; several claims were established by running the resolver, and two of those runs were repeated here.
- **Re-verified claims (14):**

| # | Claim in 04 | Source opened / run | Result |
|---|---|---|---|
| 1 | `_STRATEGIES` panel.py:35, `_KINDS` :36 (first / re-review only), closed slot keys :46 (no role/lens/persona field) | `panel.py` 35-36, 46 | Exact |
| 2 | Reflect constants :71-73 (prefix, launch sonnet/opus/haiku, max 3); launch check :153-156 | `panel.py` 71-73, 153-156 | Exact |
| 3 | `select_env` :485-494 reads only `T3Model01` (:492) | `panel.py` 485-494 | Exact |
| 4 | D11 silent re-admission: `fixed` -> `candidates[0]` :536-537; empty pool + `hard` -> `ExclusionExhausted` :541-542, else `pool = candidates` :543 | `panel.py` 536-545 | Exact |
| 5 | `launch = environment.get("launch", {})` :595; per reviewer `launch.get(model)` :679 | `panel.py` 595, 679 | Exact |
| 6 | Tier file: tier2 first model `gpt-6.1-sol` (:7); tier4 luna/haiku/grok (:10); no `tier0`; `muse-ember-1.0` absent from aliases, names and classes; gateway `launch: {}` (:29), note "dispatch mechanism per model not defined yet" (:26); anthropic-only stand-ins all haiku (:34), launch map (:35), note dated 2026-11-10 (:32) | `review-tiers.default.json` (whole file) | Exact |
| 7 | `panel validate` calls `validate_panel(obj)` without tiers (panel_cmd.py:124) | `panel_cmd.py` 120-126 | Exact |
| 8 | `live7` gateway resolves Qwen3.8-max twice (D11 reproduced) | re-ran `superclaude review panel resolve --template @live7 --env gateway --run-id run1` | Reproduced: sonnet, muse-spark-1.3, Qwen3.8-max, glm-5.3, Qwen3.8-max, haiku, luna |
| 9 | No reflect template resolves in gateway (`launch None`) | re-ran `... --template @reflect-pre --env gateway` | Reproduced, same error text |
| 10 | E2 runner: OBS from top-level events :51; `MODEL_LADDER` :44 never written; ladder loop :73-76 sets `MODEL="$NEXT"` and resets `attempt=0` (:76), so `expected_model` (:58) records the fallback; entry condition :66 includes `$APIERR`, loop :73 does not; `cost.json` sums `attempt*.meta.json` (:87) | `git show 4a22d742:.../tools/run-reviewer.sh` 44, 51, 55-58, 66, 73-76, 85-87 | Exact; the overwrite and APIERR findings follow from the code |
| 11 | E3 telemetry `REVIEWER_GROUPS` :30 with `model` group `(resolved, launch, observed)` :49; `STRATA` sonnet/haiku :112-115; `model_scores` view groups by `model_observed` :364-378 | `telemetry.py` 30-31, 49, 112-115; grep :364, :378 | Exact |
| 12 | `reflect_shadow_exit.py:148` compares card `model` with resolution `model` as a string; never reads `model_observed` | script 146-153; grep over `src` | Exact |
| 13 | `identity_source` / `model_observed` / `reviewer_model_self_report` exist only in prose (SKILL.md :341, :348, :974-975; reviewer-spec.md:39) and the telemetry view — no code sets `identity_source` [CODE-CONTRADICTED as implemented] | Grep over `src/` | Confirmed |
| 14 | Combo evidence: `results.md:33-38` haiku slot served by gpt-6.1-sol (A1, A2, B1-B3), A3 collapsed to sonnet (:35); `FINDINGS.md:9`, `:13` (E = 2 distinct models), `:15`; E2 `CR:298` second-luna effect, `CR:428` final guidance ember + 2x luna | the two files; `git show .../COMBO-REPORT.md` 298, 428 | Exact |

- **Scope coverage:** panel.py, panel_cmd.py, the 8 templates (table built per template, two re-run), tier file, E2 runner, reflect SKILL.md §4.3a/§7.1, combo PLAN/FINDINGS/results, troubleshoot REPORT, commit 9874d63fb — all examined. PASS.
- **Doc cross-validation:** tags present; the correction that `document_review_loop_prompts.md:70` does call `review panel resolve` (contradicting scope 02 D14) re-verified (seen under file 01 claim 9). Load-bearing distinctness and launch claims re-verified by running the CLI. PASS.
- **Notes:** none.

### File 05 — `research/05-blocking-calibration.md` (421 lines)

- **Inventory:** `**Status:** Complete` (line 5); `## Summary` (line 417); Gaps (389) and Stale Documentation (409) present. PASS.
- **Evidence density:** Dense. All cited source paths opened exist (contract.py, SKILL.md, rubric, calibrator agent, installed finding-grader, stage0a report, shadow run dirs, E2 reports via `git show`).
- **Re-verified claims (13):**

| # | Claim in 05 | Source opened | Result |
|---|---|---|---|
| 1 | `_DEVIATION_KEYS` contract.py:40; `single-reviewer-fallback` -> DEGRADED :295-296; T2 convergence < 0.80 / NaN / unparseable -> DEGRADED :317-326; count fallback halts on regression or drift > 0 :377-381 | `contract.py` 40, 295-296, 317-326, 377-381 | Exact |
| 2 | `contract.py` never reads `calibrator_diversity` (no `calibrat` hit) | `grep -c -i calibrat contract.py` -> 0 | Confirmed |
| 3 | `unauthorized_deviation_present` occurs only at SKILL.md:854 in the whole reflect skill directory (no producer rule) | `grep -rn unauthorized` over the skill dir | Confirmed (single hit :854) |
| 4 | Reuse-Miss "Blocking bar (high)" `S_reuse >= 0.82 AND confidence >= 0.85` at SKILL.md:1176; calibrator class list `{opus, sonnet, haiku, qwen, kimi, deepseek}` at :1248 | `SKILL.md` 1176, 1248 | Exact |
| 5 | [STALE DOC] rubric dimension 3 vocabulary `{Aligned, Refinement, Drift, Regression}` at reflection-rubric.md:39 | `reflection-rubric.md:39` | Exact |
| 6 | [CODE-CONTRADICTED] "5-dim reflection rubric": calibrator agent is a 6-dimension troubleshoot rubric (:3), `rubric_path` = `refs/escalation-rubric.md` (:48), six named dimensions (:61), gated-min formula (:67) | `confidence-calibrator.md` 3, 48, 61, 67 | Exact |
| 7 | Legacy "Uncalibrated findings: 689 of 689" `stage0a-report.md:376` | `stage0a-report.md` 370-376 | Exact |
| 8 | Shadow calibration coverage table sums to 142/142 | `jq .calibration_coverage` over every `.dev/reflect/*shadow*/panel/clusters.json` | Confirmed: 14 files, values match the table row by row, sum 142/142 (see note N5-1) |
| 9 | Rule A consequence rule `spec-panel.md:259`, verdict :260 | `spec-panel.md` 259-260 | Exact |
| 10 | Cluster-level single-member veto: docstring `cluster.py:46-47` "blocking when blocking_any", `:375-376` | `cluster.py` 46-47, 375-376 | Exact |
| 11 | `calibration_coverage` computed `cluster_cmd.py:177-179`, printed n/m :190 | `cluster_cmd.py` 177-179, 190 | Exact |
| 12 | E2 `PILOT-REPORT.md:14` wrong blockers definition; `:71` 0/8 blocking recall and Arm A passed both defect-rich packages | `git show .../PILOT-REPORT.md` 14, 71 (grep for "passed both defect-rich" hits :71) | Exact |
| 13 | E2 `COMBO-REPORT.md:291` 65 vs 38; `:298` 2x luna + 2x ember +2.75-3.25 wrong blockers p 0.005-0.03; `:319` haiku + 2x luna 3.00, `:331` ember + 2x luna 1.83, `:332` 2x ember + 2x luna 4.75 | `git show .../COMBO-REPORT.md` 291, 298, 319, 331-332 | Exact |

- **Scope coverage:** contract.py, SKILL.md §10/§11.3/§5/§7/§9.1, rubric, taxonomy, calibrator agent, finding-grader (installed), card_convert, findings_v2, cluster.py, spec-panel.md, shadow cards, E2 COMBO/PILOT — all examined. PASS.
- **Doc cross-validation:** tags present and correct; the load-bearing blocking-rule claims (veto in ledger/cluster, reflect halt classes, label rule) re-verified. The self-declared [UNVERIFIED] item "rf-qa IMPORTANT is blocking" is true (rf-qa.md:111, verified under file 01). PASS.
- **Notes (MINOR):**
  - N5-1: §5.2 says "142/142 ... over 13 runs with a `clusters.json`"; 14 runs have a `clusters.json` (shadow02-15; shadow12 is 0/0). 13 is the count of runs with findings. Wording only; total is correct.
  - N5-2: Gap "rf-qa IMPORTANT is blocking [UNVERIFIED]" can be upgraded to [CODE-VERIFIED] (`rf-qa.md:111`).

### File 06 — `research/06-input-contract-briefs.md` (283 lines)

- **Inventory:** `**Status:** Complete` (line 5); `## Summary` (line 280); Gaps (253) and Stale Documentation (272) present. PASS.
- **Evidence density:** Dense. All cited paths opened exist; recorded-brief counts were re-derived.
- **Re-verified claims (12):**

| # | Claim in 06 | Source opened | Result |
|---|---|---|---|
| 1 | The "no source path" pin is `assert "src/superclaude" not in TEXT` (test_review_rules_text.py:92), not a source-document ban; `test_insertions_a_b_c_follow_their_brief_lines` :34-42 requires the findings-block line right after the brief line | `test_review_rules_text.py` 34-42, 90-92 | Exact |
| 2 | C7 three-section pin `test_shadow_skill_contract.py:146-157` pins template text only | test 146-157 | Exact |
| 3 | `reviewer-spec.md:33` "exactly these three sections"; `:55` spec body injected for the qa persona only, whole file at <= 400 lines | `reviewer-spec.md` 33, 55 | Exact |
| 4 | `reflect-reviewer.md` allowlist :5, model sonnet :6, maxTurns 50 :7, permissionMode plan :8; expects `spec_path` :52 that the template lacks [CODE-CONTRADICTED] | `reflect-reviewer.md` 5-8, 52 | Exact |
| 5 | `_MUTATORS` includes Bash/Edit/Write/NotebookEdit/Task (test_reviewer_readonly_tools.py:30) | test file :30 | Exact |
| 6 | E3 re-review Step 1 needs `diff -w` (:44) and self-check `grep -nF` (:46) | `document_review_loop_prompts.md` 44, 46 | Exact |
| 7 | E2 judge brief names only GT, candidate, merged report (judge-one.sh:12-16), "Do not read anything outside" (:12); `bypassPermissions` with no deny list (:25-27) | `git show .../tools/tmp-scripts/judge-one.sh` | Exact |
| 8 | Candidates 173/200/134 lines, `source: ./source.md` at :3; tracked `.dev/tasks/done/<pkg>/source.md` 133/378/20 lines | `git show` + `wc -l` per package | Exact |
| 9 | 156 of 665 valid-era runs never referenced source.md, per-model split (ember 81/209, luna 49/222, sonnet 1/63, terra 0/44); cause stays an inference | `git show .../COMBO-REPORT.md:373` | Exact (tagged [UNVERIFIED] in the file; it is in fact verifiable at CR:373 — note N6-1) |
| 10 | 45 recorded briefs; 0 contain "exact heading line"; 23 of 45 carry H2 sections outside the three-section template; shadow10 puts the shadow line in a 4th section `## Card format (findings-v2 ...)` | `ls`, `grep -l`, fence-aware H2 count over `.dev/reflect/*shadow*/reviewer-briefs/*.md`; `grep '^## '` on shadow10 reviewer-1 | Exact (45 / 0 / 23; shadow10 :70) |
| 11 | `input-parse.md:41` source.md = byte-exact copy of a file source or the inline prompt text | `input-parse.md:41` | Exact |
| 12 | Workflow Wave 4 calls `/sc:reflect --mode pre --spec <pkg>/source.md --tasklist <pkg>/<id>.md` (sc-workflow-protocol/SKILL.md:89) | `SKILL.md:89` | Exact |

- **Scope coverage:** prompts file, reviewer-spec.md, reflect-reviewer.md, E2 runner/candidates/judge, recorded E1 briefs, workflow Wave 4, rules-text test — all examined. PASS.
- **Doc cross-validation:** tags present; the four [CODE-CONTRADICTED] items (role vocabulary, `spec_path`, C7 in practice, L4 live execution) are supported by the sources opened above. PASS.
- **Notes (MINOR):** N6-1: Gap 2 marks the 156/665 figure [UNVERIFIED] "COMBO-REPORT itself was not re-read"; it is present verbatim at E2 `COMBO-REPORT.md:373` and can be tagged [CODE-VERIFIED] (the causal inference remains UNVERIFIED, as CR:373 itself says).

---

## Items 5-10 (outside the lens; checked within the partition)

| # | Check | Result | Evidence |
|---|---|---|---|
| 5 | Contradiction resolution | PASS | Cross-checked shared facts across 01-06: verdict flips (02 says 3; 01, 04 consistent), source-blind count (04 notes 161 -> 156 at CR:373; 06 uses 156/665), v1 keep-lines vs v2 drop-reviewer (01, 02, 03 agree), single-reviewer veto (02, 05 agree), `cluster_agreement` 1.0/null (03, 05 consistent). No contradiction between the six files. Two gaps in 01/02 are answered in 03 (see N-X1). |
| 6 | Gap severity | PASS | Every Gaps section lists items as [UNVERIFIED] with reason, [CODE-CONTRADICTED] with evidence, or owner/design questions destined for the report's Open Questions. None leaves synthesis without a verified basis for the facts it will state; no CRITICAL or IMPORTANT gap found. |
| 7 | Depth (Deep tier) | PASS | End-to-end flows traced: 02 §4.3 (over-length anchor -> parse -> merge -> verdict flip, with line cites), 04 §4-§7 (template -> resolve -> launch -> served model), 03 §1.7 (cluster -> ledger row). |
| 8 | Integration points | PASS | Panel resolution -> dispatch (04), merge CLI <-> resolution file (02 §2), parser -> clusterer (01 §2.3, 03 §2.2), brief -> parser (01 §7, 06 §2.2), contract -> verdict (05 §1). |
| 9 | Pattern documentation | PASS | Each file names conventions (closed vocabularies, pure resolvers, prose-driven loops, pinned-by-test templates) with sources. |
| 10 | Incremental writing | PASS | Every file has per-section "Key Takeaways" blocks and numbered sections that build on each other; file mtimes differ (17:44-17:50). Structure is consistent with incremental writing; this cannot be proven from the final file alone. |

## Summary
- Checks passed: 10 / 10 (items 1-4 for all six files, items 5-10 within the partition)
- Checks failed: 0
- Critical issues: 0; Important issues: 0; Minor notes: 7
- Issues fixed in-place: 0 (fix_authorization: false)
- Claims re-verified by opening the source: 83 (01: 17, 02: 14, 03: 13, 04: 14, 05: 13, 06: 12), including 4 re-runs (refs_norm probe, two `panel resolve` runs, shadow calibration tally) and 3 re-derived counts (audit-D flags, recorded-brief shapes, shadow coverage)
- No cited path was missing; no wrong line number that changes meaning was found.

## Findings

| # | Severity | File | Claim | What the source shows | Fix |
|---|---|---|---|---|---|
| N1-1 | MINOR | 01 §8.2, §16 | `_CATEGORY_TABLE` severity_router.py:34-52 | Table opens :34, entries :35-52, closes :53 | Optional: cite :34-53 |
| N1-2 | MINOR | 01 §8.2 | code :178-189 "drops one tier for every `in_diff is False`" | For architecture/layering/coupling the code sets `Severity.LOW` and clears the floor (:180-187); others drop one tier. The no-callsite-test point stands | Optional: add the category exception |
| N2-1 | MINOR | 02 Gaps 7 | 65 vs 38 judge-blocking tagged [UNVERIFIED] | Present at E2 `COMBO-REPORT.md:291` | Optional: tag [CODE-VERIFIED] |
| N5-1 | MINOR | 05 §5.2 | "142/142 ... over 13 runs with a `clusters.json`" | 14 runs have `clusters.json` (shadow02-15); shadow12 is 0/0; total 142/142 correct | Optional: "14 runs, 13 with findings" |
| N5-2 | MINOR | 05 Gaps | rf-qa "IMPORTANT is blocking" [UNVERIFIED] | `rf-qa.md:111` states it | Optional: tag [CODE-VERIFIED] |
| N6-1 | MINOR | 06 Gaps 2 | 156/665 tagged [UNVERIFIED], CR not re-read | Present at E2 `COMBO-REPORT.md:373` with the same per-model split | Optional: tag the figure [CODE-VERIFIED]; keep the cause UNVERIFIED |
| N-X1 | MINOR | 01 Gaps 1-2, 02 Gap 8 | Whether `cluster_cmd` persists per-line errors and whether `verify_cmd` checks `line_end` are left [UNVERIFIED] | Both answered yes in 03 (`cluster_cmd.py:161`; `verify_cmd.py:66-67`), re-verified here | Synthesis should take the answer from 03 |

No CRITICAL or IMPORTANT finding.

## Confidence Gate

- **Confidence:** Verified: 10/10 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- **Tool engagement:** Read: 10 | Grep: 2 | Glob: 0 | Bash: 24 (14 of them batched or single read-only inspections of source; 6 appends to this report; 4 re-runs of read-only commands). No web research performed (tavily_search: 0 | tavily_extract: 0 | web_search_fallback: 0 | web_fetch_fallback: 0).
- UNCHECKED items: none. UNVERIFIABLE items: none (item 10 is judged from structure, as noted).

## Overall Verdict: PASS

Green light for synthesis for partition 1 (research files 01-06). The seven MINOR notes are recorded for the synthesis agents and do not need a fix cycle.

## QA Complete

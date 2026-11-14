# Research Completeness Verification (Cross-Validation Lens, Partition 1 of 2)

**Topic:** Unified Review Panel (E1 reflect Tier 2 panel, E2 tasklist review-panel study at 4a22d742, E3 #346 review loop)
**Date:** 2026-11-13
**Files analyzed:** 6 assigned (01-06) plus cross-partition reads as needed
**Depth tier:** Deep
**Lens:** cross-validation (checklist items 6 contradiction detection, 7 gap compilation, 8 depth assessment)
**fix_authorization:** false (report only)

[PARTITION NOTE: Cross-file checks cover assigned files 01-06 and every other research file or scope slice that makes a claim about the same component. Full cross-file analysis requires merging with partition 2.]

---

## Verdict: FAIL (1 blocking finding: 1 IMPORTANT, 0 CRITICAL; 7 MINOR notes)

Blocking: finding 1 (file 02 states the E2 chain count "195 of 1398 rows with 3+ members" as fact; the E2 code and file 03 show 1398 is all rows). Everything else checked is consistent or correctly tagged.

## What was checked

- Read in full: `research/research-notes.md` (171 lines), `01-finding-contract.md` (474), `02-ledger-merge-verdict.md` (329), `03-clustering.md` (396), `04-panel-resolution-identity.md` (318), `05-blocking-calibration.md` (420), `06-input-contract-briefs.md` (282).
- Cross-partition reads for same-component claims: `09-consumer-plugpoints.md:219-243` (D14), Grep over `07`-`12` for `merge_round`, `195 of 1398`, `cluster_agreement`, `telemetry.py:2x`, `STRATA`, severity-router lines, `:518`; scope slices 01, 02, 04 by Grep.
- Re-read source myself (2026-11-14): `findings.py:100-120`, `findings_v2.py:108-164`, `ledger.py:107-158` and `:250-259`, `panel.py:515-556`, `cluster.py:216-258`, `telemetry.py:18-30`, `cli/review/__init__.py` (whole).
- E2 at `4a22d742` via `git show` only: `audit-D/audit2.py:136-180`, `audit-D/summary.md:1-36`, `audit-D/flags.tsv` (count and reason tally).
- E1 artefacts: `stage0a-report.md:243-292` (per-run table), every `.dev/reflect/pre-*-shadow*/panel/clusters.json` (`cluster_agreement`, `blocking_any`, `chained` counts), count of shadow dirs / `panel/cards` / `clusters.json`.
- Task-specific blocking checks: Grep of files 01-06 for any other E2 commit, run-2 hand-off, `GT3`, "four/4 verdict", audits B/C/E/F summaries, and "only in the bundle". Result: no file 01-06 cites a newer E2 commit or a run-2 hand-off; none uses `GT3`; every "4 verdicts" mention is the corrected one (02:128, :307, :323; 04:314); no file claims B/C/E/F summaries; `ledger.py:112` docstring is reported as contradicted (02:51, :305), and the one file that cites it (03:60) cites it only for the "parsable findings are kept" half, which `ledger.py:135-138` confirms.

## Reading log (incremental)

- 01: Status Complete; Gaps/Stale/Summary present; effort tags on every section.
- 02: Status Complete; Date line 2026-11-14 (others 2026-11-13; the session date is 2026-11-14, so not an error).
- 03: Status Complete; contains an executed `refs_norm` probe (section 5.2).
- 04: Status Complete; contains executed `panel resolve` runs (sections 4, 4.1).
- 05: Status Complete; contains a read-only tally of 142 shadow findings (section 5.3).
- 06: Status Complete; contains an awk pass over 45 recorded briefs (section 2.4).

## Contradictions Found (checklist item 6)

| # | Topic | Side A | Side B | Stronger code evidence | Status |
|---|---|---|---|---|---|
| X1 | E2 chain count denominator | `02-ledger-merge-verdict.md:145` states as fact: "replayed `cluster()` shows 195 of 1398 rows with 3+ members are chains" (also `08-run-recording-telemetry.md:318`, partition 2; scope 01 H16) | `03-clustering.md:288`, `:376`: 1398 counts ALL rows, because `rows_total += 1` runs before the `< 3` filter | Side B. Re-read `git show 4a22d742:.../audit-D/audit2.py`: the loop is `for r in led["rows"]: rows_total += 1 ... if len(mem) < 3: continue`, and the print is `"rows with >=3 members:", "chained(...):", chain_total, "of", rows_total` | **Unresolved in file 02** (it carries the contradicted reading with no tag). Blocking (finding 1). |
| X2 | Stage 0a `cluster_agreement` | scope slice 04 line 49: "cluster_agreement null for every listed run" | `03-clustering.md:228`: 1.0000 in 11 runs | Side B. `stage0a-report.md:247-291` shows 1.0000 in exactly 11 rows (e.g. `pre-design-20261104164711`, `pre-phase1RemovalSpe-...`) | Resolved by file 03 (scope slice is stale). Note for synthesis. |
| X3 | Shadow-run `cluster_agreement` "1.000 everywhere" | scope 04 F-18 / line 161 (exit script, 9 runs); `03-clustering.md:126`, `:373` leaves it [UNVERIFIED] | Current `panel/clusters.json` files (read 2026-11-14): 1.0 in 11 of 14 runs, all with 0 `blocking_any: true` clusters; shadow09 = 0.9328 with 3 blocking clusters; shadow02 and shadow04 = null, 1 blocking chained cluster each. `07-reflect-merge-contract.md:360` says "1.0 in 10 of 11 runs that record it" (contract copies) | The run files. "1.000 everywhere" is true only of the 9-run subset the exit script saw; the 1.0 values are the no-blocking-cluster branch (`cluster.py:407-408`). | Resolves file 03 Gap 4; not a defect of 01-06. Note for synthesis. |
| X4 | D7 token line in `telemetry.py` | Task file gate text (Phase 3 rules) and scope 02 D7: `_ID_TOKEN` at `telemetry.py:22` | `03-clustering.md:187`, `08:448`, `12:331`: `:23` | Re-read `telemetry.py:18-30`: line 22 is `_TS`, 23 `_ID_TOKEN`, 24 `_ID_RE` | Files agree with code; the gate text is off by one. Synthesis must use `:23`/`:24`. |
| X5 | Does `ledger.confidence` get used? | `02-ledger-merge-verdict.md:53`, `:306`: printed in the merged report (`ledger.py:435`, `:473`), not used by any decision | `05-blocking-calibration.md:374` (section 14 table): "computes overlap/single, unused" | Side A is more precise; both agree no decision reads it (`_decision` `ledger.py:93-96`) | Wording only. Minor. |
| X6 | Experiment variants location wording | `01:267` "installed only in ~/.claude"; `02:189`, `:191`, `:227` "installed only" | `02:325` (stale-doc note), `05:201`, `09:238`: present in `~/.claude/` AND in the phase-5 bundle builds; not in `src/` | Both are true facts; "installed only" means "not in `src`". The known contradicted claim (bundle-only) is not repeated. | Wording risk only. Minor. |
| X7 | `cluster_agreement` null rule in the Stage 0a replay | `03-clustering.md:228`: "1.0000 exactly in the runs with 0 blocking clusters and null in every run with blocking clusters" | `stage0a-report.md` rows `pre-detachTheCcsessi-...` and `pre-fixGitHubIssue31-...`: 0 blocking clusters but null (only 1 complete reviewer, `cluster.py:405-406`) | Code and table; file 03's own section 2.6 states the `< 2` complete rule correctly | Over-broad sentence. Minor. |
| X8 | Shadow `clusters.json` count | `05-blocking-calibration.md:180`: "142/142 ... over 13 runs with a `clusters.json`" | Directory count 2026-11-14: 15 shadow dirs, 14 with `panel/cards`, 14 with `panel/clusters.json` (shadow12 holds 0/0) | Directory listing; file 05's own table lists 14 runs with values | 13 = runs with findings. Wording. Minor. |
| X9 | Provenance of ledger line claims in file 05 | `05:12`: "this file does not re-read `ledger.py`" | `05:295`: ledger lines tagged "[CODE-VERIFIED, this branch]" | The cited lines are correct (`ledger.py:187`, `:213-218`, `:274`; confirmed by file 02 and by my read of `:107-158`) | Internal inconsistency in the provenance note only. Minor. |

Checked and found consistent across files (no contradiction): limit literals 12-200 / 300 / 8 (`findings.py:104`, `:108`, `:114-118`; `findings_v2.py:111`, `:126`, `:132`, `:136`; files 01, 02, 03); bad-line policy (v1 keeps valid lines `ledger.py:135-138`, v2 drops the whole reviewer `cluster.py:221`, `:256-257`; files 01, 02, 03); `merge_round` cannot take findings-v2 citations (file 02 section 5; no file in 07-12 claims otherwise); which blocking rule governs (files 01 section 5 and 05 section 10: consequence rule is reviewer prose, label rule `findings_v2.py:161-162` applies only with `reflect_category`, effective decider is `any(...)` at `ledger.py:187`); distinctness defaults (files 04 section 2 and 05 section 12: soft re-admission `panel.py:539-543`, opt-in `--strict-distinct`); D2 and D3 pin at `test_review_ledger.py:376-385` (file 02 and file 12 agree); 49 lost blocking findings = 24 anchor + 14 anchor2 + 10 claim + 1 refs (file 02; `flags.tsv` tally re-run: same); 3 verdict flips (files 02, 04, 05); 0/689 legacy calibrations (files 03, 05); `test_review_ledger.py` = 566 lines, 24 tests (file 02 and file 12; re-counted).

Gaps in one file that a sibling file already answers (no new research needed; synthesis should use the answering file):
- 01 Gap "does `cluster_cmd` persist per-line errors" -> 03 section 3: yes, `cards[].errors` (`cluster_cmd.py:161`).
- 01 Gap and 02 Gap 8 "does `verify-citations` check `line_end`" -> 03 section 4: yes, `out-of-range` (`verify_cmd.py:66-67`).
- 01 Gap "who emits `security-latent`" and "is `deep=True` single-source only" -> 10 rows D-c and D-e: router-only key, no caller passes `deep=True`.
- 03 Gap 1 (W-3 mapping) -> 01 section 3.3 (`card_convert.py:119-132`) and 06 section 2.4 item 5 (one-line `source.md`).
- 05 Gap "rf-qa IMPORTANT is blocking" -> 01 section 9 (`rf-qa.md:106-111`).
- 05 Gap "findings-v1 parse path of `review merge`" -> 02 sections 1-2 and 5.1.
- 05 Gap "6.70% agreement" -> 03 section 6.1 (`stage0a-report.md:295-297`, 24/358).
- 02 Gap 7 "65 vs 38" -> 05 section 11 read `COMBO-REPORT.md:291` directly.
- 06 Gap 3 "are `panel resolve`, `merge`, `ledger revise` registered" -> `cli/review/__init__.py` loader lists `panel_cmd`, `merge_cmd`, `ledger_cmd` (read 2026-11-14); 09 section 7.
- 04 Gap 14 (scope 02 D14 incomplete) -> 09 section 7 agrees: reflect SKILL.md and the prompts file call `panel resolve`.
- 08 (partition 2) "which audit-D script computes the chain replay [UNVERIFIED]" -> 03 section 7.2: `audit2.py:139-179`.

## Compiled Gaps (checklist item 7)

Severity here rates the gap's effect on synthesis. Every gap below is already recorded by its research file as UNVERIFIED, CODE-CONTRADICTED, an open question or an owner decision, so none is a defect of the research; they flow to report section 9 (Open Questions). "Answered" = a sibling file or this check already closes it.

### Critical gaps (block synthesis)
- None. No gap prevents writing the overlap matrix, value inventory, conflict log, target architecture or exposure list; each open item can be carried as an open question with its evidence.

### Gap table

| Gap | Source file | Severity | Needs new research? |
|---|---|---|---|
| Producer of `unauthorized_deviation_present` is undefined (declared SKILL.md:854, consumed `contract.py:371-372`, `:414`) | 05 | Important | No; owner decision (05 section 13.1 gives options) |
| Which blocking decider per consumer (veto / quorum / calibrator / blind grader / debate); only the veto has ground-truth evidence | 02 Gap 12, 05 section 14 | Important | No for the report; any choice of threshold needs E2 GT packages later |
| Distinctness: correctness requirement (E1) or cost knob (E2); intended replicas inexpressible | 04 Gap 12, 05 section 12 | Important | No; owner decision |
| Static step 5.6a: Regression (`deviation-taxonomy.md:123`) vs never sets `regression_present` (SKILL.md:1196) | 05 | Important | No; doc conflict to log |
| Drift at MINOR halts (`contract.py:380-381`) vs MINOR never blocks (`findings_v2.py:107-108`) | 05 | Important | No; owner decision |
| Calibrator rubric actually applied in recorded runs (6-dim agent vs 5-dim prose) [CODE-CONTRADICTED / UNVERIFIED] | 05 | Important | Yes, small: sample recorded calibrator outputs; report can state "unknown" |
| `identity_source: observed` has no implementation; `model_observed` read by nothing | 04 Gaps 2-3 | Important | No |
| No evidence for rounds 2-3 under a multi-reviewer ledger | 02 Gap 10 | Important | No (no data exists in any effort) |
| Rule A "Medium" vs Rule B label rule; label rule not lens-scoped | 05, 01 (D9) | Important | No; conflict to log |
| Anchor-only findings are singletons in `cluster_v2`; no anchor-to-citation step exists | 02 Gap 13, 03 section 2.9 | Important | No |
| `{{SOURCE}}` absent from every brief; source vs spec role split | 06 Gaps 11-14 | Important | No |
| Whether E2 long-anchor models would comply with a re-ask | 02 Gap 9 | Minor | Yes, but out of scope for this report |
| `--forward-subagent-text` needed for sub-agent `message.model` | 04 Gap 6 | Minor | Yes, small probe; not needed for the report |
| `claude -p --allowedTools` behaviour under `bypassPermissions` | 06 Gap 6 | Minor | Yes, small probe; not needed for the report |
| `qwen / kimi / deepseek` rotation branch has no data or code | 04 Gap 1, 05 stale doc | Minor | No |
| `tier0` rule inert; Tier 0 undefined | 04 Gap 4 | Minor | No |
| Rule D5 `N_eff` has no code (no reviewer-count option) | 04 Gap 5 | Minor | No |
| E2 runner cost under fallback and `APIERR` loop condition | 04 Gaps 8-9 | Minor | No |
| Sonnet-alone 2/16 and `manifest.md:11` alias claim cited from slices | 04 Gaps 10-11 | Minor | Possibly answered by file 11 (partition 2) |
| `sc-adversarial-protocol` weighting by calibrated confidence | 05 | Minor | Yes, small trace; not needed for the report |
| Grounding-gap producer side (orchestrator sets `partial`) is prose only | 05 | Minor | No |
| Calibration layout fenced vs unfenced (4 shadow runs) | 05 | Minor | No |
| D7 effect on real tasklist findings (empty-ref share) | 03 Gap 2 | Minor | Yes (replay E2 reports through `refs_norm`); optional |
| Population precision/recall of `cluster_v2`; human labels #525-#530 pending | 03 Gap 3 | Minor | No (pending owner labels) |
| v2 invalid-block loss on E2 data is inferred, not replayed | 03 Gap 5 | Minor | Optional |
| v1 0-based half-open vs v2 1-based inclusive line convention | 03 Gap 10 | Minor | No |
| Ordering dependence of the representative when uncalibrated | 03 Gap 13 | Minor | No |
| Audit-D kept/raw vs reason tally gap (haiku 23 vs 7, grok 2 vs 1) | 02 Gap 5 | Minor | No (summary says stale reports included) |
| Stoprule `grader_model` recording read by grep only | 02 Gap 11 | Minor | No |
| MR:142 (37/38 escalated) and 156/665 cited from slices | 06 Gaps 1-2 | Minor | Possibly answered by file 11 (partition 2) |
| Installed skill version per shadow run; `--isolate-reviewers` use | 06 Gaps 4-5 | Minor | No |
| Brainstorm/design spec review not wired; PR review ignores linked issue | 06 Gaps 15-16 | Minor | No (facts, carry to section 4) |
| `cluster_cmd` errors persisted; `verify_cmd` range check; `security-latent`; `deep=True`; W-3; rf-qa IMPORTANT; v1 merge parse; 6.70%; 65 vs 38; CLI registration; D14; chain script | 01, 02, 03, 05, 06 | — | Answered (see list above) |
| Shadow `cluster_agreement` 1.000 meaning | 03 Gap 4 | — | Answered by X3 above |
| [CODE-CONTRADICTED] items already logged by their files: `findings_v2.py:3` docstring; rubric `severity-rubric.md:90`, `:95` vs router; card_convert counter premise; `ledger.py:112` docstring; "4 verdicts"; `anch.py` as chain evidence; "195 of 1398 with >=3 members"; scope 04 null agreement; calibrator 5-dim claim; brief role list "plan or spec"; `reflect-reviewer.md:52` `spec_path`; C7 vs 23/45 briefs; SKILL.md:305 vs shadow09 | 01-06 | Minor (each correctly tagged) | No |

## Depth Assessment (checklist item 8)

**Expected depth:** Deep (data-flow traces, integration points, pattern analysis, new source reads beyond the scope slices).

| File | New source reads beyond the slices | Data flow traced | Executed evidence | Rating |
|---|---|---|---|---|
| 01 | Every validator rule of `findings.py:90-121` and `findings_v2.py:84-187` in order; `card_convert.py` shapes and maps; `pr_submit/models.py:106-207`; Auggie prompts; rf-qa tables; experiment `review_ledger.py` schema | reviewer line -> validator -> block state -> `cluster.py:256-257` / `ledger.py:135-138` | grep of limit literals (section 14.1) | Deep |
| 02 | Full `ledger.py` flow `:107-298`, `merge_cmd.py`, `ledger_cmd.py`; experiment ledger by ranges; stoprule and grader; audit-D scripts at 4a22d742 | 12-step `merge_round` trace; loss path (section 4.3) | re-count of `flags.tsv` (49) | Deep |
| 03 | Both clusterers line by line; `cluster_cmd`, `verify_cmd`; `audit2.py` side-by-side with `findings.py`; `reflect_cluster_pairs.py` sampler | v1 and v2 pipelines side by side (Q1 table) | `refs_norm` probe on 15 inputs via `uv run` | Deep |
| 04 | `panel.py:1-707`, `panel_cmd.py`, tier file, 8 templates, E2 runner, reflect §4.3a/§7.1, combo `extract.py` | resolve_slot -> resolve -> record; dispatch vs record | `panel resolve` runs for 6 templates x 2 envs | Deep |
| 05 | `contract.py` whole, SKILL.md §10/§11.3, rubric, taxonomy, calibrator agent, grader, `cluster.py` support | finding -> contract counts -> verdict (section 13) | read-only tally of 142 shadow findings | Deep |
| 06 | prompts file whole, `reviewer-spec.md` whole, agent, E2 runner/candidates/judge, test pins | brief -> reviewer -> transcript; consumer input matrix | awk pass over 45 recorded briefs; `git show` + `wc` of 3 packages | Deep |

**Actual depth achieved:** Deep for all six. No file only restates its scope slices; each corrects at least one slice claim from source (01: slice 00 §5.2 field names; 02: test :385 also pins D2; 03: `anch.py` and 195/1398; 04: scope 02 D14 and §4.2; 05: calibrator 5-dim claim; 06: `test_review_rules_text.py:92` meaning).
**Missing depth elements:** None blocking. Model-behaviour evidence is date-stamped in 01 section 11, 02 section 4, 03 section 6.3/7.2, 04 sections 4-8, 05 sections 5.3/11, 06 section 2.4.

## Completeness spot check (lens items 1-5 noted only where met)

| File | Status | Key Takeaways per section | Gaps and Questions | Stale Documentation Found | Summary | Effort tags |
|---|---|---|---|---|---|---|
| 01 | Complete | Y | Y | Y | Y | Y |
| 02 | Complete | Y | Y | Y | Y | Y |
| 03 | Complete | Y | Y | Y | Y | Y |
| 04 | Complete | Y | Y | Y | Y | Y |
| 05 | Complete | Y (section 0 included) | Y | Y | Y | Y |
| 06 | Complete | Y | Y | Y | Y | Y |

## Findings

| # | Severity | File | Finding | Remediation |
|---|---|---|---|---|
| 1 | IMPORTANT | `research/02-ledger-merge-verdict.md:145` (section 4.4, X1 bullet) | States as fact "replayed `cluster()` shows 195 of 1398 rows with 3+ members are chains". `03-clustering.md:288`, `:376` and the E2 code (`git show 4a22d742:.../audit-D/audit2.py`, loop `for r in led["rows"]: rows_total += 1` before `if len(mem) < 3: continue`) show 1398 is the count of ALL ledger rows. File 02 carries the contradicted reading untagged, so the overlap matrix or conflict log could cite a wrong chain rate. The same error is in `08-run-recording-telemetry.md:318` (partition 2). | Rewrite the bullet to "195 chained rows (rows with >= 3 members where some pair is not a direct match) among 1398 ledger rows in total; the number of rows with >= 3 members is not reported", cite `audit2.py:139-155`, and add a [CODE-CONTRADICTED] entry for `AD/summary.md:29` to Gaps and Stale Documentation. Partition 2 should apply the same fix to file 08. |
| 2 | MINOR | `research/05-blocking-calibration.md:374` | "computes overlap/single, unused" omits that `confidence` is printed in the merged report (file 02 `:53`). | Note only. |
| 3 | MINOR | `research/03-clustering.md:228` | "null in every run with blocking clusters / 1.0000 in the runs with 0 blocking clusters" is over-broad: two 0-blocking runs are null because fewer than 2 reviewers were complete. | Note only. |
| 4 | MINOR | `research/05-blocking-calibration.md:180` | "over 13 runs with a `clusters.json`": 14 runs have one (shadow12 is 0/0). | Note only. |
| 5 | MINOR | `research/05-blocking-calibration.md:12` vs `:295` | Says `ledger.py` is not re-read, then tags ledger lines CODE-VERIFIED; the lines are correct. | Note only. |
| 6 | MINOR | `research/01-finding-contract.md:267`; `research/02-ledger-merge-verdict.md:189`, `:227` | "installed only (in ~/.claude)" could be read as "not in the bundle"; the variants are in `~/.claude/` and in the phase-5 bundle, not in `src/` (02 `:325`, 05 `:201`). | Note for synthesis wording. |
| 7 | MINOR | Task file Phase 3 gate text; scope 02 D7 | Cites D7 at `telemetry.py:22`; code has `_ID_TOKEN` at `:23`, `_ID_RE` at `:24` (files 03, 08, 12 agree with code). | Synthesis uses `:23`/`:24`. Not a research defect. |
| 8 | MINOR | scope 04 line 49 and F-18 | Stage 0a "null for every listed run" is wrong (11 runs show 1.0000); shadow "1.000 everywhere" holds only for the exit script's 9-run subset (current run files: 1.0 x11, 0.9328 shadow09, null shadow02/04). | Synthesis uses `stage0a-report.md:247-291` and the run files. |

Note for the partition-2 merge: `12-test-pins-regression.md` D4 row (`:300`) does not list `test_refound_as_nonblocking_stops_failing_the_review` (`test_review_ledger.py:518-544`), which file 02 (`:97`, `:109`) identifies as the pin for the "one reviewer un-blocks" half of D4. Not a contradiction; the no-regression list should take file 02's entry.

## Recommendations

- Fix finding 1 in file 02 (and the same sentence in file 08) before synthesis.
- Synthesis should take the "Gaps answered by a sibling file" list above as resolved, so the Open Questions section does not repeat closed items.
- Synthesis should use the corrected values in X2-X4 and X7-X8, not the scope-slice wording.

**Verdict: FAIL** — one IMPORTANT finding (finding 1); MINOR findings 2-8 are notes and do not need rechecking.


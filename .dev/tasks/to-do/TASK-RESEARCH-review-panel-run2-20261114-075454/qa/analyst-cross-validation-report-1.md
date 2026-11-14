# Gate 1 Cross-Validation Report 1 (partition A, research files 01-08)

**Item:** 3.04 (Gate 1, partition A, cross-validation lens)
**Files reviewed (assigned):** research/01-overlap-capability-matrix.md through research/08-e2-evidence-grading.md
**Other files (Summary and Key Takeaways only):** research/09 through research/24
**Scope slices consulted:** research/scope/01 through 12; research/research-notes.md
**Lens:** cross-validation (contradictions, gap compilation, depth) plus gate focus (a)-(e)
**Date:** 2026-11-14
**Status:** Complete (verdict FAIL: 1 blocking, 9 minor)

[PARTITION NOTE: Cross-file checks limited to assigned subset plus the Summary/Key Takeaways of the other files.]

---

## 1. Method and read log

Tier: Deep. Report-only (fix_authorization: false). No research file, scope slice or task file was modified; the only file written is this report.

Files read completely, every line: research/research-notes.md (269 lines), research/01-overlap-capability-matrix.md (277), 02-finding-contract.md (254), 03-merge-ledger-verdict.md (284), 04-dispatch-identity-tiers.md (231), 05-input-delivery-brief.md (193), 06-reflect-two-engines.md (384, two pages), 07-e1-evidence-grading.md (124), 08-e2-evidence-grading.md (184).

Other research files, Summary section only (files 09-13 and 15-18 have a single `## Summary` paragraph and no file-level Key Takeaways heading; file 14 has per-section Key Takeaways, of which only the Summary at :274 was read; files 19-24 have a `## Summary` and a `## Gaps and Questions` section, both read): 09, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24.

Scope slices: the `## Gaps and Questions` sections of slices 01, 02, 03, 04, 09, 10, 11 were read in full; slices 05, 06, 07, 08 and 12 were consulted through keyword searches and through the Summary and Gaps of ledgers 21, 22 and 24, which enumerate their gaps.

Independent verification commands (all read-only; no checkout, fetch, pull, stash, commit or push; Python only through `uv run --no-sync` with PYTHONDONTWRITEBYTECODE=1; one batch script under /tmp per the Bash batching policy, removed on exit):
- V1 `runner.py` fix loop: Grep for `classify_fix|config.fix`, and `sed -n 740,800p src/superclaude/cli/reflect/runner.py`.
- V2 `ls src/superclaude/cli/review/data` (8 `review-panel.*.json` templates + `review-tiers.default.json` = 9 files); `git ls-files src/superclaude/cli/review | wc -l` = 25; `ls *.py | wc -l` = 16; `cat *.py | wc -l` = 5086.
- V3 `wc -l`: `findings_v2.py` 304, `findings.py` 457, `card_convert.py` 517.
- V4 `git show 6c0984326:<analysis/audits/audit-D/summary.md>` lines 1-24 and `run1.txt` lines 1-3; `git show ...:final-table.py` lines 1-30; a `uv run python` recount of the final-table exclusion flags (flags with control-package id: A 2 + B 10 + D 34 + E 13 = 59; flags that map to no package: 11; this reproduces file 16's "59 and 11"); last-round verdicts of the five "total-loss" merges through `git show ...ledger.json`.
- V5 `git log --format=... 4a22d74..6c09843 -- ':!.dev/tasks'` (four commits, times as in file 01) and `git diff --stat 4a22d74 6c09843 -- src tests | wc -l` = 0.
- V6 `git diff-tree` for #518 (167184c6b: 0 files under cli/review, 1 file under tests/review) and #519 (d2d8a2d16: 17 under cli/review, 22 under tests/review); `git show 6c09843:...snap.py | sed -n 1,6p`; `git grep -l brainstorm-reflect-panel 6c09843 -- .dev/eval-workspaces/tasklist-review-panel` (6 files).
- V7 `git ls-tree` at the E2 tip: r1..r5 `.py` counts 27/28/31/17/14; `combos/` 96 directories; 19 `RESULT.md`.
- V8 `grep -c '^def test_' tests/cli/reflect/test_verdict_mapping.py` = 36; `uv run --no-sync python scripts/reflect_shadow_exit.py` (no `--out`): `shadow runs counted: 13 of 20 required`, EV-1 `8/13 = 0.615` vs `3/39 = 0.077`, compliance mean 0.704, `OVERALL: FAIL (shadow runs 13 of 20)`, exit 1; `git status --short -- src tests scripts` empty afterwards.
- V9 `uv run python` recount of `results.jsonl` (15 rows, `out_tokens` sum 4,119,747) and `runs/*/panel/clusters_kept.json` (216 clusters: 203 single-reviewer, 13 multi-reviewer, 6 chained).
- V10 Grep `identity_source` over the 15 combo `return-contract.yaml`: 14 `requested-pinned`, 1 `observed` (comboC-r2).
- V11 Grep `T2bModel01` over the worktree excluding `.dev/tasks`, `.venv`, `.git`: 18 occurrences in 11 files (identical to file 04 section 6).
- V12 Spot-check of about 45 cited `file:line` anchors: ledger.py 136, 150, 254-258, 350-352, 37-38, 93-96; ledger_cmd.py 13; findings.py 29, 349; findings_v2.py 96-97, 161-162, 284-290, 299-304; cluster.py 219-222, 254-258, 384-388; verify_cmd.py 130-141; card_convert.py 199-202; panel.py 71-73, 80, 137, 153-156, 485, 500; telemetry.py 17, 23, 49, 112; manifest.py 38-54; contract.py 321; ensemble.py 74, 276-285, 772-773, 788, 808-809; runner.py 538-545; panel_lint.py 188; reflect_shadow_exit.py 243, 313; _diversity.py 8-15; models.py 30-50; local-gateway-alias-proxy.py 432, 697-702, 819; spec-panel.md 259-260; test_review_ledger.py 376. All matched as cited.

Not re-run: pytest (writes caches; not authorised; file 06 reports `352 passed, 1 xpassed`), the Stage 0a replay, `reflect_cluster_pairs.py`, the E2 `three-way.py` and `final-table.py` re-runs (file 08 reports them; I re-derived the exclusion-flag counts they depend on instead).

## 2. Checklist item 1: contradiction detection

Method: every claim in files 01-08 that overlaps another file or a scope slice was compared with the other side. Contradictions the assigned files already surface and resolve themselves (the [CODE-CONTRADICTED] lists of 01 section 1.3 and 2, 02 section 5, 03 section 1, 04 sections 4.2 and 6, 05 Unit 5, 06 section 4.2, 08 sections 3 and 5) were re-verified rather than re-listed; they are correct (see section 3, gate (e)). The table below lists only contradictions that are NOT resolved inside the files.

| # | Side A (location) | Side B (location) | Stronger evidence | Status |
|---|---|---|---|---|
| X1 | 01 section 4.2 grid row 7 (E1 = "absent") and section 4.3 row 7, E1 cell: "reflect has no fix loop (Tier 3 remediation is a separate opt-in)" | 06 section 4.2 ("`--fix` has no producer in production ... loop L748-L793") and 06 Key Takeaways (engine A has "dormant deviation, HALTED and `--fix` machinery") | Side B. I read `src/superclaude/cli/reflect/runner.py:748-793` (V1): a `while True` loop audits, classifies with `classify_fix`, applies a remediation through `_apply_remediation`, and re-audits up to `config.max_fix_iterations`, gated on `config.fix`; `sc-tasklist-protocol` passes `--fix` (06 section 4.1). The loop is dormant in production (engine A emits no `remediation_*` pointers, `ensemble.py:787-832`), but it exists and is code. 01's cell is true only for the `cli/review` kernel (no ledger, rounds or reviser) | UNRESOLVED, BLOCKING (finding B-1) |
| X2 | 01 section 1.2: `git grep` at the E2 tip "finds exactly these three files referencing `brainstorm-reflect-panel`" | My V6: the same grep restricted to `.dev/eval-workspaces/tasklist-review-panel` returns 6 files: the three scripts (`snap.py`, `drift-b3.py`, `rlog-r3.sh`) plus `HANDOFF-review-panel-unification-run2.md`, `HANDOFF-run1-vs-run2.md` and `handoff-notes/run2/tests-tools.md` (prose mentions) | Mine for the literal wording; 01's substantive point (three scripts that read or write E1's tree) holds | UNRESOLVED, MINOR (M-1) |
| X3 | 02 section 5.1 and 08 section 6: audit-D examined "264 merges from 89 rows x 3 packages" | 20 Summary / VL-20-734: "audit D examined 88 rows, not 89"; arithmetic: 89 x 3 = 267, 264 / 3 = 88 | Source text is internally inconsistent: `run1.txt:1` prints `merges 264 rows 89` and `summary.md:3` says 89 rows x 3 packages = 264. Neither side is provably right from committed data (my own count of `merged-1.md` files under `combos/` excluding contaminated, superseded and `i1-`/`i2-` rows gives 291 files in 93 rows, so the audit used a further filter I cannot reproduce) | UNRESOLVED, MINOR (M-9); carry "264 merges (audit's own count); row count 89 per `run1.txt:1`, 88 per 264/3" |
| X4 | 05 Summary: "Four different briefs deliver input to reviewers at HEAD" | 05 Unit 6 table: five brief families; Unit 6 answer: "Input reaches reviewers four different ways" | Unit 6 (the table lists five families; four delivery ways) | internal inconsistency, MINOR (M-3) |
| X5 | 06 section 3 Key Takeaways: "8 of 13 pilot EV-1 failures are layout mismatches" | 06 section 6.1: the 8 are 3 "no contract", 4 "merged-verdict: absent", 1 "reviewer-cards holds 0"; section 6.2 classifies the 3 as "contract assembled by the LLM", not layout | Section 6.1 (verified against my V8 run: 8/13) | internal inconsistency, MINOR (M-5) |
| X6 | 06 section 6.2 and 8(a)6: "Across all 59 recorded `reviewer-cards/` dirs, 51 use the `-card` name and only 2 use `reviewer-N.md`" | 06 section 6.2 table: reviewer-N.md names occur in shadow15 and combo B1-B3 (4 runs); 51 + 2 = 53 is not 59; my V-count over `.dev/reflect` and the combo runs root finds 84 `reviewer-cards/` directories (64 with `-card` files, 5 with `reviewer-N.md` files, 15 with neither) | The 4-run table. The "59" population is not defined and does not reproduce | MINOR (M-6) |
| X7 | 08 section 5: "the total-loss merges (g1-ember-luna2-r4/alias, g7-haiku-luna2-r4/designSpec, n4-sonnet-ember/design) ... did not flip" | `audit-D/summary.md` VERDICT FLIPS paragraph (V4) names five total-loss merges: the three above plus `h1-haiku-luna2-ember2-r2/designSpec t4-2` and `h1-...-r3/designSpec t4-1`; 02 section 5.1 correctly says "5 total-loss merges" | Source (five). I read the last-round ledger of all five at the tip: all are FAIL / REVISE with non-empty `brief_ids` (L5, L1, L1 for 08's three; L1 L2 L5 L6 and L8 for the two h1 rows), so 08's conclusion (3 flips, not 4) stands | partial enumeration, conclusion verified, MINOR (M-7) |

Contradictions with scope slices that the assigned files surface and settle with evidence (checked, correct): 01 vs slice 01/02 (#518 attribution; reflect contrast; combos 96 vs 95; `snap.py`); 02 vs slices 07/08 (`origin`; `_check_finding` naming; findings_v2 "seen only to line 135"); 03 vs slices 02/09 (variants re-implement); 04 vs slice 02 (`T2bModel01`) and slice 11 section 5.3 (`identity_source`: 14 requested-pinned, 1 observed, reproduced in V10); 05 vs slice 03 (B-6); 06 vs slice 10 (nothing contradicted); 07 vs slice 11 ("7 multi-reviewer" is "7 unchained of 13", reproduced in V9); 08 vs slices 01/03/04 (92/80/49 units, flips, 16 empty terra, 428 vs 417).

Contradictions I looked for and did not find between files 01-08 (each pair compared on its shared facts): 01 vs 02 (id grammar, `_REF_TOKEN`, 200/300 limits, `prior` lines, `refs_norm` effect); 01 vs 03 (cap 3, two ledgers, fingerprint); 01 vs 04 (reflect profile, `launch` map, tier file, `muse-ember`); 01 vs 06 (two engines, 0.75/0.80, `contract_version`); 03 vs 06 (exit-code maps, `derive_verdict`, 0.80); 04 vs 07 (collapse counts 1 of 3 / 0 of 12, served-vs-requested, `identity_source`); 06 vs 07 (13 of 20, EV-1 8/13, parity 6/13, 7 of 28 key leaks, 0.704, `:313`); 02 vs 08 (92/80/49, 3 flips, 109 vs 92, 17-19 unexplained); 05 vs 02 (reviewer-spec.md:39, brief limits).

Contradictions between files 01-08 and files 09-24 (Summary and Gaps read):
- 09, 10, 11, 12, 14, 15, 16, 18: no contradiction. Checked in particular: 11's "36-test matrix pins 0.80" = 06; 11 "no consumer passes `--t2-engine`" = 06 section 7; 12 "no review step in brainstorm/design" and "two consumers drive cli/review" = 01 section 2 point 2 (V12: `superclaude review ...` occurs only in `document_review_loop_prompts.md` and `sc-reflect-protocol/SKILL.md` outside the package); 15 "identity fields describe requested rotations" = 04/07; 16 "59 control-package exclusions mapped onto designSpec, 11 onto all packages" = my V4 recount (59 and 11), and 08's "41 / 25 / 3" is the valid-era row-package count (different unit, no contradiction); 18 "25 tracked files in cli/review" = V2.
- 13 vs 24 and research-notes: not in partition A, noted in section 7 (185 spawn-line figure).
- 17 vs 04: status mismatch for the `T2bModel01` claim (section 7, O-2).
- 19-24: status drift only (section 7).
## 3. Gate focus (a) to (e)

### (a) Every kept claim has file:line (or git path:line) evidence or an explicit [UNVERIFIED] tag

Result: PASS for all eight files. No untagged load-bearing claim was found. Per-file reading:

| File | Evidence form | Tag discipline | Spot-check result |
|---|---|---|---|
| 01 | `file:line` plus 5 executed probes (P-a..P-e) and git commands with output | `[CV]` / `[UV]` on every matrix cell; every `[UV]` names the slice | `git` facts, #518/#519 counts, E2 diff-stat, snap.py hash, r1..r5 `.py` counts, 96 / 19 counts all reproduce; one wording overstatement (X2) and one false cell (X1) |
| 02 | `file:line`, 4 executed parser runs, `git show` of audit-D | `[CODE-VERIFIED]` / `[UNVERIFIED]`; 13 numbered gaps | `findings.py`, `findings_v2.py`, `cluster.py`, `verify_cmd.py`, `card_convert.py` anchors all match; header "305 lines" vs actual 304 (M-2) |
| 03 | `file:line`, quoted reproduction output (d1, d2, d11, extra) | tagged per row; section 2 pins each test read | `ledger.py:254-258, :150, :350-352`, `test_review_ledger.py:376` match; template count 8 matches V2 |
| 04 | `file:line`, `[OBSERVED-RUNTIME]` for env, `jq`, stream logs | four tags incl. `[OBSERVED-RUNTIME]` | `T2bModel01` 18 / 11 reproduces; `panel.py` and `ensemble.py` anchors match; `local-gateway-alias-proxy.py` anchors match but the path is given only as a bare file name (M-8) |
| 05 | `file:line`, `[RUN]` probe, `git show` of E2 tip | `[SLICE-ONLY]` used and treated as `[UNVERIFIED]` | anchors match; probe results agree with 02 |
| 06 | `file:line` per sentence; executed exit script, pytest, `build_reflect_contract` probe | `[CODE-VERIFIED]` / `[UNVERIFIED]`; 13 gaps | V8 reproduces 13 of 20, 8/13, 0.704, FAIL; `runner.py:538-545`, `ensemble.py:74,773,788,808-809`, `contract.py:321`, `panel_lint.py:188`, `reflect_shadow_exit.py:313` match; two count slips (X5, X6) |
| 07 | recount scripts with printed values; `file:line` | `[CODE-VERIFIED]` / `[UNVERIFIED]`; strength scale on every finding | V9 reproduces 4,119,747, 216 / 203 / 13 / 6; token-share medians recompute (0.588 all runs; 0.568 clean rows); TP/FP/FN/TN sums to 50 |
| 08 | `git show` / `git ls-tree` / recomputed tables; S0-S3 grades | `[RECOMPUTED]` / `[UNVERIFIED]` | pilot cells recompute (any/16 A2 B3 C4; wrong blockers 0/1/3); 214 + 92 = 306 catches and 194/214 = 91% recompute; `fullpkg()` bug reproduces (V4); 5 total-loss merges (X7) |

Claims kept without evidence in files 01-08: none material. Claims explicitly left `[UNVERIFIED]` and carried to Gaps are listed in section 4.

### (b) Open items of research-notes.md and slice gaps: resolved, logged, or carried as a ledger row

| File | Open items named in research-notes (Phase 2 table) | Status |
|---|---|---|
| 01 | classify each cell; E2 post-hand-off commits change no product code (slice 01 G6); `snap.py` writes into E1's tree | all three resolved (V5, V6); plus items (d1), (d2) resolved |
| 02 | does `check_finding` reject `origin`; effect of truncate / reject / re-ask on 92/49; `T01.01` grammar | all three resolved with execution; re-ask recovery left as an unmeasured gap (logged, gap 5) |
| 03 | which pins encode defects; relation of variants to `cli/review/ledger.py`; reproduce D-1, D-2, D-11 | all resolved with execution |
| 04 | `muse-ember-1.0` at HEAD; reflect profile limits; what records the served model | all resolved (+ items (d), (e)) |
| 05 | what the core exposes per module; brief never names `source.md`; H1-H4; hard-codings; two [CODE-CONTRADICTED] claims | all resolved; effect of naming `source.md` on read rate left as an untestable gap (logged, gap 1) |
| 06 | byte-identical set; EV-1 failures mechanical; run exit script and tests; 0.75 vs 0.80; engine choice; SKILL.md ranges not read by slice 10 | all resolved; ranges L508-L621, L872-L935, L1047-L1203, L1293-L1708, L1740-L1849 stated as read |
| 07 | recount 15/15, 4,119,747, 216 / 7, TP/FP/FN/TN; grade each finding; thresholds T-1..T-10 approved? | all resolved (V9 reproduces); approval = negative result, logged |
| 08 | recompute pilot cells and `three-way.py`; unit of 92/80/49 and 3 vs 4 flips; does batch j1 invalidate "not confirmed" | all resolved (V4, V7); j1 answered with sensitivity table |

Slice gaps assigned to these files (spot-checked against the `## Gaps and Questions` of slices 01, 02, 03, 04, 09, 10, 11): resolved or logged inside 01-08: slice 01 G4 (01 gap 3), G5 (01 gap 5), G6 (01 section 1.1), Q-F (04 section 7); slice 02 gap 6 (97 vs 107 entries; 08 section 2), 8 (reflect profile; 04 section 2), 9 (variants; 01 section 6 and 03 section 3), Q-E (01 section 1.2); slice 03 gaps 3-6 (ember, Qwen count, quarantine count, flips; 04 section 7, 08 sections 2 and 5), Q9 (02 and 08); slice 04 Q3 (08 gap 3) and Q5 (08 section 6), Q2 only partly (08 section 8 notes the 930 vs 890 and 54 vs 59 audit-A mismatches but not which 70 rows the audit-A header means); slice 09 gap 1 (03 section 3); slice 10 gap 4 (logged as 06 gap 9 and 07 G-2). Carried only as ledger rows (allowed by the gate, not as a Gaps entry in the topic file): slice 10 gap 8 (live behaviour of `reflect run --transport openai_compat` not exercised; VL-23-787), slice 02 gap 7 (`r19`, `template_sha256` at HEAD; VL-19), slice 03 gap 7/8 (`merged-anon.md` identity leak in 54 files; `checks-gate8`; VL-20-249, VL-20-241). Result: PASS. The three slice-level items that are carried only as ledger rows are listed in section 4 as G-8 (slice 10 gap 8), G-17 (slice 03 gap 7) and G-18 (slice 02 gap 7) so the synthesis sees them.

### (c) No run-1 contamination

Searched `research/` for the two forbidden path strings (allowed by the item): hits are `research-notes.md:100, :151` (rule statements), `17-defect-register.md:534` (an independence statement), slice 03 gap 10 (the recorded slip), slices 07, 11, 12 (independence statements) and slice 01 line 7 (long line, independence statement). Zero hits in files 01-08. Also searched files 01-08 for run-1 report names and phrases: none. No citation or quotation from the forbidden folder or the RUN2-QUEUED note. One residual ambiguity: 07 section 4 says "A repository-wide grep for 'stop rule' returned many unrelated hits"; it does not state that `.dev/tasks/` was excluded, which research-notes rule 2 requires for every repo-wide grep (finding M-4 below, MINOR; nothing from it is cited). I did not read, list or grep into the forbidden folder or the queued note.

Result: PASS (one MINOR note).

### (d) Every value-ledger row has exactly one destination

Not applicable to partition A: files 01-08 contain no ledger rows. I read the Summary of ledgers 19-24; each states 886 / 868 / 1,685 / 955 / 796 / 589 rows with one destination per row. Not independently recounted here; that check belongs to the ledger partitions and the anti-omission gate.

### (e) No claim builds on a [CODE-CONTRADICTED] or [UNVERIFIED] row of research-notes AMBIGUITIES_FOR_USER as fact

Result: PASS. The 13 [CODE-CONTRADICTED] rows of research-notes: rows 1 (#518 attribution) and 3 (reflect contrast) are re-verified in 01; row 4 (alias GT3) in 08 and 01-era slice text; rows 5 and 6 ("no error", four flips) in 02 and 08; row 7 (16 empty terra) in 08; row 8 (`unpassable-ac`) and row 12 (`theory.py` HARD set) in 05; row 9 (`T2bModel01`) in 04. Rows 2 (D14 first half), 10 (159 functions), 11 (seed "no missing-task category") and 13 (fenced yaml memory lesson) fall in other files (11, 17, 10, 17) and no file in 01-08 relies on them (07 E1-F18 mentions row 13 and tags it `[UNVERIFIED by me]`). The [UNVERIFIED] bullets: "92 / 80 / 49 unit" resolved by 02 and 08 with the units stated; "combos/ size" resolved by 01 and 08 (96 / 97 / 106 each in its own unit); "E2 commits after 4a22d7421" resolved by 01; `muse-ember-1.0` resolved by 04; "installed variants re-implement or import" resolved by 01 and 03; "T-1..T-10 approved" resolved negative by 07; collaboration estimates and test counts used only as carried claims (01 row 15, [UV]); the #346 phase-5 numerics used only as `[UV]` pointers in 01 row 14. No file in 01-08 states an unresolved `[UNVERIFIED]` row as fact.
## 4. Checklist item 2: unified gap list (files 01-08), de-duplicated and rated

Rating rule: Critical = blocks synthesis; Important = affects the quality or the decidability of a report conclusion; Minor = recorded note, does not block. Source references are to the `## Gaps and Questions` of the named file or slice. Every gap below is already logged in a topic file or a ledger row; none was found unlogged, and none is rated Critical, because each can be carried into the report as an explicit `[UNVERIFIED]` or as an owner decision.

### Critical (block synthesis)

None.

### Important (affect quality or decidability)

| ID | Gap | Source | Why Important |
|---|---|---|---|
| G-1 | Re-ask recovery rate is unmeasured: E2 Spike 5 was deliberately not run; truncate / re-ask / keep-and-warn can only be compared through derived bounds (truncate recovers at most 88 of 92 dropped lines and 48 of 49 blocking lines; re-ask and keep-and-warn are not measurable) | 02 gap 5, section 5.2; slice 07 line 74 | The limits policy is a core decision; its evidence is a derivation, not a measurement |
| G-2 | No quality evidence for any panel design: E1 has no ground-truth scoring for any of 30 runs and its 60 seeded defects were never planted (07 N-1, N-3); E2 has 16 defects in 3 packages, 3 of them carry 89% of catches, 4 never caught, one judge, no committed re-judge artifact (08 G3, G15, "does not show" 1-9); acceptance evidence for the unified panel is undefined (07 Q-3, Q-4) | 07, 08, slice 11 Q-3 | The report cannot state that any combination or design is better; it can only state what must be built to measure it |
| G-3 | Claude Code behaviours outside the repository are unpinned and partly unverified: Agent `model` enum (sonnet/opus/haiku/fable), `resolvedModel` in the Agent result, family-alias behaviour under a same-family main session (docs/reference/model-aliases.md:51 "not verified"); hooks and `--resume` for gateway ids (research-notes UNVERIFIED) | 04 gap 3; research-notes | Any core contract that depends on them needs a version pin (Phase 4 W2 may close part of it) |
| G-4 | 17-19 findings dropped at merge with no rule-based reason (`3-conserve` 111 / `run1.txt` 109 vs 92 rule-explained; haiku 23 vs 7, grok 2 vs 1) | 02 gap 3; 08 gap 3; slice 04 Q3 | The 92 / 49 figures are then a lower bound of the true loss, or mix two populations |
| G-5 | Whether naming `source.md` in the brief raises the read rate is untested (E2 calls the cause an inference, `COMBO-REPORT.md:373`); j1 adds that 2 of 10 luna designSpec runs refused because a nested input named by `source.md` was missing from the sandbox | 05 gap 1; 08 sections 6, 7 G6 | The input-manifest requirement rests on inference plus the code-level fact that no brief names a second document |
| G-6 | Cause of the E1 citation-resolution fault (0 resolved citations in 7 of 15 combo runs and 3 pilot runs with findings; A1 pre-check 62 of 62 `missing-file`) is read from one run's notes and the reason string, not traced to the skill step that builds `--snapshot` and `--root` | 07 E1-F9, G-1 | Decides whether snapshot and root construction must move from prose into code |
| G-7 | Why EV-1 failures jumped from legacy 3/39 to shadow 8/13, why the sc-adversarial child writes `adversarial/adversarial/`, and why one run made 7 reviewer-agent calls: untraced (no transcripts read) | 06 gap 9; 07 G-3; slice 11 G-3 | Decides how much of the Stage 2 failure is fixed by writing files in code versus by skill-text fixes |
| G-8 | Live behaviour of `superclaude reflect run` engine A with `--transport openai_compat` was never exercised (only stub-transport tests); `runner.py` L120-440 and L620-686 were not re-read by 06 | slice 10 gap 8 (carried only as VL-23-787); 06 gap 6 | All engine-A claims rest on code reading and stubs; its PASS rate and DEGRADED rate on live proxies are unknown |

### Minor (notes; do not block synthesis)

| ID | Gap | Source |
|---|---|---|
| G-9 | Stoprule's fail-closed verdict works live? (`verify-transcript` failed on a real run per slice 12 C2; not read); installed variant scripts vs the phase-5 bundle `cmp` not re-run; stoprule unknown-key handling and `fix_audit.py` (1,131 lines) unread | 03 gaps 1-3; 02 gap 6 |
| G-10 | `@live7` duplicate counts differ by run-id set (slice 01: 30 of 40; slice 02: 26 of 40); the 40 files / +8,026 lines of #519 + #518 not re-derived (file counts 17 + 22 + 0 + 1 = 40 do reproduce, V6) | 01 gap 3 |
| G-11 | Items outside what 06 read: lens output template `reflect-review-output.md`; readers of the 10 engine-A-only contract keys outside `src`; behaviour (not name) of `test_shadow_steps_pin_the_header_model...`; SKILL.md ranges outside its assignment; the 28-run denominator (13 + 15) not diffed | 06 gaps 2, 3, 4, 7, 10 |
| G-12 | Count disagreements in source documents that are resolved by 01 / 08 but still appear in slices and ledgers: "428 reviewer files" (tree has 417), "107 entries" (not reproducible), "9 luna-bearing rows" (tree has 10), `combos/` "95" or "106" folders (96) | 01 gap 7; 08 section 2; research-notes |
| G-13 | Pilot dispatch-collapse "6 of 9 tier3 runs" cannot be re-derived (`/tmp/shadow-logs` absent); r1 / r2 launch models of the combos rest on `PLAN.md:83-89`; no per-run skill hash for pilot runs shadow04-15 | 04 gaps 1, 2; 07 G-2 |
| G-14 | Whether the gateway serves `muse-ember-1.0` today; ember is Tier 4 slot 04 in the live env but "slot 02" in the owner's order (`run-reviewer.sh:26`); `ccsession-models.json` lists only three tier-4 slots | 04 gap 4 |
| G-15 | Who ran `snap.py` (hash identity shows the file equals the script's output, not who wrote it); whether any E2 collaboration harness ran end to end; owner decision on removing the three E2 scripts that write into or read E1's tree | 01 gaps 4, 6; slice 02 Q-E |
| G-16 | The thinking-budget conclusion cannot be recomputed: `/tmp/pc-patterns/records_gt.json` is not among the 12 committed `pc-patterns/` files; the claim is unproven in either direction | 05 Unit 5, gap 5 |
| G-17 | 54 of 319 `merged-anon.md` files name model ids (reviewer-identity leak to the blind judge) were not classified | slice 03 gap 7 (ledger VL-20-249 only) |
| G-18 | `r19` carrying `glm-5.3` three times; `template_sha256` / `tiers_sha256` at HEAD not recomputed (tiers JSON changed) | slice 02 gap 7 (ledger VL-19 only) |
| G-19 | Batch j1 audited only by hand (2 luna refusals would be EXCLUDE under audit B); the corrected AUDIT-CLEAN table (after the `fullpkg()` fix) not recomputed; no artifact for the blind re-judge of 12 rows or `check2.py`; audit-A header counts (930 vs 890 runs, 54 vs 59 WARN) | 08 gaps 4, 6, 10; section 8 |

Questions raised for the synthesis and the owner (design decisions, not research gaps; each is already written in the source file): one finding location type or two (01 gap 9; 02 gaps 11-13); one verdict authority, quorum rule, deferral owner and expiry (03 gaps 5-7); raw-id versus class versus alias dispatch and one tier-data source (04 gap 8); whether the tasklist fidelity prompt becomes a core module (05 gap 7); which of 0.75 / 0.80 and warn / degrade for single vendor (06 gaps 11, 12); central panel builds snapshot, root and card layout in code (07 Q-1); served-model as a first-class field (07 Q-2); acceptance ground truth (07 Q-3); stop-rule and threshold approval (07 Q-4); empty-baseline rule at `reflect_shadow_exit.py:313` (07 Q-5); whether the E2 default `ember + 2x luna` counts as evidence at all (08 gap 9).

## 5. Checklist item 3: depth assessment (Deep tier)

Expected for Deep: end-to-end data flow, integration points mapped, edge cases checked.

| File | End-to-end flow | Integration points | Edge cases / reproduction | Rating |
|---|---|---|---|---|
| 01 | capability matrix across 15 capabilities x 4 programs; item (d2) traced from SKILL.md steps to CLI calls | E1/E2/E3 seams, #518/#519 attribution, E2 write paths into E1 tree | 5 executed probes (annotate KeyError, v1/v2 key split, 200/300 drops, `T01.02`, snap hash) | Deep (one false cell, B-1) |
| 02 | parse -> drop -> merge -> cluster traced for v1 and v2; card format; variants; `panel-msg/1` | tests, E2 designs, `card_convert`, `verify_cmd` | four executed parser variants for `origin`; `T01.01` in three regexes; 92/49 unit derivation | Deep |
| 03 | merge -> ledger -> revise -> verdict; both status machines; 5 verdict authorities | installed variants vs CLI; reflect `derive_verdict` | D-1 (3 variants), D-2 (4), D-11 (3), X1-X3 executed; 8 test pins read | Deep |
| 04 | class word -> env alias -> tier alias -> shim -> served model; four dispatch paths | `ccsession-models.json`, `MODEL-TIERS.md`, shim, E2 harness, E1 engines, `T2bModel01` census | gateway refusal reproduced; collapse counts re-derived from stream logs | Deep |
| 05 | five brief families with the delivery path of each document | `card_convert` filename role resolution, tasklist prompts, E2 harness | `refs_norm` probe on 19 id shapes; `theory.py` set arithmetic | Deep |
| 06 | engine A traced from `runner._audit_once` to `derive_verdict`; engine B shadow steps classified; exit script run | callers (tasklist gate, workflow, tasklist 10.5), lint, tests | contract probe (32 keys, 10 outside, 89 of 110 absent); exit script run twice | Deep |
| 07 | recounts from raw logs and manifests | exit script, replay, Stage 0a, consumer inventory | token share with the orchestrator-alias confound; calibrator collapse found in 6 of 15 | Deep |
| 08 | pilot cells, per-issue table over 106 runs, audits A-F, `final-table.py`, `three-way.py` | E2 tip through `git archive` and `git cat-file --batch` | j1 sensitivity table; permutation tests; `fullpkg()` defect reproduced | Deep |

Missing depth elements: none that block. The remaining depth limits are the logged gaps G-8 and G-11 (engine A live behaviour; some SKILL.md ranges) and G-3 (Claude Code behaviours not documented in the repo).
## 6. Findings table (partition A: research files 01-08)

Grading follows the binding definition: BLOCKING = a real defect (wrong behaviour, false claim, missing required deliverable, security or data-loss risk); MINOR = cosmetic, wording, formatting, citation format, nit, style, or a moved line number on a true claim. Graded by definition, not by label.

| # | Severity | Blocking Y/N | File and location | Finding | Evidence | Proposed fix |
|---|---|---|---|---|---|---|
| B-1 | IMPORTANT | Y | `research/01-overlap-capability-matrix.md` section 4.2 grid row 7 (line 87, E1 = "absent") and section 4.3 "7. Ledger and rounds", E1 row (line 150: "reflect has no fix loop (Tier 3 remediation is a separate opt-in)") | False claim, left unresolved against `06-reflect-two-engines.md`. The reflect code wrapper has a bounded audit, classify, apply, re-verify loop (`--fix`, `config.max_fix_iterations`); it is dormant in production only because engine A emits no remediation pointer. The matrix row feeds report section 2.9 (overlap matrix) and the "ledger and rounds" capability for E1 | `src/superclaude/cli/reflect/runner.py:748-793` (my V1: `while True:` loop; `if not config.fix: break`; `classify_fix(...) != "auto-fixable"`; `_apply_remediation(remediation, iteration, plan=use_plan)`; `iteration > max_iters`; sets `result.fix_iterations`, `fix_converged`); `runner.py:474-478` builds `--remediate` into the prompt under `config.fix`; `06` section 4.2 first bullet and Key Takeaways; `sc-tasklist-protocol/SKILL.md` L1133-L1165 passes `--fix` (06 section 4.1) | In 01 keep "absent" for the finding ledger and rounds in `cli/review`, and replace "reflect has no fix loop" with "the `cli/review` kernel has no ledger, rounds or reviser; the code wrapper `superclaude reflect run --fix` has a bounded audit/classify/apply/re-verify loop (`runner.py:748-793`) that is structurally dormant because engine A emits no `remediation_*` pointer (06 section 4.2)"; cross-reference 06 section 4.2 |
| M-1 | MINOR | N | `01` section 1.2, bullet 3 (line 21) | "`git grep` at the tip finds exactly these three files referencing `brainstorm-reflect-panel`" is literally wrong: the same grep over the E2 eval folder finds 6 files (3 scripts + 3 hand-off / note documents). The substantive point (three scripts touch E1's tree) holds | V6 `git grep -l brainstorm-reflect-panel 6c09843 -- .dev/eval-workspaces/tasklist-review-panel` lists `snap.py`, `drift-b3.py`, `rlog-r3.sh`, `HANDOFF-review-panel-unification-run2.md`, `HANDOFF-run1-vs-run2.md`, `handoff-notes/run2/tests-tools.md` | Say "three scripts (two write paths, one read path) plus three documents that name the worktree in prose" |
| M-2 | MINOR | N | `02` section 2 heading (line 26) | Header says `findings_v2.py` is "305 lines at HEAD"; the same file later says 304 and the file is 304 lines | V3 `wc -l` = 304 | Change 305 to 304 |
| M-3 | MINOR | N | `05` Summary (line 193) vs Unit 6 table and answer (lines 110-118) | Summary says "Four different briefs deliver input"; Unit 6 lists five families and says "four different ways" | the Unit 6 table has rows 1-5 | Say "five brief families, four delivery mechanisms" in the Summary |
| M-4 | MINOR | N | `07` section 4, last bullet (line 82) | "A repository-wide grep for 'stop rule' returned many unrelated hits" does not state that `.dev/tasks/` was excluded (research-notes rule 2 requires it for every repo-wide grep). Nothing from the hits is cited, so no contamination is shown, but the exposure cannot be ruled out from the text | line 82 of 07; research-notes line 151 | Add one sentence stating the scope of that grep (or that `.dev/tasks/` was excluded) |
| M-5 | MINOR | N | `06` section 3 Key Takeaways (line 132) | "so 8 of 13 pilot EV-1 failures are layout mismatches" contradicts section 6.1 (line 236): 3 of the 8 are "no contract" (contract not written), 4 are `merged-verdict: absent`, 1 is `reviewer-cards/ holds 0` | V8 run: EV-1 8/13; 06 lines 236, 243-245 | Say "5 of 8 are layout or naming mismatches and 3 are a missing contract" |
| M-6 | MINOR | N | `06` section 6.2 table (line 245) and section 8(a) item 6 (line 306) | "Across all 59 recorded `reviewer-cards/` dirs, 51 use the `-card` name and only 2 use `reviewer-N.md`": 51 + 2 is not 59, the population is undefined, and the same table lists four runs with `reviewer-N.md` names (shadow15, combo B1-B3). A recount over `.dev/reflect` and the combo runs root finds 84 directories (64 with `-card` files, 5 with `reviewer-N.md` files, 15 with neither) | V-count (batch C4) | State the population (which runs), and use "at least 4 runs use `reviewer-N.md`" or the recounted figures |
| M-7 | MINOR | N | `08` section 5, flips bullet (line 82) | Names 3 "total-loss" merges as the complete set; `audit-D/summary.md` names 5 (adds `h1-haiku-luna2-ember2-r2/designSpec t4-2` and `h1-...-r3/designSpec t4-1`). The conclusion (3 flips, none from total-loss merges) is correct: all 5 last-round verdicts are FAIL / REVISE | V4: ledger `rounds[-1]`: h1-r2 L1 L2 L5 L6; h1-r3 L8; g7 L1; g1 L5; n4 L1, all FAIL / REVISE | List all five, or say "three of the five" |
| M-8 | MINOR | N | `04` sections 3.2, 3.4, 5 (lines 56, 71, 129) | `local-gateway-alias-proxy.py:694-697`, `:698-702`, `:819-839` cited without a directory; the file is `src/superclaude/skills/ccsession-tag/local-gateway-alias-proxy.py` (anchors themselves are correct) | V12: `named_fallback` at :432, `_forward_tier` call at :697 and :702, def at :819 | Give the full repo path on first citation |
| M-9 | MINOR | N | `02` section 5.1 table row 1 (line 97) and `08` section 6 (line 91) | "264 from 89 rows x 3 packages" is the audit's own wording (`run1.txt:1` `merges 264 rows 89`; `summary.md:3`) but 89 x 3 = 267; ledger 20 (VL-20-734) says 88 rows. Both files repeat the source without noting the arithmetic gap | V4 `run1.txt` line 1; 264 / 3 = 88 | Write "264 merges (audit-D's own count; its row count is 89 in `run1.txt:1` and `summary.md:3`, which does not multiply to 264)" |

Totals for partition A: blocking 1 (IMPORTANT), minor 9, zero CRITICAL.

## 7. Observations outside partition A (not graded here; for the consolidator and the other partitions)

These were found while cross-reading files 09-24. They are not defects of files 01-08.
- O-1 `research-notes.md` section B ("9 packaged panel templates incl. 6 `reflect-*`") and scope slice 12 K23 ("9 packaged templates") disagree with file 03 section 1.1 and my V2: `data/` holds 8 `review-panel.*.json` templates plus `review-tiers.default.json` (9 data files; 25 tracked files = 16 `.py` + 9 data). File 03 lists the 8 names but does not flag the discrepancy. Use 8 templates in the synthesis.
- O-2 `17-defect-register.md` DR-075 and its stale-documentation line keep the `T2bModel01` claim `UNVERIFIED`; file 04 section 6 re-derived it as `[CODE-CONTRADICTED]` (18 occurrences in 11 files, reproduced in V11). 17 should cite 04.
- O-3 `13-future-pr-review-and-rfqa.md` (Summary) reports that scope slice 12's "185 spawn lines" could not be reproduced (175 per line, 247 per line and agent; 44 `subagent_type: rf-*` lines exact), while `24-value-ledger-evidence-consumers.md` Summary item 4 and `research-notes.md` section E still carry "185 spawn lines in 7 skills". Two research files disagree and the disagreement is not resolved in 24.
- O-4 `20-value-ledger-e2-study.md` Summary lists as "still open" the combo directory count 95 vs 96 and which alias ground-truth item was caught once; file 01 (96) and file 08 sections 2 and 3 (96 directories; alias GT1 once, GT3 twice) resolve both. 20 also says audit D examined 88 rows while 02 and 08 carry 89 (see M-9).

## 8. Summary

Files reviewed: research/01 through research/08 (completely) with research-notes.md; Summary sections of 09-24; the Gaps and Questions of slices 01, 02, 03, 04, 09, 10, 11.

- Blocking findings: 1 (B-1, IMPORTANT): an unresolved cross-file contradiction and false claim in 01 ("reflect has no fix loop") against 06 and `runner.py:748-793`.
- Minor findings: 9 (M-1 to M-9): count and wording slips, one citation-format nit, one independence-scoping ambiguity (no contamination shown).
- Critical: 0.
- Gate focus: (a) PASS, (b) PASS, (c) PASS (zero hits in 01-08; one MINOR scoping note), (d) not applicable to this partition, (e) PASS.
- Quality of the eight files: high. About 45 line anchors and 18 executed or recomputed figures (13 of 20, 8/13, 0.704, 4,119,747, 216 / 203 / 13 / 6, 14 requested-pinned / 1 observed, 18 `T2bModel01` lines in 11 files, 36 tests, #518 / #519 file counts, r1..r5 `.py` counts, 96 / 19 combo counts, 59 / 11 exclusion flags) were independently reproduced; the only false content found is B-1.
- Gaps: 0 Critical, 8 Important (G-1 to G-8), 11 Minor (G-9 to G-19), all already logged in the topic files or in ledger rows; none is hidden.
- Depth: Deep tier met for all eight files.

Verdict: FAIL (1 blocking: B-1). Re-verification after the fix needs only a re-read of 01 lines 87 and 150 against `runner.py:748-793`; no other file needs a change to clear this gate.

Status: Complete


# Check of adversarial/merged-output.md

Reviewer: independent; read the merged document in full, the base (variant-1), the merge log, and the plan's "Changes NOT Being Made" table. Repo root: /home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel. Cites are `src/superclaude/`-relative unless they start with `.dev/`.

## Verdict

**FAIL** (1 blocking finding open; 11 minor findings). Every other check passed: the owner's list is complete, the constraints hold, the sampled citations are almost all supported, and the data-derived numbers recompute except where listed.

## Blocking findings

### B1. Cost model contradicts itself: the parity lane table shows a 14% saving, but the same section, Q7, candidate C, the H-C gate and the design itself say parity is not cheaper

- **Claim (merged-output.md:481-488, 60, 93, 279, 408).** The lane table gives panel-parity 37k-56k against legacy 42k-66k (midpoint 54k to 46.5k, "about 14% saving"). Line 488 then says "Parity differs from legacy only by +0.5k per card for the findings block (+1.5k) plus possibly shorter cards; do not claim the saving". Candidate C says "Parity with legacy, not a claimed saving" next to 37k-56k. The comparison matrix (line 93) prints 37k-56k for C against 42k-66k for A. Stage 3 exit and H-C allow up to 1.05 x legacy median, which is a parity gate, not a saving gate.
- **Evidence (which side is supported).** The parity side. The parity template resolves the same three classes (verified by running `resolve` on the proposed template: sonnet, haiku, opus). Briefs are unchanged except for one added instruction line. Calibration (3 x 1k-2k) and validator are identical. The debate is kept, with the same 6k-10k. The doc says the reflect card "stays a document" and the findings-v2 block is appended to it (merged lines 165, 314, 373). The only mechanism that changes tokens is an added block, so cost goes up by about 0.5k per card. The lane table's lower primary lane (8-12 vs 10-16) and lower parallel lane (18-24 vs 21-30) rest on V3's rationale "bounded typed findings ... less repeated prose" (variant-3 cost table), which contradicts the design. The doc itself marks shorter cards UNVERIFIED (merged line 491). No measured data supports the saving. The merge log (line 89) records the contradiction and leaves it open.
- **Exact fix text.**
  1. Replace the "Panel-parity, debate kept" lane column by legacy lanes plus the block cost: primary `10-16`, parallel `22-31` (legacy 21-30 plus 1.5), calibrator `3-6`, debate `6-10`, validator `2-4`, total `43-67` (`10+22+3+6+2` to `16+31+6+10+4`; 43.5-67.5 before rounding).
  2. Replace line 488 with: "Midpoint 54k to about 55.5k: parity costs about 1.5k more, not less. The earlier lane-table saving (37k-56k, about 14%) came from an assumed shorter-card effect that this design does not contain and no data supports; it is kept only as the unproven arm-C hypothesis that the first measurement may test (H-C reports it, does not require it)."
  3. In Candidate C Cost, the matrix row "Pre T2 output tokens" and Q7 first bullet, change 37k-56k to "43k-67k (legacy plus about 1.5k); a possible 37k-56k if cards turn out shorter is a hypothesis". Change the "about 14%" wording in Q7 to "no saving is claimed".
  4. Re-derive E' (line 78, 493, matrix) from the corrected parity total minus the debate lane: 43-67 minus 6-10 gives 33k-61k. Keep the "not production behavior" label.

## Minor findings

- **M1. Candidate B contradicts itself on the evidence gate.** Merged B Verdict (line 47) says B "violates the calibration constraint and the evidence gate", but B Keeps (line 41) lists "the evidence-validator" and the comparison matrix (line 90) gives B "Evidence gate kept: yes". Base B Verdict said only "violates the calibration constraint". Fix: revert the Verdict to "...violates the calibration constraint", or change B Keeps and the matrix cell to match what B really drops.
- **M2. Depth-table cite `:323` does not support the claim.** Row `--depth standard` (default, `:323`) cites SKILL.md:323, which is "`--remediate` (depth `standard` default, or `quick`) -> plan route", the remediation depth. Reflect's own default depth is not stated at :84 or in the §5 rows I read. Fix: cite `:84` (`--depth quick | standard | deep`) and `:85` (`--tier auto` is default) and say "the default `--depth standard` is implied by `--tier auto` (UNVERIFIED as a stated default)".
- **M3. Line drift, reflect_review.py.** Line 34 cites `cli/swarm/lenses/reflect_review.py:59-64` for the `T2Model0N` env vars. Lines 59-64 are `default_workers`, `suspect`, `tier="T2"` and the next-command template. The `T2Model0N` statement is at `reflect_review.py:14` (docstring); the prefix constant is `cli/swarm/config.py:59`.
- **M4. "37 of 42" denominator is not reproducible.** Line 416 says 37 of 42 recorded pre contracts are 1.8.0. On disk, `.dev/reflect/pre-*/return-contract.yaml` has 62 files: 1.8.0 x37, 1.0 x8, 1.5.0 x5, 1.7.0 x4, 1.3.0 x4, 1.2.0 x3, none x1. The "42" matches the number of `reviewer-cards/` directories, and those have 40 contracts (35 at 1.8.0). Fix: "37 of 62".
- **M5. Null-score breakdown mixes two sets.** Line 435 says 7 are null (mixed versions, 5 `single-reviewer-fallback`, several illegal values). On disk, 9 contracts carry an explicit null and 18 lack the key. The 7 T2-reached nulls are: `none`, `sc-adversarial-protocol-mode-a`, `adversarial` (reflect-t2-fallback-ladder), `inline-orchestrator` x2, `single-reviewer-fallback` x2. So 2 of the 7 are fallback. The 5 `single-reviewer-fallback` total is over all 62 contracts. Fix: "7 T2-reached nulls (2 `single-reviewer-fallback`, 3 illegal values, 1 `adversarial` with a null score, 1 `sc-adversarial-protocol-mode-a`); 5 `single-reviewer-fallback` contracts in all".
- **M6. Grep inventory counts do not reproduce.** (a) Lines 456 and 461: "31 fixture files carry `merge_method`"; on disk `tests/cli/reflect/fixtures` has 27 files, 25 carry `merge_method`. (b) Line 461: reflect `SKILL.md` "(9)"; that is the `merge_method` count only (9). The stated three-term regex gives 25 lines (`convergence_score` 17, `adversarial_convergence_score` 1). The doc says "counts, not proof of completeness", so this is minor. Fix to 25 and 25 (or restate the pattern).
- **M7. E' cost interval is subtracted wrongly.** 37-56 minus 6-10 gives 27-50 as a worst-case interval, or 31-46 only by subtracting the smaller debate from the low end and the larger from the high end. The doc presents 31k-46k without saying so. Superseded by B1 fix item 4.
- **M8. Circular stage criterion.** Arm C of the first measurement is "`--t2-engine panel`" (line 529). Stage 2 ships only `shadow`; `panel` ships at Stage 3 (line 408), and Stage 3's entry criterion is "first measurement passed". Fix: define arm C as a dev-build `--t2-engine panel` (or as the `shadow` run with parity assertion) and add "the measurement runs on a development build; Stage 3 ships the same code to users".
- **M9. `tier4 -> haiku (stand-in list :28)` (line 207).** Haiku is a direct member of `tier4` (`review-tiers.default.json:10`) and in the anthropic-only `available` list (:27), so the stand-in list is not what selects it (it would also contain haiku, :28). My run of `resolve` on the parity template returned sonnet, haiku, opus for every run id tried. Fix: cite `:10,27`.
- **M10. Unplanned base-text change.** Candidate D's Verdict dropped "and two merges" (base: "leaves two finding formats and two merges"); the plan only asked for "Stages 1-3". It is consistent with the debate being kept, so no harm, but it is not recorded in the merge log.
- **M11. UNVERIFIED label that can be dropped.** "`promotion_gate_passed` null when `mode == pre`, SKILL.md:837 per V1, UNVERIFIED line" (lines 437, 589): SKILL.md:837 reads `promotion_gate_passed: bool | null  # null when mode == pre or Wave 7 skipped pre-gate`. Supported; the marker can be removed.

## Fidelity diff results

Method: Python difflib on the section bodies of candidates A, B, D, Q1 and Q6 (base vs merged, ignoring blank lines and provenance comments), plus a manual read of the base's Finding-format table, Q2-Q5, Q7 and the Assumptions text against the merged text.

- **Candidate A.** Two changes, both planned: Cost "about 49-96k" -> "about 42k-66k ... earlier 49k-96k estimate is a footnote" (Changes 4, 20); Verdict gains "the control arm of the first measurement". Keeps, Risk and the cites (refs/reviewer-spec.md:94-98, SKILL.md:633-651, ensemble.py:787-832, review-tiers.default.json:4-11, reflect_review.py:59-64) are unchanged.
- **Candidate B.** Changes/Keeps/Cost/Risk bullets are identical (408k, 23k + 3 x 88k, 290k, SKILL.md:342, 789, 1483, 1172-1192). One change in the Verdict: "and the evidence gate" added (the plan's text); see M1.
- **Candidate D.** Verdict: "Stage 1" -> "Stages 1-3" (planned); "and two merges" removed (not in the plan; M10). Changes/Keeps/Cost/Risk identical.
- **Q1 table.** 8 of 11 rows are identical (reviewer pool, deterministic choice, diversity, personas, parallel dispatch, telemetry, grounding row; cites panel.py:455-459, 514-525, 405, 408, 402-403, review-tiers.default.json:29 unchanged). Rows changed: exclusion, blind calibration (sidecar removed), merge (`ledger.py:200-298` -> `107-298`), evidence gate. All four are planned (Changes 5, 17, 24, 42). The direct answer lost "plus merge for pre-execution" (Change 42).
- **Q6.** Direct answer rewritten (Changes 17, 29); the Extension-point paragraph is identical except "the K4 ledger id" -> "a future ledger id".
- **Finding-format table.** `id`, `severity`, `blocking`, `claim`, `refs`, `deviation_class`, `coverage_rows`, `self_confidence`, `lens` rows are identical (regex `^[A-Za-z0-9][A-Za-z0-9._-]{0,15}$`, `≤300`, `≤8`, quote 12-200, cites findings.py:91-95, 100-101). Changed rows, all planned: `category`, `anchor` (adds "a finding with neither is invalid"), `citations` (`quote?` optional), `calibrated_confidence` and `validator_status` removed (Change 5), `reflect_category` and `channel` added.
- **Numbers and cites in unchanged prose.** No altered number, field name, table row or threshold found in text the plan did not mark. The PN1 figures (408k, 23k, 68k-108k, 227k-347k), midpoint arithmetic, 15.7 vs 2.8, and 1S+6H vs 1S+3H about 3 defects are intact.
- **Net.** One unplanned deletion (M10), one planned edit that introduced an internal contradiction (M1). No silent loss found in the retyped sections.

## Citation sample table

Paths relative to `src/superclaude/` unless they start with `.dev/`. "R" marks a cite inside a section the plan rewrote (depth-by-tier, contract mapping, invariant resolutions, first measurement).

| # | Cite | Claim | Result |
|---|---|---|---|
| 1 | cli/review/panel.py:402-403 (R) | `fixed` returns `candidates[0]`, ignores `exclude` | SUPPORTED |
| 2 | panel.py:405,408 (R) | random/round_robin use `[... not in exclude] or candidates` | SUPPORTED |
| 3 | panel.py:396-401 (R) | `NoModelAvailable` only when no candidate and no stand-in | SUPPORTED |
| 4 | panel.py:109-111, 46, 140-141, 30, 31, 142 (R) | unknown slot keys rejected; `_SLOT_KEYS`; one fixed slot; tier and slot regexes; 1..8 | SUPPORTED |
| 5 | panel.py:471-476, 455-459, 479, 417, 327-334, 514-525 (R) | round_robin seeded by date; run-id hash seed; exclude = chosen; fallbacks; `@name` load; hashes recorded | SUPPORTED |
| 6 | cli/review/ledger.py:93-96 | `_decision` returns REVISE if n < cap else ESCALATE | SUPPORTED |
| 7 | ledger.py:187-190, 182-199 | OR of blocking, max severity, first member's claim/anchor/category | SUPPORTED |
| 8 | ledger.py:196-197, 278-279, 114-118, 150-157, 86-90 | bare `span`; one `doc_sha256` per round; re-merge refused; empty-block refusal; confidence is reviewer count, no calibration | SUPPORTED |
| 9 | cli/review/findings.py:15-22, 90-101, 91-95 | six-value category enum; id regex; MINOR cannot block | SUPPORTED |
| 10 | findings.py:363-379, 382-407, 321-337 | spans without path; within 3 lines; union-find; `refs_norm` | SUPPORTED |
| 11 | cli/reflect/contract.py:187-194 (R) | major != 1 -> BLOCKED `unknown-major-version` | SUPPORTED |
| 12 | contract.py:31-33, 47-57, 138, 263 (R) | halt set auggie/env-aliases/evidence-validator; load-bearing bools; `derive_verdict`; `_degraded_reason` | SUPPORTED (47-57 start only read to :50) |
| 13 | contract.py:281-284, 295-300, 317-326, 347-352 (R) | triggers 7, 10, 11, 11b (0.80), 13 | SUPPORTED |
| 14 | cli/reflect/ensemble.py:74, 772-773, 765-770 (R) | version constant "1.0"; `tier_reached=2` on count >= 2; benign `reviewer-shortfall` | SUPPORTED |
| 15 | ensemble.py:787-832, 797, 806, 808-819, 825-831 (R) | constants `verification_ran False`, `citations_dropped 0`; `"mode": "post"`; isolation telemetry | SUPPORTED |
| 16 | cli/reflect/runner.py:103-133 (R) | `reflect_post` fields and order, three `*_verified` at end | SUPPORTED |
| 17 | cli/reflect/config.py:53-56, 351-355 | `executor_model_class` frontmatter key, `EXECUTOR_MODEL_CLASS` env | SUPPORTED |
| 18 | agents/reflect-reviewer.md:5-8, 6, 30 (R) | read-only tools, `model: sonnet`, `permissionMode: plan`; advisory slot never Regression | SUPPORTED |
| 19 | skills/sc-reflect-protocol/SKILL.md:362-366, 364, 365, 363 (R) | `--tier 1`, `--depth quick`, `--depth deep`, `--tier 2` routing | SUPPORTED |
| 20 | SKILL.md:262-273 (R) | budget rows: N<5 STOP, N=5 T1, 6<=N<52 + N<65 downgrade, N>=65 none | SUPPORTED |
| 21 | SKILL.md:323 (R) | "`--depth standard` (default)" | NOT SUPPORTED (it is the `--remediate` depth default; M2) |
| 22 | SKILL.md:1483, 663, 789, 952-953 (R) | condition 9 operative test `adversarial_unavailable == true`; null blocks promotion; legal values; minor/major rule | SUPPORTED |
| 23 | SKILL.md:600, 602, 604-608, 610, 612 (R) | exclusion rule, WARN text, unknown executor, rotation, N=2 hard, judge not pinned | SUPPORTED |
| 24 | SKILL.md:1172-1192, 1181-1186, 1204-1214 | blind calibration, calibrator selection, sampled `citations_dropped` | SUPPORTED |
| 25 | skills/sc-reflect-protocol/refs/cost-profile.yaml:36-39, 46-51, 70 (R) | T1 3k-8k + 2k-5k; T2 35k-70k + 10k-25k; kill multiplier 1.25 | SUPPORTED |
| 26 | refs/reviewer-spec.md:31-74, 45, 53-57, 94-98, 102, 108-109, 112-116 | three sections, H3 hunks, qa hunks, rotation, post-removal, judge | SUPPORTED |
| 27 | cli/review/data/review-tiers.default.json:4-11, 6, 14, 20, 23, 27-29 (R) | tier lists; tier1b three models; Fable in `available` and `launch`; gateway launch empty; no tier1b stand-in | SUPPORTED |
| 28 | cli/review/panel_cmd.py:18-52; merge_cmd.py:29-34, 76-79, 113-116 | resolve options; single `--doc`; reads reviewer_id/model; report written before ledger saved | SUPPORTED |
| 29 | cli/swarm/lenses/reflect_review.py:59-64 | `T2Model0N` env pool | LINE DRIFT: true line 14 (M3) |
| 30 | cli/reflect/_diversity.py:8-15 (R) | `insufficient` not `degraded` | SUPPORTED |
| 31 | skills/sc-workflow-protocol/SKILL.md:60-64 | default-flag reflect call; advisory | SUPPORTED |
| 32 | skills/sc-adversarial-protocol/SKILL.md:407-410, 439, 457, 948-951 (R) | skip debate under 10% difference; null score if debate not reached | SUPPORTED |
| 33 | skills/task-builder/SKILL.md:2242; sc-implement-protocol/scripts/archive_workspace.py:327; refs/ops-integration.md:239 (R) | EV-4 requires `merge_method: adversarial`; `!= "1.1"`; PromQL label | SUPPORTED |
| 34 | .dev/research/346-review-loop-experiments/p17/LEDGER-RESULTS.md:19, 49, 66 (R) | 15.7 vs 2.8, 408,316; circularity; Haiku 68k-108k vs 23k | SUPPORTED (2.8 is on :13; the :19 row has 15.7 and 408,316) |
| 35 | docs/reference/review-panel-live7.md:19-26 | 1S+6H vs 1S+3H about 3 defects | SUPPORTED (15.7/15.3 vs 19.3/17.7, "about 3 fixed defects per run") |
| 36 | .dev/reflect/pre-TASK-WF-brainstormFixBri-.../return-contract.yaml:96-97 (R) | `executor_class_source: unknown`, `executor_class_resolved: false` | SUPPORTED |
| 37 | .dev/research/.../builds/stoprule/.../nested/reflect-1/reviewer-cards/reviewer-1-card.yaml:82-103 (R) | calibration block, F1-F3 at 0.60/0.50/0.55, line-ref evidence, `model_class: sonnet` | SUPPORTED |
| 38 | .dev/eval-workspaces/sc-reflect/grader.py | no `merge_method`/`contract_version`/`convergence` match | SUPPORTED (0 matches) |
| 39 | tests/cli/reflect/fixtures (31 files with `merge_method`) | count | NOT SUPPORTED: 25 of 27 (M6) |

Sampled: 39 rows covering about 110 individual line cites; 2 not fully supported (rows 21, 39), 1 line drift (row 29). More than 5 are from rewritten sections (rows 1-5, 11-16, 18-23, 25, 27, 32-34, 36, 37).

## Number checks

All recomputed from the disk data or by arithmetic.

| Claim | Recomputed | Result |
|---|---|---|
| 38 pre tier decisions; 37 tier 2, 1 tier 1 (a `--tier 1` pin) | 38 `tier_decision.yaml`; `selected_tier` 2 x37, 1 x1; the 1 has `override: "--tier 1"` (pre-pr-submit-ci-monitor) | OK |
| 34 carry `coverage_degraded: parsed-sparse`; 21 sc-workflow packages; 2 forced by `--depth deep`; 0 rubric stops | 34; 21 directories with `WF` in the name; 2 mention depth deep (pre-uc2-reachability-*); no row with a rubric T1 stop | OK |
| Fired rules "4, 5 or 6" | rule 4 x18, 6 x10, 5 x2, 8 x1, 0 x1, null x6 (the 6 null include the pin) | OK (also rule 8 x1, not named; harmless) |
| 42 `reviewer-cards/` dirs, 33 with `merged-verdict.yaml` | 42; 33 | OK |
| 37 of 42 contracts at 1.8.0 | 37 of 62 | M4 |
| 14 of 35 numeric scores below 1.0; 21 equal 1.0 | 35 numeric over all 62 pre contracts; 21 == 1.0; 14 < 1; range 0.40 to 0.9615 | OK |
| 7 null | 9 explicit null (7 at T2, 2 at T1); 18 contracts lack the key | OK for "7 at T2", wording M5 |
| One pre run scored 0.76 | `adversarial_convergence_score: 0.76` in pre-TASK-WF-writeTheP0LivePl-... | OK |
| Legacy lane sum 42-66 | 10+21+3+6+2 = 42; 16+30+6+10+4 = 66 | OK |
| Panel lane sum 37-56 | 8+18+3+6+2 = 37; 12+24+6+10+4 = 56 | OK as arithmetic; the lane inputs are contradicted (B1) |
| Midpoints 54 and 46.5; about 14% | 7.5/54 = 13.9% | OK |
| Kill line 65 | 52 x 1.25 = 65; 52.5 x 1.25 = 65.6 | OK |
| B cost about 290k | 23 + 3 x 88 = 287 | OK |
| Full-panel parallel lane 227k-347k | 23 + 204 = 227; 23 + 324 = 347; vs 54k midpoint: 4.2x-6.4x ("4-7x") | OK |
| E' 31k-46k | 27k-50k as an interval; 31-46 only by pairing mismatched ends | M7 |
| n = 618 x d | (1.645 + 0.842)^2 = 6.185; /0.10^2 = 618.5 | OK |
| d = 0.10 / 0.20 / 0.30 -> 62 / 124 / 185 | 61.9 / 123.7 / 185.6 (rounded 186) | OK (185 is a floor; immaterial) |
| H-A n = 275 x d; d = 0.35 -> 96 | 6.185/0.15^2 = 274.9; x0.35 = 96.2 | OK |
| Pilot power d = 0.10, 60 defects: about 79% | SE = 0.0408; z = 0.10/0.0408 - 1.645 = 0.80 -> 78.9% | OK |
| Pilot power d = 0.20: about 54%, SE 0.058, bound 0.095 | SE 0.0577; z = 0.087 -> 53.5%; bound 1.645 x 0.0577 = 0.095 | OK |
| 33 plans at d = 0.20 | 618 x 0.2 x 1.3 / 5 = 32.1 -> 33 | OK |
| Per-plan arms A+B+C 73k-148k; pilot 0.9M-1.8M; 33 plans 2.4M-4.9M | 3+35+35 = 73; 8+70+70 = 148; x12 = 876k-1,776k; x33 = 2.41M-4.88M | OK |
| Parity template resolves sonnet, haiku, opus; lite resolves sonnet, haiku, haiku; x2 resolves haiku + a tier1a pick | ran `panel.validate_panel` (no errors) and `resolve` (5 run ids each) in anthropic-only | OK (x2 gives haiku, opus only once the executor class sonnet is hard-excluded, which is the PROPOSED kernel change; unexcluded it gives haiku, sonnet) |

## Owner's list check

| Item | Present | One-line judgement |
|---|---|---|
| >= 3 candidate architectures incl. leave-as-is | yes (A, B, C, D, E') | Five candidates with Changes/Keeps/Cost/Risk/Verdict; A is the control arm. Cost cells need B1. |
| Chosen architecture and reasons | yes (C, 6 reasons) | Reasons are specific and cite code; reason 3 (debate kept) is supported by the recorded 14-of-35 evidence. |
| Q1-Q7 answers | yes | Q1 table, Q2 pointer to the finding format, Q3 debate-kept with judge identity, Q4 engine, Q5/Q6/Q7 direct answers in place. |
| Finding format | yes (findings-v2 table, mapping, completion/channel, cluster_v2) | A strict superset with conversion rule for recorded cards; calibration stays embedded. |
| Pre and post adapter sketches | yes (12 pre steps, 8 post steps, shadow mode, execution contract) | Executable step-by-step with the flag read after the final tier. |
| Staged migration, pre behind a flag first | yes (Stages 0-6, `--t2-engine` default `legacy` until Stage 4) | Sound except the arm-C circularity (M8). |
| Return-contract 1.8.0 mapping: merge_method, convergence score names, null-score rules, gate 9, `reflect_post`, each consumer | yes, all six, plus a deferred 2.0.0 consumer list | Contract unchanged, bump rule stated, lint test proposed; consumers enumerated one by one. |
| Cost model with depth table (`--depth quick/standard/deep`, `--tier`) | yes | Depth table is thorough (also budget rows, `--unattended`, headless); lane numbers need B1. |
| Risks | yes (12-row table with probability, impact, mitigation) | Adequate. |
| First measurement | yes (H-A/H-B/H-C, arms A-D, sample size, strata, Stage 0a) | Power math verified; one sequencing flaw (M8). |

## What I checked and did not check

**Checked**
- Full read of merged-output.md (623 lines), merge-log.md, the base (458 lines), the plan's "Changes NOT Being Made" table and Change 40 text.
- Section-level difflib of base vs merged for A, B, D, Q1, Q6; manual comparison of the Finding-format rows, Q2-Q5, Q7 and Assumptions.
- 39 citation rows (about 110 line cites) read at the cited lines, including all cites to cli/reflect/contract.py, cli/review/panel.py, ledger.py, findings.py, ensemble.py, agents/reflect-reviewer.md, SKILL.md, refs, the stoprule card, LEDGER-RESULTS.md and a recorded reflect contract.
- Recomputed every count that depends on `.dev/reflect/pre-*` and the PN1 and power/cost arithmetic; ran the proposed parity, lite and x2 templates through the real `panel.validate_panel` and `resolve`.
- Constraints: contract stays 1.8.0 in Stages 0-4 with a named consumer list and a lint gate (OK); blind calibration kept per card and the evidence-validator kept with a flag-only pre-check (OK, at least as strong); Fable and Tier 0 appear only as forbidden and as a kernel-rejection rule (OK); Opus uses enumerated and no use is new (OK); no instruction tells an installed primitive to read `src/superclaude` (3 hits, all in the conventions paragraph, OK); UNVERIFIED markers remain where lines were not read (OK).
- Consistency: merge_method is `adversarial`/`single-reviewer-fallback` in every pre and post stage and `panel` only in E'; calibrator stays `degraded` for the parity template and becomes `full` only in the lite arm; the N=2 floor counts complete reviewers of distinct classes in D3, Q4 gate 8, Guards, Completion and the mapping; the engine flag is read after the final tier in D1/D2, pre step 1-2, Q5 and Stage 2; the panel is skipped at `--depth quick`, `--tier 1`, `--no-escalate`, rubric stops, N<6 budgets. The only contradictions found are B1, M1 and M8.
- The parity-cost contradiction the merger flagged is B1: the evidence supports +0.5k per card, not a 3k-6k saving.

**Not checked**
- Rubric rows 3-7 (SKILL.md around :383-399) and the claim that they drive the table row label; `SKILL.md:1180` vs enrichment calibrator vocabulary beyond lines read.
- Bodies of `cli/reflect/fallback.py`, `cli/review/telemetry.py`, the sprint executor, `refs/report-template.md`, the Agent-tool reply model id, whether the `reflect-reviewer` tools allowlist survives a `model` override, and the `sc-adversarial` judge-exclusion input (all stay UNVERIFIED in the document; I did not read them either).
- `REPORT.md:130-132` of the stoprule run (doc marks it unread).
- Whether the "21 sc-workflow packages" count matches the document's definition (I counted directory names containing `WF`).
- I did not re-run the full repository grep inventory beyond the files and counts listed in M6.

# QA Report — Research-Gate Qualitative Review (Partition 2 of 2)

**Report reviewed:** research files 07-12 of `.dev/tasks/to-do/TASK-RESEARCH-review-panel-unify-20261113-155942/research/` (07-reflect-merge-contract, 08-run-recording-telemetry, 09-consumer-plugpoints, 10-future-consumers, 11-evaluation-evidence, 12-test-pins-regression)
**Lens:** research-depth
**QA phase:** research-gate (rf-qa-qualitative, partition 2 of 2)
**Date:** 2026-11-13
**Fix authorization:** false (report only)
**Fix cycle:** N/A (first review)

[PARTITION NOTE: Cross-file checks limited to assigned subset (07-12). Full cross-file verification requires merging with partition 1.]

---

## Findings

| # | Severity | File | Section | Finding | Proposed remedy |
|---|----------|------|---------|---------|-----------------|
| 1 | MINOR | 07-reflect-merge-contract.md | §5.1 "Reading of the output" | Heading says "Failing criteria (4 of 6)" but the list holds 3 failing criteria plus a 4th bullet marked "(passing)"; the Key Takeaways say "three criteria" plus the run count. Wording only; the counts beneath are correct. | Re-label as "Failing: run count + 3 of the 6 checks" and move the passing bullet out of the failing list. |
| 2 | MINOR | 07-reflect-merge-contract.md | §9 Key Takeaways | "12 of 16 constraints are code-backed", but the table marks 13 rows CODE-VERIFIED (C1-C4, C6-C12, C14, C15); C5 is protocol-only, C13 process, C16 partly contradicted. Off by one, or C15 (checked by test names only) was left out without saying so. | State 13, or say 12 and name C15 as checked by test names only. |
| 3 | MINOR | 08-run-recording-telemetry.md | §8.2 Audit D results | Audit A results carry a snapshot date ("2026-11-13 ~01:12 UTC", 890 runs) but the audit D numbers (49 dropped blocking findings, 16 stale, 3 verdict flips) carry a sample size (264 merges) and no date. | Add the audit-D summary's date, or "date not stated in summary.md". |
| 4 | MINOR | 09-consumer-plugpoints.md | §2.4 installed-only variants | "Each variant is a full fork of the 490-line base" is stated as fact, but no diff was run, and all five variants are shorter than the base (472-483 lines vs 490, re-counted with `wc -l`). The conclusion that a change to `spec-panel.md` will not reach them holds anyway. | Say "each variant is a separate 472-483-line copy derived from the base (not diffed)". |
| 5 | MINOR | 07-reflect-merge-contract.md (cross-file with 11) | §5.1 item 2; §5.1 "[UNVERIFIED] which runs predate the fix commits" | 07 says both parity-failure causes "are the defects fixed in skill text by `9874d63fb`/`c2e3347d3`" and leaves run timing unverified. 11 §8 settles the timing from file mtimes and brief text: shadow15 ran after `9874d63fb` and still lacked `reviewer_personas`/`reviewer_models` (an orchestrator lapse, not a fixed text defect). `c2e3347d3` touched only the findings-heading line in `refs/reviewer-spec.md` (re-checked with `git show --stat`: reviewer-spec.md + one test). 07 hedges, so this is not a false claim, but a synthesis that reads 07 alone could call the parity failures "fixed". | In 07, cite only `9874d63fb` for the parity causes and point to 11 §8 for the per-run before/after-fix classification. The synthesis should take 11 §8 as authoritative. |
| 6 | MINOR | 11-evaluation-evidence.md | Summary (last paragraph, [E2] sentence) | The Summary says "2-reviewer panels as good as 3-reviewer ones" with no caveat. The body (§12 item 2 and its Verdict) correctly limits this to E2's setting (spec-panel critique, deterministic merge, n=4 per 2-reviewer panel, no 2-vs-3 test run). The Summary drops the scope and sample size. | Add "(in E2's setting, n=4 per panel, untested)" to the Summary sentence. |
| 7 | MINOR | 12-test-pins-regression.md (cross-file with 07) | §0 "Correction to the task prompt", §2 heading, §8 G9 ("remaining 33 files"), Gaps, Summary | 12 says `tests/cli/reflect/` holds **37** test files; 07 §4 says **38**. Re-checked: `ls tests/cli/reflect/test_*.py` gives 38, and pytest collection finds tests in all 38 files, 353 items total. So 07 is right and 12 is off by one, which also makes G9 "the remaining 33 files" really 34. 12's item totals (353, 82 panel, 271 legacy, 1182) are correct, and the G9 command (`uv run pytest tests/cli/reflect`) is directory-based, so no gate or migration step changes. The synthesis must not copy the 37. | Change 37 to 38 and 33 to 34 in 12 (§0, §2, §8 G9, Gaps, Summary). |

## Per-file depth rating

- **07-reflect-merge-contract.md — Deep.** Every constraint C1-C16 is re-checked and says what it blocks; the 14 recorded runs are tabulated (convergence vs `cluster_agreement`, placement, judge identity) and each Stage 2 failure is classified by cause (unquoted `[1m]` YAML, header from harness, nested verdict path, missing personas, extra keys). The merge question gets two concrete options with their contract cost, and the conclusion stays modest ("the recorded data cannot show the debate adds information ... nor that the script is as good"). Spot-checks held: `contract.py:187-194` major-1 gate, `:294-296` only `single-reviewer-fallback` read, `:317-326` 0.80 floor; `panel_lint.py:290-291` F3 strictness, `:360-365` bump line; `test_shadow_skill_contract.py:43,:53` HEAD-relative; SKILL.md:1958 `memory_status`; shadow04 contract line 103 `[1m]` flow list. The 9-of-14 and 10-of-11 counts were recomputed from the §7.2 table and match.
- **08-run-recording-telemetry.md — Deep.** It goes field by field through the manifest, review-telemetry/1, the E2 runner records and audits A/D. For each audit check it names where a built-in check would hook and what the product lacks today (§8.3), and it says which effort supplies which third of a run record (§11.1). The design input (§11.3) is nine concrete, code-anchored proposals. Spot-checks held: `telemetry.py:22/23/24` (`_TS`/`_ID_TOKEN`/`_ID_RE`), `:112` STRATA, `:371` tokens_out-only cost; `manifest.py:353` hash-only payload; `merge_cmd.py` imports with no telemetry; E2 `run-reviewer.sh:58/:75-76/:87` expected_model overwrite and `cost.json` sum.
- **09-consumer-plugpoints.md — Deep.** It maps each consumer (workflow Wave 4, tasklist Stage 10.5 and the per-phase post gate, brainstorm, design, spec-panel) to its exact plug point, states whether it is advisory or blocking, and lists the ids each one uses. It answers "does default reflect pre reach Tier 2" with the rubric rows and the `--t2-engine` default. It traces the ghost `lint_cmd`/`estimate_cmd` names to the PN2/PN3 branch commits (new evidence). §8 gives eight concrete design inputs. Spot-checks held: `cli/review/__init__.py:19-36` loader with the `_exc.name` narrow swallow; `sc-tasklist-protocol/SKILL.md:1646` "ships regardless of verdict"; spec-panel base 490 lines and five installed variants.
- **10-future-consumers.md — Deep.** The PR seam analysis names both entry points (finder vs S2b verifier) with the code each needs. The rubric-vs-router comparison gives seven concrete divergences (D-a to D-g), each correctly hedged "[UNVERIFIED as a bug]". The rf-* census is per call site (39 rows, with phase, inputs, fix authorization, verdict format and whether an in-place fix is needed); its arithmetic holds (37 review sites = 28 fix-dependent + 3 read-only + 4 read-only-then-fix + 2 unverified). The X1-X13 exposure list ties each item to a consumer need and today's code. Spot-checks held: `rf-qa.md:41`/`:92` and `rf-qa-qualitative.md:41`/`:91` self-contradiction; test bans only "surfaces zero issues as suspect" (`:146`); `reviewers.py:41` closed tuple; `severity_router.py:191-193` deep drop; `findings_v2.py:36` closed `LENSES`.
- **11-evaluation-evidence.md — Deep.** This is the strongest file in the partition. Every Stage 2 failing run from 08 to 15 is classified (harness defect / skill-text defect already fixed / real panel defect) using file-mtime timing against both fix commits and brief-text evidence. It finds that no run exercised `c2e3347d3`. Every quantitative claim carries n and a date (E2 n=4-6 per panel, 2026-11-12/13; combo n=3, 2026-11-13; pilot n=3 packages, 2026-11-11). Conclusions stay proportionate: "no panel significantly better" (p 0.54-1.0); "no valid-success verdict is implied" for the #346 bundle; H-A not measured. It also adds new evidence: the "blind" judge sees the combo name (`judge-one.sh:21`), duplicate models in E2 resolutions, and the combo-A orchestrator served by GLM/Qwen. Spot-checks held: a recount with `jq` over the comboA-r1 log gives exactly 150 `glm-5.3` + 63 `qwen3.8-max` top-level turns, and comboB-r1 gives 133 `claude-sonnet-5-5`; `git show --stat` confirms the scopes and timestamps of `9874d63fb` (01:54:25Z) and `c2e3347d3` (02:57:12Z, reviewer-spec.md + one test only).
- **12-test-pins-regression.md — Deep.** It uses real collection counts (1182 = 651 + 353 + 178). It names each test that pins a defect, with the assertion line and the replacement assertion (§3, §9). It lists the uncovered defects with the probe used (§4), the goldens with what regenerates them (§5), and an eleven-suite no-regression gate list with item counts (§8). Spot-checks held: `test_review_ledger.py:376-385` asserts `"resolved"` with one broken reviewer, which matches the hand-off's D2 definition ("even if the reviewer's block was invalid") against `ledger.py:254-258`; `ledger.py:150-157` refuses only when zero blocks are valid; 19 files in `tests/review`. The one count error is finding 7.

## Verdict

**PASS** — 0 CRITICAL, 0 IMPORTANT, 7 MINOR (notes only; not rechecked).

All six files are rated Deep against the six lens questions:
1. Key findings are actionable, each tied to a file:line and a named design or migration consequence.
2. The analysis goes past surface reading: C1-C16 each say what they block (07 §9); runs 08-15 are each classified (11 §8); the 39 rf-* call sites each say whether a read-only panel can replace them (10 §3).
3. Every assignment's design-input question gets concrete options with evidence (07 §10 Q1/Q8, 08 §11.3, 09 §8, 10 §5 X1-X13, 11 §12, 12 §8-9).
4. Each claim carries an E1/E2/E3 tag and states what each effort chose and why.
5. Quantitative claims carry sample size and date.
6. Conclusions match the evidence: no valid-success verdict for the bundle, non-significant E2 differences, unmeasured H-A, a debate-vs-script question that cannot be decided on recorded data.

Two notes for the merge step: 07's run-timing gap is resolved by 11 §8 (finding 5), and the reflect test-file count is 38, not 37 (finding 7).

## Self-Audit

**(a) Reliance list — structural PASS items relied on:**
- The spawn prompt held no `## Inherited Structural Verdict` block, so nothing was inherited and I did not re-run structural checks (file existence, section numbering, citation format). That is the job of the rf-qa partitions.

**(b) Independent semantic checks (my own tool work):**
- 07 contract claims: read `contract.py:175-329` (major-1 gate, trigger order, 0.80 floor, `merge_method` only for fallback) and `panel_lint.py:240-365` (F3 strictness at :290-291, bump line); Grep of `test_shadow_skill_contract.py` for HEAD (:43, :53, :83); Grep of SKILL.md for `memory_status` (:1958 only); Grep of shadow04 contract line 103 (`[1m]` flow list). Recomputed the 9/14, 10/11 and 6/14 counts from the 07 §7.2 table.
- 08 telemetry and runner: Grep of `telemetry.py` (`_TS`:22, `_ID_TOKEN`:23, `_ID_RE`:24, `STRATA`:112, tokens_out at :371); Grep of `manifest.py:353` and `merge_cmd.py` imports; `git show 4a22d742:.../run-reviewer.sh` lines 44/58/75-76/87.
- 09 plug points: read `cli/review/__init__.py` in full; Grep of tasklist SKILL.md:1646; `wc -l` of spec-panel base and the 5 installed variants (finding 4).
- 10 consumers: Grep of rf-qa / rf-qa-qualitative for the "0 issues is suspect" wording vs "no minimum count", and of the banned phrase in `test_review_prompt_overrides.py:146`; Grep of `reviewers.py:41`, `severity_router.py:191-193`, `findings_v2.py:36`. Re-did the census arithmetic.
- 11 evidence: `jq` count of top-level assistant models in the comboA-r1 and comboB-r1 stream logs; `git show --stat` of both fix commits.
- 12 pins: listed `tests/cli/reflect` and ran pytest collection with the cache disabled (38 files, 353 items, finding 7); read `ledger.py:108-157`, `:236-265` and `test_review_ledger.py:374-386`; checked the D2 definition in `scope/00-handoff-copy.md:106` and `02-review-cli-code.md:162`.

**Self-audit answers:**
1. Claims checked against source myself: about 40 (listed above).
2. Files read for checking: `contract.py`, `panel_lint.py`, `test_shadow_skill_contract.py`, reflect `SKILL.md`, the shadow04 `return-contract.yaml`, `telemetry.py`, `manifest.py`, `merge_cmd.py`, E2 `run-reviewer.sh` (via git show), `cli/review/__init__.py`, tasklist `SKILL.md`, `rf-qa.md`, `rf-qa-qualitative.md`, `test_review_prompt_overrides.py`, `reviewers.py`, `severity_router.py`, `findings_v2.py`, `ledger.py`, `test_review_ledger.py`, the combo stream logs, the scope hand-off and slice 02.
3. Findings: 7 (all MINOR). That is not zero, and every blocking-candidate claim I tried to break held up.
4. Web research: none performed. Every check was local, so Tavily was not needed.

## Confidence

- Lens questions × files: 6 × 6 = 36 checks. Verified: 36 | Unverifiable: 0 | Unchecked: 0 | **Confidence: 100.0%**
- Tool engagement: Read 15 | Grep 9 | Glob 0 | Bash 6 (one pytest collection with the cache disabled; the rest read-only).
- Limits: I spot-checked claims rather than re-deriving every line citation in about 380 KB of research. Line-level citation accuracy belongs to the rf-qa evidence partitions. Partition 1 (files 01-06) was not read.

## QA Complete


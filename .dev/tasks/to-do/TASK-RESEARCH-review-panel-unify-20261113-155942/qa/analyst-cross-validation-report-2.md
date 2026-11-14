# Research Completeness Verification (Partition 2 of 2) — cross-validation lens

**Topic:** Unified Review Panel (E1 reflect Tier 2 / E2 tasklist panel study / E3 #346 review loop)
**Date:** 2026-11-13
**Analysis type:** completeness-verification, lens = cross-validation (checklist items 6, 7, 8)
**Assigned files:** research/07-reflect-merge-contract.md, 08-run-recording-telemetry.md, 09-consumer-plugpoints.md, 10-future-consumers.md, 11-evaluation-evidence.md, 12-test-pins-regression.md
**Depth tier:** Deep
**fix_authorization:** false (report only)

[PARTITION NOTE: Cross-file checks cover the assigned subset plus every other research file and scope slice that makes a claim about the same component, as the prompt requires. Full cross-file analysis requires merging with partition 1.]

---

## Verdict: FAIL — 1 blocking finding (IMPORTANT), 9 MINOR notes

The six assigned files are deep, source-traced and mostly agree with each other. One blocking gap: the Python Tier 2 path behind the only blocking reflect consumer (`src/superclaude/cli/reflect/ensemble.py`, used by `superclaude reflect run`, which the sc:tasklist per-phase post gate calls) writes `return-contract.yaml` and sets `merge_method` in code. None of the assigned files examines it. Files 07 and 08 leave open exactly the questions this code answers (who writes the contract, who writes `merge_method`, who writes `verification_verified`/`reviewers_verified`/`regression_verified`/`adversarial_subrun_status`). Their merge-path conclusions cover the skill (UC-1) path only. Details in Finding 1.

What I checked: research-notes.md; scope slices 00-05 (relevant sections); every line of files 07-12; the partition-1 files (01-06) at every place that makes a claim about the same component (grep for shared numbers and ids); and direct code or data checks of 11 claims (listed under each contradiction).

---

## Coverage Audit (item 1, outside lens: defects only)

| Scope item (research-notes SUGGESTED_PHASES rows 7-12) | Covered by | Status |
|---|---|---|
| Reflect merge path, C1-C16, EV-1, `panel_lint`, `contract.py`, shadow exit | 07 | COVERED, except the Python UC-2 ensemble path (`cli/reflect/ensemble.py`), which scope slice 04 names as a contract producer (`04-this-session-artifacts.md:100`) and slice 03 lists as UNVERIFIED (`03-reflect-side.md:63, :219`). GAP (Finding 1) |
| Run recording: manifest, telemetry, E2 meta/cost/fallback, audits A/D, extract.py | 08 | COVERED |
| Consumer plug points, D13, D14, CLI surface | 09 | COVERED |
| PR review seam, rf-* census, exposure list | 10 | COVERED |
| E2 harness, E1 shadow harness, Stage 2 classification, combo study, bundle verdicts | 11 | COVERED |
| Test inventory, defect pins, goldens, gate list | 12 | COVERED |

## Evidence Quality (item 2, outside lens: defects only)

| Research file | Evidence | Rating |
|---|---|---|
| 07 | file:line on nearly every claim; live script output pasted verbatim; per-run artifact table | Strong |
| 08 | file:line throughout; E2 files read via `git show` with line numbers | Strong |
| 09 | file:line, git refs, `--help` output, grep results | Strong |
| 10 | file:line per census row; I spot-checked 5 citations, all correct (`task-builder/SKILL.md:1422`, `rf-analyst.md:281`, `rf-qa.md:41`/`:92`, `sc-reflect-protocol/SKILL.md:632-633`, `test_review_prompt_overrides.py:140-148`) | Strong (one count mislabelled, Finding 5) |
| 11 | file:line; E2 `git show` cites; run mtimes and stream logs | Strong |
| 12 | counts from a real `pytest --collect-only`; test bodies read | Strong (two small errors, Findings 6 and 7) |

No pattern of unsupported claims. Unverified items are tagged.

## Documentation Staleness (item 3, outside lens)

All six files tag doc-sourced claims with [CODE-VERIFIED] / [CODE-CONTRADICTED] / [UNVERIFIED] or list them under "Stale Documentation Found". No [CODE-CONTRADICTED] claim is reported as current fact. No defect.

## Completeness (item 4, outside lens)

| File | Status | Summary | Gaps section | Key Takeaways | Rating |
|---|---|---|---|---|---|
| 07 | Complete | Y | Y | Y | Complete |
| 08 | Complete | Y | Y | Y | Complete |
| 09 | Complete | Y | Y | Y | Complete |
| 10 | Complete | Y | Y | Y | Complete |
| 11 | Complete | Y | Y | Y | Complete |
| 12 | Complete | Y | Y | Y | Complete |

## Cross-reference check (item 5, outside lens)

Links between files that the files themselves do not make, but synthesis needs (all MINOR; listed so synthesis does not drop them):
- 08 Gap 13 ("which audit-D script replays `_check_finding`") is answered by 02 §4: `AD/audit2.py` `check` (:8-30) copies `findings._check_finding` (`02-ledger-merge-verdict.md:119`). The E2 summary itself says "Cause measured by replaying findings.py parse rules (_check_finding)" (`audit-D/summary.md`, read via `git show 4a22d742`).
- 11 §8 classifies shadow09, shadow11 and shadow14 by exit-script result only. 07 §7.3-7.5 shows shadow09 had no debate artifacts and used `cluster_agreement` as its convergence score, and that shadow11 skipped the debate on `cluster_agreement` (step 6 forbids both). 11 shows shadow14's orchestrator rewrote reviewer headings (step 4 forbids that). Together the two files show that "exit-clean" runs still broke shadow rules; neither file says so alone.
- 06 line 263 (23 of 45 produced briefs break the three-section shape) qualifies 07 §9 C7 and 12 §6 C7, which describe C7 only as a pin on the template text.

---

## Contradictions Found (item 6, lens)

Each row: the two sides, which side has the stronger code evidence, my own check, and whether it is resolved. A contradiction that the evidence settles is marked RESOLVED and is a MINOR note; one that the evidence does not settle is UNRESOLVED and blocking.

| # | Component | Side A | Side B | Stronger evidence / my check | Status |
|---|---|---|---|---|---|
| C-1 | Stage 2 exit status (files 07 vs 11) | 07 §5 and §10 Q7 | 11 §8 | **Agree on every number:** exit 1, 13 of 20, shadow02 incomplete, EV-1 8/13 vs legacy 3/39, parity fails 04/05/07/08/09/15, lint/manifest problems in 9, clean 10/11/12/14, compliance 0.704 over 9 runs, `cluster_agreement` 1.000 over 9 runs, 42 legacy runs replayed, 0 new reasons. Scope slice 03 §1.2 matches. I recomputed the compliance mean from 11's per-run values (03 1.0, 05 0.33, 06 1.0, 07 0.333, 10 1.0, 11 0.67, 12 1.0, 13 1.0, 14 0.0 = 6.333/9 = 0.704) and the `cluster_agreement` set from 07 §7.2 (the 9 parseable runs with a value are all 1.0; shadow09's 0.933 is excluded because its contract does not parse). | No contradiction |
| C-2 | Cause of shadow15's parity failure (and of shadow13's lint failure) | 07 §5.1 item 2: the parity failures of 07 and 15 (contract lacks `reviewer_personas`/`reviewer_models`) "are the defects fixed in skill text by `9874d63fb`/`c2e3347d3`"; 07 marks the run-vs-fix timing [UNVERIFIED] (§5.1 last bullet, Gaps) | 11 §8: shadow12-15 ran after `9874d63fb` (file mtimes vs commit time; the `9874d63fb` schema line is in all briefs of 12-15 and none of 03-11). So shadow15 had the fixed text and still failed: a real orchestrator defect, not a fixed skill-text defect. 06 Gap 4 (`06-input-contract-briefs.md:258`) independently reports the same timing. | 11 + 06 (two independent timing checks). 07's attribution holds for shadow07 only. | RESOLVED for 11 (MINOR, Finding 4) |
| C-3 | Number of test files in `tests/cli/reflect/` | 07 §4: 38 `test_*.py` files | 12 §0, §2, Gaps: 37 files ("4 panel + other 33") | My `ls tests/cli/reflect/test_*.py`: **38**. 12's own §2 table lists 38 file names, so its "37"/"33" text is an arithmetic slip. Collected total 353 (my run) matches 12. | RESOLVED for 07 (MINOR, Finding 6) |
| C-4 | Line of the `panel_lint` bump-rule message | 07 §2.2: B rule at `panel_lint.py:360-365` | 12 §6 C3 row: "`panel_lint.py:333` message" | My read: `:362-364` hold the B text; `:331-333` hold the L3 message. | RESOLVED for 07 (MINOR, Finding 7) |
| C-5 | rf-qa family count (the "rf-qa call-site count") | research-notes:69 and scope slice 05 §1C:89: "19 skill files / 521 lines" | 10 §3: "19 files and 591 occurrences (the scope slice's 521 counted matching *lines*, which is consistent)"; 10 Stale Doc repeats it | My grep over `src/superclaude/skills`: `rf-qa\b|rf-analyst|rf-qa-qualitative` = **591 matching lines** in 19 files (997 occurrences); `rf-qa\b|rf-qa-qualitative` without `rf-analyst` = **521 lines**. Both numbers are line counts; they differ because slice 05 left out `rf-analyst`. 10's explanation (occurrences vs lines) is wrong. The 39 call sites in 11 files are not affected. | RESOLVED (MINOR, Finding 5) |
| C-6 | Are E1's post-#519 `--coverage` / `coverage_context()` edits branch-only? | research-notes:39: "Branch-only edits after #519 (E1, commits 9874d63fb, c2e3347d3): `cluster_cmd.py`/`verify_cmd.py` `--coverage`, `findings_v2.coverage_context()` ..." | 09 §1.1: `git diff --stat origin/master HEAD -- src/superclaude/cli/review` is empty; scope slice 03 baseline note: the kernel is master code | My checks: `git diff --stat origin/master HEAD -- src/superclaude/cli/review` is empty; `git show --stat 9874d63fb c2e3347d3` touches only SKILL.md, `refs/reviewer-spec.md` and two reflect tests; `coverage_context` exists at `findings_v2.py:196` on master. The notes line is wrong; only the SKILL.md and reviewer-spec parts are branch-only. | RESOLVED for 09 (MINOR, Finding 8; matters for synth-06 branch-structure options) |
| C-7 | `_ID_TOKEN` line in `telemetry.py` (D7) | scope slice 02 §5 D7 row (`:167`) and :229: `telemetry.py:22`, and claims the hand-off's :23 is stale; research-notes:169 repeats "stale line numbers for D7" | 08 §3.2, 12 Gaps, 03 §(:187): `_ID_TOKEN` is :23, `_TS` is :22, `_ID_RE` is :24; the hand-off (`00-handoff-copy.md:111`, :23) was right | My read of `telemetry.py:17-27` confirms :23. 08 and 12 agree with each other and with the code. | RESOLVED for 08/12 (no defect in the assigned files; the stale claim sits in slice 02 and research-notes:169) |
| C-8 | Test counts in file 12 vs scope slice 02 §6 | slice 02: 651 = 131 (7 files) + 520 (12 files), per-file counts | 12 §1 | All 19 per-file counts identical; 12 adds that 4 of the 131 in `test_review_cli.py` are reflect tests (it checked `git show d2d8a2d16~1`). | No contradiction |
| C-9 | D2 test status | scope slice 02 §6 (`:210`) and the hand-off §8: D2 "not covered" | 12 §3.1 and 02 (`02-ledger-merge-verdict.md:95, :308, :329`): pinned by `test_review_ledger.py:385` | 12 and 02 read the test body; slice 02 says its own D2 call was "UNVERIFIED by body read". | RESOLVED for 12/02 (no defect in assigned files) |
| C-10 | E2 headline results vs audit D (verdict flips, blocking losses) | hand-off :105 and CR:292: "Four verdicts flipped" | 08 §8.2, 11 §6, 02 §4, 04 Stale Doc: 3 named flips plus total-loss merges | My `git show` of `audit-D/summary.md`: three named flips, five total-loss merges, "49 dropped findings were BLOCKING", drop reasons 56/18/14/3/1 (all drops, not only blocking ones). 08, 11 and 02 agree with it and with each other. 02's blocking split (24/14/10/1 = 49) and 08's all-drops split (56/18/14/3/1) measure different things; no conflict. | No contradiction among research files |
| C-11 | E2 headline ceiling | research-notes:128 "about 2-2.5 of 14 defects found" | 11 §6: replicated panels 1.60-2.50 /14 (CR:315-333); CR:428 "about 2-2.5" | 11 cites the per-panel table; the notes paraphrase CR:428. Refinement, not a conflict. | No contradiction |
| C-12 | Who writes `return-contract.yaml` and `merge_method` | 08 §6 and §12: contract writer "[UNVERIFIED] ... no Python writer ... in the files of this slice"; 07 §3 anomaly and Gaps: whether any producer writes `verification_verified`, `reviewers_verified`, `regression_verified`, `adversarial_subrun_status` "[UNVERIFIED]"; 07 §1.6 and §7.5: "Reflect MUST NOT synthesize its own merge", `merge_method` is written by the orchestrator | Code: `cli/reflect/ensemble.py:722-814` `build_reflect_contract` writes a UC-2 contract (`"mode": "post"`, :797) with `merge_method = "adversarial" if reviewer_count >= 2 else "single-reviewer-fallback"` (:773), and top-level `adversarial_subrun_status` (:793) and `verification_verified` (:814). The adversarial child runs only when no score is supplied and >= 2 workers succeeded (:424); if the child fails, `merge_method` stays `adversarial` and the deviation flags default to clean (:442-471). | The code is direct evidence and none of the assigned files reads it. | **UNRESOLVED in the research set: blocking (Finding 1)** |
| C-13 | Is the registered `review` subcommand set tested? | 09 §1.4: "No test pins the registered set ... nothing tests the registered command set" | 12 §4 D13 row: `test_review_help_lists_the_subcommands` (`test_review_cli.py:44-49`) checks that `panel, merge, ledger, telemetry` are present | 12 read the test. A partial pin exists (4 of 7 commands present, no exact-set check), so 09's "nothing tests" is too strong; 09's actual concern (a missing `cluster`, `verify-citations` or `manifest` module is silent) still holds. | RESOLVED for 12 (MINOR, Finding 9) |
| C-14 | Shadow-run "clean" vs substantive breaks | 07 §5.1 "Clean runs: 10, 11, 12, 14"; 11 §8 table "pass" for 10, 11, 12 | 07 §7.2-7.5 (shadow11 debate skipped on `cluster_agreement`); 11 §8 (shadow14 first-parse compliance 0.0 and the orchestrator rewrote headings) | Both files are right about different criteria (exit script vs shadow rules). See the item 5 cross-reference note. | Not a contradiction; MINOR cross-reference note |

---

## Compiled Gaps (item 7, lens)

Sources: the "Gaps and Questions" and "Stale Documentation Found" sections of 07-12, plus every [UNVERIFIED] and [CODE-CONTRADICTED] tag in their bodies. Duplicates across files are merged into one row (all sources named). Rows that another file or my own check already closes are marked CLOSED with the evidence; they stay in the table so synthesis carries the corrected fact. Severity: Critical = blocks a required report section; Important = changes a conclusion or a conflict-log row if wrong; Minor = note.

### Critical gaps (block synthesis)
None. Every required report part (overlap matrix, value inventory, conflict log, target architecture, future-use exposure list) can be written from the current files. The Important gap G-1 makes the conflict-log row on the merge path and contract writer incomplete; it does not stop synthesis from starting, but under this gate's severity rule it is blocking (Finding 1).

### Gap table

| # | Gap | Source file | Severity | Needs new research? |
|---|---|---|---|---|
| G-1 | Python UC-2 Tier 2 path `cli/reflect/ensemble.py` (`build_reflect_contract` :722-814, adversarial seam :423-471) not examined: it writes the contract, assigns `merge_method` by reviewer count, and writes the four top-level fields 07 could not place; it is the path behind the blocking tasklist post gate (09 §4.2) | 07 Gaps (producer of `verification_verified` etc.; `merge_method` writer), 08 Gaps 5/15 (contract writer UNVERIFIED); scope 03:63, 04:100 | Important | **Yes** (gap-fill: read `ensemble.py`, `runner.py` `write_reflect_post`, their tests; state the merge-method rule, contract writer and adversarial-failure handling in 07) |
| G-2 | Sprint `executor.py` null-convergence routing and §14.5.2 promotion-gate code not read (C16 consumer list) | 07 Gaps 1, C16 | Important | Small: my grep finds no `merge_method`/`convergence_score` in `src/superclaude/cli/sprint/`; hits only in `cli/reflect/{panel_lint,contract,ensemble}.py` and `cli/roadmap/*`. Record "no Python sprint consumer" or show the prose consumer |
| G-3 | Legacy EV-1 baseline (3/39): does it treat unparseable contracts as failures the way the shadow side does (`reflect_shadow_exit.py:243`)? Affects how inflated 0.615 vs 0.077 is | 11 U12; 07 §6.1 | Important | Small (read the baseline loader); otherwise carry as an inference |
| G-4 | E2 headline numbers are doc-sourced from COMBO-REPORT; raw `score.json`/`cost.json` not re-aggregated; whether every fallback-overwritten row was removed before the final tables | 11 U1, U7; 08 §7.4 | Important | No (the other session's report is merged later; carry as [UNVERIFIED]) |
| G-5 | Which document is authoritative for PR severity (rubric vs router, divergences D-a..D-g); `error-handling` row missing in both | 10 §2, Gaps 2, 4, 5 | Important | No (owner decision; conflict-log row) |
| G-6 | Whether `classifier.actionable_finding_comments` adds `category`/`confidence`/`in_diff` to Augment roots | 10 Gaps 1 | Minor | Small (read `classifier.py`) |
| G-7 | sc-adversarial Mode A: spawned agents vs inline run inside reflect; 6 of 14 recorded runs report an inline judge | 07 Gaps 5, §7.4 | Minor | No (recorded data already shows practice) |
| G-8 | Which shadow runs predate the fix commits | 07 Gaps 8 | Minor | CLOSED by 11 §8 and 06 Gap 4 (12-15 after `9874d63fb`; none after `c2e3347d3`) |
| G-9 | Installed SKILL.md (not only `refs/reviewer-spec.md`) carried `9874d63fb` when shadow12-15 ran | 11 U11; 06 Gap 4 | Minor | No |
| G-10 | MR decisions (debate kept, contract unchanged through Stage 4, E' deferred to 2.0.0) cited second-hand | 07 Gaps 9 | Minor | No (cite MR directly in synthesis) |
| G-11 | E3 `review merge` internals cited from the hand-off | 07 Gaps 10 | Minor | CLOSED by 02 (full read of `ledger.py`/`merge_cmd.py`) |
| G-12 | `tests/cli/reflect` file count ("twelve") | 07 Gaps 6, 12 Gaps, research-notes:46 | Minor | CLOSED: 38 files, 353 tests (my check; Finding 6 for 12's 37) |
| G-13 | Bodies of `test_verdict_replay_script.py`, `test_reviewer_readonly_tools.py`, `test_reviewer_brief_constraints.py` | 07 Gaps 7 | Minor | Partly CLOSED by 12 §6 (C9 rows read the last two); replay test bodies still names-only |
| G-14 | C13 enforcement (`make verify-sync`, pre-commit) not read | 07 Gaps 12 | Minor | No |
| G-15 | `--t2-engine panel` reject message has no code home | 07 §1.1, Gaps 13 | Minor | CLOSED by 09 §5 grep (`t2.engine` only in SKILL.md, `refs/reviewer-spec.md`, `manifest.py`, `manifest_cmd.py`) |
| G-16 | EV-1 text vs lint on the F3 branch; EV-1 "not self-written" but the orchestrator writes the verdict file; testability row lacks branch (b); `memory_status` row vs §9.2 | 07 [CODE-CONTRADICTED] x3, Stale Doc x3 | Minor (already established) | No |
| G-17 | Contract writer quoting: unquoted `[1m]` aliases make contracts unparseable; should the exit gate separate "unparseable" from "EV-1 failure"? | 07 Q, 11 Open Q 1 | Minor (design input) | No |
| G-18 | Paired legacy-vs-panel evidence run before any Stage 3 merge change; blind GT scoring of the 15 combo runs | 07 Q, 11 Open Q 3 | Minor (design input) | No |
| G-19 | `channel: advisory` does not force `blocking: false` | 07 §8, Q | Minor | No |
| G-20 | Manifest: `validate` skips the hash chain and `reviewers_complete`; failed run cannot retry in place; attempt payloads stored as hash only | 08 Gaps 1-3 | Minor (design input) | No |
| G-21 | Per-reviewer cost not derivable when reviewers share a gateway alias | 08 Gaps 4 | Minor | No |
| G-22 | review-telemetry/1 has no caller; strata fixed to sonnet/haiku (D15, owner decision "D3"); `KINDS` misnamed; list append not atomic; `panel_cmd.py` writes no telemetry [UNVERIFIED] | 08 Gaps 6-8, 14 | Minor | No |
| G-23 | `merge_cmd` writes no telemetry; ledger stores intended model only; dropped finding ids not stored | 08 Gaps 9; 12 §4 D1 row | Minor (established; D1) | No |
| G-24 | E2 records: no `fallback.log`/attempt transcripts committed; audit A not re-runnable; `expected_model` overwrite; stale attempt files; `audit-A/audit.py:33` `fam` bug | 08 Gaps 10-12; 11 §1 | Minor | No |
| G-25 | Which audit-D script does the chain replay (X1) and the `_check_finding` replay | 08 Gaps 13 | Minor | Drop replay CLOSED by 02 §4 (`AD/audit2.py`); chain replay still unnamed (summary says "Replayed it") |
| G-26 | Built-in run checks: fail the run or warn? | 08 Gaps 17 | Minor (design) | No |
| G-27 | "One reviewer for re-review by default" in `panel.py` | 09 Gaps 1 | Minor | Small (partition-1 file 04 may cover it) |
| G-28 | Global `~/.local/bin/superclaude` carries the same 7 `review` subcommands | 09 Gaps 2 | Minor | No |
| G-29 | Tasklist post gate wrapper reads `executor_model_class` from phase frontmatter | 09 Gaps 3 | Minor | Folds into G-1 |
| G-30 | How E2 drove `/sc:spec-panel --mode critique` | 09 Gaps 4 | Minor | CLOSED by 11 §1 (`run-reviewer.sh:13-17` brief is `/sc:spec-panel @<cand> --mode critique`) |
| G-31 | Installed `sc-review-ledger`, stoprule skill, `finding-grader` agent | 09 Gaps 5; 11 U15 | Minor | Partly CLOSED by 02 (read `review_ledger.py`, `stoprule.py` ranges) |
| G-32 | Fallback detection for "superclaude not installed"; recursion guard for reflect `--remediate` -> workflow -> reflect | 09 Open | Minor (design) | No |
| G-33 | Brainstorm/design hook advisory vs blocking; FR/AC ids in `merged-requirements.md`; workflow tasklist review = reflect pre or direct panel | 09 Open | Minor (owner decisions) | No |
| G-34 | Registered-command test is partial; 3 of 4 `ledger` subcommands, `telemetry`, `panel validate` have no instruction caller | 09 Gaps; 12 §4 D13 | Minor | No |
| G-35 | `fix_authorization` unstated for census rows 18 and 22; rf-qa-qualitative axes :593 and fixmap/ledger-revise citations from the slice | 10 Gaps 6-8 | Minor | No |
| G-36 | PR panel as finder vs S2b verifier; monotonicity/regression halt; owner of the three verdict contracts | 10 Gaps 9-11 | Minor (design) | No |
| G-37 | "Zero is suspect" wording survives in rf-qa agents while the test docstring says it was removed | 10 Gaps 3 | Minor (established) | No |
| G-38 | E2 judge sees the combo name; later `anon-*.sh` not read; `final-table.md` provenance; GT evidence paths exist; judge tokens per scoring | 11 U3-U6, CC 1 | Minor | No |
| G-39 | `scripts/eval_runner.py` body, `workflow_metrics.jsonl` writer, model-identity check in `cli/eval/` | 11 U9 | Minor | No |
| G-40 | Combo study: cause of leads (GLM/Qwen orchestrator in A), 7 reviewer calls in E1, answer exposure in HEAD-grounded runs, C3 base-commit archive | 11 U13-U14, §10 | Minor | No |
| G-41 | Hold the next 7 shadow runs until `c2e3347d3` is installed; owner of the E2 benchmark port | 11 Open | Minor (owner) | No |
| G-42 | C1/C6/C14 compare with HEAD only | 07 §4.1, Q5; 12 §6, Q | Minor (established) | No |
| G-43 | `test_section_adds_no_script_or_parser_requirement` deliberate or an artefact; add reflect/tasklist briefs to `BRIEF_SOURCES`; live7 test couples the tier file to `ccsession-models.json` | 12 Questions | Minor (owner) | No |
| G-44 | Bodies of `test_review_card_convert.py`, `test_review_cluster.py`, `test_review_manifest.py`, the replay tests and the 33-34 legacy reflect files not read | 12 Gaps | Minor | No |
| G-45 | Stale facts in the context files that synthesis must not copy: research-notes:39 "branch-only" coverage edits (C-6); research-notes:169 and slice 02 :167/:229 "stale D7 line" (C-7); slice 02 "D2 not covered" (C-9); slice 05 "521" without `rf-analyst` (C-5); hand-off "111 tests", "4 verdict flips", "duplicates not observed" | this report | Minor | No (correct at synthesis) |

---

## Depth Assessment (item 8, lens)

**Expected depth:** Deep (data-flow traces, integration points, pattern analysis, new source reads beyond the scope slices).

| File | New source reads beyond the slices | Restates a slice without new reads? | Rating |
|---|---|---|---|
| 07 | Full reads of `panel_lint.py`, `contract.py` (`derive_verdict` trigger order), `test_shadow_skill_contract.py`, `test_panel_contract_lint.py`, `test_shadow_exit_script.py`; ran `reflect_shadow_exit.py` and pasted the full output; listed every run's `adversarial/` dir; parsed three contracts with PyYAML to find the `[1m]` cause; read the installed sc-adversarial return contract | No. It re-checks each of the slice-03 constraints C1-C16 in code and finds three code-vs-doc contradictions the slices did not have | Deep. One coverage hole (UC-2 Python path, Finding 1) |
| 08 | Full reads of `manifest.py`, `manifest_cmd.py`, `telemetry.py`, `telemetry_cmd.py`, `merge_cmd.py`; E2 `run-reviewer.sh`, `meta.json`/`cost.json`, audit A/D scripts and summaries via `git show`; `extract.py`; `git ls-tree` counts of committed E2 files | No | Deep |
| 09 | `git diff`/`merge-base` against `origin/master`; `uv run superclaude review --help`; `git log -S` to trace `lint_cmd`/`estimate_cmd` to the PN2/PN3 experiment branches (new); full reads of the workflow, tasklist, brainstorm skills, `design.md` and the prompts file | No | Deep |
| 10 | Code trace of the pr_submit FSM, router and reviewers; line-by-line rubric-vs-router comparison (7 divergences, new); 39-row census of rf-* spawn sites; reading the test's banned phrase list | No (it corrects slice 05's `--candidate` option name) | Deep |
| 11 | E2 runner, judge, anonymiser and analysis scripts via `git show`; ran the exit script; run mtimes vs commit times; brief grep; stream-log identity (GLM/Qwen orchestrator, new); `find` of the untracked `base-e8db2fe6` folder and its origin in the stream log | No | Deep |
| 12 | `pytest --collect-only` (1182 items); `git log --diff-filter=A` origins; test bodies of every defect pin; probes for uncovered defects | No | Deep |

**Actual depth achieved:** Deep in all six files. No file only restates a scope slice. **Missing depth element:** the Python reflect Tier 2 ensemble/runner path (G-1), which is the code behind the only blocking reflect consumer.

---

## Recommendations

1. **Gap-fill for Finding 1 (blocking):** one research agent reads `src/superclaude/cli/reflect/ensemble.py` (at least `:1-24`, `:400-500`, `:722-830`), `runner.py` (`write_reflect_post` and the call into the ensemble) and `tests/cli/reflect/test_ensemble_*.py`, then appends a section to `research/07-reflect-merge-contract.md` that states: (a) the code-assigned `merge_method` rule (`ensemble.py:773`) and its behaviour when the adversarial child fails (`:436-471`); (b) the top-level fields it writes (`adversarial_subrun_status`, `verification_verified`, `reviewers_verified`, `regression_verified`, `subrun_status`, `reviewer_count`) against `panel_lint` L2 and `contract.py`; (c) whether the Q1 conclusion ("Reflect MUST NOT synthesize its own merge") and the Q8 keep-identical list hold for the UC-2 wrapper path; (d) what this means for the tasklist post gate (09 §4.2). It also closes 08 Gaps 5 and 15 (contract writer) for UC-2.
2. Before synthesis, correct the MINOR items in place or carry them as notes in synth-07 (S10 evidence trail): Findings 2-9.
3. Synthesis must take the Stage 2 numbers from 07/11 (they agree) and the shadow-run timing from 11/06, not 07 §5.1's attribution for shadow15.

---

## Findings

| # | Severity | File | Finding | Remediation |
|---|---|---|---|---|
| 1 | IMPORTANT | 07 (also 08) | The Python UC-2 Tier 2 path is not examined. `cli/reflect/ensemble.py:722-814` (`build_reflect_contract`) writes the reflect contract in code with `merge_method = "adversarial" if reviewer_count >= 2 else "single-reviewer-fallback"` (`:773`), sets `merge_method: adversarial` even when the adversarial child failed (`:436-471`, deviation flags then default to clean), and writes top-level `adversarial_subrun_status` (`:793`) and `verification_verified` (`:814`). This is the path behind `superclaude reflect run`, which the blocking sc:tasklist post gate uses (09 §4.2). 07 concludes that reflect must not synthesize its own merge and that the merge label is orchestrator-written, and 07/08 mark the contract writer and these fields [UNVERIFIED]. The code answers both, and the merge-path row of the conflict log is incomplete without it. Scope slices 03 (:63, :219) and 04 (:100) had flagged `ensemble.py` as a producer. | Gap-fill per Recommendation 1; update 07 §3, §8, §10 Q1/Q8 and Gaps, and 08 §6/§12 rows on the contract writer. |
| 2 | MINOR | 07 | 07 §5.1 item 2 attributes shadow15's parity failure (no `reviewer_personas`/`reviewer_models`) to the skill-text defects fixed by `9874d63fb`/`c2e3347d3`. 11 §8 and 06 Gap 4 show shadow15 ran after `9874d63fb`, so it is a real orchestrator defect. 07 itself marks the timing [UNVERIFIED]. | Synthesis uses 11's classification; optionally amend 07 §5.1. |
| 3 | MINOR | 11 | 11 §8 classifies shadow09/11 by exit-script criteria only. It does not say that shadow09 had no debate artifacts and reused `cluster_agreement` as its convergence score, or that shadow11 skipped the debate on `cluster_agreement` (07 §7.3-7.5). | Synthesis merges both views (cross-reference note in item 5). |
| 4 | MINOR | 07/11 | Not a defect, a merge instruction: 07 §5.1 and 11 §8 agree on every Stage 2 number (C-1). | Use either as the single source; cite both. |
| 5 | MINOR | 10 | 10 §3 says "19 files and 591 occurrences (the scope slice's 521 counted matching lines)". Both are line counts: 591 lines with `rf-analyst` in the pattern, 521 without it (slice 05's pattern); occurrences are 997 (my grep). Same wrong explanation in 10's Stale Doc list. The 39 call sites are unaffected. | Correct the sentence: "591 matching lines incl. rf-analyst; slice 05's 521 excludes rf-analyst". |
| 6 | MINOR | 12 | 12 says `tests/cli/reflect/` holds 37 test files ("other 33"); there are 38 (my `ls`; 12's own §2 table lists 38 names; 07 says 38). The 353 / 271 test counts are correct. | Change 37 to 38 and 33 to 34. |
| 7 | MINOR | 12 | 12 §6 C3 row cites `panel_lint.py:333` for the bump-rule message; `:331-333` is the L3 message, and the B text is at `:362-364` (07 cites `:360-365`). | Fix the line cite. |
| 8 | MINOR | research-notes (context) | research-notes:39 calls the `--coverage` / `coverage_context()` edits "branch-only after #519"; `git diff --stat origin/master HEAD -- src/superclaude/cli/review` is empty and the two fix commits touch only SKILL.md, `refs/reviewer-spec.md` and two tests (09 §1.1 is right). Synth-06 branch-structure options must not rely on the notes line. | Synthesis uses 09 §1.1. |
| 9 | MINOR | 09 | 09 §1.4 says nothing tests the registered `review` command set; `test_review_help_lists_the_subcommands` (`test_review_cli.py:44-49`, 12 §4) checks that 4 of the 7 are present. 09's real point (no exact-set check, so a missing E1 module is silent) stands. | Reword to "only a partial presence check exists". |
| 10 | MINOR | 07, 08, 12 | Stale facts in the context files that the assigned files already correct (D7 line :23, D2 pinned, "4" flips, 111 tests, D11 duplicates observed): synthesis must take the research-file version (gap G-45). | None in the research files. |

Blocking findings: 1 (Finding 1, IMPORTANT). MINOR notes: 9 (Findings 2-10) — they never fail the review and need no recheck.

**Verdict: FAIL** — remediation: run the gap-fill in Recommendation 1 (read `cli/reflect/ensemble.py` + `runner.py` UC-2 path and record the code-assigned `merge_method`, the contract writer and adversarial-failure handling in 07, closing 07/08's [UNVERIFIED] writer items), then re-verify Finding 1 only.

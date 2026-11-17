# QA Report — Research Gate (Partition 2 of 2), gap-detection lens

**Topic:** Unified Review Panel (E1 reflect Tier 2 panel / E2 tasklist review-panel study at 4a22d742 / E3 #346 review loop)
**Date:** 2026-11-13
**Phase:** research-gate
**Fix cycle:** N/A
**Lens:** gap-detection (checklist items 5-10: contradiction resolution, gap severity, depth, integration points, patterns, incremental writing)
**assigned_files:** research/07-reflect-merge-contract.md, 08-run-recording-telemetry.md, 09-consumer-plugpoints.md, 10-future-consumers.md, 11-evaluation-evidence.md, 12-test-pins-regression.md
**Fix authorization:** false (report only)
**Repository HEAD at review:** 792cf8c52 (branch ironbelly/shadow-runs)

[PARTITION NOTE: Cross-file checks limited to assigned subset. Full cross-file verification requires merging all partition reports.]

**Analyst reports at review start:** `qa/analyst-completeness-report-2.md` and `qa/analyst-cross-validation-report-2.md` exist but held only headers (analysts running in parallel), so full independent verification was performed.

---

## Per-file findings (appended as each file is reviewed)

### 07-reflect-merge-contract.md (488 lines, Status: Complete, Summary present)

Checks run: full Read (1-489); re-read `tests/cli/reflect/test_shadow_skill_contract.py:40-56` (HEAD-relative `git show HEAD:` / `git diff HEAD`, confirmed), `panel_lint.py:284-299` (F3 branch demands `single-reviewer-fallback` unconditionally, confirmed), `contract.py:185-195, :290-300` (major `1` gate, triggers 9/10/11, confirmed); `ls tests/cli/reflect/test_*.py | wc -l` = 38 (confirmed); recomputed the section 7.2 table counts (convergence 1.0 in 9/14; `cluster_agreement` 1.0 in 10/11; inline judge in 6/14) - all match; grep of `src/superclaude` for `derive_verdict|adversarial_convergence_score|single-reviewer-fallback` outside `cli/reflect` and `cli/review` (no sprint/roadmap Python consumer of the reflect contract).

- Item 5 (contradictions): internal tension "no contract" (section 5) vs "the file exists but is unparseable" (section 7.1) is explicitly resolved in 7.1. No unresolved contradiction inside the file. PASS.
- Item 6 (gap severity): the Gaps section lists 13 [UNVERIFIED]/[CODE-CONTRADICTED] items with no severity. QA rating: all MINOR except one: the gap "[UNVERIFIED] whether any producer writes `verification_verified`, `reviewers_verified`, `regression_verified` or `adversarial_subrun_status` at top level" (07:469) is answerable from code and the answer changes the migration plan - see finding F-1 (IMPORTANT). The sprint `executor.py` / promotion-gate gap (07:459) resolves to "no Python consumer found" by my grep; MINOR note.
- Item 7 (depth): Deep - complete traces of EV-1 text -> lint -> exit script, contract -> wrapper -> replay; live exit-script output captured verbatim. PASS.
- Item 8 (integration points): **FAIL - F-1.** The file answers "can the shared core own the merge and contract writer" (07:449-452, :488) and lists what the reflect module must keep (Q8, 07:440-449) without covering the second, code-level Tier 2 producer: `src/superclaude/cli/reflect/ensemble.py` (895 lines). `ensemble.py:773` sets `merge_method = "adversarial" if reviewer_count >= 2 else "single-reviewer-fallback"` (a count rule, not "a debate ran"); `ensemble.py:722-812` `build_reflect_contract` writes `mode: "post"`, `adversarial_subrun_status` (:793) and the `verification_verified`/`regression_verified` siblings at top level; `ensemble.py:89-95` says the `/sc:adversarial` child is "score-only"; it is called from `runner.py:36, :544` (`superclaude reflect` headless path). Consequences the file misses: (a) section 8 "UC-2 has data ... but no producer" (07:386) is true only for findings-v2 cards - UC-2 Tier 2 already runs in Python through this path; (b) the self-attested `merge_method: adversarial` problem (07:355-362) also exists in code, not only in orchestrator prose; (c) a shared-core contract writer must replace or coexist with `build_reflect_contract`, which is not in the Q8 keep-list. Scope slice 03 (:63, :219) flagged `ensemble.py` as UNVERIFIED; this file did not follow up.
- Item 9 (patterns): shadow pattern, contract pinning by tests (C1/C6 HEAD-relative, lint constants) and the reason-set replay pattern are documented with file:line. PASS.
- Item 10 (incremental writing): numbered sections each ending in Key Takeaways, gaps appended at the end, mid-file corrections (section 7.1 refines section 5). Consistent with incremental writing. PASS.

### 08-run-recording-telemetry.md (487 lines, Status: Complete, Summary present)

Checks run: full Read; re-read `telemetry.py:19-24` (`_TS` at :22, `_ID_TOKEN` :23, `_ID_RE` :24 - the file's [STALE DOC] correction is right), `telemetry.py:112-115` (STRATA sonnet/haiku, D15 confirmed), `merge_cmd.py:5-10` (imports json, os, click, ledger - no telemetry, confirmed), `manifest.py:39-51, :350-354` (9 states + failed, ENGINES incl. `panel`, attempt stores only `payload_sha256`, confirmed); `git show 4a22d742:.../tools/run-reviewer.sh` lines 58 and 76 (meta written with `expected_model:$exp` from `$MODEL`, then `MODEL="$NEXT"; ... attempt=0` - overwrite and attempt reset confirmed); grep `telemetry` in `panel_cmd.py` (no hit).

- Item 5 (contradictions): consistent with 07 on the exit script (`tele()` dual placement, parity recompute, L7 trivially equal). No contradiction. PASS.
- Item 6 (gap severity): 17 gaps, none rated by the author. QA rating: all MINOR. Gap 14 (`panel_cmd.py` writes no telemetry, [UNVERIFIED]) is resolved by my grep (no `telemetry` in `panel_cmd.py`) - note only. Gap 15 ("no Python writer of `return-contract.yaml`", 08:190, :445, :473) is true for the in-session UC-1 path but false for the headless path (`ensemble.py` `_emit_reflect_contract`, :886; `build_reflect_contract`, :722) - folded into F-1, not a separate blocking item because 08's design proposals (section 11.3) do not depend on it.
- Item 7 (depth): Deep - end-to-end trace of the manifest lifecycle (init -> advance -> attempts -> resume -> publish), telemetry record kinds to SQLite view, E2 runner per-attempt records, audits A/D check-by-check, and a cross-effort record table. PASS.
- Item 8 (integration points): manifest callers (`manifest_cmd`, exit script, tests), telemetry callers (none in `src`), merge_cmd telemetry absence, extract.py inputs all documented with file:line. PASS (headless contract writer gap counted under F-1).
- Item 9 (patterns): hash-chain/idempotent-replay pattern, telemetry-as-projection proposal, transcript-derived served identity as one shared method (E1 `extract.py:54-62` = E2 `run-reviewer.sh:51`). PASS.
- Item 10 (incremental writing): 12 numbered sections with per-section Key Takeaways; section 12 claim table and gap list built from earlier sections. PASS.

### 09-consumer-plugpoints.md (294 lines, Status: Complete, Summary present)

Checks run: full Read; re-read `cli/review/__init__.py:19-36` (nine names incl. `lint_cmd`/`estimate_cmd`, narrow `ModuleNotFoundError` swallow, confirmed), `sc-workflow-protocol/SKILL.md:89, :93` (Wave 4 reflect pre, advisory, confirmed), `sc-tasklist-protocol/SKILL.md:1157-1179` (post gate `superclaude reflect run ... --depth deep`, blocking acceptance criteria, confirmed) and `:1640, :1646` (Stage 10.5 ships regardless, confirmed), `commands/spec-panel.md:256-268` (seven Review Loop bullets + hard gate, confirmed); grep of all 12 research files for `swarm|T2Model|run_tier2_ensemble|reflect run|ensemble`.

- Item 5 (contradictions): consistent with 07 (shadow-only kernel, `--t2-engine` default legacy, UC-2 flag ignored). It correctly records its own [CODE-CONTRADICTED] corrections of hand-off D13/D14. PASS.
- Item 6 (gap severity): 6 [UNVERIFIED] items + 7 open questions, unrated. QA rating: MINOR, except gap 09:271 ("tasklist post gate's wrapper ... not traced into `superclaude reflect run` code"), which is the same untraced path as F-1. `sc-tasklist-protocol/SKILL.md:1171` step 2 says "The wrapper spawns the executor-disjoint reflect ensemble internally"; that ensemble is `runner.py:544` -> `ensemble.run_tier2_ensemble`. The only BLOCKING reflect consumer in the repo (the per-phase post gate) is therefore driven by a Tier 2 engine no research file describes. Counted in F-1 (IMPORTANT).
- Item 7 (depth): Deep - CLI registration traced from `main.py:568-570` through the loader to `--help`; history of the loader list via `git log -S`; spec-panel prose -> prompts file -> CLI sequence; reflect default-flag escalation via rubric rows. PASS.
- Item 8 (integration points): workflow Wave 4 (`:89`), tasklist Stage 10.5 (`:1619-1646`) and phase post gate (`:1155-1179`), brainstorm Wave 3/4 (`:264-339`), design (no hook, `design.md:123-124`), spec-panel loop (`:256-268`) and prompts `:68-70` all have file:line. PR-submit and rf-qa sites are delegated to file 10 (by design of the research split). The post gate is located but its engine is not traced (F-1). PASS for this file's own scope apart from F-1.
- Item 9 (patterns): prose-loop-drives-CLI pattern, optional-loader pattern, advisory-vs-blocking per consumer, shared id-regex problem (D7). PASS.
- Item 10 (incremental writing): eight numbered sections with Key Takeaways, design-input section derived from earlier ones. PASS. Minor note: header date 2026-11-14 vs task date 2026-11-13 (cosmetic).

### 10-future-consumers.md (230 lines, Status: Complete, Summary present)

Checks run: full Read; re-read `pr_submit/fsm.py:806-826` (S2_CLASSIFY -> S2B_VERIFY -> S3_DIAGNOSE / REPORT_ONLY edges, confirmed) and `:941` (`verify: Callable[[Finding], bool] = _default_verify`, confirmed); `reviewers.py:41` (`REVIEWERS = ("augment", "codex")`, confirmed); `severity_router.py:178-193` (in_diff drop + architecture-to-Low, unconditional `deep` drop, confirmed); grep `deep=` in `src/superclaude/pr_submit/*.py` (no caller passes it, confirmed); `rf-qa.md:41` and `rf-qa-qualitative.md:41` contain "0 issues is suspect" (confirmed); `test_review_prompt_overrides.py:140-148` bans only "surfaces zero issues as suspect" (confirmed).

- Item 5 (contradictions): records three real contradictions (test docstring vs agents; severity-routing.md vs router; rubric vs router D-a..D-g) and leaves authority as an owner decision rather than resolving silently. The rf-qa self-contradiction (:41 vs :91/92) is surfaced. PASS.
- Item 6 (gap severity): 12 gaps unrated. QA rating: all MINOR - each is either tagged [UNVERIFIED] with the exact unread line, or an owner decision (authoritative rubric, finder vs verifier seam, verdict-contract owner). None blocks the migration plan's no-regression list (they concern future consumers, not pinned behaviour).
- Item 7 (depth): Deep - PR finding traced source -> normalize -> grade -> dedup -> verify -> route -> dispatch -> fallback with file:line at each hop; 39-row call-site census with phase, inputs, fix authorization, verdict format, in-place-fix need. PASS.
- Item 8 (integration points): pr-submit FSM states (S2_CLASSIFY, S2B_VERIFY, S3_DIAGNOSE, REPORT_ONLY, S5B_AUGGIE_FALLBACK) with `fsm.py` lines; both PR seams (`reviewers.py:41`, `fsm.py:941`); rf-qa / rf-qa-qualitative / rf-analyst call sites in 11 files with line numbers; 28 sites needing in-place fixes identified. PASS.
- Item 9 (patterns): lens -> consolidate -> one fix agent -> verify pattern (`task/SKILL.md:225-256`) mapped to the #346 reviewer -> merge -> Reviser -> re-review loop; exposure table X1-X13. PASS.
- Item 10 (incremental writing): six numbered sections with Key Takeaways; census counts reconciled after the table (39 / 37 / 28). PASS.

### 11-evaluation-evidence.md (403 lines, Status: Complete, Summary present)

Checks run: full Read; `git show 4a22d742:.../tools/tmp-scripts/judge-one.sh` line 21 contains `\"combo\":\"$C\"` (judge sees panel name, confirmed); `analysis/final-table.py:22-24` (`if not os.path.exists(f): continue` on `/tmp/audit-*/flags.tsv`, silent skip confirmed) and `:44` (groups by `expected_model`, confirmed); control package `resolution-live7.json` models (Qwen3.8-max x2, glm-5.3 x2, confirmed - D11 evidence); `git log` commit times `9874d63fb` 01:54:25Z and `c2e3347d3` 02:57:12Z (confirmed); shadow15 dir mtimes 02:24-02:47 (after `9874d63fb`, before `c2e3347d3`, confirmed).

- Item 5 (contradictions): resolves many doc-vs-doc conflicts explicitly (CR:287 vs CR:501, CR:383 vs CR:428, 161 vs 156, 4 vs 3 flips, SSE "never run"). Cross-file with 07: 07:273 says the parity failures of 07 and 15 are "the defects fixed in skill text by `9874d63fb`/`c2e3347d3`", while 11's timeline (11:223, :238) shows shadow15 ran AFTER `9874d63fb` and still failed parity because the orchestrator ignored step 10. 07 itself marks run timing [UNVERIFIED] (07:278, :466), so this is a refinement, not a hidden contradiction; synthesis must use 11's classification. MINOR note.
- Item 6 (gap severity): 15 UNVERIFIED items + 7 contradicted + 4 open questions, unrated. QA rating: all MINOR - each is tagged and none is carried as fact; the headline E2 numbers are explicitly doc-sourced (11:141). The unfixed `[1m]` YAML-quoting defect is surfaced as an open question (11:383) and as a finding, which is the correct treatment.
- Item 7 (depth): Deep - E2 harness traced input -> brief -> dispatch -> checks -> fallback -> output -> anonymiser -> judge -> aggregation -> permutation test; E1 shadow failures classified per run with commit timeline from mtimes and brief text; stream-log evidence for the combo orchestrator family. PASS.
- Item 8 (integration points): E2 runner <-> product resolution files (`review-panel-resolution/1`), judge <-> GT, final-table <-> `/tmp/audit-*`, E1 exit script <-> panel_lint, combo study <-> E2 GT, possible host `src/superclaude/cli/eval/` all named with file:line. PASS.
- Item 9 (patterns): evaluation pattern (fixed GT, blind judge, anonymisation, permutation test, audits as separate passes, GT hashes as tamper evidence) and shadow pattern (non-interference, side signals only) both documented and contrasted (11:190). PASS.
- Item 10 (incremental writing): file mtime 20:33, later than siblings (17:4x) - consistent with a later appended re-run or edit; 12 sections with Key Takeaways and a gap list cross-referenced by section number. PASS.

### 12-test-pins-regression.md (348 lines, Status: Complete, Summary present)

Checks run: full Read; `uv run pytest --collect-only -qq -p no:cacheprovider tests/cli/reflect` -> 353 tests in **38** collected files, and every `tests/cli/reflect/test_*.py` on disk is collected; re-read `tests/skills/test_review_loop_extension.py:120-127` (forbids `parser`, `script`, `state machine`, `transcript`, `asynchronous` in the Review Loop section, confirmed), `tests/review/test_review_ledger.py:376-385` (final assertion `"resolved"` - D2/D3 pin, confirmed), `test_review_panel_exclusion.py:208-213` (6 x Haiku - D11 pin, confirmed), `test_review_telemetry.py:324-327` (`stratum="gpt"` rejected - D15 pin, confirmed).

- Item 5 (contradictions): cross-file numeric conflict with 07: 07:139 says 38 test files (correct per my collection), 12:19, :23, :327 say 37 and G9 (12:277) says "the remaining 33 files" (should be 34). The test count (353) is right in both. MINOR (count wording; the gate command `uv run pytest tests/cli/reflect` is unaffected). All hand-off contradictions (111 vs 651, D2/D11 "not covered") are resolved with evidence. PASS with note.
- Item 6 (gap severity): 4 UNVERIFIED, 6 CODE-CONTRADICTED, 4 questions, unrated. QA rating: all MINOR. The migration-critical items the prompt names are not rated Minor-and-hidden: HEAD-relative C1/C6/C14 is a finding with a stated gate procedure (12:283) plus an open question (12:333); tests that must change on purpose are enumerated per fix (section 9). Note for synthesis: the C1/C6/C14 weakness must appear in the no-regression gate list as a required procedure (run before commit, or add an absolute pin), not as an optional nicety.
- Item 7 (depth): Deep - real collection run (1182 = 651 + 353 + 178), per-file origin commits, defect pins read in body, golden fixtures traced to their pinning tests and regeneration triggers. PASS.
- Item 8 (integration points): test <-> code couplings documented (v1 vocab imported by reflect test :199-218; `cluster.py` import-set pin :784-795; live7 tier lengths coupled to `ccsession-models.json` :92-106). G9 lists the headless ensemble tests (12:88, :277) as "must not move", but no research file explains the code they guard (F-1). PASS for this file's scope.
- Item 9 (patterns): contract pinning by tests documented in depth (HEAD-relative vs absolute pins, goldens, string pins over src + plugin copies, brief lint). PASS.
- Item 10 (incremental writing): numbered sections 0-9 with Key Takeaways; section 3.7 "found while probing" is an explicit incremental addition. PASS.

---

## Overall Verdict: FAIL

One blocking (IMPORTANT) gap: F-1. Everything else in the six files passes the gap-detection lens; the remaining findings are notes.

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | File inventory (incidental) | PASS | All 6 assigned files read in full; each has `**Status:** Complete` and a `## Summary` section |
| 2 | Evidence density | Not in lens | Delegated to partition-2 analyst/QA lenses; no defect met incidentally (about 40 citations re-read, all correct) |
| 3 | Scope coverage | Not in lens | Delegated; the one coverage hole met (`cli/reflect/ensemble.py`) is reported as F-1 under item 8 |
| 4 | Documentation cross-validation | Not in lens | Delegated; files tag doc claims consistently |
| 5 | Contradiction resolution | PASS (notes) | 07 vs 11 parity-fix timing (refinement, N-2); 07 vs 12 file count 38 vs 37 (N-1); all doc-vs-doc conflicts resolved explicitly |
| 6 | Gap severity | FAIL | Authors rate no gap; QA rated every gap in the 6 files: all MINOR except the unresolved `ensemble.py` producer question (07:469, 08:473, 09:271), which blocks the migration plan -> F-1 IMPORTANT |
| 7 | Depth appropriateness (Deep) | PASS | Each file traces at least one flow end to end (EV-1 text -> lint -> exit script; manifest lifecycle; PR finding intake -> route; E2 runner -> judge -> permutation test; collection -> pins -> gates) |
| 8 | Integration point coverage | FAIL | All named plug points have file:line (workflow `:89`, tasklist `:1619-1646` / `:1155-1179`, brainstorm, design, spec-panel `:256-268`, pr-submit `fsm.py:806-826, :941`, 39 rf-qa sites). Missing: the headless Tier 2 engine behind the blocking tasklist post gate (F-1) |
| 9 | Pattern documentation | PASS | Shadow pattern (07, 08, 11), evaluation pattern (11), contract pinning by tests (07, 12), lens -> fix agent -> verify pattern (10) |
| 10 | Incremental writing compliance | PASS | All 6 files have numbered sections with per-section Key Takeaways, gap lists that reference earlier sections, and in-file refinements |

## Summary

- Checks passed: 7 / 10 (items 1, 5, 7, 9, 10 PASS; items 2-4 out of lens)
- Checks failed: 2 (items 6 and 8, same root finding)
- Critical issues: 0
- Important issues: 1 (F-1)
- Minor notes: 6
- Issues fixed in-place: 0 (fix_authorization: false)

## Issues Found

| # | Severity | File | Finding | Fix |
|---|----------|------|---------|-----|
| F-1 | IMPORTANT | 07-reflect-merge-contract.md (sections 8, 10 Q8, gaps :469); 09-consumer-plugpoints.md (:152-160, gap :271); 08-run-recording-telemetry.md (:190, :473); 12-test-pins-regression.md (:88, :277) | No research file documents the headless reflect Tier 2 engine `src/superclaude/cli/reflect/ensemble.py` (895 lines), reached through `runner.py:36, :544` by `superclaude reflect run`, which is the engine behind the only BLOCKING reflect consumer (tasklist per-phase post gate, `sc-tasklist-protocol/SKILL.md:1157-1179`, "The wrapper spawns the executor-disjoint reflect ensemble internally"). It is a second contract writer and a third panel-like engine: per-slot external models `T2Model0N` via swarm dispatch (docstring :1-11), a "score-only" `/sc:adversarial` child (:89-95, :424-440), `merge_method = "adversarial" if reviewer_count >= 2 else "single-reviewer-fallback"` (:773), and `build_reflect_contract` (:722-812) writing `mode: "post"`, `adversarial_subrun_status` and verification siblings at top level. Effects: 07 section 8 "UC-2 ... no producer" and the Q8 keep-list are incomplete; 07's open question on top-level `adversarial_subrun_status`/`verification_verified` writers (:469) and 08's "no Python writer of `return-contract.yaml`" (:190) are answerable (ensemble writes them); the self-attested `merge_method: adversarial` problem (07:355-362) exists in code too. Without this, the overlap matrix (dispatch, panel resolution, contract writer) and the migration plan (what replacing reflect Tier 2 must keep for the blocking post gate) will be built on two Tier 2 engines when there are three. | Gap-fill research item (read-only): read `cli/reflect/ensemble.py` (`run_tier2_ensemble` :296, `run_adversarial_scorer` :514, `build_reflect_contract` :722-812, `_emit_reflect_contract` :886) and `cli/reflect/runner.py` :440-580; record its dispatch and model binding, merge rule, contract fields and the tests that pin it (`tests/cli/reflect/test_ensemble_*.py`, 56 items per 12:88); append the results to 07 (section 8 and Q8 keep-list) and 09 (section 4.2 post gate), and close gap 07:469 / 08:473 / 09:271. |
| N-1 | MINOR | 12-test-pins-regression.md:19, :23, :327, :277 | `tests/cli/reflect` holds 38 collected test files (my `--collect-only`), not 37; G9 "remaining 33 files" should be 34. 07:139 has the right count. Test total 353 is correct. | Note only. |
| N-2 | MINOR | 07-reflect-merge-contract.md:273 vs 11-evaluation-evidence.md:223, :238 | 07 attributes the shadow07/15 parity failures to defects "fixed in skill text by `9874d63fb`/`c2e3347d3`"; 11's timeline shows shadow15 ran after `9874d63fb` and still failed (orchestrator ignored step 10). 07 marks timing UNVERIFIED, so this is a refinement. | Note only; synthesis should use 11's per-run classification. |
| N-3 | MINOR | all six files, "Gaps and Questions" sections | Authors list gaps without CRITICAL/IMPORTANT/MINOR ratings; QA rated them in this report. | Note only. |
| N-4 | MINOR | 07-reflect-merge-contract.md:459 | Sprint `executor.py` / promotion-gate routing on `merge_method` is left UNVERIFIED; grep of `src/superclaude` for `derive_verdict|adversarial_convergence_score|single-reviewer-fallback` finds only `cli/reflect/` modules (no sprint/roadmap Python consumer). | Note only. |
| N-5 | MINOR | 08-run-recording-telemetry.md:472 | `panel_cmd.py` writing no telemetry is left UNVERIFIED; grep shows no `telemetry` reference in `panel_cmd.py`. | Note only. |
| N-6 | MINOR | 09-consumer-plugpoints.md:6, 12-test-pins-regression.md:6 | Header dates 2026-11-14 while the task and siblings are 2026-11-13. | Note only. |

## Actions Taken

None (fix_authorization: false). No research file was modified.

## Recommendations

- Resolve F-1 with one gap-fill research item before synthesis (see Required Fix). It is narrow: two files in `src/superclaude/cli/reflect/` plus the ensemble test names.
- Carry N-1 and N-2 into synthesis as corrections (38 files; shadow15 classified per file 11).
- When synthesis builds the no-regression gate list, state the C1/C6/C14 HEAD-relative weakness as a required procedure, not an option.

## Confidence Gate

- **Confidence:** Verified: 7/10 | Unverifiable: 3 (items 2-4, outside the assigned lens; covered by the partner lens agents) | Unchecked: 0 | Confidence: 100.0%
- **Tool engagement:** Read: 11 | Grep: 0 | Glob: 0 | Bash: 12 (read-only greps, `sed -n`, `git show`, `git log`, `pytest --collect-only -p no:cacheprovider`)
- Read + Grep + Glob (11) is at least the 10 checklist items. No web research was needed.
- UNCHECKED items: none. UNVERIFIABLE items: 2, 3, 4 (assigned to other lenses by the gate rules at task line 214).

## QA Complete

Verdict: FAIL

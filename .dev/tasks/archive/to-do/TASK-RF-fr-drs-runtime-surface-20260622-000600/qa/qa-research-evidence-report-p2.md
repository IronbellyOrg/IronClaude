# QA Report — Research Gate (Evidence-Quality Lens, Partition P2)

**Topic:** FR-DRS deterministic runtime-surface sweep + integration
**Date:** 2026-06-22
**Phase:** research-gate
**Lens:** evidence-quality
**Fix cycle:** N/A
**Fix authorization:** false (report-only)
**Assigned files (P2):** 05-eval-path-grader-cases-materializer.md, 06-skill-prose-demotion-and-refs.md, 07-test-patterns-and-verification.md, 08-mdtm-template-and-examples.md

[PARTITION NOTE: Cross-file checks (contradictions, scope coverage) limited to assigned subset. Full cross-file verification requires merging all partition reports.]

---

## Overall Verdict: FAIL

One CRITICAL evidence-quality defect: R5's top-priority deliverable (the C-5 materializer location) is tagged `[CODE-VERIFIED — absence confirmed]` but the absence is **refuted by independent grep**. A near-complete materializer pattern exists on disk that R5 missed. This propagates into R7 as an inherited UNVERIFIED precondition. All other evidence in P2 is dense, accurate, and re-verified against source.

---

## Items Reviewed
| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | File inventory / Status: Complete + Summary | PASS | All 4 files (05/06/07/08) `Status: Complete`, each carries a Summary section. |
| 2 | Evidence density (paths/lines/functions) | PASS | 05: 44 CODE-VERIFIED tags; 06: 34; 07: 13 + 16 SPEC (test files don't exist yet); 08: 11. Spot-checks below confirm citations resolve. Dense (>80% evidenced). |
| 3 | Doc-claim tagging discipline (item 4) | PASS-with-exception | All claims tagged. EXCEPTION: R5's C-5 absence is mis-tagged CODE-VERIFIED (see Issue 1). |
| 4 | grader.py:191 check_yaml_list_len_eq | PASS | Read `:191-210`. Signature `(assertion, base_dir)->tuple[bool,str]`, target `:192`, missing `:193-94`, safe_load `:195`, list_field/count_field `:196-97`, list check `:198-200`, int `:202-06`, len== `:207-210`. Exact match to R5 §1.2. |
| 5 | grader.py:437 grade_eval + :440 metadata + SKIP | PASS | Read `:437-484`. `metadata_path = eval_dir/"eval_metadata.json"` `:440`; SKIP+return {} `:441-43`; assertions `:446`. Exact. |
| 6 | grader.py:448-449 C-6 target bucketing | PASS | Read verbatim: `with_skill_assertions = [a ... startswith("with_skill/")]` `:448`, `old_skill_` `:449`. Exact match R5 §2. |
| 7 | grader.py:318-434 dispatch ladder (19 types) | PASS | Read `:318-434`. 8 baseline inline (file_exists :324, frontmatter_field :330, section_present :342, section_enumerated :350, yaml_field :360, yaml_field_min :372, yaml_substring :387, dir_count :400) + 11 extension delegated `:411-432` + unknown `:434`. R5 §1.1 exact. |
| 8 | 5 case dirs exist with input/ + expected.yaml | PASS | `ls cases/uc2-*/` → 5 dirs (degraded-backend, dynamic-dispatch, positive-control, test-only-ref, unwired-surface-passes); each has `expected.yaml` + `input/{diff.patch,tasklist.md}`. R5 §3 exact. |
| 9 | **R5 C-5 materializer "NOT LOCATED" — confirm/refute** | **FAIL (REFUTED)** | Independent grep found 2 scripts that DO flatten evals.json→eval_metadata.json for ids 37-41: `scaffold_iteration.py:65` + `produce_iteration.py:216` under `TASK-RF-uc2-reachability-.../phase-outputs/plans/`. produce has `materialize()` (:87) reading input/diff.patch + copying return-contract.yaml→contract.yaml (:172). See Issue 1. |
| 10 | make reflect-eval = grader-only on empty dir (R5) | PASS | Makefile `:505-508`: `mkdir -p iterations/<ts>` then `grader.py <that-dir>`. R5 §4 item 2 exact. |
| 11 | aggregate_iteration.py:49 reads metadata (R5) | PASS | `:49` `meta = read_json(eval_dir / "eval_metadata.json")`. Exact. |
| 12 | SKILL.md 465/466/487/489/491 current (R6) | PASS | Read all. 465/466 step entries verbatim; 487/489/491 paragraphs verbatim. "never emits a clean PASS" sentence IS at line 489 (R6 P1). Exact. |
| 13 | SKILL.md §9.1 1.6.0 block 669/672/731-736 (R6) | PASS | Header `### 9.1 Stable contract (contract_version: 1.6.0)` at 669; version decl 672; six fields 731-736. R6 cited ~671-672/721-736 — anchors correct. |
| 14 | SKILL.md §5.3 surface_unreached 390/391/402/412 (R6) | PASS | 390/391 STOP rows w/ conditions; 402 D13 pre-filter precedence; 412 `surface_unreached: <string>\|null # "runtime_surface_unreached"...`. Exact. |
| 15 | ensemble.py:59 REFLECT_CONTRACT_VERSION="1.0" (R6) | PASS | `:59` `REFLECT_CONTRACT_VERSION = "1.0"`. Confirms R6's stale-stamp reconcile note. |
| 16 | tests/cli/reflect/ conventions + conftest fixtures (R7) | PASS | conftest: FIXTURES_DIR :17, _FAKE_BASE :20, _FAKE_HEAD :21, cli_runner :41, temp_tasklist :47, patch_git :59, patch_runner_env :84, make_claude_process_stub :99, make_claude_process_sequence :142. R7 line cites off by ≤3 lines but substantively exact. |
| 17 | R7 "zero @pytest.mark.parametrize" claim | PASS | `grep -rn parametrize tests/cli/reflect/ --include='*.py'` → exit 1 (no matches). Confirmed. |
| 18 | R7 make lint = ruff check only; CI ruff format --check separate | PASS | Makefile lint `:48-50` = `lint-architecture` + `uv run ruff check .`; separate `format` target = `uv run ruff format .` (mutating). Neither runs `--check`. R7 §3.1 correct (matches memory make_lint_vs_ci_ruff_format). |
| 19 | R8 template 02 exists + src/ SoT copy | PASS | `.claude/templates/workflow/02_mdtm_template_complex_task.md` (1515 lines) + src/ SoT copy (1515 lines). R8 said 1516 — 1-line offset (MINOR). |
| 20 | R8 UC2 exemplar + POST reflect gate item shape (L363) | PASS | UC2 file 141495 bytes (R8 "141 KB" ✓); L363 = `superclaude reflect run <abs-path> --depth deep --fix --promote`; L19 start_commit, L20 executor_model_class "opus", L30 reflect_post room comment. All verbatim. |

## Summary
- Checks passed: 18 / 20 (item 3 PASS-with-exception, item 9 FAIL)
- Checks failed: 1 (item 9 — C-5 materializer absence refuted)
- Critical issues: 1
- Issues fixed in-place: 0 (fix_authorization: false — report-only)

## Confidence
- **Confidence:** Verified: 20/20 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- **Tool engagement:** Read: 6 | Grep: 0 (folded into Bash) | Glob: 0 | Bash: 7 | tavily_search: 0 | tavily_extract: 0 | web_search_fallback: 0 | web_fetch_fallback: 0
- No external (web) lookups required — all claims are local/source-truth-bound (Principle 6).
- Tool calls (13) ≥ checklist items; each maps 1:1 to a verification; no padding.

## Issues Found
| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| 1 | CRITICAL | 05-...materializer.md §0 item 4, §4 (VERDICT "CONFIRMED NOT LOCATED"), §7 ledger row "materializer absence" | R5's top-priority deliverable claims the C-5 materializer (evals.json→eval_metadata.json flatten + cases/uc2-* copy) is "CONFIRMED NOT LOCATED in tracked code" and tags it `[CODE-VERIFIED — absence confirmed]`. **Independently REFUTED.** Two scripts in `.dev/tasks/to-do/TASK-RF-uc2-reachability-20260620-025931/phase-outputs/plans/` do exactly this for ids 37-41: `scaffold_iteration.py` (reads evals.json :39-40, writes eval_metadata.json :65 with `{eval_id,eval_name,assertions}`, makes `with_skill/outputs/artifacts/`) and `produce_iteration.py` (writes eval_metadata.json :216, `materialize()` :87 reads input/diff.patch into a scratch tree, runs the skill, `shutil.copy2` return-contract.yaml→contract.yaml :172). R5's *narrowly-scoped* grep (`'eval_metadata.json").write_text'` over `.dev/eval-workspaces/sc-reflect/*.py` ONLY) genuinely returns no hits — but R5 over-generalized to "no script in the repo" and "materialization was done by the LLM harness, not a tracked materializer," which is wrong. The scripts ARE on disk in the worktree (untracked: `git status` shows `??` on the plans/ dir — so "not git-tracked" is technically true, but "not located / does not exist as a script" is false). | (a) Correct R5's §4 verdict to "materializer pattern EXISTS on disk (untracked scratch from the UC2 task): `scaffold_iteration.py` + `produce_iteration.py`"; (b) re-scope the absence grep to the whole worktree, not just the sc-reflect workspace; (c) change the Phase-3 builder recommendation from "build a small materializer from scratch" to "**promote/adapt the existing UC2 scaffold+produce scripts** into a tracked `materialize.py` wired into `make reflect-eval`" — they already do the flatten + the run_sweep-equivalent contract production. This materially de-risks AC-2 and changes the Phase-1/Phase-3 task items. |
| 2 | MINOR | 07-...verification.md §1.1; 08-...template.md §0/§1b | Count/line-offset drift: R7 says "15 files" in tests/cli/reflect/ (the dir actually shows 17 entries incl. fixtures/ + __pycache__; R7's 15 = 13 test files + conftest + __init__, consistent labeling). R8 says template is "1516 lines" (actual 1515) and cites body ranges up to L1516. Off-by-one/labeling only; no downstream claim depends on the exact count. | Optionally re-anchor R8's upper-section line cites by −1; harmless — all R8 structural claims corroborated directly against the live UC2 exemplar. |
| 3 | MINOR | 05/06/08 (no "Gaps and Questions" section); cross-file | Only file 07 has explicit "Gaps and Questions" + "Stale Documentation Found" sections. 05/06/08 omit them. For 06/08 there genuinely appear to be no gaps (legitimate). But R7's gaps **inherit R5's incorrect conclusion** — R7 §2.2 + Gaps explicitly defer to R5 ("R5 owns the eval-path wiring... R7 flags it as UNVERIFIED precondition"). Once Issue 1 is corrected, R7's "materializer not located" gap is downgraded from a build-risk to a "promote-existing-script" task. | When fixing Issue 1, propagate the correction to R7 §2.2 / R7 Gaps / R7 Stale-Doc note so the determinism test's precondition reads "materializer exists (UC2 scaffold/produce) — promote it," not "UNVERIFIED, may not exist." |

## Actions Taken
None — `fix_authorization: false`. Report-only.

## Recommendations
- **BLOCKER for synthesis (research-gate item 6: ALL gaps must be resolved):** correct R5's C-5 materializer verdict before the builder writes Phase-1/Phase-3 items. The current "build from scratch / NOT LOCATED" framing would send the builder to author a redundant materializer when a working one (scaffold_iteration.py + produce_iteration.py) already exists in the UC2 task scratch and only needs promotion to tracked + wiring into `make reflect-eval`.
- Propagate the correction into R7 (§2.2 + Gaps + Stale-Doc) which inherited R5's conclusion verbatim.
- R6 and R8 are clean — no remediation required (all line anchors and shapes verified verbatim; R8's 1-line template offset is cosmetic).

## QA Complete

VERDICT: FAIL

Severity-rated issues:
- CRITICAL: 1 (R5 C-5 materializer "NOT LOCATED" refuted — materializer scripts exist on disk; mis-tagged CODE-VERIFIED)
- MINOR: 2 (line/count offset drift in R7/R8; missing Gaps sections in 05/06/08 + R7's inherited gap)

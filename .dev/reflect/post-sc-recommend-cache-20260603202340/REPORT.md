# Reflection Report — UC-2 Post-Execution Deviation Audit

**Task:** TASK-RF-20260603-032936 — sc-recommend lookup-cache (Option P)
**Mode:** post · **Tier reached:** 2 (deep) · **Reviewers:** 2 heterogeneous (sonnet/analyzer, haiku/qa; opus executor excluded per §7.1)
**Calibrator class:** opus (disjoint from sonnet/haiku reviewers) · **Evidence-validator:** ran, 0/14 dropped (`zero_drop_flag: true`)
**Spec:** `.dev/brainstorms/sc-recommend-lookup-cache/merged-requirements.md`
**Status:** **partial** · **Promotion:** BLOCKED (drift > 0)

---

## Headline

The deterministic core is **correct and tested** — both reviewers and the evidence-validator independently confirm cache/dispatch/telemetry/best_model/grader/aggregate are faithful to spec, 45/45 tests pass, and the anthropic-SDK ban holds. **But the deep ensemble caught an integration gap that all 5 inline phase gates + 2 post-completion QA passes missed: the plugin eval gate (`plugin_eval.py`) is a fully orphaned, untested library, and the `--eval` Agent fan-out exists only as thin skill prose.** This is the canonical "inline QA verifies the helpers in isolation; reflect verifies the end-to-end wiring" blindspot.

The two heterogeneous reviewers diverged (A: CONDITIONAL FAIL / 3 "Regressions"; B: PASS / 0 Regressions) — the merge reconciled them: A's findings are **real** but **mis-classified** (they are Drift/Necessary, not Regression — none contradicts an acceptance criterion and all tests pass); B was right that nothing is broken but missed the wiring gap because its lens was helper-correctness.

## Deviation register (4-category taxonomy, precedence Regression>Drift>Necessary>Authorized)

| ID | Finding | Class | Evidence (Grounded) | Spec ref |
|----|---------|-------|---------------------|----------|
| F4 | **Plugin eval gate orphaned + untested.** `plugin_eval.py` defines `run_preconditions`/`evaluate_adoption`/`patch_plugin_row` but has **zero callers** — no CLI subcommand, no skill wiring, no `--plugin --eval` path, and **no test imports it**. | **Drift** (MEDIUM-HIGH) | `plugin_eval.py:56-147` (defs); grep: only self-references; `commands.py:193-290` (no plugin subcommand); no `tests/recommend/*` imports it | Impl Order step 8 (`:424-428`) — gate must be "wired" |
| F3 | **`--eval` Agent fan-out is thin skill prose.** The Python finalization IS wired+tested (`commands.py::eval_run` → `collect_run_records`+`finalize_eval`; 5 tests), but the per-(model,run) Agent fan-out that actually produces deliverables is a one-liner in SKILL.md, not the concrete protocol step 7 specifies. | **Drift** (MEDIUM) | `commands.py:255-285`; `SKILL.md:183-196`; `eval_pipeline.py:1-20` (assumes deliverables pre-exist) | Impl Order step 7 (`:416-423`, esp. `:263-265`) |
| F2 | **Classifier few-shot density below spec.** Spec asks 3-5 few-shots per key for ~10 keys; impl has few-shots for the 4 eval-backed keys only. | **Necessary** (LOW) — the eval set only covers 4 keys (evals 1,2,3,6), so few-shots for keys 5-10 are *impossible from the eval set*; documented as a Follow-Up. NOT a Regression (A over-classified). | `prompts.py:21-39` (keys 5-10 marked "no iteration-1 eval coverage"), `:67-80`; task Follow-Up | Impl Order step 3 (`:412`) |
| F1 | **R3 gitignore exception functionally inert.** `git check-ignore` → `.claude/cache/sc-recommend-lookup.yaml` still ignored by `.gitignore:117 .claude/` (directory-prune defeats the file-negations). | **`spec_is_wrong: true`** — NOT an implementation deviation. The spec's OWN prescribed block (`merged-requirements.md:87-100`) has the identical defect; the code faithfully implemented a defective spec prescription. | `.gitignore:117-124`; `merged-requirements.md:87-103`; `git check-ignore -v` | Gitignore Exception R3 (`:81-103`), step 1 (`:410`) |
| B1/B2 | Cosmetic: `compute_source_hash` param naming; `--eval` flag-table placement. | **Drift** (LOW, cosmetic) | Reviewer B card | — |

**Counts:** Regression **0** · Drift **2** load-bearing (F3, F4) + 2 cosmetic · Necessary **1** (F2) · Authorized: the remainder (steps 1,2,4,5,6 + the deterministic half of 7 + the helper half of 8 — all faithful) · `spec_is_wrong: true` (F1).

## Scope note (steps 9-12 legitimately out of scope)

Implementation Order steps 9-12 (hand-validate 6 invocations, run the 18-run eval matrix, compare to iteration-1, decision gate) are **operational eval-execution**, not code-build. The task correctly scoped steps 1-8. Their absence is not a deviation.

## Why the inline gates missed F4 (the value of this pass)

PG5's rf-qa "verified" `plugin_eval` by smoke-testing its functions in isolation and reading them — confirming they're *correct*. It never asked "is anything *calling* them?" or "is there a *durable test*?" Reflect's cross-task/integration lens (heterogeneous A-reviewer + independent grep) caught that the module is dead code with no integration path. This is precisely the `feedback_sc_reflect_vs_inline_rfqa` pattern: structural QA checks presence + correctness of units; reflect checks end-to-end wiring.

## Recommendations (file + change + verifier)

1. **Wire OR explicitly de-scope the plugin eval gate (F4).** Either (a) add a `recommend plugin-eval` subcommand in `commands.py` that calls `run_preconditions`→panel→`evaluate_adoption`→`patch_plugin_row`, plus a `tests/recommend/test_plugin_eval.py` (verify: HARD-BLOCK raises, adoption +≥10pp/−≥20% verdicts, plugin-row patch round-trip); OR (b) move `plugin_eval.py` to a clearly-marked "deferred, not wired" status and record the de-scope in the task. Verifier: `grep` shows a caller + `pytest tests/recommend/test_plugin_eval.py`.
2. **Flesh out the `--eval` fan-out in SKILL.md (F3).** Add the concrete per-(model,run) Agent-fan-out block (one Agent call per panel cell writing `outputs/recommendation.md` + `timing.json` under `eval-runs/iteration-<N>/<key>/<model>/run-<i>/`) so a reader can execute step 7 end-to-end. Verifier: prose names the run-dir layout `eval_pipeline.collect_run_records` expects.
3. **Fix the spec + the inert gitignore (F1).** Correct `merged-requirements.md:87-100` AND `.gitignore:117` to `.claude/*` + a `.claude/cache/*` re-ignore chain (block in `staging-guard-verdict.md`). Verifier: `git check-ignore -v .claude/cache/sc-recommend-lookup.yaml` returns non-ignored.
4. **F2:** no code change required; it is a Necessary deviation. Optionally hand-author synthetic few-shots for keys 5-10 (already a logged Follow-Up).

## Asymmetric-cost flags

`regression_present: false` · `spec_is_wrong: true` · `needs_human_decision: true` (F4 wire-vs-descope + F1 spec fix are decisions) · `unauthorized_deviation_present: true` (F4 wiring gap was not disclosed as deferred — only the *generators* were).

# BUILD_REQUEST — sc-recommend lookup-cache remediation (from /sc:reflect UC-2 audit)

**Origin:** `/sc:reflect --mode post --depth deep` audit of TASK-RF-20260603-032936.
**Reflection report:** `.dev/reflect/post-sc-recommend-cache-20260603202340/REPORT.md`
**Return contract:** `.dev/reflect/post-sc-recommend-cache-20260603202340/return-contract.yaml`
**Spec (gold standard):** `.dev/brainstorms/sc-recommend-lookup-cache/merged-requirements.md`
**Prior task (context):** `.dev/tasks/to-do/TASK-RF-20260603-032936/TASK-RF-20260603-032936.md`
**Boundary already resolved:** Option P (Python `cli/recommend/` owns deterministic ops; SKILL.md thin wrapper spawns Agents; anthropic SDK BANNED — all model runs subprocess/Agent-based; never `import anthropic`).

## Goal

Close the 3 integration/spec gaps the deep reflection ensemble found in the shipped sc-recommend lookup-cache. The deterministic core (cache/dispatch/telemetry/best_model/grader/aggregate) is correct and tested (45/45) — do NOT rebuild it. This remediation is wiring + tests + a spec/gitignore fix only.

## Scope — three findings to remediate

### Phase 1 — F4: wire (or formally de-scope) the plugin eval gate [Drift, MED-HIGH]

**Problem:** `src/superclaude/cli/recommend/plugin_eval.py` defines `run_preconditions`, `evaluate_adoption`, `patch_plugin_row` (verified correct in isolation by prior QA) but has **ZERO callers** — no CLI subcommand, no skill wiring, no `--plugin --eval` path, and **no test imports it**. Spec Implementation Order step 8 (`merged-requirements.md:424-428`) requires the gate to be WIRED.

**Required (choose 1a OR 1b; 1a preferred):**
- **1a (wire it):** Add a `recommend plugin-eval` subcommand (or extend `eval run` with a `--plugin <key>` branch) in `src/superclaude/cli/recommend/commands.py` that: runs `run_preconditions` (HARD-BLOCK on `failure_mode: hard`) → finalizes with/without-resource panels → `evaluate_adoption` → `patch_plugin_row` (atomic write to `.claude/cache/sc-recommend-plugin.yaml`). Wire the `--plugin --eval` lifecycle (4-phase: discovery → adoption proposal → decision gate → hot-path use) into `SKILL.md` Phase 3. Add `tests/recommend/test_plugin_eval.py` covering: HARD-BLOCK raises on missing precondition; adoption verdicts (+≥10pp pass OR −≥20% token, must_not_regress); plugin-row patch round-trip. Verifier: `grep` shows a caller + `uv run pytest tests/recommend/test_plugin_eval.py` passes.
- **1b (de-scope):** If wiring is out of scope for now, formally mark `plugin_eval.py` as "deferred / not wired" with a module docstring note AND record the de-scope in a tracked location, so it is not silently-dead code. Still add a minimal `test_plugin_eval.py` for the helper functions so they are not untested.

### Phase 2 — F3: flesh out the `--eval` Agent fan-out protocol in SKILL.md [Drift, MED]

**Problem:** the Python finalization IS wired+tested (`commands.py::eval_run` → `collect_run_records`+`finalize_eval`), but the per-(model,run) Agent fan-out that produces the deliverables is a one-liner in `SKILL.md` ("trigger the per-row eval pipeline"). `eval_pipeline.py:1-20` assumes deliverables already exist on disk. Spec step 7 (`merged-requirements.md:416-423`, esp. `:263-265`) requires the concrete fan-out.

**Required:** Add to `SKILL.md` the concrete fan-out block: on a `--eval <mode>` cold-path insert, the skill emits N parallel Agent-tool calls (one per `(model, run)` cell of the MODE_MATRIX panel), each instructed to produce `outputs/recommendation.md` + `timing.json` under `.claude/cache/eval-runs/iteration-<N>/<key>/<model>/run-<i>/`, THEN shell `superclaude recommend eval run --key <key> --mode <mode> --iteration <N>` to grade/aggregate/select/patch. Verifier: the prose names the exact run-dir layout `collect_run_records` reads (`eval_pipeline.py`).

### Phase 3 — F1: fix the inert gitignore exception (spec + code) [spec_is_wrong]

**Problem:** `git check-ignore -v .claude/cache/sc-recommend-lookup.yaml` → still ignored by `.gitignore:117 .claude/` (a directory-prune). Git cannot re-include a file under a pruned parent dir, so the R3 file-negations are inert. The spec's OWN prescribed block (`merged-requirements.md:87-100`) has the identical defect.

**Required:** Change `.gitignore` line 117 `.claude/` → `.claude/*` and insert a `.claude/cache/*` re-ignore between `!.claude/cache/` and the per-file negations (full corrected block in `.dev/tasks/to-do/TASK-RF-20260603-032936/phase-outputs/plans/staging-guard-verdict.md`). Apply the same correction to the spec block at `merged-requirements.md:87-100` so future implementers don't reproduce the defect. Verifier: `git check-ignore -v .claude/cache/sc-recommend-lookup.yaml` returns NON-ignored (exit 1 / no match); `git check-ignore .claude/cache/sc-recommend-events.jsonl` still ignored; `make verify-sync` exit 0.

## Out of scope (do NOT include)

- The deterministic core (cache/dispatch/telemetry/best_model/grader/aggregate) — already correct + tested.
- F2 (classifier few-shots for keys 5-10) — a Necessary deviation, impossible from the current 4-key eval set; remains a documented Follow-Up, not remediation.
- Spec steps 9-12 (operational eval-execution runs) — not code.

## Conventions (must honor)

UV-only; never `import anthropic`; source-of-truth is `src/superclaude/` then `make sync-dev` → `make verify-sync` (exit 0); never stage `.claude/` mirrors (only settings.json + the authorized cache exception); tests under `tests/recommend/`; add `recommend`-group changes via `src/`; per-phase rf-qa gates with adversarial stance + fix_authorization.

# Research: reflect's two Tier-2 engines (swarm engine vs skill panel) and the Stage 2 exit
**Investigation type:** Architecture Analyst
**Scope:** `src/superclaude/cli/reflect/` (all modules), `src/superclaude/skills/sc-reflect-protocol/SKILL.md` (ranges not read by scope slice 10), `scripts/reflect_shadow_exit.py`; scope slices 10, 11, 01 in `research/scope/`
**Status:** Complete
**Date:** 2026-11-14
---

## 0. Method, HEAD and command evidence (re-run by this agent, 2026-11-14)

- HEAD re-confirmed: `git rev-parse HEAD` = `50d4d2b9d1f2288afa497830b3049f2fe48f5c75`, branch `ironbelly/shadow-runs` [CODE-VERIFIED].
- Line counts re-confirmed with `wc -l`: `runner.py` 834, `ensemble.py` 895, `contract.py` 420, `panel_lint.py` 366, `config.py` 396, `commands.py` 585, `models.py` 182, `fallback.py` 594, `_diversity.py` 61, `__init__.py` 30; `sc-reflect-protocol/SKILL.md` 2033; `scripts/reflect_shadow_exit.py` 410 (matches slice 10 S1).
- Read-only check of `scripts/reflect_shadow_exit.py` (Read of L1-L410): it writes a file only when `--out` is given (`main`, L403-L405: `args.out.parent.mkdir(...)`, `args.out.write_text(...)`); with no `--out` it only reads (`collect` L203-L263, `_yaml_map` L74, `_json_map` L82). Docstring L3-L5 says the same. Safe to run without `--out` [CODE-VERIFIED].
- `uv run python scripts/reflect_shadow_exit.py` (no `--out`): printed `shadow runs counted: 13 of 20 required`, `MALFORMED audit.log rows: 0 (must be 0)`, `EV-1 failure rate (...) shadow 8/13 = 0.615; legacy baseline 3/39 = 0.077 (must be no higher)`, parity FAILS in 6 of 13 (shadow04, 15, 05, 09, 08, 07), lint/manifest problems in 9 of 13 (04, 15, 06, 03, 13, 05, 09, 08, 07), `verdict replay against the legacy baseline (42 runs): new degraded reasons 0`, `2-of-3 shortfalls: 0`, `unknown executor class ... : 9`, `findings-block compliance rate (mean over 9 run(s)): 0.704`, `cluster_agreement (9 run(s)): min 1.000, median 1.000, max 1.000`, last line **`OVERALL: FAIL (shadow runs 13 of 20)`**, exit status 1. One incomplete run listed: `pre-TASK-WF-detachTheCcsessi-20261102-034618-shadow02 (state clustered)`. This is exactly the expected output [CODE-VERIFIED by execution].
- `uv run pytest tests/cli/reflect -p no:cacheprovider -q`: last line `352 passed, 1 xpassed, 5 warnings in 40.99s` (the 5 warnings are Click `isolated_filesystem` deprecations in `test_contract_status_cli.py`) [CODE-VERIFIED by execution]. Matches the expected figure.
- Extra read-only run for open item (b): `uv run python scripts/reflect_shadow_exit.py --runs-root .dev/eval-workspaces/shadow-model-combos/runs` (no `--out`) printed `shadow runs counted: 15 of 20 required`, `EV-1 ... shadow 3/15 = 0.200; legacy baseline 0/0 = n/a`, `verdict replay against the legacy baseline (0 runs): new degraded reasons 29`, `OVERALL: FAIL (shadow runs 15 of 20)`. The 29 and the EV-1 failure are artifacts of an empty baseline (section 6.3).
- `git status --short -- src tests scripts` after all runs printed NOTHING (empty output): the tree is unchanged under `src`, `tests`, `scripts` [CODE-VERIFIED by execution]. (`__pycache__` dirs under `src/superclaude/cli/reflect/` exist but are gitignored, so they are not in the status.)
- Independence (rule R2): none of the paths that rule forbids was read, listed, grepped or cited; every repo-wide Grep here was scoped to `src`, `tests`, `scripts` or a single file.
- Scratch directory: none used (assignment names none).

---

## 1. `contract.py` (420 lines): the single verdict map

Re-read in full (L1-L420) at HEAD 50d4d2b9d. Every item below is [CODE-VERIFIED] at the cited line; slice 10 S7 agrees except where noted.

### 1.1 Structure and purity
- Module docstring L1-L13: "the SINGLE place the verdict map, the FR-11 degradation routing, and `contract_version` gating live"; PURE (only `.models`, stdlib, PyYAML, L15-L22); order "blocked -> degraded -> halted -> pass, first-match-wins" (L12).
- Public API: `parse_contract(path) -> dict | None` (L65); `derive_verdict(contract, *, expected_tier, allow_single_vendor, child_rc, promoting=False) -> ReflectResult` (L138-L260); private `_degraded_reason` (L263-L358), `_halted_reason` (L361-L382), `classify_fix` (L385-L420), `_extract_deviations` (L90), `_make_result` (L104).
- `parse_contract` "Tolerates unknown top-level fields (NFR-8 read-and-ignore)" (L69-L70): the code verdict path NEVER rejects an unknown key. Only `panel_lint.py` rejects them (section 3).

### 1.2 Gating order inside `derive_verdict`
1. BLOCKED: `child_rc == 124` -> `timeout` (L161-L164); any other non-zero rc -> `child-crash` (L169-L172); `contract is None` -> `contract-missing` (L173-L177); `contract_version` None or blank -> `contract-version-missing` (L179-L186); major != "1" -> `unknown-major-version` (L187-L194); `degraded_components` present and not a list -> `malformed-degraded-components` (L196-L206); any of the 7 `_LOAD_BEARING_BOOL_FIELDS` (L47-L57) present, non-None and not a `bool` -> `malformed-contract-boolean` (L210-L222).
2. DEGRADED via `_degraded_reason` (L225-L239): 14 trigger slugs in this order: degraded_components in `{auggie, env-aliases, evidence-validator}` (L31-L33, L274) -> `degraded-components`; `degraded-tier1` (L278); `degraded-model-diversity` when `t2_model_class_diversity` is not None and != "full" (L282-L284); `single-vendor` unless `allow_single_vendor` (L287); `adversarial-unavailable` (L291); `single-reviewer-fallback` (L295); `null-convergence` when `tier_reached == 2` and score None (L299); `degraded-subrun-partial` when `adversarial_subrun_status in ("partial","failed")` (L306); `low-convergence` when `tier_reached == 2`, score present and (non-finite, `< 0.80`, or unparseable) (L317-L326); `verification-skipped` unless skip reason is in `_VERIFICATION_SKIP_EXEMPTIONS = {read-only-project, tool-unavailable, --no-verify, no-verification-stage}` (L36-L38, L329-L345; `promoting` removes `tool-unavailable` and `read-only-project`, L339-L343); `citations-dropped` (L349-L350); `input-drift` (L355-L356).
3. HALTED via `_halted_reason` (L242-L246, L361-L382): `status-failed`, `status-partial`, `regression`, `unauthorized-deviation`, `needs-human-decision`, `user-decision-required`, then `deviation_count_by_class.regression > 0` -> `regression`, `.drift > 0` -> `drift`.
4. PASS only when `status == "success"` AND `tier_reached == expected_tier` (L249-L252); otherwise HALTED `tier-mismatch` (L255-L260).

### 1.3 The convergence threshold lives in code at 0.80
- Code: `_score_f < 0.80` at `contract.py:L321`, in the `low-convergence` trigger (L309-L326). A present score of 0.75 degrades (exit 11); the comment at L309-L311 names "the incident 0.75".
- Skill: SKILL.md routes 0.75 / 0.60 (re-read in section 5.3). So the two thresholds are layered but unreconciled: the code is the stricter gate. See open item (c), section 7.

### 1.4 Fields `derive_verdict` actually reads (re-derived by reading L138-L382)
`contract_version`, `degraded_components`, `tier_reached`, `status`, `t2_model_class_diversity`, `t2_vendor_diversity`, `adversarial_unavailable`, `merge_method`, `adversarial_convergence_score`, `adversarial_subrun_status`, `verification_ran`, `verification_skip_reason`, `citations_dropped`, `input_drift_detected`, `regression_present`, `unauthorized_deviation_present`, `needs_human_decision`, `user_decision_required`, `deviation_count_by_class`. `_make_result` additionally copies `report_path`, `remediation_task_path`, `remediation_plan_path`, `verification_verified`, `reviewers_verified`, `regression_verified` (L112-L134). It never reads `merged-verdict.yaml`, `reviewer_cards`, `evidence_validator_ran`, `citations_total`, `t2_effective_diversity` or `calibrator_diversity`. [CODE-VERIFIED, matches slice 10 S7.]
- Consequence for a unified panel: the only fields that change a wrapper verdict are the 19 above. The other 1.8.0 stable names are inert for the wrapper verdict but are load-bearing for CONSUMERS (SKILL.md 9.3, section 5.4).

### 1.5 `classify_fix` (L385-L420)
`human-required` on any hard signal (L410-L417), `auto-fixable` only for drift/necessary with no hard signal (L418-L419), else `none`. Docstring L400-L408 relies on the invariant "`needs_human_decision is True` IFF `grounding-gaps.yaml` is non-empty (SKILL.md:754)". **[STALE DOC]** the `SKILL.md:754` citation (the current location is checked in section 5.5).

### 1.6 The 36-test verdict matrix
`tests/cli/reflect/test_verdict_mapping.py` holds exactly 36 `def test_` functions (Grep `^def test_` listing, first at L22 `test_pass_full_tier2`, last at L609 `test_graph_tokens_do_not_halt`; no `parametrize` hits in that file) [CODE-VERIFIED]. It covers (by test name, with the pass-side counterparts of each trigger included): PASS (L22, L31, L48), DEGRADED triggers and their counterparts (tier1 L66/L93, single-vendor L105 degrades / L117 passes with the flag, verification L181 exempt / L193 degrades, subrun L393 degrades / L409 absent passes, convergence L432 low degrades / L447 at-or-above passes / L460 non-finite degrades, promote exemption L478 / L537, FX7 L572 / L594), BLOCKED (L129, L138, L148, L157, L231, L255), HALTED (L81, L290, L359), additive tolerance (L169, L306-L346), non-over-halting (L205, L217, L609). This matrix is what "the verdict map is frozen" means in code.

**Key Takeaways**
- `contract.derive_verdict` is a pure, engine-neutral function over a dict; both engines (swarm and skill) can feed it. It is the one piece of code that is genuinely shared.
- It ignores unknown keys and accepts any `1.x` version: the only code that enforces "1.8.0 and no new keys" is `panel_lint.py`, and only for panel runs (section 3).
- 19 fields decide the verdict; changing a name, value set or the 0.80 / `{auggie, env-aliases, evidence-validator}` / exemption sets changes exit codes 0/10/11/2 and breaks the 36-test matrix.

---

## 2. Engine A: the code-driven swarm ensemble (`ensemble.py`, 895 lines; `_diversity.py`, 61 lines)

Read in full (ensemble.py L1-L895, _diversity.py L1-L61). This is what `superclaude reflect run --depth standard|deep` runs for Tier 2 (the runner wiring is in section 4.1).

### 2.1 Data flow (traced)
1. `run_tier2_ensemble(config, ...)` L296-L511: creates `<output>/t2-swarm/` (L320-L323, `SWARM_SUBRUN_DIR = "t2-swarm"` L81); captures a single monotonic deadline from `config.timeout_seconds` (L329-L331).
2. Primary fan-out: `build_preflight_result` (L136-L151) builds a swarm `Manifest` with `CallerMetadata(suspect=True, tier="T2")`; `resolve_t2_transport_factory` (L154-L182) delegates to the swarm `_resolve_run_transport_factory` for live transports (T2 proxy-pool guard raises eagerly) or builds one vendor-distinct `StubTransport` per slot (`stub_model_id`, L130-L133, pool `("qwen","deepseek","gpt","mistral")` L127); `dispatch_wave1(preflight, transport_for_slot=factory, prompt=worker_prompt, worker_spec=WorkerSpec(count=reviewers, models=[], timeout_sec=...))` L343-L348.
3. Normalize: `normalize_wave2(stamped_workers, "passthrough", recipe_args=...)` L350-L358 (`REFLECT_REVIEW_RECIPE = "passthrough"` L80; the comment L76-L79 explains why `bare-review-v1` is not used).
4. Optional T1 fallback ladder (L364-L390), gated on `config.tier2_fallback_enabled`; it feeds the FULL augmented worker set into reduce and contract (L389), not the trimmed contributing subset (rationale comment L381-L388).
5. Reduce: `reduce_wave3(..., lens="reflect-review", recommended_next_command_template="/sc:adversarial --compare {compare_files} --suspect-source {suspect_files}")` L404-L419 writes `<output>/t2-swarm/return-contract.yaml` and a done sentinel (L420-L421).
6. Merge: only when `>= 2` reviewers succeeded and no pre-supplied score (L424-L435): `run_adversarial_scorer` L514-L561 launches a `ClaudeProcess` with the literal prompt `/sc:adversarial --compare <csv> --suspect-source <csv> --output <output>/t2-adversarial` (`build_adversarial_prompt` L582-L598), `reviewer_profile=True`, `cwd=config.reviewer_grounding_root` (L537-L552). A non-zero child rc returns `None`, leaving the score `None` so `contract.derive_verdict` routes DEGRADED `null-convergence` (comment L436-L438; `contract.py:L299`).
7. Parse adversarial result: `parse_adversarial_contract` L564-L579 tries `<output>/adversarial/return-contract.yaml` then `<output>/return-contract.yaml` (relative to `t2-adversarial/`); `extract_convergence_score` L633-L654 unwraps `return_contract:` and keeps a score only in `[0.0, 1.0]`; `extract_adversarial_status` L657-L679 lowercases/strips; `_extract_adversarial_report_path` L682-L697 reads `merged_output_path`.
8. Contract: `build_reflect_contract` L722-L835; written by `_emit_reflect_contract` (L886-L895) to `config.contract_path`; a `None` contract (zero succeeded workers, L752-L753) unlinks the file so the runner routes BLOCKED `contract-missing` (L887-L892).

### 2.2 What the engine hard-codes (every value is a constant or a function of the worker COUNT, not of evidence)
Source: `build_reflect_contract` L787-L832.
- `contract_version: "1.0"` from `REFLECT_CONTRACT_VERSION` (L74, L788). **Not 1.8.0.** [CODE-VERIFIED]
- `status: "success"` (L789), `mode: "post"` (L797), `audit_log_path: None` (L801).
- `tier_reached = 2 if reviewer_count >= 2 else 1` (L772); `merge_method = "adversarial" if reviewer_count >= 2 else "single-reviewer-fallback"` (L773). The value `adversarial` is therefore set by COUNT, even when the adversarial child failed (score None) or was never launched. [CODE-VERIFIED]
- `verification_ran: False` + `verification_skip_reason: "no-verification-stage"` (L808-L809): exempt in `contract.py:L36-L38`, so a swarm run is never DEGRADED for no verification even under `--promote` (comment `contract.py:L331-L337`).
- `verification_verified`, `regression_verified: False` (L814, L816); `citations_dropped: 0`, `citations_dropped_extrapolated: 0` (L817-L818); `input_drift_detected: False` (L819); `user_decision_required: False` (L823, comment cites "R2-F3").
- Deviation signal: `regression_present`, `unauthorized_deviation_present`, `needs_human_decision` default `False` and `deviation_count_by_class` defaults to four zeros (L103-L113, L779-L785); the `/sc:adversarial` score-only child cannot supply them (docstring L93-L95, L527-L533 "OQ-PRODUCER", "GAP-2 scope fork"). Only `convergence_score`, `report_path` (`merged_output_path`) and the sub-run `status` are live. [CODE-VERIFIED]
- `reviewers_verified = reviewer_count >= reviewers_requested` and the benign token `reviewer-shortfall` in `degraded_components` on a shortfall (L765-L770). The token is deliberately not in `contract._DEGRADED_COMPONENTS_HALT_SET` (comment L760-L764), so a 2-of-3 swarm stays PASS-eligible. [CODE-VERIFIED]
- `t2_model_class_diversity` from `_diversity.compute_model_class_diversity` (L803), `t2_vendor_diversity` from `compute_vendor_diversity` (L804).
- `deviation_count_by_class` and `regression_present` are produced by NO reviewer reading in this engine. The engine never reads a reviewer body for a defect class: a swarm Tier-2 verdict of PASS says "reviewers disagreed no more than 0.20 apart and nothing crashed", not "no deviation was found". [CODE-VERIFIED by reading; this is a design property to flag, not a doc claim]

### 2.3 What the swarm reviewers see
- `build_worker_prompt` L601-L616 composes `lens.system_prompt_fragment` + `lens.user_template` with `{target_content}` replaced by `_load_review_target` (L619-L630) = header `# Reflect Tier-2 review target / Base ref: <base> / Tasklist: <path>` plus the TASKLIST BODY ONLY. The docstring says "full git-diff materialization is a rollout refinement (logged follow-up)" (L607-L608). Reviewers therefore audit the tasklist text, not the code diff. [CODE-VERIFIED] Contrast with the skill engine whose reviewer briefs hold `## T1 card excerpt`, `## Grounding hunks`, `## Coverage slice` (reviewer-spec.md, quoted in slice 10 S9.3).
- The lens file is `superclaude.cli.swarm.lenses.reflect_review.LENS` (import L44-L46). I did not open the lens file (it is outside the assigned code list) [UNVERIFIED content of the lens text; the import is CODE-VERIFIED].

### 2.4 Key numbers of the key probe (re-derived with `uv run python -c`, read-only, no files written)
`build_reflect_contract` called with two succeeded stub workers (`qwen-a`, `gpt-b`, `reviewers_requested=3`) returned:
- `contract_version` `1.0`, `merge_method` `adversarial`, `tier_reached` 2, `t2_model_class_diversity` `full`, `t2_vendor_diversity` `multi`; 32 top-level keys.
- Keys NOT in `panel_lint.STABLE_FIELDS_1_8_0` (110 names) + `TELEMETRY_FIELDS` (27 names): exactly 10: `adversarial_subrun_status`, `audit_tree_dirty`, `regression_verified`, `reviewer_count`, `reviewer_grounding_root`, `reviewer_isolation`, `reviewers_verified`, `subrun_status`, `subrun_status_partial`, `verification_verified`. [CODE-VERIFIED by execution; matches slice 10 S6.2 probe]
- 89 of the 110 stable names are ABSENT from the swarm contract (e.g. `reviewer_cards`, `evidence_validator_ran`, `citations_total`, `deviation_register_path`, `input_sha256`, `t2_effective_diversity`, `calibrator_diversity`). [CODE-VERIFIED by execution: `len(set(STABLE) - set(contract)) == 89`]
- Two same-vendor workers (`qwen-a`, `qwen-b`): `t2_vendor_diversity: single`, `t2_model_class_diversity: full` (so the wrapper degrades `single-vendor` unless `--allow-single-vendor`).
- One succeeded worker: `tier_reached` 1, `merge_method` `single-reviewer-fallback`, `t2_model_class_diversity` `insufficient`.

### 2.5 `_diversity.py` details
- `compute_model_class_diversity` (L8-L15): `"full"` iff at least two distinct succeeded `model_id` values, else `"insufficient"`. SKILL.md's vocabulary for `t2_model_class_diversity` is `full|degraded` (slice 10 S5, SKILL.md 9.1); `contract.py:L283` degrades on any value `!= "full"` so both words behave the same, but they are different strings in the same field. [CODE-VERIFIED code side; SKILL.md side from slice 10 S5, re-read in section 5.4]
- `compute_vendor_diversity` (L18-L36): `None` when fewer than 2 succeeded; `multi` when >= 2 vendors, else `single`.
- `_vendor_from_model_id` (L39-L61): ordered substring table. Edge case: marker `"o1"` -> `openai` (L46) is matched by substring against the lowercased id, so any id containing `o1` (for example a version string) is classed OpenAI. The table order also means `"gpt"` is tested before `"o1"`, `"claude"` after `"gemini"`. No test of this edge was searched here [UNVERIFIED that none exists].
- Both engines' diversity fields come from DIFFERENT sources: the swarm engine computes them from served `model_id`s of workers (evidence), while the skill engine records the REQUESTED rotation (section 5.1, slice 11 3.3).

**Key Takeaways**
- The swarm engine is an independent, fully code-driven producer of a 1.0-shaped contract. It shares with the skill engine only `contract.derive_verdict` (via `parse_contract`) and `fallback`/`_diversity` helpers that exist only on its side.
- It cannot report deviations: all four deviation classes are 0 and `regression_present` is `False` by construction. It is a convergence-and-diversity gate, not a deviation audit. The skill engine is the only one that classifies deviations (reflect-reviewer, SKILL.md section 10).
- `merge_method: adversarial` is a count-derived label; EV-1/EV-2 as a disk check cannot apply to this engine (it writes `t2-swarm/` and `t2-adversarial/`, not `adversarial/merged-verdict.yaml`).
- Reviewers see the tasklist body only (no diff, no spec): their evidence base is strictly narrower than the skill engine's grounded briefs.

---

## 3. `panel_lint.py` (366 lines): the 1.8.0 shape gate

Read in full (L1-L366).

### 3.1 What it fixes in place
- `STABLE_FIELDS_1_8_0` (L33-L144) = 110 names; `TELEMETRY_FIELDS` (L146-L174) = 27 names including `telemetry`; `PARITY_FIELDS` (L177-L183) = `t2_model_class_diversity`, `t2_vendor_diversity`, `t2_effective_diversity`, `calibrator_diversity`, `reviewer_cards`; `LEGAL_MERGE_METHODS = ("adversarial", "single-reviewer-fallback")` (L184); `CONTRACT_VERSION = "1.8.0"` (L185); `LOAD_BEARING_BOOLS = _LOAD_BEARING_BOOL_FIELDS` imported from `contract.py` (L31, L176). Counts re-derived by `uv run python` (110 and 27) [CODE-VERIFIED by execution].
- The docstring (L14-L18) says the two lists are copies of the YAML blocks in SKILL.md 9.1 and 9.2 and that a test fails when they drift; `extract_field_list` (L192-L197) is that extractor.
- Assertion map in `lint_panel_contract` (L302-L366): L0 (L306-L309) file missing; L1 (L311-L315) version != "1.8.0"; L2 (L316-L325) any top-level key not in stable + telemetry + `telemetry`, and `telemetry` must be a mapping; L3 (L326-L334) `merge_method` illegal (null allowed only on Tier 1); L4 (L335-L339) score must be `float` and finite or null (`type(score) is float`, so an int `1` fails); L5 (L340-L346) load-bearing booleans must be real bools, and `adversarial_unavailable` plus `regression_present` are required when Wave 4 ran; L6 (L347-L348 -> `_ev1` L246-L299) EV-1; L7 (L349-L359) parity of the five `PARITY_FIELDS`; B (L360-L365) bump rule message.
- `_ev1` (L246-L299): required = `max(2, resolved)` where `resolved` = `reviewers_resolved` from `panel/manifest.json` when valid (and `use_manifest`), else `len(reviewer_cards)` (L249-L270). Pass 1: `adversarial/merged-verdict.yaml` is a mapping with `merge_method == "adversarial"` and `reviewer-cards/` holds `>= required` files matching `_CARD_FILE = ^reviewer-(\d+)-card\.(?:yaml|yml|md)$` (L188, L271-L278). Pass 2 (loud fallback): `adversarial_unavailable is True` AND `merge_method == "single-reviewer-fallback"` AND an `audit.log` row matching `\bF[23]\b` (L189, L279-L298).
- `ev1_failures(..., use_manifest=False)` (L236-L243) exists for the exit script so shadow and legacy runs use the same rule (docstring L239-L241).

### 3.2 What the lint does NOT cover
- The `--unattended` layout `nested/adversarial-<n>/` (docstring L9-L12): `L6` reports `merged-verdict: absent` there.
- The lint is called ONLY from `scripts/reflect_shadow_exit.py` (L240 `pl.lint_panel_contract(run, contract)`, L194 `pl.ev1_failures`) and from tests; the runner, commands and ensemble never import it. [CODE-VERIFIED by Grep in section 4.5]
- The swarm engine's contract would fail it at L1 (`1.0` != `1.8.0`) and at L2 (10 unknown keys, section 2.4) and L7. The docstring scopes the lint to "panel-run contracts and the matched legacy fixture" (L11-L12). So the two engines are not just un-reconciled in prose: one of them is lint-hostile by construction.

### 3.3 A skill/lint inconsistency the lint itself exposes
- `reviewer_briefs_materialized` is emitted by the skill's own instruction ("the contract emits `reviewer_briefs_materialized: <N>`", `src/superclaude/skills/sc-reflect-protocol/refs/reviewer-spec.md:78`; also L51 and L57) but is in NEITHER `STABLE_FIELDS_1_8_0` NOR `TELEMETRY_FIELDS`, and Grep over SKILL.md and the repo (excluding `.dev`, `.claude`, `__pycache__`) found no occurrence of it in SKILL.md 9.1/9.2 [CODE-VERIFIED by Grep: hits only in `refs/reviewer-spec.md` L51, L57, L78]. The lint therefore fails every run that follows the ref. In the combo runs it is the top-level key that triggers L2 in 5 of 15 runs (section 6.2). This is a mechanical contradiction between two files of the same skill, not an orchestrator mistake.

**Key Takeaways**
- `panel_lint.py` is the only code that makes "contract 1.8.0, no new keys, no new `merge_method` values" executable; it is a pure function that could run inside any engine's output step.
- Its two lists must equal SKILL.md 9.1/9.2 (test-pinned). Any field a new unified module wants to emit must be added to SKILL.md first, and the `reviewer_briefs_materialized` gap shows the current skill already violates that rule.
- It encodes a file layout (`adversarial/merged-verdict.yaml`, `reviewer-cards/reviewer-<N>-card.*`, `audit.log` with an `F2|F3` row) that the shadow steps in SKILL.md do not produce (section 5.2), so 5 of 13 pilot EV-1 failures are layout or naming mismatches (4 `merged-verdict: absent`, 1 empty `reviewer-cards/`) and 3 are a contract file that is present but not parseable YAML (section 6.1; fix cycle 1: the earlier "8 of 13 are layout mismatches" contradicted section 6.1).

---

## 4. The wrapper around engine A: `runner.py` (834), `config.py` (396), `commands.py` (585), `models.py` (182), `fallback.py` (594), `__init__.py` (30)

Read: `runner.py` L1-L120, L440-L620, L686-L834 (the remainder is the sidecar/write-back/preflight code described in slice 10 S6.1 [UNVERIFIED by this agent beyond the cited reads]); `config.py` L236-L396; `models.py` L1-L183 in full; `commands.py` L236-L275 plus a Grep of the option names; `fallback.py` L1-L110 plus a Grep of every `def`/`class`/constant.

### 4.1 Wiring (the answer to "which engine does `superclaude reflect run` use")
- `ReflectRunner._audit_once` (`runner.py` L513-L582): `expected_tier = 2 if config.depth in {"standard","deep"} else 1` (L538); when `expected_tier == 2` AND `ClaudeProcess is _ProductionClaudeProcess` (L540) it calls `run_tier2_ensemble(config)` (L544) and sets `rc = 0` (L545); otherwise it launches the Tier-1 `/sc:reflect` child through `ClaudeProcess` (L549-L572). The only reason for the identity test is that the legacy mocked tests patch `runner.ClaudeProcess` (docstring L521-L535). [CODE-VERIFIED]
- Depth reaches the runner as `standard` or `deep` only: the CLI choice is `click.Choice(["standard","deep"])` (`commands.py` L253-L257), and `resolve_config` floors `quick` to `standard` (`config.py` L318-L319). So in production the wrapper ALWAYS runs engine A for Tier 2; the skill's `/sc:reflect` child is reachable only from a test double. [CODE-VERIFIED]
- Verdict: `derive_verdict(contract, expected_tier, allow_single_vendor, child_rc=rc, promoting=config.promote)` (L573-L580) on `parse_contract(config.contract_path)` where `contract_path = <output>/return-contract.yaml` (`models.py` L119-L122).
- Prompt for the Tier-1 child `_build_prompt` (L453-L483): `/sc:reflect --mode post [--no-promote] [--no-reachability] --diff <base> --tasklist <p> [--spec <p>] --depth <d> [--remediate] [--executor-model <m>] --output <dir>`. It never passes `--t2-engine`. [CODE-VERIFIED]
- Grep over all of `src/superclaude/cli/reflect/*.py` for `merged-verdict|t2.engine|t2_engine|review panel|review manifest|panel_lint|lint_panel|shadow|findings-v2|findings_v2|cluster` hits ONLY `panel_lint.py` (L3, L5, L10, L11, L241, L271, L297, L302). The runner, config, commands, ensemble, contract and fallback modules contain no shadow, panel, manifest, cluster or findings-v2 logic. [CODE-VERIFIED by Grep, 2026-11-14] Negative evidence: no import of `superclaude.cli.review` anywhere in the reflect package.
- Who calls the wrapper: `sc-tasklist-protocol/SKILL.md` L1133-L1165 and `templates/phase-template.md` L156-L182 emit `superclaude reflect run <phase-tasklist> --depth deep --fix --no-promote --base <PHASE_N_START_SHA> --output <...>/validation/reflect-post/phase-<PP>/` as the per-phase terminal gate; `task-builder/SKILL.md` L59/L1084 emits it only with `CLI_MODE=true`. [CODE-VERIFIED by Read/Grep] The shadow engine in SKILL.md (`--t2-engine shadow`) is reached only by `/sc:reflect --mode pre` invocations (sc:workflow Wave 4, sc-tasklist Stage 10.5 per slice 01 C2 [CODE-VERIFIED there at `sc-workflow-protocol/SKILL.md:89,:105` and `sc-tasklist-protocol/SKILL.md:1621,:1630`]), never by the wrapper.

### 4.2 Consequences found while reading the wrapper
- **`--fix` has no producer in production.** The loop (L748-L793) auto-fixes only when `derive_verdict` returns HALTED, `classify_fix(...) == "auto-fixable"` and a remediation pointer exists (L765-L775). Engine A's contract (ensemble.py L787-L832) carries NO `remediation_task_path` or `remediation_plan_path`, hard-codes `status: "success"`, zero deviations and `regression_present: False`, so HALTED cannot arise from it unless an adversarial result supplies signals, and the live adversarial seam supplies none (ensemble.py L93-L95, L527-L533). The sc-tasklist gate passes `--fix` anyway. [CODE-VERIFIED by reading; not exercised by me with a live run] Net: in production the wrapper's reachable verdicts from engine A are PASS, DEGRADED and BLOCKED; HALTED (exit 10) and the auto-fix loop are structurally dormant. This is a property of the code, not of any document.
- **The executor-class exclusion is not applied by engine A.** `config.executor_model` (resolved from env `EXECUTOR_MODEL_CLASS` or frontmatter `executor_model_class`, `config.py` L53, L350-L355) is used in exactly one place: appended to the Tier-1 `/sc:reflect` prompt as `--executor-model` (`runner.py` L480-L481). Grep for `executor_model|executor_class` in `src/superclaude/cli/reflect/` hits only `config.py` (L53, L351, L355, L376), `runner.py` (L480, L481), `models.py` (L71) and the telemetry name list in `panel_lint.py` (L154-L155); Grep over `src/superclaude/cli/swarm/` finds 0 matches. [CODE-VERIFIED by Grep]
  - **[STALE DOC] / [CODE-CONTRADICTED]** `sc-tasklist-protocol/SKILL.md` L1141 and L1152 state that the wrapper "spawns an executor-disjoint reflect ensemble internally", and L1165 says "the wrapper sources the reviewer-exclusion class from the phase file's frontmatter `executor_model_class`". `task-builder/SKILL.md` L2247 says the wrapper's POST subprocess "MUST resolve to OUR `sc-reflect-protocol` skill (the canonical executor-class-exclusion model)". The code shows that in production the wrapper does not run the skill and does not apply any exclusion (L538-L545 above). These statements describe the intended design, not the current code.
- **Two diversity vocabularies and two EV-1 notions are simultaneously live**: engine A's `merge_method` is count-derived (ensemble.py L773) and its output layout is `t2-swarm/` + `t2-adversarial/`; the skill engine's is disk-checked (`adversarial/merged-verdict.yaml`, `panel_lint._ev1`). Nothing in `runner.py` or `contract.py` reads `adversarial/merged-verdict.yaml` (Grep above).
- **Promotion default drift**: the Click default is `--promote` True (`commands.py` L236-L239, help says "default: --promote"), while `runner.py` L457-L459 comment says "--no-promote is the hard default; dropped only on --promote" and `resolve_config(promote=False)` is the function default (`config.py` L253). [CODE-CONTRADICTED comment vs CLI default; slice 10 S6.3 agrees.] Relevance: `promoting=True` changes `derive_verdict` exemptions (`contract.py` L339-L343).
- **`cli/reflect/__init__.py` docstring** [STALE DOC, slice 10 S6.3, not re-opened by me beyond its 30-line count]: describes a `claude --print` subprocess that "fans out Tier 2" and lists only five modules; the real Tier 2 is the in-process swarm (runner.py L538-L545).

### 4.3 `config.py` facts that bound a unified core (re-read L236-L396)
- Reviewers: `--reviewers` int clamped to `[2,4]`, `1` preserved as the "negative witness" (L334-L335). Stub transport defaults the T1 fallback ladder OFF (L340). `quick` is floored to `standard` (L318-L319). Output default `<task-dir>/reflect/post/<HEAD[:12]>/` (L357-L363); `--output` under `.claude/{skills,agents,commands}` rejected (L364-L368). Timeout default via `_DEFAULT_TIMEOUT_SECONDS`, max_turns `_DEFAULT_MAX_TURNS` (L379-L380) (values 3600 and 250 per slice 10 S6.3 [UNVERIFIED here; constants not re-read]).
- Nothing in `config.py` resolves a panel template, a model class, a persona or a tier file: engine A's model choice is `T2Model0N`/`T1Model0N` env slots via `swarm`, a THIRD registry besides the skill's `ANTHROPIC_DEFAULT_{OPUS,SONNET,HAIKU}_MODEL` and the review kernel's tier JSON (slice 01 §4.6 verified the first two at HEAD).

### 4.4 `fallback.py` (594 lines) facts that matter for the core
- Pure planner functions come first (`is_fallback_eligible` L106, `build_fallback_metadata` L111, `classify_outcomes` L152, `evaluate_quorum` L161, `plan_next_attempt` L182, `select_contributing_set` L229, `make_fallback_slot_factory` L263), then the one impure controller `run_fallback_ladder` (L411), per its docstring L1-L4.
- `FALLBACK_ELIGIBLE_STATUSES = {timeout, proxy_error, parse_error}` (L40); `TERMINAL_REASONS` (8 slugs, L49-L58); `TIER2_CERTIFICATION_BASES = (primary_only_quorum, primary_plus_fallback_quorum, not_certified)` (L59-L63); wall-clock floor 1.0 s (L48).
- It encodes the Tier-2 gate as `QuorumState(reviewer_count, model_class_diversity, vendor_diversity, satisfies_tier2)` (L76-L82): "Tier 2 = at least 2 reviewers, >= 2 distinct model ids, and not single-vendor". This is the same gate as the engine's contract fields, computed by `_diversity` helpers. It exists only for the swarm engine; the skill engine has no code-side equivalent (its quorum rule is prose in SKILL.md 7.1).

**Key Takeaways**
- In production, engine A is THE Tier-2 engine behind `superclaude reflect run`; the skill's panel path (shadow) is invisible to the wrapper. Documents claiming otherwise (executor-disjoint ensemble; wrapper resolves to the skill) are [CODE-CONTRADICTED].
- Engine A is a convergence-and-diversity gate with dormant deviation, HALTED and `--fix` machinery. Its value is: code-enforced 4-state exit codes, fail-closed gating, atomic write-back, recursion breaker, reviewer-isolation snapshot, bounded fallback ladder.
- The strongest transferable assets of the wrapper (fail-closed verdict map, atomic frontmatter write-back, snapshot isolation, recursion marker, bounded ladder) are all independent of which reviewer engine produces the contract.

---

## 5. Engine B: the skill panel (`SKILL.md`, 2033 lines) and its `--t2-engine shadow` path

Read for this section (ranges not read by slice 10): SKILL.md L508-L621 (grounding chain 6.1, bash envelope 6.1.1, memory 6.3, fail-open 6.5), L872-L935 (contract tail), L1047-L1203 (deviation taxonomy), L1293-L1708 (eval rubric, build path, error matrix, Wave 7 promotion), L1740-L1849 (metrics, refs table); anchors L84-L89, L305-L349; plus re-reads of L690-L714, L833-L841, L960-L1039 to quote values. All [CODE-VERIFIED] at HEAD as the SKILL text (a prose engine: "verified" here means the sentence exists at that line; whether an orchestrator obeys it is measured only by the shadow/combo evidence in section 6).

### 5.1 What the skill engine is
- A Claude-orchestrated Wave 0-7 pipeline written as prose. Tier 2 = N read-only `reflect-reviewer` agents (fixed agent type; persona and model class supplied by the brief/rotation, SKILL L646-L656 per slice 10 S3), blind calibration by `confidence-calibrator`, a legacy debate through `Skill sc-adversarial-protocol` (L691-L699), an `evidence-validator` gate, then the 1.8.0 contract (L724-L860) and optional Wave 7 promotion (L1518-L1707).
- Its grounding chain (6.1, L508-L530) gives reviewers/orchestrator codegraph/auggie/Grep/Read, `reuse-auditor`, a verification run through Bash (5.5), a contracted-sink reachability gate (5.6, L550) and a required-capability pass (5.6a, L552-L559). None of that exists in engine A.
- Deviation taxonomy (SKILL section 10, L1042-L1202): 4 classes with by-evidence precedence Regression > Drift > Necessary > Authorized (L1133-L1135); Grounding Gaps are a separate artifact (L1137-L1161); Reuse-Miss, runtime-surface UNREACHED and contracted-sink findings are modifiers that MAP onto the 4 classes (L1167-L1200). Exit-code to class table for verification (L1105-L1117). This is the only place in the repo where `regression_present` is actually decided from evidence.

### 5.2 The shadow path (SKILL L87, L309-L349)
- Flag: `--t2-engine legacy | shadow` default `legacy`; `panel` is rejected "ships in Stage 3" (L87). Rules D1-D5 (L317-L321); decision table (L323-L336); UC-1 only, "In UC-2 (post-execution) runs the flag is accepted and ignored until Stage 5" (L311). Under `legacy` "the panel code is never called" and contract 1.8.0 is unchanged (L311).
- Ten numbered shadow steps (L340-L349). They run next to the legacy waves, change no verdict and "everything the panel writes goes under `<output>/panel/`" (L338). Each is performed by the ORCHESTRATOR LLM following prose, calling the `superclaude review` CLI (`panel resolve`, `manifest init/advance`, `cluster`, `verify-citations`) and writing files itself.
- Classification of the 10 steps (my reading; evidence for each failure class is in section 6):

| # | Step (SKILL line) | Deterministic given inputs? | Current performer | Observed failure class (section 6) |
|---|---|---|---|---|
| 1 | Resolve and freeze: `panel resolve ... --hard-exclude-class <executor> --strict-distinct`, `manifest init`, write `panel/resolution.json` verbatim (L340) | Yes (CLI output copy) | LLM + CLI | none recorded |
| 2 | Parity: compare resolution vs legacy rotation; card headers `persona:`/`model_class:`/`model:` copied from `reviewers[N].model` (L341) | Yes | LLM | 6 of 13 pilot parity failures (alias in header, missing rotation keys) |
| 3 | Briefs + dispatch, record attempts in manifest (L342) | Mostly | LLM + CLI | none |
| 4 | Normalize: parse `## Findings block`, first-parse compliance rate, one bounded re-ask (L343) | Parse yes; re-ask is judgment | LLM | compliance mean 0.704 (9 pilot runs), see 6.1 |
| 5 | Calibration: write `panel/cards/reviewer-<N>.md` with header lines, findings block, fenced `yaml` `calibration:` (L344) | Assembly yes; scores are LLM | LLM | card-write corruption (slice 11 3.2) |
| 6 | Cluster + `verify-citations`, write `coverage.json` when coverage rows exist (L345) | Yes | LLM + CLI | none |
| 7 | Legacy debate, then write `<output>/adversarial/merged-verdict.yaml` "copy, never invent a value" (L346) | Yes (copy) | LLM | 4 of 13 pilot EV-1 failures (nested dir or `.md` only) |
| 8 | `kept-ids.txt`, `clusters_kept` pass (L347) | Yes | LLM + CLI | none |
| 9 | Identity: `identity_source`, self-report comparison (L348) | Mostly | LLM | self-reports unreliable (slice 11 3.2) |
| 10 | Publish: confirm no top-level key outside the stable list, `manifest advance --stage published` (L349) | Yes (lint) | LLM | 7 of 28 counted runs leaked keys (6.2) |

### 5.3 Convergence thresholds in the skill vs code (open item c, skill side)
- SKILL L703: "Convergence routing: >=0.75 PASS, >=0.60 PARTIAL, <0.60 FAIL" and "no synthetic 0.5 fallback". SKILL L1317 (eval rubric): the falsifier AUTO-FAILs "if `convergence_score >= 0.75 AND verdict != regression_present`". [CODE-VERIFIED]
- Code: `contract.py` L321 degrades below **0.80** and has no PARTIAL/FAIL band: any present score below 0.80 is the single reason `low-convergence` (exit 11); `test_verdict_mapping.py` L432-L445 pins "0.75 degrades" and L447-L458 pins "at/above 0.80 passes" (the Grep shows the strings "the incident 0.75 < 0.80" at L434 and "0.80 threshold" at L449). [CODE-VERIFIED]
- So the 0.75-0.7999 band is PASS in the skill and DEGRADED in the wrapper. The skill's 0.60 floor, PARTIAL band and the null-handling rules (L707-L712: `status: partial`, `next_action: halt-phase-for-review`) have no counterpart in `contract.py` except the null-convergence DEGRADE (L299-L300). Nothing reconciles them. (`convergence_score` is also used by the promotion gate condition 9, L1551: "`tier_reached == 2` AND null blocks promotion".)

### 5.4 Other skill-vs-code vocabulary conflicts found (all [CODE-VERIFIED] on both sides)
| Item | SKILL.md says | Code does |
|---|---|---|
| `t2_model_class_diversity` values | `full \| degraded` (L838, L1480, L1755) | engine A emits `full \| insufficient` (`_diversity.py` L15); `contract.py` L283 treats any non-`full` as degraded |
| single vendor | "warn-only in v1.0" (L839), "Continue; WARN" (L1481) | `contract.py` L287-L288 DEGRADES (exit 11) unless `--allow-single-vendor` |
| `contract_version` | `1.8.0` (L727) | engine A emits `1.0` (`ensemble.py` L74, L788); lint demands `1.8.0` (`panel_lint.py` L185, L312-L315) |
| `merge_method` meaning | `adversarial` only after a real merge, confirmed on disk (EV-1, L714) | engine A sets `adversarial` when `reviewer_count >= 2` (`ensemble.py` L773) |
| skill version | frontmatter `version: 1.0.0` (slice 10 S1, L4), contract 1.8.0, metrics example `"skill_version": "1.7.0"` (L1815) | three version strings live in one skill |
| `reviewer_briefs_materialized` | `refs/reviewer-spec.md` L78 demands the contract emit it | absent from `STABLE_FIELDS_1_8_0`/`TELEMETRY_FIELDS` and from SKILL.md 9.1/9.2 (section 3.3) |
| Contract growth rule | additive new fields are a MINOR bump and consumers MUST read-and-ignore (L1019-L1021, L1038) | lint rule B (`panel_lint.py` L360-L365) says any new top-level key "needs a contract version bump, which this plan does not make": the Stage-2 plan froze 1.8.0, SKILL.md itself permits 1.9.0 |

### 5.5 Stale citation inside `contract.py`
`classify_fix` docstring (`contract.py` L403) cites "SKILL.md:754" for the invariant `needs_human_decision is True` IFF grounding-gaps non-empty. The invariant is stated at SKILL.md L1155-L1159 (§10.6: "When `grounding-gaps.yaml` is non-empty: `status: partial` is forced; `needs_human_decision: true`...") [CODE-VERIFIED]. [STALE DOC] line cite only; the invariant holds. SKILL.md L754 was not re-read for what it now contains [UNVERIFIED].

### 5.6 What the byte-identity tests actually guard
`tests/cli/reflect/test_shadow_skill_contract.py` L42-L49 compares the working-tree 9.1 block with `git show HEAD:<SKILL.md>`; L52-L75 allows working-tree diffs against `HEAD` only under sections `### 3.1`, `### 4.3a`, `### 5.4`, `### 9.2`. The reference is the CURRENT `HEAD`, not a frozen commit, so these tests constrain uncommitted edits only; after a commit they re-baseline. [CODE-VERIFIED by Read L42-L75] The only frozen-by-test link is `tests/cli/reflect/test_panel_contract_lint.py::test_pinned_field_lists_match_skill_md` (L97), which ties `panel_lint.STABLE_FIELDS_1_8_0`/`TELEMETRY_FIELDS` to SKILL.md sections 9.1/9.2 at the same commit, and `test_constant_sizes_and_load_bearing_import` (L107). [CODE-VERIFIED by Grep of function names; bodies not read] This matters for open item (a): "byte-identical" is a convention backed by a lint and one same-commit pin, not by a frozen baseline.

**Key Takeaways**
- Engine B is the only engine that grounds, calibrates, validates and classifies; it is also the only one whose correctness depends on an LLM orchestrator performing deterministic steps (copy, name, layout) from prose.
- Of the 10 shadow steps, 7 are deterministic given their inputs and all observed shadow failures are in those steps (section 6), none in the review judgment steps.
- The skill and the code disagree on 6 vocabulary points (threshold, diversity enum, vendor severity, contract version, merge_method semantics, growth rule); none is reconciled by a test.

---

## 6. The Stage 2 exit: what fails, why, and which failures are mechanical

All numbers below were produced by me on 2026-11-14 with the commands in section 0 (the exit script run twice with different `--runs-root`; the `ls` counts quoted in 6.2).

### 6.1 State of the exit at HEAD (re-derived)
- `OVERALL: FAIL (shadow runs 13 of 20)`, exit 1 [CODE-VERIFIED by execution]. Three independent reasons, each sufficient: (i) the count: 13 < 20 (even a flawless remainder leaves the verdict INSUFFICIENT-RUNS, exit 3, per `reflect_shadow_exit.py` L376-L381); (ii) the EV-1 rate `8/13 = 0.615` vs legacy `3/39 = 0.077` (L307-L314); (iii) parity FAILS 6 of 13 and lint/manifest problems 9 of 13 (L316-L335).
- `MALFORMED audit.log rows: 0`, `verdict replay ... new degraded reasons 0` (42 legacy runs), `2-of-3 shortfalls: 0`: these three gates are clean.
- Mean first-parse compliance `0.704` over 9 runs; `cluster_agreement` min=median=max 1.000 over 9 runs. Slice 11 explains why 1.000 is vacuous (agreement is 1.0 by definition when no blocking cluster exists, `cluster.py:50`, [CODE-VERIFIED by slice 11; I did not re-open cluster.py]).
- Failure arithmetic: the 13 counted pilot runs fail the exit script on EV-1 in 8 runs (`no contract` 04, 09, 08 -> 3, where the exit script's label `no contract` means a `return-contract.yaml` that EXISTS but does not parse as YAML, not a missing file [fix cycle 1, CODE-VERIFIED: `ls -l` shows the file present in all three; `yaml.safe_load` raises `YAMLError ... expected ',' or ']', but got '['` at line 103 `reviewer_models: [claude-gw-tier1b[1m], ...]`; `_yaml_map` at `scripts/reflect_shadow_exit.py:74-79` maps YAMLError to None, `:224` `or {}`, `:242-243` print `no contract`]; `merged-verdict: absent` 06, 03, 05, 07 -> 4; `reviewer-cards/ holds 0 card(s)` 15 -> 1) and on parity in 6 (card `model:` header carries a harness alias 04, 05, 09, 08 -> 4; `legacy rotation ... not in the contract` 15, 07 -> 2).

### 6.2 Mechanical vs judgment classification (open item b)
Every failure line the exit script printed is produced by a presence/name/equality check in code I read (`panel_lint._ev1` L246-L299, `lint_panel_contract` L302-L366, `recompute_parity` `reflect_shadow_exit.py` L117-L177): file exists, file name matches a regex, key is in a tuple, two strings are equal, a count meets a number. None reads review content.

| Failure class | Runs (pilot 13 + combo 15, from my two script runs) | Mechanical? | Where the code to prevent it would go |
|---|---|---|---|
| EV-1: contract present but unparseable YAML (the exit script prints `no contract`; fix cycle 1: the file exists, `return-contract.yaml` line 103 writes unquoted `[1m]` tier aliases inside a flow sequence) | 3 pilot (04, 09, 08) | Yes: the contract is assembled by the LLM instead of a builder | one contract serializer; it must quote or escape model aliases containing `[` or `]` |
| EV-1: `merged-verdict.yaml` absent / nested `adversarial/adversarial/` / `.md` only | 4 pilot (06, 03, 05, 07) | Yes: SKILL step 7 says "copy, never invent" (L346); I confirmed `ls .../shadow06/adversarial` shows `adversarial` and `merged-verdict.md` only | a `merge`-finalizer that writes the file from the sc-adversarial return contract (the extraction functions already exist in `ensemble.py` L633-L697) |
| EV-1: `reviewer-cards/` empty for the lint | 1 pilot (15) + 3 combo (B1-B3) | Yes: cards exist as `reviewer-1.md`..`reviewer-3.md` but the lint counts only `reviewer-<N>-card.(yaml\|yml\|md)` (`panel_lint.py` L188). `ls` of `.../comboB-r1/reviewer-cards/` and `.../shadow15/reviewer-cards/` confirms the names. Across all 59 recorded `reviewer-cards/` dirs, 51 use the `-card` name and only 2 use `reviewer-N.md` | a card-writer helper that owns the file name |
| Parity: card header `model:` is a harness alias, not the pin | 4 pilot (04, 05, 09, 08) | Yes: SKILL step 2 (L341) now says copy `reviewers[N].model` verbatim; the test `test_shadow_steps_pin_the_header_model...` (`test_shadow_skill_contract.py` L221) is named for it and the first fix is in the skill text, so it pins the TEXT, not the behaviour (test body not read [UNVERIFIED]) | header writer reading `panel/resolution.json` |
| Parity: legacy rotation model written as free text (`'claude-gw-tier1b[1m] (sonnet launch)'`), neither a model id nor a class name | A1, A2 (combos) | Yes: the exit script's check is `classes.get(m, str(m).lower())` must be in the known classes (`reflect_shadow_exit.py` L163-L171) | the contract serializer writing the class name |
| Parity: legacy rotation keys missing | 2 pilot (15, 07) + C2 | Yes: contract lacks `reviewer_personas`/`reviewer_models` | the contract serializer |
| Parity: a card header lacks `persona:`/`model_class:`/`model:` | A3 | Yes | header writer |
| Recorded `panel_parity: true` but recomputed false | 2 pilot (05, 07) + A1, A2, A3, C2 = 6 of 28 | Yes: the aggregator already recomputes parity in code (`recompute_parity` L117-L177); the LLM then records a boolean that code distrusts | compute-and-record in code; drop the LLM-written boolean |
| L2: top-level keys outside the frozen list | pilot 13 (`zero_drop_flag`), 07 (`zero_drop_flag`, `memory_status`, `notes`); combos C2, D1, E2, E3 (`reviewer_briefs_materialized`), C3 (`reviewer_briefs_materialized`, `run_finished`, `run_started`) | Yes. **7 of 28 counted runs** (2 pilot + 5 combo) leaked new keys: RE-DERIVED from the two script outputs; the "7 of 28" figure is now [CODE-VERIFIED by execution]. Of the 7, the five combo runs carry `reviewer_briefs_materialized`, a key the skill's own ref instructs (section 3.3): a skill defect, not an orchestrator one. Invented keys: `zero_drop_flag`, `memory_status`, `notes`, `run_started`, `run_finished` (3 runs: 13, 07, C3) | contract serializer with the allowlist, plus fixing SKILL.md 9.1/9.2 and the two constants for `reviewer_briefs_materialized` |
| Count: 13 of 20 | - | Not a defect: needs more runs | - |
| Compliance mean 0.704 (pilot) / 0.867 (combos) | - | Partly: format drift of the findings block heading/fence (slice 11 3.2, fixed in prose by commits 9874d63fb, c2e3347d3); the first-parse metric is a code-computable number (`findings_v2` parser exists) | a block checker that records the rate itself |
| Quality failures | none in the exit script | Judgment: not measured by this exit (SKILL.md L1317 falsifier and the never-run pilot design would) | - |

The exit script as a whole measures LLM-orchestrator file-layout and copy discipline, not review quality. In the pilot (13 runs) and combo (15 runs) evidence I found no exit-gate failure that is a review-content failure.

### 6.3 Gate-design defects in the exit script itself
- `reflect_shadow_exit.py` L313: `if (s_rate or 0.0) > (l_rate or 0.0)`. An empty legacy baseline (`l_rate is None`) is treated as 0.0, so any shadow EV-1 failure fails the exit; reproduced by my second run (`legacy baseline 0/0 = n/a` and `EV-1 ... shadow 3/15 = 0.200`, failure line `EV-1 failure rate is higher than the legacy baseline`). [CODE-VERIFIED by Read and execution]
- Same run: `verdict replay against the legacy baseline (0 runs): new degraded reasons 29`: with no baseline every degraded shadow run is "new" [CODE-VERIFIED by execution]; docstring of the replay script (slice 11 2.6) says unpaired degraded reasons count as new.
- The exit docstring (L21-L22) states the matched legacy contract passed to the lint is the run's own contract, so lint L7 parity is "trivially equal" and the parity that matters is recomputed. OK, intentional.
- Corpus bias carried by the 13: every pilot and combo run is a forced `--tier 2` on a mostly parsed-sparse input (slice 11 3.1, [UNVERIFIED by me: I did not recount `tier_decision.yaml`]), so the exit says nothing about tier selection.

### 6.4 EV-1 for each engine (open item b, second half)
- Skill engine: EV-1 is a prompt rule (SKILL L714) the orchestrator must check with Glob/Bash; `panel_lint._ev1` is the same rule as code, used only post hoc by the exit script and tests.
- Swarm engine: EV-1 does not apply as written (no `adversarial/merged-verdict.yaml`, no `reviewer-cards/`); its stand-in is `merge_method` set from the count and `adversarial_convergence_score` read from the child's return contract. The `0.75`-vs-`0.80` incident that motivated `contract.py` L309-L326 is the swarm engine's own (comment cites "the incident 0.75").

**Key Takeaways**
- At HEAD the Stage 2 exit fails by count AND by 8 EV-1, 6 parity and 9 lint problems; every one of those problems is a deterministic file/copy defect, so all could be removed by code that writes the files, without touching any reviewer judgment.
- The 7-of-28 key-leak figure is confirmed (2 pilot + 5 combo); five of the seven come from a key the skill itself instructs.
- Two defects sit in the gate: the empty-baseline comparison (L313) and the 1.8.0 freeze applied to a key the skill demands.
- Because the gate measures orchestrator hygiene, passing it (20 clean runs) would not show panel quality; the quality measurement (`pilot-design.md`) was never run (slice 11 section 6).

---

## 7. The two engines side by side (every cell cites the code or skill line read in sections 1-5)

| Property | Engine A: swarm ensemble (`cli/reflect/ensemble.py` behind `superclaude reflect run`) | Engine B: skill panel (SKILL.md Waves 3-5, `--t2-engine legacy\|shadow`) |
|---|---|---|
| Reached by | `ReflectRunner._audit_once` for every production `standard`/`deep` run (`runner.py` L538-L545); sc-tasklist terminal gate (`sc-tasklist-protocol/SKILL.md` L1162) | `/sc:reflect --mode pre\|post` via Skill: sc:workflow Wave 4 (`sc-workflow-protocol/SKILL.md` L89), sc-tasklist Stage 10.5 (`sc-tasklist-protocol/SKILL.md` L1630); `--t2-engine shadow` is named only in SKILL.md, `refs/reviewer-spec.md` and `cli/review/manifest_cmd.py` (Grep of `t2-engine` in `src/superclaude`: 3 files), so no caller passes `shadow`; it is manual |
| Reviewers | External proxy models in `T2Model0N` slots, text in/text out via swarm transports; input = tasklist body + base-ref header only (`ensemble.py` L601-L630) | Read-only `reflect-reviewer` agents with Read/Grep/Glob/search/codegraph tools (agent frontmatter per slice 10 S9.1), briefs with T1 card, grounding hunks, coverage slice (reviewer-spec.md); persona is a brief lens (SKILL L646) |
| Calibration | none (`confidence_calibrated` absent from the contract, section 2.4) | blind `confidence-calibrator` per card, disjoint-class rule (SKILL L416, §11.3) |
| Evidence gate | none (`citations_dropped: 0` constant, `ensemble.py` L817; `evidence_validator_ran` absent) | mandatory `evidence-validator`, drops not downgrades (slice 10 S3) |
| Merge | `/sc:adversarial --compare ... --suspect-source ...` run as a `ClaudeProcess` child; keeps only score, report path, status (`ensemble.py` L514-L598) | `Skill sc-adversarial-protocol` Mode A, EV-1 disk check (SKILL L691-L714) |
| Deviation classes | all zero, `regression_present: False` by construction (L779-L785, L820-L823) | 4-class taxonomy decided from evidence (SKILL §10, L1042-L1202) |
| Contract | `contract_version 1.0`, 32 keys, 10 outside the frozen lists, 89 of 110 stable names absent (section 2.4) | 1.8.0, 110 stable + 27 telemetry names (L724-L989), written by the orchestrator |
| Diversity evidence | from SERVED worker `model_id`s (`_diversity.py` L8-L36); `insufficient` vocabulary | from the REQUESTED rotation/pin (`identity_source: requested-pinned`, slice 11 3.3); `full\|degraded` vocabulary |
| Executor exclusion | none (section 4.2) | rule in SKILL L648-L658, in `review panel resolve --hard-exclude-class` for shadow (L340) |
| Verdict/exit | `derive_verdict` -> 0/10/11/2 (`runner.py` L573-L580); HALTED and `--fix` loop dormant (section 4.2) | no exit code of its own; a consumer must read the contract; the wrapper's verdict map can be replayed offline (`scripts/reflect_verdict_replay.py` L50, L83) |
| Isolation | `--isolate-reviewers` snapshot covers only the two `ClaudeProcess` children (`ensemble.py` L496-L504 comment) | L1 read-only agent allowlist + L4 brief rule (SKILL L305) |
| Resilience | bounded T1 fallback ladder (`fallback.py`) | F1/F2/F3 adversarial fallback ladder (SKILL L353-L359, slice 10 S3) |
| Failure mode seen | convergence incident 0.75 (contract.py L309-L311); the `--fix` path has no remediation producer | orchestrator layout/copy drift: 8/13 EV-1, 6/13 parity, 7/28 key leaks (section 6) |
| Panel kernel (`cli/review`: resolve, manifest, cluster, verify-citations, findings-v2) | not used (Grep, section 4.1) | used only by shadow steps (L340-L349) |

---

## 8. Resolution of the four open items

### (a) What must stay byte-identical
Evidence-backed list (each item is something another file or a test reads by value):
1. **Contract 1.8.0 field lists**: SKILL.md 9.1 YAML block (header L724 to the version sentence at L895) and 9.2 telemetry block (ending L989; the `telemetry:` sub-block L969-L989); copies in `panel_lint.STABLE_FIELDS_1_8_0` (110 names, L33-L144) and `TELEMETRY_FIELDS` (27 names, L146-L174), tied together by `test_pinned_field_lists_match_skill_md` (`test_panel_contract_lint.py` L97). Binding reason: the 9.3 consumer map (L995-L1009) names fields by value for sc-troubleshoot, `superclaude sprint run`, sc-task, sc:roadmap, sc:tasklist, sc-workflow, task-builder, Wave 7 and CI; "removal or rename is a breaking change requiring a major bump" (L1011, L1021). Additions are minor and consumers must read-and-ignore (L1020, L1038).
2. **`merge_method` legal values** exactly `{adversarial, single-reviewer-fallback}`: SKILL L837 (EV-2), `panel_lint.LEGAL_MERGE_METHODS` L184 with assertion L3, and the literal `"single-reviewer-fallback"` read by `contract.py` L295.
3. **The verdict map**: `derive_verdict` signature and order, the 19 fields it reads (section 1.4), the 7 strict-bool names (`contract.py` L47-L57), the sets at L31-L38, the 0.80 constant (L321), exit codes 0/10/11/2 (`models.py` L44-L49), pinned by `tests/cli/reflect/test_verdict_mapping.py`, which holds exactly 36 test functions (section 1.6).
4. **The four deviation keys** `authorized, necessary, drift, regression` in `deviation_count_by_class` (`contract.py` L40; also read by `classify_fix` L385-L420 and Wave 7 condition 4, SKILL L1540).
5. **Reviewer brief structure and findings-block grammar**: exactly three brief sections (`test_the_brief_template_has_exactly_three_sections`, `test_shadow_skill_contract.py` L146) and the findings-v2 limits (slice 01 4.1: anchor/quote 12..200, claim <= 300, refs/citations <= 8) [limits CODE-VERIFIED by slice 01, not re-read by me].
6. **Artifact layout read by EV-1**: `adversarial/merged-verdict.yaml`, `reviewer-cards/reviewer-<N>-card.*`, `audit.log` row `F2|F3` (`panel_lint.py` L188-L189, L271-L298). 51 of 59 recorded `reviewer-cards/` dirs follow the `-card` name (my `ls` count).

What is NOT inherently byte-identical (so a unified core may change it):
- The literal `contract_version "1.8.0"`: SKILL.md 9.4 allows a minor bump for additive changes (L1020), `contract.py` accepts any major `1` (L187-L194), and the "no bump" rule is stated by the Stage 2 plan in the lint message (`panel_lint.py` L363-L365) and enforced only by `panel_lint` L1 (L311-L315) and the exit script. A 1.9.0 additive bump (for example adding `reviewer_briefs_materialized`) would need: SKILL 9.1, both lint constants, `test_f3_f4_contract_version` (`test_panel_contract_lint.py` L193), and the wording of L363-L365; it needs no consumer change by the 9.4 rule.
- The byte-identity tests (section 5.6) compare against the current `HEAD`, so they do not freeze anything across commits.
- Engine A's `1.0`, `insufficient`, `reviewer_count`/`subrun_status*` keys are not consumed by anything outside `cli/reflect` that I found (Grep of `derive_verdict|parse_contract|run_tier2_ensemble` in `src/superclaude`: only the reflect package itself); consumers of those 10 keys outside `src` (scripts, tests, other skills) were not searched [UNVERIFIED].

### (b) Which EV-1 / shadow-lint failures are mechanical and could move into code
All of them (section 6.2). Evidence: each failure line is generated by a presence, name, membership or equality check; in 13 pilot + 15 combo runs the exit script reported 0 review-content failures. The deterministic steps are SKILL shadow steps 1, 2, 5 (assembly), 6, 7 (copy), 8, 10 and the contract assembly. Existing code that already implements the check or the extraction, so moving the write path to code reuses it: `panel_lint._ev1`/`lint_panel_contract`, `reflect_shadow_exit.recompute_parity`/`card_headers`, `ensemble.parse_adversarial_contract`/`extract_convergence_score`/`extract_adversarial_status`, the `superclaude review` kernel commands. The 7 of 28 key-leak count is re-derived (2 pilot + 5 combo); 6 of 28 "recorded parity true but recomputed false" is re-derived (2 pilot + 4 combo).

Additional deterministic logic currently in SKILL.md prose that has the same shape (pure functions of contract fields or strings; none was a recorded failure, they are candidates only):
- Wave 7 promotion gate: 9 boolean conditions over contract fields (L1535-L1553) and `gate_evaluation` (L1656-L1668); `classify_fix`-style pure code.
- Convergence routing and null handling (L703-L712).
- Verification-command envelope controls (b)-(e), (i) and the no-mutation denylist (L567-L579): a string validator.
- Executor-class exclusion and rotation (L648-L658) and the calibrator disjoint-set rule (`refs/reflection-rubric.md`, slice 10 S9.3); `review panel resolve --hard-exclude-class --strict-distinct` already implements the resolution side for shadow (L340).
- Memory retention trim (last 20 entries, drop > 90 days, L598-L610); `count_model_aliases` already exists in code (`runner.py`, slice 10 S6.1 L287-L310 [UNVERIFIED by me, not re-read]).
What must stay LLM judgment: reviewing, deviation classification by evidence, blind calibration scoring, the debate, and the evidence-validator's re-read of cited lines (a deterministic `review verify-citations` pre-check exists but "neither drops anything" by design, SKILL L345).

### (c) contract 1.0 vs 1.8.0, 0.75 vs 0.80, what is shared
- `contract_version`: engine A `1.0` (`ensemble.py` L74, L788), skill `1.8.0` (L727). Both pass `derive_verdict` (any major 1, `contract.py` L187-L194); only `panel_lint` L1 distinguishes them. 
- Convergence: skill 0.75 PASS / 0.60 PARTIAL / below FAIL (SKILL L703, L1317); code single degrade below 0.80 with no PARTIAL band (`contract.py` L321; tests L432-L458). A score in [0.75, 0.80) is PASS in the skill and exit 11 in the wrapper.
- Shared code: `contract.parse_contract` and `contract.derive_verdict` are the only functions used by BOTH sides. Engine A calls them in-process (`runner.py` L573-L580, `ensemble.py` L576); the skill engine never calls code at runtime, it is reached by `scripts/reflect_verdict_replay.py` (L50, L83) and `scripts/reflect_shadow_exit.py` (via the replay module) offline on recorded 1.8.0 contracts; `panel_lint.py` additionally imports `_LOAD_BEARING_BOOL_FIELDS` from `contract.py` (L31). `_diversity`, `fallback`, `ensemble` are engine-A-only; `panel_lint` and the exit script are engine-B-only (nothing in `runner.py` imports them). Thus "only `contract.derive_verdict` is shared" is correct, with the nuance that for engine B the sharing is offline replay, not a production call. [CODE-VERIFIED by Grep and reads]

### (d) Which engine a unified core should absorb, and what would be lost
My reading from the evidence above (an analysis for the synthesizer, not a verified fact about the repo):
- Absorbing engine A into engine B (drop the swarm engine) would lose: the only code-enforced fail-closed gate with exit codes 0/10/11/2, atomic write-back and recursion marker (`runner.py`); diversity measured from SERVED model ids instead of pins (the combos showed pins do not guarantee the class: A3 collapse, slice 11 3.3); headless/CI operation without the Claude Code Agent tool (`--transport stub` credit-free lane, `ensemble.py` L123-L174); the bounded fallback ladder; the two snapshot-grounded `ClaudeProcess` children. These do not depend on which reviewers produce findings.
- Absorbing engine B into engine A (make swarm the only engine) would lose: tool-grounded reviewers (swarm sees the tasklist text only), blind calibration, the evidence validator, the four-class deviation taxonomy and the only code path that can set `regression_present` honestly, executor-class exclusion, 89 of the 110 stable contract fields that consumers read, promotion, and the findings-v2 kernel.
- Therefore neither engine is a safe base alone. Evidence-supported composition: B's data model (contract 1.8.0, findings-v2, review kernel) as the shared core; A's runner/verdict/write-back/isolation/transport as the execution shell around it; deterministic steps from section 6.2 moved into code; the 0.75/0.80 threshold and the diversity/vendor/`merge_method` vocabulary decided once (section 5.4 lists the six conflicts). One precondition from section 4.2: the swarm contract has no producer for `remediation_*` or deviation fields, so `--fix` only becomes live if the shared core supplies them.

**Key Takeaways**
- (a) The immovable set is: consumer-read field names (9.3), the `merge_method` set, the verdict map and its 36 tests, the four deviation keys, the brief/findings-block grammar and the EV-1 layout; the literal "1.8.0" and "no new key" are a Stage-2 convention with a documented minor-bump path.
- (b) All observed Stage 2 exit failures are mechanical; the code that checks them already exists and the extraction helpers exist; only the write path is prose.
- (c) Shared code is `contract.py` only; thresholds, vocabularies and versions diverge in six places.
- (d) Neither engine can be dropped without losing a capability the other lacks; the composition above is the evidence-supported direction, and the 20-run Stage 2 exit would not measure quality either way.

---

## Gaps and Questions

Each item names what I searched or ran. Tags: [UNVERIFIED] = no corresponding code or no re-derivation by me; [CODE-CONTRADICTED] = code shows otherwise (also listed under Stale Documentation Found).

1. [CODE-CONTRADICTED] `sc-tasklist-protocol/SKILL.md` L1141, L1152, L1165 and `task-builder/SKILL.md` L2247 claim the wrapper runs an executor-disjoint ensemble / resolves to the exclusion skill; code applies no exclusion (section 4.2). Open question for the owner: is the intended Stage-3+ design that the wrapper switches to engine B, or that engine A gains exclusion?
2. [UNVERIFIED] Content of the swarm lens output template `src/superclaude/cli/swarm/lenses/templates/reflect-review-output.md` (path from `reflect_review.py` L28-L30); only the lens prompt text (L39-L52) was read.
3. [UNVERIFIED] Whether anything outside `src/superclaude` (scripts, other skills, CI) reads the 10 engine-A-only keys or `contract_version 1.0`; searched only `src/superclaude` for the function names.
4. [UNVERIFIED] Behaviour (not text) of `test_shadow_steps_pin_the_header_model_the_verdict_file_and_the_first_pass_metric` (`test_shadow_skill_contract.py` L221) and of `test_pinned_field_lists_match_skill_md`: I read the function names and the file's first 104 lines only. The claim "pins text, not behaviour" for L221 is an inference from its name and slice 11.
5. [UNVERIFIED] Items inherited from slice 11 and not re-derived here: `cluster_agreement` is 1.0 by definition without a blocking cluster (`cluster.py:50`); 28 of 30 runs parsed-sparse and all forced `--tier 2`; card-write corruption 3 times; self-report unreliability; the combo experiment's own figures (FINDINGS.md/results.md); the 5 vs 7 reviewer-agent calls in E1. I re-derived only what the exit script prints.
6. [UNVERIFIED] `runner.py` L120-L440 and L620-L686 (write-back, sidecar, preflight, alias count) were not re-read; claims about them come from slice 10 S6.1 and are marked as such. `commands.py` was read only around the option definitions and by Grep; `config.py` L1-L235 not read; `fallback.py` read L1-L110 plus a symbol Grep, not the controller body (L411-L594).
7. [UNVERIFIED] SKILL.md ranges outside my assignment and outside slice 10 were not read: L1-L83, L90-L304 (except quoted lines), L354-L507, L622-L644 (except L644-L659), L660-L689, L730-L832, L842-L871, L990-L1046, L1204-L1292, L1709-L1739, L1850-L2033. Claims about L416, L631, L635, L646-L660 and §11.3 come from slice 10 S3 unless a line above says I re-read it (I re-read L644-L659, L690-L714, L833-L841, L960-L1039).
8. [UNVERIFIED] Whether `reviewer_briefs_materialized` was ever listed in a SKILL.md section I did not read: Grep over `src/superclaude` for the name hit only `refs/reviewer-spec.md` (L51, L57, L78) outside `.dev` and `.claude`; the lint constants do not contain it. So the gap is real at the repository level, but `.claude/` copies and installed `~/.claude/skills` were not compared.
9. [UNVERIFIED] Why EV-1 jumped from legacy 3/39 to shadow 8/13 (new child layout vs orchestrator drift): slice 11 O-4 lists it open; my `ls` shows the nested/`.md` layouts but I did not open the `sc-adversarial-protocol` child skill to see where it writes. Search tried: `ls` of `shadow06/adversarial`.
10. [UNVERIFIED] The 28-run denominator: it is 13 (default runs root) + 15 (combo root) = 28 only if no run is in both roots; the two runs-root directories are distinct and the combos were deliberately kept out of `.dev/reflect/` (slice 11 D-8). I did not diff the two lists.
11. Question: which of 0.75 and 0.80 is intended? Evidence for 0.80: the code comment names an incident at 0.75 (`contract.py` L309-L311) and tests pin it. Evidence for 0.75: SKILL L703, L1317. No decision record was searched for outside the files read.
12. Question: should `reviewer_briefs_materialized` be added to SKILL.md 9.2 and the lint constants (a doc-only fix), or removed from `refs/reviewer-spec.md`? Five of 15 combo runs fail the lint because of it.
14. [CODE-CONTRADICTED, fix cycle 1] The "no contract" EV-1 failures of pilot runs 04, 08, 09 are NOT a missing file: the `return-contract.yaml` exists in all three and fails `yaml.safe_load` at line 103 (`reviewer_models: [claude-gw-tier1b[1m], ...]`). Slice 11 L95 and L97 carry the wrong wording (see Stale Documentation Found). Open for the core: a contract or card writer must quote or escape model aliases containing `[` or `]`. Searches run: `ls -l` and `yaml.safe_load` on the three files, `sed -n` on `scripts/reflect_shadow_exit.py:74-79, 224, 242-243` and `contract.py:65-82`.
13. Negative evidence: no import of `superclaude.cli.review` in `src/superclaude/cli/reflect/` (Grep above); no `--t2-engine` option in `commands.py` (Grep: option names listed in section 4); no `remediation_task_path`/`remediation_plan_path` key in `build_reflect_contract` (read L787-L835); no reader of `merged-verdict.yaml` in `contract.py`, `runner.py`, `ensemble.py` (Grep).

---

## Stale Documentation Found

| Where | What it says | What the code shows | Tag |
|---|---|---|---|
| `src/superclaude/cli/reflect/__init__.py` L3-L4, L9-L14 | wrapper launches `/sc:reflect --mode post` as a `claude --print` subprocess "so Tier 2 fans out"; five modules listed | production Tier 2 is the in-process swarm (`runner.py` L538-L545); `ensemble`, `fallback`, `_diversity`, `panel_lint` unlisted | **[STALE DOC]** [CODE-CONTRADICTED] |
| `sc-tasklist-protocol/SKILL.md` L1141, L1152, L1165 (and `templates/phase-template.md` L156-L182 same block) | wrapper "spawns an executor-disjoint reflect ensemble"; sources the exclusion class from `executor_model_class` | no executor handling in the swarm path; `executor_model` only reaches the Tier-1 prompt (`runner.py` L480-L481); Grep of `swarm/` = 0 matches | **[STALE DOC]** [CODE-CONTRADICTED] |
| `task-builder/SKILL.md` L2247 | POST subprocess "MUST resolve to OUR `sc-reflect-protocol` skill (the canonical executor-class-exclusion model)" | production wrapper does not run the skill for `standard`/`deep` (`runner.py` L538-L545) | **[STALE DOC]** [CODE-CONTRADICTED] |
| `runner.py` L457-L459 comment; `commands.py` L236-L239 | "--no-promote is the hard default; dropped only on --promote" vs Click default `--promote` True | CLI default is promote; function default `promote=False` (`config.py` L253) | **[STALE DOC]** comment [CODE-CONTRADICTED] |
| Slice 11 L95 and L97 (carried into this file's s3 and s6 and into research/07 E1-F8) | pilot EV-1 failures: "no `return-contract.yaml`", "no contract file" (3 runs: 04, 08, 09) | the file exists in all three (5,648 / 5,707 / 5,637 bytes); it does not parse: `yaml.safe_load` raises `YAMLError` at line 103 `reviewer_models: [claude-gw-tier1b[1m], ...]`; `scripts/reflect_shadow_exit.py:74-79, 224, 242-243` print `no contract` for an unparseable file; `contract.py:65-82` also returns None, so production would route BLOCKED `contract-missing` (`contract.py:174`) | [CODE-CONTRADICTED] |
| `contract.py` L403 docstring | invariant at "SKILL.md:754" | invariant sits at SKILL.md L1155-L1159 (section 10.6) | **[STALE DOC]** line cite |
| SKILL.md L839, L1481 | single vendor is "warn-only in v1.0" / "Continue; WARN" | `contract.py` L287-L288 DEGRADES (exit 11) unless `--allow-single-vendor` | [CODE-CONTRADICTED] (skill vs wrapper) |
| SKILL.md L703 vs `contract.py` L321 | PASS from 0.75 | DEGRADED below 0.80 | [CODE-CONTRADICTED] (skill vs wrapper) |
| SKILL.md L838, L1480 | `t2_model_class_diversity: full \| degraded` | engine A emits `insufficient` (`_diversity.py` L15) | [CODE-CONTRADICTED] |
| `refs/reviewer-spec.md` L78 vs SKILL.md 9.1/9.2 and `panel_lint.py` L33-L174 | contract emits `reviewer_briefs_materialized` | key is in neither list; the lint fails runs that follow the ref | [CODE-CONTRADICTED] (ref vs contract lists) |
| `refs/reflection-rubric.md` L39 vs SKILL §10 / `reflect-reviewer` | classes `{Aligned, Refinement, Drift, Regression}` vs `Authorized expansion / Necessary deviation / Drift / Regression` | two vocabularies for the same four classes | carried from slice 10 S9.3, [UNVERIFIED by me] |
| `.dev/eval-workspaces/shadow-model-combos/PLAN.md` L1, L3, `combos.json` L4 | "designed, NOT run" | 15 runs completed (exit script ran on them) | carried from slice 11 2.1, [UNVERIFIED by me beyond the 15-run count I re-derived] |
| `SKILL.md` L1815 sample | `"skill_version": "1.7.0"` while contract is 1.8.0 and frontmatter `version: 1.0.0` (L4) | three version strings in one skill | **[STALE DOC]** (sample value) |

---

## Summary

The repo has two Tier-2 engines that share only `contract.py`: engine A, the in-process swarm ensemble that `superclaude reflect run` actually uses in production (a `1.0`-shaped, count-derived, tasklist-only convergence-and-diversity gate with dormant deviation, HALTED and `--fix` machinery and no executor exclusion), and engine B, the prose skill panel (contract 1.8.0, grounded reviewers, calibration, evidence validator, deviation taxonomy), reached only by `/sc:reflect` and, in shadow form, only manually. At HEAD the Stage 2 exit prints `OVERALL: FAIL (shadow runs 13 of 20)`; every failure I traced (8 EV-1, 6 parity, 7 of 28 leaked keys, 6 of 28 wrong parity records) is a deterministic file-name, copy or key-set defect whose checking code already exists, so the write path can move from LLM prose into code without touching reviewer judgment. What must stay byte-identical is the consumer-read 1.8.0 field names, the `merge_method` pair, the verdict map with its 36 tests, the four deviation keys and the brief/EV-1 layout; the literal "1.8.0" and the 0.75 vs 0.80, `insufficient` vs `degraded`, warn-only vs DEGRADED-vendor, and `merge_method` semantics need a single decision. Neither engine can absorb the other without losing a capability, so the evidence points to engine B's data model and kernel as the shared core inside engine A's fail-closed execution shell.

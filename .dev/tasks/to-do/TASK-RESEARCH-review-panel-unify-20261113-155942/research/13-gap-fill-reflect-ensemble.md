# Research: Gap fill — reflect code-driven Tier 2 engine (ensemble.py)

**Investigation type:** Architecture Analyst
**Scope:** `src/superclaude/cli/reflect/ensemble.py`, `src/superclaude/cli/reflect/runner.py`, `reflect run` CLI registration, `src/superclaude/cli/reflect/contract.py` (comparison only), `src/superclaude/cli/reflect/panel_lint.py` (field lists), `tests/cli/reflect/test_ensemble_*`, `src/superclaude/skills/sc-tasklist-protocol/SKILL.md` post gate
**Status:** Complete
**Date:** 2026-11-13

---

## 0. Context read first (not evidence)

- `research/07-reflect-merge-contract.md` concludes that under contract 1.8.0 a script merge is illegal for the reflect skill path ("Reflect MUST NOT synthesize its own merge", SKILL.md:837), that `merge_method` has exactly two legal values (`adversarial`, `single-reviewer-fallback`, `panel_lint.LEGAL_MERGE_METHODS`) and that the wrapper `contract.py` accepts any `1.x` and does not validate `merge_method`. Its C1-C16 table is at :395-412. It does not mention `ensemble.py`.
- `research/08-run-recording-telemetry.md:190` and :445 tag "Contract with `telemetry:` block written to `<output>/return-contract.yaml`" (SKILL.md:722) as [UNVERIFIED] because no Python writer was found in that slice. Section 4 of this file answers that.

---

## 1. `src/superclaude/cli/reflect/ensemble.py` (895 lines) [E1]

Read in full (:1-450, :450-895).

### 1.1 Module identity and imports

- Docstring (:1-24) names it "FR-RH2 Tier-2 ensemble driver". It states the Tier-2 path "invokes the swarm run surface (`dispatch_wave1` / `_resolve_run_transport_factory`)" and that each worker slot binds "a distinct external model (`T2Model0N`)". The embedded `phase_c_to_d` block (:13-23) claims `merge_method: "<adversarial>"`, `reviewer_count: "M (succeeded workers); >=2 for pass"`, `consumed_by: [contract.derive_verdict, runner.write_reflect_post]`, `verdict_map_unchanged: {pass: 0, halted: 10, degraded: 11, blocked: 2}`.
- Imports (:38-72): `ClaudeProcess` (pipeline), `parse_contract` (reflect.contract), `ReflectConfig` (reflect.models), and from the **swarm** package: `_resolve_run_transport_factory`, `T1_MODEL_MAX_SLOTS`, `dispatch_wave1`, the `reflect_review` lens, swarm models (`CallerInfo`, `CallerMetadata`, `Manifest`, `PreflightSummary`, `SwarmState`, `WorkerResult`, `WorkerSpec`), `normalize_wave2`, `PreflightResult`, `reduce_wave3`, `emit_done_sentinel`, `Transport`, `TransportEnvError`, `StubTransport`; plus local `_diversity` and `fallback`.
- No import of `panel_lint`, `superclaude.cli.review.*`, or any shadow-kernel module (import block :26-72; cross-check Grep in section 5). [CODE-VERIFIED]

### 1.2 Constants (:74-84)

- `REFLECT_CONTRACT_VERSION = "1.0"` (:74). **This is not the skill-path `contract_version: "1.8.0"`.** `panel_lint` rejects any version other than 1.8.0 (research 07 Q2; re-checked in section 3.2); `contract.py` accepts any `1.x` (section 3.1).
- `REFLECT_REVIEW_RECIPE = "passthrough"` (:80), `SWARM_SUBRUN_DIR = "t2-swarm"` (:81), `ADVERSARIAL_SUBRUN_DIR = "t2-adversarial"` (:82), `CONTRACT_FILENAME = "return-contract.yaml"` (:83).

### 1.3 `AdversarialResult` (:87-117)

Dataclass with `convergence_score: float | None` and defaults `regression_present=False` (:103), `unauthorized_deviation_present=False` (:104), `needs_human_decision=False` (:105), `deviation_count_by_class` all zeros (:106-113), `report_path=None`, `status=None` (:117). Docstring (:92-95): "Today only `convergence_score` + `report_path` are LIVE ... the three deviation booleans + per-class counts default CLEAN until a producer-extension emits them (OQ-PRODUCER)."

### 1.4 Transport resolution (:120-293)

- `_STUB_VENDOR_POOL = ("qwen","deepseek","gpt","mistral")` (:127); `stub_model_id` (:130-133) gives each stub slot a distinct vendor so a stub run is "genuinely PASS-eligible" (:123-126).
- `resolve_t2_transport_factory` (:154-182): `stub` builds one `StubTransport` per slot (:169-174); anything else delegates to swarm `_resolve_run_transport_factory(transport, models=models, env=env, workers_requested=reviewers)` (:176-182). The model pool is the swarm `T2Model0N` env pool (docstring :6-7): **reviewer models are external OpenAI-compatible models, not Claude model classes**. No `executor_model_class` and no phase-file frontmatter read anywhere in ensemble.py (whole-file read). [CODE-VERIFIED]
- `_T1_PROXY_BINDING` (:193-198) is set (not `None`): T1 fallback pool = env `T1Model0N`, `T1ProxyUrl`, `T1ProxyKey`. `resolve_t1_fallback_factory` (:201-293): stub arm gives `gemini/llama/claude` fallback stubs (:225-232); live arm lazily builds `OpenAICompatTransport` per ladder slot via `make_fallback_slot_factory` (:255-293). The gated branch (:237-242) is dead while `_T1_PROXY_BINDING` is set.

### 1.5 `run_tier2_ensemble` (:296-511) — the end-to-end engine

1. Creates `output_dir` and `output_dir/t2-swarm` (:319-323); one deadline from `config.timeout_seconds` (:329-331).
2. `build_preflight_result` (:136-151) fabricates a minimal swarm manifest (`job_id="reflect-ensemble"`, `target_checksum=""`, `CallerMetadata(suspect=True, tier="T2")`); no real swarm preflight runs (:333).
3. Factory (:334-338); worker prompt = `build_worker_prompt(config)` (:339; :601-616) = `reflect-review` lens `system_prompt_fragment` + `user_template` with `{target_content}` = `_load_review_target` (:619-630): a header with `Base ref` and `Tasklist` path plus the **tasklist body only**. An `OSError` silently yields an empty body (:626-629). No git diff is materialised (docstring :607-608, "full git-diff materialization is a rollout refinement (logged follow-up)").
4. **Wave 1** `dispatch_wave1(preflight, transport_for_slot=factory, prompt=..., worker_spec=WorkerSpec(count=reviewers, models=[], timeout_sec=...))` (:340-348): reviewers are in-process transport calls (HTTP to the proxy, or stub), **not subprocesses**.
5. `_stamp_worker_paths` (:349; :838-858) names files `reflect-review-NN-<model-slug>.{final,raw}.md/.meta.json` under `t2-swarm/`.
6. **Wave 2** `normalize_wave2(..., "passthrough", ...)` (:350-358).
7. Optional T1 fallback ladder when `config.tier2_fallback_enabled` (:364-390): `run_fallback_ladder` returns `all_workers` (used downstream) and `metadata` (stored as `t2_fallback`).
8. **Wave 3** `reduce_wave3(mode="normalize+merge", lens="reflect-review", ..., emit_to_disk=True)` (:404-419) writes the **swarm sub-run** `t2-swarm/return-contract.yaml` and a `done` sentinel (:420-421). This is the swarm's own contract, a different schema from the reflect contract.
9. **Adversarial seam** (:423-440): runs only when no score was pre-supplied **and** `len(succeeded_final_paths) >= 2` (:424). Default `run_adversarial_scorer` (:514-561) launches a `ClaudeProcess` with prompt `/sc:adversarial --compare <paths> --suspect-source <paths> --output <dir>` (:582-598), `model=config.model`, `reviewer_profile=True` (:548), `cwd=config.reviewer_grounding_root` (:551). Non-zero exit returns `None` (:554-555). Otherwise it parses `<dir>/adversarial/return-contract.yaml` then `<dir>/return-contract.yaml` (:564-579) and keeps only `convergence_score` (:633-654), `merged_output_path` (:682-697) and `status` (:657-679). A zero-exit child that wrote no parseable contract still yields an `AdversarialResult` with `convergence_score=None, status=None` (:556-561).
10. Deviation locals (:442-471): every field falls back to clean (`False` / `None`) when `adversarial_result is None` (section 2.2 below).
11. `build_reflect_contract(...)` (:473-509), then `_emit_reflect_contract(config.contract_path, contract)` (:510; :886-895): `yaml.safe_dump` to `config.contract_path`; if the contract is `None` (zero successful reviewers) the file is **deleted** (:887-892) so the caller sees "contract-missing".

There is **no calibration step, no evidence-validator / citation check, no clustering and no reviewer-card file** in this engine (whole-file read). `citations_dropped` is the constant `0` (:817). [CODE-VERIFIED]

### 1.6 `build_reflect_contract` (:722-835)

- Returns `None` when 0 workers succeeded (:750-753).
- `reviewers_verified` (:765-767) and `reviewer-shortfall` token (:768-770); comment (:755-764) says the token is deliberately not in the HALT set, so a 2-of-3 shortfall stays PASS-eligible.
- `tier_reached = 2 if reviewer_count >= 2 else 1` (:772).
- **`merge_method = "adversarial" if reviewer_count >= 2 else "single-reviewer-fallback"` (:773)** — see section 2.
- `deviation_count_by_class` defaulted to zeros when `None` (:779-785).
- `"status": "success"` is a literal (:789) regardless of any sub-run status.
- The contract dict (:787-832) and optional `t2_fallback` (:833-834); full key list in section 4.

### Key Takeaways
- [E1] ensemble.py is a self-contained Tier 2 engine built on the **swarm** package (dispatch_wave1 / normalize_wave2 / reduce_wave3) with external OpenAI-compatible reviewer models and a Claude `/sc:adversarial` child as the only "merge" step.
- [E1] It writes contract version `"1.0"`, not the skill-path `"1.8.0"`; it has no calibration, no evidence validation, no reviewer cards and no clustering.
- [E1] Reviewers see only the tasklist text and a base-ref string, not the diff or the code under audit (:619-630), so a UC-2 "post" audit by this engine cannot ground findings in the changed code.

### 1.7 Provenance: this engine is master code, not E1-authored

`git diff --stat origin/master -- src/superclaude/cli/reflect/{ensemble,runner,contract,commands,config,_diversity,fallback}.py` prints nothing (identical to `origin/master` d2d8a2d16, checked 2026-11-13); against the older local `master` (80f361804) only `config.py` differs (6 lines). `git log -- ensemble.py` shows it came from PRs #213 ("close POST-gate false-GREEN via honest ensemble contract"), #214 (FX7 honest-accounting), #220 (Tier-2 fallback ladder) and #329 (codegraph), and the last commit is an ancestor of `master`. The task scheme tags reflect code [E1]; this file keeps [E1] but **this engine predates the E1 shadow-run work and is part of the master baseline that every effort sees**. It is not part of the E1 panel kernel (section 5).

---

## 2. `src/superclaude/cli/reflect/runner.py` (834 lines): the `reflect run` orchestrator [E1]

Read in full (:1-834).

### 2.1 Route selection: when ensemble.py runs

- `ReflectRunner._audit_once` (:513-582): `expected_tier = 2 if config.depth in {"standard", "deep"} else 1` (:538). If `expected_tier == 2 and ClaudeProcess is _ProductionClaudeProcess` (:540) it calls `run_tier2_ensemble(config)` and then sets **`rc = 0` unconditionally** (:544-545). Otherwise it launches the Tier 1 `/sc:reflect --mode post ...` child via `ClaudeProcess` (:549-572).
- So the tasklist post gate (`--depth deep`) **always takes the ensemble route in production**; the `/sc:reflect` skill (and therefore the skill-path Tier 2 panel, §9.1 contract 1.8.0, panel_lint, shadow kernel) is **never invoked** by `superclaude reflect run --depth standard|deep`. Only a `quick` depth would reach `/sc:reflect`, and the CLI cannot produce one (section 2.4). [CODE-VERIFIED]
- The identity check `ClaudeProcess is _ProductionClaudeProcess` (:32, :540) is a test-routing switch: when a test patches `runner.ClaudeProcess`, Tier 2 runs through the mocked single child instead (docstring :521-535). Tests that patch `ClaudeProcess` therefore never exercise ensemble.py through the runner.
- `run_tier2_ensemble`'s return value is discarded (:544). After it, `parse_contract(config.contract_path)` (:573) reads whatever file is on disk; when M==0 the ensemble deleted it (ensemble.py:887-892), so `contract` is `None` and `derive_verdict` routes `contract-missing` (section 3).
- Exceptions raised inside `run_tier2_ensemble` are not caught in `_audit_once` or `run` (the `try` at :748 has only a `finally` at :830-834). Handling is in the CLI layer (section 2.4).
- `config.executor_model` is forwarded only to the Tier 1 prompt (`--executor-model`, :480-481); the ensemble route never reads it (ensemble.py whole-file read). Where `executor_model` comes from is covered in section 2.4.

### 2.2 `reflect run` loop and outputs

- `run` (:643-829): preflight (:648; `preflight` :373-398 checks the `claude` binary, tasklist file, base, head, and the `_phase_incomplete_blocker` :313-370); dry-run/print returns PASS without launching (:655-668); preflight blocker -> BLOCKED + sidecar (:674-692); `--resume` short-circuit on a prior `reflect_post` with same head and verdict pass (:695-719); `--isolate-reviewers` snapshot gate (:729-740); audit/fix loop (:748-793); `fix_iterations`/`fix_converged` (:796-797); reviewer-isolation telemetry (:804-807); `write_reflect_post` (:811-818); a non-`written` write status turns PASS into BLOCKED (:820-822); `write_sidecar` (:823-828); snapshot teardown in `finally` (:830-834).
- Under `--fix`, the loop only applies a remediation on a HALTED verdict that `classify_fix` calls `auto-fixable` and that carries `remediation_task_path` or `remediation_plan_path` (:762-775). **The ensemble contract has no remediation keys** (ensemble.py:787-834), so on the Tier 2 route the `--fix` loop always breaks at "cannot repair" (:774-775) and `--fix` is inert. [CODE-VERIFIED for the key absence; `derive_verdict` mapping of remediation keys read in section 3]
- `ReflectRunner` never writes `return-contract.yaml`; it reads `config.contract_path` (:573, :765). It writes two files: the `reflect_post:` frontmatter block in the tasklist (`write_reflect_post` :136-204) and `<output>/wrapper-result.yaml` (`write_sidecar` :207-268).

### 2.3 `write_reflect_post` (:136-204) and `_build_reflect_post_value` (:103-133)

- Keys written into the tasklist frontmatter, in order (:111-133): `verdict`, `status`, `run_id` (parent dir name of the contract path, :107-109), `tier_reached`, `report`, `contract`, `reason`, `deviations{authorized,necessary,drift,regression}`, `head`, `reviewed_at`, `verification_verified`, `reviewers_verified`, `regression_verified`.
- Replaces only the `reflect_post:` block (:179-194), compare-before-write race guard returns `frontmatter-stale` (:199-201), `frontmatter-missing` when no frontmatter (:166-167), atomic temp + `os.replace` (:81-100, :203).
- `wrapper-result.yaml` keys (:224-256): the same verdict/status/tier/reason/report/contract/deviations plus `child_exit_code`, `env_alias_count`, `write_status`, `fix_iterations`, `fix_converged`, `reviewer_isolation`, `audit_tree_dirty`, `reviewer_grounding_root`, the three `*_verified`, `error_detail`.
- `child_exit_code` on the ensemble route is always 0 (from :545), so the sidecar cannot show that the adversarial child or a reviewer failed.

### Key Takeaways
- [E1] `superclaude reflect run --depth standard|deep` never runs the `/sc:reflect` skill; in production it always runs ensemble.py, so the tasklist post gate's Tier 2 is this engine, not the skill-path panel.
- [E1] The runner trusts whatever `return-contract.yaml` the ensemble left on disk and hard-codes `rc = 0` for the ensemble route (runner.py:545), so child-exit-code routing in `derive_verdict` can never fire for Tier 2.
- [E1] `--fix` is inert on the Tier 2 route because the ensemble contract carries no remediation path.

### 2.4 CLI registration (`commands.py`) and config resolution (`config.py`)

- `reflect run` is `@reflect_group.command()` `run` (`commands.py:222-484`). Options: `TASKLIST` argument (:223-226), `--tmux`, `--print-command`, `--promote/--no-promote` (default promote, :235-240), `--reachability/--no-reachability`, `--timeout`, **`--depth` = `click.Choice(["standard","deep"])` default `standard` (:253-258)**, `--transport` = `openai_compat|stub` default `openai_compat` (:263-268), `--reviewers` default 3 (:269-274), `--output` (:275-279), `--allow-single-vendor`, `--dry-run`, `--resume`, `--fix/--no-fix` default off (:295-300), `--max-fix-iterations` default 2, `--base` (:307-315), `--isolate-reviewers` default off, `--tier2-fallback/--no-tier2-fallback` default on (:326-335). [CODE-VERIFIED]
- Because the CLI rejects `quick` (:255) and `resolve_config` floors `quick` to `standard` (`config.py:318-319`), `expected_tier` in `runner._audit_once` is always 2 from the CLI. **The Tier 1 `/sc:reflect` child branch (`runner.py:546-572`) is unreachable from `superclaude reflect run` in production**; it runs only when a test patches `runner.ClaudeProcess`. [CODE-VERIFIED]
- Reviewer model: `model = ANTHROPIC_MODEL or "opus"` (`commands.py:365`, `_DEFAULT_MODEL = "opus"` :37) is the Claude model of the `/sc:adversarial` child (ensemble.py:541). The reviewers themselves are the `T2Model0N` proxy pool (live) or the stub pool.
- **`executor_model_class` is read from the tasklist frontmatter** in `config.py`: `_FRONTMATTER_EXECUTOR_MODEL_KEY = "executor_model_class"` (:53), env `EXECUTOR_MODEL_CLASS` first (:56, :351-354), stored as `config.executor_model` (:376). It is consumed only by the Tier 1 prompt (`runner.py:480-481`), which the CLI never reaches, so **on the production Tier 2 route `executor_model_class` has no effect**: no reviewer-vs-executor class separation is applied by ensemble.py. [CODE-VERIFIED] The frontmatter read is of the `TASKLIST` argument (for the tasklist post gate this is the phase file), via `extract_frontmatter` (`config.py:304-306`).
- `reviewers` clamp: `1` stays 1 (negative witness), otherwise `max(2, min(4, n))` (`config.py:334-335`). Stub transport forces fallback off (`config.py:340`).
- Output dir: `--output` or `<task-dir>/reflect/post/<head[:12]>/` (`config.py:357-363`); refuses `.claude/{skills,agents,commands}` (:364-368). `ReflectConfig.contract_path` = `output_dir / "return-contract.yaml"` (`models.py:120-122`).
- Exit codes: `Verdict.exit_code` pass 0 / halted 10 / degraded 11 / blocked 2 (`models.py:39-49`); `run` exits with it (`commands.py:470, :484`) and writes a `.reflect-exitcode` sentinel (:474-475, :505-510). A `ValueError` from `resolve_config` exits 2 with a `config-error` sidecar when `--output` was given (:389-428). Any exception from `ReflectRunner.run` (including from `run_tier2_ensemble`, e.g. a `TransportEnvError` for a missing `T2Model0N` pool) writes a `runner-error` BLOCKED sidecar and **re-raises** (:442-469), so the process exits with Python's uncaught-exception code 1, not 2. [CODE-VERIFIED for the re-raise; exit code 1 is standard Python behaviour, not checked by a run]

### Key Takeaways (2.4)
- [E1] Production `superclaude reflect run` is Tier 2 only (depth `standard|deep`), so ensemble.py is the sole engine behind the CLI.
- [E1] `executor_model_class` is read from the phase-file frontmatter (`config.py:53, :351-354`) but is dead on the Tier 2 route; reviewer heterogeneity comes from the external `T2Model0N` pool, not from Claude model classes.
- [E1] An ensemble crash exits 1 (re-raised) rather than the documented blocked code 2, with a `runner-error` sidecar; a gate that tests only for exit codes 0/10/11/2 sees an unmapped code.

---

## 3. `contract.py` (420 lines) vs what ensemble.py writes [E1]

Read in full (:1-420).

### 3.1 Reader side

- `parse_contract` (:65-82): missing / unparseable / non-mapping -> `None`; unknown top-level keys are tolerated ("NFR-8 read-and-ignore", :69-70). So the 11 extra keys ensemble.py writes (section 4) never fail the wrapper.
- `_make_result` (:104-135) reads `status`, `tier_reached`, `report_path`, `deviation_count_by_class`, `remediation_task_path`, `remediation_plan_path`, and **`verification_verified`, `reviewers_verified`, `regression_verified` with default `False`** (:132-134). ensemble.py writes all three (ensemble.py:814-816). It does **not** read `adversarial_subrun_status` here.
- `derive_verdict` (:138-260), first match wins: BLOCKED on rc 124 (:161-164), rc != 0 (:169-172), contract `None` -> `contract-missing` (:173-177), missing version (:179-186), major != "1" (:187-194; ensemble's `"1.0"` passes), non-list `degraded_components` (:196-206), non-bool load-bearing booleans (:210-222; set at :47-57). Then `_degraded_reason` (:225-239), `_halted_reason` (:242-246), PASS iff `status == "success"` and `tier_reached == expected_tier` (:249-252), else HALTED `tier-mismatch` (:255-260).
- `_degraded_reason` (:263-358): trigger 1-5 halt-set components `{"auggie","env-aliases","evidence-validator"}` (:31-33, :274-275); 6 `degraded-tier1` (:278-279); 7 model-class diversity != full (:282-284); 8 single vendor (:287-288); 9 `adversarial_unavailable is True` (:291-292); **10 `merge_method == "single-reviewer-fallback"` (:295-296)**; **11 `tier_reached == 2` and convergence `None` -> `null-convergence` (:299-300)**; **11a `adversarial_subrun_status in ("partial","failed")` (:306-307)**; **11b convergence < 0.80 or non-finite or unparseable -> `low-convergence` (:317-326)**; 12 `verification_ran is False` unless the skip reason is exempt; `no-verification-stage` stays exempt even under `--promote` (:329-345, comment :334-336 names the ensemble); 13 `citations_dropped > 0` (:348-352); 14 `input_drift_detected is True` (:355-356).
- `_halted_reason` (:361-382): `status` failed/partial, `regression_present`, `unauthorized_deviation_present`, `needs_human_decision`, `user_decision_required` (`is True` each), `deviation_count_by_class.regression > 0`, `.drift > 0`.

### 3.2 How each ensemble.py value meets those triggers

| Ensemble value (line) | Trigger it can reach | Effect |
|---|---|---|
| `contract_version: "1.0"` (:74, :788) | major check (:187-194) | passes the wrapper; would fail `panel_lint` L1 (`panel_lint.py:311-315`) |
| `status: "success"` literal (:789) | `_halted_reason` status (:365-368), PASS (:249) | status-failed / status-partial can **never** fire for this engine |
| `tier_reached` = 2 iff >=2 succeeded (:772) | trigger 6 (:278-279) | 1 reviewer -> DEGRADED `degraded-tier1` |
| `t2_model_class_diversity` distinct model ids >= 2 (`_diversity.py:8-15`) | trigger 7 | DEGRADED if all succeeded reviewers share a model id |
| `t2_vendor_diversity` (`_diversity.py:18-36`) | trigger 8 | DEGRADED on a single vendor unless `--allow-single-vendor` |
| `adversarial_unavailable` = caller kwarg, default `False` (:303, :484); runner passes nothing (`runner.py:544`) | trigger 9 | **never True in production**; a failed adversarial child does not set it |
| `merge_method` (:773) | trigger 10 | only `single-reviewer-fallback` when 1 reviewer, but trigger 6 fires first, so trigger 10 is **unreachable** for ensemble contracts |
| `adversarial_convergence_score` = child score or `None` (:440, :807) | 11 / 11b | child failure or unparseable child contract -> `null-convergence` DEGRADED; score < 0.80 -> `low-convergence` |
| `adversarial_subrun_status` (:793) | 11a | child `partial`/`failed` -> DEGRADED |
| `verification_ran: False`, `verification_skip_reason: "no-verification-stage"` (:808-809) | trigger 12 | exempt (:37, :334-336) -> never degrades |
| `citations_dropped: 0` constant (:817) | trigger 13 | never fires |
| `input_drift_detected: False` constant (:819) | trigger 14 | never fires |
| `regression_present`, `unauthorized_deviation_present`, `needs_human_decision` from seam or `False` (:446-460) | `_halted_reason` | **always `False` with the default scorer** (`run_adversarial_scorer` never sets them, :557-561) |
| `user_decision_required: False` literal (:823) | `_halted_reason` | never fires |
| `deviation_count_by_class` zeros (:779-785; seam never fills it) | `_halted_reason` regression/drift | never fires |
| `degraded_components` = `[]` or `["reviewer-shortfall"]` (:768-770) | triggers 1-5 | `reviewer-shortfall` is not in the halt set -> no effect on verdict |

### Key Takeaways
- [E1] With the production scorer, **no ensemble contract can reach HALTED** (exit 10): every `_halted_reason` input is a literal or a seam default that the score-only scorer never changes. The tasklist post gate on this engine can only PASS, DEGRADE or BLOCK.
- [E1] The verdict therefore depends on reviewer count, model/vendor diversity and the adversarial child's convergence score and status. **Reviewer findings themselves (regressions, drift, unauthorized deviations) never influence the verdict**; reviewers that agree on a regression produce high convergence and a PASS.
- [E1] The wrapper reads `verification_verified`, `reviewers_verified`, `regression_verified` (`contract.py:132-134`) and `adversarial_subrun_status` (`:306`); ensemble.py is the only Python writer of all four (section 4), and they are visibility-only except `adversarial_subrun_status`, which routes trigger 11a.

---

## 4. Who writes `return-contract.yaml` and `reflect_post` in code (closes research 08 :190 / :445) [E1]

### 4.1 Writers found

- **`ensemble._emit_reflect_contract` (ensemble.py:886-895)** writes `<output>/return-contract.yaml` with `yaml.safe_dump(contract, sort_keys=False)`; it deletes the file when the contract is `None` (:887-892). Called once, from `run_tier2_ensemble` (:510). `config.contract_path` is `output_dir / "return-contract.yaml"` (`models.py:120-122`). [CODE-VERIFIED]
- The swarm `reduce_wave3(..., emit_to_disk=True)` (ensemble.py:404-419) writes a **different** `return-contract.yaml` under `<output>/t2-swarm/` (path built at :420). Its schema is swarm's, not reflect's (swarm `reduce.py` not read in this slice; [UNVERIFIED] key list).
- `runner.write_reflect_post` (runner.py:136-204) writes the `reflect_post:` block into the tasklist frontmatter; `runner.write_sidecar` (:207-268) writes `<output>/wrapper-result.yaml`; `commands._write_exit_sentinel` (`commands.py:505-510`) writes `.reflect-exitcode`.
- So research 08's statement (SKILL.md:722 writer is agent-written, "no Python writer of `return-contract.yaml` was found") is **[CODE-CONTRADICTED] in general and [CODE-VERIFIED] for the skill path only**: a Python writer exists, but it writes the **code-driven engine's** contract (version `"1.0"`), not the skill's 1.8.0 contract with a `telemetry:` block. No Python writer of the skill-path 1.8.0 contract was found (ensemble.py writes no `telemetry` key; whole-file read).

### 4.2 Every key ensemble.py writes (`build_reflect_contract`, :787-834)

`contract_version`, `status`, `subrun_status`, `adversarial_subrun_status`, `subrun_status_partial`, `mode`, `tier_reached`, `reviewer_count`, `report_path`, `audit_log_path`, `deviation_count_by_class`, `t2_model_class_diversity`, `t2_vendor_diversity`, `adversarial_unavailable`, `merge_method`, `adversarial_convergence_score`, `verification_ran`, `verification_skip_reason`, `verification_verified`, `reviewers_verified`, `regression_verified`, `citations_dropped`, `citations_dropped_extrapolated`, `input_drift_detected`, `regression_present`, `unauthorized_deviation_present`, `needs_human_decision`, `user_decision_required`, `degraded_components`, `reviewer_isolation`, `audit_tree_dirty`, `reviewer_grounding_root`, plus `t2_fallback` when the fallback ladder ran (:833-834). 33 keys in all (32 fixed + 1 optional).

- Emits `verification_verified` (always `False`, :814), `reviewers_verified` (:815; computed :765-767), `regression_verified` (always `False`, :816), `adversarial_subrun_status` (:793). [CODE-VERIFIED]
- `audit_log_path: None` (:801) — no audit log is produced.

### 4.3 Lint check against `panel_lint` (mechanical, 2026-11-13)

A read-only `uv run python -I` script compared the `build_reflect_contract` key literals with `STABLE_FIELDS_1_8_0` (`panel_lint.py:33-144`, 110 keys) and `TELEMETRY_FIELDS` (:146-174, 27 keys):

- **11 keys are in neither list**: `subrun_status`, `adversarial_subrun_status`, `subrun_status_partial`, `reviewer_count`, `verification_verified`, `reviewers_verified`, `regression_verified`, `reviewer_isolation`, `audit_tree_dirty`, `reviewer_grounding_root`, `t2_fallback`. Each would be an L2 failure (`panel_lint.py:316-321`) and trigger the B bump line (:360-365).
- `contract_version "1.0"` fails L1 (:311-315).
- 89 of the 110 stable 1.8.0 keys are absent (e.g. `reviewer_cards`, `evidence_validator_ran`, `citations_total`, `adversarial_artifacts_dir`, `t2_effective_diversity`, `calibrator_diversity`). Absence is not itself a lint failure, but `_ev1` (run when `wave4`, :347-348) expects `adversarial/merged-verdict.yaml` and `reviewer-cards/` under the output dir; ensemble.py writes `t2-adversarial/` and `t2-swarm/` instead (:81-82), so EV-1 would fail too (per research 07 §2.3; `_ev1` body :246-299 not re-read here).
- `citations_dropped_extrapolated` is in both lists (stable :97 and telemetry :157).
- Conclusion: **an ensemble contract fails `panel_lint` on L1, L2 (x11), B and very likely L6/EV-1.** `panel_lint` is not called on this path (no import in ensemble.py or runner.py), so nothing fails today.

### Key Takeaways
- [E1] ensemble.py is the only Python writer of a reflect `return-contract.yaml`; it writes a 33-key, version-`"1.0"` contract that is a different schema from the skill's 110-key 1.8.0 contract.
- [E1] The four wrapper-read keys absent from the panel_lint lists (`verification_verified`, `reviewers_verified`, `regression_verified`, `adversarial_subrun_status`) are written only by ensemble.py; a unified contract must either add them to the stable list (a bump) or keep a separate code-path contract.
- [E1] Two incompatible "reflect contracts" coexist under the same file name and the same reader (`contract.py`): the skill's 1.8.0 (lint-checked) and the engine's 1.0 (unchecked).

---

## 5. Is this the UC-2 `reflect-post` producer, and what does it share? [E1]

### 5.1 Producer

Yes for the tasklist post gate. The gate runs `superclaude reflect run <phase file> --depth deep ...` (`sc-tasklist-protocol/SKILL.md:1162`); the CLI only allows `standard|deep` (`commands.py:255`); `--depth deep` -> `expected_tier = 2` (`runner.py:538`) -> `run_tier2_ensemble` (`runner.py:540-545`). The `reflect_post:` frontmatter block and `wrapper-result.yaml` are written by `runner.py` from the `derive_verdict` result over ensemble.py's contract. [CODE-VERIFIED]

### 5.2 Sharing (Grep 2026-11-13, `src/`, `tests/`, `scripts/`)

- **Importers of ensemble.py**: only `runner.py:36` in `src/` (plus tests: `test_ensemble_*`, `test_fallback_select.py:3`, `test_contract_fallback_metadata.py:7`, `test_claudeprocess_reflect_children_restricted.py:27`, `tests/swarm/test_coder_tier_env_2026_10.py:142`). `fallback.py:43` and `:319` state it never imports `reflect.ensemble`.
- **Importers of `panel_lint`**: `scripts/reflect_shadow_exit.py:50` and `tests/cli/reflect/test_panel_contract_lint.py:12` only. Neither `ensemble.py` nor `runner.py` imports it.
- **E3 `src/superclaude/cli/review/`** (`card_convert`, `cluster`, `findings`, `findings_v2`, `ledger`, `manifest`, `merge_cmd`, `panel`, `telemetry`, `verify_cmd`, ...): a Grep for `ensemble|run_tier2_ensemble|panel_lint|cli.reflect|cli.swarm` in that directory returns **no matches**, and ensemble.py imports nothing from it (:26-72).
- **Shared code**: `contract.parse_contract` (ensemble.py:39) and the `contract.py` verdict map (also the reader the skill-path contract is meant for, per research 07 §3); `pipeline.process.ClaudeProcess` (also used by the Tier 1 path); the swarm engine (`dispatch_wave1`, `normalize_wave2`, `reduce_wave3`, swarm transports, the `reflect-review` lens at `swarm/lenses/reflect_review.py:33-72`); and the `/sc:adversarial` skill, invoked as a child (ensemble.py:582-598), which the skill path also uses for its Mode A merge (research 07 §1.3).
- The swarm "merge" is a mechanical concatenation, by design: `swarm/merge.py:1-29` allows only verbatim concat in slot order with a `## From {model_label}` header and forbids scoring, ranking, dedup or synthesis ("Scoring, ranking, and adversarial merge live in `/sc:adversarial`", :28).

### 5.3 Verdict on question 5

ensemble.py is a **third, independent merge path**: (1) skill-path Tier 2 (sc-reflect-protocol Mode A debate, 1.8.0 contract, `panel_lint`, E1 shadow kernel/`review cluster`); (2) E3 `superclaude review merge` (deterministic ledger merge); (3) this engine: swarm text fan-out over external models + mechanical concat + a score-only `/sc:adversarial` child, writing contract 1.0. It shares only the `/sc:adversarial` skill (as a black-box child) and `contract.py` (as reader) with path (1), and nothing with path (2).

### Key Takeaways
- [E1] The UC-2 `reflect-post` producer for the tasklist post gate is ensemble.py, not the `/sc:reflect` skill.
- [E1][E3] It shares no code with E3 `cli/review/` and does not use the E1 panel kernel or `panel_lint`; it is a third merge path built on the swarm package.
- [E1] Its only overlap with the skill-path panel is the `/sc:adversarial` child (used score-only) and the `contract.py` verdict map.

---

## 6. The tasklist post gate vs what the engine delivers (`sc-tasklist-protocol/SKILL.md:1141-1184`) [E1]

Read :1140-1184. Each gate claim checked against code:

| Gate text (SKILL.md line) | Status | Code |
|---|---|---|
| "the wrapper spawns an executor-disjoint reflect ensemble internally" (:1141, :1152, :1165, :1170) | **[CODE-CONTRADICTED]** | `executor_model_class` is read (`config.py:53, :351-354`) but used only by the unreachable Tier 1 prompt (`runner.py:480-481`); ensemble.py never reads `config.executor_model` and never excludes a class. Reviewers are the `T2Model0N` pool. |
| `--depth deep` fixed (:1165) | [CODE-VERIFIED] | `commands.py:253-258`; routes to ensemble (`runner.py:538-545`). `deep` and `standard` behave identically in ensemble.py (depth is not read there). |
| "runs the bounded `--fix` audit->apply->re-verify loop" (:1170) | **[CODE-CONTRADICTED]** in effect | the loop exists (`runner.py:748-793`) but needs a HALTED verdict with a remediation path; ensemble contracts never HALT and carry no remediation keys (section 3.2). |
| exit `0` completes; `10`/`11`/`2` fail (:1170, :1176) | [CODE-VERIFIED] for the map (`models.py:39-49`) | a crash exits 1 via re-raise (`commands.py:442-469`), outside the documented set; exit 10 is unreachable for this engine. |
| `REPORT.md` at `<output>/REPORT.md` (:1155, :1171, :1175) | **[CODE-CONTRADICTED]** | no code writes `REPORT.md` (Grep `REPORT\.md` over `cli/reflect` and `cli/swarm`: none). `report_path` is the adversarial `merged_output_path` or `t2-swarm/merged.md` or a worker `final_path` (ensemble.py:866-883). |
| reconcile `return-contract.yaml` at `reflect_post.contract` (:1171) | [CODE-VERIFIED] | `reflect_post.contract` = `config.contract_path` (`runner.py:581`, :117) = `<output>/return-contract.yaml` (`models.py:120-122`), written by ensemble.py:886-895. |
| fail if `adversarial_subrun_status` partial/failed (:1171) | [CODE-VERIFIED], redundant | ensemble.py:793 writes it; `contract.py:306-307` already DEGRADEs. |
| fail if `tier_reached == 2` and convergence present and `< 0.80` (:1171) | [CODE-VERIFIED], redundant | `contract.py:317-326` already DEGRADEs. |
| fail if `deviation_count_by_class.drift/.regression > 0` (:1171) | check is **dead** for this engine | ensemble.py always writes zeros (:779-785; seam never fills it, :557-561). |
| "raw contract `status` stays `success` by design" (:1171) | [CODE-VERIFIED] | literal at ensemble.py:789. |
| "Reflect ran with executor-disjoint reviewers" (AC :1177) | **[CODE-CONTRADICTED]** | as row 1. |
| "Report includes the per-task verdict matrix" (AC :1178) | **[CODE-CONTRADICTED]** | no `per_task_verdicts` key or matrix in ensemble.py (whole file; Grep shows `per_task_verdicts` only in `panel_lint.py:124`). |

### Key Takeaways
- [E1] Three of five gate acceptance criteria (REPORT.md, executor-disjoint reviewers, per-task verdict matrix) are not produced by the engine the gate calls; whether a gate run "passes" them depends on the executing agent's judgement, not on code.
- [E1] The gate's extra contract checks duplicate wrapper triggers 11a/11b and add a deviation-count check that can never fire on this engine.

---

## 7. Tests `tests/cli/reflect/test_ensemble_*` (2036 lines) [E1]

Run on 2026-11-13: `uv run pytest tests/cli/reflect/ -k ensemble -q -p no:cacheprovider` -> **58 passed, 295 deselected in 1.01s** (selection also picks up `test_fallback_select.py` and `test_no_nesting_guard.py` by name).

Read: `test_ensemble_stub_integration.py` (:1-641, full), `test_ensemble_unit.py` (:160-628), `test_ensemble_fallback_engage.py` (:1-237, full); `test_ensemble_fallback_stub.py` by test names only (:167-524).

### 7.1 What they pin

- **Score injection everywhere**: every integration test passes `adversarial_score_fn=_const_score` returning `AdversarialResult(convergence_score=0.86, ...)` (`test_ensemble_stub_integration.py:40-60`, :108-122; `test_ensemble_fallback_engage.py:37-59`). The production `run_adversarial_scorer` never runs in an end-to-end ensemble test; it is unit-tested with a stubbed `ClaudeProcess` that returns 0 (`test_ensemble_unit.py:469-527`).
- Positive witness I1: `tier_reached == 2`, `merge_method != "single-reviewer-fallback"`, `reviewer_count >= 2`, diversity full, convergence not None, `adversarial_unavailable is False`, `status == "success"`, PASS/0 (`test_ensemble_stub_integration.py:141-171`).
- Negative witnesses: 1 reviewer -> `single-reviewer-fallback`, non-PASS (I2 :174-196); 2-of-3 distinct -> PASS (I3 :199-221); 2-of-3 duplicate model -> DEGRADED 11 (I4 :224-248); M==1 -> DEGRADED 11 (I5 :251-277); M==0 -> contract absent, BLOCKED 2 `contract-missing` (I6 :280-303).
- Shape: I7 checks only 10 keys and `contract_version` major `1` "not an exact string" (:306-336); I8 pins the two contract paths (`<out>/return-contract.yaml` vs `<out>/t2-swarm/return-contract.yaml`) (:339-367); I9 pins `t2-swarm/done.json` (:370-384); I10 pins the lens brief prefix (:387-417).
- Routing: I11 pins production `_audit_once` -> `run_tier2_ensemble` (:420-444); I11b builds a `depth="quick"` config with `dataclasses.replace` to reach the Tier 1 branch, noting `resolve_config` floors quick (:447-471) — confirming Tier 1 is test-only.
- Deviation routing: I12 injects `regression_present=True` through the seam and gets HALTED/10 `regression` (:474-531); the partial-substatus test gets DEGRADED/11 `degraded-subrun-partial` (:534-591); the 2-of-3 quorum test keeps PASS (:594-641). **Both HALT and partial come only from injected seam values; no production code path sets them except `status` from a real child.**
- Unit: `test_u6` pins exit codes and trigger order in `derive_verdict` by source-text index (`test_ensemble_unit.py:183-206`); `test_u8` pins `swarm.merge` <= 30 code lines and no score/rank/dedup/filter/judge tokens (:209-221); `test_u10` pins the nested `return_contract:` parse (:267-296); `test_u11` pins clean defaults when no seam kwargs (:299-339); `test_r2f2` pins `verification_ran False` + `no-verification-stage` exempt (:342-363); `test_r2f3` pins `user_decision_required False` even with `needs_human_decision True` (:366-397); FX7 tests pin `reviewer-shortfall`, `reviewers_verified`, always-False `verification_verified`/`regression_verified` (:561-628).
- Fallback: ladder engages and certifies Tier 2 with a fallback, PASS (`test_ensemble_fallback_engage.py:115-150`); healthy pool keeps `reviewer_count == 3` and swarm status success (:153-201); gate off -> DEGRADED `degraded-tier1` (:204-237).

### 7.2 What is NOT pinned

- No test drives `run_tier2_ensemble` with an adversarial scorer that **fails** (returns `None`) and checks the resulting contract (`merge_method`, `adversarial_unavailable`, verdict). Grep for `null-convergence` in the ensemble tests finds only comments (`test_ensemble_stub_integration.py:484`, `test_ensemble_unit.py:274, :294`); `test_claudeprocess_reflect_children_restricted.py:64` uses rc=1 only to check the child's restricted profile.
- No test asserts `contract_version` equals any exact value, or that the contract passes `panel_lint`.
- No test checks that `executor_model_class` affects the reviewer pool.
- No test asserts the CLI exit code when `run_tier2_ensemble` raises.

### Key Takeaways
- [E1] The ensemble's PASS/DEGRADE/BLOCK/HALT witnesses are real for the swarm half but **injected for the merge half**; a unified panel can reuse these as fixtures for reviewer-count and diversity routing, not as evidence that the merge step yields deviation signal.
- [E1] The missing "adversarial child failed" end-to-end test is exactly the case QA flagged (`merge_method: adversarial` written after a failed adversarial step).

---

## 8. Answers to questions 1-3 [E1]

### Q1. End-to-end flow of `superclaude reflect run`

1. CLI `run` (`commands.py:222-484`) -> `resolve_config` (`config.py:244-396`): base from `--base` > frontmatter `start_commit` > merge-base; depth floor (`:318-319`); transport/reviewers (`:328-340`); `executor_model_class` from env then frontmatter (`:350-355`); output dir (`:357-368`).
2. `ReflectRunner.run` (`runner.py:643-829`): preflight (`:373-398`), dry-run, resume, optional snapshot (`:729-740`), audit loop.
3. `_audit_once` (`runner.py:513-582`): Tier 2 in production -> `run_tier2_ensemble(config)` (`:540-545`).
4. Reviewers: **in-process swarm transport calls**, not subprocesses: `dispatch_wave1` (ensemble.py:343-348) over `T2Model0N` OpenAI-compatible proxy models (`resolve_t2_transport_factory`, :154-182) or stubs; optional T1 fallback ladder (:364-390). Model classes are whatever the env pool names; vendor families are inferred from the model id (`_diversity.py:39-61`). `executor_model_class` is read (`config.py:53, :351-354`) but **not used** on this route.
5. Calibration: **none** (no calibration code in ensemble.py; whole-file read).
6. Merge: `normalize_wave2` passthrough (:350-358) -> `reduce_wave3` mechanical concat into `t2-swarm/merged.md` (:404-419; `swarm/merge.py:1-29`) -> `/sc:adversarial` Mode A child via `ClaudeProcess` (:514-561), used only for `convergence_score`, `status`, `merged_output_path`.
7. Evidence validation: **none**; `citations_dropped: 0` constant (:817), no evidence-validator token ever emitted.
8. Contract: `build_reflect_contract` (:722-835) -> `_emit_reflect_contract` (:886-895) -> `parse_contract` + `derive_verdict` (`runner.py:573-580`) -> `write_reflect_post` + `write_sidecar` (`runner.py:811-828`) -> exit code (`commands.py:470-484`).

### Q2. `merge_method`

- Set at **ensemble.py:773**: `"adversarial" if reviewer_count >= 2 else "single-reviewer-fallback"`, where `reviewer_count = len(succeeded)` (:750-751). It depends on **nothing but the count of successful reviewers**: not on whether the adversarial seam ran, succeeded or returned a score. [CODE-VERIFIED; QA claim confirmed]
- Adversarial step **failed** (non-zero exit -> `None`, :554-555): with >=2 reviewers the contract still says `merge_method: adversarial`, `adversarial_unavailable: False` (runner never passes `True`, `runner.py:544`), `adversarial_convergence_score: None`, `adversarial_subrun_status: None`, `report_path` falls back to `t2-swarm/merged.md` (:876-879). Verdict: DEGRADED `null-convergence` (`contract.py:299-300`), exit 11. So the label is false but the verdict is not PASS.
- Adversarial step **skipped**: (a) a pre-supplied `adversarial_convergence_score` (:424; only tests/advanced callers, the runner never passes one) — `merge_method: adversarial` with no child run and `adversarial_subrun_status: None`; verdict follows the supplied score. (b) fewer than 2 `final_path`s while `reviewer_count >= 2` (`succeeded_final_paths` also requires a non-empty `final_path`, :391-395, whereas `reviewer_count` does not, :750-751) — `merge_method: adversarial`, convergence `None` -> DEGRADED `null-convergence`. In normal runs `_stamp_worker_paths` sets `final_path` for every worker (:838-858), so (b) is a latent edge, not an observed one.
- Adversarial child **exit 0 but no parseable contract**: `AdversarialResult(convergence_score=None, status=None)` (:556-561) -> same as the failed case: `merge_method: adversarial`, DEGRADED `null-convergence`.
- 1 reviewer: `single-reviewer-fallback`, `tier_reached: 1` -> DEGRADED `degraded-tier1` (trigger 6 precedes trigger 10).

### Q3. Default deviation/flag values and "clean when nothing ran"

- `AdversarialResult` defaults (ensemble.py:103-113): `regression_present=False`, `unauthorized_deviation_present=False`, `needs_human_decision=False`, `deviation_count_by_class` zeros.
- Seam-less / failed-seam fallbacks (ensemble.py:446-471): each of the three booleans `False`, `deviation_count_by_class None` -> zeros at :779-785, `adversarial_report_path None`, `adversarial_status None`. Comment :442-445 states the intent ("Clean defaults apply when no seam ran ... OR the child failed").
- `build_reflect_contract` keyword defaults (:726-739) also clean; literals in the dict: `status: "success"` (:789), `mode: "post"` (:797), `audit_log_path: None` (:801), `verification_ran: False` + exempt `no-verification-stage` (:808-809), `verification_verified: False`, `regression_verified: False` (:814, :816), `citations_dropped: 0`, `citations_dropped_extrapolated: 0` (:817-818), `input_drift_detected: False` (:819), `user_decision_required: False` (:823).
- **The production scorer never sets any deviation field** (`run_adversarial_scorer` returns only score, report path, status, :557-561; docstring :527-530 "Only `convergence_score` + `report_path` are populated LIVE").
- What makes a run look clean when nothing ran: every healthy production run (>=2 diverse reviewers, adversarial child exit 0 with convergence >= 0.80 and status not partial/failed) is a **PASS with zero deviations, verification exempt, zero dropped citations**, regardless of what the reviewers wrote. The reviewers had no access to the diff or code (:619-630) and no evidence check ran. `reflect_post.deviations` is all zeros (`runner.py:119-124`), so the tasklist gate's drift/regression check (`SKILL.md:1171`) passes.

### Key Takeaways
- [E1] QA's three claims are confirmed at exact lines: code-written contract (ensemble.py:886-895, :510), count-only `merge_method` (:773), clean defaults (:103-113, :442-471, :779-785).
- [E1] The `merge_method` lie does not by itself produce a false PASS (null-convergence DEGRADEs), but the clean deviation defaults do: a healthy run is PASS with no deviation analysis.

---

## 9. Q6: what a unified Review Panel must keep for this caller, and C1-C16 [E1]

### 9.1 Caller-facing surface to keep unchanged

- **Command line** used by the tasklist gate (`sc-tasklist-protocol/SKILL.md:1162`): `superclaude reflect run <phase file> --depth deep --fix --no-promote --base <sha> --output <dir>`; all options at `commands.py:222-335`.
- **Exit codes**: pass 0 / halted 10 / degraded 11 / blocked 2 (`models.py:39-49`), the `.reflect-exitcode` sentinel (`commands.py:474-475, :505-510`), the recursion marker `SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE` (`runner.py:56`; gate `SKILL.md:1159-1161`).
- **Output paths**: `<output>/return-contract.yaml` (`models.py:120-122`), `<output>/wrapper-result.yaml` (`runner.py:257`), the `reflect_post:` frontmatter block in the phase file (`runner.py:136-204`). The gate also expects `<output>/REPORT.md` (`SKILL.md:1155`), which nothing writes today (section 6).
- **Contract keys the gate reads** (`SKILL.md:1171`): `adversarial_subrun_status`, `tier_reached`, `adversarial_convergence_score`, `deviation_count_by_class.drift/.regression`, plus `reflect_post.verdict` and `reflect_post.contract`.
- **Contract keys the wrapper reads** (`contract.py`): `contract_version` (major 1), `status`, `tier_reached`, `report_path`, `deviation_count_by_class`, `remediation_task_path`, `remediation_plan_path`, `verification_verified`, `reviewers_verified`, `regression_verified` (:113-134), `degraded_components` (list), the seven load-bearing booleans as real `bool` (:47-57), `t2_model_class_diversity`, `t2_vendor_diversity`, `adversarial_unavailable`, `merge_method`, `adversarial_convergence_score`, `adversarial_subrun_status`, `verification_ran`, `verification_skip_reason`, `citations_dropped`, `input_drift_detected`, `regression_present`, `unauthorized_deviation_present`, `needs_human_decision`, `user_decision_required` (:263-382).
- **Routing semantics pinned by tests**: 2-of-3 distinct survivors stays PASS (I3, quorum test); duplicate model DEGRADES (I4); M==1 DEGRADES (I5); M==0 BLOCKED `contract-missing` via an absent contract (I6); `derive_verdict` order pinned by source index (`test_u6`).

### 9.2 Reflect constraints C1-C16 (research 07 :395-412) touched by this caller

| # | Touches? | How |
|---|---|---|
| C1 (§9.1 byte-identical, 1.8.0) | Indirectly | ensemble writes `"1.0"` (:74); C1 guards only SKILL.md text, so the engine is outside it. A unified contract must decide whether this caller moves to 1.8.0 (lint-clean) or keeps 1.0. |
| C2 (no top-level key outside 110+27) | **Yes, violated if applied** | 11 extra keys (section 4.3). |
| C3 (`merge_method` legal values; new value = bump) | Yes | uses the two legal values, but `adversarial` here means "score-only child", not the Mode A merge EV-1 assumes; an honest new value (e.g. a script merge) would need a bump and wrapper changes. |
| C4 (EV-1 verdict file + cards) | **Yes, violated if applied** | no `adversarial/merged-verdict.yaml`, no `reviewer-cards/` (uses `t2-adversarial/`, `t2-swarm/`, :81-82). |
| C5 (legacy authoritative; no UC-2 panel before Stage 5) | **Yes, blocking** | this caller is UC-2. Routing it to the unified panel is a UC-2 panel, which C5 defers to Stage 5. Today's UC-2 Tier 2 is already a non-skill engine, so C5 as written ("legacy default and authoritative") does not describe this path. |
| C6, C7, C8, C14 (SKILL.md text / brief / shadow needles / installed paths) | No | the engine does not use the skill brief or SKILL.md. |
| C9 (`reflect-reviewer` read-only agent in rotation tables) | No (bypassed) | reviewers are tool-less proxy endpoints, not `reflect-reviewer`. |
| C10 (zero new degraded reasons; 20 clean shadow runs) | Yes | the engine's reasons (`null-convergence`, `low-convergence`, `degraded-subrun-partial`, `degraded-tier1`, ...) come from the shared `contract.py`; the Stage 2 replay compares only the skill path, so no evidence run exists for this caller. |
| C11 (no Fable/tier0, max 3 reviewers) | **Yes, conflict** | `--reviewers` clamps to 2..4 (`config.py:335`), default 3; 4 exceeds C11's max. Model choice is the `T2Model0N` env pool, not panel templates. |
| C12 (only `anthropic-only` launches; `gateway` launch `{}`) | **Yes, conflict** | the engine launches gateway/proxy models directly (`openai_compat`, `resolve_t2_transport_factory` :176-182); applying C12 to this caller would remove its reviewer pool. |
| C13 (src SoT) | No | process rule. |
| C15 (reviewers read-only, no live exec) | Satisfied | reviewers have no tools; the adversarial child runs `reviewer_profile=True` (:548). |
| C16 (consumers route on `merge_method` first) | Yes, contradicted | for ensemble contracts, trigger 10 is unreachable (trigger 6 fires first, section 3.2); `merge_method` never routes. |

### Key Takeaways
- [E1] A unified panel serving the tasklist post gate must keep the CLI line, exit codes 0/10/11/2, the three output files and the ~30 contract keys read by `contract.py` and the gate.
- [E1][E3] C5, C11 and C12 conflict directly with this caller (UC-2, up to 4 reviewers, gateway-launched); C2/C4 would fail if the skill-path lint were applied. The conflict log needs one row per item.

---

## 10. Q7: defects and risks, graded by impact on a blocking gate [E1]

| # | Defect | Evidence | Impact on the blocking post gate | Grade |
|---|---|---|---|---|
| D1 | Reviewer findings never reach the verdict: the scorer is score-only, deviation fields are clean defaults | ensemble.py:442-471, :557-561, :103-113; HALT unreachable (section 3.2) | A phase with a real regression that all reviewers agree on gets PASS/exit 0; the gate cannot HALT on a found deviation. `--fix` is inert. | **Critical** (false GREEN on the primary purpose) |
| D2 | Reviewers see only the tasklist text and base ref, not the diff or code; no evidence validation | ensemble.py:619-630, :817; lens asks for file:line evidence (`reflect_review.py:39-46`) | Any file:line in reviewer output is unverifiable; the audit is not grounded in the phase's changes. | **Critical** |
| D3 | `executor_model_class` ignored on the Tier 2 route | `config.py:351-354`, `runner.py:480-481`, ensemble.py (no read) | The gate's "executor-disjoint reviewers" AC (`SKILL.md:1177`) is unmet; same-family self-review is possible if the pool contains the executor's family. | High |
| D4 | `merge_method: adversarial` written when the adversarial step failed, was skipped or returned no contract; `adversarial_unavailable` never set | ensemble.py:773, :424, :554-555, :805; `runner.py:544` | Verdict still DEGRADES via `null-convergence`, so no false PASS today; the contract misreports what happened, and any consumer that trusts `merge_method`/`adversarial_unavailable` (C16) is misled. | Medium |
| D5 | Literal `status: "success"` regardless of sub-runs | ensemble.py:789 | `_halted_reason` status triggers can never fire; failure is visible only via 11a/null-convergence. Documented "by design" at `SKILL.md:1171`. | Medium |
| D6 | Ensemble exceptions exit 1 (re-raise), outside the 0/10/11/2 map | `commands.py:442-469` | A gate that maps only documented codes may treat 1 as an unknown; it is still non-zero, so it does not pass. | Low-Medium |
| D7 | `rc = 0` hard-coded after the ensemble | `runner.py:544-545` | `child_rc` triggers (timeout 124, child-crash) cannot fire for Tier 2; `child_exit_code` in the sidecar is always 0. | Medium (observability) |
| D8 | Contract `"1.0"` with 11 non-1.8.0 keys; not linted | ensemble.py:74, section 4.3 | Two incompatible schemas share one file name and reader; a future reader that enforces 1.8.0 breaks this caller. | Medium (migration risk) |
| D9 | `REPORT.md` and per-task verdict matrix never produced | section 6 | Gate ACs (:1175, :1178) depend on agent judgement; code cannot satisfy them. | Medium |
| D10 | `reviewer-shortfall` is non-gating by design | ensemble.py:755-770 | 2-of-3 PASS is intended (FR-RH2.9), pinned by tests. | Low (documented choice) |
| D11 | Empty review target on an unreadable tasklist | ensemble.py:626-629 | Reviewers review an empty body; mitigated by preflight `tasklist-missing` (`runner.py:389-390`). | Low |

### Key Takeaways
- [E1] D1 and D2 make the code-driven post gate a **reviewer-agreement and diversity check, not a deviation audit**; they are the highest-impact findings for any gate that blocks a phase.
- [E1] D4 (QA's `merge_method` claim) is real but currently masked by the null-convergence trigger; it becomes a false-PASS risk if the convergence handling changes.

---

## Gaps and Questions

1. [UNVERIFIED] Swarm `reduce_wave3` key list for `t2-swarm/return-contract.yaml` (only `workers_succeeded`, `status`, `workers_failed` seen via tests `test_ensemble_stub_integration.py:366`, `test_ensemble_fallback_engage.py:194-195`); `swarm/reduce.py` not read beyond Grep.
2. [UNVERIFIED] Whether the live `T2Model0N` pool ever contains the executor's model family (would make D3 bite); env contents not inspected.
3. [UNVERIFIED] What `/sc:adversarial` Mode A actually returns as `convergence_score` when fed free-form review texts (score semantics for this caller); no live run was made (forbidden by the task). No recorded `t2-adversarial/` run directory was looked for.
4. [UNVERIFIED] `panel_lint._ev1` body (:246-299) not re-read; the EV-1 failure for an ensemble output dir relies on research 07 §2.3 plus the directory names (ensemble.py:81-82).
5. [CODE-CONTRADICTED] research 08 :190/:445 "no Python writer of `return-contract.yaml`": ensemble.py:886-895 writes one (for the code-driven engine, version 1.0); no Python writer of the skill-path 1.8.0 contract was found.
6. [CODE-CONTRADICTED] `sc-tasklist-protocol/SKILL.md:1141, :1152, :1165, :1170, :1177` "the wrapper spawns an executor-disjoint reflect ensemble" / "sources the reviewer-exclusion class from `executor_model_class`": read but unused on the Tier 2 route.
7. [CODE-CONTRADICTED] `SKILL.md:1155, :1171, :1175` `REPORT.md` at the output dir: no writer.
8. [CODE-CONTRADICTED] `SKILL.md:1178` per-task verdict matrix: not produced.
9. [CODE-CONTRADICTED] `SKILL.md:1170` "runs the bounded `--fix` audit->apply->re-verify loop": loop code exists but cannot trigger on ensemble contracts.
10. [CODE-CONTRADICTED] ensemble.py docstring `phase_c_to_d` (:13-23) implies `merge_method: adversarial` reflects an adversarial verdict; code sets it from reviewer count alone (:773).
11. [CODE-CONTRADICTED] research 07 C5 "legacy default and authoritative" describes the skill path only; the UC-2 Tier 2 that the tasklist gate uses is this non-skill engine.
12. Question: should the unified panel replace ensemble.py for the post gate (needs a UC-2 Stage 5 decision under C5, a reviewer pool that satisfies C12, and grounding in the diff), or should ensemble.py be fixed in place (real deviation extraction, honest `merge_method`/`adversarial_unavailable`) as an interim?
13. Question: should the four wrapper-read keys absent from the 1.8.0 lists (`verification_verified`, `reviewers_verified`, `regression_verified`, `adversarial_subrun_status`) become stable keys in the unified contract (a bump), given only this engine writes them?
14. Question: `--reviewers` up to 4 (`config.py:335`) vs C11 max 3 — which wins in a shared core?

## Stale Documentation Found

- **[STALE DOC]** `sc-tasklist-protocol/SKILL.md:1141, :1152, :1165, :1170, :1177`: executor-disjoint ensemble via `executor_model_class` — not applied on the Tier 2 route (`config.py:351-354` read, `runner.py:480-481` only consumer, unreachable).
- **[STALE DOC]** `sc-tasklist-protocol/SKILL.md:1155, :1171, :1175, :1178`: `REPORT.md` and per-task verdict matrix — not produced by the engine.
- **[STALE DOC]** `sc-tasklist-protocol/SKILL.md:1170`: bounded `--fix` loop — inert for ensemble contracts.
- **[STALE DOC]** ensemble.py module docstring `phase_c_to_d` (:13-23): `merge_method: "<adversarial>"` reads as an adversarial outcome; it is a reviewer-count label.
- **[STALE DOC]** `research/08-run-recording-telemetry.md:190, :445` and SKILL.md:722 context: "no Python writer of `return-contract.yaml`" — true for the skill path only.
- **[STALE DOC]** `commands.py:257` help text "Reflect depth passthrough (POST never runs quick)" is accurate, but `runner.py:546-548` comment "The reflect Tier-1 grounded pass ... is unchanged" implies a reachable Tier 1 production path; it is reachable only in tests (`test_ensemble_stub_integration.py:447-471`).

## Summary

`superclaude reflect run`, which the blocking sc:tasklist per-phase post gate calls with `--depth deep`, always runs the code-driven Tier 2 engine in `ensemble.py` in production (the CLI allows only `standard|deep`, `commands.py:255`; routing `runner.py:538-545`); the `/sc:reflect` skill, its 1.8.0 contract, `panel_lint` and the E1 shadow kernel are never involved. The engine is master-baseline code (identical to `origin/master`), built on the swarm package: tool-less external `T2Model0N` reviewers that see only the tasklist text, a mechanical concat, and a score-only `/sc:adversarial` child; it has no calibration, no evidence validation and no executor-class exclusion, and it writes its own version-`"1.0"` contract (ensemble.py:886-895) whose 11 extra keys and missing EV-1 artifacts would fail `panel_lint`. QA's claims are confirmed: `merge_method` comes from the reviewer count alone (ensemble.py:773) and stays `adversarial` when the adversarial step fails, and deviation flags default to clean (ensemble.py:103-113, :442-471, :779-785). The worst effect is not the `merge_method` label (a failed child still DEGRADES via `null-convergence`) but that no production contract can HALT: reviewer findings never reach the verdict, so the gate is a reviewer-agreement and diversity check rather than a deviation audit. It is a third, independent merge path sharing only the `/sc:adversarial` child and the `contract.py` verdict map with the skill path, and nothing with E3's `cli/review/`; a unified panel serving this caller must keep the CLI line, exit codes, output files and the ~30 contract keys read downstream, and must resolve conflicts with C5, C11 and C12.

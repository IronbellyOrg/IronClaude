# Research Notes: Implement the reflect Tier-2 fallback model ladder

**Date:** 2026-07-06
**Scenario:** A (Explicit — a revised, reflect-reviewed component design drives the work breakdown)
**Depth Tier:** Deep (8 source files + ~9 test files across the `reflect` + `swarm` subsystems)
**Track Count:** 1 (one cohesive implementation deliverable)

**Driving design:** `.dev/brainstorms/20260706-035624-reflect-t2-fallback-ladder/design.md` (status: revised-post-reflect; closed findings F1–F7)
**Source requirements:** `.dev/brainstorms/20260706-035624-reflect-t2-fallback-ladder/merged-requirements.md`
**Target root:** `src/superclaude/`
**Integration branch:** `origin/master`; `start_commit` (merge-base) = `d8f84f71a397ed7358b83f48d46691f82aaec51d`

---

## EXISTING_FILES

Authoritative work breakdown is the design's §10 change map, §9 test surface, §12 rollout. Files (all under `src/superclaude/`), with the current symbols the design targets:

**reflect subsystem** (`src/superclaude/cli/reflect/`)
- `ensemble.py` — driver. `run_tier2_ensemble` (currently lines ~170–341) is the insertion seam; the controller call goes AFTER `normalize_wave2` (~L225) and BEFORE `succeeded_final_paths` (~L226). `build_reflect_contract` is DEFINED HERE (~L552–637), NOT in contract.py — gains additive `t2_fallback: dict | None = None` kwarg. Diversity helpers `compute_model_class_diversity` (~L640) and `compute_vendor_diversity` (~L650) live here (circular-import consideration for the new fallback.py).
- `contract.py` — verdict map. `derive_verdict` + `_degraded_reason` (first-match chain, ~L265–293). **No change** (verdict semantics unchanged). `_LOAD_BEARING_BOOL_FIELDS` must NOT gain a member.
- `models.py` — `ReflectConfig` dataclass (~L56–113). Gains 3 defaulted fields: `tier2_fallback_enabled: bool = True`, `tier2_fallback_ladder: tuple = ("T1Model01","T1Model02")`, `tier2_fallback_max_attempts: int = 2` (appended after existing defaulted fields to respect dataclass field-ordering).
- `commands.py` — `--no-tier2-fallback` CLI flag wiring.
- `fallback.py` — **NEW**. Pure helpers (`classify_outcomes`, `evaluate_quorum`, `plan_next_attempt`, `select_contributing_set`, `make_fallback_slot_factory`) + the one impure `run_fallback_ladder`.

**swarm subsystem** (`src/superclaude/cli/swarm/`)
- `config.py` — `SwarmConfig` (has `_collect_t2_models`, `T2_MODEL_ENV_PREFIX`, `T2_MODEL_MAX_SLOTS`). Add `T1_MODEL_ENV_PREFIX`, `T1_MODEL_MAX_SLOTS`, `t1_models: tuple = ()` field, and generalize `_collect_t2_models`→`_collect_models(env_map, prefix, max_slots)` called twice.
- `transports/openai_compat.py` — **F3 file (design added it to the change map)**. `read_env` (~L159–202) is hard-coded to T2 (imports only `T2_MODEL_ENV_PREFIX`/`T2_PROXY_*` at ~L98–103). Generalize to `read_env_for_pool(model_prefix, max_slots, proxy_url_env, proxy_key_env)`; keep a thin T2-bound `read_env()` wrapper so existing callers/tests stay valid.
- `commands.py` — `_resolve_run_transport_factory` (the `_factory(slot_index)` maps `pool[slot_index % len(pool)]`, ~L691–692). Parameterize on env prefix/pool (or add `_resolve_fallback_transport`); `ModelPoolTooSmallError` guard at ~L687–688.
- `dispatch.py` — `dispatch_wave1` builds tasks `0..workers_requested-1` (~L464–471) and passes local `slot_index` to `transport_for_slot(slot_index)` (~L453–459). This is the root of F1: a one-worker fallback dispatch always passes `slot_index==0`.
- `models.py` — **No change** (`WorkerStatus = Literal["success","timeout","parse_error","proxy_error"]`; no new status, no new `WorkerResult` field).

## PATTERNS_AND_CONVENTIONS

- **Additive-kwarg precedent:** `build_reflect_contract` already threads `reviewer_isolation` / `audit_tree_dirty` / `reviewer_grounding_root` as defaulted kwargs (ensemble.py). `t2_fallback` follows the identical shape — default `None`, emitted verbatim under a top-level key; existing call sites/tests stay valid.
- **Dataclass field-ordering:** `ReflectConfig` appends new defaulted fields AFTER existing defaulted fields (models.py comment "appended AFTER all existing non-default fields"). Same for `SwarmConfig.t1_models = ()`.
- **First-match verdict chain (F6):** `_degraded_reason` returns the FIRST trigger slug (contract.py:265–293): T6 `degraded-tier1` fires before T10 `single-reviewer-fallback`. Tests must assert `degraded-tier1` as the reason, `merge_method` only as a contract field.
- **Collector generalization pattern:** `_collect_t2_models` → `_collect_models(env_map, prefix, max_slots)` called twice avoids T1/T2 copy-paste divergence.
- **Fail-open transport build:** `_resolve_run_transport_factory` raises `TransportEnvError`/`ModelPoolTooSmallError` at build time; controller catches into `terminal_reason: fallback_config_missing` — never a stack trace.
- **No proxy keys in artifacts (AC #12):** resolver binds the proxy key internally, emits only `model_id`. Contract test asserts absence in dumped YAML.

## GAPS_AND_QUESTIONS

- **G1 (needs_human_decision — T1 proxy binding):** Env grounding shows `T1ProxyUrl` + `T1ProxyKey` + `T1Model01`/`T1Model02` all EXIST as distinct env-var NAMES (values not read, per `.aienv`-only-proxy-contract). This SUPERSEDES the design's "same T2 proxy" default (§7.3): a dedicated T1 proxy contract exists in this environment. Recommended binding: `read_env_for_pool(model_prefix="T1Model0", proxy_url_env="T1ProxyUrl", proxy_key_env="T1ProxyKey")`. **This must be a needs_human_decision HALT gate** before real fallback dispatch (rollout step 5) is wired — the user explicitly asked for it, and the memory `feedback_aienv_only_proxy_contract` constrains proxy work to `~/.aienv` values only. Stub-transport work (rollout steps 1–4) does NOT depend on this and proceeds.
- **G2 (circular import):** `fallback.py` reuses `compute_*_diversity` from `ensemble.py` while `ensemble.py` imports `run_fallback_ladder` from `fallback.py`. Resolve by moving the two diversity helpers to a neutral module OR function-local import. Design §10 flags option (a) preferred.
- **G3 (wall-clock, F4 — decided):** shared run deadline from `config.timeout_seconds` captured at top of `run_tier2_ensemble`, threaded as `deadline_monotonic`, clamps each fallback `timeout_sec`. Verify `runner.py` in-process path has no outer ClaudeProcess timeout to conflict.

## RECOMMENDED_OUTPUTS

Research files (evidence, file:line) to be produced by parallel researchers:
- `research/01-reflect-seam-inventory.md` — reflect/ symbols + exact seam lines (ensemble/contract/models/commands)
- `research/02-swarm-transport-slot-inventory.md` — swarm/ config/commands/transports/dispatch/models; the F1 slot_index seam + F3 read_env seam
- `research/03-patterns-conventions.md` — additive-kwarg precedent, dataclass ordering, collector generalization, first-match chain
- `research/04-test-surface.md` — existing tests/cli/reflect + tests/cli/swarm patterns, fixtures, stubs; where the 9 new test files land
- `research/05-template-and-examples.md` — MDTM template 02 + prior TASK-RF examples

## SUGGESTED_PHASES

Grounded in design §12 rollout (this is the phase skeleton the builder should encode as granular items):
1. **Phase 1 — reflect/fallback.py pure helpers + unit tests** (classify, evaluate_quorum, plan_next_attempt incl. F1 slot-name test, select_contributing_set, make_fallback_slot_factory).
2. **Phase 2 — additive `build_reflect_contract(t2_fallback=…)` in ensemble.py + contract-metadata & verdict-unchanged regression tests** (incl. F6 first-match assertion).
3. **Phase 3 — wire controller into ensemble.py behind `tier2_fallback_enabled`, capture run deadline (F4), stub transport first + stub-integration test** (F2 stamp seam; replay §8 incident + counter-case).
4. **Phase 4 — swarm T1 slot resolution:** config.py collector + `read_env_for_pool` (F3) + commands.py resolver parameterization + swarm config/transport tests.
5. **Phase 5 — needs_human_decision HALT (G1): confirm T1 proxy binding vs `~/.aienv`** → then real fallback dispatch behind the flag.
6. **Phase 6 — `--no-tier2-fallback` flag + docs.**
7. **Phase 7 — verification:** `uv run pytest tests/ -k "reflect or swarm"`, `make sync-dev`, `make verify-sync`, ruff format-check on changed files only.

## TEMPLATE_NOTES

- **Template 02 (complex):** discovery already done (design), but build → test → verify phases with a conditional human-decision gate justify 02.
- **QA_INTENSITY:** standard. **QA_GATE_REQUIREMENTS:** PER_PHASE (implementation + tests interleaved).
- **TESTING_REQUIREMENTS:** UNIT + INTEGRATION (pure-helper unit tests + stub-integration). Test paths: `tests/cli/reflect/` and `tests/cli/swarm/` (F7 — NOT `tests/reflect/`).
- **VALIDATION_REQUIREMENTS:** `uv run pytest -k "reflect or swarm"`; `make sync-dev` + `make verify-sync`; `uv run ruff format --check` on changed files only (per memory `make lint ≠ CI ruff format`).
- **Frontmatter:** `start_commit: d8f84f71a397ed7358b83f48d46691f82aaec51d`; `executor_model_class:` = the executing model's class alias.
- **CLAUDE.md invariants to encode:** edit `src/superclaude/` then `make sync-dev`; never stage `.claude/` mirrors; PRs `--repo IronbellyOrg/IronClaude`. (These are Python CLI files, not synced skills — `.claude/` staging rule still applies to the repo generally.)

## AMBIGUITIES_FOR_USER

- **G1 T1 proxy binding** is the one genuine decision point — but it is a *deliberate* needs_human_decision HALT the user explicitly requested, not an unresolved research gap. Env grounding gives the recommended answer (use `T1ProxyUrl`/`T1ProxyKey`); the HALT confirms it against `~/.aienv` before real dispatch is wired. All other design decisions were closed by the reflect pass (F1–F7).

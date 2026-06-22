# Research Notes: FR-RH1 UC-2 Contracted-Sink Reachability & Oracle-Admissibility Gate

**Date:** 2026-06-20
**Scenario:** A (Explicit — the input REPORT.md is an implementation-ready patched requirements amendment)
**Depth Tier:** Deep (multi-surface reflect protocol + Python wrapper + docs + tests + eval fixture)
**Track Count:** 1 (single cohesive feature; wrapper/docs/tests depend on the same stable contract)
**Template:** 02 (complex — spec patch, implementation planning, tests, docs, QA, reflect gates)
**Spec path (PRE reflect gate `--spec`):** `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/.dev/reflect/pre-uc2-reachability-gate-20260620-041729/REPORT.md`

---

## EXISTING_FILES

**Driving artifact:**

- `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/.dev/reflect/pre-uc2-reachability-gate-20260620-041729/REPORT.md` — patched pre-execution report for FR-RH1. It supersedes the original ambiguous design and provides R1–R9 implementation-ready amendments: real-boot-only Regression, telemetry-only `--no-reachability`, spec-absent telemetry-only behavior, contract `1.6.0`, wrapper plumbing, producer eval fixture, UC-2 field-presence rules, bounded cost, and advisory-only semantic fallback.
- `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/.dev/brainstorms/20260620-040444-reflect-uc2-reachability-gate/merged-requirements.md` — underlying merged requirements file. The report says to patch this underlying spec before building/implementing; current lines still contain superseded language such as spec-absent diff-side `unproven` and binding+oracle-mismatch proving Regression.

**Existing related task (do not resume):**

- `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/.dev/tasks/to-do/TASK-RF-uc2-reachability-20260620-025931/` — related but distinct FR-RSR runtime-surface reachability task. It targets `runtime_surface_*` symbol reachability and was built from `.dev/reflect-hardening/issue-1-uc2-reachability/tdd.md`; this FR-RH1 task targets contracted durable sinks and `reachability_*` fields from the patched REPORT. Reuse as prior-art only.

**Primary source targets (source of truth = `src/superclaude/`):**

- `src/superclaude/skills/sc-reflect-protocol/SKILL.md` — stable contract currently declares `contract_version: "1.5.0"`; UC-2 contract block currently has no `reachability_*` fields; Wave 1A evidence chain has Step 5.5 verification triangle but no Step 5.6 contracted-sink reachability gate; `--no-verify` exists but `--no-reachability` does not.
- `src/superclaude/commands/reflect.md` — slash-command flag documentation table currently lists `--no-verify` but no `--no-reachability`; command activation hands off to `sc:reflect-protocol`.
- `src/superclaude/cli/reflect/commands.py` — Click surface for `superclaude reflect run`. Options include `--tmux`, `--print-command`, `--promote/--no-promote`, `--timeout`, `--depth`, `--output`, `--allow-single-vendor`, `--dry-run`, `--resume`, `--fix/--no-fix`, `--max-fix-iterations`, and `--base`; no reachability option exists.
- `src/superclaude/cli/reflect/config.py` — `resolve_config()` builds `ReflectConfig`; no reachability model/config field exists.
- `src/superclaude/cli/reflect/models.py` — `ReflectConfig` dataclass contains wrapper run configuration; no reachability field exists.
- `src/superclaude/cli/reflect/runner.py` — `ReflectRunner._build_prompt()` composes `/sc:reflect --mode post ...`; it currently forwards `--no-promote`, `--diff`, `--tasklist`, optional `--spec`, `--depth`, `--remediate`, optional `--executor-model`, and `--output`; it cannot forward `--no-reachability` yet.
- `docs/guides/reflect-cli-tools-guide.md` — operator guide for `superclaude reflect run`; Key options are parity-tested against Click.
- `tests/cli/reflect/test_docs_cli_parity.py` — executable doc⇆CLI parity guard; adding a Click option requires adding a docs bullet or the test fails.
- `tests/cli/reflect/test_verdict_mapping.py` and fixtures under `tests/cli/reflect/fixtures/` — wrapper contract verdict tests tolerate future minor versions and route `needs_human_decision` / `regression_present`.
- `.dev/eval-workspaces/sc-reflect/` — reflect eval workspace. The patched report requires a producer-level fixture under `.dev/eval-workspaces/sc-reflect/evals/uc2-reachability-unproven-proxy-oracle/` plus `expected.yaml` assertions for contract `1.6.0` and reachability ledger output.

## PATTERNS_AND_CONVENTIONS

- **Source-of-truth discipline:** edit `src/superclaude/` first, then run `make sync-dev` and `make verify-sync`; never stage `.claude/` mirrors except `.claude/settings.json` if explicitly targeted.
- **UV only:** use `uv run pytest ...` and `uv run ruff format --check src/ tests/` for Python validation; never use bare `python -m` or `pip`.
- **Stable contract evolution:** `SKILL.md` §9.4 states minor versions are additive-only. FR-RH1 must bump the stable contract to `1.6.0` because it adds top-level `reachability_*` fields; `1.5.0` must remain D13-only (`coverage_pct_union`, `coverage_degraded`, `unmapped_requirements_union`).
- **Wrapper thinness:** the Python wrapper should expose/forward flags and parse contracts; reflect protocol semantics stay in `sc-reflect-protocol` and not in wrapper verdict logic unless the wrapper test fixtures need forward-compatible field coverage.
- **Doc parity:** `docs/guides/reflect-cli-tools-guide.md` option bullets must match Click flags exactly; `test_docs_cli_parity.py` reads Click from `commands.py`.
- **Telemetry-only disable paths:** `--no-reachability` and spec/tasklist absence must not create reachability Grounding Gaps, must not set `needs_human_decision`, and must not change status solely because reachability did not run.
- **Real-boot proof bar:** only a real-boot verifier observing the contracted sink absent can emit `unreachable` / Regression. Static missing binding, discarded result, oracle mismatch, unresolved sink identity, unavailable boot, or absent authoritative spec/tasklist can emit only `unproven` or non-blocking telemetry per the patched R1/R3/R9 rules.
- **Explicit annotation v1 trigger:** blocking-gate eligibility in v1 requires explicit `durable_sink:` or `@sink`; semantic fallback is advisory-only until precision is proven.

## GAPS_AND_QUESTIONS

- Exact insertion points and current line anchors in `SKILL.md` for Step 5.6, §9.1 contract fields, §9.3 consumer map, §10.4 Regression, §10.6 Grounding Gaps, §17.6 Testability Map, and §17.7 Kill List need researcher re-anchoring before task items cite `file:line`.
- Exact Click option placement, config/dataclass plumbing shape, and tests to add for `--no-reachability` need wrapper researcher confirmation.
- Eval workspace schema for producer-level `uc2-reachability-unproven-proxy-oracle` needs inventory from existing eval cases; the report gives desired fixture shape but not the repository's exact eval manifest format.
- The task should patch the merged requirements artifact before implementation so the implementation follows the corrected v1 design, but the durable source-of-truth location for the patched spec may be either the existing `merged-requirements.md` or a companion amendment file. Research should recommend the least destructive path.

## RECOMMENDED_OUTPUTS

- `research/01-report-and-spec-delta.md` — inventory the patched report R1–R9, map each to lines in `REPORT.md`, identify the exact superseded clauses in `merged-requirements.md`, and recommend spec-patch task items.
- `research/02-skill-protocol-anchors.md` — re-anchor `SKILL.md` locations for Step 5.6, contract `1.6.0`, reachability fields, consistency rules, Grounding Gap schema, Regression mapping, cost profile, and semantic fallback text.
- `research/03-wrapper-cli-plumbing.md` — inventory `commands.py`, `config.py`, `models.py`, `runner.py`, wrapper docs, and parity tests for `--no-reachability` plumbing.
- `research/04-eval-and-test-inventory.md` — inventory reflect eval workspace structure and existing tests/fixtures; propose producer fixture and unit/smoke tests for field presence and disable/spec-absent invariants.
- `research/05-template-and-prior-art.md` — read MDTM Template 02 from `src/superclaude/templates/workflow/02_mdtm_template_complex_task.md` plus the related prior FR-RSR task as a shape example while noting scope differences.
- `research/06-slash-command-reflect-source.md` — gap-fill research for `src/superclaude/commands/reflect.md` flag table, argument hint, activation, and sync implications.

## SUGGESTED_PHASES

- **R1 (Doc Cross-Validator / Spec Delta):** Scope: `REPORT.md`, `merged-requirements.md`. Focus: patched R1–R9, superseded original wording, task items needed to patch the driving requirements before code edits. Output: `research/01-report-and-spec-delta.md`. Other researchers cover code anchors, wrapper, evals, and MDTM shape.
- **R2 (File Inventory / Patterns):** Scope: `src/superclaude/skills/sc-reflect-protocol/SKILL.md` and refs. Focus: current contract/version/taxonomy/Step 5.5 anchors and insertion points for FR-RH1 Step 5.6 + stable fields. Output: `research/02-skill-protocol-anchors.md`. Do not cover Python wrapper.
- **R3 (Integration Points):** Scope: `src/superclaude/cli/reflect/{commands.py,config.py,models.py,runner.py}`, `docs/guides/reflect-cli-tools-guide.md`, `tests/cli/reflect/test_docs_cli_parity.py`. Focus: wrapper config field, Click option, prompt forwarding, docs parity, tests. Output: `research/03-wrapper-cli-plumbing.md`. Do not cover skill protocol text.
- **R4 (Test & Verification):** Scope: `.dev/eval-workspaces/sc-reflect/`, `tests/cli/reflect/`, reflect contract fixtures. Focus: producer-level eval fixture shape, field-presence/consistency tests, disable/spec-absent tests, command help/prompt tests. Output: `research/04-eval-and-test-inventory.md`.
- **R5 (Template & Examples):** Scope: `src/superclaude/templates/workflow/02_mdtm_template_complex_task.md`, prior task `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/.dev/tasks/to-do/TASK-RF-uc2-reachability-20260620-025931/TASK-RF-uc2-reachability-20260620-025931.md`. Focus: MDTM rules, final reflect item shape, how to adapt prior-art without carrying FR-RSR-specific obsolete content. Output: `research/05-template-and-prior-art.md`.
- **R6 (Gap-fill / Slash Command Source):** Scope: `src/superclaude/commands/reflect.md`. Focus: current slash-command flag table, `--no-reachability` row insertion, command activation constraints, and sync-dev implications. Output: `research/06-slash-command-reflect-source.md`.

## TEMPLATE_NOTES

- Use Template 02 (complex) because the generated task requires spec patching, skill protocol edits, wrapper Python plumbing, tests/evals, docs parity, sync/verify, and QA gates.
- Use `QA_INTENSITY: full`; this is a reflect hardening change touching stable contract and wrapper behavior.
- Use `QA_GATE_REQUIREMENTS: PER_PHASE` or at minimum phase verification + one final 6+ agent QA gate. The task-builder should embed explicit adversarial QA items and a POST reflect wrapper shell-out item.
- Include `POST_REFLECT_GATE: ENABLED` because the task changes reflect protocol and wrapper behavior.
- Generated task items must be granular: separate items for spec patch, Step 5.6 protocol text, contract field/version changes, wrapper config/model, Click flag, prompt forwarding, docs, producer eval fixture, unit/parity tests, sync/format/test gates, QA, and POST reflect.
- The prior FR-RSR task is useful for task shape and source-of-truth discipline only; do not copy its `runtime_surface_*` semantics into this FR-RH1 `reachability_*` contract.

## AMBIGUITIES_FOR_USER

None blocking. The patched report makes the key product choices explicitly: real-boot-only Regression, telemetry-only disable/spec-absent behavior, contract `1.6.0`, explicit-annotation-only blocking trigger for v1, bounded cost profile. The generated task should surface any implementation-time uncertainty as Open Questions rather than silently changing these choices.

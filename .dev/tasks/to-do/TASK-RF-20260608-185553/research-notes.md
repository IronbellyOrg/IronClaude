# Research Notes: `superclaude reflect run` — thin CLI wrapper for the post-execution reflect gate

**Date:** 2026-06-08
**Scenario:** A (Explicit — detailed merged-requirements spec with FRs, NFRs, architecture, reuse map, file list)
**Depth Tier:** Deep (new CLI subsystem `cli/reflect/` = 6 files + main.py registration + tests + task-builder template branch; reuses ClaudeProcess, sprint tmux/git idioms; consumes reflect contract; touches multiple subsystems)
**Track Count:** 1 (single cohesive feature — implementation, tests, and template branch are tightly coupled and build on each other; not independent work streams)
**Source spec:** `.dev/brainstorms/20260608-182553-reflect-cli-wrapper/merged-requirements.md`

---

## EXISTING_FILES

Reuse anchors (verified to exist during scope discovery):

- `src/superclaude/cli/pipeline/process.py` — **`ClaudeProcess`** (the core reused primitive). Constructor `__init__(... timeout_seconds=6300, output_format="stream-json", env_vars=None ...)`; `start() -> Popen`, `wait() -> int`, `build_env(*, env_vars=...)`, stdin prompt write (`self._process.stdin.write(self.prompt.encode())`), `--model` passthrough, stream-json. FR-1/FR-10/NFR-2.
- `src/superclaude/cli/sprint/tmux.py` (~11KB) — `launch_in_tmux` idiom + sentinel exit-code pattern (§5 `--tmux` opt-in).
- `src/superclaude/cli/sprint/process.py` (~15KB) — `git merge-base` `<BASE>..HEAD` resolution idiom (FR-3).
- `src/superclaude/cli/pipeline/frontmatter.py` (~5.5KB) — frontmatter parse/serialize (FR-6 write-back; cross-check the yamllint-safe dumper).
- `src/superclaude/cli/main.py` — subcommand registration via `main.add_command(...)` (Open Q2).
- `src/superclaude/cli/prd/`, `src/superclaude/cli/roadmap/` — existing Click-subcommand package models for the new `cli/reflect/` package.
- `src/superclaude/cli/eval/claude_process.py` — `HomeIsolation`/`ClaudeProcessAdapter` — **DELIBERATELY NOT REUSED** (FR-10 load-bearing boundary; hermetic mkdtemp HOME strips MCP+aliases).
- `src/superclaude/skills/sc-reflect-protocol/SKILL.md` + `refs/` — reflect skill (single source of truth). Contract spec in `refs/report-template.md` (currently `contract_version: 1.2.0`) and SKILL.md §9/§14. The wrapper CONSUMES this contract.
- `src/superclaude/skills/task-builder/SKILL.md` — Phase-N POST reflect HALT gate + "Reflect Depth (Deterministic TCS)" section + BUILD_REQUEST handling (template integration, Open Q7).
- `tests/cli/prd/`, `tests/cli/eval/` — CliRunner + monkeypatch test models (§8 test surface).
- **TARGET (to create):** `src/superclaude/cli/reflect/{__init__,commands,config,models,runner,contract}.py`; `tests/cli/reflect/`.

## PATTERNS_AND_CONVENTIONS

- UV-only Python ops; SoT discipline: edit `src/superclaude/` → `make sync-dev` → `.claude/` (NFR-6). Skill/template changes are `src/superclaude/skills/...`.
- Click subcommand groups registered in `main.py` like sprint/roadmap/prd (precedent to mirror).
- `ClaudeProcess` is the reuse-first subprocess primitive — wrapper constructs it directly, never reinvents lifecycle/timeout/signal/env (NFR-1/NFR-2).
- Contract-consumer pattern precedent: sprint executor status routing (null convergence → partial → halt), reflect SKILL §8.
- yamllint-safe YAML serialization required for machine-written frontmatter (memory `reference_yamllint_indent_sequences_pyyaml`: SafeDumper subclass overriding `increase_indent`).
- Lint/format gate: `make lint` (ruff check) + CI `ruff format --check` (memory `reference_make_lint_vs_ci_ruff_format`).

## GAPS_AND_QUESTIONS

Researchers must resolve:

1. **Exact current reflect `contract_version`** — spec §10 references "1.3.0→future" and FR-5 says "1.x tolerant"; `report-template.md` shows `1.2.0`. Pin the real value AND the full field catalog the verdict map (§6) + degradation checklist (FR-11) read.
2. **`ClaudeProcess.build_env` actual behavior** — does it copy `os.environ` and pop `CLAUDECODE`/`CLAUDE_CODE_ENTRYPOINT`? FR-10 requires bare-env overlay that preserves HOME/MCP/aliases and pops nested-session vars. Verify what build_env does today vs what FR-10 needs (may need a thin override).
3. **Does `/sc:reflect` accept `--executor-model`, `--depth`, `--diff`, `--tasklist`, `--spec`, `--output`, `--no-promote`, `--tier`?** Confirm against reflect SKILL invocation surface (FR-2/FR-3). Pin depth vocab (quick/standard/deep) and the STOP condition for `--output` under `.claude/{skills,agents,commands}`.
4. **Reflect degradation field semantics (§14)** — which exact field values route to `degraded` (FR-11): `degraded_components` membership set, `tier_reached`, `t2_model_class_diversity`, `t2_vendor_diversity`, `adversarial_*`/`merge_method`, `verification_ran`, `citations_dropped`, `input_drift_detected`. And which are EXPECTED (not halt): `serena_summary_corroboration: unavailable`.
5. **Frontmatter fields present in task-builder tasklists** — `start_commit`, `spec_path`, `EXECUTOR_MODEL_CLASS`/executor model class; and the exact current `reflect_post: PENDING` block + Phase-N HALT item text (for byte-identical default, NFR-3).
6. **Sprint tmux sentinel mechanic** — how `launch_in_tmux` returns an exit code via sentinel file; reusable for `--tmux` (§5).
7. **TCS flooring** — confirm the builder bakes resolved `--depth` (floored at `standard`) + `<BASE>` so the wrapper is passthrough (FR-3 single-TCS-producer, V1 R-6).

## RECOMMENDED_OUTPUTS

Research files (8 researchers, Deep tier, single track):

- `research/01-claudeprocess-primitive.md`
- `research/02-reflect-contract-schema.md`
- `research/03-cli-subcommand-pattern.md`
- `research/04-sprint-tmux-git-base.md`
- `research/05-frontmatter-writeback.md`
- `research/06-taskbuilder-template-integration.md`
- `research/07-test-patterns.md`
- `research/08-reflect-invocation-degradation-semantics.md`

## SUGGESTED_PHASES

- **R01 — `cli/pipeline/process.py` ClaudeProcess (File Inventory + Integration).** Full constructor signature + defaults; `start()`/`wait()`/`build_env()` behavior; stdin prompt delivery; timeout→124; SIGTERM→SIGKILL/process-group; output_format stream-json; argv construction (`--print --verbose --output-format ... --model ...`); what env vars build_env copies/pops. Output: `research/01-claudeprocess-primitive.md`. Other researchers cover: contract (R02), CLI pkg pattern (R03), tmux/git (R04).
- **R02 — Reflect return-contract.yaml field catalog (Data Flow / Integration).** Read `sc-reflect-protocol/refs/report-template.md` + SKILL.md §9/§9.1/§14.5 + `refs/promotion-adapters.md`. Enumerate EVERY contract field with type + meaning, focused on the verdict-map (§6 of spec) + FR-11 degradation inputs. Pin current `contract_version`. Output: `research/02-reflect-contract-schema.md`. Other researchers cover: reflect invocation flags + degrade routing semantics (R08 — distinct: R02 = data shape, R08 = which values mean degraded + flags accepted).
- **R03 — Existing Click subcommand package pattern (Template & Examples).** Deep-read `cli/prd/` and `cli/roadmap/` package layouts: __init__/commands/config/models/runner split, Click group construction, `main.add_command` registration line shape. Map each to the target `cli/reflect/{__init__,commands,config,models,runner,contract}.py`. Output: `research/03-cli-subcommand-pattern.md`. Others cover: ClaudeProcess (R01), tests (R07).
- **R04 — Sprint tmux + git-base idioms (Integration Points).** `cli/sprint/tmux.py` launch_in_tmux + sentinel exit-code file; `cli/sprint/process.py` `git merge-base <integration>` / start_commit resolution. Output: `research/04-sprint-tmux-git-base.md`. Others cover: ClaudeProcess lifecycle (R01).
- **R05 — Frontmatter parse + atomic race-safe write-back (Patterns + Integration).** `cli/pipeline/frontmatter.py` API; yamllint-safe dumper; read-bytes→parse→inject `reflect_post`→serialize→compare-on-disk-bytes→`os.replace()` pattern; body byte-preservation; sidecar `wrapper-result.yaml`. Output: `research/05-frontmatter-writeback.md`. Others cover: which frontmatter FIELDS exist in tasklists (R06 covers the tasklist template side).
- **R06 — Task-builder template integration (Doc Cross-Validator + Patterns).** Current Phase-N POST reflect HALT item text (byte-exact) + `reflect_post: PENDING` block; "Reflect Depth (Deterministic TCS)" section; BUILD_REQUEST field handling for the new opt-in `POST_REFLECT_MODE: wrapper|halt` (default halt). Tag all claims CODE-VERIFIED/CONTRADICTED/UNVERIFIED. Output: `research/06-taskbuilder-template-integration.md`. Others cover: write-back mechanics (R05), reflect invocation (R08).
- **R07 — Test patterns & verification (Test & Verification).** `tests/cli/prd/` + `tests/cli/eval/` CliRunner usage, monkeypatching ClaudeProcess, fixture-contract→verdict assertions, no-nesting guard test approach (NFR-7), pytest markers/fixtures, lint/format gates. Output: `research/07-test-patterns.md`. Others cover: ClaudeProcess internals (R01), contract fixtures shape (R02).
- **R08 — Reflect invocation surface + degradation routing semantics (Integration / Solution).** Which flags `/sc:reflect` accepts (`--mode post`, `--no-promote`, `--diff`, `--tasklist`, `--spec`, `--depth`, `--executor-model`, `--output`, `--tier`); depth vocab + TCS flooring; STOP conditions (output under `.claude/...`, zero-alias-tier2); §14 degraded-mode envelope mapping field values → degraded vs expected-not-halt. Output: `research/08-reflect-invocation-degradation-semantics.md`. Others cover: contract data shape (R02 — R08 references R02's fields but focuses on the routing semantics + invocation flags).

## TEMPLATE_NOTES

- **MDTM Template: 02 (Complex Task).** Justification: requires discovery (ClaudeProcess API, reflect contract field set, template integration), multi-phase build (6 new Python modules with distinct responsibilities), testing phase (CliRunner + fixtures + no-nesting guard), and verification gates (lint/format/type/test). Conditional flows (contract version tolerance, degradation routing). Not a simple known-input/known-output transformation → not Template 01.
- **Tier: Deep.** New CLI subsystem spanning subprocess management, contract parsing, frontmatter write-back, template branching, tests; 6 source files + main.py + tests + skill template edit; reuses 3+ existing subsystems.
- Generated task file should use granular per-module items (one item per `cli/reflect/*.py` file at minimum, likely split further by responsibility), explicit reuse-anchor citations, PER_PHASE QA gates (build is complex + safety-critical fail-closed logic), UNIT+INTEGRATION testing (CliRunner + monkeypatched ClaudeProcess + fixture contracts), and a no-nesting guard test (NFR-7). VALIDATION: lint + ruff format check + type + verify-sync (skill edits) + full test pass.

## AMBIGUITIES_FOR_USER

None that block building the task file — the spec is highly explicit (10 sections + resolved open questions + invariant probe). Genuine technical unknowns (current contract_version, build_env pop behavior, exact reflect flags) are codebase-resolvable by researchers, not user-intent ambiguities. The spec already resolved all 8 design open questions (§7). If researchers find a reflect flag named differently than the spec assumes (e.g., `--executor-model` does not exist), that will be flagged as a CODE-CONTRADICTED finding and routed to the task file's Open Questions, not silently assumed.

# Research Notes: reflect-wrapper AUTO-FIX evolution

**Date:** 2026-06-10
**Scenario:** A (Explicit — BUILD-REQUEST + merged-requirements spec with implementation surface)
**Depth Tier:** Standard (cohesive single-subsystem: `cli/reflect/` package + one skill file + tests)
**Track Count:** 1

---

## EXISTING_FILES

Canonical base = worktree `wrapper-onto-master` (audit-only reflect CLI on current
origin/master). Relative paths the task items reference:

- `src/superclaude/cli/reflect/commands.py` (~283 lines) — Click `reflect run`
  group; options `--tmux/--print-command/--promote(default False, commands.py:71-75)/
  --timeout/--depth/--output/--allow-single-vendor/--dry-run/--resume`; tmux
  fail-closed sentinel; calls `resolve_config` → `ReflectRunner(config).run()` →
  `sys.exit(result.verdict.exit_code)`.
- `src/superclaude/cli/reflect/config.py` (~223 lines) — `resolve_config` +
  `_resolve_base` (config.py:81-93: frontmatter `start_commit` else
  `git merge-base HEAD <base_branch=master>`); `.claude/{skills,agents,commands}`
  output STOP; `_DEFAULT_MAX_TURNS=250`; frontmatter keys `start_commit`,
  `spec_path`, `executor_model_class`.
- `src/superclaude/cli/reflect/runner.py` (~502 lines) — `ReflectRunner.run()`
  thin orchestrator: preflight → `_build_prompt` (`--diff <BASE>` single ref,
  runner.py:344) → `ClaudeProcess` launch → `parse_contract`/`derive_verdict` →
  atomic `write_reflect_post` (FR-6) + always-write `write_sidecar` (FR-7);
  `count_model_aliases`, `_child_env`, `_read_existing_reflect_post` (resume G2).
- `src/superclaude/cli/reflect/contract.py` (~326 lines) — pure `parse_contract`
  + `derive_verdict` (blocked→degraded→halted→pass, first-match-wins);
  `_halted_reason` reads `regression_present`/`needs_human_decision`/
  `user_decision_required`/`unauthorized_deviation_present`/drift/regression.
- `src/superclaude/cli/reflect/models.py` (~112 lines) — `Verdict` enum
  (exit map pass0/halted10/degraded11/blocked2), `ReflectConfig`, `ReflectResult`.
- `src/superclaude/cli/main.py` — `reflect_group` registered (`main.py:440-442`).
- `src/superclaude/skills/sc-reflect-protocol/SKILL.md` (§9.1 contract v1.3.0,
  §Will-Not "never auto-execute Tier 3", `refs/promotion-adapters.md`,
  `refs/remediation-handoff.md`).
- `tests/cli/reflect/` — conftest + fixtures (canonical base test home).

## PATTERNS_AND_CONVENTIONS

- Thin-wrapper guardrails (module docstrings, enforced by tests): NO import from
  `cli.sprint`/`cli.roadmap`; zero `async`; only `ClaudeProcess` launch path.
- Lazy heavy imports inside the command body (house convention, commands.py:126).
- Exit codes sourced from `Verdict.exit_code` ONLY (never re-hardcoded).
- Atomic writes via randomized same-dir temp + `os.replace` (runner.py:61).
- `_IndentDumper` for yamllint-conformant block sequences (runner.py:49).

## GAPS_AND_QUESTIONS

- Confirm `return-contract.yaml` v1.3.0 has NO `remediation_task_path` (FR-8 adds it).
- Confirm headless `--remediate` under `--print` currently OFFERS vs auto-authors (FR-9).
- Confirm exactly two promotion adapters (`task`, `sprint-release`) — no per-phase.
- Verify `ClaudeProcess.build_command()`/`build_env()` signatures for the
  `/task <remediation>` auto-run subprocess (reuse, don't reinvent).

## RECOMMENDED_OUTPUTS

- `research/01-reflect-cli-surface.md` — exact change points in commands/config/
  runner/contract/models for D1–D7 (flags, `_resolve_base` precedence, fix-loop
  insertion, marker guard, new model fields).
- `research/02-reflect-skill-contract.md` — contract v1.3.0 fields, FR-8/FR-9
  skill deltas, promotion adapters, remediation-handoff BUILD_REQUEST, Will-Not.
- `research/03-claudeprocess-tests-thinness.md` — `ClaudeProcess` launch/env API,
  `tests/cli/reflect/` patterns, thinness-guard test shapes, marker-suppression
  + carve-out + bounded-loop + `--base` test design.

## SUGGESTED_PHASES

- R1 (researcher 1): reflect CLI surface + per-file change points (commands,
  config, runner, contract, models). Reads canonical base only.
- R2 (researcher 2): reflect SKILL contract + refs (FR-8/FR-9 deltas, adapters).
- R3 (researcher 3): ClaudeProcess API + tests/cli/reflect patterns + thinness.

## TEMPLATE_NOTES

Template **02** (complex: discovery → CLI build → skill contract delta → tests →
verification). QA gates **PER_PHASE** (fail-closed verdict + recursion
termination + human-decision carve-out are safety-critical). Bootstrap exemption:
POST gate emitted as `--reflect 1` inline (CLI-independent), NOT a
`superclaude reflect run` shell-out (the command does not exist until this
tasklist completes).

## AMBIGUITIES_FOR_USER

None — intent is fully specified by the BUILD-REQUEST + merged-requirements spec
(decisions D1–D7 are pre-decided and grounded) + the contract artifact.

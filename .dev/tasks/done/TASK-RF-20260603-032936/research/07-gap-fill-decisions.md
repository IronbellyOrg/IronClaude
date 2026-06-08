# Research: Gap-Fill Decisions (A.8 quality-gate resolutions)

**Topic type:** Gap-fill / orchestrator decisions
**Status:** Complete
**Date:** 2026-06-03

Resolves the IMPORTANT/CRITICAL findings from `qa/analyst-completeness-report.md` (VERDICT FAIL, gap G1) and `qa/qa-research-gate-report.md` (VERDICT FAIL, I-1 + GAP-1). These are decisions/clarifications, not new codebase research — both gate agents independently confirmed the codebase-surface research (files 01-06) is accurate and needs no re-investigation.

---

## D1 — OQ halt-item scope (resolves analyst G1; USER-CONFIRMED 2026-06-03)

The BUILD_REQUEST framing ("OQ1–OQ3 are needs_human_decision items — write PENDING and halt") was drawn from `return-contract.yaml:40-45`, which lists all three as open. But the authoritative `merged-requirements.md` resolved two of them in round-3:

- **OQ1** (auto-eval on cold-path insert vs opt-in) → **RESOLVED: opt-in.** Auto-eval REJECTED by user (`merged-requirements.md:358`). Cold-path inserts populate `best_model: null`; user opts in via `--eval <mode>`. **Encode as a RESOLVED design fact — NOT a halt item.**
- **OQ2** (plugin precondition BLOCK vs degraded-data) → **RESOLVED: HARD-BLOCK**, option (a), no degraded-data fallback (`merged-requirements.md:378`; full schema in `round-4-synthetic-eval-cases.md`). **Encode as a RESOLVED design fact — NOT a halt item.**
- **OQ3** (best_model hint advisory vs prescriptive for downstream skills) → **genuinely OPEN** (absent from `merged-requirements.md`; only in `return-contract.yaml:45`). **Soft-PENDING Open Question** (does not gate implementation — the row schema carries `best_model` either way; the question is how downstream consumers treat it).

**User decision (AskUserQuestion, 2026-06-03): "Honor the spec."** Therefore the task file has:
- **ONE hard-halt item** — the Python-vs-skill-prose boundary (D2 below). Shape: 3A hard-halt (`status: "⚪ Blocked"` + `blocker_reason` + "DO NOT proceed") per `05-template-and-examples.md` precedent `TASK-PRD-20260514-121039`.
- **TWO soft-PENDING Open Questions** (bottom-of-file `### Open Questions` section, 3B precedent `TASK-RF-20260517-213436`): OQ3 (best_model advisory/prescriptive) + the eval-reuse conflict (D3).
- OQ1 and OQ2 encoded as resolved design constraints in the relevant phase items (opt-in default; HARD-BLOCK precondition).

## D2 — The genuine needs_human_decision: Python-vs-skill-prose boundary (HARD-HALT)

Sharpened per qa GAP-1 (the anthropic-SDK ban makes "the parent commits the cache" non-trivial). Evidence (from `04-classifier-and-dispatch.md` §4 + `06-tests-sync-registration.md`):

- **Constraint A:** `anthropic` SDK is BANNED (`pyproject.toml:208-211`, ruff `flake8-tidy-imports.banned-api`). No in-process model calls.
- **Constraint B:** Agent-tool spawning (`model: haiku`) is **Claude-session-only** (skill prose); the CLI cannot spawn Agent subagents.
- **Constraint C:** Atomic YAML write + sha256 + JSONL append + eval aggregation are **deterministic Python** (`cli/recommend/`); "Haiku cannot write files" (spec states twice) → the parent writes.

So "the parent" cannot trivially be both the Agent-spawner (Claude) and the file-committer (CLI). The HALT item must present these concrete options for the human to choose BEFORE any dispatch code is written:

- **Option H (Haiku-heavy / thin parent):** SKILL.md orchestrates everything via Agent tool; the new `cli/recommend/` module is a thin library of pure helpers (cache read/write, sha256, telemetry, eval aggregate) that the *skill* invokes via `Bash(uv run python -m superclaude.cli.recommend ...)` between Agent calls. Dispatch logic lives in skill prose. (Maps to spec line 113 "inline table into Haiku prompt".)
- **Option P (Python-heavy / thin Haiku):** A `cli/recommend/` CLI subcommand owns classify-dispatch-validate-commit as ~150 LoC; the skill is a thin wrapper that shells to it and only spawns Agents for the cold-path LLM work. (Maps to spec line 414 "~150 LoC parent code".)
- **Option Hybrid:** Skill owns Agent orchestration + dispatch decisions; CLI owns ONLY the deterministic file/eval ops as discrete subcommands (`cache get/put`, `telemetry append`, `eval run`). Most faithful to "Haiku cannot write files" + anthropic-ban. (Likely the intended reading, but the spec does not state it — so it HALTS for confirmation.)

The task file HALTS here: implementation phases 3+ (dispatch wiring, --eval) depend on this answer.

## D3 — Module path canonicalization (resolves analyst I-1 / qa I-1)

Files 01+06 say `cli/recommend/`; file 03 says `cli/sc_recommend/`. **CANONICAL: `src/superclaude/cli/recommend/`** — matches the click group name `recommend`, the peer-module convention (`cli/tasklist/`, `cli/roadmap/`), and the `main.py` registration `name="recommend"`. All task items use `cli/recommend/`. (File 03's `sc_recommend/` references are superseded.)

## D4 — Eval-reuse conflict (soft-PENDING Open Question)

`merged-requirements.md` says reuse the `.dev/eval-workspaces` scaffolding (`build_benchmark.py` + `grader.py`); `round-4-synthetic-eval-cases.md` says reuse the `cli/eval/` cliEval harness. Research file 03 verified `cli/eval/` is a PTY-subprocess harness with **no token/model axis** (`models.py:337,74`) and a scratch-root allowlist that excludes `.claude/cache/eval-runs/` — so it is NOT directly reusable for per-row multi-model eval. Both practically resolve to porting the `.dev`-style grader/aggregator into `cli/recommend/` (re-grouping the aggregation axis from `with_skill|without_skill` to `opus|sonnet|haiku`), with the anthropic-ban forcing subprocess-based model runs. **Builder encodes the `.dev`-port approach as the working plan but lists the conflict as an Open Question** so the human can override toward cliEval if desired. NEW (no precedent): deterministic `best_model` tier selection + `generate_review.py` for the round-4 user-review gate (confirmed absent).

## D5 — Minor corrections (apply silently)

- SKILL.md is **226 lines** (file 01 correct; file 04's 227 is off-by-one). Refs counts per file 01.
- `sc-recommend/SKILL.md` `allowed-tools` must GAIN `Edit, Write, Agent, Task` for the hot/cold dispatch + cache commit (currently read-only + research tools). Encode as an explicit item.
- Atomic-write temp-name: prefer the **randomized** temp-name variant (`install_hooks._atomic_write_json`) over convergence's fixed `.tmp`, per file 06 — bounds the worktree-concurrency last-write-wins risk (spec Risk #12).
- `recommend` MUST be added to `EXPECTED_TOP_LEVEL_COMMANDS` (`tests/cli/test_cli_registration.py:31`) or `test_top_level_command_roster_unchanged` fails — encode as a test-phase item.
- `.gitignore`: the `!.claude/cache/` negation block goes AFTER line 118 (the `.claude/` blanket + `!settings.json`), last-match-wins; dir-negation before file-negations; `sc-recommend-events.jsonl` re-ignore LAST. This is a `.claude/` staging touchpoint → the gitignore item itself notes user-authorization is already granted in-spec (Gitignore Exception R3) but staging still follows CLAUDE.md discipline.

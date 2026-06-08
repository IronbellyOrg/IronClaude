# Research Notes: sc-recommend lookup-cache layer

**Date:** 2026-06-03
**Scenario:** A (explicit — user supplied authoritative spec + primary surface + pattern anchors)
**Depth Tier:** Deep (20+ files across skill, command, new Python module, gitignore, hooks, eval harness, tests; multiple subsystems)
**Track Count:** 1 (one cohesive feature; the 12-step Implementation Order is sequential, not independent streams)

**TASK_ID:** TASK-RF-20260603-032936
**Authoritative spec:** `.dev/brainstorms/sc-recommend-lookup-cache/merged-requirements.md` (435 lines; MVP architecture + 12-step Implementation Order + 12 open risks)
**Supporting specs:** `.dev/brainstorms/sc-recommend-lookup-cache/round-4-synthetic-eval-cases.md`, `.dev/brainstorms/sc-recommend-lookup-cache/return-contract.yaml` (OQ1-OQ3)

---

## EXISTING_FILES

Pre-verified during the preceding `/sc:analyze` pass (every path confirmed to exist with cited symbol unless noted):

**Primary surface (create/modify):**
- `.gitignore` — line 103 currently `.claude/cache/` (IGNORED). Must flip to tracked `!.claude/cache/` exception block + re-ignore `sc-recommend-events.jsonl`. (Impl-Order step 1)
- `src/superclaude/skills/sc-recommend/SKILL.md` — 226 lines. Phase 0 (surface enum + auggie gate), Phase 1 net-value, Phase 2 prompt build, Phase 3 --plugin, R1-R4 rules. This is the cold-path source to condense to ~50 lines + add hot/cold dispatch + --eval parsing + model:haiku subagent invocation.
- `src/superclaude/skills/sc-recommend/refs/{surface-enumeration.md, delegation-vs-native-heuristics.md, plugin-ecosystem-sources.md}` — 3 refs.
- `src/superclaude/commands/recommend.md` — command surface, currently `--plugin` only. Add `--eval none|quick|normal|deep`.
- **NEW** `src/superclaude/cli/recommend/` — does NOT exist yet. Home for the ~700 LoC: YAML cache reader/writer, telemetry append, eval orchestrator, plugin eval gate.

**Pattern templates (read & mirror, do NOT modify):**
- `src/superclaude/cli/roadmap/convergence.py:304` `DeviationRegistry.save()` — atomic `tmp + os.replace()`, `schema_version`, hash-reset-on-mismatch (`load_or_create:104`). ⚠️ Writes JSON; cache is YAML → mirror pattern, use `yaml.safe_dump`.
- `src/superclaude/cli/install_mcp.py:470` `check_mcp_server_installed()` + `:156` `check_binary_available()` — plugin-eval HARD-BLOCK precondition.
- `src/superclaude/skills/sc-task-protocol/SKILL.md` + `src/superclaude/core/ORCHESTRATOR.md:162-189` — closed-enum classifier (tier keyword tables, scoring, top-2 confidence, <0.7 prompt).
- `src/superclaude/skills/task-builder/SKILL.md:786` — Agent spawn shape with `model:` override.

**Eval harness reuse:**
- `src/superclaude/cli/eval/` — FULL eval CLI: `orchestrator.py, runner.py, loader.py, run_report.py, commands.py, models.py, config.py, coverage.py, retry.py, suites/, schemas/`. Bigger reuse target than the .dev scripts; researcher must map what's reusable for `--eval`.
- `.dev/eval-workspaces/sc-recommend/iteration-1/build_benchmark.py` + `.dev/eval-workspaces/sc-recommend/grader.py` — assertion/grader mechanics.
- ⚠️ `evals.json` is at `.dev/eval-workspaces/sc-recommend/evals.json`, NOT `iteration-1/evals.json` (spec cites the wrong path).

**Install/registration surface:**
- `src/superclaude/cli/install_hooks.py:43` `_FRESHNESS_SCRIPTS` (already includes `sc-recommend-phase0.sh:85`) — register any new hook here.
- `src/superclaude/hooks/scripts/sc-recommend-phase0.sh` — existing PreToolUse(Skill) gate.
- `.claude/settings.json` — PreToolUse registration (project-local).
- `src/superclaude/cli/main.py` — CLI command group registration (verify where `recommend` subgroup would wire in).

**Feasibility confirmed:** `pyyaml>=6.0` already in `pyproject.toml`. No `tests/**recommend**` exists today → tests phase needed.

## PATTERNS_AND_CONVENTIONS

- **Source-of-truth discipline:** all edits in `src/superclaude/`; `make sync-dev` → `.claude/`; `make verify-sync` must pass before commit. NEVER stage `.claude/` except `settings.json` (CLAUDE.md ABSOLUTE RULE).
- **Atomic state write:** `tmp + os.replace()` (convergence.py:304, executor.py:2832 `write_state`). Mirror for YAML.
- **YAML I/O precedent in cli:** `spec_parser.py`, `eval/loader.py`, `audit/wiring_config.py` use `yaml.safe_load`/`safe_dump`.
- **Hash-reset:** `schema_version` + content-hash compare → reset on mismatch (DeviationRegistry.load_or_create).
- **Subagent model override:** Agent tool with `model: haiku` (task-builder/SKILL.md:786 spawn shape).
- **Hook contract:** PreToolUse fail-open (exit 0), stdout injected as context (sc-recommend-phase0.sh).

## GAPS_AND_QUESTIONS

- **Python-vs-skill-prose boundary (USER-FLAGGED needs_human_decision):** Which logic lives in the new `cli/recommend/` Python module vs. orchestrated by the SKILL.md (Claude + Agent tool)? The spec mixes "parent commits cache via atomic write" (Claude-side) with ~700 LoC Python estimates. MUST resolve before dispatch code. → task-level Open Question / PENDING-halt item.
- **OQ1** (return-contract.yaml): cold-path inserts auto-trigger `--eval quick` vs stay opt-in? (spec scaling-path #4 says REJECTED/opt-in, but listed as open) → needs_human_decision PENDING.
- **OQ2**: plugin eval BLOCK on setup self-check vs degraded-data flag? (Risk #6 says HARD-BLOCK resolved) → needs_human_decision PENDING.
- **OQ3**: best_model hint advisory vs prescriptive for downstream skills? → needs_human_decision PENDING.
- Where exactly the CLI `recommend` group registers in `cli/main.py` (researcher to confirm).
- Whether `--eval` orchestration is a CLI subcommand or skill-driven Agent fan-out (depends on Python-vs-skill boundary resolution).

## RECOMMENDED_OUTPUTS

6 researcher files in `research/`:
- `01-file-inventory.md` — primary surface + new-module insertion point + exact line counts/exports
- `02-pattern-templates.md` — convergence atomic-write, install_mcp checks, YAML I/O, classifier, Agent model-override (verbatim with file:line)
- `03-eval-harness-reuse.md` — deep map of `cli/eval/` + .dev scaffolding; reusable-vs-new for `--eval`
- `04-classifier-and-dispatch.md` — hot/cold dispatch, closed-enum classifier, current sc-recommend Phase 0-3 cold-path to condense
- `05-template-and-examples.md` — 02 template PART 1 rules (A3/A4/B2/L1-L6), done-task examples
- `06-tests-sync-registration.md` — tests/ conventions, cli test patterns, make sync model, hooks.json/settings.json/main.py registration, gitignore mechanics

## SUGGESTED_PHASES

Per merged-requirements 12-step Implementation Order (→ task phases):
1. Resolve needs_human_decision (Python-vs-skill boundary + OQ1-3) — PENDING/halt gate
2. .gitignore exception flip
3. YAML cache reader/writer (new module, mirror convergence)
4. Haiku classifier prompt (closed-enum)
5. Condensed cold-path runbook (~50 lines from SKILL.md)
6. Hot/cold dispatch wiring in SKILL.md + command --eval flag
7. JSONL telemetry append
8. --eval flag pipeline (reuse cli/eval + .dev scaffolding)
9. Plugin eval gate (install_mcp precondition HARD-BLOCK)
10. Tests phase (new tests/**recommend**)
11. sync-dev + verify-sync validation
12. Hand-validate vs eval-1 cases / decision gate

## TEMPLATE_NOTES

- **Template 02** (complex: discovery + build + test + review phases, conditional flows, QA gates). Confirmed by user ("complex template-02").
- **Tier Deep**: 6 researchers, 0-2 web (likely 0 — all internal; external knowledge already in spec).
- **QA_GATE_REQUIREMENTS: PER_PHASE** (template 02 default; multi-phase build with verify-sync gates).
- **TESTING_REQUIREMENTS: UNIT** minimum (new Python module → pytest; plus integration for dispatch).
- **VALIDATION_REQUIREMENTS:** `make lint`, `make sync-dev`, `make verify-sync`, `uv run pytest` must pass.
- **needs_human_decision items must HALT** (write PENDING, do not auto-default) per user + memory `feedback_human_decision_items_must_halt`.

## AMBIGUITIES_FOR_USER

Four genuine intent ambiguities, all routed to needs_human_decision PENDING items (NOT silently assumed): the Python-vs-skill-prose boundary, plus OQ1 (auto-eval), OQ2 (plugin precondition block mode), OQ3 (best_model advisory/prescriptive). The spec gives a leaning on each (opt-in / HARD-BLOCK / —) but return-contract.yaml lists them as unresolved, so the task file surfaces them as halt-gates rather than baking in a default.

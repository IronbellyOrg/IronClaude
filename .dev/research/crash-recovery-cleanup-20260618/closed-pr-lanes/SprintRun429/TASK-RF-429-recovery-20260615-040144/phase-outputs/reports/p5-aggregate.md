# P5 (Phase 6) Aggregate Manifest — Alias Suggester + Halt UX + CLI Flag + Doc Parity

Consolidated inventory of all P5 deliverables for the Phase 6 QA gate. Every file
below was discovered on disk; the load-bearing facts are recorded for the lens agents.

## Source files

| File | Purpose | Load-bearing facts |
|------|---------|--------------------|
| `src/superclaude/cli/sprint/aienv.py` | **NEW.** `~/.aienv` alias reader + suggester | OQ-1 **DECIDED: option A (os.environ reader)**. `_load_aliases(env=None)` reads `ANTHROPIC_DEFAULT_{OPUS,SONNET,HAIKU}_MODEL` + `T2Model01..09`, **reusing `T2_MODEL_ENV_PREFIX`/`T2_MODEL_MAX_SLOTS` imported from `swarm.config`** (no drift). `suggest_alternate_model(failed_model_or_alias, *, env=None) -> str|None`: matches by alias OR resolved id, returns next DISTINCT alias, **None-safe** (never fabricates). Module docstring documents option B (file-parser) as the **rejected** alternative. |
| `src/superclaude/cli/sprint/models.py` | halt-UX builder + exhaustion-aware resume + config field | `build_account_exhaustion_halt(config, halt_task_id, exhausted_model, suggested_model, remaining_tasks, ledger=None)` — **single-line** `--resume <task> --model <suggested>`, names exhausted model + **CLIProxyAPI** rationale, None-safe (no `--model` fabricated). `SprintResult._exhaustion_halt()` + exhaustion-aware `resume_command()` (model-switch line for `halt_reason=="provider_exhaustion"`, else `--start/--end`). `SprintResult.account_exhaustion_output()` wraps the block builder. New field `SprintConfig.max_session_resets: int = 8` (hop 4 — closes the chain). |
| `src/superclaude/cli/sprint/commands.py` | CLI flag hops 1-2 | `@click.option("--max-session-resets", "max_session_resets", type=int, default=8, show_default=True, ...)` (mirrors `--task-parallelism`); `run()` param `max_session_resets: int`; threaded into `load_sprint_config(max_session_resets=...)`. |
| `src/superclaude/cli/sprint/config.py` | CLI flag hop 3 | `load_sprint_config(..., max_session_resets: int = 8)` forwards `max_session_resets=...` into `SprintConfig(...)`. |
| `src/superclaude/cli/sprint/executor.py` | policy reads the flag | `SessionResetPolicy(max_session_resets=getattr(config, "max_session_resets", 8))` at the K>1 (`:1334`) and K=1 (`:1901`) sites now resolves the real field. (No new P5 edit — P3 wiring; the field now exists so the operator flag flows through.) |
| `src/superclaude/cli/sprint/logging_.py` | block emission | `write_summary()` appends `sprint.account_exhaustion_output()` to the markdown execution-log on exhaustion halts (no-op otherwise) — makes `build_account_exhaustion_halt` a live consumer. |
| `docs/guides/sprint-cli-tools-release-guide.md` | doc⇆CLI parity entry | `### Key options` gains `- \`--max-session-resets N\` ... Default: \`8\``. |

## Test files

| File | Purpose |
|------|---------|
| `tests/sprint/test_aienv.py` | **NEW.** 6 unit tests for `suggest_alternate_model` via the `env=` seam (never real `~/.aienv`): opus→sonnet (resolved + alias), `T2Model01`→`T2Model02`, single-slot→None, unknown→None, identical-resolved→None. |
| `tests/sprint/test_models.py` | `TestBuildAccountExhaustionHalt` golden string: exactly one `--resume` line with `--resume T03.14 --model sonnet`, names `claude-opus-4-8`, `CLIProxyAPI` rationale; None-safe asserts no `--model`. |
| `tests/sprint/test_cli_contract.py` | `test_run_help_exposes_max_session_resets` — flag in `sprint run --help`. |
| `tests/sprint/test_sprint_docs_cli_parity.py` | **NEW.** `parents[2]` repo-root; flags-parity (phantom strict; missing with `_UNDOCUMENTED_BY_DESIGN` curation; `--max-session-resets` required); defaults-parity (`Default: \`8\`` == Click default 8). |

## Validation evidence (phase-outputs/test-results/)

- `p5-pytest.txt` — **176 passed, 0 failed** (exit 0).
- `p5-lint.txt` — P5 files: `ruff format --check` 10 files already formatted (exit 0) + `ruff check` All checks passed (exit 0). Whole-tree format failures are **pre-existing, unrelated modules only** (no `cli/sprint/`).
- `p5-verify-sync.txt` — `make verify-sync` exit 0 (no `.claude/` drift).

## Key facts for lens verification

1. **os.environ reader (OQ-1 = option A, operator-decided)**; option B documented-not-shipped.
2. **Single-line resume command** (terminal cannot paste multi-line, memory `feedback_no_multiline_paste`).
3. **4-hop flag chain closed**: commands.py `@click.option` + `run()` param + `load_sprint_config` call → config.py DEF param + `SprintConfig(...)` pass → models.py `SprintConfig.max_session_resets` field → executor policy reads `config.max_session_resets`.
4. **doc⇆CLI parity entry added** with `Default: \`8\``.
5. **Necessary deviation (operator-approved):** halt-UX wired at the real seam `SprintResult.resume_command()`/`account_exhaustion_output()` + `logging_.write_summary()`, NOT executor.py + the dead `build_resume_output`. See ### Phase 6 Findings.

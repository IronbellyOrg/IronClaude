# Research Notes: Remediate `superclaude reflect run` audit findings (F0, F1, F2, F4, F5, F6)

**Date:** 2026-06-09
**Scenario:** A (explicit — fixes precisely specified with file:line)
**Depth Tier:** Quick (single subsystem, <6 source files, zero discovery needed — research pre-computed by the sc:reflect --mode post audit)
**Track Count:** 1
**Source of truth:** `.dev/reflect/post-reflect-cli-wrapper-20260609172031/deviation-register.yaml` (every finding grounded to file:line during the POST reflect audit)

---

## EXISTING_FILES

All under `src/superclaude/cli/reflect/` (the thin fail-closed POST reflect wrapper). Each finding's exact location was verified line-by-line during the audit.

- **`contract.py`** (282 lines) — the isolated §6 verdict map + FR-11 degradation routing + contract_version gating. PURE module (depends only on `.models` + stdlib + PyYAML). Touched by **F0, F2, F5**.
  - `derive_verdict(contract, *, expected_tier, allow_single_vendor, child_rc)` lines 110-204 — first-match-wins blocked→degraded→halted→pass.
  - `_make_result(...)` lines 87-107.
  - `_degraded_reason(...)` lines 207-262 (the 14 FR-11 triggers).
  - `_halted_reason(contract)` lines 265-282.
- **`runner.py`** (474 lines) — thin orchestrator + atomic race-safe write-back. Touched by **F1, F6**.
  - `_FRONTMATTER_RE` line 44 (`^---[ \t]*\n(.*?)\n---[ \t]*$`, no `\r` handling).
  - `write_reflect_post(...)` lines 110-173 (reads bytes, decodes UTF-8, splices; no CRLF normalization).
  - `_read_existing_reflect_post(...)` lines 274-307 (same regex; also affected by CRLF).
  - `_claude_argv_preview(self)` lines 340-347 (dry-run preview string, drifts from real build_command).
  - `ReflectRunner.run()` lines 351-474 (downgrade-on-unwritable at 465-467).
- **`commands.py`** (249 lines) — Click `reflect_group` + `run`. Touched by **F4**.
  - `run(...)` config-error handler lines 145-148 (`except ValueError: echo + sys.exit(2)` — no sidecar).
- **`models.py`** (111 lines) — `Verdict` enum + dataclasses. Likely unchanged (read-only reference for F0/F5).
- **`config.py`** (222 lines) — `resolve_config`. Not in remediation scope (F3 deferred).

**Reused primitives (verified to exist, do NOT modify):**
- `ClaudeProcess` at `src/superclaude/cli/pipeline/process.py:37-95` — kwargs-only ctor; `build_command()` lines 73-95 emits `claude --print --verbose --dangerously-skip-permissions --no-session-persistence --tools default --max-turns N --output-format <fmt> [--model M]`. **F6 fix must render the preview from this real shape.**
- `extract_frontmatter` at `src/superclaude/cli/pipeline/frontmatter.py:90` — normalizes `content.replace("\r\n", "\n")`. **F1 fix should mirror this normalization in the write-back parser.**

**Test surface:** `tests/cli/reflect/` — `conftest.py` (CliRunner, `patch_git`, `patch_runner_env`, Idiom-B `make_claude_process_stub`), `fixtures/*.yaml` (7 §9.1-shaped contracts), `test_verdict_mapping.py` (16), `test_runner_e2e.py` (10), `test_writeback.py` (2), `test_cli_smoke.py` (5), `test_no_nesting_guard.py` (2). 35 passing. New fixtures + tests append here.

## PATTERNS_AND_CONVENTIONS

- **First-match-wins ordering** in `derive_verdict`: blocked → degraded → halted → pass. New blocked checks go in the BLOCKED block (lines 127-153), before degraded.
- **Defensive contract reads:** `.get(...)` everywhere; `_extract_deviations` int-coerces with try/except. F2's malformed-bool guard should follow this defensive style but route to BLOCKED (fail-closed), not silently coerce.
- **Exact-membership** sets (`_DEGRADED_COMPONENTS_HALT_SET`, `_VERIFICATION_SKIP_EXEMPTIONS`) as module-level `frozenset`.
- **Atomic write:** `_atomic_write_text` randomized same-dir temp + `os.replace`; `_IndentDumper` (yamllint-safe block style).
- **Tests:** pytest, `uv run pytest`; fixtures are YAML contract files loaded via `conftest.FIXTURES_DIR`; verdict tests parametrize over fixture→expected-verdict. Idiom-B stubs `ClaudeProcess`. CI runs `ruff check` AND `ruff format --check` separately (both must pass).
- **SoT discipline:** edits ONLY in `src/superclaude/`; the task-builder SKILL.md is NOT touched by this remediation (F3 deferred, and no template change here). No `.claude/` staging. `make verify-sync` only if a synced component changes (none here — pure Python package + tests), so verify-sync is a no-op safety check.

## GAPS_AND_QUESTIONS

- **F3 is DEFERRED** — needs the operator's (a)-vs-(b) decision (persist `executor_model_class:` in task-builder frontmatter, OR add `executor_class_resolved==false` to the wrapper FR-11 degraded set). It is recorded as an Open Question, NOT a task item. Do not implement F3.
- **F0 fix shape (decided by operator):** the operator chose fail-closed — "block any non-zero child_rc in contract.py". So the fix is: in `derive_verdict`, after the `child_rc == 124` timeout check, add `if child_rc != 0: return BLOCKED reason="child-crash"` BEFORE trusting contract fields. This makes the timeout case a subset and removes the asymmetry. No §6 spec amendment needed (the literal §6 "child crash → blocked" reading wins).

## RECOMMENDED_OUTPUTS

Per-finding granular fix items (one per finding) + per-finding test items, then validation gates. No new modules — edits to 3 existing source files + new/extended tests + fixtures.

## SUGGESTED_PHASES

- **Phase 1 — contract.py fixes (F0, F2, F5):** the load-bearing verdict-map module. F0 first (highest severity), then F2 (malformed-bool→blocked), then F5 (status-failed reason slug).
- **Phase 2 — runner.py + commands.py fixes (F1, F6, F4):** F1 CRLF normalization in write-back/`_read_existing_reflect_post`, F6 argv-preview from real `build_command()`, F4 sidecar-on-config-STOP.
- **Phase 3 — tests + fixtures:** one regression test per finding (child-crash-with-success-contract→blocked; malformed-bool→blocked; status:failed→halted reason status-failed; CRLF write-back round-trip; argv-preview parity; config-STOP sidecar). New fixtures as needed.
- **Phase 4 — validation gates:** `uv run pytest tests/cli/reflect/`, `ruff check`, `ruff format --check`, `pytest tests/cli/prd/` regression, real CLI smoke.
- **Phase 5 (final) — POST reflect gate + Done.**

## TEMPLATE_NOTES

- **Template 02** (complex: multi-phase, build + test + validate). Tier Quick→Standard (precise, but multi-file + tests + gates).
- **POST reflect depth:** TCS → `deep` (S6=1 remediation-class type forces deep per O2; O4 floors POST at ≥standard). POST gate emitted as self-run subagent item (penultimate), `--executor-model opus`, `--diff 015e7285..HEAD`.
- **QA gates in the generated tasklist:** final-document gate isn't applicable (this produces code, not a >500-line doc); use a task-integrity validation phase. Keep QA proportional — this is a 6-fix remediation, not a greenfield feature.

## AMBIGUITIES_FOR_USER

- F3 resolution (deferred — explicitly out of scope per the user's instruction "F3 needs my decision first"). Recorded as the tasklist's sole Open Question.
- F0 fix direction: RESOLVED by operator = fail-closed (block any non-zero child_rc). No remaining ambiguity for the 6 in-scope fixes.

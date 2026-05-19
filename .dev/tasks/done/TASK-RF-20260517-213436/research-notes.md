# Research Notes: hook-sync-and-matcher-fix release

**Date:** 2026-05-17
**Scenario:** A (explicit — full release-spec.md + sibling design-spec.md provided)
**Depth Tier:** Standard
**Track Count:** 1

**Release spec:** `.dev/releases/current/hook-sync-and-matcher-fix/release-spec.md`
**Part 1 design:** `.dev/releases/current/hook-sync-and-matcher-fix/hook-sync-coverage-spec.md`

---

## EXISTING_FILES

Verified against master (HEAD on `feat/mig-002-execution-context-header`, 2026-05-17):

### Files to MODIFY
- `Makefile` (lines 154-247 = current `verify-sync` target)
  - Iterates `src/superclaude/skills/`, `src/superclaude/agents/`, `src/superclaude/commands/`
  - Pattern: forward (`src → .claude`) + reverse (`.claude → src`) with `diff -q`, `❌ MISSING` / `⚠️ DIFFERS` / `✅` symbols
  - Final block sets `drift=0` → exit 1 if drift detected
  - **Insertion point:** after `=== Commands ===` block ends (~line 240), before the final drift summary (~line 242)
- `src/superclaude/hooks/hooks.json` line 60 — single-line matcher change
  - Verified current value: `"matcher": "mcp__auggie__.*|mcp__airis-mcp-gateway__auggie_.*"`
  - Target: add `mcp__auggie-mcp__.*` as middle alternative
- `src/superclaude/hooks/scripts/auggie-flag-clear.sh`
  - Line 2 header comment — describe widened prefix set
  - Line 22 case body — add `mcp__auggie-mcp__*` glob

### Files to CREATE
- `tests/cli/test_verify_sync_hooks.py` — pytest wrapper invoking `make verify-sync` via subprocess

### Reference Files (read-only context)
- `src/superclaude/cli/install_hooks.py` (lines 43-56)
  - `_FRESHNESS_SCRIPTS` list (8 entries): freshness-session-start.sh, freshness-user-prompt.sh, freshness-pre-edit.sh, freshness-post-read.sh, freshness-file-changed.sh, freshness-subagent-start.sh, freshness-subagent-stop.sh, auggie-flag-clear.sh
  - `_LEGACY_SCRIPTS = ["session-init.sh"]`
- `src/superclaude/hooks/scripts/*.sh` — 8 hook scripts currently in source-of-truth
- `.claude/hooks/*.sh` — 11 hooks deployed (8 from src + session-init.sh + 2 untracked: auggie-bash-gate.sh and freshness-pre-edit.sh has been synced)
  - **Confirmed orphan:** `.claude/hooks/auggie-bash-gate.sh` exists but no `src/` counterpart (per release-spec §1.2 & §6)
- `tests/hooks/test_auggie_first.py` — existing subprocess-based test pattern to mirror
- `tests/cli/test_install_hooks.py` — existing install_hooks test patterns

### Surface map
| File | Action | LOC delta |
|------|--------|-----------|
| `Makefile` | MODIFY (insert ~75 LOC in `verify-sync` target) | +75 |
| `src/superclaude/hooks/hooks.json` | MODIFY line 60 | +0 (1-line change) |
| `src/superclaude/hooks/scripts/auggie-flag-clear.sh` | MODIFY lines 2 + 22 | +1 (header expands; case body widens 1 char) |
| `tests/cli/test_verify_sync_hooks.py` | CREATE | +~80 |

**Total surface: 1 modified Makefile, 1 modified JSON, 1 modified shell script, 1 new test file. ~155 LOC.**

---

## PATTERNS_AND_CONVENTIONS

### Makefile verify-sync section pattern (Makefile:158-241)
For each existing component type (skills/agents/commands), the verify-sync target follows this 3-part pattern:
1. **Section header:** `echo ""; echo "=== <ComponentType> ==="; \`
2. **Forward check** (`src` → `.claude`): for-loop over `src/superclaude/<type>/*`, check existence at `.claude/<type>/<name>`, run `diff -q`, emit `❌ MISSING`/`⚠️ DIFFERS`/`✅`, set `drift=1` on failure.
3. **Reverse check** (`.claude` → `src`): for-loop over `.claude/<type>/*`, check counterpart in `src/`, emit `❌ MISSING in src/...` on orphan.

The skills check has an extra `case "$$name" in __*) continue;; esac` guard. The commands check skips README.md.

Hooks section will mirror this exactly, with `session-init.sh` case-skip in the reverse loop (it lives in `src/superclaude/scripts/`, not `hooks/scripts/`).

### Hook script conventions
- All hooks live at `src/superclaude/hooks/scripts/*.sh`
- All start with `#!/usr/bin/env bash`
- All set `set -u` minimum; some `set -euo pipefail`
- Fail-open semantics (NFR-3): wrap risky ops in `|| true`
- Standard hook header: shebang → 1-line purpose comment → spec/proposal reference → set flags → optional `AUGGIE_FIRST_DISABLE`/similar disable env check

### Test patterns (tests/hooks/test_auggie_first.py)
- Uses `subprocess.run(...)` to invoke shell scripts directly with `input=` for stdin
- Asserts on stdout, exit codes, and side-effect file content
- Heavy use of `tmp_path` fixture from pytest
- Uses `monkeypatch.setenv("HOME", str(tmp_path))` to redirect `~/.claude/`
- Test names follow `test_<scenario_id>_<description>` (e.g., V1, V2)

### Test patterns (tests/cli/test_install_hooks.py)
- Uses `tmp_path` for temporary settings.json
- Calls Python API directly (`install_hooks(target_path=...)`)
- Asserts on returned `(success, message)` tuple

For `test_verify_sync_hooks.py`, the pattern needs to be **hybrid**: invoke `make verify-sync` via subprocess (per spec §7) AND operate on a `tmp_path` copy of the repo for V3-V7 (mutation scenarios). Approach: copy the few relevant files into a temp tree, run a constructed `make`-like invocation. Or alternatively: use `cwd=tmp_path` with a minimal Makefile fragment copied in. **Recommendation per spec §7:** invoke against the actual repo for V1-V2 (clean tree + simple file removal that gets restored), use `tmp_path` checkout + isolated `make verify-sync` invocation for V3-V7. See [SUGGESTED_PHASES] for testing strategy details.

---

## GAPS_AND_QUESTIONS

### Resolved by spec
- ✅ Option 1 vs 2 vs 3 for matcher widening — Option 1 chosen, debate captured in spec §4.3
- ✅ Test framework choice (Option A pytest wrapper vs Option B Python extraction) — Option A chosen per spec §7
- ✅ Orphan `.claude/hooks/auggie-bash-gate.sh` handling — explicitly OUT OF SCOPE (spec §6); release surfaces it via detection, response is separate decision
- ✅ Phase ordering — spec §10 recommends Phase 1 (Part 2 patches) → Phase 2 (Part 1) → Phase 3 (Part 3) → Phase 4 (tests) → Phase 5 (orphan decision) → Phase 6 (QA gate)

### Researcher will need to investigate / confirm
- **R-1** Exact `Makefile` insertion line range for the new sections (current `verify-sync` final `drift` summary at approximately line 242, need to verify exact line number for clean Edit anchor)
- **R-2** Existing test invocation pattern: does the project currently invoke `make` from a subprocess in any test? Check `tests/cli/test_install_hooks.py` and similar for prior art.
- **R-3** Confirm `jq` is on PATH in CI (per spec §11 R1) — check `pyproject.toml`, GitHub Actions config, or Dockerfile
- **R-4** Confirm `uv run` works in CI (per spec §4.2 caveat) — standard project assumption
- **R-5** Pre-merge state of `.claude/hooks/auggie-bash-gate.sh` — research confirms it's present on disk but gitignored (per spec §1.2)

### Acceptable open questions
- **OQ-1** AC-2.2 (manual end-to-end auggie sticky test) requires a live session — CANNOT be automated within the task file. Document as a post-merge manual verification step.
- **OQ-2** Whether to address the orphan during this task or defer per spec §6. Default: DEFER per spec §6, surface in task log.

---

## RECOMMENDED_OUTPUTS

| Researcher | Topic | Output file |
|-----------|-------|-------------|
| 1 | File Inventory | `${TASK_DIR}research/01-file-inventory.md` |
| 2 | Patterns & Conventions | `${TASK_DIR}research/02-patterns-conventions.md` |
| 3 | Test & Verification | `${TASK_DIR}research/03-test-verification.md` |
| 4 | Template & Examples | `${TASK_DIR}research/04-template-examples.md` |

---

## SUGGESTED_PHASES

The generated task file should follow the 6-phase decomposition from spec §10:

### Phase 1 — Preparation & Spec Confirmation
- Read release-spec.md and hook-sync-coverage-spec.md
- Verify current state of target files (hooks.json line 60, auggie-flag-clear.sh line 22, Makefile verify-sync target)
- Confirm `make verify-sync` currently passes (baseline)

### Phase 2 — Part 2 patches (matcher widening; highest user impact, smallest diff)
- Edit `src/superclaude/hooks/hooks.json:60` — add `mcp__auggie-mcp__.*` to matcher regex
- Edit `src/superclaude/hooks/scripts/auggie-flag-clear.sh:22` — add `mcp__auggie-mcp__*` to case body glob
- Edit `src/superclaude/hooks/scripts/auggie-flag-clear.sh:2` — update header comment for widened prefix set
- Run `make sync-dev` to propagate changes to `.claude/hooks/`
- Validate AC-2.1 (grep proves both files mention `mcp__auggie-mcp__`)

### Phase 3 — Part 1 verify-sync hook section
- Insert `=== Hooks ===` section in `Makefile` `verify-sync` target (forward + reverse checks with session-init.sh case-skip)
- Smoke-test: `make verify-sync` exits 0 on clean tree
- Smoke-test: `rm .claude/hooks/auggie-flag-clear.sh; make verify-sync` exits non-zero with `❌ MISSING in .claude/hooks/: auggie-flag-clear.sh`; restore via `make sync-dev`
- Validate AC-1.1, AC-1.2

### Phase 4 — Part 1 verify-sync installer registration section
- Insert `=== Installer Registration ===` section in `Makefile` `verify-sync` target
- Uses `uv run python -c "from superclaude.cli.install_hooks import _FRESHNESS_SCRIPTS; ..."` and `comm` for set comparison
- Smoke-test on clean tree
- Validate AC-1.3 (programmatically tested in Phase 7)

### Phase 5 — Part 3 cross-consistency assertion
- Insert `=== Hooks Cross-Consistency ===` section in `Makefile` `verify-sync` target
- Uses `jq` to extract matcher prefixes from `hooks.json`, `grep -oE` to extract from `auggie-flag-clear.sh` case body, normalize regex/glob trailing wildcards, compare with `[ "$matcher" = "$case" ]`
- Smoke-test that current (post-Part-2) state shows ✅ agreement
- Validate AC-3.1

### Phase 6 — Test file creation
- Create `tests/cli/test_verify_sync_hooks.py` with 7 test scenarios (V1-V7) per spec §9
- Each test uses `subprocess.run(["make", "verify-sync"], ...)` invocation
- V3-V7 require `tmp_path` checkout (copy of relevant files) for mutation tests
- Run `uv run pytest tests/cli/test_verify_sync_hooks.py -v` — all pass
- Validate AC-1.2, AC-1.3, AC-3.2, AC-3.3

### Phase 7 — Aggregate validation & QA gate
- Run `uv run pytest tests/ -v` — full suite passes (AC-A.1)
- Run `make lint` — clean (AC-A.2)
- Run `make verify-sync` — exits 0 (AC-1.1, AC-3.1)
- Run `make verify-sync` AFTER expected-orphan handling: ❌ MISSING report for `.claude/hooks/auggie-bash-gate.sh` is EXPECTED until orphan is resolved per spec §6 — document this in Task Log Phase Findings; do NOT auto-fix
- Spawn rf-qa task-integrity (handled by skill orchestration, not in task file)

### Phase 8 — Completion
- Update task status to 🟢 Done
- Append Task Log summary with: orphan finding, test results, any deferred items

**Granularity note:** Each file edit is its own checklist item. Each smoke-test is its own item. Each test scenario V1-V7 is one or two items (test stub + assertion body). Estimated ~22-28 checklist items across 8 phases.

---

## TEMPLATE_NOTES

- **MDTM template:** `02_mdtm_template_complex_task.md` — multi-phase work with discovery, multiple file edits, validation gates, and testing
- **Reasoning:** The release involves discovery (verify current state), iterative file edits across three files, multiple validation smoke-tests, and a new test file. Template 02's L1-L6 handoff pattern aligns with phase ordering. Template 01 would force batching that violates A3 (Complete Granular Breakdown).
- **Tier reasoning:** Standard tier. Spec is explicit (Scenario A), surface is well-bounded (~155 LOC across 4 files), but multi-phase nature and 7 test scenarios warrant 4 researchers covering inventory/patterns/tests/templates. Not Quick because >5 files involved and test scenarios need cross-checking. Not Deep because no multi-subsystem traversal needed.
- **MDTM features to use:**
  - Per-file checklist items (A3 granularity)
  - Explicit verification commands per item (Verify: ...)
  - Pre-condition / post-condition phases (Phase 1 baseline, Phase 7 aggregate)
  - Acceptance criteria mapping in Phase 6 test items (each V1-V7 scenario annotated with its AC)
  - QA_GATE_REQUIREMENTS: PER_PHASE (smoke-tests after Phase 2/3/4/5, full QA gate at Phase 7)
  - VALIDATION_REQUIREMENTS: `make verify-sync` exit-0, `make lint`, full test suite pass
  - TESTING_REQUIREMENTS: UNIT (new pytest file, ~80 LOC)
  - EXECUTION_CONTEXT_REQUIREMENTS: AUTO (≥3 distinct named source areas — Makefile verify-sync, hooks matcher/script, pytest test harness)

---

## AMBIGUITIES_FOR_USER

None — the release spec is fully explicit. The two open questions (OQ-1 manual end-to-end test, OQ-2 orphan handling) are documented in the spec itself with clear defer-to-maintainer guidance.

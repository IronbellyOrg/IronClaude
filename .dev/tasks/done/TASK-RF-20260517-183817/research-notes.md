# Research Notes: Implement hook-sync-and-matcher-fix release

**Date:** 2026-05-17
**Scenario:** A (Explicit) — release spec provides exact diffs, exact phases, exact acceptance criteria
**Depth Tier:** Standard (4 researchers)
**Track Count:** 1 (release is internally sequenced; bundle ships as single PR)
**Status:** Complete
**Source spec:** `.dev/releases/current/hook-sync-and-matcher-fix/release-spec.md`
**Sibling spec:** `.dev/releases/current/hook-sync-and-matcher-fix/hook-sync-coverage-spec.md` (Part 1 standalone design)

---

## EXISTING_FILES

### Files to MODIFY
| Path | Change | Source spec section |
|---|---|---|
| `src/superclaude/hooks/hooks.json` | Line 60 matcher widened (add `\|mcp__auggie-mcp__.*`) | §4.1 |
| `src/superclaude/hooks/scripts/auggie-flag-clear.sh` | Line 22 case body widened + line 2 comment updated | §4.2 |
| `Makefile` | Add `=== Hooks ===`, `=== Installer Registration ===`, `=== Hooks Cross-Consistency ===` sections to `verify-sync` target | §3, §5 |

### Files to CREATE
| Path | Purpose | Approximate LOC |
|---|---|---|
| `tests/cli/test_verify_sync_hooks.py` | Pytest harness for V1-V7 scenarios | ~80 |

### Read-only reference files (verified during scope discovery)
- `src/superclaude/cli/install_hooks.py` — contains `_FRESHNESS_SCRIPTS` at line 43, iterated at line 178
- `tests/hooks/test_auggie_first.py` — existing pytest harness pattern to mirror
- `tests/cli/test_install_hooks.py` — existing CLI test pattern
- `src/superclaude/hooks/scripts/` — 9 .sh files currently (auggie-flag-clear + 7 freshness + reject-workspace-writes)
- `.claude/hooks/` — 11 .sh files (the 9 src files + session-init.sh + ORPHAN auggie-bash-gate.sh)

### Orphan confirmed
- `.claude/hooks/auggie-bash-gate.sh` exists; no counterpart in `src/superclaude/hooks/scripts/`. Spec §6 says: detection is in scope, resolution is out of scope (user decision after merge).

---

## PATTERNS_AND_CONVENTIONS

### Makefile verify-sync section pattern (Makefile:154-247)
- All sections use shell continuation (`\`) and `drift` flag accumulator
- Forward check loop: `for f in src/superclaude/<type>/*; do ... if [ ! -f ".claude/<type>/$$name" ]; then ❌ MISSING; drift=1; else diff -q; fi; done;`
- Reverse check loop: `for f in .claude/<type>/*; do ... if [ ! -f "src/.../$$name" ]; then ❌ MISSING in src/; drift=1; fi; done;`
- Status symbols: `❌` (missing/error), `⚠️` (differs), `✅` (in sync)
- Section headers: `echo ""; echo "=== <SectionName> ===";`
- Per-file emit: `echo "  ✅ $$name"` or `echo "  ❌ MISSING ..."`
- Final block: `if [ "$$drift" -eq 0 ]; then echo "✅ All components in sync."; else echo "❌ Drift detected..."; exit 1; fi`

### auggie-flag-clear.sh case-body pattern
- Glob match (not regex) in case statement: `mcp__auggie__*|mcp__airis-mcp-gateway__auggie_*)`
- File header comment at line 2 currently mentions only `mcp__auggie__*`; spec §4.2 requires updating to enumerate all 3 prefixes

### hooks.json matcher pattern (hooks.json:60)
- Pipe-separated regex inside `"matcher": "..."` string
- Current: `"mcp__auggie__.*|mcp__airis-mcp-gateway__auggie_.*"`
- After patch: `"mcp__auggie__.*|mcp__auggie-mcp__.*|mcp__airis-mcp-gateway__auggie_.*"`
- Regex uses `.*` (vs glob `*` in the shell script — Part 3 normalizes the difference)

### Test pattern from `tests/hooks/test_auggie_first.py`
- Spec §9 explicitly cites this as the harness to mirror
- Pattern: `subprocess.run([...], capture_output=True, text=True, cwd=repo_root)`
- Assert on `result.returncode` AND on `result.stdout`/`result.stderr` content patterns
- Use `tmp_path` to copy the repo tree before mutating (avoid contaminating the developer's working tree for V3-V6)

### `_FRESHNESS_SCRIPTS` extraction pattern
Spec §3.2 / §4.2 of hook-sync-coverage-spec.md prescribes:
```bash
uv run python -c "from superclaude.cli.install_hooks import _FRESHNESS_SCRIPTS; print('\n'.join(sorted(_FRESHNESS_SCRIPTS)))"
```
Combined with `comm -23` / `comm -13` for set difference.

### Part 3 cross-consistency pattern (release-spec §5.1)
- Use `jq` to extract matcher from hooks.json
- Use `grep -oE` to extract case-body prefixes from auggie-flag-clear.sh
- Normalize: `sed -E 's/\.\*$$//'` (regex) and `sed -E 's/\*$$//'` (glob)
- Compare with `=` after `sort -u`

---

## GAPS_AND_QUESTIONS

1. **Test harness invocation:** Spec recommends Option A (subprocess.run + `make verify-sync`). Researchers need to verify the existing `tests/hooks/test_auggie_first.py` pattern is compatible (signature, fixtures, conftest, etc.).
2. **`tmp_path` mutation for V3/V4:** How does the test mutate `_FRESHNESS_SCRIPTS` without disrupting the live module? Likely via: copy repo → edit `install_hooks.py` in the copy → run `make verify-sync` with `cwd=tmp_path`. Researchers verify this works given that the Makefile invokes `uv run python -c "from superclaude.cli.install_hooks ..."` which imports the INSTALLED module, not the cwd module. **THIS IS A REAL DESIGN GAP** — needs explicit research.
3. **`session-init.sh` handling:** Reverse check must skip `session-init.sh` (lives in `src/superclaude/scripts/`, not `hooks/scripts/`). Spec §3.1 + §4.1 confirm. No additional question.
4. **`freshness-file-changed.sh` handling:** It IS in `_FRESHNESS_SCRIPTS` and IS in src/ and .claude/. Should pass cleanly. No additional question.
5. **Order of phase application:** Spec §10 prescribes Phase 1 (Part 2 patches) → Phase 2 (Part 1 verify-sync) → Phase 3 (Part 3 cross-consistency) → Phase 4 (tests) → Phase 5 (orphan decision) → Phase 6 (final QA). Builder follows verbatim.
6. **`make sync-dev` propagation:** After modifying `src/superclaude/hooks/scripts/auggie-flag-clear.sh`, `make sync-dev` must propagate to `.claude/hooks/auggie-flag-clear.sh`. Standard project workflow.

---

## RECOMMENDED_OUTPUTS

Research files to create (4 total):

1. `research/01-surface-verification.md` — Verify EVERY file:line claim in the release spec is accurate against current master HEAD. Map all 4 modified surfaces precisely.
2. `research/02-makefile-patterns.md` — Extract the exact Makefile verify-sync section conventions; document the shell-continuation, drift-flag, and diff-quotation patterns that the new `=== Hooks ===`, `=== Installer Registration ===`, `=== Hooks Cross-Consistency ===` sections must match.
3. `research/03-test-harness-patterns.md` — Document the `tests/hooks/test_auggie_first.py` pattern (subprocess.run + cwd + tmp_path mutation), AND specifically investigate the `tmp_path` + `_FRESHNESS_SCRIPTS` mutation gap from §GAPS_AND_QUESTIONS #2. Provide an answer the builder can use.
4. `research/04-template-examples.md` — Read MDTM template 02 (PART 1 rules) + check existing task examples for build/test/verify phase structures.

---

## SUGGESTED_PHASES

### Researcher 1 (File Inventory & Surface Verification)
**Topic type:** File Inventory + Doc Cross-Validator (combined — verify spec's file:line claims)
**Scope:**
- `src/superclaude/hooks/hooks.json` (entire file, ~70 LOC)
- `src/superclaude/hooks/scripts/auggie-flag-clear.sh` (entire file, ~33 LOC)
- `Makefile` lines 154-247 (verify-sync target)
- `src/superclaude/cli/install_hooks.py` (line 43 `_FRESHNESS_SCRIPTS`, line 178 iteration)
- `src/superclaude/hooks/scripts/*.sh` (list all 9)
- `.claude/hooks/*.sh` (list all 11; identify orphan)
**Output:** `research/01-surface-verification.md`
**Other researchers cover:** Makefile patterns (R2), test patterns (R3), templates (R4) — focus on what EXISTS where, not what to write

### Researcher 2 (Patterns & Conventions — Makefile)
**Topic type:** Patterns & Conventions
**Scope:** Read all 3 existing verify-sync sub-sections (`=== Skills ===`, `=== Agents ===`, `=== Commands ===`) at Makefile:154-247 and extract the precise shell pattern (shell-continuation, drift accumulator, status symbols, header format, per-file emit format)
**Output:** `research/02-makefile-patterns.md`
**Other researchers cover:** File contents (R1), test patterns (R3), templates (R4)

### Researcher 3 (Test & Verification + `tmp_path` design question)
**Topic type:** Test & Verification
**Scope:**
- Read `tests/hooks/test_auggie_first.py` entire file
- Read `tests/cli/test_install_hooks.py` entire file
- Check `tests/conftest.py` if exists
- Investigate `tmp_path` mutation pattern: how does a test invoke `make verify-sync` with `cwd=tmp_path` such that the Python `uv run python -c "from superclaude.cli.install_hooks import _FRESHNESS_SCRIPTS"` call reads the MUTATED `install_hooks.py` from the tmp checkout, not the installed package? (This is the GAP from §GAPS_AND_QUESTIONS #2.)
- Document V1-V7 test scenarios with concrete setup/teardown for each
**Output:** `research/03-test-harness-patterns.md`
**Other researchers cover:** File contents (R1), Makefile patterns (R2), templates (R4)

### Researcher 4 (Template & Examples)
**Topic type:** Template & Examples
**Scope:**
- Read `.claude/templates/workflow/02_mdtm_template_complex_task.md` PART 1 (all rules)
- Check `.dev/tasks/to-do/` and `.dev/tasks/done/` for similar prior task examples (Makefile changes, hook changes, pytest harness creation)
- Note: rule A3 (Complete Granular Breakdown) — each phase from spec §10 gets distinct items; each Makefile section is its own item; each test scenario V1-V7 is its own sub-item or grouped reasonably
**Output:** `research/04-template-examples.md`
**Other researchers cover:** File contents (R1), Makefile patterns (R2), test patterns (R3)

---

## TEMPLATE_NOTES

### Template selection: **Template 02 (Complex)**
**Reasoning:** Multi-phase work with build → smoke-test → build → smoke-test → tests → QA gate sequencing. Conditional flow at Phase 5 (orphan resolution — user decision, may be deferred). Final QA gate (Phase 6).

### Tier selection: **Standard (4 researchers)**
**Reasoning:** Surface is small (~4 files, ~155 LOC) and spec is extremely explicit (Scenario A). But 4 researchers needed for: surface verification, pattern extraction (Makefile structure), test harness design (with a real design gap to resolve), and template/example context. Could downgrade to Quick (3 researchers), but the `tmp_path` design question makes the test harness research non-trivial.

### MDTM features the generated task file should use
- **Rule A3 (Complete Granular Breakdown):** Individual items per Makefile section (3 sections), per file patch (3 surface patches), per test scenario (7 scenarios → can group as a single test-file-creation item but listing scenarios as a checklist within the item is fine), per phase smoke-test (sync-dev propagation + verify-sync exit checks).
- **Rule B2 (Self-contained items):** Every item must include the exact diff or exact section content from the spec (paste-ready). No "see spec" references.
- **QA gates:** PER_PHASE (release spec §10 Phase 6 explicitly calls out final QA gate; we'll also add a structural sanity check after Makefile edits to validate JSON/shell syntax before moving to next phase).
- **Validation:** `make lint` + `make verify-sync` runs after each phase, `uv run pytest tests/ -v` for the full suite at the end.

### BUILD_REQUEST fields
- `GOAL`: "Implement the hook-sync-and-matcher-fix release: Part 1 (Makefile verify-sync hook coverage), Part 2 (auggie-flag-clear matcher widening), Part 3 (verify-sync cross-consistency assertion), plus tests/cli/test_verify_sync_hooks.py."
- `WHY`: "Two confirmed bugs on master (verified 2026-05-17T18:21Z): (A) PostToolUse matcher misses `mcp__auggie-mcp__*` prefix actually used by the auggie-mcp server, causing v2.1 sticky-clear failures; (B) `make verify-sync` does not check hooks, allowing silent end-user-install divergence (already happened — orphan `.claude/hooks/auggie-bash-gate.sh` exists)."
- `TEMPLATE`: 02
- `QA_GATE_REQUIREMENTS`: PER_PHASE
- `VALIDATION_REQUIREMENTS`: "make verify-sync passes; make lint clean; jq parses hooks.json cleanly; shellcheck-style sanity on modified .sh"
- `TESTING_REQUIREMENTS`: UNIT + INTEGRATION (pytest harness invoking `make verify-sync` via subprocess; this is both a unit test of the new Makefile sections and an integration test of the verify-sync pipeline)
- `EXECUTION_CONTEXT_REQUIREMENTS`: AUTO (≥3 distinct source areas: hooks scripts, Makefile build system, pytest test harness — rollup signal is present)

---

## AMBIGUITIES_FOR_USER

1. **Phase 5 (orphan handling)** is explicitly documented as a USER DECISION in the spec §6. The generated task file should encode this as a **manual decision point** (not an automated phase) — the executor pauses, presents the three options (delete / re-add src / gitignore-with-rationale), and waits for user input. Default behavior if user opts not to decide during execution: leave the orphan present, document it in Open Questions, and proceed to Phase 6 with the expectation that `make verify-sync` will fail on the orphan check (this is the intended detection behavior of Part 1).

2. **Test option choice:** Spec §9 recommends Option A (subprocess.run + make verify-sync). Builder should default to Option A. If the test harness research (R3) discovers that the `tmp_path` + `_FRESHNESS_SCRIPTS` mutation pattern is unworkable, the builder may document this in the task file's Open Questions and propose Option B (extract verify_sync logic to a Python module) for user consideration.

Otherwise intent is clear: implement the release verbatim per the spec.

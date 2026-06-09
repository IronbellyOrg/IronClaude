# Research: Gap-Fill Resolutions (post research-gate)

**Topic type:** Gap-fill / design resolution
**Status:** Complete
**Date:** 2026-06-09
**Origin:** A.8 research gate — gap-detection lens returned FAIL with 3 CRITICAL + 1 MEDIUM findings (all with file:line evidence). These are resolved below and become mandatory builder requirements.

---

## DECISION 1 (resolves GAP-2 + GAP-3) — `_authoritative_specs_block` MUST guard each path with `is_file()`

**Problem:** `_authoritative_specs_block` is invoked with spec paths sourced from the persisted `parsed-request.json` `SPECS` array (`prompts.py:247-249`, `:919`; bound by `_bind_specs` at `executor.py:1437`), NOT from the Click-validated `config.spec_files`. On **resume**, `config.spec_files == []` and Click never re-validates; `_bind_specs` deliberately tolerates missing files (`executor.py:1357-1360`, binds `size=0`). An unguarded `_read_file` (`prompts.py:42-47`) over a missing/stale/moved path raises bare `FileNotFoundError` inside `build_scope_discovery_prompt`; the executor only catches `MissingArtifactError` → uncaught crash on the SAME `scope-discovery` step. That would trade the token crash for a file-read crash.

**Resolution — required behavior for the new `_authoritative_specs_block` body:**
- Keep the empty-input contract: `if not spec_paths: return ""` (byte-identical no-spec prompts).
- For each path `p` in `spec_paths`:
  - If `Path(p).is_file()` → emit a per-spec header + `_read_file(Path(p))` content (50 KB cap + `_TRUNCATION_MARKER` reused verbatim).
  - Else (missing/stale/moved) → **fall back to the current path-only line** (just list `- {p}`), never call `_read_file` on it.
- Preserve the imperative wording substrings `AUTHORITATIVE SPECIFICATIONS` and `MUST Read each one IN FULL` (existing tests assert these; also serves as the truncation/missing-file fallback instruction).

**Why this is correct:**
- Never raises `FileNotFoundError` → no resume crash (GAP-2 closed).
- Missing/synthetic paths still render as a path → the existing injection tests that bind non-existent paths (`/abs/SPEC_A.md` etc.) keep passing their "path appears" assertions (GAP-3 closed) without migrating them.
- Real specs (the normal run) get content inlined → realizes Option B's guarantee, token-free.

## DECISION 2 (resolves GAP-1 + GAP-3, test plan) — test changes

- **Invert/replace** `tests/cli/prd/test_spec_flag.py::TestSpecFileAttach` (:459-515): it asserts `--file` IS emitted and references the removed `_build_file_args`. Replace with assertions that the built argv / `extra_args` contains **no** `--file` for scope-discovery & investigation with `spec_files` set. (If `_build_file_args` is deleted, remove the `== []` cases that name the symbol.)
- **Keep green (no migration needed):** the prompt-injection tests that bind non-existent paths and assert the path appears — Decision 1's `is_file()` fallback keeps them valid. Do NOT delete them.
- **Add new tests** (`test_spec_flag.py` and/or `test_prompts.py`):
  1. Real `tmp_path` spec file with a UNIQUE_MARKER → `_authoritative_specs_block([str(p)])` output contains the marker (content inlined) AND `AUTHORITATIVE SPECIFICATIONS`.
  2. >50 KB `tmp_path` spec → output contains `_TRUNCATION_MARKER`.
  3. Missing path → output contains the path string and does NOT raise.
  4. Empty-input parity: `_authoritative_specs_block(None)` and `([])` return `""` (existing lock at `:310-312` stays).
- **Leave intact:** `tests/pipeline/test_process.py:78-81` tests the BASE `ClaudeProcess` `--file` support — out of scope, must NOT be touched.

## DECISION 3 (resolves GAP-4) — verify before deleting `_PHASE_ALLOWED_REFS`

- All current PRD refs are <50 KB (largest `prd/refs/agent-prompts.md` = 22,855 B), so the refs `--file` branch (`process.py:199`) is dead today — no current ref is delivered via `--file`.
- Before deleting `_PHASE_ALLOWED_REFS`: grep `prompts.py` to confirm each ref consumed by a step is inlined by literal name (e.g. `_read_file(config.skill_refs_dir / "build-request-template.md")` at `:514-518`). Document that a FUTURE >50 KB ref would be inlined truncated-at-50 KB with `_TRUNCATION_MARKER` (documented limitation; not a regression — matches the cap the prompt builder already applies).

## DECISION 4 (resolves GAP-5) — `extra_args` removal is safe

- The sole `PrdClaudeProcess` constructor call is `executor.py:714` and passes NO `extra_args`. The public `__init__` has no `extra_args` parameter (it builds `file_args` internally). Removing the internal `_build_file_args` call + `extra_args=file_args` (passing nothing, base defaults to `[]`) breaks no caller.

## NET

Research is now complete and builder-ready. Option B is retained but HARDENED with the `is_file()` guard (Decision 1), which is what makes it strictly better than Option A (Option A relies on the agent choosing to Read; guarded Option B inlines real content AND never crashes AND keeps fake-path tests green). Spec updated to match (§5.2, §6, §7).

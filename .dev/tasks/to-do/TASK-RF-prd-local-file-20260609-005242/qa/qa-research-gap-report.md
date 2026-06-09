# QA Research Gap Report — PRD `--file` local-path fix

**Lens:** ADVERSARIAL gap-detection (what would break the build that the research/spec MISSED)
**Spec:** `.dev/specs/prd-local-file-delivery-fix.md`
**Research:** `…/research/{01,02,03}.md` + `research-notes.md`
**Date:** 2026-06-09
**Mode:** read-only, no team tools

---

## Summary of verdict

The spec/research correctly identify the defect and the two `--file` emission
sites. **However, several builder-critical facts are missing or wrong**, the most
serious of which would cause **5 existing unit tests to fail** and, under the
RECOMMENDED Option B, **re-introduce a `FileNotFoundError` crash on the exact
prompt-build path the fix is meant to harden** — the missing-spec-file risk is
NOT covered by upstream Click validation in the way the spec implies.

---

## GAP-1 — Existing tests assert `--file` IS present; the spec never mentions them (BLOCKER)

**Severity: CRITICAL — the fix as specified leaves the test suite red.**

`tests/cli/prd/test_spec_flag.py` class `TestSpecFileAttach` directly tests
`PrdClaudeProcess._build_file_args` and asserts `--file` **is emitted**:

- `:485-487` — `assert args == ["--file", str(a), "--file", str(b)]`
- `:495-497` — `assert "--file" in args` (investigation-3 normalization)
- `:506` / `:510` / `:515` — `== []` cases (these survive, but the file as a whole won't import-collect cleanly if the method is deleted)

The spec §5.1 offers "remove the method … OR retain it returning `[]`." **Either
choice breaks these tests:**
- Delete the method → `:485/:495` raise `AttributeError` (no `_build_file_args`).
- Keep it returning `[]` → `:487` `assert args == ["--file", …]` and `:497`
  `assert "--file" in args` **fail** (now `[]`).

The spec's §5.3 / §7.4 grep-guard is scoped to `src/superclaude/cli/prd/` only and
the test plan §7.1 only asserts `--file` *absence*. **No task step updates or
deletes `TestSpecFileAttach`.** The research notes (`01-process-py-file-args.md`,
GAPS section) flagged "locate existing test" but the spec did not act on the
finding — it must explicitly **delete or rewrite `TestSpecFileAttach`
(`test_spec_flag.py:460-516`)** to assert no-`--file` + content-inline.

**File to check / fix:** `tests/cli/prd/test_spec_flag.py:460-516`.

---

## GAP-2 — Option B re-introduces a `FileNotFoundError` crash; upstream Click `exists=True` does NOT protect the prompt-build path (BLOCKER)

**Severity: CRITICAL — the recommended option creates a NEW crash on the SAME path the fix targets.**

This is the most dangerous gap and the spec gets the causality backwards.

### The path-source mismatch the spec missed
The spec (§5.2) says Option B will `_read_file(Path(p))` for "each spec path."
But the paths the prompt builder actually iterates do **NOT** come from
`config.spec_files` (the Click-validated input). They come from
**`parsed-request.json`'s persisted `SPECS` array**:

- scope-discovery caller — `prompts.py:247-249`:
  `_authoritative_specs_block([s.get("path","") for s in (parsed.get("SPECS") or [])])`
- investigation caller — `prompts.py:919`: `_authoritative_specs_block(spec_paths)` where `spec_paths` is derived from the persisted SPECS (`executor.py:1437-1438` `_resolved_spec_paths`).

### Why Click `exists=True` does NOT guarantee these files exist at read time
The spec's §2 evidence table and config.py (`config.py:138-142`) note Click
enforces `Path(exists=True, dir_okay=False)` **at invocation time only**. But:

1. **Resume path has NO Click validation at all.** On `prd resume`, `--spec` is
   not re-passed; `config.spec_files == []` (proven by `test_spec_flag.py:451-453`).
   The SPECS paths are read back from the persisted artifact (`executor.py:1437`).
   A spec file deleted/moved/renamed **between the original run and the resume**
   yields a path string in `SPECS` that no longer exists — Click never re-checks it.
2. **TOCTOU even on a fresh run.** Click checks existence at CLI parse; prompt
   build happens many steps later. A file removed in between is not re-validated.
3. **`_bind_specs` deliberately tolerates missing files** — `executor.py:1357-1360`
   catches `OSError` on `stat()` and binds `size=0` anyway. So a missing spec is
   *expected to flow through* into `SPECS` with a path, by design.

### The crash `_read_file` is unguarded
`prompts.py:42-47` `_read_file` calls `path.read_text(...)` with **no
`try/except`**. Under Option B, a non-existent SPECS path → `FileNotFoundError`
raised **inside `build_scope_discovery_prompt`** → propagates up through
`executor._build_prompt` (the `try` at `executor.py:693` only catches
`MissingArtifactError`, NOT bare `FileNotFoundError`) → **unhandled pipeline
crash at the exact `scope-discovery` step the fix exists to stop crashing.**

This trades a token crash for a file-read crash on the same step.

**Required, but absent from spec:** Option B's upgraded `_authoritative_specs_block`
MUST guard each read (try/except → fall back to paths-only line for that spec, or
skip). The test plan §7.2 only tests the happy path + truncation; it has **no
missing-file case**. Add one.

**Files to check:** `prompts.py:42-47` (`_read_file`, unguarded),
`prompts.py:120-138` (block), `prompts.py:247-249` + `:919` (path source =
persisted SPECS, not config.spec_files), `executor.py:1326-1382` (`_bind_specs`
tolerates missing), `executor.py:1437-1438`, `config.py:138-142` (Click only at
parse time), `executor.py:688-705` (only catches `MissingArtifactError`).

---

## GAP-3 — Option B breaks the prompt-injection tests that use non-existent `/abs/...` paths (BLOCKER)

**Severity: CRITICAL — direct corollary of GAP-2, independently fails ≥4 tests.**

The existing prompt-injection tests build a *real* scope-discovery prompt from a
`parsed-request.json` whose `SPECS` paths are **synthetic non-existent paths**:

- `test_spec_flag.py:255-265` — `{"path": "/abs/SPEC_A.md"}`, `{"path": "/abs/SPEC_B.md"}` → `build_scope_discovery_prompt(...)`; asserts the **paths** appear and "MUST Read each one IN FULL".
- `:327-328`, `:363-364`, `:455-456` — same pattern, `/abs/SPEC.md`.
- `:430-456` (`TestResumeCarriesSpecs`) — resume with persisted `/abs/SPEC.md`, `spec_files == []`, builds prompt, asserts path present.

Under Option B, every one of these calls `_read_file(Path("/abs/SPEC_A.md"))` on a
path that does not exist → `FileNotFoundError` → **test errors**, not just assertion
failures. These tests also encode the **paths-only contract** (`assert "/abs/...md"
in prompt`) that Option B changes — even with a read-guard they need updating, and
the spec's §6 claim "callers at :247 and :919 unchanged" is true for the *call* but
the **behavioral contract these tests assert is silently changed**.

**File to check:** `tests/cli/prd/test_spec_flag.py:250-266, 320-365, 425-457`.

---

## GAP-4 — `>50KB ref` truncation claim: refs `--file` branch is dead, but the spec's "future >50KB ref inlined truncated" guarantee is only TRUE if the ref is in `_PHASE_ALLOWED_REFS` AND inlined by name (MEDIUM)

**Severity: MEDIUM — no current >50KB ref exists, so no live data loss, but the spec's forward-compat reasoning is incomplete.**

Findings on the "would a >50KB ref now be truncated silently?" question:

- **No current ref is >50KB.** Measured the actual `skill_refs_dir` files:
  `prd/refs/agent-prompts.md` = 22,855 B (largest), `operational-guidance.md` =
  9,114 B, `validation-checklists.md` = 9,545 B. The spec's "<50KB" claim is
  **confirmed**. The refs `--file` branch (`process.py:198-199`) is dead in
  practice — removing it loses nothing today.
- **BUT** the spec §6 says any future >50KB ref "is inlined truncated-at-50KB by
  the prompt builder." This is only true if that ref name is **explicitly inlined
  by name** in `prompts.py` (e.g. the `:514-518` literal-name pattern the research
  cites). A ref that was *only* reachable via the `_PHASE_ALLOWED_REFS` `--file`
  branch and is **not** inlined by literal name in the prompt builder would, after
  this change, **reach the agent through neither path** → silent total loss, worse
  than truncation. The spec asserts equivalence without verifying that every entry
  in `_PHASE_ALLOWED_REFS` (`process.py:95-113`) has a corresponding literal inline
  call. **The task must grep that the refs in `_PHASE_ALLOWED_REFS` are each inlined
  by name before deleting the map**, not just assume it.

**Files to check:** `process.py:95-113` (`_PHASE_ALLOWED_REFS`),
`prompts.py:~514` (literal-name ref inlining) — verify 1:1 coverage of the map's refs.

---

## GAP-5 — `extra_args` plumbing removal: signature/caller impact (LOW — safe, but one nuance)

**Severity: LOW — no external caller passes `extra_args` to `PrdClaudeProcess`; removal is safe.**

- The **only** constructor of `PrdClaudeProcess` is `executor.py:714`, and it does
  **not** pass `extra_args` (it passes `config/step_id/prompt/output_file/error_file/
  timeout_seconds`). `PrdClaudeProcess.__init__` (`process.py:138-167`) builds
  `file_args` internally and forwards as `extra_args=` to the base. **Removing the
  internal `file_args`/`extra_args=` wiring does not change the public
  `PrdClaudeProcess.__init__` signature** (it has no `extra_args` parameter) — so no
  caller breaks. Confirmed via grep: zero external `extra_args=` passers to
  `PrdClaudeProcess`.
- The base `ClaudeProcess.__init__` keeps `extra_args` (`pipeline/process.py:48`)
  and `build_command` keeps `cmd.extend(self.extra_args)` (`:94`) — unchanged and
  still used by sibling pipelines (`roadmap/tasklist/validate` executors,
  `eval/claude_process.py`, `cli_portify`). **Do not touch the base.** The spec
  correctly scopes to `prd/` only; flag here only to confirm the base is shared and
  must NOT be edited.
- Nuance: `tests/pipeline/test_process.py:78-81` asserts `extra_args=["--file",
  "/tmp/spec.md"]` → `"--file" in cmd`. This tests the **base** class mechanism
  (legitimately — the base still supports `--file` for cloud use), is **out of
  scope**, and must be **left alone**. A naive "delete all `--file` test asserts"
  cleanup would wrongly break it. Call this out so the implementer doesn't over-reach.

**Files to check:** `executor.py:714` (sole caller),
`pipeline/process.py:48,63,94` (base — leave intact),
`tests/pipeline/test_process.py:73-81` (base test — leave intact).

---

## GAP-6 — Stale GAP-003 docstrings/comments (LOW — spec covers it, scope note)

**Severity: LOW — spec §5.1 already calls for docstring updates; this confirms the full set.**

`GAP-003` (the `--file` arg-scoping feature) references to update/remove:
- `process.py:11` (module docstring), `:90` (section comment), `:133` (class
  docstring), `:174` (method docstring).

The other `GAP-003` hits found in the repo
(`tests/cli_portify/test_brainstorm_gaps.py:115`, `.dev/test-fixtures/results/…`)
are an **unrelated coincidence** — a different "GAP-003 = admin audit log API" in
fixture data. Do **not** touch those. Confirmed no cross-file code dependency on
the PRD GAP-003 label.

**Files to check:** `process.py:11,90,133,174` (update); fixtures — ignore.

---

## GAP-7 — No e2e/integration test asserts `--file` present in the live argv (LOW — informational)

**Severity: LOW — confirms no hidden integration failure beyond the unit tests already flagged.**

Searched `tests/cli/prd/test_integration.py`, `test_cli_smoke.py` and the broader
tree. The only assertions that `--file` IS present are:
- `tests/cli/prd/test_spec_flag.py` (GAP-1, in-scope, must fix), and
- `tests/pipeline/test_process.py` (base class, GAP-5, out-of-scope, leave).

No PRD integration/e2e test asserts a live `--file` in the spawned command, so
beyond GAP-1 there is no additional hidden red test from the `--file` removal.
(The acceptance test §7.5 / §8 — headless run with no session token — is a manual
repro against the octodive repo and is not an automated assertion.)

---

## Cross-cutting gap the research/spec under-weighted

The spec frames Option B as strictly safer than Option A ("guaranteed in-context").
In reality Option B **adds a new failure mode** (GAP-2/GAP-3: unguarded
`_read_file` on persisted, possibly-stale, possibly-synthetic SPECS paths) on the
**same `scope-discovery` step** the fix is meant to stabilize, and breaks **5+
existing tests** (GAP-1, GAP-3). Option A (paths-only, the smaller diff) does
**none** of this — it touches no read path and keeps the existing prompt contract,
so the GAP-1 `TestSpecFileAttach` deletions are the only test churn. The
adversarial read is: **the spec's risk comparison is inverted for the test/crash
surface.** If Option B is kept, the read MUST be guarded and the prompt-injection
tests MUST be migrated from "path present" to "content present, missing-file
falls back to path."

---

## Builder checklist of MISSED items (must be added to the task)

1. Delete/rewrite `TestSpecFileAttach` (`test_spec_flag.py:460-516`) — asserts `--file` present. (GAP-1)
2. Guard `_read_file`/`_authoritative_specs_block` against missing SPECS paths; add a missing-file unit test. (GAP-2)
3. Migrate prompt-injection tests using non-existent `/abs/...` SPECS paths (`test_spec_flag.py:250-457`) to Option B's content/fallback contract — they currently build real prompts and will raise `FileNotFoundError`. (GAP-3)
4. Verify every `_PHASE_ALLOWED_REFS` entry is inlined by literal name in `prompts.py` before deleting the map (no silent total loss for a future >50KB ref). (GAP-4)
5. Do NOT edit base `pipeline/process.py` or `tests/pipeline/test_process.py:73-81` (legit base `--file` support). (GAP-5)
6. Recognize SPECS path source is `parsed-request.json`, not `config.spec_files`; Click `exists=True` does NOT cover resume/TOCTOU. (GAP-2 root)

---

VERDICT: FAIL

# Adversarial QA Report -- Data Flow & Runtime Behavior (Agent 4)

**Date:** 2026-03-28
**Scope:** Trace actual data flow through TDD+PRD pipeline at runtime
**Fix authorization:** REPORT ONLY

---

## Findings

### DF-01: State file records `input_type: "auto"` instead of resolved type

**Severity:** IMPORTANT
**Location:** `.dev/test-fixtures/results/test1-tdd-prd/.roadmap-state.json:6`

The state file from the actual E2E run records `"input_type": "auto"` (line 6). However, `_build_steps()` at `executor.py:858-859` creates a new config via `dataclasses.replace(config, input_type=effective_input_type)` to store the resolved type. The issue is that `_build_steps()` returns a `list[Step]` -- it does NOT return the updated config. The caller `execute_roadmap()` at line 1819 calls `steps = _build_steps(config)` but the original `config` object (still with `input_type="auto"`) is what gets passed to `_save_state(config, results)` at line 1842.

The `dataclasses.replace()` inside `_build_steps()` creates a LOCAL copy that is never propagated back. This means:
1. The state file always records "auto" for auto-detected inputs
2. The tasklist auto-wire TDD fallback at `tasklist/commands.py:132` checks `state.get("input_type") == "tdd"` -- this condition will NEVER be true for auto-detected TDD inputs because the state file says "auto"
3. Downstream consumers reading the state file cannot determine what type was actually detected

**Evidence:** The E2E test fixture state file at `.dev/test-fixtures/results/test1-tdd-prd/.roadmap-state.json` line 6 shows `"input_type": "auto"` despite the TDD being auto-detected (the extraction output contains TDD-specific sections like "Data Models and Interfaces" confirming TDD extraction was used).

**Required Fix:** `_build_steps()` must either (a) return the updated config alongside steps, or (b) mutate `config.input_type` in place before returning, or (c) `execute_roadmap()` must resolve auto-detection before calling `_build_steps()` and pass the resolved config.

---

### DF-02: `_embed_inputs` labels files by path only -- no semantic role markers

**Severity:** IMPORTANT
**Location:** `src/superclaude/cli/roadmap/executor.py:134-147`

`_embed_inputs()` wraps each file as:
```
# /path/to/file.md
\`\`\`
<content>
\`\`\`
```

When the generate step embeds `[extraction.md, prd_file]`, the LLM receives two fenced blocks labeled only by filesystem path. The prompt text says "A Product Requirements Document (PRD) is included in the inputs" but provides no explicit marker (e.g., `<!-- ROLE: PRD -->` or `# [PRD] /path/to/prd.md`) that definitively connects a specific embedded block to its semantic role.

For simple cases where one file is named `prd-user-auth.md`, the LLM can infer the role from the filename. But if files have opaque names (e.g., `spec-v3.2.md` used as a PRD alongside `spec-v3.1.md` as the primary spec), the LLM has no reliable way to distinguish which embedded content is the primary input vs. supplementary.

The prompt blocks (e.g., `build_generate_prompt` at `prompts.py:388-404`) reference "the PRD" but never say "the PRD content is the second embedded input" or tag which block is which.

**Required Fix:** Modify `_embed_inputs()` to accept optional role labels per input, or add role tags to the fenced block headers (e.g., `# [PRIMARY SPEC] /path/to/spec.md`, `# [SUPPLEMENTARY PRD] /path/to/prd.md`).

---

### DF-03: Score step prompt exceeds `_EMBED_SIZE_LIMIT` with real test data

**Severity:** IMPORTANT
**Location:** `src/superclaude/cli/roadmap/executor.py:964-971`

The score step embeds `[debate_file, roadmap_a, roadmap_b, prd_file]`. Using the actual E2E test fixture file sizes:
- debate-transcript.md: 18,076 bytes
- roadmap-opus-architect.md: 24,619 bytes
- roadmap-haiku-architect.md: 72,778 bytes
- test-prd-user-auth.md: 19,619 bytes
- Prompt template overhead: ~4,096 bytes
- **Total: ~139,188 bytes (135.9 KB)**

`_EMBED_SIZE_LIMIT` is 122,880 bytes (120 KB). The score step exceeds this by ~16 KB with real data.

At `executor.py:512-519`, the code logs a warning but proceeds anyway:
```python
if len(composed.encode("utf-8")) > _EMBED_SIZE_LIMIT:
    _log.warning("Step '%s': composed prompt exceeds %d bytes; embedding inline anyway ...")
```

On macOS, `ARG_MAX` is 1 MB (vs. Linux's per-argument `MAX_ARG_STRLEN` of 128 KB), so the 140 KB prompt will work on macOS. But the `_MAX_ARG_STRLEN` constant at line 123 is documented as "Linux kernel compile-time constant" -- on Linux, a single argument >128 KB will cause `E2BIG` from `execve()`. The warning-and-proceed strategy is correct for macOS but the pipeline will silently fail on Linux with a subprocess error.

**Evidence:** Calculated from actual file sizes in `.dev/test-fixtures/results/test1-tdd-prd/`. The test `test_prompt_plus_embedded_exceeds_limit` at `tests/roadmap/test_file_passing.py:160` verifies the warning is logged but does not test on Linux.

**Required Fix:** For Linux deployments, implement a file-based prompt injection fallback (e.g., write prompt to a temp file and pass via stdin) when composed size exceeds `_MAX_ARG_STRLEN`. Document the macOS vs. Linux behavioral difference.

---

### DF-04: `_embed_inputs` does not handle empty files or binary files

**Severity:** MINOR
**Location:** `src/superclaude/cli/roadmap/executor.py:144-146`

`_embed_inputs()` calls `Path(p).read_text(encoding="utf-8")` with no protection against:
1. **Empty files (0 bytes):** An empty PRD file will produce a fenced block with no content: `# /path/to/prd.md\n\`\`\`\n\n\`\`\``. This wastes prompt space and the LLM will see "PRD is included in the inputs" but find an empty block, potentially hallucinating PRD content.
2. **Binary files:** If `--prd-file` points to a binary file (e.g., a PDF), `read_text(encoding="utf-8")` will either raise `UnicodeDecodeError` (not caught here, unlike `detect_input_type` at line 73 which uses `errors="replace"`) or produce garbled text.

`detect_input_type()` at line 72 uses `errors="replace"` for resilience, but `_embed_inputs()` does not.

**Required Fix:** Add a check for empty files (skip or warn) and catch `UnicodeDecodeError` in `_embed_inputs()` with a user-facing error message.

---

### DF-05: `--resume` with `--prd-file` does not override state-restored `prd_file`

**Severity:** IMPORTANT
**Location:** `src/superclaude/cli/roadmap/executor.py:1755-1763`

In `_restore_from_state()` at lines 1755-1763, the PRD file is auto-wired from state only when `config.prd_file is None`. Since `commands.py:195` calls `prd_file.resolve() if prd_file is not None else None`, an explicit `--prd-file` on the CLI will set `config.prd_file` before `_restore_from_state()` runs, correctly preventing the override.

However, there is an asymmetry: `_restore_from_state()` checks `config.tdd_file is None` and `config.prd_file is None` to decide whether to auto-wire. But there is NO `prd_explicit` boolean passed (unlike `agents_explicit` and `depth_explicit`). This means if a user runs:
1. `superclaude roadmap run tdd.md --prd-file prd-v1.md` (original run)
2. `superclaude roadmap run tdd.md --resume` (resume without --prd-file)

On step 2, `config.prd_file` is `None` (user did not pass it), so `_restore_from_state()` auto-wires from state. This is the DESIRED behavior. But there is no mechanism to explicitly UN-wire a PRD file on resume. If the user wants to resume WITHOUT PRD enrichment (e.g., they realized the PRD was wrong), they cannot do so -- `--prd-file` has no `--no-prd-file` counterpart.

**Required Fix:** Add a `--no-prd-file` flag (or `--prd-file ""`) to explicitly disable PRD enrichment on resume, preventing auto-wire from state.

---

### DF-06: `_save_state` writes state only AFTER all steps complete or on failure

**Severity:** MINOR
**Location:** `src/superclaude/cli/roadmap/executor.py:1842`

`_save_state(config, results)` is called once at line 1842, AFTER `execute_pipeline()` returns. The state file is NOT written incrementally after each step. If the pipeline crashes (e.g., Python process killed, OOM, power failure) at step 5, the state file from a previous run persists unchanged. On `--resume`, the pipeline will re-evaluate gates against the stale state file's output paths.

This is actually somewhat safe because `_apply_resume` at line 2310-2331 re-checks gates on disk rather than trusting state status values. But the `state_paths` lookup (line 2328-2331) uses recorded output paths from the stale state, which may not include outputs from the crashed run's successfully completed steps.

In the actual E2E fixture, the state file shows `anti-instinct: FAIL` but `wiring-verification: PASS`. Since anti-instinct has `retry_limit=0`, a resume would skip it. But if the crash happened mid-merge (step 6), the stale state would show merge as PASS from a previous run, and resume would skip it -- even though the new extraction (step 1) may have produced different requirements.

**Evidence:** The `dirty_outputs` tracking in `_apply_resume` (line 2335) mitigates this for dependency chains -- if extract re-runs, its output is dirty, causing downstream steps to re-run. But this only works if the stale state correctly reflects the last successful extract. If extract succeeded in the crashed run but state was never written, resume uses the old state's extract and incorrectly skips re-running extract.

**Required Fix:** Write state incrementally after each step passes, or implement a WAL (write-ahead log) pattern.

---

### DF-07: Merge step does NOT receive PRD file as input

**Severity:** IMPORTANT
**Location:** `src/superclaude/cli/roadmap/executor.py:974-982`, `src/superclaude/cli/roadmap/prompts.py:505-534`

The merge step at `executor.py:974-982` assembles inputs as:
```python
inputs=[score_file, roadmap_a, roadmap_b, debate_file]
```

No `prd_file` is included. The `build_merge_prompt()` function at `prompts.py:505-534` also has no `prd_file` parameter and no PRD supplementary block.

This means the merge step -- which produces the final `roadmap.md` -- cannot directly reference PRD content. It merges the two roadmap variants (which themselves were PRD-informed) but has no access to PRD content for its own synthesis decisions.

Compare this to the score step (`executor.py:965-971`) which includes `prd_file` in inputs and `prompts.py:488-499` which adds PRD scoring dimensions. The merge step is the only step after generate that lacks PRD inputs despite being the step that produces the final artifact.

This is a design gap: if the score step identifies PRD-specific improvements from the non-base variant (e.g., "Variant B better addresses persona coverage"), the merge step has no PRD context to implement those improvements.

**Required Fix:** Add `prd_file` parameter to `build_merge_prompt()` and include `config.prd_file` in the merge step's `inputs` list, or document this as an intentional design decision (PRD influence flows indirectly through the variants).

---

### DF-08: PRD prompt blocks reference section numbers (S7, S12, S17, S19) that may not exist in the actual PRD

**Severity:** MINOR
**Location:** `src/superclaude/cli/roadmap/prompts.py:160-179, 388-404, 488-499, 618-635, 745-762`

Every PRD supplementary block references hardcoded section numbers: "the PRD's Success Metrics section (S19)", "User Personas section (S7)", "Scope Definition section (S12)", "Legal & Compliance section (S17)", "JTBD section (S6)", "Customer Journey Map (S22)", "Error Handling & Edge Cases section (S23)".

These section numbers assume a specific PRD template. If the user provides a PRD that uses different section numbering or doesn't have these sections at all, the LLM will either:
1. Search for non-existent sections and produce nothing
2. Hallucinate content for missing sections
3. Map to wrong sections (e.g., S7 in their PRD might be "Market Analysis", not "User Personas")

The test fixture PRD (`test-prd-user-auth.md`) appears to follow the expected template, so this works in testing. But the prompts should gracefully handle PRDs with different structures.

**Evidence:** The extraction output at `.dev/test-fixtures/results/test1-tdd-prd/extraction.md` does successfully reference PRD sections (e.g., "PRD S17", "PRD S7", "PRD S19"), confirming the LLM found these sections in the test fixture. But this is not guaranteed for arbitrary PRD files.

**Required Fix:** Rewrite PRD prompt blocks to reference section NAMES rather than numbers (e.g., "the PRD's success metrics or KPI section" instead of "the PRD's Success Metrics section (S19)"), or add a note: "If the PRD does not have a section matching this description, skip this extraction item."

---

### DF-09: Tasklist auto-wire TDD fallback is unreachable due to DF-01

**Severity:** IMPORTANT
**Location:** `src/superclaude/cli/tasklist/commands.py:132-144`

The code at `tasklist/commands.py:132` checks:
```python
elif state.get("input_type") == "tdd":
```

As documented in DF-01, the state file always records `"input_type": "auto"` for auto-detected inputs. This means the TDD fallback path (lines 133-144), which correctly falls back to `spec_file` as the TDD when the primary input was a TDD, is dead code for the most common case (auto-detection).

Only users who explicitly pass `--input-type tdd` will trigger this fallback. Users who rely on auto-detection (the default and recommended path) will have their tasklist validation run without TDD context even though the primary input was a TDD.

**Evidence:** The state file at `.dev/test-fixtures/results/test1-tdd-prd/.roadmap-state.json` shows `"input_type": "auto"` while the pipeline clearly ran TDD extraction (extraction.md contains TDD-specific sections). The tasklist-fidelity.md in the same directory was generated without TDD context.

**Required Fix:** Fix DF-01 (propagate resolved input_type to state). As a defense-in-depth measure, also check `state.get("input_type") in ("tdd", "auto")` and use additional heuristics (e.g., check if `extraction.md` has TDD-specific frontmatter fields) to determine if TDD fallback is appropriate.

---

### DF-10: Test files use toy data that cannot catch prompt size issues

**Severity:** MINOR
**Location:** `tests/roadmap/test_embed_inputs.py`, `tests/roadmap/test_prd_cli.py`

The embed inputs tests use content like `"hello world\n"` (12 bytes) and `"content A\n"` (10 bytes). The PRD CLI tests use `"# Test PRD\n\n## User Personas\n\nSome personas."` (46 bytes). These are 3-4 orders of magnitude smaller than real inputs (44 KB TDD, 20 KB PRD, 73 KB haiku roadmap).

As shown in DF-03, real data pushes the score step over `_EMBED_SIZE_LIMIT`. The existing test `test_prompt_plus_embedded_exceeds_limit` at `tests/roadmap/test_file_passing.py:160` tests the warning path but uses synthetic data sized to just exceed the limit -- it does not test realistic multi-file scenarios where multiple real documents are concatenated.

**Required Fix:** Add an integration test that uses realistic file sizes (at minimum the test fixtures from `.dev/test-fixtures/`) to verify prompt sizes stay within limits across all pipeline steps, or document which steps may exceed limits and under what conditions.

---

## Summary

| # | ID | Severity | Category |
|---|-----|----------|----------|
| 1 | DF-01 | IMPORTANT | State file records wrong input_type |
| 2 | DF-02 | IMPORTANT | No semantic role markers in embedded inputs |
| 3 | DF-03 | IMPORTANT | Score step exceeds embed size limit with real data |
| 4 | DF-04 | MINOR | No empty/binary file handling in embed |
| 5 | DF-05 | IMPORTANT | No way to un-wire PRD on resume |
| 6 | DF-06 | MINOR | State file not written incrementally |
| 7 | DF-07 | IMPORTANT | Merge step missing PRD input |
| 8 | DF-08 | MINOR | Hardcoded PRD section numbers in prompts |
| 9 | DF-09 | IMPORTANT | Tasklist TDD fallback unreachable (consequence of DF-01) |
| 10 | DF-10 | MINOR | Tests use toy data sizes |

**Totals:** 0 CRITICAL, 6 IMPORTANT, 4 MINOR

DF-01 and DF-09 are linked -- fixing DF-01 (propagating resolved input_type to state) automatically fixes DF-09.

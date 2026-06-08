# F4 Discovery — inline REQUIRED-read (producer_step, artifact_filename) pairs

**Date:** 2026-06-08
**Source (live):** `src/superclaude/cli/prd/prompts.py`, `src/superclaude/cli/prd/executor.py`

> Line numbers below are the CURRENT live-source lines (they shifted from the
> research-notes' originals 189/290/293/377/479 because Phase 2's F2 edit added
> ~31 lines above them). The producer-step strings and artifact filenames are
> unchanged.

## The five inline REQUIRED-read call sites (verbatim)

| prompts.py line | call | artifact path constructed | producer_step literal |
|---|---|---|---|
| 223-225 | `_load_json_required(...)` | `config.task_dir / "parsed-request.json"` | `"parse-request"` |
| 324-326 | `_read_required(...)` | `config.task_dir / "scope-discovery-raw.md"` | `"scope-discovery"` |
| 327-329 | `_load_json_required(...)` | `config.task_dir / "parsed-request.json"` | `"parse-request"` |
| 411-413 | `_read_required(...)` | `config.task_dir / "research-notes.md"` | `"research-notes"` |
| 513 | `_read_required(...)` | `config.task_dir / "research-notes.md"` | `"research-notes"` |

## DISTINCT (de-duplicated) pairs vs canonical `_STEP_ARTIFACT_FILES`

`parse-request` and `research-notes` each appear at two sites → de-duplicated to 3 distinct pairs.

| producer_step | prompts.py-side filename | `_STEP_ARTIFACT_FILES[producer_step]` (executor.py:252-263) | match? |
|---|---|---|---|
| `parse-request` | `parsed-request.json` | `parsed-request.json` (line 253) | ✅ |
| `scope-discovery` | `scope-discovery-raw.md` | `scope-discovery-raw.md` (line 254) | ✅ |
| `research-notes` | `research-notes.md` | `research-notes.md` (line 255) | ✅ |

## Verdict

**No drift today** — all three prompts-side inline filenames already match the canonical
executor-side map values. There is no real bug to record. The F4 consistency-guard test
must therefore pin these THREE distinct `(producer_step, expected_artifact_filename)`
pairs (encoding the prompts-side filenames as explicit literals — the test IS the pin) so
the two sources of truth cannot silently drift in future.

## Existing-coverage note (do NOT duplicate)

`prompts.py` already has a read-only mirror dict `_artifact_path_for_step` (lines ~107-125)
and an EXISTING test `test_prompt_executor_mapping_sync` (`tests/cli/prd/test_prompts.py`)
that pins THAT mirror dict to `_STEP_ARTIFACT_FILES` across all 8 keys. The new F4 test must
target the FIVE INLINE CALL-SITE literal pairings above (which the mirror-dict test does NOT
exercise), and its docstring must note it complements — not duplicates — that existing test.

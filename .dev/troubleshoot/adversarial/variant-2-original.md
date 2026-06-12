# Solution 2: Prompt-Side Path Pinning

## Status
Future-debate design doc for confirmed bug in PRD pipeline (v4.2.0).
Confirmed root cause: step prompts tell the agent to "Write a markdown document" or "Produce a research-notes.md file" with **no pinned output path**. The agent picks its own location (observed: `/config/workspace/Octodive/.dev/specs/scope-discovery.md`, `/config/workspace/Octodive/.dev/specs/research-notes.md`). Executor recovery (`_resolve_step_content`, executor.py:266-365) rglobs the exact canonical name (`scope-discovery-raw.md`) under `task_dir` + parent, misses the agent's file (wrong name + wrong location), and falls back to ~24 lines of NDJSON commentary. Gate fails.

---

## Summary

Change the step prompt builders so each document-producing step instructs the agent to **Write its output to an EXACT absolute path** = `{config.task_dir}/{canonical_artifact_name}` (e.g. `task_dir/scope-discovery-raw.md`), matching exactly where `_STEP_ARTIFACT_FILES` and the gate look. This is the existing idiom used by `build-task-file` (prompts.py:439), which pins its path deterministically and is recovered specially.

The fix is a **shared helper** that injects the canonical path into prompts, keeping a single source of truth with `_STEP_ARTIFACT_FILES` so prompt text and executor recovery cannot drift apart.

---

## Design

### 1. Shared Helper: `_artifact_path_for_step`

Add to `/config/workspace/IronClaude/src/superclaude/cli/prd/prompts.py` (after the existing helpers, around line 53):

```python
def _artifact_path_for_step(config: PrdConfig, step_id: str) -> Path | None:
    """Return the canonical artifact path for a step, or None if not applicable.

    Mirrors _STEP_ARTIFACT_FILES in executor.py so prompt-side path pinning
    and executor-side recovery agree on a single source of truth.
    """
    mapping = {
        "parse-request": "parsed-request.json",
        "scope-discovery": "scope-discovery-raw.md",
        "research-notes": "research-notes.md",
        "sufficiency-review": "sufficiency-review.md",
        "research-qa": "qa/qa-research-gate-report.md",
        "synthesis-qa": "qa/qa-synthesis-gate-report.md",
        "structural-qa": "qa/qa-report-validation.md",
        "qualitative-qa": "qa/qa-qualitative-review.md",
    }
    name = mapping.get(step_id)
    if name is None:
        return None
    return config.task_dir / name
```

**Why duplicate the mapping?** `_STEP_ARTIFACT_FILES` lives in `executor.py` and cannot be imported into `prompts.py` without creating a circular import (`executor.py` already imports `prompts.py` lazily in `_build_prompt`). The helper is a **read-only mirror**; a comment in both files cross-references the other. A lightweight unit test (`test_prompts.py`) asserts the two dicts are identical.

### 2. Exact Prompt-Text Changes

#### A. `build_scope_discovery_prompt` (prompts.py:110-191)

**Current** (line 143-156):
```
Your task is to explore the codebase and produce a comprehensive scope discovery document.
...
OUTPUT FORMAT:

Write a markdown document with these sections:
```

**New** (insert after line 153, before `OUTPUT FORMAT`):
```
CRITICAL -- Output Location:
Write the scope discovery document to EXACTLY this path:
{config.task_dir / "scope-discovery-raw.md"}

Do NOT write it to any other directory or filename. The pipeline depends on finding it at this exact location.
```

And change the OUTPUT FORMAT line to:
```
OUTPUT FORMAT:

Write a markdown document to the path above with these sections:
```

#### B. `build_research_notes_prompt` (prompts.py:194-266)

**Current** (line 209):
```
Produce a research-notes.md file with EXACTLY these 7 sections (all required):
```

**New** (insert after line 208, before the existing `Produce...` line):
```
CRITICAL -- Output Location:
Write the research notes to EXACTLY this path:
{config.task_dir / "research-notes.md"}

Do NOT write it to any other directory or filename. The pipeline depends on finding it at this exact location.
```

And change the following line to:
```
Write a markdown document to the path above with EXACTLY these 7 sections (all required):
```

#### C. `build_sufficiency_review_prompt` (prompts.py:269-319)

This step returns JSON, not a markdown file, so it does **not** need path pinning for its primary output. However, the prompt currently says "Return JSON" with no file instruction. The agent may still write a file. To be safe, add:

```
CRITICAL -- Output Location:
Write your JSON response to EXACTLY this path:
{config.task_dir / "sufficiency-review.md"}

Return ONLY the JSON object in that file, no markdown fencing, no explanation.
```

This aligns with `_STEP_ARTIFACT_FILES` and ensures the executor can recover it.

#### D. `build_preparation_prompt` (prompts.py:516-558)

This step writes a `.preparation-complete` marker. It already mentions the path in the prompt body (line 546: "Write a brief status report to .preparation-complete"). However, it is a relative path. Pin it:

```
Write a brief status report to EXACTLY this path:
{config.task_dir / ".preparation-complete"}
```

**Note:** `.preparation-complete` is **not** in `_STEP_ARTIFACT_FILES`, so the executor does not recover it. This is acceptable because the preparation step has no gate that reads it. Pinning is still useful for consistency and to prevent the agent from writing it to `/config/workspace/Octodive/.dev/specs/`.

#### E. Steps that ALREADY pin paths (no change needed)

- `build_task_file_prompt` (prompts.py:439): already pins `Write the task file to: {config.task_dir / (...)}` — the established idiom.
- `build_investigation_prompt` / `_render_investigation_prompt` (prompts.py:746): already pins `write findings to {output_path}`.
- `build_web_research_prompt` / `_render_web_research_prompt` (prompts.py:830): already pins `write findings to {output_path}`.
- `build_synthesis_prompt` / `_render_synthesis_prompt` (prompts.py:1009, 1017): already pins `Output path: {output_path}`.
- `build_assembly_prompt` (prompts.py:1197): already pins `Output path: {config.output_path}`.
- `build_analyst_completeness_prompt` (prompts.py:888): already pins `Output path: {config.qa_dir / "analyst-completeness-report.md"}`.
- `build_qa_research_gate_prompt` (prompts.py:956): already pins `Output path: {config.qa_dir / "qa-research-gate-report.md"}`.
- `build_analyst_synthesis_prompt` (prompts.py:1064): already pins `Output path: {config.qa_dir / "analyst-synthesis-review.md"}`.
- `build_qa_synthesis_gate_prompt` (prompts.py:1109): already pins `Output path: {config.qa_dir / "qa-synthesis-gate-report.md"}`.
- `build_structural_qa_prompt` (prompts.py:1267): already pins `Output path: {config.qa_dir / "qa-report-validation.md"}`.
- `build_qualitative_qa_prompt` (prompts.py:1321): already pins `Output path: {config.qa_dir / "qa-qualitative-review.md"}`.
- `build_completion_prompt` (prompts.py:1372): no file output needed (returns summary in NDJSON).
- `build_gap_filling_prompt` (prompts.py:1451): already pins `Write a brief report of what you fixed to: {config.qa_dir / ...}`.

### 3. How Pinning Fixes `/config/workspace/Octodive/.dev/specs/` Self-Contamination

The observed bug: the agent wrote `scope-discovery.md` and `research-notes.md` into `/config/workspace/Octodive/.dev/specs/` because the parsed request's `WHERE` clause pointed scope work at `/config/workspace/Octodive/.dev/specs/`. Without an explicit output path, the agent inferred the output directory from the context ("focus on these directories" -> "I should write my output there too").

By pinning the output to `{config.task_dir}/scope-discovery-raw.md`, the agent has **no ambiguity** about where to write. The `task_dir` is a dedicated pipeline workspace (e.g. `.dev/tasks/to-do/TASK-PRD-.../`), isolated from the source directories listed in `WHERE`. This eliminates the self-contamination entirely.

### 4. Defense-in-Depth: Executor Recovery Still Backstops

If the agent **still deviates** (ignores the pinned path and writes elsewhere), the executor's `_resolve_step_content` remains the backstop. However, with path pinning, the deviation mode changes:

- **Before:** agent writes to `/config/workspace/Octodive/.dev/specs/scope-discovery.md` (wrong name + wrong dir). `_resolve_step_content` rglobs `scope-discovery-raw.md` and misses it.
- **After:** if the agent deviates, it will likely still use a name close to the prompt's instruction (e.g. `scope-discovery-raw.md` but in `/config/workspace/Octodive/.dev/specs/`). `_resolve_step_content` searches `task_dir.parent` (the project root) with `rglob(base_name)`, so it **would** find `/config/workspace/Octodive/.dev/specs/scope-discovery-raw.md`.

Thus, path pinning improves recovery even in the failure case: the filename is now canonical, so only the directory can deviate, and the directory search is already broad (`task_dir` + `task_dir.parent`).

**Exception:** if the agent writes to a completely unrelated directory (e.g. `/tmp/`), recovery still fails. This is an inherent limitation of any recovery strategy short of filesystem sandboxing.

### 5. Interaction: Research-Notes Reads `task_dir/scope-discovery-raw.md`

`build_research_notes_prompt` (prompts.py:200) already loads:
```python
scope_content = _read_file(config.task_dir / "scope-discovery-raw.md")
```

If the agent previously wrote scope-discovery to `/config/workspace/Octodive/.dev/specs/scope-discovery.md`, this `_read_file` would fail (file not found) or read stale content from a prior run. Path pinning ensures the file is **guaranteed** to exist at the expected path before `build_research_notes_prompt` is called, fixing the cascade.

---

## Why This Approach

| Criterion | Solution 2 (Prompt-Side Path Pinning) | Solution 1 (Executor-Side Fuzzy Search) | Solution 3 (Subprocess Sandbox / chroot) |
|---|---|---|---|
| **Complexity** | Low — prompt text changes only | Medium — new heuristics in executor | High — OS-level isolation, platform-specific |
| **Risk of over-matching** | None — exact path | High — fuzzy search may pick wrong file (e.g. old run artifact) | Low — but overkill |
| **Agent compliance dependency** | Medium — assumes agent follows instructions | Low — works even if agent ignores path | Low — forces compliance |
| **Cross-platform** | Yes | Yes | No (chroot is Unix-only) |
| **Maintainability** | High — single source of truth, explicit | Medium — heuristics drift over time | Low — OS primitives fragile |
| **Performance** | No runtime cost | Slightly slower (broader search) | Overhead per subprocess |
| **Fixes root cause** | Yes — removes ambiguity that caused deviation | No — treats symptom (missed file) | Yes — prevents deviation |

**Key insight:** The root cause is **ambiguity in the prompt**, not a missing recovery mechanism. The executor's recovery was designed as a backstop for agents that write to unexpected locations, but it was never intended to handle agents that use entirely different filenames. Path pinning fixes the ambiguity at the source, making the backstop more effective.

---

## Risks & Footguns (Ranked)

### 1. Agent Non-Compliance (HIGH — inherent to all LLM-agent systems)
The agent may ignore the pinned path and write elsewhere anyway. This is the single biggest weakness of this approach (and any prompt-side fix). Mitigation: the executor's `_resolve_step_content` still runs as a backstop, and with a canonical filename the rglob search is more likely to find the file.

### 2. Mapping Drift Between `prompts.py` and `executor.py` (MEDIUM)
The `_artifact_path_for_step` helper duplicates `_STEP_ARTIFACT_FILES`. If one is updated and the other is not, pinning and recovery disagree. Mitigation: unit test `test_prompt_executor_mapping_sync` asserts the two dicts are identical.

### 3. Absolute Path Leakage into Agent Context (LOW)
Passing absolute paths (`/home/user/...`) in prompts may confuse the agent or cause it to hardcode paths in outputs. Mitigation: use `Path` objects which render cleanly; the agent only needs to use the path for `Write`/`Edit` tool calls, not embed it in content.

### 4. Breaks Custom Agent Wrappers (LOW)
If users have custom agent wrappers that intercept prompt text and modify file-writing behavior, pinning may conflict. Mitigation: this is an internal pipeline; external wrappers are not supported.

### 5. Task Dir Not Created Before Prompt Build (LOW)
The prompt builder assumes `config.task_dir` exists. It is created by `create_task_dirs` in `PrdExecutor.run` before any step runs, so this is safe.

---

## Backward Compatibility

- **No breaking changes to public API.** The fix is entirely internal to prompt text.
- **Resume behavior:** Existing resume logic in `PrdExecutor.run` (lines 446-456) skips steps whose artifacts already exist. Path pinning does not change artifact locations, so resume behavior is unchanged.
- **Gate criteria:** No changes to `GATE_CRITERIA` in `gates.py`.
- **Existing task directories:** If a user has a failed run with artifacts in `/config/workspace/Octodive/.dev/specs/`, a new run with the fix will write to `task_dir` and the old `/config/workspace/Octodive/.dev/specs/` files will be ignored. This is correct behavior — the old files were wrong.

---

## Test Plan

### Unit Tests (`/config/workspace/IronClaude/tests/cli/prd/test_prompts.py`)

1. `test_artifact_path_for_step_returns_correct_path` — assert `_artifact_path_for_step(config, "scope-discovery") == config.task_dir / "scope-discovery-raw.md"` for all mapped steps.
2. `test_artifact_path_for_step_returns_none_for_unmapped` — assert `None` for "build-task-file", "assembly", etc.
3. `test_prompt_executor_mapping_sync` — assert the dict inside `_artifact_path_for_step` matches `_STEP_ARTIFACT_FILES` (imported via a test-only reflection to avoid circular import issues).

### Prompt Builder Tests (`/config/workspace/IronClaude/tests/cli/prd/test_prompt_builders_dual_mode.py`)

4. `test_scope_discovery_prompt_contains_pinned_path` — assert the rendered prompt contains the exact absolute path to `scope-discovery-raw.md`.
5. `test_research_notes_prompt_contains_pinned_path` — assert the rendered prompt contains the exact absolute path to `research-notes.md`.
6. `test_sufficiency_review_prompt_contains_pinned_path` — assert the rendered prompt contains the exact absolute path to `sufficiency-review.md`.
7. `test_preparation_prompt_contains_pinned_path` — assert the rendered prompt contains the exact absolute path to `.preparation-complete`.

### E2E Tests (`/config/workspace/IronClaude/tests/cli/prd/test_e2e.py`)

8. `test_scope_discovery_artifact_written_to_task_dir` — run the pipeline (or mock the subprocess) and assert `scope-discovery-raw.md` exists in `task_dir` after step 3.
9. `test_research_notes_reads_scope_discovery_from_task_dir` — run steps 3 and 4, assert research-notes prompt loads scope content from `task_dir/scope-discovery-raw.md`.
10. `test_no_dev_specs_contamination` — run steps 3 and 4, assert no `scope-discovery*.md` or `research-notes*.md` files exist in `/config/workspace/Octodive/.dev/specs/` (or any `WHERE` directory).

### Regression Tests

11. `test_build_task_file_prompt_already_pins_path` — assert the existing pinned path in `build_task_file_prompt` is still present (ensures we don't break the established idiom).
12. `test_investigation_prompt_already_pins_path` — assert investigation prompts still contain `write findings to {output_path}`.

---

## Effort Estimate

| Task | Effort |
|---|---|
| Add `_artifact_path_for_step` helper + docstrings | 15 min |
| Update `build_scope_discovery_prompt` | 10 min |
| Update `build_research_notes_prompt` | 10 min |
| Update `build_sufficiency_review_prompt` | 10 min |
| Update `build_preparation_prompt` | 5 min |
| Add cross-reference comments in `executor.py` | 5 min |
| Unit tests (`test_prompts.py`) | 30 min |
| Prompt builder tests (`test_prompt_builders_dual_mode.py`) | 30 min |
| E2E tests (`test_e2e.py`) | 45 min |
| Run full test suite + fix failures | 30 min |
| **Total** | **~3 hours** |

---

## Open Questions for Debate

1. Should we also pin the `.preparation-complete` path even though it is not in `_STEP_ARTIFACT_FILES`? (Pro: consistency; Con: slightly more code for no functional gain.)
2. Should the mapping live in a third shared module (e.g. `artifact_names.py`) to eliminate the duplication risk entirely? (Pro: single source of truth; Con: new module, more imports.)
3. Should we add a post-step validator that asserts the expected file exists at the pinned path, and fails fast if the agent ignored the instruction? (Pro: catches non-compliance immediately; Con: redundant with gate check.)

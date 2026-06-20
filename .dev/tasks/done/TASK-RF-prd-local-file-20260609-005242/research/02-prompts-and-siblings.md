# Research 02 — Prompts & Siblings: inline delivery machinery that REPLACES `--file`

**Topic:** Patterns & Conventions — the inline delivery machinery that replaces `--file`, and the sibling-pipeline pattern.
**Track goal:** Upgrade `_authoritative_specs_block(spec_paths)` to embed each spec's CONTENT via existing `_read_file(...)` (50KB cap + `_TRUNCATION_MARKER`) under a per-spec header, keeping a "MUST Read IN FULL if truncated" instruction, preserving the empty-input contract (return "" for None/[]).

**Status: Complete**

> NOTE ON PATH: The task brief says `src/superclaude/cli/prd/prompts.py`. Confirmed — that is the file. (There is no top-level `cli/prd/prompts.py`; it lives under `src/superclaude/`.) All line numbers below verified against the current file (56,564 bytes, mtime Jun 9 00:42).

---

## 1. `_authoritative_specs_block(spec_paths)` — the function to upgrade

**File:** `src/superclaude/cli/prd/prompts.py:120-138`

Verbatim:

```python
def _authoritative_specs_block(spec_paths: list[str] | None) -> str:
    """Imperative AUTHORITATIVE-SPECS prompt fragment, or '' when no specs.

    Returns an empty string (no leading whitespace) when *spec_paths* is empty
    or None, so callers that interpolate it produce prompts byte-identical to
    the no-spec path. When specs are present, returns a block (prefixed with a
    blank line) instructing the agent to Read each authoritative spec in full.

    Phase 1 (paths-only): the block carries paths, not inlined content.
    """
    if not spec_paths:
        return ""
    listed = "\n".join("- " + p for p in spec_paths if p)
    return (
        "\n\nAUTHORITATIVE SPECIFICATIONS -- these files are the operator's "
        "ground truth for this PRD. You MUST Read each one IN FULL before "
        "drawing conclusions, and treat their contents as overriding any "
        "inference from directory names or structure:\n" + listed
    )
```

Key observations:
- **Empty-input contract (`prompts.py:130-131`):** `if not spec_paths: return ""` — covers both `None` and `[]` (and any falsy). Returns the empty string with **no leading whitespace**. The docstring (`:122-124`) explicitly promises "no leading whitespace … byte-identical to the no-spec path." This contract MUST be preserved by the upgrade.
- **Current body is paths-only (`:132-138`).** It builds `listed` = newline-joined `- {path}` (filtering out empty strings via `if p`), then returns a block that starts with `\n\n` (a blank line), the header `AUTHORITATIVE SPECIFICATIONS -- ...`, and the bullet list of paths.
- **Exact current wording to be aware of (`:134-138`):** `"AUTHORITATIVE SPECIFICATIONS -- these files are the operator's ground truth for this PRD. You MUST Read each one IN FULL before drawing conclusions, and treat their contents as overriding any inference from directory names or structure:\n"` followed by `listed`.
- The docstring's last line (`:128`) is a stale marker for the upgrade: `"Phase 1 (paths-only): the block carries paths, not inlined content."` — this is exactly what the track goal changes. The docstring should be updated when content is inlined.
- **Signature stays `spec_paths: list[str] | None`.** Inlining content does not require a signature change (paths are still the input; `_read_file` is called inside on each path). Confirmed below at both call sites.

---

## 2. `_read_file(...)` + `_TRUNCATION_MARKER` — the existing inlining primitive (REUSE THIS)

**`_TRUNCATION_MARKER` — `src/superclaude/cli/prd/prompts.py:34`:**

```python
_TRUNCATION_MARKER = "\n\n[TRUNCATED — file exceeds 50KB inline limit]"
```

(`—` is an em-dash `—`. Rendered: `\n\n[TRUNCATED — file exceeds 50KB inline limit]`.)

**`_read_file` — `src/superclaude/cli/prd/prompts.py:42-47`:**

```python
def _read_file(path: Path, max_bytes: int = 50_000) -> str:
    """Read a file, truncating if >50KB for prompt embedding."""
    content = path.read_text(encoding="utf-8")
    if len(content) > max_bytes:
        return content[:max_bytes] + _TRUNCATION_MARKER
    return content
```

Confirmed truncation behavior:
- Reads full file with `path.read_text(encoding="utf-8")`.
- If `len(content) > max_bytes` (default `50_000`), returns `content[:max_bytes] + _TRUNCATION_MARKER` — i.e. the first 50,000 chars plus the marker.
- Otherwise returns the full content untouched.
- **Note:** `max_bytes` actually slices on *character* count (`len(content)` / `content[:max_bytes]`) not byte count, but that is the existing semantics and the docstring/marker both say "50KB" — the upgrade should reuse `_read_file` as-is, not reinvent it.
- **`_read_file` does NOT handle a missing path** — it calls `read_text` directly and will raise `FileNotFoundError` if the path is absent. (`_read_required` at `:91-95` is the guarded variant.) The upgrade to `_authoritative_specs_block` must decide how to handle a spec path that does not exist on disk — `_read_file` alone will throw. The siblings'/refs pattern always points at known-present files; spec paths come from operator `--spec` input bound into `parsed-request.json`, so existence is not guaranteed here. **This is the one real design decision for the upgrade** (e.g. guard with `path.is_file()` / try-except, or rely on `--spec` validation upstream).

---

## 3. Both call sites — invocation + interpolation (signature change NOT needed)

**Call site A — scope-discovery prompt, `src/superclaude/cli/prd/prompts.py:244-249` (invocation) + `:257` (interpolation):**

```python
    # SPECS is a Python-owned array bound into parsed-request.json by the
    # executor after parse-request. Absent on --where-only / bare runs, so the
    # block is empty and the prompt stays byte-identical to today (R4/R6).
    specs_block = _authoritative_specs_block(
        [s.get("path", "") for s in (parsed.get("SPECS") or [])]
    )
```

Interpolation into the f-string (`:256-257`):

```python
{where_clause}
{ctx}{specs_block}
```

- Input is a `list[str]` derived from `parsed["SPECS"]` — each entry's `.get("path", "")`. When `SPECS` is absent, `parsed.get("SPECS") or []` ⇒ `[]` ⇒ block returns `""` ⇒ byte-identical prompt. (Comment at `:244-246` documents this R4/R6 contract.)
- `{specs_block}` is appended directly after `{ctx}` with no separator — relies on the block's own leading `\n\n`.

**Call site B — investigation prompt, `src/superclaude/cli/prd/prompts.py:919` (invocation) + `:927` (interpolation):**

```python
    files_list = "\n".join(f"- {f}" for f in files)
    specs_block = _authoritative_specs_block(spec_paths)
```

Interpolation into the f-string (`:927`):

```python
Product root: {product_root}{specs_block}
```

- Here `spec_paths` is passed straight through from `_render_investigation_prompt(..., spec_paths: list[str] | None = None)` (signature at `:904-911`). Defaults to `None` ⇒ block returns `""` ⇒ byte-identical (docstring `:916`).
- Again `{specs_block}` appended with no separator after `{product_root}`; leading `\n\n` lives in the block.

**Conclusion:** Both call sites pass a `list[str] | None` / list and interpolate the returned string verbatim. Upgrading the *body* of `_authoritative_specs_block` to inline content via `_read_file` requires **NO change to either call site and NO signature change** — the contract (takes spec_paths, returns a string, `""` when empty) is unchanged. Only the non-empty branch's content grows.

---

## 4. How refs are already inlined (independent of any `--file` mechanism)

`build_task_file_prompt` — `src/superclaude/cli/prd/prompts.py:507-524` — reads each ref file directly via `_read_file` against `config.skill_refs_dir`:

```python
    notes = _read_required(config.task_dir / "research-notes.md", "research-notes")
    build_template = _read_file(config.skill_refs_dir / "build-request-template.md")
    agent_prompts = _read_file(config.skill_refs_dir / "agent-prompts.md")
    synth_mapping = _read_file(config.skill_refs_dir / "synthesis-mapping.md")
    validation = _read_file(config.skill_refs_dir / "validation-checklists.md")
    operational = _read_file(config.skill_refs_dir / "operational-guidance.md")
```

And interpolates each one **inline into the prompt f-string** under a per-section header with `---` fences — `prompts.py:546-568` (representative excerpt):

```python
Research Notes:
---
{notes}
---

Build Request Template:
---
{build_template}
---

Agent Prompt Templates:
---
{agent_prompts}
---

Synthesis Mapping:
---
{synth_mapping}
---

Validation Checklists:
---
{validation}
```

Key takeaway for the upgrade:
- **The ref content reaches the agent entirely through the prompt string** — read via `_read_file`, embedded under a labeled header with `---` delimiters. There is no `--file` flag involved; content delivery is pure f-string interpolation.
- This is the **exact pattern** `_authoritative_specs_block` should adopt for specs: per-spec header + `_read_file(Path(p))` content body. The "labeled header + `---` fence + inlined `_read_file` output" idiom is already established and tested in this same file.
- Other `_read_file` inline call sites for cross-reference: `:613 task_content = _read_file(task_path)` (also inlined into a prompt). All `_read_file` usages feed prompt strings, never a `--file` arg.

---

## 5. Sibling no-`--file` pattern — content delivered via prompt, never `--file`

All three sibling executors carry a module docstring asserting the inline-only / no-`--file` contract. Verbatim:

**`src/superclaude/cli/roadmap/executor.py:7-9`:**

```
Context isolation: each subprocess receives only its prompt via inline embedding.
No --continue, --session, --resume, or --file flags are passed (FR-003, FR-023).
--file is a cloud download mechanism and does not inject local file content.
```

**`src/superclaude/cli/tasklist/executor.py:9-10`:**

```
Context isolation: each subprocess receives only its prompt via inline embedding.
--file is a cloud download mechanism and does not inject local file content.
```

**`src/superclaude/cli/roadmap/validate_executor.py:10-11`:**

```
Context isolation: each subprocess receives only its prompt via inline embedding.
--file is a cloud download mechanism and does not inject local file content.
```

Confirmation: all three siblings pass **no `--file`** and deliver all content (spec text, roadmap, tasklist) by **inline embedding into the prompt**. The PRD pipeline's `_authoritative_specs_block` upgrade aligns the PRD `--spec` path with this established sibling convention — specs become inline prompt content, not a `--file` download. (The rationale "`--file` is a cloud download mechanism and does not inject local file content" is the documented justification across the codebase for inlining instead of `--file`.)

---

## 6. TEST CONVENTIONS — what tests cover `_authoritative_specs_block` today + what a format change breaks

### 6a. The PRIMARY test file is `tests/cli/prd/test_spec_flag.py` (NOT test_prompts.py)

This is the dedicated spec-flag/inline-injection test suite. It imports `_authoritative_specs_block` and `_render_investigation_prompt` directly (`tests/cli/prd/test_spec_flag.py:35-40`). The module docstring (`:1-21`) describes the surface: "5. Prompt inject -- scope-discovery contains the AUTHORITATIVE-SPECS block + exact paths when SPECS present; byte-identical to today."

**Relevant test functions (all in `tests/cli/prd/test_spec_flag.py`):**

1. **`TestScopeDiscoverySpecInjection.test_block_present_with_exact_paths` (`:251-265`)** — builds `parsed["SPECS"]` with **non-existent paths** `/abs/SPEC_A.md`, `/abs/SPEC_B.md` (entries carry `inlined: False`, `truncated: False`), calls `build_scope_discovery_prompt`, then asserts:
   - `"AUTHORITATIVE SPECIFICATIONS" in prompt`
   - `"/abs/SPEC_A.md" in prompt` and `"/abs/SPEC_B.md" in prompt`
   - `"MUST Read each one IN FULL" in prompt`
   - **WILL BREAK under content-inlining:** these paths do NOT exist on disk. If the upgrade calls `_read_file(Path(p))` unconditionally, this test raises `FileNotFoundError`. **The upgrade either (a) must guard non-existent paths, or (b) this fixture must be changed to write real temp files.** The exact-string assertion `"MUST Read each one IN FULL"` is also a phrasing lock — the track goal's "MUST Read IN FULL if truncated" wording must keep this substring matchable (or the test/assertion must be updated). The existing string is `"You MUST Read each one IN FULL before drawing conclusions"` (`prompts.py:135`).

2. **`TestScopeDiscoverySpecInjection.test_no_specs_is_byte_identical` (`:267-308`)** — the **byte-equality lock**. Builds three prompts (no SPECS key / empty SPECS `[]` / with one spec `/abs/SPEC.md`), normalizes the incidental task_dir basename via `_norm` (`:294-295`), then asserts:
   - `empty_norm == no_spec_norm` (empty array is true no-op)
   - `"AUTHORITATIVE" not in no_spec_prompt`
   - `block = _authoritative_specs_block(["/abs/SPEC.md"])` ⇒ `block in with_prompt`
   - `with_norm.replace(block, "") == no_spec_norm` (with-spec differs from no-spec ONLY by the block)
   - **WILL BREAK under content-inlining:** `/abs/SPEC.md` is non-existent ⇒ `_authoritative_specs_block(["/abs/SPEC.md"])` at `:306` throws if unguarded. Even if guarded, this is a **byte-identity snapshot test** — it does not hardcode the block text, it derives `block` from the helper itself, so it is robust to content-format changes **as long as the same string is produced both in the prompt and by the standalone helper call** (it is, since the prompt interpolates the helper output). So this test survives a format change PROVIDED the missing-path issue is resolved.

3. **`TestScopeDiscoverySpecInjection.test_helper_empty_returns_empty_string` (`:310-312`)** — the **empty-input contract lock**:
   ```python
   assert _authoritative_specs_block([]) == ""
   assert _authoritative_specs_block(None) == ""
   ```
   This MUST keep passing — directly enforces the "return '' for None/[]" contract from the track goal. The upgrade's early return must be preserved.

4. **`TestInvestigationSpecInjection.test_render_block_present_with_specs` (`:318-328`)** — calls `_render_investigation_prompt(..., spec_paths=["/abs/SPEC.md"])`, asserts `"AUTHORITATIVE SPECIFICATIONS" in prompt` and `"/abs/SPEC.md" in prompt`. **Same non-existent-path concern.**

5. **`TestInvestigationSpecInjection.test_render_byte_identical_without_specs` (`:330-342`)** — asserts `none_prompt == empty_prompt == default_prompt` and `"AUTHORITATIVE" not in none_prompt`. Robust to format change (no specs ⇒ empty branch).

6. **`TestInvestigationSpecInjection.test_config_mode_threads_specs_from_artifact` (`:344-363`)** — writes `parsed["SPECS"] = [{"path": "/abs/SPEC.md", ...}]`, builds via config-mode `build_investigation_prompt`, asserts `"AUTHORITATIVE SPECIFICATIONS" in prompt`. **Same non-existent-path concern.**

**How tests construct a temp spec file + assert content appears (the pattern to follow):** Existing CLI-parse tests already write real temp specs — e.g. `TestSpecCliParse.test_repeated_spec_accepted` (`:85-94`): `a.write_text("# A\n", ...)`, `b.write_text("# B\n", ...)`; and `TestBindSpecs.test_adds_specs_array_and_prepends_where` (`:169-188`): `spec.write_text("x" * 123, ...)` then asserts on the SPECS entry's `size`. **For a content-appears assertion under the upgrade, the injection tests should be migrated to this pattern:** write `spec = tmp_path / "SPEC.md"; spec.write_text("UNIQUE_MARKER content")`, bind that real path into `parsed["SPECS"]`, build the prompt, and `assert "UNIQUE_MARKER content" in prompt`. The fixture helpers `_write_parsed` (`:58-60`) and `_PARSED_BASE` (`:46-55`) and `_scope_config` (`:63-71`) are the scaffolding to reuse.

### 6b. `tests/cli/prd/test_prompts.py` — truncation primitive + size guards (secondary)

- **`TestReadFileTruncation.test_read_file_truncation_at_50kb` (`tests/cli/prd/test_prompts.py:249-277`)** — directly tests `_read_file` boundary behavior: exact 50,000 chars NOT truncated; 50,001 ⇒ `result.endswith(marker)`, `len(result) == 50_000 + len(marker)`, `result[:50_000] == "B"*50_000`; small file unchanged. The marker string is hardcoded at `:253`: `"\n\n[TRUNCATED — file exceeds 50KB inline limit]"`. **This locks the `_read_file` primitive the upgrade reuses — do not change `_read_file` or this breaks.** It does NOT test `_authoritative_specs_block`.
- **`TestPromptSizeUnder100KB.test_prompt_size_under_100kb` (`:160-246`)** — asserts every builder's output `< 100_000` chars for worst-case inputs. **RELEVANT RISK:** inlining spec CONTENT (up to 50KB per spec, possibly multiple specs) into the scope-discovery / investigation prompts could push past 100KB. The fixtures here have no SPECS, so this test won't catch it directly, but the 100KB ceiling is an existing invariant the upgrade should respect (a single 50KB-capped spec plus the base prompt stays under 100KB; multiple large specs could exceed it — worth a sizing note in the task).
- `test_prompts.py` does NOT import or test `_authoritative_specs_block`. Its `config`/`task_dir` fixtures (`:42-116`) write real refs files and a `parsed-request.json` with **no SPECS key** (`:52-58`), so its prompts always exercise the empty-block path.

### 6c. `tests/roadmap/test_prd_prompts.py` is UNRELATED to this change

It imports from `superclaude.cli.roadmap.prompts` (`tests/roadmap/test_prd_prompts.py:14-22`), not the PRD `prompts.py`. It tests roadmap **PRD-supplementary blocks** (`build_extract_prompt`, `build_generate_prompt`, etc. across scenarios A-E). It does NOT reference `_authoritative_specs_block` or `_read_file`. It is, however, a **parallel example of the same idiom** (conditional supplementary block + "baseline identical without prd" byte-equality tests, e.g. `test_baseline_identical_without_prd` at `:59`, `:99`, `:211`) — useful as a model for how this codebase structures "block-present vs byte-identical-when-absent" test pairs.

### 6d. `tests/cli/prd/test_prompt_builders_dual_mode.py` — no spec/AUTHORITATIVE coverage

Grep for `_authoritative_specs_block|specs_block|AUTHORITATIVE|MUST Read|SPECS|byte` returned nothing. This file does not gate the change.

---

## SUMMARY

**The exact change site:** `_authoritative_specs_block(spec_paths)` at `src/superclaude/cli/prd/prompts.py:120-138`. Keep the signature (`list[str] | None`) and the empty-input early return (`if not spec_paths: return ""` at `:130-131`). Both call sites — scope-discovery (`:247-249`, interpolated `{specs_block}` at `:257`) and investigation (`:919`, interpolated at `:927`) — pass spec_paths and interpolate the returned string verbatim, so NO call-site or signature change is needed; only the non-empty branch body changes.

**The primitive to reuse:** `_read_file(path, max_bytes=50_000)` at `:42-47` (returns `content[:max_bytes] + _TRUNCATION_MARKER` when over cap; `_TRUNCATION_MARKER` at `:34`). The refs-inlining idiom in `build_task_file_prompt` (`:507-524` read, `:546-568` interpolate under labeled `---`-fenced headers) is the exact pattern to mirror for per-spec headers. Sibling executors (roadmap `executor.py:7-9`, tasklist `executor.py:9-10`, validate `validate_executor.py:10-11`) all document the no-`--file` / inline-only contract. `_read_file` will RAISE `FileNotFoundError` on a missing path — the one real design decision is how `_authoritative_specs_block` handles a non-existent spec path.

**Test impact (the live gate):** `tests/cli/prd/test_spec_flag.py` is the suite to update. `TestScopeDiscoverySpecInjection` (`:250-312`) and `TestInvestigationSpecInjection` (`:315-363`) bind NON-EXISTENT paths (`/abs/SPEC.md`, etc.) into SPECS — these WILL throw once content is inlined unless paths are guarded OR the fixtures are migrated to real `tmp_path` spec files (pattern already used at `:85-94`, `:169-188`). Preserve substrings `"AUTHORITATIVE SPECIFICATIONS"` and `"MUST Read each one IN FULL"`. `test_helper_empty_returns_empty_string` (`:310-312`) locks the empty-on-None/[] contract. The byte-identity test (`:267-308`) derives its expected block from the helper itself, so it survives a format change once the missing-path issue is fixed. `test_prompts.py` locks `_read_file` truncation (`:249-277`, don't touch the primitive) and a 100KB prompt ceiling (`:160-246`) — multiple large inlined specs could approach it. `tests/roadmap/test_prd_prompts.py` is UNRELATED (different module: `roadmap.prompts`).

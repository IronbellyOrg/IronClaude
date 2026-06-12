# Research: prompts.py Builder Inventory

Topic type: File Inventory
Scope: `/config/workspace/IronClaude/src/superclaude/cli/prd/prompts.py` ONLY
Status: Complete
Date: 2026-06-06

File total length: **1454 lines** (BUILD_REQUEST line estimates were close but re-confirmed below; file is larger than the ~558 range implied — Stage B builders extend to L1454).

---

## Section 3 first (foundation): Module head, imports, helper insertion point

Lines 1-53 (`prompts.py:1-53`):

- `prompts.py:13` — `from __future__ import annotations`
- `prompts.py:15` — `import json`
- `prompts.py:16` — `from datetime import date`
- `prompts.py:17` — **`from pathlib import Path`** — `Path` IS imported at module level (usable in a new helper signature/body).
- `prompts.py:18` — `from typing import TYPE_CHECKING`
- `prompts.py:20-24` — `from ._artifact_patterns import (investigation_filename, synthesis_filename, web_research_filename)`
- `prompts.py:26-27` — **`if TYPE_CHECKING:` / `from superclaude.cli.prd.models import PrdConfig`** — `PrdConfig` is imported ONLY under `TYPE_CHECKING` (used as a string-annotation type; with `from __future__ import annotations` at L13 this is fine for type hints, but a runtime `isinstance`/instantiation of `PrdConfig` would NOT work without a real import).
- `prompts.py:30-32` — `# Helpers` comment banner.
- `prompts.py:34` — `_TRUNCATION_MARKER = "..."` (module constant).
- `prompts.py:37-39` — `_load_json(path: Path) -> dict`
- `prompts.py:42-47` — `_read_file(path: Path, max_bytes: int = 50_000) -> str`
- `prompts.py:50-52` — `_today() -> str`

**Helper insertion point for `_artifact_path_for_step(config, step_id)`:** Insert it in the Helpers block, after `_today()` ends at `prompts.py:52` and before the `# Stage A Prompt Builders` banner at `prompts.py:55-57`. (BUILD_REQUEST said "near L53" — confirmed: L53 is currently blank, between `_today` and the Stage A banner.) `Path` is available (L17). To reference the `config` type in the helper signature, use the same string-annotation idiom the builders use (`config: PrdConfig`) — it resolves via the `TYPE_CHECKING` import at L27 under `from __future__ import annotations`.

---

## Section 4: How builders reference `config.task_dir` today

`config.task_dir` is a Path attribute used pervasively via the `/` operator (so an f-string `{config.task_dir / "<name>"}` renders a fully-resolved absolute path, exactly like existing pinned lines).

Verbatim example — `prompts.py:200`:

```python
    scope_content = _read_file(config.task_dir / "scope-discovery-raw.md")
```

Other examples confirming the idiom: `prompts.py:116` (`config.task_dir / "parsed-request.json"`), `prompts.py:275` (`config.task_dir / "research-notes.md"`), `prompts.py:439` (`config.task_dir / ("TASK-PRD-" + config.product_slug + ".md")`), `prompts.py:885` inside an f-string prompt body (`{config.task_dir / "research-notes.md"}`). So `{config.task_dir / "<name>"}` inside a returned f-string is already the established rendering pattern.

---

## Section 5: Canonical filenames each of the 4 steps should pin

Cross-checked against the actual read/write references inside prompts.py:

| Step | Canonical filename | Evidence (prompts.py) |
|------|--------------------|------------------------|
| scope-discovery | `scope-discovery-raw.md` | Read by research-notes at `prompts.py:200` and `prompts.py:690` (`scope_path = config.task_dir / "scope-discovery-raw.md"`). This is the file the scope-discovery step must PRODUCE. |
| research-notes | `research-notes.md` | Mentioned in-prompt at `prompts.py:222` ("Produce a research-notes.md file"); consumed downstream at `prompts.py:275, 365, 655, 679, 885, 954`. |
| sufficiency-review | `sufficiency-review.md` | **Unverified inside prompts.py** — sufficiency-review returns JSON (see Section 1) and prompts.py contains NO read or write of a `sufficiency-review.md` filename (grep returns no hits). The canonical name `sufficiency-review.md` must come from executor.py's artifact mapping (R2's scope), not prompts.py. Flag: this step currently emits a JSON verdict, NOT a document named `sufficiency-review.md`. |
| preparation | `.preparation-complete` | The preparation prompt instructs writing a status report to `.preparation-complete` (a dotfile marker, NOT a `.md`): `prompts.py:541` ("Create a .preparation-complete marker file") and `prompts.py:546` ("Write a brief status report to .preparation-complete"). There is no `preparation.md`. The pinnable canonical artifact for this step is `.preparation-complete`. |

**IMPORTANT for the builder agent:** Two of the four "document builders" named in the BUILD_REQUEST do not actually produce a free-form markdown document with an OUTPUT FORMAT section:
- `build_sufficiency_review_prompt` returns a **JSON verdict** (no document, no canonical `.md` written here).
- `build_preparation_prompt` writes a **dotfile marker** `.preparation-complete`, not a markdown doc.
Confirm the canonical filenames + whether these two should be pinned at all against R2 (executor `_STEP_ARTIFACT_FILES`). Only `build_scope_discovery_prompt` and `build_research_notes_prompt` are unambiguous free-form markdown document producers with a clear `OUTPUT FORMAT` / section-list anchor.

---

## Section 1: The 4 UN-PINNED builders that need an output-path pin

None of the 4 builders below contains an `Output path:` / `Write ... to:` line in its returned f-string (confirmed: the only such lines in the file are at L439 task-file and the QA builders L887/956/1064/1109/1267/1321). The design says inject a `CRITICAL -- Output Location:` block **before the OUTPUT FORMAT section**.

### 1a. `build_scope_discovery_prompt` — DOCUMENT producer (markdown)
- **Definition:** `prompts.py:110-191` (`def` at L110, function body's returned f-string closes with `"""` at L191).
- **Signature** (`prompts.py:110-114`):
  ```python
  def build_scope_discovery_prompt(
      config: PrdConfig,
      *,
      context_summaries: list[str] | None = None,
  ) -> str:
  ```
- **`OUTPUT FORMAT` section anchor:** the literal line `OUTPUT FORMAT:` is at **`prompts.py:154`** (inside the returned f-string). It is preceded by the `PROCESS:` block (L145-152) and a blank line (L153). **Inject the `CRITICAL -- Output Location:` block immediately before L154** (i.e., between L152/L153 `PROCESS` block and the `OUTPUT FORMAT:` header), per the "inject before OUTPUT FORMAT" design. The f-string body runs L135-190; the section headers it lists (`## Project Overview` … `## Recommended Research Assignments`) span L156-187.
- Canonical artifact to pin: `scope-discovery-raw.md` (see Section 5).

### 1b. `build_research_notes_prompt` — DOCUMENT producer (markdown)
- **Definition:** `prompts.py:194-266` (`def` at L194, returned f-string closes at L266).
- **Signature** (`prompts.py:194-198`):
  ```python
  def build_research_notes_prompt(
      config: PrdConfig,
      *,
      context_summaries: list[str] | None = None,
  ) -> str:
  ```
- **Reads scope-discovery-raw.md at `prompts.py:200`** (`scope_content = _read_file(config.task_dir / "scope-discovery-raw.md")`) — MUST NOT be broken.
- **DO-NOT-TOUCH frontmatter emission:** the prompt body emits a literal frontmatter block at **`prompts.py:224-228`**:
  ```
  ---
  Date: {_today()}
  Scenario: {parsed.get("SCENARIO", "B")}
  Tier: {config.tier}
  ---
  ```
  This is the frontmatter the produced `research-notes.md` must carry; the `---` fences at L224 and L228 and the `{_today()}` / `{config.tier}` interpolations MUST NOT be touched.
- **OUTPUT FORMAT anchor:** This builder has NO literal `OUTPUT FORMAT:` header. The equivalent section-list anchor is the line **`prompts.py:222`**: `Produce a research-notes.md file with EXACTLY these 7 sections (all required):`, immediately followed by the frontmatter at L224-228 and the `# Research Notes:` heading at L230. **Safest injection point: before L222** (the "Produce a research-notes.md file with EXACTLY these 7 sections" instruction), so the pin precedes the section spec but does not disturb the frontmatter block at L224-228. Do NOT inject between L222 and L228.
- Canonical artifact to pin: `research-notes.md` (see Section 5).

### 1c. `build_sufficiency_review_prompt` — JSON producer (NOT a free-form doc)
- **Definition:** `prompts.py:269-319` (`def` at L269, returned f-string closes at L319).
- **Signature** (`prompts.py:269-273`):
  ```python
  def build_sufficiency_review_prompt(
      config: PrdConfig,
      *,
      context_summaries: list[str] | None = None,
  ) -> str:
  ```
- Reads `research-notes.md` at `prompts.py:275`.
- **No `OUTPUT FORMAT:` header.** The output contract is a JSON block: the line `Return JSON:` at **`prompts.py:301`**, followed by the JSON schema at L302-313. If a pin is desired, the analogous injection point is **before L301 (`Return JSON:`)**. CAVEAT: this step returns a JSON verdict, not a document — see the IMPORTANT note in Section 5. Verify against R2 whether this step is in scope for path-pinning at all.

### 1d. `build_preparation_prompt` — marker-file producer (NOT a `.md` doc)
- **Definition:** `prompts.py:516-558` (`def` at L516, returned f-string closes at L558).
- **Signature** (`prompts.py:516-520`):
  ```python
  def build_preparation_prompt(
      config: PrdConfig,
      *,
      context_summaries: list[str] | None = None,
  ) -> str:
  ```
- **No `OUTPUT FORMAT:` header.** The prompt body's `PREPARATION STEPS:` block is at L539-544; it already names the output target inline at **`prompts.py:541`** ("Create a .preparation-complete marker file") and **`prompts.py:546`** ("Write a brief status report to .preparation-complete"), followed by a fenced status-report template at L548-555. If pinning, inject the `CRITICAL -- Output Location:` block before the `PREPARATION STEPS:` header (before L539). CAVEAT: target is `.preparation-complete` (dotfile marker), not a markdown document — see Section 5.

---

## Section 2: The ALREADY-PINNED idiom (the pattern to copy) + builders NOT to touch

### Idiom A — `Write ... to:` (task-file builder), `build_task_file_prompt`
Verbatim at **`prompts.py:439`** (inside the returned f-string):

```
Write the task file to: {config.task_dir / ("TASK-PRD-" + config.product_slug + ".md")}
```

This line sits AFTER the `INSTRUCTIONS:` block (L429-437) and BEFORE the frontmatter spec (L441-448). It pins an absolute path via `config.task_dir / (...)`.

### Idiom B — `Output path:` (QA / analyst builders) — the cleaner copy target
Verbatim at **`prompts.py:887`** (inside `build_*` returned f-string), shown with its surrounding pinned header lines L883-888:

```
Analysis type: completeness-verification
Research directory: {config.research_dir}
Research notes file: {config.task_dir / "research-notes.md"}
Tier: {config.tier}
Output path: {config.qa_dir / "analyst-completeness-report.md"}
```

The `Output path: {config.<dir> / "<file>.md"}` form is the canonical idiom the 4 fixes should copy (substituting `config.task_dir` and the canonical filename from Section 5).

### Other already-pinned builders — DO NOT TOUCH
Each of these already emits an `Output path:` (or `Write ... to:`) pin; the builder agent must NOT add a second pin:

- `prompts.py:439` — task-file builder (`Write the task file to: ...`).
- `prompts.py:887` — analyst completeness report (`Output path: {config.qa_dir / "analyst-completeness-report.md"}`).
- `prompts.py:956` — QA research-gate report (`Output path: {config.qa_dir / "qa-research-gate-report.md"}`).
- `prompts.py:1064` — analyst synthesis review (`Output path: {config.qa_dir / "analyst-synthesis-review.md"}`).
- `prompts.py:1109` — QA synthesis-gate report (`Output path: {config.qa_dir / "qa-synthesis-gate-report.md"}`).
- `prompts.py:1267` — QA report validation (`Output path: {config.qa_dir / "qa-report-validation.md"}`).
- `prompts.py:1321` — QA qualitative review (`Output path: {config.qa_dir / "qa-qualitative-review.md"}`).
- `prompts.py:1451` — gap-fix output (`{config.qa_dir / f"gap-fix-{cycle:02d}-{failure_area_slug}.md"}`).

(Also note `build_verify_task_file_prompt` at `prompts.py:457-513` returns a JSON verdict and reads — does not write — a doc; not a pin target.)

---

## Summary

**File:** `/config/workspace/IronClaude/src/superclaude/cli/prd/prompts.py` — 1454 lines total.

**The 4 builders named in BUILD_REQUEST, with re-confirmed line numbers and exact injection anchors:**

| Builder | Def lines | Returned-fstring close | Pin injection anchor | Output kind |
|---------|-----------|------------------------|----------------------|-------------|
| `build_scope_discovery_prompt` | 110-191 | L191 | before `OUTPUT FORMAT:` at **L154** | markdown doc → `scope-discovery-raw.md` |
| `build_research_notes_prompt` | 194-266 | L266 | before "Produce a research-notes.md … 7 sections" at **L222** (NOT inside frontmatter L224-228) | markdown doc → `research-notes.md` |
| `build_sufficiency_review_prompt` | 269-319 | L319 | before `Return JSON:` at **L301** | **JSON verdict** (not a doc) |
| `build_preparation_prompt` | 516-558 | L558 | before `PREPARATION STEPS:` at **L539** | **marker** `.preparation-complete` (not `.md`) |

**Pattern to copy:** `Output path: {config.<dir> / "<file>.md"}` — verbatim exemplar at `prompts.py:887`; older `Write ... to:` variant at `prompts.py:439`.

**Key cross-cutting findings (act on these):**
1. Only 2 of the 4 (`scope_discovery`, `research_notes`) are genuine free-form markdown document producers with a section-list anchor. `sufficiency_review` returns JSON; `preparation` writes a dotfile marker. The builder agent / R2 must decide whether path-pinning those two is even meaningful.
2. `build_research_notes_prompt` has a DO-NOT-TOUCH frontmatter emission at **L224-228** and reads `scope-discovery-raw.md` at **L200** — both must survive the edit. Inject the pin before L222, not between L222-L228.
3. `Path` is imported at module level (L17); `PrdConfig` is imported ONLY under `TYPE_CHECKING` (L26-27) — fine for annotations under `from __future__ import annotations` (L13), NOT for runtime use.
4. Helper `_artifact_path_for_step(config, step_id)` inserts cleanly at blank **L53** (after `_today()` L50-52, before the Stage A banner L55-57).
5. `config.task_dir` is a Path used via `/` everywhere (e.g. L200, L116, L885) — `{config.task_dir / "<name>"}` in an f-string renders an absolute path, matching the existing pinned idiom.
6. 8 already-pinned builders must NOT receive a second pin: L439, L887, L956, L1064, L1109, L1267, L1321, L1451.

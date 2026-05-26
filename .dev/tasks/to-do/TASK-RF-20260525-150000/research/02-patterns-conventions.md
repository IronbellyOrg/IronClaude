# Research: Patterns & Conventions
**Topic type:** Patterns & Conventions
**Scope:** integration_contracts.py refactor — code style + project rules
**Status:** Complete
**Date:** 2026-05-25
---

## 1. Code Style — `integration_contracts.py` & siblings

### 1.1 Module docstring style

- **Triple-quoted docstring at line 1**, with a 1-line summary then blank line then a multi-paragraph body. Always ends with the **"Implements FR-MOD<X>.<Y>"** trailer when the module backs a numbered FR.
- Evidence:
  - `src/superclaude/cli/roadmap/integration_contracts.py:1-11` — `"""Integration contract extraction and verification."""` + body + `Implements FR-MOD2.1 through FR-MOD2.6.`
  - `src/superclaude/cli/roadmap/fingerprint.py:1-11` — identical shape, ends with `Implements FR-MOD3.1 through FR-MOD3.4.`
  - `src/superclaude/cli/roadmap/gates.py:1-10` — uses `--` (double hyphen) ASCII separator inside its docstring; not em-dash.

### 1.2 Imports

- `from __future__ import annotations` is **mandatory** at line 13 (right after module docstring + blank line).
  - `integration_contracts.py:13`, `fingerprint.py:13`, `gates.py:22`.
- Standard library imports use plain `import` (not `from`):
  - `import re` (`integration_contracts.py:15`, `fingerprint.py:15`).
- `from dataclasses import dataclass, field` — explicit names, no `*`.
  - `integration_contracts.py:16`, `fingerprint.py:16` uses only `dataclass` (no `field`).
- **Late-binding imports inside helper functions** are acceptable for one-shot use to keep module top clean:
  - `gates.py:55` (`import re; import warnings` inside `_cross_refs_resolve`).
  - `gates.py:146`, `gates.py:227`, `gates.py:255`, `gates.py:459`, `gates.py:476` etc. — `import re` reimported inside each gate-check helper.

### 1.3 Section banner / comment style

- Section banners use **triple-dash comments** above the section:
  ```
  # --- FR-MOD2.1: 7-category dispatch pattern scanner with compiled regexes ---
  ```
  - `integration_contracts.py:18`, `integration_contracts.py:110` (`# --- FR-MOD2.6: Dataclasses ---`), `integration_contracts.py:150` (`# --- Public API ---`), `integration_contracts.py:314` (`# --- Internal helpers ---`).
  - `gates.py:27` (`# --- Semantic check functions (pure: content -> bool) ---`), `gates.py:386` (`# --- DEVIATION_ANALYSIS_GATE semantic check functions ---`), `gates.py:1018` (`# --- GateCriteria instances ---`).
- **Inline comments above regexes** label each category, e.g. `# Category 1: Dict dispatch tables` at `integration_contracts.py:21`. Each `re.compile(...)` block is preceded by 1-2 line category comment.
- Comments referencing **FR-MOD<X>.<Y>** identifiers tie the regex/helper back to the requirement, e.g. `# FR-MOD2.3:` at `integration_contracts.py:75`, `# FR-MOD2.4:` at `integration_contracts.py:94`.

### 1.4 Regex compile style

- **Module-level compiled list of regexes** is the canonical pattern:
  ```python
  DISPATCH_PATTERNS = [
      re.compile(
          r"\b(?:...|...)\b",
          re.IGNORECASE,
      ),
      ...
  ]
  ```
  - `integration_contracts.py:20-73` — 7 compiled patterns in `DISPATCH_PATTERNS`.
  - `integration_contracts.py:75-107` — 4 compiled patterns in `WIRING_TASK_PATTERNS`.
- Multi-line regex strings use **concatenated raw strings** (`r"..."` chunks joined by line continuation), each line ≤ ~80 cols:
  ```python
  re.compile(
      r"\b(?:dispatch[_\s]?table|RUNNERS|_RUNNERS|HANDLERS|"
      r"DISPATCH|routing[_\s]?table|command[_\s]?map|step[_\s]?map|"
      r"plugin[_\s]?registry)\b",
      re.IGNORECASE,
  ),
  ```
  - See `integration_contracts.py:21-27`.
- Flags appear on their **own argument line** after the pattern string. Default flag is `re.IGNORECASE`. When the regex is case-sensitive (e.g., UPPER_SNAKE_CASE matching), the flag is **omitted entirely**:
  - `integration_contracts.py:95-98` (`PROGRAMMATIC_RUNNERS`, etc., no flag).
- One-off `re.compile` inside a function is also acceptable but reserved for non-module-level patterns:
  - `integration_contracts.py:270-275` (`impl_verbs = re.compile(...)`).
  - `gates.py:258-261` (`actionable_pattern = re.compile(...)`).
  - `gates.py:470` (`id_pattern = re.compile(r"^DEV-\d+$")`).

### 1.5 Dataclass style

- All dataclasses use **`@dataclass` decorator** (no kw_only, no frozen) and have a **1-line docstring** as the first statement:
  ```python
  @dataclass
  class IntegrationContract:
      """A single integration point extracted from a spec."""

      id: str  # IC-001, IC-002, ...
      mechanism: str  # "dispatch_table", "registry", "injection", etc.
      ...
  ```
  - `integration_contracts.py:113-122` (`IntegrationContract`).
  - `integration_contracts.py:125-132` (`WiringCoverage`).
  - `integration_contracts.py:135-142` (`IntegrationAuditResult`).
  - `fingerprint.py:19-25` (`Fingerprint`).
- **Field types use builtins**: `str`, `bool`, `list[...]` (PEP 585 lowercase). Not `List`, `Dict` from `typing`. Verified `integration_contracts.py:139-142` and `fingerprint.py:21-23`.
- **Inline `# trailing comments`** annotate each field's purpose / format (e.g., `# IC-001, IC-002, ...`). Comments stay on the same line as the field definition.
- **Default factories** use `field(default_factory=list)` for mutable collections:
  - `integration_contracts.py:139-140`: `contracts: list[IntegrationContract] = field(default_factory=list)`.
- **Scalar defaults inline**: `uncovered_count: int = 0` at `integration_contracts.py:141`.
- **Computed properties** declared with `@property` immediately after fields, each with **1-line docstring**:
  - `integration_contracts.py:144-147`:
    ```python
    @property
    def all_covered(self) -> bool:
        """Returns True only when uncovered_contracts == 0."""
        return self.uncovered_count == 0
    ```

### 1.6 Function naming, visibility, and signatures

- **Public API functions**: unprefixed snake_case (`extract_integration_contracts`, `check_roadmap_coverage`, `extract_code_fingerprints`, `check_fingerprint_coverage`, `fingerprint_gate_passed`).
- **Internal helpers**: single leading underscore (`_classify_mechanism`, `_extract_identifiers`, `_is_code_like`, `_parse_frontmatter`, `_strip_yaml_quotes`, `_normalize_heading`, all gate check fns).
  - `integration_contracts.py:317-356`.
  - `fingerprint.py:78-89`.
  - `gates.py:30-91`, `gates.py:150-165`, `gates.py:168-189` etc.
- **All public functions have type-annotated signatures and a docstring**:
  ```python
  def extract_integration_contracts(spec_text: str) -> list[IntegrationContract]:
      """Extract integration contracts from spec text using pattern matching.

      FR-MOD2.1: ...
      FR-MOD2.2: ...

      Returns a list of IntegrationContract instances.
      """
  ```
  - `integration_contracts.py:153-161`.
  - `integration_contracts.py:205-217` (`check_roadmap_coverage`).
- **Multi-line return type or arg lists** use the same trailing-comma + paren-indent style:
  ```python
  def check_roadmap_coverage(
      contracts: list[IntegrationContract],
      roadmap_text: str,
  ) -> IntegrationAuditResult:
  ```
  - `integration_contracts.py:205-208`.
  - `fingerprint.py:156-160` (`check_fingerprint_coverage` with three args + default value `min_coverage_ratio: float = 0.7`).

### 1.7 Docstring style

- **One-line docstrings** for simple internal helpers:
  - `integration_contracts.py:318`: `"""Classify matched text into a mechanism category."""`
  - `gates.py:131-132`: `"""All YAML frontmatter fields have non-empty values."""`
- **Multi-line docstrings** for public functions, structured as:
  1. 1-line summary
  2. Blank line
  3. FR-MOD or rule references, each on its own line
  4. Blank line
  5. `Returns ...` line
  - Example `integration_contracts.py:154-161`.
- **Long-form behavioral docstrings** use plain prose paragraphs separated by blank lines, with `Returns False if:` / `Returns True iff:` style lists for fail-closed checks:
  - `gates.py:172-184` (`_parse_frontmatter`).
  - `gates.py:192-203` (`_high_severity_count_zero`).
  - `gates.py:317-322` (`_no_undischarged_obligations`).

### 1.8 Inline-narration comments inside functions

- **Block-level prose comments** inside functions explain WHY (not WHAT):
  - `integration_contracts.py:168-174` — explains why markdown headings and TOC links are skipped.
  - `integration_contracts.py:184-187` — `# FR-MOD2.2: Context capture (3 lines before/after)`.
  - `integration_contracts.py:254-260` — multi-line `# FR-MOD2.7: Broad mechanism-term coverage check.` block, 7 lines of rationale.
- **Comments referencing the merged-fix branch / tickets** stay close to the code they justify:
  - `integration_contracts.py:46-48` — `Bare "Strategy" removed — it matches headings like "Testing Strategy" and "Migration Strategy" which are document structure, not code patterns.` — explains a behavior tweak with rationale.

### 1.9 Type-hint conventions

- **Python 3.10+ syntax**: `str | None`, `dict[str, str]`, `list[Foo]`, `set[str]`, `tuple[int, int, list[str], float]`.
  - `gates.py:94` (`bool | str`), `gates.py:102` (`dict[str | None, set[str]]`), `gates.py:168` (`dict[str, str] | None`).
  - `fingerprint.py:160` (`-> tuple[int, int, list[str], float]:`).
- **Variable annotations inside functions** used when collection type isn't obvious:
  - `integration_contracts.py:162` (`contracts: list[IntegrationContract] = []`).
  - `integration_contracts.py:164` (`seen_evidence: set[str] = set()`).
  - `gates.py:60` (`headings: set[str] = set()`).

### 1.10 String conventions

- **f-strings** for runtime composition:
  - `integration_contracts.py:192-196` (`id=f"IC-{counter:03d}"`, `spec_location=f"line {i + 1}"`).
  - `gates.py:111` (multi-line f-string for failure message).
- **Plain string literals** for constants and patterns.
- **ID format**: `f"IC-{counter:03d}"` — zero-padded to 3 digits.

---

## 2. Test Style — `test_integration_contracts.py` & sibling integration tests

### 2.1 Module docstring + import style

- **Module docstring** matches code style: 1-line summary + numbered bullets + closing line.
  - `tests/roadmap/test_integration_contracts.py:1-10`:
    ```
    """Unit tests for integration_contracts.py.

    Tests cover:
    1. 7-category dispatch pattern detection (FR-MOD2.1)
    ...

    All tests use real content fixtures, no mocks.
    """
    ```
- **Imports** in unit tests are flat (no `from __future__ import annotations` needed but allowed):
  - `test_integration_contracts.py:12-16`:
    ```python
    from superclaude.cli.roadmap.integration_contracts import (
        IntegrationAuditResult,
        check_roadmap_coverage,
        extract_integration_contracts,
    )
    ```
- **Integration tests** add `from __future__ import annotations` + stdlib imports:
  - `test_anti_instinct_integration.py:14-17` (`from __future__ import annotations` then `import textwrap` then `from pathlib import Path`).

### 2.2 Fixture / test-data style

- **Module-level multi-line string fixtures** named in `UPPER_SNAKE_CASE` with `\` continuation to suppress leading newline:
  - `test_integration_contracts.py:18` (`# --- Real content fixtures ---` section banner).
  - `test_integration_contracts.py:20-26` (`DISPATCH_TABLE_SPEC = """\\\n..."""`).
  - `test_integration_contracts.py:28-31` (`REGISTRY_SPEC`).
  - Pattern continues for all 7 categories.
- **Composite fixtures concatenated explicitly**:
  - `test_integration_contracts.py:58-72` (`ALL_CATEGORIES_SPEC = DISPATCH_TABLE_SPEC + "\n" + REGISTRY_SPEC + ...`).
- **Integration tests** use `textwrap.dedent("""...""")` inside `_make_*_spec`/`_make_*_roadmap` helpers:
  - `test_anti_instinct_integration.py:140-170` (`spec.write_text(textwrap.dedent("""\\\n#..."""))`).
- **NO pytest fixtures (`@pytest.fixture`) in `test_integration_contracts.py`** — pure data constants only. No mocks.

### 2.3 Test class structure

- **One `TestXxxYyy` class per FR or scenario**, each with a single-line docstring referencing the FR ID:
  - `test_integration_contracts.py:130-131`:
    ```python
    class TestDispatchPatternDetection:
        """FR-MOD2.1: 7-category dispatch pattern detection."""
    ```
  - Also: `TestWiringCoverage` (l. 182), `TestDeduplication` (l. 211), `TestNamedMechanismMatching` (l. 230), `TestCliPortifyRegression` (l. 245), `TestIntegrationAuditResult` (l. 263).
- **Test classes are PascalCase, starting with `Test`** (pytest collection convention).
- **Integration test classes** follow the same pattern but with `_make_*` private helpers inside the class:
  - `test_anti_instinct_integration.py:130-200` (`class TestSC001RegressionBlocks` with `_make_bad_spec` / `_make_bad_roadmap` helpers).

### 2.4 Test method naming

- `test_<scenario>_<behavior>` lowercase snake_case.
- Common prefixes: `test_category{N}_<name>`, `test_<thing>_passes_on_<input>`, `test_<thing>_fails_on_<input>`, `test_detects_<bug>`.
  - Examples: `test_category1_dispatch_table` (l. 133), `test_covered_roadmap_passes` (l. 185), `test_uncovered_roadmap_fails` (l. 191), `test_detects_programmatic_runners_without_wiring` (l. 248).
- **Often no method docstring** — name carries the spec. Some methods do have 1-line docstrings:
  - `test_anti_instinct_integration.py:60` (`"""anti-instinct step appears in _build_steps() output."""`).

### 2.5 Assertion style

- **Plain `assert` statements** with no `pytest.raises` unless testing exceptions.
- Assertions on **set membership** and **counts**:
  ```python
  mechanisms = {c.mechanism for c in contracts}
  assert "dispatch_table" in mechanisms
  ```
  - `test_integration_contracts.py:136-137`.
- Assertions check **count thresholds**, not exact equality, where deduplication or counter behavior is involved:
  - `test_integration_contracts.py:135` (`assert len(contracts) >= 1`), `test_integration_contracts.py:179` (`assert len(mechanisms) >= 4`).
- **Custom failure messages** appear on critical asserts:
  - `test_anti_instinct_integration.py:218` (`assert len(contracts) > 0, "Spec should yield integration contracts"`).
  - `test_anti_instinct_integration.py:241-243`:
    ```python
    assert not passed, (
        f"Gate should fail but passed. File content: {audit_file.read_text()[:500]}"
    )
    ```
- **Identity asserts on bool returns** for fail-closed checks:
  - `test_anti_instinct_integration.py:487` (`assert _no_undischarged_obligations(content) is True`).

### 2.6 Pytest features used

- **`tmp_path` builtin fixture** is the canonical filesystem fixture (no custom tmpdir helpers):
  - `test_anti_instinct_integration.py:60`, etc.
- **No parametrize used in `test_integration_contracts.py`** — explicit one-method-per-category style.
- **No markers on these specific tests** — `@pytest.mark.confidence_check` / `self_check` / `reflexion` markers exist project-wide but are NOT used in this file.

### 2.7 Real-content vs synthetic

- Project-wide rule per `tests/roadmap/test_integration_contracts.py:10`: `"""All tests use real content fixtures, no mocks."""`
- The cli-portify regression test uses **near-verbatim text** from the failing case (`PROGRAMMATIC_RUNNERS`, `_run_programmatic_step`):
  - `test_integration_contracts.py:97-127`.
- Integration tests synthesize spec/roadmap content via `textwrap.dedent` but the text mimics real spec/roadmap structure (frontmatter, phases, code-fenced blocks).

---

## 3. Project Workflow Rules

### 3.1 UV-only Python

- `CLAUDE.md` (project) lines 5-15: `**CRITICAL**: This project uses **UV** for all Python operations. Never use python -m, pip install, or python script.py directly.`
- `CLAUDE.md` (global) line 9-15: same rule, reinforced as Rule #1: `**UV only** — never python -m or bare pip`.
- Test invocation: `uv run pytest tests/roadmap/test_integration_contracts.py -v` (NOT `python -m pytest`).
- Dep install: `uv pip install package` (NOT bare `pip install`).
- Script run: `uv run python script.py` (NOT bare `python script.py`).

### 3.2 Source-of-truth + sync-dev workflow (CRITICAL)

- Project `CLAUDE.md` lines 86-101 (Component Sync):
  - SoT: `src/superclaude/` — canonical location.
  - Dev copies: `.claude/skills/` and `.claude/agents/` are convenience.
  - Workflow:
    1. Edit `src/superclaude/skills/` or `src/superclaude/agents/`.
    2. Run `make sync-dev`.
    3. Run `make verify-sync` (also before committing).
- **For this refactor**: target file is `src/superclaude/cli/roadmap/integration_contracts.py`. This is `cli/` not `skills/` or `agents/`, so `sync-dev` does NOT apply (it's pure Python source code, not a synced asset). NO sync step needed for the refactor itself.
- **However**: if any skill/agent/command references the changed module behaviorally and the doc needs updating, edit under `src/superclaude/skills/...` then `make sync-dev`.

### 3.3 `.claude/` commit ban (ABSOLUTE)

- Project `CLAUDE.md` lines 21-39 (ABSOLUTE RULE: Never Stage or Commit `.claude/` Contents):
  - `.claude/{skills,commands,agents,hooks,templates}/*` is gitignored sync-dev output.
  - Only tracked `.claude/` file is `.claude/settings.json`.
  - **NEVER** `git add .claude/skills/...`, `git add -f` on `.claude/`, etc.
  - **The `-f` rule**: `git add -f` on any `.claude/` path is a siren — STOP, fix in `src/superclaude/`, then `make sync-dev`.
- For this refactor: no `.claude/` paths should be touched. All edits go to `src/superclaude/cli/roadmap/` + `tests/roadmap/`.

### 3.4 Git workflow

- Project `CLAUDE.md` lines 233-241 (Git Workflow):
  - Branch structure: `master` ← `integration` ← `feature/*`, `fix/*`, `docs/*`.
  - Feature branches only — never commit directly to `master`/`main`.
  - Conventional commits: `feat:`, `fix:`, `docs:`, `chore:`, `refactor:`.
  - PR target: branch from `integration`, merge through `integration` → `master`.
- Global `CLAUDE.md` Rule #4: `**Git** — feature branches only; never commit directly to master/main`.

### 3.5 Confidence-check trigger (≥90% gate)

- Global `CLAUDE.md` Rule #3: `**Confidence check** — ≥90% proceed, 70-89% present options, <70% ask. Trigger surface is not just code edits: run it (or its lightweight form — verify the specific token via --help/grep/file read/codebase-retrieval) BEFORE any reply that suggests an action, emits a command/snippet, or names a specific flag/path/function/version. Recommendation = action.`
- For this refactor: confidence-check skill should be invoked before implementation begins, per the F1 execution loop in `task` skill.

### 3.6 Auggie-first / parallel-by-default

- Global Rule #9: `**Auggie first** — call codebase-retrieval before significant edits to load relevant context`.
- Global Rule #2: `**Parallel by default** — batch independent tool calls; sequential only for true dependencies`.
- Implementation reads should be parallelized; sibling-style consistency checks should leverage `codebase-retrieval` before editing.

### 3.7 Finish-what-you-start + scope discipline

- Global Rule #7: `**Finish what you start** — no TODO stubs for core logic`.
- Global Rule #8: `**Scope discipline** — build exactly what's asked; no speculative additions`.
- For the merged Fix B refactor: implement only what the merged-output.md spec calls for. No drive-by enhancements.

---

## 4. Verification Commands (UV-only)

### 4.1 Test commands

```bash
# Full suite (after edits)
make test
# == uv run pytest

# Target the affected files
uv run pytest tests/roadmap/test_integration_contracts.py -v
uv run pytest tests/roadmap/test_anti_instinct_integration.py -v

# Run with coverage
uv run pytest --cov=superclaude tests/roadmap/

# By marker (not used in these files, but available)
uv run pytest -m confidence_check
```

(From project `CLAUDE.md` lines 117-127, Testing section.)

### 4.2 Lint + format

```bash
make lint     # ruff check
make format   # ruff format
```

(From project `CLAUDE.md` lines 129-131.)

### 4.3 Sync verification

```bash
make sync-dev      # if any src/superclaude/skills|agents|commands edited
make verify-sync   # confirm src/ and .claude/ match — ALWAYS run before commit
```

(From project `CLAUDE.md` lines 134-136 and 99.)

### 4.4 Health check

```bash
make doctor    # diagnostic health check
make verify    # verify installation (package, plugin, health)
```

(From project `CLAUDE.md` lines 132, 116.)

### 4.5 Targeted reproducer (anti-instinct gate)

The merged Fix B refactor explicitly touches `_run_anti_instinct_audit` flow. The integration test class `TestSC001RegressionBlocks` (`tests/roadmap/test_anti_instinct_integration.py:130-265`) is the load-bearing reproducer; must remain green:

```bash
uv run pytest tests/roadmap/test_anti_instinct_integration.py::TestSC001RegressionBlocks -v
```

---

## 5. Conventions Summary Cheat-Sheet (for the refactor implementation)

| Aspect | Convention | Citation |
|---|---|---|
| Module top | `"""<summary>..."""` ending with `Implements FR-MOD<X>.<Y>.` | `integration_contracts.py:1-11` |
| Future imports | `from __future__ import annotations` mandatory after docstring | `integration_contracts.py:13` |
| Section banner | `# --- <FR-ID>: <name> ---` | `integration_contracts.py:18,110,150,314` |
| Regex grouping | Module-level `LIST = [re.compile(...)]` with category comments above each | `integration_contracts.py:20-73` |
| Multi-line regex | Raw-string chunks joined, flag arg on its own line | `integration_contracts.py:21-27` |
| Case-sensitive regex | Omit `re.IGNORECASE` entirely | `integration_contracts.py:95-98` |
| Dataclass | `@dataclass` + 1-line docstring + trailing `# inline` comments per field | `integration_contracts.py:113-122` |
| Mutable defaults | `field(default_factory=list)` | `integration_contracts.py:139-140` |
| Computed members | `@property` immediately after fields, 1-line docstring, simple return | `integration_contracts.py:144-147` |
| Public API | snake_case, no leading underscore, full docstring | `integration_contracts.py:153,205` |
| Internal helper | `_snake_case`, 1-line docstring | `integration_contracts.py:317,347` |
| Types | PEP 585 builtins: `list[X]`, `dict[K, V]`, `X \| None` | `gates.py:94,168` |
| String ID format | `f"IC-{counter:03d}"` zero-padded | `integration_contracts.py:192` |
| Test fixtures | Module-level `UPPER_SNAKE_CASE = """\\\n..."""` strings, no mocks | `test_integration_contracts.py:20-72` |
| Test class | `TestXxxYyy: """FR-MOD<X>.<Y>: <name>."""` | `test_integration_contracts.py:130-131` |
| Test method | `test_<scenario>_<behavior>`, often no docstring | `test_integration_contracts.py:133` |
| Filesystem fixtures | Use builtin `tmp_path`, dedent multi-line content | `test_anti_instinct_integration.py:140-170` |
| Assertions | Plain `assert`, sometimes with f-string message; `is True` / `is False` for bool returns | `test_anti_instinct_integration.py:487` |
| Python ops | `uv run pytest`, `uv pip install`, never bare python/pip | `CLAUDE.md:5-15` |
| Edits to `.claude/` | FORBIDDEN; edit `src/superclaude/` then `make sync-dev` | `CLAUDE.md:21-39` |
| Branch | `feature/*` or `fix/*` off `integration`; never commit to `master` | `CLAUDE.md:233-241` |
| Pre-commit | `make verify-sync && make lint && make test` | `CLAUDE.md:99,117-131` |

---

## Summary

The refactor must use **PEP 585 builtins**, **`from __future__ import annotations`**, **module-level compiled regex lists with category comments**, **`@dataclass` + inline-comment fields**, and **`_snake_case` for internal helpers**. Tests must continue the **module-level UPPER_SNAKE_CASE multi-line string fixture pattern** (no mocks, no pytest fixtures) and group methods under **`TestXxxYyy: """FR-MOD<X>.<Y>:..."""`** classes. All Python operations go through **UV** (`uv run pytest`, `make test`), edits target **`src/superclaude/`** (no `.claude/` staging — absolute rule), and verification is **`make verify-sync && make lint && make test`** on a `feature/*` or `fix/*` branch off `integration`.

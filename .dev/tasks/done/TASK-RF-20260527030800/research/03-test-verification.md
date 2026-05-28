# Research 03: Test & Verification

**Status:** Complete
**Date:** 2026-05-27
**Researcher:** Quick tier, 3 of 3 (Test-side)
**Topic:** Test infrastructure for cosmetic_remediator — C12 + C13 slot-in analysis

---

## 1. Test file structure — every test class in `test_cosmetic_remediator.py`

File: `/config/workspace/IronClaude/tests/roadmap/test_cosmetic_remediator.py` (428 lines, 21 tests, all passing in 0.14s)

| Class | file:line | Purpose |
|---|---|---|
| `TestClassifierBasics` | `test_cosmetic_remediator.py:50` | Non-roadmap gates, `{{SC_PLACEHOLDER}}` sentinels, OQ-xxx-in-deliverable → all classify as semantic (NOT pure cosmetic) |
| `TestMilestoneH3Defects` | `test_cosmetic_remediator.py:98` | **C1-C4 transforms**: stem aliases, missing `-- M{N}` suffix, `u2014` literal, em-dash normalization, full TUIBBS failure shape end-to-end |
| `TestNonH3Cosmetics` | `test_cosmetic_remediator.py:189` | **C5-C10 transforms**: trailing whitespace, blank-line collapse, smart quotes, frontmatter ws |
| `TestIdempotency` | `test_cosmetic_remediator.py:262` | Canonical-input no-op + idempotency + **C11 resource-subsection alias** (line 294) + mixed-cosmetic-and-semantic refusal |
| `TestClassificationDataclass` | `test_cosmetic_remediator.py:342` | Round-trip of `gate_name` / `step_id` through `Classification` |
| `TestComputeFencedIndices` | `test_cosmetic_remediator.py:362` | M1 perf-refactor parity for `_compute_fenced_indices` vs `_is_in_fenced_block` |

**Slot-in recommendation:**

- **C12 tests (H2 parenthetical strip)** — new class `TestC12H2ParentheticalStrip` placed AFTER `TestNonH3Cosmetics` and BEFORE `TestIdempotency` (so the file reads C1-C4 → C5-C10 → **C12** → C11+idempotency → dataclass → fenced). C12 is structurally an H2-level transform, semantically closest to C5/C6/C10 (canonicalization), so the position-after-C10 grouping reads naturally.
- **C13 tests (gap-driven H3 repair under known parent H2s)** — co-located with C11 inside `TestIdempotency` (since C13 is the gap-driven counterpart to C11's alias-table approach and shares the `## Resource Requirements and Dependencies` parent H2 testbed). OR introduce a fresh class `TestC13GapDrivenH3Repair` immediately after `TestIdempotency` if the test count grows past 3-4.

---

## 2. Helper functions

### Existing helper (quoted verbatim)

`test_cosmetic_remediator.py:23-39`:

```python
def _content_with_milestone(
    subsections: list[str],
    *,
    mid: str = "1",
    frontmatter: str = "---\nspec_source: epics.md\n---\n",
    extras: str = "",
) -> str:
    """Assemble a minimal roadmap-ish markdown with one milestone."""
    h2 = f"## M{mid}: Foundation\n\nObjective: x | Duration: y | Exit: z\n\n"
    subs = "\n\n".join(subsections) + "\n"
    return (
        frontmatter
        + "\n# Test Roadmap\n\n## Executive Summary\nfoo\n\n"
        + h2
        + subs
        + extras
    )
```

**Critical limitation for C12 + C13**: `_content_with_milestone` produces a single milestone H2 + arbitrary H3 subsections under it. It does NOT produce:

- A `## Resource Requirements and Dependencies` parent H2 with arbitrary H3 children (needed for C13 gap-driven repair tests)
- A parenthetical-bearing H2 like `## Timeline Estimates (gate-bound, not date-bound)` (needed for C12 strip tests)

The existing C11 test at `test_cosmetic_remediator.py:294-316` works around this by hand-building the full document inline (lines 298-308) — see quote in §3. The same inline-hand-build pattern is acceptable for C12 + C13 too, but **the test file would be cleaner with a dedicated helper**.

### Proposed minimal helpers (for C12 + C13)

```python
def _content_with_h2_parenthetical(
    h2_name: str = "Timeline Estimates",
    parenthetical: str = " (gate-bound, not date-bound)",
    *,
    frontmatter: str = "---\nspec_source: epics.md\n---\n",
) -> str:
    """Roadmap with one required H2 carrying a non-canonical parenthetical suffix."""
    return (
        frontmatter
        + "\n# T\n\n## Executive Summary\nfoo\n\n"
        + "## M1: F\n\nb\n\n"
        + "### Integration Points -- M1\n"
        + "### Milestone Dependencies -- M1\n"
        + "### Risk Assessment and Mitigation -- M1\n\n"
        + f"## {h2_name}{parenthetical}\n\nbody\n"
    )


def _content_with_resource_subsections(
    subsections: list[str],
    *,
    frontmatter: str = "---\nspec_source: epics.md\n---\n",
) -> str:
    """Roadmap with `## Resource Requirements and Dependencies` and arbitrary H3 children.

    Subsections is a list of H3 lines (caller supplies leading `### `).
    Use to drive C13 gap-repair tests against opus-flavored renames like
    `### External library lockset` that share no substring with the canonical
    `External Dependencies` but DO share a token (`External`).
    """
    subs = "\n\n".join(subsections) + "\n"
    return (
        frontmatter
        + "\n# T\n\n## Executive Summary\nfoo\n\n"
        + "## M1: F\n\nb\n\n"
        + "### Integration Points -- M1\n"
        + "### Milestone Dependencies -- M1\n"
        + "### Risk Assessment and Mitigation -- M1\n\n"
        + "## Resource Requirements and Dependencies\n\n"
        + subs
    )
```

These mirror `_content_with_milestone`'s minimal-but-gate-satisfying scaffold (every other required section present), so the only variable each test is asserting on is the C12 / C13 transform under inspection.

---

## 3. Representative test (the assert pattern)

C11 test at `test_cosmetic_remediator.py:294-316` is the closest analog for C12 + C13 (same parent H2, same alias-vs-canonical pattern, hand-built body):

```python
def test_c11_resource_subsection_alias_fixed(self):
    # The actual TUIBBS-secondary failure: long-form ``External Dependencies
    # (PRD-confirmed, TDD-pinned)`` and short ``Infrastructure`` under
    # ``## Resource Requirements and Dependencies`` should both normalize.
    content = (
        "---\nspec_source: epics.md\n---\n"
        "# Test\n\n## Executive Summary\nfoo\n\n"
        "## M1: F\n\nb\n\n"
        "### Integration Points -- M1\n"
        "### Milestone Dependencies -- M1\n"
        "### Risk Assessment and Mitigation -- M1\n\n"
        "## Resource Requirements and Dependencies\n\n"
        "### External dependencies (PRD-confirmed, TDD-pinned)\n\nfoo\n\n"
        "### Infrastructure\n\nbar\n"
    )
    cl = classify_gate_failure(content, _GATE, "x", step_id="s1")
    assert cl.is_pure_cosmetic is True
    assert any(v.klass == "C11" for v in cl.cosmetic_violations)
    new, transforms = apply_cosmetic_remediations(content, cl)
    assert "### External Dependencies\n" in new
    assert "### Infrastructure Requirements\n" in new
    assert "(PRD-confirmed" not in new  # the parenthetical metadata is gone
    assert sum(1 for t in transforms if "resource H3" in t) == 2
```

**Canonical assert pattern observed (every passing test uses this 4-step shape):**

1. Build content inline (or via `_content_with_milestone`)
2. `cl = classify_gate_failure(content, _GATE, "x", step_id="s1")`
3. `assert cl.is_pure_cosmetic is True` (and optionally `assert any(v.klass == "CXX" for v in cl.cosmetic_violations)`)
4. `new, transforms = apply_cosmetic_remediations(content, cl)`
5. Assert canonical strings appear in `new`, non-canonical strings do NOT appear, and `transforms` list has expected length / contains expected substring tags

C12 + C13 tests should mirror this 5-line shape verbatim.

---

## 4. End-to-end gate test — CRITICAL ABSENCE FINDING

**Grep result** (`grep -rn "_template_sections_present" /config/workspace/IronClaude/tests/` cross-referenced with `grep -rn "apply_cosmetic_remediations" /config/workspace/IronClaude/tests/`):

- `_template_sections_present` is referenced in **4 test files**:
  - `tests/roadmap/test_gates_data.py:43` (imports it; `TestTemplateSectionsPresent` class at `:354` exhaustively tests it standalone with `_minimal_valid_roadmap` builder at `:357-422`)
  - `tests/roadmap/test_integration_v5_pipeline.py:164` (helper docstring only — references the gate by name, doesn't call it on remediator output)
  - `tests/roadmap/test_pipeline_integration.py:66` (helper docstring only — same)
  - `tests/roadmap/test_eval_gate_rejection.py:50` (helper docstring only — same)

- `apply_cosmetic_remediations` is referenced in **2 test files**:
  - `tests/roadmap/test_cosmetic_remediator.py` (16 call sites — all unit-scope)
  - `tests/roadmap/test_executor.py:1177` (docstring only — `TestCosmeticRemediatorExceptionFallthrough` tests the executor's exception fallthrough path, not the gate recheck)

**Cross-check** (`grep -n "apply_cosmetic_remediations" tests/roadmap/test_gates_data.py tests/roadmap/test_integration_v5_pipeline.py tests/roadmap/test_pipeline_integration.py tests/roadmap/test_eval_gate_rejection.py` — empty output).

### Finding

**No test in `tests/roadmap/` invokes `_template_sections_present` on the OUTPUT of `apply_cosmetic_remediations`.** The two functions are tested in complete isolation. This is exactly the integration gap that produced the TUIBBS halt described in the validation REPORT (§8 below) — `apply_cosmetic_remediations` returned `is_pure_cosmetic=True, transforms=22`, then `_template_sections_present(remediated_content)` returned `False`, and the pipeline halted via `executor.py:349-352` ("Remediator claimed success but gate still fails -- fall through to the original FAIL path").

**Required new integration test for C12 + C13:** at least one test must invoke

```python
from superclaude.cli.roadmap.gates import _template_sections_present
# ... build content with H2 parenthetical drift + resource-subsection rename ...
cl = classify_gate_failure(content, _GATE, "x", step_id="s1")
new, _ = apply_cosmetic_remediations(content, cl)
assert _template_sections_present(new) is True  # <-- THE GATE THAT WAS NEVER ASSERTED
```

Recommended placement: a new test class `TestPostRemediationGatePasses` at the end of `test_cosmetic_remediator.py` (or in a fresh file `test_cosmetic_remediator_integration.py` if it grows). The class should cover:

- C12 alone (H2 parenthetical → gate passes post-remediation)
- C13 alone (gap-driven H3 repair → gate passes post-remediation)
- C12 + C13 + C11 combined (the actual TUIBBS-shaped artifact → gate passes post-remediation)

This integration test is the load-bearing regression guard against the failure mode the REPORT documents empirically.

---

## 5. Idempotency tests

**One existing idempotency test** at `test_cosmetic_remediator.py:280-292`:

```python
def test_remediation_is_idempotent(self):
    content = _content_with_milestone(
        [
            "### Integration Points",
            "### Milestone Dependencies",
            "### Risk Assessment",
        ]
    )
    cl1 = classify_gate_failure(content, _GATE, "x", step_id="s1")
    once, _ = apply_cosmetic_remediations(content, cl1)
    cl2 = classify_gate_failure(once, _GATE, "x", step_id="s1")
    twice, _ = apply_cosmetic_remediations(once, cl2)
    assert once == twice
```

**Coverage:** C1 + C2 (milestone H3 stem and suffix). Does NOT cover C11 (resource H3 alias) — the C11 test at `:294-316` asserts the rewrite happens once but never re-runs the pipeline to assert no second mutation.

**For C12 + C13:** the existing pattern (`apply_cosmetic_remediations` → `classify_gate_failure` again → `apply_cosmetic_remediations` again → `assert once == twice`) should be replicated as two new tests, one per transform. Critical because:

- C12 strips parentheticals; a buggy implementation could keep matching the same H2 and re-stripping a now-empty suffix indefinitely (no-op but classifier might still flag).
- C13 renames an H3 to its canonical name; a buggy implementation could see the canonical name and rename it AGAIN (e.g. if the gap-set computation doesn't subtract the just-renamed H3).

Both are realistic failure modes that the idempotency contract catches.

---

## 6. UV-only pytest invocation (verbatim from CLAUDE.md)

From `/config/workspace/IronClaude/CLAUDE.md:60-114`:

```
uv run pytest                    # Run tests
uv run pytest tests/pm_agent/   # Run specific tests
...
uv run pytest tests/pm_agent/ -v              # Run specific directory
uv run pytest tests/test_file.py -v           # Run specific file
uv run pytest -m confidence_check             # Run by marker
uv run pytest --cov=superclaude               # With coverage
```

**Exact command the new task file MUST use for C12 + C13 verification (from `cwd=/config/workspace/IronClaude`):**

```bash
uv run pytest tests/roadmap/test_cosmetic_remediator.py -v
```

Or, scoped to the new class only:

```bash
uv run pytest tests/roadmap/test_cosmetic_remediator.py::TestC12H2ParentheticalStrip -v
uv run pytest tests/roadmap/test_cosmetic_remediator.py::TestPostRemediationGatePasses -v
```

User-global CLAUDE.md (`/config/.claude/CLAUDE.md`) reinforces: **"UV only — never `python -m` or bare `pip`"**. The task file MUST NOT emit `pytest ...`, `python -m pytest ...`, or `python script.py ...`.

---

## 7. Test runtime — baseline on master

Command run (per CLAUDE.md): `cd /config/workspace/IronClaude && uv run pytest tests/roadmap/test_cosmetic_remediator.py -v 2>&1 | tail -40`

**Result:**

```
============================= test session starts ==============================
platform linux -- Python 3.12.3, pytest-9.0.3, pluggy-1.6.0 -- /config/workspace/IronClaude/.venv/bin/python3
...
collected 21 items
...
21 passed in 0.14s
```

**Baseline:** 21/21 passing, 0.14s runtime on branch `chore/anti-instinct-exclude-prose-keywords`. The new C12 + C13 tests start from a clean green baseline; any failure introduced by the C12/C13 implementation will be unambiguously attributable to the new code.

**Note on environment:** the `uv run` invocation emits one warning — `VIRTUAL_ENV=/lsiopy does not match the project environment path .venv and will be ignored`. This is cosmetic (uv uses `.venv` correctly) and present on every test run in this repo. The task file should not treat this warning as a failure signal.

---

## 8. Validation REPORT reproducer — seed for the integration test

**File:** `/config/workspace/TUIBBS-scp/.dev/troubleshoot/validation-opus-mixed-drift-20260527023700/REPORT.md`
**Reproducer location:** `REPORT.md:36-47` (under the "Reproducer (re-runnable from any IronClaude checkout)" header at line 34).

**Verbatim reproducer (REPORT.md:36-47):**

```bash
uv --project /config/workspace/IronClaude run python -c "
from superclaude.cli.roadmap.cosmetic_remediator import classify_gate_failure, apply_cosmetic_remediations
from superclaude.cli.roadmap.gates import _template_sections_present
from pathlib import Path
c = Path('/config/workspace/TUIBBS-scp/.dev/releases/current/v1-MVP/roadmap-opus-architect.md.bak-pre-mixed-drift-fix').read_text()
cl = classify_gate_failure(c, 'template_sections_present', '', step_id='generate-opus-architect')
r, t = apply_cosmetic_remediations(c, cl)
print(cl.is_pure_cosmetic, len(cl.cosmetic_violations), len(cl.semantic_violations), _template_sections_present(r))
"
# Outputs: True 22 0 False
```

**What it asserts** (decoded from REPORT.md:21-32 empirical evidence block):

- `cl.is_pure_cosmetic == True` (classifier sees only cosmetic violations)
- `len(cl.cosmetic_violations) == 22` (breakdown: `C3 × 15, C1 × 5, C7 × 1, C11 × 1`)
- `len(cl.semantic_violations) == 0` (NO semantic violations — the `mixed=halt` rule does NOT fire)
- `_template_sections_present(r) == False` ← **this is the bug**: the remediator ran cleanly but two drift sites (H2 parenthetical `## Timeline Estimates (gate-bound, not date-bound)`, opus rename `### External library lockset`) have **no C-class detector at all**, so they survive into `r` and the gate still fails.

### How this seeds the new integration test

The new C12 + C13 implementation will, by construction, add transformers for exactly those two drift sites. The integration test contract is:

```python
def test_c12_c13_post_remediation_gate_passes_on_tuibbs_artifact_shape(self):
    """The shape that produced the TUIBBS halt (REPORT.md reproducer) must now
    flow through apply_cosmetic_remediations and produce content that passes
    _template_sections_present on the SAME call sequence."""
    # Build minimal content reproducing both drift sites: H2 parenthetical
    # (C12 target) AND "External library lockset" rename (C13 target).
    content = (
        "---\nspec_source: epics.md\n---\n"
        "# T\n\n## Executive Summary\nfoo\n\n"
        "## Milestone Summary\n\nfoo\n\n"
        "## Dependency Graph\n\nfoo\n\n"
        "## M1: F\n\nb\n\n"
        "### Integration Points -- M1\n"
        "### Milestone Dependencies -- M1\n"
        "### Risk Assessment and Mitigation -- M1\n\n"
        "## Resource Requirements and Dependencies\n\n"
        "### External library lockset\n\nfoo\n\n"        # C13 target
        "### Infrastructure Requirements\n\nbar\n\n"
        "## Risk Register\n\nfoo\n\n"
        "## Success Criteria and Validation Approach\n\nfoo\n\n"
        "## Decision Summary\n\nfoo\n\n"
        "## Timeline Estimates (gate-bound, not date-bound)\n\nfoo\n"  # C12 target
    )
    # Pre-condition: gate currently fails on this content
    assert _template_sections_present(content) is False
    cl = classify_gate_failure(content, _GATE, "x", step_id="s1")
    assert cl.is_pure_cosmetic is True
    new, transforms = apply_cosmetic_remediations(content, cl)
    # Post-condition: the gate that was never asserted on remediator output now passes
    assert _template_sections_present(new) is True
    assert "Timeline Estimates (gate-bound" not in new       # C12 strip happened
    assert "### External Dependencies" in new                # C13 rename happened
```

This test directly mirrors the reproducer's `cl.is_pure_cosmetic AND _template_sections_present(r)` chain and would fail on master (because C12 + C13 don't exist yet) — making it the integration regression guard the suite is currently missing.

**Helper reuse:** the `_minimal_valid_roadmap` builder at `test_gates_data.py:357-422` constructs a roadmap satisfying every required H2; the new integration test could subclass-pattern that builder to inject the two drift sites without re-typing the 16-line scaffold. Sketch:

```python
# In test_cosmetic_remediator.py, import the existing builder
from tests.roadmap.test_gates_data import TestTemplateSectionsPresent

base = TestTemplateSectionsPresent._minimal_valid_roadmap()
drifted = (
    base
    .replace("## Timeline Estimates", "## Timeline Estimates (gate-bound, not date-bound)")
    .replace("### External Dependencies", "### External library lockset")
)
```

The cross-file import is non-idiomatic but legal; alternatively, lift `_minimal_valid_roadmap` to `tests/roadmap/conftest.py` as a fixture (the conftest already exists per the `ls` output at `tests/roadmap/conftest.py`).

---

## Summary

- **Test file is hermetic** — 21 tests, 6 classes, ~0.14s runtime, all green on master. C12 + C13 slot in as a new `TestC12H2ParentheticalStrip` class after `TestNonH3Cosmetics` and new tests inside `TestIdempotency` (or fresh `TestC13GapDrivenH3Repair`).
- **Helper gap** — `_content_with_milestone` does not cover H2-parenthetical drift or `## Resource Requirements and Dependencies` parents. Two minimal helpers proposed (§2). Alternatively, inline-build per the C11 pattern (`:294-316`).
- **CRITICAL absence** — NO existing test invokes `_template_sections_present` on `apply_cosmetic_remediations` output. This is the exact integration gap the validation REPORT reproducer exploits. The new fix MUST add at least one integration test that closes this loop, mirroring the reproducer's `(cl.is_pure_cosmetic, _template_sections_present(r))` assertion pair.
- **Idempotency contract** — one existing test (`:280-292`) covers C1+C2 only. C12 + C13 each need their own idempotency test (re-classify + re-apply → no change), because both transforms have realistic non-idempotent failure modes.
- **UV invocation verbatim** — `uv run pytest tests/roadmap/test_cosmetic_remediator.py -v` (no bare `pytest`, no `python -m`).
- **Reproducer seed** — `REPORT.md:36-47` Bash block; the new integration test should reproduce that 4-tuple `(is_pure_cosmetic, n_cosmetic, n_semantic, gate_after)` shape on a hermetic minimal artifact, and assert `gate_after is True` (which today is False).

**Status:** Complete.

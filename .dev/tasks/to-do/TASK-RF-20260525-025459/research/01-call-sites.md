# Research 01 — Call-Site Map for `_is_in_fenced_block`

**Status:** Complete
**Scope:** `/config/workspace/IronClaude/src/superclaude/cli/roadmap/cosmetic_remediator.py`
**Goal:** Inventory every call site so M1 fix (precompute fenced-block index set) can replace per-line O(N) scans with O(1) set lookup.

---

## 1. Definition of `_is_in_fenced_block`

**File:** `src/superclaude/cli/roadmap/cosmetic_remediator.py`
**Line range:** L204–L210 (definition + docstring + body)

Verbatim:

```python
def _is_in_fenced_block(lines: list[str], idx: int) -> bool:
    """Return True if line ``idx`` is inside a ``` ... ``` fenced code block."""
    fence_count = 0
    for i in range(idx):
        if lines[i].lstrip().startswith("```"):
            fence_count += 1
    return fence_count % 2 == 1
```

(`src/superclaude/cli/roadmap/cosmetic_remediator.py:204-210`)

**Cost analysis (M1 motivation):** Each call walks `[0, idx)` and re-scans every prior line for a fence prefix. Called inside per-line loops in 7 sites → O(N²) per detector/transform pass. Multiplied across the 6 functions that own these loops, this is the hot path PR #79 review flagged.

**Original-helper boundary semantics (re-verify before implementing M1):**

- Opener line (e.g. line 10 with ` ``` `): loop is `range(10)` → count = 0 → returns **False** (opener NOT inside)
- Line right after opener (line 11): count over `range(11)` = 1 → returns **True**
- Closer line (e.g. line 20 with closing ` ``` `): count over `range(20)` = 1 (only the opener so far) → returns **True** (closer IS treated as inside)
- Line after closer (line 21): count over `range(21)` = 2 → returns **False**

Any replacement must preserve this exact behavior — see §5 for the corrected `_compute_fenced_indices` skeleton.

---

## 2. Call Sites (7 total — all confirmed)

All 7 grep-confirmed line numbers verified by direct Read. No additional call sites in this file.

### Call site #1 — L253 (detector: `_detect_cosmetic_violations`)

- **Call (L253):** `in_fenced = _is_in_fenced_block(lines, idx)`
- **Enclosing function:** `_detect_cosmetic_violations(content: str) -> list[CosmeticViolation]` defined at **L241**
- **Parameter list:** `(content: str)` — does **not** receive `lines` as a parameter
- **`lines` source (L249):** `lines = content.splitlines()`  (note: **no `keepends=True`** here, unlike the transform helpers)
- **Context (L251-253):**
  ```python
  for idx, line in enumerate(lines):
      line_no = idx + 1
      in_fenced = _is_in_fenced_block(lines, idx)
  ```
- **Variable checked:** `idx` (loop index from L251)
- **Threading needed:** No — `lines` already in scope. Insert `fenced_indices = _compute_fenced_indices(lines)` immediately after L249, then rewrite L253 to `in_fenced = idx in fenced_indices`.

### Call site #2 — L446 (detector C11 inside `_detect_cosmetic_violations`)

- **Call (L446):** `if _is_in_fenced_block(lines, idx):`
- **Enclosing function:** Same as #1 — `_detect_cosmetic_violations` (L241). Lives inside the **C11 resource-subsection scan loop** at L433: `for idx, line in enumerate(lines):`
- **Parameter list:** `(content: str)`
- **`lines` source:** Same `lines` from L249 (still in scope; C11 scan reuses it)
- **Context (L444-447):**
  ```python
  if not line.startswith("### "):
      continue
  if _is_in_fenced_block(lines, idx):
      continue
  ```
- **Variable checked:** `idx` (re-bound by C11 loop at L433)
- **Threading needed:** No — same `fenced_indices` computed once for #1 covers this call (just rewrite call site to `idx in fenced_indices`).

### Call site #3 — L538 (transform: `_apply_milestone_h3_rewrites`)

- **Call (L538):** `if _is_in_fenced_block(lines, idx):`
- **Enclosing function:** `_apply_milestone_h3_rewrites(content: str) -> tuple[str, list[str]]` defined at **L515**
- **Parameter list:** `(content: str)`
- **`lines` source (L523):** `lines = content.splitlines(keepends=True)` (note: `keepends=True` — differs from detector at L249)
- **Context (L536-539):**
  ```python
  if current_mid is None:
      continue
  if _is_in_fenced_block(lines, idx):
      continue
  ```
- **Variable checked:** `idx` (loop index from L527: `for idx, line in enumerate(lines):`)
- **Threading needed:** No — compute `fenced_indices = _compute_fenced_indices(lines)` after L523.

### Call site #4 — L583 (transform: `_apply_trailing_whitespace_fix`)

- **Call (L583):** `if _is_in_fenced_block(lines, idx):`
- **Enclosing function:** `_apply_trailing_whitespace_fix(content: str) -> tuple[str, list[str]]` defined at **L577**
- **Parameter list:** `(content: str)`
- **`lines` source (L580):** `lines = content.splitlines(keepends=True)`
- **Context (L582-584):**
  ```python
  for idx, line in enumerate(lines):
      if _is_in_fenced_block(lines, idx):
          continue
  ```
- **Variable checked:** `idx` (loop from L582)
- **Threading needed:** No — compute `fenced_indices` after L580.

### Call site #5 — L616 (transform: `_apply_smart_quote_fold`)

- **Call (L616):** `if _is_in_fenced_block(lines, idx):`
- **Enclosing function:** `_apply_smart_quote_fold(content: str) -> tuple[str, list[str]]` defined at **L610**
- **Parameter list:** `(content: str)`
- **`lines` source (L613):** `lines = content.splitlines(keepends=True)`
- **Context (L615-617):**
  ```python
  for idx, line in enumerate(lines):
      if _is_in_fenced_block(lines, idx):
          continue
  ```
- **Variable checked:** `idx` (loop from L615)
- **Threading needed:** No — compute `fenced_indices` after L613.

### Call site #6 — L640 (transform: `_apply_table_padding_fix`)

- **Call (L640):** `if _is_in_fenced_block(lines, idx):`
- **Enclosing function:** `_apply_table_padding_fix(content: str) -> tuple[str, list[str]]` defined at **L627**
- **Parameter list:** `(content: str)`
- **`lines` source (L635):** `lines = content.splitlines(keepends=True)`
- **Context (L637-641):**
  ```python
  for idx, line in enumerate(lines):
      if not line.startswith("|"):
          continue
      if _is_in_fenced_block(lines, idx):
          continue
  ```
- **Variable checked:** `idx` (loop from L637)
- **Threading needed:** No — compute `fenced_indices` after L635.

### Call site #7 — L712 (transform: `_apply_resource_subsection_rewrites`)

- **Call (L712):** `if _is_in_fenced_block(lines, idx):`
- **Enclosing function:** `_apply_resource_subsection_rewrites(content: str) -> tuple[str, list[str]]` defined at **L688**
- **Parameter list:** `(content: str)`
- **`lines` source (L698):** `lines = content.splitlines(keepends=True)`
- **Context (L710-713):**
  ```python
  if not in_resource or not line.startswith("### "):
      continue
  if _is_in_fenced_block(lines, idx):
      continue
  ```
- **Variable checked:** `idx` (loop from L701: `for idx, line in enumerate(lines):`)
- **Threading needed:** No — compute `fenced_indices` after L698.

---

## 3. Orchestrator(s) — where `lines = ...splitlines(...)` is constructed

There is **no single orchestrator** that owns the `lines` list. Each of the 6 enclosing functions **independently** constructs `lines` from `content`:

| Function | def line | `lines = ...` line | splitlines variant |
|---|---|---|---|
| `_detect_cosmetic_violations` | L241 | L249 | `splitlines()` (no keepends) |
| `_apply_milestone_h3_rewrites` | L515 | L523 | `splitlines(keepends=True)` |
| `_apply_trailing_whitespace_fix` | L577 | L580 | `splitlines(keepends=True)` |
| `_apply_smart_quote_fold` | L610 | L613 | `splitlines(keepends=True)` |
| `_apply_table_padding_fix` | L627 | L635 | `splitlines(keepends=True)` |
| `_apply_resource_subsection_rewrites` | L688 | L698 | `splitlines(keepends=True)` |

**Implication for M1:** The fix does **not** require threading a `fenced_indices` parameter across the public API. Each of the 6 functions can compute `fenced_indices = _compute_fenced_indices(lines)` locally **immediately after its own `lines = …splitlines(…)` line**. This preserves the existing function signatures (`(content: str) -> …`) and keeps the change minimally invasive.

**Public-API callers** (`apply_cosmetic_remediations` at L732, `classify_gate_failure` at L471) pass `content: str` only — no `lines` flows across the public surface. **No public-API change is needed.**

**Note on `splitlines()` vs `splitlines(keepends=True)`:** The fenced-block decision is based only on `line.lstrip().startswith("```")`, which is unaffected by trailing newlines. So `_compute_fenced_indices` returns the same set regardless of which `splitlines` variant produced `lines` — safe to reuse the same helper everywhere.

---

## 4. External Callers

**None.** Repository-wide grep across `/config/workspace/IronClaude/src/` and `/config/workspace/IronClaude/tests/`:

```
src/superclaude/cli/roadmap/cosmetic_remediator.py:204  (def)
src/superclaude/cli/roadmap/cosmetic_remediator.py:253  (call #1)
src/superclaude/cli/roadmap/cosmetic_remediator.py:446  (call #2)
src/superclaude/cli/roadmap/cosmetic_remediator.py:538  (call #3)
src/superclaude/cli/roadmap/cosmetic_remediator.py:583  (call #4)
src/superclaude/cli/roadmap/cosmetic_remediator.py:616  (call #5)
src/superclaude/cli/roadmap/cosmetic_remediator.py:640  (call #6)
src/superclaude/cli/roadmap/cosmetic_remediator.py:712  (call #7)
```

The symbol is module-private (`_` prefix) and not exported in `__all__` at L791-796 (only `Classification`, `CosmeticViolation`, `apply_cosmetic_remediations`, `classify_gate_failure` are public). The original helper can therefore be safely deleted OR retained as a thin shim — see §5 recommendation.

---

## 5. Recommended Placement of `_compute_fenced_indices`

### Placement

Insert `_compute_fenced_indices(lines: list[str]) -> set[int]` **immediately after `_is_in_fenced_block` at L210**, inside the existing `# --- Helpers ---` section (header at L152). The two helpers belong together: one provides O(1) lookup against a precomputed set; the other (optionally) remains as a single-call diagnostic.

The Helpers section currently contains `_strip_section_numbering` (L155), `_h3_stem_and_suffix` (L164), `_current_milestone_id` (L188), `_is_in_fenced_block` (L204). Adding `_compute_fenced_indices` right after `_is_in_fenced_block` follows the file's existing convention of grouping related helpers and keeps the diff localized.

### Disposition of the old helper

**Recommended: keep as a thin shim**, to preserve backward-compat for any future ad-hoc diagnostic call and to minimize churn:

```python
def _is_in_fenced_block(lines: list[str], idx: int) -> bool:
    """Return True if line ``idx`` is inside a ``` ... ``` fenced code block.

    For per-line scans, prefer ``_compute_fenced_indices(lines)`` once and
    test ``idx in fenced_indices`` to avoid O(N^2) cost.
    """
    return idx in _compute_fenced_indices(lines)
```

**Alternative:** Delete `_is_in_fenced_block` entirely (no external callers per §4). Cleaner module, slightly more aggressive diff. Pick this if the team prefers tight modules — but the shim above costs essentially nothing and preserves option value.

### Required corrected `_compute_fenced_indices` (preserves original semantics exactly)

```python
def _compute_fenced_indices(lines: list[str]) -> set[int]:
    """O(N) precompute matching ``_is_in_fenced_block`` semantics exactly.

    For each index i, returns whether line i is inside a ``` ... ``` fenced
    code block, where "inside" means an *odd* number of fence-marker lines
    appear strictly before i. The opener-marker line itself is NOT inside;
    the closer-marker line IS inside (matches the original ``range(idx)``
    walk).
    """
    fenced: set[int] = set()
    fence_count = 0
    for i, line in enumerate(lines):
        # Test BEFORE incrementing — mirrors original ``for i in range(idx)``
        if fence_count % 2 == 1:
            fenced.add(i)
        if line.lstrip().startswith("```"):
            fence_count += 1
    return fenced
```

Equivalence claim (must be asserted by a test): for every `lines: list[str]` and every `i in range(len(lines))`:

```python
(i in _compute_fenced_indices(lines)) == _is_in_fenced_block(lines, i)
```

### Per-call-site edit pattern (minimum diff)

After each `lines = content.splitlines(...)` line listed in §3, insert one line:

```python
    fenced_indices = _compute_fenced_indices(lines)
```

Then within each loop body, rewrite `_is_in_fenced_block(lines, idx)` → `idx in fenced_indices`.

**Total mechanical changes:** 6 single-line inserts (one per function) + 7 in-place call-site rewrites + 1 new helper definition (or 1 new helper + 1 shim rewrite of the old helper).

---

## Summary (3 lines)

`_is_in_fenced_block` is defined at L204-210 and called at exactly 7 sites (L253, L446, L538, L583, L616, L640, L712), all inside 6 module-private functions that each construct their own `lines` list via `splitlines` — no parameter threading is required because `lines` is always already in local scope at each call. There are zero external callers (grep across src/ and tests/ confirms; symbol is `_`-prefixed and absent from `__all__`), so the helper can be replaced safely with a `_compute_fenced_indices(lines) -> set[int]` precompute placed right after L210 in the existing Helpers section, with each call site rewritten to `idx in fenced_indices` after a single-line `fenced_indices = _compute_fenced_indices(lines)` insert per function. CRITICAL: the new helper must preserve the original's "closer-line counts as inside, opener-line counts as outside" edge-case semantics (see §5 corrected skeleton with `fence_count`-style test-before-increment); naive toggle-based implementations will silently change behavior at fence-marker lines.

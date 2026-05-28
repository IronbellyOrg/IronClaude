# Research: Patterns & Conventions

**Topic:** Patterns & Conventions
**Status:** Complete
**Date:** 2026-05-27
**Scope:** `/config/workspace/IronClaude/src/superclaude/cli/roadmap/cosmetic_remediator.py`
**Goal:** Extract every convention C12 (H2 parenthetical strip) and C13 (gap-driven H3 repair) must follow.

---

## 1. Detector / Transformer Split

Every C-class has a **detector** (emits `CosmeticViolation` inside `_detect_cosmetic_violations`) **and** a separate `_apply_*` transformer. Detection is read-only and produces audit-traceable violation records; rewriting happens only in the transformer pass, gated on the detector's `klasses` set.

**Detector emission** — C11 resource-subsection detector (`cosmetic_remediator.py:483-496`):

```python
for alias_lower, _canonical in _RESOURCE_SUBSECTION_ALIASES:
    if alias_lower in h3_body:
        violations.append(
            CosmeticViolation(
                klass="C11",
                description=(
                    f"resource-requirements H3 alias at line {idx + 1}: "
                    f"{line.rstrip()!r}"
                ),
                line_number=idx + 1,
                original=line,
            )
        )
        break
```

**Matching transformer** — `_apply_resource_subsection_rewrites` (`cosmetic_remediator.py:722-764`):

```python
def _apply_resource_subsection_rewrites(content: str) -> tuple[str, list[str]]:
    ...
    transforms: list[str] = []
    lines = content.splitlines(keepends=True)
    fenced_indices = _compute_fenced_indices(lines)
    h2_re = re.compile(r"^##\s+(.+?)\s*$")
    in_resource = False
    for idx, line in enumerate(lines):
        ...
```

**Why this matters for C12/C13:** Both new classes need a detector branch inside `_detect_cosmetic_violations` (returning `CosmeticViolation(klass="C12"...)` / `"C13"`) **and** a separate `_apply_h2_parenthetical_strip` / `_apply_gap_driven_h3_repair` transformer. No shortcut combining the two.

---

## 2. Dispatcher Pattern

`apply_cosmetic_remediations` (`cosmetic_remediator.py:767-823`) dispatches transformers by set-intersection on the collected `klasses`. Each branch is `if "<class>" in klasses:` (single-class) or `if klasses & {"Cx", "Cy"}:` (multi-class share one transformer).

**Branch 1** — C1-C4 share `_apply_milestone_h3_rewrites` (`cosmetic_remediator.py:795-797`):

```python
if klasses & {"C1", "C2", "C3", "C4"}:
    current, t = _apply_milestone_h3_rewrites(current)
    transforms.extend(t)
```

**Branch 2** — C11 single-class branch (`cosmetic_remediator.py:799-801`):

```python
if "C11" in klasses:
    current, t = _apply_resource_subsection_rewrites(current)
    transforms.extend(t)
```

**Why this matters for C12/C13:** Add `if "C12" in klasses:` and `if "C13" in klasses:` branches in the prescribed order slot (see §10). C12 and C13 each get their own branch — they are independent transforms and must not share state.

---

## 3. Idempotency Contract

The module docstring states the contract; every transformer docstring re-affirms it.

**Module-level statement** (`cosmetic_remediator.py:11-13`):

```python
The classifier and transformer are pure Python (stdlib only). No LLM is
invoked. All transforms are idempotent: re-running on already-canonical
content is a no-op by construction.
```

**Transformer-level confirmation** — `_apply_resource_subsection_rewrites` (`cosmetic_remediator.py:728-730`):

```python
``### External Dependencies (PRD-confirmed,
TDD-pinned)`` -> ``### External Dependencies``; ``### Infrastructure``
-> ``### Infrastructure Requirements``). Idempotent.
```

Also see the dispatcher's closing sentence (`cosmetic_remediator.py:786`): `All transforms are idempotent. The function is safe to call twice.`

**Why this matters for C12/C13:** C12's parenthetical strip must skip H2s that already lack a parenthetical. C13's gap-driven H3 repair must skip when the canonical H3 already exists under the parent H2. Both transformers' docstrings MUST end with `Idempotent.`

---

## 4. Fenced-Block Guard

Every line-walking detector and transformer skips lines that fall inside triple-backtick fenced blocks. The helper is `_compute_fenced_indices(lines: list[str]) -> set[int]` (`cosmetic_remediator.py:204-226`), computed once per pass.

**Representative skip** — `_apply_milestone_h3_rewrites` (`cosmetic_remediator.py:569-570`):

```python
if idx in fenced_indices:
    continue
```

**Helper that computes the set** (`cosmetic_remediator.py:204-226`):

```python
def _compute_fenced_indices(lines: list[str]) -> set[int]:
    ...
    result: set[int] = set()
    fence_count = 0
    for i, line in enumerate(lines):
        if fence_count % 2 == 1:
            result.add(i)
        if line.lstrip().startswith("```"):
            fence_count += 1
    return result
```

**Convention:** Every `_apply_*` and every detector branch operating on `lines` calls `fenced_indices = _compute_fenced_indices(lines)` once at function entry and tests `if idx in fenced_indices: continue` before any heading or content match.

**Why this matters for C12/C13:** Both transformers MUST compute `fenced_indices` at entry and skip fenced lines. An H2 inside a fenced block (e.g. a docs example) must not be stripped, and a gap inside a fenced block must not synthesize a new H3.

---

## 5. Section-Numbering Strip

`_strip_section_numbering(text: str) -> str` (`cosmetic_remediator.py:155-161`) is applied to candidate heading bodies before any comparison, so `### 3.2.1 Risk Assessment` and `### Risk Assessment` compare equal.

```python
def _strip_section_numbering(text: str) -> str:
    """Remove a leading ``N.``, ``N.M.``, ``N.M.K.`` numbering prefix.

    Mirrors ``gates._normalize_heading``'s prefix logic but does not lowercase
    -- the remediator needs to preserve case for transform output.
    """
    return re.sub(r"^\s*\d+(?:\.\d+)*\.?\s+", "", text)
```

**Representative usage** — C11 detector body extraction (`cosmetic_remediator.py:466`, `478`):

```python
h2_text = _strip_section_numbering(h2m.group(1)).lower().strip()
...
h3_body = _strip_section_numbering(line[4:]).strip().lower()
```

**Why this matters for C12/C13:** C12 parses an H2 body to detect a parenthetical — must call `_strip_section_numbering` on the body first so `## 4. Resource Requirements and Dependencies (Engineering Owned)` is recognized. C13 detects/synthesizes H3s under a known parent H2 — must strip numbering on both the parent H2 detection and child H3 comparison.

---

## 6. Substring vs Exact Match for Aliases

`_RESOURCE_SUBSECTION_ALIASES` (`cosmetic_remediator.py:81-88`) is a tuple of `(lowercased_substring, canonical_name)` pairs, ordered **most-specific first** so `infrastructure requirements` matches before the shorter `infrastructure` would consume it.

```python
_RESOURCE_SUBSECTION_ALIASES: tuple[tuple[str, str], ...] = (
    ("external dependencies", "External Dependencies"),
    ("external deps", "External Dependencies"),
    ("infrastructure requirements", "Infrastructure Requirements"),
    ("infrastructure", "Infrastructure Requirements"),
    ("infra requirements", "Infrastructure Requirements"),
    ("infra", "Infrastructure Requirements"),
)
```

**Matcher code** (`cosmetic_remediator.py:483-484`, `754-755`):

```python
for alias_lower, _canonical in _RESOURCE_SUBSECTION_ALIASES:
    if alias_lower in h3_body:
```

```python
for alias_lower, canonical in _RESOURCE_SUBSECTION_ALIASES:
    if alias_lower in h3_lower:
```

**CRITICAL — design driver for C13:** Substring containment cannot match an H3 whose body has **zero token overlap** with any alias substring. The validation report's case of **`### External library lockset`** under `## Resource Requirements and Dependencies` fails C11 because:

- `"external dependencies" in "external library lockset"` → False
- `"external deps" in "external library lockset"` → False
- No other alias substring is contained in `"external library lockset"`

Expanding `_RESOURCE_SUBSECTION_ALIASES` is the wrong fix (the tuple grows unbounded with every new LLM hallucination). C13's gap-driven repair sidesteps the alias-matcher entirely: it detects that a *required* canonical H3 (e.g. `### External Dependencies`) is **missing** under the parent H2 and synthesizes a placeholder under the parent, independent of whatever drift-named H3s already exist.

**Why this matters for C13:** The detector must consult `gates._REQUIRED_RESOURCE_SUBSECTIONS` (`gates.py:914-916`) to know what set of canonical H3 names is required, then diff that set against the H3s actually present under the parent H2 (after `_strip_section_numbering`), and emit one C13 violation per missing canonical H3. The transformer inserts a placeholder H3 in canonical order.

---

## 7. CosmeticViolation Field Shape

The dataclass (`cosmetic_remediator.py:131-139`) is the only allowed shape for detector emissions.

```python
@dataclass
class CosmeticViolation:
    """One detected cosmetic defect with its remediation evidence."""

    klass: str  # "C1".."C10"
    description: str  # human-readable, suitable for audit log
    line_number: int | None = None  # 1-based, if locatable
    original: str | None = None  # the offending text, for diff diagnostics
```

**Why this matters for C12/C13:** New emissions MUST use this exact shape. `klass="C12"` / `klass="C13"`, `description` is human-readable and suitable for audit-log surfacing (mention line number + offending heading text), `line_number` is 1-based, `original` is the raw offending line (or `None` for a synthesized-insert violation that has no source line). **Also update the docstring comment `# "C1".."C10"` to `# "C1".."C13"` on `klass`.**

---

## 8. Audit-Log Line Format

The convention is `transforms.append("<short human-readable string with line number and before -> after>")`. Each transformer accumulates a list and returns it; the dispatcher concatenates.

**Representative audit line 1** — C1-C4 transformer (`cosmetic_remediator.py:600-602`):

```python
transforms.append(
    f"H3 normalized at line {idx + 1}: {line.rstrip()!r} -> {new_heading!r}"
)
```

**Representative audit line 2** — C11 transformer (`cosmetic_remediator.py:758-761`):

```python
transforms.append(
    f"resource H3 normalized at line {idx + 1}: "
    f"{line.rstrip()!r} -> '### {canonical}'"
)
```

**Why this matters for C12/C13:** New transforms must produce a comparable line. Suggested shapes:

- C12: `f"H2 parenthetical stripped at line {idx + 1}: {line.rstrip()!r} -> {new_heading!r}"`
- C13: `f"missing resource H3 synthesized after line {idx + 1}: '### {canonical_h3}' (under {parent_h2!r})"`

Use repr (`!r`) on raw heading text so whitespace/dash variants are visible in the audit log.

---

## 9. `__all__` Export Contract

The public surface is exactly four entries (`cosmetic_remediator.py:826-831`):

```python
__all__ = [
    "Classification",
    "CosmeticViolation",
    "apply_cosmetic_remediations",
    "classify_gate_failure",
]
```

**Why this matters for C12/C13:** New helpers (`_apply_h2_parenthetical_strip`, `_apply_gap_driven_h3_repair`, any private regex constants) stay underscore-prefixed and are **NOT** added to `__all__`. The dispatcher (`apply_cosmetic_remediations`) is the only public entrypoint that calls them; the C12/C13 surface flows entirely through the existing public dispatch.

---

## 10. Stable Transform Ordering

The dispatcher docstring (`cosmetic_remediator.py:777-786`) prescribes the 7-step order:

```python
Transforms are applied in a stable order so the output is deterministic:
    1. Milestone H3 rewrites (C1-C4)
    2. Resource-section H3 rewrites (C11)
    3. Trailing whitespace (C5, C6)
    4. Blank-line collapse (C7)
    5. Smart-quote fold (C8)
    6. Table padding (C9)
    7. Frontmatter trim (C10)

All transforms are idempotent. The function is safe to call twice.
```

**Why this matters for C12/C13:** Both classes operate on **heading shape**, which must run before whitespace/blank/quote/table/frontmatter passes (since those passes assume headings are already canonical). Recommended slots:

- **C12 (H2 parenthetical strip)** — slot **2.5** (between current step 2 and step 3). Rationale: C12 modifies H2 lines whose text is consulted by C13's gap detection (C13 needs the *canonical* `## Resource Requirements and Dependencies` spelling to identify the parent), so C12 must run BEFORE C13.
- **C13 (gap-driven H3 repair under known parent H2)** — slot **2.75** (after C12, before step 3). Rationale: C13 inserts new H3 lines, which then become subject to trailing-whitespace fix (step 3) and so on. C13 must run after C11 so existing alias-matched H3s have already been promoted to canonical and C13's gap-diff sees the post-promotion state.

**Update the docstring** to reflect the new 9-step order. The numeric list inside `apply_cosmetic_remediations` is normative — drift between docstring and dispatch order is a contract bug.

---

## Gotcha (out of scope, flag-only)

`_NONCANONICAL_DASH_PATTERN` (`cosmetic_remediator.py:95`) flags em-dash (`—`) as a non-canonical separator:

```python
_NONCANONICAL_DASH_PATTERN = re.compile(r"(?:u2014|—|–|−|\xa0\-\xa0|\xa0|~)")
```

…but the gate at `gates.py:993-998` explicitly **accepts** em-dash:

```python
# Accept em-dash or regular hyphen between stem and M{N}.
candidates = {
    f"{stem} — m{n}",
    f"{stem} - m{n}",
    f"{stem} -- m{n}",
}
```

This means an already-gate-passing em-dash heading like `### Risk Assessment and Mitigation — M3` would be flagged C3 by the cosmetic-remediator and rewritten to `-- M3`. This is an existing pre-C12/C13 inconsistency. **Not in scope for the C12/C13 fix** — flagging only so the implementer doesn't accidentally inherit the same bug pattern when designing C13's canonical-H3 placeholder shape. (Use `—`/`-`/`--` consistently with `gates.py` when synthesizing C13 placeholders to avoid creating new instances of this drift.)

---

## Status: Complete

**Summary:**

- 10 conventions extracted with quoted code + `file:line` per section
- Each section explains why-it-matters specifically for C12 (H2 parenthetical strip) and C13 (gap-driven H3 repair)
- Critical design driver for C13 documented in §6: substring-alias matching cannot catch zero-overlap drift like `External library lockset`, which is why gap-driven repair (not alias expansion) is the correct mechanism
- Recommended order slots: C12 at 2.5, C13 at 2.75 (both before whitespace pass; C13 after C12 so C13 sees canonical parent-H2 text)
- One out-of-scope gotcha flagged: `_NONCANONICAL_DASH_PATTERN` includes em-dash even though `gates.py:993-998` accepts it

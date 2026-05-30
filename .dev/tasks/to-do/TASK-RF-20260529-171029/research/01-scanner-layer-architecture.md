# Research: Scanner Layer Architecture
**Topic type:** File Inventory + Patterns & Conventions
**Scope:** obligation_scanner.py (BareReview worktree, post-Fix-1+Fix-3)
**Status:** Complete
**Date:** 2026-05-29

**Target file:** `/config/workspace/IronClaude/.claude/worktrees/BareReview/src/superclaude/cli/roadmap/obligation_scanner.py` (710 lines, verified)
**Sibling file referenced:** `/config/workspace/IronClaude/.claude/worktrees/BareReview/src/superclaude/cli/roadmap/gates.py`

---

## 1. Module-level structure

### Imports (lines 13-28)
- `re` (stdlib), `dataclasses.dataclass`
- `from superclaude.cli.vocabulary import DISCHARGE_TERMS, SCAFFOLD_TERMS` (line 18) — the canonical scaffold/discharge vocabulary
- `from superclaude.cli.roadmap.gates import _REQUIRED_H2_SECTIONS as _TAIL_SECTION_HEADINGS` (lines 23-25) — aliased import
- `from superclaude.cli.roadmap.gates import _normalize_heading` (lines 26-28) — heading canonicalization helper

**Critical pattern for Layer 5:** The module already imports `_normalize_heading` and one tuple from `gates`. **Layer 5 should reuse `_normalize_heading` the same way** (see Section 6).

### Module-level constants / regexes (lines 30-141)
- `_SCAFFOLD_RE` (line 31) — compiled from `SCAFFOLD_TERMS`, case-insensitive
- `_DISCHARGE_RE` (line 32) — compiled from `DISCHARGE_TERMS`, case-insensitive
- `_EXEMPT_COMMENT_RE` (line 35) — FR-MOD1.7 `# obligation-exempt`
- `_CODE_BLOCK_RE` (line 38) — FR-MOD1.8 fenced block detector
- `_INLINE_CODE_SCAFFOLD_RE` (lines 43-46) — Layer 1a: scaffold inside backticks
- `_COMPLETED_CHECKLIST_RE` (line 49) — Layer 1b: `- [x]` completed item
- `_NEGATION_PREFIX_RE` (lines 52-65) — Layer 2: negation/meta-context
- `_SHELL_CMD_RE` (lines 68-71) — Layer 2: shell command lines
- `_RISK_WARNING_RE` (lines 74-77) — Layer 2: `Risk:` / `Warning:` line prefix
- `_GATE_CRITERIA_RE` (lines 80-83) — Layer 2: "no/zero X present/found"
- `_TABLE_CELL_IMPERATIVE_RE` (lines 89-92) — Layer 3a: `| ... | scaffold X` cells
- `_TABLE_SEPARATOR_RE` (line 101) — table separator row detector
- `_DESCRIPTOR_NOUNS` (lines 110-126) — **Layer 4** frozen-set (outcome, result, mitigation, fallback, historical, legacy, prior, existing, etc.)
- `_DESCRIPTOR_ADJACENCY_RE` (lines 127-130) — **Layer 4** compiled adjacency regex
- `_PAREN_PHASE_LABEL_RE` (lines 136-141) — Layer 3b: parenthetical phase label
- `_FIELD_LABELS` (lines 455-484) and `_FIELD_LABEL_LINE_RE` (lines 489-491) — used by component extraction, not severity

**No existing constant named `_SUBSECTION_NAMES`, `_DEMOTED_SUBSECTIONS`, or similar.** The builder must add one for Layer 5.

### Dataclasses (lines 147-187)
- `Obligation` (lines 147-160) — `severity: str` field already supports `"HIGH" | "MEDIUM"` (line 156). **No schema change needed for Layer 5.**
- `ObligationReport` (lines 163-187) — `undischarged_count` property excludes `severity == "MEDIUM"` (line 182). Demotion automatically removes from the failing count.

---

## 2. Scanner state machine

The main scanner is `scan_obligations(content: str)` (lines 190-378). State is **NOT carried via class instance** — it's local to the loop.

State variables tracked while walking:
| State                             | Where tracked                                 | Line(s)                  |
|-----------------------------------|-----------------------------------------------|--------------------------|
| Current section / phase index `i` | enumerate over `sections`                      | 209                      |
| `phase_id`, `phase_content`, `start_line` | unpacked per section                  | 209                      |
| Each scaffold match within phase  | `_SCAFFOLD_RE.finditer(phase_content)`         | 210                      |
| Per-match `term`, `context_line`, `abs_line` | locals                              | 211-213                  |
| Per-match `stripped_context`       | local                                         | 220                      |
| Per-match `ctx_lower`              | local                                         | 238                      |
| Per-match `component`              | from `_extract_component_context`             | 310                      |
| Per-match `severity`               | mutable local; demoted by Layer 1a/1b/2 cascade | 318 (init), 324/328/331/337 (demote) |
| Code-block ranges (precomputed)    | `code_block_ranges`                           | 204                      |

**Critical finding for Layer 5:** There is **NO existing H3-tracking state** in `scan_obligations`. The scanner currently processes each phase content slice (M2, M3...) as a flat blob — it does not know which H3 subsection within a milestone any given line belongs to. Layer 5 must introduce this state — OR, more cleanly, leverage the fact that `_split_into_phases` already splits on H3 (see below) and key Layer 5 off the resulting per-section `phase_id`.

The phase splitter `_split_into_phases` (lines 404-445) splits on BOTH H2 and H3 (regex `r"^(#{2,3})\s+..."` line 412), so when milestone bodies contain H3s like `### Risk Assessment and Mitigation — M2`, those H3s become their OWN section in `sections`. **Layer 5 can therefore operate by inspecting `phase_id` per section, not by tracking H3 line-by-line.**

---

## 3. Layer-by-layer breakdown

### Layer 1a — Inline-code scaffold
- **File:line:** detection regex line 43-46; applied at lines 327-328
- **Detects:** Scaffold term inside backticks on the current line, e.g. `` `mock_server` ``
- **Mechanism:** Regex on `context_line`
- **Severity rule:** Demotes HIGH → MEDIUM
- **Hook into scan loop:** Inline `if severity == "HIGH" and _INLINE_CODE_SCAFFOLD_RE.search(context_line):` (line 327)

### Layer 1b — Completed checklist
- **File:line:** detection regex line 49; applied at lines 330-331
- **Detects:** Line starting with `- [x]`
- **Mechanism:** Regex on `context_line`
- **Severity rule:** Demotes HIGH → MEDIUM
- **Hook into scan loop:** `elif severity == "HIGH" and _COMPLETED_CHECKLIST_RE.match(context_line):` (line 330)

### Layer 2 — Negation / meta-context (umbrella)
- **File:line:** umbrella check at lines 333-337; helper `_is_meta_context` at lines 597-628
- **Detects:** Negation prefixes (`no`, `not`, `never`...), shell commands, risk/warning lines, gate-criteria phrasing, **PLUS Layer 3a and Layer 3b (these sub-layers all live inside `_is_meta_context`)**, **PLUS Layer 4 via `_is_descriptive_context`**
- **Mechanism:** Multiple regex checks inside `_is_meta_context(line, term_start_in_line)`
- **Severity rule:** Demotes HIGH → MEDIUM
- **Hook into scan loop:** lines 333-337 (else-if branch in cascade). Note `_is_meta_context` also called **earlier** at line 280 inside the `term.lower().startswith("scaffold")` descriptive-prose suppression block (T3.3 gate-reorder).

### Layer 3a — Scaffold imperative in table cell
- **File:line:** detection regex line 89-92; applied at lines 617-618 (inside `_is_meta_context`)
- **Detects:** Table data rows where "scaffold" is the first word after the pipe (e.g., `| 2.2.1 | Scaffold command file ...`)
- **Mechanism:** Regex on the line; only handles the verb "scaffold" (others like mock/stub stay HIGH per line 87-88 comment)
- **Severity rule:** Demotes via `_is_meta_context` returning True
- **Hook:** Branch inside `_is_meta_context` (line 617)

### Layer 3b — Parenthetical phase label
- **File:line:** detection regex line 136-141; applied at lines 621-622 (inside `_is_meta_context`)
- **Detects:** Multi-word parenthetical labels like `(command scaffolding)`, `(Phase 2 mocking)`, `(stubbed layer)`. Bare `(scaffold)` stays HIGH (line 135 comment).
- **Mechanism:** Regex on the line
- **Severity rule:** Demotes via `_is_meta_context` returning True
- **Hook:** Branch inside `_is_meta_context` (line 621)

### Layer 4 — Descriptor-noun adjacency (Fix 3) — **THIS IS THE MIRROR TARGET**
- **File:line:**
  - Constant `_DESCRIPTOR_NOUNS` frozenset: lines 110-126
  - Compiled regex `_DESCRIPTOR_ADJACENCY_RE`: lines 127-130
  - Helper function `_is_descriptive_context(line, term_start_in_line)`: lines 576-594
  - Discharge-intent guard helper `_is_discharge_intent_line(line)`: lines 669-684
  - Hook inside `_is_meta_context`: lines 624-626
- **Detects:** Scaffold term within ~40 chars (~4 words) of any descriptor noun (`outcome`, `mitigation`, `fallback`, `historical`, `legacy`, etc.) on the same line, **provided the line does NOT signal discharge intent**.
- **Mechanism:** Window slice `line[term_start-40 : term_start+40]` searched with `_DESCRIPTOR_ADJACENCY_RE`. Discharge-intent override via `_is_discharge_intent_line` (regex on the full line for replace/wire/integrate/connect/swap/remove/implement-real/fill-in/complete verbs and noun forms like `replacement`).
- **Severity rule:** Demotes HIGH → MEDIUM (indirectly, by `_is_meta_context` returning True at the cascade in line 336-337)
- **Hook into scan loop:** Last branch inside `_is_meta_context` (lines 624-626):
  ```python
  # Layer 4 (Fix 3): Descriptor-noun adjacency — descriptive prose
  if _is_descriptive_context(line, term_start_in_line):
      return True
  ```

**Test cross-references (per docstrings; full inventory is Researcher 2's track):**
- Layer 4 introduced by Fix 3 — see TASK-RF-20260529-163344 (Researcher 4's track).
- Docstring at line 582-585 calls out: "(no-op outcome)", "stub-tested mitigation", "legacy stub retained" as Layer 4 hits.
- Discharge-intent guard test target: "outcome: scaffold needs replacement" (must stay HIGH, line 583).

---

## 4. Layer 4 — verbatim wiring (THE MIRROR TARGET)

### 4a. Constants (lines 103-130)
```python
# Layer 4 (Fix 3): descriptor nouns adjacent to scaffold terms signal
# descriptive/historical/fallback prose, not prescriptive scaffolding.
# Used by `_is_descriptive_context` to demote scaffold-term findings sitting
# inside per-milestone Risk Assessment / Mitigation subsections, External
# Dependencies tables, etc. A line that ALSO matches discharge intent
# (`_is_discharge_intent_line`) is NOT demoted — that protects real
# obligations like "outcome: scaffold needs replacement".
_DESCRIPTOR_NOUNS = frozenset(
    {
        "outcome",
        "result",
        "behavior",
        "behaviour",
        "property",
        "mitigation",
        "fallback",
        "dependency",
        "consideration",
        "historical",
        "legacy",
        "prior",
        "existing",
    }
)
_DESCRIPTOR_ADJACENCY_RE = re.compile(
    r"\b(" + "|".join(_DESCRIPTOR_NOUNS) + r")\b",
    re.IGNORECASE,
)
```

### 4b. Detector function (lines 576-594)
```python
def _is_descriptive_context(line: str, term_start_in_line: int) -> bool:
    """True when a scaffold term sits within ~4 words of a descriptor noun AND
    the line does NOT signal discharge intent.

    Fix 3: catches descriptive-prose contexts like
    ``(no-op outcome)``, ``stub-tested mitigation``, ``legacy stub retained``
    that the parenthetical-phrase Layer 3b misses. The discharge-intent guard
    ensures lines like ``outcome: scaffold needs replacement`` (a real
    obligation) remain HIGH.

    Window heuristic: ~40 chars on each side of the term covers ~4 short
    English words, which matches the prose density of roadmap risk tables.
    """
    if _is_discharge_intent_line(line):
        return False
    window_start = max(0, term_start_in_line - 40)
    window_end = min(len(line), term_start_in_line + 40)
    window = line[window_start:window_end]
    return bool(_DESCRIPTOR_ADJACENCY_RE.search(window))
```

### 4c. Discharge-intent guard (lines 669-684)
```python
def _is_discharge_intent_line(line: str) -> bool:
    """Return True if line clearly states discharge intent, not new scaffolding.

    Recognizes both verb and noun forms of replace/integration so a phrase
    like "needs replacement" is treated as discharge intent (used as the
    guard for Layer 4's descriptor-noun classifier).
    """
    return bool(
        re.search(
            r"\b(?:replace(?:ment|s|d)?|wire\s+(?:up|in|into)|"
            r"integrat(?:e|ing|ed|ion)|connect|swap\s+(?:out|in)|remove|"
            r"implement\s+real|fill\s+in|complete)\b",
            line,
            re.IGNORECASE,
        )
    )
```

### 4d. Hook inside `_is_meta_context` (lines 624-626)
```python
    # Layer 4 (Fix 3): Descriptor-noun adjacency — descriptive prose
    if _is_descriptive_context(line, term_start_in_line):
        return True
```

This is **the very last branch** in `_is_meta_context` before `return False` (line 628).

### 4e. Demotion mechanism — the ONE line that changes severity
The demotion is **indirect** for Layers 3a/3b/4: they all return True from `_is_meta_context`, which is checked at lines 333-337 of `scan_obligations`:
```python
elif severity == "HIGH":
    line_start = phase_content.rfind("\n", 0, match.start()) + 1
    term_start_in_line = match.start() - line_start
    if _is_meta_context(context_line, term_start_in_line):
        severity = "MEDIUM"   # <-- THE SINGLE LINE THAT DEMOTES
```
**Layer 5, if added inside `_is_meta_context`, gets demotion FOR FREE.** No edit needed to `scan_obligations`'s cascade — BUT Layer 5 needs `phase_id`, which is loop-scope, not line-scope. See Section 8 for the design choice.

---

## 5. H3 / subsection handling — current state

**No existing H3 tracking inside `scan_obligations` or `_is_meta_context`.** Findings:

- `_split_into_phases` (lines 404-445) treats H3 as a section boundary (regex `r"^(#{2,3})\s+..."`, line 412) — so any H3 in the document starts a new "section" entry in the returned list. Phase IDs come from the H3 heading text directly (`m.group(2).strip()`, line 428).
- `scan_obligations` skips H3-looking lines via `stripped_context.startswith("### ")` (line 223) — this only avoids matching scaffold terms IN the heading text itself.
- The only H3 awareness elsewhere in the file is the comment at line 381 (`# --- FR-MOD1.2: Milestone-section parser with H2/H3 fallback ---`).

**Conclusion:** This module has no current concept of "the H3 subsection I'm inside while still under milestone M2." Layer 5 must add it — and the cleanest mechanism is leveraging the H3-splitting `_split_into_phases` already does.

**Important implication:** Because `_split_into_phases` already splits on H3, when a real roadmap has `## M2: ...` followed by `### Risk Assessment and Mitigation — M2`, the latter becomes its own section entry with `phase_id = "Risk Assessment and Mitigation — M2"`. Layer 5 inspects `phase_id` to detect the target subsection — no separate state machine needed.

---

## 6. Subsection-name constants

### In `obligation_scanner.py`
**No subsection-name constants currently exist** in this file matching the four target names (Risk Assessment, Integration Points, Milestone Dependencies, Open Questions).

The closest existing constant is `_TAIL_SECTION_HEADINGS` (imported at line 23-25 as alias of `gates._REQUIRED_H2_SECTIONS`) — but this is for **tail-section boundary detection** (Fix 1), not subsection demotion. It contains H2 names like "risk register" / "decision summary", NOT the H3 subsection names.

### In `gates.py` — partial match available
`gates.py` already defines (lines 907-911):
```python
_REQUIRED_MILESTONE_SUBSECTIONS: tuple[str, ...] = (
    "integration points",
    "milestone dependencies",
    "risk assessment and mitigation",
)
```

**Three of the four target subsections are here.** The fourth — "Open Questions" — is NOT in this tuple. The builder has two options:
1. **Reuse + extend in gates.py.** Add "open questions" to `_REQUIRED_MILESTONE_SUBSECTIONS` (changes its semantics — it's currently a hard-requirement tuple, not a "demote scaffold inside these" tuple). Risky.
2. **Add a new constant in `obligation_scanner.py`.** Define a local `_DEMOTED_H3_SUBSECTIONS: frozenset[str] = frozenset({"integration points", "milestone dependencies", "risk assessment and mitigation", "open questions"})` and use the already-imported `_normalize_heading` to compare.

**Recommendation:** Option 2. Keeps gates.py semantics intact and matches the file-locality pattern (Layer 4 keeps its `_DESCRIPTOR_NOUNS` local to this module).

---

## 7. Demotion mechanism — single-line example

The actual `severity = "MEDIUM"` assignment happens in only four places in `scan_obligations`:

| Layer | File:line | Code |
|-------|-----------|------|
| Code-block local fallback (FR-MOD1.8) | 324 | `severity = "MEDIUM"` (inside `if severity == "HIGH" and _is_inside_code_block(...)`) |
| Layer 1a inline-code | 328 | `severity = "MEDIUM"` |
| Layer 1b completed checklist | 331 | `severity = "MEDIUM"` |
| Layer 2/3a/3b/4 umbrella (via `_is_meta_context`) | 337 | `severity = "MEDIUM"` |

**The Layer 4 mirror pattern:** Layer 4 does NOT touch `scan_obligations` directly. It is wired entirely as a branch inside `_is_meta_context` (lines 624-626). The line 337 demotion fires "for free" when `_is_meta_context` returns True. **Layer 5 follows the same shape, but at the cascade level (see Section 8) because it needs `phase_id`, which is loop-scope.**

For completeness, the property that uses MEDIUM is `ObligationReport.undischarged_count` (line 182):
```python
if not o.discharged and not o.exempt and o.severity != "MEDIUM"
```
So a demoted obligation still appears in `obligations` (preserving traceability) but does not count toward `undischarged_count` / `has_undischarged` (line 187).

---

## 8. Insertion point for Layer 5

Based on the Layer 4 mirror:

### Code constants
**Insert location:** Right after Layer 4's constants, between line 130 and line 132 (before the blank line and `# Layer 3b:` comment). Pattern:
```python
# Layer 5: H3 subsection-context demotion — scaffold terms inside per-milestone
# Risk Assessment / Integration Points / Milestone Dependencies / Open Questions
# subsections are descriptive, not prescriptive. Mirrors Layer 4's "descriptive
# prose" philosophy at the section level rather than the line level.
_DEMOTED_H3_SUBSECTIONS = frozenset({
    "integration points",
    "milestone dependencies",
    "risk assessment and mitigation",
    "open questions",
})
```

### Helper function
**Insert location:** Right after `_is_descriptive_context` (line 594) and before `_is_meta_context` (line 597). Pattern:
```python
def _is_demoted_subsection(phase_id: str) -> bool:
    """True when the phase_id is a milestone H3 subsection where scaffold
    terms should be demoted to MEDIUM (Layer 5).

    Mirrors Layer 4 (descriptor-noun adjacency) in shape: a pure predicate
    that, when True, signals demotion to the cascade in scan_obligations.

    Handles headings like '### Risk Assessment and Mitigation — M2' by
    stripping the milestone suffix and normalizing.
    """
    # Strip optional "— M{N}" / "- M{N}" suffix before normalizing
    base = re.sub(r"\s*[—-]\s*M\d+\w*$", "", phase_id).strip()
    return _normalize_heading(base) in _DEMOTED_H3_SUBSECTIONS
```

### Hook into the cascade
**Critical design choice for builder:** Layer 5 needs `phase_id`, which `_is_meta_context` does not currently receive. Two options:
1. **Wire in `scan_obligations` directly** as a new cascade branch parallel to Layers 1a/1b/2. Insert at line 338 (after the existing Layer 2 block at lines 333-337):
   ```python
   # Layer 5: H3 subsection-context demotion
   if severity == "HIGH" and _is_demoted_subsection(phase_id):
       severity = "MEDIUM"
   ```
2. **Pass `phase_id` into `_is_meta_context`.** Higher refactor cost; breaks the helper's "per-line" contract.

**Recommendation:** Option 1. It preserves `_is_meta_context`'s per-line contract, keeps Layer 5 isolated, and the cascade-branch shape is already used by Layers 1a (line 327), 1b (line 330), and the Layer 2 umbrella (line 333). **The mirror is at the cascade level rather than inside the umbrella helper.**

This is a slight deviation from "mirror Layer 4 EXACTLY" but is the closest faithful mirror given that `phase_id` is loop-scope, not line-scope. The shape (`if severity == "HIGH" and <predicate>: severity = "MEDIUM"`) is identical to Layers 1a/1b.

### Discharge-intent guard?
Layer 4 has `_is_discharge_intent_line` as a guard so that "scaffold needs replacement" inside a Risk subsection stays HIGH. **The builder should consider whether Layer 5 needs the same guard.** A real obligation phrased inside a Risk Assessment section like "wire mock_auth to real provider in M3" should remain HIGH. Recommend adding the same guard:
```python
if severity == "HIGH" and _is_demoted_subsection(phase_id) and not _is_discharge_intent_line(context_line):
    severity = "MEDIUM"
```

This preserves Layer 4's escape valve and is consistent with the "descriptive prose ≠ real obligation" philosophy. **This decision is for the builder — flagged here as a design surface, not prescribed.**

---

## 9. Public API impact

| Surface | Impact |
|---------|--------|
| `scan_obligations(content: str) -> ObligationReport` signature | NONE |
| `Obligation` dataclass | NONE (severity field already supports MEDIUM) |
| `ObligationReport` dataclass | NONE (undischarged_count already excludes MEDIUM at line 182) |
| `ObligationReport.has_undischarged` | NONE (derives from undischarged_count) |
| Module-level constants exported | NEW: `_DEMOTED_H3_SUBSECTIONS` (private by underscore convention; not exported) |
| Module-level helpers exported | NEW: `_is_demoted_subsection` (private; not exported) |
| Imports from `gates` | NONE if Layer 5 keeps its frozenset local; `_normalize_heading` already imported. |

**Conclusion: Zero public API change.** Layer 5 is a pure internal demotion gate, identical to Layer 4's external visibility.

---

## Summary — for builder

- **(a) Where Layer 4 lives:** Constants at `obligation_scanner.py:103-130`; helper `_is_descriptive_context` at `obligation_scanner.py:576-594`; discharge-intent guard `_is_discharge_intent_line` at `obligation_scanner.py:669-684`; wired into the cascade as the final branch inside `_is_meta_context` at `obligation_scanner.py:624-626`.
- **(b) Exact demotion mechanism:** Layer 4 returns True from `_is_meta_context`, which causes `scan_obligations` line 337 to execute `severity = "MEDIUM"`. The cascade demotion is shared by Layers 2/3a/3b/4. The only direct demotion lines in the whole module are `obligation_scanner.py:324, 328, 331, 337` — all writing `severity = "MEDIUM"`.
- **(c) Insertion point for Layer 5:** Add `_DEMOTED_H3_SUBSECTIONS` frozenset near line 131 (after Layer 4 constants) and `_is_demoted_subsection(phase_id)` helper near line 595 (after `_is_descriptive_context`). Wire into the cascade in `scan_obligations` as a new branch immediately after the Layer 2 block at lines 333-337 (around line 338), shape `if severity == "HIGH" and _is_demoted_subsection(phase_id): severity = "MEDIUM"`. Consider also gating on `not _is_discharge_intent_line(context_line)` to preserve Layer 4's HIGH-obligation-inside-risk-section escape valve.

### Additional context the builder must reconcile
- `gates._REQUIRED_MILESTONE_SUBSECTIONS` (`gates.py:907-911`) already canonicalizes 3 of the 4 target subsection names; "open questions" is NOT there. **Recommend defining `_DEMOTED_H3_SUBSECTIONS` locally in `obligation_scanner.py` with all four names** rather than mutating gates.py.
- `_normalize_heading` is **already imported** (lines 26-28). Layer 5 should use it on the phase_id (after stripping any "— M{N}" suffix) before comparing against `_DEMOTED_H3_SUBSECTIONS`.
- `_split_into_phases` (`obligation_scanner.py:404-445`) splits on BOTH H2 and H3, so milestone subsections like `### Risk Assessment and Mitigation — M2` become standalone phase entries. **Layer 5's predicate operates on `phase_id`, not on tracked H3 state** — there's no state-machine plumbing to add.

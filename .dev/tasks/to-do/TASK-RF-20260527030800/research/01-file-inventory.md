# Research: File Inventory — cosmetic_remediator.py + gates.py
**Topic type:** File Inventory
**Scope:** cosmetic_remediator.py + gates.py
**Status:** Complete
**Date:** 2026-05-27
---

## File sizes
- `src/superclaude/cli/roadmap/cosmetic_remediator.py` — 831 lines
- `src/superclaude/cli/roadmap/gates.py` — 1441 lines

---

## A. `cosmetic_remediator.py` inventory

### A.1 Public surface (`__all__` @ line 826)
- `Classification` — `@dataclass` @ line 141 (fields: `is_pure_cosmetic`, `cosmetic_violations`, `semantic_violations`, `gate_name`, `step_id`)
- `CosmeticViolation` — `@dataclass` @ line 131 (fields: `klass`, `description`, `line_number`, `original`)
- `apply_cosmetic_remediations(content, classification) -> tuple[str, list[str]]` — public dispatcher @ line 767
- `classify_gate_failure(content, gate_name, failure_reason, *, step_id) -> Classification` — public classifier @ line 501

### A.2 Canonical sets / module-level constants
| Symbol | File:Line | Purpose |
|---|---|---|
| `_REQUIRED_STEMS_ORDER: tuple[str, ...]` | line 49 | Ordered milestone-H3 stems (Integration Points, Milestone Dependencies, Open Questions, Risk Assessment and Mitigation) |
| `_REQUIRED_STEMS_LOWER: frozenset[str]` | line 57 | Lowercase fast-membership view of above |
| `_STEM_ALIASES: dict[str, str]` | line 64 | C1 alias map (e.g., "risk assessment" -> "Risk Assessment and Mitigation") |
| `_RESOURCE_SUBSECTION_ALIASES: tuple[tuple[str, str], ...]` | line 81 | C11 alias tuples, most-specific first; substring-match on lowercased H3 body |
| `_RESOURCE_PARENT_NORMALIZED: str` | line 91 | `"resource requirements and dependencies"` — the C11 parent-H2 sentinel |
| `_NONCANONICAL_DASH_PATTERN` (compiled regex) | line 95 | `r"(?:u2014|—|–|−|\xa0\-\xa0|\xa0|~)"` — used by C3 |
| `_SMART_QUOTE_MAP` (str.maketrans) | line 98 | C8 fold table |
| `_SEMANTIC_MARKERS: tuple[str, ...]` | line 113 | Currently only `"{{SC_PLACEHOLDER:"` |
| `_ROADMAP_GATE_NAMES: frozenset[str]` | line 120 | Gates this remediator narrows to (`template_sections_present`, `deliverable_table_schema`, `open_questions_placement`, `milestone_summary_present`, `frontmatter_required_fields`) |

### A.3 Private helpers (underscore family)
| Function | File:Line | Signature/role |
|---|---|---|
| `_strip_section_numbering(text)` | line 155 | Strips leading `N.`/`N.M.` (case-preserving) — pairs with `gates._normalize_heading` numbering rule |
| `_h3_stem_and_suffix(heading_text)` | line 164 | Splits `"Foo Bar -- M3"` into `("Foo Bar", "-- M3")`; canonical separators (`--`, `—`, `-`) then non-canonical fallbacks |
| `_current_milestone_id(lines, idx)` | line 188 | Walks backward to find enclosing `## M{N}:` H2 (regex `^##\s+M(\d+)\s*:`, case-insensitive); H1 resets scope |
| `_compute_fenced_indices(lines)` | line 204 | O(N) set of line indices inside ``` fences. Opener excluded, closer included. THE canonical fence helper. |
| `_is_in_fenced_block(lines, idx)` | line 229 | Thin oracle wrapper around `_compute_fenced_indices` (kept for tests + single-line callers) |
| `_detect_semantic_violations(content)` | line 245 | Emits semantic-violation strings (sentinel detection + OQ-xxx-in-deliverable-rows regex `^\|\s*\d+\s*\|\s*OQ-\d+\s*\|`) |
| `_detect_cosmetic_violations(content)` | line 270 | THE detector — emits `CosmeticViolation` for every C1-C11 finding |
| `_apply_milestone_h3_rewrites(content)` | line 545 | Transformer for C1-C4 (stem alias + missing suffix + dash variant + wrong level) |
| `_apply_trailing_whitespace_fix(content)` | line 608 | C5+C6 transformer |
| `_apply_blank_line_collapse(content)` | line 633 | C7 transformer (`re.subn(r"\n{3,}", "\n\n", ...)`) |
| `_apply_smart_quote_fold(content)` | line 642 | C8 transformer (fence-skipped `line.translate(_SMART_QUOTE_MAP)`) |
| `_apply_table_padding_fix(content)` | line 660 | C9 transformer (9/7 cell schema match only) |
| `_apply_frontmatter_trim(content)` | line 697 | C10 transformer (YAML frontmatter block only) |
| `_apply_resource_subsection_rewrites(content)` | line 722 | C11 transformer — RR&D section H3 rewrites; this is the closest existing analog to the planned C13 (it tracks the same parent H2) |

### A.4 `apply_cosmetic_remediations` dispatcher table (lines 767-823)
| Klass-set guard | File:Line | Calls |
|---|---|---|
| `klasses & {"C1", "C2", "C3", "C4"}` | line 795 | `_apply_milestone_h3_rewrites` |
| `"C11" in klasses` | line 799 | `_apply_resource_subsection_rewrites` |
| `klasses & {"C5", "C6"}` | line 803 | `_apply_trailing_whitespace_fix` |
| `"C7" in klasses` | line 807 | `_apply_blank_line_collapse` |
| `"C8" in klasses` | line 811 | `_apply_smart_quote_fold` |
| `"C9" in klasses` | line 815 | `_apply_table_padding_fix` |
| `"C10" in klasses` | line 819 | `_apply_frontmatter_trim` |

Pure-cosmetic short-circuit @ line 788: `if not classification.is_pure_cosmetic: return content, []`.
`klasses = {v.klass for v in classification.cosmetic_violations}` @ line 791.

### A.5 `_detect_cosmetic_violations` emission table (lines 270-498)
| Klass | Emit site (file:line) | Trigger summary |
|---|---|---|
| C5 | line 287 | Header line trailing whitespace, fence-skipped |
| C6 | line 299 | Any non-header line trailing whitespace, fence-skipped |
| C8 | line 310 | `any(ch in line for ch in "‘’“”′″")`, fence-skipped |
| C3 | line 335 | `### ` heading whose stem matches `_REQUIRED_STEMS_LOWER` AND `_NONCANONICAL_DASH_PATTERN.search(line)` matches; pre-empts C2 via `continue` |
| C2 | line 350 | `### ` heading whose stem matches `_REQUIRED_STEMS_LOWER` AND `not suffix`; pre-empts C1 via `continue` |
| C1 | line 366 | `### ` heading whose stem is in `_STEM_ALIASES`; pre-empts C4 via `continue` |
| C4 | line 384 | `## ` or `#### ` heading whose stem is in `_REQUIRED_STEMS_LOWER`, inside a milestone scope, and not a `## M` line |
| C7 | line 403 | Whole-file `re.search(r"\n\n\n\n", content)` |
| C9 | line 414 | Pipe-table row with 9 or 7 cells lacking cell padding (single emission; `break` after first) |
| C10 | line 440 | Frontmatter line with `:` and trailing whitespace |
| C11 | line 461 | Inside `## Resource Requirements and Dependencies` scope: H3 whose lowercased body contains an alias from `_RESOURCE_SUBSECTION_ALIASES` and isn't already canonical |

---

## B. `gates.py` inventory (canonical sets the fix depends on)

### B.1 Canonical sets
| Symbol | File:Line | Contents |
|---|---|---|
| `_REQUIRED_H2_SECTIONS: frozenset[str]` | line 891 | `{"executive summary", "milestone summary", "dependency graph", "resource requirements and dependencies", "risk register", "success criteria and validation approach", "decision summary", "timeline estimates"}` — **the C12 safety-gate set** |
| `_REQUIRED_MILESTONE_SUBSECTIONS: tuple[str, ...]` | line 907 | `("integration points", "milestone dependencies", "risk assessment and mitigation")` |
| `_REQUIRED_RESOURCE_SUBSECTIONS: frozenset[str]` | line 914 | `{"external dependencies", "infrastructure requirements"}` |

### B.2 Key functions
| Function | File:Line | Behavior summary |
|---|---|---|
| `_normalize_heading(text)` | line 919 | `re.sub(r"^\s*\d+(?:\.\d+)*\.?\s+", "", text.strip()).lower().strip()` — **strips leading numbering prefix + lowercases ONLY**. Does NOT strip parentheticals. |
| `_template_sections_present(content)` | line 927 | The gate the fix unblocks. Builds `h2_normalized` list via `_normalize_heading`, requires `_REQUIRED_H2_SECTIONS.issubset(h2_set)` (line 979). For each `## M{N}:`, requires set of `{stem - m{n}, stem — m{n}, stem -- m{n}}` candidates intersect H3s (lines 992-1000). For RR&D parent, requires `_REQUIRED_RESOURCE_SUBSECTIONS.issubset(rr_subs)` (line 1012). |

The gate's H3 collection (lines 961-973) appends `stripped[4:].strip()` raw text into the current bucket; later `_normalize_heading` is applied. Critical for C13 design: the bucket is the parent-H2's H3 list, and lookups happen via the normalized H3 set.

### B.3 Registration of `_template_sections_present` as a check
| File:Line | Context |
|---|---|
| line 1128 | Used as `check_fn` in a `GateCriteria` instance |
| line 1215 | Used as `check_fn` in another `GateCriteria` instance |

(The fix only changes the upstream transformer such that the same `check_fn` then returns `True`.)

---

## C. DRIFT FLAGS

| Question | Answer | Evidence |
|---|---|---|
| Does ANY existing function/detector/transformer handle H2 parenthetical stripping? | **NO** | `grep -n "parenthe\|paren"` in both files returns zero hits. `_strip_section_numbering` (cosmetic_remediator.py:155) only strips numbering. `_normalize_heading` (gates.py:919) only strips numbering and lowercases. No `re.sub` against `\(.*?\)` exists in either file. |
| Does ANY existing function/detector/transformer perform non-alias-based renaming (token-overlap scoring, positional gap-fill, fuzzy matching)? | **NO** | `grep -n "token_overlap\|fuzzy\|positional"` returns zero hits. Every existing rewrite path is alias-driven: `_STEM_ALIASES` (line 64) is exact-match-on-lower; `_RESOURCE_SUBSECTION_ALIASES` (line 81) is substring-match-on-lower; no scoring, no Levenshtein, no positional inference. |
| Is there a `C12` or `C13` literal already present in either file? | **NO** | `grep -n "C12\|C13"` returns zero hits in both files. The dispatcher (line 791) keys off `v.klass` strings, so C12/C13 simply need to be added to the violation table + dispatcher table. |
| Does `_normalize_heading` (gates.py) strip parentheticals? | **NO** (verified — this is the divergence the fix exploits) | gates.py:919-924: only `re.sub(r"^\s*\d+(?:\.\d+)*\.?\s+", "", text.strip())` then `.lower().strip()`. An H2 like `## Resource Requirements and Dependencies (External + Infra)` would normalize to `"resource requirements and dependencies (external + infra)"` and FAIL the `_REQUIRED_H2_SECTIONS.issubset` check at line 979 — which is exactly why C12 (strip the parenthetical in the source content before the gate runs) unblocks the gate without changing gate logic. |

---

## D. Insertion-point recommendations (no line-edits performed)

For C12 (H2 parenthetical strip, safety-gated on `_REQUIRED_H2_SECTIONS`):
- Add canonical-set import or local lowercased copy near the existing constants (after line 128, before the `@dataclass` block at line 131).
- Add detector branch in `_detect_cosmetic_violations` (cosmetic_remediator.py:270) — natural slot is after the C10 frontmatter block (line 454) and before the C11 resource section block (line 456), keeping a top-of-file C-number-ordered detector layout.
- Add transformer `_apply_h2_parenthetical_strip` near `_apply_resource_subsection_rewrites` (line 722). The latter is the closest structural analog (H2 walking + per-line rewrite).
- Add dispatcher branch in `apply_cosmetic_remediations` between C4 (line 795) and C11 (line 799). Ordering note: C12 must precede any transformer that uses the C12-stripped H2 text for parent-section tracking.

For C13 (gap-driven H3 repair under known parent H2s, scoped initially to `## Resource Requirements and Dependencies`):
- The detector needs to know `_REQUIRED_RESOURCE_SUBSECTIONS` (gates.py:914) — either re-import or mirror in cosmetic_remediator.py.
- Detector placement: after the existing C11 block (cosmetic_remediator.py:497) — C11 normalizes alias spellings, C13 fills in missing-but-required spellings.
- Transformer placement: directly after `_apply_resource_subsection_rewrites` (line 764) so C13 runs after C11's alias normalization (i.e., C13 sees the post-C11 set of canonical H3s and only injects what's still missing).
- Dispatcher branch placement: directly after the `"C11" in klasses` branch (line 799).

---

## Summary

Inventory complete. Both files are fully alias-driven with zero existing parenthetical-stripping or non-alias-based-rename logic. No `C12`/`C13` literals exist. `_normalize_heading` (gates.py:919) only strips numbering and lowercases — confirming the divergence the hybrid fix exploits. The closest structural analog for both new transformers is `_apply_resource_subsection_rewrites` (cosmetic_remediator.py:722), which already tracks parent-H2 scope. The dispatcher (line 767) is a simple klass-set guard table with stable execution order — adding C12 (before resource transforms) and C13 (after `_apply_resource_subsection_rewrites`) is mechanical. Canonical sets `_REQUIRED_H2_SECTIONS` (gates.py:891) and `_REQUIRED_RESOURCE_SUBSECTIONS` (gates.py:914) are the safety-gate sources of truth that C12 and C13 must reference.

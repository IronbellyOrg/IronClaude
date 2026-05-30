# Research: Gap-Fill — H3-tracking mechanism + test fixture correction
**Topic type:** Gap-fill (replaces research 01 §5/§8/§10 + research 02 §6)
**Scope:** obligation_scanner.py (BareReview worktree) — empirical re-verification
**Status:** Complete
**Date:** 2026-05-29
**Triggered by:** rf-qa research-gate CRITICAL finding
---

## 0. Empirical Re-Verification — _split_into_phases on real roadmap

`_split_into_phases` (obligation_scanner.py:404-445) regex at line 411-413:

```python
phase_pattern = re.compile(
    r"^(#{2,3})\s+((?:(?:Phase|Step|Stage|Milestone)\s+|M)\d+[\w.]*.*?)$",
    re.MULTILINE | re.IGNORECASE,
)
```

The character class after the alternation `(Phase|Step|Stage|Milestone)\s+|M` requires `\d+` to immediately follow. So the matcher demands one of:

- Literal `Phase|Step|Stage|Milestone` followed by `\s+\d+...`
- Literal `M\d+...` (M directly butted against a digit)

Run against `.dev/releases/Current/MultiModelSwarm/roadmap.md`:

```
Total sections: 10
  line 62: M1: Foundation & Domain Models
  line 119: M2: Transport & Recipe Layers
  line 164: M3: Lens Registry & Validator
  line 214: M4: Wave 0 — Preflight
  line 253: M5: Wave 1 — Parallel Dispatch
  line 294: M6: Wave 2/3 — Normalize, Reduce, Merge
  line 335: M7: CLI Surface, Observability, Resilience
  line 407: M8a: IMM Invariant Test Suite
  line 439: M8b: INV + Boundary Test Suite
  line 476: M9: sc-bare-review Migration & A/B Parity
```

**Empirically confirmed:** 10 H2 sections, ZERO H3 sub-sections. Every `### Risk Assessment and Mitigation — M{n}`, `### Integration Points — M{n}`, `### Milestone Dependencies — M{n}`, `### Open Questions — M{n}` is absorbed into the enclosing M{n} chunk because none of those H3 strings start with `Phase|Step|Stage|Milestone\s+` or `M\d`.

**End-to-end scanner check on the same file:**

```
Total: 26
Undischarged (excl MEDIUM/exempt): 8

Undischarged HIGH obligations:
  line 145: phase='M2: Transport & Recipe Layers' term='stub'
  line 149: phase='M2: Transport & Recipe Layers' term='stub'
  line 278: phase='M5: Wave 1 — Parallel Dispatch' term='stub'
  line 425: phase='M8a: IMM Invariant Test Suite' term='Stub'
  line 425: phase='M8a: IMM Invariant Test Suite' term='stub'
  line 437: phase='M8a: IMM Invariant Test Suite' term='Stub'
  line 437: phase='M8a: IMM Invariant Test Suite' term='stub'
  line 474: phase='M8b: INV + Boundary Test Suite' term='Stub'
```

Every single FP carries the H2 milestone name as `phase`. **No `phase_id` ever equals `"Risk Assessment and Mitigation — M2"` or any H3 text.** Research 01's `_is_demoted_subsection(phase_id)` premise is empirically falsified.

---

## 1. Scanner Main Loop Reality

### 1a. The loop iterates over chunks, not raw lines

`scan_obligations` at obligation_scanner.py:209:

```python
for i, (phase_id, phase_content, start_line) in enumerate(sections):
    for match in _SCAFFOLD_RE.finditer(phase_content):
```

The OUTER loop is over `sections` (chunks from `_split_into_phases`). The INNER loop is over scaffold-term matches **within each chunk's text**. The chunk's text is a raw multi-line string spanning from one H2 to the next; it includes all H3 subsection headings as inline `### ...` lines AND their body content.

### 1b. Context available at severity-assignment time

Severity is set in two locations (obligation_scanner.py:318 and 321-337). At those points, the local variables are:

| Variable | Source | Line |
|---|---|---|
| `i` | outer-loop index over sections | 209 |
| `phase_id` | H2 phase title, e.g. `"M2: Transport & Recipe Layers"` | 209 |
| `phase_content` | the multi-line H2-chunk body | 209 |
| `start_line` | absolute line number of the H2 heading in original `content` | 209 |
| `match` | the scaffold-term `re.Match` against `phase_content` | 210 |
| `term` | the matched scaffold term, e.g. `"stub"` | 211 |
| `context_line` | the single line containing the match (stripped) | 212 |
| `abs_line` | `start_line + phase_content[:match.start()].count("\n")` — absolute line in original content | 213 |
| `stripped_context` | left-stripped `context_line` | 220 |
| `ctx_lower` | `context_line.lower()` | 238 |
| `component` | extracted near-by component anchor | 310 |
| `abs_pos` | absolute char offset in original content | 317 |

**Key fact:** `abs_line` (line 213) is already computed BEFORE severity is set. It is the absolute line number of the match in the ORIGINAL `content`. Any H3-tracking design can lean on this without recomputation.

### 1c. Existing H3 state tracking inside a phase body — CONFIRMED ABSENT

Grep for any reference to H3-tracking state within `scan_obligations` or its helpers:

- No variable named `h3`, `subsection`, `current_h3`, `h3_state`, or similar appears anywhere in `obligation_scanner.py`.
- The skip-heading branch at lines 220-225 simply `continue`s past lines that **start with** `## ` or `### `; it does not capture or remember which subsection a non-heading line lies under.
- `_split_into_phases` discards all H3 boundary information when it returns the section tuple (only H2 boundaries inform chunk start/end).

There is currently **no H3-state tracking anywhere in the scanner**. Layer 5 must introduce it.

---

## 2. H3-Tracking Design — Three Concrete Options Compared

### Option A — Pre-scan H3 index `{line_number → containing_H3_text}`

**Touch sites:**
- New helper function `_build_h3_index(content: str) -> dict[int, str]` — added near `_split_into_phases` (~line 446).
- `scan_obligations` body: call `h3_index = _build_h3_index(content)` once after line 204 (alongside `code_block_ranges`).
- New helper `_is_demoted_h3(h3_text: str | None) -> bool` — invoked at the Layer 5 branch point (see §3 below).
- Lookup: `h3_for_line = h3_index.get(abs_line)` at the Layer 5 branch.

**Code-change size:** ~25 lines added (helper + lookup + Layer 5 branch). Zero lines modified in `_split_into_phases` or chunk loop.

**Blast radius:** **LOW.** No change to data shape returned by `_split_into_phases`. No change to chunk iteration. All discharge / component / severity-1-through-4 logic continues to operate on the existing chunk text. The only new state is a read-only line→H3 dict.

**Pros:** Surgical. Easy to unit-test the index in isolation. Index uses `abs_line` which is already computed for every obligation. Index is computed once (O(n) regex over `content`).

**Cons:** Two passes over `content` (one for splitter, one for H3 index). Negligible cost (microseconds).

---

### Option B — Augment `_split_into_phases` to emit H3 sub-chunks

**Touch sites:**
- `_split_into_phases` regex at lines 411-413 widened to also match H3 patterns, OR recursive logic added to walk each milestone's body for `### ` headings and emit `(phase_id="M2 > Risk Assessment and Mitigation", text=..., start_line=...)` sub-tuples.
- Downstream consumers of `phase_id`: cross-phase discharge search at lines 344-355 (would now scan sub-chunks instead of whole milestones; risks breaking discharge matching where discharge lives in a later H3 of the SAME milestone).
- All call sites that depend on `phase` being a milestone name (e.g., `gates.py` filtering, test fixtures asserting `o.phase == "M2"`).

**Code-change size:** ~15-30 lines in splitter + UNKNOWN downstream churn (discharge logic, gates, tests, gate-reports).

**Blast radius:** **HIGH.** Changes the contract of every tuple in `sections`. Test 1 in the current suite asserts `o.phase == "M2: Transport & Recipe Layers"`-style values. Cross-phase discharge (line 344) would now skip discharge candidates in sibling H3s of the same milestone. Any consumer of `ObligationReport.obligations[*].phase` would need re-verification.

**Pros:** Conceptually cleanest. Single source of truth for "where am I?"

**Cons:** Drastically increases the scope of this fix and almost certainly breaks tests outside the Layer 5 scope.

---

### Option C — Mutable `current_h3` variable inside per-phase scan loop

**Touch sites:**
- Inside the chunk loop (obligation_scanner.py:209-370), introduce `current_h3: str | None = None`.
- BEFORE the `_SCAFFOLD_RE.finditer` inner loop (which iterates *matches*, not lines), would need to either (a) switch to line-by-line iteration over `phase_content` and re-scan each line for scaffold terms, or (b) keep `finditer` and at each match recompute the nearest-preceding `### ` heading inside `phase_content[:match.start()]` (an O(n) reverse-scan per match).

**Code-change size:** Approach (a) ~40-60 lines (rewrite of the chunk loop). Approach (b) ~15 lines but O(n²) worst case across many matches.

**Blast radius:** **MEDIUM.**
- Approach (a) rewrites the inner loop — non-trivial risk of regression on the 4 existing layers' regex logic, ordering, and `continue` branches (lines 217-307).
- Approach (b) is functionally similar to Option A but pays the cost per-match instead of once. Strictly worse.

**Pros:** Localized state.

**Cons:** Either rewrites well-tested inner loop (a) or is strictly worse than Option A (b). Reset-on-phase-boundary semantics are tricky because `phase_content` is already a per-chunk slice — the H3 state is naturally reset by re-entering the outer loop, but if approach (b) is used, the state isn't really "tracked" — it's recomputed per match.

---

### Comparison Summary

| Option | LOC delta | Blast radius | Data-shape change | Recommended |
|---|---|---|---|---|
| A (pre-scan index) | +25 | LOW | None | **YES** |
| B (emit H3 sub-chunks) | +15-30 splitter + UNKNOWN downstream | HIGH | Changes `phase_id` contract | NO |
| C (in-loop state) | +15 (slow) or +40-60 (rewrite) | MEDIUM | None | NO |

---

## 3. Recommended Option — A — with exact code shape

### 3a. Helper function signature and body

```python
# Placed immediately after _split_into_phases (~ line 446).

# Compiled at module load (alongside other regexes around line 100).
_H3_HEADING_RE = re.compile(r"^###\s+(.+?)$", re.MULTILINE)
_H2_HEADING_RE = re.compile(r"^##\s+.+?$", re.MULTILINE)

# Subsection prefixes (canonical) that Layer 5 will demote when a scaffold
# term sits inside their H3 body. Matched as case-insensitive PREFIX after
# stripping the trailing ` — M{n}` / `— M{n}` decoration (em-dash + tag).
_DEMOTE_H3_PREFIXES: tuple[str, ...] = (
    "risk assessment",
    "integration points",
    "milestone dependencies",
    "open questions",
)


def _normalize_h3_for_match(h3_text: str) -> str:
    """Strip trailing ' — M{n}' decoration and lowercase for prefix match.

    Roadmap convention is `### Risk Assessment and Mitigation — M2`. The
    em-dash tag is removed and the remainder lowercased before matching
    against `_DEMOTE_H3_PREFIXES`.
    """
    # Strip ' — M<digits><suffix>' (em-dash U+2014; tolerate ascii ' - ' too)
    stripped = re.sub(
        r"\s+[—-]\s+M\d+\w*\s*$",
        "",
        h3_text.strip(),
        flags=re.IGNORECASE,
    )
    return stripped.lower()


def _build_h3_index(content: str) -> dict[int, str]:
    """Map every line number in `content` to the H3 heading text that
    contains it, or to '' if no H3 governs the line (i.e., between an H2
    and the first H3 inside that milestone, or in a tail section).

    H3 scope ends at the next ### heading OR the next ## heading.
    Line numbers are 1-based, matching `Obligation.line_number`.
    """
    index: dict[int, str] = {}
    # Build a sorted list of (line_number, kind, text) boundaries.
    boundaries: list[tuple[int, str, str]] = []
    for m in _H3_HEADING_RE.finditer(content):
        line_no = content[: m.start()].count("\n") + 1
        boundaries.append((line_no, "h3", m.group(1).strip()))
    for m in _H2_HEADING_RE.finditer(content):
        line_no = content[: m.start()].count("\n") + 1
        boundaries.append((line_no, "h2", ""))
    boundaries.sort(key=lambda b: b[0])

    total_lines = content.count("\n") + 1
    current_h3 = ""
    boundary_iter = iter(boundaries)
    next_boundary = next(boundary_iter, None)
    for line_no in range(1, total_lines + 1):
        while next_boundary is not None and next_boundary[0] == line_no:
            kind, text = next_boundary[1], next_boundary[2]
            if kind == "h2":
                current_h3 = ""  # H2 resets H3 state
            else:  # h3
                current_h3 = text
            next_boundary = next(boundary_iter, None)
        index[line_no] = current_h3
    return index


def _is_demoted_h3(h3_text: str) -> bool:
    """Return True if the H3 heading is one of the 4 demote-target subsections."""
    if not h3_text:
        return False
    normalized = _normalize_h3_for_match(h3_text)
    return any(normalized.startswith(prefix) for prefix in _DEMOTE_H3_PREFIXES)
```

### 3b. Exact branch point in `scan_obligations`

Insert AFTER the existing Layer 4 demotion check and BEFORE the line-numbered comment for FR-MOD1.3 cross-phase discharge search (currently obligation_scanner.py:339). The chain becomes:

```python
# Layer 2: Negation/meta-context classification  (existing, line 332-337)
elif severity == "HIGH":
    line_start = phase_content.rfind("\n", 0, match.start()) + 1
    term_start_in_line = match.start() - line_start
    if _is_meta_context(context_line, term_start_in_line):
        severity = "MEDIUM"

# Layer 5 (NEW): subsection-aware demotion.
# Scaffold terms inside Risk Assessment / Integration Points / Milestone
# Dependencies / Open Questions H3 subsections of a milestone body are
# meta-reference / cross-milestone-link prose, not new obligations.
# Guarded by `_is_discharge_intent_line` to preserve genuine obligations
# like "outcome: scaffold needs replacement" that may appear in those
# subsections (mirrors Layer 4's guard at line 589).
if severity == "HIGH":
    h3_text = h3_index.get(abs_line, "")
    if _is_demoted_h3(h3_text) and not _is_discharge_intent_line(context_line):
        severity = "MEDIUM"
```

And the one-line addition near line 204 (pre-compute step):

```python
# Pre-compute code block ranges for severity demotion
code_block_ranges = _get_code_block_ranges(content)
# Pre-compute line → containing H3 index for Layer 5 subsection demotion
h3_index = _build_h3_index(content)
```

`abs_line` is already in scope at the Layer 5 branch (computed at line 213) — no recomputation needed.

### 3c. Why this is the right place

- It runs AFTER Layer 4 because Layer 4's descriptor-adjacency check operates on intra-line text, independent of subsection context. If Layer 4 already demoted to MEDIUM, Layer 5 is a no-op (the `if severity == "HIGH"` guard skips). Order doesn't matter for correctness, but placing Layer 5 last preserves the "Layer N+1 only fires if Layer N didn't" idiom already in use.
- It runs BEFORE discharge search (line 344) so the severity assignment is final when the obligation is built at line 357.

---

## 4. Discharge-Intent Guard for Layer 5 — YES (recommended)

**Evidence:** Layer 4's `_is_descriptive_context` at obligation_scanner.py:576-594 uses `_is_discharge_intent_line` (line 589) as a guard to prevent demoting lines that mention discharge verbs. Quote:

```python
def _is_descriptive_context(line: str, term_start_in_line: int) -> bool:
    """True when a scaffold term sits within ~4 words of a descriptor noun AND
    the line does NOT signal discharge intent.
    ...
    The discharge-intent guard
    ensures lines like ``outcome: scaffold needs replacement`` (a real
    obligation) remain HIGH.
    ...
    """
    if _is_discharge_intent_line(line):
        return False
    ...
```

**`_is_discharge_intent_line` body** (obligation_scanner.py:669-684):

```python
def _is_discharge_intent_line(line: str) -> bool:
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

**Recommendation: YES, apply this same guard to Layer 5.**

**Reasoning:**

1. **Symmetry with Layer 4.** Layer 5 is conceptually identical to Layer 4 (descriptive context demotion) but keyed off subsection structure instead of intra-line lexical adjacency. Same semantic class deserves the same guard.
2. **Preserves true positives inside Risk Assessment.** Research 03 §7 notes the (rare) failure mode where a future author places a genuine obligation under "Integration Points" by accident. The discharge-intent guard catches the most common form of that mistake: a line saying "Integration Points — M2 stub needs replacement in M5" would correctly remain HIGH.
3. **Zero cost on the 6 known FP lines.** Re-check each line against `_is_discharge_intent_line`:
   - Line 145: `|`openai_compat.py` httpx transport|Strategy implementation|Registered in M2 (alongside M1 stub)|M2|M5 (production dispatch)|` — no discharge verb. Demoted ✓
   - Line 149: `- M1 (domain models for `DM-009`; `DM-010` interface; `COMP-018` package + stub).` — no discharge verb. Demoted ✓
   - Line 278: `|Transport `dispatch()` binding|Strategy selection|Bound from M2 transport per `transport.kind`|M5|M8a (stub-transport tests)|` — no discharge verb. Demoted ✓
   - Line 425: `|Stub transport fixture|Test DI/strategy|Bound from M1 stub for IMM tests in M8a|M8a|CI, M9 (parity harness reuse)|` — no discharge verb. Demoted ✓
   - Line 437: `|2|Stub transport drifts from real T2 proxy semantics|Medium|Low|Tests pass but production differs|Pin stub to documented OpenAI-compat response shape; periodic contract check against real proxy in M9|backend|` — no discharge verb. Demoted ✓
   - Line 474: `|3|Parallel M8a/M8b coordination drift|Low|Low|Test infra duplication / shared fixtures conflict|Stub-transport + fixture directory layout finalized in M5; both halves consume same fixtures|qa|` — no discharge verb. Demoted ✓

All 8 FP findings demote cleanly with the guard in place.

---

## 5. Test Fixture Correction

The original research 02 §6 fixtures used H3 text like `### Risk Assessment Matrix`, which does NOT match the real roadmap convention. Research 03 confirmed the actual convention is `### Risk Assessment and Mitigation — M{n}` (em-dash + milestone tag).

### Test 1 — Happy path: H3 demote inside `Risk Assessment and Mitigation — M{n}`

**Fixture:**

```markdown
## M2: Transport Layer

**Objective:** Build the dispatch layer.

### Risk Assessment and Mitigation — M2

| # | Risk | L | I | Detection | Mitigation | Owner |
|---|---|---|---|---|---|---|
| 1 | Stub transport drifts from real semantics | Med | Low | tests pass | Pin stub to documented shape | backend |
```

**Assertion:** The two `stub` / `Stub` matches on the risk-table row are present in `report.obligations` with `severity == "MEDIUM"`. Their `phase` is `"M2: Transport Layer"` (the H2 string), NOT the H3 text.

### Test 2 — H3 state resets at next H2 boundary

**Fixture:**

```markdown
## M2: Transport Layer

### Risk Assessment and Mitigation — M2

| 1 | Stub transport drifts | Med | Low | Tests pass | Pin stub shape | backend |

## M3: Lens Registry

**Objective:** Build a stub registry that will be wired to real lenses later.
```

**Assertion:**
- The `stub` / `Stub` matches inside the M2 risk row are MEDIUM (Layer 5 fired).
- The `stub` match on the line `**Objective:** Build a stub registry ...` under M3 is filtered by the existing `**Objective:` skip at line 231 (so it never reaches Layer 5). To exercise H3 reset cleanly, replace the M3 body with a non-Objective line, e.g.:

```markdown
## M3: Lens Registry

| 3.1 | Build stub registry component | DM-100 |
```

This M3 line lies under NO H3 (the H3 state was reset by the M3 H2). The fixture asserts that the M3 `stub` finding has `severity == "HIGH"` — proof that H3 state did not bleed across the H2 boundary.

### Test 3 — Other demote-target subsections (Integration Points / Milestone Dependencies / Open Questions)

**Fixture (Integration Points variant):**

```markdown
## M5: Parallel Dispatch

### Integration Points — M5

| Transport `dispatch()` binding | Strategy selection | M8a (stub-transport tests) |
```

**Assertion:** The `stub` match in the Integration Points table row has `severity == "MEDIUM"`. Same fixture pattern repeats with `### Milestone Dependencies — M5` and `### Open Questions — M5` swapped in for full coverage of all 4 demote-target prefixes.

A more compact form uses table-parameterized tests:

```python
@pytest.mark.parametrize("h3_text", [
    "Risk Assessment and Mitigation — M2",
    "Integration Points — M2",
    "Milestone Dependencies — M2",
    "Open Questions — M2",
])
def test_layer5_demotes_in_demote_target_h3(h3_text: str) -> None:
    content = (
        "## M2: Foo\n\n"
        f"### {h3_text}\n\n"
        "- Reference to M1 stub for context.\n"
    )
    report = scan_obligations(content)
    stubs = [o for o in report.obligations if o.term.lower() == "stub"]
    assert all(o.severity == "MEDIUM" for o in stubs), \
        f"Expected MEDIUM under '### {h3_text}', got {[o.severity for o in stubs]}"
```

### Test 4 (recommended addition) — Discharge-intent guard keeps real obligation HIGH inside a demote-target subsection

```python
def test_layer5_discharge_intent_keeps_high() -> None:
    content = (
        "## M2: Foo\n\n"
        "### Risk Assessment and Mitigation — M2\n\n"
        "- Mitigation: replace the M1 stub with real transport by M5.\n"
    )
    report = scan_obligations(content)
    stubs = [o for o in report.obligations if o.term.lower() == "stub"]
    assert any(o.severity == "HIGH" for o in stubs), \
        "Discharge-intent line must remain HIGH even inside Risk Assessment subsection"
```

This locks the discharge-intent guard from §4.

---

## 6. Reconciliation: Prior Task Deferral vs Current Task Reversal

The prior task's Follow-Up Items §234 (per research 04 §5) explicitly deferred the "subsection-aware demotion of Risk Assessment / Integration Points / Milestone Dependencies / Open Questions" work to a future Layer 5. **The current task IS that future Layer 5 work.**

There is **NO contradiction** between the prior deferral and the present implementation:

- Prior task scope: Layers 1-4 (inline code, completed checklist, negation prefix, descriptor-noun adjacency).
- Prior task explicitly marked subsection-aware demotion as out-of-scope follow-up.
- Current task scope: the deferred Layer 5 itself.

Research 04 §5 did not flag this; flagging it here. The task-builder MUST cite the prior task's Follow-Up Items §234 in the new task's "Context / Prior Work" section as the explicit authorization for this work, not as a contradicting constraint.

---

## 7. CRITICAL — Research 01's `_is_demoted_subsection(phase_id)` cascade-branch is WRONG

**DO NOT USE the design from research 01 §5 / §8 / §10.**

Research 01 proposed a Layer 5 branch keyed off `phase_id` — e.g., `if _is_demoted_subsection(phase_id): severity = "MEDIUM"`. That design assumed `_split_into_phases` would emit standalone `phase_id` entries for H3 subsections. The empirical evidence in §0 above proves it does NOT: every section returned is an H2 milestone (`M1:` through `M9:`), and the 4 demote-target H3s are absorbed silently into their parent milestone's chunk.

The downstream consequence of using research 01's design: `_is_demoted_subsection("M2: Transport & Recipe Layers")` would return False for every one of the 8 target FPs (because none of the 8 phase_ids contain "Risk Assessment", "Integration Points", "Milestone Dependencies", or "Open Questions"). **Layer 5 would silently never fire.** All 8 FPs would remain HIGH and the fix would appear to ship while accomplishing nothing.

**The correct design is Option A in §2-3 above:** key Layer 5 off the per-line H3 index, NOT off `phase_id`.

---

## 8. Builder Directives (copy-pastable)

### 8a. Source-of-truth file to edit

`src/superclaude/cli/roadmap/obligation_scanner.py` (then `make sync-dev`).

### 8b. Layer 5 mechanism — Option A: pre-scan H3 index

**Add module-level constants (alongside existing regexes ~line 100):**

```python
_H3_HEADING_RE = re.compile(r"^###\s+(.+?)$", re.MULTILINE)
_H2_HEADING_RE = re.compile(r"^##\s+.+?$", re.MULTILINE)

_DEMOTE_H3_PREFIXES: tuple[str, ...] = (
    "risk assessment",
    "integration points",
    "milestone dependencies",
    "open questions",
)
```

**Add helpers immediately after `_split_into_phases` (~line 446):**

```python
def _normalize_h3_for_match(h3_text: str) -> str:
    stripped = re.sub(
        r"\s+[—-]\s+M\d+\w*\s*$",
        "",
        h3_text.strip(),
        flags=re.IGNORECASE,
    )
    return stripped.lower()


def _build_h3_index(content: str) -> dict[int, str]:
    """Map line number (1-based) → containing H3 text (or '' if none).
    H3 scope ends at the next H3 or H2 heading."""
    boundaries: list[tuple[int, str, str]] = []
    for m in _H3_HEADING_RE.finditer(content):
        line_no = content[: m.start()].count("\n") + 1
        boundaries.append((line_no, "h3", m.group(1).strip()))
    for m in _H2_HEADING_RE.finditer(content):
        line_no = content[: m.start()].count("\n") + 1
        boundaries.append((line_no, "h2", ""))
    boundaries.sort(key=lambda b: b[0])

    total_lines = content.count("\n") + 1
    index: dict[int, str] = {}
    current_h3 = ""
    boundary_iter = iter(boundaries)
    next_boundary = next(boundary_iter, None)
    for line_no in range(1, total_lines + 1):
        while next_boundary is not None and next_boundary[0] == line_no:
            kind, text = next_boundary[1], next_boundary[2]
            current_h3 = "" if kind == "h2" else text
            next_boundary = next(boundary_iter, None)
        index[line_no] = current_h3
    return index


def _is_demoted_h3(h3_text: str) -> bool:
    if not h3_text:
        return False
    normalized = _normalize_h3_for_match(h3_text)
    return any(normalized.startswith(prefix) for prefix in _DEMOTE_H3_PREFIXES)
```

**Edit `scan_obligations` pre-compute block (line 203-204):**

```python
code_block_ranges = _get_code_block_ranges(content)
h3_index = _build_h3_index(content)  # NEW for Layer 5
```

**Insert Layer 5 branch AFTER the existing Layer 2 elif (line 337), BEFORE the FR-MOD1.3 cross-phase discharge search (line 339):**

```python
# Layer 5: subsection-aware demotion.
# Scaffold terms inside Risk Assessment / Integration Points / Milestone
# Dependencies / Open Questions H3 subsections are meta-reference prose,
# not new obligations. Discharge-intent guard preserves genuine obligations
# (mirrors Layer 4's guard).
if severity == "HIGH":
    h3_text = h3_index.get(abs_line, "")
    if _is_demoted_h3(h3_text) and not _is_discharge_intent_line(context_line):
        severity = "MEDIUM"
```

### 8c. Test fixtures — CORRECTED H3 text

Use the EXACT H3 strings below (em-dash U+2014 plus milestone tag):

| Test | H3 string |
|---|---|
| Test 1 (happy path) | `### Risk Assessment and Mitigation — M2` |
| Test 2 (reset at H2) | `### Risk Assessment and Mitigation — M2` then `## M3: ...` |
| Test 3 (other subsections) | `### Integration Points — M5`, `### Milestone Dependencies — M5`, `### Open Questions — M5` |
| Test 4 (discharge-intent guard) | `### Risk Assessment and Mitigation — M2` with body line containing `replace` |

The em-dash MUST be U+2014, NOT a hyphen-minus. The matcher's `_normalize_h3_for_match` regex tolerates both, but the fixture should match the real roadmap convention (U+2014).

### 8d. Forbidden design — do NOT implement

`_is_demoted_subsection(phase_id)` — keyed off `phase_id`. Research 01 §5/§8/§10 are wrong; Layer 5 would never fire. See §7.

### 8e. Reconciliation note for the task file

Cite the prior task's Follow-Up Items §234 as explicit authorization. The current task is the deferred Layer 5 work, not a contradiction of the prior task. See §6.

---

## 9. Gotchas Surfaced During Gap-Fill

1. **Em-dash vs hyphen-minus.** Roadmap uses U+2014 (`—`). `_normalize_h3_for_match` regex `\s+[—-]\s+` tolerates both, but a fixture authored with a hyphen-minus would still match; just document the canonical form to keep fixtures consistent with the real roadmap.
2. **H3 inside tail sections.** `_build_h3_index` does not know about tail sections (Resource Requirements, Risk Register, etc., starting at line 507 of the target roadmap). Those tail sections also contain H3s like `### External Dependencies` (line 509) and `### Infrastructure Requirements` (line 525). Those H3 names do NOT match any of the 4 demote-target prefixes, so Layer 5 will correctly NOT fire there. No special-casing needed — but worth a one-line comment in `_build_h3_index` noting the behavior is correct by virtue of prefix-set selectivity.
3. **`scan_obligations` line 213 `abs_line` is 1-based.** `_build_h3_index` MUST return a 1-based index for the lookup to align. The reference implementation above uses 1-based; the test suite should assert this once (e.g., `assert index[1] == ""` for content that begins with a body line, not a heading).
4. **`_build_h3_index` time complexity.** O(n) over total line count; called once per `scan_obligations` invocation. Negligible for roadmaps <10k lines. Memory: one string per line. Acceptable.
5. **Empty roadmap / no headings.** `_build_h3_index("")` returns `{1: ""}` (one line, no H3). `_is_demoted_h3("")` returns False. Safe.
6. **Hyphen-minus in M-tag suffix.** Roadmap uses `M8a`, `M8b`. `_normalize_h3_for_match` regex `M\d+\w*` correctly handles the alphanumeric suffix. Verified via the M8a/M8b H3 strings in research 03 §2.
7. **`phase` field on the resulting Obligation remains the H2 string** (e.g., `"M2: Transport & Recipe Layers"`). Test fixtures from the existing suite that assert against this field are unaffected by Layer 5.

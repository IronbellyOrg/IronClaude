# Research: gates.py check functions + STRICT criteria

- **Topic type:** File Inventory
- **Scope:** `/config/workspace/IronClaude/src/superclaude/cli/prd/gates.py` (+ grep for call sites in `executor.py`; model contract in `cli/pipeline/models.py`)
- **Status:** Complete
- **Date:** 2026-06-06
- **Track goal:** Layer 3 adds an optional `_check_no_truncation_marker(content) -> bool | str` to gates.py. STRICT criteria + existing semantic checks MUST stay UNCHANGED.

---

## CRITICAL: BUILD_REQUEST line numbers are STALE

The BUILD_REQUEST estimates (~110-154 / ~329-345) are **off by ~10-15 lines**. The
file is **514 lines** total. Re-confirmed actual numbers below. Every claim cites
`gates.py:LINE` with verbatim code.

---

## 1. research-notes STRICT criteria block (gates.py:329-346)

Actual location is **329-346** (BUILD_REQUEST said ~329-345 — close, end is 346):

```python
329    # Step 4: Research Notes
330    "research-notes": GateCriteria(
331        required_frontmatter_fields=["Date", "Scenario", "Tier"],
332        min_lines=100,
333        enforcement_tier="STRICT",
334        semantic_checks=[
335            _make_semantic_check(
336                "research_notes_sections",
337                _check_research_notes_sections,
338                "Research notes missing required sections",
339            ),
340            _make_semantic_check(
341                "suggested_phases_detail",
342                _check_suggested_phases_detail,
343                "Suggested Phases section lacks detail",
344            ),
345        ],
346    ),
```

**Facts:**
- `min_lines=100` (gates.py:332)
- `enforcement_tier="STRICT"` (gates.py:333)
- `required_frontmatter_fields=["Date", "Scenario", "Tier"]` (gates.py:331)
- Invokes exactly **two** semantic checks (gates.py:334-345):
  1. `_check_research_notes_sections` (named `"research_notes_sections"`)
  2. `_check_suggested_phases_detail` (named `"suggested_phases_detail"`)

**INV constraint:** This block must remain UNCHANGED. The new
`_check_no_truncation_marker` must NOT be added to this `semantic_checks=[...]`
list if the requirement is "STRICT criteria stay unchanged" — see §5 wiring
analysis below for the decision.

---

## 2. `_check_research_notes_sections` (gates.py:121-134; section-list 110-118)

The required-sections constant (gates.py:110-118):

```python
110 _RESEARCH_REQUIRED_SECTIONS = [
111     "EXISTING_FILES",
112     "PATTERNS_AND_CONVENTIONS",
113     "FEATURE_ANALYSIS",
114     "RECOMMENDED_OUTPUTS",
115     "SUGGESTED_PHASES",
116     "TEMPLATE_NOTES",
117     "AMBIGUITIES_FOR_USER",
118 ]
```

The check function (gates.py:121-134):

```python
121 def _check_research_notes_sections(content: str) -> bool | str:
122     """Check that research notes contain all 7 required sections."""
123     missing = []
124     for section in _RESEARCH_REQUIRED_SECTIONS:
125         # Match as markdown heading (## or ###) or bold text
126         heading_pat = re.compile(
127             rf"^\s*#{{1,4}}\s+.*{re.escape(section)}", re.MULTILINE | re.IGNORECASE
128         )
129         bold_pat = re.compile(rf"\*\*{re.escape(section)}\*\*", re.IGNORECASE)
130         if not heading_pat.search(content) and not bold_pat.search(content):
131             missing.append(section)
132     if missing:
133         return f"Missing research sections: {', '.join(missing)}"
134     return True
```

**Requires 7 sections** (gates.py:110-118): EXISTING_FILES,
PATTERNS_AND_CONVENTIONS, FEATURE_ANALYSIS, RECOMMENDED_OUTPUTS,
SUGGESTED_PHASES, TEMPLATE_NOTES, AMBIGUITIES_FOR_USER. Each matched as a
markdown heading (`#`–`####`) OR bold (`**SECTION**`), case-insensitive.
Returns `True` on pass, an error string listing the missing sections on fail.

---

## 3. `_check_suggested_phases_detail` (gates.py:137-154)

```python
137 def _check_suggested_phases_detail(content: str) -> bool | str:
138     """Check that the Suggested Phases section contains per-agent detail.
139
140     Expects at least one numbered or bulleted list item under a Phases heading.
141     """
142     phases_match = re.search(
143         r"(?:^|\n)\s*#{1,4}\s+.*(?:Suggested[\s_]+)?Phases",
144         content,
145         re.IGNORECASE,
146     )
147     if not phases_match:
148         return "No 'Suggested Phases' section found"
149     # Check for list items after the heading
150     after_heading = content[phases_match.end() :]
151     list_pat = re.search(r"(?:^|\n)\s*(?:\d+\.|[-*])\s+\S", after_heading)
152     if not list_pat:
153         return "Suggested Phases section has no detail items"
154     return True
```

Returns `True` on pass; returns `"No 'Suggested Phases' section found"` or
`"Suggested Phases section has no detail items"` on fail.

---

## 4. CHECK-FUNCTION CONVENTION (exact contract for the new function)

### Module docstring states the contract verbatim (gates.py:14-21)

```python
14 All semantic check functions follow Callable[[str], bool | str] signature:
15   - Return True on pass
16   - Return an error string on failure
17
18 All checks are wrapped in try/except: exceptions return
19 (False, "check '{name}' crashed: {error}") per F-005.
20
21 NFR-PRD.2: All _check_* functions match Callable[[str], bool | str].
```

### Confirmed by two existing signatures

- `_check_verdict_field(content: str) -> bool | str:` (gates.py:36)
- `_check_no_placeholders(content: str) -> bool | str:` (gates.py:64)

(Also: `_check_parsed_request_fields` :91, `_check_research_notes_sections` :121,
`_check_suggested_phases_detail` :137, `_check_task_phases_present` :157,
`_check_b2_self_contained` :170, `_check_parallel_instructions` :190,
`_check_prd_template_sections` :232, `_check_qa_verdict` :247 — **all 10** use the
identical `(content: str) -> bool | str` signature.)

### Pattern body convention
- Single positional param named `content: str`.
- Return `True` (the literal, not just truthy) on PASS.
- Return a descriptive **error string** on FAIL.
- Do NOT raise — the `_safe_check` wrapper (gates.py:257-268) converts any
  exception to `f"check '{name}' crashed: {exc}"`.

### Model-level confirmation (`cli/pipeline/models.py:82-87`)

```python
82 @dataclass
83 class SemanticCheck:
84     """Pure Python check applied to file content. No LLM invocation."""
85
86     name: str
87     check_fn: Callable[[str], bool | str]
88     failure_message: str
```

### EXACT signature the new function MUST follow

```python
def _check_no_truncation_marker(content: str) -> bool | str:
    """..."""
    # return True on pass; return error string on fail; never raise
```

This matches `merged-solution.md`'s proposed `bool | str` contract (True on pass,
failure-string on fail). **Confirmed consistent with the existing convention.**

---

## 5. WIRING: how `_check_*` functions are registered/invoked

### Registration (declarative, per-gate)

`_check_*` functions are NOT auto-discovered or registry-scanned. Each is wired
**inline** into a gate's `semantic_checks=[...]` list inside the `GATE_CRITERIA`
dict (gates.py:303-514), wrapped by `_make_semantic_check(name, fn, failure_msg)`
(gates.py:271-281), which itself wraps the fn in `_safe_check` (gates.py:257-268).

Example wiring (research-notes, gates.py:334-345) — quoted in §1.

### Invocation site (executor.py:702-715)

The grep for call sites resolves to a single dispatch loop. **`gates.py` defines;
`executor.py` consumes** (R2 owns the executor — not deep-read here, only the
dispatch loop quoted for wiring evidence):

```python
702        # Run semantic checks
703        if gate.semantic_checks:
704            for check in gate.semantic_checks:
705                result = check.check_fn(content)
706                if result is not True:
707                    msg = result if isinstance(result, str) else check.failure_message
708                    self._diagnostics.record_gate_failure(
709                        step_id, msg, gate.enforcement_tier
710                    )
711                    self._logger.log_gate_result(step_id, False, msg)
712                    return False
```

`GATE_CRITERIA` is imported once: `from .gates import GATE_CRITERIA`
(executor.py:46) and looked up by step id at executor.py:473, 621, 832, 1019.
The gate-pass loop above (around 705) is the ONLY place `check.check_fn` is
called. Note `result is not True` (executor.py:706) — confirms the strict-`True`
return contract: any non-`True` value (including a string) is treated as failure.

### Is there a registry/dict of checks per mode?

No per-mode (STRICT/STANDARD/...) registry. `enforcement_tier` is a field ON each
`GateCriteria` (models.py:151), but it does NOT select which checks run — ALL
`semantic_checks` on a gate always run (executor.py:703-704). The tier is passed
through to `record_gate_failure(..., gate.enforcement_tier)` (executor.py:709) for
diagnostics/severity, not for check selection. So wiring a new check means adding
it to a specific gate's `semantic_checks` list — there is no mode-keyed table to
append to.

### CRITICAL — is `_check_no_truncation_marker` wired into a gate, or standalone?

**This is the ambiguous point. Evidence below; flagged for design (R5) resolution.**

**Evidence FOR "defined + unit-tested only, NOT wired" (least-invasive):**
- The track goal explicitly states: *"research-notes STRICT criteria and existing
  semantic checks MUST stay UNCHANGED."* The research-notes block (gates.py:330-346)
  is the natural home for a truncation check on research notes — but adding to its
  `semantic_checks` list **changes that block**, directly contradicting the goal.
- INV-002 (from the task brief): the fix must NOT add content-faking AND a
  genuinely thin doc SHOULD still HALT. The existing `min_lines=100` +
  `_check_research_notes_sections` already HALT thin docs. A truncation guard is
  additive insurance, not a replacement.
- merged-solution.md (per brief) calls it a *"cheap, harmless guard."* "Harmless"
  + "must stay unchanged" together imply: **define the helper, unit-test it, but do
  NOT mutate any STRICT `semantic_checks` list.**

**Evidence FOR "wired into a gate":**
- A guard that is defined but never invoked is dead code — it would never fire in
  the live pipeline. If the intent is to actually catch truncated research notes at
  runtime, it MUST be appended to `research-notes` → `semantic_checks`
  (gates.py:334-345), which mutates the "unchanged" block.

**Resolution / recommendation (flagged as AMBIGUOUS — defer to R5 design):**
The two requirements ("stay unchanged" vs "actually guard") are in tension. The
LEAST-invasive reading consistent with the literal "MUST stay UNCHANGED"
constraint is:
> **Define `_check_no_truncation_marker` as a module-level helper following the
> convention, add unit tests (R4), and do NOT add it to any existing STRICT gate's
> `semantic_checks` list.** Wiring is a SEPARATE, explicitly-authorized decision.

If the design (R5) determines the guard must fire at runtime, the only correct
wiring target is `research-notes` `semantic_checks` (gates.py:334-345) — and that
re-opens the "unchanged" constraint, which must be explicitly waived. **Do not
silently wire it.** Surface this conflict to the user/design before integration.

---

## 6. Best insertion point for the new function

**Recommended:** place `_check_no_truncation_marker` in **Layer 1 (Reusable
semantic checks)**, immediately **after `_check_no_placeholders` (ends gates.py:83)
and before the Layer-2 divider (gates.py:86)**.

Rationale:
- It is content-agnostic (a truncation marker can appear in any output), so it
  belongs with the reusable checks (`_check_verdict_field`, `_check_no_placeholders`)
  in Layer 1 (gates.py:31-83), NOT with PRD-specific Layer-2 checks (gates.py:86+).
- `_check_no_placeholders` (gates.py:64-83) is its closest sibling — both are pure
  string-marker scans returning `bool | str`. Sitting beside it keeps the
  "negative content guard" checks together.

**Concrete anchor:** insert a new blank line + function between line 83 (`return True`
closing `_check_no_placeholders`) and line 86 (the `# ----...` Layer-2 header).

If the function were research-notes-specific instead, the alternative anchor is
right after `_check_suggested_phases_detail` (gates.py:154), in Layer 2 — but
Layer 1 is preferred for a generic truncation guard.

---

## 7. Imports the new function needs

**Confirmed: NONE beyond what's already imported.**

Current imports (gates.py:24-29):

```python
24 from __future__ import annotations
25
26 import re
27 from typing import Callable
28
29 from superclaude.cli.pipeline.models import GateCriteria, SemanticCheck
```

- `re` (gates.py:26) is already available if the truncation marker is matched via
  regex (every sibling check uses `re`).
- Pure string ops (`in`, `.endswith`, `.rstrip`) need no import at all.
- The `bool | str` return annotation works at runtime because
  `from __future__ import annotations` (gates.py:24) is present (PEP 563
  string-annotations), so no `typing` additions are required.

**No new imports required.** Confirmed.

---

## Summary

- File is **514 lines**; BUILD_REQUEST line estimates were stale (off ~10-15 lines).
- research-notes STRICT gate is at **gates.py:330-346**: `min_lines=100`,
  `enforcement_tier="STRICT"`, invokes `_check_research_notes_sections` (7 required
  sections, gates.py:110-118/121-134) and `_check_suggested_phases_detail`
  (gates.py:137-154). This block MUST stay unchanged per the goal.
- **Check convention (verbatim, gates.py:14-21 + sigs at :36, :64):** all 10
  `_check_*` helpers are `def _check_x(content: str) -> bool | str:` → return
  literal `True` on pass, an **error string** on fail, never raise (the
  `_safe_check` wrapper at gates.py:257-268 catches exceptions). The new function
  must follow this exactly — confirmed consistent with merged-solution's `bool | str`.
- **Wiring:** checks are wired **inline** into each gate's `semantic_checks=[...]`
  in `GATE_CRITERIA` (gates.py:303-514) via `_make_semantic_check`
  (gates.py:271-281); executor dispatches them in one loop at executor.py:702-712
  (`result is not True` → fail). **No per-mode registry exists** — `enforcement_tier`
  is diagnostics-only, not check-selection.
- **AMBIGUITY FLAGGED:** "STRICT criteria stay UNCHANGED" vs "actually guard at
  runtime" are in tension. Least-invasive correct reading: **define the helper +
  unit-test it, do NOT add it to any STRICT gate's `semantic_checks`**. If runtime
  wiring is required, the only target is research-notes `semantic_checks`
  (gates.py:334-345), which re-opens the unchanged constraint — surface to design
  (R5), do not wire silently.
- **Insertion point:** Layer 1, between `_check_no_placeholders` (ends gates.py:83)
  and the Layer-2 divider (gates.py:86) — beside its closest sibling.
- **Imports:** none needed (`re` already imported at gates.py:26;
  `from __future__ import annotations` at :24 covers the `bool | str` annotation).

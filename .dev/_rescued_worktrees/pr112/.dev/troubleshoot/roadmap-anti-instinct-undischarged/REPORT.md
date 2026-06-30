---
status: success
tier_reached: 1
confidence: 0.90
escalation_reason: none
test_is_wrong: false
behavior_is_documented: false
hypothesis_count: 1
adversarial_invoked: false
fix_authorized: false
target: "roadmap pipeline halts at anti-instinct step on MultiModelSwarm roadmap (6 undischarged obligations)"
---

# REPORT — anti-instinct gate halt (MultiModelSwarm roadmap)

## Summary

All 6 reported "undischarged obligations" are **false positives**. The pipeline is correctly halting on a deterministic-gate failure, but the gate is being triggered by two distinct scanner bugs, not by real scaffolding the roadmap fails to discharge. Five of the six false positives come from a structural bug in `_split_into_phases` (post-milestone tail sections inherit the last milestone, so there is no "later milestone" available for discharge). The sixth comes from a meta-context detector that does not recognize parenthetical outcome/result clarifications such as `(no-op outcome)`. The remediate step is correctly skipped — it was never wired to handle anti-instinct findings — but the underlying scanner needs fixing so this gate stops blocking on documentation tails.

## Diagnosis (chosen hypothesis)

**Two independent scanner defects produced 6 false positives.** Confirmed by reading the audit output (`anti-instinct-audit.md:21-26`), the chosen merge roadmap (`roadmap.md`), and the scanner source.

### Root Cause A — tail-section attribution (5 of 6 findings)

`_split_into_phases` (`obligation_scanner.py:344-374`) splits the roadmap into phase sections using a milestone-pattern regex (`^(#{2,3})\s+((?:(?:Phase|Step|Stage|Milestone)\s+|M)\d+...)$`, line 351-354). Non-milestone H2 headings — `## Resource Requirements and Dependencies`, `## Risk Register`, `## Success Criteria...`, `## Decision Summary`, `## Timeline Estimates` — do not match this pattern. For the LAST matched section, `end = matches[i + 1].start() if i + 1 < len(matches) else len(content)` (line 370) extends it to end-of-document, so every tail section is absorbed into the last milestone (M9 here).

The cross-milestone discharge search (`scan_obligations` lines 304-315) then iterates `for j in range(i + 1, len(sections))` — and since M9 is `len(sections) - 1`, that loop body never executes. **Any scaffold term in the document tail is structurally undischargeable.** The tail sections legitimately describe scaffolding as dependencies, fallbacks, mitigations, or M1/M5-bound deliverables — not as M9 work needing discharge:

- `roadmap.md:519` (`Stub`) — External Dependencies table cell: "Stub transport (M1-bound) for tests" — fallback for an M1 dependency, not M9 scaffolding
- `roadmap.md:529` (`stub`) — Infrastructure Requirements: "deterministic stub transport for all CI/test runs" — production-policy statement
- `roadmap.md:541` (`Stub`) — Risk Register R-05 mitigation: "stub-tested (SC-002/SC-008)" — describes existing tests
- `roadmap.md:553` (`Stub`) — Risk Register R-17 mitigation: "Stub-transport + fixture directory layout finalized at M5" — references M5-bound work
- `roadmap.md:600` (`stub`) — Timeline Estimates table, M1 row: "stub transport (early bind)" — describes M1's deliverable, in a table that lists *all* milestones

### Root Cause B — `(no-op outcome)` parenthetical not recognized as meta-context (1 of 6 findings)

`roadmap.md:311` matches `no-op` inside an M6 deliverable cell:

> "Wave 2 re-runs over all `.raw`; existing successes re-write deterministically (no-op outcome)"

This is a descriptive clarification of an *idempotency property* — the outcome of a re-run is a no-op — not a scaffolding obligation. The meta-context detector (`_is_meta_context`, lines 505-532) has Layer 3b (`_PAREN_PHASE_LABEL_RE`, lines 96-101) which matches parenthetical phase labels like `(command scaffolding)` or `(Phase 2 mocking)`, but the regex only includes the lexemes `scaffold`/`mock`/`stub` inside the parenthetical — it does not match `no-op`, `placeholder`, `dummy`, `fake`, `temporary`, etc. So `(no-op outcome)` falls through every layer and is graded HIGH.

### Why the pipeline halts instead of routing to remediate

This is correct behavior. `remediate` (`gates.py:1439`, `remediate.py`) is wired to consume **deviation-analysis records** (`deviations_to_findings`, `remediate.py:361`) routed by severity (HIGH→BLOCKING etc.). The `remediate` step lives AFTER `anti-instinct → test-strategy → spec-fidelity → wiring-verification → deviation-analysis` in `ALL_GATES` (`gates.py:1426-1441`); the anti-instinct gate has no upstream channel into deviation-analysis routing. There is no LLM-driven remediation prompt for obligations either — the anti-instinct audit is purely deterministic (`_run_anti_instinct_audit`, `executor.py:734-845`) and retry does not help because attempt N produces byte-identical output.

## Evidence

- `anti-instinct-audit.md:1-11` — frontmatter shows `undischarged_obligations: 6`, `fingerprint_coverage: 0.88`, gate-failing
- `anti-instinct-audit.md:21-26` — the 6 flagged obligations and their attributed milestone/component
- `roadmap.md:311` — M6 deliverable row containing `(no-op outcome)` (true M6 attribution, false meta-context classification)
- `roadmap.md:476` — `## M9: sc-bare-review Migration & A/B Parity` starts; this is the last milestone H2
- `roadmap.md:507,533,556,579,596` — `## Resource Requirements...`, `## Risk Register`, `## Success Criteria...`, `## Decision Summary`, `## Timeline Estimates` — all H2 headings that do NOT match the milestone-pattern regex
- `roadmap.md:519,529,541,553,600` — the 5 tail-section lines flagged as undischarged M9 obligations
- `obligation_scanner.py:351-354` — phase-pattern regex (matches only milestone-shaped H2/H3)
- `obligation_scanner.py:369-370` — last-section `end = len(content)` causes tail absorption
- `obligation_scanner.py:304-315` — discharge search iterates only `range(i + 1, len(sections))`; cannot find discharges for the last section
- `obligation_scanner.py:96-101` — `_PAREN_PHASE_LABEL_RE` includes only scaffold/mock/stub lexemes, missing `no-op`/`placeholder`/`dummy`/`fake`/`temporary`
- `vocabulary.py:16-28` — `SCAFFOLD_TERMS` (11 terms); only 3 of them are recognized inside parentheticals
- `gates.py:1426-1441` — `ALL_GATES` order; anti-instinct (index 7) precedes remediate (index 12)
- `executor.py:734-845` — `_run_anti_instinct_audit` runs deterministically, no LLM, no retry-resolution path
- `remediate.py:361-433` — `deviations_to_findings` consumes deviation-analysis records, not obligation findings

## Proposed Fix

Three changes, in priority order. All in `src/superclaude/cli/roadmap/obligation_scanner.py`.

**1. Terminate the last milestone at the first known tail-section H2 (eliminates 5 of 6 false positives, plus all similar ones).**

Modify `_split_into_phases` so it knows about the template tail-section headings and uses them as end-markers for the last milestone — but does NOT itself create scannable sections for them (their content is not in scope for obligation scanning).

```python
# Add at module scope (mirroring gates._REQUIRED_H2_SECTIONS shape, but local
# to avoid importing from gates.py and forming a cycle):
_TAIL_SECTION_HEADINGS = frozenset({
    "resource requirements and dependencies",
    "risk register",
    "success criteria and validation approach",
    "decision summary",
    "timeline estimates",
})

def _split_into_phases(content: str) -> list[tuple[str, str, int]]:
    # ... existing match logic ...
    sections: list[tuple[str, str, int]] = []
    for i, m in enumerate(matches):
        phase_id = m.group(2).strip()
        start = m.end()
        # Next milestone match OR first tail-section H2, whichever comes first.
        next_milestone_start = matches[i + 1].start() if i + 1 < len(matches) else len(content)
        end = _find_tail_section_start(content, start, next_milestone_start)
        start_line = content[: m.start()].count("\n") + 1
        sections.append((phase_id, content[start:end], start_line))
    return sections

def _find_tail_section_start(content: str, search_start: int, hard_end: int) -> int:
    """Return the earlier of (next H2 whose text is a known tail-section) or hard_end."""
    for line_match in re.finditer(r"^##\s+(.+?)$", content[search_start:hard_end], re.MULTILINE):
        text = _normalize_heading(line_match.group(1))  # reuse helper or inline
        if text in _TAIL_SECTION_HEADINGS:
            return search_start + line_match.start()
    return hard_end
```

This is surgical: only milestone sections see scanning; tail sections (Risk Register, Decision Summary, Timeline Estimates, etc.) are excluded entirely. This prevents the entire CLASS of false positives where descriptive risk/dependency/timeline tables mention `stub`/`mock`/`no-op` for prior milestones.

**2. Extend `_PAREN_PHASE_LABEL_RE` to all scaffold lexemes (eliminates the M6 `(no-op outcome)` false positive and similar parentheticals).**

```python
# Current (lines 96-101) covers only scaffold/mock/stub. Replace with a
# pattern generated from SCAFFOLD_TERMS so adding a vocabulary term auto-
# updates the meta-context detector.

_SCAFFOLD_TERMS_INLINE = "|".join(
    t.strip(r"\b") for t in SCAFFOLD_TERMS
)
_PAREN_PHASE_LABEL_RE = re.compile(
    rf"\(\s*\w+(?:[\s-]\w+)*\s+(?:{_SCAFFOLD_TERMS_INLINE})\s*\)"
    rf"|"
    rf"\(\s*(?:{_SCAFFOLD_TERMS_INLINE})\s+\w+(?:[\s-]\w+)*\s*\)",
    re.IGNORECASE,
)
```

Catches `(no-op outcome)`, `(placeholder value)`, `(dummy input)`, `(temporary workaround)` etc. as meta-context → severity demoted to MEDIUM → excluded from `undischarged_count`.

**3. Add a fallback descriptor classifier (defense in depth — optional).**

Add a fourth meta-context layer for "outcome/result/behavior/property" descriptive contexts: when a scaffold term sits next to nouns like `outcome`, `result`, `behavior`, `property`, `effect`, treat it as descriptive rather than prescriptive. This is broader than Fix 2 and is the right long-term hardening, but Fix 2 alone resolves the immediate signature.

**On the question "route to remediate instead of halting":** do **not** change. The current halt-on-fail behavior is correct because:

1. The anti-instinct audit is deterministic; retry without input change produces the same output. The retry counter (`attempt 1/2`) in the executor's pipeline harness is for transient LLM/IO failures and is irrelevant here.
2. Routing into remediate would require either (a) an LLM-driven roadmap rewriter that adds discharge text, which is exactly the kind of "instinct" the gate is designed to prevent post-hoc, or (b) a human-in-loop step, which is what halting already provides.
3. Fix 1 + Fix 2 eliminate the false-positive class. After they ship, any future anti-instinct failure IS a true catch and the correct response is "halt and surface to the operator" — which is what already happens.

The reasonable adjacent improvement, not part of this fix: surface the failure message with a one-line classification ("5 of 6 in document-tail sections; consider audit") so an operator can quickly recognize tail-pollution patterns if Fix 1 misses a heading variant.

## Alternative Fixes Considered

None — Tier 1 produced a single converging diagnosis. The competing route ("downgrade anti-instinct from STRICT to STANDARD so non-empty undischarged is warning-only") was rejected because it papers over real catches once Fix 1 + Fix 2 are in: STRICT enforcement is what gives the gate its value.

## Risk + Rollback

- **Fix 1 risk**: A tail-section regex anchored on `_TAIL_SECTION_HEADINGS` is template-coupled. If the template renames "Risk Register" to "Risk Assessment", the early-termination fails open and tail content is re-scanned. Mitigation: borrow `_normalize_heading` (`gates.py:919-924`) so leading numbering ("1.", "5.2.") is tolerated, and add a fixture-based unit test that exercises every template heading variant. Same heading list is already enforced as required by `_template_sections_present` (`gates.py:927-1015`), so renames break BOTH gates simultaneously — they cannot drift independently.
- **Fix 2 risk**: Widening `_PAREN_PHASE_LABEL_RE` could mask real obligations buried inside parentheticals (e.g., `(temporary mock implementation)`). Likely-rare; the existing Layer 3a/3b shape already lets parenthetical labels through to MEDIUM, so this fix moves the threshold for ~10 more lexemes, not opens a new escape hatch.
- **Rollback**: both are isolated to `obligation_scanner.py`. Revert the two functions and the new module constant; no schema or gate changes required.
- **Post-fix verification**: re-run the roadmap pipeline against the same MultiModelSwarm spec. Expect `undischarged_obligations: 0` (or low single-digit with descriptive component names tied to actual M-numbered phases). Also re-run the existing obligation-scanner test suite to confirm no regression on the genuine-obligation fixtures.

## Grounding Gaps

- Wave 1.5 documentation grounding was performed lightly: no formal spec doc exists for the obligation scanner beyond `FR-MOD1.1`–`FR-MOD1.9` markers in the module docstrings. The fix proposals are grounded in code behavior + sibling test patterns, not in an external requirements doc.
- Did not exercise the proposed fix against the actual roadmap content; the reasoning that `_TAIL_SECTION_HEADINGS` would prevent each of the 5 tail-section false positives is by structural argument (each of the 5 lines lives after line 507, and `## Resource Requirements and Dependencies` is at line 507), not by running the patched scanner.

## Next Steps

- Re-invoke this command with `--fix` to authorize Tier 3 remediation chain (task-builder will produce an MDTM task implementing Fix 1 + Fix 2 with unit tests covering both classes of false positive).
- Or apply manually: edit `src/superclaude/cli/roadmap/obligation_scanner.py` per the two snippets above, run `uv run pytest tests/roadmap/test_obligation_scanner.py -v` to confirm regression-free, then re-run the roadmap pipeline.

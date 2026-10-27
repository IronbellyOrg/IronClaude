# Anti-Instinct #02: Implicit Obligation Tracking

> **Status**: Brainstorm / Backlog
> **Created**: 2026-03-17
> **Triggered by**: cli-portify roadmap bug -- Phase 2 "mocked steps" milestone never discharged by Phases 4-7
> **Target module**: `src/superclaude/cli/roadmap/`

---

## 1. Problem Statement

### The LLM Tendency

When an LLM generates a multi-phase roadmap, it frequently writes early-phase milestones that contain **scaffolding language**: "mocked steps", "skeleton executor", "placeholder dispatch", "stub implementation". Each of these phrases creates an **implicit obligation** -- a deferred commitment that some later phase must replace the scaffold with real implementation.

Humans track these obligations mentally ("I need to wire that up in Phase 4"). LLMs do not maintain a running ledger of deferred commitments. By the time the agent generates Phase 4-7 content, the Phase 2 scaffolding decision has fallen out of active attention. The context window contains the prompt for the current phase and possibly the extraction document, but not a structured record of "things earlier phases promised that you must now fulfill."

The result: **skeletons that never get filled in, mocks that never get replaced, stubs that become production code.**

### Why This Is Hard to Catch

1. **No single artifact is wrong.** Phase 2's roadmap correctly says "implement executor skeleton with mocked steps." That is a valid milestone. Phase 4's roadmap correctly says "implement step dispatch logic." That is also valid. The bug is in the *gap between them* -- Phase 4 never references that it must replace Phase 2's mocks.
2. **It is a cross-phase coherence failure.** Each phase passes its own gate checks (frontmatter valid, actionable content present, headings well-formed). The existing gate system in `src/superclaude/cli/roadmap/gates.py` validates per-step structural quality, not cross-step semantic coherence.
3. **The obligation is implicit, not explicit.** The word "mocked" implies a future replacement, but no explicit task item says "Phase N: replace Phase 2 mocks with real dispatch."

---

## 2. Evidence: The cli-portify Bug

### What Happened

During roadmap generation for the cli-portify feature:

- **Phase 2 milestone**: "Executor skeleton with mocked steps" -- the roadmap agent generated a milestone that explicitly described using mocks as a scaffolding strategy.
- **Phases 4-7**: Step implementations were generated as standalone components. The agent produced dispatch logic, step handlers, and integration code, but none of these phases contained an explicit task to **replace the Phase 2 mocks** or **wire the new implementations into the skeleton**.
- **Result**: The generated tasklist contained both the skeleton milestone (Phase 2) and the implementation milestones (Phases 4-7) as independent work items. An engineer following the tasklist would build the skeleton, then build the components, but never connect them -- because no task said "connect them."

### Root Cause

The roadmap pipeline generates phases sequentially (or in parallel groups). Each phase's prompt (`build_generate_prompt` in `src/superclaude/cli/roadmap/prompts.py`) includes the extraction document and the agent persona, but does **not** include a structured record of obligations created by earlier phases. The `execute_pipeline` function in `src/superclaude/cli/pipeline/executor.py` processes steps in order, passing each step's output to the next step's inputs where configured, but there is no mechanism to extract, accumulate, and inject obligation metadata across the pipeline.

### How Existing Gates Failed to Catch It

The `GENERATE_A_GATE` and `GENERATE_B_GATE` in `src/superclaude/cli/roadmap/gates.py` check:
- Required frontmatter fields present
- Minimum line count (100)
- Frontmatter values non-empty
- Has actionable content (numbered/bulleted lists)

None of these checks detect the pattern: "Phase N uses scaffolding language that creates an obligation no later phase discharges."

The `SPEC_FIDELITY_GATE` compares the spec against the roadmap for deviations, but it operates on the final merged roadmap, not on the internal coherence between phases. The spec might not mention mocks at all -- it just says "implement executor." So spec-fidelity sees no deviation.

---

## 3. Proposed Solutions

### Solution A: Post-Generation Obligation Scanner (Recommended -- Start Here)

**Approach**: A deterministic, regex-based post-generation pass that scans the merged roadmap for scaffolding terms and verifies each has a corresponding discharge task.

**Implementation**:

New module: `src/superclaude/cli/roadmap/obligation_scanner.py`

```python
"""Obligation scanner -- detects undischarged scaffolding obligations in roadmaps.

Scans roadmap content for scaffolding terms (mock, stub, skeleton, placeholder,
scaffold, temporary, hardcoded) that create implicit obligations, then verifies
each obligation has a corresponding discharge term (replace, wire, integrate,
connect, implement real, remove mock, swap) in a later phase.

Pure function: content in, findings out. No I/O.
"""

from __future__ import annotations

import re
from dataclasses import dataclass


# --- Obligation vocabulary ---

# Terms that CREATE an obligation (something deferred)
SCAFFOLD_TERMS = [
    r"\bmocked?\b",
    r"\bstub(?:bed|s)?\b",
    r"\bskeleton\b",
    r"\bplaceholder\b",
    r"\bscaffold(?:ing|ed)?\b",
    r"\btemporary\b",
    r"\bhardcoded\b",
    r"\bhardwired\b",
    r"\bno-?op\b",
    r"\bdummy\b",
    r"\bfake\b",
]

# Terms that DISCHARGE an obligation (something fulfilled)
DISCHARGE_TERMS = [
    r"\breplace\b",
    r"\bwire\s+(?:up|in|into)\b",
    r"\bintegrat(?:e|ing|ed)\b",
    r"\bconnect\b",
    r"\bswap\s+(?:out|in)\b",
    r"\bremove\s+(?:mock|stub|placeholder|scaffold)\b",
    r"\bimplement\s+real\b",
    r"\bfill\s+in\b",
    r"\bcomplete\s+(?:the\s+)?(?:skeleton|scaffold)\b",
]

# Compile patterns
_SCAFFOLD_RE = re.compile("|".join(SCAFFOLD_TERMS), re.IGNORECASE)
_DISCHARGE_RE = re.compile("|".join(DISCHARGE_TERMS), re.IGNORECASE)


@dataclass
class Obligation:
    """A detected scaffolding obligation."""
    phase: str           # e.g., "Phase 2", "2.3"
    term: str            # the matched scaffold term
    context: str         # surrounding sentence/line
    line_number: int
    discharged: bool     # True if a matching discharge was found in a later phase
    discharge_phase: str | None  # phase where discharge was found
    discharge_context: str | None


@dataclass
class ObligationReport:
    """Result of obligation scanning."""
    total_obligations: int
    discharged: int
    undischarged: int
    obligations: list[Obligation]

    @property
    def has_undischarged(self) -> bool:
        return self.undischarged > 0


def scan_obligations(content: str) -> ObligationReport:
    """Scan roadmap content for scaffolding obligations and discharge status.

    Algorithm:
    1. Parse content into phase-delimited sections (by H2/H3 headings
       containing "Phase" or numbered sections).
    2. For each section, find all scaffold terms.
    3. For each scaffold term found, search ALL subsequent sections
       for a discharge term that references the same component.
    4. Report undischarged obligations.

    Returns an ObligationReport with all findings.
    """
    sections = _split_into_phases(content)
    obligations: list[Obligation] = []

    for i, (phase_id, phase_content, start_line) in enumerate(sections):
        for match in _SCAFFOLD_RE.finditer(phase_content):
            term = match.group()
            context_line = _get_context_line(phase_content, match.start())
            abs_line = start_line + phase_content[:match.start()].count("\n")

            # Search later phases for discharge
            discharged = False
            discharge_phase = None
            discharge_context = None

            # Extract the component name near the scaffold term
            component = _extract_component_context(phase_content, match.start())

            for j in range(i + 1, len(sections)):
                later_phase_id, later_content, _ = sections[j]
                # Look for discharge terms that reference the same component
                if _has_discharge(later_content, component):
                    discharged = True
                    discharge_phase = later_phase_id
                    discharge_match = _DISCHARGE_RE.search(later_content)
                    if discharge_match:
                        discharge_context = _get_context_line(
                            later_content, discharge_match.start()
                        )
                    break

            obligations.append(Obligation(
                phase=phase_id,
                term=term,
                context=context_line,
                line_number=abs_line,
                discharged=discharged,
                discharge_phase=discharge_phase,
                discharge_context=discharge_context,
            ))

    undischarged_count = sum(1 for o in obligations if not o.discharged)
    return ObligationReport(
        total_obligations=len(obligations),
        discharged=len(obligations) - undischarged_count,
        undischarged=undischarged_count,
        obligations=obligations,
    )


def _split_into_phases(content: str) -> list[tuple[str, str, int]]:
    """Split content into (phase_id, text, start_line_number) tuples.

    Splits on H2/H3 headings that contain phase-like patterns:
    "## Phase 2", "### 2.3 Executor", "## Step 4", etc.
    """
    phase_pattern = re.compile(
        r"^(#{2,3})\s+((?:Phase|Step|Stage|Milestone)\s+\d+[\w.]*.*?)$",
        re.MULTILINE | re.IGNORECASE,
    )
    matches = list(phase_pattern.finditer(content))
    if not matches:
        # Fallback: treat whole content as one section
        return [("entire-document", content, 1)]

    sections: list[tuple[str, str, int]] = []
    for i, m in enumerate(matches):
        phase_id = m.group(2).strip()
        start = m.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(content)
        start_line = content[:m.start()].count("\n") + 1
        sections.append((phase_id, content[start:end], start_line))

    return sections


def _get_context_line(text: str, pos: int) -> str:
    """Extract the line containing position `pos`."""
    start = text.rfind("\n", 0, pos) + 1
    end = text.find("\n", pos)
    if end == -1:
        end = len(text)
    return text[start:end].strip()


def _extract_component_context(text: str, pos: int) -> str:
    """Extract likely component name near a scaffold term.

    Looks for capitalized words, quoted terms, or code-formatted
    terms within ~60 chars of the match position.
    """
    window_start = max(0, pos - 60)
    window_end = min(len(text), pos + 60)
    window = text[window_start:window_end]

    # Try to find backtick-delimited terms first
    code_terms = re.findall(r"`([^`]+)`", window)
    if code_terms:
        return code_terms[0].lower()

    # Try capitalized multi-word terms (e.g., "Executor Skeleton")
    cap_terms = re.findall(r"[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*", window)
    if cap_terms:
        return cap_terms[0].lower()

    # Fallback: the whole line context
    return _get_context_line(text, pos).lower()


def _has_discharge(content: str, component: str) -> bool:
    """Check if content contains a discharge term referencing the component."""
    if not component:
        # No component context -- just check for any discharge term
        return bool(_DISCHARGE_RE.search(content))

    # Check if content mentions both a discharge term AND the component
    has_discharge = bool(_DISCHARGE_RE.search(content))
    has_component = component.lower() in content.lower()
    return has_discharge and has_component
```

**Integration point**: Hook into the pipeline after the `merge` step completes, before `spec-fidelity`. Add a new semantic check to `MERGE_GATE` in `src/superclaude/cli/roadmap/gates.py`:

```python
def _no_undischarged_obligations(content: str) -> bool:
    """Verify all scaffolding obligations in early phases are discharged by later phases."""
    from .obligation_scanner import scan_obligations
    report = scan_obligations(content)
    return not report.has_undischarged

# Add to MERGE_GATE.semantic_checks:
SemanticCheck(
    name="no_undischarged_obligations",
    check_fn=_no_undischarged_obligations,
    failure_message="Undischarged scaffolding obligations detected: early-phase mocks/stubs/skeletons have no corresponding replace/integrate/wire task in later phases",
)
```

**How this catches the cli-portify bug**: The merged roadmap contains Phase 2 with "mocked steps" and Phases 4-7 without any discharge term ("replace mock", "wire into skeleton", "integrate with executor"). The scanner finds "mocked" in Phase 2, searches Phases 3-7 for a discharge referencing the same component, finds none, and reports an undischarged obligation. The `MERGE_GATE` fails with an actionable error message.

---

### Solution B: Deferred Commitment Ledger (Pipeline-Maintained State)

**Approach**: Maintain a structured JSON ledger that accumulates obligations as phases are generated. Inject the ledger into subsequent phase prompts so the LLM is aware of outstanding commitments.

**Implementation**:

New file created by the pipeline: `<output_dir>/obligation-ledger.json`

```json
{
  "schema_version": "1.0",
  "obligations": [
    {
      "id": "OBL-001",
      "source_phase": "Phase 2",
      "term": "mocked steps",
      "context": "Executor skeleton with mocked steps",
      "component": "executor",
      "status": "OPEN",
      "discharge_phase": null,
      "discharge_task": null
    }
  ]
}
```

**Pipeline changes** (in `src/superclaude/cli/roadmap/executor.py`):

1. After each `generate-*` step completes, run the obligation scanner on the output.
2. Append any new obligations to `obligation-ledger.json` in the output directory.
3. When building prompts for subsequent steps (`build_generate_prompt`, `build_merge_prompt`), inject the ledger as context:

```
## Outstanding Obligations

The following scaffolding commitments from earlier phases have NOT yet been
addressed. You MUST include explicit tasks to discharge each one:

| ID | Source Phase | Obligation | Component |
|----|-------------|------------|-----------|
| OBL-001 | Phase 2 | Replace mocked steps with real dispatch | executor |
```

4. After each subsequent step, re-scan to check if new content discharges any open obligations. Update ledger status to "DISCHARGED" with the phase and task that discharged it.

**Prompt injection point**: Modify `build_generate_prompt()` and `build_merge_prompt()` in `src/superclaude/cli/roadmap/prompts.py` to accept an optional `obligation_ledger: str | None` parameter. When non-None, append it to the prompt.

**Advantages over Solution A**:
- Preventive, not just detective. The LLM sees the obligations *while generating* later phases.
- Creates an auditable trail of what was promised and when it was fulfilled.

**Disadvantages**:
- More complex to implement (state management, JSON schema, prompt injection).
- Semi-deterministic: relies on the LLM actually reading and acting on the injected ledger.
- The obligation extraction from phase output requires either regex (imprecise) or an LLM call (expensive, non-deterministic).

---

### Solution C: Dual-Pass Validation with Obligation Extraction LLM Call

**Approach**: After the merge step, run a dedicated validation LLM call that receives the full roadmap and a structured prompt asking it to identify all scaffolding obligations and verify each is discharged.

**Implementation**: New step in the pipeline between `merge` and `spec-fidelity`:

```python
# In executor.py, add a new step:
Step(
    id="obligation-check",
    output_file=output_dir / "obligation-check.md",
    inputs=[output_dir / "roadmap-merged.md"],
    gate=OBLIGATION_CHECK_GATE,
    retry_limit=1,
)
```

New prompt builder:

```python
def build_obligation_check_prompt(merged_roadmap_path: Path) -> str:
    return (
        "You are a roadmap coherence analyst.\n\n"
        "Read the provided merged roadmap. Your task is to identify every instance "
        "where an early phase creates a scaffolding obligation (uses terms like "
        "'mock', 'stub', 'skeleton', 'placeholder', 'scaffold', 'temporary', "
        "'hardcoded', 'no-op', 'dummy', 'fake') and verify that a LATER phase "
        "contains an explicit task to discharge that obligation (uses terms like "
        "'replace', 'wire up', 'integrate', 'connect', 'swap out', 'remove mock', "
        "'implement real', 'fill in', 'complete skeleton').\n\n"
        "Your output MUST begin with YAML frontmatter:\n"
        "- total_obligations: (integer) count of scaffolding obligations found\n"
        "- discharged: (integer) count that have matching discharge tasks\n"
        "- undischarged: (integer) count with NO matching discharge task\n"
        "- coherence_pass: (boolean) true only if undischarged == 0\n\n"
        "After frontmatter, provide a table:\n"
        "| Obligation | Source Phase | Scaffold Term | Discharge Phase | Discharge Task | Status |\n"
        "For undischarged obligations, Discharge Phase and Task should be '[MISSING]'.\n\n"
        "Be thorough. Check every phase."
    )
```

**Advantages**:
- Can catch subtle obligations that regex misses (e.g., "defer X to later" without explicit scaffold vocabulary).
- Produces human-readable evidence.

**Disadvantages**:
- Non-deterministic (LLM may miss obligations or hallucinate them).
- Adds pipeline cost (one additional LLM call per run).
- Requires a new gate definition.

---

### Solution D: Hybrid -- Regex Scanner + LLM Fallback

**Approach**: Run Solution A (deterministic regex scanner) first. If it finds zero obligations (possible false negative -- the roadmap uses unusual vocabulary for scaffolding), run Solution C (LLM call) as a fallback. If Solution A finds obligations and all are discharged, skip the LLM call.

This gives deterministic catches for common patterns and LLM coverage for edge cases, while minimizing unnecessary LLM calls.

---

## 4. Recommended Implementation Plan

### Phase 1: Deterministic Scanner (Solution A)

**Priority**: High -- this is the minimum viable mitigation.

1. Create `src/superclaude/cli/roadmap/obligation_scanner.py` with the `scan_obligations()` function and vocabulary constants.
2. Add `_no_undischarged_obligations` semantic check to `MERGE_GATE` in `src/superclaude/cli/roadmap/gates.py`.
3. Write tests in `tests/roadmap/test_obligation_scanner.py` covering:
   - Roadmap with scaffolding in Phase 2 and discharge in Phase 4 (should pass)
   - Roadmap with scaffolding in Phase 2 and NO discharge (should fail -- the cli-portify case)
   - Roadmap with no scaffolding terms (should pass trivially)
   - Multiple obligations, some discharged and some not (should fail)
   - Edge case: scaffold term in a code block (should still detect)

**Files to create/modify**:
- `src/superclaude/cli/roadmap/obligation_scanner.py` (new)
- `src/superclaude/cli/roadmap/gates.py` (add semantic check to MERGE_GATE)
- `tests/roadmap/test_obligation_scanner.py` (new)

### Phase 2: Ledger Injection (Solution B)

**Priority**: Medium -- preventive measure for after Phase 1 proves the scanner works.

1. Define `ObligationLedger` JSON schema.
2. Add ledger accumulation logic to roadmap executor after generate steps.
3. Modify `build_generate_prompt()` and `build_merge_prompt()` to accept and inject ledger context.
4. Add ledger discharge tracking after each step.

**Files to create/modify**:
- `src/superclaude/cli/roadmap/obligation_ledger.py` (new)
- `src/superclaude/cli/roadmap/executor.py` (add ledger accumulation hooks)
- `src/superclaude/cli/roadmap/prompts.py` (add ledger injection to prompt builders)

### Phase 3: LLM Fallback (Solution C/D)

**Priority**: Low -- only if regex scanner proves insufficient in practice.

---

## 5. Vocabulary Management

The scaffold and discharge term lists are the critical data driving Solution A. They should be:

1. **Configurable**: Store in a YAML or Python constant that can be extended without code changes.
2. **Versioned**: Track additions/removals as the vocabulary evolves.
3. **Tested**: Each term should have a test case confirming it matches expected patterns.
4. **Bidirectional**: For each scaffold term, there should be at least one known discharge term that logically pairs with it:

| Scaffold Term | Expected Discharge Terms |
|---------------|------------------------|
| mock/mocked | replace mock, remove mock, swap out mock |
| stub/stubbed | replace stub, implement real, fill in |
| skeleton | complete skeleton, flesh out, fill in |
| placeholder | replace placeholder, implement real |
| scaffold/scaffolding | remove scaffolding, replace scaffold |
| temporary | replace temporary, make permanent |
| hardcoded | make configurable, parameterize, replace hardcoded |
| no-op | implement, add logic, replace no-op |
| dummy | replace dummy, implement real |
| fake | replace fake, use real |

---

## 6. How This Would Have Caught the cli-portify Bug

With Solution A in place:

1. The `merge` step produces `roadmap-merged.md` containing Phase 2: "Executor skeleton with **mocked** steps" and Phases 4-7 with standalone implementation milestones.
2. The `MERGE_GATE` runs `_no_undischarged_obligations` as a semantic check.
3. `scan_obligations()` finds "mocked" in Phase 2, extracts component context "executor" / "steps".
4. It searches Phases 3-7 for discharge terms referencing "executor" or "steps" -- finds none (the later phases describe implementations but never say "replace the Phase 2 mocks" or "wire into the skeleton").
5. The obligation is marked `discharged=False`.
6. `ObligationReport.has_undischarged` returns `True`.
7. The `MERGE_GATE` **fails** with message: *"Undischarged scaffolding obligations detected: early-phase mocks/stubs/skeletons have no corresponding replace/integrate/wire task in later phases"*.
8. The pipeline halts. The operator sees the failure, understands that the roadmap has a coherence gap, and either:
   - Re-runs the merge with explicit instructions to address the obligation, or
   - Manually adds the discharge task to the roadmap before proceeding.

**The tasklist is never generated with the gap. The bug is prevented, not discovered post-facto.**

---

## 7. Risks and Mitigations

| Risk | Severity | Mitigation |
|------|----------|-----------|
| False positives: scaffold terms used descriptively ("the test uses mocks") | MEDIUM | Add context-aware filtering: ignore terms inside code blocks, test descriptions, or after "test" keywords. Allow `# obligation-exempt` comment to suppress. |
| False negatives: unusual vocabulary ("defer this to later") | LOW | Solution D (LLM fallback) catches these. Solution A vocabulary can be extended over time. |
| Over-blocking: legitimate scaffolding strategies where mocks ARE the final implementation (e.g., test doubles) | MEDIUM | Add allowlist for known-legitimate scaffolding patterns. The scanner should check for explicit "this is the final form" markers. |
| Performance: scanning large roadmaps with many phases | LOW | Regex scanning is O(n*m) where n=phases, m=terms. Even a 10,000-line roadmap with 20 phases and 10 terms completes in <100ms. |

---

## 8. Related Anti-Instincts

This is part of a broader pattern of LLM attention/coherence failures in multi-step generation:

- **Anti-Instinct #01** (if it exists): [placeholder for cross-reference]
- **Scope creep in later phases**: The inverse problem -- later phases add scope that was not in the spec.
- **Requirement drift**: Early phases interpret a requirement one way, later phases interpret it differently.
- **Dangling cross-references**: Phase 3 says "see Phase 5 for details" but Phase 5 never mentions the topic.

The obligation scanner infrastructure (phase splitting, term matching, cross-phase reference checking) could be extended to catch these related patterns.

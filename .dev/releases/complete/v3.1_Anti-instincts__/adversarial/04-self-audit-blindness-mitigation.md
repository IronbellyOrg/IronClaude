# Anti-Instinct 04: Self-Audit Blindness — Programmatic Mitigation for Spec-Fidelity Gates

**Date**: 2026-03-17
**LLM Tendency**: Self-Audit Blindness / Completion Bias in Review
**Trigger Event**: cli-portify executor no-op bug (forensic report: `.dev/releases/backlog/fidelity-refactor/cli-portify-executor-noop-forensic-report.md`)
**Target Codebase**: `src/superclaude/cli/roadmap/` (roadmap pipeline gates and executor)
**Status**: Brainstorm — ready for debate/scoring

---

## 1. The LLM Tendency Being Mitigated

**Self-Audit Blindness**: An LLM cannot reliably audit its own output for omissions. The same attention dynamics that caused a requirement to be dropped during generation will also cause the requirement to be overlooked during review. This is not a random failure — it is a systematic one. Well-structured output creates a false signal of completeness that both the generating LLM and a reviewing LLM interpret as "nothing missing."

**Completion Bias in Review**: When an LLM reviews a well-formatted document with proper headings, numbered phases, and clear deliverables, it is biased toward confirming completeness. The structural quality of the output masks content gaps. A 10-phase roadmap with milestones and risk sections "looks complete" even when a critical dispatch design has been silently dropped.

**Why LLM-on-LLM review fails here**: The `SPEC_FIDELITY_GATE` uses a separate LLM invocation to compare spec against roadmap and classify deviations by severity. But the reviewing LLM shares the same tendency: it sees a well-structured roadmap, scans for obvious contradictions, and produces low severity counts. The Python gate deterministically enforces `high_severity_count == 0` — but the LLM generating those counts has the same blindspot. The deterministic enforcement is only as good as the LLM's classification.

---

## 2. The Evidence: cli-portify Three-Way Dispatch Bug

### What the spec defined

Three release specs (v2.24, v2.24.1, v2.25) all specified the same executor architecture:

- **Three-way dispatch**: `_run_programmatic_step()`, `_run_claude_step()`, `_run_convergence_step()`
- **`PROGRAMMATIC_RUNNERS` dictionary**: Maps step IDs to Python functions
- **Module dependency graph**: `executor.py --> steps/validate_config.py`, `executor.py --> steps/discover_components.py`, etc.
- **Integration test**: `test_programmatic_step_routing` — "Programmatic steps call Python functions, not Claude subprocesses"

### What the roadmap produced

The roadmap reduced the executor design to:
> "Implement executor: sequential execution only, `--dry-run`, `--resume <step-id>`, signal handling"

And at Milestone M2:
> "Sequential pipeline runs end-to-end with **mocked steps**"

The three-way dispatch, `PROGRAMMATIC_RUNNERS`, module dependency graph, and integration test were all silently dropped. The roadmap produced a plausible-looking executor phase that addressed infrastructure concerns (dry-run, resume, signals) while omitting the core wiring that makes steps execute real work.

### How the SPEC_FIDELITY_GATE failed

The gate infrastructure at `src/superclaude/cli/roadmap/gates.py:633-656` defines `SPEC_FIDELITY_GATE` with:
- Required frontmatter: `high_severity_count`, `medium_severity_count`, `low_severity_count`, `total_deviations`, `validation_complete`, `tasklist_ready`
- Semantic checks: `_high_severity_count_zero()` (deterministic) and `_tasklist_ready_consistent()` (deterministic)

The deterministic checks are sound — they correctly enforce that `high_severity_count == 0`. But the LLM that generates the fidelity report either:
1. Did not notice the three-way dispatch was missing (same blindspot as the generator), or
2. Noticed it but classified it as MEDIUM or LOW severity (completion bias — the roadmap "addresses" the executor, just not fully)

Either way, `high_severity_count` was set to 0 by the LLM, and the deterministic gate passed.

### Corruption propagation

The fidelity chain is: `Spec --> [SPEC_FIDELITY_GATE] --> Roadmap --> [TASKLIST_FIDELITY_GATE] --> Tasklist --> [no gate] --> Code`

Once Link 1 (spec-to-roadmap) passed with the omission, the corruption propagated cleanly:
- The tasklist faithfully reproduced the roadmap's already-incomplete executor description
- The code faithfully implemented the tasklist's already-incomplete tasks
- Every downstream artifact was "correct" relative to its parent — but the root was wrong

---

## 3. Design Principle: Deterministic Floor Under LLM Judgment

The core insight: **the mitigation must include programmatic (non-LLM) verification**. LLM-on-LLM review shares the same blindspots. The deterministic gate (`high_severity_count == 0`) is already the right pattern — it just needs to be extended so that the severity counts themselves have a deterministic floor, not just the threshold check.

The architecture should be:

```
Spec ──[Programmatic ID extraction]──> ID Manifest
                                            │
Roadmap ──[Programmatic ID scan]──> Coverage Set
                                            │
                              ID Manifest ∖ Coverage Set = Missing IDs
                                            │
                              Missing IDs ≠ {} ──> GATE FAIL (hard, no LLM override)
                                            │
                              Missing IDs = {} ──> Proceed to LLM fidelity check
```

The LLM fidelity check still runs for semantic depth (misinterpretation, insufficient detail, contradictions). But the programmatic check provides a **deterministic floor** that catches the class of bug that LLMs systematically miss: complete omissions of named requirements.

---

## 4. Proposed Solutions

### Solution 1: Programmatic Requirement ID Cross-Reference Gate (RECOMMENDED)

**What it does**: Extracts all formal requirement IDs (FR-NNN, NFR-NNN, SC-NNN) from the spec extraction output, scans the roadmap for references to each ID, and fails the gate if any spec IDs are absent from the roadmap.

**Implementation**:

```python
# New file: src/superclaude/cli/roadmap/id_crossref.py

import re
from pathlib import Path

# Patterns for formal requirement IDs
_ID_PATTERNS = [
    re.compile(r'\bFR-\d{3}\b'),
    re.compile(r'\bNFR-\d{3}\b'),
    re.compile(r'\bSC-\d{3}\b'),
]


def extract_requirement_ids(content: str) -> set[str]:
    """Extract all formal requirement IDs from document content.

    Returns set of strings like {'FR-001', 'FR-002', 'NFR-001', 'SC-001'}.
    """
    ids: set[str] = set()
    for pattern in _ID_PATTERNS:
        ids.update(pattern.findall(content))
    return ids


def compute_missing_ids(
    spec_content: str,
    roadmap_content: str,
) -> set[str]:
    """Compute spec requirement IDs missing from roadmap.

    Returns set of IDs present in spec but absent from roadmap.
    Empty set means full coverage.
    """
    spec_ids = extract_requirement_ids(spec_content)
    roadmap_ids = extract_requirement_ids(roadmap_content)
    return spec_ids - roadmap_ids


def format_missing_ids_report(missing: set[str]) -> str:
    """Format missing IDs into a human-readable gate failure message."""
    if not missing:
        return ""
    sorted_ids = sorted(missing)
    lines = [
        f"PROGRAMMATIC CROSS-REFERENCE FAILURE: {len(missing)} spec requirement(s) "
        f"not referenced in roadmap:",
    ]
    for id_ in sorted_ids:
        lines.append(f"  - {id_}: present in spec extraction, absent from roadmap")
    lines.append("")
    lines.append(
        "This is a deterministic check. These IDs appear in the spec extraction "
        "output but have zero mentions in the roadmap. The LLM fidelity check "
        "cannot override this result."
    )
    return "\n".join(lines)
```

**Gate integration** — two options:

*Option A: Pre-gate check in executor (simpler, recommended for v1)*

Modify `src/superclaude/cli/roadmap/executor.py` to run the cross-reference check after the spec-fidelity step produces its output but before the gate is evaluated. If missing IDs are found, inject them as HIGH severity deviations into the fidelity report frontmatter before the gate reads it. This sidesteps the `SemanticCheck(check_fn: Callable[[str], bool])` single-argument limitation.

```python
# In executor.py, after spec-fidelity step completes but before gate check:
from .id_crossref import compute_missing_ids, format_missing_ids_report

spec_extraction_content = (output_dir / "extraction.md").read_text()
roadmap_content = (output_dir / "roadmap.md").read_text()
missing = compute_missing_ids(spec_extraction_content, roadmap_content)

if missing:
    # Override the LLM's high_severity_count in the fidelity report
    fidelity_path = output_dir / "spec-fidelity.md"
    fidelity_content = fidelity_path.read_text()

    # Append programmatic findings to the report
    appendix = (
        "\n\n## Programmatic Cross-Reference Findings\n\n"
        + format_missing_ids_report(missing)
    )

    # Rewrite frontmatter to set high_severity_count >= len(missing)
    fidelity_content = _inject_high_severity_floor(
        fidelity_content, len(missing)
    )
    fidelity_path.write_text(fidelity_content + appendix)
    # Now the existing deterministic gate (_high_severity_count_zero)
    # will correctly fail
```

*Option B: Extended SemanticCheck with multi-file access (cleaner, requires model change)*

Extend `SemanticCheck` in `src/superclaude/cli/pipeline/models.py` to support a `context_files` parameter, allowing the check function to receive content from multiple pipeline artifacts. This is architecturally cleaner but requires modifying the shared pipeline model.

```python
# In pipeline/models.py:
@dataclass
class SemanticCheck:
    name: str
    check_fn: Callable[..., bool]  # (content, **context) -> bool
    failure_message: str
    context_files: list[str] | None = None  # relative artifact names

# In roadmap/gates.py:
def _spec_ids_covered(content: str, *, extraction: str = "", roadmap: str = "") -> bool:
    """Programmatic cross-reference: all spec IDs must appear in roadmap."""
    from .id_crossref import compute_missing_ids
    missing = compute_missing_ids(extraction, roadmap)
    return len(missing) == 0

SPEC_FIDELITY_GATE = GateCriteria(
    ...,
    semantic_checks=[
        ...,  # existing checks
        SemanticCheck(
            name="spec_ids_cross_reference",
            check_fn=_spec_ids_covered,
            failure_message="Spec requirement IDs missing from roadmap (programmatic check)",
            context_files=["extraction.md", "roadmap.md"],
        ),
    ],
)
```

**How it would have caught the cli-portify bug**: The spec extraction would have contained FR-NNN IDs for the three-way dispatch design, PROGRAMMATIC_RUNNERS, and the integration test. The roadmap mentioned none of these IDs. The set difference would have been non-empty. The gate would have failed deterministically, regardless of the LLM's severity classification.

**Limitations**:
- Only catches omissions of formally-tagged requirements (FR-NNN, NFR-NNN, SC-NNN)
- Does not verify semantic coverage — a roadmap could mention FR-007 in a throwaway sentence
- Requires that the spec extraction step preserves all IDs (if extraction drops IDs, the baseline is wrong)
- Does not catch requirements described only in prose without formal IDs

---

### Solution 2: Structural Fingerprint Extraction (Catches Prose Requirements)

**What it does**: Goes beyond formal IDs to extract "structural fingerprints" — function names, class names, data structure names, and design pattern names that appear in code fences or backtick-delimited spans in the spec. Verifies each fingerprint appears in the roadmap.

**Implementation**:

```python
# New file: src/superclaude/cli/roadmap/fingerprint.py

import re
from dataclasses import dataclass

@dataclass
class Fingerprint:
    """A named code-level entity from the spec."""
    text: str           # e.g., "_run_programmatic_step"
    category: str       # "function", "class", "variable", "test", "pattern"
    source_context: str # surrounding line for debugging


def extract_code_fingerprints(content: str) -> list[Fingerprint]:
    """Extract code-level identifiers from spec content.

    Sources:
    1. Backtick-delimited identifiers: `_run_programmatic_step()`
    2. Code-fenced blocks: function/class definitions
    3. Explicitly named patterns: "three-way dispatch"
    """
    fingerprints: list[Fingerprint] = []

    # 1. Backtick identifiers (most reliable)
    for match in re.finditer(r'`([a-zA-Z_]\w*(?:\(\))?)`', content):
        text = match.group(1).rstrip('()')
        if len(text) >= 4:  # skip trivial identifiers
            ctx_start = max(0, match.start() - 40)
            ctx_end = min(len(content), match.end() + 40)
            fingerprints.append(Fingerprint(
                text=text,
                category="identifier",
                source_context=content[ctx_start:ctx_end].replace('\n', ' '),
            ))

    # 2. Code block function/class definitions
    code_block_pat = re.compile(r'```(?:python)?\n(.*?)```', re.DOTALL)
    for block_match in code_block_pat.finditer(content):
        block = block_match.group(1)
        for def_match in re.finditer(r'(?:def|class)\s+(\w+)', block):
            fingerprints.append(Fingerprint(
                text=def_match.group(1),
                category="definition",
                source_context=def_match.group(0),
            ))

    # 3. ALL_CAPS constants (likely important data structures)
    for match in re.finditer(r'\b([A-Z][A-Z_]{3,})\b', content):
        text = match.group(1)
        # Filter out common non-specific constants
        if text not in {'TRUE', 'FALSE', 'NONE', 'TODO', 'NOTE', 'WARNING',
                        'HIGH', 'MEDIUM', 'LOW', 'YAML', 'JSON', 'STRICT',
                        'STANDARD', 'EXEMPT', 'LIGHT'}:
            fingerprints.append(Fingerprint(
                text=text,
                category="constant",
                source_context=content[max(0, match.start()-40):match.end()+40].replace('\n', ' '),
            ))

    # Deduplicate by text
    seen: set[str] = set()
    unique: list[Fingerprint] = []
    for fp in fingerprints:
        if fp.text not in seen:
            seen.add(fp.text)
            unique.append(fp)

    return unique


def check_fingerprint_coverage(
    spec_content: str,
    roadmap_content: str,
    min_coverage_ratio: float = 0.7,
) -> tuple[bool, list[Fingerprint]]:
    """Check that spec fingerprints appear in roadmap.

    Returns (passed, missing_fingerprints).
    Gate passes if coverage ratio >= min_coverage_ratio.

    The ratio threshold (default 0.7) accounts for the fact that not every
    backtick identifier in a spec is a hard requirement — some are examples,
    alternatives, or references to existing code. But a coverage ratio below
    70% strongly indicates wholesale omission of design detail.
    """
    spec_fps = extract_code_fingerprints(spec_content)
    if not spec_fps:
        return True, []  # No fingerprints to check

    roadmap_lower = roadmap_content.lower()
    missing: list[Fingerprint] = []
    for fp in spec_fps:
        if fp.text.lower() not in roadmap_lower:
            missing.append(fp)

    coverage = 1.0 - (len(missing) / len(spec_fps))
    return coverage >= min_coverage_ratio, missing
```

**How it would have caught the cli-portify bug**: The spec contained these code-level identifiers in backticks and code blocks:
- `_run_programmatic_step`
- `_run_claude_step`
- `_run_convergence_step`
- `PROGRAMMATIC_RUNNERS`
- `test_programmatic_step_routing`

None appeared in the roadmap. The fingerprint coverage ratio would have been far below 0.7, triggering the gate. This solution catches the bug even if the spec did not use formal FR-NNN tags for the dispatch design.

**Limitations**:
- False positives from identifiers mentioned as context/examples rather than requirements
- The `min_coverage_ratio` threshold requires tuning — too low misses omissions, too high causes false failures
- Sensitive to identifier naming conventions in different spec styles

---

### Solution 3: Negative-Space Prompting (Adversarial LLM Reframing)

**What it does**: Instead of asking the LLM "is the roadmap complete?" (which triggers completion bias), asks "what specific spec requirements are NOT covered by this roadmap?" — exploiting the finding that LLMs are better at finding problems when prompted to search for them than at confirming absence.

**Implementation**:

```python
# New prompt in src/superclaude/cli/roadmap/prompts.py

def build_negative_space_prompt(
    spec_file: Path,
    roadmap_path: Path,
) -> str:
    """Prompt for adversarial negative-space analysis.

    Reframes the fidelity check from "confirm completeness" to "find gaps."
    This exploits the asymmetry in LLM review: they are better at searching
    for specific problems than at confirming nothing is missing.
    """
    return (
        "You are a specification gap hunter. Your SOLE job is to find requirements "
        "that the roadmap FAILS to cover.\n\n"
        "You are NOT evaluating quality. You are NOT confirming what IS present. "
        "You are searching ONLY for what is MISSING.\n\n"
        "Read the specification and the roadmap. For each section of the specification, "
        "ask: 'Is there a corresponding plan in the roadmap for this?' If the answer is "
        "no or uncertain, report it.\n\n"
        "## Method\n\n"
        "1. List every concrete deliverable mentioned in the spec (functions, classes, "
        "data structures, tests, CLI commands, configuration options, dispatch patterns, "
        "integration points)\n"
        "2. For each deliverable, search the roadmap for explicit coverage\n"
        "3. Report ONLY the deliverables that have NO roadmap coverage\n\n"
        "## Anti-Bias Instructions\n\n"
        "- Do NOT assume a roadmap phase 'covers' something unless it explicitly names it\n"
        "- A roadmap phase titled 'Executor Implementation' does NOT automatically cover "
        "all executor-related spec requirements — check each one individually\n"
        "- 'Sequential execution' does NOT imply dispatch wiring exists\n"
        "- 'Mocked steps' does NOT imply real step integration is planned\n"
        "- If a spec requirement uses specific function names, those names must appear "
        "in the roadmap (or an explicit alternative)\n\n"
        "## Output\n\n"
        "Your output MUST begin with YAML frontmatter:\n"
        "- uncovered_count: (integer) number of spec deliverables with no roadmap coverage\n"
        "- total_checked: (integer) total spec deliverables examined\n"
        "- coverage_ratio: (float) covered / total\n\n"
        "After frontmatter, list each uncovered deliverable:\n"
        "- **Deliverable**: name/description\n"
        "- **Spec Location**: where it appears in the spec\n"
        "- **Spec Quote**: verbatim quote\n"
        "- **Roadmap Gap**: why no roadmap coverage was found\n\n"
        "If you find ZERO gaps, state that explicitly with justification for each "
        "spec section checked. An empty gap list must be earned, not assumed."
    ) + _OUTPUT_FORMAT_BLOCK
```

**Gate integration**: Add as a new pipeline step `negative-space` that runs in parallel with (or after) the existing `spec-fidelity` step. The gate checks `uncovered_count == 0` deterministically.

**How it would have caught the cli-portify bug**: The reframed prompt forces the LLM to enumerate spec deliverables and search for each one individually. The spec's `_run_programmatic_step()`, `PROGRAMMATIC_RUNNERS`, and `test_programmatic_step_routing` would each need to be individually located in the roadmap. The LLM would search for them, fail to find them, and report them as uncovered. The adversarial framing ("your SOLE job is to find gaps") counteracts completion bias.

**Limitations**:
- Still LLM-dependent — a sufficiently long spec could cause attention limits to drop items from the enumeration
- The anti-bias instructions help but cannot guarantee the LLM will not still rationalize coverage
- Does not provide the deterministic floor of Solutions 1-2
- Should be used as a complement to programmatic checks, not a replacement

---

### Solution 4: Hybrid — Programmatic IDs + Fingerprints + Adversarial Prompt (RECOMMENDED FULL SOLUTION)

**What it does**: Combines Solutions 1, 2, and 3 into a layered defense:

| Layer | Type | What it catches | Can be overridden by LLM? |
|-------|------|----------------|--------------------------|
| Layer 1: ID Cross-Reference | Deterministic | Missing FR-NNN, NFR-NNN, SC-NNN | No |
| Layer 2: Fingerprint Coverage | Deterministic | Missing code-level identifiers | No |
| Layer 3: Negative-Space Prompt | LLM (adversarial) | Semantic gaps, prose requirements | Yes (but reframing reduces blindspot) |
| Layer 4: Existing Fidelity Check | LLM (standard) | Nuanced deviations, misinterpretations | Yes |

**Implementation sequence**:

1. After roadmap generation, run Layers 1-2 programmatically (zero tokens, milliseconds)
2. If Layer 1 or 2 fails, gate fails immediately — no LLM invocation needed
3. If Layers 1-2 pass, run Layer 3 (negative-space prompt) as an additional pipeline step
4. If Layer 3 reports `uncovered_count > 0`, gate fails
5. If Layers 1-3 pass, run Layer 4 (existing spec-fidelity check) for semantic depth
6. Final gate: all four layers must pass

**Gate modification in `src/superclaude/cli/roadmap/gates.py`**:

```python
# Add to SPEC_FIDELITY_GATE semantic_checks:
SemanticCheck(
    name="programmatic_id_crossref",
    check_fn=_spec_ids_cross_reference,  # from id_crossref.py
    failure_message="Spec requirement IDs missing from roadmap (deterministic check)",
),
SemanticCheck(
    name="fingerprint_coverage",
    check_fn=_fingerprint_coverage_check,  # from fingerprint.py
    failure_message="Spec code-level identifiers missing from roadmap (deterministic check)",
),
```

**How it would have caught the cli-portify bug**:
- Layer 1 catches it if the spec used FR-NNN IDs for dispatch requirements
- Layer 2 catches it regardless, via the code-level fingerprints (`_run_programmatic_step`, `PROGRAMMATIC_RUNNERS`, etc.)
- Layer 3 catches it via adversarial enumeration of spec deliverables
- Any single layer succeeding would have blocked the roadmap from passing

**Limitations**:
- Most complex to implement (three new modules + prompt + gate wiring)
- Layer 2 threshold tuning requires empirical testing across multiple specs
- Layer 3 adds token cost (one additional LLM invocation)

---

### Solution 5: Extraction-Time Requirement Registry with Pipeline-Wide Tracking

**What it does**: Modifies the `extract` step to produce a machine-readable requirement registry (JSON) alongside the extraction markdown. Every downstream step must update the registry. Gates verify registry state transitions.

**Implementation**:

```python
# New file: src/superclaude/cli/pipeline/requirement_registry.py

import json
from dataclasses import dataclass, field, asdict
from enum import Enum
from pathlib import Path


class RequirementState(Enum):
    EXTRACTED = "EXTRACTED"      # Found in spec
    ROADMAPPED = "ROADMAPPED"   # Referenced in roadmap phase
    TASKED = "TASKED"            # Has corresponding tasklist task
    IMPLEMENTED = "IMPLEMENTED"  # Code exists
    VERIFIED = "VERIFIED"        # Tests pass


@dataclass
class RequirementEntry:
    id: str                      # FR-001, NFR-002, etc.
    description: str             # One-line summary
    state: RequirementState = RequirementState.EXTRACTED
    roadmap_phase: str = ""      # Which phase covers it
    tasklist_task: str = ""      # Which task implements it
    last_updated_by: str = ""    # Pipeline step that last touched it


@dataclass
class RequirementRegistry:
    entries: dict[str, RequirementEntry] = field(default_factory=dict)

    def add(self, entry: RequirementEntry) -> None:
        self.entries[entry.id] = entry

    def advance(self, id: str, new_state: RequirementState, **kwargs) -> None:
        if id not in self.entries:
            raise KeyError(f"Unknown requirement: {id}")
        entry = self.entries[id]
        entry.state = new_state
        for k, v in kwargs.items():
            if hasattr(entry, k):
                setattr(entry, k, v)

    def stuck_at(self, state: RequirementState) -> list[RequirementEntry]:
        """Return entries that haven't advanced past the given state."""
        return [e for e in self.entries.values() if e.state == state]

    def save(self, path: Path) -> None:
        data = {id: asdict(e) for id, e in self.entries.items()}
        path.write_text(json.dumps(data, indent=2))

    @classmethod
    def load(cls, path: Path) -> "RequirementRegistry":
        data = json.loads(path.read_text())
        registry = cls()
        for id, entry_data in data.items():
            entry_data["state"] = RequirementState(entry_data["state"])
            registry.entries[id] = RequirementEntry(**entry_data)
        return registry
```

**Gate check at spec-fidelity step**:

```python
def _registry_all_roadmapped(content: str) -> bool:
    """All extracted requirements must have advanced to ROADMAPPED state."""
    # Registry path would need to be discoverable from the gate context
    # This is the main architectural challenge with this approach
    ...
```

**How it would have caught the cli-portify bug**: The extraction step would have registered all dispatch-related requirements as EXTRACTED. After roadmap generation, the registry check would find them still at EXTRACTED (not ROADMAPPED), failing the gate.

**Limitations**:
- Requires the LLM to correctly populate the registry during extraction (if the LLM drops a requirement during extraction, it never enters the registry)
- Adds a stateful JSON artifact to what is currently a stateless document pipeline
- The registry update during roadmap generation is itself LLM-dependent (the LLM must be prompted to produce registry updates)
- Significant architectural change to the pipeline model

---

## 5. Implementation Roadmap

### Phase 1: Minimal Viable Mitigation (Solution 1 only)

**Files to create**:
- `src/superclaude/cli/roadmap/id_crossref.py` — ID extraction and cross-reference functions

**Files to modify**:
- `src/superclaude/cli/roadmap/executor.py` — Add pre-gate cross-reference check after spec-fidelity step
- `src/superclaude/cli/roadmap/gates.py` — Add `SemanticCheck` for ID cross-reference (if Option B chosen)

**Tests to add**:
- `tests/roadmap/test_id_crossref.py` — Unit tests for `extract_requirement_ids()`, `compute_missing_ids()`
- Extend `tests/roadmap/test_spec_fidelity.py` — Integration test verifying the cross-reference blocks when IDs are missing

**Estimated effort**: 1-2 tasks in a sprint tasklist

### Phase 2: Fingerprint Coverage (Solution 2)

**Files to create**:
- `src/superclaude/cli/roadmap/fingerprint.py` — Fingerprint extraction and coverage check

**Files to modify**:
- Same as Phase 1 (add fingerprint check alongside ID check)

**Estimated effort**: 1-2 tasks

### Phase 3: Negative-Space Prompt (Solution 3)

**Files to modify**:
- `src/superclaude/cli/roadmap/prompts.py` — Add `build_negative_space_prompt()`
- `src/superclaude/cli/roadmap/executor.py` — Add `negative-space` step to pipeline
- `src/superclaude/cli/roadmap/gates.py` — Add `NEGATIVE_SPACE_GATE` criteria

**Estimated effort**: 2-3 tasks (includes prompt tuning)

### Phase 4: Full Hybrid (Solution 4)

Combine Phases 1-3 with unified gate logic.

**Estimated effort**: 1 task (integration only, if Phases 1-3 are done)

---

## 6. How Each Solution Would Have Caught the Specific Bug

| Solution | Detection mechanism | Confidence |
|----------|-------------------|------------|
| 1. ID Cross-Reference | `FR-NNN` IDs for dispatch requirements missing from roadmap | HIGH (if spec used formal IDs) |
| 2. Fingerprint Coverage | `_run_programmatic_step`, `PROGRAMMATIC_RUNNERS`, `test_programmatic_step_routing` missing from roadmap | VERY HIGH (these identifiers definitely appeared in spec) |
| 3. Negative-Space Prompt | Adversarial enumeration would fail to find dispatch coverage in roadmap | HIGH (reframing counteracts completion bias) |
| 4. Hybrid (all three) | Any single layer catches it | VERY HIGH (defense in depth) |
| 5. Requirement Registry | Dispatch requirements stuck at EXTRACTED state | HIGH (if extraction captured them) |

The fingerprint approach (Solution 2) is the strongest single solution for this specific bug class because it operates on the exact code-level identifiers that the spec contained and the roadmap dropped. The ID cross-reference (Solution 1) is the most general and lowest-risk to implement. The recommended approach is the hybrid (Solution 4, implemented incrementally via Phases 1-3).

---

## 7. Codebase Integration Points

| File | Purpose | Change type |
|------|---------|-------------|
| `src/superclaude/cli/roadmap/id_crossref.py` | ID extraction and set-difference logic | New file |
| `src/superclaude/cli/roadmap/fingerprint.py` | Code-level fingerprint extraction | New file |
| `src/superclaude/cli/roadmap/prompts.py` | Negative-space prompt builder | New function |
| `src/superclaude/cli/roadmap/gates.py` | Add semantic checks to `SPEC_FIDELITY_GATE` | Modify existing |
| `src/superclaude/cli/roadmap/executor.py` | Pre-gate cross-reference check | Modify existing |
| `src/superclaude/cli/pipeline/models.py` | Extend `SemanticCheck` for multi-file access (Option B) | Modify existing (optional) |
| `tests/roadmap/test_id_crossref.py` | Unit tests for ID cross-reference | New file |
| `tests/roadmap/test_fingerprint.py` | Unit tests for fingerprint extraction | New file |
| `tests/roadmap/test_spec_fidelity.py` | Integration tests for combined gate | Extend existing |

---

## 8. Open Questions for Debate

1. **Should Layer 1 (ID cross-ref) be a hard gate or a warning?** If the extraction step itself drops an ID, the cross-reference would have a false baseline. A hard gate might block on extraction errors rather than roadmap omissions. Counter-argument: extraction errors should also be caught, and a false positive is safer than a false negative for this bug class.

2. **What is the right fingerprint coverage threshold?** 0.7 is proposed as a default, but this needs empirical validation across diverse specs. Specs with many illustrative examples (not requirements) would have lower coverage ratios even for correct roadmaps.

3. **Should the negative-space prompt run in parallel with or sequential to the existing fidelity check?** Parallel saves time but uses more tokens. Sequential allows the negative-space findings to be injected into the fidelity prompt as additional context.

4. **Should the `SemanticCheck` model be extended (Option B) or should the executor handle multi-file logic (Option A)?** Option A is simpler and keeps the model stable. Option B is architecturally cleaner and would benefit other gates that need multi-file access.

5. **How do we handle specs that don't use formal IDs?** Layer 1 provides no value for such specs. Layer 2 (fingerprints) is the fallback, but its threshold needs to be lenient enough to avoid false positives on loosely-structured specs. Should we make the ID cross-reference check conditional on the extraction reporting `> 0` formal IDs?

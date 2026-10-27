---
title: "Deterministic Spec-Fidelity Gate — Architecture Design"
version: "1.0.0"
status: draft
created: 2026-03-19
source: "/sc:design systematic deep codebase"
parent_spec: "deterministic-fidelity-gate-requirements.md"
parent_feature: v3.0_unified-audit-gating
---

# Deterministic Spec-Fidelity Gate — Architecture Design

## 1. Design Principles

1. **Structural-first**: ~70% of checks are deterministic Python; LLM handles only the residual semantic 30%.
2. **Immutable data flow**: Parsers produce frozen dataclasses; checkers return new `Finding` lists — no shared mutable state.
3. **Registry-centric gate**: The convergence gate reads the deviation registry, never raw scan output. `SPEC_FIDELITY_GATE` is excluded from convergence mode to prevent dual-authority conflicts (see Sec 5.3).
4. **Backward compatibility**: Pipeline steps 1–7 are untouched. The new system replaces step 8 (`spec-fidelity`) internals and adds post-step-8 orchestration.
5. **Minimal new files**: 5 new modules, 2 modified modules. No new CLI commands.

---

## 2. Module Map

### 2.1 New Modules

| Module | Location | Responsibility | FR |
|--------|----------|----------------|----|
| `spec_parser.py` | `cli/roadmap/spec_parser.py` | Parse spec + roadmap into structured `SpecData` / `RoadmapData` | FR-2 |
| `structural_checkers.py` | `cli/roadmap/structural_checkers.py` | 5 checker callables + registry + severity rule tables | FR-1, FR-3 |
| `semantic_layer.py` | `cli/roadmap/semantic_layer.py` | Chunked LLM residual pass + adversarial debate hook | FR-4, FR-5 |
| `deviation_registry.py` | `cli/roadmap/deviation_registry.py` | File-backed JSON registry with stable IDs, run metadata | FR-6, FR-10 |
| `convergence.py` | `cli/roadmap/convergence.py` | 3-run budget, monotonic progress (structural_high_count only), regression detection | FR-7, FR-8 |

### 2.2 Modified Modules

| Module | Change | FR |
|--------|--------|----|
| `executor.py` | Replace `spec-fidelity` step construction; add convergence loop after step 8 | FR-7 |
| `remediate_executor.py` | Add MorphLLM patch format + diff-size guard + fallback applicator | FR-9 |

### 2.3 Unchanged Modules

Steps 1–7 (`prompts.py` build_extract/generate/diff/debate/score/merge/test_strategy), `gates.py` (existing gate definitions), `fidelity.py` (Severity enum + FidelityDeviation — retained, extended), `spec_patch.py` (accepted deviation workflow), `models.py` (Finding dataclass — extended, not replaced).

---

## 3. Data Model

### 3.1 Spec Parser Output (`spec_parser.py`)

```python
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Literal

@dataclass(frozen=True)
class FunctionSignature:
    """Extracted Python function signature from fenced code block."""
    name: str
    params: list[str]           # parameter names (no types)
    return_type: str | None     # return annotation string or None
    source_section: str         # heading path where found, e.g. "3.1/FR-1"

@dataclass(frozen=True)
class RequirementID:
    """A requirement identifier extracted from spec text."""
    id: str                     # e.g. "FR-1.2", "NFR-3", "SC-1", "G-2", "D5"
    family: str                 # e.g. "FR", "NFR", "SC", "G", "D"
    source_section: str

@dataclass(frozen=True)
class FileManifestEntry:
    """A file path from a spec manifest table (Sec 4.1, 4.2, 4.3)."""
    path: str                   # e.g. "src/superclaude/cli/roadmap/spec_parser.py"
    description: str
    source_section: str

@dataclass(frozen=True)
class ThresholdExpression:
    """A numeric threshold from spec text, e.g. '< 5s', '>= 90%'."""
    raw: str                    # original text
    operator: str               # '<', '<=', '>', '>=', '=='
    value: float
    unit: str                   # 's', '%', 'KB', '' etc.
    source_section: str

@dataclass(frozen=True)
class EnumLiteral:
    """A Literal[...] enum value extracted from a fenced code block."""
    type_name: str              # e.g. "enforcement_tier"
    values: tuple[str, ...]     # e.g. ("STRICT", "STANDARD", "LIGHT", "EXEMPT")
    source_section: str

@dataclass(frozen=True)
class CrossReference:
    """A cross-section reference extracted from spec text."""
    from_section: str           # section containing the reference
    to_section: str             # section being referenced
    context: str                # surrounding text snippet

@dataclass(frozen=True)
class SpecSection:
    """A parsed top-level section of the spec."""
    heading: str                # e.g. "3. Functional Requirements"
    heading_path: str           # e.g. "3"
    level: int                  # heading level (2 = ##)
    content: str                # raw markdown content
    byte_size: int              # len(content.encode('utf-8'))

@dataclass(frozen=True)
class SpecData:
    """Complete structured extraction from a spec document."""
    frontmatter: dict[str, str]
    sections: tuple[SpecSection, ...]
    signatures: tuple[FunctionSignature, ...]
    requirement_ids: tuple[RequirementID, ...]
    file_manifest: tuple[FileManifestEntry, ...]
    thresholds: tuple[ThresholdExpression, ...]
    enum_literals: tuple[EnumLiteral, ...]
    cross_references: tuple[CrossReference, ...]

    # Derived lookup indexes (computed in __post_init__ of mutable builder)
    section_by_heading: dict[str, SpecSection] = field(default_factory=dict)
    ids_by_family: dict[str, frozenset[str]] = field(default_factory=dict)

@dataclass(frozen=True)
class RoadmapData:
    """Structured extraction from a roadmap document."""
    frontmatter: dict[str, str]
    sections: tuple[SpecSection, ...]      # reuse SpecSection for heading+content
    referenced_ids: frozenset[str]         # all FR-*, NFR-*, etc. found in text
    file_paths: frozenset[str]             # all file paths found in tasks
    function_names: frozenset[str]         # function/method names in task descriptions
    field_references: frozenset[str]       # dataclass field names referenced
    gate_params: frozenset[str]            # Step(...) parameter names referenced
```

**Parser functions** (all pure, no I/O beyond reading the two input files):

```python
def parse_spec(spec_path: Path) -> SpecData: ...
def parse_roadmap(roadmap_path: Path) -> RoadmapData: ...
```

**Implementation notes**:
- YAML frontmatter: `yaml.safe_load` on `---` delimited block (reuse `_extract_frontmatter` pattern from `spec_patch.py`)
- Markdown tables: regex split on `|` with header row detection
- Fenced code blocks: `^```python` … `^```\n` regex, then `ast.parse` for signatures
- Requirement IDs: `re.findall(r'(?:FR|NFR|SC|G|D)-?\d+(?:\.\d+)*', text)`
- `Literal[...]`: regex on `Literal\[([^\]]+)\]` within fenced blocks
- Thresholds: regex `(<=?|>=?|==)\s*([\d.]+)\s*(%|s|ms|KB|MB|)?`
- Cross-references: regex for `See (?:section |§)(\d+(?:\.\d+)*)` and `FR-\d+` in non-home sections
- Section splitting: `^## \d+\.` regex on spec; `^## ` on roadmap

---

### 3.2 Structural Finding Model

Extends the existing `Finding` dataclass in `models.py`:

```python
# Addition to models.py (or new field in Finding)
# No new class needed — Finding already has all required fields.
# New fields added:

@dataclass
class Finding:
    # ... existing fields ...
    rule_id: str = ""           # e.g. "SIG-MISSING-FUNC", "DM-PATH-PREFIX"
    spec_quote: str = ""        # verbatim spec text
    roadmap_quote: str = ""     # verbatim roadmap text or "[MISSING]"
    stable_id: str = ""         # hash-derived ID for registry dedup
```

**Stable ID derivation** (FR-6):

```python
import hashlib

def compute_stable_id(
    dimension: str,
    rule_id: str,
    spec_location: str,
    mismatch_type: str,
) -> str:
    """Deterministic finding ID from structural properties."""
    key = f"{dimension}:{rule_id}:{spec_location}:{mismatch_type}"
    return hashlib.sha256(key.encode()).hexdigest()[:16]
```

---

### 3.3 Severity Rule Table Schema

```python
from dataclasses import dataclass
from typing import Literal as Lit

SeverityLevel = Lit["HIGH", "MEDIUM", "LOW"]

@dataclass(frozen=True)
class SeverityRule:
    """One row in a checker's severity rule table."""
    dimension: str          # e.g. "signatures"
    mismatch_type: str      # e.g. "function_missing"
    severity: SeverityLevel
    description: str        # human-readable rule description

# Type alias for the rule table
SeverityRuleTable = dict[str, SeverityLevel]  # key: mismatch_type -> severity
```

---

## 4. Component Architecture

### 4.1 Spec Parser (`spec_parser.py`)

**Responsibility**: FR-2. Read spec and roadmap files, return `SpecData` and `RoadmapData`.

```
Input:  spec_path: Path, roadmap_path: Path
Output: SpecData, RoadmapData
I/O:    Reads 2 files (the only I/O in the entire checker pipeline)
```

**Key design decisions**:
- **Single point of file I/O**: All downstream components receive parsed data, never file paths.
- **Frozen dataclasses**: Parser output is immutable — checkers cannot accidentally mutate shared state (NFR-4).
- **Section-level chunking**: Each `SpecSection` tracks its byte size for prompt budgeting (NFR-3).
- **Reference graph**: `cross_references` enables supplementary section injection per checker.

**Section→Dimension mapping** (FR-5):

```python
# Static mapping: which spec sections feed which checker dimension
DIMENSION_SECTIONS: dict[str, list[str]] = {
    "signatures":  ["3"],           # Sec 3: Functional Requirements
    "data_models": ["4.1", "4.2", "4.3"],  # Sec 4: File manifests
    "gates":       ["3", "4"],      # FR + data model gates
    "cli":         ["5.1"],         # Sec 5: CLI options
    "nfrs":        ["6"],           # Sec 6: Non-functional requirements
}

def get_sections_for_dimension(
    dimension: str,
    spec: SpecData,
) -> list[SpecSection]:
    """Return primary + supplementary sections for a checker dimension.

    Primary sections come from DIMENSION_SECTIONS.
    Supplementary sections come from cross_references that link
    from primary sections to other sections.
    """
```

---

### 4.2 Structural Checkers (`structural_checkers.py`)

**Responsibility**: FR-1, FR-3. Five independent checker callables, each producing `list[Finding]`.

#### 4.2.1 Checker Protocol

```python
from typing import Protocol

class StructuralChecker(Protocol):
    """Protocol for all structural checkers."""

    dimension: str
    rules: SeverityRuleTable

    def check(self, spec: SpecData, roadmap: RoadmapData) -> list[Finding]:
        """Run deterministic checks, return findings with rule-based severity."""
        ...
```

#### 4.2.2 Five Checker Implementations

**1. SignatureChecker** (dimension: `"signatures"`, ~80% structural)

```python
class SignatureChecker:
    dimension = "signatures"
    rules: SeverityRuleTable = {
        "phantom_id":        "HIGH",    # Roadmap references ID not in spec
        "function_missing":  "HIGH",    # Spec function absent from roadmap
        "param_arity":       "MEDIUM",  # Parameter count mismatch
        "id_missing":        "MEDIUM",  # Spec ID not referenced in roadmap
    }

    def check(self, spec: SpecData, roadmap: RoadmapData) -> list[Finding]:
        findings = []
        # 1. Phantom ID check: roadmap IDs ⊄ spec IDs
        spec_ids = set()
        for req in spec.requirement_ids:
            spec_ids.add(req.id)
        phantom = roadmap.referenced_ids - spec_ids
        for pid in sorted(phantom):
            findings.append(Finding(
                dimension=self.dimension,
                rule_id="phantom_id",
                severity="HIGH",
                ...
            ))
        # 2. Missing function check
        # 3. Parameter arity check
        return findings
```

**2. DataModelChecker** (dimension: `"data_models"`, ~85% structural)

```python
rules = {
    "file_missing":      "HIGH",    # Required spec file missing from roadmap
    "path_prefix":       "HIGH",    # File path prefix mismatch
    "enum_uncovered":    "MEDIUM",  # Enum literal not covered
    "field_missing":     "MEDIUM",  # Dataclass field not referenced
}
```

**3. GateChecker** (dimension: `"gates"`, ~65% structural)

```python
rules = {
    "frontmatter_field": "HIGH",    # Required frontmatter field not covered
    "step_param":        "MEDIUM",  # Step parameter missing
    "ordering":          "MEDIUM",  # Ordering constraint violated
}
```

**4. CLIChecker** (dimension: `"cli"`, ~75% structural)

```python
rules = {
    "mode_uncovered":    "MEDIUM",  # Config mode not covered
    "default_mismatch":  "MEDIUM",  # Default value mismatch
}
```

**5. NFRChecker** (dimension: `"nfrs"`, ~55% structural)

```python
rules = {
    "threshold_contradicted": "HIGH",    # Numeric threshold contradicted
    "security_missing":       "HIGH",    # Security primitive missing
    "dependency_violated":    "HIGH",    # Dependency direction violated
    "coverage_mismatch":      "MEDIUM",  # Coverage threshold mismatch
}
```

#### 4.2.3 Checker Registry

```python
# Module-level registry
CHECKER_REGISTRY: dict[str, StructuralChecker] = {
    "signatures":  SignatureChecker(),
    "data_models": DataModelChecker(),
    "gates":       GateChecker(),
    "cli":         CLIChecker(),
    "nfrs":        NFRChecker(),
}

def run_all_checkers(
    spec: SpecData,
    roadmap: RoadmapData,
) -> list[Finding]:
    """Execute all checkers in parallel, merge findings."""
    from concurrent.futures import ThreadPoolExecutor, as_completed

    all_findings: list[Finding] = []
    with ThreadPoolExecutor(max_workers=5) as pool:
        futures = {
            pool.submit(checker.check, spec, roadmap): dim
            for dim, checker in CHECKER_REGISTRY.items()
        }
        for future in as_completed(futures):
            all_findings.extend(future.result())

    # Assign stable IDs
    for f in all_findings:
        f.stable_id = compute_stable_id(
            f.dimension, f.rule_id, f.location, f.rule_id
        )

    return all_findings
```

**Key design decisions**:
- **ThreadPoolExecutor** not ProcessPoolExecutor: checkers are CPU-light (string matching), not CPU-bound. Thread pool avoids serialization overhead.
- **No shared mutable state**: Each checker receives the same frozen `SpecData`/`RoadmapData` and returns its own list (NFR-4).
- **Rule tables in code**: `SeverityRuleTable` dicts are module-level constants, not prompt text (FR-3).

---

### 4.3 Residual Semantic Layer (`semantic_layer.py`)

**Responsibility**: FR-4, FR-5. LLM-based checking for the ~30% that structural checkers can't handle.

```python
@dataclass
class SemanticCheckRequest:
    """Input to the semantic LLM layer for one dimension."""
    dimension: str
    spec_sections: list[SpecSection]        # primary + supplementary
    roadmap_sections: list[SpecSection]
    structural_findings: list[Finding]      # context to avoid re-checking
    prior_findings_summary: str             # FR-10: run-to-run memory

def build_semantic_prompt(request: SemanticCheckRequest) -> str:
    """Build a chunked prompt for one semantic check.

    Enforces NFR-3: prompt size ≤ 30KB.
    Includes structural findings as "already checked" context.
    Includes prior findings summary (max 50 entries) for anchoring.
    """

def run_semantic_layer(
    spec: SpecData,
    roadmap: RoadmapData,
    structural_findings: list[Finding],
    registry: DeviationRegistry,
    config: PipelineConfig,
) -> list[Finding]:
    """Execute semantic checks per dimension, with adversarial debate for HIGHs.

    Flow:
    1. For each dimension, build SemanticCheckRequest with only uncovered aspects
    2. Spawn ClaudeProcess with chunked prompt (≤30KB)
    3. Parse LLM output into Finding list
    4. For any Finding with severity HIGH:
       a. Spawn adversarial debate (lightweight variant)
       b. Debate produces verdict: CONFIRM_HIGH | DOWNGRADE_TO_MEDIUM | DOWNGRADE_TO_LOW
       c. Apply verdict, record debate transcript reference
    5. Return all semantic findings with final severities
    """
```

**Adversarial debate integration** (FR-4):

```python
def validate_semantic_high(
    finding: Finding,
    spec_sections: list[SpecSection],
    roadmap_sections: list[SpecSection],
    config: PipelineConfig,
) -> tuple[str, str]:
    """Spawn adversarial debate for a semantic HIGH finding.

    Returns (verdict, transcript_reference):
        verdict: "CONFIRM_HIGH" | "DOWNGRADE_TO_MEDIUM" | "DOWNGRADE_TO_LOW"
        transcript_reference: path to debate output file

    **Protocol**: Single-round prosecutor/defender with automated deterministic judge.

    **Roles**:
    - Prosecutor (LLM): argues finding IS high severity
    - Defender (LLM): argues finding should be downgraded
    - Judge (Python): deterministic rubric scoring, no LLM call

    **Rubric weights**:
    - Evidence quality: 30%
    - Impact specificity: 25%
    - Logical coherence: 25%
    - Concession handling: 20%

    **Verdict thresholds**:
    - Prosecutor margin > 0.15 → CONFIRM_HIGH
    - Defender margin > 0.15 → DOWNGRADE_TO_{defender's recommendation}
    - Margin ≤ 0.15 (tiebreak) → CONFIRM_HIGH (conservative)

    **Token budget**: ~3,800 tokens per finding (cap: 5,000)
    **LLM calls**: 2 per finding (prosecutor + defender, parallelized)
    """
```

**Key design decisions**:
- **Per-dimension chunking**: Each semantic check receives only its relevant sections, not the full documents (NFR-3).
- **Structural findings as negative context**: The prompt says "the following have already been checked structurally — do NOT re-report them", preventing double-counting.
- **Lightweight debate for semantic HIGHs**: Uses a streamlined 2-agent format (not full `/sc:adversarial`), reducing token cost while preserving adversarial validation.
- **FR-8 regression debate**: Uses full `/sc:adversarial` for consolidated post-regression findings. Regression is only triggered by increases in `structural_high_count`; semantic fluctuations are logged as warnings but never trigger regression.

#### 4.3.1 Prompt Budget Enforcement (NFR-3)

**Budget**: `MAX_PROMPT_BYTES = 30,720` (30KB)

**Proportional allocation**:
| Component | Budget % | Bytes |
|-----------|----------|-------|
| Spec + roadmap sections | 60% | 18,432 |
| Structural findings context | 20% | 6,144 |
| Prior findings summary | 15% | 4,608 |
| Prompt template overhead | 5% | 1,536 |

**Overflow handling**: Tail-truncation on line boundaries with `[TRUNCATED: N bytes omitted]` marker.

**Enforcement**: `assert len(prompt.encode('utf-8')) <= MAX_PROMPT_BYTES` before LLM call.

**Edge cases**:
- Single section > 60% budget: truncated to fit
- Empty sections: valid (0 bytes allocated)
- Template exceeds 5% budget: `ValueError` raised at build time

---

### 4.4 Deviation Registry (`deviation_registry.py`)

**Responsibility**: FR-6, FR-10. Persistent finding store across runs.

#### 4.4.1 Registry Schema (JSON)

```json
{
  "schema_version": 1,
  "release_id": "v3.0_unified-audit-gating",
  "spec_hash": "abc123...",
  "runs": [
    {
      "run_number": 1,
      "timestamp": "2026-03-19T10:00:00Z",
      "spec_hash": "abc123...",
      "roadmap_hash": "def456...",
      "structural_count": 12,
      "semantic_count": 3,
      "high_count": 4,
      "medium_count": 8,
      "low_count": 3
    }
  ],
  "findings": {
    "a1b2c3d4e5f67890": {
      "stable_id": "a1b2c3d4e5f67890",
      "dimension": "signatures",
      "rule_id": "phantom_id",
      "severity": "HIGH",
      "mismatch_type": "phantom_id",
      "spec_location": "FR-1.2",
      "description": "Roadmap references FR-009 which does not exist in spec",
      "status": "ACTIVE",
      "first_seen_run": 1,
      "last_seen_run": 1,
      "debate_verdict": null,
      "debate_transcript": null
    }
  }
}
```

#### 4.4.2 Registry API

```python
@dataclass
class DeviationRegistry:
    """File-backed deviation registry with stable finding IDs."""

    path: Path                              # JSON file path
    release_id: str
    spec_hash: str
    runs: list[dict]                        # run metadata
    findings: dict[str, dict]               # stable_id -> finding dict

    @classmethod
    def load_or_create(cls, path: Path, release_id: str, spec_hash: str) -> DeviationRegistry:
        """Load existing registry or create fresh one.

        If spec_hash differs from saved → reset (new spec version, FR-6).
        """

    def begin_run(self, roadmap_hash: str) -> int:
        """Start a new run. Returns run_number."""

    def merge_findings(
        self,
        structural: list[Finding],
        semantic: list[Finding],
        run_number: int,
    ) -> None:
        """Merge current scan findings into registry.

        - New findings (stable_id not in registry): append with first_seen_run
        - Known findings (stable_id exists): update last_seen_run
        - Missing findings (in registry but not in current scan): mark FIXED
        """

    def get_active_highs(self) -> list[dict]:
        """Return findings with status=ACTIVE and severity=HIGH."""

    def get_active_high_count(self) -> int:
        """Count of active HIGH findings (gate evaluation)."""

    def get_prior_findings_summary(self, max_entries: int = 50) -> str:
        """Format prior findings for semantic layer prompt (FR-10).

        Returns formatted string: ID | severity | status | first_seen_run
        Truncates at max_entries, oldest first.
        """

    def update_finding_status(self, stable_id: str, status: str) -> None:
        """Update a finding's status (FIXED, FAILED, SKIPPED)."""

    def record_debate_verdict(
        self,
        stable_id: str,
        verdict: str,
        transcript_path: str,
    ) -> None:
        """Record adversarial debate outcome for a finding."""

    def save(self) -> None:
        """Atomic write: tmp + os.replace()."""
```

**Key design decisions**:
- **JSON format**: Simpler than YAML for programmatic access; no PyYAML dependency for this module.
- **Spec hash reset**: When `spec_hash` changes, all findings are archived and registry starts fresh (FR-6).
- **Stable IDs**: 16-char hex hash of `(dimension, rule_id, spec_location, mismatch_type)` — collision-resistant for the expected finding cardinality (<1000).
- **Status values**: `ACTIVE`, `FIXED`, `FAILED`, `SKIPPED` — matching existing `Finding.status` but with `ACTIVE` replacing `PENDING` for registry clarity.

> **Status compatibility note**: Both `ACTIVE` and `PENDING` are valid initial statuses in `VALID_FINDING_STATUSES`. `ACTIVE` is used by the deviation registry for findings not yet resolved; `PENDING` is the legacy pipeline default. Both represent "not yet resolved" and have equivalent semantics. The deviation registry uses `ACTIVE`; the existing pipeline steps 1–7 continue using `PENDING`.

---

### 4.5 Convergence Engine (`convergence.py`)

**Responsibility**: FR-7, FR-8. Budget enforcement, monotonic progress (`structural_high_count` only — semantic findings do not trigger regression), regression handling.

```python
@dataclass
class ConvergenceResult:
    """Outcome of a convergence-controlled fidelity run."""
    passed: bool
    run_count: int
    final_high_count: int
    progress_log: list[str]             # per-run "{run_n_highs} → {run_n+1_highs}"
    structural_progress_log: list[str]  # per-run "{structural_highs_n} → {structural_highs_n+1}"
    semantic_fluctuation_log: list[str] # per-run semantic HIGH count changes (informational)
    regression_detected: bool
    halt_reason: str | None             # None if passed

def execute_fidelity_with_convergence(
    spec_path: Path,
    roadmap_path: Path,
    registry_path: Path,
    config: RoadmapConfig,
    max_runs: int = 3,
) -> ConvergenceResult:
    """Run the full fidelity pipeline with convergence control.

    Algorithm:

    for run in 1..max_runs:
        1. Parse spec + roadmap (spec_parser)
        2. Run structural checkers (structural_checkers)
        3. Run semantic layer with structural findings as context
        4. Merge all findings into deviation registry
        5. Evaluate gate: active_high_count == 0?
           → YES: return PASS
        6. Check monotonic progress (structural findings only):
           → run_n+1.structural_high_count > run_n.structural_high_count? → REGRESSION
              (semantic fluctuations logged as warnings, never trigger regression)
              a. Spawn 3 parallel validation agents (FR-8)
              b. Merge/dedup results by stable ID
              c. Adversarial debate on each HIGH
              d. Update registry with debate verdicts
              e. Re-evaluate gate
        7. If budget remaining: run patch remediation (FR-9)
           → apply patches, re-run from step 1

    if budget exhausted:
        return HALT with diagnostic report
    """
```

#### 4.5.1 Regression Detection & Parallel Validation (FR-8)

```python
def handle_regression(
    registry: DeviationRegistry,
    spec_path: Path,
    roadmap_path: Path,
    registry_path: Path,
    config: RoadmapConfig,
) -> list[Finding]:
    """Spawn 3 parallel validation agents in temporary directories.

    Steps:
    1. Create 3 temporary directories with independent file copies
    2. In each temp directory, run full checker suite independently
    3. Collect all findings from all 3 agents
    4. Merge by stable_id: union of all findings
    5. Deduplicate: finding present in ≥2 agents = confirmed
    6. Write consolidated report to fidelity-regression-validation.md
    7. For each HIGH in consolidated: adversarial debate
    8. Update registry with debate verdicts
    9. Clean up temporary directories

    Returns merged+debated findings.
    """
```

**Temp directory management**:

```python
def _create_validation_dirs(
    spec_path: Path,
    roadmap_path: Path,
    registry_path: Path,
    count: int = 3,
) -> list[Path]:
    """Create temporary directories with independent file copies.

    Each directory gets its own copy of spec, roadmap, and registry.
    Uses tempfile.mkdtemp for OS-managed temp directory creation.
    """

def _cleanup_validation_dirs(dirs: list[Path]) -> None:
    """Remove temporary validation directories.

    Best-effort cleanup: logs warning on failure, does not raise.
    Registered as atexit fallback for crash safety.
    """
```

**Key design decisions**:
- **Temp directory isolation**: Each agent gets independent file copies in an OS-managed temp directory, preventing file contention (NFR-4). No git dependency required.
- **Union merge**: Any finding that appears in ANY agent's output is preserved. This is deliberately inclusive to avoid false negatives.
- **Confirmation threshold**: Findings in ≥2/3 agents are marked `confirmed=True` in the registry for auditability.
- **Counts as one run**: The entire regression flow (spawn + merge + debate) counts as a single run toward the 3-run budget.
- **Crash-safe cleanup**: `atexit.register(_cleanup_validation_dirs, dirs)` ensures temp directories are removed even on unexpected exits.

---

### 4.6 Patch-Based Remediation (Modified `remediate_executor.py`)

**Responsibility**: FR-9. Replace freeform file rewrites with structured patches.

#### 4.6.1 Patch Model

```python
@dataclass
class RemediationPatch:
    """MorphLLM-compatible lazy edit snippet."""
    target_file: str
    finding_id: str
    original_code: str              # relevant section from current file
    instruction: str                # human-readable edit instruction
    update_snippet: str             # new code with // ... existing code ... markers
    rationale: str                  # why this edit is needed

    def diff_size_ratio(self, file_content: str) -> float:
        """Compute changed_lines / total_file_lines."""
        total = len(file_content.splitlines())
        if total == 0:
            return 1.0
        # Count lines in update_snippet that differ from original_code
        original_lines = set(self.original_code.splitlines())
        update_lines = self.update_snippet.splitlines()
        changed = sum(1 for line in update_lines
                      if line.strip() != "// ... existing code ..."
                      and line not in original_lines)
        return changed / total
```

#### 4.6.2 Patch Application Pipeline

```python
def apply_patches(
    patches: list[RemediationPatch],
    config: PipelineConfig,
    registry: DeviationRegistry,
    diff_threshold: float = 0.30,
    allow_regeneration: bool = False,
) -> tuple[int, int]:  # (applied_count, rejected_count)
    """Apply patches sequentially per file with diff-size guard.

    Args:
        allow_regeneration: If True, patches exceeding diff_threshold are applied
            with a WARNING log instead of being rejected. Useful for convergence
            runs where regeneration of large sections is expected.

    Algorithm:
    1. Group patches by target_file
    2. For each file:
       a. Create snapshot (.pre-remediate)
       b. For each patch (sequential within file):
          i.   Compute diff_size_ratio
          ii.  If ratio > threshold:
               - If allow_regeneration=True: log WARNING, proceed with application
               - If allow_regeneration=False: reject, log, mark FAILED in registry
          iii. Apply patch (MorphLLM or fallback)
          iv.  Mark FIXED in registry
       c. If any patch failed: rollback file from snapshot
    3. Return (applied, rejected) counts
    """

def fallback_apply(patch: RemediationPatch, file_path: Path) -> bool:
    """Deterministic Python text replacement when MorphLLM unavailable.

    Uses original_code as anchor:
    1. Read file content
    2. Find original_code substring (exact match)
    3. If not found: try fuzzy match (strip whitespace differences)
    4. Replace with update_snippet (stripped of // ... markers)
    5. Write back atomically

    Returns True on success, False on anchor-not-found.
    """

def check_morphllm_available() -> bool:
    """Check if MorphLLM MCP server is active at runtime.

    Returns True if the morph-edit tool is available via MCP.
    """
```

**Key design decisions**:
- **Per-patch guard, not per-file**: Each individual patch is evaluated against the 30% threshold independently (resolved question #4).
- **Sequential within file**: Patches for the same file are applied one at a time to prevent ordering conflicts.
- **MorphLLM optional**: `check_morphllm_available()` probes for the MCP tool at runtime. If absent, the deterministic `fallback_apply()` is used.
- **Per-file rollback**: Existing `create_snapshots`/`restore_from_snapshots` mechanism is reused from `remediate_executor.py`.

---

## 5. Integration with Existing Pipeline

### 5.1 Pipeline Step Modification

The existing step 8 (`spec-fidelity`) becomes the entry point for the new convergence-controlled system. Steps 1–7 remain unchanged.

**Current** (in `executor.py::_build_steps`):
```python
Step(
    id="spec-fidelity",
    prompt=build_spec_fidelity_prompt(config.spec_file, merge_file),
    output_file=spec_fidelity_file,
    gate=SPEC_FIDELITY_GATE,
    ...
)
```

**Proposed** — Step 8 construction is conditional based on convergence mode:

```python
# In executor.py::_build_steps, step 8 construction:
if config.convergence_enabled:
    # Convergence mode: registry is authoritative (Design Principle #3)
    Step(
        id="spec-fidelity",
        prompt=None,  # No LLM fidelity prompt; convergence engine handles this
        output_file=spec_fidelity_file,
        gate=None,    # No SPEC_FIDELITY_GATE; registry evaluates pass/fail
    )
else:
    # Legacy mode: SPEC_FIDELITY_GATE is authoritative
    Step(
        id="spec-fidelity",
        prompt=build_spec_fidelity_prompt(config.spec_file, merge_file),
        output_file=spec_fidelity_file,
        gate=SPEC_FIDELITY_GATE,
    )
```

**Post-step orchestration** (in `executor.py::execute_roadmap`, after steps 1-7 complete):

```python
from .convergence import execute_fidelity_with_convergence

result = execute_fidelity_with_convergence(
    spec_path=config.spec_file,
    roadmap_path=out / "roadmap.md",
    registry_path=out / "deviation-registry.json",
    config=config,
    max_runs=3,
)

if not result.passed:
    # Write diagnostic report
    _write_convergence_halt_report(result, out)
    sys.exit(1)
```

### 5.2 State Integration

The deviation registry lives alongside `.roadmap-state.json`:

```
output_dir/
├── .roadmap-state.json          # existing pipeline state
├── deviation-registry.json      # NEW: persistent finding registry
├── spec-fidelity.md             # existing: LLM fidelity report (now generated per-run)
├── fidelity-regression-validation.md  # NEW: regression validation report
└── roadmap.md                   # existing: merged roadmap
```

**State file updates**: `.roadmap-state.json` gains a `fidelity_convergence` key:

```json
{
  "fidelity_convergence": {
    "status": "pass|fail|in_progress",
    "runs_completed": 2,
    "final_high_count": 0,
    "registry_path": "deviation-registry.json",
    "regression_detected": false
  }
}
```

### 5.3 Gate Authority Model

The system uses **mutual exclusion** to prevent dual-authority conflicts:

- **Convergence mode** (`convergence_enabled=True`): The `DeviationRegistry` is the sole authority for pass/fail evaluation. `SPEC_FIDELITY_GATE` is excluded from step 8. The `spec-fidelity.md` report is generated FROM registry state for human readability but is not gate-evaluated.

- **Legacy mode** (`convergence_enabled=False`): `SPEC_FIDELITY_GATE` is the sole authority, reading `high_severity_count` from `spec-fidelity.md` frontmatter. No `DeviationRegistry` is used.

**The two authorities never coexist in the same execution mode.** This eliminates the contradiction where the registry says PASS but the gate says FAIL (or vice versa).

---

## 6. Data Flow Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                    CONVERGENCE ENGINE (max 3 runs)              │
│                                                                 │
│  ┌──────────┐   ┌──────────────────┐   ┌───────────────────┐   │
│  │ spec.md  │──→│  SPEC PARSER     │──→│ SpecData (frozen)  │   │
│  │          │   │  (spec_parser.py) │   │ RoadmapData        │   │
│  │roadmap.md│──→│                  │   │ (frozen)           │   │
│  └──────────┘   └──────────────────┘   └─────────┬─────────┘   │
│                                                   │             │
│                        ┌──────────────────────────┤             │
│                        │                          │             │
│                        ▼                          ▼             │
│  ┌─────────────────────────────┐  ┌──────────────────────────┐  │
│  │   5 STRUCTURAL CHECKERS    │  │   RESIDUAL SEMANTIC      │  │
│  │   (parallel execution)     │  │   LAYER (chunked LLM)    │  │
│  │                            │  │                          │  │
│  │   Signatures ──→ findings  │  │   Receives structural    │  │
│  │   DataModels ──→ findings  │  │   findings as context    │  │
│  │   Gates ──────→ findings   │  │   ↓                      │  │
│  │   CLI ────────→ findings   │  │   Semantic findings      │  │
│  │   NFRs ───────→ findings   │  │   ↓                      │  │
│  │                            │  │   Any HIGH?              │  │
│  │   Rule-based severity      │  │   → adversarial debate   │  │
│  │   (no LLM)                 │  │   → verdict applied      │  │
│  └─────────┬──────────────────┘  └──────────┬───────────────┘  │
│            │                                 │                  │
│            └──────────┬──────────────────────┘                  │
│                       ▼                                         │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │                 DEVIATION REGISTRY                       │   │
│  │                 (deviation-registry.json)                │   │
│  │                                                          │   │
│  │  merge_findings(): new → append, known → update,        │   │
│  │                    missing → FIXED                       │   │
│  │                                                          │   │
│  │  Gate: active_high_count == 0?                           │   │
│  │    YES → PASS (exit convergence loop)                    │   │
│  │    NO + monotonic → REMEDIATE → next run                 │   │
│  │    NO + regression → PARALLEL VALIDATION (3 temp dirs)   │   │
│  │                      → merge → debate → update registry  │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │              PATCH REMEDIATION (if needed)               │   │
│  │                                                          │   │
│  │  Active HIGHs → generate MorphLLM patches                │   │
│  │  Per-patch: diff_size_ratio ≤ 30%?                       │   │
│  │    YES → apply (MorphLLM or fallback)                    │   │
│  │    NO  → reject, mark FAILED                             │   │
│  │  Per-file rollback on failure                            │   │
│  └──────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

---

## 7. Error Handling & Edge Cases

### 7.1 Parser Robustness

| Scenario | Handling |
|----------|----------|
| Spec has no frontmatter | Return empty `SpecData.frontmatter`; checkers operate on body only |
| Malformed fenced code block | Skip block, log warning; don't crash parser |
| Requirement ID regex false positive | Checkers verify against spec-defined ID set; false positives filtered |
| Roadmap uses different heading style | Roadmap parser accepts both `## Phase` and `## N. Section` |

### 7.2 Checker Edge Cases

| Scenario | Handling |
|----------|----------|
| Spec has 0 function signatures | SignatureChecker returns empty findings (not an error) |
| Roadmap references IDs with different casing | Normalize to uppercase before comparison |
| File path has OS-specific separators | Normalize to forward slashes before comparison |

### 7.3 Convergence Edge Cases

| Scenario | Handling |
|----------|----------|
| Run 1 already has 0 HIGHs | PASS immediately (1-run convergence) |
| All 3 validation agents fail | Treat as regression NOT resolved; halt with diagnostic |
| MorphLLM patch anchor not found | Fallback apply fails → finding marked FAILED → proceeds |
| Registry JSON corrupted | `load_or_create` catches `JSONDecodeError`, creates fresh registry |

---

## 8. Testing Strategy

### 8.1 Unit Tests

| Module | Test Focus | Example |
|--------|-----------|---------|
| `spec_parser.py` | Extraction accuracy | Parse known spec → assert exact SpecData fields |
| `structural_checkers.py` | Rule application | Inject known mismatches → assert correct severity |
| `deviation_registry.py` | State transitions | ACTIVE → FIXED when finding disappears across runs |
| `convergence.py` | Budget enforcement | 3 runs with no progress → halt |

### 8.2 Integration Tests

| Test | Validates |
|------|-----------|
| Same inputs twice → identical findings | NFR-1 (determinism) |
| 5 checkers run in parallel without race | NFR-4 (independence) |
| Prompt size never exceeds 30KB | NFR-3 |
| Steps 1-7 unmodified in output | NFR-7 (backward compat) |

### 8.3 Property-Based Tests

| Property | Generator |
|----------|-----------|
| Stable ID uniqueness | Random (dimension, rule_id, location, type) tuples |
| Registry merge idempotency | Merge same findings twice → no change |
| Severity rule determinism | Same mismatch → always same severity |

---

## 9. Migration Plan

### Phase 1: Foundation (No behavioral change)
1. `spec_parser.py` — parser with full test suite
2. `deviation_registry.py` — registry with persistence tests
3. Extend `Finding` dataclass with `rule_id`, `spec_quote`, `roadmap_quote`, `stable_id`

### Phase 2: Structural Checkers
4. `structural_checkers.py` — all 5 checkers with rule tables
5. Integration test: parse real v3.0 spec → run checkers → validate findings

### Phase 3: Semantic + Convergence
6. `semantic_layer.py` — chunked prompts + adversarial debate hook
7. `convergence.py` — budget, progress, regression handling

### Phase 4: Patch Remediation
8. Patch model + diff-size guard + fallback applicator in `remediate_executor.py`
9. MorphLLM integration (optional path)

### Phase 5: Integration
10. Wire into `executor.py` — replace step 8 internals
11. End-to-end test with real spec + roadmap
12. Remove old `build_spec_fidelity_prompt` from `prompts.py` (dead code after migration)

---

## 10. Non-Functional Requirement Compliance Matrix

| NFR | How Satisfied | Verified By |
|-----|---------------|-------------|
| NFR-1 (Determinism) | Structural checkers are pure functions; same inputs → same output | Run twice, diff findings |
| NFR-2 (Convergence ≤3) | `max_runs=3` hard limit in convergence engine | Run counter + halt test |
| NFR-3 (Prompt ≤30KB) | Section-level chunking; byte_size tracked per section; proportional budget allocation (Sec 4.3.1) | Assert before LLM call; `MAX_PROMPT_BYTES` enforcement |
| NFR-4 (Checker independence) | Frozen dataclasses; ThreadPoolExecutor; no shared state | Parallel execution test |
| NFR-5 (Edit safety ≤30%) | Per-patch `diff_size_ratio()` with configurable threshold | Patch rejection test |
| NFR-6 (Traceability) | Every finding has `rule_id` or `debate_verdict` + transcript | Audit log assertion |
| NFR-7 (Backward compat) | Steps 1-7 untouched; new code is additive, not modifying | Integration test |

---

## Appendix A: File Sizes & Token Estimates

| New Module | Estimated LOC | Estimated Tokens |
|-----------|---------------|------------------|
| `spec_parser.py` | 350-450 | ~3,500 |
| `structural_checkers.py` | 400-500 | ~4,000 |
| `semantic_layer.py` | 200-250 | ~2,000 |
| `deviation_registry.py` | 250-300 | ~2,500 |
| `convergence.py` | 300-400 | ~3,000 |
| **Total new code** | **1,500-1,900** | **~15,000** |
| Modified `executor.py` | +50-80 lines | ~500 |
| Modified `remediate_executor.py` | +150-200 lines | ~1,500 |

## Appendix B: Dependency Graph

```
spec_parser.py          ← depends on: stdlib only (ast, re, yaml)
structural_checkers.py  ← depends on: spec_parser, models (Finding)
semantic_layer.py       ← depends on: spec_parser, models, pipeline.process (ClaudeProcess)
deviation_registry.py   ← depends on: stdlib only (json, hashlib)
convergence.py          ← depends on: ALL above modules + executor (for pipeline integration)
```

No circular dependencies. `convergence.py` is the top-level orchestrator; all other modules are leaf or mid-level.

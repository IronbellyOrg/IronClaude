# Anti-Instincts Gate -- Unified Specification

<!-- Source: Merge (new content bridging V2+V5) -->

> **Status**: Design Spec -- Ready for Implementation
> **Created**: 2026-03-17
> **Protocol**: sc:adversarial Step 5 (Merge Execution)
> **Co-bases**: V2 (7.60) + V5 (7.55)
> **Cherry-picks**: V4-2 (Fingerprints), V1-C (Spec Structural Audit), V1-D+V5-2 (Prompt Constraint)
> **Target module**: `src/superclaude/cli/roadmap/`
> **Pipeline latency added**: <1s (all checks are pure Python)
> **LLM calls added**: 0

---

## 1. Problem Statement

<!-- Source: Merge (new content bridging V2+V5) -->

LLMs exhibit several correlated tendencies when generating multi-phase roadmaps from specifications. These tendencies cause systematic omission of integration wiring, undischarged scaffolding obligations, and dropped code-level requirements -- even when the output passes all existing format and fidelity gates.

The Anti-Instincts Gate is a unified deterministic defense layer that addresses four failure modes simultaneously:

| Failure Mode | Detection Module | Source |
|---|---|---|
| Undischarged scaffolding (mocks/stubs never replaced) | `obligation_scanner.py` | V2-A |
| Missing integration wiring (dispatch tables, registries never populated) | `integration_contracts.py` | V5-1 |
| Code-level identifier omissions (function names, constants dropped) | `fingerprint.py` | V4-2 |
| Extraction-stage requirement loss (upstream guard) | `spec_structural_audit.py` | V1-C |

Additionally, a prompt-level prevention layer reduces generation-time omissions:

| Prevention Layer | Target | Source |
|---|---|---|
| Integration enumeration block in generate prompt | `prompts.py` | V1-D + V5-2 |
| Integration wiring dimension in spec-fidelity prompt | `prompts.py` | V5-2 |

---

## 2. Evidence: The cli-portify Bug

<!-- Source: Merge (new content bridging V2+V5) -->

### What the spec defined

Three release specs (v2.24, v2.24.1, v2.25) specified:

- **Three-way dispatch**: `_run_programmatic_step()`, `_run_claude_step()`, `_run_convergence_step()`
- **`PROGRAMMATIC_RUNNERS` dictionary**: Maps step IDs to Python functions
- **Module dependency graph**: `executor.py --> steps/validate_config.py`, etc.
- **Integration test**: `test_programmatic_step_routing`

### What the roadmap produced

The roadmap reduced the executor to: "Implement executor: sequential execution only, `--dry-run`, `--resume <step-id>`, signal handling" with milestone M2: "Sequential pipeline runs end-to-end with **mocked steps**."

Zero mentions of `PROGRAMMATIC_RUNNERS`, three-way dispatch, or the `executor.py --> steps/*.py` import chain.

### How existing gates failed

The `SPEC_FIDELITY_GATE` enforces `high_severity_count == 0` deterministically, but the LLM generating the severity counts shared the same blindspot as the generator. The deterministic enforcement was sound; the LLM input to that gate was wrong.

### How each module in this spec would have caught it

| Module | Detection mechanism | Confidence |
|---|---|---|
| `obligation_scanner.py` | "mocked steps" in Phase 2 with no discharge in later phases | 85% |
| `integration_contracts.py` | `PROGRAMMATIC_RUNNERS` dispatch pattern with no wiring task | 90% |
| `fingerprint.py` | `_run_programmatic_step`, `PROGRAMMATIC_RUNNERS`, `test_programmatic_step_routing` absent from roadmap | 95% |
| `spec_structural_audit.py` | Pseudocode block + `PROGRAMMATIC_RUNNERS` registry + `def _run_*` signatures inflate structural count beyond extraction's requirement count | 85% |

---

## 3. Architecture

<!-- Source: Merge (new content bridging V2+V5) -->

```
Spec ──[V1-C: Structural audit]──> Extraction validated
                                         |
                                    [V1-D+V5-2: Prompt constraint]
                                         |
                              LLM generates roadmap
                                         |
                                    Merge step
                                         |
                          +--------------+--------------+
                          |              |              |
                    [V2-A: Obligation    [V5-1: Contract   [V4-2: Fingerprint
                     scanner]            extractor]         coverage]
                          |              |              |
                          +--------------+--------------+
                                         |
                              ANTI_INSTINCT_GATE (STRICT)
                                         |
                                    GATE FAIL / Proceed to spec-fidelity
```

**Pipeline position**: The three post-merge checks run as a single non-LLM step between `merge` and `test-strategy` in the pipeline. The structural audit runs between `extract` and `generate` as an executor-level hook.

**Key design property**: All four detection modules are pure Python with zero LLM calls. This is deliberate -- LLM-on-LLM review shares the same blindspots that caused the original bug. The deterministic floor cannot be bypassed by completion bias.

---

## 4. Module 1: Obligation Scanner

<!-- Source: V2-A (obligation scanner) -->

### Concept

A deterministic, regex-based post-generation pass that scans the merged roadmap for scaffolding terms and verifies each has a corresponding discharge task in a later phase. Catches the failure mode where early phases use "mocked", "stub", "skeleton", "placeholder" language that creates implicit obligations that later phases never fulfill.

### Detection Axis

V2-A's obligation scanner detects a fundamentally different failure mode than omission-based approaches. Rather than checking whether a requirement is present, it checks whether deferred commitments are fulfilled. This catches bugs where the requirement IS mentioned (as scaffolding) but the follow-through is missing.

### Implementation

**File**: `src/superclaude/cli/roadmap/obligation_scanner.py` (new, ~200 LOC)

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

            # Extract the component name near the scaffold term
            component = _extract_component_context(phase_content, match.start())

            # Search later phases for discharge
            discharged = False
            discharge_phase = None
            discharge_context = None

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

### Vocabulary Management

<!-- Source: V2-A (obligation scanner) -->

The scaffold and discharge term lists are the critical data. Each scaffold term has at least one known discharge pairing:

| Scaffold Term | Expected Discharge Terms |
|---|---|
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

### False Positive Mitigation

<!-- Source: V2-A (obligation scanner), adapted per refactor-plan Section 6 Weakness 1 -->

- Component context extraction uses a 60-char window to associate scaffold terms with nearby component names. This reduces false positives from "the test uses mocks" because test description scaffold terms will not share component context with phase milestone scaffold terms.
- Scaffold terms inside code blocks (backtick-fenced) are treated as potential false positives and flagged at MEDIUM severity rather than failing the gate.
- An `# obligation-exempt` comment mechanism is available for legitimate scaffolding strategies where mocks ARE the final implementation (e.g., test doubles).
- Phase 1 enforcement: STRICT on undischarged obligations, with the component-context filter active.

---

## 5. Module 2: Integration Contract Extractor

<!-- Source: V5-1 (integration contract extractor) -->

### Concept

A deterministic pre-validation step that extracts "integration contracts" from the spec and verifies each has a corresponding explicit task in the roadmap. An integration contract is any place where a data structure maps identifiers to callables, a constructor accepts injectable dependencies, an explicit wiring step is described, or a lookup/dispatch mechanism is defined.

### Detection Axis

V5-1 is mechanism-aware. It does not just detect missing identifiers but verifies the roadmap contains explicit wiring tasks for specific integration mechanisms. The key insight: "implementing components" is necessary but not sufficient. The wiring task itself must be explicit. Building a class does not register it in a dispatch table.

### Implementation

**File**: `src/superclaude/cli/roadmap/integration_contracts.py` (new, ~250 LOC)

```python
"""Integration contract extraction and verification.

Extracts non-obvious integration points from spec text and verifies
each has an explicit corresponding task in the roadmap. Catches the
"pattern-matching trap" where LLMs assume standard skeleton->implement
phasing covers custom dispatch/wiring mechanisms.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field


# --- Pattern definitions for integration contract detection ---
# Expanded to cover all 7 categories from the integration mechanism taxonomy.

DISPATCH_PATTERNS = [
    # Category 1: Dict dispatch tables
    re.compile(
        r'\b(?:dispatch[_\s]?table|RUNNERS|_RUNNERS|HANDLERS|'
        r'DISPATCH|routing[_\s]?table|command[_\s]?map|step[_\s]?map|'
        r'plugin[_\s]?registry)\b',
        re.IGNORECASE,
    ),
    # Category 2: Plugin registry / explicit wiring
    re.compile(
        r'\b(?:populate|register|wire|inject|bind|map|route)\s+'
        r'(?:the\s+|all\s+|each\s+)?'
        r'(?:implementations?|runners?|handlers?|plugins?|steps?|commands?)\b',
        re.IGNORECASE,
    ),
    # Category 3: Callback injection / constructor injection
    re.compile(
        r'\b(?:accepts?|takes?|requires?|expects?)\s+(?:a\s+)?'
        r'(?:Callable|Protocol|ABC|Interface|Factory|Provider|Registry)\b',
        re.IGNORECASE,
    ),
    # Category 3 (continued): Type annotations for dispatch
    re.compile(
        r'\b(?:Dict|Mapping|dict)\s*\[\s*str\s*,\s*(?:Callable|Awaitable|Coroutine)\b',
        re.IGNORECASE,
    ),
    # Category 4: Strategy pattern
    re.compile(
        r'\b(?:Context\s*\(\s*strategy\s*=|Strategy|ConcreteStrategy|'
        r'set_strategy|get_strategy)\b',
        re.IGNORECASE,
    ),
    # Category 5: Middleware chain
    re.compile(
        r'\b(?:middleware|app\.use|pipeline\.add|add_middleware|'
        r'use_middleware)\b',
        re.IGNORECASE,
    ),
    # Category 6: Event binding
    re.compile(
        r'\b(?:emitter\.on|addEventListener|subscribe|on_event|'
        r'event_handler|add_listener)\b',
        re.IGNORECASE,
    ),
    # Category 7: DI container
    re.compile(
        r'\b(?:container\.bind|container\.register|Provider|'
        r'Injector|inject_dependency|DependencyContainer)\b',
        re.IGNORECASE,
    ),
]

# Patterns that indicate a roadmap task explicitly addresses wiring
WIRING_TASK_PATTERNS = [
    # Explicit creation/population of dispatch/registry mechanisms
    re.compile(
        r'\b(?:create|build|construct|populate|wire|assemble|register)\s+'
        r'(?:the\s+|a\s+)?'
        r'(?:dispatch|routing|registry|runner|handler|command|middleware|'
        r'event|strategy|plugin)\s*'
        r'(?:table|map|dict|registry|lookup|chain|binding|container)\b',
        re.IGNORECASE,
    ),
    # Explicit wiring of implementations into mechanisms
    re.compile(
        r'\b(?:wire|connect|bind|inject|register|plug)\s+.*?'
        r'(?:implementations?|runners?|handlers?|plugins?|strategies?|'
        r'middlewares?|listeners?)\s+'
        r'(?:into|to|with|in)\b',
        re.IGNORECASE,
    ),
    # Specific named mechanisms from common specs
    re.compile(
        r'\bPROGRAMMATIC_RUNNERS\b|\bDISPATCH_TABLE\b|\bHANDLER_REGISTRY\b|'
        r'\bMIDDLEWARE_CHAIN\b|\bEVENT_BINDINGS\b|\bROUTE_MAP\b',
    ),
    # Strategy/middleware/event-specific wiring verbs
    re.compile(
        r'\b(?:configure|set[_\s]up|initialize|bootstrap)\s+'
        r'(?:the\s+)?'
        r'(?:strategy|middleware|event\s+binding|DI\s+container|'
        r'dependency\s+injection|plugin\s+registry)\b',
        re.IGNORECASE,
    ),
]


@dataclass
class IntegrationContract:
    """A single integration point extracted from a spec."""
    id: str                          # IC-001, IC-002, ...
    mechanism: str                   # "dispatch_table", "registry", "injection", etc.
    spec_evidence: str               # verbatim quote from spec
    spec_location: str               # line number or section heading
    description: str                 # human-readable description
    requires_explicit_wiring: bool   # True if cannot be implicit


@dataclass
class WiringCoverage:
    """Result of checking whether a contract is covered by roadmap tasks."""
    contract: IntegrationContract
    covered: bool
    roadmap_evidence: str            # quote from roadmap if covered, empty if not
    roadmap_location: str            # phase/task if covered


@dataclass
class IntegrationAuditResult:
    """Full audit result: all contracts and their coverage status."""
    contracts: list[IntegrationContract] = field(default_factory=list)
    coverage: list[WiringCoverage] = field(default_factory=list)
    uncovered_count: int = 0
    total_count: int = 0

    @property
    def all_covered(self) -> bool:
        return self.uncovered_count == 0


def extract_integration_contracts(spec_text: str) -> list[IntegrationContract]:
    """Extract integration contracts from spec text using pattern matching.

    Scans spec text for dispatch tables, registries, injection points,
    strategy patterns, middleware chains, event bindings, and DI containers.
    Returns a list of IntegrationContract instances, each representing a
    non-obvious integration point that requires an explicit roadmap task.
    """
    contracts: list[IntegrationContract] = []
    lines = spec_text.splitlines()
    seen_evidence: set[str] = set()  # dedup
    counter = 1

    for i, line in enumerate(lines):
        for pattern in DISPATCH_PATTERNS:
            match = pattern.search(line)
            if match:
                evidence = line.strip()
                if evidence in seen_evidence:
                    continue
                seen_evidence.add(evidence)

                # Extract surrounding context (3 lines before/after)
                context_start = max(0, i - 3)
                context_end = min(len(lines), i + 4)
                context = "\n".join(lines[context_start:context_end])

                mechanism = _classify_mechanism(match.group(0))
                contracts.append(IntegrationContract(
                    id=f"IC-{counter:03d}",
                    mechanism=mechanism,
                    spec_evidence=context,
                    spec_location=f"line {i + 1}",
                    description=f"{mechanism}: {evidence}",
                    requires_explicit_wiring=True,
                ))
                counter += 1

    return contracts


def check_roadmap_coverage(
    contracts: list[IntegrationContract],
    roadmap_text: str,
) -> IntegrationAuditResult:
    """Check whether each integration contract has explicit roadmap coverage.

    For each contract, searches the roadmap for explicit wiring tasks that
    address the integration point. A contract is "covered" only if the
    roadmap contains a task that explicitly mentions creating, populating,
    or wiring the mechanism -- NOT just implementing the components that
    will be wired.

    This is the key anti-pattern-matching check: implementing components
    is necessary but not sufficient. The wiring task itself must be explicit.
    """
    result = IntegrationAuditResult(
        contracts=contracts,
        total_count=len(contracts),
    )

    roadmap_lines = roadmap_text.splitlines()

    for contract in contracts:
        covered = False
        evidence = ""
        location = ""

        # Check for explicit wiring tasks in roadmap
        for pattern in WIRING_TASK_PATTERNS:
            for j, rline in enumerate(roadmap_lines):
                if pattern.search(rline):
                    covered = True
                    evidence = rline.strip()
                    location = f"line {j + 1}"
                    break
            if covered:
                break

        # Also check for the specific mechanism name from the spec
        if not covered:
            identifiers = _extract_identifiers(contract.spec_evidence)
            for ident in identifiers:
                for j, rline in enumerate(roadmap_lines):
                    if ident.upper() in rline.upper():
                        covered = True
                        evidence = rline.strip()
                        location = f"line {j + 1}"
                        break
                if covered:
                    break

        result.coverage.append(WiringCoverage(
            contract=contract,
            covered=covered,
            roadmap_evidence=evidence,
            roadmap_location=location,
        ))

        if not covered:
            result.uncovered_count += 1

    return result


def _classify_mechanism(matched_text: str) -> str:
    """Classify matched text into a mechanism category."""
    lower = matched_text.lower()
    if any(k in lower for k in ("dispatch", "runner", "handler", "command_map", "step_map")):
        return "dispatch_table"
    if "registry" in lower or "register" in lower:
        return "registry"
    if any(k in lower for k in ("inject", "callable", "protocol", "factory", "provider")):
        return "dependency_injection"
    if any(k in lower for k in ("wire", "bind", "populate")):
        return "explicit_wiring"
    if any(k in lower for k in ("route", "routing")):
        return "routing"
    if any(k in lower for k in ("strategy", "concretestrategy")):
        return "strategy_pattern"
    if any(k in lower for k in ("middleware", "app.use", "pipeline.add")):
        return "middleware_chain"
    if any(k in lower for k in ("emitter", "addeventlistener", "subscribe", "listener")):
        return "event_binding"
    if any(k in lower for k in ("container", "injector", "dependencycontainer")):
        return "di_container"
    return "integration_point"


def _extract_identifiers(text: str) -> list[str]:
    """Extract UPPER_SNAKE_CASE and PascalCase identifiers from text."""
    # UPPER_SNAKE_CASE (likely constants/tables)
    upper_snake = re.findall(r'\b[A-Z][A-Z0-9_]{2,}\b', text)
    # PascalCase class names
    pascal = re.findall(r'\b[A-Z][a-z]+(?:[A-Z][a-z]+)+\b', text)
    return upper_snake + pascal
```

### Pattern Library Expansion

<!-- Source: V5-1 (integration contract extractor), adapted per refactor-plan Section 6 Weakness 2 -->

The `DISPATCH_PATTERNS` and `WIRING_TASK_PATTERNS` have been expanded beyond V5's original 4+3 patterns to cover all 7 categories from V5's integration mechanism taxonomy:

| Category | DISPATCH_PATTERNS coverage | WIRING_TASK_PATTERNS coverage |
|---|---|---|
| Dict dispatch | `DISPATCH_TABLE`, `RUNNERS`, `HANDLERS`, `command_map`, `step_map` | `create/populate dispatch table/map` |
| Plugin registry | `registry`, `register` | `register implementations into registry` |
| Callback injection | `Callable`, `Protocol`, `ABC`, `Factory`, `Provider` | `wire/inject handlers into` |
| Strategy pattern | `Context(strategy=...)`, `Strategy`, `ConcreteStrategy` | `configure strategy` |
| Middleware chain | `middleware`, `app.use`, `pipeline.add` | `set up middleware chain` |
| Event binding | `emitter.on`, `addEventListener`, `subscribe` | `configure event binding` |
| DI container | `container.bind`, `container.register`, `Provider`, `Injector` | `initialize DI container` |

---

## 6. Module 3: Fingerprint Extraction

<!-- Source: V4-2 (fingerprint extraction) -->

### Concept

Goes beyond formal requirement IDs to extract "structural fingerprints" -- function names, class names, data structure names, and design pattern names that appear in code fences or backtick-delimited spans in the spec. Verifies each fingerprint appears in the roadmap. This is mechanism-agnostic: it catches any code-level identifier omission regardless of whether the spec uses FR-NNN tags or specific integration patterns.

### Detection Axis

V4-2 has the highest single-check efficacy (95% confidence) because it operates on the exact code-level identifiers that specs contain. A spec that mentions `_run_programmatic_step` in backticks expects the roadmap to plan for that function. If the roadmap does not mention it at all, coverage is objectively incomplete.

### Implementation

**File**: `src/superclaude/cli/roadmap/fingerprint.py` (new, ~150 LOC)

```python
"""Structural fingerprint extraction and coverage checking.

Extracts code-level identifiers from spec content (backtick-delimited names,
code-block definitions, ALL_CAPS constants) and verifies a minimum coverage
ratio appears in the roadmap. Catches wholesale omission of design detail
that text-matching on formal IDs would miss.

Pure function: content in, result out. No I/O.
"""

from __future__ import annotations

import re
from dataclasses import dataclass


@dataclass
class Fingerprint:
    """A named code-level entity from the spec."""
    text: str           # e.g., "_run_programmatic_step"
    category: str       # "identifier", "definition", "constant"
    source_context: str # surrounding text for debugging


# Common non-specific constants to exclude from fingerprint extraction
_EXCLUDED_CONSTANTS = frozenset({
    'TRUE', 'FALSE', 'NONE', 'TODO', 'NOTE', 'WARNING',
    'HIGH', 'MEDIUM', 'LOW', 'YAML', 'JSON', 'STRICT',
    'STANDARD', 'EXEMPT', 'LIGHT', 'PASS', 'FAIL',
    'INFO', 'DEBUG', 'ERROR', 'CRITICAL',
})


def extract_code_fingerprints(content: str) -> list[Fingerprint]:
    """Extract code-level identifiers from spec content.

    Sources:
    1. Backtick-delimited identifiers: `_run_programmatic_step()`
    2. Code-fenced blocks: function/class definitions
    3. ALL_CAPS constants (likely important data structures)
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
        if text not in _EXCLUDED_CONSTANTS:
            fingerprints.append(Fingerprint(
                text=text,
                category="constant",
                source_context=content[
                    max(0, match.start() - 40):match.end() + 40
                ].replace('\n', ' '),
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
) -> tuple[bool, float, list[Fingerprint], list[Fingerprint]]:
    """Check that spec fingerprints appear in roadmap.

    Returns (passed, coverage_ratio, all_fingerprints, missing_fingerprints).
    Gate passes if coverage ratio >= min_coverage_ratio.

    The ratio threshold (default 0.7) accounts for the fact that not every
    backtick identifier in a spec is a hard requirement -- some are examples,
    alternatives, or references to existing code. But a coverage ratio below
    70% strongly indicates wholesale omission of design detail.
    """
    spec_fps = extract_code_fingerprints(spec_content)
    if not spec_fps:
        return True, 1.0, [], []

    roadmap_lower = roadmap_content.lower()
    missing: list[Fingerprint] = []
    for fp in spec_fps:
        if fp.text.lower() not in roadmap_lower:
            missing.append(fp)

    coverage = 1.0 - (len(missing) / len(spec_fps))
    return coverage >= min_coverage_ratio, coverage, spec_fps, missing
```

### Threshold Rationale

<!-- Source: V4-2 (fingerprint extraction), adapted per refactor-plan Section 6 Weakness 4 -->

The default `min_coverage_ratio` of 0.7 is conservative because:
- Not every backtick identifier is a requirement (some are examples, alternatives, or references).
- A single mention in a design overview adds 1 to the numerator but does not inflate the ratio enough to mask wholesale omissions.
- The 0.7 threshold means 30% of spec identifiers can be absent before the gate triggers, accommodating illustrative content.
- Empirical tuning is expected: shadow-mode runs on real pipelines will calibrate the final value.

### Interaction with A-009 ("Mentioned is not Planned")

The fingerprint check is presence-based and therefore susceptible to the "mentioned is not planned" limitation (diff analysis A-009). However, the 0.7 threshold is for coverage ratio, not exact-match. A roadmap that passively mentions identifiers without planning tasks for them would still need to mention 70%+ of spec fingerprints to pass, which in practice requires genuine engagement with the spec content. The V5-1 contract extractor provides the verb-anchored check that distinguishes mention from planning.

---

## 7. Module 4: Spec Structural Audit

<!-- Source: V1-C (spec structural audit) -->

### Concept

A deterministic upstream guard between the spec input and the extraction output. It catches the case where the extraction LLM itself drops requirements before they ever reach the roadmap. Neither the obligation scanner, contract extractor, nor fingerprint check can detect this -- all downstream checks are vacuous if extraction drops a requirement.

### Detection Axis

V1-C is the only solution that guards the extraction step itself. All other checks assume the extraction is correct and validate downstream artifacts. If the extraction LLM drops the dispatch requirement entirely, V2-A has nothing to scan, V5-1 has nothing to extract contracts from, and V4-2 has no fingerprints to compare against.

### Implementation

**File**: `src/superclaude/cli/roadmap/spec_structural_audit.py` (new, ~80 LOC)

```python
"""Spec structural audit -- upstream guard on extraction quality.

Counts structural requirement indicators in the raw spec (code blocks,
MUST/SHALL clauses, function signatures, test names, registry patterns)
and compares against the extraction's total_requirements frontmatter value.
If the extraction reports suspiciously few requirements relative to the
spec's structural richness, it flags a potential extraction failure.

Pure function: spec text + extraction requirement count in, result out.
"""

from __future__ import annotations

import re
from dataclasses import dataclass


@dataclass
class SpecStructuralAudit:
    """Result of structural indicator counting."""
    code_block_count: int          # Number of code blocks in spec
    must_shall_count: int          # Sentences with MUST/SHALL/REQUIRED
    function_signature_count: int  # def foo() patterns in code blocks
    class_definition_count: int    # class Foo patterns in code blocks
    test_name_count: int           # test_* patterns
    registry_pattern_count: int    # UPPERCASE_DICT = { patterns
    pseudocode_blocks: int         # Blocks showing control flow (if/else/for)
    total_structural_indicators: int


def audit_spec_structure(spec_text: str) -> SpecStructuralAudit:
    """Count structural requirement indicators in the raw spec.

    These indicators approximate the spec's "requirement density." A spec
    with many code blocks, function signatures, MUST clauses, and test names
    should produce a correspondingly rich extraction. If the extraction's
    total_requirements is far below the indicator count, the extraction may
    have dropped requirements.
    """
    code_blocks = re.findall(r"```[\s\S]*?```", spec_text)
    code_text = "\n".join(code_blocks)

    code_block_count = len(code_blocks)
    must_shall_count = len(re.findall(
        r"\b(?:MUST|SHALL|REQUIRED)\b", spec_text
    ))
    function_signature_count = len(re.findall(
        r"\bdef\s+\w+\s*\(", code_text
    ))
    class_definition_count = len(re.findall(
        r"\bclass\s+\w+", code_text
    ))
    test_name_count = len(re.findall(
        r"\btest_\w+", spec_text
    ))
    registry_pattern_count = len(re.findall(
        r"\b[A-Z][A-Z_]+\s*=\s*\{", code_text
    ))
    pseudocode_blocks = len(re.findall(
        r"```[\s\S]*?(?:if\s|elif\s|else:|for\s|while\s)[\s\S]*?```", spec_text
    ))

    total = (
        code_block_count
        + must_shall_count
        + function_signature_count
        + class_definition_count
        + test_name_count
        + registry_pattern_count
        + pseudocode_blocks
    )

    return SpecStructuralAudit(
        code_block_count=code_block_count,
        must_shall_count=must_shall_count,
        function_signature_count=function_signature_count,
        class_definition_count=class_definition_count,
        test_name_count=test_name_count,
        registry_pattern_count=registry_pattern_count,
        pseudocode_blocks=pseudocode_blocks,
        total_structural_indicators=total,
    )


def check_extraction_adequacy(
    spec_text: str,
    extraction_total_requirements: int,
    threshold: float = 0.5,
) -> tuple[bool, SpecStructuralAudit]:
    """Check whether extraction captured enough of the spec's structural content.

    Returns (passed, audit_result).

    The threshold is conservative (0.5) because structural indicators overcount:
    code examples, alternatives, and non-requirement prose inflate the indicator
    count. A ratio below 0.5 strongly suggests the extraction dropped content.

    Phase 1: warning-only (logs warning but does not block pipeline).
    Phase 2: STRICT enforcement after shadow-mode validation.
    """
    audit = audit_spec_structure(spec_text)

    if audit.total_structural_indicators == 0:
        return True, audit  # No indicators to compare against

    ratio = extraction_total_requirements / audit.total_structural_indicators
    return ratio >= threshold, audit
```

### Enforcement Strategy

<!-- Source: V1-C (spec structural audit), adapted per refactor-plan -->

Phase 1 (immediate): Warning-only. The executor logs a warning if the ratio falls below 0.5 but does not block the pipeline. This allows shadow-mode validation on real specs before enforcement.

Phase 2 (after validation): STRICT enforcement. If the structural count suggests the extraction is missing significant content, the executor re-triggers extraction or halts with an actionable error.

---

## 8. Gate Definition

<!-- Source: Merge (new content bridging V2+V5) -->

### New Gate: `ANTI_INSTINCT_GATE`

**File**: `src/superclaude/cli/roadmap/gates.py` (modify existing)

```python
# --- Anti-Instinct Gate check functions ---

def _no_undischarged_obligations(content: str) -> bool:
    """Verify all scaffolding obligations in early phases are discharged by later phases.

    Runs V2-A obligation scanner on the anti-instinct audit report content.
    The actual scan has already been performed by the executor; this check
    validates the frontmatter result.
    """
    fm = _parse_frontmatter(content)
    if fm is None:
        return False
    try:
        return int(fm.get("undischarged_obligations", -1)) == 0
    except (ValueError, TypeError):
        return False


def _integration_contracts_covered(content: str) -> bool:
    """Verify all integration contracts from spec are covered in roadmap.

    This check requires both spec and roadmap content. Since semantic
    checks receive only a single content string, the real enforcement
    happens in the executor. This validates the executor's written result.
    """
    fm = _parse_frontmatter(content)
    if fm is None:
        return False
    try:
        return int(fm.get("uncovered_contracts", -1)) == 0
    except (ValueError, TypeError):
        return False


def _fingerprint_coverage_check(content: str) -> bool:
    """Verify spec code-level identifiers have sufficient roadmap coverage.

    This check requires both spec and roadmap content. Since semantic
    checks receive only a single content string, the real enforcement
    happens in the executor. This validates the executor's written result.
    """
    fm = _parse_frontmatter(content)
    if fm is None:
        return False
    try:
        return float(fm.get("fingerprint_coverage", 0.0)) >= 0.7
    except (ValueError, TypeError):
        return False


# --- Gate definition ---

ANTI_INSTINCT_GATE = GateCriteria(
    required_frontmatter_fields=[
        "undischarged_obligations",    # V2-A: integer count
        "uncovered_contracts",         # V5-1: integer count
        "fingerprint_coverage",        # V4-2: float 0.0-1.0
    ],
    min_lines=10,
    enforcement_tier="STRICT",
    semantic_checks=[
        SemanticCheck(
            name="no_undischarged_obligations",
            check_fn=_no_undischarged_obligations,
            failure_message=(
                "Undischarged scaffolding obligations detected: early-phase "
                "mocks/stubs/skeletons have no corresponding replace/integrate/"
                "wire task in later phases"
            ),
        ),
        SemanticCheck(
            name="integration_contracts_covered",
            check_fn=_integration_contracts_covered,
            failure_message=(
                "Spec integration contracts missing from roadmap: dispatch tables, "
                "registries, or injection points defined in spec have no explicit "
                "wiring task in roadmap"
            ),
        ),
        SemanticCheck(
            name="fingerprint_coverage_sufficient",
            check_fn=_fingerprint_coverage_check,
            failure_message=(
                "Spec code-level identifiers missing from roadmap: fingerprint "
                "coverage ratio below 0.7 threshold"
            ),
        ),
    ],
)
```

### Position in ALL_GATES

```python
ALL_GATES = [
    ...
    ("merge", MERGE_GATE),
    ("anti-instinct", ANTI_INSTINCT_GATE),   # NEW
    ("test-strategy", TEST_STRATEGY_GATE),
    ("spec-fidelity", SPEC_FIDELITY_GATE),
    ...
]
```

### Why a Separate Gate

<!-- Source: Merge (new content bridging V2+V5) -->

The `MERGE_GATE` validates the merge step's output quality (heading hierarchy, cross-refs, duplicates). The anti-instinct checks validate cross-artifact semantic fidelity -- a different concern. Keeping them separate follows the existing pattern where each gate corresponds to one validation concern. The `MERGE_GATE` runs on the merged roadmap; the `ANTI_INSTINCT_GATE` runs on the anti-instinct audit report produced by the executor.

### Coexistence with Unified Audit Gating D-03/D-04

D-03/D-04 (Unified Audit Gating SS13.4) materially overlap with this spec's fingerprint and integration-contract modules. If both ship:
- D-03/D-04 should be made conditional on `ANTI_INSTINCT_GATE` not being active, OR
- Both coexist as defense-in-depth with a documented deduplication policy

When modifying `roadmap/gates.py`, coordinate with Wiring Verification (`WIRING_GATE`) and Unified Audit Gating (D-03/D-04) to avoid merge conflicts.

### Anti-Instinct Audit Report Format

The executor produces `output_dir / "anti-instinct-audit.md"` with frontmatter:

```yaml
---
undischarged_obligations: 0
uncovered_contracts: 0
fingerprint_coverage: 0.85
total_obligations: 3
discharged_obligations: 3
total_contracts: 2
covered_contracts: 2
total_fingerprints: 15
matched_fingerprints: 13
structural_audit_passed: true
---
```

This file is the gate artifact. The `ANTI_INSTINCT_GATE` validates its frontmatter fields. The executor writes it after running all three deterministic checks.

---

## 9. Executor Integration

<!-- Source: Merge (new content bridging V2+V5) -->

### File: `src/superclaude/cli/roadmap/executor.py` (modify existing)

#### Change 1: Structural Audit After Extract

**Location**: After `EXTRACT_GATE` passes, before `generate-*` steps.

This is NOT a new pipeline Step. It is executor-level logic that runs between steps, following the existing pattern of `_inject_pipeline_diagnostics` after extract.

```python
# In executor.py, after extract gate passes:
from .spec_structural_audit import check_extraction_adequacy

def _run_structural_audit(config, output_dir):
    """Post-extract structural audit (V1-C upstream guard).

    Compares spec structural indicators against extraction requirement
    count. Phase 1: warning-only.
    """
    import yaml

    spec_text = config.spec_file.read_text(encoding="utf-8")
    extraction_path = output_dir / "extraction.md"
    extraction_text = extraction_path.read_text(encoding="utf-8")

    # Parse extraction frontmatter for total_requirements
    fm_match = re.match(r"^---\n(.*?)\n---", extraction_text, re.DOTALL)
    total_requirements = 0
    if fm_match:
        try:
            fm = yaml.safe_load(fm_match.group(1))
            total_requirements = int(fm.get("total_requirements", 0))
        except (yaml.YAMLError, ValueError, TypeError):
            pass

    passed, audit = check_extraction_adequacy(spec_text, total_requirements)
    if not passed:
        logger.warning(
            "Spec structural audit: extraction may be incomplete. "
            f"Spec has {audit.total_structural_indicators} structural indicators "
            f"but extraction reports only {total_requirements} requirements "
            f"(ratio: {total_requirements / max(audit.total_structural_indicators, 1):.2f}, "
            f"threshold: 0.5). Consider re-running extraction."
        )
    return passed, audit
```

#### Change 2: Anti-Instinct Audit Step After Merge

**Location**: Between `merge` Step and `test-strategy` Step in `_build_steps()`.

This is a non-LLM step. The executor handles it specially (runs Python logic instead of a subprocess) when `step.id == "anti-instinct"`. The step appears in the pipeline step list for progress reporting and halt diagnostics.

```python
# Add to _build_steps() between merge and test-strategy:
Step(
    id="anti-instinct",
    prompt="",  # Non-LLM step; executor handles directly
    output_file=out / "anti-instinct-audit.md",
    gate=ANTI_INSTINCT_GATE,
    timeout_seconds=30,  # Pure Python, <1s expected
    inputs=[config.spec_file, extraction, merge_file],
    retry_limit=0,  # Deterministic; retry would produce same result
),
```

#### Change 3: Anti-Instinct Audit Runner

```python
from .obligation_scanner import scan_obligations
from .integration_contracts import extract_integration_contracts, check_roadmap_coverage
from .fingerprint import check_fingerprint_coverage

def _run_anti_instinct_audit(config, output_dir):
    """Run all three deterministic anti-instinct checks.

    Reads spec, extraction, and merged roadmap. Runs:
    1. V2-A obligation scanner on roadmap content
    2. V5-1 integration contract extractor on spec + roadmap
    3. V4-2 fingerprint coverage on spec + roadmap

    Writes anti-instinct-audit.md with frontmatter for gate validation.
    """
    spec_text = config.spec_file.read_text(encoding="utf-8")
    roadmap_path = output_dir / "roadmap.md"
    roadmap_text = roadmap_path.read_text(encoding="utf-8")

    # 1. Obligation scanner (V2-A) -- single-file, roadmap only
    obligation_report = scan_obligations(roadmap_text)

    # 2. Integration contracts (V5-1) -- spec + roadmap
    contracts = extract_integration_contracts(spec_text)
    contract_result = check_roadmap_coverage(contracts, roadmap_text)

    # 3. Fingerprint coverage (V4-2) -- spec + roadmap
    fp_passed, fp_coverage, all_fps, missing_fps = check_fingerprint_coverage(
        spec_text, roadmap_text
    )

    # Write audit report
    report_lines = [
        "---",
        f"undischarged_obligations: {obligation_report.undischarged}",
        f"uncovered_contracts: {contract_result.uncovered_count}",
        f"fingerprint_coverage: {fp_coverage:.2f}",
        f"total_obligations: {obligation_report.total_obligations}",
        f"discharged_obligations: {obligation_report.discharged}",
        f"total_contracts: {contract_result.total_count}",
        f"covered_contracts: {contract_result.total_count - contract_result.uncovered_count}",
        f"total_fingerprints: {len(all_fps)}",
        f"matched_fingerprints: {len(all_fps) - len(missing_fps)}",
        f"structural_audit_passed: true",
        "---",
        "",
        "# Anti-Instinct Audit Report",
        "",
    ]

    # Obligation details
    report_lines.append("## Obligation Scanner (V2-A)")
    report_lines.append("")
    if obligation_report.obligations:
        report_lines.append("| Phase | Term | Context | Discharged | Discharge Phase |")
        report_lines.append("|---|---|---|---|---|")
        for obl in obligation_report.obligations:
            discharged_str = "YES" if obl.discharged else "**NO**"
            d_phase = obl.discharge_phase or "N/A"
            report_lines.append(
                f"| {obl.phase} | {obl.term} | {obl.context[:60]} | "
                f"{discharged_str} | {d_phase} |"
            )
    else:
        report_lines.append("No scaffolding obligations detected.")
    report_lines.append("")

    # Contract details
    report_lines.append("## Integration Contracts (V5-1)")
    report_lines.append("")
    if contract_result.coverage:
        report_lines.append("| Contract | Mechanism | Covered | Evidence |")
        report_lines.append("|---|---|---|---|")
        for cov in contract_result.coverage:
            covered_str = "YES" if cov.covered else "**NO**"
            evidence = cov.roadmap_evidence[:60] if cov.covered else "N/A"
            report_lines.append(
                f"| {cov.contract.id} | {cov.contract.mechanism} | "
                f"{covered_str} | {evidence} |"
            )
    else:
        report_lines.append("No integration contracts detected in spec.")
    report_lines.append("")

    # Fingerprint details
    report_lines.append("## Fingerprint Coverage (V4-2)")
    report_lines.append("")
    report_lines.append(f"Coverage ratio: {fp_coverage:.2f} (threshold: 0.70)")
    report_lines.append("")
    if missing_fps:
        report_lines.append("### Missing Fingerprints")
        report_lines.append("")
        for fp in missing_fps:
            report_lines.append(f"- `{fp.text}` ({fp.category})")
    report_lines.append("")

    audit_path = output_dir / "anti-instinct-audit.md"
    audit_path.write_text("\n".join(report_lines), encoding="utf-8")

    return obligation_report, contract_result, (fp_passed, fp_coverage, missing_fps)
```

#### Change 4: Import and Step ID Updates

```python
# Add to executor.py imports:
from .gates import ANTI_INSTINCT_GATE

# Add "anti-instinct" to _get_all_step_ids() between "merge" and "test-strategy"
```

---

## 10. Prompt Modifications

<!-- Source: V1-D+V5-2 merged (prompt constraint) -->

### File: `src/superclaude/cli/roadmap/prompts.py` (modify existing)

#### Change 1: Integration Enumeration Block in `build_generate_prompt()`

**Location**: Append before the `_OUTPUT_FORMAT_BLOCK` in the return value.

```python
INTEGRATION_ENUMERATION_BLOCK = """

## CRITICAL: Integration Point Enumeration

Before generating the roadmap phases, you MUST first enumerate ALL
integration points from the extraction document. An integration point
is any place where:
- A data structure maps identifiers to implementations (dispatch table,
  registry, router, lookup dict)
- A constructor/factory accepts injectable dependencies (Callable,
  Protocol, ABC, Factory parameters)
- An explicit wiring/binding step is described ("populate X with Y",
  "register Z in W")
- A lookup/dispatch mechanism is defined (match/case, dict dispatch,
  plugin registry)

For EACH integration point, your roadmap MUST contain an explicit task that:
1. Names the integration artifact (e.g., 'PROGRAMMATIC_RUNNERS dispatch table')
2. Lists what gets wired into it (e.g., 'all step runner implementations')
3. Specifies which phase owns this wiring task
4. Is NOT the same phase that implements the components being wired

WARNING: Do NOT assume that implementing components automatically wires them.
Building a class does not register it in a dispatch table. Building a function
does not add it to a lookup dict. Import-time side effects are NOT wiring.
The wiring is a separate, explicit task.

Common integration patterns that MUST be explicitly tasked:
- Dispatch tables: creating the mapping from IDs to implementation functions
- Constructor injection: passing dependencies that default to None
- Import chains: adding import statements from consumer to producer
- Registration: adding entries to registries, dictionaries, or configuration

If the spec defines a dispatch model (e.g., a dictionary mapping step IDs to
functions), the roadmap MUST contain a task for populating that dictionary with
real function references. "Implement executor" does NOT satisfy this --
"Wire step dispatch table to step implementations" does.

Include an '## Integration Wiring Tasks' section in your roadmap that
cross-references each integration point to its wiring task and phase.
"""
```

#### Change 2: Integration Wiring Dimension in `build_spec_fidelity_prompt()`

<!-- Source: V5-2 (prompt augmentation) -->

**Location**: After dimension 5 ("NFRs") in the "Comparison Dimensions" section.

```python
INTEGRATION_WIRING_DIMENSION = """
6. **Integration Wiring**: For every dispatch table, registry, or
dependency injection point defined in the spec, verify the roadmap
contains an explicit task that creates and populates the mechanism --
not just tasks that implement the components being dispatched. Flag any
integration point where the spec defines custom wiring (e.g., a dispatch
dict, plugin registry, callback injection) but the roadmap only has
component implementation tasks without an explicit wiring phase.
"""
```

---

## 11. Contradiction Resolutions

<!-- Source: Merge (new content bridging V2+V5) -->

All contradictions identified in the diff analysis (X-001 through X-008) are resolved in this specification:

| ID | Contradiction | Resolution |
|---|---|---|
| X-001 | V1-A vs V4-1 duplicate ID cross-reference | Neither adopted in Phase 1. V4-2 fingerprints subsume ID cross-ref for code-heavy specs. If formal ID tracking is wanted later, it can be added as a separate module. |
| X-002 | V1-D vs V5-2 overlapping prompt constraints | Merged into single `INTEGRATION_ENUMERATION_BLOCK`. V5-2's enumeration requirement is the base; V1-D's specific examples (dispatch tables, constructor injection, import chains, registration) are incorporated. |
| X-003 | V1-B vs V3-1 duplicate producer-consumer graphs | V3-1 subsumes V1-B. Both deferred to Phase 2 (coherence graph). |
| X-004 | V2-A vs V5-3 AP-001 duplicate scaffold detection | V2-A adopted as the implementation. V2-A is more precise (tracks component context, per-phase scan vs. whole-document boolean). V5-3's rule engine framework deferred to Phase 2. |
| X-005 | V1-E vs V4-3 opposing LLM review framing | V4-3 (negative framing) preferred over V1-E (positive framing) per forensic evidence. Both deferred to Phase 2. V1-E's structured table output format preserved for Phase 2's response schema. |
| X-006 | V2-B vs V3-2 competing prompt injections | Merged into single "prior phase context" injection concept. Deferred to Phase 2 alongside coherence graph. |
| X-007 | V3 vs V4 on enforcement tier | Deterministic checks (V2-A, V5-1, V4-2) get STRICT enforcement (zero false-positive risk on true positives). Heuristic checks (future V3-1) get TRAILING initially. |
| X-008 | V4-5 stateful registry vs stateless pipeline | V4-5 rejected. Architecturally incompatible with current stateless pipeline model. All other variants implicitly reject this approach. |

---

## 12. File Change List

<!-- Source: Merge (new content bridging V2+V5) -->

### New Files (4 source + 4 test)

| File | Source | LOC | Purpose |
|---|---|---|---|
| `src/superclaude/cli/roadmap/obligation_scanner.py` | V2-A | ~200 | Scaffold-discharge obligation detection |
| `src/superclaude/cli/roadmap/integration_contracts.py` | V5-1 | ~250 | Integration contract extraction and roadmap coverage verification |
| `src/superclaude/cli/roadmap/fingerprint.py` | V4-2 | ~150 | Code-level identifier extraction and coverage check |
| `src/superclaude/cli/roadmap/spec_structural_audit.py` | V1-C | ~80 | Upstream extraction quality guard |
| `tests/roadmap/test_obligation_scanner.py` | V2-A | ~100 | Scaffold/discharge detection, phase splitting, component context |
| `tests/roadmap/test_integration_contracts.py` | V5-1 | ~100 | Contract extraction, coverage checking, mechanism classification |
| `tests/roadmap/test_fingerprint.py` | V4-2 | ~100 | Fingerprint extraction, coverage ratio, threshold behavior |
| `tests/roadmap/test_spec_structural_audit.py` | V1-C | ~60 | Structural indicator counting, ratio comparison |

### Modified Files (3)

| File | Changes | Source |
|---|---|---|
| `src/superclaude/cli/roadmap/gates.py` | Add `ANTI_INSTINCT_GATE` definition with 3 semantic checks; add 3 check functions (`_no_undischarged_obligations`, `_integration_contracts_covered`, `_fingerprint_coverage_check`); update `ALL_GATES` list to insert `("anti-instinct", ANTI_INSTINCT_GATE)` between `merge` and `test-strategy` | V2-A + V5-1 + V4-2 |
| `src/superclaude/cli/roadmap/executor.py` | Add anti-instinct step to `_build_steps()`; add structural audit hook after extract (`_run_structural_audit`); add `_run_anti_instinct_audit()` function; add import for `ANTI_INSTINCT_GATE`; update `_get_all_step_ids()` to include `"anti-instinct"` | All |
| `src/superclaude/cli/roadmap/prompts.py` | Add `INTEGRATION_ENUMERATION_BLOCK` to `build_generate_prompt()` return value; add `INTEGRATION_WIRING_DIMENSION` as 6th comparison dimension to `build_spec_fidelity_prompt()` | V1-D + V5-2 |

### Total Impact

- **New files**: 4 source + 4 test = 8 files
- **Modified files**: 3 files
- **Total new LOC**: ~680 (source) + ~360 (tests, estimated) = ~1,040
- **LLM calls added**: 0 (all checks are pure Python)
- **Pipeline latency added**: <1s (combined deterministic execution)
- **Existing model changes**: 0 (no changes to `SemanticCheck`, `GateCriteria`, `Step`, or `PipelineConfig`)

---

## 13. Implementation Phases

<!-- Source: Merge (new content bridging V2+V5) -->

### Phase 1: Immediate (this specification)

All content in Sections 4-10 above. Four new modules, one new gate, executor wiring, prompt modifications. Zero LLM calls added. Estimated implementation: 4-6 sprint tasks.

**Implementation sequence** (respects dependency graph):

```
obligation_scanner.py --+
integration_contracts.py --+--> gates.py --> executor.py
fingerprint.py -----------+                    |
spec_structural_audit.py --------------------->+
prompts.py (independent, can be done in parallel)
```

1. `obligation_scanner.py` + tests -- highest implementation readiness
2. `integration_contracts.py` + tests -- expanded pattern library
3. `fingerprint.py` + tests
4. `spec_structural_audit.py` + tests
5. `gates.py` -- add `ANTI_INSTINCT_GATE` with all 3 semantic checks
6. `executor.py` -- wire anti-instinct step + structural audit hook
7. `prompts.py` -- add enumeration block + 6th fidelity dimension
8. Integration test -- end-to-end using cli-portify spec/roadmap as regression case

### Phase 2: Deferred Items

Items explicitly deferred from Phase 1 with adoption conditions:

| Item | Source | Adoption Condition |
|---|---|---|
| Negative-space prompting (with V1-E structured output schema) | V4-3 + V1-E | After Phase 1 deterministic checks validated in shadow mode (3+ pipeline runs with zero false positives) |
| Coherence graph (producer-consumer graph with disconnected pair detection) | V3-1 | After existing dataflow infrastructure assessed for reuse; requires extraction heuristic design doc |
| Obligation ledger + manifest injection (prevention layer via prompt state) | V2-B + V3-2 merged | After pipeline state management design approved; requires prompt injection testing |
| SemanticCheck model extension for multi-file access | V4 Option B | After 2+ multi-file checks are in production and the executor workaround proves limiting |
| Anti-pattern rule engine framework | V5-3 | After 3+ anti-pattern rules are identified beyond AP-001 (already covered by V2-A) |

---

## 14. Shared Assumptions and Known Risks

<!-- Source: Merge (new content bridging V2+V5) -->

| ID | Assumption | Risk If Wrong | Mitigation |
|---|---|---|---|
| A-001 | Extraction produces requirement IDs | V1-A/V4-1 would be vacuous | Not adopted in Phase 1; V4-2 fingerprints work without IDs |
| A-002 | Roadmap uses parseable natural language | All regex solutions produce false negatives | Prompt constraint (V1-D+V5-2) reduces probability; fingerprints catch code-level names regardless |
| A-004 | Scaffolding language is keyword-detectable | V2-A misses non-vocabulary deferral | Component context extraction + `# obligation-exempt` escape hatch |
| A-007 | SemanticCheck single-file limitation | Multi-file checks need workarounds | Executor-level workaround (write audit report, validate frontmatter). Phase 2: model extension |
| A-008 | Thresholds are correct without empirical data | False positives or negatives | Shadow-mode validation before STRICT enforcement on fingerprint threshold |
| A-009 | Mention equals coverage | Keyword presence without task adequacy | V5-1 uses verb-anchored wiring patterns; V4-2 uses ratio threshold; combined checks reduce risk |
| A-010 | LLM tendencies are correlated | Joint miss-rate optimistic | All Phase 1 checks are deterministic (not LLM), so correlation between LLM tendencies is irrelevant |

---

## 15. V5-3 AP-001 Subsumption by V2-A

<!-- Source: V2-A (obligation scanner), V5-1 (integration contract extractor) -->

Per diff analysis X-004: V2-A's obligation scanner is the implementation of V5-3's AP-001 rule ("skeleton_without_wiring"). The rule engine framework from V5-3 is not adopted in Phase 1 because:

1. V2-A's scanner is more precise (tracks component context, per-phase scan vs. whole-document boolean)
2. The rule engine adds structural overhead without adding detection capability
3. AP-002 ("implicit_integration_assumption") is too imprecise for STRICT enforcement
4. AP-003 ("dict_dispatch_without_population_phase") is subsumed by V5-1's contract extractor

If additional anti-pattern rules are needed in Phase 2, the rule engine can be introduced at that time with V2-A as a delegate for AP-001.

---

## 16. Rejected Alternatives

<!-- Source: Merge (new content bridging V2+V5) -->

For completeness, these alternatives were evaluated and not included in Phase 1:

| Alternative | Source | Reason for Rejection |
|---|---|---|
| Requirement ID cross-reference | V1-A / V4-1 | Duplicated by V4-2 fingerprints; depends on extraction producing FR-NNN IDs |
| Orphaned component detection | V1-B | Subsumed by V3-1 (deferred to Phase 2) |
| Negative-space prompting | V4-3 | Adds LLM call cost; deferred until deterministic checks validated |
| Coherence graph | V3-1 | Highest implementation risk; extraction heuristics underspecified |
| Obligation ledger + manifest injection | V2-B + V3-2 | Requires state management; deferred to Phase 2 |
| Requirement registry | V4-5 | Architecturally incompatible with stateless pipeline |
| Anti-pattern rule engine (as separate module) | V5-3 | AP-001 subsumed by V2-A; framework adds overhead without Phase 1 value |
| Integration completeness LLM pass (positive framing) | V1-E | Forensic evidence shows positive framing fails; negative framing (V4-3) preferred for Phase 2 |

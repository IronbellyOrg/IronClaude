# Anti-Instinct 05: Pattern-Matching Trap Mitigation

## Problem Statement

### The LLM Tendency

LLMs have internalized thousands of examples of the common software engineering pattern: **"build skeleton -> implement components -> test"**. When generating roadmaps from specifications, the LLM reproduces this familiar structure without verifying that it covers ALL integration points required by the specific spec. The pattern "feels complete" because it usually is in training data -- except when it isn't.

This is a form of **overgeneralization from training data**: the model assumes standard wiring will suffice because that's what the pattern usually implies, even when the spec defines non-obvious custom dispatch mechanisms that require explicit integration tasks.

### The Specific Bug (cli-portify)

The roadmap pipeline generated a roadmap for the cli-portify feature that followed a familiar phasing:

- Phase 2: Scaffold executor loop with injectable step structure
- Phases 4-7: Implement individual step runners (preflight, executor, etc.)
- Later phases: Test and integrate

The spec explicitly required a `PROGRAMMATIC_RUNNERS` dispatch table -- a concrete Python dictionary mapping step names to their runner callables -- that the executor loop would use to dispatch work. This is a **non-standard integration artifact**: it is not a "component" in the usual sense, nor is it "wiring" that happens implicitly when you import modules. It is a first-class artifact that must be explicitly constructed, populated, and injected.

The LLM recognized the "skeleton with mocks -> fill in later" pattern and assumed the dispatch wiring would happen implicitly as part of the component implementation phases. No phase explicitly owned the task of: "create the PROGRAMMATIC_RUNNERS dispatch table, populate it with all step implementations, and wire it into the executor loop." The gap between "skeleton exists" and "implementations exist" was a non-obvious integration task that fell through the cracks.

### Why Existing Gates Did Not Catch This

The current `spec-fidelity` step (see `src/superclaude/cli/roadmap/prompts.py::build_spec_fidelity_prompt`) compares the spec against the roadmap across 5 dimensions: Signatures, Data Models, Gates, CLI Options, and NFRs. However:

1. **Dispatch tables** are not a named dimension. `PROGRAMMATIC_RUNNERS` is a data structure, but the fidelity check looks for "schemas, field definitions" -- not dispatch/routing tables.
2. **Integration wiring** is not a dimension. The fidelity check does not ask "for every injectable dependency in the skeleton, is there a phase that explicitly wires the implementations into the skeleton?"
3. The fidelity check is a single LLM call, so it is susceptible to the same pattern-matching bias: it may see "Phase 2 creates skeleton, Phases 4-7 implement runners" and conclude the wiring is covered.

---

## Proposed Solutions

### Solution 1: Integration Contract Extractor (Recommended -- Primary)

**Concept**: A deterministic pre-validation step that extracts "integration contracts" from the spec and verifies each has a corresponding explicit task in the roadmap.

**What is an integration contract?** Any place in the spec where:
- A data structure maps identifiers to callables (dispatch table, registry, router)
- A constructor/factory accepts injectable dependencies (Callable, Protocol, ABC params)
- An explicit wiring step is described ("populate X with Y", "register Z in W")
- A lookup/dispatch mechanism is defined (match/case on type, dict dispatch, plugin registry)

**Implementation**:

#### File: `src/superclaude/cli/roadmap/integration_contracts.py` (new module)

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

# These patterns identify spec text that describes integration mechanisms
# which require explicit roadmap tasks (not implicit from component phasing).
DISPATCH_PATTERNS = [
    # Dict dispatch tables: "RUNNERS = {", "dispatch_table", "registry"
    re.compile(
        r'\b(?:dispatch[_\s]?table|registry|RUNNERS|_RUNNERS|HANDLERS|'
        r'DISPATCH|routing[_\s]?table|command[_\s]?map|step[_\s]?map|'
        r'plugin[_\s]?registry)\b',
        re.IGNORECASE,
    ),
    # Explicit wiring language: "populate X with", "register Y in", "wire Z to"
    re.compile(
        r'\b(?:populate|register|wire|inject|bind|map|route)\s+'
        r'(?:the\s+|all\s+|each\s+)?'
        r'(?:implementations?|runners?|handlers?|plugins?|steps?|commands?)\b',
        re.IGNORECASE,
    ),
    # Constructor injection: "accepts a Callable", "takes a Protocol"
    re.compile(
        r'\b(?:accepts?|takes?|requires?|expects?)\s+(?:a\s+)?'
        r'(?:Callable|Protocol|ABC|Interface|Factory|Provider|Registry)\b',
        re.IGNORECASE,
    ),
    # Dict[str, Callable] or Mapping[str, ...] type annotations in spec
    re.compile(
        r'\b(?:Dict|Mapping|dict)\s*\[\s*str\s*,\s*(?:Callable|Awaitable|Coroutine)\b',
        re.IGNORECASE,
    ),
]

# Patterns that indicate a roadmap task explicitly addresses wiring
WIRING_TASK_PATTERNS = [
    re.compile(
        r'\b(?:create|build|construct|populate|wire|assemble|register)\s+'
        r'(?:the\s+|a\s+)?'
        r'(?:dispatch|routing|registry|runner|handler|command)\s*'
        r'(?:table|map|dict|registry|lookup)\b',
        re.IGNORECASE,
    ),
    re.compile(
        r'\b(?:wire|connect|bind|inject|register)\s+.*?'
        r'(?:implementations?|runners?|handlers?|plugins?)\s+'
        r'(?:into|to|with|in)\b',
        re.IGNORECASE,
    ),
    re.compile(
        r'\bPROGRAMMATIC_RUNNERS\b|\bDISPATCH_TABLE\b|\bHANDLER_REGISTRY\b',
    ),
]


@dataclass
class IntegrationContract:
    """A single integration point extracted from a spec."""
    id: str                          # IC-001, IC-002, ...
    mechanism: str                   # "dispatch_table", "registry", "injection"
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
    and explicit wiring instructions. Returns a list of IntegrationContract
    instances, each representing a non-obvious integration point that
    requires an explicit roadmap task.
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
            # Extract key identifiers from the spec evidence
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
    if any(k in lower for k in ("dispatch", "runner", "handler", "command_map")):
        return "dispatch_table"
    if "registry" in lower or "register" in lower:
        return "registry"
    if any(k in lower for k in ("inject", "callable", "protocol", "factory")):
        return "dependency_injection"
    if any(k in lower for k in ("wire", "bind", "populate")):
        return "explicit_wiring"
    if any(k in lower for k in ("route", "routing")):
        return "routing"
    return "integration_point"


def _extract_identifiers(text: str) -> list[str]:
    """Extract UPPER_SNAKE_CASE and PascalCase identifiers from text."""
    # UPPER_SNAKE_CASE (likely constants/tables)
    upper_snake = re.findall(r'\b[A-Z][A-Z0-9_]{2,}\b', text)
    # PascalCase class names
    pascal = re.findall(r'\b[A-Z][a-z]+(?:[A-Z][a-z]+)+\b', text)
    return upper_snake + pascal
```

#### Integration point: `src/superclaude/cli/roadmap/gates.py`

Add a new semantic check and gate:

```python
def _integration_contracts_covered(content: str) -> bool:
    """Verify all integration contracts from spec are covered in roadmap.

    This check requires both spec and roadmap content. Since semantic
    checks receive only a single content string, this check must be
    run as a standalone audit step rather than a gate semantic check.

    Placeholder: always returns True. Actual enforcement happens in
    the integration_audit pipeline step.
    """
    # Integration audit runs as a separate step; this is a schema placeholder.
    # See: IntegrationAuditStep in executor.py
    return True
```

#### Integration point: `src/superclaude/cli/roadmap/executor.py`

Add a new pipeline step between `merge` and `spec-fidelity`:

```python
def _run_integration_audit(
    spec_text: str,
    roadmap_text: str,
    output_dir: Path,
) -> IntegrationAuditResult:
    """Run deterministic integration contract audit.

    This is NOT an LLM step. It is a pure Python function that:
    1. Extracts integration contracts from the spec
    2. Checks each against the roadmap for explicit coverage
    3. Returns structured results

    If uncovered contracts are found, the pipeline emits warnings
    and optionally blocks (depending on enforcement tier).
    """
    from .integration_contracts import (
        extract_integration_contracts,
        check_roadmap_coverage,
    )

    contracts = extract_integration_contracts(spec_text)
    result = check_roadmap_coverage(contracts, roadmap_text)

    # Write audit report
    report_path = output_dir / "integration-audit.md"
    _write_audit_report(report_path, result)

    return result
```

#### How it would have caught the cli-portify bug

1. The spec contains text like: `PROGRAMMATIC_RUNNERS = {`, `dispatch table mapping step names to runner callables`, `populate the runner registry`
2. `extract_integration_contracts()` would match these via `DISPATCH_PATTERNS` and produce `IntegrationContract(id="IC-001", mechanism="dispatch_table", ...)`
3. `check_roadmap_coverage()` would scan the roadmap for explicit tasks mentioning `PROGRAMMATIC_RUNNERS`, "create dispatch table", "wire runners into executor", etc.
4. Finding none (because the roadmap only had "implement step runners" tasks, not "wire runners into dispatch table" tasks), it would flag `IC-001` as **uncovered**.
5. The pipeline would emit: `UNCOVERED INTEGRATION CONTRACT: IC-001 (dispatch_table) -- spec defines PROGRAMMATIC_RUNNERS dispatch table but no roadmap task explicitly creates/populates it.`

---

### Solution 2: Prompt Augmentation -- Forced Integration Enumeration

**Concept**: Augment the `build_generate_prompt()` and `build_spec_fidelity_prompt()` templates to force the LLM to explicitly enumerate all integration points before generating or validating the roadmap.

**Implementation**: Modify `src/superclaude/cli/roadmap/prompts.py`

Add this block to `build_generate_prompt()`:

```python
INTEGRATION_ENUMERATION_BLOCK = (
    "\n\n## CRITICAL: Integration Point Enumeration\n\n"
    "Before generating the roadmap phases, you MUST first enumerate ALL "
    "integration points from the spec. An integration point is any place where:\n"
    "- A data structure maps identifiers to implementations (dispatch table, registry, router)\n"
    "- A constructor/factory accepts injectable dependencies\n"
    "- An explicit wiring/binding step is described\n"
    "- A lookup/dispatch mechanism is defined\n\n"
    "For EACH integration point, your roadmap MUST contain an explicit task that:\n"
    "1. Names the integration artifact (e.g., 'PROGRAMMATIC_RUNNERS dispatch table')\n"
    "2. Lists what gets wired into it (e.g., 'all step runner implementations')\n"
    "3. Specifies which phase owns this wiring task\n"
    "4. Is NOT the same phase that implements the components being wired\n\n"
    "WARNING: Do NOT assume that implementing components automatically wires them. "
    "Building a class does not register it in a dispatch table. Building a function "
    "does not add it to a lookup dict. The wiring is a separate, explicit task.\n\n"
    "Include an '## Integration Wiring Tasks' section in your roadmap that "
    "cross-references each integration point to its wiring task."
)
```

Add this block to `build_spec_fidelity_prompt()` as a 6th comparison dimension:

```python
"6. **Integration Wiring**: For every dispatch table, registry, or "
"dependency injection point defined in the spec, verify the roadmap "
"contains an explicit task that creates and populates the mechanism -- "
"not just tasks that implement the components being dispatched. "
"Flag any integration point where the spec defines custom wiring "
"(e.g., a dispatch dict, plugin registry, callback injection) but "
"the roadmap only has component implementation tasks without an "
"explicit wiring phase.\n"
```

**Pros**: Low implementation cost, addresses the problem at the prompt level.
**Cons**: Still relies on LLM compliance. A sufficiently strong pattern-matching bias could override the prompt instruction. This is "asking the LLM to try harder" with more specific instructions, which is semi-deterministic at best.

**Recommendation**: Use as a complement to Solution 1, not a replacement.

---

### Solution 3: Anti-Pattern Rule Engine

**Concept**: A set of deterministic rules that detect known dangerous roadmap patterns and flag them for review.

**Rules**:

```python
ANTI_PATTERN_RULES = [
    {
        "id": "AP-001",
        "name": "skeleton_without_wiring",
        "description": (
            "A phase creates a class/module with injectable parameters "
            "(Callable, Optional, Protocol) and a later phase implements "
            "the injected dependencies, but no phase explicitly wires them."
        ),
        "detection": (
            "Scan roadmap for phases containing 'scaffold', 'skeleton', "
            "'stub', 'mock' AND later phases containing 'implement', "
            "'build'. Then check for an intervening or subsequent phase "
            "containing 'wire', 'register', 'populate', 'dispatch', 'bind'."
        ),
        "severity": "HIGH",
    },
    {
        "id": "AP-002",
        "name": "implicit_integration_assumption",
        "description": (
            "The roadmap assumes a standard build-test pattern covers "
            "integration without naming the specific integration mechanism."
        ),
        "detection": (
            "Scan for phases labeled 'integration' or 'testing' that "
            "do not name specific artifacts being integrated. Generic "
            "'integration testing' without naming what is integrated "
            "is a red flag."
        ),
        "severity": "MEDIUM",
    },
    {
        "id": "AP-003",
        "name": "dict_dispatch_without_population_phase",
        "description": (
            "The spec defines a dict-based dispatch/lookup mechanism "
            "but the roadmap has no phase that explicitly populates it."
        ),
        "detection": (
            "Cross-reference: if spec mentions Dict[str, Callable] or "
            "similar dispatch patterns, verify roadmap has a phase "
            "that populates the specific dict."
        ),
        "severity": "HIGH",
    },
]
```

**Implementation**: `src/superclaude/cli/roadmap/anti_patterns.py` (new module)

```python
"""Anti-pattern detection rules for roadmap validation.

Deterministic checks that detect known dangerous roadmap patterns where
LLM pattern-matching tendencies produce familiar-looking but incomplete
phasing. Each rule checks for a specific structural anti-pattern.
"""

from __future__ import annotations

import re
from dataclasses import dataclass


@dataclass
class AntiPatternMatch:
    """A detected anti-pattern instance."""
    rule_id: str
    rule_name: str
    severity: str
    evidence: str               # what triggered the match
    missing_element: str        # what the roadmap is missing
    recommendation: str


def check_skeleton_without_wiring(roadmap_text: str) -> list[AntiPatternMatch]:
    """AP-001: Detect skeleton phases without corresponding wiring phases.

    Scans for roadmap phases that create scaffolds/skeletons with
    injectable points, then checks whether a subsequent phase
    explicitly wires implementations into those injection points.
    """
    matches: list[AntiPatternMatch] = []
    lines = roadmap_text.splitlines()

    scaffold_pattern = re.compile(
        r'\b(?:scaffold|skeleton|stub|mock|placeholder|framework)\b',
        re.IGNORECASE,
    )
    implement_pattern = re.compile(
        r'\b(?:implement|build|create|develop)\s+'
        r'(?:the\s+|all\s+|each\s+|individual\s+)?'
        r'(?:step|runner|handler|plugin|command|component)s?\b',
        re.IGNORECASE,
    )
    wiring_pattern = re.compile(
        r'\b(?:wire|register|populate|bind|connect|dispatch|inject|plug\s*in)\b',
        re.IGNORECASE,
    )

    has_scaffold = any(scaffold_pattern.search(line) for line in lines)
    has_implement = any(implement_pattern.search(line) for line in lines)
    has_wiring = any(wiring_pattern.search(line) for line in lines)

    if has_scaffold and has_implement and not has_wiring:
        matches.append(AntiPatternMatch(
            rule_id="AP-001",
            rule_name="skeleton_without_wiring",
            severity="HIGH",
            evidence=(
                "Roadmap contains scaffold/skeleton phase and implementation "
                "phase but no explicit wiring/registration phase."
            ),
            missing_element=(
                "A phase that explicitly wires/registers/populates the "
                "implementations into the scaffold's injection points."
            ),
            recommendation=(
                "Add a dedicated wiring phase (or task within a phase) that "
                "explicitly: (1) names the dispatch/registry mechanism, "
                "(2) lists what gets registered, (3) verifies registration "
                "completeness."
            ),
        ))

    return matches


def check_all_anti_patterns(roadmap_text: str) -> list[AntiPatternMatch]:
    """Run all anti-pattern checks and return combined results."""
    results: list[AntiPatternMatch] = []
    results.extend(check_skeleton_without_wiring(roadmap_text))
    # Future: add AP-002, AP-003, etc.
    return results
```

---

## Recommended Implementation Plan

### Phase 1: Deterministic Checks (High Confidence, No LLM Risk)

1. Create `src/superclaude/cli/roadmap/integration_contracts.py` (Solution 1)
2. Create `src/superclaude/cli/roadmap/anti_patterns.py` (Solution 3)
3. Add `_run_integration_audit()` to `executor.py` as a new pipeline step between `merge` and `spec-fidelity`
4. Add `check_all_anti_patterns()` as part of the integration audit step
5. Output: `integration-audit.md` with frontmatter fields:
   - `contracts_found: (integer)`
   - `contracts_covered: (integer)`
   - `contracts_uncovered: (integer)`
   - `anti_patterns_detected: (integer)`
   - `integration_ready: (boolean) true only if contracts_uncovered == 0 AND anti_patterns_detected == 0`

### Phase 2: Prompt Hardening (Defense in Depth)

6. Add `INTEGRATION_ENUMERATION_BLOCK` to `build_generate_prompt()` in `prompts.py` (Solution 2)
7. Add "Integration Wiring" as 6th comparison dimension in `build_spec_fidelity_prompt()` (Solution 2)

### Phase 3: Gate Integration

8. Add `INTEGRATION_AUDIT_GATE` to `gates.py`:
   ```python
   INTEGRATION_AUDIT_GATE = GateCriteria(
       required_frontmatter_fields=[
           "contracts_found",
           "contracts_covered",
           "contracts_uncovered",
           "anti_patterns_detected",
           "integration_ready",
       ],
       min_lines=10,
       enforcement_tier="STRICT",
       semantic_checks=[
           SemanticCheck(
               name="integration_ready_true",
               check_fn=_integration_ready_true,
               failure_message="integration_ready must be true; uncovered contracts or anti-patterns detected",
           ),
       ],
   )
   ```
9. Add to `ALL_GATES` list between `merge` and `spec-fidelity`

### Phase 4: Testing

10. Unit tests in `tests/roadmap/test_integration_contracts.py`:
    - Test pattern extraction against known spec text (including cli-portify verbatim)
    - Test coverage checking against known roadmap text (good and bad examples)
    - Test anti-pattern detection against known bad roadmaps
    - Regression test: the exact cli-portify spec/roadmap pair must trigger the uncovered contract warning

---

## Files Changed

| File | Change Type | Description |
|------|-------------|-------------|
| `src/superclaude/cli/roadmap/integration_contracts.py` | NEW | Integration contract extraction and coverage verification |
| `src/superclaude/cli/roadmap/anti_patterns.py` | NEW | Anti-pattern rule engine |
| `src/superclaude/cli/roadmap/executor.py` | MODIFY | Add integration audit step to pipeline |
| `src/superclaude/cli/roadmap/gates.py` | MODIFY | Add INTEGRATION_AUDIT_GATE |
| `src/superclaude/cli/roadmap/prompts.py` | MODIFY | Add integration enumeration block to generate prompt |
| `src/superclaude/cli/roadmap/prompts.py` | MODIFY | Add integration wiring dimension to spec-fidelity prompt |
| `tests/roadmap/test_integration_contracts.py` | NEW | Unit tests for contract extraction and coverage |
| `tests/roadmap/test_anti_patterns.py` | NEW | Unit tests for anti-pattern detection |

---

## Key Design Decisions

1. **Deterministic-first**: Solutions 1 and 3 are pure Python pattern matching with zero LLM involvement. They cannot be fooled by the same bias they are designed to catch.

2. **Defense in depth**: Solution 2 (prompt augmentation) is layered on top. If the deterministic checks miss a contract (novel naming convention), the prompt hardening provides a second line of defense.

3. **The audit step is NOT an LLM call**: The integration audit runs as a Python function, not a `claude -p` subprocess. This is critical: using an LLM to check for LLM blind spots reintroduces the same bias.

4. **Pattern library is extensible**: New dispatch patterns, wiring patterns, and anti-pattern rules can be added as they are discovered, without changing the pipeline structure.

5. **Fail-open initially, fail-closed later**: During rollout, uncovered contracts emit warnings. Once the pattern library is validated against real specs, switch to STRICT enforcement (fail-closed).

## Appendix: Pattern-Matching Trap Taxonomy

For reference, these are the categories of integration mechanisms that commonly fall through the "standard phasing" pattern:

| Category | Example | Why LLMs Miss It |
|----------|---------|-------------------|
| Dict dispatch | `RUNNERS = {"step": fn}` | Looks like a data structure, not a task |
| Plugin registry | `registry.register("name", cls)` | Registration call hidden in module init |
| Callback injection | `executor(on_step=callback)` | Wiring happens at call site, not definition |
| Strategy pattern | `Context(strategy=ConcreteStrategy())` | Instantiation is the wiring; not a separate "build" step |
| Middleware chain | `app.use(middleware_fn)` | Ordering matters; not just "implement middleware" |
| Event binding | `emitter.on("event", handler)` | Subscription is separate from handler implementation |
| DI container | `container.bind(Interface, Concrete)` | Binding configuration is a first-class artifact |

Each of these requires an explicit roadmap task because the "implementing the component" step does NOT automatically wire it into the system. The LLM's training data overwhelmingly shows cases where import-time side effects or framework magic handles the wiring -- but when the spec defines custom wiring, there is no magic.

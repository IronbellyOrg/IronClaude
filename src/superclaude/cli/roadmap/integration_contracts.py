"""Integration contract extraction and verification.

Extracts non-obvious integration points from spec text and verifies
each has an explicit corresponding task in the roadmap. Catches the
"pattern-matching trap" where LLMs assume standard skeleton->implement
phasing covers custom dispatch/wiring mechanisms.

Pure function: content in, findings out. No I/O.

Implements FR-MOD2.1 through FR-MOD2.6.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field


# --- FR-MOD2.1: 7-category dispatch pattern scanner with compiled regexes ---

DISPATCH_PATTERNS = [
    # Category 1: Dict dispatch tables
    re.compile(
        r"\b(?:dispatch[_\s]?table|RUNNERS|_RUNNERS|HANDLERS|"
        r"DISPATCH|routing[_\s]?table|command[_\s]?map|step[_\s]?map|"
        r"plugin[_\s]?registry)\b",
        re.IGNORECASE,
    ),
    # Category 2: Plugin registry / explicit wiring
    re.compile(
        r"\b(?:populate|register|wire|inject|bind|map|route)\s+"
        r"(?:the\s+|all\s+|each\s+)?"
        r"(?:implementations?|runners?|handlers?|plugins?|steps?|commands?)\b",
        re.IGNORECASE,
    ),
    # Category 3: Callback injection / constructor injection
    re.compile(
        r"\b(?:accepts?|takes?|requires?|expects?)\s+(?:a\s+)?"
        r"(?:Callable|Protocol|ABC|Interface|Factory|Provider|Registry)\b",
        re.IGNORECASE,
    ),
    # Category 3 (continued): Type annotations for dispatch
    re.compile(
        r"\b(?:Dict|Mapping|dict)\s*\[\s*str\s*,\s*(?:Callable|Awaitable|Coroutine)\b",
        re.IGNORECASE,
    ),
    # Category 4: Strategy pattern
    re.compile(
        r"\b(?:Context\s*\(\s*strategy\s*=|Strategy|ConcreteStrategy|"
        r"set_strategy|get_strategy)\b",
        re.IGNORECASE,
    ),
    # Category 5: Middleware chain
    re.compile(
        r"\b(?:middleware|app\.use|pipeline\.add|add_middleware|"
        r"use_middleware)\b",
        re.IGNORECASE,
    ),
    # Category 6: Event binding
    re.compile(
        r"\b(?:emitter\.on|addEventListener|subscribe|on_event|"
        r"event_handler|add_listener)\b",
        re.IGNORECASE,
    ),
    # Category 7: DI container
    re.compile(
        r"\b(?:container\.bind|container\.register|Provider|"
        r"Injector|inject_dependency|DependencyContainer)\b",
        re.IGNORECASE,
    ),
]

# FR-MOD2.3: Verb-anchored wiring task coverage patterns
WIRING_TASK_PATTERNS = [
    # Explicit creation/population of dispatch/registry mechanisms
    re.compile(
        r"\b(?:create|build|construct|populate|wire|assemble|register)\s+"
        r"(?:the\s+|a\s+)?"
        r"(?:dispatch|routing|registry|runner|handler|command|middleware|"
        r"event|strategy|plugin)\s*"
        r"(?:table|map|dict|registry|lookup|chain|binding|container)\b",
        re.IGNORECASE,
    ),
    # Explicit wiring of implementations into mechanisms
    re.compile(
        r"\b(?:wire|connect|bind|inject|register|plug)\s+.*?"
        r"(?:implementations?|runners?|handlers?|plugins?|strategies?|"
        r"middlewares?|listeners?)\s+"
        r"(?:into|to|with|in)\b",
        re.IGNORECASE,
    ),
    # FR-MOD2.4: Specific named mechanisms (UPPER_SNAKE_CASE, PascalCase)
    re.compile(
        r"\bPROGRAMMATIC_RUNNERS\b|\bDISPATCH_TABLE\b|\bHANDLER_REGISTRY\b|"
        r"\bMIDDLEWARE_CHAIN\b|\bEVENT_BINDINGS\b|\bROUTE_MAP\b",
    ),
    # Strategy/middleware/event-specific wiring verbs
    re.compile(
        r"\b(?:configure|set[_\s]up|initialize|bootstrap)\s+"
        r"(?:the\s+)?"
        r"(?:strategy|middleware|event\s+binding|DI\s+container|"
        r"dependency\s+injection|plugin\s+registry)\b",
        re.IGNORECASE,
    ),
]


# --- FR-MOD2.6: Dataclasses ---


@dataclass
class IntegrationContract:
    """A single integration point extracted from a spec."""

    id: str  # IC-001, IC-002, ...
    mechanism: str  # "dispatch_table", "registry", "injection", etc.
    spec_evidence: str  # verbatim quote from spec
    spec_location: str  # line number or section heading
    description: str  # human-readable description
    requires_explicit_wiring: bool  # True if cannot be implicit


@dataclass
class WiringCoverage:
    """Result of checking whether a contract is covered by roadmap tasks."""

    contract: IntegrationContract
    covered: bool
    roadmap_evidence: str  # quote from roadmap if covered, empty if not
    roadmap_location: str  # phase/task if covered


@dataclass
class IntegrationAuditResult:
    """Full audit result: all contracts and their coverage status."""

    contracts: list[IntegrationContract] = field(default_factory=list)
    coverage: list[WiringCoverage] = field(default_factory=list)
    uncovered_count: int = 0
    total_count: int = 0

    @property
    def all_covered(self) -> bool:
        """Returns True only when uncovered_contracts == 0."""
        return self.uncovered_count == 0


# --- Public API ---


def extract_integration_contracts(spec_text: str) -> list[IntegrationContract]:
    """Extract integration contracts from spec text using pattern matching.

    FR-MOD2.1: Scans spec text for 7-category dispatch patterns.
    FR-MOD2.2: Context capture (3 lines), mechanism classification,
               sequential ID assignment, deduplication.

    Returns a list of IntegrationContract instances.
    """
    contracts: list[IntegrationContract] = []
    lines = spec_text.splitlines()
    seen_evidence: set[str] = set()  # dedup by evidence line
    counter = 1

    for i, line in enumerate(lines):
        for pattern in DISPATCH_PATTERNS:
            match = pattern.search(line)
            if match:
                evidence = line.strip()
                if evidence in seen_evidence:
                    continue
                seen_evidence.add(evidence)

                # FR-MOD2.2: Context capture (3 lines before/after)
                context_start = max(0, i - 3)
                context_end = min(len(lines), i + 4)
                context = "\n".join(lines[context_start:context_end])

                mechanism = _classify_mechanism(match.group(0))
                contracts.append(
                    IntegrationContract(
                        id=f"IC-{counter:03d}",
                        mechanism=mechanism,
                        spec_evidence=context,
                        spec_location=f"line {i + 1}",
                        description=f"{mechanism}: {evidence}",
                        requires_explicit_wiring=True,
                    )
                )
                counter += 1

    return contracts


def check_roadmap_coverage(
    contracts: list[IntegrationContract],
    roadmap_text: str,
) -> IntegrationAuditResult:
    """Check whether each integration contract has explicit roadmap coverage.

    FR-MOD2.3: Verb-anchored wiring task coverage check.
    FR-MOD2.5: Wiring-task-specific coverage semantics — a contract is
    "covered" only if the roadmap contains a task that explicitly mentions
    creating, populating, or wiring the mechanism.

    Returns IntegrationAuditResult with all contracts and their coverage.
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

        # FR-MOD2.4: Also check for specific mechanism identifiers
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

        result.coverage.append(
            WiringCoverage(
                contract=contract,
                covered=covered,
                roadmap_evidence=evidence,
                roadmap_location=location,
            )
        )

        if not covered:
            result.uncovered_count += 1

    return result


# --- Internal helpers ---


def _classify_mechanism(matched_text: str) -> str:
    """Classify matched text into a mechanism category."""
    lower = matched_text.lower()
    if any(
        k in lower
        for k in ("dispatch", "runner", "handler", "command_map", "step_map")
    ):
        return "dispatch_table"
    if "registry" in lower or "register" in lower:
        return "registry"
    if any(
        k in lower
        for k in ("inject", "callable", "protocol", "factory", "provider")
    ):
        return "dependency_injection"
    if any(k in lower for k in ("wire", "bind", "populate")):
        return "explicit_wiring"
    if any(k in lower for k in ("route", "routing")):
        return "routing"
    if any(k in lower for k in ("strategy", "concretestrategy")):
        return "strategy_pattern"
    if any(k in lower for k in ("middleware", "app.use", "pipeline.add")):
        return "middleware_chain"
    if any(
        k in lower for k in ("emitter", "addeventlistener", "subscribe", "listener")
    ):
        return "event_binding"
    if any(k in lower for k in ("container", "injector", "dependencycontainer")):
        return "di_container"
    return "integration_point"


def _extract_identifiers(text: str) -> list[str]:
    """Extract UPPER_SNAKE_CASE and PascalCase identifiers from text.

    FR-MOD2.4: Named mechanism identifier matching.
    """
    # UPPER_SNAKE_CASE (likely constants/tables)
    upper_snake = re.findall(r"\b[A-Z][A-Z0-9_]{2,}\b", text)
    # PascalCase class names
    pascal = re.findall(r"\b[A-Z][a-z]+(?:[A-Z][a-z]+)+\b", text)
    return upper_snake + pascal

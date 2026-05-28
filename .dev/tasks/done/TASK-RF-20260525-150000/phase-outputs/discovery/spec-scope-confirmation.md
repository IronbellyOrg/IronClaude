# Spec Scope Confirmation — Fix B Merged

Source: `/config/workspace/IronClaude/.dev/troubleshoot/build-anti-instinct-uncovered-contracts-20260525141717/adversarial/merged-output.md`

Status: Spec re-read in full per Step 1.4. All verbatim code blocks below are copied byte-identical from merged-output.md.

---

## §2.1 Data Model Change — IN SCOPE

- **merged-output.md source:** lines 38-58
- **Target:** `src/superclaude/cli/roadmap/integration_contracts.py:113-122` (`IntegrationContract` dataclass)

**Verbatim code (from merged-output.md):**

```python
@dataclass
class IntegrationContract:
    id: str
    mechanism: str
    spec_evidence: str
    spec_location: str
    description: str
    requires_explicit_wiring: bool
    # NEW
    mechanism_signature: tuple[str, frozenset[str]] = field(
        default=(("", frozenset()))
    )
    # signature = (mechanism, frozenset of normalized identifiers)
```

Only the new field + inline comment are added. Existing 6 fields stay verbatim.

---

## §2.2 Tighten DISPATCH_PATTERNS[0] — IN SCOPE

- **merged-output.md source:** lines 64-84
- **Target:** `src/superclaude/cli/roadmap/integration_contracts.py:22-27` (DISPATCH_PATTERNS[0] regex)

**Verbatim code (from merged-output.md):**

```python
re.compile(
    r"\b(?:dispatch[_\s]?table|DISPATCH_TABLE|RUNNERS|_RUNNERS|HANDLERS|"
    r"routing[_\s]?table|command[_\s]?map|step[_\s]?map|"
    r"plugin[_\s]?registry|"
    # NEW: compound dispatch nouns — keeps mechanism semantics,
    # rejects bare "dispatch" in prose
    r"(?:[a-z]+-)?(?:class-priority|priority|named-theme|role-keyed|"
    r"theme|severity-keyed|module-tier|subprocess|gRPC)[\s_-]?dispatch"
    r")\b",
    re.IGNORECASE,
),
```

Drops bare `DISPATCH`; adds explicit `DISPATCH_TABLE` and the compound-noun arm.

---

## §2.3a New helper `_signature_subsumed` — IN SCOPE

- **merged-output.md source:** lines 144-161
- **Target:** `src/superclaude/cli/roadmap/integration_contracts.py` — append at end of `# --- Internal helpers ---` section (after `_extract_identifiers` at line 356)

**Verbatim code:**

```python
def _signature_subsumed(
    sig: tuple[str, frozenset[str]],
    seen: dict[tuple[str, frozenset[str]], int],
) -> bool:
    """Subsume sig if same mechanism AND identifier-set ⊆ an existing one
    that shares ≥1 identifier. Empty-identifier signatures dedup by exact
    match only (preserves test_duplicate_lines_deduplicated)."""
    mech, idents = sig
    if not idents:
        return sig in seen
    for (smech, sidents) in seen:
        if smech != mech:
            continue
        if idents and sidents and idents.issubset(sidents) and (idents & sidents):
            return True
        if idents == sidents:
            return True
    return False
```

---

## §2.3b Refactor `extract_integration_contracts` — IN SCOPE

- **merged-output.md source:** lines 96-141
- **Target:** `src/superclaude/cli/roadmap/integration_contracts.py:153-202` (body of `extract_integration_contracts`)

**Verbatim code:**

```python
def extract_integration_contracts(spec_text: str) -> list[IntegrationContract]:
    contracts: list[IntegrationContract] = []
    lines = spec_text.splitlines()
    seen_signatures: dict[tuple[str, frozenset[str]], int] = {}
    counter = 1

    for i, line in enumerate(lines):
        stripped = line.lstrip()
        if stripped.startswith("#") or stripped.startswith("- ["):
            continue

        for pattern in DISPATCH_PATTERNS:
            match = pattern.search(line)
            if not match:
                continue

            evidence = line.strip()
            context_start = max(0, i - 3)
            context_end = min(len(lines), i + 4)
            context = "\n".join(lines[context_start:context_end])

            mechanism = _classify_mechanism(match.group(0))
            idents = frozenset(_extract_identifiers(context))
            signature = (mechanism, idents)

            # Signature-based dedup — collapse contracts whose
            # (mechanism, identifier-set) is identical OR is a strict
            # subset of an already-seen signature.
            if _signature_subsumed(signature, seen_signatures):
                continue
            seen_signatures[signature] = counter

            contracts.append(IntegrationContract(
                id=f"IC-{counter:03d}",
                mechanism=mechanism,
                spec_evidence=context,
                spec_location=f"line {i + 1}",
                description=f"{mechanism}: {evidence}",
                requires_explicit_wiring=True,
                mechanism_signature=signature,
            ))
            counter += 1
            break  # one contract per line max

    return contracts
```

NOTE: Existing docstring of the function MUST be preserved (the body is replaced; the signature + docstring stay).

---

## §2.4 3-Layer FR-MOD2.7 Fallback — IN SCOPE

- **merged-output.md source:** lines 178-253
- **Target:** `src/superclaude/cli/roadmap/integration_contracts.py:254-297` (FR-MOD2.7 fallback block inside `check_roadmap_coverage`)

**Verbatim code:**

```python
if not covered:
    mechanism_term = contract.mechanism.replace("_", " ")
    raw_terms = [mechanism_term]
    if "middleware" in contract.description.lower():
        raw_terms.append("middleware")
    if "strategy" in contract.description.lower():
        raw_terms.append("strategy")

    # Layer 1: dispatch-family-specific tolerance (Opus base)
    dispatch_family = re.compile(
        r"\b(?:[a-z]+-)?(?:class-priority|priority|named-theme|"
        r"role-keyed|theme|severity-keyed|module-tier|subprocess|gRPC)"
        r"[\s_-]?dispatch(?:\s+table)?\b",
        re.IGNORECASE,
    )

    impl_verbs = re.compile(
        r"\b(?:implement|configure|add|create|set\s*up|deploy|"
        r"build|integrate|wire|enable|install|bound|attach|"
        r"apply|use|route|log|emit|handle|populate)\b",  # +populate (Opus)
        re.IGNORECASE,
    )

    # Layer 1+2: full-term and dispatch-family — same-line or 3-line window verb
    for j, rline in enumerate(roadmap_lines):
        hit_term = any(t.lower() in rline.lower() for t in raw_terms)
        hit_family = (
            contract.mechanism == "dispatch_table"
            and dispatch_family.search(rline)
        )
        if not (hit_term or hit_family):
            continue
        if impl_verbs.search(rline):
            covered = True; evidence = rline.strip()
            location = f"line {j + 1}"; break
        window_start = max(0, j - 2)
        window_end = min(len(roadmap_lines), j + 3)
        window_text = " ".join(roadmap_lines[window_start:window_end])
        if impl_verbs.search(window_text):
            covered = True; evidence = rline.strip()
            location = f"lines {window_start + 1}-{window_end}"; break

    # Layer 3 (NEW from Sonnet, with overlap guard from Sonnet's counter-arg
    # mitigation): generic stem fallback for ANY compound mechanism term.
    # SAME-LINE constraint AND identifier-overlap guard against the
    # contract's persisted mechanism_signature.
    if not covered:
        stem_terms: list[str] = []
        for mt in raw_terms:
            parts = mt.split()
            if len(parts) >= 2:
                stem_terms.append(parts[0])  # "dispatch" from "dispatch table"

        contract_idents = contract.mechanism_signature[1]  # frozenset
        for stem in stem_terms:
            for j, rline in enumerate(roadmap_lines):
                if stem.lower() not in rline.lower():
                    continue
                if not impl_verbs.search(rline):
                    continue
                # IDENTIFIER-OVERLAP GUARD: require at least one of the
                # contract's mechanism_signature identifiers to appear in
                # the matching line's 3-line window. Defeats the
                # "Implement priority dispatch for logging" false-positive
                # class (Sonnet's own counter-argument scenario).
                if contract_idents:
                    window_start = max(0, j - 2)
                    window_end = min(len(roadmap_lines), j + 3)
                    window_text = " ".join(roadmap_lines[window_start:window_end])
                    if not any(ident in window_text for ident in contract_idents):
                        continue
                covered = True; evidence = rline.strip()
                location = f"line {j + 1} (stem+overlap)"; break
            if covered: break
```

---

## §3 Test Methods t1-t7 — IN SCOPE (with RQ-1 Option A adaptations for t1/t6/t7)

- **merged-output.md source:** lines 298-361
- **Target:** `tests/roadmap/test_integration_contracts.py` — append `TestHubDispatchRegression` after `TestIntegrationAuditResult` (current line 276)

### t1 (RQ-1 ADAPTED — `FR-S10-02` instead of `Interactive`)

```python
def test_t1_one_contract_per_hub_mechanism(self):
    """4 epic lines mentioning hub dispatch → 1 IntegrationContract."""
    contracts = extract_integration_contracts(TUIBBS_HUB_SPEC)
    hub_contracts = [c for c in contracts
                     if c.mechanism == "dispatch_table"
                     and "FR-S10-02" in c.spec_evidence]  # RQ-1 Option A
    assert len(hub_contracts) == 1
```

### t2 (verbatim)

```python
def test_t2_class_priority_dispatch_covers_hub(self):
    """Roadmap phrase 'class-priority dispatch' covers hub contract."""
    contracts = extract_integration_contracts(TUIBBS_HUB_SPEC)
    result = check_roadmap_coverage(contracts, TUIBBS_HUB_ROADMAP)
    assert result.uncovered_count == 0
```

### t3 (verbatim)

```python
def test_t3_prose_dispatch_not_extracted_alone(self):
    """'priority dispatch cannot be undermined' in isolation yields ≤1 contract."""
    prose = "So that priority dispatch cannot be undermined by mis-tagged messages."
    contracts = extract_integration_contracts(prose)
    assert len(contracts) <= 1
```

### t4 (verbatim)

```python
def test_t4_existing_dispatch_table_test_still_passes(self):
    """DISPATCH_TABLE_SPEC still yields a dispatch_table contract."""
    contracts = extract_integration_contracts(DISPATCH_TABLE_SPEC)
    assert any(c.mechanism == "dispatch_table" for c in contracts)
```

### t5 (verbatim)

```python
def test_t5_cli_portify_regression_still_blocks(self):
    """SC-003 regression: PROGRAMMATIC_RUNNERS without wiring still uncovered."""
    contracts = extract_integration_contracts(CLI_PORTIFY_SPEC)
    result = check_roadmap_coverage(contracts, CLI_PORTIFY_BAD_ROADMAP)
    assert result.uncovered_count >= 1
```

### t6 (RQ-1 ADAPTED — `FR-S10-02` instead of `Interactive`)

```python
def test_t6_stem_fallback_with_ident_overlap_covers(self):
    """Roadmap with 'Implement ... class-priority dispatch' + FR-S10-02 in window covers hub contract."""
    spec = (
        "The hub uses class-priority dispatch — FR-S10-02 is the relevant requirement.\n"
        "Default dispatch order is strict.\n"
    )
    roadmap = (
        "## M5\n"
        "Implement the message hub with typed class-priority dispatch.\n"
        "FR-S10-02 messages take priority over others.\n"
    )
    contracts = extract_integration_contracts(spec)
    result = check_roadmap_coverage(contracts, roadmap)
    assert result.uncovered_count == 0
```

### t7 (RQ-1 ADAPTED — `FR-S10-02` instead of `Interactive`)

```python
def test_t7_stem_fallback_without_ident_overlap_uncovers(self):
    """'Implement priority dispatch for logging' must NOT cover hub contract because no identifier overlap with the contract's signature."""
    spec = (
        "The hub uses class-priority dispatch — FR-S10-02 is the relevant requirement.\n"
    )
    roadmap = (
        "## M5\n"
        "Implement priority dispatch for logging events.\n"
        "Configure debug log levels and rotation.\n"
    )
    contracts = extract_integration_contracts(spec)
    result = check_roadmap_coverage(contracts, roadmap)
    # No FR-S10-02 in the roadmap → stem-fallback identifier-overlap guard rejects the match → contract uncovered.
    assert result.uncovered_count >= 1
```

---

## §7 Merge-step prompt blindness — OUT OF SCOPE

Per RQ-2: Captured as a separate follow-up task file in Step 5.4. Not implemented in this task.

---

**Scope locked: 4 sub-changes + 7 tests + 2 fixtures.**

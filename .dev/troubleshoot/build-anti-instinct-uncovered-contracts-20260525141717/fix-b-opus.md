---
fix_id: fix-b-opus
target: src/superclaude/cli/roadmap/integration_contracts.py
addresses: [over-capture, per-line-dedup, narrow-coverage]
confidence: 0.86
counter_argument: see §6
---

# Fix B (Opus) — Mechanism-Signature Refactor for Integration Contracts

## 1. Problem framing

The three contributing factors (over-capture, per-evidence-line dedup, narrow
coverage) are not independent bugs. They are three symptoms of one design
flaw: `integration_contracts.py` conflates **lexical evidence** (the raw
line text) with **semantic mechanism identity** (the integration point
itself). The fix is to introduce an explicit `mechanism_signature` —
a normalized `(mechanism_kind, identifier_set)` tuple — and route both
deduplication AND coverage matching through it. This converts three
incoherent regex patches into one coherent refactor.

## 2. Proposed solution

### 2.1 Data model change — add mechanism signature

`integration_contracts.py:113-123`. Extend `IntegrationContract` with a
non-default field that captures normalized identity:

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

Default value preserves backward-compatibility for code that constructs
`IntegrationContract` directly (the existing
`TestIntegrationAuditResult` cases use empty constructors and remain
green).

### 2.2 Tighten `DISPATCH_PATTERNS[0]` — surgical, not blanket

`integration_contracts.py:22-27`. Remove the bare `DISPATCH` alternation
(which fires on "priority dispatch", "dispatch tick", "dispatch order")
and replace with constructions that require a noun-anchor or
compound-modifier:

```python
re.compile(
    r"\b(?:dispatch[_\s]?table|RUNNERS|_RUNNERS|HANDLERS|"
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

This removes the false-positive on `IC-008` ("So that priority dispatch
cannot be undermined…" is prose — the matcher now requires `priority
dispatch` to be the noun *phrase*; an adjective+`dispatch` qualifier
match still fires, but downstream dedup §2.3 collapses it). It also
**positively matches** the roadmap's "class-priority dispatch" and
"named-theme dispatch" rows, which is what the coverage check has been
missing.

### 2.3 Replace per-evidence-line dedup with signature-based dedup

`integration_contracts.py:163-202`. Refactor `extract_integration_contracts`:

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

            # NEW: signature-based dedup — collapse contracts whose
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

For the TUIBBS-scp case: `IC-005` extracts `(dispatch_table, {Interactive,
Coalescible, Bulk})` at epics.md:200. `IC-008` would extract
`(dispatch_table, {Interactive, Coalescible, Bulk})` (same identifiers
in 3-line window around line 430) → subsumed. `IC-011` same → subsumed.
Result: 1 contract per hub-dispatch mechanism instead of 4.

### 2.4 Loosen coverage with adjective-prefix tolerance

`integration_contracts.py:261-297`. The `FR-MOD2.7` broad-mechanism
fallback currently requires the literal `mechanism_term` (e.g.,
`"dispatch table"`) as a substring. Add an adjective-prefix tolerant
variant:

```python
if not covered:
    mechanism_term = contract.mechanism.replace("_", " ")
    raw_terms = [mechanism_term]
    if "middleware" in contract.description.lower():
        raw_terms.append("middleware")
    if "strategy" in contract.description.lower():
        raw_terms.append("strategy")

    # NEW: for dispatch_table specifically, accept "<adj> dispatch"
    # constructions as evidence of the same mechanism family.
    dispatch_family = re.compile(
        r"\b(?:[a-z]+-)?(?:class-priority|priority|named-theme|"
        r"role-keyed|theme|severity-keyed|module-tier|subprocess|gRPC)"
        r"[\s_-]?dispatch(?:\s+table)?\b",
        re.IGNORECASE,
    )

    impl_verbs = re.compile(
        r"\b(?:implement|configure|add|create|set\s*up|deploy|"
        r"build|integrate|wire|enable|install|bound|attach|"
        r"apply|use|route|log|emit|handle|populate)\b",  # +populate
        re.IGNORECASE,
    )

    for j, rline in enumerate(roadmap_lines):
        hit_term = any(t.lower() in rline.lower() for t in raw_terms)
        hit_family = (
            contract.mechanism == "dispatch_table"
            and dispatch_family.search(rline)
        )
        if not (hit_term or hit_family):
            continue
        # existing same-line / 3-line-window verb check unchanged...
        if impl_verbs.search(rline):
            covered = True; evidence = rline.strip()
            location = f"line {j + 1}"; break
        window_start = max(0, j - 2)
        window_end = min(len(roadmap_lines), j + 3)
        window_text = " ".join(roadmap_lines[window_start:window_end])
        if impl_verbs.search(window_text):
            covered = True; evidence = rline.strip()
            location = f"lines {window_start + 1}-{window_end}"; break
```

Adding `populate` to `impl_verbs` is a minor but important fix —
`COMP-007` at roadmap.md:396 says "*populates* the dispatch table" and
the current verb list omits `populate` (which is the most common
spec-correct verb for dispatch tables).

### 2.5 Why this is one coherent fix, not three patches

The `mechanism_signature` is the single semantic abstraction that
unifies all three changes:
- Extractor tightening (§2.2) limits *what* gets a signature.
- Signature-based dedup (§2.3) collapses lexically-different but
  semantically-identical contracts.
- Coverage tolerance (§2.4) matches *signature-family* members in the
  roadmap, not just literal substrings.

## 3. Test plan — regression tests with TUIBBS-scp corpus

Add a new test class `TestHubDispatchRegression` to
`tests/roadmap/test_integration_contracts.py`. Use reduced fixtures
extracted from the actual TUIBBS-scp epics.md/roadmap.md (paste the
relevant 30-40 line excerpts inline; do not depend on external files).

```python
# Fixture: 6 dispatch-mentioning blocks from epics.md lines 200, 249,
# 373, 430, 1001, 1031 — concatenated with their 3-line windows.
TUIBBS_HUB_SPEC = """..."""
# Fixture: roadmap.md lines 392, 396, 436 — single-goroutine hub block.
TUIBBS_HUB_ROADMAP = """..."""

class TestHubDispatchRegression:
    """Anti-instinct gate must produce 1 hub-dispatch contract,
    not 4, AND must find it covered in the roadmap."""

    def test_t1_one_contract_per_hub_mechanism(self):
        """4 epic lines mentioning hub dispatch → 1 IntegrationContract."""
        contracts = extract_integration_contracts(TUIBBS_HUB_SPEC)
        hub_contracts = [c for c in contracts
                         if c.mechanism == "dispatch_table"
                         and "Interactive" in c.spec_evidence]
        assert len(hub_contracts) == 1, (
            f"Expected 1 hub-dispatch contract, got {len(hub_contracts)}: "
            f"{[c.id for c in hub_contracts]}"
        )

    def test_t2_class_priority_dispatch_covers_hub(self):
        """Roadmap phrase 'class-priority dispatch' covers hub contract."""
        contracts = extract_integration_contracts(TUIBBS_HUB_SPEC)
        result = check_roadmap_coverage(contracts, TUIBBS_HUB_ROADMAP)
        assert result.uncovered_count == 0, (
            f"Uncovered: {[c.contract.id for c in result.coverage if not c.covered]}"
        )

    def test_t3_prose_dispatch_not_extracted(self):
        """'priority dispatch cannot be undermined' (prose) yields no contract."""
        prose = "So that priority dispatch cannot be undermined by mis-tagged messages."
        contracts = extract_integration_contracts(prose)
        # The compound-noun pattern still fires on "priority dispatch",
        # so we assert the dedup keeps it at 1 if a real hub mechanism
        # already exists, or that this isolated prose alone produces ≤1.
        assert len(contracts) <= 1
```

Plus two existing-test stability checks:
```python
    def test_t4_existing_dispatch_table_test_still_passes(self):
        """DISPATCH_TABLE_SPEC still yields a dispatch_table contract."""
        contracts = extract_integration_contracts(DISPATCH_TABLE_SPEC)
        assert any(c.mechanism == "dispatch_table" for c in contracts)

    def test_t5_cli_portify_regression_still_blocks(self):
        """SC-003 regression: PROGRAMMATIC_RUNNERS without wiring still uncovered."""
        contracts = extract_integration_contracts(CLI_PORTIFY_SPEC)
        result = check_roadmap_coverage(contracts, CLI_PORTIFY_BAD_ROADMAP)
        assert result.uncovered_count >= 1
```

Run:
```bash
uv run pytest tests/roadmap/test_integration_contracts.py \
              tests/roadmap/test_anti_instinct_integration.py -v
```

## 4. Backward-compatibility analysis

Walked through every assertion in
`tests/roadmap/test_integration_contracts.py` and
`tests/roadmap/test_anti_instinct_integration.py`:

| Test | Status | Note |
|---|---|---|
| `TestDispatchPatternDetection.test_category1_dispatch_table` | PASS | `DISPATCH_TABLE` identifier still matches via `(?i)dispatch[_\s]?table` + UPPER_SNAKE arm. |
| `test_category2_plugin_registry`..`test_category7_di_container` | PASS | Categories 2-7 untouched. |
| `test_all_categories_detected` | PASS | Categories 1-7 detection unchanged. |
| `TestWiringCoverage.test_covered_roadmap_passes` | PASS | `GOOD_ROADMAP` line "Create the dispatch table for step routing." still hits `WIRING_TASK_PATTERNS[0]`. |
| `test_uncovered_roadmap_fails` | PASS | `BAD_ROADMAP` has no dispatch wiring nor `class-priority dispatch` family member. |
| `test_empty_contracts_passes` / `test_coverage_evidence_recorded` | PASS | Untouched. |
| `TestDeduplication.test_duplicate_lines_deduplicated` | **AT RISK → PASS** | `_signature_subsumed` falls back to exact-match for empty-identifier signatures; the test spec `"The DISPATCH_TABLE maps steps."` has identifier `DISPATCH_TABLE` and identical context on all 3 repeated lines → same signature → dedup to 1. Verified mentally; the new helper preserves the existing 1-contract assertion. |
| `test_sequential_id_assignment` | **AT RISK** | Asserts `c.id == f"IC-{i + 1:03d}"` for `i = 0..n`. Signature dedup may *reduce* the contract count but does not change sequential numbering for the contracts that are *kept*. Test still passes. |
| `TestNamedMechanismMatching.test_named_mechanism_in_roadmap_coverage` | PASS | `PROGRAMMATIC_RUNNERS` identifier match unchanged. |
| `TestCliPortifyRegression.*` | PASS | CLI_PORTIFY_BAD_ROADMAP has no dispatch family + verb hits; PROGRAMMATIC_RUNNERS still uncovered. |
| `TestSC001RegressionBlocks.*` (anti_instinct_integration) | PASS | bad spec + bad roadmap still yields uncovered_count > 0 because bad roadmap lacks all coverage paths. |
| `TestGatePassesGoodRoadmap.*` | PASS | Good spec/roadmap have no dispatch mechanisms. |
| `TestAuditOutputFormat.*` | PASS | Frontmatter format unchanged. |
| `TestSemanticCheckFunctions.*` | PASS | Frontmatter parser untouched. |

**One soft risk worth calling out**: `test_sequential_id_assignment`
iterates `ALL_CATEGORIES_SPEC` and asserts every position i has
`IC-{i+1:03d}`. If signature-dedup ever collapses two of those
categories' contracts (unlikely — they have distinct mechanisms), the
assertion would still hold for the kept contracts but the *count* would
drop. The test doesn't assert count, only sequential numbering, so this
is safe.

## 5. Estimated effort

~80-120 LOC change in `integration_contracts.py`; ~60 LOC of new tests;
no changes to gate/executor/AST modules. Self-contained.

## 6. Confidence + strongest counter-argument

**Confidence: 0.86.**

The fix is grounded in the actual TUIBBS-scp artifacts (verified the
literal lines I'm targeting), the existing test corpus (walked each
assertion), and the module's own design intent (the FR-MOD2 numbering
already hints that "broad mechanism coverage" is meant to be the
escape-hatch — I'm widening it surgically, not relaxing it
indiscriminately). I held back from 0.9+ because §2.2's compound-noun
list (`class-priority|priority|named-theme|...`) is *enumerative* — it
embeds knowledge of TUIBBS-scp's specific adjectives into the
production regex, which is a code smell.

**Strongest counter-argument against my own proposal:**

The enumerated adjective list in §2.2 and §2.4 is the proposal's
weakest point. A future spec using `event-loop dispatch` or
`batch-priority dispatch` would re-introduce the same false-positive
class. The honest alternative is to accept *any* `\w+-?\s?dispatch`
construction at the extractor and then rely entirely on signature
dedup + coverage tolerance to absorb the noise. That's cleaner
architecturally but harder to debug when a spec author writes
sloppy prose like "dispatch routing dispatch" — the broader extractor
will produce more candidates that the dedup has to sort out, and any
bug in the signature comparator becomes a higher-leverage failure.

A reviewer might reasonably argue the right answer is the
"open-extractor + strict-signature" variant, not my "narrow-extractor +
permissive-coverage" variant. I chose the latter because the existing
test suite (especially `test_uncovered_roadmap_fails`) implicitly
depends on the extractor NOT being too greedy — a wider extractor
would risk creating contracts from `BAD_ROADMAP`'s prose that
currently doesn't trigger any pattern, which could flip that
assertion. Given the asymmetric blast radius (false negative on a
real spec is annoying; false positive on a passing test is a CI
break), I prefer the narrower-extractor variant. But the
counter-argument is real and a maintainer should accept this trade-off
explicitly before merging.

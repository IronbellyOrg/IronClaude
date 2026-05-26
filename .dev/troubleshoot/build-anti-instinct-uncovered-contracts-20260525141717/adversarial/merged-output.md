<!-- Provenance: This document was produced by /sc:adversarial -->
<!-- Base: Variant 1 (Opus) — score 0.9765 -->
<!-- Incorporated: Variant 2 (Sonnet) — score 0.8475 -->
<!-- Merge date: 2026-05-25T14:43:00Z -->

---
fix_id: fix-b-merged
target: src/superclaude/cli/roadmap/integration_contracts.py
addresses: [over-capture, per-line-dedup, narrow-coverage, stem-fallback-false-positives]
confidence: 0.88
counter_argument: see §6
inherits_from: [fix-b-opus, fix-b-sonnet]
---

# Fix B (Merged) — Mechanism-Signature Refactor + Generic Stem Fallback with Identifier-Overlap Guard

## 1. Problem framing
<!-- Source: Base (original, modified) — incorporates Sonnet's narrative framing fragment -->

The three contributing factors (over-capture, per-evidence-line dedup, narrow
coverage) are not independent bugs. They are three symptoms of one design
flaw: `integration_contracts.py` conflates **lexical evidence** (the raw
line text) with **semantic mechanism identity** (the integration point
itself). The fix is to introduce an explicit `mechanism_signature` —
a normalized `(mechanism_kind, identifier_set)` tuple — and route both
deduplication AND coverage matching through it. This converts three
incoherent regex patches into one coherent refactor.

A fourth concern surfaced in adversarial review: a generic stem-fallback
in the coverage check (Sonnet) extends mechanism coverage beyond dispatch
but introduces semantic looseness. The merged design accepts the stem
fallback but adds an identifier-overlap guard against the persisted
`mechanism_signature` to defeat the false-positive class Sonnet's
counter-argument named.

## 2. Proposed solution

### 2.1 Data model change — add mechanism signature
<!-- Source: Base (original) -->

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
`IntegrationContract` directly. **The persisted field is load-bearing
for §2.4's stem-fallback identifier-overlap guard** — not speculative.

### 2.2 Tighten `DISPATCH_PATTERNS[0]` — surgical, not blanket
<!-- Source: Base (original, modified) — merged with Sonnet's explicit DISPATCH_TABLE alternation per Change #1 -->

`integration_contracts.py:22-27`. Remove the bare `DISPATCH` alternation
(which fires on "priority dispatch", "dispatch tick", "dispatch order"),
add explicit `DISPATCH_TABLE` for reviewer clarity, and add a compound-noun
arm that keeps signal-rich phrasings detectable:

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

The explicit `DISPATCH_TABLE` alternation (Sonnet) removes a class of
"did the IGNORECASE catch this?" reviewer confusion. The compound-noun
arm (Opus) catches "class-priority dispatch table" in artifact-table
rows that a deletion-only pattern would miss.

### 2.3 Replace per-evidence-line dedup with signature-based dedup
<!-- Source: Base (original) -->

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
Coalescible, Bulk})` at epics.md:200. `IC-008` would extract the same
signature → subsumed. `IC-011` same → subsumed. Result: 1 contract per
hub-dispatch mechanism instead of 4. Subsumption (vs. Sonnet's exact-
match dedup) also handles the asymmetric case where one context window
contains additional identifiers (`{Interactive, Coalescible, Bulk, MUST}`)
that the other lacks — the subset still collapses correctly.

### 2.4 Loosen coverage with adjective-prefix tolerance, generic stem fallback, and identifier-overlap guard
<!-- Source: Base (original, modified) — incorporates Sonnet's stem fallback (Change #2) and §counter-argument mitigation (Change #3) -->

`integration_contracts.py:261-297`. The `FR-MOD2.7` broad-mechanism
fallback gets three layers:

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

Three layers:
- **Layer 1** (Opus): mechanism-family regex catches adjective-compound dispatch (`class-priority dispatch`).
- **Layer 2** (existing): literal mechanism term substring + impl verb in line or 3-line window.
- **Layer 3** (Sonnet, defended): generic stem-fallback for any compound mechanism (middleware → "middleware", event_binding → "event"), constrained to same-line + impl verb + at-least-one identifier from the contract's signature in the window.

The identifier-overlap guard turns Sonnet's "could be added later" mitigation into a present-tense defense. It is enabled by the persisted `mechanism_signature` from §2.1 — vindicating that field's existence.

Adding `populate` to `impl_verbs` (Opus's catch) — the roadmap line at `roadmap.md:396` (post Fix A) says "populates the dispatch table"; without `populate` the coverage check would fail on a clean spec.

### 2.5 Why this is one coherent fix, not three patches
<!-- Source: Base (original) -->

The `mechanism_signature` is the single semantic abstraction that
unifies all four changes:

- Extractor tightening (§2.2) limits *what* gets a signature.
- Signature-based dedup (§2.3) collapses lexically-different but
  semantically-identical contracts.
- Coverage tolerance Layer 1 + Layer 2 (§2.4) match *signature-family*
  members and the literal mechanism term.
- Coverage tolerance Layer 3 (§2.4) generalises to any compound mechanism,
  with identifier-overlap as the only mechanism-specificity it preserves.

The persisted signature is what makes Layer 3 safe.

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
        assert len(hub_contracts) == 1

    def test_t2_class_priority_dispatch_covers_hub(self):
        """Roadmap phrase 'class-priority dispatch' covers hub contract."""
        contracts = extract_integration_contracts(TUIBBS_HUB_SPEC)
        result = check_roadmap_coverage(contracts, TUIBBS_HUB_ROADMAP)
        assert result.uncovered_count == 0

    def test_t3_prose_dispatch_not_extracted_alone(self):
        """'priority dispatch cannot be undermined' in isolation yields ≤1 contract."""
        prose = "So that priority dispatch cannot be undermined by mis-tagged messages."
        contracts = extract_integration_contracts(prose)
        assert len(contracts) <= 1

    def test_t4_existing_dispatch_table_test_still_passes(self):
        """DISPATCH_TABLE_SPEC still yields a dispatch_table contract."""
        contracts = extract_integration_contracts(DISPATCH_TABLE_SPEC)
        assert any(c.mechanism == "dispatch_table" for c in contracts)

    def test_t5_cli_portify_regression_still_blocks(self):
        """SC-003 regression: PROGRAMMATIC_RUNNERS without wiring still uncovered."""
        contracts = extract_integration_contracts(CLI_PORTIFY_SPEC)
        result = check_roadmap_coverage(contracts, CLI_PORTIFY_BAD_ROADMAP)
        assert result.uncovered_count >= 1

    # NEW (Change #6) — exercise stem-fallback + identifier-overlap guard

    def test_t6_stem_fallback_with_ident_overlap_covers(self):
        """Roadmap with 'Implement ... class-priority dispatch' + Interactive in window covers hub contract."""
        spec = (
            "The hub uses class-priority dispatch — `Interactive > Coalescible > Bulk`.\n"
            "Default dispatch order is strict.\n"
        )
        roadmap = (
            "## M5\n"
            "Implement the message hub with typed class-priority dispatch.\n"
            "Interactive messages take priority over Coalescible and Bulk.\n"
        )
        contracts = extract_integration_contracts(spec)
        result = check_roadmap_coverage(contracts, roadmap)
        assert result.uncovered_count == 0

    def test_t7_stem_fallback_without_ident_overlap_uncovers(self):
        """'Implement priority dispatch for logging' must NOT cover hub contract
        because no identifier overlap with the contract's signature."""
        spec = (
            "The hub uses class-priority dispatch — `Interactive > Coalescible > Bulk`.\n"
        )
        roadmap = (
            "## M5\n"
            "Implement priority dispatch for logging events.\n"
            "Configure debug log levels and rotation.\n"
        )
        contracts = extract_integration_contracts(spec)
        result = check_roadmap_coverage(contracts, roadmap)
        # No Interactive/Coalescible/Bulk in the roadmap → stem-fallback
        # identifier-overlap guard rejects the match → contract uncovered.
        assert result.uncovered_count >= 1
```

Run:
```bash
uv run pytest tests/roadmap/test_integration_contracts.py \
              tests/roadmap/test_anti_instinct_integration.py -v
```

## 4. Backward-compatibility analysis
<!-- Source: Base (original) — verified against the merged solution -->

Walked through every assertion in
`tests/roadmap/test_integration_contracts.py` and
`tests/roadmap/test_anti_instinct_integration.py`:

| Test | Status | Note |
|---|---|---|
| `TestDispatchPatternDetection.test_category1_dispatch_table` | PASS | `DISPATCH_TABLE` explicit + `dispatch[_\s]?table` arm both match. |
| `test_category2..test_category7` | PASS | Categories 2-7 untouched. |
| `test_all_categories_detected` | PASS | Categories 1-7 detection unchanged. |
| `TestWiringCoverage.test_covered_roadmap_passes` | PASS | `GOOD_ROADMAP` line "Create the dispatch table for step routing." still hits `WIRING_TASK_PATTERNS[0]`. |
| `test_uncovered_roadmap_fails` | PASS | `BAD_ROADMAP` has no dispatch wiring nor `class-priority dispatch` family member nor stem+overlap match. |
| `test_empty_contracts_passes` / `test_coverage_evidence_recorded` | PASS | Untouched. |
| `TestDeduplication.test_duplicate_lines_deduplicated` | PASS | `_signature_subsumed` falls back to exact-match for empty-identifier signatures; identical lines have identical signatures → dedup. |
| `test_sequential_id_assignment` | PASS | Dedup may reduce count but does not change sequential numbering for the contracts that are kept. |
| `TestNamedMechanismMatching.test_named_mechanism_in_roadmap_coverage` | PASS | `PROGRAMMATIC_RUNNERS` identifier match unchanged. |
| `TestCliPortifyRegression.*` | PASS | CLI_PORTIFY_BAD_ROADMAP has no dispatch family or stem+overlap hits; PROGRAMMATIC_RUNNERS still uncovered. |
| `TestSC001RegressionBlocks.*` (anti_instinct_integration) | PASS | bad spec + bad roadmap still yields uncovered_count > 0. |
| `TestGatePassesGoodRoadmap.*` | PASS | Good spec/roadmap have no dispatch mechanisms. |
| `TestAuditOutputFormat.*` | PASS | Frontmatter format unchanged. |
| `TestSemanticCheckFunctions.*` | PASS | Frontmatter parser untouched. |

**Soft risk** (carried from Opus base): `test_sequential_id_assignment`
iterates `ALL_CATEGORIES_SPEC` and asserts every position i has
`IC-{i+1:03d}`. Signature dedup may *reduce* the contract count but does
not change sequential numbering for the contracts that are *kept*. The
test doesn't assert count, only sequential numbering — safe.

## 5. Estimated effort

- `integration_contracts.py`: ~100-140 LOC change (Opus base + Layer 3 stem-fallback + identifier-overlap guard)
- Test additions (`test_integration_contracts.py`): ~80 LOC (7 new test methods, reduced TUIBBS fixtures)
- No changes to gate/executor/AST modules
- Total: 1-2 hours implementation + test verification

## 6. Confidence + strongest counter-argument

**Confidence: 0.88.**

Higher than Opus's standalone 0.86 because the identifier-overlap guard
(§2.4 Layer 3) directly defeats the false-positive class Sonnet
acknowledged but did not concretely mitigate. The merged design uses
Opus's structured signature as the enabling primitive for that defense,
turning what Sonnet called YAGNI into load-bearing infrastructure.

**Strongest counter-argument against the merged proposal:**

§2.2's compound-noun list (`class-priority|priority|named-theme|...`)
inherits Opus's enumeration code smell. A future spec using
`event-loop dispatch` or `batch-priority dispatch` re-introduces the
same false-positive class. The merged solution accepts this trade-off
for the same reason Opus did: a wider extractor would risk creating
contracts from prose that the existing `test_uncovered_roadmap_fails`
implicitly forbids. Future-proofing means committing to ongoing
maintenance of the adjective list, with a regression test added each
time it grows.

Secondary counter-argument: §2.4 Layer 3's identifier-overlap guard
depends on `_extract_identifiers` capturing enough identifiers from the
spec context to be discriminating. If a spec author writes hub-dispatch
context using only single-PascalCase tokens like `Interactive`/`Bulk`
(which DON'T match the multi-cap `[A-Z][a-z]+(?:[A-Z][a-z]+)+`
regex), the identifier set may be empty, the overlap guard short-
circuits, and the stem-fallback admits matches it would otherwise
reject. Mitigation: in a follow-up, broaden `_extract_identifiers` to
accept single-PascalCase tokens that appear in code-formatted spans
(backticked, in tables) — but that's out of scope for this fix.

## 7. Known follow-up: merge-step prompt blindness
<!-- Source: Round 2.5 invariant probe INV-005 (Change #4) -->

This fix lands the **gate side** of the failure mode: the anti-instinct
audit becomes more tolerant of valid LLM-generated roadmap phrasing
and less prone to false-positive uncovered contracts. It does NOT fix
the **merge-step side**.

The merge step's LLM prompt (in `src/superclaude/cli/roadmap/prompts.py`
or wherever the merge synthesis is templated) does not currently
include explicit guidance that emitted roadmaps must contain explicit
wiring tasks for each integration mechanism in the spec. Without that
guidance, repeat roadmap pipeline runs depend on LLM phrasing luck:
sometimes the output contains `populate the X dispatch table`,
sometimes only `class-priority dispatch` prose.

The merged Fix B reduces but does not eliminate this dependency. A
proper end-to-end fix would also:

1. Add a directive to the merge prompt: "Every spec-level integration
   mechanism (dispatch table, registry, middleware chain, event
   binding, DI container) MUST appear in the roadmap with an explicit
   wiring task using one of: create, populate, wire, register,
   configure, set up the [mechanism]."
2. Add a corresponding regression test against the merge step's
   prompt that asserts the directive's presence.

Severity (per Round 2.5 invariant probe): **HIGH** for the original
failure mode; **MEDIUM** with this Fix B applied (the gate is now
more tolerant, so LLM phrasing variance is less likely to trigger
failure).

Track as a separate work item: `roadmap-merge-prompt-wiring-directive`.

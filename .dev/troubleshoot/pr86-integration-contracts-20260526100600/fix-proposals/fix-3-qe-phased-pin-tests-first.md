# Tier 2 Hypothesis — Quality Engineer (test fidelity + regression safety)

**Author**: quality-engineer (Wave 3, parallel)
**Tier**: 2
**Angle**: test fidelity, regression safety, fixture-vs-extractor mismatch
**Scope**: `src/superclaude/cli/roadmap/integration_contracts.py` @ PR #86 sha `67ab0af5`
**PR**: <https://github.com/IronbellyOrg/IronClaude/pull/86>

---

## Claim

PR #86's test suite **silently validates the wrong invariant** in three of its
seven new `TestHubDispatchRegression` cases because the fixture comment
(`FR-S10-02` "UPPER_SNAKE token") does not describe what `_extract_identifiers`
actually produces (`{'S10'}`). The quality risk is **not** that tests fail —
they pass — but that the green bar provides **false assurance** that
mechanism-signature dedup and Layer-3 identifier-overlap behave correctly for
hyphenated requirement IDs. Worse: a future "obvious" fix to F1 (broaden the
extractor to capture `FR-S10-02`) will leave every existing assertion still
green by accident (because `S10` is also a substring of `FR-S10-02` and the
Layer-2/Layer-3 guards do substring matching, not set-membership), so the
test suite **cannot distinguish "fix worked" from "fix had no observable
effect"**. This is the asymmetric failure mode the Tier 1 card under-weights:
the cluster's most dangerous risk is not the production bugs themselves, but
the test suite's inability to detect whether the bugs are fixed or merely
masked.

The proposed fix therefore re-baselines the test suite *first* with
behavior-pinning assertions that nail down what the extractor returns
(`assert set(_extract_identifiers(...)) == {...}`), *then* ships the
production change, *then* updates assertions to the new expected set. Each
phase produces an independently-verifiable diff.

## Evidence (PR sha `67ab0af5`)

### Fixture-vs-extractor mismatch is structural, not cosmetic

- `tests/roadmap/test_integration_contracts.py:130-134` (PR sha) — comment
  claims `FR-S10-02` is a single UPPER_SNAKE token threaded through every
  context window for `_signature_subsumed` to fire.
- `src/superclaude/cli/roadmap/integration_contracts.py:410-419` (PR sha) —
  `_extract_identifiers` regex `\b[A-Z][A-Z0-9_]{2,}\b` tokenizes
  `FR-S10-02` as `['S10']` only (`FR` rejected at `{2,}`, `02` rejected at
  `[A-Z]` anchor). Verified by direct regex execution against the fixture
  string: `re.findall(r'\b[A-Z][A-Z0-9_]{2,}\b', 'FR-S10-02') == ['S10']`.
- Every dispatch-hit line (indices 5, 6, 10, 11, 14, 15, 18, 20 in
  `TUIBBS_HUB_SPEC`) produces a 7-line context window whose
  `_extract_identifiers` output is exactly `{'S10'}`. The dedup-collapse to
  1 contract in `test_t1_one_contract_per_hub_mechanism` happens via the
  `S10` fragment — not the `FR-S10-02` ID the comment advertises.

### Test cases that silently validate the wrong thing

1. **`test_t1_one_contract_per_hub_mechanism`** (lines 260-268 PR sha) —
   asserts `len(hub_contracts) == 1` AND filters by
   `"FR-S10-02" in c.spec_evidence`. The substring filter is satisfied
   because the *evidence text* (raw context lines) contains the literal
   `FR-S10-02`. But the dedup that produces `== 1` is driven by `{'S10'}`
   signature equality, **not** the `FR-S10-02` identifier the comment
   claims. If `_extract_identifiers` were patched to return `{}` for this
   fixture (e.g. someone tightens the regex), dedup would still collapse
   to 1 via the empty-idents `sig in seen` exact-match branch on
   line 432-433 — the test would still pass for the wrong reason.

2. **`test_t6_stem_fallback_with_ident_overlap_covers`** (lines 309-322 PR
   sha) — asserts coverage via Layer 3 identifier-overlap. The literal
   substring check on line 355 (`if not any(ident in window_text for
   ident in contract_idents)`) succeeds because `'S10' in
   'FR-S10-02 messages...'`. If F1 fix changes idents to
   `{'FR-S10-02'}` only (dropping `S10`), the substring check still
   passes (`'FR-S10-02' in window_text`). If F1 keeps both, no observable
   change. **Either way, the test cannot tell which extractor variant
   is running** — it green-bars on substring containment, not
   identifier equality.

3. **`test_t7_stem_fallback_without_ident_overlap_uncovers`** (lines
   323-336 PR sha) — asserts uncovered when the roadmap has no
   identifier overlap. The roadmap line "Implement priority dispatch
   for logging events" has no `S10`, no `FR-S10-02`. Both pre-fix and
   post-fix extractors agree this is uncovered. **The test correctly
   asserts the negative case**, but cannot distinguish "F2 fix worked"
   (empty-idents fallback now strict) from "F2 didn't ship" (because
   the contract's idents are non-empty `{'S10'}` either way).

### Tests that WILL shift if F1/F4 fixes land naïvely

- **`test_duplicate_lines_deduplicated`** (line 222-230 PR sha) — relies on
  empty-idents `sig in seen` exact-match dedup (line 432-433). F4 fix
  (symmetric containment) must preserve this code path or the test
  fails. The Tier 1 F4 fix sketch ("retroactively merge") risks
  breaking it if the new path replaces the empty-idents short-circuit.
- **`test_named_mechanism_in_roadmap_coverage`** (line 250-254 PR sha) —
  relies on `_extract_identifiers` returning `PROGRAMMATIC_RUNNERS`.
  F1 fix must not narrow the existing regex (only widen). Safe if F1
  adds a new pattern; unsafe if F1 rewrites the existing regex into a
  single combined pattern.
- **`test_sequential_id_assignment`** (line 232-235 PR sha) — asserts
  `c.id == f"IC-{i+1:03d}"`. F4 fix that changes dedup ordering will
  shift IC-### numbering for any fixture where multiple distinct-but-
  related signatures previously slipped through. `ALL_CATEGORIES_SPEC`
  is the highest-risk fixture (7 mechanisms, dense overlap potential).

## Proposed Fix — Test-First, Phased

### (a) Phase 0 — Pin current behavior (lands before any production change)

Add **5 new "extractor behavior pin" tests** to
`tests/roadmap/test_integration_contracts.py` that assert exact set
equality on `_extract_identifiers` output for every fixture currently in
the file. These are golden-master tests. They must pass on PR sha
`67ab0af5` unchanged.

```python
from superclaude.cli.roadmap.integration_contracts import _extract_identifiers

class TestExtractorBehaviorPin:
    def test_fr_s10_02_tokenized_as_s10_only(self):
        assert set(_extract_identifiers("FR-S10-02")) == {"S10"}

    def test_dispatch_table_spec_identifiers(self):
        assert set(_extract_identifiers(DISPATCH_TABLE_SPEC)) == {
            "PROGRAMMATIC_RUNNERS", "DISPATCH_TABLE", "HANDLERS"
        }

    def test_cli_portify_spec_identifiers(self):
        idents = set(_extract_identifiers(CLI_PORTIFY_SPEC))
        assert "PROGRAMMATIC_RUNNERS" in idents

    def test_pascal_case_identifiers(self):
        assert set(_extract_identifiers("ConcreteStrategy")) == {"ConcreteStrategy"}

    def test_tuibbs_hub_spec_window_idents(self):
        # The dispatch-hit window must contain S10 (current) — pin it.
        assert "S10" in _extract_identifiers(TUIBBS_HUB_SPEC)
```

### (b) Phase 1 — Production change (F1 + F3 only, F2 + F4 separately)

Bundle F1 (hyphenated ID extraction) with F3 (case-insensitive Layer 3
overlap) into a single PR. **Do NOT bundle F2 or F4 with F1/F3** —
their failure modes are independent and re-baselining is easier
phase-by-phase.

```python
def _extract_identifiers(text: str) -> list[str]:
    upper_snake = re.findall(r"\b[A-Z][A-Z0-9_]{2,}\b", text)
    pascal = re.findall(r"\b[A-Z][a-z]+(?:[A-Z][a-z]+)+\b", text)
    # NEW: hyphenated requirement IDs (FR-S10-02, RFC-1234, JIRA-456)
    hyphenated = re.findall(r"\b(?:[A-Z][A-Z0-9]*-)+[A-Z0-9]+\b", text)
    return upper_snake + pascal + hyphenated  # ADDITIVE — preserves all existing tokens
```

**Critical design constraint:** the patch is **additive only**. `S10`
remains in the output. `FR-S10-02` is added. Every existing assertion
that relies on substring containment continues to work. The
behavior-pin test from Phase 0 (`test_fr_s10_02_tokenized_as_s10_only`)
flips from green to red — this is the **acceptance signal** that F1
shipped. Update it to:

```python
def test_fr_s10_02_tokenized_as_hyphenated_and_fragment(self):
    assert set(_extract_identifiers("FR-S10-02")) == {"S10", "FR-S10-02"}
```

F3 (case-insensitive Layer 3):

```python
# Layer 3, line 355 (PR sha)
window_text_upper = window_text.upper()
if not any(ident.upper() in window_text_upper for ident in contract_idents):
    continue
```

### (c) Phase 2 — F2 + F4 in a separate PR

F2 (empty-idents fallback strictness) and F4 (symmetric subsumption)
each ship with their own behavior-pin tests + a re-baseline of
`test_sequential_id_assignment` on `ALL_CATEGORIES_SPEC` if IC-###
numbering shifts.

### Re-baseline strategy

1. Run `uv run pytest tests/roadmap/test_integration_contracts.py -v`
   on PR sha `67ab0af5` and **save the full JSON report**
   (`--json-report --json-report-file=baseline.json`).
2. After Phase 1 production change, re-run and **diff** assertion
   outcomes line-by-line. Any test that flips green→green for a
   different reason is a silent-pass risk — flag it manually.
3. Update `test_t1_one_contract_per_hub_mechanism` filter to use the
   *extracted* identifier set, not substring:

   ```python
   hub_contracts = [
       c for c in contracts
       if c.mechanism == "dispatch_table"
       and "FR-S10-02" in c.mechanism_signature[1]  # NEW: assert against signature, not text
   ]
   ```

   This is the test-fidelity fix that makes the assertion actually
   validate the comment's claim.
4. Update the fixture comment on line 132-134 to match reality:

   ```python
   # Synthetic fixture per RQ-1 Option A: TUIBBS-scp-inspired prose
   # threading hyphenated requirement ID `FR-S10-02` through every
   # hub-dispatch context window. With the post-F1 extractor, every
   # window's idents = {'S10', 'FR-S10-02'}; signature dedup collapses
   # to 1 hub contract via set equality.
   ```

## Confidence

**Self-reported: 0.88** — high on the diagnosis (verified by direct regex
execution + per-window analysis of every dispatch hit in TUIBBS_HUB_SPEC);
moderate on the F4 dedup re-baseline impact because IC-### shifts on
`ALL_CATEGORIES_SPEC` need empirical confirmation, not just inspection.

## Risks (asymmetric)

- **Silent-pass risk is the dominant cost.** A green test suite after F1
  ships could mean either (a) the fix correctly added `FR-S10-02` to the
  ident set, or (b) the fix had no observable effect because every
  downstream consumer uses substring matching. Without the Phase 0
  behavior-pin tests, this cluster is undetectable in CI.
- **F4 dedup change is a numbering bomb.** `test_sequential_id_assignment`
  asserts `IC-{i+1:03d}`. If F4 fix retroactively merges signatures, the
  remaining contracts re-number. `ALL_CATEGORIES_SPEC` has 7 distinct
  mechanisms and shared `dispatch`-keyword context; high probability of
  shift. Tier 1's "needs re-baseline" footnote understates this — it
  cascades to every downstream pipeline test that snapshots IC-### IDs.
- **F1 additive vs. replacement matters.** If a future refactor combines
  the three `re.findall` calls into one regex alternation, the union
  semantics must be preserved. Add a property-based test
  (`hypothesis.strategies.text` over `[A-Z0-9_-]`) to guard.
- **Fixture-comment-only fix is wrong.** Tier 1's F5 sketch suggests
  "either change the fixture's comment OR change the fixture's ID." The
  comment-only fix leaves the test asserting against `S10` while
  documenting `FR-S10-02` — that's a worse outcome than the current
  state (now the comment lies about *intent* rather than *behavior*).
  Only the production fix + assertion update pattern is acceptable.
- **Hyphenated regex precedence.** Naïve concatenation
  `upper_snake + pascal + hyphenated` means `S10` and `FR-S10-02` both
  appear. Downstream code that iterates idents and short-circuits on
  first match (`for ident in identifiers: ... break`) will see `S10`
  first, mask the `FR-S10-02` codepath. Add a test that asserts at
  least one consumer (Layer 2 ident scan) is order-independent.

## "If I'm wrong, it's probably because..."

...the test suite's substring-matching behavior is **intentional** as a
defense-in-depth measure: the team wants `S10` AND `FR-S10-02` to both
match, regardless of which the extractor returns, because spec authors
write IDs inconsistently. In that worldview, "silent green" is a
feature (robustness), not a bug (false assurance). If true, the correct
fix is to add **explicit assertions on `c.mechanism_signature`** (the
persisted frozenset) rather than re-architecting the extractor — and
the fixture comment should describe "the dedup collapses on any
S10-containing window" rather than "FR-S10-02 token threaded."

The second way I could be wrong: F4 dedup re-baseline may be a non-event
because `ALL_CATEGORIES_SPEC` separates each mechanism into its own
3-line block (per the fixture concatenation with `"\n"`). The 7-line
context window pulls in adjacent mechanism prose but distinct
`dispatch` vs `register` vs `wire` keywords mean the
`_classify_mechanism` partition prevents cross-contamination. I rate
this 60/40 — testing required.

## Files to change

- `src/superclaude/cli/roadmap/integration_contracts.py` —
  Phase 1: lines 410-419 (`_extract_identifiers` + hyphenated pattern);
  line 355 (Layer 3 `.upper()` normalization);
  Phase 2: lines 350-358 (F2 empty-idents fallback);
  lines 425-441 (F4 `_signature_subsumed` symmetric).
- `tests/roadmap/test_integration_contracts.py` —
  Add `TestExtractorBehaviorPin` class (5 new tests, Phase 0);
  update `test_t1_one_contract_per_hub_mechanism` filter to use
  `mechanism_signature[1]`;
  update fixture comment lines 132-134;
  add property-based test for extractor union semantics.
- New file `tests/roadmap/conftest.py` (optional) —
  fixture for `_extract_identifiers` golden-master tables.

## Test plan (extensive — regression-first)

### Pre-fix behavior pin (Phase 0, must land first)

- `test_fr_s10_02_tokenized_as_s10_only` — exact set equality
  `{"S10"}`. Green on PR sha.
- `test_dispatch_table_spec_identifiers` — exact set equality with
  current 3 UPPER_SNAKE tokens.
- `test_cli_portify_spec_identifiers` — `PROGRAMMATIC_RUNNERS`
  membership.
- `test_pascal_case_identifiers` — `ConcreteStrategy` membership.
- `test_tuibbs_hub_spec_window_idents` — `S10` membership.

### F1 acceptance gate (Phase 1)

- Flip `test_fr_s10_02_tokenized_as_s10_only` to
  `test_fr_s10_02_tokenized_as_hyphenated_and_fragment` asserting
  `{"S10", "FR-S10-02"}`. **Red→green is the acceptance signal.**
- Add `test_hyphenated_id_alone` — `_extract_identifiers("RFC-1234")
  == ["RFC-1234"]` (RFC is 3-char, passes existing pattern? — verify
  with regex; if no, add to expected set).
- Add `test_hyphenated_mixed_with_pascal` —
  `_extract_identifiers("FR-S10-02 uses ConcreteStrategy")` contains
  both `FR-S10-02` and `ConcreteStrategy`.
- Add `test_hyphenated_id_with_digits_only_segment` —
  `_extract_identifiers("JIRA-456")` must include `JIRA-456` (not just
  `JIRA`).
- Add `test_extractor_does_not_capture_lowercase_hyphen` —
  `_extract_identifiers("fr-s10-02")` must NOT include the lowercase
  form (regression guard: F3 normalization is the case-insensitivity
  fix, not the extractor).

### F3 acceptance gate (Phase 1)

- Add `test_layer3_overlap_case_insensitive_match` — contract with
  ident `FR-S10-02`, roadmap with lowercase `fr-s10-02`, assert
  covered.
- Add `test_layer3_overlap_case_insensitive_negative` — contract with
  ident `FR-S10-02`, roadmap with `FR-S10-03` (different number),
  assert uncovered. Guards against over-broad normalization.

### F2 acceptance gate (Phase 2 — separate PR)

- Add `test_empty_idents_strict_fallback_rejects_unrelated_dispatch` —
  contract with `mechanism_signature[1] == frozenset()`, roadmap line
  "Implement priority dispatch for logging events" — assert
  uncovered. **Currently green by accident on PR sha because
  `contract_idents` is non-empty `{'S10'}` for TUIBBS fixture, but the
  TIER 1 F2 risk is on a different fixture where idents ARE empty.**
- Add `test_empty_idents_strict_fallback_accepts_same_line_match` —
  same fixture, roadmap line "Implement dispatch_table for routing"
  (mechanism term + impl verb on same line) — assert covered.
  Validates that F2's strictness fallback isn't a blanket reject.

### F4 acceptance gate (Phase 2)

- `test_signature_subsumption_order_independent` —
  parametrize `[(min_first, super_second), (super_first, min_second)]`
  and assert same contract count after dedup.
- `test_signature_subsumption_preserves_empty_dedup` — duplicate
  empty-ident lines (the existing
  `test_duplicate_lines_deduplicated` invariant) must still collapse
  to 1.

### Negative / edge / permutation tests (cross-cutting)

- `test_extractor_handles_empty_string` —
  `_extract_identifiers("") == []`.
- `test_extractor_handles_single_char` —
  `_extract_identifiers("A") == []` (below `{2,}` threshold).
- `test_extractor_handles_hyphenated_at_line_boundary` —
  `"line1\nFR-S10-02\nline3"` extracts the ID.
- `test_extractor_handles_hyphenated_in_markdown_emphasis` —
  `"*FR-S10-02*"` and `` "`FR-S10-02`" `` and `"_FR-S10-02_"` all
  extract.
- `test_extractor_does_not_double_count` — set equality
  (`len(set(...)) == len(set(_extract_identifiers(...)))`).
- Property-based (hypothesis): for any string `s`, every token in
  `_extract_identifiers(s)` is a substring of `s` and starts with
  `[A-Z]`.
- Permutation test for `test_sequential_id_assignment` —
  shuffle the 7-section concatenation order of `ALL_CATEGORIES_SPEC`
  10× and assert contract count is constant (catches F4 ordering
  regressions).

### Snapshot regression guards

- Add `tests/roadmap/snapshots/integration_contracts_baseline.json`
  generated from PR sha `67ab0af5` containing
  `{fixture_name: [c.id, c.mechanism, sorted(c.mechanism_signature[1])]}`
  for every fixture. After each phase, diff against snapshot and
  require human review for any changed entry.

### CI gating

- Make the Phase 0 behavior-pin tests **required for merge** so any
  future extractor change must update them deliberately. Document
  this in `tests/roadmap/README.md`.

fix(roadmap): canonicalize identifiers in integration_contracts (F1+F3+F5)

PR A from the pr86-integration-contracts adversarial-merge remediation
(targets PR #86 `fix/integration-contracts-mechanism-signature`,
head sha `67ab0af5276317f83df05e25e1e620cfa59e7790`).

Bundles 7 enumerable steps that close findings F1, F3, F5 with one
named invariant (`_canonicalize_identifiers`) so call sites stop
disagreeing on case-folding and hyphen-tokenization:

- Add 4 behavior-pin tests in a new `TestExtractIdentifiersInvariants`
  class (RED → GREEN acceptance signals — defeats silent-green
  downstream assertions).
- Introduce `_canonicalize_identifiers(text) -> frozenset[str]` helper
  in `src/superclaude/cli/roadmap/integration_contracts.py` with a
  3-invariant docstring (all-uppercase tokens, hyphenated requirement
  IDs emitted as one token alongside UPPER_SNAKE fragments, empty
  input → empty frozenset).
- Switch the construction site at PR-line 196 from
  `idents = frozenset(_extract_identifiers(context))` to
  `idents = _canonicalize_identifiers(context)`.
- Mandate `window_text.upper()` at Layer 3 (PR-line 355) per the
  Round 2.5 fault-finder's INV-002 amendment — both the helper AND
  the window-upper are required (AND, not OR), so case-normalization
  fires on both sides of the membership gate.
- Update `test_t1_one_contract_per_hub_mechanism` filter from
  `"FR-S10-02" in c.spec_evidence` to
  `"FR-S10-02" in c.mechanism_signature[1]` so the test actually
  asserts canonicalization fired, not silent substring on raw evidence.
- Rewrite the F5 fixture comment to correctly describe the helper's
  behavior (was: "shared UPPER_SNAKE token"; is now: "shared
  hyphenated requirement-ID token canonicalized via
  `_canonicalize_identifiers`").
- Re-run `grep -nE "\bident\b|frozenset.*\bin\b"` audit — Layer 3 was
  the sole case-sensitive ident substring check; no other sites
  required amendment.

Two surgical deviations from the spec were applied during execution
(documented in the task file's Deviations section) after Phase 2 QA
surfaced a defect in OQ-1 Option B's literal form:

1. Helper body uses `_extract_identifiers(text)` (not `text.upper()`)
   + adds a `(?=\S*\d)` digit-lookahead to the hyphen pattern so prose
   kebab-case (`class-priority`, `message-class`, `severity-keyed`) is
   excluded + extracts UPPER_SNAKE fragments from the uppercased hyphen
   tokens only. Without these refinements, `text.upper()` would
   uppercase common English words from natural prose contexts and
   pollute the identifier set, breaking pre-existing T1/T7 regression
   tests. The refinement preserves OQ-1 Option B's stated intent ("S10
   extractable from lowercase fr-s10-02") via fragment-side extraction.
2. Dropped the spec-required `_extract_identifiers` import from the
   test module — post-OQ-1 Option B, only `_canonicalize_identifiers`
   is referenced in tests; keeping the unused import triggered Ruff
   F401.

Verification:

- 4 pin tests RED → GREEN (collection-time ImportError → all PASS).
- Full `tests/roadmap/` suite: 1693 passed, 11 skipped, 0 failed.
- `make lint` (ruff check on entire repo): all checks passed.
- 2 prior-existing regression tests (`test_t1`, `test_t7`) confirmed
  still GREEN after the deviation.
- Final QA gate (rf-qa task-validation, cycle 1): PASS on all 12
  verification points.

F2 (PR B — empty-idents coverage policy) and F4 (PR C — subsumption
symmetry) are RFC-first follow-ups and are explicitly OUT OF SCOPE
for this PR.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

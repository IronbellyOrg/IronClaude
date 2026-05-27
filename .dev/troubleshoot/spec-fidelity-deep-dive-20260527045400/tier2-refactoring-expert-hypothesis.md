# Hypothesis: Primitive-obsession on requirement IDs across the roadmap pipeline — the absent `RequirementId` value object is the structural defect that *guarantees* extractor-vs-comparator asymmetry will recur, even if `D01/D1` is patched in `check_signatures`

**Agent**: refactoring-expert
**Tier**: 2
**Timestamp**: 2026-05-27T05:25:00Z
**Cause class**: Missing abstraction / primitive obsession (structural design defect)
**Consistency with docs**: aligned

## Claim

The recurrent spec-fidelity halt is the visible failure mode of a **missing domain abstraction**: a `RequirementId` value object that owns canonicalization. Raw `str` flows from `spec_parser.extract_requirement_ids` (`spec_parser.py:333-344`) into `check_signatures` (`structural_checkers.py:372-391`) and is compared with raw `set`-difference at line 380. The extractor's regex is lenient (`\bD-?\d+\b`); the comparator's `==` is strict; that asymmetry is *inevitable* whenever a primitive crosses a module seam without a canonicalization owner. The D01/D1 bug is one expression of this defect — FR-7.1 vs FR-7-1, NFR-2 vs NFR-02, and SC-001 vs SC-1 are the next three. The structurally correct fix is not "add `_canonicalize_requirement_id` inside `check_signatures`" (Tier-1 proposal): that re-introduces the same primitive obsession one rule_id over. The structurally correct fix is to *move canonicalization to a single source-of-truth helper* (`RequirementId.from_raw`) that the extractor calls before emitting, so both extractor and comparator handle the *same canonical form by construction*. This mirrors the precedent already shipped in `integration_contracts.py:445` (`_canonicalize_identifiers`), and turns "primitive flowing through pipeline" into "canonical type flowing through pipeline" — eliminating an entire class of recurrence.

## Evidence

- `src/superclaude/cli/roadmap/spec_parser.py:329` — `"D": re.compile(r"\bD-?\d+\b")` (verified). The regex is intentionally lenient (matches both `D1` and `D01`) but `extract_requirement_ids` at lines 333-344 returns `sorted(set(pattern.findall(text)))` — raw matched strings. The extractor *knows* `D1` and `D01` are the same kind of token (one regex matches both) but emits them as if they were distinct primitives. This is primitive obsession at the API boundary.
- `src/superclaude/cli/roadmap/structural_checkers.py:372-391` — verified. Lines 372-378 union family ID lists into `spec_ids` / `roadmap_ids` *as `set[str]`*. Line 380: `phantom_ids = roadmap_ids - spec_ids`. The seam between "parser produces strings" and "checker compares strings" has no canonicalization owner. The 5-checker architecture (per `architecture-design.md:27-33`) re-derives ID semantics inline inside *each* checker callable — there is no shared abstraction. If a future checker (e.g. `check_data_models`) also unions `requirement_ids` and set-subtracts, it will re-implement the same bug.
- `src/superclaude/cli/roadmap/structural_checkers.py:260-286` — `_make_finding` verified. It accepts `mismatch_type: str` and emits `fix_guidance=f"Address {mismatch_type} in {dimension} dimension"` on line 279 — generic format-string templating, no per-mismatch-type dispatch. Adding a `phantom_id`-specific guidance branch *here* is yet another inline reimplementation; the fact that `_make_finding` exists but doesn't centralize mismatch-type behavior is itself a sign that the abstraction boundary is wrong.
- `src/superclaude/cli/roadmap/integration_contracts.py:445-469` — `_canonicalize_identifiers` verified. Returns a `frozenset[str]` of uppercased canonical tokens, with explicit invariants in the docstring (lines 448-457): "All tokens are uppercase", "Hyphenated requirement IDs are emitted as ONE token, not split on hyphens", "Empty input yields an empty frozenset". This is the *exact pattern* the requirement-ID surface needs and is the project-blessed precedent (KNOWLEDGE.md 2026-05-25, "Fix B Merged"). It is currently a private helper inside one module — the refactoring move is to *promote* this pattern to a shared utility consumed by both `spec_parser.py` and `structural_checkers.py`.
- `src/superclaude/cli/roadmap/structural_checkers.py:355-364` — `check_signatures` verified. Lines 360-361 read both files and call `parse_document(spec_text)` / `parse_document(roadmap_text)` (the parser), then immediately consume `.requirement_ids` (a `dict[str, list[str]]` of raw strings). The seam is *one function-call deep* — there is no intermediate "canonicalize-or-normalize" stage. Adding canonicalization inside `check_signatures` (Tier-1 proposal) plasters over the seam; moving canonicalization into `extract_requirement_ids` *removes* the seam.

## Why it recurs (Phase 0 pattern)

Per `historical-context.md` Section 5 Pattern 2: "Every prior failure shape has been distinct" (severity drift; parser noise + `files_affected=[]`; now `D01`/`D1`). Per Section 4: "ID-schema normalization … Not present in any backlog, debate, or open task that I could find." Per debate-transcript.md:127: "no shipped remediation has ever touched the spec-fidelity comparator itself." This is the canonical signature of a **missing abstraction**: every fix is shape-specific because the structural primitive (raw `str` requirement IDs flowing through a multi-module pipeline) never changed. Each release patches the symptom in the module the symptom surfaced in; the next release surfaces the same defect in a different module under a different rule_id. A `RequirementId` value object closes the loop: the parser cannot emit a non-canonical form (constructor enforces invariants), the checker cannot compare non-canonical forms (the type system prevents it), and the next ID-family quirk (FR-7.1 vs FR-7-1) is fixed once in the constructor rather than five times across five checkers.

## Proposed Fix

**Promote canonicalization to a shared module-level helper that the parser calls at emission time, so the checker receives canonical IDs by construction.** This is a refactoring move (Extract Helper + Move Method, in Fowler's catalog), not a feature add. The change touches two files and zero behavioral seams beyond the one the bug lives in.

Concrete edits (all within restriction-1's module-ownership rules: parser owns extraction FR-2/FR-5, checker owns comparison FR-1/FR-3; this fix re-balances *where canonicalization lives within extraction*, not what either module owns):

1. **`src/superclaude/cli/roadmap/spec_parser.py:324-344`** — add a module-private `_canonicalize_requirement_id(family: str, raw: str) -> str` helper directly above `_REQUIREMENT_PATTERNS`. Implementation: strip leading zeros from the numeric tail while preserving family prefix and sub-ID structure (`D01` → `D1`; `FR-7.1` → `FR-7.1` unchanged; `NFR-02` → `NFR-2`). Pure function, no I/O, no shared state. Then modify `extract_requirement_ids` at lines 333-344 to apply the canonicalizer before the `sorted(set(...))` call:

    ```python
    for family, pattern in _REQUIREMENT_PATTERNS.items():
        raw_ids = pattern.findall(text)
        canonical = [_canonicalize_requirement_id(family, r) for r in raw_ids]
        ids = sorted(set(canonical))
        if ids:
            result[family] = ids
    ```

   ~12 lines added, 3 modified. Well under 30% per-patch guard.

2. **`src/superclaude/cli/roadmap/structural_checkers.py:380`** — **no change required**. Because `spec_parsed.requirement_ids` and `roadmap_parsed.requirement_ids` now both contain canonical forms, `phantom_ids = roadmap_ids - spec_ids` becomes correct *as written*. This is the refactoring quality signal: the bug disappears at the call site without modifying the call site. The 5-checker architecture remains untouched.

Tests that would prove the fix:

- New: `tests/cli/roadmap/test_spec_parser.py::test_canonicalize_zero_padded_d_ids` — feed `"D1, D01, D5"`, assert `{"D": ["D1", "D5"]}`.
- New: `tests/cli/roadmap/test_spec_parser.py::test_canonicalize_idempotent_on_unpadded` — feed `"D1, D3, D5"`, assert `{"D": ["D1", "D3", "D5"]}` (no spurious mutation).
- New: `tests/cli/roadmap/test_structural_checkers.py::test_phantom_id_no_false_positive_on_zero_pad_drift` — spec with `D1, D3, D5`, roadmap with `D01..D54`, assert `D02, D04, D06..D54` *are* HIGH phantom_ids (they're genuinely absent from spec) but `D01, D03, D05` are NOT (their canonical forms match). This is the structurally correct behavior — drift is normalized, genuine phantoms still fire.
- Regression: existing tests on `_REQUIREMENT_PATTERNS` continue to pass; the regex is unchanged.

## Confidence

Self-reported confidence: 0.87

Per-dimension self-assessment:
- Evidence grounding: 1.0 — every citation re-Read in this turn; snippets verified verbatim against the source files.
- Symptom coverage: 1.0 — explains the 54-HIGH count, the recurrence pattern (Section 5 Pattern 2), why no prior fix touched the comparator (debate-transcript.md:127), and why placing the fix in the checker (Tier-1 proposal) re-creates the bug surface one rule_id away.
- Reproducibility fit: 1.0 — deterministic; reproducible by running `extract_requirement_ids` on TUIBBS `epics.md` and `roadmap.md` before and after the canonicalization helper lands.
- Fix directness: 1.0 — single helper, ~12 lines, mirrors `integration_contracts.py:445` precedent shipped 2026-05-25, well under 30% per-patch guard, zero changes to checker code.
- Domain coherence: 0.5 — there is a defensible counterargument that canonicalization belongs in the comparator (Tier-1's choice) because "extraction faithfully reports what the source contains, comparison decides what counts as the same." The refactoring lens favors moving canonicalization upstream because it eliminates the asymmetric-seam pattern across all five checkers simultaneously, but a strict-fidelity-extractor purist could prefer the checker-side fix.

## Compliance with the 7 restrictions (per doc-context.md)

1. **Module ownership (`structural_checkers.py` owns checkers/severity)** — RESPECTED. No checker code changes. The seam between parser-output and checker-input is *defined by what the parser emits*; tightening that emission is parser's prerogative (FR-2/FR-5: "extraction"), and "canonicalization-as-part-of-extraction" is well within that mandate.
2. **Pure-function contract (NFR-4)** — RESPECTED. `_canonicalize_requirement_id` takes `(family: str, raw: str) -> str`, no I/O, no shared mutable state, deterministic. Identical signature shape to `_canonicalize_identifiers` precedent.
3. **30% per-patch diff guard** — RESPECTED. ~12 lines added, 3 modified in `spec_parser.py`; `structural_checkers.py` untouched. Far below 30% of either file.
4. **Pass condition is strictly binary (`active_highs == 0`)** — RESPECTED. The fix produces *zero* phantom_id HIGHs for legitimate-drift cases (D01↔D1), so the existing binary pass condition works correctly without modification.
5. **Spec is an input the agent cannot modify** — RESPECTED. Code-only change in IronClaude; no spec edit required.
6. **`max_runs=3` is the default** — RESPECTED. No convergence-loop changes. Run 1 will simply emit 0 phantom_id HIGHs for the TUIBBS case, and convergence passes immediately.
7. **Precedent for canonicalization exists locally** — DIRECTLY LEVERAGED. The fix is structurally identical to `integration_contracts.py:445` (`_canonicalize_identifiers`) — same pure-function shape, same "uppercase + canonical tokens" pattern, same module-private placement. Net effect: two sibling canonicalizers (one for integration tokens, one for requirement IDs) emerge as a *consistent project pattern* that future modules can follow.

## Risks

- **Round-trip surprise**: callers downstream of `extract_requirement_ids` that expect to see *exactly the form that appeared in the source text* (e.g. for verbatim quoting in a Finding's `roadmap_quote`) will now receive the canonical form. Mitigation: audit `Finding.roadmap_quote` consumers — currently the quote is populated at `structural_checkers.py:389` with `roadmap_quote=pid`, which is the canonical form post-fix. If a downstream report needs the raw form for human readability, store both: `RequirementId(canonical=..., raw=...)`. For the minimal fix, canonical-only is sufficient.
- **Hidden cross-family collisions**: if any project legitimately uses `D1` and `D01` to mean *different* requirements, canonicalization will collide them. This is structurally indistinguishable from the TUIBBS drift case at the regex level. Mitigation: emit a one-line warning when `extract_requirement_ids` collapses two distinct raw forms into one canonical form, so the human can investigate ambiguity at parse time rather than at compare time.
- **Family-specific canonicalization rules**: FR sub-IDs use dots (`FR-7.1`), other families may not. The canonicalizer must dispatch on `family`, not apply blanket zero-strip. Implementation risk is mechanically low but the helper *must* be unit-tested across all five families.
- **Does not address the binary-pass-condition (`active_highs == 0`) brittleness**: this fix forecloses the *recurrence vector* (extractor/comparator asymmetry across modules), but the convergence loop's missing MANUAL_TRIAGE state (S6, deferred) is a separate latent defect for *the next* failure shape that isn't an ID-canonicalization issue.

## If I'm wrong, it's probably because...

The asymmetric extractor/comparator design was an *intentional* fidelity-preservation decision (extractor reports verbatim, comparator decides equivalence) — in which case the right fix is the Tier-1 proposal (canonicalize inside the comparator), and my refactoring move papers over a deliberate seam that the team wants to keep.

## Alternatives considered

- **Introduce a `RequirementId` value object (full dataclass with `.canonical`, `.raw`, `.family`, `__eq__`, `__hash__`)**: rejected for *this* fix as over-engineering — a `str`-typed canonicalization helper inside the parser is the minimal viable refactor and matches the `_canonicalize_identifiers` precedent. The value object is the right *next* step once a second consumer beyond `check_signatures` needs ID semantics; pre-emptively introducing it now is a YAGNI violation.
- **Canonicalize inside `check_signatures` (Tier-1 proposal)**: rejected — covered in "Claim". It papers over the seam in one checker while leaving the same primitive-obsession defect in every other checker that consumes `parsed.requirement_ids`. The refactoring lens prefers eliminating the recurrence vector, not patching one instance.
- **Canonicalize inside `_make_finding` (severity-rule dispatch path)**: rejected — `_make_finding` doesn't know about ID semantics, only about (dimension, mismatch_type) tuples. Adding ID-awareness here would entangle responsibilities (severity rules + ID canonicalization), violating SRP and worsening the cohesion the architecture-design.md modules table is trying to enforce.

## Grounding gaps

- Did not enumerate every downstream consumer of `parsed.requirement_ids` to confirm no caller depends on raw-form preservation. Quick audit needed (grep `requirement_ids` across `src/superclaude/cli/roadmap/`).
- Did not verify that the FR/NFR/SC/G families exhibit canonical-form drift in real-world projects (TUIBBS evidence is D-family only). The canonicalizer's per-family logic needs to be cross-family-tested before merge.
- Did not run the proposed fix end-to-end on TUIBBS — claim that "Run 1 emits 0 phantom_id HIGHs for D01..D54" is *inferred from verified set-difference semantics post-canonicalization*, not measured.
- Did not enumerate whether any other primitive-obsession surfaces exist beyond `requirement_ids` (e.g. function signatures, file paths, severity strings). If they do, this fix sets a useful precedent but does not address them — they will need their own canonicalization owners in their own time.

# Tier 1 Hypothesis — Unified `mechanism_signature` identifier-handling defect cluster

**Author**: root-cause-analyst (inline)
**Tier**: 1
**Type**: bug
**Scope**: `src/superclaude/cli/roadmap/integration_contracts.py` @ PR #86 sha `67ab0af5`
**PR**: <https://github.com/IronbellyOrg/IronClaude/pull/86>

## Claim

PR #86's mechanism_signature refactor introduces a **cluster of 5 related defects** rooted in one design gap: `_extract_identifiers()` does not recognize hyphenated requirement IDs (e.g. `FR-S10-02`) as single tokens, and downstream consumers (signature subsumption, Layer 3 overlap guard, test fixture) inherit that weakness. Three are medium-severity correctness bugs; two are low-severity hygiene / fixture-fidelity issues. All five are independently verifiable against the PR's pinned sha.

## Evidence (PR sha `67ab0af5`)

### F1 — `_extract_identifiers()` cannot capture hyphenated IDs (medium, r3299815777)

- File: `src/superclaude/cli/roadmap/integration_contracts.py` lines 410-419 (PR sha)
  ```python
  def _extract_identifiers(text: str) -> list[str]:
      ...
      upper_snake = re.findall(r"\b[A-Z][A-Z0-9_]{2,}\b", text)
      pascal = re.findall(r"\b[A-Z][a-z]+(?:[A-Z][a-z]+)+\b", text)
      return upper_snake + pascal
  ```
- The `\b` word-boundary on `-` (non-word char) splits `FR-S10-02` into three regex candidates: `FR` (rejected — only 2 chars, `{2,}` needs 3+), `S10` (accepted), `02` (rejected — starts with digit). Result: `['S10']`.
- Verified by inspection of the regex `\b[A-Z][A-Z0-9_]{2,}\b` against the input `FR-S10-02`.

### F2 — Layer 3 skips identifier-overlap guard when `contract_idents` is empty (medium, r3299815779)

- File: `src/superclaude/cli/roadmap/integration_contracts.py` lines 350-358 (PR sha)
  ```python
  if contract_idents:
      window_start = max(0, j - 2)
      window_end = min(len(roadmap_lines), j + 3)
      window_text = " ".join(roadmap_lines[window_start:window_end])
      if not any(ident in window_text for ident in contract_idents):
          continue
  covered = True
  ```
- When `contract_idents` is empty (mechanism extracted no UPPER_SNAKE/Pascal idents — common for generic mechanisms like bare `dispatch_table` or `middleware`), the guard is bypassed and `covered = True` is set on stem+verb match alone.
- Reintroduces the very false-positive class the guard was added to prevent — "Implement priority dispatch for logging" marks an unrelated `dispatch_table` contract covered.

### F3 — Layer 3 identifier overlap is case-sensitive (medium, r3299815783)

- File: same lines 355-356 (PR sha)
  ```python
  if not any(ident in window_text for ident in contract_idents):
  ```
- Direct substring check — no `.upper()` / `.lower()` normalization.
- Inconsistent with Layer 2 at PR line 261 (`if ident.upper() in rline.upper():`) which IS case-insensitive.
- A roadmap line citing `fr_s10_02` (lowercase, as authors commonly do for IDs) misses a contract whose ident is `S10` or `FR_S10_02` (uppercase), causing false-negative uncovered reports.

### F4 — `_signature_subsumed` is order-dependent (low, r3299815789)

- File: `src/superclaude/cli/roadmap/integration_contracts.py` lines 425-441 (PR sha)
  ```python
  for (smech, sidents) in seen:
      if smech != mech:
          continue
      if idents and sidents and idents.issubset(sidents) and (idents & sidents):
          return True
      if idents == sidents:
          return True
  return False
  ```
- Only returns `True` when the NEW signature's idents are a `issubset()` of an already-seen signature. A minimal sig seen first → a later superset sig is NOT subsumed → duplicate contracts produced.
- Symmetric containment is missing: should check `sidents.issubset(idents)` AND retroactively merge (or short-circuit) when found.

### F5 — Test fixture comment mismatches `_extract_identifiers` behavior (low, r3299815792)

- File: `tests/roadmap/test_integration_contracts.py` lines 132-134 (PR sha)
  ```python
  # Synthetic fixture per RQ-1 Option A: TUIBBS-scp-inspired prose with shared
  # UPPER_SNAKE token `FR-S10-02` in every hub-dispatch context window so
  # `_signature_subsumed` fires deterministically (subset+overlap dedup).
  ```
- Comment claims `FR-S10-02` is a single UPPER_SNAKE token, but per F1 the extractor tokenizes it as `['S10']`. The test's subset+overlap dedup is actually being validated against the fragment `S10`, not the full requirement ID. Test still passes but its premise is broken.

## Proposed Fix (combined, high-level)

Four production-code changes + one test-comment correction:

1. **F1 fix** — Tokenize hyphenated requirement IDs as one identifier. Add a third pattern `r"\b(?:[A-Z][A-Z0-9]*-)+[A-Z0-9]+\b"` (or merge into a single combined regex) to capture `FR-S10-02`, `RFC-1234`, `JIRA-456` shapes. Return identifiers as a normalized list (`.upper()` at extraction or comparison time).
2. **F3 fix** — Normalize case at the Layer 3 overlap guard (mirror Layer 2's `.upper()` pattern, or canonicalize idents to upper at extraction).
3. **F2 fix** — Replace the `if contract_idents:` short-circuit with a fallback: when idents are empty, require a stricter same-line co-occurrence (mechanism term + impl verb on the SAME line, not 3-line window), OR refuse to cover. The current bypass is too permissive.
4. **F4 fix** — Switch `_signature_subsumed` to symmetric containment: detect both subset and superset cases. When a superset is detected, either replace the seen sig with the broader one or short-circuit dedup (depending on counter semantics — needs spec decision).
5. **F5 fix** — Either change the fixture's comment to accurately describe what gets tokenized, OR change the fixture's ID to a true UPPER_SNAKE form (`FR_S10_02` with underscores) that the current extractor handles cleanly. (F1 fix also makes this consistent, but the comment may still need rewording.)

## Confidence

**Self-reported: 0.92** (5/5 claims verified against PR-pinned source; the design chain is coherent; fix directions are concrete and localized.)

Calibration deferred to `tier1-calibration.md` (see Wave 1 step 4).

## Risks

- **F4 fix** (subsumption symmetry) interacts with `seen_signatures` counter ordering. Changing dedup semantics may shift IC-### numbering deterministically — needs the test suite re-baselined.
- **F1 + F2 + F3 fixes** stack: changing `_extract_identifiers` to include hyphenated IDs will populate `contract_idents` for many previously-empty contracts, which may *also* change Layer 3 coverage rates (some uncovered contracts will become covered). Net effect: harder to predict in isolation; needs adversarial debate on whether to ship as one bundle or staged.
- The test fixture `TUIBBS_HUB_SPEC` may depend on the current (buggy) tokenization; F1's fix could break tests that assumed `S10` not `FR-S10-02`.

## "If I'm wrong, it's probably because..."

...the team intentionally chose `_extract_identifiers`'s current narrow tokenization to keep `mechanism_signature` collisions rare, and the "empty-idents skip" in F2 is a deliberate fallback for the test-only path. In that case the right fix is **stricter** (raise the threshold for empty-idents coverage) rather than **broader** (normalize tokenization).

## Files to change

- `src/superclaude/cli/roadmap/integration_contracts.py` (F1, F2, F3, F4)
- `tests/roadmap/test_integration_contracts.py` (F5 + re-baseline assertions affected by F1/F4)

## Test plan

- Add focused unit tests for `_extract_identifiers` on hyphenated requirement IDs.
- Add a regression test for F2 (empty-ident contract + adversarial roadmap line).
- Add a case-insensitivity test for F3.
- Add a permutation-order test for F4: feed signatures in order (minimal, superset) and (superset, minimal); assert dedup produces the same count.
- Re-run existing `test_integration_contracts.py` to catch any baseline shifts; rebaseline only where the new behavior is the intended one.

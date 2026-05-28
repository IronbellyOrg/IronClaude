# Tier 2 Hypothesis — Root-Cause-Analyst angle

**Author**: root-cause-analyst (Tier 2 parallel specialist)
**Tier**: 2
**Scope**: PR #86 `src/superclaude/cli/roadmap/integration_contracts.py` @ sha `67ab0af5`

## Claim

There is **one root cause and two independent secondary defects**, not five peer findings. The root cause is `_extract_identifiers()`'s contract: it returns a verbatim list of `upper_snake + pascal` regex hits with **no requirement-ID shape and no case normalization**. That single contract gap is the upstream of F1, F3 (partially), and F5. F2 (empty-`contract_idents` short-circuit) and F4 (asymmetric `_signature_subsumed`) are **independent design defects** in *consumers* of the identifier set and must be fixed on their own terms — they are NOT caused by F1 and would persist after F1 is fixed.

I therefore propose **one consolidated fix to `_extract_identifiers` + Layer 3 normalization (resolves F1, F3, F5)** and **explicitly split off F2 and F4 to be handled by separate, focused changes** to avoid bundling unrelated semantic decisions into a single commit.

## Evidence (PR sha `67ab0af5`)

### Root cause — `_extract_identifiers` returns raw, unnormalized tokens

`src/superclaude/cli/roadmap/integration_contracts.py:412-419`:

```python
def _extract_identifiers(text: str) -> list[str]:
    """Extract UPPER_SNAKE_CASE and PascalCase identifiers from text.

    FR-MOD2.4: Named mechanism identifier matching.
    """
    # UPPER_SNAKE_CASE (likely constants/tables)
    upper_snake = re.findall(r"\b[A-Z][A-Z0-9_]{2,}\b", text)
    # PascalCase class names
    pascal = re.findall(r"\b[A-Z][a-z]+(?:[A-Z][a-z]+)+\b", text)
    return upper_snake + pascal
```

Two contract decisions baked in here propagate downstream:

1. **No hyphen support.** The regex `\b[A-Z][A-Z0-9_]{2,}\b` uses `\b` (word boundary). `-` is a non-word character, so `FR-S10-02` is split into three candidates: `FR` (rejected, length 2 < 3), `S10` (accepted), `02` (rejected, starts with digit). Verifiable: `re.findall(r"\b[A-Z][A-Z0-9_]{2,}\b", "FR-S10-02") == ['S10']`. This is **F1** verbatim.
2. **No canonical case.** Tokens are returned as-found. Every consumer is therefore obligated to call `.upper()`/`.lower()` themselves. **Layer 2 at line 261** does (`if ident.upper() in rline.upper()`), but **Layer 3 at line 355** does not — and that is **F3**.

### F5 is a documentation symptom of the F1 contract gap

`tests/roadmap/test_integration_contracts.py:130-134` describes the fixture's `FR-S10-02` as "shared UPPER_SNAKE token", which is *aspirationally* what the author wanted the extractor to do — but the code disagrees. The fixture happens to still produce a non-empty ident set (`{'S10'}`), so the test passes, but the test's premise is wrong. Once F1 is fixed, `FR-S10-02` becomes a single token and the comment becomes accurate **with no test rewrite**.

### F2 is independent — empty-ident short-circuit at line 351

```python
if contract_idents:
    window_start = max(0, j - 2)
    window_end = min(len(roadmap_lines), j + 3)
    window_text = " ".join(roadmap_lines[window_start:window_end])
    if not any(ident in window_text for ident in contract_idents):
        continue
covered = True
```

This is a *policy* decision about how strict Layer 3 should be when the spec evidence has no extractable idents. F1 reduces the *frequency* of empty `contract_idents` (because hyphenated IDs will now be captured), but the empty-ident case still exists for any mechanism whose context window contains zero UPPER_SNAKE / Pascal tokens (e.g. a contract whose evidence is pure prose: "the system uses a dispatch table"). F1 does not change that path's behavior; F2 must be fixed on its own.

### F4 is independent — asymmetric subsumption at line 437

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

Only `idents.issubset(sidents)` is checked — the inverse direction (`sidents.issubset(idents)`) is not. This is a pure-logic bug in dedup ordering and is **independent of what `_extract_identifiers` returns**. Even after F1 makes ident sets richer, the order-sensitivity remains: feed signatures `(mech, {A})` then `(mech, {A,B})` and you get two contracts; feed `(mech, {A,B})` then `(mech, {A})` and you get one. F1 cannot mask this.

## Proposed Fix (one coherent change set)

**In scope for this PR — fix the root cause + the symptom it actually causes (F1, F3, F5):**

1. Extend `_extract_identifiers` with a hyphenated-ID pattern AND canonicalize all returned tokens to uppercase, so downstream consumers can rely on a normalized list:

   ```python
   def _extract_identifiers(text: str) -> list[str]:
       upper_snake = re.findall(r"\b[A-Z][A-Z0-9_]{2,}\b", text)
       hyphen_id = re.findall(r"\b[A-Z][A-Z0-9]*(?:-[A-Z0-9]+)+\b", text)
       pascal = re.findall(r"\b[A-Z][a-z]+(?:[A-Z][a-z]+)+\b", text)
       # Canonicalize case so consumers (Layer 3, _signature_subsumed)
       # don't have to remember to normalize. Preserves hyphens/underscores.
       return [t.upper() for t in (upper_snake + hyphen_id + pascal)]
   ```

2. Update the Layer 3 overlap guard at line 355 to compare against the upper-cased window, consistent with Layer 2:

   ```python
   window_text_u = window_text.upper()
   if not any(ident in window_text_u for ident in contract_idents):
       continue
   ```

3. Leave the test fixture comment as-is — it becomes truthful after fix (1). The fixture text already contains `FR-S10-02`, which will now tokenize to `{'FR-S10-02'}` and exercise the subset+overlap path the comment claims.

**Explicitly deferred / split off:**

- **F2** → new focused PR. Choice between "require same-line stem+verb when idents are empty" vs. "refuse coverage when idents are empty" is a coverage-policy call that needs its own adversarial debate and test re-baselining. Bundling it here muddies F1's diff.
- **F4** → new focused PR. Fixing symmetric subsumption changes IC-### numbering for any fixture that previously produced order-sensitive duplicates. Need to re-baseline `seen_signatures` counter behavior. Should NOT ride along with a regex change.

## Confidence

**Self-reported: 0.88.**

I am confident (≈0.95) on the F1→F3→F5 chain and on F4 being independent. I am less confident (≈0.75) on whether F2 is fully independent of F1: in the test fixture, F1's fix moves `contract_idents` from `{'S10'}` (already non-empty, so F2's guard already fires) to `{'FR-S10-02', 'S10'}` (still non-empty). F2's bad path only activates when *zero* idents are extracted — which neither fixture currently exercises. So F2 may be latent rather than active, which strengthens the case for splitting it off.

## Risks

- Canonicalizing to uppercase in `_extract_identifiers` is a **contract change** for all callers. Layer 2 (line 261) already upper-cases both sides, so this is idempotent there. Layer 3 (line 355) currently does substring match raw; after this fix the window must also be upper-cased (item 2 above). Any future caller must be aware.
- The hyphenated-ID regex `\b[A-Z][A-Z0-9]*(?:-[A-Z0-9]+)+\b` will overlap with `upper_snake` for short prefixes (e.g. in `FR-S10-02`, `upper_snake` captures `S10` and `hyphen_id` captures `FR-S10-02`). Both end up in the result. That is *correct* behavior — it lets Layer 3 match either form a roadmap might cite — but it means `len(idents)` grows, which marginally increases the chance F4's asymmetry produces visible duplicates. Argues for fixing F4 soon after.
- Test fixtures that previously asserted exact ident-set membership (e.g. `assert idents == {'S10'}`) will break. Need to grep for direct assertions on `_extract_identifiers` output.

## "If I'm wrong, it's probably because..."

...F2's empty-ident path is actually exercised in production roadmaps far more than the test corpus suggests, and bundling F1 + F2 together is the right pragmatic call to prevent a coverage regression window between PRs.

## Files to change (this PR)

- `src/superclaude/cli/roadmap/integration_contracts.py` — modify `_extract_identifiers` (add hyphen regex, normalize case); modify Layer 3 guard to upper-case the window (lines 412-419 and 351-356).
- `tests/roadmap/test_integration_contracts.py` — add unit tests for `_extract_identifiers` on hyphenated IDs and mixed-case input; no fixture comment edit needed.

## Test plan

1. **Direct `_extract_identifiers` tests:**
   - `assert "FR-S10-02" in _extract_identifiers("see FR-S10-02 for details")`
   - `assert _extract_identifiers("mixedCase IDENT_ONE") == ["IDENT_ONE"]` (Pascal `mixedCase` excluded — needs 2+ humps)
   - `assert _extract_identifiers("foo-bar baz") == []` (no leading uppercase)
   - All returned values pass `.isupper() or .replace('-','_').replace('_','').isupper()` (normalized).
2. **Layer 3 case-insensitivity regression:** new contract with ident `S10`, roadmap line citing `fr-s10-02` (lowercase). Assert covered.
3. **F1+F3 integration test:** synthetic spec with `FR-S10-02` in evidence, roadmap with the same ID in lowercase elsewhere — assert coverage and assert `contract.mechanism_signature[1]` contains `'FR-S10-02'`.
4. **Re-run** existing `tests/roadmap/test_integration_contracts.py` and rebaseline only where the new ident shape is intentional.
5. **Do NOT** add tests for F2 or F4 in this PR — they belong to the split-off PRs and would otherwise be testing unfixed bugs.

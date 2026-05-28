# Research: File Inventory (PR sha 67ab0af5)
**Topic type:** File Inventory
**Scope:** integration_contracts.py + test_integration_contracts.py at PR sha 67ab0af5
**Status:** Complete
**Date:** 2026-05-26
---

## File size verification

- `src/superclaude/cli/roadmap/integration_contracts.py` @ 67ab0af5 = **441 lines** (matches claim).
- `tests/roadmap/test_integration_contracts.py` @ 67ab0af5 = **388 lines**.

All citations below use `git show 67ab0af5:<path>` line numbers — NOT on-disk content.

---

## Touch Point 1 — `_extract_identifiers` definition

**Claimed:** PR-lines 412-419.
**Actual:** PR-lines **412-421** (claim was off by 2 lines — body includes blank line + return).

Verbatim from `git show 67ab0af5:src/superclaude/cli/roadmap/integration_contracts.py`:

```
412: def _extract_identifiers(text: str) -> list[str]:
413:     """Extract UPPER_SNAKE_CASE and PascalCase identifiers from text.
414:
415:     FR-MOD2.4: Named mechanism identifier matching.
416:     """
417:     # UPPER_SNAKE_CASE (likely constants/tables)
418:     upper_snake = re.findall(r"\b[A-Z][A-Z0-9_]{2,}\b", text)
419:     # PascalCase class names
420:     pascal = re.findall(r"\b[A-Z][a-z]+(?:[A-Z][a-z]+)+\b", text)
421:     return upper_snake + pascal
```

Signature: `def _extract_identifiers(text: str) -> list[str]:` — returns `list[str]`, NOT `frozenset`.
Conversion to `frozenset` happens at construction site (touch point 2).

---

## Touch Point 2 — Construction site

**Claimed:** PR-line 196 (`idents = frozenset(_extract_identifiers(context))`).
**Actual:** Confirmed at PR-line **196** exactly.

Surrounding context (lines 193-200):

```
193:             context = "\n".join(lines[context_start:context_end])
194:
195:             mechanism = _classify_mechanism(match.group(0))
196:             idents = frozenset(_extract_identifiers(context))
197:             signature = (mechanism, idents)
198:
199:             # Signature-based dedup — collapse contracts whose
200:             # (mechanism, identifier-set) is identical OR is a strict
```

---

## Touch Point 3 — Layer 3 block with empty-idents guard

**Claimed:** PR-lines 350-358.
**Actual:** Empty-idents guard block at PR-lines **351-356**. Broader Layer 3 surrounding logic spans 346-360.

Verbatim (lines 346-360):

```
346:                         # IDENTIFIER-OVERLAP GUARD: require at least one of the
347:                         # contract's mechanism_signature identifiers to appear in
348:                         # the matching line's 3-line window. Defeats the
349:                         # "Implement priority dispatch for logging" false-positive
350:                         # class (Sonnet's own counter-argument scenario).
351:                         if contract_idents:
352:                             window_start = max(0, j - 2)
353:                             window_end = min(len(roadmap_lines), j + 3)
354:                             window_text = " ".join(roadmap_lines[window_start:window_end])
355:                             if not any(ident in window_text for ident in contract_idents):
356:                                 continue
357:                         covered = True
358:                         evidence = rline.strip()
359:                         location = f"line {j + 1} (stem+overlap)"
360:                         break
```

---

## Touch Point 4 — Layer 3 case-sensitive check

**Claimed:** PR-line 355 (`if not any(ident in window_text for ident in contract_idents):`).
**Actual:** Confirmed at PR-line **355** exactly.

This is the **case-sensitive** comparison — `ident in window_text` does NOT normalize case. Compare to Layer 2 (touch point 5) which DOES normalize.

---

## Touch Point 5 — Layer 2 case-insensitive precedent

**Claimed:** PR-line 261 (`if ident.upper() in rline.upper():`).
**Actual:** Case-insensitive check is at PR-line **262** (claim was off by 1; `for ident in identifiers:` is at 260).

Surrounding context (lines 257-268):

```
257:         # FR-MOD2.4: Also check for specific mechanism identifiers
258:         if not covered:
259:             identifiers = _extract_identifiers(contract.spec_evidence)
260:             for ident in identifiers:
261:                 for j, rline in enumerate(roadmap_lines):
262:                     if ident.upper() in rline.upper():
263:                         covered = True
264:                         evidence = rline.strip()
265:                         location = f"line {j + 1}"
266:                         break
267:                 if covered:
268:                     break
```

This is the case-folding precedent the F1 fix should mirror in Layer 3 (touch point 4).

---

## Touch Point 6 — F5 fixture comment + TUIBBS_HUB_SPEC

**Claimed:** PR-lines 132-134 in test file.
**Actual:** Comment at PR-lines **129-131**; `TUIBBS_HUB_SPEC = """\` literal opens at PR-line **132**.

Verbatim (lines 129-135):

```
129: # Synthetic fixture per RQ-1 Option A: TUIBBS-scp-inspired prose with shared
130: # UPPER_SNAKE token `FR-S10-02` in every hub-dispatch context window so
131: # `_signature_subsumed` fires deterministically (subset+overlap dedup).
132: TUIBBS_HUB_SPEC = """\
133: ## S10. Message Hub
134:
135: Goal: Route messages through the hub with strict priority semantics.
```

---

## G2 — `c.spec_evidence` occurrences in test file (PR sha)

Three occurrences, ONLY ONE matches the merged-proposal's "list-comprehension filter" pattern:

| Line | Context | Pattern type |
|---|---|---|
| 280 | `evidence_text = " ".join(c.spec_evidence for c in contracts)` | Join-then-substring (in `test_upper_snake_case_detected`) |
| 300 | `uncovered_evidence = " ".join(c.contract.spec_evidence for c in uncovered)` | Join-then-substring (in `test_detects_programmatic_runners_without_wiring`) |
| 333 | `and "FR-S10-02" in c.spec_evidence` | **List-comp filter** (in `test_t1_one_contract_per_hub_mechanism`) |

The merged proposal's claim "only test_t1 uses this pattern" is correct for the **list-comprehension filter** pattern. Lines 280 and 300 use a different idiom (join + substring) that is unrelated to the INV-002 amendment.

---

## G3 — Case-sensitive ident substring checks in production file (PR sha)

`for ident in` / `ident in window` audit (`git show 67ab0af5:src/superclaude/cli/roadmap/integration_contracts.py`):

| Line | Code | Case-sensitivity |
|---|---|---|
| 260 | `for ident in identifiers:` | (loop, not a check) |
| 262 | `if ident.upper() in rline.upper():` | **Case-insensitive** (Layer 2) |
| 355 | `if not any(ident in window_text for ident in contract_idents):` | **Case-sensitive** (Layer 3 — the bug) |

Supplementary `.upper()`/`.lower()` audit confirms: Layer 2 (262), description checks (282, 284), Layer 3 stem-term hit (307), stem-then-line (342), and matched_text classification (384) all normalize case. **Layer 3 line 355 is the sole case-sensitive ident substring check** in the file. Step 7 audit of the merged proposal is satisfied.

---

## G4 — Verification commands

Both commands exist and run from repo root:

- `make lint`: ruff invokes; reports 442 errors on the current master tree (NOT on PR sha — current branch differs from PR branch). The lint target returns `Error 1` from the Makefile. **Command is real and currently produces failures unrelated to PR #86 — task should run lint AFTER checking out the PR branch and applying the fixes, not against the current branch.**
- `uv run pytest tests/roadmap/ --collect-only`: Collected **1693 tests in 0.47s**, exit `0`. Confirms the test discovery path works.

Both are the right verification commands for the MDTM task.

---

## Summary

**6 touch points verified.** Three claims required line-number adjustments:

- Touch point 1: 412-419 → **412-421** (claim missed 2 lines of body)
- Touch point 5: 261 → **262** (off-by-one; `for ident in` at 260, check at 262)
- Touch point 6: 132-134 → comment at **129-131**, literal opens at **132**

**G2 confirmed:** Only `test_t1_one_contract_per_hub_mechanism` (line 333) uses the `c.spec_evidence in` list-comp filter pattern relevant to INV-002.

**G3 confirmed:** Only ONE case-sensitive ident substring check exists — Layer 3 at line 355. The F1 fix is surgically isolated; no other case-sensitive ident sites need amendment.

**G4 confirmed:** `make lint` and `uv run pytest tests/roadmap/ --collect-only` are valid verification commands; lint will need to run against the PR branch checkout (not the current branch) to produce a clean baseline for comparison.

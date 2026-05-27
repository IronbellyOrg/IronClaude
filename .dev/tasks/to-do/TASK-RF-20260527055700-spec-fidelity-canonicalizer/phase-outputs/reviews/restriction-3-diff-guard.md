# Restriction #3 — ≤30% per-patch diff on `structural_checkers.py`

**Verdict:** **PASS**

## Computation

```
git diff --numstat src/superclaude/cli/roadmap/structural_checkers.py
→ 97 additions, 16 deletions  (total churn = 113 lines)

wc -l src/superclaude/cli/roadmap/structural_checkers.py
→ 1069 lines (post-modification)
```

Per-patch diff percentage:

```
(additions + deletions) / total_LOC
= (97 + 16) / 1069
= 113 / 1069
= 10.57 %
```

## Threshold

30 % — referenced in `tests/roadmap/test_remediate_executor.py::test_threshold_is_30_percent` and in `src/superclaude/cli/roadmap/remediate_executor.py` constant `_DIFF_SIZE_THRESHOLD_PCT == 30`.

## Verdict

10.57 % < 30 %. **Well under the per-patch guard.** No tightening needed.

The merged-fix-spec estimated ~20 LOC added + ~10 LOC modified ≈ ~4 %. The actual figure is somewhat higher (10.57 %) primarily because the helper docstring is large (~30 LOC of forward-looking notes preserved verbatim from research/03 per Change 1's verbatim-docstring requirement), and the phantom_id-block replacement comprises ~50 LOC including the explanatory comment and structured drift/phantom partitioning logic. Both expansions are spec-mandated, not gratuitous.

## Audit basis

`git diff --numstat` + `wc -l` direct outputs at restriction-audit time. No fabrication.

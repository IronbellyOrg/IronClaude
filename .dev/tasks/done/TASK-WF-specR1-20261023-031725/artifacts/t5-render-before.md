BASE_SHA=f131592fe3094e222aad17cf82a5b0309ffcdb89
HEAD_SHA=b0de1479267353fa77d56cf9d1b59ee57b27138d

## stdout
::warning title=Mechanical-merge boundary touched::This PR modifies the caller-facing neutrality boundary in src/superclaude/cli/swarm/merge.py or one of its four structural guards. Human review is required before merge -- the merge module is intentionally pinned at <=30 LOC and must remain free of sort / score / dedup / filter / rewrite operations (AC-011, AC-012, NFR-008, NFR-009).

## GITHUB_STEP_SUMMARY
## Mechanical-merge boundary touched

This PR modifies one or more files on the caller-facing
neutrality boundary (T05.05 / FR-012). Reviewers must
verify all four structural guards remain intact:

1. **Docstring contract** -- `merge.py` module docstring
   must still enumerate ALLOWED operations (concat,
   slot-index sort, provenance header) and DISALLOWED
   operations (sort/score/dedup/filter/rewrite/reorder).
2. **<=30 LOC ceiling** -- `merge.py` body must remain
   at or below 30 lines (excluding module docstring and
   imports per NFR-008). Verified by
   `tests/swarm/test_merge_loc_ceiling.py`.
3. **PR-review discipline** -- this workflow flags the
   touch; branch protection must require this check.
4. **Boundary test** -- `tests/swarm/test_merge_mechanical_only.py`
   asserts 3-worker concat preserves slot-index order,
   verbatim bodies, and provenance-header-only output.

### Files touched in this PR

```
src/superclaude/cli/swarm/merge.py
tests/swarm/test_merge_loc_ceiling.py
tests/swarm/test_merge_mechanical_only.py
tests/swarm/test_merge_no_transforms.py
tests/swarm/test_no_scoring_engine.py
```

### Required reviewer checks

- [ ] No new sort / score / rank / dedup / filter / rewrite
      operations introduced into `merge.py`.
- [ ] Module docstring still enumerates ALLOWED and
      DISALLOWED operations.
- [ ] All four guards still listed in the module docstring.
- [ ] If `merge.py` body grew, NFR-008 (<=30 LOC) was
      explicitly revisited and the ceiling deliberately
      raised in the spec -- not silently relaxed in the test.
- [ ] Scoring / ranking work was directed to
      `/sc:adversarial`, not added here.

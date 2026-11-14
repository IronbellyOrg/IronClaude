# Merge Log (Q24)

## Metadata

- Base: Variant 1 (proposal-A), `adversarial/variant-1-original.md`
- Plan: `adversarial/refactor-plan.md` (auto-approved 2026-11-14)
- Executor: merge-executor
- Output: `../merged-proposal.md`
- Changes applied: 5 of 5
- Status: complete, validation passed
- Timestamp: 2026-11-14

## Changes Applied

### Change 1: keep the sweep report before removing the worktree
- Status: applied (replace, base step 5)
- Before: "The worktree is removed after XC-04 is recorded."
- After: the sweep report under `<root>/.dev/sweeps/` (`sweep/commands.py:235-241`) is copied into the ledger package and the copy path recorded in the XC-04 record before the worktree is removed.
- Consistency edit: the base risk bullet about the report in `.dev/sweeps/` now says it must be copied before removal (step 5) or it is lost.
- Provenance: Variant 1 advocate Concession 4

### Change 2: first recorded read settles the shared assumption
- Status: applied (insert, base step 3)
- Before: step 3 had no first-read requirement.
- After: XC-03's first recorded step is one `orca orchestration worker-list --run <id> --json` read from the Run-less terminal, of a non-empty Run held by another terminal, with `page.total` next to the unscoped count; reason and UNVERIFIED label kept from the plan.
- Consistency edit: added an unresolved bullet: whether a Run-less terminal can list another terminal's non-empty Run (UNVERIFIED until that first read).
- Provenance: all three advocates (A-001)

### Change 3: OB-03 stays with the owner by default
- Status: applied (replace, Answer; insert, step 3)
- Before: "The seeded test (OB-03) stays with the owner or a session the owner names under its own permission row."
- After: the owner runs OB-03 and authors its record, unless the owner names another runner in writing under `GRANT(OB-03,seeded-write)`; the capture session never holds that row. Step 3 states the session holds only the XC-03 and XC-04 live-read rows.
- Consistency edit: unresolved bullet "Who runs OB-03; this answer only names the owner's default" became "Whether the owner names another OB-03 runner in writing; by default the owner runs it."
- Provenance: Variant 2 (C-002; INV-014 authorship)

### Change 4: the 409 session advises, it does not run
- Status: applied (append, step 3 and the cold-start risk bullet)
- Before: cold-start risk stated with no mitigation; step 3 gave the session no observer guidance.
- After: step 3 hands the session the observer's verified field list (`src/superclaude/cli/observe/parse.py`) and allows read-only questions to the 409 session if it is alive; the 409 session runs no live Orca command for these items. The risk bullet notes the risk is reduced, not removed.
- Provenance: Variant 3 (X-002) and Variant 1 advocate Concession 2

### Change 5: note that XC-03 alone needs no worktree
- Status: applied (append, "What it costs or risks")
- Before: no statement of which item earns the worktree's cost.
- After: new bullet: XC-03 alone needs no worktree ("CAP runs no git and no sweep": merged-requirements.md line 451); the cost is earned at XC-04, and creating it for XC-03 too keeps one runner and one record.
- Provenance: Variant 1 advocate Concession 5

## Post-Merge Validation

- Structural: pass. One H1 title, then the base's five H2 sections in the base order (Answer; What happens next if the owner picks it; What it unlocks; What it costs or risks; What stays unresolved). Steps remain numbered 1 to 5; inserted content is nested under step 3. No em dashes or en dashes.
- References: pass. Internal references "step 2", "step 3" and "step 5" each resolve to an existing step. Base citations kept unchanged (merged-requirements.md lines 234, 264); plan citations carried as given (`sweep/commands.py:235-241`, `q1-result.md`, merged-requirements.md line 451, `src/superclaude/cli/observe/parse.py`). UNVERIFIED labels kept (409 session alive; Run-less `worker-list` of another terminal's non-empty Run).
- Contradictions: pass. Re-scan found no conflict: "The 409 session is left alone" is consistent with Change 4 (read-only questions only, no live Orca command, no worktree change); the report-file risk now agrees with step 5; the OB-03 statements in Answer, step 3 and the unresolved section agree; the Change 5 bullet does not conflict with step 1 creating the worktree at the start.

## Summary

| Planned | Applied | Failed | Skipped |
|---|---|---|---|
| 5 | 5 | 0 | 0 |

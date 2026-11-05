# Merge Log (M-proof-failure)

## Metadata

- Base: Variant 3 (option C, split by failure class), `variant-3-original.md`
- Plan: `refactor-plan.md` (12 planned changes, 6 rejected)
- Executor: merge-executor (sc:adversarial Step 5)
- Output: `../M-proof-failure-merged.md`
- Changes applied: 12 of 12
- Status: COMPLETE
- Timestamp: 2026-10-30

## Changes

| Change | Status | Target section | Provenance tag used |
|---|---|---|---|
| 1 Fail-closed classifier | applied | 2 Classify the failure | `Variants 1, 2 and 3 (all three advocates, debate X-003, A-001), merged per Change #1` |
| 2 Integrity issue contents | applied | 3 Integrity failure | `Base (original, modified) - expanded per Change #2 from Variant 2 (option B, U-001, C-005) and debate N-002, N-003` |
| 3 Behaviour draft PR details | applied | 4 Behaviour failure | `Base (original, modified) - expanded per Change #3 from Variant 1 (option A, S-002, U-005), Variant 2 (option B, report contents) and debate A-005, A-006, N-004` |
| 4 Infrastructure escalation | applied | 5 Infrastructure failure, plus subsection "Counter mechanism" | `Base (original, modified) - escalation appended per Change #4 ...`; subsection `Variant 2 (option B advocate threshold) and orchestrator proposal (debate N-006), merged per Change #4` |
| 5 Idempotency key and re-run rule | applied | 6.1 | `Variant 2 (option B, C-004, U-002), extended by debate N-005, merged per Change #5` |
| 6 Never push an existing branch | applied | 6.2 | `Variant 3 (option C advocate rule, debate A-002, N-001, Coder precedent), merged per Change #6` |
| 7 Later pass on the same version | applied | 6.3 | `Variant 3 (option C advocate guard, debate A-004, N-003, N-007), merged per Change #7` |
| 8 Newer release supersedes | applied | 6.4 | `Variants 1, 2 and 3 (debate A-003, N-002, N-008), merged per Change #8` |
| 9 Order of operations | applied | 7 Order of operations | `Variant 3 (option C advocate strength 3, spec fact 5), merged per Change #9` |
| 10 Permissions | applied | 8 Permissions | `Variants 1, 2 and 3 (debate A-005, spec fact 4 ...), merged per Change #10` |
| 11 Paths to test | applied | 9 Paths to test, 9.1, 9.2 | `Base (original, modified) - cost line expanded with Variant 2 (option B advocate test list), merged per Change #11`; 9.1 and 9.2 carry their own tags |
| 12 Items for the user | applied | 10 Items for the user | `Variants 1, 2 and 3 (orchestrator-settled N-001, N-002, N-006, N-007 and UNVERIFIED items), merged per Change #12` |

Not a planned change: section 1 Summary (base rationale and cost kept, summary table added as requested) and section 11 Rejected alternatives (one line per row of "Changes NOT Being Made"). Both are tagged `Base (original, modified) - <reason>`.

Notes on application:

- Change 4: the counter mechanism is written as the orchestrator proposal, marked "(proposal, UNVERIFIED, user decides)", with Option 1 as default and Option 2 as the neutral-exit alternative. One clarification was added and marked UNVERIFIED: the current run is still in progress when the `if: failure()` step runs, so its own failure comes from `if: failure()` and the two completed runs before it come from `gh run list`.
- Change 11: "three paths to test" in the base cost line became four terminal outcomes (PASS, integrity, behaviour, infrastructure), as instructed.
- Debate-sourced changes have no single original-text variant. Their tags name the variants whose advocates supported the resolution, using the `Variant N (...), merged per Change #N` form.

## Post-merge validation

### (a) Structural integrity: PASS

- Heading levels: one H1; H2 sections 1 to 11 in the required order; H3 only under H2 (5, 6, 9). No level gaps.
- Every H2 and H3 section starts with a `<!-- Source: ... -->` tag (18 tags for 18 headings below the H1: 11 H2 and 7 H3).
- Header provenance comments present (Provenance, Base, Merge date).
- No em dashes (grep count 0).

### (b) Internal references resolve: PASS

- Change numbers mentioned: #1 to #12. All exist in `refactor-plan.md`.
- IDs mentioned: A-001..A-006, C-001..C-005, N-001..N-008, S-002, U-001, U-002, U-005, X-002, X-003. Each was found by grep in `refactor-plan.md` or `debate-transcript.md`. None missing.
- In-document section references (sections 2, 3, 5, 6, 6.1 to 6.4, 9, 10) all point at headings that exist.

### (c) Contradiction re-scan: PASS (5 new tensions found, all resolved in text)

| New contradiction introduced by the merge | Resolution in the merged text |
|---|---|
| "Never push an existing branch" (Change 6) vs "mark ready" (Change 7) | 6.2 states that `gh pr ready`, the label and the title are PR state changes, not pushes. 6.3 states that an unequal hash table stays draft and the monitor does not push a corrected table; a person fixes it. |
| "Never push an existing branch" (Change 6) vs "delete the superseded branch" (Change 8) | 6.2 states that deleting a superseded bot-only branch is a ref deletion, not a content push, and is the only write the monitor makes to an existing branch. |
| "Never auto-close an integrity issue" (Change 2) vs the PASS path and the infra auto-close (Changes 4, 7) | Section 3 says only a person closes an integrity issue, on a later pass or a newer release. 6.3 says the PASS-path PR links it and it stays open. Section 5 says the infra issue is the only issue the monitor closes on its own. |
| Base "neutral exit" for infrastructure vs Change 4 Option 1 "failed job conclusion" | Section 5 states that Option 1 departs from Coder's neutral exit and that the base rule holds only if Option 2 is chosen. Flagged as item 3 in section 10. |
| Change 5 marker pattern `codegraph-monitor:vX.Y.Z:<class>` (class = infra) vs Change 4 marker `codegraph-monitor:infra` | The more specific Change 4 marker is used for infra, without a version, because the version may be unknown when upstream is unreachable. Change 5's pattern is kept for integrity. Stated in sections 5 and 6.1 and in the summary table. |

Checked and found consistent (no change needed): an integrity failure on a re-run of a version that already has a behaviour draft cannot mark the draft ready, because 6.3 requires a pass in the same run; the fingerprint's branch head SHA is empty for integrity issues (stated in 6.1).

## Summary

| Planned | Applied | Failed | Skipped |
|---|---|---|---|
| 12 | 12 | 0 | 0 |

Rejected changes (6) were not merged; each is listed in one line in section 11.

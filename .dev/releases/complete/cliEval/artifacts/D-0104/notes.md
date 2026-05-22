# D-0104 — Notes

## Design decisions

- **PR count = 6** (harness + 5 eval batches). Harness landing first
  honors R9 (`Harness lands as PR 1 (M1-M4); evals as PR 2+ via MIG-002
  batches of 3-5`).
- **Batch A is sized at 4 to fully clear FR-G5 in one PR.** All three
  v1 matcher families (`mcp__auggie__*`, `mcp__auggie-mcp__*`,
  `mcp__airis-mcp-gateway__*`) are exercised by E1 + E2.1 + E2.2 +
  E2.3, so PR 2 transitions the coverage gate from 0/3 to 3/3 families
  green. Splitting this would leave the gate red across two PRs.
- **Batches B-E partitioned by hook-event domain, not by date or
  author**, so each PR is self-contained for a reviewer who hasn't
  read its siblings.
- **Coverage-map field uses in-file anchors**
  (`docs/eval/mig-002-batch-plan.md#batch-X-coverage-map`) so the
  citation is stable, paste-ready, and resolvable from a PR description
  without leaving the file.

## Counting reconciliation

Phase goal text says "15 evals"; tasklist verification text says
"15 evals (E1, E2.1-3, E3..E15)". Enumerated entries in `real.yaml`
are actually 17 (E2 is a 3-way parameterize). The batch plan lists all
17 enumerated entries — published count "15" is preserved in the doc
header for spec consistency.

## Out of scope for this task

- Authoring batch PR descriptions: that's per-batch follow-up at PR
  time. The plan only locks the structure + the verbatim
  `coverage-map:` field each PR must cite.
- Extending `default_matcher_filter` to cover `mcp__serena__*` or other
  prefixes: design-spec future work (referenced from Batch C section
  as a forward-compat note, but not a v1 deliverable).

## Open follow-ups (post-M5)

- Run the quality-engineer sub-agent review pass and append summary to
  `evidence/T05.27/quality-engineer-review.md`. (Plan content does not
  block on this; the review is a verification step.)
- Once Batch A merges, confirm `eval doctor --check-coverage` reports
  3/3 matcher families covered as a post-condition of MIG-002 Batch A
  DoD bullet.

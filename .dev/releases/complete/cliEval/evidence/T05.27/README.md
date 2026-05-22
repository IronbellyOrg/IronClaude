# T05.27 — Define MIG-002 eval-batch rollout plan

**Status:** complete
**Date:** 2026-05-20
**Roadmap link:** R-103 / MIG-002

## Deliverable

`docs/eval/mig-002-batch-plan.md` — partitions the 17 enumerated `real.yaml` entries (published "15 evals") into 5 reviewable batches (A-E) plus an explicit PR 1 = Harness ordering. Each batch carries a paste-ready `coverage-map: <link>` field anchored within the plan file.

## Artifact set

- `.dev/releases/current/cliEval/artifacts/D-0104/spec.md`
- `.dev/releases/current/cliEval/artifacts/D-0104/notes.md`
- `.dev/releases/current/cliEval/artifacts/D-0104/evidence.md`

## AC verification

See `D-0104/evidence.md` for the per-AC verification trace.

## Open follow-ups

- Quality-engineer sub-agent review pass (T05.27 step 5): output to be appended at `quality-engineer-review.md` in this evidence dir.

# D-0104 — MIG-002 eval-batch rollout plan

**Owner task:** T05.27 (phase-5-tasklist)
**Roadmap link:** R-103 (MIG-002)
**Risk mitigated:** R9 — PR scope creep as evals are added
**Deliverable:** `docs/eval/mig-002-batch-plan.md`

## 1. Summary

The plan partitions the 17 enumerated eval entries in
`src/superclaude/cli/eval/suites/real.yaml` (published as "15 evals"
per design-spec §5: E1, E2.1, E2.2, E2.3, E3..E15) into **5 reviewable
batches** of 3-4 entries each, plus the harness PR. Total PR count:
**6** (PR 1 harness + PRs 2-6 eval batches).

| PR | Batch | Evals | Count | Domain |
|---|---|---|---|---|
| 1 | — (harness) | — | 0 | M1..M4 contract |
| 2 | A | E1, E2.1, E2.2, E2.3 | 4 | MCP matcher coverage + sticky lifecycle |
| 3 | B | E3, E4, E5 | 3 | Session / Prompt lifecycle hooks |
| 4 | C | E6, E7, E8 | 3 | PreToolUse tool-gate hooks |
| 5 | D | E9, E10, E11 | 3 | PostToolUse async + Subagent lifecycle |
| 6 | E | E12, E13, E14, E15 | 4 | Hook resilience (idempotency / fail-open / concurrency / timeout) |

All batch counts fall in the MIG-002 "3-5 evals per batch" envelope.

## 2. Acceptance criteria mapping (T05.27)

| AC bullet (T05.27) | Where satisfied | Evidence |
|---|---|---|
| `docs/eval/mig-002-batch-plan.md` exists; partitions all 15 evals into 3-5 batches. | Doc §3 (5 batches). | All 17 enumerated entries listed; published 15-eval count cited in doc header. |
| Each batch entry lists DoD and the matchers it covers. | Doc §2 (per-batch DoD common bullets) + each batch's "DoD additions" + each batch's "coverage map" subsection (matcher family + suite source rows). | Per-batch coverage-map subsections. |
| Harness PR named explicitly as PR 1 with eval PRs as PR 2+; each batch entry includes a `coverage-map: <link>` field that the corresponding eval PR description cites verbatim. | Doc §1 (PR ordering table names PR 1 = Harness, PR 2-6 = eval batches A-E). Each batch §3 section contains an explicit `coverage-map:` line citing the in-file anchor (`docs/eval/mig-002-batch-plan.md#batch-X-coverage-map`). | Doc §4 (reverse lookup table) gives the paste-ready field per eval. |
| `TASKLIST_ROOT/artifacts/D-0104/spec.md` records the batch plan summary. | This file. | — |

## 3. Coverage-map link policy

Per-batch `coverage-map:` fields point to in-file anchors so the field
is stable across repo moves and copy-pasteable verbatim into a PR
description. Reviewers resolving the link land on the batch's matcher
family + suite source rows + hook-telemetry assertions.

In-file anchors used (verified against doc §4 reverse lookup):

- `docs/eval/mig-002-batch-plan.md#batch-a-coverage-map`
- `docs/eval/mig-002-batch-plan.md#batch-b-coverage-map`
- `docs/eval/mig-002-batch-plan.md#batch-c-coverage-map`
- `docs/eval/mig-002-batch-plan.md#batch-d-coverage-map`
- `docs/eval/mig-002-batch-plan.md#batch-e-coverage-map`

## 4. Cross-references

- Roadmap entry: `.dev/releases/current/cliEval/roadmap.md` row R-103
  (MIG-002).
- R9 risk row: `roadmap.md` M5 risks table (`PR scope creep ... batches
  of 3-5 evals per PR; per-batch DoD recorded; harness merges as PR 1`).
- Coverage gate source of truth: `src/superclaude/cli/eval/coverage.py`
  (`default_matcher_filter`, `_DEFAULT_MCP_TOOL_PREFIXES` lines 103-107).
- Suite manifest: `src/superclaude/cli/eval/suites/real.yaml`
  (1618 lines; eval id rows at 43, 79, 111, 142, 179, 228, 292, 370,
  465, 565, 690, 785, 884, 1014, 1132, 1292, 1435).
- Capability gating cross-link (R9 sibling): `D-0103` (TEST-014
  `--no-mcp` skip semantics).

## 5. Why 5 batches (not 3 or 4)

- 3 batches would have averaged ~6 evals/PR, exceeding the MIG-002
  ceiling of 5 and reintroducing R9 review fatigue.
- 4 batches would either over-load one batch (>5 evals) or split a
  hook-event domain across two PRs, breaking the reviewer-ergonomic
  invariant that each batch is end-to-end-readable in isolation.
- 5 batches stays at the AC ceiling while keeping every batch under 5
  evals and aligning each PR to a single hook-event domain. The slack
  also leaves headroom for a future "Batch F — coverage gate extension"
  follow-up without re-partitioning.

## 6. Sub-agent review

T05.27 step 5 calls for sub-agent (quality-engineer) review for
batching coherence. Review summary lives at
`evidence/T05.27/quality-engineer-review.md` (to be appended after the
review pass). Plan is authored from spec + roadmap + manifest only;
no design decisions remain open.

# Runtime-Entrypoint Verification (H1)

H1 proves that the production / operator entrypoint consumes or rejects the value at the **real boundary**, not at a helper or mock. It closes **E1** (headless `--spec` replay rejects a local-path `--file`) and supports **E4** (proves the live PRD path reaches `_evaluate_gate`). The H1 status feeds the §5.4 verdict aggregation in [`hardening-output-contract.md`](hardening-output-contract.md).

## FAIL rule (FR-3)

H1 **FAILs** if the proof stops at helper construction while the defect can appear only at a subprocess / gate / generated-artifact-parser / persisted-state / review-selector boundary. The replay MUST reach the production boundary; a proof that exercises only a helper, a mock, or an argv-construction step does not satisfy H1.

The H1 evidence card records: producer · transformer(s) · consumer/evaluator · boundary crossed · replay command · evidence the replay reaches the production boundary · external outcome asserted.

## H1 Runtime-Entrypoint Card schema (§5.6)

| Field | Required | Meaning |
|-------|----------|---------|
| `producer` | yes | Component that creates the value/artifact under test |
| `transformers` | yes | Ordered list of layers that reinterpret, serialize, parse, route, or persist the value |
| `consumer_or_evaluator` | yes | Production/operator boundary that ultimately consumes the value |
| `boundary_crossed` | yes | The concrete boundary type reached by the replay |
| `replay_command` | yes | Command or scripted invocation that reaches the production boundary |
| `production_boundary_reach_proof` | yes | Evidence that the replay did not stop at a helper/mock |
| `forbidden_interpretation` | yes when applicable | The bad interpretation the negative witness must expose |
| `negative_witness_command` / `negative_witness_result` | yes | Fix-reverted or accepted-substitute run showing FAIL |
| `positive_witness_command` / `positive_witness_result` | yes | Fix-applied run showing PASS |
| `accepted_substitute_rationale` | required if no literal revert | Why captured pre-fix replay, isolated worktree revert, synthetic contract fixture, or historical log is acceptable |

## Negative-witness requirement (FR-4)

A green H1 is **rejected** unless a negative witness is recorded for every contract with a forbidden interpretation: the oracle run against real captured input, through the production entrypoint, **with the fix reverted, showing FAIL**, paired with the positive (fix applied, PASS). A test that has never been observed to fail (no negative witness) does **not** satisfy H1.

Forbidden-interpretation examples the negative witness must expose:

- a local path treated as a cloud `--file`;
- an `advisory` semantic check treated as fatal;
- dirty `/task` work omitted from the reviewed surface;
- an empty artifact accepted as valid;
- a non-executable heading treated as executable.

## Accepted-substitute-witness classes

When a literal fix-revert is impractical, the negative witness may use one of these substitute classes (the `accepted_substitute_rationale` field must justify the choice):

- captured pre-fix replay,
- isolated worktree revert,
- synthetic contract fixture,
- historical log.

> **OI-3 deferral (PENDING human decision).** The *cheapest reliable public-entrypoint probe per high-risk seam* (especially live Claude/agent execution) is an open item (OI-3). This ref intentionally lists the four substitute classes **without** committing to a single cheapest-probe-per-seam ranking; that ranking is deferred to OI-3. See `phase-outputs/plans/OI-3-PENDING.md`.

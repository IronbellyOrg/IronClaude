| Status | Result |
|---|---|
| DONE | Wrote the three missing Round 3 statements (V3, V4, V5). The debate converged: all 43 disputed points agreed, and all 8 high-severity gaps from the stress test closed. |
| DONE | Scored the five variants and picked Variant 4 as the base. It scored 0.978 against 0.946 and 0.945 for the next two. The margin was under 5%, so the tie-break rule decided it: Variant 4 was the only one to meet all five correctness criteria. |
| DONE | Wrote the merge plan (22 changes) and the merged spec, with all 22 changes applied. It has five sections and five distinct redesigns, each with all eight required elements. |
| DONE | An independent check of the merged spec failed it on two wrong numbers. I fixed both, and the third and final check passed. |
| DONE | Replaced both placeholder return contracts. Both parse as valid YAML, and both report success. |
| NEXT | None needed for this run. The brainstorm orchestrator reads `nested/adversarial-1/return-contract.yaml`. |

The merged spec is at `.dev/brainstorms/20261113-163248-panel-collaboration/nested/adversarial-1/merged-spec.md`. The full debate record is in `adversarial/debate-transcript.md`, and scoring is in `adversarial/base-selection.md`.

Some gain numbers are estimates I chose, not figures the advocates agreed in the debate:
- **Fewer messages per reviewer.** When a reviewer gets one message instead of two (the expected case), I halved each issue's gain. V3 objected to plain halving.
- **Coverage Deflection redesign.** I re-estimated its gain on the sonnet + 2x luna panel at 0.07-0.53 (one message per reviewer) and 0.13-1.06 (two). The harness-fix share on that panel is still unverified.

The spec marks all of these as estimates to be replaced by measured results.

The merge also adapted three details to keep the document consistent; no planned number changed:
- One move is numbered M8 instead of M7, to match the base's move list.
- Moves M2 and M4 were given observable signatures.
- Move Radar's "source.md never opened" check now counts toward its message cap.

The checker's 8 minor wording notes (in `adversarial/merge-review.md`) were not applied. Nothing was staged or committed.

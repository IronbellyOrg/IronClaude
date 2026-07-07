# Adversarial Debate Transcript

## Metadata

- Depth: standard
- Rounds completed: 2 synthesized rounds + invariant probe
- Convergence threshold: 0.75
- Final convergence: 0.88
- Advocate count: 3

## Round 1: Advocate Positions

### Variant 1 — Architect

Argued for an append-only fallback attempt ledger at the reflect/swarm seam. Strongest points:

- Fallback attempts must be visible, not replacement retries.
- Reflect owns quorum semantics; swarm owns transport primitives.
- A slot-family resolver is the cleanest long-term config boundary.
- Verdict contract must remain a pure fact-to-verdict layer.

Concession: the proposed early new helper module could be overkill if the first implementation is small.

### Variant 2 — Analyzer

Argued for a post-primary quorum top-up controller with a precise failure taxonomy. Strongest points:

- Fallback should trigger only from terminal failure classifications after retry and normalization.
- `T1Model02` should run not only on multiple primary failures or `T1Model01` failure, but also when `T1Model01` succeeds without repairing quorum/diversity.
- Terminal fallback reasons should be enumerated in the return contract.
- Diversity repairability should be preflighted and honestly reported.

Concession: adding many new contract fields must be done additively so old readers ignore them safely.

### Variant 3 — Backend/Refactorer

Argued for the smallest safe refactor: a post-normalization top-up ladder localized in `ensemble.py`, with extraction only if needed. Strongest points:

- Keep the first implementation minimal and testable.
- Introduce pure helper seams for planning and contributor selection before wiring live dispatch.
- Use stub integration before real OpenAI-compatible transport wiring.
- Contract fields should distinguish all attempts from contributing reviewers.

Concession: if fallback planning grows, a dedicated `reflect/fallback.py` module is justified.

## Round 2: Rebuttals and Resolution

### Dispatch timing

All variants agree on post-primary top-up. Immediate fallback was rejected because it races normalization/salvage and can spend fallback calls unnecessarily.

Winner: shared consensus.

### Fallback 2 trigger

Variant 2 sharpened the state machine: `T1Model02` should engage when more than one primary fails, when `T1Model01` fails, or when `T1Model01` succeeds but still does not produce a valid quorum/diversity set. This is necessary to satisfy the user’s exact rule plus the diversity invariant.

Winner: Variant 2, with wording merged into final design.

### Helper/module boundary

Variant 3’s staged approach is lower-risk: define pure planning/selection helpers first, extract to `reflect/fallback.py` when the code would otherwise bloat `ensemble.py`. The final design names the extraction boundary but does not require premature broad refactor.

Winner: Variant 3 for sequencing; Variant 1/2 for final boundary shape.

### Reduction and scorer inputs

The merged design resolves the apparent conflict by separating views:

- Attempt ledger: all primary and fallback attempts.
- Contributing reviewer set: successful attempts selected for quorum/diversity.
- Semantic adversarial compare/scorer: contributing successful reviewer artifacts only.
- Metadata/reduce audit: may preserve all attempts in sidecars/contract.

Winner: synthesized hybrid.

### Contract metadata

Variant 2’s terminal-reason enum is the clearest audit surface. Variant 3’s `contributing_reviewer_attempt_ids` prevents ambiguity. Variant 1’s `original_primary_pool_fully_succeeded` communicates the difference between primary-only and fallback-augmented certification.

Winner: synthesized hybrid.

## Invariant Probe

| ID | Category | Assumption | Status | Severity | Evidence |
|---|---|---|---|---|---|
| INV-001 | guard_conditions | Fallback must not trigger before parse salvage has had a chance | ADDRESSED | HIGH | All variants place fallback after normalization/salvage. |
| INV-002 | state_variables | `reviewer_count` must refer to contributing reviewers, not all attempts | ADDRESSED | HIGH | Variants 2 and 3 explicitly separate attempt ledger from final/contributing reviewer set; final design adopts this. |
| INV-003 | interaction_effects | A successful fallback may still fail diversity | ADDRESSED | HIGH | All variants require actual model/vendor diversity computation. |
| INV-004 | sufficiency_challenge | Adding fallback alone is not sufficient unless T1 model slots are resolvable | ADDRESSED | MEDIUM | Final design includes swarm/config model-slot changes and config-missing terminal reason. |

## Scoring Matrix

| Diff Point | Winner | Confidence | Evidence Summary |
|---|---|---:|---|
| S-001 | Variant 3 + extraction boundary | 82% | Lowest-risk sequencing while preserving modular destination. |
| S-002 | Hybrid | 90% | Contract should include both terminal reason and contributor IDs. |
| S-003 | Hybrid | 78% | Swarm should expose slots; reflect should own fallback policy. |
| C-001 | Consensus | 95% | All variants chose post-primary top-up. |
| C-002 | Variant 2 | 88% | Most precise state machine for `T1Model02`. |
| C-003 | Hybrid | 86% | Separate attempt ledger from contributing reviewer set. |
| C-004 | Hybrid | 90% | Additive metadata, no verdict relabeling. |

## Convergence Assessment

- Resolved points: 7 of 8
- Alignment: 0.88
- Status: CONVERGED
- Unresolved tension: exact field names can be finalized during implementation, but the semantic contract is clear.

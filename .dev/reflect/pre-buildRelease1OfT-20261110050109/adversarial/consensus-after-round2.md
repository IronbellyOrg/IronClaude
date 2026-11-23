# Emerging consensus after Round 2 (input to the Round 2.5 invariant probe)

Written by the debate-orchestrator. Per-finding positions are taken from the four advocate transcripts in this folder.

## Diff points (convergence denominator 11)

| Point | Level | R1 final | R2 final | Agreed | Winner |
|---|---|---|---|---|---|
| S-001 granularity | L1 | V2 stronger on test coverage | V1 stronger on design review, V2 on coverage | yes | V2 (coverage breadth) |
| S-002 evidence style | L2→L1 | V1 reads source code | "R1 found the defects that need reading source code" | yes | V1 |
| C-001 cycle budget | L3 | blocking, accepts SPEC:369 | blocking | yes | V2 (stronger citation) |
| C-002 T33 | L3 | upgraded to blocking | blocking | yes | V2 |
| C-003 PARTIAL text | L2 | minor | minor | yes | tie (merged) |
| X-001 T33 severity | L2 | blocking | blocking | yes | V2 |
| X-002 severity rule | L2 | instruction present = minor; missing deliverable/gate = blocking | same rule | yes | V1 (stricter application) |
| A-001 scope of SPEC tests | L2 | QUALIFY | QUALIFY | yes | — |
| A-002 authorization | L2 | QUALIFY | QUALIFY | yes | — |
| A-003 export vs view state | L3 | QUALIFY, then holds minor | REJECT, then holds minor | yes (outcome) | — |
| A-004 numeric order | L2 | REJECT | QUALIFY | no (label split; both keep R1-05 minor) | unresolved |

Convergence: 10 / 11 = 0.91. Taxonomy coverage: L1 2, L2 6, L3 3 (all levels covered).

## Per-finding consensus

| Finding | Consensus | Severity |
|---|---|---|
| R1-01 + QA-05 | confirmed | blocking |
| R1-02 | narrowed (reuse of `_find_orca` is SPEC-prescribed; defect = false "only live call" claim at plan:23 + discovery outside the injectable runner seam, T36 conflict) | blocking |
| R1-03 | confirmed | blocking |
| R1-04 | narrowed; SPLIT: V1 blocking (N:77 credential prohibition unenforceable for free text), V2 minor (wording) | split |
| R1-05 | confirmed | minor |
| R1-06 + QA-02 | confirmed | blocking |
| R1-07 + QA-06 | confirmed | minor |
| QA-01 | confirmed | blocking |
| QA-03 | narrowed | minor |
| QA-04 | narrowed (only shape-error → FAILED (shape) in poll unpinned) | minor |
| QA-07 | confirmed | minor |
| QA-08 | narrowed (NOT AVAILABLE and strip cells already covered) | minor |
| QA-09 | confirmed, narrowed to the inspector half | blocking |
| QA-10 | narrowed (SPEC:45 ties the token to the B view) | minor |
| QA-11 | narrowed (only per-value `as of HH:MM:SS`) | minor |
| QA-12 | narrowed (deviation justified at plan:33 / owner item 5; only the non-failing spike criterion survives) | minor |

## New items surfaced in debate (missed by both cards)

| Item | Consensus |
|---|---|
| T16 scenario matrix (SPEC:373) neither cited nor excluded | holds, blocking (orchestrators axis has no R1 source; sessions x widths part applies) |
| T22 view texts (`k duplicate rows ignored`, `order unknown`, `conflict (time went back)`) not assigned to view/render | holds, blocking |
| Export vs hidden/filtered rows (plan:126, plan:157, SPEC:189) | holds, minor |

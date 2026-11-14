# Round 2 Rebuttal V3

## Responses to criticisms of V3
Citation keys name files in this debate directory: V1R1 = round1-advocate-v1.md; V2R1 = round1-advocate-v2.md; V1R2 = round2-rebuttal-v1.md; V2R2 = round2-rebuttal-v2.md. A colon followed by a number is the line in that file. Original variant references name their sections unless an exact range matters.

The strongest opposing case is shared: V1 supplies enforceable boundaries and a total classifier, while V2 supplies tests and evidence that distinguish intent from effect. Both correctly identify that V3's publication safeguards cannot compensate for an unfinished probe contract. I retain V1 as the structural base and V3's publication safeguards as additions, not a competing implementation skeleton.

1. **Deferred Git argv, V1R1:56 and V2R1:68. Concede the incomplete contract; reject only the suggestion that V3 authorizes arbitrary family prefixes.** V3's Probe seams and argv allowlist says exact base/ancestry arguments are a pre-implementation gate and explicitly denies permission to run arbitrary arguments under those prefixes. That is a safety stop, not a complete allowlist. The gate does not satisfy the requested finished design. Remove the additional read families and their future-argument gate. The merged Git seam admits only the fixed global lock-free prefix followed by the single status template. Root discovery uses the plain-read walk discussed below. There is no deferred Git tuple left to invent at implementation time.
2. **Unnamed GQ-101 base read, V1R1:57 and V2R1:69. Concede without qualification.** V3's active-local definition and base-tree comparison require a baseline and a way to read it, neither of which the design supplies. Calling the comparison a plain read does not establish access to a Git base tree. Drop that mechanism, as already conceded in Round 1. Use changed or untracked package paths from the one status parse per worktree. Unchanged shared committed folders are excluded. A changed package is contention evidence, not proof of a running executor. No extra Git read is needed or authorized.
3. **Missing policy source, V1R1:58 and V2R1:72. Concede, already in Round 1.** Retain V1's proposed non-ready Task-list template as the named source for Task-spec policy text, alongside the ready-Task form. Exact runtime syntax and whether its response contains the required text remain UNVERIFIED. If that evidence is unavailable, live blocked policy remains unknown; do not guess it from path co-location or a ready-only list.
4. **Live release gate, V1R1:59 and V2R1:70. Concede, already in Round 1.** Delete the mandatory disposable-Run gate from this work. Keep indirect locking and consuming-read concerns as named UNVERIFIED risks. The debate authorizes no live check, and labeling a check separately authorized does not make it part of the current acceptance criteria.
5. **Periodic duty without a scheduler, V1R1:60 and the first half of V2R1:71. Hold the duty, not a scheduler deliverable.** A coordinator can be required to call a command periodically without the command installing or implementing scheduling. This remains contract text requiring owner approval. The supplied memory index supports the duty, but its underlying memory file was not inspected, so the historical order is UNVERIFIED. No fixed five-minute cadence is required. Both rebuttals now support this distinction.
6. **Missing contract pins, V1R1:61 and the second half of V2R1:71. Concede, already in Round 1.** Take V1's explicit phrase set, including the exact never-posted sentence and heading, plus its count-free never-as-worker test name. A paraphrase with the same intent is not enough for a literal contract pin.
7. **Missing module enforcement, V1R1:62, and missing field types, V2R1:74. Concede the structural weakness, already in Round 1.** Take V1's typed immutable models, module table and dependency test. Counter-evidence to the stronger claim that V3 never states the distinction: V3 FR-007 expressly separates absent, null and unreadable, and its data-model prose forbids missing booleans becoming false. The semantics exist in V3, but typed fields and rejection fixtures make that requirement harder to lose during implementation. Keep both.
8. **Omitted interrupted-archive blocker, V1R1:63. Concede, already in Round 1.** A present archive marker must produce an explicit blocker, not merely a report annotation. Keep unreadable ledgers as unknown, not automatically unfinished. The separate archive-blocked policy disagreement is resolved below.
9. **No report during an Orca outage without an explicit Run, V2R1:73. Concede, already in Round 1.** An unavailable binding lookup is not a confirmed missing binding. Prefer the root-scoped disk-only report with unavailable coverage and exit 0 after publication. A successful lookup returning no binding still gives exit 2. This proposed exception still needs owner agreement against the seed's literal no-binding criterion.
10. **Idle position unspecified, V1R1:27. Concede, already in Round 1.** Place idle before an explicit final fallback and pin the named rule order. V3's prose definition of idle did not establish its position in the first-match sequence.

## Responses to the open disagreements
### C-010: keep the lock-free prefix and environment, not the version gate

Hold V1. V1R2:22 and V2R2:46-52 now agree that an unsupported global flag should fail the call rather than silently become a locking status call. Historical Git behavior, the exact exit code and its first supported version remain UNVERIFIED here. The merged seam must never retry by removing the safety flag. A failed call produces a stable source-failure reason and unknown Git evidence. Keep the isolated real-Git control test; keep all other subprocess entry points blocked outside that one test. No version probe is necessary for this proposed fail-closed contract.

### C-013: leave feature-branch ancestry unobserved

Hold V1, now also accepted by V2R2:54-58. No extra log read. Use the status result for upstream state and dirt, without treating clean or not-ahead as evidence of merge into the feature branch. Unobserved ancestry stays unknown. I refine the argument in V1R2:68: adding a proven blocker could change could-not-determine to no, even though yes is unreachable. The reason to omit the probe is its additional scope and baseline requirement, not the claim that extra negative evidence can never affect a verdict.

### C-023 and X-008: keep a coordinator duty without building a scheduler

Hold V3, consistent with V1R2:69 and V2R2:60-64. Periodic calls made by the coordinator do not turn the sweep into a standing service. Require the duty in the proposed contract text, keep actual scheduling machinery and fixed cadence outside Phase 1, and retain owner approval of the text. The underlying historical memory entry remains UNVERIFIED. Neither rebuttal now maintains an opposing implementation choice on this point.

### C-012: accept a plain root walk with file and folder fixtures

Change to V2 with V1's acceptance-test refinement. V1R2:24 and V2R2:66-76 provide a concrete smaller design: walk upward from the current directory, accepting a `.git` file or folder, and return that directory as the candidate worktree root. Do not follow a gitfile to the main checkout merely to find the current root. Add both fixture shapes and a no-repository usage-error fixture. The status read remains subject to the existing seam and failure handling.

One factual correction to V2R2:38 and V2R2:68: my Round 1 C-012 row said **V3's** root method was unspecified, not V2's. It did not claim V2 omitted its path walk. That does not rescue my preference for a subprocess: the now-explicit file-or-folder acceptance criteria make V2's walk the better bounded default. No general equivalence to every Git discovery configuration is claimed; broader cases are UNVERIFIED and not a reason to add arbitrary root probes.

Consequently C-009 and X-004 also change. The merged direct Git allowlist has only the fixed status template after the fixed global prefix. Remove root rev-parse, feature-branch log and branch-family gates. This resolves the remaining exact-argv disagreement rather than deferring it.

### X-006 and C-006: accept archive-blocked as an explicit no reason

Change to merge V1+V2. V1R2:26 and V2R2:80 are persuasive that incomplete archive disposition should remain a named retention condition. Use V1's complete state set, including unknown and interrupted archive, with V2's explicit archive-blocked removal blocker. This does not label archive-blocked work unfinished, failed or unadmitted; it means the archive condition remains unresolved and removal is not proposed.

I do not adopt the rebuttals' claim that this changes no verdict: adding this blocker can change could-not-determine to no when no other blocker is known. It remains the safer and more explicit proposed policy. Keep the distinction from an unreadable ledger: unreadable evidence cannot invent a FINAL line or an archive-blocked state. No archive repair or deletion advice follows from either state.

### Additional convergence on C-003

Accept V1R2:18 and V2R2:89: preserve Orca's observed exited verdict in the unknown row's note and make the current runtime evidence limitation visible next to rule 2, not buried only in model definitions. Stalled proof is a synthetic-fixture capability until the required completion and fencing evidence mapping is actually available. This earns V2 a substantive contribution to C-003, alongside the V1 predicate and V3 unknown-evidence rule. Independent contract-based waiting and guard-refused finished evidence still follow their own precedence; not every row with an exited observation must lose other sufficient evidence.

## Updated per-point positions
Only changed preferences are listed. No confidence-only changes are made. Six of the 75 S/C/X rows change; all other Round 1 preferences retain their stated limits.

| Point ID | Old | New | Reason |
|---|---|---|---|
| C-003 | merge V1+V3 | merge V1+V2+V3 | Add V2's exited-verdict note and explicit current-runtime evidence limitation beside V1's strict predicate and V3's unreadable-evidence rule. |
| C-006 | V1 | merge V1+V2 | Keep V1's unknown and interrupted-archive states; add V2's archive-blocked removal blocker without calling that state unfinished. |
| C-009 | V1 | merge V1+V2 | Keep the narrow direct Git seam, but use V2's plain-read root walk so even root rev-parse leaves the allowlist. |
| C-012 | V1 | merge V1+V2 | Adopt V2's upward root walk with V1's explicit file-or-folder acceptance fixtures and no-repository failure case. |
| X-004 | V1 | merge V1+V2 | Only the fixed status form remains after the fixed global prefix; no log, branch, version or rev-parse probe. |
| X-006 | V1 | merge V1+V2 | Archive-blocked becomes an explicit no reason; unreadable ledger stays unknown and interrupted archive remains blocking. |

Unchanged: all other rows

## Shared assumptions and remaining limits
No A-NNN decision changes. A-004, A-101 and A-103 already say QUALIFY in my Round 1. Their existing conditions retain unknown completion/fencing evidence, indirect Orca Git effects and unverified runtime mappings as explicit limits. A-107 remains REJECT: there is no evidence that typical Runs fit inside the cap. None of these positions gains certainty merely because the advocates agree.

For A-004 and A-103, carry the C-003 explanatory note into reports whenever missing proof makes the row unknown. Do not suppress independent, sufficient earlier-rule evidence. For A-101, scope the direct lock-free claim to the sweep's own Git seam and retain indirect Orca effects as UNVERIFIED. No live launch is part of Phase 1 acceptance.

There is no remaining implementation-choice disagreement with the two rebuttals on the specifically requested Git, root, cadence and archive-blocked topics. Two reasoning corrections remain: the earlier unspecified-method criticism concerned V3, not V2; and new no reasons can change an unknown verdict even though yes is unreachable. These corrections do not block the converged design.

Still open outside advocate voting: owner approval of WC-14 wording and the disk-only outage exception, exact Orca response and continuation mappings, completion/fencing evidence availability, and indirect read-only effects. These remain UNVERIFIED where unchecked, not resolved by a majority vote.

Only the requested debate output was written. No code, QA files, Git mutations, live commands or runtime tests were performed. Recommended next step is to merge the converged requirements while preserving the named owner gates and evidence limits.

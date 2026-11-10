# Round 1 Advocate C

## Position

Variant C supplies the strongest transaction and response contract: retries cannot consume extra reviews, stale answers cannot advance the run, and a sweep blocker cannot coexist with a final clean PASS. Merge that foundation with A's component boundaries and B's traced failure analysis, but correct C's experiment contradictions, replace its unsupported optimistic forecast, and do not confuse fewer admitted findings with fewer document defects.

## Steelman of Variant A

A offers the clearest maintainable division of work. Section 2 makes the kernel the "ONLY writer of ledger state", separates its contract from the adapter, and hands fresh verifiers a generated plan rather than another prose report to reinterpret. Section 3 refuses regrading and forbids reopening untouched accepted text, directly addressing moving goalposts without requiring one persistent reviewer conversation.

A also resists a measurement shortcut. Section 9 says "counting the ledger alone would let the ledger win by not looking" and includes sweep findings in its headline proxy. Its strongest case is a small reusable kernel, predictable review packets, and visible evidence of remaining defects, not merely a nicer status table. Those strengths should survive the merge even where its outcome and coordinate rules need correction.

## Steelman of Variant B

B provides the strongest account of what actually causes work to grow. Section 1 traces the minor F22 edit into blocking N5 and then N12, explicitly showing how "A prose rule lost to a brief." Section 5 concedes that "the review surface does not shrink much" because the real blockers already had changed-line anchors. That is important counter-evidence against claiming that narrow VERIFY alone solves convergence.

B also makes the strongest experimental challenge to its own proposal. Section 9 adds baseline sweeps and predicts "P3s: mean about 5.5", while section 10 explains that "The reviser still writes the defects." Its fresh sweep and separate final outcome protect against declaring success merely because discovery moved later. Its strongest argument is that ledger machinery should be tested as a limited control on edits and counting, not sold as an automatic improvement in semantic quality.

## Key strengths claimed

1. **Retries and races have explicit meanings.** C section 6 requires a "nonblocking OS advisory lock", `--op`, and `--expect-seq`. "An identical op and request digest returns its original prefix-derived result without appending"; changed content under the same operation is refused. This is real idempotency, unlike treating a repeated command that errors as equivalent to recovering its result. The lock and sequence check protect against duplicate dispatch even when one coordinator is the intended writer.
2. **The ledger has one authoritative history.** C section 3 says "The only authoritative state is ledger.json" and "A row's current status is obtained by replaying events." Section 6 publishes immutable dependencies before committing their references and describes crash outcomes on either side of ledger publication. Reports can be rebuilt without guessing whether a report footer or a separate status object won a partial update.
3. **Actor responses are bound to the state they reviewed.** C section 2 says packets bind "response schema, round, document hash and ledger sequence". Section 6 requires exact answer coverage, snapshot-range evidence, and closed input shapes. A syntactically valid answer from an older session cannot silently certify a newer revision. This is validation of evidence, not authentication of the actor or proof that its judgment is true.
4. **Clean PASS is a delivery contract, not a provisional count.** C section 4 says "Before sweep completion, PASS is explicitly loop_decision, never delivery_outcome" and "no final PASS artifact is emitted early." A new sweep blocker, challenge to an old verification, or unresolved uncertainty forces delivery escalation. This genuinely improves A's contract while making B's two-stage outcome explicit.
5. **Edit ownership is checked before acceptance.** C section 3 requires "each changed old/new line" to belong to a submitted blocking-row span; uncovered edits fail admission. Section 6 keeps raw hunks for ownership and excludes whitespace-only changes only from discovery. This closes the path where skipping an optional check admits unrelated edits. It does not prove that a claimed edit was necessary.
6. **Deletion and relocation have defined failure outcomes.** C section 3 says "An empty replacement is a tombstone, not proof of resolution" and rejects silent nearest-match selection for repeated quotes. Section 6 retains old deletion spans and new insertion boundaries. Missing or ambiguous evidence cannot turn into a successful verification simply because the offending words disappeared.
7. **Operational uncertainty is surfaced instead of rounded down.** C section 4 uses integrity `I`, structural failures `X_r`, and an explicit pending result. Section 6 separates successful operation execution from document outcome: "callers inspect JSON, never infer PASS from process success." Section 11 openly limits the system to local storage and calls its history "crash safety, not tamper-proof audit storage".

## Weaknesses identified in Variant A

1. **Its final verdict can contradict its evidence.** A section 2 says "Sweep rows never change the verdict"; section 11 accepts that "a PASS can stand next to sweep: 2 blocking". This fails the goal of a clean PASS or justified escalation. C section 4's separate delivery outcome fixes that without permitting another automatic fix cycle.
2. **Scope enforcement can be bypassed by omission.** A section 11 says "unattributed hunks are reported, not refused" and that rows can verify without answers under `W-NO-ANSWERS`. Reporting is useful, but cannot mechanically stop the minor-edit chain that B traced. C section 3's admission check is stronger, provided refusals include a safe recovery path.
3. **Its retouch check compares incompletely specified coordinates.** A section 3 describes hunks as "new-file line ranges", while its stored example span belongs to the prior snapshot. Requiring overlap without old-side ranges or relocation can miss a retouch when earlier lines move. C sections 3 and 6 retain snapshot-qualified mappings and both sides of the diff. This is X-020, not a stylistic preference.
4. **Its early stop changes policy without evidence of necessity.** A section 4 escalates at review 2 when `B(2) >= B(1)`. B section 4 explains that the analogous proxy decreased in all six observed S1 runs, while C preserves the existing cap without importing rf-qa's policy. Equal counts can also conceal replacement of difficult blockers with simpler ones. Preserve rf-qa's stricter rule in its own adapter instead of adding it to spec-panel.
5. **Its reusable-profile claim is too broad.** A section 6 says an adopter requires "one table entry plus one parametrized test row, never a change to the transitions or the decision formula." Yet C section 7 identifies rf-qa's ordered halt guards and implement's mandatory fresh FINALs. Reuse storage and validation; do not assume every tool's authority and stop policy reduce to severity plus a cap.

## Weaknesses identified in Variant B

1. **Atomic replacement does not prevent lost updates.** B section 7 acknowledges that "two parallel QA instances on one ledger lose updates" and defers locking. Even a nominally single-writer experiment can receive retried or overlapping dispatches. C section 6's lock, expected sequence, and request identity are preferable before admitting any mutations.
2. **The blocking contract has a missing input.** B section 6 promises "CRITICAL and FR-8/FR-9 are blocking", but its `add` schema has no rule or criterion field and accepts reviewer-supplied `sev`. A and C instead derive blocking from an explicit profile and criterion. B's current contract cannot mechanically enforce its own stated FR exceptions, as X-016 observes.
3. **Its scope gate remains optional in effect.** B section 12 says that a reviser skipping `revise-check` "does not stall the loop" because `open` only records unclaimed hunks. That avoids an unattended refusal but also admits the very scope expansion being tested. C's admission boundary is stronger. Automatic `revert-unclaimed` is not a substitute for a preimage check and explicit authorization to discard live edits.
4. **Its dispute representation is inconsistent.** B section 3 T4 preserves status and sets `claim.action=disputed`, while T8 starts from a status named `disputed`. That ambiguity matters to exact row coverage and unresolved counts. Keep the five-state model and represent a dispute as evidence, not a sixth state introduced accidentally. C conservatively escalates unresolved disputes; a later human ruling needs a separate explicit contract.
5. **Its headline metric needs identity-based deduplication.** B section 9 defines P3s as P3 "plus the sweep's rows" without specifying the union rule A and C provide. A fresh blinded sweep may rediscover an open row. Counting it twice inflates failure; discarding a challenge to a verified row hides failure. Keep B's baseline sweeps, but adjudicate duplicates and challenges before applying either arm's bar.

## Concessions

1. **X-018 is a real contradiction, not a wording issue.** C section 9 promises "Only authored brief change" is an invocation substitution, but section 2 makes the coordinator run every mutation and section 11 requires four reviewer sessions. The existing fixed dispatch cannot acquire that behavior from a renamed command alone. Keep actor briefs unchanged apart from the invocation, but explicitly preregister the coordinator state checks and added sweep dispatch as treatment changes. B section 9 is more honest about the sixth session. If the one-line restriction also forbids coordinator changes, C as written is not executable under that restriction; report the conflict instead of claiming compliance.
2. **X-019 requires removing the resumable-default claim.** C section 3's random run directory cannot be re-derived after losing its path. For version 1, require the same explicit absolute ledger path on initialization and resume, with no random default selection by the command. A random run id can remain metadata. If the path is lost or missing, stop, never silently create a replacement FIND. A's deterministic location is more convenient, but silently choosing among runs is unacceptable.
3. **X-011 changes the metric, so C's forecast is not comparable as printed.** C section 9 counts every unverified CRITICAL/MAJOR row, including deferred MAJOR notes. A and B omit those notes from their raw unresolved sets. Counting them is conservative, but it changes the historical proxy's population. Preregister a common, independently adjudicated end-state proxy for both arms, deduplicate sweep identities, include challenges to verified rows, and publish deferred MAJOR notes separately. Until controls are rescored under the same rule, do not compare C's 1.5 directly with control 6.0 as an estimated treatment effect.
4. **C's optimistic forecast is unsupported.** Section 9 predicts headline counts 1 and 2, mean 1.5, and growth 20% and 25%, mean 22.5%. Its stricter count and missing trace-based derivation do not justify the lowest forecast. B's roughly 5.5 combined proxy and 23% growth are better planning estimates, still unmeasured and not transferable without adjustment to C's stricter mechanism. The quality bar of 3 may fail even if the growth bar of 44.4% passes. Keep control 6.0 and 63.5% as the supplied reference, not proof that C will beat it.
5. **C's one-row discovery quota is arbitrary.** C section 2 permits only C001 at review 2 and no discovery at review 3. It can record a later N12-like harm as an escalation observation, but should retain the complete structured allegation for audit and measurement rather than make identity depend on an exhausted quota. Prefer finite changed-range packets in both VERIFY rounds, with explicit completeness and overflow escalation; a row-count cap must not suppress evidence. Large repairs may justifiably escalate, but that is not convergence.
6. **The extra sweep violates a literal three-assessment interpretation.** C section 4 correctly admits "Do not claim the total number of assessments is three." Three remediation reviews plus one terminal sweep is the proposed contract, not three total assessments. Obtain an explicit policy decision if the goal instead means three total reviewer assessments. Neither renaming the fourth pass nor running it in the third session resolves that semantic conflict.
7. **Other limits remain real.** A shared operating-system account can bypass the helper, freeze can preserve an inflated first grade, and exact evidence does not prove a correct fix. C's supporting-context rule does not define enough dependency coverage to prevent cross-section regressions. Its duplicated schema validator needs executable parity fixtures; its durability machinery needs measured cost and filesystem tests. For this debate I read the supplied variants, diff analysis, and brief, not the underlying experiment logs or implementation sources, and ran no implementation tests.

## Shared assumptions

- **A-007: REJECT.** Freezing severity cannot prevent brief-driven inflation before the freeze. C section 11 already admits bad first-pass grading, but none measures this pressure. Retain raw review-1 grades and obtain blinded independent grading under the same rubric in both arms; report disagreement rather than silently modifying frozen operational rows.
- **A-008: QUALIFY.** Early termination is valid only if the dispatcher checks the authoritative next action before every actor launch and no previously launched reviser remains active. A refused ledger transition does not undo edits to the live document. Add and test that dispatch gate, record terminal bytes, and treat later live-document changes as an integrity failure. This is a disclosed coordinator change, not an assumed property of unchanged briefs.
- **A-009: REJECT.** A unique initial quote can later disappear or become duplicated. Use C section 3's snapshot-qualified relocation, exact context, and missing/ambiguous outcomes for every live row; unchanged status is not proof of a valid anchor.
- **A-010: REJECT.** Removing a requirement can create harm without leaving any new-side quote. C section 6's old ranges and tombstone boundaries are necessary evidence locations, followed by a semantic check that deleting the obligation was legitimate.
- **A-011: REJECT.** A remote change can contradict a previously correct fix without touching its sentence. C's undefined supporting context is not enough. Record explicit supporting passages and requirement dependencies, invalidate verification when those change, and escalate uncertain dependency coverage. Keep the independent sweep for undeclared interactions; do not claim this completely solves semantic dependency discovery.
- **A-012: QUALIFY.** Historical review-1 counts are useful planning priors, not invariants. Knowing FIND is unique, writing structured rows, and responding to an unchanged aggressive brief can alter findings and grades. Measure review-1 count, grading distribution, output cost, and blinded grading disagreement; condition forecasts on those observations instead of assuming Arm B equivalence.

## Positions table

Preferences select the strongest supplied approach unless `none` explicitly proposes a correction absent from all three. Forecast preferences rate support for the estimate, not a measured result. Cross-variant combinations retain their useful parts, not every quoted claim.

| Point | Preferred | Reason |
|---|---|---|
| S-001 | A | Specific titles expose compatibility obligations instead of hiding adopter differences. |
| S-002 | B | Explicit citation aliases and unverified markers make provenance easier to audit. |
| S-003 | B | Actor, input, output, and call order are visible together. |
| S-004 | A | Kernel, contract, and adapter boundaries clarify ownership; adapter policy still needs testing. |
| S-005 | C | Replay avoids inconsistent current-state and history stores in this bounded ledger. |
| S-006 | B | Numbered transitions and phase columns improve coverage, after fixing disputed-state inconsistency. |
| S-007 | B+C | Combine worked decisions with explicit integrity, pending, and delivery states. |
| S-008 | B+C | Use a command table plus closed schemas and transaction guarantees. |
| S-009 | C | Fixtures and crash-boundary tests directly exercise persistence and evidence failures. |
| S-010 | B | Trace-based estimates expose assumptions better than unsupported optimistic point forecasts. |
| S-011 | B | Evidence, residual causes, and self-attack prevent overstating what the ledger fixes. |
| S-012 | C | Local labels distinguish structural enforcement from semantic judgment where each rule appears. |
| S-013 | C | Schemas, fixtures, and recovery guidance support an executable contract rather than prose alone. |
| S-014 | B | An explicit unverified inventory is more honest than prematurely declaring completion. |
| S-015 | A | Moderate prose and tables are easier to scan than either dense aliases or repeated labels. |
| C-001 | C | Closed event schemas, stable operations, and replay provide a precise durable contract. |
| C-002 | B | Require an explicit ledger path; missing identity must not create a new run. |
| C-003 | C | Snapshot admission and old/new diff ranges bind each accepted revision to its evidence. |
| C-004 | C | Coordinator-owned mutations keep model responses as untrusted evidence, not direct state changes. |
| C-005 | C | History-derived reopening and retouch invalidation preserve the meaning of prior verification. |
| C-006 | A+C | Preserve unresolved state and dispute evidence; do not invent an ambiguous disputed status. |
| C-007 | A+C | Escalate grading disputes; avoid a waiver API whose quoted authority cannot be authenticated. |
| C-008 | C | Freeze issue text as well as severity so verification cannot redefine the original defect. |
| C-009 | A+C | Compute blocking from an explicit criterion and profile, never reviewer-supplied blocking labels. |
| C-010 | C | Incomplete evidence, uncertainty, and integrity failures cannot yield an accidental PASS. |
| C-011 | B+C | Every unresolved blocker affects delivery; keep loop and sweep counts explicit and nonoverlapping. |
| C-012 | C | Count the extra assessment honestly; session naming cannot erase its cost. |
| C-013 | C | Distinct provisional and delivery outcomes prevent publishing PASS before the sweep. |
| C-014 | B+C | Preserve spec-panel's cap; structural uncertainty escalates without importing rf-qa's monotonicity policy. |
| C-015 | B+C | Combine admission refusal for note-sponsored edits with measured minor-span touches. |
| C-016 | none | Inspect finite changed packets both rounds; retain all allegations and escalate incomplete coverage. |
| C-017 | C | Reject uncovered edits before acceptance; recording them later does not enforce scope. |
| C-018 | C | Exact context and snapshot identity disambiguate anchors without trusting line hints alone. |
| C-019 | C | Explicit relocation and deletion tombstones avoid silent nearest-match errors. |
| C-020 | C | Raw ownership and dual-sided ranges preserve deletions and whitespace-sensitive evidence. |
| C-021 | C | Snapshot-range evidence and cannot-verify distinguish uncertainty from an asserted resolution. |
| C-022 | none | Track explicit dependency passages; invalidate verification when relevant remote supporting text changes. |
| C-023 | C | Hunk overlap proves location, not causation; preserve independent causal adjudication. |
| C-024 | A+C | Add accidental-edit checksums to packet binding; neither mechanism authenticates deliberate editors. |
| C-025 | C | Locks, sequence checks, durable publication, and stable operation retries prevent lost or duplicate reviews. |
| C-026 | B | Its installation naming analysis supplies the clearest packaging and activation contract. |
| C-027 | C | Machine-readable outcomes separate successful commits from review decisions and operational failures. |
| C-028 | B | Drift tests preserve the panel while explicitly excluding unsupported unattended behavior. |
| C-029 | C | Generate reports from authoritative state rather than combining conflicting model tables and computed tails. |
| C-030 | B+C | Even review-1 PASS requires an independent terminal sweep under the proposed sweep policy. |
| C-031 | C | Merge before assigning identities; ledger cleanliness cannot grant promotion authority. |
| C-032 | C | Preserve regression, monotonicity, and cap order rather than flattening rf-qa's stop rules. |
| C-033 | B+C | Defer adoption; any later sidecar must preserve mandatory fresh independent FINALs. |
| C-034 | C | Session continuity is optional; packet identity and file state remain authoritative. |
| C-035 | none | Preregister one deduplicated proxy for both arms; report deferred MAJOR notes separately. |
| C-036 | B | Its conservative estimate has trace-based support and acknowledges likely quality-bar failure. |
| C-037 | B | Byte-share arithmetic is stronger evidence than an unexplained growth forecast. |
| C-038 | B+C | Preserve fixed bars and spread rules; add baseline-sweep, leakage, and operational failure checks. |
| C-039 | none | Disclose coordinator gating and the added sweep separately from unchanged actor brief text. |
| C-040 | B+C | Baseline sweeps detect hidden defects; hashes and snapshot comparisons verify actual treatment activation. |
| C-041 | B+C | Count the sixth session and all calls; distinguish estimates from observed durations. |
| C-042 | none | Calibrate resource limits before preregistration; arbitrary discovery quotas must never discard evidence. |
| C-043 | A+C | Preserve pinned cap tests and history-derived refusal of repeated FIND, extra fixes, and sweeps. |
| X-001 | B+C | A sweep blocker prevents final PASS without authorizing another automatic fix cycle. |
| X-002 | B+C | A fresh terminal reviewer reduces anchoring; count its extra session explicitly. |
| X-003 | B+C | No evidence requires an additional spec-panel monotonicity stop; retain adopter-specific guards separately. |
| X-004 | none | Both VERIFY rounds need complete bounded packets, not C's arbitrary one-row discovery allowance. |
| X-005 | C | Admission must reject unclaimed edits even when a reviser skips optional checks. |
| X-006 | C | One mutation owner plus typed evidence simplifies coordination and retry responsibility. |
| X-007 | C | A committed escalation is operational success; consumers must inspect the explicit decision field. |
| X-008 | B | Missing explicit ledger identity must stop execution rather than select a new run. |
| X-009 | B | Its explicit omission avoids claiming an unattended contract the variant has not established. |
| X-010 | B | Presence-only baseline checks do not justify changing unrelated installation lists. |
| X-011 | none | Reconcile deferred-MAJOR treatment through a common rescored proxy before comparing headline counts. |
| X-012 | B | Trace-based pessimism is more credible than C's unexplained lowest forecast. |
| X-013 | B+C | FIND alone is not independent validation; terminal PASS still needs the fresh sweep. |
| X-014 | A+C | The script derives blocking from criteria instead of trusting reviewer-selected severity classes. |
| X-015 | B | Preserve original resolution plus an explicit graded child; do not accept an unexplained broken-sentence flag. |
| X-016 | A+C | Include criterion in the input and derive FR blocking mechanically. |
| X-017 | A+C | Keep dispute evidence separate from the five-state status machine. |
| X-018 | none | Admit additional coordinator and dispatch changes; one-line substitution alone cannot execute C. |
| X-019 | B | Require an explicit persistent path; keep random identifiers as metadata, not resume discovery. |
| X-020 | C | Snapshot-qualified relocation and old/new diff ranges avoid cross-version coordinate comparisons. |
| X-021 | B+C | Require a supported fix or explicit dispute ruling; unanswered rows cannot silently become verified. |
| A-007 | none | Measure blinded review-1 grading disagreement; frozen grades do not prevent initial inflation. |
| A-008 | none | Gate every dispatch on terminal state and detect edits from already-running revisers. |
| A-009 | C | Relocate every live anchor and escalate missing or ambiguous mappings. |
| A-010 | C | Old-side evidence and deletion boundaries allow lost obligations to remain reportable. |
| A-011 | none | Explicit dependency passages must invalidate verification when remote supporting text changes. |
| A-012 | none | Measure changed FIND behavior; historical initial counts are priors, not treatment invariants. |

# Research: Repeated oracle-task QA failures

**Investigation type:** Pattern Investigator / Code Tracer  
**Scope:** Session `a9b88895-5374-4cae-8ebb-cac03a97aff1`, especially the claim-gate oracle task (Task 12).  
**Status:** Complete  
**Date:** 2026-10-23


**Persistence note:** Main session transcribed the dedicated analyst return verbatim from its on-disk transcript because that agent cannot write reports. This does not claim producer-authored disk delivery.

## 1. Finding and counting boundary

**This session contains two actual failed independent reviews of Task 12, followed by one passing review after an explicitly authorized fixture correction. The second failure retained one already-known frozen-fixture defect; it did not introduce a new requirement or identify a regression caused by the preceding repair.**

The first review identified four distinct defects. The permitted repair fixed three and deliberately left the fourth unchanged because the orchestrator prohibited modifying its frozen fixture or adding duplicate retention coverage to conceal the omission. The second review confirmed the three repairs and failed on precisely that remaining defect.

Do not count the following as additional failed reviews:

- Repeated deliveries, split messages, and idle notifications from the same reviewer.
- Task 11 failures described in the opening carryover instructions and existing ledger. This session was explicitly told not to re-review that task.
- Two local test failures during initial oracle development.
- The later archive refusal because a separate operator-written archive ruling was missing. No fresh final review had occurred at that point.

**Key Takeaways**

- Four unique defects, two failed review rounds, one later passing review.
- One finding persisted across both failed rounds.
- No new post-repair defect was established.

## 2. Evidence register

**Main session**

`/config/.claude/projects/-config-workspace-IronClaude--dev-worktrees-auggie-claim-gate/a9b88895-5374-4cae-8ebb-cac03a97aff1.jsonl`

**Builder trace**

`/config/.claude/projects/-config-workspace-IronClaude--dev-worktrees-auggie-claim-gate/a9b88895-5374-4cae-8ebb-cac03a97aff1/subagents/agent-aoracle-builder-6889f23314fbb16e.jsonl`

**Managed plan**

`/config/workspace/IronClaude/.dev/worktrees/auggie-claim-gate/.dev/tasks/to-do/TASK-WF-designV2-20261020-132032/TASK-WF-designV2-20261020-132032.md`

**Authoritative design source**

`/config/workspace/IronClaude/.dev/worktrees/auggie-claim-gate/.dev/tasks/to-do/TASK-WF-designV2-20261020-132032/source.md`

**Original family and retention requirements**

`/config/workspace/IronClaude/.dev/worktrees/auggie-claim-gate/.dev/brainstorms/20261020-043737-auggieClaimGate/merged-requirements.md`

**Independent failed reviews**

- `/config/workspace/IronClaude/.dev/worktrees/auggie-claim-gate/.dev/tasks/to-do/TASK-WF-designV2-20261020-132032/artifacts/t12-review-1.md`
- `/config/workspace/IronClaude/.dev/worktrees/auggie-claim-gate/.dev/tasks/to-do/TASK-WF-designV2-20261020-132032/artifacts/t12-review-2.md`

**Passing authorized-correction review**

`/config/workspace/IronClaude/.dev/worktrees/auggie-claim-gate/.dev/tasks/to-do/TASK-WF-designV2-20261020-132032/artifacts/t12-review-authorized.json`

**Preserved original frozen fixture**

`/config/workspace/IronClaude/.dev/worktrees/auggie-claim-gate/.dev/tasks/to-do/TASK-WF-designV2-20261020-132032/artifacts/t12-held-back-before-authorization.json`

**Current oracle**

`/config/workspace/IronClaude/.dev/worktrees/auggie-claim-gate/tests/skills/test_auggie_claim_gate_oracle.py`

**Key Takeaways**

- Graph coverage reported the investigated worktree paths excluded from its index. Conclusions therefore rely on direct source reads, historical tool payloads, fixture-byte comparison, and preserved execution logs, not graph absence.

## 3. Actual review and repair timeline

Raw anchors below refer to the main session unless expressly identified as builder-trace anchors.

| Raw anchor | Timestamp, UTC | Actual event |
|---|---|---|
| 139 | 2026-10-21T21:33:52.744Z | Builder assigned Task 12. Instructions require frozen tokens, then held-back corpus and hash, then oracle authoring. Explicitly freeze held-back bytes and forbid tuning from acceptance outcomes. |
| Builder 52 | 2026-10-21T21:35:16.358Z | Held-back generator authored. Shared facts default `default_path` to false. The security-retention constructor does not override it. |
| Builder 55 | 2026-10-21T21:35:18.945Z | Held-back generator executed before oracle creation. |
| Builder 65 | 2026-10-21T21:38:23.677Z | Initial oracle written, including unverified guard/producer rejection predicates. |
| 256 | 2026-10-21T21:43:01.005Z | First independent reviewer dispatched against the original task and parent requirements. |
| **291** | **2026-10-21T21:47:06.709Z** | **First FAIL / missing delivered. Four findings.** |
| **383** | **2026-10-21T21:49:47.309Z** | **ONE allowed repair authorized for findings 1-3 only. Finding 4 explicitly excluded because its fixture was frozen.** |
| Builder 189-196 | 2026-10-21T21:51:40.984Z through 21:51:41.074Z | Actual predicate and provenance corrections applied. |
| Builder 206-211 | 2026-10-21T21:52:07.011Z through 21:52:07.083Z | Actual structural-family corrections applied. |
| Builder 223 | 2026-10-21T21:55:55.589Z | Runnable verification, provenance, and structural regression assertions added. |
| **398** | **2026-10-21T21:56:52.809Z** | **Builder returns corrected paths and preserved evidence.** |
| 414 | 2026-10-21T21:57:25.078Z | Fresh post-repair reviewer dispatched. |
| **450** | **2026-10-21T22:03:12.606Z** | **Second FAIL / missing. Reviewer confirms the other three findings fixed; default-path security retention remains absent.** |
| 462 | 2026-10-21T22:03:47.231Z | Task recorded blocked rather than complete. |
| 475 | 2026-10-21T22:04:24.721Z | Orchestrator asks for explicit authorization to correct and re-freeze the fixture, invalidating earlier acceptance evidence. |
| **521** | **2026-10-22T00:19:07.882Z** | **Operator: “I authorize the frozen-fixture correction”.** |
| 573 | 2026-10-22T00:20:13.181Z | Security fixture’s default-path boolean changed from false to true. |
| 579 | 2026-10-22T00:20:20.483Z | Concrete default-path security coverage assertion added. |
| 585-586 | 2026-10-22T00:20:28.053Z through 00:20:28.058Z | Oracle digest constant and held-back hash pin updated. |
| 607 | 2026-10-22T00:21:13.097Z | Fresh independent authorized-correction review dispatched. |
| **668** | **2026-10-22T00:26:48.291Z** | **PASS / compliant delivered. All six Task 12 criteria verified.** |
| 691 | 2026-10-22T00:27:22.489Z | Task 12 recorded complete. |
| 779 | 2026-10-22T00:33:32.415Z | Integration task recorded complete after independent passing review. |
| 824 | 2026-10-22T00:35:03.074Z | Archive blocked by missing separate operator archive ruling. No final-review failure occurred. |

**Key Takeaways**

- The second failed review was predictable from the deliberately unresolved finding.
- The operator decision, not another predicate rewrite, removed the remaining blocker.
- Historical acceptance evidence was retained and superseded, not silently overwritten.

## 4. Finding-by-finding validity against original criteria

### 4.1 Unverified evidence incorrectly selected rejection rows

**Original requirement:** The canonical admission rules require verified guards or a verified producer/schema before those facts justify rejection. Missing required verification belongs to the unproven-evidence outcome.

**Historical implementation:** Builder trace anchor 65 contains:

```python
matches = (
    f["guard_blocks"] or f["seam_violates_precondition"],
    f["producer_refuses"],
```

These earlier matches won before the later incomplete-evidence condition, even when the corresponding verification flags were false. The first reviewer independently demonstrated both errors using development records.

**Validity:** Valid against the original oracle-fidelity requirement, not a newly introduced reviewer preference. Exact textual comparison of the table constants was insufficient because execution used separate predicates.

**Repair:** Builder anchor 189 adds verification requirements to the guard, seam, and producer predicates. The later runnable regression tests explicitly distinguish verified rejection from unverified, unproven evidence.

**Subsequent status:** Resolved. The second reviewer confirmed working development-only counterexamples. This finding did not recur.

Primary review evidence:

`/config/workspace/IronClaude/.dev/worktrees/auggie-claim-gate/.dev/tasks/to-do/TASK-WF-designV2-20261020-132032/artifacts/t12-review-1.md:20-22`

Current runnable checks:

`/config/workspace/IronClaude/.dev/worktrees/auggie-claim-gate/tests/skills/test_auggie_claim_gate_oracle.py:291-302`

### 4.2 Provenance contrast tested policy documentation instead of author identity

**Original requirement:** Contrast refusal of a present valid author against refusal of a missing author with unknown identity.

Primary requirement:

`/config/workspace/IronClaude/.dev/worktrees/auggie-claim-gate/.dev/brainstorms/20261020-043737-auggieClaimGate/merged-requirements.md:610`

**Historical implementation:** Builder anchor 58 authors the provenance pair by changing `policy_verified` while retaining the known-valid-author consequence. This was a real single-field contrast, but for the wrong causal factor.

**Validity:** Valid original semantic-coverage failure. Correct family labels, cardinality, and changing exactly one field did not establish the required known-versus-unknown author contrast.

**Repair:** Builder anchors 191-196 introduce actual author input, required-author schema facts, and an author-field contrast. The negative expectation changes to producer/schema rejection. Added assertions pin the actual author values.

**Subsequent status:** Resolved. Second review confirmed known author admitted, missing author rejected, and unverified producer classified unproven.

Current semantic assertions:

`/config/workspace/IronClaude/.dev/worktrees/auggie-claim-gate/tests/skills/test_auggie_claim_gate_oracle.py:305-322`

### 4.3 Missing-abstraction case remained another import-cycle claim

**Original requirement:** Preserve both the pre-existing-cycle case and a separate missing-abstraction claim without a convention source.

Primary requirement:

`/config/workspace/IronClaude/.dev/worktrees/auggie-claim-gate/.dev/brainstorms/20261020-043737-auggieClaimGate/merged-requirements.md:607`

**Historical implementation:** Builder anchor 58 copies the positive import-cycle record, renames it as the no-convention negative, and clears convention verification. Its consequence still describes an import cycle.

**Validity:** Valid original semantic omission. The record exercised missing convention evidence, but not the separately specified missing-abstraction claim.

**Repair:** Builder anchors 206-211 distinguish cycle and missing-abstraction facts, replace the abstraction consequence, and add its matching positive comparison. The existing new and pre-existing cycle cases remain.

**Subsequent status:** Resolved. The second reviewer explicitly found the added structural positive necessary for the required contrast, not extra scope.

Primary second-review assessment:

`/config/workspace/IronClaude/.dev/worktrees/auggie-claim-gate/.dev/tasks/to-do/TASK-WF-designV2-20261020-132032/artifacts/t12-review-2.md:30-40`

Current assertions:

`/config/workspace/IronClaude/.dev/worktrees/auggie-claim-gate/tests/skills/test_auggie_claim_gate_oracle.py:325-350`

### 4.4 Required default-path security fixture inherited a false default

**Original requirement:** Include a Critical-tier security sink on a default path.

Primary requirement:

`/config/workspace/IronClaude/.dev/worktrees/auggie-claim-gate/.dev/brainstorms/20261020-043737-auggieClaimGate/merged-requirements.md:652`

**Historical cause, directly observed:** The held-back generator at builder anchor 52 defines shared facts with `default_path=False`. Its `base-default-security` constructor overrides security category, exploitability, severity hint, and harm, but does not override default-path status. By contrast, the neighboring default-path null-dereference constructor explicitly supplies `default_path=True`.

The preserved original fixture confirms:

- Security category.
- Exploitable harm.
- Expected Critical severity.
- Correct base/security-retention labels.
- **`default_path: false`.**

Primary preserved bytes:

`/config/workspace/IronClaude/.dev/worktrees/auggie-claim-gate/.dev/tasks/to-do/TASK-WF-designV2-20261020-132032/artifacts/t12-held-back-before-authorization.json:563-628`

**Validity:** Valid against the original requirement. This was not a reviewer inventing an extra test condition after the repair.

**Why the first repair did not resolve it:** Main-session anchor 383 explicitly prohibited changing the held-back fixture, hash artifact, oracle digest constant, or frozen token file. It also prohibited adding duplicate retention to conceal the omission. The builder’s freeze log expressly retained this open finding.

**Subsequent status:** The sole retained finding in the second failed review. No changed predicate caused it; its original bytes remained unchanged.

Second-review evidence:

`/config/workspace/IronClaude/.dev/worktrees/auggie-claim-gate/.dev/tasks/to-do/TASK-WF-designV2-20261020-132032/artifacts/t12-review-2.md:20-28`

**Key Takeaways**

- All four initial findings were supported by original requirements and historical implementation.
- Three were repaired successfully.
- The recurring finding was a frozen input defect, not failed execution of those three repairs.

## 5. Why green tests did not close the findings

I independently inspected the preserved log summaries, without executing the investigated tests.

| State | Default tests | Acceptance tests | Independent review |
|---|---:|---:|---|
| Before first review | 67 passed | 78 passed | FAIL, four findings |
| After permitted repair | 74 passed | 85 passed | FAIL, one retained finding |
| After authorized fixture correction | 74 passed | 85 passed | PASS |

The mechanism is specific:

1. **Textual fidelity was not executable fidelity.** The original table constants contained verification language, while the separate executable predicates omitted verification gates.
2. **Coverage checked structure more strongly than meaning.** Family identifiers, member counts, one-field differences, and retention labels passed despite the wrong causal contrasts and missing default-path fact.
3. **Security grading could still pass.** The historical fixture already described exploitable Critical security harm. It could receive its expected disposition and severity without supplying the specifically required default-path example.

The authorized correction added an assertion requiring an actual security-category, default-path, exploitable case with supported Critical harm:

`/config/workspace/IronClaude/.dev/worktrees/auggie-claim-gate/tests/skills/test_auggie_claim_gate_oracle.py:278-283`

Thus unchanged passing test counts after correction do not imply the correction was cosmetic. An existing coverage test acquired a previously missing semantic assertion.

**Key Takeaways**

- Passing tests were genuine but incomplete evidence.
- The reviewers found compliance defects outside what those assertions established.
- The correction strengthened the test’s meaning without increasing the number of collected tests.

## 6. Freeze conflict and authorized resolution

**There was no inherent contradiction in the original feature requirement. A valid default-path security fixture could have been authored before freezing.**

The conflict arose after the deficient record had been frozen and acceptance had run. Under the first repair’s explicit boundaries, the builder could neither correct that frozen record nor substitute duplicate coverage. That made the specific remaining repair unavailable without a new operator decision.

This does **not** prove every conceivable implementation was mathematically impossible. It establishes that the permitted repair deliberately excluded the action required for the chosen fixture correction.

After authorization:

- The original fixture and hash were preserved.
- Earlier acceptance results were explicitly superseded.
- Exactly one fixture field changed: `/8/facts/default_path`, false to true.
- The hash pin and oracle constant changed.
- A concrete semantic coverage assertion was added.
- A fresh independent review passed.

My independent byte comparison verified that replacing only that boolean produces the entire current held-back file exactly. No expected disposition, severity, or other fixture fact changed.

**Historical limit:** The authorized reviewer lacked a separately preserved full pre-authorization oracle snapshot. The observed edit trace supports the limited oracle changes, but should not be described as an independent historical full-file byte comparison. The passing review expressly recorded that distinction.

**Key Takeaways**

- Freeze preservation explains the repeated failure.
- Authorization enabled a bounded input correction, not outcome-driven predicate tuning.
- Corrected held-back evidence must remain labeled re-frozen, not untouched.

## 7. Subsequent outcome and excluded events

The independent authorized-correction review passed at main-session anchor 668. Integration then passed with 255 scoped default tests and 85 acceptance tests.

The archive gate subsequently refused to proceed because the accepted Task 11 residuals lacked the separate operator archive ruling required by that gate. Main-session anchor 824 explicitly states no final review or archive move occurred. This is an authorization/state blocker, not another Task 12 QA failure.

The two earlier local oracle test failures are also separate:

- Initial table extraction omitted the first admission row.
- A subsequent mutation test changed a disposition to its existing value and therefore did not raise.

**Key Takeaways**

- They occurred during initial builder development before the first independent review. Counting them as failed independent QA rounds would mix test-debugging attempts with review outcomes.

## Gaps and Questions

- No live-model effectiveness claim is established. The oracle and deterministic tests do not prove a model follows the protocol.
- No independent pre-authorization full-oracle byte comparison was available to the historical authorized reviewer.
- Task 11’s preceding failed rounds belong to earlier execution history. This session’s carryover descriptions are not independent observations of those events.
- The worktree is excluded from the available graph index. Direct files and historical tool payloads supplied the evidence instead.
- No unresolved question prevents classifying the repeated Task 12 failure.

## Stale Documentation Found

No stale documentation was established as the cause of this review loop. The final live fixture differs intentionally from its preserved historical version because of the explicit operator-authorized correction; that is not documentation drift.

## Summary

Task 12 failed twice because its first implementation contained four real compliance defects, and the permitted repair deliberately left one defective frozen fixture unchanged. The three permitted repairs worked, and the second reviewer confirmed them rather than replacing them with new objections. The repeated security-fixture finding originated in an inherited false default and survived because the coverage test checked labels without the required default-path property. Explicit operator authorization enabled the one-field correction, re-freeze, semantic assertion, and subsequent passing independent review.

**Recommended action:** Preserve this as a **retained frozen-input defect requiring authorization**, not a moving-target review case or repair-induced regression, at `/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/research/02-session-a9b88895.md`.

## Resume traceability supplement (2026-10-23)

**Key Takeaways**

- Original event UUIDs and complete timestamps are preserved once in `screening-handoffs-source.txt:414-431`, keyed by this report's exact original session path and physical records. The main resume parser independently rechecked records 291, 383, 450, 521 and 668 against that preserved mapping, asserting all five selected records have timestamps/UUIDs and the selected/output count matches. This adds an explicit traceability join without duplicating the case analysis or relabeling the retained fourth finding as a new regression. Original physical JSONL anchors and the preserved capture remain unchanged; formatting corrections can move this research file's lines.

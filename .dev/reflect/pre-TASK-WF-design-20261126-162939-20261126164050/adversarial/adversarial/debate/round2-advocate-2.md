# Round 2 — Advocate 2 (Variant 2, QA)

## Responses to criticisms

- Concede V2's contradictory FR-109 coverage claim, missed C-004/C-009/C-010, and overclaimed T-14/AC-13 coverage. Its 67-entry table is not the requested 29-id audit. Layout transparency does not establish completeness. Normalize conflicting grade/label pairs and withdraw “Regression” for merely planned omissions.
- Concede the cap's “no implementation instruction” claim: Task 29 incorporates FR-064. C-022 likewise merits at most a Note for explicit field assertions, not Blocking; schemas already have design instructions.
- Reject calling test-first a preference: DESIGN:458 explicitly requires ordering. C-020 remains Blocking because the missing requirement changes execution order. For C-021, concede behavioral simulation is unnecessary: static assertions can satisfy the design, but the required authority assertion remains absent.
- Against advocate 1's Medium C-012: T-04/T-21/T-16 explicitly require executor observations, not just helper outputs. Missing refused records, crash-after-resolution evidence and no-flag call accounting omit required testing in substance: Blocking.
- Against its Medium C-013: timeouts do not implement stopping on credential prompts. NFR-014 names that required behavior independently; restoring it is Blocking.
- Against its C-018 defense: “five” is inside an acceptance check. Testing all seven is not established by that text. Correcting this relied-on count is Blocking under the supplied rule.
- C-008: parity tests are real, but neither Task 38 nor another quoted instruction forbids earlier copies. Constraint 24 supplies that obligation. “Unavoidable halt” and “either way breaches text” remain unsupported.

## Updated view of the other variants

V1's concessions strengthen its coverage reading; V3's concrete evidence wins C-002/C-003 over my earlier tie. V3 remains strongest on parser and transient-test defects, but V1's endorsement does not repair its plugin-timing premise. V1's new grading still understates named testing and behavior obligations.

## New evidence

REQ:679's T-16 requires existing implement tests to pass **unchanged**, whereas `tests/skills/test_task_workspace_lifecycle.py:682-688` fixes the transient vocabulary at four reasons. Task 31 necessarily requires updating that assertion. Repair must explicitly reconcile T-16's unchanged-test wording with T-14's required pin updates, rather than silently weaken tests. This is another source-level conflict supporting A-003.

## Revised per-point table

Four vote changes; unlisted votes remain unchanged. PLAN/DESIGN/REQ retain their supplied meanings.

| point | V1/V2/V3/TIE/NONE | right grade or resolution | one-line reason |
|---|---|---|---|
| S-001 | V2 | Note | Explicit coverage tables help, despite overclaims. |
| S-002 | V3 | Note | Authorized expansion fits; extra labels are presentation issues. |
| C-002 | V3 | Blocking | Required legacy-path exclusion absent. |
| C-003 | V3 | Blocking | Correct the repository-wide acceptance to the new-code scope. |
| C-008 | NONE | Note | Global parity already requires early copies; delay is inferred. |
| C-012 | V2 | Blocking | Required executor test outcomes absent in substance. |
| C-013 | V1 | Blocking | Credential-prompt stopping is separately required. |
| C-017 | V3 | Blocking; anchor Note | Net-growth acceptance needs a valid measure and final Task 30 recheck. |
| C-023 | V2 | Note | Retain missing assertion only, not absent implementation. |
| X-002 | V1 | Blocking | Timeout coverage does not cover prompt stopping. |
| X-003 | V3 | Blocking for both | Required exclusion and named acceptance change. |
| X-005 | NONE | Task 29 clarification + assertion | State first-40-lines behavior and assert truncation; retain FR-064. |
| X-006 | NONE | Clarify, not new behavior | Name per-task mirroring in Tasks 26–32; make Task 38 verify/refresh existing copies. |

## Final shared-assumption responses

- **A-001 REJECT:** Review Blocking is not the executor's checklist/read-back/inherited-origin halt model.
- **A-002 QUALIFY:** Named suites bind; mere file readership does not establish intermediate acceptance.
- **A-003 REJECT:** Correct source conflicts or record explicit overrides, including DD-8 and unchanged-test wording.
- **A-004 REJECT:** Baseline records do not freeze refs or tests; revalidate before execution.

No commands ran; runtime outcomes remain UNVERIFIED.

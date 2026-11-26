# Round 1 — Advocate 2

## Position summary

V2 correctly identifies a blocking regression, but its single-finding verdict is incomplete. Retain its FR-122 finding and requirement dispositions; incorporate the strongest V1/V3 discoveries, regraded by this debate's rule. P denotes the regenerated plan, D its design body, R the merged requirements. “Verified” below means verified from source, not executed.

## Steelman per opposing variant

**V1:** Its broad pass finds interactions V2 missed: test-first scheduling, validator context and unflagged skip settlement. Its source-versus-runtime distinction is honest. In particular, C-010 identifies a real conflict between two required outputs, not merely missing prose.

**V3:** Its strongest contribution is checking the plan against existing consumers. The existing command twin, config-isolating fixture, halt-line classifier and CI workflow expose risks a requirements-only audit misses. C-002 correctly follows the same-task mirror Constraint rather than assuming eventual parity suffices.

## Strengths claimed

V2 alone applies the right grade to C-001. P:326 rejects every keyless reply; D:387 and R:606 permit a qualifying reply after exactly one displayed key. P:329 and P:386 then pin the wrong behavior. Failing closed does not make changing a required outcome non-blocking. The M-10 repair therefore introduces a regression in owner resolution, even though its other repairs remain present.

V2 also distinguishes historical identifiers from active obligations: FR-037 occurs as provenance, not an active definition. Its 17 inactive, eight covered and one coverage-gap dispositions prevent invented work. Its explanation of NFR-015 correctly respects the requirement's stated deliverable: the spec documents the trust boundary.

## Weaknesses identified in the other variants

V1's “Medium because stricter” argument for C-001 contradicts the supplied grading rule. V3 marks M-10 resolved without comparing the very no-key text it cites.

V3's C-003 diagnosis needs qualification: the fixture constructs config isolation in a child-process environment; it does not export those variables into the test process. Merely preserving inherited variables is therefore not a demonstrated fix. System LFS filters are present, and test isolation needs attention, but actual future test failures remain UNVERIFIED.

C-004 is stronger than a stylistic Medium: embedding an implementation-time baseline comparison in a permanent test changes the named Task 32 gate and freezes future archive-helper work. The workflow omits an explicit checkout depth; the asserted effective depth and actual CI failure remain UNVERIFIED here.

C-005's definite conflict is Task 26's conditional permission versus P:20's Task-32-only exception. Extra classifier hits in Tasks 30/31 depend on how text is laid out; V3 must not assert they inevitably occur.

C-009 overstates absence: P:212 expressly assigns T-19 segment/eligibility cases, whose definition includes FR-109; other cases also appear in Tasks 9–16 and 34. A shorter acceptance bullet is not proof required tests are absent in substance.

## Concessions

V2 missed C-002 and the named acceptance conflicts C-004–C-006 and C-010. Its “one blocker” count cannot stand. Its carried-forward NFR-013 coverage gap deserves Medium rather than a cosmetic Note. V1/V3 provide useful evidence even where their grades need correction. No commands or tests were run.

## Shared assumption responses

- **A-001: QUALIFY.** This debate's grading rule governs this review; it is not identical to the executor's halt model. The read QA rubric derives severity from B1–B4, Read-back and inherited caps, not only Constraints. A wrong required behavior can block this plan review even if an executor faithfully implementing that wrong plan would pass local QA.
- **A-002: QUALIFY.** P:38 and P:432 explicitly require existing suites; fixtures and configured CI are relevant evidence. Machine-specific configuration reveals portability risks, not an unlimited new acceptance universe. System LFS config confirms filter presence, not every asserted runtime failure or a mandate to weaken the design's conservative filter refusal.

## Per-point table

| point | superior treatment | right grade | verified or UNVERIFIED | one-line reason |
|---|---|---|---|---|
| S-001 | V2 | n/a | verified | Requirement dispositions add useful coverage accounting without duplicate findings. |
| S-002 | TIE | n/a | verified | Different labels remain understandable; semantic grading matters more. |
| C-001 | V2 | Blocking | verified | P:326 contradicts D:387/R:606 and determines Tasks 28/34 acceptance. |
| C-002 | V3 | Blocking | verified | P:25 requires same-task copying; Task 19 delays its existing twin until Task 25. |
| C-003 | V3 | Medium | verified | Real test-isolation gap; preserving inherited variables alone is insufficient. |
| C-004 | V3 | Blocking | UNVERIFIED | P:366 embeds a temporary-baseline dependency in a permanent named test; CI execution unproved. |
| C-005 | V3 | Blocking | verified | P:306 permits classifier edits beyond P:20's recorded exception. |
| C-006 | V3 | Blocking | verified | Literal P:359 grep can reject the legitimate preflight reason; its acceptance scope must change. |
| C-007 | V1 | Medium | verified | Late static pins obscure test-first scheduling; impossibility is overstated. |
| C-008 | V1 | Medium | verified | P:62/65 require context-dependent validation without specifying its context source. |
| C-009 | NONE | NOT-A-DEFECT | verified | P:212 already assigns T-19 cases; no demonstrated substantive omission. |
| C-010 | V1 | Blocking | verified | P:216's unqualified skip action conflicts with unflagged STOP and R:739's allowed appends. |
| C-011 | NONE | NOT-A-DEFECT | verified | P:62 explicitly requests the version option form; runtime behavior is not disproved. |
| C-012 | V1 | Medium | verified | Claimed design-defined skip token is absent; no named exact-token check depends on it. |
| C-013 | TIE | Note | verified | Local comparison wording is weaker, but P:434 retains the authoritative base check. |
| C-014 | NONE | NOT-A-DEFECT | UNVERIFIED | A tight required budget without fallback is not demonstrated infeasibility. |
| C-015 | V3 | Note | verified | Eleven compiled patterns occupy the range; nine explicitly named ledger patterns are correct. |
| C-016 | V3 | Medium | verified | Tracked-only blind spot is real; index staging, not commitment, controls visibility. |
| C-017 | V3 | NOT-A-DEFECT | verified | Useful advisory limitation, but conservative filter refusal follows D:374. |
| C-018 | V2 | Medium | verified | No universal refusal-integrity assertion; reporting behavior is otherwise assigned. |
| C-019 | V2 | n/a | verified | Historical-ID accounting avoids treating provenance as an active requirement. |
| X-001 | V2 | n/a | verified | M-10's no-key repair regresses FR-122; other repaired portions still stand. |
| X-002 | V2 | n/a | verified | Required behavior and named acceptance checks change, so Blocking. |
| X-003 | V1 | n/a | verified | Missing validator context is substantive ambiguity, not cosmetic form. |

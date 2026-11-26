# Round 1 — Advocate 2 (QA)

## Position summary

V2's strength is separating written behavior from evidence that it is tested. Retain its authorization, resolution-crash, hook-refusal and no-flag checks, supplemented by V1's settlement findings and V3's parser/test-pin discoveries.

PLAN, DESIGN and REQ are the files identified in diff-analysis.md. “verified” means source-read verification, not an observed test result. No commands ran.

## Steelman

**V1.** Its strongest argument is that nominal coverage can lack an executable transition. DESIGN:290-291 requires empty and mixed-authorization settlements, but PLAN:156 closes the action vocabulary without skip recording. It correctly separates credential-prompt stopping from timeouts. These beat V2's coverage claims. Its weakness is undergrading consequential behavior and acceptance changes.

**V3.** Its strongest argument is that existing tests matter. `tests/skills/test_task_workspace_lifecycle.py:682-688` restricts transient reasons that PLAN:354 expands. Its ledger finding exposes incomplete grammar reuse. However, its early-plugin-copy prohibition overlooks PLAN:24's global parity instruction.

## Strengths claimed

1. **C-002/C-003 grades.** REQ:475 requires legacy-run exclusion; PLAN:168/171 omits it. Restoring required staging behavior is Blocking. Narrowing PLAN:286's repository-wide deletion assertion changes an acceptance check: also Blocking, despite V2's inconsistent MEDIUM label.
2. **Resolution evidence.** REQ:610 requires crash-after-append, two resumes and surviving outside-change pins. PLAN:223/327-328 lacks those observations. This is missing required testing, not speculative hardening.
3. **Authority checks.** PLAN:242 requires person-only, one-operation authority and no command lines on refusal, but PLAN:245-246/282 tests structure instead. V2 identifies an untested safety invariant, not absent authorization prose.
4. **Executor versus helper.** PLAN:384's read-only reconcile test cannot demonstrate zero extra executor calls or a single `off` append (REQ:679/739). PLAN:193 likewise omits T-04's refused-line and no-same-run-retry observations (REQ:667).
5. **Process/schema.** DESIGN:458 requires test-first ordering, unlike PLAN:27's shipping tests alongside changes. Envelope checks also do not establish field-level coverage, although design references already carry implementation obligations.

## Weaknesses identified in the other variants

1. **V1 undergrades C-002/C-003.** Required behavior and a literal acceptance check change. Both meet this debate's Blocking rule. C-018 also changes the quoted count an acceptance check rests on, despite V1's Medium grade.
2. **V3 overstates C-008.** Parity tests genuinely require synchronized copies, but PLAN:24 already requires them. PLAN:426 provides final synchronization, not an explicit earlier-copy prohibition. Clarification is useful; an unavoidable halt is unsupported.
3. **V3 shares V2's NFR-014 mistake.** REQ:735 says stop rather than wait for credentials. PLAN:70/252/334 supplies timeouts, not that rule. V1 wins; missing required behavior warrants Blocking rather than its Medium.

## Concessions

V2 misses skip settlement, routing order and the transient pin. Parsing `skipped` (PLAN:136) does not produce it; FR-109 is partly covered (REQ:580). V3's `_HEADER`/`_ARCH` discovery beats both others: existing grammar accepts them, while PLAN:126 lists neither. This is a specification gap, not an observed failure.

Withdraw V2's “no implementation instruction” for the 40-line cap: PLAN:19 incorporates exact wording, PLAN:252/334 cites FR-064, and REQ:501 supplies it. Only the missing explicit assertion remains defensible. Normalize V2's conflicting severity labels; its FAIL is not a test result.

## Shared assumption responses

- **A-001: REJECT.** Debate grading is not executor halting. `src/superclaude/skills/sc-implement-protocol/refs/qa.md:41-43/56-61` additionally requires checklist derivation, read-back and inherited-origin handling.
- **A-002: QUALIFY.** REQ:711 and PLAN:430 make existing suites final obligations. Reading an edited file alone does not make every test an intermediate task's acceptance check.
- **A-003: REJECT.** Faithfulness does not establish design correctness. DD-8 omits valid grammar; DESIGN:333 requests owner confirmation. Such conflicts need aligned specification correction, not silent plan-only divergence.
- **A-004: REJECT.** PLAN:36 records a baseline, but PLAN:432 uses a movable integration ref. Neither tests nor base state are frozen; later state needs revalidation.

## Per-point table

| point | superior treatment | verified or UNVERIFIED | one-line reason |
|---|---|---|---|
| S-001 | V2 | verified | Explicit tables expose coverage scope. |
| S-002 | V3 | verified | Separates authorized expansion. |
| S-003 | V1 | verified | Most consistent grade/label presentation. |
| C-001 | TIE | verified | All identify literal-token contradiction. |
| C-002 | TIE | verified | V2/V3 correctly grade exclusion Blocking. |
| C-003 | TIE | verified | V2/V3 correctly require acceptance correction. |
| C-004 | TIE | verified | V1/V3 identify skill-existence dependency. |
| C-005 | TIE | UNVERIFIED | Index/filesystem mismatch; tracked count unproved. |
| C-006 | TIE | UNVERIFIED | Owner confirmation unobserved. |
| C-007 | TIE | verified | Source-order execution avoids dependency blocking. |
| C-008 | NONE | verified | Global parity defeats mandatory-delay premise. |
| C-009 | V3 | verified | Existing transient assertion contradicts additions. |
| C-010 | V3 | verified | Seven patterns omit header/archive forms. |
| C-011 | V1 | verified | Parsing skips is not recording settlement. |
| C-012 | V2 | verified | Separates executor observations from helper outputs. |
| C-013 | V1 | verified | Prompt stopping differs from timeout. |
| C-014 | V3 | verified | Archive needs explicit sidecar guard. |
| C-015 | V1 | verified | Identifies private-index allow-list collision. |
| C-016 | V3 | verified | Useful clarification; FR-052 already scopes primitives. |
| C-017 | V3 | verified | Separates stale anchor from growth speculation. |
| C-018 | V1 | verified | Seven refusals contradict acceptance's five. |
| C-019 | V1 | verified | Moving-reference proof is fragile; runtime unproved. |
| C-020 | V2 | verified | Shipping tests does not impose test-first. |
| C-021 | V2 | verified | Authority lacks matching invariant assertion. |
| C-022 | V2 | verified | Envelope tests do not check schemas. |
| C-023 | NONE | verified | Incorporated FR-064 defeats instruction-absence claim. |
| C-024 | V1 | verified | More cautious coverage/gap dispositions. |
| X-001 | V1 | verified | Closed actions lack skip recording. |
| X-002 | V1 | verified | Credential-prompt stop remains absent. |
| X-003 | TIE | verified | V2/V3 grades reflect consequential changes. |
| X-004 | V3 | verified | Header/archive tails need acceptance. |
| X-005 | NONE | verified | V2 overlooks incorporated FR-064 wording. |
| X-006 | NONE | verified | PLAN:24 already requires early parity. |

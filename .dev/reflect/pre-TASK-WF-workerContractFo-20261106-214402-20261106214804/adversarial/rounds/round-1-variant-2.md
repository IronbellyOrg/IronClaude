# Round 1: Variant 2 advocate (haiku, qa)

Persisted by the orchestrator on receipt, 2026-11-06T21:59:20Z. Citation keys: P = the plan, S = source.md, T = tests/skills/test_worker_contract.py.

## Position summary

Variant 2's strongest contribution is QA-1: Task 4's proposed test can pass while the command text omits the required ignored-output exclusion. P1 retained under this debate's definition; concedes Variant 1 found an equally important status-test gap (R1-1) and that QA-2 should drop to P3.

## Steelman

### Variant 1
R1-1 distinguishes finding a phrase from verifying the status rule: Task 5 asks only that both files contain "exited 0" (P:76-80), which does not reject the old "when the audit finished" rule; existing checks protect scaffold reporting, not status (T:783-797). P1 under the debate definition. R1-6 correctly identifies the extraction boundary (T:769-774); P3 is right.

### Variant 3
R3-1 has the strongest scope evidence: the brief mentions spec copies (S:14); Task 1 searches only tests and plugins (P:30); `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md:72` holds the full field definition. R3-4 respects the consolidation goal (S:13).

## Strengths claimed

1. QA-1 tests the required behavior: Task 4 requires exclusion but its assertion checks only WC-4, `[]` and no write verbs (P:66-70). P1 by definition.
2. QA-1 proposes a meaningful negative; build and workflow already require "left out" (T:798-808).
3. QA-2: scan roots are skills, commands, agents, not core (T:1054-1058, 1095-1107; P:35).

## Weaknesses identified in other variants

1. R1-6's placement advice does not address QA-1's false pass.
2. V3's "left out per WC-4" formulation needs a test condition requiring the exclusion relationship, not just WC-4 (P:66).
3. R1-2 is a documented gap, not proven impossibility: workflow.md:72 sets `report_path`, which does not prove that file cannot mention the ignored locations. The strongest form: Task 2 does not explicitly arrange compliance.
4. R1-4 and R3-3: a whole-file assertion accepting a misplaced sentence is P1 under the definition; the plan's "WC-4 text" is ambiguous, not necessarily faulty (T:383-394; P:30-33).

## Concessions

- QA-1 overstates the need for duplicated reporting wording; the shared rule carries it by reference; the essential improvement is testing that the local clause excludes ignored output (S:13, 19).
- QA-2 should be P3.
- Missed R1-1 and R3-1.
- report_path and other-project ignore cases stay advisory (WORKER-CONTRACT.md:40-42; S:29-32).

## Per-point positions

| Point | Superior variant | Reason |
|---|---|---|
| S-001 | Tie | Shape does not establish correctness |
| C-001 | V1/V3 | P3 and bounded correction (P:35; T:1054-1058) |
| C-002 | V1/V3 | Whole-file vs WC-4 span; priority depends on implementation (P:30; T:383-394) |
| C-003 | V1 | Narrowed to missing explicit compliance (P:30, 43) |
| C-004 | V2 | Planned test accepts a clause without the exclusion (P:66-69) |
| C-005 | V1 | Additive phrase check need not remove contradictory text (P:76-80) |
| C-006 | V3 | Brief's spec-copy requirement (S:14; P:30) |
| C-007 | V3 | Flags repetition, correctly P3 (S:13; P:54, 66) |
| C-008 | V3 | Pointer context helps; src-path leak hypothetical (return-contract.md:43-54) |
| C-009 | V1 | Connects status wording to real failure evidence (tests/cli/test_init_lite.py:238-261) |
| C-010 | V3 | Separate report_path boundary, advisory |
| X-001 | V2, qualified | Require the exclusion relationship; WC-4 pointer carries reporting details (S:13, 19; P:66) |
| X-002 | V1/V3 | P3 (P:35; T:1054-1058) |
| X-003 | V3 | Spec row outside the plan's two search roots (S:14; P:30) |
| A-001 | Tie | All omit the delivery boundary |
| A-002 | Tie | Per-task review does not eliminate a planned-test false pass |

## Shared assumptions

- A-001: QUALIFY. `src/superclaude/skills/sc-workflow-protocol/SKILL.md:60-62` forbids editing, deleting or regenerating the plan from reflect findings; that does not give an executor automatic permission to rewrite the plan either. Treat exact_change as proposed corrections needing an authorized route.
- A-002: QUALIFY. Per-task review is a real second guard (`src/superclaude/skills/sc-implement-protocol/refs/qa.md:7-17, 27-31` checks the diff against AC, not passing tests). It lowers the chance of shipping wrong text, but the debate defines a planned test accepting wrong text as P1, so QA-1 and R1-1 keep P1 for test inadequacy.

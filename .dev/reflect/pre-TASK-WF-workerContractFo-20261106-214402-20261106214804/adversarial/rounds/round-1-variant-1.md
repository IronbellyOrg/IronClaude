# Round 1: Variant 1 advocate (sonnet, analyzer)

Persisted by the orchestrator on receipt, 2026-11-06T21:58:40Z.

## Position summary

Variant 1 is the most complete and best-evidenced card. It is the only one that found the Task 5 test passing on the old contradicting sentence (R1-1), and the only one to check the `init_lite.py` exit paths behind the plan's "exited 0" premise (R1-5). It also graded the workflow `report_path` mismatch correctly as P2 (R1-2). Variant 2's QA-1 is a real gap that Variant 1 missed. Variant 3's R3-1 is a real scope gap that Variant 1's "clean" claim missed.

## Steelman

### Variant 2 (qa, haiku)
- Strongest version: Task 4's planned pin checks only WC-4, `[]` and "no write verb" (plan :66). Build and workflow get a "left out" pin (`tests/skills/test_worker_contract.py:799`, `:808`); the test.md pin has none. A clause "every other file written; see WC-4; `[]` when none", or one listing `htmlcov/` while naming WC-4, would pass, leaving Follow-up 2 (source.md:19-20) unprotected.
- Gets right: QA-2 (Task 1 AC3 vacuous; `AUDIT_ROOTS` at `:1054-1058` excludes `core/`); its clean list on Tasks 2, 3 and 5's final verification.
- Critique: thin (2 findings; 0.94 self vs 0.82 calibrated). Its clean line "Task 5 can change the status wording without changing the existing init-lite artifacts clauses" is wrong for `init-lite.md:92`: the status sentence follows `artifacts` on the same line, so `_artifacts_clause` (`:769-774`) includes it and editing it changes what the `:787-797` pins see.

### Variant 3 (refactorer, opus)
- Strongest version: source.md:14 says keep "a plugin or spec copy" consistent; plan :30 greps only `tests/` and `plugins/`; `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md:72` restates WC-4. R3-A1 equals R1-2.
- Gets right: honest gating vs non-gating split; R3-4 and R3-5 valid minor points; the `failed tool run` (`:792`) catch in its calibration.
- Critique: R3-A1 parked as advisory though calibrated P2; never checked Task 5 against `init_lite.py`.

## Strengths claimed

1. R1-1 is the only card to find Task 5's test passing on contradicting text: plan :76 asks only for "exited 0"; `init-lite.md:92` and `SKILL.md:61` keep the old sentence; nothing at `:787-797` rejects it. My P2 is defensible (AC :79 gives the per-task QA a hook); P1 is defensible by definition.
2. R1-2: `workflow.md:72` sets `report_path` to the plan `<id>.md`, which names neither ignored file; Task 1's unconditional sentence (source.md:13, plan :30) is false for workflow after Task 2. Fix keeps the source wording as default and routes the choice to the owner.
3. R1-5 verifies Task 5's premise against `init_lite.py` (dry-run :348-352; uncaught scaffold `FileExistsError` :221-240, :267-282; `ClickException` :247-262) and adds the SKILL.md:63 fallback gap.
4. R1-3 and R1-4 give concrete repairs (rebind AC3 to tests that read the contract, regex :430-435 and :445-461; exact WC-4 slice with a failing scratch-copy verifier).
5. The 11-item clean list is checkable.

## Weaknesses identified in other variants

1. QA-1 priority inflated and fix heavier than needed: plan AC :69 already requires the exclusion with a WC-4 reference; mirror `:799`/`:808` with a "left out" assertion instead of a synthetic negative.
2. QA-2 at P2 over-grades a vacuous AC; V1 and V3 say P3.
3. R3-A1 graded advisory, calibrated P2.
4. R3-1: the spec is an approved design record; R3 itself offers "record that it stays unchanged", so P3.
5. R3-4 and R3-5 are duplication or style, not defects.
6. V2 and V3 left Task 5 unverified against the tool.

## Concessions

- R1-6 is low value (a misplaced clause makes the pin fail, not pass wrongly).
- Missed QA-1 (exclusion pin) and R3-1 (spec copy).
- Missed the `failed tool run` pin interaction (`:792`) at `init-lite.md:92`.
- R1-1 graded P2, calibrated P1.
- `test_every_repo_setup_line_is_gated` name unverified.

## Per-point positions

| Point | Superior variant | Reason |
|---|---|---|
| S-001 | Tie | Shape does not change findings |
| C-001 | Variant 1 | Best fix, right P3 |
| C-002 | Variant 1 | Same slice as V3; P3 |
| C-003 | Variant 1 | Gating P2 with owner note |
| C-004 | Variant 2 | QA-1 finds the missing "left out" pin |
| C-005 | Variant 1 | Only R1-1 found it; V2's clean claim is wrong |
| C-006 | Variant 3 | Meets source.md:14 "spec copy" |
| C-007 | Tie | Style; source.md:13 keeps each command's list |
| C-008 | Variant 3 | Unique, valid, low value |
| C-009 | Variant 1 | R1-5 verifies the premise |
| C-010 | Tie | Out of scope |
| X-001 | Variant 2 (qualified) | Pin "left out" + WC-4; clause need not restate the rule; compatible with V3 |
| X-002 | Variant 1 (and V3) | Vacuous AC cannot let wrong text pass; P3 |
| X-003 | Variant 3 | Spec copy exists at `orca-worker-contract-spec.md:72` |

## Shared assumptions

- A-001: QUALIFY. True that no variant says how changes land and Wave 4 is advisory. A third route exists: CLAUDE.md level 3 says read the plan and check result before `/sc:implement`, so the owner or orchestrator can revise the plan between the commands.
- A-002: QUALIFY. True that no variant counts the per-task AC review. The P1 definition is test-centric, so grades stand under it, but real-world risk is lower (AC :79, :69, :33 give the reviewer a hook). Keep P1 for cases where both test and AC are silent; none cleanly meets that bar, which argues QA-1 should be no higher than R1-1.

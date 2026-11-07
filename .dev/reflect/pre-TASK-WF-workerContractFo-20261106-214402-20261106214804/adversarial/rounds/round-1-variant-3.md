# Round 1: Variant 3 advocate (opus, refactorer)

Persisted by the orchestrator on receipt, 2026-11-06T21:59:00Z.

## Position summary

Variant 3 is the only card that holds the plan to its own goal (the rule lives in one place) and the only one that checked the brief's full search scope (R3-1, design-spec copy of WC-4). It misses R1-1 and QA-1, and its Task 1 AC3 fix is weaker than R1-3. The merge should take V3's single-source findings, R1-1, QA-1 limited to the exclusion token, and R1-3, and grade all "test weaker than its acceptance criterion" findings by one rule.

## Steelman

### Variant 1
- Strongest case: best evidence base; checked `init_lite.py` exit paths (R1-5); only card to find the test passing with the old sentence (init-lite.md:92 ends "The run is succeeded when the audit finished, and failed otherwise"; plan :76 checks only "exited 0"); 11 clean checks.
- Gets right: R1-3's replacement test exists (`test_every_repo_setup_line_is_gated`, test_worker_contract.py:573); R1-2 found the workflow-report gap and routes it to the owner.
- Critique: (1) its "no other test or mirror pins" check answers a narrower question than source.md:14 ("for example a plugin or spec copy"); (2) `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md` is tracked (`git ls-files`) and :72 restates WC-4; (3) R1-6 cannot make a test pass wrongly.

### Variant 2
- Strongest case: QA-1 is the highest-value single finding; Task 4's pin checks only "WC-4", `[]` and no write verb (plan :66) while build and workflow pins require "left out" (:799, :808).
- Gets right: pairs the fix with a synthetic negative.
- Critique: (1) QA-1's report-location wording in the clause re-creates the duplication Follow-up 1 removes (source.md:13); (2) QA-2 at P2 over-grades (WORKER-CONTRACT.md:41-42 already has `git add`; core/ outside AUDIT_ROOTS :1054); (3) its Task 5 clean check is wrong: the init-lite.md:92 status sentence sits inside `_artifacts_clause` (:769-774), so the :792 "failed tool run" ban applies.

## Strengths claimed

1. R3-1: the brief names "spec copy" (source.md:14); plan :30 searches only `tests/` and `plugins/`; the tracked spec restates WC-4 at :72. Honest exit offered: record the spec as the approved design record (its header says "Planning only: nothing here is implemented").
2. R3-4: Task 3 replaces only the restated reason (plan :54); build.md:104 keeps two WC-4 parts; Task 4 adds a new restatement ("which the test report names instead", plan :66); plan goal (plan :15, "stated once in WC-4") only half met. P3.
3. R3-5: return-contract.md (installed skill ref) never mentions WORKER-CONTRACT; a bare "WC-4" cannot be followed outside a checkout (CLAUDE.md "Never Hardcode src/superclaude/ Paths").
4. R3-3: matches R1-4; `_contract()` (:383) returns the whole file; verifier uses the real `_patched_copy` (:580).
5. R3-A1 and R3-A3 kept in a non-gating block for clarity.

## Weaknesses identified in other variants

1. V1, X-003: narrower scope than source.md:14.
2. V2, X-001: report-location requirement repeats WC-4 text in the command section.
3. V2, C-005: Task 5 clean check ignores that init-lite.md:92's status sentence is inside the pinned clause (:792 bans "failed tool run"; plan :76 names only "on a failed run").
4. All cards: R1-1, QA-1 and R3-3 are the same defect class (planned assertion weaker than its AC) and got three different grades.

## Concessions

1. Missed R1-1 (Task 5 not checked).
2. Missed QA-1.
3. R1-3's AC3 replacement is better than mine.
4. R3-3 at P3 is too low on the stated rubric.
5. R3-A2 is speculative and outside the brief.

## Per-point positions

| Point | Superior variant | Reason |
|---|---|---|
| S-001 | V3 | Separate non-gating block keeps the gating list clean |
| C-001 | V1 | R1-3 names a real test (:573) that reads contract lines |
| C-002 | Tie V1/V3 | Same slice; V3 adds a failing verifier |
| C-003 | V1 | Gating, routed to owner |
| C-004 | V2 (narrowed) | Pin the exclusion token ("left out" or "git ignores"), as :799/:808; drop report-location from the pin |
| C-005 | V1 | Only V1 caught it |
| C-006 | V3 | Spec :72 restates WC-4 |
| C-007 | V3 | build.md:104 keeps two WC-4 parts |
| C-008 | V3 | Installed ref needs the `~/.claude/` path |
| C-009 | V1 | Verified exit paths |
| C-010 | V3 (advisory only) | Outside the brief |
| X-001 | V3 | Pin the exclusion; keep report-location out of per-command text |
| X-002 | V1/V3 (P3) | Vacuous AC lets nothing wrong through |
| X-003 | V3 | Tracked spec copy confirmed |

## Shared assumptions

- A-001: QUALIFY. Findings do not land as plan edits under this caller (Wave 4 is advisory). Each exact_change is a per-task instruction, so the executor can apply it in-task during `/sc:implement`; the merged output should say so (regenerate the plan, or hand P1/P2 items to `/sc:implement` as in-task notes).
- A-002: QUALIFY. The literal P1 definition is met equally by R1-1, QA-1 and R3-3/R1-4. Each task's AC already states the requirement (plan :79, :69, :33), so the per-task review is a second guard and all three are P2 under "a reviewer or test would catch it". If the test-only definition is kept, all three must be P1 together.

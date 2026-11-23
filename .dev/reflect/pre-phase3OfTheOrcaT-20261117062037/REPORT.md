```yaml
contract_version: 1.8.0
status: partial                        # convergence BLOCKED_BY_INVARIANTS (INV-008, INV-021) and 1 citation dropped by the validator
mode: pre
tier_reached: 2
confidence_calibrated: 0.30            # blind calibration of the Tier 1 card and of all three reviewer cards: 0.30 each (rubric default for an undeclared claim class; the calibrators say the findings themselves checked out, and 0.75 to 0.83 under a static-defect class)
citations_total: 111
citations_revalidated: 111
citations_dropped: 1                   # C-010 count in a NOTE; corrected in the merged card
citations_inferred: 3
citation_budget_policy: full_reread
coverage_degraded: parsed-sparse
```

# Reflect report, UC-1 pre-execution review of the phase 3 plan

- Plan: /home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/.dev/tasks/to-do/TASK-WF-phase3OfTheOrcaT-20261117-061534/TASK-WF-phase3OfTheOrcaT-20261117-061534.md (7 tasks, 5 phases)
- Request: /home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/.dev/tasks/to-do/TASK-WF-phase3OfTheOrcaT-20261117-061534/source.md
- Output folder: /home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/.dev/reflect/pre-phase3OfTheOrcaT-20261117062037/
- Merged review card (full findings, plan-text edits, provenance): /home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/.dev/reflect/pre-phase3OfTheOrcaT-20261117062037/adversarial/adversarial/merged-review-card.md
- Method: Tier 2. Three reviewers (analyzer/sonnet, qa/haiku, refactorer/opus), blind calibration of every card, adversarial merge (Round 1, Round 2, invariant probe, hybrid scoring, merge), evidence-validator over all 111 citations. Tier 1 stop was forbidden by the parse-density guard (0 labeled requirements, 13 inferred) and by S_domains 3.
- Diversity: `t2_model_class_diversity: full` (three aliases, three classes); `calibrator_diversity: degraded` (all three classes were reviewers, so the calibrator class was reused); `t2_vendor_diversity: single`; `executor_class_resolved: false`.

## Verdict

**FAIL.** The plan has 3 blocking defects and 7 medium defects that all three reviewers agreed on after two debate rounds, and the invariant probe found two further high-severity gaps that the debate never ruled on. The plan covers all 13 requirements in the request, but an executor following it literally would ship the first two blocking defects with every plan-level check green.

Advisory only: the plan package was not edited.

## Inferred requirements (Pass 2)

All 13 rows validated (verbatim quotes found in source.md:1). No rows dropped.

| INF id | Verbatim quote (short) | Citation | Match result |
|---|---|---|---|
| INF-001 | "parse each coordinator question message's payload ... show payload.question (sanitized, never raw) instead of the generic subject 'Question'" | source.md:1 | Tasks 2, 4, 5; `--once` path missed (C-001) |
| INF-002 | "a payload that is not valid JSON or has no dispatchId reads as unlinked, never an error" | source.md:1 | Task 2 |
| INF-003 | "show the one linked session, found by joining payload.dispatchId to the worker-list row" | source.md:1 | Tasks 4, 5; join key (C-006, INV-015) |
| INF-004 | "that row's resource.worktreeId shown as evidence only, never as an inferred set of affected sessions" | source.md:1 | Tasks 4, 5 |
| INF-005 | "a message with no dispatchId reads 'affected scope unknown'" | source.md:1 | Tasks 4, 5 |
| INF-006 | "no one-to-one session and worktree assumption (AC-7)" | source.md:1 | Task 4 |
| INF-007 | "the Decision Desk composition from rendering-rules.md (C) behind the gate" | source.md:1 | Necessary narrowing to one stacked block (X-004); stale spec clause (C-013) |
| INF-008 | "Gate status: QUESTION-LINK passed 2026-11-17 at dispatch level ..." | source.md:1 | Tasks 3, 7 |
| INF-009 | "Read-only: no write path into Orca; keep the forbidden verb set" | source.md:1 | pinned by test_commands.py:652-668 (NOTE C-015) |
| INF-010 | "the snapshot and export carry no message bodies ... keep it out of the snapshot unless the owner says otherwise" | source.md:1 | Task 6; check cannot pass as written (C-003) |
| INF-011 | "Contract: ... SPEC.md (CAP-12), rendering-rules.md, adapter-contract.md, acceptance-tests.md, unverified-register.md" | source.md:1 | Tasks 1, 7 |
| INF-012 | "Code: src/superclaude/cli/observe/ (...) and tests/observe/" | source.md:1 | Tasks 2 to 6 |
| INF-013 | "Rebase on origin/master before pushing." | source.md:1 | Constraint only (delivery action) |

`coverage_pct` (parsed-only): null. `coverage_pct_union`: 13 of 13 requirements mapped to a task; 3 of them have a defect in how the plan proves them (INF-001, INF-007, INF-010).

## Blocking findings (all three cards agree after Round 2)

### C-001: the `--once` path never gets the link switch (Task 3) | BLOCKING | Gap
- **Where:** src/superclaude/cli/observe/commands.py:218-220 (`run_once`) and :350-356 (interactive); the plan names only the second.
- **Evidence:** `Collector(` appears at exactly those two sites (Grep). The plan's own constraint says the `--once` record carries the link state.
- **Outcome:** `observe --once --questions --run X` keeps the subject "Question", no `dispatchId=`, no `link=`; the planned collector test passes `link=True` itself, so nothing fails.

### C-002: the new help line changes the link-off screen (Task 4) | BLOCKING | Regression
- **Where:** src/superclaude/cli/observe/view.py:78-81 and :914; render.py:362-367 and :382-384.
- **Evidence:** the keys line is chosen whenever a question panel exists, with no link input; it grows from 107 to 121 characters, so at widths 116 and 120 the footer wraps and the question panel loses a line. No questions-on screen golden exists (test_render.py:753 compares to the imported constant).
- **Outcome:** link off no longer behaves "exactly as today" (plan Constraints line 24) and no check notices.

### C-003: the Task 6 snapshot check cannot pass with the linked worker present (Task 6) | BLOCKING | Gap
- **Where:** src/superclaude/cli/observe/export.py:131-145 and :195.
- **Evidence:** the snapshot exports `dispatchId` for every worker row; the plan forbids changing `snapshot_dict` and also requires a linked question whose worker is among the rows.
- **Outcome:** the executor either strips worker ids from the snapshot or leaves the worker out of the fixture, so the linked case is never tested.

## Medium findings (agreed)

C-004 (link-on source undefined, first `n` cannot select; per-focus key table), C-005 (desk height can collapse the question list; no selected flag), C-006 (join on typed `raw.dispatch_id`, skip UNKNOWN), C-009 (no desk missing-value or stale assertions), C-011 (AD-18 and the CAP-12 row say `links.py` and a field group), C-012 (extend `make_question_rows`; the planned builder drops `body` and `to_handle`), C-013 (rendering-rules.md lines 21, 24 and 43 go stale). Exact wording and citations: merged card.

## Invariant probe: not converged

The probe tested the plan as it would read after the 10 agreed edits. Of 34 findings, 21 are open: 2 HIGH, 11 MEDIUM, 8 LOW.

- **INV-008 (HIGH):** `_panel_lines` clips only the end of each question line (render.py:317), and the plan swaps the subject for a full sentence of question text, so ` reason unknown` is cut off at 80 and 116 columns on almost every linked line. rendering-rules.md:50 says only the subject is clipped. No acceptance check reaches it.
- **INV-021 (HIGH, sufficiency):** applying the 10 edits alone does not make the plan correct. The same plan would still ship INV-008, the dropped "in `all_rows`" words (INV-015), a test builder whose default sender skips the sender check (INV-016), record checks that pass without the new suffix (INV-017) and a byte-for-byte reference that can be captured from the new code (INV-018).
- MEDIUM: INV-001, INV-004, INV-009, INV-010, INV-011, INV-012, INV-013, INV-015, INV-016, INV-017, INV-018. Fixes: merged card, section "Invariant probe additions".

## Per-point outcome

NOTE level, no plan change required: C-007 (HELP constant wording), C-008 (invalid `dispatchId` reason), C-010 (split Task 4), C-014 (record that B stays the default), C-015 (INF-009 already pinned). Necessary deviation: the stacked block instead of the two-column layout (rendering-rules.md:8 leaves C undefined).

## Recommendations

### Recommendation R-001: wire the link switch at both Collector calls
- **File:** the plan, Task 3 (and tests/observe/test_commands.py)
- **Change:** replace "pass it as a new keyword `link=` to `Collector` at the call at line 355" with "pass it ... to both `Collector(...)` calls: `run_once` (line 218) and the interactive loop (line 350)"; add a `--once` test whose record has `dispatchId=` and `link=linked` on the question line and not the question text, and whose `--width 116` screen shows the question text.
- **Verifier:** the new test in `uv run pytest tests/observe/test_commands.py -q`; argv log unchanged.
- **Linked deviation(s):** C-001, INV-016, INV-017
- **Priority:** P0

### Recommendation R-002: keep the link-off keys line byte-for-byte
- **File:** the plan, Task 4 and Task 5 acceptance criteria
- **Change:** leave `QUESTIONS_KEYS_LINE` unchanged; add `QUESTIONS_LINK_KEYS_LINE` and select it in `build_view` only when link is on; capture the link-off questions-on `screen_lines` at 160, 116 and 80 (named height, fake clock) to a named file before Task 4 edits view.py, and compare after.
- **Verifier:** the comparison test passes; `git diff` shows the reference file added before the view.py change.
- **Linked deviation(s):** C-002, INV-018
- **Priority:** P0

### Recommendation R-003: narrow the snapshot check to the questions group
- **File:** the plan, Task 6 acceptance criteria
- **Change:** replace "contains neither the `ask` string nor any dispatch id of a question" with "does not contain the `ask` string anywhere, has no dispatch id in its `questions` group, and keeps `rows[].dispatchId` of the linked worker, which the fixture includes"; keep schema validation and byte-identity with the link-off snapshot.
- **Verifier:** `uv run pytest tests/observe/test_snapshot_schema.py -q` with a fixture that includes the matching worker.
- **Linked deviation(s):** C-003
- **Priority:** P0

### Recommendation R-004: clip only the question text, never the honesty labels
- **File:** the plan, Task 5 (and tests/observe/test_render.py)
- **Change:** build each question line from its parts and clip only the question text to the width left after the age, bracketed state and ` reason unknown`; add a criterion that at 80 and 116 columns every linked question line ends with `reason unknown`; show a mark when the 400-character cap cut the text (INV-009).
- **Verifier:** the new width tests in `uv run pytest tests/observe/test_render.py -q`.
- **Linked deviation(s):** INV-008, INV-009
- **Priority:** P0

### Recommendation R-005: close the sufficiency gaps the debate did not rule on
- **File:** the plan, Tasks 2, 3, 4, 5, 6
- **Change:** restore "in `all_rows`" in the join text (INV-015); make `dispatch:<dispatchId>` the default sender for linked test rows (INV-016); assert the suffix on the question line `<qid> | ... | dispatchId=<id> | link=<state>`, not "`dispatchId=` anywhere" (INV-017); decide what a non-`dispatch:` sender with a payload does (INV-004); budget the `decision desk hidden` notice line (INV-010); give the desk a distinct note when no worker read has succeeded (INV-012) and for a not-reobserved row (INV-001); blank question text keeps the subject (INV-011); name how a selection beyond the shown window is signalled (INV-013).
- **Verifier:** each added criterion has a named test; `uv run pytest tests/observe -q` passes.
- **Linked deviation(s):** INV-021 and the INV ids listed
- **Priority:** P1

### Recommendation R-006: apply the seven agreed medium edits
- **File:** the plan, Tasks 1, 2, 4, 5, 7
- **Change:** C-004 (link-on definition and per-focus key table), C-005 (selected flag; size the desk first), C-006 (typed join), C-009 (desk missing-value and stale assertions, `_field` for the worktree), C-011 (amend AD-18 and the CAP-12 row in ARCHITECTURE-SPINE.md), C-012 (extend `make_question_rows`), C-013 (rendering-rules.md lines 21, 24, 43 and the evicted-selection note). Exact text: round-2-v3.md section 4 items 4 to 10.
- **Verifier:** re-run `/sc:reflect --mode pre` on the edited plan; the 3 blocking and 7 medium findings no longer appear.
- **Linked deviation(s):** C-004, C-005, C-006, C-009, C-011, C-012, C-013
- **Priority:** P1

### Recommendation R-007: apply the form-only notes
- **File:** the plan, Tasks 1, 3, 7
- **Change:** say "the HELP constant" not "module docstring" and append a sentence qualifying "subjects are shown"; map an invalid `dispatchId` to `payload has no dispatchId`; name a selection marker other than `>` and `*`; record that B stays the default; correct the register-line-33 note (the line exists now).
- **Verifier:** read-back of the edited plan lines.
- **Linked deviation(s):** C-007, C-008, C-014 and the notes
- **Priority:** P2

## Inferred-claim audit

- `citations_inferred: 3`
- Inferred-fraction: `3 / 111` = 0.03

Notes: calibrators scored every card 0.30 because the cards declare no claim class (rubric default); this is a limit of the rubric for plan-review cards, not a finding that the evidence failed. No test was run in this review; wrapping and height effects (C-002, C-005, INV-008 to INV-013) are read from the code.

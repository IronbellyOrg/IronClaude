# A.10 Task-File Structural Validation: Consolidated Findings (cycle 1)

Sources: `qa/qa-task-validation-b2-report.md` (VERDICT: FAIL), `qa/qa-task-validation-structure-report.md` (VERDICT: FAIL).
Task file: `TASK-RESEARCH-review-panel-unify-20261113-155942.md` (104 items).

## Items Reviewed

| Check | Source | Result | Note |
|---|---|---|---|
| B2 self-containment (104 items) | b2 report | 91 PASS / 13 FAIL | 13 fails are all B-1 |
| Frontmatter, sections, Task Log | structure report | PASS | |
| Phase 5 order (synth parallel -> adversarial -> synth-05 -> synth-06 -> gate) | structure report | PASS | |
| Item hand-off: Section 4 gaps to Section 8 plan | structure report | FAIL | S-1 |
| Gate re-run after late report change | structure report | FAIL | S-2 |
| Fix-loop halt ordering (regression -> monotonicity -> cap) | structure report | PASS | |
| Owner scope rules (no workflow, no roadmap, no c2ddeb1b4, reflect_post_mode skill) | structure report | PASS | |

## Blocking findings (fix all)

| ID | Severity | Where | Defect | Fix |
|---|---|---|---|---|
| B-1 | IMPORTANT | item 348 and the 13 lens items, lines ~354-382 | Item 348 sets a >3000-line rule that splits each Step 6.2-6.4 lens agent into two (Sections 1-5 / 6-10, outputs `-a`/`-b`), but none of the 13 lens items restates it; each hard-codes one agent and one output, so the split is lost after a session rollover. | Add to each of the 13 lens items: "If the Phase Gate Findings section records the >3000-line partition rule from item 6.x, run this lens as two instances with `Assigned sections: 1-5` and `6-10`, outputs `qa/qa-lens-<lens>-a.md` and `-b.md`; otherwise one instance as written." Also make the Step 6.5 consolidation item read the `-a`/`-b` files when present. |
| S-1 | IMPORTANT | items ~280 (synth-02) and ~302 (synth-06) | synth-02 must link each unwired capability to a Section 8 migration step that does not exist yet and has no track names; synth-06 does not read synth-02 or `gaps-and-questions.md`, so Section 8 is not forced to cover every Section 4 gap. | Give synth-02 a fixed set of migration-track labels to tag each gap with (define them in the synth-02 prompt and in the synth-06 prompt identically, e.g. M1 shared-core contract, M2 reflect onto core, M3 tasklist/spec consumers, M4 future consumers PR review and rf-qa); add `synthesis/synth-02-target-gaps.md` and `gaps-and-questions.md` to synth-06's inputs with the rule "every CRITICAL or IMPORTANT gap in Section 4 maps to at least one Section 8 step or an explicit drop with a reason". |
| S-2 | IMPORTANT | items ~440 (Step 6.8) and ~446 (Step 7.1 hash check) | A late fix routed back to Step 6.5 (missing section at 6.8, or report hash changed at 7.1) changes the report after the fidelity gate (6.7) and the anti-omission gate (6.7b) passed, and neither item re-runs them; only the 6.6 verifiers re-run. | On both paths: after the fix, re-run Step 6.6 verification, then 6.7 fidelity and 6.7b anti-omission against the new report (each within its own 2-cycle cap), then 6.8; if any cap is exhausted, HALT and escalate to the user with the open blocking findings. |
| M-5 (promoted) | IMPORTANT | gate-decision items ~396, ~416, ~436 | They name only the cycle-1 verification file names; on cycle 2 verifiers write `-cycle2` files, so a passing cycle 2 read literally can hit the cap and halt. Wrong behaviour, so graded blocking despite the reviewer's minor label. | In each decision item, read the verification files of the CURRENT cycle (`...md` for cycle 1, `...-cycle2.md` for cycle 2) and say so explicitly. |

## Minor notes (record only; not fixed in this cycle)

- M-1: eight items mention stale hand-off line numbers for D7/D11/D12 without the corrected values.
- M-2: Phase 3 fix agent told to use "the same prompt as Phase 2" but its prompt lacks the task-file path.
- M-3: conditional verifier items do not name the Execution Log line that records whether a fix ran.
- M-4: item at line ~246 says "five Step 3.2 items above"; there are four.
- M-6: items ~414 and ~434 spawn two verifiers in one item.
- M-7: fidelity prompts use a `<task dir>` placeholder.
- M-8: synth-07 prompt rule numbers skip.
- M-9: three decision items lack an "ensuring" clause.
- Structure minors: three file:line references in the Execution Context block; 7 of 12 Phase 2 items name code files without file:line or evidence-absence comment; failed adversarial debate's open question not routed to Section 9.

VERDICT (consolidated, cycle 1): FAIL — 4 blocking findings to fix.

## A.10.25 research-alignment findings (appended; source qa/qa-task-research-alignment-report.md, VERDICT: FAIL)

Orchestrator re-checked each against the repo before appending.

| ID | Severity | Defect | Evidence | Fix |
|---|---|---|---|---|
| AL-B1 | IMPORTANT | All E2 study paths omit the `20261111-a1/` folder. At 4a22d742 the study lives under `.dev/eval-workspaces/tasklist-review-panel/20261111-a1/<path>`; only `HANDOFF-review-panel-unification.md` is at the `tasklist-review-panel/` root. | `git ls-tree 4a22d742 .dev/eval-workspaces/tasklist-review-panel/` lists `20261111-a1/` and the HANDOFF file only. ~18 task lines; source `research/research-notes.md` E2 prefix. | Every E2 study path (manifest.md, PILOT-REPORT, COMBO-REPORT, combos/, tools/, analysis/, per-package dirs) becomes `git show 4a22d74213f93837d00c2c314075dd967b9a98e3:.dev/eval-workspaces/tasklist-review-panel/20261111-a1/<path>`; the HANDOFF path stays at the root. Fix the `E2:` prefix definition in research-notes.md too. |
| AL-B2 | IMPORTANT | Agent 9 uses `git show master:...`; local `master` is stale (80f361804, no `cli/review/`). | `git rev-parse master` = 80f361804; `origin/master` = d2d8a2d16. | Use `origin/master` wherever a master ref is read (all items). |
| AL-B3 | IMPORTANT | `src/superclaude/cli/pr_submit/` does not exist; the package is `src/superclaude/pr_submit/`. | `ls src/superclaude/cli/pr_submit` fails; `src/superclaude/pr_submit/` exists. Task lines ~122, 182, 200, 372, 408; research-notes.md. | Replace with `src/superclaude/pr_submit/` everywhere (task file and research-notes.md). |
| AL-B4 | IMPORTANT | Slice 04 assignment 10 (Tier 2 cost/worth H-A, O-8: default panel size vs fixing the rubric; 37/38 pre runs escalate; E2 ceiling ~2.5/14 and "sonnet alone most catches per token") has no covering item. | coverage table in the alignment report. | Add the question to the most relevant Phase-2 agent prompt (agent 11 evaluation-evidence, or agent 4 panel resolution) with slice 04 as input, and add conflict row C14 `panel-size-cost` to synth-04's conflict list; ensure synth-04 and synth-05 read `research/scope/04-this-session-artifacts.md`. |

VERDICT (A.10.25, cycle 1): FAIL — 4 blocking findings to fix (max 1 fix-verify cycle).

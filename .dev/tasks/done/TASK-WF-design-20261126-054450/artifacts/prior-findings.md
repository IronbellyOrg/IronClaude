```yaml
contract_version: 1.9.0
status: success
mode: pre
tier_reached: 2
confidence_calibrated: 0.77
citations_total: 154
citations_revalidated: 154
citations_dropped: 0
citations_inferred: 3
citation_budget_policy: full_reread
coverage_degraded: parsed-sparse
```

# Reflect report (UC-1, advisory): plan for issue 676 against its design

Plan: `.dev/tasks/to-do/TASK-WF-design-20261126-042509/TASK-WF-design-20261126-042509.md` (20 tasks). Spec: `.dev/tasks/to-do/TASK-WF-design-20261126-042509/source.md`. Run folder: `.dev/reflect/pre-TASK-WF-design-20261126-042509-20261126043230/`.

## Verdict

The plan carries the design: 61 of 67 inferred requirement rows map to a task by content (`coverage_pct_union` 0.8026), and the four lexical misses plus two real gaps are listed below. It has **2 Blocking, 8 Medium and 11 Note findings** (full text with citations: `adversarial/merged-output.md`). Do not run `/sc:implement` until the two Blocking findings are fixed: Task 19 cannot pass as written, and no task runs `make sync-dev`, so the final gates fail in this worktree. All other findings can be fixed in the same edit. Findings are advisory and do not change the workflow status.

Why Tier 2 ran: the coverage pre-filter `parsed-sparse` (67 inferred rows against 9 parsed risk ids) forbids a Tier 1 stop, rule 4 fired (3 domains: code, tests, documentation) and the calibrated Tier 1 confidence was 0.69. Three reviewers (sonnet, haiku, opus) were calibrated blind (0.77, 0.73, 0.81), merged through a standard-depth adversarial debate (convergence 0.9444; the one open point, C-009, was ruled by the orchestrator), probed by an independent fault-finder (29 rows; its one HIGH row became finding M2) and every citation was re-read by the evidence validator (0 dropped).

## Inferred requirements (Pass 2)

67 rows were kept (0 failed the verbatim-quote test; 4 more were dropped as lying inside a parsed requirement's span). The full table is in `artifacts/coverage-summary.json` (field `rows`, `source: inferred`). Unmapped by content: INF-014 (forced overwrite still counts as installed, FR-042), INF-032 (never stage `.claude/`), INF-033 (routing-guide copies identical), INF-037 (failing only the victim's backup), INF-064 (AC-4 and AC-6 greps), INF-065 (one commit per work package). Four of the six are lexical misses whose content is in the plan; INF-014 and INF-065 are real (see D-2 below and M14).

## Blocking findings

### M1 (Blocking(Decision)): Task 19's grep cannot pass with the W-3 sentence Task 17 must write

- Evidence: `P:259` "lists the six categories and carries W-3"; `P:295` allows only lines that "name skill folders, hook scripts or the marketplace catalog"; `docs/getting-started/upgrading.md:46` holds "Overwritten with no copy."; the requirements' AC-4 (`merged-requirements.md:225`) has the same gap.
- Consequence: Tasks 17 and 19 cannot both pass; the executor rewords W-3 or reports Task 19 failed.
- Fix: see R-001.

### M2 (Blocking(Missing)): no task runs `make sync-dev`; the final gates fail in this worktree

- Evidence: `make verify-sync` exits 1 here ("Drift detected", `.claude/` holds only `cache/` and `settings.json`), and `tests/cli/test_verify_sync_hooks.py:124` runs it inside the `tests/cli tests/unit` runs of Tasks 10 and 20; `P:21` "Never edit or stage a path under `.claude/`" read literally forbids the fix.
- Consequence: the final verification gate cannot pass without breaking P:21.
- Fix: see R-002.

## Medium findings (M3 to M10)

| Id | Claim | Evidence (short) |
|---|---|---|
| M3 | The `agent-memory` check (TR-011, Task 5 criterion) cannot fail | `install_templates.py:58` walks source files only; no `agent-memory` folder exists in the shipped templates |
| M4 | The "no existing test reaches the new branch" claim is false | `test_install_retired_files.py:565-569`, `631-633` and `test_update_command.py:240` run the real installers; not in the Task 1, 3, 5 commands |
| M5 | A directory at the target path has no test and its behaviour changes (copy into it, now fail) | `S:143`; `install_keep.py:49`; no row in `P:65-73` |
| M6 | The Task 2 row table has no failure-key field, but the key differs per installer | `install_core.py:79`, `install_agents.py:49`, `install_templates.py:64`; contradicts `P:78` |
| M7 | Task 20's changed-files check names no command and omits `.dev/tasks/` | `P:308`; project rule: `.dev/tasks/` is always staged |
| M8 | Tests that read the edited guide and `flags.md` are never run | `test_how_we_work_routing_table.py:333`, `test_review_prompt_overrides.py:135`, `test_merge_guard_protocol.py:770` |
| M9 | Task 14 forbids the deck footer update the deck's own rule requires | `ironclaude-onboarding.html:3-5`, `:579`; `P:229` |
| M10 | Task 14's advice drops "to a place outside `~/.claude/skills/`" | `P:224` against W-2 (`P:27`) |

## Note findings (M11 to M21)

M11 Task 1's "after the skipped and kept notes" cannot be observed under force. M12 Task 6's consumer grep needs judgement (hits unrelated code, misses `scandir`, `listdir`). M13 TR-014 should first assert the backup exists. M14 the plan does not carry the design's one-commit-per-work-package grouping (`/sc:implement` never commits, so Note). M15 the audit's coverage matrix lacks FR-002, FR-005, FR-003 rows (the plan covers them). M16 Task 16 keeps the three-kind sentence beside W-1. M17 "only skill folders and hook scripts" omits the generated marketplace catalog. M18 W-4 names two of four failure causes. M19 a wrapped line can fail Task 19's line-based grep. M20 Task 14's literal `<name>.bak.<UTC time>` check cannot match HTML-escaped markup. M21 no task depends on Task 9.

## Tier 1 finding not carried into the debate

- D-2 (Note, [INFERRED] that nothing else asserts it): requirement FR-042 (a forced overwrite still counts as installed; the `✅ Installed` list does not change) has no assertion in Task 1 or in TR-001; an implementation that dropped a backed-up file from the installed list would pass every listed check.

## Withdrawn or downgraded

Downgraded by the debate: V1-F1, V2-F1, V2-F2, V2-F3 and V3-F2 (each had been graded Blocking; no named decision, deliverable or safety boundary rests on them). Withdrawn: the docstring backtick note, the documentation half of the directory-case finding, and diff point X-001 (it quoted a sentence the saved variant-2 file does not hold: the orchestrator's saved copy of that card dropped one line of the reviewer's raw return). Full list: `adversarial/merged-output.md`, section "Withdrawn or downgraded".

## Recommendations

### Recommendation R-001: Let Task 19's grep and AC-4 allow the W-3 sentence

- **File:** `.dev/tasks/to-do/TASK-WF-design-20261126-042509/TASK-WF-design-20261126-042509.md` (Task 19, line 295) and `.dev/brainstorms/20261126-031739-installer-backups/merged-requirements.md` (AC-4, line 225)
- **Change:** add "the W-3 sentence in `docs/getting-started/upgrading.md` (row one of the Step 1 table and step 1 of 'What the upgrade does'), located by its text" to the allowed hits.
- **Verifier:** after Task 18, run the Task 19 grep; every hit is on the amended allowed list.
- **Linked deviation(s):** M1
- **Priority:** P0

### Recommendation R-002: Run `make sync-dev` before the final gates and say so next to the `.claude/` rule

- **File:** the same plan (Constraints line 21; Tasks 10 and 20)
- **Change:** reword line 21 to "Never hand-edit or stage a path under `.claude/`. Regenerate the gitignored mirrors with `make sync-dev`; its output is never staged." and add a first step "run `make sync-dev`" to Tasks 10 and 20.
- **Verifier:** `make verify-sync` exits 0 and `git diff --cached --name-only -- .claude` prints nothing.
- **Linked deviation(s):** M2
- **Priority:** P0

### Recommendation R-003: Make the Medium test and gate fixes in one plan edit

- **File:** the same plan, Tasks 1, 2, 3, 5, 7, 8, 12, 14, 20
- **Change:** M3 patch `install_templates._get_templates_source` in TR-011 to a temporary source holding `agent-memory/x.md`; M4 add `tests/cli/test_install_retired_files.py tests/cli/test_update_command.py` to the Task 1, 3, 5 commands and fix the "each runs without force" sentence; M5 add a directory-at-target row to Task 2; M6 add a `key` field to the row table; M7 name `git status --porcelain` in Task 20 and allow `.dev/`; M8 add `tests/core/test_how_we_work_routing_table.py tests/skills/test_review_prompt_overrides.py tests/pr_submit/test_merge_guard_protocol.py tests/docs` to Tasks 12 and 20; M9 and M10 let Task 14 update the footer line 579 and end the advice with "to a place outside `~/.claude/skills/`"; D-2 add to Task 1 that the `✅ Installed` list still names a backed-up file.
- **Verifier:** each task's own pytest command passes after the edit; TR-011 fails when the backup step is moved above the protected-folder skip.
- **Linked deviation(s):** M3 to M10, D-2
- **Priority:** P1

### Recommendation R-004: Apply the Note fixes if the edit is already open

- **File:** the same plan
- **Change:** M11 to M21 as written in `adversarial/merged-output.md` (for example `Depends on: Task 9, Task 10, Task 19` in Task 20; one Constraints line for commit grouping).
- **Verifier:** re-read the touched task headings.
- **Linked deviation(s):** M11 to M21
- **Priority:** P2

## Inferred-claim audit

- `citations_inferred: 3` (D-2, the `[INFERRED]` marks in M-entries carried from reviewers 1 and 2: V1-F1's "tests should stay green", V2-F1/F2's test-outcome deductions)
- Inferred-fraction: `3 / 154` = 0.02

Zero-drop note: the validator dropped nothing, which the protocol treats as suspect. Independent checks in this run support the result: the orchestrator ran `make verify-sync` itself (M2), read the code and doc anchors and the three installers before the review, confirmed `v6.1.0` as a tag, and the debate itself withdrew or downgraded 5 findings and 1 diff point before validation.

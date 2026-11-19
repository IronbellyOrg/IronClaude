persona: analyzer
model_class: sonnet

(Persisted by the orchestrator from the reviewer's returned text; the reviewer agent has no Write tool.)

## Summary
Plan v4 implements Q-1 to Q-10 and the six owner decisions. No Blocking finding. The guard line numbers (10, 70-71, 444, 652, 653, 764, 786, 790, 798), the `cycle.py` ordering (949-961, 1007-1016, 1054-1058) and the test-file line cites all match the real code. Five Medium weaknesses and two Notes remain. The most material are an undefined live-item source for Task 5, no home for Status/Pipeline in the `status` retry command, and a wrong source for the `check-config` warning.

## Q-1..Q-10 and decisions
- Q-1 FIXED. Task 13. Guard 653 holds the SUBMIT row with the three issue verbs; 790 allows `SUBMIT:FS`; the 786 class list and the 788-805 case table exist as described. The new rows have the right position and precedence over 654.
- Q-2 FIXED. Task 8. `_launch` is reached only from `_examine` at 961, and `_reclaim` never launches, so one gate covers every launch path. `launch.py` has no `GOVERNED_LEVELS_ALLOWED` today. `_PENDING` is at test line 79.
- Q-3 FIXED. Tasks 3, 4 and 5. `PROJECT_ITEMS_QUERY` reads only the Status `name` (`github.py:88-103`). The Task 4 outcome table fails closed.
- Q-4 FIXED. Tasks 5 and 7 give the same order: approval reread, value-time rule, `project_check`. This matches `cycle.py:1007-1016`.
- Q-5 FIXED, Q-6 FIXED. Task 12.
- Q-7 FIXED. Task 7 moves the seven test files. `launch_argv` does reject non-matching prompts (`launch.py:101`).
- Q-8 FIXED. Task 15.
- Q-9 FIXED, Q-10 FIXED. Constraints. The same-file orders match the `Depends on` edges.
- Decisions: ship gate FIXED (Task 8). `updatedAt` observation FIXED (Task 4). Self-approval warn-only PARTIAL (see M-3). Tamper token `*.config/superclaude*` FIXED (Task 13). All four pipelines end at In review FIXED (Task 12). Extra guard refusals FIXED (Task 13; recorded in Task 26).

## Coverage
R1..R33 each map to a task. R1, R6, R9, R10, R17, R20 and R21 go to Task 27 as a Coder handoff. R30 and R32 are carried by their named tasks. No orphan tasks. R12 is covered by Task 19.

## Findings

M-1 Medium, Tasks 5 and 7. Task 5 needs the one live Project item to read the value times. Task 7 adds the helper that returns it, and Task 5 runs first. Task 5 does not say what its predicate does with zero or several matching items. In `_examine` the items are read at `cycle.py:957`, before `project_check` at 958. Fix: have Task 5 define the helper and its zero/multiple behaviour (pass through to `project_check`). Add a test for it.

M-2 Medium, Task 7. `status_report` builds the retry command from `build_claim_prompt(n)` (`cycle.py:1313`). The `status` command reads `dispatch.json` only, with no `gh` (docstring at 1279-1281). No task adds Status or Pipeline to the store record, and Task 6 leaves "which stored field" open. A retry could print a prompt that differs from the one that launched. The acceptance wording "valid for each Status" cannot be met from stored data. Fix: either store the launched prompt or level in the pending record, or pin the retry command to the stored prompt.

M-3 Medium, Task 9. The plan cites `self.account_id` (`cycle.py:767-768`) for the `check-config` warning. That value is read at run time through `gh api user`. `check_config_command` (`cli.py:185-198`) is offline and has only `Config.owner_account_id`, which is optional (`cycle.py:104`, `:768`). Fix: compare against `config.owner_account_id`, and say what happens when it is null.

M-4 Medium, Task 8. `level_gated` is a skip, so a gated issue is re-examined every cycle. Each costs about four reads, against a 35-call cap with 3 reserved (`github.py:46-49`). Several approved issues at Full could crowd out a Pipeline None issue (`budget_exhausted`). [INFERRED] Fix: apply the gate cheaply before the extra reads, or note the limit in the design note.

M-5 Medium, Task 13. The hyphen pattern `*issue-pipeline*complete*` also matches `git add docs/designs/issue-pipeline-fu1.md && git commit -m "... complete ..."`. `*issue_pipeline/complete.py*` also refuses `git add`, `git diff`, `sed` and `ruff` on that file for a governed agent working in this repo. The plan allows "anchor on the verb word or record the over-match", but the acceptance checks do not pin which. Fix: choose the anchor (for example `issue-pipeline complete` with a word boundary) and add must-allow cases.

N-1 Note, Task 13. `tests/hooks/test_launch_level_guard.py` has `GRID_CLASSES` (775-792) and an import-time assert (843). The `ISSUE` class must be added to both, not only "the expected-result grid". Per-class call rows near line 3351 probably need an `ISSUE` entry too.

N-2 Note, Task 13. The version bump lists the guard, the mirror, `orca_worktree.py:839` and the three test pins, and these all match. Docs `SUPERVISED-ORCHESTRATION-TECHNICAL-REFERENCE.md` lines 1070 and 1443 also matched the version grep. I did not read their content. Check whether they quote "version 1".

Checked: the guard at 1-110, 140-270, 425-455 and 630-808. `cycle.py` at 36-116, 440-470, 755-780, 780-1115 and 1270-1335. `predicates.py` 105-290, `launch.py` 25-134, and `github.py` 30-110 and 750-790. `cli.py` 90-205, `WORKER-CONTRACT.md` 236-302 and `claim.md` 100-146. Test lines 79 (observations), 775-843, 2714-2770 and 2865-2890 of the guard test, plus the version pins by grep. The claim session is unbound and the Wave 8 agent is governed, so the plan's "governed" definition is correct.

Not checked: `docs` line cites (Task 2), the 45-line `--pipeline none` count, `test_security_invariants.py` 911-919 and 712-730, `record.py:545`, and `orca_worktree.py` around 986. Also not checked: whether GitHub exposes `updatedAt` on single-select values (Task 3 handles this at run time), the `pr-submit` flow under the new `ISSUE` class, and `audit.py` row counts.

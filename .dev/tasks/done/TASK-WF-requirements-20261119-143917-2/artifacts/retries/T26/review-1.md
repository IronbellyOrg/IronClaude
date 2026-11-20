3bec86c711133bc1ab9ef87baff51060baa91332
# Task 26 review 1

Earlier blocking findings: none given (first review).

## ACs
- T26.AC1 met. T26.AC1@docs/designs/issue-watcher-setup.md:710 and docs/designs/issue-watcher.md:63. `grep -c` gives at least 1 per term in both files: run-all 2/2, issue-watch.d 1/3, Coordinator 2/1, Pipeline 5/2, In review 3/2, level_gated 2/1. The four allowed Statuses (Research, Spec, Plan, Debug) appear in both files.
- T26.AC2 met. T26.AC2@tests/docs: `uv run pytest tests/docs -q` gave 11 passed.

## Claims checked against live source and found true
- Caps and constants: `LOOP_CAP_S` 270, `CHILD_TIMEOUT_S` 255 (dispatch.py:52-53).
- Rotation, wait and lock files under `<state dir>/issue-watch/` (dispatch.py:154-160, 177, 235).
- The clamped reason writes nothing (dispatch.py:441-446).
- Exit codes 0, 1, 2 and 75 (cli.py:36-40, 513-514).
- First-run steps and their order, the `first-run.txt` report and `approver_is_launch_account` (first_run.py:1-20, 190).
- Coordinator path (generate.py:252) and `GOVERNED_LEVELS_ALLOWED = False` (launch.py:48), with `level_gated` raised at cycle.py:1043.
- `complete` reason words (complete.py:75-88) and the ALLOWED_STATUSES move to In review (complete.py:54-59).
- Guard stamp 2 (launch-level-guard.sh:10), the `*.config/superclaude*` token (:777), the `item-list` and `field-list` allowances (:664), and the source/plugin mirror (identical).
- The R36 amendment file and the `t4-updatedat-observation.md` artifact exist.
- The Q-1 to Q-10 rollback lines match the remediation proposal.

## Findings
F1.1 ac=scope at=docs/designs/issue-watcher-setup.md:718 anchor=src/superclaude/cli/issue_watch/cli.py:507-509 chk=amiss:n,false:y,harm:n,constraint:n family=dryrun-lock fix=Delete "Exit 75 means another sweep is running" from the dry-run sentence, or say that only a real sweep (without --dry-run) exits 75. : The doc says `run-all --dry-run` can exit 75. In cli.py a dry run runs `run_sweep` without `loop_lock`, so it never takes the lock and never exits 75. Section 19.1 of issue-watcher.md states this correctly ("takes no lock"), so the two docs contradict each other.

F1.2 ac=scope at=docs/designs/issue-watcher-setup.md:714 anchor=src/superclaude/cli/issue_watch/dispatch.py:302 chk=amiss:n,false:y,harm:n,constraint:n family=project-check fix=Say that the configured Project must be one of the repository's Projects, and that with several Projects the defaults map must name the configured one (reasons no_project, project_mismatch, project_ambiguous). : The doc says the sweep checks "that there is exactly one Project". The code allows several Projects when `defaults.projects[repo]` equals the configured Project id (`if len(ids) > 1 and defaults.projects.get(config.repo) != config.project_id` gives `project_ambiguous`). The check also fails with `project_mismatch`.

F1.3 ac=scope at=docs/designs/issue-watcher-setup.md:710 anchor=docs/designs/issue-watcher-zero-setup-coder-handoff.md (file does not exist) chk=amiss:n,false:n,harm:n,constraint:n family=dangling-ref fix=Keep, since Task 27 creates the handoff file, or say "Task 27 hands over the line". : Advisory only. The text points to a file that is not in the tree yet; a reader following it now gets nothing. This is a forward reference to Task 27 and not a task 26 failure.

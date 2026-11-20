8e5b5c3dd919520b318131ad868bc6de23fb2409
# T24 review 1

Live source read; `uv run pytest tests/issue_watch -q` gives 3013 passed. Line numbers are live-file lines of `/home/coder/workspaces/worktrees/IronClaude/claim-handoff-planb/src/superclaude/cli/issue_watch/dispatch.py` (d) and `/home/coder/workspaces/worktrees/IronClaude/claim-handoff-planb/tests/issue_watch/test_dispatch.py` (t, lines taken from the diff in the prompt at diff-line minus 1188 plus 0 offset: the Task 24 block starts at t:446).

## Earlier blocking findings
None (first review).

## Acceptance criteria
- T24.AC1 met: T24.AC1@tests/issue_watch/test_dispatch.py (Task 24 block, `test_a_rate_limited_child_stops_later_children_until_the_stored_time`, `test_a_restart_of_the_loop_honours_the_file_until_its_time`, `test_a_rate_limit_clamped_child_does_not_write_the_file`, `test_an_expired_wait_file_is_ignored`, and the parametrized `test_each_failed_pre_child_check_gives_its_own_skip_reason_and_creates_nothing` covering worktree_invalid, worktree_not_git, origin_mismatch, label_missing, approved_field_missing, and the three Project reasons, each asserting no `gh label create` and no `gh project` call); code at d:371-387 (precheck and rate wait), d:225-260 (`_precheck`), d:190-222 (wait file).
- T24.AC2 met for every reason Task 24 adds: T24.AC2@d:60-83 (`SKIP_REASONS`, with reasons that exist in `audit.py:26` `REASON_TABLE` such as config_invalid, worktree_invalid, origin_mismatch, not_enabled). Not fully met for the whole sweep, see F1.1.

## Checks of the requirement text
- R5: the wait is read before the Orca list (d:~311), written only for plain `rate_limited` (d:382-386), `rate_limit_clamped` writes nothing; `cycle.py:787-792` confirms the child sets `next_permitted_at` in its own store and the loop only reads it (d:`_child_next_permitted`). Children never write each other's stores.
- R14: label read through `repo_init.trigger_label_state` (`repo_init.py:93`, read only), field through `check_approved_field` (`repo_init.py:128`, read only); no create call exists in dispatch.py. Project rule matches `generate.py:220-226` (none, several without a map entry).
- No write to GitHub or to another store was found.

## Findings
F1.1 ac=T24.AC2 at=src/superclaude/cli/issue_watch/dispatch.py:60 anchor="All reasons used are written in the audit reason vocabulary" chk=y,n,n,n family=reason-vocab fix=add the `ensure_config` skip reasons the sweep passes through (`bad_name`, `bad_repo`, `approvers_file_exists`, `account_read_failed`, `approver_read_failed`, `maintainers_read_failed`, `no_approvers`, `generated_invalid`, plus `project_read_failed` is already in audit) to `SKIP_REASONS`, and extend the table test to cover them (`generate.py:199-276` produce them; neither `audit.py` `REASON_TABLE` nor `SKIP_REASONS` lists them) covers="All reasons used are written in the audit reason vocabulary ... or a new documented table in `dispatch.py`": a repo whose config generation is skipped is recorded at d:357 with a reason that is in neither table. Low impact; these reasons predate Task 24 (Task 23 path) but AC2 says "all reasons used".

F1.2 ac=scope at=src/superclaude/cli/issue_watch/dispatch.py:376 anchor="" chk=n,n,n,n family=cap fix=none required covers=: observation only, not blocking. The pre-child gh reads (up to 5 per repo, 15 s each via `GIT_TIMEOUT_S` and the repo_init timeouts) run before the loop cap is re-checked at d:347, so a slow GitHub can overrun the 270 s cap by one repo's checks. The 255 s child kill still bounds each child.

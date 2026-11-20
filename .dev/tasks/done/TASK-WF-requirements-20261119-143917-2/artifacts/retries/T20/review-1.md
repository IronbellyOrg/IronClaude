8b3599fca68bf0a3c6393f3dc8e6e5ee89857321
# T20 review 1

Earlier blocking findings: none (first review).

## AC marks

- T20.AC1 met. T20.AC1@/home/coder/workspaces/worktrees/IronClaude/claim-handoff-planb/tests/issue_watch/test_repo_init.py:41 (label missing, one create call), :52 (present, no create), :75 (failed create), :99 (failed/unreadable/full list never creates), :164 (Approved present), :171 (field missing), :176 (present without option Yes), :194 (failed organization read). Extra: :58 idempotence, :181 non-single-select.
- T20.AC2 met. T20.AC2@/home/coder/workspaces/worktrees/IronClaude/claim-handoff-planb/tests/issue_watch/test_security_invariants.py:1062 (`_WRITER_MODULES` names `repo_init.py`), :1064 (write sign now includes `"label", "create"`), :1074-1075 (writers subset check). I ran `uv run pytest tests/issue_watch -q`: 2943 passed. Boundary rule at /home/coder/workspaces/worktrees/IronClaude/claim-handoff-planb/tests/issue_watch/test_module_boundaries.py:77.
- T20.AC3 met. T20.AC3@/home/coder/workspaces/worktrees/IronClaude/claim-handoff-planb/src/superclaude/cli/issue_watch/repo_init.py:105 (`defaults.trigger_label`), :138 (`defaults.approval_field`), :145 (`defaults.approval_option`). Defaults come from /home/coder/workspaces/worktrees/IronClaude/claim-handoff-planb/src/superclaude/cli/issue_watch/defaults.py:54-56. A test guards against literals at /home/coder/workspaces/worktrees/IronClaude/claim-handoff-planb/tests/issue_watch/test_repo_init.py:127.

## Other checks

- Task text: `gh label list/create --repo` at repo_init.py:58-84; org read is `gh api --method GET orgs/<owner>/issue-fields` at repo_init.py:87-90; the module never creates the field (repo_init.py:128-147).
- The read-only `trigger_label_state` (repo_init.py:93) is separate from the creating `ensure_trigger_label` (repo_init.py:108), as the task requires for R14.
- Residual risk, not blocking: the org issue-fields reply shape is unverified live (repo_init.py:14-16). It is read defensively, and anything unexpected returns `failed` or `approved_field_missing`.

## Findings

None blocking.

47ac0255d1d34740b379e9d5bf06abc74de437e5
## family codex-completion-time
defect form: Codex completion time read from a key other than updated_at/updatedAt
command: grep -n -e created_at -e createdAt src/superclaude/pr_submit/reviewers.py
before:
135:    for key in ("updated_at", "updatedAt", "created_at", "createdAt"):
coupled sites: _comment_updated_at key tuple; codex_review_state docstring (updated_at only)
after:
(no hits)

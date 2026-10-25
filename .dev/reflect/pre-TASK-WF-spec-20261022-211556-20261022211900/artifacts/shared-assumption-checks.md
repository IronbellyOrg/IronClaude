# Shared-assumption checks (orchestrator, read-only, 2026-10-22)

$ gh api repos/IronbellyOrg/IronClaude/actions/permissions/workflow
{"default_workflow_permissions":"read","can_approve_pull_request_reviews":true}
-> A-001 holds: gh is authenticated and can read the setting; can_approve_pull_request_reviews=true.

$ git check-ignore -v .venv .pytest_cache uv.lock .dev/reflect/x .ruff_cache
.gitignore:56:.venv/	.venv
.gitignore:215:uv.lock	uv.lock
-> .venv and uv.lock ignored; .pytest_cache/.ruff_cache not matched by .gitignore (pytest and ruff write their own inner .gitignore); .dev/reflect/ is untracked and not ignored, so it is part of the Task 1 baseline once it exists.

$ grep -n pyyaml pyproject.toml
38:    "pyyaml>=6.0",
-> A-002 holds: PyYAML is a declared dependency.

A-003 (boundary-guard test passes on base) NOT run here: running pytest would write into the worktree during a read-only review; left UNVERIFIED for the executor's Task 5.

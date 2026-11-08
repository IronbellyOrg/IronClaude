## Recommendations

Each recommendation names a file, the change and the verifier. They are drawn from the remediation fields of the merged register (`adversarial/merged-verdict.yaml`); nothing here is new.

### Recommendation R-001: Re-check the cutoff after the pending save and restore the whole document

- **File:** src/superclaude/cli/issue_watch/cycle.py
- **Change:** capture the document before `mark_pending`; after `self._save()` re-check `launch_allowed()`; if the cutoff has passed, `_set` the captured document, save it, and raise `_Skip("budget_exhausted")`. Restore the whole document (not field by field) because `validate` rejects partial undos.
- **Verifier:** a new case in `tests/issue_watch/test_cycle.py` whose clock passes 120 s inside `store.save`, asserting no launcher call, the restored document and a `budget_exhausted` decision line; then `uv run pytest tests/issue_watch -q`.
- **Linked deviation(s):** R-1
- **Priority:** P0

### Recommendation R-002: Replace the root-only skips with checks that hold for root and non-root

- **File:** tests/issue_watch/test_cli.py, tests/issue_watch/test_record.py, tests/issue_watch/test_cycle.py
- **Change:** produce the unreadable or unopenable state with a monkeypatched `PermissionError` instead of `skipif(os.geteuid() == 0)`, and give the mountinfo test a stubbed text instead of `pytest.skip`.
- **Verifier:** `uv run pytest tests/issue_watch -rs` reports 0 skipped, including when run as uid 0 in a container.
- **Linked deviation(s):** R-5
- **Priority:** P1

### Recommendation R-003: Detect the operation-unknown marker before the 500-byte stderr cap

- **File:** src/superclaude/cli/issue_watch/runner.py and src/superclaude/cli/issue_watch/launch.py
- **Change:** look for `agent_session_operation_unknown` on the full stderr before capping it, or keep a flag on `CommandResult`.
- **Verifier:** a new launch test with the marker placed after byte 500, expecting an `unknown` outcome.
- **Linked deviation(s):** R-6
- **Priority:** P1

### Recommendation R-004: Amend the design, the spec reason table and the task text for exit 1 and the 59 names (owner decision)

- **File:** docs/designs/issue-watcher.md (exit table and reason table), spec-final.md reason table, the executed task file Open Questions
- **Change:** record `cycle_crashed` (exit 1) and `cycle_complete` (exit 0) as accepted additions, list the 59 names, and state `once` exit 1. The owner may instead reject the additions; that choice is the human decision this report flags.
- **Verifier:** `uv run pytest tests/issue_watch/test_audit.py -q` (pins 59) and a grep of the design for the two names.
- **Linked deviation(s):** R-2, R-3
- **Priority:** P1

### Recommendation R-005: Settle the `valid_operation_id` import

- **File:** src/superclaude/cli/issue_watch/record.py, or the design import table plus the task text
- **Change:** either amend design section 5.3 and the task step to name `valid_operation_id`, or give `record.py` a local copy like `launch.py`; fix the miscounted docstring in `tests/issue_watch/test_module_boundaries.py`.
- **Verifier:** `uv run pytest tests/issue_watch/test_module_boundaries.py -q`.
- **Linked deviation(s):** R-4
- **Priority:** P1

### Recommendation R-006: Correct the runbook and design facts

- **File:** docs/designs/issue-watcher-setup.md and docs/designs/issue-watcher.md
- **Change:** list `reset` among the Linux-only verbs; add exit 2 to the `status` exit lists.
- **Verifier:** re-read against `cli.py` (`status` and `reset` config loading).
- **Linked deviation(s):** D-1
- **Priority:** P2

### Recommendation R-007: Remove the small code drifts

- **File:** src/superclaude/cli/issue_watch/cli.py, cycle.py, audit.py
- **Change:** stop using `cycle.format_utc` from `cli`; use the `github` and `predicates` values instead of the copies in `cycle`; pass `ts` into `audit.stderr_fallback` where the caller holds the clock; warn instead of dropping a retry entry whose argv cannot be built.
- **Verifier:** `uv run pytest tests/issue_watch -q` and `uv run ruff check src/superclaude/cli/issue_watch`.
- **Linked deviation(s):** D-2, D-3, D-4, R-7
- **Priority:** P2

### Recommendation R-008: Pin the local constant copies and state the one-store rule

- **File:** tests/issue_watch/test_launch.py (parity of the issue bound, login regex), docs/designs/issue-watcher-setup.md (already states one enabled workspace per login)
- **Change:** add parity assertions for the copies listed under N-1 and the login regex; keep the one-store-per-login rule visible as the scope of the at-most-once guarantee.
- **Verifier:** `uv run pytest tests/issue_watch/test_launch.py -q`.
- **Linked deviation(s):** N-1, advisory INV-001
- **Priority:** P2


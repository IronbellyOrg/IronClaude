# Wave 1.5 Branch C (semantic restrictions), persisted on receipt; degraded: true (auggie not in the analyst roster; Grep/Read + codegraph search)

| source_file:line | quoted_text (abridged) | applies_to |
|---|---|---|
| src/superclaude/pr_submit/conflicts.py:11-13 | "Standard library only (`base64`, `re`, `dataclasses`, `typing`)" | parser module allowlist (tomllib not listed) |
| src/superclaude/pr_submit/conflicts.py:16 | "No I/O, no clock, no environment reads, and no version-control command names anywhere in this file." | the function takes pyproject text, never reads the file |
| src/superclaude/pr_submit/conflicts.py:19-21 | "Every public function fails closed ... the most restrictive answer is returned (False, Tier 3, a halt class)." | fits halting when tomllib is missing or the text does not parse |
| tests/pr_submit/test_conflicts_core.py:2445 | `_ALLOWED_STDLIB = {"base64", "re", "dataclasses", "typing"}` | BLOCKER: `import tomllib` fails test_conflicts_imports_only_allowed_modules (:2449-2468, ast.walk sees imports inside try) unless the allowlist and docstring change |
| tests/pr_submit/test_conflicts_core.py:2473 | `banned = {"open", "__import__", "exec", "eval", "compile", "input", "print"}` | no importlib-style workaround |
| src/superclaude/pr_submit/conflicts.py:145, 165 | `HALT_REASONS` frozenset includes "sync_tier3" | reuse sync_tier3; a new reason needs an entry |
| tests/pr_submit/test_conflicts_core.py:1224-1234 | REPORT_REASONS & HALT_REASONS overlap pinned to eight | a new halt-only reason is safe |
| tests/pr_submit/test_run_log.py:174-175 (also test_codex_reviews.py:441) | `assert len(EventType) == 43` | add no event type |
| refs/conflict-mechanical.md:296 | `sync_tier3` row: "steps 5 to 6 (Tier 2 escalation: ...)" | extend the row text for a Tier 1 trust halt |
| src/superclaude/pr_submit/__init__.py:99 | `__all__ = [` | no test pins __all__; exporting is optional |
| tests/pr_submit/test_conflict_sync_protocol.py:70-72 | MECHANICAL_PINS "git checkout --ours -- uv.lock", "uv lock --check", "git add -- uv.lock" | step 5 lines stay verbatim |
| tests/pr_submit/test_conflict_sync_protocol.py:40 | ALLOWED_PROGRAMS {git, gh, uv, make, jq} (test :514-538) | a new fenced call must start with one of these or scripts/ |
| tests/pr_submit/test_conflict_sync_protocol.py:488-494 | exactly one ("conflict-mechanical.md", "git checkout") | no new checkout; a `git show` of a side must not be added as a checkout |
| tests/pr_submit/test_conflict_sync_protocol.py:544-557 | one probe, one finish-merge commit-mode command, one push | a fenced `uv run` line in step 5 breaks none |
| tests/pr_submit/test_conflict_sync_protocol.py:94-111 | order pins cover steps 1 and 10(a) only | nothing pins order inside step 5 |

All flagged D-N references removed, and all missing spec items (files, functions, test paths) are now referenced in the roadmap.

Summary of changes applied to `roadmap.md`:

**Removed/rephrased D-N references** (5 HIGH findings):
- `D-1..D-8` → `8 ADR entries` / `all 8 ADR entries` (in SC1 row + Success Criteria table)
- `(debate D3 compromise)` → `(per debate compromise)`
- `(debate D5)` → `(per debate convergence)` (in M2 and M5 OQ-10)
- `(debate D6 convergence)` → `(per debate convergence)` (DOC-OQ4 + M2 Entry)
- `(debate D12)` → `(per debate convergence)` (M5 Duration, Decision Summary, Timeline footer)

**Added spec file references** (4 HIGH findings):
- `src/superclaude/cli/install_hooks.py:install_hooks` — added to COMP-014 + External Dependencies
- `src/superclaude/hooks/hooks.json` — added to COMP-014 + External Dependencies
- `tests/cli/test_install_hooks.py` — added to External Dependencies
- `tests/cli/test_eval/test_pty_vendor.py` — added to External Dependencies

**Added spec function references** (11 HIGH findings):
- All 11 predicate helpers (`contains_event`, `does_not_contain`, `event_count`, `greater_than`, `has_content_matching`, `has_mode`, `has_registration`, `hooks_count`, `is_valid_jsonl`, `less_than`, `matches_line`) added to COMP-010 ExpectDSL interface AC.

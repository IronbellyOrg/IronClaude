# D-0011: Rename _parse_frontmatter() → parse_frontmatter() — evidence.md

**Task:** T02.02
**Roadmap Item:** R-021
**Date:** 2026-03-16
**Status:** COMPLETE

---

## Rename Scope

| File | Change |
|------|--------|
| `src/superclaude/cli/roadmap/gates.py` | Renamed function definition `_parse_frontmatter` → `parse_frontmatter`; all internal callers updated (2 call sites: `_high_severity_count_zero`, `_tasklist_ready_consistent`) |
| `src/superclaude/cli/roadmap/executor.py` | Import and call site updated: `from .gates import _parse_frontmatter` → `from .gates import parse_frontmatter`; `_parse_frontmatter(content)` → `parse_frontmatter(content)` |
| `tests/roadmap/test_phase7_hardening.py` | Two import+call sites updated (lines 301-302 and 333-334) |
| `tests/roadmap/test_resume_pipeline_states.py` | Comment-only reference — no code change required |

## Verification

- `grep -rn "_parse_frontmatter" src/ tests/` returns only 1 comment-only reference in `test_resume_pipeline_states.py:351` — no live code references remain.
- `uv run pytest tests/roadmap/test_gates_data.py tests/roadmap/test_phase7_hardening.py tests/sprint/test_models.py -v` → **206 passed**

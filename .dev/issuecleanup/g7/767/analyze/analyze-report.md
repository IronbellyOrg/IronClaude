# /sc:analyze: src/superclaude/cli/sweep (architecture, quick)

Codegraph: index_state=fresh, checked_at=2026-11-24T20:39:52Z; degraded: graph:unused (Grep/Read floor used at quick depth)

## Findings
1. MEDIUM, architecture: `report.py` renders one flat Markdown file with no size budget, summary-only mode, or change-since-last-run mode. Evidence: no `click.option` besides --run/--window/--root/--output (`commands.py:220-238`); `render` (`report.py:608`) emits every SECTIONS block.
2. MEDIUM, duplication: a non-idle unknown row is rendered in `_could_not_determine` (`report.py:327-350`) and again in `_sessions` (`report.py:405-445`, filter `class_name != _IDLE`).
3. MEDIUM, policy coupling: the skill requires a full chunked read to `Report complete` (`SKILL.md:25`; terminator at `report.py:542`), and WORKER-CONTRACT WC-16 (line 290) runs it on every coordinator wake (max once per 5 minutes). The cost is set by that policy, not by the Python code alone.
4. Note: tests in `tests/sweep/` cover the bound-line and sections but no output-size budget.

## Metrics
sweep package 3,825 lines (classify 1009, probes 1477, report 695, models 278, commands 288); 6 test modules.

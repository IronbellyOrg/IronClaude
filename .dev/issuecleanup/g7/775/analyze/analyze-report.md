# /sc:analyze report: src/superclaude/cli/issue_watch (architecture, quick)

Codegraph: index_state=fresh, checked_at=2026-11-24T20:45:55Z; degraded: none (no graph lookups needed; lines confirmed by Grep and Read)

Scope: issue 775's area, the approval-cancel rule of the issue watcher (about 6,900 lines across src/superclaude/cli/issue_watch/).

## Findings

1. (Info) The rule is one pure function. `unchanged_since` at `src/superclaude/cli/issue_watch/predicates.py:275-297` checks body creation and edit times, every comment not authored by `own_login` (line 292), and every `renamed` event; an equal timestamp counts as changed (line 295).
2. (Info) Single call site. `src/superclaude/cli/issue_watch/cycle.py:1014-1021` calls it and raises `_Skip(why)`. `src/superclaude/cli/issue_watch/audit.py:71` classifies `edited_after_approval` as ("skip", 0): exit code 0, no GitHub write.
3. (Medium, architecture) The plan-approval code deliberately does not reuse this predicate (`src/superclaude/cli/issue_pipeline/stage_predicates.py:7-10`), so a rule change in `unchanged_since` does not reach the plan stage. Two rules for "unchanged" exist by design.
4. (Medium) The skip is visible only in the local audit log. `status_report` (`cycle.py:1400`) exists, but the issue records that it does not read the audit log (not re-verified in depth at quick depth).
5. (Info) Documentation already states the rule: `docs/designs/issue-watcher-setup.md:182, 358, 566, 645`. The issue templates in `.github/ISSUE_TEMPLATE/` (bug_report.yml, config.yml, feature_request.yml, other.yml) contain no text on approval.

## Recommendations

Owner decision first (the issue records no choice). Smallest option is (a): add the cancel rule to the template text. Behaviour change options (b), (c), (d) need the owner's pick and the shared-login decision in issue 722.

No source was modified.

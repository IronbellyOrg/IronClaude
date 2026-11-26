# Findings: issue 775 (approval cancelled by any foreign comment is silent)

Issue: https://github.com/IronbellyOrg/IronClaude/issues/775, open, label `enhancement`, no comments, last updated 2026-11-24T18:28:30Z. Checked on 2026-11-24 against the worktree at branch `ironbelly/Issuecleanup` (HEAD a7ae3dd30). Analyze run: `.dev/issuecleanup/g7/775/analyze/analyze-report.md`.

## Verdict

**still-relevant.** Nothing in the issue is done, and nothing has been started (no PR and no branch mention it; `gh pr list --search` for 775, `edited_after_approval` and `unchanged_since` returned no PR). The issue is also waiting on an owner decision: its first acceptance criterion is that the owner records which of options (a) to (d) to take, in what order, whether the own-login exemption stays, and who is told where.

Real current state, confirmed in source:

- The rule is `unchanged_since` at `src/superclaude/cli/issue_watch/predicates.py:275-297`. It collects the issue creation and last-edit times, the creation and edit times of every comment whose `author_login != own_login` (line 292), and every `renamed` event, and returns `edited_after_approval` if any time is at or after the approval time (line 295). An equal timestamp counts as changed.
- Its only call site is `src/superclaude/cli/issue_watch/cycle.py:1014-1021`; a non-None result raises `_Skip(why)`.
- `src/superclaude/cli/issue_watch/audit.py:71` classifies `edited_after_approval` as `("skip", 0)`: exit code 0, so no alert tied to exit codes 3 to 7 fires.
- `status_report` (`src/superclaude/cli/issue_watch/cycle.py:1400`) states in its docstring that `audit` is "accepted for the fixed signature and not read", so status output cannot show the skip today. This matches the issue.
- The runbook already states the rule and the recovery: `docs/designs/issue-watcher-setup.md:182` (nothing may change after approval; comment by anyone but the watcher's login), `:358` (exit table row), `:566` (clear `Approved`, wait, set `Yes`), `:645` (risk R17). So option (a) is partly done for the runbook. It is not done for the issue templates: `.github/ISSUE_TEMPLATE/` holds bug_report.yml, config.yml, feature_request.yml and other.yml, and a grep for "approv" and "comment" found no approval wording there.
- The plan stage uses a separate predicate on purpose (`src/superclaude/cli/issue_pipeline/stage_predicates.py:7-10`; comment channel at lines 17-22 ignores every commenter other than assignee or approver). A change to `unchanged_since` does not reach the plan stage.
- No commit since #707 (2ea524514) touches the rule: `git log` on `predicates.py` and `audit.py` shows only 2ea524514 and the earlier 4c93b6c73; the later watcher fix f75cf81e3 (#759, first-run setup retry) is unrelated.
- Issue text says line numbers were checked 2026-11-24; all the lines above still match.
- UNVERIFIED: whether the acceptance wording "no new GitHub write" fits `tests/issue_watch/test_security_invariants.py`; I did not read that test file. UNVERIFIED: the exact list of status fields from `status_report` beyond its docstring.

## Complexity and size

Complexity **medium**, size **M** (for the full set of options). Reason: option (a) alone is XS (template and runbook text), but (b) adds a new GitHub write path or status field behind an owner gate and security-invariant tests, (c) needs a new command or skill entry point, and (d) needs a decision on shared-login identity (#722).

## Priority

**P2.** The issue's own priority says High because an approved issue silently stalls. Weighed here: it is a recorded owner choice (risk R17, requirement R19 and R37), the recovery is documented, the fix is blocked on an owner decision and on #722 for option (d), and nothing else is blocked by it. The runbook-only part (a) is cheap and could be done at once.

## Concrete next steps

1. Owner records the choice in chat: which of (a), (b), (c), (d), their order, whether the own-login exemption stays, and who is told where (the three open questions). The agent in that session records it; the owner writes no file.
2. If (a): add the plain wording of what cancels an approval and how to approve again to the issue template text (`.github/ISSUE_TEMPLATE/feature_request.yml` and `other.yml` at minimum, UNVERIFIED which templates the owner wants) and keep the runbook lines 182, 566 and 645 in step. No behaviour change, no tests beyond a docs check.
3. If (b): decide the place (status line, issue comment, alert). A status line needs `status_report` to read the audit log. An issue comment is a new GitHub write and needs the owner's agreement. Add tests in `tests/issue_watch/test_cycle.py`, `test_cli.py` or `test_audit.py`.
4. If (c) or (d): resolve #722 (shared login) and #753 (approver rule) first; then change `unchanged_since` in place and extend `tests/issue_watch/test_predicates.py` and `test_cycle.py`.
5. Run `uv run pytest tests/issue_watch/ tests/issue_pipeline/`, `make lint`, `make verify-sync`; submit through `/sc:pr-submit --monitor 3`.

## Dependencies

- Needs: the owner's decision recorded (this issue's first acceptance criterion). For option (d): #722 (shared login, who approved) and #698 (who counts as an approver in plan approval); #753 (maintainers and admins as approvers) must be checked for overlap first.
- Option (b) shares an alert destination with #717 (W8).
- Blocks: nothing found.

## Related issues

#707 (merged watcher; source of the rule), #761 (gap check that found this), #717 (W2 and W8; the W8 alert does not cover exit-0 skips), #716 (C8 note: keep one "unchanged" test), #722 (shared login), #698 (approver check by text and assignee), #753 (admins and maintainers as approvers; open, not a duplicate as far as read: its scope is who may approve, not what cancels approval).

## Related PRs

#707 (merged; introduced `unchanged_since`, R17, R19, R37), #759 (merged; later watcher fix, unrelated to the rule), #729 (merged; records that the merged watcher is the design). No open PR addresses this issue.

Review 1-1 of T177 (fresh subagent, prompt-1-1.md): T177.AC1 unmet behind F1.1.
F1.1 ac=T177.AC1 at=src/superclaude/cli/sweep/report.py:585-592 anchor="`sanitize` neutralises `|`, ANSI escapes, bidi controls, HTML tags and Markdown links so the column count holds" chk=y,n,n,n family=sanitize-backslash: sanitize escapes `[`, `]` and `|` but not a backslash the text supplies, so `\[x\](http://e)` becomes `\\[x\\](http://e)` (a live link) and `a\|b` becomes `a\\|b`.
F1.2 note report.py:164-171 chk=n,n,n,n: _version_line splits only on `-`, not on the leading MAJOR.MINOR.PATCH part; errs toward UNVERIFIED.
F1.3 note report.py:379 chk=n,n,n,n: the Retained problems cap line is a count with no Distinct line; logged as choice (7).
F1.4 note report.py:419-427 chk=n,n,n,n: the Sessions table has a leading ID column; logged as choice (5).
F1.5 note report.py:633-689 chk=n,n,n,n: sanitize also alters `[`, `]`, `<`, `>` and `|` in JSON path values (report_path, scope.root, worktree paths); follows DESIGN literally.
F1.6 note classify.py:269 chk=n,n,n,n: the frozen-plan evidence text from classify contains "STOP code"; it describes a contract field, not an action.
Review 2-1 of T177 (fresh subagent, prompt-2-1.md): T177.AC1 met. F1.1 resolved. No blocking findings.

# Branch B result (parent-finalized)

Currency method: filesystem mtimes are all the same (1794976366 = checkout time of this worktree), so they carry no information; the parent used `git log -1 --format=%cI` per file instead. Code `src/superclaude/cli/install_keep.py` last commit 2026-11-09T22:21:16-05:00. No doc is 90 days behind it; no doc header says deprecated or archived; no `Last reviewed` marker exists.

```json
[
  {"doc_path": "/home/coder/workspaces/worktrees/IronClaude/issue-606/docs/getting-started/upgrading.md", "summary": "Step 1 says the upgrade overwrites every shipped file and keeps no backup of an edited ~/.claude/CLAUDE.md or RULES.md; plain install skips existing files, update and install --force refresh them. No content-comparison rule is described.", "currency_verdict": "current", "reason": "git last commit 2026-11-03, 6 days before the code; no header markers. Possible content drift: install_keep.py (2026-11-09, #480) now saves a differing file as <name>.bak.<stamp> before a forced overwrite, which this doc does not say."},
  {"doc_path": "/home/coder/workspaces/worktrees/IronClaude/issue-606/docs/getting-started/installation.md", "summary": "Lists --force as 'Overwrite existing files'; settings.json.bak.<timestamp> written before the settings merge. No content-comparison rule.", "currency_verdict": "current", "reason": "git last commit 2026-11-04; no header markers."},
  {"doc_path": "/home/coder/workspaces/worktrees/IronClaude/issue-606/docs/user-guide/freshness-hooks.md", "summary": "settings.json is backed up to settings.json.bak.<ISO-8601> before every hook install write; different code path (install_hooks.py).", "currency_verdict": "current", "reason": "git last commit 2026-11-03; no header markers; not about install_keep.py."},
  {"doc_path": "/home/coder/workspaces/worktrees/IronClaude/issue-606/docs/reference/troubleshooting.md", "summary": "Restore recipe for a bad settings.json merge using the newest settings.json.bak.* file.", "currency_verdict": "current", "reason": "git last commit 2026-11-03; no header markers; settings.json only."},
  {"doc_path": "/home/coder/workspaces/worktrees/IronClaude/issue-606/docs/designs/orchestrator-mode.md", "summary": "Tangential: a test (routing plugin parity) uses filecmp.cmp(..., shallow=False) as a byte-copy check. Nothing on keep-vs-overwrite.", "currency_verdict": "current", "reason": "git last commit 2026-11-16; header line 5 'Status: design for review'; not deprecated."}
]
```

Not found: no document describes `same_content`, `backup_if_differs` or `filecmp` result caching for install keep-vs-overwrite.

Harness note: the harness flagged the worker output for an instruction-like pattern ("settings-json") and neutralized angle-bracket tags (`<timestamp>` became `&lt;timestamp&gt;`). The content is plain documentation text about `settings.json.bak.<timestamp>`; no instruction was present or followed.

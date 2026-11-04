```json
[
  {
    "doc_path": "/home/coder/workspaces/worktrees/IronClaude/issue-330-ponytail-plugin/docs/getting-started/installation.md",
    "summary": "installation.md:345 says the installer merges settings defaults for 'only keys you have not set'; installation.md:458-464 gives the opt-out as \"ponytail@ironclaude\": false and warns a deleted key comes back as true; installation.md:393-411 says the next install adds ponytail@ironclaude beside ponytail@ponytail 'so both are enabled' and leaves ponytail@ponytail alone. It never covers a user who opted out with \"ponytail@ponytail\": false.",
    "currency_verdict": "current",
    "reason": "no markers found; parent mtime check: doc 1793805987 vs code 1793805928 (doc newer, not >=90 days behind)"
  },
  {
    "doc_path": "/home/coder/workspaces/worktrees/IronClaude/issue-330-ponytail-plugin/CHANGELOG.md",
    "summary": "CHANGELOG.md:11 [Unreleased] gives the opt-out as \"ponytail@ironclaude\": false (a deleted key is added back); CHANGELOG.md:14 says installs from #358 get ponytail@ironclaude beside ponytail@ponytail 'so both are enabled'. Nothing about carrying over an earlier \"ponytail@ponytail\": false.",
    "currency_verdict": "current",
    "reason": "no markers found; parent mtime check: doc 1793805999 vs code 1793805928 (doc newer)"
  }
]
```

degraded: true (auggie not used; Grep/Read). Out-of-scope related mention: `docs/getting-started/upgrading.md:42` (settings.json backup).

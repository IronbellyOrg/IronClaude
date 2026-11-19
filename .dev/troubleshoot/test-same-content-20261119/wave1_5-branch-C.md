# Branch C result (restrictions; line numbers re-read by the parent where noted)

No MUST / MUST NOT / SHALL / FORBIDDEN / NEVER wording exists about `same_content` or `backup_if_differs`. Docstring contracts instead (marked as such):

```json
[
  {"source_file": "/home/coder/workspaces/worktrees/IronClaude/issue-606/src/superclaude/cli/install_keep.py", "file_line": 19, "quoted_text": "True only when both files are readable and byte-identical.", "applies_to": "same_content(a, b): the docstring absolute; any OSError returns False"},
  {"source_file": "/home/coder/workspaces/worktrees/IronClaude/issue-606/src/superclaude/cli/install_keep.py", "file_line": 39, "quoted_text": "Returns ``None`` when the files already match. Raises ``OSError`` when the copy cannot be made; the caller must then leave ``target`` untouched.", "applies_to": "backup_if_differs: contract on its callers"},
  {"source_file": "/home/coder/workspaces/worktrees/IronClaude/issue-606/src/superclaude/cli/install_keep.py", "file_line": 3, "quoted_text": "a kept file that differs from this version's copy is stale or customized and should be named in the report.", "applies_to": "module docstring: a false 'identical' answer from same_content would hide a stale file"},
  {"source_file": "/home/coder/workspaces/worktrees/IronClaude/issue-606/src/superclaude/cli/install_user_setup.py", "file_line": 77, "quoted_text": "Without ``force`` an existing file is kept; a kept file that differs from the shipped copy is appended to ``stale``. With ``force`` a differing file is saved aside first", "applies_to": "_copy_tree, caller of same_content (:90) and backup_if_differs (:95)"},
  {"source_file": "/home/coder/workspaces/worktrees/IronClaude/issue-606/src/superclaude/cli/install_commands.py", "file_line": 65, "quoted_text": "# A forced overwrite first saves a differing file next to itself", "applies_to": "caller of backup_if_differs (:68); same_content at :61"}
]
```

The test-side row of the worker (tests/cli/test_install_keep.py:41-44) is confirmed: the parent read lines 37-44 in this session (`assert same_content(a, b)` at 41, `assert not same_content(a, b)` at 43, `assert not same_content(a, tmp_path / "missing")` at 44).

The worker could not confirm the `filecmp` cache claim; the parent confirmed it (see `tier1-observation.md`: stdlib source and probe output).
Also found by the parent: other callers of `same_content`: `src/superclaude/cli/install_user_setup.py:90`, `src/superclaude/cli/install_commands.py:61`; `install_core.py:121` has its own private `_same_content`.

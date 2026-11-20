4c11643e16e94ee6df28c157dda026866c7376e0
# Review of Task 19 (attempt 1)

Checked on disk, not from the implementer's report. `uv run pytest tests/issue_watch -q` gave 2915 passed.
`git status` shows `generate.py` and `test_generate.py` untracked on disk. `test_module_boundaries.py` and
`test_security_invariants.py` are modified.

## Earlier blocking findings

None (first review).

## Acceptance criteria

- T19.AC1 met. Citation: T19.AC1@tests/issue_watch/test_generate.py:89 (one Project), :119 (none), :126 and :135 and :143
  (several, with and without a defaults entry), :152 (failed account read), :167 (maintainers added),
  :174 (launch id never written), :222 (existing config untouched), :111 (modes 600 and dir 700),
  :253 (two repos, two `state_dir`). Paths are under `tmp_path` through the `base` fixture. F1.1 is a
  non-blocking nit about the real-home assertion, and the check that matters (`tmp_path/"home"` absent
  with HOME redirected) is real at test_generate.py:80.
- T19.AC2 met. Citation: T19.AC2@tests/issue_watch/test_generate.py:100 (`cycle.load_config(config)` on a
  generated config) and src/superclaude/cli/issue_watch/generate.py:268 (the generator itself runs
  `load_config` and `validate_approvers` at :269 before `os.link` at :270). The full suite passes
  (2915 passed).
- T19.AC3 met. Citation: T19.AC3@src/superclaude/cli/issue_watch/generate.py:91 (account), :95 (users/<login>),
  :101 (Project query), :116 (collaborators). Every REST builder carries `--method GET` (:92, :98, :119-:121).
  The GraphQL call is a pure query (`PROJECTS_QUERY`, :49). The scan covers the four builders at
  tests/issue_watch/test_security_invariants.py:1104.

## Requirement-by-requirement checks (all pass)

- `ensure_config(repo_record, defaults, runner, base)` signature: generate.py:192. `Base` holds the config dir and the state dir, with the defaults at :67-:73.
- R2, `no_project` and `project_ambiguous`, and the defaults-map id: generate.py:212, :219-:220, :221-:227.
- R4, fixed logins turned into ids, maintainers added, launch id removed: generate.py:229-:243.
- Config content (absolute `worktree`, `approvers_file`, explicit `state_dir`, `repo`, Project id, account id, `enabled: false`): generate.py:245-:255.
- Mode 600 through `os.open(..., 0o600)` with O_EXCL and O_NOFOLLOW: generate.py:183. Never overwrites: :207-:210 and the `os.link` at :270.
- `state_dir` is created by the first run, so the docstring claim at generate.py:19 is true (record.py:777).

## Findings

F1.1 ac=T19.AC1 at=tests/issue_watch/test_generate.py:82 anchor=`assert not (real / ".config/superclaude/issue-watch.d/GenTestOnly.json").exists()` chk=n,n,n,n family=test-weak-assert fix=drop the `real` line or resolve the real home before HOME is patched, and assert that the real `IronClaude.json` is unchanged [covers="asserts nothing was written under the real home"]: non-blocking nit. `real` is computed with `os.path.expanduser("~")` after HOME is redirected, so it points into `tmp_path`, and the file name `GenTestOnly.json` is never produced. That line proves nothing. The first assertion (line 80) does prove it, because HOME is redirected and any `~` write would create `tmp_path/home`.

F1.2 ac=scope at=src/superclaude/cli/issue_watch/generate.py:52 anchor=`nodes { id number }` chk=n,n,n,n family=brief-departure fix=none [covers="`nodes{ id number title }`"]: non-blocking. The Project query leaves out `title`, which the brief names. The departure is disclosed, and `_TEXT_FIELD` in test_security_invariants.py:79 forbids a `title` field in watcher queries. The title is not used.

F1.3 ac=scope at=src/superclaude/cli/issue_watch/generate.py:122 anchor=`collaborators?permission=maintain&per_page=100` chk=n,n,n,n family=brief-departure fix=none: non-blocking. The URL adds `per_page=100` to the brief's URL. It is a read, and it is not paginated beyond 100.

F1.4 ac=scope at=src/superclaude/cli/issue_watch/generate.py:260 anchor=`directory.chmod(0o700)` chk=n,n,n,n family=perm-change fix=none: non-blocking. It tightens the mode of the `issue-watch.d` directory, which this module creates or owns. Nothing tracked or production is touched.

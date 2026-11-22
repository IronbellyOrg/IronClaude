pick: advice-3-a.md; runner-up: none; reason: only passing answer
## Task 2: Create the script skeleton with the allowlisted command runner
Acceptance criteria:
- `uv run --no-project python scripts/worktree_cleanup.py --help` lists the four verbs and the two flags; `main(["list"], runner=...)` can be called from a test with an injected runner.
- `Runner.check_allowed` raises a dedicated refusal error for each banned shape listed above before any process starts and for an unlisted command such as `git reset` (asserted in `tests/worktree_cleanup/test_runner.py`, which this task creates; Task 13 extends them across every verb).
- An `ast` scan of the file finds only standard library imports and no call to `os.remove`, `os.unlink`, `shutil.rmtree` or a command named `rm`.
- The Apache-2.0 notice block and the pointer to `scripts/worktree_cleanup_PROVENANCE.md` are at the top of the file.
AC ids (in source order): T2.AC1, T2.AC2, T2.AC3, T2.AC4
Steps:
1. Start from the reverted tree. Reuse the notice block, docstring, constants, parser, `main`, the `ast`, notice and no-dash tests, and the conftest loader from the earlier attempt.
2. Write one helper, `_match(tail, flags, values, positional)`. It takes a set of exact flags, a set of flags that take a value, and a check for the positional arguments. Any other token starting with `-` raises `RefusedCommand`. A positional that starts with `-`, `+` or `:` raises it too. Build every verb check on this helper.
3. git, global options: `-C <dir>` sets the working folder. `-c` is allowed only as `CREDENTIAL_HELPER`, and only when the verb is `push`.
4. git read verbs, each with its own exact flags:
   - `status`: `--porcelain`, `-z`, `--ignored`, `--untracked-files=all`
   - `rev-parse`: `--git-dir`, `--git-common-dir`, `--show-toplevel`, `--verify`, `--abbrev-ref`, plus revisions
   - `log`: `-1`, and `--format=` matched as a prefix
   - `ls-files`, `ls-tree -r --name-only`, `merge-base --is-ancestor A B`, `rev-list --count R`, `diff --quiet R -- P`
   - `remote get-url origin`, `config --get K`
   - `worktree list --porcelain`
   - Never allow `--output`.
5. git write verbs:
   - `worktree remove <path>` and `branch -d <name>` must be exactly three tokens.
   - In the evidence clone only:
     - `clone <url> <evidence_dir>`
     - `fetch [--quiet] origin`
     - `add -- <paths>`
     - `commit [--quiet] -m <msg>`
     - `rebase origin/main`
     - `push [--porcelain] origin <branch>`, where the branch must match `^[A-Za-z0-9._/-]+$`.
   - For every evidence-clone verb except `clone`, the real path of the working folder must equal the evidence folder. When no working folder is given, refuse.
6. orca:
   - `repo list`, `worktree list`, `worktree ps` with `--json` only
   - `reference list` and `terminal list` with `--worktree <sel> [--json]`
   - `worktree rm --worktree <sel>`, exactly four tokens
   - `terminal close --worktree <sel> --all`, only when the selector is in `close_authorized`
7. gh: only `pr list`, `pr view <digits>` and `issue view <digits>`. Allowed value flags are `--repo` (required, must match owner/repo), `--head`, `--state`, `--json` and `--limit`. Refuse every other flag.
8. Other programs:
   - `tar`: only `-tzf <path>`.
   - `xargs`: only `-0 git clean -f -x --`, as before, with the saved-paths check on standard input.
   - The landed check: `[bash] <path> <digits>`, where the real path of `<path>` must be one of the three lookup locations from Task 1. Make those locations a `Runner` field.
   - Everything else is refused.
9. In `_env_for`, keep `GH_TOKEN` (and `GITHUB_TOKEN`) only for gh, the landed check and the git verb `push`. Remove both from every other child. Set `GIT_LITERAL_PATHSPECS=1` only for xargs. Keep `_execute` as the one hook tests can override.
10. In `tests/worktree_cleanup/test_runner.py`, add refusal cases (all refused, none started, none recorded):
    - `git push -df origin topic`, `-fd`, `--dele`, `--forc`, `--mirror`, `-o x`, `origin +main`, `origin main:main`, `origin :topic`
    - `orca worktree rm --worktree id:1 --forc`, and `--force=true`
    - `git worktree remove --forc /x`
    - `git branch -Dq t`, and `-d -f t`
    - `git clean -fx`
    - `git log --output=/tmp/x`
    - `git -c core.sshCommand=x status`
    - `git reset`
    - a push from outside the evidence clone

    Move clone and fetch into the token-absent test.
11. Run `uv run pytest tests/worktree_cleanup -v`, `uv run ruff check scripts/worktree_cleanup.py tests/worktree_cleanup` and `uv run --no-project python scripts/worktree_cleanup.py --help`.
differs-by: every verb, push included, is checked against a positive list of exact token shapes, so no deny-set matching remains anywhere, and the token is limited to gh, the landed check and `git push`.

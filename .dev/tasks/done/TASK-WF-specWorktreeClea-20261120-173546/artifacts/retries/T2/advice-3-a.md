model: top rung (tier unknown) family: claude rung: top  entry: escalation 1, adviser A
outcome: ready

| AC | why the earlier attempt missed it (path:line) | change |
|---|---|---|
| T2.AC1 | Met. The parser and `main(argv, runner, env)` are at attempt-2.diff:479-534, and the review accepted them at review-2.md:3. | Keep the same parser and the same `main` signature. |
| T2.AC2 | Missed. The push check compares each whole token against a fixed deny set (attempt-2.diff:297-308). So `-df`, `-fd` and `--dele` get through (review-2.md:7). Its tests check only the exact spellings (attempt-2.diff:731-737), which is why all tests still passed (extras-2.log:7). `orca worktree rm` has the same weakness (attempt-2.diff:360). Read verbs accept any option at all (attempt-2.diff:232-233). | Every verb gets a positive list of its exact option shapes. Any token starting with `-` that is not on the list is refused. Add tests for the bundled and shortened spellings. |
| T2.AC3 | Met. Imports are at attempt-2.diff:41-48 and the `ast` test at attempt-2.diff:872-883, accepted at review-2.md:5. | Keep both. |
| T2.AC4 | Met. The notice block is at attempt-2.diff:8-12, accepted at review-2.md:6. | Keep it. |
| scope (F2.2) | `_needs_token` also gives the token to `git clone` and `git fetch` (attempt-2.diff:430), and the tests require it (attempt-2.diff:949-950). The plan names only gh and git push (plan line 47, review-2.md:8). The plan file cannot be edited, because edits are allowed only under the listed folders (plan line 27). | The token goes only to gh, the landed check (it runs gh) and `git push`. Clone and fetch move to the tests where the token must be absent. |

differs-by: every verb, push included, is checked against a positive list of exact token shapes, so no deny-set matching remains anywhere, and the token is limited to gh, the landed check and `git push`.

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

Files: /home/coder/workspaces/worktrees/IronClaude/issue-687/scripts/worktree_cleanup.py and /home/coder/workspaces/worktrees/IronClaude/issue-687/tests/worktree_cleanup/test_runner.py

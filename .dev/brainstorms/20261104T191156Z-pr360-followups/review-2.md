# Review 2: PR #360 follow-ups (adversarial re-review)

Scope: uncommitted diff in `src/superclaude/cli/install_user_setup.py`,
`tests/cli/test_install_user_setup.py`, `CHANGELOG.md`,
`docs/getting-started/installation.md`. Baseline: `HEAD` (605da2ff). Round 1:
`review-1.md` (B1 only blocking finding).

## Verdict

PASS. B1 is fixed: every factual claim in the new CHANGELOG entry and the
`CLAUDE_CONFIG_DIR` note matches the code, and the rewording added no false
user-facing claim. The tests pass on Python 3.13 and 3.11, and ruff is clean.
One code comment still carries the old B1 wording (Minor 1).

## Blocking findings

None.

## Minor findings

1. A code comment still makes the false B1 claim.
   `src/superclaude/cli/install_user_setup.py:404-405` says home/.claude is "the
   one every other install step writes, never one CLAUDE_CONFIG_DIR names". The
   codegraph step (`main.py:246` -> `install_mcp.py:896`) and the retire step
   (Minor 2) run `claude mcp` with the inherited `CLAUDE_CONFIG_DIR`, so with
   that variable set they write `$CLAUDE_CONFIG_DIR/.claude.json`, not
   home/.claude. It is not blocking: the comment is internal, the code it
   describes behaves correctly, and its subject (the plugin commands) is right.
   Suggested wording: "the profile whose plugin records were checked above, and
   where the installer writes its own files; MCP registrations are the only
   step that follows CLAUDE_CONFIG_DIR".
2. The MCP exception is named for codegraph only. The retire step
   (`main.py:257-263` -> `install_retired_mcp.py:393-441` ->
   `install_mcp.py:824` read and `:837-838` `claude mcp remove ... --scope user`)
   also reads `.claude.json` from `CLAUDE_CONFIG_DIR` (`install_mcp.py:721-726`)
   and removes registrations in that profile. The docs note's general sentence
   ("MCP registrations are the exception", `installation.md:497`) covers it, and
   neither text says that codegraph is the only case, so nothing is false. Adding
   "and the retire step's `claude mcp remove` calls" to `installation.md:499`
   would make the list complete.
3. The CHANGELOG bullets name only `superclaude install`
   (`CHANGELOG.md:11-12`). The same `install_user_setup` runs on
   `superclaude update` (`main.py:404`), so the fixes apply there too. The
   bullets are not wrong, only narrower than the behaviour.

## Self-audit

What I checked, and the result:

- CHANGELOG bullet 1 (`CHANGELOG.md:11`):
  - "Raises on Python 3.10 to 3.12": run here, `Path.resolve()` on a symlink
    loop raises `RuntimeError` on 3.11.15 and does not raise on 3.13.5. The NUL
    path raises `ValueError` on both.
  - The exception is caught at `install_user_setup.py:292-295`, which returns
    False.
  - "Refused like one from another source, the other plugins still install":
    `:355-373` drops only the pinned plugins and leaves the registry untouched.
    The new test asserts the playwright install and an unchanged registry.
  - True.
- CHANGELOG bullet 2 (`:12`):
  - `installed` keeps only records whose scope is `user`, or that have no
    scope (`install_user_setup.py:324-329`), and the stale check uses only
    those (`:335-342`).
  - A plugin with only project-scope, local-scope or empty records is not in
    `installed`, so it gets `plugin install --scope user` (`:383-387`).
  - True.
- CHANGELOG bullet 3 (`:13`):
  - Every `claude plugin` command goes through the single `subprocess.run` at
    `install_user_setup.py:411`. Its env drops `CLAUDE_CONFIG_DIR` and sets
    `HOME=home` (`:406-407`).
  - In production `home` is `Path.home()` (`:306`).
  - The plugin records are read from `home/.claude/plugins` (`:318-320`).
  - The installer writes its own files under `Path.home()/.claude`: rules and
    settings (`install_user_setup.py:115,118,163`), commands
    (`install_commands.py:156`), skills (`install_skills.py:160`), agents
    (`install_agents.py:135`), and hooks and settings (`install_hooks.py:140`,
    docstring `:4-5`).
  - No other `claude plugin` call exists in `src/superclaude/cli`, `*.sh` or
    the `Makefile` (grep).
  - "The codegraph MCP registration still follows CLAUDE_CONFIG_DIR": the
    lookup is at `install_mcp.py:721-726`. `_claude_user_entry_cmd` ->
    `_exec_claude` -> `_bounded` (`:893-896`, `:799-801`, `:775-783`) passes no
    `env=`, so the variable is inherited.
  - True.
- Docs note (`installation.md:494-501`):
  - Plugin commands act on `$HOME/.claude/`: true, as for bullet 3.
  - The installer reads `.claude.json` from `CLAUDE_CONFIG_DIR`: true
    (`install_mcp.py:721-726`).
  - The `claude mcp` commands that register codegraph act on that profile:
    true (inherited env, as above).
  - "An empty `CLAUDE_CONFIG_DIR` makes that lookup fail ... exits 1": true.
    `read_user_mcp_servers` returns `(False, {})` (`install_mcp.py:722-723`),
    then `install_codegraph_mcp` returns False (`:954-958`), then `main.py:278-280`
    calls `sys.exit(1)`. The plugin step now strips the empty value, so it is
    unaffected.
- No new false claim: I re-read each sentence of both texts against the code
  above. The only residue of B1 is the code comment (Minor 1).
- Regressions:
  - `uv run --extra dev pytest tests/cli/test_install_user_setup.py -q`: 29
    passed (Python 3.13.5).
  - The same file under Python 3.11 (throwaway venv in `/tmp`, removed
    afterwards, `--offline`, `-p no:cacheprovider`): 29 passed. This runs the
    `RuntimeError` branch of the symlink-loop test that 3.13 cannot reach.
  - `ruff check` and `ruff format --check` on both Python files: clean.
  - The code diff matches the round-1 description (`:292-295`, `:320-329`,
    `:404-409`). The test diff adds the three tests round 1 reviewed and the
    edits to the move-pin and skip-installed tests. I found no new change.
- Round-1 minor findings were not re-raised.
- Not done, as instructed: no `claude`, no `superclaude install`, no change to
  `~/.claude`, no `git stash`, and no edits outside this report.

# Explanation (advanced): ccsession retention and repo-name list headings

Source read from origin/master (read-only git), 2026-11-17. Graph token: graph:stale (codegraph index does not cover origin/master).
Files: src/superclaude/skills/ccsession-tag/retention.py, src/superclaude/skills/ccsession-tag/ccsession, src/superclaude/skills/ccsession-tag/install.sh, src/superclaude/cli/install_ccsession.py.

## Key point

ccsession never prunes anything. Claude Code does its own sweep: it deletes a transcript file whose modification time is older than `cleanupPeriodDays` (default 30; retention.py:4-8). ccsession's only retention tools are (a) raising that number to 365 in the user's settings, and (b) warning when the value in force is lower. A named session is a row in a name list (`~/.claude/projects/<key>/topics/*.txt`); its transcript is a separate `.jsonl`. If the transcript is gone, the row shows "(transcript missing)" (ccsession:1603-1604).

## Retention decision tree (retention.py)

`ensure` (retention.py:174-232), in order:
1. Managed settings value exists (managed-settings.json, then managed-settings.d/*.json sorted, last wins; retention.py:89-106). If >= 365: report "no change", ok. Otherwise report it is left alone, not ok (exit 3). Nothing is written either way.
2. User file exists but is invalid JSON or not an object: warn, write nothing, not ok.
3. Key present but not a whole number (booleans rejected, retention.py:75-77): warn, leave unchanged, not ok.
4. Key present and >= 365: no change (a larger user value is never lowered).
5. Otherwise set to 365 and write: backup `settings.json.bak.<UTC stamp>`, temp file in the same folder, `os.replace`, original mode kept, symlink target resolved first (retention.py:154-171).

`check` (retention.py:115-151): the same precedence (managed, else user file, else default 30), returns one warning line only when the value is a whole number below 365; silent otherwise. `main` always exits 0 for check, 0 or 3 for ensure, and catches OSError (retention.py:235-255).

Managed folder: /etc/claude-code on Linux, /Library/Application Support/ClaudeCode on macOS, overridable by CCSESSION_MANAGED_SETTINGS_DIR (retention.py:62-68). Never written.

## Callers

- install.sh runs `retention.py ensure "$SETTINGS"` and ignores the status (install.sh:175-179).
- superclaude install: `wire_ccsession()` runs it with sys.executable; exit 3 with output becomes a warning in the install result (install_ccsession.py:105-125, 148-150). It skips a symlinked retention.py.
- `ccsession --list` and `--here` call `retention_warning`, which runs `retention.py check` and prints the line to stderr (ccsession:1665-1675, 1881-1895).

## Repo-name heading

- `origin_id` (ccsession:179-217 region, read at 15-53 of the excerpt): reads `remote.origin.url`, strips query and fragment, handles `scheme://` and scp forms, drops user, port, trailing slashes and `.git`, lowercases the host, collapses `//`, rejects anything outside `[A-Za-z0-9._/~+-]` or with `.` or `..` segments, and fails for file:// or no origin. Output is `host/path`.
- `repo_name` = last segment of that path (ccsession:219-227). Not derived from the list key, because the key replaces `/` with `-` and cannot be split back.
- `name_key` slugifies the same id, so key and heading cannot disagree (ccsession:229-246).
- `note_repo` writes `<list>/.repo` beside `.cwd` only when the name changed and only for origin-keyed lists (ccsession:392-405).
- `list_heading` (ccsession:1337-1366) resolves: live repo of the current folder (when the list is its list), else `.repo`, else `.cwd` folder if it still exists and has the same key, else the old folder-name heading. `--here` appends `(worktree: <name>)`. `--list` never writes files.

## Safety limits

- Never lowers a larger value; never writes under /etc or /Library; never rewrites an invalid or non-numeric settings file; always backs up first; atomic write; never raises (the install and listing continue).
- Does not touch transcript files (touching would corrupt the `last` column, which is the file mtime; PR #570 body).
- Does not read project `.claude/settings*.json`, `--settings`, or MDM/server-managed policy (retention.py:35-37; README), so the warning can be wrong in those cases.

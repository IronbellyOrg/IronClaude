# ccsession head lists and session retention

Source: origin/master, read 2026-11-17. Explain pass: /home/coder/workspaces/IronClaude/.dev/analysis/20261117-new-systems/ccsession-retention-explain.md

## 1. What it is

`ccsession` is the skill that names Claude Code sessions per repo so you can resume them by name. PR #570 (merged 2026-11-16, commit 8c21ac41f, title "head lists with the repo name, keep named sessions for a year") added two things. First, every list from `ccsession --list` or `--here` is now headed by the repo name (for example `IronFlow`) instead of whichever worktree folder wrote the list last. Second, a small script `retention.py` raises Claude Code's own `cleanupPeriodDays` setting to 365, because Claude Code deletes any saved conversation not modified for 30 days (its default) and has no exemption for a named one. Important correction to the usual wording: ccsession itself never prunes or deletes anything. Claude Code does the pruning. ccsession only raises the limit and warns when it is low.

- PR: #570 (one PR; both features).
- Entry points: `ccsession --list`, `ccsession --here [--all]` (heading and warning); `install.sh`, `superclaude install` via `wire_ccsession()` (retention); `python3 retention.py ensure|check [settings.json]`.
- Files (all under src/superclaude/skills/ccsession-tag/ unless noted): `ccsession`, `retention.py`, `install.sh`, `README.md`, `SKILL.md`; `src/superclaude/cli/install_ccsession.py`; tests `tests/unit/test_ccsession_tag.py`, `tests/unit/test_install_ccsession.py`; `CHANGELOG.md`.

## 2. How it works

### Data flow

```text
install.sh / superclaude install ──> retention.py ensure ──> ~/.claude/settings.json (cleanupPeriodDays=365)
ccsession --list / --here ────────> retention.py check ──> one warning line on stderr
Claude Code (its own sweep) ──────> deletes transcript .jsonl older than cleanupPeriodDays
ccsession list rows: name file (topics/*.txt) + transcript .jsonl; missing .jsonl => "(transcript missing)"
```

### How retention decides (it prunes nothing; it decides what limit to set)

Source: `retention.py` (read in full).
- Claude Code's rule: delete a transcript whose file modification time is older than `cleanupPeriodDays` days, default 30 (retention.py:4-8).
- Which value is in force: managed settings (`/etc/claude-code/managed-settings.json`, then `managed-settings.d/*.json` alphabetical, last wins; macOS `/Library/Application Support/ClaudeCode`) beat `~/.claude/settings.json` (retention.py:10-16, 89-106). The folder can be replaced by `CCSESSION_MANAGED_SETTINGS_DIR` (62-68).
- `ensure` (174-232), in order: managed value present and >= 365 gives "no change", ok; managed value present and lower gives "left alone", not ok (exit 3); user file not valid JSON or not an object gives a warning, not ok; key present but not a whole number (booleans rejected, 75-77) gives a warning, not ok; key present and >= 365 gives no change; otherwise write 365.
- `check` (115-151): same precedence, falls back to 30 when unset, returns a line only when the value is a whole number below 365.
- Constants: `MIN_DAYS = 365`, `DEFAULT_DAYS = 30`, `EXIT_NOT_RAISED = 3` (54-59).

### What can never be deleted or changed (safety limits)

- A larger user value is never lowered (219-224).
- Nothing is ever written under the managed folder, and nothing is written when a managed value exists (181-195).
- An invalid or non-object settings file, or a non-numeric value, is left untouched (197-218).
- Before any write: copy to `settings.json.bak.<UTC stamp>`, write via temp file and `os.replace`, keep file mode (0600 for a new file), resolve a symlinked settings file so the link stays (154-171).
- `check` always exits 0; `ensure` exits 0 or 3; OSError is caught (235-255). `install.sh` ignores the status (install.sh:175-179), so retention can never stop an install or a listing.
- ccsession never touches transcript files. Touching them would corrupt the `last` column, which is the file mtime (PR #570 body; UNVERIFIED beyond the PR text, though the listing reads the file mtime for `last`, ccsession:1520-1560 region).
- Transcripts are removed only by Claude Code. The only ccsession delete is `ccsession --rm <name>`, which clears a stale name (README troubleshooting row, README:813), not a conversation.
- Not read: project `.claude/settings*.json`, `--settings`, MDM or server-managed policy (retention.py:35-37), so the warning can miss them.

### Callers

- `install.sh:175-179` runs `ensure`, prints indented output.
- `install_ccsession.py:105-125` runs `ensure` with `sys.executable`, skips a symlinked `retention.py`, and turns exit 3 plus output into a warning in the install message (148-150). Tests: `test_wire_*retention*` in tests/unit/test_install_ccsession.py (lines 332-405 by name grep).
- `ccsession` `retention_warning` (1665-1675) is called after `--list` (1884) and `--here` (1894); output goes to stderr so rows on stdout are unchanged.

### How the repo name is derived

- `origin_id` (ccsession, about line 179): reads `git config remote.origin.url`; strips `?` and `#` parts; parses `scheme://host/path` or scp form `[user@]host:path`; drops user, port, trailing `/` and `.git`; lowercases the host; collapses `//`; fails (no repo name) for `file://`, no origin, characters outside `A-Za-z0-9._/~+-`, or `.`/`..` segments. Output is `host/path`.
- `repo_name` (219-227): last segment after the final `/`. It is deliberately not split from the list key, because the key turns `/` into `-` and `my-org/my-repo` and `my/org/my/repo` collide.
- `name_key` slugifies the same `origin_id`, so key and heading cannot disagree (229-246). Without an origin the key falls back to the git common dir, else the current folder.
- `note_repo` (392-405) writes `<list>/.repo` beside `.cwd` only when the name changed and only for origin-keyed lists; called when a name is saved (495) and when a named session starts (2023).
- `list_heading` (1337-1366) picks the heading in order: live repo of the current folder when the list is its list; the list's `.repo` file; the `.cwd` folder if it still exists and is the same repo; else the old folder-name heading. `--here` appends `(worktree: <basename>)`. `--list` never writes any file.

### Other ccsession behaviours (only where they touch listing or retention)

`CCSESSION_PERMISSIONS=default` (ccsession:99-139) only changes how Claude is started; no effect on retention or listing. `ccsession-orca` reuses `--ask` and the same lists; `ccsession-models.json` is model-tier data. None of them is read by retention.py (UNVERIFIED for ccsession-orca internals beyond grep hits).

## 3. Where it could be integrated in future

- Any tool that depends on Claude Code's local history (`~/.claude/projects/*/*.jsonl`): resume pickers, crash recovery, audit and cost reports. Why: they silently lose data on the 30-day sweep, and the settings precedence logic here is reusable.
- Any installer that edits a user's JSON settings under a possible managed policy. Why: `retention.py` is a small, tested pattern (managed wins, never lower, backup, atomic, exit 3 for "could not apply").
- Health checks (`superclaude doctor`, session-start hooks) that should report an effective setting and who set it.
- Anything that needs a human-readable repo identity from a git remote (dashboards, worktree lists, Orca views). Why: `origin_id` handles https, ssh, scp forms and rejects unsafe text.
- Coder workspace images: the image ships its own managed `cleanupPeriodDays` (90 per the PR); the PR leaves that value to the owner.

## 4. Integration guide

1. Reuse by calling, not copying: `python3 ~/.claude/skills/ccsession-tag/retention.py check` prints one line or nothing; `ensure [settings.json]` sets 365 and exits 0 or 3. Both are plain-text CLIs. Pass an explicit settings path in tests.
2. From Python, run the script the way `install_ccsession.py:108-121` does: `subprocess.run([sys.executable, path, "check"], capture_output=True, text=True, stdin=DEVNULL, timeout=30)`, and treat exit 3 as "report, do not fail".
3. The heading logic (`origin_id`, `repo_name`, `list_heading`) is shell inside `ccsession`, not a library. A second consumer should call `ccsession --list` or add a small `ccsession --repo-name` option rather than duplicate the URL parser.
4. Set `CCSESSION_MANAGED_SETTINGS_DIR` in every test so a developer machine's real managed file cannot leak in (as #570's tests do).
5. Pitfalls: a managed value always wins, so a green installer run does not prove sessions are kept (the printed line says why); `ensure` is skipped if `retention.py` is a symlink; the warning ignores project settings, `--settings` and MDM policy; the 365 days run from file mtime, so a resumed session is renewed.
6. Tests to add for a new consumer: managed value higher, equal, lower; invalid JSON; boolean and string values; larger user value kept; one backup per change; stdout unchanged when only stderr warns (model on tests/unit/test_ccsession_tag.py tests at lines 4984-5159, found by name grep).

## 5. IronClaude fit

Honest summary: the fit is modest. The best use is making existing health checks aware of retention. Ranked by value:

1. `superclaude doctor` retention check. Target: `src/superclaude/cli/doctor.py` (called from `main.py` `doctor`, main.py:477-500; doctor.py itself not read, UNVERIFIED). Change: add one advisory check that runs `retention.py check` and reports the source. Value: finds short retention on machines where the installer could not fix it (managed policy). Effort: small. Risk: low (read-only; report as advisory so a managed policy outside the user's control does not fail doctor).
2. `sc-crash-recovery` empty-result note. Target: `src/superclaude/skills/sc-crash-recovery/scripts/bootstrap_scan.sh` and `SKILL.md` (they read `~/.claude/projects/<cwd>/*.jsonl`; bootstrap_scan.sh:30-32, 64). Change: when no session logs are found, add the `retention.py check` line as a possible cause. Value: explains an otherwise confusing empty recovery. Effort: small. Risk: low.
3. Reuse the `ensure` pattern (managed wins, never lower, backup, atomic) for any other setting that `superclaude install` writes to `~/.claude/settings.json` (install paths already call `wire_ccsession()`, main.py:208, 388). Value: consistent, safe edits. Effort: medium, and only worthwhile if another setting is needed (none identified). Risk: medium, since settings edits are user-visible.
4. Not recommended: moving retention into hooks under `src/superclaude/hooks/`; `ccsession --list` already warns where the user looks and the install-time fix suffices. No other good fit found among commands, skills and agents.

## 6. Limits, open questions, UNVERIFIED items

- UNVERIFIED: Claude Code's own sweep rules (mtime based, once per 24 h, no per-name exemption) come from the PR #570 body (checked by its author against build 2.1.325), not from code in this repo.
- UNVERIFIED: `doctor.py` contents, `ccsession-orca` internals and `ccsession-models.json` use were not read in depth; the greps show no effect on retention or headings.
- Tests were counted by name grep on origin/master; none were run here.
- Open question: the Coder image's managed value (90 per the PR) is below 365, so on Coder workspaces `ccsession --list` will warn and the installer cannot fix it. The PR says that image decision belongs to the owner.
- 365 days is still a limit; sessions untouched for a year are deleted by Claude Code.
- The heading shows only the repo name, not the owner, so two repos with the same name under different owners share a heading while keeping separate lists (inferred from `repo_name`, ccsession:219-227).
- Lists with no network origin, old per-folder lists and lists whose folder is gone keep the old folder heading (list_heading, ccsession:1337-1366).

---
Footer: graph:stale (codegraph index does not cover origin/master; read with git show).

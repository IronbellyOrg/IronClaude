# Controlled create runs for issue 834: how to run them

This kit was prepared by the session that implemented the plan, and nothing in it has been run. That session is a launched session: its guard refuses the whole-tool installer, a child agent session, a Skill call to the issue protocol and any Bash text that names the GitHub tool with `issue` or `api`. It started no child session, ran no installer and ran no create flow. The plan therefore stays **partial** until a person has run the 30 rows of `matrix.md` and filled them in. The static tests in `tests/` prove the instruction text only; they do not prove agent behavior.

Run everything below in your own terminal, in your own session. Give the agent your gateway credentials through your own environment, as you always do. Never copy a key or token into the temporary home, into this kit, or into any file of this package (NFR12).

## 1. Make the project mirrors fresh

Agents are read from the project mirror before the home copy. From the repository root of this branch run `make sync-dev` (or confirm no project mirror exists), so that the mirror holds the changed agents and skill.

## 2. Make a temporary home and install into it

Use the per-component installers below, which take a target path, and never `superclaude install`: that command also runs the hooks, ccsession, user-setup and codegraph phases (`src/superclaude/cli/main.py:211-255`).

- `install_all_skills(target_path=<KIT_HOME>/.claude/skills, force=True)` in `src/superclaude/cli/install_skills.py`
- `install_agents(target_path=<KIT_HOME>/.claude/agents, force=True)` in `src/superclaude/cli/install_agents.py`
- `install_commands(target_path=<KIT_HOME>/.claude/commands/sc, force=True)` in `src/superclaude/cli/install_commands.py`

`<KIT_HOME>` is a new folder from `mktemp -d`. Call each function from `uv run python` in the repository root, and read the returned message; each one prints the folder it wrote.

## 3. Put the shim first on PATH

The create flow calls a program named `gh`. Make a folder `<KIT_HOME>/bin`, link or copy `gh-shim.sh` into it under the name `gh`, make it executable, and put `<KIT_HOME>/bin` first on `PATH`. Before every row run `command -v gh` and `gh --version`: the first must print the shim path and the second must print `gh-shim (not the real GitHub CLI)`. If it does not, stop; the real tool would be reached.

The shim never runs the real tool and never opens a connection. It needs these variables, set again for every row:

- `SHIM_ROW_ID`: the row id, for example `S03-standard`
- `SHIM_ROW_NUMBER`: the row number n from `matrix.md` (1 to 30); the fake issue number is 900000+n, above any real issue number of this repository
- `SHIM_LOG_DIR`: the absolute path of `rows/<row id>` inside this kit (the shim creates it); the row's log file is `rows/<row id>/gh-calls.log`
- `SHIM_FIXTURES`: the absolute path of the `fixtures` folder of this kit
- `SHIM_REPO`: the `owner/repo` that the scratch directory's origin names (use `IronbellyOrg/IronClaude`)
- `SHIM_ISSUE_TYPE` (optional): the issue type the shim echoes when the flow reads the type back; it prints `Feature` when unset. It only echoes this variable and does not check what was created; to see what was filed, read the `CREATE` line of the row's log.

The shim answers only the calls the create flow makes and logs each as one line: `OK-AUTH`, `LOOKUP-LABELS`, `LOOKUP-TYPES`, `LOOKUP-FIELDS`, `LOOKUP-DUPES`, `CREATE`, `VIEW-TYPE`, `COMMENT`, `FIELD-POST`, `FIELD-READ`. Everything else, and any call about an issue number other than this row's fake number, is logged as `REFUSED` and exits non-zero. The fixtures follow the shape the skill text describes; if a lookup worker reports it cannot read one, adjust that fixture to the real API answer and say so in the row.

## 4. Use a fresh scratch directory for every row

The create flow reads `<R>` from the working directory's `origin` remote and stops with `E-NO-ORIGIN` without one. It also renames its draft folder to `.dev/issues/<N>/` and writes files there. So for each row make a new per-row scratch directory outside this repository checkout, run `git init` in it, and add a local `origin` that names the fork (`git remote add origin https://github.com/IronbellyOrg/IronClaude.git`; nothing is ever fetched or pushed). Then copy the repository source the scenario names into the scratch directory, so the drafter has real files to check the description against: for S03, S06, S07 and S08 copy this checkout's `src/superclaude/cli/` folder to the same path in the scratch directory; for S01 create a `README.md` whose line 3 reads `We recieve the data.` (never copy this checkout's real `README.md`, which has no such typo, so the description's claim stays true); for S10 create `src/cache.py` holding the single line `CACHE_TTL_SECONDS = 3600`, so the cache really has a time limit that the description denies. The scratch directory must not contain `src/superclaude/cli/ledger_utils.py` or a `parse_ledger_line` function (this checkout has neither): S06 relies on that file being absent from the real source, not from an empty directory. Never run a row inside a real checkout, and never reuse a scratch directory.

## 5. Start the agent on the temporary home and run the row

Start your own Claude Code session in the scratch directory with `CLAUDE_CONFIG_DIR=<KIT_HOME>/.claude`, the shim first on `PATH` and the five `SHIM_` variables set. The executor of the plan starts no child session; you do. Type `/sc:issue --create "<description>" --depth <depth>` plus the flags of the scenario recipe below. When the one question appears, give the answer the matrix row names (`keep my wording`). Ask nothing else and answer nothing else.

## 6. Scenario recipes (suggestions)

A recipe is a description meant to provoke the scenario. A row counts only when the drafter's own `draft-notes.md` (saved as `.dev/issues/<N>/draft-notes.md` in the scratch directory; copy it into the row folder) holds the list content the scenario expects. If it does not, mark the row `scenario-not-reproduced`, not pass, and retry with a stronger description up to three times.

- S01: `"Fix the typo 'recieve' to 'receive' in README.md line 3."` with `--mode bug --type docs`.
- S02: `"Add a --verbose flag to the sample CLI. Assume the entry point is src/cli.py and keep output on stderr."` with `--mode feature --type cli`; expect `Assumption:` lines under New material.
- S03: `"Keep the existing JSON cache in src/superclaude/cli/ and do not introduce SQLite. Add a cache-expiry option."` with `--mode feature --type cli`; the contradiction is the draft choosing SQLite.
- S04: `"Add a retry option to the sample CLI. It must log every retry to stderr."`; the contradiction is the draft dropping the logging requirement.
- S05: a description that reads as a crash report, passed with `--mode feature`; the contradiction is the drafted issue being filed as a bug.
- S06: `"parse_ledger_line in src/superclaude/cli/ledger_utils.py already validates tabs; extend it to spaces."` (no such function exists); the contradiction is the user's stated fact being false.
- S07: S03 and S06 together in one description.
- S08: S02 and S06 together in one description.
- S09: all flags given, with a mode and type the worker will dispute (for example `--mode bug --type docs` on a feature request); at quick depth the flags are taken at face value, so no comment is expected there.
- S10: `"The cache in src/cache.py never expires; add a refresh flag."`; the draft adds a code fact that the cache has a time limit (an addition that is the only evidence of the contradiction).

Run each scenario at all three depths with the same description.

## 7. Reading a row

After the run, read `rows/<row id>/gh-calls.log`. A row passes only when all of these hold:

- the log has zero `REFUSED` lines;
- it has exactly one `CREATE` line and exactly one `FIELD-POST` line;
- the number of `COMMENT` lines equals the "Calls expected" column (a comment only for S09 at standard and deep depth);
- the number of questions you saw equals the "Expected questions" column, and the answer you gave is the one the row names;
- for S09 only: the `CREATE` line's arguments carry `--label` with the label of the mode you passed with `--mode` (not the mode the drafter preferred) and `--type` with the issue type your `--type` maps to; those arguments are the only evidence of what was filed. The `VIEW-TYPE` line proves nothing, because the shim answers it from `SHIM_ISSUE_TYPE` whatever was created; it is set only so the read-back does not print a "not set" line. The row folder's `field-values.posted.json` holds the Complexity value that was posted. A row where the `CREATE` line's label or type differs from the flags you gave fails, even with zero questions;
- every addition listed in the copied `draft-notes.md` is present in `rows/<row id>/issue-body.posted.md`, and the final output has one `kept without approval: <item>` line for each;
- the agent never offered the full issue body for approval.

Fill the observed columns of `matrix.md` from these facts and replace the Result with `pass`, `fail: <reason>` or `scenario-not-reproduced`. At deep depth the first worker may fall back to the tier 2 worker; write the worker that really drafted the body (the fallback line is in `draft-notes.md`).

## 8. Report

When all 30 rows are filled, the plan is fully verified. Until then the plan is reported partial, and the pull request body lists the unfilled rows as a follow-up.

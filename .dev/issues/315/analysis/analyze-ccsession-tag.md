# /sc:analyze src/superclaude/skills/ccsession-tag --focus architecture --depth deep (issue #315)

- Target: `src/superclaude/skills/ccsession-tag/{ccsession,ccsession-orca,hooks/session-name.sh,hooks/session-start.sh,README.md,SKILL.md,install.sh}`, `src/superclaude/cli/install_ccsession.py`, `tests/unit/test_ccsession_tag.py`, `tests/unit/test_ccsession_tiers.py`, `docs/user-guide/session-management.md`
- Checked at: `origin/master` 38eb3c58 (2026-11-05)
- Method: static reading with Read, Grep and git. Codegraph and auggie were not used: these files are bash scripts and Markdown, so Grep and Read were enough. No code was run.

## 1. How a launch reaches the naming question today

| Entry | What runs | Question? | Evidence |
|---|---|---|---|
| `ccsession <name>` / `ccsession --name <name>` | Resumes the saved session with that name, or starts a new one with it | Never | `ccsession:1649-1714` |
| `ccsession` with options only, or only `--claude-args ...` | Starts untagged | Never | `ccsession:1635-1647` |
| bare `ccsession` | Prints help | Never | `ccsession:1564-1570` |
| `ccsession --ask [<hint>]` | Prints the list and question on stderr and the name on stdout. Exit 1: not asked, timed out or end of input. Exit 130: Ctrl+C | Yes. No time limit unless `CCSESSION_ASK_TIMEOUT` is set | `ccsession:1417-1493`, `:1543-1546` |
| `ccsession-orca [<claude args>]` (Orca's Claude command) | Decides whether to ask, then runs `ccsession [--name N] --shim --claude-args "$@"` | Yes, when stdin and stdout are terminals, `CCSESSION_AUTOSTART` is not 0, there is no `--resume`/`-r`/`--continue`/`-c`, and the #355 reopen did not fire | `ccsession-orca:48-117` |
| Coder New Terminal hook | Not in this repo. The `--ask` default hint "Enter = untagged, Ctrl+C = plain shell" matches it | Yes, with no limit by default | `ccsession:1419-1421` |

Rules inside the question (`ask_session_name`):

- Keys already waiting: the question is not asked (exit 1). `ccsession:1423-1437` turns line mode off and checks with `select` in python3.
- Enter: empty name, which means untagged.
- `*`: lists every worktree's sessions and asks again.
- An invalid name asks again (`validate_label`, `ccsession:275-302`).
- The timeout comes from `read -t` (`ccsession:1471-1483`).
- `ccsession-orca` sets a 30 s default (`ccsession-orca:99`). It sets a no-op `INT` trap so Ctrl+C leads to an untagged start (`ccsession-orca:105-109`).

Order inside `ccsession-orca`:

1. Work out `ask`.
2. The #355 reopen: it runs only when `ask=1`, `ORCA_PANE_KEY` is set and only option arguments were passed. It calls `ccsession --orca-tab-reopen`, then execs `--name` or `--resume <id>`.
3. The question.
4. Exec.

## 2. Gaps between today's code and the approved plan (IronClaude part)

| # | Severity | Finding | Where |
|---|---|---|---|
| G1 | High | A prompt-bearing launch on a terminal still waits up to 30 s at the question. The plan wants no question when a task, name or resume is given. Today `ask` ignores positional arguments. The reopen step's `plain` loop already tells positional arguments apart from options, so the same check can decide `ask`. | `ccsession-orca:48-63` vs `:71-80` |
| G2 | High | No auto-name exists. Timeout, Enter, Ctrl+C, keys typed ahead and no-terminal launches all start untagged. Untagged sessions never enter the list, because the hooks record only names a person gave (`hooks/session-name.sh:15-16`). | `ccsession-orca:112-117`; `ccsession:1640` |
| G3 | High | An auto-name must not collide with a saved name: `ccsession <name>` resumes a saved session of that name (`ccsession:1681-1706`). `sync_name` adds `-2`, `-3` suffixes only for names reported by hooks (`ccsession:328-338`), not at launch. The auto-name has to be checked against the topics directory, or made unique (for example worktree plus short task plus time), before it is passed as `--name`. It must also pass `validate_label`: no control characters, at most 245 bytes as a file name. Long or multi-line tasks must be cut down and cleaned first. | `ccsession:275-302`, `:308-313` |
| G4 | Medium | Ctrl+C semantics are reversed on purpose today: "Orca expects Claude to start in this tab, so it never ends up at a dead prompt" (`ccsession-orca:22-24`). Plan step 6 makes Ctrl+C cancel. `ccsession --ask` already exits 130, so `ccsession-orca` needs to stop trapping `INT` and exit 130 instead of exec'ing. What Orca shows after a Claude-tab command exits (tab closes, shell stays, error) is Not known yet. Test it live before release. Tests that pin today's behavior and must change: `test_orca_enter_or_ctrl_c_starts_untagged` (`test_ccsession_tag.py:1512-1520`, ctrl-c case), `test_orca_ctrl_c_while_line_mode_is_off_restores_the_terminal` (`:1536`). | `ccsession-orca:105-109` |
| G5 | Medium | The plan's "bare `claude` typed in a terminal behaves like the Claude button" needs an entry that asks. Bare `ccsession` prints help (`ccsession:1564-1570`). Either Coder's `claude` wrapper calls `ccsession-orca`, or `ccsession` gets a mode that asks when given nothing. That choice sits on the Coder/IronClaude boundary and is not settled in the issue. | `ccsession:1564-1570` |
| G6 | Medium | No-prompt orchestrator paths (`worker-start`, `agent launch` without `--prompt`) still reach the question. Keys typed before it skip it (untagged). A line typed after it appears becomes the name (`ccsession:1481-1490`). The owner's direction (comment 2) is for orchestrators to pass the name and task explicitly, with no input guessing. That needs a documented launch form. Today a Claude `--name` in Orca's arguments marks the launch as not plain for the reopen step (`ccsession-orca:75`), but `ask` does not read it: the question is still asked, and the `--name` goes to Claude through `--claude-args` instead of being ccsession's `--name`. Whether the hooks then list that name (`hooks/session-name.sh:10-12` reads Claude Code's `session_title`) is Not known yet. | `ccsession-orca:54-63`, `:75` |
| G7 | Low | Docs and code disagree: README says `--fork-session` skips the question (`README.md:235-237`), but the skip list is `--resume|--resume=*|-r|--continue|-c` (`ccsession-orca:61`). In practice `--fork-session` comes with `--resume`. The new rule should include it, or README should say it only works together with `--resume`. | `ccsession-orca:61` |
| G8 | Low | The `CCSESSION_ASK_TIMEOUT` default lives only in `ccsession-orca`. Plan step 5 asks for "a 30-second timer on every naming question", so it belongs in `ask_session_name` itself (`ccsession:1471`). With the Coder hook retired, the remaining `--ask` caller is `ccsession-orca`. Some docs pin the current default: README (`:60`, `:276-277`), CHANGELOG `:250`, `docs/testing/v5.0.0/user/D08-ccsession.md:242-248`. | `ccsession:1471` |

## 3. What must keep working (regression guard)

- **#355 tab reopen.** A plain relaunch reopens the tab's recorded session without asking (`ccsession-orca:65-95`, `ccsession:518-593`). Tests: `test_ccsession_tag.py:1706-1950`, `test_ccsession_tiers.py:412`. The new rule must run the reopen check before the auto-name or question. The reopen check must also stay where `ask` was 1 under today's rules, or a relaunched tab would get an auto-named new session instead.
- **The prompt is never read as a label.** Tests: `test_ccsession_tag.py:1643-1652`, prefill `:1654-1661`, names starting with `-` `:2923`, names with spaces `:3137`.
- **Orca worker readiness.** Orca fails a worker whose Claude is not ready within 60 s (`README.md:242-245`). Any new wait (for example a delayed typed-task check) must stay well under that.
- **Inside Claude Code.** `CLAUDECODE` set drops the Orca pane variables (`ccsession:1618-1622`) and blocks reopen (`ccsession:575`).
- **Tab title.** `orca_terminal_title` uses the label (`ccsession:1606-1616`), so auto-named sessions will show the auto-name on the tab.

## 4. Coupling and ownership

- **IronClaude owns** `ccsession`, `ccsession-orca`, the hooks, README and tests. `install.sh:56-60` and `install_ccsession.py:15-16,61-71` only link `ccsession-orca` into `~/.local/bin`. Neither sets Orca's Settings > Agents > Claude > Command; that setting is outside this repo.
- **Outside this repo (Coder):** the New Terminal hook (`templates/VSCode-AIDev02/lib/aidev/ccsession-autostart.sh`, per the plan) and the `/usr/local/bin/claude` wrapper (Coder #358). Neither can be checked here. Orca's Claude Agent Teams launch path is not referenced anywhere in this repo.
- **Branch `origin/clayphi/433-ccsession-orca-resume`:** it is the already-merged source of #355 (squash 8da537e6). It differs from master in ccsession files only in `MODEL-TIERS.md` (from #374). Its files are the same ones the plan edits, so it is a collision risk only if someone rebases on it or merges it. Leave it alone.

## 5. Recommendations (in order)

1. In `ccsession-orca`, compute one value, "launch carries a task, name or resume". Reuse the positional-argument test from the reopen step, and add `--fork-session` and `--session-id`. When it is set, skip the question and auto-name unless a name was given.
2. Add an auto-name helper in `ccsession`, for example `--auto-name [<task>]`, that prints a unique, valid label. Base it on the worktree name, the first words of the task cleaned of control characters and capped well under 245 bytes, and a short time stamp. Check it against the topics directory so it never resumes an unrelated session.
3. Map the outcomes:
   - Timeout and Enter: auto-name. Whether Enter auto-names or stays untagged is Not known yet, because the plan names only the timeout.
   - Ctrl+C: exit 130 with no Claude start.
   - Keys typed ahead and no terminal: auto-name.
4. Move the 30 s default into `ask_session_name`. Update the README, the `--ask` help text (`ccsession:55-61`), the CHANGELOG and the D08 test guide.
5. Settle the explicit orchestrator launch form with the owner: for example, a `CCSESSION_NAME` environment variable read by `ccsession-orca`, or a documented prompt-bearing launch. The owner rejected any guessing about typed lines.
6. Tests: pty tests for each row of the plan's table, the #355 reopen with the new rule, auto-name collisions and validity, and Ctrl+C exiting 130 with no `record.json` written.

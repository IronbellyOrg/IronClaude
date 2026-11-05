# Summary: #315 [Bug]: Agent spawned worktree sessins stuck at CCSession Session Name prompt

- Issue: https://github.com/IronbellyOrg/IronClaude/issues/315
- Type: bug
- Complexity: complex (rubric: `refs/claim.md`)
- Effort estimate: 24 hours

## What the issue asks for

When agents open a terminal or start Claude, they stop at ccsession's session-name question: their typed command is taken as the name, or they wait. The owner approved the plan of 2026-11-03, and only its IronClaude part is in scope here. That part covers `ccsession` and `ccsession-orca`:

- **One question rule.** The naming question and session list appear only when Claude starts with no task, name or resume.
- **Auto-name.** Every launch without a name gets an automatic, unique name: prompt-bearing launches and timed-out questions.
- **Timer.** Every naming question has a 30-second limit that ends in an auto-named start.
- **Ctrl+C.** At the question, Ctrl+C cancels instead of starting an unnamed session.

Retiring Coder's New Terminal hook and the `claude` wrapper handoff are tracked separately in the Coder repo.

Today's state (see `accuracy-check.md`):

- `ccsession-orca` already has a 30 s timer, but it starts an untagged session, and Ctrl+C does the same.
- A prompt-bearing launch on a terminal is still asked.
- No auto-name exists.
- The #355 tab reopen, merged after the plan, must keep working.

## Relevant files and systems (cheatsheet)

| Path or system | Why it matters |
|---|---|
| `src/superclaude/skills/ccsession-tag/ccsession-orca` | Orca's Claude command. It decides whether to ask (`:48-63`), runs the #355 reopen (`:65-95`), then the question with the 30 s default and the Ctrl+C-to-untagged trap (`:97-110`), then execs ccsession (`:112-117`). This is the main edit point. |
| `src/superclaude/skills/ccsession-tag/ccsession` | `ask_session_name` / `--ask` (`:1417-1493`, `:1543-1546`): the typed-ahead skip, `read -t` timer and exit 130 on Ctrl+C. `validate_label` (`:275-302`) limits any auto-name. Launch paths: untagged `:1635-1647`, labeled resume or new `:1649-1714`. Bare `ccsession` prints help (`:1564-1570`). The auto-name helper goes here. |
| `src/superclaude/skills/ccsession-tag/hooks/session-name.sh` | Records only names a person gave (`:15-16`) and the Orca tab's session for reopen. Untagged sessions never appear in the list, which is why auto-naming is needed. |
| `src/superclaude/skills/ccsession-tag/README.md` | Documents Orca launches, the question, the 30 s limit, `CCSESSION_AUTOSTART` and the reopen (`:211-277`). It must be rewritten for the new rule. It also has drift: `--fork-session` alone does not skip the question (`ccsession-orca:61`). |
| `src/superclaude/skills/ccsession-tag/install.sh`, `src/superclaude/cli/install_ccsession.py` | Only link `ccsession-orca` into `~/.local/bin`. The Orca Settings > Agents > Claude > Command option is set outside this repo. |
| `tests/unit/test_ccsession_tag.py` | Orca question tests (`:1485-1703`), relaunch tests (`:1706-1950`), names with a leading `-` (`:2923`) and with spaces (`:3137`). The Ctrl+C test (`:1512-1520`) and timeout test (`:1680-1696`) pin today's untagged behavior and must change. |
| `tests/unit/test_ccsession_tiers.py` | Orca relaunch on the default tier (`:412`). Use it to check for regressions. |
| `docs/user-guide/session-management.md` | Mentions ccsession only on line 122. Probably not affected. |
| `docs/testing/v5.0.0/user/D08-ccsession.md`, `CHANGELOG.md:250` | Pin today's `--ask` and `CCSESSION_AUTOSTART` behavior. Update with the change. |
| Coder repo: New Terminal hook (`templates/VSCode-AIDev02/lib/aidev/ccsession-autostart.sh`) and the `/usr/local/bin/claude` wrapper (Coder #358) | Out of scope and cannot be checked from here. The real "stuck with no timeout" behavior comes from this hook calling `ccsession --ask` with no limit. |
| Orca: `worker-start`, `agent launch` without a prompt, Claude Agent Teams | Still unresolved in the plan. Orca needs a no-guessing way to pass a name or task, and Agent Teams bypasses ccsession. Nothing in this repo covers Agent Teams. |
| Branch `origin/clayphi/433-ccsession-orca-resume` | The already-merged source of #355 (squash 8da537e6). In ccsession files it differs from master only in `MODEL-TIERS.md` (#374). It touches `README.md`, `ccsession`, `ccsession-orca`, `hooks/session-name.sh` and both test files, the same files this work changes. Build on master and never rebase on it or merge it. |

## Analysis

- [analyze-ccsession-tag.md](analysis/analyze-ccsession-tag.md): today's launch-path map, gaps G1-G8 against the approved plan, the regression guard for #355, and recommendations.

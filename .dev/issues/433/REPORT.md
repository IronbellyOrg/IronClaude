# Coder #433: report

Issue: IronbellyOrg/Coder#433. Decisions: `.dev/issues/433/DECISIONS.md`.

## 1. What Orca passes to the Claude command on a relaunch

Live test, deployed Orca build `1.4.237-aidev02.0e4491a95e92` (image tag `aidev02-412:local`, whose `app.asar` hash `4b64f0d5eb0a0743` matches `/opt/Orca` on this machine), container booted and restarted with `orca-port-tools/live-boot.sh` (`KEEP_VOLUMES=1`, same volumes, as a Coder restart), the project then opened in Orca Web with the harness's `reopen` journey (`orca-port-tools/live-web.sh`). Helpers: `.dev/issues/433/live/lib.sh`.

- Before the restart: `orca agent launch --agent claude --surface terminal` (the "+ Claude" path) typed `ccsession-orca '--dangerously-skip-permissions'` into the tab's shell; the name `alpha-433` started session `5a23ebdb`, and one message was answered.
- After the restart, when the project was opened, Orca typed exactly the same line again: process `/bin/bash /home/coder/.local/bin/ccsession-orca --dangerously-skip-permissions`. No `--resume`, no session id, no prompt. ccsession showed the session list and the "Session name" question (the issue's screenshot). Nobody answered, so after 30 seconds an untagged new session (`61bcab9d`) started in the tab.
- Why Orca did not add `--resume` itself: its cold-restore code (`src/renderer/src/components/terminal-pane/pty-connection/cold-restore-resume-startup.ts`, line 33 in v1.4.237, line 41 in aidev02-v1.4.245) resumes only an agent whose last reported state is not `done`, or a hibernated ("sleeping") one. A Claude that has answered and waits for input reports `done` (Orca's `agent-hooks/last-status.json` in the container showed `payload.state done`), and hibernation is off (`experimentalAgentHibernation false`), so Orca falls back to the tab's plain launch command (`launchAgent: "claude"` in the saved tab).
- Restore is lazy: `orca terminal list` shows no terminals after the restart until a client opens the project, which matches "when you click on them in the list on the left".

## 2. Is the tab's identity stable across a restart?

Read from `/proc/<pid>/environ` of the launched process before and after (non-secret variables only):

| Variable | Before restart | After restart | Stable |
|---|---|---|---|
| `ORCA_PANE_KEY` (tab id `:` pane id) | `484f1070-…:54f98029-…` | `484f1070-…:54f98029-…` | yes |
| `ORCA_TAB_ID` | `484f1070-…` | `484f1070-…` | yes |
| `ORCA_AGENT_PANE` | same as pane key | same | yes |
| `ORCA_TERMINAL_HANDLE` | `term_4438689f-…` | `term_e3ab8fbc-…` | no, new per terminal process |
| `ORCA_AGENT_LAUNCH` | `cd273b55-…` | `8e2f36d2-…` | no |
| `ORCA_RUNTIME_SOURCE_INCARNATION` | `4fb4ce74-…` | `84513517-…` | no |

Source agrees: the pane key is set from the saved pane (`src/main/ipc/pty/spawn-pane-env.ts:57` in v1.4.237, `:56` in aidev02-v1.4.245; tab and pane ids are saved in the workspace session), and the terminal handle is allocated for each new terminal process (`src/main/ipc/pty/ipc/spawn-options.ts:18`). A new tab or a split pane gets a new pane key.

## 3. Approach

ccsession alone, no Orca change (DECISIONS.md D1). The ccsession hooks remember, per Orca pane key, which session the Claude Code that ccsession launched runs there, with the launch folder and terminal handle. When Orca relaunches the tab with only its default options, `ccsession-orca` finds that record (same pane, new terminal, same folder, conversation still saved) and resumes the session instead of asking. Exact conditions and safety rules: DECISIONS.md D3 and D4.

## 4. What changed

All under `src/superclaude/skills/ccsession-tag/` plus tests:

- `ccsession`: new fast paths `--orca-tab-session <id>` (write this pane's record; take the id off every other pane; drop records whose conversation is gone; under the existing `lock_list` lock) and `--orca-tab-reopen` (print `<id>\t<name>` for a relaunched tab, else exit 1). Records live in `${XDG_STATE_HOME:-~/.local/state}/ccsession/orca-tabs/`. Each launch exports `CCSESSION_LAUNCH_CWD` (the launch folder) beside `CCSESSION_LAUNCH_ID`. Help text lists both commands.
- `ccsession-orca`: before the question, a plain relaunch (D3) reopens the recorded session by name (`ccsession --name <name>`) or by id (`--resume <id>`), printing `[ccsession] Reopening this tab's session …`.
- `hooks/session-name.sh`: at SessionStart and UserPromptSubmit, for the launched Claude Code only and when `ORCA_PANE_KEY` is set, runs `ccsession --orca-tab-session <id>` in the launch folder.
- `README.md`: new section "Reopening a tab after a restart".
- Tests: `tests/unit/test_ccsession_tag.py` (11 new tests, 18 cases), `tests/unit/test_ccsession_tiers.py` (1 new tier-mode test; `_launch` split into `_launch` and `_launch_env`, behaviour unchanged).

## 5. Tests

- New tests, `test_ccsession_tag.py`: named and untagged reopen; new tab and same-terminal re-run still asked; prompt, `--prefill`, `--name`, `-p`, `--session-id` still asked; `--resume`/`--continue` unchanged; no terminal and `CCSESSION_AUTOSTART=0` unchanged; deleted conversation falls back; two tabs never share a session and dead records are dropped; `/clear` moves the record; only the launched Claude records (not a plain claude, not a nested one); the record uses the launch folder and is refused from another worktree and inside Claude Code. `test_ccsession_tiers.py`: a relaunch in tier mode reopens by name with the default tier's model and window through the shim.
- Regression proof: with the old `ccsession-orca` put back, the 4 reopen tests fail and the 14 guard tests pass; with the new one all 18 pass.
- Full files: `uv run pytest tests/unit/test_ccsession_tag.py tests/unit/test_ccsession_tiers.py tests/unit/test_install_ccsession.py`: 311 passed, 1 failed. The failure, `test_shim_outlives_the_terminal_that_started_it`, fails the same way on the unchanged commit `5e513796` (checked in a separate detached worktree), so it is not from this change; it fails in this sandboxed shell (the shim it starts is gone after the test kills the terminal), and is left for a separate look.
- `make lint` (ruff check): passed. `ruff format --check src/ tests/` (CI's gate): passed. `make sync-dev` then `make verify-sync`: no drift. (`make` is not installed in this workspace; the GNU make 4.3 binary was copied from the local `orca-port-builder-e2e` image into `/tmp`, nothing installed system-wide.)
- Pre-commit hooks on the changed files: shellcheck and ruff-format passed; detect-secrets (test lines 104 and tiers 2230, an existing digest constant) and markdownlint (README lines 79 and 219, existing code fences without a language) report only pre-existing lines this change does not touch; neither hook runs in CI.

## 6. Live proof on this machine

Fresh test container (`aidev02-412:local`, deployed Orca `1.4.237-aidev02.0e4491a95e92`), this branch's skill copied over the installed one, the session-name hook registered for UserPromptSubmit and SessionEnd as on a current install (the image's older install registers only SessionStart). Restarts with `live-boot.sh` (`KEEP_VOLUMES=1`), project reopened with the harness's `reopen` web journey. The owner's own workspace was not restarted or touched; the gateway key lived only in the test container's `/dev/shm` and was removed with the container.

Before the restart: tab 1 named `alpha-433` (session `47bb4fe5`, told to remember PELICAN-433), tab 2 untagged (session `7ef70b1b`, told OTTER-433). The hooks wrote one record per pane.

Restart 1, project opened:

- Tab 1: no question; `[ccsession] Reopening this tab's session 'alpha-433'`, Claude ran `--name alpha-433 --resume 47bb4fe5-… --dangerously-skip-permissions`; asked "What word did I ask you to remember?" it answered `PELICAN-433`. Screenshot: `.dev/issues/433/live/evidence/restart1-reopened-project.png`.
- Tab 2: no question; `[ccsession] Reopening this tab's session 7ef70b1b`, Claude ran `--dangerously-skip-permissions --resume 7ef70b1b-…`; it answered `OTTER-433`.
- Unchanged paths in the same restarted workspace: a new "+ Claude" tab listed `alpha-433` and asked the name question; a launch with `--prompt` asked the question as before; `ccsession-orca --dangerously-skip-permissions --resume 7ef70b1b-…` in a new terminal started without the question and passed `--resume` through unchanged, and that session's record moved to the new pane (tab 2 lost it); after `/exit` in tab 1, typing `ccsession-orca --dangerously-skip-permissions` by hand in the same terminal asked the question.

Restart 2, project opened: tab 1 again reopened `alpha-433` (`--resume 47bb4fe5-…`); tab 2, whose session had moved, showed the question and, unanswered, started untagged after 30 s exactly as today. Screenshot: `restart2-reopened-project.png`.

Baseline on the unchanged code (same image, before the fix): the relaunched tab showed the question and started a new untagged session after 30 s (section 1).

Helpers: `.dev/issues/433/live/lib.sh` (boots and restarts through `orca-port-tools/live-boot.sh`, reopens through `live-web.sh`; neither harness script was changed).

## 7. Pull request

https://github.com/IronbellyOrg/IronClaude/pull/355 (base `master`, opened with `/sc:pr-submit --monitor 3`, refs IronbellyOrg/Coder#433; not merged).

- Review round 1 on `ffa58aa5`: Augment raised one Low finding (this folder's DECISIONS.md said a pane key's `:` is written as `_`, the code writes `+`); Codex found no issues. Low findings are report-only in the monitor, but the handoff asks for every comment to be addressed, so it was fixed in `04222c3e` (DECISIONS.md corrected, skill README names the file form), replied to and resolved.
- Re-review on `04222c3e`: Augment clean, Codex "Didn't find any major issues", Codex security review clean.
- CI on `04222c3e`: all checks passed (lint/plugin/sync, doctor, swarm lanes, tests on Python 3.10, test summary).
- This section was added afterwards in one more docs-only commit, reviewed the same way.
- Monitor run log (local, gitignored): `.dev/pr-monitor/pr-355-20261103T165553Z/monitor-run-355.jsonl`.

## 8. Open questions

1. **Plain terminal tabs are not covered.** A New Terminal tab (not a "+ Claude" tab) comes back after a restart as a plain shell, and the Coder template's New Terminal hook asks its own question (`Session name (Enter = untagged, Ctrl+C = plain shell)`), seen live on restart 2. That hook lives in the Coder repo. It could call `ccsession --orca-tab-reopen` the same way `ccsession-orca` does; that would be a Coder change, not made here.
2. **Making the agent continue its work** after the session reopens is out of scope (Coder#437, IronClaude#339). The session reopens and waits for input.
3. **A session open in a non-Orca terminal** (for example over `coder ssh`) is not recorded against any tab, so it cannot take a tab's record away. After a workspace restart nothing is still running, so this only matters if Orca relaunches a tab while that other terminal is still open (an Orca-only restart); the tab would then reopen a session that is also open elsewhere, as typing its name would today.
4. **Orca's own resume** skips Claude agents whose last state is `done` (section 1). If Orca later resumes those itself, it will pass `--resume <id>`, which `ccsession-orca` already passes through unchanged; the two do not conflict.
5. **Unrelated test failure** `test_shim_outlives_the_terminal_that_started_it` fails in this workspace on the unchanged commit too (section 5); worth its own look.

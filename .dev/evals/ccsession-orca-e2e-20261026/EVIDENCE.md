# ccsession-orca end-to-end evidence (Orca, 2026-10-26)

Branch `feature/ccsession-orca-launch`. Workspace: Coder `master` (`/home/coder`), Orca v1.4.237 (runtime `dd8c9bb9`), Claude Code v2.1.310.

## Setup

- Installed the branch with `src/superclaude/skills/ccsession-tag/install.sh`: `~/.local/bin/ccsession-orca -> ~/.claude/skills/ccsession-tag/ccsession-orca`. The previously installed skill folder was backed up to `~/.cache/ccsession-e2e-20261026/installed-skill-backup/`.
- Old value of Orca's Claude command (`agentCmdOverrides`): `{}` (no override). Orca's default Claude arguments stayed `--dangerously-skip-permissions`.
- Set Settings > Agents > Claude > Command to `/home/coder/.local/bin/ccsession-orca`. GUI control was not available on this host (`orca computer`: "Linux computer use requires an active desktop session; missing XDG_RUNTIME_DIR"), so the value was set with the same runtime call the Settings field makes (`settings.mutateAgentLaunch {type: "command", agent: "claude", value}`, see Orca `AgentLaunchSettingsCatalog.tsx` `onSaveOverride`), over Orca's local runtime socket. Readback: `agentCmdOverrides = {"claude": "/home/coder/.local/bin/ccsession-orca"}`.
- Launches used `orca agent launch --agent claude` ("starts the agent the way a new agent tab does"; receipt: terminal, the default for new agent tabs) and `orca worktree create --agent claude`. Each launch typed `/home/coder/.local/bin/ccsession-orca '--dangerously-skip-permissions' ...` into the new tab.
- Session details were read from `/proc/<pid>` of the `claude` process: argv, `CLAUDE_TOPIC`, `ANTHROPIC_BASE_URL`, `CCSESSION_PROFILE`, and only whether `ANTHROPIC_API_KEY` / `ANTHROPIC_AUTH_TOKEN` are set. No key or token value was printed.

## Checks

Every Claude session below ran through the shim (`ANTHROPIC_BASE_URL=http://127.0.0.1:4111`), on tier 2 (`CCSESSION_PROFILE=tier2`, `--model claude-gw-tier2[1m]`, screen: "Tier 2: Grok 4.7, Qwen 3.8 Max, GLM 5.3, Muse Spark 1.3, Muse Wonder 1.0"), with `ANTHROPIC_AUTH_TOKEN` set and `ANTHROPIC_API_KEY` unset. Claude's argv always started with ccsession's `--dangerously-skip-permissions --allowedTools=Grep --settings <per-model windows> --model claude-gw-tier2[1m]`, followed by Orca's own arguments unchanged.

| # | Launch | Expected | Result |
|---|---|---|---|
| 1 | Agent tab (+ button path), IronClaude folder | Saved-session list for this folder, then `Session name (Enter or Ctrl+C = untagged):` | PASS: list of 5 saved IronClaude sessions, then the question |
| 2 | Same tab, typed `orca-e2e` | Starts a session labeled `orca-e2e` | PASS: `CLAUDE_TOPIC=orca-e2e`; `ccsession --here` lists `orca-e2e` |
| 3 | Agent tab, pressed Enter | Untagged session | PASS: `CLAUDE_TOPIC` unset, Claude started (pid 54468) |
| 4 | Agent tab, one Ctrl+C byte | Untagged session, tab not dead | PASS: `^C` shown, Claude started untagged (pid 58194) |
| 5 | Agent tab with prompt `Reply with exactly the word READY. It's a "launch" test.`, typed `orca-e2e-prompt` | Prompt reaches Claude unchanged, label kept | PASS: last argv element is the prompt byte for byte; Claude answered `READY`; label `orca-e2e-prompt` recorded with transcript `b4a342b5` |
| 6 | Agent tab, typed the saved name `orca-e2e-prompt` | Resumes that conversation | PASS: argv has ccsession's `--resume b4a342b5-fba3-429d-92e2-64bbcb784537`, earlier prompt and answer on screen |
| 7 | Resume of `b4a342b5` as Orca builds it | No question; Orca's `--resume <id>` passes through | PASS: 0 "Session name" lines in scrollback; argv ends `--resume b4a342b5-...`; conversation shown |
| 8 | Fork-resume of `b4a342b5` as Orca builds it | No question; `--resume <id> --fork-session` passes through | PASS: 0 "Session name" lines; argv ends `--resume b4a342b5-... --fork-session` |
| 9 | `orca worktree create --agent claude` (new worktree `ccsession-orca-e2e`), typed `wt-e2e` | Question in the new folder; label belongs to that folder | PASS: question shown (no saved sessions there, so no list); `CLAUDE_TOPIC=wt-e2e`, cwd is the new worktree, `ccsession --here` there lists `wt-e2e` |

Checks 7 and 8: Orca's UI builds the resume command in the renderer, which this host could not drive (no GUI control, no browser). The commands were produced by Orca's own `buildAgentResumeStartupPlan` (v1.4.237 source, run with `tsx`) from the live settings, giving `/home/coder/.local/bin/ccsession-orca '--dangerously-skip-permissions' '--resume' '<id>'` (plus `'--fork-session'` for the fork), and opened in Orca terminals with `orca terminal create --command`. Orca's builder looks for a `claude` token to splice the selector; for a wrapper it appends the selector to the command unchanged ("fails open by design"), which is what the wrapper expects.

Unit tests (`uv run pytest tests/unit/test_ccsession_tag.py tests/unit/test_install_ccsession.py tests/unit/test_ccsession_tiers.py tests/unit/test_cli_doctor.py tests/unit/test_cli_install.py tests/cli/test_install_hooks.py`): 303 passed.

## 60-second timing check

Launch 1 started at 15:23:19 UTC. The question was left unanswered until 15:24:41 UTC (82 seconds). At that point `orca terminal show` reported `connected: true`, `writable: true`, `agentWait: none`; the screen still ended at the unanswered question, with nothing typed into it; the tab was still open. Orca did not mark the launch failed, close the tab, or type into it. The name was then entered and Claude started normally (check 2). No time limit was observed for a person's launch tab.

## Round 2: supervised workers, and re-check after the review fixes

An independent review found that Orca's supervised workers might block at the question. Checked with the round 1 code: `orca orchestration worker-start --agent claude` (run `run_3eaccd9871de`, created for this probe) launched through the same Claude command, sat at the unanswered question, and Orca never typed into it; worker-start failed after the 45-second limit given (`state: failed, stage: agent_readiness, lastError: timeout`). Orca's default worker readiness limit is 60 seconds (`ORCHESTRATION_READINESS_TIMEOUT_MS`). So with the setting on, every supervised Claude worker would fail.

Fixes in round 2: the wrapper's question falls back to untagged after `CCSESSION_ASK_TIMEOUT` seconds (default 30, shown in the question), names starting with `-` are rejected and asked again, the waiting-keys probe works on bash 3.2, the wrapper passes Orca's arguments after a dedicated `--claude-args` marker (a plain `--` keeps its old meaning), installer and doctor handle the new file. The branch was reinstalled and these were re-run in Orca (override set again, then restored):

| # | Launch | Expected | Result |
|---|---|---|---|
| 10 | `orca orchestration worker-start --agent claude`, default 60s limit, question left unanswered | Worker starts untagged after 30s and gets its task | PASS: worker-start returned after 34s, `state: ready, stage: input_accepted`; the worker replied `WORKER-OK`; its Claude ran through the shim on tier 2, untagged, auth token set and API key unset; worker then released |
| 11 | Agent tab with prompt `Reply with exactly the word READY2.`, typed `orca-e2e2` | New question text; label and prompt kept | PASS: question `Session name (Enter or Ctrl+C = untagged; untagged after 30s):`; `CLAUDE_TOPIC=orca-e2e2`; prompt is the last argv element, unchanged |
| 12 | Resume of that conversation with the command Orca's builder produces | No question; resume passes through | PASS: 0 "Session name" lines; argv ends `--resume ed09e7c8-...`; earlier prompt on screen |

Unit tests after the fixes: 310 passed (`tests/unit/test_ccsession_tag.py`, `test_install_ccsession.py`, `test_ccsession_tiers.py`, `test_cli_doctor.py`, `test_cli_install.py`, `tests/cli/test_install_hooks.py`). The full suite earlier: 14149 passed; its 5 failures were "No module named ruff" in this fresh worktree's venv and pass once the pinned ruff is installed.

## Known behaviour and limits

- A second Ctrl+C pressed while ccsession is starting (after the question was already answered by the first one) stops ccsession and leaves a shell prompt in the tab. Seen once: `orca terminal send --interrupt --text $'\x03'` sent two Ctrl+C bytes. A Ctrl+C during startup stops bare `claude` the same way; a single Ctrl+C at the question always starts Claude (check 4).
- The workspace's inherited `ANTHROPIC_MODEL=gpt-6.1-sol` is still in the session's environment. ccsession's `--model claude-gw-tier2[1m]` overrides it and the session runs on tier 2. This matches New Terminal ccsession sessions today and is not changed by this PR.
- Orca's own `--dangerously-skip-permissions` default argument arrives in addition to ccsession's; Claude Code accepts the repeat.
- A person who takes longer than 30 seconds to answer gets an untagged session (they can still name it with `/ccsession-tag <name>`). Raising `CCSESSION_ASK_TIMEOUT` above about 45 seconds would make supervised workers fail again.

## Cleanup

- Closed every test tab; removed the test worktree with `orca worktree rm` (Orca also deleted its branch `clayphi/ccsession-orca-e2e`, which had no commits of its own).
- Removed the test labels `orca-e2e`, `orca-e2e-prompt`, `wt-e2e` and `orca-e2e2` (label pointers only; transcripts kept).
- The probe run `run_3eaccd9871de` (two probe tasks: the failed round 1 worker, stopped; the round 2 worker, completed and released) stays in Orca's orchestration history. It was not deleted because `orca orchestration reset` would clear every run, not just this one.
- Restored Orca's Claude command with the same call and an empty value. Readback: `agentCmdOverrides = {}`, the original value.
- The branch's ccsession stays installed in `~/.claude/skills/ccsession-tag` (backward compatible; the next `superclaude install` or `./update.sh` replaces it). The pre-test copy is in `~/.cache/ccsession-e2e-20261026/installed-skill-backup/`.

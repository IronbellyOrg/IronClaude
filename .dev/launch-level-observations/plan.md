# Plan: launch-level observations that hold the issue watcher's ship gate closed

- Status: complete draft for owner review (2026-11-24); no observation has been run, no /sc: command run, nothing staged or committed
- Author: worker task_fea8688b3c85 (planning only; nothing in this plan has been run)
- Worktree: /home/coder/workspaces/worktrees/IronClaude/obs-plan (branch ironbelly/obs-plan)
- Repository for every GitHub action: IronbellyOrg/IronClaude only. The upstream SuperClaude-Org is never touched.
- Sources read: docs/designs/sc-issue-launch-level-hook.md (sections 1, 3, 4, 6, 7, 11, 13, 14, 16, 19.1, 19.5, 19.8), tests/hooks/test_launch_level_observations.py, tests/hooks/fixtures/launch_level/ob_h1/ (README, probe, 9 fixtures), tests/hooks/fixtures/launch_level/live_probe.py, src/superclaude/cli/issue_watch/launch.py:48, src/superclaude/skills/sc-issue-protocol/refs/claim.md:136, src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py (cmd_launch).

## 1. Summary
Four items keep the gate closed: OB-H1 item 1, OB-H1 item 5, OB-H2, OB-H3 (`_GATE_ITEMS`, tests/hooks/test_launch_level_observations.py:82). All four need a real Claude Code session with a hook registered, so none can be finished with LOCAL steps alone (section 7). Order follows design section 14: OB-H1, then OB-H2, then OB-H3.

| Step | Section | Class | Model sessions | GitHub writes | Un-skips |
|---|---|---|---|---|---|
| OB-H1 setup (temp dir, probe, settings) | 2 | LOCAL | 0 | none | none |
| OB-H1 item 1 | 4.1 | OUTWARD (paid session only) | 1 | none | `[OB-H1 item 1]` |
| OB-H1 item 5 | 4.2 | OUTWARD (paid session only) | 1 | none | `[OB-H1 item 5]` |
| OB-H1 items 2, 3, 4, 6, 7, 8, 9 | 4.3 | optional; ride in the 4.1/4.2 sessions | 0 extra | none | `[OB-H1 item N]` each |
| OB-H2 probe script | 5.1 | LOCAL to write; OUTWARD to register (edits ~/.claude/settings.json) | 0 | none | none |
| OB-H2 rehearsal | 5.2 | OUTWARD (paid session only) | 2 | none | none (not evidence) |
| OB-H2 IR-4 refusals | 5.4 | LOCAL candidate (UNVERIFIED) | 0 | none | part of `[OB-H2]` |
| OB-H2 real claim, level worktree | 5.3 | OUTWARD | 2 (claim + agent) | 1 issue, assignee, ClickUp | `[OB-H2]` |
| OB-H3 W (same claim as 5.3) | 6.2 | OUTWARD | 1 to 2 more turns | none beyond 5.3 | part of `[OB-H3]` |
| OB-H3 F | 6.3 | OUTWARD | 2 | 1 issue, assignee, ClickUp | part of `[OB-H3]` |
| OB-H3 FS | 6.4 | OUTWARD | 3 to 6 plus 2 reviewer services | 1 issue, 1 branch, 1 PR, 1 base branch | `[OB-H3]` |

Totals (estimates; the design gives no cost figure): about 12 to 18 model sessions, 3 test issues, 1 PR, 2 branches on IronbellyOrg/IronClaude, 1 edit of the owner's ~/.claude/settings.json.
Optional items 2, 3, 4, 6, 7, 8, 9: none is needed before the gate may open (section 4.3).

## 2. Conventions: LOCAL and OUTWARD, probe logs, common setup
**Classes.**
- LOCAL: no GitHub write, no push, no paid model run beyond the session that is already running, no change outside a disposable temp directory or this worktree.
- OUTWARD: creates or edits a GitHub issue or PR, pushes, opens a PR, starts a paid session, or touches a shared repo or shared config. Starting a new `claude` session counts as OUTWARD even when it writes nothing to GitHub; such steps are marked "OUTWARD (paid session only, no GitHub write)".

**Facts that shape every step** (read from disk on 2026-11-24):
- A `claude` process cannot be started from inside another Claude Code session: `live_probe.py:280-281,321-324` records "cannot be launched inside another Claude Code session". Every session below is started by a person from a plain terminal (or an Orca terminal), never from this session.
- `log-only-probe.sh` (tests/hooks/fixtures/launch_level/ob_h1/log-only-probe.sh) appends each hook input as one JSON line to the file named by `LAUNCH_LEVEL_PROBE_LOG`, exits 0, and prints nothing. It records no timestamp, no HOME, no store state and no guard verdict. `live_probe.py` records only `Bash` or `other` as the tool name and runs one Bash call (README of ob_h1), so it cannot observe any step below. Gap for OB-H2 and OB-H3: see 5.1 and 6.1.
- The installed guard and pre-push hook already exist on this machine: /home/coder/.claude/hooks/launch-level-guard.sh and /home/coder/.claude/hooks/launch-level-pre-push.sh. `claude` is /usr/local/bin/claude, version 2.1.331. `jq` is /usr/bin/jq.
- No governed claim exists yet: `launch.py:48` is `GOVERNED_LEVELS_ALLOWED = False`.

**Probe-log location.** Raw logs stay outside the repo while they are written: `/tmp/ll-obs.<random>/logs/<step>.jsonl` (created with `umask 077`). When a step passes, the owner-reviewed excerpt is copied to `/home/coder/workspaces/worktrees/IronClaude/obs-plan/.dev/launch-level-observations/evidence/<step>.jsonl`. Raw logs hold full prompts and tool inputs, so they are read before they are copied (they can contain paths or text typed by mistake). Evidence is the input of the un-skipped tests (section 8).

**Common setup for OB-H1 (LOCAL preparation, same for items 1 and 5).**
```bash
umask 077
OBS=$(mktemp -d /tmp/ll-obs.XXXXXXXX); mkdir -p "$OBS/logs" "$OBS/work"
git init "$OBS/work"
cp /home/coder/workspaces/worktrees/IronClaude/obs-plan/tests/hooks/fixtures/launch_level/ob_h1/log-only-probe.sh "$OBS/probe.sh"
chmod 700 "$OBS/probe.sh"
cat > "$OBS/settings.json" <<EOF
{"hooks":{
 "PreToolUse":[{"matcher":".*","hooks":[{"type":"command","command":"LAUNCH_LEVEL_PROBE_LOG=$OBS/logs/ob-h1.jsonl $OBS/probe.sh","timeout":5}]}],
 "PostToolUse":[{"matcher":".*","hooks":[{"type":"command","command":"LAUNCH_LEVEL_PROBE_LOG=$OBS/logs/ob-h1.jsonl $OBS/probe.sh","timeout":5}]}],
 "UserPromptSubmit":[{"hooks":[{"type":"command","command":"LAUNCH_LEVEL_PROBE_LOG=$OBS/logs/ob-h1.jsonl $OBS/probe.sh","timeout":5}]}]
}}
EOF
echo "$OBS"
```
This creates only files in a new temp directory (LOCAL). The settings file is passed with `--settings`, so no file under ~/.claude is edited. UNVERIFIED: that hooks from `--settings` run next to the user's own hooks (the installed guard sees an unbound session and allows, so it should not change the result). The log is checked for a first line right after the session starts; an empty log means the probe did not fire and the step is void.

## 3. Step 0: OB-CTX (first in design section 14, not one of the four gate items)
Design section 14 step 0 makes OB-CTX / B-CTX "the first required task", and section 19.8 lists it as pending. It is NOT one of the four items in `_GATE_ITEMS` (test_launch_level_observations.py:82), so it does not hold the ship gate closed in code, and the task did not ask for it. This plan therefore does not plan its steps. Section 19.1 says B-CTX is "OPEN/BLOCKING for the earlier plan's complete lifecycle coverage" and that the scoped per-job selector of 19.7 is not a retroactive pass. See open question Q1: whether the gate should also wait for OB-CTX.
- Class: not planned here. Un-skips: `test_pending_live_observation[OB-CTX]`.

## 4. OB-H1 (design section 14 step 1)
Design section 14 gate text: "Validate U1, typed top-level identity/event fields and turn wrapping. Gate: item 1 fails, stop (O-9); item 5 bare, apply O-17 alternative. Identity loss on a supported governed call stops deployment." Both steps use the common setup of section 2 and the probe `log-only-probe.sh`. Log: `$OBS/logs/ob-h1.jsonl`.

### 4.1 OB-H1 item 1: parent session_id in subagent and nested-subagent payloads
- Class: OUTWARD (paid session only, no GitHub write). Preparation (common setup) is LOCAL; the session is not, because a new `claude` process is a paid model run. Cost: 1 short model session (main thread, one subagent, one nested subagent, three Bash calls). Rollback: none needed; delete the temp directory `rm -rf "$OBS"` (only the exact directory printed by setup).
- Un-skips: `test_pending_live_observation[OB-H1 item 1]` (test_launch_level_observations.py:108-110).
- Commands (person, in a plain terminal, never inside Claude):
  1. `cd "$OBS/work" && claude --settings "$OBS/settings.json"`
  2. Prompt 1: "Run Bash `echo MAIN`. Then start one general-purpose subagent with the Agent tool and tell it to run Bash `echo SUB` and then, if it can, start its own subagent that runs Bash `echo NESTED`. Report which of the three echoes ran, and say plainly if the subagent had no Agent tool."
  3. Exit the session. Then inspect (LOCAL, read-only): `jq -c '{e:.hook_event_name,s:.session_id,a:.agent_id,t:.agent_type,tool:.tool_name,cmd:.tool_input.command}' "$OBS/logs/ob-h1.jsonl"`
- What the log must show (design section 11, OB-H1 item 1): "subagent and nested-subagent `session_id`, `agent_id`, `agent_type` (U1)"; README: "does the parent's `session_id` appear?"
- PASS (design section 7 item 4): "OB-H1 item 1 shows the parent's `session_id` in subagent and nested-subagent payloads". In log terms: the PreToolUse line for `echo SUB` and the line for `echo NESTED` each carry a top-level string `session_id` equal to the one on the `echo MAIN` line, and `agent_id` is present on the SUB and NESTED lines. Section 14 adds: a valid top-level string id and a consistent event shape on every supported governed call (section 3, "Identity loss").
- FAIL (design section 14 and section 7 item 5): "item 1 fails, stop (O-9)"; "no `cwd` fallback is built. If item 1 fails, stop and take O-9" (O-9 default is "stop", alternative "reserve `cwd` fallback"). Also fail: any governed-call line without a valid top-level string `session_id`: "Identity loss on a supported governed call stops deployment."
- Needs an owner reading if the harness gives subagents no Agent tool: the nested half cannot be produced. See Q2.
- UNVERIFIED (not stated in the design): that a subagent can start a nested subagent in Claude Code 2.1.331. The prompt asks the model to say so; the log is the evidence.

### 4.2 OB-H1 item 5: self-started turns wrapped
- Class: OUTWARD (paid session only, no GitHub write). Cost: 1 model session, longer (it waits on background work); can share the session of 4.1 only if the owner accepts one long session. Rollback: same as 4.1.
- Un-skips: `test_pending_live_observation[OB-H1 item 5]`. The fixture `item5-monitor-approved-line.json` stays synthetic; `test_apr_ob_h1_item5_fixture_releases_nothing` (named in the ob_h1 README) is not the observation.
- Commands (person): start `claude --settings "$OBS/settings.json"` in `$OBS/work`, then ask for three self-starting events and wait for each to arrive on its own (do not type anything while waiting):
  1. A background Bash: "Run Bash with run_in_background: `sleep 15; echo bgdone`. Then do nothing until it reports back."
  2. A Monitor line: "Start a Monitor on `sleep 10; echo approved` and do nothing until the line arrives."
  3. A background subagent: "Start a general-purpose subagent with run_in_background true that runs `echo subdone`. Do nothing until it reports back."
  Inspect (LOCAL): `jq -c 'select(.hook_event_name=="UserPromptSubmit") | {p:.prompt}' "$OBS/logs/ob-h1.jsonl"`
- What the log must show (design section 11, OB-H1 item 5): "exact `prompt` of a Monitor line `approved` and of background-Bash and background-subagent notices (U4, O-17)".
- PASS (design section 7 item 4): "item 5 shows self-started turns wrapped"; section 6: "self-started turns arrive wrapped, so never exactly `approved` (FR-L-19)". In log terms (DERIVED, see Q3): each of the three self-started turns appears as a UserPromptSubmit line (or as no line at all) and none has a prompt that is exactly `approved` or whose first line matches the release pattern `^/(sc:implement|task)([[:space:]]|$)` (design section 6, FR-L-16).
- FAIL (design section 14): "item 5 bare, apply O-17 alternative". O-17: default "self-started turns allowed", alternative "block at `W`". A prompt that is bare means: the Monitor line arrives as exactly `approved`, or any notice arrives with a first line that matches the release pattern.
- Note: since the plain `approved` route was removed (Q39, section 6), a bare `approved` no longer releases by itself; the check still matters for the first-line pattern, and the design still lists item 5 as a gate (section 7 item 4, test `_GATE_ITEMS`).

### 4.3 OB-H1 items 2, 3, 4, 6, 7, 8, 9: optional
None of them is in `_GATE_ITEMS` (test_launch_level_observations.py:82) and none is named in the ship-gate text of design section 7 item 4, claim.md:136 or launch.py:48. None is needed before the gate may open by the rules as written. The same probe and settings capture them for free in the sessions of 4.1 and 4.2, so the plan records them opportunistically (extra prompt lines, no extra session). Each un-skips its own `test_pending_live_observation[OB-H1 item N]`; the gate does not depend on those.

| Item | What to capture (design section 11) | Extra prompt in the 4.1 or 4.2 session | Needed before the gate opens? | Why it still matters |
|---|---|---|---|---|
| 2 | Skill keys, name form (U2) | "Run the Skill tool for `sc:help`" | No | If the key is not `skill` or `name`, SKILL and IMPL classes fail open |
| 3 | Agent name, `isolation` (U3, U13) | the Agent calls of 4.1 already show the tool name; add one with `isolation` set only if the owner approves a remote one (NOT recommended: it could leave the machine) | No | Records whether `Agent` or `Task` is the name |
| 4 | typed `/sc:implement x` (O-4) | type `/sc:implement x` as the first prompt of a throwaway session in `$OBS/work` (the model run is wasted; Ctrl-C after the log line) | No for the gate, but OB-H3 step W-unlock (6.2) will fail if item 4 is wrong | Order: "the prompt event runs before expansion, so `.ok` exists before Skill `sc:implement-protocol`. OB-H1 item 4 checks" (section 6) |
| 6 | `TaskCreate` versus the anchored matcher (U15) | "Create a task with TaskCreate" | No | The matcher in design section 13 does not list TaskCreate; it is meant to be unmatched |
| 7 | SendMessage, MCP names (U12) | "List your MCP tool names" is not an observation; needs a real call. Skip unless an MCP server is configured | No | MCP and SendMessage classes depend on the names |
| 8 | `claude` without `-p` (U14) | Bash `claude --help` is not enough; needs a `claude` command seen by PreToolUse | No | ESCAPE class |
| 9 | Bash, Edit, Write, Skill names (U21) | covered by 4.1 (Bash) plus one Edit and one Write on a file under `$OBS/work` | No | The matcher is anchored: a name mismatch silently skips the guard |

Class of the extra prompt lines: part of the same OUTWARD session; they add no GitHub write. Item 7 and 8 may need real MCP or `claude` calls that this plan does not authorize; they stay pending without harm to the gate.

## 5. OB-H2 (design section 14 step 8, first half)
Design section 11: "OB-H2 (after the claim feature ships). Session file before the first tool call (U8); exact first prompt and marker position (U7); hook `HOME` and `CLAUDE_CONFIG_DIR`; IR-4 refusals; LL-NOBIND visibility (U20)." The claim feature has shipped (design 19.8: IR-1, IR-2, IR-4 to IR-7 built). Section 14 gate: "no real governed launch until both [OB-H2 and OB-H3] pass". Un-skips: `test_pending_live_observation[OB-H2]`.

### 5.1 Probe for OB-H2 (needed; does not exist yet)
`log-only-probe.sh` has no timestamp and records neither HOME, CLAUDE_CONFIG_DIR nor the session file. U8 ("bind timing, OB-H2 mandatory") cannot be shown with it. The plan needs one small extra probe script, written to `$OBS/ob-h2-probe.sh` (temp dir, not the repo), run in addition to the guard on UserPromptSubmit and PreToolUse. It appends one JSON line with: `date +%s%N`, the payload (`jq -c .`), `$HOME`, `${CLAUDE_CONFIG_DIR-unset}`, and `stat -c '%W %Y %n' "$HOME/.claude/state/launch-level/sessions/<sid>"` or `absent`. It always exits 0. Writing it is LOCAL; it is not written by this plan. Registering it for a real claim needs a hook entry in ~/.claude/settings.json (see 5.3, OUTWARD, shared config) because the claim launches the agent itself and no `--settings` flag is under our control. Cost: none beyond 5.3. Rollback: restore the backup of settings.json taken first (`cp -p ~/.claude/settings.json "$OBS/settings.json.bak"`).

### 5.2 Rehearsal without GitHub (OUTWARD: paid session only, no GitHub write)
Purpose: find mistakes in the probe and the prompts before the real claim. Its result does NOT count as OB-H2 evidence, because it is not a real claim (design 19.5 and IR-4 speak of the real claim's installation and environment).
1. Make a throwaway store so the real `~/.claude/state/launch-level` is not touched: `mkdir -p "$OBS/home/.claude/state/launch-level/pending" "$OBS/home/.claude/state/launch-level/sessions"`. Write one pending record: `NONCE=$(openssl rand -hex 16); printf 'worktree\n' > "$OBS/home/.claude/state/launch-level/pending/$NONCE"` (name `^[0-9a-f]{32}$`, one word, design section 3).
2. Register the guard through `--settings` with a changed HOME for the hook only: command `env HOME=$OBS/home /home/coder/.claude/hooks/launch-level-guard.sh` on UserPromptSubmit and on PreToolUse with the section 13 matcher, plus the OB-H2 probe. UNVERIFIED that the guard derives its store from `$HOME` this way; section 3 says `$HOME/.claude/state/launch-level/`.
3. Start `claude --settings <file>` in `$OBS/work` with first prompt `[sc-launch:v1:$NONCE] list the files here`.
4. LL-NOBIND visibility (U20): repeat with `chmod 500 "$OBS/home/.claude/state/launch-level/sessions"` and a fresh nonce; design section 10 row "`sessions/` read-only" gives LL-NOBIND. Look at the terminal: is the blocked prompt's text shown to the person?
Cost: 2 short model sessions. Rollback: `rm -rf "$OBS"`; the real store is untouched.

### 5.3 The observation proper: one real claim at `worktree` (OUTWARD)
The same real claim also serves OB-H3 step W (section 6.2), so OB-H2 and the W part of OB-H3 are taken in ONE session and ONE test issue, to avoid a second claim.
- Action (person): create test issue A on IronbellyOrg/IronClaude (see 6.1), then in a Claude session run `/sc:issue --claim <A> --pipeline worktree` (claim.md and `PROMPT_PATTERN` in launch.py:33-37 give the launched agent's prompt `/sc:issue --claim <A> --pipeline worktree --stage <research|spec|plan|debug>`). Repository: IronbellyOrg/IronClaude only; never SuperClaude-Org, and never pass Orca `--issue` or `--pr` link flags (CLAUDE.md of this repo).
- GitHub writes made by the claim: the issue is assigned (and a ClickUp task is touched, per the sc-issue-protocol skill description). Orca writes: a worktree and an agent session. Cost: 1 claim session (the person's) plus 1 launched agent session that runs to the plan boundary.
- Evidence to collect (all read-only after the fact, LOCAL):
  1. U8, "session file before the first tool call": in the OB-H2 probe log, the first PreToolUse line of the launched session must show `sessions/<sid>` present (birth time earlier than the line's timestamp). Compare also with the first UserPromptSubmit line.
  2. U7, "exact first prompt and marker position": the first UserPromptSubmit line's `.prompt`. Record whether `[sc-launch:v1:<nonce>] ` is the first characters, or after an Orca preamble (O-11 "Orca worker commands", and the design asks to "Record Orca preamble (O-11)" in OB-H3). 
  3. Hook `HOME` and `CLAUDE_CONFIG_DIR`: the two fields of the OB-H2 probe line. IR-4 supports only `$HOME/.claude`; "An effective `CLAUDE_CONFIG_DIR` resolving elsewhere is unsupported and must refuse the governed launch".
  4. IR-4 refusals: the claim's result JSON (`W-ENFORCEMENT-ABSENT`, cmd_launch at orca_worktree.py:1773-1790) must be `enforcement_hook: "installed"` in the passing run. A refusal observation is a separate step: see 5.4.
  5. LL-NOBIND visibility: only seen if a bind fails; covered by 5.2 step 4 (a real claim is not forced to fail).
- PASS criteria quoted from the design: IR-4 "OB-H2 must observe actual hook execution and bind-before-first-tool order"; section 3 binding: "Failure to obtain a valid binding gives LL-NOBIND"; section 14 "Identity loss on a supported governed call stops deployment"; section 16 R6 / U7: marker position as the guard expects ("a strict marker is the first `\[sc-launch:v1:([0-9a-f]{32})\]` anywhere"). FAIL: the session file is absent at the first tool call (U8 false: then R14 "U1 or U8 false, checks skipped" applies and deployment stops), or the marker is mid-prompt with no usable record (LL-NOBIND, O-20), or HOME is not the claim's HOME, or `CLAUDE_CONFIG_DIR` points elsewhere.
- Rollback: close issue A (`gh issue close <A> --repo IronbellyOrg/IronClaude --reason "not planned"`), unassign, `orca worktree rm --worktree <name>` for the claim's worktree, remove the session and pending files of that sid by hand (no pruning exists, O-15), restore settings.json from the backup. The comment and the closed issue stay on GitHub; GitHub offers no delete for issues through `gh` without admin rights.

### 5.4 IR-4 refusals
- LOCAL candidate (to be confirmed by reading `guarded_record_path` and `enforcement_preflight` first; UNVERIFIED that it works without Orca): run `uv run --no-project python <skill base>/scripts/orca_worktree.py launch --number 1 --source <temp dir> --level worktree` inside a disposable git clone in /tmp with a PATH that has no `jq`, expecting `W-ENFORCEMENT-ABSENT` and no agent. The refusal is raised before `install_l2` and `publish_pending` (orca_worktree.py:1768-1790), so no launch record and no agent are created. The skill base path is read from the installed skill, not from `src/superclaude`. If it needs an Orca worktree record, the step becomes OUTWARD and is dropped.
- What it proves: the refusal fires for one missing item (jq). Design 19.8 names the full list: `jq`, `uv`, `cat`, `sed`, `tr`, `mkdir`, `mv`, `ln`, `rm`, the installed guard, its effective registrations, the job identity registration. One case per item is 9 to 12 local runs, no model.
- PASS: "Refuse a governed launch unless jq exists, the expected installed script/version is executable, and the effective configuration actually enables both registrations" (IR-4). FAIL: a launch record or agent appears.

## 6. OB-H3 (design section 14 step 8, second half)
Design section 11: "OB-H3 (test issue, each level, after all prior gates). `W` stops and unlocks by both routes; `F` logs git commands (U10); `FS` runs one authorized `/sc:pr-submit --monitor 3` cycle logging pushes and inline `gh api` (O-18, O-19) and a conflict (O-10). Protected-push/merge refusal tests use disposable repositories, never an actual protected branch on the fork. L2 observation follows 19.5. Count LL-PUSH-FORM, LL-GH-WRITE, LL-TEXT and NM1a/G2 UNKNOWN; separately count am-only blocked first attempts and retries before any O-21 reconsideration. Record Orca preamble (O-11), one live message (AC-7), timing, and exact harness/config versions. A skipped observation remains pending, not passed." Un-skips: `test_pending_live_observation[OB-H3]`. Every step here is OUTWARD.

### 6.1 Shared setup: probe, verdict evidence, test issues
- Probe: a hook entry in /home/coder/.claude/settings.json (OUTWARD: shared config outside this worktree) running `LAUNCH_LEVEL_PROBE_LOG=/tmp/ll-obs.<random>/logs/ob-h3.jsonl /tmp/ll-obs.<random>/probe.sh` on PreToolUse (matcher `.*`), PostToolUse and UserPromptSubmit. The path is fixed in the command string because the Orca-launched agent does not inherit this shell's environment (UNVERIFIED). Rollback: restore `$OBS/settings.json.bak`.
- Guard verdicts are not in the probe log (the probe sees inputs only). A PreToolUse line with no PostToolUse line for the same `tool_use_id` is a blocked call; the block text (`LL-<class>`, "Launch-level guard: ...") is read from the session transcript under `~/.claude/projects/<slug>/<sid>.jsonl` (U27 `transcript_path`, UNVERIFIED), with `grep -o 'LL-[A-Z0-9-]*'`. LOCAL after the fact.
- Test issues: three, one per run, because a second claim on the same issue is refused as `already_launched` (orca_worktree.py:1751-1764). Create each with `gh issue create --repo IronbellyOrg/IronClaude --title "[launch-level observation] OB-H3 <level> test issue" --body-file <filled copy of ~/.claude/ISSUE-BACKLOG.md>` (CLAUDE.md rule 10: copy the template, fill it, never edit the installed one). Body states: disposable, safe to close, no code change wanted. Pipeline field set per run to Worktree, Full, Full Submit. Cost: 3 GitHub issues. Rollback: close each with `--reason "not planned"` and a comment; labels or project items added are removed by hand.
- Disposable remote for every protected-push test: `git init --bare "$OBS/scratch-remote.git"`, then inside the claimed worktree `git remote add scratch "$OBS/scratch-remote.git"` (done by the person, before asking the agent to push). Protected-branch attempts go to `scratch`, never to `origin`.

### 6.2 Run W: `--pipeline worktree`, test issue A (same claim as 5.3)
- Class: OUTWARD (GitHub issue write, claim writes, 1 paid agent session). Cost: the claim session of 5.3 continues; plus up to 2 short follow-up turns. No extra issue.
- Un-skips: `[OB-H3]` (part), and gives the evidence for design AC-3 cases.
- Steps (design section 6 and 4):
  1. Stop at `W`: the launched agent runs the research steps up to the plan boundary (`Plan boundary: after step <K>` in next-steps.md, claim.md line 82). Ask it, as the person, to run `git commit --allow-empty -m probe`, then `git status`, then Skill `sc:implement`. Expected per the grid (section 4): commit B (LL-COMMIT), `git status` A, Skill `sc:implement` B (LL-IMPL).
  2. Unlock route 1: the person types `/sc:implement x` as a prompt (the match is the first line matching `^/(sc:implement|task)([[:space:]]|$)`; section 6, FR-L-16). Expected: `sessions/<sid>.ok` is created, W becomes WA, `/sc:implement` is allowed, commit is still blocked (WA row: SUBMIT, COMMIT, PUSH, SKILL blocked).
  3. Negative checks in the same session before step 2: typed `approved` releases nothing (Q39); a prompt with `agent_id` is ignored.
  4. Unlock route 2: the person removes `~/.claude/state/launch-level/sessions/<sid>.ok` (design section 3 and R13: `rm` releases), confirms the guard blocks again, then types `/task <some file>`. Expected: `.ok` appears again, WA.
  5. Record the Orca preamble (O-11) from the first prompt line of the probe log.
- PASS (design section 6): "only the first line matching `^/(sc:implement|task)([[:space:]]|$)` releases ... `touch .ok`; `W` becomes `WA`. It unlocks IMPL ... never COMMIT, PUSH, SUBMIT or MERGE." FAIL: the agent runs the commit at W, or either typed route leaves W blocked, or WA allows a commit/push.
- Rollback: as 5.3.

### 6.3 Run F: `--pipeline full`, test issue B
- Class: OUTWARD (GitHub issue write, claim writes, 1 paid agent session; this run also executes `/sc:implement`, so it may spend more than the other levels). Cost: 1 issue, 1 claim, 1 agent session (several turns).
- Step: let the agent implement a tiny disposable change in the worktree (README line in the claimed worktree), without commit. Capture every Bash git command from the probe log (U10: "`/sc:implement` git use") and the verdict per command.
- PASS (design section 4, F column): IMPL, TURN and NONE allowed; SUBMIT, COMMIT, PUSH, SKILL blocked. The U10 check: the list of git commands `/sc:implement` ran contains none that the guard blocked unintentionally (anything blocked that is not a commit, push, merge or similar is recorded as an over-block, R8 / O-21). The design gives no numeric criterion for U10: see Q3.
- FAIL: a commit or push at F is allowed; or `/sc:implement` cannot finish because a routine git command (add, diff, status, log) is blocked.
- Also: the OB-H3 counts of design section 11 ("Count LL-PUSH-FORM, LL-GH-WRITE, LL-TEXT and NM1a/G2 UNKNOWN; separately count am-only blocked first attempts and retries") are taken here and at FS from the transcripts (LOCAL, after the fact).
- Rollback: as 5.3; the uncommitted change dies with the worktree.

### 6.4 Run FS: `--pipeline full --submit`, test issue C
- Class: OUTWARD (GitHub issue write, a pushed branch, a PR, review services, paid sessions). Repository: IronbellyOrg/IronClaude only. Cost: 1 issue, 1 claim, 1 agent session, one `/sc:pr-submit --monitor 3` cycle (up to 3 remediation rounds, each a model turn, plus the Augment and Codex reviews on the PR), so 3 to 6 model sessions in total (estimate; no number is in the design). Rollback: close the PR without merging (`gh pr close <n> --repo IronbellyOrg/IronClaude --delete-branch`), close issue C, remove the worktree.
- Steps:
  1. Commit, push a feature branch, open one PR with the authorized `/sc:pr-submit --monitor 3 --head <branch> --title "..." --body "..."` (the repo's mandatory route; it opens the PR with `gh pr create --repo IronbellyOrg/IronClaude`). Check the printed PR URL starts with `https://github.com/IronbellyOrg/IronClaude/pull/`; if it points at SuperClaude-Org stop and report (CLAUDE.md). The change is one line in a scratch file; the PR is never merged.
  2. Record every push and every inline `gh api` call (O-18 "compound push at FS: blocked, widen form"; O-19 "non-canonical `gh api`: blocked, admit GET variants") with verdict. The O-18 and O-19 defaults stay in force; the observation shows how often they bite.
  3. Conflict (O-10, "sync merge at FS: blocked; alternative allow `--no-commit`, `--abort`"): the person makes the feature branch conflict with its base by committing a change to the same lines on the base. To avoid touching master of the fork, the PR is opened against a disposable base branch `ll-obs-base-<C>` pushed by the person, which gets the conflicting commit. Then observe what the governed agent and `/sc:pr-submit` do when a sync is needed. UNVERIFIED: how `/sc:pr-submit` handles a conflict. Extra cost: 1 branch on the fork, deleted afterwards.
  4. Protected-push and merge refusal: from inside the governed session ask the agent for `git push scratch HEAD:main`, `git push scratch HEAD:refs/heads/main --force`, and `git merge <branch>`; the targets are the disposable remote of 6.1. Expected: LL-PROTECTED / LL-MERGE from L1; if the push reaches git, the L2 hook `launch-level-pre-push.sh` refuses it (design 19.5: "Use fixture refs that actually reach pre-push ... and require the hook's own diagnostic"). Assert the before/after refs of the scratch remote: `git -C "$OBS/scratch-remote.git" for-each-ref` identical before and after. Never `origin`, never a real protected branch.
  5. Also record: one live message (AC-7, ESCAPE class SendMessage blocked text visible), timing of the guard per call (design 19.8 measured L2 at about 100 ms per push; this adds the L1 time), exact harness version (`claude --version`: 2.1.331 now) and `git --version`.
- PASS (design section 4, FS column and section 19.5): commit, push of a feature branch, SKILL and SUBMIT allowed; REPO, PUSHFORM, PROTECTED, MERGE, GHWRITE, ISSUE, UNKNOWN, MCP, ESCAPE, TAMPER, BIG blocked; remote refs of the scratch destination unchanged after each refused push. FAIL: any push to a protected name reaches a remote ref, or the monitor cycle cannot complete because a blocked class stops a step the cycle needs (that is a finding for O-18 / O-19, not an automatic fail of the gate; owner decision, Q4).
- Un-skips: `[OB-H3]`.

### 6.5 Order and dependencies
Per design 14 step 8, OB-H2 first, then OB-H3, "after all prior gates": OB-H1 items 1 and 5 pass before any real claim (4.1, 4.2); then 5.2 rehearsal, then run W (which also provides the OB-H2 evidence), then F, then FS.

## 7. Which observations can be finished with LOCAL steps only
None of the four gate observations can be completed with LOCAL steps only.
- OB-H1 item 1 and item 5: need a live harness producing subagent payloads and self-started turns; the only way to get one is a new `claude` process, which is a paid session (OUTWARD by the definition given). `live_probe.py` cannot stand in: it runs one Bash call, with only Bash enabled, and lists `nested_subagent_payload`, `Monitor` as unobserved (live_probe.py:310-319).
- OB-H2: needs a real claim (OUTWARD) for HOME, CLAUDE_CONFIG_DIR, marker position and bind order. Only the IR-4 refusal part has a LOCAL route (5.4, UNVERIFIED).
- OB-H3: needs issues, a PR, pushes (OUTWARD).
LOCAL parts: temp directory and probe setup (2), writing the OB-H2 probe (5.1), IR-4 refusal runs (5.4), reading logs and transcripts, counting LL classes, writing the evidence-reading tests of section 8 inside this worktree.
If the owner decides an attended interactive session of the owner's own account is not a "paid session beyond this session's own model" (Q5), then 4.1, 4.2 and 5.2 become LOCAL; 5.3, 6.2 to 6.4 stay OUTWARD either way, so OB-H2 and OB-H3 still cannot be LOCAL.

## 8. What flipping GOVERNED_LEVELS_ALLOWED needs besides the observations
What the code says now:
- `launch.py:48`: `GOVERNED_LEVELS_ALLOWED = False`. Its docstring: "Flipped only by a reviewed commit that also un-skips the launch-level observations of tests/hooks/test_launch_level_observations.py (a coupling test enforces it)." No config key or environment variable is the switch.
- Coupling test: `test_the_ship_gate_opens_only_when_its_observations_are_run__r33` (test_launch_level_observations.py:97-105) calls `_gate_may_be_open(launch.GOVERNED_LEVELS_ALLOWED, _PENDING)`. With the gate True it fails while any of "OB-H1 item 1", "OB-H1 item 5", "OB-H2", "OB-H3" is in `_PENDING` (line 79, built from 12 names).
- Readers of the flag: `src/superclaude/cli/issue_watch/cycle.py:1032` (level_gated skip) and `first_run.py:218` (report line "ship_gate: closed (only Pipeline None launches)").

The flipping commit needs, besides the passed observations:
1. The four ids removed from `_PENDING`, and for each removed id a real test replacing the generic `pytest.skip` of `test_pending_live_observation` that reads the committed evidence file (`.dev/launch-level-observations/evidence/<step>.jsonl`) and asserts the PASS criterion of sections 4 to 6. Removing a name from `_PENDING` alone satisfies the coupling test with no evidence at all, so the review of the commit, not the test, is what checks the evidence. The other eight ids (items 2, 3, 4, 6, 7, 8, 9 and OB-CTX) may stay pending: `_gate_may_be_open(True, ["OB-H1 item 2", "OB-CTX"])` is asserted True (line 94).
2. Existing tests that pin the closed gate must change in the same commit: tests/issue_watch/test_first_run.py:305 (`assert launch.GOVERNED_LEVELS_ALLOWED is False` and the line "ship_gate: closed ..."), tests/issue_watch/test_cycle.py:2797 (same assertion, in the `level_gated` test parametrized over Worktree, Full, Full Submit). Others that monkeypatch it to True (test_first_run.py:326, test_cycle.py:2865) keep working.
3. Docs that state the gate closed: src/superclaude/skills/sc-issue-protocol/refs/claim.md:136 ("Ship gate: no governed claim ... until OB-H1 item 1, OB-H2 and OB-H3 have passed"), docs/designs/sc-issue-launch-level-hook.md section 19.8 "Pending, none run", docs/designs/issue-watcher.md:972, docs/designs/issue-watcher-status-pipelines.md:104. Edited in `src/superclaude/`, then `make sync-dev` and `make verify-sync`; never stage `.claude/` (CLAUDE.md).
4. Reconcile the two wordings of the gate before flipping: design section 7 item 4 gates `full` and `--submit` on item 1 and any level on item 5, while claim.md:136 gates every governed claim on item 1, OB-H2 and OB-H3 (and omits item 5). One boolean follows the stricter text (issue-watcher-status-pipelines.md:104); a per-level split is an owner option (Q6).
5. Outcomes that change code before the flip: item 1 fail means stop (O-9); item 5 bare means apply the O-17 alternative; U8 false means R14. `IR7_REFUSE` (orca_worktree.py:859) is a different switch: it "stays off until the #442 observations pass and the owner approves" (design IR-7); OB-H3's L2 evidence feeds that decision but flipping `GOVERNED_LEVELS_ALLOWED` does not turn it on.
6. Repo process: the flip is one reviewed commit on a feature branch, rebased on origin/master, opened with `/sc:pr-submit --monitor 3` against IronbellyOrg/IronClaude (CLAUDE.md). This worker does not commit.

## 9. Open questions for the owner
Each question: the recommendation is first, then what each answer does.

- Q1. Must OB-CTX also pass before the gate opens? Design 14 step 0 calls it "the first required task" and 19.1 says B-CTX is "OPEN/BLOCKING", but `_GATE_ITEMS` omits it. Recommendation: yes, add "OB-CTX" to `_GATE_ITEMS` in the flipping commit, or record the owner's written decision that the scoped per-job selector of 19.7 replaces it. Yes: OB-CTX gets its own plan and the gate waits for it. No: the gate opens on the four items and 19.1's blocking status is recorded as accepted risk.
- Q2. If a subagent has no Agent tool, the nested half of item 1 cannot be produced. Recommendation: accept "nesting impossible in 2.1.331" as a pass for the nested half if the log and the model's statement show it. Yes: item 1 passes on the one-level subagent. No: item 1 stays pending until nesting is possible.
- Q3. The design gives no measurable PASS wording for item 5 (beyond "wrapped") and none for U10. This plan derived them (4.2, 6.3). Recommendation: approve the derived criteria. Yes: they are used as written. No: the owner gives the wording and the plan is updated.
- Q4. At FS, if the `/sc:pr-submit --monitor 3` cycle is blocked by a class the design blocks on purpose (O-18, O-19, O-10), is that a failed observation or a finding? Recommendation: a finding, recorded and counted; the observation passes when the guard behaves as the grid says. Yes (finding): the gate can open with documented over-blocks. No (fail): O-18/O-19/O-10 are reopened first.
- Q5. Does an attended interactive session of the owner's own account count as the "paid model run beyond this session's own model"? This plan says yes (OUTWARD). If no, 4.1, 4.2 and 5.2 are LOCAL.
- Q6. One boolean (stricter text, as now) or a per-level split with item 5 and item 1 gating `full`/`--submit` separately? Recommendation: keep one boolean. Yes (one): no code change. No (split): launch.py, cycle.py and their tests change.
- Q7. May the worker run, in order: edit ~/.claude/settings.json (hook entry, backup first), create 3 test issues and 1 PR and 1 base branch on IronbellyOrg/IronClaude, and touch ClickUp through the claim? Recommendation: yes, step by step, with the coordinator confirming each OUTWARD step before it runs. Yes: sections 5.3 and 6 may proceed in the order of 6.5. No: only the LOCAL preparation and the OB-H1 sessions run.
- Q8. The OB-H2 and OB-H3 probe cannot be passed to a claim-launched agent without a hook entry in the owner's settings. Alternative: put the entry in the claimed worktree's `.claude/settings.local.json` after the worktree exists and before the agent starts (race with the launch; UNVERIFIED). Recommendation: the settings.json entry with a backup.

# Harness feasibility for the controlled create runs (Task 4)

Written 2026-11-26 by the implementing session. Every answer below comes from a command that was run; raw logs are in the scratch directory `createQuestionEv-scratch` under the system temporary directory (`/tmp/createQuestionEv-scratch`), outside the repository. Nothing in this file is a secret: the model gateway token was passed by reference (`$ANTHROPIC_AUTH_TOKEN`) and never written to a file.

## 1. The installed `claude` and its options

Command: `claude --version`
```
2.1.332 (Claude Code)
```

Command: `claude --help` (full text saved at `/tmp/createQuestionEv-scratch/claude-help.txt`). The options that matter for a controlled run, as printed:
```
10:  --add-dir <directories...>            More directories Claude can access
13:  --agents <json-or-file>               JSON object defining custom agents, or
22:  --allowedTools, --allowed-tools <tools...>
40:  --bare                                Minimal mode: skip hooks (those defined
82:  --disallowedTools, --disallowed-tools <tools...>
116:  --include-hook-events                 Include all hook lifecycle events in the
122:  --input-format <format>               Input format (only works with --print):
132:  --mcp-config <configs...>             Load MCP servers from JSON files or
143:  --no-session-persistence              Don't save sessions to disk; they can't
145:  --output-format <format>              Output format (only works with --print):
150:  --permission-mode <mode>              Permission mode to use for the session
154:  --permission-prompts <target>         Who answers permission prompts with
162:  --plugin-dir <path>                   Load a plugin from a directory or .zip
170:  -p, --print                           Print response and exit (useful for
194:  --restricted                          Restricted mode: removes the built-in
225:  --session-id <uuid>                   Use a specific session ID for the
227:  --setting-sources <sources>           Comma-separated list of setting sources
229:  --settings <file-or-json>             Settings file or JSON string to load
231:  --strict-mcp-config                   Only use MCP servers from --mcp-config,
252:  --tmux                                Create a tmux session for the worktree
256:  --tools <tools...>                    Built-in tools to make available: "" for
```

- Print mode: `-p`, with `--output-format stream-json --verbose` for a streamed event log and `--input-format stream-json` for streamed input.
- Permission mode choices: `acceptEdits`, `auto`, `bypassPermissions`, `manual`, `dontAsk`, `plan`. Tool lists: `--allowedTools`, `--disallowedTools`, `--tools`.
- MCP: `--mcp-config` plus `--strict-mcp-config` (only the servers in the given files; with none given, no MCP server loads).
- Extra directories: `--add-dir`. Skills, agents or a plugin from a directory: `--plugin-dir <path>`, `--agents <json-or-file>`. Settings: `--settings`, `--setting-sources`.

## 2. How the `src/` copy of the skill, the workers and the command gets loaded

Options considered:

1. `--plugin-dir` with a plugin built from `src/`: not chosen. The command, skill and agent names would be namespaced by the plugin, so `/sc:issue`, `Skill sc:issue-protocol` and the `issue-worker-t*` agent types would not resolve under their real names, and the run would not test the shipped wording.
2. `--agents <json-or-file>` for the workers only: not chosen. It covers agents but not the skill or the command.
3. A temporary home and configuration directory seeded from `src/` (chosen). `HOME` and `CLAUDE_CONFIG_DIR` point at `/tmp/createQuestionEv-scratch/home`, whose `.claude/` holds copies of `src/superclaude/commands/*.md` (as `commands/sc/`), `src/superclaude/skills/*` (as `skills/`) and `src/superclaude/agents/*.md` (as `agents/`). Claude Code reads that folder as the user copy, so the names resolve as they do in a real install, and the user's real `~/.claude` is never read or written. A project folder `.claude/` is not used: a clone of the worktree has none (it is gitignored sync-dev output), and an agent file in a project folder would be read before the installed one, so the clone is kept free of one.
4. Installing into the real user directory, or keeping the real home: rejected. The installed user copy differs from `src/` (section 6), and a run must not modify it.

Proof that a run resolves to the seeded copy: dry run G (command in section 7) loads the skill by name, and the event log prints the path of the loaded copy:

```
"Base directory for this skill: /tmp/createQuestionEv-scratch/home/.claude/skills/sc-issue-protocol\n\n<!-- Extended metadata (for do"
```

So a skill load shows by name in the tool call (`Skill {"skill":"sc-issue-protocol"}`) and by directory in the text that follows (`Base directory for this skill: /tmp/createQuestionEv-scratch/home/.claude/skills/sc-issue-protocol`). Whether the event log shows worker (subagent) loads by path or only by name was not established here: the first real run (Task 6) reads every transcript file under the run's `projects/` folder, including any `subagents/` folder, and `read-files.txt` records only what the transcripts show; a worker load that shows by name only is recorded as "by name" with the hash of the seeded file the name resolves to in that home.

## 3. How `AskUserQuestion` appears, and whether the run can answer it

Finding: print mode does not offer `AskUserQuestion` in this build (2.1.332).

Dry runs A to D (print mode, probe prompt in section 7). The tool list printed in the init event of run A (`--permission-prompts none`), and the same list in run B (`--input-format stream-json`, `--permission-prompts host`):

```
A: ["Task","Bash","CronCreate","CronDelete","CronList","DesignSync","Edit","EnterWorktree","ExitWorktree","ListAgents","Monitor","NotebookEdit","Read","ReportFindings","ScheduleWakeup","SendMessage","Skill","TaskStop","WebFetch","WebSearch","Workflow","Write"]
B: ["Task","Bash","CronCreate","CronDelete","CronList","DesignSync","Edit","EnterWorktree","ExitWorktree","ListAgents","Monitor","NotebookEdit","Read","ReportFindings","ScheduleWakeup","SendMessage","Skill","TaskStop","WebFetch","WebSearch","Workflow","Write"]
C (--tools AskUserQuestion): 0 tools
D (--tools default,AskUserQuestion): 0 tools
```

The model reply in run A:
```
I couldn't ask the question because there's no AskUserQuestion tool in this session. Nothing was sent to you, so I have no answer to print.

You told me not to run any other tool, so I didn't try a substitute. This is the question I would have asked:

- **Head
```

Per the plan, a dry print-mode run that shows no question event makes the decision a stop report (section 8). Because the question rule of issue 834 is about an interactive question, a print-mode run would not exercise it, so an interactive route was tried next.

Interactive route (dry runs E and F): an interactive `claude` session inside `tmux`, driven by a script (`/tmp/createQuestionEv-scratch/probe_tmux.sh`) that sends the probe prompt as keystrokes, waits for the question screen and sends Enter. The session transcript that Claude Code writes under the isolated home (`home/.claude/projects/<cwd>/<session>.jsonl`) is the event log: it records each tool call and its result.

- Run E, `--permission-mode dontAsk`: the question call is recorded and then denied (`Permission to use AskUserQuestion has been denied because Claude Code is running in don't ask mode`), so that mode cannot be used.
- Run F, `--permission-mode manual` with the other tools pre-approved through `--allowedTools`: the question screen appears and the driver answers it. The screen the driver saw:

```
  text you receive, and stop. Do not run any other tool, do not invoke any skill or command.
────────────────────────────────────
 ☐ Probe
Keep my wording?
❯ 1. keep my wording
     Keep my wording
  2. keep the draft
     Keep the draft
  3. Type something.
────────────────────────────────────
  4. Chat about this
Enter to select · ↑/↓ to navigate · Esc to cancel
```

The transcript lines for run F (tool call, then the answered result):
```
[{"tool":"AskUserQuestion","input":"{\"questions\":[{\"header\":\"Probe\",\"question\":\"Keep my wording?\",\"options\":[{\"label\":\"keep my wording\",\"description\":\"Keep my wording\"},{\"label\":\"keep the draft\",\"description\":\"Keep the draft\"}],\"multiSe"}]
[{"tool_result":"Your questions have been answered: \"Keep my wording?\"=\"keep my wording\". You can now continue with these answers in mind."}]
```

Answer supplied: yes. The first option of the question screen is selected with Enter. The shipped rule lists "keep my wording" as the first choice (`src/superclaude/skills/sc-issue-protocol/refs/create.md:86`), and the screen shows the options in the order the model gives them, so the driver reads the question screen and sends the number key of the option whose label is "keep my wording" (Enter when it is option 1). When no answer comes (run H, the same probe with the driver told not to answer): the question screen was seen at the fourth poll, the driver pressed no key for 25 more seconds, and the screen after the wait was still the question screen (saved as `dry-H.after-wait-screen.txt`: the same header, question and four choices, "Enter to select"). The transcript of run H holds the user prompt and the `AskUserQuestion` tool call and no tool result, so the session waits at the question and an unanswered question is visible in the transcript as a tool call without a result. The driver gives up after its timeout and records "unanswered".

## 4. How each GitHub write path is blocked in a run

| Write path | Control | Evidence |
|---|---|---|
| `gh` | a stub `gh` first on `PATH` (the dry run stub exits 97 and logs; the fake `gh` of Task 5 replaces it) | `env -i PATH=<stub>:... gh auth status` printed `gh stub: blocked call: auth status` and `rc=97` |
| `gh` credentials | `GH_TOKEN`, `GITHUB_TOKEN` and `SSH_AUTH_SOCK` are not passed (the run environment is built with `env -i` and an explicit list), `GH_CONFIG_DIR` points at an empty folder, `HOME` is the isolated home that holds no `~/.config/gh` | the real home does hold `~/.config/gh/hosts.yml`; the isolated home does not |
| `git` credentials | `GIT_CONFIG_GLOBAL=/dev/null`, `GIT_CONFIG_NOSYSTEM=1`, `GIT_TERMINAL_PROMPT=0`; the real global git configuration holds no credential helper (`git config --global --list` showed none) | see the command output below |
| `git push` | the run clone's push URL for `origin` is `invalid://blocked-no-push`, and its `pre-push` hook exits 1 | `git push origin HEAD` printed `fatal: remote helper 'invalid' aborted session` |
| fetch URL | `origin` keeps the GitHub fetch URL `https://github.com/IronbellyOrg/IronClaude`, because `scripts/origin_repo.py` needs a GitHub-form fetch URL (it stops with `E-NO-ORIGIN` otherwise) | `git remote -v` below |
| MCP | `--strict-mcp-config` with no `--mcp-config`: no MCP server loads | the init event of the print runs lists no MCP tool |
| model gateway | not a GitHub path; the isolated home holds no login, so the gateway variables are passed by reference (`ANTHROPIC_AUTH_TOKEN`, `ANTHROPIC_BASE_URL`, `ANTHROPIC_MODEL` and the three default model variables) | the dry runs authenticated through them (return code 0, model `claude-gw-tier1a[1m]`) |

An unexpected finding: Claude Code itself calls `gh auth token` during start-up. The stub log from the dry runs:

```
2026-11-26T17:19:15Z auth status
2026-11-26T17:21:31Z issue list -R anthropics/claude-code --author @me --state closed --search closed:>2026-10-27 --json number,title,closedAt,stateReason --limit 30
2026-11-26T17:21:31Z auth token
2026-11-26T17:23:46Z auth token
```

Task 5 decision: the fake `gh` answers `auth token` with a non-zero exit (no token) and logs it as a start-up read, never as an unknown call, so it does not trigger the matrix-wide stop. Every other call it does not know still exits non-zero and does stop the matrix.

Commands and real output for the git controls:
```
$ git config --global --list --show-origin | grep -iE "credential|insteadof"   (real home)
(none)
$ git -C probe-clone remote -v
origin	https://github.com/IronbellyOrg/IronClaude (fetch)
origin	invalid://blocked-no-push (push)
$ git -C probe-clone push origin HEAD
git: 'remote-invalid' is not a git command. See 'git --help'.
fatal: remote helper 'invalid' aborted session
```

The real `gh` is `/home/coder/.local/bin/gh`; the run `PATH` is the stub folder, the Node folder, `/usr/local/bin`, `/usr/bin` and `/bin`, so it is not on it. A model that called it by absolute path would still have no credential (no token variable, empty `GH_CONFIG_DIR`, isolated home), which is a second layer, not the control.

### The read-only fork-activity check

Run by the harness process only (never by a model), with the real credentials, GET calls only:

```
$ gh api "repos/IronbellyOrg/IronClaude/issues?state=all&sort=created&direction=desc&per_page=1" --jq ".[0]|{number,created_at,title}"
{"created_at":"2026-11-26T17:25:48Z","number":894,"title":"feat(jev-611): offline harness for the Jev versus keyword table comparison"}
$ gh api "repos/IronbellyOrg/IronClaude/issues/comments?sort=created&direction=desc&per_page=1" --jq ".[0]|{id,created_at}"
{"created_at":"2026-11-26T17:25:59Z","id":7199007159}
```

The fork is not quiet: another session created an issue and a comment during the minutes of this task, so "any change in fork activity" cannot be the stop rule on its own. Decision (this answers the unattributed-activity gap): each run description carries a unique synthetic marker (`qev-<run name>`, appended to the description). After a run the check reads, with GET calls, the issues updated since the run start (`issues?state=all&since=<start>`), the issue comments since the start (`issues/comments?since=<start>`) and the branch list, and looks for the marker in titles and bodies and for new branches named after the run. A hit is an attributed write: it stops the matrix at once. The plan's stop rule is "a change in fork activity", so activity that carries no marker is not ignored either: the check lists every unattributed issue, comment and branch (number or id, author, creation time, title or first line) in the run's `summary.json` and the run script writes a `pending-review` file; no later run starts until the orchestrator has read each listed item between runs, and a listed item that could have come from a run (for example a comment on an existing issue, or a branch with another name, created within the run's time window and not by another visible session) stops the matrix and is reported to the lead. Only an item that plainly belongs to another session's work (its own title and content, unrelated to the run) is cleared, and the clearing is written next to the list. This keeps the plan's stop rule, with the orchestrator, not the script, deciding that unmarked activity is someone else's.

## 5. The scripts folder of the skill

Command: `ls -1 src/superclaude/skills/sc-issue-protocol/scripts/`, and a count of `create_issue.py` and `issue_logger.py` in it:

```
clickup_claim.py
orca_worktree.py
origin_repo.py
matches for create_issue.py or issue_logger.py: 0
```

Neither file exists, so the false facts of the contradiction runs in Tasks 6 to 8 are false.

## 6. The files a run must load, with their sha256

Command: `sha256sum` of every file a create run can read, taken from `src/`, from the seeded home and from the user's installed copy. The list is every file of `src/superclaude/skills/sc-issue-protocol/` (the skill, its refs, templates and scripts), the three workers, `commands/issue.md`, `commands/analyze.md` (the workers run `/sc:analyze`) and `skills/sc-adversarial-protocol/SKILL.md` (the deep flag debate). Each line ends with whether the seeded copy equals `src/` and whether the installed copy does:

```
2999717d44ecbab240016cfab6fe1a90611490ddf85156bc599b2d0b9f47fbbc  src/superclaude/skills/sc-issue-protocol/SKILL.md  seeded-equals-src=yes  installed-equals-src=no
ce0e795f89b88273dc4d5d8727ee5d532967fb258d366617b05fcce26743ed76  src/superclaude/skills/sc-issue-protocol/refs/chains.md  seeded-equals-src=yes  installed-equals-src=yes
b07c5c867c16995a153fce8783f523c71fc29c7ed5f5d4243cbd6df44dc76a71  src/superclaude/skills/sc-issue-protocol/refs/claim.md  seeded-equals-src=yes  installed-equals-src=no
56c889ba34542b0c1c5918d40b5c9f1954ab00b7dce0b5df2ff23a7daf30141b  src/superclaude/skills/sc-issue-protocol/refs/create.md  seeded-equals-src=yes  installed-equals-src=no
21417aa57aedb2aed199adc44171727f5d39c1cf38a6b92a0f05383dddb7ed55  src/superclaude/skills/sc-issue-protocol/refs/labels.md  seeded-equals-src=yes  installed-equals-src=yes
3ec58fa51e7646b655f0c8d1e20fbab0f8276b12d96f19358b081b38e4c06792  src/superclaude/skills/sc-issue-protocol/refs/tiers.md  seeded-equals-src=yes  installed-equals-src=yes
8cf366559283f770cdf367e83d7c97e3000101ae6ba86e39b9f2f266c313fff0  src/superclaude/skills/sc-issue-protocol/scripts/clickup_claim.py  seeded-equals-src=yes  installed-equals-src=yes
7817ae714b1182b4468d6baf0e12a8196f00064867bf3770a7d9b2314ec42bae  src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py  seeded-equals-src=yes  installed-equals-src=yes
47bd0d899aaa2a1b03b2fe2f297118c99850a3a15a292794270337475916cf0d  src/superclaude/skills/sc-issue-protocol/scripts/origin_repo.py  seeded-equals-src=yes  installed-equals-src=yes
36c22848edb33ed8e81f04d83e8a1427fecee11474dc12ff964efdcecbc23f50  src/superclaude/skills/sc-issue-protocol/templates/accuracy-check-comment.md  seeded-equals-src=yes  installed-equals-src=yes
fbb661f42cf433e47a5a7d92f4c62c3841b2f30df5ae90d963576d39837695ca  src/superclaude/skills/sc-issue-protocol/templates/claim-comment.md  seeded-equals-src=yes  installed-equals-src=yes
3ae8241bb81bfae9ebb3d88f5e80789f1ce6392da613d9416d7998bb586349b0  src/superclaude/skills/sc-issue-protocol/templates/create-review-comment.md  seeded-equals-src=yes  installed-equals-src=yes
f4bbd36fbcf54fa5af776dcad2dcd0903559f4bffe860305719c6fe21b403738  src/superclaude/skills/sc-issue-protocol/templates/description.md  seeded-equals-src=yes  installed-equals-src=yes
1abf40eeee2342401b85b042f858f6aaa88aaa5ebc97c80eb750e8912f9c5967  src/superclaude/skills/sc-issue-protocol/templates/draft-notes.md  seeded-equals-src=yes  installed-equals-src=no
61c89e9dd6065f69503c6998f6854f8acb640f9517d12e2cdc3656205f9094e1  src/superclaude/skills/sc-issue-protocol/templates/flags-decision.md  seeded-equals-src=yes  installed-equals-src=yes
09e5ebe4299a5aa98698e672628a48d2bd2a0e59894b9f8f86deb87725e4fd06  src/superclaude/skills/sc-issue-protocol/templates/issue-bug-complex.md  seeded-equals-src=yes  installed-equals-src=yes
7b888a6117c3ee13d80e76f99b1f09f60d8d4e8618534593d28c426c43918c41  src/superclaude/skills/sc-issue-protocol/templates/issue-bug-simple.md  seeded-equals-src=yes  installed-equals-src=yes
69975483577f75d1deb47cc1f33386626c0a53c9b62d31871dc683d5a9da8454  src/superclaude/skills/sc-issue-protocol/templates/issue-feature-complex.md  seeded-equals-src=yes  installed-equals-src=yes
d0139c56ab85be54925f49f2bb23b7c1b95cf0ab4b60d9a4ca0a1f051f20de06  src/superclaude/skills/sc-issue-protocol/templates/issue-feature-simple.md  seeded-equals-src=yes  installed-equals-src=yes
7447d7f2de28da7125df4dd937282affb2950d120bd28f5a77924eda2166140b  src/superclaude/skills/sc-issue-protocol/templates/issue-summary.md  seeded-equals-src=yes  installed-equals-src=yes
5960e7ceb61ddeda16d115a4f784d345342a5f16164f7c27d2077421e208c038  src/superclaude/skills/sc-issue-protocol/templates/launch-prompt.md  seeded-equals-src=yes  installed-equals-src=yes
b117bb6d20ccb5fcb658686732830b9dac50d1f8b610d43cf2d2682b82d3604f  src/superclaude/skills/sc-issue-protocol/templates/next-steps.md  seeded-equals-src=yes  installed-equals-src=yes
07cc451bcadf7ca8b7473b3e20ecfb1abcbc952e2c2328d4c2d3819e55f59c34  src/superclaude/skills/sc-issue-protocol/templates/recommend-record.md  seeded-equals-src=yes  installed-equals-src=yes
3acca39b3370b27e088a6b399e0476447da87065c6f7224cf637ea7681c81a1e  src/superclaude/skills/sc-issue-protocol/templates/scout-report.md  seeded-equals-src=yes  installed-equals-src=yes
98ee1838e85d650af9d29d07fa3bc19e7a9931dfd20229745a42a279135e93f2  src/superclaude/agents/issue-worker-t1.md  seeded-equals-src=yes  installed-equals-src=no
0a4397e66cc7348990a078dead1fc8308d3a11abdbead7f60318744a4185e366  src/superclaude/agents/issue-worker-t2.md  seeded-equals-src=yes  installed-equals-src=no
910c9081e725f7fe94799e35274e2ae089443d72cfcc1c91a03103f28967c21a  src/superclaude/agents/issue-worker-t3.md  seeded-equals-src=yes  installed-equals-src=no
8db89806dae11ca6fccba2a3fcd396211792c6356fe15e9df956ff9cc74feadb  src/superclaude/commands/issue.md  seeded-equals-src=yes  installed-equals-src=no
1a10c2f0669fe240f2ccd6f5b2388b9bcf6fb66a9da776ce46f01aaaceeb4b15  src/superclaude/commands/analyze.md  seeded-equals-src=yes  installed-equals-src=yes
b0106b209b3a5fea4ec267b5141a49afe852e8b484968fba5708b994d58687f3  src/superclaude/skills/sc-adversarial-protocol/SKILL.md  seeded-equals-src=yes  installed-equals-src=yes
```

Seeded copies equal `src/` for 30 of 30 files; installed copies equal `src/` for 22 of 30.

This list is the expectation, not the proof. The proof for a real run is its own `read-files.txt`, and the run script (Task 5) compares the hash of every file that the transcripts show was read, not only these, with the hash of the same relative path under `src/` computed at run time, so a file that a run reads and that is missing from this list (for example a reference file of the adversarial skill in a deep run) is still checked.

## 7. The dry runs (B-1)

The dry runs happened before any write block of Task 5 existed, so they ran in the environment that Task 4 builds by hand:

- Environment: `env -i` with an explicit list. `HOME=/tmp/createQuestionEv-scratch/home`, `CLAUDE_CONFIG_DIR=/tmp/createQuestionEv-scratch/home/.claude`, `XDG_CONFIG_HOME=.../home/.config`, `GH_CONFIG_DIR=.../home/.config/gh-empty` (empty), `GIT_CONFIG_GLOBAL=/dev/null`, `GIT_CONFIG_NOSYSTEM=1`, `GIT_TERMINAL_PROMPT=0`, `PATH=/tmp/createQuestionEv-scratch/stubbin:/opt/nvm/versions/node/v24.22.2/bin:/usr/local/bin:/usr/bin:/bin`, the model gateway variables by reference. `GH_TOKEN`, `GITHUB_TOKEN` and `SSH_AUTH_SOCK` are unset (not in the list; `env -i` drops them). `gh` is the stub (`stubbin/gh`, exit 97). The working directory is `/tmp/createQuestionEv-scratch/probe-clone`, an empty git repository whose `origin` fetch URL is the fork and whose push URL is `invalid://blocked-no-push`.
- Run H is run F with the driver told not to answer (section 3). Print-mode command (runs A, B, C, D differ only in the options noted in section 3): `claude -p "<probe>" --output-format stream-json --verbose --permission-mode dontAsk --permission-prompts none --allowedTools "AskUserQuestion" --strict-mcp-config --no-session-persistence`.
- Interactive command (runs E and F): `claude --permission-mode <dontAsk|manual> --allowedTools "Read Write Edit Task Skill Bash Glob Grep" --strict-mcp-config` in `tmux`, started through `/tmp/createQuestionEv-scratch/launch.sh` with the same `env -i` list.
- Probe prompt of runs A to F (it makes one question tool call and never invokes `/sc:issue`): `Call the AskUserQuestion tool exactly once with one question: header "Probe", question "Keep my wording?", options "keep my wording" and "keep the draft" (multiSelect false). Then print the answer text you receive, and stop. Do not run any other tool, do not invoke any skill or command.`
- Probe prompt of run G (loads a skill, never runs a command): `Use the Skill tool once to load the skill named sc-issue-protocol, then reply with only the word loaded and stop. Do not run /sc:issue or any command, and do not use any other tool.`
- Result: no dry run wrote to GitHub. The stub log in section 4 holds the only `gh` calls (my stub test and Claude Code's own `gh auth token`).

## 8. Decision

Plan rule: a dry print-mode run that shows no `AskUserQuestion` event makes this section a stop report. The stop report, then the reply, follow.

### Stop report

- Not available: `AskUserQuestion` in print mode (this build offers it in no print-mode option tried, runs A to D).
- What works instead: an interactive session in `tmux` (run F) shows the question screen, records the call and its answer in the transcript, and a driver can answer it.
- Revised estimate: the run script drives `tmux` instead of a streamed print run. Each of the nine runs is one interactive session (quick and standard runs a few minutes, deep runs longer because of the extra worker and the flag debate); the total is of the order of an hour of wall time plus gateway model tokens for nine create runs and their worker subagents, and the harness is one more script (the tmux driver and a transcript reader) than the print design.
- Phase 1 alone: the notes-contract tests of Phase 1 are already written and could ship alone (46 tests, `tests/skills/test_issue_create_question_scenarios.py`); without the runs, acceptance criteria 2 and 5 stay "partly evidenced" and the pull request uses `Refs #834` (as the plan already says).
- Question for the lead: may the controlled runs use an interactive `tmux` session in place of print mode, since print mode cannot show the question?

### Reply recorded

Clay's rule of 26 Nov 2026 (typed in by the lead): do not stop to ask unless something is ambiguous or two sources conflict; answer what has an obvious recommendation and record it in the Decided block and the pull request body. The obvious answer here is yes: run F shows the interactive route reproduces the question screen, the recorded call and the supplied answer, and every write control of section 4 holds in it. The answer is recorded in `.dev/issues/834/issue-summary.md` (Decided block) and goes into the pull request body.

### Decision: proceed

- Loading option: the isolated home seeded from `src/` (section 2).
- Observation method: the interactive session transcript under the isolated home (every tool call, including `AskUserQuestion`, `Skill`, `Task` and `Bash` calls, and their results), read by the run script after the run; questions are counted from `AskUserQuestion` tool calls in the transcripts, posts from the fake `gh` log.
- Answer: supplied by the tmux driver through the question screen (section 3); a run whose driver found no question screen is recorded "no question asked", and a question screen that could not be answered is recorded "unanswered" and counts as "partly evidenced".
- Write controls: section 4, plus the fake `gh` and the attributed fork-activity check of Task 5.
- Stop conditions (the plan's, with the two refinements found here): an unknown `gh` call (Claude Code's own `gh auth token` is a known start-up read), an uninterceptable write, a change in fork activity (an attributed change stops the matrix at once; an unattributed one is listed and held for the orchestrator's review before the next run, as the end of section 4 says), or a run that read an installed copy of the skill or workers. Any of them stops every remaining run and is reported before another run starts.
- Not shown here (stated, not hidden): where worker subagent activity is recorded in the transcripts (section 2), and whether the isolated home needs a one-time onboarding seed for each run (the seed file used in runs E and F is `home/.claude.json`, copied from the key names `hasCompletedOnboarding`, `theme` and a trusted-project entry for the run clone).

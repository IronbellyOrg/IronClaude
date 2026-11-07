## 1. Position summary

1. One bash and `jq` script, `launch-level-guard.sh`, on two events only: UserPromptSubmit (bind and approve) and PreToolUse (decide). No UserPromptExpansion, no SessionStart, no shell parser.
2. D1: the launch prompt starts with `[sc-launch:v1:<nonce>]`. The hook moves `pending/<nonce>` to `sessions/<session_id>`. That file holds one word: `worktree`, `full` or `full-submit`.
3. D2: the store sits outside the worktree. Protection is a deny rule on any call that names the store, the hook or the settings files. File modes and HMAC are rejected: same OS user.
4. D3: approval is a second, empty file, made only by UserPromptSubmit (whole-prompt `approved`, or a typed `/sc:implement` or `/task`). It unlocks starting implementation and nothing else.
5. D4: a Bash command is cut into words and scanned. Gated: `git commit|push|merge`, `gh ... merge|create`, `orca send|launch|create`, `claude`/`ccsession` launches. Over-matching is accepted.
6. Cut: JSON records, expiry and clean-up, locking, a cwd fallback, edit gating at `worktree`, MCP and Workflow coverage, approval expiry. Section 2 says what each cut leaves open.
7. Ship gate: observation OB-H1 (subagent session id, Skill key, typed slash event) passes before any real `full` launch. Guardrail for a drifting agent, not a sandbox.

## 2. Threat model and residual risks

**T1** is an honest agent that drifts: the prompt is its only limit today. **T2** is an agent that tries obvious workarounds: `bash -c`, `env`, `command git`, `/usr/bin/git`, a subagent, a fresh `claude -p`, typing `approved` into its own terminal, editing the state file or the hook settings. **T3**, a hostile agent, is not designed against.

Harness facts used: a PreToolUse exit 2 holds with permission prompts off (VERIFIED V3); hooks run inside subagents (VERIFIED V4); a hook that crashes or times out does not block (VERIFIED V8), so fail-closed lives inside the script and only for governed sessions.

| Cut (what I deleted) | What that leaves uncovered |
|---|---|
| UserPromptExpansion event | If a typed slash command never reaches UserPromptSubmit, the typed route gives no approval; `approved` still works |
| JSON record (issue, repo, path) | Messages do not name the issue; no check of the launch worktree |
| Expiry, clean-up, SessionStart, `flock` | Stale files pile up; a person removes them (`mv` and `touch` are atomic) |
| cwd fallback for subagents | Nothing if U1 holds; if not, OB-H1 stops the ship (section 7) |
| Real shell parsing | Variables, quote splicing, aliases, a script file written with Write and then run |
| Source-edit gating at `worktree` | The agent can implement by editing files directly |
| MCP, Workflow, Monitor coverage | An MCP server that runs git or a shell |
| Approval expiry or plan binding | A stale or ambiguous `approved` unlocks implementation |
| HMAC, mode bits, root directory | Deleting the store in a disguised command |
| `--repo IronbellyOrg/IronClaude` check | A `gh` call aimed at another repository (owner decision O-3) |

Residual by nature: a human choosing `claude --bare`, `--settings` or `disableAllHooks` (hooks can be switched off, VERIFIED V11; `--bare` UNVERIFIED, U6). A session with a new id (`--fork-session`, VERIFIED V14; `/clear`, UNVERIFIED N3) becomes ordinary. Input injection other than `orca terminal send` (for example `tmux send-keys`). A session never bound looks like an ordinary one.

## 3. Components and files (proposed names)

| Item | Detail |
|---|---|
| `src/superclaude/hooks/scripts/launch-level-guard.sh` | The only new code. Target size about 150 lines, no awk |
| `src/superclaude/hooks/hooks.json` | Two entries at user level, so subagents are covered (V4). UserPromptSubmit, no matcher, timeout 3. PreToolUse, timeout 3, matcher `Bash\|Skill\|Agent\|Task\|Edit\|Write\|NotebookEdit\|Cron.*\|Schedule.*` (regex alternation is already used in this file) |
| Script list | Add the script to `_FRESHNESS_SCRIPTS` (named in `codebase-context.md`), which `make verify-sync` checks |
| `tests/hooks/test_launch_level_guard.py` | Real script, JSON on stdin, temporary `HOME`, like `test_block_bare_python.py` |
| Store `~/.claude/state/launch-level/{pending,sessions}/` | Per-session state convention; `.claude/settings.json` unchanged |

Interface requests to the claim feature (not built here): **C1** before launch, write `pending/<nonce>` containing one word (`worktree`, `full`, `full-submit`; `none` launches nothing, so no file). **C2** the `--prompt` starts with `[sc-launch:v1:<nonce>]`, nonce 32 hex characters, new for every launch. **C3** `pipeline.json` stays documentation only; the hook never reads it (FR-31 amended). The claim script should also refuse to launch when `jq` is missing.

## 4. Session identity (D1) and where state lives (D2)

| Option | Rename survival | Re-claim isolation | Forgery | Interface cost |
|---|---|---|---|---|
| (a) Marker plus nonce bound to `session_id` | Yes: the id holds no path | Yes: new nonce, new session | Needs a user prompt or a write to `pending/` | Two small claim changes |
| (b) Environment variable from the shim | Yes | Yes | Hook environment unknown (UNVERIFIED) | Changes the shim, out of scope |
| (c) Record keyed by worktree path or branch | No | No: a person's own session there becomes governed | Easy | One write |

**Position: (a), simplified.** Reject (c) because it governs a place instead of a session. Reject (b) because it needs the shim.

Binding, at UserPromptSubmit: take the first `\[sc-launch:v1:([0-9a-f]{32})\]` in the prompt; if `pending/<nonce>` exists and `sessions/<sid>` does not, `mv` the first to the second. `mv` is atomic, so a nonce works once. `session_id` must match `[A-Za-z0-9._-]+`, or the hook does nothing. `--resume` keeps the id (VERIFIED V14), so a resumed session stays governed. UserPromptSubmit carries the prompt text (VERIFIED V6); that it fires before the first model call for a command-line prompt is UNVERIFIED (U8), observed in OB-H2.

| File | Written by | Content |
|---|---|---|
| `pending/<nonce>` | claim script | one word |
| `sessions/<sid>` | hook (`mv`) | the same word |
| `sessions/<sid>.ok` | hook (`touch`) | empty: approval |

The level is read only from `sessions/<sid>`. Tamper rule (D2): in a governed session, any matched call whose raw input contains a guard-surface token is blocked (T1). Tokens: the store path, `disableAllHooks`, `.claude/settings`, `.claude/hooks`. The script assembles the store name from two parts, so its own source and tests do not contain the token. Release is `rm sessions/<sid>*` by a person.

## 5. Decision table (rows: tool call patterns; columns: worktree, worktree after approval, full, full with submit)

Cell notation: ALLOW, or BLOCK plus message id (section 11).

| Tool call pattern | worktree | worktree after approval | full | full with submit |
|---|---|---|---|---|
| Skill `sc:implement`, `sc-implement-protocol`, `task` | BLOCK W1 | ALLOW | ALLOW | ALLOW |
| Skill `sc:pr-submit`, `sc-pr-submit-protocol` | BLOCK W2 | BLOCK W2 | BLOCK W2 | ALLOW |
| `git commit` | BLOCK W2 | BLOCK W2 | BLOCK W2 | ALLOW |
| `git push` of a feature branch | BLOCK W2 | BLOCK W2 | BLOCK W2 | ALLOW |
| `git push` naming master, main, `--all`, `--mirror`, or run with HEAD on master, main or detached | BLOCK M1 | BLOCK M1 | BLOCK M1 | BLOCK M1 |
| `git merge`, `gh pr merge`, `gh api .../merge` | BLOCK M2 | BLOCK M2 | BLOCK M2 | BLOCK M2 |
| `gh pr create`, `gh issue create`, any `gh <group> create` | BLOCK W2 | BLOCK W2 | BLOCK W2 | ALLOW |
| Other git (status, add, log, diff, fetch, checkout, stash, rebase) | ALLOW | ALLOW | ALLOW | ALLOW |
| Other skills (workflow, troubleshoot, load) | ALLOW | ALLOW | ALLOW | ALLOW |
| Agent or Task, normal | ALLOW | ALLOW | ALLOW | ALLOW |
| Agent or Task with remote isolation | BLOCK E1 | BLOCK E1 | BLOCK E1 | BLOCK E1 |
| Bash `orca` with send, launch, create, rm; `claude` or `ccsession` with a launch flag | BLOCK E2 | BLOCK E2 | BLOCK E2 | BLOCK E2 |
| Cron or Schedule tools | BLOCK E3 | BLOCK E3 | BLOCK E3 | BLOCK E3 |
| Any matched call naming a guard-surface token | BLOCK T1 | BLOCK T1 | BLOCK T1 | BLOCK T1 |
| Edit, Write, NotebookEdit elsewhere | ALLOW | ALLOW | ALLOW | ALLOW |
| State unreadable or invalid; `jq` missing; Skill name unreadable | BLOCK F1/F2/F3 | same | same | same |

Read, Grep, Glob and MCP tools never reach the hook. This table is the data for the parametrised test (section 12), so table and code cannot drift.

## 6. Human approval and human versus agent (D3)

- **Who can create approval.** Only the UserPromptSubmit branch. It is not a tool call, so the agent cannot produce it; the harness gives no origin field on prompts (VERIFIED V6, "also fires on turns Claude Code starts on its own"). The design therefore removes the agent's ways to start a turn: scheduling tools (E3) and `orca terminal send` (E2).
- **What counts.** The whole prompt, trimmed, matches `approved` (any case, optional final `.` or `!`), or begins with `/sc:implement` or `/task` followed by a space or the end. A prompt that merely contains the word does nothing. A prompt with an `agent_id` is ignored (whether the event fires in subagents is UNVERIFIED, N1).
- **Effect.** `touch sessions/<sid>.ok` only when the level is `worktree`. It lifts row 1 of the table and nothing else. Commit, push and `/sc:pr-submit` stay blocked; a person who wants them runs them in their own terminal or relaunches with `--submit`. A typed `/sc:pr-submit` does not approve anything.
- **Duration.** The rest of the session. Rejected: expiry and plan-hash binding (each adds states and clock edge cases). Left open: an `approved` typed before a plan exists, or in answer to a different question.
- **Typed route risk.** A typed slash command fires UserPromptExpansion, not PreToolUse (VERIFIED V5). That it also reaches UserPromptSubmit as typed is the V6 reading, checked in OB-H1. If not, W1 still tells the person to reply `approved`: loud, not silent.

## 7. Subagents and nested subagents

The decision depends only on `session_id`. If a subagent or nested subagent reports the parent's `session_id` (UNVERIFIED, U1), every rule above applies to them with no extra code. `agent_id` matters only to ignore approvals (section 6).

**U1 is a ship gate, not a design branch.** OB-H1 logs a subagent and a nested subagent Bash call. If the ids differ, the contingency (proposed, not built) is to store the launch `cwd` as a second line and treat a call with an `agent_id` and no session file as governed when its `cwd` matches. That adds a wrong case (a person's own session with subagents in the same directory), so it waits for the fact.

The Agent call itself is allowed, because the subagent's own calls hit the same hook. Matcher `Agent|Task` covers either name (UNVERIFIED, U3). One exception: remote isolation (E1), because a remote run leaves the machine and the hooks (UNVERIFIED, N2: the payload key and whether hooks run remotely). Rejected: scanning the subagent prompt for forbidden words, which blocks wording instead of actions.

## 8. Bash and git wrappers (D4)

**Position: tokens, not a parser.** The #357 hook needed 300 lines of awk, three review rounds and still lists nine ceilings (`codebase-context.md` section 2). Over-matching a word is cheaper than parsing.

Steps (one `jq` call, then bash builtins only): (1) `jq` returns the decoded command. (2) Tamper tokens on the raw call. (3) Replace `; & | ( ) { }`, backtick and newlines with a segment marker; replace every character outside letters, digits and `._/=:@+~-` with a space. (4) For each segment, apply the rules.

| Rule | Reads | Result |
|---|---|---|
| git | A token `git` or ending `/git`. Subcommand is the first later word not starting with `-`, skipping the value after `-C` and `-c` | `commit`, `push`, `merge` gated per table |
| push check | On a gated push at submit: the raw command matches `(^\|[^A-Za-z0-9._-])(master\|main)($\|[^A-Za-z0-9._-])`, or has `--all` or `--mirror`; or `git symbolic-ref -q --short HEAD` (timeout 1 s) prints master, main or nothing | M1 |
| gh | A token `gh`. First two non-option words are group and action: `pr merge` is M2; any action `create` is W2 below submit; `api` with an endpoint ending `/merge` is M2 | per table |
| orca | Token `orca` with a later word in `send`, `launch`, `create`, `rm`, `worker-start`, `dispatch`, `task-create` | E2 (agrees with WC-13) |
| claude | Token `claude` or starting `ccsession`, with a later word in `-p`, `--print`, `--resume`, `-r`, `--continue`, `--bare`, `--settings`, `--dangerously-skip-permissions` | E2 |

Covered wrappers: `bash -c`, `sh -c`, `eval`, `env`, `command`, `exec`, `sudo`, `nohup`, `xargs`, `$( )`, backticks, `\git`, `/usr/bin/git`, `NAME=x git`, `git -C dir`, `git -c k=v`, heredoc text that creates a script. Not covered: `$GIT push`, `g""it`, a git alias, a script created with Write and run later, `-C "dir with spaces"`.

Known unwanted blocks: a governed `grep "git push" docs/`, or a commit message that says `git push`. The message tells the agent to reword; only governed sessions see this.

Only `commit` is gated, not `commit-tree`, `update-ref` or `revert`: WC-9 keeps `/sc:implement` snapshots, refs and revert allowed, and I did not read which git commands it runs (UNVERIFIED, N4). OB-H3 at `full` runs a real `/sc:implement`. Rejected: a PATH shim (an agent runs `/usr/bin/git`) and git-level hooks (they cannot tell a person from the agent, `--no-verify` skips them, and they need the claim side).

## 9. Other tools and escape routes (D5)

| Tool or route | Decision | Reason |
|---|---|---|
| Bash | Scanned (section 8) | Main route |
| Skill | Name from `tool_input.skill` or `.name` (UNVERIFIED, U2). Neither present: BLOCK F3 | Fails loudly if the key differs |
| Agent, Task | Allowed except remote isolation | Section 7 |
| Edit, Write, NotebookEdit | Guard-surface tokens only | Cut: gating source edits needs a path rule that separates plan files from source; the agent writes plans, notes and tests legitimately. Owner decision O-1 |
| CronCreate, ScheduleWakeup and similar | BLOCK E3 | Self-started turn could fake `approved`. Tool names UNVERIFIED (U4); the pattern is `Cron.*\|Schedule.*` |
| Monitor, Workflow, MCP tools | Not matched | Cut. A Monitor notification is not a whole-prompt `approved`. MCP: owner decision O-6 |
| `claude -p`, `ccsession`, `orca` | BLOCK E2 | A fresh session is ordinary and would escape |
| Editing settings to remove the hook | BLOCK T1 | The likeliest workaround of a blocked agent |

`@file` mentions fire no tool call (VERIFIED V12), so they need no rule. Raw-text tokens are tested in both `/` and `\/` forms (UNVERIFIED, N5).

## 10. Fail-closed rules and speed (D6)

"Governed" means `sessions/<sid>` exists. After that point the script is default-deny: it exits 2 unless an explicit allow path runs, so any internal error blocks.

| Failure | Ordinary session | Governed session |
|---|---|---|
| No `sessions/` files at all | Exit 0, no `jq` | n/a |
| `jq` missing | Exit 0 if `session_id` (found by a bash regex) has no file | BLOCK F2 |
| Input not valid JSON | Same regex rule | BLOCK F2 |
| Session file unreadable, empty or not one of the three words | n/a | BLOCK F1 |
| Skill name unreadable | n/a | BLOCK F3 |
| Hook times out (3 s) or is killed | Allowed (VERIFIED V8) | Allowed: residual; the only slow step is the 1 s git call |
| Session file deleted | Looks ordinary | Looks ordinary: residual, covered only by the T1 rule |

`onFailure: "block"` is rejected because it also blocks ordinary sessions when the hook breaks (VERIFIED V8, per-hook setting).

Speed (proposed budget, not measured): no governed files on the machine, a few milliseconds, builtins only (`compgen -G`). Ordinary session beside a governed one: one `jq` plus one file test. Governed Bash, even a 100 KB command: one `jq` and string replacements; git runs only on a gated push. The test asserts a median of 20 runs under three times the budget and prints the real numbers (AC-8).

## 11. Block messages

Every message has three lines: "Blocked:" (what), "Why:" (reason), "You can:" (next step). Wording:

| Id | Text |
|---|---|
| W1 | Blocked: starting the implementation. Why: this session was launched to stop at an approved plan. You can: read the plan, then reply `approved` here, or type the implement command yourself. |
| W2 | Blocked: a commit, push, pull request or `/sc:pr-submit`. Why: at this launch level a person sends work out. You can: do it in your own terminal, or claim again with `--pipeline full --submit`. |
| M1 | Blocked: pushing to master or main, or pushing every branch. Why: no launch level allows it. You can: push the feature branch by name. |
| M2 | Blocked: a merge. Why: no launch level merges; a person reviews and merges. You can: leave it for the reviewer. |
| E1 | Blocked: a subagent on a remote machine. Why: the safety checks run only on this computer. You can: start a local subagent. |
| E2 | Blocked: starting another agent session or typing into a terminal. Why: that would skip this session's launch level. You can: ask the person who claimed the issue. |
| E3 | Blocked: scheduling a later turn. Why: a scheduled turn can look like a person typing `approved`. You can: finish now and tell the person what is waiting. |
| T1 | Blocked: touching the launch-level files or the hook settings. Why: they decide what this session may do. You can: ask the person; in their own terminal they can run `rm <session file path>` to release the session. |
| F1 | Blocked: this session's launch level file is unreadable or invalid. Why: I cannot tell what is allowed. You can: release the session as in T1, or claim again. |
| F2 | Blocked: `jq` is missing or the call could not be read. Why: I cannot check it. You can: install `jq`, or release the session as in T1. |
| F3 | Blocked: I could not read which skill was called. Why: I cannot check it. You can: report this; release the session as in T1. |

## 12. Test plan (D7)

All automated cases run the real script, a temporary `HOME`, and a helper `bind(level)` that writes `pending/` and sends the marker prompt. Cases marked (m) are generated from the section 5 table, one per cell.

| AC | Automated cases | Observed |
|---|---|---|
| AC-1 | `test_matrix_worktree` (m), `test_worktree_blocks_implement_until_approved`, `test_worktree_allows_plan_skills` | OB-H3 at `worktree` |
| AC-2 | `test_matrix_full` (m), `test_matrix_submit` (m), `test_submit_allows_commit_and_feature_push` | OB-H3 at `full`, `full-submit` |
| AC-3 | `test_approve_by_reply`, `test_approve_by_typed_implement`, `test_approve_by_typed_task`, `test_approve_needs_whole_prompt`, `test_approve_ignored_with_agent_id`, `test_approval_never_unlocks_commit`, `test_agent_has_no_approval_route` (E2, E3 cases) | OB-H1: typed slash reaches UserPromptSubmit |
| AC-4 | `test_ordinary_never_blocked` (no state; other sid bound), `test_bash_skill_agent_covered`, `test_subagent_call_blocked`, `test_nested_subagent_blocked`, `test_remote_isolation_blocked` | OB-H1: subagent and nested ids |
| AC-5 | `test_garbage_level_blocks`, `test_unreadable_state_blocks`, `test_no_jq_blocks_governed_only`, `test_store_tamper_bash`, `test_store_tamper_write`, `test_settings_edit_blocked`, `test_escaped_slash_token`, `test_rename_cwd_still_governed`, `test_reclaim_new_nonce_new_session`, `test_nonce_single_use`, `test_two_sessions_isolated`, `test_resume_same_sid` | OB-H2 |
| AC-6 | `test_no_level_permits_merge`, `test_push_main_variants` (origin main, `HEAD:main`, `refs/heads/master`, `--all`, `--mirror`, bare push on master, detached HEAD, in a fixture repo), `test_wrappers_at_every_level` | OB-H3 push attempt |
| AC-7 | `test_every_message_has_three_parts`, `test_each_id_reachable` | OB-H4 |
| AC-8 | all of the above plus `test_speed_no_state`, `test_speed_ordinary_with_governed_present`, `test_speed_large_bash` | OB-H5 |

Observed: **OB-H1** a throwaway logging hook records real payloads (Skill key, subagent and nested ids, typed slash on UserPromptSubmit, Agent `isolation`). **OB-H2** the session is bound before its first tool call. **OB-H3** the addendum's OB-5 to OB-9, plus one attempt per level to break the rule. **OB-H4** read the wording of a live block. **OB-H5** time the hook on a real machine. OB-H1 and OB-H2 pass before the first real `full` launch.

## 13. Acceptance criteria map

| AC | Sections | Tests (section 12 row) |
|---|---|---|
| AC-1 plan stop | 5, 6, 11 | AC-1 |
| AC-2 full, submit | 5 | AC-2 |
| AC-3 approval | 6 | AC-3 |
| AC-4 governed only, tools, nested | 4, 7, 9 | AC-4 |
| AC-5 state, tamper, rename, re-claim | 4, 10 | AC-5 |
| AC-6 no merge, no main push | 5, 8 | AC-6 |
| AC-7 plain words | 11 | AC-7 |
| AC-8 tests, speed | 10, 12 | AC-8 |

## 14. Order of work

1. OB-H1 with a throwaway logging hook on a real launch; record the answers to U1, U2, U3, U8 and N1, N2.
2. Write the test matrix from section 5, then the script until it passes.
3. Register in `hooks.json`, add to the script list, run `make sync-dev` and `make verify-sync`.
4. Claim side adds C1 to C3 (a separate sprint); amend FR-31 in the addendum.
5. OB-H2 and OB-H3. Only then use `full` or `--submit` on a real issue.

## 15. Open decisions for the owner

- **O-1** Gate source edits at `worktree` (allow only paths under `.dev/`)? Default: no.
- **O-2** Add `/sc:task` and similar to row 1? Default: only `/sc:implement` and `/task`, as the issue says.
- **O-3** At `full-submit`, require `--repo IronbellyOrg/IronClaude` on `gh`? Default: no.
- **O-4** Is `--submit` allowed if a launched session carries a worker preamble (WC-9, U7)?
- **O-5** Who removes old session files: a person (default) or the claim script on re-claim?
- **O-6** Add `mcp__.*` to the matcher with a rule for git or shell servers? Default: no.
- **O-7** Accept the script-file gap, or later add a git-level pre-push hook as a second layer?

## 16. UNVERIFIED items and how the design tolerates each

| Item | Question | Tolerance |
|---|---|---|
| U1 | Subagent `session_id` equals the parent's | Ship gate OB-H1; contingency in section 7 |
| U2 | Skill payload key | Read `skill` then `name`; neither present means BLOCK F3 (loud) |
| U3 | `Agent` also called `Task` | Matcher lists both |
| U4 | Cron and schedule tool names; `!` shell escape and Monitor effect on prompts | Pattern `Cron.*\|Schedule.*`; approval needs a whole-prompt match |
| U5 | Typed slash reaches UserPromptSubmit mid-turn | `approved` always accepted; W1 names both routes |
| U6 | `claude --bare` skips hooks | Human-chosen; residual |
| U7 | Worker preamble forbids `--submit` | Owner decision O-4; the hook ignores the preamble |
| U8 | UserPromptSubmit fires before the first model call | OB-H2; a failed bind leaves the session ordinary, so it is a ship gate |
| N1 | UserPromptSubmit in subagents | Ignored when `agent_id` is present |
| N2 | Agent `isolation` key, remote hooks | Key absent: E1 never fires; residual |
| N3 | `/clear` changes `session_id` | Residual; a person types it |
| N4 | Git commands `/sc:implement` runs | Only `commit`, `push`, `merge` gated; OB-H3 |
| N5 | Payload escapes `/` | Tokens tested in both forms |

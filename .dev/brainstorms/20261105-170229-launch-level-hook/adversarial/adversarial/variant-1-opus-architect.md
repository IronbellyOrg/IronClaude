---
variant: 1
persona: architect
focus: maintainability and extension scaffolding
issue: IronbellyOrg/IronClaude#394
status: design only, nothing implemented
---

# Variant 1 (architect): launch-level guard

## 1. Position summary

- One hook script (proposed `launch-level-guard.sh`) with internal layers: router, session resolver, state store, classifiers, policy table, messages. A new level, tool or action is a data row plus a test row, not a rewrite.
- A session is governed only when its first prompt carries a launch marker; the hook binds it to `session_id` once, never unbinds it, and only a human `rm` releases it.
- Every tool call becomes a set of action classes from a closed list; one policy table maps class and level to ALLOW or BLOCK plus a message id.
- Bash text is read by a word-window scanner, not a shell parser. It over-blocks text that only mentions a git action, but only in governed sessions.
- Approval comes only from human prompt events and unlocks implementation only. Merge and push to `master`/`main` are blocked at every level. Broken state falls to the strictest level.

## 2. Threat model and residual risks

Targets (seed A2): **T1**, an honest agent that drifts from `launch-prompt.md`; **T2**, an agent that tries obvious workarounds (`bash -c`, `env`, `command git`, `/usr/bin/git`, `xargs`, an interpreter one-liner, a git alias, editing the guard's state or settings). Out of scope: **T3**, deliberate multi-step evasion. Agent and hook share one OS user, so nothing is truly unwritable.

| Id | Not covered | Why accepted |
|---|---|---|
| R1 | Agent writes a script containing `git push`, then runs it | Scanning file content would block every plan that mentions push |
| R2 | Hook timeout or crash lets the call through | VERIFIED (V8); `onFailure: "block"` would also hit ordinary sessions |
| R3 | Store reached indirectly (`cd ~/.claude/state && rm -r l*`) | Substring rule catches direct names only |
| R4 | Human runs `--fork-session` or `claude --bare` | A fork gets a new id (VERIFIED V14); `--bare` UNVERIFIED (U6). Human choice |
| R5 | Another session types `approved` into this terminal | No prompt origin field (VERIFIED V6); the governed agent cannot run `orca terminal` |
| R6 | GitHub API merge through an unusual URL | Only URLs ending `/merge` are caught |
| R7 | Remote subagent if `isolation` is absent from the payload | UNVERIFIED (U13) |
| R8 | `@file` mentions skip PreToolUse | VERIFIED (V12); reading is not gated |

## 3. Components and files (proposed names)

| Item | Status | Purpose |
|---|---|---|
| `src/superclaude/hooks/scripts/launch-level-guard.sh` | proposed | Only script; handles UserPromptSubmit, UserPromptExpansion, PreToolUse |
| `src/superclaude/hooks/hooks.json` | existing, 3 new entries | All three events, no matcher (the `command_name` form is UNVERIFIED, U9), timeout 5 |
| `Makefile` `_FRESHNESS_SCRIPTS` and the list in `src/superclaude/cli/install_hooks.py` | existing, 1 line each | Required for every script in `scripts/` |
| `tests/hooks/test_launch_level_guard.py` | proposed | Table-driven, same pattern as `test_block_bare_python.py` |
| `~/.claude/state/launch-level/pending/<nonce>.json` | proposed, written by the claim script | Launch record before the session exists |
| `~/.claude/state/launch-level/sessions/<session_id>.json`, `<session_id>.approved` | proposed, written by the hook | Bound state and approval flag |

Layers as shell functions (proposed): `ll_main` (router, owns exit codes), `ll_resolve_session` (ordinary or a session file), `ll_load_state` / `ll_bind` / `ll_approve` (store), `ll_classify_tool` / `ll_classify_shell` (payload to classes), `ll_decide` (policy), `ll_message` (catalogue).

**Action classes:** `IMPL`, `COMMIT`, `PUSH`, `PUSH_REMOTE`, `PUSH_PROTECTED`, `MERGE`, `SUBMIT`, `SUBMIT_REPO`, `ESCAPE`, `TAMPER`, `SKILL_UNKNOWN`, `NONE`. **Effective levels:** `worktree`, `worktree+approved`, `full`, `full+submit`.

**Extension scaffolding.** The policy is one literal block in the script (`CLASS LEVEL DECISION MSGID` per line) read by a `case` lookup; the messages are a second block keyed by id. Tests assert every class has a row for every level and every id has text. A proposed `--classify` argument prints the class set for a payload and exits 0; the harness passes no arguments, so it changes no decision, and classifier tests can run apart from policy tests. Record and marker are versioned (`v: 1`, `sc-launch:v1`); an unknown version fails closed, so v2 can sit beside v1. I reject a separate policy data file: it adds an install path that can go missing.

## 4. Session identity (D1) and where state lives (D2)

**D1 position: launch record plus marker, bound on the first marked prompt (option a).**

1. The claim script writes `pending/<nonce>.json` (`umask 077`, temp name, then `mv`) with `{v, nonce, level, submit, issue, repo, worktree, created_at}` (interface R1).
2. The launch `--prompt` starts with `[sc-launch:v1:<nonce>]`, then the existing sentence (interface R2; FR-23 forbids only a leading `/`).
3. On UserPromptSubmit, for a session with no file whose prompt starts with the marker, the hook runs `mv pending/<nonce>.json sessions/<session_id>.json`. The `mv` is atomic, so a nonce binds at most one session.
4. If the record is absent, unreadable, over 30 minutes old or of unknown version, the hook still creates the session file, with `degraded: true` and level `worktree`. A marker always governs, so stealing a nonce cannot release the launched agent.
5. A marker in a later prompt of a bound session is ignored: no rebind, no downgrade.

Why: rename survival is free (nothing keyed by path); a re-claim gets a new nonce and `session_id`; `--resume` keeps the id (VERIFIED V14). Cost: two small interface items for the claim feature.

Rejected: **(b) environment variable** from the shim, which is out of scope and whose reach into hook processes is unchecked; kept as a v2 channel. **(c) worktree path or git-common-dir plus branch**, which breaks on rename, governs a human's own session in that worktree (AC-4) and confuses re-claims.

**Cwd fallback (designed, off unless an observed check fails).** If OB-H1 shows subagents get a different `session_id` (U1), or OB-H2 shows the first prompt misses UserPromptSubmit (U8), one fallback is switched on: an unbound call whose `cwd` is inside a bound session's `worktree` (or a pending record under 30 minutes old) is treated as that session. One mechanism covers both unknowns.

**D2 position: store under `~/.claude/state/launch-level/`, outside every worktree, plus a deny rule.** It follows the existing per-session state convention and id sanitising. The hook never reads `pipeline.json` (interface R3). Tamper protection is the `TAMPER` class (sections 8, 9). Mode 0600 is hygiene only. Rejected: **HMAC** (the key is readable by the agent, so no gain against T2), **root-owned directory** (install needs root), **read-only mode bits** (the agent can `chmod`; release gets harder).

## 5. Decision table

| Tool call pattern | worktree | worktree after approval | full | full with submit |
|---|---|---|---|---|
| Read, Grep, Glob, other read tools | ALLOW | ALLOW | ALLOW | ALLOW |
| Edit, Write, NotebookEdit, ordinary path | ALLOW | ALLOW | ALLOW | ALLOW |
| Edit, Write, NotebookEdit on store, guard, `.claude/settings*`, `.claude/hooks/`, `.gitconfig`, `.git/config` | BLOCK LL-TAMPER | BLOCK LL-TAMPER | BLOCK LL-TAMPER | BLOCK LL-TAMPER |
| Skill `sc:implement`, `sc-implement-protocol`, `task` | BLOCK LL-IMPL | ALLOW | ALLOW | ALLOW |
| Skill `sc:pr-submit`, `sc-pr-submit-protocol` | BLOCK LL-SUBMIT | BLOCK LL-SUBMIT | BLOCK LL-SUBMIT | ALLOW |
| Skill with no readable name | BLOCK LL-SKILL | BLOCK LL-SKILL | BLOCK LL-SKILL | ALLOW |
| Other Skill; local Agent or Task | ALLOW | ALLOW | ALLOW | ALLOW |
| Agent `isolation: remote`; Workflow; RemoteTrigger; CronCreate; ScheduleWakeup | BLOCK LL-ESCAPE | BLOCK LL-ESCAPE | BLOCK LL-ESCAPE | BLOCK LL-ESCAPE |
| Bash or Monitor: `git commit` | BLOCK LL-COMMIT | BLOCK LL-COMMIT | BLOCK LL-COMMIT | ALLOW |
| `git push` of a feature branch to `origin` | BLOCK LL-PUSH | BLOCK LL-PUSH | BLOCK LL-PUSH | ALLOW |
| `git push` to another remote | BLOCK LL-PUSH | BLOCK LL-PUSH | BLOCK LL-PUSH | BLOCK LL-REMOTE |
| Push naming `master`/`main`, `--all`, `--mirror`; bare push on `master`/`main`/detached HEAD | BLOCK LL-PROTECTED | BLOCK LL-PROTECTED | BLOCK LL-PROTECTED | BLOCK LL-PROTECTED |
| `git merge`, `git pull`, `gh pr merge`, URL ending `/merge`, MCP tool named `*merge*` | BLOCK LL-MERGE | BLOCK LL-MERGE | BLOCK LL-MERGE | BLOCK LL-MERGE |
| `gh pr create` naming the record's `repo` | BLOCK LL-SUBMIT | BLOCK LL-SUBMIT | BLOCK LL-SUBMIT | ALLOW |
| `gh pr create` not naming it | BLOCK LL-SUBMIT | BLOCK LL-SUBMIT | BLOCK LL-SUBMIT | BLOCK LL-REPO |
| MCP tool named `*push*`, `*commit*`, `*create_pull_request*` | BLOCK (class id) | BLOCK (class id) | BLOCK (class id) | ALLOW |
| `orca agent/terminal/dispatch/worker-start/task-create`, `orca worktree create/rm`; `claude` or `ccsession*` plus an option | BLOCK LL-ESCAPE | BLOCK LL-ESCAPE | BLOCK LL-ESCAPE | BLOCK LL-ESCAPE |
| Bash naming store, guard, settings or hooks; `alias.` after `git` | BLOCK LL-TAMPER | BLOCK LL-TAMPER | BLOCK LL-TAMPER | BLOCK LL-TAMPER |
| Other Bash (`git add`, `status`, `diff`, `rebase`) | ALLOW | ALLOW | ALLOW | ALLOW |
| Human types `/sc:implement` or `/task`, or replies `approved` | ALLOW, records approval | ALLOW | ALLOW | ALLOW |

A degraded or corrupt session uses the `worktree` column; approval still works, because it is a human act. A call with several classes is blocked if any is blocked; the shown message is the first in this order: TAMPER, MERGE, PROTECTED, REPO, REMOTE, ESCAPE, SUBMIT, PUSH, COMMIT, IMPL, SKILL.

## 6. Human approval and human versus agent (D3)

Approval is created only by top-level prompt events:

1. **UserPromptExpansion** whose `command_name`, after stripping a leading `/` and `sc:`, is `implement` or `task`. A typed slash command fires this event and a model-called skill does not (VERIFIED V5). This is the harness's only human-versus-agent signal for commands, so it is the primary route.
2. **UserPromptSubmit** whose whole prompt, trimmed and lower-cased, is `approved` (optional `.` or `!`), or whose first line starts with `/sc:implement` or `/task`. Typed slash lines arrive as typed (VERIFIED V6), so this also covers a mid-turn typed command that may not expand (U5).

The hook then touches `sessions/<id>.approved` (atomic, no JSON rewrite). Prompt events never block.

**Unlocks:** `IMPL` only, never COMMIT, PUSH, SUBMIT or MERGE. **Lasts:** until the session file is removed; an expiry would stop work half way and add a clock edge case (O-2).

**Self-started turns** also fire UserPromptSubmit with no origin field (VERIFIED V6). They cannot fake approval because the match is whole-prompt or first-line (notification text never equals `approved` or starts with `/sc:implement`), and the agent's scheduling tools and `orca terminal` are blocked, so it cannot start a turn whose text it chose. Whether `!cmd` or Monitor events reach UserPromptSubmit is UNVERIFIED (U4); the whole-prompt rule makes either answer safe.

Rejected: approval only by relaunch (A10; fails AC-3); approval read from PreToolUse(Skill), which the agent controls; per-run approval, which needs counting state.

## 7. Subagents and nested subagents

User-settings hooks run inside subagents, with `agent_id` and `agent_type` in the payload (VERIFIED V4). So the design enforces at the leaf: each subagent's Skill, Bash and MCP calls go through the same classifiers and session file. The Agent tool is allowed and its `prompt` is never scanned; what a subagent tries is checked when it tries it. Nested subagents need no extra rule, and subagents cannot approve, because they produce no prompt events.

Identity assumes the subagent payload carries the parent's `session_id` (UNVERIFIED, U1); if OB-H1 disagrees, the cwd fallback ships. The tool may also be named `Task` (U3), so both names match. `isolation: remote` is blocked because a remote agent runs where this hook does not; V7 does not list `isolation`, so detection is UNVERIFIED (U13, R7).

## 8. Bash and git wrappers (D4)

**Position: a word-window scanner, no shell parser, no PATH shim, no git-level hooks.** The #357 awk parser took three review rounds and still lists nine ceilings (codebase-context section 2). A word window catches every T2 wrapper because it ignores command position.

`ll_classify_shell`, for Bash `tool_input.command` and Monitor `tool_input.command` (Monitor shape UNVERIFIED, U11):

1. **Segments:** split on newline, `;`, `&`, `|`, `(`, `)`, backtick, `{`, `}`. Quotes do not split segments.
2. **Words:** split on whitespace and `' " $ [ ] , =`. So `bash -c "git push origin main"` gives `bash -c git push origin main`, and `subprocess.run(['git','push'])` gives `git push`.
3. **Git:** for each word with basename `git`, skip options (one value after `-C`, `-c`, `--git-dir`, `--work-tree`, `--namespace`, `--config-env`); the next word is the subcommand. `commit` gives COMMIT; `merge`, `pull` give MERGE; `push` gives PUSH plus the push checks; `config` with an `alias.` word, or `alias.` among git options, gives TAMPER. `git log --grep push` passes, since only the subcommand counts.
4. **Push checks:** PUSH_PROTECTED when a later word is `master`, `main`, `--all`, `--mirror`, or ends `:master`, `:main`, `refs/heads/master`, `refs/heads/main`. When no branch word follows the remote, the hook runs `timeout 2 git -C "$cwd" symbolic-ref -q --short HEAD`; `master`, `main`, failure or detached HEAD gives PUSH_PROTECTED. This is the only subprocess, run only for governed pushes. PUSH_REMOTE when the first non-option word after `push` is not `origin`.
5. **gh:** `gh pr merge` gives MERGE; `gh pr create` gives SUBMIT, plus SUBMIT_REPO unless a word equals the record's `repo`. Any word ending `/merge` gives MERGE.
6. **Escape:** `orca` followed by `agent`, `terminal`, `dispatch`, `worker-start`, `task-create`, or `worktree create`/`rm`; `claude`, `ccsession`, `ccsession-orca` followed by a word starting `-`. This matches WC-13.
7. **Tamper (raw substrings):** `state/launch-level`, `launch-level-guard`, `.claude/settings`, `.claude/hooks`, `disableAllHooks`. Bare `launch-level` is not used, because worktree names like `hook-launch-level-394` contain it.

Accepted over-blocking (A12): `echo "git push"`, a commit message containing `git merge`, `cat ~/.claude/settings.json`; governed sessions only, plain message. Accepted gaps: R1, R3.

`git add` stays allowed: `.dev/tasks/` is always staged, and staging is not committing. `/sc:implement`'s private-index snapshots and `refs/superclaude/implement/` refs are not COMMIT; WC-9 says its per-task commits wait for #326. That it runs no `git commit` today is checked in step 1 of section 14 (U10).

Rejected: **PATH shim** (absolute paths bypass it; needs a launch-environment change). **Git `pre-push` or `reference-transaction` hooks** (the worktree shares hooks with the main checkout and the human's own pushes, and git cannot tell which session called).

## 9. Other tools and escape routes (D5)

| Tool | Treatment |
|---|---|
| Skill | Name from `tool_input.skill // tool_input.name` (UNVERIFIED, U2), leading `/` and arguments stripped; no name gives SKILL_UNKNOWN |
| Agent, Task | Allowed; `isolation: remote` gives ESCAPE |
| Edit, Write, NotebookEdit | Only the TAMPER path check. Source edits at `worktree` are not gated: plans are files, and a write boundary is #322's job (O-1) |
| Monitor | Command scanned as Bash |
| CronCreate, ScheduleWakeup, RemoteTrigger, Workflow | ESCAPE at every level: self-started turns (V6) or work outside this session's hooks. Workflow internals are UNVERIFIED, so blocking is the fewer-edge-case choice |
| MCP tools | Name regex (`merge`, `push`, `commit`, `create_pull_request`); others allowed. PreToolUse fires for MCP tools (VERIFIED V1) |
| `claude -p`, `ccsession`, `orca agent launch` | ESCAPE via Bash (section 8) |

## 10. Fail-closed rules and speed (D6)

1. **Fast path 1 (builtins only):** if `sessions/` and `pending/` are empty (`compgen -G`), drain stdin, exit 0. The usual case on every machine.
2. **Fast path 2:** read `session_id` with a bash regex on the raw JSON (no `jq`), sanitise it, test for `sessions/<id>.json`. Absent and no fallback match: exit 0.
3. **Governed path:** `ERR` and `EXIT` traps turn any unexpected end into exit 2 with LL-BROKEN, because other exit codes do not block (VERIFIED V8).

| Failure in a governed session | Result |
|---|---|
| `jq` missing | Block everything except Read, Grep, Glob: LL-BROKEN |
| Session file unreadable, bad JSON, unknown `v` or level | Level `worktree`, LL-STATE note on any block |
| Marker present, record missing or stale | Bound as degraded `worktree` |
| Skill name unreadable | SKILL_UNKNOWN |
| `symbolic-ref` fails or times out | PUSH_PROTECTED |
| Hook killed at its 5 s timeout | Call goes ahead (VERIFIED V8; R2) |
| Session file deleted | Ordinary; same as a human release; TAMPER blocks direct routes (R3) |

`onFailure: "block"` is not used: it would block ordinary sessions when the hook breaks (VERIFIED V8).

**Budget:** fast path 1 under 10 ms median, fast path 2 under 20 ms, governed under 100 ms (a push up to 2 s). Tests assert medians over 30 runs with a CI margin, and every run under 1 s except the push case, as the #357 tests do.

## 11. Block messages

Each message begins `Launch-level guard: this session was launched by /sc:issue --claim for issue #<N> at level <level>.`, then three parts.

| Id | Blocked | Why | What a human can do |
|---|---|---|---|
| LL-IMPL | Starting `/sc:implement` or `/task` | At `worktree` the agent stops at the plan until a person approves | Read the plan, then type the implement command or reply `approved` |
| LL-COMMIT | `git commit` | Only `--pipeline full --submit` lets the agent commit | Commit yourself after review |
| LL-PUSH | `git push` | Only `--pipeline full --submit` lets the agent push | Push the branch yourself after review |
| LL-REMOTE | Push to a remote other than `origin` | The agent may push only to `origin` | Push elsewhere yourself |
| LL-PROTECTED | Push to `master`/`main`, `--all`, `--mirror`, or from `master`/`main` or a detached HEAD | No launch level may change the main branch | Merge through a reviewed pull request |
| LL-MERGE | Any merge or pull | Only people merge | Review and merge the pull request yourself |
| LL-SUBMIT | `/sc:pr-submit` or `gh pr create` | Opening a pull request needs `--pipeline full --submit` | Run `/sc:pr-submit` in your own session |
| LL-REPO | `gh pr create` without `--repo <repo>` | Without it, gh can open the pull request on the parent repository | Retry with `--repo <repo>` |
| LL-ESCAPE | Starting another agent, a remote agent, a scheduled turn or a workflow | That work would escape this level | Start it yourself if needed |
| LL-TAMPER | Touching the guard's state, the guard, settings, hooks or git aliases | The session must not change its own limits | To release this session, delete its file in `~/.claude/state/launch-level/sessions/` |
| LL-SKILL | A skill call with no readable name | The guard cannot tell if it is allowed | Report it; the harness changed |
| LL-STATE | (note) | The launch record was missing or unreadable, so the strictest level applies | Check `~/.claude/state/launch-level/` |
| LL-BROKEN | Every non-read action | The guard cannot run (`jq` missing or internal error) | Install `jq`, or release the session |

## 12. Test plan (D7)

Automated cases run the real script with `subprocess.run`, JSON on stdin and `HOME` in `tmp_path`, as `tests/hooks/test_block_bare_python.py` does. Proposed fixtures: `make_record`, `bind`, `pre`, `fixture_repo(branch)`. Three groups mirror the layers: classifier (`--classify`), policy (full class-by-level grid), end to end (exit code and stderr).

| Group | Named cases (automated) |
|---|---|
| Levels | `test_worktree_blocks_implement_and_task`, `test_worktree_blocks_commit_push_submit`, `test_worktree_allows_plan_write`, `test_full_allows_implement`, `test_full_blocks_commit_push_submit`, `test_submit_allows_commit_push_pr_submit`, `test_submit_blocks_pr_create_without_repo`, `test_submit_blocks_other_remote` |
| Approval | `test_approval_by_expansion`, `test_approval_by_reply`, `test_approval_slash_first_line`, `test_reply_must_be_whole_prompt`, `test_notification_not_approval`, `test_model_skill_call_not_approval`, `test_approval_never_unlocks_commit` |
| Isolation, subagents | `test_ordinary_session_never_blocked` (every BLOCK payload, unbound id), `test_two_sessions_isolated`, `test_subagent_governed`, `test_nested_subagent_governed`, `test_agent_remote_blocked`, `test_task_alias_name`, `test_skill_name_key_variants`, `test_skill_without_name_blocked` |
| State | `test_bind_consumes_record`, `test_marker_without_record_degraded`, `test_stale_record_degraded`, `test_corrupt_or_unreadable_state_strictest`, `test_unknown_version_strictest`, `test_jq_missing_governed_blocks`, `test_jq_missing_ordinary_allows`, `test_second_marker_ignored`, `test_internal_error_exits_2` |
| Tamper, rename, re-claim | `test_tamper_bash_store`, `test_tamper_edit_settings_and_hooks`, `test_tamper_git_alias`, `test_worktree_name_not_tamper`, `test_rename_still_governed`, `test_reclaim_new_session`, `test_reused_nonce_degraded`, `test_resume_same_id_governed` |
| Merge, wrappers (all levels) | `test_merge_or_protected_blocked` over: `git merge x`, `git pull`, `gh pr merge 5`, `bash -c "git push origin main"`, `sh -c 'git merge x'`, `env GIT_DIR=x git push origin master`, `command git push origin HEAD:main`, `/usr/bin/git push --all`, `git -C /x push --mirror`, `xargs git merge`, a `uv run python -c` subprocess push to `main`, a `curl` PUT to `.../pulls/5/merge`, bare push on `main`, bare push on detached HEAD, MCP `merge_pull_request` |
| Messages | `test_policy_grid_complete`, `test_every_message_id_has_text`, `test_message_has_three_parts` |
| Speed | `test_speed_empty_store`, `test_speed_other_sessions`, `test_speed_governed` |

**Observed:** **OB-H1**, a log-only hook copy records real payloads of a subagent and nested subagent Bash call, a model Skill call, a typed `/sc:implement` expansion, a Monitor call and an Agent call with `isolation` (settles U1, U2, U3, U9, U11, U13). **OB-H2**, after a claim launch the session file exists before the first tool call (U8). **OB-H3**, end to end on a test issue: `worktree` stops at the plan and `approved` unlocks implementation; `full` cannot push; `full --submit` opens a PR on the fork.

## 13. Acceptance criteria map

| AC | Sections | Tests |
|---|---|---|
| AC-1 worktree stops at plan | 5, 6 | Levels, OB-H3 |
| AC-2 full, full with submit | 5, 8 | Levels, OB-H3 |
| AC-3 approval, human versus agent | 6 | Approval |
| AC-4 claim sessions only; tools; nested subagents | 4, 7, 9 | Isolation and subagents, OB-H1 |
| AC-5 uneditable state, fail closed, tamper, rename, re-claim | 4, 10 | State; Tamper, rename, re-claim |
| AC-6 no merge or main push, wrappers | 5, 8 | Merge, wrappers |
| AC-7 plain words | 11 | Messages |
| AC-8 tests and speed | 10, 12 | All groups, Speed |

## 14. Order of work

1. OB-H1 with a log-only hook; grep that `/sc:implement` runs no `git commit` (U10); decide whether the cwd fallback ships.
2. Skeleton: router, fast paths, store, binding, traps; State tests.
3. Classifiers with `--classify`; wrapper tests.
4. Policy and message blocks; grid and message tests.
5. Approval; Approval tests.
6. Registration in `hooks.json`, `_FRESHNESS_SCRIPTS`, `install_hooks.py`; `make sync-dev`, `make verify-sync`; speed tests.
7. Hand record schema and marker (R1, R2) to the claim feature.
8. OB-H2, OB-H3 once launches exist. Until then `full` and `--submit` stay off real issues (addendum section 9).

## 15. Open decisions for the owner

| Id | Question | Recommendation |
|---|---|---|
| O-1 | Gate source edits at `worktree`? | No; #322 owns it |
| O-2 | Approval lifetime | Whole session |
| O-3 | `git pull` as a merge? | Yes |
| O-4 | Force push at `full --submit` | Allow `--force-with-lease`, block `--force` |
| O-5 | WC-9 versus `--submit` (U7) | An `orca agent launch` session has no Task or Dispatch ID, so it is an ordinary session (WORKER-CONTRACT section 1); confirm in OB-H3 |
| O-6 | Ship the cwd fallback | Only if OB-H1 or OB-H2 fails |
| O-7 | Release tool beyond `rm` | Not in v1 |
| O-8 | More `IMPL` skills (`sc:task`, `sc:spawn`) | Add `sc:task`; a one-row change |
| O-9 | Old-file cleanup | Prune pending records over a day old at bind; never prune sessions |

## 16. UNVERIFIED items and how the design tolerates each

| Item | Tolerance |
|---|---|
| U1 subagent `session_id` | Cwd fallback ready; OB-H1 decides |
| U2 Skill input keys | Read `skill`, then `name`; neither gives LL-SKILL, governed sessions only |
| U3 `Agent` or `Task` | Both matched |
| U4 `!cmd`, Monitor, Cron via UserPromptSubmit | Whole-prompt rule; scheduling tools blocked |
| U5 expansion for a mid-turn command | UserPromptSubmit first-line route |
| U6 `--bare`, `--settings` hooks | Residual R4 |
| U7 worker preamble | O-5; the hook never reads the preamble |
| U8 first prompt via UserPromptSubmit | Cwd fallback ready; OB-H2 decides |
| U9 (new) `command_name` form | No matcher; strip `/` and `sc:` |
| U10 (new) `/sc:implement` commits | Checked in step 1; if it does, owner decides whether `full` allows it |
| U11 (new) Monitor `command` field | Missing field means nothing to scan; OB-H1 |
| U12 (new) GitHub MCP tool names | Broad regex; unmatched names residual |
| U13 (new) Agent `isolation` field | Residual R7 if absent |

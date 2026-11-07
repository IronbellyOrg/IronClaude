# Variant 3 (QA): launch-level guard hook for `/sc:issue --claim --pipeline` (issue #394)

Persona: QA. Every rule is written so a named automated test can prove or disprove it; what cannot be automated is marked observed with its procedure.

## 1. Position summary

One bash script, `launch-level-guard.sh` (proposed), registered for PreToolUse (matcher `*`), UserPromptSubmit and UserPromptExpansion.
Governance binds once, at the first UserPromptSubmit, from a pending launch record written outside the worktree by the claim script, matched by a nonce marker in the prompt plus the cwd.
The level then lives in one hook-written file under `~/.claude/state/launch-level/active/`.
Bash is classified by word-window matching with wrapper normalization, not a shell parser; over-matching inside governed sessions is accepted and pinned by a test.
No level allows a merge or a push to `master`/`main`.
Approval comes only from human-keyboard events: a typed `/sc:implement` or `/task` (V5) or a whole-prompt `approved` (V6).
Fail-closed applies only to bound sessions; ordinary sessions pay one file-existence check and are never blocked.
Tests are table-driven over real JSON payloads, plus three observed checks and a speed budget.

## 2. Threat model and residual risks

T1: an honest agent that drifts: reads `launch-prompt.md`, then runs `/sc:implement`, `git commit` or `git push` anyway. Primary target; every rule has a test.

T2: obvious workarounds: `bash -c "git commit"`, `command git push`, `/usr/bin/git`, `env git merge`, `gh pr merge`, deleting state, faking approval, self-started turns, launching a fresh `claude`. Each has a named test.

Not covered:

- A script file written in the worktree and executed, whose body contains `git push`; the scan sees the command string, not file contents.
- Deleting the state files from another terminal. Same OS user owns them (seed Constraints); the deny rule blocks every in-session route naming the store, but a raw `rm` outside succeeds and the session reads as unbound.
- `orca terminal send` typing into the session: indistinguishable from the human (V6, no origin field).
- MCP tools that run shells: they fire PreToolUse (V1) but their inputs are opaque to a word scan.
- `claude --bare`, `--settings` (U6), `--fork-session` (V14), editing settings to disable non-managed hooks (V11): all need the `claude` word or a human flag, and the word is blocked (MSG-ESCAPE), so these reduce to the script-file residual.
- Hosts without `jq`: no enforcement, the fail-open contract of the existing hooks.

## 3. Components and files (proposed names)

| File | Role |
|---|---|
| `src/superclaude/hooks/scripts/launch-level-guard.sh` | the only hook script; event dispatch by payload shape |
| `src/superclaude/hooks/hooks.json` | three new entries: PreToolUse `*` (timeout 5), UserPromptSubmit (3), UserPromptExpansion (3) |
| `~/.claude/state/launch-level/pending/<nonce>.json` | launch record, written by the claim script (R1) |
| `~/.claude/state/launch-level/active/<session_id>.json` | bound record: level, submit, nonce, worktree path, approved |
| `tests/hooks/test_launch_level_guard.py` | table-driven tests, real script, real JSON, temporary HOME |
| `Makefile` `_FRESHNESS_SCRIPTS` | must list the new script or `make verify-sync` fails |

Event dispatch by shape: `tool_name` means PreToolUse, `command_name` means UserPromptExpansion, `prompt` means UserPromptSubmit; a `hook_event_name` field is UNVERIFIED, so nothing depends on it.

Interface owed by the claim feature (requests only): R1 pending record `{level, submit, issue, repo, worktree_real_path, created_at}`; R2 the launch `--prompt` starts with `[sc-launch:v1:<nonce>]`; R3 `pipeline.json` stays documentation; R4 release is `rm` of the active file.

## 4. Session identity (D1) and where state lives (D2)

D1: option (a), pending record plus first-prompt marker, bound to `session_id`.

Binding: on UserPromptSubmit, if the prompt starts with `[sc-launch:v1:<nonce>]`, `pending/<nonce>.json` exists, and its `worktree_real_path` equals the payload `cwd` resolved, write `active/<session_id>.json` (level, submit, `approved: false`) and delete the pending record (single use). Any mismatch: no binding, exit 0. Once bound, governed for life; `--resume` keeps the id (V14).

Reject (b) environment variable: the shim is out of scope, the variable is inherited by every child the agent starts, and it cannot be re-checked per call. Reject (c) keyed by worktree path: a rename breaks it (AC-5) and it misgoverns a second, human session in the same worktree, the worst false positive here and free to avoid.

D2: state under `~/.claude/state/`, the existing per-session-file convention (verified: `freshness-subagent-start.sh`, `session-init.sh`). The active file is hook-written only, the pending file claim-script-written only. Tamper rules, each with a test: (1) any Bash command string or Edit/Write `file_path` naming `~/.claude/state/launch-level` is blocked in every session (MSG-STATE); (2) an active file that is unreadable or invalid JSON is treated as level `worktree`, `approved` false (most restrictive); (3) an unknown level value likewise.

Rejected: HMAC (the key sits beside the data for the same user, adding surface with no gain), root-owned directories (no root), read-only bits (the owner can chmod back).

## 5. Decision table

PreToolUse payloads in a bound session. Shorthand `{"session_id":S,"tool_name":T,"tool_input":I}`; only T and I vary. W = worktree, WA = worktree after approval, F = full, FS = full with `--submit`.

| Tool call pattern | W | WA | F | FS |
|---|---|---|---|---|
| Skill `sc:implement` (model-called) | BLOCK MSG-PLAN | ALLOW | ALLOW | ALLOW |
| Skill `task` (model-called) | BLOCK MSG-PLAN | ALLOW | ALLOW | ALLOW |
| Bash `git commit -m "x"` | BLOCK MSG-COMMIT | BLOCK MSG-COMMIT | BLOCK MSG-COMMIT | ALLOW |
| Bash `git push origin HEAD` (feature branch) | BLOCK MSG-PUSH | BLOCK MSG-PUSH | BLOCK MSG-PUSH | ALLOW |
| Bash `git push origin master`, `git push origin HEAD:main`, `git push origin refs/heads/master` | BLOCK MSG-NEVER | BLOCK MSG-NEVER | BLOCK MSG-NEVER | BLOCK MSG-NEVER |
| Bash `git merge <x>`, `gh pr merge <n>`, `gh pr ready` | BLOCK MSG-NEVER | BLOCK MSG-NEVER | BLOCK MSG-NEVER | BLOCK MSG-NEVER |
| Skill `sc:pr-submit` | BLOCK MSG-SUBMIT | BLOCK MSG-SUBMIT | BLOCK MSG-SUBMIT | ALLOW |
| Bash `gh pr create --repo IronbellyOrg/IronClaude ...` | BLOCK MSG-SUBMIT | BLOCK MSG-SUBMIT | BLOCK MSG-SUBMIT | ALLOW |
| Bash `git status`, `git diff`, `git log --grep=push`, `git add -A`, `make test`; Skill `sc:workflow`, `sc:load`; Read, Grep, Glob | ALLOW | ALLOW | ALLOW | ALLOW |
| Edit/Write `file_path` under `~/.claude/state/launch-level/` | BLOCK MSG-STATE | BLOCK MSG-STATE | BLOCK MSG-STATE | BLOCK MSG-STATE |
| Bash naming `.claude/state/launch-level` anywhere | BLOCK MSG-STATE | BLOCK MSG-STATE | BLOCK MSG-STATE | BLOCK MSG-STATE |
| Bash command word `claude`, `ccsession`, `ccsession-orca`, `orca` | BLOCK MSG-ESCAPE | BLOCK MSG-ESCAPE | BLOCK MSG-ESCAPE | BLOCK MSG-ESCAPE |
| Tools `CronCreate`, `ScheduleWakeup`, `Workflow`; Monitor with a `command` | BLOCK MSG-SELF | BLOCK MSG-SELF | BLOCK MSG-SELF | BLOCK MSG-SELF |
| Agent/Task spawn, any `subagent_type` | ALLOW | ALLOW | ALLOW | ALLOW |
| Edit/Write inside the worktree, source files included | ALLOW | ALLOW | ALLOW | ALLOW |
| Bash `echo "run git commit later"` (documented over-match) | BLOCK MSG-COMMIT | BLOCK MSG-COMMIT | BLOCK MSG-COMMIT | ALLOW |

The Agent ALLOW rows are deliberate: subagents are policed by this same hook inside the subagent (V4), so gating the spawn adds edge cases without enforcement. Edit/Write ALLOW at W is a position, not an oversight: AC-1 draws the boundary at the implement commands, and gating edits would block plan writing under `.dev/` (reversible, O-2).

## 6. Human approval and human versus agent (D3)

Approval is recorded, never inferred. Two events create it, both unreachable by a model tool call:

1. UserPromptExpansion with `command_name` `sc:implement` or `task` (V5: a typed slash command fires this event; a model-called skill fires PreToolUse on Skill instead). Whether it fires when queued mid-turn is UNVERIFIED (U5); route 2 covers it.
2. UserPromptSubmit whose entire prompt, trimmed, equals `approved` (V6).

Either event, in a bound session, sets `approved: true`. Approval unlocks implementation only (W to WA), never commit, push or pr-submit; those need FS, which only the claim script writes.

Human versus agent is what the harness gives (V5, V6): typed and model-called commands land on different events, the mechanical difference AC-3 asks for. Forgery: a self-started turn fires UserPromptSubmit with the same shape as a typed one (V6), so the agent could schedule a turn whose prompt is `approved`; prevented by blocking self-scheduling tools (MSG-SELF). U4 (`!cmd` escapes) is tolerated: such an `approved` is still human-typed. `orca terminal send` is residual (section 2).

## 7. Subagents and nested subagents

Hooks from settings run inside subagents and the payload carries `agent_id` (V4), so governance reaches subagents with the same script and lookup.

U1 (subagent `session_id` equality) is UNVERIFIED. Fallback, in order, each step tested: (1) `active/<session_id>.json` exists, govern by it; (2) payload has `agent_id` and some active record's `worktree_real_path` equals this `cwd`, govern by that record; (3) otherwise exit 0. Rule 2 is why nesting works even if every level mints a new id: they share the worktree cwd, and it costs one directory scan only when rule 1 misses. Rule 2's false positive needs a top-level session carrying `agent_id`; top-level sessions do not (V4). Tested by T-ISO-2.

## 8. Bash and git wrappers (D4)

Position: word-window matching with wrapper normalization. No shell parser.

Algorithm, each step testable. Strip quoting characters, split on whitespace. Walk words, skipping wrapper prefixes: `sudo`, `nice`, `nohup`, `time`, `exec`, `timeout` plus its value, `env` plus `VAR=val` and `-i`/`-u X`, `command`, `coproc`, `xargs` plus options, and `bash`/`sh`/`zsh`/`dash`/`ksh` with `-c`, whose following string is re-scanned one nesting level deep. Take each remaining word's basename. Basename `git`: look ahead four words skipping options, read the subcommand; `commit`, `push`, `merge` gated per the table, all else allowed. Basename `gh`: `pr merge` never, `pr create` FS only. Basename `claude`, `ccsession`, `ccsession-orca`, `orca`: block (MSG-ESCAPE). Any word naming the store: block (MSG-STATE).

Push target check, only when push is otherwise allowed (FS): block if any word after `push` equals `master`, `main`, `origin/master`, `origin/main`, `refs/heads/master`, `refs/heads/main`, or ends with `:master`, `:main`, `:refs/heads/master`, `:refs/heads/main`. Catches `git push origin HEAD:master`; allows `git push origin ironbelly/x`.

Rejected: the #357 awk scanner (verified: 300 lines, nine documented ceilings, 100+ test cases across three PR review rounds; importing it imports its ceilings and maintenance cost); a PATH shim for git (global environment change, breaks ordinary sessions); git-level hooks (`pre-push` is skipped by `--no-verify`, and `.git/hooks` sits inside the worktree the agent can write). The word-window over-matches (`echo "git commit"`), accepted per A12 and pinned by a test: one blocked echo costs a retry, a missed commit costs the boundary.

## 9. Other tools and escape routes (D5)

Inspected at PreToolUse: `Bash`, `Skill`, `Edit`, `Write`, `Agent`, `Task` (matched `Agent|Task` for U3), `Workflow`, `Monitor`, `CronCreate`, `ScheduleWakeup`. The matcher is `*` because `if` patterns cannot be trusted to narrow Bash contents (V10), and unknown tool names still reach the fast path, which exits 0 unbound.

Skill payload keys are UNVERIFIED (U2): read `tool_input.skill // tool_input.name`, the dual read `sc-recommend-phase0.sh` uses. Neither present on a Skill call in a bound session at a gated level: fail closed with MSG-PLAN or MSG-SUBMIT. OB-H1 settles it.

Not inspected: MCP tools (opaque inputs, residual), Read/Grep/Glob (read-only), NotebookEdit (worktree write path, as Edit/Write). Direct source edits at W allowed by default; reversing is O-2.

Escape routes: `claude -p`, `ccsession`, `orca` subcommands blocked as command words at every level (MSG-ESCAPE), agreeing with WC-13 (a worker never calls `orca agent launch` or `worktree create --agent`). Re-claim by the launched agent is not blocked: no AC names it. `--bare`, `--settings` (U6) and forked ids (V14) are residual (section 2).

## 10. Fail-closed rules and speed (D6)

Fail-closed, governed sessions only:

| Condition | Behaviour |
|---|---|
| active file missing after binding (only via deletion) | not governed, exit 0 (residual, section 2) |
| active file unreadable or invalid JSON | treat as W, approved false; gated calls blocked MSG-STATE |
| level not in {worktree, full} or submit not boolean | same |
| Skill call without a readable skill key in a bound session | block that call |
| `jq` missing or stdin not JSON | exit 0 everywhere (V8: a crash does not block anyway); residual, section 2 |

`onFailure: "block"` is not used (verified constraint: it would block ordinary sessions when the hook breaks). Timeout 5 s; the script makes no network calls and reads at most 256 KB of stdin (proposed cap).

Speed. The ordinary path is one `jq` read of `session_id`, one file-existence test, exit 0. Budget: median at or under 20 ms, p95 at or under 50 ms ordinary; p95 at or under 60 ms governed allow. T-SPD-1 and T-SPD-2 measure it: 100 real subprocess invocations of a fixed payload, `time.monotonic()` around each. T-SPD-3: the ordinary-path median must stay at or under 1.5 times the median of `block-bare-python.sh` in the same run, so a slow regression is caught even under budget.

## 11. Block messages (plain words, one per message id)

- MSG-PLAN: "Blocked: the implement command needs human approval first. This session was launched at the worktree level, which stops at an approved plan. A human approves by typing the implement command or replying approved."
- MSG-COMMIT: "Blocked: committing needs the submit level. Ask the human to commit, or to relaunch with --submit."
- MSG-PUSH: "Blocked: pushing needs the submit level. Ask the human to push."
- MSG-NEVER: "Blocked: merges and pushes to master or main are never allowed at any launch level. Only a human reviews and merges."
- MSG-SUBMIT: "Blocked: opening or updating a pull request needs the submit level. This session was launched without --submit."
- MSG-STATE: "Blocked: this action touches the launch-level state files, which the launched agent must not read or change. A human can edit them outside this session."
- MSG-ESCAPE: "Blocked: launching another Claude, ccsession or Orca session would leave this launch level unenforced. Work in this session."
- MSG-SELF: "Blocked: self-scheduling tools are off in a launched session, because a scheduled turn could be mistaken for human approval."

Each names what was blocked, why, and what the human can do (AC-7). One line on stderr with exit 2 (V2).

## 12. Test plan (D7)

Automated tests run the real script with JSON on stdin and a temporary HOME, the pattern of `tests/hooks/test_block_bare_python.py`. A fixture builds payloads `{"session_id":S,"tool_name":T,"tool_input":I}` (`agent_id` where stated) and a store builder writes pending and active files. Only T and I are shown below.

AC-1 (T-W-*): `["Skill",{"skill":"sc:implement"}]` exit 2 MSG-PLAN; `["Skill",{"skill":"task"}]` exit 2 MSG-PLAN; `["Bash",{"command":"git commit -m 'x'"}]` exit 2 MSG-COMMIT; `["Bash",{"command":"git push origin HEAD"}]` exit 2 MSG-PUSH; `["Skill",{"skill":"sc:pr-submit"}]` exit 2 MSG-SUBMIT; allow row `["Skill",{"skill":"sc:workflow"}]` exit 0.

AC-2 (T-F-*, T-S-*): at F `["Skill",{"skill":"sc:implement"}]` exit 0 and `["Bash",{"command":"git commit -m 'x'"}]` exit 2 MSG-COMMIT; at FS that commit exits 0, `["Bash",{"command":"git push origin ironbelly/x"}]` exit 0, `["Skill",{"skill":"sc:pr-submit"}]` exit 0.

AC-3 (T-A-*): bound at W, `{"prompt":"approved"}` exits 0 and writes `approved: true`, and the next `["Skill",{"skill":"sc:implement"}]` exits 0; `{"command_name":"sc:implement"}` also approves; `{"prompt":"please approved"}` does not (whole-prompt rule); after approval at W, `git commit` still exits 2; unbound, `{"prompt":"approved"}` changes nothing.

AC-4 (T-ISO-*, T-SUB-*): unbound session, every gated payload exits 0 with empty stderr (T-ISO-1, the false-positive master case); second session, different id, same cwd, no `agent_id`: not governed (T-ISO-2); marker prompt plus matching record and cwd writes the active file and consumes the pending record (T-ISO-3); replayed marker binds nothing (T-ISO-4); record naming a different cwd binds nothing (T-ISO-5). Subagents: parent id plus `agent_id`, governed (T-SUB-1); unknown id plus `agent_id` plus cwd matching an active record, governed by fallback (T-SUB-2); nested shape with `agent_type`, still governed (T-SUB-3); unknown id plus `agent_id` plus cwd matching nothing, exit 0 (T-SUB-4).

AC-5 (T-ST-*): active file invalid JSON, gated call exit 2 MSG-STATE (T-ST-1); level `"bogus"`, same (T-ST-2); Edit/Write to `~/.claude/state/launch-level/active/x.json` exit 2 MSG-STATE (T-ST-3); `["Bash",{"command":"cat ~/.claude/state/launch-level/active/x.json"}]` exit 2 MSG-STATE (T-ST-4); rename survival: change the record's `worktree_real_path`, the session stays governed by id (T-ST-5); re-claim: a new pending record with a new nonce binds a new id while the old active file still governs the old one (T-ST-6).

AC-6 (T-WR-*): `bash -c "git commit -m x"` exit 2 MSG-COMMIT; `command git push origin HEAD` exit 2 MSG-PUSH; `/usr/bin/git merge x`, `git merge --no-ff x` exit 2 MSG-NEVER; `sudo git push origin master`, `git push origin HEAD:main`, `git push origin refs/heads/master` exit 2 MSG-NEVER at every level including FS; `gh pr merge 12` exit 2 MSG-NEVER at FS; `env -i git commit` exit 2 MSG-COMMIT; `timeout 30 git push origin HEAD` exit 2 MSG-PUSH; `claude -p "x"`, `orca agent launch --agent claude`, `ccsession-orca 'x'` exit 2 MSG-ESCAPE.

AC-7 (T-MSG-1..8): one assertion per message id that stderr starts with the exact first sentence and exit is 2.

AC-8 and false-positive guards (T-NEG-*): in a bound W session, exit 0 expected for `git status`, `git log --grep=push`, `git diff master...HEAD`, `git add -A`, `make test`, `ls`, `echo use uv run pytest`, Read/Grep/Glob payloads, an Agent spawn payload, an Edit payload inside the worktree. Documented over-match, asserted as blocked so a change is conscious: `["Bash",{"command":"echo \"git commit\""}]` at W exits 2 MSG-COMMIT.

Self-scheduling (T-SELF-*): `CronCreate`, `ScheduleWakeup`, `Workflow` payloads and Monitor with a `command` exit 2 MSG-SELF bound, exit 0 unbound. Speed (T-SPD-1..3): as section 10. Fail-open (T-FO-*): stdin not JSON, empty `tool_input`, unknown tool name all exit 0, in both bound and unbound sessions except where section 10 says closed.

Observed, not automatable (OB-H1 to OB-H3, from A7): OB-H1 one real governed launch, log the real payload of a subagent Bash call and a model Skill call, settle `session_id` equality (U1) and the Skill key (U2); OB-H2 confirm binding happened before the first tool call (U8); OB-H3 one run per level: W blocks implement until a typed approval, F finishes with no commit, FS pushes a branch and opens a PR on the fork. Each is a `@pytest.mark.manual` placeholder.

## 13. Acceptance criteria map

| AC | Sections | Tests |
|---|---|---|
| AC-1 worktree stops at approved plan; blocks implement, task, commit, push, pr-submit | 5, 6, 11 | T-W-*, T-A-1..3 |
| AC-2 full implements, blocks submission; FS allows it | 5, 8 | T-F-*, T-S-* |
| AC-3 approval by typing the command or replying approved; human vs agent | 6, 11 | T-A-*, T-SELF-* |
| AC-4 claim-launched only; Bash, Skill, Task; nested subagents | 4, 7, 9 | T-ISO-*, T-SUB-* |
| AC-5 uneditable state, fail closed, tamper, rename, re-claim | 4, 10 | T-ST-1..6, T-FO-* |
| AC-6 never a merge or master/main push, including wrappers | 5, 8 | T-WR-* |
| AC-7 plain-words explanation for every block | 11 | T-MSG-1..8 |
| AC-8 automated allowed/blocked per level, approval, isolation, nested, missing state, wrappers, edges; speed | 10, 12 | all T-*, T-SPD-* |

## 14. Order of work

1. Skeleton with the ordinary fast path and event dispatch; T-ISO-1 and T-FO-* pass first, so the hook is provably harmless before it governs.
2. Binding and store layout; T-ISO-3..5, T-ST-6.
3. Decision table for Skill and Bash at all four columns; T-W-*, T-F-*, T-S-*, T-NEG-*.
4. Approval recording; T-A-*.
5. Wrapper normalization, push-target check, escape and self-scheduling rules; T-WR-*, T-SELF-*.
6. Fail-closed, speed budgets, message assertions, `hooks.json` registration, `_FRESHNESS_SCRIPTS`, `make verify-sync`; then OB-H1 to OB-H3 before `full` is used on a real issue.
## 15. Open decisions for the owner

- O-1: should FS also force `--repo IronbellyOrg/IronClaude` on `gh pr create` and reject any other repo argument (the CLAUDE.md fork rule)? Default: yes, one extra word check, test T-WR-gh-repo.
- O-2: block direct source edits at W before approval? Default: no (AC-1 defines the boundary by commands).
- O-3: who cleans up finished sessions, the hook at SessionEnd or a human with `rm`? Default: human (R4); SessionEnd firing after a crash is UNVERIFIED.
- O-4: gate `git rebase` like merge? Default: no (it moves HEAD locally; no AC names it); cheap to add.
- O-5: does a launched `--submit` session count as a worker run under WC-9 (U7)? If yes, FS is unreachable and the FS column is dead code; settle before step 3, the FS tests depend on it.
- O-6: approval lifetime. Default: permanent for the session; per-plan counting needs plan identity the hook cannot see.

## 16. UNVERIFIED items and how the design tolerates each

| # | Item | Tolerance | Test |
|---|---|---|---|
| U1 | subagent `session_id` equality | lookup by id, fallback by `agent_id` plus cwd (section 7) | T-SUB-1..4, OB-H1 |
| U2 | Skill payload keys | dual read `skill // name`; neither present in a bound session fails closed | T-MSG cases, OB-H1 |
| U3 | Agent also named Task | match `Agent|Task` | T-SUB-* under both names |
| U4 | `!cmd` escapes on UserPromptSubmit | approval needs the whole prompt; such an `approved` is still human-typed | T-A-4 |
| U5 | UserPromptExpansion when queued mid-turn | second route, whole-prompt `approved` | T-A-2, T-A-3 |
| U6 | hooks under `--bare` or `--settings` | residual, listed; the `claude` command word is blocked, so the agent cannot start one | T-WR-escape |
| U7 | Orca worker preamble on launched sessions | the hook never reads preambles; O-5 gates the FS column | OB-H1 notes |
| U8 | UserPromptSubmit before the first model call for an argv prompt | if it does not fire, no binding happens and the session is unguarded; the section 7 fallback cannot help a top-level session | OB-H2 |

U8 is the one item that can silently void the design, so OB-H2 is mandatory before any governed level is used on a real issue.

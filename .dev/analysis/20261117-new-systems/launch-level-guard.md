# Launch-level guard hook

Date: 2026-11-17. Source: origin/master (read-only). Companion: launch-level-guard-explain.md

## 1. What it is

The launch-level guard is a bash script that Claude Code runs before every prompt and before risky tool calls. When `/sc:issue --claim` starts an agent in a fresh Orca worktree, the guard "governs" that one session: the agent can read, plan and edit, but cannot commit, push, open a PR, merge, message other sessions or edit its own limits, depending on the launch level (`worktree`, `full`, `full --submit`). At the default `worktree` level the agent is held at the plan boundary until a person releases it. Every other session is never touched.

**What is new (be plain about it):** the hook itself is NOT new. It first merged in PR #432 on 2026-11-07 (issue #394), then got an L2 git pre-push companion in PR #469 (2026-11-10). The new part inside the 72 hour window is the removal of the release route "type `approved`":

- PR #583, merged 2026-11-16 ("remove the plain approved route from every worktree-level claim", owner decision Q39). Now only a prompt whose first line starts `/sc:implement`, `/sc:task` or `/task` releases the agent.
- PR #584, merged 2026-11-17 04:00 UTC, touched the guard by one line (the LL-TURN explanation, which still described `approved`) plus the new `issue_pipeline` approval core (separate system, not documented here).

**Entry points**
- `src/superclaude/hooks/scripts/launch-level-guard.sh` (750 lines), byte-identical mirror at `plugins/superclaude/hooks/scripts/launch-level-guard.sh` (diff run, no differences).
- Registered in `src/superclaude/hooks/hooks.json` on UserPromptSubmit (line 67) and PreToolUse (line 120, one big matcher on Bash, Skill, Agent, Task, Edit, Write, NotebookEdit, Monitor, Workflow, RemoteTrigger, SendMessage, Cron*, Schedule* and risky mcp__ names); the plugin copy registers it at `plugins/superclaude/hooks/hooks.json:48` and `:90`. Installer list: `src/superclaude/cli/install_hooks.py:93`.
- Claim side: `src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py` (`cmd_launch`, `publish_pending`), `templates/launch-prompt.md`, `refs/claim.md`.
- Tests: `tests/hooks/test_launch_level_guard.py` (4618 lines) plus 6 sibling test files and fixtures under `tests/hooks/fixtures/launch_level/` (OB-H1 captured payloads).
- Designs: `docs/designs/sc-issue-launch-level-hook.md`, `docs/designs/sc-issue-claim-pipeline-flag.md`.
- Companion hook: `launch-level-pre-push.sh` (L2, refuses governed pushes to main/master at git level).

## 2. How it works

**Data flow**

1. `/sc:issue --claim N --pipeline <level>` ends with `orca_worktree.py launch`. It refuses the launch (`W-ENFORCEMENT-ABSENT`) if the guard is not effective (`enforcement_preflight`, orca_worktree.py:1716-1733), then tries to install the L2 pre-push hook (`install_l2`, warning only while `IR7_REFUSE = False`, lines 819, 1740-1744).
2. It writes a pending record of one word, `worktree`, `full` or `full-submit` (`word = "full-submit" if args.submit else args.level`, line 1745), at `~/.claude/state/launch-level/pending/<32 hex nonce>`, mode 0600, refusing symlinks (`publish_pending`, lines 1485-1509).
3. It starts `orca agent launch --agent claude --surface terminal --prompt "[sc-launch:v1:<nonce>] Read .dev/issues/N/launch-prompt.md and follow it."` (lines 1762-1766).
4. The guard sees that first prompt (UserPromptSubmit). The strict marker regex is at guard.sh:318. It consumes the nonce with one `mv` to `sessions/.take-<sid>` and publishes `sessions/<sid>` as a hard link, so the first binding is never replaced (lines 289-313, 373-384). A subagent prompt (`agent_id` set) never binds or releases (line 315).
5. On each PreToolUse, a valid session id with a record is governed. Its level is the exact one-word content (W, F, FS), anything else becomes W plus a "strictest level applies" note; `<sid>.ok` at W gives WA (lines 257-273).
6. Tool classifiers (lines 398-699) add classes: IMPL, SUBMIT, ESCAPE, COMMIT, PUSH, PUSHFORM, PROTECTED, MERGE, GHWRITE, REPO, UNKNOWN, MCP, TURN, TAMPER, BIG, SKILL. One case table maps CLASS:LEVEL to allow or a deny message (lines 725-745). Deny means message on stderr, exit 2.

**The release rule (the new bit).** `LL_RE_APR='^[[:space:]]*/(sc:implement|sc:task|task)([[:space:]]|$)'` (guard.sh:347) is tested against the prompt only when the level is exactly W (lines 349-351). A match creates an empty `<sid>.ok` with no-replace semantics (lines 352-360). The old extra lines that trimmed, lower-cased and matched `approved[.!]?` were deleted in #583 (diff of d32465f21). Tests now assert `approved`, `Approved.`, `approved!`, `  APPROVED!  ` and similar write no `.ok` (tests/hooks/test_launch_level_guard.py around line 3695).

**What each level allows** (table lines 725-745): W blocks IMPL, TURN, SUBMIT, COMMIT, PUSH; WA allows IMPL and TURN only; F adds IMPL and TURN; FS also allows SUBMIT, COMMIT, PUSH. At every level MERGE, GHWRITE, PROTECTED (push to master/main), ESCAPE, MCP writes, UNKNOWN git/gh commands, TAMPER and BIG are blocked.

**Safety limits and design choices**
- Fails closed for a governed session on any internal error (EXIT trap, lines 142-163), including missing jq (message LL-BROKEN or LL-NOBIND). Ordinary sessions are never blocked by a failure.
- Parses the hook JSON once with jq; a non-string tool field or NUL byte is an input error (lines 182-205).
- A push passes only as exactly `git push [-u] origin <branch>`, with one regex (line 658); `git push origin HEAD` is PUSHFORM; master/main is PROTECTED.
- `gh api` passes only as one plain GET (line 496 and following).
- `orca`, `tmux`, `screen`, `claude -p` style launches, `SendMessage`, remote agents, Workflow and RemoteTrigger are ESCAPE so the agent cannot start an ungoverned worker or type a release prompt into a terminal.
- Cron and schedule tools are TURN at W, because a scheduled prompt could look like a person typing a release.
- TAMPER tokens: the store path (built from three parts so the script never names it joined), `.claude/settings`, `.claude/hooks`, `disableAllHooks`, git config files, the pre-push hook, `--no-verify` (lines 700-717).
- Human release stays outside the model: a person runs `rm sessions/<sid> sessions/<sid>.ok` (LL-TAMPER message, line 97; claim prints it, orca_worktree.py:1466-1473).

**Inputs/outputs.** Input: hook JSON on stdin plus the store under `$HOME/.claude/state/launch-level/`. Output: exit 0 (allow) or exit 2 with `Launch-level guard: ... Blocked / Why / You can` on stderr. Never exit 1.

## 3. Where it could be integrated in future

The guard is a general "bind a session to a capability level, then gate tool calls" pattern. It could serve:

- **Any supervised or unattended worker launcher** (Orca orchestration workers, an issue watcher, scheduled agents). Why: the same launch-then-bind handshake gives a worker a hard ceiling that the model cannot raise.
- **Review or audit sessions** that must stay read-only (a level with no edit class). Why: the class table already separates read, edit, commit, push and submit.
- **Release gates other than `/sc:implement`**: a different first-line command (for example a plan-approval command) could create the `.ok` file. Why: the release is one regex plus a file; the rest is reusable. Note #584's approval core records approvals through chat, so a future release could be tied to that record instead of a prompt line (UNVERIFIED how, see section 6).
- **Other CI or agent platforms** that expose PreToolUse style hooks. Why: only the JSON field names and the `~/.claude` store path are Claude Code specific.

## 4. Integration guide

1. **Launch through the claim script, not by hand.** Use `orca_worktree.py launch` so the nonce record and marker prompt are created together. An agent started by hand is not governed (the script says so itself, orca_worktree.py:1776-1779).
2. **Install first.** Run `superclaude install` so `~/.claude/hooks/launch-level-guard.sh` exists and both registrations (hooks.json) are active. The claim preflight (`enforcement_preflight`, orca_worktree.py:952) refuses the launch otherwise. It also needs `jq`.
3. **Pick the level by the word you publish**: `worktree`, `full` or `full-submit` (the only three words the guard accepts, guard.sh:265-267). A new level means a new word, a new case line in the level reader, new rows in the table at lines 725-745, and new tests.
4. **Make the first prompt start with `[sc-launch:v1:<nonce>]`** and keep the prompt a plain sentence (design: no leading `/`). A loose marker with a missing nonce still binds as "degraded" at the strictest level (lines 377-379).
5. **Tell the agent the real release route.** Use `templates/launch-prompt.md`; since #583 it says "run the printed implement command", never "reply approved".
6. **Release.** The person types `/sc:implement <plan path>`, `/sc:task ...` or `/task ...` as the first line in the agent's own session. Emergency release is the printed `rm` of both session files.
7. **Add a new class** by adding a classifier branch in part 8 (lines 398-699), the class name to the precedence loop (line 725) and a message in `ll_say` (lines 36-114).

**Reuse:** the printer and normaliser blocks are marked so tests can run them alone (`# >>> printer`, `# >>> normalise`); the OB-H1 fixture payloads are real hook input captures; `launch-level-pre-push.sh` is the git-level backstop.

**Pitfalls**
- Quoted text is not told from commands: `git commit` inside a PR body or search pattern blocks (the LL-TEXT note, line 131). Write bodies to a file.
- Do not refresh the installed guard while a governed agent waits for the old `approved` reply; it can then only be released by one of the three commands (PR #583 body, Risks).
- Release applies at exactly level W; a bad level word still counts as W.
- Subagents: identity is `session_id` only; whether subagents carry the parent id is UNVERIFIED (design ship gate U1).
- Hook timeout is 5 seconds (hooks.json:121); keep new classifiers cheap (the script avoids `${s//.../}` over long text).

**Tests to add** (in `tests/hooks/test_launch_level_guard.py` style, which runs the real script with a temp HOME): a case per new class and level pair; typed-word negatives for any new release route; binding race (two prompts one nonce); a registration test (`test_launch_level_guard_registration.py`); and a claim-script test with a fake `orca`.

## 5. IronClaude fit

Checked on origin/master: hook scripts under `src/superclaude/hooks/scripts/` (block-bare-python, require-orca-worktree-agent, launch-job-identity, launch-level-guard, launch-level-pre-push, freshness-*), CLI packages `issue_pipeline`, `issue_watch`, `sprint`, `sweep`, `swarm`. The guard is already wired to `/sc:issue --claim`. Only the pieces below are plausible new uses; I did not read `issue_watch` or `swarm` in depth (UNVERIFIED).

1. **Supervised worker dispatch (Orca orchestration workers, `worker-start`)**. Target: the dispatch path for supervised workers (skill `orchestration`; exact script path UNVERIFIED). Change: launch workers through the same nonce plus marker handshake with a `worktree` or `full` word, so a worker has a hard ceiling on push, merge and spawning. Value: high, because workers today rely on prompt text and the worker contract. Effort: medium (a launcher call plus tests). Risk: medium; ESCAPE blocks `orca` and `SendMessage`, which workers use for ask and `worker_done`, so a worker level or allow-list would be needed.
2. **Issue watcher claim handoff (`src/superclaude/cli/issue_watch/`, `src/superclaude/cli/issue_pipeline/`)**. Change: when the watcher launches a claim agent, reuse `orca_worktree.py launch` and bind release to the approval record from #584 instead of a typed command. Value: medium-high, it removes the last human-typing route and matches the owner rule "approvals through chat". Effort: medium-high (the guard needs a new release input, as it only knows prompt-first-line today). Risk: high; this is a security hook and any release change needs its own independent review (the #583 PR said so).
3. **Read-only review sessions (`/sc:pr-submit --monitor` reviewers, `/sc:reflect` reviewer fan-out, `sc:sweep`)**. Change: add a `readonly` level (no edit, commit, push class). Value: medium; today read-only is enforced by agent tool allow-lists (for example `reflect-reviewer`), which only cover subagents. Effort: low-medium (one level word, table rows, tests). Risk: low-medium.
4. **Sprint executor (`src/superclaude/cli/sprint/executor.py`)**. Probably no good fit: sprint runs headless child `claude` processes, which the guard treats as ESCAPE, and the guard only binds through a marker prompt in an interactive claim. Not recommended without a design.

Plain verdict: a good fit for 1 and 2 as the same pattern; 3 is a cheap extension; 4 is not a fit.

## 6. Limits, open questions, UNVERIFIED

**Declared limits (from the script and design)**
- Text matching, not a shell parser: variables, quoting tricks and `$(...)` can pass some text checks (comment at guard.sh:713-714 says the real fix is the L2 layer). Over-matching also happens (LL-TEXT).
- Identity loss (missing or invalid `session_id`) allows the call without claiming enforcement (lines 387-391).
- Any other session that types `/sc:implement` counts as the person (design risk R15; prompts carry no origin field).
- The typed `approved` removal means a person with no coordinator must type a real command; an agent already waiting for `approved` needs one of the three commands.
- L2 pre-push is a warning, not a refusal, while `IR7_REFUSE = False` (orca_worktree.py:819).
- The claim preflight checks the claim process's HOME, PATH and settings files, not the agent's real environment (design doc, claim-pipeline design update).

**UNVERIFIED**
- Whether subagents carry the parent `session_id` (OB-H1 item 1), turn wrapping of self-started turns (item 5), bind timing (OB-H2), the real-claim L2 observation (OB-H3). The design says none of these live observations had been run, and "no governed claim on a real issue" until they pass; I did not confirm whether that changed after #584.
- The author's PR #583 notes 193 tests failed on their host because `/proc/sys/kernel/random/boot_id` was unreadable; CI results were not checked by me.
- I did not run the test suite, did not read `launch-job-identity.sh`, `issue_watch`, or the orchestration skill source.
- Edge not tested: the approval regex is run on the raw prompt with no BOM stripping, whereas the marker check strips a BOM (guard.sh:320-328 vs 347). Reading only; behaviour not run.

**Open questions**
- Should release be tied to the #584 approval record rather than a typed command?
- Should a `readonly` level exist?
- When does `IR7_REFUSE` turn on?

---
Footer: graph:stale (codegraph index does not cover origin/master; not used). All file:line cites are from `git show origin/master:<path>` read on 2026-11-17.

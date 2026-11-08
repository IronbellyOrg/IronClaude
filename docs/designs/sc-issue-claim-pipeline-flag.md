# Design: `/sc:issue --claim --pipeline` (worktree, launch levels, `--submit`)

**Status:** Implemented: `--pipeline` and `--submit` (PR #425). Issue #394 then changed the claim side of the launch: the IR-4 preflight refusal, the IR-7 warning and the release and layer lines of the launch result (see the Update below).
**Update (issue #394):** the launch-level guard now exists and default D3 is replaced. When the guard is missing or not effective (`enforcement_preflight()`, hook IR-4; checked from the claim process only, its HOME, PATH, environment and the user and worktree settings files, so enterprise-managed settings and what Claude Code really runs are not seen) the claim refuses the launch with `W-ENFORCEMENT-ABSENT`: no agent starts and no launch record is written. When the worktree has no L2 pre-push layer the claim warns with `W-L2-ABSENT` and the launch continues, because the L2 layer is not built yet (hook IR-7, taken as a warning). IR-3 stays documentation only because no code writes `pipeline.json`. No governed claim (`worktree` or `full`) is used on a real issue until OB-H1 item 1 (parent `session_id` in subagent payloads), OB-H2 and OB-H3 have passed. In `docs/designs/sc-issue-launch-level-hook.md`, section 7 (U1) requires item 1 before a `full` or `--submit` claim and OB-H1 item 5 (self-started turns wrapped) before a claim at any level; OB-H2 and OB-H3 come from its sections 11 and 14. Sections below that describe `W-ENFORCEMENT-ABSENT` carry this update.
**Issue:** none. This feature had no tracking issue. Related follow-on: IronbellyOrg/IronClaude #394 (launch-level enforcement hook, `docs/designs/sc-issue-launch-level-hook.md`). Launch rule from #412 (merged).
**Branch:** `ironbelly/sc-issue-claim-pipeline-flag`
**Source requirements:** `.dev/brainstorms/20261105-024132-issue-claim-orca-worktree-flag/merged-requirements.md` ("MR") as amended by `launch-levels-addendum.md` in the same folder ("AD", revision 2, after the owner's four corrections of 2026-11-05). Where MR and AD differ, AD wins. Where AD and the hook design differ on hook state, the hook design wins (section 3).
**Source of truth:** `src/superclaude/` -> `make sync-dev` -> `.claude/` (never stage `.claude/`).
**Produced by:** `/sc:design sc-issue-claim-pipeline-flag --type component --format spec`, 2026-11-07.

> **Amended 2026-11-08** (owner decisions recorded while planning `TASK-WF-enforceTheOwnerP-20261108-031809`): every Orca worktree gets an agent, and the session that creates a worktree owns its agent. So `--pipeline none` now **creates no worktree**: the claim ends after the comments, `issue-summary.md` and `next-steps.md`, and the user runs `next-steps.md` from the main checkout's `.dev/issues/<N>/`. `worktree` and `full` still create the worktree and launch an agent. The Wave 0 Orca check still runs for `none` (P1). The worktree create keeps no `--agent` (D2 and FO-18 stay, see their 2026-11-08 notes); the script closes Orca's plain first tab itself after a successful copy (section 8.3, step 8, warning `W-FIRST-TAB-LEFT`). The owner approved this first-tab close in place of "agent on create" on 2026-11-08 after the pre-execution review. Evidence: `.dev/troubleshoot/bug-agents-run-orca-worktree-create-20261108015205/REPORT.md`; review: `.dev/reflect/pre-TASK-WF-enforceTheOwnerP-20261108-031809-20261108033529/REPORT.md` (Grounding Gap G-1).

---

## 1. Purpose and scope

Today `/sc:issue --claim` assigns the issue, checks its accuracy, writes `next-steps.md` and stops. The user then opens a worktree and a session by hand. This design adds two claim-only flags so the claim does that hand-off itself, at a level the user picks:

| Level | Flag | What happens after the claim's Waves 0-6 | Agent stops at |
|---|---|---|---|
| `worktree` (default) | `--pipeline worktree` or nothing | An Orca worktree `issue-<N>` is created (or reused) and a Claude Code agent is launched in it. It runs `next-steps.md` up to the plan boundary. | An approved plan: it prints the plan path and "Waiting for approval" until a human approves |
| `full` | `--pipeline full` | Same, but the agent runs every step including `/sc:implement` or `/task`. | Finished implementation, unstaged, uncommitted, unpushed |
| `full` + `--submit` | `--pipeline full --submit` | Same, then the agent commits, pushes a feature branch to `origin` and runs `/sc:pr-submit --monitor 3`. | A pushed branch with an open PR on the fork |
| `none` | `--pipeline none` | The claim ends after the comments (amended 2026-11-08): no worktree is created, no agent is launched. | Nothing runs; the user runs `next-steps.md` from the main checkout's `.dev/issues/<N>/` |

No level merges anything. Humans only review and merge; nobody opens a PR by hand, because with `--submit` the agent's `/sc:pr-submit` opens it.

**In scope:** the two flags and their STOP rules; a Wave 0 Orca check; Wave 7 (worktree, from MR as amended by AD section 4); Wave 8 (launch behind the ccsession shim); the launch prompt template; the `Plan boundary` line in `next-steps.md`; the launch-level state the hook of #394 reads; the new contract fields; tests and docs.

**Out of scope:**

- The enforcement hook (`launch-level-guard.sh`, its L2 `pre-push` layer, `jq` and registration checks): issue #394. This design only produces the state that hook consumes (section 6) and reports the result of the hook's IR-4 preflight in `enforcement_hook`.
- A flag value for model or effort, a lock for racing claims, `linkedIssue` matching, automatic worktree removal, any Orca link flag, any behaviour for a machine without Orca.
- Running any live claim, worktree create or agent launch against a real issue. Verification in this change is unit tests with a fake `orca`; the observed runs of section 17 are owner steps after merge.

## 2. Binding decisions

"Owner" is the owner's decisions of 2026-11-05 (AD section 1) and the task brief of 2026-11-07. B1 to B15 of `docs/designs/sc-issue-command.md` still bind, except B2, which is rewritten here.

| # | Decision | Source |
|---|---|---|
| P1 | Orca is a dependency. No code, warning, option or document text exists only for a project without Orca. | Owner, AD 1.2 |
| P2 | One flag, `--pipeline worktree\|full\|none`, default `worktree`. The `--worktree` flag of MR does not exist. | Owner, AD 1.6 |
| P3 | `--submit` is a second flag, valid with `--pipeline full` only. It turns on commit, push of a feature branch and `/sc:pr-submit --monitor 3`. It never merges. | Owner, AD 1.4 |
| P4 | The default stop is an approved plan. `full` adds implementation. `none` launches no agent. Amended 2026-11-08: `none` also creates no worktree, because every worktree gets an agent. | Owner, AD 1.3; owner, 2026-11-08 |
| P5 | The launched agent is Claude Code behind the ccsession shim, always. | Owner, AD 1.5 |
| P6 | **B2 is rewritten (new text below).** B16 (worktree after `next-steps.md`), B17 (launch levels) and B18 (`--submit`) are new design decisions in `docs/designs/sc-issue-command.md`. | Owner, AD 1.1 and 3 |
| P7 | The agent is started with `orca agent launch --agent claude --surface terminal`, a Claude CLI session. Never a plain terminal, and never `--surface chat` (a chat is not behind the shim). | #412 (merged), AD FR-22 |
| P8 | Nothing here builds the hook. The level must be readable by the hook from state the agent cannot edit (section 6). | Owner, task brief, #394 |
| P9 | Order of work: `/sc:design`, `/sc:workflow --depth quick`, `/sc:implement`, `/sc:pr-submit --monitor 3`. | Owner, task brief |

**B2 (rewritten):** the claim writes the summary and `next-steps.md`, creates a worktree, and launches one agent in it. Neither the `/sc:issue` skill nor the default agent runs `/sc:implement` or `/task`. `--pipeline full` lets the agent run them. `--submit` additionally lets it commit, push and run `/sc:pr-submit`. The `/sc:issue` skill itself still runs no next-step command; the launched agent does. Merging is never done by any level.

## 3. Reconciliations (where the source documents disagree or are silent)

| Point | Source text | This design | Why |
|---|---|---|---|
| Level state file | AD FR-31: the skill writes `<wt>/.dev/issues/<N>/pipeline.json` as the hook's input | **Not built.** The hook's input is a launch record outside the worktree (section 6). | The hook design (IR-1 to IR-3) is later (2026-11-06) and says `pipeline.json` is documentation only: the agent can edit anything inside the worktree. A file nothing reads is not written. |
| Git `pre-push` layer | AD FR-32: the claim installs a `pre-push` check in the new worktree | **Not built by the claim.** The hook feature's own installer owns it (hook design 19.2). The claim reports `enforcement_hook`. | Hook design 19 answers AD's open questions (place, chaining, removal) and makes installation part of #394. |
| Hook refusal rules | Hook IR-4 and IR-7: refuse a governed launch when `jq`, the script, effective registration or L2 is missing | **Built in #394.** A guard that is missing or not effective gives the refusal `W-ENFORCEMENT-ABSENT`: no agent starts and no launch record is written. A missing L2 layer gives the warning `W-L2-ABSENT` and the launch continues (the L2 layer is not built yet). | This design first made it a warning (old default D3) because the hook did not exist; #394 turned it into a refusal (IR-4). IR-7 stays a warning until an L2 layer exists. |
| `launch_status` values | AD FR-30: `launched \| failed \| not_requested` | Adds `already_launched` | AD FR-27 needs a state for a re-claim that finds a `launch` entry. |
| Launch prompt | AD FR-22: one plain sentence, no leading `/` | The sentence is prefixed with the hook's marker `[sc-launch:v1:<nonce>] ` (hook IR-2). The prefix starts with `[`, so the no-leading-`/` rule holds. | The hook binds the session by that marker. |
| Create JSON shape | MR R2 UNVERIFIED | AD observed `result.worktree.{id, path, branch, ...}`. FR-20 (path from a row-id difference) stays; the field is not relied on. | The set difference works with an opaque create result. |
| `worktree_warning` holds one code | MR open item | The code that set the status wins; any other goes in `detail`. Launch codes use their own field `launch_warning`. | Two independent steps can each warn. |
| Statuses | MR: `created \| reused \| skipped \| failed` | `created \| reused \| failed` | AD 4.2 and 4.4: `skipped` existed only for a missing `orca`. |
| Unflagged claim | MR FR-3: byte-identical to today | Dropped. An unflagged claim is `--pipeline worktree`. | AD 4.3. |
| `--worktree` with `--create` | MR FR-2 | `--pipeline` or `--submit` with `--create`: STOP `E-CLAIM-ONLY-FLAG`. | AD section 2. |

## 4. Command interface

```text
/sc:issue --claim <number|url> [--pipeline worktree|full|none] [--submit]
/sc:issue --create "<description>" [--depth quick|standard|deep] [--mode feature|bug] [--type <type>]
```

| Flag | Mode | Default | Values | Meaning |
|---|---|---|---|---|
| `--pipeline` | claim | `worktree` | `worktree`, `full`, `none` | How far the launched agent goes (section 1). `worktree` and `full` create the worktree and launch an agent; `none` creates no worktree and launches no agent |
| `--submit` | claim | off | no value | With `--pipeline full` only: after implementation the agent commits, pushes the feature branch to `origin` and runs `/sc:pr-submit --monitor 3`. Never merges |

STOP rules added to the command file, checked in this order after the existing ones (before Activation, no external call):

1. `--pipeline` or `--submit` with `--create`: STOP `E-CLAIM-ONLY-FLAG` ("--pipeline and --submit apply to --claim only"). `--depth`, `--mode` or `--type` with `--claim` still hit `E-CREATE-ONLY-FLAG` first.
2. A `--pipeline` value that is not one of the three: STOP, list `worktree`, `full`, `none`. `--pipeline` with no value: the same STOP.
3. `--submit` with a value, or with `--pipeline worktree` or `--pipeline none` or no `--pipeline`: STOP `E-SUBMIT-NEEDS-FULL` ("--submit needs --pipeline full").

Examples: `/sc:issue --claim 302` (worktree level), `/sc:issue --claim 302 --pipeline none`, `/sc:issue --claim 302 --pipeline full`, `/sc:issue --claim 302 --pipeline full --submit`.

`commands/issue.md` gets `version: "1.1.0"` (8 of 47 commands carry one; the claim behaviour changes for every user). `argument-hint`, Usage, Options table, Examples, Outputs, Boundaries and the claim paragraph are updated. Boundaries, Will Not: replace "Run any next-step command" with "Run `/sc:implement`, `/task`, a commit, a push or `/sc:pr-submit` itself (the launched agent may, at the level the user chose)", and add "Pass an Orca link flag" and "Merge anything". `SKILL.md` Will / Will Not mirror this.

## 5. Component architecture

```text
User: /sc:issue --claim N [--pipeline L] [--submit]
  |
  v
commands/issue.md  (flags, STOP rules incl. E-CLAIM-ONLY-FLAG, E-SUBMIT-NEEDS-FULL, Activation)
  |  Skill sc:issue-protocol
  v
skills/sc-issue-protocol/SKILL.md  (orchestrator)
  |-- refs/claim.md  Wave 0 (+ Orca check)   Waves 1-6 as today   Wave 7 (worktree)   Wave 8 (launch)
  |-- templates/next-steps.md   gains the "Plan boundary" line
  |-- templates/launch-prompt.md  (new)  blocks: common | worktree | full | submit
  |-- scripts/orca_worktree.py  (new, stdlib only; every orca and worktree-git call)
  |       preflight | prompt | worktree | launch        -> one JSON object each
  v
orca worktree list / create        ->  <wt> = Orca default location, branch <prefix>/issue-<N>
orca agent launch --agent claude --surface terminal --prompt "[sc-launch:v1:<nonce>] Read ... follow it."
orca terminal read --screen        ->  ccsession shim check (screen text, else the tab title via orca terminal show)
  |
  v
~/.claude/state/launch-level/pending/<nonce>   <- the hook's input (section 6); outside the worktree
```

Responsibilities: the **skill** decides what to run and prints; it makes every GitHub and ClickUp write as today and calls the script for every Orca call (the script is the seam the tests fake). No ref file is added (`test_all_five_refs_exist` stays true); the new template and script are added to the `SKILL.md` files table. No worker agent is involved in Waves 7 and 8.

## 6. Launch-level state and the hook interface (the hook side is built by #394)

The hook must read the level from state the launched agent cannot edit. Anything inside the worktree is editable by the agent, so the level never lives there. The claim script publishes a launch record in the hook's store, which the hook design defines (`docs/designs/sc-issue-launch-level-hook.md` sections 3 and 13, IR-1 to IR-3, IR-5):

| Item | Rule | Hook design |
|---|---|---|
| Store | `$HOME/.claude/state/launch-level/pending/<nonce>`. Built from path parts in the script, directories `0700`, files `0600`. | section 3 |
| Nonce | `secrets.token_hex(16)`: 32 lowercase hex characters, new for every launch | IR-2 |
| Content | exactly one word, no spaces: `worktree`, `full` or `full-submit`. `--pipeline none` writes nothing. | IR-1 |
| Publication | written to a temporary name that does not match the nonce pattern, then `os.rename` to `<nonce>`; a half-written record is never visible | IR-1 |
| Order | written before `orca agent launch`; removed if the launch fails, so no record outlives a launch that never happened | IR-1 |
| Prompt | `--prompt` starts with `[sc-launch:v1:<nonce>] `; the hook consumes the record on the session's first prompt and binds the session id | IR-2 |
| Failure to publish | no launch (`W-LAUNCH-FAILED`); the claim never starts an agent whose level it could not record | fail closed |
| Re-claim | a new nonce and a new session for every launch, never `--resume` (a re-claim that finds a `launch` entry launches nothing; the user removes the entry to launch again) | IR-5 |
| `pipeline.json` | not written (section 3) | IR-3 |

The word-to-level map the hook applies: `worktree` = W (planning only, `WA` after a person approves), `full` = F, `full-submit` = FS. The approval step of level `worktree` is the hook's (a person types `approved` or `/sc:implement` in the session). This design adds nothing for it. The hook enforces the stop; when the guard is missing or not effective the claim refuses the launch with `W-ENFORCEMENT-ABSENT` (no agent, no launch record), so no level runs as a prompt-only instruction.

`enforcement_hook` (contract field) reports the IR-4 preflight `enforcement_preflight()` in `orca_worktree.py` (`jq`, `uv`, the commands the guard calls, the installed guard, effective registration, `CLAUDE_CONFIG_DIR`): `installed` means the whole preflight passed (also when the launch then failed), `missing` means it failed and the launch was refused with `W-ENFORCEMENT-ABSENT`, and `null` means no preflight ran (no agent requested, `already_launched`, or a launch that failed before the preflight). The IR-7 check `l2_status()` only warns with `W-L2-ABSENT`.

## 7. Claim flow changes (`refs/claim.md`)

`<L>` is the `--pipeline` value, `<submit>` the `--submit` flag, `<wt>` the worktree's absolute path, `<main>` the main checkout (parent of the absolute git-common-dir, so a linked worktree still names it), `<B>` the default branch, `<D>` = `.dev/issues/<N>/`.

**Wave 0, new step 3** (after `gh auth status`, before the default-branch lookup and before `<D>` is created): `uv run --no-project python "<skill base>/scripts/orca_worktree.py" preflight`. `ok: false` is STOP `E-ORCA-REQUIRED` with the script's `detail`. No GitHub or ClickUp write has happened yet, and none happens after a STOP. The check also runs for `--pipeline none` (P1: Orca is a dependency), although `none` makes no later Orca call.

**Waves 1 to 4 and Wave 6** are unchanged.

**Wave 5, additions after `next-steps.md`:**

1. `next-steps.md` gets its `Plan boundary: after step <K>` line (FR-26). `<K>` is the number of the last step before the first step whose command is `/sc:implement` or `/task` (default D7). In the six default chains of `refs/chains.md` that gives: features, the step before `/sc:implement`; all three bug chains, step 1. If the first step is itself the implementation step, the line reads `Plan boundary: before step 1`. `--pipeline full` ignores the line.
2. For `<L>` other than `none`: `uv run --no-project python "<skill base>/scripts/orca_worktree.py" prompt --template "<skill base>/templates/launch-prompt.md" --level <L> [--submit] --number <N> --out "<D>/launch-prompt.md"`. It is written before Wave 7 so the copy carries it. The skill does not run any step of `next-steps.md` (B2).

**Wave 6** posts the two comments as today; its step 4 ("print the `next-steps.md` path and STOP") is replaced by Waves 7 and 8 and the final output below. Wave 7 runs only after both comments are posted. Any STOP in Waves 0-6, including `E-POST-FAILED`, means no Orca call after the Wave 0 check (FR-4).

**Wave 7: worktree (orchestrator, no worker).** `worktree` and `full` only; for `--pipeline none` the claim ends after the Wave 6 posts and Waves 7 and 8 do not run (amended 2026-11-08):

Run `orca_worktree.py worktree --repo <R> --number <N> --base origin/<B> --source <D>` and read its JSON. Any failure is a warning, never a STOP (FR-10).

**Wave 8: launch (orchestrator).** Runs when `<L>` is not `none` and Wave 7 `status` is `created` or `reused` (FR-21): `orca_worktree.py launch --number <N> --source <D> --level <L> [--submit]`; read its JSON. The record's `launch` entry (FR-27) makes the script return `already_launched` without calling `orca`.

**Final output, in this order (replaces "print the path and STOP"):**

1. The `next-steps.md` path, then `Worktree: <wt>` (status, `match_key`; on key `basename` or `branch` the line "reused a worktree not created by /sc:issue").
2. The "untracked, do not stage" line (MR 2.4) when it applies, and "run `make sync-dev` there first" when `<wt>/.claude/` is absent and the plan needs an unsynced primitive (MR 5 step 2).
3. Launch result: `launched` -> "Agent launched in <wt> (level <L>[, submit]). It stops at the plan boundary and waits; reply `approved` in its tab to let it continue." (`full` -> "It runs every step and stops after implementation." `full --submit` -> "It then commits, pushes <branch> and opens the PR through /sc:pr-submit; it never merges.") `already_launched` -> "agent already launched at <time>; remove the `launch` entry of <D>/worktree.json to launch again". `none` -> no `Worktree:` line, and "No worktree created and no agent launched. Open .dev/issues/<N>/next-steps.md in this checkout and run its commands in your own session."
4. Every warning with its remedy line (section 11), the worktree warning first.
5. The return contract (section 10) and STOP. The claim `status` stays `success` through any Wave 7 or Wave 8 failure: the assignment and comments cannot be undone (AD 4.5, FR-10, FR-29).

## 8. The script `scripts/orca_worktree.py`

Python standard library only, run as `uv run --no-project python "<skill base>/scripts/orca_worktree.py" <subcommand> ...` (the `clickup_claim.py` pattern). One JSON object on stdout. Exit 0 for every runtime outcome; exit 2 only for bad arguments (argparse). Every subprocess runs without a shell, with a timeout (120 s; `preflight` 30 s; each `terminal read` 15 s) and captured output. A timeout is a failed command, not an exception. FR-5: no other file calls `orca` or runs worktree git commands.

### 8.1 `preflight`

`orca status --json`. `{"ok": true}` when it exits 0, prints JSON with `ok: true` and `result.runtime.reachable: true`; otherwise `{"ok": false, "detail": "<first stderr line, or why the JSON failed the test>"}`. A missing `orca` binary gives the same shape (no separate code, P1).

### 8.2 `prompt`

Reads the template, keeps the `<!-- block:common -->` block plus `worktree` (when `--level worktree`) or `full` (when `--level full`), plus `submit` when `--submit` is passed, drops all other blocks and the block marker lines, replaces `<N>`, writes `--out`. `--submit` with `--level worktree` is bad arguments (exit 2). Output `{"status": "written", "path": "<out>"}`. This is rendered by code, not by the model, so the "do not run" lines cannot be dropped by a paraphrase.

### 8.3 `worktree`

Arguments `--repo <R> --number <N> --base origin/<B> --source <D>`. Output `{status, path, branch, match_key, warning, detail}` with `status` `created | reused | failed`. The algorithm is MR section 5 with AD section 4 applied; commands are MR section 4 exactly, each with a 120 s timeout:

```text
git rev-parse --path-format=absolute --git-common-dir
git fetch origin
git rev-parse --verify origin/<B>
orca worktree list --repo path:<main> --limit 500 --json
orca worktree create --repo path:<main> --name issue-<N> --base-branch origin/<B> --no-parent --comment "sc:issue <R>#<N>" --json
git -C <wt> rev-parse --path-format=absolute --git-common-dir
git -C <wt> ls-files .dev/issues/<N>
orca terminal list --worktree path:<wt> --json
orca terminal close --terminal <handle> --tab --json
```

The last two lines run only for a worktree the call just created (step 8). Amended 2026-11-08: the create still carries no `--agent`, because the claim must copy `<D>` (including `launch-prompt.md`), pass the repository check and write the launch-level pending record before the agent starts; Orca opens one plain first tab for a create without `--agent`, so the script closes it itself.

| Step | Rule | MR |
|---|---|---|
| 1 | Resolve `<main>` from the absolute git-common-dir. | 5 step 2 |
| 2 | List. Unusable (FR-15): `ok != true`, `result.truncated == true`, `result.hostScope.omittedHostIds` non-empty, zero rows, or no row with `isMainWorktree: true` (field names verified on a live `orca worktree list --json` on 2026-11-07). Then a `worktree.json` record that passes its guard is `reused` (key `record`, detail "unverified"); otherwise `failed`, `W-ORCA-LIST-FAILED`. | FR-15 |
| 3 | Look up among rows with `isArchived == false`, keys in order: `marker` (`comment` contains `sc:issue <R>#<N>` not followed by a digit), `record` (path in `<D>/worktree.json` passing the record guard, matched by `realpath`), `basename` (`^issue-<N>(-\|$)` on the path's basename), `branch` (same pattern on the last `/` segment of `branch`). Dedupe by row `id`; the first key with a hit decides. One live hit: `reused`. Stale hits (path missing) only: `failed`, `W-WORKTREE-STALE`. Two or more live hits: `failed`, `W-WORKTREE-AMBIGUOUS`, all paths in `detail`. None of these creates. | 2.5 |
| 4 | No hit: `origin/<B>` must resolve (else `failed`, `W-ORIGIN-BASE-MISSING`, no create); a failed `git fetch origin` with the ref present continues with `W-ORIGIN-BASE-STALE` (FR-16). Create. On exit 0 or a timeout, list once more (FR-15 applies) and take the row-id set difference: exactly one new id whose basename matches `^issue-<N>(-\|$)` is `created` (`<wt>` = that row's `path`, FR-20); zero new ids is `failed`, `W-WORKTREE-CREATE-FAILED` "created but not listed"; two or more is `failed`, `W-WORKTREE-AMBIGUOUS`, no copy, no record. A nonzero exit is `failed`, `W-WORKTREE-CREATE-FAILED` with the first stderr line; never auto-retried. | 5 step 5 |
| 5 | Copy `<D>` to `<wt>/.dev/issues/<N>/` file by file (MR 2.4): skip when source and destination share a `realpath`; exclude `worktree.json`; a file tracked in the worktree is skipped and named; a missing file is copied; an identical file is skipped; a differing untracked file is renamed to `<name>.prev` (replacing an older `.prev`), then copied and named. Never one recursive directory copy. `analysis/` is included. | 2.4 |
| 6 | Post-condition (FR-17): `<wt>` exists, its git-common-dir equals `<main>`'s by `realpath`, and every `<D>` file is byte-identical at the destination or named in a warning; else `failed` with a named warning (`W-WORKTREE-COPY-FAILED` for a copy problem, `W-WORKTREE-STALE` for a wrong common dir). | FR-17 |
| 7 | Only on `created` or `reused`, write `<D>/worktree.json` `{"path": "<absolute>", "status": "created\|reused"}`. It keeps an existing `launch` entry. It is never copied. | FR-18 |
| 8 | First-tab close (2026-11-08). Only when the status is `created` (never on a reused worktree), after step 6 passed and step 5 copied without error, and before the call returns, so before any launch. Read the create's `--json` reply (`{"ok": ..., "result": {...}}`): a missing, non-JSON, not-ok or timed-out reply, or `result.setup` or `result.defaultTabs` reporting anything, closes nothing. Otherwise run `orca terminal list --worktree path:<wt> --json`; when it lists exactly one terminal whose `agentIdentity` is absent or empty, run `orca terminal close --terminal <handle> --tab --json`. Any list or close failure, a malformed list reply, zero or several terminals, or a terminal with an agent leaves the tab and adds the warning `W-FIRST-TAB-LEFT` (reason in `detail`); it never changes `status`. A failed copy closes nothing and reports its own copy warning. | owner, 2026-11-08 |

The record guard: the path exists and its git-common-dir equals `<main>`'s, compared by `realpath`.

### 8.4 `launch`

Arguments `--number <N> --source <D> --level worktree|full [--submit]`. Output `{status, warning, detail, terminal, launched_at, enforcement_hook, hand_command, release, layers}` with `status` `launched | failed | already_launched`. `release` (the release instruction) and `layers` (the L1/L2 status lines) are set only for `launched`, else null; they are keys of the script's launch JSON, not fields of the ten-key claim contract in `SKILL.md`.

| Step | Rule |
|---|---|
| 1 | Read `<D>/worktree.json` through the record guard. Missing or failing: `failed`, `W-LAUNCH-FAILED` "no usable worktree record". |
| 2 | A `launch` entry exists: `already_launched` with its `at` time; no `orca` call, no record written. |
| 3 | The IR-4 preflight `enforcement_preflight()` (section 6). Any failure: `failed`, `W-ENFORCEMENT-ABSENT`, `enforcement_hook` `missing`, no agent, no launch record (#394; old default D3 is replaced). All pass: `enforcement_hook` `installed`. |
| 4 | Write `pending/<nonce>` (section 6). A write error: `failed`, `W-LAUNCH-FAILED`, no launch. |
| 5 | `orca agent launch --agent claude --worktree path:<wt> --surface terminal --prompt "[sc-launch:v1:<nonce>] Read .dev/issues/<N>/launch-prompt.md and follow it." --json`. No `--model` or `--effort` (AD FR-22). A nonzero exit, a timeout, or `ok != true`: remove the pending record, `failed`, `W-LAUNCH-FAILED` with the first stderr line, and `hand_command` (the same call without the marker, with the note "an agent started by hand is not governed by the hook; re-running the claim is preferred"). A timeout may have started an agent; `detail` says to check Orca before re-running. |
| 6 | Shim check (FR-28): take the terminal handle (the first string value under a key `handle` in the launch JSON, found by a recursive walk, because the `agent launch` result shape is UNVERIFIED), then up to 5 tries, 2 s apart. Each try reads `orca terminal read --terminal <handle> --screen --json` and passes when `result.terminal.tail` text holds `[ccsession]` or `Session name (Enter or Ctrl+C` (the question text of `.dev/evals/ccsession-orca-e2e-20261026/EVIDENCE.md`, check 11). **Amended 2026-11-08 (PR #455):** when the screen read misses, the same try runs `orca terminal show --terminal <handle> --json` and passes when `result.terminal.title` holds the session name ccsession gave the launch, `sc-launch-v1-<1 to 12 hex>-<MMDD>-<HHMMSS>-<4 hex>` (`ccsession --auto-name` builds it from the first words of the launch prompt, which starts with the `[sc-launch:v1:<nonce>]` marker, plus a stamp). Reason: a 60 s probe on 2026-11-08 saw the shim text on screen in one sample only, at about 1.6 s, before Claude's interface drew over it, and the scrollback had none either; the title keeps the name. Each `terminal read` and `terminal show` call has the 15 s terminal timeout. No handle, no readable screen and no matching title: keep the launch and set `W-LAUNCH-NOT-CCSESSION` ("this agent is NOT behind the ccsession shim, or could not be verified; close it"). The pending record stays. |
| 7 | Write `launch: {level, submit, at}` (UTC ISO time) into `<D>/worktree.json`, whatever the shim result, because an agent exists. Status `launched`. |

`worktree.json` is the only file the script writes besides the copy, the pending record and the rendered prompt. It never runs `git worktree add`, `orca worktree rm`, a commit, a push or a stage (FR-12).

## 9. Launch prompt template and `next-steps.md`

`templates/launch-prompt.md` holds four blocks, each opened by a marker line `<!-- block:<name> -->` (`common`, `worktree`, `full`, `submit`). The script (8.2) assembles `common` + `worktree`, or `common` + `full`, plus `submit` with `--submit`. Content of each block (the implementation writes the exact wording; these are the required statements):

| Block | Required statements |
|---|---|
| `common` | You were started by `/sc:issue --claim <N>`. Read `.dev/issues/<N>/issue-summary.md` and `.dev/issues/<N>/next-steps.md`. Run each step of `next-steps.md` in order by invoking its command through the Skill tool in this session, never by reading a command file and never inside a subagent. `next-steps.md` names the model tier it was written for; if this session runs on a lower one, say so in your first message. Never merge anything and never push to `master` or `main`. |
| `worktree` | Follow the steps up to the `Plan boundary` line of `next-steps.md`. Do not run `/sc:implement`, `/task`, `git commit`, `git push` or `/sc:pr-submit`. When the plan exists, print its path and `Waiting for approval`, then wait. A human approves by replying `approved` or by running the printed implement command; after that, run the remaining steps, still with no commit, push or `/sc:pr-submit`. |
| `full` | Run every step through the last one. Leave the changes in the working tree, stage nothing, and finish by printing `git status --short`. |
| `submit` | The owner asked for the commit and push by passing `--submit`. After the last step: check that no PR is already open or merged for this branch; commit with a conventional-commit message, staging `.dev/tasks` and the changed files, never anything under `.claude/` and never `.dev/issues/`; push the current feature branch to `origin` (never `master`); run `/sc:pr-submit --monitor 3 --head <branch> --title "..." --body "..."`. Never merge. |

The `full` and `common` blocks never contain the tokens `/sc:pr-submit`, `git push`, `git commit` or `--monitor`; only the `worktree` block (as a prohibition) and the `submit` block (as the instruction) do. A test pins this.

`templates/next-steps.md` gains one line under the title, set by the skill in Wave 5: `Plan boundary: after step <K>` (rule in section 7).

## 10. Files, state and the return contract

| Path | Written by | Notes |
|---|---|---|
| `<D>/launch-prompt.md` | `orca_worktree.py prompt` | not for `--pipeline none`; copied to `<wt>` with the other files |
| `<D>/worktree.json` | `orca_worktree.py worktree`, then `launch` | `{path, status}` plus, after a launch, `launch: {level, submit, at}`. Never copied. Not written for `--pipeline none`. To launch again, remove the `launch` entry. |
| `<wt>/.dev/issues/<N>/*` | `orca_worktree.py worktree` | copy of `<D>`; untracked, never staged by the claim (D24) |
| `$HOME/.claude/state/launch-level/pending/<nonce>` | `orca_worktree.py launch` | section 6; consumed by the hook |

Return contract, every claim (replaces the fixed list of `SKILL.md` for claim mode; create mode is unchanged and prints none of these):

```yaml
pipeline_level: worktree | full | none
submit: true | false
worktree_status: created | reused | failed | not_requested   # not_requested for none
worktree_path: <absolute path or null>
worktree_branch: <branch or null>
worktree_match_key: marker | record | basename | branch | null
worktree_warning: <W- code or null>
launch_status: launched | already_launched | failed | not_requested
launch_warning: <W- code or null>
enforcement_hook: installed | missing | null    # null: no agent requested, already_launched, or failed before the IR-4 preflight
```

For `none` no worktree is created: `worktree_status` is `not_requested` and `worktree_path`, `worktree_branch`, `worktree_match_key` and `worktree_warning` are `null`. `launch_status` is `not_requested` for `none` and when Wave 7 `failed`. On a STOP the fields that do not apply are `null`.

## 11. STOP and warning codes

New STOPs:

| Code | When |
|---|---|
| `E-ORCA-REQUIRED` | Wave 0: `orca_worktree.py preflight` returns `ok: false` |
| `E-CLAIM-ONLY-FLAG` | `--pipeline` or `--submit` with `--create` |
| `E-SUBMIT-NEEDS-FULL` | `--submit` without `--pipeline full` |

Warnings (the claim `status` stays `success` for all of them). `W-ORCA-MISSING` and the `skipped` status of MR no longer exist.

| Code | Field | When | Remedy line |
|---|---|---|---|
| `W-ORCA-LIST-FAILED` | worktree | list fails, times out or fails FR-15 and no guarded record exists (with one, reused "unverified") | check Orca, re-run the claim |
| `W-ORIGIN-BASE-MISSING` | worktree | `origin/<B>` does not resolve | `git fetch origin`, re-run |
| `W-ORIGIN-BASE-STALE` | worktree (status `created`) | fetch failed, ref present | `git fetch origin`, rebase in `<wt>` |
| `W-WORKTREE-CREATE-FAILED` | worktree | nonzero exit (first stderr line), or "created but not listed" | re-run; a finished create is reused |
| `W-WORKTREE-AMBIGUOUS` | worktree | two or more live hits, or two or more new ids | remove the extras, re-run |
| `W-WORKTREE-STALE` | worktree | stale hits only, or wrong git-common-dir | `git worktree prune`, then `orca worktree rm` |
| `W-WORKTREE-COPY-FAILED` | worktree (created, reused or failed) | files skipped as tracked, kept as `.prev`, or not copied | copy the named files by hand |
| `W-FIRST-TAB-LEFT` | worktree (status `created`) | the plain first tab could not be closed: unknown or not-ok create reply, setup or default tabs reported, list or close failed, zero or several terminals, or the one terminal runs an agent (2026-11-08) | close the plain tab in Orca by hand |
| `W-LAUNCH-FAILED` | launch | no usable record, pending record not written, or `orca agent launch` failed | re-run the claim; the hand command is printed for reference |
| `W-LAUNCH-NOT-CCSESSION` | launch (status `launched`) | in none of the 5 tries does the screen show `[ccsession]` or the session-name question, or the tab title carry the `sc-launch-v1-...` session name (see 8.4 step 6), or the terminal could not be read | "this agent is NOT behind the ccsession shim; close it"; Orca's Claude command must be `/home/coder/.local/bin/ccsession-orca` (OB-5) |
| `W-ENFORCEMENT-ABSENT` | launch (status `failed`; updated by #394) | the guard is missing or not effective (IR-4 preflight) | the launch was refused and no agent was started; fix each condition the `detail` names (usually `superclaude install`), then claim again |
| `W-L2-ABSENT` | launch (status `launched`; added by #394) | the worktree has no L2 pre-push layer | the L2 layer is not built yet and the limits are enforced by the L1 guard only; the agent was started |

A launch is never attempted when the worktree `status` is `failed` (FR-21).

## 12. Files to create or change

All under `src/superclaude/` unless stated. Nothing under `.claude/` is edited or staged; `make sync-dev` produces it. No `plugins/superclaude/` mirror of the issue command or skill exists (checked 2026-11-07), so none is added.

**Create**

| Path | Content |
|---|---|
| `skills/sc-issue-protocol/scripts/orca_worktree.py` | Section 8: four subcommands, stdlib only, `enforcement_preflight()` |
| `skills/sc-issue-protocol/templates/launch-prompt.md` | Section 9: four marked blocks |
| `tests/skills/test_issue_orca_worktree.py` | Section 13, fake `orca` on `PATH` |
| `.dev/brainstorms/20261105-024132-issue-claim-orca-worktree-flag/` | Copied in whole from the main checkout (untracked there) so it is committed with the PR; this design cites it |

**Change**

| Path | Change |
|---|---|
| `commands/issue.md` | `version: "1.1.0"`, `argument-hint`, Usage, two Options rows, three STOP rules (section 4), Examples, Outputs, Boundaries (Will, Will Not), claim paragraph (no longer "stops"; creates the worktree and launches an agent) |
| `skills/sc-issue-protocol/SKILL.md` | description and claim paragraph; files table rows for `scripts/orca_worktree.py` and `templates/launch-prompt.md`; claim steps 1, 6 and 7 (Wave 0 check, Wave 5 additions, Waves 7 and 8); claim return contract (section 10); error table rows (sections 4 and 11); Will / Will Not. Stays under 500 lines. |
| `skills/sc-issue-protocol/refs/claim.md` | Wave 0 step 3, Wave 5 additions, Wave 6 hand-off, Waves 7 and 8, final output (section 7). No new ref file. |
| `skills/sc-issue-protocol/templates/next-steps.md` | `Plan boundary: after step <K>` line |
| `core/HOW-WE-WORK.md` | the `/sc:issue` row: a claim now also creates a worktree and launches an agent at the chosen level, and never merges; then byte-copy the file to `plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md` |
| `docs/designs/sc-issue-command.md` | B2 row rewritten (section 2), new rows B16 to B18, and short "Amended 2026-11-07" notes in sections 1, 4, 7, 14, 16, 20 pointing to this design. Section 15's list of files gains the new script and template. |
| `docs/user-guide/commands.md` | the `/sc:issue` section: two flags, the four levels, examples, the "never merges" statement |
| `tests/commands/test_issue_command.py` | Options table pin becomes seven flags with the new values and defaults; STOP rule pins; Will Not text |
| `tests/skills/test_issue_protocol.py` | files-table pins, Wave 7 and 8 order, forbidden-flag scan, `Plan boundary` pin, prompt block pins |

Path rule: every new reference inside the primitives to another primitive uses the installed path and the script is called as `<skill base>/scripts/orca_worktree.py`, never a `src/superclaude/` path (FR-14). Pre-commit check: `grep -rn 'src/superclaude' src/superclaude/{commands,skills,agents,core,hooks}` shows no new hit.

## 13. Tests

All run with `uv run pytest`. The Orca and git seams are faked; no test calls a real `orca`, `gh` or the network.

**`tests/skills/test_issue_orca_worktree.py` (new).** A fake `orca` executable and a throwaway git repository with an `origin` remote are put first on `PATH`; the fake logs every argv and answers from JSON fixtures copied from the live list shape (nested `result.worktrees`, `isArchived`, `isMainWorktree`, prefixed full-ref branches, diverging path and branch, a stale row, a tracked file, a truncated page, `hostScope.omittedHostIds`). `HOME` is a temporary directory.

| Id | Case |
|---|---|
| PF-1, PF-2 | `preflight`: ok; not reachable, nonzero exit, and no `orca` on `PATH` all give `ok: false` with a detail |
| PR-1 to PR-4 | `prompt`: `worktree` and `full` keep their own block only; `--submit` adds the `submit` block; `--submit` with `worktree` exits 2; the `full` and `common` blocks and the rendered `full` output hold none of `/sc:pr-submit`, `git push`, `git commit`, `--monitor` |
| FO-1 | list fails while a guarded record exists: `reused`, key `record`, "unverified" |
| FO-2, FO-3, FO-4, FO-13 | key `marker`; empty marker falls to `basename`; suffix `issue-<N>-2`; prefixed branch matched on its last segment |
| FO-6 | a hang at the timeout is a failed command, not a crash |
| FO-7 | copy error: `failed`, `W-WORKTREE-COPY-FAILED` |
| FO-8, FO-10, FO-9 | ambiguity, stale, archived-only |
| FO-11 | opaque create JSON; zero and two new ids |
| FO-12 | each unusable-list condition (not ok, truncated, omitted host, zero rows, no main row), also after the create |
| FO-14, FO-15, FO-16 | `.prev` and tracked files; self-copy skipped; `worktree.json` never copied |
| FO-17 | `origin/<B>` missing: `W-ORIGIN-BASE-MISSING`, no create call; fetch failing with the ref present: `W-ORIGIN-BASE-STALE`, create called |
| FO-18 | exact create argv equals section 8.3 (note 2026-11-08: FO-18 stays, and the create still has no `--agent`, because the claim must copy `<D>` and write the pending record before its agent starts; a created run with a valid create reply now also records `terminal list` and `terminal close --tab` after the second `worktree list`); no forbidden flag (`--issue`, `--pr`, `--reference*`, `--linear-issue`, `--gitlab-*`, `--agent`, `--prompt`, `--model`, `--effort`, `--surface`, `--setup`, `--branch`, `--activate`, `--run-hooks`) in any list or create call |
| LA-1 | exact launch argv equals section 8.4 step 5, `--prompt` starts with `[sc-launch:v1:` plus 32 hex characters and `] `, no leading `/`, no `--model`, no `--effort`, no link flag |
| LA-2 | the pending record is a regular file of mode `0600` holding exactly `worktree`, `full` or `full-submit` (matching the call), published before the launch call, in a `0700` directory; the same nonce appears in the prompt |
| LA-3 | launch failure (nonzero exit, timeout, `ok: false`) removes the pending record and gives `W-LAUNCH-FAILED` with a hand command; pending write failure (read-only store) makes no launch call |
| LA-4 | a `launch` entry in the record: `already_launched`, no `orca` call, no new pending record; a record without one launches; the entry is written after a launch even when the shim check fails |
| LA-5 | shim check: a screen with `[ccsession]` and a screen with the session-name question pass; so does a plain screen whose tab title carries the `sc-launch-v1-<nonce>-<MMDD>-<HHMMSS>-<4 hex>` session name, also when the title only appears on a later try (2026-11-08, PR #455); seven non-matching titles (another session, no stamp, no clock, a non-hex nonce, an over-long stamp, none, a non-string) do not pass; `terminal show` uses the 15 s terminal timeout, not the 120 s default; a screen without any of these, an unreadable terminal and a launch JSON with no `handle` give `W-LAUNCH-NOT-CCSESSION` and status `launched` |
| LA-6 | `enforcement_hook`: `missing` and `W-ENFORCEMENT-ABSENT` without `$HOME/.claude/hooks/launch-level-guard.sh`; `installed` with an executable file. Updated by #394: `installed` only when the whole IR-4 preflight passes (executable guard with the version line, both registrations that can fire, `jq`, `uv`, the commands the guard calls, the Linux process interfaces); `missing` refuses the launch (no agent, no launch record), and `W-L2-ABSENT` is a warning on a `launched` result |
| LA-7 | no launch call for a `failed` worktree record and no pending record for `none` (the skill never calls `worktree` or `launch` for `none`, which creates no worktree since 2026-11-08; the test pins the skill text, ST-9) |
| ARG-1 | bad arguments of every subcommand exit 2 |

**Static pins** (`tests/commands/test_issue_command.py`, `tests/skills/test_issue_protocol.py`):

| Id | Pin |
|---|---|
| ST-1 | Options table has exactly `--claim`, `--create`, `--depth`, `--mode`, `--type`, `--pipeline`, `--submit` with the values and defaults of section 4 |
| ST-2 | STOP rules list `E-CLAIM-ONLY-FLAG`, `E-SUBMIT-NEEDS-FULL` and the `--pipeline` value STOP, all before Activation; `E-CREATE-ONLY-FLAG` is still first |
| ST-3 | Will Not no longer says "Run any next-step command"; it names `/sc:implement`, `/task`, a commit, a push and `/sc:pr-submit`; `version: "1.1.0"` |
| ST-4 | no forbidden Orca flag of FO-18 appears in the skill, refs, command or script outside the launch call's `--agent`, `--prompt`, `--surface` |
| ST-5 | still five refs (`test_all_five_refs_exist` unchanged); `scripts/orca_worktree.py` and `templates/launch-prompt.md` are in the `SKILL.md` files table and exist |
| ST-6 | in `refs/claim.md`, `preflight` is in Wave 0 before Wave 1; Wave 7 is after the Wave 6 posts; Wave 8 is after Wave 7 and says it runs for `created` or `reused` only |
| ST-7 | `templates/next-steps.md` contains `Plan boundary`; `refs/claim.md` states the `<K>` rule |
| ST-8 | `templates/launch-prompt.md` has exactly the four blocks; the `submit` block alone contains `/sc:pr-submit --monitor 3`, `git push` and the commit instruction; the `worktree` block contains the prohibition line; no other block contains those tokens |
| ST-9 | `refs/claim.md` skips Wave 7 and Wave 8 for `none` (Wave 7 since 2026-11-08) and names `launch-prompt.md` as written before Wave 7 |
| ST-10 | the claim return contract in `SKILL.md` lists the ten fields of section 10 |
| ST-11 | no `src/superclaude/` path in any new or changed primitive file; `HOW-WE-WORK.md` and its plugin mirror are byte-identical (existing parity test) |

The old MR cases FO-5 and AC-5 (no `orca`) are not built; `preflight` PF-2 covers the only place a missing binary matters.

Run before commit: `uv run pytest tests/commands tests/core tests/skills tests/recommend tests/cli/test_issue_body_templates.py -q`, `make lint`, the pinned ruff format check (`uv run ruff format --check` on the changed Python files with the version the repository pins), `make sync-dev`, `make verify-sync`.

## 14. Defaults chosen by this design

Each is a **design default**: a choice made where MR, AD and the hook design are silent or need reconciling. Change one by editing this table before `/sc:workflow` runs.

| ID | Default | Why |
|---|---|---|
| D1 | This design lives at `docs/designs/sc-issue-claim-pipeline-flag.md` | The existing design-doc folder |
| D2 | Worktree name `issue-<N>`, `--no-parent`, base `origin/<B>`, `--repo path:<main>`, `--comment "sc:issue <R>#<N>"`, no `--agent` on create | MR 2.3, AD 4.6: the create command stays as accepted; the agent is started by `agent launch` so a re-claimed worktree can be launched too. **Note 2026-11-08: D2 stays.** The owner's rule "every worktree gets an agent" does not move the agent into the create, because the claim must copy `.dev/issues/<N>/` (including `launch-prompt.md`), pass the repository check and write the launch-level pending record before the agent starts, and a failed copy must mean no agent. The owner approved closing Orca's plain first tab from the script instead (section 8.3, step 8) |
| D3 | Replaced by #394: a guard that is missing or not effective refuses the launch (`W-ENFORCEMENT-ABSENT`; no agent, no launch record) for every level; a missing L2 layer is the warning `W-L2-ABSENT` and the launch continues | Originally a warning because the hook did not exist; #394 built the guard and its IR-4 preflight. No governed claim is used on a real issue until OB-H1 item 1, OB-H2 and OB-H3 pass (hook design section 7, U1: item 1 before `full` or `--submit`, item 5 before any level; OB-H2 and OB-H3: its sections 11 and 14) |
| D4 | `version: "1.1.0"` in `commands/issue.md` only | MR 2.7 |
| D5 | Pending-record words `worktree`, `full`, `full-submit` | The hook design's `pending/<nonce>` content (section 3) |
| D6 | Shim check: 5 tries, 2 s apart (about 10 s when Orca answers at once; each Orca call has the 15 s terminal timeout). Each try passes on `[ccsession]` or the session-name question on the screen, or on the `sc-launch-v1-...` session name in the tab title (amended 2026-11-08, PR #455: the screen text is visible for only 1 to 2 s) | The ccsession question falls back to untagged after 30 s (EVIDENCE check 11), so the window is inside it; the whole call stays inside the 120 s timeout |
| D7 | `<K>` for `Plan boundary` is the last step before the first `/sc:implement` or `/task` step | Covers all six default chains and a `/sc:recommend` route that differs from them |
| D8 | No `pipeline.json` | Section 3 |
| D9 | No automatic retry of a launch and no `--retry-launch` in version 1 | A lost reply may have started an agent; the warning says to check Orca. A duplicate agent is recoverable, a silent second launch is not predictable |
| D10 | `--surface terminal` always | The agent must be a Claude CLI session behind the shim (P5, P7) |
| D11 | The launch prompt file is assembled by script code, not by the model | The prohibition lines are the only enforcement for a text-level route the #394 guard does not check; the guard (built, live observations pending) checks the routes its design lists |
| D12 | No `--model` or `--effort` on the launch | AD FR-22. The tier of the launched session is UNVERIFIED (section 15); the prompt asks the agent to report a mismatch with the tier named in `next-steps.md` |
| D13 | The launch happens only after both Wave 6 comments are posted and the worktree `status` is `created` or `reused` | FR-4, FR-21: nothing external happens for a claim that stopped early |
| D14 | `docs/user-guide/commands.md` and the `/sc:issue` row of `HOW-WE-WORK.md` are updated in the same change | Both say the claim "stops without running" the next steps, which becomes false |

## 15. Orca facts: verified and UNVERIFIED

Verified on 2026-11-07 against the installed `orca` CLI and the repository:

- `orca agent launch --agent <id> --worktree <selector> --prompt <text> --surface chat|terminal --model --effort --json`; `--surface terminal` always runs the agent CLI (`orca agent launch --help`). `orca terminal read --terminal <handle> --screen --json` returns `result.terminal.{handle, status, tail, ...}` (`orca terminal read --help`). `orca terminal show --terminal <handle> --json` returns `result.terminal.title` among other fields (`orca terminal show --help`; checked on a live terminal 2026-11-08). `orca status --json` returns `ok` and `result.runtime.reachable`.
- `orca worktree list --repo path:<main> --limit 500 --json` returns `result.{worktrees, truncated, totalCount, hostScope.omittedHostIds}`; each row has `id`, `path`, `branch` (a full ref such as `refs/heads/<prefix>/<name>`), `comment`, `isMainWorktree`, `isArchived`, `linkedIssue`, `linkedPR`, `projectId`.
- AD section 6 (observed 2026-11-05): a launched Claude is behind `/home/coder/.local/bin/ccsession-orca`; the prompt is the last argument, unchanged; the session runs without permission prompts; `.claude/commands/sc/` is absent in a new worktree. The ccsession question text is `Session name (Enter or Ctrl+C = untagged; untagged after 30s):`.
- #412 is merged: `agent launch --surface terminal` is the supported route for a Claude CLI session.

UNVERIFIED (each is checked in an observed run of section 17; none blocks the code):

- The JSON shape of `orca agent launch` (the terminal handle location); the script walks the result for a `handle` key.
- Whether `--comment` fills `comment` (marker key), the suffix on a taken name, and whether Orca contacts the upstream project its `projectId` names (MR R7).
- Whether the launched session carries an Orca worker preamble. If it does, the worker contract's turn-off of outward actions (WC-9) and its `/sc:pr-submit` refusal would block `--submit`.
- Which model tier the launched session runs on; whether the Orca Claude command still points at the ccsession wrapper (the shim check reports it each time).
- Whether the agent honours the plan boundary. Permission prompts are off, so the instruction alone is not enforcement; that is the hook's job (#394).

## 16. Order of work

One `/sc:workflow` plan, two phases (AD section 9). Both phases ship in one PR; the observed runs of section 17 are owner steps after merge.

- **Phase 1, the worktree step.** Command flags and STOP rules; SKILL.md and `refs/claim.md` Wave 0 check and Wave 7; `orca_worktree.py` with `preflight` and `worktree`; the `worktree.json` record; tests PF, FO, ST-1 to ST-3 and ST-5, ST-6; design-doc B2 and B16.
- **Phase 2, the launch.** `templates/launch-prompt.md`; `prompt` and `launch` subcommands, pending record, shim check; `Plan boundary` in `next-steps.md`; Wave 5 additions and Wave 8; return contract; tests PR, LA, ST-4, ST-7 to ST-11; docs (user guide, `HOW-WE-WORK.md` and mirror, B17, B18); `make sync-dev`, `make verify-sync`.

## 17. Acceptance criteria and observed runs

**Acceptance criteria for the implementation** (all verified by the tests of section 13):

1. `--pipeline` and `--submit` with `--create`, a bad `--pipeline` value and `--submit` without `--pipeline full` STOP with `E-CLAIM-ONLY-FLAG`, the value list and `E-SUBMIT-NEEDS-FULL`, with no `gh` and no `orca` call.
2. `preflight` failing STOPs `E-ORCA-REQUIRED` before any GitHub or ClickUp write.
3. The create and launch argument lists equal sections 8.3 and 8.4 exactly; no link flag and no other forbidden flag ever appears; the launch uses `--agent claude --surface terminal`.
4. The pending record exists, is a `0600` file with the right word and nonce, before the launch call; it is removed when the launch fails; `none` writes none; nothing level-related is written inside the worktree.
5. Any Wave 7 or Wave 8 failure leaves the claim `status: success` with the stated warning, and a failed worktree launches nothing.
6. A re-claim finds the worktree by one of four keys, creates nothing, refreshes only the copy, and launches nothing when the record has a `launch` entry.
7. The `worktree` prompt block contains the prohibition line, the `full` block does not mention commit, push or `/sc:pr-submit`, and only the `submit` block instructs them.
8. `make verify-sync` passes, the tests of section 13 pass, `make lint` and the pinned ruff format check pass, the `src/superclaude` path grep shows no new hit.

**Observed runs** (owner steps after merge, on test issues only; **not run in this change**): OB-1 default claim: one new row at Orca's default location, `git merge-base HEAD origin/<B>` equals `git rev-parse origin/<B>`, record `comment`, branch prefix, `projectId`, launch JSON shape. OB-2 repeat claim: no new row, `reused`, no second agent. OB-4 claim from a linked worktree: same `<main>`, no parent. OB-5 default claim: the agent starts behind the shim, writes a plan, waits and does not run `/sc:implement`; the process arguments show `ccsession-orca`. OB-6 `--pipeline full` on a trivial issue ends with finished implementation and no push. OB-7 `--pipeline none` launches nothing. OB-8 re-claim launches nothing. OB-9 `--pipeline full --submit` on a trivial issue pushes a branch and opens a PR on `IronbellyOrg/IronClaude` (check the URL). The launch-level guard of #394 now exists, but no governed claim is used on a real issue until OB-H1 item 1, OB-H2 and OB-H3 have passed (see the Update at the top); until then `full` and `--submit` are used on test issues only.

## 18. Amendments from the plan review (reflect, 2026-11-07)

`/sc:workflow` ran an advisory `/sc:reflect --mode pre` on the plan `TASK-WF-scIssueClaimPipe-20261107-063237` (verdict FAIL: 6 blocking findings B-1 to B-6, 6 MEDIUM, 8 minor; report `.dev/reflect/pre-TASK-WF-scIssueClaimPipe-20261107-063237-20261107063558/REPORT.md`). The workflow protocol does not edit a plan from findings, so the fixes live here. **Where this section and a task text or an earlier section disagree, this section wins.** The plan keeps the old text; the implementer applies these amendments while doing the task named in brackets.

### 18.1 Design changes (design first)

- **A1, tracked files (B-2) [Tasks 2, 4].** The `worktree` stdout gains `tracked_files` (paths under `.dev/issues/<N>/` that git tracks in `<wt>`) and `tracked_known` (false when `git ls-files` failed). The skill prints "untracked, do not stage" only when `tracked_known` is true and `tracked_files` is empty. When `git ls-files` fails, the copy copies missing files only: no file is renamed to `.prev` or overwritten, and `W-WORKTREE-COPY-FAILED` names the skipped files. Both fields live in the stdout, not in `worktree.json`.
- **A2, fork safety of the launch prompt (B-3) [Tasks 5, 7].** Every gh call in the `submit` block names `--repo IronbellyOrg/IronClaude`; the open-PR check is `gh pr list --repo IronbellyOrg/IronClaude --head <branch> --state all`. A new pin ST-12 runs `gh_lines_missing_repo` over `templates/launch-prompt.md`.
- **A3, shared return contract (B-4) [Task 7].** The ten claim fields are added to the shared contract of `SKILL.md`; `status`, `mode`, `issue_number`, `issue_url`, `dir`, `clickup_status`, `labels_applied`, `labels_missing` and `next_steps_path` stay, and create mode prints none of the new fields. ST-10 asserts both.
- **A4, ST-4 rule (B-5) [Task 7].** The test parses `scripts/orca_worktree.py` with `ast`, collects string constants that are whole `--` tokens, and compares them for equality with the forbidden list, ignoring constants inside the launch argv list. For markdown files it scans only lines that hold an `orca ` command and matches whole tokens (so `--prompt` never matches `--pr`, and `--issue-url` on a `clickup_claim.py` line is out of scope).
- **A5, warning precedence (M-2) [Tasks 2, 6].** `warning` holds the code that set the status; every other applicable code is appended to `detail` with its remedy line. `enforcement_hook` on `already_launched` is `null` (step 3 is skipped).
- **A6, re-claim keeps the running agent's files (M-5) [Tasks 4, 7].** When `<D>/worktree.json` already has a `launch` entry, Wave 5 does not rewrite `<D>/launch-prompt.md` and Wave 7 does not refresh it in the worktree.
- **A7, pending records (m-5).** Pending launch records are consumed by the #394 guard when a session binds to one; an unconsumed record is never pruned (owner decision O-15), so unused records keep accumulating.
- **A8, change table (B-1).** Section 12 gains `tests/skills/test_worker_contract.py`: one exact-text classification entry per new line that names `git add|commit|push|merge|stash|update-ref|worktree add|remove` or `gh pr|api` under `src/superclaude/{skills,commands,agents}`.

### 18.3 Amendments from the PR review (PR 425, 2026-11-07; they win over sections 8 and 9)

Augment and Codex reviewed PR 425; eight findings were verified against the code, reproduced as failing tests (`test_pr425_*` in `tests/skills/test_issue_orca_worktree.py`) and fixed.

- **A9, launch state per worktree.** `launch` also writes `{path, launch}` to `sc-issue-launch-<N>.json` in the worktree's own git directory (`git -C <wt> rev-parse --absolute-git-dir`): untracked by construction, never inside the working tree, removed with the worktree. `launch` returns `already_launched` when the source record or this file (whose `path` names this worktree) holds a `launch` entry, so a re-claim from inside the worktree, or from a checkout with a fresh record, starts no second agent. The `detail` of `already_launched` names both files; the user removes the entry from both to launch again. Section 8.4 step 2 and section 10 are read this way.
- **A10, a replacement worktree starts clean.** `write_record` keeps an earlier `launch` entry only for status `reused` at the same path; a `created` worktree, or one at a different path, has none.
- **A11, no write through a symlink.** `copy_issue_dir` refuses (error, `W-WORKTREE-COPY-FAILED`, nothing written) when any component from the worktree root down to a destination file's directory is a symlink; a symlinked source directory is named and not copied; an unreadable source directory is an error. The three writers of section 8 (`worktree.json`, `launch-prompt.md`, the launch entry) use a random exclusive temp file and a rename (`atomic_write_text`), never a fixed temp name.
- **A12, the repository comes from origin.** The `submit` block reads `gh pr list --repo <R> ...`; `prompt` takes a required `--repo <owner/repo>` and renders `<R>` next to `<N>`; Wave 5 passes the `<R>` printed by `origin_repo.py`. This replaces the literal fork name of A2; every `gh` call in the template still names a repository (ST-12). The `full` block now says in words (no pinned token) that it makes no commit, pushes no branch and opens no pull request, and the `submit` block says it replaces that rule.
- **A13, preflight.** A `result` that is not an object makes `preflight` print `{"ok": false, ...}` instead of raising.
- **A14, a stale prompt is replaced (round 2; refines A6).** The keep-the-prompt decision is in code: `prompt --source <D>` prints `{"status": "kept"}` and leaves `<D>/launch-prompt.md` alone only when `<D>/worktree.json` has a `launch` entry, its worktree still exists (the guarded record path check) and the prompt file exists. When the worktree was removed and replaced, the prompt is rendered again for the new launch level. Wave 5 passes `--source "<D>"`.
- **A15, a tracked backup name is not overwritten (round 2).** When a differing file would be renamed to `<file>.prev` and `.dev/issues/<N>/<file>.prev` is tracked in the worktree, `copy_issue_dir` names the file in the notes ("its backup name is tracked, so it was not overwritten") and skips it.
- **A16, the launch checks the prompt the agent will read (round 3, the one extra round the owner allowed for this High finding).** The copy never overwrites a tracked file, so a reused worktree can hold an older, more permissive `.dev/issues/<N>/launch-prompt.md` than the one rendered for this claim. `launch` now compares that file byte for byte with `<D>/launch-prompt.md` after the `already_launched` check and before it publishes a launch record or calls Orca. A missing, differing or symlinked worktree prompt, or a source without a rendered prompt, gives `status: failed` with `W-LAUNCH-FAILED`, a `detail` naming the file and the fix, and no `hand_command`; no agent starts and no record is written. The fix is the user's: make the worktree file match (a tracked copy needs `git rm` or `git checkout`) and re-run the claim. The copy itself still preserves tracked files and keeps its `W-WORKTREE-COPY-FAILED` note.
- **Not changed.** A re-claim from inside the worktree rewrites `launch-prompt.md` there with the same text (A6 covers the main-checkout case); the check and the write of the launch state are not atomic across two simultaneous claims. The wording of the removal instruction when the launch entry is found only in the git-directory file is left as is (a low-severity review note).

### 18.2 Implementer notes (plan only)

- **B-1 [Tasks 1 to 5, 7].** Run `uv run pytest tests/skills/test_worker_contract.py -q` in every task that adds or edits such a line. Choose the category per line (`never-worker`, `no-command`, `read-only` or `wc9-allowed`, as the existing sc-issue keys do). When a task edits an already-classified line (`SKILL.md:72`, `SKILL.md:135`, `refs/claim.md:9` and the other sc-issue keys), update its key in the same task.
- **M-1 [Tasks 1, 5].** Add the `SKILL.md` files-table row in the task that creates the file (the script in Task 1, the template in Task 5), so `test_every_named_path_exists_and_every_file_is_named` stays green.
- **B-6 [Tasks 1, 2, 5, 6, 7].** Add LA-7, a bad-argument case for each subcommand (ARG-1), the ST-5 template-row pin and the ST-6 Wave 8 half. Task 6 also carries: on a launch timeout `detail` says to check Orca before re-running; `hand_command` states that a hand-started agent is not governed by the hook; the pending record stays after a failed shim check.
- **M-3 [Tasks 3, 4, 7].** Rewrite `SKILL.md:3` and claim steps 6 and 7 for Waves 5, 7 and 8, and `commands/issue.md` lines 3, 68, 71 and 100 (the Outputs row says `launch-prompt.md` is not written for `--pipeline none`). Do not write the literal `--repo` in `commands/issue.md` (`tests/commands/test_issue_command.py:99-103`).
- **M-4.** Do Task 3 before Tasks 7 and 9.
- **M-6 [Tasks 1, 2].** `run()` marks a timeout apart from a nonzero exit; a create that times out is followed by the second list; add a create-timeout case.
- **Minor.** Add the Orca dependency (P1) to the plan's Constraints reading; run `uv run ruff format --check` on the script and its test in every task that edits them; add `tests/docs` to Task 9's test run; the new `HOW-WE-WORK.md` row is ASCII only; create each level of `$HOME/.claude/state/launch-level/pending` with mode `0700` (extend LA-2); name `launched_at` as the `already_launched` time field; do not use a `-k` filter that matches the module name.

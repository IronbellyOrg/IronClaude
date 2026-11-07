# Reviewer 2 brief (qa lens)

This is a UC-1 pre-execution review: there is no diff. Audit the TASKLIST at `.dev/tasks/to-do/TASK-WF-scIssueClaimPipe-20261107-063237/TASK-WF-scIssueClaimPipe-20261107-063237.md` against the SPEC (the design) at `.dev/tasks/to-do/TASK-WF-scIssueClaimPipe-20261107-063237/source.md`. A 'deviation' here is a place where the plan omits, contradicts, reorders or over-reaches the design, or would break an existing test or invariant. Map classes as: Authorized = plan goes beyond the design with a stated basis; Necessary = plan departs from the design for a stated, real constraint; Drift = plan omits or alters a design instruction with no rationale; Regression = plan step would break an existing test, invariant or documented rule. Ground every finding at file:line (plan lines or spec lines or repository files). Read the live repository only to verify a cited fact; do not modify anything.

Lens: Coverage and acceptance. Audit the coverage matrix AGAINST the spec body in your grounding hunks; surface any requirement-bearing span absent from the matrix (parsed or inferred) as a finding. Also check that each task's acceptance criteria are observable and sufficient for the requirement it carries.

## T1 card excerpt

```yaml
  - id: F-4
    kind: coverage-gap
    severity_proposed: MINOR
    claim: "Requirement INF-001 (Orca is a dependency; no non-Orca accommodation anywhere) has no task and is absent from the plan Constraints."
    evidence:
      - "source.md:39"
      - "plan:17 ## Constraints (no such line)"
    recommendation: "Add one Constraints bullet."
```

## Grounding hunks

codegraph run state: index_state=fresh checked_at=2026-11-07T06:36:50Z worktree_root=/home/coder/workspaces/worktrees/IronClaude/sc-issue-claim-pipeline-flag projectPath=/home/coder/workspaces/worktrees/IronClaude/sc-issue-claim-pipeline-flag

### .dev/tasks/to-do/TASK-WF-scIssueClaimPipe-20261107-063237/TASK-WF-scIssueClaimPipe-20261107-063237.md:1-28

````markdown
---
schema: workflow-plan/1.2
source: ./source.md
strategy: systematic
depth: quick
slug: TASK-WF-scIssueClaimPipe-20261107-063237
version: "1"
priority: Medium
created_date: "2026-11-07"
---

# Add the --pipeline and --submit flags to /sc:issue --claim

Source: ./source.md
Goal: `/sc:issue --claim <N> [--pipeline worktree|full|none] [--submit]` creates or reuses an Orca worktree `issue-<N>`, launches a Claude Code agent behind the ccsession shim at the chosen level, and records the level in the hook's launch store, with all behaviour covered by unit tests that use a fake `orca`.

## Constraints

- Edit canonical sources under `src/superclaude/` only, then run `make sync-dev`. Never stage anything under `.claude/` (only `.claude/settings.json` is tracked). `.dev/tasks` is staged with `git add .dev/tasks`; staging is not committing.
- Python through UV only: `uv run pytest`, `uv run --no-project python <script>`. No `python -m`, no bare `pip`.
- No test calls a real `orca`, `gh`, the network or a real agent. A fake `orca` executable and a throwaway git repository are put first on `PATH`; `HOME` is a temporary directory in every test that writes the launch store.
- GitHub target is `IronbellyOrg/IronClaude` only; no Orca link flag (`--issue`, `--pr`, `--reference*`, `--linear-issue`, `--gitlab-*`) anywhere. `--agent`, `--prompt`, `--surface` appear only in the `orca agent launch` call.
- Do not build the enforcement hook of issue 394 (no `launch-level-guard.sh`, no `pre-push` hook, no hooks.json change). Only the launch record it reads is written.
- No `src/superclaude/` path inside any installed primitive (command, skill, ref, template). The skill calls the script as `<skill base>/scripts/orca_worktree.py`.
- No new ref file in `src/superclaude/skills/sc-issue-protocol/refs/` (the five-refs test stays true).
- Design: `docs/designs/sc-issue-claim-pipeline-flag.md` (this plan's source, section numbers below refer to it). Requirements: the folder `.dev/brainstorms/20261105-024132-issue-claim-orca-worktree-flag/` (`merged-requirements.md` as amended by `launch-levels-addendum.md`), already copied into this repository and part of the change.

## Phase 1: The worktree step
````

### .dev/tasks/to-do/TASK-WF-scIssueClaimPipe-20261107-063237/source.md:1-11

````markdown
# Design: `/sc:issue --claim --pipeline` (worktree, launch levels, `--submit`)

**Status:** Design only (nothing implemented). Next: `/sc:workflow docs/designs/sc-issue-claim-pipeline-flag.md --depth quick --handoff none`, then `/sc:implement` on the plan it prints.
**Issue:** none. This feature had no tracking issue. Related follow-on: IronbellyOrg/IronClaude #394 (launch-level enforcement hook, `docs/designs/sc-issue-launch-level-hook.md`). Launch rule from #412 (merged).
**Branch:** `ironbelly/sc-issue-claim-pipeline-flag`
**Source requirements:** `.dev/brainstorms/20261105-024132-issue-claim-orca-worktree-flag/merged-requirements.md` ("MR") as amended by `launch-levels-addendum.md` in the same folder ("AD", revision 2, after the owner's four corrections of 2026-11-05). Where MR and AD differ, AD wins. Where AD and the hook design differ on hook state, the hook design wins (section 3).
**Source of truth:** `src/superclaude/` -> `make sync-dev` -> `.claude/` (never stage `.claude/`).
**Produced by:** `/sc:design sc-issue-claim-pipeline-flag --type component --format spec`, 2026-11-07.

---

````

### .dev/tasks/to-do/TASK-WF-scIssueClaimPipe-20261107-063237/source.md:12-32

````markdown
## 1. Purpose and scope

Today `/sc:issue --claim` assigns the issue, checks its accuracy, writes `next-steps.md` and stops. The user then opens a worktree and a session by hand. This design adds two claim-only flags so the claim does that hand-off itself, at a level the user picks:

| Level | Flag | What happens after the claim's Waves 0-6 | Agent stops at |
|---|---|---|---|
| `worktree` (default) | `--pipeline worktree` or nothing | An Orca worktree `issue-<N>` is created (or reused) and a Claude Code agent is launched in it. It runs `next-steps.md` up to the plan boundary. | An approved plan: it prints the plan path and "Waiting for approval" until a human approves |
| `full` | `--pipeline full` | Same, but the agent runs every step including `/sc:implement` or `/task`. | Finished implementation, unstaged, uncommitted, unpushed |
| `full` + `--submit` | `--pipeline full --submit` | Same, then the agent commits, pushes a feature branch to `origin` and runs `/sc:pr-submit --monitor 3`. | A pushed branch with an open PR on the fork |
| `none` | `--pipeline none` | The worktree is created (or reused); no agent is launched. | Nothing runs; the user opens the worktree |

No level merges anything. Humans only review and merge; nobody opens a PR by hand, because with `--submit` the agent's `/sc:pr-submit` opens it.

**In scope:** the two flags and their STOP rules; a Wave 0 Orca check; Wave 7 (worktree, from MR as amended by AD section 4); Wave 8 (launch behind the ccsession shim); the launch prompt template; the `Plan boundary` line in `next-steps.md`; the launch-level state the hook of #394 reads; the new contract fields; tests and docs.

**Out of scope:**

- The enforcement hook (`launch-level-guard.sh`, its L2 `pre-push` layer, `jq` and registration checks): issue #394. This design only produces the state that hook consumes (section 6) and reports whether the hook script is present.
- A flag value for model or effort, a lock for racing claims, `linkedIssue` matching, automatic worktree removal, any Orca link flag, any behaviour for a machine without Orca.
- Running any live claim, worktree create or agent launch against a real issue. Verification in this change is unit tests with a fake `orca`; the observed runs of section 17 are owner steps after merge.

````

### .dev/tasks/to-do/TASK-WF-scIssueClaimPipe-20261107-063237/source.md:33-50

````markdown
## 2. Binding decisions

"Owner" is the owner's decisions of 2026-11-05 (AD section 1) and the task brief of 2026-11-07. B1 to B15 of `docs/designs/sc-issue-command.md` still bind, except B2, which is rewritten here.

| # | Decision | Source |
|---|---|---|
| P1 | Orca is a dependency. No code, warning, option or document text exists only for a project without Orca. | Owner, AD 1.2 |
| P2 | One flag, `--pipeline worktree\|full\|none`, default `worktree`. The `--worktree` flag of MR does not exist. | Owner, AD 1.6 |
| P3 | `--submit` is a second flag, valid with `--pipeline full` only. It turns on commit, push of a feature branch and `/sc:pr-submit --monitor 3`. It never merges. | Owner, AD 1.4 |
| P4 | The default stop is an approved plan. `full` adds implementation. `none` launches no agent but still creates the worktree. | Owner, AD 1.3 |
| P5 | The launched agent is Claude Code behind the ccsession shim, always. | Owner, AD 1.5 |
| P6 | **B2 is rewritten (new text below).** B16 (worktree after `next-steps.md`), B17 (launch levels) and B18 (`--submit`) are new design decisions in `docs/designs/sc-issue-command.md`. | Owner, AD 1.1 and 3 |
| P7 | The agent is started with `orca agent launch --agent claude --surface terminal`, a Claude CLI session. Never a plain terminal, and never `--surface chat` (a chat is not behind the shim). | #412 (merged), AD FR-22 |
| P8 | Nothing here builds the hook. The level must be readable by the hook from state the agent cannot edit (section 6). | Owner, task brief, #394 |
| P9 | Order of work: `/sc:design`, `/sc:workflow --depth quick`, `/sc:implement`, `/sc:pr-submit --monitor 3`. | Owner, task brief |

**B2 (rewritten):** the claim writes the summary and `next-steps.md`, creates a worktree, and launches one agent in it. Neither the `/sc:issue` skill nor the default agent runs `/sc:implement` or `/task`. `--pipeline full` lets the agent run them. `--submit` additionally lets it commit, push and run `/sc:pr-submit`. The `/sc:issue` skill itself still runs no next-step command; the launched agent does. Merging is never done by any level.

````

### .dev/tasks/to-do/TASK-WF-scIssueClaimPipe-20261107-063237/source.md:51-65

````markdown
## 3. Reconciliations (where the source documents disagree or are silent)

| Point | Source text | This design | Why |
|---|---|---|---|
| Level state file | AD FR-31: the skill writes `<wt>/.dev/issues/<N>/pipeline.json` as the hook's input | **Not built.** The hook's input is a launch record outside the worktree (section 6). | The hook design (IR-1 to IR-3) is later (2026-11-06) and says `pipeline.json` is documentation only: the agent can edit anything inside the worktree. A file nothing reads is not written. |
| Git `pre-push` layer | AD FR-32: the claim installs a `pre-push` check in the new worktree | **Not built by the claim.** The hook feature's own installer owns it (hook design 19.2). The claim reports `enforcement_hook`. | Hook design 19 answers AD's open questions (place, chaining, removal) and makes installation part of #394. |
| Hook refusal rules | Hook IR-4 and IR-7: refuse a governed launch when `jq`, the script, effective registration or L2 is missing | **Not built.** A missing hook script gives warning `W-ENFORCEMENT-ABSENT`; the launch proceeds (default D3). | The hook does not exist yet, and AD section 9 says phase 2 does not wait for it; OB-6 to OB-9 must run before it exists. #394 turns the warning into a refusal by extending one function (section 8). |
| `launch_status` values | AD FR-30: `launched \| failed \| not_requested` | Adds `already_launched` | AD FR-27 needs a state for a re-claim that finds a `launch` entry. |
| Launch prompt | AD FR-22: one plain sentence, no leading `/` | The sentence is prefixed with the hook's marker `[sc-launch:v1:<nonce>] ` (hook IR-2). The prefix starts with `[`, so the no-leading-`/` rule holds. | The hook binds the session by that marker. |
| Create JSON shape | MR R2 UNVERIFIED | AD observed `result.worktree.{id, path, branch, ...}`. FR-20 (path from a row-id difference) stays; the field is not relied on. | The set difference works with an opaque create result. |
| `worktree_warning` holds one code | MR open item | The code that set the status wins; any other goes in `detail`. Launch codes use their own field `launch_warning`. | Two independent steps can each warn. |
| Statuses | MR: `created \| reused \| skipped \| failed` | `created \| reused \| failed` | AD 4.2 and 4.4: `skipped` existed only for a missing `orca`. |
| Unflagged claim | MR FR-3: byte-identical to today | Dropped. An unflagged claim is `--pipeline worktree`. | AD 4.3. |
| `--worktree` with `--create` | MR FR-2 | `--pipeline` or `--submit` with `--create`: STOP `E-CLAIM-ONLY-FLAG`. | AD section 2. |

````

### .dev/tasks/to-do/TASK-WF-scIssueClaimPipe-20261107-063237/source.md:66-87

````markdown
## 4. Command interface

```text
/sc:issue --claim <number|url> [--pipeline worktree|full|none] [--submit]
/sc:issue --create "<description>" [--depth quick|standard|deep] [--mode feature|bug] [--type <type>]
```

| Flag | Mode | Default | Values | Meaning |
|---|---|---|---|---|
| `--pipeline` | claim | `worktree` | `worktree`, `full`, `none` | How far the launched agent goes (section 1). Every value creates the worktree; `none` launches no agent |
| `--submit` | claim | off | no value | With `--pipeline full` only: after implementation the agent commits, pushes the feature branch to `origin` and runs `/sc:pr-submit --monitor 3`. Never merges |

STOP rules added to the command file, checked in this order after the existing ones (before Activation, no external call):

1. `--pipeline` or `--submit` with `--create`: STOP `E-CLAIM-ONLY-FLAG` ("--pipeline and --submit apply to --claim only"). `--depth`, `--mode` or `--type` with `--claim` still hit `E-CREATE-ONLY-FLAG` first.
2. A `--pipeline` value that is not one of the three: STOP, list `worktree`, `full`, `none`. `--pipeline` with no value: the same STOP.
3. `--submit` with a value, or with `--pipeline worktree` or `--pipeline none` or no `--pipeline`: STOP `E-SUBMIT-NEEDS-FULL` ("--submit needs --pipeline full").

Examples: `/sc:issue --claim 302` (worktree level), `/sc:issue --claim 302 --pipeline none`, `/sc:issue --claim 302 --pipeline full`, `/sc:issue --claim 302 --pipeline full --submit`.

`commands/issue.md` gets `version: "1.1.0"` (8 of 47 commands carry one; the claim behaviour changes for every user). `argument-hint`, Usage, Options table, Examples, Outputs, Boundaries and the claim paragraph are updated. Boundaries, Will Not: replace "Run any next-step command" with "Run `/sc:implement`, `/task`, a commit, a push or `/sc:pr-submit` itself (the launched agent may, at the level the user chose)", and add "Pass an Orca link flag" and "Merge anything". `SKILL.md` Will / Will Not mirror this.

````

### .dev/tasks/to-do/TASK-WF-scIssueClaimPipe-20261107-063237/source.md:88-113

````markdown
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
orca terminal read --screen        ->  ccsession shim check
  |
  v
~/.claude/state/launch-level/pending/<nonce>   <- the hook's input (section 6); outside the worktree
```

Responsibilities: the **skill** decides what to run and prints; it makes every GitHub and ClickUp write as today and calls the script for every Orca call (the script is the seam the tests fake). No ref file is added (`test_all_five_refs_exist` stays true); the new template and script are added to the `SKILL.md` files table. No worker agent is involved in Waves 7 and 8.

````

### .dev/tasks/to-do/TASK-WF-scIssueClaimPipe-20261107-063237/source.md:114-133

````markdown
## 6. Launch-level state and the hook interface (design for #394, nothing hook-side built)

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

The word-to-level map the hook applies: `worktree` = W (planning only, `WA` after a person approves), `full` = F, `full-submit` = FS. The approval step of level `worktree` is the hook's (a person types `approved` or `/sc:implement` in the session). This design adds nothing for it; until the hook exists the stop at the plan is an instruction in the launch prompt only, and the claim says so (`W-ENFORCEMENT-ABSENT`).

`enforcement_hook` (contract field) is `installed` when `$HOME/.claude/hooks/launch-level-guard.sh` exists and is executable, else `missing`. It does not claim the hook is registered or effective. The check is one function, `enforcement_status()` in `orca_worktree.py`; #394 extends it with the IR-4 and IR-7 refusals (`jq`, registration, `CLAUDE_CONFIG_DIR`, L2) without touching the flag design.

````

### .dev/tasks/to-do/TASK-WF-scIssueClaimPipe-20261107-063237/source.md:134-162

````markdown
## 7. Claim flow changes (`refs/claim.md`)

`<L>` is the `--pipeline` value, `<submit>` the `--submit` flag, `<wt>` the worktree's absolute path, `<main>` the main checkout (parent of the absolute git-common-dir, so a linked worktree still names it), `<B>` the default branch, `<D>` = `.dev/issues/<N>/`.

**Wave 0, new step 3** (after `gh auth status`, before the default-branch lookup and before `<D>` is created): `uv run --no-project python "<skill base>/scripts/orca_worktree.py" preflight`. `ok: false` is STOP `E-ORCA-REQUIRED` with the script's `detail`. No GitHub or ClickUp write has happened yet, and none happens after a STOP.

**Waves 1 to 4 and Wave 6** are unchanged.

**Wave 5, additions after `next-steps.md`:**

1. `next-steps.md` gets its `Plan boundary: after step <K>` line (FR-26). `<K>` is the number of the last step before the first step whose command is `/sc:implement` or `/task` (default D7). In the six default chains of `refs/chains.md` that gives: features, the step before `/sc:implement`; all three bug chains, step 1. If the first step is itself the implementation step, the line reads `Plan boundary: before step 1`. `--pipeline full` ignores the line.
2. For `<L>` other than `none`: `uv run --no-project python "<skill base>/scripts/orca_worktree.py" prompt --template "<skill base>/templates/launch-prompt.md" --level <L> [--submit] --number <N> --out "<D>/launch-prompt.md"`. It is written before Wave 7 so the copy carries it. The skill does not run any step of `next-steps.md` (B2).

**Wave 6** posts the two comments as today; its step 4 ("print the `next-steps.md` path and STOP") is replaced by Waves 7 and 8 and the final output below. Wave 7 runs only after both comments are posted. Any STOP in Waves 0-6, including `E-POST-FAILED`, means no Orca call after the Wave 0 check (FR-4).

**Wave 7: worktree (orchestrator, no worker).** Every `--pipeline` value:

Run `orca_worktree.py worktree --repo <R> --number <N> --base origin/<B> --source <D>` and read its JSON. Any failure is a warning, never a STOP (FR-10).

**Wave 8: launch (orchestrator).** Runs when `<L>` is not `none` and Wave 7 `status` is `created` or `reused` (FR-21): `orca_worktree.py launch --number <N> --source <D> --level <L> [--submit]`; read its JSON. The record's `launch` entry (FR-27) makes the script return `already_launched` without calling `orca`.

**Final output, in this order (replaces "print the path and STOP"):**

1. The `next-steps.md` path, then `Worktree: <wt>` (status, `match_key`; on key `basename` or `branch` the line "reused a worktree not created by /sc:issue").
2. The "untracked, do not stage" line (MR 2.4) when it applies, and "run `make sync-dev` there first" when `<wt>/.claude/` is absent and the plan needs an unsynced primitive (MR 5 step 2).
3. Launch result: `launched` -> "Agent launched in <wt> (level <L>[, submit]). It stops at the plan boundary and waits; reply `approved` in its tab to let it continue." (`full` -> "It runs every step and stops after implementation." `full --submit` -> "It then commits, pushes <branch> and opens the PR through /sc:pr-submit; it never merges.") `already_launched` -> "agent already launched at <time>; remove the `launch` entry of <D>/worktree.json to launch again". `none` -> "No agent launched. Open <wt> and run .dev/issues/<N>/next-steps.md there."
4. Every warning with its remedy line (section 11), the worktree warning first.
5. The return contract (section 10) and STOP. The claim `status` stays `success` through any Wave 7 or Wave 8 failure: the assignment and comments cannot be undone (AD 4.5, FR-10, FR-29).

````

### .dev/tasks/to-do/TASK-WF-scIssueClaimPipe-20261107-063237/source.md:163-216

````markdown
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
```

| Step | Rule | MR |
|---|---|---|
| 1 | Resolve `<main>` from the absolute git-common-dir. | 5 step 2 |
| 2 | List. Unusable (FR-15): `ok != true`, `result.truncated == true`, `result.hostScope.omittedHostIds` non-empty, zero rows, or no row with `isMainWorktree: true` (field names verified on a live `orca worktree list --json` on 2026-11-07). Then a `worktree.json` record that passes its guard is `reused` (key `record`, detail "unverified"); otherwise `failed`, `W-ORCA-LIST-FAILED`. | FR-15 |
| 3 | Look up among rows with `isArchived == false`, keys in order: `marker` (`comment` contains `sc:issue <R>#<N>` not followed by a digit), `record` (path in `<D>/worktree.json` passing the record guard, matched by `realpath`), `basename` (`^issue-<N>(-\|$)` on the path's basename), `branch` (same pattern on the last `/` segment of `branch`). Dedupe by row `id`; the first key with a hit decides. One live hit: `reused`. Stale hits (path missing) only: `failed`, `W-WORKTREE-STALE`. Two or more live hits: `failed`, `W-WORKTREE-AMBIGUOUS`, all paths in `detail`. None of these creates. | 2.5 |
| 4 | No hit: `origin/<B>` must resolve (else `failed`, `W-ORIGIN-BASE-MISSING`, no create); a failed `git fetch origin` with the ref present continues with `W-ORIGIN-BASE-STALE` (FR-16). Create. On exit 0 or a timeout, list once more (FR-15 applies) and take the row-id set difference: exactly one new id whose basename matches `^issue-<N>(-\|$)` is `created` (`<wt>` = that row's `path`, FR-20); zero new ids is `failed`, `W-WORKTREE-CREATE-FAILED` "created but not listed"; two or more is `failed`, `W-WORKTREE-AMBIGUOUS`, no copy, no record. A nonzero exit is `failed`, `W-WORKTREE-CREATE-FAILED` with the first stderr line; never auto-retried. | 5 step 5 |
| 5 | Copy `<D>` to `<wt>/.dev/issues/<N>/` file by file (MR 2.4): skip when source and destination share a `realpath`; exclude `worktree.json`; a file tracked in the worktree is skipped and named; a missing file is copied; an identical file is skipped; a differing untracked file is renamed to `<name>.prev` (replacing an older `.prev`), then copied and named. Never one recursive directory copy. `analysis/` is included. | 2.4 |
| 6 | Post-condition (FR-17): `<wt>` exists, its git-common-dir equals `<main>`'s by `realpath`, and every `<D>` file is byte-identical at the destination or named in a warning; else `failed` with a named warning (`W-WORKTREE-COPY-FAILED` for a copy problem, `W-WORKTREE-STALE` for a wrong common dir). | FR-17 |
| 7 | Only on `created` or `reused`, write `<D>/worktree.json` `{"path": "<absolute>", "status": "created\|reused"}`. It keeps an existing `launch` entry. It is never copied. | FR-18 |

The record guard: the path exists and its git-common-dir equals `<main>`'s, compared by `realpath`.

### 8.4 `launch`

Arguments `--number <N> --source <D> --level worktree|full [--submit]`. Output `{status, warning, detail, terminal, launched_at, enforcement_hook, hand_command}` with `status` `launched | failed | already_launched`.

| Step | Rule |
|---|---|
| 1 | Read `<D>/worktree.json` through the record guard. Missing or failing: `failed`, `W-LAUNCH-FAILED` "no usable worktree record". |
| 2 | A `launch` entry exists: `already_launched` with its `at` time; no `orca` call, no record written. |
| 3 | `enforcement_hook = enforcement_status()` (section 6). `missing` sets `W-ENFORCEMENT-ABSENT` ("levels are instructions in the prompt only until the hook of #394 ships"); it does not stop the launch (default D3). |
| 4 | Write `pending/<nonce>` (section 6). A write error: `failed`, `W-LAUNCH-FAILED`, no launch. |
| 5 | `orca agent launch --agent claude --worktree path:<wt> --surface terminal --prompt "[sc-launch:v1:<nonce>] Read .dev/issues/<N>/launch-prompt.md and follow it." --json`. No `--model` or `--effort` (AD FR-22). A nonzero exit, a timeout, or `ok != true`: remove the pending record, `failed`, `W-LAUNCH-FAILED` with the first stderr line, and `hand_command` (the same call without the marker, with the note "an agent started by hand is not governed by the hook; re-running the claim is preferred"). A timeout may have started an agent; `detail` says to check Orca before re-running. |
| 6 | Shim check (FR-28): take the terminal handle (the first string value under a key `handle` in the launch JSON, found by a recursive walk, because the `agent launch` result shape is UNVERIFIED), then `orca terminal read --terminal <handle> --screen --json` up to 5 times, 2 s apart. Pass when `result.terminal.tail` text holds `[ccsession]` or `Session name (Enter or Ctrl+C` (the question text of `.dev/evals/ccsession-orca-e2e-20261026/EVIDENCE.md`, check 11). No handle, no readable screen or no match: keep the launch and set `W-LAUNCH-NOT-CCSESSION` ("this agent is NOT behind the ccsession shim, or could not be verified; close it"). The pending record stays. |
| 7 | Write `launch: {level, submit, at}` (UTC ISO time) into `<D>/worktree.json`, whatever the shim result, because an agent exists. Status `launched`. |

`worktree.json` is the only file the script writes besides the copy, the pending record and the rendered prompt. It never runs `git worktree add`, `orca worktree rm`, a commit, a push or a stage (FR-12).

````

### .dev/tasks/to-do/TASK-WF-scIssueClaimPipe-20261107-063237/source.md:217-231

````markdown
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

````

### .dev/tasks/to-do/TASK-WF-scIssueClaimPipe-20261107-063237/source.md:232-257

````markdown
## 10. Files, state and the return contract

| Path | Written by | Notes |
|---|---|---|
| `<D>/launch-prompt.md` | `orca_worktree.py prompt` | not for `--pipeline none`; copied to `<wt>` with the other files |
| `<D>/worktree.json` | `orca_worktree.py worktree`, then `launch` | `{path, status}` plus, after a launch, `launch: {level, submit, at}`. Never copied. To launch again, remove the `launch` entry. |
| `<wt>/.dev/issues/<N>/*` | `orca_worktree.py worktree` | copy of `<D>`; untracked, never staged by the claim (D24) |
| `$HOME/.claude/state/launch-level/pending/<nonce>` | `orca_worktree.py launch` | section 6; consumed by the hook |

Return contract, every claim (replaces the fixed list of `SKILL.md` for claim mode; create mode is unchanged and prints none of these):

```yaml
pipeline_level: worktree | full | none
submit: true | false
worktree_status: created | reused | failed
worktree_path: <absolute path or null>
worktree_branch: <branch or null>
worktree_match_key: marker | record | basename | branch | null
worktree_warning: <W- code or null>
launch_status: launched | already_launched | failed | not_requested
launch_warning: <W- code or null>
enforcement_hook: installed | missing | null    # null when no agent was requested
```

`launch_status` is `not_requested` for `none` and when Wave 7 `failed`. On a STOP the fields that do not apply are `null`.

````

### .dev/tasks/to-do/TASK-WF-scIssueClaimPipe-20261107-063237/source.md:258-284

````markdown
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
| `W-LAUNCH-FAILED` | launch | no usable record, pending record not written, or `orca agent launch` failed | re-run the claim; the hand command is printed for reference |
| `W-LAUNCH-NOT-CCSESSION` | launch (status `launched`) | the screen shows no `[ccsession]` and no session-name question, or could not be read | "this agent is NOT behind the ccsession shim; close it"; Orca's Claude command must be `/home/coder/.local/bin/ccsession-orca` (OB-5) |
| `W-ENFORCEMENT-ABSENT` | launch (status `launched`) | hook script not installed | "the level is an instruction in the prompt only until the launch-level hook (#394) ships; do not use `full` or `--submit` on a real issue yet" |

A launch is never attempted when the worktree `status` is `failed` (FR-21).

````

### .dev/tasks/to-do/TASK-WF-scIssueClaimPipe-20261107-063237/source.md:285-313

````markdown
## 12. Files to create or change

All under `src/superclaude/` unless stated. Nothing under `.claude/` is edited or staged; `make sync-dev` produces it. No `plugins/superclaude/` mirror of the issue command or skill exists (checked 2026-11-07), so none is added.

**Create**

| Path | Content |
|---|---|
| `skills/sc-issue-protocol/scripts/orca_worktree.py` | Section 8: four subcommands, stdlib only, `enforcement_status()` |
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

````

### .dev/tasks/to-do/TASK-WF-scIssueClaimPipe-20261107-063237/source.md:314-362

````markdown
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
| FO-18 | exact create argv equals section 8.3; no forbidden flag (`--issue`, `--pr`, `--reference*`, `--linear-issue`, `--gitlab-*`, `--agent`, `--prompt`, `--model`, `--effort`, `--surface`, `--setup`, `--branch`, `--activate`, `--run-hooks`) in any list or create call |
| LA-1 | exact launch argv equals section 8.4 step 5, `--prompt` starts with `[sc-launch:v1:` plus 32 hex characters and `] `, no leading `/`, no `--model`, no `--effort`, no link flag |
| LA-2 | the pending record is a regular file of mode `0600` holding exactly `worktree`, `full` or `full-submit` (matching the call), published before the launch call, in a `0700` directory; the same nonce appears in the prompt |
| LA-3 | launch failure (nonzero exit, timeout, `ok: false`) removes the pending record and gives `W-LAUNCH-FAILED` with a hand command; pending write failure (read-only store) makes no launch call |
| LA-4 | a `launch` entry in the record: `already_launched`, no `orca` call, no new pending record; a record without one launches; the entry is written after a launch even when the shim check fails |
| LA-5 | shim check: a screen with `[ccsession]` and a screen with the session-name question pass; a screen without either, an unreadable terminal and a launch JSON with no `handle` give `W-LAUNCH-NOT-CCSESSION` and status `launched` |
| LA-6 | `enforcement_hook`: `missing` and `W-ENFORCEMENT-ABSENT` without `$HOME/.claude/hooks/launch-level-guard.sh`; `installed` with an executable file; the launch happens in both cases |
| LA-7 | no launch call for a `failed` worktree record and no pending record for `none` (the skill never calls `launch` for `none`; the test pins the skill text, ST-9) |
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
| ST-9 | `refs/claim.md` skips Wave 8 for `none` and names `launch-prompt.md` as written before Wave 7 |
| ST-10 | the claim return contract in `SKILL.md` lists the ten fields of section 10 |
| ST-11 | no `src/superclaude/` path in any new or changed primitive file; `HOW-WE-WORK.md` and its plugin mirror are byte-identical (existing parity test) |

The old MR cases FO-5 and AC-5 (no `orca`) are not built; `preflight` PF-2 covers the only place a missing binary matters.

Run before commit: `uv run pytest tests/commands tests/core tests/skills tests/recommend tests/cli/test_issue_body_templates.py -q`, `make lint`, the pinned ruff format check (`uv run ruff format --check` on the changed Python files with the version the repository pins), `make sync-dev`, `make verify-sync`.

````

### .dev/tasks/to-do/TASK-WF-scIssueClaimPipe-20261107-063237/source.md:363-383

````markdown
## 14. Defaults chosen by this design

Each is a **design default**: a choice made where MR, AD and the hook design are silent or need reconciling. Change one by editing this table before `/sc:workflow` runs.

| ID | Default | Why |
|---|---|---|
| D1 | This design lives at `docs/designs/sc-issue-claim-pipeline-flag.md` | The existing design-doc folder |
| D2 | Worktree name `issue-<N>`, `--no-parent`, base `origin/<B>`, `--repo path:<main>`, `--comment "sc:issue <R>#<N>"`, no `--agent` on create | MR 2.3, AD 4.6: the create command stays as accepted; the agent is started by `agent launch` so a re-claimed worktree can be launched too |
| D3 | A missing hook script is a warning (`W-ENFORCEMENT-ABSENT`), not a refusal, for every level | The hook is #394 and does not exist; AD section 9 says phase 2 does not wait for it and OB-6 to OB-9 must run first. The warning states that `full` and `--submit` should not be used on a real issue yet. Turning it into a refusal is a one-function change in #394 |
| D4 | `version: "1.1.0"` in `commands/issue.md` only | MR 2.7 |
| D5 | Pending-record words `worktree`, `full`, `full-submit` | The hook design's `pending/<nonce>` content (section 3) |
| D6 | Shim check: 5 screen reads, 2 s apart (about 10 s). Pass on `[ccsession]` or the session-name question | The ccsession question falls back to untagged after 30 s (EVIDENCE check 11), so the window is inside it; the whole call stays inside the 120 s timeout |
| D7 | `<K>` for `Plan boundary` is the last step before the first `/sc:implement` or `/task` step | Covers all six default chains and a `/sc:recommend` route that differs from them |
| D8 | No `pipeline.json` | Section 3 |
| D9 | No automatic retry of a launch and no `--retry-launch` in version 1 | A lost reply may have started an agent; the warning says to check Orca. A duplicate agent is recoverable, a silent second launch is not predictable |
| D10 | `--surface terminal` always | The agent must be a Claude CLI session behind the shim (P5, P7) |
| D11 | The launch prompt file is assembled by script code, not by the model | The prohibition lines are the only enforcement until #394 ships |
| D12 | No `--model` or `--effort` on the launch | AD FR-22. The tier of the launched session is UNVERIFIED (section 15); the prompt asks the agent to report a mismatch with the tier named in `next-steps.md` |
| D13 | The launch happens only after both Wave 6 comments are posted and the worktree `status` is `created` or `reused` | FR-4, FR-21: nothing external happens for a claim that stopped early |
| D14 | `docs/user-guide/commands.md` and the `/sc:issue` row of `HOW-WE-WORK.md` are updated in the same change | Both say the claim "stops without running" the next steps, which becomes false |

````

### .dev/tasks/to-do/TASK-WF-scIssueClaimPipe-20261107-063237/source.md:384-400

````markdown
## 15. Orca facts: verified and UNVERIFIED

Verified on 2026-11-07 against the installed `orca` CLI and the repository:

- `orca agent launch --agent <id> --worktree <selector> --prompt <text> --surface chat|terminal --model --effort --json`; `--surface terminal` always runs the agent CLI (`orca agent launch --help`). `orca terminal read --terminal <handle> --screen --json` returns `result.terminal.{handle, status, tail, ...}` (`orca terminal read --help`). `orca status --json` returns `ok` and `result.runtime.reachable`.
- `orca worktree list --repo path:<main> --limit 500 --json` returns `result.{worktrees, truncated, totalCount, hostScope.omittedHostIds}`; each row has `id`, `path`, `branch` (a full ref such as `refs/heads/<prefix>/<name>`), `comment`, `isMainWorktree`, `isArchived`, `linkedIssue`, `linkedPR`, `projectId`.
- AD section 6 (observed 2026-11-05): a launched Claude is behind `/home/coder/.local/bin/ccsession-orca`; the prompt is the last argument, unchanged; the session runs without permission prompts; `.claude/commands/sc/` is absent in a new worktree. The ccsession question text is `Session name (Enter or Ctrl+C = untagged; untagged after 30s):`.
- #412 is merged: `agent launch --surface terminal` is the supported route for a Claude CLI session.

UNVERIFIED (each is checked in an observed run of section 17; none blocks the code):

- The JSON shape of `orca agent launch` (the terminal handle location); the script walks the result for a `handle` key.
- Whether `--comment` fills `comment` (marker key), the suffix on a taken name, and whether Orca contacts the upstream project its `projectId` names (MR R7).
- Whether the launched session carries an Orca worker preamble. If it does, the worker contract's turn-off of outward actions (WC-9) and its `/sc:pr-submit` refusal would block `--submit`.
- Which model tier the launched session runs on; whether the Orca Claude command still points at the ccsession wrapper (the shim check reports it each time).
- Whether the agent honours the plan boundary. Permission prompts are off, so the instruction alone is not enforcement; that is the hook's job (#394).

````

### .dev/tasks/to-do/TASK-WF-scIssueClaimPipe-20261107-063237/source.md:401-407

````markdown
## 16. Order of work

One `/sc:workflow` plan, two phases (AD section 9). Both phases ship in one PR; the observed runs of section 17 are owner steps after merge.

- **Phase 1, the worktree step.** Command flags and STOP rules; SKILL.md and `refs/claim.md` Wave 0 check and Wave 7; `orca_worktree.py` with `preflight` and `worktree`; the `worktree.json` record; tests PF, FO, ST-1 to ST-3 and ST-5, ST-6; design-doc B2 and B16.
- **Phase 2, the launch.** `templates/launch-prompt.md`; `prompt` and `launch` subcommands, pending record, shim check; `Plan boundary` in `next-steps.md`; Wave 5 additions and Wave 8; return contract; tests PR, LA, ST-4, ST-7 to ST-11; docs (user guide, `HOW-WE-WORK.md` and mirror, B17, B18); `make sync-dev`, `make verify-sync`.

````

### .dev/tasks/to-do/TASK-WF-scIssueClaimPipe-20261107-063237/source.md:408-421

````markdown
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

**Observed runs** (owner steps after merge, on test issues only; **not run in this change**): OB-1 default claim: one new row at Orca's default location, `git merge-base HEAD origin/<B>` equals `git rev-parse origin/<B>`, record `comment`, branch prefix, `projectId`, launch JSON shape. OB-2 repeat claim: no new row, `reused`, no second agent. OB-4 claim from a linked worktree: same `<main>`, no parent. OB-5 default claim: the agent starts behind the shim, writes a plan, waits and does not run `/sc:implement`; the process arguments show `ccsession-orca`. OB-6 `--pipeline full` on a trivial issue ends with finished implementation and no push. OB-7 `--pipeline none` launches nothing. OB-8 re-claim launches nothing. OB-9 `--pipeline full --submit` on a trivial issue pushes a branch and opens a PR on `IronbellyOrg/IronClaude` (check the URL). Until the hook of #394 exists, `full` and `--submit` are used on test issues only.
````

## Coverage slice

| Requirement | Spec line | Status | Matched task | Ratio | Quote |
|---|---|---|---|---|---|
| INF-001 | .dev/tasks/to-do/TASK-WF-scIssueClaimPipe-20261107-063237/source.md:39 | unmatched | - (best Task 6) | 0.5 | Orca is a dependency. No code, warning, option or document text exists only for a project without Orca. |
| INF-002 | .dev/tasks/to-do/TASK-WF-scIssueClaimPipe-20261107-063237/source.md:41 | covered | Task 3 (best Task 3) | 0.667 | `--submit` is a second flag, valid with `--pipeline full` only. |
| INF-003 | .dev/tasks/to-do/TASK-WF-scIssueClaimPipe-20261107-063237/source.md:45 | covered | Task 6 (best Task 6) | 0.778 | The agent is started with `orca agent launch --agent claude --surface terminal`, a Claude CLI session. |
| INF-004 | .dev/tasks/to-do/TASK-WF-scIssueClaimPipe-20261107-063237/source.md:46 | unmatched | - (best Task 7) | 0.583 | Nothing here builds the hook. The level must be readable by the hook from state the agent cannot edit (section 6). |
| INF-005 | .dev/tasks/to-do/TASK-WF-scIssueClaimPipe-20261107-063237/source.md:80 | covered | Task 3 (best Task 3) | 1.0 | `--pipeline` or `--submit` with `--create`: STOP `E-CLAIM-ONLY-FLAG` |
| INF-006 | .dev/tasks/to-do/TASK-WF-scIssueClaimPipe-20261107-063237/source.md:81 | covered | Task 3 (best Task 3) | 1.0 | A `--pipeline` value that is not one of the three: STOP, list `worktree`, `full`, `none`. |
| INF-007 | .dev/tasks/to-do/TASK-WF-scIssueClaimPipe-20261107-063237/source.md:82 | covered | Task 3 (best Task 3) | 1.0 | `--submit` with a value, or with `--pipeline worktree` or `--pipeline none` or no `--pipeline`: STOP `E-SUBMIT-NEEDS-FULL` |
| INF-008 | .dev/tasks/to-do/TASK-WF-scIssueClaimPipe-20261107-063237/source.md:86 | covered | Task 3 (best Task 3) | 0.857 | `commands/issue.md` gets `version: "1.1.0"` |
| INF-009 | .dev/tasks/to-do/TASK-WF-scIssueClaimPipe-20261107-063237/source.md:120 | covered | Task 6 (best Task 6) | 0.8 | `$HOME/.claude/state/launch-level/pending/<nonce>`. Built from path parts in the script, directories `0700`, files `0600`. |
| INF-010 | .dev/tasks/to-do/TASK-WF-scIssueClaimPipe-20261107-063237/source.md:121 | covered | Task 6 (best Task 6) | 0.778 | `secrets.token_hex(16)`: 32 lowercase hex characters, new for every launch |
| INF-011 | .dev/tasks/to-do/TASK-WF-scIssueClaimPipe-20261107-063237/source.md:122 | covered | Task 3 (best Task 3) | 0.727 | exactly one word, no spaces: `worktree`, `full` or `full-submit`. `--pipeline none` writes nothing. |
| INF-012 | .dev/tasks/to-do/TASK-WF-scIssueClaimPipe-20261107-063237/source.md:123 | covered | Task 6 (best Task 6) | 0.625 | written to a temporary name that does not match the nonce pattern, then `os.rename` to `<nonce>` |
| INF-013 | .dev/tasks/to-do/TASK-WF-scIssueClaimPipe-20261107-063237/source.md:124 | covered | Task 6 (best Task 6) | 0.857 | written before `orca agent launch`; removed if the launch fails |
| INF-014 | .dev/tasks/to-do/TASK-WF-scIssueClaimPipe-20261107-063237/source.md:125 | covered | Task 6 (best Task 6) | 1.0 | `--prompt` starts with `[sc-launch:v1:<nonce>] ` |
| INF-015 | .dev/tasks/to-do/TASK-WF-scIssueClaimPipe-20261107-063237/source.md:126 | covered | Task 6 (best Task 6) | 0.778 | no launch (`W-LAUNCH-FAILED`); the claim never starts an agent whose level it could not record |
| INF-016 | .dev/tasks/to-do/TASK-WF-scIssueClaimPipe-20261107-063237/source.md:132 | covered | Task 6 (best Task 6) | 0.875 | `enforcement_hook` (contract field) is `installed` when `$HOME/.claude/hooks/launch-level-guard.sh` exists and is executable, else `missing`. |
| INF-017 | .dev/tasks/to-do/TASK-WF-scIssueClaimPipe-20261107-063237/source.md:138 | covered | Task 4 (best Task 4) | 1.0 | `ok: false` is STOP `E-ORCA-REQUIRED` with the script's `detail`. |
| INF-018 | .dev/tasks/to-do/TASK-WF-scIssueClaimPipe-20261107-063237/source.md:144 | covered | Task 5 (best Task 5) | 0.75 | `next-steps.md` gets its `Plan boundary: after step <K>` line (FR-26). |
| INF-019 | .dev/tasks/to-do/TASK-WF-scIssueClaimPipe-20261107-063237/source.md:145 | covered | Task 7 (best Task 7) | 1.0 | It is written before Wave 7 so the copy carries it. |
| INF-020 | .dev/tasks/to-do/TASK-WF-scIssueClaimPipe-20261107-063237/source.md:147 | covered | Task 4 (best Task 4) | 0.833 | Wave 7 runs only after both comments are posted. |
| INF-021 | .dev/tasks/to-do/TASK-WF-scIssueClaimPipe-20261107-063237/source.md:153 | covered | Task 7 (best Task 7) | 0.8 | Runs when `<L>` is not `none` and Wave 7 `status` is `created` or `reused` (FR-21) |
| INF-022 | .dev/tasks/to-do/TASK-WF-scIssueClaimPipe-20261107-063237/source.md:161 | covered | Task 4 (best Task 4) | 0.889 | The claim `status` stays `success` through any Wave 7 or Wave 8 failure |
| INF-023 | .dev/tasks/to-do/TASK-WF-scIssueClaimPipe-20261107-063237/source.md:165 | covered | Task 1 (best Task 1) | 1.0 | One JSON object on stdout. Exit 0 for every runtime outcome; exit 2 only for bad arguments (argparse). |
| INF-024 | .dev/tasks/to-do/TASK-WF-scIssueClaimPipe-20261107-063237/source.md:165 | covered | Task 1 (best Task 1) | 0.857 | Every subprocess runs without a shell, with a timeout (120 s; `preflight` 30 s; each `terminal read` 15 s) and captured output. |
| INF-025 | .dev/tasks/to-do/TASK-WF-scIssueClaimPipe-20261107-063237/source.md:169 | covered | Task 1 (best Task 1) | 1.0 | `{"ok": true}` when it exits 0, prints JSON with `ok: true` and `result.runtime.reachable: true` |
| INF-026 | .dev/tasks/to-do/TASK-WF-scIssueClaimPipe-20261107-063237/source.md:173 | covered | Task 1 (best Task 1) | 0.714 | `--submit` with `--level worktree` is bad arguments (exit 2). |
| INF-027 | .dev/tasks/to-do/TASK-WF-scIssueClaimPipe-20261107-063237/source.md:192 | covered | Task 2 (best Task 2) | 1.0 | Unusable (FR-15): `ok != true`, `result.truncated == true`, `result.hostScope.omittedHostIds` non-empty, zero rows, or no row with `isMainWorktree: true` |
| INF-028 | .dev/tasks/to-do/TASK-WF-scIssueClaimPipe-20261107-063237/source.md:193 | covered | Task 2 (best Task 2) | 0.857 | Dedupe by row `id`; the first key with a hit decides. |
| INF-029 | .dev/tasks/to-do/TASK-WF-scIssueClaimPipe-20261107-063237/source.md:194 | covered | Task 2 (best Task 2) | 1.0 | a failed `git fetch origin` with the ref present continues with `W-ORIGIN-BASE-STALE` (FR-16). |
| INF-030 | .dev/tasks/to-do/TASK-WF-scIssueClaimPipe-20261107-063237/source.md:195 | covered | Task 2 (best Task 2) | 1.0 | Never one recursive directory copy. |
| INF-031 | .dev/tasks/to-do/TASK-WF-scIssueClaimPipe-20261107-063237/source.md:195 | covered | Task 2 (best Task 2) | 0.9 | a differing untracked file is renamed to `<name>.prev` (replacing an older `.prev`), then copied and named. |
| INF-032 | .dev/tasks/to-do/TASK-WF-scIssueClaimPipe-20261107-063237/source.md:197 | covered | Task 2 (best Task 2) | 0.833 | It keeps an existing `launch` entry. It is never copied. |
| INF-033 | .dev/tasks/to-do/TASK-WF-scIssueClaimPipe-20261107-063237/source.md:207 | covered | Task 6 (best Task 6) | 1.0 | Read `<D>/worktree.json` through the record guard. |
| INF-034 | .dev/tasks/to-do/TASK-WF-scIssueClaimPipe-20261107-063237/source.md:208 | covered | Task 6 (best Task 6) | 1.0 | A `launch` entry exists: `already_launched` with its `at` time; no `orca` call, no record written. |
| INF-035 | .dev/tasks/to-do/TASK-WF-scIssueClaimPipe-20261107-063237/source.md:211 | covered | Task 2 (best Task 2) | 0.6 | No `--model` or `--effort` (AD FR-22). |
| INF-036 | .dev/tasks/to-do/TASK-WF-scIssueClaimPipe-20261107-063237/source.md:212 | covered | Task 6 (best Task 6) | 1.0 | then `orca terminal read --terminal <handle> --screen --json` up to 5 times, 2 s apart. |
| INF-037 | .dev/tasks/to-do/TASK-WF-scIssueClaimPipe-20261107-063237/source.md:213 | covered | Task 6 (best Task 6) | 0.938 | Write `launch: {level, submit, at}` (UTC ISO time) into `<D>/worktree.json`, whatever the shim result, because an agent exists. |
| INF-038 | .dev/tasks/to-do/TASK-WF-scIssueClaimPipe-20261107-063237/source.md:215 | covered | Task 2 (best Task 2) | 1.0 | It never runs `git worktree add`, `orca worktree rm`, a commit, a push or a stage (FR-12). |
| INF-039 | .dev/tasks/to-do/TASK-WF-scIssueClaimPipe-20261107-063237/source.md:228 | covered | Task 5 (best Task 5) | 0.923 | The `full` and `common` blocks never contain the tokens `/sc:pr-submit`, `git push`, `git commit` or `--monitor` |
| INF-040 | .dev/tasks/to-do/TASK-WF-scIssueClaimPipe-20261107-063237/source.md:256 | covered | Task 7 (best Task 7) | 0.857 | `launch_status` is `not_requested` for `none` and when Wave 7 `failed`. |
| INF-041 | .dev/tasks/to-do/TASK-WF-scIssueClaimPipe-20261107-063237/source.md:283 | covered | Task 2 (best Task 2) | 0.75 | A launch is never attempted when the worktree `status` is `failed` (FR-21). |
| INF-042 | .dev/tasks/to-do/TASK-WF-scIssueClaimPipe-20261107-063237/source.md:287 | covered | Task 4 (best Task 4) | 0.625 | Nothing under `.claude/` is edited or staged; `make sync-dev` produces it. |
| INF-043 | .dev/tasks/to-do/TASK-WF-scIssueClaimPipe-20261107-063237/source.md:296 | covered | Task 2 (best Task 2) | 0.667 | Copied in whole from the main checkout (untracked there) so it is committed with the PR; this design cites it |
| INF-044 | .dev/tasks/to-do/TASK-WF-scIssueClaimPipe-20261107-063237/source.md:303 | covered | Task 4 (best Task 4) | 1.0 | Stays under 500 lines. |
| INF-045 | .dev/tasks/to-do/TASK-WF-scIssueClaimPipe-20261107-063237/source.md:306 | covered | Task 9 (best Task 9) | 1.0 | then byte-copy the file to `plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md` |
| INF-046 | .dev/tasks/to-do/TASK-WF-scIssueClaimPipe-20261107-063237/source.md:307 | covered | Task 8 (best Task 8) | 0.958 | B2 row rewritten (section 2), new rows B16 to B18, and short "Amended 2026-11-07" notes in sections 1, 4, 7, 14, 16, 20 pointing to this design. |
| INF-047 | .dev/tasks/to-do/TASK-WF-scIssueClaimPipe-20261107-063237/source.md:312 | covered | Task 2 (best Task 2) | 0.636 | every new reference inside the primitives to another primitive uses the installed path and the script is called as `<skill base>/scripts/orca_worktree.py`, never a `src/superclaude/` path (FR-14). |
| INF-048 | .dev/tasks/to-do/TASK-WF-scIssueClaimPipe-20261107-063237/source.md:316 | unmatched | - (best Task 2) | 0.444 | The Orca and git seams are faked; no test calls a real `orca`, `gh` or the network. |
| INF-049 | .dev/tasks/to-do/TASK-WF-scIssueClaimPipe-20261107-063237/source.md:335 | covered | Task 6 (best Task 6) | 1.0 | the pending record is a regular file of mode `0600` holding exactly `worktree`, `full` or `full-submit` |
| INF-050 | .dev/tasks/to-do/TASK-WF-scIssueClaimPipe-20261107-063237/source.md:359 | unmatched | - (best Task 2) | 0.5 | The old MR cases FO-5 and AC-5 (no `orca`) are not built |
| INF-051 | .dev/tasks/to-do/TASK-WF-scIssueClaimPipe-20261107-063237/source.md:371 | covered | Task 6 (best Task 6) | 0.889 | A missing hook script is a warning (`W-ENFORCEMENT-ABSENT`), not a refusal, for every level |
| INF-052 | .dev/tasks/to-do/TASK-WF-scIssueClaimPipe-20261107-063237/source.md:377 | covered | Task 3 (best Task 3) | 0.6 | No automatic retry of a launch and no `--retry-launch` in version 1 |
| INF-053 | .dev/tasks/to-do/TASK-WF-scIssueClaimPipe-20261107-063237/source.md:382 | covered | Task 9 (best Task 9) | 0.846 | `docs/user-guide/commands.md` and the `/sc:issue` row of `HOW-WE-WORK.md` are updated in the same change |
| INF-054 | .dev/tasks/to-do/TASK-WF-scIssueClaimPipe-20261107-063237/source.md:419 | covered | Task 9 (best Task 9) | 0.8 | `make verify-sync` passes, the tests of section 13 pass, `make lint` and the pinned ruff format check pass, the `src/superclaude` path grep shows no new hit. |
| INF-055 | .dev/tasks/to-do/TASK-WF-scIssueClaimPipe-20261107-063237/source.md:31 | covered | Task 2 (best Task 2) | 0.6 | Running any live claim, worktree create or agent launch against a real issue. |
| INF-056 | .dev/tasks/to-do/TASK-WF-scIssueClaimPipe-20261107-063237/source.md:29 | unmatched | - (best Task 6) | 0.467 | The enforcement hook (`launch-level-guard.sh`, its L2 `pre-push` layer, `jq` and registration checks): issue #394. |

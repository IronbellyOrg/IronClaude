---
domain: code
strategy: systematic
status: draft requirements, not implemented, not debated
builds_on: merged-requirements.md
amends: merged-requirements.md sections 1-9 where stated below, and design rule B2
revision: 2 (2026-11-05, after the owner's four corrections)
generated: 2026-11-05
---

# Addendum: `/sc:issue --claim --pipeline` (worktree, launch levels, submit)

Notation is the same as `merged-requirements.md`. Where this file and that one disagree, this file wins. It was written from the owner's decisions and from facts checked today; it did not go through the three-variant debate.

## 1. Owner decisions (2026-11-05)

1. B16 accepted: a worktree is created after `next-steps.md`. B2 is rewritten: any next step that is not a full implementation is allowed.
2. **Orca is a dependency.** All or nearly all projects use it. No code, warning, option or document text exists only to accommodate a project without Orca.
3. Default stop is an approved plan; `full` adds implementation; `none` launches no agent.
4. `full` has an extra flag that turns on commit, push and `/sc:pr-submit`. It never merges. Humans only review and merge.
5. The launched agent is Claude Code behind the ccsession shim, always.
6. One flag: `--pipeline worktree|full|none`, default `worktree`.

## 2. Flags

| Flag | Values | Default | Meaning |
|---|---|---|---|
| `--pipeline` | `worktree` | yes | worktree created; an agent runs `next-steps.md` up to the plan boundary and waits for a human |
| | `full` | | worktree created; the agent runs every step through implementation; no commit, no push |
| | `none` | | worktree created; no agent launched |
| `--submit` | boolean | off | with `--pipeline full` only: after implementation the agent commits, pushes the branch to `origin`, and runs `/sc:pr-submit --monitor 3`. Never merges |

- Every claim now creates a worktree, whatever the value. `none` means "no agent", not "no worktree".
- Both flags are claim only. With `--create`: STOP `E-CLAIM-ONLY-FLAG`. An unknown `--pipeline` value: STOP listing the three values. `--submit` without `--pipeline full`: STOP `E-SUBMIT-NEEDS-FULL`.
- The `--worktree` flag of the accepted spec no longer exists. Its behaviour is the always-on worktree step, and `none` is its "no launch" form.

## 3. Amended rules

- **B2 becomes:** the claim writes the summary and `next-steps.md`, creates a worktree, and launches one agent in it. Neither the `/sc:issue` skill nor the default agent runs `/sc:implement` or `/task`. `--pipeline full` lets the agent run them. `--submit` additionally lets it commit, push and run `/sc:pr-submit`.
- **B16** (worktree after `next-steps.md`), **B17** (launch levels), **B18** (`--submit`) are new design-doc decisions.
- The `/sc:issue` skill itself still runs no next-step command. The launched agent does.
- `commands/issue.md` and `SKILL.md` Will Not: replace "Run any next-step command" with "Run `/sc:implement`, `/task`, a commit, a push or `/sc:pr-submit` itself".
- Merging is never done by any level. Humans open nothing: with `--submit` the agent's `/sc:pr-submit` opens the PR on the fork.

## 4. Changes to the accepted spec caused by Orca being a dependency

1. New Wave 0 prerequisite: `orca status --json` must succeed. Otherwise STOP `E-ORCA-REQUIRED` before any GitHub or ClickUp write, the same way `gh auth status` gives `E-GH-AUTH`.
2. Remove `W-ORCA-MISSING`, the `skipped` status and every "orca not installed" edge row and test (FO-5, AC-5).
3. FR-1, FR-2, FR-3 and FR-11 are replaced: FR-1 adds the two rows of section 2; FR-2 is the STOP list of section 2; FR-3 is dropped (an unflagged claim is `--pipeline worktree`); FR-11 becomes "worktree and launch fields print on every claim".
4. Statuses are `created | reused | failed`. A missing `origin/<B>` or an unusable list is `failed` with its warning.
5. Failures after Wave 3 (create, copy, launch) stay warnings. The assignment and comments cannot be undone, so the claim stays `success`.
6. Section 2.1's "worktree only, no agent" is replaced by section 2 here. FR-6's forbidden list keeps the link flags, `--setup`, `--branch`, `--activate`, `--run-hooks`; `--agent`, `--prompt`, `--surface` are allowed only in the launch call.

## 5. Requirements

- **FR-21** Wave 8 runs after Wave 7 when its status is `created` or `reused`, `--pipeline` is not `none`, and the record has no `launch` entry (FR-27).
- **FR-22** One call from `scripts/orca_worktree.py`, 120-second timeout:

```text
orca agent launch --agent claude --worktree path:<wt> --surface terminal --prompt "Read .dev/issues/<N>/launch-prompt.md and follow it." --json
```

  `agent launch` is used, not `worktree create --agent`, so a re-claimed worktree can be launched and the create command stays as accepted. No `--model` or `--effort` in version 1.
- **FR-23** The skill writes `<D>/launch-prompt.md` from a new template `templates/launch-prompt.md`; the file is copied with the others. The `--prompt` text is one plain sentence with no leading `/`.
- **FR-24 (`worktree`)** The file tells the agent: follow `next-steps.md` step by step up to `Plan boundary`; do not run `/sc:implement`, `/task`, a commit, a push or `/sc:pr-submit`; when the plan exists, print its path and "Waiting for approval", then wait. A human approves by replying "approved" or by running the printed implement command.
- **FR-25 (`full`)** Same through the last step. No commit, no push.
- **FR-25a (`full` with `--submit`)** After implementation: commit with a conventional-commit message; stage `.dev/tasks` and the changed files; never `.claude/` and never `.dev/issues/`; push the current feature branch to `origin`; run `/sc:pr-submit --monitor 3 --head <branch> --title "..." --body "..."`. Check that no PR is already open and merged first. Never merge, never push to `master`. The prompt says the owner asked for the commit and push by passing `--submit`.
- **FR-26** `templates/next-steps.md` gains `Plan boundary: after step K`, set by the skill: features stop before `/sc:implement`; the simple bug chain after step 1; the complex bug chain before `/task`. `full` ignores it.
- **FR-27** `worktree.json` gains `launch: {level, submit, at}`, written only after a successful launch. A re-claim with that entry launches nothing and prints "agent already launched at <time>". To launch again, remove the entry.
- **FR-28** The agent is always behind the ccsession shim. After launch the script reads the new terminal once (`orca terminal read`) and requires the shim's question or `[ccsession]` text. If absent: `W-LAUNCH-NOT-CCSESSION`, printed as "this agent is NOT behind the ccsession shim; close it". Orca's Claude command setting must be `/home/coder/.local/bin/ccsession-orca`; Orca has no command to read that setting, so OB-5 verifies it from the process arguments.
- **FR-29** A launch failure is `W-LAUNCH-FAILED`; the claim stays `success` and the output prints the command to run by hand.
- **FR-30** Contract fields, every claim: `pipeline_level`, `submit`, `worktree_status`, `worktree_path`, `worktree_branch`, `worktree_match_key`, `worktree_warning`, `launch_status` (launched | failed | not_requested).
- **FR-31 (hook interface)** The stop at the plan is only an instruction in the prompt until the hook ships (follow-on issue). The skill writes `<wt>/.dev/issues/<N>/pipeline.json` (`{level, submit}`) as the hook's input. The hook design may move this file to a place the agent cannot edit.
- **FR-32 (git-level layer, owner decision O-22, 2026-11-06)** The claim also installs a `pre-push` check in the new worktree that refuses any update of `refs/heads/master` or `refs/heads/main`, at every level. Where it is installed, how it chains with the repository's existing hooks, and how it is removed are open (hook spec section 11.3, UNVERIFIED U28). The claim spec cannot be finished until they are answered.

## 6. Facts checked today, and what is UNVERIFIED

Verified: `orca agent launch` and `orca worktree create --agent` take `--prompt`, `--surface`, `--model`, `--effort`. Orca has no settings command. A launched Claude behind ccsession starts a "Session name" question that falls back to untagged after 30 seconds, and the prompt arrives as the last argument unchanged (`.dev/evals/ccsession-orca-e2e-20261026/EVIDENCE.md`, checks 5, 10, 11). Orca adds `--dangerously-skip-permissions`; ccsession adds its own, so the session runs without permission prompts. In that evidence the session ran on tier 2 by default. `/sc:issue` and `/sc:pr-submit` are on the never-as-worker list (`WORKER-CONTRACT.md`); no command has an `## Unattended mode` section today.

UNVERIFIED (check in OB-5):
- Whether Orca's Claude command is still the ccsession wrapper (evidence restored it to empty on 2026-10-26).
- Whether the launched session carries an Orca worker preamble. If it does, the worker contract's turn-off of outward actions (WC-9) and its pr-submit refusal would block `--submit`.
- Which tier the launched session runs on. Medium and complex work needs tier 1; whether `--model claude-gw-tier1a` passed to Orca overrides the wrapper's own `--model` is unknown. Until checked the prompt file names the tier in text only.
- Whether the agent honours the plan boundary. Because permission prompts are off, that is the case the hook must cover.

### Observed on 2026-11-05 (one manual run: worktree `hook-launch-level-394` for issue #394)

Command: `orca worktree create --repo path:<main> --name hook-launch-level-394 --no-parent --base-branch origin/master --agent claude --prompt "Read <file> and follow it." --json`.

- Create JSON shape: `result.worktree.{id, path, branch, displayName, comment, projectId}` and `result.launch.{outcome.handle, outcome.kind, receipt, prompt.outcome, operationId}`. Resolves R2 of the accepted spec. FR-20 (path from a row-id difference) still stands as the safe route, but `result.worktree.path` is now a known field.
- Path: `/home/coder/workspaces/worktrees/IronClaude/<name>`. Branch: `refs/heads/ironbelly/<name>`, so the configured prefix plus `--name` holds (R4 resolved for a name with no `--branch`).
- `projectId` in the create result: `github:superclaude-org/superclaude_framework`, with no link flag passed. So Orca tags this repo's worktrees with the upstream id by itself. R7 stays open: it shows the tag, not whether Orca contacts that project.
- Launch: `outcome.kind: terminal`, `prompt.outcome: handed-to-terminal`. The prompt arrived as the last argument of `/home/coder/.local/bin/ccsession-orca '--dangerously-skip-permissions' '<prompt>'`.
- ccsession shim: **verified.** The running `claude` process has `--dangerously-skip-permissions --allowedTools=Grep --settings {"modelSettings":{"claude-gw-tier1b":...` (ccsession's arguments), so Orca's Claude command is currently the wrapper. FR-28 can check this from the typed command line or the process arguments. The session ran on tier 1b, which is the tier of the session that launched it, not a value this spec set.
- `.claude/commands/sc/` does **not** exist in the new worktree. `/sc:` commands come from the installed `~/.claude/` copy. R6 resolved: setup does not fill the project `.claude/`, and the `make sync-dev` hint is needed only for a session that must run a changed, unsynced primitive.
- Still UNVERIFIED: whether `--comment` fills `comment` (not passed this time); whether the session carries an Orca worker preamble (see the hook session result); taken-name suffix.

## 7. Tests

Fake-`orca`: exact launch argv; no link flag; no launch for `none`, for a `failed` worktree, or when the record has `launch`; `E-SUBMIT-NEEDS-FULL`; bad `--pipeline` value; `E-ORCA-REQUIRED` makes no GitHub call; the shim check passes on a screen with `[ccsession]` and warns without it; launch failure leaves `status: success`.
Static: the `worktree` template contains the "do not run" lines and the `full` template does not; only the submit block mentions `/sc:pr-submit`, push and commit; `templates/launch-prompt.md` is named in `SKILL.md`; `Plan boundary` is in `templates/next-steps.md`.
Observed: **OB-5** default claim on a test issue: the agent starts behind the shim, writes a plan, waits, and does not run `/sc:implement`; the process arguments show `ccsession-orca`. **OB-6** `--pipeline full` on a trivial test issue ends with finished implementation and no push. **OB-7** `--pipeline none` launches nothing. **OB-8** re-claim launches nothing. **OB-9** `--pipeline full --submit` on a trivial test issue pushes a branch and opens a PR on `IronbellyOrg/IronClaude` (check the URL).

## 8. Files to change beyond the accepted spec

`templates/launch-prompt.md` (new); `templates/next-steps.md`; `refs/claim.md` (Wave 0 check, Wave 8); `scripts/orca_worktree.py`; `SKILL.md`; `commands/issue.md` (two options, STOP rules, Will Not); `docs/designs/sc-issue-command.md` (B2 rewrite, B16 to B18); tests as in section 7; remove the skipped-status and not-installed cases from the accepted spec's tests.

## 9. Rollout

One `/sc:workflow` plan, two phases. Phase 1: the accepted worktree step with sections 4 and 2 applied, then the AC-1 run. Phase 2: Wave 8 and `--submit`, then OB-5 to OB-9. The hook is a separate issue and sprint, designed in parallel; phase 2 does not wait for it, but `--submit` and `full` should not be used on real issues until it exists.

---
name: pr-submit
description: "Open a PR on the fork and arm an in-session PR-review auto-remediation monitor — poll for the Augment and Codex reviews, re-grade + verify findings, dispatch verified ones to /sc:troubleshoot, then (at higher --monitor ordinals) fix, validate, push, reply, and resolve under a capped monotonic round counter."
category: quality
complexity: advanced
mcp-servers: [litellm, auggie]
personas: [analyzer, architect, security, qa, devops]
argument-hint: "[--monitor {0,1,2,3}] [--max-rounds N≤5] [--poll-interval ≥30] [--timeout 600] [--silence-timeout 300] [--base <branch>] [--head <branch>] [--title ...] [--body ...] [--pr <N>] [--conflict-max-tier {0,1,2}] [--merge-guard {draft,off}] [--output-dir <dir>] [--resume <run-log.jsonl>]"
version: "1.0"
---

# /sc:pr-submit - PR Review Auto-Remediation Monitor

## Triggers

Explicit only — two activation paths:

1. **Direct:** the user runs `/sc:pr-submit --monitor {0,1,2,3}` to open a PR (and optionally arm the monitor).
2. **Programmatic:** another skill invokes the protocol via the Skill tool.

## Required Input

| Input | Required | Notes |
|-------|----------|-------|
| `--monitor {0,1,2,3}` | No (default 3) | The autonomy ceiling on a single FSM. Explicit 0 = open PR only (byte-identical to today). |
| PR context (`--head`/`--base`/`--title`/`--body`) OR an existing PR number (`--pr <N>`) | Yes | To open or attach to the PR. |

**STOP** if `--monitor >= 1` and the PR cannot be confirmed on the resolved target repo (origin's `owner/repo`, parsed from `git remote get-url origin`), or if your checkout is not the PR's head branch and commit (`pr_head_mismatch`; do not close the PR, follow the recovery steps in the HALT message).

**STOP** if `--monitor >= 1` and the CI-wait preflight fails: `gh pr checks --repo <owner/repo> --help` must list `--json`, and the runtime must import `superclaude.pr_submit.ci`. The skill's CI-wait preflight is authoritative.

## Usage

```text
/sc:pr-submit --monitor 0 --head feature/x --title "..." --body "..."     # open PR only (zero regression)
/sc:pr-submit --monitor 1 --head feature/x                                 # arm + poll + propose (no edits)
/sc:pr-submit --monitor 2 --head feature/x                                 # + fix locally, HALT before push
/sc:pr-submit --monitor 3 --max-rounds 3 --head feature/x                  # full loop: fix→push→reply→resolve
/sc:pr-submit --resume <repo-root>/.dev/pr-monitor/pr-42-.../monitor-run-42.jsonl
```

## Options

| Flag | Default | Description |
|------|---------|-------------|
| `--monitor {0,1,2,3}` | 3 | Capability ceiling (G-arm/G-edit/G-push gates). |
| `--max-rounds N` | 2 | Remediation cycles; hard cap 5 (reject >5). |
| `--poll-interval S` | 30 | Poll interval; minimum 30 seconds (reject <30). |
| `--timeout S` | 600 | Per-wait wall-clock timeout (~10 min). CI runs can exceed this; size it to the full check run. |
| `--silence-timeout S` | 300 | No-activity window per reviewer; min 30s; clamped to `--timeout`. Augment silence: L3 at most one poke via INV-S1 write-ahead. Codex with no activity by then (or once Augment has settled) is recorded absent and ignored; Codex is never poked. |
| `--base <branch>` | repo default branch | PR base branch; defaults to the repo's actual default (`gh repo view "$REPO" --json defaultBranchRef`), overridable here. |
| `--head <branch>` | — | PR head branch. |
| `--pr <N>` | — | Attach to an existing PR instead of opening one. |
| `--conflict-max-tier {0,1,2}` | 0 | Highest merge-conflict tier to act on: 0 (default) detect and report only; 1 also regenerate a conflicted root `uv.lock` (Tier 1, opt-in because `uv lock` can run the PR's build code); 2 also resolve text conflicts by stated intent (Tier 2, off by default). Tier 3 always halts at L3. Tier 1 halts before `uv lock` when the merged `pyproject.toml` declares `build-system.backend-path`, a non-empty `project.dynamic`, or a path or editable `[tool.uv.sources]` entry. Conflict resolution and validation run the project's build and test code, so run pr-submit only on PRs from collaborators you trust with your credentials. |
| `--merge-guard {draft,off}` | draft | Effective only at `--monitor 3`. `draft` holds the PR as a draft while a fix cycle runs and marks it ready again once the fix push is confirmed (see "Merge guard"); `off` leaves the PR untouched and prints "Remediation is unprotected: --merge-guard off." once. |
| `--title` / `--body` | — | PR title / body. |
| `--output-dir <dir>` | `.dev/pr-monitor/pr-<N>-<ts>/` | Run-log + artifacts dir. |
| `--resume <jsonl>` | — | Reconstruct state from a write-ahead run-log. |

`status` enum: `terminal_clean` / `terminal_max_rounds` / `terminal_halted` / `terminal_timeout` / `terminal_augment_no_response` / `terminal_failed` / `proposed` / `halt_before_push`. Silence of every configured reviewer (Augment and Codex) is `terminal_augment_no_response`, not `terminal_clean`; the output also reports each reviewer as `present` / `absent` / `incomplete` (`reviewers`).

## Merge-conflict handling

`--monitor` (default 3) and `--conflict-max-tier` (default 0) are independent ceilings. Monitor 0 skips conflict handling. At monitor 1 and above, the skill checks for an operation already in progress, detects conflicts before the first review, and reports a per-path plan before editing. Being behind the base without conflicts is reported, not automatically rebased. Cap 0 detects and reports only: it does not guarantee a clean outcome or allow Tier 3 resolution.

| Conflict tier | Permission and timing |
|---|---|
| 0: no local conflicts | Report the result; no conflict merge is needed. A contradictory GitHub result still needs investigation. |
| 1: conflicted root `uv.lock` | Opt in with cap 1 or 2. Before the CI wait, an eligible cycle at monitor 1 proposes; at monitor 2 it resolves and validates but leaves an uncommitted merge in progress; at monitor 3 it may publish one validated merge of the recorded base tip. Proposing or resolving locally happens only after a clean or report-only review outcome. |
| 2: text/tree conflicts with statable intent | Cap 2 and monitor 3 only, before the first review, with at least two remaining review rounds and at most eight text-conflict files. The skill records both sides' intent and any dropped behavior, requires a read-only grounding check and full tests, then may publish the merge and re-trigger configured reviewers. An attributed re-review spends a round. |
| 3: unsafe or unclassifiable | Report at monitor 1 or 2; halt for human resolution at monitor 3. Examples include protected or migration paths, binaries, symlinks, submodules, mode changes and unsupported lock/generated files. Unclear or semantic intent escalates here rather than being invented. |

There is at most one conflict cycle per run across both resolving tiers. Late text conflicts halt; this is not continuous automatic conflict repair. A conflict that first appears while the CI wait is running gets one more Tier 1 sync only when no conflict cycle started earlier in the run; it needs `--conflict-max-tier` of at least 1 at every monitor level (with the default cap of 0 it ends with `tier_above_cap`), and with a cap of at least 1 monitor 1 only proposes and monitor 2 only leaves a validated uncommitted merge, both only after a `clean` or `report_only` review, and only monitor 3 pushes; a late text (Tier 2) conflict halts. A Tier 1 sync push spends no review round and sends no reviewer re-trigger, reply or thread resolution. It is the single sync exception on otherwise wait-only paths; it does not turn reviewer silence or round exhaustion into a clean review. Normal fix-cycle re-trigger behavior described below is unchanged.

After a merge push, CI is checked against the new head. Expected checks that have not appeared keep the wait open and can time out as `ci_not_started`; they are not read as success. Unresolved conflicts skip the CI wait with reason `pr_conflicting`. The run output includes `sync_tier`, `sync_outcome` and `sync_push_count` alongside the review result.

**Trust and recovery:** conflict resolution requires a clean tracked tree and no foreign operation; it never stashes changes or rewrites a published head. The lock trust gate is not a sandbox: it does not cover Git/URL dependency sources, and it fails closed without a TOML parser (including Python 3.10). Regeneration, tests and commit hooks can execute project code. Opt in only for collaborators trusted with your credentials. A monitor-2 result leaves the merge resolved and validated but uncommitted: review and finish it yourself, or abort it. Incomplete owned resolutions are aborted; some finish failures deliberately leave the merge for inspection. Resume uses the recorded ownership and push state, never aborts a foreign merge, and never blindly publishes an uncovered local commit. A published merge is undone with a new revert commit, not history rewriting.

The protocol's `refs/conflict-mechanical.md` owns detection, validation and recovery; `refs/conflict-intent.md` adds Tier 2 judgment and evidence requirements. Load them through the protocol, not as a replacement for its mandatory activation.

## Merge guard (`--merge-guard`)

`--merge-guard {draft,off}` is on by default (`draft`) and acts only at `--monitor 3`. Below that, and with `off`, the skill makes no draft or ready change. A run at `--monitor 2` that applies fixes and halts before the push reports that the PR is still mergeable and the fixes are local only.

- **When the PR becomes a draft:** at the end of Wave 3, when at least one verified finding of Medium severity or higher is routed to a fix, once per fix cycle (a CI-fix cycle counts as its own cycle). The PR becomes a draft before any edit, so nobody merges it while the fix exists only locally. A PR that was already a draft is left alone and this run never makes it ready.
- **When it becomes ready:** only after the cycle's fix push is confirmed on the PR head (or a cycle that applied no edit is proven), and before any reply, resolve or re-trigger comment, so the reviewers see a ready PR.
- **Held outcome:** an exit with unpublished or uncertain work (a validation failure, a halt before the push, a rejected or failed push, a push whose landing is unknown, a release that could not be confirmed, a PR that was merged or closed) leaves the PR a draft. The output then reports `merge_guard: held` with the reason and the clear command, which marks the PR ready by hand once you have checked it:

```text
gh pr ready <N> --repo "$REPO"
```

- **Unreadable timeline:** the guard decides from the PR's draft and ready history. If that history cannot be read, the guard never marks the PR ready: at the start of a cycle the run halts with reason `draft_guard_unavailable` before any edit, and at a later checkpoint it keeps the PR a draft and reports `held`. If someone else changes the draft state, the guard stands down and reports `user_override`.
- **Effects on reviewers and workflows:** drafts and ready transitions may change which reviews and workflows run. Whether the Augment and Codex reviews and the CI workflows behave as expected on a draft or on a ready transition (release gates G4 and G5 of the design) is unverified until the owner's run on a disposable PR; do not rely on it, and the PR body states this release gate. Pass `--merge-guard off` to run without the guard.

## Behavioral Flow

This command does ONLY parse + environment-validate + handoff. It parses the flags, verifies the PR target is the resolved origin repo (origin's `owner/repo`, never an upstream parent the host's CLI might default to), and hands off to the protocol skill via the Activation section below. The full behavioral specification — the FSM, the detection contract, severity routing, verify-before-remediate, troubleshoot dispatch, validation gates, the push triad, reply/resolve, and the loop guard — lives in the skill.

## Arming

`--monitor 0` always works (it just opens the PR). At `--monitor >= 1`, `DetectionContract.for_arming()` loads the shipped baked-identity contract: Augment (`augmentcode[bot]` / `augmentcode`) and Codex (`codex_bot_login` `chatgpt-codex-connector[bot]`, `codex_app_slug` `chatgpt-codex-connector`, `codex_retrigger_phrase` `@codex review`). An override that omits the Codex keys keeps the shipped Codex values; blanking both Codex identities disables Codex. A gitignored local override at `<repo-root>/.dev/pr-monitor/detection-contract.locked.md` is preferred when present; a missing or unlocked override is not a halt. No R1 probe is required.

## Activation

**MANDATORY**: Before executing any protocol steps, invoke:
> Skill sc:pr-submit-protocol

Pass the following context:

- `--monitor` ordinal (0/1/2/3) and `--max-rounds` / `--poll-interval` / `--timeout` / `--silence-timeout` / `--conflict-max-tier` / `--merge-guard`.
- PR context: `--base` / `--head` / `--title` / `--body`, or the existing PR number (`--pr <N>`).
- `--output-dir` and `--resume` if supplied.

Do NOT attempt to execute the monitor using only this command file. The deterministic decisions defer to the importable `superclaude.pr_submit` core; the orchestration, the attended poll loop, and `gh`/`git` I/O live in the protocol skill.

## Boundaries

**Will:** open the PR on the resolved origin repo with `--repo <owner/repo>` pinned on every `gh` call (the pin is computed from origin, never bare); arm an in-session monitor at L1+ that handles the Augment and Codex reviews the same way (one poll snapshot, merged results, one fix commit per cycle, reply to and resolve every remediated, verified thread of either reviewer, one re-trigger comment per present reviewer); verify before remediating; respect the ordinal ceiling; after a clean review or `terminal_augment_no_response`, wait on PR checks (silence is wait-only, never claimed as `terminal_clean` for the review).

**Will Not:** run headless / imply a daemon; push to an upstream parent remote or to the repo's default/protected branch; force-push; push any commit besides the cycle's one fix commit (it halts with `push_range_mismatch` instead, so unreviewed local commits are never published), except a conflict cycle's one merge commit, whose parents must be exactly the PR head and the recorded base tip (`merge_parent_ok`); rebase a published PR head (at L1+ the create path no longer rebases); emit `--depth quick --fix`; apply edits at L1 or push/reply at L2.

## Related Commands

- `/sc:auggie-review` — the sibling PR-review command.
- `/sc:troubleshoot` — invoked per verified finding for diagnosis.

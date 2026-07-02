---
name: pr-submit
description: "Open a PR on the fork and arm an in-session PR-review auto-remediation monitor — poll for the Augment review, re-grade + verify findings, dispatch verified ones to /sc:troubleshoot, then (at higher --monitor ordinals) fix, validate, push, reply, and resolve under a capped monotonic round counter."
category: quality
complexity: advanced
mcp-servers: [sequential, serena, auggie]
personas: [analyzer, architect, security, qa, devops]
argument-hint: "[--monitor {0,1,2,3}] [--max-rounds N≤5] [--poll-interval ≥30] [--timeout 600] [--base <branch>] [--head <branch>] [--title ...] [--body ...] [--output-dir <dir>] [--resume <run-log.jsonl>]"
version: "1.0"
---

# /sc:pr-submit - PR Review Auto-Remediation Monitor

## Triggers

Explicit only — three activation paths:

1. **Direct:** the user runs `/sc:pr-submit --monitor {0,1,2,3}` to open a PR (and optionally arm the monitor).
2. **PR-creation hook:** after a successful `gh pr create`, the `offer-pr-review.sh` hook mentions `sc:pr-submit --monitor` alongside `/sc:auggie-review` (the hook NEVER arms a monitor itself, NEVER implies level-3 without explicit invocation).
3. **Programmatic:** another skill invokes the protocol via the Skill tool.

## Required Input

| Input | Required | Notes |
|-------|----------|-------|
| `--monitor {0,1,2,3}` | No (default 2) | The autonomy ceiling on a single FSM. Explicit 0 = open PR only (byte-identical to today). |
| PR context (`--head`/`--base`/`--title`/`--body`) OR an existing PR number | Yes | To open or attach to the PR. |

**STOP** if `--monitor >= 1` and the PR cannot be confirmed on the resolved target repo (origin's `owner/repo`, via `gh repo view --json nameWithOwner`), or if `detection-contract.md` is `locked: false` (run the R1 probe first — T-210).

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
| `--monitor {0,1,2,3}` | 2 | Capability ceiling (G-arm/G-edit/G-push gates). |
| `--max-rounds N` | 2 | Remediation cycles; hard cap 5 (reject >5). |
| `--poll-interval S` | 30 | Poll interval; minimum 30 seconds (reject <30). |
| `--timeout S` | 600 | Review-wait wall-clock timeout (~10 min). |
| `--base <branch>` | repo default branch | PR base branch; defaults to the repo's actual default (`gh repo view --json defaultBranchRef`), overridable here. |
| `--head <branch>` | — | PR head branch. |
| `--title` / `--body` | — | PR title / body. |
| `--output-dir <dir>` | `.dev/pr-monitor/pr-<N>-<ts>/` | Run-log + artifacts dir. |
| `--resume <jsonl>` | — | Reconstruct state from a write-ahead run-log. |

## Behavioral Flow

This command does ONLY parse + environment-validate + handoff. It parses the flags, verifies the PR target is the resolved origin repo (origin's `owner/repo`, never an upstream parent the host's CLI might default to), and hands off to the protocol skill via the Activation section below. The full behavioral specification — the FSM, the detection contract, severity routing, verify-before-remediate, troubleshoot dispatch, validation gates, the push triad, reply/resolve, and the loop guard — lives in the skill.

## Arming (R1 detection probe, T-210)

`--monitor 0` always works (it just opens the PR). To arm at `--monitor >= 1`, the detection contract must be locked. The shipped `refs/detection-contract.md` ships `locked: false`, so a fresh clone safely HALTs ("probe first"). On that missing/unusable locked-contract halt, the protocol must keep the existing fail-closed arm path (`DetectionContract.for_arming()` raises before Monitor arming), call the read-only `superclaude.pr_submit.contract_setup.diagnose()`/`render_pr_submit_missing_contract_halt()` surface to print the readiness state, checked paths, blockers, and the approved next safe readiness command: `superclaude reflect contract-status [--validate] --repo <owner/repo> --pr <number>`. The halt then stops with the literal side-effect guarantee: `No monitor was armed. No comments, pushes, retries, resolves, or retriggers were performed.` `--monitor 0` remains unaffected and no setup/readiness path writes a lock, arms a monitor, or mutates the PR by default. To arm on a given repo after a validated local lock exists, rerun `/sc:pr-submit --monitor 1 --pr <number>` or a higher monitor ordinal with the existing PR number. The gitignored operator-local override remains `<repo-root>/.dev/pr-monitor/detection-contract.locked.md` with `locked: true`, and the arm path (`DetectionContract.for_arming()`) prefers it (resolved relative to the cwd). The repo-specific bot identity therefore never ships in the distributable skill.

## Activation

**MANDATORY**: Before executing any protocol steps, invoke:
> Skill sc:pr-submit-protocol

Pass the following context:

- `--monitor` ordinal (0/1/2/3) and `--max-rounds` / `--poll-interval` / `--timeout`.
- PR context: `--base` / `--head` / `--title` / `--body`, or the existing PR number.
- `--output-dir` and `--resume` if supplied.

Do NOT attempt to execute the monitor using only this command file. The deterministic decisions defer to the importable `superclaude.pr_submit` core; the orchestration, Monitor arming, and `gh`/`git` I/O live in the protocol skill.

## Boundaries

**Will:** open the PR on the resolved origin repo with `--repo <owner/repo>` pinned on every `gh` call (the pin is computed from origin, never bare); arm an in-session monitor at L1+; verify before remediating; respect the ordinal ceiling.

**Will Not:** run headless / imply a daemon; push to an upstream parent remote or to the repo's default/protected branch; auto-lock the detection contract; emit `--depth quick --fix`; apply edits at L1 or push/reply at L2.

## Related Commands

- `/sc:auggie-review` — the sibling PR-review command (offered together by the post-PR-create hook).
- `/sc:troubleshoot` — invoked per verified finding for diagnosis.

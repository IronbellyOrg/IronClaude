---
topic: "A PR-review auto-remediation monitor: on PR open, watch for Augment Code's GitHub-App review, then route findings by severity into sc:troubleshoot fix sessions and reply to the review threads."
domain: architecture
strategy: systematic
depth: standard
proposals_target: 3
handoff_target: none
created: 2026-06-10T23:47:50Z
scope_version: "1.0"
---

# Seed Brief: PR Review Auto-Remediation Monitor (V1.0)

## Problem Statement

When a PR is opened on the fork (`IronbellyOrg/IronClaude`), the external **Augment Code
GitHub App** posts an asynchronous code review on the PR (review summary + inline comments,
each with a severity). Today there is no automated bridge between that review and the repo's
own remediation tooling (`/sc:troubleshoot --fix`). A human must read the review, decide what
to fix, run troubleshoot manually, implement, push, and reply to each thread.

V1.0 closes that loop **in-session**: a PR-submission skill opens the PR and arms an
**in-session Monitor** that polls the PR until Augment's review lands, parses each finding's
severity, routes it into the correct troubleshoot tier, and (subject to an autonomy gate)
proposes / validates / implements / pushes fixes and replies to each review thread, resolving
it. The loop stops when a re-review returns zero Medium-or-above findings, or a max-rounds cap
is hit.

## Critical Reframing (established during dialogue)

- **Hooks cannot host the monitor.** Claude Code hooks are short-lived shell scripts
  (1–10s timeouts) that can only emit context text — they cannot run a Monitor tool or a
  Claude agent loop. Therefore V1.0's entry point is a **skill**, not the existing
  `offer-pr-review.sh` hook. The hook's role is unchanged: a lightweight *suggester*.
- **The reviewer is the external Augment Code GitHub App** (cloud, asynchronous), NOT the
  local `/sc:auggie-review` skill. The monitor must *poll the GitHub PR* for the App's review,
  parse its comments, and reply onto its threads.
- **In-session only for V1.0.** The execution host is the **Monitor tool** in the live Claude
  Code session. The session must stay open until the review lands and remediation completes.
  Detached / headless `claude -p` and CI hosting are explicitly **out of scope for V1.0**
  (V2.0 territory — see below).

## Known Context (repo facts, grounded)

- `PostToolUse(Bash)` hook `offer-pr-review.sh` already fires after a successful `gh pr create`
  and *offers* `/sc:auggie-review`. (`/config/workspace/IronClaude/.claude/settings.json`,
  `src/superclaude/hooks/scripts/offer-pr-review.sh`)
- `/sc:auggie-review` already assigns **Critical / High / Medium / Low / Nit** severities, has a
  reusable **severity rubric** (`src/superclaude/skills/sc-auggie-review-protocol/refs/severity-rubric.md`),
  and posts to PRs via `gh pr review --comment` + inline `gh api .../pulls/N/comments`.
- `/sc:troubleshoot` already exposes `--fix`, `--depth deep`, and a tiered protocol
  (`src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md`).
- This is a **fork**: PRs target `IronbellyOrg/IronClaude` (NEVER upstream). All `gh` calls
  must pin `--repo IronbellyOrg/IronClaude`.
- The Monitor tool streams stdout lines as events back into the live session; the agent then
  acts on each event (this is the substrate that lets a poll-loop trigger `/sc:troubleshoot`).

## The Unified Autonomy Model (reconciling the two answer enumerations)

The user described two overlapping scales (`--monitor 0/1/2` and autonomy `0/1/2/3`). They
reconcile into **one ordinal `--monitor` level** that sets how far the loop runs before
halting for a human:

| Level | Name | Behavior |
|-------|------|----------|
| `0` | off (default) | Open PR, do nothing else. No monitor armed. |
| `1` | review + report | Poll → Augment review lands → run troubleshoot (diagnose only) → **report all comments + proposed remediation path to the user; ask before fixing.** |
| `2` | fix-local + ask-push | Level 1 + **implement & validate fixes locally** (tests green) → **HALT and ask the user before committing/pushing** + before posting replies. |
| `3` | autonomous | Level 2 + **commit, push to PR branch, post reply-to-thread + resolve**, fully unattended, governed by the loop-guard. |

This single ordinal subsumes both the user's `--monitor` triad and the 0/1/2/3 autonomy
gradient. Level `1` == "in-session monitor that reports + offers remediation"; level `3` ==
"full automated pipeline".

## Constraints

- **Fork-only PR targeting**: every `gh` PR/review/reply call pins `--repo IronbellyOrg/IronClaude`.
- **In-session host**: monitor runs via the Monitor tool; no detached daemon in V1.0.
- **Severity → tier mapping is fixed**:
  - Medium → `/sc:troubleshoot --fix`
  - High or Critical → `/sc:troubleshoot --depth deep --fix`
  - Low / Nit → no auto-remediation (report only).
- **Reply mechanism**: reply onto the *specific* Augment review-comment thread (`gh api`
  reply-to-review-comment), then resolve the thread. Not a single summary blob.
- **Loop-stop**: stop when a fresh Augment re-review surfaces zero Medium+ findings, OR a
  `--max-rounds` cap (default 2–3) is reached — whichever first.
- **No commit/push below level 3** without explicit human approval.
- **Source-of-truth discipline**: skill + hook source live in `src/superclaude/`, synced via
  `make sync-dev`; never edit `.claude/` directly; never stage `.claude/` except `settings.json`.
- **Reuse, don't reinvent**: the severity rubric and the `gh` posting patterns already exist in
  `sc-auggie-review-protocol` — V1.0 imports/mirrors them rather than redefining.

## Success Criteria

1. A user can open a PR via the new skill with `--monitor {0,1,2,3}` and the chosen autonomy
   level is honored end-to-end.
2. The monitor reliably detects when the Augment Code App has posted its review (and
   distinguishes "review not yet posted" from "review posted, zero findings").
3. Each Augment finding's severity is parsed and correctly routed (Medium→fix,
   High/Critical→deep fix; Low/Nit→report).
4. Fixes are validated locally (tests) before any push; pushes happen only at level 3 or after
   explicit approval at level 2.
5. Replies land on the correct individual review threads and the threads are resolved.
6. The loop terminates deterministically (clean re-review OR max-rounds) with no infinite
   fix→review→fix cycle.
7. A re-review triggered *by the monitor's own push* does not spuriously re-arm remediation
   beyond the round cap (loop-guard correctness).

## Open Questions (carried into requirements red-team)

- **OQ1 — Augment review-detection signal.** What exact GitHub artifact does the Augment App
  emit (a formal `PULL_REQUEST_REVIEW` by a known bot login? plain issue comments? check-run?),
  and how do we poll for "review complete" vs "still reviewing"? Needs an empirical probe on a
  real Augment-reviewed PR before locking the parser.
- **OQ2 — Severity extraction from Augment comments.** Does the App emit a structured severity
  label we can parse, or do we re-grade its prose through the local severity rubric?
- **OQ3 — Round-cap vs convergence.** Default `--max-rounds`? How to detect "the push I just
  made is what triggered this new review" to avoid double-counting a round.
- **OQ4 — Validation definition.** What counts as "validated locally" — `make test` full suite,
  or targeted tests touching changed files? Affects level-2/3 gating latency.
- **OQ5 — Auth/session longevity.** In-session monitor requires the session to stay alive
  through Augment's review latency (minutes). Acceptable for V1.0? Timeout behavior?

## Explicitly Deferred to V2.0 (separate brainstorm — see generated prompt)

- **@bot-mention → headless `claude -p` trigger.** A user (or anyone) replies to a PR comment,
  @-mentions the bot with free-form instructions; a server-side/headless `claude -p` session
  runs e.g. `/sc:troubleshoot "${opComment}" --depth deep --fix` with the mentioned comment's
  body substituted for `${opComment}`. Not automatic — human-initiated via mention. This needs
  its own brainstorm (execution host = GitHub Actions / detached headless; auth; comment-parsing
  command-injection safety; who is authorized to invoke).

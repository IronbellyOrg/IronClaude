# D3 option (b): `/sc:pr-submit` runs as an Orca worker with pre-authorization

Position: apply the section 3.2 pr-submit row: `--monitor 1` refused under `--unattended`, operator HALTs reported as blocked, a markdown summary in `--output-dir`, waits split so the session can heartbeat; outward actions as D4 decides (`SPEC:137`, `SPEC:342`).

Citation key: `SPEC:N` = spec line; `PRS:N` = `src/superclaude/skills/sc-pr-submit-protocol/SKILL.md:N`; `PRC:N` = `src/superclaude/commands/pr-submit.md:N`; `CAPS:N` = `.dev/orca-command-refactor/inventory/orca-capabilities.md:N`.

## Strongest case for it
- **Parallel PR monitoring.** A coordinator that lands several independent changes can monitor several PRs at once, each worker in its own worktree, instead of serially holding its own session in poll waits (`PRC:47-49`).
- **It already fits a worker technically.** It must run top-level, not in a subagent (`PRS:47-49`), and an Orca worker is a top-level Claude session in its own terminal (`CAPS:161`). The 600 s default is a cumulative budget over repeated poll-then-sleep iterations (`PRS:56-80`), so the session can heartbeat between iterations (`SPEC:137`). It is durable: a write-ahead run-log plus `--resume` (`PRS:43-45`; `PRC:56`), which matches WC-6's resume cell.
- **The coordinator stays free** to answer other workers' questions while PRs are reviewed.

## Safety
- The command's own boundary says "**Will Not:** run headless / imply a daemon" (`PRC:85`) and the skill calls itself "an **attended, in-session** loop" (`PRS:43`). Making it a worker either rewrites that boundary or treats the worker's session as "attended" when no person watches it.
- At `--monitor 3` the worker pushes fix commits and replies to and resolves review threads with no person watching (`PRC:83`); safety then rests entirely on D4's authorization and on pr-submit's own guards (no force-push, only the cycle's one fix commit, `PRC:85`).

## Reliability
- One poll iteration's runtime is UNVERIFIED (`SPEC:394`); AC-4.3 must show no single Bash call exceeds 240 s (`SPEC:276`).
- HALTs such as `pr_head_mismatch` (`PRC:28`) become blocked contracts and new Tasks (WC-6), which is slower than a person reading the HALT in place.

## How a person works day to day
- The person sees PR results as worker reports; to act on a HALT they read a contract and the coordinator re-dispatches.

## Implementation cost
- The full pr-submit row in P4 (`SPEC:137`, `SPEC:185`), AC-4.3 on a scratch fork PR (`SPEC:276`), and a reconciled "Will Not: run headless" line. Depends on D4 (a) or (c) for any push.

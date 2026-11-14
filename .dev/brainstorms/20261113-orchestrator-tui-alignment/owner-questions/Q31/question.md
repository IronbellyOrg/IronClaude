# Q31: Does the owner's 10-minute recurring check apply to this program's coordinator?

## The question (verbatim from the spec row)

Source: `merged-requirements.md` section 3, row Q31 (line 558).

> Does your 2026-11-05 recurring-check order (about every 10 minutes: Orca Run, ListAgents, open PRs on IronClaude and Coder, idle subscriptions) apply to this program's coordinator? (new, R25-INV-010)

## The spec's recommended answer

> Yes, read-only

## Default if unanswered

> WC-16 only, and Q31 is shown open at the top of the ledger (the spec does not pick an answer from memory either way)

In plain words: the coordinator keeps only the worker-contract loop (rule WC-16, below), adds no 10-minute timer, and the decision ledger (the program's on-disk record of owner answers, work item XC-01) lists Q31 as still open.

## What it gates

> none scheduled; sets the status of the last row of the 6.6 cadence record

No work item waits on Q31. The answer only fills in the status of the last row of the coordinator's "cadence record" (section 6.6, line 1026), the table that lists every clock the coordinator respects. Dependency graph edge 101 (line 748): "Q11, Q31, Q32 -> XC-01 ... Recorded only; they gate no item." Wave: W0 (the intake wave before any program work starts; asked in the W0 order after Q1, Q33, Q26, Q2, Q3, Q4, Q25, line 523).

Limit written into the spec (line 579): "Q31 does not authorize `/sc:sweep` above WC-16's cap or any write."

## Facts the question depends on

1. **The owner's order (memory, the lowest source tier).** `~/.claude/projects/-home-coder-workspaces-IronClaude/memory/coordinator-never-stop-polling.md`, modified 2026-11-05: "the coordinator is forbidden from stopping polling of all sessions; everything must flow through the coordinator." How to apply: re-arm the Orca wait after every wake "even when no Orca worker is active", and "Keep a recurring CronCreate sweep (every ~10 minutes, off-minute) that re-checks the Orca run, ListAgents, open PRs on IronClaude and Coder, and re-subscribes `notify_when_idle` on busy peers." Why it was given: a lapsed wait left sessions unwatched, and "Peer sessions (interactive, not Orca workers) do not appear in the Orca message queue at all."
2. **WC-16, the worker contract's coordinator loop.** `src/superclaude/core/WORKER-CONTRACT.md:288`: the coordinator "never stops watching on its own. When a wait on Orca expires, the coordinator re-arms it. On every coordinator wake or wait timeout, at most once every 5 minutes, the coordinator runs 'The sweep.' ... and, in the same pass, runs `/sc:sweep`". Also: "Phase 1 adds this duty, not a scheduler."
3. **Why this is asked rather than decided.** Probe finding INV-010 (`adversarial/adversarial/invariant-probe.md:18`): the "no extra scheduler" reading rests on WC-16's sentence, which is about the `/sc:sweep` duty, "not a ban on that cron"; an earlier draft's "GitHub state ... not on a timer" contradicts the cron's PR re-check; "Memory is the lowest source tier, so this needs the owner's confirmation, not a silent pick."
4. **The cadence record.** `merged-requirements.md` section 6.6 (lines 1013 to 1034): every existing clock (WC-16 watch, `/sc:sweep` at most every 5 minutes once runnable, observer 15 seconds, watcher cron 5 minutes after its follow-up, PM checkpoints 30 minutes, GitHub reads at wave gates and wakes) plus the owner's check as the last row: "status is Q31's answer; never runs `/sc:sweep` more often than WC-16 allows and never writes".
5. **A second owner order on how such checks report.** Memory `orchestration-decision-ledger-only.md` (2026-11-09): "For automated orchestration checks, display only outstanding questions or decisions requiring the user ... Do not print DONE/NEXT tables or routine no-action notices on those turns." Lowest source tier; UNVERIFIED that it applies to this program.
6. **Mechanism limit.** The session cron tool (CronCreate) used by the order is session-only and "Recurring tasks auto-expire after 7 days" (CronCreate tool description in this session). A program longer than a week needs the job re-created. Whether a cron fire counts as a "coordinator wake" for WC-16 (and so triggers "The sweep." in that pass) is not stated in WC-16: UNVERIFIED, my reading.
7. **The sweep command is not runnable yet.** Section 6.6 note (line 1031): until SWEEP-RUNNABLE holds (after PR #539 merges and Q29's install route runs), the `/sc:sweep` duty is recorded as "not runnable".

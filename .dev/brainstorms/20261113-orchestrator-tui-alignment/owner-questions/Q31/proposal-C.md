# Proposal C: Yes, read-only, for this program's coordinator

## Answer

Yes. The 2026-11-05 order applies to this program's coordinator as a read-only check: about every 10 minutes it reads the Orca Run, the session list (ListAgents), open PRs on the two fork repositories and renews idle subscriptions on busy peers, and it never writes and never runs `/sc:sweep` more often than WC-16 allows.

## What happens next if the owner picks it

- The ledger records Q31 = yes, read-only, with the date; the last row of the cadence record (section 6.6, line 1026) becomes "in force".
- At W0 the coordinator creates one recurring session cron job at an off-minute about every 10 minutes. Each run: reads the Run's messages, lists agents, reads open PRs with `gh pr list --repo IronbellyOrg/IronClaude` and `--repo IronbellyOrg/Coder` (read only), and re-subscribes `notify_when_idle` on busy peers (a one-shot subscription that sends nothing to the peer).
- Because CronCreate jobs expire after 7 days and live only in the session, the coordinator records the job id and its expiry in the ledger and re-creates it on expiry or after a resume.
- The check reports to the owner only when something needs a decision (owner order of 2026-11-09, memory `orchestration-decision-ledger-only.md`); routine "nothing changed" runs are silent.
- Limits kept (spec line 579): no `/sc:sweep` above WC-16's 5-minute cap, no write of any kind, no grant implied.

## What it unlocks

- Follows the owner's own standing order and the reason behind it: non-worker peers (the PR sessions of Q25 and the #539 author of Q33) never appear in the Orca message queue, so only a timer-driven check sees them go idle.
- PR events (new review comments, CI failures) on the program's PRs are seen within about 10 minutes instead of at the next wave gate.
- Closes INV-010 with an owner answer instead of a silent pick from memory.

## What it costs or risks

- A second clock beside WC-16. If a cron fire counts as a "coordinator wake", each fire also triggers WC-16's sweep pass (UNVERIFIED reading of `WORKER-CONTRACT.md:288`); that stays within the 5-minute cap but adds load.
- About 144 read cycles a day across Orca and two GitHub repos; rate limits were not measured (UNVERIFIED).
- The cron's 7-day expiry and session-only life mean the check can silently stop if the re-creation step is missed.
- The rule stays in a memory note and a ledger row, not in a checked-in file, so the next coordinator outside this program may again miss it.

## What stays unresolved

- Whether the rule should become part of the worker contract for all coordinators (not asked here).
- Whether the order still fits coordinators outside this program.

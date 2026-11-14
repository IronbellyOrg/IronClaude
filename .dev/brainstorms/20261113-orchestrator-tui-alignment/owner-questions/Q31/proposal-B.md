# Proposal B: Yes, and make it a written rule for every coordinator, not a memory note

## Answer

Yes, the ten-minute read-only check applies to this coordinator, and the owner also asks for it to be written into the checked-in coordinator rules (the worker contract's WC-16 loop or the orchestration guide) through its own small PR, so it stops depending on a memory note that the spec ranks as the lowest source.

## What happens next if the owner picks it

- Immediately: same as a plain "yes" for this program. The ledger records Q31 = yes, read-only; the coordinator creates one recurring session cron job, about every 10 minutes off the hour and half-hour, that reads the Orca Run, ListAgents and open PRs on `IronbellyOrg/IronClaude` and `IronbellyOrg/Coder`, and renews idle subscriptions on busy peers. It never runs `/sc:sweep` more often than WC-16 allows and never writes (spec line 1026, line 579).
- Separately: a new work item, outside this program's 50, drafts a one-paragraph addition to WC-16 (for example: "Besides the wait, the coordinator keeps one read-only recurring check of about 10 minutes covering its Run, the session list, open PRs on the named fork repositories and idle subscriptions on non-worker peers; the check never writes and never runs `/sc:sweep` above this cap"). It goes through the normal PR route (`/sc:pr-submit --monitor 3` on the fork), with a test that pins the sentence if the contract has one.
- Until that PR merges, the memory note and the ledger row carry the rule.

## What it unlocks

- Removes the root cause INV-010 found: the order lived only in memory, so two of three debate drafts wrote "no extra scheduler" without it (`invariant-probe.md:18`). Once written in the contract, every future coordinator gets it without being asked again.
- Resolves the WC-16 wording ambiguity ("Phase 1 adds this duty, not a scheduler") at its source rather than with a spec note.
- Lets the contract say once whether a cron fire counts as a "coordinator wake" for the sweep pass, which today is UNVERIFIED.

## What it costs or risks

- Scope growth: a change to an installed core file (`~/.claude/WORKER-CONTRACT.md`) that every project using IronClaude receives. That is a decision for all coordinators, not just this program, made through a question that was framed for one program.
- One more PR during a program whose bottleneck is already owner latency (section 3: "Owner latency is the real schedule").
- The CronCreate mechanism auto-expires after 7 days and lives only in the session; a contract rule that names a 10-minute cron must also say what happens on expiry and on resume, or it writes a promise the tool cannot keep.
- The memory order's GitHub scope (all open PRs on two repos) may be wider than every coordinator needs.

## What stays unresolved

- The exact contract wording and where it lives (WC-16 or the orchestration guide), which the drafting item and its review settle.
- Whether the read-only check's output follows the 2026-11-09 order to show only outstanding decisions (memory `orchestration-decision-ledger-only.md`).

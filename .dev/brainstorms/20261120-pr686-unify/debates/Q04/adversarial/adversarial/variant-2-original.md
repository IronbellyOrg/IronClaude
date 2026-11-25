# Position CLAY (Q04): one go per issue or PR covers every push of the feature branch until merge

Notation as in position-OURS.md: "WC:nnn" is a line of `src/superclaude/core/WORKER-CONTRACT.md`, "D:nnn" a line of `docs/designs/orchestrator.md`, both in `/home/coder/.cache/ic-snap-20261120/master`.

## Claim

The person decides once, per issue (the Full Submit setting) or per PR (the typed `/sc:pr-submit --monitor 3` line), that this branch may be published. Every later push of that feature branch until merge is the same decision carried out. Asking again for each fix-round push adds no safety, because the loop has its own caps and guards, and it defeats the purpose of an autonomous review-and-fix loop. The merge is where the person's go is spent.

## Mechanism

1. Clay's design lets a worker push its own feature branch and open its PR through `/sc:pr-submit --monitor 3` in its own top-level session (ADD1, D:135; owner ruling 3 of 2026-11-19: "workers push and open pull requests, never merge or force-push, only the orchestrator merges", D:1397). The authority line is drawn at merge, not at push.
2. The loop then runs fix rounds by itself: edits, validation, one fix commit per cycle, push, reply, resolve (`src/superclaude/skills/sc-pr-submit-protocol/SKILL.md:291, 308`). The cap is `max_rounds` (default 2, hard cap 5, `pr-submit.md:47`) and `push_count <= max_rounds + 1` (`SKILL.md:262`).
3. One go for the issue or PR therefore covers: the first push, the PR, each fix-round push, a conflict-merge push and CI-fix pushes, until the PR merges or closes.

## Cited facts

1. D:135 (ADD1) and D:117 (DQ7): the handoff worker "may push its own feature branch and open its pull request through `/sc:pr-submit --monitor 3` ... must never merge, delete a branch or force push". The design bounds the worker by what it may never do, not by a go per push.
2. D:1397: "Owner ruling 3: workers push and open pull requests, never merge or force-push, only the orchestrator merges" (the ruling text is in Clay's design table; the ruling is Clay's, see D11 and D06 notes that rulings 1 to 39 are posted under `clayphi`).
3. The built tool already runs unattended after one command: CLAUDE.md of the project ("fixes the confirmed findings ... pushes the fixes without asking") and `pr-submit.md:38` (`--monitor 3 --max-rounds 3`: "full loop: fix, push, reply, resolve"). A per-push go is incompatible with the mandatory way the owner opens PRs.
4. The loop is already fenced at the push: one fix commit per cycle; halts with `push_range_mismatch` rather than publish unreviewed local commits; no force push; no push to the default or protected branch; fast-forward only, with parent checks (`pr-submit.md:121`, `SKILL.md:342-348`). So a go per push re-asks a question the tool already answers mechanically.
5. The owner's own Full Submit rule is a per-issue go: "for an issue the owner has put at Full Submit and approved ..., that setting is the person's go for that issue's push and pull request" (requirements.md R25 row, `claim-handoff-planb`; D04 VERDICT Our strengths; D06 item 7). The owner has accepted that one go can stand for a push and its PR without a typed line per step.
6. A go bound to a head sha cannot exist for a fix commit that is not yet written. The sha pin in D06 and Q01 is designed for merge, where the sha is known (SEC-01, SPEC:288). Binding every push to a sha forces a prompt after every cycle.
7. Merge-time controls already cover the downstream risk: the 13-reason `merge-gate`, `--match-head-commit`, reviewer hold (D06 items 1, 2, 4). A bad fix push is caught at the merge go, which the person must type for the final head.
8. Cost of asking each time: up to 5 prompts per PR (hard cap), each a stop for the person; Clay's own stated aim is fewer interruptions (D06 VERDICT Implications; no measured figure exists).

## What it costs

- A go that lasts for days (a PR can wait for review) widens exposure: any later push of that branch, including a worker script's, is read as covered.
- Nothing in the record ties the go to an end: no sha, no run id, no PR-state check, so merge, close or branch deletion does not void it (compare PR 368).
- "Until merge" is not testable: no event in the system marks the go as spent except the merge itself.

## What it risks

- WC:245 says "no earlier pre-authorization waives this". A per-issue go given before the commits exist is an earlier pre-authorization, so the CLAY form needs the same contract amendment as R25, and wider.
- SEC-13 / D05: a worker's own script can push a feature branch and nothing stops it (INV-025). A per-PR go would make that push look authorized after the fact.
- After a revert or rebase the commit set is different from what the person approved; one go for the PR would silently cover it.

## What it gets right

- Fix-round pushes made by `/sc:pr-submit --monitor 3` are not new decisions; they are the run the person started, inside caps and guards that exist today.
- A per-push go for each fix cycle is not workable without making `--monitor 3` pointless.
- The merge, not the push, is the irreversible step on an unprotected master; keeping the strict go there keeps the owner's brake where it matters.

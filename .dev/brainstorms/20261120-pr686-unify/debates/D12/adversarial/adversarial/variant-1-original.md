# Position OURS (D12): /sc:issue plan sections and planning at claim

Paths below are read from the master snapshot `/home/coder/.cache/ic-snap-20261120/master` (origin/master 61ac2c2e6) unless stated. "Master" means that snapshot.

## Claim

Keep the owner's claim chain where it is. Planning with brainstorm and design happens at claim, after an accuracy check, because an issue body is assumed to be out of date by the time somebody picks it up. Take from Clay only what sits beside that chain: the three plan sections in the templates (PR 661, merged) and, with changes, the plain `--plan` mode (PR 690). Reject moving brainstorm and design into create and refusing plan-less claims (Clay's issue 689).

## Mechanism (how the owner's line works today)

1. `--claim` assigns the issue, runs an accuracy check of the issue text against today's code and the PRs merged since the issue was opened, writes a summary, then in Wave 5 loads `refs/chains.md`, calls `/sc:recommend` with the default chain row for the type and complexity, and writes `next-steps.md`. `/sc:issue` itself never runs the chain commands; the launched agent does, up to the plan boundary of its level (`worktree` stops at a plan a human approves; `full` goes on to implement).
2. `--create` files an issue. It drafts the body with a worker on the tier of the depth and, since PR 661, fills Priority, Fix approach and Test plan at every depth.
3. The owner's pipeline for the watcher picks the command from the issue's Project Status (Research, Spec, Plan, Debug) and the level from the Pipeline field. Planning commands are therefore chosen after claim, per stage, by the person who set the Status.

## Cited facts

1. The owner's own spec for the command, issue 302 "[feat]sc-issue command" (closed), says the claim "Assumes context in issue body is out of date", validates the body against code and later PRs, and then builds a chain by bug or feature and complexity: simple, medium and complex features start with `/sc:brainstorm` (design for medium), then `/sc:workflow`, then `/sc:implement` (issue 302 body, lines 9 to 19, read with `gh issue view 302 --repo IronbellyOrg/IronClaude`). The planning-at-claim shape is the owner's stated design, not an accident.
2. Design record `docs/designs/sc-issue-command.md`: B2 (line 29) the claim writes the next-step prompt and an agent runs it; B4 (line 31) `/sc:recommend` picks the chain; B14 (line 41) brainstorm and implement work run on T1 or T2 by complexity; D23 (line 469) `/sc:recommend` overrides the default row.
3. `src/superclaude/skills/sc-issue-protocol/refs/chains.md:7`: "`/sc:issue` never runs these commands (B2); it writes them into `next-steps.md`". The create-mode workers cannot run them either: `src/superclaude/agents/issue-worker-t1.md:5` (same line in t2 and t3) gives the tools `Read, Grep, Glob, Write, Bash`, with no Skill or Agent tool. Issue 689 asks create to "run the brainstorm and design steps"; it names no actor that can.
4. `/sc:issue` is on the never-as-worker list (`src/superclaude/core/WORKER-CONTRACT.md:23`). So any planning that `/sc:issue` runs must run in a calling session, not in a worker. That is also why Clay's own design says PR 690's plan mode is called by the orchestrator session (design `docs/designs/orchestrator.md`, section 8.3, and risk K27).
5. The owner's zero-setup requirements (unpushed, worktree `claim-handoff-planb`, `.dev/releases/backlog/issue-watcher-zero-setup/requirements.md`): R23 (line 47) Status picks the command (Spec: `/sc:design` or `/sc:brainstorm`; Plan: `/sc:workflow`; Debug: `/sc:troubleshoot --fix`) and R25 (line 51) Pipeline picks the level. If design and brainstorm ran at create, the Spec stage would have nothing left to do and R23 would need a rewrite.
6. Issue 689 is an open issue, not a PR: no assignee, no comments, `updatedAt` 2026-11-20T00:47:18Z (read with `gh issue view 689`). Its own Fix approach says "Settle the decisions marked Decision for Clay in items 2, 5, 6, 7, 8 and 9 with Clay. Nothing is built before this." Nothing in it is built and several of its own decisions are open.
7. Issue 689 would make `--claim` refuse any issue without the three plan sections. PR 661 merged on 2026-11-19T01:29:57Z, so every issue filed before then, and every issue filed by hand through the GitHub forms (issue 689 itself states `.github/ISSUE_TEMPLATE/*.yml` has no plan field; `grep` of the three forms on master finds 0 matches), would be refused. The owner's open issues 339, 409, 423, 431, 444 and 450 were filed before 2026-11-19 (their filing dates are not re-read here; UNVERIFIED), so they would likely be refused.
8. Master claim ignores the plan sections that PR 661 added: `grep` for "Fix approach" in `refs/claim.md`, `templates/next-steps.md` and `templates/issue-summary.md` finds nothing. This is a real gap in the owner's line, conceded below, but it is closed by one rule in claim, not by moving the chain.
9. PR 690 as built keeps the owner's boundary: one body edit, no comment, no label, no assignment, no ClickUp, no worktree, no launch (`commands/issue.md` Will Not, plan line, in the pr-p snapshot). Its drafting worker has the same tool set as claim and create and sees issue text only as fenced data (PR 690 body, "Known limits"; hardening tracked on follow-up issue 665).

## What it costs

- Claim time is expensive: a brainstorm and a design on tier 1b for each medium or complex claim.
- Two places draft a plan today (create's light plan, claim's heavy chain), and claim does not read the first. That is duplicate work and is the one point in issue 689 that is right.
- A person who files by hand gets no plan until claim.

## What it risks

- Keeping the chain at claim leaves the unattended watcher with no plan-before-start check. That is the "hold" question, which belongs to another debate (D-topics on the watcher), not to this one.
- If PR 690's `--remaining` is merged now, it carries an interface for a hand-back loop that does not exist (the `handback` verb is in PR B, unbuilt: design 8.3).

## What it gets right

- Staleness: a design written into the body at filing time is a claim about code that moves. The owner's accuracy check exists to test the body against today's code. A heavy design baked into the body makes the accuracy check validate a design, and a stale design is worse than none.
- Human gate: `worktree` level stops at a plan a human approves (`templates/launch-prompt.md:21-23`). Plan-at-claim puts the human review where the plan is built from fresh facts.
- Small blast radius: no rename of `## Fix approach`, no change to the four templates, no new `## Design` section, no change to the claim refusal rules.
- PR 661 (light plan at create) and PR 690 plain `--plan` already fill the plan-less gap without moving the heavy planning.

## Recommended shape of the owner's line (to compare with Clay's)

- KEEP PR 661 as merged.
- KEEP-ADAPT PR 690: take plain `--plan`, `scripts/plan_body.py` and the deterministic splice; hold back `--remaining` until the hand-back loop exists and is approved.
- REJECT issue 689's moves of brainstorm and design into create, the `## Design` section, the claim refusal and the tier-1 floor at every create depth.
- Add one rule at claim (this is a concession to the point 8 gap): when the issue's three plan sections pass the check, `/sc:recommend`'s suggested route is the short chain (`/sc:workflow` then `/sc:implement`), and the plan sections are quoted into `next-steps.md`.

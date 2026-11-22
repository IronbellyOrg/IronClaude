# D11 position paper: OURS (the owner's line)

Topic: Observability stack: work report, sweep, observer, TUI dashboard.

All paths below are inside the read-only export of origin/master 61ac2c2e6, `/home/coder/.cache/ic-snap-20261120/master` ("M:"), unless another source is named.

## The claim

The human should read one picture of the fleet, built from one read-only fact source. That source is the sweep's JSON (`superclaude sweep run`, schema version 1, PR 539 "sweep: read-only report of Orca sessions"). The terminal observer (`superclaude observe`, the code behind issue 409 "TUI dashboard to manage orchestration at scale") is the one screen that shows it. Clay's daily work report (PR 684 "move the agent-work-report skill into IronClaude") is a useful extra layer of plain-English work items, but it must sit on top of that source and not be a third collector and a third report next to the first two. Clay's report features are adopted where they fill a gap (the notice cap, the table of reasons a person is needed), and only on our rules (read-only facts, nothing recommended by the sweep, approvals given in chat).

## The mechanism

1. Facts layer: the sweep reads Orca (`ALLOWED_ORCA`, a fixed list of argv templates; M:src/superclaude/cli/sweep/probes.py:49-56), git state, transcripts and package ledgers, and classifies every session by fixed rules into eight classes (M:src/superclaude/cli/sweep/models.py, `CLASSES`). It uses no model and writes one dated report and one JSON object. The coordinator runs it on every wake, at most every 5 minutes (WC-16, M:src/superclaude/core/WORKER-CONTRACT.md:287).
2. Screen layer: the observer polls `worker-list` (M:src/superclaude/cli/observe/adapter.py:29) and, with the questions panel on (`QUESTION_GATE_PASSED = True`, M:src/superclaude/cli/observe/commands.py:67), the coordinator's open questions (adapter.py:32). Issue 409's own plan is that it reads "the sweep's JSON, not a second collector" (issue 409 body, "Alignment decisions" item 1, read with `gh issue view 409`).
3. Work-item layer: the report's GitHub, ClickUp and plain-English parts are the only thing the sweep lacks (issue 409 item 3). They join the same pipeline as an added source, written through a contract note, not as a parallel stack.
4. Notice policy: what reaches the person is one table (Clay's nine rows) and a cap on notices, with the entry on the page never dropped.

## Cited facts

1. Master already holds two independent collectors. `observe/` has zero references to `sweep` (`grep -rn sweep src/superclaude/cli/observe/*.py` returns nothing), and both call Orca separately. The planned fix, "read the sweep's JSON", is recorded in issue 409 and in the alignment spec (`.dev/brainstorms/20261113-orchestrator-tui-alignment/merged-requirements.md` lists the contract note `docs/designs/observe-sweep-contract.md` as "NOT WRITTEN"; `find` over the master export finds no such file). A third collector makes the unification harder, not easier.
2. The report is a third collector. Its `sessions.py` finds terminals through `orca terminal list` and the Orca hook file and reads transcripts from a saved position (M:src/superclaude/skills/agent-work-report/scripts/sessions.py:1-28); `collect.py` reads GitHub; `clickup.py` reads ClickUp. No file in the skill refers to `cli/sweep` or `cli/observe` (the only hits for the word "sweep" in the skill are an unrelated paging function in `clickup.py`).
3. The sweep's own design says what it will not do: "Recommend anything, propose an action, or add advice" (M:src/superclaude/skills/sc-sweep-protocol/SKILL.md:61). The observer's design contract is "navigation only" (issue 409 item 2). Clay's report entries carry Options, Recommendation and a typed answer (M:src/superclaude/skills/agent-work-report/templates/needs-you-template.md). Those are two different rule sets, and the owner's rule must win on the sweep and observer surfaces.
4. The report is built for one person. `config.json` sets `"person": "clayphi"`, the time zone is America/Chicago, the ClickUp token is that person's, and the session tag is `coordinator` (M:src/superclaude/skills/agent-work-report/config.json). It also sends a ClickUp direct message (SKILL.md Step 13), which is a write to an outside service, and commits its own state folder (Step 14). The sweep and observer write nothing outside their own report folder or state folder.
5. The report needs a model. SKILL.md line 10 states "Target: about 5 minutes and well under 1M new tokens a run", and Step 10 is "MODEL". The sweep is a script (zero tokens) and is the only one of the three that can run every 5 minutes under WC-16.
6. The design in PR 681 (merged) never mentions sweep, observe or issue 409 (H-design681-map.md lines 10 and 59 in `/home/coder/workspaces/IronClaude/.dev/analyze/pr686-20261120/`), although the analyst map says the living report is "a third view beside `/sc:sweep` reports and the observer" (H-design681-map.md line 59). The owner's alignment decisions (PRs 587 to 589 "orchestrator, observer and issue-watcher alignment decisions") set the chain watcher, then orchestrator, then dashboard.
7. The nine-row table and the cap of 5 are spec text only. In PR 686's head the only trace is the config key `reach_daily_max` parsed in `issue_watch/repos.py:91,262` (`/home/coder/.cache/ic-snap-20261120/pr-a`); no `escalate` verb, no `orchestrator` command group and no file `asks.json` exist in master, pr-a or pr-p (greps found none). The design says "5 is this design's number; Jay's own default is 0, no cap" (M:docs/designs/orchestrator.md:1177, AD-B4). So the cap and the table are policy that can be adopted, but nothing built depends on them.
8. The owner's standing rule for automated reports: show outstanding user decisions only, no heartbeat or timeout chatter (owner memory "Orchestration decision ledger only"). The cap and "when in doubt, a case does not reach Clay" (M:docs/designs/orchestrator.md:668) agree with it.

## What it costs

- A contract note and a pinning test (named in the alignment spec, not written) before the observer can read the sweep JSON.
- The sweep JSON v1 lacks per-item plain-English text, issue and PR links, a step flow and a session-open link (issue 409 item 1). Adding them is an additive change to schema v1 or a schema v2.
- The report keeps working meanwhile, so for a while three outputs exist.

## What it risks

- The unification may stay on paper: the contract note has been "not written" since 2026-11-13.
- An owner-only approach could leave Clay's real daily need (a short written summary per issue, issue 409 comment of 2026-11-11) unmet for months, because the observer's Decision Desk is "NOT BUILT" (alignment spec 0.3).

## What OURS gets right

The sweep and observer follow the owner's decided chain and the read-only rule, run without a model, and have proof-based classes with "could not determine" instead of guesses. The report is a good second layer, but it is the layer, not the base.


# Round 2 findings for #793 (C12): Playbook for unsticking a worker and answering its questions

Checked against master `f2894fc44` (2026-11-24). Round 1: `/home/coder/workspaces/worktrees/IronClaude/Analyze716/.dev/issuecleanup/a716/4/793/findings.md`. Command run: `/sc:analyze src/superclaude/cli/sweep --focus architecture --depth quick` (report `.dev/issuecleanup/b/4/analyze/analyze-report.md`). `WORKER-CONTRACT.md:N` is `src/superclaude/core/WORKER-CONTRACT.md`. `SPEC` = `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/spec/SPEC.md`; `DEC` = `.../DECISIONS.md`; `D15` = `.../debates/D15/VERDICT.md`. `R38` = row 64 of `.dev/releases/backlog/issue-watcher-zero-setup/requirements.md`.

## Alignment with architectural decisions

- **D14 of D15 (`D15:98`) and FR-40 (`SPEC:242`): aligned on the no-approval rule.** "Reject approving permission prompts ... drop approval rules and test cases; S4 stays a report line." The item's done-when ("a test fails if the file contains a permission-approval step") is the same rule. DEC:603: "never answers a permission prompt, never interrupts a worker". `WORKER-CONTRACT.md:123` (S4: capture the screen, never answer the prompt).
- **Existing contract text: aligned, and it already holds the content.** State table S0 to S11 (`:117-130`), ladder L0 to L5 with caps (`:149-156`), nudge text (`:162-166`), typed copy (`:141-145`) and its condition "only to a positively idle prompt" (`:136-138`), "Never on silence" (`:183-193`). Pinned by `tests/skills/test_worker_contract.py` (rows S9, S10, S11 at lines 217-220). The playbook's states come from here, not from Clay's FR-23.
- **R38 (`requirements.md:64`): partly aligned.** R38 adopts no element of Clay's design; the playbook of `agent-work-report`/FR-23 is Clay's (`D08 VERDICT:63` names the line to fix in a skill that PR #700 removed; `src/superclaude/skills` has no `agent-work-report` and no coordinator skill, checked with `ls`). A playbook that copies Clay's rows is not adopted. A thin ref that points at the merged contract rows is consistent with R38 (the contract text is the merged design, PR #434).
- **Restart rule: in conflict inside the contract.** `WORKER-CONTRACT.md:155` and `:158` allow L4 restart on Orca's stall proof within a budget; `:303` says "Never: ... relaunch a dead worker by itself (WC-6 and the person decide)". WC-6 (`:73-81`) makes every retry a new Task and, for a live attempt, needs the person's directed cancellation (`:81`). DEC:327 ("adopt guarded restart with a resume wake, bounded to 3 attempts") and DEC:579 ("C2 guarded restart: adopt with change") come from the Clay rows that R38 supersedes, so that 3-attempt counter must not enter the playbook. Clay's suggestion on #716 (2026-11-24) to restart with a small budget is a proposal, not a decision.
- **WC-10 (`:46`): in conflict with the item's state name "stalled".** Only Orca's stall proofs authorize L4; silence, late heartbeats and context exhaustion are not stalls (`:158`, `:46`). The contract has no state called "stalled"; "errored" is not a state either. A row "stalled -> restart" would break WC-10.
- **WC-3 (`:55-56`) for "answering its questions":** the worker asks once per Task; the coordinator answers with `reply --id`, then the ack timeline (`:132-139`). Aligned.
- **WC-13 (`:63`) and the issue-pipeline duties (`:296-303`):** WC-17 plan approval is the reply to the worker's own ask; it is a plan approval, not a permission-prompt approval. The playbook must keep the two apart (round 1 found a grep for "approve" hits only WC-17 and `:300`).
- **#716 closing review step 4 (2026-11-24): aligned.** It asks for a regression check that includes "no permission-prompt approval".
- **FR-26 (`SPEC:228`):** no `refuse(argv)` dependency for this item; the test is a text scan.

## Complementary issues

- **#782 (C1, skill layout and file-table test):** the refs folder and the file table this issue's done-when relies on ("the file-table test lists it"). Blocked by C1.
- **#774 (docs refresh and the restart-rule contradiction):** settles the rule the playbook states once. Interface: the owner's choice between `:155/:158` and `:303`; the playbook then points at the single rule.
- **#791 (C10, check-in template):** the playbook says what to do with a status answer; S07-F4 asks for the template here, which C10 owns.
- **#806 (C25, template tests):** owns the generic template test; this item's test is about states and prohibited steps.
- **#725 (ask the peer coordinator read-only before a human):** its rule belongs in "when to escalate".
- **#794 (C13, Orca decision gates) and #771 (closeout and the "not done" result):** escalation destinations the playbook names.
- **#795 (C14, report entry):** S14-F14 (record the named state in the issue's entry) waits for it and for #720.
- **#757 and #766 (detection of states):** change how a state is detected, not what the playbook does.
- **#800 (C19):** the last playbook step (settle the worker).

## Closest overlap

**#774 "Docs refresh for the issue watcher and coordinator" (section B, the restart-rule contradiction).** Shared: the one real unresolved piece of C12, the restart rule at `WORKER-CONTRACT.md:155/158` versus `:303`. Estimated share of C12's done-when covered: about 20 percent (it settles the one rule the playbook must state; it does not create the file, the S0-S11 test or the no-approval test). Next two: **#791 (C10)**, about 15 percent (S07-F4 asks for the same check-in template and "each check-in uses the template" test), and **#725**, about 10 percent (adds a peer-first step to the escalation rule). #782 (C1) is a dependency (about 10 percent of the done-when: the file-table test), not an overlap.

## Standalone or merge

**Verdict: stand alone.** Tested against #774:

- Owner: #774 is an owner decision plus a docs edit by the contract's author; C12 is the coordinator-skill author.
- Acceptance test: different. #774 is a docs diff with no behaviour change; C12 is a test that every S0-S11 state has a row, each maps to an allowed action, and no row approves a prompt or interrupts.
- Files: #774 touches `WORKER-CONTRACT.md`, `docs/designs/*.md` and `HOW-WE-WORK.md`; C12 adds a ref file in the skill and a test.
- Build phase: #774 can ship now; C12 waits for C1.
- Risk if merged: the urgent docs and contract fix would wait for a skill that does not exist, and a docs-only PR would carry a new skill file.

Merging into #774 would be right if the owner decides the playbook has no content beyond the restart rule; then C12 reduces to one contract edit and closes. Merging into #782 (C1) would be right if the owner treats the playbook as just the watching-wave ref; that is a build-grouping choice, not a tracking reason, and C12's test is separate.

## Closed issues and merged PRs checked

- **PR #434 (merged 2026-11-08) and #431 (closed):** deliver the states, ladder, nudge and ack timeline the playbook would list. C12 adds only a skill-side entry point.
- **PR #539 (merged):** the sweep and WC-16; the classes the sweep reports are not the S0-S11 states (analyze finding A4), so the playbook cannot be keyed on sweep classes.
- **PR #591 (merged):** WC-17 and G2 (a bound worker asks and sends only to its own coordinator); defines "answering its questions" for plan approval.
- **PR #700 and #701 (merged):** rolled back the 655 build (removing `agent-work-report`) and restored the "no `--to`" duty; so D08's "fix `agent-work-report/SKILL.md:12`" is moot.
- **PR #729 (merged):** R38; voids Clay's rows, including the guarded restart counter.
- **#655 (closed, not planned) and #444 (closed):** source of the Clay playbook and `--sub`; nothing built.
- **PR #724 (merged):** owner records are given in chat; relevant to the "Ruling halt is never asked" part (`WORKER-CONTRACT.md:57`) that the playbook must repeat for answers.

## Updated recommendation

- **Action: keep open with changes.** (1) Make the playbook a thin ref that points at `WORKER-CONTRACT.md` rows (no copy of the table); the test checks that every state S0 to S11 has a row naming its contract section. (2) Let #774 settle the restart rule first; the playbook states it once and does not import Clay's 3-attempt counter. (3) Use the contract's state names; no "stalled" or "errored" row. (4) Drop S07-F4 (duplicate of #791 and #806) and move S14-F14's entry recording to C14. (5) Add the peer-coordinator-first step from #725 to the escalation row. (6) Keep WC-17 plan approval separate from permission prompts.
- **Priority: P3. Complexity: simple, size S.**
- **Versus round 1: action, priority, complexity and size unchanged.** Added: R38 and DEC:327/579 as the reason Clay's restart counter has no standing; the state-name conflict tied to WC-10 (`:46`); D08's `agent-work-report` fix noted as moot; closest overlap named with a share.

## Scan record

- Lists read in full (columns number and title): open-issues.tsv 134 of 134; closed-issues.tsv 157 of 157; merged-prs.tsv 508 of 508.
- Search terms: playbook, stuck, stall, restart, nudge, probe, approval, permission, escalation, liveness, state, ladder, contract, check-in.
- Opened with `gh` (partly read by sections): open #716 (all comments), #774, #725, #782, #787, #789, #790, #791, #794, #795, #800, #806, #757, #766, #770, #771, #767, #590; closed #431, #444, #655 (keyword lines); PRs #434, #539, #591, #729. Not opened: PRs #700, #701, #724 (list titles only).
- Files read: `WORKER-CONTRACT.md` lines 46, 55-63, 73-81, 111-193, 296-303; `tests/skills/test_worker_contract.py:217-220`; SPEC rows 226, 228, 242; DEC rows 327, 579, 603; D15:96-98; D08 VERDICT:63. UNVERIFIED: the playbook text of Clay's FR-23 (not in any file read); which of its rows approve prompts.

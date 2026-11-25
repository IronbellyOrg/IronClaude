# Verdict D04: Claim level and grants

Line references "D:nnn" are to `docs/designs/orchestrator.md` in the master snapshot `/home/coder/.cache/ic-snap-20261120/master` (Clay's merged design from PR 681, the design document). "R23, R25, R33, R36" are rows of the owner's zero-setup requirements file `/home/coder/workspaces/worktrees/IronClaude/claim-handoff-planb/.dev/releases/backlog/issue-watcher-zero-setup/requirements.md`. "owner-answers line N" is `.../claim-handoff-planb/.dev/brainstorms/20261113-orchestrator-tui-alignment/owner-questions/owner-answers.md`.

## Question

When the watcher claims an issue, should it always claim at level none (CLAY R9, D:81) with a standing `grants` list in repos.yaml (DQ6, D:116), or should the issue's Pipeline field choose the launch level (OURS R23, R25, widened 2026-11-19) with one grant row per issue? Include the `/sc:issue --claim` flag semantics (`--pipeline none|worktree|full`, `--submit`) in `src/superclaude/skills/sc-issue-protocol/` and `docs/designs/sc-issue-claim-pipeline-flag.md`.

## Winner

HYBRID. The live claim is level none with one supervised worker (Clay's rule, which is also the owner's own Q35 of 2026-11-14), the owner's Pipeline-level design stays as the named, gated, later design, and the grants split into four standing low-stakes entries and per-PR chat go for merge and close.

## Winning recommendation

The spec must say all of the following (each is testable):

1. **Claim level now: none, nothing else.** Whatever starts a claim passes exactly `--pipeline none`: the watcher's launch prompt on master (`PROMPT_PATTERN = ^/sc:issue --claim [1-9][0-9]{0,8} --pipeline none$`, `src/superclaude/cli/issue_watch/launch.py:33`; `src/superclaude/commands/issue.md:48` "it always passes `--pipeline none`") and, in Clay's design, the orchestrator's wave 1 (D:544). After the claim the orchestrator starts one supervised worker with `orca orchestration worker-start`. Test: the pattern test stays; the K4 test (D:1226) fails if the skill launches through `orca_worktree.py launch` or passes `--pipeline worktree` or `full`.
2. **The Pipeline field is not read while no governed level is allowed.** No Project read for Status or Pipeline until a governed level is allowed. This defers, and does not drop, R23 and R25.
3. **The gate-open design is named and belongs to the owner.** When governed levels open, the Pipeline field picks the level (None = `--pipeline none`, Worktree = `--pipeline worktree`, Full = `--pipeline full`, Full Submit = `--pipeline full --submit`; empty means None; R25, requirements.md line 51). Preconditions, all required: the 12 live observations pass (OB-H1 items 1 to 9, OB-H2, OB-H3, OB-CTX; `tests/hooks/test_launch_level_observations.py`, issue 442 closed, issue 442 is OPEN today per `gh issue view 442 --repo IronbellyOrg/IronClaude`); a reviewed owner commit amends R9 (D:81, "never used"), the K4 test (D:1226) and DQ7 (D:117) in the same change; the change states how the orchestrator watches a launched agent that reports only through `.dev/issues/<N>/result.md` (R24) instead of `worker_done` (D:575); and the change replaces the protection R36 removed (a Pipeline raised after approval; requirements.md line 62). Until then the words "never used" are replaced in the spec by "not used until the owner opens the gate".
4. **Flag semantics of `/sc:issue --claim` are unchanged** (`docs/designs/sc-issue-claim-pipeline-flag.md` lines 69-89; skill `src/superclaude/skills/sc-issue-protocol/SKILL.md`, `refs/claim.md`): `--pipeline none|worktree|full`; `--submit` only with `--pipeline full` (else STOP `E-SUBMIT-NEEDS-FULL`); `--pipeline` or `--submit` with `--create` (STOP `E-CLAIM-ONLY-FLAG`; Clay's design adds the same code for `--plan`, D:1065); a person who types no `--pipeline` gets the level the skill picks from the issue (`full` for a bug or a simple or medium feature of 16 hours or less, else `worktree`); an explicit value wins; the watcher never relies on the default. The level is recorded outside the worktree and a missing guard refuses the launch (`W-ENFORCEMENT-ABSENT`).
5. **Grants: four standing, two per PR.** Standing: `issue.assign`, `issue.comment`, `issue.body.append_plan_sections`, `issue.hold` (bounded, reversible, about the issue's own text; D:116). Not standing: `pr.merge` and `issue.close`. Each is released per PR and head sha by a go that the owner gives in chat, the agent records, and an `answer-check`-style verb accepts, with the owner identity as a parameter (D:694 hardwires Clay's terminal or Clay's ClickUp id). The key is `merge_safety:<PR>:<head sha>` style (D:598). No file row written by the owner (owner's order of 2026-11-17: approvals are given in chat, never written into files).
6. **Controls adopted and scoped honestly.** `E-NO-GRANT` backs only the orchestrator's own verbs (D:696): assignment and claim comments come from `/sc:issue` and are outside it, `pr.merge` is a raw `gh pr merge` (D:588), `issue.close` is written by `/sc:closeout` (D:605). The merge gate (the closed set of thirteen reasons, D:582) gets one added reason, "no recorded merge go", so `merge_ok: true` cannot print without it. Tests: one `E-NO-GRANT` case per standing entry that the verbs do write, and a merge-gate case for the new reason.
7. **Fail closed for the grants list.** An absent or malformed `grants` gives no grants (PR 686 head already reads a missing key as an empty list, `src/superclaude/cli/issue_watch/repos.py:295`), and the `repos` verbs refuse to change `grants` without an accepted answer record. The file must either sit outside the orchestrator's write reach or be guarded by a hook, because D:688 admits the guard is "the verb and a test" only.
8. **No second issue runs on the unguarded worker route** until the owner rules on the guard question: Q34 and Q38 (owner-answers lines 147 and 187) accepted the no-guard worker for one test issue only and said any further issue waits for G2 (topic D05 settles the guard).

## Strongest points

OURS:
1. The Pipeline value is per-issue consent for how far automation goes, including the Full Submit push rule (the Pipeline value plus the `Approved` field is the person's go for that issue's push only). Source: requirements.md lines 47 and 51; `docs/designs/issue-watcher-status-pipelines.md:83` in `claim-handoff-planb`.
2. Merge and close must not be granted in bulk: the old contract line 241 (outward action only on an instruction naming it), line 245 (push needs the person's go, "no earlier pre-authorization waives this"); Clay's R10 is Clay's own ruling (D:71 "Ruling (Clay, 2026-11-18)"), and ADD1 (D:135) admits R10 contradicts lines 239-246; Q38 (owner-answers line 187). B conceded.
3. A level chosen per issue with a guard the agent cannot edit is the only built brake; Clay's workers run with no L1 guard, no L2 hook, `master` unprotected (D:117, K12), accepted for one test issue only (Q34, owner-answers line 147). B conceded this as a verified defect (X-004).

CLAY:
1. None-only is the only route that can run: R33 closes the gate, 12 observations are skipped, issue 442 is open; and it is the owner's own Q35 "B1b" (owner-answers line 184) and the built code (`launch.py:33`, `issue.md:48`).
2. One supervised route: `worker-start` with mailbox, one message handled once per id, check-ins, restart (D:1104, D:575) against a launched agent that reports only through `result.md` (R24, requirements.md line 50). K4 (D:1226) states a one-route reason independent of the gate.
3. Controls OURS lacks: `answer-check` (D:688, D:694), `E-NO-GRANT` with a log of each use (D:696), closed `refuse(argv)` with one test per pattern (D:736, D:1117); they fit the owner's chat-only approval rule better than a hand-written grant row (owner-answers line 130 against the 2026-11-17 order).

## Clay strengths to adopt

- **None-only live route with one supervised `worker-start` worker.** Why: it is the only route that can run today (both advocates agree), it matches Q35 and the code on master, and it has one watch path. Merge: adopt as the live rule; override R9's "never used" and the K4 test text with "until the owner opens the gate" so R25 survives.
- **`answer-check`.** Why: it refuses relayed, wrong-entry, stale and unknown-source answers, which fills the gap that a per-issue row written by an agent from chat has no check. Merge: adopt; parameterise the owner identity (D:694 is hardwired to Clay); the shared `ironbelly` login (owner-answers line 162) means the source test must be "typed in the orchestrator's own terminal by a person", not a login.
- **`E-NO-GRANT` with a log of each grant used.** Why: refusal and audit in code. Merge: adopt for the orchestrator's own verbs; state its coverage gap (at most 2 of 6 entries, INV-006) instead of claiming all six.
- **Closed "may do" list and `refuse(argv)`.** Why: tested denylist for the orchestrator. Merge: adopt (topic D15 lists it); it limits the orchestrator, not the worker.
- **Four standing low-stakes grants.** Why: removes a person from every assign, comment, plan-section and hold write, which the old per-issue row covered (Decision 8, owner-answers line 130). Merge: adopt these four; override the standing `pr.merge` and `issue.close`.
- **No Project read while the gate is closed.** Why: smaller surface; R31 needed a value-time observation and R36 withdrew it. Merge: defer the read (topic D01 decides the approval and Status signals).

## Our strengths that must be kept

- The `/sc:issue --claim` flag semantics and board-value mapping, including `--submit` only with `--pipeline full`.
- The launch-level guard, level state outside the worktree and the fail-closed `W-ENFORCEMENT-ABSENT`.
- R23, R25 and the Full Submit push rule as the named gate-open design.
- The ship gate: 12 pending observations and issue 442 before any governed level.
- Merge and close by a per-PR chat-recorded go, never in bulk; the chat-only approval rule of 2026-11-17.
- Q34 and Q38: the no-guard acceptance covers one test issue only.

## Actions

| Action | Type | Target | Order or dependency |
|---|---|---|---|
| Keep the watcher launch prompt pinned to `--pipeline none` and its pattern test | PR KEEP | `src/superclaude/cli/issue_watch/launch.py:33` (master); Clay's orchestrator wave 1 (D:544) | None; true on master now |
| Keep R23, R25 and R33 code dormant; do not enable the Pipeline read, the per-Status prompt (Tasks 3, 7, 10) or any governed level | LOCAL CHANGE | worktree `claim-handoff-planb`, branch `ironbelly/issue-watcher-zero-setup-plan` | Before the rebase onto master (topic D14) |
| Replace "never used" with "not used until the owner opens the gate" and tie the K4 test and DQ7 text to the same gate decision | DOC | `docs/designs/orchestrator.md` D:81, D:117, D:1102, D:1226 | After D14 decides the fate of the design document |
| Change the default `grants` list to the four standing entries; drop `pr.merge` and `issue.close` from the default and from the example `repos.yaml` (D:291, D:872) | PR KEEP-ADAPT | PR 686 (the open poll rewrite, `repos.py` reads `grants`, `repos.py:295`) and the design doc | With the doc change; PR B (not built) follows |
| Add the gate reason "no recorded merge go" and the per-PR go to the merge gate; parameterise the owner identity in `answer-check` | DOC | `docs/designs/orchestrator.md` wave 6 to 7 (D:582, D:588, D:598, D:694) | Before PR B is built |
| Put the grants file out of the orchestrator's write reach or guard it by a hook; state the fail-closed default | DOC | `docs/designs/orchestrator.md` D:300, D:688 | Before PR B is built |
| Rule on R10 (orchestrator merges and closes) against the contract lines 239-246 and G2, in chat, recorded by the agent | DECISION | repository owner `ironbelly`; WORKER-CONTRACT lines 239-246 | Before `pr.merge` or `issue.close` can become standing |
| Decide who "the owner" is for `answer-check` and for changing grants | DECISION | topics D06 and D16 | With D06 |
| Decide the guard for `worker-start` workers before a second issue runs (Q38, G2) | DECISION | topic D05 | Before the first live issue beyond the test issue |
| Add to R25 the two open requirements for the gate-open design: how a launched agent is watched (`result.md`) and what replaces R36's protection | DOC | requirements.md rows R24, R25, R36 in `claim-handoff-planb` | With the local plan update |
| No revert or close of a PR is recommended by this topic | PR KEEP | PRs 681 to 686 | None |

## Implications

- **Watcher.** The poll stays a claim-at-none trigger. The Pipeline read and the per-Status prompt (zero-setup Tasks 3, 7, 10) become dormant code; merging them now would add a Project read that nothing can use (R33).
- **Coordinator or orchestrator.** One worker route, one watch path (`worker_done` on the Run mailbox). The owner's WORKER-CONTRACT lines 239-246 still say a coordinator acts outward only on a named instruction; PR 682 already removed the "grant row" rule (old line 300) from master, so the per-issue row cannot be restored as an owner-written file. The per-PR chat go replaces it for merge and close.
- **Dashboard and observer.** With none-only, every live worker is a Run-mailbox worker, so the observer needs one data source for now (topic D11). Launched agents (`result.md`) would add a second source later.
- **Claim pipeline.** `/sc:issue --claim` is unchanged. The levels `worktree`, `full` and `--submit` stay built and gated; no watcher passes them.
- **What breaks.** Any test that pins the Pipeline read or per-Status prompt in `claim-handoff-planb`; Clay's K4 test text when the gate opens; Clay's default `grants` list (two entries come out); `answer-check` for any source other than Clay until it is parameterised.
- **What the owner must know.** R9 and R10 are Clay's rulings (D:71, D:688), not the repository owner's; `ironbelly` is a login shared by the owner and every session on this host (owner-answers line 162), so a chat go does not by itself prove who gave it; the fault-finder found 5 HIGH conditions (INV-001, 002, 003, 004, 012) that the spec must state before unattended claiming is called safe.

## Confidence

75 percent. The live rule (none) and the four standing grants are agreed by both advocates and supported by cited sources. The 25 percent is the open owner calls: whether R9 yields to R25 later (C-001, X-001), whether `ironbelly` ratifies R10 (C-007), the identity question (A-003), and the debate did not converge (78.9 percent against 80 percent, status partial). A different answer would follow from: an owner ruling that the orchestrator may merge on a standing grant; or issue 442 closing with all 12 observations passed (which would move the gate-open design forward); or evidence that a second launch route is wanted.

## Unverified

- Whether Clay's design holds any other per-issue stop after a claim: the Round 2 search covered "hold:", pause, skip, stop, `max_in_flight` and `enabled`; Clay's `RULINGS.md` (the full rulings file) and the IronFlow coordinator spec were not read.
- Whether R10's author is Clay alone: D:71 says "Ruling (Clay, 2026-11-18)" and the full report says every ruling read was posted under `clayphi`; chat or call agreement by the owner is not visible.
- The exact order of R9 (D:81, Clay, 2026-11-18) and R25 (owner, 2026-11-19); the 2026-11-18 date of R9 comes from D:71.
- Whether `E-NO-GRANT` covers `issue.comment` for the R24 result comment (INV-006).
- Whether `GOVERNED_LEVELS_ALLOWED` will be pushed: it exists only in the unpushed worktree `claim-handoff-planb` (no match in the master, pr-a or pr-p snapshots).
- `answer-check` behaviour was read from the design text (D:688, D:694), not from running code; PR 686's `repos.py` was read only for the `grants` key.
- The base of the debate (Variant A, OURS) scored 0.854 against 0.783; this concerns the quality of the papers, not the answer.

## Debate artifacts

- `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/D04/position-OURS.md`
- `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/D04/position-CLAY.md`
- `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/D04/adversarial/merged-output.md`
- `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/D04/adversarial/return-contract.yaml`
- `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/D04/adversarial/adversarial/diff-analysis.md`
- `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/D04/adversarial/adversarial/debate-transcript.md`
- `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/D04/adversarial/adversarial/invariant-probe.md`
- `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/D04/adversarial/adversarial/base-selection.md`
- `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/D04/adversarial/adversarial/refactor-plan.md`
- `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/D04/adversarial/adversarial/merge-log.md`
- `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/D04/adversarial/adversarial/return-contract.yaml`
- Variants: `.../adversarial/adversarial/variant-1-original.md`, `variant-2-original.md`
- Adversarial status: partial (convergence 78.9 percent, 5 HIGH unaddressed invariants); the skill ran in full with nested advocate, fault-finder, evaluator and merge-executor agents.

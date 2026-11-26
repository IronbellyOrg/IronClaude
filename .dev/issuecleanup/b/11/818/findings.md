# Round 2 findings: issue 818 (W10, permissions of launched sessions, FU-6)

Item: sub-issue of the watcher umbrella #717. Checked 2026-11-24 against master `f2894fc44` (this worktree equals `origin/master`). Paths below are relative to the IronClaude checkout unless they start with `/home/coder`. "REQ" means `.dev/releases/backlog/issue-watcher-zero-setup/requirements.md`. "UNIFY" means `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/`.

## Alignment with architectural decisions

- **R38 (REQ:64, owner 2026-11-21, the merged watcher is the design): partly aligned.** FU-6 is a follow-up of the merged design (`docs/designs/issue-watcher-setup.md:673`, `docs/designs/issue-watcher.md:865`), so the need survives R38. But the item's own words ("S17 record", "S11-F17", "S11-F28", "D01 text") are rows of the unification plan whose "Clay strengths adopted" rows R38 supersedes. There is no S17 record to write into; the nearest real home is the live-test record `docs/designs/issue-watcher-live-test.md`, which does not exist (checked: file absent; #450's closing comment lists it as never written).
- **Setup runbook rule, `docs/designs/issue-watcher-setup.md:624-628`: aligned (this is the requirement).** Line 627 says "Record the mode you saw ... Read the mode off the session in the live test and do not assume it", and line 628 says "Do not add a second approver before FU-6". Line 626 holds the owner's recorded acceptance of "permission checks off" for the first test session only.
- **R4 (REQ:30, owner 2026-11-18): in conflict with the "block a second approver" half.** R4 makes `ironbelly`, `clayphi` and every repository maintainer approvers automatically, built in `src/superclaude/cli/issue_watch/generate.py:233-247`. A refusal would reject the generated config. The live approvers file already holds 3 ids (read-only look at `~/.config/superclaude/issue-watch.d/IronClaude-approvers.txt` by round 1; I did not reopen it, UNVERIFIED today), so the FU-6 precondition is already past.
- **Owner rule in open issue #753 (2026-11-23, body of #753): in conflict with the block half.** "Every maintainer and every admin must always be allowed to approve." A block until per-actor checks exist refuses what the owner ordered.
- **D01 (`UNIFY/DECISIONS.md:145-160`, "an allowed approver's approval"): aligned with a multi-approver set.** The text allows more than one approver and never mentions FU-6. It is a unification-plan decision, but its approver part matches merged R35 (REQ:61).
- **R33 and the ship gate (REQ:59; `src/superclaude/cli/issue_watch/launch.py:48` `GOVERNED_LEVELS_ALLOWED = False`): aligned.** Only Pipeline None launches, so the claim session runs `/sc:issue --claim N --pipeline none` and starts no agent. The recorded mode matters more once the gate opens.
- **Launch argv pin (`tests/issue_watch/test_security_invariants.py:16`, T10; `launch.py:136-157`): aligned if W10 stays an observation; in conflict if W10 is fixed by adding a permission flag.** The argv is 12 elements and has no permission flag; setup.md:624 says "Do not add a permission flag".
- **D05 (`UNIFY/DECISIONS.md:259-275`, launch guard for started workers) and `UNIFY/debates/D05/VERDICT.md`: do not govern this item.** D05 is about orchestrator-started workers; the watcher's claim session is launched by the poll, and R38(C) drops the orchestrator parts. Not in conflict.
- **WORKER-CONTRACT (`src/superclaude/core/WORKER-CONTRACT.md:57`): aligned.** Any owner acceptance of a permission mode is given in chat and recorded by an agent with the quoted words and the date; the owner is never asked to write a file.
- **Related and not in conflict:** `docs/designs/issue-pipeline-fu1.md:38-42` records the permission flags of the coordinator's `worker-start` worker (`--dangerously-skip-permissions --allowedTools=Grep`, PR 584 body). That is a different session from the poll-launched claim session, so it does not satisfy W10.

## Complementary issues

- **#753 (maintainers and admins always approvers, open):** completes the approver side. W10 supplies the precondition fact (the launched session's mode); #753 supplies the rule. Interface: the approvers file and `cycle.validate_approvers` (`src/superclaude/cli/issue_watch/cycle.py:323`). W10 must not add a refusal there.
- **#442 (live observations OB-H1 to OB-CTX of the launch-level guard, open):** a person in a real session can read the permission mode at the same time. Interface: same live session, different question (guard behaviour versus the mode the launch line gives).
- **#823 (W15, runbook update with captured steps, open):** the runbook sentence at setup.md:627 is where the mode record would be quoted. Interface: W10's one fact becomes a line in W15's runbook text.
- **#722 (owner and AI helpers share one GitHub login, open):** limits what "per-actor" can mean. On one shared login a per-actor check cannot tell a person from an agent (#722 body). W10's flag half is blocked by that decision, not by code.
- **#698 (release-worker and plan-approval checks rest on text matching and an assignee shortcut, open):** the approvers file is read by both the watcher and `issue_pipeline` (`src/superclaude/cli/issue_pipeline/stage_predicates.py:130-137`, from #698 body). Any approver-set rule must be sequenced with #698 item 2.
- **#678 (guard bypass by a bare `claude <prompt>`, open):** matters only once governed levels open; it is the other half of "what a launched session may do".

## Closest overlap

- **#753, "issue-watch: always accept maintainers and admins as approvers".** Shared: the approver set (`generate.py`, `cycle.validate_approvers`, `cli.py check-config`) and the question of who may approve. Share of W10's done-when it covers: about 0% of the record half (nothing in #753 reads a session's permission mode) and it points the opposite way on the block half, so at most 10% by effect (it removes the reason for the block).
- **Next two closest:** #442 (about 15%: a live session where the mode could be read, but its acceptance is about the guard, not the launch line) and #698 (about 5%: shares the approvers file and `stage_predicates.py`, different acceptance).

## Standalone or merge

**Verdict: stand alone, with the block half removed. If the owner drops the flag half, merge the remaining one-fact record into #823 (W15) and close W10.**

| Test against #753 | #818 | #753 |
|---|---|---|
| Owner | the watcher owner | the same owner |
| Acceptance test | a record that names the observed mode of the launched session (a recorded fact) | tests for promotion, demotion, launch account as admin, excluded id, failed read |
| Files touched | docs (live-test record or runbook); optionally `cycle.py`/`cli.py check-config` for a flag | `generate.py`, `predicates.py`, `cycle.py`, `cli.py` |
| Build phase | before more approvers are relied on | after the open design question (live permission read each cycle or refresh on a schedule) |
| Risk if merged | the one-fact record (XS, doable today) would wait for #753's open design, and a block that contradicts #753's done-when would sit inside #753 | none for #753, which would carry a contradiction in its own text |

Why it decides: the observation has a different acceptance test and no code dependency, and #753's own text forbids what W10's second half asks for. Keeping them apart also keeps the safety fact from being buried in an approver-rule debate.

Merging would be right in one case: if the owner confirms the "block or flag" half is dropped, W10 is a single recorded fact that belongs in the live-test record that W15 (#823) writes anyway, and the owner has used that move before (W5 #813 was closed with "make it a one-time runbook check recorded in W15 (#823)", closing comment 2026-11-24T22:10Z).

## Closed issues and merged PRs checked

- **#450 (watcher rollout, closed completed 2026-11-24):** closing comment says the live-test record was never written and the 20 assumed fixtures were not replaced; ship gate closed. Delivers none of W10, confirms the record is missing.
- **#331 (original watcher request, closed completed):** no permission content.
- **#655 (orchestrator proposal, closed not planned 2026-11-23):** source of the item; closing comment says the merged watcher is the design.
- **#813 (W5, closed not planned 2026-11-24) and #809 (W1, merged into #716):** precedent for how the owner settles W-items replaced by automatic checks; shows W10 can be folded the same way.
- **#390 and PR 403 (ccsession `CCSESSION_PERMISSIONS=default` starts Claude without the permission bypass; closed and merged):** deliver the switch that sets the mode (`UNIFY/techref/ISSUE-TO-WORK-PIPELINE-TECHNICAL-REFERENCE.md:1555`: unset means the bypass applies). They do not record what the poll-launched session actually ran with. PR 301 (Orca Claude launches go through ccsession) means the claim session's mode follows ccsession's environment. UNVERIFIED for the two real sessions (#597 and #751): not observed by me.
- **PR 707 (zero-setup watcher, merged):** closed ship gate, Approved field, generated approvers file; the code W10 would touch. PR 584 / 591: coordinator handoff, the `worker-start` flags quoted above.
- **PR 729 (R38 record, merged):** puts the unification plan out of scope as a source of S-ids. PR 700/701: the issue pipeline restored; no permission-mode content.
- **#394 / PR 432 (launch-level guard, closed completed) and PR 469 (L2 pre-push):** the guard exists; the live observations remain open as #442.

## Updated recommendation

- **Suggested action: keep open with changes.** (1) Replace "the S17 record" with `docs/designs/issue-watcher-live-test.md` (to be created) or the #450/#442 observation notes. (2) Drop "refused or flagged" for a second approver (it contradicts R4 and #753); if a flag is wanted, make it a warning in `check-config` that fires only when the recorded mode is checks-off, and only after the owner decides. (3) Remove the unification-plan row ids. (4) Fall back to merging into #823 if the owner drops the flag.
- **Priority: P2.** Unchanged from round 1: one safety fact, bounded exposure (Pipeline None, closed ship gate), and two real claim sessions already ran with an unrecorded mode.
- **Complexity and size: simple, XS** for the observation alone. Changed from round 1's "medium, S overall": the S part was the block half, which conflicts with R4 and #753 and is not recommended. If the owner keeps a flag, it returns to medium, S.
- **What changed from round 1:** the closest-overlap choice and merge fallback are new; the alignment evidence added R4, R33 and WORKER-CONTRACT:57; the action and priority are unchanged in substance.

## Scan record

- Lists read in full: open-issues.tsv 134 rows, closed-issues.tsv 157 rows, merged-prs.tsv 508 rows (all three).
- Search terms used over titles and bodies: permission, bypass, approver, approvers, second approver, launch, FU-6, guard, ccsession, maintainers, shared login, W10, watcher, claim.
- Opened with `gh issue view`/`gh pr view` (read-only) and read: open issues #717 (body and closing review), #753, #442, #698, #722, #678, #788, #816, #814, #821, #822, #823, #774, #777, #761, #770; closed issues #450, #331, #655, #813, #809; merged PRs #707, #729, #584, #591, #447, #759. Bodies of #753, #442, #698, #722, #816, #814, #823, #821, #822, #450, #331 and the PR bodies were read; #716, #761, #774, #777, #770, #678, #757, #775, #773, #776 were searched by keyword and not read end to end.
- Source checked on master: `launch.py:48, 136-157`, `generate.py:228-248`, `cycle.py:323`, `docs/designs/issue-watcher-setup.md:624-628, 671-679`, `docs/designs/issue-watcher.md:862-873`, `tests/issue_watch/test_security_invariants.py:16`.
- Command line run: `/sc:analyze src/superclaude/cli/issue_watch --focus architecture --depth quick --unattended --report-dir .dev/issuecleanup/b/11/analyze` (one run for all three items; report in that directory).
- UNVERIFIED: the permission mode of the two real claim sessions; whether Orca applies default agent arguments (FU-6's own question); the live approvers file content today.

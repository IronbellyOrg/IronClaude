# Verdict D14: Final disposition of PR 686, the PR stack and the merged design doc

Notation. "Dnn" = `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/Dnn/VERDICT.md`. "Planb" = the owner's unpushed branch `ironbelly/issue-watcher-zero-setup-plan` in worktree `/home/coder/workspaces/worktrees/IronClaude/claim-handoff-planb`. "Go" = the owner's approval of one named action, given in the owner's chat and recorded by the agent as a quote with the date (one login, `ironbelly`, serves the owner and every host session, so a GitHub comment under it proves nothing). Every disposition below is a recommendation; this task took no GitHub, Orca or git action. Full text with every condition: `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/D14/adversarial/merged-output.md` (sections 3 to 6).

Two corrections to the question: 687 and 689 are ISSUES, not pull requests (`gh issue view 687` and `689` resolve, `gh pr view` does not). And a new owner PR exists since the inventory: PR 693 (saves the claim launch result file, issue 691, opened 2026-11-20 04:15Z); it edits four of the same files as PR 690.

## Question
Using the verdicts D01-D13 (in /home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/D*/VERDICT.md; read all that exist), decide per item: PR 686 (open, rewrite of the watcher, head 8e5ae29ad), branch issue-655-pr-p/PR 690, PRs 687 and 689, the merged design doc from PR 681, PR 682 (merged), PRs 683 and 684 (merged). For each: MERGE as is, REBASE-AND-ADAPT, SPLIT, CLOSE, REVERT, or KEEP. Also issue 655 and the owner's issue 450 (Clay's issue "replaces 450").

## Winner
HYBRID: the owner's rules decide what lands and in what order (PR 682 reverted, PR 686 never merged as it stands), and Clay's evidenced points set how (two lanes, adapt in place and keep review history, PR 690 first, the eight removal PRs not reverted).

## Winning recommendation
The spec must say all of the following (full tables in `merged-output.md`).

**Dispositions (recommendations; each needs a go before anyone acts):**

| Item | Disposition | Condition first |
|---|---|---|
| PR 686 (Clay's rewrite of the watcher, open, 59 files) | REBASE-AND-ADAPT in place, as a draft. Not MERGE, not SPLIT, not CLOSE | Revert merged; planb landed first; D08 names settled; PR 690's `plan_body.py check` merged; the merge checks below; drops the deletions of D01's must-keep symbols, the registry, `repos.py`, the label writer |
| PR 690 and branch issue-655-pr-p (`/sc:issue --plan`, `--remaining`, open) | REBASE-AND-ADAPT, lane 1, then merge | PR 693 merged first; D12's four fixes with tests; green CI; draft until fixed; go |
| Issue 687 (daily worktree cleanup; an issue) | KEEP-ADAPT (edit text; nothing built) | Owner's chat approval of the cleanup design; ruling on local `git branch -d` |
| Issue 689 (plan everything at creation; an issue) | SPLIT and DEFER | `--mode other` and form fields to a small new issue after PR 690; items 1, 2, 4, 8 wait for the owner's ruling on B2 |
| PR 681 (merged design doc) | KEEP, not reverted: banner now, same-PR correction of the three "gate retired" statements inside the revert PR, later owner-reviewed amendment PR | No builder starts PR B or PR E (unbuilt orchestrator skill and live test) before the amendment merges |
| PR 682 (merged deletion of `issue_pipeline`, WC-17, guard rule 1) | REVERT as one new PR plus the "no `--to`" bullet re-applied | Owner says in chat that BOTH gates stay (start approval and plan approval after claim); dry run in a clean git checkout bound to a master head sha passes; go. If the owner says only the start gate stays, PR 682 stands (D03 item 7) |
| PR 683 (`/sc:closeout`, merged) | KEEP | Its `/sc:issue --plan` reference resolves once PR 690 merges |
| PR 684 (work-report skill move, merged) | KEEP-ADAPT (follow-up PR) | D08 wording fix (`SKILL.md:12`), D11 config and state path |
| Issue 655 (Clay's tracking issue) | KEEP and RESCOPE | Assignee `clayphi` edits it: drop "replaces #450" |
| Issue 450 (owner's rollout issue) | KEEP open, and answer Clay's 2026-11-18 comment | Its live test, shadow run and cron stay required under every verdict |
| PR 693, PR 685 (owner's open PRs) | MERGE (693 first); KEEP and merge (685) | Own review loops; 693 before 690 |
| Eight removal PRs (620, 622, 627, 629, 631, 632, 650, 656) | KEEP, not reverted | One non-blocking owner question; blocks only host install |
| All other Clay PRs in the inventory (tables 2A to 2C) | KEEP | None |

**Order of operations** (three lanes after a hold step):
- H0 hold: ask Clay to make PR 686 and PR 690 drafts and not merge until told; recommend a ruleset on `master` requiring a review by someone other than the author (`protected` is false today).
- Lane 1: merge PR 693, adapt and merge PR 690, then the claim rule C1 of D12.
- Lane 2: dry run, revert PR (with the same-PR gate correction), banner, contract and guard amendment PR (lines 57, 70, 245, 298, 300; guard comment 441-443; `core/CLAUDE.md:58`), planb committed, pushed as a draft and landed first, design amendment PR, then the adapted PR 686. Per-host check before any `superclaude install`.
- Lane 3: the verdict actions no step carried (D11 contract note, PR 685, D10 live spike, D02 cron line, and so on; `merged-output.md` section 8).

**Mechanical merge checks** for any PR touching `issue_watch/` or restoring `issue_pipeline`: `uv run superclaude --help` exits 0; every package under `src/superclaude/cli/` imports; a names check derived from the imports of the restored package (35 names; 9 are missing on the PR 686 head, including `EVENTS_JQ`, `argv_edits`, `github.edits`, `github.events`); a test that removing the approval between wake and start refuses; a test that the global `enabled` flag absent means off; the Rule B test (an acknowledgment without a state file leaves the wake entry in place); `make verify-sync`.

## Strongest points
OURS:
1. Revert plus PR 686 merges with no git conflict beyond CHANGELOG.md and then crashes `superclaude --help` (29 test modules fail at collection), because PR 686 deletes `issue_watch` names the restored package imports. Source: D03 Winning recommendation item 3; checked again in the debate (pr-a lacks names master has; invariant probe INV-007 found 9 of 35 missing).
2. PR 686 deletes the code D01 keeps (14 predicate symbols, about 30 in `github.py`); the owner's rules decide every contested rule in all 13 verdicts. Source: D01 "Our strengths that must be kept"; `gh pr view 686` (`predicates.py` +114/-207, `github.py` +535/-426).
3. PR 682 merged 66 minutes after opening with a bot review only, deleting owner PRs 584 and 591 merged three days earlier, and no review or comment by `ironbelly` exists on PRs 681 to 684, 686 or 690; `master` is unprotected. Source: D03 Strongest points OURS 1 and 3; `gh api repos/IronbellyOrg/IronClaude/branches/master`.

CLAY:
1. Independent work should not queue behind the hardest item: PR 690 and PR 693 share no code with the revert or PR 686. Source: round 1 CLAY strengths 1 to 3; conceded by OURS (round 2, R-1).
2. No verdict says CLOSE for PR 686 (nine rows say KEEP-ADAPT) and no module of it runs by itself on post-revert master (10 of 13 `predicates` names missing), so adapt in place and keep the review history. Source: round 1 CLAY strengths 4 and 5; round 2 OURS R-2.
3. Both sides missed things that Clay's advocate found: the eight confirm-approval removal PRs, the install step as a hidden prerequisite, the clean-checkout condition for the dry run, and verdict actions no step carried. Source: round 2 CLAY section 3.

## Clay strengths to adopt
- **Two lanes.** What: PR 693 then PR 690 do not wait for the revert. Why: no shared code (only `CHANGELOG.md`), and PR 683 already points at the `--plan` flag that exists only in PR 690. How: lane 1 in `merged-output.md` section 4; the owner's PR 693 goes first.
- **Adapt PR 686 in place, keep it open, keep credit.** What: no "close and re-file". Why: no verdict says CLOSE; no module runs alone. How: draft until adapted; who adapts is owner question Q2.
- **`plan_body.py check` as the single plan check** imported by the adapted `hold.py` (D12, D01).
- **The wake envelope and acknowledgment code, the merge-gate keys, the four standing grants, the in-flight cap and guarded restart as ideas** (D10, D06, D04, D07), renamed and re-homed as those verdicts say.
- **Pinned test that `enabled` absent means off, and R33 built before R18**: Clay's advocate showed the "brake" is one config default (`cycle.py:228`).

## Our strengths that must be kept
- Revert PR 682 before any merge of PR 686; both gates (start approval and the plan approval after the claim) stay until the owner rules otherwise.
- The approval, trigger, Project and approver code in `predicates.py`, `github.py`, `cycle.py` (D01), and the restored `issue_pipeline` package with its 117 tests and the planb branch that builds on it.
- The poll writes nothing to GitHub (NG-2); no registry repo; "coordinator" not "orchestrator"; names fixed before any merge (D08).
- Every approval, go and ruling given in the owner's chat and recorded by the agent; never a hand-written file.
- A person's typed go for every merge; `master` unprotected makes this the only brake until a ruleset exists.

## Actions
| Action | Type | Target | Order or dependency |
|---|---|---|---|
| Ask Clay to make PR 686 and PR 690 drafts and not merge; recommend a ruleset requiring a non-author review on `master` | DECISION | Owner (admin); PRs 686, 690; `master` settings | First (H0); the plan is falsified by one merge click otherwise |
| Merge the owner's PR 693 | PR KEEP | PR 693 (issue 691) | Lane 1 step 1; needs its own `/sc:pr-submit --monitor 3` loop |
| Rebase onto master plus 693 and fix four items (fence-aware heading count, one definition of "passes", document the `--remaining` caller, confirm live head), then merge | PR KEEP-ADAPT | PR 690 / branch `issue-655-pr-p` | After PR 693; independent of the revert |
| Add claim rule C1 and the manual-claim warning | LOCAL CHANGE | `sc-issue-protocol` `refs/claim.md`, `refs/chains.md`, `templates/next-steps.md`, tests | After PR 690 |
| Owner answers Q1 (both gates stay?) | DECISION | Owner, in chat | Before the revert PR |
| Dry run of the revert in a clean git checkout, bound to a master head sha, repeated if master moves | LOCAL CHANGE | throwaway checkout, nothing pushed | Needs no go; before the revert PR |
| Open the revert of commit 01e7a9e23 with the "no `--to`" bullet and the same-PR correction of three design statements | PR REVERT (recommendation only; not executed here) | PR 682 | After Q1, H0, dry-run record; before any merge of PR 686 |
| Banner on the design doc ("contested, not owner-approved"; check dated 2026-11-20) | DOC | `docs/designs/orchestrator.md` (PR 681) | Beside or inside the revert PR |
| Contract and guard amendment (lines 57, 70, 245, 298, 300, guard comment 441-443, `core/CLAUDE.md:58`) | LOCAL CHANGE | `WORKER-CONTRACT.md`, `launch-level-guard.sh`, tests | After the revert; needs the owner's chat approval of R25, R17, R9 for lines 70 and 245 |
| Design amendment PR for the remaining nine rows; no PR B or PR E before it | DOC | `docs/designs/orchestrator.md` | After the owner's rulings on D01 to D13 |
| Commit planb, push as a draft, rebase onto post-revert master, land first; do not resume the half-finished `/sc:implement` ledger across the rebase | DECISION | Owner; planb | After the revert (Q4); D01 and D03 conditions R33 before R18 |
| Rename persisted wake names and write the glossary note | DOC | D08 names; `HOW-WE-WORK.md`; PR 686 pieces | Before any edit of PR 686 |
| Adapt PR 686 in place as a draft with the merge checks | PR KEEP-ADAPT | PR 686 (head 8e5ae29ad) | After lane 1 step 2, revert, planb, Q2, Q4; M1 Rule B, M2 fix, shared terminal helper |
| Per-host diff of installed guard and contract before any `superclaude install`; no blanket install until the eight removal PRs are confirmed | LOCAL CHANGE | each host | After the revert and the amendment PR; blocked by NB-1 for hosts that would run the retire step of PR 633 |
| Keep PR 683; follow-up PR for PR 684 | PR KEEP / PR KEEP-ADAPT | PRs 683, 684 | 683 depends on 690 landing; 684 after D08 |
| Keep issue 450 open and answer Clay's comment; rescope issue 655; adapt issue 687; split issue 689 | DECISION | Issues 450, 655, 687, 689 (assignees edit; agents write nothing) | After Q1; the 689 split after PR 690 |
| Confirm the eight removal PRs | DECISION | Owner; PRs 620, 622, 627, 629, 631, 632, 650, 656 | Non-blocking; blocks only host install |
| Merge PR 685 (issue 442 evidence) and run the lane 3 verdict actions | PR KEEP | PR 685; `merged-output.md` section 8 | Independent of lanes 1 and 2 |

## Implications
- **Watcher.** PR 686 will not become the watcher as written. The owner's approval, trigger and Project code stays; the adapted PR 686 supplies the plan check, the wake file with acknowledgment (renamed, M1 and M2 fixed), merge-gate keys and the wake-line builder on top of planb. Nothing is switched on: `enabled` stays false and the poll command contract (D02) is open.
- **Coordinator or orchestrator.** Restoring the revert brings back WC-17, the approval verbs and guard rule 1; the contract amendment rewords "grant row written by the owner" to "given in chat, recorded by the agent". No coordinator skill or `commands/coordinator` exists on master, so WC-17 has no executor yet; protection rests on owner vigilance until PR B-equivalent work is built.
- **Dashboard and report.** No change from this topic; D11's contract note and `session_id` field are lane 3 and independent.
- **Claim pipeline.** Order 693, 690, then claim rule C1; issue 689's items wait for the owner.
- **What breaks.** If PR 686 merges first, the revert is no longer clean and `superclaude --help` crashes. A blanket `superclaude install` would run the retire step and remove skills of PRs 632, 650 and 656 from the owner's host. The design doc, uncorrected, orders the deletion of a gate the repo would have again.
- **The owner must know.** Everything here is a recommendation. The plan is only as strong as H0: with no hold and no ruleset, one merge click falsifies it. Counts changed since the analysis: planb has 348 status entries today (69 code, tests and docs), not 225, and overlaps PR 686 on 23 files (7 source).

## Confidence
About 80 percent in the disposition set (an estimate from the scoring matrix, not a measurement). All 21 diff-point positions were agreed by both advocates after round 2; the debate is partial because four HIGH invariants were left to this plan as conditions. It drops to about 50 percent if the owner answers Q1 "only the start gate stays" (PR 682 then stands) or if the dry run of the revert fails; it rises to about 90 percent once the dry-run record exists and passes, planb is pushed as a draft, and H0 is in place.

## Unverified
- The revert tree has not passed the full test suite and `tests/hooks/test_launch_level_guard.py` (did not finish in D03).
- The merge-only trial of PR 690 onto master plus PR 693 was not run; PR 690 and 693 share four files, so it is never conflict-free by file list.
- Whether a resent wake with an acknowledgment file present delivers the same wake id twice.
- How Coder's template updates reach hosts, and which other hosts exist.
- Whether the owner saw issue 450, 655 or PRs 681 to 690 outside GitHub (chat, calls); the shared login weakens the GitHub evidence.
- Q01 (who writes a grant row), Q02 (cleanup script may delete local branches) and Q03 (dormant label code in PR 686) have no VERDICT.md yet; this verdict assumes the defaults in the debate (agent records the owner's chat go; label writer left out of the adapted PR 686; `git branch -d` open). If those verdicts differ, rows for issue 687, the amendment PR and PR 686 change.
- The "ruling of 2026-11-20" quoted in issue 689 (Clay's, unverified).
- The evaluators scored the opening papers knowing the final debate state; the per-criterion disagreement log of the two passes was not itemised. Scores are estimates.
- Owner PR 693's merge state beyond "open, mergeable, six checks green" at the time of the probe (08:30 UTC).

## Debate artifacts
- /home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/D14/position-OURS.md
- /home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/D14/position-CLAY.md
- /home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/D14/adversarial/merged-output.md
- /home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/D14/adversarial/return-contract.yaml
- /home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/D14/adversarial/adversarial/diff-analysis.md
- /home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/D14/adversarial/adversarial/debate-transcript.md
- /home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/D14/adversarial/adversarial/invariant-probe.md
- /home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/D14/adversarial/adversarial/base-selection.md
- /home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/D14/adversarial/adversarial/refactor-plan.md
- /home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/D14/adversarial/adversarial/merge-log.md
- /home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/D14/adversarial/adversarial/return-contract.yaml
- /home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/D14/adversarial/adversarial/rounds/ (round1-advocate-OURS.md, round1-advocate-CLAY.md, round2-rebuttal-OURS.md, round2-rebuttal-CLAY.md, qual-pass1.md, qual-pass2.md)
- Adversarial skill ran in full (Skill tool and nested agents available): 2 advocates, 2 rebuttals, 1 fault-finder, 2 evaluators, 1 merge-executor; status partial.

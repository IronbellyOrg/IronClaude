# D14 position: OURS (the owner line)

Question: what is the final disposition of PR 686 (Clay's rewrite of the watcher, head 8e5ae29ad), PR 690 (branch issue-655-pr-p), issues 687 and 689, the merged design doc (PR 681), the merged deletion (PR 682), PRs 683 and 684, issue 655 and issue 450?

All "Dnn" references are verdicts in `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/Dnn/VERDICT.md`. Terms: "the gate" = a person's approval before work starts (owner requirements R19, R22, R35, R36). "Planb" = the owner's unpushed branch `ironbelly/issue-watcher-zero-setup-plan` in worktree `claim-handoff-planb`.

## Claim

The contested rules must not land, and the order of operations matters more than any single disposition. Concretely: (1) revert PR 682 first as a new PR; (2) do not merge PR 686 as it stands: split it, keeping only the additive, read-only and rule-compatible parts, and close the original once the pieces are re-filed; (3) keep PR 681's design file but stamp it "contested, not owner-approved" and amend it to the unified rules; (4) keep PRs 683, 684, 690 with named adaptations; (5) keep issue 450 open (it is the owner's rollout issue) and rescope issue 655.

## Mechanism

- All thirteen verdicts D01 to D13 are HYBRID with the owner's rule as the base on every contested rule: the approval gate stays (D01), cron stays (D02), the plan-approval package returns (D03), claim level none now with the owner's Pipeline design kept (D04), the launch guard is required for started workers (D05), merge only on a person's typed go (D06), project-local coordinators with no registry repo (D07), "coordinator" not "orchestrator" (D08), the poll writes nothing to GitHub (D09), no GitHub text on a typed line and no copied terminal code (D10).
- PR 686 implements the opposite on at least seven of those: it removes the approval, trigger and Project code, adds a registry, a label writer, wake names with "orchestrator" in them, and a copied terminal helper. Merging it and fixing forward means re-adding what it deleted.
- The cheap time to fix wire names, schemas and rules is before merge (D08 action: "Must land before any merge of it"; Clay's own point that wire names are cheap until merge).

## Cited facts

1. Reverting PR 682 and merging PR 686 together gives a broken CLI: `superclaude --help` crashes and 29 test modules fail at collection, because PR 686 deletes `issue_watch` names the restored `issue_pipeline` package imports (`EditEvidence`, `LabelEvent`, `CommentEdit`, `github.edits`, `github.events`, `cycle.validate_approvers`). Git sees no conflict beyond CHANGELOG.md. Source: D03 VERDICT.md, Winning recommendation item 3 (fault-finder INV-001).
2. PR 686 would delete 14 symbols in `predicates.py` and about 30 in `github.py` that D01 says must survive (`approval_of`, `unchanged_since`, `project_check`, `marker_in_window`, `eligibility_order`, the evidence dataclasses). Source: D01 VERDICT.md, "Our strengths that must be kept"; `gh pr view 686 --repo IronbellyOrg/IronClaude` files: predicates.py +114/-207, github.py +535/-426, cycle.py +1478/-652.
3. PR 682 was opened 2026-11-19 22:56 UTC and merged 2026-11-20 00:02 UTC (66 minutes), 3 seconds after PR 681, both by `clayphi`, with only a bot review; it deleted PRs 584 and 591, merged by the owner three days before (2026-11-17), which implement owner Decision 6 = B. Source: D03 VERDICT.md Strongest points OURS 1 and 3; inventory/clay-prs.md table 2A.
4. No GitHub review, approval or comment by `ironbelly` exists on PRs 681 to 684, 686, 690 or issue 655; the design says "approved by the owner (Clay)"; branch `master` has `protected: false`. Source: FULL-REPORT.md section 4 and section 1 point 7; `gh api repos/IronbellyOrg/IronClaude/branches/master` printed `protected:false` (2026-11-20).
5. Planb has 225 status entries and edits the same six `issue_watch/` files PR 686 rewrites; its 13-file tracked patch passes `git apply --check` on the revert tree and fails on current master for all 13 files. Source: D03 VERDICT.md Our strengths; inventory 5C (223 entries then, 225 now by `git status --short`).
6. PR 686's wake transport has two HIGH defects: M1 (acknowledgment can precede the per-issue state file, so a crash loses the issue; `cycle.py:777-810`) and M2 (an abandoned wake is never re-woken and a new orchestrator rejects it as `wrong_target`; `cycle.py:994`, `route.py:407-413`), plus a blind session lookup that starts a duplicate (`wake.py:609-621`). Source: D10 VERDICT.md, recommendation items 8, 10, 11.
7. The registry design (`.orchestrator/orchestrators.json`, `IronbellyOrg/IronOrchestrator`) needs a hand-made clone at an absolute path; on this host `/home/coder/workspaces/IronOrchestrator` does not exist, against owner requirement R17 "Nothing in the setup is manual". Source: D07 VERDICT.md, Strongest points OURS 2.
8. The label-writing code (`hold.py`, `LabelWriter` in `github.py`) contradicts NG-2 ("the poll writes nothing to GitHub") with no evidenced benefit; the plan check also lets the unfilled template through because only HTML comments are stripped (`hold.py:69-70, :140`). Source: D09 VERDICT.md, recommendation item 6.
9. The design PR's own text admits its contradictions with the owner's contract: ADD1 says autonomous merge "contradict[s]" WORKER-CONTRACT lines 239-246, and the command name `/sc:orchestrator` is not an owner decision (OQ5 Owner column "no"). Source: D06 VERDICT.md Strongest points OURS 1; D08 VERDICT.md Implications.

## What it gets right

- It keeps every separable Clay benefit: `plan_check` and `hold:backlog` as read-only skip reasons (D01), `/sc:issue --plan` (D12), merge gate, answer-check and reviewer hold (D06), wake file with acknowledgment (D10), in-flight cap and guarded restart (D07), the report layer (D11), closeout (D13).
- It protects the owner's merged work and the one local branch that builds on it.
- It turns a design the verdicts changed in ten places into one set of rules before code ships under them.

## What it costs

- Clay's 59-file PR cannot land as a unit. About 88 percent of its deleted lines are tests, but the live source changes (cycle.py, github.py, predicates.py, launch.py, record.py) must be redone or re-split. Authors lose review history on one PR (64 Clay comments, 27 Augment, 24 Codex reviews).
- A 4,599-line revert PR, with a CHANGELOG conflict and a re-applied "no `--to`" bullet.
- Delay of every later PR (B and E are unbuilt, so little is blocked now).

## What it risks

- The revert tree is not verified: the full test suite and `tests/hooks/test_launch_level_guard.py` did not finish in the fault-finder's time (D03 Unverified).
- Treating closing PR 686 as a rejection of the contributor; the split must credit Clay and keep the branch.
- All owner decisions are recorded here as recommendations; none is made until the owner gives them in chat.
- It leans on verdict confidences between 62 and 85 percent; D02 (cron) is the thinnest at 62.


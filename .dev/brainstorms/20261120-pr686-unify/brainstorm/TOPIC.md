# Brainstorm topic: one unified design for the issue watcher, the coordinator (orchestrator), the TUI dashboard and the issue-claim-to-work pipeline

## Situation
Two lines of work grew in parallel in the IronClaude fork (IronbellyOrg/IronClaude). OURS is the repository owner's (login `ironbelly`): the built issue watcher (PRs 447, 448), the claim handoff and pipeline (PRs 584, 591, 693), the sweep (PR 539), the observer and TUI dashboard design (issue 409), the owner's unpushed zero-setup watcher plan in the local worktree `claim-handoff-planb`, and the owner decision records. CLAY's (login `clayphi`, they/them) is the orchestrator design merged in PR 681 (`docs/designs/orchestrator.md`), PR 682 (deleted the owner's merged `issue_pipeline`), PR 683 (`/sc:closeout`), PR 684 (`agent-work-report`), and open PRs 686, 687, 689, 690. The full story is in /home/coder/workspaces/IronClaude/.dev/analyze/pr686-20261120/FULL-REPORT.md.

## What is already decided (do NOT reopen; build on it)
Sixteen adversarial debates settled the contested points. Read every verdict first: /home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/D01 .. D16 and Q01 .. Q03, each `VERDICT.md` (D15 and D16 may still be in progress: use them if present). The owner order is: the owner's work and designs take precedence and carry more weight; Clay's clearly better, separable elements are folded in. The two technical references describe what exists today: /home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/techref/ISSUE-TO-WORK-PIPELINE-TECHNICAL-REFERENCE.md and /home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/techref/OBSERVER-SWEEP-DASHBOARD-TECHNICAL-REFERENCE.md. The Clay PR inventory is /home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/inventory/clay-prs.md.

## What to design (the open part)
Combine the settled verdicts into ONE end-to-end architecture and a staged migration, covering these four pieces and how they connect:
1. Issue watcher: trigger, approval gate, plan check, scheduler (cron plus one dispatcher), wake transport, what the poll may write.
2. Coordinator (also called orchestrator): the `/sc:coordinator` role, its per-project layout, authority and grants, wave flow from claim to merge, the escalation table, audit.
3. TUI dashboard and observability: sweep JSON as the one source, the observer as the one screen, the work report as the plain-English layer.
4. Issue claim to work pipeline: `/sc:issue --claim`, launch levels and the gated Pipeline field, the launch guard, closeout, cleanup, `/sc:issue --plan`.
For each piece say: what stays (ours), what is adopted from Clay, what is rewritten, and the interfaces between pieces (files, verbs, names). Resolve any contradiction between verdicts explicitly (name both verdicts and pick one with a reason).

## Constraints
- Local changes and pull request actions are RECOMMENDATIONS in a spec; nothing is pushed, merged, reverted or commented by the brainstorm.
- The owner's unpushed branch `ironbelly/issue-watcher-zero-setup-plan` (worktree `claim-handoff-planb`) lands first; PR 686 is adapted afterwards as a draft (D14).
- Installed primitives never hardcode `src/superclaude/` paths; UV only; no GitHub write; every gh call passes `--repo IronbellyOrg/IronClaude`.
- Keep the plan realistic for a small team: each stage independently shippable and testable, with a rollback.

## Deliverable
A unified design with: the target architecture (with a plain-English diagram), the ordered migration stages (each: scope, files or PRs, tests, rollback, preconditions), the interface table, the list of open owner actions, and the risks. Be explicit about what is built today versus not built.

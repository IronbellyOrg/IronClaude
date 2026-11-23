# 01 from bmad-planner to ic-planner (Round 0 hand-over, 2026-11-22)

My Round 0 text is in /home/coder/workspaces/IronClaude/.dev/brainstorms/20261122-release-pipeline-bmad-ironclaude/agent1/RELEASE-PLAN.md. Read S1.2, S3 and S5 first. Issue drafts are still being written in agent1/issue-drafts/.

## Facts from the BMAD skill files that change your side (all read, see S1.2)

1. BMAD "features" = PRD feature groups with FR ids (`bmad-prd`: "Features grouped; FRs nested"). GitHub epic = BMAD Epic N, feature sub-issue = PRD feature, user story = `Story N.M`.
2. `bmad-create-epics-and-stories` is interactive only (no headless mode), writes a fixed `{planning_artifacts}/epics.md`, and its step 1 initialises that file from a template with no mention of an existing file. Multi-release use needs a recipe (RELEASE-PLAN S3.5 R1).
3. `bmad-create-story` does implementation planning (architecture extraction, files to modify, previous-story and git intelligence). I propose we skip it and hand over the epics-file story plus a hand-off packet. Please say if `/sc:workflow` loses anything by this.
4. The BMAD ledger is `_bmad-output/implementation-artifacts/sprint-status.yaml` with status machine `backlog -> ready-for-dev -> in-progress -> review -> done` and a never-regress rule. `_bmad/` and `_bmad-output/` are in `.git/info/exclude` of this clone, so each Orca worktree would have its own copy: the ledger needs one home.
5. Precedent: issue 409 on origin/master holds a full BMAD chain under `.dev/issues/409/bmad/` and a hand-written hand-off `final-review/workflow-input.md` that ends in a `/sc:workflow` command line. Its review needed 63 blocking fixes, so a BMAD-only spec needs an independent review before IronClaude builds from it.

## My questions to you: RELEASE-PLAN.md S5.2 (11 questions), and what I need: S5.3 (N1 to N5).

## What I will do next
Finish the issue drafts (15 epics, about 60 feature sub-issues), then read your agent2/IRONCLAUDE-SIDE.md when it exists and answer your questions in 02-from-bmad-planner.md (Round 1).

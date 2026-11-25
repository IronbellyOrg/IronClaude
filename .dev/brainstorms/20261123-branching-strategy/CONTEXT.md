# Branching strategy for fast AI-driven release work: the use case (coordinator's facts, 2026-11-23)

Owner request (2026-11-23, in chat): "Branch name: use tavily to research branching strategies with fast-based AI workflows and come up with three proposals. Invoke the adversarial command, debate them all and refactor into a unified branching proposal that fits our use case here. [Another agent searches] the gfxai github repo for branching strategy documents that outline [a] decided upon approach; add that approach to the mix and validate if it is appropriate here."

## What the branching has to serve (facts, with sources)
- Repo: IronbellyOrg/IronClaude (a private fork). Default branch `master`. A long-lived `integration` branch also exists and the other maintainer (Clay) opens most pull requests into it (CLAUDE.md "Git Workflow": master (production) <- integration (testing) <- feature/*, fix/*, docs/*; 12 of the last 12 merged integration PRs were by that maintainer). Branches made by the owner's sessions are prefixed `ironbelly/` by Orca.
- The owner's model (2026-11-23): each dashboard release (1.1 ... 2.0) is an integration branch; each user story is a sub-branch of it; when the release is done the release branch merges to the default branch; then the next release. The owner wrote `dash1.3` for the release and `dash1.3/story1` for a story.
- Git cannot hold `dash1.3` and `dash1.3/story1` together (verified in a scratch repo 2026-11-23: "cannot lock ref 'refs/heads/dash1.3/story1': 'refs/heads/dash1.3' exists"). `dash1.3/release` plus `dash1.3/story-...` works.
- Work is done by AI sessions under a coordinator: one Orca worktree per story, each story run through spec panel, `/sc:workflow` plan, plan review panel, `/sc:implement`, then the coordinator merges the settled story into the release branch locally (the worker contract's feature-worktree and child-worktree rules: `~/.claude/WORKER-CONTRACT.md` lines around 92 and 233 to 237: a child is made with `worker-start --worktree new-child --base-branch <feature branch>`; the coordinator merges the child branch into the feature branch after the result is admitted; a merge conflict is stopped and reported, never resolved automatically).
- Parallelism: two stories at once for the first release; they must name disjoint paths; merges into the release branch are serialised by the coordinator.
- Pull requests: `/sc:pr-submit --monitor 3` is the only way PRs are opened; it must run in its own top-level session in the branch's worktree; it never rewrites a published branch; it takes `--base <branch>`; CI (`.github/workflows/test.yml`) runs only for pull requests and pushes into `master` and `integration`, so a pull request into a release branch gets no CI; two automatic reviewers (Augment, Codex) review PRs. Nothing is merged by an agent: the owner merges every pull request (one per release into master; story merges into the release branch are local coordinator actions, to be confirmed).
- `worker-start` has no `--branch` flag; exact branch names need `orca worktree create --branch <name> --base-branch <ref> --parent-worktree <selector> --agent claude`.
- Rules: no commit directly on master or main; never push to or open PRs on the upstream SuperClaude-Org repository; rebasing a branch that others branched from is not allowed by `/sc:pr-submit`; local-only `.dev/` records are committed on the release branch.
- A progress ledger (`sprint-status.yaml`, BMAD) is tracked on the release branch being executed, written only by the coordinator. BMAD planning of release n+1 would start from master after release n merges.
- Release numbers 1.1, 1.105, 1.2 ... 2.0 are dashboard release numbers, not package versions (the package is 6.1.0 on master).
- Scale: one owner and one other maintainer, several AI coordinators in parallel, bursts of 15 to 60 AI-made pull requests in a few days are normal here (the repository saw this in 2026-11).

## Questions the unified proposal must answer
1. Names: the release branch and story branch names (no ref conflict; sortable; carries the release number and story id; Orca prefixing).
2. Where story work merges and how (local merge by the coordinator, or pull requests into the release branch; merge commit, squash or rebase; who resolves conflicts; what protects against two AI stories colliding).
3. How the release branch stays current with master and `integration` (merge or rebase; before or after the first push; because `/sc:pr-submit` never rewrites a published branch).
4. How the release lands (one PR into master? via `integration`? CI and the two reviewers run once at that point; release size).
5. Feature flags or trunk-based alternatives for incomplete features, short-lived branches, and whether long-lived release branches are justified for AI-speed work.
6. Hotfixes and bug fixes during a release (the owner's list has 1.1 bug-fix releases and 1.105 test-only releases between feature releases).
7. Clean-up: when story and release branches and worktrees are deleted; what is kept as a record.
8. How it fits `integration` and Clay's habit of branching from `integration`.
9. Failure and rollback: a story that goes bad after merging into the release; a release that fails on master.

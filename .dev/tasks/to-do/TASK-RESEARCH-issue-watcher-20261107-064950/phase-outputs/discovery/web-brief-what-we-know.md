# What we already know from codebase (brief for the Phase 4 web agents, 2026-11-07)

Verified facts only (tags as in the research files; anything UNVERIFIED is listed in gaps-and-questions.md, not here):

1. `/sc:issue --claim <N>` never prompts, assigns the issue to `@me` (the `gh` login of the session that runs it), stops without writing when the issue is closed, a pull request, or assigned to someone else, edits its own marked comments on a re-run, and stops after writing `next-steps.md` (src/superclaude/commands/issue.md:15,79,83; skills/sc-issue-protocol/refs/claim.md:41-47,80) [CODE-VERIFIED].
2. The claim has no mutual exclusion: two logins racing for an unassigned issue can both pass the checks (derived from claim.md:41-47; not observed) [CODE-VERIFIED as code reading].
3. The claim reads the repo only from the `origin` remote and rejects an issue URL on another repo (scripts/origin_repo.py) [CODE-VERIFIED].
4. `/sc:issue` is on the never-as-worker list (core/WORKER-CONTRACT.md:23); a watcher must start an ordinary top-level session, e.g. `orca agent launch --agent claude --worktree path:<abs> --surface terminal --prompt "/sc:issue --claim <int>"` (research/01, section on launch) [CODE-VERIFIED from help text and README; live behavior UNVERIFIED].
5. The claim itself reads the issue title, body and comments later (claim.md Waves 1 and 4), so the integer-only rule protects only the launch prompt, not the session (research/03).
6. The repo's workflows trigger only on push, pull_request and workflow_dispatch; no `schedule:` or issue-event workflow exists (.github/workflows/*) [CODE-VERIFIED].
7. The fork `IronbellyOrg/IronClaude` is PUBLIC and has only the 9 default GitHub labels (live `gh` check 2026-11-07); no trigger or approval label exists [CODE-VERIFIED].
8. No Python `gh` wrapper exists under `src/superclaude`; the repo mocks `gh` in tests with PATH-stub executables (tests/pr_submit/test_conflict_e2e.py) [CODE-VERIFIED].
9. The `gh` token observed in this workspace lacks the `read:project` scope (`gh project list` failed), so Project and Status filters are not readable with it [CODE-VERIFIED observation, this host only].
10. Orca's default `--dangerously-skip-permissions` still applies to launched Claude sessions even when `CCSESSION_PERMISSIONS=default` (ccsession-tag/README.md:534; local Orca config) [CODE-VERIFIED].
11. Routing under a pull model: the claim stops on a different assignee and is idempotent for the same assignee, so the poller selects issues already assigned to its own login (candidate 1) or claims unassigned issues first-come with its own dispatch record (candidate 4); file 02 section 2c states the per-candidate rules.
12. Owner decisions (binding): option A (workspace-side poller, no listener/inbound port/registry), claim-only, integer-only prompt; IronbellyOrg/Coder#477 was filed assuming a push design and is unnecessary under A unless B or C is revisited.
13. Open and not to be assumed: where the 5-minute poller runs inside a Coder workspace and where its dispatch record lives (gap 9); whether a slash command runs as a launch prompt (gap 1); Project read permissions (gap 5); who counts as an approver and how "approved" is recorded (gaps 10, 14).

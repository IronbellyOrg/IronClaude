# PIPELINE-PROPOSAL: a reusable release pipeline, BMAD for planning and IronClaude for implementation (agent 1, bmad-planner)

STATUS: complete draft by agent 1 (2026-11-22), awaiting agent 2's dated review section at the end. Source: shared/CONSENSUS.md (signed by both agents, 2026-11-22) plus agent1/ and agent2/. Everything here is a PROPOSAL for the owner; nothing is built, filed or committed. UNVERIFIED items are marked.

## 1. The pipeline on one page

```
OWNER'S ROADMAP (issue 727)
   |
   |  EPIC-01 Release 2 prep (once, owner in the session)
   v
PROGRAM RUN (BMAD, attended):  project-context -> investigate -> research -> PRD(update) -> UX -> architecture(update)
                               (+ IronClaude deep brainstorm, attended)  -> SPEC -> independent review -> epics+stories (EPIC-01, 02)
                               -> readiness -> sprint planning -> sprint-status.yaml
   |
   |  per scheduled release (just in time), same shape every time
   v
RELEASE PLANNING (BMAD, attended, release worktree):  correct-course? -> PRD/arch update? -> epics+stories for THIS release
                               -> readiness -> sprint planning -> PACKET FOLDER per feature
   |
   |  hand-off gate H1 (IronClaude coordinator) + owner's go in chat
   v
IRONCLAUDE EXECUTION (coordinator, Mode C):  one feature worktree; per story in order:
        spec-panel -> workflow (plan) -> owner approves plan -> implement (person-run today) -> ledger read
        one PR per feature (/sc:pr-submit --monitor 3) -> /sc:closeout
   |
   |  write-back by the coordinator only
   v
LEDGER + GITHUB:  sprint-status.yaml, story record, progress comment, issue closure
   |
   v
RETROSPECTIVE (BMAD) -> action items -> next release's inputs
```

Division in one line each: BMAD owns what and why (documents, epics, stories, acceptance criteria, order, ledger values, retrospectives, change proposals). IronClaude owns how and when (design only when asked, tasklist, code, tests, review, PR, CI, closeout, retries). Only a spec defect goes back to BMAD, as a Spec Gap Report into `/bmad-correct-course`. IronClaude never contradicts an architecture `AD-n`.

## 2. Who does what

| Actor | Opened by | Does | Never does |
|---|---|---|---|
| Owner | n/a | schedules releases, says go per epic or feature, approves plans, gives Rulings, answers O1 to O7 | n/a |
| BMAD planning session (attended; John, Winston, Sally, Mary, Paige personas available) | owner or a developer, in the release worktree | every `/bmad-*` skill; builds packet folders by hand in v0 | is dispatched, messaged or typed into by the coordinator |
| Release coordinator (one session per release, Orca Run) | owner | H1 intake, story issues, Tasks and briefs, `/sc:sweep`, write-back, progress comments, `/sc:closeout`, each outward action only on the owner's instruction; reads the result of `/sc:pr-submit`, which runs in a separate top-level session opened in the feature worktree | answers a BMAD menu; lets a worker push, comment or commit; runs `/sc:pr-submit --monitor` itself (it would stop its wait loop) |
| Story workers (one per Task, `--unattended`) | coordinator via `worker-start` | `/sc:spec-panel`, `/sc:workflow`; alternate arm `/sc:brainstorm` and `/sc:adversarial` | commit, push, comment, create worktrees |
| Implement session | a person (pilot) or a worker after `/sc:implement` gets an unattended mode | `/sc:implement <plan path>` in the feature worktree | commit, push, open a PR |
## 3. Steps, commands, outputs, where files live

`<D>` = a per-story run folder, proposed `.dev/stories/<N-M>/`, one subfolder per Task. IronClaude flags below were read by agent 2 in the command files (IRONCLAUDE-SIDE.md section 10); BMAD skill names and catalog args were read by agent 1. Not run by either agent.

### 3.1 Program run (EPIC-01, once)

| # | Step | Who | Command | Output |
|---|---|---|---|---|
| P1 | project context | BMAD session | `/bmad-generate-project-context` | `_bmad-output/project-context.md` (points to CLAUDE.md) |
| P2 | evaluate current dashboard | BMAD session + owner use | `/bmad-investigate` | case file in `_bmad-output/implementation-artifacts/` |
| P3 | research requirements, similar projects, storage | BMAD session | `/bmad-market-research`, `/bmad-technical-research` | `_bmad-output/planning-artifacts/research/` |
| P4 | pressure-test the two-way idea | BMAD session | `/bmad-forge-idea` | optional `forged-idea.md` |
| P5 | PRD (Update of 409 PRD) | BMAD session | `/bmad-prd` | `prd.md`, `addendum.md`, `.memlog.md` |
| P6 | UX | BMAD session | `/bmad-ux` | `DESIGN.md`, `EXPERIENCE.md` |
| P7 | deep brainstorm on storage, Postgres per project, history (owner's deliverable 1); run from the worktree that holds `.dev/issues/727/issue-body.md` (untracked, a new worktree lacks it) or copy it in first | person's own session | `/sc:brainstorm "<topic> @.dev/issues/727/issue-body.md" --depth deep --research deep --codebase --blind --output <dir>` | brainstorm package (input to P8) |
| P8 | architecture (Update; `AD` ids stable) | BMAD session | `/bmad-architecture` | `ARCHITECTURE-SPINE.md` |
| P9 | SPEC | BMAD session | `/bmad-spec` | `SPEC.md` + companions |
| P10 | independent review | worker or person | `/sc:spec-panel @<SPEC.md> --mode critique ...` (first on one file); optional `/bmad-review-adversarial-general <path>`, `/bmad-review-edge-case-hunter <path>` | review reports |
| P11 | epics and stories (EPIC-01, EPIC-02); try the multi-release recipe | BMAD session | `/bmad-create-epics-and-stories` | epics file(s) |
| P12 | readiness gate | BMAD session | `/bmad-check-implementation-readiness` | readiness report |
| P13 | ledger | BMAD session | `/bmad-sprint-planning` | `sprint-status.yaml` |
| P14 | review of the release list (owner's deliverable 1) and the owner's record of scheduled releases | BMAD session + owner | `/bmad-editorial-review-structure <path>` optional | written review; owner's chat record |

### 3.2 Per release (just in time; the same shape for every epic)

| # | Step | Who | Command | Output |
|---|---|---|---|---|
| R1 | orient | person | `/bmad-help` | next step |
| R2 | absorb change | BMAD session | `/bmad-correct-course` if scope moved; `/bmad-prd` or `/bmad-architecture` (Update) if needed | change proposal; updated documents |
| R3 | epic and stories for THIS release; criteria ids `S<N>.<M>-AC<n>`; complexity class and paths per story | BMAD session | `/bmad-create-epics-and-stories` | epic file `epics/epic-NN-<release>.md` (recipe, trial) |
| R4 | gate | BMAD session | `/bmad-check-implementation-readiness` | readiness report |
| R5 | ledger | BMAD session | `/bmad-sprint-planning` | `sprint-status.yaml` refreshed |
| R6 | packet folder per feature | BMAD-side person (by hand, v0) | templates `agent1/templates/handoff-packet.md` (v2) | `.dev/issues/<feature-issue>/bmad/INDEX.md` + `story-<N>-<M>-<slug>.md` |
| R7 | intake check H1, then owner's go | IronClaude coordinator + owner | checklist H1.1 to H1.9 (IRONCLAUDE-SIDE.md 3.2) | INDEX.md `status: accepted` or `rejected: <row>` |
| R8 | file story issues and link them | coordinator, on the owner's instruction | `/sc:issue --create @<description> --mode feature --type <area> --depth <quick|standard|deep by complexity>`; then `gh issue edit <story> --parent <feature issue>` (and `--add-blocked-by <earlier story>` for order; flags read in `gh issue edit --help` by agent 2, not run; REST `sub_issues` is a fallback only) | story issues |
| R9 | feature worktree and first Task | coordinator | Orca `worker-start --worktree new-child --base-branch origin/master --setup skip --agent claude --spec <brief>` (all Orca; never raw `git worktree add`); every later Task of that feature: `worker-start --worktree path:<that worktree> --agent claude --spec <brief>` with no creation flags (creation flags are rejected for existing worktrees; agent 2's review C3). UNVERIFIED: whether `new-child` with `--base-branch origin/master` really bases on master and not on the coordinator's branch; if not, O4 option 2 needs another way to create the worktree. Packet folder copied in with `diff -r` proof | feature worktree |
| R10 | per story: spec review | story worker | `/sc:spec-panel @<story file> --mode critique --focus requirements,testing,correctness --unattended --report-dir <D>/panel` | panel report |
| R10a | only on a trigger (S1 to S4): code-grounded spec | story workers | `/sc:brainstorm "..." --codebase --blind --depth quick --proposals 2 --research none --unattended --output <D>/bs`, then `/sc:adversarial --compare <story file>,<D>/bs/merged-requirements.md --depth quick --focus correctness,architecture --unattended --output <D>/adv` | merged spec (an input, never the spec) |
| R11 | per story: plan | story worker | `/sc:workflow <story file> --depth <quick|standard> --handoff none --unattended --report-dir <D>/wf` | `.dev/tasks/to-do/TASK-WF-<subject>-<YYYYMMDD>-<HHMMSS>/` package |
| R12 | plan approval | owner in chat | policy O3 | recorded in run notes |
| R13 | per story: build | person today (worker after B4) | `/sc:implement <plan path>` | ledger `progress.md`; package to `.dev/tasks/done/` |
| R14 | coordinator reads ledger, local commit, write-back, next story | coordinator | explicit paths plus `.dev/tasks`; status sync (B6) | ledger, story record, progress comment |
| R15 | after the last story: PR | a top-level session opened in the FEATURE worktree (by the owner; the coordinator does not run it: `/sc:pr-submit` STOPs with `pr_head_mismatch` unless the checkout is the PR head, and `--monitor` is an attended loop that would stop the coordinator's wait and sweep loop; agent 2's review C2) | pre-PR checks (`git remote get-url origin` is `IronbellyOrg/IronClaude`; `git fetch origin`, rebase on `origin/master`), then `/sc:pr-submit --monitor 3 --head <feature branch> --title "<title>" --body "<body>"`; the returned PR URL must point at `IronbellyOrg/IronClaude`. The coordinator reads the result and does the write-back. UNVERIFIED: whether a coordinator may open such a session itself | one PR per feature on the fork |
| R16 | after merge | coordinator | `/sc:closeout <PR> --issue <N>` | issue settled |
| R17 | epic end | BMAD session | `/bmad-sprint-status` (data mode), `/bmad-retrospective` | retrospective, action items |

How a Task is made (agent 2's review C4, C5): each Task's brief follows `~/.claude/WORKER-CONTRACT.md` section 5 (guard line, chain line, blocked-gate line, `Local commit: not authorized`, a unique report directory, worktree, `Outward actions: none`, one `Command:` line; detail in IRONCLAUDE-SIDE.md section 10); before the first Task for a command, the two-copy test (the installed command file and the worktree copy both carry `## Unattended mode`; `/sc:implement` does not); `--unattended` on `/sc:spec-panel` rests on the owner's instruction naming it, recorded in the run notes; each Task is created only after its predecessor settled and its contract was read, so the plan path for R13 is the `report_path` of the workflow contract; a plan is implemented only in the checkout where it was written (`E-MANAGED-INVALID` otherwise), so R10 to R13 of one story share the feature worktree and a plan is never copied between worktrees.

Halts: a halt of `/sc:implement` freezes the story until the owner's Ruling in chat; a spec defect becomes a Spec Gap Report (file next to the packet) and the story waits for `/bmad-correct-course`.

### 3.3 Where files live

| Kind | Path | Tracked? |
|---|---|---|
| BMAD working output, ledger, epics | `_bmad-output/{planning,implementation}-artifacts/` in the release worktree | untracked per clone today; owner decision O2 recommends tracking |
| BMAD team overrides | `_bmad/custom/<skill>.toml` | untracked today (O2); `*.user.toml` ignored by `_bmad/custom/.gitignore` |
| Copies of BMAD sets for audit (house precedent) | `.dev/issues/<N>/bmad/<artifact>-<slug>/` | tracked on master for 409 |
| Packet folder per feature | `.dev/issues/<feature-issue>/bmad/` | O2 |
| Plan packages and ledgers | `.dev/tasks/to-do/` then `.dev/tasks/done/` | always staged (repo rule) |
| Per-story run folders and run notes | `.dev/stories/<N-M>/` (proposal) | proposal |
| Brainstorm packages | `.dev/brainstorms/<date>-<topic>/` | by house habit |
| Issue drafts and templates from this planning | `.dev/brainstorms/20261122-release-pipeline-bmad-ironclaude/agent1/` | draft |
## 4. GitHub objects, status mapping, write-back

| Object | Source | Filed | How | Closed |
|---|---|---|---|---|
| Epic (one per release) | `agent1/issue-drafts/EPIC-NN-*.md` (15) | when the owner schedules that release (EPIC-01 first) | `gh issue create --repo IronbellyOrg/IronClaude --title ... --body-file <draft body below the --- line> --parent 727 --type Feature` (flags read in `--help`, not run) | by the coordinator after the retrospective, with a comment linking it |
| Feature sub-issue | `EPIC-NN-STORY-MM-*.md` (73) | with its epic | same, `--parent <epic number>`; `--blocked-by` for dependency order | with its last story |
| Story issue | `agent1/templates/story-issue-description.md` | at hand-off | `/sc:issue --create @<file> --mode feature --type <area> --depth <by complexity>`, then `gh issue edit <story> --parent <feature issue>` (read in help, not run; REST `sub_issues` fallback) | by `/sc:closeout` when its acceptance rows pass |

Labels: only `enhancement`, `bug`, `documentation`, `question` exist; `epic` and `release:<version>` in the drafts are (new) and optional. A milestone per dashboard release is a candidate home for "1.1" (owner's call, nothing records a dashboard release number today).

Status mapping, written only by the coordinator, never regressing a status (rules copied from `bmad-quick-dev/sync-sprint-status.md`):

| Event | `sprint-status.yaml` | GitHub | BMAD story record |
|---|---|---|---|
| packet accepted | story `ready-for-dev` (means "packet accepted") | progress comment opened on the story issue | none |
| first implement task started | story `in-progress`; epic lifts from `backlog` | comment edited | none |
| story implemented and reviewed | none | comment edited with files from the ledger | coordinator writes `{implementation_artifacts}/<story_key>.md` from `agent1/templates/story-record.md` |
| halt or spec defect | none (story frozen) | comment names the STOP code | none |
| PR opened | `review` | comment with PR link | Status updated |
| PR merged, closeout done | `done` | story issue closed; feature comment | Status updated |
| all stories done | epic `done` | feature then epic closed in order | none; `/bmad-retrospective` next |

GitHub's own sub-issue counter (`sub_issues_summary`) gives the roll-up bar on the feature and the epic; no second counter is built. Every GitHub write and commit needs the owner's instruction naming it (standing instruction O6).
## 5. What exists, what to build, trial plan, owner decisions, risks

**Exists, reuse.** All `bmad-*` skills (BMAD 6.9.0) and personas; `bmad-customize`; the 409 worked example on master; `/sc:spec-panel`, `/sc:brainstorm`, `/sc:adversarial`, `/sc:workflow`, `/sc:implement`, `/sc:pr-submit`, `/sc:closeout`, `/sc:sweep`, `/sc:issue`; WORKER-CONTRACT and the Orca machinery; from this planning: 15 epic drafts, 73 feature drafts and their generator (`agent1/tools/`), `agent1/templates/handoff-packet.md` (v2), `story-issue-description.md`, `story-record.md`; agent 2's notes (`agent2/IRONCLAUDE-SIDE.md`, `agent2/recommend/`, `agent2/brainstorm-b/`).

**Build (priority P0 = pilot, P1 = trial release, P2 = later; full lists: CONSENSUS (g) items A1 to A10 and IRONCLAUDE-SIDE 9.2 items B1 to B11).** P0: `project-context.md`; the `_bmad/custom/bmad-create-epics-and-stories.toml` facts (criteria ids, complexity, paths, epic number); the multi-release epics recipe trial; H1 checklist; run-notes template; Spec Gap Report template. P1: `/sc:implement` unattended mode (B4; the one item that decides whether execution is unattended); progress comment template and renderer; status sync script and story record writer; coordinator duties text (no new `/sc:` command). P2: story rows in the worker brief so the watcher can drive stories; packet builder; observer view of per-story progress. Not built: a new hand-off command, a spec-review agent, a second issue filer, a release-planner agent.

**Trial plan (the owner's "trial and error").** (1) EPIC-01 feature 7 runs `/bmad-create-epics-and-stories` for EPIC-01 and EPIC-02 and tests the multi-release recipe. (2) Plan-only pilot on issue 706 item 6 (scale tests; paths named, no open owner decision): a person writes the story in BMAD form, builds the story file, the coordinator runs H1, `/sc:spec-panel`, `/sc:workflow`, then reads the plan and stops before implement; record whether story and criteria ids survive into the plan's task criteria (UNVERIFIED), calls and minutes per step, anything lost. (3) Second pilot adds a person-run `/sc:implement`, the write-back and the story record. (4) First trial release, 2 features at once, measuring per story: path taken, triggers fired, calls and minutes, conflicts missed by the default arm, criteria lost, halts. Thresholds in the trigger list are guesses until step 4; the trigger list is frozen during a trial release.

**Owner decisions pending (both agents recommend the same option; nothing is decided until the owner says so in chat).** O1 Mode C (coordinator-written briefs) rather than waiting for the watcher flow. O2 track `_bmad-output/` and `_bmad/custom/*.toml` in git (remove the two `.git/info/exclude` lines; they cover all worktrees of a clone) and keep the packet under `.dev/issues/<feature>/bmad/`. O3 plan approval for every medium and complex story plus the first story of each feature. O4 one PR per feature from worktrees based on `origin/master` (an exception to the contract's "children merge back"). O5 build `/sc:implement` unattended mode first. O6 a standing instruction per release naming each routine write. O7 two features at once for the first release.

**Risks and UNVERIFIED items.**
- `bmad-create-epics-and-stories` may overwrite `epics.md` on a second run (its step 1 initialises from the template; not tested). Recipe in the trial.
- Whether a `persistent_facts` line makes BMAD number criteria `S<N>.<M>-AC<n>` and add complexity and paths (not tested). Fallback: the person builds them into the story file.
- Whether `/sc:workflow` keeps story and criteria ids in its tasks (not tested).
- BMAD planning is attended only (no headless for epics and stories or forge). A headless BMAD worker is a later experiment and needs a contract extension.
- Until B4, execution past the plan is person-run: the pipeline is not fully unattended.
- Where "1.1" of the dashboard is recorded: nowhere found; `pyproject.toml` says 5.0.0 and `VERSION` here says 3.7. Candidate: a GitHub milestone per release.
- Observer code is on `origin/master`, not on this working branch: feature worktrees must base on `origin/master`.
- `bmad-document-project` writes to `docs/`; not used in this plan.
- Some drafts name things not known yet: Clay's HTML dashboards (location), the Coder canvas button mechanism and the repository it lives in, the delivery channel from the dashboard to a coordinator session. Each draft says "Not known yet" and plans research first.
- No GitHub write, commit or worktree was made by either planning agent; `gh issue create --parent`, REST `sub_issues`, and the `/sc:` command lines were read, not run.

## 6. Reuse for the next release or another project

1. Release cycle: keep the shapes (prep, validation cycle, tests cycle, decision review, build release). To make the next release's drafts, change the data in `agent1/tools/plan_unique.py` (hand-written epics) or the parameters of the two cycle templates in `plan_cycles.py` (version, build under test, owner's item, bug source) and run `uv run python agent1/tools/render.py`; it rewrites `issue-drafts/` and its README (idempotent, writes only there).
2. Another project: copy the templates (`agent1/templates/`) and the generator (`agent1/tools/`); replace `plan_common.py` links (repo, roadmap issue, code paths, CI files), the labels and the repo name in the filing lines. The BMAD side needs `_bmad/` installed (`setup-bmad` skill exists; not read) and a `project-context.md`.
3. The pipeline's contract is five files: INDEX.md, story files, story-issue descriptions, the story record, the Spec Gap Report. Everything else is existing commands.

## Review by agent 2 against IronClaude's real rules (dated section, written by ic-planner)

Dated 2026-11-22, ic-planner. Method: I read sections 1 to 6 whole and checked each IronClaude statement and command line against the files: `~/.claude/WORKER-CONTRACT.md`, `~/.claude/HOW-WE-WORK.md`, the command files of spec-panel, workflow, brainstorm, adversarial, implement, issue and pr-submit (usage and required input), and read-only `--help` output of `gh issue create`, `gh issue edit` and `orca orchestration worker-start`. I ran none of the commands. Verdict: the proposal is consistent with the signed CONSENSUS.md; I found two corrections that change text in sections 3.2, 4 and 2 (C1, C2), three that complete it (C3 to C5), and three minor ones. Where this section contradicts sections 1 to 6 on these points, this section prevails until agent 1 folds the changes in.

**Corrections**

- **C1 (3.2 R8 and section 4, story issue row): link a story with `gh issue edit`, not the REST call.** `gh issue edit --help` lists `--parent <number or URL>` ("Set the parent issue"), `--add-blocked-by`, `--type`, `--milestone`. So after `/sc:issue --create` files a story (which has no parent option), the link is `gh issue edit <story> --parent <feature issue>`, and story order is `--add-blocked-by <earlier story>`. The REST `sub_issues` call is then a fallback only. Flags read in help, not run.
- **C2 (section 1 diagram, section 2 coordinator row, 3.2 R15): `/sc:pr-submit` does not run in the coordinator's own session.** Two read facts. (a) `pr-submit.md` STOPs with `pr_head_mismatch` unless the checkout is the PR's head branch and commit, so the session must be opened in the feature worktree, while the coordinator runs in the release worktree. (b) With `--monitor >= 1` it is "an attended in-session loop, not a daemon" (HOW-WE-WORK 3.11), so running it inside the coordinator would stop the coordinator's wait and `/sc:sweep` loop (WC-16). So R15 is: a top-level session opened in the feature worktree (by the owner; at Full Submit level a launched agent does it, but that level is gated) runs `/sc:pr-submit --monitor 3 --head <feature branch> --title "<title>" --body "<body>"` (creation needs the head, title and body; usage in `pr-submit.md`), after the repo's pre-PR checks: `git remote get-url origin` is `IronbellyOrg/IronClaude`, `git fetch origin` then rebase on `origin/master`, and the returned PR URL must point at `IronbellyOrg/IronClaude` (project CLAUDE.md, "PR Target = Fork"). The coordinator then reads the result and does write-back. UNVERIFIED: whether a coordinator may open such a session itself; the contract does not say.
- **C3 (3.2 R9): the worker-start line is incomplete and one assumption is unchecked.** `worker-start --help` shows `--agent <id>` (or `--terminal`) is required, `--spec <text>` carries the brief, and the creation flags (`--name`, `--repo`, `--base-branch`, `--setup`) are "rejected for current/existing worktrees". So the first Task of a feature is `worker-start --worktree new-child --base-branch origin/master --setup skip --agent claude --spec <brief>`, and every later Task of that feature is `worker-start --worktree path:<that worktree> --agent claude --spec <brief>` with no creation flags. Not verified: whether `new-child` with `--base-branch origin/master` yields a worktree based on master rather than on the coordinator's branch. If it bases on the coordinator's branch, O4 option 2 needs another way to create the worktree (the contract's default is children based on the feature branch and merged back).
- **C4 (3.2 R10 to R13): the proposal omits how a Task is made, which the contract requires.** Add: (i) each Task's brief follows `WORKER-CONTRACT.md` section 5 (guard line, chain line, blocked-gate line, `Local commit: not authorized`, a unique report directory, worktree, `Outward actions: none`, one `Command:` line); (ii) before the first Task for a command, the two-copy test (read `~/.claude/commands/sc/<name>.md` and the worktree copy for the line `## Unattended mode`; the installed copies of spec-panel, workflow, brainstorm and adversarial have it, implement does not); (iii) `--unattended` on `/sc:spec-panel` rests on the owner's instruction naming it (a P2 command), recorded in the run notes; (iv) each Task is created only after its predecessor settled and its contract was read, so the plan path for R13 is the `report_path` of the workflow contract. Detail: IRONCLAUDE-SIDE.md section 10.
- **C5 (3.2 R13): a plan is implemented in the checkout where it was written.** A managed plan copied or taken from another checkout is refused (`E-MANAGED-INVALID`), so R10 to R13 of one story must share the feature worktree, and a plan is never copied between worktrees. A halted `/sc:implement` freezes the story under the contract's "After an `/sc:implement` stop" rules; that is the meaning of the Halts line below the table.

**Minor**

- **M1 (3.1 P7):** the command names `@.dev/issues/727/issue-body.md`, which is untracked in this checkout; a different worktree will not contain it. Run P7 from the worktree that holds it, or copy it in first.
- **M2 (section 4, epic row):** `--type Feature` assumes that issue type exists in the organisation; the issue skill assumes it (`refs/labels.md` lists Feature, Bug, Test) but I did not verify the list on GitHub.
- **M3 (3.3):** `.dev/stories/<N-M>/` is a proposal; nothing in the files I read forbids it (a report directory only must not sit inside `.git/`, `.codegraph/` or the `.claude/` skill, agent and command folders), but whether it is tracked is undecided. Per-Task report folders under it need no extra rule.

**Checked and consistent with the files (no change):** the flags on the spec-panel, workflow, brainstorm and adversarial lines (R10, R10a, R11, P7) against their option tables and Unattended mode sections, including `--output` versus `--report-dir`; the `/sc:issue --create` line (`--mode feature`, `--type <area>`, `--depth` mapped to Complexity); `/sc:closeout <PR> --issue <N>`; the triggers S1 to S4 and the merge rules as in CONSENSUS (b); the status mapping and write-back rules as in CONSENSUS (c); the one-PR-per-feature choice as owner decision O4; the O1 to O7 text in section 5 (matches CONSENSUS "Owner decisions pending"); the statement that execution past the plan is person-run until `/sc:implement` has an unattended mode (no `unattended` text in its command file or skill, also on master).

**Not verified by me, as listed in section 5:** whether `/sc:workflow` keeps story and criteria ids; whether a `persistent_facts` line makes BMAD number criteria; how `/sc:spec-panel` takes a folder; whether the phase 2 live check of `--unattended` passed; whether the launch-level ship gate opened; the shape of GitHub issue types in the organisation. No command in this proposal was run by either agent.

# IRONCLAUDE-SIDE (agent 2, ic-planner): the IronClaude half of the BMAD to IronClaude release pipeline

STATUS: Round 0 text complete (sections 1 to 11), 2026-11-22. Positions are agent 2's opening positions for the debate, not consensus. Anything not read in a file or command output is marked UNVERIFIED. Companion files: `agent2/recommend/` (the `/sc:recommend` result), `agent2/brainstorm-b/` (the brainstorm on topic b) and `agent2/brainstorm-b-topic.md` (its input).

## 1. Scope, sources, how this was made
What I did, in order:

1. Read OWNER-INSTRUCTIONS.md, PROTOCOL.md and the roadmap in issue 727 (`.dev/issues/727/issue-body.md`).
2. Ran `/sc:recommend` through its Skill with `--unattended --report-dir agent2/recommend/`. Result: `agent2/recommend/recommendation.md` and `return-contract.yaml`. Outcome: no routing row of `~/.claude/HOW-WE-WORK.md` fits the whole goal (each covers one step), so it returned a multi-path result built from verified commands.
3. Read the real sources (list in section 2): the guide, `~/.claude/WORKER-CONTRACT.md` in full, the command files of brainstorm, adversarial, spec-panel (first 150 lines), workflow, implement and issue, the implement and workflow protocol files named there, the issue protocol `refs/claim.md` and `refs/chains.md`, and on origin/master (read with `git show`, nothing checked out) `docs/user-guide/orchestrator-mode.md`, `docs/user-guide/observer.md`, `docs/designs/issue-watcher-status-pipelines.md` and the `issue_pipeline` CLI.
4. Ran `/sc:brainstorm` (topic b, quick depth, 2 proposals, `--unattended`) through a delegated agent: `agent2/brainstorm-b/` (input: `agent2/brainstorm-b-topic.md`). Its internal adversarial step ran (convergence 0.654 against 0.75, so flagged "not fully converged"; the orchestrator of that run adjudicated nine open points). I read the result and use it in section 4, with changes I state there. Deviations of that run, as it reported them: the Socratic questions were answered from the topic file; the codebase scan used the auggie search tool and direct reads, not `/sc:analyze`; the merge ran inline, not through the `merge-executor` agent; the token hard-kill was not enforced (about 671K tokens for 5 calls against an estimate of about 208K).
5. I did NOT run `/sc:adversarial --compare` as a separate step: the brainstorm's own debate is the adversarial step, and the two specs to merge (a BMAD story spec and an IronClaude spec) do not exist yet. It is part of the pipeline designed here (section 10), not something to run in planning.
6. I did NOT run `/sc:spec-panel`, `/sc:workflow` or `/sc:implement` (no spec exists to run them on, and workflow and implement write outside this folder). Their behaviour here comes from reading their files.

Limits kept: no GitHub writes (only read-only `gh` calls with `--repo IronbellyOrg/IronClaude`), no git writes, no `orca` write calls, nothing written outside this folder.

## 2. Facts read that shape the design
Each row was read in the file named; "master" means read with `git show origin/master:<path>` (this working branch is behind master: it still has the `sprint`, `roadmap` and `tasklist` CLI folders that master no longer lists).

| # | Fact | Source |
|---|---|---|
| F1 | `/sc:brainstorm "<topic or @file>"` accepts `--depth`, `--proposals`, `--blind`, `--codebase`, `--research`, `--handoff none\|design`, `--output DIR`, `--unattended --report-dir DIR`. Under `--unattended` it skips Socratic questions, refuses `--interactive`, skips deep research, nests adversarial under the output folder. It writes requirements only (`merged-requirements.md`). | `~/.claude/commands/sc/brainstorm.md` |
| F2 | `/sc:adversarial --compare a.md,b.md` takes 2 to 10 files, `--depth`, `--focus`, `--convergence`, `--blind`, `--output`. Under `--unattended` it needs exactly one of `--output` or `--report-dir` and refuses `--interactive`. | `~/.claude/commands/sc/adversarial.md` |
| F3 | `/sc:spec-panel @file --mode critique --focus requirements,architecture,testing,compliance,correctness [--unattended --report-dir DIR] [--target-release R]`. Findings CRITICAL, MAJOR, MINOR. | `~/.claude/commands/sc/spec-panel.md` |
| F4 | `/sc:workflow <file or prompt> --depth quick\|standard\|deep --handoff none --unattended --report-dir DIR` writes a package `.dev/tasks/to-do/TASK-WF-<subject>-<YYYYMMDD>-<HHMMSS>/` with the plan `<id>.md`, a byte-exact `source.md` snapshot of the one source and `return-contract.yaml`, then runs an advisory `/sc:reflect --mode pre`. Under `--unattended` it skips `--handoff implement`. | `workflow.md`, `sc-workflow-protocol/refs/input-parse.md` |
| F5 | `/sc:implement <plan path>`: per-task spec-compliance QA, ledger `progress.md` with lines like `T<id>: complete verdict=compliant ... files=...`, a final independent review (`FINAL: pass\|issues`), archive to `.dev/tasks/done/`. A managed plan must resolve to `<this checkout>/.dev/tasks/to-do/<slug>/<slug>.md`; a copied plan or one from another checkout is refused (`E-MANAGED-INVALID`). A halt for a Ruling needs the person's own chat confirmation. It never commits, pushes or opens a PR. | `implement.md`, `sc-implement-protocol/SKILL.md`, `refs/managed-workspace.md`, `refs/ledger.md` |
| F6 | `/sc:implement` has NO `## Unattended mode` section (command file and skill: zero matches for "unattended"; same on master). Workers that run it write no `return-contract.yaml`. | grep of `~/.claude/commands/sc/`, of `sc-implement-protocol/`, and `git show origin/master:src/superclaude/commands/implement.md` |
| F7 | Unattended mode exists for 30 command files; the P1 default set is 13 commands (adversarial, brainstorm, cleanup-audit, graph, impact, init-lite, workflow, analyze, business-panel, design, document, explain, test); the 10 P2 commands (including spec-panel, recommend, research, troubleshoot, reflect) get the flag when the user's instruction names them or after a phase 2 live check. UNVERIFIED whether that check passed. | `WORKER-CONTRACT.md` section 5; grep |
| F8 | Coordinator rules: person-opened session; one Orca Task per unit, one worker per Task; a Task's brief cannot change (every retry is a new Task); workers never push, PR, comment or commit (a local commit only by grant); the coordinator does every outward action, only when the owner's instruction names it; PRs only via `/sc:pr-submit --monitor 3` in a top-level session; Orca creates worktrees; a worker that edits project files (implement) gets its own child worktree; children merge back into the feature branch; `/sc:sweep` on every wake; person-opened sessions are observed, never messaged. | `WORKER-CONTRACT.md` sections 2 to 4 |
| F9 | Issue pipeline (`superclaude issue-watch`, `superclaude issue-pipeline`, `/sc:issue --claim N --pipeline none\|worktree\|full [--submit] --stage research\|spec\|plan\|debug`): acts only when the Project item Status is Research, Spec, Plan or Debug and the `Approved` field is Yes; at level `none` the coordinator's worker runs the stage command (research, design or brainstorm then design, workflow, troubleshoot) and every stage ends at `In review`; no stage runs `/sc:implement`; the worker brief is a closed template with one row per Status; `issue-pipeline complete` posts one result comment per run and moves Status only on `succeeded`. Levels `worktree`, `full`, `full submit` are gated (ship gate, `GOVERNED_LEVELS_ALLOWED`); UNVERIFIED whether the gate has opened since the design note of 2026-11-19. | master `docs/designs/issue-watcher-status-pipelines.md`, `src/superclaude/cli/issue_pipeline/cli.py`, `templates/worker-brief.txt`; `~/.claude/skills/sc-issue-protocol/refs/claim.md` |
| F10 | `/sc:issue --claim` already does an accuracy check of an issue against today's code (`current` or `out_of_date`), writes `issue-summary.md` (type, complexity by hours rubric: simple up to 4 h in one area, medium over 4 up to 16 h, complex over 16 h or more than one subsystem or security or data migration; a `spec-route` line) and a next-steps chain per type and complexity (simple: workflow, implement; medium: brainstorm `--blind`, design, workflow, implement; complex: brainstorm `--depth deep --research deep --codebase --blind`, design, workflow `--depth deep`, implement). | `refs/claim.md`, `refs/chains.md` |
| F11 | `/sc:issue --create` makes a templated issue with a GitHub issue type, the Complexity field and a mode label; I found no sub-issue or parent linking in the issue skill (grep for "sub-issue", "parent": no match). Agent 1 read that the API returns `sub_issues_summary`. | `issue.md`, grep of `sc-issue-protocol/` |
| F12 | `/sc:closeout <PR>` settles a merged PR: decides if the issue is done (reads its criteria), closes it or leaves a note of what remains, settles the work report entry and the worker's Orca task. It does not touch BMAD (grep of its skill: no "bmad", no "sprint-status"). | `docs/user-guide/orchestrator-mode.md` (master), grep |
| F13 | `/sc:sweep` reads Orca, `git status` per worktree, session transcripts and the `return-contract.yaml` and `progress.md` files of the sessions it finds; one dated report under `.dev/sweeps/` plus JSON on stdout; person-started sessions appear as `person session (active)`. Several counts are not yet observed (stalled, fenced, working). | master `docs/user-guide/orchestrator-mode.md` |
| F14 | The observer dashboard is read-only: it never approves, retries, dispatches or messages; questions are answered in the coordinator's terminal. | master `docs/user-guide/observer.md`, `orchestrator-mode.md`; issue 727 |
| F15 | BMAD is installed here as project skills (`.claude/skills/bmad-*`, BMAD 6.9.0 per agent 1) with output in `_bmad-output/{planning,implementation}-artifacts`; both `_bmad/` and `_bmad-output/` are in `.git/info/exclude` (a per-clone file), so they are untracked here. `bmad-create-story` writes `<story_key>.md` (Story, Acceptance Criteria, Tasks / Subtasks with `(AC: #)`, Dev Notes, Dev Agent Record), sets `ready-for-dev`, updates `sprint-status.yaml` (`backlog, ready-for-dev, in-progress, review, done`); the next story's creation reads the previous story's Dev Agent Record. | `.claude/skills/bmad-create-story/SKILL.md`, `template.md`; `_bmad/config.toml`; `sprint-status-template.yaml`; agent 1 RELEASE-PLAN S1.2 |
| F16 | IronClaude code has no BMAD integration: `git grep -il bmad origin/master -- src docs` finds only the cleanup-audit exclusion of BMAD paths, the HOW-WE-WORK guide, the observer commands and one design note (`docs/designs/prd-spec-flag.md`). | grep on master |
| F17 | Related open issues (read-only `gh issue list/view`): #689 (move planning to `/sc:issue --create`, claim goes straight to workflow and implement), #721 (claim should estimate time and complexity accurately), #725 (coordinators ask the peer coordinator before a human), #339 (orchestrator to run all sessions in a worktree), #726 (vote on interventions), #409 and #706 (dashboard). | `gh issue list/view --repo IronbellyOrg/IronClaude` |

## 3. Hand-off (topic a): when a story goes to IronClaude, and the contract
**Position 3.1: one packet folder per feature, one self-contained story file per story; IronClaude plans and runs per story, and opens one PR per feature.**

Where I agree with agent 1 (RELEASE-PLAN S3.2, S3.3, S5.1 a): the unit BMAD hands over is a feature (a group of 2 to 6 ready stories); BMAD does not run `bmad-create-story`, `bmad-dev-story` or `bmad-code-review` for these stories; a hand-off packet carries the stories verbatim, the binding documents by role, the `AD-n` ids that bind, the constraints and the write-back keys.

Where I change it, with the file fact behind each change:

1. **The story, not the feature, is the unit of one `/sc:workflow` run and of one plan package.** `/sc:workflow` takes exactly one source and writes one package from it, and the package keeps a byte-exact copy of that one source (`input-parse.md`, "Package contents"). `/sc:implement` then walks that plan with one ledger. Per story gives: a ledger per story (write-back is a direct read of one `progress.md`, no mapping from tasks back to stories); failure isolation (a halted story does not stall its siblings' plans); and the BMAD rule that a story is completable by one dev agent (agent 1, S1.2 point 1). A batch run would need every task to carry a story-id token for write-back, and whether `/sc:workflow` keeps such tokens is UNVERIFIED (brainstorm-b risk 3).
2. **Each story file must be self-contained.** The plan package snapshots only the source file. The binding documents live under `_bmad-output/` and `_bmad/`, which are untracked per clone (F15), so an Orca worktree created for the work will not contain them. So the story file copies in the rows it needs: its ACs, the `AD-n` rows that bind it, the constraints, the paths it touches, and a "Previous story notes" section. The packet folder is the copy that travels; the BMAD originals stay where BMAD keeps them.
3. **Packet location.** `.dev/issues/<feature-issue>/bmad/` (agent 1's choice, and the house precedent on master `.dev/issues/409/bmad/`). Note the conflict to settle: `/sc:issue` says it never stages or commits `.dev/issues/` and prints "untracked: do not stage it" (`issue.md`, Boundaries), while `.dev/issues/409/bmad/` is tracked on master (agent 1 read it with `git ls-tree`). For a worktree to see the packet, it must be copied in by the coordinator (as the claim script does for `.dev/issues/<N>/`) or be tracked. Owner decision O2 (section 11).

**Position 3.2: the hand-off gate H1.** A story is handed over only when all hold:

| # | Check | Why (file fact) |
|---|---|---|
| H1.1 | `bmad-check-implementation-readiness` passed for the epic and `bmad-sprint-planning` lists the story (`backlog`) | agent 1 S4.1 P11, P12 |
| H1.2 | The story has numbered acceptance criteria with stable ids `S<N>.<M>-AC<n>` and no criterion that cannot be checked by reading code or running a command | `/sc:implement` stops `E-NO-AC` on a task with no acceptance criterion and grades each task against its own AC; brainstorm-b section 3 |
| H1.3 | Type (feature or bug) and complexity (simple, medium, complex) are set using the repo rubric (hours, subsystems, security or data migration) | F10; it picks the chain |
| H1.4 | Paths the story touches are named, or the story says "new area: <where>" | a plan needs real files; trigger T1, T7 of brainstorm-b |
| H1.5 | The `AD-n` rows that bind the story are copied in | agent 1 S3.3 item 3 |
| H1.6 | Constraints are in a `## Constraints` or `## Out of scope` block | `/sc:implement` treats those headings as global constraints and records a breach as `quoted-constraint-breach` (SKILL.md, "Global constraints") |
| H1.7 | Dependencies: the story keys it needs finished first | stories in a feature run in order (section 7) |
| H1.8 | A story GitHub issue exists, with the Complexity field and the Project fields the owner uses | section 8 |
| H1.9 | The owner has said go for this epic or feature, in chat | WORKER-CONTRACT "Git and GitHub ownership": every outward action needs the owner's instruction; memory rule "approvals through chat, never files" |

**Who accepts.** The IronClaude coordinator runs the checklist and writes `status: accepted` or `status: rejected: <reason>` into the packet header (agent 1's template, section 10). A rejection goes back to BMAD with the failing row number; it is not repaired by IronClaude, because the acceptance criteria are BMAD's. Optional second check: `/sc:issue --claim <story issue> --pipeline none` runs the accuracy check of the issue text against today's code (verdict `current` or `out_of_date`) and records effort and complexity; it assigns the issue and posts two comments, so it is an outward action under the owner's go (F10, F8).

**What IronClaude does not lose by skipping `bmad-create-story`** (answers agent 1 question 3): `/sc:workflow` grounds the plan in the real code (codegraph when the index is fresh, else Grep and Read) and runs an advisory pre-review against the source; `/sc:implement` maps each task to its AC. **What it does lose**, so the packet must replace it: (a) previous-story learnings (create-story reads the previous story's Dev Agent Record), replaced by the "Previous story notes" section the coordinator writes from the last story's ledger and write-back record (section 5); (b) extraction of BMAD architecture and PRD text into the story, replaced by the copied `AD-n` rows and constraints; (c) library and version research (create-story does web research); IronClaude's `/sc:workflow` does none, so a story that depends on a library version states it in its constraints, or the alternate arm (section 4) runs with `--research light`. None of this is verified by a run; it is read from the two skills.

## 4. Spec authorship (topic b): default and switch
**Position 4.1 (default): the BMAD story is the spec; IronClaude reviews it once with `/sc:spec-panel` and plans from it. IronClaude writes its own code-grounded spec (`/sc:brainstorm`) and merges it with the BMAD story (`/sc:adversarial --compare`) only when a trigger fires.** This agrees with agent 1 (S5.1 b: BMAD-only plus spec-panel, dual for high-risk) and with the brainstorm run in `agent2/brainstorm-b/merged-requirements.md` (conditional, BMAD default). Two independent proposals in that run reached the same default, but both were produced by the same kind of model reading the same topic file I wrote, so treat the agreement as weak evidence; the trial in 4.4 is the evidence.

**Why BMAD-only is the default (read facts, not measured):** the BMAD material is requirements and architecture, which the owner assigns to BMAD; IronClaude's issue chains already plan a simple feature straight from its text and add a brainstorm only from medium upward (F10); a second spec on every story adds a merge step, which is a new place to lose acceptance criteria; and a quick brainstorm is not cheap: the run I made used 5 sub-agent calls and about 671K tokens (how the harness counts them is UNVERIFIED).

**4.2 Triggers (when to switch to the alternate arm).** The brainstorm proposed seven (T1 to T7) with scripted thresholds. I keep the four that a coordinator can check in a minute without a script, and drop two thresholds:

| Trigger | Check | Kept from brainstorm-b |
|---|---|---|
| S1 stale or ungrounded | a path the story names is missing at HEAD (`test -e`), or the story names no paths | T1, T7 |
| S2 drift | the named paths changed a lot since the story was written (coordinator reads `git log --oneline -- <paths>` since the packet date; a count of 3 commits is the starting guess, UNVERIFIED) | T2 |
| S3 risk class | complexity is `complex` by the repo rubric, or the story changes stored data shape or a protocol (Postgres schema, migration, wire format, credentials, auth) | T4 plus the rubric |
| S4 panel code gap | `/sc:spec-panel` reports a blocking finding located in Dev Notes, constraints or tasks (not on criterion text) | T6 |

Dropped for v0: T3 (3-segment path prefixes) and T5 (more than 8 criteria or 12 tasks): the first is a proxy for "more than one subsystem", which BMAD sets as complexity under the repo rubric; the second is size, which `/sc:workflow --depth` already handles. Both can return if the trial shows missed conflicts. All thresholds are guesses until measured, and the trigger list is frozen during a trial release.

A story with zero criteria, criteria that are not a numbered list, or a task with no AC reference is returned to BMAD (`bmad-correct-course` or a re-run of the story step) with no model call (brainstorm-b section 3; agrees with H1.2).

**4.3 Merge rules (when the alternate arm runs).** I keep brainstorm-b's rules R1, R2, R3, R6 as the core and drop the scripting of them for v0:
- BMAD acceptance criteria are a floor: never renumbered, never dropped, never reworded without a logged row (id, old text, new text or `removed`, reason, evidence `path:line`, status `proposed` or `approved`, approver).
- A worker writes only `proposed` rows; a coordinator (with the owner for criteria changes) sets `approved`. Any `proposed` row stops the story before `/sc:workflow`.
- IronClaude-added criteria get `[IC-n]` ids in a separate list and say which BMAD id they support.
- The adversarial merge output is an input, never the spec: its criteria section is discarded and rebuilt from the story.
- A factual conflict (the code contradicts a path, symbol or signature in the story's notes) is settled for the code and logged as a correction; a normative conflict (a criterion or an `AD-n` cannot hold) is settled for the story, goes to BMAD as a Spec Gap Report, and the story waits.
- IronClaude may not contradict an `AD-n`; a needed change goes up through `bmad-correct-course` (answers agent 1 question 8: accepted).

Brainstorm-b also wants two scripts (`story-gate`, `ac-map-check`) built before any trial. I disagree for v0: the first stories will show whether ids are lost or mapped wrongly; if they are, build the checker then. The checks in the meantime are `grep` of the ids in the plan's task criteria by the coordinator. Risk accepted: an id lost silently in the first story. Guard: the coordinator reads the ledger `ac=` fields against the story's ids before write-back (section 5).

**4.4 Trial.** Measure per story: path taken, triggers fired, model calls and minutes per step (tokens where the command reports them), conflicts found after the default arm ran (a missed conflict), acceptance criteria lost, escalations and `E-HALT-QA` halts and whether the spec caused them. Keep the default if spec-caused failures and missed conflicts stay low in the first stories; the brainstorm proposed thresholds of 10% and 25% over at least 12 stories, which I treat as guesses to set with the owner, not as rules. Start with a plan-only pilot (section 10) before any code is written.

**4.5 Where this leaves `/sc:design`.** Brainstorm-b runs no `/sc:design` on either arm (BMAD's architecture document is the design). I agree for simple and medium stories. For a complex story that creates a new interface or schema (the Postgres and write-path stories of EPIC-01 and EPIC-12), the existing complex chain adds `/sc:design` after the brainstorm (F10); I would keep it there, because `/sc:design` writes an interface spec that `/sc:workflow` then plans from. Open for debate.

**4.6 Doc-level review.** BMAD owns review of its documents (PRD, architecture, epics: `bmad-validate-prd`, `bmad-check-implementation-readiness`, the BMAD review skills); IronClaude reviews at story level only, because the story is the thing it executes. Agent 1 notes that issue 409's BMAD set needed 63 blocking fixes (S1.3); that argues for a document-level independent review before stories are cut, which can be `/sc:spec-panel` on the SPEC (agent 1 S4.1 P9). I accept that as a BMAD-side gate; it is not repeated per story.

## 5. Progress write-back (topic c)
**Principle 5.1: workers never write progress anywhere; the coordinator is the single writer to BMAD and to GitHub, and it writes only from files it has read.** This is the existing rule, not a new one: workers report only through heartbeats and `worker_done` (WC-5, WC-10), the coordinator makes every outward action only on the owner's instruction (WORKER-CONTRACT "Git and GitHub ownership", "Progress posts ... are such actions, made from contracts the coordinator has read"). It also avoids two writers on `sprint-status.yaml`, which agent 1 reports is untracked per clone (so each worktree has its own copy).

**5.2 Events, and where each is read.** The sources are machine-written files, not agent prose:

| Event | Detected from (coordinator reads) | BMAD side (`sprint-status.yaml`, story record) | GitHub side |
|---|---|---|---|
| E0 packet accepted | packet header `status: accepted` | story to `ready-for-dev` | comment on story issue (opens the progress comment) |
| E1 spec reviewed | panel report path from the worker contract; alternate arm: brainstorm and adversarial contracts | none | progress comment: arm taken, panel verdict, open `proposed` rows |
| E2 plan written | workflow contract: `worker_status`, the package's `return-contract.yaml` (`status`, `review_verdict`, `open_blockers`) | none | progress comment: plan path, task count, pre-review result |
| E3 plan approved | the owner's chat approval, recorded by the coordinator (policy O3) | none | progress comment: approved plan hash |
| E4 implement started | ledger `progress.md`: first `T<id>: start` | story to `in-progress` (epic lifts from `backlog`) | Project Status to `In progress` (owner-approved mirror) |
| E5 task done | ledger `T<id>: complete verdict=compliant ...` lines | none | progress comment edited at phase boundaries only (n of m tasks) |
| E6 halted | ledger `halt` or `blocked`, or a blocked contract with a STOP code | none | comment naming the STOP code and that a Ruling or a decision is needed; the story is frozen (WORKER-CONTRACT, "After an `/sc:implement` stop") |
| E7 implemented and reviewed | ledger `FINAL: pass`, package in `.dev/tasks/done/` | story record written (5.4) | progress comment: files from the ledger `files=` fields |
| E8 PR opened | `/sc:pr-submit --monitor 3` result (coordinator or person ran it) | story to `review` | comment with the PR link |
| E9 PR merged and closed out | `/sc:closeout <PR> --issue <N>` result block | story to `done` | story issue closed by closeout; feature issue comment; close the feature when its last story is done |
| E10 spec defect found | a Spec Gap Report from the panel, the pre-review or a halt | none until BMAD answers | comment; coordinator hands the report to BMAD (`bmad-correct-course`) |

`/sc:sweep` already reads the `progress.md` and `return-contract.yaml` of sessions it finds (F13), so the coordinator's wake pass gets E4 to E7 from the report it reads anyway; it does not need a second poller.

**5.3 The GitHub progress comment.** One comment per story issue, edited in place (the claim does this with markers and `gh api -X PATCH`, `claim.md` Wave 6): marker `<!-- sc:release-pipeline:progress story=<N-M> -->` (a name I propose; the existing markers are `sc:issue:claim`, `sc:issue:accuracy-check` and `sc:issue:result`), a fixed table (stage, state, plan path, n of m tasks, PR, last event time), no free text from workers. At most about 8 edits per story. This is new: the only existing GitHub write-back is `issue-pipeline complete` (one result comment per run, Status moved only on `succeeded`, tied to a watcher-claimed issue's `dispatch.json` entry and Project id), which I cannot reuse for a story that did not come through the watcher (F9, gap G2).

**5.4 The BMAD write-back.** Two writes, both by the coordinator, both idempotent and never regressing a status (agent 1 read this behaviour in `bmad-quick-dev/sync-sprint-status.md`; I did not read that file):
1. **Status.** Set the story key to the target status, lift the epic from `backlog` to `in-progress` on the first `in-progress`, refresh `last_updated`, preserve comments. Skipping `ready-for-dev` is impossible because E0 sets it. A small script copying those rules is the one piece to build (section 9); a hand edit by an agent is the fallback and is not idempotent.
2. **A BMAD-conformant story record.** On E7 the coordinator writes `{implementation_artifacts}/<story_key>.md` (BMAD's own name for a story file) from the packet's story file: Status, the story and acceptance criteria copied, Tasks marked from the ledger, and a Dev Agent Record filled from the ledger and the contracts (model names recorded by the commands, file list from the `files=` fields, completion notes from the FINAL review, links to the plan package and the ledger). Why: the next story's `bmad-create-story` and `bmad-retrospective` read story files and sprint status; a story that exists only as an IronClaude package is invisible to them. UNVERIFIED: I did not read `bmad-retrospective`, and whether BMAD tooling accepts a story record written this way is a trial item (brainstorm-b also proposes writing only the story's Dev Agent Record, rule R7).

**5.5 Where the ledger lives.** One `sprint-status.yaml`, written only by the coordinator, in the release (planning) worktree, never in a story worktree. For it to survive and be shared it must be tracked (the `.git/info/exclude` lines are per clone). Owner decision O2.

**5.6 What I did not design:** a push notification to the person, and a per-task live view; the dashboard roadmap (issue 727) is where those belong, and the observer is read-only today (F14).

## 6. Gaps in IronClaude today that the pipeline hits
Each gap is a verified fact about the files today and what it costs the pipeline. None is fixed by this planning.

| # | Gap | Cost to the pipeline | Proposed handling |
|---|---|---|---|
| G1 | `/sc:implement` has no worker (unattended) mode and writes no `return-contract.yaml` (F6). The worker contract text already assumes one ("for `/sc:implement`, also when blocked, carrying the STOP code", WC-4; per-task commits wait for issue #326, WC-9). | The execution step has no coordinator-dispatched route. Under WC-5 a worker with no contract sends `worker_done --outcome failed`, so Orca would record a successful implement as failed. | A (pilot): the person, or a person-opened session, runs `/sc:implement <plan path>` in the feature worktree; the coordinator reads the ledger. B: dispatch a worker with no flag and read the ledger as the contract; works but Orca records `failed`. C (build): add an `## Unattended mode` section to `/sc:implement` that writes the contract from the ledger (succeeded when every task is complete and FINAL passed; partial when archive is blocked; blocked on a halt with the STOP code; failed on a STOP). Work item #1 of the pipeline. Whether an issue for it exists: I found none (issue search by title words); UNVERIFIED. |
| G2 | The issue pipeline's worker brief is a closed template with one row per Project Status (research, spec, plan, debug); no implement row; `issue-pipeline complete` and `stage-status` assume a watcher-claimed issue (`dispatch.json` entry, Project id, grant row) (F9). | Stories cannot use the watcher flow end to end. | Mode C (section 7): the coordinator hand-writes briefs from the template in WORKER-CONTRACT section 5; later add story rows to `brief.py` and its template, with tests. |
| G3 | Launch levels `worktree`, `full`, `full submit` are behind a ship gate (F9). Only level `none` launches. UNVERIFIED whether it opened after 2026-11-19. | No launched agent can run implement for a claimed issue; the goal of issue 689 (claim goes straight to workflow and implement) is not reachable yet. | Do not depend on governed levels in v0. |
| G4 | No progress write exists between start and `worker_done`; no BMAD write-back exists; IronClaude has no BMAD code (F16). | Progress is invisible in BMAD and on the issues until something is built. | Section 5: one progress-comment template, one status-sync script, one story-record writer. |
| G5 | `/sc:spec-panel` gets `--unattended` on a worker line only after a phase 2 live check or when the owner's instruction names it (F7). | A worker run of the panel needs the owner's instruction quoted. | The owner's text names spec-panel; the coordinator quotes it; record it in run notes. UNVERIFIED whether the phase 2 check passed. |
| G6 | BMAD skills are not `/sc:` commands: no command file, no `## Unattended mode`, no worker contract. Agent 1 found headless modes in some BMAD skills (prd, architecture, spec, ux, product-brief, brainstorming) but none for epics and stories. | The brief guard and the contract do not cover them. | v0: every BMAD skill runs in a person-opened attended session. A headless BMAD worker is a later experiment and needs a contract extension. |
| G7 | UNVERIFIED: whether `/sc:workflow` keeps story and AC ids in the plan's task criteria. | Write-back and the id-loss check depend on it. | Test in the plan-only pilot (section 10) before any code is written. |
| G8 | A managed plan must be implemented in the same checkout where `/sc:workflow` wrote it (`E-MANAGED-INVALID` for a copy or another checkout; F5). | The panel, workflow and implement Tasks of one story must share one worktree; a plan cannot be written in one worktree and implemented in another. | One worktree per feature, stories in order inside it (section 7); resume with `--worktree path:<that worktree>`. |
| G9 | `.dev/issues/` is "never staged" by `/sc:issue` yet `.dev/issues/409/bmad/` is tracked on master; `_bmad/` and `_bmad-output/` are untracked per clone. | A new worktree does not contain the packet or the ledger. | Owner decision O2. |
| G10 | Plan approval (WC-17) uses `issue-pipeline plan-hash` and `check-approval`, which need an issue number and an approval record whose evidence comes from GitHub through `stage-status` (F9). How that works for a Mode C story (no watcher claim) I did not verify. | A plan-approval gate for stories is not defined. | Owner policy O3; until then the owner approves the plan in chat and the coordinator records it in run notes, and no worker is told to cross a plan boundary on its own. |
| G11 | The observer is read-only (F14); a halt for a Ruling needs the person's own chat confirmation (F5). | Halts and plan approvals are handled in chat. | This is the dashboard roadmap itself (issue 727); the decision inventory in section 7.7 is an input to it. |
| G12 | Per-task commits inside `/sc:implement` do not exist yet (issue #326); a worker may not commit without a quoted owner instruction and its own child worktree (WC-9). | Local commits per story are the coordinator's. | The coordinator commits explicit paths plus `.dev/tasks` after a story settles, under the owner's instruction (WORKER-CONTRACT "Git and GitHub ownership"). |

## 7. Coordinator, worktrees, sessions, sequence (topic d)
**7.1 Mode C (v0) versus Mode W.** The existing issue pipeline (Mode W) is driven by the issue watcher, the Project Status and the `Approved` field, and its briefs are closed templates (F9, G2). For the release pipeline I recommend **Mode C: the coordinator drives the story chain itself**, writing each Task's brief from the template in WORKER-CONTRACT section 5, and using the existing `issue-pipeline` and Orca verbs only where they fit. Reasons: no implement row and no worker mode for implement exist in Mode W (G1, G2); the watcher's prompt pattern is pinned to `/sc:issue --claim N --pipeline ... --stage ...` and its worker brief is built from a closed set so that no issue text reaches a brief (F9), which is a security property worth keeping, not bypassing. Convergence path: when implement has an unattended mode (G1) and the governed levels open (G3), add story rows to `brief.py` and let the watcher drive stories. Mode C is not a new coordinator: it is the coordinator the contract already describes, working on tasks it plans itself.

**7.2 Sessions.**

| Session | Opened by | Does | Never does |
|---|---|---|---|
| Release coordinator (one per release, one Orca Run) | the owner | accepts packets (H1), creates Tasks and workers, reads contracts and ledgers, runs `/sc:sweep`, writes progress and BMAD status, files issues and runs `/sc:pr-submit` and `/sc:closeout` on the owner's instruction | answers a BMAD menu; types into a person's session; pushes or comments without the owner's instruction; relaunches a worker on silence (WC-6, WC-10) |
| BMAD planning session (attended, as many as the owner opens) | the owner or a developer, ordinary session in the planning worktree | runs `/bmad-*` skills with the person present | is messaged or dispatched by the coordinator |
| Story worker (one per Task) | the coordinator through `worker-start` | one command (panel; or brainstorm and adversarial; or workflow) under `--unattended` | commits, pushes, comments, creates worktrees or Tasks (WC-9, WC-13) |
| Implement session | person (pilot) or worker (after G1) | `/sc:implement <plan path>` in the feature worktree | commit, push, PR |

**7.3 Worktrees (all created by Orca, never raw `git worktree add`).**
- One **release worktree** where the coordinator runs and BMAD planning happens: it holds the `sprint-status.yaml` ledger and the planning artifacts, and nothing else writes the ledger.
- One **feature worktree** per BMAD feature that is being built, created as an Orca child with `worker-start --worktree new-child --base-branch <ref> --setup skip`. Inside it, the stories of the feature run one after another; each story's panel, workflow and implement Tasks run in that same worktree (G8); a later Task is placed with `--worktree path:<that worktree>`. Packages are separate per story (distinct plan slugs, as the contract requires for concurrent implement runs).
- The base ref: agent 1 found that the dashboard code is on origin/master, not on this working branch, so features that touch the code must start from a worktree based on `origin/master`; the contract's default is `--base-branch <feature branch>` with children merged back into it. **Owner decision O4:** (1) contract default: children merge back into a release branch and one PR carries the release (a release of 30 stories would be one unreviewable PR); (2) my recommendation: each feature worktree is based on `origin/master`, is never merged back, and carries its own PR per feature through `/sc:pr-submit --monitor 3` in a top-level session of that worktree, after a rebase on origin/master (owner rule of 2026-11-17 in memory). Option 2 is a documented exception to WORKER-CONTRACT's "children merge back" rule and needs the owner's go.

**7.4 Order of work per story, and what each Task is.** Tasks are created one at a time, each only after its predecessor settled and was read (contract "Reading a result before anything depends on it"), so the plan path is known when the implement Task is created.

1. Coordinator, no model call: check H1; check triggers S1 to S3 (section 4.2) to choose the arm.
2. Task A, default arm: `/sc:spec-panel` on the story file. Coordinator reads the verdict; S4 or a CRITICAL finding on criteria goes to BMAD as a Spec Gap Report (E10), the story waits. Alternate arm: Task A1 `/sc:brainstorm`, Task A2 `/sc:adversarial --compare`, then Task A3 the panel on the merged spec.
3. Task B: `/sc:workflow` on the (merged) story file. Coordinator reads the package contract, the plan, the pre-review result.
4. Plan boundary: the owner's approval in chat (policy O3).
5. Task C: `/sc:implement <plan path>` (pilot: person-run; after G1: worker). A halt freezes the story (WORKER-CONTRACT "After an `/sc:implement` stop"); the owner gives the Ruling in chat.
6. Coordinator: reads the ledger, commits locally (under the owner's instruction, G12), writes E7 and the BMAD record, starts the next story.
7. After the last story of a feature: rebase, `/sc:pr-submit --monitor 3` (owner's instruction), then `/sc:closeout <PR>` after the merge, then E9.

**7.5 Sequential or parallel.**

| What | Mode | Why |
|---|---|---|
| BMAD planning of release n+1 and IronClaude execution of release n | parallel | planning writes the planning worktree and issues; execution writes feature worktrees. One shared file: `sprint-status.yaml` (written by BMAD's sprint-planning, which never downgrades, and by the coordinator's never-regress edits); the race is small and is a trial item |
| Stories inside a feature | sequential | BMAD says a story must not depend on a later one and the next story learns from the previous (F15); same files; one worktree |
| Features of one release | parallel when they declare no dependency and touch different named paths; start with 2 at a time | no concurrency cap is documented in the files I read (UNVERIFIED); issue 468 reports Orca wait spam; measure |
| Panel, workflow, implement of one story | sequential | each reads the previous result; WC-11 one writer per worktree |
| Several workers in one worktree | no | WC-11: workers share a worktree only if they write nothing but their own report directory; workflow and implement write under `.dev/tasks/` and implement writes product files |

**7.6 What the coordinator does while the person is in a BMAD session.** It does not wait on it. It runs its execution queue, runs `/sc:sweep` on each wake (the planning session appears as `person session (active)`, never messaged, F13), and reads the planning worktree's epics and `sprint-status.yaml` read-only to spot stories that have become `backlog` and ready for a packet. It tells the owner when a packet is ready or rejected.

**7.7 Decisions that need a person (input to the dashboard roadmap).** Everything below is a question the coordinator cannot answer itself; each can be boiled down to a binary or multiple-choice question, which is what the owner wants the dashboard to do (issue 727):

| Decision | Options |
|---|---|
| Owner go for an epic or feature (H1.9) | go / hold |
| Packet rejected: return to BMAD or override | return / override |
| Plan approval for a story | approve / request changes / reject |
| Ruling after `E-HALT-QA` (accept the explained gap, fix the code, send to BMAD) | accept scope X / fix / spec gap |
| Spec Gap Report: change criterion, change story, drop story | per row |
| Push, PR, merge, closeout | go / no |
| Add a trigger or change a threshold mid-release | refused by rule; owner can re-open |
| Concurrency (how many features at once) | 1 / 2 / 3 |

## 8. GitHub issues (topic e) and the division of labour (topic f)
**8.1 Who files, what, when.**

| Object | Filed by | Tool | When |
|---|---|---|---|
| Epic issue and feature sub-issue (containers) | the coordinator, from agent 1's drafts, after the owner reviews the consensus | plain `gh issue create --repo IronbellyOrg/IronClaude --title ... --body-file <draft>` with labels, then link as a native sub-issue | when the owner schedules that release (owner rule in issue 727) |
| Story issue (the claimable unit) | the coordinator at hand-off (H1.8) | `/sc:issue --create @<draft> --mode feature --type <area> --depth quick` so the issue type, the Complexity field and the mode label are set | at hand-off, not earlier (agrees with agent 1 S3.1) |
| Sub-issue links | the coordinator | the GitHub sub-issues REST endpoint through `gh api` (I did not verify its shape in this repo; agent 1 saw `sub_issues_summary` on 727 and 609) | at filing |

`/sc:issue --create` is the right tool for stories because it sets the issue type, the Complexity field and the label that the later claim and the rubric use (F11); I found no linking in it, so links are a separate `gh api` call. For container issues, `/sc:issue --create` is a worse fit: its templates are for a feature or a bug with Priority, Fix approach and Test plan (issue 689 text), and it posts directly with no preview ("nothing is shown for approval first"). Every filing is a GitHub write, so each happens only on the owner's instruction naming it (WORKER-CONTRACT "Git and GitHub ownership").

**8.2 Updates through the life of a story** (all by the coordinator, section 5): the progress comment edited in place at the events E0 to E10; Project Status mirrored at E4 (In progress), E8 (In review) and E9 (Done) when the owner has authorised the mirror; closure through `/sc:closeout` (it reads the issue's own criteria and closes it, or leaves a note of what remains); the feature issue gets one comment per finished story and closes with its last story; the epic closes with a summary comment that links the BMAD retrospective. GitHub's own sub-issue counter gives the roll-up bar, so nothing else counts.

**8.3 What each issue body carries.** Agent 1's drafts carry the BMAD workflow to invoke to start story planning. At hand-off the story issue also carries an "IronClaude execution" section: the packet path, the arm (default or alternate and which trigger), the complexity, the chain, the plan path once known. The coordinator edits that section; workers never touch issues.

**8.4 Division of labour (topic f).**

| Step | Owner | Notes |
|---|---|---|
| Brief, research, PRD, UX, architecture, SPEC, epics, stories, acceptance criteria, story order, the sprint ledger, retrospectives, course corrections | BMAD (attended sessions) | IronClaude never edits these except the two write-backs below |
| Document-level review of those artifacts | BMAD side (BMAD review skills; `/sc:spec-panel` on the SPEC as a gate agent 1 proposed) | not repeated per story |
| Intake check H1, story-level spec review, optional code-grounded spec, design when open, tasklist, implementation, per-task QA, final review, retries, PR, review loop, CI fixes, closeout | IronClaude | rapid iteration lives here: the retry ladder, `/sc:troubleshoot`, the PR monitor |
| Write-back: story status, story record, progress comments, issue closure | the coordinator | the only IronClaude writes into BMAD artifacts: `sprint-status.yaml` status values and the story record |
| Spec defects found during execution | IronClaude detects, BMAD decides | a Spec Gap Report (failing AC, evidence `path:line`, options) goes to `bmad-correct-course`; IronClaude never rewrites a criterion or an `AD-n` on its own |
| Owner decisions | the owner | section 7.7 |

Rule (f): loops that stay inside implementation never go back to BMAD; only a spec defect does. A failed task, a failed review, a PR review finding and a CI failure are handled in IronClaude; a criterion that is wrong, ambiguous, impossible or in conflict with an `AD-n` is a Spec Gap Report.

## 9. Reusable: what exists, what to build (topic g)
**9.1 Already exists (read in files; reuse, do not rebuild).**

| Kind | Items |
|---|---|
| IronClaude commands for the chain | `/sc:spec-panel`, `/sc:brainstorm`, `/sc:adversarial`, `/sc:design`, `/sc:workflow`, `/sc:implement`, `/sc:reflect`, `/sc:troubleshoot`, `/sc:pr-submit`, `/sc:closeout`, `/sc:sweep`, `/sc:issue`, `/sc:recommend`; for the release boundary `/sc:release-split` (the guide lists it for "assess release split versus intact release", section 3.13; I did not read it, so whether it suits a dashboard release list is UNVERIFIED) |
| Coordinator machinery | WORKER-CONTRACT (brief template, WC rules, liveness ladder, after-implement-stop rules, fan-in rule); `superclaude issue-pipeline` verbs `plan-hash`, `check-approval`, `adopt-create`, `adopt-mark`, `record-create`, `record-show`, `record-mark`, `release-worker`, `complete`, `stage-status` (read in `cli.py`; only `plan-hash` and `check-approval` fit Mode C unchanged); `superclaude issue-watch`; `superclaude sweep run`; `superclaude observe` (read-only) |
| Agents | `issue-worker-t1`, `-t2`, `-t3` (claim lookups, accuracy check, issue drafts); `reflect-reviewer`, `evidence-validator`, `merge-executor`, `debate-orchestrator`, `implement-retry-adviser`, `workflow-reviser`, `finding-grader`, `reuse-auditor`. The `rf-*` agents are under review (issue 572: keep, refactor, simplify or remove), so the pipeline should not depend on them |
| Templates | WORKER-CONTRACT section 5 brief template; `~/.claude/ISSUE-HANDOFF.md`, `~/.claude/ISSUE-BACKLOG.md`; `~/.claude/templates/documents/` (`prd_template.md`, `tdd_template.md`, `release-spec-template.md`, `roadmap_template.md`) and `~/.claude/templates/workflow/` (listed with `find`, not read); the `/sc:issue --create` templates (issue skill `templates/`); agent 1's `agent1/templates/handoff-packet.md` |
| BMAD side | all `bmad-*` skills installed in the project `.claude/skills/` (agent 1); the worked example `.dev/issues/409/bmad/` on master |
| Patterns to copy | marker comments edited in place with `gh api -X PATCH` (`claim.md` Wave 6); the ledger grammar (`refs/ledger.md`); the idempotent never-regress status sync of `bmad-quick-dev/sync-sprint-status.md` (agent 1) |

Answer to agent 1 question 9: I found no script that edits issue bodies and no BMAD ledger code in IronClaude (grep on master for "bmad"; read of the issue-pipeline CLI verbs). The roadmap and sprint CLI families that CLAUDE.md of this branch lists are not in master's `src/superclaude/cli/` (checked with `git ls-tree`), and issue 571 plans their removal; do not build on them.

**9.2 To build, in priority order.** Priority P0 is needed for the plan-only pilot, P1 for a trial release, P2 later. Owners are proposals.

| # | Item | Kind | P | Notes |
|---|---|---|---|---|
| B1 | H1 intake checklist and the packet template amended to a folder with one story file per story | template (agent 1 owns the template, I own the checklist) | P0 | sections 3.1, 3.2 |
| B2 | Release coordinator run-notes template: per-story state, arm taken, triggers fired, placement map, Task and Dispatch ids, measurements | template | P0 | WORKER-CONTRACT already requires run notes and a placement map |
| B3 | Spec Gap Report template (failing criterion, evidence `path:line`, options, who decides) | template | P0 | section 8.4 |
| B4 | `/sc:implement` Unattended mode (G1) | command and skill change plus tests | P1 | IronClaude work item #1; until it lands, the person runs implement |
| B5 | Progress comment template and a script that renders it from the ledger and contracts and prints a body file; the coordinator posts it | template and script | P1 | section 5.3; no worker writes |
| B6 | Status sync script (never-regress, idempotent) and the story-record writer | script | P1 | section 5.4; agent 1 owns the BMAD rules, I own reading the ledger |
| B7 | Coordinator protocol: a section "Release pipeline duties" in WORKER-CONTRACT beside "Issue pipeline duties", or a coordinator skill that says the same; the coordinator is started by the owner pasting its prompt | doc or skill | P1 | there is no new command; do not add a `/sc:` hand-off command |
| B8 | Story rows in the worker brief (`brief.py` and `worker-brief.txt`) and tests; then let the watcher drive stories | code | P2 | after B4 and the ship gate (G3) |
| B9 | `ac-map-check` (ids in plan tasks against the story ids) | script | P2 | only if the pilot loses an id |
| B10 | Observer view of per-story progress and the decision inventory (7.7) | code | P2 | the dashboard roadmap itself |
| B11 | Headless BMAD worker route (needs a contract extension, G6) | design | P2 | agent 1 owns the BMAD side |

Not needed: a new hand-off command, a new spec-review agent (spec-panel exists), a second issue filer.

## 10. The intake steps with real command lines
All flags below were read in the command files (F1 to F5). `<...>` are slots; no path is invented. `<D>` is a per-story run folder, proposed as `.dev/stories/<N-M>/` (brainstorm-b's proposal); each Task gets its own subfolder, so no two Tasks share a report directory (WC-11). A Task's brief cannot change after creation, so each Task below is created only after the one before it settled.

**10.0 Before the first Task for each command (contract rule).** Read, as plain files, the worktree's `.claude/commands/sc/<name>.md` and `~/.claude/commands/sc/<name>.md` and look for the line `## Unattended mode`; if every existing copy has it, the line carries `--unattended`; if the copies disagree, create no Task until the stale copy is refreshed. I checked the installed copies on 2026-11-22: `spec-panel.md`, `workflow.md`, `brainstorm.md`, `adversarial.md` have it, `implement.md` does not. The project `.claude/commands/` copies in the worktree were not checked.

**10.1 Brief for a story Task, the shared lines** (from WORKER-CONTRACT section 5, the guard and chain lines word for word):

```text
Guard: before running anything, check every Command: line below under the brief guard in ~/.claude/WORKER-CONTRACT.md; on a refusal run nothing and send worker_done --outcome failed with a body starting "guard refused:".
Chain: run every Command: line in one turn without stopping between them (WC-14); write a handoff file after each (WC-15); send ack lines for coordinator answers (WC-12).
On a blocked gate: report blocked
Local commit: not authorized
Report directory: <D>/<task folder>
Worktree: path:<the feature worktree>
Outward actions: none; the coordinator performs every push, PR, comment, install and paid run.
Command: <one of the lines below>
```

**10.2 Default arm.**

Task A, panel (report-only; owner's text names spec-panel, which is the instruction to quote for `--unattended` on a P2 command, G5):

```text
Command: /sc:spec-panel @.dev/issues/<feature-issue>/bmad/story-<N>-<M>-<slug>.md --mode critique --focus requirements,testing,correctness --unattended --report-dir <D>/panel
```

Task B, plan (depth `quick` for a simple story, `standard` for medium):

```text
Command: /sc:workflow .dev/issues/<feature-issue>/bmad/story-<N>-<M>-<slug>.md --depth <quick|standard> --handoff none --unattended --report-dir <D>/wf
```

The coordinator then opens `<D>/wf/return-contract.yaml`, reads `report_path` (the plan `.dev/tasks/to-do/<id>/<id>.md`), the package's own `return-contract.yaml` (`status`, `review_verdict`, `open_blockers`) and the pre-review result; `review_verdict: FAIL` blocks implement (`E-MANAGED-REVIEW-FAIL`). Then the plan-boundary approval (O3).

Task C, implement. No `--unattended` exists (G1):

```text
/sc:implement <plan path printed by Task B>
```

Run by the person in the feature worktree (pilot), or by a worker after B4. The ledger is `<package>/progress.md`; resume is the same command again; a halt is handled under "After an `/sc:implement` stop". `/sc:implement` does not commit, push or open a PR.

**10.3 Alternate arm (a trigger fired).**

```text
Command: /sc:brainstorm "code-grounded spec for story <N>.<M> @.dev/issues/<feature-issue>/bmad/story-<N>-<M>-<slug>.md" --codebase --blind --depth quick --proposals 2 --research none --unattended --output <D>/bs
Command: /sc:adversarial --compare .dev/issues/<feature-issue>/bmad/story-<N>-<M>-<slug>.md,<D>/bs/merged-requirements.md --depth quick --focus correctness,architecture --unattended --output <D>/adv
```

Then rebuild the merged spec under rules R1, R2, R3, R6 (4.3), run Task A on it, then Task B on it with `--depth standard`. For `--depth standard --proposals 3` and `--research light` use them only when the story is complex or depends on a library version. `/sc:design` follows the brainstorm only for a complex story that creates a new interface or schema (4.5). Under `--unattended` brainstorm and adversarial take their own `--output` as the report directory, never together with `--report-dir`.

**10.4 Plan-only pilot (no code is written).** Purpose: test the contract with real files before anything is built or run on code. Steps: (1) the owner picks one small real story; agent 1's template is filled for it under `.dev/issues/<N>/bmad/`; (2) the coordinator runs H1 and records the result; (3) Task A and Task B above; (4) read the plan: are the story ids present in the task criteria (G7), is anything lost, what did the pre-review say, how many model calls and minutes did each step take; (5) stop before implement; (6) write a one-page pilot report. Nothing here commits, pushes or posts. A second pilot adds a person-run `/sc:implement` of the same plan in the feature worktree and the write-back of section 5. The owner's issue 726 (a vote on each question, kept as a local record) is a candidate only after its open decision about the read-only rule is settled (issue 727, owner's text); I did not verify its current state beyond the text of 727.

## 11. Questions for the other agent, and what I need
**11.1 Questions for the other agent (bmad-planner).**

1. Per-story execution: do you accept a packet folder with one self-contained story file per story, in place of one packet file per feature (section 3.1)? If not, how would write-back map tasks to stories?
2. Who assigns the story ids `S<N>.<M>-AC<n>` and the numbered acceptance criteria: BMAD in the epics file, or the packet generator? BMAD's epics use Given, When, Then (your S1.2); the BMAD story template uses free numbered text (`bmad-create-story/template.md`). I need stable numbered ids either way.
3. Status mapping: do you accept `ready-for-dev` at packet acceptance (E0), `in-progress` at the first `T<id>: start` of the implement ledger, `review` at PR open, `done` at closeout (section 5.2)? Your template (section 9) flips at claim, PR open and merge.
4. Ledger home: do you accept that `sprint-status.yaml` and the planning artifacts are tracked in git (the two `.git/info/exclude` lines are per clone) and written only by the coordinator in the release worktree? Does the BMAD installer tolerate that? Did you read `bmad-quick-dev/sync-sprint-status.md` in full (section 5.4 relies on your reading)?
5. Does `bmad-retrospective` or `bmad-sprint-status` read story files (their Dev Agent Record), or only `sprint-status.yaml`? It decides whether the story record of section 5.4 is needed.
6. Do your story-issue drafts leave a section "IronClaude execution" for the coordinator to fill (section 8.3)? Stories are filed at hand-off in both our plans.
7. Complexity: will the BMAD story carry `Complexity: simple|medium|complex` and an hours estimate using the repo rubric (section 3.2, H1.3)? The rubric text is in `refs/claim.md`.
8. BMAD sessions are attended-only in v0 and a headless BMAD worker is deferred (G6). Do you accept?
9. The Spec Gap Report goes to `bmad-correct-course`, which needs the PRD and the epics. Is that enough input, or does it need a different shape from me?
10. First pilot story: do you have a candidate among your drafts that is small, real and has stated paths?

**11.2 What I need from the other agent.** N1: your answer on the packet shape (question 1) and the ids (question 2), because B1 and the H1 checklist depend on them. N2: the BMAD-side rules of the status sync and the sprint planning re-run (question 3, 4), because I only read them second-hand. N3: confirmation of which of your files are templates I may reference by path in CONSENSUS.md. N4: for each epic draft, the complexity class you expect (it picks the chain and the arm).

**11.3 Decisions for the owner that I cannot settle with agent 1** (they go into CONSENSUS.md as open items if not settled).

| # | Decision | My recommendation | If the owner says otherwise |
|---|---|---|---|
| O1 | Drive stories in Mode C (coordinator-written briefs) or wait for the watcher flow | Mode C | the pipeline waits for B4 and B8 and the ship gate, which are not scheduled |
| O2 | Track `_bmad-output/` (and team files `_bmad/custom/*.toml`) in git, and where the packet lives (`.dev/issues/<N>/bmad/` versus `_bmad-output/`) | track `_bmad-output/` on the release branch; packet under `.dev/issues/<N>/bmad/` per the 409 precedent, copied into each worktree | the ledger stays per clone and only one clone may run the pipeline |
| O3 | Plan approval before implement: every story, medium and complex only, or one approval per feature | every medium and complex story, plus the first story of each feature; simple stories after the feature's first approval | the `Plan approval:` line (WC-17) is dropped from briefs, which weakens the stop before code is written |
| O4 | PR topology: one PR per feature from worktrees based on `origin/master`, or one release branch with children merged back | one PR per feature | one PR per release, which the contract supports without exception |
| O5 | Build `/sc:implement` Unattended mode first (B4) | yes | implement stays person-run, and the pipeline does not run unattended past the plan |
| O6 | Standing instruction for the coordinator: local commit per settled story, progress comment edits, Project Status mirror, issue filing | give it in chat once per release, naming each action | each action is asked at the moment, which costs the owner a decision per story |

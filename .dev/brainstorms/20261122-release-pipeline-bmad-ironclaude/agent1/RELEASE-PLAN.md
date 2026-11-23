# RELEASE-PLAN (agent 1, bmad-planner): multi-release plan to version 2.0 via BMAD

STATUS: Round 0 text complete (S1 to S5), amended in Round 2 (S4.1 P7b and S4.2 L8 to L10 follow the agreed text). Issue drafts in `issue-drafts/` (see its README.md). Section S3.2, S3.3 and S5.1 are agent 1's OPENING positions; where they differ from `shared/CONSENSUS.md` (packet is a folder of story files, story-level planning, status mapping D3, `/sc:implement` person-run today), CONSENSUS.md governs.

## S1. What BMAD gives us (read in the skill files on 2026-11-22; BMAD 6.9.0 per `_bmad/_config/manifest.yaml`)

### S1.1 Result of `/bmad-help` (invoked with the owner's roadmap as the question)

State found by following the skill's own data-source rules: catalog `_bmad/_config/bmad-help.csv` (read); config `_bmad/bmm/config.yaml` (read: `planning_artifacts` = `_bmad-output/planning-artifacts`, `implementation_artifacts` = `_bmad-output/implementation-artifacts`, `project_knowledge` = `docs`); artifacts: both output folders are EMPTY; `docs/index.md` does not exist; no `project-context.md` anywhere in the repo. So `/bmad-help` places us at the very start of module BMad Method (bmm), phase `1-analysis`, nothing complete, and this is a brownfield project. The catalog's required gates are: `bmad-prd` (phase 2-planning), `bmad-architecture` (3-solutioning), `bmad-create-epics-and-stories` (3), `bmad-check-implementation-readiness` (3), `bmad-sprint-planning` (4), then the story cycle `bmad-create-story` and `bmad-dev-story`. Everything in phase 1 and the `anytime` skills is optional. The skill says to run each skill in a fresh context window and to offer a quick start.

The catalog's order, quoted from `bmad-help.csv` columns `phase`, `preceded-by`, `required`:

| Phase | Skill (menu code) | Required | Output (catalog) |
|---|---|---|---|
| anytime | `bmad-generate-project-context` (GPC), `bmad-document-project` (DP), `bmad-quick-dev` (QQ), `bmad-correct-course` (CC), `bmad-brainstorming` (BSP), `bmad-party-mode` (PM), `bmad-forge-idea` (FI), `bmad-spec` (SP), `bmad-customize` (BC), review skills (EP, ES, AR, ECH), `bmad-shard-doc` (SD), `bmad-index-docs` (ID), `bmad-agent-tech-writer` (WD, US, MG, VD, EC) | no | project-context.md; change proposal; SPEC.md; etc. |
| 1-analysis | `bmad-brainstorming` (BP), `bmad-market-research` (MR), `bmad-domain-research` (DR), `bmad-technical-research` (TR), `bmad-product-brief` (CB), `bmad-prfaq` (WB) | no | research documents; product brief; prfaq |
| 2-planning | `bmad-prd` (PRD), `bmad-ux` (CU) | PRD yes; UX no | prd; ux design |
| 3-solutioning | `bmad-architecture` (CA), `bmad-create-epics-and-stories` (CE), `bmad-check-implementation-readiness` (IR) | all three yes | architecture; epics and stories; readiness report |
| 4-implementation | `bmad-sprint-planning` (SP), `bmad-sprint-status` (SS), `bmad-create-story` (CS, VS), `bmad-dev-story` (DS), `bmad-code-review` (CR), `bmad-qa-generate-e2e-tests` (QA), `bmad-retrospective` (ER), `bmad-checkpoint-preview` (CK), `bmad-investigate` (IN) | SP, CS, DS yes | sprint status; story; story validation; test suite; retrospective |

Note: the catalog carries the menu code `SP` twice (Sprint Planning in bmm, Spec in core). Quote the skill name, not the code.

### S1.2 Facts that shape the pipeline (each read in a skill file)

1. **Epics and stories.** `bmad-create-epics-and-stories` (4 step files) needs a PRD and an architecture document in `{planning_artifacts}`, builds `{planning_artifacts}/epics.md` from `templates/epics-template.md`, asks the user for approval at each menu (steps 2 and 3 say "NEVER generate content without user input", "halt at menus"). Story form: `As a / I want / So that` plus `Given / When / Then` acceptance criteria; each story must be completable by one dev agent and must not depend on a later story; epics are organised by user value, not technical layers. Step 4 validates FR coverage. It has NO headless mode (no headless file in the skill folder). It writes one fixed file, `epics.md`; there is no per-release naming.
2. **Features exist in BMAD, as PRD feature groups.** `bmad-prd` says "Features grouped; FRs nested with globally numbered stable IDs" (SKILL.md, section PRD Discipline). This is the layer the owner calls "features": a GitHub epic = BMAD epic, a sub-issue "feature" = a PRD feature group with its FR ids, user stories = BMAD stories `N.M` under it.
3. **Sprint ledger.** `bmad-sprint-planning` turns every `## Epic N:` and `### Story N.M: Title` found in `*epic*.md` (whole or sharded `epics/index.md`) into `{implementation_artifacts}/sprint-status.yaml` keys `epic-N`, `N-M-kebab-title`, `epic-N-retrospective`. Status machines (verbatim from the skill): epic `backlog -> in-progress -> done`; story `backlog -> ready-for-dev -> in-progress -> review -> done`; retrospective `optional <-> done`; action items `open -> in-progress -> done`. It never downgrades a status and carries `action_items` over.
4. **Status sync rule.** `bmad-quick-dev/sync-sprint-status.md` is an idempotent updater: set the story to the target status, never regress, lift the parent epic from `backlog` to `in-progress` when a story goes `in-progress`, refresh `last_updated`, preserve comments. This is the exact behaviour an IronClaude write-back must copy. `bmad-sprint-status` has a `data` mode (returns `count_backlog`, `count_ready`, `count_in_progress`, `count_review`, `count_done`, epic counts, `open_action_items`, `risks`) and a `validate` mode (checks metadata and status values).
5. **Story file.** `bmad-create-story` produces `{implementation_artifacts}/<story_key>.md` with sections Story, Acceptance Criteria, Tasks / Subtasks, Dev Notes, Dev Agent Record, File List, sets `Status: ready-for-dev`, moves the sprint-status entry from `backlog` to `ready-for-dev`, and lifts the epic to `in-progress`. Its job (its own words) is "everything needed for flawless implementation": architecture extraction, files to modify, previous-story intelligence, git intelligence, web research. That is implementation planning, which the owner gives to IronClaude (see the hand-off question in S5).
6. **Dev side.** `bmad-dev-story` may only change the story's checkboxes, Dev Agent Record, File List, Change Log and Status, and sets `review` when done; `bmad-code-review` then moves it on (catalog: "If issues back to DS if approved then next CS or ER if epic complete"). IronClaude replaces these two for this project (proposed).
7. **Loops back up.** `bmad-correct-course` (needs PRD and epics; optional architecture, UX, spec, document-project index) writes `{planning_artifacts}/sprint-change-proposal-{date}.md`. `bmad-retrospective` reads the sprint status, previews the next epic and appends `action_items`. These are the BMAD ends of the feedback loops the roadmap needs (feedback releases 1.2, 1.9; bug cycles).
8. **Headless.** Headless (no TTY, caller supplies inputs, JSON status returned) exists for `bmad-prd` (`references/headless.md`), `bmad-architecture`, `bmad-spec`, `bmad-ux`, `bmad-product-brief`, `bmad-brainstorming`. NOT for `bmad-create-epics-and-stories` (interactive only) and NOT for `bmad-forge-idea` ("interactive and socratic by nature; there is no headless mode"). So an unattended IronClaude worker can draft a PRD, architecture, spec or brainstorm, but epics and stories need a person in the session.
9. **Customization hooks.** Every workflow has a `customize.toml` `[workflow]` table with `activation_steps_prepend/append`, `persistent_facts`, `on_complete`; `bmad-prd` and `bmad-architecture` also have `external_sources` and `external_handoffs` (natural-language directives run at Finalize); override files live in `{project-root}/_bmad/custom/{skill-name}.toml` (team) and `.user.toml` (personal, gitignored); `bmad-customize` writes them. `persistent_facts` defaults to `file:{project-root}/**/project-context.md`.
10. **Memory discipline.** PRD, architecture, spec, brief, brainstorm keep an append-only `.memlog.md` written only through `uv run {project-root}/_bmad/scripts/memlog.py append --workspace <dir> --type <...> --text "..."`. SPEC.md and the spine are DERIVED from the memlog and must never be hand-edited (`bmad-spec`: "a hand-edit to SPEC.md from outside is unsupported and is overwritten on the next derive"). Architecture IDs `AD-n` and spec ids `CAP-n` are stable and never renumbered.
11. **Personas.** Agents installed (read in `_bmad/config.toml`): Mary (analyst), Paige (tech writer), John (PM), Sally (UX), Winston (architect); Amelia the Developer appears in the retrospective and dev skills (`bmad-agent-dev`; name not read in config, UNVERIFIED beyond the retrospective text).

### S1.3 Where BMAD output lives here (verified)

- `_bmad/` and `_bmad-output/` are listed in `.git/info/exclude` of this checkout (line 18 and 19), so they are NOT tracked in this clone.
- The house precedent for keeping BMAD output is `.dev/issues/<N>/bmad/<artifact>-<slug>/` on `origin/master` (read with `git ls-tree`): issue 409 holds `prd-orca-observer/`, `ux-orca-observer/`, `architecture-orca-observer/`, `spec-orca-observer/` (SPEC.md + 11 companions), `final-review/`, and `handoff-step1.md` to `handoff-step5.md`. Handoff step 5 records "Copy proof: `diff -r` between each Coder folder and its copy here returned exit 0".
- The hand-off to IronClaude in that precedent was a hand-written file, `.dev/issues/409/bmad/final-review/workflow-input.md` (documents to pass with roles, staged-release gating, tasks that can start now, constraints, and one suggested command `/sc:workflow "..." --depth standard --handoff none`). This plan generalises that file into the hand-off packet (S3).
- The observer code and tests are on `origin/master` (`git ls-tree` shows `src/superclaude/cli/observe/` with adapter.py, collector.py, commands.py, export.py, keys.py, questions.py, view.py, `snapshot.schema.json`, and `tests/observe/`), NOT in this working branch (`ironbelly/orch-ledger-20261122`, where `tests/observe` does not exist). Epics that touch the code must start from a worktree based on `origin/master`.
- Deliverables written by agent 1 so far: `agent1/issue-drafts/` (15 epics and 73 feature sub-issues, generated from `agent1/tools/` data; `README.md` there lists them), `agent1/templates/handoff-packet.md`.
- The 409 review was needed: handoff step 5 records "55 blocking found in review 1, 8 new in reviews 2-3, 63 fixed" for the BMAD artifacts. Evidence that a BMAD-only spec needs an independent review before IronClaude builds from it.
## S2. Release map from the owner's roadmap (issue 727, owner text of 2026-11-22)

Order rule from the owner: the architecture and preliminary evaluation (Release 2 prep) take precedence over the release list; nothing is built before the owner says go; each release gets its own issue only when the owner schedules it. So every draft below is `unscheduled` except EPIC-01, which the owner marked first. Reading notes (mine, UNVERIFIED): "1\n5 release" is 1.5; the Zellij and Coder canvas review has no version number in the owner's list, so it sits in the otherwise missing 1.3 slot (EPIC-05) and its outcome feeds 1.4; version numbers such as 1.105 are kept as written. The dashboard release numbers (1.1 to 2.0) are NOT the package version (`pyproject.toml` says 5.0.0; issue 571 plans 6.0.0): where a dashboard "1.1" is tagged or recorded is not known yet (question Q3 in S5).

| Epic | Release | Owner's item (issue 727, paraphrased closely) | Kind of cycle |
|---|---|---|---|
| EPIC-01 | Release 2 prep | Usage and evaluation of the current version; research of requirements, best approaches and similar GitHub projects; state persistence and storage needs of a two-way dashboard; Postgres database per project; session and decision history of all coordinators, vectorised or organised otherwise; Deliverable 1 (review of the release list, `/sc:brainstorm --depth deep` on architecture, data storage, database) | prep (planning only, no code) |
| EPIC-02 | 1.1 | Human validation of all features and desired functionality; file and fix bugs for 1.1 (high and medium) | validation cycle (first) |
| EPIC-03 | 1.105 | Automated tests or CI that would have caught the high and medium bugs without human validation; regression tests | tests cycle |
| EPIC-04 | 1.2 | File feedback from current usage, release 1.2 | feedback release |
| EPIC-05 | 1.3 slot | Review porting the dashboard to Zellij and opening it from the Coder workspace canvas with a new button | decision review |
| EPIC-06 | 1.4 | Planning, testing and integration for 1.4 | build release (conditional on EPIC-05) |
| EPIC-07 | 1.5 | Human testing, bug filing and fixing | validation cycle |
| EPIC-08 | 1.505 | Automated tests or CI, regression tests | tests cycle |
| EPIC-09 | 1.6 | Review additional screens from the first TUI mockups and Clay's HTML dashboards, pick 2 to 4 to recreate in the TUI | build release |
| EPIC-10 | 1.7 | Human testing, bug filing and fixing | validation cycle |
| EPIC-11 | 1.705 | Automated tests or CI, regression tests | tests cycle |
| EPIC-12 | 1.8 | Planning, brainstorming and implementation of the first write and respond features: coordinator needs boiled down to binary or multiple-choice decisions, or a notice that the person is needed in the coordinator session | build release (the big one) |
| EPIC-13 | 1.9 | Human testing, feedback and feature requests, validation, bug filing and fixing | validation cycle |
| EPIC-14 | 1.905 | Automated tests or CI, regression tests | tests cycle |
| EPIC-15 | 2.0 | Implement feedback from 1.9 and additional write and respond features | build release |

Not planned here (owner: "Release 2 and beyond"): user feedback systems that gather data to tune when and how the person is prompted. It is recorded as a closing note in EPIC-15, not as an epic.

Goal text that every epic must keep (owner, issue 727): the dashboard is NOT meant to replace talking to the coordinator sessions; it becomes where decisions are made, with as many coordinator questions as possible reduced to binary or multiple-choice, and when that fails, demands to the coordinator for more context, a better explanation, a debate of several proposals, extra validation, research, fact checking, or use of specific plugins or tools (for example ponytail). Dashboard, watcher and coordinator work are developed together as needed. Facts read in issue 727 for the starting point: the observer (`superclaude observe`) is read-only by design, keeps no database, questions live in process memory, stored files are an export record and a snapshot under the observer state folder; issue 726 (vote on each question) is the first small step and its open decision is whether the read-only rule may be relaxed.
## S3. How epics, features and stories map (agent 1 position, to be debated)

### S3.1 Three layers, three owners

| Layer | GitHub object | BMAD object | Created by | When filed | Who executes |
|---|---|---|---|---|---|
| Epic | issue, child of umbrella 727 (native sub-issue), label `epic` (proposed) | one `Epic N` in the epics file, N = the EPIC number (EPIC-07 = Epic 7) | owner schedules, coordinator files with `/sc:issue --create` | when the owner schedules that release | BMAD planning (people in session) then IronClaude |
| Feature | sub-issue of the epic (native sub-issue; GitHub reports `sub_issues_summary` completed/total, read on issue 727 and 609) | PRD feature group with its FR ids (`bmad-prd`: "Features grouped; FRs nested") | this plan (drafts), coordinator files | together with the epic | its body names the BMAD workflow that starts user-story planning |
| User story | sub-issue of the feature (proposed, filed only at hand-off) | `### Story N.M` in the epics file, key `N-M-title` in `sprint-status.yaml` | `bmad-create-epics-and-stories` (people in session) | at hand-off, not earlier | IronClaude worker (`/sc:issue --claim`, then the IronClaude chain) |

Why stories become issues only at hand-off: the IronClaude pipeline claims GitHub issues (`/sc:issue --claim <N>` assigns, checks accuracy, writes a summary and a next-step prompt, creates an Orca worktree, launches an agent; read in `~/.claude/commands/sc/issue.md`), and filing 15 epics times roughly 5 features times roughly 5 stories of issues before the work is scheduled would bury the board in stale issues. Open for debate with ic-planner (topic e).

### S3.2 Hand-off unit

Position: the unit handed to IronClaude is ONE FEATURE (a batch of its stories, typically 2 to 6), not one story. Reason: `/sc:workflow` produces one phased tasklist package from one source (`/sc:workflow <path-or-prompt> ...`, read in `~/.claude/commands/sc/workflow.md`), `/sc:implement` walks that one tasklist, and the precedent (issue 409 `workflow-input.md`) handed over a set of related tasks in one document. Stories stay the unit of acceptance and of status in the BMAD ledger: each story has its own acceptance rows in the tasklist and is flipped separately. Counter-position expected from ic-planner: per-story hand-off is simpler for write-back.

### S3.3 What BMAD hands over: the hand-off packet (proposed deliverable, one file per feature)

Path: `.dev/issues/<feature-issue-N>/bmad/handoff-<feature-slug>.md` (house precedent: `.dev/issues/409/bmad/` and `workflow-input.md`). Contents, every item a BMAD output that already exists or is a mechanical copy:

1. Feature issue number, epic number, release, FR ids covered.
2. Stories: for each, key (`N-M-title`), the `As a / I want / So that` text and the `Given / When / Then` acceptance criteria copied verbatim from the epics file, and its sprint-status key.
3. Binding documents by role (path, and the rule that on conflict SPEC wins, as in the 409 packet): SPEC.md plus companions; ARCHITECTURE-SPINE.md with the `AD-n` ids that bind this feature (IronClaude must not contradict an `AD`; a needed change goes back up through `bmad-correct-course`); PRD feature group and FRs; UX `DESIGN.md` and `EXPERIENCE.md` when UI is touched; project-context.md.
4. Constraints every plan step must keep (copied from the spec, as the 409 packet did).
5. Staged gates: what may start now and what is blocked on an owner answer.
6. Open questions and UNVERIFIED register entries that touch the feature.
7. The suggested first IronClaude command, using only flags read in the command files (S4.2).
8. Write-back instructions: the sprint-status keys to flip and the GitHub issues to update at each state.

Producing the packet is mechanical, so it is a candidate for a small skill or script (S5 deliverables list).

### S3.4 Five reusable cycle shapes (the roadmap repeats them)

| Shape | Used by | Features (sub-issues) it always has |
|---|---|---|
| Prep | EPIC-01 | evaluation; research; requirements and UX; storage and database architecture; deliverable review; program epics and stories |
| Validation cycle | EPIC-02, 07, 10, 13 | human test pass against the acceptance list; bug filing and triage by severity; fix high and medium bugs; release cut and retrospective |
| Tests cycle | EPIC-03, 08, 11, 14 | gap map (which automated check would have caught each bug); new automated tests; CI additions; regression set for every fixed bug; release cut and retrospective |
| Decision review | EPIC-05 | research; feasibility; go or no-go record by the owner |
| Build release | EPIC-04, 06, 09, 12, 15 | requirements delta; UX/architecture delta; build features; release cut and retrospective |

In the drafts, the Validation and Tests shapes come from two templates so a later release only changes version, inputs and the bug list.

### S3.5 Risks found while reading BMAD (each needs a trial or a decision)

- R1 `bmad-create-epics-and-stories` step 1 copies the template to `{planning_artifacts}/epics.md` with no mention of an existing file (step 1, section 7). A second run for the next release may overwrite the first (not tested, UNVERIFIED). Recipe to trial in EPIC-01: one run per release, rename the result to `epics/epic-NN-<release>.md` plus `epics/index.md` (`bmad-sprint-planning`, `bmad-create-story` and `bmad-correct-course` read sharded `epics/index.md`), and put the epic number in a `persistent_facts` line of `_bmad/custom/bmad-create-epics-and-stories.toml` so numbering does not restart at 1 (numbering restart would collide `epic-1` keys in sprint-status.yaml).
- R2 Stories cannot be written for later releases now: 1.105 depends on the bugs 1.1 finds, 1.2 and 1.9 on feedback. So only EPIC-01 and EPIC-02 get stories at once; the others get stories just in time, when the owner schedules them, from the previous cycle's output. This follows the owner's own rule (each release gets its issue when scheduled).
- R3 `bmad-document-project` writes to `project_knowledge` = `docs/`, the user documentation tree (config, not run here). Not used in this plan; `bmad-generate-project-context` (writes `project-context.md` to `output_folder`) plus `bmad-investigate` on `src/superclaude/cli/observe/` replace it. UNVERIFIED which files DP would touch.
- R4 `_bmad/` is untracked in this clone (`.git/info/exclude`), so team overrides in `_bmad/custom/*.toml` would not be committed. Where team overrides live and how a workspace gets `_bmad/` is not known yet (question Q4).
- R5 Installed BMAD skills ask the user at menus. Anything unattended must be limited to the headless-capable skills (S1.2 point 8).
- R6 `project-context.md` is loaded by default into most BMAD workflows (`persistent_facts` glob over the whole repo). A hand-written copy of CLAUDE.md rules would drift; it should point to CLAUDE.md and list only what BMAD needs (UV only, fork-only PR rule, `.dev/tasks/` staged, no `.claude/` staging).
## S4. Step-by-step invocations

Conventions. A BMAD skill is invoked by typing its skill name as a slash command (the owner writes `/bmad-help`); every BMAD skill is conversational, so the line after it is what you say first. Run each skill in a fresh context window (the `bmad-help` skill says so). Args beyond the ones in the catalog's `args` column (`-A` for the product brief, `-H` for the PRFAQ, `[path]` for the review skills and `bmad-shard-doc`) were not verified. IronClaude command lines use only flags read in the command files' headers: `/sc:brainstorm "<topic>" [--depth quick|standard|deep] [--handoff none|design] [--output DIR] [--unattended --report-dir DIR]`; `/sc:workflow <path-or-prompt> [--depth quick|standard|deep] [--handoff none|design|implement]`; `/sc:implement <path-or-prompt> [--resume] [--ledger <path>] [--skip-final-review]`; `/sc:issue --create "<description or @file>" [--depth quick|standard|deep] [--mode feature|bug] [--type <area>]`; `/sc:closeout <PR> [--issue <N>]`. (`/sc:issue --claim` is NOT used by the agreed v0 pipeline: the coordinator drives stories itself, Mode C.) Flags of `/sc:adversarial`, `/sc:spec-panel` and `/sc:research` were NOT read by me; the lines for spec-panel and adversarial in this plan were read and written by agent 2 (IRONCLAUDE-SIDE.md section 10) and are UNVERIFIED by me.

### S4.1 Program run (EPIC-01, once, people in the session)

| Step | Invocation | Say first | Output | Notes |
|---|---|---|---|---|
| P0 | `/bmad-help` | the roadmap question (done in S1.1) | none | fresh context before each skill |
| P1 | `/bmad-generate-project-context` | "brownfield: IronClaude, focus `src/superclaude/cli/observe/`; point to CLAUDE.md, do not copy it" | `project-context.md` in `_bmad-output/` | later workflows load it by default |
| P2 | `/bmad-investigate` | "map what `superclaude observe` does today and where it stops short of two-way (read-only rule, no database, questions in memory)" | case file in `{implementation_artifacts}/...` | evidence grades Confirmed/Deduced |
| P3 | `/bmad-technical-research` (web search required) | "similar open-source projects for a two-way terminal or web dashboard over agent sessions; storage options" | `{planning_artifacts}/research/technical-<slug>-research-<date>.md` | also `/bmad-market-research` for the comparables |
| P4 | `/bmad-forge-idea` | "the dashboard is where decisions are made; boil coordinator questions down to binary or multiple choice; fallback demands (context, explanation, debate, validation, research, fact check, plugins)" | optional `forged-idea.md` | interactive only |
| P5 | `/bmad-prd` (intent Update) | "update the PRD copied from `.dev/issues/409/bmad/prd-orca-observer/` for the two-way dashboard to 2.0; change signal: issue 727 text" | `prd.md` + `addendum.md` + `.memlog.md` | feature groups and FR ids born here |
| P6 | `/bmad-ux` | "two-way screens: decision card, escalation actions, notification that the person is needed" | `DESIGN.md`, `EXPERIENCE.md` | extends the 409 UX pair |
| P7 | `/bmad-architecture` (intent Update; AD ids stay stable) | "extend the spine for write path, persistence, Postgres per project, cross-coordinator history" | `ARCHITECTURE-SPINE.md` | brainstorm below feeds it |
| P7b | `/sc:brainstorm "architecture, data storage and database needs for releases 1.1 to 2.0 incl. per-project Postgres and vectorised or otherwise organised session and decision history @.dev/issues/727/issue-body.md" --depth deep --research deep --codebase --blind --output <dir>` (run attended; agreed with agent 2 in message 04) | owner's Deliverable 1 | brainstorm package | IronClaude helping BMAD in planning |
| P8 | `/bmad-spec` | "distill PRD, UX, architecture into the SPEC kernel" | `SPEC.md` + companions | derived from memlog, never hand-edited |
| P9 | review gate before hand-off: `/sc:spec-panel` on the SPEC (agent 2 owns the flags) and/or `/bmad-review-adversarial-general [path]`, `/bmad-review-edge-case-hunter [path]` | | review reports | evidence: 409 needed 63 blocking fixes |
| P10 | `/bmad-create-epics-and-stories` | "create epics and stories for EPIC-01 and EPIC-02 only" | epics file | interactive; see risk R1 |
| P11 | `/bmad-check-implementation-readiness` | | readiness report | gate |
| P12 | `/bmad-sprint-planning` | | `sprint-status.yaml` | ledger created |

### S4.2 Per-release loop (general, each build or cycle epic)

| Step | Who | Invocation | Output |
|---|---|---|---|
| L1 orient | person | `/bmad-help` | next step |
| L2 absorb change | person | `/bmad-correct-course` when the previous cycle changed scope; `/bmad-prd` Update when requirements change; `/bmad-architecture` Update when an invariant changes | `sprint-change-proposal-<date>.md`; PRD/spine updates |
| L3 stories | person | `/bmad-create-epics-and-stories` for this release's epic only (R1 recipe) | epic file with stories (BDD) |
| L4 gate | person or unattended worker | `/bmad-check-implementation-readiness` | readiness report |
| L5 ledger | person | `/bmad-sprint-planning` (re-run refreshes; never downgrades) | `sprint-status.yaml` |
| L6 packet | person in the BMAD session (by hand in v0; script only if hand-building loses ids) | build the packet FOLDER per feature from `agent1/templates/handoff-packet.md` v2 | `.dev/issues/<feature-issue>/bmad/INDEX.md` and `story-<N>-<M>-<slug>.md` per story |
| L7 hand-off | IronClaude coordinator (Mode C, shared/CONSENSUS.md (d)) | H1 intake check; on the owner's go file story issues (`/sc:issue --create @<description> --mode feature --type <area> --depth <by complexity>`), link them under the feature issue; create the feature worktree with Orca and the Tasks for each story | accepted packet, story issues, feature worktree |
| L8 spec review (and design only if INDEX marks it open) | IronClaude worker | `/sc:spec-panel @<story file> --mode critique --focus requirements,testing,correctness --unattended --report-dir <D>/panel`; alternate arm only on a trigger: `/sc:brainstorm` plus `/sc:adversarial --compare` (shared/CONSENSUS.md (b)) | panel report |
| L9 plan (per story) | IronClaude worker | `/sc:workflow <story file> --depth <quick or standard> --handoff none --unattended --report-dir <D>/wf`; owner approves the plan in chat | `.dev/tasks/to-do/TASK-WF-<subject>-<YYYYMMDD>-<HHMMSS>/` package |
| L10 build (per story, then per feature) | person today; worker after `/sc:implement` gets an unattended mode | `/sc:implement <plan path>`; after the last story of the feature `/sc:pr-submit --monitor 3` | ledger `progress.md`; one PR per feature on the fork |
| L11 write back | script (to build) | flip sprint-status keys; comment and close story and feature issues; `/sc:closeout <PR> --issue <N>` settles the issue and the work report | ledger and issues current |
| L12 status | person or script | `/bmad-sprint-status` (data mode) | counts and next |
| L13 close epic | person | `/bmad-retrospective` for this epic; open `action_items` become next-cycle inputs | retrospective |

### S4.3 Per epic: features and the first BMAD workflow in each sub-issue

The drafts carry the full text. Summary of the starting workflow per feature (feature = sub-issue):

- EPIC-01: F01 baseline and usage evaluation (`/bmad-generate-project-context` then `/bmad-investigate`); F02 research of requirements, approaches, similar GitHub projects (`/bmad-technical-research`, `/bmad-market-research`); F03 two-way interaction requirements and UX (`/bmad-forge-idea`, `/bmad-prd` Update, `/bmad-ux`); F04 state persistence and storage evaluation (`/bmad-technical-research`, then `/sc:brainstorm --depth deep`); F05 Postgres database per project (`/bmad-architecture` Update); F06 session and decision history across coordinators and developers (`/bmad-technical-research`, `/sc:brainstorm --depth deep`, `/bmad-architecture`); F07 review of the release plan and program epics and stories (`/bmad-create-epics-and-stories`, readiness, sprint planning).
- EPIC-02, 07, 10, 13 (validation cycle): F01 human test pass (`/bmad-spec` or the SPEC acceptance tests as checklist, `/bmad-agent-tech-writer` write-document for the guide); F02 bug filing and triage (`/bmad-investigate` per high or medium bug); F03 fix high and medium bugs (`/bmad-correct-course` if scope moves, then stories via `/bmad-create-epics-and-stories`); F04 release cut and retrospective (`/bmad-retrospective`).
- EPIC-03, 08, 11, 14 (tests cycle): F01 gap map (`/bmad-investigate`, `/bmad-review-edge-case-hunter`); F02 new automated tests; F03 CI additions; F04 regression set; F05 release cut (`/bmad-retrospective`). Whether `/bmad-qa-generate-e2e-tests` is used or IronClaude's own test conventions are used is open (question Q6).
- EPIC-04 (1.2): feedback intake (`/bmad-brainstorming`), triage into the PRD (`/bmad-prd` Update, `/bmad-correct-course`), build the chosen items, cut.
- EPIC-05 (1.3 slot): Zellij feasibility; Coder canvas button; go or no-go record (`/bmad-technical-research`, `/bmad-forge-idea`, `/bmad-architecture`).
- EPIC-06 (1.4): test and integration plan (`/bmad-create-epics-and-stories`, readiness, sprint planning), then build the parts the go record allows.
- EPIC-09 (1.6): screen review and pick of 2 to 4 (`/bmad-ux`), recreate each picked screen, cut.
- EPIC-12 (1.8): write and respond requirements (`/sc:brainstorm`, `/bmad-forge-idea`), boundary change from read-only (`/bmad-prd` Update, `/bmad-architecture` Update), decision cards, escalation demands, notice that the person is needed, vote record (issue 726), persistence, cut.
- EPIC-15 (2.0): feedback absorbed from 1.9 (`/bmad-correct-course`), more write and respond features, cross-coordinator history surfaced, cut.
## S5. Round 0 position summary, questions for the other agent, what I need

### S5.1 My opening positions (to be debated in Round 2; PROTOCOL topics a to g)

- (a) Hand-off: BMAD hands over a FEATURE batch of ready stories after `bmad-check-implementation-readiness` passes and `bmad-sprint-planning` has listed them, through a hand-off packet (S3.3). BMAD does NOT run `bmad-create-story` for them (implementation planning is IronClaude's) and does NOT run `bmad-dev-story`, `bmad-code-review` (IronClaude replaces them). Acceptor: the IronClaude coordinator (accepts the packet into a feature issue) and the claiming worker (checks it against its intake list).
- (b) Spec authorship: default BMAD-only for requirements (PRD, UX, architecture, SPEC, epics and stories), then an independent IronClaude review (`/sc:spec-panel`) before hand-off. Switch to dual authorship (`/sc:brainstorm` design from IronClaude, `/sc:adversarial` merge with the BMAD spec) only for high-risk features: EPIC-01 storage and Postgres, EPIC-05 go or no-go, EPIC-12 first write path.
- (c) Progress back: a small write-back script copies the idempotent, never-regress behaviour of `bmad-quick-dev/sync-sprint-status.md` to flip `sprint-status.yaml` keys at claim, PR open, PR merged; plus issue comments and closure; GitHub's own sub-issue counter gives the rollup. `/bmad-sprint-status` (data mode) and `/bmad-retrospective` read it.
- (d) Coordinator: BMAD planning sessions are attended by the owner (menus, approvals), one planning worktree per release; IronClaude execution is unattended, one worktree per feature, features run in parallel when their stories do not depend on each other and in sequence otherwise. The coordinator preps (inputs, packet), dispatches, waits, writes back, and never answers a BMAD menu.
- (e) GitHub: epics and features are filed when scheduled; stories at hand-off; every state change leaves a comment; native sub-issues give the progress bar.
- (f) BMAD owns what and why: product brief, PRD, UX, architecture invariants (`AD-n`), spec, epics, stories, acceptance criteria, order, the ledger. IronClaude owns how and when: design, tasklist, code, tests, review, PR, CI, closeout, rapid iteration. IronClaude may not contradict an `AD`; a needed change goes up through `/bmad-correct-course`.
- (g) Reusable: already exists, all BMAD skills (installed, BMAD 6.9.0), `.dev/issues/409/bmad/` as a worked example, IronClaude `/sc:issue`, `/sc:brainstorm`, `/sc:workflow`, `/sc:implement`, `/sc:closeout`, `/sc:pr-submit`, agents `issue-worker-t1..t3`. To build (proposed): hand-off packet skill or script, write-back script, issue-draft generator and templates (a start is in `agent1/issue-drafts/`), `_bmad/custom/*.toml` overrides, release-planner agent.

### S5.2 Questions for the other agent (ic-planner)

1. (a) Can one `/sc:workflow` run turn a packet of 2 to 6 stories (one feature) into one coherent tasklist, or does IronClaude want one story per run? What size limit have you seen?
2. (a) What must a packet contain for the IronClaude coordinator or worker to accept it, and what makes them reject it? Give your acceptance checklist; I will fold it into the packet template.
3. (a) Does IronClaude already add its own implementation-context work that duplicates `bmad-create-story` (architecture extraction, files to touch, previous-story learnings), so that skipping CS loses nothing?
4. (b) Do you agree with BMAD-only plus `/sc:spec-panel` as the default, dual authorship only for the three high-risk features? What are the real command lines and costs of `/sc:spec-panel`, `/sc:brainstorm` and `/sc:adversarial` on a SPEC folder of a dozen files?
5. (c) `_bmad-output/` is untracked per checkout and workers run in separate Orca worktrees. Which worktree holds the single `sprint-status.yaml` ledger, and who writes it: the coordinator after `worker_done`, or each worker? Could `/sc:closeout` carry the write-back step?
6. (d) Can the coordinator launch an attended BMAD session (owner present, menus) as a managed Claude CLI session, and what does the coordinator do while it waits? How many planning sessions and execution workers can run in parallel under the current coordinator rules and the issue watcher?
7. (e) Which tool files the epic, feature and story issues and links them as native sub-issues (I only read that the API returns `sub_issues_summary`)? Is `/sc:issue --create` (feature template, issue type Feature, Complexity field) the right way, or the ISSUE-BACKLOG shape?
8. (f) Do you accept the rule that IronClaude must not contradict an architecture `AD-n` and sends change requests through `/bmad-correct-course`?
9. (g) Which pieces of the proposed "to build" list already exist in IronClaude (any script that edits issue bodies, any ledger code), so I do not propose duplicates?
10. Does IronClaude want `/bmad-qa-generate-e2e-tests` (QA) for the tests cycles, or its own test conventions (`uv run pytest`, `tests/observe/`)?
11. Where is a dashboard release "1.1" recorded (tag, docs, version string)? The package is 5.0.0.

### S5.3 What I need from the other agent

- N1 The IronClaude intake steps after the hand-off with real command lines (brainstorm, adversarial, workflow, implement), flags verified in the command files.
- N2 The coordinator and session topology design (worktrees, sessions, sequential versus parallel, who files issues).
- N3 The write-back events available on the IronClaude side (what fires at claim, PR open, merge, closeout) and where the write-back script can hook.
- N4 The `/sc:recommend` result and its reasoning for the owner's goal.
- N5 A decision on question 1 (hand-off unit) and 5 (ledger home), because both change my drafts.

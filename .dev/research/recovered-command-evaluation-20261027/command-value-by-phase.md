# Command Value by Phase

**Generated**: 2026-10-27 by command-value-analyst (read-only analysis; only this file written)
**Method**: /sc:analyze skill invoked and followed (Discover, Scan, Evaluate, Recommend, Report). It ran normally.
**Source rule**: every description below is taken from the file on disk. Anything not confirmed from a file is marked UNVERIFIED.
**Rating scale**: REQUIRED / WORTH IT / OPTIONAL / SKIP
**Work sizes (column order)**: one-off task (T), bug fix (B), single story (S), multi-story feature (F), multi-feature release (R), new product (N). R (Ryan, 2026-10-27) means a multi-feature release: a full release plan, its implementation and the push. It is one step below greenfield new product (N). A single feature's release is a phase inside S or F, not R.

> **Banner (2026-10-27):** the R column in Section 2 was rated under the older reading of "release" ("a release assembles and ships work already built") and has NOT been re-rated in place. Re-rating proposals, together with the complexity layer, are in Section 6 (see 6.2).

<!-- SECTION 1: inventory and exclusions -->
## 1. Inventory and exclusions

### Where the commands actually live (verified on disk)

| Location | What is there | Count |
|---|---|---|
| Repo `.claude/skills/*/SKILL.md` | `bmad-*` (47) and `openspec-*` (10) | 57 |
| Repo `.claude/commands/opsx/*.md` | `opsx:*` slash-command forms of the OpenSpec skills | 10 |
| User-level `~/.claude/commands/sc/*.md` | `sc:*` commands (NOT in the repo) | 43 |
| User-level `~/.claude/skills/` | `task-builder`, `task`, `tdd`, `prd`, `roadmap`, `tech-research`, `tech-reference`, `confidence-check`, `operational-guide`, `readme`, plus `sc-*` backing skills (NOT in the repo) | n/a |
| User-level `~/.claude/HOW-WE-WORK.md` | The team's own routing guide: six process levels, workflows 3.1-3.12, routing table. Its text is the main evidence for the ratings below. | 1 file |
| Built-ins (not files) | `/code-review`, `/security-review`, `/simplify`: named in the routing guide and the session skill list; no file to read | 3 |

Consequence for the checker job: `sc:*`, `task-builder`, `task`, `prd`, `tdd`, `roadmap` exist only in each engineer's home directory. Only the BMad and OpenSpec sets are guaranteed by the repo.

Repo evidence of which lanes are used (counted on disk, 2026-10-27):
- BMad lane: `_bmad-output/planning-artifacts/` holds `prd.md`, `architecture.md`, `epics*.md` (incl. `epics-micro-first.md`), four `implementation-readiness-report-*.md`; `_bmad-output/implementation-artifacts/` holds story files (`1-1-*.md`).
- Task-file lane (task-builder / task): `.dev/tasks/to-do` has 20 entries, `.dev/tasks/done` has 33.
- OpenSpec lane: `openspec/changes/` has one entry (`template-comprehensive-refactor`). Barely used.

### Inventoried commands (names only; purposes and ratings are in Section 2)

**SuperClaude commands (`/sc:`)**: brainstorm, design, spec-panel, research, adversarial, release-split, workflow, roadmap, tasklist, validate-roadmap, reflect, implement, task, test, build, improve, cleanup, cleanup-audit, spawn, git, auggie-review, pr-submit, troubleshoot, analyze, explain, document, post-release, tdd (alias of `/tdd`), swarm-wizard, recommend, help.

**Task-file skills**: `/prd`, `/tdd`, `/roadmap`, `/task-builder`, `/task`, `/tech-research`, `/tech-reference`, `/operational-guide`, `/readme`, `/confidence-check`.

**Built-ins**: `/code-review`, `/security-review`, `/simplify`.

**BMad (`bmad-*`)**: product-brief, prfaq, brainstorming, forge-idea, party-mode, advanced-elicitation, market-research, domain-research, technical-research, prd, ux, architecture, spec, create-epics-and-stories, check-implementation-readiness, sprint-planning, sprint-status, create-story, dev-story, quick-dev, dev-auto, code-review, checkpoint-preview, qa-generate-e2e-tests, retrospective, correct-course, investigate, review-adversarial-general, review-edge-case-hunter, editorial-review-prose, editorial-review-structure, document-project, generate-project-context, agent-analyst, agent-architect, agent-dev, agent-pm, agent-tech-writer, agent-ux-designer, help; deprecated: create-prd, edit-prd, validate-prd, create-architecture.

**OpenSpec**: `openspec-{explore, new-change, continue-change, ff-change, apply-change, verify-change, sync-specs, archive-change, bulk-archive-change, onboard}` and their 10 `opsx:*` twins (explore, new, continue, ff, apply, verify, sync, archive, bulk-archive, onboard).

### Exclusions (one line)

Excluded as not SDLC-relevant: Notion:*, dropbox:*, google-cloud-storage:*, understand-anything:*, frontend-design, update-config, keybindings-help, loop, claude-api, dataviz, artifact-*, plugin-authoring, ccsession-tag, computer-use, orca-cli, orchestration, run, init, fewer-permission-prompts, workflow-authoring, sc-crash-recovery, sc-bare-review, the `sc-*-protocol` backing skills (loaded by their `/sc:` command), `/sc:agent` and `/sc:business-panel` (no frontmatter, so no description to verify; business strategy, not code), `/sc:pm`, `/sc:load`, `/sc:save`, `/sc:index`, `/sc:index-repo`, `/sc:init-lite` (the routing guide says prefer its levels, or that they are not pipeline or resume steps), `/sc:cli-eval`, `/sc:cli-portify`, `/sc:review-translation`, `/sc:validate-tests` (IronClaude contributor tools), `bmad-customize`, `bmad-index-docs`, `bmad-shard-doc` (document tooling).

### Rating rules used in every table

- Columns: **T** one-off task, **B** bug fix, **S** single story, **F** multi-story feature, **R** multi-feature release (a full release plan, implementation and push; one step below N; a single feature's release is a phase inside S or F, not R; the R cells were rated under the older reading, see the banner at the top and Section 6.2), **N** new product.
- Values: REQUIRED / WORTH IT / OPTIONAL / SKIP.
- `‡` in Notes = one of a pair or lane: two commands do the same job and the team does one of them. Both carry the rating; running both is waste (see Section 3).
- Ratings come from (a) the command's own description, (b) `HOW-WE-WORK.md` routing text and routing table, (c) `_bmad/_config/bmad-help.csv` (`required=true` flag and phase). Where a rating is my judgment and not stated in any of those, the Notes column says "judgment".
- "Sizes" assume the work changes tracked files. A pure question is level 1 in the guide and needs no pipeline.
- Each command has one row, in its primary phase. Secondary phases are named in its Notes.

<!-- SECTION 2: per-phase tables -->
## 2. Per-phase tables

### 2.1 Phase: Spec (shape the idea, requirements, design)

**Task-file / SuperClaude lane**

| Command | Purpose (from its own description) | T | B | S | F | R | N | Notes |
|---|---|---|---|---|---|---|---|---|
| `/sc:brainstorm` | Orchestrated multi-agent brainstorm: Socratic dialogue + parallel proposals + adversarial merge | SKIP | SKIP | OPTIONAL | WORTH IT | OPTIONAL | WORTH IT | Guide: "only if the idea is still vague". `--handoff task` goes straight to a task file. ‡ with `bmad-brainstorming` |
| `/sc:design` | Design system architecture, APIs, and component interfaces with comprehensive specifications | SKIP | SKIP | SKIP | OPTIONAL | SKIP | OPTIONAL | Single-pass draft of one API/component (guide section 5). Use for a new interface inside a spec file. ‡ with `/tdd` |
| `/sc:spec-panel` | Multi-expert specification review and improvement using renowned specification and software engineering experts | SKIP | SKIP | OPTIONAL | WORTH IT | OPTIONAL | REQUIRED | Guide full-spec steps 3 and 5 (`--mode critique`). Report only. Also a Review-phase tool |
| `/prd` | Create or populate a Product Requirements Document (PRD) for a product, feature, or platform | SKIP | SKIP | SKIP | OPTIONAL | SKIP | REQUIRED | Guide level 6. F: guide 3.2 says a short spec file is enough when requirements are clear. ‡ with `bmad-prd` |
| `/tdd` (= `/sc:tdd`) | Create or populate a Technical Design Document (TDD) for a component, service, or system | SKIP | SKIP | SKIP | OPTIONAL | SKIP | REQUIRED | Guide level 6. Not test-driven development. Use when others build against the design. ‡ with `bmad-architecture` |
| `/tech-research` | Deep technical investigation and feasibility research across the codebase | SKIP | SKIP | OPTIONAL | WORTH IT | OPTIONAL | WORTH IT | Guide level 5: use when you do not yet know how the current system works. Bug work uses `/sc:troubleshoot` instead |
| `/sc:research` | Deep web research with adaptive planning and intelligent search | SKIP | SKIP | OPTIONAL | OPTIONAL | SKIP | WORTH IT | Outside knowledge only (library, standard). `/tech-research` is for our code |
| `/sc:adversarial` | Structured adversarial debate, comparison, and merge pipeline for 2-10 artifacts | SKIP | SKIP | SKIP | OPTIONAL | SKIP | OPTIONAL | Only when two or more competing designs exist |
| `/sc:release-split` | Neutral two-phase release split analysis with adversarial validation and fidelity verification | SKIP | SKIP | SKIP | OPTIONAL | WORTH IT | OPTIONAL | Guide step 6 of full-spec: optional; "do not split" is a normal answer. Judgment: WORTH IT only at release size |
| `/confidence-check` | Pre-implementation confidence assessment (>=90% required): duplicate check, architecture compliance, docs verification, root cause identification | SKIP | SKIP | OPTIONAL | WORTH IT | OPTIONAL | WORTH IT | Guide names it as the readiness check before an implementation. Judgment on sizes. Also a Review/Validate tool |

**BMad lane (repo-installed)**

| Command | Purpose (from its own description) | T | B | S | F | R | N | Notes |
|---|---|---|---|---|---|---|---|---|
| `bmad-brainstorming` | Facilitate a brainstorming session using diverse creative techniques | SKIP | SKIP | OPTIONAL | WORTH IT | OPTIONAL | WORTH IT | `bmad-help.csv`: phase 1-analysis, required=false. ‡ with `/sc:brainstorm` |
| `bmad-forge-idea` | Pressure-test an idea through persona-driven interrogation until it hardens, proves out, or dies cheaply | SKIP | SKIP | SKIP | OPTIONAL | SKIP | OPTIONAL | csv: anytime, required=false. Idea stage only |
| `bmad-prfaq` | Working Backwards PRFAQ challenge that stress-tests a product concept customer-first | SKIP | SKIP | SKIP | SKIP | SKIP | OPTIONAL | csv: 1-analysis, required=false |
| `bmad-product-brief` | Create, update, or validate a product brief | SKIP | SKIP | SKIP | OPTIONAL | SKIP | WORTH IT | csv: 1-analysis, required=false; precedes `bmad-prd` |
| `bmad-market-research` | Conduct market research on competition and customers | SKIP | SKIP | SKIP | SKIP | SKIP | OPTIONAL | csv: 1-analysis, required=false. Product-market question, not engineering |
| `bmad-domain-research` | Conduct domain and industry research | SKIP | SKIP | SKIP | SKIP | SKIP | OPTIONAL | csv: 1-analysis, required=false |
| `bmad-technical-research` | Conduct technical research on technologies and architecture | SKIP | SKIP | SKIP | OPTIONAL | SKIP | OPTIONAL | csv: "feasibility, architecture options, implementation approach". Whether it searches the web or the codebase is UNVERIFIED. Partly overlaps `/tech-research` and `/sc:research` |
| `bmad-prd` | Create, update, or validate a PRD | SKIP | SKIP | SKIP | OPTIONAL | SKIP | REQUIRED | csv: 2-planning, required=true. Absorbs the deprecated create/edit/validate PRD skills. ‡ with `/prd` |
| `bmad-ux` | Plan UX patterns and design specifications | SKIP | SKIP | SKIP | OPTIONAL | SKIP | OPTIONAL | csv: 2-planning, required=false, "strongly recommended" if there is a UI. Whether this team's products have a UI is UNVERIFIED |
| `bmad-architecture` | Produce the architecture: a lean spine of invariants that keeps everything built from it consistent | SKIP | SKIP | SKIP | OPTIONAL | SKIP | REQUIRED | csv: 3-solutioning, required=true. Replaces deprecated `bmad-create-architecture`. ‡ with `/tdd` |
| `bmad-spec` | Distill any intent input into the SPEC kernel + companions, the preservation-validated machine contract for downstream work | SKIP | SKIP | SKIP | OPTIONAL | SKIP | OPTIONAL | csv: anytime, required=false. Which downstream command consumes the SPEC kernel is UNVERIFIED (not checked in the skill body) |
| `bmad-party-mode` | Orchestrates group discussions between installed BMAD agents or custom personas | SKIP | SKIP | SKIP | OPTIONAL | SKIP | OPTIONAL | Discussion aid, no artifact in the csv |
| `bmad-agent-analyst`, `-architect`, `-pm`, `-ux-designer` | Persona entry points (Mary, Winston, John, Sally) for analysis, architecture, PRD, UX work | SKIP | SKIP | OPTIONAL | OPTIONAL | SKIP | OPTIONAL | Wrappers to talk to a persona, not separate pipeline steps. Content of what each wraps is UNVERIFIED |
| `bmad-document-project` | Document brownfield projects for AI context | SKIP | SKIP | SKIP | OPTIONAL | SKIP | OPTIONAL | csv: anytime. Judgment: repo already has `_bmad-output/project-context.md` |
| `bmad-generate-project-context` | Create project-context.md with AI rules | SKIP | SKIP | SKIP | OPTIONAL | SKIP | OPTIONAL | csv: anytime. Re-run only when stale |
| `bmad-advanced-elicitation` | Push the LLM to reconsider, refine, and improve its recent output (socratic, first principles, pre-mortem, red team) | SKIP | SKIP | SKIP | OPTIONAL | SKIP | OPTIONAL | Also a Review tool |

**OpenSpec lane (third lane; not in Ryan's pipelines)**

| Command | Purpose (from its own description) | T | B | S | F | R | N | Notes |
|---|---|---|---|---|---|---|---|---|
| `openspec-explore` = `opsx:explore` | Enter explore mode: a thinking partner for exploring ideas, investigating problems, and clarifying requirements | SKIP | SKIP | SKIP | SKIP | SKIP | SKIP | ‡ with `/sc:brainstorm`. judgment: only one change dir in repo |
| `openspec-new-change` = `opsx:new` | Start a new OpenSpec change using the experimental artifact workflow | SKIP | SKIP | SKIP | SKIP | SKIP | SKIP | Own artifact flow; duplicates the Spec + Tasklist phases. See Section 3 |
| `openspec-continue-change` = `opsx:continue` | Continue working on an OpenSpec change by creating the next artifact | SKIP | SKIP | SKIP | SKIP | SKIP | SKIP | Same |
| `openspec-ff-change` = `opsx:ff` | Fast-forward through OpenSpec artifact creation | SKIP | SKIP | SKIP | SKIP | SKIP | SKIP | Same |
| `openspec-onboard` = `opsx:onboard` | Guided onboarding walkthrough of a complete OpenSpec workflow cycle | SKIP | SKIP | SKIP | SKIP | SKIP | SKIP | Training only |

### 2.2 Phase: Tasklist (turn a spec or request into steps someone can execute)

| Command | Purpose (from its own description) | T | B | S | F | R | N | Notes |
|---|---|---|---|---|---|---|---|---|
| `/sc:workflow` | Generate a phased implementation plan from a PRD, spec, or feature prompt | SKIP | OPTIONAL | REQUIRED | OPTIONAL | OPTIONAL | SKIP | Guide level 3: `--depth quick`; plan is auto-checked against the request; output `.dev/tasks/to-do/<id>/<id>.md`; run with `/sc:implement`, never `/task`. B: only when the fix spans a few files. ‡ with `/task-builder` |
| `/task-builder` | Build MDTM task files from user requests via parallel codebase research, quality gates, and automated task file creation | SKIP | OPTIONAL | WORTH IT | REQUIRED | WORTH IT | WORTH IT | Guide level 4. Add `--spec <path>` so the file is checked against the spec (`reflect_pre`). N: normally invoked by `/roadmap`. B: larger or riskier fix. ‡ with `/sc:workflow` |
| `/roadmap` | Create a phased implementation roadmap from any input; produces roadmap, BUILD_REQUEST files, and MDTM task files by composing `/task-builder` and `/task` | SKIP | SKIP | SKIP | OPTIONAL | WORTH IT | REQUIRED | Guide level 6 step 7. Ask for a "full roadmap" or it stops at build requests. Runs at deepest setting by default |
| `/sc:roadmap` | Generate roadmap pipeline artifacts from 1-3 spec, TDD, and PRD inputs; mirrors the CLI `superclaude roadmap run` | SKIP | SKIP | SKIP | SKIP | OPTIONAL | OPTIONAL | Guide section 5: belongs to a separate release pipeline (`/sc:tasklist`, then `superclaude sprint run`). Use `/roadmap` unless the lead says otherwise. ‡ with `/roadmap`. Note: `/sc:tasklist` named here is retired (Ryan), see its row. |
| `/sc:tasklist` | Generate deterministic, Sprint CLI-compatible tasklist bundles from roadmaps with integrated roadmap validation | SKIP | SKIP | SKIP | SKIP | SKIP | SKIP | Retired (Ryan). Only programmatic caller: /sc:tasklist Stage 9 calls /sc:task. |
| `/sc:spawn` | Meta-system task orchestration with intelligent breakdown and delegation | SKIP | SKIP | SKIP | SKIP | SKIP | SKIP | Guide "Other commands": for work that changes code, prefer `/task-builder` |
| `bmad-create-epics-and-stories` | Break requirements into epics and user stories | SKIP | SKIP | SKIP | REQUIRED | WORTH IT | REQUIRED | csv: 3-solutioning, required=true; preceded by `bmad-architecture`. BMad lane only. ‡ with `/task-builder` + `/roadmap` |
| `bmad-sprint-planning` | Generate sprint status tracking from epics | SKIP | SKIP | OPTIONAL | REQUIRED | WORTH IT | REQUIRED | csv: 4-implementation, required=true. `bmad-dev-story` implements "the next story in the sprint plan". BMad lane only |
| `bmad-create-story` | Creates a dedicated story file with all the context the agent will need to implement it later | SKIP | SKIP | REQUIRED | REQUIRED | WORTH IT | REQUIRED | csv: 4-implementation, required=true; has a `validate` action that precedes `bmad-dev-story`. Output: `implementation_artifacts`. ‡ with `/sc:workflow` for the single-story case |

### 2.3 Phase: Review / Revise / Validate (plans, specs, and finished work against the plan)

| Command | Purpose (from its own description) | T | B | S | F | R | N | Notes |
|---|---|---|---|---|---|---|---|---|
| `/sc:reflect` | Tiered reflection: pre-execution coverage/gap audit (`--mode pre`) and post-execution deviation audit (`--mode post`) with evidence-validator gate | SKIP | SKIP | OPTIONAL | WORTH IT | REQUIRED | REQUIRED | Guide 3.1 step 9: after each `/task` phase run `--mode post ... --diff <one commit> --no-promote` because `/task` does not commit. `--mode pre` only when `reflect_pre` verdict is `skipped` or the plan is hand-written. S: `/sc:workflow` already self-checked |
| `/sc:validate-roadmap` | Validate roadmap pipeline outputs (roadmap.md, test-strategy.md, extraction.md) produced by `superclaude roadmap run` | SKIP | SKIP | SKIP | SKIP | OPTIONAL | OPTIONAL | Only in the separate `/sc:roadmap` pipeline. `/roadmap` runs its own QA |
| `bmad-check-implementation-readiness` | Validate PRD, UX, Architecture and Epics specs are complete | SKIP | SKIP | SKIP | WORTH IT | WORTH IT | REQUIRED | csv: 3-solutioning, required=true; preceded by epics. Repo has 4 readiness reports, so the team already runs it |
| `bmad-review-adversarial-general` | Perform a Cynical Review and produce a findings report | SKIP | SKIP | OPTIONAL | OPTIONAL | OPTIONAL | OPTIONAL | csv: anytime, "for quality assurance or before finalizing deliverables". ‡ with `/sc:spec-panel` for specs, `/code-review` for code |
| `bmad-review-edge-case-hunter` | Walk every branching path and boundary condition, report only unhandled edge cases | SKIP | OPTIONAL | OPTIONAL | OPTIONAL | SKIP | OPTIONAL | csv: "use alongside adversarial review". B: after a fix to probe boundaries |
| `bmad-editorial-review-prose` | Clinical copy-editor that reviews text for communication issues | SKIP | SKIP | SKIP | OPTIONAL | OPTIONAL | OPTIONAL | Doc polish only |
| `bmad-editorial-review-structure` | Structural editor that proposes cuts, reorganization, and simplification while preserving comprehension | SKIP | SKIP | SKIP | OPTIONAL | OPTIONAL | OPTIONAL | Doc polish only |
| `bmad-correct-course` | Manage significant changes during sprint execution | SKIP | SKIP | SKIP | OPTIONAL | OPTIONAL | OPTIONAL | csv: anytime; output a change proposal in `planning_artifacts`. Becomes the right step only when scope changes mid-sprint; unconditional value is low |
| `/sc:swarm-wizard` | Plain-language interactive guide to the `superclaude swarm` CLI: reviewers from other AI model families | SKIP | SKIP | SKIP | OPTIONAL | OPTIONAL | OPTIONAL | Guide 3.6: real runs need a model proxy set in `~/.aienv` (`T2ProxyUrl`, `T2ProxyKey`, `T2Model01`). Whether it is configured here is UNVERIFIED |
| `openspec-verify-change` = `opsx:verify` | Verify implementation matches change artifacts | SKIP | SKIP | SKIP | SKIP | SKIP | SKIP | OpenSpec lane only |

Also used in this phase (rated in their home tables): `/sc:spec-panel`, `bmad-advanced-elicitation`, `/confidence-check` (2.1); `/code-review`, `/security-review`, `/sc:auggie-review`, `bmad-code-review` (2.5).

### 2.4 Phase: Implement

Reading of the R column in this phase (rewritten 2026-10-27 per Ryan): R means a multi-feature release, which includes the full release plan, its implementation and the push, one step below a new product (N). A single feature's release is a phase inside S or F, not R. The R cells in the table below were rated under the older reading ("a release assembles and ships work already built at story or feature size, so build-the-code commands rate SKIP for R unless they check the assembled result") and have NOT been re-rated in place; re-rating proposals are in Section 6.2.

| Command | Purpose (from its own description) | T | B | S | F | R | N | Notes |
|---|---|---|---|---|---|---|---|---|
| `/sc:implement` | Middleweight spec executor: walk a spec/PRD/tasklist, per-task spec-compliance QA, one-line ledger | SKIP | OPTIONAL | REQUIRED | OPTIONAL | SKIP | SKIP | Runs `/sc:workflow` plans (`TASK-WF-*`). Resumes from first unfinished step. Stops with `E-HALT-QA` after two failed step checks. ‡ with `/task` |
| `/task` | Execute an MDTM task file: checklist items in order, subagents where needed, progress tracked in frontmatter and task log | SKIP | OPTIONAL | WORTH IT | REQUIRED | SKIP | REQUIRED | Runs `/task-builder` files. Has reviewer panels after each phase except setup, tests, and a final audit. Does not commit. Never tick items by hand. ‡ with `/sc:implement` |
| `/sc:task` | Unified task execution with intelligent workflow management, MCP compliance enforcement, and multi-agent delegation | SKIP | SKIP | SKIP | SKIP | SKIP | SKIP | Retired (Ryan). Only programmatic caller: /sc:tasklist Stage 9 calls /sc:task. |
| `bmad-dev-story` | Execute story implementation following a context filled story spec file | SKIP | SKIP | REQUIRED | REQUIRED | SKIP | REQUIRED | csv: 4-implementation, required=true; preceded by `bmad-create-story` validate. BMad lane only. ‡ with `/sc:implement` and `/task` |
| `bmad-quick-dev` | Implements any user intent, requirement, story, bug fix or change request, following the project's existing architecture and conventions | WORTH IT | WORTH IT | OPTIONAL | SKIP | SKIP | SKIP | csv: anytime; output spec + implementation in `implementation_artifacts`. BMad-lane substitute for `/sc:task` on small work. ‡ with `/sc:task`. Note: `/sc:task` is retired (Ryan), see its row in this table. |
| `bmad-dev-auto` | One iteration of an unattended development loop (its body: turn intent into a reviewable artifact without human interaction) | SKIP | SKIP | OPTIONAL | OPTIONAL | SKIP | SKIP | Not in `bmad-help.csv`. "Use when invoked by name". Conflicts in spirit with "do not push without approval" if it is allowed to push: UNVERIFIED whether it pushes |
| `bmad-agent-dev` | Senior software engineer persona (Amelia) for story execution and code implementation | SKIP | SKIP | OPTIONAL | OPTIONAL | SKIP | OPTIONAL | Persona wrapper; do not run alongside `bmad-dev-story` for the same story |
| `/sc:test` | Execute tests with coverage analysis and automated quality reporting | WORTH IT | WORTH IT | WORTH IT | OPTIONAL | WORTH IT | OPTIONAL | Running the related test is mandatory in the guide (levels 2, 3, bug route 3a); this command is one way. F: `/task` runs tests itself. Does not write tests. Also in Bug-fix phase |
| `bmad-qa-generate-e2e-tests` | Generate end to end automated tests for existing features | SKIP | SKIP | OPTIONAL | WORTH IT | WORTH IT | WORTH IT | csv: 4-implementation, required=false; "NOT for code review". Judgment on sizes |
| `/sc:build` | Build, compile, and package projects with intelligent error handling and optimization | SKIP | SKIP | OPTIONAL | OPTIONAL | OPTIONAL | OPTIONAL | Guide: "Build or package the project". `CLAUDE.md` says validation goes through `.github` Actions; local build is a convenience, CI is the gate |
| `/sc:improve` | Apply systematic improvements to code quality, performance, and maintainability | SKIP | SKIP | OPTIONAL | OPTIONAL | SKIP | SKIP | Guide 3.7: commit first, `--safe --interactive`, review `git diff`. The one allowed exception to the five-edit limit |
| `/sc:cleanup` | Systematically clean up code, remove dead code, and optimize project structure | SKIP | SKIP | OPTIONAL | OPTIONAL | OPTIONAL | SKIP | Same guard rails as `/sc:improve` |
| `/sc:cleanup-audit` | Multi-pass read-only repository audit producing evidence-backed cleanup recommendations | SKIP | SKIP | SKIP | OPTIONAL | OPTIONAL | SKIP | Report only (`--pass all`); run before `/sc:cleanup` |
| `/simplify` | Review the changed code for reuse, simplification, efficiency, and altitude cleanups, then apply the fixes | SKIP | SKIP | OPTIONAL | OPTIONAL | SKIP | SKIP | Built-in, no file to read. Edits code, so run before the commit, not after review |
| `openspec-apply-change` = `opsx:apply` | Implement tasks from an OpenSpec change | SKIP | SKIP | SKIP | SKIP | SKIP | SKIP | OpenSpec lane only |

### 2.5 Phase: Commit / Push / PR (including review before push)

| Command | Purpose (from its own description) | T | B | S | F | R | N | Notes |
|---|---|---|---|---|---|---|---|---|
| `/sc:git` | Git operations with intelligent commit messages and workflow optimization | OPTIONAL | OPTIONAL | OPTIONAL | OPTIONAL | OPTIONAL | OPTIONAL | Committing regularly is mandatory (Ryan, pipeline step 4); plain `git` does the same. Guide: "never push without approval". How `--smart-commit` treats `.dev/tasks` (which `CLAUDE.md` says must always be staged) is UNVERIFIED |
| `/code-review` | Review the current diff, or a PR/branch/path, for correctness bugs at a chosen effort level | OPTIONAL | WORTH IT | REQUIRED | REQUIRED | REQUIRED | REQUIRED | Guide 3.11 step 2, unconditional; catches bugs the per-step reviewer does not. Built-in. ‡ with `bmad-code-review` |
| `/security-review` | Security review of pending changes (built-in) | OPTIONAL | OPTIONAL | OPTIONAL | WORTH IT | WORTH IT | WORTH IT | Guide step 3: required when login, permissions, secrets, user input, or file paths changed. This repo's `CLAUDE.md` has a secrets incident history, so treat any env/secret-path change as that trigger. Description taken from guide; no file |
| `/sc:auggie-review` | Auggie-powered code review for PRs, local diffs, or file snapshots: narrow bugs, architectural risks, anti-patterns, optional remediation handoff | SKIP | OPTIONAL | WORTH IT | WORTH IT | WORTH IT | WORTH IT | Guide step 4: `--diff origin/<main>...HEAD --no-post-pr`. Default on a PR number posts publicly. Judgment: WORTH IT, not REQUIRED, because it overlaps `/code-review` and the PR bot |
| `/sc:pr-submit` | Open a PR on the fork and arm an in-session PR-review auto-remediation monitor | REQUIRED | REQUIRED | REQUIRED | REQUIRED | REQUIRED | REQUIRED | Ryan's pipeline step 4. Always pass `--monitor 1` (default is 2, which edits code; 3 pushes). Needs `gh` logged in and the Augment review app; app presence is UNVERIFIED, else `--monitor 0` |
| `bmad-code-review` | Review code changes adversarially using parallel review layers (Blind Hunter, Edge Case Hunter, Acceptance Auditor) with structured triage | SKIP | OPTIONAL | REQUIRED | REQUIRED | OPTIONAL | REQUIRED | csv: follows `bmad-dev-story`; sends issues back to dev-story. BMad lane. ‡ with `/code-review` |
| `bmad-checkpoint-preview` | LLM-assisted human-in-the-loop review: make sense of a change, focus attention where it matters, test | SKIP | SKIP | OPTIONAL | WORTH IT | WORTH IT | WORTH IT | csv: 4-implementation, required=false. Fits "show your lead what changed before push". Judgment on sizes |

### 2.6 Phase: Bug fix / Troubleshoot

| Command | Purpose (from its own description) | T | B | S | F | R | N | Notes |
|---|---|---|---|---|---|---|---|---|
| `/sc:troubleshoot` | Tiered debugging: Tier 1 triage with auggie + serena grounding, auto-escalation to parallel hypothesis agents + adversarial fix debate, opt-in remediation chain | OPTIONAL | REQUIRED | OPTIONAL | OPTIONAL | OPTIONAL | SKIP | Ryan's pipeline step 5. Flags verified in the command file: `--type bug\|build\|performance\|deployment\|security\|test`, `--depth quick\|standard\|deep`, `--fix`. Diagnoses only; writes `.dev/troubleshoot/<name>-<timestamp>/REPORT.md`. Give it the exact error and reproduction. S/F: when a failing test or build stops a story |
| `bmad-investigate` | Forensic case investigation with evidence-graded findings; investigate a bug, trace an incident, or build a mental model of a code area | SKIP | OPTIONAL | OPTIONAL | OPTIONAL | SKIP | SKIP | Not in `bmad-help.csv`. Produces a case file. ‡ with `/sc:troubleshoot` for bugs |
| `/sc:analyze` | Comprehensive code analysis across quality, security, performance, and architecture domains | SKIP | OPTIONAL | SKIP | OPTIONAL | OPTIONAL | SKIP | Reports only, changes nothing. Module health check, not a bug finder. Next step per its file: `/sc:improve` or `/sc:cleanup` |
| `/sc:explain` | Provide clear explanations of code, concepts, and system behavior with educational clarity | OPTIONAL | OPTIONAL | SKIP | SKIP | SKIP | SKIP | Guide level 1: understanding, no files change |

Also used in this phase (rated in their home tables): `/sc:test` (reproduce, then confirm; 2.4), `bmad-quick-dev` (small fix; 2.4), `/sc:workflow` + `/sc:implement` (fix spanning a few files; 2.2/2.4), `/task-builder` + `/task` (larger or riskier fix; 2.2/2.4), `bmad-review-edge-case-hunter` (probe the fix; 2.3).

### 2.7 Phase: Post-merge / Release

| Command | Purpose (from its own description) | T | B | S | F | R | N | Notes |
|---|---|---|---|---|---|---|---|---|
| `/sc:post-release` | Post-release follow-through: sync and create a shipped version's external surface (user docs, tech docs, install/deploy scripts validated by real runs, human-run e2e guides). Runs AFTER the release gate tags a version | SKIP | SKIP | SKIP | SKIP | WORTH IT | WORTH IT | Whether this team tags versions is UNVERIFIED (`CHANGELOG.md` carries "template-version notes") |
| `bmad-retrospective` | Post-epic review to extract lessons and assess success | SKIP | SKIP | SKIP | WORTH IT | WORTH IT | WORTH IT | csv: 4-implementation, optional at epic end; follows `bmad-code-review`. Output: `implementation_artifacts` |
| `bmad-sprint-status` | Summarize sprint status and surface risks | SKIP | SKIP | SKIP | OPTIONAL | WORTH IT | OPTIONAL | csv: anytime, "route to next workflow". Tracking aid. BMad lane |
| `/tech-reference` | Create or populate a Technical Reference document for a built feature | SKIP | SKIP | OPTIONAL | WORTH IT | WORTH IT | WORTH IT | Guide 3.1 step 11 (document what was built). Repo already carries `aidev02-v1.0-as-built-technical-reference.md`. ‡ with `/sc:document` |
| `/operational-guide` | Create or populate an Operational Guide for a deployment, setup, or operations procedure | SKIP | SKIP | SKIP | OPTIONAL | WORTH IT | WORTH IT | Repo has `docs/operations/*`. Needed when deploy or operator steps changed |
| `/readme` | Create or populate a README.md for a project, module, or package | SKIP | SKIP | SKIP | OPTIONAL | OPTIONAL | OPTIONAL | Only for a new package or module |
| `/sc:document` | Generate focused documentation for components, functions, APIs, and features | SKIP | SKIP | OPTIONAL | OPTIONAL | OPTIONAL | OPTIONAL | One-pass reference text (`--type api`). ‡ with `/tech-reference` |
| `bmad-agent-tech-writer` | Technical documentation specialist persona (Paige) | SKIP | SKIP | SKIP | OPTIONAL | OPTIONAL | OPTIONAL | Persona wrapper; csv lists doc, diagram, explain and review actions |
| `openspec-archive-change` = `opsx:archive`; `openspec-bulk-archive-change` = `opsx:bulk-archive`; `openspec-sync-specs` = `opsx:sync` | Archive a completed change; archive several; sync delta specs to main specs | SKIP | SKIP | SKIP | SKIP | SKIP | SKIP | OpenSpec lane only |

Navigation helpers (no phase; never part of a checked pipeline):

| Command | Purpose | T | B | S | F | R | N | Notes |
|---|---|---|---|---|---|---|---|---|
| `/sc:recommend` | Build a refined, paste-ready prompt that delegates the goal to the right local skill, command, agent, or tool sequence | OPTIONAL | OPTIONAL | OPTIONAL | OPTIONAL | OPTIONAL | OPTIONAL | Guide: use "when unsure which tool to use". Reads the routing table |
| `/sc:help` | List installed SuperClaude commands and skills, show the six process levels, point to the routing guide | SKIP | SKIP | SKIP | SKIP | SKIP | SKIP | Listing only |
| `bmad-help` | Analyzes current state and user query to recommend the next BMad skill | OPTIONAL | OPTIONAL | OPTIONAL | OPTIONAL | OPTIONAL | OPTIONAL | Lane navigator |

### 2.8 Deprecated (any phase)

| Command | Purpose (from its own description) | T | B | S | F | R | N | Notes |
|---|---|---|---|---|---|---|---|---|
| `bmad-create-prd` | DEPRECATED, consolidated into `bmad-prd` create intent; removed in v7 | SKIP | SKIP | SKIP | SKIP | SKIP | SKIP | Use `bmad-prd` |
| `bmad-edit-prd` | DEPRECATED, consolidated into `bmad-prd` update intent | SKIP | SKIP | SKIP | SKIP | SKIP | SKIP | Use `bmad-prd` |
| `bmad-validate-prd` | DEPRECATED, consolidated into `bmad-prd` validate intent | SKIP | SKIP | SKIP | SKIP | SKIP | SKIP | Use `bmad-prd` |
| `bmad-create-architecture` | DEPRECATED, consolidated into `bmad-architecture` create intent | SKIP | SKIP | SKIP | SKIP | SKIP | SKIP | Use `bmad-architecture` |

A checker should not count a deprecated skill as a missing step, and should not flag its use as wrong either; it should treat it as its replacement.

<!-- SECTION 3: overlaps and picks -->
## 3. Overlaps and picks

The biggest overlap is not one command pair. It is two whole lanes that both go from idea to merged code:

- **Task-file lane**: `/sc:brainstorm` -> `/prd` -> `/tdd` -> `/roadmap` or `/sc:workflow` / `/task-builder` -> `/task` or `/sc:implement` -> `/sc:pr-submit`.
- **BMad lane**: `bmad-brainstorming` -> `bmad-prd` -> `bmad-architecture` -> `bmad-create-epics-and-stories` -> `bmad-check-implementation-readiness` -> `bmad-sprint-planning` -> `bmad-create-story` -> `bmad-dev-story` -> `bmad-code-review` -> `bmad-retrospective` (order from `bmad-help.csv` `preceded-by`).

Repo evidence shows both lanes in use (Section 1). The rule that keeps a checker simple: pick the lane at the Spec step and stay in it until the PR. Do not run `/task-builder` on a BMad story file or `bmad-dev-story` on a `TASK-WF-*` plan. The `/sc:pr-submit` step is shared by both lanes.

| # | Job | Overlapping commands | Pick | Why |
|---|---|---|---|---|
| O1 | Shape a vague idea | `/sc:brainstorm`, `bmad-brainstorming`, `bmad-forge-idea`, `bmad-party-mode`, `openspec-explore` / `opsx:explore`, `/tech-research` (when it is really a feasibility question) | `/sc:brainstorm` | Has `--handoff none\|design\|tasklist\|task`, so its output feeds either lane. Use `bmad-brainstorming` only when the next step is `bmad-prd` |
| O2 | Write the PRD | `/prd`, `bmad-prd` (+ deprecated `bmad-create-prd`, `bmad-edit-prd`, `bmad-validate-prd`), `bmad-product-brief` | `bmad-prd` for this repo | `_bmad-output/planning-artifacts/prd.md` and the epics exist, and `bmad-prd` has create/update/validate in one skill. Producer of those existing files is UNVERIFIED. Use `/prd` if the work goes to `/roadmap` |
| O3 | Technical design | `/tdd` (= `/sc:tdd`), `bmad-architecture` (+ deprecated `bmad-create-architecture`), `/sc:design` | Follows O2: `bmad-architecture` after `bmad-prd`, `/tdd` after `/prd` | `/sc:design` is a single-pass draft of one interface; not a substitute for either |
| O4 | Critique a spec | `/sc:spec-panel`, `bmad-review-adversarial-general`, `bmad-advanced-elicitation`, `bmad-editorial-review-*`, `/sc:adversarial` | `/sc:spec-panel` (`--mode critique`) | Named in the guide's full-spec path. `/sc:adversarial` is for choosing between two competing drafts, not for critique |
| O5 | Cross-document readiness | `bmad-check-implementation-readiness`, `/sc:reflect --mode pre`, `/sc:validate-roadmap`, `/sc:tasklist` integrated validation | `/sc:reflect --mode pre` in the task-file lane; `bmad-check-implementation-readiness` in the BMad lane | Different inputs (plan vs spec, versus PRD+UX+arch+epics). Same job, one per lane |
| O6 | Turn spec into steps | `/sc:workflow`, `/task-builder`, `/roadmap`, `/sc:roadmap` + `/sc:tasklist`, `bmad-create-epics-and-stories` + `bmad-sprint-planning` + `bmad-create-story`, `openspec-ff-change`, `/sc:spawn` | By size: `/sc:workflow` (S), `/task-builder` (F, R), `/roadmap` (N); BMad lane: `bmad-create-story` (S), `bmad-create-epics-and-stories` (F, N) | Guide section 5 table of mix-ups. `/sc:roadmap` + `/sc:tasklist` are a separate release pipeline; `/sc:spawn` is superseded by `/task-builder`. Note: `/sc:tasklist` is retired (Ryan), see Section 2.2. |
| O7 | Execute the steps | `/sc:implement`, `/task`, `/sc:task`, `bmad-dev-story`, `bmad-quick-dev`, `bmad-dev-auto`, `bmad-agent-dev`, `openspec-apply-change` / `opsx:apply` | The executor that matches the input file: `TASK-WF-*` plan -> `/sc:implement`; task-builder file -> `/task`; BMad story file -> `bmad-dev-story`; no file, tiny change -> `/sc:task` or a plain edit | Guide: running a `TASK-WF-*` folder with `/task` is wrong. `bmad-quick-dev` is the BMad lane's small-work option. Note: `/sc:task` is retired (Ryan), see Section 2.4. |
| O8 | Review code before push | `/code-review`, `bmad-code-review`, `/sc:auggie-review`, `bmad-review-adversarial-general`, `bmad-review-edge-case-hunter`, `bmad-checkpoint-preview`, `/sc:swarm-wizard`, the PR bot driven by `/sc:pr-submit --monitor 1` | `/code-review` (task-file lane) or `bmad-code-review` (BMad lane); then `/sc:pr-submit` | One bug review plus the PR monitor is enough. `/sc:auggie-review` adds a whole-branch view; the other four are for extra assurance |
| O9 | Diagnose a bug | `/sc:troubleshoot`, `bmad-investigate`, `/sc:analyze` | `/sc:troubleshoot` | Named in Ryan's pipeline step 5 and the guide; produces `REPORT.md` with file:line evidence. `/sc:analyze` is health, not bugs |
| O10 | Research | `/tech-research` (our code), `/sc:research` (web), `bmad-technical-research`, `bmad-domain-research`, `bmad-market-research` | `/tech-research` for code questions, `/sc:research` for outside questions | Guide section 5. The three BMad research skills are product/market framing; whether `bmad-technical-research` reads code or web is UNVERIFIED |
| O11 | Document what was built | `/tech-reference`, `/sc:document`, `/readme`, `/operational-guide`, `bmad-agent-tech-writer`, `bmad-document-project` | `/tech-reference` | Researches a whole feature and is reviewed; `/sc:document` is one-pass reference for specific code |
| O12 | Make a small change | `/sc:task`, `bmad-quick-dev`, plain edit + test | Plain edit + related test, or `/sc:task` | Guide level 2. `bmad-quick-dev` produces a spec file first, which is overkill at T size. Note: `/sc:task` is retired (Ryan), see Section 2.4. |
| O13 | OpenSpec versus everything above | 10 `openspec-*` skills and 10 `opsx:*` commands, each pair with identical descriptions | Neither; if ever used, use `opsx:*` | Third lane covering Spec, Tasklist, Implement, Review, Archive. Not in any of Ryan's pipelines; repo has one change dir. Each pair is the same flow packaged twice |
| O14 | Same skill under two names | `/tdd` and `/sc:tdd` | `/tdd` | Guide "Other commands": `/sc:tdd` invokes the same skill. Not test-driven development |
| O15 | Commit | `/sc:git`, plain `git` | `/sc:git` for the message, plain `git` is equivalent | Judgment. How `/sc:git` handles `.dev/tasks` staging is UNVERIFIED |

Not overlaps despite similar names: `/task` (runs a task file) versus `/sc:task` (does one job, no file); `bmad-retrospective` (lessons after an epic) versus `/sc:reflect --mode post` (deviation audit against a plan); `/sc:cleanup-audit` (report) versus `/sc:cleanup` (edits).

<!-- SECTION 4: minimum viable path per work size -->
## 4. Minimum viable path per work size

"Fewest commands that still count as following the pipeline" = every command rated REQUIRED for that size in Section 2, in order, plus the commit that Ryan's pipeline requires between implement and push. Commits are not a command here: plain `git` or `/sc:git` both count.

| Size | Task-file lane (minimum) | BMad lane (minimum) | WORTH IT additions (skip only with a reason) |
|---|---|---|---|
| **One-off task** (small code change) | 1. edit (plain, or `/sc:task`) 2. run the related test 3. commit 4. `/sc:pr-submit --monitor 1` | `bmad-quick-dev` in place of step 1 | `/sc:task` (T: WORTH IT), `/sc:test` |
| **Bug fix** | 1. `/sc:troubleshoot "<error + repro>" --type <kind>` 2. write a failing test, fix 3. run the test 4. commit 5. `/sc:pr-submit --monitor 1` | same; `bmad-quick-dev` may replace step 2 | `/sc:test`, `/code-review`. If the fix spans a few files: add `/sc:workflow` + `/sc:implement`; if larger or riskier: `/task-builder` + `/task` |
| **Single story** | 1. `/sc:workflow "<..>" --depth quick` 2. read the plan and its check result 3. `/sc:implement <plan path>` 4. commit 5. `/code-review` 6. `/sc:pr-submit --monitor 1` | `bmad-create-story` -> `bmad-dev-story` -> `bmad-code-review` -> commit -> `/sc:pr-submit --monitor 1` | `/task-builder` + `/task` instead of steps 1-3 if the story is multi-session; `/sc:auggie-review`; `/security-review` if secrets, login, permissions, input, or paths changed; `/sc:test` |
| **Multi-story feature** | 1. short agreed spec file 2. `/task-builder "<..>" --spec <path>` 3. read the task file and its `reflect_pre` entry 4. `/task <file>` 5. commit per phase 6. `/code-review` 7. `/sc:pr-submit --monitor 1` | `bmad-create-epics-and-stories` -> `bmad-sprint-planning` -> per story: `bmad-create-story` -> `bmad-dev-story` -> `bmad-code-review` -> commit; then `/sc:pr-submit --monitor 1` | `/sc:reflect --mode post --no-promote` per phase, `bmad-check-implementation-readiness`, `/tech-research` first, `/sc:spec-panel` on the spec, `/sc:auggie-review`, `/security-review`, `bmad-retrospective`, `/tech-reference` |
| **Release** | 1. `/sc:reflect --mode post --diff <commit> --no-promote` on every phase of the release 2. `/code-review` on the full branch 3. `/sc:pr-submit --monitor 1` | same three steps; `bmad-code-review` may replace step 2 | `/sc:release-split`, `/task-builder` / `/roadmap` for release steps, `/sc:test` full run, `/sc:auggie-review`, `/security-review`, `/sc:post-release` after the tag, `bmad-retrospective`, `bmad-check-implementation-readiness`, `/operational-guide`, `/tech-reference` |
| **New product** | 1. `/prd` 2. `/sc:spec-panel` (critique) 3. `/tdd` 4. `/sc:spec-panel` 5. `/roadmap` (dry run, then full) 6. `/task` per phase 7. `/sc:reflect --mode post --no-promote` per phase 8. commit per phase 9. `/code-review` 10. `/sc:pr-submit --monitor 1` | `bmad-prd` -> `bmad-architecture` -> `bmad-create-epics-and-stories` -> `bmad-check-implementation-readiness` -> `bmad-sprint-planning` -> per story: `bmad-create-story` -> `bmad-dev-story` -> `bmad-code-review` -> `/sc:pr-submit --monitor 1` | `/sc:brainstorm` or `bmad-brainstorming` when the idea is vague, `bmad-product-brief`, `/tech-research`, `/sc:release-split`, `/task-builder`, `/sc:auggie-review`, `/security-review`, `/tech-reference`, `/operational-guide`, `bmad-retrospective`, `bmad-checkpoint-preview`, `bmad-qa-generate-e2e-tests` |

> Note: `/sc:task` named in the One-off row above is retired (Ryan, 2026-10-27), see Section 2.4. The replacement one-off minimum is pending Ryan (see 6.6).

Skippable at every size: all `openspec-*` / `opsx:*`, the four deprecated `bmad-*` skills, `/sc:spawn`, `/sc:roadmap` + `/sc:tasklist` + `/sc:validate-roadmap` (separate pipeline), `/sc:help`, `bmad-party-mode`, the `bmad-agent-*` personas, `bmad-editorial-review-*`.

### What a checker could observe (from the guide's stated output paths and the BMad csv; not yet confirmed by running the commands)

| Command | Footprint a scheduled job could look for | Source |
|---|---|---|
| `/sc:brainstorm` | `.dev/brainstorms/<timestamp>-<name>/merged-requirements.md` | guide 3.1 |
| `/sc:workflow` | `.dev/tasks/to-do/TASK-WF-*/<id>.md` and `progress.md`; `return-contract.yaml` with `reflect_status`; folder moves to `.dev/tasks/done/` when `/sc:implement` finishes (Linux only) | guide level 3, 3.10 |
| `/task-builder` | task file under `.dev/tasks/to-do/` with a `reflect_pre` block in its frontmatter (`verdict: pass\|fail\|skipped`) | guide 3.10 |
| `/task` | `reflect_post` entry and a Task Log in the same file | guide 3.1 step 9 |
| `/roadmap` | `.dev/tasks/to-do/TASK-ROADMAP-*/` with `build-requests/` and `qa/` | guide 3.1 step 7 |
| `/tech-research` | `.dev/tasks/to-do/TASK-RESEARCH-*/RESEARCH-REPORT-*.md` | guide level 5 |
| `/sc:troubleshoot` | `.dev/troubleshoot/<name>-<timestamp>/REPORT.md` | guide 3.4 |
| `/sc:reflect --mode pre` | `.dev/reflect/pre-<name>-<timestamp>/` (post-mode path not stated in the guide: UNVERIFIED) | guide 3.10 |
| `/sc:pr-submit` | the PR itself; a `run-log.jsonl` exists (`--resume` flag), its location is UNVERIFIED | pr-submit file |
| BMad planning | `_bmad-output/planning-artifacts/` (prd, architecture, epics, readiness report, change proposal) | `bmad-help.csv` |
| BMad implementation | `_bmad-output/implementation-artifacts/` (sprint status, story, story validation report, retrospective, quick-dev spec). `bmad-dev-story` and `bmad-code-review` have no output location in the csv | `bmad-help.csv` |
| `/code-review`, `/security-review`, `/sc:test`, `/sc:implement` (beyond `progress.md`), `/sc:git` | No file footprint stated anywhere I read. Only visible in a session transcript or PR comments: UNVERIFIED | guide; absence is not proof |

<!-- SECTION 5: unverified items -->
## 5. Unverified items

What I read in full: `~/.claude/HOW-WE-WORK.md` (327 lines), `~/.claude/commands/sc/help.md`, and the frontmatter of every file in the inventory. For `/sc:troubleshoot`, `/sc:pr-submit`, `/sc:brainstorm`, `/sc:design`, `/sc:test`, `/sc:implement`, `/sc:workflow`, `/sc:tasklist`, `/sc:spec-panel`, `/sc:reflect`, `/sc:git`, `/sc:post-release` I read only the usage and flag lines (grep), not the whole body. For `bmad-quick-dev`, `bmad-dev-auto`, `bmad-investigate` I read the first lines only. I did not run any command.

| # | Item | Why unverified | What would resolve it |
|---|---|---|---|
| U1 | All ratings marked "judgment" in the Notes column | Not stated in a description, the routing guide, or `bmad-help.csv` | Team agreement (this is the decision the brainstorm needs to make) |
| U2 | `/security-review` description | It is a built-in with no file; the guide only names it and its trigger conditions | Read Claude Code docs or run it |
| U3 | `/simplify` and `/code-review` behavior | Descriptions come from the session skill list, not a file | Same |
| U4 | Whether the Augment Code review app is installed on `IronbellyOrg/Coder` | Guide says `/sc:pr-submit --monitor 1` needs it; a grep for "augment" in `.github` matched `coder-automation-routes.yaml` and contract tests 57 and 60, which I did not open, so the result is inconclusive | Repo Settings > GitHub Apps; otherwise use `--monitor 0` |
| U5 | Whether the `T2ProxyUrl` / `T2ProxyKey` / `T2Model01` proxy is configured, so `/sc:swarm-wizard` can run for real | Not checked (env values must not be read or printed) | Presence check of variable names only |
| U6 | Whether the team runs `superclaude sprint run` (the `/sc:roadmap` + `/sc:tasklist` pipeline). The `superclaude` binary exists at `/usr/local/bin/superclaude` here | Existence of the binary does not prove use | Ask the team; look for `.dev/releases/` runs |
| U7 | What the `bmad-spec` SPEC kernel feeds downstream | Not read past the description | Read `bmad-spec/SKILL.md` |
| U8 | Whether `bmad-technical-research` searches the web or the codebase | Description says "technologies and architecture" only | Read its SKILL.md |
| U9 | Whether `bmad-dev-auto` pushes or commits on its own | Body says "without human interaction"; remainder not read | Read the full skill |
| U10 | What each `bmad-agent-*` persona wraps (e.g. does `bmad-agent-dev` call `bmad-dev-story`?) | Only descriptions read | Read the SKILL.md files |
| U11 | Which command produced the existing `_bmad-output/planning-artifacts/*` files (O2 pick) | Files exist; producer not recorded in what I read | Check file headers or git log |
| U12 | Whether `/sc:git --smart-commit` respects the "always stage `.dev/tasks`" rule in `CLAUDE.md` | `/sc:git` body not read beyond usage lines | Read the command file |
| U13 | Post-mode output folder of `/sc:reflect` and location of the `/sc:pr-submit` run log | Guide gives only the pre-mode path | Run once, or read the protocol skills |
| U14 | Whether the team tags versions (relevance of `/sc:post-release`, `/sc:release-split`) | `CHANGELOG.md` mentions template-version notes; no tag check done | `git tag -l`, `docs/operations/` |
| U15 | Whether any product here has a UI (relevance of `bmad-ux`) | Repo is mostly Terraform templates and operations docs | Ask |
| U16 | `/sc:spec-panel` file mentions `/sc:code-to-spec` in an example block | No such command exists in the inventory; I did not list it | Fix that example in the spec-panel command file |
| U17 | Home-directory commands are not shared | `sc:*`, `task-builder`, `task`, `prd`, `tdd`, `roadmap` live in `~/.claude`, so another engineer's machine may lack them or have an older `HOW-WE-WORK.md` (the file's own header says `superclaude update` refreshes it) | Compare `~/.claude` across engineers, or check the install version |
| U18 | The guide says the routing table "is read by `/sc:recommend` and checked by tests" | I did not find or run those tests | Locate the tests in the IronClaude source |

Not in the inventory because it could not be verified: `/sc:agent` and `/sc:business-panel` (no frontmatter in their files).

<!-- SECTION 6: complexity layer -->
## 6. Complexity layer (added 2026-10-27)

Added by folding the 27 per-command nuance files in `command-nuance/` into this file, on top of the scope ratings in Section 2. Nothing in Sections 1 to 5 was re-rated from this section: every rating or path proposal that rests on an agent's judgment sits in 6.2 and waits for Ryan. Subsections: 6.1 the two axes; 6.2 proposed rating changes; 6.3 per-command nuance (27 commands); 6.4 conflicts between sources; 6.5 defects found; 6.6 decisions waiting for Ryan; 6.7 coverage and gaps.

### 6.1 The two axes

| Axis | Values | Defined by |
|---|---|---|
| Scope | T one-off task, B bug fix, S single story, F multi-story feature, R multi-feature release (as redefined by Ryan: full release plan, implementation and push; one step below N), N new product | Section 1 rating rules and the banner at the top. The R column in Section 2 is still the older reading (not re-rated in place) |
| Complexity | LOW, MEDIUM, HIGH | Per command, in the matrix and band definitions copied into each 6.3 subsection. Signals used: files or subsystems touched, expected sessions, whether the author can name the files up front, whether a driving spec exists, risk (secrets, permissions, user input, paths, infrastructure), drift sensitivity, need for research, shared interfaces between stories |

What the files give for complexity, and what they do not:

- The only on-disk formula is task-builder's TCS (`~/.claude/skills/task-builder/SKILL.md` around lines 2410-2441: quick <=12, standard 13-34, deep >=35). It is computed on a finished task file and sets `/sc:reflect` depth, not the choice between commands (`command-nuance/sc-workflow.md` 3.4; `command-nuance/sc-reflect.md` section 3). A few commands carry their own measure: the Wave 1.6 gate of `/sc:troubleshoot`, the input score of `/sc:roadmap`, the runtime rubric of `/sc:reflect`. Each is stated inside its own 6.3 subsection.
- Every other band edge is a judgment (J) built from the signals above. A cell marked (J), JUDGMENT or "proposed" in 6.3 is a proposal, not a ruling.
- No file defines "story". The validation of the multi-story feature minimum records it twice: no file read defines "story" or "multi-story", and no file gives a number of stories, files or modules at which to switch commands (`validation-feature-task-builder-vs-sc-workflow.md` lines 12, 138; open item V8 at line 291). Pending Ryan (6.6 item 1).
- The guide's levels 3 and 4 overlap at two sessions: level 3 "fits in one or two sessions", level 4 is "more than one session" (HOW-WE-WORK.md lines 17 and 18). Tie rule on disk: "choose the heavier one" (HOW-WE-WORK.md line 9). Recorded in `validation-feature-task-builder-vs-sc-workflow.md` lines 12 and 143, open item V9 at line 292. Pending Ryan (6.6 item 2).
- Two validations are already done and are treated as fixed here. `validation-feature-task-builder-vs-sc-workflow.md`: `/task-builder` + `/task` is the minimum tasklist step for a multi-story feature; `/sc:workflow` + `/sc:implement` is not eligible as that minimum (verdict, lines 9-13). `validation-oneoff-sc-task-vs-sc-implement.md`: `/sc:implement` has no `--depth` flag, and the one-off minimum (a plain edit plus the related test, with `/sc:implement "<prompt>"` as an optional add-on) is PROPOSED, not confirmed by Ryan (verdict, lines 5-9; `command-nuance/_brief.md` line 16).
- Retired: `/sc:task` and `/sc:tasklist` (Ryan). No band, cell or path in 6.3 recommends either as an engineer step.

### 6.2 Proposed rating changes awaiting Ryan

One consolidated table of every proposal from section 7 of the 27 nuance files (217 rows, P001 to P217). Nothing in it has been applied to Section 2 or Section 4. Rows are grouped by command in pipeline-phase order: Spec (brainstorm, design, spec-panel, tdd, research, adversarial, release-split); Tasklist (workflow, roadmap, spawn); Review (reflect, validate-roadmap, swarm-wizard); Implement (implement, test, build, improve, cleanup, cleanup-audit); Commit/PR (git, auggie-review, pr-submit); Bug fix (troubleshoot, analyze, explain); Post-merge (post-release, document).

How to read the columns:

- Command links to the full nuance file. Row or cell is the source's own row label (`#` is the source's row id). The source line numbers refer to this file as it read on 2026-10-27, before the edits made by this merge, so they may be a few lines off now.
- Current text and Proposed text are copied from the source row. `\|` is a literal pipe inside a cell.
- Basis is the source's own "Why" or "Evidence" column. Where the source row has none, the cell says so.
- Judgment? is Y when the source row carries a (J), JUDGMENT or PROPOSED marker, or when its rating or band change rests on the agent's reading although the row carries no marker (11 rows: P001, P011, P039, P043, P066, P125, P128, P134, P147, P198, P201). Y rows are proposals only. N rows are wording, footprint or cross-reference changes that a file supports, or "no change" rows. 70 rows are Y and 147 are N.
- Rows that restate Ryan's rulings (the R definition, the retirement of `/sc:task` and `/sc:tasklist`) were applied above for the wording only: the R definition text, the 2.4 reading note, the two retired rows and the retirement notes. Their rating consequences are still proposals.
- Five source files wrote section 7 as a list, not a table (analyze, explain, git, swarm-wizard, build). Their items were carried into rows as written. In the document file, two items written as sentences beside the table were added as rows.

| Ref | Command | Row or cell | Current text | Proposed text | Basis | Judgment? |
|---|---|---|---|---|---|---|
| P001 | [/sc:brainstorm](command-nuance/sc-brainstorm.md) | #1: Line 64, `/sc:brainstorm` row, columns T/B/S/F/R/N | `SKIP \| SKIP \| OPTIONAL \| WORTH IT \| OPTIONAL \| WORTH IT` | Keep the six cells. **R cell: keep `OPTIONAL`, but under the new definition (multi-feature release, one step below N) it reads "OPTIONAL; WORTH IT only when the release scope is unsettled (HIGH); SKIP when each feature already has a spec or `/sc:release-split` runs".** The old R cell was probably rated on a single-feature reading, where it was OPTIONAL for a different reason (a feature's release is a phase inside S or F). If the merged file gains complexity sub-columns, use the section 3 matrix | No separate basis column in the source row; see the source file, sections 3 and 4 | Y |
| P002 | [/sc:brainstorm](command-nuance/sc-brainstorm.md) | #2: Line 64, Notes | `Guide: "only if the idea is still vague". \`--handoff task\` goes straight to a task file. ‡ with \`bmad-brainstorming\`` | `Never REQUIRED: guide runs it "only if the idea is vague" (HOW-WE-WORK.md:309). Skip when a spec, PRD or story already exists. --depth quick/standard/deep by complexity. Use --handoff none, then /task-builder --spec <merged-requirements.md>: --handoff task passes no --spec, and --handoff tasklist calls the retired /sc:tasklist. Footprint .dev/brainstorms/<ts>-<slug>/. ‡ with bmad-brainstorming` | No separate basis column in the source row; see the source file, sections 3 and 4 | N |
| P003 | [/sc:brainstorm](command-nuance/sc-brainstorm.md) | #3: Line 79, `bmad-brainstorming` Notes | `bmad-help.csv: phase 1-analysis, required=false. ‡ with /sc:brainstorm` | Append: `Divergent idea generation with a coach (Facilitator / Creative Partner / Ideate for me); no adversarial merge, no requirements spec. Pick when the next step is bmad-product-brief / bmad-prd or when ideas, not a decision, are needed. Footprint _bmad-output/brainstorming/brainstorm-<slug>-<date>/.memlog.md (status: complete at wrap-up)`. R cell: same note as row 1 | No separate basis column in the source row; see the source file, sections 3 and 4 | N |
| P004 | [/sc:brainstorm](command-nuance/sc-brainstorm.md) | #4: Line 227, O1 "Why" | `Has --handoff none\|design\|tasklist\|task, so its output feeds either lane. Use bmad-brainstorming only when the next step is bmad-prd` | `Its merged-requirements.md feeds either lane (as a file, not through --handoff: tasklist calls the retired /sc:tasklist and task passes no --spec). Use bmad-brainstorming when the next step is bmad-product-brief / bmad-prd, or when the need is ideas rather than a decision` | No separate basis column in the source row; see the source file, sections 3 and 4 | N |
| P005 | [/sc:brainstorm](command-nuance/sc-brainstorm.md) | #5: Line 255 (F row, WORTH IT additions) | list has no `/sc:brainstorm` | Add `/sc:brainstorm --depth standard` (only when no spec or requirements file exists) | No separate basis column in the source row; see the source file, sections 3 and 4 | N |
| P006 | [/sc:brainstorm](command-nuance/sc-brainstorm.md) | #6: Line 256 (R row, WORTH IT additions) | no `/sc:brainstorm` | Add `/sc:brainstorm --depth deep` (only when release scope is unsettled and `/sc:release-split` is not planned) | No separate basis column in the source row; see the source file, sections 3 and 4 | N |
| P007 | [/sc:brainstorm](command-nuance/sc-brainstorm.md) | #7: Line 265 (footprint table) | `.dev/brainstorms/<timestamp>-<name>/merged-requirements.md` / `guide 3.1` | `.dev/brainstorms/<YYYYMMDDTHHMMSSZ>-<slug>/`: `merged-requirements.md` (9 of 11 observed), `seed-brief.md` (7), `return-contract.yaml` (7); tracked in git when committed. BMad twin: `_bmad-output/brainstorming/brainstorm-<slug>-<date>/.memlog.md`. Source: protocol `SKILL.md:136-147,334-378` and observed folders | No separate basis column in the source row; see the source file, sections 3 and 4 | N |
| P008 | [/sc:brainstorm](command-nuance/sc-brainstorm.md) | #8: Line 281 (what was read) | says `/sc:brainstorm` was read for usage and flag lines only | Note that command file, protocol skill and its three refs were later read in full (this file) | No separate basis column in the source row; see the source file, sections 3 and 4 | N |
| P009 | [/sc:brainstorm](command-nuance/sc-brainstorm.md) | #9: New unverified items for section 5 (line 283 onward) | n/a | Add U-items from section 8 below that concern `--handoff task`, the missing `sc-research-protocol` skill, and the 1-proposal runs on disk | No separate basis column in the source row; see the source file, sections 3 and 4 | N |
| P010 | [/sc:design](command-nuance/sc-design.md) | #1: CV:65, `/sc:design` row, ratings | `SKIP \| SKIP \| SKIP \| OPTIONAL \| SKIP \| OPTIONAL` (T, B, S, F, R, N) | `SKIP \| SKIP \| SKIP \| OPTIONAL \| OPTIONAL (J) \| OPTIONAL`. **Only R changes: SKIP to OPTIONAL.** Section 3 adds that R-HIGH is WORTH IT (J) when a split is approved | R re-rated under the multi-feature-release definition: `/sc:release-split` Part 3 says "Default to /sc:design for producing release specs" (RS:270-275; RSC:134). The old SKIP fits a "release ships work already built" reading (the reading CV:139 states for the Implement phase). F and N keep OPTIONAL | Y |
| P011 | [/sc:design](command-nuance/sc-design.md) | #2: CV:65, `/sc:design` row, Notes | "Single-pass draft of one API/component (guide section 5). Use for a new interface inside a spec file. ‡ with `/tdd`" | "Single-pass draft of one interface, API, component or schema (HW:244). No `--depth` or `--tier`, no protocol skill, no file footprint. Use `--type api\|component --format spec` for a new interface inside a spec file (HW:98). Never REQUIRED. By complexity: LOW one interface, `/sc:design`; MEDIUM `/tdd --tier standard`; HIGH (20+ files, several services, shared interfaces) `/tdd --tier heavyweight` or `bmad-architecture`. Also called by `/sc:auggie-review` remediation Phase A and `/sc:release-split` Part 3. ‡ with `/tdd`" | Adds the complexity layer and the callers | Y |
| P012 | [/sc:design](command-nuance/sc-design.md) | #3: CV:229, O3 "Technical design", Why | "`/sc:design` is a single-pass draft of one interface; not a substitute for either" | Append: "Pick by size: one interface = `/sc:design`; component or service needing verified claims = `/tdd` (lightweight under 5 files, standard 5-20, heavyweight 20+ or several services, TDDS:71-73); BMad lane and shared-interface drift risk = `bmad-architecture`. Lane rule: stay in the lane chosen at the Spec step (CV:223)" | Gives O3 a complexity rule | N |
| P013 | [/sc:design](command-nuance/sc-design.md) | #4: CV:276, footprint row for commands with no stated footprint | "`/code-review`, `/security-review`, `/sc:test`, `/sc:implement` (beyond `progress.md`), `/sc:git`" | Add `/sc:design` to the list, and add a note: "only caller-supplied paths exist: `<output_dir>/remediation-spec.md` (auggie remediation), `<output>/release-1-spec.md` (release-split); verify with a spec/design artifact check, not the command name" | Section 5 of this file | N |
| P014 | [/sc:design](command-nuance/sc-design.md) | #5: CV:281, "What I read in full" | "For `/sc:troubleshoot`, `/sc:pr-submit`, `/sc:brainstorm`, `/sc:design`, `/sc:test`, ... I read only the usage and flag lines (grep)" | Remove `/sc:design` from that list; add "`/sc:design` read in full (110 lines, 2026-10-27); it has no backing protocol skill" | Corrects the read-depth statement | N |
| P015 | [/sc:design](command-nuance/sc-design.md) | #6: CV:7 / CV:48, definition of R | "release (R)" | Out of scope for this file: a global change. Every R cell in the whole file needs the same re-rating pass under the new definition | Brief ruling 2 | N |
| P016 | [/sc:spec-panel](command-nuance/sc-spec-panel.md) | #P1: Row 66, `/sc:spec-panel`, columns T B S F R N | `SKIP / SKIP / OPTIONAL / WORTH IT / OPTIONAL / REQUIRED` | Keep the six headline cells and add the complexity split in Notes: `T SKIP; B SKIP (OPTIONAL at HIGH if the fix changes a contract); S SKIP-OPTIONAL-WORTH IT by LOW-MED-HIGH; F OPTIONAL-WORTH IT-REQUIRED (as "any spec critique"); R OPTIONAL-WORTH IT-REQUIRED (as "any spec critique"); N REQUIRED at all bands`. Mark every non-stated cell (J) | No separate basis column in the source row; see the source file, sections 3 and 4 | Y |
| P017 | [/sc:spec-panel](command-nuance/sc-spec-panel.md) | #P2: Row 66, R cell (re-rating under the multi-feature release definition) | `OPTIONAL` | `WORTH IT` as the headline R rating. Reason: R is now a release plan, implementation and push, so the release-level spec or TDD is a new cross-feature document; the command already scopes output to a release (`SP:35`, `SP:272`). Sub-bands: LOW OPTIONAL, MEDIUM WORTH IT, HIGH REQUIRED (J). The old OPTIONAL fits a reading where "release" is only the ship step | No separate basis column in the source row; see the source file, sections 3 and 4 | Y |
| P018 | [/sc:spec-panel](command-nuance/sc-spec-panel.md) | #P3: Row 66, Notes | `Guide full-spec steps 3 and 5 (--mode critique). Report only. Also a Review-phase tool` | Append: `Always --mode critique. Flags by artifact: PRD --focus requirements; TDD --focus architecture,testing; add correctness for 3+ state variables, numeric guards or pipelines; add compliance for secrets or permissions. Applying findings and re-running is the engineer's step (no --apply). No backing skill and no fixed output path; observed files are spec-panel-review[-rN].md. --downstream roadmap feeds the separate /sc:roadmap pipeline: do not recommend.` | No separate basis column in the source row; see the source file, sections 3 and 4 | N |
| P019 | [/sc:spec-panel](command-nuance/sc-spec-panel.md) | #P4: Row 230 (O4, critique a spec), Why column | `Named in the guide's full-spec path. /sc:adversarial is for choosing between two competing drafts, not for critique` | Append: `BMad-lane artifacts may use bmad-review-adversarial-general instead (ungraded list, no severity); scenarios S5 accepts "spec-panel or BMad equivalent". Pick spec-panel when severity grading or the correctness artifacts are needed.` | No separate basis column in the source row; see the source file, sections 3 and 4 | N |
| P020 | [/sc:spec-panel](command-nuance/sc-spec-panel.md) | #P5: Row 255 (Section 4, multi-story feature), "WORTH IT additions" | `... /sc:spec-panel on the spec ...` | Keep as WORTH IT for MEDIUM; at HIGH complexity move to the minimum as "a spec critique (spec-panel or BMad equivalent) before step 2". Mark (J) | No separate basis column in the source row; see the source file, sections 3 and 4 | Y |
| P021 | [/sc:spec-panel](command-nuance/sc-spec-panel.md) | #P6: Row 256 (Section 4, release), WORTH IT additions | no `/sc:spec-panel` | Add `/sc:spec-panel` on the release-level spec or TDD (WORTH IT at MEDIUM, REQUIRED (J) at HIGH). The release minimum there lists only post-implementation steps (`reflect post`, `/code-review`, `pr-submit`), which looks rated under the old reading; the merge step should re-derive it under the new R definition | No separate basis column in the source row; see the source file, sections 3 and 4 | Y |
| P022 | [/sc:spec-panel](command-nuance/sc-spec-panel.md) | #P7: Section 5, U16 (`/sc:code-to-spec`) | `/sc:spec-panel file mentions /sc:code-to-spec in an example block ... Fix that example in the spec-panel command file` | Mark confirmed: `spec-panel.md:416-417` is the only mention in `~/.claude/commands` and `~/.claude/skills` (grep), and `~/.claude/commands/sc/` has 43 files and none is `code-to-spec`. The whole first block (`SP:415-419`) is built on it ("generate spec, review, refine"). Suggested fix: replace its first line with a real producer such as `/sc:design <name> --type api --format spec` (named at `HWW:98`) or start the block at the first `/sc:spec-panel` line | No separate basis column in the source row; see the source file, sections 3 and 4 | N |
| P023 | [/sc:spec-panel](command-nuance/sc-spec-panel.md) | #P8: Section 5, intro paragraph | `/sc:spec-panel ... I read only the usage and flag lines (grep)` | Update: the full command file (463 lines) has now been read; the protocol is inline and no backing skill exists | No separate basis column in the source row; see the source file, sections 3 and 4 | N |
| P024 | [/sc:spec-panel](command-nuance/sc-spec-panel.md) | #P9: Section 4 "What a checker could observe", add a row | none for `/sc:spec-panel` | Add: `/sc:spec-panel`: no fixed path; observed `spec-panel-review[-rN].md` beside the spec and `.dev/reviews/<name>-<date>/spec-review-spec-panel.md`, each with an Invocation row; a recorded NO-GO with reason (e.g. `03-planning-roi.md`) is the footprint of a deliberate skip | No separate basis column in the source row; see the source file, sections 3 and 4 | N |
| P025 | [/sc:tdd](command-nuance/sc-tdd.md) | #1: 68, `/tdd` row, columns T B S F R N | `SKIP \| SKIP \| SKIP \| OPTIONAL \| SKIP \| REQUIRED` | `SKIP \| SKIP \| SKIP \| OPTIONAL \| OPTIONAL \| REQUIRED` (R changed, J) | R re-rated under Ryan's definition (planning is inside a multi-feature release). Section 3 gives the bands: R OPTIONAL at LOW, WORTH IT at MEDIUM and HIGH | Y |
| P026 | [/sc:tdd](command-nuance/sc-tdd.md) | #2: 68, Notes | "Guide level 6. Not test-driven development. Use when others build against the design. ‡ with `bmad-architecture`" | "Guide level 6. Not test-driven development. Use when others build against the design. F: SKIP at LOW, OPTIONAL at MEDIUM, WORTH IT at HIGH (J). R: OPTIONAL / WORTH IT / WORTH IT (J). N: REQUIRED at every band, tier by band (`--tier`). Stacks with `bmad-architecture` (spine = invariants, TDD = full spec); at LOW and MEDIUM pick one. Even `--tier lightweight` runs the full 7-phase pipeline" | Sections 3 and 4b; SK:69-80; BR:98-160 | Y |
| P027 | [/sc:tdd](command-nuance/sc-tdd.md) | #3: 88, `bmad-architecture` Notes | "... ‡ with `/tdd`" | Replace the double-dagger with "partly overlaps `/tdd`; repo evidence shows the TDD built after the spine (`_bmad-output/planning-artifacts/tdd.md:14-18`)" | Section 4b | N |
| P028 | [/sc:tdd](command-nuance/sc-tdd.md) | #4: 65, `/sc:design` Notes | "... ‡ with `/tdd`" | Replace with "overlaps `/tdd` for one interface only; stacks with it (CMD:183)" | Section 4a | N |
| P029 | [/sc:tdd](command-nuance/sc-tdd.md) | #5: 223 and 229 (O3 "Technical design", Section 3 intro) | "pick the lane at the Spec step and stay in it" / "`bmad-architecture` after `bmad-prd`, `/tdd` after `/prd`" | Add: "Not exclusive at the design step. `/tdd` consumed a BMad PRD in `.dev/releases/current/v2-m3/TDD_V2_M3.md:14` and was written after `bmad-architecture` in `_bmad-output/planning-artifacts/tdd.md:14-18`. Both may appear at N and HIGH F; a checker must not flag `/tdd` after `bmad-prd`" | Section 4b | N |
| P030 | [/sc:tdd](command-nuance/sc-tdd.md) | #6: 240 (O14) | "`/tdd` and `/sc:tdd` ... Pick `/tdd`" | Add: "A checker treats them as one command and must not match 'tdd' in test-driven-development contexts" | CMD:156; section 5 | N |
| P031 | [/sc:tdd](command-nuance/sc-tdd.md) | #7: 254-257 minimum paths, N row task-file lane step 3 | "3. `/tdd`" | "3. `/tdd --from-prd <prd> --tier heavyweight` (BMad lane: `bmad-architecture`)" | Section 2, 3 | N |
| P032 | [/sc:tdd](command-nuance/sc-tdd.md) | #8: 256 (Release row, WORTH IT additions) | no `/tdd` | Add "`/tdd` (MEDIUM and HIGH: one release-level TDD or per-feature TDDs; input to `/sc:release-split`)" (J) | R re-rating; HW:72 | Y |
| P033 | [/sc:tdd](command-nuance/sc-tdd.md) | #9: 255 (Multi-story feature row, WORTH IT additions) | no `/tdd` | Add "`/tdd` at HIGH complexity (20+ files, several services or layers, others build against it) (J)" | SK:73, SK:80; HW:20 | Y |
| P034 | [/sc:tdd](command-nuance/sc-tdd.md) | #10: 263-276 footprint table | no `/tdd` row | Add: "`/tdd`: folder `.dev/tasks/to-do/TASK-TDD-*/` (`research-notes.md` with `**Tier:**`, `research/`, `qa/`) plus the TDD file with frontmatter `type: \"📐 Technical Design Document\"` and `parent_doc`. Observed: 1 `TASK-TDD` folder (in `done/`, no task file) against 3 TDD files; location and QA file names vary, so the document alone does not prove the command ran" | Section 5 | N |
| P035 | [/sc:tdd](command-nuance/sc-tdd.md) | #11: 110 (`/sc:workflow` row Notes; the hint comes from CMD:184) | no mention of TDD | Add to the note: "CMD:184 recommends `/sc:workflow` after a TDD; for a TDD-sized feature use `/task-builder --spec <TDD>` (VAL)" | Section 4e | N |
| P036 | [/sc:tdd](command-nuance/sc-tdd.md) | #12: 281 (Section 5 intro) | Lists the files read in full and those read only by grep; `/tdd` is in neither list (only its frontmatter was read) | Add: "`/sc:tdd` command file, the `tdd` skill and its five refs were read in full (nuance file `sc-tdd.md`); its flags are defined only in the command file (U1)" | This file | N |
| P037 | [/sc:research](command-nuance/sc-research.md) | #1: Section 2.1, `/sc:research` row, R cell | `SKIP` | `OPTIONAL` | Re-rated under the new R definition (multi-feature release plan). The old SKIP read R as "assembles already-built work". A multi-feature release plan can hinge on an outside standard or shared dependency. Only cell that changes under the new R definition. (J) | Y |
| P038 | [/sc:research](command-nuance/sc-research.md) | #2: Same row, T/B/S/F/N cells | `SKIP / SKIP / OPTIONAL / OPTIONAL / WORTH IT` | unchanged | Matrix above agrees as a summary; F and R become WORTH IT only at HIGH complexity (J) | Y |
| P039 | [/sc:research](command-nuance/sc-research.md) | #3: Same row, Notes | `Outside knowledge only (library, standard). /tech-research is for our code` | `Outside knowledge only (library, standard). /tech-research is for our code. Depth by question difficulty: quick (one fact), standard (several facets), deep (high-stakes or ambiguous; the guide's mandatory flag for external-research, HWW:312). Use --strategy planning when unattended; the default unified waits for confirmation. Never REQUIRED. Backing skill sc-research-protocol does not exist; the command runs from its own file` | Adds the complexity layer and the flags that matter | Y |
| P040 | [/sc:research](command-nuance/sc-research.md) | #4: Section 3, O10 row, Why | `Guide section 5. The three BMad research skills are product/market framing; whether bmad-technical-research reads code or web is UNVERIFIED` | `Guide section 5. bmad-technical-research needs web search (SKILL.md:21), so it is the BMad twin of /sc:research, not of /tech-research. Pick by lane` | Resolves U8 | N |
| P041 | [/sc:research](command-nuance/sc-research.md) | #5: Section 4 "What a checker could observe" table | no `/sc:research` row | Add `/sc:research` -> `claudedocs/research_<topic>_<timestamp>.md` (only if committed; no depth recorded) -> CMD:104 | New footprint | N |
| P042 | [/sc:research](command-nuance/sc-research.md) | #6: Section 5, U8 | open | Mark resolved for the web/code question (web); `bmad-domain-research` and `bmad-market-research` still unread | See above | N |
| P043 | [/sc:adversarial](command-nuance/sc-adversarial.md) | #1: Row `/sc:adversarial`, section 2.1 (line 71) | `SKIP \| SKIP \| SKIP \| OPTIONAL \| SKIP \| OPTIONAL \| Only when two or more competing designs exist` | `SKIP \| SKIP \| OPTIONAL \| OPTIONAL \| OPTIONAL \| OPTIONAL \| Needs 2+ competing artifacts or every cell is SKIP. Complexity = number of artifacts, size, cost of a wrong pick: quick for N=2 small, standard default, deep rare, WORTH IT at HIGH for S/F/R/N. Not in Ryan's pipelines. Also runs inside /sc:brainstorm, /sc:reflect Tier 2, /sc:troubleshoot Tier 2, /sc:release-split: do not stack a manual run on those.` | No separate basis column in the source row; see the source file, sections 3 and 4 | Y |
| P044 | [/sc:adversarial](command-nuance/sc-adversarial.md) | #2: Same row, **S** cell | `SKIP` | `OPTIONAL` (J). Reason: a story-level approach debate has a precedent (`.dev/reviews/story-1-4-approach-debate-20260911`, N=2, quick) | No separate basis column in the source row; see the source file, sections 3 and 4 | Y |
| P045 | [/sc:adversarial](command-nuance/sc-adversarial.md) | #3: Same row, **R** cell (re-rating under the multi-feature definition) | `SKIP` (consistent with the 2.4 reading that a release "assembles and ships work already built", line 139) | `OPTIONAL` (J) at MEDIUM, WORTH IT at HIGH. Changed because a multi-feature release has a planning step with competing release plans; the neighbouring `/sc:release-split` row (line 72) is already WORTH IT at R and calls this command in Mode B | No separate basis column in the source row; see the source file, sections 3 and 4 | Y |
| P046 | [/sc:adversarial](command-nuance/sc-adversarial.md) | #4: Section 3, overlap O4 (line 230) | `/sc:adversarial is for choosing between two competing drafts, not for critique` | Append: `It also runs inside /sc:brainstorm (Wave 3), /sc:reflect Tier 2, /sc:troubleshoot Tier 2 and /sc:release-split; do not repeat it by hand there. 4 to 10 artifacts are allowed but no run above 3 exists on disk; each extra artifact adds a Round 1 and Round 2 call and grows Round 1 input.` | No separate basis column in the source row; see the source file, sections 3 and 4 | N |
| P047 | [/sc:adversarial](command-nuance/sc-adversarial.md) | #5: Section 4 footprint table (after line 265, `/sc:brainstorm`) | `.dev/brainstorms/<timestamp>-<name>/merged-requirements.md` | Add: `and adversarial/ (6 artifacts; brainstorm.md:193)` | No separate basis column in the source row; see the source file, sections 3 and 4 | N |
| P048 | [/sc:adversarial](command-nuance/sc-adversarial.md) | #6: Section 4 footprint table (new row) | no row for `/sc:adversarial` | `\| /sc:adversarial \| <output>/adversarial/{diff-analysis,debate-transcript,base-selection,refactor-plan,merge-log}.md`, a merged output, `variant-*.md`, `invariant-probe.md` (standard/deep only), sometimes `return-contract.yaml`; default location is next to the first input file \| SK:371-390, 605-606; observed 31 dirs \|` | No separate basis column in the source row; see the source file, sections 3 and 4 | N |
| P049 | [/sc:adversarial](command-nuance/sc-adversarial.md) | #7: Section 2.1 row `/sc:brainstorm` Notes (line 64) | `Guide: "only if the idea is still vague". --handoff task goes straight to a task file. ‡ with bmad-brainstorming` | Append: `Runs /sc:adversarial in Wave 3; --depth quick caps proposals at 2 (brainstorm.md:69).` | No separate basis column in the source row; see the source file, sections 3 and 4 | N |
| P050 | [/sc:adversarial](command-nuance/sc-adversarial.md) | #8: Section 2.2 rows `/sc:roadmap`, `/sc:tasklist` (lines 113-114) | no mention of the debate | Add to `/sc:roadmap`: `Its debate step is one LLM call inside superclaude roadmap run, not /sc:adversarial; its files (debate-transcript.md, base-selection.md) look like adversarial output but are not.` Note for `/sc:tasklist`: `adversarial.md:182` still lists it as a related command; it is retired (ruling 3). | No separate basis column in the source row; see the source file, sections 3 and 4 | N |
| P051 | [/sc:adversarial](command-nuance/sc-adversarial.md) | #9: Section 5 unverified list | n/a | Add the items from section 8 below that bear on the checker (U5, U9, U10) | No separate basis column in the source row; see the source file, sections 3 and 4 | N |
| P052 | [/sc:release-split](command-nuance/sc-release-split.md) | #1: CV:72 `/sc:release-split` row, R cell | `WORTH IT` | `WORTH IT` (R-MEDIUM and R-HIGH); `SKIP` at R-LOW (J) | Section 3 | Y |
| P053 | [/sc:release-split](command-nuance/sc-release-split.md) | #2: CV:72, F cell | `OPTIONAL` | `OPTIONAL` only at F-HIGH with a full spec and a foundation-versus-application seam; `SKIP` otherwise (J) | A single feature's release is a phase inside F (Ruling 2); HW:70 targets "work too big for one release"; SK:159 | Y |
| P054 | [/sc:release-split](command-nuance/sc-release-split.md) | #3: CV:72, N cell | `OPTIONAL` | `OPTIONAL` at MEDIUM/HIGH, `SKIP` at LOW (J) | `/roadmap` phases are already independently deployable (HW:75) | Y |
| P055 | [/sc:release-split](command-nuance/sc-release-split.md) | #4: CV:72, Notes | `Guide step 6 of full-spec: optional; "do not split" is a normal answer. Judgment: WORTH IT only at release size` | `Spec-phase step 6 of full-spec (HW:309), optional. Input is a release spec/TDD/roadmap (not a tasklist). Runs brainstorm and adversarial itself: do not run them first for the split question. Output in <spec-dir>/release-split/. If split: R1 spec replaces the TDD in the roadmap step and R2 is not planned until R1 is validated (HW:72). Part 3 may offer /sc:tasklist (retired) and /sc:workflow (not the F minimum): take specs only. "Do not split" is a valid result and counts as the command having run. Use --interactive at R-MEDIUM and above.` | Sections 1, 2, 4 | N |
| P056 | [/sc:release-split](command-nuance/sc-release-split.md) | #5: CV:256 R row, "WORTH IT additions" | `/sc:release-split, /task-builder / /roadmap for release steps, ...` listed after the three-step minimum | Move `/sc:release-split` out of the tail and put it at the start of the R path as "optional step 0 (R-MEDIUM+): record a split or no-split decision". Note that the three-step R minimum (reflect post, code-review, pr-submit) assumes already-built work (CV:139) and must be rebuilt for the new R definition: per-feature F pipelines plus release-level review and push. That rebuild is outside this command | Ruling 2; Section 6 | N |
| P057 | [/sc:release-split](command-nuance/sc-release-split.md) | #6: CV:257 N row, "WORTH IT additions" | lists `/sc:release-split` | Add "(run on the first release's spec; R1 spec replaces the TDD in `/roadmap`)" | HW:72 | N |
| P058 | [/sc:release-split](command-nuance/sc-release-split.md) | #7: CV:114 `/sc:tasklist` Notes | "Same separate pipeline. `superclaude` is on PATH here ..." | Add: "Also offered as a Part 3 option by `/sc:release-split` (SK:105, 272; CMD:136). Retired: do not take that option." | Ruling 3; a second programmatic mention beyond Stage 9 | N |
| P059 | [/sc:release-split](command-nuance/sc-release-split.md) | #8: CV:110 `/sc:workflow` Notes | "... ‡ with `/task-builder`" | Add: "Also offered as a Part 3 option by `/sc:release-split` (SK:270): not eligible for a multi-feature release." | VF:11 | N |
| P060 | [/sc:release-split](command-nuance/sc-release-split.md) | #9: CV:266-276 footprint table | no row for release-split | Add row: `<spec-dir>/release-split/`: `split-proposal.md`, `split-proposal-final.md` (frontmatter `adversarial:`), then `release-1-spec.md` + `release-2-spec.md` + `boundary-rationale.md` (split) or `release-spec-validated.md` (no split); always `fidelity-audit.md` (`## Verdict:`) and `release-split-report.md`. Source: PT/VP/SK templates; never observed (none found in this repo) | Section 5 | N |
| P061 | [/sc:release-split](command-nuance/sc-release-split.md) | #10: CV:298 U14 "Whether the team tags versions" | UNVERIFIED | Partly resolved: `git tag -l` shows `aidev02-v1.0` (2026-06-22) and `aidev02-v2-m2` (2026-07-09), and `.dev/releases/current/v2-m2/post-release/` holds a `post-release-report.md`, so tagging and `/sc:post-release` are in use here. No release-split output exists anywhere in the repo | observed on disk this session | N |
| P062 | [/sc:release-split](command-nuance/sc-release-split.md) | #11: CV:229 area, or new O-row | none | New overlap row "Decide one release or two": `/sc:release-split` (task-file lane) versus milestone planning (`bmad-correct-course`, `roadmap.md`, BMad lane; this repo's `v2-m3/00-revised-plan.md`). Pick by lane (J) | Section 4 | Y |
| P063 | [/sc:release-split](command-nuance/sc-release-split.md) | #12: `scenarios.md:40-41` (outside CV, for the merge step) | S6 lists "release split" among phases that run, "Allowed to skip: none" | Conflicts with HW:309 ("optional") and with CV. Change to "release split or an equivalent recorded split decision; skipping is fine for R-LOW" | HW:309; SC:40-41 | N |
| P064 | [/sc:workflow](command-nuance/sc-workflow.md) | #1: CV:110 `/sc:workflow`, T..N cells | `SKIP \| OPTIONAL \| REQUIRED \| OPTIONAL \| OPTIONAL \| SKIP` | Per scope with bands (LOW / MEDIUM / HIGH): T `SKIP / N/A / N/A`; B `SKIP / WORTH IT / SKIP`; S `REQUIRED (plan) / OPTIONAL either-or / SKIP`; F `OPTIONAL (J, 4.2 exception only) / SKIP / SKIP`; R `OPTIONAL (J, per-story only) / SKIP / SKIP`; N `SKIP`. One-cell summary if bands are not adopted: T SKIP, B WORTH IT (MEDIUM only), S REQUIRED (LOW), F SKIP, R SKIP, N SKIP | No separate basis column in the source row; see the source file, sections 3 and 4 | Y |
| P065 | [/sc:workflow](command-nuance/sc-workflow.md) | #2: CV:110 R cell (R re-rating) | `OPTIONAL` (rated under CV:139: a release "assembles and ships work already built") | `SKIP` at release level. Under Ryan's definition (multi-feature plan, implementation, push) a release is several F-scope features, each planned by `/task-builder` or `/roadmap`. Only per-story workflow plans inside a feature meeting 4.2 survive (R-LOW, J) | No separate basis column in the source row; see the source file, sections 3 and 4 | Y |
| P066 | [/sc:workflow](command-nuance/sc-workflow.md) | #3: CV:110 B cell | `OPTIONAL` ("B: only when the fix spans a few files") | `WORTH IT` for B-MEDIUM: it is the guide's route 3b (HW:132; HW:311), `--depth quick`. Keep `SKIP` for B-LOW and B-HIGH | No separate basis column in the source row; see the source file, sections 3 and 4 | Y |
| P067 | [/sc:workflow](command-nuance/sc-workflow.md) | #4: CV:110 Notes | "Guide level 3: `--depth quick`; plan is auto-checked against the request ..." | Append: "`--depth quick` for LOW, `standard` for MEDIUM or a spec-file source (only standard/deep check requirement coverage, QG:39). `--depth` never adds research or reviewers. Use `--handoff none`; `--handoff tasklist` prints a retired command; callers use `--depth standard --handoff none`." Keep VAL row 2's wording on the advisory check | No separate basis column in the source row; see the source file, sections 3 and 4 | N |
| P068 | [/sc:workflow](command-nuance/sc-workflow.md) | #5: CV:254 Single story, step 1 | "`/sc:workflow "<..>" --depth quick`" | "`/sc:workflow "<..>" --depth quick` (LOW) or `--depth standard` (MEDIUM, or source is a spec file); HIGH goes to `/task-builder` + `/task`" | No separate basis column in the source row; see the source file, sections 3 and 4 | N |
| P069 | [/sc:workflow](command-nuance/sc-workflow.md) | #6: CV:254 WORTH IT additions | "`/task-builder` + `/task` instead of steps 1-3 if the story is multi-session" | "... instead of steps 1-3 if any HW:18 trigger applies: more than 2 sessions, must not drift or a spec must be traced, files cannot be named, risk class touched, amendments expected (4.1 tests 1-6)" (extends VAL row 10) | No separate basis column in the source row; see the source file, sections 3 and 4 | N |
| P070 | [/sc:workflow](command-nuance/sc-workflow.md) | #7: CV:255 Multi-story feature | Task-file lane: steps 1-4 start with a spec file and `/task-builder` | Add one line: "Exception (J, needs Ryan): two or more independent LOW/MEDIUM stories with no feature spec may use one `/sc:workflow` plan each (4.2); this is tolerated, not the minimum" | No separate basis column in the source row; see the source file, sections 3 and 4 | Y |
| P071 | [/sc:workflow](command-nuance/sc-workflow.md) | #8: CV:232 O6 Turn spec into steps | "By size: `/sc:workflow` (S), `/task-builder` (F, R), `/roadmap` (N) ..." | "By size and band: `/sc:workflow` (S-LOW, S-MEDIUM, B-MEDIUM), `/task-builder` (S-HIGH, F, R), `/roadmap` (N). Tie at two sessions: heavier (HW:9)" | No separate basis column in the source row; see the source file, sections 3 and 4 | N |
| P072 | [/sc:workflow](command-nuance/sc-workflow.md) | #9: CV:259 Skippable at every size | lists `/sc:roadmap` + `/sc:tasklist` + `/sc:validate-roadmap` | Add "the `--handoff tasklist` option of `/sc:workflow`" (prints the retired `/sc:tasklist`, OR:8) | No separate basis column in the source row; see the source file, sections 3 and 4 | N |
| P073 | [/sc:workflow](command-nuance/sc-workflow.md) | #10: CV:266 `/sc:workflow` footprint row | `.dev/tasks/to-do/TASK-WF-*/<id>.md` and `progress.md`; `return-contract.yaml` with `reflect_status`; ... | Add what is observed: `done/` already holds 2 packages; frontmatter `schema: workflow-plan/1.2`; contract fields `depth`, `strategy`, `handoff_action`, `source_origin`; ledger lines `PLAN:`, `T<id>:`, `Ruling:`, `FINAL:`, `ARCHIVE:`; caller-built packages carry `remediation-source.md` or `diagnosability-plan-source.md` as source (section 5) | No separate basis column in the source row; see the source file, sections 3 and 4 | N |
| P074 | [/sc:workflow](command-nuance/sc-workflow.md) | #11: CV Section 5 intro (CV:281) | "For ... `/sc:implement`, `/sc:workflow` ... I read only the usage and flag lines" | Command file, protocol skill and all six refs of `/sc:workflow` have now been read in full (this file and VAL) | No separate basis column in the source row; see the source file, sections 3 and 4 | N |
| P075 | [/sc:workflow](command-nuance/sc-workflow.md) | #12: CV:256 Release row (cross-command, not mine to rate) | Minimum path starts at `/sc:reflect --mode post`; planning appears only under "WORTH IT additions" | Under the multi-feature definition planning is not optional; the release minimum should start from the per-feature plans. Left to the agents rating `/task-builder` and `/roadmap` | No separate basis column in the source row; see the source file, sections 3 and 4 | N |
| P076 | [/sc:roadmap](command-nuance/sc-roadmap.md) | #1: Row 113 `/sc:roadmap`, R and N columns | `OPTIONAL` / `OPTIONAL` | R: `OPTIONAL at HIGH complexity, else SKIP (J)`. N: `OPTIONAL at MEDIUM or HIGH, else SKIP (J)`. T, B, S, F stay `SKIP` | Section 3 matrix; R re-rated under the multi-feature-release definition | Y |
| P077 | [/sc:roadmap](command-nuance/sc-roadmap.md) | #2: Row 113 Notes | "Guide section 5: belongs to a separate release pipeline (`/sc:tasklist`, then `superclaude sprint run`). Use `/roadmap` unless the lead says otherwise. ‡ with `/roadmap`" | "Mirrors CLI `superclaude roadmap run`. Its designed next step `/sc:tasklist` is RETIRED, so output stops at `roadmap.md` / `extraction.md` / `test-strategy.md` and a person must carry it to `/task-builder` or `/roadmap`. Use `/roadmap` unless the lead says otherwise (HW:245). Overlaps `/roadmap` for the roadmap document only: only `/roadmap` ends in runnable task files. Not expected by a checker at any size." Drop the ‡ (it says "same job") | Sections 4.1, 4.3 | N |
| P078 | [/sc:roadmap](command-nuance/sc-roadmap.md) | #3: Row 114 `/sc:tasklist`, R and N | `OPTIONAL` / `OPTIONAL` | `SKIP` / `SKIP`; Notes: "RETIRED (Ryan, 2026-10-27). Never invoke; only programmatic caller of `/sc:task` (Stage 9). Legacy output in `.dev/releases/complete/v1.3-2026Upgrade/`." Remove "whether the team runs `superclaude sprint run` is UNVERIFIED" | Section 4.3 items 3-5 | N |
| P079 | [/sc:roadmap](command-nuance/sc-roadmap.md) | #4: Row 125 `/sc:validate-roadmap` Notes | "Only in the separate `/sc:roadmap` pipeline." | Append: "that pipeline's terminal step is retired; run only if `/sc:roadmap` was run" | Section 4.3 | N |
| P080 | [/sc:roadmap](command-nuance/sc-roadmap.md) | #5: Row 112 `/roadmap` Notes | "Guide level 6 step 7. Ask for a "full roadmap" or it stops at build requests. Runs at deepest setting by default" | Append: "Not the same tool as `/sc:roadmap`; they share only the name. `task-builder` text at TB:1668 wrongly says `/sc:roadmap` invokes `/task-builder`: it is `/roadmap` that does (RM:8, RM:660)" | Section 4.1 | N |
| P081 | [/sc:roadmap](command-nuance/sc-roadmap.md) | #6: O6 (CV:232) Why | "`/sc:roadmap` + `/sc:tasklist` are a separate release pipeline" | "`/sc:roadmap` is a separate planning pipeline whose tasklist step (`/sc:tasklist`) is retired; `/roadmap` is the release/new-product pick" | Section 4.3 | N |
| P082 | [/sc:roadmap](command-nuance/sc-roadmap.md) | #7: Section 4 "Release" row (CV:256) | Minimum = `/sc:reflect --mode post` per phase, `/code-review`, `/sc:pr-submit --monitor 1` | The multi-feature-release definition includes plan + implement + push, so the minimum needs a tasklist step: `/roadmap` or `/task-builder` per feature, before step 1. `/sc:roadmap` is not that step | Section 3 R re-rating; `/sc:roadmap` is not a minimum step | N |
| P083 | [/sc:roadmap](command-nuance/sc-roadmap.md) | #8: Section 4 "Skippable at every size" (CV:259) | "`/sc:roadmap` + `/sc:tasklist` + `/sc:validate-roadmap` (separate pipeline)" | "`/sc:tasklist` (retired: never invoke). `/sc:roadmap` and `/sc:validate-roadmap` (skippable; optional at R/N HIGH)" | Retirement differs from "skippable" | N |
| P084 | [/sc:roadmap](command-nuance/sc-roadmap.md) | #9: Section 4 footprint table (CV:262-276) | no `/sc:roadmap` row | Add: "`/sc:roadmap`: `<output>/.roadmap-state.json` with `steps`, plus `extraction.md`, `roadmap.md`, `test-strategy.md`, `diff-analysis.md`, `debate-transcript.md`, `base-selection.md`; key on the state file, not `generator:` (version drift). Name collision with `/roadmap`'s `.roadmap-state.json` (check for `steps` vs `input_hash`)" | Section 5 | N |
| P085 | [/sc:roadmap](command-nuance/sc-roadmap.md) | #10: Section 5 U6 (CV:290) | "Whether the team runs `superclaude sprint run`... Existence of the binary does not prove use" | Mark RESOLVED: run observed. `repo:.dev/releases/complete/v1.3-2026Upgrade/execution-log.jsonl` has `sprint_start` 2026-05-17, 8 phases, 192 tasks; archived 2026-06-24 (commit 730ca38f). Later releases use BUILD_REQUEST/task files | Section 4.3 item 5 | N |
| P086 | [/sc:roadmap](command-nuance/sc-roadmap.md) | #11: Section 5 (new row) | - | Add: "`/sc:roadmap` command file and protocol skill disagree on flags, default output dir, and resume flag; command file governs the CLI surface, skill governs the inference workflow (CMD:89, CMD:92). Which one an engineer actually hits: UNVERIFIED" | Section 2 conflicts | N |
| P087 | [/sc:spawn](command-nuance/sc-spawn.md) | #1: Section 2.2, line 115, `/sc:spawn` row, R column (R RE-RATING under "multi-feature release") | `SKIP` | `OPTIONAL (J)`. Changed because the old R reading ("a release assembles and ships work already built", line 139) made a planning tool irrelevant, while under Ryan's definition (full release plan) the batch-decomposition case (TOP9) belongs to R/HIGH. T, B, S, F, N stay `SKIP` | No separate basis column in the source row; see the source file, sections 3 and 4 | Y |
| P088 | [/sc:spawn](command-nuance/sc-spawn.md) | #2: Same row, Notes | `Guide "Other commands": for work that changes code, prefer /task-builder` | `Guide "Other commands" only (HW:262, HW:282); not in any workflow or the routing table. Stops after a task hierarchy (CMD:192-208), writes no executable tasklist, no output path, no backing skill, and no other skill consumes its output, so it never satisfies the Tasklist step. Flags: --strategy sequential\|parallel\|adaptive, --depth normal\|deep (defaults and effect not stated). R/HIGH only (a batch of independent items with cross-item ordering): OPTIONAL (J), single precedent .dev/plans/top9-issues-20261001/spawn-runbook.md, invocation UNVERIFIED. Rule 2.5 mentions retired /sc:task (CMD:124)` | No separate basis column in the source row; see the source file, sections 3 and 4 | Y |
| P089 | [/sc:spawn](command-nuance/sc-spawn.md) | #3: Section 3, line 232 (O6), Why cell | `... /sc:spawn is superseded by /task-builder` | `... /sc:spawn is superseded by /task-builder for code-changing work; for a batch of independent items it is OPTIONAL (J) at R/HIGH` | No separate basis column in the source row; see the source file, sections 3 and 4 | Y |
| P090 | [/sc:spawn](command-nuance/sc-spawn.md) | #4: Section 4, line 259 "Skippable at every size" | `... /sc:spawn, ...` | No change needed (OPTIONAL is skippable). Optional wording: add "(OPTIONAL (J) only for R/HIGH batches)" | No separate basis column in the source row; see the source file, sections 3 and 4 | Y |
| P091 | [/sc:spawn](command-nuance/sc-spawn.md) | #5: "What a checker could observe" table, after line 276 | no row | Add: `/sc:spawn` \| none defined; transcript only (no output path in CMD:203-208) \| sc-spawn.md section 5 | No separate basis column in the source row; see the source file, sections 3 and 4 | N |
| P092 | [/sc:spawn](command-nuance/sc-spawn.md) | #6: Section 1 inventory line 19 or section 5 unverified list | no mention that spawn has no backing skill | Add: "`/sc:spawn` has no backing protocol skill (`~/.claude/skills/sc-spawn-protocol/` missing); it runs from its command file" | No separate basis column in the source row; see the source file, sections 3 and 4 | N |
| P093 | [/sc:spawn](command-nuance/sc-spawn.md) | #7: Section 4 "Minimum viable path", Release row, WORTH IT additions | lists `/task-builder` / `/roadmap` for release steps | No change: spawn is not a minimum or WORTH IT item at any size | No separate basis column in the source row; see the source file, sections 3 and 4 | N |
| P094 | [/sc:reflect](command-nuance/sc-reflect.md) | #1: CV:124 | One row: `/sc:reflect` : SKIP SKIP OPTIONAL WORTH IT REQUIRED REQUIRED | Split into two rows. **`/sc:reflect --mode pre`**: T N/A, B SKIP, S OPTIONAL, F REQUIRED (automatic inside `/task-builder --spec`), R REQUIRED, N REQUIRED. **`/sc:reflect --mode post`**: T SKIP, B SKIP, S OPTIONAL, F WORTH IT (REQUIRED at HIGH), R REQUIRED, N REQUIRED. Only F-pre changes a rating (WORTH IT to REQUIRED, and only when a spec exists); the split makes the two modes' different triggers visible | HW:307 (`--spec` mandatory flag), TB:1664-1666, HW:81-83. F-pre REQUIRED is (J) | Y |
| P095 | [/sc:reflect](command-nuance/sc-reflect.md) | #2: CV:124, R column, and CV:256 Release row | R = REQUIRED, Release steps list only `--mode post --diff <commit> --no-promote` on each phase | Keep REQUIRED, but re-state it for the multi-feature meaning: (a) `--mode pre` on the release plan and on every phase task file against its spec, (b) `--mode post --no-promote` per phase of EVERY feature in the release, (c) one final `--mode post --depth deep --no-promote` over the whole release range with the release plan as `--tasklist`. Old reading looks like the shipping step of one feature, which the new ruling puts inside S or F | Brief ruling 2; SKILL:338-349 (interaction scan needs 3 or more tasks), SKILL:1055 and SKILL:1283 (large-diff behaviour). (b)-(c) are (J) | Y |
| P096 | [/sc:reflect](command-nuance/sc-reflect.md) | #3: CV:124 Notes | "`--mode pre` only when `reflect_pre` verdict is `skipped` or the plan is hand-written. S: `/sc:workflow` already self-checked" | "`--mode pre` by hand only when `reflect_pre` is `skipped` or the plan is hand-written AND a spec exists (without `--spec` it STOPs, CMD:32). S: `/sc:workflow` already ran an advisory pre against its own source at default depth (WP:56-58); rerun only against a separate spec (HW:191). Automatic callers: workflow Wave 4, task-builder A.10.7 and its POST item. Depth follows the task file's TCS, never below `standard` at post (TB:2440). Default `--mode post` MOVES a passing folder to `done/`; HW:322 mandates `--no-promote`" | Same as validation-feature row 14 (qualifies "self-checked") | N |
| P097 | [/sc:reflect](command-nuance/sc-reflect.md) | #4: CV:231, O5 row | "`/sc:reflect --mode pre` in the task-file lane" | Add: "run automatically by `/task-builder --spec` and by `/sc:workflow`; do not rerun when `reflect_pre.verdict` is `pass` or `fail`" | HW:190, TB:1701, WP:56 | N |
| P098 | [/sc:reflect](command-nuance/sc-reflect.md) | #5: CV:255 Multi-story row, "WORTH IT additions" | `/sc:reflect --mode post --no-promote` per phase | Keep. Add that it is REQUIRED (J) at HIGH complexity (TCS 35 or more, or refactor type), with `--depth deep` | TB:2433, TB:2438 | Y |
| P099 | [/sc:reflect](command-nuance/sc-reflect.md) | #6: CV:272, footprint row for `--mode pre` | "`.dev/reflect/pre-<name>-<timestamp>/` (post-mode path not stated in the guide: UNVERIFIED)" | Replace with the table in Section 5 of this file: hand-run default `.dev/reflect/<mode>-<slug>-<ts>/` for both modes; inside task-builder `<task-dir>/reflect/pre/`; CLI post `<task-dir>/reflect/post/<short-sha>/`; frontmatter `reflect_pre` and `reflect_post`; add the `.gitignore:32` caveat and the `report.md` versus `REPORT.md` mismatch | CMD:101, TB:1675, TB:2239; `.gitignore:32` | N |
| P100 | [/sc:reflect](command-nuance/sc-reflect.md) | #7: CV:267-268, `/task-builder` and `/task` footprint rows | `reflect_pre` block; `reflect_post` entry | Add the observed shapes: values may be a plain string or empty (`reflect_post: ""` before completion), keys may be quoted, extra keys exist | Observed in `.dev/tasks/to-do` files, see Section 5 | N |
| P101 | [/sc:reflect](command-nuance/sc-reflect.md) | #8: CV:281 | "For `/sc:reflect` ... I read only the usage and flag lines (grep)" | Update: `/sc:reflect` command file, `sc-reflect-protocol/SKILL.md` and its refs have now been read in full (this file) | This file's header | N |
| P102 | [/sc:reflect](command-nuance/sc-reflect.md) | #9: CV:297, U13 | "Post-mode output folder of `/sc:reflect` ... Guide gives only the pre-mode path" | Resolve the reflect half: same default folder pattern for both modes. The `/sc:pr-submit` log half stays open | CMD:101, SKILL:87 | N |
| P103 | [/sc:reflect](command-nuance/sc-reflect.md) | #10: CV Section 5 table | none for reflect depth | Add one line: depth is the only complexity dial; TCS 12 or less quick, 13-34 standard, 35 or more deep; post never quick | TB:2429-2440 | N |
| P104 | [/sc:validate-roadmap](command-nuance/sc-validate-roadmap.md) | #1: CV:125, `/sc:validate-roadmap` row, R and N cells | `OPTIONAL` / `OPTIONAL` (flat) | R: `OPTIONAL` base, banded: LOW SKIP, MEDIUM OPTIONAL, HIGH WORTH IT (J). N: banded: LOW N/A, MEDIUM OPTIONAL, HIGH WORTH IT (J). **R changed**: yes, from flat to banded, because under "multi-feature release" a roadmap coverage gap repeats per feature. Base stays OPTIONAL. All of it applies only to the `/sc:roadmap` lane. | No separate basis column in the source row; see the source file, sections 3 and 4 | Y |
| P105 | [/sc:validate-roadmap](command-nuance/sc-validate-roadmap.md) | #2: CV:125, Notes | `Only in the separate /sc:roadmap pipeline. /roadmap runs its own QA` | `Only for a /sc:roadmap output directory (roadmap.md, test-strategy.md, extraction.md); /roadmap output is not valid input. /sc:roadmap already validates by default (--no-validate skips it), so this is a re-run or deeper pass. Its documented next step /sc:tasklist is retired. Command file and skill disagree on flags and output layout (command-nuance/sc-validate-roadmap.md section 2).` | No separate basis column in the source row; see the source file, sections 3 and 4 | N |
| P106 | [/sc:validate-roadmap](command-nuance/sc-validate-roadmap.md) | #3: CV:231, O5 row, "Overlapping commands" and "Why" | lists `/sc:validate-roadmap`, `/sc:tasklist` integrated validation | Add: `/sc:validate-roadmap` applies only to `/sc:roadmap` outputs; `/sc:tasklist` is retired and drops out of the comparison. | No separate basis column in the source row; see the source file, sections 3 and 4 | N |
| P107 | [/sc:validate-roadmap](command-nuance/sc-validate-roadmap.md) | #4: CV:259, "Skippable at every size" | `/sc:roadmap + /sc:tasklist + /sc:validate-roadmap (separate pipeline)` | `/sc:tasklist` (retired). `/sc:roadmap` + `/sc:validate-roadmap` stay skippable at S and F; optional at R and N, as a pair, and a `/sc:roadmap` output has no documented continuation now (see unverified item 5). | No separate basis column in the source row; see the source file, sections 3 and 4 | N |
| P108 | [/sc:validate-roadmap](command-nuance/sc-validate-roadmap.md) | #5: CV:263-276, "What a checker could observe" | no `/sc:validate-roadmap` row | Add row: `/sc:validate-roadmap` / `/sc:roadmap` validation: `<out>/validate/validation-report.md` (frontmatter `blocking_issues_count`, `warnings_count`, `tasklist_ready`) and `reflect-<agent>.md`; `.roadmap-state.json` `validation.{status,timestamp}`. Source: observed in `_bmad-output/planning-artifacts/`. | No separate basis column in the source row; see the source file, sections 3 and 4 | N |
| P109 | [/sc:validate-roadmap](command-nuance/sc-validate-roadmap.md) | #6: CV:290, U6 "Whether the team runs `superclaude sprint run`" | `Existence of the binary does not prove use`; resolve by "look for `.dev/releases/` runs" | Add evidence: `/sc:roadmap` was run once (`_bmad-output/planning-artifacts/.roadmap-state.json`, `last_run` 2026-05-17, depth deep) and `.dev/releases/complete/v1.3-2026Upgrade/` holds `phase-1..8-tasklist.md`, `tasklist-index.md`, `execution-log.jsonl`, `manifest.json`. Both pipelines were used in the past; current use is still UNVERIFIED. | No separate basis column in the source row; see the source file, sections 3 and 4 | N |
| P110 | [/sc:validate-roadmap](command-nuance/sc-validate-roadmap.md) | #7: CV:113-114, `/sc:roadmap` and `/sc:tasklist` rows | R and N `OPTIONAL` for both | Out of scope for this file; cross-reference only: `/sc:tasklist` should read retired (SKIP everywhere) per brief ruling 3. | No separate basis column in the source row; see the source file, sections 3 and 4 | N |
| P111 | [/sc:swarm-wizard](command-nuance/sc-swarm-wizard.md) | #P1: Row at CVP:132 (Review phase, `/sc:swarm-wizard`) | `SKIP \| SKIP \| SKIP \| OPTIONAL \| OPTIONAL \| OPTIONAL \| Guide 3.6: real runs need a model proxy set in ~/.aienv (T2ProxyUrl, T2ProxyKey, T2Model01). Whether it is configured here is UNVERIFIED` | Keep the six letters as the LOW/MEDIUM baseline, add a complexity qualifier in Notes: `Never required. One file per run (cap 4000 lines), 2-4 reviewers, output is unscored and suspect: needs /sc:adversarial --suspect-source. Judgment: OPTIONAL at HIGH complexity for T, B, S; WORTH IT at HIGH for F, R, N on named high-risk files (secrets, permissions, infrastructure, data loss). Dry run alone is not a cross-model review. Real runs need T2ProxyUrl, T2ProxyKey, T2Model01; configured here UNVERIFIED.` | Cap and reviewer count from the CLI contract (CC:23-24); worth-it thresholds are (J) | Y |
| P112 | [/sc:swarm-wizard](command-nuance/sc-swarm-wizard.md) | #P2: R re-rating under "multi-feature release" | R = OPTIONAL | No letter changes for this command: R stays OPTIONAL at LOW/MEDIUM and becomes WORTH IT (J) at HIGH. The old R reading in CVP 2.4 ("a release assembles and ships work already built") was about build commands and never applied to this row, so nothing moves because of the redefinition. | No separate basis column in the source row; see the source file, sections 3 and 4 | Y |
| P113 | [/sc:swarm-wizard](command-nuance/sc-swarm-wizard.md) | #P3: Row O8 at CVP:234 | Current text lists `/sc:swarm-wizard` among "the other four are for extra assurance". | Append "swarm only at HIGH complexity, on one named file, and only if someone will triage its output". | No separate basis column in the source row; see the source file, sections 3 and 4 | N |
| P114 | [/sc:swarm-wizard](command-nuance/sc-swarm-wizard.md) | #P4: Row U5 at CVP:289 | "Not checked (env values must not be read or printed). Presence check of variable names only." | Keep, and add a second unknown: whether `uv run superclaude swarm` runs from this repo (no `pyproject.toml` at the repo root; `uv`, `superclaude`, `tmux` are on PATH). | No separate basis column in the source row; see the source file, sections 3 and 4 | N |
| P115 | [/sc:swarm-wizard](command-nuance/sc-swarm-wizard.md) | #P5: Note on HWW:291 vs wizard files | HWW says `sc-bare-review` "is internal (used by /sc:swarm-wizard...)". | No wizard file mentions `sc-bare-review`; the wizard drives `swarm run --lens bare-review` itself (CC:43). Record as a documented contradiction in the merged file (not resolvable from files). | CC:43; recorded in 6.4 of this file | N |
| P116 | [/sc:swarm-wizard](command-nuance/sc-swarm-wizard.md) | #P6: Section 3 or Section 4 of CVP (pairs) | (no pair row for the swarm lens) | Add: "swarm `edge-case-hunt` is the same job as `bmad-review-edge-case-hunter`; use the BMad skill by default." | CVP:128; CC:47 | N |
| P117 | [/sc:implement](command-nuance/sc-implement.md) | #1: CV:143, `/sc:implement` row, T..N cells | `SKIP \| OPTIONAL \| REQUIRED \| OPTIONAL \| SKIP \| SKIP` | `OPTIONAL \| OPTIONAL \| REQUIRED \| SKIP \| OPTIONAL \| SKIP`. Changes: T SKIP to OPTIONAL (VO row 129; rests on the PROPOSED T minimum); F OPTIONAL to SKIP (VF row 5, J); **R SKIP to OPTIONAL (J, Ruling 2)**. B stays OPTIONAL, S stays REQUIRED | Matrix in section 3. R: under Ruling 2 a release includes implementation, so the "R assembles work already built" reading no longer holds; `/sc:implement` shows up only as executor of S-size items inside it | Y |
| P118 | [/sc:implement](command-nuance/sc-implement.md) | #2: CV:143, Notes cell | "Runs `/sc:workflow` plans (`TASK-WF-*`). Resumes from first unfinished step. Stops with `E-HALT-QA` after two failed step checks. ‡ with `/task`" | "Executor for `/sc:workflow` plans (`TASK-WF-*`), hand-written plans, notes files, or one inline prompt (one task, ledger in `.dev/implement/<slug>/`). No `--depth`. Options: `--resume` (implicit), `--ledger`, `--skip-final-review` (never on a managed plan: blocks archiving). Never run it on a task-builder file. Resumes from first unfinished step; stops with `E-HALT-QA` after one failed fix pass. Rating holds in the `/sc:workflow` lane only; at S-HIGH and F use `/task-builder` + `/task`. ‡ overlaps `/task` at S size only" | Sections 2, 3; IM:53-59; IS:100,153 | N |
| P119 | [/sc:implement](command-nuance/sc-implement.md) | #3: CV:139, intro to Section 2.4 | "Reading of the R column in this phase: a release assembles and ships work already built at story or feature size, so build-the-code commands rate SKIP for R unless they check the assembled result." | "R = multi-feature release including its implementation (Ruling 2). Build-the-code commands rate R by the items inside the release: `/task` for F-size features, `/sc:implement` and `bmad-dev-story` only for S-size items. Release-level steps are review, push and docs." Note: the R cells of `/task` (CV:144, SKIP), `bmad-dev-story` (CV:146, SKIP) and `bmad-quick-dev` (CV:147, SKIP) rest on the old reading and need the same re-rating; other agents own those rows | Ruling 2; CV:139 | N |
| P120 | [/sc:implement](command-nuance/sc-implement.md) | #4: CV:276, last row of the footprint table | "`/code-review`, `/security-review`, `/sc:test`, `/sc:implement` (beyond `progress.md`), `/sc:git` \| No file footprint stated anywhere I read..." | Remove `/sc:implement` from that row. Add its own row: "`/sc:implement` \| prompt run: `.dev/implement/<slug>/source.md` + `progress.md`; file run: `.dev/implement/<slug>/progress.md` (header `source:` has the path); managed plan: `<pkg>/progress.md` with `PLAN:`, `FINAL:`, `ARCHIVE:` lines, package moves to `.dev/tasks/done/`; git ref `refs/superclaude/implement/<slug>/T<id>` only while a task is in flight. Real ledgers carry extra `retry`/`halt` lines the installed grammar does not define: match by line prefix, not whole-line regex" | Section 5 | N |
| P121 | [/sc:implement](command-nuance/sc-implement.md) | #5: CV:50, double-dagger legend, row 144 note for `/task` | "‡ ... two commands do the same job" | Add to the `/sc:implement` / `/task` pair: "never swap inputs: task-builder file to `/task`, `TASK-WF-*` to `/sc:implement`". The task-builder-to-implement direction is a convention (IS:78 does not refuse it); the `TASK-WF`-to-`/task` direction is stated at HW:216 | Section 2c | N |
| P122 | [/sc:implement](command-nuance/sc-implement.md) | #6: CV:254 and CV:252 | Single-story and one-off rows list `/sc:implement <plan path>` in step 3 and `/sc:task` in step 1 | S step 3: append "(creates `progress.md` beside the plan; on Linux the package moves to `done/` after a fresh FINAL; do not pass `--skip-final-review`)". T step 1 per VO row 132 | IM:63-65; MW:44-62; HW:17 | N |
| P123 | [/sc:implement](command-nuance/sc-implement.md) | #7: CV Section 5 (unverified), add rows | - | Add: the extra ledger record kinds (U3 below), the `.dev/tasks/archive/` folder (U4 below), and that `--resume` is a no-op | Section 8 | N |
| P124 | [/sc:test](command-nuance/sc-test.md) | #P1: CVP:150, 2.4 row `/sc:test`, S cell | S = WORTH IT | S = OPTIONAL (J). WORTH IT only at MEDIUM test-target size (a module folder, once before commit), because `/sc:implement` and `/task` already run tests (HWW:81, 117, 226; VO E3.5) | No separate basis column in the source row; see the source file, sections 3 and 4 | Y |
| P125 | [/sc:test](command-nuance/sc-test.md) | #P2: CVP:150, same row, T / B / F / R / N cells | T WORTH IT, B WORTH IT, F OPTIONAL, R WORTH IT, N OPTIONAL | Ratings unchanged. Add a complexity qualifier in Notes: T WORTH IT at LOW only; B WORTH IT at LOW (guide step 3a), SKIP at HIGH; F SKIP at LOW/MEDIUM, OPTIONAL at HIGH. R: rating unchanged, rationale re-based (see P5) | No separate basis column in the source row; see the source file, sections 3 and 4 | Y |
| P126 | [/sc:test](command-nuance/sc-test.md) | #P3: CVP:150, same row, Notes | "Running the related test is mandatory in the guide (levels 2, 3, bug route 3a); this command is one way. F: `/task` runs tests itself. Does not write tests. Also in Bug-fix phase" | "The ACTIVITY (run the related test) is mandatory in the guide (levels 2, 3, bug route 3a); this command is one way, not a gate: `implement.md:140` calls it optional, CI is the gate (repo `CLAUDE.md`). Flags: `[target] [--type unit\|integration\|e2e\|all] [--coverage] [--watch] [--fix]` (`test.md:22`); no `--depth`. Does not write tests (`test.md:104`). No backing protocol skill (`sc-test-protocol` absent; expected, HWW:232). Leaves no file footprint. Guide names it only in bug step 3a with `--coverage` (HWW:311). Avoid `--watch` in unattended runs; `--fix` is undefined (see section 8)" | No separate basis column in the source row; see the source file, sections 3 and 4 | N |
| P127 | [/sc:test](command-nuance/sc-test.md) | #P4: CVP:180 | "`/sc:test` (reproduce, then confirm; 2.4)" | "`/sc:test` (confirm the fix after a failing test was written and the fix made, HWW:131, 311; 2.4)". The command file does not reproduce bugs; it runs existing tests (`test.md:98`) | No separate basis column in the source row; see the source file, sections 3 and 4 | N |
| P128 | [/sc:test](command-nuance/sc-test.md) | #P5: CVP:139 and Section 4 Release row (CVP:256) | R reading: "a release assembles and ships work already built ... unless they check the assembled result"; additions list "`/sc:test` full run" | Under the multi-feature release definition (brief ruling 2): `/sc:test --type all [--coverage]` stays WORTH IT at MEDIUM and HIGH as a cross-feature regression signal before push, labelled "pre-push signal; CI is the gate". Rating did not change; the reason did. In this repo a full local run may not reproduce the gate, because the contract suite runs inside a built image (`coder-ci-aidev02-contract.yml:1,1158-1163`) | No separate basis column in the source row; see the source file, sections 3 and 4 | Y |
| P129 | [/sc:test](command-nuance/sc-test.md) | #P6: CVP:253 (Bug fix) | step 3 "run the test"; additions "`/sc:test`, `/code-review`" | Step 3: "run the test (`/sc:test <test path> --coverage` per HWW:131, 311, or the plain runner)". Drop `/sc:test` from the additions because it is now in the path | No separate basis column in the source row; see the source file, sections 3 and 4 | N |
| P130 | [/sc:test](command-nuance/sc-test.md) | #P7: CVP:254 (Single story) and CVP:252 (One-off) | additions include `/sc:test` | S: "`/sc:test <module>` at MEDIUM complexity only". T: unchanged (WORTH IT at LOW; the proposed one-off minimum, plain edit plus related test, is still PROPOSED per VO) | No separate basis column in the source row; see the source file, sections 3 and 4 | Y |
| P131 | [/sc:test](command-nuance/sc-test.md) | #P8: CVP:276 footprint row | "`/code-review`, `/security-review`, `/sc:test`, ... No file footprint stated anywhere I read" | Split out `/sc:test`: "none defined. `test.md:52` lists a Write for 'coverage reports and test summaries' with no path; routing row `tests` is `changes_files: no` (HWW:319). Nothing found in `claudedocs/`, `.gitignore`, `.dev/` on 2026-10-27. A checker should use CI check status and test files in the diff instead" | No separate basis column in the source row; see the source file, sections 3 and 4 | N |
| P132 | [/sc:test](command-nuance/sc-test.md) | #P9: CVP:281 (Unverified preamble) | "`/sc:test` ... I read only the usage and flag lines (grep)" | `/sc:test` file read in full (107 lines) for this nuance pass; no protocol skill exists | No separate basis column in the source row; see the source file, sections 3 and 4 | N |
| P133 | [/sc:build](command-nuance/sc-build.md) | #1: Row `/sc:build` in section 2.4 (line 152) | `\| /sc:build \| Build, compile, and package projects ... \| SKIP \| SKIP \| OPTIONAL \| OPTIONAL \| OPTIONAL \| OPTIONAL \| Guide: "Build or package the project". CLAUDE.md says validation goes through .github Actions; local build is a convenience, CI is the gate \|` | (this repo, J): `\| ... \| SKIP \| SKIP \| SKIP \| OPTIONAL \| OPTIONAL \| OPTIONAL \| No backing protocol skill exists, so flags are only those on the usage line (--type, --clean, --optimize, --verbose, [target]); --validate appears only in an example. Never REQUIRED. In this repo the image and Orca package builds run only in CI (build-deb.sh:22), and no package.json/Makefile exists, so a local run is rarely possible. For a build failure use /sc:troubleshoot --type build. HIGH-complexity N (after a build config exists): WORTH IT (J) \|` | build-deb.sh:22 refuses to run outside Actions; no root build manifest; CI is the gate (CLAUDE.md) | Y |
| P134 | [/sc:build](command-nuance/sc-build.md) | #2: Cell S (row `/sc:build`) | OPTIONAL | SKIP (this repo) | CI is the gate; no local build target (`build-deb.sh:22`, find result) | Y |
| P135 | [/sc:build](command-nuance/sc-build.md) | #3: Cells T, B, F, N (row `/sc:build`) | SKIP, SKIP, OPTIONAL, OPTIONAL | unchanged (B is OPTIONAL only at HIGH complexity in the matrix) | No separate basis column in the source row; see the source file, sections 3 and 4 | N |
| P136 | [/sc:build](command-nuance/sc-build.md) | #4: Cell R (row `/sc:build`) | OPTIONAL | OPTIONAL, unchanged. Re-rated under "multi-feature release including implementation and push": the release build is a CI job, local build adds nothing the gate does not; rating holds. | Release build is a CI job | N |
| P137 | [/sc:build](command-nuance/sc-build.md) | #5: Related note for the merge step (not this command's row): the 2.4 intro (line 139) | Reads R as "assembles and ships work already built at story or feature size", so build-the-code commands rate SKIP for R. | Under the new R definition a multi-feature release includes its own implementation, so that sentence no longer holds; `/sc:implement`, `/task` and others rated SKIP in R on that reading need re-rating by their own agents. | Ruling 2 | N |
| P138 | [/sc:build](command-nuance/sc-build.md) | #6: Line 276 (footprint table) | (`/sc:build` not listed in the no-footprint row) | Add `/sc:build` to the "No file footprint stated anywhere" row. | build.md:52 names no report path | N |
| P139 | [/sc:improve](command-nuance/sc-improve.md) | #1: 153, `/sc:improve` row, T/B/S/F/R/N cells | `SKIP \| SKIP \| OPTIONAL \| OPTIONAL \| SKIP \| SKIP` | `OPTIONAL (J) \| SKIP \| OPTIONAL \| OPTIONAL \| OPTIONAL (J) \| SKIP`. T changes only because a folder-wide tidy is itself a one-off and is the case the guide's exception exists for (HWW:22): Ryan to confirm that reading. R changes under ruling 2 (R was SKIP under the "assembles built work" reading, CV:139) | No separate basis column in the source row; see the source file, sections 3 and 4 | Y |
| P140 | [/sc:improve](command-nuance/sc-improve.md) | #2: 153, Notes | "Guide 3.7: commit first, `--safe --interactive`, review `git diff`. The one allowed exception to the five-edit limit" | "Off-pipeline hygiene step; never REQUIRED, never credited as the implement step. Guide 3.7 and routing row `cleanup` (HWW:318): after `/sc:cleanup`, run `--type quality --safe --interactive`, commit first, review `git diff`. The exception to the five-edit limit covers small, contained FOLDER cleanups only (HWW:22, 163); structural refactors go `/task-builder --spec` + `/task` (HWW:168). No file footprint. Backing protocol skill does not exist; `--safe`, `--interactive`, `--preview`, `--validate`, `--force` are not defined in any file read." | No separate basis column in the source row; see the source file, sections 3 and 4 | N |
| P141 | [/sc:improve](command-nuance/sc-improve.md) | #3: 139, R reading under 2.4 | "a release assembles and ships work already built at story or feature size, so build-the-code commands rate SKIP for R unless they check the assembled result" | Replace under ruling 2: R is a multi-feature release including plan, implementation and push, so implement-phase commands inside R follow the F ratings unless a row says otherwise. This affects every 2.4 row, not only `/sc:improve`: merge step to re-rate | No separate basis column in the source row; see the source file, sections 3 and 4 | N |
| P142 | [/sc:improve](command-nuance/sc-improve.md) | #4: after 241 (Section 3, O15) | none | Add O16 "Tidy or improve existing code": `/sc:cleanup-audit`, `/sc:cleanup`, `/sc:improve`, `/simplify`, `/sc:analyze`. Pick: folder tidy = audit, commit, cleanup, improve, review diff (HWW:318); code you just changed = `/simplify`; structural = task file (HWW:168). Reason: `/sc:cleanup` and `/sc:improve` share guard rails and auto-fix lists (CLN:109-115, IMP:110-115) | No separate basis column in the source row; see the source file, sections 3 and 4 | N |
| P143 | [/sc:improve](command-nuance/sc-improve.md) | #5: 259, "Skippable at every size" | list without hygiene commands | Add a line: "Never counted as a missing step: `/sc:improve`, `/sc:cleanup`, `/sc:cleanup-audit`, `/simplify`, `/sc:analyze`" (J; none is REQUIRED at any size) | No separate basis column in the source row; see the source file, sections 3 and 4 | Y |
| P144 | [/sc:improve](command-nuance/sc-improve.md) | #6: 276, no-footprint row | lists `/code-review`, `/security-review`, `/sc:test`, `/sc:implement`, `/sc:git` | Add `/sc:improve`: "no output path defined (IMP:31); only the git diff and transcript; no `improve` folder under `.dev/` (observed 2026-10-27)" | No separate basis column in the source row; see the source file, sections 3 and 4 | N |
| P145 | [/sc:improve](command-nuance/sc-improve.md) | #7: Section 5 (add rows) | none | Add the unverified items 1-8 below (flags undefined, approval/exception conflict, missing protocol skill) | No separate basis column in the source row; see the source file, sections 3 and 4 | N |
| P146 | [/sc:cleanup](command-nuance/sc-cleanup.md) | #1: value:154 `/sc:cleanup`, T cell | SKIP | OPTIONAL (J). A standalone "tidy a folder / dead code / unused imports" job is the guide's own one-off row (HWW:318) and the one allowed exception to the 5-edit limit (HWW:22). | No separate basis column in the source row; see the source file, sections 3 and 4 | Y |
| P147 | [/sc:cleanup](command-nuance/sc-cleanup.md) | #2: value:154, B / S / F / N cells | SKIP / OPTIONAL / OPTIONAL / SKIP | No change to the single letters. Add the complexity layer from section 3: S and F are OPTIONAL at LOW, F is WORTH IT at MEDIUM, HIGH is not a direct run. | No separate basis column in the source row; see the source file, sections 3 and 4 | Y |
| P148 | [/sc:cleanup](command-nuance/sc-cleanup.md) | #3: value:154, R cell (re-rated under the multi-feature release definition) | OPTIONAL | OPTIONAL at LOW, WORTH IT at MEDIUM, SKIP direct run at HIGH (J). Letter-level cell stays OPTIONAL; the change is the MEDIUM nuance, backed by `audit-skill:19` ("pre-release cleanup"). N stays SKIP (OPTIONAL only late at HIGH). | No separate basis column in the source row; see the source file, sections 3 and 4 | Y |
| P149 | [/sc:cleanup](command-nuance/sc-cleanup.md) | #4: value:139 (reading of the R column in Implement) | "a release assembles and ships work already built at story or feature size, so build-the-code commands rate SKIP for R unless they check the assembled result" | Reading no longer matches the redefined R (a multi-feature release includes planning, implementation and push). It does not change this row's cell, but the merge step should reword it. | No separate basis column in the source row; see the source file, sections 3 and 4 | N |
| P150 | [/sc:cleanup](command-nuance/sc-cleanup.md) | #5: value:154 Notes | "Same guard rails as `/sc:improve`" | "Backing skill `sc-cleanup-protocol` does not exist; runs from its own file. NOT the same guard rails as `/sc:improve`: it has no `--force` and no stated rule for whole-file removal. Auto-applies unused imports, zero-reference code, empty blocks, redundant annotations even with `--interactive`. Commit first; always `--type code --safe --interactive`; give an explicit folder; never point it at `.dev/`, `_bmad-output/`, `.github/`. No output file: checker sees the git diff only." | No separate basis column in the source row; see the source file, sections 3 and 4 | N |
| P151 | [/sc:cleanup](command-nuance/sc-cleanup.md) | #6: value:155 `/sc:cleanup-audit` Notes | "Report only (`--pass all`); run before `/sc:cleanup`" | Add: "Excludes hidden paths and `_bmad*` directories (so not `.github/`, `.dev/`, `_bmad-output/`). Output `.claude-audit/` is untracked in this repo. `/sc:cleanup` has no input flag for the report: hand it the 'Immediate' paths by hand. Run first for whole-file deletions or HIGH work." Its R cell (OPTIONAL) deserves a re-rate to WORTH IT at MEDIUM and HIGH (J): `audit-skill:19`; the audit command's own nuance file should confirm. | No separate basis column in the source row; see the source file, sections 3 and 4 | Y |
| P152 | [/sc:cleanup](command-nuance/sc-cleanup.md) | #7: value:243 | "Not overlaps despite similar names: ... `/sc:cleanup-audit` (report) versus `/sc:cleanup` (edits)." | Keep, but add that they are a sequenced pair, not alternatives (`audit-cmd:119`, HWW:318). | No separate basis column in the source row; see the source file, sections 3 and 4 | N |
| P153 | [/sc:cleanup-audit](command-nuance/sc-cleanup-audit.md) | #1: Section 2.4, row `/sc:cleanup-audit` (line 155), T / B / S / F / R / N cells | `SKIP / SKIP / SKIP / OPTIONAL / OPTIONAL / SKIP` | `SKIP / SKIP / OPTIONAL / OPTIONAL / WORTH IT / SKIP`. Changes: S up one step, R up one step | S: a story that deletes or moves files with unknown referrers can use `--pass surface` (J). R: see row 3 | Y |
| P154 | [/sc:cleanup-audit](command-nuance/sc-cleanup-audit.md) | #2: Same row, Notes | `Report only (`--pass all`); run before `/sc:cleanup`` | `Report only at every --pass; writes untracked .claude-audit/ (not gitignored here). Step 1 of the cleanup route (guide 3.7, routing row cleanup) with --pass all. Size decides, not scope: judgment says skip for a target of 50 in-scope files or fewer (go straight to /sc:cleanup or grep). It cannot see hidden or BMad folders (.github, .dev, .claude, _bmad*), 94.6% of this repo's tracked files. No input flag on /sc:cleanup reads its report; hand-off is manual` | "Report only (`--pass all`)" reads as if `--pass all` makes it report-only; every pass is read-only (`CA:103-110`) | Y |
| P155 | [/sc:cleanup-audit](command-nuance/sc-cleanup-audit.md) | #3: Section 2.4 intro (line 139), R reading | `a release assembles and ships work already built at story or feature size, so build-the-code commands rate SKIP for R unless they check the assembled result` | Under Ryan's ruling 2 a release is multi-feature and includes plan, implementation and push. Replace with: `a release is multi-feature and includes planning, implementation and push; commands that look for accumulated leftovers across features rate higher for R` | Re-rating of R for this command: OPTIONAL to WORTH IT at MEDIUM/HIGH (OPTIONAL at LOW), anchored on `SK:19` "Pre-release cleanup to reduce attack surface and deployment weight". Still judgment: not REQUIRED, because no pipeline of Ryan's names it | Y |
| P156 | [/sc:cleanup-audit](command-nuance/sc-cleanup-audit.md) | #4: Section 4, Release row, "WORTH IT additions" (line 256) | list without `/sc:cleanup-audit` | add `/sc:cleanup-audit <path> --pass all` (MEDIUM or HIGH target) | Consistent with row 1. Multi-story feature row (line 255): no addition | N |
| P157 | [/sc:cleanup-audit](command-nuance/sc-cleanup-audit.md) | #5: Section 3 "Not overlaps" (line 243) | `/sc:cleanup-audit` (report) versus `/sc:cleanup` (edits) | append: `; the report does not feed /sc:cleanup automatically, and the audit is not a delivery step in any of Ryan's pipelines` | `CL:22`, `CL:27-31` | N |
| P158 | [/sc:cleanup-audit](command-nuance/sc-cleanup-audit.md) | #6: Section 3, new overlap row (after O15) | none | `O16 \| Cleanup route \| /sc:cleanup-audit, /sc:cleanup, /sc:improve, plain git grep + git rm \| Audit first for MEDIUM/HIGH targets, file-level actions, unknown referrers, or stale-doc doubt; straight to /sc:cleanup (or grep) for 50 in-scope files or fewer (J) \| guide 3.7; SK:16-20; CL:109-127` | Section 4 of this file | Y |
| P159 | [/sc:cleanup-audit](command-nuance/sc-cleanup-audit.md) | #7: Section 4, footprint table (lines 263-276) | no row for this command | add: `/sc:cleanup-audit \| .claude-audit/pass1-summary.md, pass2-summary.md, pass3-summary.md, pass{N}/batch-NN.md, progress.json, final report (file name unverified); header line "Passes Completed" shows which --pass ran; untracked in this repo, so absent from PR diffs \| protocol templates` | Section 5 of this file | N |
| P160 | [/sc:cleanup-audit](command-nuance/sc-cleanup-audit.md) | #8: Section 5 unverified list | no item | add U-items for: Pass 1 model mismatch (command says Haiku, agent file says sonnet); no real run observed; routing table makes `--pass all` mandatory vs size-based leniency | Section 8 of this file | N |
| P161 | [/sc:git](command-nuance/sc-git.md) | #1: CVP line 163 (`/sc:git` row, Notes column) | `Committing regularly is mandatory (Ryan, pipeline step 4); plain `git` does the same. Guide: "never push without approval". How `--smart-commit` treats `.dev/tasks` (which `CLAUDE.md` says must always be staged) is UNVERIFIED` | `Committing regularly is mandatory (Ryan, pipeline step 4); the command is optional, plain `git` does the same. Cadence by scope: T/B/S-LOW one commit; S-MEDIUM and above and all of F/R/N one per task-file phase (/task does not commit). Resolved from the command file: it says nothing about `.dev/tasks` or staging, so it does not enforce the repo rule; stage `.dev/tasks` yourself (plain `git add .dev/tasks`) before committing. Guide: "never push without approval"; the command file does not say it asks before push` | Command file (91 lines) read in full: no mention of `.dev/tasks`, no staging policy (sc-git.md section 7 resolution paragraph). Cadence beyond "per phase" is (J) | Y |
| P162 | [/sc:git](command-nuance/sc-git.md) | #2: CVP line 241 (O15 row) | `Judgment. How `/sc:git` handles `.dev/tasks` staging is UNVERIFIED` | `Judgment. `/sc:git` does not define staging (command file silent), so use plain `git` when staging must be exact` | Same resolution as item 1 | N |
| P163 | [/sc:git](command-nuance/sc-git.md) | #3: CVP line 276 (footprint row listing `/sc:git`) | `No file footprint stated anywhere I read. Only visible in a session transcript or PR comments: UNVERIFIED` | Split `/sc:git` out: `No file footprint (command file names none). The commit itself is visible in `git log`; the checker should count commits per phase, not the command. Conventional message style and the `Co-Authored-By` trailer do not identify `/sc:git`` | Command file names no output file; commit style and trailer come from the session (sc-git.md section 5) | N |
| P164 | [/sc:git](command-nuance/sc-git.md) | #4: CVP line 296 (U12) | `Whether `/sc:git --smart-commit` respects the "always stage `.dev/tasks`" rule ... command body not read` | Mark RESOLVED: command file read in full; silent on staging; behaviour at run time still UNVERIFIED (see U1 in sc-git.md). | Command file read in full | N |
| P165 | [/sc:git](command-nuance/sc-git.md) | #5: CVP line 256 (Release scenario row, "Fewest" column) | `1. `/sc:reflect --mode post --diff <commit> --no-promote` on every phase of the release 2. `/code-review` on the full branch 3. `/sc:pr-submit --monitor 1`` | Add the commit step, matching the other rows: `... 1. commit per phase 2. `/sc:reflect --mode post ...` on every phase 3. `/code-review` 4. `/sc:pr-submit --monitor 1``. The `/sc:git` column cell for R stays OPTIONAL; this is a cadence fix, not a re-rating of the command. Under the new multi-feature R definition the commit count is higher (per phase of each feature) (J). | Commit between implement and push is required by Ryan's pipeline; cadence per feature is (J) | Y |
| P166 | [/sc:git](command-nuance/sc-git.md) | #6: CVP line 163, columns T..N | all six OPTIONAL | All six stay OPTIONAL (no change); the command does not vary by scope or complexity. | No separate basis column in the source row; see the source file, sections 3 and 4 | N |
| P167 | [/sc:auggie-review](command-nuance/sc-auggie-review.md) | #1: CV:166 `/sc:auggie-review` row, Notes | "Guide step 4: `--diff origin/<main>...HEAD --no-post-pr`. Default on a PR number posts publicly. Judgment: WORTH IT, not REQUIRED, because it overlaps `/code-review` and the PR bot" | "Guide step 4: `--diff origin/<main>...HEAD --no-post-pr`. Always add `--no-post-pr` with a PR number: the default posts a public review with no prompt (CMD:52) and quotes diff code, so a secret in the diff would be copied into the PR. Not available above 5000 diff lines (SKILL:138; observed STOP at `--depth quick`). Default `--depth standard`; `deep` (10-15 min) only for a risk trigger (J). Remediation offer routes by review depth, not fix size; for F-size fixes build with `/task-builder --spec` instead (section 4 of the nuance file). Not worth it at LOW complexity (J)" | Covers the posting risk, the size ceiling and the depth/risk rule | Y |
| P168 | [/sc:auggie-review](command-nuance/sc-auggie-review.md) | #2: CV:166 ratings T B S F R N = SKIP OPTIONAL WORTH IT WORTH IT WORTH IT WORTH IT | as listed | Keep T=SKIP, B=OPTIONAL, N=WORTH IT. Change S to "OPTIONAL at LOW, WORTH IT at MEDIUM and HIGH" (J). F stays WORTH IT. R: see row 3 | Only data point: a `standard` review of 12 files / 321 lines found 0 issues (REV pr-322), against deep reviews with 12-13 findings (pr-266, pr-43). Thin evidence, so JUDGMENT | Y |
| P169 | [/sc:auggie-review](command-nuance/sc-auggie-review.md) | #3: CV:166, R column; CV:139 R reading; CV:256 Release row | R = WORTH IT; CV:256 additions list `/sc:auggie-review` | Rating stays WORTH IT but the meaning changes under the multi-feature definition: run it per feature PR diff, plus optionally once on an integration diff; a single run over the whole release will exceed 5000 lines and STOP (SKILL:138; observed 286 files / 32,834 lines in REV pr-151). Use `--snapshot <risky subtree>` for cross-feature structure | The old R reading (one assembled release diff) cannot run; the new reading (several features) is where the size ceiling bites. Rating unchanged, usage rewritten | N |
| P170 | [/sc:auggie-review](command-nuance/sc-auggie-review.md) | #4: CV:234 O8 "Review code before push", Why column | "`/sc:auggie-review` adds a whole-branch view; the other four are for extra assurance" | "`/sc:auggie-review` adds a whole-branch view for diffs up to 5000 lines (it STOPs above that); use `--no-post-pr`. The built-in `/code-review` and `bmad-code-review` are the bug reviews; do not run `bmad-code-review` and this on the same diff as two 'one bug review' steps" | Size ceiling; same job as bmad-code-review (BMCR step-02) | N |
| P171 | [/sc:auggie-review](command-nuance/sc-auggie-review.md) | #5: CV Section 4 footprint table (after CV:276) add a row | `/sc:auggie-review` has no row; CV:276 lists `/code-review` etc. as "no file footprint" | Add: "`/sc:auggie-review`: `.dev/reviews/<pr-N or diff-... or snapshot-...>-<timestamp>/REVIEW.md` (header `Reviewer: /sc:auggie-review (depth=...)`), `audit.log` with `SC:AUGGIE-REVIEW:TARGET` and `:SUMMARY` comment headers (SKILL:103-114, 296-303); `claude-side-review.json` marks `deep`. Folder is tracked by git here. A PR post is visible only on GitHub. A folder with `Status: Failed` is not a review" | Brief section 5; observed folders | N |
| P172 | [/sc:auggie-review](command-nuance/sc-auggie-review.md) | #6: CV:135 and CV:166 "overlap" wording; CV:233 O7 | O7 says execute with `/sc:implement`, `/task`, ... by input file | Add a sentence under O6/O7: "A `TASK-WF-*` plan or task-builder file created from `/sc:auggie-review`'s remediation offer is a valid artifact of that chain. Route is keyed on review depth (quick/standard -> workflow, deep -> task-builder), which can disagree with the F-size rule; the checker should not flag it" | Section 4 lane note | N |
| P173 | [/sc:auggie-review](command-nuance/sc-auggie-review.md) | #7: CV Section 5 unverified (new U19) | - | Add: "`offer-pr-review.sh` named in CMD:18 and `pr-submit.md:19` does not exist on this machine (find + settings.json); whether other engineers have it is UNVERIFIED" | Hook search result | N |
| P174 | [/sc:auggie-review](command-nuance/sc-auggie-review.md) | #8: CV Section 5 intro (CV:281) | "I read only the usage and flag lines" for several commands | `/sc:auggie-review` command file, `sc-auggie-review-protocol` SKILL.md and its three refs and eval file have now been read in full (this file) | Coverage statement | N |
| P175 | [/sc:pr-submit](command-nuance/sc-pr-submit.md) | #1: Line 167, `/sc:pr-submit` row, T/B/S/F columns | REQUIRED (x4) | REQUIRED (x4), unchanged. Complexity changes flags, not the rating | No separate basis column in the source row; see the source file, sections 3 and 4 | N |
| P176 | [/sc:pr-submit](command-nuance/sc-pr-submit.md) | #2: Line 167, R column | REQUIRED | REQUIRED, rating unchanged under the multi-feature definition. Reason: it was already REQUIRED and a multi-feature release is HIGH complexity by definition; what changes is the Notes (below). R re-rated: no rating change | No separate basis column in the source row; see the source file, sections 3 and 4 | N |
| P177 | [/sc:pr-submit](command-nuance/sc-pr-submit.md) | #3: Line 167, N column | REQUIRED | REQUIRED, unchanged; add "`--monitor 0` until the Augment app is on the new repo" | No separate basis column in the source row; see the source file, sections 3 and 4 | N |
| P178 | [/sc:pr-submit](command-nuance/sc-pr-submit.md) | #4: Line 167, Notes | "Ryan's pipeline step 4. Always pass `--monitor 1` (default is 2, which edits code; 3 pushes). Needs `gh` logged in and the Augment review app; app presence is UNVERIFIED, else `--monitor 0`" | "Ryan's pipeline step 4. Opens the PR; it does not push your branch, push first. Always pass `--monitor 1` (default 2 edits code and leaves a dirty tree; 3 also commits, pushes, replies and resolves threads). At 0 and 1 only the PR appears on GitHub. Size `--timeout` to the CI run (default 600 s, observed CI is longer); on F, R, N expect Augment to decline an oversized PR. Needs `gh` and the Augment app; app presence: indirect evidence only (run log for PR 286 polled `review_present`), else `--monitor 0`" | No separate basis column in the source row; see the source file, sections 3 and 4 | N |
| P179 | [/sc:pr-submit](command-nuance/sc-pr-submit.md) | #5: Line 273, checker footprint | "the PR itself; a `run-log.jsonl` exists (`--resume` flag), its location is UNVERIFIED" | "L0/L1: the PR itself, indistinguishable from a plain `gh pr create`. L1+: `monitor-run-<N>.jsonl`; default `<cwd>/.dev/pr-monitor/pr-<N>-<timestamp>/` (`run_log.py:282-295`), but `--output-dir` moves it, so glob `**/monitor-run-*.jsonl`. L3 also: extra commits, replies, resolved threads, `auggie review` comments" | No separate basis column in the source row; see the source file, sections 3 and 4 | N |
| P180 | [/sc:pr-submit](command-nuance/sc-pr-submit.md) | #6: Line 288, U4 (Augment app installed) | "Guide says `/sc:pr-submit --monitor 1` needs it; ... result is inconclusive" | Add: "indirect evidence: run log `/home/coder/workspaces/Coder/.dev/plans/top9-issues-20261001/closeout/pr-monitor/monitor-run-286.jsonl` shows an Augment poll reaching `review_present` on 2026-10-02; the tracked `.dev/pr-monitor/detection-contract.locked.md` lists the Augment identities. Still not confirmed in repo Settings" | No separate basis column in the source row; see the source file, sections 3 and 4 | N |
| P181 | [/sc:pr-submit](command-nuance/sc-pr-submit.md) | #7: Line 297, U13 | "Post-mode output folder of `/sc:reflect` and location of the `/sc:pr-submit` run log" | Split. pr-submit part answered from source (default path above; `--output-dir` override; observed logs use an explicit dir). Not observed from a live default run | No separate basis column in the source row; see the source file, sections 3 and 4 | N |
| P182 | [/sc:pr-submit](command-nuance/sc-pr-submit.md) | #8: Line 256, Release scenario step 3 | "`/sc:pr-submit --monitor 1`" | "`/sc:pr-submit --monitor 1 --timeout 3600`" (J: size to CI) | No separate basis column in the source row; see the source file, sections 3 and 4 | Y |
| P183 | [/sc:pr-submit](command-nuance/sc-pr-submit.md) | #9: Line 254 and 253 etc., the other scenario rows | `/sc:pr-submit --monitor 1` | unchanged | No separate basis column in the source row; see the source file, sections 3 and 4 | N |
| P184 | [/sc:troubleshoot](command-nuance/sc-troubleshoot.md) | #1: VAL:175 `/sc:troubleshoot`, column T | OPTIONAL | SKIP at LOW, OPTIONAL at MEDIUM, N/A at HIGH (reclassify as B) (J) | No separate basis column in the source row; see the source file, sections 3 and 4 | Y |
| P185 | [/sc:troubleshoot](command-nuance/sc-troubleshoot.md) | #2: VAL:175, column B | REQUIRED | REQUIRED at MEDIUM and HIGH; OPTIONAL at LOW when a failing test already names the line (J, proposed; the guide lists it as step 1 for every bug, HWW:311, so Ryan decides) | No separate basis column in the source row; see the source file, sections 3 and 4 | Y |
| P186 | [/sc:troubleshoot](command-nuance/sc-troubleshoot.md) | #3: VAL:175, columns S and F | OPTIONAL | OPTIONAL at LOW; WORTH IT at MEDIUM and HIGH (J) | No separate basis column in the source row; see the source file, sections 3 and 4 | Y |
| P187 | [/sc:troubleshoot](command-nuance/sc-troubleshoot.md) | #4: VAL:175, column R (re-rated under the multi-feature release definition) | OPTIONAL | WORTH IT at MEDIUM; REQUIRED at HIGH when release-blocking (CI, push or deploy failure); OPTIONAL at LOW (J). Why: a multi-feature release has more CI, deploy and cross-feature regression failures, and observed run folders are mostly CI-triggered `build`/`deployment`/`test` types (observed on disk, per-PR rather than per-release). Which reading of R the old OPTIONAL used is UNVERIFIED; VAL:7 defines R only as "release" | No separate basis column in the source row; see the source file, sections 3 and 4 | Y |
| P188 | [/sc:troubleshoot](command-nuance/sc-troubleshoot.md) | #5: VAL:175, column N | SKIP | SKIP before code exists; OPTIONAL to WORTH IT once code exists and the bug is MEDIUM or HIGH (J) | No separate basis column in the source row; see the source file, sections 3 and 4 | Y |
| P189 | [/sc:troubleshoot](command-nuance/sc-troubleshoot.md) | #6: VAL:175 Notes, flags | "Flags verified in the command file: `--type ...`, `--depth quick\|standard\|deep`, `--fix`. Diagnoses only" | Add: `--fix` only offers Tier 3 after a `success` report; plain `--fix` = `/sc:workflow --depth standard` then user runs `/sc:implement`; `--fix --depth deep` = `task-builder` then user runs `/task`; `--depth quick --fix` is a STOP; `--no-escalate` caps at Tier 1 (CMD:51-54; SKILL:553-568) | No separate basis column in the source row; see the source file, sections 3 and 4 | N |
| P190 | [/sc:troubleshoot](command-nuance/sc-troubleshoot.md) | #7: VAL:175 Notes, path; VAL:271 | `.dev/troubleshoot/<name>-<timestamp>/REPORT.md` | `.dev/troubleshoot/<type>-<first-5-words>-<YYYYMMDDHHMMSS>/REPORT.md` (SKILL:135); note older folders are hand-named | No separate basis column in the source row; see the source file, sections 3 and 4 | N |
| P191 | [/sc:troubleshoot](command-nuance/sc-troubleshoot.md) | #8: VAL:253 scenario "Bug fix" | "1. `/sc:troubleshoot "<error + repro>" --type <kind>` 2. write a failing test, fix ..." | Mark step 1 "skip when a failing test already names the cause (proposed, not confirmed)"; in the escalation text, say a larger or riskier fix needs `--fix --depth deep` or `/task-builder` from the existing report (HWW:133), because plain `--fix` builds a workflow plan | No separate basis column in the source row; see the source file, sections 3 and 4 | N |
| P192 | [/sc:troubleshoot](command-nuance/sc-troubleshoot.md) | #9: VAL:176 `bmad-investigate` | "‡ with `/sc:troubleshoot` for bugs" | Add the split: investigate for log-only incidents, tickets and the BMad lane (resumable case file); troubleshoot when a reproducer exists and a fix proposal is wanted | No separate basis column in the source row; see the source file, sections 3 and 4 | N |
| P193 | [/sc:analyze](command-nuance/sc-analyze.md) | #1: Section 2.6 row `/sc:analyze` (line 177), ratings T B S F R N | `SKIP \| OPTIONAL \| SKIP \| OPTIONAL \| OPTIONAL \| SKIP` | `SKIP \| OPTIONAL \| SKIP \| OPTIONAL \| WORTH IT \| SKIP`. Only R changes (re-rated under the multi-feature release definition, ruling 2): OPTIONAL becomes WORTH IT (J) at MEDIUM and HIGH complexity, OPTIONAL at LOW. Reason: R is the first scope with several features sharing subsystems. Still never REQUIRED. Other columns keep their label, with conditions: B only at HIGH after a fix (J); S SKIP, OPTIONAL only at HIGH (J); F WORTH IT only at HIGH when no `/tech-research` ran (J); N SKIP, OPTIONAL at HIGH once code exists (J). | Reason is inside the proposal text (R is the first scope with several features sharing subsystems) | Y |
| P194 | [/sc:analyze](command-nuance/sc-analyze.md) | #2: Same row, Notes cell | `Reports only, changes nothing. Module health check, not a bug finder. Next step per its file: /sc:improve or /sc:cleanup` | `Reports only, changes nothing. Module health check, not a bug finder: use it when there is no symptom (troubleshoot.md:209), no spec and no diff (reflect.md:310). Flags: [target] --focus quality\|security\|performance\|architecture (one value; the guide's routing row makes it mandatory) --depth quick\|deep ONLY (no standard) --format text\|json\|report. No protocol skill exists; defaults and depth meaning are not defined. Output path undefined, so a checker sees transcript only. Never an expected step. Next step per its file is /sc:improve or /sc:cleanup, but the guide's cleanup route starts with /sc:cleanup-audit.` | Cited inside the proposal (troubleshoot.md:209, reflect.md:310, guide cleanup route) | N |
| P195 | [/sc:analyze](command-nuance/sc-analyze.md) | #3: Section 2.x row O9 (line 235) | `/sc:troubleshoot, bmad-investigate, /sc:analyze` ... `/sc:analyze is health, not bugs` | Drop `/sc:analyze` from the O9 "Diagnose a bug" command list; it has no symptom input. Keep the health-not-bugs note on the 2.6 row only. (Low priority.) | analyze has no symptom input (CMD:22) | N |
| P196 | [/sc:analyze](command-nuance/sc-analyze.md) | #4: Method line 4 (`/sc:analyze skill invoked and followed ... It ran normally`) | `/sc:analyze skill invoked and followed ... It ran normally` | No change; but note no `sc-analyze-protocol` skill backs it, so "followed" means CMD only. | No `sc-analyze-protocol` skill exists | N |
| P197 | [/sc:analyze](command-nuance/sc-analyze.md) | #5: Cross-file note for the merge step: the `/sc:release-split` row | (not quoted in the source item) | The `/sc:release-split` row should say its Part 4 "deep fidelity verification via /sc:analyze" is not backed by CMD (CMD defines no source-versus-output comparison) and that `inline verification` is the file's own alternative (sc-release-split-protocol/SKILL.md:324). | sc-release-split-protocol/SKILL.md:324; CMD defines no comparison of an output against a source | N |
| P198 | [/sc:explain](command-nuance/sc-explain.md) | #P1: Row `/sc:explain` (line 178, section 2.6) | `\| /sc:explain \| Provide clear explanations ... \| OPTIONAL \| OPTIONAL \| SKIP \| SKIP \| SKIP \| SKIP \| Guide level 1: understanding, no files change \|` | `\| /sc:explain \| Provide clear explanations ... \| OPTIONAL \| OPTIONAL \| OPTIONAL \| OPTIONAL \| OPTIONAL \| OPTIONAL \| Guide level 1: understanding, no files change (HOW-WE-WORK:15, 303). Not tied to a phase or scope; no backing protocol skill. Never expected by a checker and never penalized: no on-disk footprint. Flags: --level, --format, --context only; no --depth \|` | A SKIP reads as "do not use", but no file says that; the guide puts level 1 outside the scope ladder, and CMD:12-17 triggers do not depend on scope. SKIP also gives a checker a reason to treat use as odd. The T/B OPTIONAL cells stay as they are. R re-rating: R was SKIP; under the multi-feature release definition nothing changes in substance (no release role in any file); it moves to OPTIONAL only by the consistency argument above. | Y |
| P199 | [/sc:explain](command-nuance/sc-explain.md) | #P2: Section 2 "Rating rules" (after line 51) | (no such line) | Add one line: "Commands that change no files and have no on-disk footprint (for example `/sc:explain`) are never expected steps for a checker; absence is never a miss and use is never a deviation, at any scope or complexity." | No separate basis column in the source row; see the source file, sections 3 and 4 | N |
| P200 | [/sc:explain](command-nuance/sc-explain.md) | #P3: Section 2.6 phase placement | (the row sits under "Bug fix / Troubleshoot" only because it needs a home) | Add to the row Notes or section intro: "side tool, usable in any phase (HWW:145)". | HWW:145 | N |
| P201 | [/sc:post-release](command-nuance/sc-post-release.md) | #1: VAL:186 (row `/sc:post-release`), Notes cell | `Whether this team tags versions is UNVERIFIED (CHANGELOG.md carries "template-version notes")` | `Needs a git tag (runs after it). Verified 2026-10-27: this repo has 2 manual, non-semver tags (aidev02-v1.0, aidev02-v2-m2), one prior run (2026-07-09), none since. R: LOW OPTIONAL, MEDIUM/HIGH WORTH IT; N: WORTH IT (ground-up). Flags: <tag> and --output only; pass --output .dev/releases/current/<short>/post-release/ here` | No separate basis column in the source row; see the source file, sections 3 and 4 | Y |
| P202 | [/sc:post-release](command-nuance/sc-post-release.md) | #2: VAL:186, Purpose cell | `...Runs AFTER the release gate tags a version` | Append: `The "release gate" is a human-cut tag here; no workflow tags` | No separate basis column in the source row; see the source file, sections 3 and 4 | N |
| P203 | [/sc:post-release](command-nuance/sc-post-release.md) | #3: VAL:256 (Section 4, Release row, WORTH IT additions) | `/sc:post-release after the tag` | `/sc:post-release <tag> after the tag is cut (skip if no tag is cut)` | No separate basis column in the source row; see the source file, sections 3 and 4 | N |
| P204 | [/sc:post-release](command-nuance/sc-post-release.md) | #4: VAL:261-276 (footprint table) | no row for post-release | Add: `/sc:post-release` : `<output-dir>/audit.log` (RUN and RESULT blocks), `post-release-report.md`, `post-release-manifest.json`; prior run at `.dev/releases/current/v2-m2/post-release/` : SKILL:227-277 | No separate basis column in the source row; see the source file, sections 3 and 4 | N |
| P205 | [/sc:post-release](command-nuance/sc-post-release.md) | #5: VAL:237 (O11, Document what was built) | Pick `/tech-reference`; `/sc:post-release` not listed | Add `/sc:post-release` to the Overlapping commands cell; keep the pick `/tech-reference`; Why: add `/sc:post-release` is the tag-anchored, whole-surface, install-proven variant for R and N | No separate basis column in the source row; see the source file, sections 3 and 4 | N |
| P206 | [/sc:post-release](command-nuance/sc-post-release.md) | #6: VAL:298 (U14) | `Whether the team tags versions ... no tag check done` | Resolved: `git tag` shows 2 annotated tags (2026-06-22, 2026-07-09); `.dev/releases/current/v2-m2/post-release/` holds one prior run. Residual question: whether the team will tag again (none for 3.5 months, 763 commits) | No separate basis column in the source row; see the source file, sections 3 and 4 | N |
| P207 | [/sc:post-release](command-nuance/sc-post-release.md) | #7: VAL:139 (reading of R in 2.4) | `a release assembles and ships work already built at story or feature size, so build-the-code commands rate SKIP for R` | Cross-note for the merge step, outside my command: under the new R (release plan + implementation + push) `/sc:implement` and `/task` rated SKIP for R at VAL:143-144 need re-rating by their own agents | No separate basis column in the source row; see the source file, sections 3 and 4 | N |
| P208 | [/sc:post-release](command-nuance/sc-post-release.md) | #8: Section 4 "Skippable at every size" (VAL:259) | does not mention post-release | Optional: note `/sc:post-release` is skippable at every size except R and N with a fresh tag | No separate basis column in the source row; see the source file, sections 3 and 4 | N |
| P209 | [/sc:document](command-nuance/sc-document.md) | #1: 192 `/sc:document` | `SKIP SKIP OPTIONAL OPTIONAL OPTIONAL OPTIONAL` / "One-pass reference text (`--type api`). ‡ with `/tech-reference`" | Ratings unchanged. Notes: "One pass, no task folder, no backing skill, no ledger: transcript only. `--type inline` is the only path that writes docstrings; no neighbour covers it. Use for a named target of under 5 files; at 5+ files or several subsystems use `/tech-reference`. Never required. R (multi-feature): OPTIONAL at LOW and MEDIUM, `--type inline` only at HIGH (J)." | No separate basis column in the source row; see the source file, sections 3 and 4 | Y |
| P210 | [/sc:document](command-nuance/sc-document.md) | #2: 189 `/tech-reference` Notes | "Repo already carries `aidev02-v1.0-as-built-technical-reference.md`. ‡ with `/sc:document`" | Remove the repo-evidence sentence: that file says it was produced by `bmad-retrospective` (its line 13), and `.dev/tasks` holds 0 `TASK-TECHREF-*` folders. Replace with: "Full pipeline even at Lightweight tier (`/task-builder` + `/task`, 7 phases). Footprint `TASK-TECHREF-*`. S: OPTIONAL at HIGH only (J). R: per feature, WORTH IT at MEDIUM and HIGH, OPTIONAL at LOW (J)." | No separate basis column in the source row; see the source file, sections 3 and 4 | Y |
| P211 | [/sc:document](command-nuance/sc-document.md) | #3: 190 `/operational-guide` Notes | "Repo has `docs/operations/*`. Needed when deploy or operator steps changed" | Keep the trigger, make it the rule: "Rated by trigger, not scope: WORTH IT in ANY scope when deploy or operator steps changed (J), otherwise SKIP. Default output `docs/docs-product/ops/` does not exist here: pass the path. Existing `docs/operations/aidev02-operator.md` is 3467 lines, above the skill's 1,000-line ceiling, so edit it by hand." | No separate basis column in the source row; see the source file, sections 3 and 4 | Y |
| P212 | [/sc:document](command-nuance/sc-document.md) | #4: 191 `/readme` Notes | "Only for a new package or module" | Add: "Footprint `TASK-README-*`; 500-line ceiling; output at the module root. Updating one table in an existing README is a plain edit or `/sc:document <file> --type guide`." | No separate basis column in the source row; see the source file, sections 3 and 4 | N |
| P213 | [/sc:document](command-nuance/sc-document.md) | #5: 237 O11 "Why" | "Researches a whole feature and is reviewed; `/sc:document` is one-pass reference for specific code" | Append the decision rule: "`/tech-reference` when 5+ relevant files or several subsystems; `/operational-guide` when the reader executes steps; `/readme` for a new module; `/sc:document` for a named target under 5 files, or `--type inline` at any size." | No separate basis column in the source row; see the source file, sections 3 and 4 | N |
| P214 | [/sc:document](command-nuance/sc-document.md) | #6: After 269-276 (footprint table) | No rows for the four doc commands (line 276 lists commands with no footprint but not these) | Add four rows from section 5 of this file. `/sc:document`: "none, transcript only". | No separate basis column in the source row; see the source file, sections 3 and 4 | N |
| P215 | [/sc:document](command-nuance/sc-document.md) | #7: 260 (skippable list) / 256 (R path) | R path lists `/operational-guide`, `/tech-reference` as WORTH IT additions | Keep; add `/sc:post-release` as the release-level docs step after the tag (already at line 256) and note that a checker must not require the doc skills by name. | No separate basis column in the source row; see the source file, sections 3 and 4 | N |
| P216 | [/sc:document](command-nuance/sc-document.md) | #R-note: R reading (multi-feature release) | Old R column fits "one release's docs"; rating letters of the four doc commands do not change. | Add to the R reading "per feature, scaled by complexity band" and the cells in the table above; `/sc:post-release` (line 186, R: WORTH IT) is the release-level vehicle. | Under the new definition the doc sweep is per feature plus release level | N |
| P217 | [/sc:document](command-nuance/sc-document.md) | #Cross-ref: Doc rows of the main file (cross-reference) | (none) | Add a one-line cross-reference to the scope x complexity matrix of this file in the doc rows, so the main file shows `/sc:document` as OPTIONAL only (J) and never REQUIRED. | No separate basis column in the source row; see the source file, sections 3 and 4 | Y |

### 6.3 Per-command nuance

One subsection per command, 27 in all, in pipeline-phase order. Spec: brainstorm, design, spec-panel, tdd, research, adversarial, release-split. Tasklist: workflow, roadmap, spawn. Review: reflect, validate-roadmap, swarm-wizard. Implement: implement, test, build, improve, cleanup, cleanup-audit. Commit/PR: git, auggie-review, pr-submit. Bug fix: troubleshoot, analyze, explain. Post-merge: post-release, document.

Each subsection copies five sections of the command's nuance file word for word: 1 status and role, 2 flags, 3 scope x complexity matrix, 4 choose this or the neighbour, 6 expected-step rule. Only two things differ from the source: heading levels are pushed down three levels so they nest under this section, and the HTML section-marker comments between sections are dropped (with the extra blank lines they left). The markers (J), JUDGMENT, UNVERIFIED and PROPOSED are exactly as in the source. A cell marked (J) is a proposal, not a ruling; the matching cell in Section 2 stays as it was.

The citation keys used in the copied text (for example `cmd:12`, `HWW:309`, `SK:45`) are defined in the header of each source file, reached through the link that closes every subsection. Line numbers in the copied text refer to the files as they read on 2026-10-27. Where a copied section names `/sc:task` or `/sc:tasklist`, it either records that a command file or a skill still points at a command Ryan has retired (see 6.5) or says that the command does not call them; none of them recommends either as a step.

#### 6.3.1 /sc:brainstorm (Spec)

##### 1. Status and role

- **Does**: "Orchestrated multi-agent brainstorm: Socratic dialogue + parallel proposals + adversarial merge" (`cmd:3`). It produces a requirements spec (`merged-requirements.md`) and stops; it writes no code and never auto-runs `/sc:design` (`cmd:179-187`, `SKILL:413-418`). Phase: Spec, idea shaping.
- **Status**: NOT retired. Standalone-invokable by the engineer (`cmd:25-29`); its protocol skill is never run directly (`SKILL:23-30`). It is also called programmatically by `/sc:release-split` Part 1 (`sc-release-split-protocol/SKILL.md:103,149,161`).
- **Overlaps**: `bmad-brainstorming` (the lane twin), `/tech-research` (when the unknown is facts about our code), `/sc:adversarial` (when drafts already exist), `/sc:design`, `/prd`. Retired `/sc:tasklist` is still named in its `--handoff tasklist` and in its "Next:" text (`cmd:174,199`, `SKILL:315-318`): never use it.

##### 2. Flags

Source: option table `cmd:45-64`, interactions `cmd:66-71`. The protocol's `argument-hint` lists only `--proposals --depth --strategy --handoff --output` (`SKILL:5`); the other flags exist in the command file only, and all arguments are passed through to the protocol (`SKILL:27-28`). Short forms `-p -d -s -i -o` appear only in `cmd:46-61`.

| Flag | Values | Default | What it changes (cited) | Worth using | Avoid |
|---|---|---|---|---|---|
| `<topic>` | free text or `@file` | required; empty STOPs (`cmd:29`, `SKILL:70`) | Becomes the seed brief's `topic`, and drives domain and strategy auto-detection (`st:5-32`) | Always. Give who it is for, the outcome, the main constraint (`HWW:30,310`) | A one-word topic: auto-detection then guesses the domain |
| `--proposals N` (`-p`) | 2-7 | 3 | Number of parallel variants. Clamped silently: quick max 2, standard max 5, deep max 7 (`SKILL:96-100`; the command file states only the quick and deep caps, `cmd:68-70`). At exactly 2, per-persona instructions are dropped (`asb:101`) | 3 (default) for most work. 4-5 at deep when approaches truly differ | 7 at deep: by the formula in `asb:146-152` with the code-domain personas the estimate is about 276K tokens, over the 250K trigger, so it auto-downgrades to 3 (derived arithmetic, not observed). 1 is invalid (below the 2 floor) |
| `--depth` (`-d`) | `quick`, `standard`, `deep` | `standard` | Socratic question count 3-5 / 6-10 / 10-20 (`SKILL:131-133`); proposal cap (above); token estimate per proposal 8K / 15K / 35K (`SKILL:237`); passed to adversarial where `--depth` sets debate rounds 1 / 2 / 3 (`adv:334`): quick skips Round 2 and 2.5 (`adv:1083,1112`), Round 3 runs only at deep and only below the convergence threshold (`adv:1361`). At deep the first two personas run on opus (`asb:63`) | `standard` is the guide's default and "need not be passed" (`HWW:309-310`). `quick` for a narrow question. `deep` for cross-component or risky topics | `deep` for routine ideas: 35K per proposal against 15K at standard |
| `--strategy` (`-s`) | `systematic`, `agile`, `enterprise`, `auto` | `auto` | `auto` picks by keywords: compliance / audit / regulation / enterprise / SOC2 / SOX / HIPAA / large customers means enterprise; MVP / prototype / quick / experiment / iterate / ship fast / validate means agile; else systematic (`st:26-32`). `enterprise` forces `--depth deep` unless `--depth` is given (`cmd:67`, `SKILL:110`) and sets personas architect, analyzer, devops, scribe, qa (`asb:19`) | Set it explicitly when the topic is compliance-driven | Leaving `auto` on a topic that merely contains "audit", "quick" or "validate": the keyword rules can flip strategy. Whether an auto-detected enterprise also forces deep is unclear: Wave 0 applies the rule (`SKILL:110`) before Wave 1 detects the strategy (`SKILL:123`) (UNVERIFIED) |
| `--codebase` / `--no-codebase` | flags | auto: on for domains code, architecture, incident (`SKILL:183`) | Runs a quick codebase scan (Auggie, then Serena, then Glob/Grep) into `enrichment/codebase-context.md` (`hr:9-40`); total enrichment summary capped near 3000 tokens (`SKILL:198`) | `--codebase` for a product or process topic that touches existing code | `--no-codebase` is right for a greenfield N topic. The scan is shallow: not a substitute for `/tech-research` |
| `--research` / `--no-research` | `light`, `deep`, `none` / flag | auto | `light` routes to `/sc:research --depth quick`, `deep` routes to the `tech-research` skill (`SKILL:185-186`, `hr:42-80`). Auto-light when the topic names a framework not in the project; auto-deep only for enterprise + novel technology (`SKILL:185-186`) | `light` when the topic depends on an outside library or standard | `deep` below HIGH: `tech-research` is itself a heavy run (`HWW:255`). Note: the skill directory `sc-research-protocol` does not exist under `~/.claude/skills/`; the table allows `/sc:research` standalone and `hr:55-59` falls back to WebSearch (UNVERIFIED which path runs) |
| `--personas p1,p2` | comma list | auto by domain (`asb:9-17`) | Overrides persona choice. `security` is never auto-selected, only when named here (`asb:29-35`, `SKILL:216`). Empty value STOPs (`SKILL:101`) | HIGH topics with a risk class (secrets, permissions, user input, paths, infrastructure): name `security` explicitly | Naming personas for LOW work: adds cost for no gain (J) |
| `--models a,b,c` | aliases | `opus,sonnet,haiku` | Round-robin model per persona (`asb:53-73`). Unset env aliases are not an error (`SKILL:109`) | Leave default | Changing it without a reason |
| `--blind` | flag | false | Pass-through: strips model names before adversarial scoring (`cmd:57`, `adv:343`) | HIGH, deep, when model bias would matter | Everything else |
| `--convergence FLOAT` | 0.50-0.99 (`adv:335`) | 0.75 here; adversarial's own default is 0.80 (`adv:335`) | Pass-through threshold; the adversarial table describes it as the threshold "for deep mode" (`adv:335`). Brainstorm's own PASS / PARTIAL / FAIL cutoffs are fixed at 0.65 and 0.50 whatever you pass (`SKILL:290-292`) | Leave default | Raising it to force agreement: it does not move the 0.65 pass line |
| `--interactive` (`-i`) | flag | false | Pauses for the user at Socratic and adversarial decision points (`cmd:59`). Without it the Socratic batches "auto-proceed using best-available context" (`SKILL:134`): no real answers are collected | Any MEDIUM+ topic whose answers are not in files or the topic text | Unattended runs. Do not expect a dialogue if you leave it off |
| `--handoff` | `none`, `design`, `tasklist`, `task` | `none` | Runs in Wave 4, only after PASS or PARTIAL (`SKILL:290-292`). `none`: prints the artifact table and next steps (`SKILL:311`). `design`: prints a hint only (`SKILL:313`). `tasklist`: calls `sc-tasklist-protocol --source merged-requirements.md` after a 3-requirement check (`SKILL:315-318`): RETIRED, never use. `task`: calls `Skill task-builder --source ... --template <feature/bugfix/migration/documentation/decision-record>-template` (`SKILL:320-330`, `hr:206-225`) | `none`, then build the task file yourself with `--spec` (J, see section 4) | `tasklist` (retired). `task`: `task-builder` documents only a goal, `--spec`, `--cli` and a BUILD_REQUEST path (`task-builder/SKILL.md:33-43`), has no `--source`, `--template` or the five `*-template` names (grep: no hits), and the handoff passes no `--spec` (`hr:217-223`); so it may leave `reflect_pre` as `skipped` (UNVERIFIED, derived from `task-builder/SKILL.md:41`). `design` adds nothing a person cannot type |
| `--output` (`-o`) | dir | `.dev/brainstorms/<ts>-<slug>/` | Run folder; on collision a `-N` suffix, STOP at 100 (`SKILL:108`) | Leave default so a checker can find it (J) | Custom paths hide the footprint (J) |
| `--dry-run` | flag | false | Runs Waves 0-2B, prints the agent spec and token estimate, skips Waves 3-4; contract `status: dry-run` (`SKILL:249-254`) | Before `--depth deep` or `--strategy enterprise`, to see cost | It is not a deliverable: no `merged-requirements.md` |
| `--resume-from PATH` | seed-brief path | none | Skips the Socratic dialogue and reuses a saved seed brief; needs frontmatter `topic, domain, strategy, depth` (`SKILL:124-128`). Also the retry route after a hard abort (`SKILL:400`); an interrupted dialogue saves `seed-brief-partial.md` (`SKILL:393`) | Continue an interrupted run | Starting over a finished run |
| `--force-stale` | flag | false | Lets `--resume-from` proceed when domain re-classification differs (`cmd:64`, `SKILL:127`) | Only with `--resume-from` | Otherwise |

**Does not exist** (people may assume it): `--spec` (a spec can only arrive as `@file` in the topic); `--handoff implement` or `roadmap` (the `implement` value belongs to `/sc:workflow`, `workflow.md:7,40`); `--proposals 1` (floor is 2, `SKILL:96`, although a 1-proposal run exists on disk, see section 5); `--focus` and `--pipeline` (adversarial flags, not passed through, `adv:334-345`); `--tier` or `--compliance`.

##### 3. Scope x complexity matrix

**How this command varies with complexity.** It does vary, through one knob: `--depth` (plus `--proposals` and `--interactive`). Its own files tie depth only to cost and rounds, never to scope or to a score. Examples in the command file: `standard` for a feature discovery, `deep` for an incident post-mortem, a cross-domain redesign and a blind comparison (`cmd:78,86,102,112`); no `quick` example. The task-builder TCS (`task-builder/SKILL.md:2402-2441`) cannot be used as an input: it is computed from a finished task file (S1 reads the "MDTM body", S3 needs a `--spec`), which does not exist yet when a brainstorm runs. So the bands below are JUDGMENT, built from signals the files do name:

| Band | Signals (all (J) as a grouping; each signal is cited) |
|---|---|
| LOW | The author can state the outcome and name the files; one subsystem; a driving spec, PRD or story already exists, or the request already answers what / why / where (`HWW:30`); no risk class touched |
| MEDIUM | Intent is clear but alternatives are open; two or three components (the file's own rule: three or more components or "across" means `architecture`, one component means `code`, `st:20`); no driving spec yet; the author names some files, not all; low-to-moderate risk |
| HIGH | Three or more components or "across" (`st:20`); competing approaches; interfaces shared between stories; novel outside technology (`hr:67-69`); compliance wording (`st:30`); a security-review class: login, permissions, secrets, user input, file paths (`HWW:200`); costly to reverse (deep probe questions, `st:55-62`) |

No file rates this command REQUIRED anywhere: the guide runs it "only if the idea is vague" (`HWW:309`) and the BMad twin is `required=false` (`bmad-help.csv:3`). So REQUIRED never appears below.

| Scope | LOW | MEDIUM | HIGH |
|---|---|---|---|
| T one-off | SKIP | SKIP | SKIP (J). A one-off means the exact change is already known (`HWW:16`); if it is not known, it is not a T: re-scope |
| B bug fix | SKIP | SKIP | OPTIONAL (J), `--depth quick --no-research`. `/sc:troubleshoot` comes first; brainstorm is "upstream ... when the symptom is genuinely ambiguous" (`troubleshoot.md:213`). It yields requirements, not a diagnosis (`cmd:186`) |
| S single story | SKIP (`scenarios.md:29` lists brainstorm as skippable for a story) | OPTIONAL (J), `--depth quick` | OPTIONAL (J), `--depth standard --interactive`. A single story that needs a deep brainstorm is probably an F: re-scope |
| F multi-story feature | SKIP. Clear requirements go straight to a short spec file and `/task-builder --spec`; the guide route has no brainstorm step (`HWW:93,306-307`) | WORTH IT, `--depth standard --handoff none` | WORTH IT, `--depth deep --interactive`; add `--personas ...,security` if a risk class applies (J) |
| R multi-feature release (re-rated, see section 7) | SKIP (J) | OPTIONAL (J), `--depth standard`. Skip it if `/sc:release-split` will run: that command runs a brainstorm itself as Part 1 (`release-split SKILL:103,149-161`) | WORTH IT (J), `--depth deep --interactive`, only when the release scope itself is unsettled; not when each feature already has a spec |
| N new product | OPTIONAL (J), `--depth quick`. Full-spec step 1 is "only if the idea is vague" (`HWW:309`) | WORTH IT, `--depth standard` (guide default, `HWW:309`) | WORTH IT, `--depth deep --interactive`; `--strategy enterprise` only if compliance wording is real; `--no-codebase` if greenfield (J) |

Flag set by band in one line: LOW and MEDIUM use `--handoff none` and default or `quick` depth; HIGH uses `deep` with `--interactive`; `--handoff` is `none` at every band (J), because the two useful values are worse than doing the next step by hand (section 4).

##### 4. Choose this or the neighbour

###### 4.1 `/sc:brainstorm` vs `bmad-brainstorming`

What each is (files): `bmad-brainstorming` is a creative coach with three stances (Facilitator, Creative Partner, Ideate for me, `bmad:SKILL.md:12`); it says "aim past 100 ideas; resist concluding" and one prompt per message (`bmad:SKILL.md:33,35`); output is a `.memlog.md` under `_bmad-output/brainstorming/brainstorm-{topic_slug}-{date}/` (`bmad:customize.toml:67-68`) plus opt-in `brainstorm.html` / `brainstorm-intent.md` (`bmad:references/finalize.md:20-22`); it has no adversarial merge and no enumerated-requirements output. `/sc:brainstorm` is convergent: it ends in `merged-requirements.md` with a convergence score (`SKILL:289-292`). BMad catalog: phase 1-analysis `required=false` and "anytime" (`_bmad/_config/bmad-help.csv:3,33`). Running both on one idea is waste (value file line 50, O1).

| Signal | Pick |
|---|---|
| Next step is `bmad-product-brief`, `bmad-prd` or `bmad-spec` (BMad lane) | `bmad-brainstorming`: its own wrap-up points to those (`bmad:references/finalize.md:21,26`) |
| Next step is `/prd`, `/task-builder --spec`, `/sc:workflow` or `/roadmap` (task-file lane) | `/sc:brainstorm`: the output is a requirements file you can pass as the spec |
| Need many ideas, the human wants to generate them, no decision needed yet | `bmad-brainstorming` (divergent) |
| Topic is ambiguous with competing approaches that need a decision and a spec | `/sc:brainstorm` (parallel proposals plus debate) |
| HIGH: three or more components, shared interfaces, risk class | `/sc:brainstorm --depth deep` (J): only it has an adversarial debate |
| LOW or MEDIUM and a person wants to think aloud | `bmad-brainstorming` (J) |
| Must run unattended | `/sc:brainstorm` without `--interactive`. `bmad-brainstorming` goes headless only on a machine signal; a present human always means interactive (`bmad:references/headless.md:7-11`) |

###### 4.2 Other neighbours

| Neighbour | Rule (cited) |
|---|---|
| `/tech-research` | The unknown is facts about our code or feasibility, or you cannot name the files: `/tech-research` first (`HWW:19,142`). Brainstorm's codebase scan is capped near 3000 tokens (`SKILL:198`). Brainstorm only if "what to build" is still open afterwards (J) |
| `/sc:adversarial` | You already have two or more drafts: `/sc:adversarial --compare` (`HWW:152`). Brainstorm generates its own variants (adversarial Mode B, `SKILL:266-281`); do not run it to compare drafts you wrote |
| `/sc:design` | Brainstorm never invokes it (`cmd:158`, `SKILL:313`). One new interface: `/sc:design` afterwards (`HWW:98`). Something others build against: `/tdd` |
| `/prd`, `bmad-prd` | Requirements already clear: skip brainstorm, write the PRD or short spec (`HWW:93`). Vague: brainstorm, then `/prd "Start from <merged-requirements.md>"` (`HWW:56`) |
| `/sc:workflow` vs `/task-builder` after brainstorm | Not decided by this command. Use the validated rule: multi-story feature needs `/task-builder` + `/task` with `--spec` (`validation-feature-task-builder-vs-sc-workflow.md`); a single story may use `/sc:workflow --depth quick` (`HWW:17`). Pass the `merged-requirements.md` path as `--spec` (J) |
| `/sc:tasklist` | RETIRED. Do not use `--handoff tasklist`. The "Next:" text of `--handoff none` still suggests `/sc:tasklist` and `/sc:implement @merged-requirements.md` (`SKILL:311`, `hr:164-166`): a checker must not treat that printed suggestion as the pipeline, and `/sc:implement` straight from requirements skips the tasklist step that is the validated minimum for F |
| `/sc:release-split` | It calls brainstorm itself (`release-split SKILL:149,161`). A brainstorm folder created inside a release-split run belongs to release-split; a standalone one before it is redundant at R-MEDIUM (J) |
| `bmad-forge-idea`, `bmad-party-mode`, `openspec-explore` | Idea-stage aids outside Ryan's pipelines (value file rows 80, 90, 100). Not a substitute for either brainstorm in the checker's eyes |

##### 6. Expected-step rule

- **Count the idea-shaping step as expected** (either `/sc:brainstorm` or `bmad-brainstorming` satisfies it) only when all three hold (J, built on `HWW:309` "only if the idea is vague"): scope is F or N (R only at HIGH); complexity is MEDIUM or HIGH; and no spec, PRD, requirements file or story file existed before the tasklist step was created. Even then it is WORTH IT, never REQUIRED: no file marks it required (`bmad-help.csv:3`, `HWW:309`).
- **Absence is fine** for T and B at any complexity; S at any complexity; F-LOW; any scope when a spec / PRD / story / epic predates the tasklist; R when each feature already has a spec or `/sc:release-split` ran (it runs a brainstorm itself). Do not judge the flags chosen (`--depth`, `--proposals`, `--handoff none`) or short and hand-run forms (3 of the 11 observed folders). The one thing a checker may flag is `--handoff tasklist` (retired `/sc:tasklist`).
- Note for the checker design: `scenarios.md:34-35` lists "brainstorm or design" in S5 and says "Allowed to skip: nothing in the chain", which conflicts with the guide's "only if vague". Align S5 with this rule.

Full file for the citation key, the footprint (section 5), the proposals (section 7) and the unverified items (section 8): [command-nuance/sc-brainstorm.md](command-nuance/sc-brainstorm.md)

#### 6.3.2 /sc:design (Spec)

##### 1. Status and role
- **What it does** (DS:3): "Design system architecture, APIs, and component interfaces with comprehensive specifications". One 110-line command file, `complexity: basic`, no personas, no MCP servers (DS:5-7). Five-step flow Analyze, Plan, Design, Validate, Document (DS:27-31). No waves, no gates, no sub-agents, no research step named.
- **Phase**: Spec (CV:65). **Not retired, standalone-invokable.** **No backing protocol skill**: `~/.claude/skills/sc-design-protocol/` does not exist (`ls` exit 2; glob `~/.claude/skills/sc-design*` empty, checked 2026-10-27). Per HW:232, a command whose file names no skill runs from its own file, so no skill-load line appears in a transcript.
- **Overlaps**: `/tdd` = `/sc:tdd` (HW:244; TDDC:183), `bmad-architecture` (CV:88, CV:229), `/sc:spec-panel` (critique, not a rival), `/sc:workflow` (downstream; workflow.md:76 lists `/sc:design` as "Architecture spec"). Called programmatically by `/sc:auggie-review` remediation Phase A (RH:63-78; AR:137). Named by `/sc:release-split` Part 3 as the default command for release specs (RS:270-275; RSC:134). Text-only suggestion from `/sc:brainstorm --handoff design` (HR:170-181).

##### 2. Flags
Usage line (DS:22): `/sc:design [target] [--type architecture|api|component|database] [--format diagram|spec|code]`. That is the whole flag surface. No protocol skill exists to add more.

| Flag / argument | Values | Default | What it changes (cited) | Worth using when | Avoid when |
|---|---|---|---|---|---|
| `[target]` | A name (DS:59, 67, 75, 83) or, per callers, `@<file>` (HR:164, 175; OR:10; RH:68). Whether design.md handles `@file`: UNVERIFIED (U4) | none stated | Subject of the design; Analyze step "examine target requirements and existing system context" (DS:27) | Name one interface, component or schema; or pass the requirements/plan file a caller prints | Target is a whole product or several subsystems (use `/tdd` or `bmad-architecture`, section 4) |
| `--type` | `architecture`, `api`, `component`, `database` (DS:22) | not stated (U2) | Selects the pattern: system structure, RESTful/GraphQL interface, functional interface, schema (DS:49-52) | `api` or `component` for one new interface inside a spec file (HW:98 uses `--type api`) | `architecture` on a narrow job. RH:76 calls it the broadest type and uses it only because reviews span many concerns |
| `--format` | `diagram`, `spec`, `code` (DS:22) | not stated (U2) | Output shape: diagrams, specification text, interface code (DS:37, DS:102-107) | `spec` when the output goes into a spec file that `/task-builder --spec` or `/sc:workflow` will read (HW:98; RH:77 "text that sc:workflow / the task-builder can consume") | `code`: DS:75-77 shows interface code with "implementation guidance" but DS:98 says it will not generate implementation code, and the boundary is undefined (U6). `diagram` when a downstream tool must read the result as text |

**Do not exist in DS (people might assume):** `--depth`, `--tier`, `--handoff`, `--resume`, `--focus`, `--from-prd`, `--spec`, `--strategy`. Those belong to other commands: `--depth` and `--handoff` to `/sc:workflow` (workflow.md:7, 30-31); `--tier`, `--from-prd`, `--focus`, `--resume` to `/tdd` (TDDC:43-51). **`--output` is not defined in DS either, but `/sc:auggie-review` passes it** (`--output <output_dir>/remediation-spec.md`, RH:68-72), while AR:137 and AR:149 show the same call without it. Whether it is honoured: UNVERIFIED (U3).

Consequence: there is no `--depth` or `--tier`, so `/sc:design` cannot be made lighter or heavier. The complexity choice is made by picking a different command (sections 3 and 4).

##### 3. Scope x complexity matrix
**Does the command vary by complexity? No.** It is one pass with no depth or tier control (section 2). What varies is whether one pass is enough, so the bands below describe the work, and the cells say whether `/sc:design` is the right tool or a heavier design command takes over. All band boundaries are JUDGMENT built from numbers that other files give for `/tdd` tiers and for task-builder's subsystem counting rule. No file sets a threshold for `/sc:design` itself.

| Band | Signals (all (J) as a combination) | File numbers borrowed |
|---|---|---|
| LOW | One interface, component or schema; author can name the files up front; under 5 relevant files; one subsystem; no driving spec; nobody else builds against it | `/tdd` lightweight "single service or component, narrow scope, <5 relevant files" (TDDS:71) |
| MEDIUM | Two or more interfaces, or one interface shared by two or more stories; 5-20 files; two subsystems; a short spec exists | `/tdd` standard "5-20 files, moderate complexity" (TDDS:72); subsystem = first 2 path segments (TB:2411) |
| HIGH | 20+ files, or several services, layers or integration boundaries; other people or teams build against the design; units built independently could choose incompatible shapes; "must not drift" | `/tdd` heavyweight "20+ files", "always Heavyweight" for multi-service/layer scope (TDDS:73, 80); HW:18, HW:244; BA:11 (the "could two units choose incompatibly" test) |

Cell = rating of `/sc:design` itself. Text after the dash says what carries the design step. Every cell is JUDGMENT `(J)` unless it cites a file for the cell's own claim.

| Scope | LOW | MEDIUM | HIGH |
|---|---|---|---|
| **T** one-off | SKIP. Levels 1-2 contain no design step (HW:15-16); a plain edit plus its test (proposed one-off minimum, not yet confirmed by Ryan) | N/A (J). Needing a design for a new interface breaks the level-2 limit "more than 5 edits or more than one source file" (HW:22); the work is no longer T | N/A (J). Same reason |
| **B** bug fix | SKIP. Diagnosis is `/sc:troubleshoot` and `REPORT.md` (HW:123-128) | SKIP. A few files with clear scope go to `/sc:workflow --depth quick` from the REPORT (HW:132) | SKIP (J). Larger or riskier fix goes to `/task-builder` built from the REPORT (HW:133). A redesign discovered here is a new F, not a B step |
| **S** single story | SKIP. Levels 2-3 have no design step (HW:16-17); scenario S4 lists design as skippable (SC:29) | OPTIONAL (J). `--type api` or `--type component`, `--format spec` only if the story adds an interface that the story file does not already define; output goes into the story/spec file, not straight to the executor (RH:14) | SKIP /sc:design (J). If others build against the interface, the design step is WORTH IT (J) via `/tdd --tier lightweight`, or a `bmad-architecture` slice in the BMad lane (BA:15 "the one slice a feature touches") |
| **F** multi-story feature | SKIP (J). HW:98 asks for a short agreed spec file; design is named only "if it includes a new interface or API" | OPTIONAL. `/sc:design <name> --type api --format spec`, paste into the spec file, then `/task-builder --spec` (HW:98; HW:307 notes column). This is the one file-stated use | SKIP /sc:design as the design step (J). Stories that share an interface and must not drift (HW:18; `validation-feature-task-builder-vs-sc-workflow.md:155` items 2 and 5, itself marked JUDGMENT there) need `/tdd --tier standard\|heavyweight` or `bmad-architecture`. `/sc:design` may still draft one interface section inside that document (HW:98, HW:244) |
| **R** multi-feature release (re-rated, see section 7) | SKIP (J). Small features with named files already have per-feature specs | OPTIONAL (J). One shared cross-feature interface drafted as a spec section | WORTH IT (J) only when `/sc:release-split` approves a split: Part 3 says "Default to /sc:design for producing release specs" and writes `release-1-spec.md`, `release-2-spec.md` (RS:270-275, 306-310). Usually runs inside release-split, so the engineer may never type it. Without a split, the design step is per-feature `/tdd` or one `bmad-architecture` run (J) |
| **N** new product | OPTIONAL (J). Helper for one interface. The design step in the file-routed path is `/prd` then `/tdd` (HW:20, HW:309); `/tdd --tier lightweight` fits under 5 files | OPTIONAL (J). Helper only. Design step is `/tdd --tier standard` or `bmad-architecture` (REQUIRED at N per CV:88, csv required=true) | SKIP as the design step (J). A single pass cannot cover 20+ files or several services (TDDS:73, 80). `/tdd --tier heavyweight` or `bmad-architecture` carries it; `/sc:design` only for a single interface section |

##### 4. Choose this or the neighbour
###### 4.1 `/sc:design` versus `/tdd` (= `/sc:tdd`)

HW:244 gives the base rule: `/sc:design` drafts one design (an API, a component, a schema) in a single pass; `/tdd` writes a full technical design document from the template, with research and independent reviewers; use `/tdd` when other people will build against the design.

| Signal | Pick `/sc:design` | Pick `/tdd` (tier) |
|---|---|---|
| What is being designed | One interface, component or schema (HW:244; DS:49-52) | A component, service or system (TDDS:12, 39) |
| Relevant files | Under 5 and nameable up front (LOW) (J) | Lightweight under 5 files; standard 5-20; heavyweight 20+ or several services/layers (TDDS:71-73, 80) |
| Who builds against it | The author, or one agent in one session | Other people or teams (HW:244) |
| Claims must be code-verified | No research step is named in DS:27-31 and DS:42-45 | Yes: "every claim through codebase verification", analyst and QA gates, template conformance (TDDS:16, 24-29; TDDC:65) |
| A PRD drives it | No `--from-prd` flag | `/tdd --from-prd <path>` (TDDC:26, 51) |
| Footprint and cost | No output path, no folder (section 5) | `.dev/tasks/to-do/TASK-TDD-<timestamp>/` with `research/`, `synthesis/`, `qa/` and a final `docs/<domain>/TDD_<NAME>.md` (TDDS:86-111); runs through `rf-task-builder` then `/task` (TDDS:10, 353-386) |
| Tier default | n/a | "Default to Standard"; "If in doubt, pick Standard" (TDDS:67, 77) |

Rule (J): LOW goes to `/sc:design`; LOW with a wish for verified claims goes to `/tdd --tier lightweight`; MEDIUM goes to `/tdd --tier standard` unless the only new thing is one interface section (then `/sc:design`, OPTIONAL); HIGH goes to `/tdd --tier heavyweight`. They are not exclusive: TDDC:183 lists `/sc:design` as "complementary" for "architecture diagrams and API specs", so both can appear in one feature (the TDD for the whole, `/sc:design` for one interface section).

###### 4.2 `/sc:design` versus `bmad-architecture`

| Signal | Pick `/sc:design` | Pick `bmad-architecture` |
|---|---|---|
| Lane | Task-file lane: next step is `/task-builder --spec` or `/sc:workflow` (HW:98, HW:307) | BMad lane: next step is `bmad-create-epics-and-stories`, or at epic altitude `bmad-create-story` (BA:76). CV:223: pick the lane at the Spec step and stay in it |
| What it produces | Diagrams, API specs, schemas, interface definitions (DS:102-107) | A lean "architecture spine" of invariants: paradigm, boundaries, state mutation, shared-data ownership. Stack, tree and full data shape are "seed", owned by code once it exists (BA:9) |
| Decision test | None stated | "If two units one level down built this independently, could they choose incompatibly?" Fix it only if yes, non-obvious and a real trade-off (BA:11). This is the HIGH signal (shared interfaces, drift) |
| Size handling | None | "A few decisions for a small thing, comprehensive for a platform; the whole system or the one slice a feature touches" (BA:15); altitude initiative, feature, epic (BA:29, 31, 60) |
| Cost | One pass | Coaching path is the default, with a mandatory purpose-and-audience question and a memlog, then a reviewer gate of parallel subagents (BA:21, 35-41, 58, 62-64). Fast path drafts with `[ASSUMPTION]` tags (BA:21); headless mode exists (BA:55) |
| Output home | Unspecified | `{planning_artifacts}/architecture/architecture-{project_name}-{date}/ARCHITECTURE-SPINE.md` per `customize.toml:54-55` (this repo's `_bmad-output/planning-artifacts/architecture/` exists) |

Rule (J): BMad lane at LOW or MEDIUM: neither is needed at S (CV:88 SKIP at S; story file is the handoff); at F-MEDIUM an interface section is optional via `/sc:design` only if the team is not using BMad epics. BMad lane at F-HIGH or N: `bmad-architecture` at the matching altitude, not `/sc:design`. `/sc:design` and `bmad-architecture` are not substitutes for interface text: the spine defers detail it cannot justify fixing (BA:9, BA:11).

###### 4.3 Neighbours that are order, not alternatives

| Neighbour | Relation | Rule |
|---|---|---|
| `/sc:spec-panel` | Critique of a spec; spec-panel.md:462 says to incorporate feedback, then use `/sc:design` | Not a rival. No ordering requirement for a checker (HW:309 puts spec-panel after `/tdd`) |
| `/sc:adversarial --compare a.md,b.md` | Picks or merges competing designs (adversarial.md:179; CV:230) | Only when two real candidate designs exist: a HIGH signal. Otherwise SKIP |
| `/sc:workflow`, `/sc:implement` (downstream) | DS:109 says "Next Step: /sc:implement". RH:14 says a design spec is prose and "would collapse to one task", so the plan route puts `/sc:workflow` between spec and implement. HW:98 pastes the output into a spec file for `/task-builder --spec` | LOW, one task: straight to `/sc:implement` is acceptable (J). MEDIUM: `/sc:workflow --depth quick` on the spec (S) or `/task-builder --spec` (F). HIGH: `/task-builder --spec` |
| `/sc:brainstorm --handoff design`, `/sc:workflow --handoff design` | Print a recommendation only; "design is interactive, user-initiated, not auto-invoked" (HR:177; OR:10; brainstorm.md:159) | A printed `/sc:design ...` line in a transcript is a suggestion, not a run |
| `/sc:release-split` Part 3 | Default command for release specs after an approved split (RS:270-275) | Runs inside the release-split run; see R row of section 3 |
| `/sc:auggie-review` remediation | Phase A of an opt-in five-phase chain, gated on explicit user acceptance (RH:27-61, 63-84; AR:54) | Part of a review-remediation chain, not a Spec step. Count it as that chain, not as a design step |

##### 6. Expected-step rule
- **`/sc:design` is never an expected step at any scope or complexity** (no cell is REQUIRED, section 3). A checker must not flag its absence, and must not flag its presence as a wrong step. Its absence is fine at T, B, S-LOW, F-LOW, R-LOW, and wherever a heavier design command is used instead.
- **What to expect instead (J):** at F-HIGH, R-HIGH and N-MEDIUM/HIGH, expect *a design artifact before the tasklist*: any of a `/tdd` output (`TASK-TDD-*` folder or `TDD_*.md`), a `bmad-architecture` spine (`ARCHITECTURE-SPINE.md`), a release-split spec, or a spec file with a design/interface section (scenario S5 "spec before tasklist", SC:36). Accept `/sc:design` as one valid producer only for a single interface section.
- **Short paths that are legitimate:** (a) `/sc:design` output going straight to `/sc:implement` when the work is one task (DS:109; RH:14 explains the per-task QA is lost for prose input); (b) a printed `/sc:design` suggestion from brainstorm or workflow that was never run (HR:177; OR:10); (c) `/sc:design` appearing inside the opt-in auggie remediation chain or inside release-split, which a user did not type as a Spec step (RH:63; RS:270-275).
- The "design" allowed-skip at S4 (SC:29) and "brainstorm or design" at S5 (SC:34) already agree with this: design is a one-of choice, not a fixed step.

Full file for the citation key, the footprint (section 5), the proposals (section 7) and the unverified items (section 8): [command-nuance/sc-design.md](command-nuance/sc-design.md)

#### 6.3.3 /sc:spec-panel (Spec)

##### 1. Status and role
- **Does**: "Multi-expert specification review and improvement using renowned specification and software engineering experts" (`SP:3`). Review-only in practice: "Will Not ... Modify specifications without explicit user consent" and "Generate specifications from scratch" (`SP:451-452`); HWW:61 and HWW:153 say it "only reports".
- **Phase / invocation**: Spec critique (also usable in Review). Standalone-invokable, not retired. No backing protocol skill: `~/.claude/skills/sc-spec-panel-protocol/` does not exist (checked); the protocol is inline in the command file (`integration-map.md:8-10` says the same). The file references neither `/sc:task` nor `/sc:tasklist` (grep, no hits); its "Next Step" names `/sc:design` or `/sc:implement` (`SP:462`).
- **Overlaps**: `bmad-review-adversarial-general`, `bmad-advanced-elicitation`, `bmad-party-mode` (a party-mode review sits beside a spec-panel review at `.dev/reviews/orca-catalogue-bundle-20260924/`), `/sc:adversarial`, `/sc:reflect --mode pre`, `/sc:business-panel`. See section 4.

##### 2. Flags
Usage line: `SP:22`. Complexity of the spec, not the scope label, is what moves these flags. "Default" says "not stated" where the file gives none.

| Flag | Values | Default | What it changes (cited) | Worth using when | Avoid when |
|---|---|---|---|---|---|
| positional spec | `@file` or inline text (`SP:22`) | none; required in every example (`SP:398-410`) | What is reviewed. Inline text is allowed but nothing is generated from nothing (`SP:452`) | `@file` always, so the review is tied to a path on disk | Inline text for anything an engineer will later cite; there is no file to point at |
| `--mode` | `discussion`, `critique`, `socratic` (`SP:22`, `SP:113-125`) | not stated (UNVERIFIED). The team guide always passes `critique` (`HWW:60`, `HWW:67`, `HWW:153`, `HWW:309`) | `critique` = findings with CRITICAL/MAJOR/MINOR, expert, recommendation, priority, grouped under `=== ... ANALYSIS ===` (`SP:121`). `discussion` = expert dialogue transcript (`SP:117`). `socratic` = questions only, no answers (`SP:125`) | `critique` for any gate-style review. `discussion` for a requirements workshop (`SP:400`). `socratic` to teach an author (`SP:403`, `SP:421-424`) | `discussion` / `socratic` when you need a finding list someone can pass or fail: neither mode defines severity grading |
| `--experts` | quoted comma list of surnames, e.g. `"wiegers,adzic,cockburn"` (`SP:22`, `SP:401`, `SP:410`) | auto-selected "based on specification type and focus area" (`SP:30`) | Narrows the panel to a subset of the 11 (`SP:101-111`, `SP:457`) | A narrow question on a small spec (J) | When you need the correctness artifacts: the Guard Condition Boundary Table names Nygard, Crispin and Whittaker (`SP:299`), and Whittaker is "Active in every panel review" (`SP:81`). What a subset does to those is not stated (UNVERIFIED) |
| `--focus` | one or more of `requirements`, `architecture`, `testing`, `compliance`, `correctness`, comma-separated (`SP:25`) | not stated (UNVERIFIED). Observed: `requirements,architecture,testing` in the 2026-09-24 review; `architecture,correctness,testing` in the 2026-10-22 rounds | Chooses the expert subset per area (`SP:129-190`). `correctness` also forces three outputs: State Variable Registry, Guard Condition Boundary Table, Pipeline Flow Diagram (`SP:184-188`) and "shifts" six experts (`SP:196-206`). A GAP row in the boundary table is MAJOR minimum and an incomplete table blocks the synthesis (`SP:316-318`) | `requirements` for a PRD (`HWW:60`); `architecture,testing` for a TDD (`HWW:67`); add `correctness` when the spec has 3+ mutable state variables, numeric-threshold guards or a pipeline (the command's own advisory trigger, `SP:190`); `compliance` when secrets, permissions or audit are in the spec (J, from `SP:162-171`) | `correctness` on a CRUD-only or prose-only spec: the pipeline heuristic itself does not fire on CRUD (`SP:337`) and the hard gates add output without finding anything. With no guards the table just says "No guard conditions identified" and does not block (`SP:297`) |
| `--iterations` | integer N (`SP:22`) | 1 ("Single Iteration (Default)", `SP:227`) | N>1 runs in-command passes: 1 structural, 2 detail and edge cases, 3 polish (`SP:234-252`). Adds the "Improve" step that writes an enhanced spec (`SP:34`) | Rarely. Documented phases stop at 3 (`SP:248`) | By default. The team guide does not use it: it says apply accepted findings, then re-run the same command "until no critical findings remain" (`HWW:61`). That conflicts with "will not modify specifications without explicit consent" (`SP:451`) (UNVERIFIED how reconciled) |
| `--format` | `standard`, `structured`, `detailed` (`SP:22`, `SP:254-266`) | not stated; `standard` is listed first (UNVERIFIED as default) | `standard` = YAML keys `specification_review`, `quality_assessment` (0-10 scores), `critical_issues`, `expert_consensus`, `improvement_roadmap`, `adversarial_analysis` (`SP:258`). `structured` = symbol-compressed (`SP:262`). `detailed` = full commentary and state traces (`SP:266`) | `standard` when a human or checker needs the verdict and scores fast (J). `detailed` for HIGH-complexity specs where Whittaker attack traces matter. Observed: the 2026-10-22 rounds used `detailed` and each round file is 84-112 KB (file sizes on disk) | `detailed` on a short, low-risk spec: volume without added decisions (J) |
| `--downstream roadmap` | `roadmap` (only value mentioned) | off | Adds roadmap frontmatter (`spec_type`, `complexity_score`, `complexity_class`, `target_release`, `feature_id`) and a scoped release spec in `release-spec-template.md` format (`SP:36`, `SP:272`, `SP:280`). NOT in the Usage line (`SP:22`) | Only inside the separate `/sc:roadmap` release pipeline, which `HWW:245` says to avoid "unless your lead says otherwise" | In the normal pipeline: `/roadmap` takes the PRD and TDD directly (`HWW:76`). Do not recommend it: the pipeline it feeds ends in `/sc:tasklist`, which is retired (brief ruling 3) |
| (auto) TDD input | no flag; detected by a weighted score >= 5 (`SP:35`) | on when detected | Scopes the improved output to one release using `target_release` from the TDD frontmatter; if it is empty or absent the command asks the user to specify it before going on (`SP:35`) | n/a | An unattended run: the question stops it (J, from `SP:35`) |
| (auto) PRD input | no flag; detected by persona/JTBD headings, frontmatter type or 3+ PRD headings (`SP:37`) | on when detected | Checks personas, stories, acceptance criteria and business alignment; no `target_release` needed (`SP:37`); Wiegers traces stories to FRs, Cockburn checks story structure, Adzic checks metric measurability (`SP:38`, `SP:284-287`) | n/a | n/a |

**Does not exist (people may assume)**: `--depth` (no hit in the file; sizing here is by `--focus`, `--experts`, `--iterations`, `--format`); `--output` / output-path flag; `--apply` / `--fix` (the command reports, the engineer edits); `--spec`, `--handoff`, `--tier`, `--dry-run`; a `--downstream` entry in the Usage line (it is mentioned in prose only); `--experts all`.

##### 3. Scope x complexity matrix
**What varies**: the command varies by the complexity of the SPEC under review, and it only applies when a written spec, PRD, TDD or story file exists (it will not write one, `SP:452`). TCS (`task-builder/SKILL.md:2406-2441`) is computed on a task file to pick a `/sc:reflect --depth`; it is not a spec-size formula, so no on-disk threshold exists for this command. The bands below are JUDGMENT, built from signals the command file and the repo name.

| Band | Signals (all JUDGMENT as a bundle; cited parts are file statements) |
|---|---|
| LOW | Spec sits in one subsystem; the author can name every file up front; no driving PRD/TDD; no guards, state or pipeline; none of secrets, permissions, user input, paths, infrastructure; design space already constrained (the 2026-06-23 planning record rejected a panel for slugs "design-covered three ways over", `03-planning-roi.md:43-52`, `:56-65`) |
| MEDIUM | Spec spans 2-3 subsystems or defines an interface other stories build against (shared interface); requirements are new or contested; a PRD or TDD drives it; at most a couple of guard conditions; one review round is expected |
| HIGH | Any of: 3+ mutable state variables, numeric-threshold guards, or a multi-stage pipeline (the command's own trigger for `--focus correctness`, `SP:190`, and for pipeline analysis, `SP:337`); touches secrets, permissions, user input, paths or infrastructure; cross-subsystem; "must not drift"; several rounds expected. Observed example: the orca upstream-tracking design spec (CI, release publishing, GitHub token permissions; 469 to 616 to 555 lines across rounds) got 11 panel rounds |

| Scope | LOW | MEDIUM | HIGH |
|---|---|---|---|
| **T** one-off | SKIP | SKIP | N/A: work that needs a written spec is no longer a one-off (hard limit, `HWW:22`) |
| **B** bug fix | SKIP | SKIP | OPTIONAL (J): only if the fix changes a contract or interface and a fix spec exists. `--mode critique --focus correctness` |
| **S** single story | SKIP (stated: skippable, `scenarios.md:29`) | OPTIONAL (J). `--mode critique --focus requirements` on the story file | WORTH IT (J). `--mode critique --focus requirements,correctness`; add `compliance` if secrets or permissions are in the story |
| **F** multi-story feature | OPTIONAL (J). Short agreed spec; guide 3.2 has no panel step (`HWW:91-106`). `--mode critique --focus requirements` | WORTH IT (stated for F in `CVP:66`; offered for a feature spec at `HWW:153`). `--mode critique --focus requirements,architecture,testing` | REQUIRED (J), in the sense "some spec critique before the tasklist"; spec-panel or a BMad equivalent satisfies it (`scenarios.md:34`). `--mode critique --focus architecture,correctness,testing --format detailed`, re-run after fixes until no CRITICAL (`HWW:61`) |
| **R** multi-feature release (re-rated) | OPTIONAL (J). Each feature's spec was already critiqued at F; critique only a new release-level spec | WORTH IT (J). Release plan or release TDD is a new cross-feature document (shared interfaces); `--mode critique --focus architecture,testing`; the command already knows release scoping (`target_release`, `SP:35`, `SP:272`) | REQUIRED (J), same sense as F HIGH, applied to the release-level spec. `--focus architecture,correctness,testing,compliance`; run once per document, not once per feature again |
| **N** new product | REQUIRED (stated: full-spec route, `HWW:309`, which has no complexity split). Use the cheapest panel: PRD `--focus requirements`, TDD `--focus architecture,testing` | REQUIRED (stated, `HWW:309`, `CVP:66`). Same flags as LOW, one pass each, one more pass if CRITICAL findings | REQUIRED (stated). PRD `--focus requirements,compliance`; TDD `--focus architecture,correctness,testing`; `--format detailed`; re-run each until no CRITICAL |

**R re-rating**: `CVP:66` rates R as OPTIONAL. Under the multi-feature definition (a release plan, implementation and push, one step below N) R is no longer just a ship step, so the critique of the release-level spec moves up: OPTIONAL to WORTH IT at MEDIUM, REQUIRED (J) at HIGH. LOW stays OPTIONAL.

##### 4. Choose this or the neighbour
| Neighbour | Decision rule by signal | Cited |
|---|---|---|
| `bmad-review-adversarial-general` | It takes any content (diff, spec, story, doc), forces at least ten findings in one pass, and outputs a bare list "no severity, priority, or ranking". Pick it for a quick cynical pass on a BMad-lane story or planning artifact in `_bmad-output/` (LOW/MEDIUM). Pick spec-panel when you need severity-graded, expert-attributed findings, a pass/fail on CRITICAL, or the correctness artifacts (HIGH, or a PRD/TDD going on to `/roadmap`). Either counts as "spec critique" for the checker (J) | `bmad-review-adversarial-general/SKILL.md` Step 2-3; `scenarios.md:34`; `CVP:230` |
| `bmad-party-mode`, `bmad-advanced-elicitation` | Different job: elicitation and multi-persona discussion. A party-mode review was run beside a spec-panel review on the same spec (`.dev/reviews/orca-catalogue-bundle-20260924/spec-review-party-mode.md`), so they are complements, not substitutes. Use spec-panel for the graded verdict | file listing of that folder |
| `/sc:adversarial` | One spec to critique: spec-panel. Two or more competing drafts to choose or merge: `/sc:adversarial --compare`. After a panel, run adversarial only when the panel leaves GAP rows or competing remedies; its integration table feeds GAP entries into adversarial's invariant round (J on "only when") | `HWW:152-153`; `SP:324-326`, `SP:384-390`; `CVP:230` |
| `/sc:reflect --mode pre` (and `reflect_pre` in a task file) | Different input. spec-panel judges whether the spec is good. `reflect --mode pre` judges whether the tasklist covers the spec. Order: spec-panel on the spec, then `/task-builder --spec`, then read `reflect_pre`. Running spec-panel does not replace the coverage check, and the coverage check does not replace a spec critique | `HWW:99-106`, `HWW:188-194`; `CVP:230` (O5) |
| `/sc:design`, `/tdd`, `/prd` | Producers, not rivals: spec-panel will not create a spec (`SP:452`). Run it after one of them has written the document | `SP:451-453`; `HWW:59-67` |
| `/sc:business-panel` | Business strategy, not spec quality | `HWW:155` |
| `/sc:swarm-wizard` | Reviewers from other model families. Add it, instead of re-running spec-panel a fourth time, when the same panel keeps returning the same MAJOR findings (J) | `HWW:154` |

Spec-panel is not a tasklist tool, so the `/sc:workflow` versus `/task-builder` rule does not apply to it. The only bridge: the finished, accepted spec is what `/task-builder --spec <path>` and `/sc:workflow` consume, and the validated rule (`/task-builder` + `/task` is the minimum for a multi-story feature) is unchanged by anything here.

##### 6. Expected-step rule
- **Expected**: N at any complexity, once on the PRD and once on the TDD, before the roadmap or tasklist step (`HWW:309`, steps 3 and 5). F HIGH and R MEDIUM/HIGH (J): some spec critique of the written spec before the tasklist; spec-panel or a BMad equivalent (`bmad-review-adversarial-general`) satisfies it (`scenarios.md:34`). After a pass that reported CRITICAL findings, expect a re-run or a written acceptance (`HWW:61`); a first pass with zero CRITICAL needs no re-run (J). Observed convergence: CRITICAL reached 0 at round 7 of 11; MAJOR was 0 at round 6, came back at 1-2 in rounds 7-10, and was 0 only in round 11 (`spec-panel-review-r11.md` metadata, "Earlier rounds" row; every round up to r10 is marked FAIL), so do not treat a single pass, or `--iterations 1`, as incomplete.
- **Absence is fine**: T, B, and S at LOW/MEDIUM (`scenarios.md:29`); F LOW and MEDIUM-with-no-new-interface (J); any scope where no written spec file exists (the command will not write one, `SP:452`); any scope with a recorded NO-GO and reason (`03-planning-roi.md:56-65`); a BMad-lane story where `bmad-create-story` and a BMad review ran instead. Never flag a missing `--iterations`, `--format`, `--experts` or `--downstream`: none is required by any file.

Full file for the citation key, the footprint (section 5), the proposals (section 7) and the unverified items (section 8): [command-nuance/sc-spec-panel.md](command-nuance/sc-spec-panel.md)

#### 6.3.4 /sc:tdd (Spec)

##### 1. Status and role
- **What it does (CMD:3):** "Create or populate a Technical Design Document (TDD) for a component, service, or system": researches the code with parallel agents, then assembles the 28-section template with independent QA gates (SK:8-12; SM:36-117). It is the Technical Design Document, NOT test-driven development (CMD:11, CMD:156; HW:283).
- **Phase and status:** Spec phase (design step). Standalone-invokable, NOT retired. `/sc:tdd` and `/tdd` are the same skill (CMD:148-156 "invoke: Skill tdd"; HW:283). The command file, SK and all five refs name neither `/sc:task` nor `/sc:tasklist` (none seen in the full read); Stage B hands the built task file to `/task` (SK:411).
- **Overlaps:** `/sc:design` (one-pass draft of one design), `bmad-architecture` (invariants spine), partly `/tech-research` (research first) and the spec-file route of HW 3.2 (HW:98).

##### 2. Flags
All flags are defined ONLY in the command file (CMD:43-51). A grep of SK and the five refs for `--tier`, `--resume`, `--from-prd`, `--prd`, `--focus`, `--output`, `--depth` returned nothing: the skill describes the same four inputs in prose (SK:37-48) and picks the tier itself (SK:226, SK:75-80). Whether the flags are honoured as written is therefore UNVERIFIED (U1).

| Flag | Values | Default | What it changes | Worth using when | Avoid when |
|---|---|---|---|---|---|
| `<component>` (positional, required) | free text: component, service or system plus why | none | Becomes GOAL/WHY of the request (SK:39, SK:172-178). Topic-only input "will work but produces broader, less focused results"; no input at all gives agents "no context" (CMD:136-146). If it is too vague to search, the skill asks; otherwise it proceeds without quizzing (SK:50-61 vs SK:190) | Always: name the component and why a design is needed | A bare topic such as `"wizard"` |
| `--from-prd` / `--prd` (alias) | path to a PRD | none | Adds `research/00-prd-extraction.md` (SK:104; OG:101), traces every FR to a PRD epic (AP:189; VC:30 FR-trace check), inherits scope and sets `parent_doc` (OG:99-105). Without it PRD_CONTEXT is "N/A", a feature description is the requirements source (SK:44, SK:268) and FR rows are marked `[NO PRD TRACE]` (AP:189) | A PRD exists, from `/prd` or `bmad-prd`. Repo evidence: `.dev/releases/current/v2-m3/TDD_V2_M3.md:14` has `parent_doc` pointing at a BMad PRD | The "PRD" is a stub with no epics or acceptance criteria (every FR will carry `[NO PRD TRACE]`) |
| `--tier` / `-t` | `lightweight`, `standard`, `heavyweight` | `standard` (CMD:46) | Codebase agents 2-3 / 4-6 / 6-10+, web agents 0-1 / 1-2 / 2-4, target lines 300-600 / 800-1,400 / 1,400-2,200 (CMD:57-61; SK:69-73); QA checks the line budget (VC:97) and requires SLO/SLI tables for Standard and Heavyweight only (AP:378). The BUILD_REQUEST encodes all seven phases and both QA gates whatever the tier (BR:98-160), so the tier changes size, not the gate structure (whether the builder trims Lightweight: U3) | Heavyweight when the design spans several services, layers or integration boundaries (SK:80) or the request says "detailed", "comprehensive", "thorough" (SK:78). Lightweight only when "genuinely narrow": single service, under 5 relevant files (SK:79) | Lightweight "to save time": the same phases run (BR:98-160). Also: CMD:59 lists "Bug fixes, config changes" under Lightweight, but SK:71 does not and HW routes bugs to `/sc:troubleshoot` (HW:311) |
| `--resume` / `-r` | path to the MDTM task file | none | Per CMD:28-29 resumes an interrupted session. The skill does this on its own: A.1 looks in `.dev/tasks/to-do/` for `TASK-TDD-*` with unchecked `- [ ]` items and skips to Stage B (SK:157-167); `/task` then continues from the first unchecked item (SK:149; OG:126) | After a crash or lost session; give the folder's task file | Starting over (the skill finds the prior folder anyway, SK:116) |
| `--output` / `-o` | path for the final TDD | auto: stub location if a stub exists, else `docs/[domain]/TDD_[COMPONENT-NAME].md` (SK:48, SK:111) | Where the assembler writes the TDD (BR:148; path rule SK:111) | The downstream reader expects another path. Observed TDDs sit at `.dev/releases/current/v2-m3/TDD_V2_M3.md`, `.dev/releases/complete/v1.3-2026Upgrade/TDD_VSCODE_AIDEV02.md`, `_bmad-output/planning-artifacts/tdd.md`, not under `docs/` | Never harmful; omit to take the default |
| `--focus` / `-f` | comma-separated directories or files | all | Bounds scope discovery and the research assignments (SK:46, SK:194-199); "saves significant time" (SK:46) | Whenever the directories can be named (the author "can name the files up front", a LOW-complexity signal) | Scenario B, where broad discovery is the point (SK:186-188, SK:198) |
| Keywords in the request (not flags) | "detailed", "comprehensive", "thorough"; multi-service, multi-layer scope | n/a | Force Heavyweight (SK:78, SK:80) | When you want the deepest run | When the scope is narrow: the keyword overrides it |
| BUILD_REQUEST `TEMPLATE: 01\|02` (set by the skill, not the user) | 01 simple, 02 complex | 02 ("almost always", SK:349) | Selects the MDTM template the builder uses (BR:17-19; SK:331-349) | n/a | n/a |

Short forms in CMD:43-51: `-t`, `-r`, `-o`, `-f`; `--prd` is an alias for `--from-prd`.

**Flags and behaviours that do NOT exist:**

- No `--depth`. The tier is the only depth control (`--depth` belongs to `/sc:workflow`, `/sc:troubleshoot`, `/sc:reflect`). No `--spec`, `--handoff`, `--type`, `--format` (those are other commands).
- No flag to skip, shorten or turn off QA gates, research or web research. CMD:175 lists "Skip investigation phases to produce faster but shallower output" under Will Not; web research is driven by gaps, not a flag (OG:17).
- `/sc:prd` is named at CMD:172 and CMD:182, but `/home/coder/.claude/commands/sc/` holds no `prd.md` (only `design.md` and `tdd.md` matched `prd|tdd|design`). The PRD step is `/prd` or `bmad-prd` (U5).
- No automatic hand-off flag. Phase 7 only asks the user whether to build implementation tasks (BR:158).

##### 3. Scope x complexity matrix
**Does the command vary by complexity?** Yes, but only in size, not in structure. The one internal switch is the tier, chosen by relevant-file count and service/layer breadth (SK:69-80). The same seven phases and QA gates are encoded at every tier (BR:98-160). `/task-builder`'s TCS formula (task-builder SKILL lines 2410-2441) does NOT apply to `/tdd`: the TDD skill has no TCS and no `reflect` call (grep of SK for `TCS|reflect` found nothing). TCS applies later, to the task file built FROM the TDD.

**Bands for this command** (file counts and breadth are the only thresholds on disk, SK:71-73, SK:80; everything else is JUDGMENT):

| Band | Signals | Tier it maps to |
|---|---|---|
| LOW | under 5 relevant files, one service or component, author can name the files, no one else builds against it (SK:71; CMD:59) | `lightweight` |
| MEDIUM | 5-20 files, one subsystem, moderate complexity (SK:72) | `standard` |
| HIGH | 20+ files, or several services, layers or integration boundaries, or platform-scale (SK:73, SK:80); also "others will build against it" and "must not drift" (HW:20, HW:18) (J) | `heavyweight` |

**Cost note (my sum from BR, not a file statement):** every run spawns at least 7 fixed agents beyond research (Phase 3 analyst + QA: BR:121; Phase 5 analyst + QA: BR:142; Phase 6 assembler, structural QA, qualitative QA: BR:148-151), plus 2-3 or more codebase agents (CMD:59-61), at least one synthesis agent (SM:149-163), an optional PRD extraction item (BR:111) and a reuse-audit pass (SK:212). `/task` adds its own phase-gate QA on top (SK:414; VAL E2 gives "at least 6 agents" per phase after the first, TK:188-199, not re-read here). So even Lightweight is a heavy run; that is why LOW is mostly SKIP.

| Scope | LOW | MEDIUM | HIGH |
|---|---|---|---|
| **T** one-off | SKIP | SKIP | SKIP (J: a HIGH one-off is not a one-off, reclassify; HW:22) |
| **B** bug fix | SKIP (HW:311 has no design step; CMD:59 names bug fixes under Lightweight, which conflicts) | SKIP | SKIP (J: a design-sized fix is an F; use `/sc:troubleshoot --fix`, HW:125-126) |
| **S** single story | SKIP (J: `/sc:design` for one interface, HW:98) | SKIP (J) | OPTIONAL (J) `--tier standard --from-prd <spec>` only if other engineers build against the story; a HIGH single story usually means it is really an F |
| **F** multi-story feature | SKIP (J: a short agreed spec file, HW:91-98) | OPTIONAL (J) `--tier standard --from-prd <spec> --focus <dirs>`: when stories share an interface and several people build, or no spec exists | WORTH IT (J) `--tier heavyweight --from-prd <prd> --focus <dirs>`: HW:20 "major feature that other people will build against", multiple services or layers (SK:80) |
| **R** multi-feature release | OPTIONAL (J) | WORTH IT (J) `--tier standard`: one release-level TDD for cross-feature interfaces plus sections 19, 24, 25 (rollout, release criteria, operational readiness: SM:90, SM:105, SM:108) | WORTH IT (J) `--tier heavyweight`; per-feature TDDs follow the F HIGH row. Input for `/sc:release-split` (HW:72, HW:309) |
| **N** new product | REQUIRED (HW:20, HW:309; band sets tier: `--tier lightweight` allowed for a tiny product, J) | REQUIRED `--tier standard --from-prd <prd>` | REQUIRED `--tier heavyweight --from-prd <prd>` (CMD:61 "New systems") |

Notes on the cells:

- N is REQUIRED because HW's `full-spec` route lists `/tdd` unconditionally (only steps 1 and 6 are marked optional, HW:309) and CV:68 already rates N REQUIRED. In the BMad lane the same step is `bmad-architecture` (CV:88), and the repo shows both were used together (section 4).
- N is greenfield, but the skill's discovery is codebase-first (SK:194-199) and CMD:173 forbids "architectural decisions without codebase evidence". How it behaves with no code to scan: U15.
- **R re-rating.** CV:68 rates R as SKIP. Under Ryan's definition (a multi-feature release includes the plan, the build and the push), design work for shared interfaces and rollout happens inside R, so SKIP is too low: proposed OPTIONAL at LOW, WORTH IT at MEDIUM and HIGH. All three are (J): no file rates `/tdd` for a release. CV:139 states the "release ships already built work" reading only for the Implement table; whether the /tdd row used it is unknown.

##### 4. Choose this or the neighbour
**4a. `/tdd` vs `/sc:design`**

| Signal | Pick `/sc:design` | Pick `/tdd` |
|---|---|---|
| What is being designed | One interface (API, component, schema), `--type api\|component\|database\|architecture` (DES:22) | A whole component, service or subsystem (SK:72-73) |
| Who builds against it | The same engineer or one story; the output is pasted into a spec file (HW:98) | Other people (HW:244, HW:20) |
| Requirements to trace | None, or the prompt itself | A PRD with epics and acceptance criteria to trace requirement by requirement (SK:44; AP:189) |
| Evidence standard | Single pass; reads existing system context (DES:27) but describes no parallel research, verification tags or QA gates | Every claim code-verified with file:line, doc-only claims excluded, independent reviewers (OG:13-19, VC:117-118) |
| Downstream | `/sc:implement` per DES:109 (stale for F and above, see 4e) | `/roadmap`, `/task-builder --spec <TDD>` (roadmap SKILL:12, task-builder SKILL:41) |
| Size | Under 5 files and one interface (J) | 5 or more files (SK:72) |

Rule (J built from those rows): if you can name one interface and one reader, use `/sc:design` and put the result in a spec file; a Lightweight TDD still runs the full pipeline (section 3 cost note), so it rarely beats `/sc:design` plus a short spec. They stack rather than compete: CMD:183 calls `/sc:design` "complementary", and the TDD already contains diagrams (VC:101).

**4b. `/tdd` vs `bmad-architecture`**

| Signal | Pick `bmad-architecture` | Pick `/tdd` |
|---|---|---|
| Artifact | A lean spine of invariants: paradigm, boundaries, state ownership; "record decisions, not rationale" (BA:9, BA:17) | A full 28-section engineering spec: requirements, data models, API, testing, rollout; detailed enough to "begin implementation from the TDD alone" (OG:35; SM:36-117) |
| How decisions are made | Coaching by default: it elicits the invariants from the user (BA:21) | Autonomous research pipeline; "do NOT interrogate the user" (SK:190) |
| Brownfield | Reads real code to ratify existing conventions (BA:25) | Verifies every claim against code (OG:13-19) |
| Altitude | Scales: a few decisions for a small thing, comprehensive for a platform; initiative, feature or epic (BA:15, BA:29) | Scales by tier only (SK:69-73) |
| Lane | BMad lane; next step `bmad-create-epics-and-stories` (BA:76; CV:88, CV:116) | Task-file lane; next step `/roadmap` or `/task-builder --spec` (HW:309) |

Rule: when the invariants are still undecided, run `bmad-architecture` first. When they are decided and a detailed spec is needed (HIGH F, R, N), `/tdd` fills the detail. Repo evidence says they stack: `_bmad-output/planning-artifacts/tdd.md:4,14-18` describes itself as an "Engineering bridge document" with `parent_doc` `prd.md` and `depends_on` `architecture.md`, and `.dev/releases/current/v2-m3/TDD_V2_M3.md:14` has a BMad PRD as parent. At LOW and MEDIUM pick ONE; at HIGH F, R and N both are legitimate. This contradicts CV:223 ("pick the lane at the Spec step and stay in it") for the design step.

**4c. `/tdd` vs the PRD step (`/prd`, `bmad-prd`) and the spec-file route.** The TDD takes a PRD as input (SK:44), so it is downstream, not an alternative. When requirements are already clear and the feature extends an existing system, HW 3.2 needs no PRD and no TDD: a short agreed spec file plus `/task-builder --spec` (HW:91-98, HW:307). That is the F LOW and often F MEDIUM answer.

**4d. `/tdd` vs `/tech-research`.** If you do not yet know how the current system works or whether the idea is feasible, research first (HW:19). The TDD researches the code too, but only to document a design, bounded by `--focus`. Feasibility question with no design wanted: `/tech-research`. Design wanted and the system is understood: `/tdd`.

**4e. What comes after a TDD (stale hints in CMD).** CMD:184 names `/sc:workflow` for "post-TDD implementation planning" and CMD:171 names `/sc:implement` for implementation. A TDD only appears at HIGH F, R or N, and VAL confirms `/task-builder` + `/task` is the minimum for a multi-story feature while `/sc:workflow` + `/sc:implement` is not eligible (VAL Verdict 1). So downstream of a TDD, a checker should expect `/roadmap` or `/task-builder --spec <TDD path>`, not `/sc:workflow`. BR:158 (Phase 7) offers to build implementation tasks "using the `/task` skill"; `/task` only executes files (HW:242), so the builder step is `/task-builder` (U6). Neither retired command (`/sc:task`, `/sc:tasklist`) is referenced by this command.

##### 6. Expected-step rule
- **Count `/tdd` (or `bmad-architecture` in the BMad lane) as expected only at N, any band** (HW:309; CV:68). At HIGH F and at R MEDIUM/HIGH treat it as a soft expectation (J): do not flag its absence when a spec file, an existing architecture spine, or a PRD plus architecture pair covers the same scope (HW:98; section 4b), and never flag it as a skipped step at T, B, S, or F LOW/MEDIUM.
- **Its presence at T, B or S is over-process, not a violation**; a checker should note it, not fail it. If a TDD exists, the next expected step is `/roadmap` or `/task-builder --spec <TDD>`, not `/sc:workflow` (section 4e). Treat `/tdd` and `/sc:tdd` as one command, and ignore "tdd" hits that mean test-driven development.

Full file for the citation key, the footprint (section 5), the proposals (section 7) and the unverified items (section 8): [command-nuance/sc-tdd.md](command-nuance/sc-tdd.md)

#### 6.3.5 /sc:research (Spec)

##### 1. Status and role

- **Does**: "Deep web research with adaptive planning and intelligent search" (CMD:3); writes a report only, no implementation (CMD:124-142). Standalone-invokable, NOT retired; CMD never mentions `/sc:task` or `/sc:tasklist` (grep: none). Serves the Spec phase as a side input for OUTSIDE knowledge (library, standard, best practice): routing row `external-research` (HWW:312), HWW 3.5 (HWW:143). It is also called automatically by `/sc:brainstorm` as "research light" (BS:185).
- **Backing protocol skill `~/.claude/skills/sc-research-protocol/` DOES NOT EXIST** (`ls` failed; `find` under `~/.claude` finds no `*research-protocol*`). CMD names no skill; it runs from its own file plus the `deep-research-agent` persona (CMD:7), AGT and CFG (CMD:93,97). HWW:232 allows a command with no skill, but BS:185 and HR:49,76 tell brainstorm to call `Skill sc-research-protocol` / `Skill sc:research-protocol`, which cannot load; HR:55 supplies a WebSearch fallback.
- **Overlaps**: `/tech-research` (our code, has its own web phase), `bmad-technical-research` (BMad lane; requires web search, `.claude/skills/bmad-technical-research/SKILL.md:8,21`), `bmad-domain-research` / `bmad-market-research` (content UNVERIFIED), and the `feasibility-probe` swarm lens that points at this command (`skills/sc-swarm-wizard-protocol/refs/cli-contract.md:47`).

##### 2. Flags

CMD has exactly two flags plus one positional argument (CMD:25; grep of `--` in CMD finds only `--depth` and `--strategy`). AGT and CFG define no further user-facing flags.

| Flag / arg | Values | Default | What it changes (cited) | Worth using when | Avoid when |
|---|---|---|---|---|---|
| `"[query]"` (positional) | free text | none; behaviour when missing is UNVERIFIED | Becomes the research question (CMD:25). Step 1 scores "query complexity and ambiguity" (CMD:32), and step 3 scales the task list "to query complexity (3-15 tasks)" (CMD:46) | Always. Put question, why, and constraints in it (HWW:30-35, four-part request rule) | The question is about our own code: use `/tech-research` (HWW:247) |
| `--depth` | `quick`, `standard`, `deep`, `exhaustive` (CMD:25) | **Not stated in CMD or CFG.** CFG has no depth default (CFG:5-13); `max_hops: 5` (CFG:8) equals exhaustive's hop count but is not labelled a depth. UNVERIFIED | Hops: quick 1, standard 2-3, deep 3-4, exhaustive 5 (CMD:86-91). Profiles (CFG:66-71): quick = 10 sources, 1 hop, 2 min, confidence 0.6, `basic` search, search only; standard = 20, 3 hops, 5 min, 0.7, basic, search+extract; deep = 40, 4 hops, 8 min, 0.8, **advanced** search+extract, adds `tavily-map`; exhaustive = 50+, 5 hops, 10 min, 0.9, advanced, adds `tavily-crawl`. Caps: maps=2, crawls=1, crawl result max 50 URLs (CFG:77-78). Global ceiling 10 min / 10 iterations / 5 hops (CFG:35) | `deep`: the guide sets `--depth deep` as the mandatory flag on `external-research` (HWW:312, example HWW:143); `/sc:recommend` emits it too (`skills/sc-recommend/SKILL.md:255`). `quick`: one-fact lookup; brainstorm uses it (BS:185) | `exhaustive` for a fact one official page answers (spends the full 10 min, CFG:71). Omitting the flag in routine use: the bare default is undocumented |
| `--strategy` | `planning`, `intent`, `unified` (CMD:25) | `unified` (CFG:6). Mapping of flag names to config keys `planning_only` / `intent_planning` / `unified` (CFG:18-20) is by inference: UNVERIFIED | `planning`: no clarification, executes immediately. `intent`: asks up to 3 clarifying questions, then executes. `unified`: optional clarification, **presents the plan and executes only after user confirmation** (CFG:17-20; AGT:38-56). Selection indicators (CFG:39-43): clear, well-scoped query -> planning; ambiguous or broad -> intent; complex multi-faceted or high-stakes -> unified | `planning` for a clear narrow question, and in any unattended run. `unified` for high-stakes or multi-faceted topics (CMD:114 example) | `unified` when no human is watching: it waits for confirmation (CFG:20). `intent` when the question is already precise |

**Does not exist** (grep of CMD, AGT, CFG): `--output`, `--format`, `--sources`, `--hops`, `--handoff`, `--fix`, any QA-intensity flag. Output formats `summary` / `report` / `academic` are a CFG concept (CFG:125-129) with no flag in CMD. The report path is fixed: `claudedocs/research_[topic]_[timestamp].md` (CMD:104,135). `--research light|deep` belongs to `/sc:brainstorm`, not here (BS:185-186). The depth tiers and QA-intensity override at TR:99-121 belong to `/tech-research`, a different command.

##### 3. Scope x complexity matrix

**Complexity here means how hard the OUTSIDE question is, not how big the code change is.** The command does vary by complexity: through `--depth` and `--strategy`. No file gives a numeric threshold (TCS at `skills/task-builder/SKILL.md:2410-2441` scores task files, not research queries), so the bands below are JUDGMENT, built from the signals CFG already uses for strategy (CFG:39-43) and the profile table (CFG:66-71).

| Band | Definition (signals) | Flags (J) |
|---|---|---|
| LOW | One factual question, one authoritative source likely; "clear query, technical docs, well-defined scope" (CFG:41) | `--depth quick --strategy planning` |
| MEDIUM | One topic, several facets or two or three options to compare; answer needs cross-checking sources | `--depth standard`, or `deep` to follow the guide (HWW:312); `--strategy planning` |
| HIGH | Multi-faceted, ambiguous, or high-stakes decision resting on outside facts (CFG:43); the answer could change the design | `--depth deep --strategy unified` (`exhaustive` only for a whole-domain survey) |

Scope here is the size of the work the research serves. No file rates `/sc:research` REQUIRED anywhere: the guide's `external-research` row is an intent route (`changes_files: no`, HWW:312), not a mandatory step.

| Scope | LOW | MEDIUM | HIGH |
|---|---|---|---|
| T one-off | SKIP (J) | SKIP (J) | OPTIONAL (J) `--depth standard`; a one-off rarely needs more than a doc lookup |
| B bug fix | SKIP (J) | SKIP (J) | OPTIONAL (J) `--depth standard`, only after `/sc:troubleshoot` points at third-party behaviour |
| S single story | SKIP (J) | OPTIONAL (J) `--depth standard` | OPTIONAL (J) `--depth deep` |
| F multi-story feature | SKIP (J) | OPTIONAL (J) `--depth standard` | WORTH IT (J) `--depth deep --strategy unified` |
| R multi-feature release (new definition) | SKIP (J) | OPTIONAL (J) `--depth standard` | WORTH IT (J) `--depth deep`; e.g. a dependency or standard that several features share |
| N new product | OPTIONAL (J) `--depth quick` | WORTH IT (J) `--depth standard` or `deep` | WORTH IT (J) `--depth deep --strategy unified` |

Every cell is `(J)`: no file ties this command to a scope or a complexity band. N MEDIUM/HIGH keep the existing WORTH IT rating in `command-value-by-phase.md` (Section 2.1, `/sc:research` row).

##### 4. Choose this or the neighbour

| Neighbour | Decision rule (by signal) | Cited |
|---|---|---|
| `/tech-research` | **Where the answer lives.** Question names our code, or "how does our system work / what would need to change / is it feasible" -> `/tech-research`. Question is a library, standard, or best practice outside our code -> `/sc:research`. Never use `/tech-research` for a pure web question (`sc-recommend/SKILL.md:255` says so) | HWW:247, HWW:143, HWW:308 |
| `/tech-research` (mixed question) | If the work needs both (our code plus an outside library), `/tech-research` already runs a web phase: 0-1 web agents at Quick, 1-2 at Standard, 2-4 at Deep (TR:99-103; web phase TR:388). Run `/sc:research` first only when the outside answer decides whether the code investigation is worth doing | TR:99-103, TR:388 |
| `/tech-research` (cost) | `/tech-research` runs at its deepest setting by default with many agents (HWW:255) and at least 11 agents at the final gate (TR:27). `/sc:research` stops at one report with a 10 min ceiling (CFG:35). For a question that only needs outside facts, `/sc:research` is the cheap path | HWW:255, TR:27, CFG:35 |
| `/tech-research` (what follows) | `/tech-research` feeds `/task-builder` (HWW:19, HWW:308). `/sc:research` has no routed next step in the guide. Its own file says "use `/sc:design` ... or `/sc:implement`" (CMD:142), which skips the tasklist step and disagrees with HWW:308 (report -> `/task-builder`). Treat the CMD line as stale (J) | CMD:142, HWW:308 |
| `bmad-technical-research` | **Lane.** In the BMad lane use `bmad-technical-research`; it also requires web search (SKILL.md:21) and writes `{planning_artifacts}/research/technical-<slug>-research-<date>.md` (SKILL.md:91). This resolves `command-value-by-phase.md` U8 for the web/code question: web. Inside one lane, run one of the two, not both | `.claude/skills/bmad-technical-research/SKILL.md:8,21,91` |
| `/sc:brainstorm --research light` | Not an engineer decision. Brainstorm calls `/sc:research --depth quick` itself for framework/library topics not in the project (BS:185); `--research deep` routes to `/tech-research`, with `sc-research-protocol --depth deep` only as fallback (BS:186, HR:70-76). Do not run `/sc:research` again for the same topic | BS:185-186, HR:49,70-76 |
| Plain library lookup (context7 / `WebSearch`) | For one API signature or flag, CFG routes tech docs to context7 (CFG:116) and "native" for simple explanations (CFG:117). `/sc:research --depth quick` is a heavier way to get the same answer (J) | CFG:112-117 |
| `/sc:swarm-wizard` | Different job (review by other model families). `feasibility-probe` lens names `/sc:research` as the human-run precursor (cli-contract.md:47), not a replacement | `skills/sc-swarm-wizard-protocol/refs/cli-contract.md:47` |

Retired commands: none of the above route through `/sc:task` or `/sc:tasklist`.

##### 6. Expected-step rule

- **Never count `/sc:research` as an expected step at any scope or complexity.** It is OPTIONAL or WORTH IT at most (Section 3), no pipeline lists it, and the guide's own routing row makes it an answer-only route (HWW:312, `changes_files: no`). Its absence is always fine, including for N.
- **Presence is also fine at any scope.** At most, a checker may treat "N or F HIGH, spec cites an outside standard or library, and no research artifact of any kind (`/sc:research` report, `/tech-research` report with a web phase, or `bmad-technical-research` file)" as an advisory note (J), never a skipped step. Do not flag a short path that omits it, and do not flag a different depth than `deep`: depth is a flag and leaves no footprint (Section 5).

Full file for the citation key, the footprint (section 5), the proposals (section 7) and the unverified items (section 8): [command-nuance/sc-research.md](command-nuance/sc-research.md)

#### 6.3.6 /sc:adversarial (Spec)

##### 1. Status and role

- **Does:** "Structured adversarial debate, comparison, and merge pipeline for 2-10 artifacts" (`~/.claude/commands/sc/adversarial.md:3`). Five steps: diff, debate, scoring and base pick, refactor plan, merge (`adversarial.md:76`). Backing skill exists: `~/.claude/skills/sc-adversarial-protocol/SKILL.md` (2998 lines, 128,257 bytes) plus `refs/` (4 files). Loading it is mandatory (`adversarial.md:145-149`).
- **Phase and status:** Spec (choose between competing drafts; `HOW-WE-WORK.md:152`, routing row `compare-options` at `:314`). Standalone-invokable, NOT retired. Not in Ryan's pipelines or in any HOW-WE-WORK level 1-6. Also runs INSIDE other commands (see section 4).
- **Overlaps:** `/sc:spec-panel` (critique of one spec), `/sc:brainstorm` (calls it in Wave 3), `/sc:reflect` and `/sc:troubleshoot` (call it in Tier 2), `/sc:release-split` (calls it in Mode B), `bmad-review-adversarial-general` (name only). `adversarial.md:182` lists the retired `/sc:tasklist` as a related command: never route to it.

**Complexity here is not code size.** It is: how many competing artifacts (N), how big they are together, and how costly a wrong pick is. Scope is only a proxy.

##### 2. Flags

Citation key (all under `~/.claude/`): **AD** = `commands/sc/adversarial.md`; **SK** = `skills/sc-adversarial-protocol/SKILL.md`; **DP** / **AS** / **SP** / **AT** = `skills/sc-adversarial-protocol/refs/` `debate-protocol.md` / `agent-specs.md` / `scoring-protocol.md` / `artifact-templates.md`. "Observed" = counted on disk in this checkout on 2026-10-27: 32 `debate-transcript.md` files, of which 31 are in the `adversarial/` layout and 1 is a roadmap-CLI look-alike (section 5).

###### 2.1 Every flag and argument

| Flag | Values | Default | What it changes | Worth using | Avoid |
|---|---|---|---|---|---|
| `--compare`, `-c` (Mode A) | 2-10 file paths, comma separated | none | Files copied to `adversarial/variant-N-original.md` (SK:62-63). Count 2-10 enforced; non-`.md` only warns (SK:561-563, 567). One advocate per file (SK:1031-1033) | You already hold the competing drafts (HOW-WE-WORK:152) | Fewer than 2 files (AD:171). Near-identical files (see 2.3) |
| `--source`, `-s` (Mode B) | one file path | none | Source for variant generation (SK:68-71) | No drafts yet, want N generated from one source | Idea still vague: use `/sc:brainstorm`, which wraps this (`brainstorm.md:133`) |
| `--generate`, `-g` (Mode B) | artifact type word (roadmap, spec, design...) | none | Only labels the generated artifact; callers use `spec` for everything (`skills/sc-release-split-protocol/refs/adversarial-integration.md`: "the `--generate` value only controls artifact labeling") | With `--source` | Alone: all three Mode B flags are required together (SK:575) |
| `--agents`, `-a` (Mode B) | `model[:persona[:"instruction"]]`, 2-10 specs | none | Each spec generates one variant AND is that variant's advocate (AS:195-196). All agents dispatched in parallel (SK:2204-2206) | Want model or persona diversity | Mixing with `--compare`: SK:555 says STOP, yet SK:1032 and AS:191 say Mode A "defaults to current model if `--agents` not specified" (see U1) |
| `--pipeline` | inline `"generate:a,b -> compare"` or `@file.yaml` | none | Routes to the DAG meta-orchestrator (SK:538-549). Mutually exclusive with Mode A/B flags | Multi-stage generate-then-compare with checkpoints | Anything a single Mode A/B call does. Observed: zero `pipeline-manifest.yaml` on disk |
| `--pipeline-parallel` | integer 1-10 | `3` | Max concurrent phases per DAG level (SK:2722-2723, 2742-2746) | Wide generate stages | Without `--pipeline` (no effect) |
| `--pipeline-resume` | flag | `false` | Re-reads `pipeline-manifest.yaml`, skips phases whose SHA-256 still match (SK:2821-2852) | Pipeline died mid-way | Edited artifacts: mismatch re-runs that phase and all downstream |
| `--pipeline-on-error` | `halt`, `continue` | `halt` | Failed phase marks dependents `skipped`; `continue` lets independent branches run (SK:2943-2993) | `continue` when branches are independent | `continue` when a compare phase would get under 2 inputs (it fails) |
| `--depth`, `-d` | `quick`, `standard`, `deep` | `standard` | quick = Round 1 only; standard = Rounds 1+2 and Round 2.5 invariant probe; deep = adds Round 3 only if convergence is still under threshold after Round 2 (SK:1083, 1111-1112, 1361-1364; DP:148-152). Unknown value warns and uses standard (SK:595-598) | The main cost lever (2.2) | `deep` on small or consensus-heavy inputs: Round 3 is conditional, so it often adds nothing |
| `--convergence` | 0.50-0.99 | `0.80` (callers pass 0.75: `brainstorm.md:58`) | Agreement bar for stopping, for Round 3, and for the stable-majority exit (SK:1441-1444, 1361). Out of range warns and uses 0.80 (SK:599-602) | Raise for decisions that are expensive to reverse (J) | Tuning it at `--depth quick`: DP:150 says no convergence check at quick |
| `--interactive`, `-i` | flag | `false` | Four `AskUserQuestion` pauses: after diff, after debate, after base pick, after refactor plan (SK:1911-1955) | Large N or stakes where you want to override the base | Unattended or scheduled runs; runs started by `/sc:reflect` or `/sc:troubleshoot` (they pass only what they set) |
| `--output`, `-o` | directory | "Auto-derived from input file directory" (SK:605-606; AD:69 says "Auto") | Artifacts go to `<output>/adversarial/` (SK:371-385). Refuses `.claude/skills/`, `.claude/agents/`, `.claude/commands/` before any write (SK:41) | Always set it to a `.dev/` path so the footprint is findable and committable | Leaving the default: output lands next to the first input file |
| `--focus`, `-f` | comma list | all | Injected into each advocate prompt as "Focus on these areas" (SK:981). No step is skipped by it in the protocol text | Narrow big artifacts to the risks that matter, e.g. `correctness,risk,test-coverage` (`sc-troubleshoot-protocol/SKILL.md:437`) | Expecting it to cut calls or tokens (UNVERIFIED, U2) |
| `--blind` | flag | `false` | Strips model names from artifacts before compare phases (SK:2856-2886). Spelled out only inside pipeline artifact routing | Mode B variants from different models, to stop brand bias | Same-model variants, or reviewer cards. Effect outside `--pipeline` UNVERIFIED (U3). Observed: no `blind/` dir anywhere |
| `--auto-stop-plateau` | flag | `false` | Pipeline halts when convergence moves under 0.05 for 2 consecutive compare phases (SK:2899-2926) | Long multi-compare pipelines | Anything else. By the algorithm it needs 3 compare phases (derived from SK:2915-2922) |
| `--dry-run` / `--pipeline-dry-run` | flag | `false` | Pipeline only: validates the DAG, prints plan and "Estimated Token Costs", runs nothing (SK:2546-2547, 2575-2580). **Not in the AD option table (AD:56-72)** | Only built-in cost preview | Mode A/B: no dry run exists |
| `--suspect-source` | file list | none | Named by `sc-bare-review` as the next step (`sc-bare-review/SKILL.md:3,18,55`). **No definition in AD, SK, or refs** (grep for "suspect" found nothing there) | Do not use until defined | Always (U4) |

###### 2.2 Does not exist (people may assume)

`--rounds`, `--measure-first`, `--verdict-per-claim` (named as fabricated in `sc-recommend/SKILL.md:337`); `--proposals` (that is `/sc:brainstorm`, `brainstorm.md:48`); a flag to stop after Step 3 or skip the merge (none in AD:56-72 or SK:332-344: every full run writes `refactor-plan.md` and a merged output); a similarity-threshold flag (the 10% skip is fixed, SK:406-409); `--model`; a size cap or chunking flag (no size limit in the protocol); `--dry-run` for Mode A/B.

###### 2.3 Cost drivers, by number and size of artifacts (derived from the protocol; counts are JUDGMENT)

| Driver | Text | Effect |
|---|---|---|
| Protocol load | SKILL.md is 128,257 bytes (`ls`). `sc-recommend` rule: do not load a protocol over about 2000 tokens for under about 500 tokens of work (`delegation-vs-native-heuristics.md:50`) | Fixed entry cost before any debate. At 4 bytes per token (J) about 32k tokens |
| Round 1 | N advocates in parallel, each gets its variant + ALL other variants + diff-analysis (SK:1022-1029, 1049-1055), `max_turns` 5 | Input grows about N x (total size of all variants): quadratic in N at fixed artifact size |
| Round 2 | N advocates, sequential, each reads all Round 1 transcripts (SK:1086-1092) | N more calls and wall-clock grows with N. Skipped at quick |
| Round 2.5 | one fault-finder over the consensus (SK:1111-1116) | One call. Skipped at quick. Observed: 12 `invariant-probe.md` files; of the 9 with a readable depth line, 6 are standard and 3 are deep, none quick (3 have no readable depth line) |
| Round 3 | N sequential, only when `deep` and still under threshold (SK:1361-1364) | Rare. Observed: 3 deep runs of 26 with a readable depth line |
| Scoring | 30-criterion rubric per variant, run twice (forward and reverse), disagreements re-judged (SK:1750-1773) | Grows with N and with disagreement |
| Plan + merge | one plan, one `merge-executor` (`max_turns` 10, SK:1973) | Roughly fixed per run, grows with merge size |
| Failure | one retry, then continue with N-1 (SK:401-404) | Hidden extra cost on flaky agents |
| Budget guard | protocol lowers depth itself (deep to standard, standard to quick) if it judges the run over budget (SK:494, 2241) | A checker may see a lower depth than requested |

**Cost references on disk:** `/sc:troubleshoot` Tier 2 with adversarial is ~30-60k Claude tokens, 8-15 min, versus ~15-30k, 4-7 min without (`sc-troubleshoot-protocol/SKILL.md:656-657`); so adversarial adds roughly 15-30k tokens and 4-8 min on small fix files (subtraction, derived). `/sc:reflect` Tier 2 is "+15-60k tokens, +4-15 min" for the whole tier (`reflect.md:145`). No file gives a standalone figure (U6).

**Observed sizes:** quick, N=2: variants 2.0-9.6 KB total, transcript 1.3-6.5 KB (e.g. `.dev/reviews/story-1-4-approach-debate-20260911/adversarial`). Standard, N=3: variants 38.5-117.8 KB total, transcript 2.4-30.8 KB (e.g. `.dev/brainstorms/20261022T011827Z-orca-upstream-tracking/adversarial`). Deep, N=2: 4.5 KB, 9.6 KB, 52 KB. Depth tally (26 of 32 transcripts have a readable depth line): quick 16, standard 7, deep 3. Largest N seen: 3.

###### 2.4 Settings by number and size of artifacts

Only the first column of evidence is from files; the setting itself is JUDGMENT unless a cite says otherwise.

| N | Combined size | Setting | Evidence |
|---|---|---|---|
| 1 | any | do not run | AD:171 minimum 2 |
| 2 | small (observed quick runs 2-10 KB) | `--depth quick --focus <the one question>` | 16 quick runs observed; `troubleshoot` uses quick when proposals share one diagnosis and differ only in mechanism (`sc-troubleshoot-protocol/SKILL.md:441`) |
| 2 | medium to large (observed 20-100 KB) | `--depth standard` (default) | observed standard runs: top9-issues unified 97 KB, architectural patch 71 KB |
| 2 | decision shapes several stories or has no clean winner | `standard`, `deep` only if standard ends under threshold; add `--interactive` | observed deep: `claudedocs/orca-consolidation` 52 KB, `head-to-head` 9.6 KB |
| 3 | small | `--depth quick`: one round, no rebuttal | observed: `i263/reflect-post` N=3 at 2 KB |
| 3 | medium to large (observed 38-118 KB) | `--depth standard`; this is the `/sc:brainstorm` default shape (3 proposals, opus/sonnet/haiku, `brainstorm.md:48,56`) | 5 brainstorm runs observed at N=3 |
| 4-7 | any | avoid by hand. Quadratic Round 1 input plus N sequential rebuttals. If forced, reduce to the best 3 first | `brainstorm.md:69-70` caps proposals at 2 for quick and 7 for deep ("cost guardrail"); no run above 3 observed |
| 8-10 | any | do not use | allowed by the protocol (SK:561-563); no run observed; never as a way to "get more opinions" |

###### 2.5 When the debate is worth its cost

Run it only when ALL hold; otherwise do not (rules 1-3 are file statements, 4-5 are JUDGMENT):

1. Two or more genuinely competing artifacts exist or will be generated (AD:171; HOW-WE-WORK:152).
2. They disagree on substance. Under 10% difference the protocol skips the debate and scoring and keeps the first file as base (SK:406-409, 944-948, 2164-2171), so you paid the load and diff cost for no decision.
3. The caller's own rule: debate only when there are at least 2 competing strong proposals, never on consensus ("that wastes the debate", `sc-troubleshoot-protocol/SKILL.md:596`).
4. A wrong pick is costly to reverse: it sets an interface other stories build on, a release scope, or an architecture (J).
5. No cheaper tool answers it: one artifact to critique is `/sc:spec-panel`; a vague idea is `/sc:brainstorm` (J).

##### 3. Scope x complexity matrix

**Precondition for every non-SKIP cell:** at least 2 genuinely competing artifacts exist or will be generated (AD:171). With fewer, every cell is SKIP. No file maps adversarial to scope or to the task-builder TCS (`task-builder/SKILL.md` ~2410-2441 drives `/sc:reflect --depth`, not this command). The matrix is therefore JUDGMENT throughout, anchored on the observed runs in 2.3.

**Bands (all thresholds JUDGMENT; anchors are observed sizes):**

- **LOW:** N=2, combined size under about 10 KB (observed quick runs), decision reversible inside one story, no shared interface, files nameable.
- **MEDIUM:** N=2-3, about 20-120 KB (observed standard runs), decision shapes a feature design or a spec, or touches an interface two stories share, a driving spec exists.
- **HIGH:** N=3 or more, or over about 100 KB (largest observed 118 KB), or "must not drift" / infrastructure / secrets / permissions risk (HOW-WE-WORK:18), or a standard debate ended under the convergence bar.

| Scope | LOW | MEDIUM | HIGH |
|---|---|---|---|
| **T** one-off | SKIP (J) | SKIP (J) | N/A (weighing two designs is not a level-2 job, HOW-WE-WORK:22) |
| **B** bug fix | SKIP (J) | SKIP (J): `/sc:troubleshoot` Tier 2 runs the debate itself when it has 2+ competing strong fixes (`sc-troubleshoot-protocol/SKILL.md:425-427`) | OPTIONAL (J): `--compare fix-1.md,fix-2.md --depth standard --focus correctness,risk,test-coverage`, only if troubleshoot did not already debate them (`adversarial_invoked` false, SKILL:525) |
| **S** single story | SKIP (J) | OPTIONAL (J): `--depth quick --focus <the disputed acceptance criterion>`. Precedent: `.dev/reviews/story-1-4-approach-debate-20260911` (N=2, quick, 8.9 KB) | WORTH IT (J): `--depth standard`, N=2 |
| **F** multi-story feature | SKIP (J): a short agreed spec file is enough (HOW-WE-WORK routing row `feature-existing`, :307) | OPTIONAL (J): N=2, `--depth quick`, or `standard` if the drafts exceed about 20 KB | WORTH IT (J): `--depth standard`; `deep` plus `--interactive` only if standard ends under the bar |
| **R** multi-feature release (re-rated, see 7) | SKIP (J) | OPTIONAL (J): `--depth standard` when two release plans or scope cuts compete | WORTH IT (J): `--depth standard --interactive`; normally reached through `/sc:release-split`, which calls it in Mode B with default `opus:architect` + `haiku:analyzer` (`sc-release-split-protocol/refs/adversarial-integration.md`, "Default Agent Configuration") |
| **N** new product | OPTIONAL (J) | OPTIONAL (J): `--depth standard`, N=2-3 competing PRD/TDD/roadmap drafts. No standalone N-scope precedent found on disk; the nearest file, `_bmad-output/planning-artifacts/debate-transcript.md`, is a look-alike (see section 5) | WORTH IT (J): `--depth standard` or `deep`, `--interactive`; for a vague idea start at `/sc:brainstorm`, which runs the debate for you |

**Does the command vary by complexity?** Yes, but along N, size and stakes, not code size. Flags that change with the band: `--depth` (quick to standard to deep), `--interactive` (HIGH only), `--focus` (narrow it as size grows), `--agents` (diversity only when Mode B).

##### 4. Choose this or the neighbour

| Neighbour | Rule by signal | Cite |
|---|---|---|
| `/sc:spec-panel` | One spec to critique: spec-panel (`--mode critique`). Two or more competing drafts to pick or merge: adversarial. After a panel, adversarial may be run on the competing revisions | HOW-WE-WORK:150-152, routing rows `compare-options` / `critique-spec` (:314-315); `adversarial.md:180` |
| `/sc:brainstorm` | No drafts yet, idea vague: brainstorm. It runs adversarial itself in Wave 3 (Mode B, 3 proposals default, 2-7, quick caps at 2). Drafts already exist: `adversarial --compare`. Do not run both on one question | `brainstorm.md:48,69-70,133`; `sc-brainstorm-protocol/SKILL.md:258-281` |
| `/sc:reflect` Tier 2 | Reflect debates its own 2-3 reviewer cards (`--depth standard`, `--focus correctness,coverage,deviation-classification`). Never run adversarial on those cards by hand | `sc-reflect-protocol/SKILL.md:699-714`; `reflect.md:145` |
| `/sc:troubleshoot` Tier 2 | Troubleshoot debates 2+ competing fixes itself (quick if one diagnosis, else standard). Run adversarial yourself only on fix files written by hand | `sc-troubleshoot-protocol/SKILL.md:425-441,596` |
| `/sc:release-split` | Release split question: use release-split (wraps Mode B, 2 agents). Do not call adversarial for it | `sc-release-split-protocol/refs/adversarial-integration.md` |
| `/sc:roadmap` | The `superclaude roadmap run` debate is one LLM step, not this command; skill delegation is "inference-only". A `/sc:roadmap` run is not an adversarial run | `sc-roadmap-protocol/refs/adversarial-integration.md:11,31,82` |
| `/sc:swarm-wizard` / `sc-bare-review` | Other-model reviews can feed a compare, but the named flag `--suspect-source` is not defined by this command (U4) | `sc-bare-review/SKILL.md:3,18,55` |
| `bmad-review-adversarial-general` | BMad lane: reviews ONE artifact cynically and reports findings; adversarial compares 2+ and merges. Different jobs despite the name | repo `.claude/skills/bmad-review-adversarial-general/SKILL.md:3,5-9` |
| `/sc:tasklist` (RETIRED) | Named in `adversarial.md:182` as "Pipeline output as sprint input". Never run it; a merged document goes to `/task-builder` or `/sc:workflow` | brief ruling 3 |
| `/task-builder` (`--spec`) | (J) The merged output can serve as the `--spec` for the next step; requirement-bearing merges carry requirement-level provenance tags (DP:346-358). Adversarial neither validates domain correctness nor executes the result (AD:167-168), so a reader still checks it | `adversarial.md:165-168` |

##### 6. Expected-step rule

- **Never count `/sc:adversarial` as an expected step at any scope or complexity.** It is in none of Ryan's five pipelines and in no HOW-WE-WORK level; its only routing row is the optional `compare-options` (`HOW-WE-WORK.md:314`). Absence is always fine, including at HIGH.
- **Count it only as "done right or half-done":** if an `adversarial/` folder exists, expect `diff-analysis.md`, `debate-transcript.md`, `base-selection.md`, `refactor-plan.md`, `merge-log.md` and a merged output; `invariant-probe.md` too when the transcript says standard or deep. Variants present but no `base-selection.md`, or a contract `status: failed` / `partial` with `unresolved_conflicts` above 0 that nobody addressed, is a finding. A run on near-identical inputs that skipped the debate and scoring (Steps 2-3, then a minimal merge, SK:2164-2171) is legal, so a thin `debate-transcript.md` or a missing `base-selection.md` is explained by a "variants substantially identical" line in `merge-log.md`. An `adversarial/` folder under brainstorm, troubleshoot or reflect belongs to that parent command's own rule, not to this one.

Full file for the citation key, the footprint (section 5), the proposals (section 7) and the unverified items (section 8): [command-nuance/sc-adversarial.md](command-nuance/sc-adversarial.md)

#### 6.3.7 /sc:release-split (Spec)

##### 1. Status and role
- **Does**: "Neutral two-phase release split analysis with adversarial validation and fidelity verification" (CMD:3). Four parts: Socratic discovery via `/sc:brainstorm`, competing proposals via `/sc:adversarial` Mode B, execution via `/sc:design` | `/sc:workflow` | `/sc:tasklist`, fidelity audit (CMD:64; SK:101-107). It never executes the resulting plans or touches git (CMD:122-123).
- **Phase and invocation**: Spec phase, after the PRD/TDD and before the roadmap or tasklist step; optional step 6 of the full-spec route (HW:70-72, HW:309). Standalone-invokable by a user (CMD:19); the protocol skill is loaded by the command only (SK:20). Not retired.
- **Overlaps**: `/sc:brainstorm` and `/sc:adversarial` (it calls both inside Parts 1-2), `/sc:reflect` (both are coverage checks, different inputs), `/roadmap` and `/task-builder` (downstream). **Retired neighbour**: `/sc:tasklist` is offered as a Part 3 option (CMD:136; SK:35, 105, 272). Never take that option. `/sc:task` is not referenced anywhere in the command or protocol (grep).

##### 2. Flags
Every flag is in CMD:50-60 and in the SK argument-hint (SK:5). Short forms (`-o -d -i -a`) exist only in CMD, not in SK.

| Flag | Values | Default | What it changes (cited) | Worth using | Avoid |
|---|---|---|---|---|---|
| `<spec-file-path>` | path to spec, roadmap, tasklist or refactor plan (`.md/.yaml/.yml`) | required | STOP if missing, empty, or <3 extractable requirements; WARN if >500 lines (chunked) or if it looks like a tasklist (asks to confirm) (SK:77-88, 130). | Pass the release-level spec/TDD (HW:72 passes the TDD). | Passing a tasklist: the split comes after the work was already broken into steps. |
| `--output`, `-o` | directory | `<spec-dir>/release-split/` (CMD:53) | Where all artifacts go. Refused before any write if under `.claude/skills/`, `.claude/agents/`, `.claude/commands/` (SK:132). | Point it at the release's own folder, e.g. `.dev/releases/current/<release>/release-split/` (this repo keeps `.dev/releases/current/v2-m2/`). | The three forbidden prefixes. |
| `--depth`, `-d` | `quick` `standard` `deep` | `standard` (CMD:54) | Only documented effect: passed to `/sc:adversarial` in Part 2 (SK:205), where it sets debate rounds 1/2/3 (ADV:334) and `quick` skips Round 2 (ADV:1083). Retry after a Part 2 failure uses `quick` (SK:244). CMD:54 calls it "Analysis depth" but no text applies it to Part 1 (SK:161 passes only `--interactive` to brainstorm) or Part 4. | `deep` for R-HIGH (J); `quick` when the seam is already obvious (J). | Expecting it to deepen the fidelity audit: not stated anywhere. |
| `--interactive`, `-i` | bool | false | Pause after Part 1 (SK:180-182) and Part 2 (SK:256); prompt on NOT VERIFIED (SK:368); the only way to accept convergence 0.50-0.59, otherwise abort (SK:224, 436). Passed on to brainstorm and adversarial (SK:161, 206). | Always at R-MEDIUM and above: the split is a human decision and low convergence aborts without it (J). | Unattended or scheduled runs: it blocks on prompts. |
| `--resume-from` | path to a proposal | none | Skips Parts 1-2; the file is read as the validated proposal and Part 3 starts (SK:120; CMD:34). Only check is that the file exists and is readable (SK:138). | Restart after a crash, or after a human edited `split-proposal-final.md`. | Feeding a hand-written file as "validated": nothing verifies it was adversarially validated (UNVERIFIED gap). |
| `--no-split` | bool | false | Skips Parts 1-2; Part 3 writes a single-release validation spec; Part 4 audits it (SK:122). No split analysis happens at all. | Cheap path when the engineer already decided "one release" and wants a coverage audit. | Treating its output as evidence that a split was considered: no `split-proposal*.md` is produced (SK:50-55 lists them only for the analysed path). |
| `--r1-scope` | `fidelity-schema` `minimal-viable` `custom` | `fidelity-schema` (CMD:58) | Bias for what Release 1 contains (SK:175). Default means "planning fidelity and schema hardening only" (SK:63). `custom` prompts the user for guidance (SK:175). Matters only if a split is proposed. | `minimal-viable` for a feature release (smallest independently valuable subset) (J). | Leaving the default on a release that is not about planning or schemas: it was written for pipeline-planning releases (J, SK:33, 63). `custom` in unattended runs. |
| `--smoke-gate` | `r1` `r2` | `r2` (CMD:59) | Puts the smoke gate in Release 1 or Release 2 (SK:176, 285, 291). "Smoke gate" is not defined in any of the four files read. | `r1` only when a live post-deploy check is itself what R1 must prove (J). | Using it without agreeing what the gate is (UNVERIFIED meaning). |
| `--agents`, `-a` | `model[:persona[:"instruction"]]`, comma list | `opus:architect,sonnet:analyzer` (CMD:60; SK:92) | Number and mix of Part 2 variant generators; 2-10 allowed; unknown model stops the run (SK:134-136); presence selects adversarial Mode B (SK:94). Persona hints in PT:33-38 (`security`, `qa` listed). | Add `sonnet:security` when the split would divide auth, secrets or access changes (PT:37). | Going above the default without a reason: no cost data exists in the files. Conflict: AI:33 lists the default second agent as `haiku:analyzer`. |

**Does not exist** (not found in CMD, SK or the three refs): `--spec` (the artifact is positional), `--split` or any force-split (only `--no-split`), `--yes` or auto-approve of low convergence (needs `--interactive`), `--handoff` (Part 3 picks the command itself, SK:266-275), `--dry-run`, `--mode`, `--resume` (the flag is `--resume-from`).

##### 3. Scope x complexity matrix
**Does the command vary by complexity?** Yes, but only where a release artifact with real seams exists (R, and the top of F and N). At T, B and S it does not vary: there is no release artifact, and the protocol STOPs under 3 extractable requirements (SK:83, 427). Per Ruling 2, a single feature's release is a phase inside S or F, so S never needs this command.

**Band definitions for this command** (no file gives thresholds; anchors are real, the cut-offs are JUDGMENT):

| Band | Signals (all (J) cut-offs) | Anchor |
|---|---|---|
| LOW | 2-3 features, one subsystem, files nameable up front, independent features, release artifact short, no risk class touched, no open decisions. | HW:17, TB:2410-2441 (subsystem = first 2 path segments) |
| MEDIUM | 3+ features across 2+ subsystems, or shared interfaces between features; multi-session; a driving spec/TDD exists; part of it could be proven live before the rest. | HW:18; TB:2410-2441 (TCS 13-34) |
| HIGH | Cross-subsystem plus risk (secrets, permissions, infrastructure, paths), drift-sensitive, release artifact over 500 lines (the protocol's own chunking WARN, SK:87), live validation costly or hard to undo, or any constituent task file at TCS >= 35. | SK:87; TB:2410-2441; HW:22 |

**Matrix** (`(J)` = my judgment, not a file's statement; flags in brackets):

| Scope | LOW | MEDIUM | HIGH |
|---|---|---|---|
| T one-off | SKIP | SKIP | SKIP |
| B bug fix | SKIP | SKIP | SKIP |
| S single story | SKIP | SKIP | SKIP |
| F multi-story feature | SKIP (J) | SKIP (J): phases inside the task file already sequence the work | OPTIONAL (J) [`--interactive --r1-scope minimal-viable`] only when a full spec exists (HW:20, 70) and there is a foundation-versus-application seam (SK:159) |
| R multi-feature release | SKIP (J): ship the features as separate F items | WORTH IT (J) [`--interactive --r1-scope minimal-viable`] | WORTH IT (J) [`--depth deep --interactive --r1-scope minimal-viable`; add `--agents opus:architect,sonnet:analyzer,sonnet:security` if auth/secrets split] |
| N new product | SKIP (J) | OPTIONAL (J) | OPTIONAL (J) [`--interactive`; run on the first release's spec]: `/roadmap` phases are already "independently deployable" (HW:75) |

No cell is REQUIRED: HW calls the step optional (HW:309 step 6, "(optional)"; HW:70), the protocol itself says "do not split" is always valid (SK:31, 61), and no file marks it required. REQUIRED would make a checker flag every legitimate "keep it as one release" decision that skipped the command.

##### 4. Choose this or the neighbour
| Neighbour | Choose `/sc:release-split` when | Choose the neighbour when | Source |
|---|---|---|---|
| `/sc:brainstorm` | The question is "should this release be split, and where". Part 1 already runs brainstorm on that question (SK:149-161). | The idea or requirements are still unclear (HW:151). Do not run brainstorm first on the same split question. | HW:310; SK:149 |
| `/sc:adversarial` | You have one release artifact and want a decision. Part 2 runs adversarial Mode B itself (SK:190). | You already hold two or more competing drafts: `/sc:adversarial --compare a,b` (HW:314). | HW:152, 314 |
| `/sc:spec-panel` | The spec is already agreed and the question is shape. | The spec quality is the question. Release-split does not critique; Part 4 only checks the split outputs against the original (SK:330-363). Run spec-panel first (HW:309 steps 3 and 5). | HW:309 |
| `/sc:reflect --mode pre` | Input is a release spec and output is two specs (spec versus spec fidelity, VP:11-141). | Input is a tasklist or task file and the question is spec coverage (HW:192-194). Neither replaces the other. After a split, `/task-builder --spec <release-1-spec>` produces its own `reflect_pre` (VF:92-95). | VP; HW:192 |
| `/roadmap`, `/task-builder` | Never as a substitute: this command ends at specs and an audit (CMD:123). | Always next. If split: the Release 1 spec replaces the TDD in the roadmap step and Release 2 is not planned until Release 1 is built and validated (HW:72; SK:65, 290). If not split: continue with the original or `release-spec-validated.md`. | HW:72-77 |
| `/sc:design` (Part 3 default) | Part 3 needs release specs: this is the protocol's default (SK:268-275). | `/sc:design` is a single-pass draft of one interface (HW:244; CV:65). For a full release spec, a person or `/tdd` is the better author (J). Protocol fallback is writing the specs inline (SK:430). | SK:268-275; HW:244 |
| `/sc:workflow` (Part 3 option "execution workflow") | Do not pick it for a multi-feature release. | Not eligible as the minimum tasklist step for a multi-story feature (VF:11); use `/task-builder --spec`. | SK:270; VF:11 |
| `/sc:tasklist` (Part 3 option "tasklists") | **Never.** Retired (Ruling 3). The protocol names it at SK:272 and CMD:136, but SK:275 already says not to use it unless the proposal says so. | Tasklist step after the split: `/task-builder` per feature (or `/roadmap`). | SK:272, 275; brief Ruling 3 |
| BMad milestone planning (`bmad-correct-course`, `_bmad-output/planning-artifacts/roadmap.md`) | Task-file lane releases. | BMad lane. This repo shows the milestone route in use: `.dev/releases/current/v2-m3/00-revised-plan.md` (method `bmad-correct-course`) re-scoped a milestone. A milestone plan is a recorded split decision made without this command (J). | observed on disk |
| `/sc:post-release` | Before the tag: decides how to cut the release. | After the tag: documents and e2e-tests what shipped (CV:186). Release 2's gate (R1 "passed real-world validation", SK:290) may use the same evidence (J). | CV:186 |

##### 6. Expected-step rule
**Rule (J except where cited):**
- T, B, S, F-LOW, F-MEDIUM, R-LOW, N-LOW: never expected. Its absence is never a skipped step.
- R-MEDIUM, R-HIGH (and F-HIGH, N-MEDIUM, N-HIGH, weaker): expected is "a recorded split or no-split decision", not necessarily this command. Accept any of: `release-split/` outputs, a milestone or revised-plan document that states the scope cut (this repo's `v2-m3/00-revised-plan.md` is one), or an explicit one-release statement in the release plan. If none exists at R-MEDIUM or above, report it as informational, not as a failed step: no file makes the command required (HW:309 "optional"; SK:31).
- If the command did run: expect `fidelity-audit.md` with a verdict. `NOT VERIFIED` means the split should be revised or abandoned (SK:366; VP:77), so a roadmap or task-builder run on the output without a fix is a finding.

**What "do not split" means for expected steps** (the ask in the lead's message):

| Outcome | Steps of the command itself | Downstream expectation | What the checker must not flag |
|---|---|---|---|
| Ran, result "do not split" (valid at every part, CMD:64; SK:61) | All four parts still happened; five files exist (`split-proposal.md`, `split-proposal-final.md`, `release-spec-validated.md`, `fidelity-audit.md`, report). | The release continues as one release: every feature in it follows its own F pipeline (spec, `/task-builder --spec`, `/task`, commit, `/code-review`, push), then release-level review and `/sc:pr-submit`. "No split" shortens nothing downstream. | Missing `release-1-spec.md` / `release-2-spec.md`; missing `boundary-rationale.md`. |
| Ran, result "split" | Seven files (SK:41-48, 402). | Two sequential releases, each its own R-sized (or smaller) piece of work. Release 1 goes down the normal pipeline using its spec in place of the TDD (HW:72). Release 2 must not have a roadmap or tasklist until Release 1 is built, validated and reviewed (SK:65, 290; VP:108-121). | Release 2 pipeline artifacts absent for days or weeks after Release 1 ships. A checker window must not time out Release 2. |
| Ran with `--no-split` | Parts 3-4 only; no proposal files. | As "do not split", but no split analysis exists. | Missing split-proposal files. Do not count it as evidence a split was considered (J). |
| Did not run | None. | Same as "do not split" if the engineer kept one release; same as "split" if the plan shows two releases (milestones). | Absence (see rule above). |

**Violation the checker can look for**: a Release 2 roadmap, task file or tasklist whose date precedes the Release 1 validation evidence. Detect via Release 2 spec frontmatter `validation-gate` (PT:131) and the dates of Release 1 validation artifacts. How Release 1 validation evidence is recorded is UNVERIFIED (see Section 8).

Full file for the citation key, the footprint (section 5), the proposals (section 7) and the unverified items (section 8): [command-nuance/sc-release-split.md](command-nuance/sc-release-split.md)

#### 6.3.8 /sc:workflow (Tasklist)

##### 1. Status and role

- Does: "Generate a phased implementation plan from a PRD, spec, or feature prompt" (WF:3); writes a new package `.dev/tasks/to-do/TASK-WF-<subject>-<YYYYMMDD>-<HHMMSS>/` and no product code (WF:12, WF:65). Phase: Tasklist; with `--handoff implement` it also starts Implement (WP:64). Standalone-invokable, NOT retired. Backing skill exists: `skills/sc-workflow-protocol/` (SKILL.md plus 6 refs, all read).
- Also called by other skills with fixed flags `--depth standard --handoff none`: `/sc:troubleshoot --fix` plan route (TSK:561; RH:109) and `/sc:reflect --remediate` plan route (RFC:307). An engineer did not necessarily choose such a package.
- Overlaps: `/task-builder` (plan for the same work, heavier), `/sc:implement` (its executor, not an overlap), `bmad-create-story` (BMad lane, CV:118). Retired neighbour: `/sc:tasklist` is named in WF:74, WF:80 and printed by `--handoff tasklist` (OR:8): never follow it (ruling 3).

##### 2. Flags

Defined in WF:35-42 and WP:5 (frontmatter `argument-hint`); enums at IN:54. The command file and the protocol agree on every flag.

| Flag | Values | Default | What it changes | Worth using | Avoid |
|---|---|---|---|---|---|
| `<path>` or `<prompt>` | exactly one: existing file (`@path` unwraps) or leftover text | required (`E-NO-SOURCE`, WF:22; IN:46) | Source is snapshotted byte-exact to `<pkg>/source.md`; the ID subject comes from the file basename or the prompt (IN:5, IN:18-20, IN:37) | File path when a spec, PRD or story file exists: it is the only way to give workflow a spec (no `--spec`, WF:35-40). Prompt when the change is a few named files (TPL:15) | Prompt standing in for a driving spec: the Wave 4 check then only confirms the plan covers the prompt (HW:191) |
| `--strategy` | `systematic` \| `agile` \| `enterprise` | `systematic` (WF:38) | Phase skeleton only (PT:5-9). `enterprise` adds a risk/ops column on every phase plus a rollout phase and, when `--depth` is omitted, sets depth `deep` (WP:28; PT:9) | `systematic` always as default. `agile` (slice 0 spike, then thin increments, PT:7) when the first slice should prove the approach (J). `enterprise` when a rollout phase is wanted (infra, deploy) (J) | `enterprise` as a way to get more review: the review is unchanged, one reviewer per task (QA:11) and Wave 4 gets default reflect flags (WP:56) |
| `--depth` | `quick` \| `standard` \| `deep` | `standard` (WF:39) | Phase cap quick 2-4, standard 4-8, deep 6-12 (WP:38; PT:13). Gate: quick = schema-min, standard/deep = full, which adds "every source requirement is covered by at least one task" (WP:52; QG:24-39). Does NOT change: research (none exists, WP:72), reviewer count (QA:11), or the Wave 4 reflect depth (defaults, WP:56) | `quick` for LOW prompt-sourced work (HW:17, HW:113, HW:305). `standard` when the source is a spec file or the work needs 5-8 phases. `deep` only when more than 8 phases are needed or `enterprise` forces it | `quick` on a spec-file source with several requirements (the coverage line is not in schema-min, QG:26-29 vs QG:39). `deep` as a substitute for task-builder: PT:13 says deep is "split layers, still one session", it adds phases, not research or panels |
| `--handoff` | `none` \| `design` \| `implement` \| `tasklist` | `none` (WF:40) | `none`: prints next-step strings incl. `/sc:implement <pkg>/<id>.md` (OR:13). `design`: prints `/sc:design @<pkg>/<id>.md` (OR:10). `tasklist`: prints `/sc:tasklist --source <roadmap>` (OR:8). `implement`: invokes `sc:implement-protocol` on the plan after the contract is written; a failed handoff makes the contract `partial` (WP:64; OR:7; RC:28) | `none`: the guide's route is read the plan, then run `/sc:implement` (HW:17, HW:114, HW:228). `implement` only when the plan was already approved or the source is trivial (J) | `tasklist`: never, it points at a retired command (ruling 3). `design`: no guide row uses it (HW has no `--handoff` with workflow; its three hits are brainstorm, HW:53, 151, 310). `implement`: skips the human read of the plan, and callers forbid it (TSK:613; RH:109) |
| Banned | `--output`, `--parallel`, `--validate`, `--depth shallow\|normal` | - | `E-LEGACY`, no package, no yaml (WF:42; IN:9-12, IN:49) | - | - |
| Unknown enum value | any value outside the enums above | - | `E-BAD-FLAG`, no package (IN:48) | - | - |

**Does not exist on `/sc:workflow`** (absent from WF:35-40 and WP:5): `--spec` (the source argument is the spec); `--output` (retired, WF:42); `--resume`, `--ledger`, `--skip-final-review` (these belong to `/sc:implement`, IM:57-59); any flag to turn off the Wave 4 reflect (WP:56-58); `--tier`, `--coverage-floor`, `--remediate` (reflect or troubleshoot flags; Wave 4 passes defaults, WP:56); `--fix`, `--type`.

**Three different "quick"s** a checker may meet: workflow `--depth quick` (phase cap and gate, WP:38, WP:52); task-builder's Quick tier (3 researchers, under 5 files, TB:134-136); and TCS-quick (reflect depth, TCS <= 12, TB:2429-2431). They are unrelated settings.

##### 3. Scope x complexity matrix

`/sc:workflow` DOES vary by complexity, but only in plan size and gate strictness (`--depth`), not in rigor: it never gains research, a reviewer panel, or `--spec`. That ceiling is why HIGH belongs to task-builder.

###### 3.1 Bands for this command

No file defines bands for workflow. The on-disk anchors are HW:17 (level 3), HW:18-19 (levels 4-5), HW:22 (hard limit), HW:9 (tie rule) and the TCS signals S1 and S2 (TB:2410-2411). Band edges below are (J) unless a cite is shown.

| Band | One-line definition (all must hold) |
|---|---|
| LOW | Files can be named up front and are few (HW:17 "a few files"), one subsystem, requirement stated in a paragraph or one short story, at most 1-2 sessions (HW:17), no driving spec to trace, no risk class, no shared interface. Counting proxy (J): S1 <= 5 and S2 = 1, using the TCS counting rules (TB:2410-2411); the 5 is borrowed from HW:22's edit limit, which counts edits, not files |
| MEDIUM | Files still nameable, 2 subsystems or about 6-10 files (J), a short spec or story file exists but nothing must be traced requirement by requirement, 2 sessions (tie row, HW:17 vs HW:18, HW:9), stable requirements, no risk class |
| HIGH | ANY of: more than 2 sessions (HW:18); must not drift or a spec must be traced (HW:18, HW:102); files cannot be named or the system is not understood (HW:19; workflow has no discovery, TPL:20, WP:72); risk class: secrets, permissions, user input, file paths, infrastructure (J, built from the security-review trigger list HW:200 and the repo `CLAUDE.md` secrets section); shared interface with sibling stories (J); mid-run amendments expected (HW:102 vs MW:42, HW:117) |

###### 3.2 Matrix

Legend: "REQUIRED (plan)" = HW:22 makes a written plan mandatory above 5 edits or more than one source file, and either plan command satisfies it; the cell names the lighter command that suits the band. Flag sets are in 3.3.

| Scope | LOW | MEDIUM | HIGH |
|---|---|---|---|
| T one-off | SKIP (HW:16, HW:22: plain edit plus related test) | N/A (J): more than 5 edits or more than one source file is not a one-off (HW:22); rate on the S row | N/A (J): not a one-off; rate on S or F |
| B bug fix | SKIP (J): failing test, fix, `/sc:test` (HW:131) | WORTH IT: `--depth quick`, then `/sc:implement` (HW:132; HW:311 route 3b). A plan (either command) is REQUIRED here by HW:22 | SKIP: `/task-builder` (HW:133; HW:311 route 3c; `/sc:troubleshoot --fix --depth deep` also routes to task-builder, TSC:54) |
| S single story | REQUIRED (plan): `--depth quick` | OPTIONAL, either-or with `/task-builder`; HW:9 says pick the heavier when unsure: `--depth standard` | SKIP: `/task-builder` + `/task` (HW:18) |
| F multi-story feature | OPTIONAL (J), only under the 4.2 exception: one plan per story, `--depth quick`. NOT the F minimum (ruling 4; VAL verdict 1) | SKIP (VAL verdict 1) | SKIP |
| R multi-feature release | OPTIONAL (J), same as F-LOW: per-story plans inside a feature that meets 4.2; never the release plan | SKIP (J) | SKIP (J) |
| N new product | SKIP (J): a product small enough for LOW is S-LOW; rate it there | SKIP (HW:20; `/roadmap` makes the tasks, CV:112) | SKIP |

R re-rating: CV:110 rates workflow R = OPTIONAL. Under Ryan's definition (a multi-feature release with its own plan, implementation and push) the release plan is made of F-scope features, so workflow at release level becomes SKIP; the only surviving use is per-story plans inside a feature (R-LOW, J). The old reading behind the R column is stated at CV:139 ("a release assembles and ships work already built").

###### 3.3 Flag set by band (applies to S, B-MEDIUM, F-LOW exception)

| Band | `--depth` | `--strategy` | `--handoff` | Why |
|---|---|---|---|---|
| LOW | `quick` (HW:17, HW:113, HW:305). Use `standard` instead when the source is a spec file with several requirements (J), because only standard/deep check requirement coverage (QG:39) | `systematic` | `none` | 2-4 phases is enough for a few files (PT:13); schema-min gate is cheap; Wave 4 reflect still runs at default depth whatever you pick (WP:56) |
| MEDIUM | `standard` | `systematic`; `agile` (J) if the first slice should prove the approach | `none` | 4-8 phases; full gate including "every source requirement covered" (QG:31-39) |
| HIGH | Not this command. If forced (a caller-built remediation plan, or the operator overrides): `deep` | `enterprise` only if a rollout phase is wanted | `none`, never `implement` | `deep` gives 6-12 phases but the same single reviewer per task (QA:11) and no research or `--spec`; it is not a substitute for task-builder |

###### 3.4 TCS as a switch? No (cross-check)

TCS (`3*S1 + 4*S2 + 2*S3 + 2*S4 + 5*S5 + 4*S6`, TB:2422) picks reflect's depth for task-builder (TB:2402), not workflow-versus-task-builder. Arithmetic from the formula: TCS <= 12 allows at most 2 files in one subsystem (3 files in one subsystem is already 13); 13-34 spans about 3-10 files in one subsystem (TB:2429-2433). HW's "a few files" is therefore already TCS-standard, so TCS cannot be the line between level 3 and level 4. Use S1 and S2 only as a counting aid (JUDGMENT).

###### 3.5 What this repo actually shows (OBS)

Two real workflow packages sit in `.dev/tasks/done/`; none in `to-do/` (`ls`, 2026-10-27). Counts are from `grep` over the plan body outside fenced code, not a run of the TCS rules, and they include paths named in prose, so treat as approximate.

| Package | Tasks / phases / `Depends on` | Distinct paths S1 / subsystems S2 (approx) | `depth` / `strategy` / `handoff_action` | `source_origin`, `reflect_status` |
|---|---|---|---|---|
| `TASK-WF-designSpec-20261022-132541` | 15 / 7 / 13 | about 44 / about 17 | standard / systematic / none | a 68 KB design spec file; `partial` (contract says the plan was amended three times after reflect runs, to v4) |
| `TASK-WF-takeThePlanConfi-20261023-173430` | 8 / 5 / 6 | about 51 / about 21 | standard / systematic / none | `inline`; `skipped` (contract: reflect was interrupted, plan not independently reviewed) |

Reading: the team already uses `/sc:workflow` at sizes the guide assigns to task-builder (HW:18), always at default depth. A checker that applied the LOW/MEDIUM/HIGH edges above to these two would call both HIGH. The first one shows the operator hand-running the spec trace that task-builder automates (two reflect rounds, three FINAL `issues` before `pass`, OBS `progress.md`). Do not flag workflow use on size alone (see 6).

##### 4. Choose this or the neighbour

###### 4.1 `/sc:workflow` or `/task-builder` for ONE story (Ryan's example)

Ordered tests, first hit wins. Cites are the on-disk basis; (J) marks my reading. Differentiators already validated (VAL verdict 1): research, spec trace, review depth; not multi-session resume (both resume, VAL E3).

| # | Test | Result | Basis |
|---|---|---|---|
| 0 | One source file plus its test, 5 edits or fewer, exact change known | Neither: plain edit plus related test, optionally `/sc:implement "<prompt>"` (the one-off minimum is PROPOSED, not confirmed by Ryan) | HW:16, HW:22 |
| 1 | An agreed spec, PRD, TDD or story file must be traced requirement by requirement | `/task-builder --spec <path>`. Workflow has no `--spec`; its Wave 4 check only covers its own source (inline prompt: "checked against your request", HW:191) | HW:18, HW:102; WF:35-40; WP:56; TB:41 |
| 2 | Files cannot be named up front, or how the system works is unknown | `/tech-research` first, then `/task-builder` (level 5). Workflow pushes discovery onto the author and has no research wave | HW:19; TPL:15, TPL:20; WP:72 |
| 3 | More than 2 sessions expected, or "must not drift from what was agreed" | `/task-builder` + `/task` | HW:18, HW:243 |
| 4 | Risk class touched: secrets, permissions, user input, paths, infrastructure | `/task-builder` (J): HW:22 sends "riskier" work to level 4; the risk list is my reading of HW:200 and the repo `CLAUDE.md` secrets section | HW:22 |
| 5 | The plan is likely to be amended mid-run (open questions expected) | `/task-builder`: task files accept new unchecked items; a managed workflow plan freezes at the first task start (`E-PLAN-CHANGED`) | HW:102; HW:117; MW:42 |
| 6 | Story shares an interface with sibling stories | `/task-builder`, one run for the feature (J) | VAL signals table |
| 7 | Exactly 2 sessions, or 2 subsystems, none of tests 1-6 hit | Either command is legal; HW:9 says choose the heavier (`/task-builder`). A checker should accept either (J) | HW:9, HW:17, HW:18 |
| 8 | Few files, clear scope, 1-2 sessions, no spec to trace | `/sc:workflow`: `--depth quick` (LOW) or `standard` (MEDIUM) | HW:17, HW:113 |

Cost side: task-builder has no lightweight mode; even its Quick tier spawns 3 researchers (TB:136) and adds its gates (VAL E2; agent counts there are the VAL author's arithmetic and were not re-derived here). That is the plausible reason the guide keeps level 3 for workflow (the guide does not state it: J).

###### 4.2 Two or more single-story workflow plans instead of ONE task-builder run for a feature

Status: this is a JUDGMENT exception. Ruling 4 says workflow + implement is not eligible as the multi-story F minimum, and VAL line 155 offers the same exception as a suggestion. It needs Ryan's confirmation (U1). It does not make workflow the F minimum; it only says a checker need not flag it.

Acceptable only when ALL hold:

| # | Condition | Basis |
|---|---|---|
| 1 | Every story is individually LOW or MEDIUM and trips none of tests 1-6 in 4.1 | HW:18 |
| 2 | Stories are independent: own goal, different source files, different outputs, no dependency between them. This is task-builder's own test for splitting into tracks | TB:304-309 |
| 3 | No feature-level spec to trace. Each package checks only its own source and a new package is made per run, so no feature-level coverage number exists | WP:56; IN:16; VAL E4 |
| 4 | Each story fits 1-2 sessions and is built and committed on its own | HW:17 (commit-per-story is Ryan's pipeline, brief item 5) |
| 5 | No shared interface: no shared files and no `Depends on` across packages | VAL signals table (J) |
| 6 | Count of plans: no file gives a number. Soft ceiling 5 (J), borrowed from task-builder's maximum of 5 tracks | TB:324 |

If any condition fails: ONE `/task-builder` run for the feature (single track, or up to 5 independent tracks, TB:311-324) with `--spec` when a spec exists.

###### 4.3 Other neighbours

| Neighbour | Decision rule | Basis |
|---|---|---|
| `/sc:implement` without a workflow plan | A prompt, spec, tasklist or informal notes are all valid sources; informal prose becomes one task whose acceptance criteria are the text (IM:24-29; IS:62, IS:88). Use direct for the T-level optional step. Above HW:22's limit, write a plan first. What workflow adds: per-task acceptance criteria, coverage gate at standard/deep, advisory pre-reflect, and the managed package with a mandatory fresh FINAL review plus archive (MW:44-62) instead of the advisory whole-list pass on legacy sources (IS:153) | HW:22 |
| `bmad-create-story` (BMad lane, CV:118 marks it "‡ with `/sc:workflow` for the single-story case") | Pick the lane at the Spec step and stay in it until the PR (CV:223). In the BMad lane the story file replaces the plan; do not also run workflow on it. Its stated goal: a story file giving the dev agent everything needed (`.claude/skills/bmad-create-story/SKILL.md:8`) | CV:223 |
| `/sc:tasklist` (RETIRED) | Never recommend or run. WF:74, WF:80 and OR:8 (`--handoff tasklist`) still name it; treat those lines as stale | ruling 3 |
| `/sc:design` via `--handoff design` | Prints `/sc:design @<pkg>/<id>.md` only (OR:10). No guide row routes plan-to-design; design comes before the plan in every guide workflow (HW:98) | HW:98 |
| Callers (`/sc:troubleshoot --fix`, `/sc:reflect --remediate`) | They build the plan for the engineer with `--depth standard --handoff none` and stop; the engineer then runs `/sc:implement`. For HIGH bug fixes `--fix --depth deep` routes to task-builder instead (TSC:54, TSC:191) | TSK:561, TSK:613; RFC:307 |

##### 6. Expected-step rule

**Count `/sc:workflow` as expected** only when the change crosses HW:22 (more than 5 edits or more than one source file) AND is S-LOW, S-MEDIUM or B-MEDIUM AND no task-builder file covers the same change AND the work is in the task-file lane. A `TASK-WF-*` package OR a task-builder task file satisfies the same "written plan" expectation (HW:22); workflow is never the only acceptable plan.

**Its absence is fine** at T and B-LOW (HW:16, HW:22); at S-HIGH, F, R and N (a task-builder file or `/roadmap` output is the expected plan instead); when a BMad story file exists (CV:223); and when the plan came from a caller. Two further rules: (1) do not flag a `TASK-WF-*` package as the WRONG tool on size alone, because this repo's own packages run well past the LOW/MEDIUM edges (3.5); flag only when a driving spec file exists for the work and the package's `source_origin` is `inline` or is not that spec (spec trace missing, HW:102, HW:191). (2) At F, two or more `TASK-WF-*` packages with disjoint files, `source_origin` pointing at different story sources, and no `Depends on` across them meet the 4.2 exception (J, pending Ryan) and are not a skipped step.

Full file for the citation key, the footprint (section 5), the proposals (section 7) and the unverified items (section 8): [command-nuance/sc-workflow.md](command-nuance/sc-workflow.md)

#### 6.3.9 /sc:roadmap (Tasklist)

##### 1. Status and role

- **What it does**: "Generate roadmap pipeline artifacts from 1-3 specification, TDD, and PRD markdown inputs. Mirrors the CLI `superclaude roadmap run` surface" (CMD:3). Output is `roadmap.md`, `extraction.md`, `test-strategy.md` plus per-step files; it "will not" generate tasklists, execute implementation, or trigger downstream commands (CMD:98; PRO:38, PRO:458-466).
- **Phase and status**: Tasklist phase (planning artifact; CV row 113). STANDALONE-INVOKABLE and NOT retired under Ryan's rulings (only `/sc:task` and `/sc:tasklist` are retired). Its backing skill `sc:roadmap-protocol` is never run directly (PRO:21, PRO:28). Its designed next steps, `/sc:validate-roadmap` and `/sc:tasklist` (CMD:102-103), leave it with no sanctioned downstream in this team's pipeline (see section 4).
- **Overlaps**: `/roadmap` (a different thing with a similar name, section 4), `/task-builder`, `/sc:workflow`, `/sc:release-split` (runs before it), `/sc:validate-roadmap` (runs after it). Observed use in this repo: one full run on 2026-05-17 (section 5).

##### 2. Flags

**The command file and the protocol skill disagree on the flag surface.** CMD is the CLI-mirroring list (CMD:7, CMD:92: "preserve CLI-faithful behavior"); PRO is an older design that still documents flags CMD lists as unsupported (CMD:46-48 vs PRO:67-82). The table follows CMD; every conflict is marked CONFLICT. The "worth using / avoid" columns are JUDGMENT (J) unless a file is cited.

| Flag | Values | Default | What it changes | Worth using when | Avoid when |
|---|---|---|---|---|---|
| `INPUT_FILES...` | 1-3 markdown files; at most one spec, one TDD, one PRD, any order | required | Type auto-detected: PRD scorer first (>=5), then TDD (>=5), else spec (CMD:19, CMD:25; R-SC:9-15). PRD/TDD content enriches extraction (personas, metrics, scope, data models) but not the complexity score (R-EXT:289-307; R-SC:215-219) | Pass all of spec + TDD + PRD that exist: the full-spec route (HW:51-77) produces PRD and TDD, so both are available at N | Passing two files of one kind. A borderline detection score of 3 to 6 prints a warning (R-SC:15): then set `--input-type` |
| `--agents` | `model[:persona]`, comma list | `opus:architect,sonnet:architect` (CMD:27) | Two generator steps, then `diff -> debate -> score -> merge` (PRO:111-137; R-ADV:68-75) | Keep default (J) | A longer list: PRO says 2-10 agents with an orchestrator at 3+ (PRO:84, PRO:248) but CMD and the CLI default to 2. CONFLICT. Observed state file shows a third generator `haiku-architect` that FAILED (repo:`_bmad-output/planning-artifacts/.roadmap-state.json`) |
| `--output PATH` | directory | parent dir of the first input (CMD:19, CMD:27) | Where every artifact lands. CONFLICT: PRO:71 says `.dev/releases/current/<spec-name>/` | Always set it explicitly to a release folder (J), so the checker finds it | Relying on the default: the observed run wrote next to `tdd.md` in `_bmad-output/planning-artifacts/`, matching CMD (repo `.roadmap-state.json` `spec_file`), not PRO |
| `--depth` | `quick`, `standard`, `deep` | `standard` | Debate rounds 1 / 2 / 3, inside the single `debate` step (CMD:28; R-ADV:25-31) | `deep` when HIGH complexity and variants differ (the observed run used `deep`, repo `.roadmap-state.json`) | `deep` on small input: only the debate step gets longer (J) |
| `--resume` | boolean | false | Skip steps whose outputs already pass their gates; re-run from the first failing step (CMD:29). State is `.roadmap-state.json` (R-EXT:307). CONFLICT: PRO has `--resume-from <adversarial dir>` (PRO:81), a different mechanism (R-ADV:81) plus a Serena session-resume prompt (PRO:436-441) | After a halt on the same inputs | After editing the spec: whether the CLI checks the stored `spec_hash` is UNVERIFIED (PRO:439 checks it in skill mode only) |
| `--dry-run` | boolean | false | CMD: print step plan and gate criteria, exit, no subprocesses (CMD:30). PRO: run Waves 0-2 then print a preview (PRO:272). Not identical | First run on any new input (J): free | Never harmful |
| `--model TEXT` | model id | per-agent model (CMD:31) | Overrides the model for all steps | Cost control (J) | Mixed-model debate is the point of the default two agents (J) |
| `--max-turns` | integer | 100 (CMD:32) | Cap per Claude subprocess | Raise if a step times out (J) | - |
| `--debug` | boolean | false | Writes `output_dir/roadmap-debug.log` (CMD:33) | Diagnosing a halt | - |
| `--no-validate` | boolean | false | Skips post-pipeline validation (CMD:34). PRO also writes `validation_status: SKIPPED`, `validation_score: 0.0` (PRO:78, R-VAL:347-352) | Throwaway exploration (J) | R and N: it removes the only gate-checked review of the roadmap (J) |
| `--allow-regeneration` | boolean | false | Allows patches over the diff-size threshold (FR-9); "use with caution" (CMD:35). Threshold value is not stated in any file read | Rare | Default |
| `--no-convergence` | boolean | false | Turns off the spec-fidelity convergence engine; single-shot LLM check instead (CMD:36). PRO:137 says the convergence-aware gate is the fail-closed replacement for the old bypass | Never on R or N (J) | Always (J). Interaction with the gate: UNVERIFIED |
| `--retrospective PATH` | file | none | Prior release-cycle retrospective; a missing file is not an error (CMD:37) | When a prior release has one (J) | - |
| `--input-type` | `auto`, `tdd`, `spec` | `auto` | Forces the type for a single file; PRD stays auto-detected (CMD:38). TDD uses a different extract prompt with 6 extra sections (R-EXT:212-225) | Detection warning shown (R-SC:15) | Multi-file input |
| `--tdd-file PATH` | file | none | Supplementary TDD when the primary is a spec: data models, endpoints, components, test strategy (CMD:39) | Spec primary plus a TDD | Primary is already a TDD (ignored, CMD:39) |
| `--prd-file PATH` | file | none | Supplementary PRD: personas, metrics, compliance, scope; auto-wired from `.roadmap-state.json` on `--resume` (CMD:40) | Spec or TDD primary plus a PRD | - |
| `--no-compress` | boolean | false | Stops lossless markdown compression of the LLM-read inputs; deterministic steps already read originals (CMD:41). Observed run's `roadmap.md` cites `tdd.compressed.md` (repo) | Debugging a fidelity finding (J) | - |
| `--allow-cosmetic-remediation` / `--no-allow-cosmetic-remediation` | toggle | enabled | Auto-fix pure-cosmetic gate failures (11 deterministic transforms C1-C11); semantic failures always halt (CMD:42; R-VAL:104-146) | Default | `--no-...` on high-stakes runs (J) |
| `--strict-no-remediation` | boolean | false | Alias for `--no-allow-cosmetic-remediation` (CMD:43; R-VAL:113) | High-stakes runs | - |
| `--help` | - | - | CLI help (CMD:44) | - | - |

**Flags that do not exist (people may assume them):**

| Assumed flag | Evidence |
|---|---|
| `--specs`, `--template` / `-t`, `--multi-roadmap`, `--interactive` / `-i`, `--compliance` / `-c`, `--persona` / `-p` | CMD:46-48 says unsupported. CONFLICT: PRO:67-82 and PRO:5 (`argument-hint`) still document all of them. Behaviour of an engineer typing one: UNVERIFIED |
| `--validate` / `-v` | In PRO:77 only. Not in CMD's flag table or its unsupported list. Not defined in CMD |
| `--resume-from` | In PRO:81 only. Not in CMD. Not defined in CMD |
| `--spec`, `--tasklist`, any "emit tasklist" flag | None. CMD:98 "Will not: generate tasklists" |
| `--depth` meaning task-builder's TCS bands | `--depth` here is debate rounds only (R-ADV:25-31); TCS is task-builder's (TB:2406-2441) |

##### 3. Scope x complexity matrix

**Does the command vary by complexity?** Its OUTPUT does: the pipeline scores the input and sets milestone count and test interleave from the score (R-SC:98-104). The DECISION TO RUN it barely does: no pipeline Ryan listed names it, and the team guide routes everyone to `/roadmap` "unless your lead says otherwise" (HW:245). So the matrix is nearly flat on purpose.

**Bands for this command** (the only on-disk formula is the command's own input score, computed by the run itself, so an engineer cannot read it before running; the pre-run proxies are JUDGMENT):

| Band | On-disk definition | Pre-run proxy (J) |
|---|---|---|
| LOW | `complexity_score` < 0.4: 3-4 milestones, validation 1 per 3 work milestones (R-SC:100-102) | One spec, one subsystem, under about one session of work per milestone |
| MEDIUM | 0.4 to 0.7: 5-7 milestones, 1 per 2 (R-SC:103) | Several domains or a TDD with data models and APIs; clear dependency order |
| HIGH | above 0.7: 8-12 milestones, 1 per 1 (R-SC:104) | Spec + TDD + PRD, many requirements, deep dependency chains, security or infrastructure risk. Observed: AIDev02 GA scored 0.85 HIGH (repo:`_bmad-output/planning-artifacts/roadmap.md` frontmatter) |

The score formula weights requirement count (/50), dependency depth (/8), domain spread (/5), risk, and spec line count (/1000) (R-SC:76-82). This is NOT task-builder's TCS (TB:2406-2441); TCS does not apply to this command.

| Scope | LOW | MEDIUM | HIGH | Flag set when run |
|---|---|---|---|---|
| T one-off | SKIP | SKIP | SKIP | - |
| B bug fix | SKIP | SKIP | SKIP | - |
| S single story | SKIP | SKIP | SKIP | - |
| F multi-story feature | SKIP | SKIP | SKIP (J) | A feature that scores HIGH is probably an R: re-scope before reaching for this (J) |
| R multi-feature release | SKIP (J) | OPTIONAL (J) | OPTIONAL (J) | `--dry-run` first, then `--output <release dir> --depth standard` (MEDIUM) or `--depth deep` (HIGH); give every spec/TDD/PRD; keep validation on (J) |
| N new product | SKIP (J) | OPTIONAL (J) | OPTIONAL (J) | Same as R. N always has PRD and TDD in hand (HW:51-77), so enrichment inputs exist (J) |

Why OPTIONAL and not WORTH IT at R and N: the output stops at roadmap documents; `/sc:tasklist`, its designed consumer, is retired, so a human must carry the result to `/task-builder` or `/roadmap` (section 4). The deterministic gates, two-agent debate and fail-closed spec-fidelity convergence (PRO:137, PRO:157) are a real advantage over `/roadmap` for the roadmap document only (J).

**R re-rating under the multi-feature-release definition.** CV rated `/sc:roadmap` R = OPTIONAL (CV:113) under a reading where a release "assembles and ships work already built" (CV:139). Under Ryan's definition (full release plan, implementation, push) planning commands do matter at R. Result for this command: R stays OPTIONAL at MEDIUM/HIGH and becomes SKIP at LOW (J). Changed: the reason, not the rating.

##### 4. Choose this or the neighbour

###### 4.1 `/sc:roadmap` versus `/roadmap` (same word, different tools)

`/roadmap` is the task-file skill at `~/.claude/skills/roadmap/SKILL.md`; `/sc:roadmap` is the command at `~/.claude/commands/sc/roadmap.md`. They share a name and nothing else on disk.

| Dimension | `/sc:roadmap` | `/roadmap` | Source |
|---|---|---|---|
| What it is | Slash command that loads `sc:roadmap-protocol`; mirrors the Python CLI `superclaude roadmap run` (14 gated steps) | Skill that is "a pure orchestrator": composes `/task-builder` and `/task` | CMD:92; PRO:111-126; RM:8 |
| Input | 1-3 markdown files: spec, TDD, PRD | Anything: PRD, TDD, free-form prompt, any document | CMD:19; RM:60 |
| Output | `roadmap.md`, `extraction.md`, `test-strategy.md`, plus diff, debate, score, fidelity and remediation files | Roadmap document, one BUILD_REQUEST per phase, one executable MDTM task file per phase (Deep tier) under `.dev/tasks/to-do/TASK-ROADMAP-*/` | PRO:46-50, PRO:113-126; RM:8, RM:130-143 |
| Depth control | `--depth` = debate rounds 1/2/3 only | Quick = roadmap only; Standard = roadmap + BUILD_REQUESTs; Deep = + task files. Default Deep; "if in doubt, pick Deep" | CMD:28; RM:102-114 |
| Quality checks | Per-step deterministic gates, spec-fidelity convergence, optional two-agent debate | Lens-based QA across 4 stages, 44-48 evaluating agents at minimum | R-VAL:7-74; RM:27 |
| Dry run | Prints step plan and gate criteria | Phase plan summary, asks "Proceed? (y/n)" | CMD:30; RM:2614-2644 |
| Next step | `/sc:validate-roadmap`, then the RETIRED `/sc:tasklist` | `/task <phase task file>` per phase | CMD:102-103; RM:8 |
| State file | `.roadmap-state.json` with `spec_file`, `spec_hash`, `agents`, `depth`, `steps{}` (observed) | `.roadmap-state.json` with `input_hash`, `input_paths`, `roadmap_status`, `task_files_created` | repo `.roadmap-state.json`; RM:579 |
| Guide's rule | "Separate release pipeline... Use `/roadmap` unless your lead says otherwise" | The full-spec step 7 | HW:245; HW:74-77 |

**Decision rule by scope.**
- **N (new product)**: `/roadmap`. It is step 7 of the full-spec route and its output is the thing `/task` runs (HW:74-84, routing row `full-spec`, HW:309). `/sc:roadmap` is OPTIONAL and only "if the lead says otherwise" (HW:245).
- **R (multi-feature release)**: `/roadmap` when the release needs executable per-phase task files; `/task-builder` per feature when the features are already specified (J; `/task-builder` is the validated F minimum, VF). `/sc:roadmap` only if the lead asks for the CLI pipeline's adversarial roadmap and accepts a manual hand-off afterwards.
- **F and below**: neither. Use `/task-builder` + `/task` (F) or `/sc:workflow` + `/sc:implement` (S), per the validation files.
- **Trap**: do not run both on the same inputs; the double-dagger in CV:113 marks that as waste, but the two do NOT do the same job (only `/roadmap` ends in runnable files). A checker that sees both should not treat one as a substitute for the other.
- **Stale cross-reference**: `TB:1668` says "`/sc:roadmap` invokes `/task-builder`". Neither CMD nor PRO does; `/roadmap` is the one that does (RM:8, RM:660). Treat the TB line as a mix-up.

###### 4.2 Neighbours in one line each

| Neighbour | Rule |
|---|---|
| `/sc:release-split` | Runs BEFORE any roadmap. If it recommends a split, give the Release 1 spec to the roadmap command, not the whole TDD (HW:70-72). "Do not split" is a normal answer. |
| `/sc:validate-roadmap` | Runs AFTER `/sc:roadmap`, same pipeline only (HW:284; CV:125). `/roadmap` runs its own QA, so never pair it with `/roadmap` output. |
| `/task-builder` (+ `/task`) | The sanctioned tasklist step at F, and per feature inside an R (VF verdict). Whether it accepts a `/sc:roadmap` `roadmap.md` as `--spec` or goal context is UNVERIFIED (spec resolution in VF E4: flag, `@file`, BUILD_REQUEST field). |
| `/sc:workflow` | S-size only. It does not read a roadmap. |

###### 4.3 What the `/sc:tasklist` retirement means for this pipeline

Ruling (brief item 3): `/sc:task` and `/sc:tasklist` are retired and never recommended as an engineer step. No file on disk records this: TLC has no deprecation text (grep for "retire" and "deprecat" in TLC, TLP and the sc-task files found nothing relevant), and `/sc:roadmap` still points at it. The ruling is Ryan's, not a file's.

1. **The designed pipeline loses its terminal step.** PRO:36 says `spec(s) -> sc:roadmap -> roadmap artifacts -> (user triggers) -> future tasklist command -> (user triggers) -> sc:task`. CMD:103 lists `/sc:tasklist` under See Also. PRO:383-385 names the "future tasklist generator" as consumer of `roadmap.md` and `test-strategy.md`; `estimated_phases` is "a hint for future tasklist generator" (R-TPL:394); the validate gate requires a `tasklist_ready` field (R-VAL:32). Those are now dead ends.
2. **`/sc:roadmap` becomes a planning artifact generator only.** It already says so ("The roadmap is a planning artifact", PRO:38; final message "recommend user review", PRO:329). A human must carry its output into `/task-builder` or `/roadmap` input. No file describes that hand-off: UNVERIFIED (see section 8).
3. **The one programmatic `/sc:task` caller dies with it.** TLP Stage 9 invokes `sc:task --compliance strict` through the Skill tool to apply the patch checklist, and the P2 loop re-enters Stage 9 (TLP:1535-1557, TLP:1607). With `/sc:tasklist` retired, no remaining skill read here calls `/sc:task`.
4. **`superclaude sprint run` loses its input.** `/sc:tasklist` produced the Sprint-compatible bundle; "invocation is separate" (TLC:118; TLP:16). Another generator for that bundle: UNVERIFIED.
5. **History is legitimate, not a violation.** The team ran the whole chain once: `repo:.dev/releases/complete/v1.3-2026Upgrade/` holds `tasklist-index.md` (Generator Version "Roadmap->Tasklist Generator v4.0", 8 phases, 192 tasks), `phase-1..8-tasklist.md`, `execution-log.jsonl` with `sprint_start` on 2026-05-17, and was archived 2026-06-24 (commit 730ca38f). The later releases `repo:.dev/releases/current/v2-m2/tasks/T1-*.md` and `v2-m3/BUILD-REQUEST-V2-M3.md` show the BUILD_REQUEST / task-file lane instead. A checker must not flag old tasklist bundles, and must not expect new ones. This resolves CV unverified item U6 (see section 7).

##### 6. Expected-step rule

- **Count it as expected: never**, at any scope or complexity. No pipeline Ryan listed includes it, the guide routes R and N to `/roadmap` (HW:245, HW:309), and a work item that has a task file or `/roadmap` output instead has followed the pipeline. Its absence is always fine, including at R-HIGH and N-HIGH.
- **If it IS present** (a `.roadmap-state.json` with `steps`): do not flag it as wrong, and do not accept it as the tasklist step by itself. Expect (a) the run was not `--no-validate` at R/N (J), (b) the next step is a human hand-off into `/task-builder` or `/roadmap`, never `/sc:tasklist`, and (c) a task file or phase task files exist before implementation starts. Flag only a `/sc:tasklist` or `/sc:task` invocation as a step an engineer ran, and treat old `tasklist-index.md` bundles as legacy.

Full file for the citation key, the footprint (section 5), the proposals (section 7) and the unverified items (section 8): [command-nuance/sc-roadmap.md](command-nuance/sc-roadmap.md)

#### 6.3.10 /sc:spawn (Tasklist)

##### 1. Status and role
- Role (CMD:3, CMD:192-194): "Meta-system task orchestration with intelligent breakdown and delegation", but it STOPS after producing a task hierarchy (Epic, Story, Task, Subtask) and delegates execution to other `/sc:*` commands; it writes no code. Phase served: Tasklist (decompose only). Standalone-invokable: yes; no file marks it retired or deprecated. No backing skill, so it runs from its own file (HW:232).
- Routing: HW lists it only under "Other commands ... no workflow above routes to them" (HW:262, HW:282: "For work that changes code, prefer `/task-builder`"); it is absent from the six levels, workflows 3.1-3.12 and the routing table (HW:301-325; grep for `spawn` in HW returns line 282 only).
- Overlaps: `/task-builder`, `/sc:workflow`, `/roadmap`, `bmad-create-epics-and-stories`. Answer to the focus question: no complexity band is justified by any file (section 3); it is effectively retired from the pipeline (JUDGMENT), though not formally retired by a file. It names the retired `/sc:task` once (CMD:124, section 2).

##### 2. Flags
Only one usage line defines flags (CMD:22): `/sc:spawn [complex-task] [--strategy sequential|parallel|adaptive] [--depth normal|deep]`. Frontmatter has no `argument-hint` (CMD:1-8). There is no backing skill, so no second source.

| Flag | Values | Default | What it changes (cited) | Worth using | Avoid |
|---|---|---|---|---|---|
| `[complex-task]` (positional) | free text | none stated; a bare call is not addressed in the file | The operation to decompose (CMD:22, CMD:27) | Only for the narrow case in section 3 (R/HIGH batch) | Any code-changing job with files nameable up front: use `/task-builder` (HW:282) |
| `--strategy` | `sequential`, `parallel`, `adaptive` | NOT STATED | Names the coordination strategy recorded in the output ("Coordination strategy", CMD:208). Key Patterns defines them as "Sequential (dependency-ordered) -> Parallel (independent) -> Adaptive (dynamic)" (CMD:146). Whether it changes anything beyond a label is UNVERIFIED, because the command also says it does not execute (CMD:192-201) | `adaptive` (JUDGMENT) when a batch mixes dependent and independent items, as in TOP9 spawn-runbook.md section 5 lanes | When all items are one dependency chain: the choice is moot |
| `--depth` | `normal`, `deep` | NOT STATED | Nothing in the file says what it changes. Only evidence is the example `... --strategy adaptive --depth deep` described as "Enterprise-scale operation with sophisticated orchestration" (CMD:163-165). Effect UNVERIFIED | `deep` is only evidenced for "migrate legacy monolith"-class jobs (CMD:163) | Do not confuse with `/sc:workflow --depth quick\|standard\|deep` (workflow.md line 7): value sets differ |

**Does not exist** (people may assume): `--depth quick` or `--depth standard` (value set is `normal|deep` only, CMD:22); `--handoff` (exists on `/sc:workflow`, workflow.md line 7); `--spec` (task-builder only, HW:18); any output-path flag (output path never specified, CMD:203-208); `--resume` or any ledger/progress file; `--dry-run`; any flag that makes it execute tasks. Frontmatter `complexity: high` (CMD:5) is metadata, not a flag.

**Internal contradiction in CMD (affects what a user gets):** Behavioral Flow step 4 says "Orchestrate: Execute tasks using optimal coordination strategy" and step 5 "Monitor: Track progress" (CMD:30-31), and Will says it will "Execute meta-system operations" (CMD:182). The closing section says "STOP AFTER TASK DECOMPOSITION ... Explicitly Will NOT: Execute implementation tasks directly" (CMD:192-201). I treat the closing section as binding (JUDGMENT; later and capitalised, and Will Not at CMD:186-188 does not contradict it). Untested.

**Retired-command reference:** CMD:124 lists, as a case where Rule 2.5 is NOT triggered, "any `/sc:task` invocation without an adversarial-debate stage". That is the only mention of `/sc:task` (grep over CMD for `sc:task\|sc:tasklist`). Its delegation list (CMD:210) names `/sc:implement`, `/sc:design`, `/sc:test`: not retired commands. It never names `/task`, `/task-builder` or `/sc:workflow`.

**Rule 2.5 is inert in this repo:** it fires only for a single Python function in a failing-test cohort of 4 or more (CMD:78-83) and is "NOT triggered" for non-Python targets (CMD:124). `docs/generated/PROJECT_INDEX.md` (Structure) shows a Terraform/shell/workflow repo. Rules 1-3 (absolute paths, tiered evidence standard, count injection; CMD:45-128) are prompt-writing practices, not flags.

##### 3. Scope x complexity matrix
**Does it vary by complexity?** Barely. CMD's triggers are all "complex", "multi-domain", "large-scale" (CMD:14-17) and Will Not says it does not "Replace domain-specific commands for simple operations" (CMD:186). So only the HIGH band is even in its stated domain. CMD names no file counts, no session counts, no thresholds, and no spec input. The only on-disk numeric formula, task-builder's TCS (TB:2402-2433: quick <=12, standard 13-34, deep >=35), scores a finished task file, so it cannot be computed on a spawn input; I use it only as the band vocabulary.

Band definitions for this command (signals from the brief; edges are JUDGMENT, no numbers invented):
- LOW: author can name the files up front, one subsystem, fits one or two sessions (HW:17 level 3 profile; TB:2431 TCS <=12 profile).
- MEDIUM: several files or subsystems, one domain, more than one session, a driving spec exists or is easy to write (HW:18 level 4 profile).
- HIGH: several independent work items or domains, shared files between them that force ordering ("lanes" in TOP9 spawn-runbook.md section 5: PIN, ENV, TEST-57), or risk items (secrets, infrastructure) in some of them.

| Scope | LOW | MEDIUM | HIGH |
|---|---|---|---|
| T one-off | SKIP | SKIP | N/A (J): a one-off that is HIGH is not a one-off; HW:22 hard limit sends it to a written plan |
| B bug fix | SKIP | SKIP | SKIP (bug route 3c is `/task-builder` + `/task`, HW routing row `bug`, HW:311) |
| S single story | SKIP | SKIP | SKIP (levels 3 and 4, HW:17-18) |
| F multi-story feature | SKIP | SKIP | SKIP (`/task-builder` + `/task` is the validated minimum; `validation-feature-task-builder-vs-sc-workflow.md` line 11) |
| R multi-feature release | SKIP | SKIP | OPTIONAL (J), no flag set evidenced; `--strategy adaptive` if used. Sole candidate band, see below |
| N new product | N/A (J): never LOW | SKIP (J): `/roadmap` is REQUIRED here in `command-value-by-phase.md` and produces the same decomposition plus task files | SKIP (J): same reason |

**Why R/HIGH is the only non-SKIP cell, and how weak the evidence is.**
- For: TOP9 is a batch of nine open issues described as a `/sc:spawn` decomposition (Epic, then Story per issue, then Task per chain stage), "stopped before delegation" (`spawn-runbook.md:5`), with cross-issue file lanes (`spawn-runbook.md` section 5) and a per-issue pipeline. Nothing file-backed in the pipeline decomposes a batch of independent items with cross-item ordering: `/task-builder` and `/sc:workflow` take one job, `/roadmap` takes a spec (HW:75). The adversarial review scored that runbook 0.977 against 0.867 for the BMad alternative (`adversarial/top9-recommendation.md:14`).
- Against: (1) it is a batch of issues, not strictly a release as Ryan defines R; (2) the runbook header says "Nothing in this runbook has been executed" (`spawn-runbook.md:7`) and no file shows `/sc:spawn` was actually invoked to make it (section 8, U1); (3) the recommended final chain (`top9-recommendation.md:47-64`) contains no `/sc:spawn` step: it uses `/sc:design`, `/sc:reflect`, `/sc:implement`, `/bmad-code-review`, `/sc:pr-submit`; (4) only the shape and the Prompt Construction Rules were reused (`spawn-runbook.md:53`).
- Conclusion: OPTIONAL at most, and only in R/HIGH. Every other cell is SKIP or N/A. A checker never expects it (section 6).

##### 4. Choose this or the neighbour
Common fact for every row: nothing consumes `/sc:spawn` output. `grep -c "sc:spawn"` returns 0 in `task-builder/SKILL.md`, `task/SKILL.md`, `sc-workflow-protocol/SKILL.md` and `sc-implement-protocol/SKILL.md`; the only `~/.claude` files naming it are CMD and HW:282.

| Neighbour | Decision rule by complexity signal | Cited basis |
|---|---|---|
| `/task-builder` (+ `/task`) | Work changes code and the files can be named, or a spec exists, or it spans more than one session, or must not drift: `/task-builder`. It researches the code, gates quality, writes a checklist file `/task` runs, and traces `--spec` (`reflect_pre`). `/sc:spawn` does none of those: it emits a hierarchy and stops. Choose `/sc:spawn` over it only for a batch of independent items (R/HIGH), and then each item still gets its own `/task-builder` run | HW:18, HW:282, HW:243; CMD:192-208; `validation-feature-task-builder-vs-sc-workflow.md` line 11 |
| `/sc:workflow` (+ `/sc:implement`) | LOW to MEDIUM, a few files, clear scope, one or two sessions: `/sc:workflow --depth quick`. It writes an executable `TASK-WF-*` package that `/sc:implement` resumes; spawn writes no package, no progress file, no resume | HW:17, HW:305; workflow.md lines 7-12 |
| `/roadmap` | New product or major feature from a PRD/TDD: `/roadmap` gives phases plus task files. Spawn's Epic/Story/Task shape (CMD:36) duplicates the phase plan without the task files | HW:20, HW:74-77 |
| `bmad-create-epics-and-stories` (BMad lane) | In the BMad lane never use spawn; the epics step is REQUIRED there and produces the tracked artifact | `command-value-by-phase.md` section 2.2 row |
| `/sc:task`, `/sc:tasklist` (RETIRED, Ryan ruling 3) | Not a choice. Spawn does not call them; it only mentions `/sc:task` in an exclusion clause (CMD:124). Never recommend either as the step spawn delegates to | CMD:124, CMD:210 |

##### 6. Expected-step rule
- **Never count `/sc:spawn` as an expected step, at any scope or complexity.** No file routes to it, no file consumes its output, and it leaves no footprint. Its absence is always fine, including T/B/S/F/R/N at LOW, MEDIUM and HIGH.
- **Its presence is allowed but earns nothing.** Do not flag its use (R/HIGH is OPTIONAL (J); elsewhere it is merely redundant). Do not count it as the tasklist step: it stops after decomposition (CMD:192-201) and writes no executable tasklist, so a feature (F) that went spawn, then implement with no `/task-builder` or `/sc:workflow` plan is still missing its tasklist step.

Full file for the citation key, the footprint (section 5), the proposals (section 7) and the unverified items (section 8): [command-nuance/sc-spawn.md](command-nuance/sc-spawn.md)

#### 6.3.11 /sc:reflect (Review)

##### 1. Status and role
- **What it is** (CMD:3): "Tiered reflection protocol: UC-1 pre-execution coverage/gap audit and UC-2 post-execution deviation audit with heterogeneous reviewer ensemble, blind calibration, and mandatory evidence-validator gate". Phase: Review/Revise/Validate. `--mode pre` checks a plan against a spec; `--mode post` checks built work against a plan. Backing skill EXISTS (`sc-reflect-protocol/SKILL.md`, 2045 lines, plus 12 refs; all read).
- **Standalone and automatic**: NOT retired, invokable by hand (CMD:19). Also called with no engineer action by `/sc:workflow` Wave 4 (WP:56), `/task-builder` A.10.7 PRE gate and its generated POST item (TB:1662, TB:2215), and `/sc:troubleshoot --fix` Wave 6 (CMD:305). `/sc:implement` does NOT call it and forbids it as a per-task gate (IM:130, IS:11, IS:171).
- **Neighbours / retired names**: overlaps `bmad-check-implementation-readiness` (CV:231), `/sc:analyze` (CMD:310), `/sc:implement` FINAL reviewer. The reflect files still name retired `/sc:task` (end-of-task hook, CMD:309, SKILL:54) and `/sc:tasklist` (consumer row, SKILL:1008). Neither is ever an engineer step; ignore those mentions.

##### 2. Flags
Citation key: CMD = command file, SKILL = backing skill, refs/x = file under `sc-reflect-protocol/refs/`, TB = `~/.claude/skills/task-builder/SKILL.md`, HW = `~/.claude/HOW-WE-WORK.md`, WP = `~/.claude/skills/sc-workflow-protocol/SKILL.md`, TK = `~/.claude/skills/task/SKILL.md`, IM/IS = `/sc:implement` command file and skill, CV = `command-value-by-phase.md`.

###### 2a. Flags in the command file's option table (CMD:86-116)

| Flag | Values | Default | What it changes | Worth using | Avoid |
|---|---|---|---|---|---|
| `--mode` | `pre` or `post` | auto-detect, 6 rules, first match wins (SKILL:103-112) | `pre` = UC-1 coverage/gap audit of a plan; `post` = UC-2 deviation audit of built work (CMD:88). A bare call with neither resolves to STOP (SKILL:112) | Always pass it (CMD:88, SKILL:77) | Mixing with legacy `--type/--analyze/--validate` is a STOP (CMD:127) |
| `--type` / `--analyze` / `--validate` | `task` / flag / flag | legacy | `--type task --analyze` = `--mode pre`; `--validate` = `--mode post` (CMD:118-125). Kept for `/sc:troubleshoot` MDTM route only (CMD:305) | Never in new use | - |
| `--spec` | path | none | `pre`: REQUIRED, no spec = STOP (CMD:32). `post`: recommended (CMD:92). Also feeds the reachability gate (SKILL:552-558) | Whenever a spec, PRD or TDD exists | - |
| `--tasklist` | path | none | The plan under audit. Strongly recommended for `post` (CMD:93) | Always when a task file or plan exists. Without it every hunk is "unmapped" so Drift cannot be assigned (J, from S_dev_density definition, SKILL:430) | - |
| `--diff` | git ref, `A..B`, or diff file | none | `post`: required unless `--task-log` (CMD:94). A SINGLE ref is diffed against the working tree, so uncommitted tracked edits are audited; `A..B` sees committed work only (refs/remediation-handoff.md:103, HW:83) | After `/task`: one commit before the work started (HW:83, HW:322) | `..HEAD` range right after `/task`: `/task` does not commit, so it misses the phase (HW:81) |
| `--commit-range` | range | none | Alternative to `--diff` (CMD:95) | - | - |
| `--scope` | path | none | Narrows scope; may flip auto-detect to `post` (CMD:96, SKILL:109) | Only with auto-detect | - |
| `--task-log` | path | none | Alternative `post` input (CMD:97). Plan-route Phase D passes the sibling `progress.md` so files created but untracked are seen (refs/remediation-handoff.md:100-103) | After `/sc:implement` of a remediation plan | - |
| `--depth` | `quick`, `standard`, `deep` | `standard` | `quick` = Tier 1 only; `deep` = force Tier 2 (CMD:98). Both are hard overrides applied BEFORE the rubric (SKILL:410-415). `deep` on under-specified input (1-line spec, empty tasklist) = STOP (CMD:34). With `--remediate`, depth also picks the route (CMD:110) | Pick by TCS band (TB:2429-2433): `quick` only at `pre` | `quick` at `post`: task-builder forbids it, because it disables regression escalation (TB:2440, SKILL:414) |
| `--tier` | `1`, `2`, `auto` | `auto` | Explicit pin that overrides the rubric (CMD:99, SKILL:412-413). `--tier 2` needs at least 2 distinct model classes (SKILL:242-244) | `--tier 1` for a cheap second opinion (CMD:53-54) | Combining with a contradicting `--depth`: precedence not stated (UNVERIFIED) |
| `--reviewers` | 2 or 3 | 3 | Tier 2 reviewer count, clamped by depth and alias count (CMD:100, SKILL:242-244) | Leave default | - |
| `--output` | dir | `.dev/reflect/<mode>-<slug>-<YYYYMMDDHHMMSS>/` | Report location (CMD:101, SKILL:87). STOP if under `.claude/skills`, `agents`, `commands` (CMD:35). STOP `output_input_overlap` if it equals or contains an input (SKILL:209) | A fresh dedicated dir when a previous report is an input | Reusing an earlier report's folder |
| `--coverage-floor` | float | `0.90` | `pre` only. Used in Tier-1 STOP row 1 (SKILL:438, SKILL:448). Does not touch the `S_dev_density > 0.20` escalation (refs/coverage-mapping.md:204-208) | `0.95` for high-safety work (CMD:102) | Expecting it to change `/task-builder`'s pass line: task-builder does not pass it (TB:1671-1676) |
| `--no-mcp` | bool | false | Native tools only, quality degrades (CMD:103) | Debug | Normal runs |
| `--no-evidence-validator` | bool | false | Skips the final citation gate; forces `status: partial` (CMD:104, SKILL:1246) | Debug only | Normal runs |
| `--no-doc-discovery` | bool | false | Skips Wave 1.5 documentation grounding, logged as a gap (CMD:105) | Debug | Normal runs |
| `--no-verify` | bool | false (post) | Turns off the test/lint/type-check "verification triangle"; regression detection falls back to the task-log claim plus a Grounding Gap (CMD:106, SKILL:1109) | Only when tests cannot run in this environment | When tests can run |
| `--rerun-tests` | alias | - | Deprecated alias for verification on (the default) (CMD:106) | Never | - |
| `--no-reachability` | bool | false (post) | Switches off the contracted-sink reachability gate; telemetry only, no Grounding Gap, no `status: partial` (CMD:107, SKILL:552) | Operator rollback only | - |
| `--onboard` | bool | false | One-shot Serena `onboarding` bootstrap when project memory is empty (CMD:108) | Never routinely | - |
| `--with-hierarchy` | bool | false | Opt-in type-hierarchy retrieval; backend-gated (CMD:109) | OO codebases on a capable backend | Others |
| `--remediate` | bool | false | After the audit, offers the Tier 3 chain. Plan route (default): `sc:workflow` builds `.dev/tasks/to-do/<slug>/<slug>.md`, you run `/sc:implement`, then re-run `--mode post`. `--depth deep` adds MDTM route: `task-builder`, you run `/task`. `--depth deep` alone never remediates (CMD:110, refs/remediation-handoff.md:11-19). Reflect never runs the executor (CMD:282, CMD:297). +20-40k Claude tokens, +5-10 min (SKILL:1725) | After a `post` audit with Drift or Regression you want fixed as a plan | `confirm-built` routing row does not use it (HW:322) |
| `--budget-remaining` | int | none | Caller budget hint; `N < 5` STOP, may force Tier 1 (CMD:111, SKILL:320-324) | Sprint callers only | Humans |
| `--no-promote` | bool | false (post) | Suppresses Wave 7, which otherwise MOVES a passing work folder to its done location (CMD:112, SKILL:1538-1563) | ALWAYS when you want a report only. HW:322 lists it as the mandatory flag of `confirm-built` | - |
| `--promote-anyway` | bool | false | Overrides the `status: partial` gate condition only; no effect on `failed` (CMD:113) | Never routinely | Defeats the gate |
| `--promote-dry-run` | bool | false | Prints the `mv` command and 9-condition gate result, no mutation (CMD:114) | To debug why a folder did or did not move | - |
| `--promote-mode` | `auto`, `task`, `sprint-release`, `none` | `auto` | Forces a promotion adapter (CMD:115, refs/promotion-adapters.md:9-12) | Rare | - |
| `--promote-resume` | checkpoint path | none | Resumes an interrupted cross-filesystem move; exclusive with the other promote flags (CMD:116, refs/promotion-adapters.md:33) | After a crash | - |

###### 2b. Flags found in the skill or refs but NOT in the command file's option table

| Flag | Where | What it is | Status |
|---|---|---|---|
| `--no-escalate` | SKILL:416 | Stop at Tier 1 with a warning if confidence < 0.85 | Not in CMD:10 argument-hint. Whether the slash command accepts it: UNVERIFIED |
| `--strategy enterprise` | SKILL:445, SKILL:674 | "set on caller": forces escalation (rubric row 7) and an `opus` reviewer | Same |
| `--executor-model <class>` | SKILL:666, refs/reviewer-spec.md:88 | Removes the executor's model class from the reviewer pool. Used by task-builder CLI mode (TB:2246) | Same |
| `--isolate-reviewers` | SKILL:283 | Wrapper-level snapshot grounding; default OFF | Wrapper CLI; source not read |
| `--fuzzy-ids` | refs/coverage-mapping.md:93 | Optional fuzzy requirement-ID matching | Mentioned only there |
| `--remediate-docs` | SKILL:1085, refs/remediation-handoff.md:265 | Offers a spec-update task for Necessary deviations | Mentioned only there |
| `--recursive`, `--resume-from` | SKILL:1887, SKILL:1497 | Named in prose, never defined | Treat as not existing |
| `superclaude reflect run <task> --depth deep --fix --promote [--base]` | CMD:66-70, TB:2237 | Headless wrapper used by `/task-builder --cli`; exit 0 = pass, 10/11/2 = fail (TB:2237) | Wrapper source not read: UNVERIFIED |
| `superclaude reflect contract-status [--validate] --repo --pr` | CMD:73-82 | Detection-contract readiness; not a reflect audit; writes nothing by default | Out of SDLC scope here |

###### 2c. Does not exist (people may assume)

- `--fix` on `/sc:reflect` itself: only the wrapper CLI has it (CMD:66-70, TB:2237). The slash command uses `--remediate` (CMD:110). `/sc:troubleshoot` is the one that has `--fix`.
- A `--coverage-floor` for `post`: it is `pre` only (SKILL:448).
- `--rollback-last` and `--auto-rollback-on-verify-fail`: deferred to v1.1, not built (SKILL:2027, refs/promotion-adapters.md:128). Rollback is a manual inverse `mv` printed in `promotion-log.yaml` (SKILL:1648).
- Operator-registered promotion adapters: v1.1 only; two adapters are hard-coded (refs/promotion-adapters.md:21).
- `--jury`: eval-runner flag, not a command flag (SKILL:1426).
- `--handoff` / `--output` on workflow: reflect passes `--handoff none` to `sc:workflow` and never `--output` (refs/remediation-handoff.md:74).

##### 3. Scope x complexity matrix
**The command varies by complexity in exactly one way the files define: the depth/tier it runs at.** Whether to run it at all is driven by scope and by whether a spec or a tasklist exists. Two different measures share the words LOW/MEDIUM/HIGH, so a checker must not mix them:

- **Before the run (static, on disk):** the Tasklist Complexity Score (TCS) that `/task-builder` computes and writes to `reflect_pre.tcs` (TB:2410-2441): LOW = TCS 12 or less (`quick`), MEDIUM = 13-34 (`standard`), HIGH = 35 or more (`deep`, Tier 2 forced).
- **During the run (measured by reflect in Wave 1, not available beforehand):** Tier-1 STOP only if `C >= 0.90`, `S_scope <= 5 files`, one domain, `S_dev_density <= 0.05` (SKILL:438); otherwise escalate on `S_domains >= 3`, `S_dev_density > 0.20`, `C < 0.85`, or any Regression candidate (SKILL:440-446).

Band definitions used below (one line each):

- **LOW**: TCS 12 or less (TB:2431); files can be named up front; one subsystem; no driving spec or a short one; no human-decision items; not a refactor.
- **MEDIUM**: TCS 13-34 (TB:2432); up to about 10 files and 2 domains (SKILL:439); a driving spec exists; stories share no interface (J on the last clause).
- **HIGH**: TCS 35 or more (TB:2433), OR a refactor/remediation `type:` (forces `deep`, O2, TB:2438), OR 3 or more domains (SKILL:442), OR spec-declared required capabilities or durable sinks (SKILL:552-558), OR "must not drift" with a spec to trace. Human-decision items floor depth at `standard` (O1, TB:2437).

Only the TCS thresholds, the SKILL rubric thresholds and the O1-O4 overrides are file facts. Every REQUIRED/WORTH IT/OPTIONAL/SKIP rating below is `(J)` unless a file is cited in the same cell.

###### 3a. `--mode pre` (plan against spec)

| Scope | LOW | MEDIUM | HIGH |
|---|---|---|---|
| **T** one-off | N/A: no tasklist, and `--mode pre` STOPs without `--spec` (CMD:32) | N/A | N/A |
| **B** bug fix | SKIP (J) | SKIP (J). A task file built from a troubleshoot report normally records `reflect_pre: skipped` (HW:192) | OPTIONAL (J): only if a real spec exists; `--spec <spec>` or `@<spec>` in the goal makes `/task-builder` run it (TB:41) |
| **S** single story | SKIP: `/sc:workflow` already ran it in Wave 4 (WP:56). Do not rerun (J) | OPTIONAL: manual only if a separate spec exists beyond the request (HW:191): `--mode pre --spec <spec> --tasklist <plan>` | REQUIRED, but automatic: `/task-builder --spec <path>` runs it, depth from TCS (TB:1666-1675). Do not rerun if `reflect_pre.verdict` is `pass` or `fail` (HW:190) |
| **F** multi-story feature | WORTH IT (J), automatic via `--spec`, `--depth quick` | REQUIRED, automatic via `--spec`, `--depth standard` (HW:307 lists `--spec` as the mandatory flag) | REQUIRED, automatic, `--depth deep`, Tier 2 forced; `--coverage-floor 0.95` optional (J) |
| **R** multi-feature release | WORTH IT (J): each phase task file | REQUIRED (J): every phase task file built with `--spec <TDD>` (HW:77) | REQUIRED (J), `deep`; plus run by hand on any hand-written release plan that has a spec |
| **N** new product | WORTH IT (J) | REQUIRED (J), same as R | REQUIRED, `deep`. `/roadmap` composes `/task-builder`, so the gate is automatic when `--spec` is passed (CV:112, HW:77) |

If no spec exists the only legal state is `reflect_pre.verdict: skipped` with `skip_reason: no-spec` (TB:1666). That is a pass for a checker, not a miss.

###### 3b. `--mode post` (built work against plan)

| Scope | LOW | MEDIUM | HIGH |
|---|---|---|---|
| **T** one-off | SKIP (J): no tasklist to audit against; proposed one-off minimum is a plain edit plus the related test (validation-oneoff file, still PROPOSED) | SKIP (J) | SKIP (J) |
| **B** bug fix | SKIP (J) | SKIP (J) | WORTH IT (J), and automatic when the fix went through `/task-builder` (in-task POST item, TB:2215). Manual re-confirm OPTIONAL |
| **S** single story | OPTIONAL. Workflow + `/sc:implement` lane: implement has its own per-task reviewer and FINAL review and does not call reflect (IS:11, IS:171). If run: `--mode post --tasklist <pkg>/<id>.md --diff <commit> --no-promote` (J) | WORTH IT (J): `--no-promote`, `--depth standard` | WORTH IT (J): task-file lane, POST item ran automatically, but it audits a committed range and `/task` does not commit, so re-confirm with one commit and `--no-promote` (HW:81-83, HW:322) |
| **F** multi-story feature | OPTIONAL (J): POST item already ran in each task file | WORTH IT per phase: `--no-promote` (CV:255) | REQUIRED (J) per phase, `--depth deep --no-promote`. Cross-task interaction scan only fires with 3 or more completed tasks (SKILL:338) |
| **R** multi-feature release | WORTH IT (J) | REQUIRED (J): every phase of every feature, `--no-promote` | REQUIRED (J): every phase PLUS one final run over the whole release range with the release plan as `--tasklist`, `--depth deep`. Large diffs switch to per-file classification above 100 hunks and to sampled citation checks above 20 (SKILL:1055, SKILL:1283) |
| **N** new product | REQUIRED: "always run the re-confirm audit" after each phase (HW:81-83); routing note repeats it (HW:309). Band only changes depth | REQUIRED | REQUIRED, `--depth deep` |

POST depth is never `quick` (O4, TB:2440). In `--cli` mode the generated POST item is fixed at `--depth deep` (TB:2441); in skill mode it is the TCS depth floored at `standard` (TB:1081).

###### 3c. `--promote` / `--no-promote` by band

Does not vary by complexity. For hand-run audits the team routing mandates `--no-promote` at every size (HW:322); the default (promote on) moves a passing folder to `.dev/tasks/done/` only when all 9 gate conditions hold, including `tasklist_completion_pct == 1.0`, zero Drift and Regression, zero dropped citations, zero Grounding Gaps, and tasklist `status: done` (SKILL:1545-1563). A higher band makes promotion less likely (more Grounding Gaps and human-decision flags), not more (J). The `/task-builder --cli` POST item passes `--promote` on purpose (TB:2237); the skill-mode item does not pass `--no-promote`, but HW:252 says the folder stays in `to-do/` because the audit runs before the task is marked Done.

##### 4. Choose this or the neighbour
###### 4a. When it runs by itself, and when a person should run it

| Caller | What it runs | Flags it passes | Person should add a manual run when |
|---|---|---|---|
| `/sc:workflow` Wave 4 (WP:56-58) | `--mode pre --spec <pkg>/source.md --tasklist <pkg>/<id>.md`, always, advisory, never edits the plan, never changes workflow status | Defaults only: `--depth standard`, no `--remediate`. Workflow's own `--depth quick` is NOT passed through, so complexity does not scale this call | A separate spec/PRD/TDD exists beyond the request (HW:191). Result lives in `return-contract.yaml` as `reflect_status`, `reflect_report_path` |
| `/task-builder` A.10.7 (TB:1662-1703) | `--mode pre` on the built file. Mandatory when a spec resolves; `skipped` is legal ONLY with no spec (TB:1666, TB:1701). Never auto-loops | `--mode pre --remediate [--spec] --tasklist <file> --depth <TCS depth> --output ${TASK_DIR}reflect/pre/`; no `--executor-model` (TB:1671-1678) | `reflect_pre.verdict` is `skipped`, or the plan is hand-written, AND a spec exists (HW:192-194). Not when verdict is `pass` or `fail` (HW:190) |
| Generated POST item inside every task file (TB:2215-2240, TB:1077) | `--mode post` as the penultimate item, before "Update status to Done". Skill mode: a dedicated subagent runs `Skill(sc-reflect-protocol, "--mode post --remediate --diff {BASE}..HEAD --tasklist {TASK_FILE} [--spec] --depth {DEPTH} --output {OUTPUT_DIR}")` (TB:2223). CLI mode (`/task-builder --cli`, default OFF): `superclaude reflect run {TASK_FILE} --depth deep --fix --promote` (TB:2237) | `{BASE}..HEAD` is a range, so uncommitted phase work is NOT audited (HW:81) | After every `/task` phase of a roadmap or multi-phase feature: single commit, `--no-promote` (HW:83, HW:322). Skill mode is "NOT yet session-validated"; the `--cli` path is the validated one (TB:2371) |
| `/sc:troubleshoot --fix` Wave 6 (CMD:305, troubleshoot.md:54) | Plan route: workflow's own pre, then `--mode post` as the pre-commit gate. `--fix --depth deep`: legacy `--type task --analyze/--validate` | - | After `/sc:implement <tasklist>` completes, run `--mode post` yourself (troubleshoot.md:202) |
| `/sc:implement` (IM:130, IS:11, IS:171) | Does NOT call reflect and refuses it as a per-task gate | - | Post-audit of an implement run is always manual |
| `/roadmap` (CV:112) | Composes `/task-builder`, so PRE/POST items appear in every phase task file | As above | The phase re-confirm in HW:83 |

###### 4b. Choose this or the neighbour

| Neighbour | Decision rule by signal | Cites |
|---|---|---|
| In-task POST item (`reflect_post`) versus manual `--mode post` | Rely on the in-task item when the work is committed and `reflect_post` holds a verdict. Run manually when work is uncommitted at POST time (HW:81), when `reflect_post` is empty or failed, or when the lane is workflow + `/sc:implement` (no automatic post) | HW:81-83, HW:322, IM:130 |
| Workflow Wave 4 pre versus manual `--mode pre` | One signal decides: does a spec exist that is separate from the request? Yes: run manual pre against it. No: nothing to check against; read the plan yourself | HW:191-194 |
| Task-builder PRE versus manual `--mode pre` | `reflect_pre.verdict` is `pass` or `fail`: do not rerun, fix Open Questions instead. `skipped` plus spec on hand: run manual pre, then add missed requirements as new unchecked `- [ ]` items | HW:190-194 |
| `/sc:implement` FINAL review versus `--mode post` | Implement's reviewer is one fresh reviewer against the plan (validation-feature file E1/E2). Reflect post adds a heterogeneous reviewer ensemble and a Drift/Regression taxonomy. At LOW complexity implement's own review is enough (J). At MEDIUM or HIGH with a driving spec, add a manual post (J) | IS:11, SKILL:1051-1210 |
| `bmad-check-implementation-readiness` | Same job (O5), different inputs (plan versus spec, versus PRD+UX+architecture+epics). One per lane: task-file lane uses `--mode pre`; BMad lane uses the BMad skill | CV:231 |
| `/sc:analyze` | No spec and no diff to compare to: use analyze. Reflect needs a spec (pre) or a diff or task log (post) | CMD:310 |
| `/sc:brainstorm` | The spec or tasklist itself is ambiguous: scope it first | CMD:311 |
| `bmad-retrospective`, `bmad-code-review` | Not overlaps: retrospective is lessons after an epic; reflect post is a deviation audit against a plan | CV:243 |
| `/code-review` (built-in) | Relation to reflect is stated in no file read: UNVERIFIED. HW:323 lists it as a separate step after the commit | HW:323 |
| `/sc:adversarial` | Reflect calls it internally in Tier 2 Wave 4; never run it for this purpose | CMD:306, SKILL:699 |
| `/sc:task`, `/sc:tasklist` | RETIRED. Reflect text mentions them (CMD:309, SKILL:54, SKILL:1006-1008). Do not follow | brief ruling 3 |

###### 4c. Choosing `--depth` / `--tier` from complexity signals

| Signal (on disk) | Choose | Basis |
|---|---|---|
| `reflect_pre.tcs` 12 or less, no refactor type | pre `quick` (Tier 1); post `standard` | TB:2431, TB:2440 |
| TCS 13-34, or any human-decision item, or more than 40 checklist items (50 single-track) | `standard` (reflect may escalate) | TB:2432, TB:2437, TB:2439 |
| TCS 35 or more, or `type:` Refactor/Remediation/Code Remediation | `deep`, Tier 2 forced | TB:2433, TB:2438 |
| Diff touches 3 or more domains (code, infra, docs, tests, config), or more than 20 percent of hunks unmapped, or any Regression candidate | Reflect escalates to Tier 2 on its own under `standard` | SKILL:440-444 |
| Cost matters | Tier 1 about 3-8k Claude tokens, 1-3 min; Tier 2 about 35-70k, 8-15 min. These are targets, not measurements | SKILL:1721-1727 |

##### 6. Expected-step rule
- **Count as expected (flag if missing):** (1) any task-builder file built with a spec: `reflect_pre.verdict` of `pass` or `fail` with a real `run_id` and a report on disk, at the depth the TCS dictates (TB:1701); (2) any task-builder file whose `status` is Done: non-empty `reflect_post` (TB:2231; observed files with `reflect_post: ""` exist, so check status first); (3) N (new product): a hand-run `--mode post --no-promote` after each `/task` phase (HW:81-83); (4) R and HIGH F (J): the same per phase, plus a final whole-release run for R.
- **Absence is fine:** T at any band; B at LOW and MEDIUM; `reflect_pre.verdict: skipped` with `skip_reason: no-spec` (TB:1666); the workflow + `/sc:implement` lane has no post-audit requirement (IS:11, IS:171) and its pre-check is automatic and advisory (WP:56-58); manual pre when `reflect_pre` already says `pass` or `fail` (HW:190); LOW and MEDIUM F or S where the in-task POST item already recorded a verdict and nothing is uncommitted (J).

Full file for the citation key, the footprint (section 5), the proposals (section 7) and the unverified items (section 8): [command-nuance/sc-reflect.md](command-nuance/sc-reflect.md)

#### 6.3.12 /sc:validate-roadmap (Review)

##### 1. Status and role

- Does: "Validate roadmap pipeline outputs (roadmap.md, test-strategy.md, extraction.md) produced by `superclaude roadmap run`" (VR:3). Phase: Review/Validate, but only inside the separate `/sc:roadmap` release pipeline (HW:245, HW:284).
- Standalone-invokable, NOT on the retired list in the brief. Its documented next step is `/sc:tasklist` (VR:103, VP:76, VP:969), which is retired: nothing in the supported pipelines consumes its output. It never calls `/sc:task` or `/sc:tasklist` itself (VR:97; VP:1138). The one programmatic `/sc:task` caller is `/sc:tasklist` Stage 9 (TL:1535-1540), outside this command.
- Overlaps: `/sc:reflect --mode pre` (CV:231), `/roadmap` built-in QA (RS:27-34), `/sc:roadmap` built-in validation (RM:34, RM:80), `/sc:tasklist` stages 7-10 (retired). **The command file and its protocol skill describe two different interfaces** (section 2).

##### 2. Flags

Two flag sets exist, one per file. VR:76 says to pass all arguments "verbatim" to the skill, but the skill defines a different set (see the CONTRADICTION list below the tables). Which set is live in a real run: UNVERIFIED.

**A. Command-file surface (VR:23-34), mirrors the CLI `superclaude roadmap validate`**

| Flag | Values | Default | What it changes | Worth using | Avoid |
|---|---|---|---|---|---|
| `OUTPUT_DIR` (positional, required) | dir holding `roadmap.md`, `test-strategy.md`, `extraction.md` | none | Input location; results go to `<OUTPUT_DIR>/validate/` (VR:21, VR:25) | Always (required) | Pointing it at a `/roadmap` or `/sc:workflow` output: those do not produce `test-strategy.md` / `extraction.md` (grep of RS found neither name) |
| `--agents` | `model[:persona]`, comma list | `opus:architect` (VR:31) | N=1: one reflection writes `validation-report.md`; N>=2: N parallel reflections then adversarial merge (VR:38-39) | N>=2 on a MEDIUM/HIGH roadmap, e.g. `opus:architect,haiku:qa` (VR:31, VR:52) (J) | N>=2 on a LOW roadmap: cost with little extra signal (J) |
| `--model` | model name | `""` = each agent's own model (VR:32) | Overrides the model for every validation step | HIGH only, when one strong model should do all steps (VR:55-59 example) (J) | Default runs |
| `--max-turns` | integer | `100` (VR:33) | Turn cap per claude subprocess | Raise (example uses 150, VR:58) if a large roadmap run stops early (J) | Default runs |
| `--debug` | bool | `false` (VR:34) | Debug logging | Only when a run misbehaves | Routine runs |

**B. Protocol-skill surface (VP:3-5, VP:80-109)**

| Flag | Values | Default | What it changes | Worth using | Avoid |
|---|---|---|---|---|---|
| `<roadmap-path>` (required) | roadmap file path | none | Document under test (VP:92) | Always on this surface | n/a |
| `--specs` / `-s` (required) | 1-10 spec paths, comma list | none | Source of truth the roadmap is checked against (VP:93, VP:1085 R4) | Always on this surface; pass every driving spec/TDD/PRD | Omitting it: the skill refuses without specs (VP:82) |
| `--output` / `-o` | dir | `{roadmap-dir}/validation/` (VP:94) | Where `00-` to `05-` artifacts go | Keep default so a checker finds it | Pointing at a tracked path by accident |
| `--depth` / `-d` | `quick` / `standard` / `deep` | `standard` (VP:96) | quick: explicit requirements only, max 6 agents, abbreviated adversarial, no file-path or freshness check; standard: 7-category extraction, max 12 agents, full adversarial; deep: adds one-hop references, max 20 agents, silent-assumption audit, symbol lookups (VP:105-109, VP:318-322, VP:620) | quick for LOW, standard for MEDIUM, deep for HIGH (J: no file ties depth to size) | deep on LOW: pure cost |
| `--max-agents` | 4-20 | `20` (VP:97) | Cap on parallel agents; domain clusters capped at `max-agents - 4` (VP:312) | Lower it to bound cost on LOW/MEDIUM (J) | Below 4 (out of stated range) |
| `--exclude` / `-x` | comma list of domains | none | Table entry only (VP:95); no step in the body uses it. Effect: UNVERIFIED | Not recommended until its behaviour is confirmed | Relying on it to scope a run |
| `--skip-adversarial` | bool | `false` (VP:98) | Skips Phase 4 (VP:744) | LOW roadmaps, when a cheap pass is enough (J) | HIGH: Phase 4 is the check on false COVERED claims (VP:752-760) |
| `--skip-remediation` | bool | `false` (VP:99) | Skips Phase 5 remediation plan (VP:850) | When only a verdict is wanted | When the verdict is not GO and someone must fix the roadmap |
| `--report` / `-r` | path | none | Also writes the summary there (VP:100, VP:974) | When a human wants the summary outside the output dir | Writing into a tracked path without reading it |
| `--prior-taxonomy` | path to a prior `00-domain-taxonomy.md` | none | Seeds domain clustering for repeat runs (VP:101, VP:304) | Re-validating the same roadmap after fixes (J) | First run |

**CONTRADICTION list** (both versions recorded; neither silently picked)

| # | VR says | VP says |
|---|---|---|
| C1 | Invoke as `<OUTPUT_DIR>` (VR:18) | Invoke as `<roadmap-path> --specs <spec...>`, specs required (VP:84, VP:93) |
| C2 | Writes `<OUTPUT_DIR>/validate/reflect-<agent-id>.md` + `validation-report.md` (VR:62-69) | Writes `{roadmap-dir}/validation/00-...05-validation-summary.md` (VP:94, VP:953-966) |
| C3 | "Will Not ... Spawn additional sub-agents beyond the `--agents` list" (VR:98) | Dispatches domain + 4 cross-cutting agents, all `sonnet`, up to 20 (VP:97, VP:365, VP:496) |
| C4 | "Mirrors the CLI `roadmap validate` surface" (VR:3, VR:81) | "NOT a behavioural mirror" of the CLI (VP:20) |
| C5 | Exit 0 always; findings as blocking/warning/info counts (VR:43) | Verdict GO / CONDITIONAL_GO / NO_GO from a fixed matrix (VP:686-693) |
| C6 | Flags `--agents`, `--model`, `--max-turns`, `--debug` (VR:31-34) | None of the four appear anywhere in VP (grep: zero hits) |
| C7 | n/a | Depth table promises a freshness-check column and abbreviated adversarial at `quick` (VP:105-109); Step 3.5 has no depth gate (VP:582-590) and Phase 4 is skipped only by `--skip-adversarial` (VP:744) |

**Does not exist** (flags people may assume): `--depth`, `--specs`, `--output` on the command-file surface (they live only in the skill); `--no-validate`, `--resume`, `--dry-run`, `--input-type` (these belong to `/sc:roadmap`, RM:29-38); `--fix` / auto-remediation (the skill only plans remediation and never edits the roadmap, VP:1134-1140, VR:93-96); `--no-reflect` (that is `/sc:tasklist`, `commands/sc/tasklist.md:23,39`).

##### 3. Scope x complexity matrix

**Does the command vary by complexity?** Yes, but only in how heavy the run is (agent count on the command-file surface, `--depth` on the skill surface), not in whether it applies. It does not vary by scope in any file: the command exists only for `/sc:roadmap` output (VR:3, VR:21), and that exists only at release or new-product size. No file ties complexity to a depth or agent count, so every band below is JUDGMENT; the only file-stated numbers are the skill's size cut-offs: under 10 requirements is "very small", over 500 is "very large" (VP:1114-1115), and domain clusters split above 20 requirements (VP:310). TCS (TB:2410-2441) scores task files for reflect depth and is not defined for roadmaps.

| Band | Signals (file-sourced where cited; band edges are J) |
|---|---|
| LOW | One source doc, under 10 extractable requirements (VP:1115) or a single milestone; no irreversible or infrastructure gates (VP:385). Run: command `--agents opus:architect` (default) / skill `--depth quick`. |
| MEDIUM | 10 to 500 requirements; two or more milestones; spec plus TDD or PRD, so the 9 input-aware dimensions apply (VR:41, VP:38-39). The one observed run (about 146 input entities, 5 milestones, about 151 roadmap rows; `REPO/_bmad-output/planning-artifacts/validate/validation-report.md`, Proportionality finding) sits here by count. Run: `--agents opus:architect,haiku:qa` (VR:52) / `--depth standard`. |
| HIGH | Over 500 requirements (VP:1114), or the roadmap sequences irreversible or infrastructure steps (VP:385), or several sources that may conflict (VP:1086). Run: three agents, `--model opus`, `--max-turns 150` (VR:55-59) / `--depth deep` with every driving doc in `--specs`. |

| Scope | LOW | MEDIUM | HIGH |
|---|---|---|---|
| T one-off | N/A (no roadmap exists) | N/A | N/A |
| B bug fix | N/A (bug route is `/sc:troubleshoot`, HW:311) | N/A | N/A |
| S single story | SKIP (J) | SKIP (J) | SKIP (J) |
| F multi-story feature | SKIP (J) | SKIP (J) | SKIP (J) |
| R multi-feature release | SKIP (J) | OPTIONAL (J) | WORTH IT (J) |
| N new product | N/A (J) | OPTIONAL (J) | WORTH IT (J) |

Rules that apply to every cell:
- Cells assume a `/sc:roadmap` (or `superclaude roadmap run`) output directory exists. If the roadmap came from `/roadmap` or from `bmad-create-epics-and-stories`, the command has no valid input and the cell is N/A for the command and SKIP for a checker.
- S and F are SKIP because their tasklist step is `/sc:workflow` or `/task-builder` (brief, ruling 5), and the spec check there is `--spec` / `reflect_pre` (validation-feature file, E4) or `/sc:reflect --mode pre` (HW:190-194), not this command.
- R and N use `/roadmap` as the default roadmap tool (HW:245; CV:112), and `/roadmap` runs its own 4-stage QA with coverage validation (RS:27-34). The R and N cells above apply only to the rarer `/sc:roadmap` lane.
- **R re-rating** (brief, ruling 2): CV:125 rates R flat OPTIONAL. Under "multi-feature release" a roadmap-level plan is the central artifact, so a coverage gap is paid for once per feature. Proposed: R splits into SKIP / OPTIONAL / WORTH IT by band (J). The base (MEDIUM) stays OPTIONAL, because `/sc:roadmap` already validates by default (RM:34, RM:80) and the next documented step, `/sc:tasklist`, is retired. N also splits the same way (CV:125 had flat OPTIONAL).

##### 4. Choose this or the neighbour

The deciding signal is the kind of artifact being checked, then its size. This command accepts one artifact type: a `/sc:roadmap` output directory (VR:21).

| Neighbour | Rule | Cited |
|---|---|---|
| `/sc:reflect --mode pre` | Checking a task file or a `/sc:workflow` plan against a spec: use reflect (`reflect_pre` already runs inside `/task-builder --spec`; run reflect by hand only when it says `skipped` or the plan is hand-written). Checking a `/sc:roadmap` directory: this command. The skill says a tasklist-shaped roadmap is still validated (VP:1117), but the command file's three-file input rule (VR:25) would reject it: do not use this command for plans. | HW:190-194; VR:25; VP:1117; validation-feature file E4 |
| `/roadmap` built-in QA | If the roadmap came from `/roadmap`, do not run this command: it has no `test-strategy.md` / `extraction.md` (grep of RS: no hit) and `/roadmap` already runs 4 QA stages (document, coverage, BUILD_REQUEST, cross-task). | RS:27-34; HW:245 |
| `/sc:roadmap` own validation | `/sc:roadmap` validates after generation unless `--no-validate` (RM:34, RM:80). Run this command after it only when (a) `--no-validate` was used, (b) the roadmap was hand-edited after a failed report, or (c) the roadmap is in the HIGH band and the deeper multi-phase protocol (coverage matrix, gap registry, adversarial pass; VP:20-25) is wanted. Otherwise the pipeline's own `validate/validation-report.md` is the check. | RM:34; RM:80; VP:20-25 |
| `/sc:tasklist` (retired) | Do not follow the "next step" text. VP:969-971 says "Proceed to tasklist generation with `/sc:tasklist`"; VR:103 lists it under See Also. Ignore both. `/sc:tasklist` stages 7-10 validate a tasklist against a roadmap, the opposite direction (TL:3, TL:16). | VP:969-971; VR:103; TL:3 |
| `bmad-check-implementation-readiness` | BMad-lane analogue for PRD, UX, architecture, epics. No overlap in inputs: BMad lane never creates a `/sc:roadmap` directory. | CV:126 |
| `/sc:spec-panel` | Critiques the spec, not the roadmap. Run it before the roadmap exists; this command assumes the spec is the source of truth (VP:1085). | CV:66; VP:1085 |
| `/sc:adversarial` | Embedded: with N>=2 agents the command does an adversarial merge itself (VR:39). Do not stack `/sc:adversarial` on top. | VR:39 |

##### 6. Expected-step rule

- **Never expected** at T, B, S, F, or at R and N when the roadmap came from `/roadmap` or the BMad lane. Its absence is fine, and its presence there is also fine (do not flag either way).
- **Soft-expected** only at R or N when a `/sc:roadmap` output directory (`roadmap.md`, `test-strategy.md`, `extraction.md`, `.roadmap-state.json`) is in the branch AND no `validate/validation-report.md` sits beside it AND the work proceeds to implementation (J). If `validate/validation-report.md` exists, the step is satisfied, whether `/sc:roadmap` produced it or this command did. Never require a following `/sc:tasklist`: it is retired.

Full file for the citation key, the footprint (section 5), the proposals (section 7) and the unverified items (section 8): [command-nuance/sc-validate-roadmap.md](command-nuance/sc-validate-roadmap.md)

#### 6.3.13 /sc:swarm-wizard (Review)

##### 1. Status and role
- **What it does**: "Plain-language interactive guide to the superclaude swarm CLI" that interviews, picks a lens, proves it with a stub dry run, then launches a real multi-model review only after a yes (CMD:3, SKILL:121-153). It reviews ONE target file or path per run (INT:27-31). Phase: Review (CVP 2.3 row); two lenses touch other phases (`troubleshoot-hypothesis` = Bug fix, `spec-completeness` = Spec review: CC:46,48).
- **Standalone-invokable, not retired.** User-facing command (CMD:17-22). Lists no dependency on `/sc:task` or `/sc:tasklist`: neither name appears in any file read (checked by reading all six files in full).
- **Overlaps**: `/code-review` (HWW:199), `/sc:auggie-review`, `bmad-code-review`, `bmad-review-edge-case-hunter` (same job as the `edge-case-hunt` lens), `/sc:troubleshoot`, `/sc:reflect`, `/sc:spec-panel`. Downstream consumer, not rival: `/sc:adversarial` (CC:43; BARE:17-19).

##### 2. Flags
###### 2a. Flags on `/sc:swarm-wizard` itself (CMD:47-55; identical `argument-hint` at SKILL:8)

| Flag | Values | Default | What it changes | Worth using when | Avoid when |
|---|---|---|---|---|---|
| `--goal <text>` | free text | none; asked in interview (CMD:28, INT:10-25) | Pre-seeds the goal so Q1 is skipped; a clear match is confirmed, not menu-picked (INT:23-25) | You already know what to ask the other models | Goal fits two lenses (wizard will ask anyway: SKILL:95-96) |
| `--target <path>` | file or path | none; asked (CMD:29) | Pre-seeds the review target; must exist and hold >=50 non-whitespace bytes or the wizard STOPs (SKILL:49-50, CC:77-78) | Always, when the file is known | Tiny/empty file; a whole feature (one target per run; default cap 4000 lines, `--target-line-cap`, CC:24) |
| `--output <dir>` | directory | `.dev/swarm-runs/<lens>-<ts>/`, `-N` appended if it exists, never overwrites (CMD:51, SKILL:114-116) | Where all run artifacts land | You want the evidence under a task-file or story folder | Reusing the dry-run folder for the real run (real run needs a fresh dir: RMS:33) |
| `--real` | on/off | off (CMD:52) | Signals intent to use real models; a stub dry run STILL runs first (CMD:52, SKILL:126-128). Real run needs go-ahead + green dry run + env contract (SKILL:141-144) | The second-family opinion is worth the cost (section 3) | Proxy not configured: wizard downgrades to a stub run (SKILL:59-60, 193) |
| `--detached` | on/off | off (CMD:53) | Prefers a background tmux run (`swarm-<job_id>`) over a live dashboard (CMD:53, CC:28). Needs tmux on PATH and not nested in tmux (CC:86) | Long real run you will come back to | Already inside tmux; mutually exclusive with `--tui` (CC:83,27-28) |
| `--advanced` | on/off | off (CMD:54) | Unlocks custom-lens / hand-authored JobSpec branch with trust-boundary warnings; `custom-py:` recipes run arbitrary host code (SKILL:103-107, CC:55-57) | Maintainer testing a custom prompt dir | Normal reviews: the 7 shipped lenses cover them |
| `--yes` | on/off | off (CMD:55) | Asks only goal + target, defaults the rest (INT:4, SKILL:85-86) | Repeat runs by someone who knows the lenses | Whether `--yes` also skips the real-run go-ahead is not stated: UNVERIFIED (U9); assume it does not (CMD:87) |

No positional argument. Pre-seed flags are passed to the skill as context (CMD:70-73).

###### 2b. Settings the wizard chooses and passes to `uv run superclaude swarm run` (not wizard flags; CC:17-32)

| Setting | Values | Default | What it changes | Notes |
|---|---|---|---|---|
| `--lens` | `bare-review`, `refactor-find`, `edge-case-hunt`, `spec-completeness`, `feasibility-probe`, `troubleshoot-hypothesis`, `doc-completeness` | from interview Q1 (INT:10-21) | Which review prompt/recipe runs; `custom` rejected as a shortcut (CC:41-55) | Only `bare-review` is `stable`; the other six are `experimental` (CC:51) |
| `--transport` | `stub`, `openai_compat` | `stub` on the lens path (CC:22) | `stub` = placeholder text, no network; `openai_compat` = real models via proxy (CC:61-66) | Dry run is always `stub` (SKILL:126) |
| `--reviewers` | 2-4 | 3; 4 for `edge-case-hunt` and `troubleshoot-hypothesis` (CC:23) | Number of independent reviewers; outside range = exit 2 | "More = broader but slower" (INT:43-46) |
| `--target-line-cap` | integer | 4000 (CC:24) | Truncation of the target | Rarely changed |
| `--timeout-sec` | integer | 180 per worker (CC:25) | Per-reviewer time limit | |
| `--label` | text | `swarm-run-lens-<lens>` (CC:26) | Cosmetic; tmux-legal when detached | |
| `--tui` | on/off | off | Live dashboard; real TTY + `--output` only; exclusive with `--detached` and `--resume` (CC:27) | Not for a wizard tailing in a non-TTY (RMS:57-58) |
| `--resume <JOB_ID>` | job id | none | Re-runs only failed workers from `manifest.json` (CC:29, RMS:108-112) | After `partial`/`failed` (SKILL:196) |
| `--force-relens`, `--stdin`, `--auto-inject-guard`, `scaffold`, `validate` | | | In the CLI contract (CC:30-37) but the wizard flow uses them only on the `--advanced` branch (SKILL:103-107) or not at all: `--force-relens`, `--stdin`, `--auto-inject-guard` are not mentioned in SKILL, INT, or RMS | |

###### 2c. Does not exist (people may assume)

- `--depth` on the wizard: absent from CMD and SKILL. Depth equivalent is the lens choice plus `--reviewers` 2-4.
- A flag to skip the dry run: none. The stub dry run is a mandatory gate (SKILL:121-128, CMD:87-88).
- `--lens`, `--reviewers`, `--transport` as wizard flags: not in CMD:47-55; the wizard sets them from the interview.
- `--custom-prompt-dir` on `swarm run`: stale doc claim; it is a JobSpec field (CC:117). `--recipe`: no such flag, recipe follows the lens (CC:51).
- Waiting on `done.json` for an inline run: never written there (CC:93-95, 118).
- `/sc:bare-review`: no command exists; `sc-bare-review` is delegate-only (BARE:24).

##### 3. Scope x complexity matrix
**Does the command vary by complexity?** Its mechanics do not (same interview, same mandatory dry run, `--reviewers` 2-4 is the only size knob: CC:23). What varies is whether running it is worth the cost. No file gives a threshold for that: HWW lists it once as a choice ("You want reviewers from other AI model families", HWW:154), never inside a level, a numbered workflow step, or 3.11 review/PR steps (HWW:196-199). CVP O8 calls it "extra assurance" (CVP:234). Every cell below is therefore (J) except where a file is cited.

**What a real run costs (all that files state)**: real models via a proxy, "may take a bit" (SKILL:144); up to 180 s per reviewer (CC:25); 2-4 reviewers (CC:23); ONE file per run, truncated at 4000 lines by default (CC:24). A dry run is "free, instant, no setup" (INT:37). No token or money figure appears anywhere (U7). The output is not a verdict: findings are unscored, undeduped, unordered and, for `bare-review`, tagged `suspect: true` and meant for `/sc:adversarial --suspect-source` (CC:51-53; BARE:17-19,54-55). A run is only worth it if someone then triages that output.

**Band definitions for this command (J; signals are the brief's list)**
- LOW: author can name the one file; no secrets, permissions, user input, paths or infrastructure in it; no drift sensitivity. (Analogue only: task-builder TCS <=12 = quick, `task-builder/SKILL.md` around 2406-2441.)
- MEDIUM: 2-5 files in one subsystem, or the file handles user input or file paths, but no secrets/permissions/infrastructure; a driving spec may exist.
- HIGH: the file touches secrets, permissions, auth, infrastructure/deploy scripts or data-loss paths; or "must not drift"; or shared interfaces between stories; or a root cause that `/sc:troubleshoot` could not confirm. (Analogue: task-builder forces `--depth deep` for refactor/remediation `type:` and TCS >=35: same file, O2 and threshold table.)

| Scope | LOW | MEDIUM | HIGH |
|---|---|---|---|
| T one-off | SKIP (J) | SKIP (J) | OPTIONAL (J): `bare-review`, 3 reviewers, on the one risky file |
| B bug fix | SKIP (J) | SKIP (J) | OPTIONAL (J): `troubleshoot-hypothesis` (4 reviewers) only after `/sc:troubleshoot` reports "cause not confirmed" and `--depth deep` did not settle it (HWW:134); experimental lens (CC:51) |
| S single story | SKIP (J) | SKIP (J) | OPTIONAL (J): `bare-review` on the single riskiest file |
| F multi-story feature | SKIP (J) | OPTIONAL (J): `bare-review` on the one or two files with the most risk | WORTH IT (J): one run per high-risk file (not per feature); `edge-case-hunt` (4) where input handling is the risk. Flags: `--real --reviewers 3` |
| R multi-feature release | SKIP (J) | OPTIONAL (J) | WORTH IT (J): before the push, on release-critical files (deploy/install scripts, migrations, permission or secret handling). Flags: `--real`; add `--detached` if several files are queued |
| N new product | N/A (J): a new product has no LOW band | OPTIONAL (J) | WORTH IT (J) on security-foundational files only (auth, payments, data model). `spec-completeness` on a PRD/TDD is OPTIONAL (J): `/sc:spec-panel` is the guide's spec reviewer (HWW:153) |

Every cell assumes real models are reachable. If the proxy is not configured, the wizard only produces a stub run (HWW:154, SKILL:59-60), which is not a cross-model review.

##### 4. Choose this or the neighbour
| Neighbour | Decision rule by complexity signal | Cited basis |
|---|---|---|
| `/code-review` (built-in bug review) | Default for every scope: HWW step "Bug review. `/code-review`" (HWW:199) and "One bug review plus the PR monitor is enough" (CVP:234). Add swarm only on top, never instead, and only at HIGH (secrets, permissions, infrastructure, data loss) on a named file. | HWW:199; CVP:234 |
| `/sc:auggie-review` | Auggie gives a whole-branch view (CVP:234); swarm sees one file. Use auggie for breadth across a branch, swarm for a second model family on one risky file. | CVP:234; CC:24 |
| `bmad-code-review` | BMad-lane equivalent of `/code-review` (CVP:234). Same rule: swarm is extra assurance on top. | CVP:234 |
| `bmad-review-edge-case-hunter` | Same job as swarm's `edge-case-hunt` lens. Use the BMad skill by default (no proxy needed); use the swarm lens only when you specifically want other model families to probe input/state boundaries on a HIGH-risk file. | CVP:128; CC:47 |
| `/sc:adversarial` | Not an alternative: it is the next step. `bare-review` and `edge-case-hunt` hand off to it (CC:43,45; BARE:55). Rule: if you ran swarm `bare-review`, running `/sc:adversarial --suspect-source` (or reading `merged.md` yourself) is what turns raw suspect findings into something to act on. A swarm run nobody triages has no value. | CC:51-53 |
| `/sc:troubleshoot` | Always first for a bug (HWW:124-126). `/sc:troubleshoot` already runs its own parallel hypothesis agents on low confidence (HWW:125). Swarm `troubleshoot-hypothesis` only adds other model families when the cause stays unconfirmed. | HWW:125,134; CC:48 |
| `/sc:reflect`, `/sc:spec-panel` | For spec or plan checks these are the routed tools (HWW:153,190-194). Swarm `spec-completeness` hands off to `/sc:reflect` (CC:46); it does not replace the spec trace (`--spec`, `reflect_pre`). | HWW:153,194; CC:46 |
| `/sc:research` / `/tech-research` | Lens `feasibility-probe` hands off to `/sc:research` (CC:47) but HWW routes feasibility of OUR system to `/tech-research` (HWW:142). Prefer `/tech-research`. | HWW:142; CC:47 |
| `/sc:code-review --apply` (named hand-off of `refactor-find`) | No `code-review.md` exists under `~/.claude/commands/sc/` (directory listing); the session skill list shows `code-review` with `--comment`, `--fix`, `--max-findings`, no `--apply`. Do not rely on the `refactor-find` hand-off; use `/sc:cleanup` or `/sc:improve` per HWW 3.7. | CC:44, INT:65; HWW:157-168 |

##### 6. Expected-step rule
- **Never an expected step at any scope x complexity.** No level, workflow step, or routing-table step requires it (HWW:154,309,317; the routing row `multi-model-review` has level `-` and `changes_files` no). Absence must never be flagged, including in HIGH cells: those are (J) recommendations, not file rules.
- **Count it as present, not required, only when** a run folder exists with `status` success/partial, real-model content (no `stub:` marker), and a follow-up triage (e.g. `/sc:adversarial --suspect-source`). A stub-only folder means "wizard practised", not "second-family review done". Expected only if a task file or spec explicitly names multi-model review for that work (J; no such file seen).

Full file for the citation key, the footprint (section 5), the proposals (section 7) and the unverified items (section 8): [command-nuance/sc-swarm-wizard.md](command-nuance/sc-swarm-wizard.md)

#### 6.3.14 /sc:implement (Implement)

##### 1. Status and role

- Does: "Middleweight spec executor: walk a spec/PRD/tasklist, per-task spec-compliance QA, one-line ledger" (IM:3). Phase: Implement (executor for `/sc:workflow` plans, hand-written plans, notes, or one inline prompt). Standalone-invokable, explicit only, never auto-activated (IM:15-20). Backing skill exists: `skills/sc-implement-protocol/` (SKILL.md, 3 refs, 1 script). Not retired.
- Overlaps: plain edit + test (T/B, proposed minimum per VO), `/sc:task` (retired standalone; `/sc:implement` is forbidden to call it, IM:129, IS:11), `/task` (MDTM executor; "operator types it themselves", IM:139), `bmad-dev-story` / `bmad-quick-dev` (BMad lane, CV:146-147).
- One path only: Q0-Q8 (IS:102-131). Complexity changes only reviewer mode (inline vs one subagent, IS:100), the N=1 FINAL skip (IS:133,153), the N>=20 notice (IS:65), and managed-vs-legacy rules (IS:13). There is no tier, no `--depth` (VO E1.6).

##### 2. Flags

###### 2a. Options (every one in IM:51-59 and IS:49; both files agree, no flag is defined in one and missing from the other)

| Flag | Values | Default | What it changes | Worth using | Avoid |
|---|---|---|---|---|---|
| `<path>` (aliases `--spec`, `--prd`, `--tasklist`) | one existing file | one of path or prompt (IM:55) | Source file. Aliases are cosmetic: "aliases for one file" (IM:49). Two files = `E-NO-SOURCE`; directory or missing = `E-SOURCE-MISSING`; path under `.claude/skills\|agents\|commands` = `E-NO-SOURCE` (IS:56-58). Ledger slug = `{basename<=24}-{sha256(absolute path)[:8]}` (IS:63) | Any enumerable plan: workflow plan, hand-written plan, spec, informal notes (HW:194 names "a plan you wrote yourself") | A task-builder (MDTM) file (see 2c) |
| `<prompt>` (leftover text) | free text | one of path or prompt (IM:56) | Persisted to `.dev/implement/<slug>/source.md` before any edit; `<slug>` = first 24 slug-chars + sha256(full prompt)[:8] (IS:60). Becomes ONE task, the prompt text is its AC (IM:29; IS:62,88). No parallel, no end-of-list pass (IS:133) | One deliverable, files and test nameable in the prompt, one session (see 2b) | Anything with several independent deliverables or any need to trace requirements one by one |
| `--resume` | switch | implicit when a matching ledger exists (IM:57; LG:104) | Nothing observable. No Wave 0 step reads it beyond the known-option list (IS:49; grep of IS for "resume" shows no flag handling). Resume = re-invoke on the same source; first task whose latest ledger status is not `complete` (LG:89-100) | Optional, as documentation to the reader | Do not rely on it to change behaviour. Resume does NOT happen if the source key changed: reworded prompt = new slug (IS:60); copied or moved file = new absolute-path hash (IS:63) |
| `--ledger <path>` | path under `.dev/implement/` | `.dev/implement/<slug>/progress.md` (IM:58) | Relocates the ledger inside `.dev/implement/`. Outside it = `E-LEDGER-PATH` (IS:36). Managed package: only its sibling `progress.md` is accepted, anything else `E-LEDGER-PATH` (IM:58; MW:31) | Almost never. Only to give a legacy run a human-readable folder (J) | Managed plans (pointless, rejected). Also avoid when a checker globs `.dev/implement/*/progress.md`: a different file name or depth would be missed (J) |
| `--skip-final-review` | switch | off | Legacy source: skips the whole-list review when N>1 (IS:153). N=1: already skipped, so a no-op (IS:133,153). Managed package: no FINAL and no archive, `E-ARCHIVE-BLOCKED` (MW:51; IS:41). Also suppresses the "run FINAL on resume" step (LG:99,104) | By band, see 2d. HW:227 says "Never turn off a quality check... skip a reviewer step to save time" | Managed packages (always). Any HIGH-band run (J) |

Banned, stop with `E-LEGACY`: `--type`, `--framework`, `--safe`, `--with-tests` (IM:61; IS:32,49-51). `--force` as an option token stops with `E-NO-RULING` (IS:34,49). After the first non-option token these four banned words are plain prompt text (IS:51).

###### Does not exist (people may assume)

| Assumed flag | Fact |
|---|---|
| `--depth quick\|standard\|deep` | Not in the option table (IM:53-59), not in the known-option list (IS:49). Belongs to `/sc:workflow` (VO E1.4). Behaviour if typed: UNVERIFIED (VO E1.3; reading of IS:50-51 says `quick` would start an inline prompt) |
| `--reviewer`, `--fresh`, `--no-extras`, dual-mode pitch | Listed as out of scope (IS:172). No Wave 0 handling, so not valid options |
| `--commit`, `--pr`, `--release` | Will Not auto-commit, open PRs or release (IM:131) |
| `--fix` | No such flag on `/sc:implement`. `--fix` belongs to `/sc:troubleshoot` and `/sc:reflect`, which build a plan the operator then runs with `/sc:implement <pkg>/<id>.md` (`commands/sc/troubleshoot.md:54,201`; `skills/sc-troubleshoot-protocol/refs/remediation-handoff.md:11,138`) |
| per-tier review flags | None. Reviewer mode has no flag: inline when N<=3 and source <=400 lines and session not compacted, else one Task subagent (IS:98-100) |

###### 2b. Input form: plain prompt versus plan file

| Input form | Tasks it yields | Review | Ledger and footprint | Fits | Cited |
|---|---|---|---|---|---|
| Inline prompt | exactly 1 (T1); AC = the prompt text; "do not invent extra tasks or extra scope" | Inline same-session reviewer by rule (N=1, short); one fix pass; no FINAL | `.dev/implement/<slug>/source.md` + `progress.md`; never seen on disk here | LOW only: single deliverable. Prompt must name file, change and test, because the reviewer judges only against the text and an AC not observable from the diff with no check added is `cannot-verify`, not a pass (VO E2.5; QA:52) | IS:60,62,88; QA:52 |
| Informal notes file / prose spec | 1 (T1 = whole document) when zero enumerable items (IS:62,76) | same as prompt | `.dev/implement/<slug>/progress.md` | LOW | IS:62,76 |
| Spec/PRD/tasklist with enumerable items (`- [ ]`, numbered, `R-NNN`, `## Task N`) | N, in source order; mixed prose + items = items only (IS:68-76) | Per-task review; FINAL for N>1 (advisory) | `.dev/implement/<slug>/progress.md` | MEDIUM and above | IS:68-78,153 |
| `/sc:workflow` plan (`schema: workflow-plan/1.2`, `TASK-WF-*`) = managed package | N from its `## Task N` headings | Per-task review + mandatory fresh FINAL subagent + archive helper | `<pkg>/progress.md`, `<pkg>/artifacts/`, `PLAN:` pin, `FINAL:`, `ARCHIVE:` lines; package moves `to-do/` to `done/` (Linux only) | S and B-MEDIUM, per HW:17,132 | IM:63-65; MW:1-62 |
| Task-builder / MDTM file | See 2c | | | NOT intended | IS:78 |

Prompt nuance (reading of IS:82-88, not seen in a run: UNVERIFIED): a multi-clause prose prompt stays ONE task, since prose paragraphs are never split (IS:76). If its sentences contain `MUST`/`SHALL`/`Done when`, AC QUALIFY rules 1 and 3 may split T1 into several ACs; otherwise the whole text is the single `T1.AC1` (IS:82-88). So a prompt written with explicit "Done when" lines gets per-AC citations, a vague one gets one blanket AC. For several separate deliverables, give a checkbox or numbered list in a file instead.

###### 2c. The "never runs a task-builder file" rule: what the files actually say

- Hard refusal: NONE found. The protocol says the opposite of a refusal: "Ignore MDTM fields (`depends-on`, `agent:`, `wave:`, `compliance:`) except `independent`. Phase-N tasklists are accepted as markdown. MDTM-shaped files still use **this** protocol. Do not auto-handoff." (IS:78). `E-NO-SOURCE` only blocks paths under `.claude/skills|agents|commands` (IS:57).
- What it does refuse to do: invoke `/task`, `/sc:task`, `sc:task-protocol` (IS:11; IM:129) and import "MDTM F1, 6-agent phase gates, or `/sc:reflect` as the per-task gate" (IM:130; IS:173; QA:11).
- Consequence (by rule, not run; VF E1 point 2): every `- [ ]` item of a task-builder file, including its QA-gate and reflect items, would be walked as a product task; the file's own checkboxes, frontmatter and Task Log are not updated; the phase panels and `reflect_pre/post` sign-offs never run.
- The team rule is a pairing convention: "TASK-WF folders run with `/sc:implement`, never with `/task`" (HW:216); first pair vs second pair (HW:243, 305-306); "executor that matches the input file" (CV:233). The reverse direction (task-builder file to `/sc:implement`) is implied by those pairings and by IM:129-130, not stated as a prohibition in any file read. Treat as a CONVENTION a checker may flag (J), not as a tool-enforced stop.

###### 2d. `--skip-final-review` by complexity band

Band thresholds below are the file's own reviewer-mode switch (N<=3, source <=400 lines, IS:100) and the N=1 FINAL skip (IS:133); the band names are mine (J).

| Band (signals) | Legacy source | Managed package |
|---|---|---|
| LOW: N=1 (a prompt, notes file, or one-task spec) | No-op: FINAL is already skipped at N=1 (IS:153). Never type it | FINAL is mandatory even at N=1 (IS:155; MW:46-48); the flag blocks archiving. Never type it |
| MEDIUM: N=2-3, source <=400 lines, one session (inline review) | Allowed: FINAL is "advisory" and does not rewrite verdicts or reopen tasks (IS:153). Skipping loses the only whole-list check, and HW:227 forbids skipping a reviewer step to save time. Acceptable only with a stated reason (J) | Do not use |
| HIGH: N>=4, or source >400 lines, or multi-session / compacted (subagent review; N>=20 prints a compaction notice, IS:65,100) | Do not use (J). Per-task QA diffs only the increment since that task's Q0 snapshot (IS:118-119), so cross-task drift is caught only by FINAL. Likely also outside the plan-lane (see 3) | Do not use. The package would stay in `to-do/` forever (MW:51,60) |

##### 3. Scope x complexity matrix

Scope letters per the brief: T one-off, B bug fix, S single story, F multi-story feature, R multi-feature release (Ruling 2: full release plan, implementation and push), N new product. The command does not vary by complexity itself (one path, section 1); the bands decide whether it is the right executor at all.

Bands for this command (signals from files; thresholds marked J are mine):

| Band | Signals |
|---|---|
| LOW | One deliverable; files and test nameable in one sentence; one session; no driving spec; no risk trigger (secrets, permissions, user input, file paths, infrastructure). Fits HW level 2 shape (HW:16) or a 1-task level 3 plan (HW:17). N=1. TCS-equivalent <=12 (J; TCS is defined only for task-builder bodies, TB:2410-2433; 2 files in one subsystem = 10, 3 files = 13) |
| MEDIUM | A few files, clear scope, 1-2 sessions, 2-3 tasks, a short or no spec, nothing that "must not drift" (HW:17). Review still inline (N<=3, <=400 lines, IS:100). TCS-equivalent 13-34 (J) |
| HIGH | Many files or several subsystems, more than one session, must not drift, a spec to trace requirement by requirement, files not nameable up front, stories sharing an interface, or a risk trigger (HW:18,19,22; VF "Complexity signals" table; TB:2410-2415 for the counting rules). Subagent review, N>=4 or >400 lines (IS:100). TCS-equivalent >=35 or refactor-class `type:` (TB:2438, J) |

Cells: rating, then the flag set. "(lane)" = rating holds when the tasklist step chose the `/sc:workflow` lane; in the task-builder lane the cell is SKIP.

| Scope | LOW | MEDIUM | HIGH |
|---|---|---|---|
| T | OPTIONAL (J, built on the PROPOSED T minimum "plain edit + related test", VO verdict 2): `/sc:implement "<file, change, test>"`, no flags | REQUIRED (J, lane): HW:22 hard limit (>5 edits or >1 source file) forces a written plan; level 3 = `/sc:implement <plan path>`, no flags | SKIP (J): level 4, `/task-builder` + `/task` (HW:18,22). A "one-off" this big is mis-scoped |
| B | OPTIONAL (J): HW bug route 3a is test-first fix + `/sc:test`, no implement (HW:131; routing row bug 3a, HW:311). Prompt form allowed, no flags | REQUIRED (lane): route 3b/4, `/sc:workflow --depth quick` then `/sc:implement <plan>` (HW:132; HW:311). Operator-run, never auto (`commands/sc/troubleshoot.md:190`) | SKIP: route 3c, `/task-builder` + `/task` (HW:133) |
| S | REQUIRED (lane): `/sc:workflow --depth quick` then `/sc:implement <plan>`, no flags (HW:17,305; CV:143) | REQUIRED (lane), but move to task-builder when any HIGH signal appears; at exactly 2 sessions both rows fit and the heavier wins (HW:9, VF verdict 2) | SKIP: `/task-builder` + `/task`; conditions in VF "Is /task-builder ever justified on a SINGLE story" (more than one session, spec to trace, larger or riskier, files not nameable) |
| F | OPTIONAL (J), per story only: several independent single-subsystem stories, each 1-2 sessions, no driving spec, may run as separate workflow plans, but no feature-level coverage check exists (VF "Rule I suggest", J) | SKIP (J): not eligible as the feature minimum (VF verdict 1: no research wave, no `--spec`, plan frozen after task 1, sized for 1-2 sessions) | SKIP: `/task-builder --spec` + `/task` is the feature minimum (VF verdict 1; HW:306-307) |
| R | OPTIONAL (J): only as executor of a constituent S-size item inside the release. Never the release-level step. Re-rated, see section 7 | OPTIONAL (J): same | SKIP (J): constituent features at F-size use `/task` |
| N | N/A: a new product is not LOW; if it is, it is S | SKIP: `/roadmap` emits task files for `/task` (HW:76,309; CV:112,144) | SKIP: same |

Flag set in every cell above: none. `--resume` is implicit (IM:57). `--skip-final-review`: never in LOW (no-op), reason-only in MEDIUM, never in HIGH or managed (2d). `--ledger`: default.

##### 4. Choose this or the neighbour

| Neighbour | Pick `/sc:implement` when | Pick the neighbour when | Cited |
|---|---|---|---|
| Plain edit + related test (T/B) | You want a checkable record: ledger with `path:line` citations per AC, an independent-by-rubric review, git pin. The prompt names file, change and test | One source file plus its test, <=5 edits, exact change known (HW:16, 22). The edit alone is the T minimum (PROPOSED, VO verdict 2). Do not use the prompt form to get around the HW:22 written-plan limit: a prompt is one task with one blanket AC, not a plan (J) | HW:16,22,304; VO verdict 2; IS:62,88 |
| `/sc:task` | Never as an alternative: retired standalone (Ruling 3). `/sc:implement` itself may not call it | Never | IM:129; IS:11; VO E5.1 (only caller is `/sc:tasklist` Stage 9) |
| `/sc:workflow` first, then `/sc:implement <plan>` (versus prompt form or a hand-written list) | Prompt form is not enough when: more than one source file or >5 edits (HW:22); 2-3 separable deliverables each needing its own acceptance check; files not obvious; reviewer should read AC written by someone other than the implementer | Prompt form or a hand-written checkbox list is enough when it is one deliverable (prompt) or you can write N clear items yourself (HW:194 accepts "a plan you wrote yourself"). `/sc:workflow` adds a structure gate and an advisory `/sc:reflect --mode pre` against its own source only (VF E4) | HW:17,22,194; IS:68-78; VF E4 |
| `/task-builder` + `/task` | S/B with a plan-lane fit: few files, clear scope, 1-2 sessions, nothing "must not drift" (HW:17) | Any of: more than one session; a spec to trace (`--spec`, `reflect_pre`); larger or riskier than a few files; files cannot be named up front; stories share an interface; plan likely to be amended mid-run (managed plan freezes after task 1: `E-PLAN-CHANGED`, MW:42). Tie at 2 sessions: heavier row (HW:9). Never feed the task-builder file to `/sc:implement` (2c) | VF verdict 1-2, "Complexity signals" table; HW:9,18,19,22 |
| `bmad-dev-story` / `bmad-quick-dev` | Task-file lane work (`TASK-WF-*` or hand plan) | BMad lane: a story file exists from `bmad-create-story` (dev-story); BMad small change (quick-dev). "Pick the lane at the Spec step and stay in it" (CV:223) | CV:146-147,223 |
| `/sc:troubleshoot --fix` | Executing the plan that Tier 3 built: troubleshoot surfaces the literal `/sc:implement <pkg>/<id>.md` and stops; the operator runs it | Diagnosis only (default) | `commands/sc/troubleshoot.md:54,190,201`; `skills/sc-reflect-protocol/refs/remediation-handoff.md:21,96` |
| `/sc:reflect --mode post` | Not a substitute. `/sc:implement` does not run reflect as the per-task gate and does not need it (IM:130; QA:11) | Optional audit afterwards against spec; troubleshoot and reflect remediation chains surface it as the post-execution gate | IM:130,140; `skills/sc-troubleshoot-protocol/SKILL.md:564` |
| `/sc:test`, `/sc:git` | Not gates; "Suggest ... only as optional next steps" (IS:159). Lint, typecheck, tests run inside Q6 as extras if they already exist; they never decide the verdict (IS:135-147) | Run `/sc:test` yourself when no test existed to detect | IS:135-159 |

##### 6. Expected-step rule

- Count `/sc:implement` as EXPECTED when the work's tasklist step produced a `/sc:workflow` plan or a hand-written plan as its executor input: S (LOW, MEDIUM) and B-MEDIUM, and T-MEDIUM (J). Evidence of the miss: a `TASK-WF-*` package whose `files=`-listed product paths changed but has no `progress.md`, or whose tasks are all `complete` with no `FINAL:` (legacy N>1) or no `ARCHIVE: start` / still in `to-do/` (managed). Do not flag a plan that exists with no ledger and no related commits yet: not started (J).
- Its ABSENCE is fine for: T and B at LOW (plain edit + test; PROPOSED minimum), every task-builder lane (S/B HIGH, F, N via `/task`), the BMad lane (`bmad-dev-story`, `bmad-quick-dev`), and the release-level step of R. At F and R, a `/sc:implement` ledger is allowed only for a constituent S-size item (J).
- Flag as WRONG (not as a skipped step): ledger `source:` is a task-builder output, or a `TASK-WF-*` folder was run with `/task` (HW:216); `/sc:task` used standalone (retired).
- `--skip-final-review` has no direct footprint except the missing `FINAL:`/archive. Do not flag a missing `FINAL:` at N=1 (IS:153). At N>1 legacy, a missing `FINAL:` is a soft finding (the pass is advisory, IS:153); on a managed package it is a hard one (no archive possible, MW:51).

Full file for the citation key, the footprint (section 5), the proposals (section 7) and the unverified items (section 8): [command-nuance/sc-implement.md](command-nuance/sc-implement.md)

#### 6.3.15 /sc:test (Implement)

##### 1. Status and role

- Does: "Execute tests with coverage analysis and automated quality reporting" (cmd:3). Runs the project's existing runner, reports coverage and failure analysis; does not write tests (cmd:98-106). Standalone and invokable; NOT retired. Frontmatter: `category: utility`, `complexity: enhanced`, `mcp-servers: [playwright]`, `personas: [qa-specialist]` (cmd:4-7).
- Phase: Implement (verify), also Bug fix step 3a (HWW:131, 311). Backing protocol skill `~/.claude/skills/sc-test-protocol/` DOES NOT EXIST (`ls` returned "No such file or directory"). Expected, not a defect: HWW:232 says commands whose file names no skill, "for example `/sc:help`, `/sc:explain`, `/sc:test`", run from their own file. The only similarly named skill, `sc-validate-tests-protocol`, tests `/sc:task` tier rules and is unrelated (HWW:285).
- Overlaps: the plain test runner (the real alternative), test steps inside `/task` (HWW:18, 81) and `/sc:implement` (VO E3.5), `/sc:troubleshoot --type test` (HWW:125). Does not call or depend on `/sc:task` or `/sc:tasklist`. No skill calls `/sc:test` programmatically: every hit is a suggested next step in prose (`implement.md:140,144`; `sc-implement-protocol/SKILL.md:159`; `spawn.md:210`; `cleanup-audit.md:119`; `sc-cleanup-audit-protocol/SKILL.md:171`).

##### 2. Flags

Usage line, the only flag definition anywhere: `/sc:test [target] [--type unit|integration|e2e|all] [--coverage] [--watch] [--fix]` (cmd:22). There is no protocol skill, so cmd is the complete flag source. The command file defines no flag defaults; the one default behaviour is inferred from the "Basic Test Execution" example.

| Flag / arg | Values | Default | What it changes (cited) | Worth using when | Avoid when |
|---|---|---|---|---|---|
| `target` (positional) | path to a file or directory | whole project (inferred from example cmd:66-68, "Discovers and runs all tests") | Scopes discovery to that path, e.g. `src/components` (cmd:74). Guide examples pass a test file or folder (HWW:131, 172) | Always, when the related test or folder is known up front. It is what makes this equivalent to "run the related test" | Never omit it on a repo with a slow suite: the no-target form runs everything (cmd:66-68) |
| `--type` | `unit` \| `integration` \| `e2e` \| `all` | not stated; no-flag example implies all (cmd:66-68) | Narrows the category (cmd:22, 74). `e2e` auto-activates Playwright MCP for browser testing, cross-browser and visual checks (cmd:43, 81-84) | `unit` for a fast loop on one module. `e2e` only when a browser-facing product exists. HWW:172 says add it "to narrow" | `e2e` where there is no UI or Playwright is not wired (UI presence in this repo is UNVERIFIED, CVP U15). Do not pass it just to look thorough |
| `--coverage` | switch | off; but the no-flag example already "generates pass/fail summary and basic coverage" (cmd:68), while `--coverage` gives "detailed coverage metrics" (cmd:75) | Adds a coverage report and metrics (cmd:30, 36, 52, 75) | Routing table lists it as the mandatory flag for bug step 3a (HWW:311) and for the `tests` row (HWW:319). Use when someone will read the numbers | When the repo has no coverage tooling: none of `pytest.ini`, `tox.ini`, `package.json`, `Makefile`, `.coveragerc` exists at this repo's root (checked), and the main tests are bash scripts. What it would do here is UNVERIFIED |
| `--watch` | switch | off | Continuous run on file changes (cmd:39, 58-59, 86-90) | Interactive local dev loop only | Any unattended or scripted session (a watch never returns). Never in a pipeline step. Behaviour in a non-interactive session is UNVERIFIED |
| `--fix` | switch | off | "automatic simple failure fixes" (cmd:89-90) | Rarely: trivial failures during a watch loop | Whenever the diff must stay reviewable or a ledger-style record is wanted. The file does not say WHAT it edits (source or tests). Its own Boundaries say it will not "make destructive changes to test files without explicit permission" and will not modify test framework configuration (cmd:106, 104): the flag and the boundary are not reconciled |

Does not exist (absent from cmd; do not assume): `--depth` (belongs to `/sc:workflow`, `/sc:troubleshoot`, etc., VO E1.4), `--spec`, `--tasklist`, `--resume`, `--ledger`, `--framework`, `--parallel`, `--no-coverage`, `--compliance`, `--output`. Test generation is explicitly out of scope: "Will Not: Generate test cases" (cmd:104); use `bmad-qa-generate-e2e-tests` or the spec/task file instead (HWW:173).

##### 3. Scope x complexity matrix

Plain statement: the command itself does not vary by task complexity. It has no tiers, no `--depth`, and no complexity formula (no TCS use; cmd has no such text). What varies is the SIZE OF THE TEST TARGET, so the bands below are JUDGMENT bands on test-target signals (the brief allows proposed thresholds when labelled; no file gives one).

Band definitions (all (J)):
- LOW: one named test file or test command, known before starting (HWW:16, 131).
- MEDIUM: a test folder or module, still named up front (HWW:172 example `tests/billing/`), no special infrastructure.
- HIGH: the whole suite, tests spanning subsystems, e2e/browser tests, or tests that need infrastructure. In THIS repo that means the contract suite, which the AIDev02 gate builds an image for and runs inside it (`.github/workflows/coder-ci-aidev02-contract.yml:1`, 1158-1163).

Reasons shared by the cells: `/task` already runs tests and an audit (HWW:18, 81; "do not re-run ... the tests yourself", HWW:81; "Do not repeat a skill's own checks", HWW:226). `/sc:implement` runs tests only if they exist, scoped to the task's files, and never as the pass/fail (VO E3.5; `implement.md:128`), and tells the user `/sc:test` is "Optional ... not gates" (`implement.md:140`). The repo gate is CI (repo `CLAUDE.md` Development Practices). So no cell is REQUIRED for the COMMAND. What is mandatory is the ACTIVITY "run the related test" (HWW:16, 119, 311), by any means.

| Scope | LOW | MEDIUM | HIGH |
|---|---|---|---|
| T one-off | WORTH IT (J): `/sc:test <test file>`; the plain runner is equally valid. Proposed one-off minimum is a plain edit plus the related test (VO verdict item 2; PROPOSED, not confirmed by Ryan) | OPTIONAL (J): `/sc:test <folder> --type unit` | N/A (J): HWW:22 hard limit (>5 edits or >1 source file) moves the work out of a one-off |
| B bug fix | WORTH IT: `/sc:test <test path> --coverage`. Guide names exactly this as step 3a for a small fix (HWW:131, 311) | OPTIONAL (J): the `/sc:workflow` + `/sc:implement` route runs tests as it goes (HWW:117); add `/sc:test <folder>` only for a regression sweep beyond the task's files | SKIP (J): `/task-builder` + `/task` runs tests and a final audit (HWW:18, 81, 133) |
| S single story | OPTIONAL (J): `/sc:implement` ran scoped tests (HWW:117, 119) | WORTH IT (J): `/sc:test <module folder> --type unit\|integration` once before commit, because `/sc:implement`'s tests are scoped to the task's files and not a pass/fail (VO E3.5) | OPTIONAL (J): story run through `/task`, whose end-of-run tests apply (HWW:18); add only for a coverage figure (`--coverage`) |
| F multi-story feature | SKIP (J): HWW:81, 226 | SKIP (J): same | OPTIONAL (J): one `/sc:test --type all --coverage` after the last phase if coverage numbers are wanted and a local runner exists; otherwise CI |
| R multi-feature release | OPTIONAL (J): few features, CI covers it | WORTH IT (J): `/sc:test --type all` as a pre-push integration signal across features | WORTH IT (J): `--type all --coverage`, plus `--type e2e` only if a UI exists. Pre-push signal only: CI remains the gate |
| N new product | N/A (J): a new product is not LOW | OPTIONAL (J): `/task` runs tests per phase (HWW:18, 81) | OPTIONAL (J): `--type e2e` if a UI product exists (UNVERIFIED, CVP U15) |

R re-rating under the multi-feature definition (brief ruling 2): the rating stays WORTH IT, but the reason changes. The old reading ("a release assembles and ships work already built", CVP:139) had `/sc:test` valued as a final check of assembled work; under the new definition the value is cross-feature regression, which is a stronger case. See section 7.

##### 4. Choose this or the neighbour

| Neighbour | Decision rule (signals) | Cites |
|---|---|---|
| Plain test runner (`bash <script>`, `pytest <file>`, etc.) | Use the plain runner when the related test is one named file and its run command is known (LOW). It satisfies "run the related test" (HWW:16, 304). Use `/sc:test` when you need ANY of: coverage figures, framework auto-detection because the runner is unknown, a written failure analysis, or Playwright e2e. What `/sc:test` adds over the plain runner is auto-detect, coverage report, failure analysis with recommendations, e2e via Playwright (cmd:27-31, 35-38, 43). What it does NOT add: no spec trace, no acceptance criteria, no independent reviewer, no ledger, no named output file | cmd:25-39, 98-100; HWW:16 |
| Tests inside `/task` or `/sc:implement` | If the work went through `/task`, do not run `/sc:test` again for the same scope (HWW:81, 226). If it went through `/sc:implement`, `/sc:test` is the only step that gives a whole-folder pass/fail, because implement's test run is scoped and not a verdict (VO E3.5) | HWW:81, 119, 226; `implement.md:128,140` |
| `/sc:troubleshoot --type test` | Failure obvious from the output and the fix is small: stay in `/sc:test`. Failure unexplained, intermittent, or spanning areas: switch to `/sc:troubleshoot ... --type test` (it diagnoses and writes `REPORT.md`; `/sc:test` only "analyses") | HWW:124-125, 311; CVP:175 |
| `bmad-qa-generate-e2e-tests` | Needs new tests written: use the generator. `/sc:test` only runs existing suites (cmd:98, 104) | cmd:98, 104; CVP:151 |
| `/sc:validate-tests` | Name collision only: it tests `/sc:task` tier rules, a contributor tool. Never a substitute | HWW:285 |
| CI (`.github` Actions) | CI is the validation gate; one-off local validation scripts are discouraged. A local `/sc:test` result is a convenience signal and never replaces the CI result. In this repo most validation is bash contract tests that run in a built image, so a local run may not be able to reproduce the gate at all | repo `CLAUDE.md` "Development Practices"; `PROJECT_INDEX.md` Pipeline; `coder-ci-aidev02-contract.yml:1,1158-1163` |

##### 6. Expected-step rule

- Count the ACTIVITY, not the command: "related test run, or CI green on the PR" is expected for T, B, and S whenever source changed (HWW:16, 119, 311). Never flag a missing `/sc:test` invocation as a skipped step at any scope or complexity, because plain runners, `/task`, `/sc:implement` and CI all satisfy the activity.
- The only place the guide names the command as a step is B LOW (small fix), `/sc:test <test path> --coverage` (HWW:131, 311). A checker may accept either that or an equivalent plain run there; it cannot tell them apart, since `/sc:test` leaves no footprint. Absence is fine for F (tests are inside `/task`, HWW:81), for all N, and for S/B when a plan executor ran.

Full file for the citation key, the footprint (section 5), the proposals (section 7) and the unverified items (section 8): [command-nuance/sc-test.md](command-nuance/sc-test.md)

#### 6.3.16 /sc:build (Implement)

##### 1. Status and role

- Does: "Build, compile, and package projects with intelligent error handling and optimization" (`~/.claude/commands/sc/build.md:3`). Phase: Implement (verify side). Standalone-invokable, NOT retired. Playwright MCP and `devops-engineer` persona are declared (`build.md:6-7`).
- **Backing protocol skill does not exist.** `ls /home/coder/.claude/skills/sc-build-protocol/` returned "No such file or directory", and no `sc-*build*` skill exists in `~/.claude/skills/`. Behaviour is the 108-line command file only; nothing is defined beyond it.
- Overlaps: `/sc:test` (runs tests), `/sc:troubleshoot --type build` (`troubleshoot.md:8,50`, diagnoses a broken build), `/task` (runs tests itself), and the CI workflows under `.github/workflows/`. `HOW-WE-WORK.md:269` lists it only under "installed but no workflow above routes to them": "Build or package the project." `sc-cli-portify-protocol/SKILL.md:584` lists it as an optional follow-up ("Build and compile after generating").

##### 2. Flags

Usage line: `/sc:build [target] [--type dev|prod|test] [--clean] [--optimize] [--verbose]` (`build.md:22`). The command file defines no defaults and no flag semantics beyond the example comments; there is no protocol skill to define them.

| Flag / arg | Values | Default | What it changes (cited) | Worth using | Avoid |
|---|---|---|---|---|---|
| `[target]` | a component name, e.g. `frontend` | whole project (`build.md:66-68`) | "Builds specific project component with detailed output" (`build.md:82-84`) | When one buildable component exists and the others are slow | Never useful here for a Terraform-only change: this repo has no component to name (see section 8, U3) |
| `--type` | `dev`, `prod`, `test` | not stated; no-flag example uses "default configuration" (`build.md:66-68`) | Selects environment-specific config and optimization (`build.md:56`) | `--type test` before a manual test run if a test build target exists | `--type prod` in this repo: nothing here produces a prod bundle locally |
| `--clean` | boolean | off | "Clean production build" (`build.md:74-76`); exact meaning (wipe output dir? caches?) not defined | After a dependency or toolchain change, when a stale cache is the suspect | Routine runs: slower, and the command may not own the directory it cleans (UNVERIFIED) |
| `--optimize` | boolean | off | "Minification, tree-shaking, and deployment preparation" (`build.md:76`) | A JS/bundled front end where size matters | Anything not bundled. Terraform, shell and Docker work in this repo have no minify step |
| `--verbose` | boolean | off | "Real-time progress monitoring and diagnostic information" (`build.md:84`) | A build that fails with a thin message | Normal runs: floods the transcript |
| `--validate` | not defined | n/a | Appears ONLY in the example at `build.md:90` ("Development build with Playwright validation"). It is NOT in the usage line (`build.md:22`). Treat as undocumented. | Not recommended | Always, until the file defines it |

Does not exist (people may assume):

- `--depth` (that is `/sc:workflow`, `/sc:reflect`, `/sc:troubleshoot`; `/sc:build` has none).
- `--fix`, `--dry-run`, `--output-dir`, `--report-path`: not in `build.md`. The report location is undefined: "Write: Build reports and deployment documentation" (`build.md:52`) names no path.
- Any flag that installs dependencies or edits build config: banned, "Will Not: Modify build system configuration or create new build scripts; Install missing build dependencies or development tools; Execute deployment operations beyond artifact preparation" (`build.md:103-107`).

##### 3. Scope x complexity matrix

**Does the command vary by complexity? No.** Its flags (section 2) pick an environment and an optimization level, not a depth of process; there is no `--depth` and no complexity tier in the file (`build.md:5` "complexity: enhanced" is a catalogue label, not a TCS value). What varies is whether a local build entry point exists and can run. So the bands below are defined by build-relevance signals (all JUDGMENT, marked `(J)` as a set), not by the TCS formula (`~/.claude/skills/task-builder/SKILL.md:2422-2433`, which scores task files, not builds).

Repo facts behind the cells:

- No `package.json`, `Makefile`, `pyproject.toml`, `go.mod`, `Cargo.toml`, `pom.xml` or `build.gradle` anywhere outside `.git`, `_bmad` and `node_modules` (find, 2026-10-27). Only Dockerfiles: `templates/VSCode-AIDev02/Dockerfile.coder`, `templates/VSCode-AIDev02/collector/Dockerfile`, and AIDev01 files.
- The image is built in CI: `docker buildx build ... --file "$TEMPLATE_DIR/Dockerfile.coder"` (`.github/workflows/coder-ci-aidev02-contract.yml:696`, also `:939`).
- The one real package build, `orca-build/build-deb.sh`, refuses to run outside Actions: `[[ ${GITHUB_ACTIONS:-} == true && ${GITHUB_RUN_ID:-} =~ ^[0-9]+$ ... ]]` (`orca-build/build-deb.sh:22`), header "Run only in the separately authorized Actions build" (`:2`), needs Linux x86_64 and Node v24 (`:24-25`). CI runs it in job `orca_derivative`, `workflow_dispatch` only, on `[self-hosted, big]` (`coder-ci-aidev02-contract.yml:219-221,308`).
- Project rule: "Validation should be done via the .github actions. One off validation scripts should be avoided" (`CLAUDE.md`, Development Practices).

Band definitions (this repo, J):

| Band | Signal |
|---|---|
| LOW | Change touches no build input: docs, markdown, shell under `scripts/`, Terraform `.tf`, contract-test scripts. |
| MEDIUM | Change touches an input to the image or package build (`Dockerfile.coder`, `orca-build/*`), so CI will rebuild. |
| HIGH | Change to the build itself: base image or apt pins, toolchain versions, `build-deb.sh` patches or pins. A build failure is the main risk. |

| Scope | LOW | MEDIUM | HIGH |
|---|---|---|---|
| T one-off | SKIP (J) | SKIP (J): CI builds it | N/A (J): more than one source file or more than 5 edits is level 3+ (`HOW-WE-WORK.md:22`) |
| B bug fix | SKIP (J) | SKIP (J): use `/sc:troubleshoot --type build` for a red build | OPTIONAL (J), only to reproduce locally, `--type dev --verbose`; likely cannot run here (`build-deb.sh:22`) |
| S single story | SKIP (J) | SKIP (J): push and let CI be the gate | OPTIONAL (J), same as B |
| F multi-story feature | SKIP (J) | OPTIONAL (J), `--type test` only if a local build target exists | OPTIONAL (J), `--verbose`; CI remains the gate |
| R multi-feature release | SKIP (J) | OPTIONAL (J) | OPTIONAL (J): the image build and the Orca package build and publish are CI jobs (`coder-ci-aidev02-contract.yml:308,370-438,696`) |
| N new product | SKIP (J) | OPTIONAL (J) | WORTH IT (J), only after the product has a build config; the command will not create one (`build.md:105`) |

No cell is REQUIRED: no Ryan pipeline names it (brief ruling 5), no routing row routes to it (`HOW-WE-WORK.md:269`), and the project gate is CI. For a repo that does have a bundler and local build, T/B/S MEDIUM would move to WORTH IT (J) as a pre-push smoke build; that is not this repo.

##### 4. Choose this or the neighbour

| Neighbour | Decision rule | Cite |
|---|---|---|
| CI (`.github` Actions) | In this repo CI wins unless a local build is genuinely runnable. Push the commit and read the workflow result; do not build locally to "pre-validate". Use `/sc:build` only if a local toolchain exists AND you need the error before pushing. | `CLAUDE.md` Development Practices; `build-deb.sh:22` |
| `/sc:troubleshoot --type build` | A build is already failing: use troubleshoot (diagnosis, evidence, `REPORT.md`). `/sc:build` runs a build and parses errors; it has no hypothesis testing. | `troubleshoot.md:8,42,50`; `build.md:57` |
| `/sc:test` | Tests, not packaging: use `/sc:test`. Running the related test is the mandatory check at levels 2 and 3. | `HOW-WE-WORK.md:170` (section 3.8) |
| `/task` | `/task` runs the tests itself at the end; no separate `/sc:build` step is needed inside a task file. | `HOW-WE-WORK.md` level 4 row |
| `bmad-quick-dev` / `bmad-dev-story` | Not alternatives; they implement code. A build step after them is optional on the same terms as above. | `command-value-by-phase.md` 2.4 |

##### 6. Expected-step rule

Never count `/sc:build` as an expected step at any scope or complexity in this repo: it is in none of Ryan's pipelines (brief ruling 5) and the validation gate is CI (`CLAUDE.md`). Its absence is always fine; its presence is not a deviation and must not be accepted as a substitute for a green CI run or for the related test.

Full file for the citation key, the footprint (section 5), the proposals (section 7) and the unverified items (section 8): [command-nuance/sc-build.md](command-nuance/sc-build.md)

#### 6.3.17 /sc:improve (Implement)

##### 1. Status and role

- Does: "Apply systematic improvements to code quality, performance, and maintainability" (IMP:3). Phase: Implement, as an off-pipeline hygiene step (CV:153); routing row `cleanup`, step 4 (HWW:318). Standalone-invokable, not retired. Not in any of the brief's five pipelines.
- Backing protocol skill `~/.claude/skills/sc-improve-protocol/` DOES NOT EXIST (`ls` exit 2; no skill folder with "improve" in its name under `~/.claude/skills/`). The command file names no skill (IMP:1-8), so it runs from its own file (HWW:232). Everything below comes from IMP plus the guide.
- Overlaps: `/sc:cleanup` (same guard rails, CV:154), `/simplify` (built-in, CV:156), `/sc:analyze` (reports; its own "Next Step" points here, ANA:111), and the level 3 / level 4 plan routes for anything beyond a small folder tidy (HWW:22, 168).

##### 2. Flags

Usage line, the only place IMP lists flags: `/sc:improve [target] [--type quality|performance|maintainability|style] [--safe] [--interactive]` (IMP:22). No `argument-hint` frontmatter (IMP:1-8). Flags 5-7 below appear only in examples or boundaries, not in the Usage line.

| # | Flag | Values | Default | What it changes (cited) | Worth using | Avoid |
|---|---|---|---|---|---|---|
| 1 | `[target]` | a path or a name. Examples: `src/`, `api-endpoints`, `legacy-modules`, `auth-service` (IMP:65,73,81,89). The guide passes a folder: `src/billing/` (HWW:165) | not stated | Scope of analysis and edits (IMP:27). A FOLDER target is what the guide's exception to the 5-edit limit covers (HWW:22) | Always give one explicit folder so the whole `git diff` stays reviewable (J) | No target or the repo root: default not stated (UNVERIFIED). A single file expected to need more than 5 edits: the exception text says "on a folder", so it is not covered (HWW:22; reading, not a stated rule) |
| 2 | `--type` | `quality`, `performance`, `maintainability`, `style` (IMP:22) | not stated | Picks the pattern and persona: quality = debt then refactor; performance = profile then optimise; maintainability = structure then complexity then docs (IMP:55-57). Personas architect, performance, quality, security (IMP:7,44) | `quality` is the only value the guide uses (HWW:165, 318). `style` for format-and-naming only (J) | `performance` without a measured bottleneck: IMP:56 puts profiling first and names no tool (J). `security`: used in an example (IMP:89) but not in the enum (IMP:22), so unconfirmed |
| 3 | `--safe` | switch | off (not stated) | Named in Usage and examples (IMP:22,65-68 "safe refactoring application"). NO file read defines what it does. The guide makes it mandatory with `--type quality` in the `cleanup` row, step 4 (HWW:318 `mandatory_flags`) | Always when running under the guide (HWW:165, 318) | Treating it as a guarantee: undefined. The guide still says commit first "so every change can be undone" (HWW:163) |
| 4 | `--interactive` | switch | off (not stated) | Named in Usage and the `api-endpoints` example (IMP:22,73-76). Indirect definition only: the Approval Required list (IMP:117-123) and the guide: it "asks before complex changes, but some changes are applied automatically even then" - formatting, naming, unused variables, import order, simple type annotations (HWW:166; matches IMP:110-115) | Always; mandatory in `cleanup` step 4 (HWW:318). It is the main brake at MEDIUM | Reading it as a substitute for `git diff` review: the guide requires the review anyway (HWW:166, 318 step 5) |
| 5 | `--preview` | switch (example only) | n/a | Example: "Preview mode shows changes before application for review" (IMP:81-84). Not in Usage, not in the guide | MEDIUM band first pass, if the command really parses it (J) | Relying on it: UNVERIFIED that it is a parsed flag |
| 6 | `--validate` | switch (example only) | n/a | Example with `--type security`: "Comprehensive validation ensures security improvements are effective" (IMP:89-92). Not in Usage, not in the guide | none established | Relying on it: UNVERIFIED |
| 7 | `--force` | switch (named in a boundary only) | off | IMP:125-129: "Explicitly Will NOT (without `--force` flag)": make architectural decisions, refactor structure without confirmation, remove functionality. So `--force` lifts the guard rails | never under the guide's exception | Always avoid. If the change needs `--force`, it is HIGH band: use a task file (HWW:168) |

Does not exist in the command file (checked by reading all 130 lines): `--depth`, `--spec`, `--dry-run`, `--aggressive` (cleanup only, CLN:22), `--type code|imports|files|all` (cleanup only, CLN:22), `--handoff`, `--resume`, `--ledger`, `--output`, `--coverage`, `--no-promote`. Also: `/sc:implement` bans `--safe` (V1:79), so do not carry improve's flags over to it.

##### 3. Scope x complexity matrix

The command DOES vary by complexity, because the guide draws a size line around it: it is the one allowed exception to the hard limit (more than 5 edits or more than one source file must go through a written plan), "run on a folder ... commit first and review `git diff` afterwards" (HWW:22). The exception is for "small, contained cleanups" (HWW:163). "Large refactors (many files or a structural change): treat it as a feature" with `/task-builder ... --spec` (HWW:168). No file gives a number for "small" or "large": the band edges below are JUDGMENT unless a cell cites a file.

Band definitions (one line each):

- LOW: only the auto-fix classes (formatting, naming, unused variables, import order, simple type annotations; IMP:110-115); one folder; no signature or public API change; the whole `git diff` can be read in one pass (J).
- MEDIUM: also needs an Approval Required class (logic refactor, signature change, change spanning several files; IMP:119-123), but stays inside one subsystem (counted the TCS way: first two path segments, TB:2411) and must not change behaviour; files can be named up front (HWW:22 "clear scope"). The MEDIUM/HIGH edge is J.
- HIGH: any of: structural or architectural change (IMP:119; IMP:105 says it will not without understanding system impact); two or more subsystems (TB:2411); removing code used by public APIs (IMP:122); risk areas (secrets, permissions, user input, paths, infrastructure); a driving spec or "must not drift" (HWW:18); performance work needing profiling (IMP:56); files that cannot be named up front. At HIGH the guide sends it to a task file (HWW:168).

| Scope | LOW | MEDIUM | HIGH |
|---|---|---|---|
| T one-off | OPTIONAL (J): folder-wide mechanical tidy, `--type quality --safe --interactive`. SKIP if it is one file and 5 edits or fewer: use a plain edit | OPTIONAL (J): `--type quality|maintainability --safe --interactive`, commit first, review diff | SKIP: not a one-off (HWW:168) |
| B bug fix | SKIP (J): a bug goes to `/sc:troubleshoot` (HWW:3.4, CV:175) | SKIP (J) | SKIP (J) |
| S single story | OPTIONAL: tidy the folder the story touched, before the commit; `--type quality --safe --interactive` | OPTIONAL (J): separate commit after the story's tests pass, never mixed into the story's own commit | SKIP: put the refactor in the plan: `/sc:workflow ... --depth quick` + `/sc:implement` if few files (HWW:17), else `/task-builder` + `/task` |
| F multi-story feature | OPTIONAL | OPTIONAL (J): one separate cleanup commit after the feature is built, never inside a `/task` phase | SKIP: `/task-builder --spec` + `/task` (HWW:168). A refactor-type task file scores S6=1 and is forced to `--depth deep` (TB:2415, 2438) |
| R multi-feature release | OPTIONAL (J), was SKIP | OPTIONAL (J), was SKIP | SKIP |
| N new product | SKIP (J) | SKIP (J) | SKIP (J) |

Notes on the matrix:

- No cell is REQUIRED or WORTH IT: no file makes it a step in any pipeline; it is never credited as an implement step.
- R: under ruling 2 a release includes plan, implementation and push, so the CV:139 reading ("a release only assembles work already built, build commands SKIP") no longer holds. For this command R now matches F's LOW/MEDIUM ratings (J); the HIGH cell stays SKIP because structural work belongs in a task file.
- N: nothing legacy exists yet to improve; a hygiene pass over built phases uses the F/R cells.

##### 4. Choose this or the neighbour

| Neighbour | Decision rule | Cite |
|---|---|---|
| `/sc:cleanup` | Dead code, unused imports, empty blocks, redundant annotations: `/sc:cleanup <folder> --type code --safe --interactive`. Quality, naming, formatting, structure: `/sc:improve`. Order in the guide: `/sc:cleanup-audit`, commit, `/sc:cleanup`, `/sc:improve`, review `git diff`. Both auto-apply unused-import handling, so a second pass right after cleanup adds little for LOW (J) | HWW:318; CLN:109-115; IMP:110-115 |
| `/sc:analyze` | Target or type unknown, or you want a report first: `/sc:analyze <path> --focus quality|performance|...` (reports only), then improve. Target and type already known: skip analyze | ANA:111; HWW:144 |
| `/simplify` (built-in) | Code you just changed on this branch: `/simplify` works on the changed code and edits it before the commit. A folder you did not change: `/sc:improve` (J split; `/simplify` has no file, CV:156) | CV:156 |
| `/sc:workflow --depth quick` + `/sc:implement` | The improvement is a defined change in a few named files with testable acceptance criteria, or exceeds the folder-tidy sense of the exception: plan route. Do not hand `/sc:implement` improve's flags (`--safe` is banned there) | HWW:17, 22; V1:79 |
| `/task-builder --spec` + `/task` | HIGH band: structural, several subsystems, public API removal, risk areas, must not drift, or files not nameable up front. Refactor-type file gets TCS S6=1 and `--depth deep` | HWW:168; TB:2415, 2438; V2 "Complexity signals" |
| `/sc:troubleshoot --type performance` | A slow path already observed as a defect: diagnose first (file:line evidence), then fix by the size rules. `/sc:improve --type performance` is for undiagnosed general tuning, and its own pattern wants profiling first | CV:175; HWW:125; IMP:56 |
| `/sc:adversarial` | Only when two competing refactor plans exist; its file lists `/sc:improve` as "Compare improvement approaches" | ADV:181 |

After a run, the guide's normal exits apply: read `git diff` (HWW:166), commit, and `/code-review` before pushing (HWW:199). The command's own "Validate" step says it ensures functionality is preserved (IMP:30) but names no test run, so run the related tests yourself (J; `CLAUDE.md` says validation goes through `.github` Actions).

##### 6. Expected-step rule

- Never count `/sc:improve` as an expected step: no scope x band cell is REQUIRED or WORTH IT (section 3), and it is in none of the five pipelines. Its absence is fine at every scope and complexity. Do not credit it as the implement step for S or F (no spec trace, no ledger), nor as the test step.
- If it appears, treat it as a hygiene extra, not a pipeline step. Optional quality notes (not "skipped step" flags, all J): HIGH-band work done through it with no task file; no commit before the run (HWW:163); a run that used `--force` (IMP:125) or lacked `--safe --interactive` where the routing row wants them (HWW:318, transcript only).

Full file for the citation key, the footprint (section 5), the proposals (section 7) and the unverified items (section 8): [command-nuance/sc-improve.md](command-nuance/sc-improve.md)

#### 6.3.18 /sc:cleanup (Implement)

##### 1. Status and role

- Does: "Systematically clean up code, remove dead code, and optimize project structure" (`cleanup.md:3`). It EDITS files (`cleanup.md:49`, Edit/MultiEdit). Phase: Implement (value:154). Standalone-invokable; not retired. It is not `/sc:task` or `/sc:tasklist`.
- Backing skill `~/.claude/skills/sc-cleanup-protocol/` DOES NOT EXIST (`ls` returned "No such file or directory"). The command file names no skill to load (no Activation block, unlike `audit-cmd:79-84`), so it runs from its own 128 lines (consistent with HWW:232). Nothing beyond `cleanup.md` specifies its behaviour.
- Overlaps: `/sc:cleanup-audit` (its report-only pair, `audit-cmd:119`), `/sc:improve` (same guard-rail pattern, `improve.md:108-129`), built-in `/simplify` (value:156), plain edit.

##### 2. Flags

Usage line: `/sc:cleanup [target] [--type code|imports|files|all] [--safe|--aggressive] [--interactive]` (`cleanup.md:22`). No backing skill, so these are the only definitions. No flag has a stated default (`cleanup.md` has no defaults section): every default below is UNVERIFIED.

| Flag | Values | Default | What it changes (cited) | Worth using when | Avoid when |
|---|---|---|---|---|---|
| `[target]` | path (file or folder); omitted is shown in an example (`cleanup.md:73`, `:81`) | not stated (UNVERIFIED whether omitted means whole repo) | Limits scope of analysis and edits ("across target scope", `cleanup.md:27`). Risk driver number one: the guide says run it "on a folder" (HWW:22, HWW:164). | Always pass an explicit folder (J). | Omitting it, or `.`, in this repo: no exclusion list exists in `cleanup.md`, so `.dev/`, `_bmad-output/`, `.github/` are not protected (J; contrast `audit-skill:54-62`). |
| `--type` | `code`, `imports`, `files`, `all` | not stated | `code` = dead code removal; `imports` = unused import removal; `files` = file organization and structure; `all` = every domain with all three personas (`cleanup.md:55-58`, `:81-83`). Examples only show `code`, `imports`, `all`. | `code` is the only value the guide's routing row names (HWW:318, mandatory step 3: `--type code --safe --interactive`). `imports` for a language-specific import sweep. | `files` and `all`: `files` moves and removes files, and whole-file removal is in NEITHER the auto-fix list nor the approval list (`cleanup.md:109-121`). `all` also "activates all personas" (`cleanup.md:83`) over the widest target. Treat both as HIGH risk (J). |
| `--safe` | flag | not stated (one of the pair `--safe\|--aggressive`) | "Conservative cleanup with automatic safety validation" (`cleanup.md:66`). | Every run (the guide's row carries it, HWW:318). | n/a |
| `--aggressive` | flag | not stated | "Thorough cleanup with Context7 framework patterns" (`cleanup.md:90`). No definition of what extra it removes. | Never as a first pass (J). Only after a clean commit, on a named folder, with the diff read afterwards. | Anywhere the target holds shared interfaces, exports, config values or fixtures; those are approval-class (`cleanup.md:118-121`) and "aggressive" has no stated rule that keeps the prompt. Not in the guide's routing row (HWW:318), so using it is outside the documented path. |
| `--interactive` | flag | not stated | "User guidance for complex decisions" (`cleanup.md:82`). Does NOT stop auto-fixes: the guide says unused imports, zero-reference code, empty blocks and redundant type annotations are still applied automatically (HWW:166, matching `cleanup.md:111-114`). | Every run (HWW:318). It is the only prompt path for approval-class items. | Do not read it as "nothing changes without asking". |
| `--preview` | flag | n/a | Appears ONLY in one example: "shows unused import cleanup without execution" (`cleanup.md:73-74`). It is NOT in the Usage line (`cleanup.md:22`) and is defined nowhere. The same pattern exists in `improve.md:81`. | Try it as a dry run on a first pass over a new folder, but do not rely on it: UNVERIFIED that it is honoured. | Never treat `--preview` as a guard rail in a policy or checker. |

**Does not exist** (people may assume): `--dry-run`, `--backup`, `--rollback` (the file promises "backup and rollback capabilities", `cleanup.md:38`, `:98`, but defines no flag or mechanism; git is the only undo, HWW:163 "commit first so every change can be undone"), `--force` (only in `improve.md:125`), `--exclude`, `--from-audit` / any report-path input, `--depth`, `--pass`, `--focus` (those belong to `/sc:cleanup-audit`, `audit-cmd:31`), `--batch-size`. There is no per-project exclusion file: `.claude-audit/SCOPE.md` is read by `repo-inventory.sh` (`repo-inventory.sh:13`) for the audit only; `cleanup.md` never mentions it.

**Risk order, lowest to highest (J, built from the cited lists):** `--type imports --safe --interactive` on one file < `--type code --safe --interactive` on one folder (documented path, HWW:318) < the same with `--aggressive` < `--type files` < `--type all` < any of these with no explicit target.

**In-file guard rails** (`cleanup.md:107-127`): auto-fix = unused imports, dead code with zero references, empty blocks, redundant type annotations. Prompt first = indirect references, exports possibly used externally, test fixtures/utilities, configuration values. Safety threshold = any usage path, any public API effect, or any doubt means prompt. Gap: "zero references" has no stated method (no grep requirement, no dynamic-use check), while the audit requires a cited grep, a CI/Docker/package/build search, and five dynamic-loading patterns before it will even propose DELETE (`verification-protocol.md:20-25`, `dynamic-use-checklist.md:5-9`, `:120-130`). So `/sc:cleanup`'s auto-delete bar is lower than the audit's recommendation bar.

##### 3. Scope x complexity matrix

**Bands for this command.** The command does vary by complexity, because the damage a cleanup can do scales with what it can reach. No file gives a cleanup threshold; the only on-disk numbers are the guide's 5-edit / one-source-file limit with its cleanup-on-a-folder exception (HWW:22) and task-builder's TCS, where a refactor-class file forces `--depth deep` (`task-builder/SKILL.md:2415`, `:2438`). Everything else is JUDGMENT (J).

| Band | Signals (all J except where cited) |
|---|---|
| LOW | One named folder or file; author can name the files up front; only auto-fix class items (unused imports, zero-reference code, `cleanup.md:111-114`); no exports, fixtures, config, CI or infra paths touched. |
| MEDIUM | One subsystem, several files; some items fall in the approval class (indirect references, exports, fixtures, config, `cleanup.md:118-121`); the author cannot list every file but can name the folder. |
| HIGH | More than one subsystem or whole repo; any `--type files` or `--type all`; target includes CI, infra, secrets or `.dev/` paths (repo `CLAUDE.md:8` makes `.dev/tasks` always-staged); public API or shared interfaces between stories; or the work reads as a structural refactor (HWW:168 sends that through `/task-builder ... --spec`, where a refactor `type:` scores TCS S6=1 and forces `--depth deep`). |

| Scope | LOW | MEDIUM | HIGH |
|---|---|---|---|
| T one-off | OPTIONAL (J): a plain edit does it; `--type imports\|code --safe --interactive` on one folder after a commit | WORTH IT (J): this is the guide's own standalone "tidy a folder" row (HWW:318, `changes_files` yes); `--type code --safe --interactive`, commit first | SKIP as a direct run (J): run `/sc:cleanup-audit <path> --pass all` first, then `/sc:cleanup` only on the audit's "Immediate" paths; a structural job is a feature (HWW:168) |
| B bug fix | SKIP (J) | SKIP (J) | SKIP (J). A bug fix should not carry unrelated deletions (diff widens, review gets harder); clean up in a separate commit or task after the fix merges. |
| S single story | OPTIONAL (J): dead code or imports the story created, `--type code --safe --interactive` on the story's files, before the commit | OPTIONAL (J): same flags; commit first | SKIP (J): too big to ride inside a story; split it out as its own story or task |
| F multi-story feature | OPTIONAL (J) | WORTH IT (J): after the last story, audit then cleanup of the feature's folder, `--type code --safe --interactive`, as its own commit | SKIP direct run (J): audit first; execute via a task package (`/task-builder`) so each deletion is a checklist item with review |
| R multi-feature release | OPTIONAL (J) | WORTH IT (J): `audit-skill:19` lists "pre-release cleanup to reduce attack surface and deployment weight" as a trigger; audit `--pass all`, then cleanup of "Immediate" items; do it early enough to merge and re-test before the release is sealed | SKIP direct run (J): audit report feeds a task package; never an unattended `--type all` at release time |
| N new product | SKIP (J): greenfield, nothing to clean | SKIP (J) | OPTIONAL (J), late only: one audit plus guarded cleanup before first release; never early |

Cells with no `(J)` marker: none. This matrix is judgment built on cited guard rails; the only file-stated cell content is the flag set in the T/MEDIUM cell, which copies HWW:318.

##### 4. Choose this or the neighbour

**`/sc:cleanup-audit` then `/sc:cleanup` (the pair).** The audit is read-only (`audit-cmd:103-110`) and its own "Next Step" says to use `/sc:cleanup` to execute safe recommendations, then `/sc:test`, then `/sc:git` (`audit-cmd:119`, `audit-skill:171`). The guide's cleanup row orders it: audit (`--pass all`), commit, cleanup, improve, review `git diff` (HWW:318, HWW:159-166).

| Signal | Rule (J unless cited) |
|---|---|
| You can name the folder and it is LOW | Skip the audit. Commit, then `/sc:cleanup <folder> --type code --safe --interactive`. The audit costs a Haiku/Sonnet fan-out in waves of 7-8 agents plus a 10% spot-check (`audit-skill:68-69`), and `sc-recommend` warns a large protocol dwarfs a small task (`delegation-vs-native-heuristics.md:50`). |
| You cannot name the files, or scope is repo-wide, or HIGH | Audit first (`delegation-vs-native-heuristics.md:29`, `:40` rate the audit YES for scope above a few files or whole repo). Pass an explicit path and `--pass all`; without `--pass all` it runs only the quick first pass (HWW:161). |
| You want to delete or move WHOLE FILES | Audit first, always (J). Only the audit holds a written evidence bar for DELETE (grep count, CI/Docker/package search, five dynamic-load patterns, successor or transient; `verification-protocol.md:20-25`). `/sc:cleanup` has no equivalent and no rule for whole-file removal (`cleanup.md:109-121`). |
| The audit's report exists | Hand `/sc:cleanup` only the paths in the report's "Immediate (safe, no dependencies)" section (`templates/final-report.md:23-26`) as the `[target]`. There is no input flag for a report (see section 2), so the handoff is manual. Items under "Requires Decision" or "Requires Code Changes" (`final-report.md:28-36`) are not for `/sc:cleanup`: decide or plan them. |

Coverage gap to remember: the audit never sees hidden paths (`.github/`, `.dev/`, `.claude/`) or `_bmad/`, `_bmad-output/`, `_planning-input/` (`audit-skill:54-62`, `repo-inventory.sh:20`). In this repo that is the CI workflows, the task packages and the BMad artifacts. So the audit cannot clear a deletion there, and `/sc:cleanup` has no exclusion list. Do not point `/sc:cleanup` at those paths (J).

**`/sc:improve`.** Same sibling pattern: both are the guide's only exception to the 5-edit limit (HWW:22), both need a commit first and a read of `git diff` (HWW:163-166). Rule: removal of dead code, unused imports, empty blocks, redundant annotations = `/sc:cleanup`; formatting, naming, unused variables, import ordering, simple annotations, performance, maintainability = `/sc:improve` (`improve.md:110-115`, `:22`). They overlap on unused imports (`cleanup.md:111` vs `improve.md:113-114`); run cleanup first (HWW:318 steps 3 then 4) and do not run both on the same files in LOW work (J).

**`/simplify` (built-in).** Diff-scoped: reviews changed code for reuse and simplification and applies fixes; "run before the commit, not after review" (value:156; no file, description from the session skill list). Rule (J): tidying code you just wrote in this branch = `/simplify`; removing dead code that already existed in a folder = `/sc:cleanup`.

**`/sc:analyze`.** Reports only (value:177); its Next Step names `/sc:improve` or `/sc:cleanup` (`analyze.md:111`). Use it when you want a health read on a module before deciding; it is lighter than the audit but gives no deletion evidence.

**Plain edit.** At LOW with named lines (one file, 5 edits or fewer) a plain edit plus the related test is enough (HWW:16, HWW:304). `/sc:cleanup` earns its use only on a folder (HWW:22).

**`/task-builder` + `/task`.** Large or structural refactors are treated as a feature: spec plus `/task-builder ... --spec` (HWW:168; routing row note at HWW:318). Any HIGH cell above goes here, not to a raw `/sc:cleanup`.

##### 6. Expected-step rule

- `/sc:cleanup` is never an expected step at any scope x complexity: the matrix has no REQUIRED cell, and WORTH IT appears only at T/MEDIUM, F/MEDIUM and R/MEDIUM (J). A checker must not flag its absence anywhere. Only the repo's own pipeline steps (spec, tasklist, implement, commit, push) are expected; cleanup is an extra.
- A checker should instead flag unguarded presence (J): a diff that deletes or moves whole tracked files, or touches `.dev/`, `_bmad-output/` or `.github/`, with no commit before it and no `.claude-audit/` report or task-package item behind it, at HIGH or with `--type files|all`. The audit is expected before whole-file deletions at HIGH, not before LOW code-and-import tidying.

Full file for the citation key, the footprint (section 5), the proposals (section 7) and the unverified items (section 8): [command-nuance/sc-cleanup.md](command-nuance/sc-cleanup.md)

#### 6.3.19 /sc:cleanup-audit (Implement)

##### 1. Status and role

- Does: "Multi-pass read-only repository audit producing evidence-backed cleanup recommendations" (`CA:3`). Standalone-invokable, not retired; backing skill exists (`~/.claude/skills/sc-cleanup-audit-protocol/`, plus five `AG:audit-*.md` agents). It names neither `/sc:task` nor `/sc:tasklist`.
- Phase: none of Ryan's five pipelines. It is a hygiene job: step 1 of guide 3.7 and routing row `cleanup` (`HWW:159-161`, `HWW:318`). Its only declared hand-off is "use `/sc:cleanup` to execute safe recommendations, then `/sc:test`, then `/sc:git`" (`CA:119`).
- Overlaps: `/sc:cleanup` (the editor that acts on it), `/sc:analyze` (module health), `/sc:auggie-review` (diff-scoped, "complementary", `auggie-review.md:185`), built-in `/simplify` (changed code only).

##### 2. Flags

Syntax (`CA:31`, `SK:25`): `/sc:cleanup-audit [target-path] [--pass surface|structural|cross-cutting|all] [--batch-size N] [--focus infrastructure|frontend|backend|all]`. Four arguments; the command file and the protocol skill define them identically.

| Flag | Values | Default | What it changes | Worth using when | Avoid when |
|---|---|---|---|---|---|
| `target-path` | a directory | `.` whole repo (`CA:36`) | Files enumerated with `git ls-files -- "$TARGET"` (`INV:63`), then the default scope floor is applied (below). Guide: "leave out the path only when you mean the whole repository" (`HWW:161`) | Always give a path for a folder cleanup | Omitting it on a large repo: cost scales with in-scope files |
| `--pass surface` | Pass 1 | The bare command runs Pass 1 only (`CA:53`; `HWW:161`). The Arguments list itself states no default | Quick scan: each file DELETE / REVIEW / KEEP, grep proof for every DELETE (`CA:43`, `pass1:80-86`). Output `.claude-audit/pass1-summary.md` (`CA:53`) | Question is "is there junk here?" Target is LOW or MEDIUM and you only want delete candidates | You need to know whether docs/config are still true, or whether files duplicate each other |
| `--pass structural` | Pass 2 | none | 8-field profile per file; finding types MISPLACED / STALE / STRUCTURAL ISSUE / BROKEN REFS / VERIFIED OK; only files Pass 1 marked KEEP or REVIEW (`pass2:30,51-62`). Highest-value finding: a doc "describes things that don't exist" (`pass2:89`). Command file says it "requires Pass 1 results as input context" (`CA:61`) | Docs, runbooks, configs may have drifted from code (this repo: `docs/operations/*`, `templates/*/README.md`, per `PROJECT_INDEX.md`) | No Pass 1 output exists yet (behaviour undefined, U6); target is a handful of files you can read yourself |
| `--pass cross-cutting` | Pass 3 | none | Compares files across directories; mandatory duplication matrix with overlap % when similar files exist (`pass3:76-87`); receives Pass 1-2 findings and does not re-flag them (`pass3:56`); directories of 50+ files are sampled at 10-15 files (`pass3:59`) | Sprawl: several compose / Dockerfile / deploy scripts / configs (`pass3:62-66`); example flag set `--pass cross-cutting --focus infrastructure` (`CA:66`) | Single small directory (nothing to compare against); Pass 1-2 output absent |
| `--pass all` | Passes 1, 2, 3 in order | none | Quality gate between passes, then a final report: executive summary, prioritized actions, cross-cutting findings, issues registry (`CA:77`, `SK:70`). This is the `mandatory_flags` entry for routing row `cleanup` (`HWW:318`) | MEDIUM or HIGH target, or a pre-release sweep (section 3) | LOW target: three passes, a validator and a consolidator for at most one Pass-1 batch of files (J) |
| `--batch-size N` | integer | 50 surface, 25 structural, 30 cross-cutting (`CA:38`) | Files per agent. Binary assets get grep-only audits at 50-100 per batch (`pass1:63-76`). Each agent has `maxTurns: 60` (`AG:audit-scanner.md:6`) | Lower it when files are long scripts or an agent reports "Remaining / Not Audited" (`batch-report.md:74-76`) | Raising it above defaults: more reads and greps per agent, more unreached files (J). `INV:12` takes a single size, so how one N maps onto three passes under `all` is not defined (U8) |
| `--focus` | `infrastructure`, `frontend`, `backend`, `all` | not stated | "Domain filter for targeted auditing" (`CA:39`). `INV:146-168` groups files into 8 domains (adds tests, documentation, config, assets, other) but the script takes no focus argument (`INV:3`) | Splitting a HIGH target into slices; Pass 3 on infrastructure (`CA:66`) | Expecting to audit only docs, config or tests: no value selects them. Mechanism is not defined (U4) |

Default scope floor, not a flag and not removable (`SK:54-65,103`; `INV:20`): hidden paths (any leading-dot segment), `_bmad/`, `_bmad-output/`, `_planning-input/`, `.claude-audit/`. A project may add regexes with `EXCLUDE: <regex>` lines in `.claude-audit/SCOPE.md`; it can tighten, never loosen.

Does not exist (a checker or engineer might assume them):

| Assumed flag | Fact |
|---|---|
| `--depth` | Absent from both files. Depth is chosen by `--pass` |
| `--resume` | Absent. Resume is described as automatic via `progress.json` (`SK:76,100`), but `sc-crash-recovery` says audits "are not designed for fine-grained resume": re-invoke the skill (`~/.claude/skills/sc-crash-recovery/refs/pipelines.md:203-205`) |
| `--fix` / `--apply` / `--dry-run` / `--preview` | Absent. The command is read-only by design (`CA:103-110`). `--type`, `--safe`, `--aggressive`, `--interactive` belong to `/sc:cleanup` (`CL:22`) |
| `--output` / `--out-dir` | Absent. Output location is fixed: `.claude-audit/` (`CA:112`) |
| `--exclude` / `--include-hidden` | Absent. Only `SCOPE.md` EXCLUDE lines; hidden and BMAD paths cannot be switched on (`SK:64,103`) |
| `--model` | Absent. Pass 1 "Haiku", Passes 2-3 "Sonnet" per prose (`SK:68`), but see U1 |

##### 3. Scope x complexity matrix

This command does not vary with the complexity of a delivery task. It varies with the size and risk of the TARGET folder. No file rates it by scope (T/B/S/F/R/N), so every cell below is judgment, labelled `(J)`, derived from the triggers in `SK:16-20` and the cleanup route in `HWW:157-168,318`.

###### Size facts (what "repository size" means for this command)

| Fact | Value | Source |
|---|---|---|
| Unit of work | one Pass-1 batch = 50 files; one agent wave = 7-8 batches, so about 350-400 files per wave | `CA:38`, `SK:68` |
| Size that matters | files left after the scope floor, not repo size. The command prints "Total tracked files" and "In-scope after default excludes" itself (`CA:15-16`), but both are repo-wide, not target-scoped | `CA:15-16` |
| Designed-for scale | Pass 3 depth plan budgets about 1,400 files (~200 deep, ~800 medium, ~400 light) | `pass3:70-74` |
| This repo (observed 2026-10-27) | 5,152 tracked files, 277 in scope (5.4%), 73 MB on disk excluding `.git` | `git ls-files`, `du` |
| Excluded here by the floor | `.dev` 3,936; `.claude` 263; `_bmad-output` 261; `.agents` 237; `.github` 128; `.opencode` 20; `_bmad` 17 | `git ls-files` + `INV:20` |
| In scope here by top folder | `templates` 168; `claudedocs` 31; `docs` 29; `ci-timing` 14; `scripts` 12; `orca-build` 9; `artifacts` 6; `openspec` 2; `install` 1; `SECURITY.md` 1 | `git ls-files` |
| Protocol load cost | `SKILL.md` 10,202 bytes + command file 5,126 bytes. `sc-recommend` says do not invoke a skill whose protocol is over ~2,000 tokens for a task under ~500 tokens of work, and names `/sc:cleanup-audit` as one of the large ones | `wc -c`; `delegation-vs-native-heuristics.md:50` |
| Derived agent count, this repo, `--pass all`, defaults | Pass 1: ceil(277/50) = 6 (one wave). Pass 2: at most ceil(277/25) = 12 (two waves; DELETEs drop out, `pass2:30`). Pass 3: at most ceil(277/30) = 10 (it samples, `pass3:58-59`). Upper bound about 28 batch agents plus validators and consolidators | arithmetic from the rows above (J) |
| Derived agent count, LOW target (50 files), `--pass all` | 1 + up to 2 + up to 2 batch agents, plus the same validator and consolidator steps per pass, so overhead is about the size of the work | arithmetic (J) |

Consequence: on this repo the pipeline's own CI (`.github/`, 128 files) and the task ledgers (`.dev/`, 3,936 files) are invisible to the audit by design (`SK:55-62`, `INV:20`). A "whole repo" audit here covers templates, docs and scripts only.

###### Bands (edges are JUDGMENT, anchored on the batch and wave sizes above)

| Band | Definition for this command |
|---|---|
| LOW | 50 in-scope files or fewer in the target (one Pass-1 batch); one domain; you can name every referrer with a grep |
| MEDIUM | About 51-350 in-scope files (2 to ~7 Pass-1 batches, at most one wave); or 2+ domains; or suspected duplicates across directories. This repo as a whole (277) is MEDIUM |
| HIGH | More than ~350 in-scope files (more than one wave); or dynamic loading in play (env-var, string-built imports, plugin registries, glob discovery, config-driven: `dynamic-use-checklist.md:11-118`); or config/compose/deploy sprawl (`pass3:62-66`); or a pre-release sweep with unknown referrers |

###### Matrix

| Scope | LOW | MEDIUM | HIGH |
|---|---|---|---|
| T one-off | SKIP (J) | SKIP (J) | SKIP (J) |
| B bug fix | SKIP (J) | SKIP (J) | SKIP (J) |
| S single story | SKIP (J) | OPTIONAL (J): `<path> --pass surface`, only if the story deletes or moves files and referrers are unknown | OPTIONAL (J): `<slice> --pass all`; a story that needs this is probably mis-sized |
| F multi-story feature | SKIP (J) | OPTIONAL (J): `<path> --pass surface` after merge, when the feature replaced or retired something (`SK:17` post-migration) | WORTH IT (J): `<path> --pass all` as research input to a cleanup or refactor feature spec; a large refactor is treated as a feature (`HWW:168`) |
| R multi-feature release | OPTIONAL (J): `<path> --pass surface` | WORTH IT (J): `--pass all` on the release paths or whole repo (`SK:19` pre-release cleanup) | WORTH IT (J): `--pass all` in slices by path or `--focus` (`verification-protocol.md:86` "cap files per agent... prevent audit the world") |
| N new product | SKIP (J) | SKIP (J) | SKIP (J): greenfield has nothing accumulated; a brownfield port is not N |

Reading rules:
- A job whose whole purpose is tidying (routing row `cleanup`, `HWW:318`) is its own route, outside T..N. Judge it by target band, not by scope.
- B stays SKIP at every band: the audit finds dead, duplicate and misplaced files, not defects. Use `/sc:troubleshoot` (`HWW:311`).
- T stays SKIP: removing unused imports in one file is level 2 (`HWW:16`) or `/sc:cleanup --type imports`.

##### 4. Choose this or the neighbour

###### Audit first, or straight to `/sc:cleanup`?

| Signal | Straight to `/sc:cleanup <path> --type imports\|code --safe --interactive` | Run `/sc:cleanup-audit` first |
|---|---|---|
| Target size | LOW: 50 in-scope files or fewer (J) | MEDIUM or HIGH (section 3) |
| What you want removed | Unused imports, code with zero references, empty blocks, redundant annotations: the things `/sc:cleanup` auto-fixes (`CL:109-114`) | Whole files: delete, move, merge duplicates (the audit's DELETE / MOVE / CONSOLIDATE actions, `verification-protocol.md:9-16`) |
| Who references it | You can name them, or one grep settles it | Unknown referrers; dynamic loading possible (`dynamic-use-checklist.md:9-13`) |
| Doc or config truth | Not in question | Docs or configs may describe things that no longer exist (`pass2:85-90`) |
| Duplication | None suspected | Several similar compose / deploy / config files (`pass3:62-66`) |
| In the scope floor? | Target is hidden or BMad (`.github/`, `.dev/`, `.claude/`, `_bmad*`): the audit cannot see it, so grep by hand | Target is outside the floor |
| Part of a larger refactor | Do not use either as the plan: a large or structural refactor is "a feature": spec plus `/task-builder --spec` (`HWW:168`, `HWW:318` notes). The audit may feed the spec as research | same |

`/sc:cleanup` safety behaviour to know: it prompts the user for anything with "ANY usage path", anything affecting a public API, or when unsure (`CL:123-127`). So skipping the audit does not make small cleanups unsafe; it removes the cross-file evidence.

Hand-off is manual. `/sc:cleanup` usage has no flag that reads an audit report (`CL:22`) and its own flow re-analyses the target (`CL:27-31`). Guide order: audit, commit, cleanup, improve, review `git diff` (`HWW:318`). The audit recommends file-level actions; the guide's step 3 passes `--type code`, while `/sc:cleanup` also offers `--type files|all` (`CL:22`). Which type executes the audit's file moves and deletes is not stated (U10).

###### Other neighbours

| Neighbour | Pick the neighbour when | Pick `/sc:cleanup-audit` when | Cite |
|---|---|---|---|
| `/sc:analyze` | Question is module health: quality, security, performance, architecture (route `module-health`, `--focus <area>`) | Question is which files are dead, duplicate, misplaced, or documented wrongly | `HWW:313`, `HWW:318` (analyze file not read in full) |
| `/sc:auggie-review` | You want a review of the diff or PR before push (route `review-pr`) | You want the whole repo, not a diff. The two are "complementary", never substitutes | `auggie-review.md:185`, `HWW:323` |
| `/simplify` (built-in) | Your own changed code needs reuse and simplification cleanups before commit | Accumulated files you did not just change | session skill list; no file (U12) |
| `/tech-research` | You do not know how the system works or what must change (level 5) | You know the intent (remove dead stuff) and need evidence | `HWW:19` |
| Plain `git grep` then `git rm` | One to a few files; one grep settles referrers | More than that, or any dynamic-loading doubt | `pass1:80-86` sets the same grep-proof standard by hand |
| `/task-builder --spec` + `/task` | Acting on a large audit result (many files, more than one session, must not drift) | The audit itself, the evidence-gathering step | `HWW:18`, `HWW:168` |

##### 6. Expected-step rule

- Delivery work (T, B, S, F, N at any band; R at any band): never count its absence as a skipped step. No pipeline of Ryan's names it, and R is WORTH IT, not REQUIRED (J). Using it where it is overkill (LOW target, `--pass all`) is a cost note, not a violation.
- Cleanup jobs (routing row `cleanup`, `HWW:318`): expected as step 1 when the target is MEDIUM or HIGH (51+ in-scope files, or file-level DELETE / MOVE / CONSOLIDATE planned, or unknown referrers) (J). Flag a possible skip only when `/sc:cleanup` runs with `--type files|all` or `--aggressive` on such a target and there is neither a `.claude-audit/` report nor a stated grep proof. On a LOW target, going straight to `/sc:cleanup`, or running `--pass surface` instead of `--pass all`, is legitimate (J), even though the routing table lists `--pass all` as the mandatory flag (U9).

Full file for the citation key, the footprint (section 5), the proposals (section 7) and the unverified items (section 8): [command-nuance/sc-cleanup-audit.md](command-nuance/sc-cleanup-audit.md)

#### 6.3.20 /sc:git (Commit/PR)

##### 1. Status and role
- Does: "Git operations with intelligent commit messages and workflow optimization" (CMD:3). Serves the Commit phase only (CVP section 2.5). Standalone-invokable, not retired; CMD never mentions `/sc:task` or `/sc:tasklist`.
- Overlaps: plain `git` (HWW:272 "Commit with a generated message"), `/sc:pr-submit` (push and PR, not commit; its L2 ceiling leaves edits uncommitted, `skills/sc-pr-submit-protocol/SKILL.md:194`). Callers elsewhere only suggest it as optional: `/sc:implement` ("not gates", `commands/sc/implement.md:140`, `skills/sc-implement-protocol/SKILL.md:171`) and `/sc:cleanup-audit` (`commands/sc/cleanup-audit.md:119`).
- Frontmatter says `complexity: basic`, `mcp-servers: []`, `personas: []` (CMD:5-7). That label describes the command itself, not a task-complexity band.

##### 2. Flags
Usage line: `/sc:git [operation] [args] [--smart-commit] [--interactive]` (CMD:22). No default is stated for any of them. No protocol skill exists, so nothing else defines them.

| Flag / argument | Values | Default | What it changes | Worth using | Avoid |
|---|---|---|---|---|---|
| `[operation]` | `status`, `add`, `commit`, `push`, `pull`, `branch` (CMD:14); `merge <branch>` appears only in an example (CMD:75) | none stated | Selects the git command to run (CMD:29) | `status` for a state summary and next steps (CMD:59-61) | `push`: HWW:229 says never push without approval; CMD does not list push as needing confirmation (CMD:89 covers "destructive operations" only). UNVERIFIED how it behaves |
| `[args]` | free text, e.g. a branch name (CMD:75) | none | Passed to the operation | n/a | n/a |
| `--smart-commit` | boolean | off | "Generates conventional commit message from change analysis" (CMD:66-69, 49) | Many changed files or mixed concerns, want a conventional message | When `.dev/tasks` staging must be exact: CMD says nothing about which files get staged (section 8, U1) |
| `--interactive` | boolean | off | "Guided merge with conflict resolution assistance" (CMD:75-76); only shown with `merge` | Merges with conflicts | Complex merges: CMD:91 says it will not handle merges needing manual intervention |

Does not exist in CMD (people might assume): `--depth`, `--dry-run`, `--amend`, `--no-verify`, `--all` or any path-selection flag, `--push`, `--approve`, any flag that sets staging scope. CMD only promises not to "modify repository configuration without explicit authorization" (CMD:89).

##### 3. Scope x complexity matrix
The command does not vary by complexity: CMD has no complexity input, depth flag, or branching on task size. What varies is HOW OFTEN the commit step happens, and that is Ryan's pipeline rule ("commit regularly", brief ruling 5), not a file-defined threshold. So two matrices.

Matrix A: the command `/sc:git` itself. OPTIONAL everywhere, because plain `git` does the same (HWW:272; CVP line 163).

| Scope | LOW | MEDIUM | HIGH |
|---|---|---|---|
| T one-off | OPTIONAL | OPTIONAL | OPTIONAL |
| B bug fix | OPTIONAL | OPTIONAL | OPTIONAL |
| S single story | OPTIONAL | OPTIONAL | OPTIONAL `--smart-commit` (J: more files, more message value) |
| F multi-story feature | OPTIONAL | OPTIONAL | OPTIONAL `--smart-commit` (J) |
| R multi-feature release | OPTIONAL | OPTIONAL | OPTIONAL `--smart-commit` (J) |
| N new product | OPTIONAL | OPTIONAL | OPTIONAL `--smart-commit` (J) |

Matrix B: the COMMIT STEP (by any means) and its expected cadence. Floor is "at least one commit before push" in every scope that changes files (CVP lines 252-253 list "commit" as a step; HWW:198 "Commit locally"). Everything above the floor is JUDGMENT unless cited.

| Scope | LOW | MEDIUM | HIGH |
|---|---|---|---|
| T | REQUIRED, 1 commit | REQUIRED, 1 commit | n/a (T is by definition small; HWW:22 sends >5 edits or >1 source file to a written plan) |
| B | REQUIRED, 1 commit | REQUIRED, 1 commit; separate commit for the failing test (J) | REQUIRED, commit before risky edits (J), then per fix |
| S | REQUIRED, 1 commit | REQUIRED, 1 commit per ledger milestone (J) | REQUIRED, per phase of the task file (HWW:83 "Commit each phase once it passes") |
| F | REQUIRED, per phase (HWW:83; CVP line 255 "commit per phase") | same | same, plus commit before any `/sc:cleanup` or `/sc:improve` (HWW:163, 22) |
| R | REQUIRED, per phase of each feature (J extension of HWW:83 and CVP line 255) | same | same |
| N | REQUIRED, per phase (CVP line 257 "commit per phase") | same | same |

Band definitions for the commit step (signals from the brief):
- LOW: files nameable up front, 1 session, 1 subsystem, no driving spec, no secrets/permissions/paths. One commit is enough.
- MEDIUM: 2 to 5 files or 2 subsystems, or 1 to 2 sessions, spec exists. Commit at each natural checkpoint (J).
- HIGH: many files or subsystems, 3 or more sessions (so a `/task-builder` task file with phases, which is the HIGH signal in the brief), shared interfaces, risk areas, or drift sensitivity. Commit per phase, because `/task` does not commit (HWW:81) and the phase audit needs a commit reference (HWW:83).

##### 4. Choose this or the neighbour
| Neighbour | Decision rule | Cite |
|---|---|---|
| Plain `git add` / `git commit` | Default for LOW. Use plain `git` whenever the staging set must be exact, in particular when `.dev/tasks` must be staged (REPO-CLAUDE "Development Practices"), because CMD does not define staging. | CMD:14, 49; REPO-CLAUDE |
| `/sc:git commit --smart-commit` | Use when the diff is large or mixed and you want a conventional message. Still stage by hand first (J). | CMD:35, 66-69 |
| `/sc:pr-submit` | Different phase: it opens the PR and runs the review monitor after you have committed and been approved to push. It does not replace the commit step. At L2 it leaves edits in the working tree with no commit. | `skills/sc-pr-submit-protocol/SKILL.md:194`; HWW:198-205 |
| `/sc:implement`, `/task` | Neither commits. `/sc:implement` lists "Auto-commit" under Will Not (`commands/sc/implement.md:131`); `/task` does not commit (HWW:81). So the commit after them is always a separate step the engineer (or `/sc:git`) takes. | as cited |

No complexity-based choice between `/sc:git` and plain `git` is stated anywhere on disk. Any rule beyond the table is JUDGMENT.

##### 6. Expected-step rule
- Never expect the command `/sc:git`; always expect the commit. Count a commit (any tool) as the expected step; absence of `/sc:git` is fine in every cell.
- Expected commits: T and B at least 1; S at least 1 (more if the task file has phases or the work spanned sessions, J); F, R, N at least 1 per task-file phase (HWW:83; CVP lines 255, 257). A single commit for a multi-phase F, R or N branch is a reportable deviation (J). No commit at all before `/sc:pr-submit` on a branch with code changes is a deviation in every scope.

Full file for the citation key, the footprint (section 5), the proposals (section 7) and the unverified items (section 8): [command-nuance/sc-git.md](command-nuance/sc-git.md)

#### 6.3.21 /sc:auggie-review (Commit/PR)

##### 1. Status and role
- **What it does** (CMD:3): "Auggie-powered code review for PRs, local diffs, or file snapshots: narrow bugs + architectural risks + anti-patterns, with auto-posted PR review and optional remediation handoff". Phase: Commit/Push/PR, review before push (GUIDE:201; routing row `review-pr`, GUIDE:323). Its optional remediation chain reaches into Tasklist and Implement (REM:9-12).
- **Standing**: NOT retired; standalone-invokable; explicit invocation only, never from conversational keywords (CMD:15-19). Neither `/sc:task` nor `/sc:tasklist` appears in CMD, SKILL or any ref (grep, 0 hits), so nothing here has to be rerouted.
- **Overlaps**: `/code-review`, `bmad-code-review`, `/security-review`, the PR bot driven by `/sc:pr-submit --monitor 1`, `/sc:swarm-wizard`; CMD:184-185 names `/sc:adversarial` and `/sc:cleanup-audit` as complementary.

##### 2. Flags
One target is mandatory (CMD:25-31); everything else is optional. Rows marked "not in CMD options" are referenced elsewhere but absent from the command's own option table.

| Flag | Values | Default | What it changes (cited) | Worth using | Avoid |
|---|---|---|---|---|---|
| `<PR-num>` / `<PR-URL>` (positional) | PR number or URL | none; STOP if no target resolves (CMD:31) | Target mode `pr`; diff via `gh pr diff` (SKILL:127); the ONLY target mode that can post (SKILL:314); needs authed `gh` (SKILL:38) | Reviewing an open PR where findings should be visible on the PR | Pre-push self-review (use `--diff`); PRs over 5000 diff lines (observed STOP, REV pr-151) |
| `--diff <base>...HEAD` | git range | implicit `origin/<default>...HEAD` "if no target given and a dirty working tree is detected" (CMD:27; SKILL:26-32 does not state this rule) | Target mode `diff`; `git diff <base>...HEAD` (SKILL:127); never posts (no PR). Three-dot range covers COMMITTED changes only (git semantics, not stated in a file) | Pre-push self-review of the branch (GUIDE:201, mandatory flag row GUIDE:323) | Expecting uncommitted edits to be reviewed. CMD:107 heading says "Review uncommitted local changes" but the example uses `...HEAD`; commit first (GUIDE:198 step 1) |
| `--snapshot <path>` | file or directory | none | Target mode `snapshot`: full-content review, no diff (CMD:28, 115-120); file list from `find`, skipping .png/.jpg/.pdf/.lock (SKILL:132); `in_diff` ignored (PRM:132); SEV:93 diff-locality downgrade is PR/diff only, so pre-existing issues keep full severity | Module or subtree audit with no baseline (N scope, new module) | Reviewing a change set (no in-diff scoping) |
| `--focus` | `security,architecture,quality,performance,anti-patterns,tests,docs,all` (CMD:50) | `all` | Which focus blocks go into the Auggie prompt (PRM:92-104). CMD:8 `argument-hint` lists only `security,architecture,quality,performance,all`. A past run used `focus=cicd` (REV pr-43 REVIEW.md header), a value outside both lists; how it was handled: UNVERIFIED | Risk-specific pass (`security`); SKILL:45 recommends it at over 30 files | Using it to clear the over-5000-line STOP: SKILL:383 suggests "rerun with `--focus`", but no file says focus shrinks the measured diff: UNVERIFIED |
| `--depth` | `quick` / `standard` / `deep` (CMD:51) | `standard` | `--max-turns` 8/16/24 (SKILL:171). `deep` only: per-persona Auggie calls (SKILL:192), `auggie-reviewer` agent pass (SKILL:193), `auggie-only/claude-only/both` cross-check (SKILL:224-225), inline comments also for Medium (SKILL:316), MDTM remediation route (SKILL:336; REM:9-12). Quick vs standard: SKILL has no other step that differs (grep "quick": lines 90, 108, 171, 336, 389 only), so CMD:51's "Claude synthesis" for standard is not a separate step: UNVERIFIED. Cost table SKILL:387-391; observed standard Auggie run about 350 s (REV pr-322 audit.log) | See "Depth selection" table in section 3 | `deep` as a default (10-15 min, SKILL:391); `deep` on a diff over 5000 lines (STOP, SKILL:39) |
| `--post-pr` | switch | TRUE when target is a PR (CMD:52) | `gh pr review --comment --body-file REVIEW.md` plus inline `gh api` comments for Critical and High (SKILL:314-327; CMD:52). "No confirmation prompt" (CMD:52). Posts only if PR target AND findings > 0 (SKILL:314); not when every finding failed grounding (SKILL:379). Never `--approve`/`--request-changes` (SKILL:328; CMD:172). Contradiction: SEV:35 says High gets inline comments only at deep; CMD:52 and SKILL:316 say Critical and High at every depth | Deliberately making findings visible on someone's PR | Default use. The posted report quotes real code (SKILL:253-255) and SEV:17 makes hardcoded credentials Critical, which also gets an inline comment (SEV:22): a leaked secret would be copied into a public PR comment. Repo history: CLAUDE.md "Secrets discipline" (PR #57) |
| `--no-post-pr` | switch | off | Report only, nothing sent to GitHub (CMD:53, 176) | Every PR-number run unless public output is the goal; GUIDE:253 and GUIDE:323 name it as the safe form | Nothing; redundant with `--diff`/`--snapshot` because only PR targets post (SKILL:314) |
| `--remediation-offer` | switch | TRUE (CMD:54) | After the report, ONE free-text offer of the five-phase chain (REM:27-61), only if critical + high >= 1 and not already declined this session (REM:18-23; SKILL:333). Chain: `/sc:design` -> `sc:workflow` (`--depth standard --handoff none`, SKILL:338) -> `/sc:reflect --mode pre` -> user-run `/sc:implement` -> `/sc:reflect --mode post`; at `--depth deep`: `task-builder` -> `/task` (SKILL:336; REM:9-12). Never auto-runs (CMD:175) | When you actually want a fix plan (GUIDE:201 "accept only if you want one") | Accepting by reflex: route follows REVIEW depth, not fix size (see section 4) |
| `--no-remediation-offer` | switch | off | Suppresses the offer (CMD:55) | Self-review where you will fix by hand | - |
| `--output-dir` | path | `.dev/reviews/<target-slug>-<timestamp>/` (CMD:56; SKILL:100) | Where REVIEW.md, raw Auggie JSON, `audit.log` go. The default is inside the repo and 140 files under `.dev/reviews/` are tracked by git (`git ls-files`) | A path under `/tmp` when the diff may contain secrets (J) | Default path for a secret-bearing diff, then a bulk `git add` |
| `--auggie-model` | model id | `prism-b` (CMD:57) | SKILL:172 uses `--model "${AUGGIE_MODEL:-prism-b}"` and never names `--auggie-model`; how the flag maps is UNVERIFIED | Rarely | - |
| `--revagent` | `opus`, `sonnet`, `haiku`, `fable` (CMD:58) | unset: reviewer agent keeps its frontmatter model | `model:` on the `auggie-reviewer` Task spawn only (SKILL:193); invalid or missing value STOPs at Wave 0 before anything else (SKILL:83-89); at quick/standard prints a WARN and has no effect (SKILL:90) | `deep` when you want to control reviewer cost or model (J) | At quick/standard (no reviewer runs) |
| `--force` (not in CMD options) | switch | off | Bypasses the over-5000-line STOP (SKILL:138, 383). SKILL:39 scopes that STOP to `--depth deep`; SKILL:138/367/383 state it generally and REV pr-151 hit it at `--depth quick` | Almost never: SKILL:367 says no useful signal at that scale | Using it instead of splitting the diff by feature |
| `--resume <output_dir>` (not in CMD options) | path | none | Resumes the remediation chain from `remediation-state.json` (REM:195-214) | After a closed session mid-chain | Whether the command accepts it: UNVERIFIED |

**Does not exist** (people may assume): `--staged`, `--uncommitted`, `--working-tree` (a `...HEAD` range is committed-only; `bmad-code-review` does take staged/uncommitted, BMCR step-01:26-27); `--comment` (that is the built-in `/code-review` switch; here posting is the default); `--approve` / `--request-changes` (never, CMD:172); `--fix` or any auto-edit (advisory only, CMD:171); `--spec` (no spec input; the prompt carries only PR title and body, PRM:24-26, so it cannot audit acceptance criteria); `--max-findings`; `--model` (use `--auggie-model`); `--monitor` (that is `/sc:pr-submit`).

##### 3. Scope x complexity matrix
**Does this command vary by complexity?** Yes, in three ways: Auggie call count and runtime (chunking at 16-30 files or 1500-5000 lines, SKILL:136-137), depth (turn cap and the deep-only extras), and a hard STOP above 5000 diff lines (SKILL:138). The SKILL numbers are capacity limits for Auggie, not a statement of when a review is worth it. No file ties depth to risk. In this repo the two `deep` runs on record were small (REV pr-266: 6 files, 263 lines, 12 findings; REV pr-43: 12 files, 289 lines, 13 kept), so size did not drive depth there; why deep was chosen is not recorded: UNVERIFIED. A `standard` run on 12 files and 321 lines found 0 issues (REV pr-322).

**Complexity bands for this command** (numbers are SKILL facts; the grouping into bands is JUDGMENT):

| Band | Signals |
|---|---|
| LOW | Fits the single-call band (<= 1500 diff lines OR <= 15 files, SKILL:136); one subsystem; no risk trigger (login, permissions, secrets, user input, file paths: GUIDE:200; infrastructure and env paths: CLAUDE.md secrets section); no shared interface |
| MEDIUM | <= 30 files and <= 5000 lines (SKILL:137, chunked by top-level directory); OR a small diff that touches two or more subsystems, a shared interface, or exactly one risk trigger |
| HIGH | Over 30 files (SKILL:45 WARN) or over 5000 lines (SKILL:138 STOP); OR any risk trigger combined with "must not drift" or several subsystems |

**Matrix** (rating, then flags; every cell is JUDGMENT unless noted, because no file rates this command by scope or complexity; GUIDE:201 and GUIDE:323 list it in the ship path without a size condition). No cell is REQUIRED: `/code-review` already covers bugs at S through R (CV:164) and the PR bot covers the PR (CV:167).

| Scope | LOW | MEDIUM | HIGH |
|---|---|---|---|
| T one-off | SKIP (J) | OPTIONAL (J): `--diff <base>...HEAD --depth quick --focus security`; `/security-review` is the guide's tool for that trigger (GUIDE:200) | N/A: a T cannot be HIGH, GUIDE:22 sends more than one source file to a written plan |
| B bug fix | SKIP (J) | OPTIONAL (J): `--diff <base>...HEAD --depth standard`, when the fix changes shared code | WORTH IT (J): `--diff <base>...HEAD --depth standard --focus <risk area>`; `--depth deep` only for security or data-integrity bugs |
| S single story | OPTIONAL (J): `--diff <base>...HEAD --depth quick` | WORTH IT (J): `--diff <base>...HEAD --depth standard` | WORTH IT (J): `--diff <base>...HEAD --depth deep --focus security,architecture` |
| F multi-story feature | WORTH IT (J): `--depth standard` | WORTH IT (J): `--depth standard`; `deep` if a risk trigger | WORTH IT (J): `--depth deep`, one run per sub-diff; one run over 5000 lines STOPs (observed at `quick`, REV pr-151) |
| R multi-feature release | N/A (J): a multi-feature release inside the single-call band is really F | WORTH IT (J): `--depth standard` on each feature's PR diff plus one on the integration diff | WORTH IT (J) per feature or per PR; the whole release diff will exceed 5000 lines and STOP; use `--snapshot <risky subtree>` for cross-feature structure; avoid `--force` (SKILL:367) |
| N new product | OPTIONAL (J): `--snapshot <module> --depth quick` | WORTH IT (J): `--snapshot <module> --depth standard --focus architecture,quality` | WORTH IT (J): `--snapshot <module> --depth deep --focus security,architecture`, one run per module |

Every cell that uses a PR number instead of `--diff` also needs `--no-post-pr` unless public output is the goal.

**Depth selection by size and risk** (the question asked for this command):

| Situation | `--depth` | Target and post flag | Basis |
|---|---|---|---|
| Pre-push self-review, single-call band, no risk trigger | `quick` (differs from `standard` only by the turn cap, 8 vs 16, SKILL:171) | `--diff origin/<main>...HEAD`; cannot post | GUIDE:201; depth choice J |
| Same size, one risk trigger | `deep` with `--focus security` (add `architecture` for layering) | `--diff`; or PR number with `--no-post-pr` | GUIDE:200; two observed deep runs were small and risky-looking (REV pr-266, pr-43); J |
| 16-30 files or 1500-5000 lines | `standard`; `deep` only with a risk trigger (whether deep per-persona calls multiply per chunk: UNVERIFIED) | `--diff` or PR with `--no-post-pr` | SKILL:137 |
| Over 30 files | split the diff; `--focus` narrows prompts, not size | - | SKILL:45 |
| Over 5000 lines | none works: STOP at `quick` (REV pr-151: 286 files, 32,834 lines, Auggie not run) and at `deep` (SKILL:39). Split the work into per-feature diffs | do not use `--force` | SKILL:138, 367; REV pr-151 REVIEW.md:1-7 |
| Open PR where the author or bot thread should see findings | `standard` | PR number, default posting | CMD:52; the only case where posting is wanted |
| Open PR, findings for your own use | any | PR number with `--no-post-pr` | GUIDE:253, 323 |
| No baseline (new module, audit) | `standard` or `deep` | `--snapshot <path>`; cannot post | CMD:115-120 |

**Posting risk in one place.** The default for a PR number posts a public review and inline comments with no prompt (CMD:52). Posted text includes verbatim code excerpts (SKILL:253-255). A secret in the diff becomes a Critical finding (SEV:17) with an inline comment (SEV:22) quoting the line. The command cannot unpost. The GUIDE-recommended form (`--diff ...`) cannot post at all (SKILL:314).

##### 4. Choose this or the neighbour
None of the neighbours is a strict substitute: they differ in what they read, who sees the output, and whether they edit code.

| Neighbour | Facts from files | Decision rule |
|---|---|---|
| `/code-review` (built-in; description from the session skill list, no file; UNVERIFIED beyond that) | Correctness bugs on the current diff or a PR/branch/path; `--comment` is opt-in for PR posting (skill list). GUIDE:199 puts it first and unconditional; CV:164 rates it REQUIRED for S-R | Always run it first. Add `/sc:auggie-review` when the diff spans two or more subsystems, touches a shared interface, or needs a layering or anti-pattern view (SEV rubric covers architecture, layering, coupling, SEV:70-87). Skip auggie-review when the diff is LOW (single-call band, one subsystem, no risk trigger) (J) |
| `bmad-code-review` (BMad lane) | Three parallel layers (Blind Hunter, Edge Case Hunter, optional Acceptance Auditor, BMCR step-02:16-29); the Acceptance Auditor needs a spec or story file (step-01:66-70); halts for human input at a checkpoint and at several menus (step-01:78-80, step-04:49, 68); writes findings into the story file and syncs `sprint-status.yaml` (step-04:19-32, 83-105); can apply patches itself (step-04:58, 70). Sources of diff: staged, uncommitted, branch, commit range, PR (step-01:26-31); warns above about 3000 lines (step-01:74). Step-03 triage file and `customize.toml` not read: UNVERIFIED | Pick by lane (CV:223): BMad story file in hand -> `bmad-code-review` (it checks acceptance criteria, which `/sc:auggie-review` cannot, PRM:24-26). Task-file lane -> `/code-review` then optionally `/sc:auggie-review`. Do not run both on the same diff as the "one bug review" (CV:234) |
| `/security-review` (built-in; no file) | GUIDE:200: required when login, permissions, secrets, user input, or file paths changed | Risk trigger present -> `/security-review` first; add `/sc:auggie-review --focus security` only on a HIGH diff (J). A secret in the diff is a finding class for auggie-review (SEV:17) but a posting hazard (section 2) |
| `/sc:pr-submit --monitor 1` | Opens the PR and watches the Augment bot (CV:167; GUIDE:205). Not a bug review the author runs | Complementary, not alternative. It is the REQUIRED push step at every scope (CV:167); `/sc:auggie-review` is the optional extra view before it (GUIDE:201 puts the branch review BEFORE push, step 4 before step 5-6) |
| `/sc:swarm-wizard` | Reviewers from other AI model families via a proxy (GUIDE:154). Proxy configured: UNVERIFIED (CV U5) | Only at HIGH risk and only if the proxy is set; not a replacement (J) |
| `/sc:reflect --mode post` | Audits finished work against a plan or spec and classifies deviations (CV:124). `/sc:auggie-review` has no `--spec` flag | Different question. Plan fidelity -> `/sc:reflect`; defects in the code -> a review command. A task file already runs its own reflect (GUIDE:81), so the branch review is not a substitute for it |
| Its own remediation chain vs choosing a tasklist command directly | Route is keyed on the REVIEW `--depth`, not on fix size: `quick`/`standard` -> `/sc:workflow` (`--depth standard --handoff none`, SKILL:338) + `/sc:implement`; `deep` -> `task-builder` + `/task` (REM:9-12; SKILL:336) | The offer ignores the validated rule (VF Verdict 1: multi-story feature minimum is `/task-builder` + `/task`; `/sc:workflow` + `/sc:implement` is not eligible for F). So: accept the offer as written only when fixes are a few files and one or two sessions. When the findings need many files or several sessions, decline, then run `/task-builder` yourself with `--spec <REVIEW.md or remediation-spec.md>` (the offer also accepts "start at Phase B using existing spec", REM:57-58). Neither `/sc:task` nor `/sc:tasklist` is in the chain |
| `/sc:troubleshoot` | Bug diagnosis with REPORT.md (CV:175). Not in this command's chain | A single failing behaviour found by the review -> `/sc:troubleshoot`; a list of findings -> the remediation offer (J) |

**Checker note on lanes.** A review-driven remediation produces `.dev/tasks/to-do/TASK-WF-*` or `TASK-RF-*` files plus `remediation-spec.md` in the review folder (REM:65-123). A checker that expects the F-scope tasklist to be `/task-builder` must not treat that package as a wrong-lane skip when it descends from a review.

##### 6. Expected-step rule
**Rule: never count absence as a skipped step; count presence as valid extra review.** The command is not in Ryan's pipelines (brief ruling 5), CV:166 rates it WORTH IT and not REQUIRED, and GUIDE:201 lists it as step 4 of the `review-pr` row without a size condition. By scope x complexity (J, from section 3):

| Situation | Checker treatment |
|---|---|
| T, B at LOW or MEDIUM; S at LOW | Absence is fine. Do not look for it |
| S MEDIUM/HIGH, F, R, N | Absence is fine for the pipeline check. A checker MAY log "no extra branch review" as informational if `/code-review` is also absent, because then no review of any kind is visible (REQUIRED is `/code-review`, CV:164) |
| Any scope, HIGH complexity with a risk trigger (secrets, permissions, user input, paths) | Absence of `/security-review` is the thing to look at, not absence of this command (GUIDE:200) |
| Over 5000 diff lines | Absence is expected: the command STOPs (SKILL:138). A `REVIEW.md` with "Status: Failed" (observed REV pr-151) is not a completed review |
| Review-driven remediation present (`remediation-spec.md` in a review folder, then a `TASK-WF-*` or task-builder file) | Valid path. Do not flag a `/sc:workflow` plan here as the wrong lane for F (section 4) |

**Posting is the only presence to inspect.** If the checker can see GitHub, a `/sc:auggie-review` review on a PR is allowed but should be read together with the repo secrets rule (CLAUDE.md "Secrets discipline"): the default posts without confirmation (CMD:52). Recommend the checker record "posted" vs "local" informationally and not score either.

Full file for the citation key, the footprint (section 5), the proposals (section 7) and the unverified items (section 8): [command-nuance/sc-auggie-review.md](command-nuance/sc-auggie-review.md)

#### 6.3.22 /sc:pr-submit (Commit/PR)

##### 1. Status and role
- Does: "Open a PR on the fork and arm an in-session PR-review auto-remediation monitor" (CMD:3). Phase: Commit / Push / PR (the last step of every pipeline). Standalone-invokable, explicit only (CMD:16-20); not retired. It never refers to `/sc:task` or `/sc:tasklist` (grep of CMD and the whole skill folder: no hit).
- Overlaps: `/sc:auggie-review` (sibling; pr-submit also calls it once as a decline fallback, SKILL:196), `/sc:troubleshoot` (called per verified finding, CMD:90), `/code-review` / `bmad-code-review` (local review before the PR), plain `gh pr create` (identical to `--monitor 0` on GitHub).
- Correction to the brief's wording "push with `/sc:pr-submit`": the command OPENS the PR (SKILL:189). It does not push the engineer's branch; the only push it can make is a remediation push at `--monitor 3` (SKILL:195). HOW-WE-WORK has the engineer push first, then run it (`HOW-WE-WORK.md:202-204`).

##### 2. Flags
###### 2a. The `--monitor` levels: what each does to code, repo, GitHub, disk

`--monitor` is a capability ceiling on ONE state machine, compared at three gates (arm >= 1, edit >= 2, push >= 3) plus one override (`needs_human_decision` halts at any level) (SKILL:26-27; `refs/state-machine.md:58-81`; `fsm.py:139-146`). Default is 2 (CMD:47; `fsm.py:30`). HOW-WE-WORK says "always pass `--monitor 1`" (`HOW-WE-WORK.md:254`).

| Level | What it does (cited) | Product code | Local git | GitHub | Disk |
|---|---|---|---|---|---|
| 0 | Opens the PR on the origin repo and returns; FSM never leaves idle; no polling, no CI wait (SKILL:189, SKILL:198; `refs/state-machine.md:23-25`) | untouched | untouched | PR only | none documented: the run log is initialised in Wave 1, an L1+ wave (SKILL:190; U2) |
| 1 | L0 + arms; polls for the Augment review; re-grades; verifies each finding with the read-only `evidence-validator`; diagnoses via `/sc:troubleshoot`; PROPOSES "fix these? y/n" and applies NO edits; then waits on CI (SKILL:190-193, 198; `fsm.py:41`) | untouched | untouched | PR only (polls are reads: `scripts/poll-augment-review.sh`, `scripts/poll-ci-checks.sh`) | run log + per-round dirs (see 2c); troubleshoot output (U4) |
| 2 (default) | L1 + the skill itself applies the diagnosed edits in the working tree, runs the validation gates, then HALTS before push: "no commit, no push, no reply" (SKILL:194; `refs/state-machine.md:83-94`) | EDITED in working tree | dirty tree, nothing committed | PR only, except possibly the oversized-PR fallback report (U6) | as L1 |
| 3 | L2 + commit/push to the PR head branch, reply on each finding thread, resolve it, post the `auggie review` re-trigger comment, re-poll; up to `--max-rounds` pushes; one silence re-request (SKILL:195, 198; `refs/thread-reply.md`; `refs/review-retrigger.md:24-35`) | EDITED and PUSHED | commits created (mechanism: U1) | commits on the branch, replies, resolved threads, trigger comments, summary comment | as L1 |

Push gate at L3 (all five must hold, recorded in a write-ahead `push_decision` event): ordinal >= 3; validation green; no `needs_human_decision`; `round_counter < max_rounds`; at least one applied edit (`refs/state-machine.md:145-164`). The first push of a run needs `--yes` or an interactive confirm unless non-interactive (`refs/state-machine.md:155-159`). Never pushes to an upstream parent or the default/protected branch (SKILL:225).

Time cost, derived (U13): the attended monitor blocks the session. At L1 the Augment wait and the CI wait each get a fresh `--timeout` clock (SKILL:198), so the worst case is about 2 x `--timeout` (default 20 minutes); each L3 cycle adds another re-review wait.

###### 2b. Flags

| Flag | Values | Default | What it changes | Worth using | Avoid |
|---|---|---|---|---|---|
| `--monitor` | 0, 1, 2, 3 | 2 | The ceiling above (CMD:47; `fsm.py:75-77` rejects anything else) | 1 per the guide; 0 when the Augment app is not on the repo (`HOW-WE-WORK.md:205`) | 2 and 3 in this repo: see 2a and U5 (validation gates cannot run as written) |
| `--max-rounds` | int 0..5 | 2 | Cap on remediation cycles; `>= max_rounds` halts (`refs/loop-guard.md:10-28`); parser rejects >5 and <0 (`fsm.py:114-117`) | Only at L3 | Setting it at L0-L2: the counter ticks only at the re-review edge, which exists only after an L3 push (derived from `refs/loop-guard.md:22-23`, SKILL:195) |
| `--poll-interval` | seconds >= 30 | 30 | Sleep between polls; <30 is rejected, not rounded (SKILL:138; `fsm.py:110`) | 60 for long CI (all 8 observed runs used 60) | below 30 (rejected) |
| `--timeout` | seconds | 600 | Per-wait wall clock; the Augment wait and the CI wait each start a fresh clock (SKILL:139, 198). CI "has run longer than 600s" (SKILL:139; `refs/ci-poll.md:32`) | Size to the full CI run; 3600 and 7200 were used in the 8 observed runs | Leaving 600 when CI is a long matrix: ends `terminal_timeout` |
| `--silence-timeout` | seconds >= 30 | 300 | Window with no Augment activity before `terminal_augment_no_response`; clamped to `--timeout` (`fsm.py:112,123`). Only L3 may poke once (`refs/review-retrigger.md:30-35`) | Default | n/a |
| `--base` | branch | repo default branch | PR base (CMD:52) | Only when not targeting the default | n/a |
| `--head` | branch | none | PR head (CMD:53) | Always give it | n/a |
| `--title` / `--body` | text | none | PR title / body (CMD:54) | Always: the PR text is the one thing a checker reads on GitHub at L0/L1 | n/a |
| `--output-dir` | path | `<cwd>/.dev/pr-monitor/pr-<N>-<YYYYMMDDHHMMSS>/` | Where the run log and artifacts go; overrides the default entirely (CMD:55; `run_log.py:282-295`) | When the run log must sit next to a task package | Assuming the default path: 8 of 8 observed logs used an explicit dir (see 2c) |
| `--resume` | path to `monitor-run-<N>.jsonl` | none | Rebuild state from the write-ahead log (CMD:56; SKILL:141) | After a crash or closed session | Expecting the monitor to survive a closed session by itself: it is attended and dies with the session (SKILL:33-35) |
| `--yes` | flag | off | First-push confirm bypass at L3 (`refs/state-machine.md:155-159`; `fsm.py:97`) | n/a | NOT in CMD's argument-hint or Options table, and not in SKILL's Required Input: it exists only in the core parser and one ref (U9) |

**Does not exist** (people may assume): `--fix` and `--depth` on this command (it only hands `--fix` / `--depth deep --fix` to troubleshoot and never `--depth quick --fix`, CMD:85, `refs/severity-routing.md:71-74`); `--repo` (repo is computed from origin and pinned internally, CMD:83; only the helper scripts take `--repo`); `--pr` (CMD:27 and SKILL:136 accept "an existing PR number" but name no flag for it, U10); `--draft`, `--reviewer`, `--label` (not in CMD:8); `--no-post-pr` (belongs to `/sc:auggie-review`; the fallback passes `--depth quick --remediation-offer` and must NOT pass `--no-post-pr`, `refs/auggie-fallback.md:28-35`); any daemon or background option (CMD:85, SKILL:33).

###### 2c. Run log: where it lands (the earlier UNVERIFIED item)

- Default: `<cwd>/.dev/pr-monitor/pr-<N>-<YYYYMMDDHHMMSS>/monitor-run-<N>.jsonl`, with `state.snapshot.json` beside it and `validation/round-<N>/`, `troubleshoot/round-<N>/` below (`run_log.py:77-82,285,295,299-300`; `refs/loop-guard.md:61-80`). `cwd` is the directory the command is run from, so in a worktree it is the worktree root (`run_log.py:287-289`). VERIFIED from source, not from a live default run: no `.dev/pr-monitor/pr-*` directory exists anywhere under `/home/coder/workspaces`.
- `--output-dir` replaces the whole default (`run_log.py:289-291`). The 8 real logs sit in `<plan-dir>/pr-monitor/monitor-run-<N>.jsonl` (plan dirs `closeout`, `i263`, `i269`, `cd-ci-exclude`, `orca-worktree-root`, ...), so a checker must glob `**/monitor-run-*.jsonl`, not rely on the default.
- Those 8 logs do NOT match the documented schema: they use key `event` (documented: `event_type`) and have no `schema_version`, `event_id` or `run_id` (grep count 0 in two of them; `refs/loop-guard.md:98-100`). A core `RunLog` writes `schema_version`/`event_id`/`event_type` (seen in a unit-test log, `/tmp/pytest-of-coder/pytest-21/test_rereview_count_and_auggie0/monitor-run-99.jsonl`). So the observed logs were written by hand or by a model following the skill loosely (U8). A checker should read a minimal common core: an `armed` line carrying `monitor`, and a last line whose `status` (or `event_type`) starts with `terminal`.
- Git status of the log: in this worktree `git check-ignore` on a default-shaped path returns not ignored, so a default log would show as untracked; `.dev/pr-monitor/detection-contract.locked.md` IS tracked here (commit `6a8e33f8`) although SKILL:190 calls it a gitignored override. `/home/coder/workspaces/IronClaude/.gitignore:246` ignores the whole `.dev/pr-monitor/`. The observed logs in `/home/coder/workspaces/Coder` are tracked (`git ls-files` lists them). CLAUDE.md requires `.dev/tasks/` staged; it says nothing about `.dev/pr-monitor/` or `.dev/plans/`.

##### 3. Scope x complexity matrix
The command does not change WHETHER it runs with complexity: it is the PR step at every scope (existing table rates it REQUIRED in all six). Complexity changes the flag set, mainly `--timeout`, and what to expect from the bot. No file gives a threshold for these bands; all three are JUDGMENT, built from signals that do appear in files.

| Band | Signals (one line) |
|---|---|
| LOW (J) | Few files, one subsystem, no secrets, permissions, user input, paths or infra; CI fits the 600 s default timeout (SKILL:139) |
| MEDIUM (J) | Several files or one large subsystem; CI matrix can exceed 600 s (SKILL:139, `refs/ci-poll.md:32`) |
| HIGH (J) | Multi-subsystem or large diff, where Augment can decline an "abnormally large" PR and trigger the one-shot auggie fallback (`refs/auggie-fallback.md:13-19`, SKILL:196); OR risk paths (secrets, permissions, infra), given this repo's secrets incident (`CLAUDE.md` Secrets discipline) |

| Scope | LOW | MEDIUM | HIGH |
|---|---|---|---|
| T one-off | REQUIRED `--monitor 1` (J; `--monitor 0` is fine, see rule below) | REQUIRED `--monitor 1 --timeout <CI length>` (J) | REQUIRED `--monitor 1` only when risk-driven (J); size-driven HIGH is N/A, re-scope to B or S |
| B bug fix | REQUIRED `--monitor 1` (J) | REQUIRED `--monitor 1 --timeout <CI length>` (J) | REQUIRED `--monitor 1 --timeout <CI length>` (J) |
| S single story | REQUIRED `--monitor 1` (J) | REQUIRED `--monitor 1 --timeout <CI length>` (J) | REQUIRED `--monitor 1 --timeout <CI length>`; `/sc:auggie-review --no-post-pr` first (J) |
| F multi-story feature | N/A (J; a feature with several stories is not LOW) | REQUIRED `--monitor 1 --timeout <CI length>` (J) | REQUIRED `--monitor 1 --timeout 3600` or more (J; 3600 and 7200 were used in observed runs); expect a decline and fallback (J) |
| R multi-feature release | N/A (J) | REQUIRED `--monitor 1 --timeout <CI length>` (J) | REQUIRED `--monitor 1 --timeout 3600` or more (J); expect decline and fallback (J) |
| N new product | N/A (J) | REQUIRED `--monitor 1 --timeout <CI length>` (J; first PR small scaffold) | REQUIRED `--monitor 1 --timeout 3600` or more (J); or `--monitor 0` if the Augment app is not yet on the new repo (`HOW-WE-WORK.md:205`) |

Level choice, all scopes and bands:

| Level | Rating | Why |
|---|---|---|
| `--monitor 0` | OPTIONAL | Guide's own fallback when the app is absent or unsure (`HOW-WE-WORK.md:205`); equal to a plain PR on GitHub |
| `--monitor 1` | REQUIRED as the baseline | Guide: "Always pass `--monitor 1`" (`HOW-WE-WORK.md:254`, step 6 at :204) |
| `--monitor 2` | SKIP (J) | It is the command default, so omitting the flag silently edits code (`HOW-WE-WORK.md:254`); leaves an uncommitted dirty tree; validation gates are repo-specific (U5) |
| `--monitor 3` | SKIP (J) | Autonomous push, reply, resolve on the engineer's identity; the guide never recommends it. Observed use was 8 of 8 runs at `monitor` 3 in `/home/coder/workspaces/Coder` (see 5), so the guide is not what happens in practice |

Flag by complexity: `--timeout` grows with MEDIUM and HIGH (size to CI, not to the diff). `--poll-interval` 60 for MEDIUM/HIGH (J; observed practice). `--max-rounds` and `--silence-timeout` matter only at L3, so they are irrelevant at the recommended level. `--base` only for a non-default target. `--output-dir` only when a checker or task package needs the log in a known place.

##### 4. Choose this or the neighbour
| Neighbour | Decision rule by signal | Cited |
|---|---|---|
| plain `gh pr create` / web UI | Same as `--monitor 0` on GitHub. Prefer `/sc:pr-submit` because it pins `--repo` to origin and halts on a misrouted PR (a CLI that defaulted to an upstream parent). Plain `gh` is acceptable when the engineer only wants a PR and no monitor | CMD:83; SKILL:143-146, 189 |
| `/sc:auggie-review` | Different timing. auggie-review runs BEFORE the PR on the local diff (`--diff origin/<main>...HEAD --no-post-pr`); pr-submit runs AFTER the PR exists and waits for the Augment App. For HIGH complexity (large diff) run auggie-review first, because the App may decline an oversized PR. pr-submit calls auggie-review itself once, only on a decline, and only described for L2+ (L1: U3) | `HOW-WE-WORK.md:201`; SKILL:196; `refs/auggie-fallback.md` |
| `/code-review`, `bmad-code-review` | Not replaced. They run locally before the push; pr-submit checks the bot's findings after. `HOW-WE-WORK.md:198-205` lists code-review (step 2) before pr-submit (step 6) | `HOW-WE-WORK.md:198-205` |
| `/sc:troubleshoot` | pr-submit calls it per VERIFIED finding at L1+ for diagnosis; the engineer does not run troubleshoot on bot findings by hand. For a bug that did not come from a PR review, use troubleshoot directly (pipeline "bugs and issues via /sc:troubleshoot") | `refs/troubleshoot-dispatch.md:9-24`; brief ruling 5 |
| `/sc:git` | `/sc:git` commits. pr-submit commits only at L3 (mechanism U1) and never at L0-L2 | SKILL:194-195 |
| `/sc:task`, `/sc:tasklist` | Retired. No relation: pr-submit never calls either (no grep hit) | grep of CMD and skill folder |

##### 6. Expected-step rule
- Expected: exactly once per branch that is shipped, as the last step of the pipeline, at every scope and band (existing table: REQUIRED in all six scopes; unchanged by complexity, only the flags change). Count it as done when a PR exists for the branch AND the engineer either ran the command or the PR is equivalent to `--monitor 0` (plain `gh pr create` or the web UI). Because `--monitor 0` and `--monitor 1` leave no GitHub footprint beyond the PR (section 5), the checker should NOT flag a missing run log or a missing monitor when a PR exists (J).
- Absence is fine: nothing is shipped yet (local-only work); the Augment app is not installed so `--monitor 0` is used (`HOW-WE-WORK.md:205`); a PR opened through the UI. Not skipped steps: `terminal_timeout`, `terminal_augment_no_response`, `halt_before_push`, `proposed` are outcomes, not omissions (SKILL:159). Worth a separate "deviates from guide" note, not a skipped-step flag: `--monitor 2` or `3` (guide says 1, `HOW-WE-WORK.md:254`).

Full file for the citation key, the footprint (section 5), the proposals (section 7) and the unverified items (section 8): [command-nuance/sc-pr-submit.md](command-nuance/sc-pr-submit.md)

#### 6.3.23 /sc:troubleshoot (Bug fix)

##### 1. Status and role
- Does: "Tiered debugging": Tier 1 triage, auto-escalation to parallel hypothesis agents plus adversarial fix debate (Tier 2), opt-in remediation chain (Tier 3) (CMD:3). It diagnoses and writes a report; it never edits code (CMD:196-204).
- Phase: bug fix / troubleshoot (Ryan's pipeline step 5; VAL:175). Standalone-invokable, not retired. Backing skill exists: `skills/sc-troubleshoot-protocol/`. Also called by others: `/sc:pr-submit` Wave 4 (`skills/sc-pr-submit-protocol/SKILL.md:193`) and the retired `/sc:task` (`skills/sc-task-protocol/SKILL.md:217`, with `--caller task-unified`).
- Overlaps: `bmad-investigate`, `/sc:analyze`, `/tech-research`, a plain failing test plus edit (proposed one-off minimum). Tier 3 hands off to `/sc:workflow` + `/sc:implement` (default) or `/task-builder` + `/task` (`--fix --depth deep`) (CMD:54). It does not call `/sc:task` or `/sc:tasklist` itself; only the retired `/sc:task` calls it.

##### 2. Flags
Required input: an issue description or `--scope`; STOP if neither (CMD:26-31). `--depth deep` with a description under 10 words and no `--scope` is also a STOP (CMD:33).

| Flag | Values | Default | What it changes | Worth using | Avoid |
|---|---|---|---|---|---|
| `--type` | `bug` `build` `performance` `deployment` `security` `test` | auto-detect from keywords (SKILL:127-133) | Picks the Tier 2 agent set (SKILL:353-360). `security` raises the stop bar to 0.95 (refs/escalation-rubric:68) and forces "non-trivial" (refs/diagnosability-audit:180). `performance` adds +1 to the complexity gate (refs/diagnosability-audit:174) | Always when the kind is clear; the guide's routing row lists `--type <kind>` as mandatory (HWW:311) | Do not force it when the symptom is ambiguous; unset keeps all specialties open (SKILL:133) |
| `--depth` | `quick` `standard` `deep` | `standard` | `quick`: stop after Tier 1 (CMD:51). `standard`: escalate by rubric (refs/escalation-rubric:63-73). `deep`: always Tier 2 after Tier 1 (refs/escalation-rubric:60-61); with `--fix` it also picks the task-file route (CMD:51) | `quick` for a named cause you want confirmed fast. `deep` when a standard run said the cause is not confirmed (HWW:134) | `quick` with `--fix` is a STOP (CMD:51). `quick` does not skip the doc and diagnosability waves, which are "always" (SKILL:103-104). `deep` on a vague one-liner is a STOP |
| `--scope` | file, directory, or symbol | none | Narrows auggie/serena queries (CMD:52); names the failing component (SKILL:251); more than 2 files adds +1 to the complexity gate (refs/diagnosability-audit:175) | When you can name the file or symbol | A wrong scope anchors retrieval on the wrong code (J) |
| `--no-escalate` | flag | false | Stop at Tier 1 whatever the confidence (CMD:53). Also turns the Wave 1.6 hard-stop into a warning (SKILL:271, 617). Beats `--depth deep` by rule order (refs/escalation-rubric:56-61) | Known-cause bug, one pass wanted | Intermittent, security, production incident: it removes the safety net |
| `--fix` | flag | false | After a `success` report only, offers Tier 3 (SKILL:553). Plain `--fix` = plan route: `/sc:workflow --depth standard --handoff none`, then you run `/sc:implement` (SKILL:561-563). `--fix --depth deep` = task-file route: `task-builder`, then you run `/task` (SKILL:565-568). Never edits code, never runs the executor, never commits (CMD:190-192) | Fix is expected to exceed a few files and you want the plan built from the report in one go (HWW:126) | One file plus test (HWW:311). Cause unconfirmed: no offer is made unless status is `success` (SKILL:553). You can skip it and build from the existing report with `/task-builder` (HWW:133) |
| `--models` | `tier:model,...` e.g. `tier1:sonnet,hypothesis:opus` (CMD:55) | agent defaults | Per-tier model override (SKILL:384) | Rarely; cost control | Valid tier keys beyond the two examples: UNVERIFIED |
| `--output-dir` | path | `.dev/troubleshoot/<slug>-<timestamp>/` (CMD:56) | Where REPORT.md and all artifacts go. The 3-round counter stays at `<repo-root>/.dev/troubleshoot/diagnosability-rounds.json` regardless (SKILL:279) | When a caller or checker needs a known path | Paths outside `.dev/troubleshoot/` hide the run from a checker that scans it |
| `--no-doc-discovery` | flag | false | Skips Wave 1.5 doc grounding; skip recorded in Grounding Gaps (CMD:57; SKILL:496). `Behavior is documented` becomes `n/a` (refs/report-template:18) | Repo with no docs, or symptom already grounded | Otherwise: the "do not regress documented behavior" guard (CMD:184) loses its input |
| `--no-mcp` | flag | false | Native tools only; Tier 1 quality drops, noted in the report (CMD:58) | MCP outage | Otherwise |
| `--context` | file path | none | Reads a caller brief in Wave 0; STOP if unreadable (SKILL:153) | Do not use by hand. Its named consumer is the retired `/sc:task` (CMD:59; `skills/sc-task-protocol/SKILL.md:217`) | Always, as an engineer step |
| `--caller` | name | none | Writes `return-contract.yaml` (CMD:60). Only value named: `task-unified`, from the retired `/sc:task` (SKILL:153, 537) | Do not use by hand | Always, as an engineer step |
| `--no-diagnosability-audit` | flag | false | Skips Wave 1.6; bypass logged in the report header (SKILL:246; refs/report-template:20). In SKILL:125 and the protocol, not in CMD:8 | Known false hard-stop (J) | Intermittent or HIGH bugs, where the audit is the point |
| `--diagnosability-handoff` | flag | false | Packages the instrumentation tasklist as a `/sc:workflow` plan, `--handoff none`; you run `/sc:implement` (refs/diagnosability-audit:243-249). Not in CMD:8 | Intermittent bug that needs instrumentation first (J) | Anything diagnosable from existing evidence |
| `--reset-diagnosability-rounds` | flag | false | Clears the current branch/venue entry of the 3-round cap (SKILL:279). Not in CMD:8 | After the cap, when the venue truly changed (J) | Using it to skip the cap |

Does not exist: `--type incident|production|regression`; `--hotfix`, `--severity`, `--apply` (no flag applies code: CMD:196-204); `--hardening` (auto-triggered by topology, no flag: refs/pipeline-hardening-closure:11); `--validate-task` (mentioned as "a flag like", refs/remediation-handoff:221, defined nowhere); `--depth quick --fix` (STOP); `--handoff implement` is never passed to `/sc:workflow` (SKILL:561, 613).

##### 3. Scope x complexity matrix
This command varies mostly by BUG complexity, only weakly by scope. Scope changes which fix route follows (Tier 3), not whether diagnosis is useful. Bands describe the bug, not the story.

Troubleshoot has its own on-disk complexity formula, separate from task-builder's TCS: the Wave 1.6 gate scores +1 each for `--type performance` or flaky test, scope over 2 files, stack trace over 2 modules, "occasionally/race/intermittent/only in CI/prod" wording, "slow/p99/memory/regression/leak" wording, and a race/stale-state/performance/substituted-primitive cause class; score 0-1 = trivial, 2+ = non-trivial, `--type security` always non-trivial (refs/diagnosability-audit:170-185). The stop bar is calibrated confidence 0.85 (refs/escalation-rubric:63-79). TCS does not apply to this command.

| Band | Bug kind | Signals (cited) |
|---|---|---|
| LOW | Known cause | Exact error with a stack trace ending in your code (verdict `sufficient`, refs/diagnosability-audit:140); gate score 0-1; reproducible; fix fits "one source file plus its test, five edits or fewer" (HWW:16, 131) |
| MEDIUM | Unknown cause, deterministic | Cause not yet named; reproducible; Tier 1 confidence likely under 0.85 so it escalates (refs/escalation-rubric:64); fix expected in "a few files with clear scope" (HWW:132) |
| HIGH | Intermittent, production incident, security, multi-domain | Gate score 2+ or `--type security` (refs/diagnosability-audit:185); triggers `intermittent`, `not_reproducible`, `security_caution`, `multi_domain` (refs/escalation-rubric:65-68); symptom spans over 3 modules, or fix touches over 3 files (refs/triage-checklist:68, 74); fix "larger or riskier" (HWW:133) |

Production incident has no dedicated path in any file. It maps to HIGH with `--type deployment` (keywords "production, deploy, container, env var, service won't start": SKILL:130; agents `devops-architect`, `root-cause-analyst`, `system-architect`: SKILL:359) or the symptom's own type. "only in CI/prod" wording adds +1 (refs/diagnosability-audit:177). Limits: if the production arm cannot be reached, the run records "no repro available: run-site unobservable" (SKILL:189); pasting logs never proves locality (SKILL:186); re-runs need existing authorization (SKILL:182). Expect a `partial` or UNDETERMINED report unless real evidence is supplied (J, from those rules). There is no hotfix or rollback fast path; Risk + Rollback is mandatory only for security and performance fixes (refs/report-template:134).

| Scope | LOW (known cause) | MEDIUM (unknown cause) | HIGH (intermittent / prod incident / security) |
|---|---|---|---|
| T one-off | SKIP (J): plain edit + related test (proposed minimum) | OPTIONAL (J): `--type <kind>` | N/A (J): not a one-off any more; "if unsure choose the heavier one" (HWW:9), treat as B |
| B bug fix | OPTIONAL (J), proposed: failing test + edit may replace it when the test names the line. The guide lists it as step 1 for every bug (HWW:311), so Ryan should confirm. If run: `--type <kind> --depth quick` | REQUIRED: `--type <kind>`, default depth (HWW:311, 134) | REQUIRED: `--type <kind>`, default depth auto-escalates on these signals (refs/escalation-rubric:65-68); add `--depth deep` after an unconfirmed standard run (HWW:134) or up front for security (J). `--fix --depth deep` only if the fix is larger or riskier (HWW:133) |
| S single story | OPTIONAL (J): a failing test or build inside the story; same rule as B-LOW | WORTH IT (J): `--type test` or `build` when the failure blocks the story (VAL:175) | WORTH IT (J): treat as a B-scope detour; do not edit until the report names a cause (HWW:134) |
| F multi-story feature | OPTIONAL (J) | WORTH IT (J): failures across shared interfaces between stories | WORTH IT (J): `--depth deep`; `--fix --depth deep` if the fix is multi-story-sized (CMD:51) |
| R multi-feature release | OPTIONAL (J) | WORTH IT (J): red CI or failed push on a release branch; `--type build` or `deployment` | REQUIRED (J) for a release-blocking failure: `--type deployment`, `--depth deep`. Closest project rule is narrower, secret-scan only: do not merge over a failing P-7 check, "investigate before merging" (project `CLAUDE.md`, Secrets discipline item 3) |
| N new product | SKIP (J) | OPTIONAL (J) | WORTH IT (J) once code exists and the bug is HIGH; no pre-code use |

`--fix` by band (what the files say; the choice rules are (J) unless cited):
- LOW: no `--fix`. Failing test, edit, `/sc:test` (HWW:131; routing row says add `--fix` only when larger or riskier: HWW:311).
- MEDIUM: no `--fix` at step 1 because the cause is unknown and the offer needs a `success` report (SKILL:553). After the report: `/sc:workflow "<fix>" --depth quick` then `/sc:implement` (HWW:132). Note plain `--fix` calls `/sc:workflow` with `--depth standard`, not `quick` (SKILL:561), so it is heavier than the guide's manual route.
- HIGH: `--fix --depth deep` gives the task-file route (CMD:51); or no `--fix` and build from the existing report with `/task-builder` (HWW:133). Task-file template becomes `complex` when the fix touches over 3 files, regression risk is high, or it has a schema, migration or public-API change (refs/remediation-handoff:183-186). Plain `--fix` on a HIGH bug builds a workflow plan, not a task file (CMD:54).

Required before an edit, or is a failing test alone enough (J, anchored where cited):
- Failing test alone is enough (proposed, J) when ALL hold: the test's assertion points at one line you can name; one source file plus its test, five edits or fewer (HWW:16); the test is known to be right (documented or specified behavior); deterministic. Troubleshoot's Tier 1 would re-confirm what the test already shows: a failing test with its assertion is an accepted evidence item (refs/triage-checklist:42), and an executed reproducer scores Runtime check 1.0 (refs/escalation-rubric:18, 43).
- Troubleshoot is needed first when ANY holds: the cause is not named; the test passes sometimes; more than one source file is implicated (HWW:22 hard limit); the test itself may be wrong. That last case is why the command exists beyond a test: it sets `test_is_wrong` and `behavior_is_documented` so automation never "fixes" code to match a bad test or regresses documented behavior (SKILL:49-51, 84-96); a failing test cannot tell you which side is wrong. Also security (asymmetric cost: refs/escalation-rubric:68) and anything where evidence lives outside the repo.

##### 4. Choose this or the neighbour
| Neighbour | Rule | Cite |
|---|---|---|
| Failing test + plain edit (proposed one-off minimum) | Use the test and edit when the cause is named, one source file, five edits or fewer, deterministic. Use troubleshoot when any of those fail, or when the test itself may be wrong | HWW:16, 131, 311; band rule in section 3 (J) |
| `bmad-investigate` | Same job, different lane and output: it takes a ticket ID, log file, diagnostic archive or an existing case file, grades findings Confirmed/Deduced/Hypothesized and writes a resumable case file; it also covers "walk through unfamiliar code". Use it in the BMad lane, or for log-only incidents with no reproducer. Use troubleshoot when you have a reproducer and want a fix proposal and a remediation offer. Running both on one bug is waste | `.claude/skills/bmad-investigate/SKILL.md:3-12`; VAL:176 (J on the split) |
| `/sc:analyze` | No specific symptom: analyze. A specific symptom: troubleshoot | CMD:209 |
| `/tech-research` | Do not yet know how the system works or whether something is feasible: research. A reported bug: troubleshoot | HWW:19; VAL:69 |
| `/sc:brainstorm` | Symptom genuinely ambiguous and you want to scope it first: brainstorm upstream | CMD:213 |
| `/sc:auggie-review`, `/code-review` | Whole diff or PR looking for bugs nobody reported: review. One reported symptom: troubleshoot | CMD:214; HWW:199 |
| Tier 3 `/sc:workflow` + `/sc:implement` vs `/task-builder` + `/task` | Few files, clear scope: workflow route. Larger, riskier, multi-session or must not drift: task-builder route. Per the validated finding, `/sc:workflow` is not the minimum tasklist for a multi-story feature; a bug is smaller, so the guide allows workflow for "a few files with clear scope" | HWW:132-133, 305-306; `validation-feature-task-builder-vs-sc-workflow.md` |
| `/sc:pr-submit` | It dispatches VERIFIED review findings to troubleshoot itself: Medium = `--fix`, High/Critical = `--depth deep --fix`, Low/Nit = report-only, never `--depth quick --fix`. Do not run troubleshoot by hand for those findings | `skills/sc-pr-submit-protocol/refs/troubleshoot-dispatch.md:17-31` |

##### 6. Expected-step rule
- Count `/sc:troubleshoot` as EXPECTED when the work is a bug fix (B, or a bug-fix detour inside S/F/R) AND the cause is not already named by a failing test: the band is MEDIUM or HIGH (unknown cause, intermittent, production or CI-only failure, security, more than one source file implicated). Evidence: a run folder in `.dev/troubleshoot/` dated before the fix commit, or a `/sc:pr-submit` dispatch. For a release-blocking CI or deploy failure (R), expect it (J).
- Its absence is FINE (proposed, J) for LOW: a fix commit that touches one source file plus its test, adds or changes a regression test, with no sign of intermittency. Also fine at T and N. Never expected: `--depth deep`, `--fix`, `--no-escalate`, `--models` and the other optional flags; `--fix` absent is always fine; the executor after `--fix` (`/sc:implement` or `/task`) is absent when the offer was declined (SKILL:570). `/sc:task` and `/sc:tasklist` are never an expected step here.

Full file for the citation key, the footprint (section 5), the proposals (section 7) and the unverified items (section 8): [command-nuance/sc-troubleshoot.md](command-nuance/sc-troubleshoot.md)

#### 6.3.24 /sc:analyze (Bug fix)

##### 1. Status and role
- What it does: "Comprehensive code analysis across quality, security, performance, and architecture domains" (CMD:3, 10). Static only, reports only, changes nothing (CMD:99-100; HOW-WE-WORK.md:144). Frontmatter `category: utility`, `complexity: basic` (CMD:4-5); it names no skill and no agents (CMD:6-7, 40-46), so it runs from its own file (HOW-WE-WORK.md:232).
- Phase: standalone health check of existing code, no symptom, no spec, no diff (troubleshoot.md:209; reflect.md:310). Standalone-invokable, NOT retired (HOW-WE-WORK.md:144, 313). CMD does not mention `/sc:task` or `/sc:tasklist`.
- Overlaps: `/sc:troubleshoot` (has a symptom), `/sc:reflect` (has a spec or diff), `/tech-research`, `/sc:explain`, `/sc:cleanup-audit`, `/code-review`, `/security-review`. Also called by other protocols: `/sc:brainstorm` Wave 2A (sc-brainstorm-protocol/SKILL.md:183) and `/sc:release-split` Part 4 (release-split.md:137; sc-release-split-protocol/SKILL.md:106, 324).

##### 2. Flags
Usage line, the only flag definition anywhere: `/sc:analyze [target] [--focus quality|security|performance|architecture] [--depth quick|deep] [--format text|json|report]` (CMD:22). No protocol skill, so nothing else defines semantics. Every default and every depth meaning below is example-implied only.

| Flag | Values | Default | What it changes (cited) | Worth using | Avoid |
|---|---|---|---|---|---|
| `[target]` | path (file or directory) | Whole project: bare `/sc:analyze` = "multi-domain analysis of entire project" (CMD:60-63). Default is inferred from the example, never stated | Narrows the file discovery step (CMD:27). Path syntax (glob, several paths) not defined: UNVERIFIED | Always. Name the subsystem. HOW-WE-WORK routing row takes `<path>` (HOW-WE-WORK.md:313) | Bare whole-project run: one context, no agent fan-out in CMD:40-46, so coverage of a large repo is unmeasured (J) |
| `--focus` | `quality`, `security`, `performance`, `architecture`: one value per usage line | Omitted = all four domains (inferred from CMD:60-62; not stated) | Selects the domain-specific technique (CMD:50, 66-68, 84). Combining values (`a,b`) is not defined: UNVERIFIED | Always pass one. The team guide makes it a mandatory flag for the module-health row: `1: --focus <area>` (HOW-WE-WORK.md:313) even though CMD marks it optional | Omitting it on a target of more than one subsystem: a diluted pass across four domains |
| `--depth` | `quick`, `deep` ONLY | Not stated | Only by example: `quick` = "rapid assessment ... code smells and maintainability issues" (CMD:84-86); `deep` = "vulnerability assessment with detailed remediation guidance" (CMD:68-71). What work each does is not defined: UNVERIFIED. Callers use `quick`: `--focus quality --depth quick` (sc-brainstorm-protocol/SKILL.md:183). Observed `deep` use: `--focus architecture --depth deep` (.dev/reviews/orca-catalogue-bundle-20260924/01-template-analyze.md:3) | `quick` for one subsystem or a context scan; `deep` for risk areas (auth, secrets, infra) or cross-subsystem architecture | `deep` on a whole-project, all-domain run (cost unknown; J) |
| `--format` | `text`, `json`, `report` | Not stated | Output shape only. `report` is described as "Generates HTML report" (CMD:76-78) while the Output list says "Analysis report" (CMD:103-109): the two do not say the same thing. Where a file is written is not stated, although Write is listed (CMD:46) | `text` for chat reading. `report`/`json` only when someone will keep or parse the file: no consumer found on disk (grep of `~/.claude/commands`, `~/.claude/skills`) | `json` with no parser; a checker cannot rely on any of the three producing a file at a fixed path |

Does NOT exist in CMD (people may assume them):
- `--depth standard` (that value exists on `/sc:troubleshoot`, HOW-WE-WORK.md:125, and `/sc:workflow`; analyze takes only `quick|deep`, CMD:22).
- `--fix`, `--apply`, `--safe`, `--interactive` (analyze must not modify code, CMD:100; `--safe --interactive` belong to `/sc:cleanup` and `/sc:improve`, HOW-WE-WORK.md:164-165).
- `--spec`, `--diff`, `--tasklist`, `--mode` (reflect flags, HOW-WE-WORK.md:309-322; analyze has no spec or diff concept).
- `--type`, `--output`, `--handoff`, `--monitor`, `--no-post-pr`, `--coverage`.
- Comma-listed `--focus`, a `--depth` default, and an output-path flag: not defined.

##### 3. Scope x complexity matrix
Does it vary by complexity? Only in HOW MUCH to point it at, not WHETHER it is a pipeline step. No file makes it required anywhere: HOW-WE-WORK lists it once as an answer to "general health of a module" (HOW-WE-WORK.md:144) and once as a routing row with `changes_files: no` (HOW-WE-WORK.md:313); the callers treat it as optional enrichment (sc-brainstorm-protocol/SKILL.md:183 gives `OR mcp__auggie__codebase-retrieval`; sc-release-split-protocol/SKILL.md:324 gives `or inline verification`).

Band definitions, all (J). The band describes the TARGET being analyzed, not the story. No file gives a threshold for `/sc:analyze`. TCS (task-builder/SKILL.md:2410-2433) sizes a task file for `/sc:reflect --depth` and does NOT apply to analyze; only its counting rule is borrowed here: S1 = distinct files, S2 = distinct subsystems = first 2 path segments (task-builder/SKILL.md:2410-2411). Risk classes: login, permissions, secrets, user input, file paths (HOW-WE-WORK.md:200); this repo adds env/secret paths (CLAUDE.md "Secrets discipline").

| Band | Signals (J) | Flag set (J) |
|---|---|---|
| LOW | Target is 1 subsystem key (S2 = 1), author can name the path up front, no risk class | `<path> --focus <one> --depth quick` |
| MEDIUM | Target spans 2-3 subsystem keys, OR author cannot name the files up front, OR exactly 1 risk class | `<path> --focus <one> --depth quick` first; `--depth deep` only on the subsystem the quick pass flags; one run per `--focus` |
| HIGH | 4+ subsystem keys, OR shared interfaces between stories or features, OR 2+ risk classes, OR infrastructure | `--depth deep`, one run per `--focus` domain per subsystem group. Never one bare whole-project run |

| Scope | LOW | MEDIUM | HIGH |
|---|---|---|---|
| T one-off | SKIP (J). Level 2: one file plus test, change already known (HOW-WE-WORK.md:16, 22); nothing to assess | SKIP (J) | SKIP (J). A risky one-off wants `/security-review` on the diff (HOW-WE-WORK.md:200), not a module health pass |
| B bug fix | SKIP (J). A symptom exists, so `/sc:troubleshoot` (HOW-WE-WORK.md:123-125; troubleshoot.md:209) | SKIP (J) | OPTIONAL (J), after the fix: `<cited path> --focus <domain REPORT.md names> --depth quick`, only if REPORT.md says the cause is a module-wide pattern. Not a bug finder |
| S single story | SKIP (J) | SKIP (J). The context question is `/tech-research` (HOW-WE-WORK.md:95-96, 142) | OPTIONAL (J): `<path> --focus <risk domain> --depth quick` before the story when it touches a risk class in code nobody on the story knows |
| F multi-story feature | SKIP (J) | OPTIONAL (J): `<path> --focus architecture --depth quick` before the spec | WORTH IT (J): `--focus architecture --depth deep` per shared subsystem before `/task-builder --spec`, when `/tech-research` was not run. Observed: `/sc:analyze templates/VSCode-AIDev02 --focus architecture --depth deep` for a feature spec (.dev/reviews/orca-catalogue-bundle-20260924/01-template-analyze.md:3) |
| R multi-feature release (re-rated) | OPTIONAL (J): `--focus architecture --depth quick` on the shared code before release planning | WORTH IT (J): one `--focus architecture` run and one `--focus security` run, `--depth quick`, before the release plan | WORTH IT (J): `--depth deep`; `architecture` per shared subsystem before the plan, `security` on every risk-class subsystem before push. Never REQUIRED: output feeds no downstream step |
| N new product | N/A (J). Greenfield: no code to analyze | SKIP (J). Spec exists, so drift is `/sc:reflect`'s job (reflect.md:310) | OPTIONAL (J): at a milestone, once code exists, `--focus security|performance --depth quick` (domains with no spec); or at the start when the product is built on an existing codebase being ported or replaced |

Where it is useful in R and N (J): R is the first scope with several features sharing subsystems, so a per-domain health read of the shared code before planning and of risk subsystems before push is the cheapest use. N is mostly SKIP because the first useful moment is after code exists, and then a spec exists too.

##### 4. Choose this or the neighbour
| Neighbour | Rule | Source |
|---|---|---|
| `/sc:troubleshoot` | Have a symptom, error or failing test: troubleshoot. No symptom yet: analyze | troubleshoot.md:209; HOW-WE-WORK.md:123-125, 144 |
| `/sc:reflect` | Have a spec, tasklist or diff to compare against: reflect. None of those: analyze | reflect.md:310 |
| `/tech-research` | Question is "how does it work, is it feasible, what must change" and the answer should be options plus a plan: tech-research. Question is "how healthy is this module" with severity-rated findings: analyze. Tech-research runs at its deepest setting by default (HOW-WE-WORK.md:255); analyze's cost is UNVERIFIED | HOW-WE-WORK.md:95-96, 142, 144, 308 |
| `/sc:explain` | Understand what specific code does: explain. Assess its health: analyze | HOW-WE-WORK.md:145 |
| `/sc:cleanup-audit` | Looking for dead code, duplication, files to delete or merge: cleanup-audit (evidence-backed passes). CONFLICT: CMD:111 names `/sc:improve` or `/sc:cleanup` as the next step, while the cleanup routing row starts with `/sc:cleanup-audit` (HOW-WE-WORK.md:318). Follow the routing row | CMD:111; HOW-WE-WORK.md:160-161, 318 |
| `/code-review`, `/security-review`, `/sc:auggie-review` | Review of a pending diff or branch: those. Analyze takes a path, not a diff (CMD:22); it does not review changes | HOW-WE-WORK.md:199-201, 322-323 |
| `/sc:improve`, `/sc:cleanup` | Apply fixes: those. Analyze never modifies code without explicit consent (CMD:100). Commit first, review `git diff` after (HOW-WE-WORK.md:22) | CMD:111 |
| `/sc:brainstorm` (caller) | Wave 2A auto-runs `/sc:analyze <paths> --focus quality --depth quick` when domain is code, architecture or incident and `--no-codebase` is absent, OR auggie retrieval. Not an engineer step | sc-brainstorm-protocol/SKILL.md:183 |
| `/sc:release-split` (caller) | Part 4 "fidelity verification" delegates to `sc:analyze` OR inline verification. MISMATCH: CMD defines no comparison of an output against a source artifact (CMD:93-95), only code analysis in four domains. Do not read this caller as proof analyze checks fidelity | release-split.md:137; sc-release-split-protocol/SKILL.md:106, 324 |
| `/sc:task`, `/sc:tasklist` (retired) | Not referenced by CMD, nor required by it | CMD (whole file) |

##### 6. Expected-step rule
- A checker must NEVER count `/sc:analyze` as an expected step in any scope x complexity cell, including R and N: no file requires it and nothing downstream consumes its output. Its absence is always fine.
- If it does appear (F HIGH, R MEDIUM/HIGH are the likeliest), treat it as an extra. Do NOT let it satisfy a review step (`/code-review`, `/sc:auggie-review`), a validate step, or a spec-trace step (`/sc:reflect`): it reviews no diff and compares nothing to a spec (CMD:22, 93-101).

Full file for the citation key, the footprint (section 5), the proposals (section 7) and the unverified items (section 8): [command-nuance/sc-analyze.md](command-nuance/sc-analyze.md)

#### 6.3.25 /sc:explain (Bug fix)

##### 1. Status and role
- Does: "Provide clear explanations of code, concepts, and system behavior with educational clarity" (CMD:3). Guide level 1, "Ask a question": "An answer. No files change." (HWW:15). Routing row `ask`, `changes_files` = `no` (HWW:303).
- Phase: none in the build pipeline. It is a side tool usable at any point; HWW lists it under "Investigate how something works" (HWW:145). Not retired. Standalone-invokable, and the guide names it directly (HWW:15, 303).
- **No backing protocol skill exists**: `/home/coder/.claude/skills/sc-explain-protocol/` is absent (checked with `ls`). The guide says commands with no skill "run from their own file, so no skill load is expected", naming `/sc:explain` (HWW:232). Overlaps: a plain-English question to Claude (same level, HWW:15), `/sc:analyze`, `/tech-research`, `/sc:document`. It does not refer to `/sc:task` or `/sc:tasklist` anywhere in CMD.
- **Checker rule up front**: guide level 1, changes no files. A checker should never expect it and never penalize it, unless a file says otherwise (none found). Details in sections 5 and 6.

##### 2. Flags
Usage line: `/sc:explain [target] [--level basic|intermediate|advanced] [--format text|examples|interactive] [--context domain]` (CMD:22). The command file defines no defaults for any flag. No flag in the file changes whether files are written.

| Flag / argument | Values | Default | What it changes (cited) | Worth using when | Avoid when |
|---|---|---|---|---|---|
| `[target]` | a file, concept or system name; examples: `authentication.js`, `react-hooks`, `microservices-system`, `jwt-authentication` (CMD:64, 72, 80, 87) | none stated | What gets analysed (Behavioral Flow step 1, CMD:27) | Always; without it the command has nothing to explain (inference, J) | n/a |
| `--level` | `basic`, `intermediate`, `advanced` (CMD:22) | not stated (UNVERIFIED) | Audience level and explanation depth (CMD:28, 54 "Progressive Learning"; examples CMD:64-66, 72-74, 80-81) | Onboarding someone new to a module (`basic`); a design walkthrough for a senior (`advanced`). Both J | Never harmful; picking the wrong level only changes wording |
| `--format` | `text`, `examples`, `interactive` (CMD:22) | not stated (UNVERIFIED) | Presentation shape: "Static content → examples → interactive exploration" (CMD:57). Only `interactive` appears in an example (CMD:80) | `examples` for a usage walkthrough (J) | `interactive`: the file never says what it does or whether it writes anything (UNVERIFIED), so do not rely on it producing a file |
| `--context` | `domain`, free word; the file shows `react` and `security` (CMD:72, 87) | not stated (UNVERIFIED) | `react` routes through Context7 for official docs (CMD:73, 42-43); `security` brings the Security persona (CMD:88, 44) | A framework or security question where official patterns matter | A question about this repo's own code; Context7 only serves library docs (CMD:42, J) |

Does not exist (absent from CMD and no protocol skill to define them; people may assume them):

| Flag | Where people might expect it |
|---|---|
| `--depth` (any value) | exists on `/sc:workflow`, `/sc:troubleshoot`, `/sc:research`; not on `/sc:explain`. Depth here is `--level`. |
| `--output` / `--save` / any output path | the file defines no output location at all |
| `--spec`, `--fix`, `--no-promote`, `--monitor`, `--handoff` | belong to other commands |

Frontmatter note: `complexity: standard` (CMD:5) is a label on the command file, not task-builder's TCS score and not a flag. Do not use it as a complexity signal for a task. There is no `allowed-tools` key (CMD:1-8), so "changes no files" is stated in the guide (HWW:15) and implied by the tool list (CMD:48-50: Read/Grep/Glob, TodoWrite, Task), not enforced by a tool allowlist.

##### 3. Scope x complexity matrix
**It does not vary by scope or complexity.** Its triggers (CMD:12-17) are about understanding something, not about the size of the job, and the guide places it at level 1, outside the scope ladder (HWW:15). No file gives a complexity threshold for it, and the only complexity-like input is the audience `--level` (CMD:28), which is about the reader, not the task. So every cell is the same. Nothing here is REQUIRED or WORTH IT in any cell, and no cell makes absence a miss.

Complexity bands (one line each, all J since no file defines them for this command):
- LOW: one file or one concept; a plain question to Claude does the same job.
- MEDIUM: several files, named up front; the engineer wants a walkthrough before editing.
- HIGH: unfamiliar subsystem, no named files, shared interfaces; orientation is more valuable but `/tech-research` is the better tool if the answer must be kept or acted on (see section 4).

| Scope | LOW | MEDIUM | HIGH |
|---|---|---|---|
| T one-off | OPTIONAL (J) | OPTIONAL (J) | OPTIONAL (J) |
| B bug fix | OPTIONAL (J), orientation before `/sc:troubleshoot` | OPTIONAL (J) | OPTIONAL (J) |
| S single story | OPTIONAL (J) | OPTIONAL (J) | OPTIONAL (J) |
| F multi-story feature | OPTIONAL (J) | OPTIONAL (J) | OPTIONAL (J) |
| R multi-feature release | OPTIONAL (J) | OPTIONAL (J) | OPTIONAL (J) |
| N new product | OPTIONAL (J) | OPTIONAL (J) | OPTIONAL (J) |

Flag set in every cell: none needed. `--level` / `--context` only tune the wording (section 2).
R under the new definition: no change in substance. The command has no release role in any file; the existing R cell was SKIP, and the only change proposed is the same SKIP to OPTIONAL as for S/F/N (section 7).

##### 4. Choose this or the neighbour
None of these is a pipeline step that `/sc:explain` stands in for. The rules below are about picking the right side tool, not about a pipeline choice.

| Neighbour | Use `/sc:explain` (or a plain question) when | Use the neighbour when | Cited |
|---|---|---|---|
| Plain-English question to Claude | You name a file or concept and want it explained. Equivalent at level 1 | n/a: the guide gives both as the same level-1 route ("Ask Claude in plain English. For an explanation of specific code, `/sc:explain ...`") | HWW:15, 303 |
| `/sc:analyze <path> --focus ...` | You want to understand what code does | You want a health verdict on a module (security, quality, performance, architecture). Reports only | HWW:144-145 |
| `/tech-research "<question, why, code>"` | The answer is for you now, nothing needs saving, and you can name the code | The system is not understood yet, files are unknown, the idea needs feasibility or options, or the answer must be kept: it writes `RESEARCH-REPORT-<topic>.md` and feeds `/task-builder` (level 5, the better fit at HIGH complexity) | HWW:19, 142, 308 |
| `/sc:research "<q>" --depth deep` | The subject is code in this repo | The subject is outside the repo: a library, standard, best practice (searches the web) | HWW:143, 247, 312 |
| `/sc:document <path> --type api` | You only need to read an explanation | You need reference text written into the repo; it changes files | HWW:184, 246, 320 |
| `/tech-reference` | Same as above | You need a reviewed architecture document for a built feature | HWW:181, 246 |
| `bmad-document-project` (BMad) | Not comparable: existence only; its behaviour was not read here (UNVERIFIED) | | command-value-by-phase.md:38 |

Complexity rule, one line: LOW or MEDIUM and files already named, ask or `/sc:explain`; HIGH or files not named or an answer that must persist, `/tech-research` (J, built from the level 1 and level 5 rows at HWW:15, 19).

##### 6. Expected-step rule
- **Never expected, at any scope or complexity (T, B, S, F, R, N; LOW, MEDIUM, HIGH).** Its absence is never a skipped step. Its presence is never a deviation either: it changes no files (HWW:15), so running it cannot break the pipeline, and a checker must not penalize it or any engineer who uses it.
- **Never count it as a stand-in for a pipeline check.** Its own "Validate" step (CMD:31) checks the accuracy of the explanation, not the work product, so it does not satisfy review, validation, spec-panel, `/sc:reflect`, `/code-review` or `/sc:analyze` for any scope.

Full file for the citation key, the footprint (section 5), the proposals (section 7) and the unverified items (section 8): [command-nuance/sc-explain.md](command-nuance/sc-explain.md)

#### 6.3.26 /sc:post-release (Post-merge)

##### 1. Status and role

- **Does**: "synchronize and create a shipped version's entire external surface: user docs, technical docs, install/deploy scripts (validated by real end-to-end runs), and human-run e2e test guides. Runs AFTER the release gate tags a version" (CMD:3). Phase: Post-merge / Release only. Not retired; standalone-invokable as `/sc:post-release <version>` (CMD:18); the protocol skill is never invoked directly (SKILL:30).
- **Overlaps**: `/tech-reference`, `/operational-guide`, `/readme`, `/sc:document` (doc writing), `bmad-qa-generate-e2e-tests` (automated e2e tests; this command writes guides a human runs by hand, SKILL:189). It does NOT call `/sc:task` or `/sc:tasklist`: a grep of CMD, SKILL, refs and templates finds neither name; SKILL:153-159 only says "the project's" task-decomposition, execution and reflection tooling, optional, with a direct-write fallback.
- **Hard precondition**: an existing git tag for `<version>` (CMD:15; SKILL:71-73). It is the tail of an R or N, not a step inside the release PR.

##### 2. Flags

Only two inputs exist. The `--xxx` strings elsewhere in the protocol (`--help`, `--version`, `--admin`, `--debug`, `--watch`, `--base`) are examples of the target repo's flags or of `gh`, not flags of this command (grep of CMD + SKILL + refs).

| Flag | Values | Default | What it changes | Worth using when | Avoid when |
|---|---|---|---|---|---|
| `<version>` (required) | an existing tag name, e.g. `v1.4.1` (CMD:15,35); SKILL:71 matches exact tag, else a tag whose name contains it | none: STOP if absent (SKILL:72) | Chooses the tag the whole scan is anchored to (SKILL:91). Untagged version: STOP unless the user confirms a pre-tag run (SKILL:73,303) | A tag exists on `origin/main` lineage. Here pass the full tag text, e.g. `aidev02-v2-m2` (REPO tags are not `vX.Y.Z`) | No tag cut yet; use `/tech-reference` or `/operational-guide` instead |
| `--output` | directory path (CMD:28,36) | `docs/testing/<version>/` (CMD:36; SKILL:223). Fallback `.dev/releases/current/<version>/test-guides/` when the repo keeps release artifacts under `.dev/` (SKILL:223). Ambiguous convention: confirm with the user (SKILL:75,225) | Where report, manifest, `audit.log` and test guides land (CMD:36; SKILL:223). Also where the NEXT run finds the manifest: mode detection globs `.dev/releases/**/post-release-manifest.json` and `docs/testing/**/post-release-manifest.json` (SKILL:96) | Always in this repo: `docs/testing/` does not exist here, `.dev/releases/current/` does, so the default is "ambiguous" and triggers a confirm prompt. Prior run passed `--output .dev/releases/current/v2-m2/post-release/` (REPO report header) | Never omit it when a prior manifest lives elsewhere: a run-mode miss turns an additive run into ground-up (SKILL:98) |

**Does not exist** (not defined in CMD or SKILL, both read in full): `--ground-up` / `--additive` (mode is auto-detected, "do not ask", SKILL:93); `--prev-tag` (auto-detected by `git tag --sort=-creatordate`, SKILL:76); `--workstream` / `--skip-e2e` (A-E are all run; one-shot vs decompose is the controller's per-workstream judgment, SKILL:148-157); `--depth`; `--dry-run`; `--commit` / `--pr` (commit and PR are only offered as a next step and need confirmation, SKILL:324,340,351).

**Frontmatter oddity**: CMD:6 `allowed-tools: Read, Glob, Grep, Skill`, but SKILL:4 needs `Edit, Write, Bash, Task, TodoWrite` and the skill comment (SKILL:15-23) says unrestricted Bash is intentional. Whether the narrower command list blocks the skill is UNVERIFIED; the 2026-07-09 run produced all artifacts, so in practice it works.

##### 3. Scope x complexity matrix

###### 3.1 What the command needs before it can run, and whether this repo has it (read-only checks, 2026-10-27)

| Need | What the files say | This repo | Met? |
|---|---|---|---|
| A tag for `<version>` | CMD:15; SKILL:71-73 STOP if none (unless user confirms a pre-tag run) | Two annotated tags, both on `origin`: `aidev02-v1.0` (2026-06-22, "AIDev02 v1.0 GA") and `aidev02-v2-m2` (2026-07-09, "V2-M2 convergent hybrid"). Both are ancestors of `origin/main` (`merge-base --is-ancestor`). No `vX.Y.Z` tags (`git tag --list 'v*'` empty). 763 commits and 245 merge commits on `origin/main` since `aidev02-v2-m2`, no tag | YES, but names are `aidev02-v*`, and none since July |
| A "release gate" that tags | CMD:3,15 assume one; neither file defines it | No workflow in `.github/workflows` creates a tag or GitHub Release (grep for `git tag`, `gh release`, `create-release`, `softprops`, `on: release`: only unrelated Tailscale `tags:` and Orca upstream `tag_name` reads). `gh release list` returned no rows. `docs/operations/aidev02-operator.md:639` says "AIDev02 GA is the v1.0 git tag cut in Phase 8 (T08.27)": a manual, operator-cut tag | NO automated gate; a human cuts the tag. The command only needs the tag |
| Release intent source | SKILL:77: per-version dir under `.dev/releases/{current,complete}/` (may be tag-fuzzy), else `CHANGELOG.md` + `RELEASES.md` | `.dev/releases/current/v2-m2/` matches `aidev02-v2-m2` fuzzily (briefing, research, TDD). `RELEASES.md` absent. Root `CHANGELOG.md` has only `[Unreleased]` (line 20) and `[1.3.0] 2026-05-19` (line 167); same at the tag (`git show aidev02-v2-m2:CHANGELOG.md`). The v2-m2 release notes the prior run used are in the payload changelog `templates/VSCode-AIDev02/aienv.d/CHANGELOG.md:59` (`## [20260701-1] - 2026-07-01`). The current payload `aienv.d/VERSION` is `20261016-1`; it is a payload stamp, not a git tag | PARTIAL: root CHANGELOG does not carry the tags; release dir does |
| Prior manifest (decides additive vs ground-up) | SKILL:95-99 globs | `.dev/releases/current/v2-m2/post-release/post-release-manifest.json`, tracked in commit `60f5ff85` (2026-07-09); the SKILL:96 glob finds it, so the next run auto-selects additive | YES. Caveat: it is additive over `v1.0..v2-m2` only (manifest `run_mode_note`) and all 13 `feature_inventory` entries are `added_in: aidev02-v2-m2`; the v1.0 GA surface was never inventoried (AD:60-62 stale carry-forward; SKILL:101 "prefer ground-up when in doubt") |
| Output directory | CMD:36 `docs/testing/<version>/`; SKILL:223 fallback `.dev/releases/current/<version>/test-guides/` | `docs/testing/` does not exist; `.dev/releases/current/` does. Prior run used neither default (explicit `--output`) | AMBIGUOUS: expect a confirm prompt unless `--output` is passed |
| Workstream C target | SKILL:127-134, PB:76-110 | Prior run class `local-deploy`: throwaway HOME, scripts from `git archive` of the tag; full terraform-to-Coder-platform provision (`vm-e2e`) NOT exercised, no live platform (manifest `install_surface_note`) | Shell-level only. A `vm-e2e` run needs a live platform and a confirm (SKILL:340,351) |

**Verdict**: the repo meets the one hard precondition (a tag exists and the command has run once on it). There is nothing new to run it on today: the last tag is 2026-07-09 and every merge since (763 commits) is un-tagged, so a missing post-release for those merges is not a skipped step. The earlier open question (value file U14, "does the team tag?") is answered: yes, twice, rarely, with a manual cut.

###### 3.2 Does the command vary by complexity?

Not by anything the engineer types: there are no flags that change depth (Section 2). Complexity changes what the controller does inside the run: one-shot versus decompose per workstream (SKILL:148-157) and, in additive mode, re-run versus carry forward Workstream C (AD:42). So the matrix below is about WHETHER to run it, and the bands predict how heavy the run is.

**Bands (signals from files; thresholds are JUDGMENT)**

| Band | Signals a checker or engineer can read on disk |
|---|---|
| LOW | Additive run. `git diff --name-only <prev_tag>..<tag>` (AD:13) maps to no user-facing, install or sysop surface, or to a few A/B doc edits only (AD:30). Install surface unchanged, so C is carried forward with an explicit statement (AD:42). One-shot per workstream (SKILL:150). |
| MEDIUM | Additive. Several user-facing or sysop capabilities new or changed (AD:22-26), or install files changed so C re-runs on the changed path (AD:29,42). Class `package` or `local-deploy` (SKILL:130-131). Calibration, the only observed run: `aidev02-v1.0..aidev02-v2-m2` = 84 commits, 13 capabilities, `local-deploy`, all five workstreams, 1293 s (`audit.log` `duration_sec`). (J) |
| HIGH | Ground-up (no prior manifest, SKILL:98), OR class `vm-e2e` (SKILL:129), OR a stateful service whose migrations must be proven (PB:100), OR a surface no earlier manifest covered (this repo: the v1.0 GA surface). Decompose path with itemized worklist (SKILL:151-157). |

###### 3.3 Matrix

`(J)` = my judgment, not a file's statement. No file rates this command REQUIRED anywhere: `HOW-WE-WORK.md:279` lists it only as "After tagging a release." in the "Other commands" table; it is not one of the six levels and not in Ryan's pipelines (brief, ruling 5).

| Scope | LOW | MEDIUM | HIGH |
|---|---|---|---|
| T one-off | N/A (no tag) | N/A | N/A |
| B bug fix | N/A (a hotfix tag, if ever cut, is an R-sized event, not B) (J) | N/A | N/A |
| S single story | SKIP (J): a single feature's release is a phase inside S (brief, ruling 2); use `/tech-reference` or `/operational-guide` | SKIP (J) | SKIP (J) |
| F multi-story feature | SKIP (J) | SKIP (J) | OPTIONAL (J): only if the feature itself is tagged AND changed install/deploy files; else `/operational-guide` |
| R multi-feature release | OPTIONAL (J): `<tag> --output .dev/releases/current/<short>/post-release/`. If the delta touches no external surface, the run records "internal only" (AD:30-32) | WORTH IT (J): same flags | WORTH IT (J): same flags; first run over a never-inventoried surface should be ground-up (SKILL:101) |
| N new product | OPTIONAL (J): `no-install-surface` class, run yields an honest gap + quickstart (SKILL:132) | WORTH IT (J): package class, install proven in a fresh venv/container (PB:97) | WORTH IT (J): always ground-up (first release has no manifest, SKILL:98); this is where C and D/E guides pay most |

All rows assume a tag exists. With no tag the cell is N/A regardless of scope (SKILL:73).

##### 4. Choose this or the neighbour

Neighbour descriptions come from the session skill list and `command-value-by-phase.md` (VAL) rows; I did not read the neighbours' own skill files (UNVERIFIED beyond the descriptions). The deciding difference is always the same: `/sc:post-release` is anchored to a TAG, covers the WHOLE external surface, and PROVES the install by a real run.

| Neighbour | Pick the neighbour when | Pick `/sc:post-release` when |
|---|---|---|
| `/tech-reference` (VAL:189, O11 VAL:237) | One built feature (S, F), no tag, only an architecture/implementation reference is missing. Guide 3.1 step 11 | A tag was cut for a multi-feature release (R) and user docs, tech docs, install path and test guides must all match the tagged commit (SKILL:41,59) |
| `/operational-guide` (VAL:190) | One deploy, setup or ops procedure changed (e.g. `docs/operations/*`), no tag, no need to run it clean | Install/deploy scripts changed across a tag and the new-user path must be re-run to green with a transcript (SKILL:187; PB:91-100); this command fixes scripts and writes the quickstart, not just a doc |
| `/readme` (VAL:191) | A new package or module needs a README | The README is one of several stale user docs for a tag (PB:46-56 splits mixed READMEs into A and B) |
| `/sc:document` (VAL:192) | One-pass reference text for specific code (`--type api`) | Never as a substitute: no tag anchoring, no e2e |
| `bmad-qa-generate-e2e-tests` (VAL:151) | You want AUTOMATED end-to-end tests for existing features | You want step-by-step guides a human runs by hand: preconditions, actions, expected result, pass/fail, expected results traced to code (SKILL:189; PB:116-122). They do not conflict; D/E guides are not tests |
| `/sc:release-split` (VAL:72) | Before the build, deciding whether to split the release | After the tag. Different phase; no overlap |
| `bmad-retrospective` (VAL:187) | Lessons learned after an epic | Not an overlap: retrospective reviews the work, this command documents the product surface |

Sequencing inside an R (judgment): `/sc:pr-submit` merges the release PR, a human cuts the tag (3.1 above), THEN `/sc:post-release <tag>`. Its own commit and PR follow the same rules as any other branch: feature branch off the auto-detected default branch, commit and PR only on confirmation, PR target from `git remote -v` (SKILL:347-348, 340). Running it before the tag (pre-tag run) is allowed only after explicit user confirmation (SKILL:73).

##### 6. Expected-step rule

- **Expected** only when scope is R or N AND a new git tag exists with no matching manifest `tag` (Section 5 trigger). Then the expected footprint is `audit.log` with RUN and RESULT blocks, report, manifest, and (MEDIUM/HIGH) the guides. Grace period is a judgment call; this repo cut no tag in the 3.5 months since 2026-07-09, so a window based on merges instead of tags would wrongly flag all 245 merges.
- **Absence is fine** for T, B, S, F (no tag, SKIP/N/A in Section 3), for any R or N with no new tag, and for R-LOW where the delta touches no external surface (OPTIONAL: the run may legitimately be skipped or end as "internal only", AD:30-32). A short path that skips it is legitimate. A pre-tag run also exists and needs user confirmation (SKILL:73), so a run dated before the tag is not an error.

Full file for the citation key, the footprint (section 5), the proposals (section 7) and the unverified items (section 8): [command-nuance/sc-post-release.md](command-nuance/sc-post-release.md)

#### 6.3.27 /sc:document (Post-merge)

##### 1. Status and role
- One sentence from its own file: "Generate focused documentation for components, functions, APIs, and features" (CMD:3). Single pass: Analyze, Identify, Generate, Format, Integrate (CMD:27-31). Frontmatter `complexity: basic` (CMD:5) is the command's own weight class, not a task-complexity signal.
- Phase: Document (post-implement / post-merge). Standalone-invokable; NOT retired; CMD never mentions `/sc:task` or `/sc:tasklist`. No backing skill, no task folder, no ledger.
- Overlaps: `/tech-reference`, `/operational-guide`, `/readme` (HWW:175-184, 246, 320), `/sc:post-release` at release level (its description covers user and technical docs; it does not name the doc skills, grep found no reference), `bmad-agent-tech-writer` / `bmad-document-project` in the BMad lane (value file:92,193).

##### 2. Flags
The command has one positional argument and two flags (CMD:22). No defaults are stated for any of them (UNVERIFIED default behaviour).

| Flag / arg | Values | Default | What it changes (cited) | Worth using | Avoid |
|---|---|---|---|---|---|
| `[target]` | file, directory, module or component name (CMD:59, 67, 75, 83) | none stated | Scope of the code analysis (CMD:27) | Always give a named path; "Will Not" generate docs "without proper code analysis and context understanding" (CMD:98) | Vague names or the whole repo: one pass cannot verify a large target (J) |
| `--type inline` | inline | not stated | JSDoc/docstring generation plus inline comments, "Adds comprehensive inline documentation for functions and classes" (CMD:49, 60-62). Edits source files. | A new or changed public function with no docstring. The only documentation path that touches source; no neighbour writes docstrings (TR:148, OG:153, RM:155 all write one document file) | Files where a docstring-only diff would mix with a feature diff in review (J) |
| `--type api` | api | not stated | Interface extraction, reference material, usage examples (CMD:50); "endpoints and schemas" (CMD:68). HWW's one example (HWW:184, 320 note) | A bounded interface: one route file, one module's public surface | Targets spanning several subsystems (use `/tech-reference`) |
| `--type guide` | guide | not stated | Feature analysis, tutorial content, implementation guidance (CMD:51); "user-focused documentation with practical examples" (CMD:76-77). Used by `/sc:cli-eval` to update an inventory table (integration-map.md:46-55) | Small edits to an existing guide; a brief how-to for a LOW target | Operator procedures (install, deploy, rollback): use `/operational-guide` (HWW:182) |
| `--type external` | external | not stated | Component overview, detailed specifications, integration instructions as external doc files (CMD:52, 83-85) | A component library folder needing a doc file | A README for a new module (use `/readme`) |
| `--style brief` | brief | not stated | Focuses on "implementation patterns and common use cases" (CMD:77-78 example) | LOW targets; edits to existing docs | HIGH targets |
| `--style detailed` | detailed | not stated | "comprehensive API documentation with endpoints and schemas", usage examples, integration guidelines (CMD:68-69 example) | MEDIUM interface docs | Using it as a substitute for a reviewed reference (no review step exists, CMD:25-31) |

Does NOT exist in CMD: `--depth` (the `--depth quick` flag belongs to `/sc:workflow`, validation-oneoff file), `--output` / `--path` (no output path convention at all), `--audience`, `--spec`, `--dry-run`, `--tier`, `--format`, `--no-write`. Output location is whatever the target and `--type` imply; CMD:44 only says "Write: Documentation file creation with proper formatting".

Neighbour "pseudo-flags" (natural-language only, no CLI flags in TR, OG or RM): the inputs WHAT / WHY / WHERE / OUTPUT (TR:38-47; OG:56-65; RM:55-68). Words "thorough", "comprehensive", "detailed" force Heavyweight (TR:93; OG:116; RM:122); "quick", "fast", "light QA", "basic" force `qa_intensity: lite` (TR:105; OG:128; RM:132). Default output paths: `docs/[domain]/FEATURE-NAME-TECHNICAL-REFERENCE.md` (TR:47), `docs/docs-product/ops/[name]-operational-guide.md` (OG:61, a folder this repo does not have; this repo has `docs/operations/`), `[module-dir]/README.md` (RM:61). Pass the output path explicitly (HWW:41, 181-183 do).

##### 3. Scope x complexity matrix
Does the command vary by complexity? Not in its own file: it is one fixed pass (CMD:25-31) with `--style` as the only dial, and `--style` is not tied to any signal. The variation below comes from the neighbours' own tier tables, which are the only on-disk file-count thresholds for documentation. Applying them to `/sc:document` is JUDGMENT.

Bands (signals: files in the target, subsystems, procedure vs reference, risk):
- LOW: target named up front; fewer than 5 relevant files; one subsystem; no new deploy or operator steps. Borrowed boundary: TR:83, 85 (Lightweight "<5 relevant files"), RM:110, OG:108.
- MEDIUM: 5-20 files or several subsystems, but the reader needs reference for one bounded interface. Borrowed: TR:88 (Standard "5-20 files, multiple subsystems"), OG:109 (5-15 config files).
- HIGH: 20+ files, cross-cutting, several integration points, multi-machine or multi-environment, or content touching secrets, permissions, paths, infrastructure. Borrowed: TR:89, 95; OG:110, 118. CMD:100 also bars docs that expose "sensitive implementation details", and the user NFR12 rule bars secrets in docs: one unreviewed pass is the wrong tool here.

| Scope | LOW | MEDIUM | HIGH |
|---|---|---|---|
| T one-off | SKIP (J). A docstring is part of the edit itself; `--type inline` OPTIONAL only when a new public function has none | SKIP (J) | SKIP (J) |
| B bug fix | SKIP (J) | SKIP (J) | SKIP (J) |
| S single story | OPTIONAL (J) `--type inline --style brief` or `--type api --style brief` | OPTIONAL (J) `--type api --style detailed` on the changed interface | OPTIONAL (J) `--type api --style detailed`; escalate to `/tech-reference` at 20+ files (TR:89) |
| F multi-story feature | WORTH IT (J) `--type api --style detailed`; cheaper than the `/tech-reference` minimum | OPTIONAL (J) `--type inline` only; `/tech-reference` covers the rest | OPTIONAL (J) `--type inline` only; the reference is `/tech-reference` |
| R multi-feature release | OPTIONAL (J) `--type api` per feature | OPTIONAL (J) `--type inline` | OPTIONAL (J) `--type inline` only; release docs are `/tech-reference` per feature, `/operational-guide`, `/sc:post-release` |
| N new product | OPTIONAL (J) `--type guide --style brief` | OPTIONAL (J) `--type inline` | OPTIONAL (J) `--type inline` only; the module README is `/readme` (RM:61) |

Exception in any cell: if a `/sc:troubleshoot` REPORT.md says the fix belongs "in the documentation" (HWW:128), the doc edit IS the fix; a plain edit or `/sc:document <file> --type guide --style brief` both fit (J).
No cell is REQUIRED: no file requires this command at any scope.

##### 4. Choose this or the neighbour
Cost anchor: the three doc skills are NOT one-pass. Each runs Stage A scope discovery, writes a BUILD-REQUEST, calls `/task-builder`, then `/task` over 7 phases with analyst, QA and fidelity gates (TR:159-183; OG:164-188; RM:170-194). Even the Lightweight tier (TR:85: 2-3 codebase agents, 400-600 lines) goes through that pipeline; only "trivial updates to an existing tech reference" use the simple Template 01 (TR:368). Neither `/task-builder` nor `/task` is retired. So the question is "does this documentation justify a research-and-QA pipeline", not "which template".

| Neighbour | Pick the NEIGHBOUR when (signals) | Pick `/sc:document` when | Cited |
|---|---|---|---|
| `/tech-reference` | A whole feature or subsystem, not a named file; 5+ relevant files or more than one subsystem; the reader needs architecture, how it works, how to extend; claims must be code-verified (the skill tags CODE-VERIFIED / CODE-CONTRADICTED, TR:792); the document will be relied on later by maintainers | A named file, route file or small module (under 5 files); reference text, not architecture; or `--type inline` docstrings (no neighbour does that) | HWW:181, 246; TR:85-95, 792 |
| `/operational-guide` | The reader EXECUTES steps: install, deploy, operate, roll back; multi-service or 5+ config files; multi-machine or multi-environment; infrastructure or secrets handling | LOW only: single-service, under 5 config files, linear procedure, no secret handling, and `--type guide --style brief` is enough (J) | HWW:182; OG:106-118 |
| `/readme` | A new package or module needs a navigational entry file at the module root; README must follow `readme_template.md`; 500-line ceiling | Editing an existing README or one table in it (the `/sc:cli-eval` create flow does this with `--type guide`) | HWW:183; RM:55-61, 116; integration-map.md:46-55 |
| `/sc:post-release` | Multi-feature release already tagged; the whole external surface (user docs, technical docs, install scripts, e2e guides) must be synchronised | Per-target docstrings or API text written during the release, before the tag | `commands/sc/post-release.md:3` |
| `/sc:explain` | Reader only needs an answer, no file (HWW:15) | You need the text on disk | HWW:15 |
| BMad `bmad-agent-tech-writer`, `bmad-document-project` | Work is in the BMad lane; pick the lane at the Spec step and stay in it | Task-file lane | value file:92, 193, 223 |

Cross-pick rule: never run `/sc:document` and `/tech-reference` for the same target and the same output type (value file:50 `‡`, 237). The one safe pairing is `/tech-reference` for the document plus `/sc:document --type inline` for docstrings (J).

##### 6. Expected-step rule
- `/sc:document` is never an expected step at any scope x complexity. The only routing-table row that names it is `document-built`, an either-or among four commands with `mandatory_flags` "-" (HWW:320). Absence is always fine; presence is always fine.
- What a checker MAY expect is "some documentation action" for F, R and N at MEDIUM or HIGH complexity (HWW:87, step 11 of the full-spec flow; value file:255-257 lists the doc skills as additions, not minimums), satisfied by any of `/tech-reference`, `/operational-guide`, `/readme`, `/sc:document`, a plain docs edit, a BMad tech-writer step, or doc items inside the task file (J). For T and B expect nothing. Do not flag a missing `TASK-TECHREF-*` folder when docs were edited by hand.

Full file for the citation key, the footprint (section 5), the proposals (section 7) and the unverified items (section 8): [command-nuance/sc-document.md](command-nuance/sc-document.md)

### 6.4 Conflicts between sources

Each row records both versions with file and line. Nothing here is resolved; the Status column says who can resolve it. Line numbers of this file (written "main file") are those of the file as read before this merge, the same numbering the nuance files cite as CV or CVP. Line numbers of the nuance, validation, scenarios and brief files are those of the files as read on 2026-10-27. The folder is `_bmad-output/brainstorming/brainstorm-clay-feedback-decisions-2026-10-26/`; `HW` is `~/.claude/HOW-WE-WORK.md`.

| # | Topic | Version A (source and line) | Version B (source and line) | Status |
|---|---|---|---|---|
| C1 | Does `/sc:implement` refuse a task-builder file? | `validation-feature-task-builder-vs-sc-workflow.md` line 42 (also line 11 and the proposal at line 265): `/sc:implement` "explicitly refuses what makes the file MDTM: 'Invoke /task', 'Import MDTM F1, 6-agent phase gates, or /sc:reflect as the per-task gate'"; proposed note "do not use on a task-builder file" | `command-nuance/sc-implement.md` lines 51-54 and 167 (U5): "Hard refusal: NONE found"; the protocol says "MDTM-shaped files still use this protocol. Do not auto-handoff" (IS:78); the rule is only a pairing convention (HW:216, 243), "a CONVENTION a checker may flag (J), not a tool-enforced stop" | Open. Neither source ran the command (validation V2; nuance U5). Pending Ryan (6.6 item 16) |
| C2 | Is brainstorm or design a fixed step at multi-story feature size (scenario S5)? | `scenarios.md` lines 34-35: S5 phases include "brainstorm or design"; "Allowed to skip: nothing in the chain, but depth varies" | `command-nuance/sc-brainstorm.md` lines 116-118: brainstorm is expected only at F or N, MEDIUM or HIGH, with no earlier spec; S5 "conflicts with the guide's 'only if vague'. Align S5 with this rule". `command-nuance/sc-design.md` line 109 says the opposite about the same S5 line: the S5 wording "already agree[s] with this: design is a one-of choice, not a fixed step" | Open. The two nuance files disagree with each other about whether S5 is wrong. `scenarios.md` is Ryan's draft context, not edited here |
| C3 | Is a release the same size as a new product (scenario S6)? | `scenarios.md` lines 39-43: S6 is "Release and new product (largest end of the ladder)", one scenario for both | `command-nuance/_brief.md` line 12 (ruling 2): R is a multi-feature release, "one step below greenfield new product (N)"; the work-size list at the top of this file says the same | Open. Recorded only; S6 may need splitting into R and N |
| C4 | Is a release split a required step at release size? | `scenarios.md` lines 40-41: S6 phases include "release split"; "Allowed to skip: none" | `command-nuance/sc-release-split.md` line 69: "No cell is REQUIRED: HW calls the step optional (HW:309 step 6, '(optional)'; HW:70)"; "do not split" is a valid result (SK:31, 61). Row 12 at line 141 proposes rewording S6 to "release split or an equivalent recorded split decision; skipping is fine for R-LOW" | Open. Pending Ryan |
| C5 | Is a post-release check always expected at release size? | `scenarios.md` lines 40 and 42: "post-release check"; "post-release verification [is] present" | `command-nuance/sc-post-release.md` lines 111-112: expected only at R or N when a new git tag exists with no matching manifest; absence is fine for R-LOW; the repo cut no tag in the 3.5 months after 2026-07-09 | Open |
| C6 | May the design step use both lanes? | Main file line 223: "pick the lane at the Spec step and stay in it until the PR" (also O3 at line 229). `command-nuance/sc-design.md` lines 71 and 78 apply the same rule | `command-nuance/sc-tdd.md` lines 86 and 128: repo evidence shows `bmad-architecture` then `/tdd` stacked (`_bmad-output/planning-artifacts/tdd.md:14-18`; `.dev/releases/current/v2-m3/TDD_V2_M3.md:14` has a BMad PRD as parent); "This contradicts CV:223 ... for the design step"; both legitimate at N and HIGH F | Open. Pending Ryan (6.6 item 27) |
| C7 | Are `/sc:cleanup` and `/sc:improve` under the same guard rails? | Main file line 154: `/sc:cleanup` Notes "Same guard rails as `/sc:improve`" | `command-nuance/sc-cleanup.md` lines 28 and 101: "NOT the same guard rails as `/sc:improve`: it has no `--force` and no stated rule for whole-file removal"; its auto-delete bar is lower than the audit's. `command-nuance/sc-improve.md` line 38: `--force` exists on `/sc:improve` | Open. Main-file rewording is proposal P150 in 6.2 |
| C8 | Is a medium-complexity one-off a T item? | `command-nuance/sc-implement.md` line 82: T MEDIUM is "REQUIRED (J, lane)" because HW:22 forces a written plan above 5 edits or more than one source file | `command-nuance/sc-workflow.md` line 50: T MEDIUM is "N/A (J)" because the same HW:22 limit means the work "is not a one-off"; rate it on the S row | Open. Both cite HW:22 and both are (J) |
| C9 | Executor at R-MEDIUM | `command-nuance/sc-implement.md` line 86: R LOW "OPTIONAL (J)", R MEDIUM "OPTIONAL (J): same" (executor of a constituent S-size item), R HIGH SKIP | `command-nuance/sc-workflow.md` line 54: R LOW "OPTIONAL (J)", R MEDIUM "SKIP (J)", R HIGH "SKIP (J)" | Open. Both (J) |
| C10 | Who writes the release specs after a split? | `command-nuance/sc-design.md` lines 46 and 117: R-HIGH `/sc:design` is WORTH IT (J) when `/sc:release-split` approves a split, because Part 3 says "Default to /sc:design for producing release specs" (RS:270-275) | `command-nuance/sc-release-split.md` line 80: `/sc:design` is "a single-pass draft of one interface (HW:244; CV:65). For a full release spec, a person or `/tdd` is the better author (J)"; line 156 (U10) leaves open whether `/sc:design` can author a whole release spec | Open. Neither ran Part 3 |
| C11 | Does `/sc:pr-submit` push the branch? | `command-nuance/_brief.md` line 17 (ruling 5): "commit regularly and push with `/sc:pr-submit`"; main file line 167: "Ryan's pipeline step 4" | `command-nuance/sc-pr-submit.md` line 10: "the command OPENS the PR (SKILL:189). It does not push the engineer's branch; the only push it can make is a remediation push at `--monitor 3` (SKILL:195)"; HW:202-204 has the engineer push first | Open. Pending Ryan (6.6 item 4) |
| C12 | Which `--monitor` level is used in practice? | Guide: "always pass `--monitor 1`" (HW:254; `command-nuance/sc-pr-submit.md` lines 15 and 76); the default 2 "silently edits code" (line 77) | `command-nuance/sc-pr-submit.md` line 78: 8 of 8 observed run logs in `/home/coder/workspaces/Coder` used `--monitor 3`, "so the guide is not what happens in practice" | Open. Pending Ryan (6.6 item 13) |
| C13 | What does plain `--fix` on `/sc:troubleshoot` offer? | HW lines 126, 133 and 311 (as quoted at `command-nuance/sc-troubleshoot.md` line 110): `--fix` "offers to build a task file" | `command-nuance/sc-troubleshoot.md` lines 20 and 110: the command and the ref say plain `--fix` offers a `/sc:workflow` plan (`--depth standard --handoff none`); the task-file route needs `--fix --depth deep` (CMD:54, 191; refs/remediation-handoff:9-12) | Open. The nuance file treats the command file as the source (U11, line 123) |
| C14 | Does `/sc:swarm-wizard` use `sc-bare-review`? | HW:291 (quoted at `command-nuance/sc-swarm-wizard.md` lines 115 and 127): `sc-bare-review` "is internal (used by /sc:swarm-wizard...)" | `command-nuance/sc-swarm-wizard.md` lines 115 and 126: no wizard file mentions `sc-bare-review`; the wizard drives `swarm run --lens bare-review` itself (CC:43) | Open. "Not resolvable from files" |
| C15 | Stage `.dev/tasks` or do not stage the ledger? | Repo `CLAUDE.md` Development Practices: `.dev/tasks/` is always staged, "ledgers ... included" | `skills/sc-implement-protocol/refs/ledger.md:3` "Do not `git add` the ledger", reported at `validation-feature-task-builder-vs-sc-workflow.md` lines 249 and 295 (V12), `validation-oneoff-sc-task-vs-sc-implement.md` lines 116-117 (F2, F3), `command-nuance/sc-implement.md` line 132 and `command-nuance/sc-workflow.md` lines 146 and 189 | Open. Not resolved by any file. `sc-workflow.md` line 146 advises not to treat `progress.md` as a defect either way |
| C16 | Does the staging rule reach new `reflect/` folders? | Repo `CLAUDE.md`: `git add .dev/tasks` stages everything under `.dev/tasks/` | `command-nuance/sc-reflect.md` lines 170 and 203 (U9): `.gitignore:32` is `reflect/`, which matches at any depth, so a plain `git add .dev/tasks` does not stage a new `reflect/` subfolder | Open. Whether engineers force-add is unverified |
| C17 | `--no-promote` or `--promote` on the post-audit? | HW:322 (as quoted at `command-nuance/sc-reflect.md` lines 41 and 112): `--no-promote` is the mandatory flag of the hand-run post audit at every size | `command-nuance/sc-reflect.md` line 112: the `/task-builder --cli` POST item passes `--promote` on purpose (TB:2237); the skill-mode item passes no `--no-promote`, while HW:252 says the folder stays in `to-do/` | Open |
| C18 | What should the Release row of Section 4 (main file line 256) say? | `command-nuance/sc-release-split.md` line 134, `command-nuance/sc-roadmap.md` line 187 and `command-nuance/sc-workflow.md` line 171: the three-step release minimum assumes already-built work and must be rebuilt for the new R; planning (a tasklist step per feature, or a split decision at step 0) cannot be optional | `command-nuance/sc-reflect.md` line 182, `command-nuance/sc-git.md` lines 99-101, `command-nuance/sc-pr-submit.md` line 123, `command-nuance/sc-spec-panel.md` line 97 and `command-nuance/sc-test.md` line 94 each keep or amend the post-implementation steps (restate reflect, add a commit step, add `--timeout 3600`, add spec-panel, add a pre-push test signal) | Open. Eight files edit one cell in different ways; one reconciled rewrite is needed once Ryan fixes the R minimum (6.6 item 11) |
| C19 | Is the roadmap validator worth more than the roadmap generator at HIGH? | `command-nuance/sc-roadmap.md` lines 81-84: `/sc:roadmap` is OPTIONAL at R and N MEDIUM and HIGH (J), "OPTIONAL and not WORTH IT" because its consumer is retired | `command-nuance/sc-validate-roadmap.md` lines 74-75: `/sc:validate-roadmap` is WORTH IT (J) at R HIGH and N HIGH | Open. Both (J) |
| C20 | Is `/sc:workflow` ever OPTIONAL at feature size? | Main file line 110: F = OPTIONAL. `command-nuance/sc-workflow.md` lines 53 and 104: F-LOW OPTIONAL (J) under the "several single-story plans" exception only; MEDIUM and HIGH SKIP | `validation-feature-task-builder-vs-sc-workflow.md` lines 261 and 155: F = SKIP (JUDGMENT), "not eligible as the F minimum"; the exception is offered only as a suggestion | Open. Pending Ryan (6.6 item 6) |
| C21 | Is the existing technical reference evidence of `/tech-reference` use? | Main file line 189: "Repo already carries `aidev02-v1.0-as-built-technical-reference.md`" | `command-nuance/sc-document.md` lines 71 and 87: that file says it was "Produced by the `bmad-retrospective` milestone-exit reconciliation gate" (its line 13); the repo holds 0 `TASK-TECHREF-*` folders | Open. Main-file note is rewritten by proposal P210 in 6.2 |
| C22 | May a checker require `--pass all` before a cleanup? | HW:318 (quoted at `command-nuance/sc-cleanup-audit.md` lines 25, 137-138): the cleanup route lists `--pass all` as the mandatory flag | `command-nuance/sc-cleanup-audit.md` lines 138 and 167 (U9): for a target of 50 in-scope files or fewer, `--pass surface` or no audit is "legitimate (J)"; "A strict checker would flag the second" | Open. Pending Ryan (6.6 item 5) |
| C23 | Is `/sc:troubleshoot` a step for every bug? | HW:311 (quoted at `command-nuance/sc-troubleshoot.md` lines 49 and 113): troubleshoot is step 1 for every bug; main file lines 175 and 253 rate B REQUIRED and list it as step 1 | `command-nuance/sc-troubleshoot.md` lines 49 and 101: at B-LOW (known cause, failing test names the line) it is OPTIONAL (J, proposed) | Open. Pending Ryan (6.6 item 12) |
| C24 | Is `/sc:task` the level-2 tool? | HW lines 16 and 304: level 2 is "`/sc:task "<change>"` or a plain edit" (`validation-oneoff-sc-task-vs-sc-implement.md` line 64, E5.5) | `command-nuance/_brief.md` line 13 (ruling 3): `/sc:task` and `/sc:tasklist` are retired; `validation-oneoff-sc-task-vs-sc-implement.md` line 128: the guide is shipped by `superclaude update` and is not ours to edit | Open. The guide text stays until the shipped guide changes |
| C25 | Which tasklist route does a command's remediation offer take? | `command-nuance/sc-auggie-review.md` line 83: the offer routes by review depth: quick and standard go to `/sc:workflow` + `/sc:implement`, deep to `/task-builder` + `/task`, "not on fix size"; `command-nuance/sc-troubleshoot.md` line 73: plain `--fix` builds a `/sc:workflow` plan at `--depth standard` | `validation-feature-task-builder-vs-sc-workflow.md` lines 11-13: the multi-story feature minimum is `/task-builder` + `/task`; `/sc:workflow` + `/sc:implement` is not eligible | Open. `sc-auggie-review.md` line 83 advises declining the offer for many-file fixes; a checker should not flag the resulting `TASK-WF-*` package (lines 86 and 114) |

### 6.5 Defects found in the guide and the command files

Collected from the 27 nuance files and the two validation files. One row per defect; a row may bundle small defects of one command that share a source. Nothing was fixed: the command files and skills live in each engineer's `~/.claude` (not in this repo), and the guide is shipped by `superclaude update`. Categories: Command vs skill (the command file and its protocol skill disagree); Internal inconsistency (one file contradicts itself or an undefined item); Undefined flag (recommended or named but defined nowhere); Retired-command handoff (a flag or text that calls `/sc:task` or `/sc:tasklist`); Wrong cross-reference; Stale text; Missing hook or file; Repo state. "Reported in" gives the nuance file and the line where the defect is written; the line inside the command or skill is in the "Where it sits" cell using the citation keys of that nuance file.

| # | Category | Defect | Where it sits | Reported in |
|---|---|---|---|---|
| 1 | Command vs skill | `/sc:roadmap`: the command file and the protocol skill give two flag surfaces. The command file mirrors the CLI and calls `--specs`, `--template`, `--multi-roadmap`, `--interactive`, `--compliance`, `--persona` unsupported; the skill still documents them | CMD:46-48 against PRO:5, PRO:67-82 | `sc-roadmap.md` lines 25, 54, 198 (U1) |
| 2 | Command vs skill | `/sc:roadmap`: default output directory (parent of the first input in CMD; `.dev/releases/current/<spec-name>/` in PRO), resume flag (`--resume` against `--resume-from`), agent limit (2 by default against 2-10 with an orchestrator at 3 or more), and `--validate/-v` only in the skill | CMD:19, 27, 29 against PRO:71, 77, 81, 84, 248 | `sc-roadmap.md` lines 30-33, 55-56 |
| 3 | Command vs skill | `/sc:validate-roadmap`: seven contradictions between the command file and the skill: invocation, output layout, sub-agents, the "mirrors the CLI" claim, exit code against verdict, the flags `--agents --model --max-turns --debug` (absent from the skill), and a depth table whose promises the body does not gate | VR:18, 31-34, 43, 62-69, 98 against VP:20, 84, 93-97, 105-109, 582-590, 686-693, 744 | `sc-validate-roadmap.md` lines 44-54, 136 |
| 4 | Command vs skill | `/sc:reflect`: version drift. The command file says 2.0.0, the skill frontmatter says 1.0.0 with contract 1.8.0; the command file points at a source-tree path | CMD:8, 153; SKILL frontmatter | `sc-reflect.md` line 204 (U10) |
| 5 | Command vs skill | `/sc:reflect`: flags in the skill or refs that the command's option table lacks: `--no-escalate`, `--strategy enterprise`, `--executor-model`, `--isolate-reviewers`, `--fuzzy-ids`, `--remediate-docs`; `--recursive` and `--resume-from` are named in prose and never defined | SKILL:283, 416, 445, 666, 674, 1085, 1497, 1887 against CMD:10, 86-116 | `sc-reflect.md` lines 47-57, 196 |
| 6 | Command vs skill | `/task-builder` and `/sc:reflect` disagree on the report file name: task-builder's hard check names lowercase `report.md`, reflect writes `REPORT.md` (observed on disk: uppercase) | TB:1697, 1701 against SKILL:734, CMD:138 | `sc-reflect.md` lines 161, 200 (U6) |
| 7 | Command vs skill | `/sc:troubleshoot`: `--caller`. CMD says setting it makes Wave 5 emit `return-contract.yaml`; the skill says only `caller=task-unified` does | CMD:60 against SKILL:153, 537 | `sc-troubleshoot.md` line 116 |
| 8 | Command vs skill | `/sc:troubleshoot`: `--no-diagnosability-audit`, `--diagnosability-handoff`, `--reset-diagnosability-rounds` are in the skill, not in the command's argument hint; under `--depth quick` the hard-stop text names only `--no-escalate` as a suppressor | SKILL:125, 270-271, 617 against CMD:8 | `sc-troubleshoot.md` lines 27-29, 117-118 |
| 9 | Command vs skill | `/sc:troubleshoot`: CMD:185 says Tier 1 always runs first, but one observed `audit.log` shows `depth: deep (user explicit skip-Tier-1)` | CMD:185; a run folder under `.dev/troubleshoot/` | `sc-troubleshoot.md` line 122 |
| 10 | Command vs skill | `/sc:auggie-review`: where High findings get inline comments. SEV says deep only; CMD and SKILL say Critical and High at every depth | SEV:35 against CMD:52, SKILL:316 | `sc-auggie-review.md` lines 21, 136 |
| 11 | Command vs skill | `/sc:auggie-review`: the over-5000-line STOP. SKILL:39 limits it to `--depth deep`; SKILL:138, 367, 383 apply it to every depth; observed at `quick` | SKILL:39 against SKILL:138, 367, 383 | `sc-auggie-review.md` lines 28, 137 |
| 12 | Command vs skill | `/sc:auggie-review`: CMD says `standard` adds "Claude synthesis"; the skill has no step gated on standard | CMD:51 against SKILL (grep) | `sc-auggie-review.md` lines 20, 135 |
| 13 | Command vs skill | `/sc:auggie-review`: `--force` and `--resume` exist in the skill and the remediation ref but not in the command's options or argument hint; `--focus cicd` was used and is in neither list; the implicit `--diff` on a dirty tree is stated only in CMD; `--auggie-model` against the `AUGGIE_MODEL` variable | CMD:8, 27, 50, 57 against SKILL:26-32, 138, 172; REM:195-214 | `sc-auggie-review.md` lines 17, 19, 26, 28-29, 139-142 |
| 14 | Command vs skill | `/sc:adversarial`: the skill says STOP when `--agents` is combined with `--compare`, then says Mode A advocates default to the current model if `--agents` is not given | SK:555 against SK:1032, AS:191 | `sc-adversarial.md` lines 24, 167 (U1) |
| 15 | Internal inconsistency | `/sc:adversarial` protocol: the rubric is 30 criteria in some places and "25-criterion" in others; the probe is 6 categories at one line and 5 at another; `--dry-run` is in the skill but not in the command's option table; roadmap refs say "5+ agents triggers orchestrator" while the skill always uses the debate orchestrator | SK:1669, 1740 against SK:1753, 1756, DP:192, AT:201; SK:1110 against SK:1307; SK:2546 | `sc-adversarial.md` lines 36, 173 (U7) |
| 16 | Undefined flag | `/sc:adversarial`: `--suspect-source` is named as the next step by `sc-bare-review` and defined in no adversarial file; `invocation_method: manual` and the path of the return contract are undefined | `sc-bare-review/SKILL.md:3, 18, 55`; SK:427, 459 | `sc-adversarial.md` lines 37, 132, 170-171 |
| 17 | Command vs skill | `/sc:pr-submit`: `--yes` exists in the core parser and one ref only, not in the command's argument hint or the skill's required input; attaching to an existing PR number is allowed with no flag defined | fsm.py:97; refs/state-machine.md:155-159; CMD:27, SKILL:136 | `sc-pr-submit.md` lines 42, 44, 137-138 |
| 18 | Command vs skill | `/sc:pr-submit`: Wave 6b is labelled "L2+" in the skill while the state-machine edges are not ordinal-gated in text; the oversized-PR fallback report is auto-posted according to one ref, and the skill does not mention the post | SKILL:196; refs/state-machine.md:108-111; refs/auggie-fallback.md:35 | `sc-pr-submit.md` lines 131, 134 (U3, U6) |
| 19 | Internal inconsistency | `/sc:pr-submit`: the 8 observed run logs use the key `event` and lack `schema_version`, `event_id`, `run_id`, against the documented schema; the validation gates VG-1 to VG-5 (`uv run pytest`, `make test`, `make lint`, ...) cannot run in this repo (no Makefile, pyproject, src or tests), so predicate 2 of the L3 push gate cannot be met as written | refs/loop-guard.md:98-100; SKILL:205-209 | `sc-pr-submit.md` lines 50, 133, 136 |
| 20 | Repo state | `.dev/pr-monitor/detection-contract.locked.md` is tracked in this repo although the skill calls it a gitignored override | SKILL:190 | `sc-pr-submit.md` line 51 |
| 21 | Command vs skill | `/sc:release-split`: prerequisite 4 checks a source-tree path (`src/superclaude/skills/sc-adversarial-protocol/SKILL.md`) that does not exist here; the installed copy is under `~/.claude/skills/`; the check is unconditional, so it also applies to `--no-split` and `--resume-from`, which never call adversarial | SK:137 | `sc-release-split.md` line 149 (U3) |
| 22 | Internal inconsistency | `/sc:release-split`: the default second agent is `sonnet:analyzer` in CMD:60 and SK:92 but `haiku:analyzer` in AI:33; the artifact count is "4-6" in CMD:64 against 7 or 5 files in SK:41-55, 402; Part 4 is "6-point" in SK:332 against 8 checks in VP:9; the convergence threshold is 0.6 in SK:223 against (0.7, 0.5) in `sc-roadmap-protocol/refs/templates.md:321`; "smoke gate" is used in a flag and four places and never defined; the no-split path reads a "no-split rationale" that does not exist (SK:301) | as listed | `sc-release-split.md` lines 41-42, 102, 150-155 |
| 23 | Command vs skill | `/sc:brainstorm --handoff task` passes `--source` and `--template <x>-template` to `task-builder`, which defines neither flag nor the five template names, and passes no `--spec`; a task file made this way may record `reflect_pre: skipped` | SKILL:320-330; hr:206-225 against `task-builder/SKILL.md:33-43` | `sc-brainstorm.md` lines 31, 141-142 |
| 24 | Internal inconsistency | `/sc:brainstorm`: Wave 0 applies the "enterprise forces deep" rule before Wave 1 detects the strategy; runs on disk used 1 proposal and a "lightweight two-critic debate", below the protocol floor of 2 | SKILL:110, 123, 96 | `sc-brainstorm.md` lines 23, 110, 145-146 |
| 25 | Missing hook or file | `sc-research-protocol` does not exist, yet `/sc:brainstorm` and its handoff ref call it; the research command runs from its own file | SKILL:185-186; hr:49, 76 | `sc-brainstorm.md` lines 25, 143; `sc-research.md` lines 10, 106 |
| 26 | Wrong cross-reference | `/sc:brainstorm` cites a spec file `.dev/eval-workspaces/sc-brainstorm/SPEC.md` that is not on this machine, and Wave 0 reads a source-tree path for the adversarial skill | cmd:9; SKILL:103 | `sc-brainstorm.md` line 144 (U5) |
| 27 | Internal inconsistency | `/sc:design`: `--output` is passed by the auggie remediation call but not defined in the usage line (and omitted in the command's own examples of that call); `--format code` against Will Not "generate actual implementation code"; "Next Step: /sc:implement" is stale above single-task size; brainstorm calls design "interactive" while the file has no interaction step | RH:68-72, AR:137, 149; DS:22, 75-77, 98, 109 | `sc-design.md` lines 24, 132-135 |
| 28 | Wrong cross-reference | The `/sc:tdd` command file names `/sc:prd` (twice); no such command exists (the PRD step is `/prd` or `bmad-prd`) | CMD:172, 182 | `sc-tdd.md` lines 31, 146 |
| 29 | Internal inconsistency | `/sc:tdd`: Lightweight and Standard are worded differently in the command file and the skill (the command puts "Bug fixes, config changes" under Lightweight); the flags `--tier --resume --from-prd --prd --focus --output` are defined only in the command file; three QA report naming schemes; the template path `src/superclaude/examples/tdd_template.md` is not found and two other copies (1,240 and 1,310 lines) differ | CMD:43-51, 59-60 against SK:71-72; SK:109-110, OG:86-88, BR:121-149; SK:12, 112 | `sc-tdd.md` lines 12, 18, 103, 142-145; `sc-design.md` line 137 |
| 30 | Stale text | The `/sc:tdd` command file recommends `/sc:workflow` for post-TDD planning and `/sc:implement`, against the validated feature minimum; the Phase 7 offer creates tasks "using the `/task` skill" though `/task` only executes files | CMD:171, 184; BR:158 | `sc-tdd.md` lines 92, 147 |
| 31 | Wrong cross-reference | The `/sc:spec-panel` example block is built on `/sc:code-to-spec`, a command that does not exist (the only mention in `~/.claude`) | SP:415-419 | `sc-spec-panel.md` line 98 (P7) |
| 32 | Internal inconsistency | `/sc:spec-panel`: Whittaker "Review Order: 11" against 6 elsewhere in the same file; `--downstream` is in prose only, not in the usage line; the release template path is a source-tree path; "11 simulated experts" against sub-agent fan-out in `integration-map.md`; the `--iterations` Improve step against "will not modify specifications without explicit consent"; two sessions read the focus-to-expert mapping two ways | SP:22, 34, 82, 91, 106, 218, 234-252, 451, 457; integration-map.md:64 | `sc-spec-panel.md` lines 107-114 |
| 33 | Stale text | The `/sc:research` next step ("use `/sc:design` ... or `/sc:implement`") skips the tasklist step and disagrees with the guide (report goes to `/task-builder`); the default `--depth` is documented nowhere | CMD:142 against HW:308; CFG:5-13 | `sc-research.md` lines 55, 97 |
| 34 | Stale text | `/sc:workflow` and its refs still name `/sc:tasklist`; the guide says `--depth quick` "checks the plan against your request automatically", but the check is the advisory Wave 4 reflect and the quick gate lacks requirement coverage; WF:54 names a source-tree path | WF:54, 74, 80; OR:8; HW:17; QG:26-29 against QG:39 | `sc-workflow.md` lines 125, 190-191, 193 |
| 35 | Internal inconsistency | `/sc:implement`: real managed ledgers contain record kinds the installed grammar never defines (`T12: halt review=`, `T14: retry n=`); `.dev/tasks/archive/` is unexplained; `--resume` has no handling beyond the known-option list; IM:83 cites a source-tree path | `refs/ledger.md:56`; IS:49; IM:83 | `sc-implement.md` lines 21, 129, 165-166, 174 |
| 36 | Internal inconsistency | `/sc:spawn`: the behavioral flow and Will say it executes, the closing section says "STOP AFTER TASK DECOMPOSITION"; `--strategy` and `--depth` defaults and effects are not stated; Rule 2.5 is inert here and cites a path in another repository | CMD:30-31, 76, 182, 192-201 | `sc-spawn.md` lines 17-18, 22, 26, 93, 95 |
| 37 | Wrong cross-reference | `/sc:swarm-wizard`: the refactor-find hand-off names `/sc:code-review --apply`, which has no command file; `--custom-prompt-dir` is a stale doc claim; whether `--yes` skips the real-run go-ahead is not stated | CC:44, 117; INT:65; CMD:55, 87 | `sc-swarm-wizard.md` lines 24, 47, 83, 125, 130 |
| 38 | Internal inconsistency | `/sc:cleanup`: promises "backup and rollback capabilities" with no flag or mechanism; `--preview` appears in one example and not in the usage line; "zero references" has no stated method; whole-file removal is in neither the auto-fix nor the approval list; `--aggressive` has no definition | cleanup.md:22, 38, 73, 98, 109-121 | `sc-cleanup.md` lines 22, 24, 28, 107-113 |
| 39 | Command vs skill | `/sc:cleanup-audit`: Pass 1 model is Haiku in the command and the skill but `model: sonnet` in `audit-scanner.md`; four of five audit agents have Read/Grep/Glob only and `permissionMode: plan`, yet the protocol says each writes its report | CA:43; SK:68, 74, 94 against AG:audit-scanner.md:4-7 | `sc-cleanup-audit.md` lines 133, 159-160 |
| 40 | Internal inconsistency | `/sc:cleanup-audit`: preprocessing lines use `${0:-.}` not `$ARGUMENTS`; `--batch-size` is one number in the script and three per-pass defaults in the command; `SCOPE.md` is read from different places; a 9th "wiring" field exists in the agent files and not in the rules; resume is claimed automatic while `sc-crash-recovery` says audits have no fine-grained resume | CA:25-26, SK:47-48; CA:38 against INV:12; SK:64 against INV:13; pipelines.md:203-205 | `sc-cleanup-audit.md` lines 162-166, 172-174 |
| 41 | Undefined flag | `/sc:improve`: `--safe` and `--interactive` are named in the usage line and made mandatory by the guide's cleanup row, yet defined in no file read; `--preview`, `--validate`, `--force` appear only in examples or a boundary line; `--type security` is used in an example and is outside the enum; "rollback" and "backup" have no mechanism | IMP:22, 65-92, 100, 125; HW:318 | `sc-improve.md` lines 34-38, 117-121 |
| 42 | Undefined flag | `/sc:test`: `--fix` ("automatic simple failure fixes") is not reconciled with Will Not "destructive changes to test files without explicit permission"; the report path for "coverage reports and test summaries" is undefined; `--watch` in a non-interactive session is unstated; the guide makes `--coverage` mandatory for bug step 3a though no coverage tooling exists at this repo's root | cmd:52, 89-90, 104-106; HW:311 | `sc-test.md` lines 21-23, 106-109 |
| 43 | Undefined flag | `/sc:build`: `--validate` appears only in an example, not in the usage line; the report path is undefined | build.md:22, 52, 90 | `sc-build.md` lines 22, 27, 102-103 |
| 44 | Internal inconsistency | `/sc:git`: the command file is silent on staging and on `.dev/tasks`, and does not say whether `push` asks first (its guard covers destructive operations only) | CMD:14, 49, 89 | `sc-git.md` lines 85, 107-108 |
| 45 | Internal inconsistency | `/sc:analyze`: its next step is `/sc:improve` or `/sc:cleanup` while the cleanup route starts with `/sc:cleanup-audit`; `--format report` "Generates HTML report" against "Analysis report"; Bash is listed while dynamic analysis is excluded; `/sc:release-split` Part 4 delegates fidelity verification to analyze, which defines no source-versus-output comparison | CMD:45, 76-78, 99, 103-109, 111; HW:318 | `sc-analyze.md` lines 20, 58, 62, 103 |
| 46 | Internal inconsistency | `/sc:explain`: no `allowed-tools` key, so "changes no files" rests on the guide, not on enforcement; `--format interactive` is undefined | CMD:1-8, 57, 80 | `sc-explain.md` lines 30, 94-95 |
| 47 | Command vs skill | `/sc:post-release`: the command's `allowed-tools` (Read, Glob, Grep, Skill) is narrower than the skill needs (Edit, Write, Bash, Task, TodoWrite); the "release gate that tags a version" is undefined and no workflow here tags; the default output directory `docs/testing/<version>/` does not exist here, so a confirm prompt is certain | CMD:3, 6, 15, 36; SKILL:4 | `sc-post-release.md` lines 27, 37, 40, 138-139 |
| 48 | Internal inconsistency | `/sc:document` neighbours: `tech-reference` puts "multiple subsystems" in Standard and also says it is always Heavyweight; `operational-guide` moves a finished folder to `.dev/tasks/completed/` while the repo uses `done/`, and its default folder `docs/docs-product/ops/` does not exist here | TR:88, 95; OG:48, 61 | `sc-document.md` lines 27, 105-106 |
| 49 | Retired-command handoff | `/sc:brainstorm --handoff tasklist` calls `sc-tasklist-protocol`; the `--handoff none` "Next:" text still suggests `/sc:tasklist` and `/sc:implement @merged-requirements.md` | SKILL:311, 315-318; hr:164-166 | `sc-brainstorm.md` lines 31, 87 |
| 50 | Retired-command handoff | `/sc:workflow --handoff tasklist` prints `/sc:tasklist --source <roadmap>`; WF:74, WF:80 and OR:8 name it; the implement command file does too | WF:74, 80; OR:8; IM:138 | `sc-workflow.md` lines 22, 125, 191 |
| 51 | Retired-command handoff | `/sc:release-split` Part 3 offers `/sc:tasklist` and `/sc:workflow`; SK:275 already says not to use `/sc:tasklist` unless the proposal says so | SK:35, 105, 270-275; CMD:136 | `sc-release-split.md` lines 26, 81-82, 136-137 |
| 52 | Retired-command handoff | `/sc:adversarial` lists `/sc:tasklist` as a related command ("Pipeline output as sprint input") | adversarial.md:182 | `sc-adversarial.md` lines 9, 119 |
| 53 | Retired-command handoff | `/sc:reflect` names `/sc:task` as an "end-of-task hook" (marked deferred) and `/sc:tasklist` as a consumer row | CMD:309; SKILL:54, 1006-1008 | `sc-reflect.md` lines 9, 140 |
| 54 | Retired-command handoff | `/sc:roadmap` and its refs end in `/sc:tasklist`: See Also, "future tasklist generator", the `estimated_phases` hint, the `tasklist_ready` field. Retirement is recorded in no file; the tasklist command and skill carry no deprecation text | CMD:102-103; PRO:36, 383-385; R-TPL:394; R-VAL:32 | `sc-roadmap.md` lines 125-130, 201 |
| 55 | Retired-command handoff | `/sc:validate-roadmap` points at `/sc:tasklist` as the next step; `tasklist_ready` and the "Parseability" dimension serve the retired splitter | VR:103; VP:37, 76, 969-971 | `sc-validate-roadmap.md` lines 12, 92, 107 |
| 56 | Retired-command handoff | `/sc:spec-panel --downstream roadmap` feeds the pipeline that ends in `/sc:tasklist` | SP:36, 272, 280 | `sc-spec-panel.md` lines 25, 115 |
| 57 | Retired-command handoff | `/sc:troubleshoot` keeps `--context` and `--caller task-unified` for the retired `/sc:task` | SKILL:153, 537; `sc-task-protocol/SKILL.md:217` | `sc-troubleshoot.md` lines 8, 25-26 |
| 58 | Retired-command handoff | `/sc:spawn` Rule 2.5 mentions `/sc:task` in an exclusion clause | CMD:124 | `sc-spawn.md` line 24 |
| 59 | Retired-command handoff | `sc-crash-recovery/refs/pipelines.md` tells the user to run `/sc:task <MDTM file path>` for old tasks while its own line 179 says workflow packages go "never to MDTM `/task` or `/sc:task`"; whether `/sc:task <file>` works is unverified | pipelines.md:25, 39, 173, 179 | `validation-oneoff-sc-task-vs-sc-implement.md` lines 63, 147 |
| 60 | Retired-command handoff | The guide names `/sc:task` as the level-2 tool and in the routing row `small-change` | HW:16, 119, 242, 285, 304 | `validation-oneoff-sc-task-vs-sc-implement.md` line 64 |
| 61 | Retired-command handoff | `/sc:tasklist` Stage 9 invokes `/sc:task --compliance strict` through the Skill tool and loops back; this is the only programmatic caller found, so deleting the `/sc:task` skill would break it | `skills/sc-tasklist-protocol/SKILL.md:1535-1557, 1607` | `validation-oneoff-sc-task-vs-sc-implement.md` line 60; `sc-roadmap.md` line 129 |
| 62 | Retired-command handoff | `/sc:post-release` reuses "the project's" itemized-tasklist tool if loadable and names none; on a machine where `/sc:tasklist` still loads it could be picked | SKILL:153-159 | `sc-post-release.md` line 141 (U5) |
| 63 | Undefined flag | The guide makes `/sc:analyze --focus` mandatory though the command marks it optional; makes `/sc:research --depth deep` mandatory with no documented default; always passes `/sc:spec-panel --mode critique` with no stated default | HW:312-313; CMD:22 (analyze) | `sc-analyze.md` line 18; `sc-research.md` lines 20, 97; `sc-spec-panel.md` lines 20, 106 |
| 64 | Wrong cross-reference | `task-builder/SKILL.md` line 1668 says `/sc:roadmap` invokes `/task-builder`; it is `/roadmap` that does | TB:1668 against RM:8, RM:660 | `sc-roadmap.md` lines 112, 185 |
| 65 | Internal inconsistency | `task-builder/SKILL.md`: the research gate scales with `qa_intensity` ("lite: 2, standard: 3, full: 5") while two other places say "minimum 5"; which intensity a user-invoked build gets is unclear | TB:204, 691, 693, 1000, 2345 | `validation-feature-task-builder-vs-sc-workflow.md` lines 52, 286 (V3) |
| 66 | Wrong cross-reference | Source-tree paths cited in installed files that do not exist on an engineer's machine: `src/superclaude/skills/...` (workflow, implement, reflect, brainstorm, release-split), `src/superclaude/examples/tdd_template.md`, `src/superclaude/examples/release-spec-template.md` | WF:54; IM:83; reflect CMD:153; brainstorm SKILL:103; release-split SK:137; SK:12, 112 (tdd); SP:218 | `sc-workflow.md` line 190; `validation-oneoff-sc-task-vs-sc-implement.md` line 150; `sc-reflect.md` line 204; `sc-tdd.md` line 145; `sc-spec-panel.md` line 114 |
| 67 | Wrong cross-reference | `/sc:spawn` cites a path that belongs to another repository (`.dev/releases/current/test_obligation_scanner_meta_context-fixes/PHASE0-MITIGATION-DEBATE.md`) | CMD:76 | `sc-spawn.md` line 95 (U5) |
| 68 | Missing hook or file | `offer-pr-review.sh` is named by `/sc:auggie-review` and `/sc:pr-submit` but is not in `~/.claude/hooks/` or `settings.json`, and `find` finds none, so the "offer after PR create" trigger does not exist here | auggie CMD:18; `pr-submit.md:19`; SKILL:189 | `sc-auggie-review.md` lines 103, 146; `sc-pr-submit.md` lines 105, 135 |
| 69 | Missing hook or file | The guide says the routing table "is read by `/sc:recommend` and checked by tests"; no test was found (reported by the main file and two nuance files) | HW:297 | main file U18 (line 302); `sc-test.md` line 115; `sc-improve.md` line 129 |
| 70 | Missing hook or file | Documents linked by the swarm files are not installed here: IronClaude `docs/swarm/wizard-guide.md` and `.dev/swarm-wizard/SWARM-WIZARD-FACTS.md` | HW:154; CC:3 | `sc-swarm-wizard.md` line 134 (U13) |
| 71 | Missing hook or file | Twelve of the 27 commands have no backing protocol skill (listed in 6.7), so their flags and defaults are defined only in the one command file, if at all | `~/.claude/skills/` | 6.7 below |
| 72 | Stale text | Main file: how `/sc:git --smart-commit` treats `.dev/tasks` staging is marked UNVERIFIED (lines 163, 241, 296); the command file is silent on staging | main file lines 163, 241, 296 | `sc-git.md` lines 85-98 |
| 73 | Stale text | Main file: whether the team runs `superclaude sprint run` is marked UNVERIFIED (line 114, U6 at line 290); a full run is on disk (`execution-log.jsonl` `sprint_start` 2026-05-17, archived 2026-06-24) | main file lines 114, 290 | `sc-roadmap.md` lines 131, 190; `sc-validate-roadmap.md` line 127 |
| 74 | Stale text | Main file: whether the team tags versions is marked UNVERIFIED (U14, line 298); two annotated tags exist and `/sc:post-release` ran once | main file line 298 | `sc-post-release.md` line 128; `sc-release-split.md` line 139 |
| 75 | Stale text | Main file: whether `bmad-technical-research` searches the web or the code is marked UNVERIFIED (line 85, U8 at line 292); it requires web search | main file lines 85, 292 | `sc-research.md` lines 56, 89, 91 |
| 76 | Stale text | Main file: the troubleshoot report path is `.dev/troubleshoot/<name>-<timestamp>/REPORT.md` (lines 175, 271); the real slug is `<type>-<first-5-words>-<YYYYMMDDHHMMSS>` and 10 of 32 observed folders are hand-named | main file lines 175, 271 | `sc-troubleshoot.md` lines 81, 106 |
| 77 | Stale text | Main file: the post-mode `/sc:reflect` folder and the `/sc:pr-submit` run-log location are marked UNVERIFIED (U13, line 297); both are now answered: the same default folder pattern for both reflect modes, and a run log at `<cwd>/.dev/pr-monitor/pr-<N>-<timestamp>/` (moved by `--output-dir`) | main file line 297 | `sc-reflect.md` lines 164, 189; `sc-pr-submit.md` lines 48-49, 122 |
| 78 | Stale text | Main file Section 5 intro (line 281) says about a dozen commands were read only by usage and flag lines; each nuance file now records a full read of its command file | main file line 281 | section 7 of `sc-test.md`, `sc-design.md`, `sc-reflect.md`, `sc-tdd.md`, `sc-workflow.md`, `sc-spec-panel.md`, `sc-brainstorm.md`, `sc-git.md`, `sc-auggie-review.md` |
| 79 | Stale text | Main file: the existing technical reference is cited as evidence of `/tech-reference` use (line 189); the file says a retrospective gate produced it | main file line 189 | `sc-document.md` lines 71, 87 |
| 80 | Stale text | Main file U16 (`/sc:code-to-spec` in the spec-panel example) is confirmed: the only mention in `~/.claude`, no such command | main file line 300 | `sc-spec-panel.md` line 98 |
| 81 | Stale text | Main file: the `/sc:cleanup-audit` Notes "Report only (`--pass all`)" reads as if `--pass all` makes it report-only; every pass is read-only | main file line 155 | `sc-cleanup-audit.md` line 147 |
| 82 | Stale text | Main file: Augment review app presence is marked UNVERIFIED (U4, line 288); indirect evidence now exists: a run log for PR 286 shows an Augment poll reaching `review_present` on 2026-10-02 | main file line 288 | `sc-pr-submit.md` lines 121, 139 |
| 83 | Repo state | `.gitignore:32` is `reflect/` (no leading slash), which matches at any depth, so new `reflect/` report folders under `.dev/tasks/` are not staged by `git add .dev/tasks`; existing ones are tracked anyway | `.gitignore:32` | `sc-reflect.md` lines 170, 203 |
| 84 | Repo state | `/sc:auggie-review` with a PR number posts a public review and inline comments with no prompt and quotes diff code; a secret in the diff becomes a Critical finding with an inline comment, against this repo's PR #57 incident; review folders (140 tracked files) can carry raw Auggie output and quoted diffs, and the secrets rules do not mention `.dev/reviews/` | CMD:52; SKILL:253-255; SEV:17, 22; `CLAUDE.md` Secrets discipline | `sc-auggie-review.md` lines 21, 70, 101, 145 |
| 85 | Repo state | `/sc:cleanup` has no exclusion list, so `.dev/`, `_bmad-output/` and `.github/` are not protected, while `/sc:cleanup-audit` never sees hidden paths or `_bmad*` (94.6 percent of tracked files here) and leaves an untracked `.claude-audit/` | cleanup.md; SK:54-65; INV:20 | `sc-cleanup.md` lines 17, 62, 81; `sc-cleanup-audit.md` lines 54, 60, 130, 147 |
| 86 | Repo state | `.dev/implement/` is not gitignored; the 4 observed ledgers are tracked only through bulk commits, against "Do not `git add` the ledger" | LG:3 | `validation-oneoff-sc-task-vs-sc-implement.md` lines 116-117; `sc-implement.md` line 132 |
| 87 | Internal inconsistency | Three tables in the nuance files carry an unescaped pipe inside a cell (the `--type quality|maintainability` and `--focus quality|performance` flag text), so they render with an extra column. They are copied unchanged into 6.3 because that subsection is verbatim | 6.3.17 `/sc:improve` (scope matrix, T row; neighbour table, `/sc:analyze` row); 6.3.24 `/sc:analyze` (scope matrix, N row) | `sc-improve.md` lines 54 and 72; `sc-analyze.md` line 47 |

### 6.6 Decisions waiting for Ryan

Collected from the nuance files, the two validation files and `scenarios.md`. Each item gives the question in one sentence, where it came from, and the answer the files recommend if they give one. "(J)" marks a recommendation that is an agent's judgment, not a file's statement. Nothing below has been decided.

1. What counts as a "story"? Source: `validation-feature-task-builder-vs-sc-workflow.md` lines 138 and 291 (V8). Recommended: none in the files; "multi-story" is the lead's term, and the BMad lane keeps story files under `_bmad-output/implementation-artifacts/` (main file line 26).
2. Is exactly two sessions level 3 (`/sc:workflow`) or level 4 (`/task-builder`)? Source: `validation-feature-task-builder-vs-sc-workflow.md` lines 12, 143 and 292 (V9); `command-nuance/sc-workflow.md` line 97. Recommended: the only rule on disk is "choose the heavier one" (HW:9); `sc-workflow.md` line 97 suggests a checker accept either command at the tie (J).
3. Confirm the one-off minimum: a plain edit plus the related test, with `/sc:implement "<prompt>"` as an optional add-on that leaves a ledger? Source: `validation-oneoff-sc-task-vs-sc-implement.md` lines 8 and 138; `command-nuance/_brief.md` line 16; relied on as "proposed" in `sc-implement.md` line 172, `sc-cleanup.md` line 120, `sc-troubleshoot.md` line 113. Recommended: yes; the guide itself says level 2 is "or a plain edit" (HW:16, 304).
4. Where does the checker read "pushed" from, since `/sc:pr-submit` opens the PR and does not push the branch? Source: `command-nuance/sc-pr-submit.md` lines 10 and 108. Recommended: count the PR step as done when a PR exists for the branch, and take push evidence from git; the guide has the engineer push first (HW:202-204).
5. Is an audit required before `/sc:cleanup` on a small target (the 50-file rule)? Source: `command-nuance/sc-cleanup-audit.md` lines 138 and 167 (U9); HW:318. Recommended (J): no audit for 50 in-scope files or fewer; audit first for 51 or more, whole-file deletions or unknown referrers. The guide's routing row lists `--pass all` as mandatory, so a strict checker would flag the lenient path.
6. May several single-story `/sc:workflow` plans stand in for one `/task-builder` run at feature size? Source: `command-nuance/sc-workflow.md` lines 104-117 and 177 (U1); `validation-feature-task-builder-vs-sc-workflow.md` line 155. Recommended (J): tolerate it, never as the feature minimum, and only when all six conditions in 4.2 of `sc-workflow.md` hold.
7. Is `/sc:spawn` OPTIONAL at R/HIGH (a batch of independent items), or out of the pipeline for good? Source: `command-nuance/sc-spawn.md` lines 42-48 and 80-82. Recommended (J): OPTIONAL at most, never expected; the one precedent (`.dev/plans/top9-issues-20261001/spawn-runbook.md`) has no proof the command was invoked (U1, line 91).
8. Is the whole `/sc:roadmap` pipeline (with `/sc:validate-roadmap`) retired together with `/sc:tasklist`, and what carries a `/sc:roadmap` output into tasks now? Source: `command-nuance/sc-validate-roadmap.md` line 140; `sc-roadmap.md` lines 200 and 206 (U3, U9). Recommended: none in the files; `sc-roadmap.md` lines 84 and 128 treat it as a planning-artifact generator whose output a person carries to `/task-builder` or `/roadmap`.
9. How should a checker treat handoff flags and printed next steps that still name retired commands? Source: `command-nuance/sc-brainstorm.md` line 117; `sc-workflow.md` line 191; `sc-roadmap.md` line 201 (U4); rows 49 to 62 of 6.5. Recommended (J): flag only an engineer running `/sc:tasklist` or `/sc:task`, or passing `--handoff tasklist`; ignore printed suggestions; mark the installed files, since the retirement is recorded in none of them.
10. Where does the job read the size label from: the story file, the branch, or the first prompt? Source: `scenarios.md` lines 81-82. Recommended: none; the file leaves it open "to discuss with Ryan".
11. What is the minimum path for R (a multi-feature release)? Source: `command-nuance/sc-release-split.md` line 134; `sc-roadmap.md` line 187; `sc-workflow.md` line 171; `sc-reflect.md` line 182 (see C18 in 6.4). Recommended (J): per-feature F pipelines plus release-level review and push (`sc-release-split.md` line 134); the old three-step minimum assumes already-built work.
12. Is `/sc:troubleshoot` required for every bug, or optional when a failing test already names the cause? Source: `command-nuance/sc-troubleshoot.md` lines 49, 101 and 113; HW:311. Recommended (J): optional at B-LOW (known cause, one source file plus its test, deterministic); required at MEDIUM and HIGH.
13. What `--monitor` level counts as normal for `/sc:pr-submit`, and should 2 or 3 be flagged? Source: `command-nuance/sc-pr-submit.md` lines 77-78 and 109. Recommended: the guide says 1; the file suggests a separate "deviates from guide" note, not a skipped-step flag (line 109).
14. Adopt, amend or reject the (J) bands and the Y rows of 6.2, including every R re-rating? Source: the band and (J) items of all 27 files (for example `sc-brainstorm.md` line 140, `sc-workflow.md` line 178). Recommended: none; all are proposals.
15. Should commands with no on-disk footprint and no REQUIRED cell be written down as never expected and never penalised? Source: `command-nuance/sc-explain.md` line 87 (P2); same stance in `sc-build.md` line 76, `sc-analyze.md` line 77, `sc-improve.md` line 96, `sc-spawn.md` line 72. Recommended (J): yes, as one line in the rating rules.
16. Is running `/sc:implement` on a task-builder file a tool-enforced stop or only a pairing convention a checker may flag? Source: `command-nuance/sc-implement.md` lines 54 and 167 (U5); `validation-feature-task-builder-vs-sc-workflow.md` line 42 (see C1). Recommended (J): treat it as a convention and flag it as the wrong lane, not as a skipped step (`sc-implement.md` line 140).
17. Should `progress.md` ledgers be staged, given "Do not `git add` the ledger" against "`.dev/tasks/` is always staged", and what about the untracked `.dev/implement/`? Source: `validation-feature-task-builder-vs-sc-workflow.md` line 295 (V12); `validation-oneoff-sc-task-vs-sc-implement.md` line 117 (F3); `sc-workflow.md` line 189. Recommended: none; `sc-workflow.md` line 146 says a staged-files check should not treat `progress.md` as a defect either way.
18. Should the `reflect/` pattern in `.gitignore:32` be narrowed so new report folders are staged? Source: `command-nuance/sc-reflect.md` lines 170 and 203 (U9). Recommended: none; the durable record in git is the `reflect_pre` and `reflect_post` frontmatter.
19. Are `.claude-audit/` reports committed or ignored? Source: `command-nuance/sc-cleanup-audit.md` line 130; `sc-cleanup.md` line 81. Recommended: none; the folder is untracked here by default, so a checker that reads only the PR will not see an audit.
20. Do `.dev/reviews/` folders (140 tracked files with raw Auggie output) fall under the secret scan, and who commits them? Source: `command-nuance/sc-auggie-review.md` lines 101 and 145 (U11). Recommended: none; read the gitleaks workflow.
21. Should `/sc:auggie-review` with a PR number always use `--no-post-pr`? Source: `command-nuance/sc-auggie-review.md` lines 21 and 123. Recommended: yes; the default posts a public review that quotes diff code, with no prompt.
22. May `/sc:cleanup` run with `--type files` or `--type all`, with `--aggressive`, with no explicit folder, or on `.dev/`, `_bmad-output/`, `.github/`? Source: `command-nuance/sc-cleanup.md` lines 17-20, 62 and 88-89. Recommended (J): no; use `--type code --safe --interactive` on an explicit folder after a commit, and audit first for whole-file deletions.
23. Is a single-file `/sc:improve` with more than 5 edits inside the guide's folder exception, and what is "small, contained"? Source: `command-nuance/sc-improve.md` lines 123-124. Recommended: none in the files.
24. May engineers use `--handoff implement` on `/sc:workflow` or `--handoff task` on `/sc:brainstorm`? Source: `command-nuance/sc-workflow.md` line 22; `sc-brainstorm.md` lines 31 and 141. Recommended (J): use `--handoff none` and take the next step by hand; `implement` skips the human read of the plan, and `task` passes no `--spec`.
25. Should a checker require the named `/sc:test` step at B-LOW? Source: `command-nuance/sc-test.md` lines 81-82. Recommended: count the activity ("related test run, or CI green"), not the command; `/sc:test` leaves no footprint.
26. Do `bmad-review-adversarial-general` and a recorded NO-GO count as "spec critique" and as a deliberate skip? Source: `command-nuance/sc-spec-panel.md` lines 56, 79 and 83-84; `scenarios.md` line 34. Recommended (J): yes to both.
27. May the design step use both lanes (`bmad-architecture` and then `/tdd`)? Source: `command-nuance/sc-tdd.md` lines 86 and 128; main file line 223 (see C6). Recommended (J): yes at HIGH F, R and N; pick one at LOW and MEDIUM; a checker must not flag `/tdd` after `bmad-prd`.
28. Which artifact counts as the recorded split decision for a release, and does a BMad milestone plan count? Source: `command-nuance/sc-release-split.md` lines 108 and 159 (U13). Recommended (J): accept `release-split/` outputs, a milestone or revised-plan document that states the scope cut, or an explicit one-release statement in the release plan.
29. When is `/sc:post-release` expected, and after what grace period? Source: `command-nuance/sc-post-release.md` lines 111 and 143 (U7). Recommended (J): only at R or N with a new git tag that has no manifest; tags only (not payload `VERSION` stamps); no grace period is set by any file.
30. Does the swarm proxy need a presence check, and does a stub dry run count as a review? Source: `command-nuance/sc-swarm-wizard.md` lines 96, 102 and 122 (U1). Recommended: check variable names only, never values; a stub-only folder means "wizard practised", not a cross-model review.
31. How many commits per phase should a checker expect, and is one commit for a multi-phase branch a deviation? Source: `command-nuance/sc-git.md` lines 82 and 109 (U3). Recommended (J): at least one per task-file phase; one commit for a multi-phase F, R or N is a reportable deviation.
32. When does a spec-panel loop stop? Source: `command-nuance/sc-spec-panel.md` lines 83 and 116 (U11). Recommended: none beyond "until no critical findings remain" (HW:61); the observed orca spec ran four more rounds after CRITICAL reached 0.
33. Which wording is intended for plain `/sc:troubleshoot --fix`: a task file (the guide) or a `/sc:workflow` plan (the command)? Source: `command-nuance/sc-troubleshoot.md` lines 110 and 123. Recommended: the nuance file treats the command file as the source (see C13).
34. Does a PR opened with plain `gh pr create` or the web UI count as the PR step? Source: `command-nuance/sc-pr-submit.md` line 108. Recommended: yes when a PR exists for the branch; do not flag a missing run log or monitor at levels 0 and 1.
35. Are run folders committed (`.dev/brainstorms/`, `.dev/troubleshoot/`, `.dev/reviews/`, `.dev/swarm-runs/`, `.dev/pr-monitor/`), and may the checker read an engineer's uncommitted workspace? Source: `command-nuance/sc-brainstorm.md` lines 104 and 150 (U11); `sc-troubleshoot.md` line 89; `sc-swarm-wizard.md` lines 98 and 131 (U10); `sc-pr-submit.md` line 51. Recommended: none; the answer decides whether runs are visible in PRs or only in the engineer's workspace.
36. Which hand-run `/sc:reflect --mode post --no-promote` runs are expected: after each phase at N, HIGH F and R, plus one whole-release run at R? Source: `command-nuance/sc-reflect.md` lines 173 and 182. Recommended: the per-phase run at N is stated by the guide (HW:81-83, 309); the F-HIGH and R expectations and the whole-release run are (J).

### 6.7 Coverage and gaps

No agent ran any command; every nuance file is a reading of files, and every footprint outside a file the agent opened is UNVERIFIED. The nuance files describe one checkout and one `~/.claude`; another engineer's copies may differ (the guide's own header says `superclaude update` refreshes it). Each of the 27 files has all eight sections, so nothing was missing to copy; the structural differences are listed at the end of this subsection.

**Commands whose agents did not read all of their references** (the full read of the command file itself is recorded in every file unless stated):

| Command | Not read, or read in part | Stated in |
|---|---|---|
| `/sc:troubleshoot` | 10 of 18 refs unread: `calibrator-eval-cases`, `contract-enumeration`, `doc-discovery`, `effective-input-proof`, `environment-deltas`, `hardening-output-contract`, `primitive-differential`, `runtime-entrypoint-verification`, `unmask-and-sweep`, `probe-packs/read-parse`. Five refs read in full; `report-template`, `diagnosability-audit`, `hypothesis-card-template` read in part | `sc-troubleshoot.md` lines 4, 114 |
| `/sc:brainstorm` | Protocols of `sc-adversarial`, `task-builder` (flags and TCS section) and `sc-release-split` read by grep only; persona agent files not found | `sc-brainstorm.md` lines 5, 148 |
| `/sc:design` | `bmad-architecture` `references/reviewer-gate.md`, `references/headless.md`, `assets/spine-template.md` not read in full; the rest of release-split Part 3 and its `refs/phase-templates.md` not read | `sc-design.md` lines 136, 139 |
| `/sc:tdd` | `bmad-architecture` `references/` not read; `rf-task-builder` agent file not read; `/task` SKILL not re-read | `sc-tdd.md` lines 4, 144, 148, 152 |
| `/sc:research` | `bmad-domain-research` and `bmad-market-research` not read | `sc-research.md` line 104 |
| `/sc:release-split` | Adversarial depth lines, the brainstorm command's flag lines, one line of the roadmap templates and about 40 lines of the task-builder TCS section read by grep only | `sc-release-split.md` line 163 |
| `/sc:workflow` | `task-builder` read only at lines 134-146, 288-324, 2402-2445; `bmad-create-story` first 60 lines; `sc-reflect-protocol` not read | `sc-workflow.md` lines 182, 186-187 |
| `/sc:roadmap` | `/roadmap` skill read at lines 1-200 and 2610-2678 plus grep of its 2678 lines; `sc-tasklist-protocol` Stage 9 and 10 only; the Python CLI source (`executor.py`, `gates.py`, `prompts.py`) never opened | `sc-roadmap.md` lines 9-10, 199, 212 |
| `/sc:reflect` | Wrapper source, `reflect-reviewer`, `confidence-calibrator`, `evidence-validator` agent files not read; `refs/grader-extensions.md` past line 80 (eval-only) not read | `sc-reflect.md` line 210 |
| `/sc:validate-roadmap` | CLI source `validate_prompts.py` not opened; `superclaude roadmap validate --help` read to 5 lines; names only of the v1.3 `validation/` folder | `sc-validate-roadmap.md` lines 136, 144-145 |
| `/sc:swarm-wizard` | IronClaude `docs/swarm/wizard-guide.md` and `SWARM-WIZARD-FACTS.md` not installed here; live `--help` not run | `sc-swarm-wizard.md` lines 124, 134 |
| `/sc:implement` | Complete for command, skill and three refs; the archive script `archive_workspace.py` appears in the citation key and is not stated as read (`validation-feature-task-builder-vs-sc-workflow.md` line 293, V10, says it was not read) | `sc-implement.md` line 5 |
| `/sc:test` | CI workflows read in part (lines 1 and 1158-1163 of one); `bmad-dev-story` and `bmad-quick-dev` not read | `sc-test.md` lines 111-113 |
| `/sc:build` | Other workflows grepped for build commands only; `test-18-docker-cli-presence.sh` not opened; one `.specstory` file not opened | `sc-build.md` lines 105, 108-109 |
| `/sc:improve` | `/sc:analyze`, `/sc:adversarial` and the `sc-recommend` refs read by grep only; the `/sc:troubleshoot` command file not read | `sc-improve.md` lines 9-15, 127 |
| `/sc:cleanup` | `settings.json` (45 KB) not read in full when searching for a deny rule | `sc-cleanup.md` line 116 |
| `/sc:cleanup-audit` | `audit-analyzer.md` and `audit-comparator.md` frontmatter only; `/sc:analyze`, `/sc:auggie-review` and `/simplify` neighbours not read in full | `sc-cleanup-audit.md` lines 7, 170 |
| `/sc:auggie-review` | `bmad-code-review` step-03 triage file and `customize.toml` not read | `sc-auggie-review.md` line 148 |
| `/sc:document` | Neighbour skills read in part: `tech-reference` lines 1-420 and 536-545, `operational-guide` 1-200, `readme` 1-200; agent prompts and QA details unread | `sc-document.md` lines 5, 104 |
| `/sc:post-release` | Neighbour skills (`tech-reference`, `operational-guide`, `readme`, `sc:document`, `bmad-qa-generate-e2e-tests`) known from descriptions only | `sc-post-release.md` lines 75, 140 |
| `/sc:explain` | `bmad-document-project` and the persona definitions not read | `sc-explain.md` lines 97, 101 |

Read in full with no stated gap: `/sc:adversarial` (command, 2998-line skill, four refs), `/sc:pr-submit` (command, skill, 11 refs, script headers, installed core), `/sc:git`, `/sc:spawn`, `/sc:analyze`, `/sc:spec-panel` (command only; no skill exists).

**Commands with no backing protocol skill** (12 of the 27; each checked by `ls` or a glob in its own file). The command file is then the only definition of every flag and default, and the guide accepts this (HW:232: such a command "runs from its own file"): `/sc:design`, `/sc:spec-panel`, `/sc:research`, `/sc:spawn`, `/sc:test`, `/sc:build`, `/sc:improve`, `/sc:cleanup`, `/sc:git`, `/sc:analyze`, `/sc:explain`, `/sc:document`. The other 15 have one: `/sc:brainstorm`, `/sc:adversarial`, `/sc:release-split`, `/sc:workflow`, `/sc:roadmap`, `/sc:reflect`, `/sc:validate-roadmap`, `/sc:swarm-wizard`, `/sc:implement`, `/sc:auggie-review`, `/sc:pr-submit`, `/sc:troubleshoot`, `/sc:post-release`, `/sc:cleanup-audit`, and `/sc:tdd` (its skill is `~/.claude/skills/tdd`, not `sc-tdd-protocol`). Three files call a skill that does not exist: `sc-research-protocol` (6.5 row 25).

**Commands in this file with no nuance file.** The retired `/sc:task` and `/sc:tasklist`; `/sc:recommend` and `/sc:help`; the task-file skills `/task-builder`, `/task`, `/prd`, `/roadmap`, `/tech-research`, `/tech-reference`, `/operational-guide`, `/readme`, `/confidence-check`; the built-ins; all BMad and OpenSpec commands. The first two groups matter most: `/task-builder` and `/task` carry the multi-story feature minimum and `/prd` and `/roadmap` carry new-product work, yet they are covered only by the two validation files and by the neighbour sections of other nuance files.

**Structure notes where the files differ from the brief.** Section 7 is a list, not a table, in `sc-analyze.md`, `sc-explain.md`, `sc-git.md`, `sc-swarm-wizard.md` and partly `sc-build.md`; `sc-reflect.md` splits sections 2 to 4 into a, b, c parts and gives separate pre and post matrices; `sc-git.md` gives two matrices (the command, and the commit step by any tool); `sc-adversarial.md` carries cost-driver and settings subsections 2.1 to 2.5 inside section 2; the bands are not the same measure across files (bug kind in `sc-troubleshoot.md`, test-target size in `sc-test.md`, difficulty of the outside question in `sc-research.md`, in-scope file count in `sc-cleanup-audit.md`, input score in `sc-roadmap.md`); `sc-validate-roadmap.md` is titled "complexity nuance" and puts its focus answer at the top of section 8. In every file the matrix cells marked (J) are the agent's judgment and the band edges are unconfirmed.

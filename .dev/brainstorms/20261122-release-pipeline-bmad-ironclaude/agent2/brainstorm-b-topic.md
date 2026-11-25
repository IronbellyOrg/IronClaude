# Brainstorm topic (b): who writes the spec at the BMAD to IronClaude hand-off

Written by ic-planner on 2026-11-22. Input for `/sc:brainstorm`. Facts below were read in files on 2026-11-22; anything marked UNVERIFIED was not.

## The question

A release pipeline has two halves. BMAD (the BMAD-METHOD planning skills installed in this repo under `.claude/skills/bmad-*`) plans upfront: product requirements, architecture, epics and user stories. IronClaude (this repo's `/sc:` commands) plans the implementation and executes it. When BMAD hands one user story to IronClaude, who writes the spec that the IronClaude tasklist (`/sc:workflow`) and the executor (`/sc:implement`) work from?

- Option 1, BMAD only: IronClaude accepts BMAD's story file as the spec and only reviews it with `/sc:spec-panel` (multi-expert spec critique).
- Option 2, both, always: IronClaude also generates its own spec with `/sc:brainstorm` (Socratic dialogue, parallel proposals, adversarial merge, grounded in the code), then merges the two specs with `/sc:adversarial --compare`, then plans from the merged spec.
- Option 3, conditional: one of the two as the default, the other only when a stated trigger fires.

Decide: which is the default, which triggers switch it, what each costs, and what must be true of the merged spec so BMAD traceability is not lost. Recommend one default.

## What BMAD hands over (read in `.claude/skills/bmad-create-story/`)

`bmad-create-story` writes `_bmad-output/implementation-artifacts/<epic>-<story>-<slug>.md` with status `ready-for-dev`. Template sections: Story (As a / I want / so that), Acceptance Criteria (numbered, BDD from the epics file), Tasks / Subtasks (checkboxes referencing ACs), Dev Notes (architecture constraints, files to touch with their current state, testing standards, references), Dev Agent Record (model, debug log, completion notes, file list). The skill reads the epics file, PRD, architecture and UX docs, the previous story's dev notes, the last 5 git commits, and does web research; it says its purpose is to prevent developer mistakes by exhaustive analysis. It also updates `sprint-status.yaml` (`backlog` to `ready-for-dev`). The next story's creation reads the previous story's Dev Agent Record for learnings.

## What IronClaude offers (read in `~/.claude/commands/sc/` and the skills)

- `/sc:brainstorm "<topic or @file>" [--depth quick|standard|deep] [--proposals N] [--blind] [--codebase] [--research light|deep|none] [--handoff none|design] [--output DIR]`: Socratic dialogue to a seed brief, enrichment (`/sc:analyze` on the code, optional `/sc:research`), 2 to 7 proposals by different models, `/sc:adversarial` debate and merge into `merged-requirements.md`. It produces requirements only. Under `--unattended` it skips the dialogue questions and skips deep research.
- `/sc:adversarial --compare a.md,b.md [--depth quick|standard|deep] [--focus ...] [--output DIR]`: 2 to 10 artifacts, diff analysis, debate, scoring, base selection, merge with provenance annotations; writes 6 artifacts.
- `/sc:spec-panel @file [--mode critique] [--focus requirements,architecture,testing,correctness]`: named experts (Wiegers, Adzic, Cockburn, Fowler, Nygard, Whittaker, Crispin and others) give CRITICAL, MAJOR, MINOR findings; review loop capped at 2 fix cycles. Reports; does not rewrite unless asked.
- `/sc:workflow <file or prompt> [--depth quick|standard|deep]`: writes a phased tasklist package with acceptance criteria per task and an advisory pre-review (`/sc:reflect --mode pre`) against the source; the package keeps a byte-exact copy of the source.
- `/sc:implement <plan path>`: per-task spec-compliance QA against each task's acceptance criteria; a story-shaped markdown file with checkboxes and an AC block is also a valid source on its own.
- The existing IronClaude issue pipeline already picks a chain by issue complexity: simple goes straight to `/sc:workflow`; medium goes `/sc:brainstorm --blind`, `/sc:design`, `/sc:workflow`, `/sc:implement`; complex adds `--depth deep --research deep --codebase`. Complexity rubric: simple up to 4 hours in one area; medium over 4 and up to 16 hours; complex over 16 hours, or more than one subsystem, or a security or data-migration change.

## Constraints and known facts

- The stories in the plan come from a roadmap to a version 2.0 of a terminal dashboard: human validation releases, bug-fix releases, automated-test releases, a Postgres database per project, porting the dashboard to Zellij and a Coder canvas button, extra TUI screens, first write and respond features (vote and answer coordinator questions from the dashboard). Mixed stories: some are small bug fixes, some are architecture (storage, protocol).
- Each model-heavy step costs real money and wall-clock time; the owner wants rapid iteration in IronClaude and wants BMAD to own the higher-level plan.
- BMAD's story already includes codebase-aware Dev Notes written by an LLM that read the architecture docs; whether those notes are accurate against today's code is not guaranteed (UNVERIFIED how often they are stale).
- IronClaude's `/sc:issue --claim` already runs an accuracy check of an issue's text against today's code and records `current` or `out_of_date`.
- Every spec must keep BMAD's acceptance criteria ids so the executor's per-task checks map back to the story. A merged spec must not drop or reword a BMAD acceptance criterion without a recorded reason.
- Stories are executed by workers that cannot ask a person mid-run; decisions that need a person go to a coordinator session.

## Deliverable asked of the brainstorm

A recommendation with: the default option, the exact triggers that switch to the other option, a cost comparison in model calls and steps (not money guesses), the rules for merging two specs so BMAD ids survive, and what to measure in a trial release to confirm or change the default.

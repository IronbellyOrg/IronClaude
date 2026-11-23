---
topic: "@/home/coder/workspaces/IronClaude/.dev/brainstorms/20261122-release-pipeline-bmad-ironclaude/agent2/brainstorm-b-topic.md (who writes the spec at the BMAD to IronClaude hand-off)"
domain: architecture
strategy: systematic
depth: quick
proposals_target: 2
handoff_target: none
created: 2026-11-22T20:05:00Z
---

# Seed Brief: who-writes-the-spec-at-the-bmad-to-ironclaude-handoff

## Problem Statement

A release pipeline has two halves. BMAD plans upfront (PRD, architecture, epics, stories) and IronClaude plans the implementation (`/sc:workflow`) and executes it (`/sc:implement`). At the hand-off of one BMAD story, someone must produce the spec that the IronClaude tasklist and executor work from. The choice is BMAD's story file reviewed by `/sc:spec-panel` (option 1), an IronClaude-generated spec via `/sc:brainstorm` merged with the story by `/sc:adversarial --compare` on every story (option 2), or one of them by default with a trigger for the other (option 3). The stories are mixed: small bug fixes and architecture work (storage, protocol), executed by workers that cannot ask a person mid-run, with the owner wanting fast iteration in IronClaude and BMAD owning the higher-level plan.

## Known Context

Dialogue (quick depth, unattended: answered from the topic file and the enrichment below, no person asked):

- Q1 What is the decision? Which of the three options is the default, which triggers flip it, the cost of each in model calls and steps, merge rules that keep BMAD ids, and what to measure in a trial release.
- Q2 What is the scope? A single hand-off per story; the pipeline around it (epics, sprint status, PR, release gate) is out of scope.
- Q3 What must never break? Every BMAD acceptance criterion survives into the spec the executor checks against, or has a recorded reason for change.
- Q4 What does done look like? A recommendation with one default, exact triggers, cost counts, merge rules and trial metrics, precise enough that a coordinator can apply it without asking a person.
- Q5 Biggest unknown? How often BMAD Dev Notes are stale against today's code (UNVERIFIED), which decides whether a code-grounded IronClaude pass is worth its cost.

Established facts are in the Enrichment Context section below (read from files on 2026-11-22).

## Constraints

- BMAD acceptance criteria are numbered in the story file and tasks reference them as `AC: #`. The executor's per-task checks must map back to these numbers.
- A merged spec must not drop or reword a BMAD acceptance criterion without a recorded reason.
- Workers cannot ask a person mid-run; any decision needing a person goes to a coordinator session.
- Each model-heavy step costs money and wall-clock time; the owner wants rapid iteration.
- `/sc:brainstorm --unattended` skips the dialogue questions and deep research, so its dialogue adds no new information for a story that is already written.
- Option 2 is not free of its own failure mode: an adversarial merge of two specs can reword or drop criteria unless the merge rules forbid it.

## Success Criteria

- One named default (option 1, 2 or 3) with the reason.
- A closed list of observable triggers, each checkable by a script or by reading the story file and the code without a person.
- A cost table in model calls and steps for each option, not money guesses.
- Merge rules (BMAD id preservation, provenance, conflict handling, who wins) stated as testable rules.
- A trial plan: what to measure across one release to confirm or change the default, with a threshold.

## Open Questions

- Is the default BMAD-only plus spec-panel, always-both plus adversarial merge, or conditional, and what are the triggers?
- Should the code-accuracy check of the story (the `current` or `out_of_date` result `/sc:issue --claim` already records) be the main trigger instead of story size?
- Should triggers use the existing issue complexity rubric (simple up to 4 hours in one area; medium over 4 and up to 16; complex over 16, more than one subsystem, security or data migration)?
- When option 2 runs, who owns a conflict between BMAD architecture constraints and what the code shows: the story (BMAD wins) or the code (IronClaude wins)?
- Does the spec-panel step run in every option, and does it run before or after the merge?

## Enrichment Context

Full notes: `enrichment/codebase-context.md` (augment scan plus direct reads; research skipped by `--no-research`).

- A BMAD story is already an LLM-researched, code-aware artifact (the create-story skill reads PRD, architecture, epics, last commits, previous story notes and says its purpose is to prevent developer mistakes). Its acceptance criteria are a numbered list and its tasks cite them as `AC: #`.
- The executor (`/sc:implement`) needs an `AC:` block per item and writes its own `T<i>.AC<k>` ids at qualify time, so BMAD AC numbers need an explicit map to those ids.
- The installed issue chains already encode a conditional rule: simple feature = `/sc:workflow` straight from the issue text (no brainstorm); medium = brainstorm `--blind`, design, workflow, implement; complex = brainstorm `--depth deep --research deep --codebase`, design, workflow, implement.
- `/sc:brainstorm --unattended` has no dialogue questions and no deep research, so for a finished story it contributes the code-grounded proposals plus the adversarial merge only; quick depth is about 80K tokens per proposal in the protocol's own estimate.
- Option 2 adds a second spec merge on top of the brainstorm merge: two adversarial runs per story (one inside brainstorm, one for the compare against the BMAD story).

# Scenarios for the scheduled pipeline check (decision 2)

Purpose: show how the "expected steps" list changes with the size of the work, so the scheduled job does not flag a legitimate short path as a skipped step. Source: Ryan's five pipelines (spec, tasklist plus review/revise/validate, implement, commit and sc:pr-submit, sc:troubleshoot). Not every command runs every time.

Status: coach-drafted at Ryan's direct request. Not yet reviewed by Ryan. Command ratings come from the separate file `command-value-by-phase.md` (pending).

## Part A: solo developer working with agents

### S1. One-off task (typo, config tweak, small script)
- Phases that run: implement, commit, push.
- Allowed to skip: spec, tasklist, review/validate, sc:troubleshoot.
- Steps the job should expect: a test or validation run if code changed; at least one commit; push through sc:pr-submit.
- Outcome check: pull request merged, build green.

### S2. Bug fix, cause already known
- Phases that run: sc:troubleshoot (short), implement, tests, commit, sc:pr-submit.
- Allowed to skip: spec, tasklist.
- Steps the job should expect: a failing test or reproduction before the fix; tests run after; pull request.
- Outcome check: merged, build green, not reverted within a week.

### S3. Bug fix, cause unknown (incident, flaky failure)
- Phases that run: full sc:troubleshoot, implement, a review pass (sc:reflect), commit, sc:pr-submit.
- Allowed to skip: spec, tasklist.
- Steps the job should expect: troubleshoot before any edit; the fix cites the root cause; independent review before the pull request.
- Outcome check: merged, no repeat of the same failure within a week, number of fix-up rounds.

### S4. Single story (one acceptance-criteria file, one to three tasks)
- Phases that run: story on disk (BMad story skills), short tasklist, implement with tests, commit regularly, sc:pr-submit.
- Allowed to skip: brainstorm, design, spec-panel, separate validate round.
- Steps the job should expect: the story file read before the first edit; tests run; commits more than once if the work is long.
- Outcome check: merged, build green, acceptance criteria met (reviewer agent compares the merged change with the story).

### S5. Multi-story feature
- Phases that run: brainstorm or design, spec (spec-panel or BMad equivalent), tasklist (sc:workflow or task-builder), review/revise, validate, implement per task, sc:reflect, sc:pr-submit.
- Allowed to skip: nothing in the chain, but depth varies.
- Steps the job should expect: spec before tasklist; tasklist validated before implementation starts; reflect before the final pull request.
- Outcome check: every story merged, build green, acceptance met, fix-up rounds.

### S6. Release and new product (largest end of the ladder)
- Phases that run: research, brainstorm, product requirements, architecture, epics and stories, roadmap, then S5 per feature; release split, post-release check.
- Allowed to skip: none; this is where the lessons store and the story-keyed evidence matter most.
- Steps the job should expect: each feature follows S5; release-level validation and post-release verification are present.
- Outcome check: release gates pass, post-release verification recorded, cost per story tied to its pull request.

## Part B: two engineers pair programming, each with an agent team

Same ladder as Part A. What changes is the handoff between two people and two agent teams. The extra things the job must watch are named under each scenario.

### P1. Two one-off tasks in parallel
- Each engineer works one task in the same repository.
- Extra check: separate git worktrees (the plan's worktree rule); no two sessions edit the same file.
- Otherwise the same expectations as S1.

### P2. Bug fix split across two people
- One engineer investigates (sc:troubleshoot), the other verifies the fix and reviews it.
- Extra check: the root-cause finding is written down where the second engineer's session can read it; the reviewer is a different session from the author.
- Outcome check as S2 or S3.

### P3. Single story, one writes and one builds
- One engineer writes the story file, the other implements it.
- Extra check: the story file is the handoff and must exist before the builder's first edit; the builder's session reads it.
- Outcome check as S4, plus whether the builder needed to ask the writer to change the story.

### P4. Multi-story feature split by module
- Shared spec and shared tasklist, then each engineer takes a set of tasks.
- Extra check: the tasklist was validated once, before the split; each engineer's agents reviewed the other's pull request (sc:reflect or code review); merge order recorded.
- Outcome check as S5, plus same-file collisions (the plan's target is zero).

### P5. Release with two owners
- One owns the release split and validation, the other owns post-release verification and the final pull request.
- Extra check: both gates ran, by different sessions; neither engineer closes their own gate.
- Outcome check as S6.

### P6. New product, two engineers brainstorming together
- Joint brainstorm and spec, then one owns architecture and the other owns epics and stories, then parallel build as in P4.
- Extra check: lessons from one engineer's session are used by the other's without a person copying them (the plan's day-14 target); every shared lesson passes the gate in decision 3.
- Outcome check as S6.

## What the scenarios imply for the scheduled job

- One fixed list of expected steps would flag S1 and S2 as "skipped spec and tasklist" when skipping is correct. The job needs a size label per piece of work before it can judge.
- The size label has to come from somewhere the job can read: the story file, the branch, or the first prompt. Which source is open (to discuss with Ryan).
- Only pairs need handoff checks: story file exists before the builder starts, author and reviewer are different sessions, no shared files across worktrees.
- Outcome checks are the same across sizes (merged, green, not reverted, fix-up rounds). Acceptance by a reviewer agent only makes sense from S4 up, where a story with acceptance criteria exists.
- All of this depends on the follow-up note from decision 1: the branch must be readable from the LiteLLM logs, or the job cannot join a session to its pull request.

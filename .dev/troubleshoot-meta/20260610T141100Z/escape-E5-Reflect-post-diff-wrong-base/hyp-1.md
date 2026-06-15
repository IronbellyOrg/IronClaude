# Why-it-escaped hypothesis card: E5-Reflect-post-diff-wrong-base

## Lens

Runtime-entrypoint lens: actual `/task` execution semantics and the generated POST-reflect runtime handoff.

## Hypothesis

The defect escaped because review verified that a POST-reflect item existed and that it invoked `/sc:reflect`, but did not validate the item from the `/task` runtime entrypoint where task work is normally left in the working tree rather than committed. Review treated `start_commit..HEAD` as a plausible audit basis because it looks like a conventional committed-range review, while the actual `/task` loop only requires checklist/frontmatter/file updates on disk and never includes a commit step in the runtime completion protocol.

That created a semantic gap: the generated item was syntactically present and off-path enough to satisfy independence concerns, but its diff argument was incompatible with the executor's real state model. A two-dot commit range audits commits reachable from `HEAD`, not unstaged/staged working-tree edits. If unrelated commits arrive after task start, the same range also points reflect at foreign work.

## Evidence chain

1. The escape table records REFLECT-E01 as a generated POST-reflect item using `/sc:reflect --mode post --diff <start_commit>..HEAD`, with two observed failure modes: uncommitted task work was omitted and unrelated committed work was included. It also states the missed verification was actual `/task` runtime semantics where work is commonly uncommitted. Source: `/config/workspace/IronClaude/.dev/troubleshoot-meta/20260610T141100Z/defect-escape-table.md` line 11.

2. The PR #153 summary states the emitted command used `<start_commit>..HEAD`, where `start_commit` is the task-start `HEAD`. It explicitly identifies the usual `/task` outcome as working-tree edits without a commit, so the commit range audited none of the task's changes; it also documents the live #151 audit where `ac80f176..HEAD` covered only a foreign sprint-recovery commit while PRD work was uncommitted. Source: `/config/workspace/IronClaude/.dev/troubleshoot-meta/20260610T141100Z/pr-broader-summary.txt` lines 65-80.

3. The timeline places this as a reflect-wiring escape found during #151 audit and says the fix changed the base to a merge-base working-tree diff. Source: `/config/workspace/IronClaude/.dev/troubleshoot-meta/20260610T141100Z/timeline.md` line 20.

4. The pipeline artifact audit says runtime-entrypoint verification failed until late and that post-reflect corrected the diff target from `ac80f176..HEAD` to the actual working-tree PRD diff, preventing another meta-level false audit. Source: `/config/workspace/IronClaude/.dev/troubleshoot-meta/20260610T141100Z/pipeline-artifact-audit.md` lines 42-45.

5. The `/task` runtime skill's core loop is file-state driven: read the task file, execute exactly one item, mark it complete on disk, and repeat. Its frontmatter protocol updates task status/start/completion dates, and its task-file modification rules allow checking items, updating frontmatter, and adding log entries. There is no corresponding required commit step in the runtime loop. Source: `/config/workspace/IronClaude/src/superclaude/skills/task/SKILL.md` lines 100-108 and 153-179.

6. The current corrected task-builder POST-reflect item now warns that `start_commit..HEAD` is wrong because `/task` usually leaves work uncommitted and because interleaved commits can add foreign work. It instructs reflect to receive a single merge-base ref so it diffs against the current working tree. This post-fix language directly identifies the runtime semantic assumption that earlier review failed to test. Source: `/config/workspace/IronClaude/src/superclaude/skills/task-builder/SKILL.md` lines 2193-2198.

7. The sc-tasklist protocol describes reflect as a fresh-session/subagent spawn over a phase commit range, which is a different surface from standalone `/task` working-tree execution. That likely reinforced a commit-range mental model during review even though the standalone `/task` entrypoint had different semantics. Source: `/config/workspace/IronClaude/src/superclaude/skills/sc-tasklist-protocol/SKILL.md` lines 1060-1067.

## Why review missed it

Review appears to have optimized for wiring presence and independence properties instead of runtime input semantics. The checks asked: does the generated task contain a POST reflect gate, is it executor-disjoint, and does it call `/sc:reflect` rather than `/sc:task`? Those are necessary but insufficient. They do not prove that the reflect command's diff operand corresponds to the actual work produced by `/task`.

The underlying blind spot was an entrypoint mismatch:

- `/sc:tasklist` and phase-level review language naturally talk in commit ranges.
- `/task` execution is a disk-mutating checklist loop with no mandatory commit boundary.
- The POST-reflect item sat at the boundary between those worlds, so a command that was review-shaped for commits was emitted into a runtime that commonly has only working-tree changes.

Because the defect lives in the relationship between generated text and later runtime state, source-level review could pass while the operational audit was vacuous. Only a dogfood self-run that actually edited the working tree without committing, then inspected the effective reflect diff, would have exposed it.

## Escaped-review signature

A future review is vulnerable to the same class when all of these are true:

- The generator emits a command containing a VCS range or base token.
- The runtime executor is allowed or expected to leave changes uncommitted.
- The validation asserts command shape or gate presence, but does not execute the entrypoint through the same dirty working-tree state the operator will use.
- There is an off-path reviewer whose input is a diff selector rather than the live file set.

## Pipeline that should have caught it

A dogfood task-builder/self-run POST-reflect e2e should:

1. Generate a task with `POST_REFLECT_GATE: ENABLED`.
2. Execute it through `/task` or a faithful `/task` harness.
3. Make a tracked-file change and leave it uncommitted.
4. Optionally add an unrelated commit after task start to simulate interleaving.
5. Run the generated POST-reflect item.
6. Assert that reflect's effective diff includes the task-touched files and excludes the unrelated commit.

This test targets the runtime-entrypoint contract, not merely the generated command text.

# Root cause: E5-Reflect-post-diff-wrong-base

## Verdict

The surviving root cause is a runtime-scope verification contract gap: generated POST-reflect was treated as valid when the review step existed and invoked `/sc:reflect`, but no blocking check proved that the diff selected by the generated command was the same work surface produced by `/task` execution.

The concrete faulty assumption was commit-centric: the generated item used `/sc:reflect --mode post --diff <start_commit>..HEAD`, where `start_commit` was the task-start `HEAD`. That two-dot commit range audits commits, not dirty working-tree edits. In the common `/task` runtime, work is completed by mutating files and task frontmatter/checklists on disk without a required commit. Therefore the reflect gate could audit none of the task work. If unrelated commits landed after task start, the same range could audit foreign work instead.

## Adversarial merge of the two cards

### Claims that survive

1. **Runtime-entrypoint mismatch is necessary and well-supported.**
   Hypothesis 1 correctly identifies the mismatch between `/task` semantics and the generated commit-range handoff. The `/task` loop is file-state driven: read the task file, execute one item, update the file, and repeat. Its allowed task-file modifications include checking items, updating frontmatter, and adding log entries; no commit boundary is required. This directly explains why `<start_commit>..HEAD` could be empty for the actual task work.

2. **Artifact-presence substitution is also necessary.**
   Hypothesis 2 correctly generalizes that the failure was not missing reflect wiring. The defect table, PR #153 summary, timeline, and stage-value reviews all point to a stronger failure: POST-reflect existed, but the evidence packet did not require the reflect artifact to prove its effective audited diff included the task-touched files and excluded unrelated commits.

3. **The live failure mode was not hypothetical.**
   The PR #153 summary documents the observed case: while auditing the PRD `--file` fix, `start_commit` (`ac80f176`) preceded an unrelated sprint-recovery commit, while the PRD work remained uncommitted. The requested range therefore covered the foreign commit, and the reflect run had to be hand-retargeted to the working-tree diff.

4. **The counterfactual catcher is the same in both cards.**
   Both cards converge on a dogfood task-builder/self-run POST-reflect e2e that edits tracked files in the working tree without committing, optionally simulates an interleaved unrelated commit, runs the generated POST-reflect item as emitted, and asserts reflect's effective diff includes the task files and excludes foreign commits.

### Claims narrowed or rejected

1. **Do not reduce the root cause to “off-path review blindness.”**
   Off-path review was part of the symptom surface, but it is not specific enough. The review was off-path in executor identity, yet could still point at the wrong work surface. The root condition is not simply independence failure; it is absence of an effective-diff proof tied to the runtime entrypoint.

2. **Do not blame `/sc:tasklist` commit-range language as a primary cause.**
   Hypothesis 1 suggests phase-level review language may have reinforced the commit-range mental model. That is plausible but weaker than the direct evidence. The documented cause is the generated POST-reflect command's invalid assumption about `/task` work state, not a proven causal chain from `/sc:tasklist` prose.

3. **Do not over-credit QA pass masking without identifying what was untested.**
   Hypothesis 2's “QA pass masking” claim is valid only when narrowed: the passes validated schema, routing, and self-run behavior, but not the invariant that the audited diff matched `/task` runtime output. Generic “multiple QA passes missed it” is descriptive, not causal, unless tied to that missing invariant.

4. **Do not treat PR #153's post-fix language as independent evidence of the original cause.**
   The corrected task-builder text is useful corroboration and regression documentation, but it is downstream of the discovered failure. The strongest pre/post evidence remains the defect table, live PR #153 summary, timeline, and pipeline artifact audit.

## Evidence chain

- `/config/workspace/IronClaude/.dev/troubleshoot-meta/20260610T141100Z/defect-escape-table.md` records `REFLECT-E01-wrong-diff`: generated POST-reflect used `/sc:reflect --mode post --diff <start_commit>..HEAD`; uncommitted task work was omitted and unrelated committed work could be included.
- `/config/workspace/IronClaude/.dev/troubleshoot-meta/20260610T141100Z/pr-broader-summary.txt` lines 65-80 document the live PR #153 failure and the two common wrong-base cases: usual uncommitted `/task` work and interleaved commits.
- `/config/workspace/IronClaude/.dev/troubleshoot-meta/20260610T141100Z/timeline.md` line 20 places the correction after the reflect-wiring escape was found while auditing #151 and states the fix changed the base to a merge-base working-tree diff.
- `/config/workspace/IronClaude/.dev/troubleshoot-meta/20260610T141100Z/pipeline-artifact-audit.md` lines 42-45 identifies the false-audit risk: post-reflect corrected `ac80f176..HEAD` to the actual working-tree PRD diff.
- `/config/workspace/IronClaude/src/superclaude/skills/task/SKILL.md` lines 95-104 and 153-179 show `/task` execution is a disk-updating loop with task-file/frontmatter updates and no required commit step.
- `/config/workspace/IronClaude/.dev/troubleshoot-meta/20260610T141100Z/stage-value-sc-reflect.md` lines 45-48 records that initial reflect wiring had already encountered an empty supplied diff and recommended a later commit-range rerun, which later materialized as the E5 failure class.

## Generalized root cause pattern

This class recurs when all of the following are true:

1. A generator emits a VCS selector, range, or base token for an independent review step.
2. The actual runtime entrypoint is allowed to leave work as staged or unstaged working-tree changes.
3. Validation checks command presence, reviewer independence, or PASS artifacts, but not the reviewed artifact's effective input set.
4. The reviewer consumes a diff selector rather than deriving and proving the live changed-file surface.
5. No negative fixture exercises a dirty working tree plus possible interleaved foreign commit.

## Final root-cause statement

E5 escaped because the POST-reflect contract stopped at “run an independent reflect step” and did not require “prove the reflect step audited the task's actual runtime changes.” That allowed a syntactically valid, executor-disjoint review command to use a commit range that was semantically wrong for `/task`: it excluded uncommitted task work and could include unrelated commits. The missing guard was an effective-diff invariant, verified under the same dirty-working-tree conditions that `/task` operators actually produce.

## Catch that should have existed

A blocking dogfood e2e should have generated a POST-reflect-enabled task, executed it through `/task` or a faithful `/task` harness, changed tracked files without committing them, optionally added or simulated a foreign commit after task start, ran the generated POST-reflect item exactly as emitted, and asserted that reflect's effective diff contained the task-touched files while excluding the foreign commit.

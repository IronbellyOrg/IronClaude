# Troubleshoot report: why `/sc:task` was recommended in next-steps.md (issue #595)

- Date: 2026-11-17T16:52:04Z
- Type: process question (not a code defect); depth: quick (Tier 1 only)
- Status: partial (Wave 1.5, Wave 1.6, independent calibration and the evidence-validator agent were not run; see Grounding Gaps)
- Tier reached: 1
- Confidence: 0.85 (self-assessed inline, not independently calibrated)

## Summary

`/sc:task` is the first step of the routing guide's `small-change` row (level 2), and I matched issue #595 to that row. I chose that row over the default feature chain because the work is one new file and one edit. The row offers `/sc:task "<change>"` or a plain edit. I then wrote only the `/sc:task` half into `next-steps.md`.

## Diagnosis

Causal chain, each link verified on disk:

1. The `/sc:issue` default row for "Feature, simple" is brainstorm, workflow, implement (`/home/coder/.claude/skills/sc-issue-protocol/refs/chains.md:11`). That chain is the starting suggestion, not the final answer.
2. `/sc:recommend` Step 0 requires matching the whole request to one routing row before anything else. Issue #595 asks for one new file with one line, so it fits the routing-table row `small-change`: "one source file plus its test; five edits or fewer; exact change known", level 2 (`/home/coder/workspaces/IronClaude/src/superclaude/core/HOW-WE-WORK.md:354`). The hard limit (more than 5 edits or more than one source file forces a written plan) is not triggered.
3. Step 1 of that row reads: `/sc:task "<change>"` or a plain edit (same line 354). The row's `/sc:task` form is where the command name came from; I did not invent it.
4. In `/home/coder/workspaces/IronClaude/.dev/issues/595/recommend.md:17` I kept both options ("or make the same edit directly with Write"). In `/home/coder/workspaces/IronClaude/.dev/issues/595/next-steps.md:9` I kept only `/sc:task`. That narrowing was my choice. Nothing in the guide requires `/sc:task` here.

Honest weakness of the choice: `/sc:task`'s own triggers are complexity above 0.6, more than 2 files, security paths, or refactoring (`/home/coder/.claude/commands/sc/task.md`, Triggers table). None applies to a one-line new file. The command also forces a classification header and a verification pass, which is heavier than the work. The plain edit the row also allows is the smaller option and arguably the better fit for the "touch nothing else" instruction.

## Proposed Fix

No code fix. If you want the smaller route, edit step 1 of `/home/coder/workspaces/IronClaude/.dev/issues/595/next-steps.md` to say: create `ob-442/T3.txt` with the single line `ob-442 T3` using a plain edit. Step 2 (read it back, `git status --short`) stays the same.

## Grounding Gaps

- Wave 1.5 (documentation grounding), Wave 1.6 (diagnosability audit), Wave 1.7 hypothesis agent, `confidence-calibrator` and `evidence-validator` were not run. The question is about my own earlier decision, and every evidence line above was read directly from disk in this session, so I answered it inline. Confidence is therefore self-assessed.
- My `/sc:recommend` Step C check of `/sc:task` was thin: I confirmed the command file exists but did not read its argument table before emitting the command. I read it now: it takes `[operation] [target] [flags]`, so a quoted free-text description is accepted, and no flag was emitted. The emitted command is valid.
- The `/sc:recommend` hot-path cache and the Auggie ranking were skipped, as the skill specifies for a matched row.

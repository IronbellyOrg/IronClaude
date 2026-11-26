# Remediation: Troubleshoot Report

Goal: Apply the fix described in /home/coder/workspaces/worktrees/IronClaude/issue-393/.dev/troubleshoot/bug-sc-implement-retry-ladder-picks-20261126031727/REPORT.md

## Summary

The retry ladder in src/superclaude/skills/sc-implement-protocol/refs/retry.md names its advisers by workspace variables that hold full model ids, but the Agent call's model parameter takes only opus, sonnet, haiku or fable, and no line turns a slot into one of those four. Four independent analyses agree on this cause, and an adversarial debate between the two candidate fixes chose one rule: the fallback ladder passes the rung's own alias, every primary-ladder adviser launches on opus, and any pick that is not a Claude id carries a family-fallback note on its header. Confidence is capped at 0.75 because no Agent call was run, so what a full id does at runtime is unobserved and the new test can pin only the instruction text. The fix is ready to be planned. This is GitHub issue 393; its acceptance is that in a workspace that sets the model-list variables the retry ladder names only advisers that can be started, and that a test pins that behaviour.

## Files

- src/superclaude/skills/sc-implement-protocol/refs/retry.md: replace the sentence at line 185 (the model tier comes from the Agent call's model parameter) with one paragraph that starts with the bold words Launch alias. It states that the Agent call's model takes only opus, sonnet, haiku or fable and never a full id or a rung variable's value; on the fallback ladder the call's model is the rung's own alias; on the primary ladder it is opus for every adviser (A, B, the critique adviser and both escalation-2 advisers); an adviser whose picked id does not start with claude- is still launched on opus and its line 1 carries family-fallback with a reason; this never STOPs. Also change the words strongest reachable model at line 181 to opus.
- Header grammar at retry.md line 181: the line-1 header of every advice file reads model: ID family: claude-or-gpt rung: T1-or-top launch: ALIAS. The fields model, family and rung describe the pick the ladder chose; launch is the Agent model value actually passed; no header asserts the family that served the call. The launch token is the one separable part of this plan (nothing parses the header today, so it can be dropped alone if a reader turns up).
- Worked table at retry.md lines 176 to 179: change the B-column cell of all four rows from the text 1× GPT T1 to the text 1× `opus` (GPT T1 not launchable, family-fallback), written with the multiplication sign and not the letter x; leave the other columns unchanged, so the last cell of each row stays 2× `opus` and the 22-row halt regex does not match the rows.
- retry.md lines 168 to 172: reword the primary-ladder wording and example that name T1Model01 as the GPT T1 model and a T2Model02 executor as Claude; the observed values contradict both (T1Model01 is claude-opus-5-5, T1Model02 is gpt-6.1-sol, T2Model02 is glm-5.3, T2bModel01 is gpt-6.1-terra). Draft the replacement wording first; the four rung names must stay in the file.
- retry.md, one added sentence after the launch rule: the id prefix decides family-fallback only for primary-ladder rung ids; the fallback ladder passes the rung's own alias and the existing family reading at lines 164 to 166 is unchanged and not part of this fix.
- plugins/superclaude/skills/sc-implement-protocol/refs/retry.md: byte-identical mirror of every change above (a test compares the two trees byte for byte).
- src/superclaude/skills/sc-implement-protocol/SKILL.md: at line 193 widen the words every family-fallback header line of an advice-3-b.md to every family-fallback header line of an advice-N-X.md, so the final summary lists the marker from every adviser.
- plugins/superclaude/skills/sc-implement-protocol/SKILL.md: byte-identical mirror of the SKILL.md change.
- tests/skills/test_task_workspace_lifecycle.py: update the four assertion rows at lines 598 to 604, which pin the four worked-table rows verbatim, to the new cell text in the same change.
- tests/skills/test_implement_launch_alias.py: new test file, described under Acceptance.

## Acceptance

- New test tests/skills/test_implement_launch_alias.py hard-codes the alias set opus, sonnet, haiku, fable and pins it to the list at docs/reference/model-aliases.md line 48, collecting the backticked alias words and dropping the words model and inherit; a comment warns not to reuse the ALIASES constant of tests/skills/test_model_alias_policy.py, which includes inherit and lacks fable.
- The test asserts that the Model ladder section of retry.md contains the Launch alias paragraph (it must fail on today's file) and that no line of the paragraph starts with the pinned spawn-path text.
- The test asserts that every B-column cell of the four worked-table rows is an alias or names a non-launchable pick together with family-fallback, and that no cell names a model id.
- The test builds hermetic environments as plain dicts and never reads the real environment: the observed values, a swapped environment (T1Model01 a gpt- id and T1Model02 a claude- id), an all-claude environment, a bracket-1m suffixed environment, a partial environment (T1Model01 empty, which forces the fallback ladder) and a fallback environment with tier ids.
- Over every environment, every executor tier and the five adviser roles (escalation 1 A and B, the critique adviser, escalation 2 first and second), the test asserts that the launch value is in the alias set and contains no opening bracket, that a non-claude- primary-ladder pick gets family-fallback and launch opus, that the fallback ladder passes the rung's own alias, and that T2Model01 is never an adviser.
- Two negative controls must each be flagged by the same checks: a resolver that returns the raw id, and a resolver that drops the family-fallback flag.
- The test pins key phrases of the Launch alias paragraph and of the reworded lines 168 to 172, so a prose rewrite that drops the rule for opus on every adviser, or that names a GPT model as a startable spawn, cannot pass silently.
- The existing tests tests/skills/test_implement_adviser_family.py, tests/skills/test_model_alias_policy.py, tests/skills/test_implement_severity_static.py, tests/skills/test_workflow_archive.py and tests/commands/test_workflow_command.py stay green.
- The change is limited to the files listed under Files
- No new lint or type errors introduced

## Constraints

- The new retry.md text must not start any line with the pinned spawn-path text GPT spawn path: (a test requires exactly one such line, at line 183), and must keep the backticked family-fallback reason phrase and the phrase never STOPs and never prompts the user (tests/skills/test_implement_adviser_family.py lines 73 to 85).
- The new text must not contain the words halt, Ruling or E-HALT-QA outside the allow-listed lines (tests/skills/test_implement_severity_static.py lines 296 to 299 and 420 to 434), must not contain the string claude-gw-tier (tests/skills/test_model_alias_policy.py lines 104 to 119), and must not put a full model id after a --model or --models flag (same file, lines 164 to 173).
- The new text must not add a fenced block with a line that begins with T and a digit and has no angle bracket (tests/skills/test_implement_severity_static.py lines 225 to 250), and must not add a table row whose first cell is a backticked lowercase key and whose last cell is the digits 2 to 5 (tests/skills/test_workflow_archive.py lines 1042 to 1076).
- retry.md must keep the four rung names T2bModel01, T2Model02, T1Model02 and T1Model01 and must not use any T-digit-underscore-Model spelling (tests/skills/test_model_alias_policy.py lines 219 to 228).
- No new flag, no new stop reason, no new halt reason, no change to the tier= ledger token (its value class is letters, digits and underscore), no extra adviser spawn (the cap of six stays), and no edit under .claude or .dev/issues.
- Run make sync-dev and make verify-sync after editing, because the plugin tree and the project dev copies must agree; stage only the src, plugins and tests files and .dev/tasks.
- Out of scope: the executor-tier tie when T2Model01 and T1Model02 hold the same id, and family inference from gateway ids such as claude-gw-tier2; both are separate defects.
- Decided for this work (iteration 3): nothing to decide; build what the issue asks for, within its own scope.

## References

- REPORT.md: /home/coder/workspaces/worktrees/IronClaude/issue-393/.dev/troubleshoot/bug-sc-implement-retry-ladder-picks-20261126031727/REPORT.md
- Audit log: /home/coder/workspaces/worktrees/IronClaude/issue-393/.dev/troubleshoot/bug-sc-implement-retry-ladder-picks-20261126031727/audit.log
- Hypothesis card (chosen): /home/coder/workspaces/worktrees/IronClaude/issue-393/.dev/troubleshoot/bug-sc-implement-retry-ladder-picks-20261126031727/tier1-hypothesis.md
- Merged fix proposal: /home/coder/workspaces/worktrees/IronClaude/issue-393/.dev/troubleshoot/bug-sc-implement-retry-ladder-picks-20261126031727/adversarial/merged-output.md
- Sanity review with three medium follow-ups: /home/coder/workspaces/worktrees/IronClaude/issue-393/.dev/troubleshoot/bug-sc-implement-retry-ladder-picks-20261126031727/self-review.md
- Issue summary: /home/coder/workspaces/worktrees/IronClaude/issue-393/.dev/issues/393/issue-summary.md

## Pipeline Hardening

pipeline_hardening_verdict: not_applicable
waiver_status: none
(Downstream stages must not re-green a blocked/advisory closure — spec §5.4 L411.)

## Revision 1

- Replaces package: TASK-WF-remediationSourc-20261126-040738 (archived under .dev/tasks/archive/TASK-WF-remediationSourc-20261126-040738/)
- Review report: /home/coder/workspaces/worktrees/IronClaude/issue-393/.dev/reflect/pre-TASK-WF-remediationSourc-20261126-040738-20261126041149/REPORT.md
- Fix map: ./artifacts/revision-log.md (diff: ./artifacts/plan.diff)

a24bee3484cfe56ddbb5f08758649b66709e5d2a
pick: advice-3-a.md; runner-up: advice-3-b.md; reason: tie, -a
## Task 5: Rename the implement retry-ladder variables to the names the workspace exports

Acceptance criteria:
T5.AC1: The retired underscore names no longer appear anywhere in src, plugins, tests or docs (grep for the pattern T[0-4]_Model0 returns nothing), and `cmp` shows the two mirrored files identical to their src counterparts.
T5.AC2: ./artifacts/t5-notes.md exists and states the activation and its effect on adviser selection.
T5.AC3: The retry names test of tests/skills/test_model_alias_policy.py passes; `uv run pytest tests/skills/test_workflow_archive.py tests/skills/test_task_workspace_lifecycle.py tests/skills/test_implement_adviser_family.py` passes; evidence saved to ./artifacts/t5-test.log.

Steps:
1. After the revert, apply the tracked edits shown in attempt-2.diff:54-77 to src/superclaude/skills/sc-implement-protocol/refs/retry.md, and attempt-2.diff:41-50 to refs/ledger.md. Then `cp` both files over plugins/superclaude/skills/sc-implement-protocol/refs/retry.md and ledger.md. Apply the test edits in attempt-2.diff:81-118. Check: `grep -rnE 'T[0-4]_Model0' src plugins tests docs` prints nothing, and `cmp` on both src/plugin pairs prints nothing.
2. Write ./artifacts/t5-notes.md with these sections:
   - "What changed" and "Behaviour change: the primary ladder now activates": same content as before. Rung table: 0 T3Model01 gpt-6.1-terra GPT; 1 T2Model02 glm-5.3 neither family; 2 T1Model02 gpt-6.1-sol GPT; 3 (top) T1Model01 claude-opus-5-5 Claude. The values come from defaults.sh:48, :37, :69 and :67.
   - One sentence after the table: T2Model01 is also gpt-6.1-sol (defaults.sh:35), so a gpt-6.1-sol executor matches both rung 1 and rung 2, and refs/retry.md "Executor tier" does not say which one wins.
   - Write the notes in your own words. Never quote the installed retry.md text, because it spells the retired names.
3. Under "Effect on adviser selection", write exactly these five rows, columns `Executor model (family) | Tier | Escalation 1 adviser A | Escalation 1 adviser B | Escalation 2`:
   - gpt-6.1-terra (GPT) | T3Model01 | gpt-6.1-sol, the GPT T1 model ("Every GPT adviser" bullet) | claude-opus-5-5, the Claude top rung (advice-3-b bullet, "Executor is GPT") | 2x claude-opus-5-5
   - glm-5.3 (neither family) | T2Model02 | claude-opus-5-5, the top rung (advice-3-b bullet, "neither family or unknown") | gpt-6.1-sol, the family that is not adviser A's | 2x claude-opus-5-5
   - gpt-6.1-sol (GPT) | T2Model02 or T1Model02, ambiguous as in step 2 | gpt-6.1-sol ("else the same T1 model"; this does not depend on which rung matched) | claude-opus-5-5 | 2x claude-opus-5-5
   - claude-opus-5-5 (Claude) | T1Model01, the top rung | claude-opus-5-5 (advice-3-a: already on the top rung) | gpt-6.1-sol (advice-3-b: "Executor is Claude", T1Model01 is not gpt- so T1Model02) | 2x claude-opus-5-5
   - claude-sonnet-* (Claude) | unknown | claude-opus-5-5, the top rung | gpt-6.1-sol | 2x claude-opus-5-5
4. Below the table, add three statements:
   - (a) For every executor, including models off the ladder, the rules pick adviser ids only from claude-opus-5-5 (T1Model01) and gpt-6.1-sol (T1Model02). No adviser resolves to glm-5.3 or gpt-6.1-terra. The critique adviser uses adviser A's model.
   - (b) The retry.md example of a Claude executor on T3Model01 getting adviser A on T2Model02 cannot happen here, because T3Model01 is the GPT model gpt-6.1-terra.
   - (c) The text above gives the model id each rule resolves to. retry.md "Resolving adviser B" says no GPT spawn path is verified (installed retry.md:181-183), so a GPT adviser B may be spawned on the strongest reachable model with a `family-fallback:` header.

   Then the fallback comparison: before the change the fallback table applied (adviser A sonnet for a haiku executor, otherwise opus; adviser B the GPT T1 model; escalation 2 2x opus), and no adviser ran on haiku. A workspace that does not export all four rung variables keeps the fallback ladder.
5. Check each row against the rules: read /home/coder/.claude/skills/sc-implement-protocol/refs/retry.md:166-179 and confirm every cell from step 3. Then confirm these return no lines: `grep -nE 'T[0-4]_Model' artifacts/t5-notes.md`, `grep -n 'adviser.*glm' artifacts/t5-notes.md`, and `grep -niE 'haiku.*(reach|adviser on)' artifacts/t5-notes.md`. Separately, confirm glm-5.3 appears only in the rung table, the step 2 sentence, the glm-5.3 executor row, and statements (a)-(b).
6. Run `uv run pytest tests/skills/test_model_alias_policy.py::test_retry_ladder_uses_the_variable_names_the_workspace_exports tests/skills/test_workflow_archive.py tests/skills/test_task_workspace_lifecycle.py tests/skills/test_implement_adviser_family.py` and save the full output to ./artifacts/t5-test.log. All tests must pass.

differs-by: The notes give no free-form statement about which models the advisers use. They list adviser A, adviser B and escalation 2 separately for each executor model in this workspace, and each cell names the retry.md rule it comes from. The only general claim is that every adviser id is claude-opus-5-5 or gpt-6.1-sol, and the notes say plainly that the T3Model01 example in retry.md cannot happen here.

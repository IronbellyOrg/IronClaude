a24bee3484cfe56ddbb5f08758649b66709e5d2a
model: claude-opus-5-5 family: claude rung: T1 family-fallback: no verified GPT spawn path (retry.md Resolving adviser B); adviser B is the GPT T1 model gpt-6.1-sol by rule and was spawned on the strongest reachable model, opus alias
outcome: ready

| AC | why earlier attempts missed it (path:line) | change |
|---|---|---|
| T5.AC1 | Not missed. Attempt 2's tracked edits removed every underscore name, and both mirrors were byte-identical to src (artifacts/retries/T5/review-2.md:3). The edits are at artifacts/retries/T5/attempt-2.diff:1-121. | Re-apply the attempt-2 tracked edits exactly. Nothing new. |
| T5.AC2 | Both failed bullets were one summary sentence, written from memory, saying which models advisers "now resolve to". Attempt 1 said advisers used to reach haiku, which is wrong (review-1.md:5). The fix for that added a glm-5.3 adviser that no rule produces here (review-2.md:4, review-2.md:6). In this workspace T3Model01 is GPT (/etc/aidev02/aienv.d/defaults.sh:48), so /home/coder/.claude/skills/sc-implement-protocol/refs/retry.md:169 applies, not the Claude-executor example at retry.md:172. The double rung match from the minor findings was never dealt with (review-2.md:7, review-1.md:6). | Replace the summary sentence with a table: one row per executor model this workspace can run, with each adviser cell worked out from a cited retry.md rule line. Then add one closing sentence that names only the models in those cells. |
| T5.AC3 | Not missed. 254 passed and ruff was clean (artifacts/retries/T5/extras-2.log:3-4, review-2.md:5). | Re-run the same command and save its output. |

differs-by: The adviser effect is written as a table with one row per executor model, and every cell cites the retry.md rule that produces it. Both earlier attempts wrote one combined summary sentence instead. A mechanical check then confirms that glm-5.3 and gpt-6.1-terra never appear in an adviser cell.

steps:
1. After the revert, use Read on src/superclaude/skills/sc-implement-protocol/refs/retry.md (lines 160-183) and refs/ledger.md (line 200). Make the edits shown in artifacts/retries/T5/attempt-2.diff:22-37, 9-10, 89-90 and 101-118:
   - Replace each `T<digit>_Model` with `T<digit>Model` in retry.md, ledger.md, tests/skills/test_workflow_archive.py (lines 774-777 and 786) and tests/skills/test_task_workspace_lifecycle.py (line 597). Build the search pattern from the regex `T([0-4])_Model`; never write a literal name.
   - Append the required sentence to the end of the Ladders paragraph (diff line 23).
   - Run `cp` from both src refs files onto plugins/superclaude/skills/sc-implement-protocol/refs/, then run `cmp` on each pair and confirm no output.
2. AC1 check: `grep -rnE 'T[0-4]_Model0' src plugins tests docs` must print nothing. Save this output and the `cmp` output to ./artifacts/t5-test.log.
3. Use Read on the edited src retry.md. Confirm the rule lines still sit at 162 (Ladders), 164 (Executor tier), 167-170 (Escalation rule), 172 (Escalation 2), 176-179 (fallback table) and 181-183 (adviser B). The attempt-2 hunk kept the line count at 17 (diff line 58). Only cite `refs/retry.md:<line>` in the notes after this Read.
4. Write ./artifacts/t5-notes.md with these sections, and nothing else that names a model:
   - **What changed.** As before. Say the refs used underscore names that /etc/aidev02/aienv.d/defaults.sh does not export. Do not say "no workspace ever".
   - **Activation.** Quote retry.md:162 ("active only when the four rung variables are all set and non-empty"). List the four values with defaults.sh line numbers: T3Model01=gpt-6.1-terra (48), T2Model02=glm-5.3 (37), T1Model02=gpt-6.1-sol (69), T1Model01=claude-opus-5-5 (67), plus optional T2Model01=gpt-6.1-sol (35). Then give the rung table: rung, variable, model, family. Family follows retry.md:166: `claude-` means Claude, `gpt-` means GPT, glm-5.3 is neither.
   - **GPT T1 model.** One line: T1Model01 is claude-opus-5-5, which does not start with `gpt-`, so the GPT T1 model of retry.md:168 is T1Model02, gpt-6.1-sol.
   - **Adviser table.** Columns: executor model | tier recorded | family | escalation 1 adviser A | escalation 1 adviser B | escalation 2 | rule lines. Exactly these rows:
     - gpt-6.1-terra | T3Model01 | GPT | gpt-6.1-sol | claude-opus-5-5 | 2x claude-opus-5-5 | 169, 168, 172. Add a note that the retry.md:172 example "on T3Model01, adviser A on T2Model02" is for a Claude executor and does not apply, because T3Model01 is GPT here.
     - glm-5.3 | T2Model02 | neither | claude-opus-5-5 (top rung) | gpt-6.1-sol | 2x claude-opus-5-5 | 168, 172.
     - gpt-6.1-sol | matches rung 1 through T2Model01 (recorded `T2Model02`, 164) and rung 2 (T1Model02) | GPT | gpt-6.1-sol ("else the same T1 model", 169) | claude-opus-5-5 | 2x claude-opus-5-5 | 164, 169, 168, 172. Add a note that retry.md:164 assumes one matching rung, so the recorded tier is ambiguous, but the advisers are the same for either rung because the GPT rule at 169 does not depend on the rung.
     - claude-opus-5-5 | T1Model01 (top) | Claude | claude-opus-5-5 (top rung, 167) | gpt-6.1-sol (168) | 2x claude-opus-5-5 | 167, 168, 172.
     - Any other model, for example claude-sonnet-5-5 (T1Model03, defaults.sh:71, not a rung) | unknown | that model's family | claude-opus-5-5 (top rung, 167) | gpt-6.1-sol (168) | 2x claude-opus-5-5 | 164, 167, 168, 172.
   - **Closing lines.**
     - In this workspace every adviser, including the critique adviser (which uses adviser A's model, retry.md:170), runs on claude-opus-5-5 or gpt-6.1-sol. No adviser runs on glm-5.3 or gpt-6.1-terra.
     - retry.md:183 records no verified spawn path for a GPT model, so adviser B on gpt-6.1-sol still goes through the family-fallback of retry.md:181 when that model cannot be reached.
     - Before this change the fallback table (retry.md:176-179) applied: adviser A was `sonnet` for a `haiku` executor and `opus` otherwise, adviser B was "GPT T1", and escalation 2 was 2x `opus`. No row puts an adviser on `haiku`.
     - A workspace that does not export all four variables keeps the fallback ladder.
5. Mechanical self-check of the notes. All three must pass before the review:
   - `grep -nE 'T[0-4]_Model' artifacts/t5-notes.md` prints nothing.
   - `grep -n 'glm-5.3\|gpt-6.1-terra' artifacts/t5-notes.md`: every hit is in the Activation list, the rung table, the executor column, the T3Model01 note, or the "No adviser runs on" sentence. None is in an adviser cell.
   - For each adviser cell, Read the cited retry.md line again and confirm the rule names that model for that executor's family.
6. Run `uv run pytest tests/skills/test_model_alias_policy.py tests/skills/test_workflow_archive.py tests/skills/test_task_workspace_lifecycle.py tests/skills/test_implement_adviser_family.py -v` and `uv run ruff check tests/skills/test_workflow_archive.py tests/skills/test_task_workspace_lifecycle.py`. Append both outputs to ./artifacts/t5-test.log. The retry names test must show PASSED, and the totals must match the earlier 254-pass baseline (extras-2.log:3) apart from the other tasks' policy tests.

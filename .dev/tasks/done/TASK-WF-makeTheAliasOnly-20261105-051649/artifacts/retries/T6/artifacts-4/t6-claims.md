# T6 claim ledger (attempt 4)

| page line | kind | source path:line | verify command | expected | counter-search | counter result | verdict |
|---|---|---|---|---|---|---|---|
| 3 | decision | issue #384 owner decision 2026-11-05 (coordinator brief) | n/a | decision recorded | grep -n 'prism' docs/reference/model-aliases.md | none | ok |
| 9 | source | tests/skills/test_model_alias_policy.py:79-97, 82-84, 89-90 | sed -n '79p;82,84p;89,90p' | def + globs + skip | grep -rn '^model:' src/superclaude | only 3 non-alias lines, all issue-worker pins at :6 | ok |
| 10 | source | tests/skills/test_model_alias_policy.py:44,48,135-157,140 | sed -n '44p;48p;135p;140p' | RESIDUAL empty, FULL_ID, def, skip | python constants scan is test-owned; no counter line | none | ok |
| 11 | source | tests/skills/test_model_alias_policy.py:49-51,70-76,160-169 | sed -n '49,51p;70p;160p' | regex + helper + def | grep -n 'MODEL_FLAG_WITH_FULL_ID' test file | single regex | ok |
| 12 | source | tests/skills/test_model_alias_policy.py:46-47,100-115,36-40 | sed -n '46,47p;100p' | dirs + suffixes + def | grep -rl claude-gw-tier over the six folders | hits only issue-worker agents, sc-issue-protocol/, ccsession-tag/ (all in TIER_TEXT_ALLOWED) | ok |
| 16 | source | src/superclaude/agents/issue-worker-t{1,2,3}.md:6 | grep -n '^model: claude-gw-tier' src/superclaude/agents/*.md | 3 hits at :6 | grep -rn 'claude-gw-tier' src/superclaude/agents | 3 pins at :6 plus prose at :11 | ok |
| 17 | source | src/superclaude/skills/sc-issue-protocol/refs/tiers.md:34,40 | sed -n '34p;40p' | E-TIER-UNAVAILABLE spawn failure; 'There is no alias fallback' | grep -n 'fallback' tiers.md | line 40 | ok |
| 18 | source | tests/skills/test_model_alias_policy.py:36-40 | sed -n '36,40p' | TIER_TEXT_ALLOWED tuple | n/a | n/a | ok |
| 22-26 | decision | mapping table and exports (owner decision; tests/skills/test_model_alias_policy.py:231-233) | grep -n 'ANTHROPIC_DEFAULT_.*_MODEL=claude-gw' docs/reference/model-aliases.md | 6 hits (3 table, 3 block) | n/a | n/a | ok |
| 38 | target | Target line | starts with 'Target, once the launcher change lands:' | yes | n/a | n/a | ok |
| 40-41 | status | /etc/aidev02/aienv.d/defaults.sh:92-94,23,25,37 | grep -nE '^export (T1aModel0[12]|T2Model02|ANTHROPIC_DEFAULT_[A-Z]+_MODEL)=' | lines 23,25,37,92,93,94 | read lines 85-100 for a condition | no condition | ok |
| 45-50 | attributed | https://code.claude.com/docs/en/sub-agents read 2026-11-05 | WebFetch (done by three reviewers) | order, accepted values, family edge case | n/a | n/a | ok |
| 49 | probe | .dev/issues/384/analysis/probe-alias-remap.md:7,13,19 | sed -n '7p;13p;19p' | OPUS and HAIKU variables set; SONNET never set | grep -n SONNET probe record | none | ok |
| 52-54 | probe | probe record lines 9,15,19-21 | sed -n '9p;15p;19,21p' | opus->tier1a, haiku->tier2, notice, Agent-call not exercised | n/a | n/a | ok |
| 58 | source | src/superclaude/cli/reflect/runner.py:291-310; src/superclaude/skills/ccsession-tag/MODEL-TIERS.md:38-39 | python -I snippet count_model_aliases with 3 tier ids | 3 | grep -n 'Sonnet 5.5' MODEL-TIERS.md | lines 38,39,69 | ok |
| 59 | source | src/superclaude/cli/sprint/aienv.py:149-152,78-82,111-128 | python -I snippet: suggest_alternate_model('opus') / ('claude-opus-5-5') with tier ids and T2 slots | sonnet / None | trace of branches at 120-126 (needs resolved==alias) | not taken for tier ids | ok |
| 60 | source | src/superclaude/skills/sc-roadmap-protocol/SKILL.md:114; src/superclaude/cli/roadmap/models.py:85,88-90; src/superclaude/cli/recommend/eval_aggregate.py:18-20 | sed -n of each | id = f'{model}-{persona}' with model text passed; eval lists use opus/sonnet/haiku | grep -n 'claude-gw' those files | none | ok |
| 61 | source | defaults.sh:48,37,69,67; src/superclaude/skills/sc-implement-protocol/refs/retry.md:162,164,168,169,172; artifacts/t5-notes.md:28-33,45-46 | grep -nE 'T[0-9]Model0[0-9]' retry.md | names at 162,164,168,169,172 | grep -nE 'T[0-4]_Model' page | none | ok |

## Negation and universal-word hits (grep -niwE ...) and dispositions
- line 7 'include': the Checks lead-in, intended non-exhaustive wording.
- line 9 'without': skip rule, test lines 89-90.
- line 16 'each': each pinned file has the pin on line 6 (counter-search above).
- line 17 'not', 'no': tiers.md lines 34 and 40.
- line 38 'none', 'keep': the Target line.
- line 40 'these': refers to the exports in the block above the status line.
- line 43 'not' (heading text), line 47 'cannot', line 48 'no': attributed to the sub-agents page.
- lines 49, 50, 54 'not' (did not set / cover / exercise): probe record lines 7, 13, 19-21.
- line 59 'no slot': sprint conditional, aienv.py lines 111-128, traced above.
- line 60 'stay': roadmap row, backed by models.py:85,88-90 and eval_aggregate.py:18-20.
- line 61 'these four variables': defaults.sh lines 48, 37, 69, 67.

## Rerun after the last edit: every command above was run on the final page text; counter results match the table.
Scope of the rerun: the negation grep, the model: and claude-gw-tier counter-searches, the sprint and reflect traces and the secret grep ran on the final text; the cited test, tiers.md, defaults.sh, retry.md and probe lines were re-read in this session; the sub-agents page claims rest on the 2026-11-05 fetches of earlier reviews.
- line 60 'stay' (repair): roadmap row, backed by models.py:75-90,102-105, commands.py:37-38,323-326 and eval_aggregate.py:18-20.

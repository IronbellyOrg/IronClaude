## (a) sweeping-word hits
16:- `ISSUE_WORKER_PINS`: `issue-worker-t3` pins `claude-gw-tier3`, `issue-worker-t2` pins `claude-gw-tier2` and `issue-worker-t1` pins `claude-gw-tier1a` (line 6 of each file under `src/superclaude/agents/`).
59:Target, once the launcher change lands: outside a ccsession tier workspace the launcher sets none of the three variables, so `opus`, `sonnet` and `haiku` keep Claude Code's meaning.
67:- The sub-agents page says the Agent-call `model` parameter takes the aliases `sonnet`, `opus`, `haiku` or `fable`, and that Claude cannot pass a full model id or `inherit` on that call.
80:- **Sprint alternate-model suggestion.** Given the alias `opus`, `suggest_alternate_model` returns `sonnet` when the two slots hold different ids (`src/superclaude/cli/sprint/aienv.py` lines 149-152). Given a Claude id from a cooldown message, such as `claude-opus-5-5`, it matches by family a slot that is left unset (line 124). When the three slots hold tier ids and no slot holds that id, it returns `None` (lines 111-128).
## (b) test names on the page vs the test file
ok test_frontmatter_model_is_an_alias_when_present
ok test_issue_worker_allow_list_entries_exist
ok test_markdown_does_not_pass_full_model_ids_to_model_flags
MISSING test_model_alias_policy
ok test_python_selection_constants_are_not_full_model_ids
ok test_tier_ids_appear_only_in_allowed_paths
## (c) forbidden phrases
exit=1
## (d) retired names
exit=1
## (e) keep Claude Code's meaning
59:Target, once the launcher change lands: outside a ccsession tier workspace the launcher sets none of the three variables, so `opus`, `sonnet` and `haiku` keep Claude Code's meaning.
## (f) step 2 hit groups: roadmap/auggie/ccsession/slots covered on page
1
1
5

## Justifications for the (a) hits
- line 16, "each": scoped to the three pinned agent files; each has its `model:` on line 6 (src/superclaude/agents/issue-worker-t3.md:6, issue-worker-t2.md:6, issue-worker-t1.md:6).
- line 59, "none" and "keep": the line starts with "Target, once the launcher change lands:".
- line 67, "cannot": attributed to the sub-agents page ("The sub-agents page says ...").
- line 80, "None": the Python value `None` returned by suggest_alternate_model (src/superclaude/cli/sprint/aienv.py lines 111-128).
## (b) note
- "MISSING test_model_alias_policy" is the module name `tests/skills/test_model_alias_policy.py`, not a test function.

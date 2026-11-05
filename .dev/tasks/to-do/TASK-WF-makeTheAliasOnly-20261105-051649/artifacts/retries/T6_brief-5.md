40950c4008013a396f395a09d8206bc392d6458a
pick: refactor of advice-4-b.md; runner-up: none; reason: escalation 3
## Task 6: Write the model-alias reference page

Acceptance criteria:
T6.AC1: docs/reference/model-aliases.md exists with the sections above and the three exports spelled exactly as in the mapping table; docs/reference/README.md links to it.
T6.AC2: The mapping document test of tests/skills/test_model_alias_policy.py passes; `grep -nE "sk-|token=" docs/reference/model-aliases.md` returns nothing; evidence saved to ./artifacts/t6-test.log.

Steps:
1. Confirm the revert: docs/reference/README.md matches the task start and docs/reference/model-aliases.md does not exist. Add the README row exactly as written at attempt-4.diff:9.
2. Recreate docs/reference/model-aliases.md byte for byte from attempt-4.diff:12-72 (page line p is diff line p+11, after the line-number prefix), with one change: replace the "Roadmap names" bullet (attempt-4.diff:71) with this bullet: "**Roadmap names.** Step ids such as `generate-opus-architect` (`src/superclaude/skills/sc-roadmap-protocol/SKILL.md` line 114) and the `/sc:recommend` eval model lists (`src/superclaude/cli/recommend/eval_aggregate.py` lines 18-20) name the aliases, so this change does not rename them." Before writing, read best_model.py (`src/superclaude/cli/recommend/best_model.py` lines 77-124) and, only if it picks its winner from the eval panel's alias keys, append to the bullet "; the `best_model` values chosen from those lists (`src/superclaude/cli/recommend/best_model.py` lines 77-124) are those aliases". Otherwise leave best_model out.
3. Every other page line passed both A4 reviews unchanged (review-4.md:2-9 mark the six earlier findings and F4.1 resolved and both ACs met); do not edit them.
4. Counter-search the new bullet: run `grep -rn 'generate-' src/superclaude/cli/roadmap/executor.py | head` and `grep -rn "claude-gw" src/superclaude/cli/roadmap src/superclaude/cli/recommend` and record the results; if either shows a roadmap step id or eval list that is not an alias, narrow or delete the bullet. Do not describe where agent specs come from.
5. Update ./artifacts/t6-claims.md (rerun after the last edit), then run `uv run pytest tests/skills/test_model_alias_policy.py -v` and `grep -nE "sk-|token=" docs/reference/model-aliases.md; echo "grep exit $?"`, and save both outputs to ./artifacts/t6-test.log. The mapping document test must pass and the grep must exit 1.

lessons from A4:
- F4.2 (review-4.md:11): a sentence that listed where the roadmap agent specs come from (the --agents option and the default specs) left out the --resume restore path; the bullet must state only that the step ids and eval lists name the aliases and must not describe code paths.

differs-by: Brief 4 explained how roadmap step ids are produced (the --agents option and the default specs); brief 5 drops that explanation and claims only that the step ids and the eval model lists name the aliases, citing the example id and the lists, so the page describes no code path.

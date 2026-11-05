# Reflect deviation patterns — issue-315-ccsession-name-prompt

## pre-fixGitHubIssue31-20261105031639 (UC-1, issue #315 ccsession naming-question plan, 2026-11-05)
- Recurring pattern: a plan that routes more inputs into a script that exits on a validation failure (`validate_label ... || exit 2` under `set -e`) must say what happens when the input is invalid; reviewers who only compare plan to spec miss it, the one reviewer who read the failure paths found it. Ask for an invalid-input fallback criterion whenever a plan adds a new entry into an existing validator.
- Recurring pattern: a new subcommand placed "next to" an existing one can sit behind an argument loop that consumes option-shaped text (`--model`, `--tier=x`); check the dispatch order, not only the name.
- New pattern: "keep these existing tests as they are" in a test-update task is wrong when the behaviour change flips what those tests press or assert (Enter now auto-names); enumerate the tests by name with the new expectation.
- New pattern: a word-containment coverage matcher cannot see a Constraints section, so constraint-only requirements show as unmatched; read the plan body before counting them as gaps.
- Process note: the haiku alias resolves to a slow non-Claude model here (one reviewer took about 24 minutes); give that reviewer the narrowest lens or run it first.
- Process note: the Round 2 rebuttals moved the one blocking disagreement (X-001) from 2-vs-1 to 3-vs-0 by attaching a concrete acceptance criterion; ask advocates what criterion would make a blocking finding non-blocking.

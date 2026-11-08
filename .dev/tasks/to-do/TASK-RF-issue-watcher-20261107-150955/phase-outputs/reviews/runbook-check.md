# Runbook check (Step 9.3)

File checked: `docs/designs/issue-watcher-setup.md` (651 lines). Rules read from `.markdownlint.json` (`default: true`; MD013, MD029, MD033 and MD036 off; MD024 siblings only), `.pre-commit-config.yaml:74-88` (markdownlint v0.38.0 hook; its exclude list covers `.dev/`, `CHANGELOG.md`, `src/superclaude/core/ISSUE-*.md` and two fixture trees, so `docs/designs/` is linted), `tests/docs/test_retired_docs_absent.py:10-31` (17 retired paths) and `tests/skills/test_model_alias_policy.py:50` (`^claude-(opus|sonnet|haiku|fable)-\d`).

Markdownlint itself is not installed locally. The rules were applied by reading and by the scripted checks below (decision DF-32). The checks ran as `uv run python -I` snippets and Grep; the runbook was not modified (no row failed, so no fix was made).

| # | Rule | Method | Result | Evidence |
|---|---|---|---|---|
| 1 | No retired path from the list | Grep for the 17 retired paths by basename or stem (ORCHESTRATOR, COMMANDS, PERSONAS, MODES, FLAGS, core/MCP, examples-cookbook, basic-examples, advanced-workflows, advanced-patterns, integration-patterns, commands-list, suggested-commands, comprehensive-features, SuperClaude-Developer-Guide, commands-skills-cross-reference, contributor-knowledge-base) | PASS | 0 matches |
| 2 | No full model id | Grep `claude-(opus\|sonnet\|haiku\|fable)-[0-9]` | PASS | 0 matches |
| 3 | No `SuperClaude-Org` | Grep `SuperClaude-Org` | PASS | 0 matches |
| 4 | Every repository-scoped `gh` command line carries `--repo IronbellyOrg/IronClaude` | Grep of every `gh <subcommand>` occurrence, each read by line | PASS | Lines 136, 137, 143, 161, 163, 177, 178, 180, 573 (`gh label create`, `gh label list`, `gh issue edit`) all carry `--repo IronbellyOrg/IronClaude`. Not repository-scoped, so correctly without it: `gh auth status` (14, 332, 333), `gh auth refresh -s read:project` (20, 333), `gh api user` and `gh api users/<login>` (125, no `repos/` path), `gh project view <number> --owner IronbellyOrg` (106, scoped by `--owner`). Lines 140 and 146 name `gh label create` in prose only (not a command line) |
| 5 | `gh auth status` and `gh auth refresh` carry no `--repo` | Same grep | PASS | Lines 14, 20, 332, 333: no `--repo` |
| 6 | No trailing spaces (MD009) | `grep -nP '[ \t]+$'` and a script | PASS | 0 lines |
| 7 | No hard tabs (MD010) | `grep -c` for a tab and a script | PASS | 0 lines |
| 8 | No skipped heading level (MD001) | Script over all headings outside fences | PASS | 43 headings, 0 skips |
| 9 | Single top-level heading (MD025) and first line is a top-level heading (MD041) | Script | PASS | Line 1 is `# Issue watcher: owner setup and runbook`; 1 h1 in the file |
| 10 | Heading style and form (MD003, MD018, MD019, MD023, MD026) | Script | PASS | All ATX, one space after `#`, none indented, no trailing punctuation |
| 11 | No duplicate sibling headings (MD024, siblings only) | Script | PASS | 0 duplicates |
| 12 | Every fenced block has a language (MD040) | Script over all fences | PASS | 31 fences, all closed, 0 without a language |
| 13 | Blank line around every fenced block (MD031) | Script | PASS | 0 violations |
| 14 | Blank line around every heading (MD022) | Script | PASS | 0 violations |
| 15 | Blank line around every list (MD032) | Script over list items outside fences | PASS | 0 violations |
| 16 | No two consecutive blank lines (MD012) | Script | PASS | 0 occurrences |
| 17 | File ends with exactly one newline (MD047) | `od -c` of the last bytes and a script | PASS | Ends `...unworkable.\n`; no `\n\n`; no CR bytes |
| 18 | Consistent list marker and code-block style (MD004, MD046), no `$` prompts (MD014) | Script | PASS | Only `-` bullets; no indented code blocks; no `$ ` lines in fences |
| 19 | No bare URLs (MD034), no spaces in code spans or emphasis (MD037, MD038) | Script with paired-delimiter matching | PASS | 0 bare URLs, 0 padded code spans, 0 padded emphasis, no unpaired backtick |
| 20 | Tables: same column count in every row, blank line around | Script | PASS | 0 issues |
| 21 | Link targets resolve (covered by `test_retired_docs_absent.py`) | `grep -o '](...'` then `ls` | PASS | The only link is `issue-watcher.md`, which exists in `docs/designs/` |
| 22 | Reason table matches `REASON_TABLE` (extra check, not a Step 9.3 rule) | Import `audit.REASON_TABLE` and compare with section 10.2 | PASS | 59 names in the table and 59 in the runbook, identical sets. The Step 9.2 text says 57; the code and the runbook say 59 |

Result: 22 rows, all PASS, 0 fixes. Unchecked: markdownlint v0.38.0 itself was not run (not installed); MD051 (link fragments), MD042 and similar rules with no matching construct in the file were not exercised separately.

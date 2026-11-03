---
schema: workflow-plan/1.2
source: ./source.md
strategy: systematic
depth: standard
slug: TASK-WF-workflowSource-20261102-233731
version: "1"
priority: Medium
created_date: "2026-11-02"
---

# Apply the /sc:post-release v5.0.0 consolidated plan: install, user and technical docs, human test guides

Source: ./source.md
Goal: every in-scope gap (1-70) of `.dev/releases/current/v5.0.0/post-release/CONSOLIDATED-PLAN.md` is fixed in the named file, the seven new docs exist, and the 16 user and 2 sysop human-test guides plus their index exist under `docs/testing/v5.0.0/`, each statement traceable to the v5.0.0 code (tag v5.0.0 = d953b983).

## Constraints

- The item text for every task lives in `.dev/releases/current/v5.0.0/post-release/CONSOLIDATED-PLAN.md`: section "Writer worklist" (items A-W1 to A-W22, B-W1 to B-W22, C-W1 to C-W3, each with doc line, corrected statement and code evidence), section "Gap list" (gap numbers), and section "Test guide plan (D and E)". Read the named item before editing. Scan inventories with the detailed code evidence are in `.dev/releases/current/v5.0.0/post-release/scan/` (A1-core-user-docs.md, A2-feature-user-docs.md, B-technical-docs.md, C-install-surface.md, DE1-cli-surface.md, DE2-claude-surface.md).
- Line numbers in the plan are from d953b983. Read the target file first and match on the quoted text, not the number.
- Every new or corrected claim must agree with the code or `--help` output (`uv run superclaude <cmd> --help` from the repo root). If a planned correction turns out wrong when checked against code, do not write it: record the item, the planned text and the code evidence in `./artifacts/deviations.md` and write the code-true statement instead.
- Ground facts (verified): version 5.0.0 (`pyproject.toml:7`); new-user install `pipx install git+https://github.com/IronbellyOrg/IronClaude` then `superclaude install`; upgrade `pipx install --force git+https://github.com/IronbellyOrg/IronClaude` then `superclaude install --force` then restart Claude sessions; `superclaude install` options are only `--target`, `--force`, `--list`; there is no `python -m superclaude` / `python3 -m SuperClaude`; 45 commands, 45 agents, 38 skill folders, 11 core files; issues go to `https://github.com/IronbellyOrg/IronClaude/issues`.
- Do not edit `docs/releases/v5.0.0.md` or `CHANGELOG.md` (published record). Do not change code (`src/superclaude/cli/**`, hooks, scripts): code findings O1-O22 are out of scope. Deferred gaps 71-84 are out of scope.
- `src/superclaude/core/HOW-WE-WORK.md` and `src/superclaude/rules/core/changelog_maintenance.md` are installed primitives: after editing them run `make sync-dev` then `make verify-sync`; never stage `.claude/` (only `.claude/settings.json` is tracked); never add `src/superclaude/...` paths inside installed primitives.
- Every `gh` command written into a doc uses `--repo IronbellyOrg/IronClaude`. No link or instruction points users at SuperClaude-Org/SuperClaude_Framework as the place to install or file issues.
- Test guides are documents a human runs by hand, built from the templates `~/.claude/skills/sc-post-release-protocol/templates/user-test-guide.md` (D) and `~/.claude/skills/sc-post-release-protocol/templates/sysop-test-guide.md` (E): Read the template first, keep its structure (Preconditions, What you're verifying, Steps with Do / Expected result / Pass-Fail, Edge cases or Negative check, Cleanup, Overall result), remove its HTML comment. Every expected result cites code file:line, `--help` output or a line range of `docs/testing/v5.0.0/c-e2e-transcript.txt`; a result that cannot be derived is written as UNVERIFIED with the reason. Every step carries one cost tag: `[FREE]`, `[LOCAL-WRITE]`, `[CLAUDE-SESSION]`, `[API-LONG]`, `[PROXY]` or `[EXTERNAL]`. Any step that writes files does so in a throwaway `HOME` or `/tmp` path, never the tester's real `~/.claude`.
- Markdown check for every created or edited `.md` file: `npx --yes markdownlint-cli@0.38.0 -c .markdownlint.json <file>` exits 0 (pre-existing violations on untouched lines of an updated file may be recorded in `./artifacts/deviations.md` instead of fixed).
- Do not run installs against the real `~/.claude`, the real pipx environment or running ccsession shims. Commit nothing; the post-release orchestrator commits and opens the PR.

## Phase 1: Install and upgrade docs agree with the e2e-proven path (Workstream C)

## Task 1: Correct docs/getting-started/installation.md (item C-W1)

Apply every correction of item C-W1 (gaps 1-4 and 6-14) to `docs/getting-started/installation.md`: the upgrade blocks use `superclaude install --force` instead of `superclaude update`; `install --force` is described as refreshing files plus installing and registering codegraph and retiring old MCP registrations, and as able to exit 1 after files were overwritten; required prerequisites (Python 3.10+, git, pipx or pip, the `claude` CLI on PATH, network); codegraph platform limits (Linux/macOS, x64/arm64); PEP 668-safe pipx install advice; verification with `superclaude doctor --verbose` and `superclaude install --list`; the full what's-installed list; uninstall additions for codegraph and `ccsession-orca`; a codegraph note with a link to `docs/user-guide/mcp-installation.md`; the `CLAUDE_CONFIG_DIR` note; the default-plugin step. Evidence: item C-W1 and `docs/testing/v5.0.0/c-e2e-transcript.txt`.

Acceptance criteria:
- `grep -n "superclaude update" docs/getting-started/installation.md` shows no line that presents `update` as the way to upgrade.
- The file contains `superclaude install --force`, names `codegraph`, lists git and the `claude` CLI as required, and its verification step uses `superclaude doctor --verbose`.
- markdownlint check passes for the file.

## Task 2: Correct docs/user-guide/mcp-installation.md (item C-W2)

Apply item C-W2 (gaps 5 and 18) to `docs/user-guide/mcp-installation.md`: reword the line saying `superclaude install --force` "reinstalls framework files only" so it states `--force` changes only the framework-file steps while the codegraph phase and the retire step run on every `superclaude install`; add the opt-in `litellm` row to the server table with its real source (`src/superclaude/cli/install_mcp.py` litellm entry, cited in the item).

Acceptance criteria:
- The phrase "reinstalls framework files only" no longer appears in `docs/user-guide/mcp-installation.md`.
- The server table has a `litellm` row marked opt-in.
- markdownlint check passes for the file.

## Task 3: Create docs/getting-started/upgrading.md (item C-W3)

Depends on: Task 1

Create `docs/getting-started/upgrading.md` per item C-W3 (gaps 15-17): back up edited `~/.claude` files; `pipx install --force git+https://github.com/IronbellyOrg/IronClaude` then `superclaude install --force`; restart Claude sessions; check with `superclaude --version`, `superclaude install --list` (codegraph block, `Ready for Serena retirement: yes`) and `superclaude doctor --verbose`; what the retire step removes and keeps (`serena-local` kept); the codebase-memory-mcp companions an upgrade from 4.3.5 leaves (skill `codebase-memory` and 3 agents, transcript lines 729-736 and 771-773) and how to remove them; `./update.sh` installs the checked-out tree (check out `v5.0.0` first) and needs `pipx` and `make`; moving `.serena/memories/` to `.superclaude/memory/`. Link it from `docs/getting-started/installation.md` and `README.md`.

Acceptance criteria:
- `docs/getting-started/upgrading.md` exists and every command in it appears in, or is consistent with, `docs/testing/v5.0.0/c-e2e-transcript.txt` scenario 2 or the cited code.
- `docs/getting-started/installation.md` links to `upgrading.md`.
- markdownlint check passes for the file.

## Phase 2: Core user docs current for 5.0.0 (Workstream A, core pages)

## Task 4: Update README.md (item A-W1)

Depends on: Task 3

Apply item A-W1 (gaps 19-21) to `README.md`: drop the "(v4.3)" label and name the codegraph SessionStart hook with its `SUPERCLAUDE_CODEGRAPH_AUTOINIT=0` switch; fix the MCP server list (no Mindbase as installable; codegraph installed by default; litellm and Morphllm as opt-in per `install_mcp.py`); add an upgrade section linking `docs/getting-started/upgrading.md`; mention `/sc:impact` and `/sc:graph`; correct the description of bare `superclaude mcp`.

Acceptance criteria:
- `README.md` contains no "(v4.3)" label, mentions `/sc:impact`, `/sc:graph` and codegraph, and links `docs/getting-started/upgrading.md`.
- markdownlint check passes for the file.

## Task 5: Update docs/getting-started/quick-start.md (item A-W2)

Depends on: Task 3

Apply item A-W2 (gap 22) to `docs/getting-started/quick-start.md`: real prerequisites (git, the `claude` CLI, network), the restart after install, and a link to `upgrading.md`.

Acceptance criteria:
- The file names the `claude` CLI prerequisite and links `upgrading.md`.
- markdownlint check passes for the file.

## Task 6: Fix the post-upgrade step in the routing guide and its mirrors (item A-W3)

Apply item A-W3 (gap 23) to `src/superclaude/core/HOW-WE-WORK.md` and `docs/user-guide/how-we-work.md`: the line telling users to run `superclaude update` after upgrading says `superclaude install --force`. Copy `src/superclaude/core/HOW-WE-WORK.md` byte-for-byte to `plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md`. Do not change the level table. Run `make sync-dev` and `make verify-sync`.

Acceptance criteria:
- `cmp src/superclaude/core/HOW-WE-WORK.md plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md` exits 0.
- `make verify-sync` exits 0 and `uv run pytest tests/ -q -k "how_we_work or routing or level_table"` passes (save output to `./artifacts/t6-tests.log`).
- markdownlint check passes for both edited docs.

## Task 7: Update docs/user-guide/commands.md (item A-W4)

Apply item A-W4 (gaps 24-29) to `docs/user-guide/commands.md`: add `/sc:impact` and `/sc:graph` entries from their command files (`src/superclaude/commands/impact.md`, `graph.md`); correct the routing lines to `/sc:workflow` (default `--depth standard`) then `/sc:implement`, with `/task-builder` only for level-4 or `--depth deep`; `/sc:troubleshoot --fix` offers a plan; add codegraph to the MCP lines the item lists; `/sc:load` `.serena` fallback and graph pointer; `superclaude reflect run --fix` plan route; the 2-fix-cycle review note; remove undeclared flags (`--type security`, `--preview`) from examples; drop "personas" for `/sc:pm`.

Acceptance criteria:
- `docs/user-guide/commands.md` has `/sc:impact` and `/sc:graph` sections and no line recommending `--depth quick` as the always-pass default for `/sc:workflow`.
- Each correction listed in item A-W4 is present; any skipped one is recorded with evidence in `./artifacts/deviations.md`.
- markdownlint check passes for the file.

## Task 8: Update docs/user-guide/flags.md (item A-W5)

Apply item A-W5 (gap 30) to `docs/user-guide/flags.md`: codegraph row; hint flags from the removed `FLAGS.md` described as hints, not defined flags; `/sc:troubleshoot --fix` offers a plan; tables for `/sc:impact`, `/sc:graph`, `/sc:pr-submit`; system flags (`install --force` upgrade meaning, `install --list`, sprint 5.0.0 flags `--resume`, `--task-parallelism`, `--yes`); remove `--preview` and `--type security`.

Acceptance criteria:
- `flags.md` contains `/sc:impact`, `/sc:graph`, `/sc:pr-submit` and `--task-parallelism`, and no example using `--preview`.
- markdownlint check passes for the file.

## Task 9: Update docs/user-guide/modes.md (item A-W6)

Apply item A-W6 (gap 31) to `docs/user-guide/modes.md`: modes are not read from removed context files; issue URL points to IronbellyOrg/IronClaude; remove Magic MCP, `/sc:help modes`, `/sc:reflect --type mode-status` and invented flags/error codes; fix the counts and anchors the item lists.

Acceptance criteria:
- `grep -n "SuperClaude-Org\|mode-status\|/sc:help modes" docs/user-guide/modes.md` returns nothing.
- markdownlint check passes for the file.

## Task 10: Update docs/user-guide/agents.md (item A-W7)

Apply item A-W7 (gap 32) to `docs/user-guide/agents.md`: remove Magic MCP and `/sc:focus`; name the agents that use codegraph; replace keyword-trigger tables that contradict "no keyword matching" with the real selection behaviour given in the item.

Acceptance criteria:
- `grep -n "/sc:focus\|Magic" docs/user-guide/agents.md` returns nothing.
- markdownlint check passes for the file.

## Task 11: Update docs/user-guide/session-management.md (item A-W8)

Apply item A-W8 (gap 33): Serena-to-`.superclaude/memory/` migration note; routing example to `/sc:workflow`; full `/sc:load` syntax; graph pointer; drop "(v4.3+)"; correct the Morphllm memory claim.

Acceptance criteria:
- `docs/user-guide/session-management.md` mentions `.superclaude/memory/` and `.serena/memories/` migration and contains no "(v4.3+)".
- markdownlint check passes for the file.

## Task 12: Update docs/user-guide/memory-system.md (item A-W9)

Apply item A-W9 (gap 34): the issue link names `IronbellyOrg/IronClaude`.

Acceptance criteria:
- The issue link in `docs/user-guide/memory-system.md` points at `https://github.com/IronbellyOrg/IronClaude/issues`.
- markdownlint check passes for the file.

## Task 13: Update docs/user-guide/mcp-servers.md (item A-W10)

Apply item A-W10 (gap 35): add codegraph; Auggie needs Node 20+; remove the nonexistent `implement` tool claim, misplaced research-depth block, AIRIS setup errors and sample-config errors listed; `/sc:validate` removed; `--no-mcp` exists only on `/sc:troubleshoot` and `/sc:reflect`; `--all-mcp` and `--concurrency` do not exist; fix the modes links.

Acceptance criteria:
- `docs/user-guide/mcp-servers.md` has a codegraph entry, says Node 20+ for Auggie, and contains no `--all-mcp` or `/sc:validate`.
- markdownlint check passes for the file.

## Task 14: Update docs/user-guide/freshness-hooks.md (item A-W11)

Apply item A-W11 (gap 36): `superclaude install -f` becomes `superclaude install --force`; mention the codegraph SessionStart hook; correct the jq "build dependency" wording.

Acceptance criteria:
- `grep -n "install -f" docs/user-guide/freshness-hooks.md` returns nothing.
- markdownlint check passes for the file.

## Task 15: Update docs/user-guide/brainstorm.md (item A-W12)

Apply item A-W12 (gap 37): MCP list includes codegraph per `src/superclaude/commands/brainstorm.md`; fallback tier; the `--brainstorm` mode flag wording.

Acceptance criteria:
- `docs/user-guide/brainstorm.md` lists codegraph with its fallback.
- markdownlint check passes for the file.

## Task 16: Update docs/user-guide/eval-pipeline.md (item A-W13)

Apply item A-W13 (gap 38): fix dead links, the `--check-coverage` wording, and add a `/sc:cli-eval` pointer.

Acceptance criteria:
- Every relative link in `docs/user-guide/eval-pipeline.md` resolves to an existing file (check with `test -e` on each target; record in `./artifacts/t16-links.txt`).
- markdownlint check passes for the file.

## Task 17: Create docs/user-guide/codegraph.md (item A-W22)

Create `docs/user-guide/codegraph.md` per item A-W22 (gap 47): what codegraph does for the user, the SessionStart auto-index and `SUPERCLAUDE_CODEGRAPH_AUTOINIT=0`, `SUPERCLAUDE_CODEGRAPH_PRIMITIVES=off`, `/sc:graph` status and init, `/sc:impact` usage, troubleshooting, with each claim citing the code named in the item. Link it from `README.md` and `docs/user-guide/mcp-installation.md`.

Acceptance criteria:
- `docs/user-guide/codegraph.md` exists, covers the sections listed in item A-W22, and is linked from `README.md`.
- markdownlint check passes for the file.

## Phase 3: Feature guides current for 5.0.0 (Workstream A, guides)

## Task 18: Update the swarm user docs (item A-W14)

Apply item A-W14 (gap 39) to `docs/swarm/README.md`, `docs/swarm/command-reference.md`, `docs/swarm/user-guide.md`, `docs/swarm/wizard-guide.md` and `docs/swarm/lens-catalog.md`: remove the Wave 2/3 "pending M5" banners; a fresh run writes `merged.md`, `return-contract.yaml` and per-worker files (`done.json` only on `swarm kill --output`); 8 lenses plus `custom` = 9 entries, 8 validated; add `reflect-review`; add `--tui` and exit 130; custom prompts come from the JobSpec field `custom_prompt_dir`, not a `--custom-prompt-dir` flag. Confirm the lens count with `uv run superclaude swarm validate-lenses` and save its output to `./artifacts/t18-validate-lenses.txt`.

Acceptance criteria:
- `grep -rn -- "--custom-prompt-dir" docs/swarm/README.md docs/swarm/command-reference.md docs/swarm/user-guide.md docs/swarm/wizard-guide.md docs/swarm/lens-catalog.md` returns nothing.
- The five files state 9 entries / 8 validated consistently with `./artifacts/t18-validate-lenses.txt` and mention `reflect-review`.
- markdownlint check passes for each file.

## Task 19: Update docs/guides/sprint-cli-tools-release-guide.md (item A-W15)

Apply item A-W15 (gap 40): full subcommand list; `--resume <task_id>`, `--task-parallelism`, `--handoff/--no-handoff`; CI example with `--yes`; `/sc:task` instead of `/sc:task-unified`; the child argv shape and tmux forward list from the item.

Acceptance criteria:
- The guide contains `--task-parallelism` and `--yes`, and no `/sc:task-unified`.
- markdownlint check passes for the file.

## Task 20: Update docs/guides/reflect-cli-tools-guide.md (item A-W16)

Apply item A-W16 (gap 41): `--fix` uses the `/sc:workflow` plan run by `/sc:implement` unless `--depth deep`; `remediation_plan_path`; `superclaude reflect contract-status`.

Acceptance criteria:
- The guide documents the plan route, `remediation_plan_path` and `contract-status`.
- markdownlint check passes for the file.

## Task 21: Update docs/guides/cli-portify-and-pipeline-runner-guide.md (item A-W17)

Apply item A-W17 (gap 42): convergence is 1 iteration by default (2 fix cycles); `--max-convergence` currently has no effect (Known Issue); missing options; argv shape; roadmap step count.

Acceptance criteria:
- No "converge until" text promising iteration past the 1-iteration default remains; the `--max-convergence` known issue is stated.
- markdownlint check passes for the file.

## Task 22: Update docs/guides/roadmap-cli-tools-release-guide.md (item A-W18)

Apply item A-W18 (gap 43) using `uv run superclaude roadmap run --help` (save to `./artifacts/t22-roadmap-help.txt`): input arguments, the options table, the convergence default.

Acceptance criteria:
- The guide's `roadmap run` options match `./artifacts/t22-roadmap-help.txt`.
- markdownlint check passes for the file.

## Task 23: Update docs/guides/prd-skill-release-guide.md (item A-W19)

Apply item A-W19 (gap 44): max 2 fix cycles; minor findings are notes, never a fix pass; pointer to `superclaude prd`.

Acceptance criteria:
- `grep -n "3 fix cycles\|max 3" docs/guides/prd-skill-release-guide.md` returns nothing.
- markdownlint check passes for the file.

## Task 24: Update docs/guides/tdd-skill-release-guide.md (item A-W20)

Apply item A-W20 (gap 45): same review-rule corrections as Task 23.

Acceptance criteria:
- `grep -n "3 fix cycles\|max 3" docs/guides/tdd-skill-release-guide.md` returns nothing.
- markdownlint check passes for the file.

## Task 25: Update docs/guides/suites-guide.md (item A-W21)

Apply item A-W21 (gap 46): remove the `git stash apply stash@{0}` instruction (suites are on disk), fix the suite and eval counts from `uv run superclaude eval list` (save to `./artifacts/t25-eval-list.txt`).

Acceptance criteria:
- `grep -n "git stash" docs/guides/suites-guide.md` returns nothing.
- Suite counts match `./artifacts/t25-eval-list.txt`.
- markdownlint check passes for the file.

## Phase 4: Technical docs reconciled with the 5.0.0 code (Workstream B, updates)

## Task 26: Fix the changelog maintenance rule (item B-W1)

Apply item B-W1 (gap 48) to `src/superclaude/rules/core/changelog_maintenance.md`: detailed release notes go to the tracked `docs/releases/v<version>.md` (decision 7.3), not `.claude/changelogs/`; the `gh release create` example passes `--repo <owner>/<repo>` and the notes file; keep paths project-relative and generic (it runs in other projects); no `src/superclaude/` paths. Run `make sync-dev` and `make verify-sync`.

Acceptance criteria:
- `grep -n ".claude/changelogs" src/superclaude/rules/core/changelog_maintenance.md` returns nothing and the `gh release create` example contains `--repo`.
- `make verify-sync` exits 0 (output in `./artifacts/t26-verify-sync.log`).
- markdownlint check passes for the file.

## Task 27: Rewrite the stale parts of docs/reference/common-issues.md (item B-W2)

Apply item B-W2 (gap 49): `superclaude --version` (5.0.0) instead of `python3 -m SuperClaude` / 4.1.5; upgrade per `upgrading.md`; remove `pipx upgrade SuperClaude`, PyPI names, `--components`, `--install-dir`, `--list-components`; `--no-mcp` only on troubleshoot/reflect; Node 18+.

Acceptance criteria:
- `grep -n "python3 -m SuperClaude\|4.1.5\|pipx upgrade SuperClaude\|--components" docs/reference/common-issues.md` returns nothing.
- markdownlint check passes for the file.

## Task 28: Rewrite the stale parts of docs/reference/troubleshooting.md (item B-W3)

Apply item B-W3 (gap 50): same family as Task 27 plus `--diagnose`, `backup`, `uninstall`, `install --fresh`, the Magic key, the upstream issues URL and "(v4.3+)".

Acceptance criteria:
- `grep -n "python3 -m SuperClaude\|4.1.5\|--diagnose\|install --fresh\|SuperClaude-Org" docs/reference/troubleshooting.md` returns nothing.
- markdownlint check passes for the file.

## Task 29: Update docs/reference/mcp-server-guide.md (item B-W4)

Apply item B-W4 (gap 51), keeping the existing codegraph section: real server list, Node 18+, `@upstash/context7-mcp`, `@morphllm/morphmcp`, no `python3 -m SuperClaude install --components mcp`, `--no-mcp` scope, no `--all-mcp`, no placeholder hosts presented as real, IronbellyOrg links.

Acceptance criteria:
- `grep -n "@context7/mcp-server\|--all-mcp\|python3 -m SuperClaude" docs/reference/mcp-server-guide.md` returns nothing and the codegraph section is still present.
- markdownlint check passes for the file.

## Task 30: Update docs/mcp/mcp-optional-design.md (item B-W5)

Apply item B-W5 (gap 52): install registers codegraph by default; session memory is `.superclaude/memory/` files, not Mindbase.

Acceptance criteria:
- The doc states codegraph is installed by default and names `.superclaude/memory/`.
- markdownlint check passes for the file.

## Task 31: Update docs/mcp/mcp-integration-policy.md (item B-W6)

Apply item B-W6 (gap 53): add codegraph; fix the `docs/patterns`, `docs/mistakes` and `~/.claude/superclaude/...` paths and the flag claims listed.

Acceptance criteria:
- The doc names codegraph and contains no `~/.claude/superclaude/` path.
- markdownlint check passes for the file.

## Task 32: Update docs/reference/diagnostic-reference.md (item B-W7)

Apply item B-W7 (gap 54): replace `rm -rf ~/.claude` reinstall advice with `superclaude install --force`; fix the `@import` check and the `commands/sc/` path; the processes statement.

Acceptance criteria:
- `grep -n "rm -rf ~/.claude" docs/reference/diagnostic-reference.md` returns nothing.
- markdownlint check passes for the file.

## Task 33: Update docs/reference/deviation-report-format.md and docs/reference/pm-agent-autonomous-reflection.md (item B-W8)

Apply item B-W8 (gap 55): correct the nonexistent `fidelity.py` / `FidelityDeviation` citation; add the session-memory distinction.

Acceptance criteria:
- Every source path cited in `deviation-report-format.md` exists in the repo (`test -e`).
- markdownlint check passes for both files.

## Task 34: Update docs/developer-guide/technical-architecture.md (item B-W9)

Apply item B-W9 (gap 56): the tree includes `CODEGRAPH.md`, `ISSUE-HANDOFF.md`, `ISSUE-BACKLOG.md`, the codegraph hook, `/sc:impact`, `/sc:graph`, skills/templates/rules; correct agent and command lists; drop "(v4.3+)"; fix "no execution engine".

Acceptance criteria:
- The doc names `CODEGRAPH.md` and the codegraph SessionStart hook and contains no "(v4.3+)".
- markdownlint check passes for the file.

## Task 35: Update docs/developer-guide/contributing-code.md (item B-W10)

Apply item B-W10 (gap 57): Node 18+; remove the `@import` grep and "Adding New Modes"; add the `make sync-dev` / `make verify-sync` step; replace `git add .` with explicit paths.

Acceptance criteria:
- The doc contains `make verify-sync` and no `git add .`.
- markdownlint check passes for the file.

## Task 36: Update docs/developer-guide/testing-debugging.md (item B-W11)

Apply item B-W11 (gap 58): Node 18+; codegraph verification; remove `rm -rf ~/.claude`; correct the "no tests" claim.

Acceptance criteria:
- `grep -n "rm -rf ~/.claude" docs/developer-guide/testing-debugging.md` returns nothing.
- markdownlint check passes for the file.

## Task 37: Update docs/developer-guide/README.md (item B-W12)

Apply item B-W12 (gap 59): fix dead anchors, "not a CLI", Python 3.10+, Node 18+, command path, modes, the repository URL (IronbellyOrg/IronClaude), and remove the unverified marketing claims the item lists.

Acceptance criteria:
- `grep -n "SuperClaude-Org" docs/developer-guide/README.md` returns nothing and every in-file anchor resolves.
- markdownlint check passes for the file.

## Task 38: Update the targeted sections of docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md (item B-W14)

Apply item B-W14 (gap 61) to the sections it names only: remove restated content from removed core files (delegation thresholds, resource zones, circuit breaker, `--all-mcp`); add a codegraph section; `/sc:task` instead of `/sc:task-unified`; fix skill/core paths and the dead source link.

Acceptance criteria:
- `grep -n "task-unified\|--all-mcp" docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md` returns nothing and the file has a codegraph section.
- markdownlint check passes for the file.

## Task 39: Update docs/dev/sync-discipline.md and docs/dev/lens-contribution-policy.md (item B-W15)

Apply item B-W15 (gaps 62-63): `make sync-dev` (not `superclaude install`) regenerates the repo `.claude/`; 9-entry registry; `custom_prompt_dir` is a JobSpec field, not a flag.

Acceptance criteria:
- `grep -n -- "--custom-prompt-dir" docs/dev/lens-contribution-policy.md` returns nothing; `sync-dev` named in `sync-discipline.md`.
- markdownlint check passes for both files.

## Task 40: Fix two spots in docs/sprint-cli-deep-dive.md (item B-W16)

Apply item B-W16 (gap 64): `/sc:task` instead of `/sc:task-unified`; drop the "(v4.3.5)" heading label. Do not touch the line-number drift (deferred gap 72).

Acceptance criteria:
- `grep -n "task-unified\|v4.3.5" docs/sprint-cli-deep-dive.md` returns nothing.
- markdownlint check passes for the file (record pre-existing violations on untouched lines in `./artifacts/deviations.md`).

## Task 41: Update the swarm operator docs (item B-W17)

Apply item B-W17 (gap 65) to `docs/swarm/operator-runbook.md` (drop "(requires the M5 contract)"; exit 1 = terminal with partial/failed contract), `docs/swarm/monitoring-patterns.md` (reduce runs on a fresh run; `done.json` only from `swarm kill --output`; watch `.swarm-state.json` / `swarm status`) and `docs/swarm/rollback-procedure.md` (past tense: sc-bare-review shell files removed).

Acceptance criteria:
- `grep -n "M5" docs/swarm/operator-runbook.md docs/swarm/monitoring-patterns.md` shows no line claiming reduce is pending.
- markdownlint check passes for the three files.

## Task 42: Update KNOWLEDGE.md and CONTRIBUTING.md (item B-W18)

Apply item B-W18 (gap 66): replace `pipx reinstall superclaude` local-edit advice with the editable/`update.sh` path from the item; replace bare `git stash` with the safe form; add the PR-target rule (`--repo IronbellyOrg/IronClaude`).

Acceptance criteria:
- `grep -n "pipx reinstall superclaude" KNOWLEDGE.md` and a bare `git stash$` in `CONTRIBUTING.md` return nothing; `CONTRIBUTING.md` contains `--repo IronbellyOrg/IronClaude`.
- markdownlint check passes for both files.

## Phase 5: Technical notes for the 5.0.0 subsystems (Workstream B, new docs)

## Task 43: Create docs/developer-guide/codegraph-integration.md (item B-W19)

Create the design note per item B-W19 (gap 67): pinned codegraph 1.6.2 acquisition (discover, download, SHA-256, extract, receipt, links), user-scope registration, the SessionStart auto-index hook, the primitives switch, `/sc:graph` and `/sc:impact`, and the MCP retire step (Tier R/K, `serena-local` kept, receipts), each claim citing `src/superclaude/cli/install_codegraph.py`, `install_mcp.py`, `install_retired_mcp.py`, the hook script and command files with line numbers.

Acceptance criteria:
- The note exists, covers acquisition, registration, hook, primitives switch and retire step, and every cited `file:line` exists in the repo.
- markdownlint check passes for the file.

## Task 44: Create docs/developer-guide/session-memory.md (item B-W20)

Create the note per item B-W20 (gap 68): `.superclaude/memory/` layout, `.gitignore` = `*`, per-worktree stores, `/sc:save` / `/sc:load` / `/sc:pm` behaviour, the one-release `.serena/memories/` read-only fallback, citing the command files.

Acceptance criteria:
- The note exists and every cited `file:line` exists.
- markdownlint check passes for the file.

## Task 45: Create docs/developer-guide/review-severity-rule.md (item B-W21)

Create the note per item B-W21 (gap 69): blocking vs minor grading, 2 fix cycles (3 reviews) then escalate, where it applies (output style, rf-qa agents, QA/MDTM templates, prd/tdd/task/task-builder skills, prd CLI, `/sc:tasklist`, `/sc:cli-portify` 1 iteration), the `/sc:implement` exception, decisions B1-B5 from `.dev/releases/current/v5.0.0/DECISIONS.md`, and the static test that guards it.

Acceptance criteria:
- The note exists, cites decisions B1-B5 and the guarding test path, and every cited path exists.
- markdownlint check passes for the file.

## Task 46: Create docs/developer-guide/release-procedure.md (item B-W22)

Create the procedure per item B-W22 (gap 70): go/no-go checks G1-G9 from `.dev/releases/current/v5.0.0/RELEASE-READINESS.md` section 6.3, release notes in `docs/releases/v<version>.md`, CHANGELOG cut, annotated tag, `gh release create --repo IronbellyOrg/IronClaude --notes-file docs/releases/v<version>.md`, then `/sc:post-release <version>`.

Acceptance criteria:
- The procedure lists G1-G9 and every `gh` command in it has `--repo IronbellyOrg/IronClaude`.
- markdownlint check passes for the file.

## Task 47: Update docs/developer-guide/documentation-index.md (item B-W13)

Depends on: Task 46

Apply item B-W13 (gap 60): fix the `docs/eval/release-checklist.md` reference and sizes; mark `git-standards-protocols.md` as copied from another project pending rewrite (deferred gap 71); remove mode development; link the four new technical notes and `docs/user-guide/codegraph.md`, `docs/getting-started/upgrading.md`.

Acceptance criteria:
- The index links `codegraph-integration.md`, `session-memory.md`, `review-severity-rule.md`, `release-procedure.md`, and every link target exists.
- markdownlint check passes for the file.

## Phase 6: User-facing human test guides (Workstream D)

## Task 48: Create docs/testing/v5.0.0/user/D01-install-upgrade-doctor.md

Build guide D01 from the user-test-guide template per the D01 row of "Test guide plan (D and E)": `--version`, `install`, `install --list`, `install --force` upgrade, `update` (notice only, no codegraph), `update.sh`, `install-skill`, `doctor --verbose`, codegraph acquisition and the retire step. All local-write steps use the throwaway recipe of `docs/testing/v5.0.0/c-e2e-run.sh` (`env -i HOME=... PATH=...` with `codegraph`/`orca`/`orca-ide` stubs, 4.3.5 baseline `539e2414`); expected outputs cite `docs/testing/v5.0.0/c-e2e-transcript.txt` line ranges. Include the upgrade leftovers (skill `codebase-memory` and 3 agents) and the negative `install-skill pm-agent` case.

Acceptance criteria:
- The guide exists with Preconditions, Steps (Do / Expected result with citation / Pass-Fail), Edge cases, Cleanup and Overall result, and every step has a cost tag.
- No step writes to the tester's real `~/.claude`.
- markdownlint check passes for the file.

## Task 49: Create docs/testing/v5.0.0/user/D02-mcp-servers.md

Build guide D02 per its plan row: `superclaude mcp --dry-run`, `--servers serena` rejected with exit 1, `--uninstall` exit 2, `mcp </dev/null` exit 1, `--servers litellm` dry run, a project-scope install in a temp project, using scan DE1 "MCP server management" evidence.

Acceptance criteria:
- Every expected exit code cites `src/superclaude/cli/main.py` or `install_mcp.py` lines; every step has a cost tag.
- markdownlint check passes for the file.

## Task 50: Create docs/testing/v5.0.0/user/D03-codegraph-graph-impact.md

Build guide D03 per its plan row from scan DE2 sections on `/sc:graph`, `/sc:impact`, the auto-index hook and the two kill switches, in a scratch git repo.

Acceptance criteria:
- Steps cover `/sc:graph` not-initialized, `init`, second `init`, invalid argument, hook-created index, `/sc:impact` with symbol, `--diff`, `--tests`, the blocked combination and `SUPERCLAUDE_CODEGRAPH_PRIMITIVES=off`, each with a citation and cost tag.
- markdownlint check passes for the file.

## Task 51: Create docs/testing/v5.0.0/user/D04-session-memory.md

Build guide D04 per its plan row: files under `.superclaude/memory/`, `.superclaude/.gitignore`, `/sc:load` reading saved content and the `.serena/memories/` fallback, per-worktree stores, `/sc:pm` sharing the store.

Acceptance criteria:
- Expected results check files on disk, not prompt wording, and cite the command files; every step has a cost tag.
- markdownlint check passes for the file.

## Task 52: Create docs/testing/v5.0.0/user/D05-routing-core-files-issue-templates.md

Build guide D05 per its plan row: `/sc:help` level table versus `~/.claude/HOW-WE-WORK.md`, "Routing guide not found" when moved, `/sc:recommend` prompts, the absent removed surface (`/sc:README`, `/ccsession-tag`, six removed core files on a fresh HOME), `~/.claude/ISSUE-*.md` templates (filing marked `[EXTERNAL]`, throwaway repo only).

Acceptance criteria:
- Every expected result cites `src/superclaude/commands/help.md`, `recommend.md` or the core files; every step has a cost tag.
- markdownlint check passes for the file.

## Task 53: Create docs/testing/v5.0.0/user/D06-plan-implement-review-cap.md

Build guide D06 per its plan row: subagent context starts with the pragmatic marker; `/sc:troubleshoot --fix` offers a `/sc:workflow` plan and `--fix --depth deep` offers `/task-builder`; a small `/sc:workflow` then `/sc:implement` run producing the package, `progress.md` and archive; the optional escalation-after-review-3 check.

Acceptance criteria:
- Steps carry `[CLAUDE-SESSION]` or `[API-LONG]` tags and cite `HOW-WE-WORK.md`, `troubleshoot.md` and the output style lines named in the plan row.
- markdownlint check passes for the file.

## Task 54: Create docs/testing/v5.0.0/user/D07-pr-submit.md

Build guide D07 per its plan row on a sandbox branch: `--monitor 0` to `3`, `--pr <N>`, the head-mismatch refusal, `--max-rounds 6` rejected, removed `--yes` (rejection wording UNVERIFIED), the Augment "0 suggestions" known issue. Every PR step is `[EXTERNAL]` and checks the PR URL owner is IronbellyOrg.

Acceptance criteria:
- Every step has a cost tag and the guide never targets SuperClaude-Org.
- markdownlint check passes for the file.

## Task 55: Create docs/testing/v5.0.0/user/D08-ccsession.md

Build guide D08 per its plan row: session names, `/rename` sync, `--here`, `--here --all`, `--list`, `--rm`, `--ask` exit codes, `ccsession-orca`, tab title, `--tier 1a`, `--model`, `--models-status`, `--refresh-models`, shim surviving its terminal (#341). Warn that `pkill -f local-gateway-alias-proxy.py` cuts every session of the user and that the default launch skips permission prompts; note flaky tests #352.

Acceptance criteria:
- Every expected result cites ccsession code or `CHANGELOG.md` 5.0.0 lines; every step has a cost tag.
- markdownlint check passes for the file.

## Task 56: Create docs/testing/v5.0.0/user/D09-hooks-freshness-pragmatic.md

Build guide D09 per its plan row: unread-file edit blocked (`no_prior_read`), Read then Edit allowed, new-file Write allowed, external modification blocked, the `<session-context>` envelope, telemetry log, `AUGGIE_FIRST_DISABLE=1`.

Acceptance criteria:
- Expected results cite `freshness-pre-edit.sh` and the hook registrations; every step has a cost tag.
- markdownlint check passes for the file.

## Task 57: Create docs/testing/v5.0.0/user/D10-sprint.md

Build guide D10 per its plan row: `attach`/`kill` with no session exit 1; `status`/`logs` stub lines; `sprint run --dry-run --start 1` on the fixture; `verify-checkpoints` on a copy; a 1-phase `--no-tmux` run with `--resume`, `--task-parallelism 2`, `--no-handoff`; non-interactive auto-resume without `--yes` exit 2; note `CI=0` behaviour (code finding O7) as observed-as-coded.

Acceptance criteria:
- Every expected result cites `src/superclaude/cli/sprint/` lines; every step has a cost tag.
- markdownlint check passes for the file.

## Task 58: Create docs/testing/v5.0.0/user/D11-roadmap-tasklist.md

Build guide D11 per its plan row: `roadmap run --dry-run` (creates the output dir), more than 3 inputs exit 2, a quick-depth run, `roadmap validate` exit 0 by design, `tasklist validate` exit 1 on HIGH deviations.

Acceptance criteria:
- Every expected result cites roadmap/tasklist code; every step has a cost tag.
- markdownlint check passes for the file.

## Task 59: Create docs/testing/v5.0.0/user/D12-reflect.md

Build guide D12 per its plan row: `reflect contract-status`, the wrapper-active breaker, `--print-command` / `--dry-run`, stub and `openai_compat` transports, `--fix` plan route, exit codes 0/10/11/2, `--promote` default, `/sc:reflect --onboard` absent.

Acceptance criteria:
- Every expected result cites `src/superclaude/cli/reflect/` lines; every step has a cost tag.
- markdownlint check passes for the file.

## Task 60: Create docs/testing/v5.0.0/user/D13-prd-portify-cleanup-audit.md

Build guide D13 per its plan row: `prd run --dry-run`, `cli-portify run --dry-run` (help versus code, finding O5), `cleanup-audit run --dry-run`, one lightweight run each, `--max-convergence 3` no effect, Ctrl-C on cli-portify.

Acceptance criteria:
- Every expected result cites the command code; every step has a cost tag.
- markdownlint check passes for the file.

## Task 61: Create docs/testing/v5.0.0/user/D14-swarm.md

Build guide D14 per its plan row: `validate-lenses` (9 inspected, 8 validated), `scaffold | validate`, a stub-transport run writing `merged.md`, `return-contract.yaml` and per-worker files, `status`/`logs`, `--detached` with `attach`/`kill`, `--tui`, `openai_compat` `[PROXY]`, `/sc:swarm-wizard`, `--lens custom` and `--custom-prompt-dir` rejected.

Acceptance criteria:
- Every expected result cites swarm code or `--help`; every step has a cost tag.
- markdownlint check passes for the file.

## Task 62: Create docs/testing/v5.0.0/user/D15-eval-harness.md

Build guide D15 per its plan row: `eval list` (17 suites), `eval describe --suite eval_smoke`, `eval doctor --json --no-mcp`, `eval run --suite real --no-pty --no-mcp --output-dir /tmp/eval-runs/t1 --junit` (bare `/tmp/eval-runs` rejected; results not authoritative under the null executor), `/sc:cli-eval`.

Acceptance criteria:
- Every expected result cites eval code or output; every step has a cost tag.
- markdownlint check passes for the file.

## Task 63: Create docs/testing/v5.0.0/user/D16-init-lite-recommend-ic.md

Build guide D16 per its plan row: `init-lite --context-optimized --dry-run`, `--scaffold` in a temp project, `--output CLAUDE.md` refused, `recommend cache get spec-generation` exit 1 on empty cache, `ic --help`, `ic --no-yolo -- --version` with a temp `AIENV`; warn that `ic` skips permission prompts unless `--no-yolo`.

Acceptance criteria:
- Every expected result cites `init_lite.py`, `recommend/` or `ic.py`/`scripts/ic` lines; every step has a cost tag.
- markdownlint check passes for the file.

## Phase 7: Sysop guides and the test-guide index (Workstream E)

## Task 64: Create docs/testing/v5.0.0/sysop/E01-ccsession-tier-policy.md

Build guide E01 from the sysop-test-guide template per its plan row: tier-rule grammar and precedence, `CCSESSION_ACCESS` fallback, broken or duplicate owner entry stops the launch, limited users see only allowed tiers, `--models-status`, letter tiers; tested only with `AIDEV_AI_DEFAULTS_PATH=/tmp/defaults.sh` and `CODER_WORKSPACE_OWNER_NAME` / `CODER_WORKSPACE_OWNER_ROLES` in a throwaway shell, never the real `/etc/aidev02/aienv.d/defaults.sh`; record the advisory-limit bypass as expected behaviour.

Acceptance criteria:
- The Gate line cites `models.py` lines; the Negative / gate check table is filled; every step has a cost tag.
- markdownlint check passes for the file.

## Task 65: Create docs/testing/v5.0.0/sysop/E02-ccsession-model-data-publishing.md

Build guide E02 per its plan row: schema 2, 256 KiB cap, field regexes, refresh status line, `CCSESSION_MODELS_REFRESH=0`, validating a candidate file with `CCSESSION_MODELS_URL` and a temp `HOME`/`XDG_CACHE_HOME`. Read `_fetch` in the ccsession `models.py` to decide whether a `file://` URL works; if not, the guide serves the file with `python3 -m http.server` on localhost. Publishing to master is `[EXTERNAL]`.

Acceptance criteria:
- The guide states which URL form `_fetch` accepts, with the `models.py` line that proves it.
- markdownlint check passes for the file.

## Task 66: Create the test-guide index docs/testing/v5.0.0/README.md

Depends on: Task 65

Create `docs/testing/v5.0.0/README.md`: one row per guide D01-D16 and E01-E02 (link, capabilities, highest cost tag), a cost-tag legend, the throwaway-HOME safety rule, and links to `c-e2e-run.sh` and `c-e2e-transcript.txt`.

Acceptance criteria:
- All 18 guide links and the two e2e links resolve (`test -e`), recorded in `./artifacts/t66-links.txt`.
- markdownlint check passes for the file.

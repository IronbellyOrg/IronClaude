# QA Report - Conventions Lens (T297)

**Topic:** /sc:sweep Phase 1 primitives, tests, CHANGELOG and table rows against house patterns
**Date:** 2026-11-12
**Phase:** doc-qualitative (conventions lens)
**Fix cycle:** N/A (`fix_authorization: false`)

## Findings

No BLOCKING or MAJOR finding. Six MINOR findings (notes only; they never fail the gate). Every line cited below was read from the file on disk in this session.

Scope note: two owner-approved changes were treated as settled and not judged: WC-16 opening "On every coordinator wake or wait timeout" and the 5-minute cap in `src/superclaude/commands/sweep.md:20`. Guide row R2 was checked against DESIGN row R2 (`docs/designs/orchestrator-mode.md:716`) and matches word for word.

| id | severity | evidence | what is wrong | smallest fix |
|---|---|---|---|---|
| F1 | MINOR | `src/superclaude/skills/sc-sweep-protocol/SKILL.md:4` (`Bash(superclaude sweep run:*)`, `Bash(uv run --frozen --no-sync superclaude sweep run:*)`) against `src/superclaude/skills/sc-graph-protocol/SKILL.md:4` (`Bash(realpath *)`, `Bash(pgrep -f *)`), `src/superclaude/skills/sc-swarm-wizard-protocol/SKILL.md:7` (`Bash(uv run superclaude swarm *)`), `src/superclaude/skills/sc-impact-protocol/SKILL.md:4` | The new skill is the only skill using the older `Bash(cmd:*)` colon form. Every other skill with `Bash(...)` entries uses the space-star form; the only other file with the colon form is the command `src/superclaude/commands/help.md:6`. The literal is pinned by `tests/commands/test_sweep_command.py:30-33` and mandated by DESIGN 7.6 (`docs/designs/orchestrator-mode.md:661`), so a change needs the pin and DESIGN edited together. | `Bash(superclaude sweep run *)` and `Bash(uv run --frozen --no-sync superclaude sweep run *)`, and update the pin. Or keep as designed and accept the departure. |
| F2 | MINOR | `src/superclaude/commands/sweep.md:47` ("Pass the user's flags unchanged. Do NOT proceed using only this command file.") against `src/superclaude/commands/graph.md:46`, `src/superclaude/commands/impact.md:48`, `src/superclaude/commands/issue.md:103`, `tests/unit/test_cli_install.py:822` | 21 command files carry the sentence "Do NOT proceed with protocol execution using only this command file."; the new command shortens it. The two closest house patterns (graph, impact) both use the full sentence. No test pins either wording for sweep. | Make the second sentence of line 47 "Do NOT proceed with protocol execution using only this command file." |
| F3 | MINOR (Medium: real but non-blocking gap) | `docs/user-guide/commands.md:116` (unlinked row); detailed sections start at `commands.md:129`; `commands.md:28` says the detailed part gives "Syntax, options, and examples for each command" | A loop over every `src/superclaude/commands/*.md` against `^### \`/sc:<name>\`` in `commands.md` finds exactly one command with no detailed section: `sweep`. Every other command, including `/sc:graph` (`:238`) and `/sc:issue` (`:348`), has a When to use / Syntax / Options / Examples / MCP servers section. DESIGN R6 (`docs/designs/orchestrator-mode.md:720`) scoped the change to one table row, so this is a plan-scope gap, not a producer error. | Add a `### \`/sc:sweep\`` section in the graph.md pattern and link the row to it. |
| F4 | MINOR (Medium) | `docs/user-guide/flags.md:182`, `:195`, `:203`, `:221` (Impact, Graph, PR Submit, Issue flag tables) | The page holds a per-command flag table for the recent commands; `/sc:sweep` adds four flags (`--run`, `--window`, `--root`, `--output`) and has none. flags.md is not in the plan's doc list (task file line 154). | Add a `### Sweep Command Flags (\`/sc:sweep\`)` table in the Graph table's three-column style. |
| F5 | MINOR (Medium) | `CHANGELOG.md:7-15` (sweep block, `#### Added (sweep)` only) against `CHANGELOG.md:181-185` (precedent: the same output-style file is announced under `#### Changed (review severity)`) | `src/superclaude/output-styles/pragmatic.md:22-26` now carries a rule that changes the chat format for every session that loads the style (the sweep chat-summary exception, plus six qualified restatements). The CHANGELOG block names the command, skill, WC-16, `.gitignore` and tests but not the style change. DESIGN R8 (`orchestrator-mode.md:722`) listed five contents; the exception came later by revision and R8 was never amended. | Add `#### Changed (sweep)` with one bullet: the output style `pragmatic` gains the sweep chat-summary exception (final successful `/sc:sweep` reply only, coordinator assignment required). |
| F6 | MINOR | `tests/commands/test_sweep_command.py:3` ("DESIGN section 7.6 (step 1.16) plus the chat-output-exception revision") and `:73` ("style lines 22 to 26") against `tests/commands/test_graph_command.py:1` ("Drift guards for /sc:graph and sc:graph-protocol (issue #323, Phase 3).") | The house test docstring cites the issue and says what is pinned. The new one cites internal plan numbering and a style line range that moves with any edit to `pragmatic.md`. Related: `src/superclaude/output-styles/pragmatic.md:23-26` adds the first nested bullets in that file (`git show HEAD:src/superclaude/output-styles/pragmatic.md \| grep -n '^  - '` printed nothing); `tests/commands/test_sweep_command.py:514` pins the shape, so it is deliberate, but it is a new pattern in the file. | Cite `issue #339` in the docstring and drop the line numbers (the `_STYLE_RULE_START` / `_STYLE_RULE_END` anchors at `:40-41` already locate the block). |

## Checks

A FAIL below carries only the MINOR finding named in the last column; MINOR findings never fail the gate.

| id | check | result | finding |
|---|---|---|---|
| C1 | `sweep.md` frontmatter keys and order match `graph.md:1-10` (name, description, category, complexity, mcp-servers, personas, argument-hint, allowed-tools); an `awk` listing of the frontmatter keys of every command file shows no file with a different relative order of these keys | PASS | none |
| C2 | `sweep.md` heading and section order: title as `issue.md:12` (`# /sc:<name>: ...`), Triggers, Usage, Options, Activation (graph.md block form), Boundaries with `**Will:**` / `**Will Not:**` | PASS | none |
| C3 | `sweep.md` Options table: Flag / Default / Meaning columns, escaped pipe in `--window <N>h\|<N>d` as in `graph.md:33`, "There is no ..." closing line as `graph.md:39` and `issue.md:46` | PASS | none |
| C4 | `sweep.md` Activation wording matches the house sentence (`graph.md:46`, `impact.md:48`, `issue.md:103`) | FAIL | F2 |
| C5 | `SKILL.md` frontmatter (name `sc:sweep-protocol`, description, allowed-tools) and the "Extended metadata (for documentation, not parsed)" comment match `sc-graph-protocol/SKILL.md:1-11` (category, complexity, mcp-servers) | PASS | none |
| C6 | `SKILL.md` heading names: `# sc:sweep-protocol`, Inputs, Steps, Boundaries with Will / Will Not; same family as `sc-graph-protocol` (`## Inputs and flags`, `## Will Not`) and `sc-init-lite-protocol` (`## Boundaries`); opening sentence "Backs `/sc:sweep` (...)" and "No other skill calls this one." as `sc-graph-protocol/SKILL.md:15` | PASS | none |
| C7 | `SKILL.md` allowed-tools entry syntax matches the house space-star form | FAIL | F1 |
| C8 | `tests/commands/test_sweep_command.py` location, `test_sweep_*` naming, `_REPO` / `_COMMAND` / `_SKILL` constants and pure file-content style match `test_graph_command.py:9-17`; `uv run ruff check` and `ruff format --check` on the four touched test files: all passed | PASS | none |
| C9 | Test module docstring follows the house pattern (issue number, what is pinned, no line ranges) | FAIL | F6 |
| C10 | `WORKER-CONTRACT.md:23` never-as-worker list: `/sc:sweep` inserted in alphabetical position, still one line, text identical to DESIGN `orchestrator-mode.md:705`; developer guide `SuperClaude-Developer-Guide-Commands-Skills-Agents.md:991` has the same order (`git diff` read) | PASS | none |
| C11 | `### WC-16. Coordinator loop` (`WORKER-CONTRACT.md:275`) follows the section-4 heading form of `### WC-6. Every retry is a new Task` (`:71`), carries `WC-16` on the heading line, sits before `### Worked example` (`:279`); no trailing spaces (`grep ' $'` printed nothing) | PASS | none |
| C12 | `test_worker_contract.py` pins: `RULE_PHRASES["WC-16"]` entry in the same tuple shape as WC-15 and placed before `"heartbeats"`; `/sc:sweep` appended to `NEVER_AS_WORKER`; test renamed `...names_every_listed_command`; `"sweep" not in UNATTENDED_COMMANDS` beside the `load` assertion (`git diff` read) | PASS | none |
| C13 | `HOW-WE-WORK.md` other-commands row after `/sc:spawn` (alphabetical), `/sc:<name>` first cell and sentence-style second cell as neighbours; Orca-coordination bullet uses the bold-lead-sentence form of its siblings; `cmp src/superclaude/core/HOW-WE-WORK.md plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md` printed no difference; R2 text equals DESIGN row R2 | PASS | none |
| C14 | `_OTHER_COMMANDS` and `_POST_REFRESH_ADDITIONS` edits are one-token additions in the existing style (`git diff` read); combined run of the five related test files: 1189 passed | PASS | none |
| C15 | `commands.md:116` table row: right category (8. UTILITIES), four columns, `sweep.md` in File column, "Report only (...)" cell form as `:117`, placed after `/sc:issue`; text equals DESIGN R6 | PASS | none |
| C16 | `commands.md` has a detailed section for the new command | FAIL | F3 |
| C17 | `flags.md` has a flag table for the new command | FAIL | F4 |
| C18 | CHANGELOG heading form: `### <topic title>` under `## [Unreleased]` then `#### Added (<topic>)`, "Tests:" bullet, backticked identifiers, no en or em dash (`CHANGELOG.md:7-15`; precedent `:19`, `:181-190`) | PASS | none |
| C19 | CHANGELOG covers every user-visible change of the work (command, skill, WC-16, ignore rule, tests, style exception) | FAIL | F5 |
| C20 | `.gitignore:255-256` comment-then-pattern form, "Never tracked." ending as the sprint-state block `:252-254`, DESIGN section 10 text byte-equal; `git check-ignore -v .dev/sweeps/x.md` matched line 256 | PASS | none |
| C21 | `pragmatic.md` edit keeps the file's own writing rules: no em or en dash in any added line (`grep -P` over `git diff -U0` printed nothing); the literal qualifier `Except for the sweep chat-summary exception above,` is identical at all six sites and the primary rule names "four sub-bullets" while the file has four (`pragmatic.md:23-26`) | PASS | none (nested-bullet note under F6) |
| C22 | Skill `## Final reply` and style rule share the same four-part titles (Exempt reply / Sweep chat-summary exception, What establishes the assignment, What stays ordinary, Scope) and the skill names the installed style path `~/.claude/output-styles/pragmatic.md` rather than a `src/superclaude/` path | PASS | none |
| C23 | No `src/superclaude/` path and no en or em dash in `sweep.md`, `SKILL.md`, `test_sweep_command.py` (`grep -n 'src/superclaude/'` on the two primitives: none; `grep -nP` for U+2013/U+2014: none) | PASS | none |
| C24 | Tests run: `uv run pytest tests/commands/test_sweep_command.py -q` 115 passed; the five-file run 1189 passed; `ruff check src/superclaude/cli/main.py` passed | PASS | none |
| C25 | No `.claude/` path is modified or staged for sweep (`git status --short .claude` printed nothing; `.claude/` in this worktree holds no `commands/` or `skills/` copies of any primitive, so `make verify-sync` is not a sweep-specific signal and was not run) | PASS | none |

## Self-Audit

**(a) Reliance list.** No `## Inherited Structural Verdict` was supplied and none was relied on. The earlier `qa/cmd-skill/` and `qa/contract/` reports were not read; every judgement comes from the files on disk.

**(b) Independent semantic checks.**
- Colon-versus-space `allowed-tools` syntax: `grep` of `allowed-tools:` over all skills and commands, then `grep -c ':\*)'` (only `sc-sweep-protocol/SKILL.md` and `help.md` hit) gave F1.
- Missing detailed section: a shell loop of every `src/superclaude/commands/*.md` name against `commands.md` headings printed `no section: sweep` and nothing else, gave F3.
- Activation sentence: `grep -c 'Do NOT proceed with protocol execution'` over the commands (21 files) against `sweep.md:47` gave F2.
- Style-file nesting: `git show HEAD:...pragmatic.md | grep -n '^  - '` printed nothing, gave the nested-bullet note in F6.
- CHANGELOG precedent: `grep -n -i pragmatic CHANGELOG.md` (hits at `:181`, `:189`) against the sweep block gave F5.
- Guide parity: `cmp` of the two HOW-WE-WORK copies and a read of DESIGN rows R1 to R8 (`orchestrator-mode.md:715-722`) against the `git diff` of each target file.
- Tests: ran the five related test files (1189 passed), the sweep file alone (115 passed) and `ruff check` / `ruff format --check`.

**Confidence:** Verified: 25/25 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0% (every check has a tool call behind it; the `make verify-sync` step was not run because this worktree's `.claude/` holds no primitive copies, see C25).

**Tool engagement:** Read: 12 | Grep tool: 0 | Glob tool: 0 | Bash: about 22 (most are batched `grep`, `git diff`, `cmp` and loop calls that each covered several checks). The Read plus Grep plus Glob count is below the 25 checks, so by the engagement rule this review is flagged as suspect on that count alone; the evidence column of each check names the command that backs it, and a reader can re-run them.

**Not checked:** the Phase 11 to 13 validation files and the step-7.10 evidence file were skimmed for their command lines and results only; this lens did not re-judge them. Nothing was run against a live Orca, ccsession or Claude. Web research: none, so no Tavily call was needed.

Verdict: PASS
Blocking count: 0

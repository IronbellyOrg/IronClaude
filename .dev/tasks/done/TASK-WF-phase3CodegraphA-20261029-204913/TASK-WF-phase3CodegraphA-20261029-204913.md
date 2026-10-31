---
schema: workflow-plan/1.2
source: ./source.md
strategy: systematic
depth: standard
slug: TASK-WF-phase3CodegraphA-20261029-204913
version: "1"
priority: Medium
created_date: "2026-10-29"
---

# Phase 3: adopt codegraph in IronClaude primitives and add /sc:graph and /sc:impact (issue #323)

Source: ./source.md
Goal: Every primitive that used Serena gets a codegraph tier above the Phase 1 Grep/Read floor, one shared guide `~/.claude/CODEGRAPH.md` holds the usage rules, two new commands `/sc:graph` (index status and manual init) and `/sc:impact` (dependents and advisory test list) exist with tests, callers are wired, and a PR is open on `IronbellyOrg/IronClaude` with progress posted on issue #323.

## Constraints

- Source of truth: `./source.md` (snapshot of `.dev/codegraph-migration/specs/phase-3-codegraph-adoption-spec.md` after the F3 review resolution). Section numbers below (for example "source §1.2 row 31", "source §5 T4") refer to it. Where `./source.md` §3 lists overrides (a)-(e), they win over `.dev/codegraph-migration/design/P3-commands/interface-design.md` (cited `DES`); otherwise `DES` wins over the source's §3 summary.
- Start only after Phase 1 and Phase 2 are merged to `master` on `origin`. Setup before `/sc:implement` starts (not a task, because `/sc:implement` keeps its ledger `progress.md` next to this plan and must run in the same checkout it changes): create `git worktree add .dev/worktrees/codegraph-adoption -b feat/codegraph-adoption origin/master` (never `.claude/worktrees/`, never `EnterWorktree`); make sure this package folder (`TASK-WF-phase3CodegraphA-20261029-204913/` under `.dev/tasks/`) and the `.dev/codegraph-migration/` reference inputs below are present in that worktree (committed on `master`, or copied in from the planning checkout and staged by exact path in Task 1's commit); then start `/sc:implement` on this plan file inside that worktree, from the worktree root. Never commit to `master`. Every command runs from that worktree root.
- Reference inputs the tasks read (they must exist in the worktree; never reconstruct a missing one, escalate instead): `.dev/codegraph-migration/design/P3-commands/interface-design.md` (`DES`), `.dev/codegraph-migration/research/codegraph-evaluation.md` (`EVAL`), `.dev/codegraph-migration/brainstorm/P3-codegraph-opportunities/merged-requirements.md` (`BS`), `.dev/codegraph-migration/decisions/P3-access-model/adversarial/P3-access-model-merged.md`, `.dev/codegraph-migration/decisions/P2-indexing-sync/probe-results.md`, `.dev/codegraph-migration/inventory/primitive-usage.md`, and Phase 1's slots ledger `.dev/codegraph-migration/handoffs/phase3-codegraph-slots.md`.
- Never: edit `~/.claude`, `~/.claude.json` or any MCP registration; run `superclaude install`, `./update.sh`, `claude mcp add/remove`, `codegraph install`, `codegraph upgrade`, `codegraph uninstall`; change `src/superclaude/cli/install_codegraph.py` or any other Phase 2 installer module (the one exception is Task 3's `KNOWN_CORE_FILES` entry in `src/superclaude/cli/install_core.py`); push to `upstream`; open a PR with bare `gh pr create`; run the whole test suite or `tests/cli/eval/` as a directory (a full run rewrites the tracked `.dev/releases/current/cliEval/evidence/T02.15/perf.json`); add a `src/superclaude/...` path to an installed primitive except the one labelled fallback line of source §4.
- Tests: every `pytest` call names files or small directories and adds `-q -p no:cacheprovider`; use `uv run` for all Python.
- One test-path set, used by Task 1 baseline (b) and Task 13 check (8): `TESTSET="tests/core tests/troubleshoot tests/skills tests/agents tests/commands tests/cli/reflect tests/unit/test_cli_install.py tests/recommend/test_routing_refresh.py tests/sc-roadmap tests/roadmap/test_threshold_registry.py tests/cli/test_how_we_work_install.py"` (source §5 baseline (b): the seven original paths plus the four paths later tasks run; a superset, so no pre-existing failure reads as new). Failing-id pipeline (pipefail-safe, from source §5 "Rules for every task"): `{ uv run pytest <paths> -q -p no:cacheprovider -rfE --tb=no || true; } | { grep -E '^(FAILED|ERROR) ' || true; } | sed 's/ - .*//' | sort -u > <file>`. Paths a task creates after Task 1 (for example `tests/agents/test_codegraph_rosters.py`) have no baseline failures.
- Every acceptance criterion of the form "`uv run pytest <paths> …` passes" means: it passes, or its failing ids written by the pipeline above to `./artifacts/t<N>-failures.txt` give no output from `comm -13 .dev/codegraph-migration/experiments/P3-baseline-failures.txt ./artifacts/t<N>-failures.txt` (source §5 records existing failures "not fixed, as out of scope"). `./artifacts/` is this package's own folder, `$(echo .dev/tasks/*/TASK-WF-phase3CodegraphA-20261029-204913)/artifacts/` from the worktree root; never the project-root `artifacts/` folder.
- Mirror rule (source §1.2): for every changed primitive, apply the same change to its tracked twin under `plugins/superclaude/` (and root `commands/sc-*.md`, `agents/sc-*.md` copies) in the same commit; where the twin differs from `src/`, change only the matching sentence.
- Standing rules 1-9 of source §1.1 apply to every edited primitive: read before cite or edit, fail open to the Phase 1 floor, empty is not absence, agents get exact names and the run's state, no `explore` and no mutating CLI verb in a skill or agent, both tool-list branches with identical text, guard every CLI `codegraph status` with `pgrep -f 'codegraph\.js (init|index)'`, bare `codegraph` CLI binary, codegraph tier above the floor (never replace or delete the floor).
- Commit after every task: `git status --short` must show only that task's files plus `.dev/` progress, decision and experiment files; stage them by exact path, plus `git add .dev/codegraph-migration/progress .dev/codegraph-migration/decisions .dev/tasks` (group-comment bodies, the decision log with any URL rows written since the last commit, and this package with its `progress.md` and `artifacts/`); never stage `.claude/` (no `.claude/settings.json` change in this phase); conventional commit message ending with the attribution line the session gives.
- Issue #323 group comment, at the last task of each phase (marked "group comment"): write the body to `.dev/codegraph-migration/progress/P3-<group letter>.md` with the template of source §6 (overwrite on retry); confirm `gh repo view --json nameWithOwner -q .nameWithOwner` prints `IronbellyOrg/IronClaude` (else `gh repo set-default IronbellyOrg/IronClaude`); post with `gh issue comment 323 --repo IronbellyOrg/IronClaude --body-file .dev/codegraph-migration/progress/P3-<group letter>.md`; record the returned URL in the decision log. Retry a failed post once; a second failure is logged and does not block the next task.
- Decision rules: simple choices (the list in source §7 "Decide alone") the executor makes itself. A mid-level choice (two or more viable options with real trade-offs the source does not settle): write each option to `.dev/codegraph-migration/decisions/P3X-<slug>/option-<x>.md`, spawn an agent that runs `/sc:adversarial --compare <option files> --depth quick --output .dev/codegraph-migration/decisions/P3X-<slug>/adversarial`, follow its recommendation. A complex or architectural choice (changes a command's return contract, a contract field read by Python, or the guide's rules): same procedure with `/sc:adversarial --compare <option files> --output .dev/codegraph-migration/decisions/P3X-<slug>/adversarial` (default depth). Never stop to ask the user except for the human items H1-H5 of source §7.
- Decision log: `.dev/codegraph-migration/decisions/P3X-execution-log.md` (create as a header stub first); one row per decision: date, task, decision, options considered, method (self / adversarial quick / adversarial full), rationale, files touched. Each group comment repeats that group's rows in one line each.
- Escalation: send an Orca `escalation` (or, without Orca, stop and tell the user) with the blocker, the command run and its output.
- In the commands below, `|` is a plain shell pipe or regex alternation; no escaping is needed.

## Phase 1: Group 0, preconditions and prerequisite experiments

## Task 1: Run the section 0 gate and record the baselines

Confirm the setup of Constraints (worktree created, package and reference inputs present, `/sc:implement` started from the worktree root), then run every row G1-G6 of source §0 and record the results and the tool-list branch in the decision log `.dev/codegraph-migration/decisions/P3X-execution-log.md` (create it as a header stub first). G1: `codegraph --version` equals `VERSION` from `src/superclaude/cli/install_codegraph.py`. G3: `jq -e --arg t "$MT" '.mcpServers.codegraph.env.CODEGRAPH_MCP_TOOLS == $t' ~/.claude.json` with `MT` from `install_codegraph.MCP_TOOLS`; the value is `node,search,callers,callees,impact,files,status` (seven-tool branch) or `status` (status-only branch); both pass. G4 uses MCP `codegraph_status` when listed; CLI `codegraph status` only when `pgrep -f 'codegraph\.js (init|index)'` prints nothing (wait 30 s and re-check up to 20 times while an init runs). G5 is branch-aware. G6: no `mcp__serena__` left and the slots ledger exists. Failures: G1, G2 or G4 → H1 of source §7. G3 → run only the parts of Task 2 that need no correct registration (E-2, E-3, E-7 and the CLI part of E-1), then stop at H1, and log this as a departure from source §0 (which lets T1-T10 continue), because E-6 and the MCP part of E-1 would measure the wrong registration and Tasks 3 and 5 consume them. G5 → restart once in a fresh `claude` session in the worktree, then H1. G6 → H4. Then record the two baselines of source §5 "Rules for every task": (a) `grep -rIn 'src/superclaude' src/superclaude/{commands,skills,agents,core,hooks} | wc -l`; (b) the pytest run over `$TESTSET` (Constraints; the superset source §5 names), with its failing ids saved through the Constraints pipeline into `.dev/codegraph-migration/experiments/P3-baseline-failures.txt`. Also confirm every reference input listed in Constraints exists.

Acceptance criteria:
- `rg -n 'mcp__serena__' src/superclaude plugins/superclaude commands agents` prints nothing and `test -s .dev/codegraph-migration/handoffs/phase3-codegraph-slots.md` exits 0 (G6).
- `jq -e --arg t "$(uv run --no-sync python -c 'from superclaude.cli.install_codegraph import MCP_TOOLS; print(MCP_TOOLS)')" '.mcpServers.codegraph.env.CODEGRAPH_MCP_TOOLS == $t' ~/.claude.json` exits 0 (G3), and the decision log names the branch (`seven-tool` or `status-only`).
- `test "$(codegraph --version)" = "$(uv run --no-sync python -c 'from superclaude.cli.install_codegraph import VERSION; print(VERSION)')"` exits 0 (G1); G2, G4 and G5 results are written in the decision log.
- The decision log records baseline (a) as a number and baseline (b) pass/fail counts with a pass count above 0; `test -f .dev/codegraph-migration/experiments/P3-baseline-failures.txt` exits 0 and the file is sorted (`sort -c` exits 0).
- The plan runs in the worktree it changes: `test "$(basename "$(git rev-parse --show-toplevel)")" = codegraph-adoption` exits 0, and `case "$(realpath "$(echo .dev/tasks/*/TASK-WF-phase3CodegraphA-20261029-204913)/source.md")" in "$(git rev-parse --show-toplevel)"/*) echo inside;; *) echo outside;; esac` prints `inside`.
- `for f in design/P3-commands/interface-design.md research/codegraph-evaluation.md brainstorm/P3-codegraph-opportunities/merged-requirements.md decisions/P3-access-model/adversarial/P3-access-model-merged.md decisions/P2-indexing-sync/probe-results.md inventory/primitive-usage.md; do test -s ".dev/codegraph-migration/$f" || echo "missing $f"; done` prints nothing (anything printed is an escalation, not a reconstruction).
- Commit `docs(codegraph): record Phase 3 gate and baselines` holding only the decision log, the baseline file, any reference inputs copied in during setup (by exact path), and `.dev/tasks`.

## Task 2: Run prerequisite experiments E-1, E-2, E-3, E-6 and the slots map E-7

Depends on: Task 1

Run source §5 row T0 exactly: scratch worktree `git worktree add .dev/worktrees/cg-sandbox -b tmp/cg-sandbox HEAD`, removed at the end with `git worktree remove .dev/worktrees/cg-sandbox` and `git branch -D tmp/cg-sandbox`. Stub each file under `.dev/codegraph-migration/experiments/P3-T0/` first: `E1-freshness.md` (the 8 steps of `BS` §2.3 plus MCP `codegraph_status` in a nested and a sibling worktree; ends with a line `Outcome: A` or `Outcome: B`), `E2-help.md` (`codegraph <verb> --help` for `callers callees node impact status affected query init telemetry`, and one `--json` sample each for `query`, `affected`, `node`, `callers`, `impact`, recording which accept `--json`), `E3-allowlist.md` (headless `claude -p --allowedTools ...` allowed/denied for `Bash(codegraph query *)`, `affected`, `node`, `callers`, `impact`, `--version`, `init --yes *` and `Bash(pgrep -f *)`; check `claude --help` first), `E6-agent-matrix.md` (for each of `troubleshoot-analyst`, `reflect-reviewer`, `reuse-auditor`, `auggie-reviewer`: a temporary gitignored `.claude/agents/cg-smoke-<agent>.md` with the target roster of source §1.2 rows 5, 7, 8, 12, spawned foreground and background with a brief that calls `mcp__codegraph__codegraph_status`; pass/fail per mode and `claude --version`; delete the copies afterwards, never stage them), and `E7-slots-map.md` (one line per ledger row, `- <ledger file> :: <ledger anchor> :: row <n>` or `- <ledger file> :: <ledger anchor> :: no tier: <reason>`; a ledger row that fits no source §1.2 row is H4). Never run CLI `codegraph status` while an init runs in the sandbox. If E-3 or E-6 needs a session the executor cannot start, use H5. E-5 is not run here (Phase 2 owns it).

Acceptance criteria:
- `for f in E1-freshness E2-help E3-allowlist E6-agent-matrix E7-slots-map; do test -s .dev/codegraph-migration/experiments/P3-T0/$f.md || echo "missing $f"; done` prints nothing.
- `rg -n '^Outcome: (A|B)$' .dev/codegraph-migration/experiments/P3-T0/E1-freshness.md` prints one line.
- `L=.dev/codegraph-migration/handoffs/phase3-codegraph-slots.md; M=.dev/codegraph-migration/experiments/P3-T0/E7-slots-map.md; test "$(rg -c '^- .* :: (row ([1-9]|[1-3][0-9]|4[0-2])|no tier: .+)$' "$M")" -eq "$(( $(rg -c '^\| ' "$L") - 1 ))"` exits 0 (or, when the ledger is not one Markdown table, the hand count is logged as a self decision and matches the map's line count).
- `! git worktree list | rg -q cg-sandbox` exits 0 and `git branch --list tmp/cg-sandbox` prints nothing; `ls .claude/agents/cg-smoke-* 2>/dev/null` prints nothing.
- Commit `docs(codegraph): record Phase 3 prerequisite experiments` with only the five experiment files, the decision log and `.dev/tasks`.
- Group comment 0 (prerequisite experiments) is posted per Constraints, naming the tool-list branch, E-1's outcome and E-6's per-agent results; its URL is in the decision log.

## Phase 2: Group A, shared guide and core docs

## Task 3: Write the shared guide CODEGRAPH.md and its test

Depends on: Task 2

Create `src/superclaude/core/CODEGRAPH.md` (at most 120 lines) with the seven sections of source §4 "Contents of `CODEGRAPH.md`": what it is; readiness check once per run (MCP detection from the tool list, guarded CLI `status`, `access: mcp|cli|none`, `index_state` enum, who indexes: Phase 2's SessionStart hook, the main session per `core/CLAUDE.md`'s block, and the user-typed `/sc:graph init`; both switches `SUPERCLAUDE_CODEGRAPH_PRIMITIVES=off` and `SUPERCLAUDE_CODEGRAPH_AUTOINIT=0` with their scope); the closed list of 14 `graph:*` tokens (including the user message for `graph:not_initialized`: "run `/sc:graph status`; it reports `next_action: run_graph_init`", per `DES` line 478, which governs the guide; `/sc:impact`'s own report keeps naming `/sc:graph init` per `DES` line 456) plus the two fixed lines `Pinned codegraph version: <VERSION from src/superclaude/cli/install_codegraph.py>` and `Freshness experiment E-1: <outcome-A|outcome-B from Task 2>`; the tool table (seven MCP tools, status-only branch, allowed CLI verbs with the flags E-2 captured); standing rules 1-9 of source §1.1 plus the call-site procedure, opened by the sentinel sentence "Caller rows give the caller's definition line, not the call site."; known gaps; and the "Never" section (the only place that names `explore` and the mutating verbs). Outside "Never", never put `index`, `sync`, `uninit`, `unlock`, `upgrade`, `install` or `uninstall` right after `codegraph `, even as a noun: source §4 item 2's "no primitive runs `codegraph sync`" becomes "no primitive syncs the index (see Never)". Add a byte copy `plugins/superclaude/core/CODEGRAPH.md`; add `CODEGRAPH.md` to `KNOWN_CORE_FILES` in `src/superclaude/cli/install_core.py` and to the `"core"` expected list in `tests/unit/test_cli_install.py`; write `tests/core/test_codegraph_guide.py` in the style of `tests/commands/test_research_command.py` (module docstring, `_REPO = Path(__file__).resolve().parents[2]`, `read_text` assertions, no network) asserting everything source §5 row T1 lists.

Acceptance criteria:
- `uv run pytest tests/core/test_codegraph_guide.py tests/unit/test_cli_install.py -q -p no:cacheprovider` passes.
- The test asserts: at most 120 lines; the seven `codegraph_*` tools and all 14 `graph:*` tokens named; both fixed lines present; `explore` and `codegraph index|sync|uninit|unlock|upgrade|install|uninstall` only inside the "Never" section; `SUPERCLAUDE_CODEGRAPH_PRIMITIVES`, `SUPERCLAUDE_CODEGRAPH_AUTOINIT` and `pgrep -f` named; sentinel present; no `src/superclaude/` path; plugin copy byte-identical (`filecmp.cmp(..., shallow=False)`); the sentinel appears in no `*.md` under `src/superclaude/{commands,skills,agents,core,modes}` or `plugins/superclaude` except the two guide copies `src/superclaude/core/CODEGRAPH.md` and `plugins/superclaude/core/CODEGRAPH.md`; the `graph:not_initialized` message names `/sc:graph status`.
- `test "$(sed -n 's/^Pinned codegraph version: //p' src/superclaude/core/CODEGRAPH.md)" = "$(uv run --no-sync python -c 'from superclaude.cli.install_codegraph import VERSION; print(VERSION)')"` exits 0.
- Commit `feat(codegraph): add shared codegraph usage guide`.

## Task 4: Point core docs and routing hints at codegraph

Depends on: Task 3

Apply source §1.2 rows 1, 3, 4, 36, 39 (row 2 is Phase 1's; verify only): in `src/superclaude/core/CLAUDE.md` edit Phase 2's single `| codegraph` MCP-table row in place to name `~/.claude/CODEGRAPH.md`, append the sentence "Skills and agents follow `~/.claude/CODEGRAPH.md`." inside the `<!-- SUPERCLAUDE_CODEGRAPH_BEGIN -->` / `<!-- SUPERCLAUDE_CODEGRAPH_END -->` block (leave Phase 2's seven-tool or status-only first sentence as shipped), and rewrite the `### Refresh-tool selection` "Symbolic queries" row to codegraph first, Grep floor kept, Read before citing; `src/superclaude/modes/MODE_Orchestration.md` and `plugins/superclaude/modes/MODE_Orchestration.md` `## Tool Selection Matrix` row (row 4); `src/superclaude/skills/sc-recommend/refs/delegation-vs-native-heuristics.md` and its plugin twin (row 36); `src/superclaude/mcp/MCP_Auggie.md` (row 39). Extend `tests/core/test_codegraph_guide.py` with the T2 assertions of source §5.

Acceptance criteria:
- `uv run pytest tests/core tests/skills/test_sc_recommend_routing_contract.py tests/commands/test_routing_plugin_parity.py -q -p no:cacheprovider` passes.
- `rg -n -i serena src/superclaude/core/CLAUDE.md src/superclaude/modes/MODE_Orchestration.md plugins/superclaude/modes/MODE_Orchestration.md` prints nothing.
- `test "$(rg -c '^\| codegraph' src/superclaude/core/CLAUDE.md)" -eq 1` exits 0, and that row names `~/.claude/CODEGRAPH.md`.
- `! rg -q codegraph_explore src/superclaude/core/CLAUDE.md` exits 0; each marker line appears exactly once (`rg -c -x` equals 1 for both) and the text between them names `~/.claude/CODEGRAPH.md`.
- The refresh-tool row names `codegraph_search` and still names Grep (asserted by the extended test).
- Commit `feat(codegraph): point core docs at codegraph`.
- Group comment A (shared guide and core docs) is posted per Constraints.

## Phase 3: Group B, agents

## Task 5: Give the four read-only agents codegraph rosters and briefs

Depends on: Task 2

Apply source §1.2 rows 5-12 to `src/superclaude/agents/troubleshoot-analyst.md`, `src/superclaude/agents/reflect-reviewer.md`, `src/superclaude/agents/reuse-auditor.md`, `src/superclaude/agents/auggie-reviewer.md` (no plugin twins exist; confirm with `ls plugins/superclaude/agents`). An agent gets the exact codegraph names of its row only if all its spawn modes passed Task 2's `E6-agent-matrix.md`; otherwise its roster stays native. Rows 9-11: the codegraph step goes above Phase 1's Grep floor, which stays unchanged (row 11: `codegraph_search` by capability tokens when listed, then "Grep by capability tokens + skeleton grep"). Each body gets the one lookup line "For symbols and callers use the codegraph tools per `~/.claude/CODEGRAPH.md`." (auggie-reviewer also "Do not run the `codegraph` CLI through Bash"). Update the `TOOLS` set in `tests/troubleshoot/test_diagnostic_worker_contract.py` (lines 17-26 at the planning HEAD) to the roster E-6 selected for `troubleshoot-analyst`. Write `tests/agents/test_codegraph_rosters.py`, parametrized over the four agents, reading the expected sets from a constant that cites the E-6 file.

Acceptance criteria:
- `uv run pytest tests/troubleshoot/test_diagnostic_worker_contract.py tests/agents -q -p no:cacheprovider` passes.
- The new test asserts per agent: no `mcp__serena` in `tools:`; exactly the codegraph names E-6 allows (none for failed agents, never `mcp__codegraph__*`); body contains `~/.claude/CODEGRAPH.md`; `reuse-auditor.md` `### 8. Cost control` and F4 name both `codegraph_` and `Grep`.
- `rg -n 'codegraph_explore|mcp__codegraph__\*|Bash\(codegraph \*\)' src/superclaude/agents` prints nothing.
- Commit `feat(codegraph): give review and diagnostic agents codegraph tools`.
- Group comment B (agents) is posted per Constraints.

## Phase 4: Group C, troubleshoot and other skills

## Task 6: Ground troubleshoot Tier 1 in codegraph

Depends on: Task 5

Apply source §1.2 rows 13-18 to `src/superclaude/commands/troubleshoot.md` and `plugins/superclaude/commands/troubleshoot.md`, `src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md` (frontmatter `allowed-tools` gains `mcp__codegraph__codegraph_status`, `_search`, `_node`, `_callers`, `_impact`; `### Wave 1` step 1 second bullet uses `codegraph_node {file, symbolsOnly:true}` or `codegraph_node {symbol, includeCode:true}` plus `codegraph_callers`, with the existing Glob + Grep floor kept below; Wave 0 step 3, TARGET header `mcps_available: <auggie|codegraph|context7|tavily|none>`, Wave 1 exit, failure table, tool matrix and Will-do say auggie/codegraph), `src/superclaude/skills/sc-troubleshoot-protocol/refs/triage-checklist.md` (row 17) and `refs/diagnosability-audit.md` (row 18). The analyst brief (Wave 1.6 and Tier 2) passes `index_state`, `checked_at`, `worktree_root` and `projectPath` (access decision §4). In the status-only branch the skill (unrestricted Bash) uses the CLI read verbs per standing rule 6. Write `tests/troubleshoot/test_codegraph_grounding.py` with the T4 assertions of source §5.

Acceptance criteria:
- `uv run pytest tests/troubleshoot -q -p no:cacheprovider` passes.
- The new test asserts: the five `mcp__codegraph__codegraph_{status,search,node,callers,impact}` names in `allowed-tools` and no `codegraph_explore`; `### Wave 1` names `codegraph_node` and still names the `Glob` + `Grep` fallback; the TARGET header line matches the source text; the analyst brief names the four state fields; none of the four files contains `serena` (any case).
- Commit `feat(codegraph): ground troubleshoot Tier 1 in codegraph`.

## Task 7: Use codegraph in validate-roadmap, brainstorm, task, tasklist, cleanup-audit and auggie-review

Depends on: Task 6

Apply source §1.2 rows 30-38 and 40 to: `src/superclaude/commands/validate-roadmap.md`, `src/superclaude/skills/sc-validate-roadmap-protocol/SKILL.md` (row 31: codegraph tier first, Phase 1's Grep-definition floor unchanged below it with the same 30-lookup cap and INFORMATIONAL ONLY artifact, never "skip"), `src/superclaude/skills/sc-brainstorm-protocol/SKILL.md` and `refs/handoff-routing.md`, `src/superclaude/commands/brainstorm.md` and plugin twin, `src/superclaude/skills/sc-task-protocol/SKILL.md` (rows 33-34; P3-D8; its `allowed-tools` gains the exact `mcp__codegraph__codegraph_callers` and `mcp__codegraph__codegraph_impact` names its STANDARD and STRICT text calls; Task 12 later replaces the inline STRICT step 7 text with the `/sc:impact` call), `src/superclaude/commands/task.md` and plugin twin (verify only: their `mcp-servers:` line, line 7 at the planning HEAD, has no `serena` after Phase 1 and gains nothing), `src/superclaude/skills/sc-tasklist-protocol/SKILL.md` (§5.5 STRICT row becomes `| STRICT | None | codegraph, Context7 | Yes (recorded) |`), `src/superclaude/skills/sc-cleanup-audit-protocol/SKILL.md`, `src/superclaude/commands/cleanup-audit.md`, `src/superclaude/commands/auggie-review.md`, `src/superclaude/skills/sc-auggie-review-protocol/SKILL.md` (deep-pass brief passes the four state fields). Row 40 in this task: `mcp-servers:` gains `codegraph` in this task's own `validate-roadmap`, `brainstorm`, `cleanup-audit` and `auggie-review` command and skill files (troubleshoot is Task 6 via row 13, reflect is Task 10, the new commands get it from `DES` frontmatter). Write `tests/skills/test_codegraph_adoption.py`, parametrized over (file, required token), with the T5 assertions of source §5.

Acceptance criteria:
- `uv run pytest tests/skills/test_codegraph_adoption.py tests/skills/test_brainstorm_protocol.py tests/skills/test_sc_recommend_routing_contract.py tests/commands tests/sc-roadmap -q -p no:cacheprovider` passes.
- The new test asserts: validate-roadmap Step 0.5 names both `codegraph_search` and `Grep` and does not contain `skip`; brainstorm Tier 2 names `codegraph_files` and `codegraph_search`; task-protocol STANDARD step 2 names `codegraph_callers`; the tasklist §5.5 STRICT row equals the text above; cleanup-audit and auggie-review name `codegraph`; the auggie-review deep-pass brief names `index_state`, `checked_at`, `worktree_root`, `projectPath`; no listed file contains `mcp__serena`.
- Commit `feat(codegraph): use codegraph in validate-roadmap, brainstorm, task, tasklist, cleanup-audit, auggie-review`.
- Group comment C (troubleshoot and other skills) is posted per Constraints.

## Phase 5: Group D, new commands

## Task 8: Add /sc:graph with its protocol skill and tests

Depends on: Task 3

Build `src/superclaude/commands/graph.md` (thin; activates `> Skill sc:graph-protocol`; holds the only `Bash(codegraph init --yes *)` and `Bash(codegraph init -i)` calls) and `src/superclaude/skills/sc-graph-protocol/SKILL.md` from `DES` §2 (frontmatter, flags `status|init`, `--worktree-local`, `--output-dir`, internal `--post-init`, steps G-R to G-V, contract, 8-line screen report) with source §3 overrides (a)-(e): switch `SUPERCLAUDE_CODEGRAPH_PRIMITIVES=off`; guarded CLI `status` (`Bash(pgrep -f *)` in the skill); `init` preflight refuses while `pgrep -f 'codegraph\.js (init|index)'` prints a line; purpose text follows Phase 2's indexing model (hook default, `/sc:graph init` manual path); `next_action: status_only_branch` replaces `add_mcp_tool_list`. Exact allowed tools: source §3.2. The guide lookup line of source §4 goes in both files; the E-1 line takes Task 2's outcome. Add `graph.md` to both `"commands"` lists and `sc-graph-protocol` to both `"skills"` lists in `tests/unit/test_cli_install.py`; write `tests/commands/test_graph_command.py` (the 14 tests of `DES` §7.2, plus: the `pgrep -f` guard in the `init` preflight, `SUPERCLAUDE_CODEGRAPH_PRIMITIVES` named and `IRONCLAUDE_CODEGRAPH` absent). In `tests/recommend/test_routing_refresh.py` add a module constant `_POST_REFRESH_ADDITIONS = {"graph"}` with a comment naming issue #323 and compare `shipped - _POST_REFRESH_ADDITIONS == active` (the test asserts `shipped == active` near lines 638-640 at the planning HEAD); never edit the `.dev/tasks/*/TASK-RESEARCH-recommend-refresh-20261024-044336/` package.

Acceptance criteria:
- `uv run pytest tests/commands/test_graph_command.py tests/unit/test_cli_install.py tests/recommend/test_routing_refresh.py -q -p no:cacheprovider` passes.
- `rg -n 'Bash\(codegraph (init|index|sync|uninit|unlock|upgrade|install|uninstall|telemetry (on|off))' src/superclaude/{commands,skills,agents} plugins/superclaude/{commands,skills,agents} | rg -v '^src/superclaude/commands/graph.md:'` prints nothing.
- `rg -n 'IRONCLAUDE_CODEGRAPH' src/superclaude plugins/superclaude` prints nothing.
- Commit `feat(codegraph): add /sc:graph for index status and user-typed init` (the spec's message, source §5 T6).

## Task 9: Add /sc:impact with its protocol skill and tests

Depends on: Task 8

Build `src/superclaude/commands/impact.md` (thin; `## Activation` says `> Skill sc:impact-protocol`) and `src/superclaude/skills/sc-impact-protocol/SKILL.md` from `DES` §4 (frontmatter, flags, steps 1-10, call-site confirmation, contract, the 12-section `impact.md` layout, failure table) with source §3 overrides (a)-(c). Do not copy the example values of the `DES` §4.d contract example into the skill or `impact.md`: it names `install_codebase_memory_mcp`, a function Phase 1 deletes, and `src/superclaude/cli/...` paths, which `test_impact_guide_lookup_line` rejects (only the labelled guide fallback may carry a `src/superclaude/` path); use neutral placeholder symbols and paths (final check by Q, FINAL-SUMMARY defect Q-M2). Overrides: switch name; guarded CLI `status`; in the status-only branch steps 3-5 use the CLI forms `codegraph query|node|callers|impact` with the flags E-2 captured, then the Grep fallback of step 9. The skill's `allowed-tools` is exactly the source §3.1 "Allowed tools (skill)" list (including `Bash(pgrep -f *)`, `Bash(codegraph node *)`, `Bash(codegraph callers *)`, `Bash(codegraph impact *)`; never `Bash(codegraph *)` or `mcp__codegraph__*`). Add `impact.md` and `sc-impact-protocol` to the lists in `tests/unit/test_cli_install.py`; `_POST_REFRESH_ADDITIONS` in `tests/recommend/test_routing_refresh.py` gains `"impact"`; write `tests/commands/test_impact_command.py` with all tests of `DES` §7.1 except `test_impact_callers_wired` (Task 12 adds it), plus the exact allowed-tools set and the status-only CLI transport described before the Grep fallback.

Acceptance criteria:
- `uv run pytest tests/commands/test_impact_command.py tests/commands/test_graph_command.py tests/unit/test_cli_install.py tests/recommend/test_routing_refresh.py -q -p no:cacheprovider` passes.
- `rg -n 'Bash\(codegraph \*\)|mcp__codegraph__\*|codegraph_explore' src/superclaude/commands/impact.md src/superclaude/skills/sc-impact-protocol` prints nothing.
- Commit `feat(codegraph): add /sc:impact for dependents and advisory test lists`.
- Group comment D (new commands) is posted per Constraints.

## Phase 6: Group E, reflect

## Task 10: Rebuild the reflect evidence chain on codegraph

Depends on: Task 9

Apply source §1.2 rows 19-26, 28, 29 to `src/superclaude/skills/sc-reflect-protocol/SKILL.md`, its refs `refs/runtime-surface.md`, `refs/coverage-mapping.md`, `refs/reviewer-spec.md`, `refs/deviation-taxonomy.md`, `refs/reflection-rubric.md`, `refs/cost-profile.yaml`, and `src/superclaude/commands/reflect.md` plus `plugins/superclaude/commands/reflect.md` (that twin differs: change matching sentences only). Key points: `allowed-tools` holds `mcp__codegraph__codegraph_status`, `_search`, `_node`, `_callers`, `_callees`, `_impact`; Step 1B.3 and chain 4/4b call `> Skill sc:impact-protocol` with `--diff <baseline_ref> --depth 1 --limit 100 --output-dir <output>/artifacts/impact --caller sc-reflect-protocol` (`DES` §5), reading only its contract, and log production and test caller counts separately while the HIGH rule keeps today's count; section 6 renamed `## 6. Code-graph evidence chain`; every codegraph step sits above Phase 1's floor (row 20 1a: `find_declaration_no_match` only when the floor also finds nothing); steps 5/5.5 and §6.1.1 were already moved to Bash by Phase 1 (verify, do not redo); step 7 keeps Phase 1's `[INFERRED]` text with no codegraph tier and no new token; the `--with-hierarchy` flag is removed (P3-D6); row 40: the `mcp-servers:` line of both `reflect.md` files (line 6 at the planning HEAD) gains `codegraph` after Phase 1's `serena` strip; the Wave 3 reviewer brief and the 4a reuse-auditor brief pass the four state fields. Extend `tests/skills/test_codegraph_adoption.py` with the T8 assertions of source §5.

Acceptance criteria:
- `uv run pytest tests/skills/test_codegraph_adoption.py tests/skills/test_reflect_input_snapshot.py tests/cli/reflect tests/roadmap/test_threshold_registry.py -q -p no:cacheprovider` passes.
- The extended test asserts: `Skill sc:impact-protocol` and `--caller sc-reflect-protocol` present; both briefs name `index_state`, `checked_at`, `worktree_root`, `projectPath`; heading `## 6. Code-graph evidence chain` exists; `allowed-tools` holds the six codegraph names; Step 1B.3 logs production and test counts separately; the files contain none of `type_hierarchy` (except the Phase 1 field `type_hierarchy_invoked`), `--with-hierarchy`, `get_diagnostics_for_file`, `execute_shell_command`, `mcp__serena`, `search_deps:unindexed`; §6.1.1 names `Bash`.
- Commit `feat(codegraph): rebuild the reflect evidence chain on codegraph`.

## Task 11: Pin that graph tokens never halt reflect

Depends on: Task 10

Add `test_graph_tokens_do_not_halt` to `tests/cli/reflect/test_verdict_mapping.py` and a fixture `tests/cli/reflect/fixtures/degraded_graph_absent.yaml` (a copy of an existing passing fixture with `degraded_components: ["graph:absent", "graph:not_initialized"]`). No change to `src/superclaude/cli/reflect/contract.py`: `graph:*` tokens stay out of `_DEGRADED_COMPONENTS_HALT_SET` (P3-D7).

Acceptance criteria:
- `uv run pytest tests/cli/reflect -q -p no:cacheprovider` passes, and the new test asserts the fixture maps to the same verdict as the same fixture without the tokens.
- `git diff --name-only "$(git merge-base HEAD origin/master)" -- src/superclaude/cli/reflect/contract.py` prints nothing (no Phase 3 commit or working change touched it).
- Commit `test(codegraph): pin that graph tokens never halt reflect`.
- Group comment E (reflect) is posted per Constraints.

## Phase 7: Group F, callers of /sc:impact and routing

## Task 12: Wire /sc:impact callers, /sc:load, /sc:explain and the routing table

Depends on: Task 11

Per source §5 row T10 and `DES` §5, add the exact `> Skill sc:impact-protocol` line and arguments to: `src/superclaude/skills/sc-implement-protocol/SKILL.md` and its byte-identical twin `plugins/superclaude/skills/sc-implement-protocol/SKILL.md` (Q1 and Q6); `src/superclaude/skills/sc-pr-submit-protocol/SKILL.md` and the wave ref it lazy-loads for Waves 3-4 (find with `rg -n 'Wave 4' src/superclaude/skills/sc-pr-submit-protocol`): Wave 3, Wave 4, VG-1; `src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md` Wave 6 Phase A (`--fix` handoff); `src/superclaude/skills/sc-auggie-review-protocol/SKILL.md` `### Wave 1: Collect Inputs`; `src/superclaude/skills/sc-task-protocol/SKILL.md` STRICT step 7 (the `/sc:impact` call replaces Task 7's inline `codegraph_impact` text there), with `Skill` added to its `allowed-tools`. Each caller reads only `return-contract.yaml`, copies `degraded` into its own list, treats `blocked`/`failed` as `graph:absent`, and changes no gate, severity or touched-file rule. Also: `src/superclaude/commands/load.md` and plugin twin get one readiness line naming `/sc:graph status`; `src/superclaude/commands/explain.md` and plugin twin get a one-hop view via `codegraph_search`, `codegraph_callers`, `codegraph_callees` (limit 10, rows re-Read); `src/superclaude/core/HOW-WE-WORK.md` `<!-- other-commands:v1 -->` table gains `/sc:graph` and `/sc:impact` rows in alphabetical order (one sentence each; `/sc:graph init` is the manual indexing path, the session-start hook indexes by default; ASCII characters only, which `tests/core/test_how_we_work_routing_table.py` enforces), then byte copy it to `plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md`. In `tests/core/test_how_we_work_routing_table.py` add `"sc:graph"` and `"sc:impact"` to the `_OTHER_COMMANDS` set (it pins the table's members exactly, `members == _OTHER_COMMANDS`, lines 27-37 and 294 at the planning HEAD). Add `test_impact_callers_wired` to `tests/commands/test_impact_command.py`.

Acceptance criteria:
- `uv run pytest tests/commands tests/core/test_how_we_work_routing_table.py tests/cli/test_how_we_work_install.py tests/recommend/test_routing_refresh.py tests/skills -q -p no:cacheprovider` passes.
- `cmp src/superclaude/core/HOW-WE-WORK.md plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md` and `cmp src/superclaude/skills/sc-implement-protocol/SKILL.md plugins/superclaude/skills/sc-implement-protocol/SKILL.md` exit 0.
- `test_impact_callers_wired` asserts each wired caller contains `Skill sc:impact-protocol` with its own `--caller` value.
- `rg -n '"sc:graph"' tests/core/test_how_we_work_routing_table.py` and `rg -n '"sc:impact"' tests/core/test_how_we_work_routing_table.py` each print a line.
- Commit `feat(codegraph): call /sc:impact from implement, pr-submit, troubleshoot, auggie-review and task`.
- Group comment F (callers and routing) is posted per Constraints.

## Phase 8: Group G, final verification, PR and Coder addendum

## Task 13: Add the changelog and user-doc entries and run the full Phase 3 verification and live smoke

Depends on: Task 12

Add one `CHANGELOG.md` entry for `/sc:impact`, `/sc:graph` and `~/.claude/CODEGRAPH.md`, and one short paragraph in `docs/user-guide/mcp-installation.md` after Phase 2's codegraph section naming the two commands, the guide path and both switches with their scope. Then run every check (0)-(9) of source §5 row T11 and record each command and result in `.dev/codegraph-migration/experiments/P3-T11-smoke.md` (stub first): sync and `make verify-sync`; installed-path count equals baseline (a); zero old tool names (the `rg --pcre2` command in that row); invocation-form mutating-verb check; no wildcard; no explore outside `core/`; pin parity; targeted tests against baseline (b); live smoke (`/sc:graph status`, `/sc:impact install_core_files --output-dir .dev/codegraph-migration/experiments/P3-T11-impact`, `/sc:troubleshoot "install_core_files skips files" --depth quick`), with the status-only variants of that row. Run the live smoke in a fresh `claude` session started in the worktree after `make sync-dev` (a running session may not load the new commands); `~/.claude/CODEGRAPH.md` does not exist there (no `superclaude install`), so record that the guide resolved through the labelled fallback `src/superclaude/core/CODEGRAPH.md`; if no fresh session can be started, use H5 for this check and log it. Fix any failure in the file it concerns (two attempts, then the decision rules, then H3).

Acceptance criteria:
- `rg -q 'sc:impact' CHANGELOG.md && rg -q 'sc:graph' CHANGELOG.md && rg -q 'SUPERCLAUDE_CODEGRAPH_PRIMITIVES' docs/user-guide/mcp-installation.md && rg -q 'SUPERCLAUDE_CODEGRAPH_AUTOINIT' docs/user-guide/mcp-installation.md` exits 0.
- `make sync-dev && make verify-sync` passes.
- With `N` set to baseline (a) from the decision log, `test "$(grep -rIn 'src/superclaude' src/superclaude/{commands,skills,agents,core,hooks} | grep -v 'src/superclaude/core/CODEGRAPH.md' | wc -l)" -le "$N"` exits 0 (a decrease is logged; the `grep -v` filter also drops every labelled-fallback lookup line, which is why the count does not grow).
- The old-tool-name `rg -n -i --pcre2 ...` command of source §5 row T11 prints nothing, `rg -n 'Bash\(codegraph \*\)|mcp__codegraph__\*' src/superclaude/{commands,skills,agents,core,hooks,modes} plugins/superclaude -g '!**/core/CODEGRAPH.md'` prints nothing, and `rg -n 'codegraph_explore|codegraph explore|codegraph context' src/superclaude/{commands,skills,agents,hooks,modes} plugins/superclaude -g '!**/core/CODEGRAPH.md'` prints nothing (the `-g` exempts the guide `core/CODEGRAPH.md` and its plugin copy, whose "Never" section names these strings by design).
- The Task 8 invocation-form check prints nothing; pin parity (Task 3's `test` command) exits 0.
- `$TESTSET` (Constraints; it holds every task's test paths) plus the test files Tasks 3-12 created, run through the Constraints pipeline into `.dev/codegraph-migration/experiments/P3-T11-failures.txt`, gives `comm -13 .dev/codegraph-migration/experiments/P3-baseline-failures.txt .dev/codegraph-migration/experiments/P3-T11-failures.txt` with no output.
- `P3-T11-smoke.md` records the real result of each live smoke command, including whether `/sc:impact` marked `install` in `src/superclaude/cli/main.py` as `call-site-verified` (checked first with `rg -n 'install_core_files\(' src/superclaude/cli/main.py`).
- Commit `chore(codegraph): sync dev copies and record Phase 3 smoke results` (the spec's message, source §5 T11) holding only `src/`, `plugins/`, `tests/`, `CHANGELOG.md`, `docs/` and `.dev/` files (never `.claude/`).

## Task 14: Open the PR on the fork and post the Coder addendum

Depends on: Task 13

Work in this order. `/sc:pr-submit` has no `--body-file` flag (it takes `--title` and `--body` only, `~/.claude/commands/sc/pr-submit.md` argument hint and options table) and places `--body` inside double quotes, so a Markdown body must never be passed inline.
- Step 1, pre-PR checks of repo `CLAUDE.md` "PR Target = Fork": `git remote -v` shows `origin` = `IronbellyOrg/IronClaude`; `gh repo view --json nameWithOwner -q .nameWithOwner` prints `IronbellyOrg/IronClaude`; `git fetch origin` and rebase onto `origin/master` if it moved. After a rebase, re-run Task 13 checks (1)-(8) and note the old and new SHA of every group commit for comment G.
- Step 2, write the PR body to `.dev/codegraph-migration/progress/P3-pr-body.md` (groups 0-G, the smoke results, the deferred ideas of source §2.3, ending with the PR attribution line the session gives).
- Step 3, run `/sc:pr-submit --monitor 3 --head feat/codegraph-adoption --title "feat(codegraph): adopt codegraph in primitives; add /sc:impact and /sc:graph (#323)" --body "Phase 3 codegraph adoption for issue 323; full description follows."` (a plain placeholder with no backtick, dollar sign, quote or backslash), then `gh pr edit <n> --repo IronbellyOrg/IronClaude --body-file .dev/codegraph-migration/progress/P3-pr-body.md`. (source §5 T12, second-pass fix M-01).
- Step 4, write `.dev/codegraph-migration/progress/P3-coder-addendum.md` addressed to the Coder agent: branch head SHA, the exact lines from `<!-- SUPERCLAUDE_CODEGRAPH_BEGIN -->` to `<!-- SUPERCLAUDE_CODEGRAPH_END -->` of `src/superclaude/core/CLAUDE.md` at that SHA, the guide path `~/.claude/CODEGRAPH.md` (installed by `superclaude install` from `src/superclaude/core/`, which Coder's `ironclaude` slug runs), and the instruction to pick both up at the next pin bump through the marker re-sync the Coder handoff defines; post it with `gh issue comment 323 --repo IronbellyOrg/IronClaude --body-file .dev/codegraph-migration/progress/P3-coder-addendum.md`.
- Step 5, write `.dev/codegraph-migration/progress/P3-G.md` and post group comment G per Constraints with the PR link and the addendum link; record the PR, addendum and comment-G URLs in the decision log.
- Step 6, one commit `docs(codegraph): record PR and Coder addendum links` with `P3-pr-body.md`, `P3-coder-addendum.md`, `P3-G.md`, the decision log and `.dev/tasks`, then `git push origin feat/codegraph-adoption`. Log the commit as a departure from source §5 T12 ("no new commit unless the monitor pushes fixes"), required by source §5 "commit after every task".
- Step 7, run `/sc:pr-submit --monitor 3 --pr <n>` once more so CI and the review of that last push are watched. Merging is human (H2); the executor never merges.

Acceptance criteria:
- The PR URL starts with `https://github.com/IronbellyOrg/IronClaude/pull/`.
- `gh pr view <n> --repo IronbellyOrg/IronClaude --json body -q .body | diff - .dev/codegraph-migration/progress/P3-pr-body.md` prints nothing (allow for one trailing newline).
- `rg -q 'SUPERCLAUDE_CODEGRAPH_BEGIN' .dev/codegraph-migration/progress/P3-coder-addendum.md` exits 0 and `rg -q 'issuecomment' .dev/codegraph-migration/decisions/P3X-execution-log.md` exits 0 (addendum and comment-G URLs recorded).
- `gh pr checks <n> --repo IronbellyOrg/IronClaude` shows no failing check after the Step 7 monitor run finishes.
- `git status --short` prints nothing after Step 7.

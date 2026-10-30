# Reviewer brief 1 (persona: analyzer)
Role: read-only Tier-2 reviewer for an `/sc:reflect --mode pre` (UC-1) audit of a proposed implementation plan against its driving spec. Audit only the supplied hunks and what you can Read/Grep/Glob from the repo root `/home/coder/workspaces/worktrees/IronClaude/feat-codememory-codegraph-init`. Do not run anything. Return findings as YAML (shape at the end).

Lens: ordering and dependency defects, acceptance commands that cannot pass at the task where they run, tasks that need a later task to go green, wrong file/line targets, and steps that contradict the spec.

## T1 card excerpt

## Deviation / root-cause section (analyzer lens)

### F-1 Task 12's repo-wide memory-name search cannot pass at Task 12 (red acceptance)
- Evidence: Task 12 acceptance runs `rg -n --no-ignore 'write_memory|...|get_current_config' src/superclaude plugins/superclaude commands agents` (tasklist Task 12). Two hits survive Task 12: `src/superclaude/skills/sc-reflect-protocol/refs/reflection-rubric.md:127` (contains `get_current_config`; the file is row P84, owned by Task 13, which runs later) and `src/superclaude/cli/reflect/contract.py:30` (comment lists `get_current_config`; Task 7 rewords that comment but its acceptance checks only `serena`).
- Class: plan defect (ordering / acceptance scope), inherited from source §8 T10/T10b.
- Fix: Task 7 also removes `get_current_config` from the `contract.py:28-31` comment and checks `rg -n 'get_current_config' src/superclaude/cli/reflect` prints nothing; Task 12's repo-wide search excludes `src/superclaude/skills/sc-reflect-protocol/refs/reflection-rubric.md` (Task 13 deletes lines 124-127, and Task 15's `acceptance-search.sh serena src/superclaude ...` covers it, because `SER` contains `get_current_config`).

## Structural section

- Phases: 6 (G0-G5), tasks 1-19 contiguous, every `Depends on` names a lower task; one commit per task; issue-#323 comment at the end of each phase (Tasks 1, 6, 9, 15, 17, 19); decision rules and test baseline rule in Constraints; final full-suite comparison in Task 18.
- Row coverage check (script, this run): every §1.2 row with Task `T9` (33 rows) appears in Task 10; every `T10`/`T11` row appears in Tasks 11-15 (P69, P70 through the `P68-P71` range); `T12` rows C8-C12, S7, S9-S13, S16, S17, S20-S31 appear in Task 16; `T13` rows S1-S5 in Task 17.
- Grounding: every repo path the plan cites exists except files the plan creates (`install_retired_mcp.py`, `test_install_retired_mcp.py`, `test_install_mcp_cli.py`, the two `.dev/codegraph-migration/handoffs/` files). Spot-checked lines match: `src/superclaude/cli/main.py:254`, `install_mcp.py:916`, `hooks/hooks.json:47`, plugin `hooks.json:37`, `tests/cli/test_install_hooks.py:684`, `commands/pm.md:52`, `core/CLAUDE.md:112`, `sc-tasklist-protocol/SKILL.md:683`, `tests/cli/eval/test_coverage_gate.py:127`, `reflect/ensemble.py:824`, `install_mcp.py:1319` ("Unknown MCP server selection").

## Risk register

- R-1 (HIGH, F-1): Task 12 acceptance is red by construction (repo-wide `get_current_config` hits in a Task-13 file and in a comment Task 7 rewrites without checking that token).
- R-2 (MEDIUM): Task 9's acceptance relies on the message at `src/superclaude/cli/install_mcp.py:1319` ("Unknown MCP server selection: ...") surviving Task 5, which rewrites `:1243-1343 (parts)` of the same file; no Task 5 check pins it.
- R-3 (LOW): Task 18's `./update.sh` sandbox run needs network for `pipx install --force ./`; the documented fallback records a deviation, not a pass.
- R-4 (LOW, F-2): without the scope Constraint an executor could "clean up" historical `.dev/` text or Coder-owned leftovers while chasing the residual search.


## Grounding hunks

### .dev/tasks/to-do/TASK-WF-phase1RemovalSpe-20261029-185100/TASK-WF-phase1RemovalSpe-20261029-185100.md:1-267

```markdown
---
schema: workflow-plan/1.2
source: ./source.md
strategy: systematic
depth: standard
slug: TASK-WF-phase1RemovalSpe-20261029-185100
version: "1"
priority: Medium
created_date: "2026-10-29"
---

# Phase 1: remove codebase-memory-mcp and Serena from IronClaude (issue #323)

Source: ./source.md
Goal: After Phases 1 and 2 merge, IronClaude neither installs nor references codebase-memory-mcp or Serena (outside the allowlist in ./source.md §2.4), `superclaude install` retires the user-scope registrations IronClaude can prove it wrote (and, once Phase 2's `codegraph_ready()` gate holds, the current-pin Serena entry), Serena memory is replaced by `.superclaude/memory/` files, every primitive step uses a Grep/Read floor instead of Serena tools, and handoff notes exist for Phase 2, Phase 3 and the other IronbellyOrg repos.

## Constraints

- Work on branch `ironbelly/feat-codememory-codegraph-init`, base commit `55d40308`. Do not open a pull request to `master` for Phase 1 alone and do not push to `upstream`; Phases 1 and 2 merge as one unit (./source.md §2.2, D9).
- `$PKG` in every command below means this package's directory as the executor resolves it at run time (the folder that holds this plan); never hardcode it. Evidence goes under `$PKG/artifacts/`; handoff notes for other repos go under `$PKG/handoffs/`.
- One commit per task, conventional commit message as given in each task, ending with the attribution line the executor's session requires. Every commit stages the task package with `git add .dev/tasks` (package, `progress.md` and `artifacts/` included). Never stage or commit `.claude/` content (only `.claude/settings.json` is tracked, and Phase 1 does not touch it). Never use `git add -f` on a `.claude/` path.
- Every edit to a `src/superclaude/...` primitive is mirrored by hand, in the same commit, in its `plugins/superclaude/...` twin and its root `commands/sc-*.md` / `agents/sc-*.md` copy where ./source.md §1.2 lists one (D15).
- After editing `src/superclaude/core/HOW-WE-WORK.md`, copy it byte for byte to `plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md`; if the edit touches the block between `<!-- level-table:v1 -->` and `<!-- /level-table -->`, re-copy that block into `src/superclaude/core/CLAUDE.md`.
- Use `uv run` for Python; standalone scripts run with `uv run --no-project python -I`. Every pytest run uses `-p no:cacheprovider`. Full-suite runs always set `T02_15_PERF_REPORT=/tmp/p1-perf.json` so the tracked `.dev/releases/current/cliEval/evidence/T02.15/perf.json` is not rewritten. After every test run, `git status --short` must list only files the task intends to change; restore any tracked file a test changed.
- Test baseline: the full suite already has failures at the base (W1 saw 27 failed and 16 errors). "Passes" for a targeted command means no failing test id that is not in `$PKG/artifacts/baseline/full.txt` (compare with the `comm -13` form in Task 18); never assume a clean suite.
- Never run the real `./update.sh`, `superclaude install` (including `--list`) or `claude mcp add/remove` against the real `HOME`; every environment check runs in a sandbox `HOME` made with `mktemp -d` (./source.md §10, D8). Never delete user data (`~/.serena`, project `.serena/` folders outside this repo, `~/.cache/codebase-memory-mcp`). Never edit another repository.
- Progress reporting (./source.md §9): at the end of each task group (Phases 1-6 below, i.e. groups G0-G5) post exactly one comment on issue #323 of the fork, and only there. First run `gh repo view --json nameWithOwner -q .nameWithOwner` (must print `IronbellyOrg/IronClaude`; otherwise run `gh repo set-default IronbellyOrg/IronClaude`), then `gh issue comment 323 --repo IronbellyOrg/IronClaude --body "Phase 1 progress: <group id and name> committed on ironbelly/feat-codememory-codegraph-init at <short sha>. Tasks: <task ids>. Checks: <exact commands> -> <result>. Decisions logged: <count, path in task package>. Next: <next group>."`. Never use a bare `gh issue comment` and never `--repo SuperClaude-Org/...`. If `gh` is unauthenticated or fails, record the exact error and the intended body in `$PKG/progress.md` and continue (not a blocker).
- Decision rules (./source.md §10), never stop to ask the user: a simple decision (one obvious option, or one the source already constrains) is made by the executor and logged as one line in `$PKG/decisions.md` (decision, options, method `self`, rationale). A mid-level decision (two or more viable options with real trade-offs inside one task) writes each option to `$PKG/decisions/<task>-<slug>/option-<x>.md`, spawns an agent that runs `/sc:adversarial --compare <option files> --depth quick`, follows its recommendation and logs method `adversarial quick` with the merged-recommendation path. A complex decision (an architectural change to the source's design: retire-step scope, memory store layout, merge order, deleting a file the source keeps) does the same with `/sc:adversarial --compare <option files>` (standard depth) and logs method `adversarial full`.
- A blocked task stays blocked with its reason in `$PKG/progress.md`; continue with tasks that do not depend on it. If a task's acceptance fails, fix it within the task's files; if the fix needs a file another task owns, pull that edit forward and log it in `$PKG/decisions.md`. A task may not need a later task to go green.
- Human actions the executor must not attempt: merging Phases 1 and 2 to `master` (Phase 2's PR via `/sc:pr-submit`) and running the real `./update.sh` on a live workspace after that merge (Phase 2 owns that live check).

## Phase 1: Baseline recorded (group G0)

## Task 1: Record the baseline and write the shared acceptance helpers

Implements ./source.md §8.0 and §8 T0. Run `make sync-dev` (the audit tests need the `.claude/` mirror). Write `$PKG/artifacts/acceptance-search.sh` and `$PKG/artifacts/check_rosters.py` with exactly the contents in ./source.md §8.0 (the `CBM`, `SER` and `ALLOW` patterns verbatim). Record these baselines:
- `uv run pytest tests/cli/test_install_codebase_memory.py tests/cli/test_install_mcp_registry.py tests/cli/test_install_mcp_tavily.py tests/cli/test_update_command.py tests/docs/test_tavily_doc_alignment.py -q -p no:cacheprovider | tee $PKG/artifacts/baseline/cbm.txt` (W1 observed 258 passed, 1 skipped).
- `uv run pytest tests/cli/reflect tests/troubleshoot tests/sc-roadmap tests/core tests/commands tests/skills tests/recommend tests/hooks tests/unit/test_cli_install.py tests/cli/test_install_hooks.py tests/cli/test_update_script.py -q -p no:cacheprovider | tee $PKG/artifacts/baseline/targeted.txt`.
- `T02_15_PERF_REPORT=/tmp/p1-perf.json uv run pytest -q -p no:cacheprovider --tb=line -rfE | tee $PKG/artifacts/baseline/full.txt` (whatever this run shows is the baseline).
- `bash $PKG/artifacts/acceptance-search.sh all > $PKG/artifacts/baseline/search.txt; uv run --no-project python -I $PKG/artifacts/check_rosters.py > $PKG/artifacts/baseline/rosters.txt` (both are expected to report hits now).

Commit `chore(tasks): record the Phase 1 removal baseline (#323)`, then post the G0 issue-#323 comment (Constraints) with the baseline pass/fail counts.

Acceptance criteria:
- `test -s $PKG/artifacts/baseline/full.txt && test -s $PKG/artifacts/baseline/targeted.txt && grep -q 'ACCEPTANCE_SEARCH_FAIL' $PKG/artifacts/baseline/search.txt` succeeds.
- `test -z "$(git status --short -- . ':!.dev')"` succeeds (no source change).
- The G0 commit exists and the G0 issue comment URL (or the recorded `gh` error) is in `$PKG/progress.md`.

## Phase 2: codebase-memory out of the installer and CLI (group G1)

## Task 2: Port the generic `superclaude mcp` tests to a new test file

Depends on: Task 1

Implements ./source.md §8 T1 and row C4. Create `tests/cli/test_install_mcp_cli.py` exactly per `.dev/codegraph-migration/inventory/codebase-memory.md` §4.1: its own home fixture and an `mcp_cli` fixture without any `native`/`install_codebase_memory_mcp` patching; port the 11 tests listed there (971 without the `--uninstall`/`--yes` cases, 1126, 1195, 1217, 1229, 1274, 1285, 1298, 1306, 1114 with `context7` instead of codebase-memory, 1334 gateway part only). The 5 menu/message tests (990, 1001, 1023, 1034, 1049) wait for Task 5. Commit `test(mcp): port generic superclaude mcp tests out of the codebase-memory suite (#323)`.

Acceptance criteria:
- `uv run pytest tests/cli/test_install_mcp_cli.py -q -p no:cacheprovider` passes.
- `uv run pytest tests/cli/test_install_codebase_memory.py tests/cli/test_install_mcp_registry.py tests/cli/test_install_mcp_tavily.py tests/cli/test_update_command.py tests/docs/test_tavily_doc_alignment.py -q -p no:cacheprovider` still shows the counts in `$PKG/artifacts/baseline/cbm.txt`.

## Task 3: Stop `superclaude install` and `install --list` from provisioning codebase-memory

Depends on: Task 2

Implements ./source.md §8 T2 and rows C3, C4, C7. Apply `.dev/codegraph-migration/inventory/codebase-memory.md` §4.2 exactly to `src/superclaude/cli/main.py` (`:66`, `:78-83`, `:161-186`, `:254-262`, the `native_success` exit term, help text `:38`, `:44`, `:50-52`), `tests/cli/test_update_command.py` (fixture `native_phase_guard` reduced to `HOME`, `CLAUDE_CONFIG_DIR` and the plugin/Orca stubs; delete the 5 test functions named in row C7; rewrite `test_install_force_target_do_not_redirect_or_force_native` to drop the native assertions) and `tests/cli/test_install_codebase_memory.py` (delete the cross-entry fixture and tests at `:1382`, `:1517`, `:1614`). The fixture and the `main.py` change land in the same commit, so no real-install test can reach the real upstream installer. Commit `feat(install)!: stop installing codebase-memory-mcp from superclaude install (#323)`.

Acceptance criteria:
- `uv run pytest tests/cli/test_update_command.py tests/cli/test_install_codebase_memory.py tests/cli/test_install_mcp_cli.py tests/cli/test_cli_registration.py tests/unit/test_cli_install.py -q -p no:cacheprovider` passes.
- `rg -n "install_codebase_memory|_NATIVE_INSTALLER|native_phase_guard" src/superclaude/cli/main.py tests/cli/test_update_command.py` prints nothing.

## Task 4: Add the non-fatal retire step for existing workspaces

Depends on: Task 3

Implements ./source.md §3 (decision 3.1, matchers 3.2, behaviour and bounds 3.3, surfaces and messages 3.4, files and tests 3.5) and §8 T3. Create `src/superclaude/cli/install_retired_mcp.py` (the `RETIRED_MCP_SERVERS` table with the sunset comment, the pure `classify_retired_entries()` classifier, the receipt/marker predicates copied from `install_codebase_memory.py:95-100`, `:125-139`, `:185-199`, the message builder and `run_retire_step()`); add `_remove_exact_user_entry(name, matcher)` and a direct-exec `claude` wrapper (argv list, `start_new_session=True`, process-group kill, 10 s per call, 15 s step cap) to `src/superclaude/cli/install_mcp.py`, replacing `_cleanup_user_native_registration`; call the step in `install()` in `src/superclaude/cli/main.py` in the slot of the deleted codebase-memory phase inside its own `try/except Exception`, and add the `install --list` lines and the `update` notice; add the warn-only check to `src/superclaude/cli/doctor.py`. Matchers, exactly as ./source.md §3.2: codebase-memory by absolute-path basename with the binary gate; Serena Tier R rows (a)-(c) removed with `env` and `headers` each absent or `{}`; Tier K (current pin and the other listed shapes) kept and printed as "Legacy Serena registration kept until codegraph is ready ...", only until Phase 2's `codegraph_ready()` gate removes it; the re-register hint uses the name `serena-local`. The literal server names live only in `install_retired_mcp.py` and its test; the module must not import `install_codebase_memory.py`. Write `tests/cli/test_install_retired_mcp.py` with every case listed in ./source.md §3.5, including `env: {}` / `headers: {}` counted as absent and the hint naming `serena-local`; update `tests/cli/test_update_command.py` so the expected call list includes the retire step after user setup. Commit `feat(install): retire stale codebase-memory-mcp and serena user registrations (#323)`.

Acceptance criteria:
- `uv run pytest tests/cli/test_install_retired_mcp.py tests/cli/test_update_command.py tests/cli/test_update_script.py tests/cli/test_install_mcp_tavily.py tests/cli/test_install_mcp_cli.py tests/unit -q -p no:cacheprovider` passes.
- `rg -n 'install_codebase_memory' src/superclaude/cli/install_retired_mcp.py` prints nothing.
- In a sandbox HOME, `T=$(mktemp -d /tmp/p1-list.XXXXXX) && env HOME="$T" CLAUDE_CONFIG_DIR="$T" UV_CACHE_DIR="$(uv cache dir)" uv run --no-sync superclaude install --list > "$T/list.txt"` exits 0 and `rg -c 'codebase-memory-mcp|serena' "$T/list.txt"` prints at least 2 (both "absent"); then `rm -rf "$T"`.
- A failing retire step never changes the `superclaude install` exit code (pinned by a test in `tests/cli/test_install_retired_mcp.py`).

## Task 5: Detach `superclaude mcp` and the MCP registry from codebase-memory

Depends on: Task 4

Implements ./source.md §8 T4, rows C2, C5, C6 and the §7 `install_mcp.py` row. Apply `.dev/codegraph-migration/inventory/codebase-memory.md` §4.3 to `src/superclaude/cli/main.py` and `src/superclaude/cli/install_mcp.py`: delete `--uninstall`/`--yes`, the native blocks listed under row C2, and make the menu "1. Install MCP servers (default)" / "2. Cancel"; keep `read_user_mcp_entry`, `_run_registration_command` and the Task 4 remover. In tests: delete `tests/cli/test_install_codebase_memory.py` lines 834-1380, `tests/cli/test_install_mcp_tavily.py` 382-end (keep 1-375), `tests/cli/test_install_mcp_registry.py` 192-240 (the 3 tests named in row C5); port the 5 deferred menu/message tests into `tests/cli/test_install_mcp_cli.py` and add one `mcp --list` output test; add `"codebase-memory-mcp"` to the `test_removed_mcp_servers_are_not_in_registry` tuple. Commit `feat(mcp)!: remove codebase-memory-mcp from the MCP registry and drop --uninstall/--yes (#323)`.

Acceptance criteria:
- `uv run pytest tests/cli/test_install_mcp_cli.py tests/cli/test_install_mcp_registry.py tests/cli/test_install_mcp_tavily.py tests/cli/test_install_codebase_memory.py tests/cli/test_update_command.py tests/cli/test_install_retired_mcp.py tests/docs/test_tavily_doc_alignment.py tests/recommend -q -p no:cacheprovider` passes.
- `rg -n "codebase_memory|_native_|install_codebase_memory_mcp|uninstall_codebase_memory_mcp|--uninstall|--yes" src/superclaude/cli/main.py src/superclaude/cli/install_mcp.py` prints nothing.

## Task 6: Delete the codebase-memory installer module and its test file

Depends on: Task 5

Implements ./source.md §8 T5 and row C1. `git rm src/superclaude/cli/install_codebase_memory.py tests/cli/test_install_codebase_memory.py` (deletion only). Commit `refactor(cli)!: delete the codebase-memory installer module (#323)`, then post the G1 issue-#323 comment (Constraints).

Acceptance criteria:
- `rg -n "install_codebase_memory|codebase_memory" src tests -g '!src/superclaude/cli/install_retired_mcp.py' -g '!tests/cli/test_install_retired_mcp.py'` prints nothing.
- `uv run pytest tests/cli tests/unit tests/recommend tests/docs -q -p no:cacheprovider --ignore=tests/cli/eval -rfE` has no failing test id that is not in `$PKG/artifacts/baseline/full.txt`.
- `uv run ruff check src/superclaude/cli tests/cli` passes and `bash $PKG/artifacts/acceptance-search.sh cbm src tests` prints `ACCEPTANCE_SEARCH_OK cbm`.
- The G1 issue comment URL (or the recorded `gh` error) is in `$PKG/progress.md`.

## Phase 3: Serena out of CLI code, hooks and the registry (group G2)

## Task 7: Remove Serena tokens from the reflect verdict contract

Depends on: Task 6

Implements ./source.md §8 T6, rule G7, rule G8 and rows S42-S44, S58-S86. In `src/superclaude/cli/reflect/contract.py` drop `"serena"` and `"serena:context-excluded"` from `_DEGRADED_COMPONENTS_HALT_SET` and fix the comment (`:28-34`); delete the `serena_summary_corroboration` key in `src/superclaude/cli/reflect/ensemble.py:824` and its line in the 24 fixtures listed as S58-S82 (except S65); delete `tests/cli/reflect/fixtures/degraded_serena.yaml`; in `degraded_with_drift.yaml` replace `- serena` with `- auggie`; delete `test_degraded_serena` and `test_serena_summary_corroboration_unavailable_not_degraded` and edit the token list at `tests/cli/reflect/test_verdict_mapping.py:245`; repoint `tests/cli/reflect/test_runner_e2e.py:71` to `degraded_tier1.yaml` and keep its exit-11 assertion; reword `src/superclaude/cli/reflect/config.py:162,199`, `tests/cli/reflect/test_ensemble_unit.py:345`, `tests/cli/reflect/test_verify_denylist_git_mutations.py:11`. Commit `refactor(reflect): drop Serena tokens and the serena_summary_corroboration field from the verdict contract (#323)`.

Acceptance criteria:
- `uv run pytest tests/cli/reflect -q -p no:cacheprovider` passes (W2 predicts about 270 tests).
- `rg -n -i 'serena' src/superclaude/cli/reflect tests/cli/reflect` prints nothing.

## Task 8: Drop Serena tools from the freshness hook and the eval suite

Depends on: Task 7

Implements ./source.md §8 T7 and rows P21, P55, D1, D2, S37, S38, S40, S57, S87. Set the matcher to `Edit|Write` in `src/superclaude/hooks/hooks.json:47` and `plugins/superclaude/hooks/hooks.json:37`; in both `freshness-pre-edit.sh` copies (`src/superclaude/hooks/scripts/` and `plugins/superclaude/hooks/scripts/`) delete the `relative_path` branch and reword the line-36 message to "no file_path in tool_input"; delete the four asserts at `tests/cli/test_install_hooks.py:684-687`; in `src/superclaude/cli/eval/suites/real.yaml` delete capability row `:40` and eval E8 (`:566-690`) and fix the comments at `:380-384`, `:406-407`, `:475-479`, `:499-506`; reword `src/superclaude/cli/eval/coverage.py:195` and `src/superclaude/cli/eval/suites/README.md:170`; change the tool string at `tests/cli/eval/test_coverage_gate.py:127` to `mcp__context7__resolve-library-id`. Commit `fix(hooks): drop Serena tools from the freshness gate and the eval suite (#323)`.

Acceptance criteria:
- `uv run pytest tests/cli/test_install_hooks.py tests/hooks tests/cli/eval/test_coverage_gate.py tests/cli/eval/test_no_mcp_skip.py tests/cli/eval/test_schema_validate.py tests/cli/eval/test_capability_gates.py -q -p no:cacheprovider` passes (only these eval files; never the whole `tests/cli/eval/`).
- `rg -n 'mcp__serena|relative_path' src/superclaude/hooks plugins/superclaude/hooks src/superclaude/cli/eval tests/cli/test_install_hooks.py tests/cli/eval/test_coverage_gate.py` prints nothing.

## Task 9: Remove the Serena registry entry and MCP package assets

Depends on: Task 8

Implements ./source.md §8 T8 and rows S32-S36, S41, S46-S51, S88, S100. Delete the Serena registry block and uv advisory in `src/superclaude/cli/install_mcp.py` (`:55-61`, `:561-570`); delete `src/superclaude/mcp/MCP_Serena.md`, `src/superclaude/mcp/configs/serena.json`, `src/superclaude/mcp/configs/serena-docker.json` and the same three under `plugins/superclaude/mcp/`; delete the Serena lines in `src/superclaude/mcp/MCP_Auggie.md`, `MCP_Morphllm.md`, `MCP_Tavily.md` and `plugins/superclaude/mcp/MCP_Morphllm.md`, `MCP_Tavily.md`; delete the Serena entries in `tests/cli/test_install_mcp_registry.py` (both dicts) and add `"serena"` to the `test_removed_mcp_servers_are_not_in_registry` tuple; remove the three names from `tests/unit/test_cli_install.py:150-153` and `:423-425` in the same commit as the deletions. Commit `feat(mcp)!: remove Serena from the MCP registry and package assets (#323)`, then post the G2 issue-#323 comment.

Acceptance criteria:
- `uv run pytest tests/cli/test_install_mcp_registry.py tests/cli/test_install_mcp_tavily.py tests/cli/test_install_mcp_cli.py tests/unit/test_cli_install.py tests/cli/test_update_command.py -q -p no:cacheprovider` passes.
- `rg -n -i serena src/superclaude/cli/install_mcp.py src/superclaude/mcp plugins/superclaude/mcp tests/unit/test_cli_install.py` prints nothing.
- `uv run superclaude mcp --servers serena --dry-run 2>&1 | grep -q 'Unknown MCP server selection: serena'` succeeds.
- The G2 issue comment URL (or the recorded `gh` error) is in `$PKG/progress.md`.

## Phase 4: Serena out of primitives (group G3)

## Task 10: Drop decorative Serena mentions and frontmatter entries

Depends on: Task 9

Implements ./source.md §8 T9, rule G5 (frontmatter part), rule G10 (lines 21 and 90) and rule M6. Edit every ./source.md §1.2 row whose Task column is `T9`: rows P3, P7, P9, P10, P12, P16, P18, P19, P32, P34-P38, P41, P42, P44-P46, P48, P51 (lines 21 and 90 of `src/superclaude/core/CLAUDE.md` only), P53, P60, P61, P66, P67, P72, P74, P75, P88, P89 (sc-roadmap: the `<output_dir>/.session-memory.md` fallback becomes the only path), S92, S93. In tests delete `test_serena_fallback` and `test_serena_referenced` from `tests/sc-roadmap/compliance/test_mcp_circuit_breakers.py`, and delete `test_circuit_breaker_for_serena` and reword `:69-74` in `tests/sc-roadmap/integration/test_wave5_completion.py`. No body text may still point at Serena. Commit `docs(primitives): drop decorative Serena mentions and frontmatter entries (#323)`.

Acceptance criteria:
- `make sync-dev && make verify-sync` passes.
- `uv run pytest tests/sc-roadmap tests/commands tests/skills tests/core tests/cli/test_how_we_work_install.py -q -p no:cacheprovider` passes.
- `rg -n --no-ignore 'mcp-servers:.*serena' src/superclaude plugins/superclaude commands agents` prints nothing.

## Task 11: Move save, load, pm and pm-agent memory to `.superclaude/memory` files

Depends on: Task 10

Implements ./source.md §5 rules M1-M4, M7, M8 and §8 T10a. Rows P1, P4, P5, P8 (root `commands/sc-load.md`, `commands/sc-pm.md`, `commands/sc-save.md`, `agents/sc-pm-agent.md`), P11, P13, P14, P17, P23 (`plugins/superclaude/agents/pm-agent.md`, `plugins/superclaude/commands/{load,pm,save}.md`, `plugins/superclaude/modes/MODE_Task_Management.md`), P27, P39, P40, P47, P57 (`src/superclaude/agents/pm-agent.md`, `src/superclaude/commands/{load,pm,save}.md`, `src/superclaude/modes/MODE_Task_Management.md`) and P73 (`src/superclaude/skills/sc-pm-protocol/SKILL.md`, kept with `/sc:pm` because `src/superclaude/commands/pm.md:52` loads it). Store `<git top-level>/.superclaude/memory/<key>.md`; tool mapping write_memory -> Write, read_memory -> Read, list_memories -> Glob, edit_memory -> Edit, no primitive deletes memories; first write creates `<project>/.superclaude/.gitignore` containing `*` when absent; single-owner keys overwritten whole, parallel-session keys written as `<key>-<session-or-timestamp>.md`; `/sc:load` reads `.serena/memories/<key>.md` only when the new file is absent, for one release, never writes there, and says it is read-only history (the one allowlisted sentence per copy). Commit `feat(memory)!: move save, load, pm and pm-agent memory to .superclaude/memory files (#323)`.

Acceptance criteria:
- `make sync-dev && make verify-sync` passes and `uv run pytest tests/commands tests/skills tests/core -q -p no:cacheprovider` passes.
- `rg -n --no-ignore 'write_memory|read_memory|list_memories|edit_memory|delete_memory|think_about_|\bsummarize_changes\b|activate_project|check_onboarding_performed|prepare_for_new_conversation|get_current_config' src/superclaude/commands/save.md src/superclaude/commands/load.md src/superclaude/commands/pm.md plugins/superclaude/commands/save.md plugins/superclaude/commands/load.md plugins/superclaude/commands/pm.md commands/sc-save.md commands/sc-load.md commands/sc-pm.md src/superclaude/agents/pm-agent.md plugins/superclaude/agents/pm-agent.md agents/sc-pm-agent.md src/superclaude/modes/MODE_Task_Management.md plugins/superclaude/modes/MODE_Task_Management.md src/superclaude/skills/sc-pm-protocol/SKILL.md` prints nothing.
- `rg --files-without-match '\.superclaude/\.gitignore' src/superclaude/commands/save.md src/superclaude/agents/pm-agent.md src/superclaude/skills/sc-pm-protocol/SKILL.md src/superclaude/modes/MODE_Task_Management.md` prints nothing (rule M3 in every writer).

## Task 12: Replace Serena memory in skills, the routing guide and reflect calibration

Depends on: Task 11

Implements ./source.md §5 rules M1-M8 and §8 T10b. Memory parts of rows P6, P15, P43 (`commands/sc-reflect.md`, `plugins/superclaude/commands/reflect.md`, `src/superclaude/commands/reflect.md`), P50 and P96 (`src/superclaude/commands/validate-roadmap.md` memory tool entries; `src/superclaude/skills/sc-validate-roadmap-protocol/SKILL.md` ledger, terminology map and pattern log move to `.superclaude/memory/validate-roadmap/<key>.md`, still fail-open), P77 (`src/superclaude/skills/sc-reflect-protocol/SKILL.md` calibration memory to tracked `docs/memory/reflect/deviation-patterns-<slug>.md`), P91 (`src/superclaude/skills/sc-task-protocol/SKILL.md` STRICT-tier memory and `activate_project` steps); rows P68-P71 (`src/superclaude/skills/sc-crash-recovery/SKILL.md`, `refs/investigators.md`, `refs/report-template.md`, `scripts/bootstrap_scan.sh:146-147` fields renamed `has_memory`, `memory_count`, reading `.superclaude/memory`), P82 and P85 (`sc-reflect-protocol/refs/input-resolution.md`, `refs/remediation-handoff.md`), P24 and P52 (`src/superclaude/core/HOW-WE-WORK.md:237,327,329` plus its byte copy), S89 (`tests/core/test_how_we_work_routing_table.py:1074`), S90 (`tests/recommend/fixtures/routing_refresh_cases.json:576,584`), and S4: `git mv .serena/memories/reflect/deviation-patterns-IronClaude.md docs/memory/reflect/deviation-patterns-IronClaude.md` (content kept). Delete, do not port, the Serena-only calls of rule M8 in these files. Commit `feat(memory)!: replace Serena memory with .superclaude/memory files in skills and the routing guide (#323)`.

Acceptance criteria:
- `make sync-dev && make verify-sync` passes and `uv run pytest tests/core tests/commands/test_routing_plugin_parity.py tests/cli/test_how_we_work_install.py tests/recommend tests/skills tests/sc-roadmap -q -p no:cacheprovider` passes.
- `cmp src/superclaude/core/HOW-WE-WORK.md plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md` succeeds.
- `rg -n --no-ignore 'write_memory|read_memory|list_memories|edit_memory|delete_memory|think_about_|\bsummarize_changes\b|activate_project|check_onboarding_performed|prepare_for_new_conversation|get_current_config' src/superclaude plugins/superclaude commands agents` prints nothing (repo-wide).
- `test -f docs/memory/reflect/deviation-patterns-IronClaude.md` succeeds.

## Task 13: Replace reflect's Serena symbol, reference and diagnostics steps with a Grep/Read floor

Depends on: Task 12

Implements ./source.md §4 rules G1-G9 and §8 T11a. Tool parts of rows P6, P15, P43 (the three reflect command copies: rewrite the tool table, delete the `--onboard` Serena bootstrap rows) and P77 (`src/superclaude/skills/sc-reflect-protocol/SKILL.md`: delete Serena probes and telemetry, symbol chain to the Grep-definition-then-Read floor, step 4.5 deleted, Step 7 `search_deps` skipped with its claim `[INFERRED]`, section 6.1.1 envelope retitled for the Bash linter/type-checker call, `serena` degraded tokens and the section 6.5 and section 10 fallback rows removed); rows P78, P79, P80, P81, P83, P84, P86, P87 (reflect refs `cost-profile.yaml`, `coverage-mapping.md`, `deviation-taxonomy.md`, `grader-extensions.md`, `ops-integration.md` Serena WARN catalog, `reflection-rubric.md:124-127`, `reviewer-spec.md`, `runtime-surface.md`); P28 (`src/superclaude/agents/reflect-reviewer.md`: drop the four tools, rewrite line 147) and P29 (`src/superclaude/agents/reuse-auditor.md`: drop the three tools, `:54`, `:57` F4 to a Grep reference search, `:131` to "Grep by capability tokens + skeleton grep"); D3 (`tests/cli/reflect/test_marker_suppression.py:101-130` follows the retitled 6.1.1 heading), D4 and D5 (drop `execute_shell_command` from the denylist sets in `tests/cli/reflect/test_reviewer_readonly_tools.py:7,31` and `tests/cli/reflect/test_reviewer_finding_parity.py:33`). Keep the stable contract fields of rule G8 (`find_declaration_no_match`, `type_hierarchy_invoked: false`, `summarize_changes_invoked: false`, `references_extended_info_used: false`). Closed rosters lose only `mcp__serena__*` names and never gain Bash. Create `.dev/codegraph-migration/handoffs/phase3-codegraph-slots.md` if absent and append one row per touched step: file, step heading or anchor (not a line number), former Serena tool, action (deleted / floor), floor used, contract fields touched. Commit `refactor(reflect): replace Serena symbol, reference and diagnostics steps with a native Grep/Read floor (#323)`.

Acceptance criteria:
- `make sync-dev && make verify-sync` passes and `uv run pytest tests/cli/reflect tests/skills tests/commands -q -p no:cacheprovider` passes.
- `bash $PKG/artifacts/acceptance-search.sh serena src/superclaude/skills/sc-reflect-protocol src/superclaude/commands/reflect.md plugins/superclaude/commands/reflect.md commands/sc-reflect.md src/superclaude/agents/reflect-reviewer.md src/superclaude/agents/reuse-auditor.md` prints `ACCEPTANCE_SEARCH_OK serena`.
- `comm -13 <(sort $PKG/artifacts/baseline/rosters.txt) <(uv run --no-project python -I $PKG/artifacts/check_rosters.py | sort)` prints nothing.
- `test -s .dev/codegraph-migration/handoffs/phase3-codegraph-slots.md` succeeds and the ledger has rows for `sc-reflect-protocol/SKILL.md`, `reflect-reviewer.md` and `reuse-auditor.md`.

## Task 14: Replace troubleshoot's Serena tools with a Grep/Read floor

Depends on: Task 13

Implements ./source.md §4 rules G1-G9 and §8 T11b, all in one commit (rule G5). Rows P49 (`src/superclaude/commands/troubleshoot.md`: rewrite wording, delete `serena` frontmatter), P93 (`src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md`: delete tools and wording; `:193` keeps its existing Glob + Grep fallback at `:194`; the prose roster at `:31`), P94 and P95 (`refs/diagnosability-audit.md:11`, `refs/triage-checklist.md:11`), P31 (`src/superclaude/agents/troubleshoot-analyst.md:5`: drop the four tools), S99 (`tests/troubleshoot/test_diagnostic_worker_contract.py`: the `TOOLS` set at `:17-26` and the mutant string at `:152`). Diagnostics run the project's own linter or type-checker through Bash under the retitled envelope (rule G4). Append the touched steps to `.dev/codegraph-migration/handoffs/phase3-codegraph-slots.md`. Commit `refactor(troubleshoot): replace Serena tools with a native Grep/Read floor (#323)`.

Acceptance criteria:
- `make sync-dev && make verify-sync` passes and `uv run pytest tests/troubleshoot tests/skills tests/commands -q -p no:cacheprovider` passes.
- `bash $PKG/artifacts/acceptance-search.sh serena src/superclaude/skills/sc-troubleshoot-protocol src/superclaude/commands/troubleshoot.md src/superclaude/agents/troubleshoot-analyst.md` prints `ACCEPTANCE_SEARCH_OK serena`.
- `comm -13 <(sort $PKG/artifacts/baseline/rosters.txt) <(uv run --no-project python -I $PKG/artifacts/check_rosters.py | sort)` prints nothing.
- `rg -q 'sc-troubleshoot-protocol' .dev/codegraph-migration/handoffs/phase3-codegraph-slots.md` succeeds.

## Task 15: Replace the remaining Serena tool steps, rewrite the core refresh row and complete the slots ledger

Depends on: Task 14

Implements ./source.md §4 rules G1-G10 and §8 T11c. Tool parts of rows P50 and P96 (`src/superclaude/commands/validate-roadmap.md` `allowed-tools` and `mcp-servers`; `src/superclaude/skills/sc-validate-roadmap-protocol/SKILL.md` Step 0.5 `:320-349` gets a Grep-definition floor with the same 30-lookup cap and the same INFORMATIONAL ONLY artifact, never "skip") and P91 (`src/superclaude/skills/sc-task-protocol/SKILL.md` STRICT prerequisites); rows P92 (`src/superclaude/skills/sc-tasklist-protocol/SKILL.md:683`, STRICT no longer needs Serena), P26 (`src/superclaude/agents/auggie-reviewer.md`: drop the two tools, rewrite `:36`, `:81`, `:115`), P33 (`src/superclaude/commands/auggie-review.md:6,78`), P2 (`commands/sc-brainstorm.md`), P62 and P63 (`src/superclaude/skills/sc-brainstorm-protocol/SKILL.md` and `refs/handoff-routing.md`, tier-2 block deleted and renumbered), P65 (`src/superclaude/skills/sc-cleanup-audit-protocol/SKILL.md`: frontmatter and line 83; the `.serena/` ignore at `:57` stays, allowlisted), P22 and P56 (`MODE_Orchestration.md` in `plugins/superclaude/modes/` and `src/superclaude/modes/`), P25 and P76 (`delegation-vs-native-heuristics.md` in `plugins/superclaude/skills/sc-recommend/refs/` and `src/superclaude/skills/sc-recommend/refs/`), P51 line 112 (`src/superclaude/core/CLAUDE.md` "Symbolic queries" refresh row becomes "Grep for the definition and references, then Read"). Append the touched steps to the slots ledger and make it cover every load-bearing file of ./source.md §4.2. Commit `refactor(primitives): replace the remaining Serena symbol tools with a native Grep/Read floor (#323)`, then post the G3 issue-#323 comment.

Acceptance criteria:
- `make sync-dev && make verify-sync` passes and `uv run pytest tests/troubleshoot tests/cli/reflect tests/skills tests/commands tests/core tests/roadmap/test_threshold_registry.py -q -p no:cacheprovider` passes.
- `rg -n --no-ignore 'mcp__serena__' src/superclaude plugins/superclaude commands agents` prints nothing.
- `comm -13 <(sort $PKG/artifacts/baseline/rosters.txt) <(uv run --no-project python -I $PKG/artifacts/check_rosters.py | sort)` prints nothing.
- `for f in commands/troubleshoot.md skills/sc-reflect-protocol/SKILL.md skills/sc-troubleshoot-protocol/SKILL.md skills/sc-validate-roadmap-protocol/SKILL.md agents/reuse-auditor.md; do rg -qF "$f" .dev/codegraph-migration/handoffs/phase3-codegraph-slots.md || echo "ledger missing $f"; done` prints nothing.
- `bash $PKG/artifacts/acceptance-search.sh serena src/superclaude plugins/superclaude commands agents` prints `ACCEPTANCE_SEARCH_OK serena`.
- The G3 issue comment URL (or the recorded `gh` error) is in `$PKG/progress.md`.

## Phase 5: Docs, repo files and the tracked `.serena/` folder (group G4)

## Task 16: Remove both servers from user docs, README, CLAUDE.md, SECURITY.md, CI comments and add the CHANGELOG entry

Depends on: Task 15

Implements ./source.md §8 T12 and rows C8-C12, S7, S9-S13, S16, S17, S20-S31. Delete or rewrite per each row's action in `docs/user-guide/mcp-installation.md`, `docs/reference/mcp-server-guide.md`, `docs/mcp/mcp-optional-design.md`, `docs/mcp/mcp-integration-policy.md`, `docs/analysis-sc-tasklist.md`, `docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md`, `docs/developer-guide/technical-architecture.md`, `docs/user-guide/{agents,brainstorm,commands,flags,freshness-hooks,mcp-servers,memory-system,modes,session-management}.md`, `README.md:38,64,75,219`, `CLAUDE.md:377`, `SECURITY.md:328`; delete `docs/troubleshooting/serena-installation.md` and confirm `rg serena-installation` finds no inbound link. In `.github/workflows/test.yml` rewrite only the comments at `:133-134` and `:155` so they name no removed server; keep the `Install Claude CLI` step (`:156-159`) and `permissions: contents: read` (row C12, D20). Add a `CHANGELOG.md` entry: what was removed, the retire step, the manual commands from ./source.md §3.4 for kind-B workspaces and user data; it must not say the current-pin Serena registration is kept for good (it is removed once codegraph is ready, Phase 2 §2.12) and names `serena-local` as the re-register name. No "Retired servers" section in user docs (D7). Commit `docs: remove codebase-memory and Serena from user docs, README and CI (#323)`.

Acceptance criteria:
- `uv run pytest tests/docs tests/core -q -p no:cacheprovider` passes.
- `bash $PKG/artifacts/acceptance-search.sh all docs README.md CLAUDE.md SECURITY.md .github` prints `ACCEPTANCE_SEARCH_OK all`.
- `uv run --no-project python -c 'import yaml,sys; d=yaml.safe_load(open(".github/workflows/test.yml")); s=[x.get("name") for x in d["jobs"]["doctor-check"]["steps"]]; sys.exit(0 if "Install Claude CLI" in s else 1)'` exits 0.
- `rg -q 'serena-local' CHANGELOG.md` succeeds.

## Task 17: Remove the tracked `.serena/` project folder

Depends on: Task 16

Implements ./source.md §8 T13 and rows S1-S5. `git rm .serena/project.yml .serena/memories/memory_maintenance.md .serena/.gitignore` (the calibration file already moved in Task 12); `.gitignore:113` stays (allowlisted, ./source.md §2.4). Commit `chore: remove the tracked .serena project folder (#323)`, then post the G4 issue-#323 comment.

Acceptance criteria:
- `git ls-files .serena` prints nothing and `test -f docs/memory/reflect/deviation-patterns-IronClaude.md` succeeds.
- The G4 issue comment URL (or the recorded `gh` error) is in `$PKG/progress.md`.

## Phase 6: Final gate and handoffs (group G5)

## Task 18: Run the Phase 1 final gate and record its evidence

Depends on: Task 17

Implements ./source.md §2.2 (DoD-1 to DoD-6) and §8 T14; writes only `$PKG/artifacts/final/*`. Run each check and record command and observed result in `$PKG/artifacts/final/summary.md`:
- Sync and lint: `make sync-dev && make verify-sync`; `make lint`; `uv run ruff format --check src/superclaude/cli tests/cli`.
- Full suite against the baseline (DoD-5): `T02_15_PERF_REPORT=/tmp/p1-perf.json uv run pytest -q -p no:cacheprovider --tb=line -rfE | tee $PKG/artifacts/final/full.txt`, then `comm -13 <(grep -E '^(FAILED|ERROR) ' $PKG/artifacts/baseline/full.txt | sed 's/ - .*//' | sort -u) <(grep -E '^(FAILED|ERROR) ' $PKG/artifacts/final/full.txt | sed 's/ - .*//' | sort -u)` prints nothing.
- Residual search (DoD-1): `bash $PKG/artifacts/acceptance-search.sh all | tee $PKG/artifacts/final/search.txt` prints `ACCEPTANCE_SEARCH_OK all`.
- Sandbox "fresh" (DoD-2): `T=$(mktemp -d /tmp/p1-sbx.XXXXXX)`; a stub `claude` at `$T/bin/claude` that logs argv to `$HOME/claude-calls.log`, prints a version for `--version`, deletes `.mcpServers[<name>]` from `${CLAUDE_CONFIG_DIR:-$HOME}/.claude.json` with `jq` for `mcp remove <name> --scope user`, and exits 1 otherwise; `env HOME=$T/fresh UV_CACHE_DIR="$(uv cache dir)" PATH="$T/bin:$PATH" uv run --no-sync superclaude install`; then `rg -n -i 'serena|codebase-memory|codebase_memory' $T/fresh` prints nothing and the call log has no `mcp add`.
- Sandbox "existing" (DoD-3, DoD-4): seed `$T/old/.claude.json` with `mcpServers.codebase-memory-mcp = {"type":"stdio","command":"/usr/local/bin/codebase-memory-mcp","args":[]}`, `mcpServers.serena` = Tier R row (a) of ./source.md §3.2 with `"env":{}`, `mcpServers.tavily` (any value) and `projects["/x"].mcpServers.serena`; seed `$T/old/.claude/settings.json` with one `PreToolUse` entry using the baseline `hooks.json:47` matcher and `~/.claude/hooks/freshness-pre-edit.sh`; run `env HOME=$T/old PIPX_HOME=$T/pipx PIPX_BIN_DIR=$T/pbin UV_CACHE_DIR="$(uv cache dir)" PATH="$T/pbin:$T/bin:$PATH" ./update.sh`. Expect `jq '.mcpServers|keys' $T/old/.claude.json` is `["tavily"]`, `jq '.projects["/x"].mcpServers|has("serena")' $T/old/.claude.json` is `true`, and `rg -n 'mcp__serena' $T/old/.claude/settings.json` and `rg -n -i 'serena|codebase-memory' $T/old/.claude` print nothing. If `pipx install` cannot reach the package index, record the error and run the same checks with `uv run --no-sync superclaude install --force && uv run --no-sync superclaude doctor` in that HOME; record this as a deviation, not as a pass of `update.sh`. Then set `mcpServers.serena` to the current pin with `"env":{}` and run `uv run --no-sync superclaude install --force`: the entry is kept and the output contains "Legacy Serena registration kept until codegraph is ready" (expected for Phase 1 alone; Phase 2's gate removes it later).
- Robustness without a Claude CLI (local only; CI keeps its step): `env HOME=$T/ci UV_CACHE_DIR="$(uv cache dir)" PATH=<a PATH where command -v claude prints nothing> uv run --no-sync superclaude install && uv run --no-sync superclaude doctor --verbose` exits 0.
- Cleanup: `git status --short` shows no modified tracked file outside the package; `rm -rf "$T"`.

Commit `chore(tasks): Phase 1 final gate evidence (#323)`.

Acceptance criteria:
- `$PKG/artifacts/final/summary.md` lists every check above with its exact command and observed result, and every check passed (or the documented `pipx` fallback is recorded as a deviation).
- `$PKG/artifacts/final/full.txt` and `$PKG/artifacts/final/search.txt` exist; the `comm -13` comparison printed nothing and `search.txt` ends with `ACCEPTANCE_SEARCH_OK all`.

## Task 19: Write the Phase 2, Phase 3 and other-repo handoff notes

Depends on: Task 18

Implements ./source.md §6 (6.2 Coder facts, 6.3 notes) and §8 T15. Copy each of the 11 paste-ready notes in ./source.md §6.3 verbatim to `$PKG/handoffs/<repo>.md` (Financials, IronFlow, IronOps, InfraDocs, ClaudeCodeCodeAudit, Ironbrain, Octodive, TUIBBS, TUIBBS-scp, shrapnel-gov, llm-workflows). Write `.dev/codegraph-migration/handoffs/phase2-facts-from-phase1.md` with the ./source.md §6.2 facts, the retire-step behaviour (§3) and the §7 shared-files table, plus a section headed "Phase 2 override: Serena removal" that quotes Phase 2 spec §2.12 (`.dev/codegraph-migration/specs/phase-2-codegraph-install-spec.md`) and names `codegraph_ready()`. Re-check that `.dev/codegraph-migration/handoffs/phase3-codegraph-slots.md` covers every step touched in Tasks 10-15. Commit `docs(tasks): Phase 1 handoff notes for Phase 2, Phase 3 and other IronbellyOrg repos (#323)`, then post the final G5 issue-#323 comment, which also links the handoff files and states the merge constraint (Phases 1 and 2 merge to `master` together; no Phase 1-only PR).

Acceptance criteria:
- `ls $PKG/handoffs/*.md | wc -l` prints 11.
- `test -s .dev/codegraph-migration/handoffs/phase2-facts-from-phase1.md && test -s .dev/codegraph-migration/handoffs/phase3-codegraph-slots.md` succeeds and `rg -q 'codegraph_ready' .dev/codegraph-migration/handoffs/phase2-facts-from-phase1.md` succeeds.
- The G5 issue comment URL (or the recorded `gh` error) is in `$PKG/progress.md`.
```
### src/superclaude/cli/reflect/contract.py:24-37

```python
# ---------------------------------------------------------------------------
# Routing constants
# ---------------------------------------------------------------------------

# FR-11 chain-critical subset: EXACT membership (NOT substring) so benign
# fail-open tokens (search_deps:lsp_unindexed, serena:onboarding-parse,
# serena:pre-v1.5-no-rename-propagation, get_current_config,
# neighbour-search:auggie_unavailable) do NOT over-HALT.
_DEGRADED_COMPONENTS_HALT_SET = frozenset(
    {"serena", "auggie", "env-aliases", "evidence-validator", "serena:context-excluded"}
)

# verification_ran == False is exempt (NOT degradation) for these skip reasons.
_VERIFICATION_SKIP_EXEMPTIONS = frozenset(
```
### src/superclaude/skills/sc-reflect-protocol/refs/reflection-rubric.md:120-130

```markdown
- `≤ 0.05` — near-zero ambiguity, eligible for the strict T1 STOP rule
- `≤ 0.10` — eligible for the §5.3 rule-2 path (WARN above 0.05)
- `> 0.20` — automatic ESCALATE (rule 5): "at one in five unmapped artifacts, a single reviewer cannot adjudicate without ensemble pressure"

**S_dev_density sub-terms (V3 Serena adoptions).** The threshold semantics above are unchanged — the following are **additive weighting inputs** (not threshold changes) layered onto the computed value (the numerator arithmetic lives in `coverage-mapping.md`):

- **FR-6 onboarding-status weight.** Keyed on `onboarding_status` (Wave 0.7): `not_bootstrapped` down-weights grounding confidence (the project has no bootstrapped memory to ground against, so unmapped artifacts are more likely genuine ambiguity). Per **FR-6.4**, `unknown` is **NO signal** — it does NOT down-weight (absence of an onboarding marker is not evidence of a missing bootstrap). `bootstrapped` is neutral.
- **FR-7 context-exclusion up-weight.** When the Wave-0 `get_current_config` probe finds the active Serena context excludes a chain-critical tool (e.g. `get_diagnostics_for_file`), S_dev_density is **up-weighted** (the grounding chain ran with a known capability gap, so its unmapped-artifact ratio under-states true ambiguity) and `"serena:context-excluded"` is appended to `degraded_components`. The `serena:context-excluded` degrade token is an **intentional new colon-namespaced convention** (flagged in this task's Open Questions) — do not normalize it back to a hyphenated slug.
- **FR-1 missing-implementor count.** For UC-1, abstract symbols whose implementors are unaccounted (the `missing_implementations` count from §6.1 step 3b `find_implementations`) feed the **unmapped-artifact numerator** — an interface added with no wired implementor is an unmapped requirement for coverage purposes. The numerator arithmetic is in `coverage-mapping.md`; the degenerate no-op (no eligible symbol of kind ∈ {Interface, AbstractMethod, Protocol, Trait, Class}) emits `implementation_coverage_pct: null` (C5) and contributes nothing to the numerator.
- **FR-4 verification-failure weight (lint/type channel).** Keyed on `verification_failures` from the §6.1 step 5.5 verification triangle, **restricted to the `ruff`/`mypy` lint/type-finding channel** (exit 1 on those tools — explicitly NOT the §10.4 Regression channel, which is `pytest` exit 1 → `regression_present`). A verified lint/type finding on a hunk the tasklist claimed clean raises structural ambiguity, so it **up-weights** S_dev_density. This is an additive weighting input, not a numerator/threshold change; it is `null`-safe — when verification did not run (`verification_ran: false`) it contributes nothing.
- **FR-RV3-MED.1 hierarchy-gap weight.** Keyed on `hierarchy_gaps_found` / `hierarchy_coverage_pct` from the §6.1 step 4.5 `type_hierarchy` retrieval: a type whose transitive subtype family is under-registered (low `hierarchy_coverage_pct` / nonzero `hierarchy_gaps_found`) raises structural ambiguity and **up-weights** S_dev_density. Additive weighting input, not a threshold change; `null`-safe — when the backend is unavailable / `--with-hierarchy` is unset (`type_hierarchy_invoked: false`, `hierarchy_coverage_pct: null`) it contributes nothing. The numerator/formula side lives in `coverage-mapping.md`.
```
### src/superclaude/cli/install_mcp.py:1300-1325

```python
            else:
                try:
                    indices = [int(value.strip()) for value in choice.split(",")]
                    names = list(MCP_SERVERS)
                    if not indices or any(
                        index < 1 or index > len(names) for index in indices
                    ):
                        return False, "Invalid selection; no changes made."
                    selected = list(
                        dict.fromkeys(names[index - 1] for index in indices)
                    )
                except ValueError:
                    return False, "Invalid selection; no changes made."
    unknown = [
        name
        for name in selected
        if name != "airis-mcp-gateway" and name not in MCP_SERVERS
    ]
    if unknown:
        return False, "Unknown MCP server selection: " + ", ".join(unknown)
    if uninstall and selected != [codebase_memory.BINARY_NAME]:
        return (
            False,
            "Uninstall accepts only --servers codebase-memory-mcp, not mixed or other servers.",
        )
    if codebase_memory.BINARY_NAME in selected:
```
### src/superclaude/cli/main.py:245-280

```python

    # Step 7: Shared user setup: rules (never auto-loaded), output styles,
    # settings defaults for keys the user has not set, and Orca's skills.
    click.echo("📦 Installing rules, output styles, settings defaults, Orca skills...")
    click.echo()

    setup_success, setup_message = install_user_setup(force=force)
    click.echo(setup_message)

    click.echo("\nInstalling Codebase Memory MCP (required user-level phase)...")
    native_success, native_message = install_codebase_memory_mcp(scope="user")
    click.echo(native_message)
    if not native_success:
        click.echo(
            "Required Codebase Memory phase incomplete. Existing framework files were kept; "
            "retry 'superclaude install' after addressing the reported stage.",
            err=True,
        )

    if (
        not core_success
        or not cmd_success
        or not agent_success
        or not skill_success
        or not cc_success
        or not hooks_success
        or not templates_success
        or not setup_success
        or not native_success
    ):
        sys.exit(1)


@main.command()
@click.option(
    "--servers",
```
### .dev/tasks/to-do/TASK-WF-phase1RemovalSpe-20261029-185100/source.md:606-660

````markdown
### 8.0 Shared definitions (created in T0, used by later tasks)

`$PKG` is the task package folder that `/sc:workflow` prints (`.dev/tasks/to-do/<id>/`). T0 writes these two helper files there:

`$PKG/artifacts/acceptance-search.sh` (prints every residual hit that is not allowlisted in section 2.4; exit 1 if any):

```bash
#!/usr/bin/env bash
# usage: acceptance-search.sh cbm|serena|all [paths...]   (default paths: .)
set -u -o pipefail
cd "$(git rev-parse --show-toplevel)"
which=$1; shift; paths=("${@:-.}")
EX=(--no-ignore --hidden -g '!.git' -g '!.dev/**' -g '!.claude/**' -g '!.specstory/**' -g '!.venv/**')
CBM='codebase-memory|codebase_memory|CodebaseMemory|Codebase Memory|cbm|CBM_|DeusData|search_graph|trace_path|get_code_snippet|query_graph|index_repository|get_architecture|detect_changes|search_code|list_projects|\.superclaude-codebase-memory'
SER='serena|mcp__serena|\.serena|MCP_Serena|find_symbol|find_referencing_symbols|get_symbols_overview|replace_symbol_body|insert_after_symbol|insert_before_symbol|write_memory|read_memory|list_memories|edit_memory|delete_memory|rename_memory|activate_project|check_onboarding_performed|initial_instructions|\bsummarize_changes\b|get_current_config|\bfind_declaration\b|find_implementations|rename_symbol|safe_delete_symbol|think_about_|search_for_pattern|get_diagnostics_for_file|\btype_hierarchy\b|execute_shell_command|prepare_for_new_conversation|--onboard\b'
ALLOW='^(\./)?(CHANGELOG\.md|POST-REFLECT-TASK\.md|docs/memory/patterns_learned\.jsonl|docs/memory/pm_context\.md|src/superclaude/skills/ccsession-tag/install\.sh|tests/skills/test_implement_severity_replay\.py|tests/troubleshoot/fixtures/regression/sysbox-20260918/Fable-D3/REPORT\.md|src/superclaude/cli/install_retired_mcp\.py|tests/cli/test_install_retired_mcp\.py):|^(\./)?\.gitignore:[0-9]+:\.serena/$|^(\./)?src/superclaude/skills/sc-cleanup-audit-protocol/SKILL\.md:[0-9]+:.*\.serena/|^(\./)?(src/superclaude/commands/load\.md|plugins/superclaude/commands/load\.md|commands/sc-load\.md):[0-9]+:.*\.serena/memories|^(\./)?tests/cli/test_install_mcp_registry\.py:[0-9]+:\s*"(serena|codebase-memory-mcp)",'
hits=$( { [ "$which" != serena ] && rg -n -i "${EX[@]}" -e "$CBM" "${paths[@]}"; [ "$which" != cbm ] && rg -n -i "${EX[@]}" -e "$SER" "${paths[@]}"; } | rg -v -e "$ALLOW" | sort -u )
[ -z "$hits" ] && { echo "ACCEPTANCE_SEARCH_OK $which"; exit 0; }
printf '%s\n' "$hits"; echo "ACCEPTANCE_SEARCH_FAIL $which $(printf '%s\n' "$hits" | wc -l)"; exit 1
```

`$PKG/artifacts/check_rosters.py` (rule 4.3 #2: every `mcp__<server>__<tool>` a primitive body names must be in its own `tools:` / `allowed-tools:` line; prints violations):

```python
import pathlib, re, sys
bad = []
for root in ("src/superclaude", "plugins/superclaude", "commands", "agents"):
    for p in sorted(pathlib.Path(root).rglob("*.md")):
        t = p.read_text(errors="ignore")
        m = re.match(r"---\n(.*?)\n---\n", t, re.S)
        line = m and re.search(r"^(?:tools|allowed-tools):\s*(.*)$", m.group(1), re.M)
        if not line:
            continue
        roster = set(re.findall(r"mcp__[\w-]+__[\w-]+", line.group(1)))
        named = set(re.findall(r"mcp__[\w-]+__[\w-]+", t[m.end():]))
        bad += [f"{p}: {n}" for n in sorted(named - roster)]
print("\n".join(bad))
sys.exit(1 if bad else 0)
```

Run it as `uv run --no-project python -I $PKG/artifacts/check_rosters.py`. Violations that already exist at baseline for other servers are out of scope; the check is "no line that is not in the T0 output, and no `serena` line".

Pytest runs use `-p no:cacheprovider`; full-suite runs set `T02_15_PERF_REPORT=/tmp/p1-perf.json` (section 10). After every test run: `git status --short` lists only intended files.

### G0: baseline

**T0. Record the baseline**
- Files: `$PKG/artifacts/acceptance-search.sh`, `$PKG/artifacts/check_rosters.py`, `$PKG/artifacts/baseline/*` (no source change).
- Change: `make sync-dev` (the audit tests need the `.claude/` mirror, `inventory/codebase-memory.md` 4.0); write the two helpers from 8.0; record baselines:
  - `uv run pytest tests/cli/test_install_codebase_memory.py tests/cli/test_install_mcp_registry.py tests/cli/test_install_mcp_tavily.py tests/cli/test_update_command.py tests/docs/test_tavily_doc_alignment.py -q -p no:cacheprovider | tee $PKG/artifacts/baseline/cbm.txt` (W1 observed 258 passed, 1 skipped)
  - `uv run pytest tests/cli/reflect tests/troubleshoot tests/sc-roadmap tests/core tests/commands tests/skills tests/recommend tests/hooks tests/unit/test_cli_install.py tests/cli/test_install_hooks.py tests/cli/test_update_script.py -q -p no:cacheprovider | tee $PKG/artifacts/baseline/targeted.txt`
  - `T02_15_PERF_REPORT=/tmp/p1-perf.json uv run pytest -q -p no:cacheprovider --tb=line | tee $PKG/artifacts/baseline/full.txt` (W1 saw 27 failed and 16 errors before `make sync-dev`; whatever this run shows is the baseline)
  - `bash $PKG/artifacts/acceptance-search.sh all > $PKG/artifacts/baseline/search.txt; uv run --no-project python -I $PKG/artifacts/check_rosters.py > $PKG/artifacts/baseline/rosters.txt` (both are expected to report hits now)
- Acceptance: `test -s $PKG/artifacts/baseline/full.txt && test -s $PKG/artifacts/baseline/targeted.txt && grep -q 'ACCEPTANCE_SEARCH_FAIL' $PKG/artifacts/baseline/search.txt && test -z "$(git status --short -- . ':!.dev')"`
- Commit: `chore(tasks): record the Phase 1 removal baseline (#323)`
````

## Coverage slice

| Plan task | Spec task | Spec rows owned |
|---|---|---|
| Task 1 | T0 | 8.0 helpers |
| Task 2 | T1 | C4 |
| Task 3 | T2 | C3,C4,C7 |
| Task 4 | T3 | §3 |
| Task 5 | T4 | C2,C5,C6 |
| Task 6 | T5 | C1 |
| Task 7 | T6 | S42-S44,S58-S86 |
| Task 8 | T7 | P21,P55,D1,D2,S37,S38,S40,S57,S87 |
| Task 9 | T8 | S32-S36,S41,S46-S51,S88,S100 |
| Task 10 | T9 | 33 T9 rows |
| Task 11 | T10a | P1,P4,P5,P8,P11,P13,P14,P17,P23,P27,P39,P40,P47,P57,P73 |
| Task 12 | T10b | memory parts P6,P15,P43,P50,P96,P77,P91; P68-P71,P82,P85,P24,P52,S89,S90,S4 |
| Task 13 | T11a | reflect tool parts; P78-P81,P83,P84,P86,P87,P28,P29,D3-D5 |
| Task 14 | T11b | P49,P93-P95,P31,S99 |
| Task 15 | T11c | remaining T11 rows, P51:112 |
| Task 16 | T12 | C8-C12,S7,S9-S13,S16,S17,S20-S31 |
| Task 17 | T13 | S1-S5 |
| Task 18 | T14 | DoD-1..6 |
| Task 19 | T15 | §6 |

## Return shape

Return ONLY a YAML document:

```yaml
reviewer: <persona>
verdict: refactor | accept      # refactor when any defect must be fixed before execution
findings:
  - id: R<N>-F<k>
    severity: CRITICAL | IMPORTANT | MINOR
    class: drift | regression | necessary | authorized | coverage-gap | plan-defect
    claim: <one sentence>
    evidence: ["<path>:<line>", ...]      # every claim cites real lines you Read
    grounded: true | false                # false = [INFERRED]
    fix: <concrete edit to the plan, naming the Task number>
self_confidence: <0.00-1.00>
self_audit: <if zero findings: what you checked and why no defect exists>
```

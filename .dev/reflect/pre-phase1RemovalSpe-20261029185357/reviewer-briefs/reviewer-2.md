# Reviewer brief 2 (persona: qa)
Role: read-only Tier-2 reviewer for an `/sc:reflect --mode pre` (UC-1) audit of a proposed implementation plan against its driving spec. Audit only the supplied hunks and what you can Read/Grep/Glob from the repo root `/home/coder/workspaces/worktrees/IronClaude/feat-codememory-codegraph-init`. Do not run anything. Return findings as YAML (shape at the end).

Lens: coverage and acceptance. Audit the coverage matrix AGAINST the spec body in your grounding hunks; surface any requirement-bearing span absent from the plan (parsed or inferred) as a finding. Also check that every plan task's acceptance criteria are observable and would actually prove the spec requirement.

## T1 card excerpt

## Coverage / acceptance section (qa lens)

- Pass 1 (regex `R-|REQ-|SPEC-|T-NNN`, fenced code skipped): 0 parsed IDs. Pass 2 (requirements-analyst): 340 quote-pinned rows, `artifacts/inferred-requirements.yaml`. `coverage_pct: null` (no parsed rows), `coverage_degraded: parsed-sparse` (340 inferred > 0 parsed).
- Deterministic containment match (`artifacts/match.py`, threshold 0.6): 241 of 340 matched, `coverage_pct_union: 0.7088`, 99 unmapped (`artifacts/coverage-matrix.yaml`).
- Triage of the 99 (`artifacts/unmapped-triage.yaml`, script `artifacts/triage.py`): 41 are named by row ID in the plan (for example `C1`-`C12`, `P68-P71`), 55 sit in a source section the plan task cites as "Implements ./source.md §N" (the plan points the executor at `./source.md` instead of copying line ranges, which lowers lexical overlap), 3 have no reference: INF-114 (goal paragraph, `source.md:261`, restated by the plan's `Goal:` line), INF-115 ("Historical `.dev/` artifacts stay untouched.", `source.md:261`) and INF-125 (§2.3 leftovers IronClaude does not own, `source.md:279`).

### F-2 Two scope limits are missing from the plan's Constraints (MINOR)
- Evidence: INF-115 (`source.md:261`) and INF-125 (`source.md:279-291`) are referenced by no task and no Constraint; the plan's Constraints forbid deleting user data and editing other repositories but never say "do not edit historical `.dev/` artifacts" or "do not remove the §2.3 leftovers (Coder image binary, `serena-agent` uv tool, bundle markers, upstream companions)".
- Class: coverage gap (scope boundary).
- Fix: add one Constraint bullet naming both limits with a pointer to `./source.md` §2.1 and §2.3.


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
### .dev/tasks/to-do/TASK-WF-phase1RemovalSpe-20261029-185100/source.md:1-4

```markdown
# Phase 1 spec: complete removal of codebase-memory-mcp and Serena (issue #323)

Status: COMPLETE (task P1, 2026-10-29). Planning artifact only: no source, test, doc or environment change was made. Input to a later `/sc:workflow` run. Base commit `55d40308` on `ironbelly/feat-codememory-codegraph-init`. Revised by task F1 (2026-10-29) to apply the task-R review (`.dev/codegraph-migration/review/review.md`); see "Review resolution" at the end.

```
### .dev/tasks/to-do/TASK-WF-phase1RemovalSpe-20261029-185100/source.md:5-256

```markdown
## 1. Preflight: file lists

Two lists, as the user required: every file outside `.dev/` associated with codebase-memory (1.1) and every file outside `.dev/` associated with Serena (1.2). Rows come from the wave-1 inventories (`.dev/codegraph-migration/inventory/codebase-memory.md` section 1.1, `.dev/codegraph-migration/inventory/serena.md` sections 1 and 2) and were re-checked against a fresh run of each inventory's own search on 2026-10-29 at HEAD `55d40308`. The "Task" column points at the task in section 8 that performs the action. `.claude/` content other than `settings.json` is a `make sync-dev` mirror and is not listed (regenerated by T14); `.claude/settings.json` has no hit for either server.

### 1.0 Re-run result and delta

| Search | Command (from the inventory) | Inventory result | Re-run result | Delta |
|---|---|---|---|---|
| codebase-memory, W1 1.0 | `PAT='codebase-memory\|codebase_memory\|CodebaseMemory\|Codebase Memory\|cbm\|CBM_\|DeusData\|search_graph\|trace_path\|get_code_snippet\|query_graph\|index_repository\|get_architecture\|detect_changes\|search_code\|list_projects\|\.superclaude-codebase-memory'; rg -n -i --hidden --no-ignore -g '!.dev/**' -g '!.claude/**' -g '!.git/**' -g '!.venv/**' -g '!.specstory/**' -e "$PAT" . \| wc -l` | 300 hits in 12 files | 300 hits in 12 files, same per-file counts | none |
| Serena word, W2 0.1 A | `rg -il serena "${EX[@]}" . \| wc -l` with `EX=(--no-ignore --hidden -g '!.git' -g '!.dev/**' -g '!.claude/**' -g '!.specstory/**' -g '!.venv/**')` | 168 files | 168 files | none |
| Serena required list, W2 0.1 B | `rg -l "${EX[@]}" -e "$PAT" .` (PAT in `serena.md` 0.1) | 193 files, 981 lines | 193 files, 981 lines | none |
| Serena indirect, W2 0.1 C | `comm -13` of B against `P2` (`serena.md` 0.1) | 3 files | the same 3 files (`src/` and `plugins/` `core/RULES.md`, `sc-reflect-protocol/refs/coverage-mapping.md`) | none |
| Tracked `.serena/`, W2 0.1 D | `git ls-files .serena` | 4 files | 4 files | none |
| Serena argument name (W6 finding, not in W2's patterns) | `rg -n 'relative_path' src/superclaude/hooks plugins/superclaude/hooks tests` | not in W2 table | `src/superclaude/hooks/scripts/freshness-pre-edit.sh:25-36` and `plugins/superclaude/hooks/scripts/freshness-pre-edit.sh:25-36` read `.tool_input.relative_path`, the argument name of Serena's edit tools (W6 `primitive-usage.md` section 1) | **+2 rows (D1, D2 in 1.2)** |
| Serena-only tool names missing from W2's `P2` (`execute_shell_command`, `type_hierarchy`, `prepare_for_new_conversation`, `--onboard`) | `rg -l "${EX[@]}" 'execute_shell_command\|type_hierarchy\|prepare_for_new_conversation' .` and `rg -l "${EX[@]}" -e '--onboard\b' .` | n/a | 16 + 5 files; all already rows except three reflect tests: `tests/cli/reflect/test_marker_suppression.py:101-130` (extracts the SKILL.md heading "### 6.1.1 `execute_shell_command` safety envelope"), `tests/cli/reflect/test_reviewer_readonly_tools.py:7,31` and `tests/cli/reflect/test_reviewer_finding_parity.py:33` (read-only denylist sets that contain `execute_shell_command`) | **+3 rows (D3-D5 in 1.2)** |
| `relative_path` elsewhere | `rg -l "${EX[@]}" 'relative_path' .` | n/a | 8 files; the other 6 (`sc-reflect-protocol/SKILL.md:218` pseudo-code, 5 `tests/cli/eval/` files) use the phrase generically, not Serena's argument | none |

Every path in the fresh result sets is a row below, and every row's path is in the fresh result sets (checked by script: 0 missing, 0 extra). `.specstory/` (untracked session logs) and `.venv/` are excluded, as in the inventories.

### 1.1 codebase-memory: every file outside `.dev/` (12 files with hits, plus 3 checked no-hit rows)

Row details, block-level line ranges and the test split are in `inventory/codebase-memory.md` sections 1.1 and 1.4; this spec changes no action except where section 3 keeps the generic registration helpers (`read_user_mcp_entry`, `_run_registration_command`, and a name-parameterised `_cleanup_user_native_registration`) that W1 row C2 would delete.

| # | Path | Lines to act on | Removal action | Task |
|---|---|---|---|---|
| C1 | `src/superclaude/cli/install_codebase_memory.py` | 1-759 (whole file; hits 23,25,82,86,223,265,323,337,611,673) | **delete file** | T5 |
| C2 | `src/superclaude/cli/install_mcp.py` | 21; 101-108; 486-503; 571-583; 714-754; 757-813; 815-913; 916-948; 951-1007; 1025-1028; 1243-1343 (parts) | **delete blocks**, keep the file (other servers use it); section 3 keeps the generic registration helpers | T3 (helpers), T4, Serena blocks: T8 |
| C3 | `src/superclaude/cli/main.py` | 38; 44; 50-52; 66; 78-83; 161-186; 254-262; 264-275; 292; 299-309; 310; 313; 319-321; 327; 334-340 | **delete blocks + rewrite text**; T3 adds the retire-step call | T2, T3, T4 |
| C4 | `tests/cli/test_install_codebase_memory.py` | 1-1633 (hits: Appendix A) | **delete file, but port 16 generic tests first** (1.4) | T1, T2, T4, T5 |
| C5 | `tests/cli/test_install_mcp_registry.py` | 192-240 (hits 192-194,196,202,209,216,223,238) | **delete 3 tests**: `test_codebase_memory_native_registry_contract` (192), `test_codebase_memory_dispatch_uses_shared_install` (202), `test_selected_native_prerequisites_do_not_probe_other_runtimes` (222). Keep the other 9 tests | T4 |
| C6 | `tests/cli/test_install_mcp_tavily.py` | 382-1050 (hits 384...1050, Appendix A) | **delete 382-end**: fixtures `native_registration` (382), `native_removal` (832), helpers `_native_entry` (472), `_seed_native_entry` (480) and 54 native tests. **Keep lines 1-375** (16 Tavily tests, 15 run + 1 live smoke skipped without `TAVILY_API_KEY`) | T4 |
| C7 | `tests/cli/test_update_command.py` | 28,33,48,50,57,86,138,267,277,296,300,323,332,390,410,421,424 plus unmarked native lines 32-76 | **rewrite**: autouse fixture `native_phase_guard` (31-76), `_NATIVE_INSTALLER` (28), `_stub_installers` branch (82-91), expected call list (138). **Delete 17 tests** (5 test functions: `test_install_native_failure_is_mandatory_and_preserves_framework_work` 254, `test_install_list_reports_native_and_exact_user_status_without_repair` 293, `test_install_list_reports_unsupported_native_without_probe` 329, `test_repeated_install_delegates_shared_noop_repair_external_policy` 386, `test_update_never_restores_native_but_later_install_calls_shared_phase` 407). **Rewrite** `test_install_force_target_do_not_redirect_or_force_native` (345) to drop the native assertions. 10 tests remain | T2 |
| C8 | `docs/user-guide/mcp-installation.md` | 5-26; 36-37; 43; 46; 56; 67; 73; 121; 124; 183-184; 206-242; 306; 309-324 | **delete sections** `## Default Framework Setup...` (5-26), `## Safe Codebase Memory Removal` (206-234), `### Codebase Memory Setup or Registration Failure` (237-242), `## Release Gate...` (309-324); **rewrite** 36-37, 43, 46, 56, 67, 73, 121, 124, 183-184, 306 | T12 |
| C9 | `docs/reference/mcp-server-guide.md` | 13; 21-22; 25; 31-55; 650 | **delete section** `## Codebase Memory Native Lifecycle` (31-55); **rewrite** 13, 21-22, 25, 650 | T12 |
| C10 | `docs/mcp/mcp-optional-design.md` | 9; 11; 13; 316; 321; 399; 420 | **rewrite text**: drop the cbm default-provisioning paragraph (9-13) and the cbm wording in the examples (316, 321, 399, 420). The page's thesis (MCP use is optional, native fallbacks) stays valid | T12 |
| C11 | `README.md` | 64; 75 | **rewrite text**: remove "required user-level Codebase Memory MCP setup" (64) and the `# framework assets + required user Codebase Memory setup (Linux)` comment (75) | T12 |
| C12 | `.github/workflows/test.yml` | 133-134; 155 | **rewrite comments only**: the `permissions` comment (133-134, "runs the unpinned upstream Codebase Memory installer") and the step comment (155, "The required Codebase Memory phase ... needs the Claude CLI") stop naming codebase-memory, e.g. "`superclaude install` registers and retires user-scope MCP servers through the Claude CLI". **Keep** the `Install Claude CLI` step (156-159) and `permissions: contents: read`: Phase 2's required codegraph phase needs `claude --version` in this job (Phase 2 spec F12, D9), and Phases 1 and 2 merge as one unit (section 2.2), so deleting it here only for Phase 2 to restore it is churn (review finding X-15) | T12 |
| C13 | `.specstory/history/2026-10-29_15-08-38Z.md` | 365 hits | **keep**, reason: untracked, globally gitignored (`/home/coder/.config/git/ignore:1`), not repo content; it records this conversation | none (keep) |
| C14 | `update.sh` | 8 (no hit) | **keep unchanged in phase 1**: line 8 `superclaude install --force` stops provisioning cbm once rows 1-3 land. Phase 2 will add the codegraph step | none (keep) |
| C15 | `.mcp.json` (tracked), `Makefile`, `pyproject.toml`, `plugins/` | no hits | **keep** | none (keep) |

### 1.2 Serena: every file outside `.dev/` (198 inventory rows plus 5 delta rows)

Rows `S1-S100` are non-primitive files (inventory section 1), `P1-P98` are primitives including the `plugins/superclaude/` and root `commands/`, `agents/` copies (inventory section 2). The removal action is the inventory's; sections 4 and 5 of this spec decide the exact rewrite for memory and load-bearing rows. 28 rows are "none (keep)": 19 `onboarding` false positives plus the history and label rows recorded in `serena.md` decisions D5 and D6; keep rows `CHANGELOG.md` (T12 adds a new entry) and `core/RULES.md` (stays because `/sc:save` and `/sc:load` stay, section 5). The Task column's `T10` and `T11` are split into T10a-T10b and T11a-T11c (review finding X-12); section 8 lists which rows each piece owns, and that list wins.

| # | Path | Lines | Removal action (from inventory; overrides in this spec are noted in sections 4-5) | Task |
|---|---|---|---|---|
| S1 | `.gitignore` | 113 | keep until `.serena/` is deleted everywhere; then delete line (decision D4) | T13 |
| S2 | `.serena/.gitignore` | path only | `git rm` the file | T13 |
| S3 | `.serena/memories/memory_maintenance.md` | 32-33 | `git rm` the file | T13 |
| S4 | `.serena/memories/reflect/deviation-patterns-IronClaude.md` | path only | move to `docs/memory/reflect/` (section 5 rule M5, `git mv`), then delete `.serena/`; do not lose the content | T10b (move), T13 |
| S5 | `.serena/project.yml` | 1,10,14,26,38,48,53,56,58,63-64,68,73,91-92,101,114-115,123,151,162 | `git rm` the file | T13 |
| S6 | `CHANGELOG.md` | 264 | keep: release history is not rewritten; add a new entry for the removal | none (keep) |
| S7 | `CLAUDE.md` | 377 | delete line 377 | T12 |
| S8 | `POST-REFLECT-TASK.md` | 70,202,206,241,320,380,403 | keep with reason: historical task record (flag to owner; could be moved under .dev/ later) | none (keep) |
| S9 | `README.md` | 38,219 | delete both mentions | T12 |
| S10 | `SECURITY.md` | 328 | delete line 328 | T12 |
| S11 | `docs/analysis-sc-tasklist.md` | 317 | rewrite after sc-task-protocol STRICT decision | T12 |
| S12 | `docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md` | 275,348,459,530,558,796,876,899,909,1500,1567 | rewrite examples to drop serena; delete 459 wording | T12 |
| S13 | `docs/developer-guide/technical-architecture.md` | 100 | delete the word | T12 |
| S14 | `docs/generated/contributor-knowledge-base/contributor-workflow.md` | 157 | keep: onboarding is generic English/template text, not Serena | none (keep) |
| S15 | `docs/generated/contributor-knowledge-base/repository-overview.md` | 69 | keep: onboarding is generic English/template text, not Serena | none (keep) |
| S16 | `docs/mcp/mcp-integration-policy.md` | 77,80,118-119,200,220,261,283,299,309,312,335,348,387,403-405,421,432,452,454,476 | delete Serena sections; rewrite memory rules per section 3 | T12 |
| S17 | `docs/mcp/mcp-optional-design.md` | 35,97,132,142,153,157,209,227,232,326,354-355,369 | delete Serena examples | T12 |
| S18 | `docs/memory/patterns_learned.jsonl` | 1 | keep: historical learned-pattern log (and it supports memory decision A) | none (keep) |
| S19 | `docs/memory/pm_context.md` | 77 | keep unchanged: line 77 ("Self-Evaluation Checklists: Replace Serena MCP `think_about_*` functions") records why the file-based design exists, so it is history; allowlisted in 2.4 (review finding X-24) | none (keep) |
| S20 | `docs/reference/mcp-server-guide.md` | 3,17,23,370,372,379,388-390,392,394,539,614,623 | delete Serena sections | T12 |
| S21 | `docs/troubleshooting/serena-installation.md` | 1,5,10,15,22,25,28,34,47-48,51,76,85,90-91,119,123-124,143,145,153 | delete file (and its links) | T12 |
| S22 | `docs/user-guide/agents.md` | 374,686 | rewrite per section 3 | T12 |
| S23 | `docs/user-guide/brainstorm.md` | 17,146 | delete Serena mentions | T12 |
| S24 | `docs/user-guide/commands.md` | 18,30,112-113,159,187,201,216,230,272,278,286,298,301,323,357,371,419,450,492,500,573,655,766,769,800,1327,1365,1372,1374,1377,1391,1397,1414,1416-1417,1419,1430,1436-1437,1443,1446-1447,1456-1457,1463 | delete Serena rows and the comparison section; rewrite /sc:save//sc:load text per section 3 | T12 |
| S25 | `docs/user-guide/flags.md` | 25,146,201,219 | delete the flag rows | T12 |
| S26 | `docs/user-guide/freshness-hooks.md` | 18 | delete the two tool names | T12 |
| S27 | `docs/user-guide/mcp-installation.md` | 43,60,83,123,304 | delete serena rows/examples and link | T12 |
| S28 | `docs/user-guide/mcp-servers.md` | 19,34,85,97,154,211,213,245,299,307,309-311,318,325-326,347 | delete Serena section and rows | T12 |
| S29 | `docs/user-guide/memory-system.md` | 18 | reword per section 3 | T12 |
| S30 | `docs/user-guide/modes.md` | 213,264 | rewrite per section 3 | T12 |
| S31 | `docs/user-guide/session-management.md` | 3,10,15,35,42,65,113,130,163,169,179,216,231,255,320 | rewrite per section 3 (or delete if Option C) | T12 |
| S32 | `plugins/superclaude/mcp/MCP_Morphllm.md` | 15,23,32 | delete the Serena lines/pairings | T8 |
| S33 | `plugins/superclaude/mcp/MCP_Serena.md` | 1,24-25,30-33 | delete file | T8 |
| S34 | `plugins/superclaude/mcp/MCP_Tavily.md` | 29,106 | delete the Serena lines/pairings | T8 |
| S35 | `plugins/superclaude/mcp/configs/serena-docker.json` | 2,11 | delete file | T8 |
| S36 | `plugins/superclaude/mcp/configs/serena.json` | 2,6-7 | delete file | T8 |
| S37 | `src/superclaude/cli/eval/coverage.py` | 195 | reword example (no behavior) | T7 |
| S38 | `src/superclaude/cli/eval/suites/README.md` | 170 | rewrite with E8 removal | T7 |
| S39 | `src/superclaude/cli/eval/suites/adversarial_merge_consistency.yaml` | 374 | keep: onboarding is generic English/template text, not Serena | none (keep) |
| S40 | `src/superclaude/cli/eval/suites/real.yaml` | 40,380,384,406-407,475,479,499,502,505-506,567,569,575-576,580-582,584,589-590,593,596,598,609,611,614-615,621-623,638,642,670-671,684,721 | delete capability row 40 and eval E8; reword E6/E7 comments | T7 |
| S41 | `src/superclaude/cli/install_mcp.py` | 55-56,59,561,568,570 | delete both blocks (see section 4) | T8 |
| S42 | `src/superclaude/cli/reflect/config.py` | 162,199 | reword comment (behavior unchanged) | T6 |
| S43 | `src/superclaude/cli/reflect/contract.py` | 29-30,33 | remove two members + comment; unknown tokens then neither halt nor degrade (see section 4) | T6 |
| S44 | `src/superclaude/cli/reflect/ensemble.py` | 824 | delete key AND the 25 test fixtures that carry it in the same change (contract is tolerant of unknown fields: fixture tolerant_unknown_field.yaml) | T6 |
| S45 | `src/superclaude/examples/tdd_template.md` | 852 | keep: onboarding is generic English/template text, not Serena | none (keep) |
| S46 | `src/superclaude/mcp/MCP_Auggie.md` | 16,18,23,37 | delete the Serena lines/pairings | T8 |
| S47 | `src/superclaude/mcp/MCP_Morphllm.md` | 15,23,31 | delete the Serena lines/pairings | T8 |
| S48 | `src/superclaude/mcp/MCP_Serena.md` | 1,24,29-32 | delete file | T8 |
| S49 | `src/superclaude/mcp/MCP_Tavily.md` | 31,152 | delete the Serena lines/pairings | T8 |
| S50 | `src/superclaude/mcp/configs/serena-docker.json` | 2,11 | delete file | T8 |
| S51 | `src/superclaude/mcp/configs/serena.json` | 2,6-7 | delete file | T8 |
| S52 | `src/superclaude/templates/documents/GFxAI_Master_Documentation_Template.md` | 143,345 | keep: onboarding is generic English/template text, not Serena | none (keep) |
| S53 | `src/superclaude/templates/documents/prd_template.md` | 681,691 | keep: onboarding is generic English/template text, not Serena | none (keep) |
| S54 | `src/superclaude/templates/documents/readme_template.md` | 28 | keep: onboarding is generic English/template text, not Serena | none (keep) |
| S55 | `src/superclaude/templates/documents/tdd_template.md` | 815 | keep: onboarding is generic English/template text, not Serena | none (keep) |
| S56 | `src/superclaude/templates/documents/technical_reference_template.md` | 120 | keep: onboarding is generic English/template text, not Serena | none (keep) |
| S57 | `tests/cli/eval/test_coverage_gate.py` | 127 | replace string with another MCP tool name (e.g. mcp__context7__resolve); test stays | T7 |
| S58 | `tests/cli/reflect/fixtures/autofixable_drift.yaml` | 26 | delete the `serena_summary_corroboration` line | T6 |
| S59 | `tests/cli/reflect/fixtures/autofixable_drift_both.yaml` | 26 | delete the `serena_summary_corroboration` line | T6 |
| S60 | `tests/cli/reflect/fixtures/autofixable_drift_no_path.yaml` | 26 | delete the `serena_summary_corroboration` line | T6 |
| S61 | `tests/cli/reflect/fixtures/autofixable_drift_plan.yaml` | 26 | delete the `serena_summary_corroboration` line | T6 |
| S62 | `tests/cli/reflect/fixtures/blocked_unknown_major.yaml` | 26 | delete the `serena_summary_corroboration` line | T6 |
| S63 | `tests/cli/reflect/fixtures/blocked_with_drift.yaml` | 26 | delete the `serena_summary_corroboration` line | T6 |
| S64 | `tests/cli/reflect/fixtures/degraded_reviewer_shortfall.yaml` | 35 | delete the `serena_summary_corroboration` line | T6 |
| S65 | `tests/cli/reflect/fixtures/degraded_serena.yaml` | 26,28 | delete file (after test_degraded_serena and test_runner_e2e are repointed) | T6 |
| S66 | `tests/cli/reflect/fixtures/degraded_single_vendor.yaml` | 26 | delete the `serena_summary_corroboration` line | T6 |
| S67 | `tests/cli/reflect/fixtures/degraded_tier1.yaml` | 28 | delete the `serena_summary_corroboration` line | T6 |
| S68 | `tests/cli/reflect/fixtures/degraded_with_drift.yaml` | 26,28 | delete the `serena_summary_corroboration` line; replace the `- serena` entry with another halt token (e.g. auggie) | T6 |
| S69 | `tests/cli/reflect/fixtures/halted_regression.yaml` | 26 | delete the `serena_summary_corroboration` line | T6 |
| S70 | `tests/cli/reflect/fixtures/human_required_needs_decision.yaml` | 26 | delete the `serena_summary_corroboration` line | T6 |
| S71 | `tests/cli/reflect/fixtures/pass.yaml` | 26 | delete the `serena_summary_corroboration` line | T6 |
| S72 | `tests/cli/reflect/fixtures/pass_no_t2_fallback.yaml` | 26 | delete the `serena_summary_corroboration` line | T6 |
| S73 | `tests/cli/reflect/fixtures/pass_with_t2_fallback.yaml` | 26 | delete the `serena_summary_corroboration` line | T6 |
| S74 | `tests/cli/reflect/fixtures/postfix_pass.yaml` | 26 | delete the `serena_summary_corroboration` line | T6 |
| S75 | `tests/cli/reflect/fixtures/reachability_1_7_0_gate_ran.yaml` | 27 | delete the `serena_summary_corroboration` line | T6 |
| S76 | `tests/cli/reflect/fixtures/reachability_proxy_oracle_unproven.yaml` | 30 | delete the `serena_summary_corroboration` line | T6 |
| S77 | `tests/cli/reflect/fixtures/reachability_semantic_fallback_advisory.yaml` | 27 | delete the `serena_summary_corroboration` line | T6 |
| S78 | `tests/cli/reflect/fixtures/reachability_skip_no_reachability.yaml` | 27 | delete the `serena_summary_corroboration` line | T6 |
| S79 | `tests/cli/reflect/fixtures/reachability_skip_spec_absent.yaml` | 27 | delete the `serena_summary_corroboration` line | T6 |
| S80 | `tests/cli/reflect/fixtures/reachability_unwired_surface_regression.yaml` | 27 | delete the `serena_summary_corroboration` line | T6 |
| S81 | `tests/cli/reflect/fixtures/tolerant_unknown_field.yaml` | 26 | delete the `serena_summary_corroboration` line | T6 |
| S82 | `tests/cli/reflect/fixtures/vacuous_no_verify.yaml` | 34 | delete the `serena_summary_corroboration` line | T6 |
| S83 | `tests/cli/reflect/test_ensemble_unit.py` | 345 | reword docstring | T6 |
| S84 | `tests/cli/reflect/test_runner_e2e.py` | 71 | point at another degraded fixture (e.g. degraded_tier1.yaml) -- see section 4 | T6 |
| S85 | `tests/cli/reflect/test_verdict_mapping.py` | 93-94,96,193-194,196,245 | delete 2 tests; edit token list | T6 |
| S86 | `tests/cli/reflect/test_verify_denylist_git_mutations.py` | 11 | reword docstring | T6 |
| S87 | `tests/cli/test_install_hooks.py` | 684-687 | delete four asserts | T7 |
| S88 | `tests/cli/test_install_mcp_registry.py` | 13-14,45,47-48,61 | delete serena entries from both dicts (tests stay) | T8 |
| S89 | `tests/core/test_how_we_work_routing_table.py` | 1074 | rewrite assertion after HOW-WE-WORK wording decision | T10 |
| S90 | `tests/recommend/fixtures/routing_refresh_cases.json` | 576,584 | rewrite strings with HOW-WE-WORK wording | T10 |
| S91 | `tests/roadmap/fixtures/recurrence/spec_fidelity/phantom_id_high_severity_case.md` | 15,18,31 | keep: onboarding is generic English/template text, not Serena | none (keep) |
| S92 | `tests/sc-roadmap/compliance/test_mcp_circuit_breakers.py` | 33-35,77-79 | delete the 2 tests | T9 |
| S93 | `tests/sc-roadmap/integration/test_wave5_completion.py` | 69,74,77-78 | delete test_circuit_breaker_for_serena; reword 69-74 | T9 |
| S94 | `tests/skills/test_implement_severity_replay.py` | 192,326-327,330 | keep: unrelated label (not the MCP server) | none (keep) |
| S95 | `tests/troubleshoot/fixtures/regression/sysbox-20260918/Astra-A3/REPORT.md` | 37,39 | keep: onboarding is generic English/template text, not Serena | none (keep) |
| S96 | `tests/troubleshoot/fixtures/regression/sysbox-20260918/Astra-A3/diagnosability-tasklist.md` | 13-14 | keep: onboarding is generic English/template text, not Serena | none (keep) |
| S97 | `tests/troubleshoot/fixtures/regression/sysbox-20260918/Astra-A3/tier1-observation.md` | 27 | keep: onboarding is generic English/template text, not Serena | none (keep) |
| S98 | `tests/troubleshoot/fixtures/regression/sysbox-20260918/Fable-D3/REPORT.md` | 17,56 | keep: frozen fixture (historical evidence text) | none (keep) |
| S99 | `tests/troubleshoot/test_diagnostic_worker_contract.py` | 22-25,152 | edit TOOLS and mutant string together with troubleshoot-analyst.md | T11 |
| S100 | `tests/unit/test_cli_install.py` | 150,153,423,425 | delete the three names from both listings | T8 |
| P1 | `agents/sc-pm-agent.md` | 10,18,20,30-34,53,66,92,108,113,132,239,243-246,249-251,259-261 | rewrite lifecycle per section 3 (repo-local file memory) | T10 |
| P2 | `commands/sc-brainstorm.md` | 6,44,78,84 | delete `serena` from frontmatter and fallback wording | T11 |
| P3 | `commands/sc-help.md` | 43-45,75 | delete the rows | T9 |
| P4 | `commands/sc-load.md` | 3,6,24,31,37,43,58,86,92 | rewrite per memory decision (section 3); delete `serena` frontmatter | T10 |
| P5 | `commands/sc-pm.md` | 6,15,34,39-43,59,65,79,86-87,95,323,423-428,530,539 | rewrite memory lifecycle per section 3; delete `serena` frontmatter | T10 |
| P6 | `commands/sc-reflect.md` | 3,6,24,31-32,36,38,80,85 | rewrite tool table; delete `--onboard` Serena bootstrap rows; delete `serena` frontmatter | T10, T11 |
| P7 | `commands/sc-research.md` | 6,85 | delete both lines | T9 |
| P8 | `commands/sc-save.md` | 3,6,25,31,37,42,58,86,91 | rewrite per memory decision (section 3): keep command, swap Serena memory for repo-local files; delete `serena` frontmatter | T10 |
| P9 | `commands/sc-task.md` | 6,32,41 | delete `serena` from the `mcp-servers:` frontmatter list | T9 |
| P10 | `commands/sc-workflow.md` | 6,41,82 | delete `serena` from the `mcp-servers:` frontmatter list | T9 |
| P11 | `plugins/superclaude/agents/pm-agent.md` | 11,19,21,31-35,54,67,93,109,114,133,240,244-247,250-252,260-262 | rewrite lifecycle per section 3 (repo-local file memory) | T10 |
| P12 | `plugins/superclaude/commands/brainstorm.md` | 6,120 | delete `serena` from frontmatter | T9 |
| P13 | `plugins/superclaude/commands/load.md` | 3,6,27,35,42,49,66,98,105 | rewrite per memory decision (section 3); delete `serena` frontmatter | T10 |
| P14 | `plugins/superclaude/commands/pm.md` | 6,16,47 | rewrite memory lifecycle per section 3; delete `serena` frontmatter | T10 |
| P15 | `plugins/superclaude/commands/reflect.md` | 6,99,135,149,157-163,258 | rewrite tool table; delete `--onboard` Serena bootstrap rows; delete `serena` frontmatter | T10, T11 |
| P16 | `plugins/superclaude/commands/research.md` | 6,100 | delete both lines | T9 |
| P17 | `plugins/superclaude/commands/save.md` | 3,6,28,35,42,48,66,98,104 | rewrite per memory decision (section 3): keep command, swap Serena memory for repo-local files; delete `serena` frontmatter | T10 |
| P18 | `plugins/superclaude/commands/task.md` | 7 | delete `serena` from the `mcp-servers:` frontmatter list | T9 |
| P19 | `plugins/superclaude/core/RESEARCH_CONFIG.md` | 98,415 | delete both | T9 |
| P20 | `plugins/superclaude/core/RULES.md` | 49-50 | keep wording if the commands are kept (decision section 3); otherwise delete | none (keep) |
| P21 | `plugins/superclaude/hooks/hooks.json` | 37 | delete the four `mcp__serena__*` alternatives from the matcher regex | T7 |
| P22 | `plugins/superclaude/modes/MODE_Orchestration.md` | 25 | delete the row (or replace with codegraph in P3) | T11 |
| P23 | `plugins/superclaude/modes/MODE_Task_Management.md` | 15-18,25-26,33,36,43,49-50,53,83-86,88,94-95,98,107,109 | rewrite memory calls per section 3 | T10 |
| P24 | `plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md` | 237,327,329 | rewrite wording per section 3 (byte-identical copy rule: edit src then copy to plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md) | T10 |
| P25 | `plugins/superclaude/skills/sc-recommend/refs/delegation-vs-native-heuristics.md` | 28 | rewrite to name only remaining tools (P3: codegraph) | T11 |
| P26 | `src/superclaude/agents/auggie-reviewer.md` | 5,36,81,115 | delete the two tools from `tools:`; rewrite lines 36, 81, 115 | T11 |
| P27 | `src/superclaude/agents/pm-agent.md` | 11,19,21,31-35,54,67,93,109,114,133,240,244-247,250-252,260-262 | rewrite lifecycle per section 3 (repo-local file memory) | T10 |
| P28 | `src/superclaude/agents/reflect-reviewer.md` | 5,147 | delete the four tools; rewrite line 147 | T11 |
| P29 | `src/superclaude/agents/reuse-auditor.md` | 5,54,57,131 | delete the three tools; rewrite lines 54, 57, 131 | T11 |
| P30 | `src/superclaude/agents/rf-qa-qualitative.md` | 154,327 | keep: onboarding is generic English/template text, not Serena | none (keep) |
| P31 | `src/superclaude/agents/troubleshoot-analyst.md` | 5 | delete the four tools from `tools:` | T11 |
| P32 | `src/superclaude/commands/adversarial.md` | 7 | delete `serena` from the `mcp-servers:` frontmatter list | T9 |
| P33 | `src/superclaude/commands/auggie-review.md` | 6,78 | delete frontmatter entry; rewrite line 78 | T11 |
| P34 | `src/superclaude/commands/brainstorm.md` | 6,120 | delete `serena` from frontmatter | T9 |
| P35 | `src/superclaude/commands/cleanup-audit.md` | 7 | delete `serena` from the `mcp-servers:` frontmatter list | T9 |
| P36 | `src/superclaude/commands/cli-eval.md` | 6 | delete `serena` from the `mcp-servers:` frontmatter list | T9 |
| P37 | `src/superclaude/commands/cli-portify.md` | 7 | delete `serena` from the `mcp-servers:` frontmatter list | T9 |
| P38 | `src/superclaude/commands/init-lite.md` | 7 | delete `serena` from the `mcp-servers:` frontmatter list | T9 |
| P39 | `src/superclaude/commands/load.md` | 3,6,27,35,42,49,66,98,105 | rewrite per memory decision (section 3); delete `serena` frontmatter | T10 |
| P40 | `src/superclaude/commands/pm.md` | 6,16,47 | rewrite memory lifecycle per section 3; delete `serena` frontmatter | T10 |
| P41 | `src/superclaude/commands/post-release.md` | 7 | delete `serena` from the `mcp-servers:` frontmatter list | T9 |
| P42 | `src/superclaude/commands/pr-submit.md` | 6 | delete `serena` from the `mcp-servers:` frontmatter list | T9 |
| P43 | `src/superclaude/commands/reflect.md` | 6,108,144,158,166-172,281 | rewrite tool table; delete `--onboard` Serena bootstrap rows; delete `serena` frontmatter | T10, T11 |
| P44 | `src/superclaude/commands/release-split.md` | 7 | delete `serena` from the `mcp-servers:` frontmatter list | T9 |
| P45 | `src/superclaude/commands/research.md` | 6,100 | delete both lines | T9 |
| P46 | `src/superclaude/commands/review-translation.md` | 6 | delete `serena` from the `mcp-servers:` frontmatter list | T9 |
| P47 | `src/superclaude/commands/save.md` | 3,6,28,35,42,48,66,98,104 | rewrite per memory decision (section 3): keep command, swap Serena memory for repo-local files; delete `serena` frontmatter | T10 |
| P48 | `src/superclaude/commands/task.md` | 7 | delete `serena` from the `mcp-servers:` frontmatter list | T9 |
| P49 | `src/superclaude/commands/troubleshoot.md` | 3,6,52,58,75,89,96,112,161,173 | rewrite wording; delete `serena` frontmatter | T11 |
| P50 | `src/superclaude/commands/validate-roadmap.md` | 6-7 | delete the mcp__serena__* entries from `allowed-tools` and `serena` from `mcp-servers` | T10, T11 |
| P51 | `src/superclaude/core/CLAUDE.md` | 21,90,112 | delete row 21; trim S2 list at 90; rewrite row at 112 | T9 (lines 21, 90), T11 (line 112) |
| P52 | `src/superclaude/core/HOW-WE-WORK.md` | 237,327,329 | rewrite wording per section 3 (byte-identical copy rule: edit src then copy to plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md) | T10 |
| P53 | `src/superclaude/core/RESEARCH_CONFIG.md` | 26,142 | delete both | T9 |
| P54 | `src/superclaude/core/RULES.md` | 49-50 | keep wording if the commands are kept (decision section 3); otherwise delete | none (keep) |
| P55 | `src/superclaude/hooks/hooks.json` | 47 | delete the four `mcp__serena__*` alternatives from the matcher regex | T7 |
| P56 | `src/superclaude/modes/MODE_Orchestration.md` | 24 | delete the row (or replace with codegraph in P3) | T11 |
| P57 | `src/superclaude/modes/MODE_Task_Management.md` | 15-18,25-26,33,36,43,49-50,53,82-85,87,93-94,97,106,108 | rewrite memory calls per section 3 | T10 |
| P58 | `src/superclaude/skills/ccsession-tag/install.sh` | 41 | keep: harmless cleanup of an obsolete file; reword comment only if desired | none (keep) |
| P59 | `src/superclaude/skills/readme/SKILL.md` | 741 | keep: onboarding is generic English/template text, not Serena | none (keep) |
| P60 | `src/superclaude/skills/sc-adversarial-protocol/SKILL.md` | 12,491,2243,2277,2285 | delete rows and YAML block | T9 |
| P61 | `src/superclaude/skills/sc-auggie-review-protocol/SKILL.md` | 10 | delete `serena` from the `mcp-servers:` frontmatter list | T9 |
| P62 | `src/superclaude/skills/sc-brainstorm-protocol/SKILL.md` | 15,57,193,387 | delete frontmatter entry and fallback_1 wording | T11 |
| P63 | `src/superclaude/skills/sc-brainstorm-protocol/refs/handoff-routing.md` | 24,26-27 | delete tier 2 block (renumber) | T11 |
| P64 | `src/superclaude/skills/sc-brainstorm-protocol/refs/socratic-templates.md` | 15 | keep: onboarding is generic English/template text, not Serena | none (keep) |
| P65 | `src/superclaude/skills/sc-cleanup-audit-protocol/SKILL.md` | 6,20,57,83 | delete frontmatter + line 83; keep `.serena/` ignore only if folder may still exist (decision D4) | T11 |
| P66 | `src/superclaude/skills/sc-cli-eval-protocol/SKILL.md` | 11 | delete `serena` from the `mcp-servers:` frontmatter list | T9 |
| P67 | `src/superclaude/skills/sc-cli-portify-protocol/SKILL.md` | 7 | delete `serena` from the `mcp-servers:` frontmatter list | T9 |
| P68 | `src/superclaude/skills/sc-crash-recovery/SKILL.md` | 3,37,62,67,79,145,157 | rewrite investigator #3 to read the new memory folder (section 3); rename report section | T10 |
| P69 | `src/superclaude/skills/sc-crash-recovery/refs/investigators.md` | 76,83,85,164 | rewrite investigator #3 to read the new memory folder (section 3); rename report section | T10 |
| P70 | `src/superclaude/skills/sc-crash-recovery/refs/report-template.md` | 63,124 | rewrite investigator #3 to read the new memory folder (section 3); rename report section | T10 |
| P71 | `src/superclaude/skills/sc-crash-recovery/scripts/bootstrap_scan.sh` | 146-147 | repoint to the new memory folder (section 3) or delete the two JSON fields | T10 |
| P72 | `src/superclaude/skills/sc-init-lite-protocol/SKILL.md` | 13 | delete `serena` from the `mcp-servers:` frontmatter list | T9 |
| P73 | `src/superclaude/skills/sc-pm-protocol/SKILL.md` | 21,26-30,43-44,50,52,113,157,166 | rewrite lifecycle per section 3 | T10 |
| P74 | `src/superclaude/skills/sc-post-release-protocol/SKILL.md` | 11,244,259 | delete serena from enum and frontmatter (P3: add codegraph) | T9 |
| P75 | `src/superclaude/skills/sc-pr-submit-protocol/SKILL.md` | 10 | delete `serena` from the `mcp-servers:` frontmatter list | T9 |
| P76 | `src/superclaude/skills/sc-recommend/refs/delegation-vs-native-heuristics.md` | 28 | rewrite to name only remaining tools (P3: codegraph) | T11 |
| P77 | `src/superclaude/skills/sc-reflect-protocol/SKILL.md` | 5,19,91,148,150-151,154,252,254-258,260,262,268,272,274-275,279,287,295,297-299,301,303,305,307-309,311,314,340,342,344-345,361,383-386,389,400,500,509-514,523,525-527,530-531,536,540,546,548,552,563,569,574-575,581,590-595,600,602,605-608,613,615-616,620,632,636,747,780,862,961,968,970-974,984-987,990-991,1081,1096,1348,1492,1496,1506,1518-1520,1867,1873,1875,1950,1986,2041 | rewrite: delete Serena probes/telemetry; symbol chain -> P3 codegraph; calibration memory -> section 3 | T10, T11 |
| P78 | `src/superclaude/skills/sc-reflect-protocol/refs/cost-profile.yaml` | 73 | rewrite tool name | T11 |
| P79 | `src/superclaude/skills/sc-reflect-protocol/refs/coverage-mapping.md` | 173 | rewrite tool name | T11 |
| P80 | `src/superclaude/skills/sc-reflect-protocol/refs/deviation-taxonomy.md` | 50,65 | delete line 65; rewrite line 50 (P3: codegraph lookup) | T11 |
| P81 | `src/superclaude/skills/sc-reflect-protocol/refs/grader-extensions.md` | 217 | reword | T11 (with the reflect rewrite) |
| P82 | `src/superclaude/skills/sc-reflect-protocol/refs/input-resolution.md` | 81-82 | delete both bullets | T10 |
| P83 | `src/superclaude/skills/sc-reflect-protocol/refs/ops-integration.md` | 118,120,125-126,137,140,164,168-170,174,178-180 | delete the catalog section together with the `--onboard` feature | T11 (with the reflect rewrite) |
| P84 | `src/superclaude/skills/sc-reflect-protocol/refs/reflection-rubric.md` | 124,126-128 | delete lines 124-127 | T11 (with the reflect rewrite) |
| P85 | `src/superclaude/skills/sc-reflect-protocol/refs/remediation-handoff.md` | 179,232 | rewrite handoff to a file under the new memory folder (section 3) | T10 |
| P86 | `src/superclaude/skills/sc-reflect-protocol/refs/reviewer-spec.md` | 49,51 | rewrite tool name | T11 |
| P87 | `src/superclaude/skills/sc-reflect-protocol/refs/runtime-surface.md` | 21 | rewrite tool name | T11 |
| P88 | `src/superclaude/skills/sc-release-split-protocol/SKILL.md` | 13 | delete `serena` from the `mcp-servers:` frontmatter list | T9 |
| P89 | `src/superclaude/skills/sc-roadmap-protocol/SKILL.md` | 13,325-326,414,419,425,436,443,455 | delete Serena rows; make the existing file fallback the primary; delete `serena` frontmatter | T9 |
| P90 | `src/superclaude/skills/sc-roadmap-protocol/refs/extraction-pipeline.md` | 343 | keep: onboarding is generic English/template text, not Serena | none (keep) |
| P91 | `src/superclaude/skills/sc-task-protocol/SKILL.md` | 88,91,103,287,303,309,319 | rewrite STRICT tier prerequisites; delete activate_project/memory steps | T10, T11 |
| P92 | `src/superclaude/skills/sc-tasklist-protocol/SKILL.md` | 683 | edit the row (STRICT no longer needs Serena) | T11 (with the sc-task STRICT rewrite) |
| P93 | `src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md` | 3-4,10,31,156,168,193,216,439,606,620 | delete tools and wording | T11 |
| P94 | `src/superclaude/skills/sc-troubleshoot-protocol/refs/diagnosability-audit.md` | 11 | delete the mention | T11 |
| P95 | `src/superclaude/skills/sc-troubleshoot-protocol/refs/triage-checklist.md` | 11 | delete the mention | T11 |
| P96 | `src/superclaude/skills/sc-validate-roadmap-protocol/SKILL.md` | 4,13,22,25,47,126-130,138,140,146-147,155,165,320,329,331-332,349,980,982,1005,1007,1018,1039-1040,1070-1071 | rewrite: state persistence to repo-local files (section 3); symbol checks to Grep/Read now, codegraph in P3 | T10, T11 |
| P97 | `src/superclaude/skills/task-builder/SKILL.md` | 35,107 | keep: onboarding is generic English/template text, not Serena | none (keep) |
| P98 | `src/superclaude/skills/tech-reference/SKILL.md` | 43,52,73,208 | keep: onboarding is generic English/template text, not Serena | none (keep) |
| D1 | `src/superclaude/hooks/scripts/freshness-pre-edit.sh` | 25-36 | delete the `relative_path` branch (`REL_PATH` lookup and its `elif`), keep `file_path`; reword the line-36 message to "no file_path in tool_input" | T7 |
| D2 | `plugins/superclaude/hooks/scripts/freshness-pre-edit.sh` | 25-36 | same edit as D1 (hand-maintained mirror) | T7 |
| D3 | `tests/cli/reflect/test_marker_suppression.py` | 101-130 | edit in the same commit as the reflect SKILL.md section 6.1.1 change: follow the section's new heading, or delete the envelope test if the section is deleted (section 4) | T11 |
| D4 | `tests/cli/reflect/test_reviewer_readonly_tools.py` | 7, 31 | drop `execute_shell_command` from the denylist set and docstring (the tool no longer exists) | T11 |
| D5 | `tests/cli/reflect/test_reviewer_finding_parity.py` | 33 | same as D4 | T11 |


```
### .dev/tasks/to-do/TASK-WF-phase1RemovalSpe-20261029-185100/source.md:257-302

```markdown
## 2. Goal and definition of done

### 2.1 Goal

Remove codebase-memory-mcp and Serena from everything IronClaude owns: installer and CLI code (`superclaude install`, `superclaude mcp`, the `update.sh` path), registry entries and MCP templates, hooks, skills, commands, agents, refs, modes, core docs, the hand-maintained `plugins/superclaude/` tree and the root `commands/`, `agents/` copies, user docs, tests and CI, plus the user-environment registrations IronClaude can prove it (or the Coder bundle, with IronClaude's exact argv) wrote. Historical `.dev/` artifacts stay untouched. Phase 2 installs codegraph; Phase 3 adopts it in primitives.

### 2.2 Definition of done (all must hold; T14 checks each)

| # | Condition | How it is checked |
|---|---|---|
| DoD-1 | No repo file outside `.dev/` references either server, except the allowlist in 2.4 | the two acceptance searches in T14 (W1 `PAT`, and W2 `PAT` plus `P2`), each filtered by the 2.4 allowlist, print nothing |
| DoD-2 | `superclaude install` on a fresh HOME writes no codebase-memory or Serena binary, MCP entry, permission, hook matcher entry, companion skill/agent/hook or `CLAUDE.md` mention | T14 sandbox run "fresh": temp `HOME` and `CLAUDE_CONFIG_DIR`, stub `claude` on `PATH`; then `rg -i 'serena\|codebase-memory\|codebase_memory' "$HOME"` prints nothing and the stub's call log has no `mcp add` |
| DoD-3 | `./update.sh` on an existing workspace removes the IronClaude-owned leftovers: the user-scope `codebase-memory-mcp` registration and every Tier R `serena` registration (section 3.2; the current-pin `serena` entry, which Coder's bundle also writes, is kept and reported by Phase 1 alone, section 3.6, only until Phase 2's `codegraph_ready()` gate removes it in the same `superclaude install` run, Phase 2 spec §2.12), IronClaude's receipt and marker files when their binary is gone, the four `mcp__serena__*` alternatives of the freshness hook matcher in `~/.claude/settings.json`, the Serena rows of `~/.claude/CLAUDE.md`, `~/.claude/HOW-WE-WORK.md`, `~/.claude/RESEARCH_CONFIG.md` and of every installed command, agent and skill | T14 sandbox run "existing": temp HOME seeded with both registrations (exact live shapes from `inventory/codebase-memory.md` 3.1 row 4 and `inventory/serena.md` E2), the old hook matcher and the old core files; run `./update.sh` with `PIPX_HOME`/`PIPX_BIN_DIR` inside the temp HOME; then the same `rg` prints nothing outside the kept data in 2.3 |
| DoD-4 | A same-named entry that IronClaude did not write (different command, non-empty `env` or `headers`, local or project scope) survives untouched; `env: {}` and `headers: {}` count as absent | unit tests of the retire step (T3) |
| DoD-5 | Targeted suites green; full `uv run pytest` has no failure that is not in the T0 baseline; `make verify-sync` and `make lint` pass | T14 |
| DoD-6 | Serena memory is replaced (section 5), so `/sc:save`, `/sc:load`, pm-agent, crash-recovery, reflect calibration and validate-roadmap ledgers work without Serena; no primitive step names a removed tool (section 4) | T10b, T11c acceptance searches; T14 |
| DoD-7 | Handoff notes exist for every other IronbellyOrg repo with live hits (section 6), and the Coder part is cross-referenced to Phase 2's Coder handoff | section 6 of this spec; T15 copies them into the task package |

Why install overwrites the core files: `install_core.py:65-67` skips an existing file only without `--force`; `update.sh:8` passes `--force`, and Coder passes it when its pinned SHA changes (`catalogue/ironclaude/install.sh:91-95`). Hook matchers are refreshed in place under `--force` (`install_hooks.py:393-431`). Commands, agents and skills are re-copied; Phase 1 deletes no shipped primitive name, so no stale installed primitive file remains (copy-only installers would otherwise leave it, `research/install-update-flow.md` 3.1).

Merge constraint (`research/install-update-flow.md` 5.2 row E, 5.3 step 3): Phase 1 commits stay on the feature branch and are **not merged to `master` on their own**. Coder's monitor bumps its pin to every new `master` commit (`ironclaude-upstream-monitor.yml:107`, `:131`), and a `master` with neither codebase-memory nor codegraph fails Coder's contract test (`test-57-catalogue-configure.sh:243`). Phases 1 and 2 merge as one unit; the Phase 1 executor never opens a `master` PR for Phase 1 alone.

### 2.3 Leftovers IronClaude does not own (handed off, not removed by Phase 1)

| Leftover | Owner | Evidence | Handed off in |
|---|---|---|---|
| Binary `/usr/local/bin/codebase-memory-mcp` (root-owned, v0.12.1) | Coder image | Coder `templates/VSCode-AIDev02/Dockerfile.coder:323-351` (`inventory/codebase-memory.md` 3.1 row 1) | Phase 2 Coder handoff (section 6.2) |
| Running codebase-memory daemon and stdio processes | Coder (restart) | `inventory/codebase-memory.md` 3.1 row 15 | Phase 2 Coder handoff |
| Serena uv tool `serena-agent` 1.7.0 and `~/.local/bin/{serena,serena-agent,serena-hooks}` | Coder bundle `catalogue/mcp-bundle-core/install.sh:128-170`; no IronClaude code installs it (`rg 'uv tool install' src` is empty, `inventory/serena.md` E9) | `research/install-update-flow.md` 4.3 | Phase 2 Coder handoff |
| Serena re-registration on every workspace start, bundle markers `~/.aidev/installed/mcp-bundle-core*`, the `serena` alias in `workspace_defaults/bashrc.skel:88`, Coder tests that assert Serena or codebase-memory (`test-57`, `test-startup-boot.sh:1978-2066`, `spec2-health.sh:79`) | Coder repo | `research/install-update-flow.md` 4.3, 4.4 | Phase 2 Coder handoff |
| Upstream codebase-memory companions (client MCP entries, skill, three agents, hooks, instructions in `~/.claude`, `~/.codex`, `~/.config/opencode`, `~/.augment`, `~/.agents`) and `~/.local/bin/codebase-memory-mcp`, only on a workspace where IronClaude ran the upstream installer ("kind B"; existence UNVERIFIED; none on this workspace) | the upstream binary's own `codebase-memory-mcp uninstall -y --dir=~/.local/bin` | `inventory/codebase-memory.md` 3.2, 3.3 | printed by the retire step (section 3) and recorded in the `CHANGELOG.md` entry (T12) |
| `~/.local/bin/install.sh` (upstream updater) and the receipt `~/.local/bin/.superclaude-codebase-memory.json` on kind-B workspaces | the user (upstream `uninstall` reports the updater but does not delete it) | `inventory/codebase-memory.md` 3.2 row 2 | printed `rm` command (section 3), `CHANGELOG.md` entry (T12) |
| User data: `~/.cache/codebase-memory-mcp` (4.2 MB, no project indexes), `~/.serena` (62 MB), 12 project `.serena/` folders, uv cache entries | the user | `inventory/codebase-memory.md` 3.1 row 14; `inventory/serena.md` E6-E8, E10 | kept by decision (section 3); printed commands |
| Current-pin `serena` user registration (`uvx --from serena-agent==1.7.0 ...`), on this workspace and every workspace | Coder's bundle writes the byte-identical entry, so Phase 1 alone cannot prove ownership: its retire step keeps it and prints `claude mcp remove serena --scope user` on every install (section 3.6) only until Phase 2's `codegraph_ready()` gate removes it in the same `superclaude install` run (Phase 2 spec §2.12, task T3b) | `install_mcp.py:59`; `research/install-update-flow.md` 4.3; Phase 2 spec §2.12 | Phase 2 (gate, T3b); Phase 2 Coder handoff step 2 stops the bundle re-adding it |
| Live `codebase-memory-mcp` registration on THIS workspace | removed by the real `./update.sh` only after Phases 1 and 2 merge; Phase 1 tests only in sandboxes (T14) | section 8 | Phase 2 final gate |

### 2.4 Allowlisted residual mentions (the only hits the acceptance searches may return)

| Path | Why it stays | Removal trigger |
|---|---|---|
| The retire step's source and tests (section 3 names the files) and the `"serena"` and `"codebase-memory-mcp"` entries in the `test_removed_mcp_servers_are_not_in_registry` guard of `tests/cli/test_install_mcp_registry.py` | they name the servers in order to remove them; the guard keeps them out of the registry | a later cleanup task once Coder ships neither server (section 3) |
| `src/superclaude/commands/load.md` and its `plugins/superclaude/commands/load.md` and root `commands/sc-load.md` copies: one legacy-read sentence for `.serena/memories/` | memory decision item 7 (section 5): one release of read-only fallback for existing Serena memories | the first release after Phases 1 and 2 merge |
| `.gitignore:113` (`.serena/`) and `src/superclaude/skills/sc-cleanup-audit-protocol/SKILL.md:57` (`.serena/` in the audit ignore list) | old checkouts still carry local `.serena/` folders (`inventory/serena.md` D4) | one release later |
| `CHANGELOG.md` (history plus the new removal entry), `POST-REFLECT-TASK.md`, `docs/memory/patterns_learned.jsonl`, `docs/memory/pm_context.md`, `src/superclaude/skills/ccsession-tag/install.sh:41`, `tests/skills/test_implement_severity_replay.py`, `tests/troubleshoot/fixtures/regression/sysbox-20260918/Fable-D3/REPORT.md` | history or an unrelated label (`inventory/serena.md` D6) | none |
| The 19 files that match only `onboarding` (rows marked "none (keep)" whose action says "onboarding is generic English") | false positives | none |

```
### .dev/tasks/to-do/TASK-WF-phase1RemovalSpe-20261029-185100/source.md:303-377

```markdown
## 3. Existing-workspace cleanup design

### 3.1 Decision

An automatic, non-interactive, **non-fatal "retire step"** runs at the end of every `superclaude install` (with or without `--force`), so both `./update.sh` (`update.sh:8`) and Coder's `ironclaude/install.sh` reach it. It removes only user-scope MCP registrations of `codebase-memory-mcp` and `serena` that IronClaude can prove it wrote, plus IronClaude's own receipt and marker files once the binary they describe is gone. Proof is tiered by provenance: a shape only IronClaude code could have produced is removed (Tier R); a shape another writer could also have produced (Coder's bundle, a hand-typed docs command) is kept and reported with the exact removal command (Tier K) until Phase 2's `codegraph_ready()` gate removes the Serena launcher entries (Phase 2 spec §2.12). Nothing Coder-owned or upstream-owned is removed; all indexes, caches and memories are kept.

Method: adversarial full (`decisions/P1-existing-workspace-cleanup/adversarial/merged-recommendation.md`; options in `decisions/P1-existing-workspace-cleanup/option-{a,b,c}.md`). Scores: A (registration-only step) 0.877, C (explicit consented command) 0.730, B (also remove binaries and the uv tool) 0.717; convergence 100% (23 of 23 points) after two rounds and a resolution round; the invariant gate blocked once (INV-001, the Serena matcher) and cleared after all 14 findings were resolved. Rejected: B's `uv tool uninstall serena-agent` (Coder installed it, no receipt, breaks Coder's health check) and its automated upstream uninstall (keeps the 759-line module and a 300 s path for unverified workspaces; prompt-free account-wide uninstall is what `install_mcp.py:981-986` forbids); C's separate command (fails the goal on `./update.sh`). One Tier R row was spot-checked for this spec: `git show 0e7bc31f^:src/superclaude/cli/install_mcp.py` line 69 is the row (a) argv below.

### 3.2 Matchers

**codebase-memory-mcp (removed when it matches):** top-level user entry whose `command` is an absolute path with basename `codebase-memory-mcp`, `type` `stdio` or absent, `args` absent or `[]`, `env` and `headers` absent or empty (IronClaude registered whatever discovery found, `install_mcp.py:866`). **Binary gate:** if `command` equals `<home>/.local/bin/codebase-memory-mcp` (unresolved `Path.home().absolute()`) and that file exists, keep it (kind B: upstream-installed binary still present). A `command` pointing at a `.local/bin/codebase-memory-mcp` path under a **different** home is also kept ("kept: path differs from current HOME"). Every other matching entry (Coder's `/usr/local/bin`, any other path, the current home's `~/.local/bin` path whose binary is gone) is removed. A non-matching shape is kept: "kept: not an IronClaude registration".

**serena, Tier R (removed):** exact `command` + `args` match, `type` `stdio` or absent, `env` and `headers` each absent or `{}` (`claude mcp add` and Coder's bundle write `"env":{}`; the live entry on this workspace has it, `jq '.mcpServers.serena.env' ~/.claude.json` prints `{}`). Removed unconditionally, whatever `codegraph_ready()` says (Phase 2 spec §2.12). Each row is pinned by a test:

| Row | Written by | `command` | `args` |
|---|---|---|---|
| (a) | IronClaude registry `050d5ea2`..`0e7bc31f^` | `uvx` | `["--from", "git+https://github.com/oraios/serena", "serena", "start-mcp-server", "--context", "ide-assistant", "--enable-web-dashboard", "false", "--enable-gui-log-window", "false"]` |
| (b) | pre-fork `setup/components/mcp.py` `5bee1571` | `uvx` | `["--from", "git+https://github.com/oraios/serena", "serena", "start-mcp-server", "--context", "ide-assistant", "--project", "$(pwd)"]` |
| (c) | pre-fork `setup/components/mcp.py` `43112779` | `serena` | `["start-mcp-server", "--context", "ide-assistant", "--project", "$(pwd)"]` |

`$(pwd)` is the literal six-character token (stored without shell expansion), which is why rows (b) and (c) prove code wrote them.

**serena, Tier K (kept, one printed line per run; matched with `env` and `headers` each absent or `{}`; kept by Phase 1 alone only until Phase 2's `codegraph_ready()` gate removes it, Phase 2 spec §2.12; a launcher with a non-empty `env` or `headers` is reported as "kept: customised registration" and is never removed, not even by that gate):** the current pin `uvx --from serena-agent==1.7.0 serena start-mcp-server --context claude-code --project-from-cwd --enable-web-dashboard false --enable-gui-log-window false` (identical to `install_mcp.py:59`, the docs command and Coder's bundle argv, so IronClaude cannot prove it wrote it; **this is the entry on this workspace**, `inventory/serena.md` E1); the bare `... --context ide-assistant` form (`00ec67c7`, identical to the old hand command); the `--project <absolute path>` family; any other user `serena` entry whose argv contains `start-mcp-server`. Printed: "Legacy Serena registration kept until codegraph is ready (IronClaude cannot prove it wrote it; the next `superclaude install` that installs codegraph removes it). Remove it now with `claude mcp remove serena --scope user`." A `serena` entry without `start-mcp-server` is "kept: not a Serena launcher registration".

**Receipt and marker (deleted):** `~/.local/bin/.superclaude-codebase-memory.json` and `~/.local/bin/.superclaude-codebase-memory.pending`, only when `~/.local/bin/codebase-memory-mcp` is absent and each file passes the existing private-file predicates (regular file, `st_uid == getuid()`, `st_nlink == 1`, `st_mode & 0o077 == 0`, opened with `O_NOFOLLOW`; `install_codebase_memory.py:95-100`, `:185-199`) and `~/.local` and `~/.local/bin` pass `_check_install_directory` (`:125-139`). Otherwise listed, not deleted. These are the only files the step ever deletes. T3 copies the small predicate logic into the retire module, because T5 deletes `install_codebase_memory.py`.

### 3.3 Behaviour, ordering and bounds

- **Never touched:** local scope (`projects.*.mcpServers`) and project `.mcp.json`, whatever the name; every binary; uv tools; the upstream updater `~/.local/bin/install.sh`; upstream client companions; `~/.cache/codebase-memory-mcp`, `~/.serena`, project `.serena/`; user permissions; the hook matcher (refreshed by the normal hook installer under `--force`, `install_hooks.py:393-431`).
- **Index and memory policy: keep.** Matches `install_codebase_memory.py:74-78` and upstream `uninstall` (keeps indexes unless `--delete-indexes`). Delete commands are printed, labelled "only if you no longer need them", never run.
- **One pure classifier** `classify_retired_entries() -> list[(name, verdict, reason)]` reads all state once (via `read_user_mcp_entry(name)`, `install_mcp.py:714-754`), then actions run in a fixed order: (1) receipt/marker cleanup, (2) codebase-memory registration, (3) serena registration.
- **Removal helper** `_remove_exact_user_entry(name, matcher)` in `install_mcp.py` (replaces the name-only `_cleanup_user_native_registration`, `:916-948`; Phase 2 reuses it): re-read and re-match immediately before `claude mcp remove <name> --scope user`; re-read after (absent -> removed; same shape -> "could not verify" warning; different shape -> "replaced concurrently, kept", never retried).
- **Bounds:** exec `claude` directly as an argv list (not the existing `_run_command`, which runs `$SHELL -c` with `shell=True`, `install_mcp.py:129-141`, so its timeout kills only the shell), `start_new_session=True`, kill the process group on timeout, 10 s per call, 15 s cap for the whole step. No subprocess when nothing needs removal.
- **Placement:** in `main.py` `install()`, in the slot of the deleted codebase-memory phase (baseline `main.py:254`), before the exit-code block, inside its own `try/except Exception` that only warns.
- **Non-fatal:** no outcome changes the install exit code (`update.sh:2` runs under `set -euo pipefail`; a non-zero install would stop `make sync-dev` and `doctor`).

| Failure | Behaviour |
|---|---|
| Lookup "unknown" | warning naming the cause (empty `CLAUDE_CONFIG_DIR`, unreadable or unparseable file, duplicate key, non-object) plus `claude mcp remove <name> --scope user` |
| Entry changed before removal | kept, reported, not retried |
| Same shape after removal | "could not verify" warning with the manual command |
| Per-call timeout (10 s) / step cap (15 s) | process group killed or remaining calls skipped; warning; next install retries (idempotent) |
| `shutil.which("claude")` is None | skip note printing the exact `claude mcp remove <name> --scope user` per entry that would have been removed |
| Receipt/marker fails a predicate | listed, not deleted |
| Any other exception | caught; warning only |

### 3.4 Read-only surfaces and messages

- `superclaude install --list`: the deleted codebase-memory block (baseline `main.py:161-186`) is replaced by one line per retired name: "absent", "will be removed (IronClaude shape)" or "kept: <reason>".
- `superclaude doctor`: a new check that **warns, never fails**, when the classifier still finds a removable entry (`update.sh:10` exit unchanged; `doctor.py:16-49`).
- `superclaude update`: prints only "legacy registration present: run `superclaude install`" (keeps its never-touches-MCP contract, `docs/user-guide/mcp-installation.md:24`).
- Messages, one line per action: after any removal, "Restart running Claude sessions; a running session can write the entry back. Check with `superclaude install --list`."; after a codebase-memory removal, "If you installed codebase-memory-mcp yourself, its own `uninstall` removes its client companions."; after a Tier R `serena` removal, the exact removed `command` + `args`, plus "To keep using Serena, register it yourself under the name `serena-local`, e.g. `claude mcp add --scope user serena-local -- uvx --from serena-agent==1.7.0 serena start-mcp-server --context claude-code --project-from-cwd --enable-web-dashboard false --enable-gui-log-window false`" (option order as in `install_mcp.py:1142-1159`; the name `serena-local` is the one Phase 2's `codegraph_ready()` gate never removes, Phase 2 spec §2.12, so the hint survives the next install); whenever `~/.local/bin/codebase-memory-mcp` exists, `"$HOME/.local/bin/codebase-memory-mcp" uninstall -y --dir="$HOME/.local/bin"` labelled "for a codebase-memory you or IronClaude installed under ~/.local/bin; removes its own client companions, keeps indexes" (never a bare command, which could resolve to Coder's copy); `uv tool uninstall serena-agent` labelled "if you installed it yourself; Coder workspaces reinstall it at start"; the Tier K line; the data delete commands.

### 3.5 Files and tests (task T3)

- New `src/superclaude/cli/install_retired_mcp.py`: `RETIRED_MCP_SERVERS` table (name -> matcher, with the comment "remove after the first release in which Coder's image and bundle no longer ship either server"), the classifier, receipt/marker predicates and cleanup, message builder, `run_retire_step()`.
- `src/superclaude/cli/install_mcp.py`: `_remove_exact_user_entry(name, matcher)` and the direct-exec `claude` wrapper (generic, no server names).
- `src/superclaude/cli/main.py`: the call in `install()`, the `install --list` lines, the `update` notice. `src/superclaude/cli/doctor.py`: the warn-only check.
- New `tests/cli/test_install_retired_mcp.py`: table-driven classifier (every Tier R row removed; every Tier K row kept with the line printed; near misses: one token changed, extra or missing arg, expanded `$(pwd)`; non-empty `env`/`headers` kept; `env: {}` and `headers: {}` count as absent (a Tier R row carrying `"env":{}` is removed; the current pin carrying `"env":{}`, the live shape, is Tier K); the re-register hint names `serena-local`; relative cbm command kept; cbm `.local/bin` path under a different home kept with "path differs from current HOME"; a Tier R serena removal prints the removed argv and the re-register command; local-scope and `.mcp.json` entries ignored; binary, receipt and marker states, including "receipt present, binary absent" converging in one run); helper (concurrent replacement kept, not retried; verify failure warns); bounds (stub `claude` that hangs: process group killed, 15 s cap honoured; missing CLI: skip note); CLI integration (temp HOME, stub `claude`, install exit code unchanged when the step fails); `superclaude update` and `doctor` never mutate and never change their exit code.
- Unchanged contract: `tests/cli/test_update_script.py` (`update.sh` list and order) still passes.

### 3.6 Goal exceptions the design accepts (closing conditions)

| Exception | Closes when |
|---|---|
| The current `serena-agent==1.7.0` registration is kept by Phase 1 alone on every workspace (including this one), with the removal command printed on every install | Phase 2's `codegraph_ready()` gate removes it in the first `superclaude install` run where codegraph is ready (Phase 2 spec §2.12, task T3b; reached by `./update.sh` and Coder's slug run), and Coder's step 2 stops the bundle re-adding it (Phase 2 Coder handoff) |
| Other Tier K Serena rows kept | the user runs the printed command |
| A non-forced `superclaude install` keeps stale core and hook text | the next `--force` install (`update.sh` and Coder's SHA-change path both force) |
| `superclaude update` removes nothing | next `superclaude install` |
| Coder re-adds `serena` at each start | Phase 2 Coder handoff |
| Kind-B `~/.local/bin` binary and companions | the user runs the printed absolute upstream `uninstall`; the next install removes registration, receipt and marker |
| Whether a Coder SHA-change run killed at 60 s is retried with `--force` is UNVERIFIED (Coder `install.sh:91-95`) | Phase 2 Coder handoff confirms it |

Accepted residual risks: `claude mcp remove` deletes by name, so a sub-second race remains; CLI-side `CLAUDE_CONFIG_DIR` resolution is UNVERIFIED; a running session can write a removed entry back until restarted; a `claude` defined only as a shell alias is skipped with the manual command printed; a hand-made entry identical to a Tier R shape is removed (restorable with one command). Sunset: a later cleanup task deletes `install_retired_mcp.py`, its tests and the doctor/list/update hooks once Coder ships neither server.

```
### .dev/tasks/to-do/TASK-WF-phase1RemovalSpe-20261029-185100/source.md:378-407

```markdown
## 4. Primitive gap policy

**Decision:** Phase 1 leaves no step that names a tool absent after Phase 1, at any commit. Load-bearing Serena symbol, reference, diagnostics and allowlist references are **triaged, then deleted or rewritten to a named native floor in Phase 1**; they are not deferred to Phase 3. Phase 1 also writes a codegraph slots ledger so Phase 3 adds codegraph as a tier above the floor; the floor stays permanently. Method: adversarial quick (`decisions/P1-primitive-gap-policy/adversarial/merged-recommendation.md`; Option A base merged with Option C's triage rule; scores A 0.841, B 0.778, C 0.735; convergence 1.00; contract status success). Rejected: deferring load-bearing rows to Phase 3 (Option B), because Phase 3 is not planned to merge with Phases 1-2 and every intermediate commit would carry dangling steps.

codebase-memory has no reference in any primitive (`inventory/primitive-usage.md` section 1, search C4: 0 hits), so this policy concerns Serena only. Memory rows (MEM) follow section 5; Serena-only activation and meta-prompts (ACT, NUDGE) are deleted (section 5 rule M8).

### 4.1 Rules the executor applies (T9, T10a-T10b, T11a-T11c)

| # | Rule |
|---|---|
| G1 | **Triage first.** For each load-bearing SYM/REF/DIAG/ALLOW row (`primitive-usage.md` section 4 lists them): **delete** the Serena half when the same step already names a Serena-free Read/Grep/Glob/auggie path (examples: `sc-troubleshoot-protocol/SKILL.md:193` has the Glob + Grep fallback at `:194`; `agents/auggie-reviewer.md:36` says "Read (or serena)"); **rewrite** it when there is no fallback, the fallback is "skip", or the fallback itself calls Serena |
| G2 | **Floor per job** (phrased as tools, never as shell commands): symbol lookup or outline -> Grep for the definition (`def name\|class name\|function name`), then Read the range, auggie first where the primitive already uses it; references -> Grep with a word-boundary pattern for the symbol, then Read the call sites; implementations and type hierarchy -> Grep for `class .*\(<Base>\)` or `implements <Iface>`, marked "best effort" |
| G3 | **Closed read-only rosters** (`agents/reflect-reviewer.md`, `agents/troubleshoot-analyst.md`, `agents/reuse-auditor.md`) only lose `mcp__serena__*` names; the floor inside them is Read/Grep/Glob/auggie; Bash is never added |
| G4 | **Diagnostics:** `get_diagnostics_for_file` is dropped everywhere. Orchestrators whose `allowed-tools` already include Bash (reflect chain steps 5/5.5, `sc-troubleshoot-protocol`) run the project's own linter or type-checker through Bash under reflect's existing section 6.1.1 safety envelope (timeout, output cap, denylist), retitled for the Bash call. Closed rosters say the orchestrator's verification leg covers diagnostics |
| G5 | **Every `tools:` / `allowed-tools:` line naming `mcp__serena__*` is load-bearing**, whatever its inventory label, and changes in the same commit as the skill body that drives that agent and its pinning test (`tests/troubleshoot/test_diagnostic_worker_contract.py` `TOOLS` set and `:152`; the prose roster at `sc-troubleshoot-protocol/SKILL.md:31`). `mcp-servers:` frontmatter lists simply drop `serena` (no Python consumer, `primitive-usage.md` C13) |
| G6 | **Fallbacks that call Serena are rewritten, not trusted:** `agents/reuse-auditor.md:131` becomes "Grep by capability tokens + skeleton grep", F4 at `:57` uses a Grep reference search; `sc-validate-roadmap-protocol/SKILL.md:320-349` (Step 0.5) gets a Grep-definition floor with the same 30-lookup cap and the same INFORMATIONAL ONLY artifact, not "skip" |
| G7 | **reflect treats floor evidence as normal.** No `serena` degraded token is emitted; `"serena"` and `"serena:context-excluded"` leave `_DEGRADED_COMPONENTS_HALT_SET` (`src/superclaude/cli/reflect/contract.py:32-34`, verified) and the section 6.5 and section 10 fallback rows of the reflect SKILL.md. T6 changes the CLI side with its fixtures; T11a changes the reflect skill side. T6 first is safe: until T11, a run whose skill still emits `serena` merely stops halting on it, and the branch is not released in between |
| G8 | **reflect contract fields:** field names without "serena" stay stable with a producer or a constant: `find_declaration_no_match` (from a zero-hit Grep), `type_hierarchy_invoked: false` (step 4.5 deleted), `summarize_changes_invoked: false`, `references_extended_info_used: false`; Step 7 `search_deps` is skipped and its claim marked `[INFERRED]`. **Exception (this spec's decision D4):** `serena_summary_corroboration` is deleted, not kept: the only producers are `ensemble.py:824` and `SKILL.md:780` and no CLI code reads it (`rg -n 'summary_corroboration' src plugins` shows only those producers and the prose at `SKILL.md:1096`, `refs/deviation-taxonomy.md:65`); it exists only to report Serena's deleted `summarize_changes` corroboration |
| G9 | **Slots ledger:** the executor writes `.dev/codegraph-migration/handoffs/phase3-codegraph-slots.md`, one row per touched step: file, step heading or anchor (not a line number), former Serena tool, action (deleted / floor), floor used, contract fields touched. It is the Phase 3 input; the first T9-T11c task that deletes or rewrites a step creates it, every later T9-T11c edit appends to it, and T11c checks it covers every load-bearing file of section 4.2 |
| G10 | **Core rules file:** `src/superclaude/core/CLAUDE.md:112` (refresh-tool table, "Symbolic queries" row) becomes "Grep for the definition and references, then Read" (Phase 3 adds codegraph); `:21` (MCP table row) and the `replace_symbol_body` item of rule S2 (`:90`) are deleted (T9) |

### 4.2 Where the load-bearing rows are (from `primitive-usage.md` section 4)

SYM: `commands/troubleshoot.md` (1), `skills/sc-reflect-protocol/SKILL.md` (6), `skills/sc-troubleshoot-protocol/SKILL.md` (1), `skills/sc-validate-roadmap-protocol/SKILL.md` (2). REF: `agents/reuse-auditor.md` (1), `skills/sc-reflect-protocol/SKILL.md` (2). DIAG: `skills/sc-reflect-protocol/SKILL.md` (3). ALLOW: `commands/validate-roadmap.md`, `skills/sc-reflect-protocol/SKILL.md`, `skills/sc-troubleshoot-protocol/SKILL.md`, `skills/sc-validate-roadmap-protocol/SKILL.md`, plus (rule G5) the four agent `tools:` lines. CONTRACT: `skills/sc-reflect-protocol/SKILL.md` (4). EDIT: `hooks/hooks.json`, `hooks/scripts/freshness-pre-edit.sh` (T7). Every row has a `plugins/superclaude/` or root `commands/`, `agents/` twin where section 1.2 lists one; twins are edited identically in the same commit.

### 4.3 Acceptance (checked in T11a-T11c, repo-wide in T11c, and in T14)

1. `rg -n "${EX[@]}" 'mcp__serena__' src/superclaude plugins/superclaude commands agents` prints nothing.
2. No primitive step names a tool absent from its own roster: for each agent and skill with a `tools:` or `allowed-tools:` line, every `mcp__<server>__<tool>` named in its body is in that line (T11a-T11c run the check script in section 8.0).

```
### .dev/tasks/to-do/TASK-WF-phase1RemovalSpe-20261029-185100/source.md:408-426

```markdown
## 5. Serena memory replacement

Decision applied: W2 decision D1 (`inventory/serena.md` 3.2; adversarial quick, `decisions/W2-serena-memory-replacement/adversarial/merged-recommendation.md`): Serena memory is replaced in Phase 1 by plain markdown files; codegraph takes no memory job. Phase 1 implements it in T10a and T10b. The rules every rewritten primitive follows:

| # | Rule | Source |
|---|---|---|
| M1 | Store: `<project>/.superclaude/memory/<key>.md`, flat markdown, subfolders for topics. Tool mapping: `write_memory` -> Write, `read_memory` -> Read, `list_memories` -> Glob `.superclaude/memory/**/*.md`, `edit_memory` -> Edit, `delete_memory` -> delete only through the user (no primitive deletes memories) | merged-recommendation.md; `serena.md` 3.2 item 1 |
| M2 | `<project>` is the git top-level of the current directory (`git rev-parse --show-toplevel`), or the current directory outside git: one store per worktree | merged-recommendation.md:27 |
| M3 | On first write, if `<project>/.superclaude/.gitignore` is absent, create it with the single line `*` (the repo-level `.superclaude/` ignore exists only in IronClaude, `.gitignore:114`) | merged-recommendation.md:34-35 |
| M4 | Single-owner keys (`pm_context`, `last_session`, `next_actions`) are overwritten whole; keys parallel sessions may write (`checkpoint`, `decision`, handoffs) are written as `<key>-<session-or-timestamp>.md` and never edited in place | merged-recommendation.md:31 |
| M5 | Reflect cold-start calibration moves to tracked `docs/memory/reflect/deviation-patterns-<slug>.md`; T13 moves `.serena/memories/reflect/deviation-patterns-IronClaude.md` there with `git mv` (content kept) | merged-recommendation.md:19 |
| M6 | `sc-roadmap-protocol`: the existing `<output_dir>/.session-memory.md` fallback becomes the only path; the Serena branches go away | merged-recommendation.md:60 |
| M7 | `/sc:load` reads `.serena/memories/<key>.md` when `.superclaude/memory/<key>.md` is absent, for one release; never writes there; tells the user the folder is read-only history (allowlisted in 2.4) | merged-recommendation.md:41-43 |
| M8 | Delete, do not port, the Serena-only non-memory calls: `think_about_*`, `summarize_changes`, `activate_project`, `onboarding`, `check_onboarding_performed`, `prepare_for_new_conversation`, `get_current_config`, and reflect's `--onboard` flow (Steps 0.5c, 0.7, 0.7b) with `refs/ops-integration.md`'s Serena WARN catalog | `serena.md` 3.2 item 8 |

Consumers rewritten in T10a and T10b (the split is listed in section 8) (from `serena.md` 3.1, verified hit lines in section 1.2): `commands/save.md`, `commands/load.md`, `commands/pm.md`, `agents/pm-agent.md`, `skills/sc-pm-protocol/SKILL.md`, `modes/MODE_Task_Management.md`, `skills/sc-task-protocol/SKILL.md` (STRICT tier memory steps), `skills/sc-validate-roadmap-protocol/SKILL.md` (ledger, terminology map, pattern log keys move to `.superclaude/memory/validate-roadmap/<key>.md`, still fail-open), `skills/sc-reflect-protocol/SKILL.md` and `refs/remediation-handoff.md`, `refs/input-resolution.md`, `skills/sc-crash-recovery/` (SKILL.md, `refs/investigators.md`, `refs/report-template.md`, `scripts/bootstrap_scan.sh:146-147` fields renamed `has_memory`, `memory_count`, reading `.superclaude/memory`), `core/HOW-WE-WORK.md` lines 237, 327, 329 (plus its byte copy), and the `plugins/superclaude/` and root `commands/`, `agents/` copies of each. `core/RULES.md` lines 49-50 stay (the commands stay).

Residual risks the adversarial run left to this spec, and where they are handled: ignore-file guard (M3, T10a acceptance greps for the `.gitignore` instruction in every writer), root resolution (M2, same), parallel-session overwrites (M4). Open point the run left (shared store across worktrees) stays per-worktree (W2 D1), reversible later.

```
### .dev/tasks/to-do/TASK-WF-phase1RemovalSpe-20261029-185100/source.md:427-578

````markdown
## 6. Other-org-repo removal

Source: `.dev/codegraph-migration/inventory/org-repos.md` (W3; GitHub code search on default branches, 2026-10-29, queries capped at 100 files, so "no hit" is not proof of absence). 13 of 44 target repositories returned hits: 67 live paths and 310 historical paths (keep). Phase 1 does **not** edit any other repository (planning rule, and no cross-repo authorization); it ships these notes. T15 copies each note to the Phase 1 task package as `handoffs/<repo>.md` so an owner can paste it into an agent session in that repository.

### 6.1 Repos and live files

| Repo | Live paths (from W3 "Per-repository live references") | Kind | Historical paths kept |
|---|---|---|---|
| Coder | `.serena/project.yml`; `templates/VSCode-AIDev02/Dockerfile.coder`; `templates/VSCode-AIDev02/catalogue/mcp-bundle-core/install.sh`; `.../mcp-bundle-core/manifest.yaml`; `_bmad-output/implementation-artifacts/6-3-mcp-register-and-proxy-betas.md`; `_bmad-output/planning-artifacts/architecture/architecture-Coder-github-automation-orca-restart-2026-09-09/ARCHITECTURE-SPINE.md`; `_bmad-output/specs/spec-aidev02-v2/catalogue-slugs.md` | image, installer, config, specs | 48 |
| Financials | `grants-credits/.serena/project.yml`; `.claude/settings.json`; `.claude/agents/{auggie-reviewer,reuse-auditor,pm-agent}.md`; `.claude/commands/sc/{cli-eval,cli-portify,help,init-lite,load,pm,pr-submit,research,save,select-tool,task,workflow,reflect,troubleshoot,validate-roadmap}.md`; `.claude/skills/sc-brainstorm-protocol/refs/handoff-routing.md`; `.claude/skills/sc-crash-recovery/{SKILL.md,refs/investigators.md}`; `.claude/skills/sc-reflect-protocol/{SKILL.md,refs/ops-integration.md}`; `.claude/skills/{sc-task-protocol,sc-troubleshoot-protocol,sc-validate-roadmap-protocol}/SKILL.md` (28 paths) | checked-in copies of IronClaude primitives, settings | 1 |
| IronFlow | `.serena/project.yml`; `.claude/settings.json`; `.claude/commands/sc/reflect.md`; `.claude/skills/sc-reflect-protocol/SKILL.md` | config, primitive copies | 39 |
| IronOps | `.claude/settings.json` (codebase-memory permissions); `.serena/project.yml`; `src/ironops/skills/ironops-troubleshoot-protocol/SKILL.md` (owned skill source) | config, owned skill | 6 |
| InfraDocs | `.serena/project.yml`; `configurations/jenkins/artifacts/phase5.1-context-refresh-requirements.md` | config, doc | 11 |
| ClaudeCodeCodeAudit | `.serena/project.yml`; `README.md`; `00-MASTER-PROCESS-OVERVIEW.md`; `01-QUICK-START.md`; `02-OUTPUT-SCHEMAS.md`; `03-ACCEPTANCE-CRITERIA.md`; `04-LITE-VARIANT.md`; `PHASE-0-DISCOVERY.md`; `PHASE-0A-PRD-VALIDATION.md`; `PHASE-2-CHUNKING.md`; `PHASE-3-NARROW-REVIEW.md`; `PHASE-4-HOLISTIC-REVIEW.md`; `PHASE-6-FINAL-REPORT.md`; `docs/generated/PROJECT_INDEX.md` | workflow docs, config | 12 |
| Ironbrain | `PLANNING.md` | doc | 8 |
| Octodive | `.serena/project.yml` | config | 159 |
| TUIBBS | `.serena/project.yml`; `docs/governance/post-merge-review-protocol.md` | config, doc | 2 |
| TUIBBS-scp | `.serena/project.yml` | config | 11 |
| shrapnel-gov | `.serena/project.yml`; `.claude/settings.json`; `workflows/resolution-charter-rpt-workflow.md` | config, workflow doc | 3 |
| llm-workflows | `.claude/commands/rf/opinion.md` | command (future-integration wording) | 8 |
| Ironeye | none | historical only | 2 (no handoff) |

The 310 historical paths (`.dev/`, `claudedocs/`, completed logs, `.serena/memories/` records) are listed in `org-repos.md` "Keep (historical)" and must not be edited or deleted by any handoff.

### 6.2 Coder (cross-reference only)

The Coder part is **merged into Phase 2's Coder handoff** (Phase 2 spec, task P2), because the Coder change must also bake codegraph and follow the order in `research/install-update-flow.md` 5.3 (additive codegraph bake first, make test-57 pin-agnostic, IronClaude merge, pin bump, then removals). Facts Phase 2's handoff must carry from Phase 1: (1) after Phases 1+2 merge, `superclaude install` no longer registers `codebase-memory-mcp`, removes the IronClaude-shaped user-scope `codebase-memory-mcp` entry (including Coder's `/usr/local/bin` path) and Tier R `serena` entries; Phase 1 alone **keeps** the current-pin `serena` entry because Coder's bundle writes the identical argv (section 3.2, 3.6), until Phase 2's `codegraph_ready()` gate removes it in the same install run (Phase 2 spec §2.12); so the Coder change must stop the bundle installing and re-registering Serena (otherwise the next workspace start writes it back), and must confirm whether a SHA-change run killed at 60 s is retried with `--force`; (2) IronClaude never deletes `/usr/local/bin/codebase-memory-mcp`, the `serena-agent` uv tool, `~/.serena`, `~/.cache/codebase-memory-mcp` or bundle markers; (3) the live Coder paths in 6.1 plus the Coder test and health surfaces in `research/install-update-flow.md` 4.3-4.4; (4) Coder's own `.serena/project.yml` is in `test-49-spec2-evidence.sh:307`'s hashed evidence set.

### 6.3 Handoff notes (one per repo, paste-ready)

Each note is self-contained. Common rules repeated inside each: do not edit historical records; do not delete project knowledge (`.serena/memories/*` content is moved, not deleted); open the PR on that repository's own origin.

**Financials**

```text
Repo: IronbellyOrg/Financials. Context: IronClaude (issue IronbellyOrg/IronClaude#323) removed the Serena and codebase-memory MCP servers; codegraph replaces code navigation later (IronClaude Phase 3). Your checked-in .claude/ copies of IronClaude commands, skills and agents still name Serena tools.
Do:
1. Find the provenance of .claude/{commands/sc,skills,agents}: if they are copies of IronClaude primitives, replace them by re-copying from the IronClaude release that contains the removal (for example from ~/.claude after `superclaude install --force` on that release) instead of hand-editing. If they are local forks, edit them.
2. Paths with live hits: .claude/settings.json (mcp__serena permissions); .claude/agents/{auggie-reviewer,reuse-auditor,pm-agent}.md; .claude/commands/sc/{cli-eval,cli-portify,help,init-lite,load,pm,pr-submit,research,save,select-tool,task,workflow,reflect,troubleshoot,validate-roadmap}.md; .claude/skills/sc-brainstorm-protocol/refs/handoff-routing.md; .claude/skills/sc-crash-recovery/SKILL.md and refs/investigators.md; .claude/skills/sc-reflect-protocol/SKILL.md and refs/ops-integration.md; .claude/skills/{sc-task-protocol,sc-troubleshoot-protocol,sc-validate-roadmap-protocol}/SKILL.md; grants-credits/.serena/project.yml.
3. Remove every mcp__serena__* entry from .claude/settings.json permissions. Delete grants-credits/.serena/project.yml; if grants-credits/.serena/memories/ exists, move its files to grants-credits/.superclaude/memory/ (IronClaude's new memory store) instead of deleting them.
Keep: the one historical path listed by the inventory, and anything under .dev/ or claudedocs/.
Verify: `git grep -n -i -E 'serena|codebase-memory|codebase_memory' -- . ':!.dev' ':!claudedocs'` returns only intentional history.
```

**IronFlow**

```text
Repo: IronbellyOrg/IronFlow. Context: IronClaude (issue IronbellyOrg/IronClaude#323) removed the Serena and codebase-memory MCP servers.
Do:
1. .claude/commands/sc/reflect.md and .claude/skills/sc-reflect-protocol/SKILL.md are copies of IronClaude's /sc:reflect; refresh them from the IronClaude release that contains the removal rather than hand-editing. If they are local forks, replace the Serena symbol and memory steps together (symbol steps -> Grep plus Read; memory -> .superclaude/memory/, reflect calibration -> docs/memory/reflect/).
2. Remove mcp__serena__* entries from .claude/settings.json.
3. Delete .serena/project.yml; move any .serena/memories/ files to .superclaude/memory/ (reflect calibration files to docs/memory/reflect/).
Keep: the 39 historical paths (.dev/, claudedocs/ and recorded logs).
Verify: `git grep -n -i -E 'serena|codebase-memory' -- . ':!.dev' ':!claudedocs'` returns only intentional history.
```

**IronOps**

```text
Repo: IronbellyOrg/IronOps. Context: IronClaude (issue IronbellyOrg/IronClaude#323) removed the Serena and codebase-memory MCP servers.
Do:
1. src/ironops/skills/ironops-troubleshoot-protocol/SKILL.md is owned distributable source: remove mcp__serena__* from its allowed-tools and rewrite its Serena symbol steps to Grep for the definition plus Read of the range (auggie first if the skill already uses it). Check whether a generated copy of this skill exists elsewhere (regeneration path UNVERIFIED) and regenerate it.
2. .claude/settings.json allows codebase-memory indexing/search tools: remove those permission entries.
3. Delete .serena/project.yml; move any .serena/memories/ files to .superclaude/memory/.
Keep: the 6 historical paths.
Verify: `git grep -n -i -E 'serena|codebase-memory|codebase_memory|mcp__codebase' -- . ':!.dev' ':!claudedocs'`.
```

**InfraDocs**

```text
Repo: IronbellyOrg/InfraDocs. Context: IronClaude (issue IronbellyOrg/IronClaude#323) removed the Serena MCP server.
Do:
1. configurations/jenkins/artifacts/phase5.1-context-refresh-requirements.md routes symbolic queries through mcp__serena tools: replace that guidance with Grep plus Read (codegraph later, where the workspace has it). It is Markdown guidance, not executable CI.
2. Delete .serena/project.yml; move any .serena/memories/ files to .superclaude/memory/.
Keep: the 11 historical paths, including dated incident and access-check records.
Verify: `git grep -n -i serena -- . ':!.dev' ':!claudedocs'`.
```

**ClaudeCodeCodeAudit**

```text
Repo: IronbellyOrg/ClaudeCodeCodeAudit. Context: IronClaude (issue IronbellyOrg/IronClaude#323) removed the Serena MCP server; this repo's audit workflow documents prescribe Serena navigation and memory and require Serena tool evidence.
Do:
1. Rewrite the tool instructions and evidence requirements in README.md, 00-MASTER-PROCESS-OVERVIEW.md, 01-QUICK-START.md, 02-OUTPUT-SCHEMAS.md, 03-ACCEPTANCE-CRITERIA.md, 04-LITE-VARIANT.md, PHASE-0-DISCOVERY.md, PHASE-0A-PRD-VALIDATION.md, PHASE-2-CHUNKING.md, PHASE-3-NARROW-REVIEW.md, PHASE-4-HOLISTIC-REVIEW.md and PHASE-6-FINAL-REPORT.md: symbol navigation -> Grep plus Read (codegraph later); memory persistence -> plain files under .superclaude/memory/; acceptance evidence -> the replacement tools' output instead of Serena tool counts.
2. docs/generated/PROJECT_INDEX.md mentions a language-server dependency: check the real dependency file before removing anything (UNVERIFIED).
3. Delete .serena/project.yml; move any .serena/memories/ files to .superclaude/memory/.
Keep: the 12 historical audit and file-list records.
Verify: `git grep -n -i -E 'serena|mcp__serena' -- . ':!.dev' ':!claudedocs'`.
```

**Ironbrain**

```text
Repo: IronbellyOrg/Ironbrain. Context: IronClaude (issue IronbellyOrg/IronClaude#323) replaced codebase-memory with codegraph (https://github.com/colbymchenry/codegraph).
Do: PLANNING.md proposes codebase-memory for selective repository-local structural retrieval; update the proposal to name codegraph, or mark codebase-memory as retired. The inventory found no runtime integration.
Keep: the 8 historical research paths.
Verify: `git grep -n -i codebase-memory -- . ':!.dev' ':!claudedocs'`.
```

**Octodive**

```text
Repo: IronbellyOrg/Octodive. Context: IronClaude (issue IronbellyOrg/IronClaude#323) removed the Serena MCP server.
Do: delete .serena/project.yml; move any .serena/memories/ files to .superclaude/memory/. Check whether runtime cleanup beyond the project file is needed (UNVERIFIED).
Keep: the 159 historical release and investigation records (evidence, not live integrations).
Verify: `git grep -n -i serena -- . ':!.dev' ':!claudedocs'`.
```

**TUIBBS**

```text
Repo: IronbellyOrg/TUIBBS. Context: IronClaude (issue IronbellyOrg/IronClaude#323) removed the Serena MCP server.
Do:
1. docs/governance/post-merge-review-protocol.md has a Serena symbol cross-reference step: replace it with `rg -n -w <symbol>` plus Read of the call sites (codegraph later).
2. Delete .serena/project.yml; move .serena/memories/ files (including the brainstorming memory) to .superclaude/memory/; do not delete them.
Keep: the decision log and the historical paths.
Verify: `git grep -n -i serena -- . ':!.dev' ':!claudedocs'`.
```

**TUIBBS-scp**

```text
Repo: IronbellyOrg/TUIBBS-scp. Context: IronClaude (issue IronbellyOrg/IronClaude#323) removed the Serena MCP server.
Do: delete .serena/project.yml; move any .serena/memories/ files to .superclaude/memory/.
Keep: the 11 prior audit, study, decision and .dev records.
Verify: `git grep -n -i serena -- . ':!.dev' ':!claudedocs'`.
```

**shrapnel-gov**

```text
Repo: IronbellyOrg/shrapnel-gov. Context: IronClaude (issue IronbellyOrg/IronClaude#323) removed the Serena MCP server.
Do:
1. workflows/resolution-charter-rpt-workflow.md reads Serena memories and falls back to auto-memory: point the lookup at .superclaude/memory/ and keep the existing fallback.
2. Remove mcp__serena__* entries from .claude/settings.json.
3. Delete .serena/project.yml. Before touching .serena/memories/, ask the repository owner whether the memories are still needed; move them to .superclaude/memory/, never delete project knowledge.
Keep: the two memory records and the completed workflow log.
Verify: `git grep -n -i serena -- . ':!.dev' ':!claudedocs'`.
```

**llm-workflows**

```text
Repo: IronbellyOrg/llm-workflows. Context: IronClaude (issue IronbellyOrg/IronClaude#323) removed the Serena MCP server.
Do: .claude/commands/rf/opinion.md mentions a future Serena integration while declaring an empty server list; delete or reword that sentence (do not describe Serena as installed).
Keep: the 8 historical paths.
Verify: `git grep -n -i serena -- . ':!.dev' ':!claudedocs'`.
```

The 31 repositories with no returned hit (listed in `org-repos.md` "Targets with no returned hits") get no note; the inventory warns this is not a clean bill of health (capped search, default branches only).

````
### .dev/tasks/to-do/TASK-WF-phase1RemovalSpe-20261029-185100/source.md:579-601

```markdown
## 7. Shared files with Phase 2

Phase 2 (install codegraph) edits these files after Phase 1. Both phases merge to `master` as one unit (section 2.2), so Phase 2 starts from the Phase 1 branch tip. "Baseline" below means commit `55d40308`; Phase 2 can recover any deleted block with `git show 55d40308:<path>`.

| File | What Phase 1 leaves behind | What Phase 2 is expected to add (not done by Phase 1) |
|---|---|---|
| `src/superclaude/cli/install_mcp.py` | Registry `MCP_SERVERS` without `serena` and `codebase-memory-mcp`. Kept and made generic: `read_user_mcp_entry(name)` (baseline `:714-754`, unchanged), `_run_registration_command(cmd)` (`:766-772`), and `_remove_exact_user_entry(name, matcher)` plus a direct-exec `claude` wrapper with process-group timeouts (section 3.3), replacing `_cleanup_user_native_registration` (`:916-948`); used by the retire step and reusable by Phase 2. Deleted: `import ... as codebase_memory` (`:21`), `_native_selection_error`, `_native_lifecycle_notice` (`:486-503`), the native prerequisite branch (`:571-583`), the Serena uv advisory (`:561-570`), `_native_registration_matches`, `_add_user_native_entry`, `_restore_user_native_entry` (`:757-812`), `install_codebase_memory_mcp` (`:815-913`), `uninstall_codebase_memory_mcp` (`:951-1007`), the dispatch (`:1025-1028`), `uninstall`/`yes` parameters and menu option "Uninstall Codebase Memory MCP" (`:1243-1343` parts). Menu: "1. Install MCP servers (default)", "2. Cancel" | a `codegraph` registry entry, a native dispatch branch and `install_codegraph_mcp` modelled on baseline `:815-913`; parameterised add/verify/restore helpers restored from baseline `:757-812` with a name and an args list (`research/install-update-flow.md` 2.2, decision 3) |
| `src/superclaude/cli/main.py` | `install()` with the eight framework phases and no MCP phase (baseline `:254-262` and the `native_success` exit term at `:273` deleted), plus the non-fatal retire step call in the slot of the deleted phase (section 3.3); `install --list` with one retired-server line per name instead of the codebase-memory block (`:161-186` replaced); `update` printing only the read-only legacy notice; `mcp()` without `--uninstall`/`--yes` (`:299-309`, `:327`, `:334-340`) and with help text that names no removed server | the required codegraph phase and its exit term, a codegraph block in `install --list` (`research/install-update-flow.md` 2.2) |
| `src/superclaude/cli/install_retired_mcp.py` (new, section 3.5) | the retire step, classifier and receipt cleanup | nothing; Phase 2 must not move codegraph registration into it |
| `src/superclaude/cli/doctor.py` | one warn-only check for removable legacy registrations (section 3.4) | an optional codegraph check (a failing doctor check turns `./update.sh` red, `research/install-update-flow.md` 1.5) |
| `tests/cli/test_update_command.py` | the autouse fixture keeps only `HOME`, `CLAUDE_CONFIG_DIR` and the plugin/Orca stubs (baseline `:68-75`); 10 tests remain; the expected phase list ends with user setup and the retire step | a codegraph phase guard, modelled on baseline `:28-76`, `:254-277`, `:345-370` |
| `tests/cli/test_install_mcp_cli.py` (new, T1) | generic `superclaude mcp` tests (scopes, prompts, gateway preflight, menu) | codegraph selection cases |
| `tests/cli/test_install_mcp_registry.py` | 9 baseline tests minus the Serena template entries; the `test_removed_mcp_servers_are_not_in_registry` tuple includes `serena` and `codebase-memory-mcp` | codegraph registry-contract tests |
| `tests/unit/test_cli_install.py` | packaged-file lists without `MCP_Serena.md`, `configs/serena.json`, `configs/serena-docker.json` (baseline `:150-153`, `:423-425`) | any new codegraph MCP guide or config file names |
| `src/superclaude/mcp/` and `plugins/superclaude/mcp/` | no `MCP_Serena.md`, no `configs/serena*.json`; no Serena cross-references in `MCP_Auggie.md`, `MCP_Morphllm.md`, `MCP_Tavily.md` | an optional codegraph guide (Phase 2 decides) |
| `src/superclaude/core/CLAUDE.md` | MCP table without the `serena` row (baseline `:21`); freshness rule S2 without `replace_symbol_body` (`:90`); refresh-tool row at `:112` names Grep/Read instead of `mcp__serena__find_symbol` (section 4) | a codegraph row in the MCP table once Phase 2 installs it; Phase 3 changes the refresh-tool row to codegraph |
| `docs/user-guide/mcp-installation.md` | the codebase-memory default-setup, removal, failure and release-gate sections deleted (`inventory/codebase-memory.md` row C8); Serena rows deleted (`serena.md` S27); no retired-server text (decision D7: the `CHANGELOG.md` entry and the retire step's output carry it) | the codegraph default-setup section where "Default Framework Setup" was (baseline `:5-26`) |
| `docs/reference/mcp-server-guide.md` | "Codebase Memory Native Lifecycle" (`:31-55`) and "Serena Project Memory" (`:370-394`) deleted | a codegraph lifecycle section |
| `docs/mcp/mcp-optional-design.md`, `README.md` (`:38`, `:64`, `:75`, `:219`) | no mention of either server | codegraph wording |
| `.github/workflows/test.yml` | the "Install Claude CLI" step (`:156-159`) kept; its comments (`:133-134`, `:155`) rewritten to name no removed server (row C12) | comments that name codegraph; no step change (the step is already there) |
| `CHANGELOG.md` | one new entry for the removal | one new entry for codegraph |
| `update.sh`, `tests/cli/test_update_script.py` | unchanged | unchanged (`research/install-update-flow.md` decision 1) |

```
### .dev/tasks/to-do/TASK-WF-phase1RemovalSpe-20261029-185100/source.md:602-792

````markdown
## 8. Task breakdown (execution order)

Six groups, 19 tasks (T10 and T11 are each split into pieces, review finding X-12). One commit per task (conventional commit, ending with the attribution line the executor's session requires); every commit stages the task package (`git add .dev/tasks`) and never stages `.claude/` (except `.claude/settings.json`, which Phase 1 does not touch). After each group's last commit the executor posts the section 9 issue comment. Tasks run in the listed order; no task needs a later task to go green.

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
- **Group G0 done:** issue comment (section 9) with the baseline pass/fail counts.

### G1: codebase-memory out of the installer and CLI

**T1. Port the generic `superclaude mcp` tests**
- Files: new `tests/cli/test_install_mcp_cli.py`.
- Change: `inventory/codebase-memory.md` 4.1 exactly: own home fixture and an `mcp_cli` fixture without any `native`/`install_codebase_memory_mcp` patching; port the 11 tests listed there (971 without `--uninstall`/`--yes` cases, 1126, 1195, 1217, 1229, 1274, 1285, 1298, 1306 and 1114 with `context7` instead of cbm, 1334 gateway part only). The 5 menu/message tests (990, 1001, 1023, 1034, 1049) wait for T4.
- Acceptance: `uv run pytest tests/cli/test_install_mcp_cli.py -q -p no:cacheprovider` passes, and `uv run pytest tests/cli/test_install_codebase_memory.py tests/cli/test_install_mcp_registry.py tests/cli/test_install_mcp_tavily.py tests/cli/test_update_command.py tests/docs/test_tavily_doc_alignment.py -q -p no:cacheprovider` still shows the T0 `cbm.txt` counts.
- Commit: `test(mcp): port generic superclaude mcp tests out of the codebase-memory suite (#323)`

**T2. Detach `superclaude install` and `install --list`**
- Files: `src/superclaude/cli/main.py`, `tests/cli/test_update_command.py`, `tests/cli/test_install_codebase_memory.py`.
- Change: `inventory/codebase-memory.md` 4.2 exactly (main.py `:66`, `:78-83`, `:161-186`, `:254-262`, the `native_success` exit term, help text `:38`, `:44`, `:50-52`; fixture `native_phase_guard` reduced to `HOME`, `CLAUDE_CONFIG_DIR` and the plugin/Orca stubs; delete 5 test functions, rewrite the `--force` test; delete the cross-entry fixture and tests at `:1382`, `:1517`, `:1614`). The fixture and `main.py` change in the same commit (hazard: the real-install tests would otherwise reach the real upstream installer).
- Acceptance: `uv run pytest tests/cli/test_update_command.py tests/cli/test_install_codebase_memory.py tests/cli/test_install_mcp_cli.py tests/cli/test_cli_registration.py tests/unit/test_cli_install.py -q -p no:cacheprovider` passes, and `rg -n "install_codebase_memory|_NATIVE_INSTALLER|native_phase_guard" src/superclaude/cli/main.py tests/cli/test_update_command.py` prints nothing.
- Commit: `feat(install)!: stop installing codebase-memory-mcp from superclaude install (#323)`

**T3. Add the retire step for existing workspaces**
- Files: section 3.5 (new `src/superclaude/cli/install_retired_mcp.py` and `tests/cli/test_install_retired_mcp.py`; `install_mcp.py` remover and direct-exec wrapper; `main.py` install call, `install --list` lines, `update` notice; `doctor.py` warn-only check), plus `tests/cli/test_update_command.py` (expected call list includes the retire step after user setup).
- Change: implement section 3 exactly (matchers 3.2, behaviour 3.3, surfaces and messages 3.4, tests 3.5). The retire module must not import `install_codebase_memory.py` (deleted in T5). The literal server names live only in `install_retired_mcp.py` and its test (allowlisted, section 2.4); `main.py` and `doctor.py` take names and messages from the module.
- Acceptance: `uv run pytest tests/cli/test_install_retired_mcp.py tests/cli/test_update_command.py tests/cli/test_update_script.py tests/cli/test_install_mcp_tavily.py tests/cli/test_install_mcp_cli.py tests/unit -q -p no:cacheprovider` passes; `rg -n 'install_codebase_memory' src/superclaude/cli/install_retired_mcp.py` prints nothing; in a sandbox HOME (section 10 forbids `superclaude install` against the real `HOME`, review finding X-16), `T=$(mktemp -d /tmp/p1-list.XXXXXX) && env HOME="$T" CLAUDE_CONFIG_DIR="$T" UV_CACHE_DIR="$(uv cache dir)" uv run --no-sync superclaude install --list > "$T/list.txt"` exits 0 and `rg -c 'codebase-memory-mcp|serena' "$T/list.txt"` prints at least 2 (one line each, both "absent"); then `rm -rf "$T"`.
- Commit: `feat(install): retire stale codebase-memory-mcp and serena user registrations (#323)`

**T4. Detach `superclaude mcp` and the registry from codebase-memory**
- Files: `src/superclaude/cli/main.py`, `src/superclaude/cli/install_mcp.py`, `tests/cli/test_install_codebase_memory.py`, `tests/cli/test_install_mcp_tavily.py`, `tests/cli/test_install_mcp_registry.py`, `tests/cli/test_install_mcp_cli.py`.
- Change: `inventory/codebase-memory.md` 4.3 (delete `--uninstall`/`--yes`, the native blocks of `install_mcp.py` listed under its row C2, menu becomes "1. Install MCP servers (default)" / "2. Cancel"; delete `T-icm` 834-1380, `T-tav` 382-end, `T-reg` 192-240; port the 5 deferred menu tests; add one `mcp --list` output test), **except** keep `read_user_mcp_entry` and `_run_registration_command` and the remover from T3 (section 7). Add `"codebase-memory-mcp"` to the `test_removed_mcp_servers_are_not_in_registry` tuple.
- Acceptance: `uv run pytest tests/cli/test_install_mcp_cli.py tests/cli/test_install_mcp_registry.py tests/cli/test_install_mcp_tavily.py tests/cli/test_install_codebase_memory.py tests/cli/test_update_command.py tests/cli/test_install_retired_mcp.py tests/docs/test_tavily_doc_alignment.py tests/recommend -q -p no:cacheprovider` passes, and `rg -n "codebase_memory|_native_|install_codebase_memory_mcp|uninstall_codebase_memory_mcp|--uninstall|--yes" src/superclaude/cli/main.py src/superclaude/cli/install_mcp.py` prints nothing.
- Commit: `feat(mcp)!: remove codebase-memory-mcp from the MCP registry and drop --uninstall/--yes (#323)`

**T5. Delete the installer module**
- Files: `git rm src/superclaude/cli/install_codebase_memory.py tests/cli/test_install_codebase_memory.py`.
- Change: deletion only (`inventory/codebase-memory.md` 4.5; section 3 records why no receipt logic is kept).
- Acceptance: `rg -n "install_codebase_memory|codebase_memory" src tests -g '!src/superclaude/cli/install_retired_mcp.py' -g '!tests/cli/test_install_retired_mcp.py'` prints nothing (the retire step and its test are allowlisted, section 2.4; review finding X-17); `uv run pytest tests/cli tests/unit tests/recommend tests/docs -q -p no:cacheprovider --ignore=tests/cli/eval` has no failure that is not in `$PKG/artifacts/baseline/full.txt`; `uv run ruff check src/superclaude/cli tests/cli` passes; `bash $PKG/artifacts/acceptance-search.sh cbm src tests` prints `ACCEPTANCE_SEARCH_OK cbm`.
- Commit: `refactor(cli)!: delete the codebase-memory installer module (#323)`
- **Group G1 done:** issue comment (section 9).

### G2: Serena out of CLI code, hooks and the registry

**T6. Reflect verdict contract**
- Files: `src/superclaude/cli/reflect/{contract.py,ensemble.py,config.py}`, the 25 `tests/cli/reflect/fixtures/*.yaml` rows S58-S82, `tests/cli/reflect/{test_verdict_mapping.py,test_runner_e2e.py,test_ensemble_unit.py,test_verify_denylist_git_mutations.py}`.
- Change: `inventory/serena.md` step S1 with rule G8: drop `"serena"` and `"serena:context-excluded"` from `_DEGRADED_COMPONENTS_HALT_SET` and fix the comment (`contract.py:28-34`); delete the `serena_summary_corroboration` key (`ensemble.py:824`) and its line in 24 fixtures; delete `fixtures/degraded_serena.yaml`; `degraded_with_drift.yaml` `- serena` -> `- auggie`; delete `test_degraded_serena` and `test_serena_summary_corroboration_unavailable_not_degraded`, edit the token list at `test_verdict_mapping.py:245`; repoint `test_runner_e2e.py:71` to `degraded_tier1.yaml` and confirm it still asserts exit 11; reword the docstrings/comments at `config.py:162,199`, `test_ensemble_unit.py:345`, `test_verify_denylist_git_mutations.py:11`.
- Acceptance: `uv run pytest tests/cli/reflect -q -p no:cacheprovider` passes (W2 predicts 270 tests); `rg -n -i 'serena' src/superclaude/cli/reflect tests/cli/reflect` prints nothing.
- Commit: `refactor(reflect): drop Serena tokens and the serena_summary_corroboration field from the verdict contract (#323)`

**T7. Freshness hook and eval suite**
- Files: `src/superclaude/hooks/hooks.json`, `plugins/superclaude/hooks/hooks.json`, `src/superclaude/hooks/scripts/freshness-pre-edit.sh`, `plugins/superclaude/hooks/scripts/freshness-pre-edit.sh`, `tests/cli/test_install_hooks.py`, `src/superclaude/cli/eval/suites/real.yaml`, `src/superclaude/cli/eval/coverage.py`, `src/superclaude/cli/eval/suites/README.md`, `tests/cli/eval/test_coverage_gate.py`.
- Change: matcher becomes `Edit|Write` (`hooks.json:47` and plugin `:37`); rows D1/D2 (drop the `relative_path` branch); delete the four asserts at `test_install_hooks.py:684-687`; `real.yaml`: delete capability row `:40` and eval E8 (`:566-690`), fix comments `:380-384`, `:406-407`, `:475-479`, `:499-506` (`inventory/serena.md` S2); reword `coverage.py:195` and `suites/README.md:170`; swap the tool string at `test_coverage_gate.py:127` to `mcp__context7__resolve-library-id`.
- Acceptance: `uv run pytest tests/cli/test_install_hooks.py tests/hooks tests/cli/eval/test_coverage_gate.py tests/cli/eval/test_no_mcp_skip.py tests/cli/eval/test_schema_validate.py tests/cli/eval/test_capability_gates.py -q -p no:cacheprovider` passes; `rg -n 'mcp__serena|relative_path' src/superclaude/hooks plugins/superclaude/hooks src/superclaude/cli/eval tests/cli/test_install_hooks.py tests/cli/eval/test_coverage_gate.py` prints nothing.
- Commit: `fix(hooks): drop Serena tools from the freshness gate and the eval suite (#323)`

**T8. Serena registry entry and MCP assets**
- Files: `src/superclaude/cli/install_mcp.py` (`:55-61`, `:561-570`), delete `src/superclaude/mcp/{MCP_Serena.md,configs/serena.json,configs/serena-docker.json}` and the same three under `plugins/superclaude/mcp/`, Serena cross-reference lines in `src/superclaude/mcp/{MCP_Auggie,MCP_Morphllm,MCP_Tavily}.md` and `plugins/superclaude/mcp/{MCP_Morphllm,MCP_Tavily}.md`, `tests/cli/test_install_mcp_registry.py`, `tests/unit/test_cli_install.py` (`:150-153`, `:423-425`, same commit as the deletions).
- Change: `inventory/serena.md` step S4 without the cleanup step (T3 owns it); add `"serena"` to the `test_removed_mcp_servers_are_not_in_registry` tuple.
- Acceptance: `uv run pytest tests/cli/test_install_mcp_registry.py tests/cli/test_install_mcp_tavily.py tests/cli/test_install_mcp_cli.py tests/unit/test_cli_install.py tests/cli/test_update_command.py -q -p no:cacheprovider` passes; `rg -n -i serena src/superclaude/cli/install_mcp.py src/superclaude/mcp plugins/superclaude/mcp tests/unit/test_cli_install.py` prints nothing; `uv run superclaude mcp --servers serena --dry-run 2>&1 | grep -q 'Unknown MCP server selection: serena'` succeeds.
- Commit: `feat(mcp)!: remove Serena from the MCP registry and package assets (#323)`
- **Group G2 done:** issue comment.

### G3: primitives (every edit to `src/superclaude/...` is mirrored by hand in its `plugins/superclaude/...` twin and root `commands/sc-*.md` / `agents/sc-*.md` copy in the same commit; `inventory/serena.md` D8)

**T9. Decorative mentions**
- Files: section 1.2 rows with Task `T9` (`mcp-servers:` lists in commands and skills, `core/CLAUDE.md:21,90`, `core/RESEARCH_CONFIG.md` src and plugin, `commands/help.md` rows, `sc-adversarial-protocol` memory rows, `sc-roadmap-protocol` Serena rows with rule M6, `research.md` persistence line, `sc-post-release-protocol` telemetry enum), plus `tests/sc-roadmap/compliance/test_mcp_circuit_breakers.py` (delete `test_serena_fallback`, `test_serena_referenced`) and `tests/sc-roadmap/integration/test_wave5_completion.py` (delete `test_circuit_breaker_for_serena`, reword `:69-74`).
- Change: delete the Serena entries and lines named in each row's action; no body text may still point at Serena.
- Acceptance: `make sync-dev && make verify-sync` passes; `uv run pytest tests/sc-roadmap tests/commands tests/skills tests/core tests/cli/test_how_we_work_install.py -q -p no:cacheprovider` passes; `rg -n --no-ignore 'mcp-servers:.*serena' src/superclaude plugins/superclaude commands agents` prints nothing.
- Commit: `docs(primitives): drop decorative Serena mentions and frontmatter entries (#323)`

T10 and T11 are split into five commits (review finding X-12): one failing acceptance line no longer blocks the whole memory or tool rewrite, and each piece is small enough for one QA pass. Each piece owns the section 1.2 rows named below (the rows' Task column still says `T10` / `T11`; this list is authoritative). Memory parts of a `T10, T11` row go to the T10 piece, tool parts to the T11 piece. Repo-wide searches run only on the last piece of each pair (T10b, T11c); earlier pieces run the same search scoped to their own files.

**T10a. Memory rewrite: commands, agents, modes and the pm protocol (section 5)**
- Files: rows P1, P4, P5, P8 (root `commands/sc-{load,pm,save}.md`, `agents/sc-pm-agent.md`), P11, P13, P14, P17, P23 (`plugins/superclaude/` twins), P27, P39, P40, P47, P57 (`src/superclaude/agents/pm-agent.md`, `commands/{load,pm,save}.md`, `modes/MODE_Task_Management.md`), P73 (`src/superclaude/skills/sc-pm-protocol/SKILL.md`; kept with `/sc:pm` because `src/superclaude/commands/pm.md:52` loads `sc:pm-protocol`).
- Change: rules M1-M4, M7, M8 for these files.
- Acceptance: `make sync-dev && make verify-sync` passes; `uv run pytest tests/commands tests/skills tests/core -q -p no:cacheprovider` passes; `rg -n --no-ignore 'write_memory|read_memory|list_memories|edit_memory|delete_memory|think_about_|\bsummarize_changes\b|activate_project|check_onboarding_performed|prepare_for_new_conversation|get_current_config' src/superclaude/commands/{save,load,pm}.md plugins/superclaude/commands/{save,load,pm}.md commands/sc-{save,load,pm}.md src/superclaude/agents/pm-agent.md plugins/superclaude/agents/pm-agent.md agents/sc-pm-agent.md src/superclaude/modes/MODE_Task_Management.md plugins/superclaude/modes/MODE_Task_Management.md src/superclaude/skills/sc-pm-protocol/SKILL.md` prints nothing; `rg --files-without-match '\.superclaude/\.gitignore' src/superclaude/commands/save.md src/superclaude/agents/pm-agent.md src/superclaude/skills/sc-pm-protocol/SKILL.md src/superclaude/modes/MODE_Task_Management.md` prints nothing (rule M3 in every writer).
- Commit: `feat(memory)!: move save, load, pm and pm-agent memory to .superclaude/memory files (#323)`

**T10b. Memory rewrite: skills, routing guide and reflect calibration (section 5)**
- Files: memory parts of rows P6, P15, P43 (reflect commands), P50 and P96 (validate-roadmap command and skill), P77 (reflect SKILL.md), P91 (sc-task-protocol STRICT memory steps); rows P68-P71 (crash-recovery), P82, P85 (reflect refs), P24 and P52 (`core/HOW-WE-WORK.md:237,327,329` and its byte copy `plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md`), S89 (`tests/core/test_how_we_work_routing_table.py:1074`), S90 (`tests/recommend/fixtures/routing_refresh_cases.json:576,584`), S4 (`git mv .serena/memories/reflect/deviation-patterns-IronClaude.md docs/memory/reflect/deviation-patterns-IronClaude.md`, rule M5).
- Change: rules M1-M8 for these files. After editing `HOW-WE-WORK.md`, copy it byte for byte to the plugin copy; if the edit touches the block between `<!-- level-table:v1 -->` and `<!-- /level-table -->`, re-copy that block into `src/superclaude/core/CLAUDE.md:50-67` (project `CLAUDE.md` rule; `tests/core/test_claude_md_routing_block.py`). The planned lines 237, 327 and 329 are outside the level table.
- Acceptance: `make sync-dev && make verify-sync` passes; `uv run pytest tests/core tests/commands/test_routing_plugin_parity.py tests/cli/test_how_we_work_install.py tests/recommend tests/skills tests/sc-roadmap -q -p no:cacheprovider` passes; `cmp src/superclaude/core/HOW-WE-WORK.md plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md` succeeds; `rg -n --no-ignore 'write_memory|read_memory|list_memories|edit_memory|delete_memory|think_about_|\bsummarize_changes\b|activate_project|check_onboarding_performed|prepare_for_new_conversation|get_current_config' src/superclaude plugins/superclaude commands agents` prints nothing (repo-wide, both T10 pieces); `test -f docs/memory/reflect/deviation-patterns-IronClaude.md`.
- Commit: `feat(memory)!: replace Serena memory with .superclaude/memory files in skills and the routing guide (#323)`

**T11a. Load-bearing tool steps: reflect (section 4)**
- Files: tool parts of rows P6, P15, P43 (reflect commands) and P77 (reflect SKILL.md, including the section 6.1.1 envelope retitle, rule G4); rows P78, P79, P80, P81, P83, P84, P86, P87 (reflect refs); P28 (`agents/reflect-reviewer.md`, reflect's fixed reviewer type) and P29 (`agents/reuse-auditor.md`, driven by reflect step 4a, whose Serena fallback is in reflect SKILL.md section 6.1); D3, D4, D5 (reflect tests). Both agents move with reflect because rule G5 puts a roster change in the same commit as the skill body that drives it.
- Change: rules G1-G9 for these files. The first T9-T11c task that deletes or rewrites a step creates the slots ledger `.dev/codegraph-migration/handoffs/phase3-codegraph-slots.md` (rule G9); this task appends a row for every reflect, reflect-reviewer and reuse-auditor step it touches.
- Acceptance: `make sync-dev && make verify-sync` passes; `uv run pytest tests/cli/reflect tests/skills tests/commands -q -p no:cacheprovider` passes; `bash $PKG/artifacts/acceptance-search.sh serena src/superclaude/skills/sc-reflect-protocol src/superclaude/commands/reflect.md plugins/superclaude/commands/reflect.md commands/sc-reflect.md src/superclaude/agents/reflect-reviewer.md src/superclaude/agents/reuse-auditor.md` prints `ACCEPTANCE_SEARCH_OK serena`; `comm -13 <(sort $PKG/artifacts/baseline/rosters.txt) <(uv run --no-project python -I $PKG/artifacts/check_rosters.py | sort)` prints nothing; `test -s .dev/codegraph-migration/handoffs/phase3-codegraph-slots.md`.
- Commit: `refactor(reflect): replace Serena symbol, reference and diagnostics steps with a native Grep/Read floor (#323)`

**T11b. Load-bearing tool steps: troubleshoot (section 4)**
- Files: rows P49 (`src/superclaude/commands/troubleshoot.md`), P93, P94, P95 (`sc-troubleshoot-protocol` SKILL.md and refs), P31 (`agents/troubleshoot-analyst.md:5`), S99 (`tests/troubleshoot/test_diagnostic_worker_contract.py:17-26,152`), all in one commit (rule G5: the roster, the prose roster at `sc-troubleshoot-protocol/SKILL.md:31` and the pinning test change together).
- Change: rules G1-G9 for these files; append the touched steps to the slots ledger.
- Acceptance: `make sync-dev && make verify-sync` passes; `uv run pytest tests/troubleshoot tests/skills tests/commands -q -p no:cacheprovider` passes; `bash $PKG/artifacts/acceptance-search.sh serena src/superclaude/skills/sc-troubleshoot-protocol src/superclaude/commands/troubleshoot.md src/superclaude/agents/troubleshoot-analyst.md` prints `ACCEPTANCE_SEARCH_OK serena`; `comm -13 <(sort $PKG/artifacts/baseline/rosters.txt) <(uv run --no-project python -I $PKG/artifacts/check_rosters.py | sort)` prints nothing; `rg -q 'sc-troubleshoot-protocol' .dev/codegraph-migration/handoffs/phase3-codegraph-slots.md`.
- Commit: `refactor(troubleshoot): replace Serena tools with a native Grep/Read floor (#323)`

**T11c. Load-bearing tool steps: remaining primitives, core rules and ledger completion (section 4)**
- Files: tool parts of rows P50 and P96 (validate-roadmap command and skill, rule G6 Step 0.5 floor) and P91 (sc-task-protocol STRICT prerequisites); rows P92 (`sc-tasklist-protocol/SKILL.md:683`), P26 and P33 (`agents/auggie-reviewer.md`, `commands/auggie-review.md`), P2, P62, P63 (brainstorm root command, skill and `refs/handoff-routing.md`), P65 (cleanup-audit skill), P22 and P56 (`MODE_Orchestration.md` twins), P25 and P76 (`delegation-vs-native-heuristics.md` twins), P51 line 112 (`core/CLAUDE.md` refresh-tool row, rule G10).
- Change: rules G1-G10 for these files; append the touched steps to the slots ledger and check it covers every load-bearing file of section 4.2.
- Acceptance: `make sync-dev && make verify-sync` passes; `uv run pytest tests/troubleshoot tests/cli/reflect tests/skills tests/commands tests/core tests/roadmap/test_threshold_registry.py -q -p no:cacheprovider` passes; `rg -n --no-ignore 'mcp__serena__' src/superclaude plugins/superclaude commands agents` prints nothing; `comm -13 <(sort $PKG/artifacts/baseline/rosters.txt) <(uv run --no-project python -I $PKG/artifacts/check_rosters.py | sort)` prints nothing; `for f in commands/troubleshoot.md skills/sc-reflect-protocol/SKILL.md skills/sc-troubleshoot-protocol/SKILL.md skills/sc-validate-roadmap-protocol/SKILL.md agents/reuse-auditor.md; do rg -qF "$f" .dev/codegraph-migration/handoffs/phase3-codegraph-slots.md || echo "ledger missing $f"; done` prints nothing; `bash $PKG/artifacts/acceptance-search.sh serena src/superclaude plugins/superclaude commands agents` prints `ACCEPTANCE_SEARCH_OK serena`.
- Commit: `refactor(primitives): replace the remaining Serena symbol tools with a native Grep/Read floor (#323)`
- **Group G3 done:** issue comment.

### G4: docs, repo files, tracked `.serena/`

**T12. Docs, README, CLAUDE.md, SECURITY.md, CI, CHANGELOG**
- Files: rows C8-C12 and the section 1.2 rows with Task `T12` (`CLAUDE.md:377`, `README.md:38,64,75,219`, `SECURITY.md:328`, `docs/**` rows, `docs/troubleshooting/serena-installation.md` deleted, no inbound link: `rg serena-installation` is empty), `.github/workflows/test.yml:133-134,155` (comments only; the `Install Claude CLI` step stays, row C12), `CHANGELOG.md` (new entry: what was removed, the retire step, the manual commands from section 3.4 for kind-B workspaces and user data; the entry must not say the current-pin Serena registration is kept for good: it says the registration is removed once codegraph is ready, Phase 2 spec §2.12, and names `serena-local` as the re-register name).
- Change: per each row's action; no "Retired servers" section in user docs (decision D7; the CHANGELOG entry and the retire step's own output carry the manual commands).
- Acceptance: `uv run pytest tests/docs tests/core -q -p no:cacheprovider` passes; `bash $PKG/artifacts/acceptance-search.sh all docs README.md CLAUDE.md SECURITY.md .github` prints `ACCEPTANCE_SEARCH_OK all`; `uv run --no-project python -c 'import yaml,sys; d=yaml.safe_load(open(".github/workflows/test.yml")); s=[x.get("name") for x in d["jobs"]["doctor-check"]["steps"]]; sys.exit(0 if "Install Claude CLI" in s else 1)'` exits 0 (step kept, row C12).
- Commit: `docs: remove codebase-memory and Serena from user docs, README and CI (#323)`

**T13. Tracked `.serena/` folder**
- Files: `git rm .serena/project.yml .serena/memories/memory_maintenance.md .serena/.gitignore` (the calibration file already moved in T10b); `.gitignore:113` stays (section 2.4).
- Acceptance: `git ls-files .serena` prints nothing; `test -f docs/memory/reflect/deviation-patterns-IronClaude.md`.
- Commit: `chore: remove the tracked .serena project folder (#323)`
- **Group G4 done:** issue comment.

### G5: final gate and handoffs

**T14. Final gate**
- Files: `$PKG/artifacts/final/*` only.
- Change (checks only):
  1. `make sync-dev && make verify-sync`; `make lint`; `uv run ruff format --check src/superclaude/cli tests/cli`.
  2. `T02_15_PERF_REPORT=/tmp/p1-perf.json uv run pytest -q -p no:cacheprovider --tb=line | tee $PKG/artifacts/final/full.txt`, then `comm -13 <(grep -E '^(FAILED|ERROR) ' $PKG/artifacts/baseline/full.txt | sed 's/ - .*//' | sort -u) <(grep -E '^(FAILED|ERROR) ' $PKG/artifacts/final/full.txt | sed 's/ - .*//' | sort -u)` prints nothing (no new failure; deleted tests simply disappear).
  3. `bash $PKG/artifacts/acceptance-search.sh all | tee $PKG/artifacts/final/search.txt` prints `ACCEPTANCE_SEARCH_OK all` (DoD-1).
  4. Sandbox "fresh" (DoD-2): `T=$(mktemp -d /tmp/p1-sbx.XXXXXX)`; stub `claude` at `$T/bin/claude` (logs argv to `$HOME/claude-calls.log`; `--version` prints a version and exits 0; `mcp remove <name> --scope user` deletes `.mcpServers[<name>]` from `${CLAUDE_CONFIG_DIR:-$HOME}/.claude.json` with `jq`; anything else exits 1); `env HOME=$T/fresh UV_CACHE_DIR="$(uv cache dir)" PATH="$T/bin:$PATH" uv run --no-sync superclaude install`; then `rg -n -i 'serena|codebase-memory|codebase_memory' $T/fresh` prints nothing and `grep -c 'mcp add' $T/fresh/claude-calls.log` prints 0 (or the file is absent).
  5. Sandbox "existing" (DoD-3, DoD-4): `$T/old/.claude.json` seeded with `mcpServers.codebase-memory-mcp = {"type":"stdio","command":"/usr/local/bin/codebase-memory-mcp","args":[]}`, `mcpServers.serena` = Tier R row (a) from section 3.2 as `{"type":"stdio","command":"uvx","args":[...],"env":{}}` (the `"env":{}` that `claude mcp add` writes counts as absent), `mcpServers.tavily` (any value), and `projects["/x"].mcpServers.serena` (local scope); `$T/old/.claude/settings.json` seeded with one `PreToolUse` entry whose matcher is the baseline `hooks.json:47` string and whose command is `~/.claude/hooks/freshness-pre-edit.sh`; then `env HOME=$T/old PIPX_HOME=$T/pipx PIPX_BIN_DIR=$T/pbin UV_CACHE_DIR="$(uv cache dir)" PATH="$T/pbin:$T/bin:$PATH" ./update.sh`. Expect: `jq '.mcpServers|keys' $T/old/.claude.json` is `["tavily"]`; `jq '.projects["/x"].mcpServers|has("serena")' $T/old/.claude.json` is `true`; `rg -n 'mcp__serena' $T/old/.claude/settings.json` prints nothing; `rg -n -i 'serena|codebase-memory' $T/old/.claude` prints nothing. If `pipx install` cannot reach the package index, record the error and run the same checks with `env HOME=$T/old ... uv run --no-sync superclaude install --force && uv run --no-sync superclaude doctor`; this fallback is a recorded deviation, not a pass of `update.sh` itself. Then repeat with `mcpServers.serena` set to the current pin with `"env":{}` (the live shape, `inventory/serena.md` E1) and `uv run --no-sync superclaude install --force`: the entry is kept and the output contains "Legacy Serena registration kept until codegraph is ready" (Tier K, section 3.6). This is the expected Phase 1-alone result, because no codegraph exists yet; once Phase 2 lands, its `codegraph_ready()` gate removes the entry in the same run (Phase 2 spec §2.12, checked by Phase 2's layer-2 sandbox step 6).
  6. Robustness check, install and doctor without a Claude CLI (local only; CI keeps its `Install Claude CLI` step, row C12; this exercises the retire step's "`claude` not found" skip path, section 3.3): `env HOME=$T/ci UV_CACHE_DIR="$(uv cache dir)" PATH=<a PATH with no claude executable; confirm with command -v claude printing nothing> uv run --no-sync superclaude install && uv run --no-sync superclaude doctor --verbose` exits 0.
  7. `git status --short` shows no modified tracked file outside `$PKG`; `rm -rf "$T"`.
- Acceptance: every numbered check above passes, and `$PKG/artifacts/final/summary.md` lists each check with its command and observed result.
- Commit: `chore(tasks): Phase 1 final gate evidence (#323)`

**T15. Handoffs**
- Files: `$PKG/handoffs/<repo>.md` for the 11 repos in section 6.3 (text copied verbatim); `.dev/codegraph-migration/handoffs/phase2-facts-from-phase1.md` (section 6.2 facts plus the retire-step behaviour and section 7 table, for the Phase 2 Coder handoff, plus a section headed "Phase 2 override: Serena removal" that quotes Phase 2 spec §2.12 and names `codegraph_ready()`; Phase 2 T0b and T3b check for it); the slots ledger from T11a-T11c is re-checked to cover every touched step.
- Acceptance: `ls $PKG/handoffs/*.md | wc -l` prints 11; `test -s .dev/codegraph-migration/handoffs/phase2-facts-from-phase1.md && test -s .dev/codegraph-migration/handoffs/phase3-codegraph-slots.md`; `rg -q 'codegraph_ready' .dev/codegraph-migration/handoffs/phase2-facts-from-phase1.md`.
- Commit: `docs(tasks): Phase 1 handoff notes for Phase 2, Phase 3 and other IronbellyOrg repos (#323)`
- **Group G5 done:** final issue comment (states the merge constraint, section 2.2, and links the handoff files).

````
### .dev/tasks/to-do/TASK-WF-phase1RemovalSpe-20261029-185100/source.md:793-803

````markdown
## 9. Progress reporting

At each task-group commit (end of G0, G1, G2, G3, G4 and G5 in section 8; the G0 comment records the baseline counts) the executor posts one brief comment on issue #323 of the fork, and only there:

```bash
gh repo view --json nameWithOwner -q .nameWithOwner      # must print IronbellyOrg/IronClaude; otherwise run: gh repo set-default IronbellyOrg/IronClaude
gh issue comment 323 --repo IronbellyOrg/IronClaude --body "Phase 1 progress: <group id and name> committed on ironbelly/feat-codememory-codegraph-init at <short sha>. Tasks: <task ids>. Checks: <exact commands> -> <result, e.g. 412 passed>. Decisions logged: <count, path in task package>. Next: <next group>."
```

Rules: one comment per group (not per task); facts only (commit SHA, commands, pass counts, open problems); never `--repo SuperClaude-Org/...` and never a bare `gh issue comment` (gh can default to the upstream parent, see the project `CLAUDE.md` PR rule). If `gh` is not authenticated or the call fails, record the exact error and the intended body in the task package's `progress.md` and continue; this is not a blocker. The G5 comment also links the handoff files (T15) and states the merge constraint (section 2.2).

````
### .dev/tasks/to-do/TASK-WF-phase1RemovalSpe-20261029-185100/source.md:804-824

```markdown
## 10. Autonomy rules for the executor

The executor (`/sc:implement` on the plan that `/sc:workflow` builds from this spec) runs without gating on the user.

| Decision size | Meaning | Method | Record |
|---|---|---|---|
| Simple | one obvious option, or a choice this spec already constrains (wording, test names, exact line moves, file names inside an allowed folder) | decide yourself | one line in the task package `decisions.md`: decision, options, method `self`, rationale |
| Mid-level | two or more viable options with real trade-offs inside one task (for example how to port a test fixture, how to word a skill step's native fallback) | write each option to `<task package>/decisions/<task>-<slug>/option-<x>.md`, then spawn an agent that runs `/sc:adversarial --compare <option files> --depth quick`; follow its recommendation | `decisions.md` entry with method `adversarial quick` and the merged-recommendation path |
| Complex | an architectural change to this spec's design (retire-step scope, memory store layout, merge order, deleting a file this spec keeps) | same, without `--depth quick` (`/sc:adversarial --compare <option files>`) | `decisions.md` entry with method `adversarial full` |

Further rules:

- Never stop to ask the user and never pause for scope, cost or context reasons. A blocked task stays blocked with its reason written in `progress.md`; continue with tasks that do not depend on it.
- Follow section 8's order. A task may not need a later task to go green. If a task's acceptance command fails, fix within the task's files; if the fix needs a file another task owns, pull that edit forward and say so in `decisions.md`.
- Never run the real `./update.sh`, `superclaude install` or `claude mcp add/remove` against the real `HOME` during Phase 1; every environment check runs in a sandbox `HOME` (T14). Never delete user data (`~/.serena`, project `.serena/` outside this repo, `~/.cache/codebase-memory-mcp`).
- Never stage or commit `.claude/` content except `.claude/settings.json` (project `CLAUDE.md`); stage `.dev/tasks/` (the task package) with every commit.
- Full-suite runs always set `T02_15_PERF_REPORT=/tmp/p1-perf.json` so `tests/cli/eval/test_perf_home_setup.py` does not rewrite the tracked `.dev/releases/current/cliEval/evidence/T02.15/perf.json` (override at `test_perf_home_setup.py:122`); run `git status --short` after every test run and restore any tracked file a test changed.
- Do not open a pull request to `master` for Phase 1 alone (section 2.2); do not push to `upstream`.

Human intervention points: **none are required during Phase 1.** Two later actions belong to the user and are listed so the executor does not attempt them: (1) merging Phases 1 and 2 to `master` together (Phase 2's PR, via `/sc:pr-submit`); (2) running the real `./update.sh` on a live workspace after that merge, which removes the live registrations listed in 2.3. Phase 2 owns the commands, expected output and issue-#323 report for that post-merge live check (review finding X-5); Phase 1 runs none of it.

```
### .dev/tasks/to-do/TASK-WF-phase1RemovalSpe-20261029-185100/source.md:825-851

```markdown
## Decisions

Format per the run README: decision, options considered, method (self / adversarial quick / adversarial full), rationale. Option files and debate output for the two adversarial decisions are under `.dev/codegraph-migration/decisions/P1-*/`.

| ID | Decision | Options considered | Method | Rationale |
|---|---|---|---|---|
| D1 | Load-bearing Serena steps in primitives are triaged and deleted or rewritten to a native Grep/Read floor in Phase 1, with a codegraph slots ledger for Phase 3 (section 4) | A: rewrite all to a floor plus ledger; B: remove decorative only, defer load-bearing to Phase 3; C: delete the Serena tier where a fallback exists, no ledger | adversarial quick (`decisions/P1-primitive-gap-policy/adversarial/merged-recommendation.md`) | A 0.841, B 0.778, C 0.735, convergence 1.00. B leaves dangling steps on every commit and ties Phase 1 to Phase 3's unplanned merge; C silently drops capability where the fallback is "skip" and loses step locations. The merge kept C's delete-where-a-fallback-exists triage |
| D2 | Existing-workspace cleanup: a non-fatal retire step in `superclaude install` removes provably IronClaude-written `codebase-memory-mcp` and Tier R `serena` user registrations and IronClaude's receipt/marker; keeps the current-pin `serena` entry (Tier K), all binaries, uv tools, companions, indexes, caches and memories; read-only lines in `install --list`, `doctor` (warn only) and `update` (section 3) | A: registration-only step in install; B: A plus removal of binaries and the Serena uv tool; C: no automatic step, explicit consented command | adversarial full (`decisions/P1-existing-workspace-cleanup/adversarial/merged-recommendation.md`) | A 0.877, C 0.730, B 0.717; convergence 100%. C fails the goal on `./update.sh`; B removes Coder-owned software and runs a prompt-free account-wide uninstall. The merge hardened A's matchers by provenance (INV-001): the current Serena pin is byte-identical to Coder's bundle argv, so Phase 1 alone keeps and reports it, only until Phase 2's `codegraph_ready()` gate removes it (Phase 2 spec §2.12, decision D22; review finding X-4), with the Phase 2 Coder handoff stopping the bundle re-adding it (section 3.6). Data is kept per existing policy (`install_codebase_memory.py:74-78`) |
| D3 | Serena memory replacement: apply W2 decision D1 unchanged (section 5), including the one-release legacy read of `.serena/memories/` in `/sc:load`, allowlisted in 2.4 | re-decide; apply | self (applies an existing adversarial-quick decision) | The brief asks for the serena.md decision to be applied; re-running it would duplicate work. The legacy read conflicts with "no mention" only in one sentence per copy, which is allowlisted with a removal trigger |
| D4 | Delete the reflect contract field `serena_summary_corroboration` (keep the other reflect field names stable) | keep the field name with a constant value (gap-policy merged recommendation, "field names stay stable"); delete it (`inventory/serena.md` D2) | self, conflict resolved from code | The two decision records disagree. Code settles it: `rg -n 'summary_corroboration' src plugins` shows only producers (`ensemble.py:824`, reflect `SKILL.md:780`) and prose; `contract.py` never reads it. It reports Serena's `summarize_changes`, which Phase 1 deletes, so keeping it would leave a Serena-named field with no meaning and break DoD-1. Fields without "serena" in the name keep the merged recommendation's stable-name rule |
| D5 | Execution order puts the retire step (T3) right after detaching `superclaude install` (T2) and before detaching `superclaude mcp` (T4) and deleting the module (T5) | W1's order with the cleanup added after step 4; cleanup first | self | The retire step reuses `read_user_mcp_entry` and `_run_registration_command`; adding it before T4 means those helpers always have a caller and their behaviour stays tested |
| D6 | Phase 1 deletes `_native_registration_matches`, `_add_user_native_entry`, `_restore_user_native_entry`; Phase 2 restores parameterised versions from `55d40308` | keep them (unused) for Phase 2; delete them | self | Keeping code with no caller and no test is dead code; section 7 gives Phase 2 the exact baseline line ranges, and Phases 1 and 2 merge together |
| D7 | No "retired servers" section in user docs; the `CHANGELOG.md` entry and the retire step's printed output carry the manual commands | a docs subsection; CHANGELOG only | self | Keeps the DoD-1 search clean without another allowlist entry; `CHANGELOG.md` is already allowlisted history and is where a user looks for removals |
| D8 | Phase 1 runs every environment check in a sandbox `HOME`; the real `./update.sh` on a live workspace waits until Phases 1 and 2 merge | run `./update.sh` live in T14; sandbox only | self | `update.sh:7` runs `pipx install --force ./`, which would replace the user's global `superclaude` with a branch build that removes codebase-memory and installs no codegraph. The sandbox run exercises the same script (T14 step 5) |
| D9 | Phase 1 is not merged to `master` alone (section 2.2) | merge Phase 1 first; merge with Phase 2 | self (forced by a verified constraint) | Coder's monitor bumps to every `master` commit and its contract test asserts the codebase-memory registration (`research/install-update-flow.md` 5.2 row E) |
| D10 | Reflect refs `grader-extensions.md`, `ops-integration.md`, `reflection-rubric.md` move from T9 to T11 (now T11a), and the calibration file move from T13 to T10 (now T10b; split per D18) | keep the generated task mapping | self | They change together with the reflect `--onboard` and verification rewrite (T11) and the calibration memory path (T10); splitting them would leave references to removed steps between commits |
| D11 | Acceptance search = W2's pattern without `onboarding` (19 false positives) and `sc:save`/`sc:load` (the commands stay), plus the Serena-only names W2 missed, with word boundaries for names that prefix kept reflect fields; line-level allowlist for files that keep one legitimate mention | W2 pattern unchanged; file-level allowlist | self | W2's own decision D5 marks the `onboarding` hits false positives; a file-level allowlist for `load.md` or the registry test would hide a stray mention there |
| D12 | Full-suite runs set `T02_15_PERF_REPORT=/tmp/p1-perf.json` | restore `perf.json` after each run | self | The override exists for this purpose (`tests/cli/eval/test_perf_home_setup.py:33`, `:122`); restoring by hand is easy to forget |
| D13 | Delete the Serena `relative_path` branch of `freshness-pre-edit.sh` (rows D1, D2) | keep it as harmless | self | Only Serena's edit tools pass `relative_path` (W6 finding); with the matcher reduced to `Edit\|Write` the branch is unreachable code |
| D14 | Phase 1 cannot prove the CI change on GitHub; T14 checks locally that install and doctor pass without a Claude CLI (step 6), and the Phases 1+2 PR proves the `doctor-check` job in CI. Amended by review finding X-15: Phase 1 keeps the `Install Claude CLI` step and rewrites only its comments (row C12) | push and dispatch the workflow from Phase 1 | self | `test.yml:3-8` runs only for `master`/`integration` pushes and PRs (or a manual dispatch); pushing for CI is not needed to meet Phase 1's DoD and the merge happens with Phase 2 |
| D15 | Edit the hand-maintained `plugins/superclaude/` tree and the root `commands/`, `agents/` copies in the same commit as `src/superclaude/` | wait for an external sync | self (inherits `inventory/serena.md` D8) | Tests read the plugin copies; the root copies' generator is not in this repo |
| D16 | Phase 1 deletes no shipped primitive name, so no "retired primitive files" cleanup is needed in the installer | add a retired-assets delete list | self | Section 5 keeps `/sc:save`, `/sc:load` and every other command, agent and skill; MCP guides and configs are package data only (`~/.claude/mcp/` is not installed, `inventory/serena.md` 4.1) |
| D17 | Ownership of other-repo work: handoff notes only, per repo; the Coder part goes to Phase 2's Coder handoff | edit other repos; notes | self (brief and run rules) | The run forbids cross-repo edits; each note is self-contained so an owner can paste it |
| D18 | Split T10 into T10a (commands, agents, modes, pm protocol) and T10b (skills, routing guide, calibration move), and T11 into T11a (reflect), T11b (troubleshoot) and T11c (the rest, `core/CLAUDE.md:112`, ledger completion); repo-wide searches only on T10b and T11c (review finding X-12) | keep T10/T11 whole; the review's exact split (sc-pm-protocol in T10b; reflect-reviewer and reuse-auditor in T11c) | self (task F1, forced by rule G5 and source) | Rule G5 puts a roster change in the same commit as the skill body that drives it: reflect SKILL.md drives `reflect-reviewer` (its fixed reviewer type, SKILL.md section 7) and `reuse-auditor` (step 4a, Serena fallback at SKILL.md:563), and D4/D5 test `reflect-reviewer`, so both agents go to T11a. `src/superclaude/commands/pm.md:52` loads `sc:pm-protocol` and the M3 check lists its SKILL.md, so it goes to T10a with `/sc:pm` |
| D19 | Apply Phase 2 T0b now (review finding X-4): the current-pin Serena entry is kept by Phase 1 alone only until Phase 2's `codegraph_ready()` gate removes it; Tier R and Tier K match `env`/`headers` absent or `{}`; the re-register hint uses `serena-local`; Tier K prints "kept until codegraph is ready" | leave Phase 1 text and let Phase 2 T3b rewrite tests and CHANGELOG later | self (task F1; Phase 2 spec §2.12 is an adversarial-full decision, D22 there) | The live entry carries `"env":{}` (`jq '.mcpServers.serena.env' ~/.claude.json` prints `{}`), so the old "no env/headers" wording would keep Tier R shapes; implementing Phase 1 from the old text would pin tests and CHANGELOG to the opposite of Phase 2 §2.12 |
| D20 | Keep the CI `Install Claude CLI` step and rewrite only its comments (review finding X-15) | delete it in Phase 1 and restore it in Phase 2 | self (task F1) | Phases 1 and 2 merge as one unit (section 2.2) and Phase 2's required codegraph phase needs `claude --version` in `doctor-check` (Phase 2 spec F12, D9); delete-then-restore inside one merge is churn |

```
### .dev/tasks/to-do/TASK-WF-phase1RemovalSpe-20261029-185100/source.md:852-867

```markdown
## Review resolution

Applied by task F1 on 2026-10-29 from `.dev/codegraph-migration/review/review.md` (task R). Each finding was re-checked against the source before it was applied. Cross-phase findings: only the Phase 1 part was applied; no other phase's spec and no handoff file was edited (the Coder handoff files belong to F2).

| Finding | Result | Reason (one line) |
|---|---|---|
| X-4 (IMPORTANT) Phase 1 not amended to Phase 2's Serena gate (T0b) | applied | Verified: 0 hits for `codegraph_ready`/`serena-local` before the edit, live entry has `"env":{}`; DoD-3, DoD-4, §2.3, §3.1, §3.2 Tier R and Tier K, §3.4 hint (`serena-local`), §3.5 tests, §3.6, §6.2, T12 CHANGELOG, T14 step 5, T15 facts-file override and D2 amended (D19); Phase 2 T0b acceptance lines 437-440 pass |
| X-12 (IMPORTANT) T10 and T11 too big | applied, split adjusted | T10 -> T10a/T10b, T11 -> T11a/T11b/T11c with per-piece scoped checks and repo-wide checks on the last piece; `reflect-reviewer` and `reuse-auditor` moved to T11a and `sc-pm-protocol` to T10a, because rule G5 and `commands/pm.md:52` tie them to those bodies (D18) |
| X-15 (MINOR) CI step deleted by Phase 1 and re-added by Phase 2 | applied (Phase 1 hunk) | `test.yml:156-159` step kept, comments `:133-134` and `:155` rewritten (row C12, §7, T12 acceptance, T14 step 6 relabelled, D14, D20); Phase 2 T8 change left to F2 |
| X-16 (MINOR) T3 runs `install --list` on the real HOME | applied | T3 now runs `install --list` in a `mktemp -d` HOME, matching §10's ban on real-HOME installs |
| X-17 (MINOR) T5 search hits allowlisted retire-step files | applied | `-g` excludes for `install_retired_mcp.py` and its test added to T5's first search |
| X-24 (MINOR) Row S19 contradicts itself | applied | `docs/memory/pm_context.md:77` read: it is design history, so the row is "keep unchanged" (still allowlisted) |
| X-5 (IMPORTANT, owner F2) live "completely absent" check has no owner | applied (Phase 1 hunk only) | §10 now states Phase 2 owns the post-merge live check; the task itself is F2's |
| X-9 (IMPORTANT, owner F3) two phases write the core MCP row | no Phase 1 change | Phase 1 already deletes only `:21`, the `:90` item and rewrites `:112` (G10, §7), which is the ownership the review prescribes |
| X-6, X-7 (owner F3) Phase 3 ignores the floor and ledger | no Phase 1 change | Phase 1's G6 floor and G9 ledger are what the review asks Phase 3 to follow; T11c now also checks the ledger covers every §4.2 load-bearing file |
| (task F1 item 3) Every task-group commit point carries an issue-#323 comment | applied | §9 and T0 now include a G0 comment, so each of the six group commit points (G0-G5) has one |
```

## Coverage slice

Union coverage 0.7088 (241/340); full matrix `.dev/reflect/pre-phase1RemovalSpe-20261029185357/artifacts/coverage-matrix.yaml`, rows `.dev/reflect/pre-phase1RemovalSpe-20261029185357/artifacts/inferred-requirements.yaml`.

| Unmapped requirement | Spec citation | Triage |
|---|---|---|
| INF-001 | source.md:30 | row-ref C1 |
| INF-002 | source.md:31 | row-ref C2 |
| INF-003 | source.md:32 | row-ref C3 |
| INF-004 | source.md:33 | row-ref C4 |
| INF-005 | source.md:34 | row-ref C5 |
| INF-006 | source.md:35 | row-ref C6 |
| INF-007 | source.md:36 | row-ref C7 |
| INF-009 | source.md:37 | row-ref C8 |
| INF-010 | source.md:38 | row-ref C9 |
| INF-011 | source.md:39 | row-ref C10 |
| INF-012 | source.md:40 | row-ref C11 |
| INF-013 | source.md:41 | row-ref C12 |
| INF-015 | source.md:48 | section-ref §1.2 |
| INF-016 | source.md:52 | row-ref S1 |
| INF-023 | source.md:63 | row-ref S12 |
| INF-025 | source.md:67 | row-ref S16 |
| INF-026 | source.md:68 | row-ref S17 |
| INF-027 | source.md:71 | row-ref S20 |
| INF-028 | source.md:72 | row-ref S21 |
| INF-035 | source.md:79 | row-ref S28 |
| INF-038 | source.md:82 | row-ref S31 |
| INF-044 | source.md:92 | row-ref S41 |
| INF-046 | source.md:94 | row-ref S43 |
| INF-047 | source.md:95 | row-ref S44 |
| INF-048 | source.md:108 | row-ref S57 |
| INF-053 | source.md:135 | row-ref S84 |
| INF-057 | source.md:140 | row-ref S89 |
| INF-063 | source.md:152-178 | row-ref P1 |
| INF-064 | source.md:153 | row-ref P2 |
| INF-066 | source.md:155-190 | row-ref P4 |
| INF-067 | source.md:156-191 | row-ref P5 |
| INF-070 | source.md:159-198 | row-ref P8 |
| INF-076 | source.md:174-208 | row-ref P23 |
| INF-084 | source.md:200 | row-ref P49 |
| INF-091 | source.md:219-221 | row-ref P68 |
| INF-093 | source.md:224 | row-ref P73 |
| INF-100 | source.md:234 | row-ref P83 |
| INF-102 | source.md:236 | row-ref P85 |
| INF-103 | source.md:240 | row-ref P89 |
| INF-104 | source.md:242 | row-ref P91 |
| INF-108 | source.md:247 | row-ref P96 |
| INF-114 | source.md:261 | NO-REF |
| INF-115 | source.md:261 | NO-REF |
| INF-116 | source.md:267 | section-ref §2.2 |
| INF-119 | source.md:269 | section-ref §2.2 |
| INF-120 | source.md:270 | section-ref §2.2 |
| INF-122 | source.md:272 | section-ref §2.2 |
| INF-125 | source.md:279 | NO-REF |
| INF-129 | source.md:300 | section-ref §2.4 |
| INF-130 | source.md:301 | section-ref §2.4 |
| INF-131 | source.md:307 | section-ref §3.1 |
| INF-132 | source.md:307 | section-ref §3.1 |
| INF-133 | source.md:307 | section-ref §3.1 |
| INF-134 | source.md:313 | section-ref §3.2 |
| INF-138 | source.md:315 | section-ref §3.2 |
| INF-139 | source.md:319 | section-ref §3.2 |
| INF-140 | source.md:320 | section-ref §3.2 |
| INF-141 | source.md:321 | section-ref §3.2 |
| INF-143 | source.md:325 | section-ref §3.2 |
| INF-147 | source.md:327 | section-ref §3.2 |
| INF-148 | source.md:327 | section-ref §3.2 |
| INF-149 | source.md:331 | section-ref §3.3 |
| INF-150 | source.md:332 | section-ref §3.3 |
| INF-151 | source.md:333 | section-ref §3.3 |
| INF-152 | source.md:334 | section-ref §3.3 |
| INF-155 | source.md:337 | section-ref §3.3 |
| INF-156 | source.md:341 | section-ref §3.3 |
| INF-157 | source.md:342 | section-ref §3.3 |
| INF-158 | source.md:343 | section-ref §3.3 |
| INF-159 | source.md:344 | section-ref §3.3 |
| INF-162 | source.md:347 | section-ref §3.3 |
| INF-163 | source.md:351 | section-ref §3.4 |
| INF-164 | source.md:352 | section-ref §3.4 |
| INF-166 | source.md:354 | section-ref §3.4 |
| INF-167 | source.md:354 | section-ref §3.4 |
| INF-168 | source.md:354 | section-ref §3.4 |
| INF-169 | source.md:354 | section-ref §3.4 |
| INF-173 | source.md:361 | section-ref §3.5 |
| INF-176 | source.md:361 | section-ref §3.5 |
| INF-178 | source.md:362 | section-ref §3.5 |
| INF-180 | source.md:380 | section-ref §4 |
| INF-181 | source.md:388 | section-ref §4.1 |
| INF-183 | source.md:389 | section-ref §4.1 |
| INF-186 | source.md:391 | section-ref §4.1 |
| INF-187 | source.md:392 | section-ref §4.1 |
| INF-188 | source.md:392 | section-ref §4.1 |
| INF-191 | source.md:394 | section-ref §4.1 |
| INF-195 | source.md:396 | section-ref §4.1 |
| INF-199 | source.md:406 | section-ref §4.3 |
| INF-200 | source.md:410 | section-ref §5 |
| INF-208 | source.md:421 | section-ref §5 |
| INF-211 | source.md:423 | section-ref §5 |
| INF-213 | source.md:449 | section-ref §6.1 |
| INF-216 | source.md:457 | section-ref §6.3 |
| INF-221 | source.md:509 | section-ref §6.3 |
| INF-231 | source.md:627 | section-ref §8.0 |
| INF-270 | source.md:712 | row-ref S4 |
| INF-276 | source.md:725 | section-ref §8 |
| INF-329 | source.md:806 | section-ref §10 |

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

# Research 04: Conventions, Contract, and MDTM Template

Status: Complete

## 1. MDTM Template 02 structure and task-shaping rules

### Template identity and intended use

- Template 02 is a complex-task template: PART 1 says it "Extends Template 01 with Section L: Intra-Task Handoff Patterns" and should be used when tasks require "discovery, testing, review, conditional logic, or aggregation between checklist items" (`/config/workspace/IronClaude/.claude/worktrees/ReflectGateWiring/.claude/templates/workflow/02_mdtm_template_complex_task.md:77-80`).
- The generated output copies PART 2 plus frontmatter: PART 2 says to copy from `# [Task Title]` to the end and that the top frontmatter is also part of the template (`/config/workspace/IronClaude/.claude/worktrees/ReflectGateWiring/.claude/templates/workflow/02_mdtm_template_complex_task.md:1143-1151`).

### Required generated sections

Template 02's output skeleton includes these required sections and structures:

1. Frontmatter with task metadata, including status, type, priority, `spec_path`, `reflect_pre`, `reflect_post`, related docs, tags, `template_schema_doc`, and `task_type` (`/config/workspace/IronClaude/.claude/worktrees/ReflectGateWiring/.claude/templates/workflow/02_mdtm_template_complex_task.md:1-61`).
2. `# [Task Title]`, `## Task Overview`, and `## Key Objectives` (`/config/workspace/IronClaude/.claude/worktrees/ReflectGateWiring/.claude/templates/workflow/02_mdtm_template_complex_task.md:1157-1169`).
3. `## Prerequisites & Dependencies`, including parent task, blocking dependencies, blocked-by relationships, and mandatory previous-stage outputs (`/config/workspace/IronClaude/.claude/worktrees/ReflectGateWiring/.claude/templates/workflow/02_mdtm_template_complex_task.md:1171-1191`).
4. `## Execution Context` with references, source areas, key constraints, handoff-file convention, and frontmatter update protocol (`/config/workspace/IronClaude/.claude/worktrees/ReflectGateWiring/.claude/templates/workflow/02_mdtm_template_complex_task.md:1193-1231`).
5. `## Detailed Task Instructions` with phases, starting with `### Phase 1: Preparation and Setup`, then task-specific execution phases (`/config/workspace/IronClaude/.claude/worktrees/ReflectGateWiring/.claude/templates/workflow/02_mdtm_template_complex_task.md:1233-1359`).
6. Phase-gate QA section when applicable, using M3 lens-based QA and serialized fixes (`/config/workspace/IronClaude/.claude/worktrees/ReflectGateWiring/.claude/templates/workflow/02_mdtm_template_complex_task.md:1365-1402`).
7. Testing and verification phase for code-modifying tasks (`/config/workspace/IronClaude/.claude/worktrees/ReflectGateWiring/.claude/templates/workflow/02_mdtm_template_complex_task.md:1404-1410`).
8. Review/quality phase (`/config/workspace/IronClaude/.claude/worktrees/ReflectGateWiring/.claude/templates/workflow/02_mdtm_template_complex_task.md:1412-1421`).
9. `## Post-Completion Actions`, including output existence verification, relevant test rerun if source code changed, mandatory post-completion lens QA, optional source-fidelity gate, task summary, and final frontmatter update (`/config/workspace/IronClaude/.claude/worktrees/ReflectGateWiring/.claude/templates/workflow/02_mdtm_template_complex_task.md:1423-1441`).
10. `## Task Log / Notes` with task summary, execution log, phase findings, QA gate findings, follow-up items, and deviations sections (`/config/workspace/IronClaude/.claude/worktrees/ReflectGateWiring/.claude/templates/workflow/02_mdtm_template_complex_task.md:1443-1515`).

### B2 self-contained item pattern

- B2 requires every checklist item to be a complete self-contained prompt with six elements: context reference with why, action with why, output specification, integrated verification, evidence on failure only, and explicit completion gate (`/config/workspace/IronClaude/.claude/worktrees/ReflectGateWiring/.claude/templates/workflow/02_mdtm_template_complex_task.md:159-166`).
- B3 requires each checklist item to be one full paragraph that can execute independently without prior context (`/config/workspace/IronClaude/.claude/worktrees/ReflectGateWiring/.claude/templates/workflow/02_mdtm_template_complex_task.md:167-170`).
- B4 explicitly forbids separate verification items because verification belongs in the action item's "ensuring..." clause; QA happens between batches (`/config/workspace/IronClaude/.claude/worktrees/ReflectGateWiring/.claude/templates/workflow/02_mdtm_template_complex_task.md:177-179`).
- C1-C3 repeat that outputs, success criteria, and verification are embedded in checklist items, not emitted as separate sections (`/config/workspace/IronClaude/.claude/worktrees/ReflectGateWiring/.claude/templates/workflow/02_mdtm_template_complex_task.md:223-240`).

### Granularity, ordering, and anti-orphaning rules

- A3 requires every workflow phase to be broken into atomic, verifiable checklist items, with exact file paths, specific requirements, and measurable outcomes; high-level or bulk operations are forbidden (`/config/workspace/IronClaude/.claude/worktrees/ReflectGateWiring/.claude/templates/workflow/02_mdtm_template_complex_task.md:108-113`).
- E1 requires flat, ordered, atomic checkboxes, with Step headers used for grouping and no parent checkboxes (`/config/workspace/IronClaude/.claude/worktrees/ReflectGateWiring/.claude/templates/workflow/02_mdtm_template_complex_task.md:295-310`).
- E2 and E3 prevent orphaned or backward-dependent items by requiring summary checkboxes after component items and top-to-bottom completion only (`/config/workspace/IronClaude/.claude/worktrees/ReflectGateWiring/.claude/templates/workflow/02_mdtm_template_complex_task.md:311-382`).
- F1 defines executor behavior as READ → IDENTIFY → EXECUTE → UPDATE → REPEAT, completing only the first unchecked item before re-reading (`/config/workspace/IronClaude/.claude/worktrees/ReflectGateWiring/.claude/templates/workflow/02_mdtm_template_complex_task.md:411-420`).
- F2 prohibits skipping phase-gate QA and post-completion validation; F2a explains that multi-item execution in one session causes context overflow, lost progress, and state drift (`/config/workspace/IronClaude/.claude/worktrees/ReflectGateWiring/.claude/templates/workflow/02_mdtm_template_complex_task.md:422-445`).
- C4/I13 make task completion a final Post-Completion Actions concern, not a separate body section, and require frontmatter update plus execution-log summary after validation (`/config/workspace/IronClaude/.claude/worktrees/ReflectGateWiring/.claude/templates/workflow/02_mdtm_template_complex_task.md:242-247`, `/config/workspace/IronClaude/.claude/worktrees/ReflectGateWiring/.claude/templates/workflow/02_mdtm_template_complex_task.md:616-621`).

### QA gate, testing, and complex-task handoff features

- Template 02's complex feature is Section L: handoff files under `.dev/tasks/TASK-NAME/phase-outputs/`, with `discovery/`, `test-results/`, `reviews/`, `plans/`, and `reports/` subdirectories that persist across batches and session rollovers (`/config/workspace/IronClaude/.claude/worktrees/ReflectGateWiring/.claude/templates/workflow/02_mdtm_template_complex_task.md:902-921`).
- L-patterns define discovery, build-from-discovery, test/execute, review/QA, conditional action, and aggregation item types (`/config/workspace/IronClaude/.claude/worktrees/ReflectGateWiring/.claude/templates/workflow/02_mdtm_template_complex_task.md:928-1012`).
- I18 requires at least one testing checklist item for source-code changes; it must specify the test command, pass criteria, result capture location, and follow B2 (`/config/workspace/IronClaude/.claude/worktrees/ReflectGateWiring/.claude/templates/workflow/02_mdtm_template_complex_task.md:688-695`).
- I15 requires phase-gate QA for any task with 2+ execution phases, and each QA spawn item must include agent type, lens, inputs, output report path, `fix_authorization: false`, and adversarial framing (`/config/workspace/IronClaude/.claude/worktrees/ReflectGateWiring/.claude/templates/workflow/02_mdtm_template_complex_task.md:635-651`).
- I16/I20 require serialized fix cycles: report-only lens agents, consolidated findings, one fix agent with `fix_authorization: true`, then verification agents; parallel fix authorization is prohibited (`/config/workspace/IronClaude/.claude/worktrees/ReflectGateWiring/.claude/templates/workflow/02_mdtm_template_complex_task.md:653-673`, `/config/workspace/IronClaude/.claude/worktrees/ReflectGateWiring/.claude/templates/workflow/02_mdtm_template_complex_task.md:745-757`).
- I17 requires post-completion validation before marking Done, including all items checked, expected output files present, blockers resolved, tests for source-code changes, mandatory lens-based QA, and source-fidelity validation when applicable (`/config/workspace/IronClaude/.claude/worktrees/ReflectGateWiring/.claude/templates/workflow/02_mdtm_template_complex_task.md:675-686`).

## 2. Project conventions that task items must honor

### Source-of-truth and `.claude/` staging constraints

- The global convention says `src/superclaude/` is the source of truth for distributable components, while `.claude/` contains dev copies synced from `src/` (`/config/.claude/CLAUDE.md:14-29`).
- The global sync rule is explicit: edit `src/superclaude/` first, then run `make sync-dev`; if `.claude/` was edited directly, copy back to `src/superclaude/` and run `make verify-sync` (`/config/.claude/CLAUDE.md:45-48`).
- The project-level rule is stronger: `.claude/{skills,commands,agents,hooks,templates}/*` is gitignored sync-dev output, only `.claude/settings.json` is tracked, and staging `.claude/` mirror paths is prohibited (`/config/workspace/IronClaude/.claude/worktrees/ReflectGateWiring/CLAUDE.md:16-29`).
- The project-level rationale says committing `.claude/skills/...` beside `src/superclaude/skills/...` creates double diffs and breaks `make verify-sync`; if `git add` needs `-f` for `.claude/`, stop and move the change to `src/superclaude/` first (`/config/workspace/IronClaude/.claude/worktrees/ReflectGateWiring/CLAUDE.md:27-31`).
- Task implication: any fix to reflect skill/protocol sources must edit `/config/workspace/IronClaude/.claude/worktrees/ReflectGateWiring/src/superclaude/...` first, then run `make sync-dev` and `make verify-sync`; task items must not tell the executor to stage `.claude/` mirrors.

### UV-only Python and pytest conventions

- The global CLAUDE file requires UV for all Python operations and forbids `python -m`, `pip install`, or direct `python script.py` (`/config/.claude/CLAUDE.md:3-12`).
- The project CLAUDE file repeats the UV-only rule and lists `uv run pytest`, `uv run pytest tests/pm_agent/`, `uv pip install`, and `uv run python script.py` as required command forms (`/config/workspace/IronClaude/.claude/worktrees/ReflectGateWiring/CLAUDE.md:5-7`, `/config/workspace/IronClaude/.claude/worktrees/ReflectGateWiring/CLAUDE.md:62-70`).
- Tests live under `tests/` in the project structure (`/config/workspace/IronClaude/.claude/worktrees/ReflectGateWiring/CLAUDE.md:93-95`), and common test commands are `make test`, `uv run pytest tests/pm_agent/ -v`, `uv run pytest tests/test_file.py -v`, and marker-based pytest invocations (`/config/workspace/IronClaude/.claude/worktrees/ReflectGateWiring/CLAUDE.md:109-114`).
- Task implication: verification items must use `uv run pytest ...` forms, never bare `python -m pytest`; if they execute scripts, they must use `uv run python ...`.

### Lint/format conventions

- Project CLAUDE says `make lint` runs the ruff linter and `make format` formats code with ruff (`/config/workspace/IronClaude/.claude/worktrees/ReflectGateWiring/CLAUDE.md:116-119`).
- The Makefile confirms `make lint` runs `uv run ruff check .` and `make format` runs `uv run ruff format .` (`/config/workspace/IronClaude/.claude/worktrees/ReflectGateWiring/Makefile:47-55`).
- CI separately runs `ruff check src/ tests/` and `ruff format --check src/ tests/` (`/config/workspace/IronClaude/.claude/worktrees/ReflectGateWiring/.github/workflows/test.yml:131-137`).
- The project memory explicitly warns that `make lint` is not sufficient for CI format parity: `make lint` only runs `ruff check`, while CI separately runs `ruff format --check src/ tests/` (`/config/.claude/projects/-config-workspace-IronClaude/memory/MEMORY.md:9`).
- Task implication: a green task should run both `make lint` or an equivalent ruff-check path and `uv run ruff format --check src/ tests/` before claiming CI-style code quality is green.

### Git and PR target conventions

- Project CLAUDE defines the branch model as `master` production, `integration` testing, and feature/fix/docs branches; the standard workflow is create a branch, develop with tests, commit conventionally, then merge through integration to master (`/config/workspace/IronClaude/.claude/worktrees/ReflectGateWiring/CLAUDE.md:243-252`).
- Project CLAUDE warns that parallel Claude sessions should use git worktrees for independent working directories and no branch-switching conflicts (`/config/workspace/IronClaude/.claude/worktrees/ReflectGateWiring/CLAUDE.md:256-274`).
- PRs must target the fork: `origin` is `IronbellyOrg/IronClaude`, `upstream` is `SuperClaude-Org/SuperClaude_Framework`, and a bare `gh pr create` is forbidden because it can default to the parent repo (`/config/workspace/IronClaude/.claude/worktrees/ReflectGateWiring/CLAUDE.md:35-44`).
- The mandatory PR command shape includes `gh pr create --repo IronbellyOrg/IronClaude --base master --head <branch> ...`, and pre-PR checks require `git remote -v`, `git fetch origin && git log master..origin/master`, and verifying the returned URL is `https://github.com/IronbellyOrg/IronClaude/pull/N` (`/config/workspace/IronClaude/.claude/worktrees/ReflectGateWiring/CLAUDE.md:46-56`).
- Task implication: if the corrective task includes final git/PR instructions, they must not stage `.claude/` mirrors, must use the fork repo explicitly, and must account for worktree isolation if concurrent sessions are active.

## 3. Authoritative marker semantics and contract fit

### Contract §3 text

The authoritative marker is `SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE` (`/config/workspace/IronClaude/.claude/worktrees/reflectWrapper/.dev/handoffs/reflect-wrapper-contract.md:76-79`). The contract states:

> **Why it exists.** When the wrapper auto-fixes (O1 `--fix`), it auto-runs the
> remediation MDTM file that reflect authored via `task-builder`. That remediation
> tasklist ALSO carries an O1 terminal gate → without a breaker, the gate re-invokes
> the wrapper → reflect → new remediation → … forever.
> (`/config/workspace/IronClaude/.claude/worktrees/reflectWrapper/.dev/handoffs/reflect-wrapper-contract.md:80-83`)

The wrapper-side semantics state:

> **Wrapper (primary breaker):** `superclaude reflect run` reads the marker at
> startup. If it equals `"1"`, the wrapper **immediately exits 0** ("nested gate
> suppressed") before any audit. The wrapper EXPORTS `SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE=1`
> into the environment of every child it spawns inside the fix subtree (the
> reflect audit subprocess AND every auto-run `/task`). This alone terminates
> the recursion; the outer wrapper owns the real re-verification.
> (`/config/workspace/IronClaude/.claude/worktrees/reflectWrapper/.dev/handoffs/reflect-wrapper-contract.md:87-92`)

The generator-side obligations state:

> **Generators (obligations):**
> - MUST NOT clear, unset, or overwrite `SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE`.
> - SHOULD additionally **skip emitting / skip executing** the gate when the
>   marker is already `"1"` at gate time (belt-and-suspenders). A safe emission
>   shape:
> (`/config/workspace/IronClaude/.claude/worktrees/reflectWrapper/.dev/handoffs/reflect-wrapper-contract.md:94-99`)

The safe gate-emission shape is:

> `if [ "${SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE:-0}" = "1" ]; then`
> `  echo "reflect-wrapper recursion breaker: nested gate suppressed"; exit 0`
> `fi`
> `superclaude reflect run <FILE> --depth deep --fix [--promote|--no-promote --base <SHA>]`
> (`/config/workspace/IronClaude/.claude/worktrees/reflectWrapper/.dev/handoffs/reflect-wrapper-contract.md:99-104`)

The truthy value rule is exact: only string `"1"` suppresses normal run; absent, empty, or any other value means not suppressed (`/config/workspace/IronClaude/.claude/worktrees/reflectWrapper/.dev/handoffs/reflect-wrapper-contract.md:107-108`).

### Marker scope from the remediation handoff

- The remediation handoff distinguishes headless non-interactive `claude --print` from the recursion-breaker marker; `--print` is the headless signal, while `SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE` is "the nested-gate suppressor" (`/config/workspace/IronClaude/.claude/worktrees/ReflectGateWiring/src/superclaude/skills/sc-reflect-protocol/refs/remediation-handoff.md:115-119`).
- The same handoff preserves the invariant that reflect authors remediation but never executes `/task`; only authoring auto-accept changes under `--print`, not the execution gate (`/config/workspace/IronClaude/.claude/worktrees/ReflectGateWiring/src/superclaude/skills/sc-reflect-protocol/refs/remediation-handoff.md:123-130`).

### Does the contract sanction marker leakage into ordinary verification pytest subprocesses?

- Intended functional scope: the marker exists to suppress nested reflect-gate recursion, specifically the remediation tasklist's terminal O1 gate re-invoking wrapper → reflect → remediation forever (`/config/workspace/IronClaude/.claude/worktrees/reflectWrapper/.dev/handoffs/reflect-wrapper-contract.md:80-83`). The handoff independently labels the marker as the "nested-gate suppressor," not the headless signal (`/config/workspace/IronClaude/.claude/worktrees/ReflectGateWiring/src/superclaude/skills/sc-reflect-protocol/refs/remediation-handoff.md:115-119`).
- Current written scope is broader than the intended functional scope: the wrapper exports the marker to every child in the fix subtree, including the reflect audit subprocess and every auto-run `/task` (`/config/workspace/IronClaude/.claude/worktrees/reflectWrapper/.dev/handoffs/reflect-wrapper-contract.md:87-92`).
- Current generator obligation is stricter still: generators "MUST NOT clear, unset, or overwrite" the marker (`/config/workspace/IronClaude/.claude/worktrees/reflectWrapper/.dev/handoffs/reflect-wrapper-contract.md:94-96`).
- Therefore, the existing §3 text does **not** explicitly sanction stripping the marker for ordinary verification commands. It can be read as forbidding a generator/executor from clearing it, even when the child command is a non-reflect verification subprocess.
- The proposed fix still aligns with the contract's intended behavior if it strips the marker only for ordinary verification command subprocesses and preserves it for reflect audits, emitted reflect gates, and `/task` auto-run contexts. That preserves nested-gate suppression because the safe gate-emission check and wrapper startup suppression still see `SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE=1` (`/config/workspace/IronClaude/.claude/worktrees/reflectWrapper/.dev/handoffs/reflect-wrapper-contract.md:87-104`).

### Recommendation: amend §3.2 / generator obligations with a verification-strip carve-out

The corrective task should include a one-line contract amendment to remove ambiguity. Recommended clause to add immediately after the generator `MUST NOT clear...` bullet in §3:

> Exception: executors MAY remove `SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE` only from ordinary verification/build/test subprocess environments that cannot emit or execute reflect gates; they MUST preserve it for reflect audits, reflect gate commands, and auto-run `/task` execution so nested-gate suppression remains intact.

Rationale: without this clause, line 95's "MUST NOT clear" conflicts with the planned verification-only strip (`/config/workspace/IronClaude/.claude/worktrees/reflectWrapper/.dev/handoffs/reflect-wrapper-contract.md:94-96`); with the clause, the contract matches the marker's documented purpose as a nested-gate suppressor (`/config/workspace/IronClaude/.claude/worktrees/reflectWrapper/.dev/handoffs/reflect-wrapper-contract.md:80-92`, `/config/workspace/IronClaude/.claude/worktrees/ReflectGateWiring/src/superclaude/skills/sc-reflect-protocol/refs/remediation-handoff.md:115-119`).

## 4. Corrective task POST-gate self-recursion risk

- The task-builder final-phase pattern defines the canonical POST gate as an independent wrapper shell-out: `superclaude reflect run {TASK_FILE} --depth deep --fix --promote`; it says the wrapper runs POST audit in a disjoint `claude --print` subprocess and, with `--fix`, runs a bounded audit→apply→re-verify loop before writing `reflect_post` itself (`/config/workspace/IronClaude/.claude/worktrees/ReflectGateWiring/src/superclaude/skills/task-builder/SKILL.md:2200-2205`).
- That same pattern embeds the §3.2 skip guard, so when `SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE=1`, a nested gate exits 0 with "nested gate suppressed" instead of re-entering the wrapper (`/config/workspace/IronClaude/.claude/worktrees/ReflectGateWiring/src/superclaude/skills/task-builder/SKILL.md:2202`). This matches the contract's safe gate shape (`/config/workspace/IronClaude/.claude/worktrees/reflectWrapper/.dev/handoffs/reflect-wrapper-contract.md:99-104`).
- Self-recursion/leak risk for this corrective task: before the fix lands, a wrapper auto-fix run that reaches the task-builder §6.1 step 5.5 verification subprocess can still inherit `SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE=1` into ordinary pytest verification; the marker should suppress reflect gates, not ordinary verification (`/config/workspace/IronClaude/.claude/worktrees/reflectWrapper/.dev/handoffs/reflect-wrapper-contract.md:80-92`, `/config/workspace/IronClaude/.claude/worktrees/ReflectGateWiring/src/superclaude/skills/sc-reflect-protocol/refs/remediation-handoff.md:115-119`).
- Recommendation: do **not** place the POST reflect gate before the implementation and verification-strip tests. Put it after the fix, sync, targeted tests, `make lint`, `uv run ruff format --check src/ tests/`, and `make verify-sync` have passed, and treat the POST gate as the end-to-end dogfood proof that the wrapper can audit/fix/re-verify without leaking the marker into ordinary verification subprocesses.
- If the task must be executed under the current broken wrapper before the fix has landed, the task should explicitly document a temporary risk-control choice: either defer the POST wrapper gate until after the verification-strip fix is in place, or run the final wrapper gate only as the dogfood proof after all verification-strip tests pass. This is preferable to disabling verification because the wrapper contract says only exit 0 may let the tasklist/phase complete (`/config/workspace/IronClaude/.claude/worktrees/reflectWrapper/.dev/handoffs/reflect-wrapper-contract.md:63-72`).
- Additional convention caveat: the generic task-builder POST pattern says to stage artifacts with `git add -A` before audit (`/config/workspace/IronClaude/.claude/worktrees/ReflectGateWiring/src/superclaude/skills/task-builder/SKILL.md:2202`), but this project forbids staging `.claude/skills`, `.claude/commands`, `.claude/agents`, `.claude/hooks`, and `.claude/templates` mirrors (`/config/workspace/IronClaude/.claude/worktrees/ReflectGateWiring/CLAUDE.md:20-29`). The corrective task should override the generic staging instruction by specifying selective staging of source/test/contract files only, never `.claude/` mirrors.

## 5. Task-builder recommendations for this corrective MDTM

1. Use Template 02 because the task needs code changes, test execution, contract-document update, sync verification, and a final POST wrapper dogfood gate; Template 02 is for discovery/testing/review/conditional/aggregation tasks (`/config/workspace/IronClaude/.claude/worktrees/ReflectGateWiring/.claude/templates/workflow/02_mdtm_template_complex_task.md:77-80`, `/config/workspace/IronClaude/.claude/worktrees/ReflectGateWiring/.claude/templates/workflow/02_mdtm_template_complex_task.md:902-927`).
2. Every implementation/test/contract item must be one self-contained B2 paragraph, embedding the exact source file(s), why they are read, exact action, exact output or modified file, integrated verification, failure-only notes, and completion gate (`/config/workspace/IronClaude/.claude/worktrees/ReflectGateWiring/.claude/templates/workflow/02_mdtm_template_complex_task.md:159-166`).
3. Include a contract-update item that edits `/config/workspace/IronClaude/.claude/worktrees/reflectWrapper/.dev/handoffs/reflect-wrapper-contract.md` §3 to add the verification-strip carve-out, because the current generator obligation says `MUST NOT clear, unset, or overwrite` the marker (`/config/workspace/IronClaude/.claude/worktrees/reflectWrapper/.dev/handoffs/reflect-wrapper-contract.md:94-96`).
4. Include verification commands using UV and CI-parity formatting: targeted pytest via `uv run pytest ...`, lint via `make lint` or equivalent, `uv run ruff format --check src/ tests/`, and sync checks via `make sync-dev` plus `make verify-sync` (`/config/workspace/IronClaude/.claude/worktrees/ReflectGateWiring/CLAUDE.md:62-70`, `/config/workspace/IronClaude/.claude/worktrees/ReflectGateWiring/CLAUDE.md:121-123`, `/config/workspace/IronClaude/.claude/worktrees/ReflectGateWiring/.github/workflows/test.yml:131-137`).
5. Encode the final POST gate as an explicit wrapper-shell-out/dogfood item after all implementation and test items, preserving the recursion-breaker guard while ensuring ordinary verification subprocesses run with the marker stripped (`/config/workspace/IronClaude/.claude/worktrees/ReflectGateWiring/src/superclaude/skills/task-builder/SKILL.md:2200-2205`).

## Summary

- Template 02 requires self-contained, one-paragraph, B2 checklist items with integrated verification, exact file paths, and forward-only execution.
- Project conventions require source-first edits under `src/superclaude/`, `make sync-dev`, `make verify-sync`, UV-only Python commands, pytest under `tests/`, ruff check plus ruff format-check for CI parity, no staged `.claude/` mirrors, and fork-targeted PR commands.
- The marker's authoritative purpose is nested reflect-gate suppression. The current contract text is broad enough to conflict with a verification-only strip, so the corrective task should amend §3 with a narrow verification/build/test subprocess carve-out while preserving marker propagation for reflect audits, reflect gate commands, and auto-run `/task` execution.
- The corrective task's POST gate should run after the fix as an end-to-end dogfood proof, not before the fix; if execution happens under the broken wrapper, defer the POST gate until the verification-strip tests pass rather than letting the same leak invalidate verification.

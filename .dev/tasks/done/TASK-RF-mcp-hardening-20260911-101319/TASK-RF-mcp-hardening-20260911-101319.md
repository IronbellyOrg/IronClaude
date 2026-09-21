---
id: "TASK-RF-mcp-hardening-20260911-101319"
title: "Harden Verified MCP Installer Commands"
description: "Apply verified MCP installer command pins, preserve established MCP client namespaces, align active project documentation and focused tests, and validate source/mirror integrity without expanding into excluded legacy or user configuration surfaces."
version: "1.0"
status: "Archived"
type: "⚙️ Maintenance"
priority: "🔼 High"
created_date: "2026-09-11"
updated_date: "2026-09-11"
assigned_to: "rf-task-executor"
autogen: false
autogen_method: "rf-task-builder-template-02"
coordinator: "rf-team-lead"
parent_doc: ""
parent_task: ""
depends_on: []
spec_path: ""
reflect_pre:
  verdict: "skipped"
  coverage_pct: null
  depth: "standard"
  tcs: 0
  run_id: ""
  report: ""
  reviewed_at: ""
reflect_post: ""
related_docs:
- path: ".dev/tasks/to-do/TASK-RF-mcp-hardening-20260911-101319/research/08-scope-dispositions.md"
  description: "Authoritative bounded command, documentation, and baseline dispositions"
- path: ".dev/tasks/to-do/TASK-RF-mcp-hardening-20260911-101319/qa/qa-research-depth-report.md"
  description: "Residual documentation and Tavily scan risks to resolve before edits"
- path: ".dev/tasks/to-do/TASK-RF-mcp-hardening-20260911-101319/qa/analyst-completeness-report.md"
  description: "Final implementation-ready evidence and validation requirements"
related_prd: ""
related_tdd: ""
tags:
- "mcp"
- "installer"
- "hardening"
- "maintenance"
template_schema_doc: ".claude/templates/workflow/02_mdtm_template_complex_task.md"
estimation: "medium"
sprint: ""
due_date: ""
start_date: "2026-09-11"
completion_date: ""
blocker_reason: ""
ai_model: ""
model_settings: ""
review_info:
  last_reviewed_by: ""
  last_review_date: ""
  next_review_date: ""
task_type: dynamic
---

# Harden Verified MCP Installer Commands

## Archive disposition — 2026-09-21

Implementation merged in IronbellyOrg/IronClaude PR #226. This record is archived under `done/` to remove it from active work, not to certify completion of its execution protocol. The original record said Doing; final QA/completion bookkeeping remains incomplete. Unchecked items and historical validation results are preserved, not retroactively marked passed.

The complete original directory, including raw logs and exit files omitted from Git, is preserved locally at `/config/IronClaude-cleanup-20260921-1454/uncommitted-artifacts/.dev/tasks/to-do/TASK-RF-mcp-hardening-20260911-101319/`. Historical `to-do/` paths below refer to that original layout; retained Markdown records now live beside this task under `done/`. This local backup is not distributed with the repository.

## Task Overview

Apply only the verified MCP installer hardening: update the five bounded registry command/version contracts, preserve the `morphllm-fast-apply` registry key/name and the root `auggie-mcp` key, replace the root Auggie launcher, and align each active project-owned source/document command literal located by the bounded scan. The work prevents floating or deprecated launchers while retaining existing CLI selectors, registration reconciliation, and tool namespaces.

The task begins with release-command re-verification and a scoped command-literal inventory because research QA identified residual documentation and Tavily-literal scan risks. It excludes user/machine configuration, aliases or registration deletion, hooks/eval namespace migration, packaged-template/plugin consolidation, and the named unrelated MCP integrations.

## Key Objectives

1. **Harden the runtime registry:** Pin Tavily, Sequential Thinking, Serena, and Auggie installation metadata; replace the deprecated Morph launcher while retaining stable client identities.
2. **Preserve project compatibility:** Change only root `.mcp.json` Auggie executable tokens while retaining `auggie-mcp`, `stdio`, and empty `env`.
3. **Align active publications and tests:** Repair every current literal discovered by the bounded scan, add focused registry/root-config contracts, and validate through UV plus baseline-aware sync verification.

## Prerequisites & Dependencies

### Parent Task & Dependencies
- **Parent Task:** None — standalone bounded maintenance task.
- **Blocking Dependencies:** None — research and QA evidence are present in this task directory.
- **This task blocks:** Downstream MCP installer release work requiring stable command contracts.

### Previous Stage Outputs (MANDATORY INPUTS)

**INFORMATIONAL ONLY - NO CHECKLIST ITEMS HERE**

**Required Previous Stage Outputs:**
- **Release and command evidence:** `.dev/tasks/to-do/TASK-RF-mcp-hardening-20260911-101319/research/03-official-releases.md`, `05-serena-launcher-gap-fill.md`, and `06-morph-migration-gap-fill.md` — exact upstream command/version decisions to re-verify before edits.
- **Scope and ownership evidence:** `.dev/tasks/to-do/TASK-RF-mcp-hardening-20260911-101319/research/07-config-ownership-gap-fill.md` and `08-scope-dispositions.md` — retained namespace and excluded-surface boundaries.
- **QA residual-risk evidence:** `.dev/tasks/to-do/TASK-RF-mcp-hardening-20260911-101319/qa/qa-research-depth-report.md`, `qa-research-evidence-report.md`, and `qa-research-gap-report.md` — preliminary-scan risks and evidence limitations to resolve.

## Execution Context

### References
- **R-001:** `.dev/tasks/to-do/TASK-RF-mcp-hardening-20260911-101319/research/03-official-releases.md` — primary release versions and upstream source URLs.
- **R-002:** `.dev/tasks/to-do/TASK-RF-mcp-hardening-20260911-101319/research/05-serena-launcher-gap-fill.md` — verified Serena v1.7.0 launcher.
- **R-003:** `.dev/tasks/to-do/TASK-RF-mcp-hardening-20260911-101319/research/06-morph-migration-gap-fill.md` — retained-name Morph successor decision.
- **R-004:** `.dev/tasks/to-do/TASK-RF-mcp-hardening-20260911-101319/research/08-scope-dispositions.md` — bounded source/docs disposition and sync baseline policy.
- **R-005:** `.dev/tasks/to-do/TASK-RF-mcp-hardening-20260911-101319/qa/qa-research-depth-report.md` — residual docs/test scan concerns.

### Source Areas
- `src/superclaude/cli/install_mcp.py`: authoritative `MCP_SERVERS` runtime registry and same-name command reconciliation.
- `.mcp.json`: project-owned Auggie runtime configuration whose `auggie-mcp` key preserves the tool namespace.
- `tests/cli/` and `tests/docs/`: focused registry, root-config, and Tavily alignment contracts.
- `src/superclaude/mcp/` and `docs/`: project-owned active MCP publication surfaces subject to the bounded command-literal scan.

### Key Constraints
- Re-verify R-001 through R-003 against their recorded primary sources before any code or documentation edit; do not invent command flags or package identities.
- Use a bounded scan of `src/superclaude`, `docs`, and focused `tests` for changed commands, old Serena Git launchers, deprecated Morph packages, and Tavily `0.2.20`; resolve QA-reported active-document/test concerns but do not edit excluded legacy/template/plugin/user surfaces.
- Run tests with UV; capture pre/post `make verify-sync`, run `make sync-dev`, treat byte-identical pre-existing sync failure as baseline, and never stage generated `.claude/` output.

### Handoff File Convention

This task uses persisted intra-task handoffs at `.dev/tasks/to-do/TASK-RF-mcp-hardening-20260911-101319/phase-outputs/`, with `discovery/` for verification and scoped inventories, `test-results/` for command output, `reviews/` for QA verdicts, `plans/` for conditional decisions, and `reports/` for aggregations.

### Frontmatter Update Protocol

YOU MUST update `status` to `🟠 Doing` and `start_date` at task start, update `updated_date` after each work session, set `status` to `⚪ Blocked` with `blocker_reason` only if all remaining work shares a blocker, and set `status` to `🟢 Done` with `completion_date` only after every item and final QA validation completes.

## Detailed Task Instructions

### Phase 1: Initialize Evidence and Handoffs

**Step 1.1: Start task and create persisted handoffs**

- [x] Read the frontmatter and `### Execution Log` in this task file to apply the required task-state protocol, then update this task file's `status` to `🟠 Doing`, set `start_date` and `updated_date` to the current date, add the prescribed timestamped task-start entry, and create `.dev/tasks/to-do/TASK-RF-mcp-hardening-20260911-101319/phase-outputs/{discovery,test-results,reviews,plans,reports}/` for cross-batch evidence, ensuring all five directories exist and no project source, user configuration, or generated `.claude/` output is changed. If unable to complete due to file access issues or an unclear task-state conflict, log the specific blocker in `### Phase 1 - Initialize Evidence and Handoffs Findings` in `## Task Log / Notes`, then mark this item complete. This item cannot be marked as done until the actions are completed in their entirety exactly as described. Once done, mark this item as complete.

**Step 1.2: Capture sync-validation baseline**

- [x] Read R-004 at `.dev/tasks/to-do/TASK-RF-mcp-hardening-20260911-101319/research/08-scope-dispositions.md` and the QA baseline concern at `.dev/tasks/to-do/TASK-RF-mcp-hardening-20260911-101319/qa/analyst-completeness-report.md` to understand why unrelated existing sync drift must not widen this change, then run `make verify-sync` from `/config/workspace/IronClaude` before any source edit and write its exact combined output plus exit code to `.dev/tasks/to-do/TASK-RF-mcp-hardening-20260911-101319/phase-outputs/discovery/verify-sync-pre.txt` and a concise baseline classification to `phase-outputs/discovery/verify-sync-baseline.md`, ensuring the records are unedited command evidence, each failure cause is identified only from actual output, and no attempt is made to repair or stage unrelated `.claude/` files. If unable to execute the command, log the specific blocker in `### Phase 1 - Initialize Evidence and Handoffs Findings` in `## Task Log / Notes`, then mark this item complete. This item cannot be marked as done until the actions are completed in their entirety exactly as described. Once done, mark this item as complete.

### Phase 2: Re-verify Commands and Enumerate Active Literals

**Step 2.1: Re-verify official release decisions before edits**

- [x] Read R-001 through R-003 at `.dev/tasks/to-do/TASK-RF-mcp-hardening-20260911-101319/research/03-official-releases.md`, `05-serena-launcher-gap-fill.md`, and `06-morph-migration-gap-fill.md` to obtain the cited primary URLs and approved release decisions, then use the recorded primary sources to re-verify and write `.dev/tasks/to-do/TASK-RF-mcp-hardening-20260911-101319/phase-outputs/discovery/official-command-verification.md` with one evidence row each for Tavily `npx -y tavily-mcp@0.2.22`, Sequential Thinking `npx -y @modelcontextprotocol/server-sequential-thinking@2026.8.31`, Serena `uvx --from serena-agent==1.7.0 serena start-mcp-server --context claude-code --project-from-cwd --enable-web-dashboard false --enable-gui-log-window false`, Auggie `auggie --mcp --mcp-auto-workspace` plus global `@augmentcode/auggie@0.36.0`, and Morph `npx -y @morphllm/morphmcp` retaining `MORPH_API_KEY`, ensuring each row records URL, retrieval date, exact command/package fact, retained local key/name, and no command is inferred from stale local documentation. If a cited primary source is unavailable or contradicts a required command, log the evidence and blocker in `### Phase 2 - Re-verify Commands and Enumerate Active Literals Findings` in `## Task Log / Notes`, do not edit the affected command, then mark this item complete. This item cannot be marked as done until the actions are completed in their entirety exactly as described. Once done, mark this item as complete.

**Step 2.2: Produce the bounded active-literal inventory**

- [x] Read R-004 and R-005 at `.dev/tasks/to-do/TASK-RF-mcp-hardening-20260911-101319/research/08-scope-dispositions.md` and `qa/qa-research-depth-report.md` to apply the scope boundary and resolve reported documentation/test scan omissions, then search only project-owned `src/superclaude`, `docs`, and focused `tests` for `tavily-mcp@0.2.20`, `git+https://github.com/oraios/serena`, `--context ide-assistant`, `@morph-llm/morph-fast-apply`, `auggie-mcp`, and the unpinned Sequential launcher, and write `.dev/tasks/to-do/TASK-RF-mcp-hardening-20260911-101319/phase-outputs/discovery/active-command-literal-inventory.md` with one row per match containing file path, line, matched literal, classification (`required update`, `preserve namespace`, or `explicit exclusion`), exact required disposition, and rationale, ensuring the scan explicitly includes the QA-identified `docs/troubleshooting/serena-installation.md`, `docs/reference/mcp-server-guide.md`, `src/superclaude/cli/eval/suites/real.yaml`, and installer comments/docstrings when present, documents negative results, and does not modify `.claude`, `plugins`, user/machine configuration, hooks, or eval namespace migrations. If the search cannot run or a match cannot be classified from the cited evidence, log the specific blocker in `### Phase 2 - Re-verify Commands and Enumerate Active Literals Findings` in `## Task Log / Notes`, then mark this item complete. This item cannot be marked as done until the actions are completed in their entirety exactly as described. Once done, mark this item as complete.

**Step 2.3: Add execution items for newly discovered active surfaces**

<!-- DYNAMIC CONTENT START: discovered-active-command-surfaces -->
<!-- After Step 2.2, insert one self-contained checklist item here for every `required update` path not already assigned a named Phase 3 or Phase 4 item; each item must read the inventory and its exact source file, update only the discovered command/pin literal, and preserve explicitly retained keys/names. -->
<!-- DYNAMIC CONTENT END: discovered-active-command-surfaces -->

- [x] Read `active-command-literal-inventory.md` at `.dev/tasks/to-do/TASK-RF-mcp-hardening-20260911-101319/phase-outputs/discovery/active-command-literal-inventory.md` and the Phase 3/Phase 4 item headers in this task file to reconcile the dynamic entries with pre-enumerated file work, then write `.dev/tasks/to-do/TASK-RF-mcp-hardening-20260911-101319/phase-outputs/reports/active-surface-work-plan.md` listing every `required update` inventory row exactly once with its assigned checklist item and every `preserve namespace`/`explicit exclusion` row with its no-change rationale, ensuring no active source/docs literal from the bounded scan is silently omitted, no row is assigned twice, and exclusions remain excluded. If the inventory is missing or contains an unassigned required row, log the specific blocker in `### Phase 2 - Re-verify Commands and Enumerate Active Literals Findings` in `## Task Log / Notes`, then mark this item complete. This item cannot be marked as done until the actions are completed in their entirety exactly as described. Once done, mark this item as complete.

### Phase 3: Apply Bounded Runtime and Root-Config Changes

**Step 3.1: Update the authoritative registry**

- [x] Read `src/superclaude/cli/install_mcp.py` and the verified command evidence at `.dev/tasks/to-do/TASK-RF-mcp-hardening-20260911-101319/phase-outputs/discovery/official-command-verification.md` to update only the five approved registry metadata/command values, then edit `src/superclaude/cli/install_mcp.py` to set `TAVILY_MCP_VERSION` to `0.2.22`, pin Sequential Thinking to `npx -y @modelcontextprotocol/server-sequential-thinking@2026.8.31`, set Serena to `uvx --from serena-agent==1.7.0 serena start-mcp-server --context claude-code --project-from-cwd --enable-web-dashboard false --enable-gui-log-window false`, change Auggie's global install command to `npm install -g @augmentcode/auggie@0.36.0`, and set only the existing `morphllm-fast-apply` entry's launcher to `npx -y @morphllm/morphmcp`, ensuring all five remain `stdio`/optional as currently defined, `morphllm-fast-apply` remains both registry key and `name`, `MORPH_API_KEY` remains, the existing exact-command reconciliation implementation is untouched, and no abstraction, alias, old-registration deletion, or excluded-server change is introduced. If unable to complete due to source drift or contradictory verified evidence, log the specific blocker in `### Phase 3 - Apply Bounded Runtime and Root-Config Changes Findings` in `## Task Log / Notes`, then mark this item complete. This item cannot be marked as done until the actions are completed in their entirety exactly as described. Once done, mark this item as complete.

**Step 3.2: Update the project-owned Auggie root configuration**

- [x] Read `.mcp.json`, `src/superclaude/cli/install_mcp.py`, and R-004 at `.dev/tasks/to-do/TASK-RF-mcp-hardening-20260911-101319/research/08-scope-dispositions.md` to preserve the independently consumed project tool namespace while aligning its launcher, then edit `.mcp.json` so `mcpServers.auggie-mcp` retains its key, `type: "stdio"`, and `env: {}` but has `command: "auggie"` and ordered `args: ["--mcp", "--mcp-auto-workspace"]`, ensuring no `npx`, `auggie-mcp` package launcher, credential, server-key rename, hook/eval migration, or user-level configuration is added. If unable to complete due to malformed current JSON or incompatible verified evidence, log the specific blocker in `### Phase 3 - Apply Bounded Runtime and Root-Config Changes Findings` in `## Task Log / Notes`, then mark this item complete. This item cannot be marked as done until the actions are completed in their entirety exactly as described. Once done, mark this item as complete.

### Phase 4: Align Active Publications and Focused Contracts

**Step 4.1: Update Tavily installer contracts**

- [ ] Read `tests/cli/test_install_mcp_tavily.py`, `src/superclaude/cli/install_mcp.py`, and the active-literal inventory to update every focused Tavily contract from `0.2.20` to `0.2.22`, then edit `tests/cli/test_install_mcp_tavily.py` so its registry assertion, literal command assertions, re-registration expected argv, fixture output, and gated smoke expectation all require the new pin while retaining existing secret-masking, scope, malformed-output, and no-op coverage, ensuring no real MCP binary, API key, or user configuration is invoked. If unable to complete due to an unexpected test contract, log the specific blocker in `### Phase 4 - Align Active Publications and Focused Contracts Findings` in `## Task Log / Notes`, then mark this item complete. This item cannot be marked as done until the actions are completed in their entirety exactly as described. Once done, mark this item as complete.

- [ ] Read `tests/docs/test_tavily_doc_alignment.py`, `src/superclaude/cli/install_mcp.py`, and the active-literal inventory to preserve the bounded source/docs scanner while advancing its single permitted pin, then edit `tests/docs/test_tavily_doc_alignment.py` to require only `tavily-mcp@0.2.22` without changing its scan roots, exclusions, non-vacuity guard, or unrelated stale-token checks, ensuring all scanner expectations match the authoritative registry and no generated/history directory is added to scope. If unable to complete due to incompatible scanner behavior, log the specific blocker in `### Phase 4 - Align Active Publications and Focused Contracts Findings` in `## Task Log / Notes`, then mark this item complete. This item cannot be marked as done until the actions are completed in their entirety exactly as described. Once done, mark this item as complete.

**Step 4.2: Add pure registry and root-config contracts**

- [ ] Read `tests/cli/test_install_mcp_tavily.py`, `src/superclaude/cli/install_mcp.py`, `.mcp.json`, and the verified command handoff to follow existing subprocess-interception conventions, then create `tests/cli/test_install_mcp_registry.py` with focused pure assertions for the retained keys/names, `stdio` transport, exact Sequential, Serena, Morph, and Auggie command metadata, retained `MORPH_API_KEY`, and stable-name command-drift add-argv behavior without executing external binaries, ensuring it covers no migration alias/deletion behavior and does not duplicate Tavily default-parameter tests. If unable to complete due to missing reusable test utilities, log the specific blocker in `### Phase 4 - Align Active Publications and Focused Contracts Findings` in `## Task Log / Notes`, then mark this item complete. This item cannot be marked as done until the actions are completed in their entirety exactly as described. Once done, mark this item as complete.

- [ ] Read `.mcp.json`, `tests/cli/test_install_mcp_tavily.py`, and R-004 to encode the root-file compatibility contract without touching a runtime Claude installation, then create `tests/cli/test_mcp_project_config.py` that parses the repository root configuration and asserts `mcpServers.auggie-mcp`, `type: "stdio"`, command `auggie`, ordered official arguments, empty environment, and absence of `npx`/inline credential values, ensuring the test reads only the repository file and explicitly preserves the `auggie-mcp` namespace. If unable to complete due to project test layout constraints, log the specific blocker in `### Phase 4 - Align Active Publications and Focused Contracts Findings` in `## Task Log / Notes`, then mark this item complete. This item cannot be marked as done until the actions are completed in their entirety exactly as described. Once done, mark this item as complete.

**Step 4.3: Update each pre-enumerated active documentation/configuration surface**

- [ ] Read `docs/user-guide/mcp-installation.md`, the verified command handoff, and the active-literal inventory to align only catalog, selection, prerequisite, and project-scope text affected by changed launchers, then update `docs/user-guide/mcp-installation.md` to retain stable selector/key names while accurately presenting the pinned Serena/Morph/Sequential/Tavily/Auggie behavior and no-secrets/project-owned boundaries, ensuring no user-level registration or excluded integration guidance is added. If unable to complete due to an unverified claim, log the specific blocker in `### Phase 4 - Align Active Publications and Focused Contracts Findings` in `## Task Log / Notes`, then mark this item complete. This item cannot be marked as done until the actions are completed in their entirety exactly as described. Once done, mark this item as complete.

- [ ] Read `docs/user-guide/mcp-servers.md`, the verified command handoff, and the inventory to repair each direct in-scope command/pin literal found there, then update `docs/user-guide/mcp-servers.md` with the verified pins and Serena/Morph launchers while retaining stated stable local server names, ensuring no stale floating Git Serena command, deprecated Morph package, or Tavily `0.2.20` literal remains and unrelated architecture cleanup is not performed. If unable to complete due to an ambiguous match, log the specific blocker in `### Phase 4 - Align Active Publications and Focused Contracts Findings` in `## Task Log / Notes`, then mark this item complete. This item cannot be marked as done until the actions are completed in their entirety exactly as described. Once done, mark this item as complete.

- [ ] Read `docs/troubleshooting/serena-installation.md`, the Serena verification handoff, and the inventory to resolve the QA-reported runnable stale launcher, then update every active install/re-registration example in `docs/troubleshooting/serena-installation.md` to the verified pinned Serena command and `claude-code` context, ensuring dashboard and GUI flags plus project-from-cwd are preserved, no obsolete Git source or `ide-assistant` remains in normative instructions, and no user/machine configuration file is changed. If unable to complete due to contradictory source guidance, log the specific blocker in `### Phase 4 - Align Active Publications and Focused Contracts Findings` in `## Task Log / Notes`, then mark this item complete. This item cannot be marked as done until the actions are completed in their entirety exactly as described. Once done, mark this item as complete.

- [ ] Read `docs/reference/mcp-server-guide.md`, the Serena verification handoff, and the inventory to resolve the QA-reported active stale Serena example without broad legacy-document modernization, then update only the matching Serena launcher/context literals in `docs/reference/mcp-server-guide.md` to the verified pinned command, ensuring unrelated version, architecture, and excluded-MCP text remains untouched. If unable to complete due to an unclassifiable occurrence, log the specific blocker in `### Phase 4 - Align Active Publications and Focused Contracts Findings` in `## Task Log / Notes`, then mark this item complete. This item cannot be marked as done until the actions are completed in their entirety exactly as described. Once done, mark this item as complete.

- [ ] Read `src/superclaude/mcp/MCP_Tavily.md`, `src/superclaude/cli/install_mcp.py`, and the inventory to align the canonical source-owned Tavily reference, then update `src/superclaude/mcp/MCP_Tavily.md` from `tavily-mcp@0.2.20` to `tavily-mcp@0.2.22` and retain the verified API-key/launcher semantics, ensuring no unrelated capability claims are fabricated. If unable to complete due to source inconsistency, log the specific blocker in `### Phase 4 - Align Active Publications and Focused Contracts Findings` in `## Task Log / Notes`, then mark this item complete. This item cannot be marked as done until the actions are completed in their entirety exactly as described. Once done, mark this item as complete.

- [ ] Read `src/superclaude/mcp/MCP_Auggie.md`, `.mcp.json`, `src/superclaude/cli/install_mcp.py`, and the inventory to align official pinned installation guidance with the preserved root namespace, then update `src/superclaude/mcp/MCP_Auggie.md` to replace any `@latest` global package instruction with `@augmentcode/auggie@0.36.0` and describe the repository-owned `auggie --mcp --mcp-auto-workspace` configuration without renaming `auggie-mcp`, ensuring no instruction edits user configuration, credentials, hooks, or eval namespaces. If unable to complete due to conflicting evidence, log the specific blocker in `### Phase 4 - Align Active Publications and Focused Contracts Findings` in `## Task Log / Notes`, then mark this item complete. This item cannot be marked as done until the actions are completed in their entirety exactly as described. Once done, mark this item as complete.

- [ ] Read `src/superclaude/cli/eval/suites/real.yaml`, the inventory, and `tests/docs/test_tavily_doc_alignment.py` to address the QA-reported in-scope explanatory Tavily literal only if Step 2.2 classifies it as `required update`, then update that literal/comment to `0.2.22` without changing eval capabilities, test cases, namespaces, or execution behavior, ensuring the edit is text-only and does not perform the explicitly excluded eval namespace migration. If Step 2.2 classifies the occurrence as excluded, record its rationale in `phase-outputs/reports/active-surface-work-plan.md` instead. If unable to classify the occurrence, log the specific blocker in `### Phase 4 - Align Active Publications and Focused Contracts Findings` in `## Task Log / Notes`, then mark this item complete. This item cannot be marked as done until the actions are completed in their entirety exactly as described. Once done, mark this item as complete.

### Phase 5: Execute Focused Validation and Source/Mirror Checks

**Step 5.1: Run focused contracts with UV**

- [ ] Read the modified `src/superclaude/cli/install_mcp.py`, `.mcp.json`, and focused test files `tests/cli/test_install_mcp_tavily.py`, `tests/cli/test_install_mcp_registry.py`, `tests/cli/test_mcp_project_config.py`, and `tests/docs/test_tavily_doc_alignment.py` to validate the exact changed contracts, then run `uv run pytest tests/cli/test_install_mcp_tavily.py tests/cli/test_install_mcp_registry.py tests/cli/test_mcp_project_config.py tests/docs/test_tavily_doc_alignment.py -v` and capture exact output in `.dev/tasks/to-do/TASK-RF-mcp-hardening-20260911-101319/phase-outputs/test-results/focused-pytest.txt` plus a pass/fail count and failing-test table in `focused-pytest-summary.md`, ensuring no external MCP executable, global npm install, API key, or user configuration is exercised and all focused tests pass before proceeding. If the command cannot execute or failures remain after root-cause fixes within this scope, log the specific blocker in `### Phase 5 - Execute Focused Validation and Source/Mirror Checks Findings` in `## Task Log / Notes`, then mark this item complete. This item cannot be marked as done until the actions are completed in their entirety exactly as described. Once done, mark this item as complete.

**Step 5.2: Re-run the bounded literal scan**

- [ ] Read the pre-change inventory at `.dev/tasks/to-do/TASK-RF-mcp-hardening-20260911-101319/phase-outputs/discovery/active-command-literal-inventory.md`, the active-surface work plan, and all modified source/docs/test files to test whether every assigned literal was resolved, then repeat the exact bounded searches from Step 2.2 and write `.dev/tasks/to-do/TASK-RF-mcp-hardening-20260911-101319/phase-outputs/test-results/active-command-literal-postscan.md` with before/after rows and a PASS/FAIL verdict, ensuring no `tavily-mcp@0.2.20`, Serena Git launcher, obsolete `ide-assistant` context, or deprecated Morph package remains in a required-update surface, any intentionally retained `auggie-mcp` key is classified as preservation rather than a false failure, and any unexpected active match is converted into one dynamic file-specific repair item before this item is marked complete. If the scan cannot establish a disposition, log the specific blocker in `### Phase 5 - Execute Focused Validation and Source/Mirror Checks Findings` in `## Task Log / Notes`, then mark this item complete. This item cannot be marked as done until the actions are completed in their entirety exactly as described. Once done, mark this item as complete.

**Step 5.3: Run sync and quality validation with baseline comparison**

- [ ] Read `verify-sync-pre.txt` and `verify-sync-baseline.md` from `.dev/tasks/to-do/TASK-RF-mcp-hardening-20260911-101319/phase-outputs/discovery/` to preserve the known pre-existing sync state, then run `make sync-dev`, `make verify-sync`, and `make lint` from `/config/workspace/IronClaude`, capture each exact combined output and exit code under `phase-outputs/test-results/`, and write `phase-outputs/test-results/sync-and-lint-summary.md` comparing pre/post `verify-sync` output byte-for-byte, ensuring a post-sync pass is recorded as PASS, a byte-identical pre-existing failure is recorded as baseline/non-blocking, any new or changed failure is FAIL and investigated only to the MCP change boundary, and generated `.claude/` output is never staged or manually repaired. If a command cannot execute or a new attributable failure cannot be resolved, log the specific blocker in `### Phase 5 - Execute Focused Validation and Source/Mirror Checks Findings` in `## Task Log / Notes`, then mark this item complete. This item cannot be marked as done until the actions are completed in their entirety exactly as described. Once done, mark this item as complete.

### Phase 6: Final Standard-Intensity Lens QA Gate

**Step 6.1: Aggregate final evidence**

- [ ] Use Glob to collect files in `.dev/tasks/to-do/TASK-RF-mcp-hardening-20260911-101319/phase-outputs/{discovery,test-results,reports}/`, then read each collected handoff and the modified runtime/config/test/docs files to write `.dev/tasks/to-do/TASK-RF-mcp-hardening-20260911-101319/phase-outputs/reports/final-output-manifest.md` containing exact changed paths, validation results, retained namespaces, excluded surfaces, and residual baseline status, ensuring every final QA agent has a complete evidence index and no success claim is made without recorded command/test output. If unable to aggregate required evidence, log the specific blocker in `### Phase 6 - Final Standard-Intensity Lens QA Gate Findings` in `## Task Log / Notes`, then mark this item complete. This item cannot be marked as done until the actions are completed in their entirety exactly as described. Once done, mark this item as complete.

**Step 6.2: Spawn independent final report-only lenses in parallel**

- [ ] Spawn `rf-qa` with `fix_authorization: false` to inspect `final-output-manifest.md`, the changed registry/config/tests/docs, and the bounded scan evidence for the **template/contract conformance** lens; instruct it, “Assume this implementation has at least 5 contract errors. Find them,” and write its PASS/FAIL verdict with specific findings to `.dev/tasks/to-do/TASK-RF-mcp-hardening-20260911-101319/phase-outputs/reviews/qa-structural-contract-report.md`, ensuring it checks all five exact commands, preserved keys/names, and root JSON schema without modifying files. If unable to spawn or obtain the report, log the specific blocker in `### Phase 6 - Final Standard-Intensity Lens QA Gate Findings` in `## Task Log / Notes`, then mark this item complete. This item cannot be marked as done until the actions are completed in their entirety exactly as described. Once done, mark this item as complete.

- [ ] Spawn `rf-qa` with `fix_authorization: false` to inspect the same final evidence for the **internal-consistency** lens; instruct it, “Assume this implementation has at least 5 consistency errors. Find them,” and write a PASS/FAIL report to `phase-outputs/reviews/qa-structural-consistency-report.md`, ensuring registry values, root config, focused tests, active docs, scan inventory, and baseline report agree without modifying files. If unable to spawn or obtain the report, log the specific blocker in `### Phase 6 - Final Standard-Intensity Lens QA Gate Findings` in `## Task Log / Notes`, then mark this item complete. This item cannot be marked as done until the actions are completed in their entirety exactly as described. Once done, mark this item as complete.

- [ ] Spawn `rf-qa` with `fix_authorization: false` to inspect the same final evidence for the **evidence/scope** lens; instruct it, “Assume this implementation has at least 5 evidence or scope errors. Find them,” and write a PASS/FAIL report to `phase-outputs/reviews/qa-structural-evidence-report.md`, ensuring every change traces to R-001 through R-005 or the bounded scan and excluded user, plugin/template, hook/eval, alias, and unrelated MCP surfaces remain unchanged. If unable to spawn or obtain the report, log the specific blocker in `### Phase 6 - Final Standard-Intensity Lens QA Gate Findings` in `## Task Log / Notes`, then mark this item complete. This item cannot be marked as done until the actions are completed in their entirety exactly as described. Once done, mark this item as complete.

- [ ] Spawn `rf-qa-qualitative` with `fix_authorization: false` to inspect final active docs and task evidence for the **actionability** lens; instruct it, “Assume this implementation has at least 5 actionable-documentation errors. Find them,” and write a PASS/FAIL report to `phase-outputs/reviews/qa-content-actionability-report.md`, ensuring installed command examples are runnable, preserve intended scope, and do not direct users to credentials or machine configuration. If unable to spawn or obtain the report, log the specific blocker in `### Phase 6 - Final Standard-Intensity Lens QA Gate Findings` in `## Task Log / Notes`, then mark this item complete. This item cannot be marked as done until the actions are completed in their entirety exactly as described. Once done, mark this item as complete.

- [ ] Spawn `rf-qa-qualitative` with `fix_authorization: false` to inspect final runtime/config/test evidence for the **domain accuracy** lens; instruct it, “Assume this implementation has at least 5 MCP compatibility errors. Find them,” and write a PASS/FAIL report to `phase-outputs/reviews/qa-content-domain-accuracy-report.md`, ensuring stable-name command reconciliation, `morphllm-fast-apply`, and `auggie-mcp` preservation are accurate and no unsupported migration behavior is claimed. If unable to spawn or obtain the report, log the specific blocker in `### Phase 6 - Final Standard-Intensity Lens QA Gate Findings` in `## Task Log / Notes`, then mark this item complete. This item cannot be marked as done until the actions are completed in their entirety exactly as described. Once done, mark this item as complete.

- [ ] Spawn `rf-qa-qualitative` with `fix_authorization: false` to inspect final evidence for the **cross-reference chain** lens; instruct it, “Assume this implementation has at least 5 broken evidence chains. Find them,” and write a PASS/FAIL report to `phase-outputs/reviews/qa-content-cross-reference-report.md`, ensuring primary evidence, registry values, docs, tests, literal inventory, test results, and sync baseline produce no contradiction. If unable to spawn or obtain the report, log the specific blocker in `### Phase 6 - Final Standard-Intensity Lens QA Gate Findings` in `## Task Log / Notes`, then mark this item complete. This item cannot be marked as done until the actions are completed in their entirety exactly as described. Once done, mark this item as complete.

- [ ] Spawn `rf-qa` with `fix_authorization: false` as the **MCP release/compatibility domain** lens to inspect all final evidence; instruct it, “Assume this implementation has at least 5 release or compatibility errors. Find them,” and write a PASS/FAIL report to `phase-outputs/reviews/qa-domain-mcp-release-report.md`, ensuring exact approved commands and pins appear only where source evidence supports them and no excluded integration is changed. If unable to spawn or obtain the report, log the specific blocker in `### Phase 6 - Final Standard-Intensity Lens QA Gate Findings` in `## Task Log / Notes`, then mark this item complete. This item cannot be marked as done until the actions are completed in their entirety exactly as described. Once done, mark this item as complete.

**Step 6.3: Serialize finding resolution and verification**

- [ ] Use Glob to locate all `phase-outputs/reviews/qa-*-report.md` reports, then read every report and write `.dev/tasks/to-do/TASK-RF-mcp-hardening-20260911-101319/phase-outputs/reports/qa-consolidated-findings.md` with a binary aggregate verdict, deduplicated findings, severity, originating lenses, and cycle-0 PASS set, ensuring any issue at any severity yields FAIL and no report is omitted. If unable to consolidate reports, log the specific blocker in `### Phase 6 - Final Standard-Intensity Lens QA Gate Findings` in `## Task Log / Notes`, then mark this item complete. This item cannot be marked as done until the actions are completed in their entirety exactly as described. Once done, mark this item as complete.

- [ ] Read `qa-consolidated-findings.md` and spawn exactly one `rf-qa` fix agent with `fix_authorization: true` only when the aggregate verdict is FAIL, instructing it to apply all in-scope fixes serially and write `.dev/tasks/to-do/TASK-RF-mcp-hardening-20260911-101319/phase-outputs/reports/qa-fix-summary.md`; if PASS, write the same file stating that no fixes were authorized, ensuring no parallel editor changes files and no out-of-scope remediation occurs. If unable to execute the applicable branch, log the specific blocker in `### Phase 6 - Final Standard-Intensity Lens QA Gate Findings` in `## Task Log / Notes`, then mark this item complete. This item cannot be marked as done until the actions are completed in their entirety exactly as described. Once done, mark this item as complete.

- [ ] Spawn `rf-qa` and `rf-qa-qualitative` in parallel with `fix_authorization: false` to read the consolidated findings, fix summary, and final changed files, and write `phase-outputs/reviews/qa-verification-structural-report.md` and `qa-verification-content-report.md` with PASS/FAIL verdicts, ensuring every prior finding is addressed and no fix introduced a new scope, command, test, documentation, or namespace error. If unable to obtain either verification report, log the specific blocker in `### Phase 6 - Final Standard-Intensity Lens QA Gate Findings` in `## Task Log / Notes`, then mark this item complete. This item cannot be marked as done until the actions are completed in their entirety exactly as described. Once done, mark this item as complete.

- [ ] Read both verification reports and the per-cycle PASS/failure sets, then write `.dev/tasks/to-do/TASK-RF-mcp-hardening-20260911-101319/phase-outputs/plans/qa-gate-verdict.md` that proceeds on two PASS verdicts or performs at most one additional standard-intensity serialized consolidation/fix/verification cycle, checking regression before monotonicity before the two-cycle cap and emitting the required regression or `[HALT-MONOTONICITY] |F|=<n>` halt message when applicable, ensuring unresolved findings after the cap become Open Questions and the task does not claim PASS. If unable to apply the protocol, log the specific blocker in `### Phase 6 - Final Standard-Intensity Lens QA Gate Findings` in `## Task Log / Notes`, then mark this item complete. This item cannot be marked as done until the actions are completed in their entirety exactly as described. Once done, mark this item as complete.

## Post-Completion Actions

- [ ] Read this task file, `phase-outputs/reports/final-output-manifest.md`, `phase-outputs/test-results/focused-pytest-summary.md`, `phase-outputs/test-results/sync-and-lint-summary.md`, and `phase-outputs/plans/qa-gate-verdict.md` to validate final completion evidence, then use Glob to confirm every named handoff/test/report deliverable exists and inspect the task for unchecked items and unresolved blocker entries, ensuring focused UV tests pass, the literal post-scan is PASS, the final QA gate is PASS or has explicitly recorded Open Questions, and any non-green `verify-sync` is byte-identical baseline rather than a new MCP regression. If evidence is missing or a new failure remains, log the specific blocker in `### Post-Completion Findings` in `## Task Log / Notes`, then mark this item complete. This item cannot be marked as done until the actions are completed in their entirety exactly as described. Once done, mark this item as complete.

- [ ] Read all completed phase findings and final reports to create the `### Task Summary` in `## Task Log / Notes`, documenting exact runtime/config/docs/tests changed, release verification evidence, validation results, byte-identical baseline treatment if applicable, exclusions preserved, challenges, deviations, and every blocker with resolution status, ensuring the summary contains no unverified success claim and explicitly states that no post-reflect gate was run or required. If unable to produce the summary due to missing evidence, log the specific blocker in `### Post-Completion Findings` in `## Task Log / Notes`, then mark this item complete. This item cannot be marked as done until the actions are completed in their entirety exactly as described. Once done, mark this item as complete.

- [ ] Read the completion evidence and `### Task Summary` in this task file to apply the final state protocol, then set `completion_date` and `updated_date` to the current date, set `status` to `🟢 Done`, and add a timestamped completion entry to `### Execution Log`, ensuring all prior checklist items are complete and no generated `.claude/` output has been staged. If the task is blocked by unresolved evidence, preserve a blocked status and log the reason instead of marking Done. This item cannot be marked as done until the actions are completed in their entirety exactly as described. Once done, mark this item as complete.

## Task Log / Notes

### Task Summary

**Completion Date:** [To be filled on completion]

**Work Completed:**
- [To be filled from final-output-manifest.md]

**Challenges Encountered:**
- [To be filled on completion]

**Deviations from Process:**
- No post-reflect gate is included by explicit task constraint.

**Blockers Logged:**
- [To be filled from phase findings]

**Follow-Up Required:** [To be filled on completion]

### Execution Log

**[2026-09-11 10:48 UTC]** - Task started: Updated status to `🟠 Doing`, set start_date, and created evidence directories.

**[YYYY-MM-DD HH:MM]** - Task completed: Updated status to `🟢 Done` and completion_date.

### Phase 1 - Initialize Evidence and Handoffs Findings

<!-- Blocker format: **[YYYY-MM-DD HH:MM]** - Step X.Y BLOCKED; **Blocker Reason:** [reason]; **Attempted:** [action]; **Required to Unblock:** [need]; **Files Affected:** [paths]. -->

### Phase 2 - Re-verify Commands and Enumerate Active Literals Findings

<!-- Record unavailable primary evidence, scan failures, or unclassifiable matches here. -->

### Phase 3 - Apply Bounded Runtime and Root-Config Changes Findings

<!-- Record only source-drift or evidence blockers here. -->

### Phase 4 - Align Active Publications and Focused Contracts Findings

<!-- Record only documentation/test-contract blockers here. -->

### Phase 5 - Execute Focused Validation and Source/Mirror Checks Findings

<!-- Record test, scan, sync, or lint blockers and whether they are baseline or new. -->

### Phase 6 - Final Standard-Intensity Lens QA Gate Findings

**[2026-09-11 10:56 UTC]** - Execution checkpoint: implementation, direct-documentation alignment, focused tests, literal post-scan, sync baseline capture, `make sync-dev`, and review are complete. Final lens gate and post-completion checklist items remain unchecked for the next `/task` run.

<!-- Record lens verdicts, fix cycles, PASS sets, monotonicity/regression halts, and Open Questions here. -->

### Post-Completion Findings

<!-- Record missing deliverables, unresolved blockers, or incomplete evidence here. -->

### Follow-Up Items Identified

<!-- - **[Priority: High/Medium/Low]** [follow-up] - Identified in Step [X.Y] -->

### Deviations from Process

<!-- **[YYYY-MM-DD HH:MM]** - Deviation from Step [X.Y]: Expected / Actual / Rationale. -->

# Phase 3 codegraph slots ledger

This file is the Phase 3 input. Phase 1 of issue #323 removed Serena from the primitives and replaced every load-bearing symbol, reference, diagnostics and allowlist step with a native floor (Grep, Read, Glob, Bash, auggie). Phase 3 adds codegraph as a tier ABOVE each floor; the floor stays permanently. Each row below is one step Phase 1 touched: where it is (a step heading or anchor, never a line number), the Serena tool it used to call, what Phase 1 did (`deleted` = no replacement needed because the step is gone or already had a Serena-free path; `floor` = rewritten to the named native floor), the floor now in place, and the stable contract fields the step touches.

Rule for Phase 3: a codegraph tier goes in front of the `floor` rows only. `deleted` rows get no codegraph slot unless Phase 3 decides to re-add the capability on purpose.

Rows are appended per task. The memory and decorative-mention steps of Tasks 10-12 come first, then Task 13 (reflect, `reuse-auditor`, reflect command copies); later tasks append below the Task 13 block.

## Tasks 10 to 12: decorative mentions and memory steps (no codegraph slot)

Tasks 10, 11 and 12 touched no symbol, reference or diagnostics step; they dropped decorative Serena mentions and moved Serena memory to plain files. The rows are here so the ledger covers every step touched in Tasks 10-15. Every action below is `deleted` or `floor`; none of them gets a codegraph tier in Phase 3 (codegraph takes no memory job). The floor is the `.superclaude/memory/<key>.md` store (rules M1-M4 of the Phase 1 spec).

| File | Step heading / anchor | Former Serena tool | Action | Floor used | Contract fields touched |
|---|---|---|---|---|---|
| 48 command, skill and agent files (every `mcp-servers:` frontmatter in `src/superclaude`, `plugins/superclaude`, `commands`, `agents`) | frontmatter `mcp-servers:` list | the `serena` entry | deleted | none | none |
| core/CLAUDE.md | MCP server table; freshness rule S2 | the `serena` row; `replace_content`, `replace_symbol_body`, `insert_*_symbol` | deleted | S2 now says Edit / Write only | none |
| core/RESEARCH_CONFIG.md and plugins/superclaude/core/RESEARCH_CONFIG.md | `memory` tool entry; tool-fallback table | `serena` as memory backend | deleted | none | none |
| skills/sc-adversarial-protocol/SKILL.md | MCP Integration table; `mcp_integration` YAML; framework registration lines | `serena` persistence row and block | deleted | none | none |
| skills/sc-post-release-protocol/SKILL.md | telemetry `mcps_available` enum | `serena` value | deleted | none | none |
| skills/sc-roadmap-protocol/SKILL.md | Post-Wave completion step 2; MCP table; circuit-breaker bullet; save points; resume protocol; graceful degradation; Boundaries | Serena session memory | floor | `<output_dir>/.session-memory.md` is the only persistence path (rule M6) | none |
| commands/research.md (src, plugins, commands/sc-research.md); commands/sc-help.md; commands/sc-task.md; commands/sc-workflow.md | MCP bullets, help rows, examples | Serena memory and persistence wording | deleted | none | none |
| commands/save.md, load.md, pm.md (src, plugins, commands/sc-*.md) | Memory Store / MCP Integration; tool coordination; flow examples | `write_memory`, `read_memory`, `list_memories`, `edit_memory`; `think_about_*`, `summarize_changes`, `activate_project` | floor / deleted | Write, Read, Glob, Edit on `<project>/.superclaude/memory/<key>.md`; `.superclaude/.gitignore` containing `*` created on first write; `/sc:load` keeps one legacy read of `.serena/memories/<key>.md` for one release | none |
| agents/pm-agent.md (src, plugins, agents/sc-pm-agent.md) | session start, checkpoints, mistake log, monthly maintenance, self-evaluation | the same memory tools; `think_about_*` | floor / deleted | memory files as above; plan key unified on `current_plan.md` (decision 5); no primitive deletes memory | none |
| modes/MODE_Task_Management.md (src, plugins) | memory schema, phase / task / todo keys, checkpoints | memory tools; `think_about_*` | floor / deleted | memory files as above | none |
| skills/sc-pm-protocol/SKILL.md | lifecycle steps | memory tools | floor | memory files as above | none |
| commands/reflect.md (src, plugins, commands/sc-reflect.md) and skills/sc-reflect-protocol/SKILL.md section 6.3 | calibration hydrate, last-pass, handoff persistence | `read_memory`, `write_memory`, `delete_memory`, `rename_memory`, `edit_memory`, `prepare_for_new_conversation` | floor | calibration in tracked `docs/memory/reflect/deviation-patterns-<slug>.md`; last-pass in `.superclaude/memory/reflect/`; handoff in `.superclaude/memory/reflect/handoff-<slug>-<timestamp>.md` | telemetry `memory_retention_skipped_readonly`, `memory_retention_unbounded`, `handoff_persist_method` removed |
| skills/sc-reflect-protocol/refs/input-resolution.md | Auggie plus Serena availability bullets | availability probe | deleted | none | none |
| skills/sc-reflect-protocol/refs/remediation-handoff.md | handoff location | memory write | floor | file under `.superclaude/memory/reflect/` | none |
| skills/sc-validate-roadmap-protocol/SKILL.md | Hooks 0a-0c and 6a-6d (ledger, terminology map, pattern log, adversarial patterns); Pre-Phase 0 project activation | `read_memory`, `write_memory`, `activate_project` | floor / deleted | `.superclaude/memory/validate-roadmap/<key>-{project-slug}.md`, still fail-open | none |
| skills/sc-task-protocol/SKILL.md | STRICT tier prerequisites, memory read, completion write | `activate_project`, memory tools, `think_about_*` | floor / deleted | Glob and Read of `.superclaude/memory/**/*.md`; completion writes `.superclaude/memory/task/session-<timestamp>.md` | none |
| skills/sc-crash-recovery/SKILL.md, refs/investigators.md, refs/report-template.md, scripts/bootstrap_scan.sh | investigator #3; report section; JSON fields | Serena memory directory | floor | investigator `project-memory` reads `.superclaude/memory`; JSON fields renamed `has_memory`, `memory_count` | JSON fields of `bootstrap_scan.sh` |
| core/HOW-WE-WORK.md and its byte copy plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md | routing-guide wording for session memory | Serena memory | floor | wording points at `.superclaude/memory/` files | none |

## Task 13: reflect, reflect-reviewer, reuse-auditor

### `src/superclaude/skills/sc-reflect-protocol/SKILL.md`

| File | Step heading / anchor | Former Serena tool | Action | Floor used | Contract fields touched |
|---|---|---|---|---|---|
| sc-reflect-protocol/SKILL.md | Frontmatter `allowed-tools` | all `mcp__serena__*` names (14) | deleted | roster keeps Read, Grep, Glob, Bash and auggie | none |
| sc-reflect-protocol/SKILL.md | Wave diagram, Wave 0 / Step 0.5c (active-project config probe) | `get_current_config` | deleted | none (no Serena state to fingerprint) | telemetry `serena_version`, `serena_active_context`, `serena_active_modes`, `serena_config_snapshot_path` removed; degraded tokens `serena:context-excluded` and `get_current_config` removed |
| sc-reflect-protocol/SKILL.md | Step 0.5d (verification and adoption availability probe) | `get_current_config` (backend, active-tools list), `.serena/project.yml` `read_only` | deleted | Step 5.5 gates only on Bash being available and `--no-verify` | `verification_skip_reason` enum unchanged (`read-only-project` kept as a legal value, no longer produced) |
| sc-reflect-protocol/SKILL.md | Step 0.7 (activate project, memory hydrate, onboarding-status parse) | `activate_project`, `list_memories` | deleted, rewritten as hydrate-only | Read of the section 6.3 memory files plus Glob `.superclaude/memory/reflect/*.md` | telemetry `onboarding_status`, degraded token `serena:onboarding-parse` removed; `memory_hits`, `memory_misses` kept |
| sc-reflect-protocol/SKILL.md | Step 0.7b (onboarding bootstrap) and flag `--onboard` | `onboarding`, `list_memories` | deleted | none (tracked `docs/memory/reflect/deviation-patterns-{slug}.md` is the cold-start baseline) | `onboarding_ran` kept as constant `false`; telemetry `onboarding_succeeded`, `onboarding_memories_count`, `onboarding_skipped_reason`, `onboarding_budget_exceeded` removed |
| sc-reflect-protocol/SKILL.md | Step 1B.3 sub-step 1a (declaration anchor for each hunk) | `find_declaration` | floor | Grep for `def <name>\|class <name>\|function <name>`, then Read the range | `find_declaration_no_match` (emitted on a zero-hit Grep) |
| sc-reflect-protocol/SKILL.md | Step 1B.3 sub-step 1 (touched symbols per task) | `find_symbol` | floor | enclosing definition found by the same Grep-for-definition then Read step | none |
| sc-reflect-protocol/SKILL.md | Step 1B.3 sub-step 3 (shared-vs-collision check) | `find_referencing_symbols` | floor | Grep with a word-boundary pattern (`\b<symbol>\b`), then Read the call sites | `interaction_effects_findings` (severity still scales with call-site count) |
| sc-reflect-protocol/SKILL.md | Step 1B.3 sub-step 3a (shared base-class lineage) and flag `--with-hierarchy` | `type_hierarchy` | deleted | edge falls back to the sub-step 3 reference Grep | `type_hierarchy_invoked` kept as constant `false` |
| sc-reflect-protocol/SKILL.md | Section 6 title and intro (Modern Serena Tool Usage) | `think_about_*` framing | floor (retitled to the auggie + native Grep/Read chain) | auggie first, then Grep and Read | none |
| sc-reflect-protocol/SKILL.md | Section 6.1 chain step 1 (activate project) | `activate_project` | deleted | none | none |
| sc-reflect-protocol/SKILL.md | Section 6.1 chain step 2 (structural map of a file) | `get_symbols_overview` | floor | auggie `codebase-retrieval`, then Grep for the file's definitions and Read the file | none |
| sc-reflect-protocol/SKILL.md | Section 6.1 chain step 2a (hunk to declaration) | `find_declaration` | floor | Grep for the definition, then Read the range | `find_declaration_no_match`, `hunk_to_declaration_map_path` |
| sc-reflect-protocol/SKILL.md | Section 6.1 chain step 3 (symbol body) | `find_symbol` | floor | Read of the located range | none |
| sc-reflect-protocol/SKILL.md | Section 6.1 chain step 3b (polymorphic surface) | `find_implementations` | floor, best effort | Grep for `class .*\(<Base>\)`, `implements <Iface>`, `impl <Trait> for` | `implementation_coverage_pct`, `missing_implementations` |
| sc-reflect-protocol/SKILL.md | Section 6.1 chain step 4 (downstream impact and signatures) | `find_referencing_symbols` with `include_info:true` | floor | Grep with a word-boundary pattern, then Read each call site | `references_extended_info_used` kept as constant `false` |
| sc-reflect-protocol/SKILL.md | Section 6.1 steps 4b' and 4b (runtime-surface tagger and production-caller sweep) | `find_referencing_symbols` result reused, Wave-0 availability surface | floor | the step 4 Grep referrer result; a failed Grep or Read degrades the edge, no re-probe | `runtime_surface_*` (six fields), degraded token `runtime-surface:backend_unavailable` kept |
| sc-reflect-protocol/SKILL.md | Section 6.1 step 4a and the `reuse-auditor` fallback text | serena plus ripgrep skeleton degrade | floor | inline Grep skeleton-grep, findings capped at advisory L2 | `reuse_*`, `neighbour_search_degraded`, degraded token `neighbour-search:auggie_unavailable` |
| sc-reflect-protocol/SKILL.md | Section 6.1 step 4.5 (type hierarchy) | `type_hierarchy` | deleted | none | `type_hierarchy_invoked` constant `false`; `hierarchy_slice_path` and `hierarchy_coverage_pct` kept as constant `null`; telemetry `hierarchy_backend`, `hierarchy_nodes_examined`, `hierarchy_gaps_found` removed |
| sc-reflect-protocol/SKILL.md | Section 6.1 step 5 (diagnostics) | `get_diagnostics_for_file` | floor | the project's own linter or type-checker run through Bash under the section 6.1.1 envelope | `verification_ran`, `verification_invocations`, `verification_failures`, `verification_skip_reason` |
| sc-reflect-protocol/SKILL.md | Section 6.1 step 5.5 (verification run, formerly the verification triangle) | `execute_shell_command` | floor | Bash under the section 6.1.1 envelope | `verification_*`, `regression_present`, `verify_*` telemetry |
| sc-reflect-protocol/SKILL.md | Section 6.1 step 5.6 (contracted-sink reachability) | `find_referencing_symbols`, `execute_shell_command` (real-boot) | floor | step 4 referrer Grep; step 5.5 Bash boot | `reachability_*` |
| sc-reflect-protocol/SKILL.md | Section 6.1 step 7 (third-party dependency surface) | `find_symbol` with `search_deps:true` | deleted (skipped) | none; the dependent claim is marked `[INFERRED]` | `third_party_api_grounding` emitted as `[]`, `third_party_api_verified` emitted as `false` |
| sc-reflect-protocol/SKILL.md | Section 6.1 step 7' (change-summary corroboration) | `summarize_changes` | deleted | none | `serena_summary_corroboration` deleted (decision D4); `summarize_changes_invoked` kept as constant `false` |
| sc-reflect-protocol/SKILL.md | Section 6.1.1 (safety envelope, retitled "Bash verification safety envelope") | `execute_shell_command` envelope | floor | same nine controls and the "No-mutation gate." paragraph, now governing the Bash call; output cap applied to what is recorded | `verify_blocked`, `verify_blocked_reason`, `verify_timeout_hit`, `verify_flaky_suspected`, `verify_timeout_default`, `verify_invocations_path` |
| sc-reflect-protocol/SKILL.md | Section 6.4 (scripted checkpoints) | `think_about_collected_information`, `think_about_task_adherence`, `think_about_whether_you_are_done` | deleted | none | telemetry `serena_checkpoints_path` removed; grader type `checkpoint_logged` kept (reworded) |
| sc-reflect-protocol/SKILL.md | Section 6.5 (fail-open policy) | "every Serena call is fail-open" | floor | native Grep/Glob/Read is the permanent baseline; no degraded token for using it; auggie missing keeps `degraded_components: ["auggie"]` | `degraded_components` |
| sc-reflect-protocol/SKILL.md | Section 10.2 (Necessary deviation signals) | `find_symbol(search_deps:true)` | deleted | signal reworded: unverifiable upstream-API attribution is `[INFERRED]` | `third_party_api_verified` |
| sc-reflect-protocol/SKILL.md | Section 10.3 (Drift signals) | `summarize_changes` corroboration | deleted | none | `serena_summary_corroboration` deleted |
| sc-reflect-protocol/SKILL.md | Section 10.4 (Regression signals and gold-standard reference) | `get_diagnostics_for_file`, `execute_shell_command` | floor | step 5 linter / type-checker run and step 5.5 Bash exit codes | `regression_present`, `verification_regressions_detected` |
| sc-reflect-protocol/SKILL.md | Section 14 fallback table (Serena unavailable row, verification-unavailable row, `think_about_*` row, Wave 1B.3 referrer row) | all four rows | deleted (3 rows) / floor (2 rows reworded) | Bash-unavailable and `--no-verify` are the only verification-skip causes; Wave 1B.3 referrer failure reworded to Grep or Read failure | `verification_skip_reason` |
| sc-reflect-protocol/SKILL.md | Section 12.4 (`checkpoint_logged` grader), section 17 Will / Will Not, section 17.6 testability map | `think_about_*`, serena MCP | deleted / floor | wording only; the Will bullet now names the auggie + Grep/Read chain | none |

### `src/superclaude/skills/sc-reflect-protocol/refs/`

| File | Step heading / anchor | Former Serena tool | Action | Floor used | Contract fields touched |
|---|---|---|---|---|---|
| refs/cost-profile.yaml | Runtime-reachability gate comment (FR-RH1) | `find_referencing_symbols`, `execute_shell_command` | floor | step 4 referrer Grep, step 5.5 Bash | `reachability_*` cost keys unchanged |
| refs/coverage-mapping.md | S_dev_density, FR-1 missing-implementor term | `find_implementations` | floor, best effort | Grep for `class .*\(<Base>\)` / `implements <Iface>` | `implementation_coverage_pct`, `missing_implementations` |
| refs/coverage-mapping.md | FR-RV3-MED.1 hierarchy-gap weight paragraph | `type_hierarchy` | deleted | none | `hierarchy_gaps_found`, `hierarchy_coverage_pct` no longer feed S_dev_density |
| refs/deviation-taxonomy.md | Necessary deviation detection signals | `find_symbol(search_deps:true)` | deleted | `[INFERRED]` attribution | `third_party_api_verified` |
| refs/deviation-taxonomy.md | Drift detection signals | `summarize_changes` corroboration | deleted | none | `serena_summary_corroboration` deleted |
| refs/deviation-taxonomy.md | Regression detection signals and gold-standard reference | `get_diagnostics_for_file`, `execute_shell_command` | floor | project linter / type-checker through Bash; Bash exit codes under the section 6.1.1 envelope | `regression_present`, `verification_regressions_detected` |
| refs/grader-extensions.md | `checkpoint_logged` semantics | `think_about_*` checkpoints | deleted (wording) | named per-step audit-emit checkpoints | none |
| refs/ops-integration.md | Serena-adoption operator WARN catalog | `read_only`, `execute_shell_command` context-excluded, onboarding WARNs | deleted (Serena and onboarding entries); catalog retitled "Verification operator WARN catalog", with a new `tool-unavailable` entry and the generic `mutation-denied` and `metachar-denied` entries kept | Bash availability | `verification_skip_reason`, `verify_blocked_reason`, `onboarding_ran` constant `false` |
| refs/reflection-rubric.md | S_dev_density sub-terms: FR-6 onboarding weight, FR-7 context-exclusion up-weight | `get_current_config`, `list_memories` | deleted | none | `onboarding_status` weight gone; degraded token `serena:context-excluded` gone |
| refs/reflection-rubric.md | S_dev_density sub-term: FR-1 missing-implementor count | `find_implementations` | floor, best effort | Grep for `class .*\(<Base>\)` | `missing_implementations` |
| refs/reflection-rubric.md | S_dev_density sub-term: FR-RV3-MED.1 hierarchy-gap weight | `type_hierarchy` | deleted | none | `hierarchy_gaps_found`, `hierarchy_coverage_pct` |
| refs/reviewer-spec.md | Constraints (no shell execution) | `execute_shell_command` named in the denylist wording | floor (wording) | "no `Bash`" kept | none |
| refs/reviewer-spec.md | Grounding hunks: FR-1 implementor-list hunks | `find_implementations` | floor, best effort | Grep for `class .*\(<Base>\)` / `implements <Iface>` | `missing_implementations` |
| refs/reviewer-spec.md | Grounding hunks: FR-3 extended-info references | `find_referencing_symbols` with `include_info:true` | floor | Read of the referrers' call sites | `references_extended_info_used` constant `false` |
| refs/reviewer-spec.md | Grounding hunks: FR-RV3-MED.1 hierarchy-slice hunk | `type_hierarchy` | deleted | none | `hierarchy_slice_path` constant `null` |
| refs/runtime-surface.md | Section 2 language table intro | `find_referencing_symbols` | floor | step 4 referrer Grep | `runtime_surface_*` |

### Agents

| File | Step heading / anchor | Former Serena tool | Action | Floor used | Contract fields touched |
|---|---|---|---|---|---|
| agents/reflect-reviewer.md | Frontmatter `tools:` roster | `find_symbol`, `find_referencing_symbols`, `get_symbols_overview`, `get_diagnostics_for_file` | deleted | roster is now Read, Grep, Glob, auggie; Bash never added; diagnostics come from the orchestrator's verification leg as a grounding hunk | none |
| agents/reflect-reviewer.md | Layer ranking, L3 (no-mutation denylist) | `execute_shell_command` / serena path wording | floor (wording) | orchestrator's Bash verification call | none |
| agents/reuse-auditor.md | Frontmatter `tools:` roster | `find_symbol`, `get_symbols_overview`, `find_referencing_symbols` | deleted | roster is now Read, Grep, Glob, auggie | none |
| agents/reuse-auditor.md | Algorithm 1, facet F1 (I/O skeleton) | `get_symbols_overview` | floor | Grep for the file's definitions, then Read the body | none |
| agents/reuse-auditor.md | Algorithm 1, facet F4 (call-graph role) | `find_referencing_symbols` | floor | Grep with a word-boundary pattern for the symbol, then Read the call sites | none |
| agents/reuse-auditor.md | Algorithm 8, "auggie-unavailable" fallback | `find_symbol` | floor | Grep by capability tokens plus skeleton grep; findings still capped at advisory | `reuse_*`, degraded token `neighbour-search:auggie_unavailable` |

### Command copies (`commands/sc-reflect.md`, `plugins/superclaude/commands/reflect.md`, `src/superclaude/commands/reflect.md`)

| File | Step heading / anchor | Former Serena tool | Action | Floor used | Contract fields touched |
|---|---|---|---|---|---|
| src/superclaude/commands/reflect.md and plugins/superclaude/commands/reflect.md | Options table rows `--onboard`, `--with-hierarchy` | `onboarding`, `list_memories`, `type_hierarchy` | deleted | none | none |
| src/superclaude/commands/reflect.md and plugins/superclaude/commands/reflect.md | Options table row `--no-verify` | `execute_shell_command` | floor (wording) | Bash verification run | `verification_skip_reason` |
| src/superclaude/commands/reflect.md and plugins/superclaude/commands/reflect.md | Behavioral Summary tier table, Tier 1 row | "auggie/serena grounding" | floor (wording) | auggie plus native Grep/Read | none |
| src/superclaude/commands/reflect.md and plugins/superclaude/commands/reflect.md | MCP Integration (Serena bullet) and Tool Coordination (six `mcp__serena__*` bullets) | `find_symbol`, `find_referencing_symbols`, `get_symbols_overview`, `find_declaration`, `find_implementations`, `type_hierarchy`, `get_diagnostics_for_file`, `execute_shell_command`, `summarize_changes`, `onboarding`, `think_about_*` | floor (two bullets) / deleted | one Grep-then-Read navigation bullet and one Bash verification-run bullet | none |
| src/superclaude/commands/reflect.md and plugins/superclaude/commands/reflect.md | Boundaries, Will Not (`think_about_*` triad bullet) | `think_about_*` | deleted | none | none |
| commands/sc-reflect.md | Description, Behavioral Flow, Key behaviors, MCP Integration, Tool Coordination, Boundaries (legacy v1 text) | `think_about_task_adherence`, `think_about_collected_information`, `think_about_whether_you_are_done` | deleted (tool names) / floor (plain-language checks) | TodoRead/TodoWrite, Read, Grep, Glob | none |

### Tests updated with this task

| File | Anchor | Why |
|---|---|---|
| tests/cli/reflect/test_marker_suppression.py | `_extract_verification_envelope` (heading anchor `### 6.1.1 Bash verification safety envelope`) | follows the retitled section 6.1.1 heading |
| tests/cli/reflect/test_reviewer_readonly_tools.py | `_MUTATORS` set and module docstring | `execute_shell_command` no longer exists as a tool |
| tests/cli/reflect/test_reviewer_finding_parity.py | `_REMOVED_TOOLS` set | same |

## Task 14: troubleshoot, troubleshoot-analyst

### `src/superclaude/skills/sc-troubleshoot-protocol/`

| File | Step heading / anchor | Former Serena tool | Action | Floor used | Contract fields touched |
|---|---|---|---|---|---|
| sc-troubleshoot-protocol/SKILL.md | Frontmatter `allowed-tools` and `description` | `find_symbol`, `find_referencing_symbols`, `get_symbols_overview` | deleted | roster keeps Read, Grep, Glob, Bash, auggie | none |
| sc-troubleshoot-protocol/SKILL.md | Native diagnostic delegation, "Resolve before dispatch" (closed roster prose) | `find_symbol`, `find_referencing_symbols`, `get_symbols_overview`, `get_diagnostics_for_file` | deleted | roster is now Read, Grep, Glob, auggie (matches `agents/troubleshoot-analyst.md` and the `TOOLS` set in `tests/troubleshoot/test_diagnostic_worker_contract.py`) | none |
| sc-troubleshoot-protocol/SKILL.md | Wave 0 step 3 (resolve `--scope`) | auggie/serena scoping | floor (wording) | auggie queries plus Grep/Read lookups scoped to the target | none |
| sc-troubleshoot-protocol/SKILL.md | Wave 0 step 5, `SC:TROUBLESHOOT:TARGET` header | `mcps_available` value `serena` | deleted | none | audit header field `mcps_available` now `<auggie\|context7\|tavily\|none>` |
| sc-troubleshoot-protocol/SKILL.md | Wave 1 step 1 (Ground the symptom in real code) | `get_symbols_overview`, `find_symbol` | floor | existing Glob + Grep fallback kept; named function or class: Grep for `def name` / `class name` / `function name`, then Read the range; callers: Grep with a word-boundary pattern, then Read the call sites | none |
| sc-troubleshoot-protocol/SKILL.md | Wave 1 step 2 (Reproduce or observe), new lint/type bullet | `get_diagnostics_for_file` | floor | orchestrator runs the project's own linter or type-checker through Bash under the "Bash diagnostics safety envelope" (reflect section 6.1.1, retitled); `troubleshoot-analyst` never gains Bash | none |
| sc-troubleshoot-protocol/SKILL.md | Wave 1 exit criteria | "auggie + serena results" | floor (wording) | auggie results or Glob/Grep fallback | none |
| sc-troubleshoot-protocol/SKILL.md | Failure handling table, "MCP call fails" row | serena in "(auggie/serena)" | floor (wording) | Grep/Glob fallback | none |
| sc-troubleshoot-protocol/SKILL.md | Tool Coordination Summary, `mcp__serena__*` row and Bash row | `find_symbol`, `find_referencing_symbols`, `get_symbols_overview` | deleted (row) / floor (Bash row names the diagnostics envelope) | Read/Grep/Glob row already present | none |
| sc-troubleshoot-protocol/SKILL.md | Will Do, in-repo grounding bullet | auggie/serena | floor (wording) | auggie every tier plus Grep/Read floor | none |
| sc-troubleshoot-protocol/refs/diagnosability-audit.md | Section 1 (branch dispatch roster prose) | "Auggie/Serena tools" | deleted | roster prose now names only the Auggie retrieval tool | none |
| sc-troubleshoot-protocol/refs/triage-checklist.md | Pre-investigation grounding checklist | "serena symbol overview" | floor | Grep for the definition, then Read the range | none |

### Agent and command

| File | Step heading / anchor | Former Serena tool | Action | Floor used | Contract fields touched |
|---|---|---|---|---|---|
| agents/troubleshoot-analyst.md | Frontmatter `tools:` roster | `find_symbol`, `find_referencing_symbols`, `get_symbols_overview`, `get_diagnostics_for_file` | deleted | roster is now Read, Grep, Glob, auggie; Bash never added | none |
| agents/troubleshoot-analyst.md | Working rules, rule 1 | symbol/reference/diagnostics tools | floor | Grep for the definition then Read; Grep with a word-boundary pattern then Read the call sites; body states the orchestrator's verification leg covers diagnostics | none |
| commands/troubleshoot.md | Frontmatter `description`; Options rows `--scope`, `--no-mcp`; Tier table row Tier 1 | "auggie/serena" | floor (wording) | auggie plus Grep/Read floor | none |
| commands/troubleshoot.md | MCP Integration (Serena bullet) | `find_symbol`, `find_referencing_symbols`, `get_symbols_overview` | floor | "Native floor" bullet: Grep for the definition then Read; Grep with a word-boundary pattern then Read the call sites | none |
| commands/troubleshoot.md | Tool Coordination (`mcp__serena__*` bullet; Read/Grep/Glob and Bash bullets) | `find_symbol`, `find_referencing_symbols`, `get_symbols_overview` | deleted (bullet) / floor (two bullets reworded) | Read/Grep/Glob as the floor; Bash runs the project's linter or type-checker under the skill's diagnostics envelope | none |
| commands/troubleshoot.md | Examples (quick Tier 1, native-tools-only) and Boundaries, Will | "auggie + serena" | floor (wording) | auggie plus Grep/Read floor | none |

### Tests updated with this task

| File | Anchor | Why |
|---|---|---|
| tests/troubleshoot/test_diagnostic_worker_contract.py | `TOOLS` set and the `mcp__*` mutation list in `test_profile_guard_rejects_capability_mutants` | roster shrinks to Read, Grep, Glob, auggie; the old `mcp__serena__replace_content` mutant becomes an extra-auggie-tool mutant |

No twins carry Serena wording: `plugins/superclaude/commands/troubleshoot.md` and `commands/sc-troubleshoot.md` are different (older, generic) texts with no Serena mention; there is no plugin or root copy of the skill or the `troubleshoot-analyst` agent.

## Task 15: validate-roadmap, task, tasklist, auggie-review, brainstorm, cleanup-audit, modes, recommend, core refresh row

### `src/superclaude/skills/sc-validate-roadmap-protocol/SKILL.md` and `src/superclaude/commands/validate-roadmap.md`

| File | Step heading / anchor | Former Serena tool | Action | Floor used | Contract fields touched |
|---|---|---|---|---|---|
| commands/validate-roadmap.md | Frontmatter `allowed-tools` | `read_memory`, `write_memory`, `find_symbol`, `get_symbols_overview`, `search_for_pattern`, `activate_project` | deleted | roster keeps Read, Glob, Grep, Edit, Write, Bash, TodoWrite, Task, Skill and auggie | none |
| skills/sc-validate-roadmap-protocol/SKILL.md | Frontmatter `allowed-tools` | `find_symbol`, `get_symbols_overview`, `search_for_pattern`, `activate_project` | deleted | roster keeps Read, Glob, Grep, Edit, Write, Bash, TodoWrite, Task, Skill and auggie | none |
| skills/sc-validate-roadmap-protocol/SKILL.md | Section 4 Execution Vocabulary (three Serena tool rows) | `activate_project`, `find_symbol`, `get_symbols_overview` | deleted | Grep and Read rows already in the table | none |
| skills/sc-validate-roadmap-protocol/SKILL.md | Step 0.5 (Symbol Context Supplement, `--depth deep` only), Requires line and procedure steps 2-3 | `activate_project`, `find_symbol` (`include_body=False`), `get_symbols_overview` | floor | Grep for the definition (`def <name>\|class <name>\|function <name>`) then Read the range; one Read per file for the structural context; same 30-lookup hard cap | artifact `00-symbol-context-supplement.md` (INFORMATIONAL ONLY, same table columns) |
| skills/sc-validate-roadmap-protocol/SKILL.md | Step 0.5 failure handling | "skip entirely if Serena is unavailable, write no artifact" | floor | artifact is always written at `--depth deep`; unmatched symbols are `NOT_FOUND` rows; never skipped | `Symbols found: N / N attempted` line |
| skills/sc-validate-roadmap-protocol/SKILL.md | Relationship to CLI, crosswalk table, "Auggie/Serena enrichment" wording | none (prose) | deleted (wording) | "Auggie enrichment" | none |

### `src/superclaude/skills/sc-task-protocol/SKILL.md`, `src/superclaude/skills/sc-tasklist-protocol/SKILL.md`

| File | Step heading / anchor | Former Serena tool | Action | Floor used | Contract fields touched |
|---|---|---|---|---|---|
| skills/sc-task-protocol/SKILL.md | STANDARD Execution step 2 (downstream impacts) | `find_referencing_symbols` | floor | Grep with a word-boundary pattern for the changed symbol, then Read the call sites | none |
| skills/sc-task-protocol/SKILL.md | Tool Coordination, Execution Phase item 3 (trace dependencies) | `find_referencing_symbols` | floor | same Grep then Read | none |
| skills/sc-task-protocol/SKILL.md | MCP Integration, STRICT prerequisites | Serena as required server | deleted (already native: "STRICT: None required") | Read, Grep, Glob, Bash, codebase-retrieval | none |
| skills/sc-tasklist-protocol/SKILL.md | Section 5.5 MCP Tool Requirements table, STRICT row | Serena as required tool | deleted | row now `STRICT \| None \| Context7 \| Yes` | tier tool-requirement table |

### Auggie review

| File | Step heading / anchor | Former Serena tool | Action | Floor used | Contract fields touched |
|---|---|---|---|---|---|
| agents/auggie-reviewer.md | Frontmatter `tools:` roster | `find_symbol`, `find_referencing_symbols` | deleted | roster keeps Read, Grep, Glob, Bash, auggie; nothing added | none |
| agents/auggie-reviewer.md | Responsibilities item 2 (adjacent context) | `find_symbol` | floor | Read, with Grep for the definition when only the name is known | none |
| agents/auggie-reviewer.md | Tools list (Serena bullet) and Boundaries, Will | `find_symbol`, `find_referencing_symbols` | floor | Grep bullet gains the definition and word-boundary reference floor, Serena bullet deleted | none |
| commands/auggie-review.md | MCP Integration (Serena bullet) | symbol-level cross-reference of Auggie citations | floor | native Read / Grep floor bullet | none |

### Brainstorm

| File | Step heading / anchor | Former Serena tool | Action | Floor used | Contract fields touched |
|---|---|---|---|---|---|
| skills/sc-brainstorm-protocol/refs/handoff-routing.md | Codebase enrichment, former Tier 2 (fallback_1) | `get_symbols_overview`, `find_symbol` | deleted, tiers renumbered | native Glob/Grep is now Tier 2 (`fallback_1`); former Tier 3 and `fallback_2` are gone | `quality_tier` enum is now `primary \| fallback_1 \| skipped` |
| skills/sc-brainstorm-protocol/SKILL.md | Output artifacts item 3, Quality-tier tracking, state schema `quality_tier`, Error Handling Matrix codebase row | `get_symbols_overview` | deleted / renumbered | same renumbering | `quality_tier`, `enrichment_used` |
| commands/sc-brainstorm.md | MCP Integration bullet, two Examples comments | cross-session persistence wording | deleted (wording) | none | none |

### Cleanup audit, modes, recommend, core rules

| File | Step heading / anchor | Former Serena tool | Action | Floor used | Contract fields touched |
|---|---|---|---|---|---|
| skills/sc-cleanup-audit-protocol/SKILL.md | MCP Integration (Serena bullet, import chain tracing) | symbol lookup / references | floor | Grep with a word-boundary pattern then Read the call sites; Grep for the definition then Read the range. The `.serena/` ignore in the exclusion list stays (allowlisted) | none |
| modes/MODE_Orchestration.md and plugins/superclaude/modes/MODE_Orchestration.md | Tool Selection Matrix, "Symbol operations" row | symbol operations | deleted | row removed (Phase 3 may add a codegraph row) | none |
| skills/sc-recommend/refs/delegation-vs-native-heuristics.md and plugins/superclaude/skills/sc-recommend/refs/delegation-vs-native-heuristics.md | Specialized capability table, "Repository-wide semantic ranking" row | "auggie/serena" | floor (wording) | "auggie beats brute Grep" | none |
| core/CLAUDE.md | Refresh-tool selection table, "Symbolic queries" row | `find_symbol`, `find_referencing_symbols` | floor | Grep for the definition and references, then Read (Phase 3 adds codegraph above this) | none |

### Coverage index: every load-bearing file of source section 4.2

Phase 3 reads the per-task blocks above; this index confirms none is missing. Every path is relative to `src/superclaude/`.

| File | Ledger block | Role |
|---|---|---|
| commands/troubleshoot.md | Task 14, Agent and command | SYM |
| skills/sc-reflect-protocol/SKILL.md | Task 13 | SYM, REF, DIAG, ALLOW, CONTRACT |
| skills/sc-troubleshoot-protocol/SKILL.md | Task 14 | SYM, ALLOW |
| skills/sc-validate-roadmap-protocol/SKILL.md | Task 15, validate-roadmap | SYM, ALLOW |
| commands/validate-roadmap.md | Task 15, validate-roadmap | ALLOW |
| agents/reuse-auditor.md | Task 13, Agents | REF, G5 roster |
| agents/reflect-reviewer.md | Task 13, Agents | G5 roster |
| agents/troubleshoot-analyst.md | Task 14, Agent and command | G5 roster |
| agents/auggie-reviewer.md | Task 15, Auggie review | G5 roster |
| hooks/hooks.json (and plugins/superclaude/hooks/hooks.json) | Task 8 (no step block: a matcher edit, not a primitive step) | EDIT: the PreToolUse matcher lost its four `mcp__serena__*` alternatives and is now `Edit\|Write`; action deleted, no floor needed (Edit and Write are native) |
| hooks/scripts/freshness-pre-edit.sh (and plugins/superclaude/hooks/scripts/freshness-pre-edit.sh) | Task 8 (no step block: a script edit, not a primitive step) | EDIT: the `relative_path` branch (Serena's argument name) was deleted; the script reads `file_path` only; action deleted, no floor needed |

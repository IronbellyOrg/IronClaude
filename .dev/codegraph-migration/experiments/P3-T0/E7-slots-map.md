# E7-slots-map (Phase 3 Task 2, prerequisite experiment E-7)

Date: 2026-10-31. Input: `.dev/codegraph-migration/handoffs/phase3-codegraph-slots.md` (Phase 1 slots ledger, 226 lines). Output: one line per ledger row, mapped to the row of source §1.2 (`./source.md` of the plan package) that adds the codegraph tier or the codegraph names at that anchor, or `no tier: <reason>` when no §1.2 row adds codegraph there.

## Counting rule (self decision, logged in `.dev/codegraph-migration/decisions/P3X-execution-log.md`)

The ledger is not one Markdown table: it holds 12 step tables (columns File | Step heading / anchor | Former Serena tool | Action | Floor used | Contract fields touched), 2 "Tests updated with this task" tables and 1 coverage index. So the plan's `rg -c '^\| '` formula (which counts every header, test row and index row of all 15 tables) does not apply, and the count is by hand:

- every data row of the 12 step tables is a ledger row: 18 + 32 + 16 + 6 + 6 + 12 + 6 + 6 + 4 + 4 + 3 + 4 = **117**;
- the coverage index adds 2 touched steps that have no step-table row (the `hooks/hooks.json` matcher and `hooks/scripts/freshness-pre-edit.sh`, both "Task 8 (no step block)"); its other 9 rows only point at step tables already counted: **2**;
- the 2 "Tests updated" tables list test files, not primitive steps: **0**.

Total: **119** ledger rows, so this map has 119 lines below.

Mapping rule: `row <n>` when §1.2 row n changes that anchor to use or name codegraph; `no tier: <reason>` when the step is memory, activation, onboarding, a nudge, type hierarchy, diagnostics or verification on Bash, a dependency lookup, or wording only. A ledger row that covers two §1.2 rows names the one whose anchor comes first in the ledger text. Every ledger row fits a §1.2 row or a no-tier reason, so there is no H4 item. Two rows where Phase 1 removed a step that a §1.2 row rewrites, both anticipated by the ledger text and resolved without H4: the `MODE_Orchestration.md` Tool Selection Matrix row (ledger: "row removed (Phase 3 may add a codegraph row)"; §1.2 row 4 adds the codegraph row back) and the brainstorm Tier 2 (ledger: former Serena Tier 2 deleted and native Glob/Grep renumbered to Tier 2 `fallback_1`; §1.2 row 32 puts the codegraph lookup above that floor and keeps the quality tier names unchanged).

## Map

### Tasks 10 to 12 (decorative mentions and memory steps)

- 48 command, skill and agent files :: frontmatter `mcp-servers:` list :: row 40
- core/CLAUDE.md :: MCP server table; freshness rule S2 :: row 1
- core/RESEARCH_CONFIG.md and plugins/superclaude/core/RESEARCH_CONFIG.md :: `memory` tool entry; tool-fallback table :: no tier: memory backend, codegraph takes no memory job (row 41)
- skills/sc-adversarial-protocol/SKILL.md :: MCP Integration table; `mcp_integration` YAML; framework registration lines :: no tier: persistence rows deleted, memory job (row 41)
- skills/sc-post-release-protocol/SKILL.md :: telemetry `mcps_available` enum :: no tier: deleted enum value; post-release uses no symbol lookup
- skills/sc-roadmap-protocol/SKILL.md :: Post-Wave completion step 2; MCP table; circuit-breaker bullet; save points; resume protocol; graceful degradation; Boundaries :: no tier: session memory file store (row 41)
- commands/research.md (src, plugins, commands/sc-research.md); commands/sc-help.md; commands/sc-task.md; commands/sc-workflow.md :: MCP bullets, help rows, examples :: no tier: memory and persistence wording deleted (row 41)
- commands/save.md, load.md, pm.md (src, plugins, commands/sc-*.md) :: Memory Store / MCP Integration; tool coordination; flow examples :: no tier: memory file store (row 41); the `/sc:load` readiness line is new work of Task 12, not a tier above this floor
- agents/pm-agent.md (src, plugins, agents/sc-pm-agent.md) :: session start, checkpoints, mistake log, monthly maintenance, self-evaluation :: no tier: memory file store and nudges (row 41)
- modes/MODE_Task_Management.md (src, plugins) :: memory schema, phase / task / todo keys, checkpoints :: no tier: memory file store (row 41)
- skills/sc-pm-protocol/SKILL.md :: lifecycle steps :: no tier: memory file store (row 41)
- commands/reflect.md (src, plugins, commands/sc-reflect.md) and skills/sc-reflect-protocol/SKILL.md section 6.3 :: calibration hydrate, last-pass, handoff persistence :: no tier: memory file store (row 41)
- skills/sc-reflect-protocol/refs/input-resolution.md :: Auggie plus Serena availability bullets :: no tier: availability probe deleted; readiness comes from the shared guide (row 41)
- skills/sc-reflect-protocol/refs/remediation-handoff.md :: handoff location :: no tier: memory file store (row 41)
- skills/sc-validate-roadmap-protocol/SKILL.md :: Hooks 0a-0c and 6a-6d; Pre-Phase 0 project activation :: no tier: memory and activation (row 41)
- skills/sc-task-protocol/SKILL.md :: STRICT tier prerequisites, memory read, completion write :: no tier: memory and activation (row 34 deletes them; its STRICT step 7 tier maps from the Task 15 rows)
- skills/sc-crash-recovery/SKILL.md, refs/investigators.md, refs/report-template.md, scripts/bootstrap_scan.sh :: investigator #3; report section; JSON fields :: no tier: memory directory (row 41)
- core/HOW-WE-WORK.md and plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md :: routing-guide wording for session memory :: no tier: memory wording (row 41); the routing rows for the new commands are new work of Task 12

### Task 13: `sc-reflect-protocol/SKILL.md`

- sc-reflect-protocol/SKILL.md :: Frontmatter `allowed-tools` :: row 19
- sc-reflect-protocol/SKILL.md :: Wave diagram, Wave 0 / Step 0.5c (active-project config probe) :: no tier: activation probe deleted (row 41)
- sc-reflect-protocol/SKILL.md :: Step 0.5d (verification and adoption availability probe) :: no tier: Serena availability probe deleted; verification gates on Bash (P3-D5)
- sc-reflect-protocol/SKILL.md :: Step 0.7 (activate project, memory hydrate, onboarding-status parse) :: no tier: memory hydrate and activation (row 41)
- sc-reflect-protocol/SKILL.md :: Step 0.7b (onboarding bootstrap) and flag `--onboard` :: no tier: onboarding deleted (row 41)
- sc-reflect-protocol/SKILL.md :: Step 1B.3 sub-step 1a (declaration anchor for each hunk) :: row 20
- sc-reflect-protocol/SKILL.md :: Step 1B.3 sub-step 1 (touched symbols per task) :: row 20
- sc-reflect-protocol/SKILL.md :: Step 1B.3 sub-step 3 (shared-vs-collision check) :: row 20
- sc-reflect-protocol/SKILL.md :: Step 1B.3 sub-step 3a (shared base-class lineage) and flag `--with-hierarchy` :: no tier: type hierarchy dropped (P3-D6, rows 20 and 26)
- sc-reflect-protocol/SKILL.md :: Section 6 title and intro (Modern Serena Tool Usage) :: row 21
- sc-reflect-protocol/SKILL.md :: Section 6.1 chain step 1 (activate project) :: no tier: activation deleted (row 21 step 1)
- sc-reflect-protocol/SKILL.md :: Section 6.1 chain step 2 (structural map of a file) :: row 21
- sc-reflect-protocol/SKILL.md :: Section 6.1 chain step 2a (hunk to declaration) :: row 21
- sc-reflect-protocol/SKILL.md :: Section 6.1 chain step 3 (symbol body) :: row 21
- sc-reflect-protocol/SKILL.md :: Section 6.1 chain step 3b (polymorphic surface) :: row 21
- sc-reflect-protocol/SKILL.md :: Section 6.1 chain step 4 (downstream impact and signatures) :: row 21
- sc-reflect-protocol/SKILL.md :: Section 6.1 steps 4b' and 4b (runtime-surface tagger and production-caller sweep) :: row 21
- sc-reflect-protocol/SKILL.md :: Section 6.1 step 4a and the `reuse-auditor` fallback text :: row 21
- sc-reflect-protocol/SKILL.md :: Section 6.1 step 4.5 (type hierarchy) :: no tier: type hierarchy dropped (P3-D6, row 21 step 4.5)
- sc-reflect-protocol/SKILL.md :: Section 6.1 step 5 (diagnostics) :: no tier: diagnostics stay on Bash (P3-D5, row 21 step 5)
- sc-reflect-protocol/SKILL.md :: Section 6.1 step 5.5 (verification run, formerly the verification triangle) :: no tier: verification stays on Bash (P3-D5, row 21 step 5.5)
- sc-reflect-protocol/SKILL.md :: Section 6.1 step 5.6 (contracted-sink reachability) :: row 21
- sc-reflect-protocol/SKILL.md :: Section 6.1 step 7 (third-party dependency surface) :: no tier: dependency dirs are not indexed; Phase 1's `[INFERRED]` text stays (row 21 step 7)
- sc-reflect-protocol/SKILL.md :: Section 6.1 step 7' (change-summary corroboration) :: no tier: `summarize_changes` deleted (row 21 step 7')
- sc-reflect-protocol/SKILL.md :: Section 6.1.1 (safety envelope, retitled "Bash verification safety envelope") :: no tier: Bash envelope; Phase 3 only verifies the heading (row 23)
- sc-reflect-protocol/SKILL.md :: Section 6.4 (scripted checkpoints) :: no tier: `think_about_*` checkpoints deleted
- sc-reflect-protocol/SKILL.md :: Section 6.5 (fail-open policy) :: row 24
- sc-reflect-protocol/SKILL.md :: Section 10.2 (Necessary deviation signals) :: no tier: upstream-API attribution stays `[INFERRED]`
- sc-reflect-protocol/SKILL.md :: Section 10.3 (Drift signals) :: no tier: `summarize_changes` corroboration deleted
- sc-reflect-protocol/SKILL.md :: Section 10.4 (Regression signals and gold-standard reference) :: no tier: diagnostics and verification stay on Bash (P3-D5)
- sc-reflect-protocol/SKILL.md :: Section 14 fallback table (Serena unavailable row, verification-unavailable row, `think_about_*` row, Wave 1B.3 referrer row) :: row 25
- sc-reflect-protocol/SKILL.md :: Section 12.4 (`checkpoint_logged` grader), section 17 Will / Will Not, section 17.6 testability map :: no tier: grader and boundary wording only

### Task 13: `sc-reflect-protocol/refs/`

- refs/cost-profile.yaml :: Runtime-reachability gate comment (FR-RH1) :: row 28
- refs/coverage-mapping.md :: S_dev_density, FR-1 missing-implementor term :: row 28
- refs/coverage-mapping.md :: FR-RV3-MED.1 hierarchy-gap weight paragraph :: no tier: type hierarchy deleted (row 28, P3-D6)
- refs/deviation-taxonomy.md :: Necessary deviation detection signals :: no tier: upstream-API attribution stays `[INFERRED]`
- refs/deviation-taxonomy.md :: Drift detection signals :: no tier: `summarize_changes` corroboration deleted
- refs/deviation-taxonomy.md :: Regression detection signals and gold-standard reference :: no tier: diagnostics and verification stay on Bash (P3-D5)
- refs/grader-extensions.md :: `checkpoint_logged` semantics :: no tier: checkpoint wording only
- refs/ops-integration.md :: Serena-adoption operator WARN catalog :: no tier: Serena and onboarding WARN entries deleted
- refs/reflection-rubric.md :: S_dev_density sub-terms: FR-6 onboarding weight, FR-7 context-exclusion up-weight :: no tier: onboarding and context weights deleted
- refs/reflection-rubric.md :: S_dev_density sub-term: FR-1 missing-implementor count :: row 28
- refs/reflection-rubric.md :: S_dev_density sub-term: FR-RV3-MED.1 hierarchy-gap weight :: no tier: type hierarchy deleted (row 28, P3-D6)
- refs/reviewer-spec.md :: Constraints (no shell execution) :: no tier: "no `Bash`" wording only
- refs/reviewer-spec.md :: Grounding hunks: FR-1 implementor-list hunks :: row 28
- refs/reviewer-spec.md :: Grounding hunks: FR-3 extended-info references :: row 28
- refs/reviewer-spec.md :: Grounding hunks: FR-RV3-MED.1 hierarchy-slice hunk :: no tier: type hierarchy deleted (row 28, P3-D6)
- refs/runtime-surface.md :: Section 2 language table intro :: row 28

### Task 13: agents

- agents/reflect-reviewer.md :: Frontmatter `tools:` roster :: row 7
- agents/reflect-reviewer.md :: Layer ranking, L3 (no-mutation denylist) :: no tier: denylist wording; verification is the orchestrator's Bash call
- agents/reuse-auditor.md :: Frontmatter `tools:` roster :: row 8
- agents/reuse-auditor.md :: Algorithm 1, facet F1 (I/O skeleton) :: row 9
- agents/reuse-auditor.md :: Algorithm 1, facet F4 (call-graph role) :: row 10
- agents/reuse-auditor.md :: Algorithm 8, "auggie-unavailable" fallback :: row 11

### Task 13: reflect command copies

- src/superclaude/commands/reflect.md and plugins/superclaude/commands/reflect.md :: Options table rows `--onboard`, `--with-hierarchy` :: no tier: flags removed (row 26, P3-D6)
- src/superclaude/commands/reflect.md and plugins/superclaude/commands/reflect.md :: Options table row `--no-verify` :: no tier: Bash verification wording
- src/superclaude/commands/reflect.md and plugins/superclaude/commands/reflect.md :: Behavioral Summary tier table, Tier 1 row :: row 29
- src/superclaude/commands/reflect.md and plugins/superclaude/commands/reflect.md :: MCP Integration (Serena bullet) and Tool Coordination (six `mcp__serena__*` bullets) :: row 29
- src/superclaude/commands/reflect.md and plugins/superclaude/commands/reflect.md :: Boundaries, Will Not (`think_about_*` triad bullet) :: no tier: `think_about_*` deleted
- commands/sc-reflect.md :: Description, Behavioral Flow, Key behaviors, MCP Integration, Tool Coordination, Boundaries (legacy v1 text) :: no tier: legacy v1 root copy has no lookup step, only plain-language checks

### Task 14: `sc-troubleshoot-protocol/`

- sc-troubleshoot-protocol/SKILL.md :: Frontmatter `allowed-tools` and `description` :: row 14
- sc-troubleshoot-protocol/SKILL.md :: Native diagnostic delegation, "Resolve before dispatch" (closed roster prose) :: row 5
- sc-troubleshoot-protocol/SKILL.md :: Wave 0 step 3 (resolve `--scope`) :: row 16
- sc-troubleshoot-protocol/SKILL.md :: Wave 0 step 5, `SC:TROUBLESHOOT:TARGET` header :: row 16
- sc-troubleshoot-protocol/SKILL.md :: Wave 1 step 1 (Ground the symptom in real code) :: row 15
- sc-troubleshoot-protocol/SKILL.md :: Wave 1 step 2 (Reproduce or observe), new lint/type bullet :: no tier: diagnostics stay on Bash (P3-D5)
- sc-troubleshoot-protocol/SKILL.md :: Wave 1 exit criteria :: row 16
- sc-troubleshoot-protocol/SKILL.md :: Failure handling table, "MCP call fails" row :: row 16
- sc-troubleshoot-protocol/SKILL.md :: Tool Coordination Summary, `mcp__serena__*` row and Bash row :: row 16
- sc-troubleshoot-protocol/SKILL.md :: Will Do, in-repo grounding bullet :: row 16
- sc-troubleshoot-protocol/refs/diagnosability-audit.md :: Section 1 (branch dispatch roster prose) :: row 18
- sc-troubleshoot-protocol/refs/triage-checklist.md :: Pre-investigation grounding checklist :: row 17

### Task 14: agent and command

- agents/troubleshoot-analyst.md :: Frontmatter `tools:` roster :: row 5
- agents/troubleshoot-analyst.md :: Working rules, rule 1 :: row 6
- commands/troubleshoot.md :: Frontmatter `description`; Options rows `--scope`, `--no-mcp`; Tier table row Tier 1 :: row 13
- commands/troubleshoot.md :: MCP Integration (Serena bullet) :: row 13
- commands/troubleshoot.md :: Tool Coordination (`mcp__serena__*` bullet; Read/Grep/Glob and Bash bullets) :: row 13
- commands/troubleshoot.md :: Examples (quick Tier 1, native-tools-only) and Boundaries, Will :: row 13

### Task 15: validate-roadmap

- commands/validate-roadmap.md :: Frontmatter `allowed-tools` :: row 30
- skills/sc-validate-roadmap-protocol/SKILL.md :: Frontmatter `allowed-tools` :: row 30
- skills/sc-validate-roadmap-protocol/SKILL.md :: Section 4 Execution Vocabulary (three Serena tool rows) :: row 30
- skills/sc-validate-roadmap-protocol/SKILL.md :: Step 0.5 (Symbol Context Supplement, `--depth deep` only), Requires line and procedure steps 2-3 :: row 31
- skills/sc-validate-roadmap-protocol/SKILL.md :: Step 0.5 failure handling :: row 31
- skills/sc-validate-roadmap-protocol/SKILL.md :: Relationship to CLI, crosswalk table, "Auggie/Serena enrichment" wording :: no tier: wording only ("Auggie enrichment")

### Task 15: task and tasklist

- skills/sc-task-protocol/SKILL.md :: STANDARD Execution step 2 (downstream impacts) :: row 33
- skills/sc-task-protocol/SKILL.md :: Tool Coordination, Execution Phase item 3 (trace dependencies) :: row 33
- skills/sc-task-protocol/SKILL.md :: MCP Integration, STRICT prerequisites :: row 34
- skills/sc-tasklist-protocol/SKILL.md :: Section 5.5 MCP Tool Requirements table, STRICT row :: row 35

### Task 15: auggie review

- agents/auggie-reviewer.md :: Frontmatter `tools:` roster :: row 12
- agents/auggie-reviewer.md :: Responsibilities item 2 (adjacent context) :: row 12
- agents/auggie-reviewer.md :: Tools list (Serena bullet) and Boundaries, Will :: row 12
- commands/auggie-review.md :: MCP Integration (Serena bullet) :: row 38

### Task 15: brainstorm

- skills/sc-brainstorm-protocol/refs/handoff-routing.md :: Codebase enrichment, former Tier 2 (fallback_1) :: row 32
- skills/sc-brainstorm-protocol/SKILL.md :: Output artifacts item 3, Quality-tier tracking, state schema `quality_tier`, Error Handling Matrix codebase row :: row 32
- commands/sc-brainstorm.md :: MCP Integration bullet, two Examples comments :: no tier: cross-session persistence wording deleted

### Task 15: cleanup audit, modes, recommend, core rules

- skills/sc-cleanup-audit-protocol/SKILL.md :: MCP Integration (Serena bullet, import chain tracing) :: row 37
- modes/MODE_Orchestration.md and plugins/superclaude/modes/MODE_Orchestration.md :: Tool Selection Matrix, "Symbol operations" row :: row 4
- skills/sc-recommend/refs/delegation-vs-native-heuristics.md and plugins/superclaude/skills/sc-recommend/refs/delegation-vs-native-heuristics.md :: Specialized capability table, "Repository-wide semantic ranking" row :: row 36
- core/CLAUDE.md :: Refresh-tool selection table, "Symbolic queries" row :: row 3

### Coverage index: steps with no step-table row

- hooks/hooks.json (and plugins/superclaude/hooks/hooks.json) :: PreToolUse matcher :: no tier: matcher is `Edit|Write`; codegraph adds no edit tool (row 42)
- hooks/scripts/freshness-pre-edit.sh (and plugins/superclaude/hooks/scripts/freshness-pre-edit.sh) :: `relative_path` branch :: no tier: script reads `file_path` only; codegraph adds no edit tool (row 42)

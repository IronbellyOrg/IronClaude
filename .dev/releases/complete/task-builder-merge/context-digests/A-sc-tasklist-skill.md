# Bucket A — sc-tasklist-protocol skill content digest

## Files read

| Path | Lines | Status |
|---|---|---|
| `src/superclaude/skills/sc-tasklist-protocol/SKILL.md` | 1390 | read fully (chunks: 1-350, 350-749, 750-1149, 1150-1389) |
| `src/superclaude/skills/sc-tasklist-protocol/rules/file-emission-rules.md` | 59 | read fully |
| `src/superclaude/skills/sc-tasklist-protocol/rules/tier-classification.md` | 103 | read fully |
| `src/superclaude/skills/sc-tasklist-protocol/templates/index-template.md` | 122 | read fully |
| `src/superclaude/skills/sc-tasklist-protocol/templates/phase-template.md` | 116 | read fully |

---

## Core architecture (10-stage pipeline)

The skill executes a deterministic, fully-gated 10-stage pipeline. The stage table is enumerated at SKILL.md:1296-1307 and per-stage completion messages at SKILL.md:1351-1361.

| Stage | What it does | What it produces | Gate (blocks advancement) |
|---|---|---|---|
| **1. Input Ingest** | Read roadmap text (SKILL.md:47-56); optional `--spec` TDD load (SKILL.md:160-174); optional `--prd-file` PRD load (SKILL.md:175-186); auto-wire from `.roadmap-state.json` (SKILL.md:188-202) | parsed roadmap text + `supplementary_context` + `prd_context` | "Roadmap text non-empty; required sections present; file read succeeded" (SKILL.md:1298) |
| **2. Parse + Phase Bucketing** | Split into roadmap items (SKILL.md:148-155), assign `R-###` IDs in appearance order (SKILL.md:156-159), create phase buckets from explicit labels or `##` headings or 3 default buckets (SKILL.md:204-213), renumber phases sequentially with no gaps (SKILL.md:215-219) | `R-###` registry + phase bucket list | "Every roadmap item assigned to exactly one phase; phase count >= 1" (SKILL.md:1299) |
| **3. Task Conversion** | 1 task per item by default; split only on 2+ independent deliverables (SKILL.md:221-230); zero-padded `T<PP>.<TT>` IDs (SKILL.md:276-280); supplementary TDD task generation (SKILL.md:231-252); supplementary PRD task generation (SKILL.md:253-274); clarification tasks when info missing (SKILL.md:285-301) | task stubs with IDs | "All items converted to task stubs; IDs assigned with no collisions; titles non-empty" (SKILL.md:1300) |
| **4. Enrichment** | Effort + Risk labels (SKILL.md:460-503); compliance tier classification (SKILL.md:505-562); confidence scoring (SKILL.md:564-575); MCP tool requirements (SKILL.md:577-585); sub-agent delegation (SKILL.md:587-594); verification routing (SKILL.md:393-401); critical path override (SKILL.md:403-410); acceptance criteria + validation (SKILL.md:303-322); checkpoints every 5 tasks + end-of-phase (SKILL.md:324-372) | fully decorated tasks | "All tasks have non-empty: Effort, Risk, Tier, Confidence score" (SKILL.md:1301) |
| **5. File Emission** | Write `tasklist-index.md` + N `phase-N-tasklist.md` files; create directories via `Bash mkdir -p` (SKILL.md:1376) | N+1 files at `TASKLIST_ROOT` | "index written; all phase files referenced exist on disk; no extra phase files" (SKILL.md:1302) |
| **6. Self-Check** | Run 17-point pre-write gate (SKILL.md:979-1034) — semantic + structural quality gates | gate verdict | "All Sprint Compatibility Self-Check assertions pass; no blocking failures" (SKILL.md:1303) |
| **7. Roadmap Validation** | Spawn 2N parallel agents (one A and one B per phase); each agent validates a 50% task slice against the roadmap (SKILL.md:1087-1148); merge + dedupe findings (SKILL.md:1129-1135); retry once on agent failure (SKILL.md:1150) | consolidated findings list | "2N agents completed; findings merged and deduped; zero agent failures" (SKILL.md:1304) |
| **8. Patch Plan Generation** | Short-circuit to clean `ValidationReport.md` if zero findings (SKILL.md:1156-1163); otherwise write `ValidationReport.md` + `PatchChecklist.md` to `TASKLIST_ROOT/validation/` (SKILL.md:1165-1242) | 2 validation artifacts | "Both artifacts written; OR clean report if zero issues" (SKILL.md:1305) |
| **9. Patch Execution** | Delegate to `sc:task` via `Skill` tool with `--compliance strict` (SKILL.md:1244-1260); orchestrator does NOT apply patches itself (SKILL.md:1258) | edited phase files | "sc:task --compliance strict completed; all checklist items addressed" (SKILL.md:1306) |
| **10. Spot-Check Verification** | Single non-parallel pass over each Stage-7 finding; record `RESOLVED`/`UNRESOLVED` (SKILL.md:1262-1287); does NOT loop on UNRESOLVED (SKILL.md:1288) | `## Verification Results` appended to `ValidationReport.md` | "All findings re-verified; results appended" (SKILL.md:1307) |

Dependency chain: each stage blockedBy the previous (SKILL.md:1317-1321, 1340-1349). Structural gates are blocking; semantic gates advisory (SKILL.md:1311-1313).

---

## Deterministic generation primitives

- **Keyword-based scoring** for tier (STRICT +0.4, EXEMPT +0.4, LIGHT +0.3, STANDARD +0.2 per match): SKILL.md:525-547; rules/tier-classification.md:33-54.
- **Appearance-order ID assignment**:
  - Roadmap items `R-001, R-002, ...` in scan order (SKILL.md:156-159).
  - Tasks `T<PP>.<TT>` zero-padded (SKILL.md:276-280).
  - Deliverables `D-0001, D-0002, ...` global appearance order (SKILL.md:419-426).
  - Checkpoint deliverables `D-CP<PP>` / `D-CP<PP>-MID` reserved namespace, no collision with `D-####` (SKILL.md:437-458).
- **Explicit tiebreakers** (4-rule cascade for "policy forks"): roadmap-named > no new deps > reversible > fewest interface changes (SKILL.md:374-383).
- **Tier conflict resolution priority**: `STRICT (1) > EXEMPT (2) > LIGHT (3) > STANDARD (4)` (SKILL.md:385-391; rules/tier-classification.md:9-11; appendix SKILL.md:1050-1053).
- **Tier classification — full inputs**:
  - Compound phrase overrides checked FIRST with +0.15 confidence boost (SKILL.md:510-523; rules/tier-classification.md:15-31).
  - Keyword matching per tier (SKILL.md:525-547).
  - Context boosters: file count, path patterns, operation type (SKILL.md:548-562; rules/tier-classification.md:57-71).
  - 4-tier scheme: STRICT / STANDARD / LIGHT / EXEMPT (SKILL.md:33-43, throughout).
  - Confidence scoring: base = max(tier_scores) capped 0.95; -15% if top two within 0.1; +15% if compound matched; -30% if no keywords (SKILL.md:564-575).
- **Effort score** (0→XS … 4+→XL) computed from text length, split flag, domain keywords, dependency words (SKILL.md:466-481).
- **Risk score** (0-1→Low, 2-3→Medium, 4+→High) computed from security/data/auth/perf/cross-cutting keyword categories (SKILL.md:486-500).
- **Critical Path Override** when paths match `auth/`, `security/`, `crypto/`, `models/`, `migrations/` → forces CRITICAL verification regardless of tier (SKILL.md:403-410).
- **TASKLIST_ROOT derivation** (3-rule cascade): `.dev/releases/current/<segment>/` substring match → version token → `v0.0-unknown` (SKILL.md:64-72).

---

## Quality gates

- **17-point pre-write gate** — enumerated as checks 1-20 across three sections (8 Sprint Compatibility checks SKILL.md:983-993, 4 Semantic Quality checks SKILL.md:996-1003, 8 Structural Quality checks in table SKILL.md:1023-1032). The skill labels them "17 checks" in the Stage 6 completion message at SKILL.md:1357. Exhaustive list:
  1. `tasklist-index.md` exists with "Phase Files" table (SKILL.md:985)
  2. Every phase file in index exists in bundle (SKILL.md:986)
  3. Phase numbers contiguous 1..N (SKILL.md:987)
  4. All task IDs match `T<PP>.<TT>` zero-padded (SKILL.md:988)
  5. Every phase file starts `# Phase N -- <Name>` (SKILL.md:989)
  6. Every phase ends with end-of-phase checkpoint (SKILL.md:990)
  7. No phase file contains registry/matrix/template sections (SKILL.md:991)
  8. Index contains literal phase filenames (SKILL.md:992)
  9. Every task non-empty Effort/Risk/Tier/Confidence/Verification Method (SKILL.md:998)
  10. All `D-####` globally unique (SKILL.md:999)
  11. No placeholder/empty task descriptions (no "TBD"/"TODO"/title-only) (SKILL.md:1000)
  12. Every task has >=1 `R-###` (no orphans) (SKILL.md:1001)
  13. Phase task count >=1 and <=25 (SKILL.md:1025)
  14. Clarification Task adjacency before blocked task (SKILL.md:1026)
  15. Circular dependency detection (no A→B→C→A) (SKILL.md:1027)
  16. XL splitting enforcement (must have subtasks) (SKILL.md:1028)
  17. Confidence bar format consistency (SKILL.md:1029)
  18. Checkpoint task emission as `### T<PP>.<NN> -- Checkpoint:` (SKILL.md:1030)
  19. End-of-phase position has highest `<NN>` in phase (SKILL.md:1031)
  20. Checkpoint Report Path line present below metadata (SKILL.md:1032)
- **Write atomicity**: "All files are written only after the full bundle passes validation. No partial bundle writes are permitted." (SKILL.md:1042)
- **Gate failure → no write**: "All checks in this section MUST pass before any `Write()` call. Invalid output is never written." (SKILL.md:981); "If any check 1-20 fails, fix it before writing any output file." (SKILL.md:1034)
- **Task Specificity Check** (generation-discipline, not parse): named artifact, no external-conversation pronouns, imperative verb + object (SKILL.md:1005-1019; also SKILL.md:957-975).
- **Near-Field Completion Criterion**: first AC bullet MUST name a specific verifiable output; rejected forms enumerated (SKILL.md:838-854; templates/phase-template.md:73-86).
- **Acceptance Criteria Specificity Rules** (tier-proportional): STRICT all AC artifact-referencing, STANDARD ≥1, LIGHT/EXEMPT no minimum (SKILL.md:856-862; templates/phase-template.md:88-91).

---

## Validation pipeline (Stages 7-10)

- **2N parallel agent architecture**: For each of N phases, spawn Agent A (tasks 1..ceil(count/2)) and Agent B (tasks ceil+1..count) via `Task` tool in parallel, totaling 2N agents (SKILL.md:1091-1106).
- **Agent prompt content** (verbatim instructions block): SKILL.md:1108-1127. Each agent checks 5 categories per task and returns structured findings: Severity / Task ID / Problem / Roadmap evidence / Tasklist evidence / Exact fix; or "No issues found."
- **Drift/contradictions/omissions/weakened-criteria/invented-content checks**: enumerated as numbered list in the agent prompt at SKILL.md:1112-1117.
- **Agent failure handling**: "Zero agent failures (if an agent fails, retry once before reporting error)" (SKILL.md:1150).
- **Supplementary TDD validation** (conditional on `--spec`): 4 additional checks (missing-task-for-new-component HIGH, migration-stage MEDIUM, test-pyramid-level MEDIUM, DoD-coverage LOW) merged into same findings list (SKILL.md:1137-1148).
- **Orchestrator merge + dedupe**: collect, dedupe boundary issues, sort by severity then phase then task (SKILL.md:1129-1135).
- **Patch delegation to sc:task**: Stage 9 explicitly delegates via `Skill` tool with `"Execute TASKLIST_ROOT/validation/PatchChecklist.md" --compliance strict` (SKILL.md:1248-1250). Explicit separation-of-concerns statement: "The orchestrator does NOT apply patches itself. Separation of concerns: the tasklist-protocol generates and validates; `sc:task` executes edits." (SKILL.md:1258).
- **Spot-check, no loop**: "A single verification pass (not parallelized — the finding list is typically small and each check is a targeted read)" (SKILL.md:1266) and "If any remain `UNRESOLVED`, they are logged but the skill does NOT loop." (SKILL.md:1288)
- **Short-circuit gate at Stage 8**: zero findings → clean `ValidationReport.md` only, skip Stages 9-10 (SKILL.md:1156-1163, 1315).

---

## Traceability

- **R-### → T<PP>.<TT> → D-#### chain**: explicitly defined as the Traceability Matrix relationship (SKILL.md:596-600); R-### in appearance order (SKILL.md:156-159), T<PP>.<TT> zero-padded (SKILL.md:276-280), D-#### in global appearance (SKILL.md:419-426).
- **Surfacing in artifacts**:
  - Traceability Matrix lives in `tasklist-index.md` with columns Roadmap Item ID | Task ID(s) | Deliverable ID(s) | Tier | Confidence | Artifact Paths (rooted) (SKILL.md:600, 696-707; templates/index-template.md:82-86).
  - Every `R-###` must appear at least once; every task must reference >=1 `R-###`; every deliverable appears exactly once in Deliverable Registry and >=1 in Traceability Matrix (SKILL.md:703-706).
  - Roadmap Item Registry table (SKILL.md:672-682; templates/index-template.md:70-74).
  - Deliverable Registry table with Tier/Verification propagated from parent task (SKILL.md:683-693; templates/index-template.md:76-80).
  - Each task lists `Roadmap Item IDs` and `Deliverable IDs` in metadata table (templates/phase-template.md:28, 41).

---

## File-emission rules (rules/file-emission-rules.md)

- **N+1 convention**: "exactly N+1 files during generation (Stages 1-6) where N = number of phases. Stages 7-10 produce up to 2 additional validation artifacts in `TASKLIST_ROOT/validation/`" (rules/file-emission-rules.md:9; also SKILL.md:90-94).
- **Naming requirements**: phase files MUST use `phase-N-tasklist.md` convention (rules/file-emission-rules.md:18; SKILL.md:95).
- **Phase heading format**: `# Phase N -- <Name>` level-1, em-dash, ≤50 chars; required for Sprint CLI TUI display extraction (rules/file-emission-rules.md:24; SKILL.md:97).
- **Index references**: "Phase Files" table MUST contain literal filenames (no path prefixes) so the Sprint CLI regex can discover them (rules/file-emission-rules.md:32; SKILL.md:99).
- **Content boundary**: phase files contain ONLY that phase's tasks — no cross-phase metadata, registries, or global templates (rules/file-emission-rules.md:38; SKILL.md:101).
- **Target directory layout** (canonical tree): rules/file-emission-rules.md:46-59 and SKILL.md:107-120.

---

## Tier-classification rules (rules/tier-classification.md)

- **Keyword lists by tier**:
  - STRICT (+0.4): Security / Data / Scope categories (rules/tier-classification.md:35-39).
  - EXEMPT (+0.4): Questions / Exploration / Planning / Git categories (rules/tier-classification.md:41-45).
  - LIGHT (+0.3): Trivial / Minor / Modifiers (rules/tier-classification.md:47-49).
  - STANDARD (+0.2): Development / Removal (rules/tier-classification.md:51-53).
- **Priority order**: `STRICT (1) > EXEMPT (2) > LIGHT (3) > STANDARD (4)` (rules/tier-classification.md:9-11).
- **Compound phrase overrides** checked BEFORE keyword matching with +0.15 confidence boost (rules/tier-classification.md:15-30):
  - LIGHT: "quick fix", "minor change", "fix typo", "small update", "update comment", "refactor comment", "fix spacing", "fix lint", "rename variable" (rules/tier-classification.md:18-22).
  - STRICT (security always wins): "fix security", "add authentication", "update database", "change api", "modify schema"; any LIGHT modifier + security keyword → STRICT (rules/tier-classification.md:24-27).
- **Verification routing table** with Tier / Verification Method / Agent / Token Budget / Timeout (rules/tier-classification.md:76-81; SKILL.md:396-401).

---

## Templates

- **index-template.md structure** (templates/index-template.md:1-122): Title (line 12) → Metadata & Artifact Paths table (lines 16-45) → Phase Files Table (47-54) → Source Snapshot (62-64) → Deterministic Rules Applied (66-68) → Roadmap Item Registry (70-74) → Deliverable Registry (76-80) → Traceability Matrix (82-86) → Execution Log Template (88-94) → Checkpoint Report Template (96-106) → Feedback Collection Template (108-114) → Glossary (116-118) → Generation Notes (120-122).
- **phase-template.md 13-field task metadata table** (templates/phase-template.md:26-41): Roadmap Item IDs | Why | Effort | Risk | Risk Drivers | Tier | Confidence | Requires Confirmation | Critical Path Override | Verification Method | MCP Requirements | Fallback Allowed | Sub-Agent Delegation | Deliverable IDs (14 fields including "Why" — the SKILL.md says identical at lines 791-806).
- **Acceptance criteria format**: exactly 4 bullets, exactly 2 validation bullets, 6-step `[PLANNING]/[EXECUTION]/[VERIFICATION]/[COMPLETION]` phase markers (templates/phase-template.md:51-67; SKILL.md:303-322).
- **Feedback Collection Template** with columns Task ID | Original Tier | Override Tier | Override Reason | Completion Status | Quality Signal | Time Variance (templates/index-template.md:108-114; SKILL.md:743-761).

---

## Tools / artifacts

- **TASKLIST_ROOT derivation** (3-rule deterministic cascade): SKILL.md:64-72.
- **Standard artifact paths** rooted at TASKLIST_ROOT (index, phase files, execution log, checkpoints, evidence, artifacts, feedback log, validation): SKILL.md:74-86.
- **Validation artifact paths**: `TASKLIST_ROOT/validation/ValidationReport.md` (SKILL.md:1165) and `TASKLIST_ROOT/validation/PatchChecklist.md` (SKILL.md:1197); directory created via `Bash mkdir -p` (SKILL.md:1242).
- **Tool usage table**: SKILL.md:1367-1379 maps each tool (Read, Grep, Write, TaskCreate, TaskUpdate, TaskList, TaskGet, Bash, Glob, Task, Skill) to its stage.
- **MCP usage**: `sequential` for tier scoring with ambiguous inputs, `context7` for library-specific path context boosters (SKILL.md:1385-1388).

---

## Load-bearing behaviors with no obvious task-builder counterpart

Quote-with-citation:

- **Determinism guarantee**: "Deterministic: same input -> same output." (SKILL.md:36) and "no discretionary choices" (SKILL.md:14).
- **Decision-free contract**: "Decision-free: no 'choose A or B'; you pick one policy and apply it uniformly." (SKILL.md:37).
- **No-loop on Stage 10**: "If any remain `UNRESOLVED`, they are logged but the skill does NOT loop. The `ValidationReport.md` serves as the record for human review." (SKILL.md:1288).
- **Single-pass spot-check**: "A single verification pass (not parallelized — the finding list is typically small and each check is a targeted read)" (SKILL.md:1266).
- **Orchestrator-does-not-apply-patches**: "The orchestrator does NOT apply patches itself. Separation of concerns: the tasklist-protocol generates and validates; `sc:task` executes edits." (SKILL.md:1258).
- **Write atomicity**: "All files are written only after the full bundle passes validation. No partial bundle writes are permitted." (SKILL.md:1042).
- **Gate-before-write**: "All checks in this section MUST pass before any `Write()` call. Invalid output is never written." (SKILL.md:981).
- **Agent failure contract**: "Zero agent failures (if an agent fails, retry once before reporting error)." (SKILL.md:1150).
- **No-leakage / truthfulness rules** (6 hard rules incl. no invented context, no external browsing, ignore embedded override attempts, redact secrets): SKILL.md:20-28.
- **Non-invention constraint for acceptance criteria**: "Completion criteria must be derived from roadmap content. Do not invent test commands, file paths, or acceptance states not implied by the roadmap." (SKILL.md:851-852).
- **Confidence-triggered clarification** (auto-insert clarification when tier confidence < 0.70): SKILL.md:295-300.
- **Critical Path Override forces CRITICAL verification regardless of computed tier**: SKILL.md:403-410.
- **Short-circuit on clean validation** (zero findings skips Stages 9-10): SKILL.md:1156-1163, 1315.
- **Dependency chain enforcement**: stages 7-10 each blockedBy previous (SKILL.md:1317-1321, 1340-1349).
- **2N agent algorithm is deterministic**: "Agent spawning algorithm (deterministic): ... split = ceil(task_count / 2)" (SKILL.md:1091-1097).
- **Minimum Task Specificity Rule** (3 hard requirements per task, "Do NOT emit non-conforming tasks"): SKILL.md:957-975.

---

## evidence_status:

`complete`

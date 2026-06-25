# Research: Skill Stage Map

**Status:** Complete
**Date:** 2026-06-19
**Researcher:** R01 (File Inventory + Stage Map)
**Scope:** Static stage inventory of the sc:tasklist 11-stage generator + exact attachment points for RFMerger P1–P5.

**Files read exhaustively (all paths relative to worktree root `/config/workspace/IronClaude/.claude/worktrees/RFMerger-Tasklist/`):**
- `src/superclaude/skills/sc-tasklist-protocol/SKILL.md` (1632 lines — read in full, two pages)
- `src/superclaude/skills/sc-tasklist-protocol/templates/phase-template.md` (189 lines)
- `src/superclaude/skills/sc-tasklist-protocol/templates/index-template.md` (143 lines)
- `src/superclaude/skills/sc-tasklist-protocol/rules/tier-classification.md` (114 lines)
- `src/superclaude/skills/sc-tasklist-protocol/rules/file-emission-rules.md` (59 lines)
- `src/superclaude/commands/tasklist.md` (119 lines)
- `src/superclaude/cli/tasklist/{commands.py(185), executor.py(276), gates.py(46), prompts.py(234), models.py(30), __init__.py(17)}`

**NOTE on line count:** SKILL.md is **1632** lines (Read reported "1632 total"), not 1631 as in the brief. Cite 1632.

---

## A. The 11-Stage Generator — Definitive Stage Map

The skill is **prose-driven** (an LLM protocol, not executable code). The 11 stages are defined in TWO authoritative places that must agree:
1. **Stage Completion Reporting Contract** table — `SKILL.md:1529-1541` (`## Stage Completion Reporting Contract`, table header at :1529-1530).
2. Stage bodies: Stages 1-6 are implicit in the Deterministic Generation Algorithm (§4-§5) + Self-Check; Stages 7-10.5 have explicit `### Stage N:` headings under `## Post-Generation Roadmap Validation (Stages 7-10, Mandatory)` at `SKILL.md:1240`.

The 11 stages = 1,2,3,4,5,6,7,8,9,10,**10.5** (the count "11 stages" includes 10.5 as the eleventh; confirmed `SKILL.md:1527` "The skill executes in 11 stages").

### Stage 1 — Input Ingest
- **Heading / anchor:** No dedicated `### Stage 1` heading. Defined by the contract row `SKILL.md:1531` (`| 1 | Input Ingest | Roadmap text non-empty; ... file read succeeded |`) and §4.1 Parse Roadmap Items begins the work.
- **Line range:** Contract row :1531; algorithm entry §4.1 `SKILL.md:155-167` (`### 4.1 Parse Roadmap Items`).
- **What it does:** Reads roadmap text (the only required input per Input Contract §47-57); validates non-empty.
- **Inputs:** roadmap text. **Outputs:** in-memory roadmap string + `R-###` parse readiness.
- **Proposal attaches?** No.

### Stage 2 — Parse + Phase Bucketing
- **Heading / anchor:** Contract row `SKILL.md:1532`. Bodies: §4.1 (`SKILL.md:155`), §4.2 Determine Phase Buckets (`### 4.2 Determine Phase Buckets`, `SKILL.md:216`), §4.3 Fix Phase Numbering (`SKILL.md:228`).
- **Line range:** §4.1–§4.3 ≈ `SKILL.md:155-233`.
- **What it does:** Splits roadmap into `R-###` items (appearance order); assigns each to exactly one phase bucket; renumbers phases contiguously (missing-Phase-8 rule).
- **Inputs:** roadmap text. **Outputs:** `R-###` registry, phase buckets.
- **Proposal attaches?** No.

### Stage 3 — Task Conversion
- **Heading / anchor:** Contract row `SKILL.md:1533`. Bodies: §4.4 Convert Roadmap Items into Tasks (`SKILL.md:235`), §4.5 Task ID/Ordering/Naming (`SKILL.md:294`), §4.6 Clarification Tasks (`SKILL.md:304`).
- **Line range:** §4.4–§4.6 ≈ `SKILL.md:235-322`. (Supplementary task-gen §4.4a `SKILL.md:246`, §4.4b `SKILL.md:269` also conversion-adjacent but `--spec`/`--prd` gated.)
- **What it does:** Converts each `R-###` into one (or split) task stubs with `T<PP>.<TT>` IDs; inserts Clarification Tasks for missing info.
- **Inputs:** `R-###` items + phase buckets + (optional) `supplementary_context`/`prd_context`. **Outputs:** task stubs with IDs + titles.
- **Proposal attaches?** No (but P1 context block is rendered into these tasks at Stage 4/5).

### Stage 4 — Enrichment  ★ P1 + P5 ATTACH HERE
- **Heading / anchor:** Contract row `SKILL.md:1534` (`| 4 | Enrichment | All tasks have non-empty: Effort ... Risk ... Tier ... Confidence score |`). Bodies: the entire `## Deterministic Enrichment (Value Preservation Without Nondeterminism)` block `SKILL.md:444` through §5.7 Traceability Matrix `SKILL.md:652-658`. Tier/Effort/Risk/Confidence/MCP/Delegation = §5.2–§5.6 (`SKILL.md:493-650`). Also §4.7-§4.11 (Acceptance/Validation, Checkpoints, Verification Routing, Critical Path Override) `SKILL.md:324-441`.
- **Line range:** §4.7–§5.7 ≈ `SKILL.md:324-658`.
- **What it does:** Computes per-task Effort, Risk, Tier, Confidence, Verification Method, MCP requirements, delegation; builds Deliverable Registry + Traceability Matrix.
- **Inputs:** task stubs. **Outputs:** fully enriched task records (still in-memory; written at Stage 5).
- **Proposal attaches? YES — P1 (Context-Armed Steps) and P5 (Tier Calibration Advisory).**

  **P1 — Context-Armed Steps → optional task-level `## Execution Context` block, emitted at Stage 4 (Enrichment), rendered into the phase-file task body at Stage 5.**
  - **Primary skill attachment file/range:** The per-task body sections in the Phase File Template, `SKILL.md:894-927`. The block should be inserted as a new optional section in the task body — the cleanest anchor is **immediately after the metadata table and Artifacts block, before `**Deliverables:**`** OR after `**Notes:**`. The Steps block is `SKILL.md:904-911`.
  - **Verbatim anchor (where the new optional block sits relative to existing body):**
    - `SKILL.md:894`: `**Artifacts (Intended Paths):**`
    - `SKILL.md:900`: `**Deliverables:**`
    - `SKILL.md:904`: `**Steps:**`
    - `SKILL.md:927`: `**Notes:** <optional; max 2 lines; include tier conflict resolution if applicable>`
  - **Mirror file (must stay in sync):** `templates/phase-template.md:55-82` — `**Deliverables:**` at :55, `**Steps:**` at :59, `**Notes:**` at :82. Implementer edits BOTH the SKILL.md inline copy and this human-review mirror.
  - **Implementer note:** "Context-Armed Steps" means each task's `**Steps:**` (or a new `## Execution Context` sub-block) carries the task's resolved context (named files, prior-task deliverables, spec section refs) so the F1 executor needs no re-derivation. Attaches to the Stage-4 enrichment loop because that is where named-artifact/MCP/dependency facts are already computed (Minimum Task Specificity Rule `SKILL.md:1110-1128`, esp. rule 3 "No cross-task prose dependency... Shared context belongs in a roadmap-referenced file" at :1122-1124 — P1 is the structured home for that shared context).

  **P5 — Tier Calibration Advisory → new `## Tier Calibration Advisory` section, emitted at Stage 4, reads `TASKLIST_ROOT/feedback-log.md`; MUST NOT mutate scored tiers.**
  - **Primary skill attachment file/range:** Tier scoring lives in §5.3 Compliance Tier Classification (`### 5.3 Compliance Tier Classification (mandatory, deterministic)`, `SKILL.md:544`) through §5.3.3 Context Boosters (`SKILL.md:596-614`), and §5.4 Confidence Scoring (`SKILL.md:616-629`). The advisory is a READ-ONLY post-pass that compares computed tiers against historical overrides in the feedback log.
  - **Where the advisory SECTION emits:** This is an index-level section (cross-phase, advisory). Cleanest home is the index file. Anchor candidates in the **Index File Template**: after `#### Feedback Collection Template` (`SKILL.md:820-839`, the feedback-log schema the advisory reads) and before `#### Glossary` (`SKILL.md:841`). Alternatively after `#### Generation Notes (Optional)` (`SKILL.md:847-849`).
  - **Verbatim anchors:**
    - `SKILL.md:822`: `Track tier classification accuracy and execution quality for calibration learning.` (Feedback Collection Template purpose line — the advisory consumes exactly this log.)
    - `SKILL.md:826`: `**Intended Path:** `TASKLIST_ROOT/feedback-log.md`` (the file P5 reads.)
    - `SKILL.md:847-849`: `#### Generation Notes (Optional)` ... `This section is informational; it does not affect Sprint CLI compatibility.` (advisory parity — also informational/non-mutating.)
  - **Feedback-log path is canonical:** declared at `SKILL.md:86` (`- Feedback log: `TASKLIST_ROOT/feedback-log.md``) and in Artifact Paths table `SKILL.md:707`.
  - **"MUST NOT mutate scored tiers" anchor:** The determinism contract is §5.3 priority order `SKILL.md:548` (`**Priority order:** `STRICT (1) > EXEMPT (2) > LIGHT (3) > STANDARD (4)``) and the Objective "Deterministic: same input -> same output" `SKILL.md:35`. P5 must be advisory text only — it surfaces "task T03.04 scored STANDARD but the feedback-log shows 2 prior STANDARD→STRICT overrides on similar items" WITHOUT changing the Tier field. Mirror: `rules/tier-classification.md:9-11` (priority order).
  - **Stage-4 gate touchpoint:** Contract row `SKILL.md:1534` defines Stage 4 done-criteria as field presence only; P5 must not add a blocking criterion (advisory).

### Stage 5 — File Emission
- **Heading / anchor:** Contract row `SKILL.md:1535` (`| 5 | File Emission | tasklist-index.md written; all phase files referenced in index exist on disk; no extra phase files written |`). Bodies: File Emission Rules §3.3 `SKILL.md:91-126`, Output Templates `SKILL.md:662-1097` (Index template `SKILL.md:666-849`, Phase File template `SKILL.md:853-1097`).
- **Line range:** Template definitions `SKILL.md:662-1097`; emission rules `SKILL.md:91-126`.
- **What it does:** Renders the enriched in-memory bundle to `tasklist-index.md` + `phase-N-tasklist.md` files (N+1 files). This is where P1's `## Execution Context` block actually lands in the phase-file task body and P5's advisory lands in the index.
- **Inputs:** enriched task records, registries. **Outputs:** N+1 markdown files on disk.
- **Proposal attaches?** Rendering site for P1/P5 (computed at Stage 4, written here). Note Tool Usage table `SKILL.md:1612` marks Write at Stage 5/8/10.

### Stage 6 — Self-Check (the 20-check pre-write gate)  ★ P4 ATTACHES HERE (emit gate-results.txt)
- **Heading / anchor:** Contract row `SKILL.md:1536` (`| 6 | Self-Check | All Sprint Compatibility Self-Check assertions pass; no blocking failures |`). Bodies: `## Sprint Compatibility Self-Check (Pre-Write, Mandatory)` `SKILL.md:1132`, `### Semantic Quality Gate (Pre-Write, Mandatory)` `SKILL.md:1147`, `### Structural Quality Gate (Pre-Write, Mandatory)` `SKILL.md:1174` (checks 13-20 in a table `SKILL.md:1176-1185`).
- **Line range:** `SKILL.md:1132-1187`.
- **What it does:** Runs checks 1-20 against the in-memory bundle BEFORE any `Write()`. Checks 1-8 = Sprint compat (`SKILL.md:1138-1145`), 9-12 = Semantic Quality Gate (`SKILL.md:1151-1156`), 13-20 = Structural Quality Gate table (`SKILL.md:1178-1185`). Write atomicity: full bundle validated before any write (`SKILL.md:1195`).
- **Inputs:** in-memory bundle. **Outputs:** pass/fail per check; gate decision.
- **Proposal attaches? YES — P4 (Evidence-Anchored Validation), part 1.**

  **P4 part 1 — emit `TASKLIST_ROOT/validation/gate-results.txt` at END of Stage 6.**
  - **Primary skill attachment file/range:** the close of the Structural Quality Gate, **`SKILL.md:1187`**: ``If any check 1-20 fails, fix it before writing any output file.`` — the new "after all 20 checks pass, serialize each check's PASS/FAIL + evidence to `TASKLIST_ROOT/validation/gate-results.txt`" instruction attaches immediately after this line (and before `## Final Output Constraint` at `SKILL.md:1191`).
  - **Verbatim anchor (the line to edit near):**
    - `SKILL.md:1187`: `If any check 1-20 fails, fix it before writing any output file.`
  - **`validation/` dir is canonical:** declared `SKILL.md:87` (Validation reports path) and Artifact Paths table `SKILL.md:706`. Stage 8 already does `mkdir -p` on `validation/` via Bash (`SKILL.md:1407`), but P4 emits at Stage 6 — so P4 must ensure `mkdir -p TASKLIST_ROOT/validation/` happens at/before Stage 6 (Tool Usage Bash currently only listed for Stages 5/8 `SKILL.md:1617`).
  - **CRITICAL — the 17-vs-20 inconsistency P4 must not inherit (see §C below):** Stage 6 is internally "1-20" (`SKILL.md:1187`) but the Stage-6 completion message says "all 17 checks passed" (`SKILL.md:1597`). gate-results.txt must serialize all **20** checks; the implementer should fix the stale "17" while wiring P4.

  **P4 part 2 — inject gate-results.txt into Stage 7 prompts (covered under Stage 7 below).**

### Stage 7 — Roadmap Validation (2N Parallel Agents)  ★ P4 (inject) + P3 (DNSP) ATTACH HERE
- **Heading / anchor:** `### Stage 7: Roadmap Validation (2N Parallel Agents)` `SKILL.md:1244`. Contract row `SKILL.md:1537`.
- **Line range:** `SKILL.md:1244-1310`.
- **What it does:** For each of N phase files, computes `split = ceil(task_count/2)` (`SKILL.md:1256`) and spawns Agent A (tasks 1..split) + Agent B (split+1..end) → **2N agents** via the `Task` tool (`SKILL.md:1263`). Each agent checks Drift/Contradictions/Omissions/Weakened/Invented (validation instructions block `SKILL.md:1265-1286`) and returns structured findings (Severity/Task ID/Problem/Roadmap evidence/Tasklist evidence/Exact fix, `SKILL.md:1279-1284`). Orchestrator merges + dedupes (`SKILL.md:1288-1295`). Retry-once on agent failure (`SKILL.md:1310`).
- **Inputs:** full roadmap text + per-phase task subset + validation instructions. **Outputs:** consolidated, deduped, severity-sorted findings list for Stage 8.
- **Proposal attaches? YES — P4 (part 2, inject) and P3 (DNSP).**

  **P4 part 2 — inject gate-results.txt into Stage 7 prompts.**
  - **Primary attachment:** the per-agent spawn payload at `SKILL.md:1253-1262` (Agent A spawn `SKILL.md:1254-1258`, Agent B spawn `SKILL.md:1259-1262`) and/or the validation-instructions block `SKILL.md:1265-1286`. P4 adds the gate-results.txt content (or its path + relevant excerpt) as an additional context input each validation agent receives, so the agent can cross-reference "the generator's own self-check claimed PASS on check N — verify it against the actual file."
  - **Verbatim anchors:**
    - `SKILL.md:1254`: `3. Spawn **Agent A** with:`
    - `SKILL.md:1255`: `   - The full roadmap text`
    - `SKILL.md:1256` (in 1255-1257 block): `   - The phase file content for tasks 1 through `split` (first 50%+1 on odd count)`
    - `SKILL.md:1267`: `> For each task in your assigned range, check:` (the instructions list P4 augments with an "evidence-anchored" check #6 vs gate-results.txt)
  - **"Evidence-Anchored" semantics:** the validation agent's findings already require `Roadmap evidence` + `Tasklist evidence` (`SKILL.md:1282-1283`); P4 extends this to also anchor against the serialized gate-results so a finding can cite the exact failing/passing self-check.

  **P3 — DNSP (Do-Not-Silently-Pass): on Stage-7 validation-agent retry failure, synthesize a HIGH `source:"synthetic-dnsp"` finding (orchestrator merge step).**
  - **Primary attachment:** the **orchestrator merge step** `SKILL.md:1288-1295` (`**Orchestrator merge and deduplication**:` at :1288) AND the **stage gate retry clause** `SKILL.md:1310`.
  - **Verbatim anchors (the exact lines P3 edits near):**
    - `SKILL.md:1310`: `**Stage gate**: All 2N agents completed successfully. Findings merged and deduplicated. Zero agent failures (if an agent fails, retry once before reporting error).`
    - `SKILL.md:1288`: `**Orchestrator merge and deduplication**:`
    - `SKILL.md:1290-1294` (numbered merge steps 1-4): step 1 `Collects all findings into a single list` (:1292), step 4 `Produces the consolidated findings list for Stage 8` (:1295).
  - **What P3 changes:** Today, if an agent fails after the one retry, the stage "report[s] error" (`SKILL.md:1310`) — a silent-pass risk if the orchestrator proceeds without that agent's findings. P3 makes the orchestrator instead SYNTHESIZE a HIGH-severity finding tagged `source:"synthetic-dnsp"` for the un-validated task range, so Stage 8 patch-plan + Stage 10 spot-check force human attention rather than shipping unvalidated content. Insert P3 as a new orchestrator merge step (between current steps 1 and 4) and amend the stage-gate retry clause.
  - **Cross-ref:** R03 owns the task-builder DNSP/PR-02 contract this reuses — do NOT re-derive the synthetic-finding schema here; this report only pins the ATTACHMENT POINT (orchestrator merge + retry clause).

### Stage 8 — Patch Plan Generation
- **Heading / anchor:** `### Stage 8: Patch Plan Generation` `SKILL.md:1312`. Contract row `SKILL.md:1538`.
- **Line range:** `SKILL.md:1312-1407`.
- **What it does:** Transforms consolidated findings into 2 artifacts in `TASKLIST_ROOT/validation/`: `ValidationReport.md` (`SKILL.md:1327`) and `PatchChecklist.md` (`SKILL.md:1360`). **Short-circuit:** zero findings → write CLEAN `ValidationReport.md` and skip Stages 9-10 (`SKILL.md:1316-1325`). Stage gate does `mkdir -p` on `validation/` (`SKILL.md:1407`).
- **Inputs:** consolidated findings. **Outputs:** ValidationReport.md + PatchChecklist.md.
- **Proposal attaches?** Indirect — P3's synthetic-dnsp HIGH findings flow into ValidationReport.md/PatchChecklist.md here; P4's gate-results.txt already written. No new primary attachment, but P3 must guarantee the short-circuit (`SKILL.md:1316`) is NOT taken when a synthetic-dnsp finding exists (a synthetic HIGH is a finding → short-circuit must not fire).

### Stage 9 — Patch Execution (Delegate to `sc:task`)  ★ P2 LOOPS BACK HERE
- **Heading / anchor:** `### Stage 9: Patch Execution (Delegate to `sc:task`)` `SKILL.md:1409`. Contract row `SKILL.md:1539`.
- **Line range:** `SKILL.md:1409-1427`.
- **What it does:** Invokes `sc:task` via the `Skill` tool (`SKILL.md:1413`) with input `"Execute TASKLIST_ROOT/validation/PatchChecklist.md"` (`SKILL.md:1415`) + `--compliance strict` (`SKILL.md:1416`). The orchestrator does NOT apply patches itself (`SKILL.md:1425`). Stage gate: `sc:task` reports completion, all items addressed (`SKILL.md:1427`).
- **Inputs:** PatchChecklist.md. **Outputs:** mutated phase files.
- **Proposal attaches? YES — P2 (Bounded Patch Loop) loops BACK to this stage from Stage 10.**

  **P2 — Bounded Patch Loop: after Stage 10, loop back to Stage 9 (delegate sc:task), bounded.**
  - **Loop-back TARGET anchor (Stage 9):** `SKILL.md:1413` (`**Mechanism**: Invoke `sc:task` via the `Skill` tool with:`) and the Stage-9 gate `SKILL.md:1427` (`**Stage gate**: `sc:task` reports completion. All checklist items addressed.`).
  - **Loop ORIGIN anchor (Stage 10) — see Stage 10 below.** P2's loop counter/bound + the "if UNRESOLVED findings remain AND iterations < BOUND, re-run Stage 9 against a residual patch-checklist" logic attaches at the Stage 10 stage-gate (`SKILL.md:1456`).
  - **Current behavior P2 replaces:** Stage 10 explicitly states `the skill does NOT loop` (`SKILL.md:1456`) — P2 directly amends this no-loop clause into a BOUNDED loop. This is the single most load-bearing edit for P2.

### Stage 10 — Spot-Check Verification  ★ P2 LOOP ORIGIN HERE
- **Heading / anchor:** `### Stage 10: Spot-Check Verification` `SKILL.md:1429`. Contract row `SKILL.md:1540`.
- **Line range:** `SKILL.md:1429-1456`.
- **What it does:** Single (non-parallelized) verification pass (`SKILL.md:1433`). For each finding in ValidationReport.md: read the flagged section, verify the exact fix was applied, verify no regression, record `RESOLVED`/`UNRESOLVED` (`SKILL.md:1435-1440`). Appends `## Verification Results` to ValidationReport.md (`SKILL.md:1442-1454`).
- **Inputs:** ValidationReport.md findings + (patched) phase files. **Outputs:** Verification Results table; RESOLVED/UNRESOLVED per finding.
- **Proposal attaches? YES — P2 (Bounded Patch Loop) loop ORIGIN / decision point.**

  **P2 — loop decision point.**
  - **Primary attachment / verbatim anchor (the exact line P2 edits):**
    - `SKILL.md:1456`: `**Stage gate**: All findings verified. If any remain `UNRESOLVED`, they are logged but the skill does NOT loop. The `ValidationReport.md` serves as the record for human review.`
  - **What P2 changes here:** Replace "the skill does NOT loop" with a bounded loop: if any finding is `UNRESOLVED` (`SKILL.md:1440`, :1453) AND `loop_iteration < MAX_PATCH_ITERATIONS`, increment the counter and re-enter Stage 9 (`SKILL.md:1413`) with a residual PatchChecklist scoped to the UNRESOLVED findings, then re-run Stage 10. On exhausting the bound, fall back to current behavior (log + ValidationReport.md as the human-review record).
  - **Bound source:** R03/R04 own where the numeric bound is specified; this report pins only that the loop's two edit sites are `SKILL.md:1456` (origin/decision) → `SKILL.md:1413`/`:1427` (target). The Dependency-chain block (`SKILL.md:1551-1557`) and Gate Behavior (`SKILL.md:1543-1557`) also describe Stage 9←10 ordering and may need a back-edge note.

### Stage 10.5 — Pre-Reflect Sign-off (the 11th stage)
- **Heading / anchor:** `### Stage 10.5: Pre-Reflect Sign-off` `SKILL.md:1460`. Contract row `SKILL.md:1541`.
- **Line range:** `SKILL.md:1460-1481` (+ deterministic depth `### Per-Phase Reflect Depth (Deterministic COMPLEXITY_SCORE)` `SKILL.md:1485-1521`).
- **What it does:** After Stage 10, fans out **N** (not 2N) `/sc:reflect --mode pre --remediate` agents — one per phase file — via the same `Task` primitive (`SKILL.md:1464`). Computes per-phase COMPLEXITY_SCORE → `--depth`/`--tier` (`SKILL.md:1466`, table `SKILL.md:1512-1516`, hard overrides `SKILL.md:1518-1521`). Non-blocking verdicts (PASS/PARTIAL/FAIL) recorded in the index "Pre-Reflect Sign-off" column (`SKILL.md:1477`); bundle ships regardless (`SKILL.md:1481`). Skipped under `--no-reflect`/`--dry-run` (`SKILL.md:1479`).
- **Inputs:** final validated phase files + resolved spec path. **Outputs:** per-phase reflect_pre verdict + `reflect_pre_summary` in index + `validation/reflect-pre/phase-<P>/` reports + `depth-map.yaml`.
- **Proposal attaches?** No primary P1-P5 attachment, but it is the existing pre-reflect anti-bias precedent the proposals should harmonize with (e.g., P5's tier advisory vs reflect's coverage audit). Note this stage is fenced AFTER the Stage 8-10 patch chain to avoid racing a mid-patch file (`SKILL.md:1462`); P2's bounded loop (Stage 9↔10) must complete before 10.5 runs.

---

## B. Slash Wrapper — `commands/tasklist.md` Flag Parse / Validate

The slash command is a **thin wrapper**: it parses + validates args, derives `TASKLIST_ROOT`, then invokes the `sc:tasklist-protocol` skill. It "does not execute any generation logic" (`commands/tasklist.md:30`, also Boundaries "Will Not: Execute the generation algorithm" `:116`).

| Concern | Location (`commands/tasklist.md`) | Verbatim anchor |
|---|---|---|
| Usage / argument-hint | `:22-24` | `/sc:tasklist <roadmap-path> [--spec <spec-path>] [--output <output-dir>] [--no-reflect]` (`:23`) |
| Arguments table (all 4 args incl. `--spec`, `--output`, `--no-reflect`) | `:34-39` | `--spec`: `:37`; `--output`: `:38`; `--no-reflect`: `:39` (`Escape hatch: skip both reflect gates (pre-reflect sign-off + templated post-reflect task). Set automatically by --dry-run.`) |
| `--output` default | `:38` | `Auto-derived from roadmap TASKLIST_ROOT` |
| TASKLIST_ROOT auto-derivation (3-step) | `:41-47` | step 1 `.dev/releases/current/<segment>/` (`:45`); step 2 version-token (`:46`); step 3 fallback `v0.0-unknown/` (`:47`) |
| Input Validation block (4 checks) | `:49-69` | check 1 roadmap exists/non-empty `:62-63` (`error_code: EMPTY_INPUT` / `MISSING_FILE`); check 2 `--spec` exists `:64-65`; check 3 `--output` parent exists `:66-67`; check 4 derivation succeeds `:68-69` (`DERIVATION_FAILED`) |
| Error format (2 fields) | `:53-58` | `error_code: <category string>` / `message: <...>` |
| Skill invocation (MANDATORY) | `:71-85` | `:76` `> Skill sc:tasklist-protocol`; passes Roadmap text / Spec text / Output dir (`:80-82`) |

**Proposal-relevant flag notes:**
- `--no-reflect` (`:39`) is the existing escape hatch for reflect gating — P1-P5 enhancements should respect it where they intersect reflect (P5 advisory is independent of reflect; P3/P2/P4 are validation-chain, not reflect-gated).
- There is **NO** `--spec §22` flag handling here for the proposals — R07 owns `--spec §22` citation cross-validation. The wrapper passes `--spec` content opaquely to the skill (`:81`); the skill's §4.1a (`SKILL.md:169-184`) does TDD-format detection.
- Wrapper does NOT add any P1-P5 flags today; if a proposal needs a new flag (e.g., a P2 `--max-patch-iterations` or P5 `--no-tier-advisory`), the Arguments table `:34-39` + Usage `:23` + Input Validation `:49-69` are the three edit sites.

---

## C. The 17-vs-20 Quality-Gate Inconsistency (VERIFIED, both verbatim)

CONFIRMED — there is a real stale-count inconsistency inside SKILL.md:

- **Says "1-20":** `SKILL.md:1187` (verbatim): `If any check 1-20 fails, fix it before writing any output file.`
  - Corroborated by the gate structure: checks 1-8 (Sprint compat `:1138-1145`), 9-12 (Semantic `:1151-1156`), 13-20 (Structural table `:1178-1185`) = **20 checks total**. So "1-20" is CORRECT.
- **Says "17":** `SKILL.md:1597` (verbatim, Stage-6 completion message): `- Stage 6: "Self-Check: all 17 checks passed"`
  - This "17" is STALE/WRONG — it predates the gate growing to 20 checks. The Stage-6 TaskUpdate completion string under-reports.

**Impact on P4:** P4 serializes gate-results.txt for "all 20" checks. The implementer should ALSO correct `SKILL.md:1597` "17" → "20" so the completion message agrees with the actual check count and with gate-results.txt. This is a one-token surgical fix; flag it as a P4-adjacent cleanup so the new evidence artifact is internally consistent. (No other "17"/"20" count drift found in the Self-Check region.)

---

## D. CLI Module Roles (`src/superclaude/cli/tasklist/`)

CRITICAL framing: the CLI `superclaude tasklist` surface is **validate-ONLY** (no `generate` subcommand). It runs roadmap→tasklist *fidelity* validation via a Claude subprocess. The **skill protocol** (Section A) is what GENERATES tasklists and is where P1-P5 attach. The two share `prompts.py` but use different builders. Scope note confirms: `SKILL.md:130-132` (`### 3.x Source Document Enrichment`, scope note) — `build_tasklist_fidelity_prompt` = CLI validate; `build_tasklist_generate_prompt` = skill protocol generation.

| Module | Role | Key exports + line numbers |
|---|---|---|
| `__init__.py` | Lazy module loader — exposes `tasklist_group` via `__getattr__` | `tasklist_group` lazy import `:9-13`; `__all__` `:17` |
| `commands.py` | Click command group `superclaude tasklist` + the single `validate` subcommand. Flag parse, default resolution, `.roadmap-state.json` auto-wire of `--tdd-file`/`--prd-file`, exit-code 1 on HIGH severity. | `tasklist_group` (group) `:15-16`; `validate()` command `:31-185`; flags `--roadmap-file` `:33-38`, `--tasklist-dir` `:39-44`, `--model` `:45-49`, `--max-turns` (default 100) `:50-55`, `--debug` `:56-60`, `--tdd-file` `:61-66`, `--prd-file` `:67-72`; auto-wire from `read_state(...)` `:114-159`; builds `TasklistValidateConfig` `:161-171`; calls `execute_tasklist_validate` `:173`; report at `tasklist-fidelity.md` `:175`; `sys.exit(1)` on fail `:181-183` |
| `prompts.py` | PURE prompt builders (no I/O, NFR-004 `:3-8`). TWO builders — the fork point for CLI-validate vs skill-generate. | **`build_tasklist_fidelity_prompt(roadmap_file, tasklist_dir, tdd_file=None, prd_file=None)`** `:17-148` — roadmap→tasklist fidelity ONLY (layering guard `:29-31`, `:42-47`); severity defs HIGH/MED/LOW `:48-68`; YAML frontmatter contract `:82-93`; TDD block `:112-128`; PRD block `:131-146`. **`build_tasklist_generate_prompt(roadmap_file, tdd_file=None, prd_file=None)`** `:151-234` — used by the SKILL protocol for inference generation, NOT called by the CLI executor (explicit note `:158-162`); baseline generation prompt `:171-184`; TDD enrichment `:186-202`; PRD enrichment `:204-221`; TDD+PRD interaction `:223-232`. Both append `_OUTPUT_FORMAT_BLOCK` (imported from `roadmap.prompts` `:14`). |
| `executor.py` | Orchestrates the fidelity validation pipeline. Reuses `execute_pipeline()` + `ClaudeProcess` from `pipeline/` (no new subprocess abstraction `:6-8`). | `_collect_tasklist_files` `:40-52`; `_embed_inputs` (fenced code blocks, inline context isolation) `:55-63`; `_sanitize_output` (strip preamble before YAML) `:66-89`; `tasklist_run_step` (single Claude subprocess; timeout=124→TIMEOUT, exit≠0→FAIL) `:92-188`; `_build_steps` (builds the one `tasklist-fidelity` Step with `TASKLIST_FIDELITY_GATE`, timeout 600, retry_limit 1) `:191-218`; `_has_high_severity` (parses `high_severity_count` from frontmatter) `:221-248`; **`execute_tasklist_validate(config) -> bool`** (entry; True=pass) `:251-276` |
| `gates.py` | Pure-data gate criteria (no logic, NFR-005 `:1-13`). Reuses semantic check fns from `roadmap/gates.py`. | **`TASKLIST_FIDELITY_GATE`** (GateCriteria) `:23-46`; required frontmatter fields `:24-31`; `min_lines=20` `:32`; `enforcement_tier="STRICT"` `:33`; semantic checks `_high_severity_count_zero` + `_tasklist_ready_consistent` `:34-45` (imported from `roadmap.gates` `:18-21`) |
| `models.py` | `@dataclass TasklistValidateConfig(PipelineConfig)` — adds `output_dir`, `roadmap_file`, `tasklist_dir`, `tdd_file`, `prd_file` | **`TasklistValidateConfig`** `:14-30`; fields `:22-30` |

**Proposal relevance of CLI modules:** P1-P5 attach to the **skill protocol** (Section A), NOT these CLI modules. The CLI validate path is a separate, narrower surface. The only CLI touchpoint a proposal might want: `build_tasklist_generate_prompt` (`prompts.py:151-234`) is the prompt the skill reads for generation — if P1 (Execution Context) or P5 (Tier Advisory) needed a code-level prompt hook (rather than pure-prose SKILL.md instructions), `:171-184` (baseline generate prompt) is the insertion point. But given the skill is prose-driven, the primary attachments remain in SKILL.md per Section A.

---

## E. Summary — Attachment-Point Index (one row per builder checklist item)

| Proposal | Stage | Primary file:line anchor (verbatim line) | Secondary / mirror |
|---|---|---|---|
| **P1** Context-Armed Steps (`## Execution Context` block) | 4 (computed) → 5 (rendered) | `SKILL.md:894-927` task body — insert near `**Steps:**` (`SKILL.md:904`) / after `**Notes:**` (`SKILL.md:927`) | `templates/phase-template.md:55-82` (Deliverables :55 / Steps :59 / Notes :82) — keep in sync |
| **P5** Tier Calibration Advisory (`## Tier Calibration Advisory`) | 4 | Index template — after `#### Feedback Collection Template` (`SKILL.md:820-839`), anchor lines `SKILL.md:822`, `:826`; advisory reads `TASKLIST_ROOT/feedback-log.md` (`SKILL.md:86`,`:707`). MUST NOT mutate tiers (§5.3 priority `SKILL.md:548`, determinism `SKILL.md:35`) | `index-template.md:123-131` (feedback template mirror); `rules/tier-classification.md:9-11` |
| **P4** Evidence-Anchored Validation — emit gate-results.txt | 6 (end) | `SKILL.md:1187` (`If any check 1-20 fails, fix it before writing any output file.`) — emit `TASKLIST_ROOT/validation/gate-results.txt` after; fix stale "17" at `SKILL.md:1597` | `validation/` path `SKILL.md:87`,`:706`; mkdir Tool Usage `SKILL.md:1617` |
| **P4** Evidence-Anchored Validation — inject into prompts | 7 | Agent spawn payload `SKILL.md:1254-1262`; instructions `SKILL.md:1265-1286` (anchor `:1267`) | findings evidence fields `SKILL.md:1282-1283` |
| **P3** DNSP synthetic-dnsp HIGH finding | 7 | Stage gate retry clause `SKILL.md:1310` (verbatim) + orchestrator merge `SKILL.md:1288-1295`; ensure Stage-8 short-circuit `SKILL.md:1316` not taken | R03 owns DNSP/PR-02 contract (do not re-derive schema) |
| **P2** Bounded Patch Loop | 10 (origin) → 9 (target) | `SKILL.md:1456` (`...the skill does NOT loop...`) → loop back to `SKILL.md:1413`/`:1427`; amend Dependency-chain `SKILL.md:1551-1557` back-edge | bound value owned by R03/R04 |

---

## F. Cross-Researcher Boundaries Observed
- R03 (reused contracts): I pinned WHERE P3 DNSP / P2 sc:task delegation attach but did NOT specify the synthetic-finding schema or the patch-loop bound value.
- R04 (data-flow trace): I gave static stage I/O; the live data flow (e.g., how findings actually propagate Stage7→8→9→10) is R04's.
- R05 (tests): no test files inspected.
- R07 (citation cross-validation + `--spec §22`): I noted `--spec` is passed opaquely by the wrapper; §22 PRD Customer-Journey handling lives in `prompts.py:140-141`/`:212` but R07 owns the §22 citation work.

**Status:** Complete

# Pipeline Stage Diagrams: SC Tasklist + Adversarial vs RF Pipeline

**Generated**: 2026-04-02
**Scope**: End-to-end stage reconstruction for both frameworks, covering control flow, gating, agent delegation, validation, artifact schemas, error handling, determinism, and cost drivers.

---

## 1. SC Tasklist Protocol — 10-Stage Pipeline

### Stage Overview

```
INPUT                           GENERATION (Stages 1-6)                    VALIDATION (Stages 7-10)           OUTPUT
──────                          ───────────────────────                    ────────────────────────           ──────
Roadmap text ──► [1] Parse ──► [2] Phase ──► [3] Convert ──► [4] Enrich ──► [5] Assemble ──► [6] Emit ──► [7] Validate ──► [8] Patch ──► [9] Spot-check ──► [10] Emit ──► N+3 files
(+ optional        Items       Buckets      Items→Tasks     (deterministic) Registries    Files           vs Roadmap       Drift        Corrections      Validation
 spec)                                                       Effort/Risk/                                                                                 Artifacts
                                                             Tier/Conf
```

### Stage Details

#### Stage 1: Parse Roadmap Items
- **Input**: Raw roadmap text (sole source of truth)
- **Process**: Split at headings/bullets/numbers/semicolons. Each independently actionable clause = 1 item
- **Output**: Ordered list of roadmap items with IDs: `R-001`, `R-002`, ...
- **Determinism**: Full — appearance-order numbering, no discretion
- **Gating**: None (parsing cannot fail; everything becomes a roadmap item)

#### Stage 2: Determine Phase Buckets
- **Input**: Parsed roadmap items
- **Process**: 3-tier priority:
  1. Explicit phases/versions/milestones in roadmap → phase buckets
  2. Top-level `##` headings → phase buckets
  3. Default: Phase 1 (Foundations), Phase 2 (Build), Phase 3 (Stabilize)
- **Output**: Sequential phase numbers with no gaps ("Missing Phase 8" rule)
- **Determinism**: Full — priority order eliminates discretion
- **Gating**: None

#### Stage 3: Convert Roadmap Items → Tasks
- **Input**: Phase buckets + roadmap items
- **Process**: 1 task per item (default). Split into 2+ tasks only when item has 2+ independently deliverable outputs (component+migration, feature+tests, API+UI, pipeline+app)
- **Output**: Tasks with IDs `T<PP>.<TT>` (zero-padded). Clarification Tasks inserted when info missing or confidence < 0.70
- **Determinism**: Full — split criteria are exhaustive, ordering preserves roadmap appearance, tie-breaking rules explicit
- **Gating**: None (Clarification Tasks handle missing info rather than blocking)

#### Stage 4: Enrich Tasks (Deterministic Scoring)
- **Input**: Raw tasks
- **Process** (all deterministic, keyword-based):
  - **Effort**: `EFFORT_SCORE` (0-4+) → `XS|S|M|L|XL` via keyword matching
  - **Risk**: `RISK_SCORE` (0-4+) → `Low|Medium|High` + risk drivers
  - **Tier**: Compound phrase check → keyword scan → context boosters → priority resolution (`STRICT > EXEMPT > LIGHT > STANDARD`)
  - **Confidence**: `max(tier_scores)` capped at 0.95, ambiguity penalty (-15%), phrase boost (+15%), vague penalty (-30%)
  - **Verification routing**: Tier → method + token budget + timeout
  - **MCP tool requirements**: Per-tier tool declarations
  - **Sub-agent delegation**: Required/Recommended/None based on tier + risk
  - **Critical path override**: Path pattern matching (auth/, security/, crypto/, models/, migrations/)
- **Output**: Fully enriched tasks with 13+ metadata fields
- **Determinism**: Full — every scoring formula is explicit, no inference involved
- **Gating**: Confidence < 0.70 → `Requires Confirmation: Yes` + Clarification Task
- **Token cost**: Zero (pure computation, no LLM calls)

#### Stage 5: Assemble Registries & Matrix
- **Input**: Enriched tasks
- **Process**:
  - Deliverable Registry: `D-0001`, `D-0002`, ... with artifact paths (`TASKLIST_ROOT/artifacts/D-####/`)
  - Traceability Matrix: `R-###` → `T<PP>.<TT>` → `D-####` → paths → Tier → Confidence
  - Checkpoints: every 5 tasks + end-of-phase
  - Templates: execution log, checkpoint report, feedback collection
- **Output**: Cross-phase metadata structures
- **Determinism**: Full — IDs assigned in task order, checkpoint cadence fixed
- **Gating**: None

#### Stage 6: Emit Files
- **Input**: All generated content
- **Process**: Write exactly N+1 files
  - `tasklist-index.md` — all cross-phase metadata, registries, matrix, templates
  - `phase-1-tasklist.md` through `phase-N-tasklist.md` — tasks + inline checkpoints
- **Output**: Multi-file bundle at `TASKLIST_ROOT/`
- **Determinism**: Full — file naming convention fixed, content boundary enforced
- **Token cost**: File write operations only

#### Stage 7: Validate Generated Tasklist vs Source Roadmap
- **Input**: Generated tasklist + original roadmap
- **Process**: Systematic comparison:
  - Missing roadmap items (no corresponding task)
  - Fabricated traceability IDs (D-NNNN not in roadmap)
  - Contradicted dependencies
  - Weaker acceptance criteria than roadmap success criteria
- **Output**: Deviation list with severity: HIGH (omit/contradict/fabricate) / MEDIUM (weak detail) / LOW (formatting)
- **Determinism**: LLM-assisted comparison — some inference discretion
- **Gating**: HIGH severity findings trigger Stage 8

#### Stage 8: Patch Drift
- **Input**: Deviation list + generated files
- **Process**: Apply fixes for HIGH and MEDIUM deviations. Re-emit affected phase files.
- **Output**: Corrected phase files
- **Determinism**: Partial — fix strategy involves inference

#### Stage 9: Spot-Check Verification
- **Input**: Patched files
- **Process**: Sample patched items, verify corrections hold
- **Output**: Verification results
- **Determinism**: Partial

#### Stage 10: Emit Validation Artifacts
- **Input**: Validation and patch results
- **Process**: Write to `TASKLIST_ROOT/validation/`
- **Output**: Up to 2 files (validation report + patch log)

---

## 2. SC Adversarial Protocol — 5-Step Pipeline

### Stage Overview

```
INPUT                    GENERATE          STEP 1           STEP 2              STEP 3             STEP 4            STEP 5           OUTPUT
──────                   (Mode B only)     ──────           ──────              ──────             ──────            ──────           ──────
2-10 files ──────────────────────────────► Diff     ──────► Adversarial  ──────► Hybrid     ──────► Refactoring ──► Merge      ──► Merged output
  OR                                       Analysis         Debate              Scoring &          Plan              Execution       + 6 artifacts
Source file ──► [Gen] ──► 2-10 variants ──┘                 (1-3 rounds)        Base Selection     (auto/interactive)               + return contract
                2-10 agents in parallel
```

### Step Details

#### Pre-Step: Variant Generation (Mode B only)
- **Input**: Source file + agent specs (`model[:persona[:"instruction"]]`)
- **Agents**: 2-10, spawned in parallel via Task tool
- **Output**: `variant-N-<model>-<persona>.md` (2-10 files)
- **Cost driver**: 2-10 parallel LLM generation calls
- **Error handling**: Agent failure → retry once → proceed with N-1 (min 2 required)

#### Step 1: Diff Analysis
- **Input**: All variants (2-10 files)
- **Agent**: Analytical agent (single)
- **Process**: 5 analysis categories:
  1. Structural diff (section ordering, hierarchy, headings) → severity Low/Medium/High
  2. Content diff (approach-by-approach, coverage differences)
  3. Contradiction detection (3 categories, falsifiability requirement)
  4. Unique contribution extraction (value: Low/Medium/High)
  5. Shared assumption extraction (STATED/UNSTATED/CONTRADICTED) → UNSTATED promoted to synthetic diff points
- **Output**: `adversarial/diff-analysis.md`
- **Cost**: 1 LLM call (reads all variants)
- **Error handling**: <10% total diff → skip debate, select either variant as base

#### Step 2: Adversarial Debate
- **Input**: All variants + diff-analysis.md
- **Agents**: debate-orchestrator + N advocate agents (one per variant)
- **Process**:
  - Auto-tag diff points: L1 (surface) / L2 (structural) / L3 (state-mechanics). Priority: L3 > L2 > L1
  - Round 1 (PARALLEL): Each advocate presents strengths, steelmans opponents before critiquing
  - Round 2 (SEQUENTIAL, if depth ≥ standard): Rebuttals addressing Round 1 criticisms
  - Round 3 (CONDITIONAL, if depth=deep AND convergence < threshold): Final arguments
  - Convergence: % diff points with agreement vs `--convergence` threshold (default 0.80)
- **Output**: `adversarial/debate-transcript.md` with per-point scoring matrix
- **Cost driver**: N advocates × (1-3 rounds). Deep mode with 10 variants = up to 30 LLM calls
- **Error handling**: Max rounds without convergence → force-select by score, flag for user review
- **Gating**: Convergence threshold determines if Round 3 fires

#### Step 3: Hybrid Scoring & Base Selection
- **Input**: All variants + debate-transcript.md
- **Agent**: debate-orchestrator
- **Process**:
  - Quantitative (50%): RC×0.30 + IC×0.25 + SR×0.15 + DC×0.15 + SC×0.15
  - Qualitative (50%): 30-criterion binary rubric (6 dimensions × 5 criteria), CEV per criterion
  - Edge-case floor: <1/5 on Invariant & Edge Case Coverage → ineligible as base
  - Position bias mitigation: Pass 1 (forward order) + Pass 2 (reverse order) → reconcile disagreements
  - Combined: 0.50 × quant + 0.50 × qual
  - Tiebreaker: debate performance → correctness count → input order (deterministic)
- **Output**: `adversarial/base-selection.md` with full scoring breakdown
- **Cost**: 2 scoring passes (forward + reverse for bias mitigation) + optional reconciliation
- **Gating**: Edge-case floor can disqualify variants; all variants 0/5 → suspend floor with warning

#### Step 4: Refactoring Plan
- **Input**: Selected base + all other variants + debate-transcript.md
- **Agent**: Orchestrator drafts, analytical agent reviews
- **Process**:
  - For each non-base strength: integration point + rationale citing debate evidence
  - For each base weakness: better variant reference + fix approach
  - Changes NOT being made: documented with rationale (transparency)
- **Output**: `adversarial/refactor-plan.md`
- **Interactive mode**: User can modify plan before execution
- **Non-interactive**: Auto-approved
- **Cost**: 1-2 LLM calls (draft + review)

#### Step 5: Merge Execution
- **Input**: Base variant + refactor-plan.md
- **Agent**: merge-executor (dedicated specialist)
- **Process**: Apply changes → maintain structural integrity → provenance annotations → validate (structure, references, contradiction re-scan)
- **Output**: `<merged-output>.md` + `adversarial/merge-log.md`
- **Return contract** (MANDATORY, always emitted):
  ```yaml
  merged_output_path: string | null
  convergence_score: float 0.0-1.0 | null
  artifacts_dir: string  # always set
  status: success | partial | failed
  base_variant: string | null  # model:persona that won
  ```
- **Error handling**: Merge failure → preserve all artifacts, provide refactor-plan.md for manual execution
- **Cost**: 1 LLM call

### Pipeline Mode (DAG Extension)
- Parses inline shorthand (`generate:agents -> compare`) or YAML file into phase graph
- Topological sort with configurable parallelism (`--pipeline-parallel`, default 3)
- Artifact routing: output of phase N becomes input of phase N+1
- Manifest-based resume: `--pipeline-resume` skips completed phases
- Error policy: `--pipeline-on-error halt` stops all; `continue` lets independent branches proceed
- Convergence plateau detection: `--auto-stop-plateau` halts on <5% delta across 2 consecutive compare phases

---

## 3. RF Pipeline — 9-Phase Pipeline + Inner Batch Loop

### Outer Pipeline (9 phases)

```
USER REQUEST
     │
     ▼
[Phase 1] Parse/Triage/Split ── TRACK_COUNT: 1-5
     │
     ▼
[Phase 2] TeamCreate("rf-pipeline")
     │
     ▼
[Phase 3] Create 3×N coordination tasks (research→build→execute per track)
     │
     ▼
[Phase 4] Spawn researcher(s) ── N researchers in parallel
     │                            │
     │                            ▼
     │                       RESEARCH_READY (per track, event-driven)
     │                            │
     ▼                            ▼
[Phase 5] Review research ─► GATE: sufficient? ─► Spawn builder(s) ── event-driven per track
     │         │   no ──► message researcher for revision (loop)
     │         │
     │         ▼
     │    TASK_READY (per track)
     │         │
     ▼         ▼
[Phase 6] Spawn executor(s) ── event-driven per track
     │
     ▼
[Phase 7] Monitor messages ── relay user input, handle errors per-track
     │
     ▼
[Phase 8] Report results ── per-track + overall status
     │
     ▼
[Phase 9] Cleanup ── shutdown all agents → TeamDelete
```

### Inner Batch Loop (automated_qa_workflow.sh, per executor)

```
┌────────────────────────────────────────────────────────────────────────┐
│ INITIALIZATION                                                         │
│  ├── validate_task_name (security: path traversal defense)             │
│  ├── Find PROJECT_ROOT (traverse up to .gfdoc/)                        │
│  ├── Create workspace dirs (conversations, outputs, handoffs, qa, logs)│
│  ├── Source helper scripts (validation, session counter, rollover)      │
│  └── Configure PABLOV (snapshot root, excludes, hash, strict mode)     │
└────────────────────────────────┬───────────────────────────────────────┘
                                 │
                                 ▼
┌────────────────────────────────────────────────────────────────────────┐
│ FOR EACH BATCH (1..N until all items checked or MAX_ITERATIONS)        │
│                                                                        │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │ ① BATCH SETUP                                                   │   │
│  │    parse_checklist → get_next_batch(BATCH_SIZE)                 │   │
│  │    → expected_batchN.json + batch_N_state.json (initialized)    │   │
│  └──────────────────────────────┬──────────────────────────────────┘   │
│                                 │                                      │
│  ┌──────────────────────────────▼──────────────────────────────────┐   │
│  │ ② PABLOV PRE-SNAPSHOT                                          │   │
│  │    fs_snapshot_pre_batchN.json                                  │   │
│  └──────────────────────────────┬──────────────────────────────────┘   │
│                                 │                                      │
│  ┌──────────────────────────────▼──────────────────────────────────┐   │
│  │ ③ RUN WORKER                                                    │   │
│  │    ├── Session check: messages ≥ 375 OR tokens ≥ 175K → ROLL   │   │
│  │    │   └── generate_rollover_context → new session              │   │
│  │    ├── Batch refresh:                                           │   │
│  │    │   ├── Normal: get_next_batch (fresh unchecked items)       │   │
│  │    │   └── Correction: UID-based refresh (stable batch identity)│   │
│  │    ├── Worker prompt: task + expected items + core rules + QA   │   │
│  │    │   feedback (if correction)                                 │   │
│  │    └── claude --continue <session> -p "<prompt>"                │   │
│  │        State: initialized → worker_in_progress → worker_complete│   │
│  └──────────────────────────────┬──────────────────────────────────┘   │
│                                 │                                      │
│  ┌──────────────────────────────▼──────────────────────────────────┐   │
│  │ ④ VERIFY + ⑤ POST-SNAPSHOT + ⑥ PABLOV EVIDENCE                 │   │
│  │    ├── Verify: check [x] items match expected set               │   │
│  │    ├── fs_snapshot_post_batchN.json                             │   │
│  │    ├── Mine worker conversation (JSONL → mentions, files)       │   │
│  │    ├── Bind evidence to batch items                             │   │
│  │    ├── Filter fs delta by conversation evidence                 │   │
│  │    ├── (Optional) Collect git diffs                             │   │
│  │    └── Create programmatic_handoff_batchN.json                  │   │
│  └──────────────────────────────┬──────────────────────────────────┘   │
│                                 │                                      │
│  ┌──────────────────────────────▼──────────────────────────────────┐   │
│  │ ⑦ SYNTHESIZE WORKER HANDOFF                                     │   │
│  │    → handoffs/worker_handoff_batchN.md (rich per-item evidence) │   │
│  └──────────────────────────────┬──────────────────────────────────┘   │
│                                 │                                      │
│  ┌──────────────────────────────▼──────────────────────────────────┐   │
│  │ ⑧ RUN QA (NEW session each time)                                │   │
│  │    ├── QA prompt: expected items + programmatic handoff +       │   │
│  │    │   worker handoff + fs snapshots + conversation snippets    │   │
│  │    ├── claude -p "<qa_prompt>"                                  │   │
│  │    ├── QA writes qa_report_batchN.md                            │   │
│  │    │   First line: "Overall Status: PASS" | "Overall Status:   │   │
│  │    │   FAIL"                                                    │   │
│  │    │   Fail: "- Line <n>: FAIL — <reason>"                     │   │
│  │    └── DNSP if report missing:                                  │   │
│  │        ├── Nudge: 1 resume attempt                              │   │
│  │        └── Synthesize: minimal report from programmatic handoff │   │
│  └──────────────────────────────┬──────────────────────────────────┘   │
│                                 │                                      │
│  ┌──────────────────────────────▼──────────────────────────────────┐   │
│  │ ⑨ QA VERDICT ROUTING                                            │   │
│  │    ├── PASS → state = "qa_complete" → NEXT BATCH               │   │
│  │    ├── FAIL + 0 bullets → normalize to PASS (contradiction fix) │   │
│  │    └── FAIL → preserve report → uncheck failed items →          │   │
│  │        reset state → RE-ENTER WORKER (⑩ correction loop)       │   │
│  └──────────────────────────────┬──────────────────────────────────┘   │
│                                 │                                      │
│  ┌──────────────────────────────▼──────────────────────────────────┐   │
│  │ ⑩ CORRECTION LOOP (max 5 cycles per batch)                      │   │
│  │    ├── Worker receives: original items + QA failure details     │   │
│  │    ├── Uses UID-based batch refresh (stable identity)           │   │
│  │    ├── QA re-reviews corrected work                             │   │
│  │    └── If max corrections hit:                                  │   │
│  │        ├── CORRECTION_LIMIT_HIT = true                          │   │
│  │        └── HALT (manual intervention required)                  │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                                                        │
│ LOOP TERMINATION:                                                      │
│  ├── All items checked → TASK_COMPLETED                                │
│  ├── MAX_ITERATIONS reached → partial progress report                  │
│  └── CORRECTION_LIMIT_HIT → failure notification + diagnostics         │
└────────────────────────────────────────────────────────────────────────┘
```

### Batch State Machine

```
                    ┌──────────────┐
                    │ initialized  │◄────────────────────────────────┐
                    └──────┬───────┘                                 │
                           │ run_worker()                            │
                           ▼                                         │
                    ┌──────────────────┐                             │
                    │ worker_in_progress│                            │
                    └──────┬───────────┘                             │
                           │ worker completes                        │
                           ▼                                         │
                    ┌──────────────────┐                             │
                    │ worker_complete   │                            │
                    └──────┬───────────┘                             │
                           │ run_qa()                                │
                           ▼                                         │
                    ┌──────────────────┐                             │
                    │ qa_in_progress   │                             │
                    └──────┬───────────┘                             │
                           │ QA writes report                        │
                           ▼                                         │
                    ┌──────────────────┐                             │
                    │ qa_complete      │                             │
                    └──────┬───────────┘                             │
                           │                                         │
                    ┌──────┴──────┐                                  │
                    │             │                                   │
                  PASS          FAIL                                  │
                    │             │                                   │
                    ▼             ▼                                   │
              [NEXT BATCH]   uncheck failed items                    │
                             reset state to ─────────────────────────┘
                             "initialized"
                             (correction cycle N of 5)
```

---

## 4. Session Management Model (RF Only)

```
Worker Session Lifecycle:
─────────────────────────
Batch 1 ──► Batch 2 ──► Batch 3 ──► ... (same session via --continue)
                                         │
                                    ROLL THRESHOLD HIT
                                    (≥375 messages OR ≥175K tokens)
                                         │
                                         ▼
                                    Generate rollover context
                                    Create new session
                                    Continue from current batch

QA Session Lifecycle:
─────────────────────
Batch 1 QA ──► [new session]
Batch 2 QA ──► [new session]
Batch 3 QA ──► [new session]
(always fresh — no context contamination)

Session Recovery (crash/death):
───────────────────────────────
1. Detect dead session (health check fails)
2. Scan batch_N_state.json files
3. Find highest incomplete batch
4. Generate context from conversation JSONL
5. Create new session with rollover context
6. Resume from incomplete batch
```

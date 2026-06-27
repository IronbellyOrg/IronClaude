# Design: RF Mechanism Import into sc:tasklist

**Generated**: 2026-04-02
**Author**: /sc:design --seq
**Scope**: Strengths/weaknesses matrix, compatibility map, 5 refactor proposals, prioritized adoption roadmap
**Target**: `sc:tasklist-protocol` SKILL.md (v4.0, 51KB) + `sc-tasklist-protocol/` skill package

---

## 1. Strengths & Weaknesses Matrix

### sc:tasklist

| # | Strength | Evidence Location | Why It Matters |
|---|----------|-------------------|----------------|
| S1 | **Full determinism** — same roadmap → same tasklist, every time | SKILL.md:30-43, Sections 4.1-4.11 | Reproducibility enables regression testing, diff-based reviews, and CI integration. No human needed to judge "did it produce the right output?" — you can diff against a known-good baseline |
| S2 | **Tier classification with confidence scoring** — every task gets STRICT/STANDARD/LIGHT/EXEMPT + 0-95% confidence | SKILL.md Section 5.3, rules/tier-classification.md | Drives verification routing, MCP tool requirements, sub-agent delegation, and token budgets. The confidence score identifies tasks that need human confirmation (<0.70) before execution |
| S3 | **Traceability matrix** — R-### → T<PP>.<TT> → D-#### → artifact paths → Tier → Confidence | SKILL.md Section 5.7, templates/index-template.md | Complete lineage from roadmap requirement to deliverable to artifact. Sprint executor can verify that every roadmap item is addressed and every deliverable is produced |
| S4 | **17-point pre-write quality gate** — structural + semantic + specificity checks before any file is written | SKILL.md lines 756-808 | Write atomicity: no partial or malformed bundles ever hit disk. Catches empty phases, orphan clarification tasks, circular dependencies, duplicate deliverable IDs, placeholder descriptions |
| S5 | **Post-generation validation (Stages 7-10)** — 2N parallel agents validate, patch, spot-check | SKILL.md lines 857-1050 | Catches drift, contradictions, omissions, weakened criteria, and invented content. Self-healing: patches are applied and verified, not just reported |
| S6 | **Multi-file bundle + Sprint CLI compatibility** — index + phase files, regex-discoverable naming | SKILL.md Section 3.3, rules/file-emission-rules.md | Enables `superclaude sprint run` phase discovery. Each phase file is a self-contained execution unit with no cross-phase metadata bleeding |
| S7 | **Non-leakage rules** — no invented context, no file access claims, no embedded override attempts | SKILL.md lines 19-27 | Prevents the generator from hallucinating repository structure, team assignments, timelines, or test outcomes that don't exist in the roadmap |

| # | Weakness | Evidence Location | Impact |
|---|----------|-------------------|--------|
| W1 | **No execution resilience** — if generation fails mid-way, no checkpoint or resume. Write atomicity means all-or-nothing | SKILL.md line 816 ("Write atomicity... all files written only after full bundle passes") | Large roadmaps with many phases risk a single validation failure aborting the entire bundle. No incremental progress is preserved |
| W2 | **Validation is LLM-only** — Stages 7-10 rely entirely on agent inference to detect drift. No programmatic evidence (filesystem snapshots, diffing, checksums) | SKILL.md lines 862-901 (validation instructions are free-text comparison prompts) | LLM agents can miss subtle drift, hallucinate findings, or disagree with each other. No machine-verifiable ground truth to anchor the validation |
| W3 | **No execution-time feedback loop** — tasklist is generated and validated, but there is no mechanism to learn from Sprint execution failures and improve future generation | (Absence) Feedback Log Template exists (SKILL.md line 575-591) but is a placeholder — no generator reads it | Tier miscalculations, effort misestimates, and structural problems repeat across runs. The Feedback Log Template is defined but never consumed |
| W4 | **No session/context protection for the executor** — the Sprint CLI executes tasks sequentially, but there is no mechanism to ensure context from Phase 1 persists into Phase 5 | (Absence) Phase files are self-contained (good for generation), but task steps assume context availability during execution | A multi-phase sprint can lose early context to compression or rollover. Tasks don't embed the context references needed for late-phase execution |
| W5 | **Single-pass correction** — Stages 8-9 patch once and spot-check once. If the patch introduces new issues or the spot-check misses something, there is no second pass | SKILL.md lines 1026-1049 ("does NOT loop") | Patches that introduce regressions or miss edge cases go undetected. The UNRESOLVED findings are logged but not fixed |
| W6 | **No PABLOV-style evidence collection** — validation agents compare text-to-text (roadmap vs tasklist) without any programmatic artifact to anchor their judgments | (Absence) No equivalent of fs snapshots, conversation mining, or programmatic handoffs | Agent validation is opinion-based rather than evidence-based. Two runs of validation can produce different findings for the same input |

### RF taskbuilder + pipeline

| # | Strength | Evidence Location | Why It Matters |
|---|----------|-------------------|----------------|
| R1 | **Self-contained checklist items** — every item is a complete prompt with context refs, action, output spec, verification clause, completion gate | taskbuilder.md:184-264, rf-task-builder.md:200-214 | Survives session rollovers. Context from batch 1 is not needed in batch 5 because every item carries its own context. This is the critical innovation for long-running execution |
| R2 | **PABLOV evidence collection** — fs snapshots before/after, conversation mining from JSONL, programmatic handoffs with machine-verifiable facts | automated_qa_workflow.sh:2353-2730 (pablov_* functions) | QA validation is anchored to machine evidence, not LLM opinion. "Did the worker actually create this file?" has a binary answer from the filesystem, not an inference |
| R3 | **DNSP protocol** — Detect missing artifacts → Nudge agent once → Synthesize minimal artifact → Proceed | automated_qa_workflow.sh:4698-4723 (run_qa DNSP), 3014-3150 (synthesize functions) | Never wedges on recoverable errors. If the QA agent fails to produce a report, the system synthesizes one from programmatic evidence and continues. Maximizes forward progress |
| R4 | **Correction loops** — up to 5 worker/QA cycles per batch with targeted feedback from QA failures | automated_qa_workflow.sh:5377-5523 (max_correction_cycles) | Self-healing at execution time. Failed items get specific QA feedback, worker retries with that feedback, and QA re-validates. This catches and fixes real issues, not just reports them |
| R5 | **Session management** — dual-threshold rollover (375 messages OR 175K tokens), crash recovery from batch state JSON, rollover context generation | automated_qa_workflow.sh:4234-4298 (session roll logic) | Handles real-world constraints: context windows fill up, sessions crash, VS Code restarts. The system recovers without losing work |
| R6 | **Batch immutability + UID tracking** — batch items are fixed once created; UID-based refresh preserves identity across user edits mid-execution | automated_qa_workflow.sh:4324-4343 (UID-based refresh) | Users can edit future task items without corrupting in-progress batches. The system adapts to edits without losing QA feedback alignment |

| # | Weakness | Evidence Location | Impact |
|---|----------|-------------------|--------|
| X1 | **No determinism** — researcher explores freely, builder synthesizes creatively, task structure varies per run | (Inherent to agent exploration model) | Cannot diff two runs of the same input. Cannot regression-test task generation. Cannot predict output structure for CI integration |
| X2 | **No tier/compliance classification** — tasks have no STRICT/STANDARD/LIGHT/EXEMPT designation. All items get equal treatment | (Absence — no tier system in RF templates or taskbuilder) | Security-critical items get the same verification depth as trivial formatting fixes. No verification routing, no confidence scoring, no escalation path for high-risk tasks |
| X3 | **No traceability** — no formal mapping from requirements to tasks to deliverables | (Absence — RF tasks reference source context per-item but no matrix) | Cannot verify that all requirements are addressed. Cannot audit which requirement drove which task. No deliverable registry |
| X4 | **Extremely token-expensive** — self-contained items duplicate context, worker sessions accumulate to 175K before rolling, each batch = 2 Claude processes | automated_qa_workflow.sh:150-151 (175K threshold), taskbuilder.md:33-35 (context duplication) | 500K-1M+ tokens per task execution. 5-10x more expensive than SC tasklist generation for comparable output |
| X5 | **Sequential batch execution** — batches run one at a time within a track. No parallelism within a single task | automated_qa_workflow.sh main loop (serial for-each) | 15-45 minute wall-clock for a 12-item task. Parallel batch execution would reduce this significantly but requires architectural changes to the worker session model |

---

## 2. Compatibility Map: RF Strengths → sc:tasklist Import

| RF Strength | SC Area Affected | Import Effort | Rationale |
|-------------|-----------------|---------------|-----------|
| **R1: Self-contained items** | Phase file task format (templates/phase-template.md, SKILL.md Section 6B) | **Low** | Add an "ensuring..." verification clause and context reference embedding to each task's Steps. The phase template already has structured Steps; this enriches them. No protocol logic changes required — only template additions |
| **R2: PABLOV evidence** | Stage 7-10 validation (SKILL.md lines 857-1050) | **High** | Requires adding filesystem snapshot logic, conversation mining from Sprint execution logs, and a programmatic handoff schema. SC validation currently has no runtime evidence — it compares text-to-text. Would need a new `validation-evidence/` artifact directory and modified agent prompts |
| **R3: DNSP protocol** | Stage 7 agent failure handling (SKILL.md line 911: "retry once before reporting error") | **Medium** | Current behavior: retry once, then report error. DNSP adds: after retry failure, synthesize a minimal finding from available evidence and proceed. Requires a synthesis function per validation agent type, but the agent spawning infrastructure already exists |
| **R4: Correction loops** | Stage 9 patch execution (SKILL.md lines 1005-1021) + Stage 10 spot-check (lines 1026-1049) | **Medium** | Current behavior: patch once, spot-check once, log UNRESOLVED, stop. Adding a bounded correction loop (max 2-3 cycles) where UNRESOLVED findings trigger re-patching would close the gap. The `sc:task-unified` delegation mechanism already supports re-invocation |
| **R5: Session management** | (Not applicable to generation) Relevant to Sprint execution, not to sc:tasklist itself | **N/A** | SC tasklist generates files; Sprint CLI executes them. Session management belongs in the Sprint CLI or `sc:task-unified` executor, not in the generator. Already present in the `superclaude sprint run` Python CLI |
| **R6: Batch immutability + UID tracking** | (Not applicable) SC tasklist produces a static bundle; there is no "batch" concept during generation | **N/A** | Batch immutability is an execution-time concept. SC tasklist's write atomicity (all-or-nothing) serves the same purpose at generation time — no partial outputs to corrupt |

---

## 3. Refactor Proposals

### Proposal 1: "Context-Armed Steps" (from R1: Self-Contained Items)

**Exact sc:tasklist area touched**:
- `SKILL.md` Section 6B — Phase File Template, task Steps format (lines 646-653)
- `templates/phase-template.md` — Steps section
- `SKILL.md` Section 4.7 — Acceptance Criteria and Validation

**What RF mechanism is borrowed**:
RF's self-contained checklist item pattern: every step embeds its context references, action, output specification, and an "ensuring..." verification clause in a single paragraph. From `rf-task-builder.md:200-214`.

**Change**:
Add a `Context` field to each EXECUTION step and an `ensuring` clause to the Acceptance Criteria. Currently, Steps are bare imperative sentences:

```
# CURRENT (SKILL.md Section 6B)
3. **[EXECUTION]** Implement rate limiting middleware
4. **[EXECUTION]** Add authentication checks

# PROPOSED
3. **[EXECUTION]** Implement rate limiting middleware
   Context: `src/middleware/`, `docs/api-spec.md` Section 3.2 (rate limit requirements)
   Ensuring: middleware file exists at expected path, rate limit config matches spec values
4. **[EXECUTION]** Add authentication checks
   Context: `src/auth/`, R-015 (auth requirements from roadmap)
   Ensuring: all protected endpoints return 401 without valid token
```

**Expected quality gain**: **Medium-High**. Sprint executor sessions that run Phase 5 can reference the exact source files and verification criteria without re-reading the entire roadmap. Reduces context-window waste during execution and makes QA verification criteria explicit per step.

**Added complexity**: **Low**. Two new sub-fields per EXECUTION step. No protocol logic changes. Template modification only.

**Speed impact**: **Negligible**. Generation adds ~10-20 tokens per step. Does not add LLM calls.

**Token/cost impact**: **+5-10% on generated output size** (added context/ensuring lines). **-10-20% during Sprint execution** (executor doesn't need to re-derive context).

**Risk level**: **Low**. Backward compatible — Sprint CLI ignores unrecognized sub-fields. Existing tasklists continue to work.

**Rollback strategy**: Remove `Context:` and `Ensuring:` sub-fields from template. Re-generate tasklist. Zero residual impact.

---

### Proposal 2: "Bounded Patch Loop" (from R4: Correction Loops)

**Exact sc:tasklist area touched**:
- `SKILL.md` Stage 9 — Patch Execution (lines 1005-1021)
- `SKILL.md` Stage 10 — Spot-Check Verification (lines 1026-1049)
- New: loop control between Stages 9 and 10

**What RF mechanism is borrowed**:
RF's correction loop: QA fails → worker retries with failure feedback → QA re-validates → up to 5 cycles. From `automated_qa_workflow.sh:5377-5523`.

**Change**:
After Stage 10, if UNRESOLVED findings remain, loop back to Stage 9 with only the UNRESOLVED subset. Cap at 2 additional cycles (3 total passes including the original).

```
# CURRENT
Stage 9: Patch → Stage 10: Spot-check → Log UNRESOLVED → Done

# PROPOSED
Stage 9: Patch → Stage 10: Spot-check → If UNRESOLVED:
  → Re-patch ONLY unresolved items (Stage 9b, max 2 more cycles)
  → Re-verify ONLY re-patched items (Stage 10b)
  → If still UNRESOLVED after 3 total passes: log and stop (same as current)
```

**Expected quality gain**: **Medium**. Currently, patches that introduce regressions or that `sc:task-unified` applies imperfectly are logged but never fixed. A bounded loop catches the most common case: a patch that was almost right but missed a detail.

**Added complexity**: **Low-Medium**. A while-loop wrapper around Stages 9-10 with a counter and a filtered finding list. The `sc:task-unified` delegation mechanism is already invocable; calling it again with a smaller checklist is straightforward.

**Speed impact**: **0-2 additional LLM calls** per loop iteration (one for patch, one for spot-check). Worst case: +4 calls if both extra cycles fire. Typical case: 0 extra calls (most runs have zero UNRESOLVED findings).

**Token/cost impact**: **+0% typical, +15-25% worst case**. Only fires when patches fail, which is uncommon.

**Risk level**: **Low**. The loop is bounded (max 3 total). Worst case: 2 unnecessary re-patch attempts that produce the same UNRESOLVED result. The existing "log and stop" behavior is preserved as the terminal condition.

**Rollback strategy**: Remove the loop wrapper. Stages 9-10 revert to single-pass. Zero impact on generated output.

---

### Proposal 3: "DNSP for Validation Agents" (from R3: DNSP Protocol)

**Exact sc:tasklist area touched**:
- `SKILL.md` Stage 7 — Roadmap Validation, agent failure handling (line 911)
- `SKILL.md` Stage 8 — Patch Plan Generation (lines 913-1003)

**What RF mechanism is borrowed**:
RF's DNSP (Detect-Nudge-Synthesize-Proceed) protocol: if an agent fails to produce its expected artifact, nudge once, then synthesize a minimal artifact from available context and proceed. From `automated_qa_workflow.sh:4698-4723`.

**Change**:
Current Stage 7 behavior: "if an agent fails, retry once before reporting error." This is Detect-Nudge only. If the retry also fails, the entire validation stage fails.

Proposed: After the retry fails, **synthesize a conservative finding list** from what we know:
- If the agent returned partial output, extract whatever structured findings exist
- If the agent returned nothing, synthesize a single HIGH finding: "Validation agent failed for tasks T<PP>.<start>-T<PP>.<end>. Manual review required."
- Proceed to Stage 8 with the synthesized finding included

```
# CURRENT (SKILL.md line 911)
"if an agent fails, retry once before reporting error"

# PROPOSED
For each of the 2N agents:
  Run agent → if success: collect findings
  If failure: retry once → if success: collect findings
  If retry failure:
    If partial output available: extract structured findings from partial
    Else: synthesize HIGH finding: "Manual review required for tasks [range]"
    Proceed (never block Stage 8 on a single agent failure)
```

**Expected quality gain**: **Medium**. Prevents a single agent timeout or crash from aborting the entire validation stage. The synthesized "manual review required" finding is conservative — it doesn't hallucinate, it flags for human review.

**Added complexity**: **Low**. ~20 lines of conditional logic in the orchestrator merge step (after all 2N agents return). The synthesis is a template fill, not an LLM call.

**Speed impact**: **Positive**. Currently, a single agent failure blocks validation. DNSP allows the other 2N-1 agents' findings to be used immediately. Net effect: validation completes faster when agents are flaky.

**Token/cost impact**: **Neutral**. Synthesis is template-based, zero LLM tokens. The retry is already present.

**Risk level**: **Very Low**. The synthesized finding is maximally conservative (flag for manual review). No false negatives — it never says "no issues found" when an agent failed. Worse case: a false HIGH finding that a human quickly clears.

**Rollback strategy**: Revert to current behavior: "retry once, then report error." One-line change in the orchestrator.

---

### Proposal 4: "Evidence-Anchored Validation" (from R2: PABLOV Evidence)

**Exact sc:tasklist area touched**:
- `SKILL.md` Stage 7 — Validation agent instructions (lines 882-901)
- `SKILL.md` Stage 8 — ValidationReport.md format (lines 926-956)
- New: evidence artifact directory `TASKLIST_ROOT/validation/evidence/`
- New: pre-validation evidence collection step (between Stage 6 and Stage 7)

**What RF mechanism is borrowed**:
RF's PABLOV evidence collection: filesystem snapshots, programmatic verification of generated artifacts, and binding evidence to specific items. From `automated_qa_workflow.sh:2353-2730` (pablov_* functions) and programmatic_handoff schema.

**Change**:
Add a **Stage 6.5: Evidence Collection** between the current Stage 6 (Self-Check) and Stage 7 (Validation). This stage programmatically verifies the generated bundle and produces machine-readable evidence that validation agents can reference:

```
Stage 6.5: Evidence Collection (NEW)
──────────────────────────────────────
For each generated file:
  1. Verify file exists and is non-empty
  2. Extract task IDs (regex: T\d{2}\.\d{2}) → actual_task_ids[]
  3. Extract deliverable IDs (regex: D-\d{4}) → actual_deliverable_ids[]
  4. Extract roadmap item references (regex: R-\d{3}) → actual_roadmap_refs[]
  5. Count tasks per phase, checkpoints per phase
  6. Verify all D-#### in phase files appear in index Deliverable Registry
  7. Verify all R-### in phase files appear in index Traceability Matrix

Produce: TASKLIST_ROOT/validation/evidence/generation-evidence.json
{
  "files_generated": ["tasklist-index.md", "phase-1-tasklist.md", ...],
  "task_ids_found": ["T01.01", "T01.02", ...],
  "deliverable_ids_found": ["D-0001", "D-0002", ...],
  "roadmap_refs_found": ["R-001", "R-002", ...],
  "orphan_deliverables": [],       // D-#### in phases but not in registry
  "orphan_roadmap_refs": [],       // R-### in phases but not in matrix
  "missing_roadmap_items": [],     // R-### in roadmap but not in any phase
  "tasks_per_phase": {"1": 5, "2": 7, ...},
  "checkpoints_per_phase": {"1": 2, "2": 2, ...}
}
```

Then modify Stage 7 agent instructions to include this evidence:

```
# CURRENT Stage 7 agent instruction
"For each task in your assigned range, check: Drift, Contradictions, ..."

# PROPOSED: append to agent instruction
"Reference the generation evidence at validation/evidence/generation-evidence.json.
If the evidence shows orphan_deliverables or missing_roadmap_items,
flag these as HIGH findings immediately — they are machine-verified facts,
not opinions. Focus your inference on semantic drift, weakened criteria,
and invented content that programmatic checks cannot detect."
```

**Expected quality gain**: **High**. The most common validation failures — missing roadmap items, orphan deliverable IDs, broken traceability — become machine-verifiable rather than inference-dependent. Agents can focus their token budget on the harder semantic checks that actually need LLM judgment.

**Added complexity**: **Medium**. A new stage (6.5) with regex-based extraction and JSON generation. The extraction is purely programmatic (Bash/Python, no LLM calls). Agent prompt changes are additive (append, don't rewrite).

**Speed impact**: **Positive**. Evidence collection is sub-second (regex over a few markdown files). Validation agents get pre-computed facts, reducing their inference burden and improving accuracy.

**Token/cost impact**: **-10-15% on validation agent tokens** (agents skip verifying things the evidence already proves). **+negligible** for evidence collection (no LLM calls).

**Risk level**: **Low-Medium**. The evidence JSON could have bugs in its regex extraction. Mitigation: the evidence is supplementary — agents still run full validation. False evidence would cause a validation agent to flag a false finding, which Stage 10 spot-check would catch. The evidence never suppresses agent investigation.

**Rollback strategy**: Remove Stage 6.5. Remove evidence reference from Stage 7 agent prompts. Revert to current text-only validation. Zero impact on generated output.

---

### Proposal 5: "Feedback-Driven Tier Calibration" (from RF's Agent Memory + Correction Patterns)

**Exact sc:tasklist area touched**:
- `SKILL.md` Section 5.3 — Tier Classification (lines 337-394)
- `SKILL.md` Section 5.4 — Confidence Scoring (lines 396-406)
- `templates/index-template.md` — Feedback Collection Template (currently a placeholder)
- New: `rules/tier-calibration-overrides.md` reference file

**What RF mechanism is borrowed**:
RF's agent memory system: agents accumulate institutional knowledge across conversations. `rf-task-builder.md:363-368` stores learned patterns. Combined with RF's correction loop pattern: failures feed back into future behavior.

**Change**:
The Feedback Collection Template (SKILL.md lines 575-591) already defines a `feedback-log.md` with columns for `Original Tier`, `Override Tier`, `Override Reason`, `Completion Status`, `Quality Signal`, `Time Variance`. But currently, **no generator reads this file**.

Proposed: Add a pre-generation step that reads any existing `feedback-log.md` from a prior Sprint run in the same `TASKLIST_ROOT` and applies tier calibration overrides:

```
Stage 0: Tier Calibration (NEW, optional)
──────────────────────────────────────────
IF TASKLIST_ROOT/feedback-log.md exists AND contains entries:
  Parse each row where Override Tier != Original Tier
  Build calibration map: { keyword_pattern → tier_adjustment }
  
  Example: if feedback shows "add rate limiting" was classified STANDARD
  but overridden to STRICT 3 times → add "rate limit" to STRICT compound phrases
  
  Store as TASKLIST_ROOT/validation/tier-calibration.json
  Apply adjustments during Stage 4 (Enrich Tasks) as additional context boosters
  Log all applied calibrations in Generation Notes section
```

**Expected quality gain**: **Medium-High over time**. First run: zero effect (no feedback data). Second run: tier accuracy improves for patterns that were miscalculated previously. Cumulative improvement across Sprint iterations within a release.

**Added complexity**: **Medium**. Requires: (1) parsing feedback-log.md, (2) computing calibration adjustments, (3) injecting adjustments into the deterministic tier algorithm without breaking its determinism guarantees. The calibration is itself deterministic (same feedback → same adjustments), preserving the overall determinism property.

**Speed impact**: **Negligible**. Parsing a small markdown table + applying a handful of score adjustments.

**Token/cost impact**: **Neutral** for generation. **-5-10% for Sprint execution over time** (fewer tier misclassifications → fewer failed verification steps → fewer retries).

**Risk level**: **Medium**. The calibration could over-correct: if one unusual task was overridden, the generator might apply that override to all similar keywords. Mitigation: require at least 2 matching feedback entries before applying a calibration. Log all calibrations transparently in Generation Notes.

**Rollback strategy**: Remove Stage 0. Delete `tier-calibration.json`. Tier classification reverts to pure keyword-based scoring. No impact on generated output structure — only tier values change.

---

## 4. Prioritized Adoption Roadmap

### Phase 1: Quick Wins (1-2 days each, low risk, immediate value)

```
Priority 1 ──► Proposal 3: "DNSP for Validation Agents"
               Effort: Low (~20 lines of conditional logic)
               Risk: Very Low
               Value: Prevents validation stage from aborting on flaky agents
               Why first: Zero downside, immediate resilience improvement,
                         no template or schema changes

Priority 2 ──► Proposal 1: "Context-Armed Steps"
               Effort: Low (template modification only)
               Risk: Low (backward compatible)
               Value: Sprint executor sessions waste less context re-deriving
                     sources; QA verification becomes explicit per step
               Why second: Pure additive change, no protocol logic touched,
                          immediately improves Sprint execution quality
```

### Phase 2: Core Improvements (3-5 days each, medium complexity, high value)

```
Priority 3 ──► Proposal 2: "Bounded Patch Loop"
               Effort: Low-Medium (loop wrapper around Stages 9-10)
               Risk: Low (bounded, preserves current terminal behavior)
               Value: Self-healing patches — catches the "almost right" fixes
               Why third: Builds on existing Stage 9-10 infrastructure,
                         small change with disproportionate quality gain

Priority 4 ──► Proposal 4: "Evidence-Anchored Validation"
               Effort: Medium (new Stage 6.5 + agent prompt modifications)
               Risk: Low-Medium (evidence is supplementary, not replacing)
               Value: Highest quality gain — machine-verifiable facts replace
                     inference-only validation for structural checks
               Why fourth: Requires a new stage, JSON schema definition,
                          and agent prompt changes — more moving parts
                          than Proposals 1-3
```

### Phase 3: Long-Term Evolution (1-2 weeks, requires design iteration)

```
Priority 5 ──► Proposal 5: "Feedback-Driven Tier Calibration"
               Effort: Medium (feedback parsing + calibration injection)
               Risk: Medium (over-correction potential)
               Value: Cumulative improvement across Sprint iterations;
                     tier accuracy improves with every execution cycle
               Why last: Requires at least one Sprint run to generate
                        feedback data. Value is zero on first use.
                        Needs careful testing of calibration thresholds
                        to avoid over-correction
```

### Adoption Dependency Graph

```
[P3: DNSP] ──────────────────────────────────────────────────► standalone
[P1: Context-Armed Steps] ───────────────────────────────────► standalone
[P2: Bounded Patch Loop] ───────────────────────────────────► standalone
[P4: Evidence-Anchored Validation] ──depends-on──► [P3: DNSP]
    (evidence collection feeds validation agents;
     DNSP handles cases where evidence-consuming agents fail)
[P5: Feedback Calibration] ──depends-on──► at least 1 Sprint run
    (needs execution feedback to calibrate against)
```

### Total Investment Summary

| Proposal | Effort | LLM Cost Impact | Quality Gain | Risk |
|----------|--------|----------------|--------------|------|
| P3: DNSP | ~20 lines | Neutral | Medium | Very Low |
| P1: Context-Armed Steps | Template edit | +5% gen / -15% exec | Medium-High | Low |
| P2: Bounded Patch Loop | Loop wrapper | +0-25% worst case | Medium | Low |
| P4: Evidence-Anchored | New stage + prompts | -10-15% validation | High | Low-Medium |
| P5: Feedback Calibration | New stage + parsing | Neutral gen / -5-10% exec | Medium-High (cumulative) | Medium |

**Net effect of all 5 proposals**: Validation quality rises substantially (evidence-anchored + correction loops + DNSP resilience), Sprint execution improves (context-armed steps + tier calibration), and the generator becomes self-healing at both generation time (patch loops) and across runs (feedback calibration). Total added complexity is moderate — no architectural changes, all changes are additive to existing stages.

---

## Examples

### Example: Context-Armed Step (Proposal 1) Before/After

**Before** (current phase-template.md format):
```markdown
### T02.03 -- Add Rate Limiting Middleware

| Field | Value |
|---|---|
| Roadmap Item IDs | R-015, R-016 |
| Tier | STRICT |
| Confidence | [████████--] 80% |
| Verification Method | Sub-agent (quality-engineer) |
...

**Steps:**
1. **[PLANNING]** Load context and identify scope
2. **[PLANNING]** Check dependencies and blockers
3. **[EXECUTION]** Implement rate limiting middleware
4. **[EXECUTION]** Configure rate limit thresholds
5. **[VERIFICATION]** Validate rate limiting behavior
6. **[COMPLETION]** Documentation and evidence
```

**After** (with Context-Armed Steps):
```markdown
**Steps:**
1. **[PLANNING]** Load context and identify scope
   Context: R-015 ("Rate limiting required for all public API endpoints at 100 req/min")
2. **[PLANNING]** Check dependencies and blockers
   Context: T02.01 (API framework setup must complete first)
3. **[EXECUTION]** Implement rate limiting middleware
   Context: `src/middleware/`, R-015 rate limit requirements
   Ensuring: middleware file exists, exports `rateLimit()` function
4. **[EXECUTION]** Configure rate limit thresholds per endpoint group
   Context: R-016 ("Different limits for authenticated vs anonymous users")
   Ensuring: config matches R-016 values (100/min auth, 20/min anon)
5. **[VERIFICATION]** Validate rate limiting behavior
   Context: T02.03 acceptance criteria, `TASKLIST_ROOT/artifacts/D-0012/evidence.md`
   Ensuring: test confirms 429 response after limit exceeded
6. **[COMPLETION]** Documentation and evidence
```

### Example: DNSP Synthesis (Proposal 3) in Stage 7

**Scenario**: Validation agent B for Phase 3 times out after retry.

**Current behavior**: "Error: Validation agent B for Phase 3 failed. Validation aborted."

**Proposed behavior**:
```
Agent B (Phase 3, tasks T03.04-T03.07) failed after retry.
Synthesizing conservative finding:

  - Severity: High
  - Task ID: T03.04-T03.07
  - Problem: Validation agent failed. Tasks T03.04 through T03.07 were not
    validated against the roadmap. Manual review required.
  - Roadmap evidence: N/A (agent did not produce output)
  - Tasklist evidence: phase-3-tasklist.md, tasks T03.04-T03.07
  - Exact fix: Human reviewer must compare T03.04-T03.07 against roadmap
    items R-022 through R-025 and verify fidelity.

Proceeding with 2N-1 agent findings. Total findings: 4 (3 from agents + 1 synthesized).
```

### Example: Evidence-Anchored Validation (Proposal 4)

**Stage 6.5 output** (`generation-evidence.json`):
```json
{
  "files_generated": ["tasklist-index.md", "phase-1-tasklist.md", "phase-2-tasklist.md"],
  "task_ids_found": ["T01.01", "T01.02", "T01.03", "T02.01", "T02.02", "T02.03"],
  "deliverable_ids_found": ["D-0001", "D-0002", "D-0003", "D-0004", "D-0005"],
  "roadmap_refs_found": ["R-001", "R-002", "R-003", "R-004", "R-005", "R-006"],
  "orphan_deliverables": ["D-0005"],
  "missing_roadmap_items": ["R-007"],
  "tasks_per_phase": {"1": 3, "2": 3},
  "checkpoints_per_phase": {"1": 1, "2": 1}
}
```

**Stage 7 agent** (receiving this evidence):
```
The generation evidence shows:
- D-0005 appears in phase files but NOT in the Deliverable Registry → HIGH finding (fabricated traceability)
- R-007 appears in the roadmap but NOT in any phase file → HIGH finding (omitted requirement)

These are machine-verified facts. Flag them immediately.

Now focus inference on semantic checks for tasks T01.01-T01.02:
- Does T01.01 accurately reflect R-001? (requires reading both and comparing)
- Are T01.02's acceptance criteria as strong as R-002's success criteria?
```

The agent spends zero tokens re-checking traceability (the evidence already proved it) and focuses entirely on semantic fidelity where LLM judgment actually adds value.

# Wave-1 Verbatim Extracts (R1..R6)

> Source: 6 backlog files in `.dev/releases/backlog/v3.75-RigorflowMerger-task-unified-v3/`. Quotes verbatim; line numbers from each source file. "IC" = the SuperClaude (this repo) implementation; "LW" = Rigorflow / external comparator framework, used in the cross-framework-deep-analysis upstream.

---

## R1: comparison-sprint-executor.md — Verbatim Extracts

### Recommendations
> "Verdict class: IC STRONGER" (L76)
> "Conditions where LW patterns should be adopted into IC: - Batch-level checkpoint granularity (per-item state persistence instead of phase-level only) - UID-based item tracking within a phase's task set - Immutable batch identity (once a phase starts, task numbering is frozen — no task renaming mid-run) - Three-mode execution (normal/incomplete/correction) for mid-phase resume" (L80-84)
> "Adopt patterns, not mass: From LW: the batch immutability principle (phase task IDs frozen at start), per-item UID tracking (each task gets a stable ID for cross-session reference), the three-mode prompt selection pattern (normal/incomplete/correction), and the fail-closed verdict logic (mismatch = FAIL, not best-effort PASS). Do NOT adopt: the bash implementation, the multiple-backup versioning strategy, the Python subprocess call from bash." (L88)

### Risks
> "LW's orchestrator is 6000+ lines of bash — a language inherently unsuited to complex state management." (L64)
> "multiple backup files (automated_qa_workflow_backup_*.sh) exist in the tracked codebase, indicating iterative patching rather than principled refactoring." (L64)
> "IC's phase-level checkpointing is coarse. If Phase 3 has 15 tasks and fails on task 14, all 15 tasks must re-run on --start 3 restart." (L66)
> "IC's TurnLedger state is NOT persisted — if the supervisor crashes mid-phase, budget tracking is lost." (L66)
> "IC cannot answer 'which specific tasks in Phase 3 completed before the crash?'" (L70)

### Flag mentions
> "minimum_allocation=5 turns prevents launching underfunded subprocesses" (L24)
> "Timeout = max_turns * 120 + 300 (linear scaling)" (L46)
> "SIGINT/SIGTERM → shutdown_requested = True" (L49)
> "shadow gate mode: TrailingGateRunner daemon thread decouples metrics from blocking" (L25)

### Scoring claims
> "confidence: 0.85" (L9, L86)
> "TurnLedger enforces budget monotonicity with 80% reimbursement for PASS tasks" (L23)
> "Exponential backoff wait for worker_handoff (up to 6 attempts)" (L59)

### Capability comparisons
> "IC is superior in implementation language, testability, and extensibility. LW is superior in batch-level granularity and per-item tracking." (L72)
> "The core divide is maintenance quality vs. execution granularity." (L72)
> "IC's Python implementation is objectively more maintainable than LW's 6000-line bash script." (L78)
> "The batch state machine (initialized → worker_in_progress → worker_complete → qa_in_progress → qa_complete) with persisted state JSON is more granular than IC's phase-level checkpointing." (L29)
> "LW's batch state survives any crash because it's written to disk at every state transition." (L66)
> "The _subprocess_factory injection point is a direct testability feature LW has no equivalent of." (L68)
> "IC's shadow gate mode enables production monitoring without blocking execution — LW has no equivalent decouple mechanism." (L68)

---

## R2: comparison-task-unified-tier.md — Verbatim Extracts

### Recommendations
> "Combining IC's automatic routing with LW's universal principles would produce a stronger system than either alone." (L73)
> "Conditions where LW patterns should be adopted into IC: - Output-type-specific gate tables (IC applies uniform tier overhead; LW's content-type discrimination is more precise) - Universal quality principles as NFR baseline (IC's tier system routes to verification agents, but LW's six principles define what those agents should actually verify) - Anti-sycophancy as a universal gate principle (not just a tier-level feature) - Mandatory task completion checklist (six conditions before 'complete' status)" (L81-85)
> "Adopt patterns, not mass: From LW: the six universal quality principles (Verifiability, Completeness, Correctness, Consistency, Clarity, Anti-Sycophancy) as the IC verification agent's check framework, output-type-specific gate application (code gates for code tasks, evidence gates for analysis tasks), and the three-tier severity model (Sev 1 blocks immediately, Sev 2 fixes in cycle, Sev 3 when able). From IC: automatic tier classification with confidence scoring, compound phrase overrides, critical path filesystem override, STRICT MCP unavailability blocking (vs. graceful degradation). Do NOT adopt: LW's manual gate application without automation, the evidence table overhead for all output types at all tiers." (L89)

### Risks
> "LW's quality gates are agent-behavioral, not programmatic. The document explicitly defers automation to future work (quality_gates.md:167-185). If the QA agent does not correctly apply the gates, they provide no protection." (L65)
> "IC's classification uses keyword matching, which cannot handle semantic context... If a task description omits the security keyword, IC's classification will miss the elevation." (L67)
> "IC's output-type awareness is limited — STRICT/STANDARD/LIGHT/EXEMPT applies uniformly to all task types... IC would apply code-level verification overhead to documentation tasks that don't warrant it." (L71)

### Flag mentions
> "--skip-compliance escape hatch with <12% usage target" (L27)
> "STRICT MCP requirement: Sequential + Serena; fallback NOT allowed" (L47)

### Scoring claims
> "confidence: 0.78" (L9, L87)
> "Confidence threshold: <70% triggers user confirmation before execution begins" (L26)
> "Context boosters: >2 files +0.3 STRICT; security paths +0.4 STRICT" (L46)
> "STRICT → quality-engineer (3-5K tokens, 60s)" (L44)
> "Three-tier severity system: Sev 1 (block), Sev 2 (cycle), Sev 3 (when able)" (L35)

### Capability comparisons
> "verdict_class: IC stronger" (L8, L77)
> "Automatic classification with confidence scoring eliminates a category of user error that LW's manual gate application cannot prevent. The critical path override (filesystem-path-based safety backstop) provides semantic safety beyond keyword matching. The STRICT MCP requirement block (rather than degraded execution) is a safety decision LW has no equivalent for." (L79)

---

## R3: improve-sprint-executor.md — Verbatim Extracts

### Recommendations
> "In execute_phase_tasks(), when evaluating whether a task is 'complete,' explicitly check for affirmative evidence (gate passed + output file present and non-empty + no BLOCKED state). If any of these conditions is inconclusive, classify as FAIL, not as a soft completion." (L26)
> "Confirm that gate_passed() handles the case where the output file exists but is empty (should return (False, 'empty output file') — not (True, None))." (L27)
> "Add task_uid: str field to the task representation within a phase. UIDs are generated at phase-load time as f'{phase_id}-{task_index:04d}' (stable across session resets for the same tasklist)." (L47)
> "Implement sub-phase resume: when --start N is provided but the phase has a partial result file with per-task UIDs, re-enter at the first task with status != DONE (not at task 0). This closes the current gap where Phase 3 task 14 failure requires re-running all 15 tasks." (L48)
> "Add ExecutionMode enum: NORMAL, INCOMPLETE_RESUME, CORRECTION." (L68)
> "Add auto_diagnostic_threshold: int = 3 parameter to execute_sprint() (configurable, default 3 consecutive gate failures). When the consecutive failure count reaches the threshold, invoke run_diagnostic_chain()" (L88)
> "Add GateFailureSeverity enum: SEV1_BLOCK, SEV2_CYCLE, SEV3_ADVISORY." (L109)

### Risks
> "Risk: Low. Tightens existing behavior; edge case for empty output files that previously may have been treated as PASS." (L34)
> "Risk: Medium. New field in task representation; requires compatibility with existing result files (may need migration for result files that lack UIDs — graceful fallback to full-phase restart is acceptable)." (L55)
> "Risk: Medium. Changes prompt construction; may affect output format for resumed phases. Requires careful testing." (L75)
> "Risk: Medium. Adds a new invocation path for the diagnostic chain; requires that run_diagnostic_chain() is robust to sprint-context input." (L96)

### Flag mentions
> "Add --auto-diagnostic-threshold N CLI option (default: 3, range: 1–10). Document the option with: 'Automatically invoke diagnostic chain after N consecutive phase gate failures.'" (L89)
> "--start N with a partial result file resumes at the first non-DONE task, not at task 0" (L54)

### Scoring claims
> "LW's severity taxonomy uses a point-based scoring system (High ≥5 pts, Medium 3-4, Low ≤2) with complex FMEA integration" (L106)
> "Default to SEV1_BLOCK for STRICT-tier gates; SEV2_CYCLE for STANDARD-tier gate failures with partial output; SEV3_ADVISORY for LIGHT-tier gate failures." (L109)

### Capability comparisons
> "verdict: IC stronger" (L4)
> "LW's fail-closed logic is embedded in bash batch processing with multi-file comparison semantics; IC's sprint executor needs only to apply fail-closed semantics" (L23)
> "LW's per-item UID tracking is implemented as a bash key-value store with inter-process file locking; IC needs only a stable identifier field on each task record in the TurnLedger" (L44)

---

## R4: improve-task-unified-tier.md — Verbatim Extracts

### Recommendations
> "Add CriticalFailCondition dataclass to represent a CRITICAL FAIL trigger: condition_type: str, description: str, always_blocks: bool = True." (L26)
> "Document the CRITICAL FAIL conditions for STRICT-tier tasks: (1) Sequential or Serena MCP unavailable — unconditional FAIL (cannot degrade), (2) output file absent after max turns — unconditional FAIL, (3) classification header absent in STRICT-tier task output — unconditional FAIL." (L28)
> "add an output_type column: code (compile/test required), analysis (evidence citation required, no lint), documentation (structure check only, no code testing), opinion (CEV structure required, no automated verification)." (L48)
> "Add output-type detection rules: if all affected files are *.md → output_type=documentation; if primary deliverable is a comparison/analysis report → output_type=analysis; if primary deliverable involves code changes → output_type=code." (L50)
> "Add a 'Quality Principles NFR' section listing the six principles ... (1) Verifiability — every claim must have file:line evidence, (2) Completeness — all acceptance criteria must be addressed, (3) Correctness — implementation matches specification intent, (4) Consistency — no contradictions between components, (5) Clarity — output is unambiguous and actionable, (6) Anti-Sycophancy — findings are independent of implementer's stated confidence." (L70)
> "when classification confidence is below 0.70, the task classification is BLOCKED and requires user confirmation. The blocking message must include: the computed tier, the competing tier (highest alternative), and the specific keywords causing the split." (L89)

### Risks
> "Risk: Low. Additive to gate model; existing GateCriteria without critical_conditions list behaves identically to current behavior." (L35)
> "Risk: Medium. Changes the routing logic for documentation and analysis tasks; requires that existing STRICT-tier doc tasks are re-evaluated against the new output-type routing." (L57)
> "Risk: Low. Agent instruction addition; no code changes." (L77)

### Flag / behavior mentions
> "Sequential or Serena MCP unavailable — unconditional FAIL (cannot degrade)" (L28)
> "a STRICT-tier task that cannot reach its Sequential + Serena MCP requirements should fail (not degrade)." (L31)

### Scoring claims
> "confidence <0.70 must produce a deterministic outcome (BLOCKED, awaiting user confirmation) not a soft degradation to the computed tier." (L93)

### Capability comparisons
> "verdict: IC stronger" (L4)
> "LW's CRITICAL FAIL equivalent is applied through behavioral-only quality gate instructions without programmatic automation (explicitly rejected in D-0022 Principle 2); IC's CRITICAL condition class must be programmatically enforced, not only instructional." (L23)
> "LW's output-type gates are applied manually by human operators selecting from a quality gate menu; IC must apply output-type discrimination programmatically through the tier routing logic." (L45)

---

## R5: strategy-ic-sprint-executor.md — Verbatim Extracts

### Recommendations
> "the executor is a thin Python supervisor that manages subprocess lifecycle, output monitoring, gate evaluation, and budget accounting — while delegating all task-level reasoning to Claude subprocess instances" (L13)
> "The sprint executor decouples the orchestrator (Python supervisor) from the agent (Claude subprocess) to enable: phase-level restart (--start N), budget-tracked multi-task execution, and observable progress via TUI and logging" (L15)
> "Extracting these concerns independently would improve testability and allow alternative frontends (e.g., headless CI mode)" (L73)

### Risks
> "this is appropriate for development but must never be used in production sprint runs where downstream tasks depend on upstream gate outputs" (L46)
> "Shadow gates trade safety for observability — pipelines can proceed past failing gates, accumulating invalid artifacts" (L46)
> "The supervisor model introduces subprocess spawn overhead per phase and constrains task execution to one subprocess per phase. A single Claude subprocess handles all tasks in a phase sequentially, which means a long-running task in Phase 2 blocks all subsequent Phase 2 tasks" (L17)
> "TurnLedger state is not persisted to disk — if the supervisor is killed mid-phase, budget consumption tracking is lost and must be re-estimated on restart" (L75)
> "Phase execution order depends on the filesystem sort order of discovered phase files. Phases with the same number prefix from different naming conventions could collide in ordering; the regex captures only the first matched number group" (L85)
> "No intra-phase checkpoint. A phase with many tasks that crashes at task N requires re-running tasks 1 through N-1, consuming turn budget and time" (L77)
> "Phase discovery regex is hard-coded. Projects using non-canonical naming conventions (e.g., sprint-phase-3.md) require modifying PHASE_FILE_PATTERN" (L81)

### Flag mentions
> "--start / --end phase range — limit execution to a subset of phases without modifying the tasklist" (L62)
> "--shadow-gates — decouple gate evaluation from execution blocking" (L63)
> "--no-tmux flag — disable tmux wrapping for environments where tmux is unavailable" (L67)
> "Gate failure triggers HALT unless --shadow-gates is active" (L40)

### Scoring claims
> "Timeout is computed as max_turns * 120 + 300 seconds — a linear function of turn budget ensuring timeout scales with expected workload" (L30)
> "Ledger enforces monotonicity (consumed can only increase), tracks reimbursement at 80% rate for PASS tasks, and enforces minimum_allocation=5 turns before launching a subprocess" (L32)

### Capability comparisons
> "Sprint and roadmap share the same execute_pipeline() function and ClaudeProcess base class. Changes to the generic executor benefit both consumers" (L71)
> "Gate tiers (EXEMPT/LIGHT/STANDARD/STRICT) produce deterministic pass/fail for a given output file and criteria. Turn budget arithmetic is pure Python with no floating-point ambiguity (integer arithmetic). Monotonic clock (time.monotonic()) for deadline enforcement prevents NTP adjustment interference" (L83)
> "STRICT gates include semantic checks (pure Python lambdas)" (L40)
> "the 4-stage diagnostic chain (run_diagnostic_chain()) can be triggered: troubleshoot → adversarial analysis × 2 → summary. This is runner-side and does not consume TurnLedger turns (diagnostic invocations are not billed against task budget per spec Gap 2)" (L56)

---

## R6: strategy-ic-task-unified.md — Verbatim Extracts

### Recommendations
> "automatic tier classification with transparent confidence scoring" (L13)
> "Merging them into a single /sc:task with orthogonal --compliance and --strategy flags eliminates the decision by automating it." (L15)
> "when uncertain, escalate" (L17)
> "STRICT: activate project (Serena), verify git state, load codebase context (Auggie), make changes, identify all affected files, spawn quality-engineer sub-agent for verification, run comprehensive tests" (L46)
> "Paths matching auth/, security/, crypto/, models/, migrations/ always trigger CRITICAL verification regardless of compliance tier" (L59)

### Risks
> "Automatic classification introduces false positive risk (over-classifying a trivial change as STRICT, adding unnecessary verification overhead) and false negative risk (under-classifying a security-critical change as LIGHT, skipping required verification)." (L17)
> "The design explicitly chooses 'better false positives than false negatives'" (L17)
> "If these servers are unavailable, a STRICT task cannot proceed." (L66)
> "The escape hatch creates a potential security hole — --skip-compliance on a truly STRICT task skips all verification." (L78)
> "Changes to keyword tables or booster weights must be propagated to all copies, creating synchronization risk between source files and dev copies." (L93)
> "The keyword-scoring approach cannot handle context-dependent semantics." (L99)
> "A task with high keyword matches but actually trivial impact will receive high confidence in an elevated tier, creating over-classification that the user must manually override." (L103)

### Flag mentions
> "--compliance flag: user can force any tier regardless of auto-classification" (L82)
> "--force-strict override: escalate to STRICT without providing rationale" (L83)
> "--skip-compliance escape hatch: bypass all compliance" (L84)
> "--parallel / --delegate: enable parallel sub-agent execution for large STRICT tasks" (L85)
> "Confidence threshold (0.70): not currently user-configurable; hardcoded in the classification algorithm" (L87)

### Scoring claims
> "Score all keywords by tier weight (STRICT +0.4, EXEMPT +0.4, LIGHT +0.3, STANDARD +0.2)" (L34)
> "Apply context boosters (>2 files +0.3 STRICT; security paths +0.4 STRICT; docs paths +0.5 EXEMPT)" (L35)
> "apply with +0.15 boost" (L33)
> "If confidence < 0.70, prompt user for confirmation" (L37)
> "The skip rate target (< 12% --skip-compliance usage) reflects tolerance for false positives." (L17)

### Capability comparisons
> "STRICT → quality-engineer sub-agent (3–5K token budget, 60s timeout)" (L54)
> "STANDARD → direct test execution (300–500 tokens, 30s timeout)" (L55)
> "LIGHT → quick sanity check (~100 tokens, 10s)" (L56)
> "EXEMPT → no verification (0 tokens, 0s)" (L57)
> "Resolve conflicts: priority STRICT > EXEMPT > LIGHT > STANDARD" (L36)
> "MCP Requirements: Required: Sequential, Serena; Fallback Allowed: No" (L66)

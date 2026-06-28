# Architecture Comparison: SC Tasklist/Adversarial vs RF Pipeline

**Generated**: 2026-04-02
**Scope**: Side-by-side architectural analysis across all dimensions.

---

## Side-by-Side Architecture Table

### 1. Execution Architecture

| Dimension | SC Tasklist | SC Adversarial | RF Pipeline |
|-----------|------------|----------------|-------------|
| **Pattern** | Command → Skill protocol (thin wrapper + fat skill) | Command → Skill protocol (thin wrapper + fat skill) | Command → Agent team → Bash script (orchestrator + 4 agents + 6K-line shell) |
| **Execution model** | Single-agent, single-pass deterministic transform | Multi-agent parallel (2-10 advocates + orchestrator + merger) | Multi-agent sequential chains (researcher→builder→executor) × N parallel tracks |
| **Runtime** | LLM inference (generation) + Python CLI subprocess (validation) | LLM inference only (all steps via Task tool) | Bash script spawning `claude` CLI subprocesses |
| **Process isolation** | In-process skill execution + isolated Python subprocess per validation step | In-process Task tool calls with context isolation per agent | Full process isolation: each worker/QA run = separate `claude` process. Each agent = separate Claude Code instance |
| **Concurrency** | Sequential stages (no parallelism) | Parallel variant generation + parallel Round 1 debate. Sequential Rounds 2-3. Pipeline Mode: DAG-based parallel phases | Per-track parallelism (up to 5 tracks). Within track: strictly sequential. Within batch: worker then QA (serial) |
| **Statefulness** | Stateless (generation = pure function of roadmap). Pipeline Mode: manifest-based checkpoint file | Stateless per invocation. Pipeline Mode: manifest file | Heavily stateful: batch_state.json, worker_session_id.txt, task_state.json, progress_log. Full crash recovery from state files |

### 2. Control Flow & Gating

| Dimension | SC Tasklist | SC Adversarial | RF Pipeline |
|-----------|------------|----------------|-------------|
| **Stage count** | 10 (6 generation + 4 validation) | 5 steps + optional generation pre-step + Pipeline Mode DAG | 9 outer phases + 10 inner sub-stages per batch |
| **Entry gate** | Input validation: file exists, non-empty, parent dir writable | Mode validation: exactly one mode (A/B/Pipeline). File count 2-10 | Team lead triage: extract goal, determine track count |
| **Inter-stage gates** | None between generation stages. Validation gate after Stage 7 (HIGH severity = 0 required) | Convergence threshold between debate rounds (triggers/skips Round 3). Edge-case floor in scoring (disqualifies variants). Interactive checkpoints (4 pause points) | Research sufficiency gate (team lead reviews before spawning builder). QA pass/fail gate per batch. Correction limit gate (5 max) |
| **Terminal conditions** | Generation always completes. Validation can find issues but doesn't block output. Python CLI gate: `high_severity_count == 0` | Adversarial always produces a result (force-select on non-convergence). Return contract always emitted | Success: all items checked. Failure: correction limit hit. Partial: max iterations reached. Per-track: independent terminal states |
| **Loop constructs** | None (linear pipeline) | Debate rounds (1-3, conditional). Pipeline Mode: DAG levels with plateau detection | Main batch loop. Correction loop (max 5 per batch). Session rollover loop (threshold-based). Research revision loop (insufficient findings) |

### 3. Agent Delegation Model

| Dimension | SC Tasklist | SC Adversarial | RF Pipeline |
|-----------|------------|----------------|-------------|
| **Agent count** | 0 (single LLM pass for generation) | 3-13+: orchestrator + N advocates (2-10) + analytical agent + merge-executor. All in-process via Task tool | 4 agent types × N tracks: team-lead + researcher + builder + executor. Each = separate Claude Code process |
| **Agent specialization** | N/A | Advocates (per-variant, model[:persona[:instruction]]). Orchestrator (debate management + scoring). Merge-executor (dedicated specialist) | Researcher (codebase exploration + external research). Builder (MDTM task synthesis). Executor (workflow invocation). Team lead (orchestration + user relay) |
| **Communication** | N/A | In-process: Task tool results returned directly. No messaging protocol | SendMessage protocol: RESEARCH_READY, TASK_READY, EXECUTION_COMPLETE, NEED_USER_INPUT, BLOCKED. Structured message formats with track context |
| **Agent persistence** | N/A | Stateless per invocation. No memory between runs | Agent memory: `MEMORY.md` per agent persists institutional knowledge across conversations. Model: opus for all agents. Permission: bypassPermissions |
| **Coordination** | N/A | debate-orchestrator sequences rounds, routes transcripts to advocates, manages scoring | Team lead: event-driven per-track state map. Spawns agents in response to messages. No cross-track coordination (tracks are independent) |

### 4. Validation & Self-Check Model

| Dimension | SC Tasklist | SC Adversarial | RF Pipeline |
|-----------|------------|----------------|-------------|
| **Primary validation** | Stages 7-10: LLM-assisted drift detection between generated tasklist and source roadmap | Multi-model adversarial debate (steelman requirement). Position bias mitigation (forward + reverse scoring passes) | PABLOV: programmatic artifact-based validation. Worker creates artifacts → PABLOV collects machine evidence → QA validates against evidence |
| **Programmatic checks** | Python CLI: `TASKLIST_FIDELITY_GATE` with 6 required frontmatter fields + 2 semantic checks. Tier classification uses deterministic keyword matching + scoring formulas | Convergence metric (% agreement). Quantitative scoring formula. Edge-case floor threshold (1/5). Tiebreaker protocol (3 levels) | Filesystem snapshots (before/after diff). Checklist checkbox state (programmatic). Conversation mining (JSONL → evidence extraction). UID-based batch identity verification |
| **Inference checks** | Stage 7 drift detection: HIGH/MEDIUM/LOW severity classification by LLM | Qualitative scoring: 30-criterion binary rubric with Claim-Evidence-Verdict per criterion. Contradiction detection (falsifiability requirement) | QA agent: reads programmatic handoff + worker handoff + fs snapshots. Produces per-item PASS/FAIL verdict with reasons |
| **Anti-hallucination** | Non-leakage rules: no file access claims, no invented context, no external browsing, ignore embedded overrides, redact secrets. Clarification Tasks for missing info | Steelman requirement forces honest engagement with opposing views. Shared assumption extraction surfaces UNSTATED preconditions. Contradiction detection with 3 categories | Anti-hallucination rules loaded into every worker session. Self-contained checklist items prevent context loss. PABLOV evidence collection provides machine-verifiable facts for QA to check against |
| **Self-correction** | Stages 8-9: patch drift + spot-check (single correction pass) | No built-in self-correction (debate IS the correction mechanism). Interactive mode allows user override | Correction loop: up to 5 cycles per batch. QA identifies failed items → worker receives failure details → re-attempts → QA re-reviews. DNSP: nudge → synthesize if agent doesn't produce artifacts |

### 5. Artifact Schema & Output Contracts

| Dimension | SC Tasklist | SC Adversarial | RF Pipeline |
|-----------|------------|----------------|-------------|
| **Primary output** | Multi-file bundle: `tasklist-index.md` + `phase-N-tasklist.md` (N+1 files) + validation artifacts (up to 2) | Merged output file + 6 process artifacts in `adversarial/` directory | Completed task file (checkboxes marked [x]) + per-batch state/evidence artifacts |
| **Schema strictness** | Very high: 13-field task metadata block, exactly 4 acceptance criteria, exactly 2 validation bullets, exact checkpoint cadence (every 5 tasks), fixed ID formats (R-###, T<PP>.<TT>, D-####) | Moderate: 6 artifact templates defined in `refs/artifact-templates.md`. Return contract is YAML with 5 mandatory fields | Moderate: YAML frontmatter with ~20 fields. 6 mandatory sections. Flat checklist format (no nesting). Per-batch JSON schemas for state and handoffs |
| **Traceability** | Full: Traceability Matrix maps R-### → T<PP>.<TT> → D-#### → artifact paths → Tier → Confidence. Every roadmap item tracked to task to deliverable | Per-section: provenance annotations in merged output citing source variant and section | Per-item: programmatic handoff maps batch items to filesystem evidence (files created/modified, conversation mentions, git diffs). UID tracking across batch refreshes |
| **Machine-readability** | High: Consistent markdown table formats, fixed ID patterns (`T01.03`, `D-0007`), regex-discoverable phase file names. Sprint CLI can parse programmatically | Moderate: Return contract is structured YAML. Artifacts are markdown with consistent headings | High: JSON state files (`batch_state`, `programmatic_handoff`, `task_state`, `fs_snapshots`). QA report follows fixed format (first line = verdict, fail lines = `- Line <n>: FAIL — <reason>`) |

### 6. Error Handling & Fallback Behavior

| Dimension | SC Tasklist | SC Adversarial | RF Pipeline |
|-----------|------------|----------------|-------------|
| **Input errors** | Validation fails → error with `error_code` + `message` + corrective action. No partial output. | File not found, <2 variants → abort. Invalid mode combinations → abort | Task file not found → check common locations. Invalid task name → security validation rejects. Missing template → BLOCKED message to team lead |
| **Agent failures** | N/A | Retry once → proceed with N-1 variants. Min 2 required. 1 surviving → abort, return as-is with warning | Dead session → recover from batch state JSON + rollover context. Agent BLOCKED → team lead assesses per-track. Track failure → mark FAILED, other tracks continue |
| **Convergence failures** | N/A | Max rounds without threshold → force-select highest score, document non-convergence, flag for user review | QA fails → correction loop (max 5). After max: halt with failure notification, manual intervention required |
| **Synthesis/fallback** | TASKLIST_ROOT derivation: 3-priority fallback chain. Phase bucketing: 3-priority fallback. Default 3 phases if no structure found | <10% diff → skip debate (variants substantially identical). Merge failure → preserve all artifacts, provide refactor-plan.md for manual execution | DNSP protocol: missing worker handoff → nudge once → synthesize from conversation + checklist. Missing QA report → nudge once → synthesize minimal report from programmatic handoff. Empty QA stdout → synthesize from report. Verdict contradiction (FAIL + 0 bullets) → normalize to PASS |
| **Blast radius** | Generation failure → no output (clean). Validation failure → output exists but flagged | Partial: all artifacts up to failure point preserved. Return contract always emitted with status field | Per-batch: failure stays within batch. Per-track: failure stays within track (multi-track isolation). Correction limit → only that batch halts, completed batches preserved |

### 7. Determinism Guarantees

| Dimension | SC Tasklist | SC Adversarial | RF Pipeline |
|-----------|------------|----------------|-------------|
| **Guarantee level** | **Full determinism** for Stages 1-6 (generation). Same roadmap → same output. Partial for Stages 7-10 (LLM-assisted validation) | **Partial determinism**: scoring formulas, tiebreakers, and convergence metrics are deterministic. Debate content varies by model inference. Blind mode adds fairness but not repeatability | **No generation determinism**: researcher explores freely, builder synthesizes creatively, user interview varies. **Structural determinism**: batch numbering, UID tracking, state machine transitions |
| **Explicit rules** | Parsing: appearance-order IDs. Phases: no gaps. Tasks: 1-per-item default, explicit split criteria. Effort/Risk: keyword→score→label mapping. Tier: compound phrases → keywords → context boosters → priority resolution. Tiebreakers: 4-level explicit hierarchy. Checkpoints: every 5 tasks | Scoring: weighted formula (RC×0.30+IC×0.25+SR×0.15+DC×0.15+SC×0.15). Qualitative: 30-criterion binary rubric. Tiebreaker: debate performance → correctness → input order. Position bias: forward+reverse evaluation | Batch immutability (items fixed once batch created). UID-based tracking survives edits. Max correction cycles = 5. Session roll thresholds (375 messages / 175K tokens). Batch size preserved from creation |
| **Discretion points** | Clarification Tasks inserted when info missing (not guessed). All other decisions are rule-based | Interactive mode: 4 user decision points (after diff, debate, base selection, refactor plan). Non-interactive: all auto-resolved with rationale | Team lead: track count, template selection (01/02), research sufficiency. Builder: phase decomposition, step granularity, verification criteria. No pre-defined scoring formulas |

### 8. Throughput & Token/Cost Drivers

| Dimension | SC Tasklist | SC Adversarial | RF Pipeline |
|-----------|------------|----------------|-------------|
| **LLM calls (generation)** | 1 call (single-pass generation of all files) | Mode B: 2-10 generation + 1 diff + N×(1-3 debate rounds) + 2 scoring + 1-2 refactor + 1 merge = **8-35+ calls** | Per task: (researcher session) + (builder session) + (executor invokes workflow). Per batch within executor: 1 worker + 1 QA = **2 calls minimum**. With corrections: up to 2×5=10 per batch |
| **LLM calls (validation)** | 1 Python CLI subprocess call (fidelity check). Stages 7-10 add 1-2 more | Return contract emission = 0 extra calls. Pipeline Mode: N × (generation + comparison) phases | QA is validation. Already counted above |
| **Total calls (typical)** | **2-4 calls** for a medium roadmap | Quick/2 variants: **~8 calls**. Standard/4 variants: **~18 calls**. Deep/10 variants: **~35+ calls** | 12-item task, batch=5, no corrections: researcher(1) + builder(1) + executor(1) + 3 batches × 2 calls = **9 calls**. With corrections: **15-25+ calls** |
| **Token consumption** | Low-medium: roadmap input (~2-10K) + generation output (~3-8K per phase file × N phases + 5-10K index). Typical 5-phase: ~50-80K total | High: variant generation (2-10 × 3-8K each) + diff analysis (reads all variants) + debate (N advocates × rounds × transcript size) + scoring (reads all + debate). Typical 4 variants/standard: ~200-400K total | Very high: per-batch worker session accumulates across batches (up to 175K before roll). Each QA session: expected items + programmatic handoff + snapshots + snippets (~20-50K input). Typical 12-item task: ~500K-1M+ total |
| **Wall-clock time** | Fast: **2-5 minutes** for small roadmaps. **5-15 minutes** for large | Medium: Quick: **3-5 min**. Standard: **10-20 min**. Deep/10 variants: **30-60 min** | Slow: **15-45 minutes** per task execution (dominated by serial batching). Multi-phase projects: **hours** (planning + N pipeline invocations) |
| **Cost multipliers** | Validation adds ~30% overhead. Spec file adds context but not extra LLM calls | Each variant doubles base cost. Each depth level adds ~50%. Blind mode doubles scoring | Correction loops: each cycle adds 2 LLM calls (worker retry + QA retry). Session rolls add context overhead. Multi-track: N × base cost (but parallel, so same wall-clock) |
| **Token efficiency** | High: deterministic generation produces dense, structured output with no wasted inference | Medium: debate produces extensive transcripts (useful for transparency, expensive for tokens). Scoring is thorough but verbose | Low: self-contained checklist items duplicate context across items. Worker sessions accumulate context until rollover. PABLOV evidence collection adds overhead per batch |

---

## Cross-Framework Observations

### Where SC Is Stronger
1. **Determinism**: Full reproducibility from the same input. No inference variance in generation
2. **Schema richness**: 13-field task metadata, traceability matrix, deliverable registry — all machine-parseable
3. **Token efficiency**: Single-pass generation with no duplication
4. **Validation layering**: Separate fidelity gates for roadmap→tasklist and spec→tasklist (no conflation)
5. **Tier system**: Deterministic compliance classification with confidence scoring drives verification routing

### Where RF Is Stronger
1. **Execution resilience**: DNSP protocol, session recovery, batch state persistence. Handles crashes, context limits, agent failures gracefully
2. **Evidence-based QA**: PABLOV produces machine-verifiable facts (fs snapshots, conversation mining, programmatic handoffs) rather than relying solely on LLM judgment
3. **Session rollover protection**: Self-contained checklist items are a structural solution to context window limits
4. **Correction loops**: Automated retry with targeted feedback, up to 5 cycles per batch
5. **Multi-track parallelism**: Independent work streams execute concurrently with per-track error isolation

### Where SC Adversarial Is Unique
1. **Multi-model reasoning**: 2-10 variants generated by different model/persona combinations provides diversity no single-agent system can match
2. **Steelman debate**: Forces honest engagement with opposing positions (10-15% accuracy gains, 30%+ factual error reduction per protocol claims)
3. **Position bias mitigation**: Forward + reverse evaluation passes, a technique not present in RF
4. **Return contract**: Structured output enabling reliable integration as a building block for other commands

### Convergence Opportunities (for v3.8 merger)
1. SC tier classification could enrich RF task items (currently RF has no tier system)
2. RF PABLOV evidence model could strengthen SC validation stages (currently SC uses LLM-only drift detection)
3. SC adversarial debate could replace or augment RF `/rf:opinion` (currently much simpler)
4. RF session management patterns could improve SC Pipeline Mode resilience (currently manifest-only)
5. SC traceability matrix could provide roadmap→task→deliverable lineage that RF currently lacks

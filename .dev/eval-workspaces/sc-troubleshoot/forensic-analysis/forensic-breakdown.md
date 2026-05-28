# /sc:forensic — Comprehensive Design Breakdown

> Source: 4-way fan-out analysis of `.dev/releases/backlog/v5.xxforensic/` (12k lines across 29 files).
> Compiled: 2026-05-21.

## 1. Executive Summary

`/sc:forensic` is a generic forensic QA & debug pipeline for any codebase or feature release — it auto-discovers investigation domains, runs parallel model-tiered root-cause analysis, delegates hypothesis and fix validation to the existing `sc:adversarial` debate protocol, delegates implementation to specialist agents, and produces an evidence-backed report (`forensic-spec.md:48-51`).

The strategic shape is **orchestrator-as-dispatcher**: an Opus orchestrator capped at ≤8,000 tokens across the whole pipeline NEVER reads source code; it only consumes structured JSON summaries and Markdown selection files. Source-reading is delegated to Haiku (recon, lint) and Sonnet (deep investigation, fix proposals, implementation). The design layers two orthogonal axes: `--tier light|standard|deep` controls *pipeline scope* (which phases execute, agent count), independent of `--depth quick|standard|deep` controlling *adversarial debate depth only* (`forensic-spec.md:108-110`, `:199-202`).

Primary audience: invoked manually for QA / debug / regression hunts on any codebase, AND auto-invoked by `sc:task-unified` on TFEP (Test Failure Escalation Protocol) escalation in light tier (~5-8K tokens) to keep failing-test recovery cheap (`forensic-spec.md:1849-1854`; TRC:382).

## 2. Purpose & Scope

**Purpose** (`forensic-spec.md:48-51`): generic forensic QA & debug pipeline; auto-discovers domains; parallel model-tiered RCA; adversarial validation; evidence-backed report.

**In scope** (`forensic-spec.md:54-66`):
- Automated codebase reconnaissance + domain discovery
- Parallel root-cause investigation with structured hypothesis output
- Adversarial hypothesis validation via `sc:adversarial-protocol`
- Fix proposal generation with tiered aggressiveness (`minimal | moderate | robust`)
- Adversarial fix validation
- Delegated implementation via specialist agents
- Delegated validation (lint, test, self-review)
- Checkpoint/resume
- Quick/triage mode for `sc:task-unified` TFEP integration
- Caller-provided context interface bypassing Phase 0
- Tiered operating modes (`light | standard | deep`) orthogonal to debate depth

**Out of scope** (`forensic-spec.md:68-72`): production deployment, git operations, domain-specific correctness validation beyond lint/test, UI/visual testing (no Playwright).

**Activation**: command file invokes the `sc:forensic-protocol` skill as MANDATORY pre-execution step (`forensic-spec.md:397-404`). Auto-invoked by `task-unified` on TFEP escalation (`forensic-spec.md:1849-1854`); escalation gradient at `forensic-spec.md:1990-1993`.

**Origin / weaknesses being mitigated** (10 W-rows in `forensic-spec.md:76-89`, mirrored at `forensic-explore.md:90-129`): hardcoded codebase (W-1), orchestrator reads everything ~50-80K (W-2), no model tiering (W-3), ad-hoc debates (W-4), MCP underutilized (W-5), no recon phase (W-6), sequential debate bottleneck (W-7), no checkpoint/resume (W-8), fixed 10 agents (W-9), orchestrator implements directly (W-10).

## 3. Strategic Choices (the WHY)

Six design principles (`forensic-spec.md:231-237`; mirrored at `forensic-explore.md:136-147`):

1. **Generic-first** — domains auto-discovered, never hardcoded (`forensic-spec.md:231`).
2. **Orchestrator-as-dispatcher** — Opus orchestrator NEVER reads source code; only structured JSON summaries and Markdown selection files. Total orchestrator budget capped at ≤8,000 tokens across the pipeline (`forensic-spec.md:215-216` NFR-001, `:309-322`).
3. **Model tiering** — Haiku for surface scans, Sonnet for deep analysis, Opus reserved for synthesis and coordination only (`forensic-spec.md:233`, decision matrix at `:1509-1527`).
4. **Leverage existing infrastructure** — delegates to `/sc:adversarial`, borrows `sc:cleanup-audit-protocol` batch-checkpoint pattern, borrows `/sc:spawn` Epic→Story→Task decomposition (`forensic-spec.md:234`, `:1811-1855`).
5. **Checkpoint-resumable** — every phase writes artifacts; any phase restartable via `progress.json` (`forensic-spec.md:235`, schema `:1448-1503`, resume logic `:1659-1682`).
6. **MCP-aware** — explicit MCP routing table assigns each server to the phases where its capabilities are most valuable (`forensic-spec.md:236`, routing table `:1552-1573`).

**Strategic refinement — orthogonal-axes design**: `--tier` controls pipeline scope (which phases execute, agent count) and is independent of `--depth` which controls adversarial debate depth only (`forensic-spec.md:108-110`, `:199-202` FR-038 + FR-056, phase behavior matrix at `:276-307`).

**Token-efficiency targets** (`forensic-spec.md:1876-1888`, §16.1):
- Orchestrator: ~50-80K → ~5-8K (~90% reduction)
- Phase 2 debate: ~15K → ~8K (~47% reduction)
- Phase 3b debate: ~10K → ~5K (~50% reduction)
- Light tier total: ~5-8K vs Standard ~50-60K (`forensic-spec.md:1889-1903`).

**Refactoring story driving the strategy** (TRC:13-77, FRH:30-46, FRH:241-269):
- Pain point 1 — `sc:task-unified` agents patched test failures with zero RCA (transcript example: 10 tests fail `KeyError: None`, agent edits tests instead of investigating — "huge risk" FRH:43).
- Pain point 2 — pre-refactor forensic spec was 7-phase generic pipeline at 50-80K, overkill for one tasklist's failing tests; ~5-8K needed for task-unified integration.
- Pain point 3 — naming/flag collision between `--mode` (intent) and `--depth` (debate); resolved by splitting into `--intent`, `--tier`, `--debate-depth` (FRH:285-296, FRH:446-454, FRH:462-470).

**Bake-vs-delegate decision** (TRC:42-77): Option A (bake into task-unified) scored 4.62/10; Option B (refactor forensic + task-unified calls it) scored 7.85/10. Deciding argument: 1:1 mapping between TFEP steps and forensic phases (TRC:65-77) — "Baking it into task-unified means writing a second, less-capable version of the same pipeline."

**Merge-winner pattern (adversarial Run 2)**: Variant A (architectural skeleton, 3-axis flag model) won as merge base via the **edge-case floor rule** even though combined score was nearly tied with Variant B (A=0.730 vs B=0.720). B was disqualified for scoring 0/5 on Invariant & Edge Case Coverage (`base-selection.md:91-95`).

## 4. Architecture (the WHAT)

Two distinct layers (TRC:382, SRTH:3):

1. **Protocol/skill layer** — refactor of `/sc:forensic` and `/sc:task-unified` skills.
2. **CLI/runner layer** — new `sprint/tfep.py` module orchestrating Claude subprocesses.

**Four concrete component types** (TRC:42-77, TRC:138-145, TAD:36-44, SRTH:38-51):

1. **Slash commands as wrappers** — `/sc:forensic`, `/sc:task-unified`, `/sc:troubleshoot`, `/sc:brainstorm`, `/sc:adversarial` are existing commands; TFEP coordinates them rather than replacing them (chose Artifact B 7.85 vs A 4.62).
2. **Skill (protocol) layer** — `src/superclaude/skills/sc-task-unified-protocol/SKILL.md` gets a ~50-100 line addition: *prohibition* + *trigger detection* + *forensic invocation* + *escalation gradient* + *resume* + *report*.
3. **CLI orchestration layer (new module)** — `src/superclaude/cli/sprint/tfep.py` contains `ForensicOrchestrator`, `EscalationState`, `perform_rollback`, `inject_remediation_tasks`, `write_incident_report` (TAD:36-44; SRTH:344-346). ~450 new lines (TAD:1391).
4. **Subprocess agents** — Each "agent" in the forensic pipeline is a separate `claude --print` subprocess spawned by the runner, not an in-session skill invocation (SRTH:38-51; TAD:447-486 `ForensicProcess` extends `pipeline/process.py` `ClaudeProcess`).

**Split-ownership rule (FRH:23-25)**: "`task-unified` should own **when** forensic analysis is required; `/sc:forensic` should own **how** forensic analysis is performed." Sprint runner adds a third: "runner-orchestrated parallel forensic subprocesses, NOT in-session skill invocation" (SRTH:40-51).

**Module map** (TAD:36-44):

```
src/superclaude/cli/sprint/
├── tfep.py        ← NEW: ForensicOrchestrator, rollback, injection, prompts, incident reports
├── executor.py    ← MODIFIED: phase loop TFEP branch, git baseline capture
├── process.py     ← MODIFIED: ForensicProcess subclass, resume prompt builder
├── monitor.py     ← MODIFIED: TFEP marker detection patterns
├── models.py      ← MODIFIED: PhaseStatus enum, MonitorState fields, SprintConfig fields
├── commands.py    ← MODIFIED: --tfep-* Click options
└── diagnostics.py ← MODIFIED: FailureCategory.TFEP
```

**Dependency direction strictly downward** (TAD:46-62): `commands.py → executor.py → tfep.py → process.py → monitor.py → models.py`. `tfep.py` imports only from `models.py`, `pipeline/process.py`, `monitor.py`, stdlib (TAD:64-68); deliberately not from `executor.py`, `commands.py`, `diagnostics.py` (TAD:70-74).

**Two-tier escalation**: light tier (4-step, 6 invocations, ~5-8K tokens) → standard tier (2-step, 3 invocations) → hard halt (TAD:344-395, TRC:99-100, SRTH:185-195). State per-phase, in-memory only — resets on sprint resume (SRTH:244).

**Selective git rollback** (TAD:644-701, FR-TFEP-10 at SRTH:289-311): `git diff --name-only {baseline}` identifies phase-changed files; save full patch regardless of scope; intersect causal files (from `rca-verdict.md`) with phase-changed files; full revert if all changed files are causal, selective `git checkout` if some. Never reverts work from prior phases (SRTH:303-306).

## 5. Pipeline / Phase Structure

**Eight-phase pipeline** (`forensic-spec.md:240-274`). Data flow: Phase 0 → `investigation-domains.json` → Phase 1 → `findings-domain-{N}.md` → Phase 2 → `base-selection.md` → Phase 3 → `fix-proposal-H-{N}.md` → Phase 3b → `fix-selection.md` → Phase 4 → manifests → Phase 5 → reports → Phase 6 → `final-report.md`.

### Phase 0 — Reconnaissance (`forensic-spec.md:488-575`)

- **Inputs**: codebase root, `--focus` hints
- **Agents**: 3 parallel Haiku — 0a structural inventory (Glob/Read), 0b dependency graph (Serena `find_referencing_symbols`), 0c risk-surface scan (error handling, subprocess, signals, env-dependent paths, untested branches, concurrency)
- **Outputs**: `structural-inventory.json`, `dependency-graph.json`, `risk-surface.json`, `investigation-domains.json` (3-10 domains, risk-scored, suggested model tier: Haiku <0.7, Sonnet ≥0.7)
- **Parallelism**: 3-way parallel
- **Orchestrator budget**: 500 tokens (`forensic-spec.md:2308-2320`)

### Phase 1 — Root-Cause Discovery (`forensic-spec.md:577-626`)

- **Inputs**: `investigation-domains.json`
- **Agents**: one per domain (N), bounded by `--concurrency`
- **Outputs**: `findings-domain-{N}.md` per Hypothesis Finding Schema (id, summary, evidence as `file:line` excerpts, confidence 0-1, falsification criterion, severity, category)
- **Parallelism**: N-way fan-out
- **Orchestrator budget**: 1000 tokens

### Phase 2 — Hypothesis Debate (`forensic-spec.md:628-666`)

- **Inputs**: `findings-domain-*.md`
- **Mechanism**: fully delegates to `/sc:adversarial --compare findings-domain-*.md --depth deep --convergence {threshold} --focus "evidence-quality,reproducibility,severity"`
- **Outputs**: `phase-2/adversarial/diff-analysis.md`, `debate-transcript.md`, `base-selection.md`, `refactor-plan.md`, `merge-log.md`
- **Orchestrator budget**: 500 tokens

### Phase 3 — Fix Proposals (`forensic-spec.md:668-716`)

- **Inputs**: surviving hypothesis clusters from Phase 2
- **Agents**: M Sonnet agents (one per surviving hypothesis); three tiers per proposal (minimal/moderate/robust) with changes list, risk text, side-effects, confidence, `test_requirements` (unit/integration/e2e)
- **Outputs**: `fix-proposal-H-{N}.md`
- **MCP**: Serena `find_referencing_symbols`, Context7 idiomatic patterns
- **Orchestrator budget**: 0 tokens

### Phase 3b — Fix Debate (`forensic-spec.md:718-751`)

- **Inputs**: `fix-proposal-H-*.md`
- **Mechanism**: `/sc:adversarial --compare fix-proposal-H-*.md --depth standard --focus "correctness,risk,side-effects"`
- **Outputs**: `phase-3b/fix-selection.md` — the **primary orchestrator decision point**
- **Orchestrator budget**: 800 tokens

### Phase 4 — Implementation (`forensic-spec.md:753-802`)

- **Agents**: 4a specialist (python-expert / backend-architect / frontend-architect selected by file-extension dominance — `forensic-spec.md:895-905`) using Serena `replace_symbol_body`; 4b quality-engineer creating regression tests with Context7
- **Outputs**: `changes-manifest.json`, `new-tests-manifest.json`
- **Parallelism**: 2-way; worktree isolation recommended (sequential fallback at concurrency=1)
- **Orchestrator budget**: 0 tokens

### Phase 5 — Validation (`forensic-spec.md:804-849`)

- **Agents**: 5a Haiku lint, 5b Sonnet quality-engineer (test execution + failure correlation), 5c Sonnet self-review (4 mandatory self-check questions vs original hypotheses)
- **Outputs**: `lint-results.txt`, `test-results.md`, `self-review.md`
- **Parallelism**: 3-way
- **Orchestrator budget**: 0 tokens

### Phase 6 — Final Report (`forensic-spec.md:851-870`)

- **Agent**: Opus orchestrator synthesizes from summary artifacts only (~2,000 tokens)
- **Outputs**: `final-report.md` — Ranked Root Causes, Rejected Hypotheses, Chosen Fixes, Files Changed, Test/Lint Results, Residual Risks + Follow-ups, Domain Coverage Map
- **Orchestrator budget**: 2000 tokens

**Light-tier path** (TFEP triage) (`forensic-spec.md:276-308`, `:1616-1649`, `:1919-2042`): Phase 0 SKIP (caller provides `--context <file>` YAML); Phase 1 fixed at 2 Sonnet `/sc:troubleshoot` agents (diagnosis only); Phase 2 `--depth quick`; Phase 3 fixed at 2 Sonnet `/sc:brainstorm` agents (proposal only); Phase 3b `--depth quick`; Phases 4 and 5 SKIP; Phase 6 produces abbreviated `tfep-report.md` + `tasklist-insertion.md` for `sc:task-unified --compliance strict`.

**Gate criteria**: each phase's artifacts must be schema-conformant for the next to proceed; Phase 2 zero-hypotheses path → terminal report (`dependency-graph.md:158`); Phase 3b `fix-selection.md` is the PRIMARY DECISION POINT (`dependency-graph.md:182-183`); Phase 4 produces `baseline-test-results.md` BEFORE any fix applied (`dependency-graph.md:192-193`); Phase 6 reads only 6 summary artifacts (no raw source) (`dependency-graph.md:226-232`).

## 6. Techniques (the HOW)

**Domain auto-discovery algorithm** (`forensic-spec.md:556-575`, panel resolution at `:2062-2065`): clustering by natural risk signals; each distinct risk category with ≥1 file generates a candidate domain; domains merged when file overlap >50%; `--focus` hints become forced domains with `risk_score: 0.5` if no auto-match (FR-047).

**Hypothesis confidence scoring**:
- Evidence-backed scores 0.0-1.0 per finding (`forensic-spec.md:1335-1338`).
- Calibration normalization happens inside adversarial debate via 25-criterion rubric — pre-debate scores agent-subjective, post-debate rubric-normalized (`forensic-spec.md:2174-2175`).
- Default filter threshold 0.7; configurable via `--confidence-threshold 0.0-1.0` (`forensic-spec.md:205-206` FR-041).

**Hypothesis ID scheme**: `H-{domain_index}-{sequence}`, regex `^H-\d+-\d+$` (`forensic-spec.md:1320-1323`). `{domain_index}` is 1-based position in `investigation-domains.json` (`forensic-spec.md:2174`). P-009 (proposal-verdicts.md:159-176) accepted replacement with stable `domain_id` hash for resume safety.

**Fix-tier rubric**: exactly three tiers per proposal — `minimal` (smallest safe change), `moderate` (balanced), `robust` (comprehensive redesign) (`forensic-spec.md:99`, `:1361-1399`). `--fix-tier` selects default aggressiveness.

**Adversarial integration pattern**: forensic delegates to the existing 5-step protocol (diff → debate round 1 parallel → debate round 2 sequential → 25-criterion rubric → ranked selection), consuming `debate-transcript.md` + `base-selection.md` with no modifications to the adversarial protocol (`forensic-spec.md:1813-1826`).

**Model-tier decision matrix** (`forensic-spec.md:1509-1527`):
- Haiku: Phase 0 (all 3 recon agents), Phase 1 low-risk domains (risk <0.7), Phase 5a lint.
- Sonnet: Phase 1 high-risk (≥0.7), Phase 2/3b advocates, Phase 3 fix proposals, Phase 4 implementation/tests, Phase 5b/5c.
- Opus: Phase 0 domain synthesis, Phase 2/3b debate-orchestrator, Phase 6 final report.
- Light tier: simplified — all 4 agents Sonnet, no Haiku/Opus (`forensic-spec.md:1529-1540`).

**Checkpoint-batch pattern**: every phase writes artifacts; any phase restartable via `progress.json` (`forensic-spec.md:1448-1503`, `:1659-1682`). Borrows from `sc:cleanup-audit-protocol`.

**Evidence-validation**: 100% hypothesis evidence coverage required; 100% falsifiability (`forensic-spec.md:1906-1915`). Every hypothesis has `file:line` excerpts.

**Specialist-agent selection signals** (`forensic-spec.md:897-905`): `.py` dominance → `python-expert`; backend/API/infrastructure → `backend-architect`; `.jsx/.tsx/.vue` → `frontend-architect`; mixed → `python-expert` default.

**Self-review 4-question checklist** (`forensic-spec.md:843-847`): (1) Tests/validation executed? (2) Edge cases covered? (3) Requirements matched (tie back to hypothesis)? (4) Follow-up or rollback steps needed?

**Worktree isolation**: Phase 4 SHOULD use git worktrees for parallelism; sequential fallback (concurrency=1) when worktrees unavailable (`forensic-spec.md:222-223` NFR-008, `:2079-2080`).

**Per-agent token bounds** (`forensic-spec.md:2127`): Phase 1 Sonnet 2-3K, Haiku 1-2K; total Phase 1 = N × avg.

**Per-MCP-server concurrency cap** (`forensic-spec.md:2127`, NFR-010): ≤3 simultaneous requests per server regardless of `--concurrency`.

**Agent prompt prefix conventions** (`forensic-spec.md:2003-2026`): Light-tier Phase 1 prompts MUST begin with `/sc:troubleshoot`; light-tier Phase 3 prompts MUST begin with `/sc:brainstorm`.

**Return contract** (`forensic-spec.md:1953-1984`): YAML structure with `status` (`success|partial|failed`), `root_cause_path`, `solution_plan_path`, `tasklist_insertion_path`, `recommended_resume_mode`, `recommended_escalation`, `requires_user_review`, `test_is_wrong` (critical flag — when debate concludes test expectations outdated rather than code wrong, caller MUST present to user). Write-on-failure required.

**Pre-flight validation** (`forensic-spec.md:2247-2248` FR-054): output dir writable, target paths exist, tools available; MCP availability checked lazily at first use.

**Stale-codebase detection** (`forensic-spec.md:2246-2247` FR-053): compare `git rev-parse HEAD` (or mtime fallback) on resume.

**Secret redaction in final report excerpts** (`forensic-spec.md:2095-2096` FR-049): redact common secret patterns to `[REDACTED]`. P-020 widens this to all artifacts via pipeline-level post-processing.

**Subprocess parallelism** (TAD:525-532): `concurrent.futures.ThreadPoolExecutor(max_workers=len(names))`. Each agent gets independent context window — separate subprocess (SRTH:46-50).

## 7. Agent Inventory

The TFEP design does **not** propose any new custom agents in `src/superclaude/agents/`. All "agents" are slash-command-prefixed Claude subprocesses spawned by the orchestrator (TAD:344-395, 463-485, 542-575; TRC:206-242):

| Name | Role | Prompt prefix | Model | Max turns | Timeout |
|---|---|---|---|---|---|
| RCA alpha | Root-cause hypothesis | `/sc:troubleshoot` | Sonnet (default) | 50 | 300s |
| RCA bravo | Root-cause hypothesis | `/sc:troubleshoot` | Sonnet (default) | 50 | 300s |
| RCA judge | Adversarial adjudication | `/sc:adversarial --compare ... --depth quick` | Sonnet | 50 | 300s |
| Solution alpha | Fix proposal | `/sc:brainstorm` | Sonnet | 50 | 300s |
| Solution bravo | Fix proposal | `/sc:brainstorm` | Sonnet | 50 | 300s |
| Solution judge | Adversarial adjudication | `/sc:adversarial` | Sonnet | 50 | 300s |
| Re-launched phase | Remediation execution | `/sc:task-unified --compliance strict` | config.model | max_turns × multiplier | extended +600s |

Sonnet is the default per FR-TFEP-03 (SRTH:172-176); TAD:1185 (`tfep_model: str = ""` empty means Sonnet). Light mode fixes agent count at 2 regardless of complexity; configurable via `--tfep-agents` flag with range 2-4 (SRTH:198-199, TAD:1213).

For the **full-pipeline forensic** (non-TFEP), agents are spawned per the model-tier decision matrix above (Phase 0: 3 Haiku; Phase 1: N Haiku/Sonnet per risk score; Phase 3: M Sonnet; Phase 4: 1 specialist Sonnet + 1 quality-engineer Sonnet; Phase 5: 1 Haiku + 2 Sonnet; Phase 6: Opus orchestrator).

**Boundary preservation** (FRH:521-538): `/sc:troubleshoot` used in diagnosis-only mode (no `--fix` flag — TAD:1271). `/sc:brainstorm` is requirements/proposal-only (does not implement). `/sc:adversarial` is the adjudication mechanism. Boundaries inherited rather than reinvented.

## 8. MCP Integration

**MCP routing table** (`forensic-spec.md:1552-1573`):
- Serena: Phase 0 `get_symbols_overview`, Phase 1 `find_referencing_symbols`/`find_symbol`, Phase 4 `replace_symbol_body`.
- Context7: Phase 0 framework detection (`resolve-library-id`, `get-library-docs`), Phase 1 framework patterns, Phase 4 test framework patterns.
- Sequential: `sequentialthinking` in Phases 1, 2, 3.

**MCP fallback / circuit-breaker** (`forensic-spec.md:1568-1572`, `:1786-1799`):
- Serena OPEN ⇒ Edit/MultiEdit (loses symbol precision).
- Sequential OPEN ⇒ auto-downgrade adversarial to `--depth quick`.
- Context7 OPEN ⇒ WebSearch.

**Graceful degradation levels** (`forensic-spec.md:1800-1807`): Full → Reduced precision (Serena down) → Reduced depth (Sequential down) → Minimal (all MCP down, `--depth quick` enforced).

**Per-server concurrency cap** (NFR-010, `forensic-spec.md:2127`): ≤3 simultaneous requests per MCP server regardless of `--concurrency`.

**Prompt-based MCP access budgets per agent type** (replaces rejected P-022 MCP scheduler): Phase 1 investigation: 3 Serena calls + 1 Context7 call per domain; Phase 4a: 5 Serena + 2 Context7 per fix. `--concurrency` default reduced from 10 → 5 (proposal-verdicts.md:446-481).

**TFEP-level MCP** (gap noted in section-B): MCP usage at TFEP layer is **inherited from the underlying slash commands**, not specified per-phase by TFEP itself. The judge format `/sc:adversarial --compare {file_list} --depth quick` (TAD:550) inherits whatever MCP wiring `/sc:adversarial` already has. RCA agents inherit `/sc:troubleshoot` wiring; Solution agents inherit `/sc:brainstorm` wiring. Adversarial judge always pinned `--depth quick` regardless of TFEP tier (SRTH:199, 383). No explicit per-phase routing for auggie/serena/context7/tavily/sequential at the TFEP layer (TRC:88-97 mentions model tiers, not MCP servers).

## 9. Two-Axis Mode Model

Two orthogonal axes (`forensic-spec.md:108-110`, `:199-202` FR-038 + FR-056, behavior matrix `:276-307`):

- **`--tier light|standard|deep`** — pipeline scope: which phases execute and how many agents.
- **`--depth quick|standard|deep`** — adversarial debate depth only.

These are independent: e.g., `--tier light --depth deep` (rare) or `--tier standard --depth quick` are both valid.

**TFEP triage mode** (`forensic-spec.md:1919-2042`):
- Targeted at ~5-8K tokens total (light tier total `:1889-1903`).
- Caller-aware defaults: `--caller task-unified` ⇒ `--tier light --intent triage --depth quick`. Otherwise `--tier standard --intent auto --depth standard` (`forensic-spec.md:304-307`).
- Phase 0 SKIP (caller provides `--context <file>` YAML); Phases 4, 5 SKIP (caller handles re-test); Phase 6 produces `tfep-report.md` + `tasklist-insertion.md`.

**Escalation gradient** (`forensic-spec.md:1986-1998`): 1st TFEP trigger → light tier (~5-8K); 2nd trigger → standard tier (~15-20K); 3rd trigger → FULL STOP, report to user. "Same failure" tracked via `escalation_count` in failure-context schema (`forensic-spec.md:1283-1288`).

## 10. CLI / Sprint-Runner Integration

**Critical constraint — no IPC** (SRTH:23-24, NFR-TFEP-01 at SRTH:316-322): the sprint runner uses `claude --print --verbose -p <prompt>` (batch, not interactive). Runner cannot send data to a live Claude subprocess. Pattern always: "Claude exits → runner orchestrates → runner re-launches Claude." Claude's work preserved on disk; re-launched subprocess picks up via resume prompt + git diff context.

**New module — `sprint/tfep.py`** (~450 lines, TAD:1391): contains `ForensicOrchestrator`, `EscalationState`, `perform_rollback`, `inject_remediation_tasks`, `write_incident_report` (TAD:36-44; SRTH:344-346).

**Detection mechanism** (SRTH:122-138 FR-TFEP-01):
- Real-time: regex patterns `TFEP_TRIGGERED`, `TFEP_RESOLVED`, `TFEP_ESCALATED` scanned from NDJSON stdout (TAD:902-907).
- Post-hoc: result file contains `EXIT_RECOMMENDATION: TFEP_HALT` (distinct from generic `HALT`); checked BEFORE generic HALT (higher priority) (TAD:947-959).
- `MonitorState` extended with `tfep_triggered: bool`, `tfep_trigger_count: int`, `tfep_status: str` (TAD:911-917).

**Phase-loop integration** (TAD:962-998): new `PhaseStatus.TFEP_HALT` branch in `execute_sprint()` calls `_handle_tfep_halt(...)` returning `"resolved"` | `"escalated"` | `"halt"`. `TFEP_HALT` NOT in `is_failure` (TAD:1162-1170) — triggers TFEP branch, not generic failure branch. `TFEP_RESOLVED` IS in `is_success` (TAD:1156-1159).

**`_handle_tfep_halt()` orchestration** (TAD:1002-1125, 10 steps):
1. Get/create `EscalationState`.
2. Read `failure_context.yaml`.
3. `esc.advance(failing_tests)` returns light/standard/halt.
4. Run `ForensicOrchestrator.run()`.
5. `perform_rollback()`.
6. `inject_remediation_tasks()` into isolation-dir phase file.
7. `build_tfep_resume_prompt()`.
8. Re-launch via `_PipelineClaudeProcess` with `extended_turns = int(config.max_turns * esc.budget_multiplier)` and `extended_timeout = extended_turns * 120 + 300 + 600` (+600s TFEP padding).
9. `_determine_phase_status()` on re-launched subprocess.
10. `write_incident_report()`.

**New CLI flags** (TAD:1209-1219, SRTH:181-182):
- `--tfep-model` (default `""` = Sonnet)
- `--tfep-agents` (default 2, range 2-4)
- `--tfep-budget-multiplier` (default 1.5, range 1.0-3.0)

**Git baseline capture** (TAD:704-719): `git rev-parse HEAD` at phase start, stored for rollback diff baseline. Wrapped in try/except for non-git repos.

**Rollback intersection algorithm** (TAD:644-701, FR-TFEP-10 at SRTH:289-311):
1. `git diff --name-only {baseline}` → files changed during this phase.
2. Save full patch to `results/phase-{N}-tfep-rollback.patch` regardless of scope.
3. Intersect causal files (from `rca-verdict.md`) with phase-changed files.
4. Full revert if all changed files are causal; selective `git checkout` if some.
5. Only files changed during *this* phase are eligible — never reverts prior-phase work (SRTH:303-306).

**Remediation task injection** (TAD:723-815): inserts `## Failure Remediation Plan (Adjudicated)` block into isolation-dir copy of phase file. Remediation tasks use `T{XX}.50+` IDs to avoid collision with `T{XX}.01-T{XX}.20`. Format matches `parse_tasklist()` regex `^###\s+(T\d{2}\.\d{2})\s*(?:--|-—|—)\s*(.+)`.

**Resume prompt** (TAD:818-893): `/sc:task-unified Execute remediation tasks in @{phase_file} --compliance strict --strategy systematic` with explicit "SKIP tasks T01-T{last_completed}", "EXECUTE remediation tasks starting from T{XX}.50", "After remediation tasks, re-run ALL verification/test tasks", git diff summary inline.

**Phase entry/exit contracts** (TAD:1252-1306):
- Contract 1 (Phase subprocess → Runner): result file `EXIT_RECOMMENDATION: TFEP_HALT`; CWD `failure_context.yaml`; NDJSON `TFEP_TRIGGERED`.
- Contract 2 (Runner → Forensic agent): RCA prompt `/sc:troubleshoot` + inline context, no `--fix`; Solution prompt `/sc:brainstorm` + inline `rca-verdict.md`, tasklist-compatible format.
- Contract 3 (`ForensicOrchestrator` → Executor): `ForensicResult` dataclass with `status`, `rca_verdict_path`, `solution_verdict_path`, `rollback_needed`, `causal_files`, `remediation_tasks`, `tier`, `agent_outputs`, `incident_summary` (TAD:292-302, 1280-1290).
- Contract 4 (Executor → Phase subprocess re-launch): `/sc:task-unified --compliance strict`, rollback notice, skip-prior-tasks, git diff summary, result file path.

## 11. Failure Handling & Fallbacks

**Three-level adversarial-failure degradation chain** (P-011 replacing original orchestrator-direct-ranking fallback; proposal-verdicts.md:268-290; section-C-R-01 `risk-register.md:27-31`):
1. Retry adversarial with `--depth quick`.
2. Spawn single Sonnet scoring agent with 60s hard timeout + 1000-token cap.
3. Emit findings as-is with `debate_status: "skipped"` — all surviving hypotheses proceed.

**Token-overrun handling** (P-012 replaces runtime token monitoring; proposal-verdicts.md:300-331): static per-phase rules — SHOULD soft target + MUST hard stop + deterministic overflow action. Adds `budget_status` field to `progress.json` for observability. Deterministic truncation (e.g., Phase 6: omit rejected-hypotheses) (`risk-register.md:64-68`).

**Graceful degradation levels** (`forensic-spec.md:1800-1807`): Full → Reduced precision (Serena down) → Reduced depth (Sequential down) → Minimal (all MCP down, `--depth quick` enforced).

**Resume protocol**: `progress.json` self-describing — every recoverable state explicitly encoded, never inferred (CCF-4, proposal-verdicts.md:879-888). Stale-codebase detection on resume via `git rev-parse HEAD` or mtime fallback (FR-053).

**TFEP-specific failure modes** (TAD):
- All forensic agents fail (TAD:534-540): explicit "at least one agent must succeed" check. If `len(successes) == 0`, log error, return partial output paths. Weakest spot — no explicit fallback beyond "return partial."
- Subprocess cleanup (TAD:578-603): `ForensicProcess.terminate()` inherits SIGTERM → 10s → SIGKILL on process group. `ForensicOrchestrator.run()` wraps in try/except, calls `_cleanup()` on exception.
- Judge subprocess failure (TAD:572-575): non-zero exit logs warning, still returns verdict path; `_build_result()` parsing presumably defensive.
- Missing `failure_context.yaml` (TAD:1031-1034): `_handle_tfep_halt` returns `"halt"` immediately. Converts missing-context bug into hard halt, not silent skip.
- Required-field validation (TAD:400-412): `_load_context()` raises `ValueError` if `test_names`, `test_files`, `error_output`, `expected_behavior`, `actual_behavior`, `changes_made`, `task_description` absent.
- Forensic `status="failed"` (TAD:1054-1057): incident report with `outcome="forensic_failed"`, return `"halt"`.
- Re-launch escalates again (TAD:983-994): loop re-enters TFEP branch; `EscalationState.advance()` returns `"halt"` on count >= 3.
- Phase isolation dir cleanup overwriting forensic artifacts (SRTH:435): mitigated by writing TFEP artifacts to `results/phase-{N}-tfep/`, NOT into per-phase isolation dir. Structural separation, not enforced by code.
- Non-git repo (TAD:716-719): `git rev-parse HEAD` wrapped in `except`; `git_baseline = ""` falls through; `perform_rollback` returns `RollbackResult(performed=False, scope="none")` when no phase-changed files (TAD:666-668).
- Backward compatibility (NFR-TFEP-03, SRTH:332-336): sprints that never trigger TFEP behave identically; `--no-escalation` bypasses TFEP entirely (Claude never writes `TFEP_HALT`); all new CLI flags optional with defaults.

**Notable gap** (section-B): no explicit MCP-unavailability fallback at the TFEP layer. Design assumes `/sc:adversarial`, `/sc:troubleshoot`, `/sc:brainstorm` always work. If those slash-command subprocesses fail (e.g., serena/auggie down), failure surfaces as subprocess non-zero exit, falls into "all agents fail / partial result" path. No graceful degradation specified.

**Risk register from SRTH:428-435**: forensic token over-consumption (mitigated 300s/agent + 3-attempt cap), rollback reverting correct work (selective rollback + preserved patch), re-launch re-executes prior tasks (explicit "skip T01-T04" + git diff), low-quality quick-depth verdict (judged low), wall-clock exhaustion (3-attempt limit), isolation-dir cleanup deleting forensic artifacts (writing outside isolation dir).

## 12. Roadmap & Phasing

### v2 Plan — 7 Milestones (authoritative)

`roadmap-2.md:60-71` declares 7 milestones with collision suffix `-2`. Calendar estimate: 10-13 weeks XL (`roadmap-2.md:24`). Complexity 0.87 HIGH (`roadmap-2.md:13`). Validation: PASS 0.91 (`roadmap-2.md:25-26`). Adversarial status: integrated (`roadmap-2.md:27`).

| ID | Name | Effort | Source |
|----|------|--------|--------|
| M0 | Spec Finalization Tier 1 (5 blockers: P-001, P-004, P-005, P-002, P-013) | M 3-5d | `roadmap-2.md:64,139` |
| M1 | Spec Finalization Tiers 2-3 (16 proposals P-006-P-016, P-021) | M 3-5d | `roadmap-2.md:65,203` |
| M2 | Foundation: command shell + skill shell + 9 finalized schemas | L 6-10d | `roadmap-2.md:66,262` |
| M3 | Phase 0 recon agents + domain discovery | M 3-5d | `roadmap-2.md:67,310` |
| M4 | Phase 1 (investigation) + Phase 3 (fix proposals) — fan-out phases | L 6-10d | `roadmap-2.md:68,363` |
| M5 | Phases 2+3b adversarial + Phases 4-6 pipeline (largest authoring milestone) | L 6-10d | `roadmap-2.md:69,376,436` |
| M6 | Testing + sync + verify-sync + docs | L 6-10d | `roadmap-2.md:70,507` |

Deliverables: 2 (`.claude/commands/sc/forensic.md` mirroring `src/superclaude/commands/forensic.md`, and `src/superclaude/skills/sc-forensic-protocol/SKILL.md` — `roadmap-2.md:18-22`).

### MVP/Shipping Gates

- **M0 gate**: 5 Tier-1 normative blockers — without these, "estimated rework cost is 3-5x" (`roadmap-2.md:105-106`).
- **M2 gate**: containers + 9 schemas finalized — required for parallel authoring (`roadmap-2.md:215-217`).
- **M6 gate**: `make sync-dev && make verify-sync` exits 0; all 58 success criteria SC-001-SC-058 pass (`test-strategy-2.md:374`); no SKILL.md stub sections (`roadmap-2.md:502`).

### Critical Path

Fully linear M0 → M1 → M2 → M3 → M4 → M5 → M6 (`roadmap-2.md:78-90`). "All sequential, no parallelism — spec correctness is prerequisite for each authoring stage" (`roadmap-2.md:89-90`).

**M5 is the bottleneck** — absorbs adversarial integration (Phases 2+3b), implementation (Phase 4), validation (Phase 5), synthesis (Phase 6), plus P-011/P-017/P-018/P-019/P-020 (`roadmap-2.md:376-440`).

**Intra-milestone parallelism opportunities** (`roadmap-2.md:91-94`):
- M4: Phase 1 and Phase 3 authoring share no dependencies.
- M5: Phases 4 and 5 can proceed in parallel.

### v1 → v2 Delta

| Aspect | v1 (`roadmap.md`) | v2 (`roadmap-2.md`) |
|--------|-------------------|---------------------|
| Date | 2026-02-26 (`roadmap.md:4`) | 2026-02-28 (`roadmap-2.md:6`) |
| Milestones | 9 (M0-M9) (`roadmap.md:14,37-47`) | 7 (M0-M6) (`roadmap-2.md:17,62-71`) |
| Proposals | 22 (14 ACCEPT + 8 MODIFY) (`roadmap.md:13`) | 21 (14 ACCEPT + 7 MODIFY, P-022 REJECTED) (`roadmap-2.md:16`) |
| Convergence basis | proposal-verdicts (initial) | proposal-verdicts.md convergence 1.00 (`roadmap-2.md:38`) |
| Validation | — | PASS, 0.91 (`roadmap-2.md:25-26`) |
| Adversarial status | — | integrated (`roadmap-2.md:27`) |
| Calendar | XL 10-14 weeks (`roadmap.md:15`) | XL 10-13 weeks (`roadmap-2.md:24`) |
| Complexity | not declared | 0.87 HIGH (`roadmap-2.md:12-13`) |
| Domain ID strategy | hash-based `[a-f0-9]{8}` | slug-based kebab-case (`roadmap-2.md:158,304`) |

**Milestone collapse rationale** (`roadmap-2.md:538`): "Fewer, larger milestones reduce coordination overhead; M3-M5 were granular enough to author but too fine for milestone tracking." Phases 1 and 3 share structural similarity.

Specifically:
- Checkpoint/Resume promoted into M5 (was standalone M3 in v1 per `roadmap.md:41`, `dependency-graph.md:50-54`) → `refs/checkpoint-resume.md` deliverable D5.7 (`roadmap-2.md:390`).
- CLI Integration absorbed into M2 Foundation (was M8 in v1 per `roadmap.md:46`).
- Testing/Sync remains terminal (M9 v1 → M6 v2).

v1 dependency-graph.md strictly linear, no intra-milestone parallelism declared (`dependency-graph.md:101-105`). v2 explicitly adds intra-milestone parallelism for M4 (Phase 1+3) and M5 (Phase 4+5) (`roadmap-2.md:91-94`).

### "-2" Suffix Rationale

`roadmap-2.md:534`: "Output directory already contains prior artifacts from 2026-02-26 run; collision protocol applied" — v2 authored as parallel artifact, not in-place replacement.

## 13. Dependency Graph

### Milestone Chain (v2)

Linear: M0 → M1 → M2 → M3 → M4 → M5 → M6 (`roadmap-2.md:78-90`).

### Pipeline Phase Runtime Data Flow (`dependency-graph.md:120-243`)

- Phase 0 → `investigation-domains.json` consumed by Phase 1 (`dependency-graph.md:133,140`).
- Phase 2 → `base-selection.md` consumed by orchestrator filter (`dependency-graph.md:154,156`); zero-hypotheses path → terminal report (`:158`).
- Phase 3b → `fix-selection.md` is PRIMARY DECISION POINT (`dependency-graph.md:182-183`).
- Phase 4 → `baseline-test-results.md` BEFORE any fix applied (`dependency-graph.md:192-193`).
- Phase 6 reads only 6 summary artifacts, no raw source — architectural constraint preserved (`dependency-graph.md:226-232`).

### External Dependencies (`dependency-graph.md:249-258`)

- `/sc:adversarial` (HIGH risk R-01 — runtime) — required by Phases 2 and 3b.
- Serena/Context7/Sequential MCP (LOW risk R-04, with fallback) — required by Phases 0b, 1, 3, 4.
- Haiku/Sonnet/Opus tier availability (MEDIUM risk R-02).
- `uv run ruff check`, `uv run pytest` (Low risk).

### Proposal-to-Proposal Dependencies (`dependency-graph.md:267-279`)

- P-001 is the root — must execute first; "all other proposals" depend on it establishing the spec baseline.
- P-017 → P-018 → P-019 chain (baseline test → exit state → `--clean` guard).
- P-020 → P-017 (baseline test results need redaction).
- P-009 → P-021 (multi-root path records reference domain_id).

### TFEP CLI Module Dependencies

Strictly downward (TAD:46-62): `commands.py → executor.py → tfep.py → process.py → monitor.py → models.py`.

## 14. Test Strategy

### Philosophy (`test-strategy-2.md:16-32`)

HIGH complexity → interleave ratio 1:1 (every authoring task pairs with a test/validation task). "Behavioral contract testing, not implementation testing" — tests validate schema-conforming artifacts on schema-defined inputs; not internal model tier heuristics or prompt wording. Continuous parallel validation at each milestone boundary, not deferred to final test milestone.

### Test Classification (`test-strategy-2.md:38-46`)

6 types — Smoke (per-phase), Integration, Edge case, Schema conformance, Security, Manual review. All gated at M6 — no upstream gating.

### Test Inventory (10 files, M6) — D6.1-D6.13 (`roadmap-2.md:456-470`)

- D6.1-D6.4: Phase 0/1/3/5 smoke tests (`tests/sprint/forensic/test_phase*_smoke.py`).
- D6.5: `test_checkpoint_resume.py` — validates `run_id` stability + `phase_status_map`.
- D6.6: `test_zero_hypotheses.py` (P-016 edge case).
- D6.7: `test_tiny_target.py` (P-015 — <5 files → single domain bypass).
- D6.8: `test_dry_run.py` (P-003).
- D6.9: `test_redaction.py` (P-020 — must redact ≥4 secret pattern types).
- D6.10: `test_schemas.py` — all 9 schemas with positive + negative variants (`test-strategy-2.md:299-311`).

### Fixture Design (`test-strategy-2.md:154-163`)

Single 5-file synthetic Python project: `main.py` (subprocess), `auth.py` (bare except), `utils.py` (untested), `tests/test_main.py` (partial coverage). Engineered to produce ≥2 domains and observable Phase 0 output. Canned artifacts per phase boundary at `tests/sprint/forensic/fixtures/canned_artifacts/{phase0,phase2,phase4}_output/` (`test-strategy-2.md:340-345`).

### Coverage Targets / Markers

- Schema tests → `@pytest.mark.unit` (`test-strategy-2.md:402`).
- Smoke tests → `@pytest.mark.integration` (`test-strategy-2.md:399-400`).
- 58 total success criteria SC-001-SC-058 (`test-strategy-2.md:374`).

### Stop-and-Fix Severity (`test-strategy-2.md:351-358`)

CRITICAL (schema/checkpoint/contract breaks) → stop immediately; HIGH (missing proposal integration) → fix in current milestone; default threshold = CRITICAL+HIGH always halt.

### Per-Milestone Gates (`test-strategy-2.md:50-145`)

M0/M1 = peer review; M2 = `make verify-sync` + file existence; M3/M4/M5 = content review; M6 = full pytest suite + sync exits 0. M6 rule: "ALL tests must pass before release. Any failing test, even in an 'optional' category, is fixed before marking M6 complete. Zero exceptions" (`test-strategy-2.md:143-144`).

## 15. Risk Register

Two distinct risk models — `risk-register.md` canonical (10 risks, P×I 1-5); `roadmap-2.md:516-526` 10 roadmap-execution risks.

### Canonical Risks (`risk-register.md:217-228`)

| ID | Risk | Prob | Impact | Exposure | Priority | Source |
|----|------|------|--------|----------|----------|--------|
| R-01 | sc:adversarial integration failures | 3 | 5 | **15 HIGH** | HIGH | `risk-register.md:18-33` |
| R-02 | Model tier unavailability (Haiku/Sonnet/Opus) | 2 | 4 | 8 MED | MED | `risk-register.md:37-52` |
| R-03 | Orchestrator token budget overruns | 4 | 3 | 12 MED | MED | `risk-register.md:56-72` |
| R-04 | MCP server unavailability | 2 | 3 | 6 LOW | LOW | `risk-register.md:76-91` |
| R-05 | Non-deterministic Phase 0 domain discovery | 3 | 4 | 12 MED | MED | `risk-register.md:95-111` |
| R-06 | Adversarial convergence failure | 2 | 3 | 6 LOW | LOW | `risk-register.md:115-129` |
| R-07 | Phase 4 worktree isolation failures | 3 | 4 | 12 MED | MED | `risk-register.md:133-149` |
| R-08 | Resume stale-target detection gaps | 3 | 3 | 9 MED | MED | `risk-register.md:153-169` |
| R-09 | Spec amendment integration complexity | 3 | 3 | 9 MED | MED | `risk-register.md:173-189` |
| R-10 | Mock agent test infrastructure | 3 | 3 | 9 MED | MED | `risk-register.md:193-210` |

**Only R-01 (adversarial integration) is HIGH (15).** Residual risk after mitigation drops to MEDIUM (`risk-register.md:33`).

### Key Mitigations (`risk-register.md:232-242`)

- **R-01**: Pre-M6 validation of `/sc:adversarial`; three-level fallback chain (P-011) — L1 retry `--depth quick`; L2 single Sonnet scoring agent (60s timeout, 1000 token cap); L3 direct passthrough with `"debate_status": "skipped"` (`risk-register.md:27-31`).
- **R-03**: P-012 per-phase overflow table; `budget_status` field; deterministic truncation (Phase 6: omit rejected-hypotheses) (`risk-register.md:64-68`).
- **R-05**: Hash-based domain ID `hash(name, sorted(files_in_scope))[:8]` (P-009) — file scope determines ID even when names shift (`risk-register.md:104-109`).
- **R-09**: P-001 executed FIRST and mechanically (verbatim move, no rephrasing); spec-amendments-checklist.md orders all 22 proposals (`risk-register.md:183-188`).
- **R-10**: Build fixtures during M2 alongside schema definitions, not at M9 (`risk-register.md:242`).

### Roadmap-Execution Risks (`roadmap-2.md:516-526`)

Different set covering authoring: R-001 (adversarial API change, exposure 10), R-002 (slug ID instability, 8), R-003 (token ceilings too low, 9), R-008 (adversarial convergence < 0.80, exposure 12 Medium, mitigated by partial-result continuation only hard-aborting below 0.5). R-010 = SKILL.md grows too large to load → use refs/ pattern.

## 16. Spec Amendments & Residual Ambiguity

The spec needed 22 proposals applied before authoring — heaviest signal of residual ambiguity.

### M0 — Tier 1-2 Structural Prerequisites (8 proposals, `spec-amendments-checklist.md:16-162`)

- **P-001 (Section 17 normativity)**: blocking root — moves FR-047-FR-055, NFR-009, NFR-010, Schema 9.9 out of Section 17 into canonical sections. "MECHANICAL move — do not rephrase" (`spec-amendments-checklist.md:40`).
- **P-004 (path inconsistencies)**: Score 10.00/10 — adversarial output paths must be `phase-2/adversarial/*` (`spec-amendments-checklist.md:45,49-54`).
- **P-009 (stable domain IDs)**: hash-based IDs; hypothesis IDs become `H-[a-f0-9]{8}-\d+` (`spec-amendments-checklist.md:60-69`).
- **P-006**: `new-tests-manifest.json` schema; **P-013** model tier observability; **P-015** minimum domain rule (1-10, not 3-10); **P-014** MCP tool contract (`Edit, MultiEdit` added to `allowed-tools`); **P-021** multi-root provenance.

### M1 — Tier 3-5 Behavioral/Runtime/Hardening (14 proposals, `spec-amendments-checklist.md:172-413`)

- P-017 (baseline test artifact); P-018 (3-state exit model success/success_with_risks/failed); P-003 (dry-run + `skipped_phases`); P-002 (`--depth` precedence); P-005 (Phase 3b canonical path).
- P-011 (three-level adversarial fallback); P-012 (token overflow table); P-020 (artifact redaction, `--no-redact` flag); P-016 (zero-hypothesis terminal + `--auto-relax-threshold`); P-022 (concurrency default 5, per-phase MCP budget — MODIFY in checklist but REJECTED in v2 roadmap convergence; `roadmap-2.md:572`).
- P-019 (`--clean` guard clause minimal scope).

### Three Internal Contradictions Still Standing

These are unresolved between `spec-amendments-checklist.md` (2026-02-26) and `roadmap-2.md` (2026-02-28):

1. **P-007 `secrets_exposure` category**: REJECTED in checklist `spec-amendments-checklist.md:362` vs ADDED in v2 roadmap `roadmap-2.md:155`.
2. **P-008 progress.json fields (`run_id` / `phase_status_map`)**: REJECTED in checklist `spec-amendments-checklist.md:400` vs REQUIRED in v2 roadmap `roadmap-2.md:157`.
3. **P-010 fix-tier count**: "up to three" with `uniqueItems` in checklist `spec-amendments-checklist.md:373` vs **exactly 3** mandated in v2 roadmap `roadmap-2.md:156`.

Additional v2-only divergence: **Domain ID strategy** — checklist uses hash-based `H-[a-f0-9]{8}-\d+` (`spec-amendments-checklist.md:64-66`) vs v2 roadmap slug-based `H-{domain_slug}-{seq}` (`roadmap-2.md:158`).

### Explicitly Deferred to v2.0 (`spec-amendments-checklist.md:445-458`)

`secrets_exposure` category, `spec_version`/`run_id`/`phase_status_map` in progress.json, exactly-3-tiers constraint, `--clean=archive|delete` variants, `--redaction-config`, full MCP scheduler with semaphores.

**Signal**: spec needed 22 proposals × major sections; multiple proposals reach v2 roadmap with inverted verdicts — team had not fully converged when v2 was authored.

## 17. Adversarial Process — How This Design Was Stress-Tested

Two distinct `/sc:adversarial` runs are evidenced in the corpus:

- **Run 1 (Spec Review, 2026-02-28)** — 3 advocate agents (architect, quality-engineer, analyzer) debated 22 spec-improvement proposals grouped A/B/C/D. Output: `proposal-verdicts.md` (one verdict per proposal).
- **Run 2 (Refactor Plan, 2026-03-19)** — 2 advocate agents (architect, analyzer) debated 2 competing refactor proposal variants (forensic-refactor-handoff.md vs tfep-refactoring-context.md). Output: `diff-analysis.md`, `debate-transcript.md`, `base-selection.md`, `refactor-plan.md`, `merge-log.md`, `merged-tasklist.md`.

Both runs are meta-process artifacts — the design itself used the adversarial protocol it later prescribes.

### Three Advocate Philosophies (Run 1)

- **opus:architect** (`variant-1-opus-architect.md:1-7`): "Architectural soundness, implementation feasibility within Claude Code's actual capabilities, avoiding over-specification" — skeptical of "proposals that add complexity without clear implementation benefit." Championed *minimalism + invariant preservation*. Pushed simpler alternatives: slug instead of UUID/hash for P-009 (`:51-55`), single `--redact-artifacts` flag instead of redaction policy framework for P-020 (`:108-112`), restrict `--clean` to terminal success without sub-options for P-019 (`:102-106`).
- **opus:quality-engineer** (`variant-2-opus-quality-engineer.md:1-7`): "Testability, determinism, edge case completeness, schema rigor" — skeptical of "proposals that weaken quality gates." Championed *mandatory fields and testable invariants*. Wanted all `progress.json` fields mandatory (P-008 `:44-47`, 0.90 confidence), wanted to retain hard token ceilings as testable max (P-012 `:64-68`), configurable redaction policy not single flag (P-020 `:106-109`).
- **opus:analyzer** (`variant-3-opus-analyzer.md:1-7`): "Practical impact — which proposals fix real implementation blockers vs theoretical concerns" — skeptical of "proposals that address unlikely scenarios at the cost of spec complexity." Championed *frequency-weighted pragmatism*. Cited day-1 implementation pain (P-001 `:11-12`, P-002 `:14-17`, P-004 `:24-27`); discounted low-frequency scenarios: domain ID drift "theoretically problematic but practically rare" (P-009 `:51-55`), full redaction policy "over-engineering for v1" (P-020 `:109-113`), multi-root provenance only at domain level since most invocations target one root (P-021 `:115-119`).

**Triangulation**: architect set ceiling on complexity, QE set floor on rigor, analyzer set lens for what ships. All three converged on rejecting **P-022** (MCP scheduler) at 0.72-0.78 confidence (`variant-1-opus-architect.md:119-122`, `variant-3-opus-analyzer.md:121-124`) — strongest cross-perspective signal in the corpus.

### Merge Winner Pattern — Edge-Case Floor Rule (Run 2)

`base-selection.md` rubric: 50% quantitative + 50% qualitative. Decision turned on an *eligibility floor*, not the score:

- **Quantitative** (`:4-15`): 5 weighted metrics (Requirement Coverage 0.30, Internal Consistency 0.25, Specificity 0.15, Dependency 0.15, Section Coverage 0.15). A = 0.860, B = 0.839 (within 2.5%).
- **Qualitative** (`:19-110`): 6 dimensions × 5 binary criteria each. Both tied at 18/30 = 0.600.
- **Combined**: A = 0.730, B = 0.720, margin 1.0% (within 5% tiebreaker range, `:135-136`).

**Variant B scored 0/5 on Invariant & Edge Case Coverage** (`:91`), triggering explicit "edge case floor" rule: "BELOW FLOOR (ineligible as base variant)" (`:95`). Variant A's 1/5 cleared by a hair. Rationale (`:141-149`): (1) floor enforcement; (2) Variant A won two most architecturally consequential debate points (C-001 flag model 65%, X-001 same-topic contradiction 60%), both L3 (state-mechanics).

**Decision criteria priority order**: edge-case eligibility floor > L3 architectural correctness > L2 specificity > L1 presentation. Floor overrode near-tied score — team trusted "covers edge cases at all" more than "complete coverage of explicit requirements."

### Orthogonal Invariant Probe — Caught What Advocates Missed (Run 2)

Debate converged to only **76%** vs 80% threshold (`debate-transcript.md:156`), explicitly NOT_CONVERGED. Blocking finding: "2 HIGH-severity UNADDRESSED invariants (INV-001, INV-004)" (`:158`).

Round 2.5 invariant probe (`:139-149`) ran independent check, surfaced 5 invariants neither variant covered:
- **INV-001 (HIGH)**: How to distinguish pre-existing vs agent-written tests without baseline mechanism.
- **INV-003 (MEDIUM)**: pytest parametrize inflates "3+ new tests fail" threshold into false positives.
- **INV-004 (HIGH)**: Forensic output → task-unified tasklist insertion format unspecified.
- **INV-005 (MEDIUM)**: Same-failure vs new-failure distinction for escalation.

**Both HIGH invariants (INV-001, INV-004) converted directly into new tasks** (Change #10, #11 in `merge-log.md:73-85`) — neither from either advocate. Six debate points remained unresolved at convergence (S-005, C-005, C-006, X-003, A-002, A-003 — `debate-transcript.md:159`), all L1/L2 (cosmetic/specificity), not L3 (architecture).

### Merge Log — 11/11 Applied (Run 2, `merge-log.md:1-12`)

Pattern: base = Variant A (architecture skeleton), 9 incorporations from Variant B (tactical specs), 2 inserts from invariant probe.

- **From Variant A (preserved)**: 3-axis flag model, responsibility split, coupling contract, `--caller`/`--trigger` concept, profiles abstraction, genericity preservation (`base-selection.md:151-159`). Explicitly NOT taken from B: `--depth` overloading approach (`refactor-plan.md:97`, X-001 60% A-win).
- **From Variant B (incorporated)**: per-phase behavior table (`merge-log.md:14-20`), binary escalation thresholds (`:22-27`), token budget estimates (`:29-32`), two-phase implementation strategy (`:34-40`), YAML context interface (`:42-46`), section-by-section forensic change mapping (`:48-53`), "test is wrong" as valid outcome (`:55-59`), artifact directory tree (`:61-65`), user-approved decision log (`:67-71`).
- **From invariant probe (new)**: test baseline snapshot mechanism (`:73-78`, Task 1.3), artifact/tasklist insertion format (`:80-85`, Task 2.5).

Post-merge validation (`:89-105`) rescanned for contradictions; found none. Merger explicitly checked merged document didn't reintroduce rejected `--depth` overloading conflict.

### Verdicts Summary (Run 1) — 14 ACCEPT, 7 MODIFY, 1 REJECT (`proposal-verdicts.md:38-42`)

22 proposals → 100% convergence in 2 rounds (`proposal-verdicts.md:6,154`).

**Pattern across all 7 MODIFY verdicts**: spec was systematically narrowed from QE's maximalist initial positions toward simpler v1 defaults, with architect and analyzer applying drag. Of 7 modifications, **5 originated as QE-vs-others disagreements** (`:23-37` Dissenting Opinions) — P-007, P-008, P-012, P-019, P-020 all moderate QE's maximalism. Structural reason protocol uses 3 advocates rather than 2: QE consistently pushed comprehensiveness, requiring two counter-voices to triangulate to v1-realistic scope.

## 18. Accepted vs Rejected Proposals (P-001 through P-022)

22 proposals submitted (`spec-review-proposals.md:1-221`). Run 1 verdict: 14 ACCEPT, 7 MODIFY, 1 REJECT (`proposal-verdicts.md:38-42`). V2 roadmap convergence: 14 ACCEPT + 7 MODIFY, P-022 REJECTED (`roadmap-2.md:16`).

### Top-3 ACCEPT (highest confidence, unanimous)

- **P-001** (conf 0.96, `proposal-verdicts.md:16`) — Move panel additions from Section 17 commentary into normative sections. "Non-normative requirements are untestable requirements" (QE, `variant-2-opus-quality-engineer.md:12`). Single highest-impact structural fix.
- **P-004** (conf 0.94, `proposal-verdicts.md:19`) — Standardize artifact paths to `phase-2/adversarial/`. Path inconsistencies "the #1 source of 'it works for me but not for you' bugs" (analyzer, `variant-3-opus-analyzer.md:27`).
- **P-013** (conf 0.93, `proposal-verdicts.md:28`) — Capability fallback for model-tier assignment with "requested vs actual tier" logging. Architect: "most feasibility-critical proposal" (`variant-1-opus-architect.md:75`); analyzer: "most practically impactful feasibility proposal" (`variant-3-opus-analyzer.md:74`).

### Top-3 REJECT/MODIFY (boundary signals — what NOT to do)

- **P-022 — REJECTED** (conf 0.76, `proposal-verdicts.md:37`, only rejection). Full MCP scheduler with semaphores + exponential backoff + deterministic queue ordering. Rejection rationale (`:87-97`, also proposal-verdicts.md:446-481): (1) Framework delegation — scheduling belongs in MCP.md, not forensic spec; duplicating creates "maintenance conflicts and potential divergence" (`:91`); (2) Existing mitigation — `--concurrency` flag already handles it (`:93`); (3) Over-specification — prescribing internal mechanisms "inappropriate for a requirements specification" (`:95`). Replaced with prompt-based MCP access budgets per agent type (Phase 1 investigation: 3 Serena + 1 Context7 per domain; Phase 4a: 5 Serena + 2 Context7 per fix) and `--concurrency` default reduced 10 → 5. **Signal: don't put framework-level concerns into feature specs**.
- **P-020 — MODIFIED** (conf 0.77, `proposal-verdicts.md:35`). Original: configurable per-environment redaction policy with secure raw retention flag. Modified: agent prompt awareness + single `--redact` flag (default true), defer configurable policy to v2 (`:73-76`, proposal-verdicts.md:816-823). Per-agent prompt-level redaction REJECTED — agents can't reliably self-redact. Replaced with pipeline-level post-processing pass after each phase write. Fixed default pattern set (AWS keys, GCP service-account keys, `password=`/`secret=`/`token=`/`api_key=`, PEM private key blocks). **Signal: don't build enterprise frameworks for v1 when a single flag covers 90% of use cases**.
- **P-019 — MODIFIED** (conf 0.78, `proposal-verdicts.md:34`). Original: `--clean=archive|delete` sub-options. Modified: binary — clean only on terminal `success`, retain otherwise (`:68-71`, proposal-verdicts.md:782-799). "Over-engineered for <5% probability scenario." Reduced to one-sentence guard clause in FR-052: "`--clean` is a no-op unless all phases completed successfully." **Signal: don't add CLI sub-options for niche cases when terminal-status gating covers the use case**.

### Other Rejected Sub-Elements (design boundaries)

- **P-007 `secrets_exposure` risk category REJECTED** (proposal-verdicts.md:117-125): no FR drives it, vague panel reference, oracle testing gap. Only `overall_risk_score` calculation alignment accepted. (Note: re-added in v2 roadmap — internal contradiction.)
- **P-008 progress.json field additions partly REJECTED** (proposal-verdicts.md:148-157): `spec_version` deferred post-v1.0 (YAGNI); `run_id` deferred (observability not correctness); `phase_status_map` rejected outright (duplicates `completed_phases` + `current_phase`). Only 3 of 5 fields accepted: `target_paths` (required), `flags` (required), `git_head_or_snapshot` (optional). (Note: re-added in v2 roadmap — internal contradiction.)
- **P-010 "Exactly 3 fix tiers" REJECTED** (proposal-verdicts.md:194-203): forces filler content; ~500-1000 tokens padding per proposal × N hypotheses; cannot distinguish genuine tiers from filler in automated tests. `minItems` stays at 1. Only uniqueness constraint accepted. (Note: v2 roadmap mandates exactly 3 — internal contradiction.)
- **P-005 — Migration fallback for legacy fix-selection.md path REJECTED** (proposal-verdicts.md:626-633): spec is v1.0.0-draft, no existing implementations; migration adds complexity for non-existent concern. Canonical path: `phase-3b/fix-selection.md`.
- **P-012 — Runtime token monitoring REJECTED** (proposal-verdicts.md:300-331): replaced with static per-phase rules (SHOULD soft target + MUST hard stop + deterministic overflow action). Runtime token monitoring not enforceable in harness. Adds `budget_status` field to `progress.json`.
- **P-011 — Orchestrator-direct-ranking fallback REJECTED** (proposal-verdicts.md:268-290): violates Section 4.3 invariant. Replaced with three-level degradation chain (retry quick, single Sonnet scoring agent, emit as-is with `debate_status: "skipped"`).
- **P-003 — `skipped_by_mode` per-phase status enum REJECTED** (proposal-verdicts.md:637-661): replaced with `skipped_phases` array in `progress.json` (self-describing).

### Cross-Cutting Findings

- **CCF-1 (aspirational vs enforceable, proposal-verdicts.md:845-857)**: spec language mandating behavior unenforceable in current Claude Code runtime (hard token ceilings, model-tier verification, MCP semaphores) gets replaced with observability hooks (`requested_tier`, `actual_tier`, `budget_status`) and deterministic fallback chains, never silent assumption.
- **CCF-3 (Section 17 normativity split, proposal-verdicts.md:871-877)**: FR-047-FR-055, NFR-009, NFR-010, Schema 9.9 live in commentary but contain normative requirements (security-relevant FR-053/FR-054). P-001 (Tier 1) requires mechanical integration before any other spec edit.
- **CCF-4 (resume safety, proposal-verdicts.md:879-888)**: most recurring weak point — `progress.json` must be self-describing; every recoverable state explicitly encoded, never inferred from flag combinations or absent entries.

## 19. Open Questions / Known Unknowns

Items the design team itself flagged as unresolved, distilled from spec amendments and adversarial verdicts:

1. **P-007 `secrets_exposure` category** — REJECTED in spec-amendments-checklist (2026-02-26, `:362`) but ADDED in v2 roadmap (2026-02-28, `roadmap-2.md:155`). Convergence incomplete between adjacent dates.
2. **P-008 `run_id` / `phase_status_map`** — REJECTED in checklist (`:400`) vs REQUIRED in v2 roadmap (`roadmap-2.md:157`).
3. **P-010 fix-tier count** — "up to three with `uniqueItems`" in checklist (`:373`) vs **exactly 3** in v2 roadmap (`roadmap-2.md:156`).
4. **Domain ID strategy** — hash-based `H-[a-f0-9]{8}-\d+` in checklist (`:64-66`) vs slug-based `H-{domain_slug}-{seq}` in v2 roadmap (`roadmap-2.md:158,304`).
5. **TFEP-layer MCP routing** — TRC:88-97 mentions model tiers but not MCP servers; no explicit per-phase routing for auggie/serena/context7/tavily/sequential at TFEP layer (section-B gap).
6. **All-forensic-agents-fail fallback** — TAD:534-540 logs error and returns partial paths; "weakest spot in design — no explicit fallback path beyond 'return partial'" (section-B).
7. **MCP-unavailability at TFEP layer** — design assumes `/sc:adversarial`, `/sc:troubleshoot`, `/sc:brainstorm` always work; no graceful degradation specified for sub-skill MCP failure (section-B notable gap).
8. **Six unresolved debate points at Run 2 convergence**: S-005, C-005, C-006, X-003, A-002, A-003 (`debate-transcript.md:159`) — all L1/L2 (cosmetic/specificity), not L3 (architecture). Did not block convergence but remain open.
9. **Deferred to v2.0 explicitly** (`spec-amendments-checklist.md:445-458`): `secrets_exposure` category, `spec_version`/`run_id`/`phase_status_map` in progress.json, exactly-3-tiers constraint, `--clean=archive|delete` variants, `--redaction-config` flag, full MCP scheduler with semaphores.

## 20. Citations

All `file:line` citations from source sections, preserved verbatim.

### From Section A (Spec & Vision)

`forensic-spec.md:48-51`, `:54-66`, `:68-72`, `:76-89`, `:99`, `:108-110`, `:144-146`, `:199-202`, `:205-206`, `:215-216`, `:222-223`, `:231-237`, `:240-274`, `:276-308`, `:309-322`, `:397-404`, `:488-575`, `:556-575`, `:577-626`, `:628-666`, `:650-657`, `:668-716`, `:718-751`, `:753-802`, `:804-849`, `:843-847`, `:851-870`, `:895-905`, `:897-905`, `:1283-1288`, `:1320-1323`, `:1335-1338`, `:1361-1399`, `:1448-1503`, `:1509-1527`, `:1529-1540`, `:1552-1573`, `:1568-1572`, `:1580-1614`, `:1616-1649`, `:1620-1649`, `:1659-1682`, `:1690-1758`, `:1786-1799`, `:1800-1807`, `:1811-1855`, `:1813-1826`, `:1849-1854`, `:1876-1888`, `:1889-1903`, `:1906-1915`, `:1919-2042`, `:1923-1945`, `:1953-1984`, `:1986-1998`, `:1990-1993`, `:2003-2026`, `:2062-2065`, `:2079-2080`, `:2095-2096`, `:2127`, `:2174`, `:2174-2175`, `:2246-2247`, `:2247-2248`, `:2308-2320`.

`forensic-explore.md:90-129`, `:132-147`, `:136-147`.

`spec-review-proposals.md:1-221`.

`proposal-verdicts.md:14-16`, `:117-125`, `:148-157`, `:159-176`, `:194-203`, `:268-290`, `:300-331`, `:446-481`, `:626-633`, `:637-661`, `:782-799`, `:803-823`, `:816-823`, `:845-857`, `:871-877`, `:879-888`.

### From Section B (Architecture)

TRC (`tfep-refactoring-context.md`): `:3`, `:13-35`, `:42-77`, `:65-77`, `:88-97`, `:91-94`, `:99`, `:99-100`, `:138-145`, `:206-242`, `:241-269`, `:273`, `:299`, `:357-372`, `:382`.

TAD (`tfep-architecture-design.md`): `:36-44`, `:46-62`, `:64-68`, `:70-74`, `:248-282`, `:259-261`, `:292-302`, `:344-376`, `:344-395`, `:380-395`, `:400-412`, `:447-486`, `:463-485`, `:525-532`, `:534-540`, `:542-575`, `:550`, `:572-575`, `:578-603`, `:644-701`, `:666-668`, `:704-719`, `:716-719`, `:723-815`, `:818-893`, `:902-907`, `:911-917`, `:947-959`, `:962-998`, `:983-994`, `:1002-1125`, `:1031-1034`, `:1054-1057`, `:1156-1159`, `:1162-1170`, `:1185`, `:1209-1219`, `:1213`, `:1252-1306`, `:1271`, `:1280-1290`, `:1391`.

FRH (`forensic-refactor-handoff.md`): `:9-25`, `:23-25`, `:30-46`, `:43`, `:241-269`, `:285-296`, `:446-454`, `:462-470`, `:521-538`.

SRTH (`sprint-runner-tfep-handoff.md`): `:3`, `:23-24`, `:38-51`, `:40-51`, `:46-50`, `:122-138`, `:172-176`, `:181-182`, `:185-191`, `:185-195`, `:192-195`, `:198-199`, `:199`, `:235-244`, `:244`, `:289-311`, `:303-306`, `:316-322`, `:332-336`, `:344-346`, `:383`, `:428-435`, `:435`.

### From Section C (Roadmap, Risks, Tests)

`roadmap.md:4`, `:13`, `:14`, `:15`, `:37-47`, `:38-47`, `:41`, `:46`.

`roadmap-2.md:6`, `:12-13`, `:13`, `:15-16`, `:16`, `:17`, `:18-22`, `:24`, `:25-26`, `:25-27,15-16`, `:27`, `:38`, `:60-71`, `:62`, `:62-71`, `:64,139`, `:65,203`, `:66,262`, `:67`, `:67,310`, `:68`, `:68,363`, `:69,376,436`, `:69,376`, `:70,507`, `:78-90`, `:89`, `:89-90`, `:91-94`, `:93-94`, `:94`, `:105-106`, `:155`, `:156`, `:157`, `:158`, `:158,304`, `:215-217`, `:376-440`, `:390`, `:456-470`, `:502`, `:516-526`, `:534`, `:538`, `:540`, `:548-572`, `:572`.

`dependency-graph.md:50-54`, `:101-105`, `:120-243`, `:133,140`, `:154,156`, `:158`, `:182-183`, `:192-193`, `:226-232`, `:249-258`, `:267-279`.

`risk-register.md:18-33`, `:27-31`, `:33`, `:37-52`, `:56-72`, `:64-68`, `:76-91`, `:95-111`, `:104-109`, `:115-129`, `:133-149`, `:153-169`, `:173-189`, `:183-188`, `:193-210`, `:217-228`, `:219`, `:221`, `:223`, `:232-242`, `:242`.

`test-strategy-2.md:16-32`, `:23-26`, `:28-32`, `:38-46`, `:50-145`, `:143-144`, `:154-163`, `:299-311`, `:340-345`, `:351-358`, `:374`, `:399-400`, `:402`.

`spec-amendments-checklist.md:16-162`, `:40`, `:45,49-54`, `:60-69`, `:64-66`, `:172-413`, `:362`, `:373`, `:400`, `:445-458`.

### From Section D (Adversarial Process)

`group-A-schema-integrity.md:1`, `:5-12`, `:14-21`, `:23-30`, `:32-39`, `:41-48`, `:50-57`.

`group-B-architecture-feasibility.md:1`, `:5-12`, `:14-21`, `:23-30`, `:32-39`, `:41-48`, `:50-57`.

`group-C-phase-contracts.md:1`, `:5-12`, `:14-21`, `:23-30`, `:32-39`, `:41-48`.

`group-D-quality-security.md:1`, `:5-12`, `:14-21`, `:23-30`, `:32-39`, `:41-48`.

`variant-1-opus-architect.md:1-7`, `:51-55`, `:75`, `:102-106`, `:108-112`, `:119-122`.

`variant-2-opus-quality-engineer.md:1-7`, `:12`, `:44-47`, `:64-68`, `:106-109`.

`variant-3-opus-analyzer.md:1-7`, `:11-12`, `:14-17`, `:24-27`, `:27`, `:51-55`, `:74`, `:109-113`, `:115-119`, `:121-124`.

`diff-analysis.md:8-12`, `:30`, `:32`, `:36`, `:46`.

`base-selection.md:4-15`, `:19-110`, `:91`, `:91-95`, `:95`, `:135-136`, `:141-149`, `:151-159`.

`debate-transcript.md:139-149`, `:156`, `:158`, `:159`.

`merge-log.md:1-12`, `:14-20`, `:22-27`, `:29-32`, `:34-40`, `:42-46`, `:48-53`, `:55-59`, `:61-65`, `:67-71`, `:73-78`, `:73-85`, `:80-85`, `:89-105`.

`refactor-plan.md:97`.

`proposal-verdicts.md:6,154`, `:16`, `:19`, `:23-37`, `:28`, `:34`, `:35`, `:37`, `:38-42`, `:68-71`, `:73-76`, `:87-97`, `:91`, `:93`, `:95`.

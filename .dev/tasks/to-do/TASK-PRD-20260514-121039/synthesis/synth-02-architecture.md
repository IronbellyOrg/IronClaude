# Synthesis 02: Architecture and Dependencies for /sc:task PRD

**Source research:** 02-architecture-and-integration.md, 01-features-and-user-flows.md
**Template sections covered:** S10, S11, S14, S15, S17, S18, S20, S26
**Date:** 2026-05-14

---

## 10. Assumptions & Constraints

### 10.1 Technical Assumptions

Sourced verbatim from FINAL-REPORT §10 (A-001..A-005) per research file `02-architecture-and-integration.md` §7. [DOC-CROSS-VAL: FINAL-REPORT §10 / RELEASE-SPEC §2.1, §3.3, §3.5]

| ID | Assumption | Risk if Wrong | Validation Method |
|----|------------|---------------|-------------------|
| A-001 | Sequential + Serena MCP hard requirement for STRICT is correct current behavior, not itself a candidate for re-evaluation under STRICT-task outages | STRICT routing becomes ungated; load-bearing axiom of architecture invalidated; all STRICT tasks impacted | Audit-log skip-compliance telemetry (Q11) + document operator escape `--skip-compliance` (target <12% per RK-03) |
| A-002 | Candidate set is closed at Wave-1 extracts (TU-001..TU-006, SE-001..SE-006, TU-007) | Scope creep mid-release; dependency graph invalidated; additions force replan | Closed-set enforcement at release boundary; novel items go to R3 or later |
| A-003 | Effort labels S/M/L and value/tractability ratings are reliable proxies without explicit estimation | Sizing overrun; tasks marked S could exceed budget; schedule slips | Release split (R1 task-side / R2 sprint-side) provides pressure-release valve if S/M/L proves inaccurate |
| A-004 | The six universal quality principles (TU-003) are sound design and need not be re-derived | TU-003 NFR adoption unsound; verification quality regression | Q14 "both prompt and checklist" enforcement provides audit trail; programmatic checklist enables rollback hook |
| A-005 | `--caller task-unified` is consumed downstream by `/sc:forensic` but no draft has verified what `/sc:forensic` does with it | Q1/Q2 rename in R3 breaks forensic pipeline; single biggest unknown in architecture | Implementation phase must enumerate `/sc:forensic` consumers before any rename; DEFER-lock tests at RELEASE-SPEC §5.2.5 encode this via SoT constants |

### 10.2 Business Assumptions

| ID | Assumption | Risk if Wrong | Validation Method |
|----|------------|---------------|-------------------|
| BA-1 | TU-004 BLOCKED state user-impact at ~5-10% of `--compliance auto` users is acceptable [inference] (RELEASE-SPEC §2.2:120) | If actual impact >10%, user friction exceeds budget; migration guide may be insufficient | Audit log telemetry on BLOCKED frequency post-deploy; release notes call-out for `--compliance auto` users |
| BA-2 | `<12%` `--skip-compliance` usage target (Q11 metering) reflects healthy operator escape behavior | If skip rate exceeds 12%, STRICT tier gating is too aggressive; operator workflow disrupted | Audit log JSONL `skip_compliance` boolean field aggregated daily; reporting layer TBD per research §10.6 |
| BA-3 | Zero new CLI flags this release preserves backward compatibility for all four invokers (end-user, sprint, cleanup-audit, forensic) | If hidden flag dependency exists, invoker integration breaks silently | Regression baselines green: 921 sprint pass / 57 fail; 125/125 TUI; 16/16 ClaudeProcess; TEST-SPEC.md:34-80 |

### 10.3 User Assumptions

| ID | Assumption | Risk if Wrong | Validation Method |
|----|------------|---------------|-------------------|
| UA-1 | Users will read TIER: BLOCKED error message and re-invoke with `--reason "..."` rather than blanket-disable via `--skip-compliance` | Skip rate breaches 12% target; BLOCKED becomes annoyance rather than safety net | Audit log captures both BLOCKED occurrences and subsequent override path; report ratio post-deploy |
| UA-2 | Sprint and cleanup-audit programmatic invokers tolerate the additive `BLOCKED` enum extension without code changes | Downstream parsers break on unrecognized TIER value; sprint phase HALTs cascade | Re-run Wave-4 +3 checkpoint parser tests (RK-15); verify `EXIT_RECOMMENDATION` markers still emitted |
| UA-3 | Operators will not paste credentials/PII into the `--reason "..."` free-text field | Audit log leaks secrets to `.dev/audit/*.jsonl`; downstream consumers exposed | Documentation warning against credential paste (research §10.9); no architectural enforcement [inference TBD on automated PII scrubbing] |

### 10.4 Constraints

| Type | Constraint | Impact on Product | Mitigation |
|------|------------|-------------------|------------|
| **Technology** | STRICT MCP requirement is **fail-closed, no fallback** (Sequential AND Serena required) per `SKILL.md:253-263` | STRICT tasks block when MCP unavailable; cannot proceed; CRITICAL FAIL per TU-001 #1 | Audit-logged `--skip-compliance --reason "..."` operator escape; target <12% usage; document operator runbook |
| **Technology** | Sentinel block `<!-- SC:TASK-UNIFIED:CLASSIFICATION -->` and `--caller task-unified` string preserved verbatim (RELEASE-SPEC §2.1) | Naming artifact carry-over from retired /sc:task-unified lineage cannot be removed in R1; downstream forensic consumers unenumerated (A-005) | DEFER-lock test `test_caller_string_is_canonical` reads canonical form from SoT constant (RELEASE-SPEC §5.2.5); rename deferred to R3 |
| **Technology** | Regression test boundary: 921 sprint pass / 57 fail baseline; 125/125 TUI; 16/16 ClaudeProcess; +3 Wave-4 parser tests (RK-15) per research file 01 §7.2 | Any prompt-construction change in sprint must re-pass Wave-4 checkpoint parser tests; net-new test additions only; no regressions | Pre-merge gate per RELEASE-SPEC §9 item 3; TEST-SPEC.md:34-80 enforces "no `/sc:task-unified` in build_prompt" |
| **Timeline** | R1 ~3-5 dev-days, R2 ~7-10 dev-days; total v3.75 ~10-15 dev-days [inference] (RELEASE-SPEC §7.1) | Effort labels are S/M/L proxies without empirical timing; S could exceed 0.5d | Release split valve per A-003 |
| **Resource** | Skill package today contains only `SKILL.md` + one-line `__init__.py`; no `refs/`, `rules/`, `templates/`, `scripts/`, `config/` (research §1.4) | `audit.py` will be **first executable Python in this skill package**; no scaffolding precedent | Pure-Python stdlib for audit.py (no new dependencies per research §8.2) |
| **Regulatory** | N/A at feature level — reference Platform PRD for SOC 2 / GDPR / CCPA platform obligations | Audit log retention policy and PII handling are feature-scoped (see S17) | Feature-scoped data handling per S17.2 |

---

## 11. Dependencies

### 11.1 External Dependencies

External MCP servers and runtime services per research file `02-architecture-and-integration.md` §3 and §8.3. [DOC-CROSS-VAL: SKILL.md:253-263 / task.md:7]

| Dependency | Type | Owner | Risk Level | Contingency |
|------------|------|-------|------------|-------------|
| Sequential MCP | MCP Server | External (gateway-hosted) | **High** (required by STRICT AND STANDARD; STRICT no-fallback) | STRICT: CRITICAL FAIL per TU-001 #1, audit-logged; STANDARD: fallback allowed with noted limitations |
| Serena MCP | MCP Server | External (gateway-hosted) | **High** (required by STRICT only; **no fallback**) | STRICT: CRITICAL FAIL per TU-001 #1; operator escape `--skip-compliance --reason "..."` (audit-logged, target <12%) |
| Context7 MCP | MCP Server | External (gateway-hosted) | **Medium** (required by STANDARD; fallback allowed) | STANDARD: proceed with fallback; record fallback in audit log even though allowed |
| Auggie / `codebase-retrieval` | MCP Tool Capability | External (any host providing capability) | **Medium** (invoked at STRICT step 3 and STANDARD step 1 per SKILL.md:83,94,269) | Tool referenced by capability name, not server name; resilient to host swap |
| Playwright / Magic / Morphllm MCP | MCP Server | External (gateway-hosted) | **Low** (declared at task.md:7 as available; not required by any tier per §3.2 matrix) | Optional; not on critical path |

### 11.2 Internal Dependencies

Internal modules per research file `02-architecture-and-integration.md` §1 and §9.1. [DOC-CROSS-VAL: task.md:50-100 / SKILL.md:7-9, 76-123]

| Dependency | Type | Owner | Status | Target Date |
|------------|------|-------|--------|-------------|
| `src/superclaude/commands/task.md` | Command file (TEXT-ONLY classification gate) | TBD | Live (v2.0.0; v3.75 plans bump to v2.2.0 per RELEASE-SPEC §1.1) | R1 (v3.75) |
| `src/superclaude/skills/sc-task-protocol/SKILL.md` | Skill file (STANDARD + STRICT execution) | TBD | Live (no NFR section yet; TU-003 designs it) | R1 (v3.75) |
| `src/superclaude/skills/sc-task-protocol/audit.py` | NEW Python module (CriticalFailCondition + JSONL writer) | TBD | **Not yet present in working tree** [UNVERIFIED] | R1 (v3.75) — first executable Python in this skill package |
| `src/superclaude/skills/sc-task-protocol/__init__.py` | Skill package init | TBD | Live (one-line stub per research §1.4) | Unchanged in R1 |
| `.claude/commands/sc/task.md` | Dev copy synced via `make sync-dev` | TBD | Live | Round-trips with src/ per CLAUDE.md sync rules |
| `.dev/audit/sc-task-{YYYY-MM-DD}.jsonl` | Daily-rotated audit log file | TBD | **Spec-only; directory does not exist yet** | R1 (v3.75) |
| `src/superclaude/core/ORCHESTRATOR.md` | Tier classification decision tree (lines 151-213) | TBD | Live | Unchanged in R1 |
| `src/superclaude/core/COMMANDS.md` | Full 8-flag inventory (lines 86-119) | TBD | Live | Unchanged in R1 |

### 11.3 Cross-Team Dependencies

Cross-team integration surfaces per research file `02-architecture-and-integration.md` §5, §6, and §9. [DOC-CROSS-VAL: cli/sprint/process.py:170 / cli/cleanup_audit/prompts.py / SKILL.md:191-197]

| Team | Dependency | What We Need | When Needed | Status |
|------|------------|--------------|-------------|--------|
| Sprint Executor team (TBD) | `ClaudeProcess.build_prompt` at `src/superclaude/cli/sprint/process.py:170` emits `/sc:task Execute all tasks in @{phase_file} --compliance strict --strategy systematic` | Tolerance of additive BLOCKED enum without prompt changes; Wave-4 +3 checkpoint parser tests (RK-15) must re-pass | R1 ship boundary | Live; SE-001 fail-closed gate, SE-002+SE-003 sub-phase resume are R2 scope |
| Cleanup-Audit Prompt Builders team (TBD) | Five prompt builders at `src/superclaude/cli/cleanup_audit/prompts.py` (lines 20, 41, 64, 87, 111) emitting `/sc:task` without `--compliance` flag (auto-classification) | Auto-classification routes to EXEMPT or STANDARD — NOT STRICT; audit log captures tier for detection if STRICT routing happens unexpectedly | R1 ship boundary | Live; no changes required in R1 |
| Forensic Skill team (TBD) | `/sc:forensic --tier {tier} --intent triage --caller task-unified --context {context_path} --output {output_dir} --depth quick` per `SKILL.md:191-197` | Enumerate consumers of `--caller task-unified` string (A-005 validation); confirm canonical form preserved | R3 (rename release) — DEFERRED in R1 | DEFER-locked; `test_caller_string_is_canonical` reads from SoT constant |
| Quality-Engineer Agent team (TBD) | Sub-agent spawned at STRICT step 9 per `SKILL.md:80-91`; consumes ~3-5K tokens, 60s timeout | TU-003 six-principle NFR checklist with citation field per row; verification artifact contract | R1 ship boundary | Verification artifact surface TBD per research §10.5 (Q14 enforcement mechanism not finalized) |
| Tasklist Generator team (TBD) | `sc-tasklist-protocol/SKILL.md:505-575` parallel classification logic (superset of /sc:task STRICT keywords) | TU-005 SoT YAML consolidation to eliminate drift | R3 — DEFERRED in R1 | DEFER-COUPLED; drift remains in v3.75 |

---

## 14. Technical Requirements

### 14.1 Architecture Requirements

Sourced from research file `02-architecture-and-integration.md` §1 and §2. [DOC-CROSS-VAL: task.md:50-100 / SKILL.md:7-9, 76-123 / RELEASE-SPEC §3.3, §3.7]

| Requirement | Description | Rationale |
|-------------|-------------|-----------|
| Command-Skill Architectural Split | `task.md` performs **TEXT-ONLY classification** (no tool calls allowed pre-header per task.md:50-56); `SKILL.md` performs **execution only** for STANDARD and STRICT tiers per SKILL.md:7-9. LIGHT and EXEMPT bypass the skill entirely per task.md:97-98. | Two-layer separation enforced via natural-language instructions, not runtime gatekeepers; the load-bearing contract is the classification header sentinel block. Downstream parsers (sprint, cleanup-audit, telemetry) rely on the sentinel. |
| audit.py Module Introduction | NEW Python module `src/superclaude/skills/sc-task-protocol/audit.py` containing `CriticalFailCondition` dataclass + JSONL writer + per-task write lock. First executable Python in the skill package. | TU-001 CRITICAL FAIL trail, TU-004 BLOCKED override audit, Q11 `--skip-compliance` metering all share this surface (research §2.1). |
| Classification Header Sentinel Preservation | Sentinel `<!-- SC:TASK-UNIFIED:CLASSIFICATION -->` (open/close paired at task.md:60,66,108,114,119,125,130,136,141,147) preserved verbatim per RELEASE-SPEC §2.1. | Carry-over from retired `/sc:task-unified` lineage; downstream forensic consumers unenumerated (A-005); rename DEFER-locked to R3. |
| STRICT MCP Fail-Closed Circuit Breaker | If Sequential OR Serena MCP unavailable for STRICT, block task execution per SKILL.md:259-263; TU-001 elevates this to programmatic `CriticalFailCondition(always_blocks=True)` checked at task entry AND after each turn. | Fail-closed semantics for safety-critical tasks; audit-log captures every block; operator escape via `--skip-compliance --reason "..."`. |
| Additive BLOCKED TIER Enum Extension | TIER enum extended from `[STRICT\|STANDARD\|LIGHT\|EXEMPT]` to `[STRICT\|STANDARD\|LIGHT\|EXEMPT\|BLOCKED]` per RELEASE-SPEC §2.4:143-145; additive only, no removal. | TU-004 replaces soft `<0.70 confidence` prompt with deterministic BLOCKED state + halt + explicit override path. |
| Per-Task UID Stability for Sub-Phase Resume | `task_id: "uuid"` field in JSONL schema (research §2.3) must be stable across sub-phase resume for SE-003 (sprint-side, R2 scope). | Enables sub-phase resume without losing audit continuity; cross-task ordering is timestamp-based but not strictly serial. |

### 14.2 Performance Requirements

Sourced from research file `02-architecture-and-integration.md` §3.5 and research file `01-features-and-user-flows.md` §3 + §7.1. [DOC-CROSS-VAL: SKILL.md:114-119, 240-244, 349-357]

| Metric | Target | Measurement Method |
|--------|--------|-------------------|
| Classification overhead | Header emission is FIRST output, TEXT-ONLY (no tool calls); negligible token cost vs. tool invocation | Execution telemetry; STRICT overhead target <25% per SKILL.md:349-357 |
| STANDARD verification | 300-500 tokens, 30s timeout (direct test execution) per SKILL.md:114-119 | Per-task token accounting in audit log |
| STRICT verification | 3-5K tokens, 60s timeout (sub-agent quality-engineer) per SKILL.md:114-119 | Per-task token accounting in audit log |
| TFEP escalation budget | 1st trigger ~5-8K tokens (`--tier light`); 2nd trigger ~15-20K tokens (`--tier standard`); 3rd trigger FULL STOP | SKILL.md:240-244; audit log captures escalation_count |
| STRICT MCP latency budget | Sequential + Serena required (no fallback); circuit-breaker check at task entry AND after each turn | TU-001 programmatic check; failures recorded with `critical_fail` field in JSONL |
| Audit log write latency | Per-task single-writer-serialized; cross-task timestamp-only ordering (research §2.4) | INV-005 mitigation; per-task write lock; downstream consumers tolerate timestamp-only ordering |

### 14.3 Security Requirements

Sourced from research file `02-architecture-and-integration.md` §2.5 and §10.9. [DOC-CROSS-VAL: RELEASE-SPEC §3.7]

| Requirement | Implementation | Compliance |
|-------------|----------------|------------|
| Audit log no-PII guarantee | JSONL schema contains only: ISO timestamp, task UUID, tier enum, numeric confidence, boolean flags, free-text `reason` string. `reason` is the ONLY free-text field. Implementation MUST avoid logging arguments, file contents, or environment variables. | Feature-scoped; no architectural enforcement on `--reason` content (research §10.9); documentation warning required |
| Append-only audit log | `.dev/audit/sc-task-{YYYY-MM-DD}.jsonl`; daily rotation; append-only mode | Tamper-resistant audit trail; preserves forensic chain-of-custody |
| Per-task write lock | Writes within a single task lifecycle MUST be serialized through a single writer (INV-005 mitigation) | Prevents interleaved partial JSONL entries; cross-task ordering relaxed to timestamp-only |
| Critical-path override (STRICT escalation) | Paths `auth/`, `security/`, `crypto/`, `models/`, `migrations/` always trigger CRITICAL verification regardless of computed tier per SKILL.md:121-123 | Defense-in-depth; preserved unchanged in v3.75 |

### 14.4 Scalability Requirements

Sourced from research file `02-architecture-and-integration.md` §2.4, §5, and §9. [DOC-CROSS-VAL: cli/sprint/process.py:170 / cli/cleanup_audit/prompts.py]

| Dimension | Current Target | Future Target | Approach |
|-----------|----------------|---------------|----------|
| Per-task UID stability | UUID per task lifecycle; stable across all audit entries for that task | Stable across sub-phase resume (SE-003, R2 scope) | UUID generated at task entry; persisted in audit log; reused on resume |
| Audit log file size | Daily rotation at `.dev/audit/sc-task-{YYYY-MM-DD}.jsonl` | Retention policy TBD [inference] (see S17) | Daily file rotation key derived from ISO timestamp |
| Concurrent task throughput | Per-task write lock; cross-task ordering timestamp-based | N/A — not globally serialized | Downstream consumers tolerate timestamp-only ordering across tasks |
| Sprint phase volume | Sprint emits `/sc:task` per phase via `build_prompt`; 921 sprint pass / 57 fail regression baseline | Sub-phase resume in R2 changes prompt construction (RK-15: +3 Wave-4 parser tests required) | Re-run Wave-4 checkpoint parser tests on any prompt change |
| Cleanup-audit pass volume | 5 sequential `/sc:task` invocations per audit run (surface → structural → cross-cutting → consolidation → validation) | Unchanged in R1 | YAML frontmatter contracts + `EXIT_RECOMMENDATION` sentinel chaining |

### 14.5 Data & Analytics Requirements

Sourced from research file `02-architecture-and-integration.md` §2.2 and §2.3. [DOC-CROSS-VAL: RELEASE-SPEC §3.3, §3.7]

| Data Type | What to Collect | Why | Storage/Retention |
|-----------|-----------------|-----|-------------------|
| Audit log entry | JSONL: `ts`, `task_id`, `tier`, `confidence`, `user_override_tier`, `skip_compliance`, `force_strict`, `reason`, `critical_fail` | TU-001 audit trail; TU-004 BLOCKED override audit; Q11 `--skip-compliance` metering (<12% target) | `.dev/audit/sc-task-{YYYY-MM-DD}.jsonl`; append-only; daily rotation; retention policy [inference TBD per S17] |
| CriticalFailCondition record | Dataclass: `condition_type` (str), `description` (str), `always_blocks` (bool=True) | Three canonical STRICT-only conditions: (1) Sequential or Serena MCP unavailable, (2) Output file absent after max_turns, (3) Classification header absent | In-memory dataclass; serialized into `critical_fail` JSONL field on trigger |
| Tier classification telemetry | TIER value + CONFIDENCE numeric + KEYWORDS matched + OVERRIDE boolean + RATIONALE one-liner | Tier classification accuracy ≥80% target per SKILL.md:349-357; user confusion <10% | Embedded in classification header sentinel block; emitted as FIRST output |
| TFEP escalation telemetry | escalation_count (int 1→2→FULL STOP); forensic outcome (success/partial/failed) | Skip rate <12%, regression prevention ≥85%, STRICT overhead <25% per SKILL.md:349-357 | Audit log JSONL; tfep-incident-report.md committed to git alongside forensic artifacts |

**Analytics Tools:**
- Audit log JSONL daily files — primary analytics surface
- Reporting/dashboard layer — TBD per research §10.6 (Q11 metering "collects but no consumer/dashboard specified")

---

## 15. Technology Stack

Sourced from research file `02-architecture-and-integration.md` §8. [DOC-CROSS-VAL: pyproject.toml / CLAUDE.md]

### 15.1 Backend

| Layer | Technology | Version | Notes |
|-------|------------|---------|-------|
| Language | Python | ≥3.10 | Per `pyproject.toml`; PEP 517 build via hatchling |
| Runtime / Package Manager | UV | N/A | All Python operations via UV — no `python -m`, no `pip install`, no bare `python script.py` per CLAUDE.md |
| Package name | superclaude | 4.2.0 | Skill file claims `version: "2.0.0"` for `/sc:task` command; v3.75 plans bump to 2.2.0 |
| Test runner | pytest | ≥7.0.0 | Auto-loaded plugin; pm_agent fixtures (`confidence_checker`, `self_check_protocol`, `reflexion_pattern`, `token_budget`, `pm_context`) |
| CLI | click | ≥8.0.0 | Sprint, roadmap, tasklist, audit subcommands |
| TUI / output | rich | ≥13.0.0 | Sprint/cleanup-audit TUI rendering |
| Data classes | stdlib `dataclasses` | N/A | `CriticalFailCondition`, models |
| JSONL I/O | stdlib `json` | N/A | Audit log persistence |
| Concurrency | stdlib `threading` / file lock | N/A | Per-task audit write lock |
| Subprocess | stdlib `subprocess` | N/A | Sprint `git diff --stat`, `claude --print --verbose` |
| Datetime | stdlib `datetime` | N/A | ISO-8601 timestamps, daily rotation key |

### 15.2 Frontend

N/A — this is a CLI/skill feature; no frontend layer. Reference Platform PRD for any UI surfaces.

### 15.3 Infrastructure

MCP servers (external runtime requirements per research §8.3):

| Component | Technology | Notes |
|-----------|------------|-------|
| MCP Server (Sequential) | Sequential MCP | Token-efficient multi-step reasoning; STRICT + STANDARD tier requirement |
| MCP Server (Serena) | Serena MCP | Symbol navigation, session memory; STRICT-only requirement (no fallback) |
| MCP Server (Context7) | Context7 MCP | Official library/framework docs; STANDARD requirement (fallback allowed) |
| MCP Tool Capability (Auggie) | `codebase-retrieval` | Tool capability invoked at STRICT step 3 and STANDARD step 1 (SKILL.md:83,94,269); resilient to host swap |
| MCP Server (Playwright) | Playwright MCP | Optional per task.md:7 declaration; not required by any tier |
| MCP Server (Magic) | Magic MCP | Optional per task.md:7 declaration; not required by any tier |
| MCP Server (Morphllm) | Morphllm MCP | Optional per task.md:7 declaration; not required by any tier |
| Audit log filesystem | `.dev/audit/` directory | Daily-rotated JSONL files; canonical generated-artifact root per CLAUDE.md |
| Build pipeline | Makefile | `make dev` (editable install), `make sync-dev` (src/→.claude/), `make verify-sync` (CI gate), `make test`, `make lint`, `make format` |

---

## 17. Legal & Compliance Requirements

> **Scope note:** This is a feature-scoped PRD. Platform-level SOC 2 / GDPR / CCPA / EU AI Act obligations are deferred to the Platform PRD. The items below cover only feature-specific data handling.

### 17.1 Regulatory Compliance

Reference Platform PRD for SOC 2, GDPR, CCPA, EU AI Act, and other platform-level compliance obligations. No feature-scoped regulatory requirements identified in research files.

### 17.2 Data Privacy (Feature-Scoped)

Sourced from research file `02-architecture-and-integration.md` §2.5 and §10.9. [DOC-CROSS-VAL: RELEASE-SPEC §3.7]

| Data Type | Collection Purpose | Retention | User Rights |
|-----------|-------------------|-----------|-------------|
| Audit log entry (JSONL) | TU-001 CRITICAL FAIL trail; TU-004 BLOCKED override audit; Q11 `--skip-compliance` metering (<12% target) | Daily-rotated files at `.dev/audit/sc-task-{YYYY-MM-DD}.jsonl`; retention policy [inference TBD] | Reference Platform PRD for user data rights |
| Audit log fields | **No PII by design** — schema contains only: ISO timestamp, task UUID (non-correlatable), tier enum, numeric confidence, boolean flags, evidence/condition paths | Same as parent JSONL file | N/A — no user-identifiable content |
| `reason` free-text field | User-supplied justification for override (`--compliance`, `--skip-compliance`, `--force-strict`) | Same as parent JSONL file | User MUST avoid pasting credentials/PII; documentation warning required per research §10.9; no architectural enforcement [inference TBD on automated PII scrubbing] |

### 17.3 Terms & Policies Required

- [ ] Reference Platform PRD for Terms of Service
- [ ] Reference Platform PRD for Privacy Policy
- [ ] Reference Platform PRD for Acceptable Use Policy
- [ ] Reference Platform PRD for Data Processing Agreement (DPA)
- [ ] Feature-scoped: Audit log retention policy [inference TBD]
- [ ] Feature-scoped: Operator runbook warning against PII in `--reason` field

---

## 18. Business Requirements

> **Scope note:** This is a feature-scoped PRD. The feature is part of the SuperClaude platform and does NOT have independent pricing or GTM. The section below contains only feature-specific cost notes. Reference Platform PRD for pricing, GTM, and support requirements.

### 18.1 Monetization Strategy

N/A — feature-scoped. Reference Platform PRD for pricing tiers, GTM, and support SLAs.

### 18.2 Feature-Specific Cost Notes

Sourced from research file `02-architecture-and-integration.md` §3 and research file `01-features-and-user-flows.md` §7. [DOC-CROSS-VAL: SKILL.md:114-119, 240-244]

| Cost Driver | Description | Impact |
|-------------|-------------|--------|
| Additional Sequential MCP calls per STRICT task | STRICT tier requires Sequential MCP (no fallback); STANDARD also requires Sequential (fallback allowed) | Token-cost impact [inference S] — small per-task overhead; aggregate scales with STRICT task volume |
| Additional Serena MCP calls per STRICT task | STRICT tier requires Serena (no fallback) for symbol navigation + session memory | Token-cost impact [inference S] — aggregate scales with STRICT task volume |
| Audit log filesystem cost | Daily-rotated JSONL files at `.dev/audit/` | Negligible per task (~10 fields per entry); retention policy [inference TBD] caps long-term storage |
| TFEP forensic escalation | 1st trigger ~5-8K tokens; 2nd trigger ~15-20K tokens; 3rd FULL STOP per SKILL.md:240-244 | Bounded escalation budget; FULL STOP prevents runaway costs |
| BLOCKED state user re-invocation | TU-004 BLOCKED halts; user re-invokes with `--reason "..."` | Per RELEASE-SPEC §2.2:120 [inference] ~5-10% of `--compliance auto` users encounter BLOCKED; doubles invocation count for that segment |

### 18.3 Go-to-Market Strategy

N/A — feature-scoped. Reference Platform PRD.

### 18.4 Support Requirements

N/A — feature-scoped. Reference Platform PRD.

---

## 20. Risk Analysis

### 20.1 Technical Risks

Sourced from RELEASE-SPEC §6 (RK-01..RK-18 risks) and FINAL-REPORT §7 (3 assumption-derived risks) per research file `02-architecture-and-integration.md` §7 and §9.5. [DOC-CROSS-VAL: RELEASE-SPEC §6 / FINAL-REPORT §7, §10]

| Risk ID | Risk | Probability | Impact | Mitigation | Contingency |
|---------|------|-------------|--------|------------|-------------|
| RK-03 | STRICT-required MCP servers (Sequential + Serena) unavailable → STRICT cannot proceed | M | H | Audit-log skip-compliance metering (Q11 target <12%); document operator escape `--skip-compliance --reason "..."` | Operator runbook; CRITICAL FAIL audit entry; manual reclassify to STANDARD if appropriate |
| RK-04 | `--skip-compliance` usage currently unmetered; cannot detect abuse | M | M | Q11 audit log infrastructure captures `skip_compliance` boolean per task | Post-deploy telemetry review; tighten thresholds if >12% |
| RK-05 | Tasklist-protocol parallel classification logic drift from `/sc:task` (4-file drift surface) | H | M | TU-005 DEFER-COUPLED to R3 (SoT YAML consolidation) | v3.75 leaves drift; documentation note; R3 consolidates via `config/tier-keywords.yaml` |
| RK-10 | Q2 forensic-caller rename (`--caller task-unified`) breaks downstream forensic consumers | M | H | DEFER-locked to R3; A-005 forensic-consumer enumeration required first; `test_caller_string_is_canonical` reads from SoT constant | Rename mechanical when SoT constant updates; non-breaking by construction |
| RK-15 | Sprint sub-phase resume (SE-003, R2) changes `build_prompt` construction and breaks Wave-4 checkpoint parser tests | M | H | Re-run Wave-4 +3 checkpoint parser tests on any prompt change; TEST-SPEC.md:34-80 enforces "no `/sc:task-unified` in build_prompt" | Block merge until parser tests pass; revert if regression |
| RK-18 | `SKILL.md:359-365` references 5 config files (`config/tier-keywords.yaml`, `config/verification-routing.yaml`, `config/tier-acceptance-criteria.yaml`, `MCP.md`, `ORCHESTRATOR.md`) that do not exist | H | L | TU-006 DEFER to R3; v3.75 leaves broken | Documentation path-correct in same release as Q7 [inference per research §10.2] |
| INV-005 | audit.py file I/O failure on daily rotation boundary | L | M | Per-task write lock; cross-task ordering timestamp-based but not strictly serial | Single-writer-per-task contract; downstream consumers tolerate timestamp-only ordering |
| RK-A-005 | A-005 forensic-consumer audit gap — `--caller task-unified` consumed by `/sc:forensic` but no draft verified what `/sc:forensic` does with it | H | H | Implementation phase must enumerate `/sc:forensic` consumers before any rename in R3; DEFER-lock tests encode SoT constants | Block R3 rename until A-005 validated; v3.75 preserves verbatim |
| RK-TU-001-cond2 | TU-001 condition #2 (empty STRICT output → FAIL) not present in source today | M | M | RELEASE-SPEC §3.3 designs net-new for v3.75; implementation phase adds | Block R1 ship until coded; tests at `tests/skills/test_task_protocol_critical_fail.py` |
| RK-TU-001-cond3 | TU-001 condition #3 (missing STRICT classification header → FAIL) not present in source today | M | M | RELEASE-SPEC §3.3 designs net-new for v3.75; implementation phase adds | Block R1 ship until coded; same test surface |
| RK-TU-003-NFR | TU-003 six-principle NFR section not present in `SKILL.md` today | M | M | RELEASE-SPEC §3.4 designs the NFR; implementation phase adds via prompt + checklist (Q14 (c) both) | Audit log captures checklist completeness; rollback hook if adoption unsound |
| RK-TU-004-BLOCKED | TU-004 BLOCKED state not present in source today; ~5-10% of `--compliance auto` users will see new halt behavior [inference] | M | M | Release notes call out change; migration guide; clear error message pointing to override paths | Audit log captures BLOCKED frequency; tighten/loosen 0.70 threshold if telemetry shows misfit |
| RK-TU-007 | TU-007 canonical completion checklist count is [inference]; LW-source verification required before merge | M | H | Pre-merge gate: investigation completes; either confirms list matches LW original OR supplies canonical list; parameterized tests handle any count (5/6/7/8) | Block merge until `docs/tu-007-completion-checklist-verification.md` published |
| RK-Q11-reporting | Audit log captures but no consumer/dashboard specified | H | L | Implementation "collects but no reporting layer defined" [inference per research §10.6] | Reporting layer TBD post-deploy |
| RK-Q5-UX | BLOCKED state UX (CLI prompt format) not pinned per research §10.7 | M | L | Header schema covers telemetry side (b); CLI prompt format is implementation choice (a) | Implementation choice; iterate post-deploy if friction high |
| RK-cleanup-audit-auto | Cleanup-audit auto-classification (no `--compliance` flag) could keyword-match STRICT on future audit pass (e.g., "authorization") | L | M | Audit log captures tier so unexpected STRICT routing is detectable | Currently routes to EXEMPT or STANDARD (read-only/analysis); monitor via audit log |
| RK-skill-package-Python | audit.py will be FIRST executable Python in `sc-task-protocol/` (no scaffolding precedent) | L | M | Pure-Python stdlib (no new dependencies); test coverage 100% on audit.py (security-sensitive write path) per RELEASE-SPEC §5.7 | Block ship if coverage <100% |
| RK-no-PII-reason | `reason` free-text field could leak PII or secrets if user pastes them | M | M | Documentation warning against pasting credentials/PII into `--reason`; not architecturally enforced | Operator training; [inference TBD on automated PII scrubbing] |
| RK-A-001-load | A-001 (STRICT MCP block axiom) load-bearing assumption not validated | L | H | Audit-log skip-compliance metering provides real-world validation; RK-03 mitigations presume A-001 stays | If skip rate breaches 12% target, revisit A-001 fundamentally |
| RK-A-002-scope | A-002 (closed candidate set at Wave-1 extracts) — novel additions force replan | L | M | Closed-set enforcement at release boundary; novel items go to R3 or later | Re-open scope only on critical defect; no scope creep mid-release |
| RK-A-003-effort | A-003 (S/M/L effort labels reliable without estimation) — tasks marked S could exceed budget | M | M | Release split (R1 task-side / R2 sprint-side) provides pressure-release valve | Re-scope R2 if R1 overruns; trim TUI bundle if needed |

### 20.2 Business Risks

| Risk | Probability | Impact | Mitigation | Contingency |
|------|-------------|--------|------------|-------------|
| BLOCKED state user friction exceeds budget (>10% of `--compliance auto` users) | M | M | Migration guide; release notes call-out; `--compliance auto` users see change first; clear error message with override path | Tighten/loosen 0.70 confidence threshold via post-deploy telemetry; revisit if friction sustained |
| `--skip-compliance` skip rate breaches 12% target | M | M | Q11 audit log infrastructure; reporting layer TBD | Operator training; tighten STRICT keyword scoring if root cause is over-classification |
| Sprint-side STRICT failure cascades affect downstream consumers (cleanup-audit, tasklist) | L | H | SE-001 fail-closed semantics (sprint-side, R2 scope); `EXIT_RECOMMENDATION: HALT` propagation | Audit log + tfep-incident-report.md provide forensic trail; manual recovery runbook |

### 20.3 Operational Risks

| Risk | Probability | Impact | Mitigation | Contingency |
|------|-------------|--------|------------|-------------|
| Two-tree sync (`src/superclaude/` ↔ `.claude/`) drift on audit.py introduction | L | M | `make sync-dev` + `make verify-sync` CI gate per CLAUDE.md | Block merge if `verify-sync` fails |
| Daily rotation boundary file-creation race | L | L | Per-task write lock; daily rotation key derived from ISO timestamp | Append-only mode tolerates same-second creates by different tasks |
| Forensic incident report (`tfep-incident-report.md`) commits diverge from audit log JSONL | L | L | Both committed to git alongside forensic artifacts (research §4.7) | Cross-reference via task_id UUID |

---

## 26. Contributors & Collaboration

### 26.1 Document Contributors

Person names TBD pending PRD finalization. Roles aligned with PRD template ownership conventions.

| Role | Name | Contribution |
|------|------|--------------|
| Product Owner | TBD | Product vision, user stories, business requirements, scope decisions for v3.75 split |
| Engineering Lead | TBD | Technical architecture (command-skill split, audit.py contract, MCP matrix), feasibility assessment of A-005 forensic-consumer investigation |
| Design Lead | TBD | UX flows for BLOCKED state CLI prompt (Q5 (a)), accessibility/error-message design |
| QA Lead | TBD | Acceptance criteria, TFEP test surface, regression baseline maintenance (921 sprint pass / 57 fail; 125/125 TUI; 16/16 ClaudeProcess; +3 Wave-4) |
| Sprint Executor Owner | TBD | `ClaudeProcess.build_prompt` consumer; Wave-4 checkpoint parser test custodian (RK-15) |
| Cleanup-Audit Owner | TBD | Five-prompt-builder consumer; auto-classification routing review |
| Forensic Skill Owner | TBD | `/sc:forensic --caller task-unified` consumer enumeration for A-005 validation |
| Tasklist Generator Owner | TBD | `sc-tasklist-protocol/SKILL.md:505-575` parallel classification drift custodian; TU-005 R3 consolidation lead |
| Stakeholders | TBD | Release approval, sign-off on RELEASE-SPEC §9 9-item acceptance checklist |

### 26.2 How to Contribute

- **Comment inline** for questions, suggestions, or clarifications on tier classification, MCP matrix, or audit log schema.
- **Tag relevant team members** using @ mentions per role assignments above.
- **Update Open Questions table** when A-005 forensic-consumer enumeration completes, when Q14 enforcement mechanism is finalized, when Q11 reporting layer is specified, when BLOCKED state UX (Q5) is pinned, or when audit log retention policy is set.
- **Link related documents**: RELEASE-SPEC.md, FINAL-REPORT.md, TEST-SPEC.md, context-task-current-state.md, RIGORFLOW source extracts.
- **Review quarterly** and flag outdated sections — especially the `[inference]` markers (TU-007 condition count, TU-004 user-impact 5-10%, S/M/L effort labels, R3/R4 target windows) when telemetry data becomes available.
- **Carry-over preservation rule**: Do NOT remove `<!-- SC:TASK-UNIFIED:CLASSIFICATION -->` sentinel or `--caller task-unified` string in R1; both DEFER-locked to R3 pending A-005 validation.

---

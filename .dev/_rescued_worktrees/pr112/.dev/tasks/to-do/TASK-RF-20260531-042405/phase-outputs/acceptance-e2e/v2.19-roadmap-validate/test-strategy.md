---
complexity_class: MEDIUM
validation_philosophy: continuous-parallel
validation_milestones: 5
work_milestones: 5
interleave_ratio: 1:2
major_issue_policy: stop-and-fix
spec_source: spec-roadmap-validate.md
generated: "2026-06-03T03:22:53.066490+00:00"
generator: superclaude-roadmap-executor
---

# Test Strategy — `superclaude roadmap validate` Subcommand

## Issue Classification

| Severity | Action | Gate Impact |
|---|---|---|
| CRITICAL | stop-and-fix immediately | Blocks current milestone |
| MAJOR | stop-and-fix before next milestone | Blocks next milestone |
| MINOR | Track and fix in next sprint | No gate impact |
| COSMETIC | Backlog | No gate impact |

Major-issue policy is **stop-and-fix**: any MAJOR finding halts forward progress and must be resolved before the next milestone gate opens. CRITICAL findings halt the in-flight milestone immediately.

## 1. Validation Milestones Mapped to Roadmap Milestones

Five validation milestones (V1–V5) are defined, each paired 1:1 with a roadmap work milestone. This is the continuous-parallel philosophy: validation runs alongside every milestone rather than being batched at the end. The MEDIUM 1:2 cadence is the *floor*; pairing each milestone with a validation gate exceeds it deliberately because the highest-error surface (M3 executor) and the architecture invariant (NFR-050.2, live from M1) cannot tolerate deferred verification.

**V1 ↔ M1: Config & Type Contracts** | runs Week 1 | gate = type contracts + import-scan green
Validates `ValidateConfig` inheritance, DM-002..DM-007 type contracts, COMP-009/010 resolvers, and the day-one import-scan architecture test (NFR-050.2).

**V2 ↔ M2: Gates & Prompts** | runs Week 2 | gate = gate-criteria + 7-dimension prompt unit assertions
Validates REFLECT_GATE / ADVERSARIAL_MERGE_GATE field sets, the `.gates` import identity (no duplication, W-001), 7-dimension reflect prompt, and merge-category enumeration.

**V3 ↔ M3: Executor & Step Dispatch** | runs Weeks 3–4 | gate = single/multi dispatch + merge + OPS-003 artifact policy
Highest-risk validation: list-of-1 vs list-of-N layout, parallel-reflect→sequential-merge ordering, agreement-table emission, count recalculation, gate-failure warn-and-continue.

**V4 ↔ M4: CLI Integration & Auto-Invocation** | runs Week 5 | gate = standalone + auto-invoke + resume dispatch + non-blocking exit
Validates subcommand registration, `--no-validate`, flag inheritance, COMP-016 resume completion-vs-halt, missing-file UX, and the never-exit-non-zero contract.

**V5 ↔ M5: Testing, Performance & Hardening** | runs Weeks 6–7 | gate = full matrix green + wall-time + false-positive precision
Terminal validation: all named tests (TEST-001..013), ≤2 min single-agent wall time, zero forbidden imports re-scanned, false-positive precision against fixtures.

## 2. Test Categories

**Unit** — pure-function and contract assertions, no subprocess: `ValidateConfig` construction; REFLECT_GATE/ADVERSARIAL_MERGE_GATE field sets (TEST-005/006); `_build_validate_steps` layout (TEST-001/002); prompt-content checks (TEST-007/008); `_has_agreement_table`, `_frontmatter_values_non_empty` import-identity. Fast, deterministic, run on every commit.

**Integration** — multi-module wiring with subprocess mocked/simulated: auto-invoke hook (TEST-003/004); dry-run plan printing without subprocess launch (TEST-009); missing-file error exit (TEST-010); gate-failure warn-and-continue + resume edges (TEST-013); flag inheritance into `ValidateConfig`.

**E2E** — real (or deterministically simulated) Claude subprocess against fixture artifacts: E2E#1 single-agent full run writes `validate/validation-report.md`; E2E#2 multi-agent produces `reflect-opus-architect.md` + `reflect-haiku-architect.md` + merged report with `## Agent Agreement Analysis`; E2E#3 injected duplicate deliverable-ID surfaces exactly one `B-xxx`.

**Acceptance** — the 10 success criteria + 3 additional gates from extraction, mapped to milestones below. Acceptance is met when every criterion's named validation method passes against the owning milestone.

**Architecture/CI** — the static import-scan (NFR-050.2) is a standing gate from M1 across all `pipeline/*` modules; re-run on the full module set in M5.

**Performance** — NFR-050.1 wall-time fixture: single-agent ≤2 min and ≤10% of pipeline wall time, per-step `timeout_seconds=300` honored.

## 3. Test-Implementation Interleaving Strategy

**Ratio: 1:2 (MEDIUM)** — the complexity-class-mandated floor is one dedicated validation milestone per two work milestones. The roadmap is a strictly linear layered chain (types → gates/prompts → executor → CLI → tests), so a back-loaded "test everything in M5" approach would let contract drift and the import-invariant regression accumulate undetected across four milestones before discovery — exactly the failure mode this feature exists to prevent.

**Justification for exceeding the floor to 1:1 continuous-parallel:** Two surfaces forbid deferral. (a) NFR-050.2's one-directional import rule is built day-one in M1 and re-run as a standing CI gate — it cannot wait for M5. (b) M3 carries the feature's highest error density (subprocess orchestration, dual dispatch path) and is explicitly sized with slack; validating it only after M4 wiring would conflate executor defects with CLI defects. Therefore each milestone ships its own unit/contract tests (TEST-005/006/007/008 land in M2 with the code they assert; TEST-001/002 land with the M3 dispatch logic), and M5 runs the *integration + E2E + performance + precision* layer that genuinely requires the assembled feature. Test scaffolding is never back-loaded — the interleave dimension (FR-050.5e) the feature itself enforces would flag that as a WARNING.

**Cadence:** unit tests authored in the same milestone as their target deliverable; integration tests authored in M4–M5 once wiring exists; E2E + performance + precision concentrated in M5 where full assembly is required.

## 4. Risk-Based Test Prioritization

Priority is set by the roadmap risk register (probability × impact), tested highest-first:

**P0 — High impact, must-pass-before-merge**
- R-01 false positives (High/Medium) → NFR-IMP-2 clean-fixture zero-BLOCKING + injected-defect exactly-one-B-xxx; adversarial BOTH_AGREE cross-check verified in E2E#2.
- R-02 circular-dependency regression (High/Medium) → NFR-050.2 import-scan, live from M1, re-scanned M5.
- R-11 silent miss of real BLOCKING via warn-don't-fail (Medium/Medium) → NFR-IMP-1 enumerates B-IDs + `tasklist_ready:false`, exit 0.

**P1 — Medium impact, gate-blocking within milestone**
- R-06 subprocess non-determinism / malformed frontmatter → TEST-013 malformed→gate-fails→warn→exit 0, report marked incomplete.
- R-09 mode divergence (NFR-050.5) → TEST-001/002 single vs multi layout guard.
- R-08 N≥3 merge layout unspecified → OQ-005 resolved before FR-050.3 coding; merge-category test (TEST-008).
- R-14/R-15 wall-time breach + resume/gate-failure edges → NFR-050.1 perf fixture; COMP-016 resume dispatch via TEST-013 resume coverage.

**P2 — Low impact, single targeted test**
- R-12 missing-file UX → TEST-010 clear-error exit.
- R-07 CONFLICT over-blocking → evidence-eval assertion before escalation.
- R-03 config inheritance drift → integration test against real `PipelineConfig`.

## 5. Acceptance Criteria per Milestone

**V1 (M1)** | exit: foundation contracts frozen
- `ValidateConfig` instantiable, extends `PipelineConfig`, all derived paths correct.
- DM-002..DM-007 contracts documented; COMP-009 filename resolver (`reflect-{agent.id}.md`) + duplicate-spec policy defined; COMP-010 model-precedence documented.
- NFR-050.2 import-scan green; zero `validate_*` imports in `pipeline/*`.
- OQ-001 + OQ-004 resolved.

**V2 (M2)** | exit: gates + prompts unit-asserted
- TEST-005: REFLECT_GATE = `[blocking_issues_count, warnings_count, tasklist_ready]`, min_lines 20, tier STANDARD.
- TEST-006: ADVERSARIAL_MERGE_GATE adds `validation_mode`, `validation_agents`, min_lines 30, tier STRICT, `has_agreement_table` check.
- TEST-007: reflect prompt enumerates all 7 dimensions, each severity-classified; "be thorough but precise" present.
- `_frontmatter_values_non_empty` imported from `.gates` (identity asserted, not duplicated).
- OQ-002/003/005/007 resolved.

**V3 (M3)** | exit: dispatch + merge + artifact policy proven
- TEST-001: agents=1 → exactly 1 step, id `reflect`, output `validation-report.md`.
- TEST-002: agents=2 → parallel reflect group → adversarial-merge; per-agent reflect outputs present.
- FR-050.7: merge emits `## Agent Agreement Analysis`, recalculates `blocking_issues_count` + `tasklist_ready` from merged findings.
- OPS-003: gate-failure warns-not-exits; missing report → `tasklist_ready:false` + "unknown"; partial → marked incomplete.
- NFR-050.5: no mode branch outside list-length; OQ-006 resolved.

**V4 (M4)** | exit: CLI + auto-invoke + resume wired
- FR-050.1/NFR-050.3: `roadmap validate <dir>` runs standalone; validates presence of all 3 input files.
- TEST-003/004: `--no-validate` skips; default run auto-validates once on success.
- FR-050.4a: pipeline halt → validation skipped; resume-with-passing-gates → validation runs (COMP-016 explicit dispatch).
- FR-050.4b: `--agents/--model/--max-turns/--debug` inherited; precedence per COMP-010.
- NFR-IMP-1: blocking findings warn + `tasklist_ready:false`, never exit non-zero.

**V5 (M5)** | exit: full matrix + budget + precision
- All named tests green incl. TEST-009 (dry-run, zero subprocess), TEST-010 (missing files), TEST-013 (gate-failure + resume edges).
- NFR-050.1: single-agent ≤2 min and ≤10% pipeline wall time.
- NFR-IMP-2: clean fixture → zero BLOCKING; injected duplicate D-ID → exactly one B-xxx (E2E#3).
- NFR-050.2 re-scan over final module set → zero forbidden imports.

## 6. Quality Gates Between Milestones

Each gate must be PASS to open the next milestone; any MAJOR/CRITICAL finding holds the gate closed (stop-and-fix).

**Gate M1→M2** | type contracts instantiable + import-scan green + OQ-001/004 resolved. CRITICAL if `ValidateConfig` fails to extend `PipelineConfig` or any `validate_*` import found in `pipeline/*`.

**Gate M2→M3** | both GateCriteria unit-asserted + 7-dimension prompt verified + `.gates` import identity confirmed + OQ-002/003/005/007 resolved. MAJOR if a gate field set diverges from DM-003 or a dimension is missing from the prompt.

**Gate M3→M4** | TEST-001/002 green + merge agreement-table + count recalculation + OPS-003 defined behavior + OQ-006 resolved. CRITICAL if dual code path branches outside list-length (NFR-050.5 violation) or N≥2 merge fails at runtime.

**Gate M4→M5** | standalone + auto-invoke + resume dispatch + non-blocking exit verified. MAJOR if validation exits non-zero on blocking findings or runs on a halted pipeline's incomplete artifacts.

**Gate M5→release** | full test matrix green + ≤2 min wall time + zero forbidden imports + false-positive precision validated. CRITICAL if any false positive survives on the clean fixture or the import invariant regresses.

**Standing CI gate (all milestones)** | NFR-050.2 import-scan runs on every commit from M1 onward; a violation is CRITICAL and blocks the in-flight milestone regardless of which milestone introduced it.

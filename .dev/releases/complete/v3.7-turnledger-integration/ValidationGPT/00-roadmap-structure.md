# Roadmap Structure

## Top-Level Sections

| Section | Line Range | Type |
|---|---|---|
| Executive Summary | roadmap.md:L9-L33 | Overview |
| Phase 1: Foundation — Audit Trail + Reachability Analyzer | roadmap.md:L38-L64 | Phase |
| Phase 2: Core E2E Test Suites | roadmap.md:L68-L133 | Phase |
| Phase 3: Pipeline Fixes + Reachability Gate Integration | roadmap.md:L137-L160 | Phase |
| Phase 4: Regression Validation + Final Audit | roadmap.md:L164-L179 | Phase |
| Risk Assessment and Mitigation | roadmap.md:L183-L193 | Governance |
| Resource Requirements and Dependencies | roadmap.md:L197-L240 | Governance |
| Success Criteria Validation Matrix | roadmap.md:L244-L259 | Governance |
| Timeline Summary | roadmap.md:L263-L275 | Sequencing |
| Open Questions | roadmap.md:L279-L290 | Governance |
| Appendix A: Integration Point Registry | roadmap.md:L294-L367 | Integration registry |

## Task Inventory

| Task ID | Requirement(s) | Line Range | Notes |
|---|---|---|---|
| 1A.1–1A.4 | FR-7.1, FR-7.2, FR-7.3 | L43-L53 | Audit writer, fixture, summary, verification test |
| 1B.1–1B.5 | FR-4.1, FR-4.2, FR-4.4 | L54-L64 | Manifest, analyzer, limitations, initial YAML, unit tests |
| 2A.1–2A.12 | FR-1.1–FR-1.18 | L74-L93 | Wiring point E2E suite |
| 2B.1–2B.4 | FR-2.1–FR-2.4 | L95-L106 | TurnLedger lifecycle coverage |
| 2C.1–2C.3 | FR-3.1a–FR-3.3 | L108-L118 | Mode matrix + exhaustion + interrupt |
| 2D.1–2D.6 | FR-6.1, FR-6.2 | L120-L131 | Outstanding QA gap closure |
| 3A.1–3A.4 | FR-5.1, FR-5.2, FR-4.3 | L143-L150 | Production code changes |
| 3B.1–3B.3 | FR-5.1, FR-4.4, FR-5.2 | L152-L159 | Validation tests for fixes |
| 4.1–4.6 | NFR-3, NFR-1, FR-7.2, NFR-5 | L170-L177 | Regression/audit/review tasks |

## Gates / Checkpoints

| Checkpoint | Source | Pass Criteria | Stop Conditions Present? |
|---|---|---|---|
| A | roadmap.md:L64 | Valid JSONL, cross-module reachability, manifest committed, analyzer contract documented | No explicit stop conditions |
| B | roadmap.md:L133 | All E2E tests pass, SC-1–6/8/12 validated, audit trail emitted, QA gaps closed | No explicit stop conditions |
| C | roadmap.md:L160 | 3 production fixes shipped, gates catch broken states, integrated into existing infrastructure | No explicit stop conditions |
| D | roadmap.md:L179 | Zero regressions, all 12 SC green, evidence package reviewable | No explicit stop conditions |

## Integration Points Parsed

| ID | Integration Point | Source |
|---|---|---|
| INT-1 | `_subprocess_factory` injection seam | roadmap.md:L298-L304 |
| INT-2 | `execute_phase_tasks()` vs `ClaudeProcess` delegation | roadmap.md:L306-L313 |
| INT-3 | `run_post_phase_wiring_hook()` callback chain | roadmap.md:L314-L320 |
| INT-4 | `run_post_task_anti_instinct_hook()` tuple contract | roadmap.md:L322-L328 |
| INT-5 | `_resolve_wiring_mode()` strategy resolution | roadmap.md:L329-L336 |
| INT-6 | `_run_checkers()` checker registry | roadmap.md:L337-L344 |
| INT-7 | `registry.merge_findings()` contract | roadmap.md:L345-L352 |
| INT-8 | Convergence registry constructor `(path, release_id, spec_hash)` | roadmap.md:L353-L359 |
| INT-9 | `DeferredRemediationLog` accumulator | roadmap.md:L361-L367 |

## Immediate Structural Risks

- Roadmap claims **13 requirements, 12 success criteria** at roadmap.md:L271, but the spec exposes a larger atomic requirement surface once FR sub-items are counted.
- Checkpoints define pass criteria but omit explicit stop conditions, despite validator rules requiring both.
- Several spec requirements added after earlier roadmap drafts appear untracked: FR-1.19, FR-1.20, FR-1.21, FR-2.1a.

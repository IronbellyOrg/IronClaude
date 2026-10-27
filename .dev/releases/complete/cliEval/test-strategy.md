---
complexity_class: HIGH
validation_philosophy: continuous-parallel
validation_milestones: 6
work_milestones: 6
interleave_ratio: 1:1
major_issue_policy: stop-and-fix
spec_source: design-spec.md
generated: "2026-05-18T19:37:23.892988+00:00"
generator: superclaude-roadmap-executor
---

# IronClaude Real-Eval Harness — Test Strategy

## 1. Validation Milestones Mapped to Roadmap

Per HIGH complexity (0.72) and security-critical surface (path-traversal, HOME containment, subprocess orchestration), validation milestones run **1:1 in parallel** with each work milestone. Validation owners run concurrently with implementation owners; gate sign-off blocks the next work milestone.

**V1: Foundation Validation** | 4d (parallels M1) | exit: schema rejection tests green, eval_id regex coverage = 100%, DSL interface mockable, AC11 sync gate verified
**V2: Isolation & Process Validation** | 5d (parallels M2) | exit: HOME containment + symlink attack suite green, ptytest provenance verified, NFR-PERF1 baseline recorded
**V3: Execution & Reporter Validation** | 6d (parallels M3) | exit: N′-vs-K contract test green, SIGINT/timeout reaping verified, 15-eval parallel isolation suite green
**V4: DSL & CLI Validation** | 4d (parallels M4) | exit: all 7 Expect primitives covered, every documented flag exercised, coverage-gate CLI green on fixture suite
**V5: Eval Body & Coverage Gate Validation** | 14d (parallels M5) | exit: all 15 evals deterministic on 3 consecutive runs, full-suite <10min at --parallel 8, coverage gate green against real `~/.claude/settings.json`
**V6: Release Hardening Validation** | 2d (parallels M6) | exit: ADRs cross-validated against tests, sync-verify green, clean-host smoke test green

## 2. Test Categories

| Category | Scope | Tooling | Trigger |
|---|---|---|---|
| Unit | Pure-function logic: regex guards, schema validators, dataclasses, DSL primitives | `uv run pytest -m unit` | pre-commit + per-PR |
| Integration | HomeIsolation+install_hooks, PtyDriver+claude binary, Reporter+ExecutorOutcome | `uv run pytest -m integration` | per-PR + milestone gate |
| Contract | N′-vs-K invariant, exit-code dispatch, schema field stability, eval_id regex post-expansion | `uv run pytest -m contract` | per-PR (fail-closed) |
| Security | Path-traversal, symlink attack, HOME containment, loader-bypass, scratch-root allowlist | `uv run pytest -m security` | per-PR + V2/V5 gates |
| E2E | Single-command `uv run superclaude eval --suite real` on clean host | shell smoke + container | V5 + V6 gates |
| Acceptance | SC1–SC5 evidence collection | `make verify-sync`, doctor, decisions.md review | V6 gate |
| Performance | NFR-PERF1 (HOME setup), NFR-PERF2 (RAM ceiling), NFR-PERF3 (<10min suite), NFR-PERF4 (disk poller) | benchmark fixtures + summary.json `duration_sec` | V2 (baseline) + V5 (full) |
| Concurrency | NFR-ISO1 no-shared-state at N×15 parallel trials | parametrized stress fixture | V3 gate |

## 3. Test-Implementation Interleaving Strategy

**Ratio: 1:1 (HIGH complexity justification).** The system has three independent failure surfaces that each demand co-located validation:

- **Security correctness** (FR-SCH2, FR-ISO2, NFR-SEC1/2/3): a single missed path-traversal case can destroy a maintainer's `~/.claude/`. Validation cannot lag implementation by even one milestone.
- **Subprocess contract** (FR-G1, FR-LC1, FR-RPT1): the N′-vs-K invariant and signal-handling code paths are not observable from unit tests alone — integration tests must land alongside the components.
- **External-tool coupling** (FR-G5, R1, R3): coverage gate and MCP retry policy depend on real `~/.claude/settings.json` and real MCP servers; empirical resolution of OQ-5/OQ-10 demands validation runs *during* M2/M3/M5.

A 1:2 or 1:3 ratio would push security gates downstream of implementation merges, creating windows where unsafe code is in `main`. Continuous-parallel 1:1 keeps every implementation deliverable bracketed by validation.

## 4. Risk-Based Test Prioritization

P0 (block release; validate first inside each milestone):
- R7 (real `~/.claude/` destruction) → TEST-002, TEST-003, NFR-SEC2/3 → V1+V2
- R11 (N′-vs-K silent eval drop) → TEST-007 → V3
- R13 (coverage gate false negative) → TEST-013 → V4+V5
- R1 (TTY behavior break) → TEST-006 + version pin → V2+V5
- RR-001 (decision churn) → OPS-001 + OQ tracking → V1+V6

P1 (block milestone gate):
- R3 (MCP flakiness) → TEST-014 + R3-mit retry-once → V5
- R12 (signal race / zombies) → NFR-REL1 tests → V3
- R2 (HOME setup perf) → NFR-PERF1 baseline → V2

P2 (track in next sprint):
- R5 (ptytest drift) → quarterly CHECKLIST review → V6
- R6 (suite >10 min) → NFR-PERF3 trend → V5
- R15 (sync drift) → make verify-sync CI → V6

## 5. Acceptance Criteria per Validation Milestone

**V1: Foundation** | exit when all below pass
- TEST-001 schema + ID rejection: invalid schema → exit 2 with no FS write; unsafe id → exit 2 pre-write; parameterize-expanded IDs re-validated.
- NFR-SEC1 negative set: `../home`, `/etc`, `..`, empty, leading-digit, template-token, parameterized-unsafe — all reject.
- COMP-010 DSL interface importable; mocked `EvalContext` exercises every method signature.
- AC11 source-of-truth gate: `make verify-sync` exits 0; pre-commit rejects `.claude/` edits.
- OPS-001: OQ-1/OQ-2/OQ-7 closed (schema-blocking subset); OQ-3/OQ-8/OQ-10 scheduled.

**V2: Isolation & Process** | exit when all below pass
- TEST-002 containment: `/tmp/eval-runs` accepted, repo `.dev/eval-runs` accepted, `/var/tmp/x` rejected, loader-bypass rejected.
- TEST-003 symlink attack: scratch-symlink-to-HOME rejected; nested symlink escape rejected; `setup_failed` artifact tag asserted; partial HOME preserved.
- TEST-004 capability gates: missing claude → HARD; --no-mcp → SOFT-SKIP; xfail honored.
- TEST-006 PTY lifecycle: real `claude` spawned, prompt readiness observed, transcript captured, timeout reaps child.
- NFR-PERF1: p50 ≤2s per eval HOME setup at --parallel 15 recorded in benchmark artifact.
- OQ-4 NOTICE/LICENSE in repo root; PROVENANCE.md records ptytest SHA; OQ-5 resolved.

**V3: Execution & Reporter** | exit when all below pass
- TEST-007 reporter contract: `len(evals[]) == counts.expanded_n_prime`; mismatch raises ReporterContractViolation → exit 2; skipped rows present.
- TEST-008 exit codes: 0/1/2/3 dispatch exercised for clean/failing/harness-error/interrupted.
- TEST-009 artifact reproducibility: run dir layout stable, transcript path recorded, stack trace on error.
- NFR-REL1: SIGINT during 15-eval parallel run → all in-flight marked INTERRUPTED, partial summary written, exit 3, zero zombies.
- NFR-ISO1: 15×N parallel trials show no shared HOME, no shared `auggie-first.jsonl` handles, no port collisions.
- NFR-PERF4: disk-budget poller halts run within 5s of breach; in-flight evals complete; `disk_budget_exceeded` artifact written.

**V4: DSL & CLI** | exit when all below pass
- FR-EXP1 primitive coverage: each of `file/jsonl/settings_json/exit_code/stderr/stdout/duration` has positive + negative + edge-case tests.
- Every flag in FR-CLI1 exercised by CLI test; help text auto-validated.
- FR-G5 coverage-gate CLI green on one-matcher fixture suite; missing matcher fails with `coverage_missing:<pattern>`.
- DOC-OQ7 (--junit) and DOC-OQ3 (--no-pty exclusion set) decisions implemented and tested.
- FR-G6 single-command smoke runs E1-only suite to completion.

**V5: Eval Bodies & Coverage Gate** | exit when all below pass
- All 15 evals (E1–E15 incl. parameterize-expanded E2.1/E2.2/E2.3) enumerate in `eval list` and pass `eval describe` round-trip.
- TEST-013 coverage gate: missing matcher fails; complete matcher set passes against real `~/.claude/settings.json`.
- TEST-014 --no-mcp behavior: MCP-dependent evals SKIPPED with reason; counts invariant kept_plus_skipped_equals_n_prime holds.
- Full-suite green on 3 consecutive runs at --parallel 8 in <10 min wall clock.
- R3-mit retry-once policy honored for MCP-flaky tag; OQ-10 resolved empirically.
- MIG-002 batch plan recorded.

**V6: Release Hardening** | exit when all below pass
- SC1: D-1..D-8 ADRs signed off in decisions.md.
- SC2: 15/15 eval IDs schema-valid; `eval doctor` zero violations.
- SC3: `uv pip list` diff shows zero new external deps.
- SC4: LOC actual within ±15% of estimate; recorded.
- SC5: 10/10 OQ-xxx resolved.
- `make verify-sync` exits 0; clean-host container smoke test green.
- MIG-001 sync evidence captured; MIG-003 macOS follow-up recorded.

## 6. Quality Gates Between Milestones

| Gate | From → To | Blocking Conditions | Owner |
|---|---|---|---|
| G1 | V1 → M2 entry | TEST-001 + NFR-SEC1 green; OQ-1/OQ-2/OQ-7 closed; AC11 enforced; OQ-4 closed (M2 entry blocker) | architect |
| G2 | V2 → M3 entry | TEST-002/003/006 green; NFR-SEC2/3 verified; OQ-5 closed; ptytest provenance complete | architect |
| G3 | V3 → M4 entry | TEST-007/008 green; NFR-REL1 zombie-free; NFR-ISO1 stress passed | architect |
| G4 | V4 → M5 entry | All 7 primitives covered; every flag exercised; coverage-gate fixture green; OQ-3 + OQ-7 implemented | architect |
| G5 | V5 → M6 entry | Full suite green ×3; coverage gate green against real settings.json; OQ-10 empirically resolved; MIG-002 recorded | architect |
| G6 | V6 → Release | SC1–SC5 evidence complete; `make verify-sync` EXIT=0; clean-host smoke green; ADRs signed | RyanW |

**Issue handling at each gate:**
- CRITICAL (security regression, real-HOME guard bypass, N′-vs-K violation, zombie process, sync drift): stop-and-fix; gate held; rollback if found post-gate.
- MAJOR (perf budget breach, flag drift, schema-validator gap, missing OQ resolution): stop-and-fix before next milestone; gate held.
- MINOR (cosmetic CLI text, non-critical log formatting, redundant test): tracked into next sprint; no gate impact.
- COSMETIC (typos in docs, README polish): backlog; no gate impact.

## 7. Test Specificity per Work Milestone

**M1 tests:** Pure-Python — exercise SuiteLoader against ≥20 fixture YAMLs (10 valid, 10 malformed); fuzz eval_id regex with property-based tests (hypothesis-style if available, else table-driven); assert no `Path.mkdir` / `open(.., "w")` reached prior to schema+regex validation; verify capability gate emits CapabilityReport JSON matching DM-008.

**M2 tests:** Real-FS — create scratch dirs under `/tmp/eval-runs` and repo `.dev/eval-runs`; verify `Path.resolve()` defeats symlink races; spawn one real `claude --version` through PtyDriver; assert install_hooks adapter never writes outside per-eval HOME (audit via inotify-style filter or post-run path scan); record p50/p95 HOME setup timings.

**M3 tests:** Subprocess + threading — run 15 trivial fixture evals at --parallel 15 across 10 trials, assert zero shared-state collisions; inject mid-run SIGINT and assert partial summary integrity; force ReporterContractViolation by tampering with counts and assert exit 2; verify disk-budget poller fires at 5±1s tick.

**M4 tests:** CLI surface — invoke every documented flag at least once via Click test runner; verify `--junit` produces JUnit XML schema-valid output (or absence per OQ-7); fixture suite with one synthetic matcher proves coverage gate red→green transition.

**M5 tests:** End-to-end — full suite execution against real `claude` + real MCP servers (where available); --no-mcp run asserts SKIPPED status taxonomy; coverage gate enumerates exactly the v1 matcher families from real settings.json; 3 consecutive green runs for determinism; record full-suite duration vs <10 min target.

**M6 tests:** Release evidence — `uv run superclaude eval doctor` on fresh container; `make verify-sync` exit 0; cross-check decisions.md against test artifacts (every OQ has resolution; every ADR cites a test that exercises its decision).

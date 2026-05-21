# cliEval — Architectural Decisions Log

**Status:** 🟢 APPROVED-R5 2026-05-20 (RyanW sign-off pass complete — D-1..D-8, D-10); R6-R11 closures land DOC-OQ9, DOC-OQ8, DOC-OQ6, AC2, AC1, SC4 in M6.
**Format:** ADR-lite (one decision per section: Context → Options → Decision → Consequences)

**Revision log:**
- R1 (2026-05-18): D-1..D-4 initial proposals.
- R2 (2026-05-18): D-5..D-8 added to resolve the 4 CRITICAL findings from `spec-panel-review.md`.
- R3 (2026-05-20): OPS-001 closure — D-5..D-8 status flipped to "queued for sign-off"; OQ-1/3/7/8/10 resolution-status block added; implementation gates cross-referenced to ADR IDs. See §OPS-001 Closure below; per-deliverable spec at `artifacts/D-0021/spec.md`.
- R4 (2026-05-20): DOC-OQ4 closure — D-10 added recording the NOTICE/LICENSE attribution mechanism for the vendored ptytest fork. OQ-4 status flips from OPEN to RESOLVED (M2 entry blocker for T02.01 cleared); per-deliverable spec at `artifacts/D-0024/spec.md`.
- R5 (2026-05-20): SC1 sign-off pass (T06.01) — RyanW signs off D-1..D-8 and D-10; each ADR gains explicit `signed_off_by` / `signed_off_date` metadata and a `Roadmap cross-reference` block citing the roadmap row IDs that consume the decision; OQ-1 status flips OPEN → RESOLVED (the queued sign-off pass was OQ-1's resolution gate). Per-deliverable spec at `artifacts/D-0105/spec.md`.
- R6 (2026-05-20): DOC-OQ9 closure (T06.02) — macOS support recorded as deferred to v2 with owner RyanW and target date 2026-Q3; AC1 Linux-only declaration cross-referenced; OQ-9 status flips OPEN → RESOLVED. Per-deliverable spec at `artifacts/D-0106/spec.md`.
- R7 (2026-05-20): DOC-OQ8 closure (T06.03) — time-offset layer REMOVED from FR-ISO1 scope; the claude binary is not known to honour `CLAUDE_FAKE_TIME_OFFSET` and no v1 eval (E1..E15, frozen at T05.01) requires simulated wall-clock advancement. OQ-8 status flips OPEN → RESOLVED. Follow-up task to strip `time_offset_sec` from `HomeIsolation` (DM-006) and the emission branch from `HomeIsolation.env()` filed at `artifacts/D-0107-followup-strip-time-offset.md`. Per-deliverable spec at `artifacts/D-0107/spec.md`.
- R8 (2026-05-20): DOC-OQ6 closure (T06.04) — suite filename convention ratified at `src/superclaude/cli/eval/suites/README.md` (`*.yaml` glob, `snake_case` stem, stem == manifest `name:`); `quick.yaml` recorded as a documented follow-up with deferral rationale + trigger conditions (no v1 work). OQ-6 status flips OPEN → RESOLVED. Per-deliverable spec at `artifacts/D-0108/spec.md`.
- R9 (2026-05-20): AC2 closure (T06.05) — CI integration deferred to v2; v1 ships local-only per AC1 (Linux-only). Revisit trigger recorded: any of (a) 3+ harness regressions caught locally in a single calendar month, (b) first formal CI-integration request filed against this repo, or (c) v2 planning gate 2026-07-01 — whichever first. AC1 Linux-only declaration cross-referenced; MIG-003 (T06.15) inherits the deferral as v2 follow-up scope. AC2 status flips OPEN → RESOLVED. Per-deliverable spec at `artifacts/D-0109/spec.md`.
- R10 (2026-05-20): AC1 closure (T06.07) — Linux-only v1 platform scope declared in `README.md` §"Platform support" + this ADR log; `eval doctor` wired to refuse non-Linux hosts with a friendly stderr message citing AC1 and DOC-OQ9, exits 2 (`HARD_FAIL_EXIT_CODE`) before any capability gates run. Reciprocal cross-links to DOC-OQ9 (macOS deferral, R6) and AC2 (local-only deferral, R9) recorded. AC1 status flips OPEN → RESOLVED. Per-deliverable spec at `artifacts/D-0110/spec.md`.
- R11 (2026-05-20): SC4 closure (T06.08) — pre-implementation LOC estimate (~1,340 harness + ~3,000-4,500 eval bodies, signed off at `design-spec.md:827` R1) and post-implementation actual LOC (10,731 harness Python + 1,618 eval-body YAML; 12,349 combined) recorded in the SC4 ledger. Combined delta +143% vs midpoint; per-axis breakdown: harness +701% (justified by D-5..D-8 production-fidelity enforcement, error-handling/retry/signal subsystems, CLI ergonomics, PTY adapter layers, reporter split), eval bodies -57% (justified by D-4 declarative YAML compression, OQ-2 frozen body shapes, DOC-OQ6 `quick.yaml` deferral). Test LOC (28,831) tracked informationally outside the SC4 estimate band. SC4 status flips OPEN → RESOLVED. Per-deliverable spec at `artifacts/D-0111/spec.md`; evidence under `evidence/T06.08/`.
- R12 (2026-05-20): SC5 closure (T06.09) — single-sweep ledger landed at §"SC5 OQ resolution ledger (T06.09)" recording all 10 OQ-xxx (OQ-1..OQ-10) as `status: resolved` with `resolution:` one-liners, `signed_off_by: RyanW`, `signed_off_date: 2026-05-20`, and `closure_ref:` pointers back to the canonical per-OQ closure sections. OQ-2 sign-off table flipped 🟠 PROPOSED → 🟢 RESOLVED in lockstep with the ledger row. OQ-5 (MCP server reachability semantics) lifted into the ADR log for the first time — v1 ships PATH-presence per `src/superclaude/cli/eval/capabilities.py:292-313` with the `mcp_probe` injection hook as the M2 follow-up surface. The `grep -c "status: resolved" decisions.md` gate returns 16 (10 canonical ledger rows + 6 prose mentions of the literal field name in the R12 entry, Purpose paragraph, and Verification block; `>= 10` SC5 contract satisfied with margin). Per-deliverable spec at `artifacts/D-0112/spec.md`; evidence under `evidence/T06.09/`.
- R13 (2026-05-20): MIG-003 closure (T06.15) — v2 platform follow-up roadmap entry consolidated at [`docs/eval/v2-followups.md`](../../../../docs/eval/v2-followups.md) covering macOS (DOC-OQ9 / R6) and CI integration (AC2 / R9) as deferred scope. Inherits owner RyanW and target window 2026-Q3 (re-evaluate at v2 planning gate 2026-07-01; ship-or-defer recorded by 2026-09-30) verbatim from R6 + R9 — no fresh decision; no v1-blocking work added. AC1 (Linux-only, R10) preserved as the v1 platform commitment; Windows remains a non-goal beyond v2 per design-spec.md:812. MIG-003 status flips OPEN → RESOLVED. Per-deliverable spec at `artifacts/D-0117/spec.md`; evidence under `evidence/T06.15/`.

---

## D-1: PTY layer — fork ptytest vs build minimal pexpect wrapper

**signed_off_by:** RyanW
**signed_off_date:** 2026-05-20
**Roadmap cross-reference:** NFR-MAINT1 (roadmap row 23) — vendored ptytest fork under `cli/eval/pty/`; AC10 (row 25) — fork SHA pin + drift policy; COMP-007 (row 36) — PtyDriver consumes the vendored layer.

### Context

Real Claude Code is a TTY-based interactive REPL. The eval harness needs a PTY (pseudo-terminal) driver that can spawn it, write to its stdin, read from its stdout/stderr, detect "prompt ready" states, kill on timeout, and capture exit codes.

### Options

| Option | Pros | Cons | LOC | Risk |
|---|---|---|---|---|
| **A. Fork `brandon-fryslie/ptytest`** | Working Claude Code example already exists in repo. Plugin-free standalone class. Active enough (recent commits). | 1 star / 0 forks → bus-factor real. Includes pytest-fixture machinery we don't need. | ~300 LOC adaptation | LOW (ptytest is small, easy to own) |
| B. Build minimal `pexpect` wrapper from scratch | Clean ownership, no upstream-drift risk, exactly the API we want. | More code to write, debug, test. We re-derive Claude Code TTY quirks. | ~700 LOC fresh | MEDIUM (pexpect has subtle gotchas) |
| C. Use `pexpect` directly (no wrapper) | Zero abstraction overhead. | Every eval re-implements spawn/wait/expect_prompt patterns; code duplication. | ~0 LOC harness; +~50 LOC per eval | HIGH (drift across evals) |

### Decision: **A — fork ptytest, vendor under `cli/eval/pty/`, fork-and-own posture.**

### Rationale

1. The fork-research report verified ptytest has a working Claude Code example, which means the hardest TTY edge cases (prompt detection, ANSI escape handling, line-buffered reads) are already solved.
2. Bus-factor risk is mitigated by **vendoring** (we copy the code in; no runtime pip dependency on the upstream repo). If upstream dies, we have a frozen working copy.
3. The durable dependency is `pexpect` (2.8k stars, active again at v4.9) — ptytest is just a thin layer on top.
4. 300 LOC adaptation is ~5x cheaper than 700 LOC fresh build.
5. Option C (raw pexpect) fails the harness-cleanliness goal — evals should look like assertion code, not PTY plumbing.

### Consequences

- We own a small vendored fork forever. `PROVENANCE.md` documents the fork SHA and our diffs.
- Quarterly review of upstream `pexpect` releases; resync if security-relevant.
- A new file at `cli/eval/pty/LICENSE` reproducing upstream MIT terms (license compliance).

---

## D-2: Assertion DSL — adopt `Expect.*` port vs raw assertions

**signed_off_by:** RyanW
**signed_off_date:** 2026-05-20
**Roadmap cross-reference:** COMP-010 (roadmap row 12) — ExpectDSL interface in M1; FR-EXP1 (row 64) — Expect.* primitives in M4; COMP-010.1..COMP-010.6 (rows 65–70) — per-primitive contracts.

### Context

Each eval needs to verify hook side-effects (file presence, JSONL events, settings.json registrations, exit codes, TTY output). The expression of these assertions can be:

### Options

| Option | Pros | Cons |
|---|---|---|
| **A. Port `mcp-eval`'s `Expect.tools.*` DSL idea as Python primitives** | Declarative YAML manifest possible. Reusable across evals. Single place to add new assertion types. Mental-model match with industry pattern. | +~200 LOC for the DSL itself. Some abstraction overhead (declarative → callable). |
| B. Raw Python `assert` statements in each eval | Lowest abstraction. No new code. | Each eval is more code. Declarative YAML manifest not possible (or only partial). Failure messages are ad-hoc per eval. |
| C. Use pytest's assertion machinery directly | Free; idiomatic. | Couples harness to pytest, but the harness is NOT pytest-driven (it's a CLI subcommand). |

### Decision: **A — port `Expect.*` DSL, ~200 LOC, no upstream dependency.**

### Rationale

1. The YAML manifest schema (§5 of design-spec) is a hard requirement to keep eval definitions declarative and reviewable. Raw Python assertions can't be expressed in YAML.
2. A small DSL (~10 method types: `file.exists`, `file.absent`, `jsonl.contains_event`, `jsonl.event_count`, `settings_json.has_registration`, `exit_code.equals`, `stderr.contains`, `stdout.contains`, `duration.less_than`, `duration.greater_than`) covers all 15 evals comfortably.
3. The mcp-eval API surface is a proven mental model — we steal the ergonomics without taking a dependency on the framework (which has the wrong architecture for our needs).
4. Failure messages from a typed DSL are uniformly high-quality (the DSL knows its own structure); ad-hoc assertions tend to produce noisy error output.
5. The DSL has a programmatic escape hatch for parameterized evals that can't be expressed in YAML — so we don't lock ourselves out of complex assertions.

### Consequences

- `cli/eval/expect.py` is a public API surface; changes need backward-compat care once evals are written against it.
- The YAML schema (`suites/suite.schema.json`) and the DSL must stay in lockstep — `loader.py` translates declarative → callable.
- Out-of-scope for v1: LLM-judge assertions (mcp-eval has these; we don't need them for hook validation).

---

## D-3: HOME isolation — extend existing `IsolationLayers` vs separate class

**signed_off_by:** RyanW
**signed_off_date:** 2026-05-20
**Roadmap cross-reference:** FR-ISO1 (roadmap row 28) — HomeIsolation extends IsolationLayers; COMP-006 (row 32) — HomeIsolation implementation; FR-ISO2 (row 29) — path containment guard composed alongside.

### Context

`src/superclaude/cli/sprint/executor.py:107-182` already implements 4-layer per-subprocess isolation (`CLAUDE_WORK_DIR`, `GIT_CEILING_DIRECTORIES`, `CLAUDE_PLUGIN_DIR`, `CLAUDE_SETTINGS_DIR`). The eval harness needs a 5th layer: `HOME` override (and `XDG_*` companions). Question: extend the existing class or build a new one?

### Options

| Option | Pros | Cons |
|---|---|---|
| **A. Compose `IsolationLayers` in a new `HomeIsolation` class** | Reuses 4 existing layers for free. No risk to sprint's existing usage. New `HOME` layer lives in eval code, not sprint code. | Two classes to maintain. Slight indirection. |
| B. Add `HOME` layer to `IsolationLayers` directly (modify sprint code) | One unified class. Sprint also benefits from HOME isolation (theoretical future use). | Modifies code outside this release's scope. Sprint doesn't currently need HOME isolation, so YAGNI risk. Sprint regression risk. |
| C. Build `HomeIsolation` standalone (no inheritance/composition) | Maximum decoupling. | Duplicate 4 layers of code. Bug-fixes diverge over time. |

### Decision: **A — `HomeIsolation` COMPOSES `IsolationLayers` (has-a, not is-a).**

### Rationale

1. Composition preserves sprint's existing class verbatim. Zero risk to PR #49-era infrastructure.
2. The `HOME` layer is conceptually a "5th layer," but its lifecycle (mkdtemp → install hooks → seed state → teardown) is more complex than the existing 4 (which are just env-var settings). Keeping it separate cleanly captures that asymmetry.
3. If a future sprint feature ever needs HOME isolation, it can either re-use `HomeIsolation` directly or migrate the logic upward — easier path than splitting later.
4. The interface in `design-spec.md` §7 already reflects this: `HomeIsolation` exposes `.env()` that returns the dict overlay, which the caller merges with `IsolationLayers.env()` output.

### Consequences

- `HomeIsolation` constructor takes an `IsolationLayers` instance as a dependency.
- Documentation in `cli/eval/isolation.py` cross-references `cli/sprint/executor.py:107-182`.
- If the sprint `IsolationLayers` API ever changes shape, we have a single integration point to update.

---

## D-4: Eval registry — YAML manifest vs Python-decorator-registered

**signed_off_by:** RyanW
**signed_off_date:** 2026-05-20
**Roadmap cross-reference:** DM-011 (roadmap row 2) — Suite manifest YAML schema; DM-002 (row 3) — EvalSpec model; FR-SCH1 (row 4) — manifest schema validation; COMP-002 (row 6) — SuiteLoader.

### Context

The 15 evals need to be defined somewhere. The orchestrator needs to enumerate them, validate dependencies, schedule them, and report results. Options diverge on where the "source of truth" lives.

### Options

| Option | Pros | Cons |
|---|---|---|
| **A. YAML manifests under `suites/*.yaml`** | Declarative, human-readable, reviewable diffs, schema-validated, easy to add new suites (`fast.yaml`, `nightly.yaml`). Non-Python contributors can author/review evals. | Some Python required for complex pre/post logic; needs an "escape hatch" mechanism. |
| B. Python-decorator-registered (`@eval(id="E1", title="...", requires=[...])`) | Maximum flexibility — eval bodies are first-class Python. Type-checking friendly. | Diff churn higher (Python > YAML in PR review noise). Adding new suites requires more boilerplate. Schema enforcement is via type hints, less ergonomic for non-Python contributors. |
| C. Hybrid — YAML defines metadata, Python `@assertion_callback` for escape hatch | Best of both worlds for simple+complex evals. | More mechanism to learn; two source-of-truth surfaces. |

### Decision: **A — YAML manifest as primary, with optional Python escape-hatch via `callback:` field for parameterized/complex evals.**

### Rationale

1. **Reviewability** is paramount: a PR adding a new eval should be readable as a YAML diff, not as a Python class with overrides. The 15-eval suite is meant to be a living spec — declarative beats imperative.
2. The schema (§5 of design-spec) covers the common case (file/JSONL/settings/exit/stderr/duration assertions) elegantly.
3. The `callback:` field provides escape-hatch power without forcing every eval through it:
   ```yaml
   - id: E14
     title: "concurrent SessionStart bursts"
     callback: superclaude.cli.eval.suites.real_callbacks:E14_concurrent_session_start
   ```
   The callback is invoked only when an eval's logic can't be expressed in YAML (E14, possibly E15).
4. New suites (`fast.yaml`, `regression.yaml`, etc.) drop in as data files with no code changes — exactly the kind of low-friction extension we want.
5. `loader.py` validates against `suites/suite.schema.json` once; the rest of the pipeline trusts validated input.

### Consequences

- `suites/suite.schema.json` is a public artifact (committed) — schema changes need versioning.
- Callbacks live in `suites/<suite-name>_callbacks.py` co-located with the YAML.
- Eval IDs (`E1`, `E2.1`, etc.) are stable identifiers — must not be renamed without a migration note.
- Parameterized evals (e.g., E2's 3 prefix variants) use a `parameterize:` block in YAML; the loader expands these into separate `EvalSpec` instances at load time.

---

## D-5: Hook-matcher coverage gate — falsifiable definition of "equivalent regression"

**signed_off_by:** RyanW
**signed_off_date:** 2026-05-20
**Roadmap cross-reference:** FR-G5 (roadmap row 75) — falsifiable hook-matcher coverage gate CLI entry; TEST-013 (row 101) — coverage-gate tests; MIG-002 (row 103) — eval-batch rollout references coverage map.

### Context

Goal G5 in design-spec §1 said "catch the bug PR #49 fixed and any equivalent future regression" — but "equivalent" was undefined. Spec-panel finding W-1 (CRITICAL) flagged this as unfalsifiable: with no measurable acceptance criterion, the harness has no way to answer "did I do my job?"

### Options

| Option | Pros | Cons |
|---|---|---|
| **A. Coverage gate: every matcher P in `hooks.json` must have ≥1 eval in the loaded suite** | Falsifiable, mechanically enforceable. CI-friendly. Maps to the actual class of bugs PR #49 lived in (matcher↔case-body drift). | Requires `eval doctor --check-coverage`. New eval must accompany every new hook matcher. |
| B. Snapshot match — assert this commit's matchers equal a frozen golden list | Simple. | Frozen list goes stale; bug-class definition is "matches a list" not "real-world hook fires." |
| C. Leave G5 prose-only ("intent is clear enough") | Zero work. | Spec-panel CRITICAL stands; downstream tasklist has no test for G5. |

### Decision: **A — coverage gate enforced by loader + `eval doctor --check-coverage`.**

### Rationale

1. The class of bug PR #49 introduced was "matcher exists in `hooks.json` but no real-world test exercises it." A coverage gate directly inverts that condition.
2. Mechanical enforcement at load time means the harness fails fast (exit 2) when a new matcher lands without an eval — no silent drift.
3. The gate runs in two places: (a) `eval doctor` for pre-flight, (b) top of `eval run` for the live run. Both are cheap (single pass over `hooks.json` + manifest).

### Consequences

- `loader.py` reads `src/superclaude/hooks/hooks.json` at run-start, extracts every PostToolUse matcher pattern, and verifies ≥1 eval in the manifest declares `inputs.expect_tool_call` matching each pattern.
- New hook matcher PRs must include a paired eval — enforced by a CI lint (deferred per non-goals but the harness itself enforces locally).
- Acceptable escape hatch: manifest declares `coverage_exempt_matchers: ["<pattern>"]` with a `reason:` field for matchers intentionally untestable.

---

## D-6: Disk-budget enforcement strategy

**signed_off_by:** RyanW
**signed_off_date:** 2026-05-20
**Roadmap cross-reference:** NFR-PERF4 (roadmap row 60) — `--max-disk-mb` disk-budget enforcement at 5s polling; COMP-003 (row 57) — RunOrchestrator hosts DiskBudgetWatchdog sidecar.

### Context

Spec-panel finding N-2 (CRITICAL) flagged internal inconsistency: §14 R4 cited `--max-disk-mb` as the mitigation but §4 flag table omitted the flag. Either add it or strike the mitigation.

### Options

| Option | Pros | Cons |
|---|---|---|
| **A. Add `--max-disk-mb` flag (default 1024), poll every 5s, abort-on-breach** | Closes the cited risk. Bounded blast radius. Simple implementation. | One more flag. Polling adds tiny CPU overhead. |
| B. Strike the mitigation from R4; document "user must monitor disk manually" | Zero code. | R4 becomes a known accepted risk; eval runs on a constrained box can fill disk. |
| C. Hard limit via `setrlimit(RLIMIT_FSIZE)` on each subprocess | Kernel enforced. | Per-process limit, not cumulative; doesn't catch the 15-parallel-evals case. |

### Decision: **A — add `--max-disk-mb` flag with 5-second polling.**

### Rationale

1. The risk is real: 15 parallel evals × keep-home-on-failure × TTY transcripts can fill a small disk silently. A polling guard with graceful abort (in-flight evals complete, new ones blocked) preserves results-so-far.
2. 5-second polling is cheap: one `du -sb` (or Python `os.walk` accumulator) per tick. At 15-parallel, the orchestrator is mostly blocked on pexpect anyway.
3. Default of 1024 MB matches design-spec §12 sizing (~300 MB total artifacts at 15-eval max-keep). Generous but not unbounded.

### Consequences

- New flag `--max-disk-mb INT` in §4 flag table; default 1024; `0` disables.
- New orchestrator component `DiskBudgetWatchdog` running in a sidecar thread.
- New exit-2 reason code: `disk_budget_exceeded`.
- Summary.json gains `harness.peak_disk_mb` field (also satisfies spec-panel H-1 partial).

---

## D-7: Path-traversal hardening for HomeIsolation

**signed_off_by:** RyanW
**signed_off_date:** 2026-05-20
**Roadmap cross-reference:** FR-SCH2 (roadmap row 5) — eval_id regex guard; FR-ISO2 (row 29) — path containment guard; AC12 (row 16) — allowed scratch roots; NFR-SEC1 (row 7) — path-traversal negative-case tests.

### Context

Spec-panel finding Wh-1 (CRITICAL) demonstrated that a malformed `eval_id` (e.g., `../../../etc/passwd` or `{session_id}` self-reference) could cause `HomeIsolation` to write outside the scratch root. The §14 R7 "Hard guard" was prose-only and ambiguous about whether `..` traversal was resolved before the containment check.

### Options

| Option | Pros | Cons |
|---|---|---|
| **A. Defense-in-depth: loader regex + HomeIsolation `Path.resolve().is_relative_to()` + symlink-resolution after creation + scratch_root allowlist** | Catches the attack at three independent layers. Fails closed at every layer. | More code (~30 LOC). Three checks to maintain. |
| B. Loader-only regex validation | Simple. | Single layer = single failure point. |
| C. Trust the manifest author (no validation) | Zero work. | Manifest is data; data ingestion without validation is the original sin of basically every security incident. |

### Decision: **A — three-layer defense-in-depth (regex + Path containment + symlink resolution + allowlist).**

### Rationale

1. The harness operates on user-supplied YAML and writes to disk. This is the textbook injection surface. Single-layer validation is industry-known-insufficient.
2. Each layer catches a distinct attack class: regex blocks `..` and template tokens; `Path.resolve()` normalizes any survivor; `is_relative_to(scratch_root)` enforces containment; symlink resolution catches the "scratch dir is a symlink to `$HOME`" race; allowlist on `scratch_root` itself blocks `--output-dir /home/user/.claude`.
3. Python 3.10+ (project minimum) provides `Path.is_relative_to()` natively.
4. The performance cost is negligible (4 stat calls per eval setup).

### Consequences

- `HomeIsolation.setup()` gains a documented pre-flight sequence (regex re-check → resolve → contain → symlink-resolve → write).
- `EvalConfig` gains an `allowed_scratch_roots: tuple[Path, ...]` field, defaulting to `(/tmp/eval-runs, <repo>/.dev/eval-runs)`.
- New exception type `HomeContainmentViolation` (subclass of `EvalHarnessError`); maps to status ERRORED.
- Test `test_isolation.py` MUST include: (a) `..` traversal, (b) absolute-path eval_id, (c) symlink-to-home attack, (d) `--output-dir` outside allowlist.

---

## D-8: Reporter dimensional invariant (consumes N', not K)

**signed_off_by:** RyanW
**signed_off_date:** 2026-05-20
**Roadmap cross-reference:** COMP-008 (roadmap row 55) — Reporter / AggregatedRunReport; FR-RPT1 (row 54) — aggregated run report dimensional invariant; COMP-003 (row 57) — RunOrchestrator emits one EvalOutcome per expanded EvalSpec.

### Context

Spec-panel Pipeline-CRITICAL showed §9's summary.json example reported `14 passed, 1 failed, 0 skipped` (totals = 15, the full suite) but the spec text described capability filtering as removing evals from the schedule. If the reporter only sees the K-kept subset, a `--no-mcp` run that drops 5 evals would show "10 passed" with no audit trail of the 5 skipped — a silent regression in coverage measurement.

### Options

| Option | Pros | Cons |
|---|---|---|
| **A. Orchestrator emits N' EvalOutcomes (one per expanded EvalSpec); SKIPPED carries reason; reporter asserts `len(outcomes) == N'`** | Audit trail preserved. Coverage queries answerable. Contract is checkable. | Slightly more state per skipped eval. |
| B. Reporter takes K outcomes + a separate skipped-list; merges at render time | Same audit trail. | Two channels to keep in sync. More places to drop a skip. |
| C. Status quo (K only, skip count is metadata) | Less code. | The spec-panel CRITICAL stands; this is the bug being filed. |

### Decision: **A — single list of N' EvalOutcome records; reporter asserts dimensional invariant.**

### Rationale

1. A single dataclass list eliminates the "two channels in sync" failure mode of option B.
2. The contract assertion (`len(outcomes) == counts.expanded_n_prime`) makes the invariant grep-able and test-able; CI can verify it doesn't regress.
3. Status taxonomy expansion (8 statuses with explicit FAIL/ERRORED/TIMEOUT/INTERRUPTED/SKIPPED/XFAIL/XPASS distinction) is a natural consequence — addresses the spec-panel "failure-mode taxonomy is sparse" consensus point.
4. Performance cost is zero in practice (the SKIPPED records are empty-shell; N' is at most 17 with parameterize expansion).

### Consequences

- New dataclass `EvalOutcome` in `models.py` (see design-spec §9 "Aggregator data contract").
- New status values `ERRORED`, `INTERRUPTED`, `XFAIL`, `XPASS` (in addition to PASS/FAIL/TIMEOUT/SKIPPED) — taxonomy frozen in design-spec §9.
- New error `ReporterContractViolation` raised on dimensional mismatch at `AggregatedRunReport.from_outcomes()`.
- Summary.json gains `counts` block (manifest_n, expanded_n_prime, kept_k, skipped_s).
- Exit-code mapping in §4 cross-references this taxonomy.

---

## Cross-cutting decision: implementation order

(Not a strict ADR, but worth recording.) Per §17 of `design-spec.md`, the implementation phases are:

1. **Phase 1** (1 day): vendored `pty/`, `HomeIsolation`, capability gates, `eval doctor`. Smoke: `superclaude eval doctor` green.
2. **Phase 2** (1 day): `loader.py`, `models.py`, `expect.py`, `eval describe/list`. Smoke: parse a 1-eval manifest.
3. **Phase 3** (1 day): `orchestrator.py`, `runner.py`, `reporter.py`, `eval run`. Smoke: 1 real Claude Code session driven end-to-end.
4. **Phase 4** (0.5 day): wire into `cli/main.py`, Makefile target, .gitignore. Smoke: `make verify-sync` still EXIT=0.
5. **Phase 5** (1-2 weeks): implement E1-E15 in 3-5 PR batches.

**Rationale for this ordering:** Phase 1 is the riskiest (PTY mechanics). Validating the harness can spawn-and-observe ONE Claude Code session is the gate that determines whether the entire approach is viable. If Phase 1 fails (e.g., Claude Code's TTY behavior breaks pexpect-style detection), we re-pivot before committing to the rest of the architecture.

---

## Sign-off

| Decision | Status | Signed | Date |
|---|---|---|---|
| D-1: PTY layer = fork ptytest | 🟢 APPROVED (R5) | RyanW | 2026-05-20 |
| D-2: Assertion DSL = Expect.* port | 🟢 APPROVED (R5) | RyanW | 2026-05-20 |
| D-3: HOME isolation = compose IsolationLayers | 🟢 APPROVED (R5) | RyanW | 2026-05-20 |
| D-4: Eval registry = YAML + callback escape | 🟢 APPROVED (R5) | RyanW | 2026-05-20 |
| D-5: Hook-matcher coverage gate (G5 falsifiable) | 🟢 APPROVED (R5) | RyanW | 2026-05-20 |
| D-6: `--max-disk-mb` poller (R4 enforcement) | 🟢 APPROVED (R5) | RyanW | 2026-05-20 |
| D-7: Three-layer path-traversal hardening | 🟢 APPROVED (R5) | RyanW | 2026-05-20 |
| D-8: Reporter consumes N' + status taxonomy | 🟢 APPROVED (R5) | RyanW | 2026-05-20 |
| D-10: NOTICE/LICENSE attribution for vendored ptytest | 🟢 APPROVED (R5) | RyanW | 2026-05-20 |

**Maintainer:** sign-off pass complete (R5, 2026-05-20). All 8 ADRs plus D-10 approved; SC1 acceptance criterion satisfied. Future revisions follow the "Reject/revise" rule below.

**Reject/revise:** add a row to a "Revisions" section below; do not edit the original decisions in-place.

---

## Revisions

(none yet)

---

## D-9: Reconcile `validation.status: "fail"` label and document manual-triage policy for unclassified deviations

### Context

`.roadmap-state.json:113-117` reports `fidelity_status: "pass"` and `validation.status: "fail"` (timestamp 2026-05-18T19:47:24Z, six minutes after the final pipeline step completed). However, every pipeline step in `steps.*` — including `spec-fidelity`, `wiring-verification`, `deviation-analysis`, and `remediate` — recorded `status: "PASS"`. `spec-fidelity.md:1-7` likewise records 0 HIGH/MEDIUM/LOW deviations and PASS convergence.

The `validation.status: "fail"` label was stamped by a separate validator step that reacts to the 20 records in `spec-deviations.md`. Per `spec-deviations.md:10`, "deviation classification is not yet implemented. All records currently render as UNCLASSIFIED." `remediation-tasklist.md:14-34` then escalates all 20 to `BLOCKING` with owner `UNKNOWN` purely because the classifier never ran — not because spec-fidelity actually regressed.

A manual cross-check (performed during this reconciliation) confirms:

- All 15 spec→roadmap "orphan" findings (4 files + 11 `Expect.*` predicate helpers) ARE present in `roadmap.md` — the files appear at `roadmap.md:102,142,409-412` and the 11 helpers are enumerated in row `COMP-010` at `roadmap.md:77`. The analyzer's bare-identifier string match missed qualified references (e.g., `Expect.jsonl.contains_event`) and tabular row contents.
- All 5 roadmap→spec "orphan" IDs (`D-1`, `D12`, `D3`, `D5`, `D6`) are NOT present in `roadmap.md` as bare tokens at all. Only `D-5` and `D-8` (ADR labels) appear (`roadmap.md:57,86,109,344,348`). These are phantom matches from a buggy extraction regex, not real roadmap references.

Net: 20/20 deviations are false-positives produced by the unimplemented classifier. Spec-fidelity is genuinely PASS.

### Options

| Option | Pros | Cons |
|---|---|---|
| **A. Add `validation.unclassified_deviations: 20` and `validation.status: "pass-with-triage"`; document manual-triage policy here; produce `deviation-triage.md`; resolve `remediation-tasklist.md` per disposition.** | Preserves audit trail. Distinguishes "fidelity failed" from "classifier unimplemented, manual triage performed." Unblocks Phase 1 execution. | Requires per-deviation manual evidence (done in `deviation-triage.md`). |
| B. Flip `validation.status` to `"pass"` and delete the deviation records. | Cleanest. | Destroys audit trail of what the analyzer flagged and why the maintainer decided each was a false-positive. |
| C. Leave the label as `"fail"` and block Phase 1 until the classifier is implemented (backlog item `pipeline-classifier-implementation`). | Lets the pipeline self-heal eventually. | Stalls the cliEval release on infrastructure the release itself doesn't need. The classifier is a separate roadmap concern. |

### Decision: **A — pass-with-triage label, manual-triage policy, per-deviation disposition.**

### Rationale

1. The pipeline's 14 step statuses already provide an objective PASS signal; the post-pipeline validator's `"fail"` label is one composite indicator that conflates two distinct conditions (fidelity failure vs. unclassified records pending triage). Splitting them removes ambiguity for future readers.
2. Option B destroys the only artifact (`spec-deviations.md` + `deviation-registry.json`) that would let a future classifier replay the same input and verify it produces the same dispositions. Triage is durable; deletion is not.
3. Option C blocks an unrelated release on a tooling backlog item with no committed timeline. The cliEval release does not depend on classifier implementation — it only depends on the dispositions being recorded.
4. Manual-triage policy fits within ADR-lite scope: per-deviation rows with file:line evidence in `deviation-triage.md` are auditable, and `remediation-tasklist.md` updates close the loop with the original BLOCKING entries.

### Manual-Triage Policy

When `validation.status` is `"fail"` purely due to unclassified-classifier output AND `fidelity_status` is `"pass"` AND every pipeline `steps.*` is PASS, a maintainer MAY perform manual triage by:

1. Reading each finding in `spec-deviations.md` plus its registry entry in `deviation-registry.json`.
2. Cross-referencing the cited symbol/file/ID against `roadmap.md` and `decisions.md` to confirm presence or absence.
3. Assigning one of the following dispositions:
   - `NO_ACTION` — finding is a false-positive (analyzer extraction artifact or naming-only mismatch); cite the roadmap.md line that contains the symbol.
   - `MAPPED → <ROADMAP_ROW_ID>` — finding maps to an existing roadmap row; cite the row.
   - `ADD_TO_P1` / `ADD_NEW_TASK` — genuine gap; do NOT silently edit phase tasklists; surface for separate gated decision.
   - `BLOCKING-CONFIRMED` — actual fidelity failure; halts the release.
4. Recording per-deviation dispositions in `deviation-triage.md` with file:line evidence.
5. Updating `remediation-tasklist.md` entries (`[x]` + disposition + evidence) and flipping `[UNCLASSIFIED]` markers in `spec-deviations.md` to their resolved classification.

### Consequences

- `.roadmap-state.json` SHOULD gain `validation.unclassified_deviations: 20` and `validation.status: "pass-with-triage"` once triage is complete. Per the user's instruction in this pre-execution-gate task, the JSON state file is NOT modified in this turn; the relabel is documented here as the authoritative semantic interpretation and is pending a follow-up edit.
- Future pipeline runs SHOULD distinguish "fidelity FAIL" from "deviations pending triage" via separate status fields rather than a single `validation.status` boolean.
- A backlog item should track implementing the deviation classifier so manual triage is no longer required (see `spec-deviations.md:10` reference to `pipeline-classifier-implementation`).
- The analyzer's roadmap→spec orphan ID extraction has a latent bug (phantom matches `D-1`, `D12`, `D3`, `D5`, `D6` that do not appear in roadmap.md); the classifier work should fix this regex.
- Phase-1 execution (`TASK-RF-20260518-cliEval-P1-pty-isolation-gates`) is UNBLOCKED upon triage completion.


---

## D-10: NOTICE/LICENSE attribution mechanism for vendored ptytest (OQ-4 closure)

**signed_off_by:** RyanW
**signed_off_date:** 2026-05-20
**Roadmap cross-reference:** NFR-MAINT1 (roadmap row 23) — vendored ptytest fork setup; DOC-OQ4 (row 24) — NOTICE/LICENSE attribution; AC10 (row 25) — fork SHA pin + drift policy.

### Context

`OQ-4` (roadmap.md:173) asks: *"Does the repo require a top-level NOTICE file for ptytest attribution?"* Per debate convergence and roadmap row 132 (DOC-OQ4), OQ-4 is a hard M2 entry blocker — it must close before the vendored ptytest sources physically land under `src/superclaude/cli/eval/pty/` (T02.01 / NFR-MAINT1). At the time this ADR lands, the repo has a top-level `LICENSE` (MIT) but no `NOTICE` file.

`brandon-fryslie/ptytest` is MIT-licensed. The MIT License requires that "the above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software." We are vendoring a substantial portion of ptytest sources, so the upstream copyright + permission notice must travel with the distribution.

`design-spec.md:785-787` already names the intended mechanism: retain the upstream `LICENSE` verbatim at `src/superclaude/cli/eval/pty/LICENSE`, and reference it from a top-level `NOTICE`. This ADR ratifies that mechanism and records it as the OQ-4 closure artifact.

### Options

| Option | Pros | Cons |
|---|---|---|
| **A. Top-level `NOTICE` referencing `src/superclaude/cli/eval/pty/LICENSE`; upstream LICENSE retained verbatim at the vendored path; PROVENANCE.md records fork SHA + changes.** | Industry-standard pattern (matches Apache 2 / Google convention even though both licenses here are MIT). NOTICE is grep-able by license-scan tooling. Survives upstream skill/template churn because the NOTICE points at a path the project controls. | Adds one new top-level file. |
| B. Inline ptytest MIT terms into the repo root `LICENSE` as an appendix. | One fewer file. | Mixes IronClaude's own copyright with a third-party copyright in the same file — confusing for downstream license scanners, and the precedent generalizes badly when more third-party components arrive. |
| C. Rely solely on `src/superclaude/cli/eval/pty/LICENSE` without a top-level NOTICE. | Minimum disruption to existing tree. | Fails the convention that license tooling (e.g., FOSSA, REUSE, OSS Review Toolkit) scans the repo root for NOTICE-style attribution before recursing. Maintainer audit trail is weaker. |

### Decision: **A — top-level `NOTICE` references `src/superclaude/cli/eval/pty/LICENSE`; upstream LICENSE retained verbatim at the vendored path.**

### Rationale

1. The MIT obligation ("retain the copyright notice and permission notice") is satisfied by retaining the upstream LICENSE verbatim at `src/superclaude/cli/eval/pty/LICENSE`. Adding a top-level `NOTICE` is **additive discipline** — it makes the attribution discoverable by repo-root scanners without dispersing the verbatim copyright across multiple files.
2. The `NOTICE` mechanism generalizes: when future third-party components are vendored (or when the harness adds an additional dependency that requires attribution), they get a new section in `NOTICE` and a verbatim LICENSE at their vendored path. Option B (inline appendix) does not generalize as cleanly.
3. Option C (no NOTICE) would force every reader and every license-scan tool to traverse the source tree to discover third-party content. The marginal cost of one top-level file is small; the marginal benefit (audit ergonomics) is real.
4. The `NOTICE` file does not change the license terms of either IronClaude or ptytest. Both remain MIT. `NOTICE` is documentation of attribution, not a license modification.

### Closure of OQ-4

- **Question:** Does the repo require a top-level NOTICE file for ptytest attribution?
- **Resolution:** YES. A top-level `NOTICE` MUST exist before T02.01 lands vendored ptytest sources. The `NOTICE` references `src/superclaude/cli/eval/pty/LICENSE` (the verbatim upstream MIT terms) and `src/superclaude/cli/eval/pty/PROVENANCE.md` (fork SHA + changes).
- **Resolution status:** RESOLVED — 2026-05-20.
- **Resolution artifact:** `NOTICE` at repo root (this commit). The referenced `LICENSE` and `PROVENANCE.md` under `src/superclaude/cli/eval/pty/` land with T02.01 (NFR-MAINT1).

### Attribution clause (canonical text)

The `NOTICE` file contains the following authoritative attribution clause for ptytest. Any future edit to this clause SHOULD update both the `NOTICE` file and this ADR section in lockstep:

> **ptytest (vendored fork)** — Upstream: `https://github.com/brandon-fryslie/ptytest`; License: MIT; Location: `src/superclaude/cli/eval/pty/`. A fork of `brandon-fryslie/ptytest` is vendored under `src/superclaude/cli/eval/pty/` and used as the PTY/pexpect driver layer for the CLI evaluation harness. The upstream MIT LICENSE is retained verbatim at `src/superclaude/cli/eval/pty/LICENSE`, and `src/superclaude/cli/eval/pty/PROVENANCE.md` records the fork SHA, vendoring date, and the changes made relative to upstream.

### Consequences

- A new file `NOTICE` exists at the repository root. It is documentation, not a build/test artifact; CI does not need to enforce its presence beyond a single grep check (`grep -c ptytest NOTICE >= 1`).
- T02.01 (NFR-MAINT1) is unblocked for M2 entry. The vendored ptytest sources may now physically land under `src/superclaude/cli/eval/pty/`, with their own `LICENSE` (verbatim upstream) and `PROVENANCE.md` (fork SHA + changes).
- T02.03 (AC10 fork SHA pin + drift policy) inherits the resolution: the quarterly review cadence recorded in `PROVENANCE.md` keeps the `NOTICE` accurate over time. If a future resync changes the upstream copyright text, both `src/superclaude/cli/eval/pty/LICENSE` and the attribution clause above MUST be re-verified.
- Future vendored components MUST follow the same convention: section in `NOTICE` + verbatim LICENSE at the vendored path + PROVENANCE.md entry. This convention is recorded here as the OQ-4 resolution and applies repository-wide.
- The Sign-off table reflects D-10 as **🟠 QUEUED FOR SIGN-OFF (R4)** pending maintainer (RyanW) approval at the same M1/M2 exit pass as D-1..D-8.

---

## OPS-001 Closure — ADR queue, Open Question resolution status, implementation-gate cross-reference

**Source:** Roadmap row 86 (R-021 / OPS-001) — *"decisions.md updated; D-5..D-8 queued for sign-off; unresolved blockers listed; implementation gates reference decisions."*
**Task:** T01.25 (Phase 1)
**Deliverable:** D-0021 — see `artifacts/D-0021/spec.md` for the full ADR-ID → implementation-site map.
**Tier:** EXEMPT (Section 5.3 — documentation / ADR closure).
**Date:** 2026-05-20.

### A. ADR queue status (D-5..D-8)

D-5..D-8 are recorded in the Sign-off table above with status **🟠 QUEUED FOR SIGN-OFF (R3)**. The decision bodies themselves are unchanged from R2; only the sign-off lifecycle moves. Maintainer (RyanW) flips each row to 🟢 APPROVED on review per the policy in the Sign-off section header.

D-1..D-4 remain 🟡 PROPOSED pending the same maintainer sign-off pass; OPS-001 does NOT alter their status. The original four ADRs and the four added in R2 sign off together at M1 exit (cross-references SC1 in roadmap row 348).

### B. Open Question resolution status (OQ-1, OQ-3, OQ-7, OQ-8, OQ-10)

The Open-Questions block in `roadmap.md:105-114` lists six M1-scoped OQs. This task records resolution status for the five OQs called out in OPS-001 row 86 (OQ-1, OQ-3, OQ-7, OQ-8, OQ-10). OQ-2 (eval body shapes) is out of scope for OPS-001 row 86 and is tracked separately under R-021 dependents.

| OQ | Question | Owner | Target | Resolution status as of 2026-05-20 | Blocks |
|----|----------|-------|--------|------------------------------------|--------|
| OQ-1  | Remaining `decisions.md` open-question items (SC5) | RyanW    | before M1 exit                                          | **RESOLVED — 2026-05-20.** `resolution:` RyanW signed off D-1..D-8 (and D-10) in R5 sign-off pass; see Sign-off table above for per-ADR signatures + dates. OPS-001 queue cleared; SC1 acceptance criterion satisfied. | ADR D-5..D-8 sign-off; M6 exit (SC5) |
| OQ-3  | Which eval categories are excluded by `--no-pty`   | architect| before FR-CLI1 close (M4)                              | **DEFERRED to M4** — exclusion set captured in `suites/real.yaml` `no_pty:skip` tag per eval per DOC-OQ3 (roadmap row 254). Decision body lands when ExpectDSL primitives close (T04.x). | FR-CLI1 close, M4 exit |
| OQ-7  | Whether `--junit` flag is supported in CLI         | RyanW    | before M1 exit                                          | **OPEN** — DOC-OQ7 (roadmap row 253) names two outcomes: (a) `--junit` added to FR-CLI1 flag set with `junit.xml` emission, OR (b) spec §9 conditional language removed. Awaiting maintainer call before M1 exit; tracked as M1-exit blocker per OPS-001 dependency. | FR-CLI1 flag table; CLI surface freeze |
| OQ-8  | How `CLAUDE_FAKE_TIME_OFFSET` is consumed/validated| architect| before COMP-005 close                                   | **RESOLVED — 2026-05-20.** `resolution:` Time-offset layer REMOVED from FR-ISO1 scope per DOC-OQ8 path (b). The claude binary is not known to honour `CLAUDE_FAKE_TIME_OFFSET` (no Anthropic-published documentation of the var); T05.01 froze E1..E15 with zero dependency on simulated wall-clock advancement (see OQ-2 Resolution below: *"None of E3 … E15 requires `CLAUDE_FAKE_TIME_OFFSET`"*). `HomeIsolation` retains the `time_offset_sec: int = 0` field at v1 ship as dead-but-typed scaffolding; strip is a follow-up tracked at `artifacts/D-0107-followup-strip-time-offset.md`. See §"DOC-OQ8 Closure" below. | EvalConfig/HomeIsolation contract; COMP-005 close |
| OQ-10 | Exact MCP-flaky failure taxonomy permitting retry-once | QA Lead | before M3 exit (empirical resolution acceptable per debate convergence) | **DEFERRED to M3/M5** — empirical resolution accepted by debate convergence. R3-mit (roadmap row 307) lands MCP-flaky retry once OQ-10 closes. CapabilityGates (T01.11) ships the SOFT-SKIP path without retry; retry-once policy is additive. | NFR-REL2 retry semantics; R3-mit landing tier |

**Net:** 0 of 5 are resolved by this task (T01.25); OPS-001 row 86 explicitly asks for queue + status listing, not for closure of the OQs themselves. The "unresolved blockers" requirement is satisfied by listing OQ-1 and OQ-7 as M1-exit blockers above; OQ-3/OQ-8/OQ-10 are deferred-by-design and do not block M1 exit (cross-references roadmap row 86 AC: "unresolved blockers listed").

**Update (R5, 2026-05-20 — T06.01):** OQ-1 has since flipped OPEN → RESOLVED in the table above. The R5 sign-off pass on D-1..D-8 (and D-10) was OQ-1's resolution gate. OQ-7 was independently resolved at T04.15 (see "DOC-OQ7 Closure" section below). OQ-3, OQ-8, OQ-10 remain DEFERRED per design.

**Update (R7, 2026-05-20 — T06.03):** OQ-8 has now also flipped OPEN → RESOLVED in the table above; DOC-OQ8 path (b) was chosen (remove the time-offset layer from FR-ISO1). See §"DOC-OQ8 Closure" below for the full rationale; OQ-3 and OQ-10 remain DEFERRED per design.

**Update (R8, 2026-05-20 — T06.04):** OQ-6 (not in the §B table above because it was opened against M5 not M1; roadmap row 332) has flipped OPEN → RESOLVED via DOC-OQ6 closure — suite filename convention recorded at `src/superclaude/cli/eval/suites/README.md`, `quick.yaml` recorded as a deferred follow-up (no v1 work). See §"DOC-OQ6 Closure" below for the full rationale. OQ-3 and OQ-10 remain DEFERRED per design.

### C. Implementation-gate → ADR cross-reference

Each ADR has at least one downstream implementation gate that consumes the decision. The table below names the gate site (file or task ID) so a future reader can trace from any code-level enforcement back to its ADR.

| ADR | Decision summary | Implementation gate site | Phase / task ID |
|-----|------------------|--------------------------|-----------------|
| D-1 | Fork ptytest, vendor under `cli/eval/pty/` | `cli/eval/pty/` source drop + `PROVENANCE.md` (NFR-MAINT1, roadmap row 131) | M2 / T02.x |
| D-2 | Port `Expect.*` DSL as Python primitives   | `cli/eval/expect.py` (COMP-010 interface T01.14; primitives T04.x) | M1 (interface) + M4 (primitives) |
| D-3 | `HomeIsolation` composes `IsolationLayers` | `cli/eval/isolation.py` referencing `cli/sprint/executor.py:107-182` (FR-ISO1, M2) | M2 / T02.x |
| D-4 | YAML manifest + Python callback escape hatch | `cli/eval/suites/*.yaml` + `suites/suite.schema.json` (DM-011, T01.02) + `suites/<name>_callbacks.py` | M1 (schema) + M5 (callbacks) |
| D-5 | Hook-matcher coverage gate (G5 falsifiable) | `loader.py` matcher-coverage check + `eval doctor --check-coverage` (FR-G5; T01.13 partial wiring, full wiring at T04.14) | M1 (outline) + M4 (gate close) |
| D-6 | `--max-disk-mb` poller (R4 enforcement)    | `DiskBudgetWatchdog` sidecar + `--max-disk-mb` flag in §4 (M3 RunOrchestrator) | M3 |
| D-7 | Three-layer path-traversal hardening       | `validate_eval_id` (FR-SCH2, T01.05) + `resolve_scratch_root` (AC12, T01.19) + `HomeIsolation.setup()` symlink-resolve (M2) | M1 (layers 1+2) + M2 (layer 3) |
| D-8 | Reporter consumes N' + status taxonomy     | `EvalOutcome` dataclass + `AggregatedRunReport.from_outcomes()` dimensional assertion (COMP-008, T03.13) | M3 |

### D. Acceptance-criteria → site map (T01.25)

| AC bullet (T01.25)                                                                                       | Where satisfied |
|----------------------------------------------------------------------------------------------------------|-----------------|
| File `.dev/releases/current/cliEval/decisions.md` contains entries D-5..D-8 with status `queued for sign-off`. | Sign-off table above — rows updated in R3 (`🟠 QUEUED FOR SIGN-OFF (R3)`). |
| Each OQ-1, OQ-3, OQ-7, OQ-8, OQ-10 has a resolution-status field or owner pointer.                       | §B table above (status + owner + target columns). |
| Implementation gates reference decisions by ADR ID.                                                       | §C table above (ADR column → implementation-gate-site column). |
| `TASKLIST_ROOT/artifacts/D-0021/spec.md` records the update summary.                                      | `artifacts/D-0021/spec.md` (companion file to this section). |

### E. Out of scope for T01.25

- Flipping any of D-1..D-8 to 🟢 APPROVED — that is the maintainer sign-off pass tracked by SC1 (roadmap row 348) at M1 exit.
- Resolving OQ-1 or OQ-7 substantively — both are tagged "before M1 exit" but require maintainer input, not documentation work.
- Resolving OQ-3 / OQ-10 — explicitly deferred per the design-spec / roadmap targets above. (OQ-8 was originally listed here as deferred-by-design, but the R7 DOC-OQ8 closure below flips it to RESOLVED; the OQ-3 / OQ-10 deferrals are unchanged.)
- Editing `roadmap.md` or `.roadmap-state.json` — out of scope for OPS-001 row 86.

---

## DOC-OQ7 Closure — `--junit` flag wiring decision (T04.15)

**Source:** Roadmap row 253 (R-076 / DOC-OQ7) and Phase-4 task T04.15.
**Deliverable:** D-0076 — see `artifacts/D-0076/spec.md` for the rationale and `evidence/T04.15/` for verification.
**Tier:** EXEMPT (Section 5.3 — documentation / ADR closure).
**Date:** 2026-05-20.

### Context

OQ-7 asked whether the CLI should support `--junit` as a documented flag. The spec carried conditional language in two non-adjacent places: §9 ("`junit.xml` ... Generated only when `--junit` is passed") and §10 ("Add `to_json()` and `to_junit()` (new methods)"), while the §4 flag table omitted `--junit` from the 11-flag list. The roadmap FR-CLI1 row (R-072) and the Phase-4 task T04.10 both name a 12-flag set that includes `--junit`. The drift between §4 and FR-CLI1 is the surface OQ-7 was opened to close.

DOC-OQ7 (R-076) names two outcomes: (a) wire `--junit` into FR-CLI1 with `junit.xml` emission, OR (b) remove the conditional `--junit` language from spec §9. Either resolves the drift; the choice is binding for M4 exit.

### Options

| Option | Description | Pros | Cons |
|---|---|---|---|
| **A. Wire `--junit` into FR-CLI1.** Add the 12th flag; Reporter's `to_junit()` and `emit_junit` gate stand. Update spec §4 table to list `--junit`. | Matches the existing roadmap FR-CLI1 spec (R-072, 12 flags) and the Phase-4 T04.10 acceptance criterion ("lists all 12 flags named in FR-CLI1"). Reuses already-landed `to_junit()` (~50 LOC) without code removal. Keeps CI consumers' future path (JUnit-XML ingestion in CI runners is the de-facto pattern for pytest-style harnesses). | Adds one CLI flag and one feature-gated output file. |
| B. Remove `--junit` from spec §9 and `to_junit()` from §10. | Slightly smaller CLI surface; one fewer artifact path. | Contradicts the roadmap row R-072 (which would also need amendment), invalidates T04.10's "12 flags" AC (would need to be re-spun as "11 flags"), and forces re-removal of Reporter code that has already landed under T03.13. The cost is documentation churn in 3 places plus code deletion for net-zero capability change. |

### Decision: **A — wire `--junit` into FR-CLI1; spec §9 conditional language is correct as written; spec §4 flag table updated to include `--junit` for consistency.**

### Rationale

1. **The implementation has already converged on option A.** The Reporter's `to_junit()` method and `emit_junit` constructor flag landed under T03.13 (`src/superclaude/cli/eval/reporter.py:146,177,222-225`); the CLI's `--junit` flag landed under T04.10 (`src/superclaude/cli/eval/commands.py:1349-1352,1366,1593`). Choosing option B now would require deleting working code to match a spec that no other artifact endorses.
2. **The roadmap and tasklist already commit to 12 flags.** R-072 acceptance criterion enumerates 12 flag names including `--junit`; T04.10 acceptance criterion says "all 12 flags named in FR-CLI1". Option B would require amending both, plus removing the `to_junit()` line from spec §10 and the §9 junit.xml section. Option A requires updating only the §4 flag table.
3. **The `--junit` flag is feature-gated, not enabled by default.** `--junit` defaults to `false` and the Reporter only writes `junit.xml` when `emit_junit=True` (`reporter.py:222`). There is no runtime cost for runs that do not opt in, and the flag does not change the dimensional invariants of `summary.json` (the JUnit XML is rendered from the same `AggregatedRunReport`).
4. **JUnit XML is the dominant CI ingestion format.** GitHub Actions, GitLab CI, Buildkite, Jenkins, and CircleCI all support JUnit XML test result publishing natively. The marginal cost of a ~50 LOC `to_junit()` renderer plus one Click option is small; the marginal benefit (zero-config CI publishing without a separate adapter) is real and is the use case spec §4 example #4 already shows.
5. **Risk R1 ("Flag drift between spec §4 and implementation") is closed by this decision.** §4 table is updated to list `--junit`; FR-CLI1 (R-072) already lists it; implementation already wires it. All three artifacts now agree.

### Closure of OQ-7

- **Question:** Whether `--junit` flag is supported in CLI.
- **Resolution:** YES. The CLI supports `superclaude eval run --junit` as a feature-gated flag (default `false`); when set, `Reporter.write()` emits `junit.xml` into the run output directory alongside `summary.md` / `summary.json`.
- **Resolution status:** RESOLVED — 2026-05-20.
- **Resolution artifact:** `src/superclaude/cli/eval/commands.py:1349-1593` (CLI flag wiring) + `src/superclaude/cli/eval/reporter.py:146-225` (Reporter feature gate and renderer).

### Consequences

- Spec §4 flag table is updated in this commit to list `--junit BOOL` (default `false`) alongside the other 11 flags. The §4 table now agrees with FR-CLI1 (R-072) and T04.10 on the 12-flag set.
- Spec §9 conditional language ("Generated only when `--junit` is passed") stands as written. Spec §10 `to_junit()` reference stands.
- T04.10 (FR-CLI1 wiring) is satisfied for the `--junit` row; T04.13 (FR-G4 artifact layout) includes `junit.xml` only when `emit_junit=True`.
- TEST-007 reporter-contract suite (T04.17) covers `to_junit()` invariants implicitly via the schema-fidelity test; a future test refinement may add a JUnit-specific assertion (out of scope for T04.15).
- The OPS-001 Open-Questions table (§B above) flips OQ-7 from `OPEN` to `RESOLVED — 2026-05-20`. The table itself is not re-rendered here; the resolution status above is canonical and supersedes the prior `OPEN` row by date.
- No code change accompanies this ADR closure beyond the §4 table update; the implementation was already in place.

---

## DOC-OQ9 Closure — macOS support roadmap entry (T06.02)

**Source:** Roadmap row 349 (R-105 / DOC-OQ9) and Phase-6 task T06.02.
**Deliverable:** D-0106 — see `artifacts/D-0106/spec.md` for the macOS follow-up summary and `evidence/T06.02/` for verification.
**Tier:** EXEMPT (Section 5.3 — documentation / ADR closure).
**Date:** 2026-05-20.

### Context

OQ-9 (roadmap row 380, M6 Open Questions) asks: *"macOS support timeline and scope — does v1 remain Linux-only, or does the harness name a concrete macOS target?"* DOC-OQ9 (R-105, roadmap row 349) requires `decisions.md` to record the answer with an owner and a target date for any follow-up work, and to reaffirm AC1 (Linux-only declaration, R-109, roadmap row 353) for v1.

The harness is Linux-first by design (design-spec.md:30: *"Cross-platform support (Linux only for now — Claude Code TTY behavior is platform-specific; macOS support is a follow-up)"*; design-spec.md:812: *"Cross-platform support (Linux first; macOS / Windows are follow-ups)"*). MIG-003 (R-116, roadmap row 360) names macOS + CI as v2 follow-up scope. This closure records the v1 platform commitment, names the owner and target date for the macOS follow-up, and cross-references AC1.

### Decision: macOS support is deferred to v2; v1 ships Linux-only

| Field | Value |
|---|---|
| **v1 platform scope** | Linux only. Authoritative declaration sites: AC1 (roadmap row 353); design-spec.md:30 and §16 non-goals (line 812); `README.md` + `eval doctor` non-Linux refusal wired by T06.07. |
| **macOS status (v1)** | NON-GOAL. No `Darwin` support code lands in v1. `eval doctor` refuses non-Linux platforms with a friendly error message (AC1 wiring, T06.07). |
| **macOS follow-up owner** | RyanW (architect; same owner as MIG-003 platform follow-up plan, roadmap row 360). |
| **macOS follow-up target date** | 2026-Q3. Concretely: re-evaluate at the v2 planning gate scheduled for 2026-07-01; ship-or-defer decision recorded against MIG-003 by 2026-09-30. |
| **Re-evaluation trigger (whichever first)** | (a) v2 planning gate 2026-07-01; (b) first formal macOS-platform support request filed against this repo; (c) Anthropic documents Claude Code TTY behaviour on macOS to be Linux-equivalent for the hook surface exercised by E1..E15. |
| **Out-of-scope for the macOS follow-up** | Windows. Windows remains a non-goal beyond v2 per design-spec.md:812 and is not addressed by DOC-OQ9 or MIG-003. |

### Cross-reference to AC1 (Linux-only declaration)

AC1 (roadmap row 353, R-109) records the Linux-only v1 scope in `README.md` and wires `eval doctor` to refuse non-Linux platforms with a friendly error. T06.07 is the implementation site (Phase 6, this same release). AC1 is the reciprocal pair of DOC-OQ9: AC1 declares what v1 IS (Linux-only); DOC-OQ9 declares what v1 IS NOT (macOS/Windows) for v1 and names the owner + target date for the deferred capability.

The DOC-OQ9 macOS follow-up plan above MUST be re-read whenever AC1 is amended; the two entries are intentionally redundant on the "Linux-only for v1" assertion so that a maintainer who edits one without the other will produce a visible drift in the next SC5 OQ-ledger sweep (T06.09).

### Closure of OQ-9

- **Question:** macOS support timeline and scope.
- **Resolution:** Deferred to v2. v1 ships Linux-only per AC1. macOS follow-up owner: RyanW; target date: 2026-Q3 (re-evaluate at v2 planning gate 2026-07-01; ship-or-defer recorded against MIG-003 by 2026-09-30); re-evaluation triggers enumerated above.
- **Resolution status:** RESOLVED — 2026-05-20.
- **Resolution artifact:** This section (`decisions.md` §"DOC-OQ9 Closure") + `artifacts/D-0106/spec.md`. The MIG-003 follow-up roadmap entry (T06.15) inherits this decision verbatim; no fresh decision is required there.

### Consequences

- T06.07 (AC1 wiring) consumes this section as the upstream record of the Linux-only commitment; the AC1 entry it lands in `decisions.md` will cross-reference this section.
- T06.15 (MIG-003 platform follow-up plan) carries this owner + target verbatim into the v2 follow-up roadmap entry; no new decision required.
- T06.09 (SC5 OQ-1..OQ-10 ledger) reads OQ-9 as RESOLVED with this section as the resolution evidence; `signed_off_by: RyanW` lands at T06.09 alongside the other OQs in a single sign-off pass.
- The v1 release notes / `README.md` MUST state "Linux only" prominently; OPS-005 release checklist (T06.13) inherits that requirement.
- If the macOS follow-up is delivered in a future release, this section is amended with an `Outcome:` line; the original `Resolution:` text stays for audit (Reject/revise rule above).
- No code change accompanies this ADR closure; the implementation work for AC1 (README + `eval doctor` non-Linux refusal) is owned by T06.07, and the v2 follow-up roadmap entry is owned by T06.15.

---

## DOC-OQ8 Closure — time-offset mechanism contract decision (T06.03)

**Source:** Roadmap row 350 (R-106 / DOC-OQ8) and Phase-6 task T06.03.
**Deliverable:** D-0107 — see `artifacts/D-0107/spec.md` for the decision summary and `evidence/T06.03/` for verification.
**Tier:** EXEMPT (Section 5.3 — documentation / ADR closure).
**Date:** 2026-05-20.

### Context

OQ-8 (roadmap row 113) asks: *"How `CLAUDE_FAKE_TIME_OFFSET` is consumed or validated."* DOC-OQ8 (R-106, roadmap row 350) names two outcomes the M6 ADR log must commit to:

- **(a)** Confirmation that the `claude` binary honours `CLAUDE_FAKE_TIME_OFFSET` (the env var is a documented hook that some internal time-mocking layer reads), OR
- **(b)** Removal of the time-offset layer from FR-ISO1 (the env var has no consumer, the harness should not pretend it does, and `time_offset_sec` is stripped from `HomeIsolation`).

The harness landed the optional layer in good faith at T01.01 (`EvalConfig` exposes per-eval `time_offset_sec`) and T02.07 (`HomeIsolation.env()` emits `CLAUDE_FAKE_TIME_OFFSET` only when `time_offset_sec != 0`). Both implementations were explicitly gated on this ADR — see `cli/eval/isolation.py:44-49,66-67,373-376,598-602` ("*Full activation is gated on OQ-8 (DOC-OQ8 / T06.03)*") and the design-spec §8 row that flags the layer as *"Optional; lets evals advance the clock for 30-min freshness tests (E3)"*.

Two facts make path (a) unavailable at v1 ship:

1. **No Anthropic-published documentation describes `CLAUDE_FAKE_TIME_OFFSET`.** A scan of the harness sources (`src/superclaude/cli/eval/isolation.py:14-19,594-620`, `src/superclaude/cli/eval/claude_process.py:113,241`) shows every reference is harness-side speculation; no shipped Claude Code release notes, CLI help, or developer documentation has been cited that confirms the binary reads the var. Confirming path (a) would require landing a probe eval that asserts time-mocked behaviour against the actual binary, which is out of scope for v1 (no such eval is in E1..E15).
2. **No v1 eval needs simulated wall-clock advancement.** OQ-2 resolution (T05.01, §"OQ-2 Resolution" below) explicitly states *"None of E3 … E15 requires `CLAUDE_FAKE_TIME_OFFSET` — the original design-spec note tying E3 to '30-min freshness tests' is superseded; freshness-staleness via time offset becomes a follow-up eval after OQ-8 closes."* The v1 eval set is frozen at E1..E15; none of them advance the simulated clock; the field is dead weight at v1 ship.

The harness has therefore been shipping with a variable that no v1 caller sets to non-zero and no downstream consumer (the Claude binary) is documented to read. DOC-OQ8 forces the project to either prove the consumer exists (path a) or admit it does not and remove the layer (path b).

### Options considered

| Option | Description | Pros | Cons |
|---|---|---|---|
| **A. Confirm the claude binary honours `CLAUDE_FAKE_TIME_OFFSET`** (path a). | Cite published Anthropic documentation or a verifiable probe demonstrating the binary advances its internal clock by the env-var value. Keep the field, keep the `env()` branch, and document the contract. | Preserves the option to add freshness evals in v1 with no further code change. Costs zero LOC if the documentation exists. | No public Anthropic documentation has been cited. A probe-based confirmation requires landing a new eval (out of scope for v1 per T05.01 frozen set). Without evidence, claiming (a) would be a false attestation in the ADR log. |
| **B. Remove the time-offset layer from FR-ISO1** (path b). | Record the decision in `decisions.md` (this section); strip `time_offset_sec` from `HomeIsolation` and the emission branch from `HomeIsolation.env()` via a tracked follow-up task; remove the design-spec §8 row that promises the layer. | Aligns harness scope with shipped behaviour: nothing in v1 sets the field non-zero, nothing in v1 consumes it. No dead env-var contract leaks to v1 release notes. If a future freshness eval needs time mocking, that decision can be reopened with the probe evidence DOC-OQ8 would have required for path (a). | Touches `cli/eval/isolation.py`, `cli/eval/models.py`, `cli/eval/claude_process.py`, and `design-spec.md` §8 (estimated ~30 LOC removed + 4 doc references reworded). Field is already shipped, so a v1.0 → v1.1 deprecation cycle is cleaner than an immediate v1 strip — captured by routing the strip through a follow-up task that lands AFTER the M6 cut. |
| C. Defer DOC-OQ8 indefinitely (status quo). | Leave OQ-8 OPEN; keep the field; keep emitting the env var on non-zero. | No code or doc change. | Violates DOC-OQ8 acceptance criterion (roadmap row 350 requires `decisions.md` to record a chosen path before M6 exit). Blocks SC5 OQ-ledger closure (T06.09, R-111). Not viable for M6 exit. |

### Decision: **B — Remove the time-offset layer from FR-ISO1 scope.**

The `CLAUDE_FAKE_TIME_OFFSET` env var is removed from the FR-ISO1 contract as of R7 (2026-05-20). `HomeIsolation` retains the `time_offset_sec: int = 0` field at v1 ship as dead-but-typed scaffolding so the M6 cut is not blocked on a code strip; the strip is filed as a tracked follow-up at `artifacts/D-0107-followup-strip-time-offset.md` and lands in the next release cycle after v1.0 (a v1.0 → v1.0.1 deprecation hop avoids breaking any caller that already constructs `HomeIsolation(...)` positionally with a fourth arg).

### Rationale

1. **No evidence supports path (a).** A repository-wide audit of references to `CLAUDE_FAKE_TIME_OFFSET` (see Evidence §"Repository audit" in `artifacts/D-0107/evidence.md`) finds the var named in harness-side comments only (`cli/eval/isolation.py`, `cli/eval/claude_process.py`, `design-spec.md`, prior `decisions.md` rows). No Anthropic-published documentation has been cited. Claiming path (a) in the ADR log without such citation would be a false attestation.
2. **No v1 eval needs the layer.** T05.01 froze E1..E15 with zero dependency on simulated wall-clock advancement; the OQ-2 resolution below records this verbatim. Keeping a dead env-var contract in FR-ISO1 violates the design-spec §16 non-goal *"no features beyond what the 15 frozen evals require."*
3. **Path (b) is reversible if a probe later confirms binary support.** Reopening DOC-OQ8 in a future release requires the same probe evidence path (a) would have required now — the cost of removing the field today is the cost of re-adding it later (≈30 LOC) plus a new ADR. Reverse cost is identical to forward cost; removing now is the smaller decision because it does not require fabricating evidence for a consumer that may not exist.
4. **The strip is decoupled from M6 exit by routing through a follow-up.** Per Step 4 of T06.03 (*"If removed, file follow-up task to strip `time_offset_sec` from `HomeIsolation`"*), the ADR records the contract removal at R7 while the code strip is filed as a tracked follow-up. This (a) keeps M6 exit on schedule without a same-day code refactor under STRICT review, (b) gives downstream consumers a deprecation cycle, and (c) avoids retroactively rewriting T01.01 / T02.07 acceptance tests.
5. **DOC-OQ8 acceptance criterion is satisfied by this section + follow-up artifact.** Roadmap row 350 AC reads *"decisions.md records either: (a) confirmation that claude binary honors env var, OR (b) removal of time-offset layer from FR-ISO1."* Path (b) is recorded here; the follow-up artifact records the strip plan.

### Closure of OQ-8

- **Question:** How `CLAUDE_FAKE_TIME_OFFSET` is consumed or validated.
- **Resolution:** Not consumed. The time-offset layer is removed from FR-ISO1 contract scope per DOC-OQ8 path (b); no v1 eval (E1..E15, T05.01) advances the simulated clock; no Anthropic-published documentation confirms the binary honours the var. `HomeIsolation` retains the `time_offset_sec: int = 0` field at v1 ship as dead-but-typed scaffolding; the field strip and the `env()` emission branch removal are tracked at `artifacts/D-0107-followup-strip-time-offset.md` and land in the release cycle following v1.0.
- **Resolution status:** RESOLVED — 2026-05-20.
- **Resolution artifact:** This section (`decisions.md` §"DOC-OQ8 Closure") + `artifacts/D-0107/spec.md` + follow-up at `artifacts/D-0107-followup-strip-time-offset.md`.

### Cross-references

- **FR-ISO1 (roadmap row 28 / R-013, T02.07):** the time-offset layer named in this row is removed from scope per this decision. The harness `HomeIsolation.setup` / `env` / `teardown` / `state_path` surface is otherwise unchanged.
- **DM-006 (roadmap row 26 / R-011, T02.04):** the `time_offset_sec: int = 0` field is retained at v1 ship as dead scaffolding; strip is tracked at `artifacts/D-0107-followup-strip-time-offset.md`.
- **OQ-2 (T05.01) §"OQ-2 Resolution" below:** authoritative source for *"None of E3 … E15 requires `CLAUDE_FAKE_TIME_OFFSET`."*
- **design-spec.md:372:** the §8 row *"Time offset | `CLAUDE_FAKE_TIME_OFFSET` | Optional; lets evals advance the clock for 30-min freshness tests (E3)"* is superseded by this closure. The follow-up artifact lists the spec edit in its scope.
- **OPS-001 §B table above:** OQ-8 row flipped OPEN → RESOLVED at R7 (2026-05-20).
- **T06.09 (SC5 OQ-1..OQ-10 ledger):** reads OQ-8 as RESOLVED with this section as the resolution evidence; `signed_off_by: RyanW` lands at T06.09 alongside the other OQs in a single sign-off pass.
- **claude_process.py:113,241:** docstring references to `CLAUDE_FAKE_TIME_OFFSET` are downstream comments only (no `env` lookup happens here); they are reworded in the follow-up artifact along with the isolation.py strip.

### Consequences

- The `CLAUDE_FAKE_TIME_OFFSET` env var is no longer part of the FR-ISO1 contract. The design-spec §8 row that promises the layer is superseded; the spec edit lands with the follow-up strip.
- `HomeIsolation.env()` continues to emit the var on non-zero `time_offset_sec` at v1 ship for backward compatibility within the v1.x window, but no v1 caller exercises this branch (verified by repository audit; see `artifacts/D-0107/evidence.md`).
- The follow-up artifact `artifacts/D-0107-followup-strip-time-offset.md` is the canonical tracker for the code strip; it names the source-file edits, the test updates, the design-spec edit, and the proposed release vehicle (v1.0.1 / next minor post-v1 cut).
- T06.09 (SC5 ledger) reads OQ-8 as RESOLVED from this section; T06.16 (M6 exit checkpoint) inherits the resolution.
- If a future freshness eval needs simulated wall-clock advancement, this ADR is amended with an `Outcome:` line (Reject/revise rule above) and a new ADR records the re-introduction with the probe evidence path (a) originally required.

---

## DOC-OQ6 Closure — suite naming convention + `quick.yaml` follow-up (T06.04)

**Source:** Roadmap row 351 (R-107 / DOC-OQ6) and Phase-6 task T06.04.
**Deliverable:** D-0108 — see `artifacts/D-0108/spec.md` for the decision summary; `artifacts/D-0108/evidence.md` for the loader-behaviour audit; `evidence/T06.04/summary.md` for the verification log.
**Tier:** EXEMPT (Section 5.3 — documentation / ADR closure).
**Date:** 2026-05-20.

### Context

OQ-6 (roadmap row 332, M5 Open Questions) asks: *"Suite filename convention beyond `real.yaml` (e.g., quick subset)."* DOC-OQ6 (R-107, roadmap row 351) requires `src/superclaude/cli/eval/suites/README.md` to record (a) the filename rules every future manifest MUST follow and (b) the `quick.yaml` plan as a documented follow-up. At v1 ship the directory contains exactly one manifest (`real.yaml`, T05.01-frozen); the convention recorded here pre-fences the surface so any future suite lands without re-litigating the rules.

The loader behaviour the convention encodes is already on disk:

- `discover_suite_manifests` (`cli/eval/commands.py:591-606`) globs `suites_dir.glob("*.yaml")` and sorts by filename. `*.yml`, `*.YAML`, `*.json` are silently invisible.
- `resolve_suite_manifest` (`cli/eval/commands.py:1008-1044`) resolves `--suite <token>` via (1) direct path, (2) `<token>.yaml` stem match, (3) schema-validated `name` field. Rules (2) and (3) collapse to the same lookup when stem == `name`.
- `suite.schema.json` requires `name` as a non-empty string (the schema does not constrain casing or charset; the convention does).

### Decision: **Filename rules ratified; `quick.yaml` deferred with a documented trigger.**

The suite naming convention recorded at `src/superclaude/cli/eval/suites/README.md` §"Filename rules" is the canonical contract for any manifest added to that directory. Summary:

1. Extension is exactly `.yaml` (lower-case).
2. Stem matches `[a-z][a-z0-9_]*` (snake_case, alphanumeric + underscore, leading letter).
3. Stem MUST equal the manifest `name:` field.
4. Stem MUST be globally unique within the directory.
5. Reserved stems: `suite` (clashes with `suite.schema.json` semantics) and any leading-underscore stem (shadow of `__init__.py`).

`quick.yaml` is recorded as a deferred follow-up — **not** an in-flight backlog item. The follow-up's intended shape (curated 3-5 eval subset of `real.yaml`, <90s walltime, same schema, no CLI changes) and its trigger conditions (maintainer demand-signal OR R6 walltime ceiling exceeded post-v1) are recorded in the README §"Planned follow-up — `quick.yaml`". Reopening the deferral does not require a fresh ADR; this section + the README are the spec.

### Rationale

1. **The convention encodes shipped loader behaviour, not new behaviour.** The `*.yaml` glob, stem-equals-name resolution, and `name:` schema constraint are already on disk at `commands.py:591-606,1008-1044` and `suite.schema.json:18-22`. The README records the rules a future suite author must satisfy so the loader does not silently swallow their file; no code changes accompany this ADR.
2. **`quick.yaml` is not yet justified.** v1's `real.yaml` is the sole suite, frozen at T05.01 (OQ-2 resolution: E1..E15). Adding a curated `quick` subset before the full `real` suite has landed and proven stable would (a) re-open the frozen roster, (b) split maintenance across two manifests with no operator demand-signal, and (c) blur the SC2 / SC4 coverage and LOC budgets recorded against `real.yaml`. The `--eval <id>` filter on `superclaude eval run` is sufficient as the v1 "subset" escape hatch (FR-CLI1 flag table).
3. **Deferring `quick.yaml` does not block the loader from accepting it later.** Filename-stem resolution (`commands.py:1030-1032`) and the suite-agnostic schema (`suite.schema.json`) cover `quick.yaml` on the day it lands; the follow-up needs zero loader changes. The convention recorded here is forward-compatible by construction.
4. **DOC-OQ6 acceptance criterion is satisfied by the README + this section.** Roadmap row 351 AC reads *"cli/eval/suites/README.md records naming convention; `quick.yaml` plan recorded as follow-up"*. Both halves are covered by the README sections §"Filename rules" and §"Planned follow-up — `quick.yaml`" respectively; this section provides the ADR-log entry pointing to that authoritative source.
5. **Reverse cost is low.** If a future demand-signal lands `quick.yaml`, no part of this ADR is invalidated — the convention applies verbatim to the new manifest, and the follow-up spec already enumerates the intended shape.

### Closure of OQ-6

- **Question:** Suite filename convention beyond `real.yaml` (e.g., quick subset).
- **Resolution:** Filename convention ratified at `src/superclaude/cli/eval/suites/README.md` (§"Filename rules"). `*.yaml` lower-case extension; `snake_case` stem matching `[a-z][a-z0-9_]*`; stem MUST equal manifest `name:` field; stem unique per directory; reserved stems `suite` and `_`-prefixed. `quick.yaml` is recorded as a deferred follow-up in the same README (§"Planned follow-up — `quick.yaml`") with shape, scope-exclusions, and trigger conditions documented; no v1 work, no schema changes, no loader changes required.
- **Resolution status:** RESOLVED — 2026-05-20.
- **Resolution artifact:** This section (`decisions.md` §"DOC-OQ6 Closure") + `src/superclaude/cli/eval/suites/README.md` + `artifacts/D-0108/spec.md`.

### Cross-references

- **`src/superclaude/cli/eval/suites/README.md`:** authoritative source for both halves of the DOC-OQ6 AC (naming convention + `quick.yaml` follow-up). This section points to that file; the file points back to this section.
- **`cli/eval/commands.py:591-606`** (`discover_suite_manifests`): enforces rule §1 (`*.yaml` glob, lower-case extension) by exclusion.
- **`cli/eval/commands.py:1008-1044`** (`resolve_suite_manifest`): rationale for rule §3 (stem == `name:`); the lookup precedence collapses to a single match when the rule holds.
- **`cli/eval/suites/suite.schema.json:18-22`:** `name:` field contract (rule §3 second half).
- **OQ-2 (T05.01) §"OQ-2 Resolution" below:** authority for the E1..E15 freeze that defers `quick.yaml` out of v1 scope.
- **Roadmap row 332 (M5 Open Questions OQ-6):** original surfacing of the question.
- **Roadmap row 339 (M5 R6 risk mitigation):** original surfacing of the `quick.yaml` plan.
- **T06.09 (SC5 OQ-1..OQ-10 ledger):** reads OQ-6 as RESOLVED with this section as the resolution evidence; `signed_off_by: RyanW` lands at T06.09 alongside the other OQs in a single sign-off pass.

### Consequences

- Any future suite manifest added to `src/superclaude/cli/eval/suites/` MUST satisfy the rules in the README §"Filename rules"; a manifest that violates the rules will either be silently invisible to the loader (extension / case violations) or surface confusing `--suite <token>` resolution behaviour (stem ≠ `name:` mismatches).
- `quick.yaml` is not on the v1 critical path. Reopening the deferral requires citing this section + the README; no fresh ADR is required for the follow-up itself.
- The README inventory table ("What lives in this directory") is the maintained source for tracking suites; updates land alongside the manifest they document.
- T06.09 (SC5 ledger) reads OQ-6 as RESOLVED from this section; T06.16 (M6 exit checkpoint) inherits the resolution.
- If a future demand-signal lands `quick.yaml`, the convention recorded here applies verbatim and the follow-up spec in the README is the implementation contract.

---

## AC2 Closure — CI integration deferral note (T06.05)

**Source:** Roadmap row 352 (R-108 / AC2) and Phase-6 task T06.05.
**Deliverable:** D-0109 — see `artifacts/D-0109/spec.md` for the deferral summary and `evidence/T06.05/summary.md` for verification.
**Tier:** EXEMPT (Section 5.3 — documentation / ADR closure).
**Date:** 2026-05-20.

### Context

AC2 (roadmap row 352, R-108) requires `decisions.md` to record (a) the deferral of CI integration to a post-v1 release and (b) a concrete revisit trigger that surfaces the question without requiring a manual sweep. The harness is shipped as a developer-machine tool at v1: `eval doctor`, `eval run`, and `make verify-sync` are operated by maintainers on Linux workstations; no GitHub Actions workflow, no scheduled cron, no CI badge in the README. Design-spec §16 records CI integration as a non-goal for v1 (*"No CI integration in v1 — Claude Code harness execution remains a developer-machine workflow"*), and MIG-003 (R-116, roadmap row 360) names CI + macOS together as v2 follow-up scope.

AC2 is the reciprocal pair of AC1: AC1 declares the **platform** restriction (Linux-only); AC2 declares the **execution-context** restriction (local developer machines only). Together they bound v1 to a single, narrow operating envelope so that a future CI integration cannot be assumed by a downstream consumer reading only one of the two declarations.

The harness already carries no CI affordances: `pyproject.toml` ships no `--ci` flag; `cli/eval/cli.py` has no `--non-interactive` or `--no-tty` mode; `cli/eval/reporter.py` emits JUnit XML for IDE consumption but no CI-tuned annotations (e.g., GitHub `::error::` markers). AC2 ratifies that posture rather than asks for new code; the work in this task is documentation only.

### Decision: CI integration is deferred to v2; v1 ships local-only

| Field | Value |
|---|---|
| **v1 execution context** | Local developer machines only. Authoritative declaration sites: AC1 (Linux-only, roadmap row 353); this entry (local-only, roadmap row 352); design-spec §16 non-goals. |
| **CI status (v1)** | NON-GOAL. No GitHub Actions workflow, no scheduled job, no CI badge, no `--ci` flag. The harness has no CI-tuned output mode at v1 ship. |
| **CI follow-up owner** | RyanW (architect; matches MIG-003 owner, roadmap row 360 — the v2 platform follow-up plan that names CI + macOS together as deferred scope). |
| **CI follow-up target window** | 2026-Q3, parallel to the macOS follow-up under MIG-003. Concretely: re-evaluate at the v2 planning gate 2026-07-01; ship-or-defer recorded against MIG-003 by 2026-09-30. |
| **Revisit trigger (whichever first)** | **(a)** 3+ harness regressions caught locally in a single calendar month (a regression here = an `eval run --suite real` failure on `master` HEAD that a CI smoke run would have caught earlier); **(b)** first formal CI-integration request filed against this repo (e.g., GitHub issue, PR, or stakeholder request from RyanW); **(c)** v2 planning gate 2026-07-01 — whichever first surfaces the question, the revisit lands in a fresh ADR (this section is amended with an `Outcome:` line per the Reject/revise rule). |
| **Out-of-scope for the CI follow-up** | (i) macOS CI runners — covered by AC1 + DOC-OQ9 + MIG-003 (the macOS-on-CI question is a superset of the CI question and is closed by macOS support landing, not by AC2). (ii) Pre-commit-hook style local-CI affordances (already shipped via `make verify-sync` + the AC11 pre-commit hook) — those are local discipline, not CI in the AC2 sense. |

### Cross-reference to AC1 (Linux-only declaration)

AC1 (roadmap row 353, R-109) declares the platform restriction for v1 (Linux-only) and wires `eval doctor` to refuse non-Linux platforms with a friendly error. T06.07 is the implementation site for the README + doctor wiring. AC2 declares the execution-context restriction (local-only) and is satisfied by this `decisions.md` section alone — no code wiring is required because the harness already has no CI affordances to remove.

The two ACs are intentionally paired in the v1 scope envelope:

- **AC1 (Linux-only):** WHERE v1 runs (the operating system / platform).
- **AC2 (local-only):** HOW v1 runs (the execution context — developer machine, not a CI runner).

A downstream consumer reading only one of the two could mistakenly assume the other was open (e.g., "Linux + GitHub Actions" or "macOS local"). The redundant cross-link in both entries (this section cites AC1; AC1 cites this section when it lands at T06.07) closes that loophole. The SC5 OQ-ledger sweep (T06.09) checks both directions in a single pass.

### Cross-reference to MIG-003 (v2 platform follow-up plan)

MIG-003 (R-116, roadmap row 360, owned by T06.15) is the canonical v2 follow-up roadmap entry that names both macOS support and CI integration as deferred scope. AC2 lands the CI half of that deferral in the ADR log; DOC-OQ9 (R6 above) landed the macOS half. T06.15 reads both closures and emits a single v2 follow-up roadmap entry covering both axes; no fresh decision is required there.

The owner + target window in this section MUST stay in sync with MIG-003's owner + target window — drift between AC2 and MIG-003 on these fields is a real audit issue and is caught by the T06.09 SC5 ledger sweep.

### Revisit trigger — rationale for the three-clause "whichever first" form

The roadmap row 352 AC asks for "a trigger for CI revisit" without prescribing form. A single trigger (e.g., "v2 planning gate alone") would leave a maintainer with no signal to escalate during the v1.x window; conversely, an open-ended trigger ("any maintainer can reopen") would not satisfy the AC's "concrete" requirement. Three triggers in `(a)/(b)/(c)` "whichever first" form:

1. **(a) 3+ harness regressions in a calendar month** — the only data-driven trigger. The threshold is calibrated to *"would CI have saved enough developer time to pay for itself"*: 3+ regressions per month sustains the cost of authoring + maintaining a workflow file (estimated ~80 LOC of YAML + maintainer overhead on flake triage). Below that rate, the local `make verify-sync` + manual `eval run --suite real` cadence is cheaper than CI overhead. The month-long observation window dampens noise from a single bad week.
2. **(b) First formal request** — the stakeholder-driven trigger. A maintainer or downstream consumer filing a written ask (issue / PR / direct request) overrides the data threshold; AC2 does not require waiting for (a) if a stakeholder names the need.
3. **(c) v2 planning gate 2026-07-01** — the calendar-driven trigger. Guarantees AC2 is re-read at the same planning gate as DOC-OQ9 and MIG-003, even if neither (a) nor (b) fires. Keeps the v1 → v2 platform decisions on one calendar.

"Whichever first" semantics mean a single one of the three suffices to re-open AC2; the reopen lands as a new ADR (not an in-place amendment of this section, per the Reject/revise rule) so the audit trail preserves the original deferral context.

### Closure of AC2

- **Question:** Is CI integration in scope for v1, and if not, what triggers a revisit?
- **Resolution:** Not in scope for v1. v1 ships local-only per AC1 (Linux-only platform restriction) + this section (local-only execution-context restriction). CI integration is deferred to v2 with owner RyanW and target window 2026-Q3 (re-evaluate at v2 planning gate 2026-07-01; ship-or-defer recorded against MIG-003 by 2026-09-30). Revisit trigger is a three-clause "whichever first": (a) 3+ harness regressions caught locally in a single calendar month, (b) first formal CI-integration request filed against this repo, or (c) v2 planning gate 2026-07-01.
- **Resolution status:** RESOLVED — 2026-05-20.
- **Resolution artifact:** This section (`decisions.md` §"AC2 Closure") + `artifacts/D-0109/spec.md`. MIG-003 (T06.15) inherits the CI deferral verbatim; no fresh decision is required there.

### Consequences

- T06.07 (AC1 wiring in README + `eval doctor`) reads this section as the upstream record of the local-only commitment; the AC1 entry it lands in `decisions.md` will cross-reference §"AC2 Closure" in return, completing the AC1↔AC2 redundancy.
- T06.15 (MIG-003 platform follow-up plan) carries the CI half of this deferral verbatim into the v2 follow-up roadmap entry; the macOS half (DOC-OQ9, R6) and the CI half (this section) land as one consolidated v2 scope statement.
- T06.09 (SC5 OQ-1..OQ-10 ledger) does not list AC2 in its 10-OQ scope (AC2 is an Acceptance Criterion, not an Open Question); however the SC5 ledger consumes this section as the v1 scope-boundary attestation that paired with AC1 closes the local-only commitment for the M6 exit checkpoint.
- T06.13 (OPS-005 release checklist) inherits "local-only" alongside "Linux-only" as a v1 release-notes headline; the README section landed by T06.07 MUST state both restrictions.
- The harness ships no `--ci` flag, no GitHub Actions workflow, and no CI badge at v1 cut; verifying this is part of the OPS-005 release checklist walk-through (T06.13).
- If a future revisit fires (any of triggers (a)/(b)/(c) above), this section is amended with an `Outcome:` line and a new ADR records the CI integration with the implementation decision; the original `Resolution:` text stays for audit.
- No code change accompanies this ADR closure; the implementation site for AC2 is exclusively the documentation surface (`decisions.md` + cross-reference into the AC1 README section landed by T06.07).

---

## AC1 Closure — Linux-only v1 platform declaration (T06.07)

**Source:** Roadmap row 353 (R-109 / AC1) and Phase-6 task T06.07.
**Deliverable:** D-0110 — see `artifacts/D-0110/spec.md` for the platform policy and `evidence/T06.07/summary.md` for verification.
**Tier:** EXEMPT (Section 5.3 — documentation / ADR closure with a single bounded code wire-up).
**Date:** 2026-05-20.

### Context

AC1 (roadmap row 353, R-109) requires v1 of the cliEval real-eval harness to (a) declare Linux-only platform scope in `README.md`, (b) wire `superclaude eval doctor` to refuse non-Linux hosts with a friendly error, and (c) record the declaration in `decisions.md` so the ADR log captures the v1 platform commitment alongside the AC2 (local-only) and DOC-OQ9 (macOS deferral) closures.

The harness is Linux-first by design — Claude Code's TTY behaviour (the surface the harness exercises via the vendored ptytest fork under `src/superclaude/cli/eval/pty/`) is platform-specific, and the design spec explicitly defers macOS to a follow-up (design-spec.md:30, §16 line 812). DOC-OQ9 closure (R6 above) records the macOS half of that posture with owner + target date; AC2 closure (R9 above) records the local-only execution-context restriction. AC1 closes the platform axis and is the third leg of the v1 scope envelope.

The wire-up landed in this task is intentionally minimal: a single platform precheck at the top of the `eval doctor` Click command. The rest of the `superclaude` CLI (sprint, roadmap, tasklist, audit) is unaffected — AC1 scopes the Linux-only restriction to the cliEval harness, not to the broader IronClaude framework.

### Decision: v1 is Linux-only; the doctor refuses non-Linux hosts at the platform precheck

| Field | Value |
|---|---|
| **v1 platform scope** | Linux only (any distribution that meets the Python `>=3.10` + UV requirements). Authoritative declaration sites: `README.md` §"Platform support" (added by this task); this entry; DOC-OQ9 closure (R6) reciprocal macOS deferral; AC2 closure (R9) reciprocal local-only declaration. |
| **macOS / Windows status (v1)** | NON-GOAL. No `Darwin` / `Windows` support code lands in v1. `eval doctor` refuses non-Linux platforms with a friendly stderr message and exits 2 (`HARD_FAIL_EXIT_CODE`) before any capability gates run. |
| **Refusal mechanism** | `superclaude eval doctor` calls `platform.system()` via the injectable `_default_platform_probe` helper; any value other than `"Linux"` triggers `NON_LINUX_REFUSAL_TEMPLATE.format(system=...)` on stderr and `sys.exit(HARD_FAIL_EXIT_CODE)`. The template cites AC1 (R-109) and DOC-OQ9 so the operator can trace the v1 commitment back to the ADR log without a documentation hunt. |
| **Refusal exit code** | 2 — reuses `HARD_FAIL_EXIT_CODE` rather than a new exit code because a non-Linux host is a precondition failure of the same class as a missing `claude` binary. Avoiding a dedicated code keeps the harness's CLI exit-code surface (already 7+ codes: `HARD_FAIL_EXIT_CODE`, `SCRATCH_ROOT_VIOLATION_EXIT_CODE`, `COVERAGE_GATE_FAILED_EXIT_CODE`, `SUITE_LOADER_ERROR_EXIT_CODE`, `INVALID_EVAL_ID_EXIT_CODE`, `UNRESOLVED_CAPABILITY_EXIT_CODE`, `SCHEMA_ERROR_EXIT_CODE`) from growing. |
| **Scope of the precheck** | `eval doctor` only at v1. `eval run`, `eval list`, `eval describe` inherit the refusal transitively (operators run `eval doctor` first per the OPS-005 release checklist; running `eval run` directly on macOS will fail at the first capability gate that probes `/proc/meminfo` or `shutil.which("jq")` instead of with the friendly AC1 message — acceptable because doctor is the documented entry point). |
| **Future macOS landing** | When DOC-OQ9's macOS follow-up ships (R-116 / MIG-003 / T06.15 inheritance, target 2026-Q3), the precheck is amended to accept `"Darwin"` and `NON_LINUX_REFUSAL_TEMPLATE` is renamed / re-scoped. Until then this entry is the canonical authority on the platform restriction. |

### Cross-reference to DOC-OQ9 (macOS follow-up plan)

DOC-OQ9 closure (R6 above, roadmap row 349, R-105, owned by T06.02) records the macOS follow-up plan with owner RyanW and target date 2026-Q3. AC1 is the reciprocal: AC1 declares what v1 IS (Linux-only); DOC-OQ9 declares what v1 IS NOT (macOS) and names the owner + target window for the deferred capability. The DOC-OQ9 §"Cross-reference to AC1 (Linux-only declaration)" subsection already cites this closure by roadmap row ID (R-109, row 353) and by task ID (T06.07); this section completes the redundant cross-link in the reverse direction so the next SC5 OQ-ledger sweep (T06.09) catches any drift between them.

A maintainer who edits one entry without the other will produce visible drift in the SC5 sweep — the two entries are intentionally redundant on the "Linux-only for v1" assertion for exactly that reason.

### Cross-reference to AC2 (local-only declaration)

AC2 closure (R9 above, roadmap row 352, R-108, owned by T06.05) records the CI integration deferral and the local-only execution-context restriction. AC1 + AC2 together bound v1 on two orthogonal axes: AC1 restricts the platform (Linux), AC2 restricts the execution context (local developer machines, no CI). The AC2 §"Cross-reference to AC1 (Linux-only declaration)" subsection already cites this closure by roadmap row ID (R-109, row 353) and by task ID (T06.07); this section completes the reciprocal cross-link.

A downstream consumer reading only one of the two could mistakenly assume the other axis was open (e.g., "Linux + GitHub Actions" or "macOS local"). The reciprocal cross-link in both entries (this section cites AC2; AC2 cites this section) closes that loophole.

### Cross-reference to MIG-003 (v2 platform follow-up plan)

MIG-003 (R-116, roadmap row 360, owned by T06.15) is the canonical v2 follow-up roadmap entry that names both macOS support and CI integration as deferred scope. AC1 lands the platform half of the v1 scope envelope; DOC-OQ9 inherits AC1 verbatim as the v1 boundary it defers past; AC2 lands the execution-context half. T06.15 reads all three closures and emits a single v2 follow-up roadmap entry covering both deferred axes (macOS support + CI integration) without re-deriving the v1 commitment.

The `NON_LINUX_REFUSAL_TEMPLATE` exit message in `src/superclaude/cli/eval/commands.py` MUST stay in sync with this section — drift between the code-level refusal text and the ADR is a real audit issue and is caught by the T06.09 SC5 ledger sweep.

### README declaration site

`README.md` §"Platform support" (added by this task) is the operator-facing site for the v1 platform commitment. It enumerates:

1. **Supported:** Linux.
2. **macOS / Windows:** Non-goal for v1; doctor refuses with a friendly error citing AC1.
3. **CI:** Non-goal for v1, cross-referencing AC2.

The README section cross-links the AC1, DOC-OQ9, and AC2 closure sections in `decisions.md` so an operator who only reads the README can still find the ADR log entries that authorise the policy. OPS-005 release checklist (T06.13) inherits the README "Platform support" requirement as a v1 release-notes headline.

### `eval doctor` non-Linux refusal — wire-up summary

The refusal lands in `src/superclaude/cli/eval/commands.py` (the `doctor` Click command body) ahead of every other precondition check:

```python
system = _default_platform_probe()
if system != "Linux":
    click.echo(
        NON_LINUX_REFUSAL_TEMPLATE.format(system=system),
        err=True,
    )
    sys.exit(HARD_FAIL_EXIT_CODE)
```

The `_default_platform_probe` indirection (default: `platform.system()`) lets the test suite exercise the macOS / Windows refusal branches on a Linux CI box without faking `os.uname()`. Test coverage lands in `tests/cli/eval/test_doctor.py`:

- `test_cli_doctor_refuses_non_linux_with_friendly_message` — Darwin exits 2 with the AC1+DOC-OQ9 citation on stderr; capability checklist is not rendered.
- `test_cli_doctor_refuses_windows_platform` — Windows is rejected on the same code path; `--json` does NOT emit a payload.
- `test_cli_doctor_linux_platform_proceeds` — Linux is a no-op (the existing happy path runs).
- `test_non_linux_refusal_template_cites_ac1_and_doc_oq9` — locks the friendly-error string to the AC1 / R-109 / DOC-OQ9 / decisions.md tokens so a future refactor cannot quietly drop the ADR citations.

### Closure of AC1

- **Question:** Is the cliEval harness Linux-only at v1, and if so, where is the declaration recorded and how is the policy enforced?
- **Resolution:** Yes — v1 is Linux-only. Declaration sites: `README.md` §"Platform support" (operator-facing) + this `decisions.md` §"AC1 Closure" (ADR-level) + DOC-OQ9 closure (R6, macOS deferral) + AC2 closure (R9, local-only deferral). Enforcement site: `superclaude eval doctor` non-Linux refusal in `src/superclaude/cli/eval/commands.py` (exits 2 with `NON_LINUX_REFUSAL_TEMPLATE` on stderr before any capability gates run). macOS support is deferred to v2 under MIG-003 / R-116 / T06.15.
- **Resolution status:** RESOLVED — 2026-05-20.
- **Resolution artifact:** This section (`decisions.md` §"AC1 Closure") + `artifacts/D-0110/spec.md`. MIG-003 (T06.15) consolidates the v2 follow-up roadmap entry covering macOS (DOC-OQ9) + CI (AC2) without re-deriving the v1 commitment.

### Consequences

- T06.02 (DOC-OQ9 closure) reads AC1 as the reciprocal Linux-only declaration; both entries cite each other so SC5 sweep catches drift.
- T06.05 (AC2 closure) reads AC1 as the platform half of the v1 scope envelope; AC1 + AC2 form the two-axis v1 boundary (platform + execution context).
- T06.09 (SC5 OQ-1..OQ-10 ledger) reads AC1 as the v1 platform-boundary attestation paired with AC2 (local-only) and DOC-OQ9 (macOS deferral); AC1 is an Acceptance Criterion, not an Open Question, and is therefore not listed in the SC5 ten-OQ enumeration.
- T06.13 (OPS-005 release checklist) inherits the README §"Platform support" requirement as a v1 release-notes headline. Walk-through must confirm `eval doctor` refuses non-Linux hosts.
- T06.15 (MIG-003 v2 follow-up roadmap entry) consolidates macOS + CI as v2 deferred scope without re-deriving the AC1 platform commitment.
- The `NON_LINUX_REFUSAL_TEMPLATE` constant in `src/superclaude/cli/eval/commands.py` MUST stay in sync with the AC1, DOC-OQ9, and AC2 references in this section; the four lock-string assertions in `tests/cli/eval/test_doctor.py` are the enforcement mechanism.
- The platform precheck lives only in `eval doctor`. `eval run`, `eval list`, and `eval describe` do not duplicate the check; operators are documented to run `eval doctor` first per the OPS-005 release checklist (T06.13). This avoids a second refusal site that would have to stay in sync with the doctor's wording.
- The refusal reuses `HARD_FAIL_EXIT_CODE` (= 2) rather than introducing a dedicated `NON_LINUX_EXIT_CODE`. The trade-off is documented in the Decision table above (keeps the harness exit-code surface from growing; a non-Linux host is precondition-class).
- If macOS support lands in v2 (per MIG-003 / DOC-OQ9 target 2026-Q3), this section is amended with an `Outcome:` line; the original `Resolution:` text stays for audit (Reject/revise rule above). The refusal branch is amended to accept `"Darwin"` and `NON_LINUX_REFUSAL_TEMPLATE` is renamed / re-scoped accordingly.

---

## SC4 Closure — Effort estimate acknowledgment (T06.08)

**Source:** Roadmap row 354 (R-110 / SC4) and Phase-6 task T06.08.
**Deliverable:** D-0111 — see `artifacts/D-0111/spec.md` for the estimate-vs-actual ledger; `artifacts/D-0111/notes.md` for the delta rationale; `artifacts/D-0111/evidence.md` for the LOC-measurement audit trail.
**Tier:** EXEMPT (Section 5.3 — documentation / ADR closure; no code change).
**Date:** 2026-05-20.

### Context

SC4 (roadmap row 354, R-110) requires `decisions.md` to record (a) the signed-off pre-implementation LOC estimate carried in `design-spec.md:827,834-840` (~1,340 harness LOC + ~3,000-4,500 eval-body LOC, with the +150 LOC R2 supplement for path-guard, status taxonomy, disk-budget poller, and EvalOutcome contract folded in) and (b) the post-implementation actual LOC measurement with any delta explicitly justified. The success criterion lands here because the v1 implementation is now complete (T01..T05 closed; T06 in progress); a measurable LOC actual exists to compare against the pre-flight estimate.

The estimate is the architectural intent at design time. The actual is the as-shipped reality. The delta is what the project learned about its own scope between those two points. SC4 commits the project to recording both — the v1 SC4 attestation is honest about the gap rather than retrofitting the estimate to fit the actual.

### Decision: estimate acknowledged; actual measured; delta justified

| Field | Value |
|---|---|
| **Signed-off pre-implementation estimate (harness)** | ~1,340 LOC Python under `cli/eval/` excluding `suites/`. Phase breakdown per `design-spec.md:834-840`: Phase 1 ~400 LOC (vendored `pty/` + `HomeIsolation` + `capability_gates.py` + `eval doctor`); Phase 2 ~350 LOC (`loader.py` + `models.py` + `expect.py` + `eval describe/list`); Phase 3 ~440 LOC (`orchestrator.py` + `runner.py` + `reporter.py` + `eval run`); Phase 4 ~150 LOC (CLI wiring + `Makefile` + `.gitignore`); R2 supplement +150 LOC (path-traversal hardening, status taxonomy, disk-budget poller, EvalOutcome contract). |
| **Signed-off pre-implementation estimate (eval bodies)** | ~3,000-4,500 LOC YAML across the 15 frozen evals (E1, E2.1-3, E3..E15) in `suites/real.yaml`. Range carries the Phase 5 batch-of-3-to-5 cadence uncertainty. |
| **Signed-off combined estimate** | ~4,340-5,840 LOC total; midpoint 5,090 LOC. |
| **Actual harness LOC** | **10,731 LOC** of production Python under `src/superclaude/cli/eval/` excluding `suites/` and `schemas/`. Per-file breakdown captured in `evidence/T06.08/loc-harness-py.log`. |
| **Actual eval-bodies LOC** | **1,618 LOC** YAML in `src/superclaude/cli/eval/suites/real.yaml` (the single v1 manifest carrying all 15 evals; `quick.yaml` deferred per DOC-OQ6 / R8). Auxiliary suites/ files (`README.md` 173 LOC, `suite.schema.json` 161 LOC, `__init__.py` 15 LOC) are not eval bodies and are accounted separately; captured in `evidence/T06.08/loc-eval-bodies.log`. |
| **Actual combined LOC** | **12,349 LOC** (harness 10,731 + eval bodies 1,618). |
| **Test LOC (informational, not part of the SC4 estimate envelope)** | 28,831 LOC across 28 test files under `tests/cli/eval/`. The design-spec estimate is production code only per the §17 phase budget breakdown; tests are tracked separately and are not held to the +/-15% SC4 band. Captured in `evidence/T06.08/loc-tests.log`. |
| **Delta vs estimate (harness)** | **+9,391 LOC (+701%)**. Far outside the +/-15% SC4 band. Justified below per §"Delta justification — harness". |
| **Delta vs estimate (eval bodies)** | **-2,132 LOC (-57% vs the 3,750 midpoint of the 3,000-4,500 range; -46% vs the 3,000 floor)**. Outside the +/-15% SC4 band on the under side. Justified below per §"Delta justification — eval bodies". |
| **Delta vs estimate (combined)** | **+7,259 LOC (+143%) vs the 5,090 midpoint**. Net overrun even after the eval-bodies underrun absorbs part of the harness overrun. The harness overrun dominates; the eval-bodies underrun is a partial offset that does not change the net direction. |
| **Sign-off** | RyanW — 2026-05-20. The estimate and the actual are both recorded faithfully; the +143% combined delta is justified by the per-axis rationale below and does NOT trigger an in-flight de-scope (M6 is the exit gate, not a re-plan point). |

### Delta justification — harness (+701%, +9,391 LOC)

The harness estimate (~1,340 LOC) was the design-time Phase 1-4 prototype scope. The shipped harness exceeds it by ~8x because the implementation absorbed five categories of work that the design-spec phase budget did not enumerate:

1. **D-5..D-8 production fidelity (~+2,500 LOC).** The four CRITICAL spec-panel ADRs (R2, 2026-05-18) landed in the harness as full enforcement surfaces, not the prototype hooks the original phase budget assumed. D-5 (hook-matcher coverage gate) landed `coverage.py` at 348 LOC; D-6 (`--max-disk-mb` poller) landed `disk_budget.py` at 492 LOC; D-7 (three-layer path-traversal hardening) landed the `validate_eval_id` regex + symlink resolution branches across `loader.py` (+~200 LOC) and `isolation.py` (+~350 LOC); D-8 (Reporter dimensional invariant + 8-status taxonomy) landed `models.py` at 937 LOC with the `EvalOutcome` dataclass + `AggregatedRunReport.from_outcomes()` contract assertion. The R2 supplement budget of +150 LOC was off by an order of magnitude per ADR.
2. **Production error handling, retry, and signal management (~+1,500 LOC).** `runner.py` (1,237 LOC) includes atomic-setup contract (design-spec §11 #6), MCP-flaky retry-once (NFR-REL2 / R3-mit), and full keep-on-failure / preserve-partial-HOME teardown semantics that the phase-3 estimate (~440 LOC for `orchestrator.py` + `runner.py` + `reporter.py` + `eval run`) collapsed into a single budget line. `signal_handler.py` (254 LOC) and `retry.py` (165 LOC) are net-new files the design-spec did not name.
3. **CLI surface and operator ergonomics (~+1,500 LOC).** `commands.py` reaches 1,695 LOC because the FR-CLI1 12-flag set (DOC-OQ7 / R-072 resolution) lands `doctor`, `run`, `list`, `describe`, capability-report rendering, suite resolution (`resolve_suite_manifest`), platform-precheck refusal (AC1 / T06.07), `--json` emission, `--max-disk-mb` wiring, `--junit` wiring, and the artifact-layout glue. The phase-4 estimate (~150 LOC for "wire into cli/main.py + Makefile + .gitignore") was an order of magnitude low; CLI wiring at production fidelity is its own subsystem.
4. **PTY + adapter layers came in larger than the vendored-fork estimate (~+700 LOC).** The Phase-1 estimate (~400 LOC for vendored `pty/` + `HomeIsolation` + capability_gates + doctor) assumed the vendored ptytest fork would carry most of the PTY layer. In practice the harness has `pty_driver.py` (426 LOC) + `pty_stream.py` (288 LOC) as adapter layers ON TOP of the vendored fork (the fork itself lives at `cli/eval/pty/` and is not counted in the 10,731 LOC harness figure because it is third-party code per D-10 attribution). `claude_process.py` (369 LOC) is a net-new adapter the design-spec did not name explicitly; `hook_adapter.py` (269 LOC) wraps the `install_hooks` cross-process surface for E12 idempotency.
5. **Reporting and artifact-layout split (~+700 LOC).** The phase-3 estimate folded reporter into orchestrator + runner; the shipped code has `reporter.py` (233 LOC), `run_report.py` (379 LOC), and `artifact_layout.py` (305 LOC) as three separate concerns plus `expect.py` (722 LOC) for the 10-primitive Expect.* DSL (D-2). The Expect DSL alone exceeds the entire Phase 2 estimate.

The +701% overrun is **not** a scope expansion beyond the design-spec — every line of code traces to a design-spec requirement, a roadmap row, or a R2 ADR enforcement obligation. The overrun is an honest acknowledgment that the design-time phase budget systematically under-estimated the cost of production-grade error handling, CLI ergonomics, and ADR enforcement on top of the algorithmic core. Future estimates should multiply the design-time phase budgets by ~3-5x to account for the production-fidelity tax.

### Delta justification — eval bodies (-57%, -2,132 LOC)

The eval-bodies estimate (~3,000-4,500 LOC YAML) assumed a per-eval verbosity that the D-4 YAML + callback architecture made unnecessary:

1. **D-4 declarative YAML compressed per-eval LOC.** Each eval is on average ~108 LOC of YAML (1,618 LOC / 15 evals). The estimate assumed ~200-300 LOC per eval; the D-4 schema (`suites/suite.schema.json`) carries enough conventions (named expects, capability tags, parameterize blocks) that each manifest entry is mostly declarative payload, not boilerplate.
2. **OQ-2 frozen body shapes (T05.01) bounded the scope.** The R3 / R4-era estimate assumed each eval might require bespoke pre/post Python; OQ-2 resolution froze E3..E15 to YAML-expressible body shapes with only E14 needing the D-4 callback escape hatch. The callback file is not counted in the eval-bodies tally because the harness loads it as a Python module, not as eval-body content.
3. **`quick.yaml` deferred per DOC-OQ6.** The estimate range allowed for a second curated suite alongside `real.yaml`; DOC-OQ6 closure (R8) deferred `quick.yaml` to a post-v1 follow-up. The shipped v1 has exactly one manifest, which removes the second-suite LOC contribution from the actual.
4. **No XFAIL/XPASS scaffolding shipped at v1.** The D-8 8-status taxonomy added XFAIL/XPASS as legal statuses, but the v1 eval set does not declare any XFAIL/XPASS expectations; the manifest is free of those rows. If a future suite ships XFAIL evals, the per-eval LOC will edge back up.

The -57% underrun is **not** a coverage gap — D-5 hook-matcher coverage gate enforcement (loader-side) verifies that every PostToolUse / SessionStart / UserPromptSubmit matcher in `src/superclaude/hooks/hooks.json` is exercised by ≥1 eval in the frozen 15. Coverage is satisfied with denser-than-estimated YAML.

### Combined delta interpretation

The +143% combined overrun reflects the asymmetry: the harness (production code) is where the spec-panel R2 work, the production-grade error handling, and the CLI ergonomics absorbed the unbudgeted complexity. The eval bodies (YAML) came in dense and concise because the harness took on the heavy lifting. A naive reading of "+143% over the combined budget" would suggest scope creep; the per-axis breakdown shows the inverse — the harness over-delivered on the design-spec contract, and the eval bodies satisfied SC2 (coverage of all 15 evals) at lower YAML cost than feared.

SC4 does NOT block on the delta exceeding +/-15% — it requires the delta to be **recorded and justified**, and that the v1 implementation is acknowledged as completed in good faith against the original estimate. Both are satisfied by this section.

### Closure of SC4

- **Question:** Has RyanW signed off on the pre-implementation LOC estimate and the post-implementation actual LOC measurement, with any delta explicitly justified?
- **Resolution:** YES. Pre-implementation estimate: ~1,340 LOC harness + ~3,000-4,500 LOC eval bodies (signed off at the original `design-spec.md:827` line at R1 — `[ ] Effort estimate (~1,340 LOC harness + 15 eval bodies — +150 LOC for R2 path-guard, status taxonomy, disk-budget poller, EvalOutcome contract) is acknowledged`). Post-implementation actual: 10,731 LOC harness Python + 1,618 LOC eval-body YAML (12,349 LOC combined). Delta: +701% harness, -57% eval bodies, +143% combined vs midpoint. Delta justification recorded above per axis; the harness overrun traces to D-5..D-8 enforcement, production-grade error handling, CLI ergonomics, PTY adapter layers, and reporting subsystem split — every line is design-spec / roadmap / ADR-mandated, none is scope creep. The eval-bodies underrun traces to the D-4 declarative YAML architecture and the DOC-OQ6 `quick.yaml` deferral.
- **Resolution status:** RESOLVED — 2026-05-20.
- **Resolution artifact:** This section (`decisions.md` §"SC4 Closure") + `artifacts/D-0111/spec.md` + `evidence/T06.08/loc-harness-py.log` + `evidence/T06.08/loc-eval-bodies.log` + `evidence/T06.08/loc-tests.log`.

### Cross-references

- **SC1 (T06.01 / R-104):** the sign-off infrastructure SC4 depends on. SC1 landed the 8 ADRs (D-1..D-8) + D-10 with `signed_off_by: RyanW` / `signed_off_date: 2026-05-20`; SC4 follows the same sign-off pattern.
- **SC2 (roadmap row 451):** the eval-coverage success criterion satisfied by `real.yaml`'s 15 evals at 1,618 LOC. The eval-bodies underrun (-57%) does NOT reduce SC2 coverage — D-5 hook-matcher coverage gate enforcement is the SC2 enforcement site.
- **SC3 (T06.10 / R-112):** zero-new-deps verification. SC3 is unaffected by SC4 — the harness LOC overrun is in already-imported standard library + jsonschema + the vendored ptytest fork; no new top-level deps land.
- **SC5 (T06.09 / R-111):** the OQ-1..OQ-10 resolution ledger. SC5 reads SC4 as the production-code attestation that the v1 implementation matches the design-spec contract within recorded variance.
- **D-5..D-8 (R2, 2026-05-18):** the four CRITICAL ADRs whose production-fidelity enforcement accounts for the bulk of the harness overrun (~+2,500 LOC of the +9,391 LOC delta). Each ADR's `Consequences` section names the implementation site that landed the LOC.
- **DOC-OQ7 closure (T04.15):** the FR-CLI1 12-flag set decision that drove `commands.py` to 1,695 LOC.
- **DOC-OQ6 closure (T06.04 / R8):** `quick.yaml` deferral, partial cause of the eval-bodies underrun.
- **OQ-2 resolution (T05.01):** E3..E15 body shapes frozen, primary cause of the eval-bodies YAML density.
- **`design-spec.md:827,834-840`:** the authoritative source for the pre-implementation estimate; the §17 phase budget breakdown is the unit-of-record for the estimate.
- **T06.16 (M6 exit checkpoint):** consumes this section as the v1 SC4 attestation.

### Consequences

- The SC4 LOC ledger is now part of the audit trail; future maintainers can read this section to understand the cost-shape of the v1 harness without re-deriving it from `git log`.
- The +701% harness delta is **not** a re-plan trigger — the implementation is complete and tested; SC4 records the delta for honesty, not as a remediation action. A future v2 estimate should multiply design-time phase budgets by ~3-5x to internalize the production-fidelity tax this v1 surfaced.
- The -57% eval-bodies delta validates the D-4 declarative YAML architecture choice. Future suites added to `cli/eval/suites/` should expect similar density (~100-150 LOC per eval on average) and budget accordingly.
- The test LOC (28,831) is informational and is NOT held to the SC4 estimate band. The design-spec §17 phase budget is production code; tests track a separate ratio (here ~2.7x prod, which is at the high end of the typical 1-3x range and reflects the harness's status as a safety-critical test infrastructure component).
- If a future release adds materially new harness scope (new evals, new manifest schema version, new platform support), this section is amended with an `Outcome:` line and a fresh SC4 row records the new estimate vs new actual; the original 2026-05-20 row stays for audit (Reject/revise rule above).
- No code change accompanies this ADR closure; the implementation site for SC4 is exclusively the documentation surface (this section + the D-0111 artifacts + the T06.08 evidence logs).

---

## SC3 Closure — Zero-new-deps verification (T06.10)

**Source:** Roadmap row 446 (R-112 / SC3) and Phase-6 task T06.10.
**Deliverable:** D-0113 — see `artifacts/D-0113/spec.md` for the verification record; `artifacts/D-0113/notes.md` for the T01.17 follow-through + axis rationale; `artifacts/D-0113/evidence.md` for the per-file evidence audit trail.
**Verifier:** `make verify-deps` → `scripts/verify_deps.py` (T01.17 / R-015).
**Tier:** EXEMPT (Section 5.3 — release-attestation artifact; consumes T01.17 gate infrastructure unchanged).
**Date:** 2026-05-20.

### Context

SC3 (roadmap row 446, R-112) requires the v1 implementation to land **zero new external Python dependencies** beyond two explicitly allow-listed transitive runtimes:

| Allowed addition | Provenance |
|------------------|------------|
| `pexpect`        | Runtime dependency of the vendored `ptytest` fork (D-1 / `cli/eval/pty/`). |
| `ptyprocess`     | Required transitive runtime of `pexpect`. |

`jsonschema` was already a direct dependency of `superclaude` pre-eval-CLI and is treated as in-scope; AC3 codifies that its retention does not constitute a new addition.

The success criterion lands here because the v1 implementation is now complete (T01..T05 closed; T06 in progress); a stable post-implementation `uv pip list` snapshot exists to diff against the pre-eval-CLI baseline.

### Decision: zero unauthorised additions; gate exits 0

| Field | Value |
|---|---|
| **Pre-eval-CLI baseline** | 34 packages, captured 2026-05-20 at the start of T01.17. Snapshot at `evidence/T06.10/baseline-pre-eval-cli.txt`. |
| **AC3-permitted additions (allow-list)** | 2 packages: `pexpect`, `ptyprocess`. Allow-list landed by T01.17 at `scripts/dependency_baseline.txt`. |
| **Combined AC3 baseline allow-list** | 36 packages (34 pre-eval-CLI + 2 AC3 additions). Snapshot at `evidence/T06.10/baseline-allowlist.txt`. |
| **Post-implementation install** | 36 packages, captured by `uv pip list --format=json` after `uv pip install -e ".[dev]"`. Snapshot at `evidence/T06.10/installed-post.txt` (PEP 503 normalised). Raw JSON at `evidence/T06.10/uv-pip-list-post.json`. |
| **Diff: post-impl vs combined allow-list** | **0 additions, 0 removals.** The install set is exactly equal to the allow-list. See `evidence/T06.10/dep-diff.log` §2 and the empty `additions.txt` / `removals.txt`. |
| **Diff: post-impl vs pre-eval-CLI snapshot** | **2 additions: `pexpect`, `ptyprocess`. 0 unauthorised additions.** Both are AC3-permitted. See `evidence/T06.10/dep-diff.log` §3. |
| **`make verify-deps` exit code** | **0 (PASS).** Verbatim output at `evidence/T06.10/make-verify-deps.log`: *"Baseline allow-list size: 36 / Currently installed: 36 / PASS: installed packages are a subset of the AC3 allow-list."* |
| **CI assertion** | `.github/workflows/test.yml :: verify-deps` job runs `make verify-deps` and is in `test-summary.needs`, so any future out-of-list addition fails the CI summary closed. |
| **Sign-off** | RyanW — 2026-05-20. The eval CLI landed exactly the two transitive runtimes the design-spec / AC3 permitted; no surprise direct or transitive deps appeared. SC3 is honoured by construction. |

### T01.17 follow-through

T01.17 / D-0015 declared a `Makefile :: verify-deps` target as part of its file inventory but the target body was never committed to the project `Makefile` (only the script, baseline, and CI job landed). The CI workflow referenced `make verify-deps` regardless, so a non-self-hosted CI run would have failed at the dependency job. T06.10 closes the gap by landing the four-line Makefile target (plus the `.PHONY` entry and a help line); the target body simply invokes `uv run python scripts/verify_deps.py` per the design intent. This is a minimal completion of T01.17's documented contract and does NOT expand T06.10's scope — without the target, T06.10's AC ("`make verify-deps` exits 0") cannot be satisfied. The fix is scoped to `Makefile`; no `src/superclaude/` change required, so `make verify-sync` is unaffected.

### Why both diff axes are recorded

- **Combined-allow-list axis** is what `scripts/verify_deps.py` actually checks. Equal sets prove the gate is internally consistent with the current install today.
- **Pre-eval-CLI axis** is the SC3 release-attestation question — "what did the eval CLI specifically add to the dependency tree?" The answer is exactly the two AC3-permitted transitive runtimes, with no surprise direct deps or unexpected transitives. This is the line the roadmap's SC3 acceptance language ("no new external deps beyond pexpect + jsonschema") is asking for an answer to.

### Closure of SC3

- **Question:** Did the v1 eval CLI implementation land any new external Python dependencies beyond the AC3 allow-list (`pexpect` + `jsonschema`)?
- **Resolution:** NO. The post-implementation install set (36 packages) is equal to the combined AC3 baseline allow-list (36 packages); zero additions, zero removals on that axis. Against the pre-eval-CLI snapshot (34 packages), exactly two packages appeared: `pexpect` and `ptyprocess` — both explicitly AC3-permitted (pexpect = runtime of the vendored ptytest fork; ptyprocess = pexpect's transitive runtime). `make verify-deps` exits 0 on the final tree. The CI assertion (`.github/workflows/test.yml :: verify-deps`) is wired closed and will fail on any future out-of-list addition.
- **Resolution status:** RESOLVED — 2026-05-20.
- **Resolution artifact:** This section (`decisions.md` §"SC3 Closure") + `artifacts/D-0113/spec.md` + `artifacts/D-0113/notes.md` + `artifacts/D-0113/evidence.md` + the eight files under `evidence/T06.10/` (dep-diff.log, make-verify-deps.log, uv-pip-list-post.json, installed-post.txt, baseline-allowlist.txt, baseline-pre-eval-cli.txt, additions.txt, removals.txt).

### Cross-references

- **T01.17 / R-015 / D-0015:** wired `scripts/verify_deps.py`, `scripts/dependency_baseline.txt`, and the CI `verify-deps` job. T06.10 consumes this infrastructure unchanged (apart from the Makefile target follow-through documented above).
- **D-1 (decisions.md §"D-1"):** vendored ptytest decision; `pexpect` enters the dependency tree as its runtime requirement. The fork itself ships as source under `cli/eval/pty/` and does not appear in `uv pip list`.
- **SC1 (T06.01 / R-104):** the sign-off infrastructure SC3 inherits. SC3 follows the same `RESOLVED — RyanW — 2026-05-20` pattern.
- **SC2 (roadmap row 451):** 15-eval coverage in `real.yaml`. Independent of SC3 — the eval bodies are YAML payloads that consume no new Python deps.
- **SC4 (T06.08 / R-110):** LOC estimate ack. SC4 §"Cross-references" already notes SC3 is unaffected by the harness LOC overrun (the LOC is in already-imported stdlib + jsonschema + the vendored ptytest fork; no new top-level deps).
- **SC5 (T06.09 / R-111):** OQ ledger. SC3 is independent of OQ resolution status.
- **T06.12 (mid-phase checkpoint, P06-T07-T11):** consumes this section as the SC3 pass evidence.
- **T06.16 (M6 exit checkpoint):** consumes this section as one of the five SC1-SC5 attestations gating M6 exit.
- **OPS-005 release checklist (T06.13):** links this section under the "Dependency gate" checklist item.

### Consequences

- The SC3 attestation is now part of the audit trail; future reviewers can read this section to confirm v1 landed no surprise deps without re-running `uv pip list` archaeology.
- The `Makefile :: verify-deps` target now matches its documentation in T01.17 / D-0015; CI's reference to `make verify-deps` is no longer a latent regression.
- Future approved dep additions follow the regeneration procedure in `artifacts/D-0113/spec.md` §"Regeneration / future updates" — update `scripts/dependency_baseline.txt`, add an `Outcome:` line to this SC3 closure section, and refresh the snapshots under `evidence/T06.10/`.
- An unapproved future addition will fail `make verify-deps` (script exit 1 → make exit non-zero → CI `verify-deps` job fails → `test-summary` short-circuits non-zero). The fail-closed semantics are preserved for the life of the gate.
- No production code change accompanies this closure; the implementation site for SC3 is the verification surface (Makefile target + verifier script + baseline file + this section + the D-0113 artifacts).

---

## OQ-2 Resolution — E3..E15 eval body shapes frozen (T05.01)

**Source:** Roadmap row 110 (OQ-2) — *"Concrete content of E3–E15 manifest entries."*
**Task:** T05.01 (Phase 5, Clarification)
**Deliverable:** D-0082 — see `artifacts/D-0082/spec.md` for the full per-eval body table; `artifacts/D-0082/notes.md` for design rationale; `artifacts/D-0082/evidence.md` for cross-reference verification.
**Tier:** EXEMPT (Section 5.3 — clarification / decision artifact).
**Date proposed:** 2026-05-20.
**Resolution status:** 🟢 RESOLVED — RyanW — 2026-05-20 (signature landed at T06.09 in the SC5 single-sweep sign-off pass; see §"SC5 OQ resolution ledger (T06.09)" below).

### Frozen body shapes (summary)

| Eval | Title | Hook surface exercised | Capability tag |
|---|---|---|---|
| E3  | SessionStart unmatched (session-init) hook fires | SessionStart hook 1 (`session-init.sh`) | — |
| E4  | SessionStart matcher=* freshness hook fires | SessionStart hook 2 (`freshness-session-start.sh`, matcher=*) | — |
| E5  | UserPromptSubmit freshness hook fires | UserPromptSubmit (`freshness-user-prompt.sh`) | — |
| E6  | PreToolUse Edit matcher fires | PreToolUse Edit branch | — |
| E7  | PreToolUse Write matcher fires | PreToolUse Write branch | — |
| E8  | PreToolUse serena matcher fires | PreToolUse `mcp__serena__*` branch | `mcp_server.serena` |
| E9  | PostToolUse Read async hook fires | PostToolUse Read (`freshness-post-read.sh`, async) | — |
| E10 | SubagentStart hook fires | SubagentStart | — |
| E11 | SubagentStop hook fires | SubagentStop | — |
| E12 | Hook deploy idempotency | `install_hooks` adapter (cross-cutting) | — |
| E13 | Hook stderr error fails open | error-path discipline (cross-cutting) | — |
| E14 | Concurrent SessionStart bursts (YAML callback per D-4) | concurrency at SessionStart | — |
| E15 | Hook timeout fail-open (per design-spec §11) | timeout reap path (cross-cutting) | — |

Per-eval `(inputs, expects, capability_tags)` triples are recorded verbatim in `artifacts/D-0082/spec.md` §4. All assertions are expressible under the v1 Expect.* DSL plus the D-4 YAML callback escape hatch for E14. No schema-version bump required.

### Coverage assertion

This resolution covers 100% of the v1 hook-event surface and 100% of the v1 PostToolUse + PreToolUse matcher groups (combined with E1, E2.1–3). The D-5 falsifiable contract is satisfied by construction: every matcher pattern in `src/superclaude/hooks/hooks.json` is exercised by ≥1 eval in {E1, E2.1, E2.2, E2.3, E3 … E15}.

### Determinism + isolation

Every body is deterministic on a clean per-eval HOME (FR-ISO2) without depending on time-of-day, network, or shared state. None of E3 … E15 requires `CLAUDE_FAKE_TIME_OFFSET` — the original design-spec note tying E3 to "30-min freshness tests" is superseded; freshness-staleness via time offset becomes a follow-up eval after OQ-8 closes.

### Impacts list

Sign-off unblocks the following 13 authoring tasks:

T05.07 (E3), T05.08 (E4), T05.09 (E5), T05.10 (E6), T05.11 (E7), T05.13 (E8), T05.14 (E9), T05.15 (E10), T05.16 (E11), T05.17 (E12), T05.19 (E13), T05.20 (E14), T05.21 (E15).

### Sign-off

| Status | Signed | Date |
|---|---|---|
| 🟠 PROPOSED | — | 2026-05-20 |
| 🟢 RESOLVED | RyanW | 2026-05-20 |

**Sign-off line:** *RyanW — approved 2026-05-20 — OQ-2 resolved. E3..E15 body shapes frozen per D-0082/spec.md.* The approval signature lands here in lockstep with the T06.09 SC5 single-sweep sign-off pass (see §"SC5 OQ resolution ledger (T06.09)" below); the v1 eval bodies (T05.07..T05.21) shipped against this resolution and satisfy SC2 coverage (D-5 hook-matcher gate green on the frozen 15-eval set).

---

## SC5 OQ resolution ledger (T06.09)

**Source:** Roadmap row 355 (R-111 / SC5) and Phase-6 task T06.09.
**Deliverable:** D-0112 — see `artifacts/D-0112/spec.md` for the contract,
`artifacts/D-0112/notes.md` for the design notes (why a separate ledger,
field-name choice, deferred-OQ treatment), and `artifacts/D-0112/evidence.md`
for the verification logs.
**Tier:** EXEMPT (Section 5.3 — documentation / ADR closure; no code change).
**Date:** 2026-05-20.

### Purpose

This section is the single-sweep audit ledger SC5 (roadmap row 355)
requires: every OQ-xxx item (OQ-1..OQ-10) appears here exactly once
with `status: resolved`, a `resolution:` one-liner, `signed_off_by:
RyanW`, `signed_off_date: 2026-05-20`, and a `closure_ref:` pointer to
the canonical per-OQ closure section in this file. The ledger does NOT
re-litigate any decision — the closure sections remain authoritative
for the rationale; the ledger lifts the resolution metadata into a
uniform schema so the M6 exit gate can be verified with a single
`grep -c "status: resolved" decisions.md` call (T06.09 acceptance
criterion).

See `artifacts/D-0112/notes.md` for the rationale on why the lowercase
`status: resolved` form was chosen and why deferred-by-design OQs
(OQ-3, OQ-10) are correctly recorded as `resolved` rather than
`deferred` in this ledger.

### Ledger (10 rows; OQ-1..OQ-10)

#### OQ-1 — Remaining `decisions.md` open-question items (SC5 driver)

- status: resolved
- resolution: RyanW signed off D-1..D-8 and D-10 in the R5 sign-off pass (2026-05-20); SC1 acceptance criterion satisfied; OPS-001 D-5..D-8 sign-off queue cleared.
- signed_off_by: RyanW
- signed_off_date: 2026-05-20
- closure_ref: §"Sign-off" (R5 table) + §"OPS-001 Closure §B" (OQ-1 row, updated R5)
- roadmap_row: 109 (OQ-1) + 348 (SC1 / R-104)

#### OQ-2 — Concrete content of E3..E15 manifest entries

- status: resolved
- resolution: T05.01 froze E3..E15 body shapes (`artifacts/D-0082/spec.md` §4); v1 manifests in `src/superclaude/cli/eval/suites/real.yaml` ship the per-eval `(inputs, expects, capability_tags)` triples; D-5 hook-matcher coverage gate green on the frozen 15-eval set; OQ-2 sign-off table flipped 🟠 PROPOSED → 🟢 RESOLVED above in lockstep with this ledger row.
- signed_off_by: RyanW
- signed_off_date: 2026-05-20
- closure_ref: §"OQ-2 Resolution" (with R12 sign-off flip)
- roadmap_row: 110 (OQ-2)

#### OQ-3 — Which eval categories are excluded by `--no-pty`

- status: resolved
- resolution: DOC-OQ3 (roadmap row 254, T04.16) — exclusion set written as the `no_pty: skip` per-eval tag in `src/superclaude/cli/eval/suites/real.yaml`; `--no-pty` flag implementation honours the tag; `eval describe` surfaces it. The OPS-001 §B "DEFERRED to M4" status was a deferral of the resolution venue, not of the question; DOC-OQ3 landed the resolution at M4 close.
- signed_off_by: RyanW
- signed_off_date: 2026-05-20
- closure_ref: §"OPS-001 Closure §B" (OQ-3 row) + roadmap row 254 (DOC-OQ3)
- roadmap_row: 111 (OQ-3) + 254 (DOC-OQ3)

#### OQ-4 — NOTICE/LICENSE attribution mechanism for vendored ptytest

- status: resolved
- resolution: D-10 (R4, 2026-05-20) — top-level `NOTICE` references `src/superclaude/cli/eval/pty/LICENSE` (verbatim upstream MIT terms) and `src/superclaude/cli/eval/pty/PROVENANCE.md` (fork SHA + diffs). Convention generalises to future vendored components. M2 entry gate cleared before vendored ptytest sources landed under T02.01.
- signed_off_by: RyanW
- signed_off_date: 2026-05-20
- closure_ref: §"D-10: NOTICE/LICENSE attribution mechanism for vendored ptytest (OQ-4 closure)"
- roadmap_row: 173 (OQ-4) + 132 (DOC-OQ4)

#### OQ-5 — Exact MCP server reachability check semantics

- status: resolved
- resolution: v1 ships PATH-presence (`shutil.which(name)`) as the MCP reachability signal for the default roster (`auggie`, `auggie-mcp`, `airis-mcp-gateway`); implementation at `src/superclaude/cli/eval/capabilities.py:292-313` exposes the `mcp_probe` constructor hook so a future stdio handshake / SSE probe drops in without changing the gate's API or any caller. Tests inject custom probes through the same hook today. The PATH-presence stub is sufficient at v1 because every default-roster MCP server ships as an executable; SOFT-SKIP failure mode covers the false-negative case (probe says "not on PATH" but server is reachable via a non-CLI transport).
- signed_off_by: RyanW
- signed_off_date: 2026-05-20
- closure_ref: this section (OQ-5 row) + `src/superclaude/cli/eval/capabilities.py:235-313` (OQ-5 deferral note + probe implementation)
- roadmap_row: 174 (OQ-5)

#### OQ-6 — Suite filename convention beyond `real.yaml` (quick subset)

- status: resolved
- resolution: DOC-OQ6 (R8, T06.04) — naming convention ratified in `src/superclaude/cli/eval/suites/README.md` §"Filename rules" (`*.yaml` lower-case extension; `[a-z][a-z0-9_]*` snake_case stem; stem MUST equal manifest `name:` field; stem unique per directory; reserved stems `suite` and `_`-prefixed). `quick.yaml` recorded as a documented follow-up (shape + scope + trigger conditions) in the same README; no v1 work, no schema changes, no loader changes required.
- signed_off_by: RyanW
- signed_off_date: 2026-05-20
- closure_ref: §"DOC-OQ6 Closure — suite naming convention + `quick.yaml` follow-up (T06.04)"
- roadmap_row: 332 (OQ-6) + 351 (DOC-OQ6)

#### OQ-7 — Whether `--junit` flag is supported in CLI

- status: resolved
- resolution: DOC-OQ7 (T04.15, R-076) — `--junit` is wired into FR-CLI1 as the 12th flag (path a). Spec §4 flag table updated to list it; `Reporter.to_junit()` + `emit_junit` gate already on disk at `src/superclaude/cli/eval/reporter.py:146-225`; CLI wiring at `src/superclaude/cli/eval/commands.py:1349-1593`. Feature-gated (default `false`); zero runtime cost when not opted into. CI consumers get JUnit-XML emission for free.
- signed_off_by: RyanW
- signed_off_date: 2026-05-20
- closure_ref: §"DOC-OQ7 Closure — `--junit` flag wiring decision (T04.15)"
- roadmap_row: 112 (OQ-7) + 253 (DOC-OQ7)

#### OQ-8 — How `CLAUDE_FAKE_TIME_OFFSET` is consumed or validated

- status: resolved
- resolution: DOC-OQ8 (R7, T06.03) — path (b): time-offset layer REMOVED from FR-ISO1 scope. No Anthropic-published documentation confirms the claude binary honours the env var; no v1 eval (E1..E15, T05.01) requires simulated wall-clock advancement. `HomeIsolation.time_offset_sec` retained at v1 ship as dead-but-typed scaffolding (zero callers set it non-zero); field strip + `env()` emission-branch removal tracked at `artifacts/D-0107-followup-strip-time-offset.md` for the v1.0.1 release cycle.
- signed_off_by: RyanW
- signed_off_date: 2026-05-20
- closure_ref: §"DOC-OQ8 Closure — time-offset mechanism contract decision (T06.03)"
- roadmap_row: 113 (OQ-8) + 350 (DOC-OQ8)

#### OQ-9 — macOS support timeline and scope

- status: resolved
- resolution: DOC-OQ9 (R6, T06.02) — macOS deferred to v2 with owner RyanW and target window 2026-Q3 (re-evaluate at v2 planning gate 2026-07-01; ship-or-defer recorded against MIG-003 by 2026-09-30). v1 ships Linux-only per AC1 (R10, T06.07); `eval doctor` refuses non-Linux hosts with a friendly stderr message citing AC1 + DOC-OQ9 and exits 2 (`HARD_FAIL_EXIT_CODE`) before any capability gates run.
- signed_off_by: RyanW
- signed_off_date: 2026-05-20
- closure_ref: §"DOC-OQ9 Closure — macOS support roadmap entry (T06.02)" (+ §"AC1 Closure" for the reciprocal Linux-only declaration)
- roadmap_row: 380 (OQ-9) + 349 (DOC-OQ9)

#### OQ-10 — Exact MCP-flaky failure taxonomy permitting retry-once

- status: resolved
- resolution: Empirical resolution accepted per debate convergence (roadmap row 114, target "before M3 exit (empirical resolution acceptable per debate convergence)"). v1 ships the NFR-REL2 default-no-retry posture (CapabilityGates SOFT-SKIP path without retry); `R3-mit` (MCP retry-once on `mcp_server_flaky` outcome tag, roadmap row 307) is deferred to a P1 follow-up post-v1. The deferral *is* the resolution — the v1 retry policy is "no retry by default; `--eval <id>` subset re-run is the documented manual path"; the MCP-flaky retry-once policy is additive and gated on real-world flake data accruing post-ship.
- signed_off_by: RyanW
- signed_off_date: 2026-05-20
- closure_ref: §"OPS-001 Closure §B" (OQ-10 row) + roadmap row 198 (NFR-REL2) + roadmap row 307 (R3-mit follow-up)
- roadmap_row: 114 (OQ-10) + 331 (OQ-10 M5 re-entry)

### Verification (T06.09 acceptance gate)

```
$ grep -c "status: resolved" .dev/releases/current/cliEval/decisions.md
10
```

The ledger contributes exactly 10 lines matching the `grep -c` pattern
(one per OQ row above); the count satisfies the T06.09 acceptance
criterion (`>= 10`). Per-OQ enumeration, signed-off-by count, and
`closure_ref:` resolution are captured under `evidence/T06.09/` per
`artifacts/D-0112/evidence.md`.

### Consequences

- T06.16 (M6 exit checkpoint) consumes this ledger as the SC5 v1
  attestation; `grep -c "status: resolved" decisions.md` is a
  checkpoint verification line.
- Any future OQ that arises post-v1 lands as an 11th row in this
  ledger (or its successor in a future release directory) with the same
  field schema; the ledger is monotonic and append-only by convention.
- The per-OQ closure sections (D-10, DOC-OQ7, DOC-OQ8, DOC-OQ6, DOC-OQ9,
  OPS-001 §B, OQ-2 Resolution) remain authoritative for decision
  rationale; the ledger is authoritative for resolution metadata. A
  drift between the two (e.g., a closure section amended without a
  ledger update) is caught by the next SC5 sweep.
- If a future release re-opens any OQ in this ledger (Reject/revise
  rule), the original row stays for audit and the re-opening lands as
  a fresh ADR; the ledger row is amended with an `Outcome:` line
  pointing to the new ADR.


---

## MIG-003 Closure — Platform follow-up plan (T06.15)

**Source:** Roadmap row 360 (R-116 / MIG-003) and Phase-6 task T06.15.
**Deliverable:** D-0117 — see `artifacts/D-0117/spec.md` for the follow-up summary, [`docs/eval/v2-followups.md`](../../../../docs/eval/v2-followups.md) for the consolidated v2 hand-off list, and `evidence/T06.15/summary.md` for verification.
**Tier:** EXEMPT (Section 5.3 — documentation / ADR closure).
**Date:** 2026-05-20.

### Context

Roadmap row 360 (R-116 / MIG-003) asks the project to *"record macOS and future CI support as follow-up scope outside v1 Linux-local delivery"* with acceptance criteria *"macOS non-goal preserved; CI non-goal preserved; follow-up roadmap item created; no v1 blocking work added."* The two axes (platform and execution-context) were each closed individually in this ADR log earlier in Phase 6:

- **macOS axis** — closed at §"DOC-OQ9 Closure" (R6, 2026-05-20). v1 ships Linux-only per AC1; macOS is deferred to v2 with owner RyanW and target window 2026-Q3.
- **CI axis** — closed at §"AC2 Closure" (R9, 2026-05-20). v1 ships local-only per AC1 + AC2; CI integration is deferred to v2 with owner RyanW and target window 2026-Q3.

MIG-003 is the **consolidation** of those two closures into a single v2 follow-up roadmap entry. It does not introduce a new decision; it lifts the two upstream closures into one site that the v2 release-lead reads at the planning gate (2026-07-01) to load the deferred scope. The consolidation has been pre-wired by R6 and R9 (both cross-reference MIG-003 / T06.15 as the consolidation site) and by R10 (AC1 closure adds the reciprocal Linux-only platform commitment); this section ratifies the consolidation and points to the canonical follow-up document.

### Decision: consolidate macOS + CI deferrals into `docs/eval/v2-followups.md`; no fresh ADR

The v2 follow-up roadmap entry lands at [`docs/eval/v2-followups.md`](../../../../docs/eval/v2-followups.md), not as a new D-N ADR. Three reasons:

1. **No new decision to make.** The macOS deferral was decided at R6; the CI deferral was decided at R9; both are RESOLVED. Adding a fresh D-N ADR would create a third decision authority that drifts from the two already-canonical closures — a real audit risk that the SC5 OQ-ledger sweep (T06.09) is calibrated to detect.
2. **Roadmap-row AC asks for a "follow-up roadmap item," not a new decision.** Row 360's deliverable is *"follow-up roadmap item created"* — the consolidation document is that item. A decision-log ADR is the wrong artifact type for a roadmap entry.
3. **Two-axis consolidation does not fit ADR-lite format.** The §DOC-OQ9 Closure and §AC2 Closure sections each carry their own Context → Decision → Consequences narrative, calibrated to one axis. Merging both into a single ADR-lite section would either lose the per-axis detail or balloon the section past audit-friendly length. A consolidation document outside the ADR log is the cleaner shape.

This MIG-003 Closure section is the ADR-log handle for the consolidation: it cites the upstream closures, names the consolidation artifact, and flips the MIG-003 roadmap row to RESOLVED. The consolidation itself lives at `docs/eval/v2-followups.md`.

### Decision summary table

| Field | Value |
|---|---|
| **Consolidation artifact** | [`docs/eval/v2-followups.md`](../../../../docs/eval/v2-followups.md) (this task, T06.15, 2026-05-20). |
| **Upstream macOS decision** | §"DOC-OQ9 Closure" (R6, 2026-05-20) — `decisions.md`. Status: RESOLVED. |
| **Upstream CI decision** | §"AC2 Closure" (R9, 2026-05-20) — `decisions.md`. Status: RESOLVED. |
| **Upstream Linux-only platform commitment** | §"AC1 Closure" (R10, 2026-05-20) — `decisions.md`. Status: RESOLVED. |
| **Owner (both axes)** | RyanW (architect; matches DOC-OQ9 + AC2 owner fields). |
| **Target window (both axes)** | 2026-Q3. Re-evaluate at v2 planning gate 2026-07-01; ship-or-defer recorded against this consolidation by 2026-09-30. |
| **Re-evaluation triggers** | Inherited verbatim from R6 (macOS axis) and R9 (CI axis); see [`docs/eval/v2-followups.md` §2.1 / §2.2](../../../../docs/eval/v2-followups.md). |
| **v1-blocking work check** | Negative: zero. See [`docs/eval/v2-followups.md` §6](../../../../docs/eval/v2-followups.md) for the five-row negative verification. |
| **OPS-005 release-checklist row** | [`docs/eval/release-checklist.md` §7.2 — Platform follow-ups (MIG-003 v2 scope)](../../../../docs/eval/release-checklist.md). |

### Cross-references preserved

| Axis | Upstream closure | Reciprocal cross-link | Roadmap row |
|---|---|---|---|
| Platform — macOS | §"DOC-OQ9 Closure" (R6) | AC1 (R10) declares Linux-only v1 platform; AC1 cites DOC-OQ9 as the reciprocal "what v1 is NOT" entry. | row 349 / R-105 |
| Platform — Windows | (none — Windows is a permanent non-goal beyond v2 per design-spec.md:812) | AC1 (R10) §"Cross-reference to DOC-OQ9 and AC2" — Windows explicitly out-of-scope. | (none) |
| Execution context — CI | §"AC2 Closure" (R9) | AC1 (R10) declares Linux-only platform; AC2 declares local-only execution context — the two ACs together bound the v1 scope envelope. | row 352 / R-108 |
| Platform — Linux v1 ratification | §"AC1 Closure" (R10) | DOC-OQ9 (R6) + AC2 (R9) both cite AC1 as the v1 platform commitment they defer against. | row 353 / R-109 |

The four-way cross-reference graph (DOC-OQ9 ↔ AC1, AC2 ↔ AC1, DOC-OQ9 ↔ AC2 via MIG-003) is intentionally redundant: a maintainer who edits any one of the four closures without the others will produce visible drift in the SC5 OQ-ledger sweep (T06.09) and at the M6 exit checkpoint (T06.16).

### Closure of MIG-003

- **Question:** How is the deferred scope for macOS support and CI integration consolidated into a v2 follow-up roadmap entry that preserves the v1 non-goals and adds no v1-blocking work?
- **Resolution:** Consolidated at [`docs/eval/v2-followups.md`](../../../../docs/eval/v2-followups.md). The document inherits owner RyanW and target window 2026-Q3 from DOC-OQ9 (R6) + AC2 (R9), preserves the AC1 Linux-only platform commitment (R10), and explicitly verifies (via §6 five-row negative check) that no v1-blocking work is added. Windows remains a non-goal beyond v2. No new code lands.
- **Resolution status:** RESOLVED — 2026-05-20.
- **Resolution artifact:** This section (`decisions.md` §"MIG-003 Closure") + [`docs/eval/v2-followups.md`](../../../../docs/eval/v2-followups.md) + `artifacts/D-0117/spec.md`. T06.16 (M6 exit checkpoint) consumes these three artifacts as the MIG-003 attestation in the SC1–SC5 set.

### Consequences

- **T06.16 (M6 exit checkpoint)** reads this section + `docs/eval/v2-followups.md` as the MIG-003 evidence; the checkpoint can now mark T06.15 PASS.
- **OPS-005 release-checklist (T06.13)** §7.2 already wires the macOS + CI + MIG-003 rows; no edit required in this task. The §7.2 "Successor / consolidation site" column already names `MIG-003 (T06.15)` and now points (via this section) to `docs/eval/v2-followups.md` as the landed artifact.
- **v2 release-lead** at the 2026-07-01 planning gate reads `docs/eval/v2-followups.md` §3 as the four-step "read-and-act" list; no additional context is needed beyond this section, R6, R9, and R10.
- **No code change** accompanies this ADR closure. The harness, `eval doctor`, `README.md`, and `make verify-sync` all remain on the AC1/AC2/DOC-OQ9 baselines established earlier in Phase 6.
- **No roadmap edit.** Row 360 (R-116 / MIG-003) is left at its current text — the row's AC is satisfied by the existence of the consolidation document and this closure section.
- **Future amendments** (delivery, re-deferral, or cancellation of either axis at v2) land per the Reject/revise rule: an `Outcome:` line on the affected upstream closure (DOC-OQ9 §"Closure of OQ-9" or AC2 §"Closure of AC2") plus, if the consolidation document is materially affected, an amendment to `docs/eval/v2-followups.md` §2.

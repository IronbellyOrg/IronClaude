---
spec_under_review: .dev/releases/current/cliEval/design-spec.md
review_date: 2026-05-18
generator: sc:spec-panel
mode: critique
format: standard
iterations: 1
expert_panel: [wiegers, adzic, cockburn, fowler, nygard, whittaker, newman, hohpe, crispin, gregory, hightower]
focus_areas: [requirements, architecture, testing, correctness]
auto_suggested_focus: correctness  # 5+ mutable state vars + numeric thresholds + pipeline ops detected
mandatory_artifacts_triggered: [guard_condition_boundary_table, pipeline_dimensional_analysis]
---

# Spec-Panel Review: cliEval design-spec.md

## Quality Assessment Summary

| Dimension | Score | Notes |
|---|---:|---|
| Overall | **7.4 / 10** | Solid architecture, clear boundaries; gaps in correctness invariants + failure semantics |
| Requirements clarity | 7.8 / 10 | Goals/non-goals strong; some FRs lack measurable thresholds |
| Architecture quality | 8.2 / 10 | Composition over inheritance correct; module boundaries clean |
| Testability | 6.9 / 10 | Harness tests planned; eval-level acceptance criteria under-specified |
| Adversarial robustness | 5.8 / 10 | Multiple zero/empty + sentinel attacks succeed |
| Operational fitness | 6.5 / 10 | Resource accounting partial; signal/cleanup edges under-defined |

**Verdict:** APPROVED-WITH-REVISIONS. 4 CRITICAL findings + 9 MAJOR + 6 MINOR. None are architectural-rework class; all are tractable spec amendments. Suggest one revision pass before `/sc:tasklist`.

---

## 1. Karl Wiegers — Requirements Quality

### W-1 ❌ CRITICAL — Goal G5 lacks falsifiable acceptance criterion
**Section:** §1 Goals, item 5 ("Catch the bug PR #49 fixed and any equivalent future regression")
**Issue:** "Equivalent future regression" is not measurable. What classes of regression count? Hook-matcher drift only? Or all `~/.claude/` mutation drift?
**Recommendation:** Replace with: "Detect when a registered PostToolUse hook with matcher pattern P fails to fire for a real MCP tool call matching P (per-prefix coverage of mcp__auggie__, mcp__auggie-mcp__, mcp__airis-mcp-gateway__)."
**Priority:** High — without this, "did the harness do its job?" is unanswerable.

### W-2 ⚠️ MAJOR — Per-eval timeout defaults are unsourced
**Section:** §5 manifest `per_eval_timeout_sec: 120`; §11 lists evals up to 90s
**Issue:** No rationale tying 120s to observed Claude Code startup + MCP call latency. On a cold-cache run with `mcp_server.auggie` reachable but slow, 120s may be tight.
**Recommendation:** Add a "Timing budget" subsection: TTY-spawn ≈ 2-5s, hook-deploy ≈ 1.4s (cited from R2), prompt round-trip ≈ 10-90s. Document the 90th-percentile observation that justifies 120s.
**Priority:** Medium.

### W-3 ⚠️ MAJOR — `min_version` semantics for `claude` binary not specified
**Section:** §5 `{ name: claude, min_version: "0.5.0", failure_mode: hard }`
**Issue:** How is version compared? `claude --version` output is not in the spec. Semver? Lexicographic? What if the binary returns `0.5.0-rc1`?
**Recommendation:** Document the version-extraction regex and comparison rule (e.g., "PEP 440 strict semver, pre-release suffixes ignored for `min_version` compare").

### W-4 ℹ️ MINOR — `xfail_if` cited but no concrete consumer
**Section:** §11 "SOFT-XFAIL" tier described, but no eval in §5 example uses it
**Recommendation:** Either (a) cite the planned consumer eval ID, or (b) defer xfail until an actual user appears (YAGNI).

---

## 2. Gojko Adzic — Specification by Example

### A-1 ⚠️ MAJOR — Eval lifecycle diagram lacks degenerate inputs
**Section:** §6 lifecycle sequence
**Issue:** No example of what happens when (a) Claude Code never reaches "prompt ready", (b) the user's prompt is rejected by a hook (`exit 2`), (c) `inject_prompt` is called before pty is ready.
**Recommendation:** Add 3 Given/When/Then scenarios:
```gherkin
Given: HomeIsolation deployed, claude subprocess spawned
  And: Claude Code SessionStart hook exits non-zero (broken hook)
When: PtyDriver.expect_prompt_ready(timeout=30) is called
Then: TimeoutError after 30s; eval marked FAIL with reason "session_start_hook_failed"
  And: stderr.log contains the hook's error output
  And: HOME is preserved (keep=True override for failures)
```
**Priority:** High — these are exactly the scenarios E15 (hook timeout) needs to exercise.

### A-2 ℹ️ MINOR — `parameterize:` block expansion semantics
**Section:** §5 E2 parameterize example
**Issue:** Three params produce E2.1, E2.2, E2.3 — but `requires: [mcp_server.{{prefix.split('__')[1]}}]` uses Jinja-style templating that isn't defined anywhere else in the spec.
**Recommendation:** Either drop the Jinja syntax (define `requires` per-parameter) or document the templating engine + allowed expressions.

---

## 3. Alistair Cockburn — Use Cases & Stakeholders

### C-1 ⚠️ MAJOR — Primary actor for `eval doctor` is ambiguous
**Section:** §4 subcommand table; §11 doctor output
**Issue:** Is `eval doctor` for (a) the maintainer pre-flighting their machine, (b) the harness itself self-checking before `eval run`, or (c) both? Spec says "preconditions" — but the doctor's output format is human-only (no `--json` flag listed).
**Recommendation:** State explicitly: "Primary actor: maintainer. Secondary actor: `eval run` (calls `check_all()` internally; does NOT shell out to `eval doctor`)."
**Priority:** Medium.

### C-2 ℹ️ MINOR — Goal of `eval describe` under-specified
**Section:** §4 "Print the manifest content for a suite or single eval"
**Recommendation:** Add: success scenario ("`eval describe --suite real --eval E1` prints the loaded+normalized EvalSpec, including expanded parameterize sub-evals"); failure ("invalid ID exits 2 with 'eval not found in suite'").

---

## 4. Martin Fowler — Architecture & Interface Design

### F-1 ⚠️ MAJOR — `Expect.exit_code()` couples assertion to runner global state
**Section:** §8 Expect DSL
**Issue:** `Expect.exit_code().equals(0)` reads from where? The DSL is stateless; exit codes live in the EvalResult, not the assertion. The §8 example `Expect.exit_code().equals(0)(ctx)` resolves this through `ctx` — but the YAML form `{ type: exit_code, value: 0 }` doesn't have a `ctx` parameter.
**Recommendation:** Make explicit that all `Expect.*` instances are `Callable[[EvalContext], ExpectResult]`. The YAML-loader binds the EvalContext at runtime. Document `EvalContext` shape (has `.exit_code`, `.stdout`, `.stderr`, `.home_path`, `.duration_sec`, `.session_id`).
**Priority:** High — without this, `loader.py` cannot translate YAML into callables.

### F-2 ⚠️ MAJOR — `HomeIsolation.env()` merge order with `IsolationLayers.env()` undefined
**Section:** §7 + decisions.md D-3
**Issue:** Spec says "the caller merges with IsolationLayers.env() output" but doesn't define precedence. If both classes set `CLAUDE_SETTINGS_DIR`, which wins?
**Recommendation:** State: "HomeIsolation.env() takes precedence; merge is `{**IsolationLayers.env(), **HomeIsolation.env()}`. Document the 4 keys HomeIsolation introduces vs IsolationLayers' 4 — explicitly list any overlaps."

### F-3 ℹ️ MINOR — `AggregatedRunReport` borrows from sprint but adds methods
**Section:** §9 "Add `to_json()` and `to_junit()` (new methods, ~50 LOC each)"
**Recommendation:** If we're adding methods, consider whether `AggregatedRunReport` should be a subclass of `AggregatedPhaseReport` (inherits to_markdown/to_yaml) or a sibling with delegation. Subclass is simpler; spec doesn't pick.

---

## 5. Michael Nygard — Failure Modes & Operations

### N-1 ❌ CRITICAL — Zombie process risk on harness SIGKILL
**Section:** §12 signal handling
**Issue:** Spec covers SIGINT/SIGTERM cleanly but not SIGKILL of the orchestrator. If the harness PID is killed -9, every spawned `claude` subprocess + every `pexpect` thread is orphaned. The per-eval HOME dirs leak. The user's box ends up with 15 detached claude processes.
**Recommendation:** Use a process group (`os.setsid()` in each `PtyDriver.spawn()`) and document: "Children inherit the orchestrator's process group. On orchestrator SIGKILL, OS cleans up children via the process group; HOMEs remain (acceptable leak, documented behavior)." Also: add a `superclaude eval cleanup` subcommand for `.dev/eval-runs/*/evals/*/home/` GC.
**Priority:** High.

### N-2 ❌ CRITICAL — `--max-disk-mb` cited as risk mitigation but absent from §4 flags
**Section:** §14 R4 mitigation says "Add `--max-disk-mb` limit" but §4's flag table doesn't include it.
**Recommendation:** Either (a) add `--max-disk-mb` flag (default 1024) with check at run-start + interval polling, OR (b) acknowledge in R4 that mitigation is "fail-open / user must monitor disk manually" and downgrade severity.
**Priority:** High — spec is internally inconsistent.

### N-3 ⚠️ MAJOR — MCP server flakiness retry policy under-specified
**Section:** §14 R3 mitigation: "Per-eval retry-once on MCP-specific failure modes"
**Issue:** What counts as "MCP-specific"? Hook-side `mcp__` event missing? Subprocess timeout? Specific stderr regex? Without a classifier, retry policy fires randomly.
**Recommendation:** Define an `MCPFailureClassifier` interface: returns `True` only if (a) the expected `expect_tool_call` MCP tool event is absent from JSONL telemetry AND (b) stderr contains one of `[connection refused, timeout, server not reachable]`. Otherwise non-retry.

### N-4 ⚠️ MAJOR — Hook-script deployment is not atomic
**Section:** §7 HomeIsolation.setup() + §10 reuse of `install_hooks.py`
**Issue:** If setup() crashes midway (e.g., between deploying script 5 of 9 and writing settings.json), the HOME is in a half-installed state. Spec doesn't say whether `teardown()` is called for failed setups, or whether the partial HOME is treated as a "fail with preserved HOME for diagnosis."
**Recommendation:** Wrap setup in try/except; on exception, mark eval ERRORED (distinct from FAILED), call teardown with `keep=True`, and emit a `setup_failed` artifact tag.

### N-5 ℹ️ MINOR — Per-eval memory limit (`per_eval_memory_mb: 512`) is unenforced
**Section:** §5 default
**Issue:** Spec lists the default but no mechanism enforces it. Python `resource.setrlimit(RLIMIT_AS)` on the child? cgroups? Or is it documentation-only?
**Recommendation:** Either implement (resource.setrlimit before exec) or downgrade to "advisory, documented expected RSS only."

---

## 6. James Whittaker — Adversarial Probing

I can break this specification by **multiple methodologies**. Findings below in severity order.

### Wh-1 ❌ CRITICAL — Sentinel Collision Attack on `eval_id` in path templates
**Invariant:** §7 `state_path(suffix)` resolves `{session_id}` and `{project_key}` templates.
**Condition:** What if a user authors a manifest with `eval_id: "E1/../etc/passwd"` or `eval_id: "{session_id}"` (self-referencing template)?
**Concrete attack:**
- State before: manifest contains `id: "../../../etc/passwd"`.
- Attack: loader.py accepts the ID. HomeIsolation.setup() builds `home_root / eval_id / home`, escaping the scratch dir.
- State after: the §14 R7 "Hard guard refuses if HOME outside eval-runs scratch dir" *might* catch this, but only if guard does post-normalize check; spec says "if HOME points outside" — ambiguous on whether `..` is resolved before check.
**Severity:** CRITICAL.
**Remediation:** `loader.py` MUST validate `eval_id` against `^[A-Z][0-9]+(\.[0-9]+)?$` regex; HomeIsolation MUST `Path.resolve()` then `is_relative_to(scratch_root)` before any write.

### Wh-2 ⚠️ MAJOR — Zero/Empty Attack on `--parallel 0`
**Invariant:** §4 "Clamped to [1, 15]"
**Condition:** Spec says clamped, doesn't say where. What if Click parses `--parallel 0` and orchestrator divides by it?
**Concrete attack:** `--parallel 0` → ThreadPoolExecutor(max_workers=0) → Python `ValueError`. Or worse, `--parallel -1` silently means "unlimited" on some platforms.
**Severity:** MAJOR.
**Remediation:** Click type `IntRange(1, 15, clamp=True)`. Reject `--parallel 0` at CLI parse, not at orchestrator.

### Wh-3 ⚠️ MAJOR — Divergence Attack on capability_gates failure_mode
**Invariant:** §11 three tiers — HARD aborts, SOFT-SKIP marks skipped, SOFT-XFAIL marks xfail.
**Condition:** What if a Capability has `failure_mode: hard` AND the user passes `--no-mcp` AND the gate fires?
**Concrete attack:** Maintainer sets `mcp_server.auggie` to `failure_mode: hard` (typo in their fork), user runs `--no-mcp`. Does --no-mcp override "hard"? Spec is silent.
**Severity:** MAJOR.
**Remediation:** Document precedence: "skip_flag presence overrides failure_mode for that capability only."

### Wh-4 ⚠️ MAJOR — Accumulation Attack on JSONL log growth
**Invariant:** §8 `JsonlExpect.contains_event` reads the per-eval `auggie-first.jsonl`.
**Condition:** What if a hook is buggy and writes 10MB of log lines during one eval? `JsonlExpect` may scan the whole file looking for one event, blocking the eval past timeout.
**Concrete attack:** Hook in infinite-loop appending; eval marked TIMEOUT not because of Claude Code latency but because of assertion scan time.
**Severity:** MAJOR.
**Remediation:** Cap JSONL scan: bail with `JsonlScanLimit` after 1MB or 10k lines, mark eval FAILED with reason `jsonl_runaway`.

### Wh-5 ℹ️ MINOR — Sequence Attack on `seed_state` before deploy
**Invariant:** §7 setup() order: "mkdtemp HOME → deploy hooks → seed state → write settings"
**Condition:** What if `seed_state` references a path under `.claude/state/` that doesn't exist yet because hook-deploy hasn't created `.claude/state/` dir?
**Severity:** MINOR.
**Remediation:** Make order explicit: "mkdtemp → write settings (creates .claude/) → deploy hooks → mkdir -p state dirs → seed state."

---

## 7. Sam Newman — Service Boundaries & API Evolution

### Sn-1 ⚠️ MAJOR — Schema version field exists but no migration policy
**Section:** §5 `version: "1.0"` in manifest
**Issue:** What happens when a future suite uses `version: "1.1"`? Strict equality? Compatible-range check? The loader behavior is undefined.
**Recommendation:** Document: "Loader accepts MAJOR=1 manifests; rejects MAJOR>=2 with error. Minor version bumps must be backward-compatible (additive fields only)."

### Sn-2 ℹ️ MINOR — `Expect.*` DSL has no deprecation path
**Section:** §8
**Recommendation:** If/when an Expect method is renamed, what's the deprecation policy? One release of dual-availability? Hard break? Note this in §8 even if the answer is "we'll cross that bridge later."

---

## 8. Gregor Hohpe — Integration & Data Flow

### G-1 ⚠️ MAJOR — Hook telemetry → Expect.jsonl is a many-to-one channel without ordering guarantees
**Section:** §8 `JsonlExpect.contains_event` + §6 lifecycle
**Issue:** Multiple hooks (PostToolUse, UserPromptSubmit, SessionStart) may all append to `auggie-first.jsonl` concurrently within a single eval. POSIX append-write is atomic up to PIPE_BUF (typically 4096 bytes); a 5KB JSONL line could interleave.
**Recommendation:** Either (a) require each hook to write its own JSONL file (`session_start.jsonl`, `post_tool_use.jsonl`, etc.), OR (b) document the 4KB line-size limit in the hook authoring guide + verify in `Expect.jsonl(...).is_valid_jsonl()`.

### G-2 ℹ️ MINOR — No spec for how `expect_tool_call` is observed
**Section:** §5 `inputs.expect_tool_call: mcp__auggie__codebase-retrieval`
**Recommendation:** Document the observation path: does the runner watch hook JSONL for a `tool_use` event, or scrape the TTY stdout, or both? Pick one.

---

## 9. Lisa Crispin — Testing Strategy

### Cr-1 ⚠️ MAJOR — Self-test coverage is named but not specified
**Section:** §10 "6 new test files under `tests/cli/test_eval/`"
**Issue:** No coverage targets, no acceptance criteria for the harness tests themselves. What's the bar for "test_orchestrator passes"? Lines? Branches? Specific scheduling scenarios?
**Recommendation:** Add per-test-file acceptance criteria:
- `test_orchestrator.py`: covers (a) all-pass run, (b) one-fail run, (c) SIGINT mid-run, (d) timeout-kill, (e) parallel=1 vs parallel=15 result equivalence
- `test_isolation.py`: covers (a) HOME path containment guard, (b) cleanup-on-success, (c) cleanup-skip-on-failure, (d) concurrent setups don't collide
- etc.

### Cr-2 ℹ️ MINOR — `--no-pty` mode untestable as specified
**Section:** §4 `--no-pty` flag "For logic-only runs in constrained environments"
**Recommendation:** Clarify what evals can possibly run without a TTY. If none, what does `--no-pty` actually do? (Possibly: skip the entire suite and emit a "no pty-capable evals to run" message.)

---

## 10. Janet Gregory — Spec Workshops & Quality

### Gr-1 ℹ️ MINOR — Manifest authoring guide TBD
**Section:** §3 `suites/README.md` "how to author a suite manifest"
**Recommendation:** Stub this as a deliverable in Phase 2 (loader/models/expect phase). Without an authoring guide, eval-body authors will reverse-engineer from existing YAML.

### Gr-2 ℹ️ MINOR — No three-amigos artifact for E1-E15 scope
**Recommendation:** Before Phase 5 (eval bodies), require a 1-page-per-eval acceptance criteria sheet jointly reviewed by maintainer + spec author. Defer from this design but capture as a Phase-5 entrance criterion.

---

## 11. Kelsey Hightower — Operational Concerns

### H-1 ⚠️ MAJOR — Observability of the harness itself is absent
**Section:** Entire spec
**Issue:** When the harness misbehaves in production (say, a maintainer's CI), what telemetry exists? Spec covers per-eval artifacts but not harness-level metrics (total wall time, max RSS, scheduling latency, retry counts).
**Recommendation:** Add `summary.json` fields: `harness.scheduling_overhead_sec`, `harness.peak_thread_count`, `harness.peak_rss_mb`, `harness.retries_attempted`.

### H-2 ℹ️ MINOR — `XDG_*` overrides under-enumerated
**Section:** §7 "`HOME` (and `XDG_*` overrides)"
**Recommendation:** Spell out the four XDG vars set: `XDG_CONFIG_HOME=$HOME/.config`, `XDG_CACHE_HOME=$HOME/.cache`, `XDG_DATA_HOME=$HOME/.local/share`, `XDG_STATE_HOME=$HOME/.local/state`. Otherwise a maintainer-side env leak (e.g., `XDG_CONFIG_HOME=/etc`) bypasses isolation.

---

## Mandatory Artifact: Guard Condition Boundary Table

**Trigger:** §4 flag clamps + §11 capability tiers + §7 HOME guard + §12 timeouts.
**Responsible:** Nygard (lead), Crispin (completeness), Whittaker (adversarial).

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|-------|----------|-----------------|----------------|--------------|-------------------|--------|
| `--parallel` clamp | §4 flags | Zero/Empty | `0` | reject | undefined (clamp says [1,15] but entry point unclear) | **GAP** (Wh-2) |
| `--parallel` clamp | §4 flags | One/Minimal | `1` | accept | sequential run | OK |
| `--parallel` clamp | §4 flags | Typical | `8` | accept | default parallelism | OK |
| `--parallel` clamp | §4 flags | Maximum/Overflow | `15` | accept | max | OK |
| `--parallel` clamp | §4 flags | Above max | `16` | clamp to 15 | clamped silently? error? | **GAP** |
| `--parallel` clamp | §4 flags | Negative | `-1` | undefined | not specified | **GAP** |
| HOME-scratch guard | §7 invariant 1 + §14 R7 | Typical | `/tmp/eval-runs/.../home` | accept | proceed | OK |
| HOME-scratch guard | §7 invariant 1 | Sentinel Match | `$HOME` (real user home) | reject (claimed) | abort with error | OK (if implemented) |
| HOME-scratch guard | §7 invariant 1 | Edge Case (symlink) | `/tmp/eval-runs/foo → $HOME` | undefined | not specified | **GAP** (need `realpath` resolution) |
| HOME-scratch guard | §7 invariant 1 | Edge Case (`..` traversal) | `/tmp/eval-runs/E1/../../../$HOME` | undefined | not specified | **GAP** (Wh-1) |
| Capability hard-fail | §11 HARD tier | `which claude` returns nonzero | absent | abort exit 2 | abort + error msg | OK |
| Capability hard-fail | §11 HARD tier | `claude --version` < min | `0.4.9` | abort exit 2 | abort, per W-3 format undefined | **GAP** (W-3) |
| Capability hard-fail | §11 HARD tier | `claude --version` has pre-release | `0.5.0-rc1` | undefined | not specified | **GAP** (W-3) |
| Capability skip vs hard | §11 mixed | hard cap + `--no-mcp` skip flag set | both | undefined precedence | not specified | **GAP** (Wh-3) |
| per_eval_timeout_sec | §5 default 120 | Zero/Empty | `0` | undefined | infinite? immediate kill? | **GAP** |
| per_eval_timeout_sec | §5 default 120 | Typical | `120` | accept | timeout enforced | OK |
| per_eval_timeout_sec | §5 default 120 | Multiplied by `--timeout-mult 0` | `0` | undefined | per W-2 timing budget gap | **GAP** |
| Hook-deploy completion | §7 setup() | Crash mid-deploy | partial state | undefined | per N-4 atomicity gap | **GAP** (N-4) |

**GAP count:** 9 of 18 rows = 50% gap rate. **FR-8 trigger:** Each GAP automatically generates a MAJOR finding minimum (some elevated above as CRITICAL by attack chains).

**FR-10 Synthesis-Blocking Gate:** Table complete. Synthesis proceeds with explicit notation that all GAPs are downstream consumption priorities for `sc:adversarial` AD-1 invariant probing.

---

## Mandatory Artifact: Pipeline Dimensional Analysis

**Trigger:** §6 multi-stage eval lifecycle (orchestrator → runner → isolation → pty → assert → reporter).
**Responsible:** Fowler (pipeline ID + counts), Whittaker (divergence attack).

### Quantity Flow Diagram

```
[Manifest: N eval_specs]
        │
        ▼
[Loader: validate + expand parameterize]
        │       N items in,  N' items out  (N' = N + Σ(parameter_count - 1) per parameterize block)
        ▼
[Capability gating]
        │       N' items in,  S skipped,  K kept  (K + S = N';  K = filter(no-mcp, no-pty, etc.))
        ▼
[Orchestrator: ThreadPoolExecutor]
        │       K items in,  K results out
        ▼
[Reporter: AggregatedRunReport]
        │       K results in,  K rows in summary.md + (K + S) rows expected by maintainer
                                                  ▲
                                                  └── MISMATCH if reporter omits skipped evals
```

### Divergence findings

| Stage | In | Out | Spec covers? |
|---|---|---|---|
| Loader → parameterize expansion | N | N' | Partial — §5 mentions E2.1/E2.2/E2.3 but never quantifies expansion. **GAP** |
| Capability filter | N' | K | §11 says "Mark gated evals as SKIPPED" but does report count K or N'? **GAP** |
| Orchestrator → reporter | K | K | OK (one-to-one) |
| Reporter aggregate | K (passed/failed) + S (skipped) | summary | §9 shows `"skipped": 0` in JSON example — should include skipped per maintainer expectation. Status implicit. |

### CRITICAL finding (FR-19)

**Dimensional mismatch — reporter input counts.** §9 summary.md example shows `14 passed, 1 failed, 0 skipped` summing to 15 (full suite). But if `--no-mcp` skips E1, E2.1, E2.2, E2.3, and a fifth eval, the spec doesn't make clear whether the reporter receives K=10 EvalResults or K+S=15 EvalResults-with-status. If only K=10, the user has no audit trail of what was skipped and why.

**Concrete scenario:** Maintainer runs `--no-mcp` on a 15-eval suite. Orchestrator schedules 10 (skipping 5 MCP-gated). Reporter receives 10 EvalResults. Summary shows "10 passed, 0 failed" — looks like a successful full run, but 5 evals were silently dropped. The skipped evals don't appear because the reporter's input count diverged from the loader's output count.

**Remediation:** Spec must state: "Capability filter produces a list of `(eval_id, status, reason)` triples where status ∈ {KEPT, SKIPPED-NO-MCP, SKIPPED-NO-PTY, ...}. The reporter consumes the full N' list, not just the K KEPT subset." Update §9 schema accordingly.

---

## Expert Consensus

Six experts independently flagged related concerns; convergence points:

1. **Boundary semantics need tightening.** (Wiegers W-3, Whittaker Wh-1/Wh-2, Nygard N-2) — version compare, parallel clamp, path resolution, max-disk-mb. Resolve via a single "Inputs & Boundaries" subsection in §4.
2. **Failure-mode taxonomy is sparse.** (Nygard N-4, Whittaker Wh-3, Newman Sn-1) — distinguish FAILED vs ERRORED vs SKIPPED vs TIMEOUT vs INTERRUPTED vs SETUP-FAILED. The §9 schema shows 4 status values; spec text implies more.
3. **Concurrency/atomicity gaps.** (Hohpe G-1, Nygard N-1/N-4, Whittaker Wh-4) — JSONL interleave, hook-deploy atomicity, zombie cleanup. All resolved by either splitting JSONL channels per hook or by adding atomicity guarantees.
4. **Audit trail for skipped evals.** (Pipeline analysis CRITICAL + Cockburn C-1) — reporter must consume the full N' list, not just K kept.

---

## Improvement Roadmap

### Immediate (block `/sc:tasklist` until resolved)
1. Resolve W-1: write a falsifiable acceptance criterion for G5.
2. Resolve N-2: decide on `--max-disk-mb` flag, add or strike the R4 mitigation.
3. Resolve Wh-1: add `eval_id` regex validation + path-resolve-then-contain check in §7.
4. Resolve Pipeline CRITICAL: reporter consumes N' (with status) not K.

### Short-term (resolve before Phase 1 implementation)
5. F-1: spec out `EvalContext` shape (used by every Expect callable).
6. F-2: define `HomeIsolation.env()` merge precedence with `IsolationLayers.env()`.
7. N-1: process-group cleanup strategy for SIGKILL.
8. N-3: define MCPFailureClassifier criteria.
9. A-1: 3 Given/When/Then scenarios for failure paths.
10. Sn-1: schema version compatibility policy.
11. G-1: JSONL-per-hook or 4KB line-size discipline.

### Long-term (resolve before Phase 5 eval bodies)
12. Cr-1: per-test acceptance criteria for harness self-tests.
13. Gr-1: write `suites/README.md` authoring guide.
14. H-1: harness-level observability fields in summary.json.
15. W-2: timing-budget subsection with empirical 90th-percentile data.

---

## Downstream Integration Wiring (for sc:tasklist / sc:roadmap)

| Source | Target | Data Flow |
|---|---|---|
| Guard Condition Boundary Table (GAP rows ×9) | `sc:adversarial` AD-1 | Invariant probe priority queue |
| Whittaker attack findings (Wh-1..Wh-5) | `sc:adversarial` AD-2 | Assumption-challenge round |
| Pipeline CRITICAL (reporter dimensional mismatch) | `sc:roadmap` RM-3 / `sc:tasklist` | Risk-weighted prioritization; spec amendment required *before* tasklist generation |
| Consensus points 1-4 | `sc:roadmap` RM-2 | Cross-cutting assumption tracking |

---

## Final Recommendation

**Status:** APPROVED-WITH-REVISIONS.

The architecture is sound (composition over inheritance for HomeIsolation; ThreadPoolExecutor matches existing sprint pattern; YAML-first with Python escape hatch is the right shape). The 4 CRITICAL findings are spec-amendment-class, not architectural-rework-class — addressable in a single revision pass to design-spec.md + decisions.md.

**Recommended next step:** Revise design-spec.md addressing the four "Immediate" items above (W-1, N-2, Wh-1, Pipeline CRITICAL). Then proceed to `/sc:workflow` → `/sc:tasklist`. The other items can land as inline spec amendments during Phase 1-4 implementation, tracked as MIGs in the build-request files.

# Wave 1.6 Diagnosability Audit — Merged Specification

<!-- Provenance: produced by /sc:brainstorm via sc-adversarial-protocol on 2026-05-29.
     Base: V3 (devops). Incorporations: V1 (architect), V4 (field study).
     adversarial_status: success (convergence 0.78, threshold 0.75). -->

**Status**: Spec for incorporation into `src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md`. Not yet applied to the live skill.
**Target wave version**: v1.0 (additive to current 7-wave protocol; v1.1 follow-ups noted inline)
**Created**: 2026-05-29
**Settled forks (locked)**: scope=logging-only-narrow; placement=between-1.5-and-1.7; default=on-with-opt-out.

---

## 1. Wave 1.6 Placement & Entry/Exit Criteria

<!-- Source: Variant 3 (base) with V1 SKILL.md diff fidelity + V4 component-identification step S0.1 -->

**Position in graph**:

```text
Wave 0: Parse + Validate Input
Wave 1: Tier 1 — Real-Code Grounding
Wave 1.5: Documentation Grounding
Wave 1.6: Diagnosability Audit          ← NEW
Wave 1.7: Tier 1 — Hypothesis Formation
Wave 2: Confidence Gate
Wave 3-6: (unchanged)
```

**Preconditions**:

- Wave 1 complete (real-code grounding done; `<output-dir>/tier1-observation.md` written).
- Wave 1.5 complete or skipped via `--no-doc-discovery` (`doc_context_card_path` is a real path or `null`).
- `--no-diagnosability-audit` is NOT set. When IT IS set: skip the wave entirely, emit `diagnosability_verdict: unknown`, `diagnosability_context_card_path: null`, `diagnosability_hard_stop: false`. **The bypass is logged in REPORT.md's header and in the audit log** (variant-4 §6 R5).
- Wave 1 has localized at least one `<component_path>` or `<scope>` — Wave 1.6 needs a code surface to inspect.

**Steps** (5 substeps):

1. **S1.6.0 — Component identification** (variant-4 §3.3 S0.1). Before any branch fan-out, identify the smallest component whose output the failure asserts against. Source priority: (a) `--scope` from Wave 0 if set; (b) stack-trace bottom frame from Wave 1's observation; (c) named subsystem in the Wave 0 issue text; (d) named test in the failure transcript. Record as `failing_component` in the audit log. Branches A and B scope queries to this component first; expand outward only if no signal is found.

2. **S1.6.1 — Load `refs/diagnosability-audit.md`** (lazy load, mirroring Wave 1.5's discipline). Read Section 1 (query templates), Section 2 (fallback paths), Section 3 (per-branch schemas), Section 4 (sufficiency rubric + 3-W's synthesis), Section 5 (complexity gate), Section 6 (Diagnosability Context Card template), Section 7 (tasklist rules), Section 8 (T4 worked example).

3. **S1.6.2 — Spawn 2 audit branches in parallel** via `Task` (single message, two Task calls):
   - **Branch A — Log-Call Inspection**: logger/print/exception-handler calls + error-reporter SDK initializations on the `failing_component` and immediate callers. Captures exception-handler richness as a piggyback signal (no separate branch).
   - **Branch B — Log-Config Inspection**: log-config files, env vars, structured-log filters, sampling configuration that governs runtime log emission for the `failing_component`.

4. **S1.6.3 — Wait for branches; synthesize Diagnosability Context Card** at `<output-dir>/diagnosability-context.md`. Synthesis includes the **3 W's coverage scoring** (variant-1 Branch F preserved as orchestrator logic): `{ when_answerable, where_answerable, why_answerable } ∈ { yes | partial | no }`, computed against Branch A inventory + Branch B reachability + Wave 1 observation. **Byte-count column** populated from runtime-content sniffs of any log file paths discoverable from the failing-run transcript; `n/a (audit-time only)` when no captured-content is available (variant-4 §3.3 S0.2 additive).

5. **S1.6.4 — Apply sufficiency rubric + complexity gate**. Compute `diagnosability_verdict ∈ {sufficient | partial | insufficient | unknown}`. Compute `issue_complexity ∈ {trivial | non-trivial}` from Wave 0 + Wave 1 signals only (no Wave 1.7 dependency). Branch on `(verdict × complexity)`:
   - `insufficient` AND `non-trivial` AND NOT `--no-escalate` → **hard-stop**: emit `diagnosability-tasklist.md`, set `diagnosability_hard_stop=true`, jump to Wave 5 with status `partial` (Waves 1.7-4 skipped). **No hypothesis work happens in the same turn as the instrumentation patch** (variant-4 §3.5).
   - `insufficient` AND `non-trivial` AND `--no-escalate` → soft-warn (suppressed by user assertion). Emit tasklist, surface in REPORT.md, continue to Wave 1.7.
   - `insufficient` AND `trivial` → soft-warn: emit tasklist (informational), continue to Wave 1.7.
   - `partial` → continue to Wave 1.7; surface in REPORT.md's Diagnosability Context section.
   - `sufficient` OR `unknown` → continue to Wave 1.7; surface in Diagnosability Context (or Grounding Gaps for `unknown`).
   - **`--depth deep` modifier**: does NOT force the hard-stop, BUT when `verdict ∈ {insufficient, partial}` under `--depth deep`, the soft-warn becomes **mandatory and prominent** — REPORT.md gains a top-of-report banner: "Your hypothesis depth was constrained by insufficient evidence — see Diagnosability Context."

**Per-defect patch-round counter** (variant-4 §3.7 additive): the Wave 1.6 orchestrator maintains `<output-dir>/diagnosability-rounds.json` keyed by the Wave 0 `issue_slug`. Each hard-stop fires the counter +1. After 3 rounds for the same defect, the off-ramp message escalates (see §7 Off-Ramp UX). Reset via `--reset-diagnosability-rounds`.

**Exit criteria**:

- Two branch outputs at `<output-dir>/wave1_6-branch-<A|B>.md`.
- Diagnosability Context Card at `<output-dir>/diagnosability-context.md`.
- Diagnosability tasklist at `<output-dir>/diagnosability-tasklist.md` (when verdict ∈ {partial, insufficient}).
- Emit `Wave 1.6 complete: verdict=<v> complexity=<c> hard_stop=<bool> round=<N>/3`.

**Token budget**: ≤ 2-3k Claude tokens (auggie offloads retrieval bulk). Hard-stop case yields a *net token saving* over the full Tier 2 pipeline.

---

## 2. Audit Mechanics

<!-- Source: Variant 3 (base) — 2-branch fan-out with literal auggie queries and bash fallbacks -->

### Branch structure: 2-branch parallel fan-out (NOT 3)

Branch A captures both logger calls and exception-handler richness in a single retrieval because the same auggie query names both patterns. A separate exception-handler branch would duplicate the code-surface scan at additional Claude-token cost. Branch B is mandatory because log-config lives in entirely different files and requires a different retrieval strategy.

### Branch A — Log-Call Inspection

**Auggie query string**:

```
In the codebase at <failing_component> (or <scope> if broader), find every location that produces diagnostic signal around the behavior described as: <symptom>. This includes:

1. Python: logging module calls (logging.debug/info/warning/error/exception/critical), loguru calls, print() statements, structlog calls.
2. JavaScript/TypeScript: console.log/warn/error/debug/info, winston/pino/bunyan logger calls.
3. Java: SLF4J/Logback calls, Log4j2 calls, java.util.logging calls.
4. Exception handlers: try/except (Python), try/catch (JS/Java). For each, whether it logs the exception or silently swallows it.
5. Error-reporter initializations: Sentry.init(), Datadog.init(), rollbar.configure(), or equivalent.

For each hit, return: file path, line number, call_type (logger_call | print | exception_handler | error_reporter_init), framework, log level, 1-2 line snippet, and (for exception handlers) richness: rich | minimal | silent.
```

**Fallback path** (auggie unavailable — full bash command set per variant-3 source):

```bash
grep -rn 'logging\.\(debug\|info\|warning\|error\|exception\|critical\)\|logger\.\(debug\|info\|warning\|error\|exception\|critical\)\|from loguru import' <failing_component>
grep -rn 'print(' <failing_component>
grep -rn 'console\.\(log\|warn\|error\|debug\|info\)' <failing_component>
grep -rn 'logger\.\(info\|warn\|error\|debug\)\|log\.\(info\|warn\|error\|debug\|trace\)' <failing_component>
grep -rn 'except\s*:' <failing_component>
grep -rn 'catch.*{.*}' <failing_component>
grep -rn 'Sentry\.init\|Datadog\.init\|rollbar\.config' <failing_component>
```

**Schema** (per `refs/diagnosability-audit.md` Section 3):

```json
{
  "branch": "A",
  "query_target": "<failing_component>",
  "hits": [
    {"file_path": "...", "line": 142, "call_type": "logger_call", "framework": "logging",
     "level": "info", "snippet": "...", "richness": "rich", "distance_to_symptom": "in_function",
     "captured_bytes": 0 }
  ],
  "degraded": false
}
```

The `captured_bytes` field (variant-4 additive) is populated when the failing-run transcript referenced specific log files — sniffed via `wc -c <file>` if accessible at audit time. Otherwise `null`.

### Branch B — Log-Config Inspection

**Auggie query string**:

```
In the entire repository, find every configuration file or environment-variable reference that controls logging behavior for <failing_component>:

1. Python: logging.yaml/.yml/.conf/.ini, log_config.py, [tool.logging] in pyproject.toml.
2. Java: log4j2.xml/.properties, logback.xml, application.properties/.yml with logging.* keys.
3. JS/Node: winston.config.js, logger.js, pino transport config, .env with LOG_LEVEL/DEBUG/NODE_ENV.
4. Env vars: LOG_LEVEL, LOGLEVEL, DEBUG, NODE_ENV=production, LOG_FORMAT=json in Dockerfile, docker-compose.yml, .env*, Makefile, CI pipeline files.
5. Structured-log filter/rate-limit config, sampling configuration.

For each hit, return: file path, config_type (file | env_var | pipeline_config), framework, effective log level if discernible, 1-3 line snippet.
```

**Fallback path**:

```bash
find . -name 'logging.{yaml,yml,conf,ini}' -o -name 'log4j2.*' -o -name 'logback*.xml' -o -name 'winston*.js' -o -name 'logger.js' 2>/dev/null
grep -n '\[tool\.logging\]\|\[tool\.pytest\.ini_options\].*log' pyproject.toml
find . -name 'application*.{properties,yml,yaml}' 2>/dev/null
grep -rn 'LOG_LEVEL\|LOGLEVEL\|DEBUG\s*=\|NODE_ENV\|LOG_FORMAT' .env* Dockerfile docker-compose.yml Makefile .github/workflows/*.yml .gitlab-ci.yml 2>/dev/null
```

**Schema** (per `refs/diagnosability-audit.md` Section 3): array of `{ config_path, config_type, framework, effective_level, snippet, location }` plus a derived `reachability_verdict: reaches_sink | filtered_out | unknown` per Branch A hit.

### Orchestrator synthesis: 3-W's coverage scoring (variant-1 Branch F preserved)

After Branches A and B return, the Wave 1.6 orchestrator computes (no MCP call):

| W | Answerable from existing instrumentation? | Signal |
|---|------------------------------------------|--------|
| **When** | Branch A has timestamped logger calls within `failing_component` AND Branch B confirms `reaches_sink` | `yes` |
| **Where** | Branch A has logger calls naming the symptom site (file + line via stack-trace mapping) | `yes` |
| **Why** | Branch A has state-capturing logger calls (fields, args, return values, exception context) near symptom site AND Branch B confirms reachability | `yes` |

Each W is `yes | partial | no`. The triple feeds the sufficiency rubric (Section 3 below).

---

## 3. Sufficiency Rubric

<!-- Source: Variant 3 (base) with V1 worked-example structure + V4 byte-count promotion -->

Applied in order. First match wins.

| Signal combination | Verdict |
|--------------------|---------|
| **S1**: Symptom is a deterministic exception with a clear stack trace bottoming in user code | `sufficient` (stack trace IS the signal — variant-1 short-circuit) |
| **S2**: Symptom is a build/compile error with line-numbered diagnostic | `sufficient` |
| **S3**: Branch A has ≥3 structured logger calls within `failing_component` AND Branch B confirms `reaches_sink` AND 3-W's coverage all `yes` | `sufficient` |
| **S4**: 3-W's coverage has 2 `yes` + 1 `partial`, Branch A moderate density, Branch B `reaches_sink` | `sufficient` (with caveat noted in card) |
| **S5**: Branch A has captured-bytes > 0 for some streams but 0 bytes for the stream that would have answered the failing W | `insufficient` (variant-4 byte-count rule — static density alone is misleading) |
| **S6**: Branch B `filtered_out` (e.g., level=WARNING but only INFO logs near symptom) | `partial` (if Branch A has higher-level calls) or `insufficient` (if no calls at or above filter level) |
| **S7**: Error-reporter SDK (Sentry/Datadog) initialized AND would capture the symptom class | `sufficient` |
| **S8**: 1-2 logger calls at INFO, no exception-handler logging, no error reporter | `partial` (if deterministic) or `insufficient` (if intermittent) |
| **S9**: Only `print()` statements, no structured logger | `partial` (deterministic) or `insufficient` (intermittent / multi-threaded) |
| **S10**: No logger calls, no print, no error reporter near symptom site | `insufficient` |
| **S11**: Auggie unavailable AND Glob/Grep fallback returned no signal AND Branch A `degraded=true` | `unknown` |
| **S12**: `failing_component` not localizable (no `--scope`, stack trace bottoms in compiled code) | `unknown` |
| **S13**: Intermittent keywords present AND 3-W's `when_answerable != yes` | `insufficient` (intermittent-with-no-trace short-circuit — variant-1) |

### Worked Example 1 — NameError (`sufficient`)

User reports `NameError: name 'Path' is not defined` at `eval_run.py:142`. Branch A finds no logger calls near line 142. Branch B finds `logging.yaml` with `level: WARNING`. S1 fires → **`sufficient`** (the Python stack trace names the file, line, missing symbol, and the fix). No instrumentation would have added diagnostic value. Wave 1.6 continues to Wave 1.7.

### Worked Example 2 — Intermittent race condition (`insufficient` → hard-stop if non-trivial)

User reports "worker occasionally hangs, no error, just stops processing." Branch A finds one `logger.info("task_started")` at `worker.py:42` and a bare `except: pass` at `worker.py:198`. No request_id, no correlation token, no timing fields. Branch A `captured_bytes=4096` for `worker.log` (existing logs are present and reaching the sink). Branch B finds `LOG_LEVEL=INFO` in `.env`. 3-W's: when=`partial`, where=`partial`, why=`no`. S13 fires (intermittent keyword + when ≠ yes) → **`insufficient`**. Complexity gate scores 3+ (intermittent + performance type + multi-module scope) → `non-trivial`. **Hard-stop fires; tasklist emitted.**

### Worked Example 3 — Config-suppressed signal (`partial`)

User reports "API returns 500 for POST /submit but no error in logs." Branch A finds `logger.error("submit_failed", error=str(e))` at `api.py:88` with full exception context. Branch B finds `logging.yaml` with `level: WARNING` and no `pyproject.toml` logging section. 3-W's: when=`yes`, where=`yes`, why=`yes` (the existing call captures everything; the config does NOT suppress ERROR-level). S3 fires → **`sufficient`**. If Branch B had returned `level: CRITICAL`, S6 second branch would fire → `insufficient` (ERROR suppressed).

### Behavior under degradation

| Scenario | Verdict | Surfaced in |
|----------|---------|-------------|
| Auggie unavailable, Grep/Glob found signal | `partial` (cap; degraded discovery loses semantic recall) | Diagnosability Context Card with `degraded: true` |
| Auggie unavailable, Grep/Glob found nothing | `unknown` | Grounding Gaps |
| `failing_component` not localizable | `unknown` | Grounding Gaps |
| `--no-diagnosability-audit` | not emitted (audit skipped); `diagnosability_verdict: unknown` in contract | REPORT.md header + Grounding Gaps |

---

## 4. Complexity Gate

<!-- Source: Variant 3 (base) — convergent with V1; both picked Option (a) reuse-escalation-rubric -->

**Position on Open Question #1**: Reuse the existing escalation-rubric signals (Option A) with a narrower pre-hypothesis interpretation. No new classification surface. The rubric's structural dimensions (multi-domain, intermittent, security_caution) are extractable from Wave 0 + Wave 1 without running a hypothesis — no circular dependency on Wave 1.7.

**Signal table** (extracted at Wave 1.6 entry):

| Signal | Source | Weight |
|--------|--------|--------|
| `--type` is `performance` OR (`test` with intermittent/flaky keyword) | Wave 0 parse | +1 |
| Scope spans > 2 files | Wave 0 `--scope` resolution | +1 |
| Stack trace crosses > 2 modules | Wave 1 grounding | +1 |
| Issue text contains "occasionally", "sometimes", "race", "deadlock", "intermittent", "randomly", "only in CI/prod", "flaky" | Wave 0 parse | +1 |
| Issue text contains "slow", "p99", "memory", "regression", "leak" | Wave 0 parse | +1 |
| Cause class from Wave 1 triage ∈ {Race/concurrency, Stale state/cache, Performance/resource} | Wave 1 checklist scan | +1 |
| `--type security` set | Wave 0 parse | **Always non-trivial (override)** |

**Classification**:

- Score 0-1: `trivial` — hard-stop does NOT fire; soft-warn only.
- Score 2+ OR `--type security`: `non-trivial` — hard-stop fires if `verdict=insufficient` AND `--no-escalate` is not set.

**Trivial examples**: NameError single-file (score 0), missing-import with clear stack trace (score 0), off-by-one with stack trace naming the line (score 0), TypeError on a single-file scope with a deterministic repro (score 0-1).

**Non-trivial examples**: "Worker occasionally hangs" (intermittent + performance = 2), "API slow after refactor" (performance + regression + multi-module = 3), "Test passes locally, fails in CI" (test + intermittent + env-drift implied = 2), any `--type security` (override).

---

## 5. Output Contract Additions

<!-- Source: Variant 3 (base) — 4 fields, no status enum extension (debate Axis 3 verdict) -->

Four new fields. All additive, all backwards-compatible.

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `diagnosability_verdict` | `"sufficient" \| "partial" \| "insufficient" \| "unknown"` | `"unknown"` | Wave 1.6 verdict. `"unknown"` when audit could not run (auggie unavailable + Grep/Glob found nothing, `failing_component` not localizable, `--no-diagnosability-audit` set). Never silently skipped — always emit a verdict. |
| `diagnosability_context_card_path` | `string \| null` | `null` | **Repo-relative** path to `<output-dir>/diagnosability-context.md`. `null` only when `--no-diagnosability-audit` was set OR Wave 1.6 was not reached. When the wave runs but finds no instrumentation, the card is still emitted with "None found" sections (mirrors Wave 1.5 `doc_context_card_path` discipline). |
| `diagnosability_tasklist_path` | `string \| null` | `null` | **Repo-relative** path to `<output-dir>/diagnosability-tasklist.md`. Populated when verdict ∈ {`partial`, `insufficient`} AND tasklist was emitted (hard-stop OR soft-warn case). `null` for `sufficient` / `unknown` / `skipped`. |
| `diagnosability_hard_stop` | `bool` | `false` | `true` when Wave 1.6 fired the hard-stop and skipped Waves 1.7-4. Downstream consumers use this to distinguish "ran to completion" from "stopped early for instrumentation." Mutually informative with existing `status: partial`. |

**No `status` enum extension** (debate Axis 3): the `status` field retains its existing values (`success | partial | failed`). Hard-stop cases set `status: partial` with `diagnosability_hard_stop: true` — consumers learn the precise reason from the boolean without needing to recognize a new enum value.

**Backwards-compat statement**: downstream consumers (Tier 3 task-builder, fleet auto-apply wrappers, telemetry) reading only the existing 13 fields are **unaffected**. They see `null` / `"unknown"` / `false` defaults in the new fields. Consumers that want to gate on the hard-stop opt in by reading `diagnosability_hard_stop`.

---

## 6. Tasklist Artifact Format

<!-- Source: Variant 3 (base) — high-specificity per-line, full worked example; with V4 hard constraints -->

**Position on Open Question #3**: tasklist lives at `<output-dir>/diagnosability-tasklist.md` (standalone, always) AND an opt-in `--diagnosability-handoff` flag invokes `task-builder` against the tasklist for MDTM packaging (debate Axis 5 verdict).

**Position on Open Question #8**: high-specificity per-line. Each task names exact file:line, framework, level, fields, current code, and add-this snippet. Achievable because Wave 1.6 has Branch A's line-numbered inventory.

### HARD CONSTRAINTS (variant-4 §5 R2 additive — non-negotiable)

**Constraint 1 — Invocation-site-only**: Every task MUST target an invocation site (test script, CI workflow YAML, dev harness, container entrypoint, dev-mode config override), NEVER the failing component's own source code. Diagnostic code in production source leaks into release artifacts.

**Constraint 2 — Additive only**: Every task is a pure ADD (or a config-override at an invocation site). No task modifies existing source logic. Tasks that would otherwise modify source are re-framed as config-overrides (`LOG_LEVEL=DEBUG` env var, `--debug` flag at invocation, structured-log filter relaxation in test config).

**Constraint 3 — Reversible**: Every task has a Rollback line describing how to revert post-defect-closure.

**Constraint 4 — Revert annotation**: Patches added by the tasklist carry the comment `# Diagnosability-tasklist instrumentation: revert after defect closed.` so cleanup is mechanizable.

### Worked tasklist example (`diagnosability-tasklist.md`)

```markdown
# Diagnosability Tasklist

**Generated**: 2026-05-29T14:32:00Z
**Wave**: 1.6
**Issue**: Worker occasionally hangs during batch processing
**Verdict**: insufficient
**Complexity**: non-trivial (score=3: intermittent keyword + performance type + multi-module scope)
**failing_component**: src/worker/processor.py
**Round**: 1 of 3

## Hard Constraints

- All tasks target INVOCATION SITES (test scripts, CI YAML, dev harnesses), not production source.
- All changes are ADDITIVE (or config-overrides at invocation sites).
- Each task is annotated `# Diagnosability-tasklist instrumentation: revert after defect closed.`

## Implementation tasks

### Task 1: Enable DEBUG log level at the test invocation site

- **Invocation site**: `tests/integration/test_worker.py:18` (the `subprocess.run([...])` that launches the worker)
- **Current**: `subprocess.run(["python", "-m", "worker", ...])`
- **Add env override**: `subprocess.run(["python", "-m", "worker", ...], env={**os.environ, "LOG_LEVEL": "DEBUG"})  # Diagnosability-tasklist instrumentation: revert after defect closed.`
- **Rationale**: Unblocks visibility into worker.py's existing DEBUG calls without modifying worker.py. If no DEBUG calls exist, Task 2 adds them.

### Task 2: Add request-correlation logging via test fixture (NOT in worker.py source)

- **Invocation site**: `tests/integration/conftest.py:45` (the `worker_runner` fixture)
- **Add fixture wrapper**:
  ```python
  @pytest.fixture
  def worker_runner_with_tracing(worker_runner):
      # Diagnosability-tasklist instrumentation: revert after defect closed.
      import logging
      handler = logging.FileHandler("worker_trace.log")
      handler.setFormatter(logging.Formatter("%(asctime)s %(threadName)s %(name)s %(levelname)s %(message)s"))
      logging.getLogger("worker").addHandler(handler)
      logging.getLogger("worker").setLevel(logging.DEBUG)
      yield worker_runner
      logging.getLogger("worker").removeHandler(handler)
  ```
- **Rationale**: Captures every existing logger call in `worker` package with timestamp + thread name (resolves the "when" W). No source change.

### Task 3: Run with strace to capture syscall-level evidence (invocation-site only)

- **Invocation site**: `tests/integration/test_worker.py:18`
- **Wrap subprocess.run**: `subprocess.run(["strace", "-f", "-e", "trace=read,write,futex", "-o", "worker_strace.log", "python", "-m", "worker", ...])  # Diagnosability-tasklist instrumentation: revert after defect closed.`
- **Rationale**: Hangs at the IPC/futex layer become visible via syscall trace. Resolves "where" when worker.py-level logging is silent. (Linux only — skip on non-Linux CI.)

### Task 4: Capture queue-depth telemetry via Sentry breadcrumb at invocation

- **Invocation site**: `tests/integration/conftest.py:80` (already initializes Sentry for test mode)
- **Add breadcrumb hook**:
  ```python
  # Diagnosability-tasklist instrumentation: revert after defect closed.
  import sentry_sdk
  sentry_sdk.set_context("queue_state", {"depth_at_start": q.qsize()})
  ```
- **Rationale**: If the process is killed mid-hang, Sentry's last breadcrumb shows queue state. Complements file-based logs which may not be flushed.

### Task 5: Add CI artifact upload for trace files

- **Invocation site**: `.github/workflows/integration-tests.yml:42`
- **Add step after test run**:
  ```yaml
  - name: Upload diagnosability traces
    if: failure()
    uses: actions/upload-artifact@v4
    with:
      name: diagnosability-traces
      path: |
        worker_trace.log
        worker_strace.log
    # Diagnosability-tasklist instrumentation: revert after defect closed.
  ```
- **Rationale**: Trace files are useless if CI discards them on failure.

## Verification

After implementing all 5 tasks:

1. Run the integration test that produces the symptom: `pytest tests/integration/test_worker.py::test_batch_hang`
2. On failure, verify `worker_trace.log` contains timestamped, thread-named entries
3. Verify `worker_strace.log` shows the hung syscall
4. Verify CI upload step produces the `diagnosability-traces` artifact
5. Re-run `/sc:troubleshoot` with the trace excerpts in the issue description. Expected: `diagnosability_verdict: sufficient` (or `partial` if config gaps remain).

## Rollback

If instrumentation introduces overhead or alters timing such that the bug no longer reproduces (Heisenbug — variant-4 §5 R3):

1. Drop Task 3 first (strace adds most overhead).
2. If still not reproducing, drop Task 2's `logging.DEBUG` (some race conditions are sensitive to log-write latency).
3. Retain Task 1 (env var only — minimum perturbation).
4. Record the Heisenbug finding in the issue description for the next `/sc:troubleshoot` run; Wave 1.6 will downgrade the next-round tasklist to env-vars-only.
5. If Round counter reaches 3 without sufficient evidence: escalate to structural change (see Off-Ramp UX §7).

## Patch-round counter

This is Round **1 of 3** for issue `worker-occasional-hang-20260529`.
```

---

## 7. Off-Ramp UX

<!-- Source: Variant 3 base + V1 `--no-escalate` framing + V4 temporal-discipline rhetoric + V4 3-round cap -->

### Hard-stop chat message (verdict=insufficient + non-trivial + NOT --no-escalate)

```
Wave 1.6 Diagnosability Audit — HALT

The reported symptom looks non-trivial (signals: <list>), and the existing instrumentation around
<failing_component> is insufficient to triangulate it: <1-line specific gap, e.g. "no thread-correlation
fields in any log call within the suspect function; intermittent symptom requires when/why traceability">.

Hypothesizing harder against blind code at this point produces low-confidence answers. The protocol will
halt the deep-debugging pipeline and emit an instrumentation tasklist instead. No hypothesis work happens
in the same turn as the instrumentation patch — once you've implemented the tasklist and re-run, the
re-entry starts fresh with new evidence.

  Diagnosability Context Card:  <abs path>
  Instrumentation Tasklist:     <abs path>
  Diagnostic REPORT.md:         <abs path>
  Round:                        1 of 3

Next steps:
  1. Review the tasklist and instrument the invocation sites (NOT the failing component's source):
       /task <tasklist-path>
       (or implement manually; tasks target test scripts / CI / dev harnesses only)
  2. Re-run the workload with the new instrumentation.
  3. Re-run /sc:troubleshoot with the fresh log/trace excerpts in the issue description.

  To override and proceed with deep debugging anyway:
       /sc:troubleshoot --no-diagnosability-audit <original args>
  (Bypass will be logged in the REPORT.md header for post-mortem auditability.)

  To package the tasklist as an MDTM task via task-builder:
       /sc:troubleshoot <original args> --diagnosability-handoff
```

### 3-round-cap escalation message (variant-4 §3.7 additive)

When the per-defect counter reaches 3 hard-stops for the same `issue_slug`:

```
Wave 1.6 Diagnosability Audit — 3-Round Cap Reached

This defect (issue: <issue_slug>) has reached the 3-round diagnosability cap. The symptom does not appear
observable through cheap log additions. Three tasklists have been emitted; the latest fresh evidence is
still insufficient.

This usually means one of:
  - The bug lives in a layer that won't surface via logging (e.g., kernel-side IO, container-runtime,
    proprietary binary dependency).
  - The component needs a structural change for testability (refactor for dependency injection,
    add a dedicated diagnostic mode, expose internal state).
  - A debugger session (gdb, lldb, py-spy, perf) is the right next tool, not more logging.

Wave 1.6 will not emit another tasklist for this issue without an explicit reset:
       /sc:troubleshoot --reset-diagnosability-rounds <original args>

Alternative paths:
  - Proceed with deep debugging despite insufficient evidence:
       /sc:troubleshoot --no-diagnosability-audit <original args>
  - Escalate to a debugger / profiler session externally.

Diagnosability Context Card (latest): <abs path>
Previous tasklists: <list of 3 paths>
```

### Soft-warn (verdict=insufficient + trivial, OR verdict=partial + any complexity, OR --no-escalate)

REPORT.md gains a `## Diagnosability Context` section (always rendered when Wave 1.6 ran) between Documentation Context and Diagnosis:

```markdown
## Diagnosability Context

**Verdict**: <verdict>
**Complexity classification**: <complexity>
**Captured-bytes (failing run)**: <bytes-or-n/a>

<≤6-line summary of the Diagnosability Context Card. Names the existing instrumentation in 1 line, names the gap in 1 line, names the implication for diagnosis confidence in 1 line.>

(Full card: <abs path to diagnosability-context.md>)
(Tasklist (informational): <abs path to diagnosability-tasklist.md>, if emitted)
```

### `--depth deep` banner (variant-1 + Round-2 compromise)

When `--depth deep` AND `verdict ∈ {insufficient, partial}`, REPORT.md gains a top-of-report banner above the Summary section:

```markdown
> ⚠ **Diagnosability Caveat**: Your hypothesis depth was constrained by insufficient evidence. See
> Diagnosability Context section below. Consider implementing the suggested instrumentation tasklist
> and re-running to get higher-confidence answers.
```

### `--no-diagnosability-audit` bypass header (variant-4 §6 R5)

When `--no-diagnosability-audit` was set, REPORT.md's header gains a line:

```markdown
**Diagnosability audit**: SKIPPED (--no-diagnosability-audit, user-bypassed)
```

And the Grounding Gaps section gains: `Diagnosability audit skipped by --no-diagnosability-audit — diagnosis confidence is not weighted against existing logging coverage.`

### Flag interactions (summary)

| Flag | Interaction with hard-stop |
|------|----------------------------|
| `--no-diagnosability-audit` | Skips Wave 1.6 entirely; emits `verdict: unknown`; logs the bypass in REPORT.md header. |
| `--no-escalate` | Suppresses the hard-stop. Tasklist still emitted (soft-warn). Wave 1.7 runs as usual. |
| `--depth deep` | Does NOT force hard-stop. Soft-warn becomes mandatory & prominent (banner). |
| `--diagnosability-handoff` | Opt-in: after Wave 1.6 emits the tasklist, invokes `task-builder` against it for MDTM packaging. Default off. |
| `--reset-diagnosability-rounds` | Resets the per-defect counter to 0 for the current `issue_slug`. Use after a structural change has been made. |
| `--type security` | Always non-trivial. Wave 1.6 verdict applied as normal; security-class issues are eligible for hard-stop. |

---

## 8. Risk Register

<!-- Source: Variant 3 + V4 additives (Heisenbug, opaque-component) + V1 R2 (gate misfire) -->

| # | Risk | Likelihood | Impact | Mitigation |
|---|------|------------|--------|------------|
| R1 | **Query coverage gaps** — auggie misses non-obvious logger patterns (custom decorators, aliased loggers, AOP-style injection) | Medium | False `insufficient` verdict; unnecessary hard-stop | Branch A query includes "and any decorator or wrapper that injects logging"; Glob/Grep fallback explicitly lists alias patterns; `degraded: true` caps verdict at `partial` (not `insufficient`) when fallback is used |
| R2 | **Log-config environment drift** — Branch B finds `LOG_LEVEL=DEBUG` in `.env` but production runs `LOG_LEVEL=WARNING` | Medium | False `sufficient` verdict in dev-only audits | Branch B explicitly searches env-specific configs (Dockerfile, docker-compose, CI YAML, .env*); card reports level per environment; `unknown` is the conservative default when env-specific config can't be resolved |
| R3 | **Tasklist staleness on re-run** — user instruments, re-runs months later, intervening refactors moved the lines | Low-medium | Tasklist targets moved/renamed code | File:line targets validated at re-run entry via lightweight Read check; stale targets dropped with a notice; the 3-round counter is keyed by `issue_slug` so cross-session continuity is preserved |
| R4 | **Complexity-gate misfires on borderline issues** (variant-1 R2) — e.g., a NameError that's actually a symptom of an import-order race | Medium | Soft-warn proceeds to Wave 1.7 against blind code; low-confidence hypothesis emerges | Wave 2's confidence gate is the safety net — low-confidence hypothesis triggers Tier 2; users can force-escalate via `--depth deep` (mandatory soft-warn banner appears) |
| R5 | **Heisenbug — instrumentation alters timing** (variant-4 §5 R3) | Low-medium | Bug stops reproducing under instrumentation | Record as Heisenbug finding in audit card; downgrade next-round tasklist to env-vars-only (no `--debug` flag changes, no log-level overrides); after 3 rounds, escalate via cap message |
| R6 | **Opaque-component degradation** (shared-assumption A-001 from diff analysis) — failing component is closed-source, managed cloud service, or behind opaque RPC | Low (per typical SuperClaude usage) | Audit returns `unknown`; no actionable tasklist | Card explicitly states "component is not inspectable; consider proxying via observability at the call boundary"; Wave 1.7 proceeds normally with reduced confidence |
| R7 | **Tasklist diagnostic code leakage** — without invocation-site-only discipline, dev `logger.debug` lines could merge into production source (variant-4 R2) | Low (now structurally prevented) | Production source carries diagnostic noise | HARD CONSTRAINT in tasklist format: invocation-site-only. CI pre-merge hook (out of v1 scope but recommended for v1.1) greps for the `# Diagnosability-tasklist instrumentation:` marker. |

---

## 9. Ref-File Changes

<!-- Source: Variant 3 + V1 hypothesis-card-template addition + V4 T4 worked example -->

### New ref: `src/superclaude/skills/sc-troubleshoot-protocol/refs/diagnosability-audit.md`

Lazy-loaded by Wave 1.6 only. Sections:

1. **Section 1** — Auggie query templates per branch (Branch A log-call, Branch B log-config). Verbatim strings with `<failing_component>`, `<scope>`, `<symptom>` placeholders.
2. **Section 2** — Fallback paths (Glob/Grep commands per branch for when auggie is unavailable).
3. **Section 3** — Structured-output schemas per branch (JSON examples for Branch A and Branch B).
4. **Section 4** — Sufficiency rubric (the S1-S13 table from §3 of this spec) + 3-W's synthesis procedure.
5. **Section 5** — Complexity gate (the 6-signal table from §4 of this spec + classification rule).
6. **Section 6** — Diagnosability Context Card template (markdown skeleton).
7. **Section 7** — Tasklist generation rules + hard constraints + worked example skeleton.
8. **Section 8** — T4 worked example (variant-4 §4 verbatim) — canonical illustration of what the audit saves.

### Modified ref: `refs/hypothesis-card-template.md`

Append one line under `## Grounding gaps`:

```markdown
If Wave 1.6 emitted a Diagnosability Context Card with `verdict ∈ {partial, insufficient}`, reference it
here (e.g., "Diagnosability verdict: partial — see <card-path>; coverage of 'why' is missing, so this
hypothesis cannot be falsified at runtime without the proposed instrumentation").
```

### Modified ref: `refs/report-template.md`

Add `## Diagnosability Context` section template (rendered between Documentation Context and Diagnosis) + `Next Steps` variant for the hard-stop case + the `--depth deep` banner template.

### Modified ref: `refs/escalation-rubric.md`

Append short section `## Diagnosability interaction` (≤15 lines) documenting that Wave 1.6's complexity gate reuses this rubric's structural dimensions but does NOT consume the calibrated confidence (which fires after Wave 1.7). Forward reference; no new behavioral rule.

### Unchanged refs: `refs/triage-checklist.md`, `refs/doc-discovery.md`, `refs/remediation-handoff.md`, `refs/calibrator-eval-cases.md`.

---

## 10. SKILL.md Diff Sketch

<!-- Source: Variant 1's structured table (better fidelity than V3's prose) + V3's contract fields substituted -->

| Section | Current line range | Change |
|---------|-------------------|--------|
| Wave Structure ASCII | 75-85 | Insert `Wave 1.6: Diagnosability Audit ← always; loads refs/diagnosability-audit.md on demand; skipped only by --no-diagnosability-audit; may hard-stop to Wave 5` between current Wave 1.5 and Wave 1.7 lines. Add the hard-stop edge note: `Wave 1.6 hard-stop edge: → Wave 5 (skip Waves 1.7-4); sets diagnosability_hard_stop=true and status=partial`. |
| Output Contract table | 41-57 | Add 4 new rows: `diagnosability_verdict`, `diagnosability_context_card_path`, `diagnosability_tasklist_path`, `diagnosability_hard_stop`. **No change to `status` field enum**. |
| Wave 0: Parse + Validate Input | 91-126 | Add to optional flags: `--no-diagnosability-audit`, `--diagnosability-handoff`, `--reset-diagnosability-rounds`. |
| New section: `### Wave 1.6: Diagnosability Audit` | insert after current line 187 (end of Wave 1.5 section) | New ~70-line section per §1 of this spec (Preconditions, Steps S1.6.0-S1.6.4, Exit criteria, Failure handling, Token budget). |
| Wave 1.7 Preconditions | 194-196 | Add: `Wave 1.6 did NOT fire its hard-stop (or was skipped via --no-diagnosability-audit, or fired soft-warn under --no-escalate). When Wave 1.6 hard-stopped, this wave is skipped entirely.` |
| Wave 5 step 2 (REPORT.md composition) | 331-342 | Add `Diagnosability Context` to the list of sections to compose (after `Documentation Context`, before `Diagnosis`). Add the hard-stop rendering path: when `diagnosability_hard_stop=true`, replace the Diagnosis section with a "Halted — instrumentation required" prose block referencing the tasklist. Add the `--depth deep` mandatory-banner rendering. |
| Tool Coordination Summary | 391-403 | Add Wave 1.6 column or annotate the Tier 1 column. `mcp__auggie__codebase-retrieval` ✓ (2 branches: A logger-call, B log-config); `Glob`/`Grep` ✓ (fallback); `Task` ✓ (2 parallel branches + 1 orchestrator synthesis). |
| Will Do / Will Not Do | 404-425 | **Will Do** additions: "Run Wave 1.6 Diagnosability Audit by default; opt-out via `--no-diagnosability-audit` (bypass is logged). Halt Waves 1.7-4 when verdict=`insufficient` AND complexity=`non-trivial` AND `--no-escalate` is not set. No hypothesis work happens in the same turn as an instrumentation patch — the user re-runs after instrumenting." **Will Not Do** additions: "Auto-apply the diagnosability tasklist (it is a proposal). Force the hard-stop when `--no-escalate` is set. Allow the tasklist to target the failing component's own source — invocation sites only." |
| Token Cost Profile | 446-454 | Add Wave 1.6 row: `+1-2k auggie, +1-2.5k Claude, +30-60s wall clock`. Hard-stop case yields a net token *saving* vs the full Tier 2 path. |
| Error Handling | 428-444 | Add 6 new rows: `--no-diagnosability-audit set` (skip wave, verdict unknown, logged); auggie unavailable (Glob/Grep fallback, cap verdict at `partial`); both branches return empty (verdict insufficient if non-trivial, partial if trivial); failing_component not localizable (verdict unknown, Grounding Gaps line); Heisenbug detected on re-run (downgrade next tasklist to env-vars-only); 3-round cap reached (emit cap message, refuse next tasklist). |
| Refs table | 458-466 | Add row: `refs/diagnosability-audit.md` — `Wave 1.6 (audit query templates, fallback paths, sufficiency rubric, complexity gate, context card template, tasklist rules, T4 worked example)`. |

---

## 11. Persona-distinctive claims preserved from the debate

These are positions that survived the adversarial debate and are now part of the merged spec's defended posture:

1. **Two branches, not three** (V3 base — Axis 1). Branch F (symptom-coverage) is folded into orchestrator synthesis because it's pure synthesis, not retrieval.
2. **Quaternary verdict, not binary** (V1+V3 vs V4). Variant-4's binary was reframed; `partial` and `unknown` are load-bearing for the soft-warn and degraded-discovery cases.
3. **Reuse the escalation rubric for complexity** (V1+V3 vs Open Question #1 alternatives). One classification surface; signals are extractable pre-hypothesis.
4. **Invocation-site-only instrumentation is non-negotiable** (V4 — Change 7). Hard constraint in the tasklist format.
5. **3-round patch-loop cap** (V4 — Change 8). Closes Open Question #6; prevents infinite iteration.
6. **No hypothesis work in the same turn as an instrumentation patch** (V4 — Change 12). Load-bearing temporal rule; preserved in the hard-stop chat message.
7. **`--depth deep` does NOT force hard-stop, but soft-warn under deep is mandatory** (V1 + Round-2 compromise — Axis 4). Threads the orthogonality argument against the deep-wrong-answer failure mode.
8. **`--no-escalate` SHOULD suppress hard-stop** (V1 — Change 3). Preserves opt-out symmetry.
9. **Tasklist standalone + opt-in `--diagnosability-handoff`** (V3 — Axis 5). Additive flag; default unchanged.
10. **High-specificity per-line tasklist** (V3 unique contribution U-001). File:line + framework + current code + add-this + rationale + verification + rollback.

---

## 12. Out of scope for v1 (tracked for v1.1)

- Broader audit scope beyond logging: CLI debug flags + OS introspection + doctor commands (variant-4 §2). User maintained narrow scope per Option A.
- Pre-Wave-1 placement (true "Phase 0" position before grounding). Wave 1.6 remains between 1.5 and 1.7.
- Generalization to a shared `epistemic-sufficiency-gate` skill for `sc:analyze`, `sc:reflect` UC-2, `sc:auggie-review` (variant-4 §8).
- CI pre-merge hook for `# Diagnosability-tasklist instrumentation:` marker (R7 mitigation).
- Tasklist file:line freshness validation at re-run entry (R3 mitigation — implementation deferred).

---

## Appendix — How the original 8 Open Questions resolved

1. **Complexity gate signal source** → Reuse escalation rubric (Option A). All 3 variants converged.
2. **Audit branch shape** → 2 branches (V3 won debate Axis 1).
3. **Where tasklist lives** → Standalone artifact + opt-in `--diagnosability-handoff` (V3 won debate Axis 5).
4. **Interaction with `--depth deep`** → Does NOT force hard-stop, BUT mandatory soft-warn banner (V1 + Round-2 compromise).
5. **Interaction with `--no-escalate`** → Suppresses hard-stop (V1+V3 convergence).
6. **Re-run loop UX** → 3-round patch-loop cap (variant-4 §3.7 additive).
7. **Cause-class coupling** → Rubric does NOT short-circuit on cause class. Stack-trace-self-documents (S1) and intermittent-with-no-trace (S13) are the only short-circuits; both are derivable from symptom shape, not cause class hypothesis.
8. **Tasklist actionability bar** → High-specificity per-line, with hard constraint that targets are invocation sites only (V3 + variant-4 R2).

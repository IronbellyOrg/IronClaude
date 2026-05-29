# Variant 3 -- Devops Perspective

## Design Position

Wave 1.6 should be a **two-branch parallel audit** (log-call inspection + log-config inspection) with exception-handler richness treated as a **piggyback signal** inside the log-call branch, not a separate fan-out. This keeps Claude-token cost under 2k while still covering the three audit surfaces the seed brief names. The third branch (exception-handler-only) adds marginal coverage at disproportionate token cost because the same auggie query that finds `logger.*` calls will also surface `except:`/`catch` blocks when the query text includes "exception handling" alongside the symptom.

The tasklist artifact should live at **`<output-dir>/diagnosability-tasklist.md`** as a standalone file AND be available for `--diagnosability-handoff` packaging into a `task-builder` BUILD_REQUEST. Standalone-first because the user may want to read and triage the tasks before committing to `/task` execution; handoff-second because the Tier 3 pattern already uses `task-builder` for fix application and the same machinery should be reusable for instrumentation.

Actionability bar for the tasklist: **high-specificity per-line**. Each task names the exact file:line, the log level, the suggested fields, and the local variables to include. "Add more logging" is useless. "Add `logger.info("loop_iter", attempt=i, latency_ms=elapsed)` at `worker.py:142`" is implementable by someone who has never seen the codebase.

## Wave 1.6 Placement & Entry/Exit Criteria

**Placement**: Insert between Wave 1.5 (Documentation Grounding) and Wave 1.7 (Hypothesis Formation). The wave graph becomes:

```text
Wave 0: Parse + Validate Input
Wave 1: Tier 1 -- Real-Code Grounding
Wave 1.5: Documentation Grounding
Wave 1.6: Diagnosability Audit        <-- NEW; loads refs/diagnosability-audit.md on demand
Wave 1.7: Tier 1 -- Hypothesis Formation
Wave 2: Confidence Gate
Wave 3: Tier 2 -- Parallel Hypotheses (conditional)
Wave 4: Tier 2 -- Adversarial Fix Debate (conditional)
Wave 5: Synthesis + Report
Wave 6: Tier 3 -- Remediation Chain (conditional)
```

**Entry criteria**:

- Wave 1.5 has completed (or was skipped via `--no-doc-discovery`).
- `--no-diagnosability-audit` is NOT set.
- Wave 1 has localized at least one `<component_path>` or `<scope>` -- the audit needs a code surface to inspect.

**Exit criteria**:

- Two branch outputs written to disk at `<output-dir>/wave1_6-branch-<A|B>.md`.
- One Diagnosability Context Card written to `<output-dir>/diagnosability-context.md`.
- If verdict is `insufficient` AND issue complexity is `non-trivial`: `<output-dir>/diagnosability-tasklist.md` written; hard-stop fires; Waves 1.7-5 are skipped; Wave 5 is invoked directly with `tier_reached=1` and a special report variant.
- If verdict is `insufficient` AND issue complexity is `trivial`: tasklist written as a soft-warn; proceed to Wave 1.7.
- If verdict is `sufficient` or `partial`: proceed to Wave 1.7; surface findings in REPORT.md's new Diagnosability Context section.
- Emit "Wave 1.6 complete: verdict=<sufficient|partial|insufficient|unknown>".

**Failure handling**:

| Scenario | Behavior | Fallback |
|----------|----------|----------|
| `--no-diagnosability-audit` set | Skip entire wave; emit `diagnosability_verdict: unknown`; no card written | None |
| Auggie unavailable for both branches | Fall back to `Grep`/`Glob` per branch targets; mark `degraded: true`; verdict capped at `partial` max | None |
| Both branches return empty (no log calls, no log config) | Verdict `insufficient` if issue is non-trivial; `partial` if trivial; emit tasklist accordingly | None |
| Branch synthesis times out / one branch crashes | Continue with surviving branch; mark missing branch as "Branch <X> failed" in context card; verdict downgraded one notch | None |
| Symptom site not localizable (Wave 1 found no component paths) | Verdict `unknown`; emit Grounding Gaps entry; proceed to Wave 1.7 | None |

## Audit Mechanics

### Branch structure: 2-branch parallel fan-out

**Branch A -- Log-Call Inspection**: Find every logging/print/exception-handler call site near the symptom code. This branch also inspects exception-handler richness (the would-be 3rd branch) because the same auggie query captures both.

**Branch B -- Log-Config Inspection**: Find every log configuration file, environment variable, and structured-log filter that governs what actually reaches the console/file at runtime. A logger call that is filtered out by config is indistinguishable from no logger call.

**Rationale for 2 vs 3 branches**: Exception-handler richness is not an orthogonal surface -- it is a subset of "what produces diagnostic signal at runtime." The auggie query for Branch A captures both `logger.exception()` and bare `except: pass` in a single retrieval because the query explicitly names both patterns. A separate branch would duplicate the code-surface scan at additional Claude-token cost. Log config, by contrast, lives in entirely different files (YAML, XML, JS config, env vars) and requires a different retrieval strategy -- hence its own branch.

### Branch A -- Log-Call Inspection

**Auggie query string**:

```
In the codebase at <scope> (or restricted to <component_paths> if scope is broader), find every location that produces diagnostic signal around the behavior described as: <symptom>. This includes:

1. Python: logging module calls (logging.debug/info/warning/error/exception/critical), loguru calls (logger.debug/info/warning/error/critical/exception), print() statements, and structlog calls (logger.info/msg).

2. JavaScript/TypeScript: console.log/warn/error/debug/info, winston logger calls (logger.info/warn/error/debug), pino calls (log.info/warn/error/debug), bunyan calls (log.info/warn/error/debug).

3. Java: SLF4J/Logback calls (log.info/warn/error/debug/trace), Log4j2 calls (logger.info/warn/error/debug/trace), java.util.logging calls (logger.info/warning/severe).

4. Exception handlers: try/except blocks (Python), try/catch blocks (JS/Java), and for each handler, whether it logs the exception (logger.exception, console.error with stack, log.error with exception parameter) or silently swallows it (bare except/pass, catch(e) {}, empty catch block).

5. Error-reporter initializations: Sentry.init(), Datadog.init(), rollbar.configure(), or equivalent -- any SDK that ships errors to an external observability service.

For each hit, return: the file path, the line number, the call type (logger_call | print | exception_handler | error_reporter_init), the framework (logging | loguru | console | winston | pino | bunyan | slf4j | log4j2 | jul | sentry | datadog), the log level, and the 1-2 line snippet showing the call. For exception handlers, also include a richness score: rich (logs exception with stack/context), minimal (logs message only), or silent (no log at all).
```

**Fallback path (when auggie unavailable)**:

```bash
# Python logger calls
grep -rn 'logging\.\(debug\|info\|warning\|error\|exception\|critical\)\|logger\.\(debug\|info\|warning\|error\|exception\|critical\)\|from loguru import\|logger\.\(debug\|info\|warning\|error\|critical\|exception\)' <scope>
# Python print statements
grep -rn 'print(' <scope>
# JS console calls
grep -rn 'console\.\(log\|warn\|error\|debug\|info\)' <scope>
# JS winston/pino/bunyan
grep -rn 'logger\.\(info\|warn\|error\|debug\)\|log\.\(info\|warn\|error\|debug\)' <scope>
# Java logger calls
grep -rn 'log\.\(info\|warn\|error\|debug\|trace\)\|logger\.\(info\|warn\|error\|debug\|trace\)' <scope>
# Exception handlers (Python bare except)
grep -rn 'except\s*:' <scope>
# Exception handlers (JS empty catch)
grep -rn 'catch.*{.*}' <scope>
# Sentry/Datadog init
grep -rn 'Sentry\.init\|Datadog\.init\|rollbar\.config' <scope>
```

**Structured per-branch output schema**:

```json
{
  "branch": "A",
  "query_target": "<scope or component_paths>",
  "hits": [
    {
      "file_path": "/absolute/path/to/worker.py",
      "line": 142,
      "call_type": "logger_call",
      "framework": "logging",
      "level": "info",
      "snippet": "logger.info(\"task_started\", task_id=task.id)",
      "richness": "rich",
      "distance_to_symptom": "in_function"
    },
    {
      "file_path": "/absolute/path/to/worker.py",
      "line": 198,
      "call_type": "exception_handler",
      "framework": "python",
      "level": null,
      "snippet": "except Exception:\n    pass",
      "richness": "silent",
      "distance_to_symptom": "in_function"
    },
    {
      "file_path": "/absolute/path/src/sentry_init.py",
      "line": 12,
      "call_type": "error_reporter_init",
      "framework": "sentry",
      "level": null,
      "snippet": "sentry_sdk.init(dsn=os.environ[\"SENTRY_DSN\"])",
      "richness": null,
      "distance_to_symptom": "cross_module"
    }
  ],
  "degraded": false
}
```

On no-hit, the branch emits: `{ "branch": "A", "hits": [], "degraded": false }`.

### Branch B -- Log-Config Inspection

**Auggie query string**:

```
In the entire repository, find every configuration file or environment-variable reference that controls logging behavior, log levels, or structured-log output. Specifically look for:

1. Python logging config files: logging.yaml, logging.yml, logging.conf, logging.ini, log_config.py, log_config.json, and [tool.logging] or [tool.pytest.ini_options].log sections in pyproject.toml.

2. Java logging config files: log4j2.xml, log4j2.properties, logback.xml, logback-spring.xml, logging.properties, and any Spring Boot application.properties or application.yml with logging.* keys.

3. JavaScript/Node.js config: winston configuration files (winston.config.js, logger.js, config/logger.js), pino transport config in package.json or separate config files, .env files containing LOG_LEVEL, DEBUG, or NODE_ENV.

4. Environment variables: any reference to LOG_LEVEL, LOGLEVEL, LOG_LEVEL_ROOT, PYTHON_LOG_LEVEL, DEBUG, NODE_ENV=production, LOG_FORMAT=json, or similar log-level/format env vars in Dockerfile, docker-compose.yml, .env*, Makefile, or CI pipeline files (.github/workflows/*.yml, .gitlab-ci.yml).

5. Structured-log filter/rate-limit config: any log-filter middleware, rate-limiter config for logs, or sampling configuration that would suppress log output.

For each hit, return: the file path, the config type (file | env_var | pipeline_config), the framework it configures, the effective log level if discernible (DEBUG, INFO, WARN, ERROR, or unknown), and the 1-3 line snippet showing the config.
```

**Fallback path (when auggie unavailable)**:

```bash
# Log config files
find . -name 'logging.yaml' -o -name 'logging.yml' -o -name 'logging.conf' -o -name 'logging.ini' -o -name 'log4j2.xml' -o -name 'logback*.xml' -o -name 'winston*.js' -o -name 'logger.js' -o -name 'log_config.*' 2>/dev/null
# pyproject.toml logging sections
grep -n '\[tool\.logging\]\|\[tool\.pytest\.ini_options\].*log' pyproject.toml
# Spring Boot configs
find . -name 'application*.properties' -o -name 'application*.yml' -o -name 'application*.yaml' 2>/dev/null
# Environment variables
grep -rn 'LOG_LEVEL\|LOGLEVEL\|DEBUG\s*=\|NODE_ENV\|LOG_FORMAT' .env* Dockerfile docker-compose.yml Makefile .github/workflows/*.yml .gitlab-ci.yml 2>/dev/null
# Sentry/Datadog config files
find . -name 'sentry*.config.*' -o -name 'datadog*.yaml' 2>/dev/null
```

**Structured per-branch output schema**:

```json
{
  "branch": "B",
  "hits": [
    {
      "file_path": "/absolute/path/to/logging.yaml",
      "config_type": "file",
      "framework": "logging",
      "effective_level": "WARNING",
      "snippet": "root:\n  level: WARNING\n  handlers: [console]",
      "location": "repo_root"
    },
    {
      "file_path": "/absolute/path/to/.env",
      "config_type": "env_var",
      "framework": "generic",
      "effective_level": "DEBUG",
      "snippet": "LOG_LEVEL=DEBUG",
      "location": "repo_root"
    },
    {
      "file_path": "/absolute/path/to/docker-compose.yml",
      "config_type": "pipeline_config",
      "framework": "generic",
      "effective_level": "unknown",
      "snippet": "      - LOG_LEVEL=${LOG_LEVEL:-INFO}",
      "location": "repo_root"
    }
  ],
  "degraded": false
}
```

On no-hit, the branch emits: `{ "branch": "B", "hits": [], "degraded": false }`.

### Diagnosability Context Card template

After both branches complete, the Wave 1.6 orchestrator synthesizes a single card at `<output-dir>/diagnosability-context.md`:

```markdown
# Diagnosability Context Card

**Generated**: <ISO 8601>
**Wave**: 1.6
**Scope**: <scope or "(none)">

## Log-call coverage

Summary of Branch A findings:

- Total logger/print calls found: <N>
- Calls within symptom function/module: <N>
- Calls at ERROR level or above: <N>
- Silent exception handlers found: <N>
- Error-reporter SDKs detected: <list or "None">
- Coverage assessment: <dense | sparse | absent>

## Log-config state

Summary of Branch B findings:

- Config files found: <list of paths or "None">
- Effective log level at symptom site: <level or "unknown">
- Level vs symptom severity: <level_would_capture | level_would_suppress | unknown>
- Structured-log format: <json | key_value | plain_text | none>

## Sufficiency verdict

- Verdict: <sufficient | partial | insufficient | unknown>
- Reason: <one-line rationale tied to the sufficiency rubric>
- Tasklist emitted: <yes | no>

## Re-frame signals

- "The symptom is a NameError with a clear stack trace -- existing log coverage is irrelevant because the exception IS the signal." (sufficient case)
- "The symptom is an intermittent race condition; all log calls within the suspect function are at INFO level with no request_id or correlation fields -- insufficient to correlate events across threads." (insufficient case)
- "Branch B found the effective log level is WARNING but the symptom would only produce INFO-level output; logs are configured to suppress the signal." (partial case)
```

## Sufficiency Rubric

The verdict is computed from these signals, applied in order:

| Signal | sufficient | partial | insufficient |
|--------|-----------|---------|-------------|
| **Symptom is a deterministic exception with a clear stack trace** | Always sufficient -- the stack trace IS the diagnostic signal | -- | -- |
| **Symptom is a build/compile error** | Always sufficient -- the compiler output IS the signal | -- | -- |
| **Logger calls within symptom function: >= 3 at DEBUG/INFO + exception handler logs with stack** | sufficient if config level would capture them | partial if config level is higher | insufficient if no logger calls exist |
| **Logger calls: 1-2 at INFO, no exception-handler logging** | -- | partial | insufficient if symptom is intermittent |
| **Only print() statements, no structured logger** | -- | partial (deterministic) | insufficient (intermittent/multi-threaded) |
| **No logger calls, no print, no error reporter near symptom** | -- | -- | insufficient |
| **Config level would suppress all existing logger calls at the symptom site** | -- | partial (if calls exist at higher level) | insufficient (if no calls at or above config level) |
| **Error-reporter SDK (Sentry/Datadog) is initialized and would capture the symptom class** | sufficient | -- | -- |

**Worked example 1 -- NameError (sufficient)**:

User reports `NameError: name 'Path' is not defined` at `eval_run.py:142`. Branch A finds no logger calls near line 142. Branch B finds `logging.yaml` with `level: WARNING`. Verdict: **sufficient** -- the Python stack trace names the file, line, missing symbol, and the fix (add the import). No instrumentation would have added diagnostic value.

**Worked example 2 -- Intermittent race condition (insufficient)**:

User reports "worker occasionally hangs, no error, just stops processing." Branch A finds one `logger.info("task_started")` at `worker.py:42` and a bare `except: pass` at `worker.py:198`. No request_id, no correlation token, no timing fields. Branch B finds `LOG_LEVEL=INFO` in `.env`. Verdict: **insufficient** -- one entry-point log and a silent exception handler cannot explain "occasionally hangs." Tasklist emitted with: add `logger.info("loop_iter", task_id=t.id, attempt=n, elapsed_ms=elapsed)` at the loop head; replace `except: pass` with `except Exception as e: logger.exception("task_failed", task_id=t.id, error=str(e))`; add `logger.debug("queue_depth", depth=q.qsize())` before the blocking call.

**Worked example 3 -- Config-suppressed signal (partial)**:

User reports "API returns 500 for POST /submit but no error in logs." Branch A finds `logger.error("submit_failed", error=str(e))` at `api.py:88` with full exception context. Branch B finds `logging.yaml` with `level: WARNING` and `pyproject.toml` with no logging section. Verdict: **partial** -- the logger call exists and is correctly placed, but the config level (WARNING) would suppress an ERROR-level call only if the root logger is misconfigured (ERROR < WARNING is false; ERROR would fire). If the config is actually `level: CRITICAL`, the verdict would be insufficient because even ERROR is suppressed.

## Complexity Gate

**Position**: Reuse the existing escalation-rubric signals (Option A from the seed brief) with a narrower pre-hypothesis interpretation. This avoids building a second classification surface and keeps the gate cheap.

The gate derives `issue_complexity` from Wave 0 + Wave 1 signals alone:

| Signal | Source | Weight |
|--------|--------|--------|
| `--type` is `performance` or `test` with "intermittent"/"flaky" keyword | Wave 0 parse | +1 |
| Scope spans > 2 files | Wave 0 `--scope` resolution | +1 |
| Stack trace crosses > 2 modules | Wave 1 grounding | +1 |
| Issue description contains "occasionally", "sometimes", "race", "deadlock", "intermittent" | Wave 0 parse | +1 |
| Issue description contains "slow", "p99", "memory", "regression" | Wave 0 parse | +1 |
| Cause class from Wave 1 triage is `Race/concurrency`, `Stale state/cache`, or `Performance/resource` | Wave 1 checklist scan | +1 |

**Classification**:

- Score 0-1: `trivial` -- hard-stop does NOT fire; soft-warn in REPORT.md.
- Score 2+: `non-trivial` -- if verdict is `insufficient`, hard-stop fires.

**Examples**:

- Trivial: `NameError` in single file, score 0. `Missing import` with clear stack trace, score 0. Off-by-one with stack trace naming the line, score 0.
- Non-trivial: "Worker occasionally hangs" (intermittent keyword + performance type = 2), "API slow after refactor" (performance type + regression keyword + multi-module scope = 3), "Test passes locally, fails in CI" (test type + intermittent keyword + env-drift = 2).

## Output Contract Additions

Add these fields to the Output Contract table in SKILL.md. All fields are additive and backwards-compatible.

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `diagnosability_verdict` | `sufficient \| partial \| insufficient \| unknown` | `unknown` | Wave 1.6 verdict. `unknown` when the audit could not run (auggie unavailable, scope not localizable, `--no-diagnosability-audit` set). Never silently skip -- always emit a verdict. |
| `diagnosability_tasklist_path` | `string \| null` | `null` | Absolute path to `diagnosability-tasklist.md` when emitted. `null` when verdict is `sufficient` or when verdict is `insufficient` but issue is trivial and hard-stop did not fire (tasklist is still emitted for soft-warn, so this would be set; only null when no tasklist was generated at all, e.g., verdict `unknown`). |
| `diagnosability_context_card_path` | `string \| null` | `null` | Absolute path to the Diagnosability Context Card (`<output-dir>/diagnosability-context.md`). Parallels `doc_context_card_path`. |
| `diagnosability_hard_stop` | `bool` | `false` | True when Wave 1.6 fired the hard-stop and skipped Waves 1.7-5. Downstream consumers use this to distinguish "ran to completion" from "stopped early for instrumentation." |

The existing 13 fields are untouched. New fields default to safe values (`unknown`, `null`, `false`) so consumers that do not read them continue to work.

## Tasklist Artifact Format

**Position**: High-specificity per-line tasks. Each task names the exact `file:line`, the log level, the exact fields to log, and the local variables to include. This bar is achievable because:

1. Wave 1.6 already has the `--scope` and `<component_paths>` localized by Wave 1.
2. The auggie queries return line numbers and snippets, so the tasklist generator knows which variables are in scope at each site.
3. Lower-specificity tasks ("add logging around the suspect function") are worse than no tasklist because they require the user to re-do the diagnostic scoping work that Wave 1.6 just performed.

**Format**: Markdown checklist with framework-aware syntax suggestions. The tasklist is framework-agnostic in structure but framework-aware in the suggested syntax.

### Worked example: `diagnosability-tasklist.md`

```markdown
# Diagnosability Tasklist

**Generated**: 2026-05-29T14:32:00Z
**Wave**: 1.6
**Issue**: Worker occasionally hangs during batch processing
**Verdict**: insufficient
**Complexity**: non-trivial (score=3: intermittent keyword + performance type + multi-module scope)
**Scope**: src/worker/, src/queue/

## Implementation tasks

Complete each task by adding the specified logging call at the given file:line. Use the framework already present in the file (or add the import if none exists).

### Task 1: Add iteration logging at the batch-processing loop head

- **File**: `src/worker/processor.py:142`
- **Current code**: `for task in batch:`
- **Framework**: `logging` (already imported as `import logging`, logger obtained via `logger = logging.getLogger(__name__)`)
- **Add after line 142**:
  ```python
  logger.info("batch_loop_iter", task_id=task.id, attempt=task.retry_count, batch_size=len(batch), timestamp=datetime.utcnow().isoformat())
  ```
- **Fields rationale**: `task_id` correlates across logs; `attempt` reveals if retries are accumulating; `batch_size` detects degenerate batches; `timestamp` enables latency computation when paired with the exit log (Task 2).

### Task 2: Add loop-exit logging after task processing

- **File**: `src/worker/processor.py:158`
- **Current code**: `results.append(result)` (end of loop body, after `result = task.execute()`)
- **Framework**: `logging` (same logger)
- **Add after line 158**:
  ```python
  logger.info("batch_loop_exit", task_id=task.id, elapsed_ms=(datetime.utcnow() - loop_start).total_seconds() * 1000, status="success")
  ```
- **Fields rationale**: Paired with Task 3, this measures per-task latency. A hang will show a Task 3 entry with no matching Task 2.

### Task 3: Add exception logging to replace silent handler

- **File**: `src/worker/processor.py:198`
- **Current code**:
  ```python
  except Exception:
      pass
  ```
- **Framework**: `logging` (same logger)
- **Replace with**:
  ```python
  except Exception as e:
      logger.exception("task_execute_failed", task_id=task.id, error_type=type(e).__name__, error=str(e))
  ```
- **Fields rationale**: `logger.exception` includes the full stack trace. `error_type` enables grouping by exception class. `task_id` correlates with the iteration log.

### Task 4: Add queue-depth logging before the blocking get()

- **File**: `src/queue/dispatcher.py:67`
- **Current code**: `task = self.queue.get(timeout=30)`
- **Framework**: `loguru` (already imported as `from loguru import logger`)
- **Add before line 67**:
  ```python
  logger.debug("queue_before_get", depth=self.queue.qsize(), timeout=30)
  ```
- **Fields rationale**: A growing `depth` indicates producer-consumer imbalance. A consistently zero depth with hangs indicates the producer is stalling, not the consumer.

### Task 5: Add Sentry breadcrumb for cross-service correlation

- **File**: `src/worker/processor.py:142` (same location as Task 1)
- **Framework**: Sentry SDK (already initialized in `src/worker/__init__.py`)
- **Add after Task 1's logger.info call**:
  ```python
  import sentry_sdk
  sentry_sdk.add_breadcrumb(
      category="worker",
      message=f"Processing task {task.id}",
      level="info",
      data={"batch_size": len(batch), "attempt": task.retry_count}
  )
  ```
- **Fields rationale**: If the process is killed (OOM, SIGTERM), Sentry's last breadcrumb will show which task was being processed. This complements the file-based logs which may not be flushed.

## Verification

After implementing all tasks:

1. Run the batch-processing workload with `LOG_LEVEL=DEBUG` (or the framework equivalent).
2. Verify that each of the 5 log lines appears in the output for a normal workload.
3. Confirm that the exception handler (Task 3) fires when given a failing task.
4. Re-run `/sc:troubleshoot` with the same issue description AND a fresh log excerpt. The re-run should produce `diagnosability_verdict: sufficient` because the new log calls would capture the loop state, latency, and exception context.

## Rollback

If instrumentation changes introduce unacceptable overhead:

1. Remove the added logger calls (they are all additive, no existing logic is modified).
2. Exception handler replacement (Task 3) MUST retain at least `logger.exception(...)` -- do NOT revert to `except: pass`. The original code was the diagnosed gap.
3. Revert the Sentry breadcrumb (Task 5) first if overhead is a concern -- breadcrumbs add ~1ms per call.
```

### Format notes

- Each task has a **numbered heading** for easy reference ("implement Task 3").
- The **current code** block lets the user confirm they are at the right line.
- The **framework** field tells the user which logger to use -- no guessing.
- The **fields rationale** explains why each field matters so the user can adapt if local variable names differ.
- Tasks that modify the same line (Task 1 + Task 5) are grouped and explicitly noted.
- The **Verification** section tells the user how to know they are done.
- The **Rollback** section protects against regressions from the instrumentation itself.

## Off-Ramp UX

**Hard-stop chat message** (when verdict is `insufficient` AND complexity is `non-trivial`):

> The diagnosability audit found that the code around the symptom site does not produce enough diagnostic signal to answer "when/where/why" for this issue. I've emitted an instrumentation tasklist at `<output-dir>/diagnosability-tasklist.md` with N concrete logging additions. The recommended workflow is: (1) implement the tasklist, (2) re-run the workload with the appropriate log level, (3) re-run `/sc:troubleshoot` with the fresh log excerpt. Skipping instrumentation and continuing to hypothesize against blind code is structurally unlikely to produce a high-confidence answer for an intermittent/multi-domain issue.

**Soft-warn REPORT.md section** (when verdict is `insufficient` AND complexity is `trivial`):

```markdown
## Diagnosability Context

The audit found limited logging coverage around the symptom site. For this deterministic issue (single-file scope, clear stack trace), the existing evidence is sufficient to proceed with hypothesis formation. However, the following instrumentation gaps were noted:

- <specific gap 1>
- <specific gap 2>

These are surfaced as informational; they do not block the diagnosis.
```

**Next Steps line** (REPORT.md when hard-stop fires):

> Next Steps: Implement the instrumentation tasklist at `<diagnosability-tasklist.md path>`, then re-run `/sc:troubleshoot <same-issue> --skip-diagnosability-audit` with a fresh log excerpt.

**Interaction with `--depth deep`**: `--depth deep` forces the hard-stop variant ONLY when verdict is `insufficient` -- even for otherwise-trivial issues. Rationale: `--depth deep` is an explicit user request for thoroughness, and the user may be using troubleshoot as part of a systematic audit of their codebase's diagnosability. The hard-stop respects that intent.

**Interaction with `--no-escalate`**: `--no-escalate` suppresses the hard-stop. The tasklist is still emitted (as a soft-warn), but Waves 1.7-5 proceed normally. Rationale: `--no-escalate` is a user assertion "give me your best Tier 1 answer" -- the hard-stop would contradict that by refusing to answer.

## Risk Register

### Risk 1: Query coverage gaps -- framework-specific patterns auggie misses

**Description**: The auggie query for Branch A names specific framework call patterns (`logging.info`, `logger.debug`, `console.warn`, `log.error`). If a codebase uses an unconventional logger name (`app_log.info`, `my_logger.debug`), an alias (`log = logging.getLogger`), or a custom wrapper (`emit("info", ...)`), the query may miss those calls entirely.

**Impact**: False-positive `insufficient` verdict -- the audit thinks there are no logger calls when there actually are. This wastes the user's time implementing a tasklist that duplicates existing logging.

**Mitigation**: The auggie query includes the instruction "find every location that produces diagnostic signal" which is semantically broader than just the named patterns. Auggie's semantic retrieval should catch alias and wrapper patterns even if the literal string does not match. The fallback `Grep` path explicitly lists the standard patterns and is acknowledged as degraded -- if the user knows their logger alias, they can supply it via `--scope`.

**Residual risk**: Medium-low. Auggie's semantic model handles alias patterns well in practice. The remaining gap is deeply custom wrappers (`log_event(level, msg, **ctx)`) that look like generic function calls.

### Risk 2: Log-config drift between environments

**Description**: Branch B finds `LOG_LEVEL=DEBUG` in `.env` but the symptom occurs in production where `LOG_LEVEL=WARNING`. The audit concludes "config level would capture" when it would not in the actual failing environment.

**Impact**: False-positive `sufficient` or `partial` verdict -- the audit thinks logs would fire but they would not in the environment where the bug manifests.

**Mitigation**: Branch B explicitly searches for environment-specific configs (Dockerfile, docker-compose, CI pipeline files, `.env*` with multiple profiles). The Diagnosability Context Card reports the effective level per environment when discernible. The sufficiency rubric treats "unknown" as the conservative verdict when env-specific config cannot be resolved.

**Residual risk**: Medium. This is an inherent limitation of static config analysis. The tasklist's Verification section instructs the user to test with the appropriate log level.

### Risk 3: Tasklist staleness on re-run

**Description**: The user instruments their code per the tasklist, then re-runs `/sc:troubleshoot` weeks later. The re-run audits the now-instrumented code, finds the tasklist's suggested calls already present, and emits a new tasklist for different gaps -- or worse, the original symptom site has moved due to intervening refactors.

**Impact**: The user implements a tasklist that was already partially implemented, or the tasklist targets lines that no longer exist.

**Mitigation**: The `--skip-diagnosability-audit` flag lets the user bypass re-audit when they know instrumentation has landed. The tasklist's Verification section instructs the user to re-run with a fresh log excerpt -- the re-run's Wave 1.6 then finds the new logger calls and emits `sufficient`, preventing duplicate tasklists. The `file:line` targets in the tasklist are validated by Wave 5's evidence-validator if the user re-runs troubleshoot before implementing -- mismatches are dropped.

**Residual risk**: Low-medium. The `--skip-diagnosability-audit` flag is the primary mitigation. Without it, the re-audit may produce redundant tasklists.

### Risk 4: Complexity-gate misfires on borderline issues

**Description**: An issue with complexity score 1 (trivial) is actually non-trivial in practice (e.g., a `NameError` that is a symptom of a deeper import-order race condition). The soft-warn path proceeds to hypothesis formation and wastes tokens on a blind guess when instrumentation would have been more productive.

**Impact**: Token waste on hypothesis formation against under-instrumented code. The user gets a low-confidence hypothesis instead of an actionable tasklist.

**Mitigation**: The complexity gate's score of 0-1 for trivial includes only the cheapest signals. If Wave 1.7's hypothesis formation produces low confidence (below 0.85), the escalation rubric in Wave 2 will still trigger Tier 2, at which point the parallel hypothesis agents can request more instrumentation. The gate is not final -- it is a fast-path optimization.

**Residual risk**: Low. The escalation rubric is the safety net.

### Risk 5: Coupling to Python-centric log frameworks

**Description**: Despite the cross-framework query design, the auggie query's concrete examples are weighted toward Python (8 patterns) vs JS (4 patterns) vs Java (3 patterns). In a polyglot codebase where the symptom is in a Java service, the query may under-perform because the Python patterns dominate the semantic context window.

**Impact**: Reduced retrieval quality for non-Python languages, leading to missed logger calls and false `insufficient` verdicts.

**Mitigation**: The query is structured as a numbered list with equal emphasis per language. The `<scope>` parameter narrows the search to the relevant language's source tree. If the scope is `src/java-service/`, auggie will naturally weight Java patterns higher. For users who know their language, they can set `--scope` to the language-specific directory.

**Residual risk**: Medium for polyglot repos with no `--scope`. The fallback `Grep` path explicitly lists patterns per language, so the degraded path is not worse than the auggie path for single-language scopes.

## Ref-File Changes

Propose a new ref file: `refs/diagnosability-audit.md`

This file is loaded on demand by Wave 1.6 only (never pre-loaded). Its sections:

### Section 1: Auggie query templates per branch

Contains the literal query strings for Branch A (Log-Call Inspection) and Branch B (Log-Config Inspection), with the `<scope>`, `<component_paths>`, and `<symptom>` placeholders.

### Section 2: Fallback paths

Contains the `Grep`/`Glob` commands per branch for when auggie is unavailable.

### Section 3: Structured-output schemas

Contains the JSON schemas for Branch A and Branch B outputs, matching the per-branch output files at `<output-dir>/wave1_6-branch-<A|B>.md`.

### Section 4: Sufficiency rubric

Contains the sufficiency table (signals vs verdict), the three worked examples (NameError, race condition, config-suppressed), and the verdict combination rules.

### Section 5: Complexity gate procedure

Contains the complexity scoring table, classification thresholds, and trivial/non-trivial examples.

### Section 6: Diagnosability Context Card template

Contains the markdown template for `<output-dir>/diagnosability-context.md`.

### Section 7: Tasklist generation rules

Contains the rules for generating `diagnosability-tasklist.md`: specificity bar, task format, framework-awareness rules, verification section requirements, and rollback guidance.

### Updated: `refs/report-template.md`

Add a new section `## Diagnosability Context` that renders the Wave 1.6 summary:

- Verdict line
- Tasklist path (if emitted)
- 1-3 bullet summary of the audit findings
- When hard-stop fires: the off-ramp message and Next Steps

This section appears between the existing "Documentation Context" and "Diagnosis" sections.

### Updated: Refs table in SKILL.md

Add a row:

| File | When loaded |
|------|-------------|
| `refs/diagnosability-audit.md` | Wave 1.6 (diagnosability audit -- auggie query templates, fallback paths, sufficiency rubric, complexity gate, context card template, tasklist rules) |

## SKILL.md Diff Sketch

### 1. Wave Structure ASCII diagram

Insert `Wave 1.6: Diagnosability Audit <-- always; loads refs/diagnosability-audit.md on demand; skipped only by --no-diagnosability-audit` between Wave 1.5 and Wave 1.7.

### 2. Output Contract table

Add the four new fields (`diagnosability_verdict`, `diagnosability_tasklist_path`, `diagnosability_context_card_path`, `diagnosability_hard_stop`) with types, defaults, and descriptions as specified in the Output Contract Additions section.

### 3. Wave 0: Parse + Validate Input

Add `--no-diagnosability-audit` to the optional flags list. Add `--skip-diagnosability-audit` as a flag for re-runs after instrumentation.

### 4. New Wave 1.6 section

Insert the full Wave 1.6 procedure between Wave 1.5 and Wave 1.7, covering:

- Entry criteria
- Branch A and B spawn via Task fan-out
- Wait + read branch outputs
- Synthesize Diagnosability Context Card
- Sufficiency verdict computation
- Complexity gate
- Hard-stop / soft-warn / continue branching
- Failure handling table

### 5. Wave 5: Synthesis + Report

Add a step to render the Diagnosability Context section in REPORT.md (between Documentation Context and Diagnosis). Note that when hard-stop fires, Wave 5 renders a special report variant with the off-ramp message as the primary Next Steps.

### 6. Tool Coordination Summary

Update the auggie row to note Wave 1.6's 2-branch fan-out. Add that Wave 1.6 uses `Grep`/`Glob` as fallback.

### 7. Will Do

Add: "Run the diagnosability audit every run unless `--no-diagnosability-audit` is set; emit an instrumentation tasklist when logging is insufficient for the symptom."

### 8. Will Not Do

Add: "Apply instrumentation changes from the tasklist -- that is always a separate `/task` invocation or manual implementation."

### 9. Error Handling

Add rows for Wave 1.6 failure scenarios matching the failure handling table in the Audit Mechanics section.

### 10. Token Cost Profile

Add a row or adjust Tier 1 only:

| Tier reached | Auggie tokens | Claude tokens | Wall clock |
|--------------|--------------|---------------|------------|
| Tier 1 + Wave 1.6 | ~4-8k (+2-3k for 1.6) | ~5-9k (+1-2k for 1.6) | 2-4 min (+30-60s for 1.6) |

### 11. Refs table

Add `refs/diagnosability-audit.md` row.

## Persona-Distinctive Claims

These are the claims that distinguish the devops-perspective variant from the architect and analyzer variants:

1. **Two-branch is the right shape, not three**. Exception-handler richness is a piggyback signal, not a separate branch. The architect variant may argue for symmetry with Wave 1.5's three branches; the devops answer is that fan-out should match orthogonal retrieval strategies, not conceptual surfaces. Log calls and log config require different auggie queries (code surface vs config surface); exception handlers live on the same code surface and are captured by the same query. Adding a third branch for exception handlers burns tokens without adding coverage.

2. **Tasklist specificity must be per-line, not per-function**. The analyzer variant may argue for lower-specificity tasks to reduce the audit's own complexity. The devops answer is that per-function tasks push the scoping burden back onto the user -- the exact burden Wave 1.6 was designed to eliminate. The auggie queries already return line numbers and snippets; the incremental cost of per-line tasks is minimal compared to the user-time savings.

3. **Log-config is a first-class audit surface, not a footnote**. A logger call that is filtered by config is indistinguishable from no logger call at runtime. Any diagnosability audit that only counts logger calls without checking what level they run at is a half-audit. The Python ecosystem alone has 4 config surfaces (`logging.yaml`, `logging.conf`, `pyproject.toml [tool.logging]`, env vars); the Java ecosystem adds 3 more (`log4j2.xml`, `logback.xml`, `application.properties`). Branch B is mandatory.

4. **Complexity gate should reuse escalation-rubric signals, not build a new surface**. The seed brief's Option B (new narrower complexity score) tempts designers who want purpose-built classification. The devops answer is that every classification surface is a maintenance burden, and the escalation rubric's signals (intermittent keywords, multi-domain, security_caution) already capture exactly what makes an issue non-trivial. Reusing them keeps the gate cheap and the mental model consistent across the protocol.

5. **The tasklist must survive polyglot and non-logger signal diversity**. Real codebases do not all use `logging.info`. Some use Sentry breadcrumbs, some use stdout JSON, some use `print()` to stderr for historical reasons, some use Datadog traces. The tasklist format must be framework-aware (telling the user which logger to use at each site) while being framework-agnostic in structure (each task has the same fields: file:line, current code, framework, add-this, rationale). This is why the tasklist format names the framework explicitly per task.

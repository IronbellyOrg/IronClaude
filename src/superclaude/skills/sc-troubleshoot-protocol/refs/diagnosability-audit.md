# Diagnosability Audit Rules

Wave 1.6 of the sc:troubleshoot protocol. Audit sections load in Wave 1.6; shared Section 7 loads lazily wherever a tasklist is created or extended.

This ref defines the two parallel audit branches (A: log-call inspection at and around the failing component; B: log-config inspection across the repository for that component's effective log level and reachability), the per-branch structured-output schemas, the sufficiency rubric that maps audit signals to a verdict, the complexity gate that decides whether an insufficient verdict warrants a hard-stop, the Diagnosability Context Card template that synthesises Branch A + Branch B outputs, the tasklist generation rules with hard constraints that bound any emitted instrumentation patch, and the T4 worked example. Wave 1.7 (hypothesis formation) and Wave 5 (synthesis + report) consume the synthesised Diagnosability Context Card.

---

## Section 1: Auggie query templates per branch

Each branch issues ONE `mcp__auggie__codebase-retrieval` call (single message, fan-out via parallel Task spawns from the Wave 1.6 orchestrator). The placeholders `<failing_component>`, `<scope>`, and `<symptom>` are filled by the Wave 1.6 orchestrator from the Wave 0 input (issue description, `--scope`, `--type`) and the Wave 1 grounding output (the localized failing component path).

### Branch A — Log-Call Inspection

Query target: `<failing_component>` (plus immediate callers).

```text
In the codebase at <failing_component> (or <scope> if broader), find every location that produces diagnostic signal around the behavior described as: <symptom>. This includes:

1. Python: logging module calls (logging.debug/info/warning/error/exception/critical), loguru calls, print() statements, structlog calls.
2. JavaScript/TypeScript: console.log/warn/error/debug/info, winston/pino/bunyan logger calls.
3. Java: SLF4J/Logback calls, Log4j2 calls, java.util.logging calls.
4. Exception handlers: try/except (Python), try/catch (JS/Java). For each, whether it logs the exception or silently swallows it.
5. Error-reporter initializations: Sentry.init(), Datadog.init(), rollbar.configure(), or equivalent.

For each hit, return: file path, line number, call_type (logger_call | print | exception_handler | error_reporter_init), framework, log level, 1-2 line snippet, and (for exception handlers) richness: rich | minimal | silent.
```

### Branch B — Log-Config Inspection

Query target: repository-wide configuration for `<failing_component>`.

```text
In the entire repository, find every configuration file or environment-variable reference that controls logging behavior for <failing_component>:

1. Python: logging.yaml/.yml/.conf/.ini, log_config.py, [tool.logging] in pyproject.toml.
2. Java: log4j2.xml/.properties, logback.xml, application.properties/.yml with logging.* keys.
3. JS/Node: winston.config.js, logger.js, pino transport config, .env with LOG_LEVEL/DEBUG/NODE_ENV.
4. Env vars: LOG_LEVEL, LOGLEVEL, DEBUG, NODE_ENV=production, LOG_FORMAT=json in Dockerfile, docker-compose.yml, .env*, Makefile, CI pipeline files.
5. Structured-log filter/rate-limit config, sampling configuration.

For each hit, return: file path, config_type (file | env_var | pipeline_config), framework, effective log level if discernible, 1-3 line snippet.
```

---

## Section 2: Fallback paths (auggie unavailable)

When `mcp__auggie__codebase-retrieval` is not available (Wave 0 detected `--no-mcp`, the gateway is down, or rate limits exhausted the per-session call budget), each branch falls back to Glob/Grep substitutes. The orchestrator MUST set the branch's `degraded` flag to `true` so the sufficiency rubric in Section 4 caps the verdict at `partial`.

### Branch A fallback

```bash
grep -rn 'logging\.\(debug\|info\|warning\|error\|exception\|critical\)\|logger\.\(debug\|info\|warning\|error\|exception\|critical\)\|from loguru import' <failing_component>
grep -rn 'print(' <failing_component>
grep -rn 'console\.\(log\|warn\|error\|debug\|info\)' <failing_component>
grep -rn 'logger\.\(info\|warn\|error\|debug\)\|log\.\(info\|warn\|error\|debug\|trace\)' <failing_component>
grep -rn 'except\s*:' <failing_component>
grep -rn 'catch.*{.*}' <failing_component>
grep -rn 'Sentry\.init\|Datadog\.init\|rollbar\.config' <failing_component>
```

When the fallback fires, set Branch A schema field `degraded` to true; the sufficiency rubric caps the verdict at `partial` (never `sufficient`) when degraded=true.

### Branch B fallback

```bash
find . -name 'logging.{yaml,yml,conf,ini}' -o -name 'log4j2.*' -o -name 'logback*.xml' -o -name 'winston*.js' -o -name 'logger.js' 2>/dev/null
grep -n '\[tool\.logging\]\|\[tool\.pytest\.ini_options\].*log' pyproject.toml
find . -name 'application*.{properties,yml,yaml}' 2>/dev/null
grep -rn 'LOG_LEVEL\|LOGLEVEL\|DEBUG\s*=\|NODE_ENV\|LOG_FORMAT' .env* Dockerfile docker-compose.yml Makefile .github/workflows/*.yml .gitlab-ci.yml 2>/dev/null
```

When the fallback fires, set Branch B schema field `degraded` to true; reachability_verdict defaults to `unknown` for every Branch A hit.

---

## Section 3: Structured-output schemas per branch

Each branch agent writes ONE structured-output file at `<output-dir>/wave1_6-branch-<A|B>.md`. Branch A returns the inventory of diagnostic-signal call sites (logger calls, prints, exception handlers, error-reporter inits) near `<failing_component>`. Branch B returns the log-config inventory plus a derived `reachability_verdict` per Branch A hit, computed by inspecting whether the effective log level for that hit's logger reaches a sink (file, stdout, error reporter) given the discovered config.

### Branch A schema

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

The `captured_bytes` field is populated when the failing-run transcript referenced specific log files (sniffed via `wc -c`); otherwise null.

### Branch B schema

```json
{
  "branch": "B",
  "query_target": "<failing_component>",
  "hits": [
    {"config_path": "...", "config_type": "env_var", "framework": "logging",
     "effective_level": "INFO", "snippet": "...", "location": ".env:3"}
  ],
  "reachability_verdicts": [
    {"file_path": "...", "line": 142, "verdict": "reaches_sink"}
  ],
  "degraded": false
}
```

`config_type` ∈ `{file, env_var, pipeline_config}`. `reachability_verdict` ∈ `{reaches_sink, filtered_out, unknown}` — one entry per Branch A hit, keyed by `{file_path, line}`. When `degraded=true`, every reachability_verdict defaults to `unknown`.

---

## Section 4: Sufficiency rubric + 3-W's synthesis

After Branches A and B return, the Wave 1.6 orchestrator computes the verdict directly (no MCP call; pure synthesis over Branch A inventory + Branch B reachability_verdicts + the Wave 1 observation). The verdict vocabulary is exactly `{sufficient, partial, insufficient, unknown}` (matches the Output Contract field `diagnosability_verdict`).

### 3-W's coverage scoring

| W | Answerable from existing instrumentation? | Signal |
|---|------------------------------------------|--------|
| **When** | Branch A has timestamped logger calls within `failing_component` AND Branch B confirms `reaches_sink` | `yes` |
| **Where** | Branch A has logger calls naming the symptom site (file + line via stack-trace mapping) | `yes` |
| **Why** | Branch A has state-capturing logger calls (fields, args, return values, exception context) near symptom site AND Branch B confirms reachability | `yes` |

Each W is `yes | partial | no`. The triple feeds the sufficiency rubric below.

### Sufficiency rubric (S14 priority, then first match)

Evaluate S14 first ONLY for evidenced loss/substitution of the actual disputed datum that remains missing from captured failing-run output. It overrides positive static sufficiency signals (including S3); an unrelated hidden field does not qualify. After a provenance-bound observation of that datum resolves the loss, re-evaluate S14 and then apply S1–S13 in their existing order, first match wins. Use this same precedence on every recomputation; merely reaching a sink or printing an expected value does not resolve S14.

| Signal combination | Verdict |
|--------------------|---------|
| **S1**: Symptom is a deterministic exception with a clear stack trace bottoming in user code | `sufficient` (stack trace IS the signal) |
| **S2**: Symptom is a build/compile error with line-numbered diagnostic | `sufficient` |
| **S3**: Branch A has ≥3 structured logger calls within `failing_component` AND Branch B confirms `reaches_sink` AND 3-W's coverage all `yes` | `sufficient` |
| **S4**: 3-W's coverage has 2 `yes` + 1 `partial`, Branch A moderate density, Branch B `reaches_sink` | `sufficient` (with caveat noted in card) |
| **S5**: Branch A has captured-bytes > 0 for some streams but 0 bytes for the stream that would have answered the failing W | `insufficient` (static density alone is misleading) |
| **S6**: Branch B `filtered_out` (e.g., level=WARNING but only INFO logs near symptom) | `partial` (if Branch A has higher-level calls) or `insufficient` (if no calls at or above filter level) |
| **S7**: Error-reporter SDK (Sentry/Datadog) initialized AND would capture the symptom class | `sufficient` |
| **S8**: 1-2 logger calls at INFO, no exception-handler logging, no error reporter | `partial` (if deterministic) or `insufficient` (if intermittent) |
| **S9**: Only `print()` statements, no structured logger | `partial` (deterministic) or `insufficient` (intermittent / multi-threaded) |
| **S10**: No logger calls, no print, no error reporter near symptom site | `insufficient` |
| **S11**: Auggie unavailable AND Glob/Grep fallback returned no signal AND Branch A `degraded=true` | `unknown` |
| **S12**: `failing_component` not localizable (no `--scope`, stack trace bottoms in compiled code) | `unknown` |
| **S13**: Intermittent keywords present AND 3-W's `when_answerable != yes` | `insufficient` (intermittent-with-no-trace short-circuit) |
| **S14**: the asserted value exists at a code-site (`file:line` known) but an intermediate layer between that site and what the model reads (filter, allowlist, projection, summary, formatter, wrapper) drops it or writes an expected/default value in its place | `insufficient` (the layer hides the datum) |

### Behavior under degradation

| Scenario | Verdict | Surfaced in |
|----------|---------|-------------|
| Auggie unavailable, Grep/Glob found signal | `partial` (cap; degraded discovery loses semantic recall) | Diagnosability Context Card with `degraded: true` |
| Auggie unavailable, Grep/Glob found nothing | `unknown` | Grounding Gaps |
| `failing_component` not localizable | `unknown` | Grounding Gaps |
| `--no-diagnosability-audit` | not emitted (audit skipped); `diagnosability_verdict: unknown` in contract | REPORT.md header + Grounding Gaps |

---

## Section 5: Complexity gate

The complexity gate reuses the structural dimensions of `refs/escalation-rubric.md` (multi-domain, intermittent, security_caution) with a narrower pre-hypothesis interpretation — extracted from Wave 0 + Wave 1 signals only, no dependency on Wave 1.7's calibrated confidence (which fires later in the pipeline). The gate's output decides whether an `insufficient` verdict triggers a hard-stop (`non-trivial`) or only a soft-warn (`trivial`).

### Signal table (extracted at Wave 1.6 entry)

| Signal | Source | Weight |
|--------|--------|--------|
| `--type` is `performance` OR (`test` with intermittent/flaky keyword) | Wave 0 parse | +1 |
| Scope spans > 2 files | Wave 0 `--scope` resolution | +1 |
| Stack trace crosses > 2 modules | Wave 1 grounding | +1 |
| Issue text contains "occasionally", "sometimes", "race", "deadlock", "intermittent", "randomly", "only in CI/prod", "flaky" | Wave 0 parse | +1 |
| Issue text contains "slow", "p99", "memory", "regression", "leak" | Wave 0 parse | +1 |
| Cause class from Wave 1 triage ∈ {Race/concurrency, Stale state/cache, Performance/resource, Substituted primitive} | Wave 1 checklist scan | +1 |
| `--type security` set | Wave 0 parse | **Always non-trivial (override)** |

### Classification rule

- Score 0-1: `trivial` — hard-stop does NOT fire; soft-warn only.
- Score 2+ OR `--type security`: `non-trivial` — hard-stop fires if `verdict=insufficient` AND `--no-escalate` is not set.

### Examples

**Trivial**: NameError single-file (score 0), missing-import with clear stack trace (score 0), off-by-one with stack trace naming the line (score 0), TypeError on a single-file scope with a deterministic repro (score 0-1).

**Non-trivial**: "Worker occasionally hangs" (intermittent + performance = 2), "API slow after refactor" (performance + regression + multi-module = 3), "Test passes locally, fails in CI" (test + intermittent + env-drift implied = 2), any `--type security` (override).

---

## Section 6: Diagnosability Context Card template

The Diagnosability Context Card is the synthesised artifact at `<output-dir>/diagnosability-context.md`. It is written by step S1.6.3 (the orchestrator synthesis step) from Branch A + Branch B outputs plus the Wave 1 observation, and it is the consumer-facing summary that Wave 1.7 (hypothesis formation), Wave 5 (REPORT.md composition), and any future re-run of the protocol reads to decide downstream behavior. The card carries a bounded ≤6-line `Implication for diagnosis confidence` block that REPORT.md's `## Diagnosability Context` section renders verbatim.

```markdown
# Diagnosability Context Card

**Issue**: <issue_description from Wave 0>
**failing_component**: <repo-relative path from Wave 1 grounding>
**Verdict**: <sufficient | partial | insufficient | unknown>
**Complexity**: <trivial | non-trivial> (score breakdown: <signal weights>)
**Hard-stop fired**: <true | false>
**Round**: <N> of 3
**Captured bytes (failing run)**: <bytes-or-n/a>

## 3-W's coverage

| W | Answerable | Evidence |
|---|------------|----------|
| When  | <yes | partial | no> | <Branch A timestamp evidence + Branch B reachability> |
| Where | <yes | partial | no> | <Branch A symptom-site evidence> |
| Why   | <yes | partial | no> | <Branch A state-capture evidence + Branch B reachability> |

## Branch A — Log-call inventory

Summary of hits found near `<failing_component>`. Total: <N>. Breakdown by call_type: <logger_call: M | print: M | exception_handler: M | error_reporter_init: M>. Exception-handler richness breakdown: <rich: M | minimal: M | silent: M>. `degraded`: <true | false>.

## Branch B — Log-config reachability

Effective log level for `<failing_component>`: <LEVEL from config>. Source: <config_path>. Per-Branch-A-hit reachability_verdict summary: <reaches_sink: M | filtered_out: M | unknown: M>. `degraded`: <true | false>.

## Sufficiency rubric application

Row fired: <S1 | S2 | ... | S13 | S14>. Reason: <evidence for S14's disputed-datum override, or why this S1–S13 row matched first after S14 did not apply; cite the resolving observation when recomputed>.

## Implication for diagnosis confidence

<≤6 lines. Names the existing instrumentation in 1 line, names the gap (what the audit could not answer) in 1 line, names the consequence for any Tier 1 or Tier 2 hypothesis in 1-2 lines, and names the actionable next step (instrument first vs proceed) in 1-2 lines. This block is the soft-warn summary REPORT.md's `## Diagnosability Context` section renders verbatim.>

## Tasklist reference

<Path to <output-dir>/diagnosability-tasklist.md if the verdict triggered tasklist emission; otherwise "n/a (verdict=sufficient | unknown)".>
```

---

## Section 7: Tasklist generation rules + hard constraints

When the verdict triggers tasklist emission (verdict ∈ {partial, insufficient} on any complexity, plus the hard-stop branch under `insufficient + non-trivial + NOT --no-escalate`), the orchestrator writes a standalone tasklist at `<output-dir>/diagnosability-tasklist.md`. The tasklist file is ALWAYS standalone (a markdown artifact the user reads and applies manually). The opt-in `--diagnosability-handoff` flag additionally invokes `task-builder` against the tasklist for full MDTM packaging.

### Hard constraints (non-negotiable)

1. **Invocation-site-only**: Every task MUST target an invocation site (test script, CI workflow YAML, dev harness, container entrypoint, dev-mode config override), NEVER the failing component's own source code. Diagnostic code in production source leaks into release artifacts.
2. **Additive only**: Every task is a pure ADD (or a config-override at an invocation site). No task modifies existing source logic. Tasks that would otherwise modify source are re-framed as config-overrides (`LOG_LEVEL=DEBUG` env var, `--debug` flag at invocation, structured-log filter relaxation in test config).
3. **Reversible**: Every task has a Rollback line describing how to revert post-defect-closure.
4. **Revert annotation**: Patches added by the tasklist carry the comment `# Diagnosability-tasklist instrumentation: revert after defect closed.` so cleanup is mechanizable.
5. **Emitter search before `blocked`**. Before any task or verdict uses the word `blocked`, run this read-only discovery procedure and record it in the tasklist under `## Emitter search`; this requirement never authorizes a refused rerun:
   1. From the missing-evidence list, take every predicate that is a single boolean or enum expression at a known `file:line`. None → write `emitter-search: n/a (no single-expression predicate)` and skip only the producer-specific grep in 2; still assess the actual missing evidence's capture channels in 3–4 before claiming a capability block.
   2. Grep the function containing the producer line and the one function that calls it (one level) for existing emit calls (print/log/echo/printf/write/tee/report append). Record `emitters-found: N` with `file:line` of each.
   3. Record raw `already-read-files: <count>` separately from eligible artifact sinks. For each candidate record site/sink, actual datum access, capture command/transport, and eligibility or exclusion reason. A usable capture route requires a technically viable path from the actual value to a permitted invocation-site emitter or preserved log/report/artifact sink; sink existence alone is not a route. Production-source emit calls are truthful discovery hits, NEVER authorized edit sites. A wrapper is eligible only if it can actually access the datum without changing production source. Existing artifacts may supply read-only observations with provenance; artifact-only access never authorizes a new run. Propose ONE line `<predicate-name>=<observed value>` via a viable route; read error/missing value emits `<predicate-name>=unobserved`, never an expected/default value. Preserve original captured input and bind observations to run/arm/command. Generated annotations do not manufacture evidence. Record `usable-capture-routes: <count>` and the searched channels even when the count is zero; permission to execute is recorded separately as `re-run permitted` and enforced before execution.
   4. `capability-verdict: blocked` is valid ONLY when the search establishes `usable-capture-routes: 0`, with exclusions for all discovered candidates/channels. Positive raw emitter/read-file counts do not forbid this result. A viable route with unknown or refused permission is not a capability failure: leave execution pending with its permission/transport reason. An emitter row plus refused rerun instead triggers `blocked-on-authorization`; never invent a viable route to obtain that verdict. For no single-expression predicate, record the n/a reason and assess the actual missing evidence's channels before claiming a capability block.
   Each line proposed by 3 is a **task type 5 — fail-closed observed-value emission**, subject to constraints 1-4 (invocation site, additive, reversible, annotated). Name the actual missing evidence it measures; link S14 ONLY when the disputed-datum loss/substitution predicate applies. A `fix-candidate` row (diff path) may accompany it in the same round under `## Fix candidate` as a proposal subject to existing fix authorization; no later wave is a precondition.
6. **Preregister measurements; link enabling tasks**: every measurement in `## Discriminator rows` names its claim, observable, provenance, and `value-if-<claim>-true | value-if-false` predictions derived from cited evidence before execution. Values may be equal (non-discriminating); use `unknown — <reason>` when not derivable rather than fabricate a split. Record the outcome mapping as consistent/refuted/inconclusive; consistency is not proof. Empty/incomplete/error captures are `unobserved`, never false and never an outcome-table input. Enabling tasks (log-level, wrapper, upload) reference their measurement row IDs and give operational verification/rollback, not invented causal values. A missing preregistration must be filled or explicitly marked unknown before publication; pending execution never prevents publishing the tasklist. Next Steps preserves each pending row with its role, reason and preregistered outcomes. Relevant unresolved core evidence contributes partial, without lowering blocked/failed; optional pack rows are informational pending work only, never a status prerequisite or causal decision input.

### High-specificity per-line task format

Each task names:

- **Invocation site**: exact `file:line` of the invocation surface to be modified
- **Current code**: a 1-3 line snippet showing what's there now
- **Task type** (exactly one of the five below): the concrete code change (additive, invocation-site-only, with the revert annotation comment)
  1. **Env override** — set a log-level / debug / trace env var at the invocation site (skeleton Task 1)
  2. **Fixture wrapper** — a test fixture or harness wrapper that captures correlation, timing, or state around the existing call (skeleton Task 2)
  3. **Subprocess wrap** — wrap the invocation in a tracer or verbose mode (skeleton Task 3)
  4. **Telemetry / artifact capture** — breadcrumb, metric, or CI artifact-upload step so the signal survives the run (skeleton Tasks 4-5)
  5. **Fail-closed observed-value emission** — one line `<predicate-name>=<observed value>` through a technically viable, permitted-site capture route established by constraint 5 (never a production-source edit); prints `<predicate-name>=unobserved` on read error or missing data and never the expected value. Name the missing evidence; link S14 only when it applies, including for bracket rows that otherwise measure ordinary thresholds.
- **Rationale**: why this resolves one of the missing W's (when / where / why) from Section 4's 3-W's coverage scoring

### Worked tasklist skeleton

```markdown
# Diagnosability Tasklist
**Issue**: <issue text>
**Verdict**: <verdict>  **Complexity**: <complexity>  **failing_component**: <path>  **Round**: <N> of 3  **re-run permitted**: yes|no|unknown  **discriminator-required**: yes|no  **capability-verdict**: blocked|n/a
**branch**: <branch>  **repro-venue-id**: <stable matrix/job label or repro command, digits stripped>
<!-- append to the header only when they apply: **indistinguishable**: <a>,<b> (S1.6.4 step (ii) gave up)  **probe-rows-truncated**: <n> (omitted base pairs when more than 8 were proposed; excludes optional pack rows) -->

## Emitter search
emitters-found: 0
already-read-files: 0
usable-capture-routes: 0
<Candidate sites/sinks, datum-access routes and exclusions; authorization/transport state per constraint 5.>

## Discriminator rows
<core-rows=C, pack-rows=P, total-rows=C+P; each row has ID, core/optional role, claim, observable, probe, true/false predictions or justified unknown, outcome mapping, provenance, observed/pending state and reason per constraint 6. Enabling tasks link these IDs.>

## Bracket
<Only when triggered: measurement rows and evidence per primitive-differential Section 3.>

## Fix candidate
<Optional proposal and paired verification; no implicit authorization.>

## Hard Constraints
- INVOCATION SITES only; ADDITIVE only; each task is annotated `# Diagnosability-tasklist instrumentation: revert after defect closed.`

## Implementation tasks
<The six headings below are illustrative; populate applicable tasks with invocation site/current code, type, linked measurement IDs or measurement preregistration, rationale, operational verification and rollback.>
### Task 1: Enable DEBUG log level at the test invocation site
### Task 2: Add request-correlation logging via test fixture (NOT in production source)
### Task 3: Run with strace at invocation (Linux only — skip on non-Linux CI)
### Task 4: Capture queue-depth telemetry via Sentry breadcrumb at invocation
### Task 5: Add CI artifact upload for trace files
### Task 6: Fail-closed observed-value emission beside the nearest existing emitter (task type 5)
- One line `<predicate-name>=<observed value>` via the viable route documented in `## Emitter search`; missing/error data prints `<predicate-name>=unobserved`. Link the measurement preregistration and actual missing evidence; name S14 only when applicable.

## Verification
## Rollback
## Patch-round counter
```

The fully-worked 5-task example appears in Section 8 (T4 worked example).

### Section order (S1.6.4a)

When S1.6.4 emits `diagnosability-tasklist.md` (verdict ∈ {partial, insufficient}, including when the discriminator trigger forced `partial`), the file has these sections in this order, each written by the step named. Keep the file and its path if probes subsequently make the verdict sufficient; later Wave 3 creation paths use the same composition:

1. Header: `Round: <N> of 3`, stable branch and repro-venue identity, `re-run permitted: yes|no|unknown`, `discriminator-required: yes|no`, `capability-verdict: blocked|n/a`, `indistinguishable: <a>,<b>` (only when the discriminator step (ii) gave up), `probe-rows-truncated: <n>` (omitted base pairs, only when the 8-pair cap applied).
2. `## Emitter search` (constraint 5 above).
3. `## Discriminator rows` (discriminator pairs + control row; falsifier columns per constraint 6 on every core row; the 2×2 differential of `refs/primitive-differential.md` Section 2 when both environments were observed). At most 19 core rows: 8 pairs + 1 control + up to 2 distinguishing rows. Optional pack rows are appended and accounted separately under that ref's Section 2 step 3: `core-rows=C`, `pack-rows=P`, `total-rows=C+P`; informational packs never displace core rows or become decision inputs. Core runs first; optional row/venue attempts share a limit of 3 per invocation, with unattempted cells retained as pending and reasons recorded. A full core plus the existing three-row read/parse pack for one producer emits 22 rows. Ten proposed base pairs retain eight and report `probe-rows-truncated: 2`, independent of pack rows.
4. `## Bracket` (`refs/primitive-differential.md` Section 3, only when its trigger fired).
5. `## Fix candidate` (constraint 5 trailing rule, optional; proposal only, subject to existing fix authorization).
6. `## Hard Constraints` (constraints 1–6 above).
7. `## Implementation tasks` (applicable tasks nested at `###`; the skeleton's six headings illustrate the five task types, not six mandatory changes).
8. `## Verification` (measurement evidence and enabling-task operational checks).
9. `## Rollback` (per-task reversal).
10. `## Patch-round counter` (identity, authoritative value and snapshot; update once as below).

One tasklist per run, one shared authoritative counter with a per-run snapshot (see Patch-round counter below). All tasklist creation paths preserve pending rows for Wave 5 Next Steps; execution obeys the shared authorization/transport gate before the verdict branch. Known refusal forbids execution regardless of complexity or `--no-escalate`; artifact-file access permits reading captured evidence, not executing new probes. Branch on the recomputed verdict even when probes ran but remained inconclusive.

### Patch-round counter

The orchestrator maintains the authoritative per-defect counter at `<repo-root>/.dev/troubleshoot/diagnosability-rounds.json`, independent of the timestamped or custom output directory; `<output-dir>/diagnosability-rounds.json` is only this run's snapshot. Entries are logically keyed `<branch>:<repro-venue-id>` and stored as nested JSON objects keyed by branch then venue, avoiding delimiter collisions. Preserve the failing arm's stable matrix/job label (or exact repro command) with digits stripped so re-numbered runs of the same venue share one 3-round key; never use a transient run ID. Record the identity in the tasklist and snapshot. Read the authoritative store before every counted emission; create its parent as needed and initialize an absent store to an empty mapping under the same lock. An existing unreadable/corrupt/locked store is a reported block, never a silent reset. Serialize read/update/snapshot under the store lock and replace the store atomically. Increment once per invocation that emits a tasklist with `discriminator-required: yes`, including later Wave 3 emissions, not per rewrite, append or probe; bracket rounds are separate. At round 3 or later still write the tasklist and cap message (refs/report-template.md), set `status: blocked`, skip automatic reruns and suppress their recommendation. `--reset-diagnosability-rounds` clears only the current branch/venue entry under the same lock before increment; other keys survive. Three fresh output directories for the same identity record 1, 2, 3, not 1, 1, 1.

---

## Section 8: T4 worked example — what the audit saves

T4 is the canonical example of the `insufficient + non-trivial` hard-stop path: the user reports "worker occasionally hangs, no error, just stops processing." Without Wave 1.6 the protocol spends Tier 2 token-rounds hypothesizing against blind code; with Wave 1.6, the user instruments first, re-runs with fresh evidence, and the second-pass hypothesis converges on the real cause.

### Inputs

- **Wave 0 issue text**: "worker occasionally hangs during batch processing, no error, just stops"
- **Wave 1 observation**: `failing_component = src/worker/processor.py`; cause-class triage = Race/concurrency

### Branch A findings

One `logger.info("task_started")` at `worker.py:42`. One bare `except: pass` at `worker.py:198`. No request_id, no correlation token, no timing fields. `captured_bytes=4096` for `worker.log` — existing logs ARE present and reaching the sink.

### Branch B findings

`LOG_LEVEL=INFO` in `.env`. No `pyproject.toml` logging section. Effective level: INFO. `reachability_verdict` for `worker.py:42` and `worker.py:198`: `reaches_sink`.

### Synthesis

3-W's coverage:

- **When**: `partial` (the `task_started` log gives turn-of-event timing but no per-iteration timing)
- **Where**: `partial` (only one logger naming the entry; the hang is somewhere between line 42 and the bare-except at line 198 with no intermediate signal)
- **Why**: `no` (no state-capturing logs; the `except: pass` silently swallows whatever the exception was)

S-row fired: **S13** (intermittent keyword "occasionally" present AND `when_answerable != yes`) → `insufficient` short-circuit.

### Verdict + complexity

- `verdict = insufficient`
- `complexity = non-trivial` (score 3: intermittent keyword +1, `--type performance` implied +1, multi-module scope +1)
- `--no-escalate` is NOT set
- → **Hard-stop fires.** `diagnosability_hard_stop = true`. Waves 1.7–4.5 are skipped (hardening does not run). `status = partial` unless S1.6.4 precedence contributes `blocked`.

### Tasklist emitted

A 5-task skeleton at `<output-dir>/diagnosability-tasklist.md` (per Section 7 — invocation-site-only, additive, reversible, revert-annotated):

1. **Task 1**: Enable `LOG_LEVEL=DEBUG` env override at `tests/integration/test_worker.py:18` (the `subprocess.run` invocation site).
2. **Task 2**: Add request-correlation logging via a `worker_runner_with_tracing` pytest fixture in `tests/integration/conftest.py:45` — NOT in `worker.py` source. Captures thread name + timestamp + level for every existing logger call.
3. **Task 3**: Wrap `subprocess.run` with `strace -f -e trace=read,write,futex` at `tests/integration/test_worker.py:18` (Linux only; skip on non-Linux CI). Surfaces IPC/futex-level hangs when worker.py-level logging is silent.
4. **Task 4**: Add a Sentry breadcrumb at `tests/integration/conftest.py:80` capturing `queue.qsize()` at test start. Survives mid-hang process kill.
5. **Task 5**: Add CI artifact upload step in `.github/workflows/integration-tests.yml:42` with `if: failure()` for `worker_trace.log` and `worker_strace.log`. Trace files are useless if CI discards them.

### What was saved

Without Wave 1.6 the protocol would have spent Tier 2 hypothesis-round tokens against blind code (no request_id, no thread names, no captured state) and produced low-confidence hypotheses indistinguishable from informed guesses. With Wave 1.6 the user instruments first (5 invocation-site-only tasks, all reversible), re-runs the workload, and re-enters `/sc:troubleshoot` with fresh log/trace excerpts. The second-pass hypothesis has the request-correlation + thread-name + queue-depth + syscall data needed to converge on the actual cause (typically a futex deadlock or queue-starvation scenario the bare-`except: pass` was swallowing). Net effect: one round of instrumentation-time investment displaces multiple Tier 2 token-rounds against blind code.

---

## Loading discipline

Wave 1.6 reads Sections 1–8 once on entry. Any later tasklist creator/append path (including behaviour-definition failure and Wave 3 split after audit bypass) loads Section 7 lazily without rerunning audit Sections 1–6 or 8. First creation uses the full Section order, stable identity and shared locked counter, eligibility search, authorization/transport gates and pending-row publication. Later appends reuse that artifact and the once-per-invocation increment; if the discriminator requirement first becomes yes on append, perform the one counted update then. Audit bypass remains logged and never grants execution permission.

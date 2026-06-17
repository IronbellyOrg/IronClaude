# Briefing — `task_vs_sctask` eval suite + the cliEval v-next it requires

> **Purpose of this file.** It is the cross-session context substrate for two linked efforts:
> **(A)** the eval suite we *want* (a head-to-head comparison of two tasklist pipelines), and
> **(B)** the next version of the **cliEval** harness that suite needs in order to run end-to-end.
> A `/sc:cli-eval create` attempt stopped at the Wave-0 fresh-context gate because the suite cannot be
> authored as *executable* against today's harness. This briefing captures why, and what to build.
>
> **Freshness caveat.** Every `file:line` citation below was captured on **2026-06-15** from a live
> `eval-docs-loader` digest. The harness is under active development — **re-load the live contract
> from source before acting on any citation.** Do not trust this file's line numbers as current.

---

## A. The suite we want — `task_vs_sctask`

A standardized, repeatable **head-to-head comparison of two tasklist pipelines**, both fed an
**identical spec**, then executed by their native executors, then scored and audited.

1. **Generation (identical input spec):**
   - Pipeline 1: build a small tasklist with **`/task-builder`**.
   - Pipeline 2: build a small tasklist with **`/sc:tasklist`**.
2. **Execution (each tasklist by its native executor):**
   - Pipeline 1's tasklist → executed by **`/task`**.
   - Pipeline 2's tasklist → executed by the **`superclaude sprint run`** CLI pipeline.
3. **Scoring framework (brainstormed, standardized):** a KPI set capturing **effectiveness,
   efficiency, accuracy, thoroughness, and quality** for each pipeline — applied identically to both.
4. **Audit:** a **formal generated audit report** over the outputs of both pipelines.
5. **Adversarial debate:** an **adversarial debate against both reports** (i.e. the two pipelines'
   audit reports are pitted against each other / stress-tested).
6. **Matrix:** **2 runs per model**, with the **entire suite run by all T0, T1, and T2 models** defined
   in `~/.aienv`.

### Design decisions already agreed (carry these forward)

- **Runs axis → `parameterize`.** The 2-runs-per-model axis is encoded inside the manifest via the
  schema's `parameterize` (expands eval ids `E1.1`, `E1.2`, …).
- **Model sweep → external wrapper.** Because the suite schema has **no model dimension** (see B2),
  the T0/T1/T2 sweep is an **external wrapper** that re-runs the validated suite once per model by
  setting the `~/.aienv` env (`ANTHROPIC_DEFAULT_*_MODEL`) before each `eval run`. (Per the `.aienv`
  contract: use only the endpoints/models declared there.)
- **Scoring/audit/debate → prompt-driven evals + downstream stage.** Each eval is a Claude PTY
  session whose **prompt** instructs the work (generate / execute / audit) and emits artifacts to
  known paths; **coarse `expects`** (`file` / `jsonl` / `stdout` / `exit_code`) assert the artifacts
  exist and are well-formed. The **KPI math + audit report + adversarial debate** run as a
  **downstream stage** over the run artifacts (e.g. `/sc:adversarial`), *not* as native eval
  assertions — because the assertion layer that would let them be native is not wired (see B3).

---

## B. Why it can't run end-to-end today — the missing harness pieces

All three are blockers for *authoritative end-to-end execution*. The suite can be **authored and
schema-validated** today, but a real run would be non-authoritative and/or skipped.

### B1 — The executor is a non-production stub (runs are NON-AUTHORITATIVE)

`_resolve_executor_factory()` returns a zero-side-effect `_NullLifecycleExecutor`; production wiring
(`ClaudeProcessAdapter` + `PtyDriver`) lands only when the vendored PTY harness is on disk.
`src/superclaude/cli/eval/commands.py:1357-1405`. A real `eval run` emits a one-shot stderr warning:
`_NullLifecycleExecutor active … results MUST NOT be treated as authoritative`
(`commands.py:1860-1885`) — and that warning is **suppressed under `--json`** (`commands.py:1866-1870`),
so absence of the warning does **not** prove a production executor. Today the only operator-reachable
green path is `--no-pty` short-circuiting tagged evals to `SKIPPED`.
**Needed:** vendored PTY harness + production lifecycle executor wired into `_resolve_executor_factory()`.

### B2 — No model dimension in the suite schema

`suite.schema.json`'s `evalEntry` exposes `id, title, category, requires, timeout_sec, isolation,
inputs, expects, parameterize, no_pty` — **no `model:` field** (`suite.schema.json:124-158`). Model
routing happens via `~/.aienv` env at `claude` spawn time, which the manifest does not parameterize.
So "all T0/T1/T2 models, 2 runs each" is **not expressible in one manifest** — only the runs axis is.
**Needed (for native support):** a first-class model dimension in the schema + runner (e.g. a
`models:` matrix the runner sweeps by setting spawn env per cell), **or** a blessed, documented
external sweep wrapper if native support is deliberately out of scope.

### B3 — `expects`→callable resolver unwired; `callback:` rejected

The per-spec worker constructs `EvalRunner(..., expect_callables=(), ...)` and an inline comment says
the manifest-`expects`→callable resolver "lands in a follow-up"; specs that survive `--no-pty`
currently PASS via the null executor (`commands.py:1431-1434`, `1463-1475`). The declarative `expects`
primitives that DO exist: `file, jsonl, settings_json, exit_code, stderr, stdout, duration`
(`src/superclaude/cli/eval/expect.py:1-9`). The README documents a `*_callbacks.py` escape hatch, but
`evalEntry` is `additionalProperties: false` with **no `callback:` field** — a `callback:` entry fails
validation today (`suite.schema.json:124-158`; README at
`src/superclaude/cli/eval/suites/README.md:24-26,84-86`).
**Needed:** wire the `expects`→`ExpectCallable` resolver into the run path, and (if rich
programmatic assertions are wanted) add a schema-blessed `callback:` field + loader/runner resolver.
Without this, KPI scoring / audit / debate cannot be native assertions.

### Contract anchors (re-verify before use)

- Status enum: `PASS, FAIL, ERRORED, TIMEOUT, INTERRUPTED, SKIPPED, XFAIL, XPASS`
  (`src/superclaude/cli/eval/models.py:49-58`). `SKIPPED ≠ PASS`.
- Run exit codes: `0` all PASS/SKIPPED/XFAIL · `1` any FAIL/ERRORED/TIMEOUT/XPASS · `2` harness
  rejection · `3` SIGINT/SIGTERM (`commands.py:1678-1686`; `exit_codes.py:21-24`).
- Artifacts: `<output_root>/.dev/eval-runs/<YYYY-MM-DD>/<run-id>/` with `summary.{md,json,yaml}` +
  per-eval dirs; `summary.json` is machine-readable truth (`artifact_layout.py:1-21,151-204`).
- FR-G5 coverage gate (exit 2) checks `~/.claude/settings.json` matchers; empty-`HOME` workaround
  documented (`commands.py:1813-1829`; `docs/eval/suites-guide.md:529-548`).
- Reference suites to imitate: `eval_smoke.yaml`, `installer_sync_drift.yaml`.

---

## C. What the v-next design effort must deliver

A cliEval version that makes the `task_vs_sctask` suite (and others like it) **authoritatively
executable end-to-end**. Minimum scope implied by B1–B3:

1. **Production executor** (vendored PTY harness + real lifecycle executor) so runs are authoritative.
2. **Model matrix** — native `models:` sweep in schema+runner, **or** a blessed external sweep
   wrapper driven by `~/.aienv` (decision to be made in the design).
3. **Assertion plumbing** — wire `expects`→callable; decide whether to add a schema-blessed
   `callback:` for programmatic KPI/scoring/audit assertions.
4. **Downstream debate integration** — a sanctioned path for `/sc:adversarial` to consume run
   artifacts (the two audit reports) as a post-run stage.
5. **Multi-pipeline / multi-session orchestration** — a suite step model that can run a *generate →
   execute → audit* chain where one eval's artifacts feed the next.

The design should be grounded in the **current** code (re-load the live contract first), enumerate
options + tradeoffs for each of the above, and produce a spec hard enough to hand to implementation.

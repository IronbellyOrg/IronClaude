# D-0081 — Implementation notes

## Module-level decisions

* **One constant, three surfaces.** The OPS-003 retention advice
  string is pinned exactly once in
  `src/superclaude/cli/eval/disk_budget.py::DISK_BUDGET_RETENTION_ADVICE`.
  The policy doc `docs/eval/retention.md` quotes the constant verbatim
  inside a fenced code block; the CLI dispatcher echoes the same bytes
  via `click.echo(..., err=True)` before the breach exit. A single
  edit point keeps the three surfaces aligned forever — any drift is a
  test failure rather than a silent operator surprise.

* **Advice content driven by operator playbook, not formatting
  prefs.** Three sentences, each load-bearing:
  1. Lead with the breach name (`"disk-budget exceeded"`) so
     operators reading the failing-CI log tail can grep + pivot.
  2. Tell the operator what was preserved (run dir + summaries +
     per-eval artifacts for finished evals + the
     `disk_budget_exceeded.json` side-car) so they do not assume the
     run was wiped — preserving evidence is the load-bearing OPS-003
     behaviour.
  3. Tell the operator the two retention knobs (`--max-disk-mb`,
     `--keep-home`) and back-link to `docs/eval/retention.md` so the
     next invocation can be reconfigured without re-reading the source.
  Test `test_retention_advice_constant_shape` asserts every signal is
  present so a future edit to the advice that drops one fails loudly.

* **Doc-quotes-constant invariant, not the other way round.** The
  test asserts `DISK_BUDGET_RETENTION_ADVICE in doc_text`. The doc may
  contain additional commentary around the quoted block, but the
  constant must appear verbatim. This means the doc is free to wrap
  the advice in a fenced code block, add a heading, or re-render it
  for readability — as long as the canonical bytes survive intact.

* **`click.echo(..., err=True)`, not `sys.stderr.write`.** The eval
  dispatcher already uses `click.echo` for every operator-facing
  diagnostic (HARD_FAIL gate messages, capability-report rendering,
  etc.). Reusing `click.echo` keeps the breach advice on the same
  channel discipline (line-buffered, newline-terminated, encoding
  honouring `PYTHONIOENCODING`) as the rest of the Phase 4 surface.

## Test design decisions

* **Five run-today tests + one forward-dep gated test, not all six
  forward-dep gated.** The four doc + constant + advice-shape tests
  (1–4) exercise the library/document seam and depend on no run-loop
  closure helpers. They run today. The CLI-stderr emission test (5)
  and the `--keep-home True` HOME-preservation test (6) traverse the
  closure; they reuse the `_t0410_missing()` /
  `_skip_unless_t0410_landed()` probe pattern from
  `test_exit_codes.py` so the skip diagnostic stays consistent.

* **Synthesised disk-budget breach via pre-seeded run dir.** Test 5
  creates `output_dir` and seeds it with a 2 MB file *before* invoking
  `superclaude eval run --max-disk-mb 1`. The poller's first
  recursive `stat()` walk observes 2 MB > 1 MB and trips immediately;
  no scheduling games or time-based waits are needed. This keeps the
  test fast (a single subprocess + a single 2 MB write to `tmp_path`)
  and deterministic across CI hardware.

* **Pillar coverage by literal substring assertions, not by parsing.**
  The policy doc is markdown, not a structured data file. Rather than
  parse headings and tables we assert the **load-bearing literals**
  appear in the doc text:
  * `.eval-meta/setup_failed` — exact constant value, not a paraphrase;
  * `NFR-ISO2` — the upstream identifier operators can pivot to;
  * `disk_budget_exceeded.json` — the side-car filename a `cat`
    invocation would target;
  * `--keep-home`, `--max-disk-mb`, `--junit-xml` — the operator-
    visible flags.
  This catches a future edit that paraphrases the pillar away (e.g.
  "the failed-setup tag is preserved" without naming the relpath)
  while leaving the doc free to add prose around each literal.

* **Status-name coverage as a separate assertion.** `PASS`, `FAIL`,
  `ERRORED`, `TIMEOUT` are checked individually rather than as a
  single concatenated string so the failure message names the
  missing status. The retention matrix in `docs/eval/retention.md` §2
  is the load-bearing operator-facing table and a missing status row
  silently corrupts the contract.

## Wiring point (commands.py)

The advice is emitted at the breach branch in the exit-code switch:

```python
if poller.is_breached():
    click.echo(DISK_BUDGET_RETENTION_ADVICE, err=True)
    sys.exit(DISK_BUDGET_EXCEEDED_EXIT_CODE)
```

Two design constraints land in this two-line addition:

1. The advice is rendered **after** the Reporter has written
   `summary.{md,json}` / `junit.xml` — `Reporter(...).write(...)`
   runs unconditionally before the exit-code switch. So the operator
   reading the stderr advice can immediately `cat` the path the
   advice text points at.
2. The advice is rendered **before** `sys.exit` so it always reaches
   the channel regardless of any down-stream `atexit` handler
   buffering games.

## T04.10 hand-off

T04.10 is the run-loop closure that adds `_new_run_id`,
`_run_one_spec`, `_compute_run_stats`, and the three terminal
exit-code constants. Once T04.10 lands:

* Tests 5 and 6 un-skip automatically (the probe pattern returns an
  empty `_t0410_missing()` list).
* The OPS-003 advice path becomes reachable in normal end-to-end
  runs, not just the synthetic pre-seeded-output-dir breach.
* No edit to this module's deliverables is required; the constant +
  doc + dispatcher wiring are all forward-compatible with T04.10.

## Rejected alternatives

* **Render the advice as YAML or JSON.** Considered structuring the
  advice as `{"reason": "...", "knobs": ["--max-disk-mb", "--keep-home"], "doc": "docs/eval/retention.md"}`
  so downstream tools could parse it. Rejected: the stderr surface is
  for humans reading a failing CI log tail; the
  `disk_budget_exceeded.json` side-car already carries the structured
  payload. A second machine-readable surface would just double the
  drift surface.

* **Constant on `DiskBudgetPoller` class.** Considered hanging
  `RETENTION_ADVICE` off `DiskBudgetPoller` next to `ARTIFACT_NAME` /
  `BREACH_REASON`. Rejected: the advice text is OPS-003 (an operator-
  facing policy) rather than NFR-PERF4 (the poller mechanism), and the
  policy spans multiple non-poller surfaces (`--keep-home` is part of
  it). A module-level constant keeps the ownership boundary clean.

* **CLI flag to suppress the advice.** Considered `--no-retention-advice`
  for CI-quiet scenarios. Rejected on YAGNI: the advice is rendered
  only on a breach (exit code 2), which is by definition a noisy
  failure path — suppressing the recovery instructions would defeat
  the purpose.

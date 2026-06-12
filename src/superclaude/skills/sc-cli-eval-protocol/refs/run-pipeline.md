# Ref: RUN Pipeline (full step detail)

Load this in the run branch after Wave 0. The run pipeline is **interactive orchestration the skill
performs directly** — AskUserQuestion + background Bash + Monitor + reading summary.json. It adds NO
flags to `superclaude eval`. Run artifacts/notes go under `.dev/eval-workspaces/cli-eval/runs/`.

## W1 — Enumerate via the CLI (never scrape the dir)

```bash
uv run superclaude eval list --json
```

Parse the `{name, version, eval_count}` array. This is the menu's source of truth — it reflects
exactly what the loader will accept, including schema validity.

## W2 — Interactive selection (AskUserQuestion)

- Build one menu option per suite: `"<name> — v<version> — <eval_count> evals"`.
- Honor `--suite`/`--eval` pre-selections by pre-filling.
- On selection, optionally drill: `uv run superclaude eval describe --suite <name>` and surface the
  per-eval id/title, `isolation.home_strategy`, `timeout_sec`, and any `no_pty: skip` markers. Offer
  `--eval <id>` filtering if the user wants a single eval.

## W3 — Confirm invocation + flags (AskUserQuestion) + gotchas

Confirm the EXACT command before launching. Flags to offer (from the Wave-0 digest):
`--parallel`, `--eval <id>`, `--no-mcp`, `--no-pty`, `--json`, `--junit`, `--timeout-mult`,
`--keep-home`, `--max-disk-mb`, `--output-dir`.

Surface the gotchas explicitly and let the user choose:

- **FR-G5 coverage gate (exit 2)** — the doctor preflight checks every `~/.claude/settings.json`
  matcher against the suite; if the host's settings would leave matchers uncovered, the run aborts
  with exit 2. Offer the empty-HOME workaround from the digest:

  ```bash
  TMPHOME=$(mktemp -d) && HOME=$TMPHOME uv run superclaude eval run --suite <name> --no-mcp; rm -rf "$TMPHOME"
  ```

- **`--no-pty` → SKIPPED** — PTY-driven evals (`no_pty: skip`) short-circuit to SKIPPED with
  `skip_reason="--no-pty"` and exit 0. That is the CI-canary path, NOT a real pass. For real
  PASS/FAIL, omit `--no-pty` (and handle FR-G5 via the empty-HOME workaround).
- Default `--output-dir` to a workspace path (e.g. `.dev/eval-workspaces/cli-eval/runs/<stem>`) so
  artifacts are easy to find; the FR-G4 layout (`.dev/eval-runs/<date>/<run-id>/`) is layered under it.

## W4 — Monitor a live run (background Bash + Monitor)

Launch the confirmed command as a **background** Bash job (per-eval timeouts can reach 3600s — never
block the session). Attach a **Monitor** whose filter catches BOTH progress and every terminal state,
not just success — e.g.:

```text
grep -E --line-buffered "PASS|FAIL|SKIP|ERROR|TIMEOUT|INTERRUPT|summary.json|Traceback"
```

Report per-eval signals as they stream and the terminal exit code. Silence is not success — if the
job crashes, the filter must still emit something.

**Authoritativeness probe**: prefer `--verbose` over (or in addition to) `--json` for the run, because
`--json` suppresses the executor warning line. The harness may run a non-production executor (e.g. a
milestone-gated `_NullLifecycleExecutor` that emits canned PASS before the real PTY executor lands);
that surfaces as a `results MUST NOT be treated as authoritative` warning on the verbose path. Capture
it — a green summary.json from a stubbed executor is a *plumbing* pass, not a real one.

## W5 — Parse + report (DELEGATE eval-run-reporter)

After completion (or interrupt), Task the `eval-run-reporter` agent with the run dir. It reads
`summary.json` (truth) and produces the operator report using `templates/run-report.md`:

- per-eval table: id, title, status, duration_sec, skip_reason/skip_flag_triggered, error_class;
- the `counts`/`totals` line and the process exit-code interpretation;
- the run-dir path and the preserved failed-HOME paths (from each non-PASS eval's `artifacts{}`).

**Honesty invariants**: non-zero exit or any FAIL/ERRORED/TIMEOUT/XPASS is a surfaced result, never a
silent pass. An all-SKIPPED run (e.g. `--no-pty`) is reported as skipped with the reason, and the
real-run invocation is offered. Exit 2 is interpreted as usage/harness/FR-G5, not an eval failure.
And a PASS from a non-production/stubbed executor is labeled **NON-AUTHORITATIVE (plumbing only)** with
what unblocks a real run — never presented as a real eval pass.

## Completion criteria

- summary.json parsed; operator report rendered with run-dir + forensic HOME paths.
- Verdict stated plainly (pass / fail / interrupted / all-skipped) with the exit code.

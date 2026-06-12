# cliEval Run Report — {{suite}}

> Rendered by the `eval-run-reporter` agent from `summary.json` (machine-readable truth).
> Run dir: `{{run_dir}}`

## Verdict

**{{verdict}}** — process exit code `{{exit_code}}` ({{exit_meaning}}).

**Authoritativeness: {{AUTHORITATIVE | NON-AUTHORITATIVE (plumbing only)}}** — executor:
`{{executor}}`. {{if non-authoritative: "Result produced by a stubbed/non-production executor
(canned outcome); the `results MUST NOT be treated as authoritative` warning is suppressed by --json.
Unblocked by: {{what lands the production executor}}."}}

> Reminder: SKIPPED ≠ PASS. Exit 2 = usage/harness/FR-G5 coverage gate, not an eval failure.
> A PASS from a non-production executor is a plumbing pass, NOT a real eval pass.

## Counts / totals

| metric | value |
|---|---|
| manifest_n / expanded_n′ | {{counts.manifest_n}} / {{counts.expanded_n_prime}} |
| passed / failed / errored | {{totals.passed}} / {{totals.failed}} / {{totals.errored}} |
| skipped / timeout / interrupted | {{totals.skipped}} / {{totals.timeout}} / {{totals.interrupted}} |
| parallel | {{parallel}} |
| duration_sec | {{duration_sec}} |

## Per-eval

| eval_id | title | status | duration_sec | skip_reason / error_class | preserved HOME (forensics) |
|---|---|---|---|---|---|
| {{eval_id}} | {{title}} | {{status}} | {{duration_sec}} | {{skip_reason_or_error}} | {{home_path_if_non_pass}} |

## Forensics

For every non-PASS eval, the per-eval HOME is preserved (runner default) at the path in its
`artifacts{}` map above. Inspect `per-eval/<eval_id>/{logs.jsonl, tty.transcript, artifacts/}` under
the run dir for the failing transcript.

## Surfaced issues

- {{each FAIL / ERRORED / TIMEOUT / XPASS, or "none — all evals passed"}}
- {{if all SKIPPED: "All evals SKIPPED ({{skip_reason}}). This is the canary/skip path, not a pass.
  Real-run invocation: omit --no-pty (handle FR-G5 via the empty-HOME workaround)."}}

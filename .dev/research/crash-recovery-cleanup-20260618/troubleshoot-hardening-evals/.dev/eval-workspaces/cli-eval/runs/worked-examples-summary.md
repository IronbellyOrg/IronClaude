# Worked Examples — run record

## CREATE pipeline — 3 suites authored, schema-validated, run in parallel

Authored under `src/superclaude/cli/eval/suites/` (one via the iteration-1 create-pipeline test,
two authored here in the same house style):

| Suite | evals | `eval describe` (done-ness gate) | `eval list --json` |
|---|---|---|---|
| `eval_cli_doc_parity` | 3 (DP1/DP2/DP3) | exit 0 ✓ | discovered ✓ |
| `cli_eval_skill_contract` | 2 (CE1/CE2) | exit 0 ✓ | discovered ✓ |
| `suite_schema_guard` | 2 (SG1/SG2) | exit 0 ✓ | discovered ✓ |

**Parallel run** (3 concurrent `eval run` jobs, empty-HOME FR-G5 workaround, `--verbose --no-mcp`),
2026-06-12 141534Z:

| Suite | run-dir | process exit | per-eval | Authoritative? |
|---|---|---|---|---|
| eval_cli_doc_parity | `.dev/eval-runs/2026-06-12/141534Z-6dc1f0a6/` | 0 | DP1/DP2/DP3 PASS | **NO** |
| cli_eval_skill_contract | `.dev/eval-runs/2026-06-12/141534Z-e85285a9/` | 0 | CE1/CE2 PASS | **NO** |
| suite_schema_guard | `.dev/eval-runs/2026-06-12/141534Z-fe2414c2/` | 0 | SG1/SG2 PASS | **NO** |

**Authoritativeness — NON-AUTHORITATIVE (plumbing only).** Every eval shows `duration_sec=0.0` and
`expects=0` (assertions NOT evaluated), and all three `--verbose` runs printed:
`eval run: WARNING: _NullLifecycleExecutor active — ... run results MUST NOT be treated as
authoritative.` The PASSes prove the pipeline is wired end-to-end (discovery → FR-G5 → HOME isolation
→ per-eval layout → summary emission → exit-code mapping); they do NOT prove the DP/CE/SG assertions
hold. A real assertion pass is unblocked when the production PTY executor (ClaudeProcessAdapter +
PtyDriver) lands at milestone M5/M6 and replaces `_NullLifecycleExecutor`.

> This is the `eval-run-reporter` honesty contract working as designed: a stubbed-executor PASS is
> reported as NON-AUTHORITATIVE, never as a real eval pass.

## RUN pipeline — monitored `eval_smoke` (iteration-1 + iteration-2)

Selected via `eval list --json` → menu → confirm; FR-G5 exit-2 gate fired → cleared with the
empty-HOME workaround; `--no-pty`→SKIPPED gotcha surfaced. `summary.json` parsed: ES1/ES2/ES3 PASS,
exit 0 — likewise **NON-AUTHORITATIVE** (M2 null executor; `--json` suppresses the warning, `--verbose`
surfaces it). Run dirs under `.dev/eval-runs/2026-06-12/`. Full operator reports:
`.dev/eval-workspaces/cli-eval/iteration-{1,2}/eval-1/with_skill/run-1/outputs/report.md`.

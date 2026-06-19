# Iteration 1 — grading + analysis (autonomous/headless mode)

Mode: autonomous, no human reviewer/browser → self-graded against the evals.json assertions; written
report substitutes for the browser viewer (skill-creator headless adaptation).

## Benchmark

| Eval | With-skill | Baseline (no skill) | Discriminating? |
|---|---|---|---|
| 0 layperson-bug-review | 7/7 PASS | ~5/7 (missed lens hand-off `/sc:adversarial`; otherwise good) | partial |
| 1 edge-case→edge-case-hunt | 4/4 PASS | FAIL: chose `bare-review` (wrong lens), reviewers 3 (wrong default 4) | YES — strong |
| 2 real-run-env-missing | 6/6 PASS | FAIL: launched a real run ignoring intent (workers 404'd) | YES — strong |

With-skill pass rate: **17/17 (100%)**. The skill's value is clearest where a vanilla agent mis-maps the
goal to a lens (eval 1) and where it skips the dry-run/go-ahead gate and fires a real run (eval 2).

## Real findings to fix (evidence-based)

1. **Proxy 404 gotcha (HIGH value).** A real `openai_compat` run against the `~/.aienv` proxy
   (`T2ProxyUrl=…:4000/cli`) returns **HTTP 404 proxy_error** on every worker, because the swarm
   transport posts `{base}/chat/completions` → `…/cli/chat/completions` (404), while the working OpenAI
   route is `…/cli/v1/chat/completions` (200). Verified by direct curl in baseline eval-2 (`/v1/models`
   200, key valid). → The wizard must have a 404 diagnostic that explains "the proxy base path doesn't
   expose chat/completions where the CLI looks" and tells the user to verify `T2ProxyUrl` in `~/.aienv`,
   WITHOUT the wizard inventing the corrected path.
2. **`uv run` noise.** The `VIRTUAL_ENV=… will be ignored` warning prints on every `uv run` line and can
   confuse a true non-programmer. → Add a one-line reassurance in the run ref.

## Non-issues / confirmations

- Wave-0 ground-truth gate worked: live `--help` matched the ref; `--tui` real; stale-doc warning #3
  (fresh inline run emits merged.md + return-contract.yaml) re-confirmed.
- The mandatory stub-first gate + Wave-4 explicit-go-ahead both fired correctly.
- No fabrication of proxy values in any with-skill run.

## Plan for remaining rounds

- R2: apply the two fixes; re-test the real-run/proxy path; add a harder ambiguous-goal scenario (must
  disambiguate, not silently pick) + a doc-completeness mapping.
- R3: trigger-description evals (should-trigger vs near-miss negatives) + description optimization.
- R4: edge gates — target too small → STOP; advanced/custom-lens trust-boundary warning.
- R5: final regression pass over core scenarios; conformance check vs dev-guide; finalize + sync.

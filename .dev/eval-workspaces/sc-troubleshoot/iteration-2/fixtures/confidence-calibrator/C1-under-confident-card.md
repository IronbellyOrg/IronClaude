# Hypothesis: eval_run passes --output-dir as both candidate and allowlist-extending kwarg

**Agent**: root-cause-analyst
**Tier**: 1
**Timestamp**: 2026-05-21T05:50:00Z
**Cause class**: Logic regression

## Claim

`eval_run` at `commands.py:1476` calls `resolve_scratch_root(requested_output, config=base_config, output_dir=output_dir)`, passing the operator-supplied `--output-dir` as both the candidate AND the `output_dir=` kwarg. `resolve_scratch_root` extends its allowlist with the kwarg value before checking the candidate, so the candidate trivially matches itself — the OPS-002 policy check becomes a tautology and any path (`/etc/foo`, `/root`, `/`) is silently accepted.

## Evidence

- `/config/workspace/IronClaude/.dev/eval-workspaces/sc-troubleshoot/evals/fixtures/real-bug-scratch-root/commands.py:1476` — `output_dir=output_dir,`
- `/config/workspace/IronClaude/.dev/eval-workspaces/sc-troubleshoot/evals/fixtures/real-bug-scratch-root/commands.py:1406` — `def eval_run(`
- `/config/workspace/IronClaude/.dev/eval-workspaces/sc-troubleshoot/evals/fixtures/real-bug-scratch-root/scratch-roots.md` — OPS-002 policy doc with verbatim `/etc/foo` rejection example
- Command: `git show 1ca2595:src/superclaude/cli/eval/commands.py | sed -n '1473,1477p'` → shows the exact buggy line

## Proposed Fix

Drop the `output_dir=output_dir` kwarg from `eval_run` call site at `commands.py:1476`. Add regression test at `tests/cli/eval/test_eval_run_scratch_root.py` asserting `/etc/foo` is rejected with exit 2 and the OPS-002 policy reference in stderr.

## Confidence

Self-reported confidence: 0.65

(Agent's note: confidence kept low because I haven't run the test myself and the symptom may have a non-obvious second cause I missed.)

## Risks

- Removing the kwarg may break legitimate callers that rely on it (defense-in-depth helpers).
- Fix should preserve the kwarg in the function signature even after removing it from the eval_run call site.

## If I'm wrong, it's probably because

The bug is actually in `resolve_scratch_root`'s allowlist-extension logic, not in the call site.

## Alternatives considered

- Helper-level guard rejecting self-allowlisting pattern — rejected as wrong layer.

## Grounding gaps

None.

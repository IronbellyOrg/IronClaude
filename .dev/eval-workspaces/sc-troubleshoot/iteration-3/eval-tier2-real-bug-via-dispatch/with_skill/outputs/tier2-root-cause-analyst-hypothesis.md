# Tier 2 Hypothesis Card — root-cause-analyst

**Brief received**: Original issue + Tier 1 card. Asked to validate or extend the Tier 1 hypothesis.

**Claim**: I confirm the Tier 1 diagnosis and refine the root-cause framing. The bug is **a misreading of the `resolve_scratch_root(output_dir=...)` contract by the `eval_run` author**. The kwarg's documented purpose (per `config.py:192-196` docstring and `scratch-roots.md:91-97`) is to let *programmatic callers inside `src/superclaude/cli/eval/`* check sub-paths under a *user-supplied root that has already been validated elsewhere*. The author of `eval_run` used the kwarg as if it were a "policy override" — passing the candidate as its own escape hatch. Doctor's author got it right; eval_run's author re-derived the API wrong.

**Evidence**:

- `config.py:192-196` (docstring of `output_dir` kwarg):
  > "Optional CLI-supplied ``--output-dir`` to extend the allowlist for this call only."
  This is correct for *downstream sub-path validation*, but the kwarg name + docstring don't loudly distinguish "extend allowlist for sub-path checks" from "extend allowlist when checking the operator-supplied root itself" — and the bug is the operator confusing the two.
- `config.py:225-229` — the resolution loop. The check returns the resolved candidate immediately if it equals any prefix in `allowed`. When the candidate IS one of the appended prefixes, the comparison is trivially satisfied.
- `commands.py:1472-1477` — eval_run's call site.
- `commands.py:815-823` — doctor's call site. Note the *absence* of the `output_dir=` kwarg.
- `commands.py:1490-1499` — the *correct* downstream extension pattern. AFTER the candidate has passed validation, the author builds `runtime_allowed = base.allowlist + (resolved_output, home_root)` and constructs a `runtime_config` with this extended allowlist for downstream HomeIsolation / containment_guard checks. **This is what the `output_dir` kwarg is for, but applied at the right layer.** The bug is that the author conflated the two layers.

**Proposed fix (root-cause-analyst choice)**: Same as security-engineer (FIX-A) — drop the `output_dir=output_dir` kwarg from the line-1473 call. The runtime_config built at lines 1490-1499 already handles the legitimate "extend the allowlist for downstream sub-paths" case correctly. The two layers should not be confused.

**Alternate fix worth considering (FIX-B)**: Remove the `output_dir` kwarg from `resolve_scratch_root` entirely, since the legitimate use case (sub-path under a validated root) is already covered by building a `runtime_config` with the extended allowlist (commands.py:1490-1499 pattern). The kwarg's existence invites exactly this misuse. **Verdict**: appealing for API hygiene but out of scope for a security fix; defer to a refactor task.

**Confidence (agent self-report)**: 0.94

**If I'm wrong it's probably because...**: there's a test or call site I haven't read that depends on `output_dir=output_dir` self-validation. A grep across the rest of `src/superclaude/cli/eval/` is the next step (deferred to evidence-validator).

**Risks of fix**: Confirmed minimal. Same risk register as security-engineer's card. One additional note: the `output_dir` kwarg should probably grow a docstring warning ("do NOT pass the candidate being validated") as a follow-up hardening — but that's a doc change, not part of the fix.

**Test plan**: One regression test as security-engineer proposed, plus one positive test asserting `eval run --output-dir /tmp/eval-runs/op1` still succeeds (sanity check that the fix doesn't over-correct).

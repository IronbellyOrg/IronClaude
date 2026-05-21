# Tier 1 Hypothesis Card — root-cause-analyst

**Symptom**: `superclaude eval run --output-dir /etc/foo` silently succeeds and creates the directory; `superclaude eval doctor --output-dir /etc/foo` correctly rejects with `ScratchRootViolation` exit 2. Both should enforce the same OPS-002 / AC12 allowlist.

**Hypothesis (single, best-evidence)**: The `eval_run` call to `resolve_scratch_root` passes the rejected operator path **as the `output_dir` kwarg**, which `resolve_scratch_root` interprets as an *additional allowlist entry valid for this call*. The result: `/etc/foo` is checked against an allowlist that has just been extended with `/etc/foo` itself — tautologically passing. `doctor` calls `resolve_scratch_root(output_dir)` positionally with no kwarg, so the allowlist remains the default 2-entry tuple and `/etc/foo` is correctly rejected.

**Evidence**:

- `commands.py:1472-1477` (eval_run): the call site reads
  ```python
  resolved_output = resolve_scratch_root(
      requested_output,
      config=base_config,
      output_dir=output_dir,   # <-- bug: extends allowlist with the very path being checked
  )
  ```
- `commands.py:815-823` (doctor): the call site reads
  ```python
  if output_dir is not None:
      try:
          resolve_scratch_root(output_dir)        # positional; no output_dir kwarg
      except ScratchRootViolation as exc: ...
  ```
- `config.py:219-220` (resolve_scratch_root): when `output_dir` kwarg is non-None it is appended to the allowlist:
  ```python
  if output_dir is not None:
      allowed.append(_resolve_prefix(Path(output_dir)))
  ```
- `config.py:225-229`: the check `resolved == prefix or resolved.is_relative_to(prefix)` then trivially matches because `resolved` (the candidate) and `prefix` (the just-appended `output_dir`) are the same path.
- `scratch-roots.md:19-20`: the `--output-dir <path>` allowlist extension is documented as "extends the allowlist **for the current invocation only**" — intended for downstream sub-path checks (per-eval homes under the operator-supplied root), NOT for self-validating the operator-supplied root itself.

**Reproduction (observation)**: User report is the observation; matches the code paths exactly. No additional repro needed for Tier 1.

**Proposed Fix (provisional)**: Stop passing `output_dir=output_dir` to the *first* `resolve_scratch_root` call in `eval_run`. That first call's purpose is to validate the operator's `--output-dir` against the *default* allowlist, identical to how doctor does it.

**Confidence (agent self-report)**: 0.92

**If I'm wrong it's probably because...**: there is a deliberate design intent that lets `--output-dir` self-authorize (e.g. a "trust the operator" escape hatch). The `scratch-roots.md` policy text contradicts this reading — the call-scoped extension is meant for sub-paths under an *already-validated* root, not the root itself. So a deliberate escape hatch would be a documentation drift bug rather than this code-level bug.

**Risks of fix**: Downstream code in `eval_run` (commands.py:1490-1499) builds a `runtime_allowed` tuple that includes `resolved_output` and `home_root`, so per-eval HOMEs under the validated output_dir still resolve. The fix should not break that downstream path.

# Tier 2 Hypothesis Card — security-engineer

**Brief received**: Original issue + Tier 1 card. Asked to look from a security-first lens.

**Claim**: This is a **policy-bypass vulnerability** classified as **CWE-732 (Incorrect Permission Assignment) / CWE-285 (Improper Authorization) variant**. The `output_dir=output_dir` self-reference at `commands.py:1476` turns the OPS-002 allowlist into a no-op for the `eval run` surface: any operator-supplied `--output-dir` is unconditionally whitelisted by the very call meant to validate it. The four-layer defense documented in `scratch-roots.md:39-52` collapses to one layer (loader-time) for this code path, and the loader can't help because no suite has been loaded yet.

**Severity**: HIGH. The scratch-root policy exists specifically because `claude` runs with operator-supplied hooks + settings inside the per-eval HOME (per `scratch-roots.md:31-37`). A buggy or malicious suite + a tricked operator-supplied `--output-dir` of, e.g., `/root/.ssh`, `/etc/cron.d`, or `~/.claude/` would let cliEval mutate operator state outside the sandbox. The `scratch-roots.md` doc explicitly enumerates this as the reason for the allowlist.

**Evidence**:

- `commands.py:1472-1477` — the smoking gun. `output_dir=output_dir` passes the candidate path as its own validator. The allowlist is extended *with the path under test* before the test runs.
- `config.py:216-220` — the allowlist construction. The user-supplied `output_dir` is appended to the resolved allowlist:
  ```python
  allowed: list[Path] = [_resolve_prefix(p) for p in config.allowed_scratch_roots]
  if output_dir is not None:
      allowed.append(_resolve_prefix(Path(output_dir)))
  ```
- `config.py:225-229` — the comparison loop. With `output_dir` self-appended, the first iteration that touches the appended prefix returns immediately because `resolved == prefix` is trivially true.
- `commands.py:815-823` (doctor, control) — proves the *intended* enforcement. Doctor calls `resolve_scratch_root(output_dir)` positional-only and correctly raises.
- `scratch-roots.md:82-88` — explicitly states that future `eval run` MUST funnel rejections through `format_scratch_root_violation` "the same way" as doctor. This commitment is violated.

**Proposed fix (security-engineer choice)**: Match the doctor pattern. Remove the `output_dir=output_dir` kwarg from the `eval_run` call. The first call to `resolve_scratch_root` in `eval_run` exists to validate the operator-supplied `--output-dir` against the **default** allowlist — exactly what doctor does. Downstream uses of the `output_dir` kwarg (where sub-paths under an already-validated root are checked) are unaffected; that pattern still works for `containment_guard` and friends downstream, because by that point `resolved_output` is known-safe.

**Confidence (agent self-report)**: 0.95

**If I'm wrong it's probably because...**: there's an undocumented intent that `eval run` should accept arbitrary operator-supplied output dirs while doctor is the only enforcement boundary. Reading the docs (`scratch-roots.md:82-88`) and the Wave 0 audit explicitly: there is no such intent. The OPS-002 cross-module consistency requirement names this exact code path as a place that MUST enforce.

**Risks of fix**: Minimal. The change is one-line. Risk register:
- Risk 1: Existing CI uses `--output-dir <non-allowlisted>` and depends on it succeeding. **Likelihood low**: doctor already rejects, so any CI that runs both commands is already broken; if only `eval run` is used, this is exactly the silent-pass bug. **Mitigation**: communicate the fix in release notes; document that `--output-dir` must resolve under `/tmp/eval-runs/` or `<repo>/.dev/eval-runs/`.
- Risk 2: Regression in downstream `runtime_allowed` tuple construction (commands.py:1490-1493). **Likelihood very low**: `runtime_allowed` adds `resolved_output` + `home_root` *after* validation succeeds. If the first call rejects, code never reaches line 1490. No change to that branch.

**Test plan**: Add a regression test asserting `superclaude eval run --output-dir /etc/foo` exits 2 with the policy text printed — mirrors `test_doctor_rejects_non_allowlisted_output_dir`.

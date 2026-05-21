# D-0016 — Implementation notes

## Decisions

1. **Helper lives in `config.py`, not `loader.py`.** The allowlist source
   is `EvalConfig.allowed_scratch_roots`, which already lives in
   `config.py`. Co-locating the policy check next to the policy data
   keeps the "only one source of truth" guarantee structural rather
   than aspirational. (Loader-layer typed errors stay in `loader.py`;
   this is a config-layer policy, not a manifest-validation gate.)

2. **`output_dir` is a kwarg, not a stored config field.** AC12 names
   `--output-dir` as a *per-invocation* override, not a permanent
   widening of the allowlist. Keeping it call-scoped means a doctor
   run cannot accidentally relax future calls inside the same process.
   The test `test_output_dir_is_call_scoped_not_persistent` locks this
   in.

3. **Exit code mirrors the loader trio (= 2).** Operators already learn
   "exit 2 means the harness refused to start"; adding a fourth distinct
   code would dilute that signal. Keeping the constant named separately
   (`SCRATCH_ROOT_VIOLATION_EXIT_CODE`) lets call sites still branch on
   *which* gate fired when logging.

4. **`resolve(strict=False)` over `strict=True`.** M1 outline runs and
   the eval doctor command may evaluate the policy before any scratch
   tree exists. `strict=True` would refuse to resolve a not-yet-created
   directory and force callers to pre-create scratch paths — exactly
   the side effect AC12 forbids.

5. **Equality branch alongside `is_relative_to`.** `Path.is_relative_to`
   returns False when both paths are equal in older Python builds (the
   3.12 stdlib returns True, but staying explicit prevents future
   regressions and documents intent).

## Open follow-ups

* **FR-ISO2 reuse.** `HomeIsolation.setup()` (T02.06) should call
  `resolve_scratch_root` rather than re-implementing the check. That
  wiring lands in Phase 2 — out of scope for T01.19.
* **`eval doctor --json` allowlist surfacing.** The doctor JSON payload
  could include the resolved allowlist for operator sanity. T01.13
  already shipped without it; adding it is non-blocking and tracked
  loosely under OPS-002 (R-policy enforcement) rather than this task.

## What was deliberately left out

* No symlink-following audit in this helper. Symlink attacks are
  caught by `HomeIsolation` AFTER scratch creation (NFR-SEC2 /
  TEST-003), which is the right time to follow them. Doing it here
  would force `resolve_scratch_root` to walk a not-yet-existing tree.
* No `--output-dir` mutation of the stored `EvalConfig`. AC12 calls
  the override per-invocation; folding it into the config would
  silently widen the allowlist for the rest of the run.
* No mention of `~/.claude/` as an explicit reject prefix. The
  general-case allowlist already rejects it; carving out a named
  reject would suggest there are other hidden reject prefixes, which
  is misleading.

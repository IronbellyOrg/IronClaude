# Hypothesis: `eval_run` passes the operator-supplied `--output-dir` back into `resolve_scratch_root` as the `output_dir=` kwarg, turning the OPS-002 allowlist check into a tautology

**Agent**: root-cause-analyst
**Tier**: 1
**Timestamp**: 2026-05-21T05:00:00Z
**Cause class**: Security gate bypass via misuse of an internal API (parameter-aliasing tautology)

## Claim

`resolve_scratch_root(path, *, config, output_dir)` extends its allowlist with `output_dir` when that kwarg is provided. The snapshot `eval_run` at `commands.py:1473-1477` calls `resolve_scratch_root(requested_output, config=base_config, output_dir=output_dir)` — passing the same operator-supplied path as both the candidate AND the kwarg. The allowlist gets extended with `/etc/foo`, then `/etc/foo` is checked against an allowlist that now contains `/etc/foo`, so the check trivially passes. `doctor` at `commands.py:817` calls `resolve_scratch_root(output_dir)` without the kwarg, so its allowlist stays `(/tmp/eval-runs, .dev/eval-runs)` and `/etc/foo` is correctly rejected.

## Evidence

- Snapshot `commands.py:1472-1477` —

  ```python
  resolved_output = resolve_scratch_root(
      requested_output,
      config=base_config,
      output_dir=output_dir,
  )
  ```

  Both `requested_output` and `output_dir` derive from the same Click option (`output_dir if output_dir is not None else _default_output_dir(run_id)`, line 1468-1470).
- Snapshot `commands.py:815-823` (doctor) —

  ```python
  if output_dir is not None:
      try:
          resolve_scratch_root(output_dir)
      ...
  ```

  No `output_dir=` kwarg → allowlist stays canonical → `/etc/foo` raises `ScratchRootViolation`.
- Snapshot `config.py:219-220` (the extension step that bites) —

  ```python
  if output_dir is not None:
      allowed.append(_resolve_prefix(Path(output_dir)))
  ```

- Snapshot `config.py:225-231` (the loop where the tautology completes) —

  ```python
  for prefix in allowed:
      if resolved == prefix or resolved.is_relative_to(prefix):
          return resolved
  raise ScratchRootViolation(candidate, resolved, allowed)
  ```

  When `path == output_dir`, `_resolve_prefix(output_dir) == resolved`, so the first branch (`resolved == prefix`) matches on the appended entry.
- Live (post-fix) `commands.py:1770-1773` and `config.py:203-213` already carry inline comments anti-documenting this exact pattern — confirming the snapshot is the historical pre-fix shape and the fix has the maintainers' explicit blessing.

## Proposed Fix

Drop the `output_dir=output_dir` keyword argument from the `resolve_scratch_root` call at snapshot `commands.py:1473-1477`. The operator-supplied path must be validated as the *candidate*, not as a self-extension of the allowlist. The `output_dir=` kwarg is reserved for **layered** re-checks (e.g. `containment_guard` re-validating after `mkdtemp`) where the path has *already* been gate-validated.

- `src/superclaude/cli/eval/commands.py` — remove `output_dir=output_dir` from the `eval_run` call to `resolve_scratch_root`.

Tests:

- New regression test asserting `superclaude eval run --output-dir /etc/foo --target src/foo` exits 2 with the OPS-002 policy on stderr (mirrors the existing doctor test).

## Confidence

Self-reported: 0.92

Per-dimension:

- Evidence grounding: 1.0 — direct file:line, both call sites quoted, behaviour proven by reading `resolve_scratch_root`.
- Symptom coverage: 1.0 — diff in one kwarg explains both "eval run accepts" and "doctor rejects".
- Reproducibility fit: 1.0 — deterministic; trivial repro.
- Fix directness: 1.0 — drop a keyword arg; 2-line patch.
- Domain coherence: 0.5 — single-domain logic bug, but `--type security` raises the bar (rubric §3).

Skill re-grading: 0.90 (averaged with security caution).

## Risks

- If callers other than `eval_run` and `doctor` rely on the same-path tautology semantics, dropping the kwarg in `eval_run` is still safe — but a broader audit is warranted. Grep for `resolve_scratch_root(.*output_dir=` is the audit query.
- The `output_dir=` kwarg itself remains a sharp tool: `containment_guard` legitimately uses it. Removing the parameter outright (Fix-2 mechanism) is a wider change and is not part of this hypothesis.

## If I'm wrong, it's probably because

The bug is more subtle and the kwarg is intentional — e.g. the design wants the first gate to admit operator paths and rely on a *second* gate (`containment_guard`) to enforce policy. But the doctor's behaviour contradicts that reading: doctor is itself the first-gate enforcer for the same input, and it does NOT pass the kwarg. So the asymmetry is the bug, not the design.

## Alternatives considered

- **`_default_allowed_scratch_roots` regressed** — checked: the defaults are still `(/tmp/eval-runs, .dev/eval-runs)` (`config.py:63-68`). Not the cause.
- **`Path.resolve(strict=False)` symlink trick** — checked: doctor and eval_run share the same resolution code; not the cause.
- **Click default expands `/etc/foo` to a relative path** — checked: the option is `type=click.Path(file_okay=False, path_type=Path)`; absolute paths pass through verbatim.

## Grounding gaps

- Did not execute the snapshot binary; relied on a static read of the snapshot Python plus the live in-repo fixed code.
- Did not enumerate every external caller of `resolve_scratch_root`; the audit query is recorded under Risks.

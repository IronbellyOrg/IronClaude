# Hypothesis: OPS-002 gate is a tautology in `eval_run`; fix is to drop the `output_dir=` kwarg at the first gate

**Agent**: security-engineer
**Tier**: 2
**Timestamp**: 2026-05-21T05:02:00Z
**Cause class**: Security gate bypass via parameter aliasing

## Claim

The snapshot `eval_run` first-gate call extends the AC12 allowlist with the very path it is checking, making the gate vacuous. The fix that matches the design intent is to call `resolve_scratch_root(requested_output, config=base_config)` (no `output_dir=` kwarg) at the first gate. Defense-in-depth re-checks (`containment_guard`) legitimately use `output_dir=` because by then the operator path has already been gate-validated.

## Evidence

- Snapshot `commands.py:1473-1477` — the tautological call.
- Snapshot `commands.py:815-823` — the correct doctor call (no kwarg) which is why doctor rejects `/etc/foo`.
- Snapshot `config.py:219-220` and `225-231` — the extension + loop where the tautology completes.
- Snapshot `scratch-roots.md:62-76` — operator-facing policy explicitly forbids `/etc/foo`; the policy text is the contract the gate must enforce.
- Live `config.py:203-213` (post-fix docstring) — explicitly anti-documents the snapshot's pattern: *"Do NOT pass the raw operator-supplied --output-dir here at the first gate."*

## Proposed Fix

`src/superclaude/cli/eval/commands.py` — at the `eval_run` first-gate call, drop the `output_dir=output_dir` kwarg:

```python
resolved_output = resolve_scratch_root(
    requested_output,
    config=base_config,
)
```

This matches the doctor's gate semantics. The downstream `containment_guard` (`isolation.py:307-318`) still re-checks the resolved path against the allowlist after `mkdtemp`, preserving defense-in-depth.

Test:

- New regression in `tests/cli/eval/test_scratch_root_allowlist.py` (or `test_scratch_root_policy.py`): invoke `eval_run` with `--output-dir /etc/foo` via Click's `CliRunner`, assert exit code 2 and `OPS-002` / `AC12` on stderr.

## Confidence

Self-reported: 0.95

Per-dimension:

- Evidence grounding: 1.0
- Symptom coverage: 1.0
- Reproducibility fit: 1.0
- Fix directness: 1.0
- Domain coherence: 0.5 (security; rubric caution)

## Risks

- **None at the eval_run call site** — the kwarg is dead weight there.
- Watch: any future call site that copies the snapshot pattern. Recommend a `# DO NOT pass the operator path as output_dir=` comment OR a lint rule.

## If I'm wrong, it's probably because

The intended design is that `containment_guard` is the *real* gate and the first call was meant to be a no-op formatter. But that would make the doctor wrong, which contradicts the OPS-002 policy doc.

## Alternatives considered

- Move enforcement entirely into `containment_guard` (Fix-2 territory) — too wide; defense-in-depth wants both layers active.
- Make `resolve_scratch_root` raise if `path == output_dir` — defensive but couples two parameters; cleaner to fix the call site (Fix-1) and add a docstring (already present in live code).

## Grounding gaps

- Did not enumerate every external caller of `resolve_scratch_root` outside the snapshot. Live grep should be part of the regression PR.

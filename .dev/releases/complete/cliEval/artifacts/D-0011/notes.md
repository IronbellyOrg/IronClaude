# D-0011 — design notes

## Why supplementary rows live in `commands.py` instead of `CapabilityGates`

`CapabilityGates` (D-0010 / T01.11) has a frozen roster declared in
`_DEFAULT_CAPABILITY_SPECS` and the T01.11 tests assert that exact set.
The three doctor-specific checks (`claude.min_version`,
`filesystem.claude_home`, `vendored.ptytest`) are FR-CLI4-only and the
T01.11 spec (D-0010 §"Out of scope") explicitly defers them to T01.13.

Putting them in `commands.py` and joining via `_extend_report(base,
extras)` keeps the gates roster stable, keeps the per-check probes
injectable for tests, and preserves the `CapabilityReport` contract so
the JSON payload still satisfies the D-0010 schema.

## ptytest row stays SOFT-SKIP at M1

T01.13 AC requires `superclaude eval doctor` to exit 0 on a clean dev
machine. The vendored ptytest path doesn't exist yet (lands at M2). If
the row were HARD it would fail closed every CI run between T01.13 and
the M2 vendoring task. SOFT-SKIP keeps the row visible in the green
checklist (so reviewers see the missing dependency) without breaking
exit 0.

## `--check-coverage` wiring

Full FR-G5 coverage logic lands in M4 T04.14. The flag is wired now so:

* the human checklist prints `coverage gate: deferred to M4 T04.14`;
* the JSON payload always carries `coverage_gate.{requested,
  status:"deferred", milestone:"M4", task:"T04.14"}` so callers can
  detect both whether the flag was passed and the deferral state.

This means downstream consumers can author manifests / CI rules against
the payload schema today; T04.14 only has to replace `status` with the
real gate outcome.

## Click 8.3 compatibility

The test suite originally used `CliRunner(mix_stderr=False)`. That
kwarg was removed in Click 8.2. Click 8.3+ separates stdout/stderr by
default, so `CliRunner()` + `result.stderr` is the correct pattern. The
doctor tests now use the default constructor.

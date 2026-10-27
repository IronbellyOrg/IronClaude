# D-0042 — Design notes

## Why inject an xfail spec via `capabilities=` instead of monkeypatching the default roster

The default `_DEFAULT_CAPABILITY_SPECS` table has no `xfail` rows today — every default spec is either `hard` or `skip`. The natural way to test xfail support is to monkeypatch `_DEFAULT_CAPABILITY_SPECS` to inject an extra row. **D-0042 deliberately does not do this.**

The `CapabilityGates` constructor already exposes a `capabilities=` keyword precisely for this purpose ("Tests inject a custom spec tuple via the `capabilities` keyword to mock PATH state without monkeypatching `shutil`," per `capabilities.py:233-234`). Using the documented hook keeps the test honest about how a production xfail entry would land — through the same API surface — and prevents accidental coupling to a private implementation detail. If the default roster ever grows an xfail entry, this slice continues to pin the classification surface unchanged.

## Why pin the exact doctor marker strings instead of just checking the failure-bucket routing

`CapabilityGates.check_all()` routes failing rows into `hard_failures` / `soft_skips` / `soft_xfails` — testing that routing alone proves the bucket logic works. But the operator-facing contract is the **rendered checklist line** that a human reads in CI output:

```
  [XX] Claude CLI on PATH (HARD) -- not found on PATH
  [--] Auggie MCP server reachable (SOFT-SKIP) -- MCP server binary not on PATH
  [--] Auggie MCP server reachable (skipped by flag) -- /opt/auggie
  [??] Optional xfail probe (xfail) -- not found on PATH
  [ok] Claude CLI on PATH -- /usr/bin/claude
```

Each glyph + tag pair is a distinct visual signal. If `_row_marker()` ever drifted (e.g. someone changed `[XX]` to `[!!]` to "make it look prettier"), the bucket-routing tests would still pass but operators would silently lose the visual disambiguation. The marker-string assertions catch that class of regression directly.

## Why test the `--no-mcp` override against BOTH passing and failing probes

A naïve `--no-mcp` test only covers one branch: probe fails AND flag is active → row in `soft_skips`. But the *override semantics* the design-spec promises is "force soft-skip regardless of probe result." Two tests are therefore needed:

1. Probe passes (via injected `mcp_probe`) + flag active → row STILL in `soft_skips` with `skipped_by_flag=True`. Proves the flag overrides a green probe.
2. Probe fails (binary absent) + flag active → row in `soft_skips`. Proves the flag's behaviour is consistent when the probe agrees.

If `--no-mcp` ever regressed to "skip only when the probe also fails," test (1) would fail. If it regressed to "ignore the probe and always set `skipped_by_flag=True` regardless of probe result, even when probe passes", the `passed=False` assertion in test (1) would still hold because the override forces `passed=False` — but the `skipped_by_flag=True` assertion would catch any drift to "ignore the flag entirely."

## Why pin `HARD_FAIL_EXIT_CODE` as `== 2` only transitively (via `CliRunner.exit_code`)

`test_doctor.py` already imports and references `HARD_FAIL_EXIT_CODE` directly. D-0042 imports the same constant and uses it in `CliRunner.exit_code` assertions — the constant's value (2) is pinned by `HARD_FAIL_EXIT_CODE` in `commands.py`, not by a literal `== 2` here. This keeps the spec-level "exit 2 on HARD failure" contract enforced exactly once (in `test_doctor.py::test_cli_doctor_exits_two_when_hard_capability_missing` via direct integer comparison there); D-0042's role is to pin the *classification-to-exit-code* mapping, not the integer value.

If a future change reroutes HARD failures through a different exit-code constant, both this module and `test_doctor.py` will fail in the same PR, making the regression obvious. Pinning the literal `2` in two places would create a maintenance burden without adding signal.

## Why the doctor-end-to-end test re-invokes with `--no-mcp` instead of asserting both markers in one run

The default doctor run already includes a `vendored.ptytest` SOFT-SKIP row (M2-deferred per `_check_ptytest_vendored`), so `(SOFT-SKIP)` will appear in the output regardless of MCP probe results. To prove that `(skipped by flag)` *specifically* renders when `--no-mcp` is active, the test re-invokes with the flag and asserts the override marker appears AND the `skip flags: --no-mcp` line appears. This isolates the two markers cleanly across two runs rather than relying on which row happened to use which marker in a combined run.

## Why a coverage-pin meta-test

`test_test_004_slice_coverage_is_complete` walks the AC bullet list and asserts each has a corresponding test class in the module. This is overkill for a 4-class module — but the same pattern is used in D-0040 (4 test classes) and D-0041 (4 test classes), and uniformity matters more than minimal cost. The cost is one assertion; the value is forcing future AC additions to land with their tests in the same PR.

## Sibling regression

After landing this module, the five-module capability family (`test_capability_classifications.py` + `test_capability_gates.py` + `test_capability_dataclass.py` + `test_capability_report.py` + `test_doctor.py`) runs clean at **92 passed in 0.22s**. No drift in sibling deliverables.

## Verification method

T02.23 is STANDARD tier with `Verification Method: Direct test execution` and `Sub-Agent Delegation: None`. Per phase-2-tasklist: "Run `uv run pytest tests/cli/eval/test_capability_classifications.py -v`." Evidence log captures the 20-passed result.

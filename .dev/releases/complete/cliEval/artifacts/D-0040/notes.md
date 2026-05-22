# D-0040 — Design notes

## Why use real canonical roots instead of a narrowed test config

The natural way to write these tests is to construct an `EvalConfig(allowed_scratch_roots=(tmp_path,))` and point the scratch root at that tempdir — clean, hermetic, no filesystem pollution. **D-0040 deliberately does not do this.**

The TEST-002 AC bullets cite `/tmp` and the repo `.dev` directory *by name*. The contract being pinned is not "the allowlist works" (D-0029 already pins that). The contract is **"the default `EvalConfig()` allowlist contains exactly these two canonical roots."** If a future refactor accidentally removed `/tmp/eval-runs` from the default, every test in this repo using a narrowed allowlist would still pass — but the harness would no longer match the operator-facing documentation that says "drop your eval there." D-0040 binds the test to the default config so that drift surfaces immediately.

The cost is a `tmp_eval_runs_subdir` fixture that creates a real `/tmp/eval-runs/test-containment-<uuid>` directory and tears it down in `finally:`. The `<uuid>` suffix prevents collision with concurrent test workers and live eval runs. Cleanup uses `shutil.rmtree(..., ignore_errors=True)` so a leaked HomeIsolation handle inside a failed test doesn't break the fixture teardown.

## Why pin exit codes as `== 2` literals

`INVALID_EVAL_ID_EXIT_CODE` and `SCRATCH_ROOT_VIOLATION_EXIT_CODE` are exported constants — the obvious test is `assert INVALID_EVAL_ID_EXIT_CODE == SCRATCH_ROOT_VIOLATION_EXIT_CODE`. That asserts *consistency* but not *value*. The operator-facing contract is "rejections from the containment system exit with code 2"; if both constants drifted to `3` together, the consistency check would still pass but the contract would silently break. D-0040 includes three exit-code assertions:

1. `INVALID_EVAL_ID_EXIT_CODE == 2` (literal pin)
2. `SCRATCH_ROOT_VIOLATION_EXIT_CODE == 2` (literal pin)
3. The two are aligned with each other (consistency pin)

All three must hold simultaneously. Any single one being false catches a different class of regression.

## Why patch `__post_init__` instead of `validate_eval_id` for the loader-bypass second-layer test

The second-layer test (`test_direct_construction_with_post_init_disabled_is_caught_by_guard`) needs to prove `containment_guard` still catches a bad `eval_id` even when the constructor's check has been bypassed. The naïve approach is `monkeypatch.setattr(loader, "validate_eval_id", lambda *_: None)`. **D-0040 does not do this** — that would patch the function *both* in `__post_init__` *and* in `containment_guard`, so the test would prove nothing about layered defense (both layers would be disabled simultaneously).

Instead, D-0040 patches `HomeIsolation.__post_init__` to a slot-only initializer (assigning only `_home_path` via `object.__setattr__`). This disables *only* the constructor check; `containment_guard`'s own `validate_eval_id` call inside `setup()` still runs unmodified. The test then confirms the guard catches the bad id at `setup()` time. The two defense layers remain genuinely independent.

## Why parametrize FR-SCH2-rejected ids in the loader-bypass slice

Ten parametrized cases (`../escape`, `/etc/passwd`, `E1/with/sep`, `..`, `9bad`, ``, `with spaces`, `{{template}}`, `${shell}`, `E1\nE2`) cover the FR-SCH2 rejection regex from multiple angles:
- **Path separators**: `../escape`, `/etc/passwd`, `E1/with/sep`, `..` — would escape the tempdir if mkdtemp ran
- **Lowercase first char**: `9bad` — violates the `^[A-Z]` anchor
- **Empty / whitespace**: ``, `with spaces` — bypasses tokenization
- **Template / shell metacharacters**: `{{template}}`, `${shell}` — defends against injection if the id ever reaches a shell
- **Control characters**: `E1\nE2` — defends against log/file-format injection

Each is a single AC case (`AC4 — loader-bypass rejected`), but the parametrization shape means a future regex relaxation that allowed, say, lowercase first chars would break exactly one parametrized case, making the regression obvious.

## Why a coverage-pin meta-test

`test_test_002_slice_coverage_is_complete` walks the AC bullet list and asserts each has a corresponding test class in the module. This is overkill for a 4-class module — but the same pattern is used in D-0030 (5 vector classes), and uniformity matters more than minimal cost. The cost is one assertion; the value is forcing future AC additions to land with their tests in the same PR.

## Sub-agent review checkpoint

T02.21 is STRICT tier with `Sub-Agent Delegation: Required` (quality-engineer). Per phase-2-tasklist: "Run `uv run pytest tests/cli/eval/test_containment.py -v` + sub-agent review." The pytest run is in `evidence.md`; sub-agent review note attached there.

## Sibling regression

After landing this module, the four-module containment family (`test_containment.py` + `test_defense_in_depth.py` + `test_path_containment.py` + `test_scratch_root_allowlist.py`) runs clean at **115 passed in 0.26s**. No drift in sibling deliverables.

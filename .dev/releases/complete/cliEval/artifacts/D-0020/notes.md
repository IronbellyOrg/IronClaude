# D-0020 — implementation notes

## Why TEST-001 is a first-class deliverable

T01.04 (FR-SCH1), T01.05 (FR-SCH2), T01.07 (COMP-002), and T01.08
(NFR-SEC1) each own a slice of the loader-layer security model. Their
function-surface tests verify the slice in isolation. TEST-001 is the
**integration matrix** that ties those slices together at the CLI
boundary so the operator-visible contract — "harness exits 2 with a
typed error class on stderr and no FS writes before rejection" — is
verified end-to-end.

The matrix-style approach means a single CI failure in
`test_schema_id_rejection.py` surfaces a regression in any of the four
upstream tasks. The docstring on every test names the FR / NFR ID, so
the failing test log identifies the failing gate without requiring a
cross-suite lookup.

## CLI-surface vs function-surface coverage

TEST-001 invokes the CLI through `click.testing.CliRunner` rather than
spawning a real subprocess. The CliRunner-based approach is consistent
with the patterns established by `test_describe.py` and `test_list.py`
(T01.21 / T01.22) and avoids the cost of spinning up a subprocess
per-test on a hot path. The exit-code contract is verified by
`result.exit_code` against the canonical exit-code constants exported
from `superclaude.cli.eval`.

## Mocking strategy for the post-expansion re-check

The "unsafe parameterize expansion" test mocks `_expand_entry` so the
test can simulate a hostile (or buggy) expansion strategy without
introducing a malicious fixture. The current `.{index}` expansion
convention is safe by construction; the test exists to pin the
load-bearing invariant that the loader applies `validate_eval_id`
AFTER expansion, not just before. A future change to the expansion
strategy (e.g., named indices, parameter-driven suffixes) cannot
silently bypass the re-check without tripping this test.

## Snapshot baseline strategy

The NFR-SEC1 invariant tests use two snapshot mechanisms:

1. Per-test `tmp_path` snapshot — captured via the `sandbox_snapshot`
   fixture that yields `(sandbox_path, baseline_set)`. Tests compare
   `set(rglob("*"))` before and after; an empty delta confirms no
   writes leaked into the per-test sandbox.
2. Default scratch root (`/tmp/eval-runs`) snapshot — captured via the
   module-level `_scratch_snapshot()` helper. The directory is not
   guaranteed to exist on a clean dev box, so an empty set is treated
   as a valid baseline. Only the *delta* matters.

The two snapshots complement each other: the per-test sandbox catches
leaks into the test's own working directory (e.g., a stray
`Path.write_text(...)` against a relative path), and the scratch-root
snapshot catches leaks into the production default location.

## Reuse vs duplication

`test_path_traversal.py` (T01.08) already contains the
per-named-case NFR-SEC1 checklist. TEST-001 deliberately re-runs a
subset of those cases through a single parametrized test so the
TEST-001 file has a self-contained assertion for each AC bullet —
T01.23's AC text reads "tests for schema-violation rejection, unsafe
id rejection, parameterize expansion validated post-expansion, and
pre-flight ordering", which implies an in-file checklist. The
duplication is bounded (one parametrized case in TEST-001 vs seven
individual tests in T01.08) and the trade is intentional.

## CLI rejection surfaces covered

| Command | Test |
|---|---|
| `eval describe --suite <broken>` | `test_schema_violation_cli_describe_exits_two`, `test_unsafe_id_cli_describe_exits_two`, `test_no_fs_write_when_cli_describe_rejects` |
| `eval list --suites-dir <broken>` | `test_schema_violation_cli_list_exits_two` |

`eval doctor` is not covered here because doctor does not load suite
manifests; its rejection surface is the capability gate (covered by
`test_doctor.py`, T01.13).

## Open follow-ups

None. The 20-case suite passes green on first run and the full
`tests/cli/eval/` suite expanded from 299 → 319 passing with zero
regressions. Spec / notes / evidence artefacts are produced inline
with the test module.

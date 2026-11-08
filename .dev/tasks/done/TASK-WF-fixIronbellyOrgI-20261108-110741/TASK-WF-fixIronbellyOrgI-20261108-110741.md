---
schema: workflow-plan/1.2
source: ./source.md
strategy: systematic
depth: standard
slug: TASK-WF-fixIronbellyOrgI-20261108-110741
version: "1"
priority: Medium
created_date: "2026-11-08"
---

# Keep ccsession test shim ports clear of the stand-in gateway port (#443)

Source: ./source.md
Goal: No test in tests/unit/test_ccsession_tiers.py can pair a stand-in gateway with a shim base port that ccsession refuses as "a ccsession shim address", and a failing launch names both ports.

## Constraints

- Change only tests/unit/test_ccsession_tiers.py. Do not change src/superclaude/skills/ccsession-tag/models.py or src/superclaude/skills/ccsession-tag/ccsession: the refusal is the documented launcher contract (REPORT.md, Documentation Context).
- Leave the `shim` fixture pairing at tests/unit/test_ccsession_tiers.py:766-767, the line at :1075 and the gateway at :2098 unchanged (source.md).
- The forbidden windows are defined by `models.shim_upstream_problem(url, base)` (models.py:822-844): a gateway port 0..97 above `base + 101*k`, k in 0..5. Use that function; do not re-implement the window arithmetic in the test.
- Out of scope, record only: the `_real_launch` environment leak (test:1680 copies os.environ, :1689 removes only CC_SHIM_PORT), ccsession:985 treating every rc==1 as a refusal, the remaining #352 port races, and the 30 CI runs.
- pytest-xdist is not installed locally; CI installs it with `uv pip install "pytest-xdist>=3.5,<4"` (.github/workflows/test.yml:29). Install it the same way for the parallel runs; do not add it to pyproject.toml or uv.lock.
- UV only (`uv run ...`). Evidence goes under ./artifacts/ in this package.

## Phase 1: Make a refused launch name both ports

## Task 1: Print gateway_port, shim_base_port and upstream in the `_real_launch` failure message

In `_real_launch` (tests/unit/test_ccsession_tiers.py:1669-1704), read the upstream URL into a local variable before `extra.pop("upstream")` at :1684 and use that variable for ANTHROPIC_BASE_URL. Replace the bare message of `assert proc.returncode == 0, proc.stderr` at :1702 with one that starts `gateway_port=<port> shim_base_port=<port> upstream=<url>` and then the full stderr. The gateway port is the port parsed from the upstream URL (`urllib.parse.urlsplit`); the shim base port is the `port` argument. Each value that is missing or cannot be parsed prints as `unobserved` (for example `shim_base_port=unobserved` when `port` is None). Add `import urllib.parse` to the import block (:10-26) if it is not already importable there.

Acceptance criteria:
- A launch with a non-zero exit fails with an AssertionError whose message contains `gateway_port=`, `shim_base_port=`, `upstream=` and the launcher stderr; with `port=None` it contains `shim_base_port=unobserved`.
- The environment `_real_launch` passes to ccsession is unchanged (same keys and values as before for every caller).
- `uv run pytest tests/unit/test_ccsession_tiers.py -q -p no:cacheprovider -k "busy_shim or tiers_off_launch or upgraded_code or relative_defaults or every_shim_launch"` passes; output saved to ./artifacts/t1-pytest.log.

## Phase 2: Add the bounded port helper

## Task 2: Add `_free_port_clear_of(gateway_url)` and its unit tests

Depends on: Task 1

Add `_free_port_clear_of(gateway_url: str) -> int` directly after `_free_port` (tests/unit/test_ccsession_tiers.py:757-760). It calls the module-level `_free_port()` (looked up at call time, so a test can monkeypatch it) up to a fixed bound held in a module constant (50 tries), returns the first port for which `models.shim_upstream_problem(gateway_url, port) == ""`, and otherwise fails loudly with `pytest.fail` naming the gateway URL, the bound and the rejected ports. A one-line comment says why it exists (#443: the gateway and shim ports come from separate random binds). `models` is already imported at :33.

Add two tests next to the helper's other users (after `_real_launch`):
- rejected then accepted: monkeypatch `_free_port` to return first a port inside window k=0 of a fixed gateway URL (gateway port minus 5), then an accepted port; assert the helper returns the second value, called `_free_port` exactly twice, and that `models.shim_upstream_problem` is non-empty for the first value.
- loud-failure bound: monkeypatch `_free_port` to always return an in-window port; assert the helper raises pytest's fail exception, the message names the gateway URL, and `_free_port` was called exactly the bound number of times.

Acceptance criteria:
- `_free_port_clear_of` exists in tests/unit/test_ccsession_tiers.py, uses `models.shim_upstream_problem`, and contains no window arithmetic of its own.
- Both new tests pass: `uv run pytest tests/unit/test_ccsession_tiers.py -q -p no:cacheprovider -k free_port_clear_of`; output saved to ./artifacts/t2-pytest.log.

## Phase 3: Use the helper at every gateway and shim pairing

## Task 3: Replace `_free_port()` at the four `_real_launch` pairing sites

Depends on: Task 2

In tests/unit/test_ccsession_tiers.py, at each site below the `StandInGateway()` is already created before the port, so replace `port = _free_port()` with `port = _free_port_clear_of(gateway.url)`:
- :1714 in `test_a_busy_shim_is_never_stopped_by_a_new_launch` (gateway at :1712)
- :2076 in `test_tiers_off_launch_never_takes_over_a_tier_shim` (gateway at :2075)
- :2119 in `test_upgraded_code_starts_a_new_shim_and_keeps_the_old` (gateway at :2118)
- :2146 in `test_relative_defaults_path_keeps_each_directory_on_its_own_shim` (gateway at :2145)

Acceptance criteria:
- None of these four tests calls `_free_port()` directly for its shim base port; each uses `_free_port_clear_of(gateway.url)`.
- The fixture at :766-767, the line at :1075 and the gateway at :2098 are unchanged (`git diff` shows no hunk there).
- `uv run pytest tests/unit/test_ccsession_tiers.py -q -p no:cacheprovider -k "busy_shim or tiers_off_launch or upgraded_code or relative_defaults"` passes; output saved to ./artifacts/t3-pytest.log.

## Task 4: Cover the two hand-built launch sites

Depends on: Task 2

These two tests set CC_SHIM_PORT and ANTHROPIC_BASE_URL themselves instead of calling `_real_launch` (REPORT.md, Proposed Fix note), so a collision there does not reach the :1702 message.
- `test_shim_outlives_the_terminal_that_started_it` (:1779): the port is taken at :1796 before the gateway is created at :1806. Move `gateway = StandInGateway()` above the port line and replace `port = _free_port()` with `port = _free_port_clear_of(gateway.url)`; keep `env["ANTHROPIC_BASE_URL"] = gateway.url` and the existing try/finally that stops the gateway, so the gateway is still stopped on every path (if the move puts gateway creation outside the try, make sure no statement between creation and the try can raise without stopping it).
- `test_launch_never_attaches_to_a_shim_that_won_the_port_race` (:2270): the gateway is at :2281; replace `port = _free_port()` at :2282 with `port = _free_port_clear_of(gateway.url)`.

Acceptance criteria:
- Both tests take their shim base port from `_free_port_clear_of(gateway.url)` with the gateway created first.
- The gateway in `test_shim_outlives_the_terminal_that_started_it` is still stopped in a finally block.
- `uv run pytest tests/unit/test_ccsession_tiers.py -q -p no:cacheprovider -k "outlives_the_terminal or won_the_port_race"` passes; output saved to ./artifacts/t4-pytest.log.

## Phase 4: Prove the fix

## Task 5: Add the forced-collision regression test and record the run evidence

Depends on: Task 3, Task 4

Add `test_forced_in_window_shim_port_is_skipped` to tests/unit/test_ccsession_tiers.py, modelled on the scratch reproduction /tmp/issue443-repro/test_forced_collision.py (recorded in .dev/issues/443/handoff-repro.md). With monkeypatch it wraps `StandInGateway` to record the gateway port and makes the first `_free_port()` call return the gateway port minus 5 (inside window k=0); later calls use the real `_free_port`. It asserts `models.shim_upstream_problem(gateway_url, forced_port)` is non-empty (the old pairing would be refused, as ccsession:986 did in handoff-repro.md) and then runs `test_a_busy_shim_is_never_stopped_by_a_new_launch(tmp_path)`, which must pass because the helper skips the forced port.

Before evidence: copy the reproduction command and output from .dev/issues/443/handoff-repro.md into ./artifacts/t5-before.md (gateway_port=33361, forced_base=33356, the "is a ccsession shim address" refusal). After evidence: run the new test.

Acceptance criteria:
- The new test passes: `uv run pytest tests/unit/test_ccsession_tiers.py -q -p no:cacheprovider -k forced_in_window`; output saved to ./artifacts/t5-after.log. ./artifacts/t5-before.md holds the old-pairing refusal.
- Parallel runs: after `uv pip install "pytest-xdist>=3.5,<4"`, five runs of `uv run pytest tests/unit/test_ccsession_tiers.py -q -p no:cacheprovider -n auto` and one serial run of `uv run pytest tests/unit/test_ccsession_tiers.py -q -p no:cacheprovider` all pass; ./artifacts/t5-runs.md lists each run's passed/failed/skipped counts and duration.
- `make lint` (or `uv run ruff check tests/unit/test_ccsession_tiers.py` and `uv run ruff format --check tests/unit/test_ccsession_tiers.py`) and `make verify-sync` pass; output saved to ./artifacts/t5-lint.log.
- `git diff --name-only` lists only tests/unit/test_ccsession_tiers.py outside .dev/.

"""REAL end-to-end tests that run the ACTUAL swarm pipeline against the LIVE T2
proxy, making REAL model calls that spend REAL tokens.

This is the opposite of ``test_e2e_user_guide.py`` (which uses the deterministic,
network-free ``stub`` transport). Here every test drives ``--transport
openai_compat`` against the live proxy defined in ``~/.aienv``:

  * Endpoint : ``T2ProxyUrl`` + ``/v1`` (the user-authorized OpenAI-compatible
               path under ``:4000/cli``). The harness/runner sets
               ``T2ProxyUrl=http://192.168.133.101:4000/cli/v1``.
  * Key      : ``T2ProxyKey`` from ``.aienv``.
  * Models   : ``T2Model0N`` from ``.aienv`` (kimi-k2.6 / qwen3.6-plus / glm-5.1
               / deepseek-v4-pro). NEVER queried from the proxy API.

These tests are **gated** and SKIP unless ``SWARM_REAL_E2E=1`` is set AND the
proxy contract env is present — so CI / normal ``pytest`` runs stay hermetic.
Run them deliberately via ``scripts/run_swarm_real_e2e.sh``.

Ground truth established live (2026-06-09):
  * Per-worker model differentiation IS wired: the openai_compat factory binds
    worker slot i to the env pool model at ``pool[i % len(pool)]`` (one
    ``OpenAICompatTransport`` per ``T2Model0N`` slot). The single-model tests
    below use ``pin_model`` (pool of 1 → every slot same model); the
    ``pin_pool`` tests assert an N-worker job covers all N pool models.
  * ``qwen3.6-plus`` (~6 s) and ``deepseek-v4-pro`` (~32 s) reliably return
    HTTP 200 with real content on the full lens prompts. (kimi/glm 400 on some
    assembled prompts — real model-specific sensitivity, not a swarm bug.)
  * ``swarm run`` is dispatch-only today: it writes execution-log.{jsonl,md},
    manifest.json, .swarm-state.json. Worker *content* is not persisted to disk
    in this mode (the log records status/http_code/elapsed_ms but ``bytes`` is
    None) — so content-level proof is done at the transport layer (the first
    two tests), and pipeline tests assert on real status/http/latency.
"""

from __future__ import annotations

import json
import os
from pathlib import Path

import pytest
from click.testing import CliRunner

from superclaude.cli.swarm import swarm_group
from superclaude.cli.swarm.commands import (
    EXECUTION_LOG_JSONL_FILENAME,
    EXIT_OK,
    SWARM_STATE_FILENAME,
    TERMINAL_STATE_VALUE,
)

MANIFEST_FILENAME = "manifest.json"

# Models from .aienv that reliably do real work on full lens prompts.
MODEL_FAST = "qwen3.6-plus"  # ~6 s
MODEL_REASONER = "deepseek-v4-pro"  # ~32 s

# Latency floor that proves a real network round-trip (the stub transport
# returns in ~0 ms; any real proxy call is far above this).
REAL_LATENCY_FLOOR_MS = 300

# ---------------------------------------------------------------------------
# Gating: skip the whole module unless explicitly opted in AND env present.
# ---------------------------------------------------------------------------
_REASONS = []
if os.environ.get("SWARM_REAL_E2E") != "1":
    _REASONS.append("set SWARM_REAL_E2E=1 to run real-proxy tests")
if not os.environ.get("T2ProxyKey"):
    _REASONS.append("T2ProxyKey (from .aienv) not set")
if not os.environ.get("T2ProxyUrl"):
    _REASONS.append("T2ProxyUrl (from .aienv) not set")

pytestmark = pytest.mark.skipif(bool(_REASONS), reason="; ".join(_REASONS))


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------
@pytest.fixture()
def runner() -> CliRunner:
    return CliRunner()


@pytest.fixture()
def pin_model(monkeypatch):
    """Return a function that pins T2Model01 to a chosen .aienv model and
    clears the rest, so the shared-transport binds that model for all workers.

    Also normalizes T2ProxyUrl to the authorized ``/cli/v1`` OpenAI path if the
    sourced value is the bare ``/cli`` base (so the test works whether the
    runner already appended ``/v1`` or not). Only ``.aienv`` values are used.
    """

    def _pin(model: str) -> None:
        url = os.environ.get("T2ProxyUrl", "")
        if url.rstrip("/").endswith("/cli"):
            url = url.rstrip("/") + "/v1"
        monkeypatch.setenv("T2ProxyUrl", url)
        monkeypatch.setenv("T2Model01", model)
        for i in range(2, 10):
            monkeypatch.delenv(f"T2Model0{i}", raising=False)

    return _pin


@pytest.fixture()
def pin_pool(monkeypatch):
    """Return a function that pins T2Model01..0N to an ORDERED list of .aienv
    models (clearing the rest) and normalizes T2ProxyUrl to /cli/v1.

    This is the multi-model-pool counterpart to ``pin_model``: it lets a test
    assert per-worker model differentiation — the swarm openai_compat factory
    binds worker slot i to pool[i % len(pool)], so an N-worker job over an
    N-model pool uses all N models, one per slot.
    """

    def _pin(models: list[str]) -> None:
        url = os.environ.get("T2ProxyUrl", "")
        if url.rstrip("/").endswith("/cli"):
            url = url.rstrip("/") + "/v1"
        monkeypatch.setenv("T2ProxyUrl", url)
        for i in range(1, 10):
            key = f"T2Model0{i}"
            if i <= len(models):
                monkeypatch.setenv(key, models[i - 1])
            else:
                monkeypatch.delenv(key, raising=False)

    return _pin


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def _worker_done(out: Path) -> list[dict]:
    events = []
    for line in (out / EXECUTION_LOG_JSONL_FILENAME).read_text().splitlines():
        if not line.strip():
            continue
        r = json.loads(line)
        if r["event_type"] == "worker_done":
            events.append(r["payload"])
    return events


def _run_lens(runner: CliRunner, lens: str, target: Path, out: Path):
    return runner.invoke(
        swarm_group,
        [
            "run",
            "--lens",
            lens,
            "--target",
            str(target),
            "--output",
            str(out),
            "--transport",
            "openai_compat",
        ],
    )


def _write(tmp_path: Path, name: str, body: str) -> Path:
    p = tmp_path / name
    p.write_text(body)
    return p


# Real targets (each >= 50 non-whitespace bytes so they clear IMM-4).
BUGGY_CODE = (
    "def binary_search(arr, target):\n"
    "    lo, hi = 0, len(arr)\n"
    "    while lo < hi:\n"
    "        mid = (lo + hi) // 2\n"
    "        if arr[mid] == target:\n"
    "            return mid\n"
    "        elif arr[mid] < target:\n"
    "            hi = mid          # BUG: should be lo = mid + 1\n"
    "        else:\n"
    "            hi = mid\n"
    "    return -1\n"
)
SPEC_DOC = (
    "# Rate Limiter Spec\n\n"
    "The service MUST limit each API key to 100 requests per minute.\n"
    "Requests over the limit return HTTP 429. The window is fixed.\n"
    "Open question: behavior on clock skew is unspecified.\n"
)
PROPOSAL = (
    "# Proposal: migrate session store from Postgres to Redis\n\n"
    "We will move all session reads/writes to Redis for sub-ms latency,\n"
    "keeping Postgres as the system of record, synced asynchronously.\n"
)
FAILURE_DESC = (
    "Symptom: the nightly ETL job intermittently writes duplicate rows.\n"
    "It started after we added a retry wrapper around the batch insert.\n"
    "No unique constraint exists on the staging table. Logs show 2 inserts.\n"
)
DOC_TEXT = (
    "## Installation\n\n"
    "Run `pip install widget`. Then import it. The configure() step is\n"
    "required but undocumented; users routinely miss the API key argument.\n"
)


# ---------------------------------------------------------------------------
# Transport-level: prove REAL model content comes back (spends tokens).
# ---------------------------------------------------------------------------
@pytest.mark.parametrize("model", [MODEL_FAST, MODEL_REASONER])
def test_transport_returns_real_content(model, pin_model):
    """OpenAICompatTransport.send() against the live proxy returns a real,
    non-empty completion (HTTP 200, real latency, real body)."""
    pin_model(model)
    from superclaude.cli.swarm.transports.openai_compat import (
        OpenAICompatTransport,
        read_env,
    )

    cfg = read_env()
    assert cfg.models and cfg.models[0] == model
    transport = OpenAICompatTransport(
        base_url=cfg.base_url, api_key=cfg.api_key, model=cfg.models[0]
    )
    result = transport.send(
        "Reply with one short sentence describing what a binary search does.",
        timeout=120,
    )
    assert result.status == "success", f"{model}: {getattr(result, 'body', '')[:200]}"
    assert result.http_code == 200
    assert result.elapsed_ms >= REAL_LATENCY_FLOOR_MS
    body = getattr(result, "body", "") or ""
    assert body.strip(), f"{model} returned empty content"


# ---------------------------------------------------------------------------
# Pipeline-level: real fan-out across each lens (spends tokens per worker).
# ---------------------------------------------------------------------------
def _assert_real_success(result, out: Path, expected_workers: int):
    assert result.exit_code == EXIT_OK, result.output
    assert "dispatched job" in result.output
    done = _worker_done(out)
    assert len(done) == expected_workers, (
        f"expected {expected_workers} workers, got {len(done)}"
    )
    assert all(d["status"] == "success" for d in done), [d["status"] for d in done]
    assert all(d["http_code"] == 200 for d in done), [d["http_code"] for d in done]
    # at least one worker shows real network latency (not a stub's ~0 ms)
    assert max(d["elapsed_ms"] for d in done) >= REAL_LATENCY_FLOOR_MS
    # standard dispatch-only artifacts present + terminal state
    assert (out / MANIFEST_FILENAME).exists()
    state = json.loads((out / SWARM_STATE_FILENAME).read_text())
    assert state["state"] == TERMINAL_STATE_VALUE


def test_bare_review_real_fanout(runner, pin_model, tmp_path):
    """bare-review across 3 real qwen workers — all succeed with HTTP 200."""
    pin_model(MODEL_FAST)
    out = tmp_path / "out"
    r = _run_lens(runner, "bare-review", _write(tmp_path, "t.py", BUGGY_CODE), out)
    _assert_real_success(r, out, expected_workers=3)


def test_refactor_find_real(runner, pin_model, tmp_path):
    """refactor-find real fan-out (3 workers)."""
    pin_model(MODEL_FAST)
    out = tmp_path / "out"
    r = _run_lens(runner, "refactor-find", _write(tmp_path, "t.py", BUGGY_CODE), out)
    _assert_real_success(r, out, expected_workers=3)


def test_edge_case_hunt_real_four_workers(runner, pin_model, tmp_path):
    """edge-case-hunt real fan-out — defaults to 4 workers."""
    pin_model(MODEL_FAST)
    out = tmp_path / "out"
    r = _run_lens(runner, "edge-case-hunt", _write(tmp_path, "t.py", BUGGY_CODE), out)
    _assert_real_success(r, out, expected_workers=4)


def test_spec_completeness_real(runner, pin_model, tmp_path):
    """spec-completeness real fan-out on a real spec doc."""
    pin_model(MODEL_FAST)
    out = tmp_path / "out"
    r = _run_lens(
        runner, "spec-completeness", _write(tmp_path, "spec.md", SPEC_DOC), out
    )
    _assert_real_success(r, out, expected_workers=3)


def test_feasibility_probe_real(runner, pin_model, tmp_path):
    """feasibility-probe real fan-out on a real proposal."""
    pin_model(MODEL_FAST)
    out = tmp_path / "out"
    r = _run_lens(runner, "feasibility-probe", _write(tmp_path, "p.md", PROPOSAL), out)
    _assert_real_success(r, out, expected_workers=3)


def test_troubleshoot_hypothesis_real_four_workers(runner, pin_model, tmp_path):
    """troubleshoot-hypothesis real fan-out — defaults to 4 workers."""
    pin_model(MODEL_FAST)
    out = tmp_path / "out"
    r = _run_lens(
        runner, "troubleshoot-hypothesis", _write(tmp_path, "f.txt", FAILURE_DESC), out
    )
    _assert_real_success(r, out, expected_workers=4)


def test_doc_completeness_real(runner, pin_model, tmp_path):
    """doc-completeness real fan-out on real docs."""
    pin_model(MODEL_FAST)
    out = tmp_path / "out"
    r = _run_lens(runner, "doc-completeness", _write(tmp_path, "d.md", DOC_TEXT), out)
    _assert_real_success(r, out, expected_workers=3)


def test_reasoner_model_real_pipeline(runner, pin_model, tmp_path):
    """A second real .aienv model (deepseek-v4-pro) drives a full pipeline —
    proves the suite isn't bound to a single model."""
    pin_model(MODEL_REASONER)
    out = tmp_path / "out"
    r = _run_lens(runner, "bare-review", _write(tmp_path, "t.py", BUGGY_CODE), out)
    _assert_real_success(r, out, expected_workers=3)


def test_manifest_records_real_openai_compat_run(runner, pin_model, tmp_path):
    """The manifest of a real run records transport_kind=openai_compat and a
    real target checksum — distinguishing it from a stub run."""
    pin_model(MODEL_FAST)
    out = tmp_path / "out"
    r = _run_lens(runner, "bare-review", _write(tmp_path, "t.py", BUGGY_CODE), out)
    assert r.exit_code == EXIT_OK, r.output
    manifest = json.loads((out / MANIFEST_FILENAME).read_text())
    assert manifest["preflight"]["transport_kind"] == "openai_compat"
    assert len(manifest["preflight"]["target_checksum"]) == 64  # sha256 hex
    assert manifest["resolved_lens_entry"]["name"] == "bare-review"


# ---------------------------------------------------------------------------
# Per-worker model differentiation — confirm a single job uses ALL pool models
# ---------------------------------------------------------------------------
# Ordered .aienv model pool (T2Model01..04). model_id is stamped by the
# transport on EVERY WorkerResult (success AND proxy_error), so these tests
# assert per-slot model *attribution* covering the pool — independent of
# whether a given model returns 200 or 400 on the prompt.
AIENV_POOL_4 = ["kimi-k2.6", "qwen3.6-plus", "glm-5.1", "deepseek-v4-pro"]
AIENV_POOL_3 = ["kimi-k2.6", "qwen3.6-plus", "glm-5.1"]
RELIABLE_2 = ["qwen3.6-plus", "deepseek-v4-pro"]


def _model_ids(out: Path) -> list[str]:
    return [d.get("model_id") for d in _worker_done(out)]


def test_four_workers_use_all_four_models(runner, pin_pool, tmp_path):
    """The headline proof: a 4-worker job over the full 4-model .aienv pool
    binds each worker slot to a DISTINCT model — all four models are used in a
    single job (not T2Model01 shared across all)."""
    pin_pool(AIENV_POOL_4)
    out = tmp_path / "out"
    r = _run_lens(runner, "edge-case-hunt", _write(tmp_path, "t.py", BUGGY_CODE), out)
    assert r.exit_code == EXIT_OK, r.output
    ids = _model_ids(out)
    assert len(ids) == 4, f"expected 4 workers, got {len(ids)}"
    assert set(ids) == set(AIENV_POOL_4), (
        f"workers did not cover the full pool; saw {sorted(set(ids))}, "
        f"expected {sorted(AIENV_POOL_4)}"
    )
    assert len(set(ids)) == 4, (
        "models are not distinct per slot (single-model regression)"
    )


def test_three_workers_distinct_models(runner, pin_pool, tmp_path):
    """A 3-worker job over a 3-model pool uses all 3, one per slot."""
    pin_pool(AIENV_POOL_3)
    out = tmp_path / "out"
    r = _run_lens(runner, "bare-review", _write(tmp_path, "t.py", BUGGY_CODE), out)
    assert r.exit_code == EXIT_OK, r.output
    ids = _model_ids(out)
    assert len(ids) == 3
    assert set(ids) == set(AIENV_POOL_3), f"saw {sorted(set(ids))}"
    assert len(set(ids)) == 3


def test_two_reliable_models_heterogeneous_and_succeed(runner, pin_pool, tmp_path):
    """A 2-worker job over the two reliably-succeeding .aienv models uses BOTH
    (distinct per slot) AND both return real successful completions (http=200).
    This proves heterogeneous fan-out end-to-end, not just attribution."""
    pin_pool(RELIABLE_2)
    # 2-worker run via a full spec (scaffold bare-review, override count to 2).
    spec = tmp_path / "job.json"
    sr = runner.invoke(
        swarm_group, ["scaffold", "--lens", "bare-review", "--output", str(spec)]
    )
    assert sr.exit_code == EXIT_OK, sr.output
    target = _write(tmp_path, "t.py", BUGGY_CODE)
    out = tmp_path / "out"
    doc = json.loads(spec.read_text())
    doc["target"]["path"] = str(target)
    doc["output"]["dir"] = str(out)
    doc["workers"]["count"] = 2
    doc["workers"]["models"] = doc["workers"]["models"][
        :2
    ]  # keep count <= |spec models|
    spec.write_text(json.dumps(doc, indent=2))

    rr = runner.invoke(
        swarm_group,
        ["run", str(spec), "--output", str(out), "--transport", "openai_compat"],
    )
    assert rr.exit_code == EXIT_OK, rr.output
    done = _worker_done(out)
    ids = [d.get("model_id") for d in done]
    assert len(ids) == 2
    assert set(ids) == set(RELIABLE_2), f"saw {sorted(set(ids))}"
    assert all(d["status"] == "success" for d in done), [d["status"] for d in done]
    assert all(d["http_code"] == 200 for d in done)

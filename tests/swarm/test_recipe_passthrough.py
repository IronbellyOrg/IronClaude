"""T04.08 -- ``passthrough`` recipe tests (R-092 / COMP-020 / D-0074).

Three layers:

1. **Byte-identity contract**: ``Passthrough.normalize`` returns the
   raw body unchanged across the alphabet, frontmatter, control
   characters, mixed line endings, and pure-empty / pure-whitespace
   inputs.

2. **REGISTRY**: the ``passthrough`` slot resolves to a Recipe-
   conforming :class:`Passthrough` instance (no longer the M2-era
   ``None`` sentinel), and the Wave-2 dispatcher routes a worker
   through it producing a byte-identical ``final_path``.

3. **AC-011 boundary**: random bytes (including duplicate findings,
   re-ordered headings, and obvious garbage) reach the output
   verbatim. The recipe ignores the ``args`` dict and never sets
   ``salvaged=True`` -- raw mode does not classify the body.
"""

from __future__ import annotations

import json
import string
from pathlib import Path

from superclaude.cli.swarm.models import WorkerResult
from superclaude.cli.swarm.normalize import normalize_wave2
from superclaude.cli.swarm.recipes import REGISTRY, NormalizedResult, Recipe
from superclaude.cli.swarm.recipes.passthrough import Passthrough

# ---------------------------------------------------------------------------
# 1 -- Byte-identity contract
# ---------------------------------------------------------------------------


def test_normalize_returns_input_unchanged_for_ascii_body():
    body = "hello world\n"
    result = Passthrough().normalize(body, {})
    assert result.text == body
    assert result.salvaged is False
    assert result.error is None


def test_normalize_returns_input_unchanged_for_empty_body():
    result = Passthrough().normalize("", {})
    assert result.text == ""
    assert result.salvaged is False
    assert result.error is None


def test_normalize_returns_input_unchanged_for_whitespace_only_body():
    body = "   \n  \t  \n"
    result = Passthrough().normalize(body, {})
    assert result.text == body  # whitespace preserved verbatim


def test_normalize_returns_input_unchanged_for_unicode_body():
    body = "Verdict: ✅ yes — confidence 95% — éàü\n日本語\n"
    result = Passthrough().normalize(body, {})
    assert result.text == body
    # Byte-level identity: encoded form round-trips identically.
    assert result.text.encode("utf-8") == body.encode("utf-8")


def test_normalize_returns_input_unchanged_for_full_alphabet():
    body = string.ascii_letters + string.digits + string.punctuation + "\n\r\t\x0b\x0c"
    result = Passthrough().normalize(body, {})
    assert result.text == body


def test_normalize_returns_input_unchanged_for_frontmatter_body():
    body = (
        "---\n"
        'schema_version: "1.0"\n'
        'lens: "bare-review"\n'
        "---\n"
        "\n"
        "# Findings\n"
        "- Finding A\n"
        "- Finding B\n"
        "- Finding A\n"  # intentional dupe -- AC-011: preserved
    )
    result = Passthrough().normalize(body, {})
    assert result.text == body
    # AC-011 boundary: duplicate finding survives the recipe.
    assert result.text.count("Finding A") == 2


def test_normalize_returns_input_unchanged_for_mixed_line_endings():
    body = "line one\r\nline two\nline three\rline four\n"
    result = Passthrough().normalize(body, {})
    # Line endings preserved verbatim (no normalization).
    assert result.text == body


def test_normalize_ignores_args_dict():
    body = "anything"
    args = {
        "status": "parse_error",
        "target": "/x.md",
        "lens": "bare-review",
        "model_id": "m",
        "elapsed_ms": 42,
    }
    result = Passthrough().normalize(body, args)
    assert result.text == body
    # Even though status==parse_error in args, passthrough does NOT
    # mark salvaged -- raw mode never classifies the body.
    assert result.salvaged is False
    assert result.error is None


# ---------------------------------------------------------------------------
# 2 -- REGISTRY integration
# ---------------------------------------------------------------------------


def test_registry_resolves_passthrough_to_recipe():
    entry = REGISTRY["passthrough"]
    assert entry is not None  # M2-era sentinel must be replaced
    assert isinstance(entry, Recipe)
    assert isinstance(entry, Passthrough)


def test_registry_passthrough_protocol_callable():
    recipe = REGISTRY["passthrough"]
    assert recipe is not None
    result = recipe.normalize("payload", {})
    assert isinstance(result, NormalizedResult)
    assert result.text == "payload"


def _make_worker(
    tmp_path: Path,
    index: int,
    *,
    status: str,
    body: str,
) -> WorkerResult:
    raw_path = tmp_path / f"worker-{index:02d}.raw.md"
    raw_path.write_text(body, encoding="utf-8")
    return WorkerResult(
        index=index,
        path=str(tmp_path / f"worker-{index:02d}.md"),
        raw_path=str(raw_path),
        meta_path=str(tmp_path / f"worker-{index:02d}.meta.json"),
        final_path=str(tmp_path / f"worker-{index:02d}.final.md"),
        model_id=f"model-{index}",
        model_label=f"Model {index}",
        bytes=len(body.encode("utf-8")),
        status=status,
        http_code=200 if status == "success" else None,
        attempts=1,
        elapsed_ms=42,
    )


def test_dispatcher_routes_worker_through_passthrough_byte_identical(tmp_path):
    body = (
        "## Verdict\n"
        "uncertain (60) — needs more context\n"
        "\n## Notes\n"
        "raw body should survive untouched.\n"
    )
    worker = _make_worker(tmp_path, 0, status="success", body=body)

    [out] = normalize_wave2([worker], "passthrough")

    assert out.status == "success"
    final_bytes = Path(worker.final_path).read_bytes()
    # Byte-identity: dispatcher output == raw input bytes.
    assert final_bytes == body.encode("utf-8")
    assert out.bytes == len(body.encode("utf-8"))

    meta = json.loads(Path(worker.meta_path).read_text(encoding="utf-8"))
    assert meta["recipe"] == "passthrough"
    assert meta["salvaged"] is False
    assert meta["status"] == "success"


def test_dispatcher_passthrough_does_not_salvage_parse_error(tmp_path):
    """Raw mode preserves transport's terminal classification."""
    body = "garbage that any normalizer would reject\n"
    worker = _make_worker(tmp_path, 1, status="parse_error", body=body)

    [out] = normalize_wave2([worker], "passthrough")

    # Passthrough never sets salvaged=True; status stays parse_error.
    assert out.status == "parse_error"
    final_bytes = Path(worker.final_path).read_bytes()
    assert final_bytes == body.encode("utf-8")

    meta = json.loads(Path(worker.meta_path).read_text(encoding="utf-8"))
    assert meta["recipe"] == "passthrough"
    assert meta["salvaged"] is False
    assert meta["status"] == "parse_error"


def test_dispatcher_passthrough_empty_body_writes_zero_bytes(tmp_path):
    worker = _make_worker(tmp_path, 2, status="success", body="")

    [out] = normalize_wave2([worker], "passthrough")

    # Empty input -> recipe returns empty text; dispatcher does NOT
    # write final_path when text is empty (see _normalize_one in
    # normalize.py), so bytes stay at 0 and final_path may or may not
    # exist. The meta sidecar IS written for surface uniformity.
    assert out.bytes == 0
    meta = json.loads(Path(worker.meta_path).read_text(encoding="utf-8"))
    assert meta["recipe"] == "passthrough"
    assert meta["bytes"] == 0
    assert meta["salvaged"] is False


# ---------------------------------------------------------------------------
# 3 -- AC-011 boundary (no judging transforms)
# ---------------------------------------------------------------------------


def test_passthrough_preserves_duplicates_and_order():
    body = (
        "Finding A\n"
        "Finding B\n"
        "Finding A\n"  # duplicate must survive
        "Finding C\n"
        "Finding B\n"  # duplicate must survive
    )
    result = Passthrough().normalize(body, {})
    assert result.text == body
    assert result.text.count("Finding A") == 2
    assert result.text.count("Finding B") == 2
    # Order preserved: first finding is still "Finding A".
    assert result.text.splitlines()[0] == "Finding A"
    assert result.text.splitlines()[-1] == "Finding B"


def test_passthrough_random_byte_fixture_round_trip():
    """Random fixture -> output bytes == input bytes (validation row)."""
    # Deterministic but adversarial fixture: punctuation, control
    # characters, embedded markdown structures, and trailing
    # whitespace. None of these may be touched.
    body = (
        "# Title\n"
        "\n"
        "    indented code block?\n"
        "\t- tabbed bullet\n"
        "trailing spaces below   \n"
        "\n"
        "​‌invisible chars\n"  # zero-width spaces
        "## Section\n"
        "content\r\n"
    )
    assert Passthrough().normalize(body, {}).text == body
    assert Passthrough().normalize(body, {}).text.encode("utf-8") == body.encode(
        "utf-8"
    )

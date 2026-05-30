"""TEST-009 artifact reproducibility tests (R-080 / D-0080 / T04.20).

Pins the FR-G4 + DM-012 reproducibility contract every ``superclaude
eval run`` invocation must satisfy at the artifact layer. The five
acceptance criteria from ``phase-4-tasklist.md`` §T04.20 are:

1. **Run dir matches the FR-G4 pattern** —
   ``<output_root>/.dev/eval-runs/<YYYY-MM-DD>/<run-id>/`` and is
   deterministic for a ``(started_at, suite_name)`` pair so two runs
   on the same instant collide on the same path.
2. **Per-eval ``logs.jsonl`` exists and is non-empty after a run** —
   the per-eval JSONL emitter (T03.05 / D-0049) drops events under
   the pinned filename and the file survives the run.
3. **Per-eval ``tty.transcript`` exists** — the PtyDriver / PtyStream
   capture lands at the pinned filename inside the per-eval subtree.
4. **Stack trace recorded on ERRORED outcomes** — the per-eval JSONL
   carries a ``traceback`` field on the failure event AND the
   Reporter-rendered ``summary.json`` carries the same traceback
   inside the ``evals[].expects[].failure.traceback`` field (DM-005).
5. **summary.json ``evals[]`` cross-links to per-eval artifact paths** —
   each row's ``artifacts`` mapping names the per-eval ``logs.jsonl``,
   ``tty.transcript``, and ``artifacts/`` directory using paths
   relative to the run directory so a reviewer can navigate from
   summary → per-eval transcript without re-deriving the layout.

The module is deliberately self-contained: it builds RunSummary
fixtures from scratch and writes per-eval artifacts via the
:mod:`superclaude.cli.eval.artifact_layout` helpers (the FR-G4
source-of-truth). The full ``superclaude eval run`` end-to-end loop
is a T04.10 forward dependency; by anchoring the contract at the
layout + Reporter seam this module pins the reproducibility matrix
today and the T04.10 closure must satisfy the same invariants when
it lands.

Cross-links:
* FR-G4 / R-074 / D-0074 / T04.13 — the artifact-layout module
  (``compose_run_dir``, ``allocate_per_eval_paths``,
  ``parse_run_dir_components``) this test exercises.
* DM-012 / T03.10 — the summary.schema.json the Reporter renders to;
  ``evals[].artifacts`` is the cross-link field this test reads.
* DM-005 / T01.16 — ``ExpectFailure.traceback`` is the rendered
  traceback channel; ``logs.jsonl`` carries the same string verbatim
  so the JSONL log is the authoritative source the schema docs name.
* T04.17 / D-0078 (Reporter contract suite) — sibling tests that pin
  the N'-vs-K invariant; this module trusts that guard and focuses
  on the artifact + cross-link contract.
"""

from __future__ import annotations

import json
import re
import traceback as tb_mod
from pathlib import Path

import pytest

from superclaude.cli.eval.artifact_layout import (
    ARTIFACTS_SUBDIR_NAME,
    LOGS_JSONL_NAME,
    PER_EVAL_DIRNAME,
    RUN_DIR_PREFIX,
    TTY_TRANSCRIPT_NAME,
    allocate_per_eval_paths,
    compose_per_eval_dir,
    compose_run_dir,
    compose_run_id,
    parse_run_dir_components,
)
from superclaude.cli.eval.models import (
    EvalOutcome,
    ExpectFailure,
    ExpectResult,
    RunCounts,
    RunSummary,
    RunTotals,
)
from superclaude.cli.eval.reporter import Reporter

# ---------------------------------------------------------------------------
# Layout pattern constants (kept identical to artifact_layout's pins so a
# rename there breaks here intentionally).
# ---------------------------------------------------------------------------


_RUN_ID_RE = re.compile(r"^\d{6}Z-[0-9a-f]{8}$")
_DATE_SEGMENT_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")

# Fixture inputs used across the matrix. Kept as module-level constants so
# every test exercises the *same* (started_at, suite_name) pair and the
# determinism assertions in test_run_dir_deterministic_for_inputs and
# test_summary_json_cross_links_per_eval_artifacts can compare against the
# same expected run-id.
_STARTED_AT = "2026-05-20T15:58:38Z"
_FINISHED_AT = "2026-05-20T15:59:30Z"
_SUITE_NAME = "real"


# ---------------------------------------------------------------------------
# Fixture helpers — build a complete FR-G4 artifact tree on disk
# ---------------------------------------------------------------------------


def _make_traceback() -> str:
    """Return a realistic Python traceback string.

    Raises and catches a ``RuntimeError`` so the resulting traceback
    contains live frame lines (``File "...", line ...``) rather than a
    hand-crafted string a future change could let pass while losing the
    actual stack content.
    """

    try:
        raise RuntimeError("simulated harness error inside eval body")
    except RuntimeError as exc:
        return "".join(tb_mod.format_exception(type(exc), exc, exc.__traceback__))


def _write_pass_per_eval(
    run_dir: Path,
    eval_id: str = "E1",
) -> dict[str, Path]:
    """Materialise the per-eval subtree for a PASS scenario.

    Writes a minimal JSONL stream (start / expect / end events) and a
    short TTY transcript so the layer-level assertions can confirm both
    files exist and carry content. Returns a mapping of the three
    cross-link names the Reporter will surface in ``evals[].artifacts``.
    """

    paths = allocate_per_eval_paths(run_dir, eval_id)

    paths.logs_jsonl.write_text(
        "\n".join(
            [
                json.dumps(
                    {
                        "event": "eval.start",
                        "eval_id": eval_id,
                        "ts": _STARTED_AT,
                    }
                ),
                json.dumps(
                    {
                        "event": "expect.pass",
                        "eval_id": eval_id,
                        "name": "exit_code",
                    }
                ),
                json.dumps(
                    {
                        "event": "eval.end",
                        "eval_id": eval_id,
                        "ts": _FINISHED_AT,
                        "status": "PASS",
                    }
                ),
            ]
        )
        + "\n",
        encoding="utf-8",
    )

    paths.tty_transcript.write_text(
        f"$ claude --eval {eval_id}\nready\n[exit 0]\n",
        encoding="utf-8",
    )

    return {
        "logs.jsonl": paths.logs_jsonl,
        "tty.transcript": paths.tty_transcript,
        "artifacts/": paths.artifacts_dir,
    }


def _write_errored_per_eval(
    run_dir: Path,
    eval_id: str = "E2",
) -> tuple[dict[str, Path], str]:
    """Materialise the per-eval subtree for an ERRORED scenario.

    Returns a ``(paths, traceback_string)`` pair so callers can both
    cross-link the artifacts and confirm the traceback round-trips
    verbatim into the JSONL log + Reporter output.
    """

    paths = allocate_per_eval_paths(run_dir, eval_id)
    trace = _make_traceback()

    paths.logs_jsonl.write_text(
        "\n".join(
            [
                json.dumps(
                    {
                        "event": "eval.start",
                        "eval_id": eval_id,
                        "ts": _STARTED_AT,
                    }
                ),
                json.dumps(
                    {
                        "event": "eval.error",
                        "eval_id": eval_id,
                        "error_class": "builtins.RuntimeError",
                        "message": "simulated harness error inside eval body",
                        "traceback": trace,
                    }
                ),
                json.dumps(
                    {
                        "event": "eval.end",
                        "eval_id": eval_id,
                        "ts": _FINISHED_AT,
                        "status": "ERRORED",
                    }
                ),
            ]
        )
        + "\n",
        encoding="utf-8",
    )

    paths.tty_transcript.write_text(
        f"$ claude --eval {eval_id}\nready\nTraceback (most recent call last):\n",
        encoding="utf-8",
    )

    return (
        {
            "logs.jsonl": paths.logs_jsonl,
            "tty.transcript": paths.tty_transcript,
            "artifacts/": paths.artifacts_dir,
        },
        trace,
    )


def _per_eval_artifacts_map(
    run_dir: Path,
    eval_id: str,
) -> dict[str, str]:
    """Return the run-relative artifact paths the Reporter cross-links.

    Mirrors the convention DM-001 / DM-012 declare: ``artifacts`` values
    are run-relative POSIX strings so the JSON is portable across hosts.
    """

    eval_dir = compose_per_eval_dir(run_dir, eval_id)
    return {
        LOGS_JSONL_NAME: (eval_dir.relative_to(run_dir) / LOGS_JSONL_NAME).as_posix(),
        TTY_TRANSCRIPT_NAME: (
            eval_dir.relative_to(run_dir) / TTY_TRANSCRIPT_NAME
        ).as_posix(),
        ARTIFACTS_SUBDIR_NAME: (
            eval_dir.relative_to(run_dir) / ARTIFACTS_SUBDIR_NAME
        ).as_posix(),
    }


def _build_summary(
    *,
    run_id: str,
    pass_eval_id: str,
    pass_artifacts: dict[str, str],
    errored_eval_id: str,
    errored_artifacts: dict[str, str],
    traceback_str: str,
) -> RunSummary:
    """Construct a two-row RunSummary (PASS + ERRORED) for the matrix.

    The pass row's ``artifacts`` maps the three FR-G4 entries; the
    errored row carries an :class:`ExpectFailure` with the same
    traceback string the JSONL log holds so callers can confirm the
    cross-channel cross-link.
    """

    pass_outcome = EvalOutcome(
        eval_id=pass_eval_id,
        title=f"{pass_eval_id} pass",
        status="PASS",
        duration_sec=1.25,
        expects=(ExpectResult(name="exit_code", passed=True, message="ok"),),
        artifacts=pass_artifacts,
    )

    errored_failure = ExpectFailure(
        eval_id=errored_eval_id,
        expect_id="harness[0]",
        expect_name="harness",
        expected=None,
        actual=None,
        message="harness raised RuntimeError",
        artifact_ref=errored_artifacts[LOGS_JSONL_NAME],
        traceback=traceback_str,
    )
    errored_outcome = EvalOutcome(
        eval_id=errored_eval_id,
        title=f"{errored_eval_id} errored",
        status="ERRORED",
        duration_sec=0.5,
        expects=(
            ExpectResult(
                name="harness",
                passed=False,
                message="harness raised RuntimeError",
                failure=errored_failure,
            ),
        ),
        artifacts=errored_artifacts,
        error_class="builtins.RuntimeError",
    )

    counts = RunCounts(
        manifest_n=2,
        expanded_n_prime=2,
        kept_k=2,
        skipped_s=0,
        kept_plus_skipped_equals_n_prime=True,
    )
    totals = RunTotals(passed=1, errored=1)

    return RunSummary(
        run_id=run_id,
        started_at=_STARTED_AT,
        finished_at=_FINISHED_AT,
        duration_sec=52.0,
        suite=f"suites/{_SUITE_NAME}.yaml",
        manifest_version="1.0",
        parallel=1,
        counts=counts,
        totals=totals,
        evals=(pass_outcome, errored_outcome),
    )


# ---------------------------------------------------------------------------
# Scenario 1 — Run-dir pattern matches `.dev/eval-runs/<ISO>/<run-id>/`
# ---------------------------------------------------------------------------


def test_run_dir_matches_fr_g4_pattern(tmp_path: Path) -> None:
    """FR-G4 AC: run-dir is anchored under ``.dev/eval-runs/<date>/<run-id>/``.

    Pins the three structural invariants the rest of the matrix
    depends on:

    * The path is rooted at :data:`RUN_DIR_PREFIX` (``.dev/eval-runs``).
    * The date segment is ``YYYY-MM-DD`` (derived from ``started_at``).
    * The run-id matches the ``<HHMMSSZ>-<8-hex>`` shape.
    """

    run_dir = compose_run_dir(tmp_path, _STARTED_AT, suite_name=_SUITE_NAME)

    # Path is rooted at .dev/eval-runs/.
    assert RUN_DIR_PREFIX.as_posix() in run_dir.as_posix()

    # Decomposed: <output_root>/.dev/eval-runs/<YYYY-MM-DD>/<run-id>/
    rel = run_dir.relative_to(tmp_path).parts
    assert rel[0] == ".dev"
    assert rel[1] == "eval-runs"
    assert _DATE_SEGMENT_RE.fullmatch(rel[2]), rel[2]
    assert _RUN_ID_RE.fullmatch(rel[3]), rel[3]

    # parse_run_dir_components round-trips the pair.
    parsed = parse_run_dir_components(run_dir)
    assert parsed.date_segment == "2026-05-20"
    assert parsed.run_id == compose_run_id(_STARTED_AT, _SUITE_NAME)


def test_run_dir_deterministic_for_inputs(tmp_path: Path) -> None:
    """Reproducibility: same ``(started_at, suite_name)`` -> same run-dir.

    The FR-G4 spec promises run-id determinism so two replayed runs
    against the same suite at the same instant land on the same path
    (a precondition for cache-style behaviour and idempotent CI
    re-runs). Different inputs MUST differ — both axes are checked
    here.
    """

    a = compose_run_dir(tmp_path, _STARTED_AT, suite_name=_SUITE_NAME)
    b = compose_run_dir(tmp_path, _STARTED_AT, suite_name=_SUITE_NAME)
    assert a == b

    # Different suite name -> different run-dir (hash tail diverges).
    c = compose_run_dir(tmp_path, _STARTED_AT, suite_name="other")
    assert a != c
    assert a.parent == c.parent  # Same date segment.

    # Different timestamp -> different run-dir.
    d = compose_run_dir(tmp_path, "2026-05-20T15:58:39Z", suite_name=_SUITE_NAME)
    assert a != d


# ---------------------------------------------------------------------------
# Scenario 2 — Per-eval logs.jsonl exists, non-empty, JSON-Lines parsable
# ---------------------------------------------------------------------------


def test_per_eval_logs_jsonl_present_and_parsable(tmp_path: Path) -> None:
    """FR-G4 AC: per-eval ``logs.jsonl`` exists and is JSONL-parsable.

    The JSONL emitter (T03.05) writes one event per line. The
    reproducibility contract requires (a) the file exists at the
    pinned filename, (b) the file is non-empty, and (c) every line
    parses as JSON so downstream parsers (CI dashboards, the
    `Expect.jsonl` primitive) do not blow up on a corrupt run.
    """

    run_dir = compose_run_dir(tmp_path, _STARTED_AT, suite_name=_SUITE_NAME)
    paths = _write_pass_per_eval(run_dir, eval_id="E1")

    logs = paths["logs.jsonl"]
    assert logs.is_file(), "logs.jsonl must exist at the FR-G4 pinned path"
    assert logs.name == LOGS_JSONL_NAME
    raw = logs.read_text(encoding="utf-8")
    assert raw.strip(), "logs.jsonl must be non-empty after a run"

    events = [json.loads(line) for line in raw.splitlines() if line.strip()]
    assert len(events) == 3, "PASS fixture writes start/expect/end events"
    assert events[0]["event"] == "eval.start"
    assert events[-1]["status"] == "PASS"

    # And the file sits under the per-eval subtree (defense in depth: a
    # refactor that placed logs.jsonl outside per-eval/ would skip this
    # assertion silently if we only checked the name).
    eval_dir = compose_per_eval_dir(run_dir, "E1")
    assert logs.parent == eval_dir


# ---------------------------------------------------------------------------
# Scenario 3 — Per-eval tty.transcript exists and carries content
# ---------------------------------------------------------------------------


def test_per_eval_tty_transcript_present_and_non_empty(tmp_path: Path) -> None:
    """FR-G4 AC: per-eval ``tty.transcript`` exists at the pinned filename.

    The PtyDriver / PtyStream layer (T02.16 / T02.17) writes the raw
    PTY capture to ``tty.transcript``. The reproducibility contract
    requires the file exists, is non-empty, and lives inside the
    per-eval subtree.
    """

    run_dir = compose_run_dir(tmp_path, _STARTED_AT, suite_name=_SUITE_NAME)
    paths = _write_pass_per_eval(run_dir, eval_id="E1")

    transcript = paths["tty.transcript"]
    assert transcript.is_file(), "tty.transcript must exist at the FR-G4 path"
    assert transcript.name == TTY_TRANSCRIPT_NAME
    body = transcript.read_text(encoding="utf-8")
    assert body, "tty.transcript must be non-empty after a run"

    eval_dir = compose_per_eval_dir(run_dir, "E1")
    assert transcript.parent == eval_dir


# ---------------------------------------------------------------------------
# Scenario 4 — Stack trace recorded on ERRORED outcomes
# ---------------------------------------------------------------------------


def test_errored_outcome_records_stack_trace(tmp_path: Path) -> None:
    """FR-G4 AC: ERRORED outcomes record the harness traceback.

    DM-005 names ``ExpectFailure.traceback`` as the rendered
    traceback channel and the design-spec notes the per-eval JSONL is
    the authoritative source. Both surfaces must carry the *same*
    traceback string so a reviewer can chase the failure from
    summary.json into logs.jsonl without parsing format differences.
    """

    run_dir = compose_run_dir(tmp_path, _STARTED_AT, suite_name=_SUITE_NAME)
    paths, expected_trace = _write_errored_per_eval(run_dir, eval_id="E2")

    # Source-of-truth: the JSONL event the runner wrote.
    events = [
        json.loads(line)
        for line in paths["logs.jsonl"].read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    error_events = [e for e in events if e["event"] == "eval.error"]
    assert len(error_events) == 1, "exactly one eval.error event per ERRORED"
    jsonl_trace = error_events[0]["traceback"]
    assert jsonl_trace == expected_trace
    # Must contain a real Python frame line — guards against a future
    # change that records an empty string under the right key.
    assert "Traceback (most recent call last):" in jsonl_trace
    assert "RuntimeError" in jsonl_trace
    assert re.search(r'File ".+?", line \d+', jsonl_trace), (
        "traceback must include at least one frame line"
    )

    # Reporter surface: ExpectFailure.traceback round-trips into
    # summary.json via the FR-RPT1 renderer.
    summary = _build_summary(
        run_id=compose_run_id(_STARTED_AT, _SUITE_NAME),
        pass_eval_id="E1",
        pass_artifacts=_per_eval_artifacts_map(run_dir, "E1"),
        errored_eval_id="E2",
        errored_artifacts=_per_eval_artifacts_map(run_dir, "E2"),
        traceback_str=expected_trace,
    )
    payload = json.loads(Reporter(summary).to_json())

    errored_row = next(row for row in payload["evals"] if row["status"] == "ERRORED")
    assert errored_row["error_class"] == "builtins.RuntimeError"
    assert errored_row["expects"], "ERRORED row must carry an ExpectResult"
    rendered_failure = errored_row["expects"][0]["failure"]
    assert rendered_failure is not None
    assert rendered_failure["traceback"] == expected_trace, (
        "summary.json and logs.jsonl must carry the same traceback"
    )


# ---------------------------------------------------------------------------
# Scenario 5 — summary.json evals[] cross-link to per-eval artifact paths
# ---------------------------------------------------------------------------


def test_summary_json_cross_links_per_eval_artifacts(tmp_path: Path) -> None:
    """FR-G4 AC: ``summary.json evals[].artifacts`` references per-eval paths.

    Pins the cross-link reviewers rely on to navigate from the
    aggregate summary into a single eval's transcript: each row's
    ``artifacts`` map must name the three FR-G4 entries
    (``logs.jsonl``, ``tty.transcript``, ``artifacts/``) and each
    referenced path must resolve to a real file (or directory) under
    the run directory.
    """

    run_dir = compose_run_dir(tmp_path, _STARTED_AT, suite_name=_SUITE_NAME)
    pass_paths = _write_pass_per_eval(run_dir, eval_id="E1")
    errored_paths, trace = _write_errored_per_eval(run_dir, eval_id="E2")

    summary = _build_summary(
        run_id=compose_run_id(_STARTED_AT, _SUITE_NAME),
        pass_eval_id="E1",
        pass_artifacts=_per_eval_artifacts_map(run_dir, "E1"),
        errored_eval_id="E2",
        errored_artifacts=_per_eval_artifacts_map(run_dir, "E2"),
        traceback_str=trace,
    )

    # Write the Reporter output beside the per-eval tree so the
    # summary.json can be read back from disk (matches what the
    # T04.10 closure will do at runtime).
    written = Reporter(summary).write(run_dir)
    summary_path = written["summary.json"]
    assert summary_path.parent == run_dir, (
        "summary.json must land at the run-dir root, alongside per-eval/"
    )
    payload = json.loads(summary_path.read_text(encoding="utf-8"))

    # Every row's artifacts mapping must name the three FR-G4 entries.
    rows_by_id = {row["eval_id"]: row for row in payload["evals"]}
    for eval_id, on_disk in (("E1", pass_paths), ("E2", errored_paths)):
        row = rows_by_id[eval_id]
        artifacts = row["artifacts"]
        assert set(artifacts) >= {
            LOGS_JSONL_NAME,
            TTY_TRANSCRIPT_NAME,
            ARTIFACTS_SUBDIR_NAME,
        }, f"{eval_id} row must cross-link the 3 FR-G4 entries; got {sorted(artifacts)}"

        # Each cross-link path resolves against the run-dir to a real
        # entry. The Reporter records paths as run-relative POSIX
        # strings; the on-disk Path the fixture wrote is the
        # ground-truth target.
        resolved_logs = (run_dir / artifacts[LOGS_JSONL_NAME]).resolve()
        resolved_tty = (run_dir / artifacts[TTY_TRANSCRIPT_NAME]).resolve()
        resolved_artifacts = (run_dir / artifacts[ARTIFACTS_SUBDIR_NAME]).resolve()
        assert resolved_logs == on_disk["logs.jsonl"].resolve()
        assert resolved_tty == on_disk["tty.transcript"].resolve()
        assert resolved_artifacts == on_disk["artifacts/"].resolve()
        assert resolved_logs.is_file()
        assert resolved_tty.is_file()
        assert resolved_artifacts.is_dir()

        # Cross-links live under per-eval/<eval_id>/ — guards against a
        # future change that moved the per-eval subtree without
        # updating the artifact map.
        assert (
            artifacts[LOGS_JSONL_NAME]
            == f"{PER_EVAL_DIRNAME}/{eval_id}/{LOGS_JSONL_NAME}"
        )

    # ERRORED row also surfaces error_class so a CI dashboard can
    # bucket harness failures without re-reading per-eval logs.
    assert rows_by_id["E2"]["error_class"] == "builtins.RuntimeError"


# ---------------------------------------------------------------------------
# Reproducibility matrix — single end-to-end test that re-runs the fixture
# and asserts byte-stable summary.json output.
# ---------------------------------------------------------------------------


def test_artifact_tree_reproducible_across_replays(tmp_path: Path) -> None:
    """Two replays with identical inputs produce identical artifact paths
    and a byte-stable ``summary.json`` payload.

    This is the headline reproducibility assertion: the FR-G4 layout
    + DM-001 outcome serialisation + DM-012 summary schema are all
    deterministic, so a second run against the same ``(started_at,
    suite_name)`` and the same eval outcomes lands on the same paths
    AND emits the same bytes. A future change that introduces
    non-determinism (timestamp jitter, random run-id suffix,
    dict-ordering instability) breaks this assertion loudly.
    """

    # Two independent run-roots so the second replay's writes can't
    # alias the first's on-disk state.
    root_a = tmp_path / "replay_a"
    root_b = tmp_path / "replay_b"

    payloads: list[dict] = []
    for root in (root_a, root_b):
        run_dir = compose_run_dir(root, _STARTED_AT, suite_name=_SUITE_NAME)
        _write_pass_per_eval(run_dir, eval_id="E1")
        _, trace = _write_errored_per_eval(run_dir, eval_id="E2")
        summary = _build_summary(
            run_id=compose_run_id(_STARTED_AT, _SUITE_NAME),
            pass_eval_id="E1",
            pass_artifacts=_per_eval_artifacts_map(run_dir, "E1"),
            errored_eval_id="E2",
            errored_artifacts=_per_eval_artifacts_map(run_dir, "E2"),
            traceback_str=trace,
        )
        written = Reporter(summary).write(run_dir)
        payloads.append(json.loads(written["summary.json"].read_text(encoding="utf-8")))

    # The two replays' run-dir tails (date + run-id) match.
    tail_a = compose_run_dir(root_a, _STARTED_AT, suite_name=_SUITE_NAME).relative_to(
        root_a
    )
    tail_b = compose_run_dir(root_b, _STARTED_AT, suite_name=_SUITE_NAME).relative_to(
        root_b
    )
    assert tail_a == tail_b

    # Summary payloads compare equal field-for-field. ``traceback``
    # contains absolute file paths from the test process, so the two
    # replays share that traceback verbatim *only* because both were
    # built inside the same test process — the inequality would
    # otherwise be a real reproducibility hazard worth surfacing.
    assert payloads[0] == payloads[1]

    # And the cross-link strings are themselves run-relative (no
    # tmp_path leakage into the summary), which is what makes the
    # payload portable across hosts.
    for row in payloads[0]["evals"]:
        for key in (LOGS_JSONL_NAME, TTY_TRANSCRIPT_NAME, ARTIFACTS_SUBDIR_NAME):
            assert key in row["artifacts"]
            value = row["artifacts"][key]
            assert not value.startswith("/"), (
                f"{row['eval_id']}/{key} must be a run-relative path, not absolute"
            )
            assert str(tmp_path) not in value, (
                "summary.json must not leak the test tmp_path into cross-links"
            )


# ---------------------------------------------------------------------------
# Negative guard — non-layout paths fail loudly in parse_run_dir_components
# ---------------------------------------------------------------------------


def test_parse_run_dir_rejects_non_layout_paths(tmp_path: Path) -> None:
    """A run-dir that does NOT match the FR-G4 layout raises ``ValueError``.

    The inverse parser is the structural assertion the CLI relies on
    when it accepts an operator-supplied ``--output-dir``. Letting a
    malformed path through silently would let a reviewer chase
    artifacts under a directory that doesn't match the layout the
    summary advertises — which is the exact failure this module
    guards against.
    """

    with pytest.raises(ValueError):
        parse_run_dir_components(tmp_path / "not" / "the" / "layout")

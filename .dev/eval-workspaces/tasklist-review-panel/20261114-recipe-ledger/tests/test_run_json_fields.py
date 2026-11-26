"""DR-12: run.json and timing.json hold the field names of DESIGN 2.2 and 9.3 (the sibling's names, `SWD` 2.2 and 11.4),
plus the RL fields. The expected names are written out here and each is checked against the DESIGN text, so a change of
either side fails."""

import re

import pytest
from helpers import SW
from panel_support import ok_runs, sandbox  # noqa: F401  (session fixtures)

pytestmark = pytest.mark.slow
DESIGN = (SW / "DESIGN.md").read_text(encoding="utf-8")
# DESIGN 2.2, the paragraph that starts "`run.json` (written first": the names it spells out in backticks
RUN_FIELDS = {
    "arm", "panel", "doc", "replicate", "seed", "block", "rl_version", "recipes_sha256", "lenses_sha256",
    "registry_version", "freeze_tag", "fallback", "no_source", "c2_not_applicable", "no_budget", "check_skipped",
    "reask", "time_cap_exception", "concurrent_panels_at_start",
}  # fmt: skip
# the same paragraph in words: the sha256 of candidate, source, every brief and the Z0 brief; the row cap, b and c per reviewer
RUN_FIELDS_IN_WORDS = {"candidate_sha256", "source_sha256", "z0_sha256", "b"}
REVIEWER_FIELDS = {"brief_sha256", "row_cap", "b", "c", "recipes", "model"}
# DESIGN 9.3, the first column of the table
TIMING_FIELDS = {
    "t0",
    "render_s",
    "rev_start",
    "rev_end",
    "check_s",
    "reask_s",
    "panel_elapsed_s",
    "slowest_reviewer_s",
}


def design_names(heading_start, stop):
    block = DESIGN[DESIGN.index(heading_start) :]
    block = block[: block.index(stop)]
    return set(re.findall(r"`([a-z_0-9]+)(?:\[rid\])?`", block))


def test_fields_match_sibling_schema(ok_runs):  # noqa: F811
    run_names = design_names("`run.json` (written first", "### 2.3")
    assert RUN_FIELDS <= run_names, RUN_FIELDS - run_names
    timing_names = design_names(
        "One clock per run in `timing.json`", "Mean and median per arm"
    )
    assert TIMING_FIELDS <= timing_names, TIMING_FIELDS - timing_names
    for r in (ok_runs.rl, ok_runs.z0):
        run, timing = r.js("run.json"), r.js("timing.json")
        assert (RUN_FIELDS | RUN_FIELDS_IN_WORDS) <= set(run), (
            RUN_FIELDS | RUN_FIELDS_IN_WORDS
        ) - set(run)
        assert TIMING_FIELDS <= set(timing), TIMING_FIELDS - set(timing)
        assert run["time_cap_exception"] is False and run["reask"] == []
        assert run["arm"] in ("RL", "Z0") and run["concurrent_panels_at_start"] >= 0
        assert (
            set(run["reviewers"]) == set(timing["rev_start"]) == set(timing["rev_end"])
        )
    rl = ok_runs.rl.js("run.json")
    for rid, rv in rl[
        "reviewers"
    ].items():  # RL: the row cap used per reviewer, with the b and c it came from
        assert REVIEWER_FIELDS <= set(rv), rid
        assert 1 <= rv["row_cap"] <= 14 and rv["b"] > 0 and rv["c"] > 0
    assert len(rl["recipes_sha256"]) == len(rl["lenses_sha256"]) == 64
    # the arms differ only where they must: Z0 has no render or check seconds
    z0 = ok_runs.z0.js("timing.json")
    assert (z0["render_s"], z0["check_s"]) == (0, 0) and ok_runs.rl.js("timing.json")[
        "render_s"
    ] > 0

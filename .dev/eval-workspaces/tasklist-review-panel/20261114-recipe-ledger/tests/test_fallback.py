"""REQ-12 (a): a failing lens render runs the Z0 briefs with fallback=true, decided before any reviewer starts
(DESIGN 8 rows 1 and 2, INV-012). Through bin/run-panel.sh on the fake claude; no model starts."""

import hashlib
import json

import pytest
from panel_support import EMBER, L1, L2, run_panel, sandbox  # noqa: F401  (session fixture)

from fixtures.lens import make_lens
from scaffold import briefs

pytestmark = pytest.mark.slow


def z0_text(box):
    doc = {
        "cand_sb": str(box.cand),
        "sha": hashlib.sha256(box.cand.read_bytes()).hexdigest(),
    }
    return briefs.render("Z0", doc, None, str(box.source))["text"]


def assert_z0_run(box, r, reason):
    assert r.rc == 0, r.err
    z0 = z0_text(box)
    z0_sha = hashlib.sha256(z0.encode()).hexdigest()
    run = r.js("run.json")
    assert run["fallback"] is True and run["fallback_reason"] == reason
    assert run["arm"] == "RL"  # intention to treat: the run stays in its arm
    assert run["z0_sha256"] == z0_sha
    for rid in (EMBER, L1, L2):
        assert (r.run / "briefs" / f"{rid}.txt").read_text() == z0
        assert run["reviewers"][rid]["brief_sha256"] == z0_sha
        assert not (
            r.run / "lens" / f"{rid}.json"
        ).exists()  # no lens: no recipes, no ledger rule
    assert len(r.calls) == 3 and {c[3] for c in r.calls} == {"review"}
    # no check was asked for, so none was skipped; the raw reports were merged
    assert (run["check_ran"], run["check_skipped"]) == (False, False)
    assert (r.run / "merged" / "merged-1.md").is_file() and run[
        "merge_refused"
    ] is False


def test_forced_exception_in_lens_render_runs_z0_briefs(sandbox):  # noqa: F811
    r = run_panel(sandbox, env={"RL_FORCE_EXC": "lens"})
    assert_z0_run(sandbox, r, "error")
    err = json.loads((r.run / "lens" / "error.json").read_text())
    assert err["error"] == "RuntimeError" and err["reason"] == "error"


def test_invalid_lens_table_falls_back(sandbox, tmp_path):  # noqa: F811
    rule, table = make_lens.invalid_tables()["table_cap_15"]
    assert rule == 3
    path = sandbox.root / "bad-lenses.json"
    path.write_text(json.dumps(table), encoding="utf-8")
    r = run_panel(sandbox, env={"RL_LENSES": str(path)})
    assert_z0_run(sandbox, r, "lens_invalid")
    assert "E_LENS_INVALID" in r.err
    assert (
        json.loads((r.run / "lens" / "error.json").read_text())["reason"]
        == "lens_invalid"
    )


def test_fallback_decided_before_first_reviewer_starts(sandbox):  # noqa: F811
    r = run_panel(sandbox, env={"RL_FORCE_EXC": "lens"})
    assert r.rc == 0, r.err
    decided = r.js("run.json")["fallback_at"]
    first_call = min(float(c[0]) for c in r.calls)
    assert decided < first_call
    # the briefs the reviewers read were written before that too
    for rid in (EMBER, L1, L2):
        assert (r.run / "briefs" / f"{rid}.txt").stat().st_mtime < first_call
        assert (
            r.js(f"reviews/{rid}.meta.json")["prompt_sha256"]
            == r.js("run.json")["z0_sha256"]
        )

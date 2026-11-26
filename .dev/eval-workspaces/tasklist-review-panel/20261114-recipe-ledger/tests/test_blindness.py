"""The merged report does not show which arm made it (DESIGN 9.6, REQ-11 by the real merge): the keys class, probe and src
and the ledger block reach neither merged-1.md nor the merge ledger."""

import json
import re

import pytest
from panel_support import EMBER, L1, L2, ok_runs, sandbox  # noqa: F401  (session fixtures)

pytestmark = pytest.mark.slow
KEYS = ("probe", "src", "class")


def keys_in(obj):
    if isinstance(obj, dict):
        for k, v in obj.items():
            yield k
            yield from keys_in(v)
    elif isinstance(obj, list):
        for v in obj:
            yield from keys_in(v)


def test_merged_report_has_no_telemetry_keys(ok_runs):  # noqa: F811
    r = ok_runs.problem
    # the control: the report the merge was given does carry the telemetry (the check adds `class` to a linked line)
    given = (r.run / "normalised" / f"{EMBER}.md").read_text()
    assert '"class"' in given and "ledger-v1" in given
    for run in (ok_runs.rl, ok_runs.problem):
        merged = (run.run / "merged" / "merged-1.md").read_text()
        ledger = (run.run / "merged" / "ledger.json").read_text()
        assert "ledger-v1" not in merged and "ledger-v1" not in ledger
        # the words are checked as keys: the invented plan itself says `src/exporter/` in a quote
        assert not re.search(r'"(probe|src|class)"\s*:', merged)
        assert not set(KEYS) & set(keys_in(json.loads(ledger)))
        assert "probe" not in merged and "class" not in merged
    assert "blocking" in (r.run / "merged" / "merged-1.md").read_text().lower()
    assert r.js("run.json")["merge_refused"] is False and {L1, L2} <= set(
        r.js("run.json")["reviewers"]
    )

"""REQ-24, DESIGN 12.1 and 12.5: S1 on the largest tree (the repository itself) stays under the kill limit.

The kill limit is `min(cap_s, frac_of_b * b)` (DESIGN 12.2, config/values.json `kill_s`). The tightest limit of the
study is the smallest `b` in the config (100 s, so 10 s). The test runs bin/time-prepass.sh, which times the whole
`sweep prepass` command, on the repository root with the F-PLAN-1 plan and its source, and fails if the measured
seconds reach that limit. The measured seconds are written to a record file under pytest's tmp_path, never into SW.
"""

import json
import re
import subprocess

import pytest
from helpers import REPO, SW


def kill_limit_s() -> float:
    """The strictest kill limit of config/values.json: min(cap_s, frac_of_b * smallest b of any panel and document)."""
    values = json.loads((SW / "config" / "values.json").read_text(encoding="utf-8"))
    smallest_b = min(b for panel in values["b"].values() for b in panel.values())
    return min(values["kill_s"]["cap_s"], values["kill_s"]["frac_of_b"] * smallest_b)


@pytest.mark.slow
def test_largest_tree_under_kill_limit(tmp_path):
    record = tmp_path / "timing.tsv"
    r = subprocess.run(
        [
            "bash",
            str(SW / "bin" / "time-prepass.sh"),
            "--record",
            str(record),
            str(REPO),
        ],
        capture_output=True,
        text=True,
    )
    assert r.returncode == 0, r.stdout + r.stderr
    m = re.search(r"^prepass_s=([0-9.]+) rc=0 ", r.stdout, re.M)
    assert m, r.stdout
    seconds = float(m.group(1))
    limit = kill_limit_s()
    assert seconds < limit, (
        f"S1 on the repository root took {seconds} s, the kill limit is {limit} s: "
        "revisit DD-5 (scope) and DD-10 (attach bound), IMPLEMENTATION step 9 checkpoint"
    )
    line = record.read_text(encoding="utf-8").splitlines()
    assert len(line) == 1 and line[0].split("\t")[1] == str(REPO)

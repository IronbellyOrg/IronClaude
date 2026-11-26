"""bin/open-manual-checks.sh (TESTING section 6 item 4) and bin/check-sandbox-gt.sh (REQ-34, the real-run check)."""

import json
import re
import subprocess

from helpers import SW
from panel_support import make_world

OPEN = SW / "bin" / "open-manual-checks.sh"
SANDBOX_GT = SW / "bin" / "check-sandbox-gt.sh"


def open_checks(roots, *extra):
    r = subprocess.run(
        ["bash", str(OPEN), *map(str, extra)],
        capture_output=True,
        text=True,
        env=roots.with_env(),
    )
    assert r.returncode == 0, r.stderr  # it reports; it never gates
    return r.stdout.splitlines()


def test_open_records_are_listed_for_this_tree(tmp_roots):
    lines = open_checks(tmp_roots)
    open_ids = [
        m.group(1) for m in (re.match(r"OPEN (\S+?): ", ln) for ln in lines) if m
    ]
    assert lines[-1] == f"open: {len(open_ids)}"
    # nothing of the manual side has been done in this build: the eight swap tests, the authors file, the second reader,
    # the owner values, the spike, the attestations
    for n in range(1, 9):
        assert f"swap:C{n}" in open_ids
    for want in (
        "recall-authors",
        "readme-second-reader",
        "owner-values",
        "spike",
        "gt-attestation",
        "attest:freeze-order",
        "attest:prereg-order",
        "attest:report-claims",
        "model-stage-ablation",
    ):
        assert want in open_ids, want


def test_closing_records_removes_them_from_the_list(tmp_roots, tmp_path):
    tree = tmp_path / "tree"
    for n in range(1, 9):
        (tree / "cards").mkdir(parents=True, exist_ok=True)
        (tree / "cards" / f"C{n}.json").write_text(
            json.dumps({"swap_test": {"reviewer": "A. Second", "date": "2026-11-20"}})
        )
    (tree / "cards" / "README.md").write_text(
        "- Second reader of this table: reader: B, date: 2026-11-21. Status: DONE.\n"
    )
    (tree / "fixtures" / "recall").mkdir(parents=True)
    (tree / "fixtures" / "recall" / "AUTHORS.md").write_text(
        "Seeded by A. Second, who had not read the extractors.\n"
    )
    (tree / "config").mkdir()
    (tree / "config" / "prereg.json").write_text(json.dumps({"owner_confirmed": True}))
    (tree / "config" / "values.json").write_text(
        json.dumps({"spike": {"runs": 5, "c_luna": 2.0}})
    )
    (tree / "config" / "attestation.md").write_text("signed\n")
    (tree / "results").mkdir()
    ids = (
        "freeze-order",
        "prereg-order",
        "report-measured-values",
        "report-headline",
        "report-claims",
    )
    (tree / "results" / "attestations.md").write_text(
        "\n".join(f"ATTEST {i}: C. Reader, 2026-11-22, confirmed" for i in ids) + "\n"
    )
    lines = open_checks(tmp_roots, "--sw", tree)
    assert lines == [
        "OPEN model-stage-ablation: not run: 8 extra arms and 96 panel runs outside the run budget; an owner decision (DD-13)",
        "open: 1",
    ]
    # one record reopened: the attestation line for the claims is missing again, and a card loses its signature
    (tree / "results" / "attestations.md").write_text(
        "\n".join(f"ATTEST {i}: C. Reader, 2026-11-22, confirmed" for i in ids[:-1])
        + "\n"
    )
    (tree / "cards" / "C3.json").write_text(
        json.dumps({"swap_test": {"reviewer": "", "date": ""}})
    )
    lines = open_checks(tmp_roots, "--sw", tree)
    assert [ln.split(":")[0] for ln in lines[:-1]] == [
        "OPEN swap",
        "OPEN attest",
        "OPEN model-stage-ablation",
    ] and lines[-1] == "open: 3"
    assert (
        subprocess.run(
            ["bash", str(OPEN), "--sw", "/etc"],
            capture_output=True,
            text=True,
            env=tmp_roots.with_env(),
        ).returncode
        == 2
    )


def test_sandbox_ground_truth_check_is_clean_over_built_sandboxes(tmp_roots):
    w = make_world(
        tmp_roots
    )  # F-REPO with its trap file named ground-truth.json, built into a sandbox by build-sandbox.sh
    r = w.run("SS", "ss")  # a run that has prepass/sheets
    assert r.returncode == 0, r.stderr
    assert (r.dir / "prepass" / "sheets").is_dir()
    cmd = [
        "bash",
        str(SANDBOX_GT),
        "--sb",
        str(tmp_roots.sb),
        "--runs",
        str(tmp_roots.runs),
    ]
    out = subprocess.run(cmd, capture_output=True, text=True, env=tmp_roots.with_env())
    assert (out.returncode, out.stdout, out.stderr) == (
        0,
        "",
        "",
    )  # exits 0 with no output
    # a ground-truth file in the sandbox, and a field name in a sheet, are found
    (w.sandbox / "ground-truth.json").write_text("{}\n")
    out = subprocess.run(cmd, capture_output=True, text=True, env=tmp_roots.with_env())
    assert (
        out.returncode == 1
        and f"{w.sandbox}/ground-truth.json: a file named like ground truth"
        in out.stdout
    )
    (w.sandbox / "ground-truth.json").unlink()
    sheet = next((r.dir / "prepass" / "sheets").glob("*.md"))
    sheet.write_text(sheet.read_text() + "\nplan_quote: x\n")
    out = subprocess.run(cmd, capture_output=True, text=True, env=tmp_roots.with_env())
    assert (
        out.returncode == 1 and f"{sheet}:" in out.stdout and "plan_quote" in out.stdout
    )
    # no sandbox at all: nothing could be checked, which is not a pass
    none = subprocess.run(
        ["bash", str(SANDBOX_GT), "--sb", str(tmp_roots.root / "empty")],
        capture_output=True,
        text=True,
        env=tmp_roots.with_env(),
    )
    assert none.returncode == 2 and "E_NO_SANDBOX" in none.stderr

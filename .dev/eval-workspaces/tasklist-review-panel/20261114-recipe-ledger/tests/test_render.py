"""REQ-01, REQ-05 (RL parts), REQ-09, REQ-25 (brief part), REQ-34 (no markers), DR-2, DR-3, DR-7, DR-4 (cli): the RL brief,
the run.json fields and the `lens` subcommand. MR is read as a file; nothing else outside RL is."""

import difflib
import hashlib
import json
import subprocess
import sys

import pytest
from helpers import REPO, SW
from rl_support import (
    CLASSES,
    DOC,
    LENSES,
    PANELS,
    RECIPES_JSON,
    REQ25,
    SEP,
    SOURCE,
    TABLE,
    recipe_paragraphs,
    rl_briefs,
    roles,
    z0,
)

from fixtures.lens.make_lens import invalid_tables, write_table
from rl import cli, render
from scaffold import briefs

MR = (
    REPO
    / ".dev/brainstorms/20261113-223124-panel-process-redesign/merged-requirements.md"
)
MR_BLOCK = briefs.mr_quote(MR.read_text(encoding="utf-8"), "RECIPES AND LEDGER.")
RULE = (SW / "briefs" / "ledger-rule.txt").read_text(encoding="utf-8").rstrip("\n")
SEARCH_FORM = (
    (SW / "recipes" / "search-form.txt").read_text(encoding="utf-8").rstrip("\n")
)
PLAN = SW / "fixtures" / "plans" / "p_basic.md"
PLAN_SOURCE = SW / "fixtures" / "plans" / "source.md"
GT_MARKERS = ("ground-truth", "ground_truth", "plan_quote", "TASK-WF-", "score.json")


def lens_args(out, *extra, source=True):
    args = [
        "lens",
        "--panel",
        "primary",
        "--doc",
        "doc-1",
        "--candidate-sb",
        str(PLAN),
        "--out",
        str(out),
    ]
    if source:
        args += ["--source", str(PLAN_SOURCE)]
    return [*args, *extra]


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


# ---- REQ-01, DR-7


def test_cb1_present_with_source():
    for role, b in rl_briefs("primary").items():
        assert b["text"].count(f"Driving document: {SOURCE}.") == 1
        assert b["no_source"] is False
        has_c2 = "C2" in TABLE["panels"]["primary"]["roles"][role]["lens"]
        assert ("R-C2. " in b["text"]) is has_c2


@pytest.mark.parametrize("panel", PANELS)
def test_cb1_absent_without_source(panel):
    for b in rl_briefs(panel, source=None).values():
        assert "Driving document:" not in b["text"] and b["no_source"] is True
        assert "R-C2. " not in b["text"]
        assert RECIPES_JSON["C2"]["text"][:60] not in b["text"]
        for cb in ("cb2", "cb3", "cb4", "cb5"):
            assert cb in b["parts"]


@pytest.mark.parametrize("panel", PANELS)
def test_c2_recipe_dropped_without_source(panel):
    for role, b in rl_briefs(panel, source=None).items():
        assert "C2" not in b["recipes"]
        ids = [c for c, _ in recipe_paragraphs(b["text"])]
        assert ids == [
            c for c in TABLE["panels"][panel]["roles"][role]["lens"] if c != "C2"
        ]
        assert len(ids) >= 2


def test_no_source_flags_in_run_json():
    kw = {"b": 100, "c_by_model": {}, "lenses_path": LENSES}
    for has_source in (False, True):
        r = roles("primary", has_source)
        kw["c_by_model"] = {x["model"]: 1 for x in r.values()}
        f = render.run_fields(r, has_source=has_source, **kw)
        assert f["no_source"] is (not has_source)
        assert f["c2_not_applicable"] is (not has_source)


# ---- REQ-05 RL parts, DR-2, DR-3


@pytest.mark.parametrize("panel", PANELS)
def test_rl_brief_starts_with_z0_text(panel):
    base = z0()
    for b in rl_briefs(panel).values():
        assert b["text"].startswith(base["text"] + SEP + RULE + SEP)
        assert b["z0_sha256"] == base["sha256"]
        assert b["parts"][: len(base["parts"])] == base["parts"]
    # the same holds without a source: the prefix is that state's Z0 brief
    for b in rl_briefs(panel, source=None).values():
        assert b["text"].startswith(z0(None)["text"] + SEP + RULE + SEP)


@pytest.mark.parametrize("panel", PANELS)
def test_fallback_brief_equals_z0_by_hash(panel):
    for source in (SOURCE, None):
        for role, r in roles(panel, bool(source)).items():
            b = render.brief(r, DOC, source, fallback=True)
            assert b["sha256"] == z0(source)["sha256"] == b["z0_sha256"]
            assert b["text"] == z0(source)["text"] and b["fallback"] is True
            assert b["recipes"] == [] and b["parts"] == z0(source)["parts"]


@pytest.mark.parametrize("panel", PANELS)
def test_rl_part_order(panel):
    for role, b in rl_briefs(panel).items():
        r = roles(panel)[role]
        tail = [f"R-{c}" for c in r["recipes"]]
        assert b["parts"] == [
            *z0()["parts"],
            "ledger-rule",
            "rl-block",
            "recipes-heading",
            *tail,
            *(["search-form"] if r["search_form"] else []),
        ]
        block = render.rl_block(r["row_cap"])
        paragraphs = [RECIPES_JSON[c]["text"] for c in r["recipes"]]
        want = SEP.join(
            [
                z0()["text"],
                RULE,
                block,
                "## RECIPES ASSIGNED TO YOU",
                *(f"R-{c}. {t}" for c, t in zip(r["recipes"], paragraphs)),
                *([SEARCH_FORM] if r["search_form"] else []),
            ]
        )
        assert b["text"] == want and b["sha256"] == briefs.sha256_text(want)
        at = [b["text"].index(x) for x in (RULE, block, "## RECIPES ASSIGNED TO YOU")]
        assert at == sorted(at) and len(set(at)) == 3


def test_row_cap_placeholder_equals_mr_at_14():
    assert render.rl_block(14) == MR_BLOCK
    assert render.PLACEHOLDER in (SW / "recipes" / "rl-block.txt").read_text()
    for panel in PANELS:
        for b in rl_briefs(panel).values():
            assert render.PLACEHOLDER not in b["text"]
    for b in rl_briefs("primary").values():  # every primary lens has the cap 14
        assert MR_BLOCK in b["text"]


@pytest.mark.parametrize("cap", [6, 8])
def test_other_cap_changes_only_the_number(cap):
    block = render.rl_block(cap)
    assert block == MR_BLOCK.replace("more than 14 rows", f"more than {cap} rows")
    old, new = MR_BLOCK.split(), block.split()
    assert len(old) == len(new)
    assert [(a, b) for a, b in zip(old, new) if a != b] == [("14", str(cap))]
    assert difflib.SequenceMatcher(None, MR_BLOCK, block).ratio() > 0.99


@pytest.mark.parametrize("panel", PANELS)
def test_row_cap_in_brief_is_the_lens_row_cap(panel):
    for role, b in rl_briefs(panel).items():
        cap = roles(panel)[role]["row_cap"]
        assert f"never write more than {cap} rows." in b["text"]
    assert [x["row_cap"] for x in roles("haiku").values()][0] == 6


# ---- REQ-09, REQ-34


@pytest.mark.parametrize("source", [SOURCE, None])
def test_no_src_path_in_any_brief(source):
    seen = 0
    for arm in ("Z0-raw", "Z0", "K"):
        assert "src/superclaude/" not in briefs.render(arm, DOC, None, source)["text"]
        seen += 1
    for panel in PANELS:
        for role, r in roles(panel, bool(source)).items():
            for fallback in (False, True):
                text = render.brief(r, DOC, source, fallback=fallback)["text"]
                assert "src/superclaude/" not in text, (panel, role, fallback)
                seen += 1
    assert seen == 3 + 3 * 3 * 2


def test_briefs_hold_no_gt_markers():
    for panel in PANELS:
        for source in (SOURCE, None):
            for b in rl_briefs(panel, source).values():
                low = b["text"].lower()
                assert not [m for m in GT_MARKERS if m.lower() in low]


# ---- REQ-25, brief part


@pytest.mark.parametrize("panel", PANELS)
def test_generated_briefs_match_lens_table(panel):
    seen: dict[str, int] = {}
    for role, b in rl_briefs(panel).items():
        spec = TABLE["panels"][panel]["roles"][role]
        found = recipe_paragraphs(b["text"])
        assert 2 <= len(found) <= 4
        assert [c for c, _ in found] == spec["lens"]
        for c, p in found:
            assert p == f"R-{c}. {RECIPES_JSON[c]['text']}"
            seen[c] = seen.get(c, 0) + 1
        assert (SEARCH_FORM in b["text"]) is spec["search_form"]
        assert b["text"].count(SEARCH_FORM) == int(spec["search_form"])
    assert set(seen) == set(CLASSES)
    assert {c for c, n in seen.items() if n > 1} == REQ25[panel]


# ---- determinism (DESIGN 2.4)


def test_byte_identical_same_inputs():
    for panel in PANELS:
        a, b = rl_briefs(panel), rl_briefs(panel)
        assert {k: v["text"] for k, v in a.items()} == {
            k: v["text"] for k, v in b.items()
        }
        assert {k: v["sha256"] for k, v in a.items()} == {
            k: v["sha256"] for k, v in b.items()
        }


def test_cli_byte_identical_same_inputs(tmp_path):
    for n in (1, 2):
        assert cli.main(lens_args(tmp_path / f"r{n}")) == 0
    files = sorted(p.relative_to(tmp_path / "r1") for p in (tmp_path / "r1").rglob("*"))
    assert files == sorted(
        p.relative_to(tmp_path / "r2") for p in (tmp_path / "r2").rglob("*")
    )
    for f in files:
        if (tmp_path / "r1" / f).is_file():
            assert sha(tmp_path / "r1" / f) == sha(tmp_path / "r2" / f), f


# ---- the `lens` subcommand


def test_cli_writes_lens_briefs_and_run_json(tmp_path):
    out = tmp_path / "run"
    assert cli.main(lens_args(out)) == 0
    rids = {"t2b-1", "t4-1", "t3-1"}
    assert {p.stem for p in (out / "lens").iterdir()} == rids
    assert {p.name for p in (out / "briefs").iterdir()} == {
        f"{r}.{e}" for r in rids for e in ("txt", "sha256")
    }
    for rid in rids:
        txt = out / "briefs" / f"{rid}.txt"
        assert (out / "briefs" / f"{rid}.sha256").read_text() == sha(txt) + "\n"
        assert txt.read_text(encoding="utf-8").startswith(
            briefs.render(
                "Z0",
                {"cand_sb": str(PLAN), "sha": sha(PLAN)},
                None,
                str(PLAN_SOURCE),
            )["text"]
        )
    info = json.loads((out / "lens" / "t4-1.json").read_text(encoding="utf-8"))
    assert info["recipes"] == ["C1", "C2", "C3"] and info["row_cap"] == 14
    assert info["assigned_ids"][0] == "C1.1" and info["role"] == "L1"
    assert (info["panel"], info["doc"], info["b"], info["c"]) == (
        "primary",
        "doc-1",
        100,
        2,
    )
    run = json.loads((out / "run.json").read_text(encoding="utf-8"))
    assert run["no_source"] is False and run["c2_not_applicable"] is False
    assert run["no_budget"] is False and run["fallback"] is False
    assert run["lenses_sha256"] == sha(LENSES)
    assert run["recipes_sha256"] == sha(SW / "recipes" / "recipes.json")
    assert (
        run["reviewers"]["t2b-1"]["b"] == 100 and run["reviewers"]["t2b-1"]["c"] == 0.4
    )
    assert run["reviewers"]["t4-1"]["brief_sha256"] == sha(out / "briefs" / "t4-1.txt")
    assert (
        run["z0_sha256"]
        == briefs.render(
            "Z0", {"cand_sb": str(PLAN), "sha": sha(PLAN)}, None, str(PLAN_SOURCE)
        )["sha256"]
    )
    for p in out.rglob("*.json"):  # sorted keys, no ASCII escapes, trailing newline
        text = p.read_text(encoding="utf-8")
        assert text == render.dumps(json.loads(text)) and text.endswith("}\n")


def test_cli_merges_into_an_existing_run_json(tmp_path):
    (tmp_path / "run.json").write_text('{"arm": "RL", "seed": 7}\n')
    assert cli.main(lens_args(tmp_path)) == 0
    run = json.loads((tmp_path / "run.json").read_text())
    assert (run["arm"], run["seed"], run["panel"]) == ("RL", 7, "primary")


def test_cli_without_source(tmp_path):
    assert cli.main(lens_args(tmp_path, source=False)) == 0
    run = json.loads((tmp_path / "run.json").read_text())
    assert run["no_source"] is True and run["c2_not_applicable"] is True
    for p in (tmp_path / "briefs").glob("*.txt"):
        text = p.read_text(encoding="utf-8")
        assert "Driving document:" not in text and "R-C2. " not in text
    info = json.loads((tmp_path / "lens" / "t4-1.json").read_text())
    assert info["recipes"] == ["C1", "C3"] and info["has_source"] is False


def test_cli_runs_as_a_script_by_path(tmp_path):
    r = subprocess.run(
        [sys.executable, str(SW / "rl" / "cli.py"), "lens", "--validate"],
        capture_output=True,
        text=True,
        cwd=tmp_path,
        env={"PATH": "/usr/bin:/bin", "PYTHONDONTWRITEBYTECODE": "1"},
    )
    assert r.returncode == 0, r.stderr
    for name in PANELS:
        assert f"{name}: " in r.stdout
    assert r.stdout.count("lens=") == 9


@pytest.mark.parametrize("name", sorted(invalid_tables()))
def test_bad_lens_table_exits_non_zero_with_e_lens_invalid(name, tmp_path, capsys):
    rule, table = invalid_tables()[name]
    bad = write_table(tmp_path / "bad.json", table)
    assert cli.main(["lens", "--validate", "--lenses", str(bad)]) == 1
    assert "E_LENS_INVALID" in capsys.readouterr().err
    out = tmp_path / "run"
    assert cli.main(lens_args(out, "--lenses", str(bad))) == 1
    assert f"rule {rule}" in capsys.readouterr().err
    err = json.loads((out / "lens" / "error.json").read_text())
    assert err["reason"] == "lens_invalid" and err["error"] == "LensInvalid"
    assert not (out / "briefs").exists() and not (out / "run.json").exists()


def test_cli_no_budget_exits_3(tmp_path):
    assert cli.main(lens_args(tmp_path, "--b", "20")) == 3
    run = json.loads((tmp_path / "run.json").read_text())
    assert run["no_budget"] is True and run["reviewers"]["t4-1"]["row_cap"] == 0


def test_cli_forced_exception_exits_1_with_error_file(tmp_path, monkeypatch):
    monkeypatch.setenv("RL_FORCE_EXC", "lens")
    assert cli.main(lens_args(tmp_path)) == 1
    err = json.loads((tmp_path / "lens" / "error.json").read_text())
    assert (err["error"], err["reason"]) == ("RuntimeError", "error")
    assert not (tmp_path / "briefs").exists()


@pytest.mark.parametrize("bad_table", [False, True])
def test_cli_fallback_writes_the_z0_briefs(bad_table, tmp_path):
    extra = ["--fallback", "lens_invalid" if bad_table else "error"]
    if bad_table:
        _, table = invalid_tables()["class_in_no_lens"]
        extra += ["--lenses", str(write_table(tmp_path / "bad.json", table))]
    assert cli.main(lens_args(tmp_path / "run", *extra)) == 0
    z0_sha = briefs.render(
        "Z0", {"cand_sb": str(PLAN), "sha": sha(PLAN)}, None, str(PLAN_SOURCE)
    )["sha256"]
    run = json.loads((tmp_path / "run" / "run.json").read_text())
    assert run["fallback"] is True and run["fallback_reason"] == extra[1]
    for rid in ("t2b-1", "t3-1", "t4-1"):
        assert (
            tmp_path / "run" / "briefs" / f"{rid}.sha256"
        ).read_text() == z0_sha + "\n"
        assert set(run["reviewers"][rid]) == {"model", "brief_sha256"}
    assert not (tmp_path / "run" / "lens").exists()


def test_cli_refuses_a_source_that_disagrees_with_packages(tmp_path, capsys):
    pk = tmp_path / "packages.json"
    for declared, source in ((None, True), ("x.md", False)):
        pk.write_text(json.dumps({"packages": {"doc-1": {"source": declared}}}))
        args = lens_args(tmp_path / "run", "--packages", str(pk), source=source)
        assert cli.main(args) == 2
        assert "packages.json source" in capsys.readouterr().err
        assert not (tmp_path / "run").exists()


def test_cli_usage_errors_exit_2(tmp_path, capsys):
    assert cli.main(["lens", "--panel", "primary"]) == 2
    assert "--doc" in capsys.readouterr().err
    args = lens_args(tmp_path)
    args[args.index("--candidate-sb") + 1] = str(tmp_path / "missing.md")
    assert cli.main(args) == 2
    args = lens_args(tmp_path)
    args[args.index("--panel") + 1] = "nosuch"
    assert cli.main(args) == 2

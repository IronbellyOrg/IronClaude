"""The shadow-mode text of the reflect skill (Task 19): where it may change, the brief template, a fixture run directory."""

from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path

import pytest
from click.testing import CliRunner

from superclaude.cli.main import main
from superclaude.cli.review import panel as pnl

ROOT = Path(__file__).resolve().parents[3]
SKILL_REL = "src/superclaude/skills/sc-reflect-protocol/SKILL.md"
SKILL = ROOT / SKILL_REL
SPEC = ROOT / "src/superclaude/skills/sc-reflect-protocol/refs/reviewer-spec.md"
SKILL_DIR = ROOT / "src/superclaude/skills/sc-reflect-protocol"


def git(*args: str) -> str | None:
    try:
        out = subprocess.run(
            ["git", *args], cwd=ROOT, capture_output=True, text=True, timeout=60
        )
    except (OSError, subprocess.SubprocessError):
        return None
    return out.stdout if out.returncode == 0 else None


def block_after(text: str, heading: str) -> str:
    start = text.index(heading)
    first = text.index("```yaml\n", start)
    return text[first : text.index("\n```", first)]


# ------------------------------------------------------------ where the skill may change (AC1)


def test_stable_contract_block_and_version_are_byte_identical_to_head():
    head = git("show", f"HEAD:{SKILL_REL}")
    if head is None:
        pytest.skip("no git history for the skill")
    heading = "### 9.1 Stable contract (contract_version: 1.8.0)"
    current = SKILL.read_text(encoding="utf-8")
    assert block_after(current, heading) == block_after(head, heading)
    assert 'contract_version: "1.8.0"' in block_after(current, heading)


def test_skill_changes_are_confined_to_the_allowed_sections():
    diff = git("diff", "HEAD", "-U0", "--", SKILL_REL)
    if diff is None:
        pytest.skip("no git history for the skill")
    lines = SKILL.read_text(encoding="utf-8").splitlines()
    headings = [
        (i, text) for i, text in enumerate(lines, 1) if re.match(r"^#{2,4} ", text)
    ]

    def section(lineno: int) -> str:
        above = [h for i, h in headings if i <= lineno]
        return above[-1] if above else ""

    allowed = ("### 3.1 ", "### 4.3a ", "### 5.4 ", "### 9.2 ")
    seen = set()
    for m in re.finditer(r"^@@ -\d+(?:,\d+)? \+(\d+)(?:,(\d+))? @@", diff, re.M):
        start, count = int(m.group(1)), int(m.group(2) or 1)
        for n in range(start, start + max(count, 1)):
            sec = section(n)
            seen.add(sec)
            assert sec.startswith(allowed), f"line {n} changed under {sec!r}"
            if sec.startswith("### 3.1 "):
                assert "--t2-engine" in lines[n - 1]
    assert not any(s.startswith("### 9.1 ") for s in seen)


def test_no_new_src_superclaude_hit_in_the_skill_directory():
    head = git(
        "grep",
        "-c",
        "src/superclaude",
        "HEAD",
        "--",
        "src/superclaude/skills/sc-reflect-protocol",
    )
    if head is None:
        pytest.skip("no git history for the skill")
    # `git grep -c` counts lines, so count lines on the working side too
    before = sum(int(row.rsplit(":", 1)[1]) for row in head.splitlines())
    now = sum(
        1
        for p in SKILL_DIR.rglob("*")
        if p.is_file()
        for line in p.read_text(encoding="utf-8", errors="replace").splitlines()
        if "src/superclaude" in line
    )
    assert now <= before


# ------------------------------------------------------------ the manifest recipe as the skill writes it


def test_the_skills_manifest_recipe_runs_as_written(tmp_path):
    """Follow the shadow steps literally: init, resolved with --payload, attempts before each advance, published."""
    sha = "a" * 64
    snap = tmp_path / "artifacts" / "input-snapshot.yaml"
    snap.parent.mkdir()
    snap.write_text(f"input_tree_sha256: {sha}\nfile_list: []\n")
    out = ["--out", str(tmp_path)]

    def run(*args):
        res = CliRunner().invoke(main, ["review", "manifest", *args])
        assert res.exit_code == 0, res.output
        return res

    run(
        "init", *out, "--run-id", "r1", "--snapshot", str(snap),
        "--template-sha256", sha, "--tiers-sha256", sha, "--brief-template-sha256", sha,
        "--schema-id", "review-panel/1", "--schema-id", "findings-v2",
        "--t2-engine-requested", "shadow", "--t2-engine-effective", "shadow",
    )  # fmt: skip
    payload = tmp_path / "resolved.json"
    payload.write_text(json.dumps({"reviewers_requested": 3, "reviewers_resolved": 3}))
    run("advance", *out, "--stage", "resolved", "--payload", str(payload))
    for stage in ("dispatched", "collected"):
        for rid in ("t1b-1", "t4-1", "t1a-1"):
            run(
                "advance", *out, "--stage", stage, "--reviewer-id", rid,
                "--attempt-id", "1", "--completion", "complete",
            )  # fmt: skip
        run("advance", *out, "--stage", stage)
    for stage in ("calibrated", "clustered", "debated", "validated"):
        run("advance", *out, "--stage", stage)
    for name in ("REPORT.md", "return-contract.yaml", "audit.log"):
        (tmp_path / name).write_text("legacy writer output\n")
    run("advance", *out, "--stage", "published")
    manifest = json.loads((tmp_path / "panel/manifest.json").read_text())
    assert manifest["state"] == "published" and manifest["reviewers_complete"] == 3
    assert manifest["reviewers_resolved"] == 3


# ------------------------------------------------------------ the brief template (AC2)


def test_the_brief_template_has_exactly_three_sections():
    text = SPEC.read_text(encoding="utf-8")
    region = text[
        text.index("### Required sections (per brief)") : text.index(
            "### Contract emission"
        )
    ]
    assert re.findall(r"(?m)^#### `(## [^`]+)`", region) == [
        "## T1 card excerpt",
        "## Grounding hunks",
        "## Coverage slice",
    ]
    # the shadow instruction lives inside the T1 card excerpt section, not in a section of its own
    excerpt = region[
        region.index("#### `## T1 card excerpt`") : region.index(
            "#### `## Grounding hunks`"
        )
    ]
    assert "findings-v2" in excerpt and "reviewer_model_self_report" in excerpt
    assert "legacy run's briefs do not carry this line" in excerpt


def test_skill_names_the_card_header_fields_and_the_authority_of_the_legacy_path():
    text = SKILL.read_text(encoding="utf-8")
    shadow = text[text.index("**Shadow-mode steps") : text.index("### 4.5 ")]
    for needle in (
        "`persona:`",
        "`model_class:`",
        "`model:`",
        "unmodified output of `review panel resolve`",
        "authoritative and unchanged",
    ):
        assert needle in shadow
    assert "manifest advance" in shadow and "kept-ids.txt" in shadow
    assert "judge_class_collision: unknown" in shadow


def test_the_calibrator_line_is_shadow_only_and_its_example_is_read_by_the_cluster_command():
    from superclaude.cli.review.cluster_cmd import _embedded_calibration

    text = SKILL.read_text(encoding="utf-8")
    step5 = text[text.index("5. **Calibration.**") : text.index("6. **Clustering")]
    line = re.search(r"`(Also report one confidence[^`]+)`", step5)
    assert line, "the literal calibrator line is missing from step 5"
    assert "Your card score is unchanged." in line.group(1)
    assert "a legacy run's calibrator brief does not carry the line" in step5
    # the block the line asks for is the one the cluster command reads
    card = "## Findings block\n\n```yaml\ncalibration:\n  per_finding:\n    F1: 0.85\n```\n"
    assert _embedded_calibration(card) == {"F1": 0.85}
    # and the line is written only in the shadow steps, never in the legacy Wave 3C text
    assert text.count(line.group(1)) == 1


def test_the_reviewer_brief_line_carries_the_schema_and_its_example_parses():
    from superclaude.cli.review import findings as f1
    from superclaude.cli.review import findings_v2 as fv2

    text = SPEC.read_text(encoding="utf-8")
    line = re.search(r"`(End your card with a ## Findings block[^`]+)`", text).group(1)
    for word in ("JSON lines", "never a table", *f1.SEVERITIES, *f1.CATEGORIES):
        assert word in line, word
    example = re.search(r"Example line: (\{.*\}\]\})\. After the block", line).group(1)
    block = f"## Findings block\n\n```findings-v2\n{example}\n```\n"
    parsed = fv2.parse_block(
        block, lens="reflect-pre", assigned_rows=["R-1"], observed_rows=["R-1"]
    )
    assert parsed["ok"], parsed["errors"]


def test_shadow_steps_pin_the_header_model_the_verdict_file_and_the_first_pass_metric():
    text = SKILL.read_text(encoding="utf-8")
    shadow = text[text.index("**Shadow-mode steps") : text.index("### 4.5 ")]
    # parity: the header model is the pin, the harness model goes on its own line
    assert (
        "copied verbatim from `reviewers[N].model` of `panel/resolution.json`" in shadow
    )
    assert "`model_observed:`" in shadow
    # compliance: first parse, before any re-ask, and the orchestrator never remaps
    assert "valid on this first parse" in shadow and "before any re-ask" in shadow
    assert "never edits, remaps or normalizes a reviewer's findings itself" in shadow
    assert "first parse (before any re-ask)" in text  # the section 9.2 definition
    # EV-1: the step that writes the file the rule reads
    assert "write `<output>/adversarial/merged-verdict.yaml`" in shadow
    assert "`adversarial/adversarial/`" in shadow
    # contract: the legacy rotation keys and no new top-level key
    assert "`reviewer_personas` and `reviewer_models`" in shadow
    assert "every shadow field goes under `telemetry:`" in shadow


# ------------------------------------------------------------ a fixture run directory (AC3)

RESOLVE = [
    "review", "panel", "resolve", "--template", "@reflect-pre", "--run-id", "r1",
    "--kind", "first", "--env", "anthropic-only", "--strict-distinct",
]  # fmt: skip
PERSONAS = ("analyzer", "qa", "refactorer")


def recompute_parity(run: Path, legacy: list[tuple[str, str]]) -> bool:
    """Ordered (persona, model class) pairs of the resolution against the card headers and the legacy rotation."""
    classes = pnl.load_tiers()["classes"]
    resolution = json.loads((run / "panel/resolution.json").read_text())
    expected = [
        (PERSONAS[i], classes[r["model"]])
        for i, r in enumerate(resolution["reviewers"])
    ]
    cards = []
    for n in range(1, len(expected) + 1):
        head = (
            (run / "panel/cards" / f"reviewer-{n}.md").read_text().split("\n\n", 1)[0]
        )
        fields = dict(row.split(": ", 1) for row in head.splitlines() if ": " in row)
        assert set(fields) >= {"persona", "model_class", "model"}
        assert fields["model"] == resolution["reviewers"][n - 1]["model"]
        cards.append((fields["persona"], fields["model_class"]))
    return cards == expected == legacy


def build_run(tmp_path: Path) -> tuple[Path, str]:
    run = tmp_path / "pre-run"
    (run / "panel/cards").mkdir(parents=True)
    raw = CliRunner().invoke(main, RESOLVE).output
    (run / "panel/resolution.json").write_text(raw)
    for n, r in enumerate(json.loads(raw)["reviewers"], 1):
        cls = pnl.load_tiers()["classes"][r["model"]]
        (run / "panel/cards" / f"reviewer-{n}.md").write_text(
            f"persona: {PERSONAS[n - 1]}\nmodel_class: {cls}\nmodel: {r['model']}\n\n## Findings block\n"
        )
    return run, raw


def test_shadow_card_headers_and_resolution_json_on_a_fixture_run(tmp_path):
    run, raw = build_run(tmp_path)
    # panel/resolution.json is the raw, unmodified output of `review panel resolve`
    assert (
        (run / "panel/resolution.json").read_text()
        == CliRunner().invoke(main, RESOLVE).output
        == raw
    )
    legacy = [("analyzer", "sonnet"), ("qa", "haiku"), ("refactorer", "opus")]
    assert recompute_parity(run, legacy) is True
    # a legacy rotation that differs gives false and is only recorded
    assert (
        recompute_parity(
            run, [("analyzer", "sonnet"), ("qa", "opus"), ("refactorer", "haiku")]
        )
        is False
    )


def test_a_card_header_missing_a_field_is_caught(tmp_path):
    run, _ = build_run(tmp_path)
    card = run / "panel/cards/reviewer-2.md"
    card.write_text(card.read_text().replace("model_class: haiku\n", ""))
    with pytest.raises(AssertionError):
        recompute_parity(run, [])

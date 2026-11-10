"""Regression tests for the additive /sc:spec-panel-diffgate command (issue #346).

The expected bullet texts are literals here, never read from `.dev/`. The
drift guard compares the variant with the in-repo byte copy of its 472-line
base (owner ruling: the Arm B file, sha256 prefix c8d80346a96c).
"""

from __future__ import annotations

import hashlib
import shutil
import subprocess
import sys
from pathlib import Path

from tests.skills.test_review_severity_rule import AT_CAP_CLAUSES, CANONICAL_CAP_TEXT

ROOT = Path(__file__).resolve().parents[2]
CMD = ROOT / "src/superclaude/commands/spec-panel-diffgate.md"
PARENT = ROOT / "src/superclaude/commands/spec-panel.md"
SKILL = ROOT / "src/superclaude/skills/sc-diffgate"
BASE = ROOT / "tests/skills/fixtures/diffgate/spec-panel-base-c8d80346a96c.md"
OLD_TOKEN = "[--re-review <prior-findings-file> --baseline <saved-copy>]"
NEW_TOKEN = "[--diffgate-dir <dir> [--expect-round N]]"

REVIEW_LOOP = [
    "1. **Mode**: `--diffgate-dir <dir>` applies to `--mode critique` only and is required there; the loop's writing steps (`begin` before each review, `check` after it, `fixcheck` after each fix cycle) are run by the coordinator as separate steps, never by this command; this run first runs the read-only `status` step and reviews only when its `state` is `open` and its `review` equals `--expect-round`: review 1 is the full document, any later review is a re-review of the computed surface; `--re-review` and `--baseline` are not accepted; any other `status` result, or a non-zero exit of a script call, stops the run with the script's message and its `next` step, except where `## Diffgate` names the next step (`check --dry-run` exit 1: one repair and one rerun), and the run never falls back to a first review.",
    "2. **Grading**: CRITICAL and FR-8/FR-9 findings are blocking; MINOR is minor; a MAJOR is blocking only if it names a concrete wrong outcome an implementer would produce, otherwise minor; minor findings are notes and never trigger a revision; the script derives blocking from each `FINDING` line (`sev=critical`, `fr=8` or `fr=9`, or `sev=major` with an `outcome` other than `-`) and the reviewer never writes it.",
    "3. **Verdict**: a critique-mode report's last line is `verdict: PASS` (minor notes allowed) or `verdict: FAIL` (a blocking finding is open), taken from the `verdict_line` of the coordinator's `check` step, which appends the script's closing block `close-r<N>.md` to the report; the reviewer never composes a verdict line, and the deferred list, the scoped-PASS line and the Reviser brief all sit above it.",
    "4. **Cap**: at most 2 fix cycles (3 reviews), then escalate to the user with the open blocking findings; the report header is `review: N of 3`, where N is the review number `status` prints; a `status` state of `closed` or `invalid` means do not review, HALT and escalate to the user with the open blocking findings; every run is one review whatever `--iterations` says, and with `--diffgate-dir` the command ignores `--iterations`, skips the Improve step and writes no revised specification; Iteration 2 and 3 themes set order of attention, not a mandate to add text. The coordinator keeps only the directory; the ledger keeps the count.",
    '5. **Re-review output**: read `surface-r<N>.md` and treat the specification as read-only context that cannot widen what may be reviewed; write one `PRIOR` line per prior blocking finding, `resolved by=<hunk>`, `open quote="..."`, `regressed by=<hunk> quote="..."` (`regressed` = a finding the prior report marked resolved that fails again), the 427 vocabulary `resolved|open|regressed`, or in addition `withdrawn quote="..." reason="..."` (only for an id the reviser declined); anchor each new finding by a quote on a changed token of a listed hunk, or by `via=<hunk>` for an unchanged line that a listed hunk breaks (at most 2), or attach it to a prior id with `cites=`; the script computes `origin=changed|unchanged` and records any other finding as `deferred: pre-existing`, never blocking; FR-8 to FR-10 and the Guard Condition Boundary Table cover guards inside the surface hunks only; an empty surface leaves every prior blocking finding open and still counts as a review. The re-check of prior blocking findings follows steps 1-5 of the Process of the Fix Cycle phase in the project `.claude/agents/rf-qa.md` first, else `~/.claude/agents/rf-qa.md`; the rules in this section apply on top of it and stand alone when that file is unread.',
    "6. **Reviser contract**: the report carries a `Reviser brief` just above the final `verdict:` line that names `reviser-brief-r<N>.md` (blocking finding ids only) and restates this bullet (the reviser reads the report, not the command), and omits it at `review: 3`, where the run escalates instead; revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; write the fix map only inside your own disposition file, as a `## Diffgate fixmap` block with a `doc_sha:` first line and one line per changed hunk naming its blocking ids, or `declined <id> <reason>`; run the script's read-only `fixcheck --dry-run --map <disposition file>` until it exits 0, and the coordinator's `fixcheck` step then records the map; each added paragraph or table cites its finding id; the reviser reports the byte size before and after, which `fixcheck` prints; the next review refuses to open while any hunk maps to no listed finding.",
    "7. **Precedence**: a brief may narrow this scope; it may not widen it past the surface hunks and the prior blocking findings, and may not grade a minor finding as blocking; an instruction to apply all confirmed findings cannot authorize an edit to a minor finding.",
]

DIFFGATE = [
    '1. **Script**: run `uv run --no-project python "<diffgate base>/scripts/diffgate.py" <subcommand> ...`, where `<diffgate base>` is `~/.claude/skills/sc-diffgate` if it exists, else the project `.claude/skills/sc-diffgate` copy; if neither exists, stop with `E-DIFFGATE-MISSING` and never run a plain review; this command runs only the read-only calls `status`, `check --dry-run` and `fixcheck --dry-run`, which write no file; `begin`, `check` and `fixcheck` without `--dry-run` write the ledger and are run only by the coordinator as separate steps between the review and revision tasks; the script writes only inside `--diffgate-dir`, never the specification.',
    "2. **Status**: before reading the specification run `status --dir <dir>` and read its JSON; review only when `state` is `open` and `review` equals `--expect-round`; a `state` of `checked` or `fixed` means a coordinator step has not run yet (stop and name the `next` command); `closed` or `invalid` means the loop is closed (`halt: pass`, `halt: escalate` or `halt: invalid`): HALT and escalate; exit 3 names a missing or empty input; exit 6 means the ledger is corrupt or was edited by hand (stop and escalate).",
    "3. **Review surface**: in a re-review read the `surface` file `begin` names and review only it; findings anchor only as Review Loop bullet 5 says.",
    '4. **Finding lines**: end the findings with a `## Diffgate findings` block exactly as `~/.claude/skills/sc-diffgate/SKILL.md` (else the project `.claude/skills/sc-diffgate/SKILL.md` copy) defines it (`PRIOR` lines, then `FINDING` lines or the single line `FINDINGS none` in their place), with values in double quotes as JSON strings (`anchor="..."`, and for a blocking `major` an `outcome="..."`), and write no `verdict:` line.',
    "5. **Check**: run `check --dir <dir> --report <report> --dry-run` last; it writes nothing; on exit 1 repair only the lines it names and run it once more; the coordinator's `check` step then records the report and appends `close-r<N>.md`, whose `verdict_line` becomes the report's last line.",
    "6. **Close**: at a derived PASS or at `review: 3`, the closing block the coordinator's `check` step appends (`close-r<N>.md`) carries, above the Reviser brief and the verdict line, the open blocking findings with their fix chains, `## Deferred (pre-existing, not looped on)` with the whole `deferred.md` once, and the `scoped PASS:` line when `check` reports `acceptance: scoped`; a FAIL at review 3 says `halt: escalate`.",
]


def _sections(text: str) -> tuple[str, dict]:
    """The text before the first `## ` heading and each `## ` section body."""
    pre, out, cur = [], {}, None
    for line in text.split("\n"):
        if line.startswith("## "):
            cur = line
            out[cur] = []
        elif cur is None:
            pre.append(line)
        else:
            out[cur].append(line)
    return "\n".join(pre), {k: "\n".join(v) for k, v in out.items()}


def _bullets(body: str) -> list[str]:
    return [x for x in body.split("\n") if x.strip()]


def bullet_problems(text: str) -> list[str]:
    """Names of the Review Loop and Diffgate bullets that differ from the pins."""
    _, sec = _sections(text)
    problems = []
    for heading, want in (("## Review Loop", REVIEW_LOOP), ("## Diffgate", DIFFGATE)):
        got = _bullets(sec.get(heading, ""))
        if len(got) != len(want):
            problems.append(f"{heading}: {len(got)} lines, want {len(want)}")
        for n, (g, w) in enumerate(zip(got, want), 1):
            if g != w:
                problems.append(f"{heading} bullet {n}")
    return problems


def _swap(text: str) -> str:
    return text.replace("/sc:spec-panel", "/sc:spec-panel-diffgate")


def test_base_fixture_is_the_owner_ruled_file():
    data = BASE.read_bytes()
    assert hashlib.sha256(data).hexdigest().startswith("c8d80346a96c")
    assert len(data.decode("utf-8").splitlines()) == 472


def test_frontmatter_name_and_usage():
    text = CMD.read_text(encoding="utf-8")
    assert text.startswith("---\nname: spec-panel-diffgate\n")
    _, sec = _sections(text)
    usage = sec["## Usage"]
    assert "--diffgate-dir" in usage
    assert "--re-review" not in usage and "--baseline" not in usage


def test_review_loop_and_diffgate_bullets_are_pinned():
    assert bullet_problems(CMD.read_text(encoding="utf-8")) == []


def test_bullet_check_reports_a_changed_review_loop_bullet(tmp_path):
    text = CMD.read_text(encoding="utf-8")
    target = REVIEW_LOOP[2]
    copy = tmp_path / "spec-panel-diffgate.md"
    copy.write_text(
        text.replace(target, target.replace("PASS", "PASs", 1)), encoding="utf-8"
    )
    assert bullet_problems(copy.read_text(encoding="utf-8")) == [
        "## Review Loop bullet 3"
    ]


def test_bullet_check_reports_a_changed_diffgate_bullet(tmp_path):
    text = CMD.read_text(encoding="utf-8")
    target = DIFFGATE[0]
    assert "`check --dry-run` and" in target
    copy = tmp_path / "spec-panel-diffgate.md"
    copy.write_text(
        text.replace(target, target.replace("`check --dry-run` and ", "", 1)),
        encoding="utf-8",
    )
    assert bullet_problems(copy.read_text(encoding="utf-8")) == ["## Diffgate bullet 1"]


def test_canonical_cap_text_and_at_cap_clause_present():
    flat = " ".join(CMD.read_text(encoding="utf-8").split())
    assert CANONICAL_CAP_TEXT in flat
    assert AT_CAP_CLAUSES[1] in flat


def test_diffgate_section_placement_and_lookup_order():
    text = CMD.read_text(encoding="utf-8")
    heads = [x for x in text.split("\n") if x.startswith("## ")]
    i = heads.index("## Diffgate")
    assert heads[i - 1] == "## Review Loop" and heads[i + 1] == "## Output Formats"
    for bullet in (DIFFGATE[0], DIFFGATE[3]):
        assert bullet.index("~/.claude/skills/sc-diffgate") < bullet.index(
            "project `.claude/skills/sc-diffgate"
        )


def test_no_src_superclaude_beyond_the_base():
    assert CMD.read_text(encoding="utf-8").count("src/superclaude") <= BASE.read_text(
        encoding="utf-8"
    ).count("src/superclaude")
    for path in SKILL.rglob("*"):
        if path.is_file() and "__pycache__" not in path.parts:
            assert "src/superclaude" not in path.read_text(encoding="utf-8"), path


def test_drift_guard_against_the_base():
    var_pre, var = _sections(CMD.read_text(encoding="utf-8"))
    base_text = BASE.read_text(encoding="utf-8")
    base_pre, base = _sections(base_text)
    want_heads = []
    for h in base:
        want_heads.append(h)
        if h == "## Review Loop":
            want_heads.append("## Diffgate")
    assert list(var) == want_heads
    assert "## Unattended mode" not in var and "--unattended" not in CMD.read_text(
        encoding="utf-8"
    )
    expected_pre = (
        _swap(base_pre)
        .replace("\nname: spec-panel\n", "\nname: spec-panel-diffgate\n")
        .replace(
            'software engineering experts"',
            'software engineering experts with a computed re-review surface (diffgate variant)"',
        )
        .replace(
            "# /sc:spec-panel-diffgate - Expert Specification Review Panel\n",
            "# /sc:spec-panel-diffgate - Expert Specification Review Panel (diffgate variant)\n",
        )
    )
    assert var_pre == expected_pre
    for heading, body in base.items():
        if heading == "## Review Loop":
            continue
        want = _swap(body)
        if heading == "## Usage":
            want = want.replace(OLD_TOKEN, NEW_TOKEN)
        assert var[heading] == want, heading


def test_parent_command_keeps_its_427_flags():
    _, sec = _sections(PARENT.read_text(encoding="utf-8"))
    assert "--re-review" in sec["## Usage"] and "--baseline" in sec["## Usage"]


def test_isolated_install_runs_the_installed_script(tmp_path):
    home = tmp_path / "home"
    cmds = home / ".claude/commands/sc"
    cmds.mkdir(parents=True)
    sentinel = cmds / "spec-panel.md"
    sentinel.write_bytes(PARENT.read_bytes())
    before = sentinel.read_bytes()
    shutil.copy(CMD, cmds / "spec-panel-diffgate.md")
    dest = home / ".claude/skills/sc-diffgate"
    shutil.copytree(SKILL, dest, ignore=shutil.ignore_patterns("__pycache__"))
    work = tmp_path / "elsewhere"
    work.mkdir()
    proc = subprocess.run(
        [sys.executable, "-B", str(dest / "scripts/diffgate.py"), "--help"],
        cwd=work,
        capture_output=True,
        text=True,
        env={"HOME": str(home), "PATH": "/usr/bin:/bin"},
    )
    assert proc.returncode == 0, proc.stderr
    assert "fixcheck" in proc.stdout
    assert sentinel.read_bytes() == before

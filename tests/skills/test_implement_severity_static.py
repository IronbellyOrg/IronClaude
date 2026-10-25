"""Static pins for the P1 severity-model text of sc-implement-protocol.

Enforcement type: STATIC - assertions over protocol Markdown and the archive
helper source (SPEC AC-01..AC-04, AC-07, AC-10, AC-11; V1 F-05; V2 F-12).
"""

import importlib.util
import re
from pathlib import Path

_REPO = Path(__file__).resolve().parents[2]
_P = _REPO / "src/superclaude/skills/sc-implement-protocol"
_HELPER = _P / "scripts/archive_workspace.py"
_spec = importlib.util.spec_from_file_location("archive_workspace_sev", _HELPER)
aw = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(aw)

_PROTOCOL_FILES = (
    "SKILL.md",
    "refs/ledger.md",
    "refs/managed-workspace.md",
    "refs/qa.md",
    "refs/retry.md",
)


def _read(rel: str) -> str:
    return (_P / rel).read_text(encoding="utf-8")


def _flat(text: str) -> str:
    return " ".join(text.split())


QA = _read("refs/qa.md")
QA_FLAT = _flat(QA)


# --- SPEC AC-01 -------------------------------------------------------------


def test_ac01_checklist_readback_and_vocabulary_mapping():
    for name in (
        "ac-outcome-missing",
        "false-claim",
        "harmful-effect",
        "quoted-constraint-breach",
    ):
        assert f"| `{name}` |" in QA, name
    assert "**Four checklist answers; the blocking triggers.**" in QA
    assert "Reads each anchor back once" in QA
    assert "A finding whose only `yes` fails its Read-back is a note." in QA
    assert "**Derivation and vocabulary mapping.**" in QA
    assert (
        "high = any confirmed checklist `yes` = `blocking`; medium, IMPORTANT "
        "without a `yes`, low-medium, low and cosmetic = `minor` or `note`"
    ) in QA


# --- SPEC AC-02 (V2 F-03) ---------------------------------------------------

_FENCE = re.compile(r"^```[^\n]*\n(.*?)^```$", re.M | re.S)
_SLOTS = {
    "task_brief",
    "global_constraints",
    "diff",
    "start_sha",
    "prior_findings",
    "delta_diff",
    "recheck_list",
}


def _templates():
    return [b for b in _FENCE.findall(QA) if b.startswith("Review one task for spec")]


def test_ac02_one_closed_reviewer_template_with_seven_slots():
    blocks = _templates()
    assert len(blocks) == 1
    tpl = blocks[0]
    assert set(re.findall(r"\{([a-z_]+)\}", tpl)) == _SLOTS
    assert "Require citations:" in tpl
    assert "Do not read the retry folders" in tpl
    assert "A citation into either makes the verdict `cannot-verify`." in tpl


def test_ac02_no_finding_quota_phrase():
    assert not re.search(r"at least (N|\d+)", QA, re.I)


# --- SPEC AC-03 (V2 F-01, V1 F-04, V3 F-01, V3 F-03) ------------------------


def test_ac03_verdict_order_fed_by_blocking_findings_only():
    assert (
        'the parent runs the closed order of "## Verdict (exactly one)" over '
        "the parent-confirmed blocking findings only and records the result as "
        "the verdict, once; nobody rewrites a recorded verdict."
    ) in QA_FLAT
    assert "## Verdict owner (deliberate SPEC correction)" in QA
    assert (
        "`minor` and `note` findings never change the verdict. A review whose "
        "findings are all `minor` or `note` yields `compliant`"
    ) in QA_FLAT


def test_ac03_retired_spec_sentences_absent():
    for rel in _PROTOCOL_FILES:
        flat = _flat(_read(rel))
        assert (
            "The reviewer produces the verdict by running today's order" not in flat
        ), rel
        assert "The orchestrator never rewrites a verdict." not in flat, rel


def test_ac03_label_rules():
    assert "- An AC is unmet only when a B1 or B2 finding is attached to it." in QA
    assert '- `misunderstood` requires a B1 finding of the "contradicts" kind.' in QA
    assert "- `extra_scope` is non-empty only for B3 or B4 findings." in QA


def test_ac03_scope_attachment_and_non_blocking_unmet_rules():
    assert (
        "A confirmed B1 or B2 finding with `ac=scope` is attached to every AC "
        "whose cited text or file it touches, or to every AC of the task when it "
        "touches none"
    ) in QA_FLAT
    assert "never yields `compliant`" in QA_FLAT
    assert (
        "An `unmet` mark whose listed findings are all non-blocking after the "
        "Read-back and the inherited cap counts as met with its citation."
    ) in QA_FLAT


# --- V1 F-05 ----------------------------------------------------------------


def test_v1f05_reviewer_limits_and_parent_keys():
    assert "The reviewer may not widen the AC" in QA
    assert (
        "The parent writes `sev=`, `trigger=`, `first=` and `origin=`; the "
        "reviewer never writes these four keys."
    ) in QA
    assert "fix=local|nonlocal" not in QA
    assert "never invokes the `ponytail-review` plugin" in QA
    assert "never deletes or shrinks text an AC requires" in QA


# --- V2 F-12 ----------------------------------------------------------------


def test_v2f12_notes_append_on_failing_review_and_superseded_prefix():
    assert (
        "Every review that fails appends its `minor` and `note` findings to the "
        "notes file at once, tagged with its review id `r<k>-<j>`, before any "
        "later review can overwrite `review-<k>.md`."
    ) in QA_FLAT
    assert "prefixed `superseded `" in QA


# --- SPEC AC-04 (NFR-003): regex text equals base 77288289 ------------------

_BASE_LEDGER_VERDICT = (
    r"^T([0-9A-Za-z.-]+): (complete|blocked) verdict=(compliant|missing|extra|"
    r"misunderstood|cannot-verify) ac=([^ ]+) evidence=(.+) extras=lint:"
    r"(pass|fail|skip),typecheck:(pass|fail|skip),test:(pass|fail|skip|"
    r"unrelated-red) files=(.+)$"
)
_BASE_LEDGER_GRAMMAR_REGEXES = [
    r"^T([0-9A-Za-z.-]+): retry n=([345]) (?:step=open checkpoint=([0-9a-f]{40}) "
    r"tier=([A-Za-z0-9_]+)|step=revert brief=(\S+) supersedes=(T[0-9A-Za-z.-]+"
    r"_brief-[34]\.md|none)|step=review)$",
    r"^T([0-9A-Za-z.-]+): halt review=([2-5]) reason=([a-z][a-z-]*)$",
]
_BASE_ARCHIVE_REGEX_BLOCK = r"""ID_RE = re.compile(r"^TASK-WF-[a-z][A-Za-z0-9]{0,15}-\d{8}-\d{6}(?:-[2-9])?$")
TASK_ID = r"[0-9A-Za-z.-]+"
_HEADER = re.compile(
    r"^# implement ledger — source: .+ — created: \d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$"
)
_PLAN = re.compile(r"^PLAN: sha256=([0-9a-f]{64}) source_sha256=([0-9a-f]{64})$")
_START = re.compile(rf"^T({TASK_ID}): start sha=([0-9a-f]{{40}}|nogit)$")
_VERDICT = re.compile(
    rf"^T({TASK_ID}): (complete|blocked) verdict=(compliant|missing|extra|misunderstood|cannot-verify)"
    r" ac=([^ ]+) evidence=(.+) extras=lint:(?:pass|fail|skip),typecheck:(?:pass|fail|skip),"
    r"test:(?:pass|fail|skip|unrelated-red) files=(.+)$"
)
_RULING = re.compile(rf"^T({TASK_ID}): Ruling: .+ — .+ — .+$")
_RETRY = re.compile(
    rf"^T({TASK_ID}): retry n=([345]) "
    r"(?:step=open checkpoint=([0-9a-f]{40}) tier=([A-Za-z0-9_]+)"
    r"|step=revert brief=(\S+) supersedes=(T[0-9A-Za-z.-]+_brief-[34]\.md|none)"
    r"|step=review)$"
)
_HALT = re.compile(rf"^T({TASK_ID}): halt review=([2-5]) reason=([a-z][a-z-]*)$")
_LEGACY_BRIEF = re.compile(
    r"^\.dev/implement/([^/]+)/retries/(T[^/]+_brief-[345]\.md)$"
)
_FINAL = re.compile(r"^FINAL: (\S+)(?: .*)?$")
_FINAL_OK = re.compile(r"^FINAL: pass evidence=(.+) state=([0-9a-f]{64})$")
_ARCH = re.compile(r"^ARCHIVE: (start|failed|Ruling:) .+$")
"""


def test_ac04_ledger_regexes_unchanged():
    lines = _read("refs/ledger.md").splitlines()
    assert lines.count(_BASE_LEDGER_VERDICT) == 1
    i = lines.index("<!-- ledger-grammar-block: regexes -->")
    assert lines[i + 1] == "```"
    assert lines[i + 2 : i + 4] == _BASE_LEDGER_GRAMMAR_REGEXES
    assert lines[i + 4] == "```"


def test_ac04_archive_helper_regexes_unchanged():
    src = _HELPER.read_text(encoding="utf-8")
    m = re.search(r"^ID_RE = .*?^_ARCH = [^\n]*\n", src, re.M | re.S)
    assert m and m.group(0) == _BASE_ARCHIVE_REGEX_BLOCK


# --- SPEC AC-07: fixture ledgers still parse with the unchanged helper -------

_LEDGER_LINE = re.compile(r"^(# implement ledger|T[0-9]|PLAN: |FINAL: |ARCHIVE: )")


def _fixture_ledger_lines():
    """Concrete ledger lines in the fenced examples of ledger.md and retry.md."""
    out = []
    for rel in ("refs/ledger.md", "refs/retry.md"):
        for block in _FENCE.findall(_read(rel)):
            for line in block.splitlines():
                if (
                    _LEDGER_LINE.match(line)
                    and "<" not in line
                    and not line.startswith("#")
                ):
                    out.append(line)
    return out


def test_ac07_fixture_ledgers_parse(tmp_path):
    lines = _fixture_ledger_lines()
    assert len(lines) >= 25
    header = "# implement ledger — source: ./x.md — created: 2026-10-01T06:30:00Z"
    ledger = tmp_path / "progress.md"
    ledger.write_text("\n".join([header, *lines]) + "\n", encoding="utf-8")
    recs = aw._parse_ledger(ledger)
    assert len(recs) == len(lines) + 1


def test_ac07_archive_suite_fixture_ledger_parses_and_archives(tmp_path):
    spec = importlib.util.spec_from_file_location(
        "wf_archive_fixture", Path(__file__).with_name("test_workflow_archive.py")
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    pkg = mod.Pkg(tmp_path)
    assert [k for k, _, _ in aw._parse_ledger(pkg.pkg / "progress.md")] == [
        "header",
        "plan",
        "start",
        "verdict",
        "start",
        "verdict",
    ]
    pkg.final()
    pkg.run()
    assert (pkg.done / "progress.md").is_file()


# --- SPEC AC-10: per-attempt table ------------------------------------------


def test_ac10_per_attempt_table_rows():
    for row in (
        "| Attempt | May fail the attempt | May halt | May prompt the user | Minors may be edited |",
        "| A1 | `blocking` only | `blocking` only (in practice never: an A1 failure goes to the A2 fix pass) | `blocking` only (in practice never) | only inside lines already changed for a blocker |",
        "| A2 with repairs 1 and 2 | `blocking` only | `blocking` only | `blocking` only | only inside lines already changed for a blocker |",
        "| A3 | `blocking` only | `blocking` only | `blocking` only | no, recorded only |",
        "| A4 | `blocking` only | `blocking` only | `blocking` only | no, recorded only |",
        "| A5 | `blocking` only | `blocking` only (`ladder-end`) | `blocking` only | no, recorded only |",
        "| legacy FINAL | `blocking` only, advisory (never reopens a task) | never | never (summary only) | no |",
        "| managed FINAL | `blocking` only (`issues`) | `blocking` only (`E-ARCHIVE-BLOCKED`) | `blocking` only | no |",
    ):
        assert row in QA.splitlines(), row


# --- SPEC AC-11 (V1 F-11, V2 F-15): every halt/STOP/Ruling site classified ---
#
# blocking   reachable only while a blocking finding with a confirmed anchor is open
# stop-row   non-finding STOP row of the SKILL.md STOP table, or FR-019 items 5 and 6
# definition grammar, examples, the reason table, or a rule that writes nothing

_SITE = re.compile(r"\bhalt(s|ed|ing)?\b|E-HALT-QA|E-ARCHIVE-BLOCKED|\bRuling\b")

_ALLOW = [
    ("SKILL.md", "Load `refs/qa.md` fo", "definition"),
    ("SKILL.md", "| `E-HALT-QA` | A te", "stop-row"),
    ("SKILL.md", "| `E-ARCHIVE-BLOCKED", "stop-row"),
    ("SKILL.md", "Default sequential i", "blocking"),
    ("SKILL.md", "Q7 GATE    Apply the", "blocking"),
    ("SKILL.md", "Q8 NEXT    Only if c", "definition"),
    ("SKILL.md", "Every enumerable tas", "definition"),
    ("refs/ledger.md", "`complete` on the ve", "definition"),
    ("refs/ledger.md", "## Ruling line (user", "definition"),
    ("refs/ledger.md", "T<id>: Ruling: <what", "definition"),
    ("refs/ledger.md", "^T([0-9A-Za-z.-]+): Rulin", "definition"),
    ("refs/ledger.md", "After a valid operat", "definition"),
    ("refs/ledger.md", "Legal **only** when ", "definition"),
    ("refs/ledger.md", "## Retry and halt re", "definition"),
    ("refs/ledger.md", "Two kinds for the es", "definition"),
    ("refs/ledger.md", "T<id>: halt review=<", "definition"),
    ("refs/ledger.md", "^T([0-9A-Za-z.-]+): halt ", "definition"),
    ("refs/ledger.md", "Placement rules: `st", "definition"),
    ("refs/ledger.md", "Halt reason: open cl", "definition"),
    ("refs/ledger.md", "if last line does no", "definition"),
    ("refs/ledger.md", "Definitions, over th", "definition"),
    ("refs/ledger.md", "| R | An eligible Ru", "definition"),
    ("refs/ledger.md", "| P | Latest verdict", "blocking"),
    ("refs/ledger.md", "| H | A `halt` recor", "blocking"),
    ("refs/ledger.md", "| X | Last record is", "blocking"),
    ("refs/ledger.md", "| B | Last record is", "blocking"),
    ("refs/ledger.md", "Executor-recorded Ru", "definition"),
    ("refs/ledger.md", "T2: Ruling: accept T", "definition"),
    ("refs/ledger.md", "The earlier operator", "definition"),
    ("refs/ledger.md", "T1: halt review=2 re", "definition"),
    ("refs/ledger.md", "^ARCHIVE: (start|fai", "definition"),
    ("refs/ledger.md", "- Legacy `ARCHIVE: R", "definition"),
    ("refs/managed-workspace.md", "2. `--skip-final-rev", "stop-row"),
    ("refs/managed-workspace.md", "3. State: `uv run --", "stop-row"),
    ("refs/managed-workspace.md", "6. `pass` → run the ", "blocking"),
    ("refs/managed-workspace.md", "Do not ask the user ", "definition"),
    ("refs/managed-workspace.md", "| real direct packag", "definition"),
    ("refs/qa.md", "**Precedence over th", "definition"),
    ("refs/qa.md", "| | Accepted-minor |", "definition"),
    ("refs/qa.md", "| Ledger | `complian", "definition"),
    ("refs/qa.md", "| Writes a `Ruling:`", "definition"),
    ("refs/qa.md", "The Ruling path is u", "definition"),
    ("refs/qa.md", "- A batch task whose", "blocking"),
    ("refs/qa.md", "| a terminal `halt` ", "blocking"),
    ("refs/qa.md", "| clear user confirm", "blocking"),
    ("refs/qa.md", "| `E-RESUME-NEEDED` ", "stop-row"),
    ("refs/qa.md", "A Ruling counts only", "blocking"),
    ("refs/qa.md", "The executor MUST au", "blocking"),
    ("refs/qa.md", "T<id>: Ruling: <what", "definition"),
    ("refs/qa.md", "| Attempt | May fail", "definition"),
    ("refs/qa.md", "| managed FINAL | `b", "blocking"),
    ("refs/qa.md", "Mapping: high = any ", "definition"),
    ("refs/qa.md", "1. `E-HALT-QA` after", "blocking"),
    ("refs/qa.md", "2. `dispute` halt: o", "blocking"),
    ("refs/qa.md", "4. `operator-review`", "blocking"),
    ("refs/qa.md", "7. `E-ARCHIVE-BLOCKE", "blocking"),
    ("refs/qa.md", "No other path may st", "definition"),
    ("refs/retry.md", "Loaded when A2 (the ", "definition"),
    ("refs/retry.md", "| A5 fails | `blocke", "blocking"),
    ("refs/retry.md", "- Files written for ", "definition"),
    ("refs/retry.md", "The k rule: k = the ", "definition"),
    ("refs/retry.md", "If a check fails whe", "blocking"),
    ("refs/retry.md", "Procedure step 0 (Q6", "blocking"),
    ("refs/retry.md", "Per-run cap: when A2", "blocking"),
    ("refs/retry.md", "Then append the exis", "blocking"),
    ("refs/retry.md", "- No answer passes: ", "blocking"),
    ("refs/retry.md", "5. **Procedure step ", "blocking"),
    ("refs/retry.md", "Every halt in proced", "blocking"),
    ("refs/retry.md", "- The runner-up is t", "blocking"),
    ("refs/retry.md", "- The parent checks ", "blocking"),
    ("refs/retry.md", "- If A5 fails, proce", "blocking"),
    ("refs/retry.md", "1. **Entry.** The Re", "blocking"),
    ("refs/retry.md", "11. **Convergence.**", "definition"),
    ("refs/retry.md", "Each review may also", "definition"),
    ("refs/retry.md", "1. Bind, then guard.", "blocking"),
    ("refs/retry.md", "Move-back on a resum", "blocking"),
    ("refs/retry.md", "Finished reverts and collisions: (a", "blocking"),
    ("refs/retry.md", "`no-evidence` is a t", "blocking"),
    ("refs/retry.md", "**The revert block.*", "definition"),
    ("refs/retry.md", "last=$(grep -v '^$' ", "definition"),
    ("refs/retry.md", "**Terminal halt.** E", "blocking"),
    ("refs/retry.md", "Reason-to-`review=` ", "definition"),
    ("refs/retry.md", "| `operator-review` ", "definition"),
    ("refs/retry.md", "```halt-examples", "definition"),
    ("refs/retry.md", "T1: halt review=5 reason=ladde", "definition"),
    ("refs/retry.md", "T1: halt review=2 reason=no-sn", "definition"),
    ("refs/retry.md", "T1: halt review=3 reason=no-sn", "definition"),
    ("refs/retry.md", "T1: halt review=4 reason=no-sn", "definition"),
    ("refs/retry.md", "T1: halt review=2 reason=batch", "definition"),
    ("refs/retry.md", "T1: halt review=2 reason=head-", "definition"),
    ("refs/retry.md", "T1: halt review=3 reason=head-", "definition"),
    ("refs/retry.md", "T1: halt review=4 reason=head-", "definition"),
    ("refs/retry.md", "T1: halt review=2 reason=budge", "definition"),
    ("refs/retry.md", "T1: halt review=2 reason=advic", "definition"),
    ("refs/retry.md", "T1: halt review=3 reason=advic", "definition"),
    ("refs/retry.md", "T1: halt review=2 reason=dispu", "definition"),
    ("refs/retry.md", "T1: halt review=3 reason=dispu", "definition"),
    ("refs/retry.md", "T1: halt review=4 reason=no-ru", "definition"),
    ("refs/retry.md", "T1: halt review=4 reason=brief", "definition"),
    ("refs/retry.md", "T1: halt review=2 reason=no-ev", "definition"),
    ("refs/retry.md", "T1: halt review=3 reason=no-ev", "definition"),
    ("refs/retry.md", "T1: halt review=4 reason=no-ev", "definition"),
    ("refs/retry.md", "T1: halt review=2 reason=opera", "definition"),
    ("refs/retry.md", "T1: halt review=3 reason=opera", "definition"),
    ("refs/retry.md", "T1: halt review=4 reason=opera", "definition"),
    ("refs/retry.md", "T1: halt review=5 reason=opera", "definition"),
    ("refs/retry.md", "Everywhere else in t", "definition"),
    ("refs/retry.md", "Any `halt` after the", "definition"),
    ("refs/retry.md", "The halt message pri", "blocking"),
    ("refs/retry.md", "Every ladder halt is", "blocking"),
    ("refs/retry.md", "**Transient stops.**", "stop-row"),
    ("refs/retry.md", "**Ruling eligibility", "definition"),
    ("refs/retry.md", "A Ruling written aft", "definition"),
]


def test_ac11_allow_list_classes_are_closed():
    assert {c for _, _, c in _ALLOW} <= {"blocking", "stop-row", "definition"}
    assert len({(f, s) for f, s, _ in _ALLOW}) == len(_ALLOW)


def test_ac11_every_halt_stop_ruling_site_is_classified():
    hits = {i: 0 for i in range(len(_ALLOW))}
    unlisted = []
    for rel in _PROTOCOL_FILES:
        for n, line in enumerate(_read(rel).splitlines(), 1):
            if not _SITE.search(line):
                continue
            ids = [i for i, (f, s, _) in enumerate(_ALLOW) if f == rel and s in line]
            if len(ids) != 1:
                unlisted.append(f"{rel}:{n} matches {len(ids)} entries: {line[:80]}")
            for i in ids:
                hits[i] += 1
    stale = [_ALLOW[i] for i, c in hits.items() if c != 1]
    assert not unlisted, unlisted
    assert not stale, stale


def test_ac11_minors_only_replay_writes_no_halt_and_no_ruling():
    assert "| Writes a `Ruling:` line | Never | Always |" in QA
    assert "no halt, no Ruling, no user prompt, at every row" in QA_FLAT
    assert "A minors-only replay writes no `halt` and no `Ruling:` line." in QA


# --- Family probe (SPEC FR-026; V1 F-16, V2 F-10, F-11, F-26) ---


def test_family_probe_section_in_qa():
    assert "\n## Family probe\n" in QA
    assert "probe-<k>-<j>.md" in QA
    for opt in ("`-n`", "`-E`", "`-F`", "`-i`", "`-w`", "`-e <pattern>`", "`--`"):
        assert opt in QA_FLAT, opt
    assert "`git grep -O` / `--open-files-in-pager`" in QA_FLAT
    assert "`git grep --textconv`" in QA_FLAT
    assert "`rg` is refused entirely" in QA_FLAT
    assert "including on resume" in QA_FLAT


def test_skill_q5_names_family_probe():
    q5 = [ln for ln in _read("SKILL.md").splitlines() if ln.startswith("Q5 FIX")]
    assert len(q5) == 1 and "Family probe" in q5[0] and "refs/retry.md" in q5[0]


# --- Repair round (SPEC FR-024; V2 F-02, F-05, F-25) ---


def test_retry_repair_round_rules():
    r = _read("refs/retry.md")
    assert "\n### Repair round\n" in r
    assert "deliberate SPEC correction of FR-024 and FR-026" in r
    assert (
        "is probe-pending" in r
        and "only then does it apply the locality predicate" in r
    )
    assert "a batch task never gets a repair" in r
    assert "A batch A2 with only minors still completes" in r
    assert (
        "line 2 is `reviewed=none ref=none` and the last line is `applied tree=none`"
        in r
    )
    assert "no ref is pinned" in r

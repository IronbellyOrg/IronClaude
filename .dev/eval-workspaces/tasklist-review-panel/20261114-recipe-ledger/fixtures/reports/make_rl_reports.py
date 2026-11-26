"""F-REPORT-RL (TESTING section 2): reviewer final messages built by code from fixtures/plans/p_basic.md.

Every quote is cut out of the plan (or of fixtures/plans/source.md) by a regular expression, so it is exact and a
change of the plan that breaks a quote makes `cut` raise instead of leaving a stale quote. All text is invented.

    build(name) -> SimpleNamespace(name, report, lens, assigned, transcript, via_reask)
        report      the final message (str)
        lens        the recipe ids of the reviewer: EMBER_LENS or LUNA_LENS
        assigned    the row ids the row check accepts for that lens (`rl.lens.assigned_ids`)
        transcript  the events of a matching run (fixtures/transcripts/make_transcripts.py) or None
        via_reask   True when the report stands for a re-asked message (its rows are never promoted)
    build_all() -> {name: case}; write_all(folder) writes <name>.md (and <name>.transcript.json when present).
    plan_text(), source_text() give the candidate and the source the quotes were cut from; Q holds the quotes.

`anchor_250` and `claim_301` are the copied report files next to this one.
"""

import json
import re
from pathlib import Path
from types import SimpleNamespace

from fixtures.transcripts import make_transcripts as tr
from rl import lens

HERE = Path(__file__).resolve().parent
PLANS = HERE.parent / "plans"
EMBER_LENS = ["C4", "C5", "C6", "C8"]
LUNA_LENS = ["C1", "C2", "C3"]
CB3 = "An implementer who follows the stated text as written builds"


def plan_text():
    return (PLANS / "p_basic.md").read_text(encoding="utf-8")


def source_text():
    return (PLANS / "source.md").read_text(encoding="utf-8")


def cut(pattern, text):
    m = re.search(pattern, text)
    if not m:
        raise ValueError(f"fixture quote not found in its text: {pattern}")
    return m.group(0)


_P, _S = plan_text(), source_text()
Q = {
    "grep": cut(r"`grep -c 'retention-window' docs/guide\.md` prints at least 1", _P),
    "heading": cut(r'add the heading "Retention window" to it', _P),
    "count": cut(r"update the count from 3 report formats to 4 report formats", _P),
    "remain": cut(
        r"No remaining `3 report formats` text exists in `docs/guide\.md`\.", _P
    ),
    "legal": cut(
        r"The purge step keys on `legal_hold` and leaves such reports in place\.", _P
    ),
    "skips": cut(r"it skips any report whose hold flag is set", _P),
    "ndjson": cut(
        r'`render\(rows, fmt="ndjson"\)` returns one JSON object per row, one object per line\.',
        _P,
    ),
    # two plan lines: the quote keeps the line break and the indent, as a model copies it
    "wrap": cut(
        r"is the only document that changes\.\n  - The exporter package has no network access\.",
        _P,
    ),
    "short": cut(r"report\.py", _P),  # 9 characters: below the anchor minimum of 12
    "source_legal": cut(
        r"The purge step must skip a report whose `legal_hold` flag is set\.", _S
    ),
}
NOT_IN_PLAN = (
    "The retention job deletes expired reports every night at three in the morning."
)
PROBLEM = "The pattern has a hyphen and lower case but the ordered heading has a space and a capital, so grep -c prints 0."
CLAIM_CB3 = f"{CB3} a guide with no Retention window heading, and that is wrong because grep -c prints 0."


def row(item, verdict="OK", qp="", qo="", problem="", ran="read the task text"):
    return json.dumps(
        {
            "item": item,
            "verdict": verdict,
            "quote_plan": qp,
            "quote_other": qo,
            "problem": problem,
            "ran": ran,
        },
        ensure_ascii=False,
    )


def problem_row(item="C4.1", qp=None, qo=None, problem=PROBLEM, verdict="PROBLEM"):
    return row(
        item,
        verdict,
        Q["grep"] if qp is None else qp,
        Q["heading"] if qo is None else qo,
        problem,
        "printf into grep -c: 0",
    )


def finding(
    fid="F1",
    anchor=None,
    claim="The criterion cannot pass.",
    probe=None,
    blocking=False,
    severity="MAJOR",
):
    obj = {
        "id": fid,
        "severity": severity,
        "blocking": blocking,
        "category": "unpassable-check",
        "anchor": Q["ndjson"] if anchor is None else anchor,
        "refs": [],
        "claim": claim,
    }
    if probe:
        obj["probe"] = probe
    return json.dumps(obj, ensure_ascii=False)


def fence(info, lines, closed=True):
    return "\n".join([f"```{info}", *lines, *(["```"] if closed else [])])


def ledger_part(rows, closed=True):
    return "## Ledger\n\n" + fence("ledger-v1", rows, closed)


def findings_part(lines, closed=True):
    return "## Findings block\n\n" + fence("findings-v1", lines, closed)


def message(
    *parts,
    prose="review: 1 of 3\n\nTwo recipe rows were run on the plan.",
    tail="verdict: FAIL",
):
    return "\n\n".join([prose, *parts, tail]) + "\n"


def standard(rows, findings=(), **kw):
    return message(ledger_part(rows), findings_part(list(findings)), **kw)


def _ember_rows():
    return [
        problem_row("C4.1"),
        row("C4.2", ran="literal pattern matches the ordered text"),
        row("C5.1", ran="grep -c of the old count: 1"),
        row("C6.1", ran="compared both scopes"),
        row("C8.1", ran="git grep of edited paths over tests and docs: 0 hits"),
    ]


def _none_found(classes):
    return [
        row(f"{c}.1", ran=f"NONE FOUND: searched the plan for {c} shapes")
        for c in classes
    ]


def _rows_for(classes, k):
    return [row(f"{c}.{i}") for c in classes for i in range(1, k + 1)]


def _good_ember():
    return standard(
        _ember_rows(),
        [
            finding(
                anchor=Q["grep"],
                probe="C4.1",
                claim="The criterion's pattern cannot match the ordered heading.",
            )
        ],
    )


def _good_luna1():
    rows = [
        row("C1.1", ran="compared the two scopes"),
        problem_row(
            "C2.1",
            Q["legal"],
            Q["source_legal"],
            "The plan keys on legal_hold but the source says the purge must skip the held report.",
        ),
        row("C3.1", ran="searched for a value read and never written"),
    ]
    return standard(rows, [finding(anchor=Q["legal"], probe="C2.1")])


def _broken_ledger(rows, closed=True):
    return message(ledger_part(rows, closed), findings_part([finding()]))


def _over_budget_lens():
    rows = [row(f"{c}.{i}") for c in ("C4", "C5", "C6") for i in range(1, 5)]
    return standard(rows + [row("C8.1"), row("C8.2"), problem_row("C8.3")])


def _linked(row_line, finding_line):
    return standard([row_line], [finding_line])


_UNRELATED = finding("F1", Q["ndjson"], "The format name is not defined in the source.")
SUPPORTED = problem_row("C4.1")  # exact plan quote and a different exact plan quote


def _dup_row():
    return standard(
        [problem_row("C4.1"), row("C4.1", ran="a second line for the same row")], []
    )


# name -> (message builder, lens classes, transcript name or None, via_reask)
_SPEC = {
    "good_ember": (_good_ember, EMBER_LENS, "search_done", False),
    "good_luna1": (_good_luna1, LUNA_LENS, "luna_array_results", False),
    "none_found": (
        lambda: standard(_none_found(EMBER_LENS)),
        EMBER_LENS,
        "none_found_with_search",
        False,
    ),
    "none_found_with_rows": (
        lambda: standard(
            [_none_found(["C4"])[0], row("C4.2"), *_none_found(["C5", "C6", "C8"])]
        ),
        EMBER_LENS,
        "none_found_without_search",
        False,
    ),
    # a heading and the words of the opener in prose, no block: a grep for the opener text would pass this report
    "ledger_missing": (
        lambda: message(
            "## Ledger\n\nMy ledger-v1 block with the ```ledger-v1 opener is in an earlier message.",
            findings_part([finding()]),
        ),
        EMBER_LENS,
        None,
        False,
    ),
    "ledger_after_findings": (
        lambda: message(findings_part([finding()]), ledger_part(_ember_rows())),
        EMBER_LENS,
        None,
        False,
    ),
    "ledger_twice": (
        lambda: message(
            ledger_part([problem_row("C4.1")]),
            fence("ledger-v1", [row("C5.1")]),
            findings_part([finding()]),
        ),
        EMBER_LENS,
        None,
        False,
    ),
    "ledger_unclosed": (
        lambda: _broken_ledger([problem_row("C4.1")], closed=False),
        EMBER_LENS,
        None,
        False,
    ),
    "findings_unclosed": (
        lambda: message(
            ledger_part(_ember_rows()),
            findings_part([finding()], closed=False),
            tail="",
        ),
        EMBER_LENS,
        None,
        False,
    ),
    "findings_twice": (
        lambda: message(
            ledger_part(_ember_rows()),
            findings_part([finding()]),
            fence("findings-v1", [finding("F2")]),
        ),
        EMBER_LENS,
        None,
        False,
    ),
    "heading_between": (
        lambda: message(
            ledger_part(_ember_rows()),
            "## Notes\n\nOne more remark.",
            findings_part([finding()]),
        ),
        EMBER_LENS,
        None,
        False,
    ),
    "bad_json_line": (
        lambda: standard(
            [problem_row("C4.1"), row("C4.2")[:-1], row("C5.1")],
            [finding(probe="C4.1")],
        ),
        EMBER_LENS,
        None,
        False,
    ),
    "verdict_lowercase": (
        lambda: standard(
            [problem_row("C4.1", verdict="problem"), row("C4.2", verdict=" Ok ")]
        ),
        EMBER_LENS,
        None,
        False,
    ),
    "unknown_class": (
        lambda: standard([row("C4.1"), problem_row("C1.1")]),
        EMBER_LENS,
        None,
        False,
    ),
    "over_budget_recipe": (
        lambda: standard(
            [row("C4.1"), row("C4.2"), row("C4.3"), row("C4.4"), problem_row("C4.5")]
        ),
        EMBER_LENS,
        None,
        False,
    ),
    "over_budget_lens": (_over_budget_lens, EMBER_LENS, None, False),
    "recipe_missing": (
        lambda: standard([row("C4.1"), row("C5.1"), row("C6.1")]),
        EMBER_LENS,
        None,
        False,
    ),
    "dup_row": (_dup_row, EMBER_LENS, None, False),
    "quote_plan_not_in_candidate": (
        lambda: standard([problem_row("C4.1", NOT_IN_PLAN, Q["heading"])]),
        EMBER_LENS,
        None,
        False,
    ),
    "quote_wraps_line": (
        lambda: standard([problem_row("C4.1", Q["wrap"], Q["heading"])]),
        EMBER_LENS,
        None,
        False,
    ),
    "quote_other_in_source": (
        lambda: standard([problem_row("C4.1", Q["legal"], Q["source_legal"])]),
        EMBER_LENS,
        None,
        False,
    ),
    "quote_other_in_candidate": (
        lambda: standard([problem_row("C4.1")]),
        EMBER_LENS,
        None,
        False,
    ),
    "quote_other_in_transcript": (
        lambda: standard([problem_row("C4.1", Q["legal"], tr.SEARCH_HIT)]),
        EMBER_LENS,
        "search_done",
        False,
    ),
    "quote_other_only_in_assistant_text": (
        lambda: standard([problem_row("C4.1", Q["legal"], tr.ASSISTANT_ONLY)]),
        EMBER_LENS,
        "assistant_text_only",
        False,
    ),
    "problem_no_finding": (
        lambda: standard([problem_row("C4.1")], [_UNRELATED]),
        EMBER_LENS,
        None,
        False,
    ),
    "finding_linked_by_probe": (
        lambda: _linked(
            problem_row("C4.1"), finding("F1", Q["ndjson"], CLAIM_CB3, "C4.1", True)
        ),
        EMBER_LENS,
        None,
        False,
    ),
    "finding_linked_by_quote": (
        lambda: _linked(
            problem_row("C4.1"),
            finding(
                "F1",
                f"Acceptance criteria: {Q['grep']} in the guide",
                CLAIM_CB3,
                None,
                True,
            ),
        ),
        EMBER_LENS,
        None,
        False,
    ),
    "ok_but_finding": (
        lambda: _linked(
            row("C4.1", ran="pattern matches"),
            finding("F1", Q["ndjson"], "The criterion cannot pass.", "C4.1"),
        ),
        EMBER_LENS,
        None,
        False,
    ),
    "unsure_with_blocking": (
        lambda: _linked(
            problem_row("C4.1", verdict="UNSURE"),
            finding("F1", Q["ndjson"], CLAIM_CB3, "C4.1", True),
        ),
        EMBER_LENS,
        None,
        False,
    ),
    "blocking_no_cb3": (
        lambda: _linked(
            problem_row("C4.1"),
            finding("F1", Q["ndjson"], "The criterion cannot pass.", "C4.1", True),
        ),
        EMBER_LENS,
        None,
        False,
    ),
    "blocking_with_cb3": (
        lambda: _linked(
            problem_row("C4.1"), finding("F1", Q["ndjson"], CLAIM_CB3, "C4.1", True)
        ),
        EMBER_LENS,
        None,
        False,
    ),
    # an item of 17 characters gives the promoted id "P" + item, 18 characters, over the limit of 16
    "promote_long_id": (
        lambda: standard([problem_row("C4.12345678901234")]),
        EMBER_LENS,
        None,
        False,
    ),
    "promote_short_anchor": (
        lambda: standard([problem_row("C4.1", Q["short"], Q["heading"])]),
        EMBER_LENS,
        None,
        False,
    ),
    # the id the promotion would take, PC4.1, is already used by a finding of the block
    "promote_dup_id": (
        lambda: standard(
            [problem_row("C4.1")],
            [finding("PC4.1", Q["ndjson"], "The format name is not defined.")],
        ),
        EMBER_LENS,
        None,
        False,
    ),
    "via_reask": (
        lambda: standard([problem_row("C4.1"), row("C5.1"), row("C6.1"), row("C8.1")]),
        EMBER_LENS,
        None,
        True,
    ),
}
COPIED = ("anchor_250", "claim_301")
CASES = tuple(_SPEC) + COPIED


def build(name):
    if name in COPIED:
        report, classes, transcript, via = (
            (HERE / f"{name}.md").read_text(encoding="utf-8"),
            EMBER_LENS,
            None,
            False,
        )
    else:
        make, classes, tname, via = _SPEC[name]
        report = make()
        transcript = None if tname is None else tr.build(tname, report)
    return SimpleNamespace(
        name=name,
        report=report,
        lens=classes,
        assigned=lens.assigned_ids(classes),
        transcript=transcript,
        via_reask=via,
    )


def build_all():
    return {n: build(n) for n in CASES}


def write_all(folder):
    folder = Path(folder)
    folder.mkdir(parents=True, exist_ok=True)
    for n, c in build_all().items():
        (folder / f"{n}.md").write_text(c.report, encoding="utf-8")
        if c.transcript is not None:
            (folder / f"{n}.transcript.json").write_text(
                json.dumps(c.transcript), encoding="utf-8"
            )
    return folder

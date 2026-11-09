6bbe5caacc9ce8f5f7234c0c2198992bfef41098
family check-rederivation
form: a script-written ledger record (mark, uncovered, audit, grade, form, final) can be edited between script calls and check does not notice
command: grep -n -e 'def cmd_check' -e 'of_kind(records, "uncovered")' -e 'of_kind(records, "audit")' -e '"k": "uncovered"' -e '"k": "audit"' -e 'def append_records' -- src/superclaude/skills/sc-spec-panel-stoprule-protocol/scripts/stoprule.py
before:
188:def append_records(report_path, records):
602:        out.append({"k": "uncovered", "hunk": h["new"]})
914:        for a in of_kind(records, "audit")
942:        a for a in of_kind(records, "audit") if "hunk" in a and a.get("real") is True
1107:                "k": "audit",
1161:    uncovered = of_kind(records, "uncovered")
1503:    for u in of_kind(records, "uncovered"):
1578:def cmd_check(args):
1676:    for u in of_kind(records, "uncovered"):
coupled sites: append_records (every script write), cmd_finalize (direct insert), cmd_check, mark quote_lines read without --spec
after:
188:def append_records(report_path, records):
615:        out.append({"k": "uncovered", "hunk": h["new"]})
927:        for a in of_kind(records, "audit")
955:        a for a in of_kind(records, "audit") if "hunk" in a and a.get("real") is True
1120:                "k": "audit",
1174:    uncovered = of_kind(records, "uncovered")
1516:    for u in of_kind(records, "uncovered"):
1596:def cmd_check(args):
1670:    if want != [u.get("hunk") for u in of_kind(records, "uncovered")]:
1692:                "k": "audit",
1699:    if expect_audit != [dump(a) for a in of_kind(records, "audit")]:
1736:    for u in of_kind(records, "uncovered"):

0047c2b27973251d0eb09a98eae2c34de5c7b671
## family missing-transition-test
defect form: a source.md section 2 transition-table row with no test of its own
command: grep -n -e E-NOT-CHANGED -e reopened -e "E-ANCHOR" tests/skills/test_review_ledger_script.py
before:
216:    assert code == 2 and out["error"] == "E-ANCHOR"
231:    assert code == 2 and out["error"] == "E-ANCHOR-AMBIGUOUS"
782:    assert code == 2 and out["error"] == "E-ANCHOR"
922:            "E-NOT-CHANGED",
937:            "E-ANCHOR",
1150:    assert by_id(lp.state())["R1"]["status"] == "reopened"
coupled sites: source.md:34 (verify new row anchors), :36 (unmappable anchor), :37 (fixed to reopened via open), :39 (untouched verified)
after:
216:    assert code == 2 and out["error"] == "E-ANCHOR"
231:    assert code == 2 and out["error"] == "E-ANCHOR-AMBIGUOUS"
782:    assert code == 2 and out["error"] == "E-ANCHOR"
922:            "E-NOT-CHANGED",
937:            "E-ANCHOR",
1150:    assert by_id(lp.state())["R1"]["status"] == "reopened"
1227:def test_untouched_verified_row_cannot_be_reopened(tmp_path, result):
1239:    assert code == 2 and out["error"] == "E-NOT-CHANGED"
1242:def test_open_on_a_once_verified_fixed_row_gives_reopened(tmp_path):
1252:    assert by_id(lp.state())["R1"]["status"] == "reopened"
1277:    assert code == 2 and out["error"] == "E-ANCHOR"
1284:        ("This sentence is not in the snapshot.", "E-ANCHOR"),
1285:        ("The cache is refreshed every hour.", "E-ANCHOR-AMBIGUOUS"),

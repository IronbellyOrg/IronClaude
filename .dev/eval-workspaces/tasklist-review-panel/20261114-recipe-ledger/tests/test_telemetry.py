"""scaffold/telemetry.py (Tier B, built locally): the class, probe and src keys and the per-class table (MR 3.0.6)."""

from scaffold import telemetry

F = {"id": "F1", "severity": "MAJOR", "blocking": True}


def test_class_of_takes_the_recipe_prefix():
    assert telemetry.class_of("C4.1") == "C4"
    assert telemetry.class_of("C12.30") == "C12"
    assert all(
        telemetry.class_of(x) is None for x in ("C4", "C4x", "4.1", "S3", "", None)
    )


def test_tag_sets_only_the_given_keys_and_copies():
    assert telemetry.tag(F) == F
    t = telemetry.tag(F, class_="C4", probe="C4.1")
    assert (
        t == dict(F, **{"class": "C4", "probe": "C4.1"})
        and "src" not in t
        and "class" not in F
    )
    assert telemetry.tag(F, src="ledger")["src"] == "ledger"
    assert set(telemetry.KEYS) == {"class", "probe", "src"}


def test_per_class_table_counts_found_wrong_blockers_and_time():
    findings = [
        telemetry.tag(F, class_="C4"),
        telemetry.tag(dict(F, id="F2"), class_="C4"),
        telemetry.tag(dict(F, id="F3", blocking=False), class_="C4"),
        dict(F, id="F4"),
    ]
    table = telemetry.per_class_table(
        findings, wrong={"F1", "F3", "F4"}, seconds={"C4": 12.5}
    )
    assert table == {
        "C4": {
            "found": 3,
            "wrong_blockers": 1,
            "seconds": 12.5,
        },  # F3 is wrong but not blocking
        "none": {"found": 1, "wrong_blockers": 1, "seconds": 0},
    }
    assert telemetry.per_class_table([]) == {}

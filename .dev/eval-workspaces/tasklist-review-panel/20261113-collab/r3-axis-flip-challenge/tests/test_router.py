import json

from conftest import R3

from r3lib import digest

RT = json.loads((R3 / "config/routing.json").read_text())


def test_routes():
    q = "every acceptance criterion passes"
    assert (
        digest.route(q, None, "reading", RT) == "M3"
        and digest.route(q, None, "search", RT) == "M2"
    )
    c = "`grep -c foo tests/` returns 0"
    assert (
        digest.route(c, None, "reading", RT) == "M4"
        and digest.route(c, None, "search", RT) == "M7"
    )
    t = "| quick | Simple | standard |"
    assert (
        digest.route(t, None, "reading", RT) == "M5"
        and digest.route(t, None, "search", RT) == "M6"
    )
    k = "The worker must keep the old rule here"
    assert (
        digest.route(k, None, "reading", RT) == "M8"
        and digest.route(k, None, "search", RT) == "M8"
    )
    assert digest.route(q, "contradiction", "reading", RT) == "M8"
    assert digest.route(q, "contradiction", "search", RT) == "M8"
    assert digest.route("The sky is blue today here", None, "reading", RT) is None
    assert digest.route("Phase 1: Protocol rules", None, "search", RT) is None
    assert digest.route("mapping of reasons -> outputs", None, "search", RT) == "M6"
    assert digest.route("the run-time steps in order", None, "reading", RT) is None

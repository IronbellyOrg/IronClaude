"""T4 primitive-grep targeting — R-05 acceptance test. Harness §3 T4."""

from __future__ import annotations

from pathlib import Path

from tests.troubleshoot._procedures import overwrite_run_site, primitive_grep

FIX = Path(__file__).parent / "fixtures" / "procedures" / "primitivegrep"


def test_primitive_grep_targets_only_sink_and_overwrites_sentinel() -> None:
    """R-05: hits only sink.sh lines {2,3,7}; decoy excluded; sentinel overwritten."""
    files = {
        "sink.sh": (FIX / "sink.sh").read_text(),
        "decoy.sh": (FIX / "decoy.sh").read_text(),
    }
    hits = primitive_grep(files, {"sink.sh"}, {"read/parse": r"/proc/|/sys/|/dev/"})
    assert all(name == "sink.sh" for name, _, _ in hits), hits
    assert {n for _, n, _ in hits} == {2, 3, 7}, hits
    assert len(hits) <= 8, hits
    locus = "RUN-SITE: pending-producers @ ci-runner\n"
    assert (
        overwrite_run_site(locus, "sink.sh:2") == "RUN-SITE: sink.sh:2 @ ci-runner\n"
    ), locus

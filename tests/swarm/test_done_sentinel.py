"""T07.13 -- ``reduce.emit_done_sentinel`` (DM-017 / FR-027) writer tests.

Pins the IMM-5 reduce-path ``done.json`` emitter exposed by
:func:`superclaude.cli.swarm.reduce.emit_done_sentinel`:

1. **Co-location.** The sentinel lands at ``contract_path.parent /
   "done.json"`` so detached / tmux callers polling with
   ``until [ -f done.json ]`` find it next to ``return-contract.yaml``
   without threading two paths through the executor.
2. **Atomic write.** The writer routes through the tmp + ``os.replace``
   idiom (IMM-6 / NFR-002) so a mid-write SIGKILL leaves either no
   file or the prior file -- never a half-written sentinel that the
   ``-f`` poll would treat as complete. The cross-module IMM-6 sweep
   (``tests/swarm/test_imm6_atomic_write.py``) also guards this; here
   we pin the on-disk behaviour by reading the file back.
3. **Field set.** The sentinel carries exactly the three DM-017
   fields (``atomic_write``, ``terminal_status``, ``contract_path``)
   with the dataclass-default ``atomic_write=True`` and the stringified
   contract path stamped onto the marker.
4. **Polling pattern.** The acceptance criterion's
   ``until [ -f done.json ]`` pattern works against a fixture: before
   the call the file is absent, after the call it is present and
   parseable JSON.
5. **Terminal-status enum.** Only IMM-5 verdicts
   (``success`` / ``partial`` / ``failed``) round-trip cleanly;
   arbitrary strings are rejected by the :class:`DoneSentinel`
   dataclass guard before the bytes hit disk.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from superclaude.cli.swarm.reduce import (
    DONE_SENTINEL_FILENAME,
    emit_done_sentinel,
)


# ---------------------------------------------------------------------------
# Co-location + return value.
# ---------------------------------------------------------------------------


def test_emit_done_sentinel_lands_next_to_contract(tmp_path: Path) -> None:
    """``done.json`` is written to ``contract_path.parent``."""
    contract = tmp_path / "return-contract.yaml"
    contract.write_text("status: success\n", encoding="utf-8")

    target = emit_done_sentinel("success", contract)

    assert target == tmp_path / DONE_SENTINEL_FILENAME
    assert target.is_file()


def test_emit_done_sentinel_accepts_str_contract_path(tmp_path: Path) -> None:
    """The signature accepts ``str`` -- callers that store contract path
    as a string (e.g. the rendered :class:`Artifacts` bundle) need not
    re-wrap in :class:`Path`."""
    contract = tmp_path / "return-contract.yaml"
    contract.write_text("status: success\n", encoding="utf-8")

    target = emit_done_sentinel("partial", str(contract))

    assert target == tmp_path / DONE_SENTINEL_FILENAME


# ---------------------------------------------------------------------------
# Field set (DM-017).
# ---------------------------------------------------------------------------


def test_emit_done_sentinel_payload_carries_dm017_fields(tmp_path: Path) -> None:
    """The emitted JSON has exactly ``atomic_write`` + ``terminal_status``
    + ``contract_path`` -- the three DM-017 fields, nothing more."""
    contract = tmp_path / "return-contract.yaml"
    contract.write_text("status: success\n", encoding="utf-8")

    target = emit_done_sentinel("success", contract)
    payload = json.loads(target.read_text(encoding="utf-8"))

    assert set(payload) == {"atomic_write", "terminal_status", "contract_path"}
    assert payload["atomic_write"] is True
    assert payload["terminal_status"] == "success"
    assert payload["contract_path"] == str(contract)


@pytest.mark.parametrize("status", ["success", "partial", "failed"])
def test_emit_done_sentinel_round_trips_every_imm5_verdict(
    tmp_path: Path, status: str
) -> None:
    """Every IMM-5 terminal status round-trips through JSON intact."""
    contract = tmp_path / "return-contract.yaml"
    contract.write_text("status: " + status + "\n", encoding="utf-8")

    target = emit_done_sentinel(status, contract)  # type: ignore[arg-type]
    payload = json.loads(target.read_text(encoding="utf-8"))

    assert payload["terminal_status"] == status


# ---------------------------------------------------------------------------
# Atomic write (IMM-6).
# ---------------------------------------------------------------------------


def test_emit_done_sentinel_leaves_no_tmp_sibling(tmp_path: Path) -> None:
    """After a successful write, no ``.tmp`` sibling remains.

    The tmp + ``os.replace`` idiom must clean up the temporary file via
    the atomic swap; a stranded ``.tmp`` would mean the writer leaked
    on the happy path. The IMM-6 sweep
    (``tests/swarm/test_imm6_atomic_write.py``) already pins the
    static-source contract; this is the dynamic complement.
    """
    contract = tmp_path / "return-contract.yaml"
    contract.write_text("status: success\n", encoding="utf-8")

    emit_done_sentinel("success", contract)

    siblings = [
        p for p in tmp_path.iterdir() if p.name != "return-contract.yaml"
    ]
    assert siblings == [tmp_path / DONE_SENTINEL_FILENAME], (
        f"Expected only done.json next to the contract; got {siblings!r}"
    )


def test_emit_done_sentinel_overwrites_prior_sentinel(tmp_path: Path) -> None:
    """A second emit replaces the first sentinel's bytes via ``os.replace``.

    The reduce path is **not** idempotent the way the kill path is --
    the kill writer preserves the first sentinel byte-for-byte because
    ``swarm kill`` is operator-initiated and re-runnable; the reduce
    writer is always called exactly once per terminal classification,
    so an overwrite would only happen if the executor re-ran reduce,
    in which case the second result must win.
    """
    contract = tmp_path / "return-contract.yaml"
    contract.write_text("status: partial\n", encoding="utf-8")

    emit_done_sentinel("partial", contract)
    target = emit_done_sentinel("success", contract)

    payload = json.loads(target.read_text(encoding="utf-8"))
    assert payload["terminal_status"] == "success"


# ---------------------------------------------------------------------------
# Polling pattern (acceptance criterion).
# ---------------------------------------------------------------------------


def test_emit_done_sentinel_supports_until_f_polling_pattern(
    tmp_path: Path,
) -> None:
    """``until [ -f done.json ]`` poll resolves only after emission.

    Mirrors the AC for T07.13: "Polling pattern ``until [ -f done.json ]``
    works against fixture". Before the call the file is absent (the
    poll would keep spinning); after the call the file is present and
    parseable JSON (the poll exits and the caller proceeds to read the
    contract).
    """
    contract = tmp_path / "return-contract.yaml"
    contract.write_text("status: success\n", encoding="utf-8")
    target = tmp_path / DONE_SENTINEL_FILENAME

    assert not target.exists()

    emit_done_sentinel("success", contract)

    assert target.is_file()
    # Re-parse to confirm the post-poll caller can extract terminal status.
    payload = json.loads(target.read_text(encoding="utf-8"))
    assert payload["terminal_status"] == "success"


# ---------------------------------------------------------------------------
# Enum guard -- arbitrary strings rejected by DoneSentinel.
# ---------------------------------------------------------------------------


def test_emit_done_sentinel_rejects_unknown_terminal_status(tmp_path: Path) -> None:
    """Out-of-enum ``terminal_status`` raises before any file is written.

    The :class:`DoneSentinel` ``__post_init__`` guard fires inside
    :func:`emit_done_sentinel`, so the writer never reaches
    ``_atomic_write_bytes`` and no partial sentinel hits disk.
    """
    contract = tmp_path / "return-contract.yaml"
    contract.write_text("status: success\n", encoding="utf-8")

    with pytest.raises(ValueError, match="terminal_status"):
        emit_done_sentinel("killed", contract)  # type: ignore[arg-type]

    assert not (tmp_path / DONE_SENTINEL_FILENAME).exists()


# ---------------------------------------------------------------------------
# DM-017 alignment -- payload mirrors DoneSentinel.to_dict().
# ---------------------------------------------------------------------------


def test_emit_done_sentinel_payload_mirrors_dataclass(tmp_path: Path) -> None:
    """The on-disk JSON equals :func:`to_dict` of a :class:`DoneSentinel`
    built with the same inputs -- no extra fields, no rename, no
    serialization drift between the dataclass and the writer."""
    from superclaude.cli.swarm.models import DoneSentinel, to_dict

    contract = tmp_path / "return-contract.yaml"
    contract.write_text("status: failed\n", encoding="utf-8")

    target = emit_done_sentinel("failed", contract)

    on_disk = json.loads(target.read_text(encoding="utf-8"))
    expected = to_dict(
        DoneSentinel(
            atomic_write=True,
            terminal_status="failed",
            contract_path=str(contract),
        )
    )
    assert on_disk == expected

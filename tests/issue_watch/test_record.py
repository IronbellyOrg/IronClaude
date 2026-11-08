"""Tests for the dispatch record, part A: validation, migration, save, lock, kill switch.

Every path is under ``tmp_path`` (through the ``tmp_state`` fixture, which also
moves HOME and XDG inside it); no case sleeps. Test names carry the AC, FR and
NFR ids they assert. The literal key lists below are never read from the module
under test, so adding or dropping a field in ``record.py`` fails the pin test.
"""

from __future__ import annotations

import copy
import dataclasses
import fcntl
import json
import os
import stat
from datetime import datetime, timedelta, timezone

import pytest

from superclaude.cli.issue_watch import record
from superclaude.cli.issue_watch.audit import REASONS
from superclaude.cli.issue_watch.predicates import ApprovalResult
from superclaude.cli.issue_watch.record import (
    Entry,
    FileStore,
    LockError,
    LockHeld,
    PendingContext,
    StoreDoc,
    StoreError,
    TransitionError,
    init_state,
    migrate,
    validate,
)
from superclaude.cli.swarm import atomic

from .conftest import FIXED_NOW

T0 = "2026-11-07T12:00:00Z"
OLD_NS = 1_700_000_000_000_000_000  # an mtime far from "now", in nanoseconds
DROP = object()  # marks a key the builders remove

TOP_KEYS = [
    "schema_version",
    "created_at",
    "next_permitted_at",
    "last_completed_cycle_at",
    "considered",
    "consumed_log",
    "entries",
]
ENTRY_KEYS = [
    "issue",
    "state",
    "attempts",
    "launches",
    "operation_id",
    "approver_id",
    "approval_event_id",
    "approved_at",
    "launch_cwd",
    "launch_login",
    "launch_account_id",
    "consumed_at",
    "pending_at",
    "created_at",
    "updated_at",
    "lease_expires_at",
    "last_reason",
]


def _apply(raw: dict, over: dict) -> dict:
    for key, value in over.items():
        if value is DROP:
            raw.pop(key, None)
        else:
            raw[key] = value
    return raw


def entry_raw(n: int = 7, **over: object) -> dict:
    """A valid ``pending`` entry (launches 1, consumed and pending set)."""
    raw = {
        "issue": n,
        "state": "pending",
        "attempts": 0,
        "launches": 1,
        "operation_id": None,
        "approver_id": 11,
        "approval_event_id": 22,
        "approved_at": "2026-11-07T11:00:00Z",
        "launch_cwd": "/work/repo",
        "launch_login": "watcher-bot",
        "launch_account_id": 33,
        "consumed_at": T0,
        "pending_at": T0,
        "created_at": T0,
        "updated_at": T0,
        "lease_expires_at": None,
        "last_reason": None,
    }
    return _apply(raw, over)


def failed_entry_raw(n: int = 9) -> dict:
    """A valid ``failed`` entry (launches 0, no consumed or pending time)."""
    return entry_raw(
        n,
        state="failed",
        attempts=1,
        launches=0,
        approver_id=None,
        approval_event_id=None,
        approved_at=None,
        launch_cwd=None,
        launch_login=None,
        launch_account_id=None,
        consumed_at=None,
        pending_at=None,
        last_reason="prompt_invalid",
    )


def store_raw(**over: object) -> dict:
    """A valid on-disk document with one ``pending`` and one ``failed`` entry."""
    raw = {
        "schema_version": 1,
        "created_at": "2026-11-07T10:00:00Z",
        "next_permitted_at": None,
        "last_completed_cycle_at": "2026-11-07T11:30:00Z",
        "considered": {"7": T0, "9": T0},
        "consumed_log": ["2026-11-06T13:00:00Z"],
        "entries": {"7": entry_raw(7), "9": failed_entry_raw(9)},
    }
    return _apply(raw, over)


def with_entry(**over: object) -> dict:
    """``store_raw`` whose entry 7 is changed by ``over`` (``DROP`` removes a key)."""
    return store_raw(entries={"7": entry_raw(7, **over)})


def put(store: FileStore, raw: object) -> bytes:
    """Write ``raw`` as the store file and return its bytes."""
    data = json.dumps(raw).encode()
    (store.state_dir / "dispatch.json").write_bytes(data)
    return data


def assert_invalid(store: FileStore, data: bytes) -> None:
    """``load`` raises ``store_invalid`` and leaves the file's bytes and mtime."""
    path = store.state_dir / "dispatch.json"
    path.write_bytes(data)
    os.utime(path, ns=(OLD_NS, OLD_NS))
    with pytest.raises(StoreError) as info:
        store.load()
    assert info.value.reason == "store_invalid"
    assert path.read_bytes() == data
    assert path.stat().st_mtime_ns == OLD_NS


def hold(store: FileStore):
    """Enter the store lock and discard the result; for ``pytest.raises`` blocks."""
    with store.lock():
        pass


# --------------------------------------------------------------------------- load


def test_valid_document_loads_with_int_keys_and_aware_times(tmp_state):
    put(tmp_state, store_raw())
    doc = tmp_state.load()
    assert doc.schema_version == 1
    assert doc.created_at == datetime(2026, 11, 7, 10, 0, tzinfo=timezone.utc)
    assert sorted(doc.entries) == [7, 9]
    assert sorted(doc.considered) == [7, 9]
    assert doc.entries[7].state == "pending"
    assert doc.entries[7].consumed_at == FIXED_NOW
    assert doc.entries[9].consumed_at is None
    assert doc.consumed_log == (datetime(2026, 11, 6, 13, tzinfo=timezone.utc),)
    assert doc.last_completed_cycle_at == datetime(
        2026, 11, 7, 11, 30, tzinfo=timezone.utc
    )
    assert doc.entries[7].approved_at == datetime(
        2026, 11, 7, 11, 0, tzinfo=timezone.utc
    )
    assert doc.entries[7].pending_at == FIXED_NOW
    assert tmp_state.migrated is False


def test_schema_key_lists_match_the_module():
    assert set(Entry.__dataclass_fields__) == set(ENTRY_KEYS)
    assert set(record._STORE_KEYS) == set(TOP_KEYS)


def test_ac22_load_missing_file_is_store_missing__nfr011(tmp_state, tmp_path):
    (tmp_state.state_dir / "dispatch.json").unlink()
    with pytest.raises(StoreError) as info:
        tmp_state.load()
    assert info.value.reason == "store_missing"
    assert not (tmp_state.state_dir / "dispatch.json").exists()
    with pytest.raises(StoreError) as info:
        FileStore(tmp_path / "no-such-dir").load()
    assert info.value.reason == "store_missing"


def test_ac22_load_unreadable_path_is_store_invalid__nfr011(tmp_state):
    path = tmp_state.state_dir / "dispatch.json"
    path.unlink()
    path.mkdir()
    with pytest.raises(StoreError) as info:
        tmp_state.load()
    assert info.value.reason == "store_invalid"


@pytest.mark.parametrize("cut", [0, 1, 20, 150])
def test_ac22_truncated_json_is_store_invalid__nfr011(tmp_state, cut):
    full = json.dumps(store_raw(), indent=2).encode()
    assert cut < len(full)
    assert_invalid(tmp_state, full[:cut])


@pytest.mark.parametrize(
    "data",
    [b"[]", b"null", b'"text"', b"7", b"\xff\xfe not utf-8", b"{} trailing"],
    ids=["list", "null", "string", "number", "binary", "trailing"],
)
def test_ac22_non_object_or_garbage_is_store_invalid__nfr011(tmp_state, data):
    assert_invalid(tmp_state, data)


@pytest.mark.parametrize("key", TOP_KEYS)
def test_ac22_missing_top_level_key_is_store_invalid__nfr011(tmp_state, key):
    assert_invalid(tmp_state, json.dumps(store_raw(**{key: DROP})).encode())


def test_ac22_extra_top_level_key_is_store_invalid__nfr011(tmp_state):
    assert_invalid(tmp_state, json.dumps(store_raw(surplus=1)).encode())


@pytest.mark.parametrize("key", ENTRY_KEYS)
def test_ac22_missing_entry_key_is_store_invalid__nfr011(tmp_state, key):
    assert_invalid(tmp_state, json.dumps(with_entry(**{key: DROP})).encode())


def test_ac22_extra_entry_key_is_store_invalid__nfr011(tmp_state):
    assert_invalid(tmp_state, json.dumps(with_entry(surplus=1)).encode())


@pytest.mark.parametrize(
    "over",
    [
        {"considered": []},
        {"considered": None},
        {"consumed_log": {}},
        {"consumed_log": "x"},
        {"entries": []},
        {"entries": None},
        {"created_at": 20261107100000},
        {"next_permitted_at": 5},
        {"last_completed_cycle_at": 5},
        {"last_completed_cycle_at": ["2026-11-07T11:30:00Z"]},
        {"considered": {"7": 5}},
        {"consumed_log": [5]},
        {"entries": {"7": []}},
        {"entries": {"7": None}},
    ],
    ids=lambda over: next(iter(over)) + "=" + json.dumps(over)[-14:],
)
def test_ac22_wrong_top_level_type_is_store_invalid__nfr011(tmp_state, over):
    assert_invalid(tmp_state, json.dumps(store_raw(**over)).encode())


@pytest.mark.parametrize(
    "over",
    [
        {"issue": "7"},
        {"issue": 7.0},
        {"issue": None},
        {"state": 3},
        {"state": "done"},
        {"state": None},
        {"attempts": "1"},
        {"attempts": True},
        {"attempts": 1.5},
        {"attempts": -1},
        {"launches": True},
        {"launches": "1"},
        {"operation_id": 5},
        {"approver_id": "11"},
        {"approval_event_id": 2.5},
        {"launch_account_id": "33"},
        {"launch_login": 5},
        {"launch_cwd": 5},
        {"launch_cwd": "relative/path"},
        {"last_reason": 5},
        {"approved_at": 5},
        {"lease_expires_at": ["x"]},
    ],
    ids=lambda over: next(iter(over)) + "=" + json.dumps(over)[-12:],
)
def test_ac22_wrong_entry_type_is_store_invalid__nfr011(tmp_state, over):
    assert_invalid(tmp_state, json.dumps(with_entry(**over)).encode())


@pytest.mark.parametrize("key", ["07", "0", "-7", "abc", "7.0", " 7", ""])
def test_ac22_entry_key_not_a_decimal_issue_is_store_invalid__nfr011(tmp_state, key):
    raw = store_raw(entries={key: entry_raw(7)})
    assert_invalid(tmp_state, json.dumps(raw).encode())


@pytest.mark.parametrize("where", ["entries", "considered"])
@pytest.mark.parametrize("digits", [10, 4301, 20000])
def test_ac22_overlong_digit_key_is_store_invalid_not_valueerror__nfr011(
    tmp_state, where, digits
):
    """A key of 4301+ digits made ``int(key)`` raise a raw ``ValueError`` (B-12)."""
    key = "1" * digits
    raw = store_raw(**{where: {key: entry_raw(7) if where == "entries" else T0}})
    assert_invalid(tmp_state, json.dumps(raw).encode())


def test_ac22_deeply_nested_json_is_store_invalid_not_recursionerror__nfr011(
    tmp_state,
):
    """``json.loads`` raises ``RecursionError`` on deep nesting; ``load`` must type it."""
    depth = 100_000
    assert_invalid(tmp_state, b"[" * depth + b"]" * depth)
    assert_invalid(tmp_state, b'{"a":' * depth + b"1" + b"}" * depth)


@pytest.mark.parametrize(
    "bad",
    ["a;b", "$(id)", "op\n1", "x; rm -rf ~\n\x1b[31m", "x" * 129, "", "a b", "a/b"],
    ids=[
        "semicolon",
        "subshell",
        "newline",
        "escape",
        "129-chars",
        "empty",
        "space",
        "slash",
    ],
)
def test_ac22_unsafe_operation_id_on_disk_is_store_invalid__nfr011(tmp_state, bad):
    """``status`` prints the stored id in a shell command, so ``load`` refuses a bad one."""
    assert_invalid(tmp_state, json.dumps(with_entry(operation_id=bad)).encode())


@pytest.mark.parametrize("good", ["a", "op-1", "A.b_c:d-9", "x" * 128])
def test_ac22_safe_operation_id_on_disk_loads__nfr011(tmp_state, good):
    put(tmp_state, with_entry(operation_id=good))
    assert tmp_state.load().entries[7].operation_id == good


def test_ac22_issue_not_equal_to_its_key_is_store_invalid__nfr011(tmp_state):
    assert_invalid(tmp_state, json.dumps(with_entry(issue=8)).encode())
    raw = store_raw(entries={"8": entry_raw(7)})
    assert_invalid(tmp_state, json.dumps(raw).encode())


def test_ac22_launches_two_is_store_invalid__nfr011(tmp_state):
    assert_invalid(tmp_state, json.dumps(with_entry(launches=2)).encode())
    assert_invalid(tmp_state, json.dumps(with_entry(launches=-1)).encode())


def test_ac22_failed_with_one_launch_is_store_invalid__nfr011(tmp_state):
    assert_invalid(tmp_state, json.dumps(with_entry(state="failed")).encode())


@pytest.mark.parametrize("missing", ["consumed_at", "pending_at"])
def test_ac22_one_launch_without_its_times_is_store_invalid__nfr011(tmp_state, missing):
    assert_invalid(tmp_state, json.dumps(with_entry(**{missing: None})).encode())


BAD_TIMES = [
    "2026-11-07T12:00:00",
    "2026-11-07T12:00:00+00:00",
    "2026-11-07T12:00:00-05:00",
    "2026-11-07 12:00:00Z",
    "2026-11-07T12:00:00z",
    "2026-11-07T12:00:00.5Z",
    "2026-11-07T12:00Z",
    "2026-11-7T12:00:00Z",
    "2026-13-07T12:00:00Z",
    "",
    "now",
]
TIME_PLACES = {
    "created_at": lambda t: store_raw(created_at=t),
    "next_permitted_at": lambda t: store_raw(next_permitted_at=t),
    "last_completed_cycle_at": lambda t: store_raw(last_completed_cycle_at=t),
    "considered": lambda t: store_raw(considered={"7": t}),
    "consumed_log": lambda t: store_raw(consumed_log=[t]),
    "consumed_at": lambda t: with_entry(consumed_at=t),
    "approved_at": lambda t: with_entry(approved_at=t),
    "pending_at": lambda t: with_entry(pending_at=t),
    "updated_at": lambda t: with_entry(updated_at=t),
    "lease_expires_at": lambda t: with_entry(lease_expires_at=t),
}


@pytest.mark.parametrize("place", sorted(TIME_PLACES))
@pytest.mark.parametrize("bad", BAD_TIMES)
def test_ac22_naive_or_non_z_time_is_store_invalid__nfr011(tmp_state, place, bad):
    assert_invalid(tmp_state, json.dumps(TIME_PLACES[place](bad)).encode())


@pytest.mark.parametrize(
    "version",
    [True, False, "1", 1.0, None, 2, 99, 0, -1],
    ids=["true", "false", "str", "float", "null", "two", "99", "zero", "minus1"],
)
def test_ac22_bad_schema_version_is_store_invalid__nfr011(tmp_state, version):
    assert_invalid(tmp_state, json.dumps(store_raw(schema_version=version)).encode())


def test_validate_rejects_non_dict_input_without_touching_files():
    for raw in (None, [], "x", 3):
        with pytest.raises(StoreError) as info:
            validate(raw)
        assert info.value.reason == "store_invalid"


# ------------------------------------------------------------------------ migrate


def v0_raw() -> dict:
    """A test-only v0 document: version 0 plus a legacy key the step removes."""
    raw = store_raw(schema_version=0)
    raw["legacy_note"] = "kept only in v0"
    return raw


def v0_to_v1(doc: dict) -> dict:
    """A pure v0 -> v1 step: drop ``legacy_note``, bump the version."""
    new = {k: v for k, v in doc.items() if k != "legacy_note"}
    new["schema_version"] = 1
    return new


def test_ac22_migrate_keeps_every_entry_and_consumed_at__nfr011():
    old = v0_raw()
    snapshot = json.dumps(old, sort_keys=True)
    moved = migrate(old, migrations={0: v0_to_v1})
    assert moved["schema_version"] == 1
    assert json.dumps(old, sort_keys=True) == snapshot  # input never mutated
    assert moved["entries"] == store_raw()["entries"]
    doc = validate(moved)
    assert doc == validate(store_raw())
    assert doc.entries[7].consumed_at == FIXED_NOW
    assert doc.entries[9].consumed_at is None


def test_migrate_current_version_is_returned_as_is():
    raw = store_raw()
    assert migrate(raw, migrations={}) is raw
    assert migrate(raw) is raw


def test_migrations_ship_empty_and_default_has_no_step_for_v0():
    assert record.MIGRATIONS == {}
    with pytest.raises(StoreError) as info:
        migrate(v0_raw())
    assert info.value.reason == "store_invalid"


def test_ac22_migrate_chains_steps_in_order__nfr011(monkeypatch):
    monkeypatch.setattr(record, "SCHEMA_VERSION", 3)
    order: list[int] = []

    def step(v: int):
        def run(doc: dict) -> dict:
            order.append(v)
            return {**doc, "schema_version": v + 1}

        return run

    out = migrate(
        {"schema_version": 0}, migrations={0: step(0), 1: step(1), 2: step(2)}
    )
    assert order == [0, 1, 2]
    assert out["schema_version"] == 3


@pytest.mark.parametrize(
    "doc, migrations",
    [
        (None, {}),
        ([], {}),
        ({}, {}),
        ({"schema_version": True}, {}),
        ({"schema_version": "0"}, {0: v0_to_v1}),
        ({"schema_version": 2}, {0: v0_to_v1}),
        ({"schema_version": 0}, {}),
        ({"schema_version": 0}, {0: lambda d: {**d, "schema_version": 0}}),
        ({"schema_version": 0}, {0: lambda d: {**d, "schema_version": 2}}),
        ({"schema_version": 0}, {0: lambda d: {**d, "schema_version": True}}),
        ({"schema_version": 0}, {0: lambda d: [d]}),
        ({"schema_version": 0}, {0: lambda d: {"entries": {}}}),
    ],
    ids=[
        "none",
        "list",
        "no-version",
        "bool",
        "str",
        "higher",
        "no-step",
        "step-stays",
        "step-skips",
        "step-bool",
        "step-list",
        "step-drops-version",
    ],
)
def test_ac22_migrate_refuses_unusable_input__nfr011(doc, migrations):
    with pytest.raises(StoreError) as info:
        migrate(doc, migrations=migrations)
    assert info.value.reason == "store_invalid"


def test_ac22_file_store_migrates_in_memory_and_never_writes__nfr011(tmp_state):
    data = put(tmp_state, v0_raw())
    path = tmp_state.state_dir / "dispatch.json"
    os.utime(path, ns=(OLD_NS, OLD_NS))
    store = FileStore(tmp_state.state_dir, migrations={0: v0_to_v1})
    assert store.migrated is False
    doc = store.load()
    assert store.migrated is True
    assert doc == validate(store_raw())
    assert doc.entries[7].consumed_at == FIXED_NOW
    # A dry-run style flow loads (twice) and never saves: the file is untouched.
    assert store.load() == doc
    assert path.read_bytes() == data
    assert path.stat().st_mtime_ns == OLD_NS


def test_ac22_saving_a_migrated_store_writes_the_current_version__nfr011(tmp_state):
    put(tmp_state, v0_raw())
    store = FileStore(tmp_state.state_dir, migrations={0: v0_to_v1})
    store.save(store.load())
    written = json.loads((tmp_state.state_dir / "dispatch.json").read_bytes())
    assert written["schema_version"] == 1
    assert "legacy_note" not in written
    assert store.load().entries[7].consumed_at == FIXED_NOW
    assert store.migrated is False


def test_file_store_without_seam_uses_the_module_migrations(tmp_state):
    assert tmp_state.migrations is record.MIGRATIONS
    put(tmp_state, v0_raw())
    with pytest.raises(StoreError) as info:
        tmp_state.load()
    assert info.value.reason == "store_invalid"


def test_ac22_a_failed_load_resets_migrated__nfr011(tmp_state):
    put(tmp_state, v0_raw())
    store = FileStore(tmp_state.state_dir, migrations={0: v0_to_v1})
    store.load()
    assert store.migrated is True
    put(store, store_raw(entries=[]))
    with pytest.raises(StoreError):
        store.load()
    assert store.migrated is False


# --------------------------------------------------------------------------- save


def test_ac13_second_save_of_the_same_doc_is_byte_identical__fr019(tmp_state):
    doc = validate(store_raw())
    path = tmp_state.state_dir / "dispatch.json"
    tmp_state.save(doc)
    first = path.read_bytes()
    tmp_state.save(doc)
    assert path.read_bytes() == first
    tmp_state.save(tmp_state.load())  # a load/save round trip changes nothing
    assert path.read_bytes() == first


def test_ac13_saved_file_is_sorted_indented_ascii_with_final_newline__fr019(
    tmp_state,
):
    tmp_state.save(validate(store_raw()))
    data = (tmp_state.state_dir / "dispatch.json").read_bytes()
    assert data.endswith(b"}\n") and not data.endswith(b"\n\n")
    data.decode("ascii")
    parsed = json.loads(data)
    assert list(parsed) == sorted(parsed)
    assert list(parsed["entries"]["7"]) == sorted(parsed["entries"]["7"])
    assert data == json.dumps(parsed, sort_keys=True, indent=2).encode() + b"\n"
    assert validate(parsed) == validate(store_raw())


def test_save_orders_issue_keys_as_decimal_strings(tmp_state):
    raw = store_raw(
        considered={"10": T0, "9": T0},
        entries={"10": entry_raw(10), "9": failed_entry_raw(9)},
    )
    tmp_state.save(validate(raw))
    parsed = json.loads((tmp_state.state_dir / "dispatch.json").read_bytes())
    assert list(parsed["considered"]) == ["10", "9"]  # string order, not int order
    assert tmp_state.load().entries[10].issue == 10


def test_save_forces_mode_0600_over_a_wider_existing_file(tmp_state):
    path = tmp_state.state_dir / "dispatch.json"
    os.chmod(path, 0o666)
    tmp_state.save(validate(store_raw()))
    assert stat.S_IMODE(path.stat().st_mode) == 0o600


def test_save_chmod_is_a_guard_when_the_writer_leaves_a_wider_file(
    tmp_state, monkeypatch
):
    real = atomic.write_prepared_bytes

    def wide(path, data):
        written = real(path, data)
        os.chmod(path, 0o666)
        return written

    monkeypatch.setattr(atomic, "write_prepared_bytes", wide)
    tmp_state.save(validate(store_raw()))
    path = tmp_state.state_dir / "dispatch.json"
    assert stat.S_IMODE(path.stat().st_mode) == 0o600


def test_init_state_makes_dir_0700_and_files_0600_under_a_permissive_umask(tmp_path):
    old = os.umask(0)
    try:
        store = init_state(tmp_path / "fresh" / "state", FIXED_NOW)
    finally:
        os.umask(old)
    state_dir = store.state_dir
    assert stat.S_IMODE(state_dir.stat().st_mode) == 0o700
    assert stat.S_IMODE((state_dir / "lock").stat().st_mode) == 0o600
    assert stat.S_IMODE((state_dir / "dispatch.json").stat().st_mode) == 0o600
    assert store.load().created_at == FIXED_NOW


def test_ac22_save_fsyncs_the_state_directory_last__nfr005(tmp_state, monkeypatch):
    real = os.fsync
    seen: list[tuple[bool, int]] = []

    def counting(fd):
        st = os.fstat(fd)
        seen.append((stat.S_ISDIR(st.st_mode), st.st_ino))
        real(fd)

    monkeypatch.setattr(os, "fsync", counting)
    tmp_state.save(validate(store_raw()))
    dir_ino = tmp_state.state_dir.stat().st_ino
    assert (True, dir_ino) in seen
    assert seen[-1] == (True, dir_ino)  # after the file's own fsync
    assert any(not is_dir for is_dir, _ in seen)


def test_save_calls_write_prepared_bytes_through_the_lazy_import(
    tmp_state, monkeypatch
):
    real = atomic.write_prepared_bytes
    calls: list[tuple[object, bytes]] = []

    def spy(path, data):
        calls.append((path, data))
        return real(path, data)

    monkeypatch.setattr(atomic, "write_prepared_bytes", spy)
    assert not hasattr(record, "write_prepared_bytes")  # no module-level binding
    doc = validate(store_raw())
    tmp_state.save(doc)
    assert len(calls) == 1
    path, data = calls[0]
    assert path == tmp_state.state_dir / "dispatch.json"
    assert data.endswith(b"\n")
    assert validate(json.loads(data)) == doc


def test_save_surfaces_a_failed_write_and_keeps_the_old_file(tmp_state, monkeypatch):
    path = tmp_state.state_dir / "dispatch.json"
    before = path.read_bytes()

    def boom(path, data):
        raise OSError("disk full")

    monkeypatch.setattr(atomic, "write_prepared_bytes", boom)
    with pytest.raises(OSError):
        tmp_state.save(validate(store_raw()))
    assert path.read_bytes() == before


# --------------------------------------------------------------------------- lock


def test_ac11_lock_file_missing_is_lock_missing__fr017(tmp_state):
    (tmp_state.state_dir / "lock").unlink()
    with pytest.raises(LockError) as info:
        hold(tmp_state)
    assert info.value.reason == "lock_missing"


def test_ac11_lock_symlink_is_lock_invalid__fr017(tmp_state, tmp_path):
    target = tmp_path / "elsewhere"
    target.write_bytes(b"")
    lock = tmp_state.state_dir / "lock"
    lock.unlink()
    lock.symlink_to(target)
    with pytest.raises(LockError) as info:
        hold(tmp_state)
    assert info.value.reason == "lock_invalid"


def test_ac11_dangling_lock_symlink_is_lock_invalid__fr017(tmp_state, tmp_path):
    lock = tmp_state.state_dir / "lock"
    lock.unlink()
    lock.symlink_to(tmp_path / "does-not-exist")
    with pytest.raises(LockError) as info:
        hold(tmp_state)
    assert info.value.reason == "lock_invalid"


def test_ac11_lock_directory_is_lock_invalid__fr017(tmp_state):
    lock = tmp_state.state_dir / "lock"
    lock.unlink()
    lock.mkdir()
    with pytest.raises(LockError) as info:
        hold(tmp_state)
    assert info.value.reason == "lock_invalid"


@pytest.mark.skipif(os.geteuid() == 0, reason="root ignores file permission bits")
def test_ac11_unopenable_lock_file_is_lock_invalid__fr017(tmp_state):
    """A lock the user cannot open is a typed ``lock_invalid``, not a raw OSError (B-3)."""
    lock = tmp_state.state_dir / "lock"
    os.chmod(lock, 0)
    try:
        with pytest.raises(LockError) as info:
            hold(tmp_state)
    finally:
        os.chmod(lock, 0o600)
    assert info.value.reason == "lock_invalid"
    hold(tmp_state)  # the failed open held nothing


def test_ac11_lock_with_a_foreign_owner_is_lock_invalid__fr017(tmp_state, monkeypatch):
    real = os.geteuid
    monkeypatch.setattr(os, "geteuid", lambda: real() + 1)
    with pytest.raises(LockError) as info:
        hold(tmp_state)
    assert info.value.reason == "lock_invalid"
    monkeypatch.setattr(os, "geteuid", real)
    hold(tmp_state)  # a rejected lock leaves nothing held


def test_ac11_second_open_file_description_gives_lock_held__fr017(tmp_state):
    lock = tmp_state.state_dir / "lock"
    other = os.open(lock, os.O_RDWR)
    try:
        fcntl.flock(other, fcntl.LOCK_EX | fcntl.LOCK_NB)
        with pytest.raises(LockHeld):
            hold(tmp_state)
        with pytest.raises(LockHeld):  # and again: the refusal released nothing
            hold(tmp_state)
    finally:
        os.close(other)
    hold(tmp_state)  # free once the other description is closed


def test_ac11_nested_lock_is_held_and_the_outer_lock_survives__fr017(tmp_state):
    probe = os.open(tmp_state.state_dir / "lock", os.O_RDWR)
    try:
        with tmp_state.lock():
            with pytest.raises(LockHeld):
                hold(tmp_state)
            with pytest.raises(BlockingIOError):  # outer lock still held
                fcntl.flock(probe, fcntl.LOCK_EX | fcntl.LOCK_NB)
        fcntl.flock(probe, fcntl.LOCK_EX | fcntl.LOCK_NB)  # released on exit
    finally:
        os.close(probe)


@pytest.mark.parametrize("swap", ["replace", "unlink", "rename_aside"])
def test_ac11_lock_replaced_or_unlinked_after_flock_is_lock_held__fr017(
    tmp_state, monkeypatch, swap
):
    """FR-017, design 7.6: any swap of the lock path after the flock is LockHeld.

    `rename_aside` keeps the old inode linked (``st_nlink`` stays 1) and leaves a
    file at the path, so only the ``(st_dev, st_ino)`` comparison can catch it.
    """
    lock = tmp_state.state_dir / "lock"
    real = fcntl.flock
    done: list[bool] = []

    def flock_then_swap(fd, op):
        real(fd, op)
        if op & fcntl.LOCK_EX and not done:
            done.append(True)
            if swap == "replace":
                # The old file is still open, so its inode cannot be reused.
                fresh = lock.with_name("lock.new")
                fresh.write_bytes(b"")
                os.replace(fresh, lock)
            elif swap == "rename_aside":
                os.rename(lock, lock.with_name("lock.aside"))
                lock.write_bytes(b"")
            else:
                lock.unlink()

    monkeypatch.setattr(fcntl, "flock", flock_then_swap)
    with pytest.raises(LockHeld):
        hold(tmp_state)
    assert done == [True]
    monkeypatch.setattr(fcntl, "flock", real)
    if swap in ("replace", "rename_aside"):
        hold(tmp_state)  # the new file is a normal lock
    else:
        with pytest.raises(LockError) as info:
            hold(tmp_state)
        assert info.value.reason == "lock_missing"


@pytest.mark.parametrize(
    "raised", [SystemExit(3), KeyboardInterrupt(), RuntimeError("boom")]
)
def test_ac22_lock_is_free_again_after_an_exit_inside_the_with__nfr005(
    tmp_state, raised
):
    with pytest.raises(type(raised)):
        with tmp_state.lock():
            raise raised
    probe = os.open(tmp_state.state_dir / "lock", os.O_RDWR)
    try:
        fcntl.flock(probe, fcntl.LOCK_EX | fcntl.LOCK_NB)  # not held by a leak
    finally:
        os.close(probe)
    with tmp_state.lock():  # and the store lock can be taken again
        pass


def test_lock_is_released_on_normal_exit_and_reusable(tmp_state):
    for _ in range(3):
        with tmp_state.lock():
            pass


# ------------------------------------------------------------------ kill switch


def test_ac12_disabled_absent_means_enabled__fr018(tmp_state):
    assert tmp_state.disabled() is False
    assert tmp_state.disabled_since() is None
    assert record.disabled_present(tmp_state.state_dir) is False


def test_ac12_disabled_present_reports_the_aware_mtime__fr018(tmp_state):
    flag = tmp_state.state_dir / "DISABLED"
    flag.write_bytes(b"")
    stamp = (FIXED_NOW - timedelta(days=2, hours=3)).timestamp()
    os.utime(flag, (stamp, stamp))
    assert tmp_state.disabled() is True
    assert record.disabled_present(tmp_state.state_dir) is True
    since = tmp_state.disabled_since()
    assert since == FIXED_NOW - timedelta(days=2, hours=3)
    assert since.tzinfo is not None
    assert since.utcoffset() == timedelta(0)


def test_ac12_disabled_counts_for_any_content_or_a_dangling_link__fr018(tmp_state):
    flag = tmp_state.state_dir / "DISABLED"
    flag.symlink_to(tmp_state.state_dir / "nowhere")
    assert tmp_state.disabled() is True
    flag.unlink()
    flag.write_text("stopped by the owner\n")
    assert tmp_state.disabled() is True


def test_ac12_disabled_switch_never_touches_the_store_files__fr018(tmp_state):
    path = tmp_state.state_dir / "dispatch.json"
    before = (path.read_bytes(), path.stat().st_mtime_ns)
    (tmp_state.state_dir / "DISABLED").write_bytes(b"")
    tmp_state.disabled()
    tmp_state.disabled_since()
    assert (path.read_bytes(), path.stat().st_mtime_ns) == before


# ============================================================================
# Part B: transitions T-1 to T-13 (design section 7.4) and half-open windows
# (section 7.5). Every expected value below is a literal; nothing is read from
# the module under test. ``doc_of`` and ``ent`` check that every ``last_reason``
# a case builds or receives is a member of ``audit.REASONS`` (decision DF-42).
# ============================================================================

NOW_B = datetime(2026, 11, 7, 13, 0, 0, tzinfo=timezone.utc)
APPROVED = datetime(2026, 11, 7, 11, 0, 0, tzinfo=timezone.utc)
LEASE_END = "2026-11-07T14:00:00Z"  # 60 min after the 13:00 launch used below


def blank(**over: object) -> Entry:
    """Issue 7 as a ``failed`` entry of 12:00 with every optional field null."""
    fields: dict = {
        "issue": 7,
        "state": "failed",
        "attempts": 0,
        "launches": 0,
        "operation_id": None,
        "approver_id": None,
        "approval_event_id": None,
        "approved_at": None,
        "launch_cwd": None,
        "launch_login": None,
        "launch_account_id": None,
        "consumed_at": None,
        "pending_at": None,
        "created_at": FIXED_NOW,
        "updated_at": FIXED_NOW,
        "lease_expires_at": None,
        "last_reason": None,
    }
    fields.update(over)
    return Entry(**fields)


PENDING_FIELDS = {
    "state": "pending",
    "launches": 1,
    "approver_id": 11,
    "approval_event_id": 22,
    "approved_at": APPROVED,
    "launch_cwd": "/work/repo",
    "launch_login": "watcher-bot",
    "launch_account_id": 33,
    "consumed_at": FIXED_NOW,
    "pending_at": FIXED_NOW,
}


def pending(**over: object) -> Entry:
    """Issue 7 as the ``pending`` entry that ``entry_raw(7)`` describes."""
    return blank(**{**PENDING_FIELDS, **over})


CTX = PendingContext(
    approver_id=11,
    approval_event_id=22,
    approved_at=APPROVED,
    launch_cwd="/work/repo",
    launch_login="watcher-bot",
    launch_account_id=33,
)
APPROVAL = ApprovalResult(
    approved=True,
    reason=None,
    approver_id=44,
    approval_event_id=55,
    approved_at=datetime(2026, 11, 7, 12, 30, 0, tzinfo=timezone.utc),
)

STATE_RAWS = {
    "pending": lambda n=7: entry_raw(n),
    "launched": lambda n=7: entry_raw(
        n,
        state="launched",
        operation_id="op-1",
        lease_expires_at=LEASE_END,
        last_reason="launched",
    ),
    "unknown": lambda n=7: entry_raw(n, state="unknown", last_reason="launch_unknown"),
    "failed": lambda n=7: failed_entry_raw(n),
    "abandoned": lambda n=7: entry_raw(
        n, state="abandoned", last_reason="claim_not_observed"
    ),
    "claimed": lambda n=7: entry_raw(n, state="claimed", last_reason="claimed"),
}


def tombstone_raw(n: int = 7) -> dict:
    """An ``abandoned`` ``attempts_exhausted`` entry: no ``pending_at``, no launch."""
    return {
        **failed_entry_raw(n),
        "state": "abandoned",
        "attempts": 3,
        "last_reason": "attempts_exhausted",
    }


def check_reasons(doc: StoreDoc) -> None:
    for entry in doc.entries.values():
        assert entry.last_reason is None or entry.last_reason in REASONS


def doc_of(*raws: dict, consumed_log: tuple[str, ...] = ()) -> StoreDoc:
    """A validated document holding exactly ``raws`` (each keyed by its issue)."""
    doc = validate(
        store_raw(
            considered={},
            consumed_log=list(consumed_log),
            entries={str(raw["issue"]): raw for raw in raws},
        )
    )
    check_reasons(doc)
    return doc


def doc_in(state: str | None) -> StoreDoc:
    """A document with issue 7 in ``state``; ``None`` means no entry."""
    return doc_of() if state is None else doc_of(STATE_RAWS[state]())


def ent(doc: StoreDoc, n: int = 7) -> Entry:
    """Entry ``n`` of ``doc`` after checking every ``last_reason`` in it."""
    check_reasons(doc)
    return doc.entries[n]


def failed_with(attempts: int) -> StoreDoc:
    return doc_of({**failed_entry_raw(7), "attempts": attempts})


# ------------------------------------------------------------------ T-1 to T-3


@pytest.mark.parametrize("reason", ["prompt_invalid", "revalidation_transient"])
def test_t1_first_failure_makes_a_failed_entry_with_one_attempt__nfr005(reason):
    before = doc_of()
    after = record.fail(before, 7, reason, NOW_B)
    assert ent(after) == blank(
        state="failed",
        attempts=1,
        launches=0,
        created_at=NOW_B,
        updated_at=NOW_B,
        last_reason=reason,
    )
    assert before.entries == {}


def test_t2_failed_entry_is_eligible_after_ten_minutes_and_nothing_changes__nfr005():
    doc = doc_of(failed_entry_raw(7))
    before = copy.deepcopy(doc)
    result = record.backoff_elapsed(doc.entries[7], FIXED_NOW + timedelta(minutes=10))
    assert result is True
    assert doc == before
    assert ent(doc) == blank(state="failed", attempts=1, last_reason="prompt_invalid")


@pytest.mark.parametrize("attempts", [1, 2])
def test_t2_failed_entry_below_three_attempts_is_eligible__nfr005(attempts):
    entry = ent(failed_with(attempts))
    later = FIXED_NOW + timedelta(days=1)
    assert record.backoff_elapsed(entry, later) is True


@pytest.mark.parametrize("attempts", [3, 4])
def test_t2_failed_entry_with_three_attempts_is_never_eligible__nfr005(attempts):
    entry = ent(failed_with(attempts))
    assert entry.state == "failed"
    assert record.backoff_elapsed(entry, FIXED_NOW + timedelta(minutes=10)) is False
    assert record.backoff_elapsed(entry, FIXED_NOW + timedelta(days=30)) is False


def test_t3_third_failure_abandons_with_attempts_exhausted__nfr005():
    before = failed_with(2)
    after = record.fail(before, 7, "revalidation_transient", NOW_B)
    assert ent(after) == blank(
        state="abandoned",
        attempts=3,
        launches=0,
        created_at=FIXED_NOW,
        updated_at=NOW_B,
        last_reason="attempts_exhausted",
    )
    assert ent(before) == blank(
        state="failed", attempts=2, last_reason="prompt_invalid"
    )


def test_df43_fail_on_a_failed_entry_counts_up_one_two_three_then_abandons__nfr005():
    t2 = datetime(2026, 11, 7, 12, 10, 0, tzinfo=timezone.utc)
    t3 = datetime(2026, 11, 7, 12, 20, 0, tzinfo=timezone.utc)
    first = record.fail(doc_of(), 7, "prompt_invalid", FIXED_NOW)
    second = record.fail(first, 7, "revalidation_transient", t2)
    third = record.fail(second, 7, "prompt_invalid", t3)
    assert ent(first) == blank(state="failed", attempts=1, last_reason="prompt_invalid")
    assert ent(second) == blank(
        state="failed", attempts=2, updated_at=t2, last_reason="revalidation_transient"
    )
    assert ent(third) == blank(
        state="abandoned", attempts=3, updated_at=t3, last_reason="attempts_exhausted"
    )
    with pytest.raises(TransitionError):  # an exhausted entry takes no more failures
        record.fail(third, 7, "prompt_invalid", t3)


# ------------------------------------------------------------------ T-4 to T-9


def test_t4_pending_from_no_entry_sets_launch_and_approval_fields__fr010_fr011():
    before = doc_of()
    after = record.mark_pending(before, 7, CTX, NOW_B)
    assert ent(after) == pending(
        attempts=0,
        launches=1,
        consumed_at=NOW_B,
        pending_at=NOW_B,
        created_at=NOW_B,
        updated_at=NOW_B,
        last_reason=None,
    )
    assert before.entries == {}


def test_t4_pending_from_failed_keeps_attempts_and_clears_the_reason__fr010_fr011():
    before = failed_with(2)
    after = record.mark_pending(before, 7, CTX, NOW_B)
    assert ent(after) == pending(
        attempts=2,
        launches=1,
        consumed_at=NOW_B,
        pending_at=NOW_B,
        created_at=FIXED_NOW,
        updated_at=NOW_B,
        last_reason=None,
    )
    assert ent(before) == blank(
        state="failed", attempts=2, last_reason="prompt_invalid"
    )


def test_t5_launched_outcome_sets_operation_id_and_a_sixty_minute_lease__fr013():
    before = doc_in("pending")
    after = record.mark_launched(before, 7, "op-123", NOW_B)
    assert ent(after) == pending(
        state="launched",
        operation_id="op-123",
        lease_expires_at=datetime(2026, 11, 7, 14, 0, 0, tzinfo=timezone.utc),
        updated_at=NOW_B,
        last_reason="launched",
    )
    assert ent(before) == pending()


@pytest.mark.parametrize("operation_id", ["op-9", None])
def test_t6_unknown_outcome_keeps_the_operation_id_if_any__fr014(operation_id):
    before = doc_in("pending")
    after = record.mark_unknown(before, 7, operation_id, NOW_B)
    assert ent(after) == pending(
        state="unknown",
        operation_id=operation_id,
        updated_at=NOW_B,
        last_reason="launch_unknown",
    )
    assert after.entries[7].lease_expires_at is None
    assert ent(before) == pending()


def test_t7_spawn_error_abandons_a_pending_entry__fr013_fr014():
    before = doc_in("pending")
    after = record.mark_spawn_error(before, 7, NOW_B)
    assert ent(after) == pending(
        state="abandoned", updated_at=NOW_B, last_reason="spawn_error"
    )
    assert ent(before) == pending()


def test_t8_sweep_abandons_a_pending_entry_as_pending_orphan__nfr005():
    before = doc_of(
        entry_raw(7),
        failed_entry_raw(8),
        STATE_RAWS["launched"](10),  # lease ends at 14:00, still running at 13:00
    )
    after, changed = record.sweep(before, NOW_B)
    orphan = pending(state="abandoned", updated_at=NOW_B, last_reason="pending_orphan")
    assert ent(after) == orphan
    assert changed == [orphan]
    assert after.entries[8] == before.entries[8]
    assert after.entries[10] == before.entries[10]
    assert ent(before) == pending()


def test_t9_sweep_abandons_an_expired_launched_entry_as_claim_not_observed__nfr005():
    before = doc_in("launched")
    after, changed = record.sweep(
        before, datetime(2026, 11, 7, 14, 30, tzinfo=timezone.utc)
    )
    expired = pending(
        state="abandoned",
        operation_id="op-1",
        lease_expires_at=datetime(2026, 11, 7, 14, 0, 0, tzinfo=timezone.utc),
        updated_at=datetime(2026, 11, 7, 14, 30, 0, tzinfo=timezone.utc),
        last_reason="claim_not_observed",
    )
    assert ent(after) == expired
    assert changed == [expired]
    assert ent(before).state == "launched"


# ----------------------------------------------------------------- T-10 to T-13

LEASE_END_AT = datetime(2026, 11, 7, 14, 0, 0, tzinfo=timezone.utc)


@pytest.mark.parametrize(
    "state, kept",
    [
        ("launched", {"operation_id": "op-1", "lease_expires_at": LEASE_END_AT}),
        ("unknown", {}),
        ("abandoned", {}),
    ],
)
def test_t10_claim_marker_after_a_launch_moves_the_entry_to_claimed__fr009(state, kept):
    before = doc_in(state)
    after = record.mark_claimed(before, 7, NOW_B)
    assert ent(after) == pending(
        state="claimed", updated_at=NOW_B, last_reason="claimed", **kept
    )
    assert after.entries[7].launches == 1
    assert ent(before).state == state


def test_t10_claim_with_a_current_approval_replaces_only_the_approval_fields__fr009():
    after = record.mark_claimed(doc_in("launched"), 7, NOW_B, approval=APPROVAL)
    assert ent(after) == pending(
        state="claimed",
        operation_id="op-1",
        lease_expires_at=LEASE_END_AT,
        approver_id=44,
        approval_event_id=55,
        approved_at=datetime(2026, 11, 7, 12, 30, 0, tzinfo=timezone.utc),
        updated_at=NOW_B,
        last_reason="claimed",
    )


def test_t10_claim_on_an_attempts_exhausted_tombstone_uses_the_approval__fr009():
    before = doc_of(tombstone_raw(7))
    assert ent(before).pending_at is None
    after = record.mark_claimed(before, 7, NOW_B, approval=APPROVAL)
    assert ent(after) == blank(
        state="claimed",
        attempts=3,
        launches=0,
        approver_id=44,
        approval_event_id=55,
        approved_at=datetime(2026, 11, 7, 12, 30, 0, tzinfo=timezone.utc),
        updated_at=NOW_B,
        last_reason="claimed",
    )
    bare = record.mark_claimed(before, 7, NOW_B)
    assert ent(bare) == blank(
        state="claimed", attempts=3, updated_at=NOW_B, last_reason="claimed"
    )


def test_t11_claim_marker_with_no_entry_makes_claimed_without_a_launch__fr009():
    before = doc_of()
    after = record.mark_claimed(before, 7, NOW_B, approval=APPROVAL)
    assert ent(after) == blank(
        state="claimed",
        attempts=0,
        launches=0,
        approver_id=44,
        approval_event_id=55,
        approved_at=datetime(2026, 11, 7, 12, 30, 0, tzinfo=timezone.utc),
        consumed_at=None,
        pending_at=None,
        created_at=NOW_B,
        updated_at=NOW_B,
        last_reason="claimed",
    )
    assert before.entries == {}
    assert ent(record.mark_claimed(before, 7, NOW_B)).approver_id is None


def test_t12_claim_marker_on_a_failed_entry_keeps_zero_launches__fr009():
    before = doc_in("failed")
    after = record.mark_claimed(before, 7, NOW_B)
    assert ent(after) == blank(
        state="claimed",
        attempts=1,
        launches=0,
        consumed_at=None,
        pending_at=None,
        created_at=FIXED_NOW,
        updated_at=NOW_B,
        last_reason="claimed",
    )
    assert ent(before).state == "failed"


# NOW_B is 13:00, so the first time is exactly 24 h old and is pruned.
LOG_IN = ("2026-11-06T13:00:00Z", "2026-11-06T13:00:01Z", "2026-11-07T00:00:00Z")
LOG_KEPT = (
    datetime(2026, 11, 6, 13, 0, 1, tzinfo=timezone.utc),
    datetime(2026, 11, 7, 0, 0, 0, tzinfo=timezone.utc),
)


@pytest.mark.parametrize(
    "raw, log_after, count",
    [
        (STATE_RAWS["abandoned"], (*LOG_KEPT, FIXED_NOW), 3),
        (STATE_RAWS["unknown"], (*LOG_KEPT, FIXED_NOW), 3),
        (tombstone_raw, LOG_KEPT, 2),
    ],
    ids=["abandoned", "unknown", "tombstone-no-consumed_at"],
)
def test_t13_reset_removes_the_entry_and_keeps_its_consumed_at__fr016_fr023_fr024(
    raw, log_after, count
):
    before = doc_of(raw(7), failed_entry_raw(8), consumed_log=LOG_IN)
    after = record.reset_entry(before, 7, NOW_B)
    assert sorted(after.entries) == [8]
    assert after.entries[8] == before.entries[8]
    assert after.consumed_log == log_after  # the 24 h old time is pruned
    assert record.day_cap_count(before, NOW_B) == count
    assert record.day_cap_count(after, NOW_B) == count  # the cap holds through reset
    assert sorted(before.entries) == [7, 8]


# ------------------------------------------- every other (state, trigger) pair

STATES = (None, "pending", "launched", "unknown", "failed", "abandoned", "claimed")

ACTIONS = {
    "fail": lambda doc: record.fail(doc, 7, "prompt_invalid", NOW_B),
    "pending": lambda doc: record.mark_pending(doc, 7, CTX, NOW_B),
    "launched": lambda doc: record.mark_launched(doc, 7, "op-1", NOW_B),
    "launch_unknown": lambda doc: record.mark_unknown(doc, 7, None, NOW_B),
    "spawn_error": lambda doc: record.mark_spawn_error(doc, 7, NOW_B),
    "claimed": lambda doc: record.mark_claimed(doc, 7, NOW_B),
    "reset": lambda doc: record.reset_entry(doc, 7, NOW_B),
    "backoff": lambda doc: record.backoff_elapsed(doc.entries[7], NOW_B),
}

# The allowed rows of design section 7.4, written out by hand. The ``failed`` to
# ``failed`` retry is the ``fail`` row of "failed"; ``backoff`` needs an entry.
ALLOWED = {
    "fail": {None, "failed"},
    "pending": {None, "failed"},
    "launched": {"pending"},
    "launch_unknown": {"pending"},
    "spawn_error": {"pending"},
    "claimed": {None, "failed", "launched", "unknown", "abandoned"},
    "reset": {"abandoned", "unknown"},
    "backoff": {"failed"},
}


def pairs(allowed: bool, *, skip: tuple[str, ...] = ()) -> list:
    return [
        pytest.param(state, trigger, id=f"{state}-{trigger}")
        for trigger, ok in ALLOWED.items()
        for state in STATES
        if (state in ok) is allowed
        and trigger not in skip
        and not (trigger == "backoff" and state is None)
    ]


def test_the_pair_table_covers_every_state_and_trigger_once():
    assert len(pairs(True)) == 15
    assert len(pairs(False)) == 40  # 8 triggers x 7 states, minus backoff of no entry


@pytest.mark.parametrize("state, trigger", pairs(False))
def test_every_other_state_trigger_pair_raises_transition_error__nfr005(state, trigger):
    doc = doc_in(state)
    before = copy.deepcopy(doc)
    with pytest.raises(TransitionError):
        ACTIONS[trigger](doc)
    assert doc == before


@pytest.mark.parametrize("state, trigger", pairs(True))
def test_every_allowed_pair_runs_without_transition_error__nfr005(state, trigger):
    result = ACTIONS[trigger](doc_in(state))
    if trigger == "backoff":
        assert result is True  # failed at 12:00 with attempts 1, checked at 13:00
        return
    assert isinstance(result, StoreDoc)
    check_reasons(result)


@pytest.mark.parametrize("state", STATES)
@pytest.mark.parametrize("reason", ["spawn_error", "claimed", ""])
def test_fail_with_a_reason_that_is_not_a_failure_trigger_raises__nfr005(state, reason):
    doc = doc_in(state)
    with pytest.raises(TransitionError):
        record.fail(doc, 7, reason, NOW_B)


# --------------------------------------------------------------- half-open windows


@pytest.mark.parametrize(
    "now, abandoned",
    [
        (datetime(2026, 11, 7, 13, 59, 59, tzinfo=timezone.utc), False),
        (datetime(2026, 11, 7, 14, 0, 0, tzinfo=timezone.utc), True),
        (datetime(2026, 11, 7, 14, 0, 1, tzinfo=timezone.utc), True),
    ],
    ids=["one-second-before", "exactly-at-lease-end", "one-second-after"],
)
def test_lease_is_expired_at_exactly_lease_expires_at_not_one_second_before__nfr005(
    now, abandoned
):
    after, changed = record.sweep(doc_in("launched"), now)
    assert ent(after).state == ("abandoned" if abandoned else "launched")
    assert len(changed) == (1 if abandoned else 0)
    if abandoned:
        assert ent(after).last_reason == "claim_not_observed"


@pytest.mark.parametrize(
    "now, eligible",
    [
        (datetime(2026, 11, 7, 12, 9, 59, tzinfo=timezone.utc), False),
        (datetime(2026, 11, 7, 12, 10, 0, tzinfo=timezone.utc), True),
        (datetime(2026, 11, 7, 12, 10, 1, tzinfo=timezone.utc), True),
    ],
    ids=["one-second-before", "exactly-ten-minutes", "one-second-after"],
)
def test_t2_backoff_is_elapsed_at_exactly_updated_at_plus_ten_minutes__nfr005(
    now, eligible
):
    entry = ent(doc_in("failed"))  # attempts 1, updated_at 12:00:00
    assert record.backoff_elapsed(entry, now) is eligible


def consumed(n: int, when: str) -> dict:
    """A ``pending`` entry for issue ``n`` consumed (and pending) at ``when``."""
    return entry_raw(n, consumed_at=when, pending_at=when)


def test_ac10_consumed_at_exactly_24h_old_no_longer_counts__fr016_fr023():
    doc = doc_of(consumed(7, "2026-11-06T13:00:00Z"))  # NOW_B minus exactly 24 h
    assert record.day_cap_count(doc, NOW_B) == 0
    one_second_earlier = NOW_B - timedelta(seconds=1)
    assert record.day_cap_count(doc, one_second_earlier) == 1


def test_ac10_consumed_log_time_exactly_24h_old_no_longer_counts__fr016_fr023():
    assert (
        record.day_cap_count(doc_of(consumed_log=("2026-11-06T13:00:00Z",)), NOW_B) == 0
    )
    assert (
        record.day_cap_count(doc_of(consumed_log=("2026-11-06T13:00:01Z",)), NOW_B) == 1
    )


def test_ac10_day_cap_window_is_open_at_now_minus_24h_and_closed_at_now__fr016_fr023():
    doc = doc_of(
        consumed(7, "2026-11-06T13:00:00Z"),  # exactly 24 h: out
        consumed(8, "2026-11-06T13:00:01Z"),  # 23 h 59 min 59 s: in
        consumed(9, "2026-11-07T13:00:00Z"),  # exactly now: in
        consumed(10, "2026-11-07T13:00:01Z"),  # after now: out
        failed_entry_raw(11),  # no consumed_at: out
        consumed_log=("2026-11-06T13:00:00Z", "2026-11-06T13:00:01Z"),
    )
    assert record.day_cap_count(doc, NOW_B) == 3


# ---------------------------------------------------------- purity and reasons


@pytest.mark.parametrize("state, trigger", pairs(True, skip=("backoff",)))
def test_every_transition_returns_a_new_document_and_leaves_its_input__nfr005(
    state, trigger
):
    doc = doc_in(state)
    before = copy.deepcopy(doc)
    after = ACTIONS[trigger](doc)
    assert isinstance(after, StoreDoc)
    assert after is not doc
    assert after.entries is not doc.entries
    assert doc == before
    assert after != before
    check_reasons(after)


def test_sweep_returns_a_new_document_and_leaves_its_input__nfr005():
    doc = doc_of(entry_raw(7), STATE_RAWS["launched"](8))
    before = copy.deepcopy(doc)
    after, changed = record.sweep(
        doc, datetime(2026, 11, 7, 14, 0, tzinfo=timezone.utc)
    )
    assert after is not doc
    assert doc == before
    assert [e.issue for e in changed] == [7, 8]
    assert [e.last_reason for e in changed] == ["pending_orphan", "claim_not_observed"]
    assert doc.entries[7].state == "pending"
    assert doc.entries[8].state == "launched"


LITERAL_REASONS = [
    "prompt_invalid",
    "revalidation_transient",
    "attempts_exhausted",
    "launched",
    "launch_unknown",
    "spawn_error",
    "pending_orphan",
    "claim_not_observed",
    "claimed",
]


@pytest.mark.parametrize("reason", LITERAL_REASONS)
def test_df42_every_reason_these_tests_write_is_in_the_audit_table(reason):
    assert reason in REASONS


def test_df42_every_reason_the_transitions_write_is_in_the_audit_table():
    written = set()
    for state, trigger in [p.values[:2] for p in pairs(True, skip=("backoff",))]:
        after = ACTIONS[trigger](doc_in(state))
        written.update(e.last_reason for e in after.entries.values())  # reset: none
    after, _ = record.sweep(
        doc_of(entry_raw(7), STATE_RAWS["launched"](8)),
        datetime(2026, 11, 7, 14, 0, tzinfo=timezone.utc),
    )
    written.update(e.last_reason for e in after.entries.values())
    written.discard(None)  # mark_pending writes no reason: the table has none for it
    assert written
    assert written <= REASONS
    assert written <= set(LITERAL_REASONS)


# ============================================================================
# Part C: day cap, sweep, init-state, resets and the dry-run file (design
# sections 7.1, 7.2 and 7.5; decisions DF-03, DF-04 and DF-44). Expected values
# are literals; the real umask is set (and restored) where a test needs one,
# because a patched ``os.umask`` would not change what the kernel applies.
# ============================================================================

WINDOW_STATES = ("pending", "launched", "unknown", "abandoned", "claimed")
WINDOW_TIMES = (
    "2026-11-06T13:00:01Z",  # 23 h 59 min 59 s before NOW_B
    "2026-11-06T18:00:00Z",
    "2026-11-07T00:00:00Z",
    "2026-11-07T06:00:00Z",
    "2026-11-07T12:59:59Z",
)
LOG_TIME = "2026-11-07T01:00:00Z"


def six_in_window() -> StoreDoc:
    """Issues 7-11 (one per launched state) plus one ``consumed_log`` time: six.

    Issue 20 is ``failed`` with no ``consumed_at``, so it never counts.
    """
    raws = [
        {**STATE_RAWS[state](n), "consumed_at": when}
        for n, (state, when) in enumerate(zip(WINDOW_STATES, WINDOW_TIMES), start=7)
    ]
    raws.append(failed_entry_raw(20))
    return doc_of(*raws, consumed_log=(LOG_TIME,))


def at(hour: int, minute: int = 0, second: int = 0, day: int = 7) -> datetime:
    return datetime(2026, 11, day, hour, minute, second, tzinfo=timezone.utc)


def snapshot(path) -> tuple[bytes, int]:
    """A file's bytes and mtime, to show that nothing wrote it."""
    return path.read_bytes(), path.stat().st_mtime_ns


# ------------------------------------------------------------------- day cap


def test_ac10_day_cap_counts_every_state_plus_consumed_log__fr024():
    doc = six_in_window()
    assert sorted(e.state for e in doc.entries.values()) == sorted(
        [*WINDOW_STATES, "failed"]
    )
    assert record.day_cap_count(doc, NOW_B) == 6  # at 6 the next issue skips day_cap
    after_seventh = record.mark_pending(doc, 30, CTX, NOW_B)
    assert record.day_cap_count(after_seventh, NOW_B) == 7
    assert record.day_cap_count(doc, NOW_B) == 6  # the input document is unchanged


def test_ac10_day_cap_count_drops_the_oldest_time_when_it_turns_24h_old__fr024():
    doc = six_in_window()
    assert record.day_cap_count(doc, at(13, 0, 0)) == 6
    assert record.day_cap_count(doc, at(13, 0, 1)) == 5  # 11-06 13:00:01 is now 24 h
    # 18:00 on the 6th and 00:00 on the 7th are gone; log 01:00, 06:00 and 12:59:59 stay.
    assert record.day_cap_count(doc, at(0, 0, 0, day=8)) == 3


def test_ac10_day_cap_of_an_empty_or_failed_only_store_is_zero__fr024():
    assert record.day_cap_count(doc_of(), NOW_B) == 0
    assert record.day_cap_count(doc_of(failed_entry_raw(7)), NOW_B) == 0


@pytest.mark.parametrize("victim, state", [(9, "unknown"), (10, "abandoned")])
def test_ac10_reset_keeps_the_day_cap_count_through_consumed_log__fr024_fr026(
    victim, state
):
    before = six_in_window()
    assert before.entries[victim].state == state
    moved = before.entries[victim].consumed_at
    after = record.reset_entry(before, victim, NOW_B)
    assert victim not in after.entries
    assert sorted(after.entries) == [n for n in sorted(before.entries) if n != victim]
    assert after.consumed_log == (at(1), moved)  # the old log time, then the moved one
    assert moved in after.consumed_log
    assert record.day_cap_count(before, NOW_B) == 6
    assert record.day_cap_count(after, NOW_B) == 6
    assert victim in before.entries and before.consumed_log == (at(1),)


def test_ac10_reset_then_a_new_issue_still_hits_the_cap__fr024_fr026():
    after = record.reset_entry(six_in_window(), 10, NOW_B)
    assert record.day_cap_count(record.mark_pending(after, 30, CTX, NOW_B), NOW_B) == 7


def test_ac10_consumed_log_is_pruned_after_24h_in_reset__fr024_fr026():
    before = six_in_window()
    # 06:00 on the 7th is the victim's consumed_at; a day later both it and the
    # 01:00 log time are at least 24 h old, so neither survives the reset.
    later = at(6, day=8)
    after = record.reset_entry(before, 10, later)
    assert after.consumed_log == ()
    just_before = at(5, 59, 59, day=8)
    kept = record.reset_entry(before, 10, just_before)
    assert kept.consumed_log == (at(6),)  # 01:00 is pruned, 06:00 is 23 h 59 min old
    assert before.consumed_log == (at(1),)


def test_ac10_prune_consumed_log_drops_t_at_or_before_now_minus_24h__fr024():
    doc = doc_of(
        consumed_log=(
            "2026-11-06T12:59:59Z",
            "2026-11-06T13:00:00Z",  # exactly NOW_B minus 24 h: dropped
            "2026-11-06T13:00:01Z",
            "2026-11-07T13:00:00Z",
        )
    )
    pruned = record.prune_consumed_log(doc, NOW_B)
    assert pruned.consumed_log == (at(13, 0, 1, day=6), at(13))
    assert doc.consumed_log[0] == at(12, 59, 59, day=6)  # input untouched
    assert pruned.entries == doc.entries


# -------------------------------------------------------------------- resets


@pytest.mark.parametrize("state", ["pending", "launched", "failed", "claimed", None])
def test_ac17_reset_entry_refuses_states_it_may_not_remove__fr026(state):
    doc = doc_in(state)  # None: no entry for issue 7
    before = copy.deepcopy(doc)
    with pytest.raises(TransitionError) as info:
        record.reset_entry(doc, 7, NOW_B)
    assert "issue 7" in str(info.value)
    assert doc == before


def test_ac17_reset_entry_of_an_absent_issue_leaves_other_entries_alone__fr026():
    doc = doc_of(STATE_RAWS["abandoned"](8))
    with pytest.raises(TransitionError):
        record.reset_entry(doc, 7, NOW_B)
    assert sorted(doc.entries) == [8]


def test_ac18_reset_rate_limit_clears_next_permitted_at_only__fr028():
    raw = store_raw(next_permitted_at="2026-11-07T13:30:00Z")
    doc = validate(raw)
    assert doc.next_permitted_at == at(13, 30)
    cleared = record.reset_rate_limit(doc)
    assert cleared.next_permitted_at is None
    assert cleared == validate(store_raw())  # nothing else differs
    assert doc.next_permitted_at == at(13, 30)  # the input is not mutated
    assert record.reset_rate_limit(cleared) == cleared  # clearing twice is a no-op


# --------------------------------------------------------------------- sweep


def test_ac13_sweep_returns_the_change_list_and_writes_nothing__fr019(
    tmp_state, monkeypatch
):
    put(
        tmp_state,
        store_raw(
            considered={},
            entries={
                "7": entry_raw(7),
                "8": STATE_RAWS["launched"](8),  # lease ended 14:00
                "9": entry_raw(
                    9,
                    state="launched",
                    operation_id="op-2",
                    lease_expires_at="2026-11-07T15:00:00Z",
                    last_reason="launched",
                ),
                "10": entry_raw(
                    10,
                    state="unknown",
                    lease_expires_at="2026-11-07T12:30:00Z",
                    last_reason="launch_unknown",
                ),
                "11": STATE_RAWS["abandoned"](11),
                "12": STATE_RAWS["claimed"](12),
                "13": failed_entry_raw(13),
            },
        ),
    )
    path = tmp_state.state_dir / "dispatch.json"
    files = sorted(p.name for p in tmp_state.state_dir.iterdir())
    stored = snapshot(path)

    def no_save(self, doc):
        raise AssertionError("sweep must not save")

    monkeypatch.setattr(FileStore, "save", no_save)
    before = tmp_state.load()
    when = at(14, 30)
    after, changed = record.sweep(before, when)

    assert [e.issue for e in changed] == [7, 8]
    assert changed[0] == pending(
        state="abandoned", updated_at=when, last_reason="pending_orphan"
    )
    assert changed[1] == pending(
        issue=8,
        state="abandoned",
        operation_id="op-1",
        lease_expires_at=LEASE_END_AT,
        updated_at=when,
        last_reason="claim_not_observed",
    )
    assert {n: e.state for n, e in after.entries.items()} == {
        7: "abandoned",
        8: "abandoned",
        9: "launched",  # lease runs until 15:00
        10: "unknown",  # an unknown entry never moves on the lease
        11: "abandoned",
        12: "claimed",
        13: "failed",
    }
    assert after.entries[10] == before.entries[10]
    assert after.entries[11] == before.entries[11]
    assert before.entries[7].state == "pending"  # the input document is unchanged
    assert snapshot(path) == stored
    assert sorted(p.name for p in tmp_state.state_dir.iterdir()) == files


def test_ac13_sweep_of_a_store_with_nothing_to_abandon_changes_nothing__fr019():
    doc = doc_of(
        STATE_RAWS["unknown"](7),
        STATE_RAWS["claimed"](8),
        STATE_RAWS["abandoned"](9),
        failed_entry_raw(10),
    )
    after, changed = record.sweep(doc, at(23, 0, 0, day=9))
    assert changed == []
    assert after == doc


def test_sweep_abandons_a_launched_entry_with_no_lease_at_once__nfr005():
    doc = doc_of(entry_raw(7, state="launched", operation_id="op-1", last_reason=None))
    after, changed = record.sweep(doc, FIXED_NOW)
    assert [e.last_reason for e in changed] == ["claim_not_observed"]
    assert ent(after).state == "abandoned"


# ---------------------------------------------------------------- init-state


def init_under(umask: int, state_dir):
    old = os.umask(umask)
    try:
        return init_state(state_dir, FIXED_NOW)
    finally:
        os.umask(old)


@pytest.mark.parametrize("mask", [0o022, 0o077, 0o000])
def test_ac17_init_state_modes_hold_under_any_umask__fr026(tmp_path, mask):
    store = init_under(mask, tmp_path / "outer" / "state")
    state_dir = store.state_dir
    assert stat.S_IMODE(state_dir.stat().st_mode) == 0o700
    assert stat.S_IMODE((state_dir / "dispatch.json").stat().st_mode) == 0o600
    assert stat.S_IMODE((state_dir / "lock").stat().st_mode) == 0o600
    assert sorted(p.name for p in state_dir.iterdir()) == ["dispatch.json", "lock"]


def test_ac17_init_state_chmods_an_existing_wider_directory__fr026(tmp_path):
    state_dir = tmp_path / "state"
    state_dir.mkdir(mode=0o755)
    os.chmod(state_dir, 0o755)
    init_under(0o022, state_dir)
    assert stat.S_IMODE(state_dir.stat().st_mode) == 0o700


def test_ac17_init_state_writes_an_empty_store_stamped_with_now__fr026(tmp_path):
    store = init_state(tmp_path / "state", FIXED_NOW)
    doc = store.load()
    assert doc.created_at == FIXED_NOW
    assert doc.schema_version == 1
    assert doc.next_permitted_at is None
    assert doc.last_completed_cycle_at is None
    assert (dict(doc.considered), doc.consumed_log, dict(doc.entries)) == ({}, (), {})
    assert json.loads((store.state_dir / "dispatch.json").read_bytes()) == {
        "schema_version": 1,
        "created_at": T0,
        "next_permitted_at": None,
        "last_completed_cycle_at": None,
        "considered": {},
        "consumed_log": [],
        "entries": {},
    }
    assert (store.state_dir / "lock").read_bytes() == b""
    later = init_state(tmp_path / "later", NOW_B)
    assert later.load().created_at == NOW_B


def test_ac17_init_state_creates_the_lock_exclusively_and_nofollow__fr026(
    tmp_path, monkeypatch
):
    real = os.open
    seen: list[tuple[int, int]] = []

    def spy(path, flags, mode=0o777, **kwargs):
        if os.fspath(path).endswith("/lock"):
            seen.append((flags, mode))
        return real(path, flags, mode, **kwargs)

    monkeypatch.setattr(os, "open", spy)
    init_state(tmp_path / "state", FIXED_NOW)
    assert len(seen) == 1
    flags, mode = seen[0]
    need = os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW
    assert flags & need == need
    assert mode == 0o600


def test_ac17_init_state_refuses_an_existing_store_and_changes_nothing__fr026(
    tmp_path,
):
    store = init_state(tmp_path / "state", FIXED_NOW)
    state_dir = store.state_dir
    store.save(validate(store_raw()))  # a non-empty store
    watched = [state_dir / "dispatch.json", state_dir / "lock"]
    before = [snapshot(p) for p in watched]
    mode = stat.S_IMODE(state_dir.stat().st_mode)
    with pytest.raises(record.StateExists):
        init_state(state_dir, NOW_B)
    with pytest.raises(record.StateExists):
        init_state(state_dir, NOW_B)
    assert [snapshot(p) for p in watched] == before
    assert sorted(p.name for p in state_dir.iterdir()) == ["dispatch.json", "lock"]
    assert stat.S_IMODE(state_dir.stat().st_mode) == mode
    assert store.load().created_at == at(10)


@pytest.mark.parametrize("keep", ["dispatch.json", "lock"])
def test_ac17_init_state_refuses_when_either_file_exists__fr026(tmp_path, keep):
    state_dir = init_state(tmp_path / "state", FIXED_NOW).state_dir
    (state_dir / ("lock" if keep == "dispatch.json" else "dispatch.json")).unlink()
    before = snapshot(state_dir / keep)
    with pytest.raises(record.StateExists):
        init_state(state_dir, NOW_B)
    assert [p.name for p in state_dir.iterdir()] == [keep]
    assert snapshot(state_dir / keep) == before


def test_ac17_init_state_exclusive_create_catches_a_lock_made_in_a_race__fr026(
    tmp_path, monkeypatch
):
    state_dir = init_state(tmp_path / "state", FIXED_NOW).state_dir
    watched = [state_dir / "dispatch.json", state_dir / "lock"]
    before = [snapshot(p) for p in watched]
    monkeypatch.setattr(os.path, "lexists", lambda path: False)  # the pre-check misses
    with pytest.raises(record.StateExists):
        init_state(state_dir, NOW_B)
    assert [snapshot(p) for p in watched] == before


def test_ac17_init_state_on_a_read_only_parent_is_state_dir_unwritable__fr026(
    tmp_path,
):
    parent = tmp_path / "readonly"
    parent.mkdir()
    os.chmod(parent, 0o500)
    try:
        with pytest.raises(StoreError) as info:
            init_state(parent / "state", FIXED_NOW)
        assert info.value.reason == "state_dir_unwritable"
        assert list(parent.iterdir()) == []
    finally:
        os.chmod(parent, 0o700)


def test_ac17_init_state_under_a_plain_file_is_state_dir_unwritable__fr026(tmp_path):
    plain = tmp_path / "plain"
    plain.write_bytes(b"x")
    with pytest.raises(StoreError) as info:
        init_state(plain / "state", FIXED_NOW)
    assert info.value.reason == "state_dir_unwritable"
    assert plain.read_bytes() == b"x"


def test_ac17_init_state_removes_the_lock_it_made_when_the_store_cannot_save__fr026(
    tmp_path, monkeypatch
):
    def boom(self, doc):
        raise OSError("disk full")

    monkeypatch.setattr(FileStore, "save", boom)
    state_dir = tmp_path / "state"
    with pytest.raises(StoreError) as info:
        init_state(state_dir, FIXED_NOW)
    assert info.value.reason == "state_dir_unwritable"
    assert not (state_dir / "lock").exists()
    assert not (state_dir / "dispatch.json").exists()


# ------------------------------------------------------------ dry-run shadow

SHADOW = {
    "schema_version": 1,
    "considered": {"9": T0, "10": "2026-11-07T13:00:00Z"},
    "shadow_launches": [T0],
}


def test_ac13_load_dry_run_missing_file_is_an_empty_shadow_not_replaced__fr019(
    tmp_state,
):
    shadow, replaced = record.load_dry_run(tmp_state.state_dir)
    assert replaced is False
    assert dict(shadow.considered) == {}
    assert shadow.shadow_launches == ()
    assert not (tmp_state.state_dir / "dry-run.json").exists()  # load never writes


@pytest.mark.parametrize(
    "data",
    [
        b"",
        b"{not json",
        b"\xff\xfe binary",
        b"[]",
        json.dumps({"schema_version": 1}).encode(),
        json.dumps({**SHADOW, "extra": 1}).encode(),
        json.dumps({**SHADOW, "schema_version": 2}).encode(),
        json.dumps({**SHADOW, "schema_version": True}).encode(),
        json.dumps({**SHADOW, "considered": []}).encode(),
        json.dumps({**SHADOW, "considered": {"0": T0}}).encode(),
        json.dumps({**SHADOW, "considered": {"9": "2026-11-07T12:00:00"}}).encode(),
        json.dumps({**SHADOW, "shadow_launches": {}}).encode(),
        json.dumps({**SHADOW, "shadow_launches": [5]}).encode(),
    ],
    ids=[
        "empty",
        "garbage",
        "binary",
        "list",
        "missing-keys",
        "extra-key",
        "version-two",
        "version-bool",
        "considered-list",
        "issue-zero",
        "naive-time",
        "launches-dict",
        "launch-int",
    ],
)
def test_ac13_load_dry_run_unparseable_file_is_an_empty_shadow_and_replaced__fr019(
    tmp_state, data
):
    path = tmp_state.state_dir / "dry-run.json"
    path.write_bytes(data)
    shadow, replaced = record.load_dry_run(tmp_state.state_dir)
    assert replaced is True
    assert dict(shadow.considered) == {}
    assert shadow.shadow_launches == ()
    assert path.read_bytes() == data  # load itself never rewrites the file


def test_ac13_load_dry_run_unreadable_path_is_replaced__fr019(tmp_state):
    (tmp_state.state_dir / "dry-run.json").mkdir()
    shadow, replaced = record.load_dry_run(tmp_state.state_dir)
    assert replaced is True
    assert shadow == record.DryRunDoc(considered={}, shadow_launches=())


def test_ac13_load_dry_run_reads_a_valid_shadow__fr019(tmp_state):
    (tmp_state.state_dir / "dry-run.json").write_text(json.dumps(SHADOW))
    shadow, replaced = record.load_dry_run(tmp_state.state_dir)
    assert replaced is False
    assert dict(shadow.considered) == {9: FIXED_NOW, 10: NOW_B}
    assert shadow.shadow_launches == (FIXED_NOW,)


def test_ac13_save_dry_run_writes_sorted_ascii_json_at_mode_0600__fr019(tmp_state):
    doc = record.DryRunDoc(
        considered={9: FIXED_NOW, 10: NOW_B}, shadow_launches=(NOW_B,)
    )
    old = os.umask(0)
    try:
        record.save_dry_run(tmp_state.state_dir, doc)
    finally:
        os.umask(old)
    path = tmp_state.state_dir / "dry-run.json"
    assert stat.S_IMODE(path.stat().st_mode) == 0o600
    expected = {
        "schema_version": 1,
        "considered": {"10": "2026-11-07T13:00:00Z", "9": T0},
        "shadow_launches": ["2026-11-07T13:00:00Z"],
    }
    data = path.read_bytes()
    assert data == json.dumps(expected, sort_keys=True, indent=2).encode() + b"\n"
    assert record.load_dry_run(tmp_state.state_dir) == (doc, False)


def test_ac13_save_dry_run_forces_0600_over_a_wider_existing_file__fr019(
    tmp_state, monkeypatch
):
    """The writer leaves a 0666 file, so only ``save_dry_run``'s own chmod gives 0600.

    ``mkstemp`` already creates 0600, so a plain wider-file case passes even with the
    chmod deleted; this twin of ``test_save_chmod_is_a_guard_...`` makes the writer
    leave the wide mode.
    """
    path = tmp_state.state_dir / "dry-run.json"
    path.write_text("old")
    os.chmod(path, 0o666)
    real = atomic.write_prepared_bytes

    def wide(target, data):
        written = real(target, data)
        os.chmod(target, 0o666)
        return written

    monkeypatch.setattr(atomic, "write_prepared_bytes", wide)
    record.save_dry_run(tmp_state.state_dir, record.DryRunDoc({}, ()))
    assert stat.S_IMODE(path.stat().st_mode) == 0o600
    assert record.load_dry_run(tmp_state.state_dir) == (record.DryRunDoc({}, ()), False)


def test_ac13_save_dry_run_fsyncs_the_state_directory_last__fr019(
    tmp_state, monkeypatch
):
    """The directory fsync after the replace is observed, as for ``FileStore.save``."""
    real = os.fsync
    seen: list[tuple[bool, int]] = []

    def counting(fd):
        st = os.fstat(fd)
        seen.append((stat.S_ISDIR(st.st_mode), st.st_ino))
        real(fd)

    monkeypatch.setattr(os, "fsync", counting)
    record.save_dry_run(tmp_state.state_dir, record.DryRunDoc({}, ()))
    dir_ino = tmp_state.state_dir.stat().st_ino
    assert seen[-1] == (True, dir_ino)  # after the file's own fsync
    assert any(not is_dir for is_dir, _ in seen)


def test_ac13_load_dry_run_deep_nesting_is_an_empty_shadow_and_replaced__fr019(
    tmp_state,
):
    """``RecursionError`` from ``json.loads`` is a replaced shadow, never a raise (B-12)."""
    path = tmp_state.state_dir / "dry-run.json"
    data = b"[" * 100_000 + b"]" * 100_000
    path.write_bytes(data)
    shadow, replaced = record.load_dry_run(tmp_state.state_dir)
    assert replaced is True
    assert shadow == record.DryRunDoc(considered={}, shadow_launches=())
    assert path.read_bytes() == data


@pytest.mark.parametrize("digits", [10, 4301, 20000])
def test_ac13_load_dry_run_overlong_digit_key_is_replaced__fr019(tmp_state, digits):
    """A 4301+ digit key made ``int(key)`` raise ``ValueError`` out of the loader (B-12)."""
    path = tmp_state.state_dir / "dry-run.json"
    path.write_text(json.dumps({**SHADOW, "considered": {"1" * digits: T0}}))
    shadow, replaced = record.load_dry_run(tmp_state.state_dir)
    assert replaced is True
    assert shadow == record.DryRunDoc(considered={}, shadow_launches=())


def test_ac13_a_replaced_shadow_is_fixed_by_the_next_save__fr019(tmp_state):
    (tmp_state.state_dir / "dry-run.json").write_bytes(b"{not json")
    shadow, replaced = record.load_dry_run(tmp_state.state_dir)
    assert replaced is True
    record.save_dry_run(tmp_state.state_dir, shadow)
    assert record.load_dry_run(tmp_state.state_dir) == (shadow, False)


def test_ac13_a_flow_using_only_the_dry_run_helpers_never_saves_dispatch_json__fr019(
    tmp_state, monkeypatch
):
    put(tmp_state, store_raw())
    path = tmp_state.state_dir / "dispatch.json"
    stored = snapshot(path)
    saves: list[StoreDoc] = []

    def no_save(self, doc):
        saves.append(doc)
        raise AssertionError("a dry-run flow must not save dispatch.json")

    monkeypatch.setattr(FileStore, "save", no_save)
    doc = tmp_state.load()
    swept, _changed = record.sweep(doc, NOW_B)  # reported, not written
    shadow, replaced = record.load_dry_run(tmp_state.state_dir)
    assert replaced is False
    count = record.day_cap_count(swept, NOW_B) + len(shadow.shadow_launches)
    record.save_dry_run(
        tmp_state.state_dir,
        record.DryRunDoc(
            considered={**shadow.considered, 9: NOW_B},
            shadow_launches=(*shadow.shadow_launches, NOW_B),
        ),
    )
    again, _ = record.load_dry_run(tmp_state.state_dir)
    # Entry 7 (consumed 12:00) counts; the log time is exactly 24 h old and does not.
    assert count == 1
    assert dict(again.considered) == {9: NOW_B}
    assert again.shadow_launches == (NOW_B,)
    assert saves == []
    assert snapshot(path) == stored
    assert sorted(p.name for p in tmp_state.state_dir.iterdir()) == [
        "dispatch.json",
        "dry-run.json",
        "lock",
    ]


# ============================================================================
# Part D: the input guards of the transitions and setters, the operation-id
# pattern at the record layer, and the round trip of every written document
# (Gate B findings B-4 to B-8, B-10, B-11). Every case checks that the input
# document is untouched and that nothing was created.
# ============================================================================

BAD_POSITIVE_IDS = [0, -1, True, False, "11", None, 1.5]
NAIVE = datetime(2026, 11, 7, 11, 0, 0)
UNSAFE_IDS = [
    "a;b",
    "$(id)",
    "op\n1",
    "a b",
    "a/b",
    "x" * 129,
    "x; rm -rf ~\n\x1b[31m",
    "",
]
NOT_STR_IDS = [None, 5, b"op", ["op"], True]


def refused(call, doc: StoreDoc) -> None:
    """``call`` raises ``ValueError`` and ``doc`` is exactly as it was."""
    before = copy.deepcopy(doc)
    with pytest.raises(ValueError):
        call()
    assert doc == before


@pytest.mark.parametrize("bad", BAD_POSITIVE_IDS)
@pytest.mark.parametrize(
    "field", ["approver_id", "approval_event_id", "launch_account_id"]
)
def test_mark_pending_refuses_a_non_positive_or_non_int_id__nfr001(field, bad):
    """Ids reach audit lines and the retry command, so only positive ints are kept."""
    doc = doc_of()
    ctx = dataclasses.replace(CTX, **{field: bad})
    refused(lambda: record.mark_pending(doc, 7, ctx, NOW_B), doc)
    assert doc.entries == {}


@pytest.mark.parametrize(
    "bad", [NAIVE, None, "2026-11-07T11:00:00Z", 5], ids=["naive", "none", "str", "int"]
)
def test_mark_pending_refuses_a_naive_or_non_datetime_approved_at__nfr001(bad):
    doc = doc_of()
    ctx = dataclasses.replace(CTX, approved_at=bad)
    refused(lambda: record.mark_pending(doc, 7, ctx, NOW_B), doc)
    assert doc.entries == {}


@pytest.mark.parametrize("bad", ["relative/path", "", None, 5, "./x"])
def test_mark_pending_refuses_a_non_absolute_launch_cwd__nfr001(bad):
    """``launch_cwd`` becomes the directory of the operator's retry command."""
    doc = doc_of()
    ctx = dataclasses.replace(CTX, launch_cwd=bad)
    refused(lambda: record.mark_pending(doc, 7, ctx, NOW_B), doc)
    assert doc.entries == {}


@pytest.mark.parametrize("bad", ["", None, 5, b"bot"])
def test_mark_pending_refuses_an_empty_or_non_str_launch_login__nfr001(bad):
    doc = doc_of()
    ctx = dataclasses.replace(CTX, launch_login=bad)
    refused(lambda: record.mark_pending(doc, 7, ctx, NOW_B), doc)
    assert doc.entries == {}


def test_mark_pending_guards_also_protect_a_failed_entry__nfr001():
    doc = doc_in("failed")
    ctx = dataclasses.replace(CTX, launch_account_id=0)
    refused(lambda: record.mark_pending(doc, 7, ctx, NOW_B), doc)
    assert doc.entries[7].state == "failed"


@pytest.mark.parametrize("bad", BAD_POSITIVE_IDS)
@pytest.mark.parametrize("field", ["approver_id", "approval_event_id"])
def test_mark_claimed_refuses_a_bad_approval_id__nfr001(field, bad):
    doc = doc_in("launched")
    approval = dataclasses.replace(APPROVAL, **{field: bad})
    refused(lambda: record.mark_claimed(doc, 7, NOW_B, approval=approval), doc)


@pytest.mark.parametrize(
    "bad", [NAIVE, None, "2026-11-07T12:30:00Z"], ids=["naive", "none", "str"]
)
def test_mark_claimed_refuses_a_naive_or_non_datetime_approved_at__nfr001(bad):
    doc = doc_in("launched")
    approval = dataclasses.replace(APPROVAL, approved_at=bad)
    refused(lambda: record.mark_claimed(doc, 7, NOW_B, approval=approval), doc)


@pytest.mark.parametrize("bad", ["", "a;b", "$(id)", "op\n1", "x" * 129, *NOT_STR_IDS])
def test_mark_launched_refuses_an_unsafe_or_non_str_operation_id__fr015(bad):
    """The id is printed in a shell command by ``status``; only the pattern is stored."""
    doc = doc_in("pending")
    refused(lambda: record.mark_launched(doc, 7, bad, NOW_B), doc)
    assert doc.entries[7].state == "pending"


@pytest.mark.parametrize("good", ["a", "A.b_c:d-9", "x" * 128])
def test_mark_launched_keeps_a_safe_operation_id_at_the_boundaries__fr015(good):
    after = record.mark_launched(doc_in("pending"), 7, good, NOW_B)
    assert ent(after).operation_id == good


@pytest.mark.parametrize("bad", [*UNSAFE_IDS, *NOT_STR_IDS[1:]])
def test_mark_unknown_refuses_an_unsafe_or_non_str_operation_id__fr015(bad):
    """Only None or a pattern-conforming str may be saved (a bad id once broke load)."""
    doc = doc_in("pending")
    refused(lambda: record.mark_unknown(doc, 7, bad, NOW_B), doc)
    assert doc.entries[7].state == "pending"


@pytest.mark.parametrize("good", [None, "a", "A.b_c:d-9", "x" * 128])
def test_mark_unknown_keeps_none_or_a_safe_operation_id__fr015(good):
    after = record.mark_unknown(doc_in("pending"), 7, good, NOW_B)
    assert ent(after).operation_id == good


@pytest.mark.parametrize("state, trigger", pairs(True, skip=("backoff",)))
def test_every_transition_output_is_a_document_load_accepts__fr019(state, trigger):
    """A saved document must always load again, so each result must validate."""
    after = ACTIONS[trigger](doc_in(state))
    assert validate(record._to_raw(after)) == after


def test_sweep_output_is_a_document_load_accepts__fr019():
    doc = doc_of(entry_raw(7), STATE_RAWS["launched"](8))
    after, _ = record.sweep(doc, datetime(2026, 11, 7, 14, 0, tzinfo=timezone.utc))
    assert validate(record._to_raw(after)) == after


def test_a_hostile_operation_id_never_reaches_a_saved_file__fr019(tmp_state):
    """No transition can write the id that ``load`` would then refuse for ever."""
    doc = tmp_state.load()
    pending_doc = record.mark_pending(doc, 7, CTX, NOW_B)
    for call in (
        lambda: record.mark_launched(pending_doc, 7, "x; rm -rf ~\n", NOW_B),
        lambda: record.mark_unknown(pending_doc, 7, 5, NOW_B),
    ):
        with pytest.raises(ValueError):
            call()
    tmp_state.save(record.mark_unknown(pending_doc, 7, "op-ok", NOW_B))
    assert tmp_state.load().entries[7].operation_id == "op-ok"


@pytest.mark.parametrize("bad", [0, -1, True, "7", None, 7.0, 10**9])
def test_fail_refuses_an_invalid_issue_number__fr012(bad):
    doc = doc_of()
    refused(lambda: record.fail(doc, bad, "prompt_invalid", NOW_B), doc)
    assert doc.entries == {}


@pytest.mark.parametrize("bad", [0, -1, True, "7", None, 7.0, 10**9])
def test_mark_pending_refuses_an_invalid_issue_number__fr012(bad):
    doc = doc_of()
    refused(lambda: record.mark_pending(doc, bad, CTX, NOW_B), doc)
    assert doc.entries == {}


def test_init_state_refuses_a_naive_now_and_creates_nothing__fr026(tmp_path):
    state_dir = tmp_path / "state"
    with pytest.raises(ValueError):
        init_state(state_dir, datetime(2026, 11, 7, 12, 0, 0))
    assert not state_dir.exists()


# ------------------------------------------------- set_considered and the setters

T_OLD = datetime(2026, 11, 7, 9, 0, 0, tzinfo=timezone.utc)


def with_considered(considered: dict) -> StoreDoc:
    return dataclasses.replace(doc_of(), considered=considered)


def test_fr023_set_considered_stamps_examined_and_drops_undiscovered():
    doc = with_considered({7: T_OLD, 8: T_OLD, 9: T_OLD})
    after = record.set_considered(doc, [7], [7, 8], NOW_B)
    # 7 examined: stamped now. 8 discovered but not examined: keeps its old time.
    # 9 not discovered any more: dropped.
    assert dict(after.considered) == {7: NOW_B, 8: T_OLD}


def test_fr023_set_considered_does_not_stamp_an_examined_but_undiscovered_issue():
    doc = with_considered({7: T_OLD})
    after = record.set_considered(doc, [7, 99], [7], NOW_B)
    assert dict(after.considered) == {7: NOW_B}


def test_fr023_set_considered_adds_a_newly_discovered_examined_issue():
    after = record.set_considered(
        with_considered({}), iter([5, 6]), iter([5, 6]), NOW_B
    )
    assert dict(after.considered) == {5: NOW_B, 6: NOW_B}


def test_fr023_set_considered_with_nothing_discovered_empties_the_map():
    after = record.set_considered(with_considered({7: T_OLD}), [7], [], NOW_B)
    assert dict(after.considered) == {}


def test_fr023_set_considered_leaves_its_input_and_other_fields_alone():
    doc = with_considered({7: T_OLD, 9: T_OLD})
    before = copy.deepcopy(doc)
    after = record.set_considered(doc, [7], [7], NOW_B)
    assert doc == before
    assert after is not doc
    assert dataclasses.replace(after, considered=doc.considered) == doc


def test_fr028_set_next_permitted_sets_and_clears_only_that_field():
    doc = doc_of()
    before = copy.deepcopy(doc)
    when = at(13, 30)
    set_doc = record.set_next_permitted(doc, when)
    assert set_doc.next_permitted_at == when
    assert dataclasses.replace(set_doc, next_permitted_at=None) == doc
    assert record.set_next_permitted(set_doc, None).next_permitted_at is None
    assert doc == before


def test_set_last_completed_stamps_exactly_now_and_nothing_else():
    doc = doc_of()
    assert doc.last_completed_cycle_at == at(11, 30)  # store_raw's own value
    before = copy.deepcopy(doc)
    after = record.set_last_completed(doc, NOW_B)
    assert after.last_completed_cycle_at == NOW_B
    assert (
        dataclasses.replace(after, last_completed_cycle_at=doc.last_completed_cycle_at)
        == doc
    )
    assert doc == before

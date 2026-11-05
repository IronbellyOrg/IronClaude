# Capture recipe for fixtures/merge_tree_conflict.z (run once from the repository root;
# it works in a scratch directory, copies out.z into fixtures/ and removes the scratch
# directory afterwards):
#
#   R=$(pwd)
#   S=$(mktemp -d /tmp/t3-mergetree.XXXXXXXX)
#   export GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_NOSYSTEM=1
#   export GIT_AUTHOR_NAME=Test GIT_AUTHOR_EMAIL=test@example.com
#   export GIT_COMMITTER_NAME=Test GIT_COMMITTER_EMAIL=test@example.com
#   export GIT_AUTHOR_DATE=2026-01-01T00:00:00Z GIT_COMMITTER_DATE=2026-01-01T00:00:00Z
#   cd "$S" && git init -q -b main repo && cd repo
#   printf 'base\n' > f.txt; printf 'keep\n' > d.txt
#   git add f.txt d.txt && git commit -q -m base
#   git checkout -q -b pr
#   printf 'ours\n' > f.txt; printf 'modified\n' > d.txt
#   git commit -q -am pr
#   git checkout -q main
#   printf 'theirs\n' > f.txt; git rm -q d.txt
#   git commit -q -am main
#   git merge-tree --write-tree -z pr main > "$S/out.z"   # exit 1: conflicts
#   cp "$S/out.z" "$R/tests/pr_submit/fixtures/merge_tree_conflict.z"
#   cd / && rm -rf "$S"
#
# Result: one content conflict f.txt (stages 1/2/3) and one modify/delete d.txt
# (stages 1/2: deleted on main, modified on pr), captured with git 2.47.3.
"""Pure conflict core tests (design section 5; section 12.1 Hint, Parse, Classify,
Plan, Router, Gates, Cycle ids, Record and message, Resume and Purity cases)."""

from __future__ import annotations

import ast
import base64
import itertools
import json
from pathlib import Path

import pytest

from superclaude.pr_submit import conflicts as c
from superclaude.pr_submit import recovery
from superclaude.pr_submit.conflicts import (
    DEFAULT_ACTION,
    MECHANICAL_RULES,
    ConflictAction,
    ConflictEntry,
    MergeTreeListing,
    ResumePlan,
    StageRecord,
    SyncDecision,
    classify_path,
    conflict_plan,
    group_entries,
    mergeability_hint,
    needs_probe,
    parse_numstat_binary,
    parse_probe,
    parse_stage_records,
)
from superclaude.pr_submit.fsm import (
    build_push_triad,
    evaluate_push_decision,
    push_parent_ok,
)
from superclaude.pr_submit.models import MonitorState

FIXTURE = Path(__file__).parent / "fixtures" / "merge_tree_conflict.z"
CONFLICTS_PY = (
    Path(__file__).resolve().parents[2]
    / "src"
    / "superclaude"
    / "pr_submit"
    / "conflicts.py"
)

TREE = "94f94fd471e0a27a1da0c3e76fc54479e74be423"
SHA_A = "a" * 40
SHA_B = "b" * 40
SHA_C = "c" * 40
OID = "1" * 40


def _b64(text: str) -> str:
    return base64.b64encode(text.encode("utf-8")).decode("ascii")


# ---------------------------------------------------------------------------
# Hint
# ---------------------------------------------------------------------------

_STATES = [
    "CLEAN",
    "DIRTY",
    "BEHIND",
    "BLOCKED",
    "UNSTABLE",
    "HAS_HOOKS",
    "UNKNOWN",
    "dirty",
    "behind",
    "blocked",
    None,
    "junk",
    7,
]
# Expected hint for mergeable == MERGEABLE, by state.
_MERGEABLE_ROW = {
    "CLEAN": "clean",
    "DIRTY": "conflicting",
    "BEHIND": "behind",
    "BLOCKED": "blocked",
    "UNSTABLE": "clean",
    "HAS_HOOKS": "clean",
    "UNKNOWN": "clean",
    "dirty": "conflicting",
    "behind": "behind",
    "blocked": "blocked",
    None: "clean",
    "junk": "clean",
    7: "clean",
}


@pytest.mark.parametrize("mergeable", ["MERGEABLE", "mergeable", "Mergeable"])
@pytest.mark.parametrize("state", _STATES)
def test_hint_mergeable(mergeable, state):
    assert mergeability_hint(mergeable, state) == _MERGEABLE_ROW[state]


@pytest.mark.parametrize("mergeable", ["CONFLICTING", "conflicting"])
@pytest.mark.parametrize("state", _STATES)
def test_hint_conflicting_always_wins(mergeable, state):
    assert mergeability_hint(mergeable, state) == "conflicting"


@pytest.mark.parametrize(
    "mergeable", ["UNKNOWN", "unknown", None, "junk", "", 3, ["MERGEABLE"]]
)
@pytest.mark.parametrize("state", _STATES)
def test_hint_not_mergeable_is_unknown_unless_dirty(mergeable, state):
    expected = (
        "conflicting"
        if isinstance(state, str) and state.upper() == "DIRTY"
        else "unknown"
    )
    assert mergeability_hint(mergeable, state) == expected


@pytest.mark.parametrize(
    "hint, expected",
    [
        ("conflicting", True),
        ("unknown", True),
        ("clean", False),
        ("behind", False),
        ("blocked", False),
        ("CONFLICTING", False),
        ("", False),
    ],
)
def test_needs_probe(hint, expected):
    assert needs_probe(hint) is expected


# ---------------------------------------------------------------------------
# Parse: merge-tree stage records
# ---------------------------------------------------------------------------


def test_parse_stage_records_on_captured_fixture():
    listing = parse_stage_records(FIXTURE.read_bytes().decode("utf-8"))
    assert listing == MergeTreeListing(
        tree_oid=TREE,
        records=(
            StageRecord(
                "100644", "2fa992c0b8b5c6acd2bdd4fa31de29d29799bdd5", 1, "d.txt"
            ),
            StageRecord(
                "100644", "2e0996000b7e9019eabcad29391bf0f5c7702f0b", 2, "d.txt"
            ),
            StageRecord(
                "100644", "df967b96a579e45a18b8251732d16804b2e56a55", 1, "f.txt"
            ),
            StageRecord(
                "100644", "b19a1e93bec1317dc6097229e12afaffbfa74dc2", 2, "f.txt"
            ),
            StageRecord(
                "100644", "950b81b7eee953d050aa05a641f8e056c85dd1bd", 3, "f.txt"
            ),
        ),
    )


def test_group_entries_on_captured_fixture():
    listing = parse_stage_records(FIXTURE.read_bytes().decode("utf-8"))
    entries = group_entries(listing, frozenset({"f.txt"}))
    assert [(e.path, e.stages, e.binary) for e in entries] == [
        ("d.txt", "12", False),
        ("f.txt", "123", True),
    ]
    d = entries[0]
    assert d.modes == {"base": "100644", "ours": "100644", "theirs": None}
    assert d.oids == {
        "base": "2fa992c0b8b5c6acd2bdd4fa31de29d29799bdd5",
        "ours": "2e0996000b7e9019eabcad29391bf0f5c7702f0b",
        "theirs": None,
    }


def test_group_entries_sorts_stages_and_keeps_first_seen_order():
    listing = MergeTreeListing(
        TREE,
        (
            StageRecord("100644", OID, 3, "b"),
            StageRecord("100644", OID, 2, "a"),
            StageRecord("100644", OID, 2, "b"),
        ),
    )
    entries = group_entries(listing, frozenset())
    assert [(e.path, e.stages) for e in entries] == [("b", "23"), ("a", "2")]


def test_group_entries_rejects_non_listing():
    with pytest.raises(ValueError):
        group_entries("junk", frozenset())  # type: ignore[arg-type]


def test_parse_stage_records_tree_only_gives_no_records():
    assert parse_stage_records(TREE + "\0") == MergeTreeListing(TREE, ())
    assert parse_stage_records(TREE) == MergeTreeListing(TREE, ())


def test_parse_stage_records_ignores_messages_after_empty_field():
    raw = (
        f"{TREE}\x00100644 {OID} 2\tx\x00\x00"
        + "1\x00x\x00CONFLICT (junk)\x00not a record\x00"
    )
    assert parse_stage_records(raw).records == (StageRecord("100644", OID, 2, "x"),)


@pytest.mark.parametrize(
    "raw",
    [
        pytest.param("deadbeef\0", id="bad-tree-oid-short"),
        pytest.param(("g" * 40) + "\0", id="bad-tree-oid-nonhex"),
        pytest.param("", id="empty-output"),
        pytest.param(f"{TREE}\x0010064 {OID} 1\tx\0\0", id="bad-mode-5-digits"),
        pytest.param(f"{TREE}\x00100648 {OID} 1\tx\0\0", id="bad-mode-non-octal"),
        pytest.param(f"{TREE}\x00100644 {OID[:39]} 1\tx\0\0", id="short-oid"),
        pytest.param(f"{TREE}\x00100644 {OID} 0\tx\0\0", id="stage-0"),
        pytest.param(f"{TREE}\x00100644 {OID} 4\tx\0\0", id="stage-4"),
        pytest.param(f"{TREE}\x00100644 {OID} 1\t\0\0", id="empty-path"),
        pytest.param(
            f"{TREE}\x00100644 {OID} 1\tx\x00100644 {OID} 1\tx\0\0",
            id="duplicate-path-stage",
        ),
        pytest.param(f"{TREE}\x00100644 {OID} 1 x\0\0", id="missing-tab"),
        pytest.param(f"{TREE}\x00100644  {OID} 1\tx\0\0", id="extra-space"),
    ],
)
def test_parse_stage_records_malformed_raises(raw):
    with pytest.raises(ValueError):
        parse_stage_records(raw)


def test_parse_stage_records_non_string_raises():
    with pytest.raises(ValueError):
        parse_stage_records(b"bytes")  # type: ignore[arg-type]


# ---------------------------------------------------------------------------
# Parse: numstat binary listing
# ---------------------------------------------------------------------------


def test_parse_numstat_binary_rows():
    raw = "-\t-\timg.png\x003\t1\tsrc/a.py\x00-\t-\tdir/with\ttab.bin\x00"
    assert parse_numstat_binary(raw) == frozenset({"img.png", "dir/with\ttab.bin"})


def test_parse_numstat_binary_text_only_and_empty():
    assert parse_numstat_binary("1\t2\ta.txt\x00") == frozenset()
    assert parse_numstat_binary("") == frozenset()


@pytest.mark.parametrize(
    "raw",
    [
        pytest.param("1\ta.txt\x00", id="one-tab"),
        pytest.param("x\t2\ta.txt\x00", id="non-numeric"),
        pytest.param("1\t-\ta.txt\x00", id="mixed-dash"),
        pytest.param("1\t2\t\x00", id="empty-path"),
        pytest.param("1\t2\ta\x00\x00", id="empty-record"),
    ],
)
def test_parse_numstat_binary_malformed_raises(raw):
    with pytest.raises(ValueError):
        parse_numstat_binary(raw)


# ---------------------------------------------------------------------------
# Parse: probe JSON
# ---------------------------------------------------------------------------


def _probe(**overrides):
    payload = {
        "ok": True,
        "mode": "full",
        "merge_tree_supported": True,
        "base_ref": "origin/main",
        "base_sha": SHA_A,
        "head_sha": SHA_B,
        "merge_base": SHA_C,
        "behind": 3,
        "ahead": 2,
        "foreign_op": None,
        "merge_head": None,
        "tree_clean": True,
        "status_b64": "",
        "clean": False,
        "merge_tree_b64": base64.b64encode(FIXTURE.read_bytes()).decode("ascii"),
        "numstat_ours_b64": _b64("1\t1\tf.txt\x001\t1\td.txt\x00"),
        "numstat_theirs_b64": _b64("1\t1\tf.txt\x000\t1\td.txt\x00"),
        "programs": ["uv"],
        "truncated": False,
    }
    payload.update(overrides)
    return payload


def _without(key):
    return {k: v for k, v in _probe().items() if k != key}


_UNSUPPORTED = {
    "merge_tree_supported": False,
    "clean": None,
    "merge_tree_b64": None,
    "numstat_ours_b64": None,
    "numstat_theirs_b64": None,
}
_CLEAN = {
    "clean": True,
    "merge_tree_b64": _b64(TREE + "\0"),
    "numstat_ours_b64": None,
    "numstat_theirs_b64": None,
}


def test_parse_probe_valid_conflicting():
    result = parse_probe(_probe())
    assert result.merge_tree_supported is True
    assert result.clean is False
    assert result.base_ref == "origin/main"
    assert (result.base_sha, result.head_sha, result.merge_base) == (
        SHA_A,
        SHA_B,
        SHA_C,
    )
    assert (result.behind, result.ahead) == (3, 2)
    assert result.foreign_op is None
    assert result.listing is not None and result.listing.tree_oid == TREE
    assert len(result.listing.records) == 5
    assert result.binary_paths == frozenset()
    assert result.programs == frozenset({"uv"})
    assert result.status_porcelain == ""


@pytest.mark.parametrize("op", c.FOREIGN_OPS)
def test_parse_probe_accepts_each_foreign_op(op):
    assert parse_probe(_probe(foreign_op=op)).foreign_op == op


def test_parse_probe_binary_paths_union_both_sides():
    result = parse_probe(
        _probe(
            numstat_ours_b64=_b64("-\t-\tf.txt\x00"),
            numstat_theirs_b64=_b64("-\t-\tother.bin\x00"),
        )
    )
    assert result.binary_paths == frozenset({"f.txt", "other.bin"})


def test_parse_probe_decodes_status():
    status = " M pyproject.toml\x00"
    result = parse_probe(_probe(tree_clean=False, status_b64=_b64(status)))
    assert result.tree_clean is False
    assert result.status_porcelain == status


def test_parse_probe_unsupported_shape():
    result = parse_probe(_probe(**_UNSUPPORTED))
    assert result.merge_tree_supported is False
    assert result.clean is None and result.listing is None
    assert result.binary_paths == frozenset()


def test_parse_probe_clean_shape():
    result = parse_probe(_probe(**_CLEAN))
    assert result.clean is True
    assert result.listing == MergeTreeListing(TREE, ())


_BAD_PROBES = {
    "not-a-dict": ["not", "a", "dict"],
    "ok-false": _probe(ok=False),
    "ok-truthy": _probe(ok=1),
    "mode-ops": _probe(mode="ops"),
    "truncated-true": _probe(truncated=True),
    "truncated-missing": _without("truncated"),
    "supported-not-bool": _probe(merge_tree_supported="yes"),
    "base-ref-empty": _probe(base_ref=""),
    "base-ref-non-string": _probe(base_ref=3),
    "base-sha-short": _probe(base_sha="a" * 39),
    "head-sha-nonhex": _probe(head_sha="z" * 40),
    "head-sha-trailing-newline": _probe(head_sha=SHA_B + "\n"),
    "merge-base-missing": _without("merge_base"),
    "behind-negative": _probe(behind=-1),
    "ahead-bool": _probe(ahead=True),
    "behind-str": _probe(behind="3"),
    "foreign-op-unknown": _probe(foreign_op="bisect"),
    "foreign-op-missing": _without("foreign_op"),
    "merge-head-bad": _probe(merge_head="abc"),
    "tree-clean-not-bool": _probe(tree_clean="true"),
    "tree-clean-disagrees": _probe(tree_clean=True, status_b64=_b64(" M x\x00")),
    "status-missing": _without("status_b64"),
    "status-non-strict-b64": _probe(tree_clean=False, status_b64="IE0ge*A="),
    "status-missing-padding": _probe(tree_clean=False, status_b64="IE0geAA"),
    "merge-tree-b64-junk": _probe(merge_tree_b64="!!!!"),
    "merge-tree-b64-null": _probe(merge_tree_b64=None),
    "merge-tree-not-utf8": _probe(
        merge_tree_b64=base64.b64encode(b"\xff\xfe").decode()
    ),
    "merge-tree-bad-records": _probe(
        merge_tree_b64=_b64(TREE + "\x00100644 bad 1\tx\0\0")
    ),
    "numstat-ours-missing": _without("numstat_ours_b64"),
    "numstat-theirs-malformed": _probe(numstat_theirs_b64=_b64("x\ty\tz\x00")),
    "programs-not-list": _probe(programs="uv"),
    "programs-non-string": _probe(programs=["uv", 1]),
    "clean-not-bool": _probe(clean="false"),
    "clean-missing": _without("clean"),
    "clean-with-records": _probe(clean=True),
    "conflicting-without-records": _probe(merge_tree_b64=_b64(TREE + "\0")),
    "unsupported-clean-not-null": _probe(**{**_UNSUPPORTED, "clean": False}),
    "unsupported-listing-not-null": _probe(
        **{**_UNSUPPORTED, "merge_tree_b64": _b64(TREE + "\0")}
    ),
    "unsupported-numstat-missing": {
        k: v for k, v in _probe(**_UNSUPPORTED).items() if k != "numstat_ours_b64"
    },
    "oversize-field": _probe(
        merge_tree_b64=_b64(TREE + "\0" + "x" * c.MAX_PROBE_BYTES)
    ),
}


@pytest.mark.parametrize("payload", list(_BAD_PROBES.values()), ids=list(_BAD_PROBES))
def test_parse_probe_rejects_invalid(payload):
    with pytest.raises(ValueError):
        parse_probe(payload)


# ---------------------------------------------------------------------------
# Classify
# ---------------------------------------------------------------------------


def _entry(path, stages="123", *, mode="100644", modes=None, binary=False):
    sides = {"base": "1", "ours": "2", "theirs": "3"}
    if modes is None:
        modes = {side: (mode if num in stages else None) for side, num in sides.items()}
    oids = {side: (OID if num in stages else None) for side, num in sides.items()}
    return ConflictEntry(
        path=path, stages=stages, modes=modes, oids=oids, binary=binary
    )


UV = frozenset({"uv"})


@pytest.mark.parametrize(
    "entry, programs, expected",
    [
        # rule 0
        pytest.param(_entry("a\nb.txt"), UV, "halt:unsafe_path", id="r0-newline"),
        pytest.param(_entry("a\tb.txt"), UV, "halt:unsafe_path", id="r0-tab"),
        pytest.param(_entry("a\x7fb.txt"), UV, "halt:unsafe_path", id="r0-del"),
        # rule 1
        pytest.param(
            _entry("vendor/lib", mode="160000"), UV, "halt:submodule", id="r1"
        ),
        # rule 2
        pytest.param(_entry("link", mode="120000"), UV, "halt:symlink", id="r2"),
        # rule 3
        pytest.param(
            _entry(
                "run.sh", modes={"base": "100644", "ours": "100755", "theirs": "100644"}
            ),
            UV,
            "halt:mode_change",
            id="r3",
        ),
        # rule 4
        pytest.param(
            _entry(".github/workflows/ci.yml"), UV, "halt:protected", id="r4-workflows"
        ),
        pytest.param(
            _entry(".github/actions/a/x.yml"), UV, "halt:protected", id="r4-actions"
        ),
        pytest.param(
            _entry(".claude/settings.json"), UV, "halt:protected", id="r4-settings"
        ),
        pytest.param(
            _entry(".claude/settings.local.json"), UV, "halt:protected", id="r4-local"
        ),
        # rule 5
        pytest.param(
            _entry("app/migrations/0001.py"), UV, "halt:migration", id="r5-migrations"
        ),
        pytest.param(
            _entry("alembic/versions/x.py"), UV, "halt:migration", id="r5-alembic"
        ),
        pytest.param(
            _entry("db/migrate/2026_x.rb"), UV, "halt:migration", id="r5-db-migrate"
        ),
        # rule 6
        pytest.param(_entry("img.png", binary=True), UV, "halt:binary", id="r6"),
        # rule 7
        pytest.param(_entry("uv.lock"), UV, "regen:uv.lock", id="r7-root-uv-lock"),
        # rule 8
        pytest.param(
            _entry("package-lock.json"), UV, "halt:lockfile_no_recipe", id="r8-npm"
        ),
        pytest.param(
            _entry("Cargo.lock"), UV, "halt:lockfile_no_recipe", id="r8-cargo"
        ),
        pytest.param(
            _entry("x/custom.lock"), UV, "halt:lockfile_no_recipe", id="r8-dot-lock"
        ),
        # rule 9
        pytest.param(
            _entry("generated/api.py"), UV, "halt:generated_no_recipe", id="r9-seg"
        ),
        pytest.param(
            _entry("web/dist/app.js"), UV, "halt:generated_no_recipe", id="r9-dist"
        ),
        pytest.param(
            _entry("build/out.txt"), UV, "halt:generated_no_recipe", id="r9-build"
        ),
        pytest.param(
            _entry("src/api.generated.ts"), UV, "halt:generated_no_recipe", id="r9-gen"
        ),
        pytest.param(
            _entry("tests/x.snap"), UV, "halt:generated_no_recipe", id="r9-snap"
        ),
        # rule 10
        pytest.param(_entry("src/a.py"), UV, "text:content", id="r10"),
        # rule 11
        pytest.param(_entry("src/a.py", "12"), UV, "text:modify_delete", id="r11-12"),
        pytest.param(_entry("src/a.py", "13"), UV, "text:modify_delete", id="r11-13"),
        # rule 12
        pytest.param(_entry("src/a.py", "23"), UV, "text:add_add", id="r12"),
        # rule 13
        pytest.param(
            _entry("src/a.py", "2"), UV, "halt:unknown_shape", id="r13-stage-2-only"
        ),
        pytest.param(
            _entry("src/a.py", "1"), UV, "halt:unknown_shape", id="r13-stage-1-only"
        ),
        # boundaries (section 12.1)
        pytest.param(
            _entry("sub", mode="160000", binary=True),
            UV,
            "halt:submodule",
            id="b-submodule-beats-binary",
        ),
        pytest.param(
            _entry(".github/workflows/x.yml", "12"),
            UV,
            "halt:protected",
            id="b-protected-beats-text",
        ),
        pytest.param(
            _entry("uv.lock", "12"), UV, "halt:lockfile_no_recipe", id="b-uv-lock-12"
        ),
        pytest.param(
            _entry("uv.lock", "13"), UV, "halt:lockfile_no_recipe", id="b-uv-lock-13"
        ),
        pytest.param(
            _entry("pkg/uv.lock"), UV, "halt:lockfile_no_recipe", id="b-pkg-uv-lock"
        ),
        pytest.param(
            _entry("uv.lock"),
            frozenset(),
            "halt:lockfile_no_recipe",
            id="b-root-uv-lock-no-uv",
        ),
        pytest.param(
            _entry("__snapshots__/x.snap"),
            UV,
            "halt:generated_no_recipe",
            id="b-snapshots",
        ),
        pytest.param(_entry("a\tb.py"), UV, "halt:unsafe_path", id="b-path-with-tab"),
        pytest.param(
            _entry("uv.lock", binary=True), UV, "halt:binary", id="b-binary-beats-regen"
        ),
    ],
)
def test_classify_path_rules(entry, programs, expected):
    result = classify_path(entry, programs=programs)
    assert result.cls == expected
    assert result.path == entry.path
    assert result.stages == entry.stages
    assert result.reason


@pytest.mark.parametrize(
    "entry",
    [
        pytest.param("not an entry", id="non-entry"),
        pytest.param(None, id="none"),
        pytest.param(
            ConflictEntry(path=5, stages="123", modes={}, oids={}, binary=False),  # type: ignore[arg-type]
            id="non-string-path",
        ),
        pytest.param(_entry("a.py", "321"), id="unsorted-stages"),
        pytest.param(_entry("a.py", "124"), id="stage-4"),
        pytest.param(_entry("a.py", ""), id="empty-stages"),
        pytest.param(
            ConflictEntry(path="a.py", stages=123, modes={}, oids={}, binary=False),  # type: ignore[arg-type]
            id="non-string-stages",
        ),
        pytest.param(_entry(""), id="empty-path"),
    ],
)
def test_classify_path_unexpected_shape_is_unknown_shape(entry):
    assert classify_path(entry, programs=UV).cls == "halt:unknown_shape"


def test_classify_regen_needs_every_program_of_the_rule():
    rule = c.MechanicalRule(
        "gen.lock", "lockfile", ("src",), ("uv", "lock"), ("make", "check")
    )
    only_uv = classify_path(_entry("gen.lock"), programs=UV, rules=(rule,))
    assert only_uv.cls == "halt:lockfile_no_recipe"
    both = classify_path(
        _entry("gen.lock"), programs=frozenset({"uv", "make"}), rules=(rule,)
    )
    assert both.cls == "regen:gen.lock"


def test_shipped_mechanical_rules():
    assert MECHANICAL_RULES == (
        c.MechanicalRule(
            "uv.lock",
            "lockfile",
            ("pyproject.toml",),
            ("uv", "lock"),
            ("uv", "lock", "--check"),
        ),
    )


# ---------------------------------------------------------------------------
# Plan
# ---------------------------------------------------------------------------


def _conflict_probe(entries, programs=("uv",)):
    """A conflicting probe from (path, stages, binary) triples."""
    parts = [TREE]
    for path, stages, _binary in entries:
        parts.extend(f"100644 {OID} {s}\t{path}" for s in stages)
    listing = "\0".join(parts) + "\0\0"
    binary = "".join(f"-\t-\t{p}\x00" for p, _s, b in entries if b)
    text = "".join(f"1\t1\t{p}\x00" for p, _s, b in entries if not b)
    return _probe(
        merge_tree_b64=_b64(listing),
        numstat_ours_b64=_b64(binary + text),
        numstat_theirs_b64=_b64(text),
        programs=list(programs),
    )


@pytest.mark.parametrize(
    "hint, reason",
    [("clean", "no_conflict"), ("behind", "behind_only"), ("blocked", "blocked")],
)
def test_plan_tier0_hint_rows_run_no_probe(hint, reason):
    plan = conflict_plan(hint=hint, probe=None)
    assert (plan.tier, plan.reason, plan.hint) == (0, reason, hint)
    assert plan.github_conflicting is False
    assert plan.paths == () and plan.listing is None and plan.base_sha is None


def test_plan_blocked_row_from_merge_state():
    hint = mergeability_hint("MERGEABLE", "BLOCKED")
    plan = conflict_plan(hint=hint, probe=None)
    assert (plan.tier, plan.reason) == (0, "blocked")


@pytest.mark.parametrize("hint", ["conflicting", "unknown"])
def test_plan_probe_failed_is_unclassified(hint):
    plan = conflict_plan(hint=hint, probe=None, probe_failed=True)
    assert (plan.tier, plan.reason) == (None, "probe_failed")
    assert plan.github_conflicting is (hint == "conflicting")


def test_plan_merge_tree_unsupported_is_unclassified():
    plan = conflict_plan(hint="conflicting", probe=_probe(**_UNSUPPORTED))
    assert (plan.tier, plan.reason) == (None, "merge_tree_unsupported")
    assert (
        plan.base_sha == SHA_A and plan.merge_tree_oid is None and plan.listing is None
    )


@pytest.mark.parametrize(
    "probe",
    [
        pytest.param(None, id="missing-probe-with-probe-hint"),
        pytest.param(_probe(truncated=True), id="truncated"),
        pytest.param(_probe(status_b64="***"), id="bad-b64"),
        pytest.param(_probe(merge_tree_b64=_b64("nottree\0")), id="bad-listing"),
        pytest.param(_probe(behind=-2), id="invalid-field"),
        pytest.param("junk", id="non-dict"),
    ],
)
def test_plan_malformed_probe_is_tier3(probe):
    plan = conflict_plan(hint="conflicting", probe=probe)
    assert (plan.tier, plan.reason) == (3, "probe_malformed")


def test_plan_junk_hint_is_tier3():
    assert conflict_plan(hint="junk", probe=None).tier == 3
    assert conflict_plan(hint=None, probe=None).tier == 3  # type: ignore[arg-type]


def test_plan_clean_probe_is_tier0_and_flags_github_disagreement():
    plan = conflict_plan(hint="conflicting", probe=_probe(**_CLEAN))
    assert (plan.tier, plan.reason) == (0, "no_conflict")
    assert plan.github_conflicting is True
    assert plan.merge_tree_oid == TREE and plan.behind == 3
    assert (
        conflict_plan(hint="unknown", probe=_probe(**_CLEAN)).github_conflicting
        is False
    )


def test_plan_captured_fixture_is_tier2():
    plan = conflict_plan(hint="conflicting", probe=_probe())
    assert (plan.tier, plan.reason) == (2, "text_conflict")
    assert [(p.path, p.cls) for p in plan.paths] == [
        ("d.txt", "text:modify_delete"),
        ("f.txt", "text:content"),
    ]
    assert plan.text_paths == ("d.txt", "f.txt")
    assert plan.regen_paths == ()
    assert plan.merge_tree_oid == TREE
    assert (plan.base_sha, plan.head_sha) == (SHA_A, SHA_B)
    assert plan.listing is not None and len(plan.listing.records) == 5


def test_plan_halt_class_is_tier3_with_first_halt_reason():
    entries = [
        ("a.py", "123", False),
        ("img.png", "123", True),
        ("uv.lock", "12", False),
    ]
    plan = conflict_plan(hint="conflicting", probe=_conflict_probe(entries))
    assert (plan.tier, plan.reason) == (3, "halt:binary")


def test_plan_eight_text_paths_is_tier2():
    entries = [(f"src/f{i}.py", "123", False) for i in range(8)]
    plan = conflict_plan(hint="conflicting", probe=_conflict_probe(entries))
    assert (plan.tier, plan.reason) == (2, "text_conflict")
    assert len(plan.text_paths) == 8


def test_plan_nine_text_paths_is_tier3_too_many_files():
    entries = [(f"src/f{i}.py", "123", False) for i in range(9)]
    plan = conflict_plan(hint="conflicting", probe=_conflict_probe(entries))
    assert (plan.tier, plan.reason) == (3, "too_many_files")


def test_plan_regen_plus_text_is_tier2_and_regen_not_counted():
    entries = [("uv.lock", "123", False)] + [
        (f"src/f{i}.py", "123", False) for i in range(8)
    ]
    plan = conflict_plan(hint="conflicting", probe=_conflict_probe(entries))
    assert (plan.tier, plan.reason) == (2, "text_conflict")
    assert plan.regen_paths == ("uv.lock",)
    assert len(plan.text_paths) == 8


def test_plan_regen_only_is_tier1():
    plan = conflict_plan(
        hint="unknown", probe=_conflict_probe([("uv.lock", "123", False)])
    )
    assert (plan.tier, plan.reason) == (1, "regen_only")
    assert plan.regen_paths == ("uv.lock",) and plan.text_paths == ()


def test_plan_regen_without_program_is_tier3():
    probe = _conflict_probe([("uv.lock", "123", False)], programs=())
    plan = conflict_plan(hint="conflicting", probe=probe)
    assert (plan.tier, plan.reason) == (3, "halt:lockfile_no_recipe")


def test_plan_tier2_max_files_override_and_invalid():
    probe = _conflict_probe([(f"src/f{i}.py", "123", False) for i in range(3)])
    assert conflict_plan(hint="conflicting", probe=probe, tier2_max_files=2).reason == (
        "too_many_files"
    )
    bad = conflict_plan(hint="conflicting", probe=probe, tier2_max_files="8")  # type: ignore[arg-type]
    assert (bad.tier, bad.reason) == (3, "probe_malformed")


def test_plan_never_raises_on_bad_rules():
    probe = _conflict_probe([("uv.lock", "123", False)])
    plan = conflict_plan(hint="conflicting", probe=probe, rules="junk")  # type: ignore[arg-type]
    assert plan.tier == 3


# ---------------------------------------------------------------------------
# Router (design section 4.4)
# ---------------------------------------------------------------------------

A = ConflictAction
T = "terminal_halted"


def _route(
    hook,
    tier,
    ordinal,
    *,
    entering=None,
    cap=2,
    rc=0,
    mr=3,
    prior=0,
    gc=True,
    reason="",
):
    return c.conflict_action(
        hook=hook,
        plan_tier=tier,
        ordinal=ordinal,
        entering=entering,
        conflict_max_tier=cap,
        round_counter=rc,
        max_rounds=mr,
        prior_conflict_cycles=prior,
        github_conflicting=gc,
        plan_reason=reason,
    )


def test_default_action_literal():
    assert DEFAULT_ACTION == A("halt", "router_unreachable", T, skip_ci=True)


# (plan_tier, ordinal, conflict_max_tier, plan_reason, expected)
_WAVE0_ROWS = [
    (None, 1, 2, "probe_failed", A("report", "probe_failed")),
    (None, 3, 2, "probe_failed", A("report", "probe_failed")),
    (None, 2, 0, "merge_tree_unsupported", A("report", "merge_tree_unsupported")),
    (0, 1, 2, "no_conflict", A("report", "no_conflict")),
    (0, 2, 0, "behind_only", A("report", "behind_only")),
    (0, 3, 1, "blocked", A("report", "blocked")),
    (1, 1, 0, "", A("report", "tier_above_cap")),
    (1, 3, 0, "", A("report", "tier_above_cap")),
    (1, 1, 1, "", A("report", "tier1_planned")),
    (1, 3, 2, "", A("report", "tier1_planned")),
    (2, 3, 1, "", A("report", "tier_above_cap")),
    (2, 1, 2, "", A("report", "tier2_report_only")),
    (2, 2, 2, "", A("report", "tier2_report_only")),
    (2, 3, 2, "", A("report", "tier2_planned")),
    (3, 1, 2, "", A("report", "conflict_tier3")),
    (3, 2, 0, "", A("report", "conflict_tier3")),
    (3, 3, 2, "", A("halt", "conflict_tier3", T)),
    (3, 3, 0, "", A("halt", "conflict_tier3", T)),
]


@pytest.mark.parametrize("tier,ordinal,cap,reason,expected", _WAVE0_ROWS)
def test_router_wave0_rows(tier, ordinal, cap, reason, expected):
    assert _route("wave0", tier, ordinal, cap=cap, reason=reason) == expected


# (plan_tier, conflict_max_tier, round_counter, max_rounds, prior, plan_reason, expected)
_C_INITIAL_ROWS = [
    (None, 2, 0, 3, 0, "probe_failed", A("report", "probe_failed")),
    (None, 2, 0, 3, 0, "merge_tree_unsupported", A("report", "merge_tree_unsupported")),
    (0, 2, 0, 3, 0, "no_conflict", A("none", "no_conflict")),
    (1, 2, 0, 3, 0, "", A("none", "tier1_deferred")),
    (1, 0, 0, 3, 1, "", A("none", "tier1_deferred")),
    (2, 1, 0, 3, 0, "", A("report", "tier_above_cap")),
    (2, 2, 2, 3, 0, "", A("report", "no_round_budget")),
    (2, 2, 0, 1, 0, "", A("report", "no_round_budget")),
    (2, 2, 0, 3, 1, "", A("report", "sync_cap")),
    (
        2,
        2,
        1,
        3,
        0,
        "",
        A("resolve_push", "tier2_merge", fsm_event="conflicting", push_kind="merge"),
    ),
    (3, 2, 0, 3, 0, "", A("halt", "conflict_tier3", T)),
    (3, 0, 0, 3, 5, "", A("halt", "conflict_tier3", T)),
]


@pytest.mark.parametrize("tier,cap,rc,mr,prior,reason,expected", _C_INITIAL_ROWS)
def test_router_c_initial_rows(tier, cap, rc, mr, prior, reason, expected):
    got = _route(
        "c_initial", tier, 3, cap=cap, rc=rc, mr=mr, prior=prior, reason=reason
    )
    assert got == expected


# (plan_tier, ordinal, entering, conflict_max_tier, prior, github_conflicting,
#  plan_reason, expected)
_WAVE8A_ROWS = [
    (None, 1, "clean", 2, 0, True, "probe_failed", A("halt", "probe_failed", T, True)),
    (
        None,
        3,
        "no_response",
        2,
        0,
        True,
        "merge_tree_unsupported",
        A("report", "merge_tree_unsupported", None, True),
    ),
    (0, 2, "clean", 2, 0, False, "no_conflict", A("none", "no_conflict")),
    (0, 3, "halt_max_rounds", 0, 1, False, "", A("none", "no_conflict")),
    (0, 1, "report_only", 2, 0, True, "", A("halt", "github_disagrees", T, True)),
    (
        0,
        1,
        "halt_max_rounds",
        2,
        0,
        True,
        "",
        A("report", "github_disagrees", None, True),
    ),
    (1, 3, "clean", 0, 0, True, "", A("halt", "tier_above_cap", T, True)),
    (1, 3, "no_response", 0, 0, True, "", A("report", "tier_above_cap", None, True)),
    (1, 3, "clean", 1, 1, True, "", A("halt", "sync_cap", T, True)),
    (1, 2, "halt_max_rounds", 1, 1, True, "", A("report", "sync_cap", None, True)),
    (
        1,
        1,
        "halt_max_rounds",
        1,
        0,
        True,
        "",
        A("report", "tier1_l1_preserved", None, True),
    ),
    (
        1,
        1,
        "no_response",
        2,
        0,
        True,
        "",
        A("report", "tier1_l1_preserved", None, True),
    ),
    (1, 1, "clean", 1, 0, True, "", A("propose", "tier1_proposed", "proposed", True)),
    (
        1,
        1,
        "report_only",
        2,
        0,
        True,
        "",
        A("propose", "tier1_proposed", "proposed", True),
    ),
    (
        1,
        2,
        "halt_max_rounds",
        1,
        0,
        True,
        "",
        A("report", "tier1_l2_preserved", None, True),
    ),
    (
        1,
        2,
        "clean",
        1,
        0,
        True,
        "",
        A("resolve_local", "tier1_local", "halt_before_push", True),
    ),
    (1, 3, "clean", 1, 0, True, "", A("resolve_push", "tier1_sync", push_kind="sync")),
    (
        1,
        3,
        "halt_max_rounds",
        1,
        0,
        False,
        "",
        A("resolve_push", "tier1_sync", push_kind="sync"),
    ),
    (2, 3, "clean", 1, 0, True, "", A("halt", "tier_above_cap", T, True)),
    (
        2,
        3,
        "halt_max_rounds",
        1,
        0,
        True,
        "",
        A("report", "tier_above_cap", None, True),
    ),
    (2, 3, "clean", 2, 0, True, "", A("halt", "late_conflict", T, True)),
    (2, 1, "no_response", 2, 0, True, "", A("report", "late_conflict", None, True)),
    (3, 3, "clean", 2, 0, True, "", A("halt", "conflict_tier3", T, True)),
    (
        3,
        2,
        "halt_max_rounds",
        2,
        0,
        True,
        "",
        A("report", "conflict_tier3", None, True),
    ),
]


@pytest.mark.parametrize(
    "tier,ordinal,entering,cap,prior,gc,reason,expected", _WAVE8A_ROWS
)
def test_router_wave8a_rows(tier, ordinal, entering, cap, prior, gc, reason, expected):
    got = _route(
        "wave8a",
        tier,
        ordinal,
        entering=entering,
        cap=cap,
        prior=prior,
        gc=gc,
        reason=reason,
    )
    assert got == expected


@pytest.mark.parametrize("entering", c.PRESERVED_OUTCOMES)
def test_router_wave8a_tier1_preserved_column(entering):
    by_ordinal = {
        o: _route("wave8a", 1, o, entering=entering, cap=1, prior=0) for o in (1, 2, 3)
    }
    assert by_ordinal == {
        1: A("report", "tier1_l1_preserved", None, True),
        2: A("report", "tier1_l2_preserved", None, True),
        3: A("resolve_push", "tier1_sync", push_kind="sync"),
    }


@pytest.mark.parametrize(
    "hook,entering", [("wave0", None), ("wave8a", "clean"), ("wave8a", "no_response")]
)
@pytest.mark.parametrize("tier", [None, 0, 1, 2, 3])
def test_router_l0_row(hook, entering, tier):
    reason = {None: "probe_failed", 0: "no_conflict"}.get(tier, "")
    got = _route(hook, tier, 0, entering=entering, reason=reason)
    assert got == A("none", "l0")


_DOMAIN_VIOLATIONS = [
    {"hook": "wave1"},
    {"hook": None},
    {"hook": "WAVE0"},
    {"ordinal": -1},
    {"ordinal": 4},
    {"ordinal": "3"},
    {"ordinal": True},
    {"ordinal": 3.0},
    {"conflict_max_tier": -1},
    {"conflict_max_tier": 3},
    {"conflict_max_tier": True},
    {"conflict_max_tier": "1"},
    {"plan_tier": 4},
    {"plan_tier": -1},
    {"plan_tier": True},
    {"plan_tier": "1"},
    {"round_counter": -1},
    {"round_counter": "0"},
    {"max_rounds": -1},
    {"max_rounds": None},
    {"prior_conflict_cycles": -1},
    {"prior_conflict_cycles": 1.5},
    {"prior_conflict_cycles": False},
    {"entering": "clean"},
    {"hook": "c_initial", "entering": "clean"},
    {"hook": "wave8a", "entering": None},
    {"hook": "wave8a", "entering": "junk"},
    {"hook": "c_initial", "ordinal": 1},
    {"github_conflicting": None},
    {"github_conflicting": "yes"},
    {"plan_tier": None, "plan_reason": "junk"},
    {"plan_tier": None, "plan_reason": "no_conflict"},
    {"plan_tier": 0, "plan_reason": ""},
    {"plan_tier": 0, "plan_reason": "probe_failed"},
    {"hook": "wave8a", "entering": "clean", "plan_tier": None, "plan_reason": ""},
]


@pytest.mark.parametrize("override", _DOMAIN_VIOLATIONS)
def test_router_domain_violation_reaches_default_row(override):
    kwargs = {
        "hook": "wave0",
        "plan_tier": 1,
        "ordinal": 3,
        "entering": None,
        "conflict_max_tier": 1,
        "round_counter": 0,
        "max_rounds": 3,
        "prior_conflict_cycles": 0,
        "github_conflicting": True,
        "plan_reason": "",
    }
    kwargs.update(override)
    assert c.conflict_action(**kwargs) == DEFAULT_ACTION


_TIER_REASONS = [
    (None, "probe_failed"),
    (None, "merge_tree_unsupported"),
    (0, "no_conflict"),
    (0, "behind_only"),
    (0, "blocked"),
    (1, ""),
    (2, ""),
    (3, ""),
]
_RANK = {
    "none": 0,
    "report": 1,
    "halt": 1,
    "propose": 2,
    "resolve_local": 3,
    "resolve_push": 4,
}


def _in_domain_product(hook):
    enterings = [None] if hook == "wave0" else list(c.ENTERING_OUTCOMES)
    return itertools.product(
        _TIER_REASONS,
        enterings,
        (0, 1, 2),  # conflict_max_tier
        (0, 1, 2, 3),  # round_counter
        (0, 1, 3),  # max_rounds
        (0, 1, 2),  # prior_conflict_cycles
        (False, True),  # github_conflicting
    )


@pytest.mark.parametrize("hook", ["wave0", "wave8a"])
def test_router_ordinal_monotonicity(hook):
    checked = 0
    for (tier, reason), entering, cap, rc, mr, prior, gc in _in_domain_product(hook):
        actions = [
            _route(
                hook,
                tier,
                o,
                entering=entering,
                cap=cap,
                rc=rc,
                mr=mr,
                prior=prior,
                gc=gc,
                reason=reason,
            )
            for o in range(4)
        ]
        for act in actions:
            assert act != DEFAULT_ACTION
            assert act.action in c.ACTIONS
            assert act.reason in c.REPORT_REASONS
        ranks = [_RANK[a.action] for a in actions]
        assert ranks == sorted(ranks), (tier, entering, cap, rc, mr, prior, gc, actions)
        checked += 1
    assert checked > 1000


def test_router_c_initial_below_l3_is_default_row():
    for (tier, reason), cap, rc, mr, prior, gc in itertools.product(
        _TIER_REASONS, (0, 1, 2), (0, 1, 3), (0, 1, 3), (0, 1), (False, True)
    ):
        for ordinal in (0, 1, 2):
            got = _route(
                "c_initial",
                tier,
                ordinal,
                cap=cap,
                rc=rc,
                mr=mr,
                prior=prior,
                gc=gc,
                reason=reason,
            )
            assert got == DEFAULT_ACTION


def test_report_and_halt_reasons_overlap_in_exactly_eight():
    assert c.REPORT_REASONS & c.HALT_REASONS == {
        "tier_above_cap",
        "conflict_tier3",
        "probe_failed",
        "merge_tree_unsupported",
        "github_disagrees",
        "sync_cap",
        "late_conflict",
        "router_unreachable",
    }


# ---------------------------------------------------------------------------
# Gates
# ---------------------------------------------------------------------------

PRE = SHA_A
BASE = SHA_B


@pytest.mark.parametrize(
    "parents,pre,base,expected",
    [
        ([PRE, BASE], PRE, BASE, True),
        ([PRE.upper(), BASE.upper()], PRE, BASE, True),
        ([PRE, BASE], PRE.upper(), BASE.upper(), True),
        ([PRE + "\n", BASE], PRE, BASE, False),
        ([PRE, BASE + "\n"], PRE, BASE, False),
        ([" " + PRE, BASE], PRE, BASE, False),
        ([PRE, BASE], " " + PRE, BASE, False),
        ([BASE, PRE], PRE, BASE, False),
        ([PRE, PRE], PRE, PRE, False),
        ([PRE, PRE.upper()], PRE, PRE, False),
        ([], PRE, BASE, False),
        ([PRE], PRE, BASE, False),
        ([PRE, BASE, SHA_C], PRE, BASE, False),
        (None, PRE, BASE, False),
        ((PRE, BASE), PRE, BASE, False),
        (f"{PRE} {BASE}", PRE, BASE, False),
        ([PRE[:7], BASE], PRE[:7], BASE, False),
        ([PRE, BASE[:12]], PRE, BASE[:12], False),
        ([PRE, BASE], None, BASE, False),
        ([PRE, BASE], PRE, None, False),
        ([PRE, None], PRE, BASE, False),
        ([PRE, 123], PRE, BASE, False),
        ([PRE, SHA_C], PRE, BASE, False),
        (["null", BASE], "null", BASE, False),
    ],
)
def test_merge_parent_ok_matrix(parents, pre, base, expected):
    assert c.merge_parent_ok(parents, pre, base) is expected


def test_merge_parent_ok_disjoint_from_push_parent_ok():
    pool = [SHA_A, SHA_B, SHA_C, SHA_A.upper(), SHA_A[:7], SHA_A + "\n", "", None, 5]
    accepted = 0
    for n in range(4):
        for combo in itertools.product(pool, repeat=n):
            parents = list(combo)
            for pre, base in ((SHA_A, SHA_B), (SHA_A.upper(), SHA_C), (SHA_A, SHA_A)):
                merge_ok = c.merge_parent_ok(parents, pre, base)
                push_ok = push_parent_ok(parents, pre)
                assert not (merge_ok and push_ok), parents
                if merge_ok:
                    accepted += 1
                    assert push_parent_ok(parents, pre) is False
    assert accepted > 0


@pytest.mark.parametrize(
    "porcelain,expected",
    [
        ("", (True, [])),
        ("M  a.py\0", (False, ["a.py"])),
        (" M b.py\0", (False, ["b.py"])),
        ("MM a.py\0 D gone.py\0", (False, ["a.py", "gone.py"])),
        ("R  new.py\0old.py\0", (False, ["new.py", "old.py"])),
        ("C  copy.py\0orig.py\0 M x.py\0", (False, ["copy.py", "orig.py", "x.py"])),
        ("?? untracked.txt\0", (True, [])),
        ("?? untracked.txt\0 M b.py\0", (False, ["b.py"])),
        (None, (False, ["<unparsable status>"])),
        (b"", (False, ["<unparsable status>"])),
        (["M  a.py"], (False, ["<unparsable status>"])),
        ("M  a.py", (False, ["<unparsable status>"])),
        ("garbage\0", (False, ["<unparsable status>"])),
        ("ZZ a.py\0", (False, ["<unparsable status>"])),
        ("M\0", (False, ["<unparsable status>"])),
        ("R  new.py\0", (False, ["<unparsable status>"])),
        ("   a.py\0", (False, ["<unparsable status>"])),
    ],
)
def test_merge_preflight_ok_rows(porcelain, expected):
    assert c.merge_preflight_ok(porcelain) == expected


def _sync(**overrides):
    kwargs = {
        "monitor_ordinal": 3,
        "validation_status": "validated",
        "tier": 1,
        "conflict_max_tier": 2,
        "halt_reason": None,
        "prior_conflict_cycles": 0,
        "round_counter": 0,
        "max_rounds": 3,
    }
    kwargs.update(overrides)
    return c.evaluate_sync_decision(**kwargs)


_BOOLS4 = list(itertools.product((True, False), repeat=4))


@pytest.mark.parametrize("p1,p2,p3,p4", _BOOLS4)
def test_evaluate_sync_decision_truth_table_tier1(p1, p2, p3, p4):
    got = _sync(
        tier=1,
        monitor_ordinal=3 if p1 else 2,
        validation_status="validated" if p2 else "failed",
        halt_reason=None if p3 else "sync_tier3",
        prior_conflict_cycles=0 if p4 else 1,
        round_counter=3,  # no round term for tier 1
        max_rounds=3,
    )
    assert got == SyncDecision(p1, p2, p3, p4, p1 and p2 and p3 and p4, "sync")


@pytest.mark.parametrize("p4_via", ["prior", "rounds"])
@pytest.mark.parametrize("p1,p2,p3,p4", _BOOLS4)
def test_evaluate_sync_decision_truth_table_tier2(p1, p2, p3, p4, p4_via):
    blocked_prior = not p4 and p4_via == "prior"
    blocked_rounds = not p4 and p4_via == "rounds"
    got = _sync(
        tier=2,
        monitor_ordinal=3 if p1 else 1,
        validation_status="validated" if p2 else "failed",
        conflict_max_tier=2 if p3 else 1,
        prior_conflict_cycles=1 if blocked_prior else 0,
        round_counter=3 if blocked_rounds else 2,
        max_rounds=3,
    )
    assert got == SyncDecision(p1, p2, p3, p4, p1 and p2 and p3 and p4, "merge")


@pytest.mark.parametrize("tier", [0, 3, None, True, "1", 1.0])
def test_evaluate_sync_decision_invalid_tier(tier):
    got = _sync(tier=tier)
    assert got.predicate_3_tier_allowed is False
    assert got.authorized is False
    assert got.kind == "sync"


@pytest.mark.parametrize(
    "override,predicate",
    [
        ({"monitor_ordinal": "3"}, "predicate_1_ordinal"),
        ({"monitor_ordinal": True}, "predicate_1_ordinal"),
        ({"conflict_max_tier": "2"}, "predicate_3_tier_allowed"),
        ({"prior_conflict_cycles": "0"}, "predicate_4_under_cap"),
        ({"prior_conflict_cycles": -1}, "predicate_4_under_cap"),
        ({"tier": 2, "round_counter": "0"}, "predicate_4_under_cap"),
        ({"tier": 2, "max_rounds": None}, "predicate_4_under_cap"),
    ],
)
def test_evaluate_sync_decision_non_int_inputs_fail_the_predicate(override, predicate):
    got = _sync(**override)
    assert getattr(got, predicate) is False
    assert got.authorized is False


def test_evaluate_sync_decision_audit_predicates():
    assert _sync().audit_predicates == {
        "p1_ordinal": True,
        "p2_validated": True,
        "p3_tier_allowed": True,
        "p4_under_cap": True,
    }


@pytest.mark.parametrize("ordinal", [0, 1, 2, 3, 4])
@pytest.mark.parametrize("status", ["validated", "failed", "", "VALIDATED"])
def test_sync_and_push_gates_agree_on_ordinal_and_validation(ordinal, status):
    sync = _sync(monitor_ordinal=ordinal, validation_status=status)
    push = evaluate_push_decision(
        monitor_ordinal=ordinal,
        validation_status=status,
        needs_human_decision=False,
        round_counter=0,
        max_rounds=3,
        applied_edits=1,
    )
    assert sync.predicate_1_ordinal == push.predicate_1_ordinal
    assert sync.predicate_2_validated == push.predicate_2_validated


@pytest.mark.parametrize(
    "decision,expected",
    [
        (
            SyncDecision(True, True, False, False, False, "sync"),
            MonitorState.HALT_HUMAN,
        ),
        (
            SyncDecision(True, True, False, True, False, "merge"),
            MonitorState.HALT_HUMAN,
        ),
        (
            SyncDecision(True, True, True, False, False, "sync"),
            MonitorState.REPORT_ONLY,
        ),
        (
            SyncDecision(False, True, True, True, False, "sync"),
            MonitorState.REPORT_ONLY,
        ),
        (
            SyncDecision(True, False, True, True, False, "merge"),
            MonitorState.REPORT_ONLY,
        ),
        (SyncDecision(True, True, True, True, True, "sync"), MonitorState.REPORT_ONLY),
        (None, MonitorState.HALT_HUMAN),
        ("blocked", MonitorState.HALT_HUMAN),
    ],
)
def test_sync_fail_state_mapping(decision, expected):
    assert c.sync_fail_state(decision) is expected


_GREEN = {"VG-1": True, "VG-3": True, "VG-4": True}


@pytest.mark.parametrize(
    "tier,results,expected",
    [
        (1, _GREEN, "validated"),
        (1, {**_GREEN, "VG-5": True}, "validated"),
        (1, {**_GREEN, "VG-2": False}, "failed"),
        (1, {"VG-1": True, "VG-3": True}, "failed"),
        (2, _GREEN, "failed"),
        (2, {**_GREEN, "VG-2": True}, "validated"),
        (2, {**_GREEN, "VG-2": False}, "failed"),
        (2, {**_GREEN, "VG-2": 1}, "failed"),
        (2, {"VG-2": True, "VG-1": True}, "failed"),
        (0, {**_GREEN, "VG-2": True}, "failed"),
        (3, {**_GREEN, "VG-2": True}, "failed"),
        (True, _GREEN, "failed"),
        (1, None, "failed"),
        (1, [("VG-1", True)], "failed"),
    ],
)
def test_conflict_validation_status(tier, results, expected):
    assert c.conflict_validation_status(tier, results) == expected


# ---------------------------------------------------------------------------
# Cycle ids
# ---------------------------------------------------------------------------


def test_conflict_cycle_id_values():
    assert c.conflict_cycle_id(1, 1) == "sync-1"
    assert c.conflict_cycle_id(2, 1) == "conflict-1"
    assert c.conflict_cycle_id(2, 3) == "conflict-3"


@pytest.mark.parametrize(
    "tier,n",
    [(0, 1), (3, 1), (1, 0), (2, -1), (True, 1), (1, True), ("1", 1), (1, "1")],
)
def test_conflict_cycle_id_rejects(tier, n):
    with pytest.raises(ValueError):
        c.conflict_cycle_id(tier, n)


@pytest.mark.parametrize(
    "cycle_id,expected",
    [
        ("sync-1", True),
        ("conflict-2", True),
        ("c1", False),
        ("cB", False),
        ("round-0", False),
        ("cycle-1", False),
        ("3f2b8a64-1c2d-4e5f-9a0b-1c2d3e4f5a6b", False),
        ("SYNC-1", False),
        ("", False),
        (None, False),
        (1, False),
    ],
)
def test_is_conflict_cycle(cycle_id, expected):
    assert c.is_conflict_cycle(cycle_id) is expected


@pytest.mark.parametrize(
    "cycles,cycle_id,expected",
    [
        (["sync-1"], "sync-1", 0),
        (["sync-1"], "sync-2", 1),
        ([], "sync-1", 0),
        (["sync-1", "sync-1", "conflict-2"], "sync-3", 2),
        ([1, None, "sync-1"], "sync-2", 1),
        (None, "sync-1", c.SYNC_CAP),
        ("sync-1", "sync-1", c.SYNC_CAP),
        (("sync-1",), "sync-2", c.SYNC_CAP),
    ],
)
def test_prior_conflict_cycles(cycles, cycle_id, expected):
    assert c.prior_conflict_cycles(cycles, cycle_id) == expected


# ---------------------------------------------------------------------------
# Record and message
# ---------------------------------------------------------------------------

_LISTING = MergeTreeListing(
    TREE,
    (
        StageRecord("100644", SHA_A, 1, "f.txt"),
        StageRecord("100644", SHA_B, 2, "f.txt"),
        StageRecord("100644", SHA_C, 3, "f.txt"),
        StageRecord("100644", OID, 2, "new.txt"),
        StageRecord("100644", SHA_B, 3, "new.txt"),
        StageRecord("100644", SHA_C, 1, "d.txt"),
        StageRecord("100644", SHA_B, 2, "d.txt"),
    ),
)


def test_finish_manifest_lines_in_listing_order():
    got = c.finish_manifest(_LISTING, ["d.txt", "new.txt", "f.txt"])
    assert got == f"{SHA_A}\tf.txt\n-\tnew.txt\n{SHA_C}\td.txt\n"
    assert c.finish_manifest(_LISTING, ["d.txt"]) == f"{SHA_C}\td.txt\n"
    assert c.finish_manifest(_LISTING, []) == ""


def test_finish_manifest_on_captured_fixture():
    listing = parse_stage_records(FIXTURE.read_bytes().decode("utf-8"))
    base = {r.path: r.oid for r in listing.records if r.stage == 1}
    order = list(dict.fromkeys(r.path for r in listing.records))
    assert sorted(order) == ["d.txt", "f.txt"]
    got = c.finish_manifest(listing, ["f.txt", "d.txt"])
    assert got == "".join(f"{base[p]}\t{p}\n" for p in order)


@pytest.mark.parametrize(
    "paths", [["x.txt"], ["f.txt", "f.txt"], ["f\tx.txt"], ["f.txt\n"], [""], [None]]
)
def test_finish_manifest_rejects(paths):
    with pytest.raises(ValueError):
        c.finish_manifest(_LISTING, paths)


def test_finish_manifest_rejects_non_listing():
    with pytest.raises(ValueError):
        c.finish_manifest("listing", ["f.txt"])  # type: ignore[arg-type]


_RECORD_TEXT = """\
## src/a.py
kind: additive
root_cause: both sides added an import block
ours_intent: Ours adds request logging.
theirs_intent: Theirs adds a metrics counter.
resolution: keep_both(ours first)
behavior_after: Requests are logged and counted.
dropped: none
evidence: stage files 1, 2 and 3 of src/a.py

## docs/b.md
kind: competing
root_cause: both sides reworded one sentence
ours_intent: Ours names the new flag.
theirs_intent: Theirs fixes a typo.
resolution: synthesized
behavior_after: The sentence names the flag without the typo.
dropped: none
evidence: stage files of docs/b.md
"""


def _good_entry(**overrides):
    entry = {
        "kind": "additive",
        "root_cause": "both sides added an import block",
        "ours_intent": "Ours adds request logging.",
        "theirs_intent": "Theirs adds a metrics counter.",
        "resolution": "keep_both(ours first)",
        "behavior_after": "Requests are logged and counted.",
        "dropped": "none",
        "evidence": "stage files 1, 2 and 3",
    }
    entry.update(overrides)
    return entry


def test_parse_resolution_record_valid():
    record = c.parse_resolution_record(_RECORD_TEXT)
    assert list(record) == ["src/a.py", "docs/b.md"]
    assert record["src/a.py"] == _good_entry(
        evidence="stage files 1, 2 and 3 of src/a.py"
    )
    assert record["docs/b.md"]["resolution"] == "synthesized"
    assert c.resolution_record_ok(record, ("src/a.py", "docs/b.md")) == []


@pytest.mark.parametrize(
    "text",
    [
        "## a.py\nkind: additive\n## a.py\nkind: additive\n",  # duplicate heading
        "## a.py\nkind: additive\nkind: competing\n",  # duplicate field
        "## a.py\ncolour: blue\n",  # unknown field
        "## a.py\nthis line has no field\n",  # not a field line
        "kind: additive\n## a.py\n",  # field before the first heading
        "## \nkind: additive\n",  # empty heading
    ],
)
def test_parse_resolution_record_rejects(text):
    with pytest.raises(ValueError):
        c.parse_resolution_record(text)


def test_parse_resolution_record_rejects_non_string():
    with pytest.raises(ValueError):
        c.parse_resolution_record(None)  # type: ignore[arg-type]


@pytest.mark.parametrize(
    "record,text_paths,expected",
    [
        ({"a.py": _good_entry()}, ("a.py",), []),
        ({"a.py": _good_entry(resolution="keep_both")}, ("a.py",), []),
        ({"a.py": _good_entry(ours_intent="Ours uses the v1.2 API.")}, ("a.py",), []),
        ({"a.py": _good_entry()}, ("a.py", "b.py"), ["b.py: missing entry"]),
        (
            {"a.py": _good_entry(), "z.py": _good_entry()},
            ("a.py",),
            ["z.py: extra entry"],
        ),
        (
            {"a.py": _good_entry(root_cause="  ")},
            ("a.py",),
            ["a.py: root_cause is missing or empty"],
        ),
        (
            {"a.py": _good_entry(ours_intent="Ours logs. It also counts.")},
            ("a.py",),
            ["a.py: ours_intent is not exactly one sentence"],
        ),
        (
            {"a.py": _good_entry(theirs_intent="Theirs adds\na counter.")},
            ("a.py",),
            ["a.py: theirs_intent is not exactly one sentence"],
        ),
        (
            {"a.py": _good_entry(behavior_after="Requests are logged")},
            ("a.py",),
            ["a.py: behavior_after is not exactly one sentence"],
        ),
        (
            {"a.py": _good_entry(kind="semantic")},
            ("a.py",),
            ["a.py: kind semantic means Tier 3"],
        ),
        (
            {"a.py": _good_entry(kind="mystery")},
            ("a.py",),
            ["a.py: unknown kind mystery"],
        ),
        (
            {"a.py": _good_entry(resolution="take_both")},
            ("a.py",),
            ["a.py: unknown resolution take_both"],
        ),
        (
            {"a.py": _good_entry(resolution="keep_both()")},
            ("a.py",),
            ["a.py: unknown resolution keep_both()"],
        ),
        (
            {"a.py": {k: v for k, v in _good_entry().items() if k != "dropped"}},
            ("a.py",),
            ["a.py: dropped is missing or empty"],
        ),
        ({"a.py": "kind: additive"}, ("a.py",), ["a.py: entry is not a mapping"]),
        ("## a.py", ("a.py",), ["record is not a mapping"]),
        (None, ("a.py",), ["record is not a mapping"]),
    ],
)
def test_resolution_record_ok_problems(record, text_paths, expected):
    assert c.resolution_record_ok(record, text_paths) == expected


def test_merge_commit_message_tier1():
    msg = c.merge_commit_message(
        base_ref="origin/master",
        head_branch="feat/x",
        tier=1,
        rule_patterns=("uv.lock",),
        lock_changes="requests 2.31.0 -> 2.32.0",
    )
    assert msg == (
        "Merge origin/master into feat/x (sc:pr-submit sync, tier 1)\n"
        "\n"
        "uv.lock regenerated from the merged pyproject.toml\n"
        "requests 2.31.0 -> 2.32.0\n"
    )


def test_merge_commit_message_tier2_labels_only():
    secret = "SENTINEL_FILE_CONTENT"
    record = {
        "src/a.py": _good_entry(
            ours_intent=f"Ours adds {secret}.",
            theirs_intent=f"Theirs adds {secret}.",
            behavior_after=f"Runs {secret}.",
            root_cause=secret,
            evidence=secret,
        )
    }
    msg = c.merge_commit_message(
        base_ref="origin/master", head_branch="feat/x", tier=2, record=record
    )
    assert msg == (
        "Merge origin/master into feat/x (sc:pr-submit sync, tier 2)\n"
        "\n"
        "src/a.py: kind additive, resolution keep_both(ours first), dropped none\n"
    )
    assert secret not in msg


@pytest.mark.parametrize(
    "kwargs",
    [
        {"tier": 2},
        {"tier": 2, "record": {}},
        {"tier": 2, "record": "## a.py"},
        {"tier": 3},
        {"tier": 0},
        {"tier": True},
        {"tier": 1, "rule_patterns": ("pkg/uv.lock",)},
        {"tier": 1, "base_ref": ""},
        {"tier": 1, "head_branch": "feat\nx"},
        {"tier": 2, "record": {"a.py": _good_entry(dropped="line one\nline two")}},
    ],
)
def test_merge_commit_message_rejects(kwargs):
    full = {"base_ref": "origin/master", "head_branch": "feat/x", **kwargs}
    with pytest.raises(ValueError):
        c.merge_commit_message(**full)


# ---------------------------------------------------------------------------
# Resume: crash_resume_plan (design section 4.8, table 2)
# ---------------------------------------------------------------------------


def test_branch_literals_equal_recovery():
    assert c.BRANCH_LANDED == recovery.BRANCH_A_LANDED
    assert c.BRANCH_NOT_LANDED == recovery.BRANCH_B_NOT_LANDED
    assert c.BRANCH_AMBIGUOUS == recovery.BRANCH_C_AMBIGUOUS


_ABSENT = object()
_DANGLING = {
    "event_type": "push_initiated",
    "run_id": "r1",
    "cycle_id": "sync-1",
    "pre_push_sha": SHA_A,
    "target_sha": SHA_C,
    "target_branch": "feat/x",
    "target_remote": "origin",
    "base_sha": SHA_B,
    "review_terminal": "clean",
    "expect_checks": False,
}
_FSM_STATE = MonitorState.S5A_RETRIGGER_REVIEW
_COMMON = {"cycle_id": "sync-1", "target_sha": SHA_C, "base_sha": SHA_B}
_WAVE8 = {"wait_sha": SHA_C, "review_terminal": "clean", "expect_checks": False}
_A, _B, _C = c.BRANCH_LANDED, c.BRANCH_NOT_LANDED, c.BRANCH_AMBIGUOUS


def _dangling(kind=_ABSENT, **overrides):
    record = dict(_DANGLING)
    if kind is not _ABSENT:
        record["kind"] = kind
    record.update(overrides)
    return record


def _ambiguous(kind):
    return ResumePlan(
        "halt",
        state=MonitorState.HALT_HUMAN,
        reason="ambiguous_remote_tip",
        kind=kind,
        **_COMMON,
    )


def _unrep(kind):
    return ResumePlan("halt", reason="resume_unrepresentable", kind=kind, **_COMMON)


_CRASH_TABLE = {
    ("fix", _A): ResumePlan("fsm", state=_FSM_STATE, kind="fix", **_COMMON),
    ("fix", _B): ResumePlan(
        "fsm", state=MonitorState.S4_PUSHING, kind="fix", **_COMMON
    ),
    ("fix", _C): _ambiguous("fix"),
    ("fix", "junk"): _unrep("fix"),
    (_ABSENT, _A): ResumePlan("fsm", state=_FSM_STATE, kind="fix", **_COMMON),
    (_ABSENT, _B): ResumePlan(
        "fsm", state=MonitorState.S4_PUSHING, kind="fix", **_COMMON
    ),
    (_ABSENT, _C): _ambiguous("fix"),
    (_ABSENT, "junk"): _unrep("fix"),
    ("merge", _A): ResumePlan("fsm", state=_FSM_STATE, kind="merge", **_COMMON),
    ("merge", _B): ResumePlan(
        "fsm",
        state=MonitorState.S4_PUSHING,
        kind="merge",
        check_merge_parent=True,
        **_COMMON,
    ),
    ("merge", _C): _ambiguous("merge"),
    ("merge", "junk"): _unrep("merge"),
    ("sync", _A): ResumePlan("wave8_ci_wait", kind="sync", **_COMMON, **_WAVE8),
    ("sync", _B): ResumePlan(
        "redrive_then_wave8",
        kind="sync",
        rerun_guard=True,
        check_merge_parent=True,
        **_COMMON,
        **_WAVE8,
    ),
    ("sync", _C): _ambiguous("sync"),
    ("sync", "junk"): _unrep("sync"),
    ("ci", _A): ResumePlan("wave8_ci_wait", kind="ci", **_COMMON, **_WAVE8),
    ("ci", _B): ResumePlan(
        "redrive_then_wave8",
        kind="ci",
        rerun_guard=True,
        check_merge_parent=False,
        **_COMMON,
        **_WAVE8,
    ),
    ("ci", _C): _ambiguous("ci"),
    ("ci", "junk"): _unrep("ci"),
    ("rebase", _A): _unrep(None),
    ("rebase", _B): _unrep(None),
    ("rebase", _C): _unrep(None),
    ("rebase", "junk"): _unrep(None),
}


@pytest.mark.parametrize(
    "kind,branch",
    list(_CRASH_TABLE),
    ids=[f"{'absent' if k is _ABSENT else k}-{b}" for k, b in _CRASH_TABLE],
)
def test_crash_resume_plan_table(kind, branch):
    dangling = _dangling(kind)
    before = dict(dangling)
    got = c.crash_resume_plan(dangling, branch, _FSM_STATE)
    assert got == _CRASH_TABLE[(kind, branch)]
    assert dangling == before  # pure: the record is not touched
    if kind in ("sync", "ci"):
        assert got.state not in (
            MonitorState.S4_PUSHING,
            MonitorState.S5A_RETRIGGER_REVIEW,
            MonitorState.S5_AWAITING_REREVIEW,
        )


@pytest.mark.parametrize("kind", ["sync", "ci"])
@pytest.mark.parametrize("branch", [_A, _B])
@pytest.mark.parametrize("review_terminal", [_ABSENT, None, "junk", "CLEAN"])
def test_crash_resume_plan_bad_review_terminal_halts(kind, branch, review_terminal):
    dangling = _dangling(kind)
    if review_terminal is _ABSENT:
        del dangling["review_terminal"]
    else:
        dangling["review_terminal"] = review_terminal
    got = c.crash_resume_plan(dangling, branch, _FSM_STATE)
    assert (got.directive, got.reason) == ("halt", "resume_unrepresentable")


@pytest.mark.parametrize("branch", [_A, _B])
@pytest.mark.parametrize("base_sha", [_ABSENT, None, SHA_B[:7], "null"])
def test_crash_resume_plan_sync_without_base_sha_halts(branch, base_sha):
    dangling = _dangling("sync")
    if base_sha is _ABSENT:
        del dangling["base_sha"]
    else:
        dangling["base_sha"] = base_sha
    got = c.crash_resume_plan(dangling, branch, _FSM_STATE)
    assert (got.directive, got.reason) == ("halt", "resume_unrepresentable")


def test_crash_resume_plan_ci_needs_no_base_sha():
    dangling = _dangling("ci")
    del dangling["base_sha"]
    got = c.crash_resume_plan(dangling, _A, _FSM_STATE)
    assert got.directive == "wave8_ci_wait"
    assert got.base_sha is None


@pytest.mark.parametrize("expect", [_ABSENT, None, "no", 0])
@pytest.mark.parametrize("kind", ["sync", "ci"])
def test_crash_resume_plan_missing_expect_checks_reads_true(expect, kind):
    dangling = _dangling(kind)
    if expect is _ABSENT:
        del dangling["expect_checks"]
    else:
        dangling["expect_checks"] = expect
    assert c.crash_resume_plan(dangling, _A, _FSM_STATE).expect_checks is True


def test_crash_resume_plan_ambiguous_wins_over_record_checks():
    dangling = _dangling("sync")
    del dangling["review_terminal"]
    assert c.crash_resume_plan(dangling, _C, _FSM_STATE) == ResumePlan(
        "halt",
        state=MonitorState.HALT_HUMAN,
        reason="ambiguous_remote_tip",
        kind="sync",
        **_COMMON,
    )


def test_crash_resume_plan_fails_closed_on_bad_inputs():
    assert c.crash_resume_plan(None, _A, _FSM_STATE) == ResumePlan(  # type: ignore[arg-type]
        "halt", reason="resume_unrepresentable"
    )
    got = c.crash_resume_plan(_dangling("fix"), _A, "S5_AWAITING_REREVIEW")  # type: ignore[arg-type]
    assert (got.directive, got.reason) == ("halt", "resume_unrepresentable")


# ---------------------------------------------------------------------------
# Resume: conflict_resume_plan (design section 4.8, table 1)
# ---------------------------------------------------------------------------


def _open_cycle(**overrides):
    entry = {
        "event_type": "sync_started",
        "run_id": "r1",
        "cycle_id": "sync-1",
        "tier": 1,
        "kind": "sync",
        "hook": "wave8a",
        "base_ref": "origin/master",
        "base_sha": SHA_B,
        "pre_push_sha": SHA_A,
        "merge_tree_oid": TREE,
        "conflict_max_tier": 1,
        "review_terminal": "clean",
        "paths": ["uv.lock"],
        "resumed": False,
        "push_initiated": False,
        "push_completed": False,
        "target_sha": None,
        "expect_checks": None,
        "superseded": False,
    }
    entry.update(overrides)
    return entry


_MERGE_CYCLE = {
    "cycle_id": "conflict-1",
    "tier": 2,
    "kind": "merge",
    "hook": "c_initial",
    "review_terminal": None,
}


def _state(open_cycle=None, *, rejected=False):
    cycles = [open_cycle["cycle_id"]] if isinstance(open_cycle, dict) else []
    return {
        "push_count": 0,
        "sync_push_count": 0,
        "conflict_cycles": cycles,
        "open_conflict_cycle": open_cycle,
        "push_rejected": rejected,
    }


def _resume(
    state,
    *,
    foreign_op=None,
    merge_head_sha=None,
    local_head_sha=SHA_A,
    local_head_parents=None,
    dangling=None,
):
    return c.conflict_resume_plan(
        state,
        foreign_op=foreign_op,
        merge_head_sha=merge_head_sha,
        local_head_sha=local_head_sha,
        local_head_parents=local_head_parents,
        dangling=dangling,
    )


_SYNC_IDS = {"cycle_id": "sync-1", "hook": "wave8a", "review_terminal": "clean"}
_MERGE_IDS = {"cycle_id": "conflict-1", "hook": "c_initial", "review_terminal": None}


def test_resume_row1_push_rejected_without_open_cycle():
    assert _resume(_state(rejected=True)) == ResumePlan("halt", reason="push_rejected")


def test_resume_row1_push_rejected_closes_open_cycle():
    state = _state(_open_cycle(push_initiated=True, target_sha=SHA_C), rejected=True)
    assert _resume(state) == ResumePlan(
        "halt", reason="push_rejected", cycle_id="sync-1"
    )


def test_resume_row2_no_open_cycle_no_foreign_op():
    assert _resume(_state()) == ResumePlan("none")


@pytest.mark.parametrize("op", c.FOREIGN_OPS)
def test_resume_row3_no_open_cycle_foreign_op(op):
    assert _resume(_state(), foreign_op=op, merge_head_sha=SHA_B) == ResumePlan(
        "halt", reason="foreign_op_in_progress"
    )


def test_resume_row3b_superseded_cycle_halts_before_row4():
    state = _state(
        _open_cycle(
            superseded=True, push_initiated=True, push_completed=True, target_sha=SHA_C
        )
    )
    assert _resume(state) == ResumePlan(
        "halt", reason="resume_unrepresentable", cycle_id="sync-1"
    )


@pytest.mark.parametrize(
    "overrides",
    [
        {"hook": _ABSENT},
        {"hook": "wave0"},
        {"hook": None},
        {"review_terminal": _ABSENT},
        {"review_terminal": None},
        {"review_terminal": "junk"},
        {"hook": "c_initial", "review_terminal": "clean"},
    ],
)
def test_resume_row4c_invalid_hook_or_review_terminal_halts(overrides):
    entry = _open_cycle(push_initiated=True, push_completed=True, target_sha=SHA_C)
    for key, value in overrides.items():
        if value is _ABSENT:
            del entry[key]
        else:
            entry[key] = value
    assert _resume(_state(entry)) == ResumePlan(
        "halt", reason="resume_unrepresentable", cycle_id="sync-1"
    )


def test_resume_row4c_c_initial_without_review_terminal_key_is_valid():
    entry = _open_cycle(**_MERGE_CYCLE)
    del entry["review_terminal"]
    assert _resume(_state(entry)).directive == "restart"


def test_resume_row4_sync_complete_after_push():
    state = _state(
        _open_cycle(
            push_initiated=True,
            push_completed=True,
            target_sha=SHA_C,
            expect_checks=False,
        )
    )
    assert _resume(state) == ResumePlan(
        "complete_after_push",
        kind="sync",
        wait_sha=SHA_C,
        target_sha=SHA_C,
        base_sha=SHA_B,
        expect_checks=False,
        **_SYNC_IDS,
    )


@pytest.mark.parametrize("expect", [_ABSENT, None, "false", 0])
def test_resume_row4_missing_expect_checks_reads_true(expect):
    entry = _open_cycle(push_initiated=True, push_completed=True, target_sha=SHA_C)
    if expect is _ABSENT:
        del entry["expect_checks"]
    else:
        entry["expect_checks"] = expect
    assert _resume(_state(entry)).expect_checks is True


def test_resume_row4_merge_resumes_at_retrigger():
    state = _state(
        _open_cycle(
            push_initiated=True,
            push_completed=True,
            target_sha=SHA_C,
            expect_checks=True,
            **_MERGE_CYCLE,
        )
    )
    assert _resume(state) == ResumePlan(
        "complete_after_push",
        state=MonitorState.S5A_RETRIGGER_REVIEW,
        kind="merge",
        target_sha=SHA_C,
        base_sha=SHA_B,
        expect_checks=True,
        **_MERGE_IDS,
    )


@pytest.mark.parametrize("overrides", [{"kind": "fix"}, {"target_sha": None}])
def test_resume_row4_unusable_push_record_halts(overrides):
    entry = _open_cycle(push_initiated=True, push_completed=True, target_sha=SHA_C)
    entry.update(overrides)
    got = _resume(_state(entry))
    assert (got.directive, got.reason, got.cycle_id) == (
        "halt",
        "resume_unrepresentable",
        "sync-1",
    )


def test_resume_row4b_matching_dangling_is_crash_window():
    state = _state(_open_cycle(push_initiated=True, target_sha=SHA_C))
    dangling = {"event_type": "push_initiated", "cycle_id": "sync-1", "kind": "sync"}
    assert _resume(state, dangling=dangling) == ResumePlan(
        "crash_window", kind="sync", target_sha=SHA_C, base_sha=SHA_B, **_SYNC_IDS
    )


@pytest.mark.parametrize(
    "dangling", [None, {"cycle_id": "c7"}, {"cycle_id": "conflict-1"}, "sync-1"]
)
def test_resume_row4b_prime_unmatched_dangling_halts(dangling):
    state = _state(_open_cycle(push_initiated=True, target_sha=SHA_C))
    assert _resume(state, dangling=dangling) == ResumePlan(
        "halt", reason="resume_unrepresentable", cycle_id="sync-1", target_sha=SHA_C
    )


@pytest.mark.parametrize("merge_head", [SHA_B, SHA_B.upper()])
def test_resume_row5_own_merge_aborts_and_restarts(merge_head):
    state = _state(_open_cycle())
    got = _resume(
        state, foreign_op="MERGE_HEAD", merge_head_sha=merge_head, local_head_sha=SHA_A
    )
    assert got == ResumePlan(
        "abort_and_restart", kind="sync", base_sha=SHA_B, **_SYNC_IDS
    )


def test_resume_row5_c_initial_cycle_carries_its_hook():
    state = _state(_open_cycle(**_MERGE_CYCLE))
    got = _resume(state, foreign_op="MERGE_HEAD", merge_head_sha=SHA_B)
    assert got == ResumePlan(
        "abort_and_restart", kind="merge", base_sha=SHA_B, **_MERGE_IDS
    )


@pytest.mark.parametrize(
    "op,merge_head",
    [("MERGE_HEAD", SHA_C), ("MERGE_HEAD", None), ("rebase-apply", SHA_B)],
)
def test_resume_row6_other_foreign_op_halts(op, merge_head):
    state = _state(_open_cycle())
    assert _resume(state, foreign_op=op, merge_head_sha=merge_head) == ResumePlan(
        "halt", reason="sync_foreign_operation", cycle_id="sync-1"
    )


@pytest.mark.parametrize("head", [SHA_A, SHA_A.upper()])
def test_resume_row7_head_at_pre_push_restarts(head):
    assert _resume(_state(_open_cycle()), local_head_sha=head) == ResumePlan(
        "restart", kind="sync", base_sha=SHA_B, **_SYNC_IDS
    )


def test_resume_row7_c_initial_restart_carries_its_hook():
    got = _resume(_state(_open_cycle(**_MERGE_CYCLE)), local_head_sha=SHA_A)
    assert got == ResumePlan("restart", kind="merge", base_sha=SHA_B, **_MERGE_IDS)
    assert got.hook == "c_initial"


@pytest.mark.parametrize(
    "head,parents",
    [(SHA_C, [SHA_A, SHA_B]), (SHA_C, None), (None, None), (SHA_A[:7], [SHA_A])],
)
def test_resume_row8_anything_else_halts(head, parents):
    got = _resume(
        _state(_open_cycle()), local_head_sha=head, local_head_parents=parents
    )
    assert got == ResumePlan("halt", reason="resume_unrepresentable", cycle_id="sync-1")


@pytest.mark.parametrize(
    "state",
    [
        None,
        {},
        {"open_conflict_cycle": None, "push_rejected": False},
        {k: v for k, v in _state().items() if k != "sync_push_count"},
        {**_state(), "push_rejected": "yes"},
        {**_state(), "conflict_cycles": None},
        {**_state(), "sync_push_count": -1},
        {**_state(), "open_conflict_cycle": "sync-1"},
        _state(_open_cycle(cycle_id="c1")),
        _state(_open_cycle(cycle_id=None)),
    ],
)
def test_resume_unusable_state_halts(state):
    assert _resume(state) == ResumePlan("halt", reason="resume_unrepresentable")


def test_resume_planners_are_pure():
    entry = _open_cycle(push_initiated=True, target_sha=SHA_C)
    state = _state(entry)
    dangling = {"cycle_id": "sync-1", "kind": "sync"}
    snapshot = (repr(state), repr(dangling))
    _resume(state, dangling=dangling)
    _resume(state, foreign_op="MERGE_HEAD", merge_head_sha=SHA_B)
    assert (repr(state), repr(dangling)) == snapshot


# ---------------------------------------------------------------------------
# Triad (fsm.build_push_triad keyword-only extras, design section 6.1 item 6)
# ---------------------------------------------------------------------------

# Captured from the pre-#305 build_push_triad (fsm.py:238-288) for _TRIAD_ARGS with
# the authorized evaluate_push_decision below, before the function was edited.
_RECORDED_TRIAD = [
    {
        "event_type": "push_decision",
        "round_counter": 0,
        "authorized": True,
        "predicates": {
            "p1_ordinal": True,
            "p2_validated": True,
            "p3_no_human": True,
            "p4_under_cap": True,
            "p5_applied_edits": 1,
        },
        "run_id": "run-1",
        "cycle_id": "c1",
        "idempotency_key": "push:run-1:c1:aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa:feat/x",
        "pre_push_sha": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
        "target_sha": "cccccccccccccccccccccccccccccccccccccccc",
        "target_branch": "feat/x",
        "target_remote": "origin",
    },
    {
        "event_type": "push_initiated",
        "remote_ref": "origin/feat/x",
        "run_id": "run-1",
        "cycle_id": "c1",
        "idempotency_key": "push:run-1:c1:aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa:feat/x",
        "pre_push_sha": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
        "target_sha": "cccccccccccccccccccccccccccccccccccccccc",
        "target_branch": "feat/x",
        "target_remote": "origin",
    },
    {
        "event_type": "push_completed",
        "run_id": "run-1",
        "cycle_id": "c1",
        "idempotency_key": "push:run-1:c1:aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa:feat/x",
        "pre_push_sha": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
        "target_sha": "cccccccccccccccccccccccccccccccccccccccc",
        "target_branch": "feat/x",
        "target_remote": "origin",
    },
]

_TRIAD_ARGS = {
    "run_id": "run-1",
    "cycle_id": "c1",
    "round_counter": 0,
    "pre_push_sha": SHA_A,
    "target_sha": SHA_C,
    "target_branch": "feat/x",
    "target_remote": "origin",
}


def _fix_decision():
    return evaluate_push_decision(
        monitor_ordinal=3,
        validation_status="validated",
        needs_human_decision=False,
        round_counter=0,
        max_rounds=2,
        applied_edits=1,
    )


def _sync_decision(tier=1):
    return c.evaluate_sync_decision(
        monitor_ordinal=3,
        validation_status="validated",
        tier=tier,
        conflict_max_tier=2,
        halt_reason=None,
        prior_conflict_cycles=0,
        round_counter=0,
        max_rounds=2,
    )


def test_triad_default_call_is_byte_identical_to_recorded_output():
    out = build_push_triad(**_TRIAD_ARGS, decision=_fix_decision())
    assert out == _RECORDED_TRIAD
    # Key order too: the JSONL bytes the run log writes are unchanged.
    assert json.dumps(out) == json.dumps(_RECORDED_TRIAD)


def test_triad_explicit_none_extras_equal_the_default_call():
    out = build_push_triad(
        **_TRIAD_ARGS,
        decision=_fix_decision(),
        push_kind=None,
        base_sha=None,
        review_terminal=None,
        expect_checks=None,
    )
    assert json.dumps(out) == json.dumps(_RECORDED_TRIAD)


def test_triad_sync_call_adds_kind_base_and_push_extras():
    decision = _sync_decision(tier=1)
    out = build_push_triad(
        **{**_TRIAD_ARGS, "cycle_id": "sync-1"},
        decision=decision,
        push_kind="sync",
        base_sha=SHA_B,
        review_terminal="clean",
        expect_checks=True,
    )
    assert [r["event_type"] for r in out] == [
        "push_decision",
        "push_initiated",
        "push_completed",
    ]
    for record in out:
        assert record["kind"] == "sync"
        assert record["base_sha"] == SHA_B
        # kind and base_sha follow target_remote.
        keys = list(record)
        assert keys[keys.index("target_remote") + 1 :] == ["kind", "base_sha"]
    dec, init, done = out
    assert "review_terminal" not in dec and "expect_checks" not in dec
    assert list(init)[:4] == [
        "event_type",
        "remote_ref",
        "review_terminal",
        "expect_checks",
    ]
    assert init["review_terminal"] == "clean" and init["expect_checks"] is True
    assert "review_terminal" not in done
    assert done["expect_checks"] is True
    assert dec["authorized"] is True


def test_triad_sync_decision_yields_the_four_p_predicates():
    decision = _sync_decision(tier=2)
    out = build_push_triad(
        **_TRIAD_ARGS, decision=decision, push_kind="merge", base_sha=SHA_B
    )
    assert out[0]["predicates"] == {
        "p1_ordinal": True,
        "p2_validated": True,
        "p3_tier_allowed": True,
        "p4_under_cap": True,
    }
    assert out[0]["predicates"] == decision.audit_predicates
    assert out[0]["predicates"] is not decision.audit_predicates
    assert all(r["kind"] == "merge" for r in out)
    assert "expect_checks" not in out[1] and "review_terminal" not in out[1]


def test_triad_each_optional_extra_is_independent():
    out = build_push_triad(**_TRIAD_ARGS, decision=_fix_decision(), push_kind="fix")
    assert all(r["kind"] == "fix" and "base_sha" not in r for r in out)
    out = build_push_triad(**_TRIAD_ARGS, decision=_fix_decision(), expect_checks=False)
    assert out[1]["expect_checks"] is False and out[2]["expect_checks"] is False
    assert all("kind" not in r for r in out)


@pytest.mark.parametrize("kind", ["", "Sync", "rebase", "push", 1])
def test_triad_invalid_push_kind_raises(kind):
    with pytest.raises(ValueError):
        build_push_triad(**_TRIAD_ARGS, decision=_fix_decision(), push_kind=kind)


def test_triad_decision_of_neither_shape_raises_attribute_error():
    class _Shapeless:
        authorized = True

    with pytest.raises(AttributeError):
        build_push_triad(**_TRIAD_ARGS, decision=_Shapeless())


# ---------------------------------------------------------------------------
# Purity
# ---------------------------------------------------------------------------

_ALLOWED_STDLIB = {"base64", "re", "dataclasses", "typing", "tomllib"}
_ALLOWED_INTERNAL = {"models": {"MonitorState"}, "fsm": {"run_validation_gates"}}


def test_conflicts_imports_only_allowed_modules():
    tree = ast.parse(CONFLICTS_PY.read_text(encoding="utf-8"))
    offenders: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name.split(".")[0] not in _ALLOWED_STDLIB:
                    offenders.append(f"import {alias.name}")
        elif isinstance(node, ast.ImportFrom):
            if node.level == 0:
                if (node.module or "").split(".")[0] not in _ALLOWED_STDLIB:
                    offenders.append(f"from {node.module} import ...")
            else:
                allowed = _ALLOWED_INTERNAL.get(node.module or "")
                names = {a.name for a in node.names}
                if node.level != 1 or allowed is None or not names <= allowed:
                    offenders.append(
                        f"from {'.' * node.level}{node.module} import {names}"
                    )
    assert not offenders, offenders


def test_conflicts_makes_no_io_or_dynamic_calls():
    tree = ast.parse(CONFLICTS_PY.read_text(encoding="utf-8"))
    banned = {"open", "__import__", "exec", "eval", "compile", "input", "print"}
    called = {
        node.func.id
        for node in ast.walk(tree)
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
    }
    assert not (called & banned)


def test_tomllib_import_is_guarded_for_python_3_10():
    """``import tomllib`` sits in a ``try`` whose ``ImportError`` handler binds
    ``tomllib = None``, so the module still imports on Python 3.10."""
    tree = ast.parse(CONFLICTS_PY.read_text(encoding="utf-8"))
    guarded = False
    for node in tree.body:
        if not isinstance(node, ast.Try):
            continue
        imports = [
            a.name
            for stmt in node.body
            if isinstance(stmt, ast.Import)
            for a in stmt.names
        ]
        handler_binds_none = any(
            isinstance(h.type, ast.Name)
            and h.type.id == "ImportError"
            and any(
                isinstance(s, ast.Assign)
                and [t.id for t in s.targets if isinstance(t, ast.Name)] == ["tomllib"]
                and isinstance(s.value, ast.Constant)
                and s.value.value is None
                for s in h.body
            )
            for h in node.handlers
        )
        guarded = guarded or (imports == ["tomllib"] and handler_binds_none)
    assert guarded


# ---------------------------------------------------------------------------
# Attempt directories (PR #378 review: a restart under the same cycle id)
# ---------------------------------------------------------------------------


def test_conflict_attempt_counts_sync_started_of_that_cycle_only():
    events = [
        {"event_type": "sync_started", "cycle_id": "conflict-1"},
        {"event_type": "sync_concluded", "cycle_id": "conflict-1"},
        {"event_type": "sync_started", "cycle_id": "sync-1"},
        {"event_type": "sync_started", "cycle_id": 7},
        "not an event",
        {"event_type": "sync_started", "cycle_id": "conflict-1", "resumed": True},
    ]
    assert c.conflict_attempt(events[:1], "conflict-1") == 1
    assert c.conflict_attempt(events, "conflict-1") == 2
    assert c.conflict_attempt(events, "sync-1") == 1


@pytest.mark.parametrize(
    "events, cycle_id",
    [
        ([], "sync-1"),
        ([{"event_type": "sync_concluded", "cycle_id": "sync-1"}], "sync-1"),
        ("not a list", "sync-1"),
        ([{"event_type": "sync_started", "cycle_id": "sync-1"}], None),
    ],
    ids=["empty", "no-start", "not-a-list", "non-string-id"],
)
def test_conflict_attempt_without_a_matching_start_raises(events, cycle_id):
    with pytest.raises(ValueError):
        c.conflict_attempt(events, cycle_id)


# ---------------------------------------------------------------------------
# Lock trust gate (PR #378 review, owner decision: halt Tier 1 before `uv lock`)
# ---------------------------------------------------------------------------

_needs_tomllib = pytest.mark.skipif(
    c.tomllib is None, reason="tomllib needs Python 3.11 or later"
)
_CLEAN_PYPROJECT = (
    '[project]\nname = "app"\nversion = "1.0"\ndependencies = ["requests>=2"]\n\n'
    '[build-system]\nrequires = ["hatchling"]\nbuild-backend = "hatchling.build"\n'
)


@_needs_tomllib
@pytest.mark.parametrize("value", ['["."]', "[]"], ids=["dot", "empty-list"])
def test_lock_trust_backend_path_is_a_finding(value):
    text = _CLEAN_PYPROJECT + f"backend-path = {value}\n"
    assert c.lock_trust_findings(text) == ["build-system.backend-path"]


@_needs_tomllib
def test_lock_trust_non_empty_dynamic_is_a_finding_and_empty_is_not():
    dynamic = _CLEAN_PYPROJECT.replace('version = "1.0"\n', 'dynamic = ["version"]\n')
    assert c.lock_trust_findings(dynamic) == ["project.dynamic"]
    empty = _CLEAN_PYPROJECT.replace(
        'version = "1.0"\n', 'version = "1"\ndynamic = []\n'
    )
    assert c.lock_trust_findings(empty) == []


@_needs_tomllib
@pytest.mark.parametrize(
    "sources",
    [
        '[tool.uv.sources]\nlib = { path = "../lib" }\n',
        '[tool.uv.sources.lib]\npath = "../lib"\n',
    ],
    ids=["inline-table", "table-header"],
)
def test_lock_trust_path_source_is_a_finding(sources):
    assert c.lock_trust_findings(_CLEAN_PYPROJECT + sources) == [
        "tool.uv.sources.lib (path)"
    ]


@_needs_tomllib
@pytest.mark.parametrize(
    "sources",
    [
        "[tool.uv.sources]\n"
        'lib = [{ path = "./lib", editable = true, marker = "sys_platform == \'linux\'" },'
        ' { index = "pypi", marker = "sys_platform != \'linux\'" }]\n',
        '[[tool.uv.sources.lib]]\npath = "./lib"\neditable = true\n'
        "marker = \"sys_platform == 'linux'\"\n"
        '[[tool.uv.sources.lib]]\nindex = "pypi"\n',
    ],
    ids=["inline-list", "array-of-tables"],
)
def test_lock_trust_editable_source_in_a_list_of_tables_is_a_finding(sources):
    assert c.lock_trust_findings(_CLEAN_PYPROJECT + sources) == [
        "tool.uv.sources.lib (path)",
        "tool.uv.sources.lib (editable)",
    ]


@_needs_tomllib
@pytest.mark.parametrize(
    "source",
    [
        '{ git = "https://example.com/lib.git", rev = "v1" }',
        '{ index = "pytorch" }',
        '{ url = "https://example.com/lib-1.0-py3-none-any.whl" }',
    ],
    ids=["git", "index", "url"],
)
def test_lock_trust_git_index_and_url_sources_are_not_findings(source):
    text = _CLEAN_PYPROJECT + f"[tool.uv.sources]\nlib = {source}\n"
    assert c.lock_trust_findings(text) == []


@_needs_tomllib
def test_lock_trust_clean_pyprojects_pass():
    assert c.lock_trust_findings(_CLEAN_PYPROJECT) == []
    assert c.lock_trust_findings("") == []
    repo_pyproject = (CONFLICTS_PY.parents[3] / "pyproject.toml").read_text(
        encoding="utf-8"
    )
    assert c.lock_trust_findings(repo_pyproject) == []


@_needs_tomllib
def test_lock_trust_reports_every_finding_in_a_fixed_order():
    text = (
        '[project]\nname = "app"\ndynamic = ["version"]\n\n'
        '[build-system]\nrequires = []\nbuild-backend = "be"\nbackend-path = ["."]\n\n'
        '[tool.uv.sources]\nb = { path = "b", editable = true }\na = { path = "a" }\n'
    )
    assert c.lock_trust_findings(text) == [
        "build-system.backend-path",
        "project.dynamic",
        "tool.uv.sources.a (path)",
        "tool.uv.sources.b (path)",
        "tool.uv.sources.b (editable)",
    ]


@_needs_tomllib
@pytest.mark.parametrize(
    "text",
    [
        "<<<<<<< ours\n[project]\n=======\n[project]\n>>>>>>> theirs\n",
        '[project]\nname = "a"\nname = "b"\n',
        "[project\n",
        "tool = 1\n",
        "build-system = 1\n",
        "project = 1\n",
        '[project]\ndynamic = "version"\n',
        "[tool]\nuv = 1\n",
        '[tool.uv]\nsources = "x"\n',
        '[tool.uv]\nsources = ["a"]\n',
        "[tool.uv.sources]\nlib = 1\n",
        '[tool.uv.sources]\nlib = ["x"]\n',
        '[tool.uv.sources]\nlib = { path = "a", editable = "yes" }\n',
    ],
    ids=[
        "conflict-markers",
        "duplicate-key",
        "unterminated-header",
        "tool-not-table",
        "build-system-not-table",
        "project-not-table",
        "dynamic-not-list",
        "uv-not-table",
        "sources-string",
        "sources-list",
        "source-int",
        "source-list-of-strings",
        "editable-not-bool",
    ],
)
def test_lock_trust_malformed_or_unexpected_shape_is_unreadable(text):
    assert c.lock_trust_findings(text) == [c.LOCK_TRUST_UNREADABLE]


@_needs_tomllib
def test_lock_trust_deeply_nested_input_is_unreadable_not_an_exception():
    text = "x = " + "[" * 100_000 + "]" * 100_000 + "\n"
    assert c.lock_trust_findings(text) == [c.LOCK_TRUST_UNREADABLE]


@pytest.mark.parametrize("value", [None, b"[project]\n", 1])
def test_lock_trust_non_string_input_is_unreadable(value):
    assert c.lock_trust_findings(value) == [c.LOCK_TRUST_UNREADABLE]


def test_lock_trust_without_a_toml_parser_is_unreadable(monkeypatch):
    monkeypatch.setattr(c, "tomllib", None)
    assert c.lock_trust_findings(_CLEAN_PYPROJECT) == [c.LOCK_TRUST_UNREADABLE]


@pytest.mark.skipif(c.tomllib is not None, reason="only Python 3.10 has no tomllib")
def test_lock_trust_on_python_3_10_fails_closed():
    assert c.lock_trust_findings(_CLEAN_PYPROJECT) == [c.LOCK_TRUST_UNREADABLE]
    trigger = _CLEAN_PYPROJECT + 'backend-path = ["."]\n'
    assert c.lock_trust_findings(trigger) == [c.LOCK_TRUST_UNREADABLE]

"""Panel run manifest: states, idempotency, resume, atomic publish and the `review manifest` commands."""

from __future__ import annotations

import copy
import hashlib
import json

import pytest
from click.testing import CliRunner

from superclaude.cli.main import main
from superclaude.cli.review import manifest as mf


def h(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()


def frozen(tree="tree-1", template="tpl-1"):
    return {
        "snapshot_ref": "artifacts/input-snapshot.yaml",
        "snapshot_sha256": h("snap"),
        "input_tree_sha256": h(tree),
        "template_sha256": h(template),
        "tiers_sha256": h("tiers"),
        "brief_template_sha256": h("brief"),
        "schema_ids": ["review-panel/1", "findings-v2"],
    }


def fresh(engine="shadow", **kw):
    return mf.new_manifest(
        run_id="r1",
        frozen=frozen(**kw),
        engine_requested=engine,
        engine_effective=engine,
    )


RESOLVED = {
    "reviewers_requested": 3,
    "reviewers_resolved": 3,
    "outputs": {"resolution.json": h("res")},
}


def walk(m, upto="published"):
    for stage in mf.STATES[1 : mf.STATES.index(upto) + 1]:
        payload = (
            RESOLVED
            if stage == "resolved"
            else {"outputs": {f"{stage}.json": h(stage)}}
        )
        mf.advance_stage(m, stage, payload)
    return m


# ------------------------------------------------------------ states and idempotency (AC1)


def test_a_new_manifest_carries_both_engines_and_validates():
    m = fresh()
    assert (m["t2_engine_requested"], m["t2_engine_effective"]) == ("shadow", "shadow")
    assert m["state"] == "frozen" and mf.validate(m) == []
    assert m["policy_sha256"] == mf.policy_sha256(m["frozen"])


@pytest.mark.parametrize("key", ["t2_engine_requested", "t2_engine_effective"])
def test_validate_fails_when_an_engine_is_missing(key):
    m = fresh()
    del m[key]
    assert any(key in e for e in mf.validate(m))
    m[key] = "turbo"
    assert any(key in e for e in mf.validate(m))


def test_all_states_are_advanced_in_order_with_none_skipped():
    m = walk(fresh())
    assert m["state"] == "published" and list(m["stages"]) == list(mf.STATES)
    assert mf.validate(m) == []
    assert (m["reviewers_requested"], m["reviewers_resolved"]) == (3, 3)


def test_replaying_an_identical_advance_is_a_no_op():
    m = walk(fresh(), "dispatched")
    before = copy.deepcopy(m)
    assert mf.advance_stage(m, "resolved", RESOLVED) is False
    assert (
        mf.advance_stage(
            m, "dispatched", {"outputs": {"dispatched.json": h("dispatched")}}
        )
        is False
    )
    assert m == before


def test_a_conflicting_payload_is_rejected():
    m = walk(fresh(), "dispatched")
    with pytest.raises(mf.Conflict):
        mf.advance_stage(m, "dispatched", {"outputs": {"dispatched.json": h("other")}})
    with pytest.raises(mf.Conflict):
        mf.advance_stage(m, "resolved", {**RESOLVED, "reviewers_resolved": 2})


@pytest.mark.parametrize("stage", ["dispatched", "published", "frozen", "collected"])
def test_an_out_of_order_state_is_rejected(stage):
    m = fresh()  # frozen: the only legal next stage is resolved
    with pytest.raises(mf.OutOfOrder):
        mf.advance_stage(m, stage, {})
    assert m["state"] == "frozen"


def test_resolved_needs_the_counts():
    m = fresh()
    with pytest.raises(mf.Invalid):
        mf.advance_stage(m, "resolved", {})
    with pytest.raises(mf.Invalid):
        mf.advance_stage(
            m, "resolved", {"reviewers_requested": 2, "reviewers_resolved": 3}
        )
    assert m["state"] == "frozen"


def test_outputs_must_be_sha256_values():
    m = walk(fresh(), "resolved")
    with pytest.raises(mf.Invalid):
        mf.advance_stage(m, "dispatched", {"outputs": {"x": "not-a-hash"}})


def test_a_failed_run_accepts_nothing_more():
    m = walk(fresh(), "resolved")
    mf.fail(m, "deadline")
    assert m["state"] == "failed" and m["failure_reason"] == "deadline"
    with pytest.raises(mf.OutOfOrder):
        mf.advance_stage(m, "dispatched", {})
    with pytest.raises(mf.OutOfOrder):
        mf.record_attempt(m, "dispatched", "t1b-1", "a1", "complete")


# ------------------------------------------------------------ attempts


def test_attempt_replay_is_a_no_op_and_a_different_payload_conflicts():
    m = walk(fresh(), "resolved")
    assert (
        mf.record_attempt(m, "dispatched", "t1b-1", "a1", "failed", {"why": "timeout"})
        is True
    )
    assert (
        mf.record_attempt(m, "dispatched", "t1b-1", "a1", "failed", {"why": "timeout"})
        is False
    )
    with pytest.raises(mf.Conflict):
        mf.record_attempt(m, "dispatched", "t1b-1", "a1", "failed", {"why": "other"})
    with pytest.raises(mf.Conflict):
        mf.record_attempt(
            m, "dispatched", "t1b-1", "a1", "complete", {"why": "timeout"}
        )


def test_a_new_attempt_supersedes_a_failed_one_without_adding_a_vote():
    m = walk(fresh(), "dispatched")
    mf.record_attempt(m, "collected", "t1b-1", "a1", "timed_out")
    mf.record_attempt(m, "collected", "t4-1", "a1", "complete")
    assert m["reviewers_complete"] == 1
    mf.record_attempt(m, "collected", "t1b-1", "a2", "complete")
    assert m["reviewers_complete"] == 2  # two reviewers, not three attempts
    assert [a.get("superseded_by") for a in m["attempts"]] == ["a2", None, None]
    with pytest.raises(mf.Conflict, match="add a vote"):
        mf.record_attempt(m, "collected", "t1b-1", "a3", "complete")
    assert m["reviewers_complete"] == 2


def test_attempts_are_recorded_only_while_their_stage_is_open():
    m = fresh()
    with pytest.raises(mf.OutOfOrder):
        mf.record_attempt(m, "collected", "t1b-1", "a1", "complete")
    with pytest.raises(mf.OutOfOrder):
        mf.record_attempt(m, "clustered", "t1b-1", "a1", "complete")
    walk(m, "dispatched")
    mf.record_attempt(m, "collected", "t1b-1", "a1", "complete")
    walk_rest = {"outputs": {"collected.json": h("c")}}
    mf.advance_stage(m, "collected", walk_rest)
    with pytest.raises(mf.OutOfOrder):  # collected is committed
        mf.record_attempt(m, "collected", "t4-1", "a1", "complete")
    assert (
        mf.record_attempt(m, "collected", "t1b-1", "a1", "complete") is False
    )  # identical replay


def test_attempt_inputs_are_checked():
    m = walk(fresh(), "resolved")
    with pytest.raises(mf.Invalid):
        mf.record_attempt(m, "dispatched", "t1b-1", "a1", "weird")
    with pytest.raises(mf.Invalid):
        mf.record_attempt(m, "dispatched", "", "a1", "complete")


# ------------------------------------------------------------ resume


def test_resume_reuses_the_manifest_when_the_frozen_fields_match():
    m = walk(fresh(), "dispatched")
    same, new = mf.resume(m, frozen=frozen())
    assert new is False and same is m
    assert mf.reusable_stages(m) == ["resolved", "dispatched"]


@pytest.mark.parametrize("change", [{"tree": "tree-2"}, {"template": "tpl-2"}])
def test_a_changed_plan_or_policy_hash_starts_a_new_invocation(change):
    m = walk(fresh(), "dispatched")
    new_m, new = mf.resume(m, frozen=frozen(**change))
    assert new is True
    assert new_m["invocation"] == 2 and new_m["state"] == "frozen"
    assert new_m["run_id"] == "r1" and new_m["t2_engine_requested"] == "shadow"
    assert new_m["history"] == [
        {
            "invocation": 1,
            "input_tree_sha256": m["input_tree_sha256"],
            "policy_sha256": m["policy_sha256"],
            "state": "dispatched",
        }
    ]
    assert list(new_m["stages"]) == ["frozen"] and mf.validate(new_m) == []


def test_resume_refuses_another_run_and_a_changed_engine_starts_a_new_invocation():
    m = walk(fresh(), "dispatched")
    with pytest.raises(mf.Conflict, match="r1"):
        mf.resume(m, frozen=frozen(), run_id="r2")
    same, new = mf.resume(
        m,
        frozen=frozen(),
        run_id="r1",
        engine_requested="shadow",
        engine_effective="shadow",
    )
    assert new is False and same is m
    changed, new = mf.resume(
        m,
        frozen=frozen(),
        run_id="r1",
        engine_requested="shadow",
        engine_effective="legacy",
    )
    assert (
        new is True
        and changed["t2_engine_effective"] == "legacy"
        and changed["invocation"] == 2
    )


def test_fail_keeps_the_first_reason():
    m = walk(fresh(), "resolved")
    mf.fail(m, "a")
    mf.fail(m, "b")
    assert m["failure_reason"] == "a"


def test_a_stage_is_reusable_only_while_its_dependency_hashes_match():
    m = walk(fresh(), "calibrated")
    assert mf.reusable_stages(m) == list(
        mf.STATES[1 : mf.STATES.index("calibrated") + 1]
    )
    m["stages"]["dispatched"]["deps"]["prev"] = h("tampered")
    assert mf.reusable_stages(m) == ["resolved"]
    m["stages"]["resolved"]["deps"]["input_tree_sha256"] = h("old input")
    assert mf.reusable_stages(m) == []


# ------------------------------------------------------------ publish


def contents():
    return {n: f"{n} body\n".encode() for n in mf.PUBLISH_FILES}


def test_publish_renames_the_three_files_then_commits(tmp_path):
    path = tmp_path / "panel" / "manifest.json"
    m = walk(fresh("panel"), "validated")
    mf.save(path, m)
    hashes = mf.publish_files(tmp_path, contents(), path)
    committed = mf.read_committed(path)
    assert committed["state"] == "published"
    assert committed["stages"]["published"]["outputs"] == hashes
    assert {n: (tmp_path / n).read_bytes() for n in mf.PUBLISH_FILES} == contents()
    assert not [p for p in tmp_path.iterdir() if ".tmp-" in p.name]


def test_a_crash_between_rename_and_commit_leaves_a_manifest_readers_refuse(tmp_path):
    path = tmp_path / "panel" / "manifest.json"
    mf.save(path, walk(fresh("panel"), "validated"))

    def crash(manifest_path, hashes):
        raise RuntimeError("crash before commit")

    with pytest.raises(RuntimeError):
        mf.publish_files(tmp_path, contents(), path, commit=crash)
    assert all((tmp_path / n).exists() for n in mf.PUBLISH_FILES)  # renamed
    assert mf.load(path)["state"] == "validated"  # not committed
    with pytest.raises(mf.NotCommitted):
        mf.read_committed(path)
    # recovery: the same publish can run again and commits
    mf.publish_files(tmp_path, contents(), path)
    assert mf.read_committed(path)["state"] == "published"


def _tree(path):
    return {p.name: p.read_bytes() for p in path.iterdir() if p.is_file()}


def test_publish_checks_the_manifest_before_touching_any_file(tmp_path):
    path = tmp_path / "panel" / "manifest.json"
    for n in mf.PUBLISH_FILES:
        (tmp_path / n).write_text("legacy")
    legacy = _tree(tmp_path)
    # not yet validated
    mf.save(path, walk(fresh("panel"), "debated"))
    with pytest.raises(mf.OutOfOrder, match="validated"):
        mf.publish_files(tmp_path, contents(), path)
    assert _tree(tmp_path) == legacy
    # shadow engine: the legacy writers own the files
    mf.save(path, walk(fresh("shadow"), "validated"))
    with pytest.raises(mf.OutOfOrder, match="shadow"):
        mf.publish_files(tmp_path, contents(), path)
    assert _tree(tmp_path) == legacy


def test_publishing_twice_is_a_no_op_and_different_files_conflict_before_writing(
    tmp_path,
):
    path = tmp_path / "panel" / "manifest.json"
    mf.save(path, walk(fresh("panel"), "validated"))
    mf.publish_files(tmp_path, contents(), path)
    published = _tree(tmp_path)
    assert mf.publish_files(tmp_path, contents(), path)  # identical replay
    different = {n: b"other" for n in mf.PUBLISH_FILES}
    with pytest.raises(mf.Conflict):
        mf.publish_files(tmp_path, different, path)
    assert _tree(tmp_path) == published
    committed = mf.read_committed(path)
    assert committed["stages"]["published"]["outputs"] == {
        n: hashlib.sha256(published[n]).hexdigest() for n in mf.PUBLISH_FILES
    }


def test_shadow_publish_records_the_hashes_and_rewrites_nothing(tmp_path):
    for n, data in contents().items():
        (tmp_path / n).write_bytes(data)
    stat = {n: (tmp_path / n).stat().st_mtime_ns for n in mf.PUBLISH_FILES}
    hashes = mf.hash_published_files(tmp_path)
    m = walk(fresh(), "validated")
    mf.advance_stage(m, "published", {"outputs": hashes})
    assert {n: (tmp_path / n).stat().st_mtime_ns for n in mf.PUBLISH_FILES} == stat
    assert m["stages"]["published"]["outputs"] == {
        n: hashlib.sha256(d).hexdigest() for n, d in contents().items()
    }
    (tmp_path / "audit.log").unlink()
    with pytest.raises(mf.Invalid, match="audit.log"):
        mf.hash_published_files(tmp_path)


def test_save_is_atomic_and_load_rejects_garbage(tmp_path):
    path = tmp_path / "panel" / "manifest.json"
    mf.save(path, fresh())
    assert not [p for p in path.parent.iterdir() if ".tmp-" in p.name]
    path.write_text("{ not json")
    with pytest.raises(mf.Invalid):
        mf.load(path)


# ------------------------------------------------------------ commands


def run(*args):
    return CliRunner().invoke(main, ["review", "manifest", *args])


@pytest.fixture
def cli_run(tmp_path):
    snap = tmp_path / "input-snapshot.yaml"
    snap.write_text(f"input_tree_sha256: {h('tree-1')}\nfile_list: []\n")
    return tmp_path, snap


def init_args(tmp_path, snap, **over):
    opts = {
        "--out": str(tmp_path), "--run-id": "r1", "--snapshot": str(snap),
        "--template-sha256": h("tpl"), "--tiers-sha256": h("tiers"), "--brief-template-sha256": h("brief"),
        "--t2-engine-requested": "shadow", "--t2-engine-effective": "shadow",
    }  # fmt: skip
    opts.update(over)
    args = [x for kv in opts.items() for x in kv]
    return [*args, "--schema-id", "review-panel/1"]


def test_init_on_an_existing_manifest_checks_run_id_and_engines(cli_run):
    tmp, snap = cli_run
    assert run("init", *init_args(tmp, snap)).exit_code == 0
    other = run("init", *init_args(tmp, snap, **{"--run-id": "r2"}))
    assert other.exit_code == 1 and "Conflict" in other.output
    assert json.loads((tmp / "panel/manifest.json").read_text())["run_id"] == "r1"
    engines = {"--t2-engine-requested": "legacy", "--t2-engine-effective": "legacy"}
    res = json.loads(run("init", *init_args(tmp, snap, **engines)).output)
    assert res["result"] == "new-invocation" and res["invocation"] == 2
    data = json.loads((tmp / "panel/manifest.json").read_text())
    assert (data["t2_engine_requested"], data["t2_engine_effective"]) == (
        "legacy",
        "legacy",
    )


def test_cli_publish_from_refuses_in_shadow_mode_and_before_validated(cli_run):
    tmp, snap = cli_run
    run("init", *init_args(tmp, snap))  # shadow / shadow
    staging = tmp / "staging"
    staging.mkdir()
    for n, data in contents().items():
        (staging / n).write_bytes(data)
    res = run(
        "advance",
        "--out",
        str(tmp),
        "--stage",
        "published",
        "--publish-from",
        str(staging),
    )
    assert res.exit_code == 1 and "OutOfOrder" in res.output
    assert not [n for n in mf.PUBLISH_FILES if (tmp / n).exists()]


def test_help_lists_the_three_subcommands():
    res = run("--help")
    assert res.exit_code == 0
    for name in ("init", "advance", "validate"):
        assert name in res.output
    assert "manifest" in CliRunner().invoke(main, ["review", "--help"]).output


def test_init_carries_both_engines_and_validate_fails_when_one_is_missing(cli_run):
    tmp, snap = cli_run
    res = run("init", *init_args(tmp, snap))
    assert res.exit_code == 0, res.output
    path = tmp / "panel/manifest.json"
    data = json.loads(path.read_text())
    assert (data["t2_engine_requested"], data["t2_engine_effective"]) == (
        "shadow",
        "shadow",
    )
    assert run("validate", "--out", str(tmp)).exit_code == 0
    del data["t2_engine_effective"]
    path.write_text(json.dumps(data))
    bad = run("validate", "--out", str(tmp))
    assert bad.exit_code == 1 and "t2_engine_effective" in bad.output


def test_init_requires_both_engine_values(cli_run):
    tmp, snap = cli_run
    args = init_args(tmp, snap)
    i = args.index("--t2-engine-effective")
    res = run("init", *args[:i], *args[i + 2 :])
    assert res.exit_code == 2 and "t2-engine-effective" in res.output
    assert not (tmp / "panel/manifest.json").exists()


def test_init_twice_reuses_and_a_changed_snapshot_starts_a_new_invocation(cli_run):
    tmp, snap = cli_run
    assert json.loads(run("init", *init_args(tmp, snap)).output)["result"] == "created"
    assert json.loads(run("init", *init_args(tmp, snap)).output)["result"] == "reused"
    snap.write_text(f"input_tree_sha256: {h('tree-2')}\nfile_list: []\n")
    res = json.loads(run("init", *init_args(tmp, snap)).output)
    assert res == {"result": "new-invocation", "state": "frozen", "invocation": 2}


def test_advance_flow_with_replay_conflict_and_out_of_order(cli_run):
    tmp, snap = cli_run
    run("init", *init_args(tmp, snap))
    payload = tmp / "resolved.json"
    payload.write_text(json.dumps(RESOLVED))
    out = ["--out", str(tmp)]
    first = run("advance", *out, "--stage", "resolved", "--payload", str(payload))
    assert json.loads(first.output) == {"result": "advanced", "state": "resolved"}
    again = run("advance", *out, "--stage", "resolved", "--payload", str(payload))
    assert json.loads(again.output)["result"] == "noop"
    payload.write_text(json.dumps({**RESOLVED, "reviewers_resolved": 2}))
    conflict = run("advance", *out, "--stage", "resolved", "--payload", str(payload))
    assert conflict.exit_code == 1 and "Conflict" in conflict.output
    skip = run("advance", *out, "--stage", "collected")
    assert skip.exit_code == 1 and "OutOfOrder" in skip.output
    attempt = run(
        "advance",
        *out,
        "--stage",
        "dispatched",
        "--reviewer-id",
        "t1b-1",
        "--attempt-id",
        "a1",
        "--completion",
        "complete",
    )
    assert attempt.exit_code == 0, attempt.output
    half = run("advance", *out, "--stage", "dispatched", "--reviewer-id", "t1b-1")
    assert half.exit_code != 0


def test_cli_publish_in_shadow_mode_records_hashes_of_the_legacy_files(cli_run):
    tmp, snap = cli_run
    run("init", *init_args(tmp, snap))
    payload = tmp / "resolved.json"
    payload.write_text(json.dumps(RESOLVED))
    out = ["--out", str(tmp)]
    run("advance", *out, "--stage", "resolved", "--payload", str(payload))
    for stage in mf.STATES[2:-1]:
        assert run("advance", *out, "--stage", stage).exit_code == 0
    early = run("advance", *out, "--stage", "published")
    assert (
        early.exit_code == 1 and "REPORT.md" in early.output
    )  # legacy files not written yet
    for n, data in contents().items():
        (tmp / n).write_bytes(data)
    done = run("advance", *out, "--stage", "published")
    assert done.exit_code == 0, done.output
    assert {n: (tmp / n).read_bytes() for n in mf.PUBLISH_FILES} == contents()
    assert run("validate", *out, "--require-published").exit_code == 0
    assert mf.read_committed(tmp / "panel/manifest.json")["state"] == "published"


def test_cli_publish_from_a_staging_directory_uses_temporaries_and_renames(cli_run):
    tmp, snap = cli_run
    run(
        "init",
        *init_args(
            tmp,
            snap,
            **{"--t2-engine-requested": "panel", "--t2-engine-effective": "panel"},
        ),
    )
    payload = tmp / "resolved.json"
    payload.write_text(json.dumps(RESOLVED))
    out = ["--out", str(tmp)]
    run("advance", *out, "--stage", "resolved", "--payload", str(payload))
    for stage in mf.STATES[2:-1]:
        run("advance", *out, "--stage", stage)
    staging = tmp / "staging"
    staging.mkdir()
    for n, data in contents().items():
        (staging / n).write_bytes(data)
    done = run("advance", *out, "--stage", "published", "--publish-from", str(staging))
    assert done.exit_code == 0, done.output
    assert {n: (tmp / n).read_bytes() for n in mf.PUBLISH_FILES} == contents()
    assert not [p for p in tmp.iterdir() if ".tmp-" in p.name]


def test_failed_stage_and_validate_require_published(cli_run):
    tmp, snap = cli_run
    run("init", *init_args(tmp, snap))
    res = run("advance", "--out", str(tmp), "--stage", "failed", "--reason", "deadline")
    assert json.loads(res.output)["state"] == "failed"
    assert run("validate", "--out", str(tmp)).exit_code == 0
    assert run("validate", "--out", str(tmp), "--require-published").exit_code == 1


def test_validate_reports_an_unreadable_manifest(tmp_path):
    res = run("validate", "--out", str(tmp_path))
    assert res.exit_code == 1

"""Raw transport text and saved output policy survive fresh and resumed runs."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest
import yaml
from click.testing import CliRunner

from superclaude.cli.swarm.commands import _build_spec_from_lens, run_cmd
from superclaude.cli.swarm.models import WorkerResult


@pytest.mark.parametrize("retention", ["default", "disabled", "disabled-stale"])
@pytest.mark.parametrize(
    ("body_kind", "status", "body"),
    [
        ("success", "success", "## Verdict\nKeep café intact.\r\n\n"),
        ("parse-error", "parse_error", "unstructured café\r\n\n"),
        ("empty", "success", ""),
        ("missing", "success", None),
        ("nonstring", "success", 42),
    ],
)
def test_fresh_run_raw_retention_at_contract_emission(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    retention: str,
    body_kind: str,
    status: str,
    body: Any,
) -> None:
    """Check disk before emission, using real preflight, normalize and reduce."""
    import superclaude.cli.swarm.dispatch as dispatch_mod
    import superclaude.cli.swarm.reduce as reduce_mod

    target = tmp_path / "target.py"
    target.write_text("# A real review target with enough content.\n" * 4)
    output = tmp_path / "out"
    spec = _build_spec_from_lens("bare-review")
    spec["target"]["path"] = str(target)
    spec["output"]["dir"] = str(output)
    spec["workers"]["count"] = 1
    spec["workers"]["models"] = ["fixture-model"]
    spec["transport"]["kind"] = "stub"
    if retention != "default":
        spec["normalization"]["on_parse_error"]["retain_raw"] = False
    raw_file = output / "bare-review-00-fixture-model.raw.md"
    if retention == "disabled-stale":
        output.mkdir()
        raw_file.write_bytes(b"previous run body\n")

    def fake_dispatch(*args: Any, **kwargs: Any) -> list[WorkerResult]:
        worker = WorkerResult(index=0, model_id="fixture-model", status=status)
        if body_kind != "missing":
            worker.body = body
        return [worker]

    real_emit = reduce_mod.emit_contract
    observed = []

    def check_emit(contract: Any, directory: Path) -> Path:
        observed.append(contract)
        assert len(contract.output_files) == 1
        worker = contract.output_files[0]
        assert worker.status == status
        assert Path(worker.meta_path).is_file()
        if body_kind == "success":
            assert Path(worker.final_path).is_file()
        if retention != "default" or not isinstance(body, str):
            assert worker.raw_path == ""
        else:
            assert worker.raw_path == str(raw_file)
            assert raw_file.read_bytes() == body.encode("utf-8")
        if retention == "disabled":
            assert not raw_file.exists()
        if retention == "disabled-stale":
            assert raw_file.read_bytes() == b"previous run body\n"
        return real_emit(contract, directory)

    monkeypatch.setattr(dispatch_mod, "dispatch_wave1", fake_dispatch)
    monkeypatch.setattr(reduce_mod, "emit_contract", check_emit)
    result = CliRunner().invoke(
        run_cmd, ["--stdin", "--output", str(output)], input=json.dumps(spec)
    )
    if result.exception is not None:
        raise result.exception
    assert result.exit_code == 0, result.output
    assert len(observed) == 1


def _persist_resume_job(
    tmp_path: Path, *, retain_raw: bool = True, custom_names: bool = False
) -> tuple[Path, str, str]:
    """Persist the real Wave-0 manifest, not a fabricated recovery policy."""
    from superclaude.cli.swarm.preflight import run_preflight

    target = tmp_path / "target.py"
    target.write_text("# Review this real target.\n" * 8, encoding="utf-8")
    output = tmp_path / "out"
    spec = _build_spec_from_lens("bare-review")
    spec["target"]["path"] = str(target)
    spec["output"]["dir"] = str(output)
    spec["workers"]["count"] = 4
    spec["workers"]["models"] = [f"fixture-model-{i}" for i in range(4)]
    spec["transport"]["kind"] = "stub"
    spec["normalization"]["on_parse_error"]["retain_raw"] = retain_raw
    lens = "saved-review" if custom_names else "bare-review"
    template = "{lens}-{index:02d}-saved-{model_slug}.md"
    if custom_names:
        spec["output"]["lens_name"] = lens
        spec["output"]["filename_template"] = template
    result = run_preflight(spec, output_dir=output)
    return output, result.manifest.job_id, lens


def _seed_resume_slot(output: Path, index: int, lens: str) -> None:
    """Simulate a completed worker, including the actual sibling inventory."""
    stem = f"{lens}-{index:02d}-fixture-model-{index}"
    body = f"## Verdict\nPrior café body {index}.\r\n\n".encode()
    (output / f"{stem}.raw.md").write_bytes(body)
    (output / f"{stem}.final.md").write_bytes(body)
    (output / f"{stem}.meta.json").write_text(
        json.dumps({"status": "success", "bytes": len(body)}), encoding="utf-8"
    )


@pytest.mark.parametrize("force_relens", [False, True])
@pytest.mark.parametrize("retain_raw", [True, False])
def test_resume_restores_persisted_retention_and_naming(
    tmp_path: Path, force_relens: bool, retain_raw: bool
) -> None:
    from superclaude.cli.swarm.preflight import resume_mode

    output, _, lens = _persist_resume_job(
        tmp_path, retain_raw=retain_raw, custom_names=True
    )
    recovered = resume_mode(output / "manifest.json", force_relens=force_relens)
    assert recovered.normalization.on_parse_error.retain_raw is retain_raw
    assert recovered.output.lens_name == lens
    assert (
        recovered.output.filename_template == "{lens}-{index:02d}-saved-{model_slug}.md"
    )


@pytest.mark.parametrize("retain_raw", [True, False])
def test_completed_resume_preserves_raw_inventory_at_emission(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, retain_raw: bool
) -> None:
    import superclaude.cli.swarm.dispatch as dispatch_mod
    import superclaude.cli.swarm.reduce as reduce_mod

    output, job_id, lens = _persist_resume_job(tmp_path, retain_raw=retain_raw)
    for index in range(4):
        _seed_resume_slot(output, index, lens)
    before = {p.name: p.read_bytes() for p in output.iterdir() if p.suffix != ".yaml"}

    def unexpected_dispatch(*args: Any, **kwargs: Any) -> Any:
        pytest.fail("completed workers must not be redispatched")

    real_emit = reduce_mod.emit_contract
    observed = []

    def check_emit(contract: Any, directory: Path) -> Path:
        observed.append(contract)
        assert len(contract.output_files) == 4
        for worker in contract.output_files:
            if retain_raw:
                assert (
                    Path(worker.raw_path).read_bytes()
                    == before[Path(worker.raw_path).name]
                )
            else:
                assert worker.raw_path == ""
        return real_emit(contract, directory)

    monkeypatch.setattr(dispatch_mod, "dispatch_wave1", unexpected_dispatch)
    monkeypatch.setattr(reduce_mod, "emit_contract", check_emit)
    result = CliRunner().invoke(run_cmd, ["--resume", job_id, "--output", str(output)])
    if result.exception is not None:
        raise result.exception
    assert result.exit_code == 0, result.output
    assert len(observed) == 1
    for name, data in before.items():
        if name.endswith((".raw.md", ".final.md", ".meta.json", "manifest.json")):
            assert (output / name).read_bytes() == data


@pytest.mark.parametrize("force_relens", [False, True])
@pytest.mark.parametrize(
    "policy", ["enabled-custom", "disabled", "historical", "disabled-custom-context"]
)
def test_partial_resume_retains_original_slot_paths(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    force_relens: bool,
    policy: str,
) -> None:
    import dataclasses

    import superclaude.cli.swarm.dispatch as dispatch_mod
    import superclaude.cli.swarm.preflight as preflight_mod
    import superclaude.cli.swarm.reduce as reduce_mod
    from superclaude.cli.swarm.lenses import LENSES
    from superclaude.cli.swarm.models import CallerMetadata

    combined = policy == "disabled-custom-context"
    custom = policy == "enabled-custom" or combined
    disabled = policy == "disabled" or combined
    if combined:
        real_preflight = preflight_mod.run_preflight

        def accepted_preflight(spec: Any, **kwargs: Any) -> Any:
            spec["caller"] = {
                "skill": "context-test",
                "skill_version": "1.0",
                "invocation_label": "accepted",
                "kind": "cli",
            }
            spec["target"]["truncation"]["line_cap"] = 3
            spec["recommended_next_command_template"] = (
                "inspect {job_id} {suspect_files} {compare_files}"
            )
            spec["recommended_next_command_substitutions"] = {
                "job_id": "accepted-job",
                "suspect_files": "accepted-files",
                "compare_files": "accepted-compare",
            }
            return real_preflight(
                spec,
                caller_metadata_override=CallerMetadata(suspect=False, tier="T1"),
                **kwargs,
            )

        monkeypatch.setattr(preflight_mod, "run_preflight", accepted_preflight)
    output, job_id, lens = _persist_resume_job(
        tmp_path, retain_raw=not disabled, custom_names=custom
    )
    manifest_path = output / "manifest.json"
    if combined:
        accepted = json.loads(manifest_path.read_text(encoding="utf-8"))
        assert isinstance(accepted["caller"], dict), "accepted caller must be persisted"
        assert isinstance(accepted["target"], dict), "accepted target must be persisted"
        assert accepted["caller"]["invocation_label"] == "accepted"
        assert accepted["caller_metadata"] == {"suspect": False, "tier": "T1"}
        assert accepted["target"]["truncated"] is True
        assert accepted["target"]["truncation_line_cap"] == 3
        assert accepted["lens_source"] == "registry"
        assert accepted["retain_raw"] is False
        assert accepted["output_lens_name"] == lens
        live = dataclasses.replace(
            LENSES["bare-review"],
            recommended_next_command_template="live {job_id} {suspect_files}",
        )
        monkeypatch.setattr(preflight_mod, "resolve_lens", lambda _: live)
        recovered = preflight_mod.resume_mode(manifest_path, force_relens=force_relens)
        assert dataclasses.asdict(recovered.caller) == accepted["caller"]
        assert recovered.target.path == accepted["target"]["path"]
        assert recovered.target.truncation.line_cap == 3
        assert (
            recovered.recommended_next_command_substitutions
            == accepted["recommended_next_command_substitutions"]
        )
        assert recovered.normalization.on_parse_error.retain_raw is False
        assert recovered.output.lens_name == lens
        assert (
            recovered.output.filename_template == accepted["output_filename_template"]
        )
        expected_template = (
            live.recommended_next_command_template
            if force_relens
            else accepted["recommended_next_command_template"]
        )
        assert recovered.recommended_next_command_template == expected_template
    if policy == "historical":
        manifest_path = output / "manifest.json"
        payload = json.loads(manifest_path.read_text(encoding="utf-8"))
        # Keep only fields present before durable retention/naming recovery.
        original_fields = {
            "contract_version",
            "job_id",
            "resolved_lens_entry",
            "preflight",
            "caller_metadata",
        }
        payload = {
            key: value for key, value in payload.items() if key in original_fields
        }
        manifest_path.write_text(json.dumps(payload), encoding="utf-8")
    manifest_before = manifest_path.read_bytes()
    for index in (0, 2):
        _seed_resume_slot(output, index, lens)
    preserved = {
        p.name: p.read_bytes()
        for p in output.iterdir()
        if p.name.endswith((".raw.md", ".final.md", ".meta.json"))
    }
    bodies = {
        1: "## Verdict\nResumed café one.\r\n\n",
        3: "## Verdict\nResumed three.\n",
    }
    dispatched = []

    def fake_dispatch(preflight_result: Any, **kwargs: Any) -> list[WorkerResult]:
        assert preflight_result.manifest.preflight.workers_requested == 2
        dispatched.append(True)
        workers = []
        for position, original in enumerate((1, 3)):
            worker = WorkerResult(
                index=position, model_id=f"fixture-model-{original}", status="success"
            )
            worker.body = bodies[original]
            workers.append(worker)
        return workers

    real_emit = reduce_mod.emit_contract
    observed = []

    def check_emit(contract: Any, directory: Path) -> Path:
        observed.append(contract)
        assert [worker.index for worker in contract.output_files] == [0, 1, 2, 3]
        if combined:
            assert contract.lens == "bare-review"
            assert contract.lens_source == "registry"
            assert dataclasses.asdict(contract.caller) == accepted["caller"]
            assert (
                dataclasses.asdict(contract.caller_metadata)
                == accepted["caller_metadata"]
            )
            assert dataclasses.asdict(contract.target) == accepted["target"]
            assert contract.recommended_next_command == (
                "live accepted-job accepted-files"
                if force_relens
                else "inspect accepted-job accepted-files accepted-compare"
            )
            for worker in contract.output_files:
                if worker.index in bodies:
                    stem = (
                        f"{lens}-{worker.index:02d}-saved-fixture-model-{worker.index}"
                    )
                    assert worker.final_path == str(output / f"{stem}.final.md")
                    assert worker.meta_path == str(output / f"{stem}.meta.json")
        # Check the raw seam first; absent final/meta should not mask the defect.
        for worker in contract.output_files:
            if disabled:
                assert worker.raw_path == "", (
                    "disabled resumed retention advertises nothing"
                )
            elif worker.index in bodies:
                extra = "saved-" if custom else ""
                stem = f"{lens}-{worker.index:02d}-{extra}fixture-model-{worker.index}"
                expected = output / f"{stem}.raw.md"
                assert worker.raw_path == str(expected), (
                    "resume must restore original naming and slot indexes"
                )
                assert expected.read_bytes() == bodies[worker.index].encode("utf-8")
            else:
                assert Path(worker.raw_path).is_file()
        for worker in contract.output_files:
            assert Path(worker.final_path).is_file()
            assert Path(worker.meta_path).is_file()
        assert {name: (output / name).read_bytes() for name in preserved} == preserved
        if disabled:
            assert {p.name for p in output.glob("*.raw.md")} == {
                name for name in preserved if name.endswith(".raw.md")
            }
        return real_emit(contract, directory)

    monkeypatch.setattr(dispatch_mod, "dispatch_wave1", fake_dispatch)
    monkeypatch.setattr(reduce_mod, "emit_contract", check_emit)
    args = ["--resume", job_id, "--output", str(output)]
    if force_relens:
        args.append("--force-relens")
    result = CliRunner().invoke(run_cmd, args)
    if result.exception is not None:
        raise result.exception
    assert result.exit_code == 0, result.output
    assert dispatched == [True]
    assert len(observed) == 1
    assert manifest_path.read_bytes() == manifest_before


@pytest.mark.parametrize("force_relens", [False, True])
def test_resume_preserves_explicit_empty_output_lens(tmp_path, force_relens):
    from superclaude.cli.swarm.preflight import resume_mode

    output, _, _ = _persist_resume_job(tmp_path)
    path = output / "manifest.json"
    payload = json.loads(path.read_text())
    payload["output_lens_name"] = ""
    path.write_text(json.dumps(payload))
    assert resume_mode(path, force_relens=force_relens).output.lens_name == ""


@pytest.mark.parametrize("inventory", ["missing", "directory"])
def test_discovered_raw_path_requires_a_file(tmp_path, inventory):
    from superclaude.cli.swarm.commands import discover_succeeded_slots

    output, _, lens = _persist_resume_job(tmp_path)
    stem = f"{lens}-00-fixture-model-0"
    (output / f"{stem}.meta.json").write_text(json.dumps({"status": "success"}))
    if inventory == "directory":
        (output / f"{stem}.raw.md").mkdir()
    assert discover_succeeded_slots(output, 4)[0].raw_path == ""


@pytest.mark.parametrize("escape", ["parent", "symlink"])
def test_shared_worker_paths_reject_output_escape(tmp_path: Path, escape: str) -> None:
    from superclaude.cli.swarm.commands import _stamp_inline_worker_paths
    from superclaude.cli.swarm.state import OutputConfinementError

    output = tmp_path / "out"
    output.mkdir()
    outside = tmp_path / "outside"
    outside.mkdir()
    if escape == "symlink":
        (output / "linked").symlink_to(outside, target_is_directory=True)
        template = "linked/{lens}-{index:02d}-{model_slug}.md"
    else:
        template = "../outside/{lens}-{index:02d}-{model_slug}.md"
    worker = WorkerResult(index=0, model_id="fixture-model", status="success")
    worker.body = "## Verdict\nDo not write outside the output directory.\n"
    with pytest.raises(OutputConfinementError):
        _stamp_inline_worker_paths([worker], output, "bare-review", template)
    assert list(outside.iterdir()) == []


@pytest.mark.parametrize("force_relens", [False, True])
@pytest.mark.parametrize("retain_raw", [False, True])
@pytest.mark.parametrize(
    "template",
    [
        "nested/{lens}/{index:02d}-{model_slug}.md",
        "audit-17-{model_slug}-{lens}-slot-{index:02d}.md",
    ],
)
def test_resume_discovers_saved_custom_layout(
    tmp_path, monkeypatch, force_relens, retain_raw, template
):
    output, job_id, lens = _persist_resume_job(tmp_path, retain_raw=retain_raw)
    manifest_path = output / "manifest.json"
    manifest = json.loads(manifest_path.read_text())
    manifest["output_filename_template"] = template
    manifest_path.write_text(json.dumps(manifest))
    for index in (0, 2):
        _seed_resume_slot(output, index, lens)
        old = f"{lens}-{index:02d}-fixture-model-{index}"
        new = template.format(
            lens=lens, index=index, model_slug=f"fixture-model-{index}"
        )[:-3]
        for suffix in (".raw.md", ".final.md", ".meta.json"):
            destination = output / f"{new}{suffix}"
            destination.parent.mkdir(parents=True, exist_ok=True)
            (output / f"{old}{suffix}").rename(destination)
    preserved = {
        p.relative_to(output): p.read_bytes() for p in output.rglob("*") if p.is_file()
    }
    dispatched = []

    def captured_dispatch(preflight_result, **kwargs):
        dispatched.append(preflight_result.manifest.preflight.workers_requested)
        assert dispatched == [2], "only incomplete original slots may be dispatched"
        workers = []
        for position, original in enumerate((1, 3)):
            worker = WorkerResult(
                index=position, model_id=f"fixture-model-{original}", status="success"
            )
            worker.body = f"## Verdict\nResumed slot {original}.\n"
            workers.append(worker)
        return workers

    monkeypatch.setattr(
        "superclaude.cli.swarm.dispatch.dispatch_wave1", captured_dispatch
    )
    args = ["--resume", job_id, "--output", str(output)]
    if force_relens:
        args.append("--force-relens")
    result = CliRunner().invoke(run_cmd, args)
    assert result.exit_code == 0, result.output
    assert dispatched == [2]
    contract = yaml.safe_load((output / "return-contract.yaml").read_text())
    assert [w["index"] for w in contract["output_files"]] == [0, 1, 2, 3]
    for worker in contract["output_files"]:
        assert bool(worker["raw_path"]) is retain_raw
        if worker["index"] in (1, 3):
            expected = template.format(
                lens=lens,
                index=worker["index"],
                model_slug=f"fixture-model-{worker['index']}",
            )[:-3]
            assert worker["final_path"] == str(output / f"{expected}.final.md")
    assert {p: (output / p).read_bytes() for p in preserved} == preserved


@pytest.mark.parametrize("force_relens", [False, True])
@pytest.mark.parametrize("retain_raw", [True, False])
def test_custom_resume_normalization_preserves_provenance_and_retention(
    tmp_path, monkeypatch, force_relens, retain_raw
):
    from superclaude.cli.swarm import preflight as preflight_mod

    real_preflight = preflight_mod.run_preflight

    def accepted_recipe(spec, **kwargs):
        spec["normalization"]["recipe_args"] = {
            "caller_label": "accepted-retention-label",
            "target_truncated": False,
        }
        return real_preflight(spec, **kwargs)

    monkeypatch.setattr(preflight_mod, "run_preflight", accepted_recipe)
    output, job_id, lens = _persist_resume_job(
        tmp_path, retain_raw=retain_raw, custom_names=True
    )
    manifest_bytes = (output / "manifest.json").read_bytes()
    manifest = json.loads(manifest_bytes)
    for index in (0, 2):
        _seed_resume_slot(output, index, lens)
    completed = {
        path.name: path.read_bytes()
        for path in output.iterdir()
        if path.name.endswith((".raw.md", ".final.md", ".meta.json"))
    }
    Path(manifest["target"]["path"]).write_text("# changed live target\n" * 8)

    def captured_dispatch(*args, **kwargs):
        workers = []
        for position, original in enumerate((1, 3)):
            worker = WorkerResult(
                index=position, model_id=f"fixture-model-{original}", status="success"
            )
            worker.body = f"## Verdict\nCaptured café slot {original}.\n"
            workers.append(worker)
        return workers

    monkeypatch.setattr(
        "superclaude.cli.swarm.dispatch.dispatch_wave1", captured_dispatch
    )
    args = ["--resume", job_id, "--output", str(output)]
    if force_relens:
        args.append("--force-relens")
    result = CliRunner().invoke(run_cmd, args)
    assert result.exit_code == 0, result.output
    contract = yaml.safe_load((output / "return-contract.yaml").read_text())
    for worker in contract["output_files"]:
        if worker["index"] not in (1, 3):
            continue
        final = Path(worker["final_path"])
        assert "-saved-" in final.name
        provenance = yaml.safe_load(final.read_text().split("---", 2)[1])
        assert provenance["target"] == manifest["target"]["path"]
        assert provenance["target_checksum"] == manifest["preflight"]["target_checksum"]
        assert provenance["caller_label"] == "accepted-retention-label"
        assert provenance["target_truncated"] is False
        meta = json.loads(Path(worker["meta_path"]).read_text())
        assert meta["status"] == "success"
        assert meta["recipe"] == "bare-review-v1"
        assert bool(worker["raw_path"]) is retain_raw
        if retain_raw:
            assert "Captured café" in Path(worker["raw_path"]).read_text()
    assert {name: (output / name).read_bytes() for name in completed} == completed
    assert (output / "manifest.json").read_bytes() == manifest_bytes


@pytest.mark.parametrize("force_relens", [False, True])
@pytest.mark.parametrize("retain_raw", [False, True])
@pytest.mark.parametrize("completed", [(0, 2), (0, 1, 2, 3)])
@pytest.mark.parametrize(
    "template",
    [
        "{lens}_{model_slug}_{index}.json",
        "nested/{lens}/{index:02d}-{model_slug}.md",
        "audit-17-{model_slug}-{lens}-slot-{index:02d}.md",
    ],
)
def test_resume_discovers_saved_layout_without_replacing_completed_files(
    tmp_path, monkeypatch, force_relens, retain_raw, completed, template
):
    import superclaude.cli.swarm.dispatch as dispatch_mod
    import superclaude.cli.swarm.reduce as reduce_mod

    output, job_id, lens = _persist_resume_job(tmp_path, retain_raw=retain_raw)
    manifest = output / "manifest.json"
    payload = json.loads(manifest.read_text())
    payload["output_filename_template"] = template
    manifest.write_text(json.dumps(payload))
    for index in completed:
        _seed_resume_slot(output, index, lens)
        old = f"{lens}-{index:02d}-fixture-model-{index}"
        rendered = template.format(
            lens=lens, index=index, model_slug=f"fixture-model-{index}"
        )
        base = rendered[:-3] if rendered.endswith(".md") else rendered
        for suffix in (".raw.md", ".final.md", ".meta.json"):
            destination = output / f"{base}{suffix}"
            destination.parent.mkdir(parents=True, exist_ok=True)
            (output / f"{old}{suffix}").rename(destination)
    before = {
        p.relative_to(output): p.read_bytes() for p in output.rglob("*") if p.is_file()
    }
    missing = [i for i in range(4) if i not in completed]
    calls = []

    def dispatch(preflight, **kwargs):
        calls.append(preflight.manifest.preflight.workers_requested)
        assert calls == [len(missing)]
        workers = []
        for compact, original in enumerate(missing):
            worker = WorkerResult(
                index=compact, model_id=f"fixture-model-{original}", status="success"
            )
            worker.body = f"## Verdict\nNew body {original}.\n"
            workers.append(worker)
        return workers

    real_emit = reduce_mod.emit_contract
    observed = []

    def emit(contract, directory):
        observed.append(contract)
        assert [w.index for w in contract.output_files] == list(range(4))
        for worker in contract.output_files:
            rendered = template.format(
                lens=lens,
                index=worker.index,
                model_slug=f"fixture-model-{worker.index}",
            )
            base = rendered[:-3] if rendered.endswith(".md") else rendered
            assert worker.final_path == str(output / f"{base}.final.md")
            assert worker.raw_path == (
                str(output / f"{base}.raw.md") if retain_raw else ""
            )
        assert all((output / p).read_bytes() == data for p, data in before.items())
        return real_emit(contract, directory)

    monkeypatch.setattr(dispatch_mod, "dispatch_wave1", dispatch)
    monkeypatch.setattr(reduce_mod, "emit_contract", emit)
    args = ["--resume", job_id, "--output", str(output)]
    if force_relens:
        args.append("--force-relens")
    for _ in range(2):
        result = CliRunner().invoke(run_cmd, args)
        assert result.exit_code == 0, result.output
    assert calls == ([len(missing)] if missing else [])
    assert len(observed) == 2
    assert all((output / p).read_bytes() == data for p, data in before.items())


@pytest.mark.parametrize(
    "unsafe",
    [
        "no-index",
        "unsupported",
        "unsupported-nested",
        "formatted-model",
        "escape",
        "directory-link",
        "meta-link",
        "final-link",
        "raw-link",
        "duplicate",
        "identity-collision",
    ],
)
def test_resume_rejects_unsafe_inventory_before_dispatch(tmp_path, monkeypatch, unsafe):
    import superclaude.cli.swarm.dispatch as dispatch_mod

    output, job_id, lens = _persist_resume_job(tmp_path)
    outside = tmp_path / "outside"
    outside.mkdir()
    sentinel = outside / "sentinel"
    sentinel.write_bytes(b"must not change\n")
    manifest = output / "manifest.json"
    payload = json.loads(manifest.read_text())
    template = "{lens}-{index:02d}-{model_slug}.md"
    if unsafe == "no-index":
        template = "{lens}-{model_slug}.md"
    elif unsafe == "unsupported":
        template = "{lens}-{index}-{unknown}.md"
    elif unsafe == "unsupported-nested":
        template = "{lens}-{index:{unknown}}-{model_slug}.md"
    elif unsafe == "formatted-model":
        template = "{lens}-{index}-{model_slug!r}.md"
    elif unsafe == "escape":
        template = "../outside/{index}-{model_slug}.md"
    elif unsafe == "directory-link":
        (output / "linked").symlink_to(outside, target_is_directory=True)
        template = "linked/{index}-{model_slug}.md"
    elif unsafe.endswith("-link"):
        _seed_resume_slot(output, 0, lens)
        suffix = {
            "meta-link": ".meta.json",
            "final-link": ".final.md",
            "raw-link": ".raw.md",
        }[unsafe]
        linked = output / f"{lens}-00-fixture-model-0{suffix}"
        linked.unlink()
        linked.symlink_to(sentinel)
    elif unsafe == "duplicate":
        _seed_resume_slot(output, 0, lens)
        (output / f"{lens}-00-other.meta.json").write_text('{"status":"success"}')
    elif unsafe == "identity-collision":
        template = "{lens}-00-{index:02d}-{model_slug}.md"
        (output / f"{lens}-00-01-model.meta.json").write_text('{"status":"success"}')
    payload["output_filename_template"] = template
    manifest.write_text(json.dumps(payload))
    before = {
        p.relative_to(output): p.read_bytes() for p in output.rglob("*") if p.is_file()
    }

    def unexpected_dispatch(*args, **kwargs):
        pytest.fail("unsafe inventory must be rejected before dispatch")

    monkeypatch.setattr(dispatch_mod, "dispatch_wave1", unexpected_dispatch)
    result = CliRunner().invoke(run_cmd, ["--resume", job_id, "--output", str(output)])
    assert result.exit_code == 1, result.output
    assert "unsafe or ambiguous worker inventory" in result.output
    assert all((output / p).read_bytes() == data for p, data in before.items())
    assert sentinel.read_bytes() == b"must not change\n"


def test_saved_layout_discovery_matches_whole_paths_and_repeated_slugs(tmp_path):
    from superclaude.cli.swarm.commands import discover_succeeded_slots

    output = tmp_path / "out"
    output.mkdir()
    template = "nested/{lens}/{model_slug}-{index:02d}-{model_slug}.json"
    nested = output / "nested" / "review.17"
    nested.mkdir(parents=True)
    for name, status in [
        ("model-2-4-01-model-2-4.json.meta.json", "success"),
        ("other-00-different.json.meta.json", "success"),
        ("ignored-02-ignored.json.meta.json", "failed"),
        ("prefix-model-03-model.json.meta.json.extra", "success"),
    ]:
        (nested / name).write_text(json.dumps({"status": status}))
    (output / "unrelated.meta.json").write_text('{"status":"success"}')
    slots = discover_succeeded_slots(
        output, 4, lens_name="review.17", filename_template=template
    )
    assert set(slots) == {1}
    assert slots[1].model_id == "model-2-4"
    assert slots[1].final_path == ""  # Preserve historical final-evidence policy.

"""Stored reduction context survives public stub runs and completed-job resume."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest
import yaml
from click.testing import CliRunner

from superclaude.cli.swarm import preflight as preflight_mod
from superclaude.cli.swarm.commands import _build_spec_from_lens, run_cmd
from superclaude.cli.swarm.models import CallerMetadata

CONTEXT_FIELDS = (
    "lens",
    "lens_source",
    "recommended_next_command",
    "caller",
    "caller_metadata",
    "target",
)


def _fresh(tmp_path: Path, monkeypatch: pytest.MonkeyPatch, explicit: bool = False):
    target = tmp_path / "target.py"
    target.write_text("# accepted target with sufficient non-whitespace content\n" * 5)
    output = tmp_path / "out"
    spec = _build_spec_from_lens("bare-review")
    spec["job_id"] = "stored-context"
    spec["target"]["path"] = str(target)
    spec["target"]["truncation"]["line_cap"] = 2
    spec["output"]["dir"] = str(output)
    spec["caller"] = dict(
        skill="context-test",
        skill_version="1.0",
        invocation_label="accepted",
        kind="cli",
    )
    if explicit:
        spec["recommended_next_command_template"] = (
            "inspect {job_id} {suspect_files} {compare_files}"
        )
        spec["recommended_next_command_substitutions"] = dict(
            job_id="accepted-job",
            suspect_files="accepted-files",
            compare_files="accepted-compare",
        )
    original = preflight_mod.run_preflight

    def with_override(*args, **kwargs):
        return original(
            *args,
            **kwargs,
            caller_metadata_override=CallerMetadata(suspect=False, tier="T1"),
        )

    monkeypatch.setattr(preflight_mod, "run_preflight", with_override)
    path = tmp_path / "spec.json"
    path.write_text(json.dumps(spec))
    result = CliRunner().invoke(run_cmd, [str(path), "--output", str(output)])
    assert result.exit_code == 0, result.output
    contract = yaml.safe_load((output / "return-contract.yaml").read_text())
    assert contract["workers_succeeded"] == spec["workers"]["count"]
    return output, spec, contract


def _resume(output: Path, monkeypatch: pytest.MonkeyPatch):
    def forbidden(*args, **kwargs):
        raise AssertionError(
            "completed resume must not redispatch or consult live lens state"
        )

    monkeypatch.setattr(preflight_mod, "resolve_lens", forbidden)
    monkeypatch.setattr("superclaude.cli.swarm.dispatch.dispatch_wave1", forbidden)
    manifest_bytes = (output / "manifest.json").read_bytes()
    result = CliRunner().invoke(
        run_cmd, ["--resume", "stored-context", "--output", str(output)]
    )
    assert result.exit_code == 0, result.output
    assert "redispatched=0" in result.output
    assert "skipped=3" in result.output
    assert (output / "manifest.json").read_bytes() == manifest_bytes
    return yaml.safe_load((output / "return-contract.yaml").read_text())


@pytest.mark.parametrize("explicit", [False, True])
def test_fresh_and_completed_resume_keep_populated_context(
    tmp_path, monkeypatch, explicit
):
    output, spec, fresh = _fresh(tmp_path, monkeypatch, explicit)
    resumed = _resume(output, monkeypatch)
    assert {key: resumed[key] for key in CONTEXT_FIELDS} == {
        key: fresh[key] for key in CONTEXT_FIELDS
    }
    assert fresh["lens"] == "bare-review"
    assert fresh["lens_source"] == "registry"
    assert fresh["caller"] == spec["caller"]
    assert fresh["caller_metadata"] == dict(suspect=False, tier="T1")
    expected_checksum = hashlib.sha256(
        ("# accepted target with sufficient non-whitespace content\n" * 2).encode()
    ).hexdigest()[:12]
    assert fresh["target"] == dict(
        path=spec["target"]["path"],
        checksum=expected_checksum,
        truncated=True,
        truncation_line_cap=2,
    )
    if explicit:
        assert (
            fresh["recommended_next_command"]
            == "inspect accepted-job accepted-files accepted-compare"
        )
    else:
        assert "/sc:adversarial" in fresh["recommended_next_command"]
        assert ".final.md" in fresh["recommended_next_command"]
        assert "{suspect_files}" not in fresh["recommended_next_command"]


def test_preflight_persists_context_before_any_dispatch(tmp_path, monkeypatch):
    spec = _build_spec_from_lens("bare-review")
    spec["target"]["path"] = str(tmp_path / "never-read.py")
    spec["target"]["truncation"]["line_cap"] = 2
    spec["output"]["dir"] = str(tmp_path)
    spec["recommended_next_command_template"] = "inspect {job_id}"
    spec["recommended_next_command_substitutions"] = {"job_id": "accepted-job"}
    body = b"# sufficient non-whitespace content for the target boundary\n" * 5
    result = preflight_mod.run_preflight(
        spec,
        target_loader=lambda _: body,
        output_dir=tmp_path,
        caller_metadata_override=CallerMetadata(suspect=False, tier=""),
    )
    assert not (tmp_path / "return-contract.yaml").exists()
    manifest = result.manifest
    assert manifest.caller.invocation_label == spec["caller"]["invocation_label"]
    assert manifest.caller_metadata == CallerMetadata(suspect=False, tier="")
    assert manifest.target.path == spec["target"]["path"]
    assert manifest.target.truncated is True
    assert manifest.target.truncation_line_cap == 2
    assert manifest.target.checksum == manifest.preflight.target_checksum[:12]
    assert (
        manifest.preflight.target_checksum
        == hashlib.sha256(b"\n".join(body.splitlines()[:2]) + b"\n").hexdigest()
    )
    assert manifest.lens_source == "registry"
    before = (tmp_path / "manifest.json").read_bytes()

    def forbidden(*args, **kwargs):
        raise AssertionError("default resume must not load target or live lens")

    monkeypatch.setattr(preflight_mod, "resolve_lens", forbidden)
    monkeypatch.setattr(preflight_mod, "_default_target_loader", forbidden)
    rehydrated = preflight_mod.resume_mode(tmp_path / "manifest.json")
    assert rehydrated.caller == manifest.caller
    assert rehydrated.target.path == spec["target"]["path"]
    assert rehydrated.recommended_next_command_template == "inspect {job_id}"
    assert rehydrated.recommended_next_command_substitutions == {
        "job_id": "accepted-job"
    }
    assert (tmp_path / "manifest.json").read_bytes() == before


@pytest.mark.parametrize("empty", [False, True])
def test_resume_mode_distinguishes_absent_and_empty_template(
    tmp_path, monkeypatch, empty
):
    from superclaude.cli.swarm.models import Manifest, ResolvedLensEntry, to_dict

    payload = to_dict(
        Manifest(
            resolved_lens_entry=ResolvedLensEntry(
                name="bare-review",
                recommended_next_command_template="snapshot {job_id}",
            )
        )
    )
    payload["preflight"]["transport_kind"] = "stub"
    if empty:
        payload["recommended_next_command_template"] = ""
        payload["recommended_next_command_substitutions"] = {}
    else:
        payload.pop("recommended_next_command_template")
        payload.pop("recommended_next_command_substitutions")
    path = tmp_path / "manifest.json"
    path.write_text(json.dumps(payload, indent=3))
    before = path.read_bytes()
    monkeypatch.setattr(
        preflight_mod, "resolve_lens", lambda _: pytest.fail("live lookup")
    )
    restored = preflight_mod.resume_mode(path)
    assert restored.recommended_next_command_template == (
        "" if empty else "snapshot {job_id}"
    )
    assert restored.recommended_next_command_substitutions == {}
    assert path.read_bytes() == before


_NEW_CONTEXT = (
    "caller",
    "target",
    "lens_source",
    "recommended_next_command_template",
    "recommended_next_command_substitutions",
)


def _legacy(output, *, metadata=False):
    path = output / "manifest.json"
    payload = json.loads(path.read_text())
    for name in _NEW_CONTEXT:
        payload.pop(name, None)
    if not metadata:
        payload.pop("caller_metadata", None)
    path.write_text(json.dumps(payload, indent=3))
    return payload


@pytest.mark.parametrize("explicit", [False, True])
def test_resume_without_contract_and_repeated_resume_use_manifest(
    tmp_path, monkeypatch, explicit
):
    output, spec, fresh = _fresh(tmp_path, monkeypatch, explicit)
    (output / "return-contract.yaml").unlink()
    Path(spec["target"]["path"]).unlink()
    for _ in range(2):
        resumed = _resume(output, monkeypatch)
        assert {k: resumed[k] for k in CONTEXT_FIELDS} == {
            k: fresh[k] for k in CONTEXT_FIELDS
        }


def test_legacy_prior_contract_recovers_only_missing_context(tmp_path, monkeypatch):
    output, spec, fresh = _fresh(tmp_path, monkeypatch, True)
    payload = _legacy(output)
    # Historical rendered text is a fallback only without a saved template.
    payload["resolved_lens_entry"]["recommended_next_command_template"] = ""
    (output / "manifest.json").write_text(json.dumps(payload, indent=3))
    fresh["caller"]["invocation_label"] = "historical-caller"
    fresh["recommended_next_command"] = "historical command {literal-braces}"
    fresh["target"]["truncation_line_cap"] = 27
    fresh["lens_source"] = "custom"
    (output / "return-contract.yaml").write_text(yaml.safe_dump(fresh))
    Path(spec["target"]["path"]).unlink()
    for _ in range(2):
        resumed = _resume(output, monkeypatch)
        assert {k: resumed[k] for k in CONTEXT_FIELDS} == {
            k: fresh[k] for k in CONTEXT_FIELDS
        }


@pytest.mark.parametrize("prior", [False, True])
@pytest.mark.parametrize("metadata", [False, True])
def test_legacy_empty_contract_does_not_mask_snapshot(
    tmp_path, monkeypatch, prior, metadata
):
    from superclaude.cli.swarm.models import CallerInfo, ContractTarget, to_dict

    output, spec, contract = _fresh(tmp_path, monkeypatch)
    payload = _legacy(output, metadata=metadata)
    snapshot = payload["resolved_lens_entry"]
    assert snapshot["suspect"] is True
    assert snapshot["tier"] == "T2"
    if prior:
        contract.update(
            lens="",
            lens_source="",
            recommended_next_command="",
            caller_metadata=dict(suspect=False, tier=""),
            target=to_dict(ContractTarget()),
            caller=to_dict(CallerInfo()),
        )
        (output / "return-contract.yaml").write_text(yaml.safe_dump(contract))
    else:
        (output / "return-contract.yaml").unlink()
    Path(spec["target"]["path"]).unlink()
    for _ in range(2):
        resumed = _resume(output, monkeypatch)
        assert resumed["lens"] == "bare-review"
        assert resumed["lens_source"] == "registry"
        assert resumed["caller_metadata"] == (
            dict(suspect=False, tier="T1")
            if metadata
            else dict(suspect=True, tier="T2")
        )
        assert resumed["caller"] == to_dict(CallerInfo())
        assert resumed["target"] == to_dict(
            ContractTarget(checksum=payload["preflight"]["target_checksum"][:12])
        )
        assert "/sc:adversarial" in resumed["recommended_next_command"]
        assert ".final.md" in resumed["recommended_next_command"]
        assert "{suspect_files}" not in resumed["recommended_next_command"]


def test_explicit_empty_manifest_values_override_populated_prior(tmp_path, monkeypatch):
    from superclaude.cli.swarm.models import CallerInfo, ContractTarget, to_dict

    output, spec, _ = _fresh(tmp_path, monkeypatch, True)
    path = output / "manifest.json"
    payload = json.loads(path.read_text())
    payload.update(
        caller=to_dict(CallerInfo()),
        target=to_dict(ContractTarget(truncated=False, truncation_line_cap=0)),
        lens_source="",
        recommended_next_command_template="",
        recommended_next_command_substitutions={},
        caller_metadata=dict(suspect=False, tier=""),
    )
    path.write_text(json.dumps(payload))
    Path(spec["target"]["path"]).unlink()
    for _ in range(2):
        resumed = _resume(output, monkeypatch)
        for key in ("caller", "target", "lens_source", "caller_metadata"):
            assert resumed[key] == payload[key]
        assert resumed["recommended_next_command"] == ""


@pytest.mark.parametrize(
    "bad", ["yaml", "list", "job", "version", "fields", "encoding"]
)
def test_legacy_invalid_prior_is_ignored_safely(tmp_path, monkeypatch, bad):
    output, spec, contract = _fresh(tmp_path, monkeypatch)
    _legacy(output)
    if bad == "yaml":
        body = b"["
    elif bad == "list":
        body = b"[]"
    elif bad == "encoding":
        body = b"\xff"
    else:
        if bad == "job":
            contract["job_id"] = "unrelated-job"
        elif bad == "version":
            contract["contract_version"] = "unsupported"
        else:
            contract.update(
                caller_metadata=[False],
                target=dict(
                    path=[], checksum=7, truncated="false", truncation_line_cap=False
                ),
                caller=dict(kind="invalid"),
                lens_source=["registry"],
                recommended_next_command=[],
            )
        body = yaml.safe_dump(contract).encode()
    (output / "return-contract.yaml").write_bytes(body)
    Path(spec["target"]["path"]).unlink()
    resumed = _resume(output, monkeypatch)
    assert resumed["lens"] == "bare-review"
    assert resumed["caller_metadata"] == dict(suspect=True, tier="T2")
    assert resumed["target"]["path"] == ""
    assert "/sc:adversarial" in resumed["recommended_next_command"]


def test_force_relens_keeps_explicit_live_template_semantics(tmp_path, monkeypatch):
    from dataclasses import replace

    from superclaude.cli.swarm.lenses import LENSES

    output, _, _ = _fresh(tmp_path, monkeypatch, True)
    live = replace(
        LENSES["bare-review"],
        recommended_next_command_template="live {job_id} {suspect_files}",
    )
    calls = []

    def resolver(name):
        calls.append(name)
        return live

    monkeypatch.setattr(preflight_mod, "resolve_lens", resolver)
    monkeypatch.setattr(
        "superclaude.cli.swarm.dispatch.dispatch_wave1",
        lambda *a, **kw: pytest.fail("completed slots redispatched"),
    )
    before = (output / "manifest.json").read_bytes()
    result = CliRunner().invoke(
        run_cmd,
        ["--resume", "stored-context", "--output", str(output), "--force-relens"],
    )
    assert result.exit_code == 0, result.output
    assert calls
    assert "redispatched=0" in result.output
    resumed = yaml.safe_load((output / "return-contract.yaml").read_text())
    assert resumed["recommended_next_command"] == "live accepted-job accepted-files"
    assert resumed["caller_metadata"] == dict(suspect=False, tier="T1")
    assert (output / "manifest.json").read_bytes() == before


def test_legacy_partial_resume_refreshes_saved_template_inputs(tmp_path, monkeypatch):
    from superclaude.cli.swarm.models import WorkerResult

    output, _, prior = _fresh(tmp_path, monkeypatch)
    _legacy(output)
    for path in output.iterdir():
        if any(f"-{index:02d}-" in path.name for index in (1, 2)):
            path.unlink()
    completed = {
        path.name: path.read_bytes()
        for path in output.iterdir()
        if path.name.endswith((".final.md", ".meta.json", ".raw.md"))
    }
    prior["recommended_next_command"] = "historical " + str(
        next(output.glob("*.final.md"))
    )
    (output / "return-contract.yaml").write_text(yaml.safe_dump(prior))
    manifest_before = (output / "manifest.json").read_bytes()
    calls = []

    def captured_dispatch(preflight_result, **kwargs):
        assert preflight_result.manifest.preflight.workers_requested == 2
        calls.append(True)
        workers = []
        for index in range(2):
            worker = WorkerResult(
                index=index, model_id=f"recovered-{index}", status="success"
            )
            worker.body = "## Verdict\nCaptured recovery review.\n"
            workers.append(worker)
        return workers

    monkeypatch.setattr(
        "superclaude.cli.swarm.dispatch.dispatch_wave1", captured_dispatch
    )
    result = CliRunner().invoke(
        run_cmd, ["--resume", "stored-context", "--output", str(output)]
    )
    assert result.exit_code == 0, result.output
    resumed = yaml.safe_load((output / "return-contract.yaml").read_text())
    assert calls == [True]
    assert len(resumed["output_files"]) == 3
    for worker in resumed["output_files"]:
        assert worker["final_path"] in resumed["recommended_next_command"]
    assert (output / "manifest.json").read_bytes() == manifest_before
    assert {name: (output / name).read_bytes() for name in completed} == completed


@pytest.mark.parametrize("force_relens", [False, True])
def test_partial_resume_preserves_provider_request_and_policy(
    tmp_path, monkeypatch, force_relens
):
    import dataclasses

    from superclaude.cli.swarm import commands as commands_mod
    from superclaude.cli.swarm.models import JobSpec, WorkerResult, from_dict

    target = tmp_path / "accepted.py"
    target.write_text("# accepted content with enough non-whitespace bytes\n" * 4)
    output = tmp_path / "out"
    spec = _build_spec_from_lens("bare-review")
    spec["job_id"] = "accepted-provider"
    spec["target"]["path"] = str(target)
    spec["target"]["truncation"]["line_cap"] = 2
    spec["output"]["dir"] = str(output)
    spec["transport"]["kind"] = "openai_compat"
    spec["workers"].update(
        count=3, models=["captured-one", "captured-two", "captured-three"],
        timeout_sec=17, temperature=0.7,
        retry={"on_5xx": False, "on_5xx_backoff_sec": 9,
               "on_4xx": True, "on_timeout": True},
    )
    spec["prompt"]["system"] += "\nAccepted instruction override."
    accepted = from_dict(JobSpec, spec)
    preflight_mod.run_preflight(spec, output_dir=output)
    stem = output / "bare-review-00-captured-one"
    stem.with_suffix(".final.md").write_text("Completed review.\n")
    stem.with_suffix(".meta.json").write_text(
        json.dumps({"status": "success", "bytes": 18})
    )
    before = (output / "manifest.json").read_bytes()
    calls = []

    factory_settings = []
    sent = []
    from superclaude.cli.swarm.dispatch import dispatch_wave1 as real_dispatch

    class CapturedTransport:
        def __init__(self, index):
            self.index = index

        def send(self, prompt, timeout_sec):
            sent.append((self.index, prompt, timeout_sec))
            worker = WorkerResult(
                index=self.index, model_id=spec["workers"]["models"][self.index],
                status="success",
            )
            worker.body = "## Verdict\nCaptured resumed review.\n"
            return worker

    def captured_factory(kind, **kwargs):
        assert kind == "openai_compat"
        factory_settings.append(kwargs)
        return CapturedTransport

    def captured_dispatch(result, **kwargs):
        calls.append(True)
        assert result.manifest.preflight.workers_requested == 2
        assert [kwargs["transport_for_slot"](i).index for i in range(2)] == [1, 2]
        prompt = kwargs.get("prompt", "")
        assert prompt, "resumed provider request must not be empty"
        assert target.read_text().splitlines()[0] in prompt
        if not force_relens:
            assert "Accepted instruction override." in prompt
        worker_spec = kwargs.get("worker_spec")
        assert worker_spec is not None, "accepted worker policy must reach dispatch"
        assert dataclasses.asdict(worker_spec) == dataclasses.asdict(accepted.workers)
        return real_dispatch(result, **kwargs)

    monkeypatch.setattr(commands_mod, "_resolve_run_transport_factory", captured_factory)
    monkeypatch.setattr("superclaude.cli.swarm.dispatch.dispatch_wave1", captured_dispatch)
    args = ["--resume", "accepted-provider", "--output", str(output)]
    if force_relens:
        args.append("--force-relens")
    result = CliRunner().invoke(run_cmd, args)
    if result.exception and not isinstance(result.exception, SystemExit):
        raise result.exception
    assert result.exit_code == 0, result.output
    assert calls == [True]
    assert factory_settings[0]["models"] == spec["workers"]["models"]
    assert factory_settings[0]["temperature"] == 0.7
    assert sorted(index for index, _, _ in sent) == [1, 2]
    assert all(prompt and timeout == 17 for _, prompt, timeout in sent)
    assert (output / "manifest.json").read_bytes() == before


def test_completed_legacy_provider_resume_needs_no_live_inputs(tmp_path, monkeypatch):
    from superclaude.cli.swarm import commands as commands_mod

    output, spec, _ = _fresh(tmp_path, monkeypatch)
    payload = _legacy(output)
    payload.pop("accepted_workers", None)
    payload.pop("accepted_prompt", None)
    payload["preflight"]["transport_kind"] = "openai_compat"
    (output / "manifest.json").write_text(json.dumps(payload))
    Path(spec["target"]["path"]).unlink()

    def forbidden(*args, **kwargs):
        pytest.fail("completed legacy provider resume needs no transport or target read")

    monkeypatch.setattr(commands_mod, "_resolve_run_transport_factory", forbidden)
    monkeypatch.setattr(commands_mod, "_read_truncated_target", forbidden)
    resumed = _resume(output, monkeypatch)
    assert resumed["workers_succeeded"] == 3


@pytest.mark.parametrize("damage", ["legacy", "changed", "missing"])
def test_partial_provider_resume_refuses_unrecoverable_inputs(tmp_path, monkeypatch, damage):
    from superclaude.cli.swarm import commands as commands_mod

    output, spec, _ = _fresh(tmp_path, monkeypatch)
    next(path for path in output.glob("*.meta.json") if "-01-" in path.name).unlink()
    manifest_path = output / "manifest.json"
    payload = json.loads(manifest_path.read_text())
    if damage == "legacy":
        payload.pop("accepted_workers", None)
        payload.pop("accepted_prompt", None)
        manifest_path.write_text(json.dumps(payload))
    elif damage == "changed":
        Path(spec["target"]["path"]).write_text("# different accepted input\n" * 5)
    else:
        Path(spec["target"]["path"]).unlink()
    before = {path.name: path.read_bytes() for path in output.iterdir() if path.is_file()}

    def forbidden(*args, **kwargs):
        pytest.fail("unsafe recovery must fail before transport construction or dispatch")

    monkeypatch.setattr(commands_mod, "_resolve_run_transport_factory", forbidden)
    monkeypatch.setattr("superclaude.cli.swarm.dispatch.dispatch_wave1", forbidden)
    result = CliRunner().invoke(
        run_cmd, ["--resume", "stored-context", "--output", str(output),
                  "--transport", "openai_compat"]
    )
    if result.exception and not isinstance(result.exception, SystemExit):
        raise result.exception
    assert result.exit_code == 1
    assert "cannot recover" in result.output
    assert ("accepted" if damage == "legacy" else "target") in result.output
    assert {path.name: path.read_bytes() for path in output.iterdir() if path.is_file()} == before


def test_resume_mode_keeps_accepted_worker_policy(tmp_path, monkeypatch):
    import dataclasses

    from superclaude.cli.swarm.models import JobSpec, from_dict

    output, spec, _ = _fresh(tmp_path, monkeypatch)
    spec["workers"].update(
        timeout_sec=17, temperature=0.7,
        retry={"on_5xx": False, "on_5xx_backoff_sec": 9,
               "on_4xx": True, "on_timeout": True},
    )
    preflight_mod.run_preflight(spec, output_dir=output)
    before = (output / "manifest.json").read_bytes()
    for force_relens in (False, True):
        recovered = preflight_mod.resume_mode(
            output / "manifest.json", force_relens=force_relens
        )
        assert dataclasses.asdict(recovered.workers) == dataclasses.asdict(
            from_dict(JobSpec, spec).workers
        )
    assert (output / "manifest.json").read_bytes() == before


@pytest.mark.parametrize("force_relens", [False, True])
@pytest.mark.parametrize("empty_label", [False, True])
@pytest.mark.parametrize("legacy_context", [False, True])
def test_partial_resume_keeps_accepted_normalization_provenance(
    tmp_path, monkeypatch, force_relens, empty_label, legacy_context
):
    from superclaude.cli.swarm import commands as commands_mod
    from superclaude.cli.swarm.models import WorkerResult

    original = preflight_mod.run_preflight

    def with_recipe_args(spec, **kwargs):
        spec["normalization"]["recipe_args"] = {
            "caller_label": "" if empty_label else "accepted-recipe-label",
            "target_truncated": False,
        }
        return original(spec, **kwargs)

    monkeypatch.setattr(preflight_mod, "run_preflight", with_recipe_args)
    output, spec, fresh = _fresh(tmp_path, monkeypatch)
    if legacy_context:
        _legacy(output)
    first = next(output.glob("*.final.md"))
    expected = yaml.safe_load(first.read_text().split("---", 2)[1])
    next(path for path in output.glob("*.meta.json") if "-01-" in path.name).unlink()
    preserved = {
        path.name: path.read_bytes() for path in output.iterdir()
        if path.name.endswith((".raw.md", ".final.md", ".meta.json"))
        and "-01-" not in path.name
    }
    manifest_before = (output / "manifest.json").read_bytes()
    Path(spec["target"]["path"]).write_text("# changed live input\n" * 5)

    def forbidden(*args, **kwargs):
        pytest.fail("normalization provenance must not reread changed live inputs")

    def captured_dispatch(*args, **kwargs):
        worker = WorkerResult(index=0, model_id="captured-provenance", status="success")
        worker.body = "## Verdict\nCaptured normalized result.\n"
        return [worker]

    monkeypatch.setattr(commands_mod, "_read_truncated_target", forbidden)
    monkeypatch.setattr(preflight_mod, "_default_target_loader", forbidden)
    monkeypatch.setattr("superclaude.cli.swarm.dispatch.dispatch_wave1", captured_dispatch)
    args = ["--resume", "stored-context", "--output", str(output)]
    if force_relens:
        args.append("--force-relens")
    result = CliRunner().invoke(run_cmd, args)
    assert result.exit_code == 0, result.output
    resumed = yaml.safe_load((output / "return-contract.yaml").read_text())
    worker = next(worker for worker in resumed["output_files"] if worker["index"] == 1)
    provenance = yaml.safe_load(Path(worker["final_path"]).read_text().split("---", 2)[1])
    for field in ("target", "target_checksum", "caller_label", "target_truncated"):
        assert provenance[field] == expected[field], field
    assert len(provenance["target_checksum"]) == 64
    assert resumed["target"] == fresh["target"]
    assert {name: (output / name).read_bytes() for name in preserved} == preserved
    assert (output / "manifest.json").read_bytes() == manifest_before

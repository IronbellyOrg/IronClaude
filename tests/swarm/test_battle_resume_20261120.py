"""Model-free regressions for provider recovery and truthful resume artifacts."""
from __future__ import annotations

import dataclasses
import json
from pathlib import Path

import pytest
import yaml
from click.testing import CliRunner

from superclaude.cli.swarm import commands as cmd
from superclaude.cli.swarm.models import WorkerResult

from .test_raw_retention import _persist_resume_job, _seed_resume_slot


def inventory(root):
    return {p.relative_to(root): p.read_bytes() for p in root.rglob("*") if p.is_file()}


def resume(output, job, force=False):
    return CliRunner().invoke(cmd.run_cmd, ["--resume", job, "--output", str(output)] +
                              (["--force-relens"] if force else []))


@pytest.mark.parametrize("hazard", ["unknown", "positional", "duplicate", "symlink", "missing-final", "final-directory", "meta-directory"])
def test_battle_inventory_safety(tmp_path, monkeypatch, hazard):
    output, job, lens = _persist_resume_job(tmp_path)
    for index in range(4):
        _seed_resume_slot(output, index, lens)
    manifest_path = output / "manifest.json"
    data = json.loads(manifest_path.read_text())
    if hazard in ("unknown", "positional"):
        data["output_filename_template"] = "{unknown}-{index}.md" if hazard == "unknown" else "{}-{index}.md"
        manifest_path.write_text(json.dumps(data))
    elif hazard == "duplicate":
        (output / f"{lens}-00-another.meta.json").write_text('{"status":"success"}')
    elif hazard == "symlink":
        outside = tmp_path / "outside"
        outside.mkdir()
        victim = next(output.glob("*-00-*.final.md"))
        victim.unlink()
        victim.symlink_to(outside / "body.md")
    elif hazard in ("missing-final", "final-directory"):
        final = next(output.glob("*-00-*.final.md"))
        final.unlink()
        if hazard == "final-directory":
            final.mkdir()
    else:
        meta = next(output.glob("*-00-*.meta.json"))
        meta.unlink()
        meta.mkdir()
    before = inventory(output)
    calls = []
    def dispatch(preflight_result, **kwargs):
        calls.append(preflight_result.manifest.preflight.workers_requested)
        worker = WorkerResult(index=0, model_id="metadata-retry", status="success")
        worker.body = "## Verdict\nRecovered unreadable sidecar.\n"
        return [worker]

    monkeypatch.setattr("superclaude.cli.swarm.dispatch.dispatch_wave1", dispatch)
    result = resume(output, job)
    assert all((output / p).read_bytes() == v for p, v in before.items())
    if hazard == "meta-directory":
        # Unreadable metadata deliberately retries only the unproven slot.
        assert result.exit_code == 0, result.output
        assert calls == [1]
        assert meta.is_dir()
        contract = yaml.safe_load((output / "return-contract.yaml").read_text())
        assert contract["output_files"][0]["model_id"] == "metadata-retry"
    else:
        assert result.exit_code != 0, "invalid completed inventory reported success"
        assert calls == [], "invalid inventory must be refused before redispatch"


@pytest.mark.parametrize("final_present", [False, True])
def test_completed_replay_allows_zero_byte_final(tmp_path, monkeypatch, final_present):
    output, job, lens = _persist_resume_job(tmp_path)
    for index in range(4):
        _seed_resume_slot(output, index, lens)
    final = next(output.glob("*-00-*.final.md"))
    if final_present:
        final.write_text("")
    else:
        final.unlink()
    meta = next(output.glob("*-00-*.meta.json"))
    meta.write_text(json.dumps({"status": "success", "bytes": 0}))
    before = inventory(output)

    def forbidden(*args, **kwargs):
        pytest.fail("zero-byte completion must not redispatch")

    monkeypatch.setattr("superclaude.cli.swarm.dispatch.dispatch_wave1", forbidden)
    result = resume(output, job)
    assert result.exit_code == 0, result.output
    contract = yaml.safe_load((output / "return-contract.yaml").read_text())
    assert contract["output_files"][0]["final_path"] == (str(final) if final_present else "")
    assert all((output / p).read_bytes() == data for p, data in before.items())


@pytest.mark.parametrize("prior_final", [False, True])
@pytest.mark.parametrize("canonical_is_final", [False, True])
def test_empty_normalization_does_not_advertise_planned_final(
    tmp_path, prior_final, canonical_is_final
):
    from superclaude.cli.swarm.normalize import normalize_wave2

    from .test_normalize import _make_worker

    worker = _make_worker(tmp_path, 0, body="")
    worker.path = worker.final_path if canonical_is_final else worker.raw_path
    final = Path(worker.final_path)
    if prior_final:
        final.write_text("Older output must not masquerade as this empty result.")
    before = inventory(tmp_path)
    [out] = normalize_wave2([worker], "passthrough")
    assert out.status == "success" and out.bytes == 0
    assert out.final_path == ""
    assert out.path == ("" if canonical_is_final else worker.raw_path)
    assert Path(out.meta_path).is_file()
    assert worker.final_path == str(final), "normalization must not mutate input"
    assert all((tmp_path / p).read_bytes() == data for p, data in before.items())


@pytest.mark.parametrize(("body", "status"), [
    ("## Verdict\nGood.\n", "success"), ("unstructured", "success"),
    ("", "success"), (None, "success"), (42, "success"),
    ("failed body", "proxy_error"), ("parse-error body", "parse_error"),
])
@pytest.mark.parametrize("retain", [False, True])
def test_two_partial_resumes_truthful_paths(tmp_path, monkeypatch, body, status, retain):
    output, job, lens = _persist_resume_job(tmp_path, retain_raw=retain, custom_names=True)
    _seed_resume_slot(output, 0, lens)
    calls = []

    def dispatch(preflight_result, **kwargs):
        calls.append(preflight_result.manifest.preflight.workers_requested)
        # One success per invocation leaves a genuine partial job twice.
        worker = WorkerResult(index=0, model_id=f"battle-{len(calls)}", status=status)
        if body is not None:
            worker.body = body
        return [worker]

    monkeypatch.setattr("superclaude.cli.swarm.dispatch.dispatch_wave1", dispatch)
    manifest = (output / "manifest.json").read_bytes()
    missing = []
    for _ in range(2):
        completed = {p: data for p, data in inventory(output).items()
                     if str(p).endswith((".final.md", ".meta.json", ".raw.md"))}
        result = resume(output, job)
        if result.exception and not isinstance(result.exception, SystemExit):
            raise result.exception
        assert result.exit_code in (0, 1), result.output
        contract = yaml.safe_load((output / "return-contract.yaml").read_text())
        assert (output / "manifest.json").read_bytes() == manifest
        assert all((output / p).read_bytes() == data for p, data in completed.items())
        for worker in contract["output_files"]:
            # Failed statuses may retain a planned final write target. Only
            # successful normalization promises a usable final output.
            keys = ("raw_path", "meta_path")
            if worker["status"] == "success":
                keys += ("final_path",)
            else:
                assert worker["status"] == status
                assert worker["final_path"].endswith(".final.md")
                assert not Path(worker["final_path"]).exists()
            for key in keys:
                if worker[key]:
                    if not Path(worker[key]).is_file():
                        missing.append((len(calls), worker["index"], key))
            if not retain:
                assert worker["raw_path"] == ""
        command = contract["recommended_next_command"]
        assert all(w["final_path"] in command for w in contract["output_files"] if w["status"] == "success" and w["final_path"])
    assert len(calls) == 2
    assert not missing, f"advertised paths absent after actual repeated resumes: {missing}"


@pytest.mark.parametrize("prompt_mode", ["empty-defaults", "explicit"])
@pytest.mark.parametrize("force", [False, True])
def test_exact_fresh_resume_provider_parity(tmp_path, monkeypatch, prompt_mode, force):
    from superclaude.cli.swarm import preflight
    from superclaude.cli.swarm.dispatch import dispatch_wave1
    from superclaude.cli.swarm.lenses import LENSES

    target = tmp_path / "target.py"
    target.write_text("# accepted target body\n" * 6)
    output = tmp_path / "out"
    spec = cmd._build_spec_from_lens("bare-review")
    spec["job_id"] = "battle-parity"
    spec["target"]["path"] = str(target)
    spec["output"]["dir"] = str(output)
    spec["transport"]["kind"] = "openai_compat"
    spec["workers"].update(timeout_sec=13, temperature=0.0)
    # The schema requires a guard in an enabled prompt. Disable it explicitly
    # for this harmless fixture so genuinely empty prompt fields are valid.
    spec["target"]["injection_guard"].update(enabled=False, required_substring="")
    spec["prompt"].update({"system": "", "user_template": ""} if prompt_mode == "empty-defaults" else {
        "system": "Accepted explicit system.", "user_template": "Accepted user: {target_content}"})
    sent, policies = [], []

    class Capture:
        def __init__(self, index):
            self.index = index

        def send(self, prompt, timeout_sec):
            sent.append((self.index, prompt, timeout_sec))
            worker = WorkerResult(index=self.index, model_id=f"battle-model-{self.index}", status="success")
            worker.body = "## Verdict\nCaptured model-free review.\n"
            return worker

    def factory(*args, **kwargs):
        return Capture

    def dispatch(*args, **kwargs):
        policies.append(dataclasses.asdict(kwargs["worker_spec"]))
        return dispatch_wave1(*args, **kwargs)

    monkeypatch.setattr(cmd, "_resolve_run_transport_factory", factory)
    monkeypatch.setattr("superclaude.cli.swarm.dispatch.dispatch_wave1", dispatch)
    fresh = CliRunner().invoke(cmd.run_cmd, ["--stdin", "--output", str(output)], input=json.dumps(spec))
    assert fresh.exit_code == 0, fresh.output
    fresh_request = next(row for row in sent if row[0] == 1)
    sent.clear()
    for p in output.glob("*-01-*.meta.json"):
        p.unlink()
    before = inventory(output)
    if force:
        live = dataclasses.replace(LENSES["bare-review"],
            system_prompt_fragment="Intentionally relensed system.", user_template="Live: {target_content}")
        monkeypatch.setattr(preflight, "resolve_lens", lambda _: live)
    result = resume(output, spec["job_id"], force)
    assert result.exit_code == 0, result.output
    assert len(sent) == 1 and sent[0][0] == 1
    assert policies[0] == policies[1], "exact accepted worker policy must survive"
    if prompt_mode == "empty-defaults":
        assert fresh_request[1] == "", "explicitly accepted empty prompt changed"
    else:
        assert target.read_text().splitlines()[0] in fresh_request[1]
    assert all((output / p).read_bytes() == body for p, body in before.items()
               if "-00-" in str(p) or "-02-" in str(p) or p.name == "manifest.json")
    if force:
        assert "Intentionally relensed system." in sent[0][1]
        assert sent[0][1] != fresh_request[1]
    else:
        assert sent[0] == fresh_request, "fresh and ordinary resume requests differ"


def test_completed_replay_without_raw_sibling(tmp_path, monkeypatch):
    output, job, lens = _persist_resume_job(tmp_path)
    for index in range(4):
        _seed_resume_slot(output, index, lens)
    next(output.glob("*-00-*.raw.md")).unlink()
    before = inventory(output)

    def forbidden(*args, **kwargs):
        pytest.fail("completed replay must not redispatch")

    monkeypatch.setattr("superclaude.cli.swarm.dispatch.dispatch_wave1", forbidden)
    for _ in range(2):
        result = resume(output, job)
        assert result.exit_code == 0, result.output
        contract = yaml.safe_load((output / "return-contract.yaml").read_text())
        assert contract["output_files"][0]["raw_path"] == ""
        assert all((output / p).read_bytes() == data for p, data in before.items())


@pytest.mark.parametrize("initial", [True, False])
def test_saved_retention_toggle_between_partial_resumes(tmp_path, monkeypatch, initial):
    output, job, lens = _persist_resume_job(tmp_path, retain_raw=initial)
    _seed_resume_slot(output, 0, lens)
    position = []

    def dispatch(*args, **kwargs):
        position.append(True)
        worker = WorkerResult(index=0, model_id=f"toggle-{len(position)}", status="success")
        worker.body = "## Verdict\nToggle body.\n"
        return [worker]

    monkeypatch.setattr("superclaude.cli.swarm.dispatch.dispatch_wave1", dispatch)
    for retained in (initial, not initial):
        manifest_path = output / "manifest.json"
        data = json.loads(manifest_path.read_text())
        data["retain_raw"] = retained  # deliberate fixture policy edit, no product edit
        manifest_path.write_text(json.dumps(data))
        manifest_bytes = manifest_path.read_bytes()
        before = {p: body for p, body in inventory(output).items() if str(p).endswith((".raw.md", ".meta.json", ".final.md"))}
        result = resume(output, job)
        assert result.exit_code in (0, 1), result.output
        contract = yaml.safe_load((output / "return-contract.yaml").read_text())
        assert manifest_path.read_bytes() == manifest_bytes
        assert all((output / p).read_bytes() == body for p, body in before.items())
        new_worker = next(w for w in contract["output_files"] if w["model_id"] == f"toggle-{len(position)}")
        assert bool(new_worker["raw_path"]) is retained
        if not retained:
            assert all(w["raw_path"] == "" for w in contract["output_files"])
    assert len(position) == 2


@pytest.mark.parametrize("damage", ["same-length", "missing-target", "missing-workers", "missing-prompt", "malformed-prompt", "conflicting-prior"])
def test_battle_provider_recovery_state(tmp_path, monkeypatch, damage):
    output, job, lens = _persist_resume_job(tmp_path)
    for index in (0, 2):
        _seed_resume_slot(output, index, lens)
    manifest_path = output / "manifest.json"
    data = json.loads(manifest_path.read_text())
    data["preflight"]["transport_kind"] = "openai_compat"
    target = Path(data["target"]["path"])
    if damage == "same-length":
        body = target.read_bytes()
        target.write_bytes(body.replace(b"Review", b"review"))
        assert target.stat().st_size == len(body)
    elif damage == "missing-target":
        target.unlink()
    elif damage == "missing-workers":
        data.pop("accepted_workers")
    elif damage == "missing-prompt":
        data.pop("accepted_prompt")
    elif damage == "malformed-prompt":
        data["accepted_prompt"] = []
    else:
        data.pop("accepted_prompt")
        (output / "return-contract.yaml").write_text(yaml.safe_dump({"job_id": "another-job", "lens": "custom", "recommended_next_command": "invented"}))
    manifest_path.write_text(json.dumps(data))
    before = inventory(output)
    calls = []
    monkeypatch.setattr(cmd, "_resolve_run_transport_factory", lambda *a, **k: calls.append(True))
    result = resume(output, job)
    assert result.exit_code != 0
    assert calls == [], "unrecoverable state reached provider construction"
    assert inventory(output) == before
    assert "success" not in result.output.lower()

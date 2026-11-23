"""Model-free regressions for provider recovery and truthful resume artifacts."""
from __future__ import annotations

import json

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

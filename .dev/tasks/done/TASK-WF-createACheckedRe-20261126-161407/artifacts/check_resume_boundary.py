"""Real public-CLI persisted-boundary witness, using only actual stub workers.

Derived from the retained local reproducer; wrappers observe and forward, and
never retire or publish markers themselves. All writes are in pytest temporary
HOME/output roots. Run this file explicitly with pytest despite its check_ name.
"""

import hashlib
import json
from pathlib import Path

import pytest
import yaml
from click.testing import CliRunner

import superclaude.cli.swarm.commands as commands
import superclaude.cli.swarm.dispatch as dispatch
import superclaude.cli.swarm.preflight as preflight
import superclaude.cli.swarm.reduce as reducer
from superclaude.cli.swarm import swarm_group
from superclaude.cli.swarm.transports.stub import StubTransport


def _bytes(root):
    return {
        str(p.relative_to(root)): p.read_bytes() for p in root.rglob("*") if p.is_file()
    }


@pytest.mark.parametrize("enabled", [True, False])
@pytest.mark.parametrize("remaining", [True, False])
def test_actual_cli_boundary(tmp_path, monkeypatch, enabled, remaining):
    home = tmp_path / "home"
    home.mkdir()
    monkeypatch.setenv("HOME", str(home))
    target = tmp_path / "target.md"
    target.write_text("A local simulated review target. " * 12)
    out = tmp_path / "out"
    fresh_args = [
        "run",
        "--lens",
        "bare-review",
        "--transport",
        "stub",
        "--target",
        str(target),
        "--output",
        str(out),
    ]
    fresh = CliRunner().invoke(swarm_group, fresh_args)
    assert fresh.exit_code == 0, fresh.output
    marker = out / "done.json"
    old_marker = marker.read_bytes()
    job_id = json.loads((out / "manifest.json").read_text())["job_id"]
    if remaining:
        meta = sorted(out.glob("*.meta.json"))[0]
        data = json.loads(meta.read_text())
        data["status"] = "timeout"
        meta.write_text(json.dumps(data))
    saved = {}
    for meta in out.glob("*.meta.json"):
        if json.loads(meta.read_text())["status"] == "success":
            final = meta.with_name(meta.name.removesuffix(".meta.json") + ".final.md")
            saved[meta] = meta.read_bytes()
            saved[final] = final.read_bytes()
    assert len(saved) == (4 if remaining else 6)
    # A saved crash snapshot is not evidence of a live process owner.
    commands._write_swarm_state(out, "dispatching", job_id)
    real_rehydrate, real_send = preflight.resume_mode, StubTransport.send
    real_dispatch, real_reduce = dispatch.dispatch_wave1, reducer.reduce_wave3
    real_contract, real_state = reducer.emit_contract, commands._write_swarm_state
    real_marker = reducer.emit_done_sentinel
    events = []

    def record(event, **extra):
        contract = out / "return-contract.yaml"
        events.append(
            {
                "event": event,
                "enabled": enabled,
                "remaining": remaining,
                "marker_exists": marker.exists(),
                "state": json.loads((out / ".swarm-state.json").read_text())["state"],
                "contract_sha256": hashlib.sha256(contract.read_bytes()).hexdigest(),
                **extra,
            }
        )

    def rehydrate(*args, **kwargs):
        spec = real_rehydrate(*args, **kwargs)
        spec.runtime.on_completion.write_done_sentinel = enabled
        return spec

    def overlap():
        before = _bytes(out)
        count = len(events)
        inner = CliRunner().invoke(
            swarm_group,
            ["run", "--resume", job_id, "--output", str(out / ".." / out.name)],
        )
        assert inner.exit_code != 0
        assert _bytes(out) == before
        assert len(events) == count
        record("overlap-rejected", exit_code=inner.exit_code, artifacts_unchanged=True)

    def at_dispatch(*args, **kwargs):
        record("dispatch-entry")
        assert not marker.exists()
        overlap()
        return real_dispatch(*args, **kwargs)

    def inside_stub(self, prompt, timeout):
        record("actual-stub-send", model=self.model)
        assert not marker.exists()
        return real_send(self, prompt, timeout)

    def at_reduce(*args, **kwargs):
        record("reduction-entry")
        assert not marker.exists()
        if not remaining:
            overlap()
        return real_reduce(*args, **kwargs)

    def contract(*args, **kwargs):
        value = real_contract(*args, **kwargs)
        assert not marker.exists()
        record("current-contract-written")
        return value

    def state(root, value, identity):
        assert not marker.exists()
        if value == "terminal":
            assert any(e["event"] == "current-contract-written" for e in events)
        result = real_state(root, value, identity)
        record("terminal-written" if value == "terminal" else "accepted-state-written")
        return result

    def emit_marker(status, contract_path):
        assert events[-1]["event"] == "terminal-written"
        assert yaml.safe_load(Path(contract_path).read_text())["status"] == status
        value = real_marker(status, contract_path)
        record("new-marker-written", status=status)
        return value

    monkeypatch.setattr(preflight, "resume_mode", rehydrate)
    monkeypatch.setattr(dispatch, "dispatch_wave1", at_dispatch)
    monkeypatch.setattr(StubTransport, "send", inside_stub)
    monkeypatch.setattr(reducer, "reduce_wave3", at_reduce)
    monkeypatch.setattr(reducer, "emit_contract", contract)
    monkeypatch.setattr(commands, "_write_swarm_state", state)
    monkeypatch.setattr(reducer, "emit_done_sentinel", emit_marker)
    before = _bytes(out)
    wrong = CliRunner().invoke(
        swarm_group, ["run", "--resume", "wrong-job", "--output", str(out)]
    )
    assert wrong.exit_code != 0
    assert events == []
    assert _bytes(out) == before
    record("validation-rejected", exit_code=wrong.exit_code, artifacts_unchanged=True)
    resumed = CliRunner().invoke(
        swarm_group, ["run", "--resume", job_id, "--output", str(out)]
    )
    for event in events:
        print("BOUNDARY " + json.dumps(event, sort_keys=True))
    print(
        "CLI "
        + json.dumps(
            {
                "enabled": enabled,
                "remaining": remaining,
                "exit_code": resumed.exit_code,
                "fresh_exit_code": fresh.exit_code,
            }
        )
    )
    if resumed.exception and not isinstance(resumed.exception, SystemExit):
        raise resumed.exception
    assert resumed.exit_code == 0, resumed.output
    assert sum(e["event"] == "actual-stub-send" for e in events) == int(remaining)
    assert sum(e["event"] == "dispatch-entry" for e in events) == int(remaining)
    assert sum(e["event"] == "reduction-entry" for e in events) == 1
    publication = [
        e["event"]
        for e in events
        if e["event"]
        in ("current-contract-written", "terminal-written", "new-marker-written")
    ]
    assert publication == ["current-contract-written", "terminal-written"] + (
        ["new-marker-written"] if enabled else []
    )
    assert marker.exists() is enabled
    assert all(p.read_bytes() == data for p, data in saved.items())
    assert not commands._ACTIVE_OUTPUTS
    print(
        "FINAL "
        + json.dumps(
            {
                "enabled": enabled,
                "remaining": remaining,
                "marker_exists": marker.exists(),
                "state": json.loads((out / ".swarm-state.json").read_text())["state"],
                "succeeded_files_unchanged": len(saved),
                "old_marker_bytes_equal": marker.read_bytes() == old_marker
                if marker.exists()
                else False,
                "publication": publication,
                "active_claims": len(commands._ACTIVE_OUTPUTS),
            }
        )
    )

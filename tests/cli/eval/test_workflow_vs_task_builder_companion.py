"""Offline companion checks; never invoke inference or manufacture a suite YAML."""

from __future__ import annotations

import importlib.util
import json
import os
import shutil
from pathlib import Path
from types import SimpleNamespace

import pytest
import yaml

ROOT = Path(__file__).resolve().parents[3]
SPEC = importlib.util.spec_from_file_location(
    "workflow_companion", ROOT / "scripts/eval_workflow_vs_task_builder.py"
)
companion = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(companion)


@pytest.fixture(autouse=True)
def clean_private_test_roots(monkeypatch):
    """Tests remove only the exact private directories they allocate; live runs retain them."""
    original = companion.tempfile.mkdtemp
    roots = []

    def create(*args, **kwargs):
        path = original(*args, **kwargs)
        roots.append(Path(path))
        return path

    monkeypatch.setattr(companion.tempfile, "mkdtemp", create)
    yield
    for root in roots:
        for path in (root, *root.rglob("*")):
            if path.is_dir() and not path.is_symlink():
                path.chmod(0o700)
        shutil.rmtree(root)


def controls():
    return {
        "models": ["vendor/a", "vendor/b", "vendor/c"],
        "judge_model": "vendor/judge",
        "max_calls": 57,
        "max_turns": 20,
        "timeout_seconds": 120,
        "total_seconds": 7200,
        "per_call_budget_usd": 1,
        "total_budget_usd": 57,
        "acknowledge_soft_budget": True,
        "acknowledge_live": True,
    }


def specs():
    # The expanded loader contract retains the ENTIRE parameter list per spec.
    rows = [
        {"model_slot": slot, "effort": effort}
        for slot in (3, 1, 2)
        for effort in reversed(companion.EFFORTS)
    ]
    return [
        SimpleNamespace(id=f"WF{case}.{ordinal}", parameterize=rows)
        for case in (1, 2, 3)
        for ordinal in range(1, 10)
    ]


def rubric():
    return [
        {
            "id": "R1",
            "dimension": "scope",
            "text": "do this",
            "source_path": "spec.md",
            "source_quote": "source",
        },
        {
            "id": "R2",
            "dimension": "safety",
            "text": "safe",
            "source_path": "spec.md",
            "source_quote": "source",
        },
    ]


PKG = "TASK-WF-source-20261009-120000"


def package_of(cwd, slug=PKG):
    return cwd / ".dev/tasks/to-do" / slug


def write_plan(cwd, slug=PKG):
    """Write a merged-contract managed package: <id>.md + source.md + return-contract.yaml."""
    package = package_of(cwd, slug)
    package.mkdir(parents=True)
    shutil.copyfile(cwd / "inputs/source.md", package / "source.md")
    front = {
        "schema": "workflow-plan/1.2",
        "source": "./source.md",
        "strategy": "systematic",
        "depth": "standard",
        "slug": slug,
        "version": "1",
        "priority": "Medium",
        "created_date": "2026-10-09",
    }
    body = "# Plan\nSource: ./source.md\nGoal: preserve source\n"
    for i in range(1, 5):
        body += f"## Phase {i}: phase\n## Task {i}: implement\nAcceptance criteria:\n- Assert expected result.\n"
    (package / f"{slug}.md").write_text(
        "---\n" + yaml.safe_dump(front) + "---\n" + body
    )
    contract = {
        "contract_version": "1.1",
        "status": "success",
        "slug": slug,
        "plan_path": f"./{slug}.md",
        "source_path": "./source.md",
        "source_origin": "inputs/source.md",
        "strategy": "systematic",
        "depth": "standard",
        "handoff_action": "none",
        "handoff_output_path": None,
        "reflect_status": "success",
        "reflect_report_path": "/tmp/reflect/REPORT.md",
        "unresolved": [],
    }
    (package / "return-contract.yaml").write_text(yaml.safe_dump(contract))
    return body


def edit_contract(cwd, **changes):
    path = package_of(cwd) / "return-contract.yaml"
    doc = yaml.safe_load(path.read_text())
    for key, value in changes.items():
        if value is KeyError:
            del doc[key]
        else:
            doc[key] = value
    path.write_text(yaml.safe_dump(doc))


def staged_with_plan(tmp_path):
    cwd, _ = companion.stage(
        tmp_path / "cell", "source", companion.protocol_files(companion.ROOT)
    )
    write_plan(cwd)
    return cwd


def stream(
    path, *, model="vendor/a", tool="Skill", argument=None, tools=None, effort=None
):
    message = {"model": model, "content": []}
    if tool:
        message["content"].append(
            {
                "type": "tool_use",
                "id": "tool-1",
                "name": tool,
                "input": argument or {"skill": "sc:workflow-protocol"},
            }
        )
    events = [
        {
            "type": "system",
            "subtype": "init",
            "permissionMode": "dontAsk",
            "model": model,
            "tools": list(companion.TOOLS) if tools is None else tools,
            "mcp_servers": [],
            "effort": effort,
            "skills": ["sc:workflow-protocol"],
            "slash_commands": ["sc:workflow"],
        },
        {"type": "assistant", "message": message},
    ]
    if tool == "Skill":
        events.append(
            {
                "type": "user",
                "message": {
                    "content": [
                        {
                            "type": "tool_result",
                            "tool_use_id": "tool-1",
                            "content": "Mock canonical Skill loaded",
                            "is_error": False,
                        }
                    ]
                },
            }
        )
    events.append(
        {"type": "result", "subtype": "success", "is_error": False, "result": "{}"}
    )
    path.write_text("\n".join(json.dumps(e) for e in events))
    return events


def test_ordinal_selects_explicit_row_not_implicit_cross_product():
    rows = companion.matrix(specs(), controls()["models"])
    assert rows[0]["model"] == "vendor/c"
    assert rows[0]["effort"] == "high"
    assert rows[4]["model"] == "vendor/a"
    assert rows[4]["effort"] == "medium"
    assert len(rows) == 27


@pytest.mark.parametrize(
    "models", [[], ["one"], ["a", "a", "b"], ["a", "b", "c", "d"], ["auto", "b", "c"]]
)
def test_matrix_model_collection_rejected(models):
    with pytest.raises(ValueError):
        companion.matrix(specs(), models)


@pytest.mark.parametrize(
    "mutate",
    [
        lambda s: s.pop(),
        lambda s: setattr(s[0], "id", "WF1.0"),
        lambda s: setattr(s[0], "id", "WF1.10"),
        lambda s: setattr(s[0], "id", "WF1.2"),
        lambda s: s[0].parameterize[0].update(effort="max"),
        lambda s: s[0].parameterize[0].update(model_slot=True),
        lambda s: s[0].parameterize.__setitem__(0, s[0].parameterize[1]),
    ],
)
def test_matrix_malformed_ordinal_and_rows(mutate):
    entries = specs()
    mutate(entries)
    with pytest.raises(ValueError):
        companion.matrix(entries, controls()["models"])


def test_missing_capabilities_block_and_cli_acceptance_is_not_proof(tmp_path):
    config = controls()
    blockers, _, _ = companion.config_gate(config, tmp_path, {})
    assert len([b for b in blockers if "missing effort" in b]) == 10
    proof = {
        "model": "vendor/a",
        "effort": "low",
        "supported": True,
        "verification": "cli-acceptance",
        "observable_models": ["vendor/a"],
    }
    companion.write_json(tmp_path / "proof.json", proof)
    config["effort_evidence"] = {"vendor/a": {"low": "proof.json"}}
    assert any(
        "CLI acceptance" in b for b in companion.config_gate(config, tmp_path, {})[0]
    )


def test_full_evidence_binds_routing_protocol_and_binary(tmp_path, monkeypatch):
    config = controls()
    config["effort_evidence"] = {}
    for model in [*config["models"], config["judge_model"]]:
        config["effort_evidence"][model] = {}
        for effort in companion.EFFORTS:
            name = model.replace("/", "-") + "-" + effort + ".json"
            companion.write_json(
                tmp_path / name,
                {
                    "model": model,
                    "effort": effort,
                    "supported": True,
                    "verification": "provider request capture",
                    "observable_models": [model],
                },
            )
            config["effort_evidence"][model][effort] = name
    binary = tmp_path / "claude"
    binary.write_bytes(b"not executable; boundary mocked")
    monkeypatch.setattr(companion.shutil, "which", lambda _: str(binary))
    companion.write_json(
        tmp_path / "confinement.json",
        {
            "restricted_paths": True,
            "settings_validated": True,
            "skill_denials": True,
            "discovery_validated": True,
            "protocol_hashes": {"p": "h"},
            "tool_policy": companion.restricted_policy(),
            "settings_sha256": companion.settings_digest(),
            "cli_sha256": companion.digest(binary),
        },
    )
    config["confinement_evidence"] = "confinement.json"
    assert companion.config_gate(config, tmp_path, {"p": "h"})[0] == []
    assert (
        "hash mismatch"
        in companion.config_gate(config, tmp_path, {"p": "different"})[0][-1]
    )


@pytest.mark.parametrize(
    "key,value",
    [
        ("max_calls", 58),
        ("max_calls", True),
        ("max_turns", 0),
        ("timeout_seconds", -1),
        ("per_call_budget_usd", float("inf")),
        ("total_budget_usd", float("nan")),
    ],
)
def test_finite_config_bounds(tmp_path, key, value):
    config = {**controls(), key: value}
    with pytest.raises(ValueError):
        companion.config_gate(config, tmp_path, {})


def test_rubric_exact_quotes_duplicate_and_scores():
    companion.validate_rubric(rubric(), "source")
    with pytest.raises(ValueError, match="quote absent"):
        companion.validate_rubric(rubric(), "different")
    duplicate = [rubric()[0], rubric()[0]]
    with pytest.raises(ValueError):
        companion.validate_rubric(duplicate, "source")
    score = companion.score_judgment(
        {
            "scores": [
                {"id": "R1", "score": 2, "evidence": "artifact"},
                {"id": "R2", "score": 1, "evidence": "artifact"},
            ]
        },
        rubric(),
        "artifact",
    )
    assert score["aggregate"] == 75


@pytest.mark.parametrize(
    "rows",
    [
        [],
        [{"id": "R1", "score": 3, "evidence": "artifact"}],
        [{"id": "R1", "score": True, "evidence": "artifact"}],
        [{"id": "R1", "score": 1, "evidence": "invented"}],
        [{"id": "R1", "score": 2, "evidence": ""}],
        [{"id": "unknown", "score": 0, "evidence": ""}],
        [{"id": "R1", "score": 0, "evidence": ""}] * 2,
    ],
)
def test_invalid_judgments_rejected(rows):
    with pytest.raises(ValueError):
        companion.score_judgment({"scores": rows}, rubric(), "artifact")


def test_real_frozen_corpus_and_hash_mismatch(tmp_path):
    cases = companion.corpus(companion.DEFAULT_CORPUS)
    assert [len(cases[c]["requirements"]) for c in ("WF1", "WF2", "WF3")] == [
        29,
        145,
        104,
    ]
    copied = tmp_path / "corpus"
    shutil.copytree(companion.DEFAULT_CORPUS, copied)
    manifest = companion.read_json(copied / "corpus.json")
    (copied / manifest["cases"][0]["input_path"]).write_text("tampered")
    with pytest.raises(ValueError, match="hash mismatch"):
        companion.corpus(copied)


def test_canonical_staging_argv_environment_and_filesystem(tmp_path, monkeypatch):
    files = companion.protocol_files(companion.ROOT)
    cwd, home = companion.stage(tmp_path / "cell", "source", files)
    skill = "src/superclaude/skills/sc-workflow-protocol/SKILL.md"
    assert (cwd / ".claude/skills/sc-workflow-protocol/SKILL.md").read_bytes() == (
        companion.ROOT / skill
    ).read_bytes()
    assert not list(cwd.rglob("baseline*")) and not list(cwd.rglob("requirements.json"))
    process = companion.process_for(
        cwd,
        home,
        tmp_path,
        "/sc:workflow inputs/source.md",
        "vendor/a",
        "high",
        controls(),
    )
    command = process.build_command()
    assert command[command.index("--effort") + 1] == "high"
    assert (
        "--restricted" in command
        and "--bare" not in command
        and "--strict-mcp-config" in command
    )
    assert "--dangerously-skip-permissions" not in command and "default" not in command
    assert set(command[command.index("--disallowed-tools") + 1].split(",")) == set(
        companion.DENY
    )
    monkeypatch.setenv("AWS_SECRET_ACCESS_KEY", "never forwarded")
    monkeypatch.setenv("ANTHROPIC_LOG", "debug")
    env = process.build_env(env_vars=process._extra_env_vars)
    assert (
        env["HOME"] == str(home)
        and "AWS_SECRET_ACCESS_KEY" not in env
        and "ANTHROPIC_LOG" not in env
    )
    assert (cwd / "inputs/source.md").stat().st_mode & 0o777 == 0o444
    assert cwd.stat().st_mode & 0o777 == 0o555
    # Exactly two writable roots: the workflow package parent and reflect's default output.
    assert companion.WRITABLE_ROOTS == (".dev/tasks/to-do", ".dev/reflect")
    for root in companion.WRITABLE_ROOTS:
        assert (cwd / root).stat().st_mode & 0o777 == 0o700
    assert (cwd / ".dev/tasks").stat().st_mode & 0o777 == 0o555
    assert not (cwd / ".dev/workflow").exists()
    # The reflect pre-review that workflow Wave 4 runs is staged and byte-identical.
    assert (cwd / ".claude/skills/sc-reflect-protocol/SKILL.md").read_bytes() == (
        companion.ROOT / "src/superclaude/skills/sc-reflect-protocol/SKILL.md"
    ).read_bytes()
    assert (cwd / "plugin/skills/reflect-protocol/SKILL.md").exists()
    assert (cwd / ".claude/commands/sc/reflect.md").exists()
    if os.geteuid() != 0:
        companion.filesystem_gate(cwd)
        (cwd / "inputs/source.md").chmod(0o644)
        with pytest.raises(ValueError, match="writable"):
            companion.filesystem_gate(cwd)
    monkeypatch.setattr(companion.os, "geteuid", lambda: 0)
    with pytest.raises(ValueError, match="privileged"):
        companion.filesystem_gate(cwd)


def test_symlink_and_outside_roots_rejected(tmp_path):
    outside = tmp_path / "outside"
    outside.write_text("hidden")
    root = tmp_path / "root"
    root.mkdir()
    (root / "link").symlink_to(outside)
    for target in ("../outside", "link", str(outside)):
        with pytest.raises(ValueError):
            companion.safe_path(root, target)


@pytest.mark.parametrize(
    "change",
    [
        lambda p: p.replace("Task 2:", "Task 8:"),
        lambda p: p + "\n- [ ] not allowed\n",
        lambda p: p + "\n1. not allowed\n",
        lambda p: p + "\nDepends on: Task 8\n",
        lambda p: p.replace("Acceptance criteria:", "Criteria:"),
        lambda p: p.replace("Phase 4:", "not a phase:"),
        lambda p: p + "\nTBD\n",
    ],
)
def test_plan_gates(tmp_path, change):
    cwd = staged_with_plan(tmp_path)
    assert "# Plan" in companion.validate_package(cwd)
    plan = package_of(cwd) / f"{PKG}.md"
    plan.write_text(change(plan.read_text()))
    with pytest.raises(ValueError):
        companion.validate_package(cwd)


@pytest.mark.parametrize("status", ["failed", "partial"])
def test_stop_contracts_fail(tmp_path, status):
    cwd = staged_with_plan(tmp_path)
    edit_contract(cwd, status=status)
    with pytest.raises(ValueError, match="return contract"):
        companion.validate_package(cwd)


def test_package_discovery_fails_closed_on_zero_or_two_packages(tmp_path):
    cwd, _ = companion.stage(
        tmp_path / "cell", "source", companion.protocol_files(companion.ROOT)
    )
    with pytest.raises(ValueError, match="exactly one workflow package"):
        companion.validate_package(cwd)  # zero
    write_plan(cwd)
    write_plan(cwd, "TASK-WF-source-20261009-120001")
    with pytest.raises(ValueError, match="exactly one workflow package"):
        companion.validate_package(cwd)  # two (a retry/rerun must not be guessed at)


def test_valid_package_discovers_and_records_advisory_reflect(tmp_path):
    cwd = staged_with_plan(tmp_path)
    assert companion.discover_package(cwd) == package_of(cwd)
    evidence = companion.package_evidence(cwd)
    assert evidence["package_id"] == PKG
    assert set(evidence["artifact_hashes"]) == {
        f"{PKG}.md",
        "source.md",
        "return-contract.yaml",
    }
    assert evidence["reflect_status"] == "success"
    assert evidence["reflect_report_path"] == "/tmp/reflect/REPORT.md"


@pytest.mark.parametrize(
    "mutate,match",
    [
        # package id must match TASK-WF-source-<date>-<time>[-2..-9]
        (
            lambda c: package_of(c).rename(
                package_of(c, "TASK-WF-other-20261009-120000")
            ),
            "package id",
        ),
        (lambda c: package_of(c).rename(package_of(c, "plan")), "package id"),
        # file stem / slug / dir name must all agree
        (
            lambda c: (package_of(c) / f"{PKG}.md").rename(package_of(c) / "plan.md"),
            "missing or special",
        ),
        (
            lambda c: edit_contract(c, slug="TASK-WF-source-20261009-999999"),
            "return contract",
        ),
    ],
)
def test_slug_filestem_and_dirname_mismatch_rejected(tmp_path, mutate, match):
    cwd = staged_with_plan(tmp_path)
    mutate(cwd)
    with pytest.raises(ValueError, match=match):
        companion.validate_package(cwd)


def test_frontmatter_slug_mismatch_rejected(tmp_path):
    cwd = staged_with_plan(tmp_path)
    plan = package_of(cwd) / f"{PKG}.md"
    plan.write_text(plan.read_text().replace(f"slug: {PKG}", "slug: other"))
    with pytest.raises(ValueError, match="source/slug"):
        companion.validate_package(cwd)


def test_source_snapshot_byte_mismatch_rejected(tmp_path):
    cwd = staged_with_plan(tmp_path)
    snapshot = package_of(cwd) / "source.md"
    snapshot.write_text(snapshot.read_text() + "\n")  # one extra byte
    with pytest.raises(ValueError, match="source.md snapshot differs"):
        companion.validate_package(cwd)


@pytest.mark.parametrize(
    "old,new",
    [
        ("workflow-plan/1.2", "workflow-plan/1.1"),  # retired schema
        ("source: ./source.md", "source: inputs/source.md"),  # not package-relative
    ],
)
def test_retired_schema_and_nonrelative_source_rejected(tmp_path, old, new):
    cwd = staged_with_plan(tmp_path)
    plan = package_of(cwd) / f"{PKG}.md"
    plan.write_text(plan.read_text().replace(old, new))
    with pytest.raises(ValueError):
        companion.validate_package(cwd)


@pytest.mark.parametrize(
    "changes",
    [
        {"contract_version": "1.0"},
        {"plan_path": ".dev/workflow/plan/plan.md"},
        {"plan_path": "plan.md"},
        {"source_path": "inputs/source.md"},
    ],
)
def test_retired_contract_shape_rejected(tmp_path, changes):
    cwd = staged_with_plan(tmp_path)
    edit_contract(cwd, **changes)
    with pytest.raises(ValueError, match="return contract|contract path"):
        companion.validate_package(cwd)


@pytest.mark.parametrize("missing", ["reflect_status", "reflect_report_path"])
def test_reflect_fields_must_be_present(tmp_path, missing):
    cwd = staged_with_plan(tmp_path)
    edit_contract(cwd, **{missing: KeyError})
    with pytest.raises(ValueError, match="missing return contract keys"):
        companion.validate_package(cwd)


def test_reflect_is_advisory_skipped_is_accepted(tmp_path):
    cwd = staged_with_plan(tmp_path)
    edit_contract(
        cwd,
        reflect_status="skipped",
        reflect_report_path=None,
        unresolved=["reflect unavailable: skipped"],
    )
    assert "# Plan" in companion.validate_package(cwd)
    assert companion.package_evidence(cwd)["reflect_status"] == "skipped"
    # ...but a skipped/failed reflect cannot claim a report, and the enum is closed.
    for bad in (
        {"reflect_status": "skipped", "reflect_report_path": "/tmp/r.md"},
        {"reflect_status": "bogus"},
    ):
        edit_contract(cwd, **bad)
        with pytest.raises(ValueError, match="reflect"):
            companion.validate_package(cwd)


def test_workflow_prompt_never_carries_the_retired_output_flag():
    assert "--output" not in companion.WORKFLOW_PROMPT
    assert companion.WORKFLOW_PROMPT.startswith("/sc:workflow inputs/source.md ")
    text = (ROOT / "scripts/eval_workflow_vs_task_builder.py").read_text()
    literals = [m for m in text.splitlines() if '"/sc:workflow' in m]
    assert all("--output" not in ln for ln in literals)


@pytest.mark.parametrize(
    "tool,args,model",
    [
        (None, None, "vendor/a"),
        ("Bash", {}, "vendor/a"),
        ("Agent", {}, "vendor/a"),
        ("Skill", {"skill": "other"}, "vendor/a"),
        ("Read", {"file_path": "../baseline.md"}, "vendor/a"),
        ("Write", {"file_path": "inputs/source.md"}, "vendor/a"),
        ("Skill", None, "fallback/model"),
    ],
)
def test_skill_identity_and_tool_trace_fail_closed(tmp_path, tool, args, model):
    path = tmp_path / "stream.jsonl"
    stream(path, tool=tool, argument=args, model=model)
    with pytest.raises(ValueError):
        companion.stream_result(
            path, "vendor/a", "low", {"observable_models": ["vendor/a"]}, tmp_path, True
        )


def test_stream_missing_telemetry_is_null_and_effort_not_inferred(tmp_path):
    path = tmp_path / "stream.jsonl"
    events = stream(path)
    value = companion.stream_result(
        path, "vendor/a", "low", {"observable_models": ["vendor/a"]}, tmp_path, True
    )
    assert (
        value["effective_effort"] is None
        and value["usage"] is None
        and value["cost_usd"] is None
    )
    events[0]["effort"] = "high"
    path.write_text("\n".join(json.dumps(e) for e in events))
    with pytest.raises(ValueError, match="effort mismatch"):
        companion.stream_result(
            path, "vendor/a", "low", {"observable_models": ["vendor/a"]}, tmp_path, True
        )


@pytest.mark.parametrize("rc,status", [(124, "TIMEOUT"), (2, "FAILED")])
def test_mock_process_timeout_nonzero_terminated_and_reaped(tmp_path, rc, status):
    calls = []
    process = SimpleNamespace(
        start=lambda: calls.append("start"),
        wait=lambda: rc,
        terminate=lambda: calls.append("terminate"),
        _process=SimpleNamespace(wait=lambda timeout: calls.append("reap")),
    )
    result = companion.call(process, {}, "low", True)
    assert result["status"] == status and result["exit_code"] == rc
    assert result["cost_usd"] is None and calls == ["start", "terminate", "reap"]


def test_mock_process_cancellation_terminates_before_return():
    calls = []

    def cancel():
        raise KeyboardInterrupt

    process = SimpleNamespace(
        start=cancel,
        terminate=lambda: calls.append("terminate"),
        _process=SimpleNamespace(wait=lambda timeout: calls.append("reap")),
    )
    with pytest.raises(KeyboardInterrupt):
        companion.call(process, {}, "low", True)
    assert calls == ["terminate", "reap"]


def test_call_time_and_soft_budget_caps(monkeypatch):
    budget = companion.Budget(controls())
    for _ in range(57):
        assert budget.reserve() > 0
        budget.account(0.1)
    with pytest.raises(ValueError, match="budget exhausted"):
        budget.reserve()
    budget = companion.Budget(controls())
    budget.account(None)
    with pytest.raises(ValueError, match="telemetry unavailable"):
        budget.reserve()
    budget = companion.Budget({**controls(), "total_budget_usd": 0.5})
    with pytest.raises(ValueError, match="spend ceiling"):
        budget.reserve()
    budget = companion.Budget(controls())
    monkeypatch.setattr(companion.time, "monotonic", lambda: budget.started + 7201)
    with pytest.raises(ValueError, match="time budget"):
        budget.reserve()


def test_independently_authored_suite_and_prepare_never_spawn(tmp_path, monkeypatch):
    if not companion.DEFAULT_SUITE.exists():
        pytest.skip("independent suite author has not yet produced manifest")
    parsed = companion.SuiteLoader().load(companion.DEFAULT_SUITE)
    assert len(companion.matrix(parsed.evals, controls()["models"])) == 27
    config = tmp_path / "config.json"
    companion.write_json(config, controls())
    monkeypatch.setattr(
        companion.RestrictedProcess,
        "start",
        lambda self: pytest.fail("prepare spawned inference"),
    )
    output = tmp_path / "run"
    assert (
        companion.main(["--config", str(config), "--output", str(output), "--prepare"])
        == 2
    )
    result = companion.read_json(output / "summary.json")
    assert result["mode"] == "offline-prepare" and result["state"] == "BLOCKED"
    assert len(result["rows"]) == 27 and all(
        r["status"] == "BLOCKED" for r in result["rows"]
    )
    assert result["calls"] == 0 and result["cost_usd"] is None
    argv = companion.read_json(output / "plan/argv.json")
    assert len(argv) == 27 and all(
        r["prompt"].startswith("/sc:workflow ") for r in argv
    )
    with pytest.raises(SystemExit):
        companion.main(["--config", str(config), "--output", str(output), "--prepare"])


def install_mock_boundary(
    monkeypatch, calls, *, interrupt=False, unknown_cost=False, bad_baseline=False
):
    # The mocked boundary must not depend on who runs the suite: under root the real
    # guard would return BLOCKED before reaching any process mock.
    monkeypatch.setattr(companion, "privileged", lambda: False)
    evidence = {
        model: {effort: {"observable_models": [model]} for effort in companion.EFFORTS}
        for model in [*controls()["models"], controls()["judge_model"]]
    }
    monkeypatch.setattr(companion, "config_gate", lambda *args: ([], evidence, {}))
    monkeypatch.setenv("ANTHROPIC_API_KEY", "mock-boundary-only")

    def start(process):
        calls.append(process.model)
        if interrupt:
            raise KeyboardInterrupt
        is_generator = process.prompt.startswith("/sc:workflow ")
        if is_generator:
            assert process.prompt == companion.WORKFLOW_PROMPT
            assert "--output" not in process.prompt
            write_plan(process.cwd)
            stream(
                process.output_file, model=process.model, effort=process.extra_args[1]
            )
        else:
            packet = json.loads(process.prompt.split("\n", 1)[1])
            scores = [
                {"id": r["id"], "score": 0, "evidence": ""} for r in packet["rubric"]
            ]
            stream(
                process.output_file,
                model=process.model,
                tool=None,
                tools=[],
                effort="medium",
            )
            events = [
                json.loads(line)
                for line in process.output_file.read_text().splitlines()
            ]
            events[-1]["result"] = json.dumps({"scores": scores})
            if bad_baseline and "baseline-" in str(process.output_file):
                events[-1]["result"] = "not json: malformed baseline judgment"
            process.output_file.write_text("\n".join(json.dumps(e) for e in events))
        events = [
            json.loads(line) for line in process.output_file.read_text().splitlines()
        ]
        if not unknown_cost:
            events[-1]["total_cost_usd"] = 0.1
            events[-1]["usage"] = {"input_tokens": 10, "output_tokens": 20}
        process.output_file.write_text("\n".join(json.dumps(e) for e in events))

    monkeypatch.setattr(companion.RestrictedProcess, "start", start)
    monkeypatch.setattr(companion.RestrictedProcess, "wait", lambda process: 0)
    monkeypatch.setattr(
        companion.RestrictedProcess, "terminate", lambda process: calls.append("reaped")
    )


def test_real_serial_logic_mocked_boundary_57_calls_30_judges(tmp_path, monkeypatch):
    if not companion.DEFAULT_SUITE.exists():
        pytest.skip("independent suite author has not yet produced manifest")
    calls = []
    install_mock_boundary(monkeypatch, calls)
    config = tmp_path / "config.json"
    companion.write_json(config, controls())
    output = tmp_path / "run"
    assert (
        companion.main(
            [
                "--config",
                str(config),
                "--output",
                str(output),
                "--execute",
                "--confirm-live",
            ]
        )
        == 0
    )
    result = companion.read_json(output / "summary.json")
    assert result["state"] == "COMPLETED" and result["mode"] == "actual-companion"
    assert (
        result["calls"] == 57
        and calls.count("vendor/judge") == 30
        and calls.count("reaped") == 57
    )
    assert len(result["rows"]) == 27 and all(
        row["status"] == "SCORED" for row in result["rows"]
    )
    assert all(row["score"] == 0 and row["delta"] == 0 for row in result["rows"])
    assert len(result["baselines"]) == 3 and result[
        "reported_cost_usd"
    ] == pytest.approx(5.7)
    assert result["cost_usd"] is None and result["actual_spend_usd"] is None
    assert "pricing unverified" in result["cost_provenance"]


def test_cancellation_summary_and_unknown_cost_stop_before_more_calls(
    tmp_path, monkeypatch
):
    if not companion.DEFAULT_SUITE.exists():
        pytest.skip("independent suite author has not yet produced manifest")
    config = tmp_path / "config.json"
    companion.write_json(config, controls())
    calls = []
    install_mock_boundary(monkeypatch, calls, interrupt=True)
    output = tmp_path / "cancelled"
    assert (
        companion.main(
            [
                "--config",
                str(config),
                "--output",
                str(output),
                "--execute",
                "--confirm-live",
            ]
        )
        == 130
    )
    result = companion.read_json(output / "summary.json")
    assert calls[-1] == "reaped" and result["state"] == "CANCELLED"
    assert result["rows"][0]["status"] == "CANCELLED" and result["cost_usd"] is None
    assert all(row["status"] == "NOT_RUN" for row in result["rows"][1:])
    calls.clear()
    install_mock_boundary(monkeypatch, calls, unknown_cost=True)
    output = tmp_path / "uncertain"
    assert (
        companion.main(
            [
                "--config",
                str(config),
                "--output",
                str(output),
                "--execute",
                "--confirm-live",
            ]
        )
        == 1
    )
    result = companion.read_json(output / "summary.json")
    assert result["calls"] == 1 and result["cost_usd"] is None
    assert calls == ["vendor/a", "reaped"] and result["state"] == "STOPPED"
    assert all(row["status"] == "NOT_RUN" for row in result["rows"][1:])


def test_stdin_delivery_has_its_own_deadline(tmp_path, monkeypatch):
    import select

    cwd, home = companion.stage(
        tmp_path / "cell", "source", companion.protocol_files(companion.ROOT)
    )
    process = companion.process_for(
        cwd, home, tmp_path, "payload", "vendor/a", "low", controls()
    )
    closed = []
    process._process = SimpleNamespace(
        stdin=SimpleNamespace(fileno=lambda: 99, close=lambda: closed.append(True))
    )
    monkeypatch.setattr(companion.os, "set_blocking", lambda *args: None)
    monkeypatch.setattr(select, "select", lambda *args: ([], [], []))
    monkeypatch.setattr(process, "terminate", lambda: closed.append("terminated"))
    process._write_prompt_to_stdin(b"payload")
    assert isinstance(process._stdin_error, TimeoutError)
    assert closed == ["terminated", True]


def test_execute_without_human_confirmation_or_bare_auth_never_spawns(
    tmp_path, monkeypatch
):
    if not companion.DEFAULT_SUITE.exists():
        pytest.skip("independent suite author has not yet produced manifest")
    calls = []
    install_mock_boundary(monkeypatch, calls)
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    monkeypatch.setenv("ANTHROPIC_AUTH_TOKEN", "do-not-convert")
    config = tmp_path / "config.json"
    companion.write_json(config, controls())
    output = tmp_path / "blocked"
    assert (
        companion.main(["--config", str(config), "--output", str(output), "--execute"])
        == 2
    )
    result = companion.read_json(output / "summary.json")
    assert calls == [] and result["state"] == "BLOCKED"
    assert any("confirm-live" in b for b in result["blockers"])
    assert any("token-only auth" in b for b in result["blockers"])


def test_absolute_source_is_rejected_and_readonly_claude_mentions_are_valid(tmp_path):
    cwd = staged_with_plan(tmp_path)
    plan = package_of(cwd) / f"{PKG}.md"
    original = plan.read_text()
    # An absolute source path is no longer an accepted equivalent: the package links ./source.md.
    plan.write_text(
        original.replace(
            "source: ./source.md", "source: " + str(cwd / "inputs/source.md")
        )
    )
    with pytest.raises(ValueError, match="source/slug"):
        companion.validate_package(cwd)
    plan.write_text(
        original
        + "\nConstraint: do not edit .claude/skills; read .claude/commands only.\n"
    )
    companion.validate_package(cwd)
    plan.write_text(plan.read_text() + "\nOutput: .claude/skills/bad.md\n")
    with pytest.raises(ValueError, match="forbidden output"):
        companion.validate_package(cwd)


def test_attempted_error_stream_is_explicit_and_timeout_status_survives_summary(
    tmp_path, monkeypatch
):
    if not companion.DEFAULT_SUITE.exists():
        pytest.skip("independent suite author has not yet produced manifest")
    calls = []
    install_mock_boundary(monkeypatch, calls)
    config = tmp_path / "config.json"
    companion.write_json(config, controls())
    monkeypatch.setattr(companion.RestrictedProcess, "wait", lambda process: 124)
    output = tmp_path / "timeout"
    assert (
        companion.main(
            [
                "--config",
                str(config),
                "--output",
                str(output),
                "--execute",
                "--confirm-live",
            ]
        )
        == 1
    )
    result = companion.read_json(output / "summary.json")
    assert (
        result["rows"][0]["status"] == "TIMEOUT"
        and result["rows"][0]["exit_code"] == 124
    )
    assert result["rows"][0]["generation_status"] == "TIMEOUT" and result["calls"] == 1

    install_mock_boundary(monkeypatch, calls)
    original_start = companion.RestrictedProcess.start

    def malformed_judge(process):
        original_start(process)
        if process.model == "vendor/judge":
            events = [
                json.loads(line)
                for line in process.output_file.read_text().splitlines()
            ]
            events[-1]["is_error"] = True
            process.output_file.write_text("\n".join(json.dumps(e) for e in events))

    monkeypatch.setattr(companion.RestrictedProcess, "start", malformed_judge)
    output = tmp_path / "judge-error"
    assert (
        companion.main(
            [
                "--config",
                str(config),
                "--output",
                str(output),
                "--execute",
                "--confirm-live",
            ]
        )
        == 1
    )
    result = companion.read_json(output / "summary.json")
    assert result["baselines"]["WF1"]["status"] == "ERRORED"
    assert result["baselines"]["WF1"]["exit_code"] == 0
    assert result["rows"][0]["generation_status"] == "EXECUTED"
    assert result["rows"][0]["format_status"] == "VALID"
    assert result["calls"] == 2


def test_zero_cli_cost_is_not_verified_zero_provider_bill(tmp_path):
    path = tmp_path / "stream.jsonl"
    events = stream(path)
    events[-1]["total_cost_usd"] = 0
    path.write_text("\n".join(json.dumps(e) for e in events))
    value = companion.stream_result(
        path, "vendor/a", "low", {"observable_models": ["vendor/a"]}, tmp_path, True
    )
    assert value["cost_usd"] == 0
    assert (
        value["actual_spend_usd"] is None
        and "pricing unverified" in value["cost_provenance"]
    )


def test_preflight_limits_omit_dollar_cap_and_bearer_is_not_assumed(
    tmp_path, monkeypatch
):
    limits = companion.preflight_limits({"preflight_budget_usd": None})
    assert limits == {
        "max_calls": 10,
        "max_turns": 20,
        "timeout_seconds": 300,
        "total_seconds": 3600,
        "per_call_budget_usd": None,
    }
    cwd, home = companion.stage(
        tmp_path / "cell", "source", companion.protocol_files(companion.ROOT)
    )
    process = companion.process_for(
        cwd, home, tmp_path, "/sc:workflow inputs/source.md", "vendor/a", "low", limits
    )
    assert "--max-budget-usd" not in process.build_command()
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    monkeypatch.setenv("ANTHROPIC_AUTH_TOKEN", "synthetic-private-token")
    assert companion.verified_isolated_auth({}, tmp_path) is False
    with pytest.raises(ValueError):
        companion.preflight_limits({"preflight_max_calls": 11})
    with pytest.raises(ValueError):
        companion.preflight_limits({"preflight_budget_usd": 1})
    with pytest.raises(ValueError):
        process.build_env(
            env_vars={
                "HOME": str(home),
                "CLAUDE_CONFIG_DIR": str(home),
                "ANTHROPIC_BASE_URL": "https://other.invalid",
            }
        )


def test_capability_and_wire_redaction_never_turn_echo_into_support():
    secret = "DO-NOT-PERSIST-PRIVATE-TEXT"
    body = json.dumps(
        {
            "model": "vendor/a",
            "output_config": {"effort": "low"},
            "messages": [{"role": "user", "content": secret}],
            "thinking": {"type": "adaptive", "private": secret},
            "tools": [
                {
                    "name": "Read",
                    "description": secret,
                    "input_schema": {"secret": secret},
                }
            ],
        }
    ).encode()
    wire = companion.wire_subset(body)
    assert wire["model"] == "vendor/a" and wire["effort"] == "low"
    assert secret not in json.dumps(wire)
    metadata = companion.capability_subset(
        {
            "id": "vendor/a",
            "secret": secret,
            "capabilities": {
                "effort": {
                    "supported": True,
                    "low": {"supported": True, "secret": secret},
                }
            },
        },
        "vendor/a",
    )
    assert metadata["capabilities"]["effort"]["low"]["supported"] is True
    assert metadata["capabilities"]["effort"]["medium"]["supported"] is False
    assert secret not in json.dumps(metadata)
    with pytest.raises(ValueError, match="exact-ID"):
        companion.capability_subset({"id": "fallback", "capabilities": {}}, "vendor/a")


def test_recorder_forwards_exact_auth_and_model_without_persisting_secrets(monkeypatch):
    import io

    token = "synthetic-secret-never-log"
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    monkeypatch.setenv("ANTHROPIC_AUTH_TOKEN", token)
    handlers, forwarded, errors = [], [], []

    class FakeServer:
        server_port = 12345

        def __init__(self, address, handler):
            assert address == ("127.0.0.1", 0)
            handlers.append(handler)

        def serve_forever(self):
            pass

        def shutdown(self):
            pass

        def server_close(self):
            pass

    monkeypatch.setattr(companion.http.server, "ThreadingHTTPServer", FakeServer)
    recorder = companion.IngressRecorder(
        "https://approved.invalid/anthropic", 3, ["vendor/a"], 1
    )
    assert recorder.start() == "http://127.0.0.1:12345"

    class Response:
        status = 200

        def getheaders(self):
            return [("Content-Type", "text/event-stream")]

        def read1(self, size):
            if getattr(self, "done", False):
                return b""
            self.done = True
            return b'data: {"type":"message_start","message":{"model":"vendor/a","content":"PRIVATE RESPONSE"}}\n\n'

    class Connection:
        def request(self, method, path, body, headers):
            forwarded.append((method, path, body, headers))

        def getresponse(self):
            return Response()

        def close(self):
            pass

    monkeypatch.setattr(recorder, "connection", Connection)

    def request(model="vendor/a", supplied=token, path="/v1/messages"):
        body = json.dumps(
            {
                "model": model,
                "output_config": {"effort": "low"},
                "messages": [{"role": "user", "content": "PRIVATE PROMPT"}],
                "tools": [],
            }
        ).encode()
        handler = object.__new__(handlers[0])
        handler.path = path
        handler.headers = {
            "Authorization": "Bearer " + supplied,
            "Content-Length": str(len(body)),
            "Host": "loopback",
        }
        handler.rfile, handler.wfile = io.BytesIO(body), io.BytesIO()
        handler.send_response = lambda status: None
        handler.send_header = lambda *args: None
        handler.end_headers = lambda: None
        handler.send_error = lambda status, text: errors.append(status)
        handler.do_POST()

    request(path="/v1/messages?beta=true")
    assert forwarded[0][0:2] == ("POST", "/anthropic/v1/messages?beta=true")
    assert forwarded[0][3]["Authorization"] == "Bearer " + token
    serialized = json.dumps(recorder.records)
    assert (
        token not in serialized
        and "PRIVATE PROMPT" not in serialized
        and "PRIVATE RESPONSE" not in serialized
    )
    assert recorder.records[0]["response_models"] == ["vendor/a"]
    request(supplied="wrong")
    request(model="unapproved")
    request(path="/v1/models")
    request()  # Upstream request ceiling prevents another forward.
    assert len(forwarded) == 1 and recorder.message_requests == 1 and 403 in errors
    recorder.close()
    with pytest.raises(ValueError):
        companion.IngressRecorder(
            "https://userinfo:secret@other.invalid", 1, ["vendor/a"]
        )


def mock_preflight(monkeypatch, *, denied=True, write_attempt=True, write_denied=True):
    monkeypatch.setattr(companion, "privileged", lambda: False)  # root-proof, as above
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    monkeypatch.setenv("ANTHROPIC_AUTH_TOKEN", "mock-private-bearer")
    monkeypatch.setenv("ANTHROPIC_BASE_URL", "https://approved.invalid/anthropic")
    binary = companion.ROOT / "scripts/eval_workflow_vs_task_builder.py"
    monkeypatch.setattr(companion.shutil, "which", lambda _: str(binary))
    recorders = []

    def start_recorder(recorder):
        recorders.append(recorder)
        return "http://127.0.0.1:12345"

    monkeypatch.setattr(companion.IngressRecorder, "start", start_recorder)
    monkeypatch.setattr(
        companion.IngressRecorder,
        "metadata",
        lambda *args: pytest.fail("snapshot must suppress metadata query"),
    )

    def start(process):
        assert "--max-budget-usd" not in process.build_command()
        assert (
            process.build_env(env_vars=process._extra_env_vars)["ANTHROPIC_BASE_URL"]
            == "http://127.0.0.1:12345"
        )
        assert process.prompt == companion.WORKFLOW_PROMPT
        assert "--output" not in process.prompt
        write_plan(process.cwd)
        events = stream(
            process.output_file, model=process.model, effort=process.extra_args[1]
        )
        decoy = process._preflight_decoy
        events.insert(
            2,
            {
                "type": "assistant",
                "message": {
                    "model": process.model,
                    "content": [
                        {
                            "type": "tool_use",
                            "id": "outside",
                            "name": "Read",
                            "input": {"file_path": str(decoy)},
                        }
                    ],
                },
            },
        )
        events.insert(
            3,
            {
                "type": "user",
                "message": {
                    "content": [
                        {
                            "type": "tool_result",
                            "tool_use_id": "outside",
                            "is_error": denied,
                            "content": "mock denial",
                        }
                    ]
                },
            },
        )
        if write_attempt:
            # After the Skill result (index 4): an artifact Write before activation is
            # rejected by the trace gate, as it should be.
            events.insert(
                5,
                {
                    "type": "assistant",
                    "message": {
                        "model": process.model,
                        "content": [
                            {
                                "type": "tool_use",
                                "id": "outside-write",
                                "name": "Write",
                                "input": {
                                    "file_path": str(process._preflight_write_target),
                                    "content": "denied",
                                },
                            }
                        ],
                    },
                },
            )
            events.insert(
                6,
                {
                    "type": "user",
                    "message": {
                        "content": [
                            {
                                "type": "tool_result",
                                "tool_use_id": "outside-write",
                                "is_error": write_denied,
                                "content": "mock write denial",
                            }
                        ]
                    },
                },
            )
        process.output_file.write_text("\n".join(json.dumps(e) for e in events))
        wire = {
            "model": process.model,
            "effort": process.extra_args[1],
            "http_status": 200,
            "auth_method": "bearer",
            "response_models": [process.model],
            "operation": "messages",
            "tools": list(companion.TOOLS),
        }
        recorders[0].records.extend([wire, wire])
        recorders[0].message_requests += 2

    monkeypatch.setattr(companion.RestrictedProcess, "start", start)
    monkeypatch.setattr(companion.RestrictedProcess, "wait", lambda process: 0)
    monkeypatch.setattr(companion.RestrictedProcess, "terminate", lambda process: None)


@pytest.mark.parametrize("metadata_supported", [False, True])
def test_mock_preflight_snapshot_ten_jobs_no_cost_stop_and_genuine_evidence(
    tmp_path, monkeypatch, metadata_supported
):
    mock_preflight(monkeypatch)
    config = {
        **controls(),
        "acknowledge_preflight": True,
        "preflight_budget_usd": None,
        "preflight_metadata_snapshot": "metadata.json",
    }
    _, fingerprint = companion.endpoint_identity()
    records = []
    for model in [*config["models"], config["judge_model"]]:
        row = {
            "model": model,
            "endpoint_sha256": fingerprint,
            "auth_method": "bearer",
            "http_status": 200 if metadata_supported else 404,
        }
        if metadata_supported:
            row["metadata"] = {
                "id": model,
                "capabilities": {
                    "effort": {
                        "supported": True,
                        **{level: {"supported": True} for level in companion.EFFORTS},
                    }
                },
            }
        records.append(row)
    companion.write_json(tmp_path / "metadata.json", {"records": records})
    companion.write_json(tmp_path / "config.json", config)
    output = tmp_path / "preflight"
    assert companion.main(
        [
            "--config",
            str(tmp_path / "config.json"),
            "--output",
            str(output),
            "--preflight",
            "--confirm-live",
        ]
    ) == (0 if metadata_supported else 2)
    summary = companion.read_json(output / "preflight-summary.json")
    assert summary["calls"] == summary["probe_processes"] == 10
    assert summary["upstream_message_request_count"] == 20
    assert summary["actual_spend_usd"] is None and summary["scored"] is False
    assert len(summary["probes"]) == 10 and all(
        p["effective_effort"] is None for p in summary["probes"]
    )
    assert summary["state"] == ("VERIFIED" if metadata_supported else "BLOCKED")
    index = companion.read_json(output / "evidence-index.json")
    assert "confinement_evidence" in index
    assert companion.verified_isolated_auth(index, tmp_path) is True
    assert len(index["effort_evidence"]) == (4 if metadata_supported else 0)
    if metadata_supported:
        launch_config = {**config, **index}
        assert (
            companion.config_gate(launch_config, tmp_path, summary["protocol_hashes"])[
                0
            ]
            == []
        )
    monkeypatch.setenv("ANTHROPIC_BASE_URL", "https://different.invalid")
    assert companion.verified_isolated_auth(index, tmp_path) is False


def test_preflight_expected_denial_cannot_hide_successful_escape(tmp_path):
    path = tmp_path / "stream.jsonl"
    decoy = tmp_path.parent / "public-decoy.md"
    events = stream(path)
    events.insert(
        2,
        {
            "type": "assistant",
            "message": {
                "content": [
                    {
                        "type": "tool_use",
                        "id": "read",
                        "name": "Read",
                        "input": {"file_path": str(decoy)},
                    }
                ]
            },
        },
    )
    events.insert(
        3,
        {
            "type": "user",
            "message": {
                "content": [
                    {"type": "tool_result", "tool_use_id": "read", "is_error": True}
                ]
            },
        },
    )
    path.write_text("\n".join(json.dumps(e) for e in events))
    proof = {"observable_models": ["vendor/a"]}
    companion.stream_result(path, "vendor/a", "low", proof, tmp_path, True, (decoy,))
    with pytest.raises(ValueError):
        companion.stream_result(path, "vendor/a", "low", proof, tmp_path, True)
    events[3]["message"]["content"][0]["is_error"] = False
    path.write_text("\n".join(json.dumps(e) for e in events))
    with pytest.raises(ValueError):
        companion.stream_result(
            path, "vendor/a", "low", proof, tmp_path, True, (decoy,)
        )


def test_preflight_without_explicit_confirmation_never_contacts_endpoint(
    tmp_path, monkeypatch
):
    config = {**controls(), "acknowledge_preflight": True, "preflight_budget_usd": None}
    companion.write_json(tmp_path / "config.json", config)
    monkeypatch.setattr(
        companion.IngressRecorder,
        "start",
        lambda *args: pytest.fail("unapproved contact"),
    )
    with pytest.raises(SystemExit):
        companion.main(
            [
                "--config",
                str(tmp_path / "config.json"),
                "--output",
                str(tmp_path / "run"),
                "--preflight",
            ]
        )


def test_preflight_successful_outside_read_stops_and_preserves_nine_not_run(
    tmp_path, monkeypatch
):
    mock_preflight(monkeypatch, denied=False)
    config = {
        **controls(),
        "acknowledge_preflight": True,
        "preflight_budget_usd": None,
        "preflight_metadata_snapshot": "metadata.json",
    }
    companion.write_json(
        tmp_path / "metadata.json",
        {
            "records": [
                {
                    "model": model,
                    "endpoint_sha256": companion.endpoint_identity()[1],
                    "auth_method": "bearer",
                    "http_status": 404,
                }
                for model in [*config["models"], config["judge_model"]]
            ]
        },
    )
    companion.write_json(tmp_path / "config.json", config)
    output = tmp_path / "partial"
    assert (
        companion.main(
            [
                "--config",
                str(tmp_path / "config.json"),
                "--output",
                str(output),
                "--preflight",
                "--confirm-live",
            ]
        )
        == 1
    )
    result = companion.read_json(output / "preflight-summary.json")
    assert result["state"] == "STOPPED" and result["probe_processes"] == 1
    assert result["probes"][0]["status"] == "ERRORED"
    assert all(row["status"] == "NOT_RUN" for row in result["probes"][1:])
    assert "confinement_evidence" not in result["evidence_index"]


def test_system_string_message_denial_shape_matches_actual_cli(tmp_path):
    path = tmp_path / "stream.jsonl"
    decoy = tmp_path.parent / "public-decoy.md"
    events = stream(path)
    events.insert(
        3,
        {
            "type": "assistant",
            "message": {
                "content": [
                    {
                        "type": "tool_use",
                        "id": "outside",
                        "name": "Read",
                        "input": {"file_path": str(decoy)},
                    }
                ]
            },
        },
    )
    events.insert(
        4,
        {
            "type": "system",
            "subtype": "permission_denied",
            "tool_use_id": "outside",
            "message": "--restricted: public decoy outside working directory",
        },
    )
    events.insert(
        5,
        {
            "type": "user",
            "message": {
                "content": [
                    {
                        "type": "tool_result",
                        "tool_use_id": "outside",
                        "is_error": True,
                        "content": "denied",
                    }
                ]
            },
        },
    )
    path.write_text("\n".join(json.dumps(e) for e in events))
    assert companion.probe_trace(path, tmp_path, decoy) is True
    assert (
        companion.stream_result(
            path,
            "vendor/a",
            "low",
            {"observable_models": ["vendor/a"]},
            tmp_path,
            True,
            (decoy,),
        )["skill_activated"]
        is True
    )


@pytest.mark.parametrize("kind", ["missing", "denied", "parallel", "wrapper-only"])
def test_protocol_activation_requires_successful_result_before_writes(tmp_path, kind):
    path = tmp_path / "stream.jsonl"
    events = stream(path)
    write = {
        "type": "tool_use",
        "id": "write",
        "name": "Write",
        "input": {
            "file_path": f".dev/tasks/to-do/{PKG}/{PKG}.md",
            "content": "not enough",
        },
    }
    if kind == "missing":
        events.pop(2)
    elif kind == "denied":
        events[2]["message"]["content"][0]["is_error"] = True
    elif kind == "parallel":
        events[1]["message"]["content"].append(write)
    else:
        events[1]["message"]["content"][0]["input"]["skill"] = "sc:workflow"
    if kind != "parallel":
        events.insert(-1, {"type": "assistant", "message": {"content": [write]}})
    path.write_text("\n".join(json.dumps(e) for e in events))
    with pytest.raises(ValueError, match="before successful protocol"):
        companion.stream_result(
            path, "vendor/a", "low", {"observable_models": ["vendor/a"]}, tmp_path, True
        )


@pytest.mark.parametrize("missing", ["tool", "command", "protocol"])
def test_discovery_missing_is_fail_closed_even_when_files_or_prompt_exist(
    tmp_path, missing
):
    path = tmp_path / "stream.jsonl"
    events = stream(path)
    if missing == "tool":
        events[0]["tools"] = ["Edit", "Read"]
    elif missing == "command":
        events[0]["slash_commands"] = ["builtin-only"]
    else:
        events[0]["skills"] = ["builtin-only"]
    path.write_text("\n".join(json.dumps(e) for e in events))
    with pytest.raises(ValueError, match="absent|not discovered"):
        companion.stream_result(
            path, "vendor/a", "low", {"observable_models": ["vendor/a"]}, tmp_path, True
        )


def test_private_nonbare_staging_collection_keeps_original_contract_and_hides_home(
    tmp_path, monkeypatch
):
    directory = tmp_path / "cell"
    cwd, home = companion.stage(
        directory, "source", companion.protocol_files(companion.ROOT)
    )
    assert cwd.is_relative_to(Path("/tmp")) and not cwd.is_relative_to(companion.ROOT)
    assert cwd.parent.stat().st_mode & 0o777 == 0o500
    process = companion.process_for(
        cwd,
        home,
        tmp_path,
        "/sc:workflow inputs/source.md",
        "vendor/a",
        "low",
        controls(),
    )
    argv = process.build_command()
    assert "--bare" not in argv
    assert argv[argv.index("--setting-sources") + 1] == "project"
    assert companion.restricted_policy()["setting_sources"] == "project"
    plugin = cwd / "plugin"
    assert argv[argv.index("--plugin-dir") + 1] == str(plugin)
    assert companion.read_json(plugin / ".claude-plugin/plugin.json")["name"] == "sc"
    frozen = companion.protocol_files(companion.ROOT)
    assert (plugin / "commands/workflow.md").read_bytes() == frozen[
        "src/superclaude/commands/workflow.md"
    ]
    assert (plugin / "skills/workflow-protocol/SKILL.md").read_bytes() == frozen[
        "src/superclaude/skills/sc-workflow-protocol/SKILL.md"
    ]
    settings = companion.read_json(cwd / "settings.json")
    assert (
        settings["disableAllHooks"] is True
        and settings["disableSkillShellExecution"] is True
    )
    env = process.build_env(env_vars=process._extra_env_vars)
    assert env["CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC"] == "1"
    assert env["CLAUDE_CODE_DISABLE_OFFICIAL_MARKETPLACE_AUTOINSTALL"] == "1"
    write_plan(cwd)
    contract = package_of(cwd) / "return-contract.yaml"
    original = contract.read_bytes()
    (home / ".claude/credentials.json").write_text("MOCK_SECRET_MUST_NOT_COLLECT")
    monkeypatch.setattr(companion, "ROOT", tmp_path / "unrelated-live-source")
    companion.validate_package(cwd)  # Only frozen staged template is read.
    companion.collect_stage(cwd)
    captured = directory / "captured-fixture"
    assert (
        captured / f".dev/tasks/to-do/{PKG}/return-contract.yaml"
    ).read_bytes() == original
    assert not list(directory.rglob("credentials.json"))
    assert companion.read_json(directory / "collection.json")["original_cwd"] == str(
        cwd
    )
    assert (
        companion.read_json(directory / "collection.json")["paths_rewritten"] is False
    )


def test_unexpected_preflight_parser_exception_always_saves_terminal_state(
    tmp_path, monkeypatch
):
    mock_preflight(monkeypatch)
    config = {
        **controls(),
        "acknowledge_preflight": True,
        "preflight_budget_usd": None,
        "preflight_metadata_snapshot": "metadata.json",
    }
    companion.write_json(
        tmp_path / "metadata.json",
        {
            "records": [
                {
                    "model": model,
                    "endpoint_sha256": companion.endpoint_identity()[1],
                    "auth_method": "bearer",
                    "http_status": 404,
                }
                for model in [*config["models"], config["judge_model"]]
            ]
        },
    )
    companion.write_json(tmp_path / "config.json", config)

    def broken(*args):
        raise AttributeError("synthetic unknown parser shape")

    monkeypatch.setattr(companion, "probe_trace", broken)
    output = tmp_path / "parser-error"
    assert (
        companion.main(
            [
                "--config",
                str(tmp_path / "config.json"),
                "--output",
                str(output),
                "--preflight",
                "--confirm-live",
            ]
        )
        == 1
    )
    result = companion.read_json(output / "preflight-summary.json")
    assert result["state"] == "STOPPED" and result["error"] == "AttributeError"
    assert result["probes"][0]["status"] == "ERRORED"
    assert all(row["status"] == "NOT_RUN" for row in result["probes"][1:])


def test_explicit_case_only_responses_and_sdk_recovery_preserve_controls(monkeypatch):
    model = "Qwen3.8-max"
    names = companion.observed_model_names(
        {"observed_model_aliases": {model: ["qwen3.8-max"]}}, model
    )
    assert names == [model, "qwen3.8-max"]
    with pytest.raises(ValueError, match="not model substitutions"):
        companion.observed_model_names(
            {"observed_model_aliases": {model: ["vendor/other"]}}, model
        )
    monkeypatch.setattr(companion, "auth_method", lambda: "bearer")
    common = {
        "model": model,
        "effort": "low",
        "auth_method": "bearer",
        "tools": ["Read", "Skill"],
    }
    recovered = [
        dict(common, http_status=400, response_models=[]),
        dict(common, http_status=200, response_models=["qwen3.8-max"]),
        dict(common, http_status=200, response_models=["qwen3.8-max"]),
    ]
    assert companion.transport_verified(recovered, model, "low", names)
    assert not companion.transport_verified(recovered, model, "low", [model])
    assert not companion.transport_verified(
        [dict(recovered[0], effort="medium"), *recovered[1:]], model, "low", names
    )
    assert not companion.transport_verified(
        [
            recovered[0],
            recovered[1],
            dict(recovered[2], response_models=["vendor/other"]),
        ],
        model,
        "low",
        names,
    )


def _with_reflect(path, *, ok=True):
    """Workflow Skill (ok) -> advisory reflect Skill, as the merged workflow's Wave 4 does."""
    events = stream(path)
    events[0]["skills"].append("sc:reflect-protocol")
    events.insert(
        -1,
        {
            "type": "assistant",
            "message": {
                "model": "vendor/a",
                "content": [
                    {
                        "type": "tool_use",
                        "id": "tool-reflect",
                        "name": "Skill",
                        "input": {"skill": "sc:reflect-protocol"},
                    }
                ],
            },
        },
    )
    events.insert(
        -1,
        {
            "type": "user",
            "message": {
                "content": [
                    {
                        "type": "tool_result",
                        "tool_use_id": "tool-reflect",
                        "content": "Mock reflect Skill loaded" if ok else "",
                        "is_error": not ok,
                    }
                ]
            },
        },
    )
    path.write_text("\n".join(json.dumps(e) for e in events))


def _result(path, tmp_path):
    return companion.stream_result(
        path, "vendor/a", "low", {"observable_models": ["vendor/a"]}, tmp_path, True
    )


def test_reflect_skill_is_allowed_and_recorded_but_never_required(tmp_path):
    plain = tmp_path / "plain.jsonl"
    stream(plain)
    base = _result(plain, tmp_path)
    assert base["skill_activated"] is True
    assert base["reflect_skill_activated"] is False  # advisory: not required
    assert base["reflect_protocol_discovered"] is False
    with_reflect = tmp_path / "reflect.jsonl"
    _with_reflect(with_reflect)
    seen = _result(with_reflect, tmp_path)
    assert seen["skill_activated"] and seen["reflect_skill_activated"] is True
    assert seen["reflect_protocol_discovered"] is True
    failed = tmp_path / "reflect-denied.jsonl"
    _with_reflect(failed, ok=False)
    assert _result(failed, tmp_path)["reflect_skill_activated"] is False


@pytest.mark.parametrize(
    "target,ok",
    [
        (f".dev/tasks/to-do/{PKG}/{PKG}.md", True),
        (".dev/tasks/to-do/" + PKG + "/source.md", True),
        (".dev/reflect/pre-source-20261009120000/REPORT.md", True),
        (".dev/tasks/done/x/x.md", False),  # archive area is not writable
        (".dev/tasks/other.md", False),
        (".dev/workflow/plan/plan.md", False),  # retired root
        ("inputs/source.md", False),
    ],
)
def test_writes_confined_to_package_parent_and_reflect_output(tmp_path, target, ok):
    path = tmp_path / "stream.jsonl"
    events = stream(path)
    events.insert(
        -1,
        {
            "type": "assistant",
            "message": {
                "content": [
                    {
                        "type": "tool_use",
                        "id": "w1",
                        "name": "Write",
                        "input": {"file_path": target, "content": "x"},
                    }
                ]
            },
        },
    )
    path.write_text("\n".join(json.dumps(e) for e in events))
    if ok:
        assert _result(path, tmp_path)["skill_activated"] is True
    else:
        with pytest.raises(ValueError):
            _result(path, tmp_path)


def test_settings_allow_only_the_two_writable_roots_and_both_skills():
    allow = companion.fixture_settings()["permissions"]["allow"]
    assert [a for a in allow if a.startswith("Edit(")] == [
        "Edit(/.dev/tasks/to-do/**)",
        "Edit(/.dev/reflect/**)",
    ]
    assert {"Skill(sc:workflow-protocol)", "Skill(sc:reflect-protocol)"} <= set(allow)
    assert not any("workflow/plan" in a for a in allow)
    assert companion.restricted_policy()["writable_roots"] == list(
        companion.WRITABLE_ROOTS
    )


# --- review follow-ups: baseline completion, write probe, scoring notes, root-proof mocks ---


def _run_execute(tmp_path, name):
    config = tmp_path / "config.json"
    companion.write_json(config, controls())
    output = tmp_path / name
    rc = companion.main(
        [
            "--config",
            str(config),
            "--output",
            str(output),
            "--execute",
            "--confirm-live",
        ]
    )
    return rc, companion.read_json(output / "summary.json")


def test_baseline_judge_failure_is_never_a_completed_pass(tmp_path, monkeypatch):
    if not companion.DEFAULT_SUITE.exists():
        pytest.skip("independent suite author has not yet produced manifest")
    install_mock_boundary(monkeypatch, [], bad_baseline=True)
    rc, result = _run_execute(tmp_path, "bad-baseline")
    # Candidates all score, but no baseline did, so no delta exists: not a PASS.
    assert rc == 1
    assert result["state"] == "COMPLETED"
    assert all(row["status"] == "SCORED" for row in result["rows"])
    assert all(row.get("delta") is None for row in result["rows"])
    assert {b["status"] for b in result["baselines"].values()} == {"INVALID_JUDGMENT"}
    for cid in ("WF1", "WF2", "WF3"):
        assert any(
            f"baseline judgment not SCORED: {cid}" in b for b in result["blockers"]
        )


def test_mock_boundaries_are_root_proof(monkeypatch):
    monkeypatch.setattr(companion.os, "geteuid", lambda: 0)
    assert companion.privileged() is True
    install_mock_boundary(monkeypatch, [])
    assert companion.privileged() is False
    monkeypatch.setattr(companion.os, "geteuid", lambda: 0)
    monkeypatch.undo()  # restore, then prove mock_preflight neutralises it independently
    monkeypatch.setattr(companion.os, "geteuid", lambda: 0)
    mock_preflight(monkeypatch)
    assert companion.privileged() is False


def _write_stream(path, tmp_path, use_id, name, target, is_error):
    events = stream(path)
    events.insert(
        2,
        {
            "type": "assistant",
            "message": {
                "content": [
                    {
                        "type": "tool_use",
                        "id": use_id,
                        "name": name,
                        "input": {"file_path": str(target), "content": "x"},
                    }
                ]
            },
        },
    )
    events.insert(
        3,
        {
            "type": "user",
            "message": {
                "content": [
                    {
                        "type": "tool_result",
                        "tool_use_id": use_id,
                        "is_error": is_error,
                        "content": "result",
                    }
                ]
            },
        },
    )
    path.write_text("\n".join(json.dumps(e) for e in events))


def test_probe_write_trace_requires_an_attempted_and_refused_write(tmp_path):
    target = tmp_path.parent / "write-target.md"
    path = tmp_path / "stream.jsonl"
    _write_stream(path, tmp_path, "w", "Write", target, True)
    assert companion.probe_write_trace(path, tmp_path, target) is True
    _write_stream(path, tmp_path, "w", "Write", target, False)  # write succeeded
    assert companion.probe_write_trace(path, tmp_path, target) is False
    _write_stream(path, tmp_path, "w", "Read", target, True)  # never tried to write
    assert companion.probe_write_trace(path, tmp_path, target) is False
    _write_stream(path, tmp_path, "w", "Write", tmp_path.parent / "other.md", True)
    assert companion.probe_write_trace(path, tmp_path, target) is False


def _snapshot_config(tmp_path, supported=True):
    config = {
        **controls(),
        "acknowledge_preflight": True,
        "preflight_budget_usd": None,
        "preflight_metadata_snapshot": "metadata.json",
    }
    _, fingerprint = companion.endpoint_identity()
    records = []
    for model in [*config["models"], config["judge_model"]]:
        row = {
            "model": model,
            "endpoint_sha256": fingerprint,
            "auth_method": "bearer",
            "http_status": 200 if supported else 404,
        }
        if supported:
            row["metadata"] = {
                "id": model,
                "capabilities": {
                    "effort": {
                        "supported": True,
                        **{lv: {"supported": True} for lv in companion.EFFORTS},
                    }
                },
            }
        records.append(row)
    companion.write_json(tmp_path / "metadata.json", {"records": records})
    companion.write_json(tmp_path / "config.json", config)


def _preflight(tmp_path, name):
    output = tmp_path / name
    rc = companion.main(
        [
            "--config",
            str(tmp_path / "config.json"),
            "--output",
            str(output),
            "--preflight",
            "--confirm-live",
        ]
    )
    return rc, output


def test_preflight_successful_outside_write_stops_and_certifies_nothing(
    tmp_path, monkeypatch
):
    mock_preflight(monkeypatch, write_denied=False)
    _snapshot_config(tmp_path)
    rc, output = _preflight(tmp_path, "write-escape")
    result = companion.read_json(output / "preflight-summary.json")
    assert rc == 1 and result["state"] == "STOPPED" and result["probe_processes"] == 1
    assert result["probes"][0]["status"] == "ERRORED"
    assert "confinement_evidence" not in result["evidence_index"]


def test_preflight_without_a_write_attempt_does_not_certify_restricted_paths(
    tmp_path, monkeypatch
):
    mock_preflight(monkeypatch, write_attempt=False)
    _snapshot_config(tmp_path)
    rc, output = _preflight(tmp_path, "no-write-attempt")
    result = companion.read_json(output / "preflight-summary.json")
    assert rc == 2 and result["state"] != "VERIFIED"
    assert all(p["status"] != "VERIFIED" for p in result["probes"])
    assert all(p.get("outside_write_denied") is False for p in result["probes"])
    assert "confinement_evidence" not in result["evidence_index"]


def test_preflight_with_read_and_write_denied_certifies_restricted_paths(
    tmp_path, monkeypatch
):
    mock_preflight(monkeypatch)
    _snapshot_config(tmp_path)
    rc, output = _preflight(tmp_path, "both-denied")
    result = companion.read_json(output / "preflight-summary.json")
    assert rc == 0 and result["state"] == "VERIFIED"
    assert all(p["outside_write_denied"] is True for p in result["probes"])
    proof = companion.read_json(output / "confinement-evidence.json")
    assert proof["restricted_paths"] is True and "Write" in proof["verification"]


REQS = [
    {"id": "A", "dimension": "testability"},
    {"id": "B", "dimension": "testability"},  # restates A
    {"id": "C", "dimension": "testability"},
    {"id": "D", "dimension": "safety"},
]


def _payload(**scores):
    # nonzero scores must quote exact artifact text; the test artifact body is "quote"
    return {
        "scores": [
            {"id": k, "score": v, "evidence": "quote" if v else ""}
            for k, v in scores.items()
        ]
    }


def test_score_judgment_excluded_rows_are_judged_but_not_weighted():
    body = "quote"
    plain = companion.score_judgment(_payload(A=2, B=0, C=2, D=2), REQS, body)
    assert plain["dimensions"]["testability"] == pytest.approx(100 * 4 / 6)
    notes = {"B": {"kind": "corroborates", "target": "A"}}
    weighted = companion.score_judgment(_payload(A=2, B=0, C=2, D=2), REQS, body, notes)
    assert weighted["dimensions"]["testability"] == 100  # B no longer takes a slot
    assert weighted["excluded"] == notes
    # still judged: dropping the excluded row from the judgment is a missing ID
    with pytest.raises(ValueError, match="missing judgment IDs"):
        companion.score_judgment(_payload(A=2, C=2, D=2), REQS, body, notes)


@pytest.mark.parametrize(
    "notes",
    [
        {"corroborates": {"Z": "A"}, "superseded_by": {}},  # unknown id
        {"corroborates": {"B": "Z"}, "superseded_by": {}},  # unknown target
        {"corroborates": {"B": "B"}, "superseded_by": {}},  # self reference
        {"corroborates": {"D": "A"}, "superseded_by": {}},  # crosses dimensions
        {"corroborates": {"B": "A"}, "superseded_by": {"B": "C"}},  # excluded twice
        {"corroborates": {"B": "A", "A": "C"}, "superseded_by": {}},  # chain
        {"corroborates": {}},  # missing key
    ],
)
def test_scoring_notes_reject_invalid_overlays(notes):
    with pytest.raises(ValueError):
        companion.scoring_notes(
            {"schema": companion.SCORING_NOTES_SCHEMA, **notes}, REQS
        )
    with pytest.raises(ValueError, match="invalid scoring notes"):
        companion.scoring_notes(
            {"schema": "wrong", "corroborates": {}, "superseded_by": {}}, REQS
        )


def test_frozen_corpus_pins_scoring_notes_and_excludes_the_reviewed_rows():
    cases = companion.corpus(companion.DEFAULT_CORPUS)
    assert set(cases["WF1"]["excluded"]) == {"WF1-R021"}
    assert set(cases["WF2"]["excluded"]) == {"WF2-R082", "WF2-R140"}
    assert set(cases["WF3"]["excluded"]) == {"WF3-R043", "WF3-R093", "WF3-R003"}
    assert cases["WF3"]["excluded"]["WF3-R003"] == {
        "kind": "superseded_by",
        "target": "WF3-R038",
    }
    # governing/primary rows stay weighted; the requirement counts are unchanged
    for primary in ("WF1-R019", "WF2-R061", "WF3-R006", "WF3-R068", "WF3-R038"):
        assert all(primary not in c["excluded"] for c in cases.values())
    assert [len(cases[c]["requirements"]) for c in ("WF1", "WF2", "WF3")] == [
        29,
        145,
        104,
    ]
    assert all("scoring-notes.json" in c["hashes"] for c in cases.values())


def test_scoring_notes_are_hash_pinned(tmp_path):
    copy = tmp_path / "corpus"
    shutil.copytree(companion.DEFAULT_CORPUS, copy)
    notes = copy / "reflect-integration" / "scoring-notes.json"
    data = json.loads(notes.read_text())
    data["superseded_by"] = {}
    notes.write_text(json.dumps(data, indent=2) + "\n")
    with pytest.raises(ValueError, match="hash mismatch"):
        companion.corpus(copy)

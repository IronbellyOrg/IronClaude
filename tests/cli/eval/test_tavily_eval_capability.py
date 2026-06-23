"""C7 / M2 drift guards for the Tavily eval capability + the E16 verification eval.

CI-safe: pure registry + manifest parsing through the same loader path
``eval describe`` uses; no live eval run, no network, no TAVILY_API_KEY required.

Note: the task referred to this eval as ``E-tavily-search``; it is registered as
``E16`` because the FR-SCH2 eval-id regex forbids hyphens (user-approved rename).
"""

import yaml

from superclaude.cli.eval.capabilities import _DEFAULT_CAPABILITY_SPECS
from superclaude.cli.eval.commands import _DEFAULT_SUITES_DIR, resolve_suite_manifest
from superclaude.cli.eval.loader import validate_manifest

_CAP = "mcp_server.tavily"
_TOOL = "mcp__tavily__tavily-search"


def _real_manifest_path():
    return resolve_suite_manifest("real", _DEFAULT_SUITES_DIR)


def test_capabilities_registers_mcp_server_tavily():
    """M2: mcp_server.tavily is a mandatory _DEFAULT_CAPABILITY_SPECS row (kind mcp_server)."""
    by_name = {s.name: s for s in _DEFAULT_CAPABILITY_SPECS}
    assert _CAP in by_name, f"{_CAP} not registered in _DEFAULT_CAPABILITY_SPECS (M2)"
    assert by_name[_CAP].kind == "mcp_server"


def test_real_suite_has_tavily_capability_and_verification_eval():
    """The real suite resolves mcp_server.tavily and carries the E16 verification eval."""
    path = _real_manifest_path()
    # Parses through the same loader path `eval describe --suite real` uses.
    specs = validate_manifest(path)
    matches = [s for s in specs if s.id == "E16"]
    assert matches, "E16 tavily verification eval not present in the real suite"
    spec = matches[0]
    assert _CAP in spec.requires, f"E16 must require {_CAP}: {spec.requires}"
    tool_calls = [i.get("expect_tool_call") for i in spec.inputs]
    assert _TOOL in tool_calls, f"E16 must expect {_TOOL}: {tool_calls}"

    raw = yaml.safe_load(path.read_text(encoding="utf-8"))
    cap_names = {c["name"] for c in raw.get("optional_capabilities", [])}
    assert _CAP in cap_names, (
        "real suite optional_capabilities missing mcp_server.tavily"
    )


def test_tavily_eval_gated_to_skip_without_key():
    """The eval SKIPs cleanly (not fails) when Tavily is unreachable / no key — failure_mode: skip."""
    raw = yaml.safe_load(_real_manifest_path().read_text(encoding="utf-8"))
    cap = next((c for c in raw["optional_capabilities"] if c["name"] == _CAP), None)
    assert cap is not None, f"{_CAP} missing from real suite optional_capabilities"
    assert cap["failure_mode"] == "skip"
    assert cap.get("gate_flag") == "--no-mcp"
    # The default-spec gate agrees, so non-real suites resolve the capability too (M2).
    by_name = {s.name: s for s in _DEFAULT_CAPABILITY_SPECS}
    assert by_name[_CAP].failure_mode == "skip"

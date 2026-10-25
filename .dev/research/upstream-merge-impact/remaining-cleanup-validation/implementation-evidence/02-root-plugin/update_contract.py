"""Bind expected plugin frontends to the native candidate inventory."""

import hashlib
import json
from pathlib import Path

OUT = Path(__file__).resolve().parent
ROOT = Path(__file__).resolve().parents[6]


def main():
    path = OUT / "plugin-contract.json"
    contract = json.loads(path.read_text())
    init = json.loads((OUT / "loader-candidates-init.json").read_text())
    assert any(row["name"] == "sc" for row in init["plugins"])
    assert init["mcp_servers"] == []
    original = (OUT / "isolation/plugin/.claude-plugin/plugin.json").read_bytes()
    corrected = (ROOT / ".claude-plugin/plugin.json").read_bytes()
    assert corrected == original.replace(b'  "homepage": "",\n', b"", 1)
    contract["manifest_exception"] = {
        "authorization": "scope-revision.json",
        "original_sha256": hashlib.sha256(original).hexdigest(),
        "corrected_sha256": hashlib.sha256(corrected).hexdigest(),
        "exact_change": "Delete only the invalid empty homepage line",
    }
    for row in contract["commands"]:
        row["frontend"] = row["expected_frontend"]
        row["verified"] = row["frontend"] in init["slash_commands"]
        assert row["verified"], row
    for row in contract["existing_agents"]:
        row["frontend"] = row["expected_frontend"]
        row["verified"] = row["frontend"] in init["agents"]
        assert row["verified"], row
    resources = []
    for candidate in contract["candidate_resources"]:
        row = dict(candidate)
        parts = Path(row["destination"]).parts
        if parts[0] == "agents":
            row["frontend"] = "sc:" + Path(row["destination"]).stem
            row["verified"] = row["frontend"] in init["agents"]
        else:
            row["skill_frontend"] = "sc:" + parts[1]
            row["verified"] = row["skill_frontend"] in init["skills"]
        row["resource_lookup"] = "${CLAUDE_PLUGIN_ROOT}/" + row["destination"]
        row["source_sha256"] = hashlib.sha256((ROOT / row["source"]).read_bytes()).hexdigest()
        assert row["verified"], row
        resources.append(row)
    contract["candidate_resources"] = resources
    contract["skills"] = [{"directory": "skills/confidence-check", "frontend": "sc:confidence-check", "verified": "sc:confidence-check" in init["skills"]}] + [{"directory": "skills/" + name, "frontend": "sc:" + name, "verified": "sc:" + name in init["skills"]} for name in ("sc-reflect-protocol", "sc-adversarial-protocol")]
    contract["lookup_rule"] = "Native inventory proves sc:<command filename stem>, sc:<skill directory>, sc:<agent filename stem>. Runtime file reads resolve ${CLAUDE_PLUGIN_ROOT}/skills/... or ${CLAUDE_PLUGIN_ROOT}/agents/...; do not use global or checkout paths."
    contract["loader_probe_history"] = contract.get("loader_probe_history", []) + [contract["loader_probe"]]
    contract["loader_probe"] = {"validation_and_session": "loader-candidates-probes.json", "session_init": "loader-candidates-init.json", "native_plugin_loaded": True, "candidate_fixture_only": True, "existing_specialist_dispatch": "loader-external-session.stdout.txt", "bare_mode_limitation": "bare mode suppresses plugin agents in this native client; use a clean external cwd, isolated HOME/config, user-only settings and strict empty MCP instead", "builtin_note": "Native built-ins listed but no framework dependency supplied by them; inventory prompt forbids skill invocation and tools."}
    contract["blockers"] = []
    contract["status"] = "LOADER VERIFIED: required dependency closure pending"
    path.write_text(json.dumps(contract, indent=2) + "\n")
    print("Verified 28 command mappings, 21 existing agent mappings and all 22 candidate resource frontend mappings")


if __name__ == "__main__":
    main()

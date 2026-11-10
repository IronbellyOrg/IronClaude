"""Approved compatibility inventory/backup only. This helper never installs a skill."""

import hashlib
import json
import os
import re
import stat
import sys
import tarfile
from pathlib import Path

import superclaude.cli.install_skill as installer

os.umask(0o077)
ROOT = Path("/home/coder/workspaces/worktrees/IronClaude/issue-441")
PKG = ROOT / ".dev/tasks/to-do/TASK-WF-diagnosticRefres-20261109-144413"
OUT = PKG / "artifacts"
SOURCE = ROOT / "src/superclaude/skills/sc-troubleshoot-protocol"
TARGET = Path("/home/coder/.claude/skills/sc-troubleshoot-protocol")
PROFILES = [
    ROOT / "src/superclaude/agents/troubleshoot-analyst.md",
    ROOT / ".claude/agents/troubleshoot-analyst.md",
    Path("/home/coder/.claude/agents/troubleshoot-analyst.md"),
]
SETTINGS = [
    ROOT / ".claude/settings.json",
    ROOT / ".claude/settings.local.json",
    Path("/home/coder/.claude/settings.json"),
    Path("/home/coder/.claude/settings.local.json"),
]
EXPECTED = {
    "Read",
    "Grep",
    "Glob",
    "mcp__litellm__augment_code-augment_code_search",
    "mcp__auggie__codebase-retrieval",
    "mcp__codegraph__codegraph_search",
    "mcp__codegraph__codegraph_node",
    "mcp__codegraph__codegraph_callers",
    "mcp__codegraph__codegraph_impact",
}
EXPECTED_DRIFT = ["SKILL.md", "refs/diagnosability-audit.md", "refs/doc-discovery.md"]
# Owner decision A (reply '1', 2026-11-10T00:02Z, relayed by the coordinator): exactly these
# 19 entries may differ in mode only, source 0700/0600 against installed 0755/0644 (the
# install tightens the installed copy). Any other mode difference, any loosening, or any
# value other than these pairs stops the run.
_DIRS = (".", "refs", "refs/probe-packs")
_FILES = (
    "refs/agent-assertions.md",
    "refs/calibrator-eval-cases.md",
    "refs/contract-enumeration.md",
    "refs/effective-input-proof.md",
    "refs/environment-deltas.md",
    "refs/escalation-rubric.md",
    "refs/hardening-output-contract.md",
    "refs/hypothesis-card-template.md",
    "refs/pipeline-hardening-closure.md",
    "refs/primitive-differential.md",
    "refs/probe-packs/read-parse.md",
    "refs/remediation-handoff.md",
    "refs/report-template.md",
    "refs/runtime-entrypoint-verification.md",
    "refs/triage-checklist.md",
    "refs/unmask-and-sweep.md",
)
AUTHORIZED_MODE_TIGHTENING = {
    **{k: {"source": 0o700, "installed": 0o755} for k in _DIRS},
    **{k: {"source": 0o600, "installed": 0o644} for k in _FILES},
}
OWNER_DECISION_A = {
    "decision": "A: mode-only exception for the 19 install-skill entries AUTHORIZED",
    "source": "owner reply '1' at 2026-11-10T00:02Z, relayed by the coordinator",
    "verbatim": (
        "(A) AUTHORIZED: the mode-only exception for the 19 install-skill entries "
        "(2 directories, 17 refs files; source 700/600 vs installed 755/644; the install "
        "makes installed copies stricter). It covers ONLY those 19 entries and ONLY mode "
        "differences. Any other drift, any content-hash difference, or any mode difference "
        "that loosens permissions = STOP and report."
    ),
    "count_note": (
        "The recorded entry set is 3 directories (., refs, refs/probe-packs) and 16 files; "
        "the total of 19 and the mode pairs match the wording."
    ),
    "entries": sorted(AUTHORIZED_MODE_TIGHTENING),
}
OWNER_DECISION_B = {
    "decision": "B: settings.json rebaseline stays approved with conditions",
    "source": "owner reply '1' at 2026-11-10T00:02Z, relayed by the coordinator",
    "provenance": (
        "owner ran /model in the coordinator session on 2026-11-09 ~19:38Z; the default "
        "model changed and was saved; setup-bmad is an unrelated tooling skill"
    ),
}


def hash_stream(stream):
    h = hashlib.sha256()
    for chunk in iter(lambda: stream.read(65536), b""):
        h.update(chunk)
    return h.hexdigest()


def file_state(path):
    if not os.path.lexists(path):
        return {"kind": "absent"}
    st = path.lstat()
    mode = stat.S_IMODE(st.st_mode)
    if stat.S_ISLNK(st.st_mode):
        return {"kind": "symlink", "mode": mode, "target": os.readlink(path)}
    if stat.S_ISDIR(st.st_mode):
        return {"kind": "dir", "mode": mode}
    if not stat.S_ISREG(st.st_mode):
        return {"kind": "special", "mode": mode}
    fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK)
    with os.fdopen(fd, "rb") as f:
        actual = os.fstat(f.fileno())
        assert stat.S_ISREG(actual.st_mode) and (actual.st_dev, actual.st_ino) == (
            st.st_dev,
            st.st_ino,
        ), path
        return {
            "kind": "file",
            "mode": mode,
            "size": actual.st_size,
            "sha256": hash_stream(f),
        }


def manifest(folder):
    return {
        ".": file_state(folder),
        **{
            str(p.relative_to(folder)): file_state(p) for p in sorted(folder.rglob("*"))
        },
    }


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True).encode()).hexdigest()


def roster(path):
    front = re.match(r"\A---\n(.*?)\n---", path.read_text(), re.S)
    assert front, path
    tools = re.search(r"^tools:\s*(.+)$", front[1], re.M)
    assert tools, path
    return set(x.strip() for x in tools[1].split(","))


def contract_roster(path):
    match = re.search(r"closed roster `([^`]+)`", path.read_text())
    assert match, path
    return set(x.strip() for x in match[1].split(","))


def current():
    assert os.environ.get("ANTHROPIC_DEFAULT_SONNET_MODEL") == "claude-gw-tier1b[1m]", (
        "Unverified helper mapping"
    )
    assert SOURCE.resolve() == SOURCE and TARGET.resolve() == TARGET and TARGET.is_dir()
    assert installer._get_skill_source("sc-troubleshoot-protocol").resolve() == SOURCE
    assert (
        Path(installer.__file__).resolve()
        == ROOT / "src/superclaude/cli/install_skill.py"
    )
    assert Path.home() == Path("/home/coder")
    source = manifest(SOURCE)
    installed = manifest(TARGET)
    assert all(v["kind"] in ("file", "dir") for v in source.values())
    assert all(v["kind"] in ("file", "dir") for v in installed.values())
    assert (
        roster(PROFILES[0])
        == roster(PROFILES[1])
        == contract_roster(SOURCE / "SKILL.md")
        == EXPECTED
    )
    profiles = {str(p): file_state(p) for p in PROFILES}
    settings = {str(p): file_state(p) for p in SETTINGS}
    other = {
        str(p.name): digest(manifest(p))
        if p.is_dir() and not p.is_symlink()
        else file_state(p)
        for p in sorted(TARGET.parent.iterdir())
        if p != TARGET
    }
    mirrors = {
        name: digest(manifest(ROOT / ".claude" / name))
        for name in ("skills", "agents", "commands", "hooks", "templates")
    }
    binding = {
        "module": str(Path(installer.__file__).resolve()),
        "module_state": file_state(Path(installer.__file__)),
        "source": str(SOURCE),
        "target": str(TARGET),
        "source_realpath": str(SOURCE.resolve()),
        "target_realpath": str(TARGET.resolve()),
        "model_alias": "sonnet",
        "model_mapping": os.environ["ANTHROPIC_DEFAULT_SONNET_MODEL"],
    }
    return {
        "source": source,
        "installed": installed,
        "profiles": profiles,
        "settings": settings,
        "other_installed_digest": digest(other),
        "other_installed_entries": len(other),
        "project_mirrors": mirrors,
        "binding": binding,
        "roster": sorted(EXPECTED),
    }


def verify_backup(before):
    backup = OUT / "installed-skill-before.tar.gz"
    assert stat.S_IMODE(backup.stat().st_mode) == 0o600
    with tarfile.open(backup, "r:gz") as archive:
        actual = {}
        for member in archive.getmembers():
            rel = str(Path(member.name).relative_to(TARGET.name))
            if member.isdir():
                actual[rel] = {"kind": "dir", "mode": member.mode}
            elif member.isfile():
                with archive.extractfile(member) as stream:
                    actual[rel] = {
                        "kind": "file",
                        "mode": member.mode,
                        "size": member.size,
                        "sha256": hash_stream(stream),
                    }
            else:
                raise AssertionError("Unexpected archive member type")
    assert actual == before["installed"], (
        "Archive does not preserve every byte/type/mode"
    )
    return {"path": "./artifacts/installed-skill-before.tar.gz", **file_state(backup)}


phase = sys.argv[1]
if phase == "before":
    state = current()
    keys = set(state["source"]) | set(state["installed"])
    assert set(state["source"]) == set(state["installed"]), (
        "Unexpected extra or missing entry"
    )
    assert all(
        state["source"][k]["kind"] == state["installed"][k]["kind"] for k in keys
    ), "Entry type drift"
    drift = sorted(
        k
        for k in keys
        if state["source"][k].get("sha256") != state["installed"][k].get("sha256")
    )
    mode_changes = {
        k: {
            "source": state["source"][k]["mode"],
            "installed": state["installed"][k]["mode"],
        }
        for k in sorted(keys)
        if state["source"][k]["mode"] != state["installed"][k]["mode"]
    }
    assert all((v["source"] & ~v["installed"]) == 0 for v in mode_changes.values()), (
        "Normal refresh would broaden filesystem permissions"
    )
    state["selected_mode_tightening"] = mode_changes
    # Plan Task 1: stop on any drift beyond the three stale files. The only mode difference
    # allowed is the exact owner-authorized set above (decision A), value for value.
    if drift != EXPECTED_DRIFT or mode_changes != AUTHORIZED_MODE_TIGHTENING:
        keys = set(state["source"]) | set(state["installed"])
        state["observed_drift"] = drift
        state["content_drift"] = sorted(
            k
            for k in keys
            if state["source"].get(k, {}).get("sha256")
            != state["installed"].get(k, {}).get("sha256")
        )
        state["mode_drift"] = sorted(
            k
            for k in keys
            if state["source"].get(k, {}).get("mode")
            != state["installed"].get(k, {}).get("mode")
        )
        (OUT / "blocked-before-state.json").write_text(
            json.dumps(state, indent=2) + "\n"
        )
        print(
            json.dumps(
                {
                    "phase": "blocked_before",
                    "content_drift": state["content_drift"],
                    "mode_drift_count": len(state["mode_drift"]),
                    "examples": {
                        k: {
                            "source": oct(state["source"][k]["mode"]),
                            "installed": oct(state["installed"][k]["mode"]),
                        }
                        for k in state["mode_drift"][:5]
                    },
                    "installer_run": False,
                    "backup_exists": (OUT / "installed-skill-before.tar.gz").exists(),
                }
            )
        )
        raise AssertionError(
            "Unexpected metadata drift; preserved state, no installation"
        )
    assert set(state["source"]) == set(state["installed"]), (
        "Unexpected extra or missing entry"
    )
    assert contract_roster(TARGET / "SKILL.md") == EXPECTED - {
        "mcp__litellm__augment_code-augment_code_search"
    }
    backup = OUT / "installed-skill-before.tar.gz"
    # A backup from the first run is never overwritten: a re-run must prove the existing
    # backup still matches the (unchanged) installed folder byte for byte, type and mode.
    state["backup_reused"] = backup.exists()
    if not backup.exists():
        with tarfile.open(backup, "w:gz") as archive:
            archive.add(TARGET, arcname=TARGET.name, recursive=True)
        os.chmod(backup, 0o600)
    state["backup"] = verify_backup(state)
    state["differing_files"] = drift
    old_before = OUT / "compatibility-before.json"
    if old_before.exists():
        prev = json.loads(old_before.read_text())
        if "rebaseline" in prev:
            state["rebaseline"] = prev["rebaseline"]
    state["owner_decision_A"] = OWNER_DECISION_A
    state["owner_decision_B"] = OWNER_DECISION_B
    (OUT / "compatibility-before.json").write_text(json.dumps(state, indent=2) + "\n")
    (OUT / "authorization-and-binding.json").write_text(
        json.dumps(
            {
                "owner_message": "msg_fbc81030bd4f",
                "owner_provenance": "2026-11-09T14:12UTC direct genuine owner message relayed by coordinator:441 pr469 authorized; checked compatibility only",
                "scope": "No permissions/profile/tool/gate broadening; normal one-skill installer; old failures/caps preserved; no merge/closure",
                "owner_decision_A": OWNER_DECISION_A,
                "owner_decision_B": OWNER_DECISION_B,
                "binding": state["binding"],
                "source_target_verified": True,
                "profile_roster": state["roster"],
                "backup": state["backup"],
            },
            indent=2,
        )
        + "\n"
    )
    print(
        json.dumps(
            {
                "phase": "before",
                "drift": drift,
                "backup_verified": True,
                "archive_mode": "0600",
                "file_entries": len(state["installed"]),
                "profiles_settings_unchanged": True,
            }
        )
    )
elif phase in ("guard", "after", "verify"):
    before = json.loads((OUT / "compatibility-before.json").read_text())
    state = current()
    assert verify_backup(before) == before["backup"]
    for key in (
        "source",
        "profiles",
        "settings",
        "other_installed_digest",
        "other_installed_entries",
        "project_mirrors",
        "binding",
        "roster",
    ):
        assert state[key] == before[key], key + " changed"
    if phase == "guard":
        assert state["installed"] == before["installed"], "Target changed since backup"
        print(
            json.dumps(
                {
                    "phase": "guard",
                    "all_prerequisites_unchanged": True,
                    "backup_reverified": True,
                }
            )
        )
    else:
        assert state["installed"] == state["source"], (
            "Installed package not exactly canonical"
        )
        changed = sorted(
            k
            for k in state["installed"]
            if state["installed"][k].get("sha256")
            != before["installed"][k].get("sha256")
        )
        assert changed == EXPECTED_DRIFT, changed
        assert contract_roster(TARGET / "SKILL.md") == EXPECTED
        state.update(
            {
                "changed_files": changed,
                "selected_mode_tightening": before["selected_mode_tightening"],
                "protected_invariants_unchanged": True,
                "exact_canonical_parity": True,
                "backup": before["backup"],
            }
        )
        if phase == "after":
            (OUT / "compatibility-after.json").write_text(
                json.dumps(state, indent=2) + "\n"
            )
        else:
            assert state == json.loads(
                (OUT / "compatibility-after.json").read_text()
            ), "Live state changed after recorded installation"
        print(
            json.dumps(
                {
                    "phase": phase,
                    "exact_canonical_parity": True,
                    "changed_files": changed,
                    "protected_invariants_unchanged": True,
                }
            )
        )
else:
    raise ValueError(phase)

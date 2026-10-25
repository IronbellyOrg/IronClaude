#!/usr/bin/env python3
"""Run real native root-command cases in an isolated actual-copy plugin fixture."""

import argparse
import hashlib
import json
import os
import shutil
import signal
import subprocess
import tempfile
import time
from pathlib import Path

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[5]
RUNTIME = OUT / "task4-runtime"


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def dump(path, value):
    path.write_text(json.dumps(value, indent=2) + "\n")


def prepare():
    if RUNTIME.exists():
        raise SystemExit("Runtime fixture already exists; retain it and use its recorded contents")
    RUNTIME.mkdir()
    for folder in (".claude-plugin", "commands", "agents", "skills"):
        shutil.copytree(ROOT / folder, RUNTIME / "plugin" / folder)
    binary = RUNTIME / "runtime-bin"
    binary.mkdir()
    uv = shutil.which("uv")
    if not uv:
        raise SystemExit("Existing uv unavailable; do not install it")
    (binary / "uv").symlink_to(Path(uv).resolve())
    project = RUNTIME / "fixtures/project"
    (project / "src").mkdir(parents=True)
    (project / "tests").mkdir()
    subprocess.run(["git", "init", "--quiet", str(project)], check=True)
    (project / "spec.md").write_text("""# Synthetic greeting contract

This fixture is synthetic audit input, not shipped product code.

## R-001 Greeting
The greet function MUST return the exact string Hello, Ada! for Ada.

## R-002 Empty input
The greet function MUST reject an empty name with ValueError.

## R-003 Evidence
Tests MUST exercise the ordinary greeting and empty-input rejection.
""")
    (project / "proposed.md").write_text("""# Proposed synthetic greeting plan

## T-101 R-001
Implement greet(name) returning the required greeting.

## T-102 R-002
Reject an empty name using ValueError.

## T-103 R-003
Add ordinary and empty-name test cases.
""")
    (project / "completed.md").write_text("""---
status: done
---
# Synthetic completed tasklist

- [x] T-101 implements R-001 ordinary greeting.
- [x] T-102 implements R-002 empty-name rejection.
- [x] T-103 implements R-003 both ordinary and empty-input tests.
""")
    (project / "src/greeting.py").write_text('def greet(name):\n    if not name:\n        raise ValueError("name required")\n    return f"Hello, {name}!"\n')
    (project / "tests/test_greeting.py").write_text('from src.greeting import greet\n\n\ndef test_ordinary():\n    assert greet("Ada") == "Hello, Ada!"\n\n\ndef test_empty():\n    try:\n        greet("")\n    except ValueError:\n        return\n    raise AssertionError("empty name accepted")\n')
    (project / "changes.patch").write_text('diff --git a/src/greeting.py b/src/greeting.py\nnew file mode 100644\n--- /dev/null\n+++ b/src/greeting.py\n@@ -0,0 +1,4 @@\n+def greet(name):\n+    if not name:\n+        raise ValueError("name required")\n+    return f"Hello, {name}!"\n')
    (project / "execution.log").write_text("Synthetic completed-work log, not an execution claim about product code.\nT-101 R-001: created src/greeting.py.\nT-102 R-002: empty names raise ValueError.\nT-103 R-003: created tests/test_greeting.py with ordinary and empty-name cases.\nNo test execution is claimed; inspect these files independently.\n")
    help_result = subprocess.run([shutil.which("claude"), "--help"], capture_output=True, text=True, check=True)
    (RUNTIME / "native-help.txt").write_text(help_result.stdout)
    required = ("--setting-sources", "--strict-mcp-config", "--mcp-config", "--plugin-dir", "--permission-mode", "acceptEdits", "--restricted", "--add-dir", "--allowed-tools", "--permission-prompts", "--forward-subagent-text", "--append-system-prompt", "--no-session-persistence")
    assert all(token in help_result.stdout for token in required)
    files = {str(path.relative_to(RUNTIME / "plugin")): sha(path) for path in (RUNTIME / "plugin").rglob("*") if path.is_file()}
    inputs = {str(path.relative_to(project)): sha(path) for path in project.rglob("*") if path.is_file() and ".git" not in path.relative_to(project).parts}
    dump(RUNTIME / "fixture-contents.json", {"actual_plugin_copy_sha256": files, "audit_input_sha256": inputs, "git_init_only_no_staging_or_commits": True, "runtime_bin_uv_target": str((binary / "uv").resolve())})
    print(RUNTIME)


def blocks(event):
    message = event.get("message")
    content = message.get("content") if isinstance(message, dict) else None
    return [block for block in content if isinstance(block, dict)] if isinstance(content, list) else []


def main():
    global RUNTIME
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--runtime", default="task4-runtime")
    parser.add_argument("--persist-session", action="store_true")
    parser.add_argument("--prepare", action="store_true")
    parser.add_argument("--case")
    parser.add_argument("--attempt", default="1")
    parser.add_argument("--timeout", type=int, default=1800)
    args = parser.parse_args()
    RUNTIME = OUT / args.runtime
    if RUNTIME.parent != OUT:
        parser.error("runtime must be an immediate evidence child")
    if args.prepare:
        prepare()
        return
    if not args.case:
        parser.error("--case required")
    project = RUNTIME / "fixtures/project"
    runs = RUNTIME / "runs"
    runs.mkdir(exist_ok=True)
    case = runs / f"{args.case}-attempt-{args.attempt}"
    case.mkdir(exist_ok=False)
    artifacts = case / "artifacts"
    home = case / "home"
    config = case / "config"
    home.mkdir()
    config.mkdir()
    (config / "settings.json").write_text("{}\n")
    cwd = Path(tempfile.mkdtemp(prefix="ironclaude-reflect-runtime-"))
    env = {"PATH": str(RUNTIME / "runtime-bin") + ":/usr/bin:/bin", "HOME": str(home),
           "CLAUDE_CONFIG_DIR": str(config), "XDG_CONFIG_HOME": str(home / ".config")}
    provider_keys = [key for key in os.environ if key.startswith("ANTHROPIC_")]
    env.update({key: os.environ[key] for key in provider_keys})
    absence = subprocess.run(["/bin/sh", "-c", "command -v superclaude; command -v uv; command -v git"], cwd=cwd, env=env, capture_output=True, text=True)
    assert shutil.which("superclaude", path=env["PATH"]) is None, "Package executable unexpectedly exposed"
    common = ["--spec", str(project / "spec.md"), "--tasklist", str(project / "completed.md"), "--scope", str(project / "src")]
    cases = {
        "pre-smoke": ["--mode", "pre", "--spec", str(project / "spec.md"), "--tasklist", str(project / "proposed.md"), "--tier", "1", "--no-mcp"],
        "pre-default": ["--mode", "pre", "--spec", str(project / "spec.md"), "--tasklist", str(project / "proposed.md")],
        "post-default": ["--mode", "post", "--diff", str(project / "changes.patch"), *common],
        "post-tier1": ["--mode", "post", "--diff", str(project / "changes.patch"), *common, "--tier", "1"],
        "post-tier2": ["--mode", "post", "--diff", str(project / "changes.patch"), *common, "--tier", "2", "--reviewers", "2"],
        "legacy-pre": ["--type", "task", "--analyze", "--spec", str(project / "spec.md"), "--tasklist", str(project / "proposed.md"), "--tier", "1"],
        "legacy-post": ["--type", "task", "--validate", "--task-log", str(project / "execution.log"), *common, "--tier", "1"],
        "post-log-only": ["--mode", "post", "--task-log", str(project / "execution.log"), "--scope", str(project / "src"), "--tier", "1", "--no-mcp"],
        "missing-pre": ["--mode", "pre", "--tasklist", str(project / "proposed.md")],
        "missing-post": ["--mode", "post", "--spec", str(project / "spec.md")],
        "unsafe-output": ["--mode", "pre", "--spec", str(project / "spec.md"), "--output", str(RUNTIME / "plugin/skills/forbidden-runtime-output")],
        "remediation-unavailable": ["--mode", "post", "--task-log", str(project / "execution.log"), "--scope", str(project / "src"), "--tier", "1", "--remediate", "--no-mcp"],
        "readiness-unavailable": ["detection-contract", "readiness", "--repo", "synthetic/example", "--pr", "1"],
        "invalid-commit-range": ["--mode", "post", "--commit-range", "NOT_A_REAL_REF..ALSO_NOT_REAL", "--scope", str(project / "src")],
    }
    flags = cases[args.case] + ["--no-promote"]
    if "--output" not in flags:
        flags.extend(["--output", str(artifacts)])
    prompt = "/sc:sc-reflect " + " ".join(flags)
    context = (f"This is an authorized isolated plugin-only audit. The synthetic audited repository is {project}, not your empty launch cwd. "
               f"Use that explicit repository for read-only Git operations and scope resolution. It has git init only, no commits/index entries. "
               f"All supplied files are safe synthetic fixtures. Do NOT stage, commit, edit audit inputs, edit plugin distribution resources, create a CLAUDE.md, install dependencies or invoke the superclaude package. "
               f"Write only under the requested safe output {artifacts}; when the actual --output is forbidden, refuse without creating it. "
               "Follow the actual loaded root command and bundled protocol, including genuine independent calibration/citation gates; no invented agent results or convergence. "
               "If native tools are named Agent rather than Task, use Agent with the exact plugin-qualified registered subagent type. "
               "Use real opus/sonnet/haiku slot aliases already configured by this environment and their actual diversity; do not invent an external model. "
               "All --no-promote requests forbid moves/archive/promotion mutations. Return the actual report/contract paths and honest status. "
               "You may serialize return-contract.yaml as JSON, which is valid YAML, for machine readability; preserve all protocol fields and semantics. "
               f"Every delegated Agent brief must explicitly bind audit_repo_root={project}, allowed evidence roots to that project or the actual frozen snapshot, allowed output to {artifacts}, and plugin resources to {RUNTIME / 'plugin'}. Propagate this to all debate/fault-finder/scoring/merge workers; never read the ancestor checkout's pyproject.toml, CLAUDE.md, package or project mirrors. Exact permitted role cwd paths are launch_cwd={cwd} and audit_repo_root={project}; repeat this policy and both exact paths in EVERY secondary handoff, including advocates/scorers/merge/final validator. This declared test profile is stricter: scoped native permissions deny shell cd/pushd/popd, freezing cwd at the exact launch directory. Use absolute file paths and git -C; do not bypass denials or enter outputs/snapshots/resources as cwd. "
               "Use the available uv for every Python subprocess. Do not invoke global or unrelated built-in skills as substitutes for missing framework resources. Never print provider credentials or credential environment values.")
    command = [shutil.which("claude"), "--setting-sources", "user", "--strict-mcp-config", "--mcp-config", '{"mcpServers":{}}',
               "--plugin-dir", str(RUNTIME / "plugin"), "--print", "--output-format", "stream-json", "--verbose",
               "--forward-subagent-text", "--model", "opus", "--restricted", "--add-dir", str(project), str(case), str(RUNTIME / "plugin"),
               "--permission-mode", "acceptEdits", "--permission-prompts", "none",
               "--allowed-tools", "Read,Grep,Glob,Bash,Write,Edit,Agent,Skill", "--tools", "Read,Grep,Glob,Bash,Write,Edit,Agent,Skill",
               "--disallowed-tools", "Bash(cd *)", "Bash(cd)", "Bash(pushd *)", "Bash(pushd)", "Bash(popd *)", "Bash(popd)",
               "--append-system-prompt", context, prompt]
    if not args.persist_session:
        command.insert(-1, "--no-session-persistence")
    baseline = json.loads((RUNTIME / "fixture-contents.json").read_text())
    record = {"case": args.case, "attempt": args.attempt, "state": "running", "command": command, "cwd": str(cwd),
              "environment": {key: value for key, value in env.items() if not key.startswith("ANTHROPIC_")},
              "provider_variable_names_only": provider_keys, "framework_executable_absent": True,
              "runtime_tools_probe": absence.stdout, "timeout_seconds": args.timeout,
              "started_monotonic": time.monotonic()}
    record["plugin_sha256_at_launch"] = {path: sha(RUNTIME / "plugin" / path) for path in baseline["actual_plugin_copy_sha256"]}
    record["fixture_manifest_sha256"] = sha(RUNTIME / "fixture-contents.json")
    if record["plugin_sha256_at_launch"] != baseline["actual_plugin_copy_sha256"]:
        raise SystemExit("Plugin drift before launch: no native audit started")
    dump(case / "execution.json", record)
    with (case / "stdout.jsonl").open("w") as stdout, (case / "stderr.txt").open("w") as stderr:
        process = subprocess.Popen(command, cwd=cwd, env=env, stdout=stdout, stderr=stderr, start_new_session=True)
        try:
            rc = process.wait(timeout=args.timeout)
            record.update({"state": "exited", "returncode": rc})
        except subprocess.TimeoutExpired:
            os.killpg(process.pid, signal.SIGTERM)
            try:
                process.wait(timeout=15)
            except subprocess.TimeoutExpired:
                os.killpg(process.pid, signal.SIGKILL)
                process.wait()
            record.update({"state": "timeout", "returncode": process.returncode})
    record["duration_seconds"] = time.monotonic() - record["started_monotonic"]
    record["changed_plugin_files"] = [path for path, digest in baseline["actual_plugin_copy_sha256"].items() if not (RUNTIME / "plugin" / path).is_file() or sha(RUNTIME / "plugin" / path) != digest]
    record["added_plugin_files"] = sorted({str(path.relative_to(RUNTIME / "plugin")) for path in (RUNTIME / "plugin").rglob("*") if path.is_file()} - set(baseline["actual_plugin_copy_sha256"]))
    record["fixture_staged_files"] = subprocess.check_output(["git", "ls-files"], cwd=project, text=True).splitlines()
    fixture_head = subprocess.run(["git", "rev-parse", "--verify", "HEAD"], cwd=project, capture_output=True, text=True)
    record["fixture_head_created"] = fixture_head.returncode == 0
    record["changed_audit_inputs"] = [path for path, digest in baseline["audit_input_sha256"].items() if not (project / path).is_file() or sha(project / path) != digest]
    events = []
    for line in (case / "stdout.jsonl").read_text().splitlines():
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue
        if event.get("type") == "system" and event.get("subtype") == "init":
            dump(case / "native-init.json", event)
        if event.get("type") == "result":
            record["native_result"] = event
        if event.get("type") == "assistant":
            for block in blocks(event):
                if block.get("type") == "tool_use":
                    events.append({"parent_tool_use_id": event.get("parent_tool_use_id"), "tool": block.get("name"), "input": block.get("input")})
    dump(case / "role-and-tool-calls.json", events)
    record["artifact_files"] = [str(path.relative_to(case)) for path in case.rglob("*") if path.is_file() and not any(part in ("home", "config") for part in path.relative_to(case).parts)]
    dump(case / "execution.json", record)
    print(json.dumps({key: record.get(key) for key in ("case", "state", "returncode", "duration_seconds", "changed_plugin_files", "changed_audit_inputs")}, indent=2))
    print(case)
    raise SystemExit(record["state"] != "exited" or record["returncode"] != 0 or bool(record["changed_plugin_files"]) or bool(record["changed_audit_inputs"]) or bool(record["added_plugin_files"]) or bool(record["fixture_staged_files"]) or record["fixture_head_created"])


if __name__ == "__main__":
    main()

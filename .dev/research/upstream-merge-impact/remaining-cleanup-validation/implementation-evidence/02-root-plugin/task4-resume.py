#!/usr/bin/env python3
"""Genuinely resume a persisted unfinished native audit, retaining original execution/logs."""
import argparse
import hashlib
import json
import os
import signal
import subprocess
import time
from pathlib import Path

OUT = Path(__file__).resolve().parent


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--runtime", required=True)
    parser.add_argument("--case", required=True)
    parser.add_argument("--label", default="1")
    parser.add_argument("--timeout", type=int, default=6000)
    args = parser.parse_args()
    runtime = OUT / args.runtime
    case = runtime / "runs" / args.case
    original = json.loads((case / "execution.json").read_text())
    baseline = json.loads((runtime / "fixture-contents.json").read_text())
    for relative, digest in baseline["actual_plugin_copy_sha256"].items():
        if hashlib.sha256((runtime / "plugin" / relative).read_bytes()).hexdigest() != digest:
            raise SystemExit("Plugin drift: cannot resume as same-body proof")
    session = original["native_result"]["session_id"]
    env = dict(original["environment"])
    env.update({key: os.environ[key] for key in original["provider_variable_names_only"] if key in os.environ})
    command = original["command"][:-1]
    command.extend(["--resume", session,
                    "Continue the SAME unfinished authorized audit from its actual retained state. The prior print turn ended while a background debate worker was still running, so it was killed before the merge and final evidence gate. Do NOT claim completion from that turn. Follow the actual loaded root command/protocol to finish this same requested audit, preserving every prior artifact, actual results and failed-attempt evidence. Resume or retry the incomplete pipeline stage, then real merge-executor and NEW final evidence-validator on the actual merged draft are still required. Do not invent agent results. Wait for every required native Agent return before ending this resumed turn; use foreground calls or wait for the actual background completion rather than ending while a required worker is in flight. Keep the existing exact launch cwd and audit root, native scoped directory-change denials, read-only reviewers, absolute paths, no-promote and missing-resource boundaries. Do not rerun against old/cohort/global resources or edit inputs/plugin files. This is continuation of the existing root command, not manual replacement of its role pipeline. Return only after actual report and contract exist or a truthful terminal blocker is recorded."])
    path = case / f"resume-{args.label}-execution.json"
    record = {"state": "running", "session_id": session, "command": command, "cwd": original["cwd"],
              "environment": original["environment"], "provider_variable_names_only": original["provider_variable_names_only"], "timeout_seconds": args.timeout,
              "plugin_sha256_at_launch": baseline["actual_plugin_copy_sha256"]}
    with path.open("x") as handle:
        json.dump(record, handle, indent=2)
        handle.write("\n")
    started = time.monotonic()
    with (case / f"stdout-resume-{args.label}.jsonl").open("x") as stdout, (case / f"stderr-resume-{args.label}.txt").open("x") as stderr:
        process = subprocess.Popen(command, cwd=original["cwd"], env=env, stdout=stdout, stderr=stderr, start_new_session=True)
        try:
            code = process.wait(timeout=args.timeout)
            record.update({"state": "exited", "returncode": code})
        except subprocess.TimeoutExpired:
            os.killpg(process.pid, signal.SIGTERM)
            try:
                process.wait(timeout=15)
            except subprocess.TimeoutExpired:
                os.killpg(process.pid, signal.SIGKILL)
                process.wait()
            record.update({"state": "timeout", "returncode": process.returncode})
    record["duration_seconds"] = time.monotonic() - started
    record["changed_plugin_files"] = [relative for relative, digest in baseline["actual_plugin_copy_sha256"].items() if hashlib.sha256((runtime / "plugin" / relative).read_bytes()).hexdigest() != digest]
    record["changed_audit_inputs"] = [relative for relative, digest in baseline["audit_input_sha256"].items() if hashlib.sha256((runtime / "fixtures/project" / relative).read_bytes()).hexdigest() != digest]
    for line in (case / f"stdout-resume-{args.label}.jsonl").read_text().splitlines():
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue
        if event.get("type") == "result":
            record["native_result"] = event
    path.write_text(json.dumps(record, indent=2) + "\n")
    print(json.dumps({key: record.get(key) for key in ("state", "returncode", "duration_seconds", "changed_plugin_files", "changed_audit_inputs")}, indent=2))
    print(path)
    raise SystemExit(record["state"] != "exited" or record["returncode"] != 0 or bool(record["changed_plugin_files"]) or bool(record["changed_audit_inputs"]))


if __name__ == "__main__":
    main()

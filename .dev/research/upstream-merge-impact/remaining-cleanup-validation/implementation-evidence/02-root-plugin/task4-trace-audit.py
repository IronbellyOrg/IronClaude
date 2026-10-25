#!/usr/bin/env python3
"""Retain every successful shell command and flag literal foreign-checkout reads/context."""
import argparse
import json
import re
import subprocess
from pathlib import Path

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[5]


def blocks(event):
    message = event.get("message")
    content = message.get("content") if isinstance(message, dict) else None
    return [block for block in content if isinstance(block, dict)] if isinstance(content, list) else []


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--runtime", default="task4-runtime-bounded")
    args = parser.parse_args()
    runtime = OUT / args.runtime
    results = []
    for case in sorted((runtime / "runs").iterdir()):
        execution = json.loads((case / "execution.json").read_text())
        events = []
        for trace_path in [case / "stdout.jsonl", *sorted(case.glob("stdout-resume-*.jsonl"))]:
            for line in trace_path.read_text().splitlines():
                try:
                    events.append(json.loads(line))
                except json.JSONDecodeError:
                    continue
        returns = {block["tool_use_id"]: block for event in events for block in blocks(event) if block.get("type") == "tool_result"}
        allowed = (runtime / "fixtures/project", runtime / "plugin", case, Path(execution["cwd"]))
        shells = []
        foreign_files = []
        for index, event in enumerate(events):
            for block in blocks(event):
                if block.get("type") != "tool_use" or block.get("id") not in returns or returns[block["id"]].get("is_error"):
                    continue
                arguments = block.get("input", {})
                if block.get("name") in ("Read", "Grep", "Glob"):
                    value = arguments.get("file_path", arguments.get("path"))
                    if value and Path(value).is_absolute() and not any(Path(value).is_relative_to(root) for root in allowed):
                        foreign_files.append({"event": index, "tool": block["name"], "path": value, "parent": event.get("parent_tool_use_id")})
                if block.get("name") == "Bash":
                    command = arguments.get("command", "")
                    paths = re.findall(re.escape(str(ROOT)) + r"[^\s\"'`;|&<>(){}]*", command)
                    suspicious = sorted({value for value in paths if not any(Path(value).is_relative_to(root) for root in allowed)})
                    shells.append({"event": index, "parent": event.get("parent_tool_use_id"), "description": arguments.get("description"), "command": command, "literal_foreign_checkout_references": suspicious})
        cwd_records = []
        context_attachments = []
        for transcript in (case / "config").rglob("*.jsonl"):
            cwds = set()
            for line in transcript.read_text().splitlines():
                try:
                    record = json.loads(line)
                except json.JSONDecodeError:
                    continue
                if record.get("cwd"):
                    cwds.add(record["cwd"])
                if record.get("type") == "attachment":
                    attachment = record.get("attachment", {})
                    context_attachments.append({"transcript": str(transcript), "type": attachment.get("type"), "path": attachment.get("path", attachment.get("filePath"))})
            for cwd in sorted(cwds):
                git = subprocess.run(["git", "-C", cwd, "rev-parse", "--show-toplevel"], capture_output=True, text=True)
                cwd_records.append({"transcript": str(transcript), "cwd": cwd, "git_root": git.stdout.strip() if git.returncode == 0 else None})
        results.append({"case": case.name, "state": execution["state"], "foreign_successful_file_tools": foreign_files,
                        "successful_shells": shells, "persisted_cwd_records": cwd_records, "context_attachments": context_attachments})
    record = {"runtime": str(runtime), "cases": results, "scope": "Actual successful file/shell tool traces plus persisted cwd/context attachments; shell commands retained for manual semantic inspection, not a claim of OS sandboxing"}
    target = OUT / f"{args.runtime}-trace-audit.json"
    target.write_text(json.dumps(record, indent=2) + "\n")
    print(json.dumps({"cases": len(results), "successful_shell_commands": sum(len(row["successful_shells"]) for row in results),
                      "foreign_file_calls": sum(len(row["foreign_successful_file_tools"]) for row in results),
                      "shells_with_foreign_checkout_literals": [{"case": row["case"], "event": shell["event"], "paths": shell["literal_foreign_checkout_references"]} for row in results for shell in row["successful_shells"] if shell["literal_foreign_checkout_references"]],
                      "output": str(target)}, indent=2))


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Stand-in `gh` for the controlled create runs of issue 834.

Never runs a real `gh`, never opens a network connection and imports nothing
that could (no subprocess, socket, urllib or http). Every call is appended as
one JSON line to the file named by FAKE_GH_LOG; created issues and comments are
kept in the state file FAKE_GH_STATE; the body of every issue create and
comment is copied to FAKE_GH_DIR.

Known read shapes answer with canned, clearly synthetic output. Writes are
logged and answered with success. Any other call exits 98.
"""

from __future__ import annotations

import json
import os
import sys
import time

REPO = os.environ.get("FAKE_GH_REPO", "IronbellyOrg/IronClaude")
OWNER = REPO.split("/")[0]
FIRST_FAKE_NUMBER = 990001  # no real issue of the fork has a number this high
STARTUP_REPO = "anthropics/claude-code"
SIMPLE, MEDIUM, COMPLEX = "Simple", "Medium", "Complex"
FIELD_ID = 7001
OPTION_IDS = {SIMPLE: 7101, MEDIUM: 7102, COMPLEX: 7103}


def _now() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def _log_path() -> str:
    path = os.environ.get("FAKE_GH_LOG")
    if not path:
        sys.stderr.write("fake gh: FAKE_GH_LOG is not set\n")
        sys.exit(99)
    return path


def _state() -> dict:
    path = os.environ.get("FAKE_GH_STATE", "")
    if path and os.path.exists(path):
        with open(path, encoding="utf-8") as handle:
            return json.load(handle)
    return {"next": FIRST_FAKE_NUMBER, "issues": {}, "comments": 0}


def _save(state: dict) -> None:
    path = os.environ.get("FAKE_GH_STATE", "")
    if path:
        with open(path, "w", encoding="utf-8") as handle:
            json.dump(state, handle)


def _opt(args: list[str], *names: str) -> str | None:
    for index, arg in enumerate(args):
        if arg in names and index + 1 < len(args):
            return args[index + 1]
        for name in names:
            if arg.startswith(name + "="):
                return arg.split("=", 1)[1]
    return None


def _copy_body(kind: str, number: int, path: str | None) -> str:
    """Copy a posted body file next to the log and return the copy's path."""
    out_dir = os.environ.get("FAKE_GH_DIR", "")
    if not (out_dir and path and os.path.isfile(path)):
        return ""
    os.makedirs(out_dir, exist_ok=True)
    copy = os.path.join(out_dir, f"posted-{kind}-{number}-{int(time.time() * 1000)}.md")
    with open(path, encoding="utf-8", errors="replace") as src, open(copy, "w", encoding="utf-8") as dst:
        dst.write(src.read())
    return copy


def _record(argv: list[str], kind: str, **extra: object) -> None:
    line = {"t": _now(), "argv": argv, "kind": kind, **extra}
    with open(_log_path(), "a", encoding="utf-8") as handle:
        handle.write(json.dumps(line) + "\n")


def _fail_unknown(argv: list[str]) -> int:
    _record(argv, "unknown")
    sys.stderr.write("fake gh: unknown call, refused: " + " ".join(argv) + "\n")
    return 98


def _api_path(args: list[str]) -> str:
    skip_next = False
    for arg in args[1:]:
        if skip_next:
            skip_next = False
            continue
        if arg in ("-X", "--method", "--input", "-F", "-f", "-H", "--jq", "-q", "--field", "--raw-field"):
            skip_next = True
            continue
        if arg.startswith("-"):
            continue
        return arg
    return ""


def main(argv: list[str]) -> int:
    args = argv
    if not args:
        return _fail_unknown(args)
    group = args[0]
    sub = args[1] if len(args) > 1 else ""
    repo = _opt(args, "--repo", "-R")

    # --- reads that Claude Code itself makes when a session starts
    if group == "auth" and sub == "token":
        _record(args, "start-up-read")
        sys.stderr.write("fake gh: no oauth token (synthetic)\n")
        return 1
    if group == "issue" and sub == "list" and repo == STARTUP_REPO:
        _record(args, "start-up-read")
        print("[]")
        return 0

    # --- reads that the create protocol makes
    if group == "auth" and sub == "status":
        _record(args, "protocol-read")
        print(f"github.com\n  Logged in to github.com account fake-user (synthetic, {REPO})")
        return 0
    if group == "label" and sub == "list" and repo == REPO:
        _record(args, "protocol-read")
        print(json.dumps([{"name": "enhancement"}, {"name": "bug"}]))
        return 0
    if group == "issue" and sub == "list" and repo == REPO:
        _record(args, "protocol-read")
        print("[]")
        return 0
    if group == "api":
        path = _api_path(args)
        method = (_opt(args, "-X", "--method") or "GET").upper()
        if method != "GET":
            body_file = _opt(args, "--input")
            copy = _copy_body("api-input", 0, body_file)
            state = _state()
            number = path.split("/issues/")[1].split("/")[0] if "/issues/" in path else ""
            if path.endswith("/issue-field-values") and number in state["issues"]:
                payload = {}
                if body_file and os.path.isfile(body_file):
                    with open(body_file, encoding="utf-8") as handle:
                        payload = json.load(handle)
                state["issues"][number]["fields"] = payload.get("issue_field_values", [])
                _save(state)
            _record(args, "write", method=method, path=path, body_copy=copy)
            print("{}")
            return 0
        if path == "user":
            _record(args, "protocol-read")
            print(json.dumps({"login": "fake-user"}))
            return 0
        if path == f"repos/{REPO}/issue-types":
            _record(args, "protocol-read")
            types = [{"id": 1, "name": "Task"}, {"id": 2, "name": "Bug"}, {"id": 3, "name": "Feature"}, {"id": 4, "name": "Test"}]
            print(json.dumps(types))
            return 0
        if path == f"orgs/{OWNER}/issue-fields":
            _record(args, "protocol-read")
            options = [{"id": OPTION_IDS[n], "name": n} for n in (SIMPLE, MEDIUM, COMPLEX)]
            print(json.dumps([{"id": FIELD_ID, "name": "Complexity", "data_type": "single_select", "options": options}]))
            return 0
        if path.startswith(f"repos/{REPO}/issues/") and path.endswith("/issue-field-values"):
            _record(args, "protocol-read")
            number = path.split("/issues/")[1].split("/")[0]
            rows = []
            for value in _state()["issues"].get(number, {}).get("fields", []):
                name = value.get("value")
                rows.append(
                    {
                        "issue_field_id": value.get("field_id"),
                        "value": OPTION_IDS.get(name),
                        "single_select_option": {"id": OPTION_IDS.get(name), "name": name},
                    }
                )
            print(json.dumps(rows))
            return 0
        return _fail_unknown(args)

    # --- writes: logged, answered with success, never forwarded
    if group == "issue" and sub == "create" and repo == REPO:
        state = _state()
        number = state["next"]
        state["next"] = number + 1
        body_file = _opt(args, "--body-file", "-F")
        copy = _copy_body("issue", number, body_file)
        state["issues"][str(number)] = {
            "title": _opt(args, "--title", "-t") or "",
            "labels": [a for i, a in enumerate(args) if i and args[i - 1] in ("--label", "-l")],
            "type": _opt(args, "--type") or "",
            "fields": [],
        }
        _save(state)
        _record(
            args,
            "write",
            op="issue create",
            number=number,
            title=state["issues"][str(number)]["title"],
            labels=state["issues"][str(number)]["labels"],
            type=state["issues"][str(number)]["type"],
            body_copy=copy,
        )
        print(f"https://github.com/{REPO}/issues/{number}")
        return 0
    if group == "issue" and sub == "comment" and repo == REPO:
        state = _state()
        state["comments"] = state.get("comments", 0) + 1
        _save(state)
        number = args[2] if len(args) > 2 else "0"
        copy = _copy_body("comment", number, _opt(args, "--body-file", "-F"))
        _record(args, "write", op="issue comment", number=number, body_copy=copy)
        print(f"https://github.com/{REPO}/issues/{number}#issuecomment-{state['comments']}")
        return 0
    if group == "issue" and sub == "edit" and repo == REPO:
        _record(args, "write", op="issue edit", number=args[2] if len(args) > 2 else "")
        return 0
    if group == "issue" and sub == "view" and repo == REPO and len(args) > 2:
        _record(args, "protocol-read")
        issue = _state()["issues"].get(args[2], {})
        if _opt(args, "--jq") == ".issueType.name":
            print(issue.get("type", ""))
        else:
            print(json.dumps({"issueType": {"name": issue.get("type", "")}}))
        return 0
    return _fail_unknown(args)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

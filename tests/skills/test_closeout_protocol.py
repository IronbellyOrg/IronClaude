"""Tests for the sc-closeout-protocol skill: the two scripts and the files they read.

This module runs the real ``scripts/branch-landed.sh`` and ``scripts/settle.sh`` in a
scratch git repository inside a pytest temporary directory. A local bare repository is
``origin``; a fake ``gh``, a fake ``orca`` and a fake ``superclaude`` come first on
``PATH`` and serve canned JSON, and a thin ``git`` wrapper records every call and
forwards it to the real ``git``. ``GIT_CONFIG_GLOBAL=/dev/null``,
``GIT_CONFIG_NOSYSTEM=1`` and a fixed author and committer are set for every git call;
``HOME`` points into the temporary directory. Nothing here touches the network, a real
GitHub repository, a real Orca Run or the operator's ``~/.claude``.

The fixtures live in this file only (the build plan allows two test files: this one and
``tests/commands/test_closeout_command.py``).
"""

from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
SKILL_DIR = REPO_ROOT / "src" / "superclaude" / "skills" / "sc-closeout-protocol"
SCRIPTS_DIR = SKILL_DIR / "scripts"
BRANCH_LANDED = SCRIPTS_DIR / "branch-landed.sh"
SETTLE = SCRIPTS_DIR / "settle.sh"
DENY_NAMES = SCRIPTS_DIR / "deny-names.txt"
TEMPLATES_DIR = SKILL_DIR / "templates"
REFS_DIR = SKILL_DIR / "refs"

GIT = shutil.which("git")
BASH = shutil.which("bash")
JQ = shutil.which("jq")

pytestmark = pytest.mark.skipif(
    GIT is None or BASH is None or JQ is None,
    reason="git, bash and jq are all needed to run the closeout scripts",
)

REPO_SLUG = "acme/widgets"
FAKE_ORIGIN_URL = f"git@github.com:{REPO_SLUG}.git"
DONE_MARKER = "<!-- sc:closeout pr={pr} -->"
NOT_DONE_MARKER = "<!-- sc:closeout pr={pr} verdict=not_done -->"
EM_DASH = chr(0x2014)
EN_DASH = chr(0x2013)


# ---------------------------------------------------------------------------
# The fakes: gh, git wrapper, orca, superclaude
# ---------------------------------------------------------------------------

FAKE_GH = r"""
import json
import os
import subprocess
import sys
from datetime import datetime, timedelta

STATE = os.environ["FAKE_STATE"]
CALLS = os.environ["FAKE_CALLS"]
argv = sys.argv[1:]

with open(CALLS, "a", encoding="utf-8") as fh:
    fh.write(json.dumps(["gh"] + argv) + "\n")

with open(STATE, encoding="utf-8") as fh:
    state = json.load(fh)

PR_FIELDS = {
    "number", "state", "mergedAt", "mergedBy", "mergeCommit", "baseRefName",
    "headRefName", "headRefOid", "commits", "url", "body", "title", "files",
    "changedFiles", "closingIssuesReferences",
}
ISSUE_FIELDS = {"state", "stateReason", "comments", "title", "body"}


def save():
    with open(STATE, "w", encoding="utf-8") as out:
        json.dump(state, out)


def stamp():
    state["clock"] = state.get("clock", 0) + 1
    base = datetime(2026, 11, 19, 10, 0, 0)
    return (base + timedelta(seconds=state["clock"])).strftime("%Y-%m-%dT%H:%M:%SZ")


def flag(name, default=None):
    if name in argv:
        i = argv.index(name)
        if i + 1 < len(argv):
            return argv[i + 1]
    return default


def pick(obj, allowed):
    spec = flag("--json")
    if spec is None:
        return obj
    names = spec.split(",")
    for name in names:
        if name not in allowed:
            return None
    return {name: obj.get(name) for name in names}


def emit(obj):
    return 0, json.dumps(obj) + "\n", ""


def fail(msg, code=1):
    return code, "", msg + "\n"


def jq_apply(data, expr):
    res = subprocess.run(
        ["jq", "-r", expr],
        input=json.dumps(data),
        capture_output=True,
        text=True,
    )
    return res.returncode, res.stdout, res.stderr


def apply_effect(effect):
    if not effect:
        return
    if "close" in effect:
        issue = state["issues"][effect["close"]]
        issue["state"] = "CLOSED"
        issue["stateReason"] = "COMPLETED"
        issue.setdefault("timeline", []).append(
            {"event": "closed", "created_at": stamp()}
        )
    if "reopen" in effect:
        issue = state["issues"][effect["reopen"]]
        issue["state"] = "OPEN"
        issue["stateReason"] = ""
        issue.setdefault("timeline", []).append(
            {"event": "reopened", "created_at": stamp()}
        )
    if "comment" in effect:
        spec = effect["comment"]
        state["issues"][spec["issue"]]["comments"].append(
            {
                "body": spec["body"],
                "author": {"login": spec["login"]},
                "authorAssociation": spec.get("assoc", "MEMBER"),
                "createdAt": stamp(),
            }
        )


def repo_ok():
    value = flag("--repo")
    return value == state["repo"]


def handle():
    joined = " ".join(argv)
    for rule in state.get("rules", []):
        if rule["match"] in joined and rule.get("when", "before") == "before":
            rule["hits"] = rule.get("hits", 0) + 1
            nth = rule.get("nth")
            if nth is None or rule["hits"] == nth:
                apply_effect(rule.get("effect"))
                if "exit" in rule or "stdout" in rule:
                    return rule.get("exit", 0), rule.get("stdout", ""), rule.get(
                        "stderr", ""
                    )
    cmd = argv[:2]
    if cmd[0] in ("pr", "issue") and not repo_ok():
        return fail("fake gh: wrong or missing --repo")
    if cmd == ["pr", "view"]:
        number = argv[2]
        pr = state["prs"].get(number)
        if pr is None:
            return fail(
                f"GraphQL: Could not resolve to a PullRequest with the number of "
                f"{number}. (repository.pullRequest)"
            )
        picked = pick(pr, PR_FIELDS)
        if picked is None:
            return fail("Unknown JSON field")
        return emit(picked)
    if cmd == ["pr", "list"]:
        key = "open_search" if flag("--state") == "open" else "pr_search"
        rows = list(state.get(key, []))
        limit = int(flag("--limit", "30"))
        return emit(rows[:limit])
    if cmd == ["issue", "view"]:
        issue = state["issues"].get(argv[2])
        if issue is None:
            return fail("GraphQL: Could not resolve to an Issue")
        picked = pick(issue, ISSUE_FIELDS)
        if picked is None:
            return fail("Unknown JSON field")
        return emit(picked)
    if cmd == ["issue", "comment"]:
        issue = state["issues"].get(argv[2])
        if issue is None or state.get("refuse_comment"):
            return fail("could not add comment")
        if not state.get("comment_not_stored"):
            runner = state.get("runner", {"login": "runner", "assoc": "MEMBER"})
            issue["comments"].append(
                {
                    "body": flag("--body"),
                    "author": {"login": runner["login"]},
                    "authorAssociation": runner["assoc"],
                    "createdAt": stamp(),
                }
            )
        return 0, f"https://github.com/{state['repo']}/issues/{argv[2]}#c\n", ""
    if cmd == ["issue", "close"]:
        issue = state["issues"].get(argv[2])
        if issue is None or state.get("close_fails"):
            return fail("could not close issue")
        if not state.get("close_noop"):
            apply_effect({"close": argv[2]})
        return 0, "", ""
    if cmd[0] == "api":
        return handle_api()
    return fail("fake gh: unsupported call " + joined)


def handle_api():
    paginate = "--paginate" in argv
    jq_expr = flag("--jq")
    path = None
    for item in argv[1:]:
        if not item.startswith("-") and item != jq_expr:
            path = item
            break
    if path is None:
        return fail("fake gh: no api path")
    route = path.split("?")[0]
    parts = route.split("/")
    repo = state["repo"]
    if parts[0] == "users" and len(parts) == 2:
        login = parts[1]
        name = state.get("users", {}).get(login)
        data = {"login": login, "name": name}
        if jq_expr is not None:
            code, out, err = jq_apply(data, jq_expr)
            return code, out, err
        return emit(data)
    if parts[:3] != ["repos", *repo.split("/")]:
        return fail("fake gh: wrong repository in api path " + path)
    rest = parts[3:]
    if rest[:1] == ["issues"] and len(rest) == 2:
        number = rest[1]
        if number in state.get("prs", {}) or number in state.get("pulls", []):
            data = {"number": int(number), "pull_request": {"url": "x"}}
        elif number in state.get("issues", {}):
            issue = state["issues"][number]
            data = {"number": int(number), "state": issue["state"].lower()}
        else:
            return fail("gh: Not Found (HTTP 404)")
        return emit(data)
    if rest[:1] == ["issues"] and len(rest) == 3 and rest[2] == "timeline":
        issue = state["issues"].get(rest[1])
        if issue is None:
            return fail("gh: Not Found (HTTP 404)")
        events = issue.get("timeline", [])
        pages = [events[i : i + 100] for i in range(0, len(events), 100)] or [[]]
        if not paginate:
            pages = pages[:1]
        out_text = ""
        for page in pages:
            if jq_expr is None:
                out_text += json.dumps(page) + "\n"
            else:
                code, out, err = jq_apply(page, jq_expr)
                if code != 0:
                    return code, "", err
                out_text += out
        return 0, out_text, ""
    if rest[:1] == ["collaborators"] and len(rest) == 3 and rest[2] == "permission":
        login = rest[1]
        entry = state.get("perms", {}).get(login, {"mode": "http404"})
        if isinstance(entry, str):
            entry = {"role": entry}
        mode = entry.get("mode")
        if mode == "http404":
            return fail("gh: Not Found (HTTP 404)")
        if mode == "http500":
            return fail("gh: Server Error (HTTP 500)")
        if mode == "net":
            return fail("error connecting to api.github.com")
        if mode == "notjson":
            return 0, "<html>oops</html>\n", ""
        if mode == "norole":
            data = {"login": login, "permission": "none"}
        else:
            role = entry.get("role", "")
            data = {"login": login, "permission": "write", "role_name": role}
        if jq_expr is not None:
            code, out, err = jq_apply(data, jq_expr)
            return code, out, err
        return emit(data)
    return fail("fake gh: unsupported api path " + path)


code, out, err = handle()
joined_args = " ".join(argv)
for rule in state.get("rules", []):
    if rule["match"] in joined_args and rule.get("when") == "after":
        rule["hits"] = rule.get("hits", 0) + 1
        nth = rule.get("nth")
        if nth is None or rule["hits"] == nth:
            apply_effect(rule.get("effect"))
save()
sys.stdout.write(out)
sys.stderr.write(err)
sys.exit(code)
"""

FAKE_ORCA = r"""
import json
import os
import sys

STATE = os.environ["ORCA_STATE"]
CALLS = os.environ["ORCA_CALLS"]
argv = sys.argv[1:]
with open(CALLS, "a", encoding="utf-8") as fh:
    fh.write(json.dumps(["orca"] + argv) + "\n")
with open(STATE, encoding="utf-8") as fh:
    state = json.load(fh)


def save():
    with open(STATE, "w", encoding="utf-8") as out:
        json.dump(state, out)


def reply(obj, code=0):
    sys.stdout.write(json.dumps(obj) + "\n")
    sys.exit(code)


joined = " ".join(argv)
for rule in state.get("rules", []):
    if rule["match"] in joined:
        sys.stderr.write(rule.get("stderr", "") + "\n")
        sys.stdout.write(rule.get("stdout", ""))
        sys.exit(rule.get("exit", 1))
if argv[:2] != ["orchestration", argv[1] if len(argv) > 1 else ""]:
    sys.exit(2)
verb = argv[1]
if verb == "run-current":
    reply({"id": "x", "ok": True, "result": {"run": state.get("run")}})
if state.get("run") is None and verb in ("task-list", "worker-list", "task-update"):
    reply({"ok": False, "error": {"code": "run_required"}}, 1)
if verb == "worker-list":
    reply({"ok": True, "result": {"workers": state.get("workers", [])}})
if verb == "task-list":
    reply({"ok": True, "result": {"tasks": state.get("tasks", [])}})
if verb == "task-update":
    task_id = argv[argv.index("--id") + 1]
    status = argv[argv.index("--status") + 1]
    for task in state.get("tasks", []):
        if task["id"] == task_id and not state.get("update_noop"):
            task["status"] = status
            task["result"] = argv[argv.index("--result") + 1]
    save()
    reply({"ok": True, "result": {"task": {"id": task_id, "status": status}}})
sys.exit(2)
"""

GIT_WRAPPER = """#!/bin/bash
# Records every git call (arguments joined by the unit separator) and forwards it.
{ printf '%s\\037' "$@"; printf '\\n'; } >> "$FAKE_GIT_LOG"
if [ "${1:-}" = "remote" ] && [ "${2:-}" = "get-url" ] && [ "${3:-}" = "origin" ] \\
    && [ -n "${FAKE_ORIGIN_URL:-}" ]; then
    if [ "$FAKE_ORIGIN_URL" = "none" ]; then
        exit 2
    fi
    printf '%s\\n' "$FAKE_ORIGIN_URL"
    exit 0
fi
exec "$REAL_GIT" "$@"
"""

FAKE_SUPERCLAUDE = """#!/bin/bash
# Fake `superclaude orchestrator report-entry`: prints FAKE_ENTRY_WORD.
printf '%s\\n' "$*" >> "$FAKE_SC_LOG"
if [ "${1:-}" = "orchestrator" ] && [ "${2:-}" = "report-entry" ]; then
    if [ "${3:-}" = "--help" ]; then
        exit 0
    fi
    printf '%s\\n' "${FAKE_ENTRY_WORD:-moved}"
    exit "${FAKE_ENTRY_RC:-0}"
fi
exit 2
"""


@dataclass
class Result:
    stdout: str
    stderr: str
    code: int

    @property
    def lines(self) -> list[str]:
        return self.stdout.splitlines()

    @property
    def line(self) -> str:
        assert len(self.lines) == 1, f"expected one stdout line: {self.stdout!r}"
        return self.lines[0]


def fields(line: str) -> dict[str, str]:
    """The key=value fields of a one-line script result."""
    out: dict[str, str] = {}
    for word in line.split()[1:]:
        if "=" in word:
            key, _, value = word.partition("=")
            out[key] = value
    return out


@dataclass
class Scratch:
    """A scratch repository with a bare ``origin`` and the fakes on ``PATH``."""

    root: Path
    origin: Path = field(init=False)
    seed: Path = field(init=False)
    work: Path = field(init=False)
    bin_dir: Path = field(init=False)
    home: Path = field(init=False)
    tmp: Path = field(init=False)
    state_path: Path = field(init=False)
    calls_path: Path = field(init=False)
    git_log: Path = field(init=False)
    orca_state: Path = field(init=False)
    orca_calls: Path = field(init=False)
    sc_log: Path = field(init=False)
    extra_env: dict[str, str] = field(default_factory=dict)

    def __post_init__(self) -> None:
        root = self.root
        self.origin = root / "origin.git"
        self.seed = root / "seed"
        self.work = root / "work"
        self.bin_dir = root / "bin"
        self.home = root / "home"
        self.tmp = root / "tmp"
        self.state_path = root / "gh-state.json"
        self.calls_path = root / "gh-calls.jsonl"
        self.git_log = root / "git-calls.log"
        self.orca_state = root / "orca-state.json"
        self.orca_calls = root / "orca-calls.jsonl"
        self.sc_log = root / "sc-calls.log"
        for d in (self.bin_dir, self.home, self.tmp):
            d.mkdir(parents=True, exist_ok=True)
        for path in (self.calls_path, self.git_log, self.orca_calls, self.sc_log):
            path.write_text("", encoding="utf-8")
        self._write_exec(self.bin_dir / "gh", f"#!{sys.executable}\n{FAKE_GH}", True)
        self._write_exec(self.bin_dir / "git", GIT_WRAPPER, False)
        self.state: dict = {
            "repo": REPO_SLUG,
            "clock": 0,
            "runner": {"login": "runner", "assoc": "MEMBER"},
            "prs": {},
            "pulls": [],
            "issues": {},
            "perms": {"runner": "maintain", "maint": "maintain"},
            "users": {},
            "pr_search": [],
            "open_search": [],
            "rules": [],
        }
        self.save_state()

    def ensure_repos(self) -> None:
        """Build the bare origin, the seed clone and the work clone on first use."""
        if not self.work.exists():
            self._make_repositories()

    # -- plumbing ---------------------------------------------------------

    @staticmethod
    def _write_exec(path: Path, text: str, _python: bool) -> None:
        path.write_text(text, encoding="utf-8")
        path.chmod(0o755)

    def env(self, **extra: str) -> dict[str, str]:
        system_dirs = ["/usr/bin", "/bin"]
        for tool in ("git", "jq", "bash"):
            found = shutil.which(tool)
            if found:
                parent = str(Path(found).parent)
                if parent not in system_dirs:
                    system_dirs.append(parent)
        env = {
            "PATH": os.pathsep.join([str(self.bin_dir), *system_dirs]),
            "HOME": str(self.home),
            "TMPDIR": str(self.tmp),
            "LC_ALL": "C",
            "GIT_CONFIG_GLOBAL": "/dev/null",
            "GIT_CONFIG_NOSYSTEM": "1",
            "GIT_AUTHOR_NAME": "Closeout Test",
            "GIT_AUTHOR_EMAIL": "closeout-test@example.com",
            "GIT_COMMITTER_NAME": "Closeout Test",
            "GIT_COMMITTER_EMAIL": "closeout-test@example.com",
            "GIT_TERMINAL_PROMPT": "0",
            "REAL_GIT": str(GIT),
            "FAKE_GIT_LOG": str(self.git_log),
            "FAKE_ORIGIN_URL": FAKE_ORIGIN_URL,
            "FAKE_STATE": str(self.state_path),
            "FAKE_CALLS": str(self.calls_path),
            "ORCA_STATE": str(self.orca_state),
            "ORCA_CALLS": str(self.orca_calls),
            "FAKE_SC_LOG": str(self.sc_log),
            # Canary values: no script may ever print or write them.
            "GH_TOKEN": "canary-gh-token-0001",
            "CLICKUP_API_TOKEN": "canary-clickup-token-0002",
        }
        env.update(self.extra_env)
        env.update(extra)
        return env

    def save_state(self) -> None:
        self.state_path.write_text(json.dumps(self.state), encoding="utf-8")

    def load_state(self) -> dict:
        self.state = json.loads(self.state_path.read_text(encoding="utf-8"))
        return self.state

    def git(self, cwd: Path, *args: str, check: bool = True) -> str:
        res = subprocess.run(
            [str(GIT), *args],
            cwd=cwd,
            env={k: v for k, v in self.env().items() if k != "FAKE_ORIGIN_URL"},
            text=True,
            capture_output=True,
            timeout=60,
        )
        if check and res.returncode != 0:
            raise AssertionError(f"git {args} failed: {res.stderr}")
        return res.stdout

    def run(
        self,
        script: Path,
        *args: str,
        stdin: str = "",
        env: dict[str, str] | None = None,
        cwd: Path | None = None,
    ) -> Result:
        res = subprocess.run(
            [str(BASH), str(script), *args],
            cwd=cwd or (self.work if self.work.exists() else self.root),
            env=env if env is not None else self.env(),
            input=stdin,
            text=True,
            capture_output=True,
            timeout=120,
        )
        return Result(res.stdout, res.stderr, res.returncode)

    # -- the repositories ---------------------------------------------------

    def _make_repositories(self) -> None:
        self.git(self.root, "init", "-q", "--bare", "-b", "main", str(self.origin))
        self.git(self.root, "clone", "-q", str(self.origin), str(self.seed))
        self.git(self.seed, "checkout", "-q", "-b", "main")
        self.commit_files(
            self.seed,
            {"keep.txt": "keep\n", "old.txt": "old\n", "gone.txt": "gone\n"},
            "base",
        )
        self.git(self.seed, "push", "-q", "origin", "main")
        self.git(self.root, "clone", "-q", str(self.origin), str(self.work))

    def commit_files(
        self, repo: Path, files: dict[str, str | None | tuple[str, str]], msg: str
    ) -> str:
        """Commit changes: text writes, ``None`` deletes, ``("mv", new)`` renames."""
        for name, content in files.items():
            if content is None:
                self.git(repo, "rm", "-q", "--", name)
            elif isinstance(content, tuple):
                self.git(repo, "mv", name, content[1])
            else:
                path = repo / name
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(content, encoding="utf-8")
                self.git(repo, "add", "--", name)
        self.git(repo, "commit", "-q", "--allow-empty", "-m", msg)
        return self.git(repo, "rev-parse", "HEAD").strip()

    def head(self) -> str:
        return self.git(self.seed, "rev-parse", "HEAD").strip()

    def pr_branch(
        self, number: int, commits: list[dict[str, str | None | tuple[str, str]]]
    ) -> str:
        """Create ``pr-<n>`` from the current base tip and keep ``refs/pull/<n>/head``."""
        self.ensure_repos()
        branch = f"pr-{number}"
        self.git(self.seed, "checkout", "-q", "-b", branch, "main")
        head = ""
        for index, files in enumerate(commits):
            head = self.commit_files(self.seed, files, f"pr {number} commit {index}")
        self.git(self.seed, "push", "-q", "origin", f"{branch}:refs/pull/{number}/head")
        self.git(self.seed, "checkout", "-q", "main")
        return head

    def squash(
        self,
        number: int,
        extra: dict[str, str | None | tuple[str, str]] | None = None,
    ) -> str:
        self.git(self.seed, "merge", "-q", "--squash", f"pr-{number}")
        if extra:
            for name, content in extra.items():
                (self.seed / name).write_text(content or "", encoding="utf-8")
                self.git(self.seed, "add", "--", name)
        self.git(self.seed, "commit", "-q", "-m", f"squash (#{number})")
        return self._finish_merge(number)

    def merge_commit(self, number: int) -> str:
        self.git(
            self.seed,
            "merge",
            "-q",
            "--no-ff",
            f"pr-{number}",
            "-m",
            f"Merge pull request #{number}",
        )
        return self._finish_merge(number)

    def rebase_merge(self, number: int) -> str:
        shas = self.git(self.seed, "rev-list", "--reverse", f"main..pr-{number}")
        for sha in shas.split():
            self.git(self.seed, "cherry-pick", sha)
        return self._finish_merge(number)

    def _finish_merge(self, number: int) -> str:
        merge = self.head()
        self.git(self.seed, "push", "-q", "origin", "main")
        self.git(self.seed, "branch", "-q", "-D", f"pr-{number}")
        return merge

    # -- canned pull requests, issues and fakes ------------------------------

    def add_pr(
        self,
        number: int,
        *,
        state: str = "MERGED",
        merge: str | None = None,
        head: str | None = None,
        base: str = "main",
        commits: int = 1,
        by: str | None = "octo",
        files: list[str] | None = None,
        title: str = "A harmless title",
        body: str = "",
        closing: list[tuple[str, int]] | None = None,
        merged_at: str = "2026-11-19T12:00:00Z",
    ) -> dict:
        pr = {
            "number": number,
            "state": state,
            "mergedAt": merged_at if state == "MERGED" else None,
            "mergedBy": {"login": by} if by else None,
            "mergeCommit": {"oid": merge} if merge else None,
            "baseRefName": base,
            "headRefName": f"pr-{number}",
            "headRefOid": head,
            "commits": [{"oid": f"{i:040x}"} for i in range(commits)],
            "url": f"https://github.com/{REPO_SLUG}/pull/{number}",
            "body": body,
            "title": title,
            "files": [{"path": name} for name in (files or [])],
            "changedFiles": len(files or []),
            "closingIssuesReferences": [
                {
                    "number": n,
                    "repository": {
                        "name": repo.split("/")[1],
                        "owner": {"login": repo.split("/")[0]},
                    },
                }
                for repo, n in (closing or [])
            ],
        }
        self.state["prs"][str(number)] = pr
        self.save_state()
        return pr

    def gh_calls(self) -> list[list[str]]:
        rows = self.calls_path.read_text(encoding="utf-8").splitlines()
        return [json.loads(row)[1:] for row in rows if row]

    def git_calls(self) -> list[list[str]]:
        text = self.git_log.read_text(encoding="utf-8")
        return [row.split("\x1f")[:-1] for row in text.split("\n") if row]

    def clear_calls(self) -> None:
        for path in (self.calls_path, self.git_log, self.orca_calls, self.sc_log):
            path.write_text("", encoding="utf-8")

    def install_orca(self, **state: object) -> None:
        self._write_exec(
            self.bin_dir / "orca", f"#!{sys.executable}\n{FAKE_ORCA}", True
        )
        data: dict = {"run": {"id": "run-1"}, "workers": [], "tasks": [], "rules": []}
        data.update(state)
        self.orca_state.write_text(json.dumps(data), encoding="utf-8")

    def orca_calls_list(self) -> list[list[str]]:
        rows = self.orca_calls.read_text(encoding="utf-8").splitlines()
        return [json.loads(row)[1:] for row in rows if row]

    def install_superclaude(self) -> None:
        self._write_exec(self.bin_dir / "superclaude", FAKE_SUPERCLAUDE, False)

    def status(self) -> str:
        self.ensure_repos()
        return self.git(self.work, "status", "--porcelain")


@pytest.fixture()
def scratch(tmp_path: Path) -> Scratch:
    return Scratch(tmp_path)


# ---------------------------------------------------------------------------
# Truth check: scripts/branch-landed.sh (section 4.5 of the design)
# ---------------------------------------------------------------------------

FORBIDDEN_IN_SCRIPT = (
    "merge-base",
    "--is-ancestor",
    "branch --merged",
    "rev-list",
    "git log",
    "python3",
)
FORBIDDEN_GIT_ARGS = ("merge-base", "--is-ancestor", "rev-list", "log")


def _check_git_calls(calls: list[list[str]], *, fetch: bool = True) -> None:
    """The recorded git calls never use ancestry and always use ``--no-renames``."""
    for args in calls:
        sub = args[0] if args else ""
        for word in FORBIDDEN_GIT_ARGS:
            assert word not in args, f"forbidden git call: {args}"
        assert not (sub == "branch" and "--merged" in args), args
        if sub == "diff":
            assert "--no-renames" in args, args
            assert any("..." in a for a in args), f"not a three-dot diff: {args}"
            assert not any(re.search(r"[^.]\.\.[^.]", a) for a in args), args
        elif sub == "diff-tree":
            assert "--no-renames" in args, args
        elif sub == "fetch":
            assert fetch, f"unexpected fetch: {args}"
        else:
            assert sub in ("remote", "fetch"), f"unexpected git call: {args}"


def _check_gh_calls_name_the_origin_repo(calls: list[list[str]]) -> None:
    for args in calls:
        if args[0] in ("pr", "issue", "label"):
            assert "--repo" in args and args[args.index("--repo") + 1] == REPO_SLUG
        text = " ".join(args)
        assert "SuperClaude-Org" not in text
        if args[0] == "api":
            assert any(
                a.startswith(f"repos/{REPO_SLUG}/") or a.startswith("users/")
                for a in args
            ), args


def _merged_state(
    scratch: Scratch,
    number: int,
    merge: str,
    head: str,
    commits: int = 1,
    by: str | None = "octo",
) -> None:
    scratch.add_pr(number, merge=merge, head=head, commits=commits, by=by)


def _expect_line(res: Result, token: str, code: int, **want: str) -> dict[str, str]:
    assert res.code == code, (res.code, res.stdout, res.stderr)
    line = res.line
    assert line.split()[0] == token, line
    got = fields(line)
    for key, value in want.items():
        assert got.get(key) == value, (key, line)
    return got


def test_truth_script_source_has_no_ancestry_and_no_python() -> None:
    text = BRANCH_LANDED.read_text(encoding="utf-8")
    for word in FORBIDDEN_IN_SCRIPT:
        assert word not in text, word
    assert EM_DASH not in text and EN_DASH not in text
    assert "/home/" not in text and "/Users/" not in text
    assert os.access(BRANCH_LANDED, os.X_OK)


def test_truth_squash_merge_is_merged_and_same(scratch: Scratch) -> None:
    head = scratch.pr_branch(41, [{"keep.txt": "keep 2\n"}, {"new.txt": "new\n"}])
    merge = scratch.squash(41)
    _merged_state(scratch, 41, merge, head, commits=2)
    # Ancestry would say "not landed": the original commits are not in the base.
    res = subprocess.run(
        [str(GIT), "merge-base", "--is-ancestor", head, "main"],
        cwd=scratch.seed,
        capture_output=True,
        env=scratch.env(),
    )
    assert res.returncode == 1
    scratch.clear_calls()
    out = scratch.run(BRANCH_LANDED, "41")
    got = _expect_line(out, "MERGED", 0, pr="41", by="octo", merge=merge, head=head)
    assert got["base"] == "main" and got["match"] == "same"
    assert got["url"] == f"https://github.com/{REPO_SLUG}/pull/41"
    calls = scratch.git_calls()
    _check_git_calls(calls)
    assert ["diff", "--no-renames", "--name-only", f"{merge}~1...{head}"] in calls
    _check_gh_calls_name_the_origin_repo(scratch.gh_calls())
    assert scratch.status() == ""


def test_truth_merge_commit_is_same_with_one_try(scratch: Scratch) -> None:
    head = scratch.pr_branch(42, [{"keep.txt": "k\n"}, {"other.txt": "o\n"}])
    merge = scratch.merge_commit(42)
    _merged_state(scratch, 42, merge, head, commits=2)
    scratch.clear_calls()
    out = scratch.run(BRANCH_LANDED, "#42")
    _expect_line(out, "MERGED", 0, match="same", merge=merge)
    trees = [c for c in scratch.git_calls() if c[0] == "diff-tree"]
    assert len(trees) == 1
    _check_git_calls(scratch.git_calls())


def test_truth_rebase_merge_needs_the_second_try(scratch: Scratch) -> None:
    head = scratch.pr_branch(
        43, [{"a.txt": "a\n"}, {"b.txt": "b\n"}, {"keep.txt": "k3\n"}]
    )
    # The base moves on, so the rebased commits get new ids and the first try differs.
    scratch.commit_files(scratch.seed, {"base2.txt": "moved\n"}, "base moves on")
    scratch.git(scratch.seed, "push", "-q", "origin", "main")
    merge = scratch.rebase_merge(43)
    _merged_state(scratch, 43, merge, head, commits=3)
    scratch.clear_calls()
    out = scratch.run(BRANCH_LANDED, "43")
    _expect_line(out, "MERGED", 0, match="same", merge=merge)
    calls = scratch.git_calls()
    trees = [c for c in calls if c[0] == "diff-tree"]
    assert len(trees) == 1 + 3, "one diff-tree for the first try, three for the second"
    assert ["diff", "--no-renames", "--name-only", f"{merge}~3...{head}"] in calls
    _check_git_calls(calls)


def test_truth_squash_that_renames_a_file_is_same_only_with_no_renames(
    scratch: Scratch,
) -> None:
    head = scratch.pr_branch(44, [{"old.txt": ("mv", "new.txt")}, {"keep.txt": "k2\n"}])
    merge = scratch.squash(44)
    _merged_state(scratch, 44, merge, head, commits=2)
    # Prove the reason for the flag in the scratch repository: without it the sets
    # differ, because git diff detects renames and git diff-tree does not.
    scratch.git(scratch.work, "fetch", "-q", "origin", "main", "refs/pull/44/head")
    held = scratch.git(
        scratch.work, "diff", "--name-only", f"{merge}~1...{head}"
    ).split()
    merged = scratch.git(
        scratch.work, "diff-tree", "-r", "--name-only", f"{merge}^1", merge
    ).split()
    assert set(held) != set(merged)
    scratch.clear_calls()
    out = scratch.run(BRANCH_LANDED, "44")
    _expect_line(out, "MERGED", 0, match="same")
    _check_git_calls(scratch.git_calls())


def test_truth_squash_that_deletes_a_file_is_same(scratch: Scratch) -> None:
    head = scratch.pr_branch(45, [{"gone.txt": None}, {"keep.txt": "k4\n"}])
    merge = scratch.squash(45)
    _merged_state(scratch, 45, merge, head, commits=2)
    out = scratch.run(BRANCH_LANDED, "45")
    _expect_line(out, "MERGED", 0, match="same")


def test_truth_a_pull_request_that_was_not_the_last_one_merged_is_same(
    scratch: Scratch,
) -> None:
    head1 = scratch.pr_branch(46, [{"keep.txt": "from 46\n"}])
    head2 = scratch.pr_branch(47, [{"old.txt": "from 47\n"}])
    merge1 = scratch.squash(46)
    merge2 = scratch.squash(47, extra=None)
    _merged_state(scratch, 46, merge1, head1)
    _merged_state(scratch, 47, merge2, head2)
    out1 = scratch.run(BRANCH_LANDED, "46")
    _expect_line(out1, "MERGED", 0, match="same", merge=merge1)
    out2 = scratch.run(BRANCH_LANDED, "47")
    _expect_line(out2, "MERGED", 0, match="same", merge=merge2)


def test_truth_a_merge_that_changed_other_files_is_differs(scratch: Scratch) -> None:
    head = scratch.pr_branch(48, [{"keep.txt": "k48\n"}])
    merge = scratch.squash(48, extra={"extra.txt": "added while merging\n"})
    _merged_state(scratch, 48, merge, head)
    out = scratch.run(BRANCH_LANDED, "48")
    _expect_line(out, "MERGED", 0, match="differs")


def test_truth_missing_merge_commit_prints_unknown_and_unchecked(
    scratch: Scratch,
) -> None:
    head = scratch.pr_branch(49, [{"keep.txt": "k49\n"}])
    scratch.squash(49)
    scratch.add_pr(49, merge=None, head=head)
    scratch.clear_calls()
    out = scratch.run(BRANCH_LANDED, "49")
    _expect_line(out, "MERGED", 0, merge="unknown", match="unchecked")
    assert [c for c in scratch.git_calls() if c[0] != "remote"] == []


def test_truth_merged_by_nobody_named_prints_unknown_login(scratch: Scratch) -> None:
    head = scratch.pr_branch(50, [{"keep.txt": "k50\n"}])
    merge = scratch.squash(50)
    _merged_state(scratch, 50, merge, head, by=None)
    out = scratch.run(BRANCH_LANDED, "50")
    _expect_line(out, "MERGED", 0, by="unknown", match="same")


def test_truth_merged_by_a_person_carries_the_login(scratch: Scratch) -> None:
    head = scratch.pr_branch(51, [{"keep.txt": "k51\n"}])
    merge = scratch.squash(51)
    _merged_state(scratch, 51, merge, head, by="Ironbelly")
    out = scratch.run(BRANCH_LANDED, "51")
    _expect_line(out, "MERGED", 0, by="Ironbelly")


def test_truth_open_prints_open_and_runs_no_fetch(scratch: Scratch) -> None:
    scratch.add_pr(52, state="OPEN", head="a" * 40)
    scratch.clear_calls()
    out = scratch.run(BRANCH_LANDED, "52")
    _expect_line(out, "OPEN", 1, pr="52")
    _check_git_calls(scratch.git_calls(), fetch=False)
    assert not [c for c in scratch.git_calls() if c[0] == "fetch"]


def test_truth_closed_without_merge_prints_closed_and_runs_no_fetch(
    scratch: Scratch,
) -> None:
    scratch.add_pr(53, state="CLOSED", head="b" * 40)
    scratch.clear_calls()
    out = scratch.run(BRANCH_LANDED, "53")
    _expect_line(out, "CLOSED", 4, pr="53")
    assert not [c for c in scratch.git_calls() if c[0] == "fetch"]


def test_truth_no_such_pull_request_prints_none(scratch: Scratch) -> None:
    out = scratch.run(BRANCH_LANDED, "999999")
    _expect_line(out, "NONE", 3, pr="999999")
    assert out.lines == ["NONE pr=999999"]


def test_truth_gh_failure_and_non_json_are_unknown(scratch: Scratch) -> None:
    scratch.state["rules"] = [
        {"match": "pr view 54", "exit": 1, "stderr": "HTTP 502: Bad Gateway"}
    ]
    scratch.save_state()
    out = scratch.run(BRANCH_LANDED, "54")
    _expect_line(out, "UNKNOWN", 2, reason="gh_failed")
    scratch.state["rules"] = [
        {"match": "pr view 55", "exit": 0, "stdout": "this is not json\n"}
    ]
    scratch.save_state()
    out = scratch.run(BRANCH_LANDED, "55")
    _expect_line(out, "UNKNOWN", 2, reason="bad_json")
    scratch.state["rules"] = [
        {"match": "pr view 56", "exit": 0, "stdout": '{"state": "ODD"}\n'}
    ]
    scratch.save_state()
    out = scratch.run(BRANCH_LANDED, "56")
    _expect_line(out, "UNKNOWN", 2, reason="bad_json")


def test_truth_url_for_another_repository_is_refused(scratch: Scratch) -> None:
    scratch.clear_calls()
    out = scratch.run(BRANCH_LANDED, "https://github.com/other-org/other-repo/pull/12")
    _expect_line(out, "UNKNOWN", 2, reason="foreign_repo")
    assert scratch.gh_calls() == []


def test_truth_url_for_this_repository_uses_only_the_number(scratch: Scratch) -> None:
    scratch.add_pr(57, state="OPEN", head="c" * 40)
    out = scratch.run(BRANCH_LANDED, f"https://github.com/{REPO_SLUG}/pull/57")
    _expect_line(out, "OPEN", 1, pr="57")
    out = scratch.run(BRANCH_LANDED, f"https://github.com/{REPO_SLUG}/pull/57/files")
    _expect_line(out, "OPEN", 1, pr="57")


@pytest.mark.parametrize(
    "argv",
    [[], ["abc"], ["0"], ["12", "13"], [""], ["https://example.com/x/y/pull/1"]],
)
def test_truth_bad_arguments_print_usage(scratch: Scratch, argv: list[str]) -> None:
    out = scratch.run(BRANCH_LANDED, *argv)
    _expect_line(out, "UNKNOWN", 2, reason="usage")
    assert scratch.gh_calls() == []


def test_truth_no_origin_or_not_github_is_no_origin(scratch: Scratch) -> None:
    for url in ("none", "https://gitlab.com/acme/widgets.git"):
        env = scratch.env(FAKE_ORIGIN_URL=url)
        out = scratch.run(BRANCH_LANDED, "12", env=env)
        _expect_line(out, "UNKNOWN", 2, reason="no_origin")
    assert scratch.gh_calls() == []


def test_truth_missing_jq_is_no_jq(scratch: Scratch, tmp_path: Path) -> None:
    empty = tmp_path / "empty-path"
    empty.mkdir()
    out = scratch.run(
        BRANCH_LANDED, "12", env={"PATH": str(empty), "HOME": str(tmp_path)}
    )
    _expect_line(out, "UNKNOWN", 2, reason="no_jq")


def test_truth_ignores_stdin_and_prints_one_line(scratch: Scratch) -> None:
    scratch.add_pr(58, state="OPEN", head="d" * 40)
    out = scratch.run(BRANCH_LANDED, "58", stdin="never read\n")
    assert out.stdout.count("\n") == 1


def test_truth_never_prints_a_secret(scratch: Scratch) -> None:
    scratch.add_pr(59, state="OPEN", head="e" * 40)
    out = scratch.run(BRANCH_LANDED, "59")
    for canary in ("canary-gh-token-0001", "canary-clickup-token-0002"):
        assert canary not in out.stdout and canary not in out.stderr


# ---------------------------------------------------------------------------
# settle.sh: a shared world for the issue, evidence and verdict tests
# ---------------------------------------------------------------------------

MERGE_SHA = "abcdef0123456789abcdef0123456789abcdef01"
ISSUE_N = 12
PR_N = 34
TITLE = "Distinctive Title Text"
OLD = "2026-11-19T09:00:00Z"
WRITE_VERBS = (
    ("issue", "comment"),
    ("issue", "close"),
    ("issue", "edit"),
    ("issue", "reopen"),
)

DEFAULT_CHECKED = [
    "- [issue_body] #12 | The issue lists one done criterion.",
    "- [issue_comments] #12 | No comment changes the criteria.",
    "- [target_pr] PR #34 | Merged and changes a.py and b.py.",
    "- [other_pr] none found | No other pull request names the issue.",
]
DEFAULT_CRITERIA = ["- [done_when] The widget works | delivered | PR #34: a.py, b.py"]
PARTLY_CRITERIA = [
    "- [done_when] The widget works | delivered | PR #34: a.py",
    "- [acceptance] The widget is documented | partly | PR #34: b.py",
]


def comment(
    body: str, login: str = "maint", assoc: str = "MEMBER", at: str = OLD
) -> dict:
    return {
        "body": body,
        "author": {"login": login} if login else None,
        "authorAssociation": assoc,
        "createdAt": at,
    }


def make_world(
    s: Scratch,
    *,
    body: str = "Fixes #12",
    closing: bool = True,
    files: tuple[str, ...] = ("a.py", "b.py"),
    title: str = TITLE,
    state: str = "OPEN",
    comments: list[dict] | None = None,
    timeline: list[dict] | None = None,
    by: str | None = "octo",
) -> None:
    s.add_pr(
        PR_N,
        merge=MERGE_SHA,
        head="f" * 40,
        by=by,
        files=list(files),
        title=title,
        body=body,
        closing=[(REPO_SLUG, ISSUE_N)] if closing else None,
    )
    s.state["issues"][str(ISSUE_N)] = {
        "state": state,
        "stateReason": "COMPLETED" if state == "CLOSED" else "",
        "title": "Widget issue",
        "body": "## Done when\n- The widget works",
        "comments": comments or [],
        "timeline": timeline or [],
    }
    s.state["users"]["octo"] = "Octo Cat"
    s.state["pr_search"] = [
        {
            "number": PR_N,
            "state": "MERGED",
            "mergedAt": "2026-11-19T12:00:00Z",
            "baseRefName": "main",
        }
    ]
    s.save_state()


def verdict_text(
    word: str = "done",
    *,
    issue: str = f"{REPO_SLUG}#{ISSUE_N}",
    pr: str = str(PR_N),
    checked: list[str] | None = None,
    criteria: list[str] | None = None,
    reason: str | None = "The change delivers the whole list.",
    unsettled: str | None = None,
    question: str | None = None,
) -> str:
    lines = [f"verdict: {word}", f"issue: {issue}", f"pr: {pr}"]
    if checked is not None or word:
        lines.append("checked:")
        lines.extend(DEFAULT_CHECKED if checked is None else checked)
    lines.append("criteria:")
    lines.extend(DEFAULT_CRITERIA if criteria is None else criteria)
    if unsettled is not None:
        lines.append(f"unsettled: {unsettled}")
    if question is not None:
        lines.append(f"question: {question}")
    if reason is not None:
        lines.append(f"reason: {reason}")
    return "\n".join(lines) + "\n"


def get_evidence(s: Scratch, *extra: str) -> Path:
    res = s.run(SETTLE, "evidence", str(PR_N), "--issue", str(ISSUE_N), *extra)
    assert res.code == 0, (res.stdout, res.stderr)
    return Path(fields(res.line)["dir"])


def write_verdict(directory: Path, text: str) -> Path:
    path = directory / "done-verdict.md"
    path.write_text(text, encoding="utf-8")
    return path


def run_issue(
    s: Scratch,
    *args: str,
    verdict: Path | None = None,
    directory: Path | None = None,
    what: str | None = None,
) -> Result:
    argv = [str(PR_N), *args]
    if verdict is not None:
        argv += ["--verdict", str(verdict)]
    if directory is not None:
        argv += ["--dir", str(directory)]
    if what is not None:
        argv += ["--what", what]
    return s.run(SETTLE, "issue", *argv)


def issue_with_verdict(
    s: Scratch, text: str, *args: str, what: str | None = None
) -> Result:
    """The two-step flow of the skill: the real evidence step, then the verdict."""
    directory = get_evidence(s)
    path = write_verdict(directory, text)
    return run_issue(s, *args, verdict=path, directory=directory, what=what)


def writes(s: Scratch) -> list[list[str]]:
    return [c for c in s.gh_calls() if tuple(c[:2]) in WRITE_VERBS]


def comments_of(s: Scratch) -> list[dict]:
    return s.load_state()["issues"][str(ISSUE_N)]["comments"]


def deny_names() -> list[str]:
    names = []
    for raw in DENY_NAMES.read_text(encoding="utf-8").splitlines():
        text = raw.strip()
        if text and not text.startswith("#"):
            names.append(text)
    return names


# ---------------------------------------------------------------------------
# settle.sh: the source scan
# ---------------------------------------------------------------------------


def test_settle_script_source_scan() -> None:
    text = SETTLE.read_text(encoding="utf-8")
    for word in FORBIDDEN_IN_SCRIPT:
        assert word not in text, word
    for word in (
        "worker-release",
        "worker-stop",
        "worker-abandon",
        "orchestration send",
        "gh pr merge",
        "git push",
        "git commit",
        "git add",
        "gh issue reopen",
        "gh issue edit",
        "gh api -X",
        "--method",
    ):
        assert word not in text, word
    assert EM_DASH not in text and EN_DASH not in text
    assert "/home/" not in text and "/Users/" not in text
    assert "src/superclaude" not in text
    assert os.access(SETTLE, os.X_OK)
    for line in text.splitlines():
        if re.search(r"\borca\b", line) and "orchestration" in line:
            assert " --pr" not in line and " --issue" not in line, line
    # orca is called from settle.sh only.
    assert "orca " not in BRANCH_LANDED.read_text(encoding="utf-8")
    for gh_line in re.findall(r"gh (?:issue|pr) [^\n]*", text):
        if gh_line.lstrip().startswith("#"):
            continue
        assert "--repo" in gh_line or "gh issue comment" in gh_line, gh_line


# ---------------------------------------------------------------------------
# Issue handling (test plan row 3)
# ---------------------------------------------------------------------------


def test_issue_closed_is_already_final_and_never_closed_twice(scratch: Scratch) -> None:
    make_world(scratch, state="CLOSED")
    res = run_issue(scratch)
    got = _expect_line(
        res, "ISSUE", 0, n="12", links="closing", how="already_closed", note="none"
    )
    assert got["reason"] == "COMPLETED"
    assert res.line.split()[1] == "already_final"
    assert writes(scratch) == []
    _check_gh_calls_name_the_origin_repo(scratch.gh_calls())


def test_issue_open_with_a_done_verdict_comments_then_closes(scratch: Scratch) -> None:
    make_world(scratch)
    res = issue_with_verdict(scratch, verdict_text(), what="Adds the widget files.")
    _expect_line(res, "ISSUE", 0, how="closed_now", note="posted", links="closing")
    assert res.line.split()[1] == "settled"
    calls = scratch.gh_calls()
    kinds = [tuple(c[:2]) for c in calls]
    wr = writes(scratch)
    assert [tuple(c[:2]) for c in wr] == [("issue", "comment"), ("issue", "close")]
    comment_args, close_args = wr
    assert comment_args[:5] == ["issue", "comment", "12", "--repo", REPO_SLUG]
    assert close_args == [
        "issue",
        "close",
        "12",
        "--repo",
        REPO_SLUG,
        "--reason",
        "completed",
    ]
    assert "--comment" not in close_args
    body = comment_args[comment_args.index("--body") + 1]
    assert "Octo Cat" in body and "#34" in body and "abcdef0" in body
    assert "Adds the widget files." in body
    assert body.rstrip().splitlines()[-1] == DONE_MARKER.format(pr=34)
    assert "Status: completed (merged)." in body
    assert "deployed" not in body.lower()
    # Each write is preceded by a state read (the note also by the marker read).
    i_comment = kinds.index(("issue", "comment"))
    i_close = kinds.index(("issue", "close"))
    assert ("issue", "view") in kinds[:i_comment]
    assert ("issue", "view") in kinds[i_comment:i_close]
    assert ("issue", "view") in kinds[i_close:]
    assert len(comments_of(scratch)) == 1
    assert scratch.load_state()["issues"]["12"]["state"] == "CLOSED"


@pytest.mark.parametrize(
    ("kind", "body", "closing", "extra"),
    [
        ("closing", "Fixes #12", True, []),
        ("closing", "Closes #12", False, []),
        ("refs", "Refs #12", False, []),
        ("refs", "Part of the work, see #12", False, []),
        ("none", "", False, ["--issue", "12"]),
    ],
)
def test_issue_links_are_read_as_data(
    scratch: Scratch, kind: str, body: str, closing: bool, extra: list[str]
) -> None:
    make_world(scratch, body=body, closing=closing)
    res = run_issue(scratch, *extra)
    got = _expect_line(res, "ISSUE", 1, why="no_verdict", n="12")
    assert got["links"] == kind
    assert writes(scratch) == []


def test_issue_no_issue_several_issues_and_the_pull_requests_own_number(
    scratch: Scratch,
) -> None:
    make_world(scratch, body="", closing=False)
    res = run_issue(scratch)
    _expect_line(res, "ISSUE", 1, why="no_issue_named", note="none")
    assert "n" not in fields(res.line)
    # The pull request's own number is dropped without a call.
    scratch.load_state()
    scratch.state["prs"]["34"]["body"] = "Refs #34"
    scratch.save_state()
    scratch.clear_calls()
    res = run_issue(scratch)
    _expect_line(res, "ISSUE", 1, why="no_issue_named")
    assert not [c for c in scratch.gh_calls() if c[:1] == ["api"]]
    res = run_issue(scratch, "--issue", "34")
    _expect_line(res, "ISSUE", 1, why="not_an_issue")
    # Two same-repository issues.
    scratch.load_state()
    scratch.state["prs"]["34"]["body"] = "Fixes #12 and Refs #13"
    for n in ("12", "13"):
        scratch.state["issues"][n] = {
            "state": "OPEN",
            "stateReason": "",
            "comments": [],
            "timeline": [],
        }
    scratch.save_state()
    res = run_issue(scratch)
    _expect_line(res, "ISSUE", 1, why="several_issues")
    assert writes(scratch) == []


def test_issue_filters_the_repository_and_issue_versus_pull_request(
    scratch: Scratch,
) -> None:
    make_world(scratch, body="", closing=False)
    state = scratch.load_state()
    # A closing row of another repository is ignored (so is the body that follows).
    state["prs"]["34"]["closingIssuesReferences"] = [
        {
            "number": 5,
            "repository": {"name": "other-repo", "owner": {"login": "other-org"}},
        }
    ]
    state["prs"]["34"]["body"] = "Closes other-org/other-repo#5"
    scratch.save_state()
    res = run_issue(scratch)
    _expect_line(res, "ISSUE", 1, why="no_issue_named")
    assert not [c for c in scratch.gh_calls() if c[:1] == ["api"]]
    # A bare number whose object has a pull_request key is dropped.
    state = scratch.load_state()
    state["prs"]["34"]["body"] = "Refs #40"
    state["pulls"] = ["40"]
    scratch.save_state()
    res = run_issue(scratch)
    _expect_line(res, "ISSUE", 1, why="no_issue_named")
    # A bare number whose object has no such key is the issue.
    state = scratch.load_state()
    state["prs"]["34"]["body"] = "Refs #12"
    scratch.save_state()
    res = run_issue(scratch)
    _expect_line(res, "ISSUE", 1, why="no_verdict", n="12", links="refs")
    # --issue with a pull request number.
    res = run_issue(scratch, "--issue", "40")
    _expect_line(res, "ISSUE", 1, why="not_an_issue")
    # A failed read of the object.
    state = scratch.load_state()
    state["rules"] = [{"match": "api repos/acme/widgets/issues/12", "exit": 1}]
    scratch.save_state()
    res = run_issue(scratch)
    _expect_line(res, "ISSUE", 1, why="issue_lookup_failed")
    # One same-repository and one other-repository issue: the same-repository one.
    state = scratch.load_state()
    state["rules"] = []
    state["prs"]["34"]["body"] = "Fixes other-org/other-repo#9 and Refs #12"
    scratch.save_state()
    res = run_issue(scratch)
    _expect_line(res, "ISSUE", 1, why="no_verdict", n="12")
    assert writes(scratch) == []


def test_issue_second_run_on_a_closed_issue_writes_nothing(scratch: Scratch) -> None:
    make_world(scratch)
    first = issue_with_verdict(scratch, verdict_text())
    _expect_line(first, "ISSUE", 0, how="closed_now")
    scratch.clear_calls()
    second = run_issue(scratch)
    _expect_line(second, "ISSUE", 0, how="already_closed", note="none")
    assert writes(scratch) == []


@pytest.mark.parametrize("variant", ["close_fails", "close_noop"])
def test_issue_failed_close_rerun_posts_no_second_note(
    scratch: Scratch, variant: str
) -> None:
    make_world(scratch)
    state = scratch.load_state()
    state[variant] = True
    scratch.save_state()
    first = issue_with_verdict(scratch, verdict_text())
    _expect_line(first, "ISSUE", 1, why="close_failed", note="posted")
    assert [tuple(c[:2]) for c in writes(scratch)] == [
        ("issue", "comment"),
        ("issue", "close"),
    ]
    state = scratch.load_state()
    state[variant] = False
    scratch.save_state()
    scratch.clear_calls()
    second = run_issue(scratch)
    _expect_line(second, "ISSUE", 0, how="closed_now", note="already_there")
    assert [tuple(c[:2]) for c in writes(scratch)] == [("issue", "close")]
    assert len(comments_of(scratch)) == 1


def test_issue_refused_post_is_note_failed_and_never_closes(scratch: Scratch) -> None:
    make_world(scratch)
    state = scratch.load_state()
    state["refuse_comment"] = True
    scratch.save_state()
    res = issue_with_verdict(scratch, verdict_text())
    _expect_line(res, "ISSUE", 1, why="note_failed", note="none")
    assert [tuple(c[:2]) for c in writes(scratch)] == [("issue", "comment")]


def test_issue_post_accepted_but_marker_not_read_back_is_note_failed(
    scratch: Scratch,
) -> None:
    make_world(scratch)
    state = scratch.load_state()
    state["comment_not_stored"] = True
    scratch.save_state()
    res = issue_with_verdict(scratch, verdict_text())
    _expect_line(res, "ISSUE", 1, why="note_failed")
    assert ("issue", "close") not in [tuple(c[:2]) for c in writes(scratch)]


def test_issue_closed_by_someone_between_the_read_and_the_guard(
    scratch: Scratch,
) -> None:
    make_world(scratch)
    state = scratch.load_state()
    state["rules"] = [
        {
            "match": "issue comment 12",
            "when": "after",
            "effect": {"close": "12"},
        }
    ]
    scratch.save_state()
    res = issue_with_verdict(scratch, verdict_text())
    _expect_line(res, "ISSUE", 0, how="already_closed", note="posted")
    assert res.line.split()[1] == "already_final"
    assert ("issue", "close") not in [tuple(c[:2]) for c in writes(scratch)]


def test_issue_marker_for_another_pull_request_does_not_count(
    scratch: Scratch,
) -> None:
    make_world(scratch, comments=[comment(DONE_MARKER.format(pr=35))])
    res = run_issue(scratch)
    _expect_line(res, "ISSUE", 1, why="no_verdict", note="none")
    make_world(scratch, comments=[comment(NOT_DONE_MARKER.format(pr=34))])
    res = run_issue(scratch)
    _expect_line(res, "ISSUE", 1, why="no_verdict", note="none")
    assert writes(scratch) == []


def test_issue_note_value_of_each_case(scratch: Scratch) -> None:
    # (a) closed: none; (b) closed now: posted; (f) rerun: posted then already_there;
    # (h) closed in between: posted; (g) refused: none; (d) no issue: none.
    make_world(scratch, state="CLOSED")
    assert fields(run_issue(scratch).line)["note"] == "none"
    make_world(scratch)
    assert fields(issue_with_verdict(scratch, verdict_text()).line)["note"] == "posted"
    make_world(scratch)
    state = scratch.load_state()
    state["close_fails"] = True
    scratch.save_state()
    assert fields(issue_with_verdict(scratch, verdict_text()).line)["note"] == "posted"
    state = scratch.load_state()
    state["close_fails"] = False
    scratch.save_state()
    assert fields(run_issue(scratch).line)["note"] == "already_there"
    make_world(scratch, body="", closing=False)
    assert fields(run_issue(scratch).line)["note"] == "none"


def test_issue_match_differs_wins_over_a_done_verdict(scratch: Scratch) -> None:
    make_world(scratch)
    directory = get_evidence(scratch)
    path = write_verdict(directory, verdict_text())
    scratch.clear_calls()
    res = run_issue(scratch, "--match", "differs", verdict=path, directory=directory)
    _expect_line(res, "ISSUE", 1, why="merge_differs")
    assert scratch.gh_calls() == []
    res = run_issue(scratch, "--issue", "12", "--match", "differs")
    _expect_line(res, "ISSUE", 1, why="merge_differs", n="12")
    assert scratch.gh_calls() == []


# ---------------------------------------------------------------------------
# The done-check verdict (test plan rows 15 to 23)
# ---------------------------------------------------------------------------

UNCLEAR_TEXT = verdict_text(
    "unclear_escalate",
    criteria=["- [done_when] The widget works | unknown | none"],
    unsettled="The behaviour cannot be checked from files.",
    question="Does the widget work in the field?",
)
NOT_DONE_TEXT = verdict_text("not_done", criteria=PARTLY_CRITERIA)


def _no_write_and_refused(res: Result, scratch: Scratch) -> None:
    assert res.code == 1, (res.stdout, res.stderr)
    assert fields(res.line)["why"] == "no_verdict", res.line
    assert writes(scratch) == []


def test_verdict_shape_accepts_each_closed_word(scratch: Scratch) -> None:
    make_world(scratch)
    done = issue_with_verdict(scratch, verdict_text())
    _expect_line(done, "ISSUE", 0, how="closed_now")
    make_world(scratch)
    not_done = issue_with_verdict(scratch, NOT_DONE_TEXT)
    _expect_line(not_done, "ISSUE", 0, how="left_open", note="posted", remaining="1")
    make_world(scratch)
    unclear = issue_with_verdict(scratch, UNCLEAR_TEXT)
    _expect_line(unclear, "ISSUE", 1, why="unclear", note="none")
    assert "question: " not in unclear.stdout
    assert "Does the widget work in the field?" in unclear.stderr


def _drop(prefix: str):
    return lambda text: (
        "\n".join(ln for ln in text.splitlines() if not ln.startswith(prefix)) + "\n"
    )


MALFORMED = {
    "no_verdict_key": lambda t: t.split("\n", 1)[1],
    "a_fourth_word": lambda t: t.replace("verdict: done", "verdict: maybe"),
    "missing_reason": _drop("reason:"),
    "reason_of_41_words": lambda t: t.replace(
        "The change delivers the whole list.", " ".join(["word"] * 41)
    ),
    "reason_on_two_lines": lambda t: t + "and a second line\n",
    "empty_reason": lambda t: t.replace(
        "reason: The change delivers the whole list.", "reason:"
    ),
    "placeholder_reason": lambda t: t.replace(
        "The change delivers the whole list.", "<one plain sentence>"
    ),
    "missing_criteria": lambda t: t.replace(DEFAULT_CRITERIA[0] + "\n", ""),
    "missing_checked_list": lambda t: (
        "\n".join(
            ln
            for ln in t.splitlines()
            if not ln.startswith(("checked:", "- [issue", "- [target", "- [other"))
        )
        + "\n"
    ),
    "delivered_word_outside_the_set": lambda t: t.replace(
        " | delivered | ", " | finished | "
    ),
    "done_with_a_not_delivered": lambda t: t.replace(
        " | delivered | ", " | not_delivered | "
    ),
    "issue_line_differs": lambda t: t.replace("acme/widgets#12", "acme/widgets#13"),
    "pr_line_differs": lambda t: t.replace("pr: 34", "pr: 35"),
    "kind_outside_the_set": lambda t: t.replace("[issue_body]", "[the_body]"),
    "checked_without_what_was_found": lambda t: t.replace(
        " | The issue lists one done criterion.", ""
    ),
    "source_outside_the_set": lambda t: t.replace("[done_when]", "[hunch]"),
    "pr_not_in_the_fixed_form": lambda t: t.replace(
        "[target_pr] PR #34", "[target_pr] 34"
    ),
    "cited_part_without_files": lambda t: t.replace("PR #34: a.py, b.py", "PR #34"),
    "delivered_with_none": lambda t: t.replace("PR #34: a.py, b.py", "none"),
    "unknown_key": lambda t: t + "mood: fine\n",
    "repeated_key": lambda t: t + "reason: again\n",
    "text_before_the_first_key": lambda t: "hello\n" + t,
}


@pytest.mark.parametrize("name", sorted(MALFORMED))
def test_verdict_shape_refuses_a_malformed_file(scratch: Scratch, name: str) -> None:
    make_world(scratch)
    res = issue_with_verdict(scratch, MALFORMED[name](verdict_text()))
    _no_write_and_refused(res, scratch)
    assert res.stderr.strip(), "the reason of a refusal goes to stderr"


@pytest.mark.parametrize("word", ["done", "not_done", "unclear_escalate"])
@pytest.mark.parametrize(
    "missing", ["issue_body", "issue_comments", "target_pr", "other_pr"]
)
def test_verdict_shape_refuses_a_checked_list_without_a_required_kind(
    scratch: Scratch, word: str, missing: str
) -> None:
    make_world(scratch)
    checked = [ln for ln in DEFAULT_CHECKED if f"[{missing}]" not in ln]
    extra = {}
    if word == "unclear_escalate":
        extra = {"unsettled": "x", "question": "y"}
    criteria = PARTLY_CRITERIA if word == "not_done" else None
    res = issue_with_verdict(
        scratch, verdict_text(word, checked=checked, criteria=criteria, **extra)
    )
    _no_write_and_refused(res, scratch)


@pytest.mark.parametrize("omit", ["unsettled", "question"])
def test_verdict_unclear_needs_unsettled_and_question(
    scratch: Scratch, omit: str
) -> None:
    make_world(scratch)
    args = {"unsettled": "x", "question": "y"}
    args[omit] = None  # type: ignore[assignment]
    res = issue_with_verdict(scratch, verdict_text("unclear_escalate", **args))
    _no_write_and_refused(res, scratch)


def test_verdict_not_done_with_every_criterion_delivered_is_refused(
    scratch: Scratch,
) -> None:
    make_world(scratch)
    res = issue_with_verdict(scratch, verdict_text("not_done"))
    _no_write_and_refused(res, scratch)


def test_verdict_without_a_usable_dir_is_refused_as_no_verdict(
    scratch: Scratch, tmp_path: Path
) -> None:
    make_world(scratch)
    directory = get_evidence(scratch)
    path = write_verdict(directory, verdict_text())
    _no_write_and_refused(run_issue(scratch, verdict=path), scratch)
    _no_write_and_refused(
        run_issue(scratch, verdict=path, directory=tmp_path / "missing"), scratch
    )
    empty = tmp_path / "empty-dir"
    empty.mkdir()
    _no_write_and_refused(run_issue(scratch, verdict=path, directory=empty), scratch)
    # An evidence file that names another pull request.
    text = (directory / "evidence.md").read_text(encoding="utf-8")
    (directory / "evidence.md").write_text(
        text.replace("pr: 34", "pr: 35", 1), encoding="utf-8"
    )
    _no_write_and_refused(
        run_issue(scratch, verdict=path, directory=directory), scratch
    )


def test_verdict_refuses_a_quoted_pull_request_title(scratch: Scratch) -> None:
    make_world(scratch)
    for text in (
        verdict_text(reason=f"Delivers the {TITLE.lower()} work."),
        verdict_text(
            criteria=[f"- [done_when] {TITLE.upper()} | delivered | PR #34: a.py"]
        ),
    ):
        _no_write_and_refused(issue_with_verdict(scratch, text), scratch)
    # A --what sentence that holds the title is replaced by the default sentence.
    res = issue_with_verdict(scratch, verdict_text(), what=f"It is the {TITLE}.")
    _expect_line(res, "ISSUE", 0, how="closed_now")
    body = comments_of(scratch)[0]["body"]
    assert "2 files changed." in body
    assert TITLE not in body


def _place(name: str, where: str) -> Path | str:
    text = f"Written with {name} in it."
    if where == "reason":
        return verdict_text(reason=text)
    if where == "criterion":
        return verdict_text(
            criteria=[f"- [done_when] {text} | delivered | PR #34: a.py"]
        )
    if where == "checked":
        return verdict_text(
            checked=[DEFAULT_CHECKED[0].replace("The issue lists", text)]
            + DEFAULT_CHECKED[1:]
        )
    return verdict_text(
        "unclear_escalate",
        criteria=["- [done_when] The widget works | unknown | none"],
        unsettled=text if where == "unsettled" else "x",
        question=text if where == "question" else "y",
    )


@pytest.mark.parametrize(
    "name", [*deny_names(), "A" + EM_DASH + "B", "A" + EN_DASH + "B"]
)
def test_verdict_refuses_an_agent_or_model_name_or_a_dash(
    scratch: Scratch, name: str
) -> None:
    make_world(scratch)
    directory = get_evidence(scratch)
    path = directory / "done-verdict.md"
    for where in ("reason", "criterion", "checked", "unsettled", "question"):
        for form in {name, name.upper(), name.capitalize()}:
            path.write_text(_place(form, where), encoding="utf-8")
            res = run_issue(scratch, verdict=path, directory=directory)
            _no_write_and_refused(res, scratch)
    # The same name or dash in the --what sentence is replaced by the default one.
    path.write_text(verdict_text(), encoding="utf-8")
    res = run_issue(
        scratch, verdict=path, directory=directory, what=f"Done by {name} today."
    )
    _expect_line(res, "ISSUE", 0, how="closed_now")
    body = comments_of(scratch)[0]["body"]
    assert name not in body and "2 files changed." in body


def test_verdict_names_inside_a_path_are_not_refused(scratch: Scratch) -> None:
    make_world(scratch, files=("src/superclaude/skills/x.md", ".claude/settings.json"))
    criteria = [
        "- [done_when] The skill file changes | delivered | PR #34: src/superclaude/skills/x.md",
        "- [acceptance] The settings file changes | delivered | PR #34: .claude/settings.json",
    ]
    res = issue_with_verdict(scratch, verdict_text(criteria=criteria))
    _expect_line(res, "ISSUE", 0, how="closed_now")
    # A name next to a path, and a hyphenated compound, is still refused.
    make_world(scratch)
    scratch.clear_calls()
    bad = verdict_text(reason=f"See skills/x.md for the {deny_names()[0]}-code change.")
    _no_write_and_refused(issue_with_verdict(scratch, bad), scratch)


def test_done_verdict_goes_on_to_the_two_guarded_writes(scratch: Scratch) -> None:
    make_world(scratch)
    criteria = [
        f"- [done_when] Criterion {i} | delivered | PR #34: a.py" for i in range(1, 13)
    ]
    res = issue_with_verdict(scratch, verdict_text(criteria=criteria))
    _expect_line(res, "ISSUE", 0, how="closed_now", note="posted")
    comment_args = writes(scratch)[0]
    body = comment_args[comment_args.index("--body") + 1]
    assert "Why the issue is done: The change delivers the whole list." in body
    assert "- Criterion 10 (PR #34)" in body and "Criterion 11" not in body
    assert "and 2 more" in body
    assert "The pull request closes this issue with a closing keyword." in body
    assert [tuple(c[:2]) for c in writes(scratch)] == [
        ("issue", "comment"),
        ("issue", "close"),
    ]


def test_not_done_posts_one_marked_note_and_never_closes(scratch: Scratch) -> None:
    make_world(scratch)
    directory = get_evidence(scratch)
    criteria = [
        "- [done_when] First | delivered | PR #34: a.py",
        *[f"- [acceptance] Part {i} | not_delivered | none" for i in range(1, 12)],
        "- [other] Half done | partly | PR #34: b.py",
    ]
    path = write_verdict(directory, verdict_text("not_done", criteria=criteria))
    res = run_issue(scratch, verdict=path, directory=directory)
    got = _expect_line(res, "ISSUE", 0, how="left_open", note="posted")
    assert got["remaining"] == "12", "11 not_delivered plus 1 partly"
    wr = writes(scratch)
    assert [tuple(c[:2]) for c in wr] == [("issue", "comment")]
    body = wr[0][wr[0].index("--body") + 1]
    assert "Part 1 (no pull request yet)" in body
    assert "Half done (delivered in part by PR #34)" not in body, "cut at ten lines"
    assert "and 2 more" in body
    assert "Why: The change delivers the whole list." in body
    assert body.rstrip().splitlines()[-1] == NOT_DONE_MARKER.format(pr=34)
    assert "Status: completed" not in body
    # The verdict file stays in the private directory, outside the repository.
    assert path.exists() and scratch.work not in path.parents
    assert scratch.load_state()["issues"]["12"]["state"] == "OPEN"
    # No worker, no plan and no Dispatch is started.
    for call in scratch.gh_calls() + scratch.orca_calls_list():
        assert "worker-start" not in call and "--plan" not in call
    # A rerun with the marker present records no write and prints note=already_there.
    scratch.clear_calls()
    again = run_issue(scratch, verdict=path, directory=directory)
    _expect_line(
        again, "ISSUE", 0, how="left_open", note="already_there", remaining="12"
    )
    assert writes(scratch) == []
    # The two markers never match each other.
    assert DONE_MARKER.format(pr=34) not in NOT_DONE_MARKER.format(pr=34)
    assert NOT_DONE_MARKER.format(pr=34) not in DONE_MARKER.format(pr=34)


def test_not_done_with_a_failed_post_is_note_failed_without_a_hand_back(
    scratch: Scratch,
) -> None:
    make_world(scratch)
    state = scratch.load_state()
    state["refuse_comment"] = True
    scratch.save_state()
    res = issue_with_verdict(scratch, NOT_DONE_TEXT)
    _expect_line(res, "ISSUE", 1, why="note_failed")
    assert "remaining" not in fields(res.line)


def test_handback_sentence_is_in_the_settle_reference() -> None:
    text = (REFS_DIR / "settle.md").read_text(encoding="utf-8")
    sentence = (
        "The issue is not done and stays open with one note of what remains. "
        "The orchestrator takes the rest from here; by hand, run "
        "`/sc:issue --plan <N>` and start a worker on what remains."
    )
    assert sentence in text
    for name in deny_names():
        assert not re.search(rf"\b{name}\b", sentence, re.IGNORECASE)


def test_unclear_and_missing_verdict_write_nothing(scratch: Scratch) -> None:
    make_world(scratch)
    directory = get_evidence(scratch)
    for call in (
        run_issue(scratch),
        run_issue(scratch, verdict=directory / "absent.md", directory=directory),
        run_issue(scratch, verdict=write_verdict(directory, ""), directory=directory),
    ):
        _expect_line(call, "ISSUE", 1, why="no_verdict", n="12", note="none")
    path = write_verdict(directory, UNCLEAR_TEXT)
    res = run_issue(scratch, verdict=path, directory=directory)
    _expect_line(res, "ISSUE", 1, why="unclear", note="none")
    assert writes(scratch) == []
    # An already closed issue needs no verdict.
    make_world(scratch, state="CLOSED")
    _expect_line(run_issue(scratch), "ISSUE", 0, how="already_closed")


def test_a_refs_only_issue_with_a_done_verdict_closes(scratch: Scratch) -> None:
    make_world(scratch, body="Refs #12", closing=False)
    res = issue_with_verdict(scratch, verdict_text())
    _expect_line(res, "ISSUE", 0, links="refs", how="closed_now")
    assert scratch.load_state()["issues"]["12"]["state"] == "CLOSED"
    body = comments_of(scratch)[0]["body"]
    assert "names this issue without closing it" in body


def test_a_closes_linked_issue_with_a_not_done_verdict_does_not_close(
    scratch: Scratch,
) -> None:
    make_world(scratch, body="Closes #12")
    res = issue_with_verdict(scratch, NOT_DONE_TEXT)
    _expect_line(res, "ISSUE", 0, links="closing", how="left_open")
    assert [tuple(c[:2]) for c in writes(scratch)] == [("issue", "comment")]
    assert scratch.load_state()["issues"]["12"]["state"] == "OPEN"

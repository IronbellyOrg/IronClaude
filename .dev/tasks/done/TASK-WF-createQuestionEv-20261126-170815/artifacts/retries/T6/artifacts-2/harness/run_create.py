#!/usr/bin/env python3
"""Controlled `/sc:issue --create` runs for issue 834 (see harness-feasibility.md).

A run starts an interactive Claude Code session in `tmux`, in an isolated home
seeded from `src/`, with a fake `gh` first on PATH, no credentials, a clone whose
push URL is invalid, and answers the question screen with "keep my wording".
The session transcripts are the event log; the fake `gh` log is the post count.

    run_create.py --self-test
    run_create.py seed
    run_create.py run --name N --depth quick|standard|deep --description TEXT \
        [--mode feature|bug] [--type T] --expect-questions Q --expect-create C \
        [--expect-comments K]
    run_create.py check-stop
    run_create.py clear-pending --note TEXT

Raw output goes to the scratch directory (QEV_SCRATCH, default
/tmp/createQuestionEv-scratch), never into the repository. Exit status of `run`:
0 normal, 3 matrix already stopped, 4 a stop condition met in this run, 5 the
session could not be started.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shlex
import shutil
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = Path(os.environ.get("QEV_REPO_ROOT") or HERE.parents[5]).resolve()
SCRATCH = Path(os.environ.get("QEV_SCRATCH", "/tmp/createQuestionEv-scratch"))
HOME = SCRATCH / "home"
BIN = SCRATCH / "fakebin"
RUNS = SCRATCH / "runs"
STOP_FILE = SCRATCH / "STOP"
PENDING_FILE = SCRATCH / "PENDING-REVIEW"
FORK = "IronbellyOrg/IronClaude"
REAL_HOME = Path(os.path.expanduser("~")).resolve()
NODE_BIN = os.environ.get("QEV_NODE_BIN", "/opt/nvm/versions/node/v24.22.2/bin")
PASS_ENV = [
    "ANTHROPIC_AUTH_TOKEN",
    "ANTHROPIC_BASE_URL",
    "ANTHROPIC_MODEL",
    "ANTHROPIC_DEFAULT_HAIKU_MODEL",
    "ANTHROPIC_DEFAULT_OPUS_MODEL",
    "ANTHROPIC_DEFAULT_SONNET_MODEL",
    "CLAUDE_CODE_DISABLE_EXPERIMENTAL_BETAS",
    "CLAUDE_CODE_ENABLE_GATEWAY_MODEL_DISCOVERY",
]
TIMEOUTS = {"quick": 1200, "standard": 1800, "deep": 2700}
ANSWER_LABEL = "keep my wording"
INVALID_PUSH_URL = "invalid://blocked-no-push"
FALSE_FILES = ("create_issue.py", "issue_logger.py")


# ---------------------------------------------------------------- small helpers


def sha256(path: Path) -> str:
    try:
        return hashlib.sha256(path.read_bytes()).hexdigest() if path.is_file() else "-"
    except OSError:  # a guessed path such as /root/.claude is not readable
        return "-"


def run(cmd: list[str], **kw) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, capture_output=True, text=True, **kw)


def nap(seconds: float) -> None:
    time.sleep(seconds)


def utc() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def src_root() -> Path:
    return REPO / "src" / "superclaude"


def load_list() -> list[str]:
    """Every file of src/superclaude that a create run can read."""
    base = src_root()
    rels = sorted(str(p.relative_to(base)) for p in (base / "skills/sc-issue-protocol").rglob("*") if p.is_file())
    rels += [f"agents/issue-worker-t{n}.md" for n in (1, 2, 3)]
    rels += ["commands/issue.md", "commands/analyze.md", "skills/sc-adversarial-protocol/SKILL.md"]
    return rels


def home_path(rel: str, base: Path) -> Path:
    """Where a src-relative file lives under a Claude config folder."""
    if rel.startswith("commands/"):
        return base / "commands/sc" / Path(rel).name
    return base / rel


def src_for_home_path(path: Path) -> Path | None:
    """The src counterpart of a path under the seeded home's .claude, or None."""
    try:
        rel = path.resolve().relative_to((HOME / ".claude").resolve())
    except ValueError:
        return None
    parts = rel.parts
    if parts and parts[0] == "commands" and len(parts) >= 3 and parts[1] == "sc":
        return src_root() / "commands" / Path(*parts[2:])
    if parts and parts[0] in ("skills", "agents"):
        return src_root() / rel
    return None


# ------------------------------------------------------------------ the stop file


def check_stop() -> str | None:
    if STOP_FILE.exists():
        return "STOP file: " + STOP_FILE.read_text(encoding="utf-8").strip()[:300]
    if PENDING_FILE.exists():
        return "PENDING-REVIEW file (unattributed fork activity is held for the orchestrator): " + PENDING_FILE.read_text(
            encoding="utf-8"
        ).strip()[:300]
    return None


def write_stop(reason: str, run_name: str) -> None:
    SCRATCH.mkdir(parents=True, exist_ok=True)
    STOP_FILE.write_text(json.dumps({"reason": reason, "run": run_name, "at": utc()}), encoding="utf-8")


# ---------------------------------------------------------------- environment


def seed_home() -> dict[str, str]:
    """Copy src commands, skills and agents into the isolated home; return hash facts."""
    claude = HOME / ".claude"
    for sub in ("commands", "skills", "agents"):
        shutil.rmtree(claude / sub, ignore_errors=True)
    (claude / "commands/sc").mkdir(parents=True, exist_ok=True)
    (claude / "skills").mkdir(parents=True, exist_ok=True)
    (claude / "agents").mkdir(parents=True, exist_ok=True)
    (HOME / ".config/gh-empty").mkdir(parents=True, exist_ok=True)
    (SCRATCH / "tmp").mkdir(parents=True, exist_ok=True)
    for src in sorted((src_root() / "commands").glob("*.md")):
        shutil.copy2(src, claude / "commands/sc" / src.name)
    for src in sorted((src_root() / "skills").iterdir()):
        if src.is_dir():
            shutil.copytree(src, claude / "skills" / src.name, dirs_exist_ok=True)
    for src in sorted((src_root() / "agents").glob("*.md")):
        shutil.copy2(src, claude / "agents" / src.name)
    BIN.mkdir(parents=True, exist_ok=True)
    shutil.copy2(HERE / "fake_gh.py", BIN / "gh")
    (BIN / "gh").chmod(0o755)
    facts = {}
    for rel in load_list():
        a, b = sha256(src_root() / rel), sha256(home_path(rel, claude))
        if a != b:
            raise SystemExit(f"seeded copy differs from src for {rel}")
        facts[rel] = a
    return facts


def trust_config(clone: Path) -> None:
    """Pre-seed onboarding, the trusted clone and the daily closed-issue check key."""
    data = {
        "hasCompletedOnboarding": True,
        "theme": "dark",
        "numStartups": 5,
        "closedIssuesLastChecked": int(time.time() * 1000),
        "projects": {
            str(clone): {
                "hasTrustDialogAccepted": True,
                "allowedTools": [],
                "hasCompletedProjectOnboarding": True,
                "projectOnboardingSeenCount": 3,
            }
        },
    }
    for target in (HOME / ".claude.json", HOME / ".claude/.claude.json"):
        target.write_text(json.dumps(data), encoding="utf-8")


def run_env(run_dir: Path) -> dict[str, str]:
    """The environment of a run, without any credential. Gateway variables are added by launch.sh by reference."""
    return {
        "HOME": str(HOME),
        "CLAUDE_CONFIG_DIR": str(HOME / ".claude"),
        "XDG_CONFIG_HOME": str(HOME / ".config"),
        "GH_CONFIG_DIR": str(HOME / ".config/gh-empty"),
        "GIT_CONFIG_GLOBAL": "/dev/null",
        "GIT_CONFIG_NOSYSTEM": "1",
        "GIT_TERMINAL_PROMPT": "0",
        "PATH": f"{BIN}:{NODE_BIN}:/usr/local/bin:/usr/bin:/bin",
        "LANG": "C.UTF-8",
        "TERM": "xterm-256color",
        "TMPDIR": str(SCRATCH / "tmp"),
        "FAKE_GH_LOG": str(run_dir / "gh.log"),
        "FAKE_GH_STATE": str(run_dir / "gh-state.json"),
        "FAKE_GH_DIR": str(run_dir / "gh-posted"),
        "FAKE_GH_REPO": FORK,
    }


def make_clone(path: Path) -> str:
    """A shared clone of the worktree's HEAD with a GitHub fetch URL and an invalid push URL."""
    shutil.rmtree(path, ignore_errors=True)
    path.parent.mkdir(parents=True, exist_ok=True)
    head = run(["git", "-C", str(REPO), "rev-parse", "HEAD"]).stdout.strip()
    for cmd in (
        ["git", "clone", "-q", "--shared", "--no-checkout", str(REPO), str(path)],
        ["git", "-C", str(path), "checkout", "-q", "-B", "qev-run", head],
        ["git", "-C", str(path), "remote", "set-url", "origin", f"https://github.com/{FORK}"],
        ["git", "-C", str(path), "config", "remote.origin.pushurl", INVALID_PUSH_URL],
        ["git", "-C", str(path), "config", "user.email", "run@example.invalid"],
        ["git", "-C", str(path), "config", "user.name", "controlled run"],
    ):
        done = run(cmd)
        if done.returncode:
            raise SystemExit(f"clone step failed: {cmd[:5]}: {done.stderr.strip()[:200]}")
    hook = path / ".git/hooks/pre-push"
    hook.write_text('#!/bin/sh\necho "pre-push blocked (controlled run)" >&2\nexit 1\n', encoding="utf-8")
    hook.chmod(0o755)
    # project settings of the repository carry hooks that point at user-home scripts; a run uses none
    shutil.rmtree(path / ".claude", ignore_errors=True)
    return head


def launch_script(run_dir: Path, clone: Path) -> Path:
    """launch.sh: `env -i` with an explicit list; gateway variables by reference, never by value."""
    env = run_env(run_dir)
    pairs = " ".join(f"{k}={shlex.quote(v)}" for k, v in env.items())
    refs = " ".join(f'{k}="${k}"' for k in PASS_ENV)
    text = (
        "#!/bin/bash\n"
        f"cd {shlex.quote(str(clone))}\n"
        f"exec env -i {pairs} {refs} claude --permission-mode manual "
        '--allowedTools "Read Write Edit Task Skill Bash Glob Grep" --strict-mcp-config\n'
    )
    run_dir.mkdir(parents=True, exist_ok=True)
    path = run_dir / "launch.sh"
    path.write_text(text, encoding="utf-8")
    path.chmod(0o755)
    return path


# ----------------------------------------------------------------- fork activity


def _real_gh() -> str:
    found = shutil.which("gh")
    return found or str(REAL_HOME / ".local/bin/gh")


def gh_get(path: str, jq: str | None = None, paginate: bool = False) -> list:
    """Read-only GET against the fork, made by this process with the real credentials."""
    if not path.startswith(f"repos/{FORK}/") or " " in path:
        raise ValueError("fork-activity check only reads repos/" + FORK)
    cmd = [_real_gh(), "api", path]
    if paginate:
        cmd.append("--paginate")
    if jq:
        cmd += ["--jq", jq]
    done = run(cmd, timeout=120)
    if done.returncode:
        raise RuntimeError(done.stderr.strip()[:200])
    out = []
    for line in done.stdout.splitlines():
        if not line.strip():
            continue
        value = json.loads(line)
        if isinstance(value, str):  # `@json` wraps each item in a JSON string
            try:
                inner = json.loads(value)
                if isinstance(inner, (dict, list)):
                    value = inner
            except ValueError:
                pass
        out.append(value)
    return out


def fork_snapshot() -> dict:
    return {
        "start": utc(),
        "branches": sorted(gh_get(f"repos/{FORK}/branches?per_page=100", ".[].name|@json", paginate=True)),
    }


def classify_activity(issues: list, comments: list, branches_new: list, marker: str, start: str) -> dict:
    """Split fork changes into attributed (they carry the run marker) and unattributed."""
    attributed, unattributed = [], []

    def line(body: str) -> str:
        return (body or "").strip().splitlines()[0][:80] if (body or "").strip() else ""

    for item in issues:
        text = (item.get("title") or "") + "\n" + (item.get("body") or "")
        row = {
            "kind": "issue",
            "number": item.get("number"),
            "author": (item.get("user") or {}).get("login"),
            "created_at": item.get("created_at"),
            "new": (item.get("created_at") or "") >= start,
            "title": (item.get("title") or "")[:80],
        }
        (attributed if marker in text else unattributed).append(row)
    for item in comments:
        row = {
            "kind": "comment",
            "id": item.get("id"),
            "author": (item.get("user") or {}).get("login"),
            "created_at": item.get("created_at"),
            "first_line": line(item.get("body") or ""),
        }
        (attributed if marker in (item.get("body") or "") else unattributed).append(row)
    for name in branches_new:
        (attributed if "qev" in name else unattributed).append({"kind": "branch", "name": name})
    return {"attributed": attributed, "unattributed": unattributed}


def fork_after(before: dict, marker: str) -> dict:
    start = before["start"]
    issues = gh_get(f"repos/{FORK}/issues?state=all&since={start}&per_page=100", ".[]|@json", paginate=True)
    comments = gh_get(f"repos/{FORK}/issues/comments?since={start}&per_page=100", ".[]|@json", paginate=True)
    now_branches = gh_get(f"repos/{FORK}/branches?per_page=100", ".[].name|@json", paginate=True)
    new_branches = sorted(set(now_branches) - set(before["branches"]))
    return classify_activity(issues, comments, new_branches, marker, start)


# ----------------------------------------------------------------------- tmux


class Session:
    def __init__(self, name: str, launch: Path, log):
        self.name, self.launch, self.log = f"qev-{name}", launch, log

    def start(self) -> None:
        done = run(["tmux", "new-session", "-d", "-s", self.name, "-x", "200", "-y", "50", str(self.launch)])
        if done.returncode:
            raise RuntimeError("tmux new-session failed: " + done.stderr.strip()[:200])

    def screen(self) -> str:
        return run(["tmux", "capture-pane", "-p", "-t", self.name]).stdout

    def scrollback(self) -> str:
        return run(["tmux", "capture-pane", "-p", "-S", "-400", "-t", self.name]).stdout

    def keys(self, *keys: str) -> None:
        run(["tmux", "send-keys", "-t", self.name, *keys])

    def type_text(self, text: str) -> None:
        run(["tmux", "send-keys", "-t", self.name, "-l", text])

    def alive(self) -> bool:
        return run(["tmux", "has-session", "-t", self.name]).returncode == 0

    def kill(self) -> None:
        self.keys("C-c")
        nap(1)
        self.keys("C-c")
        nap(1)
        run(["tmux", "kill-session", "-t", self.name])


OPTION = re.compile(r"^\s*[❯>]?\s*(\d+)\.\s+(.+?)\s*$")


def question_options(screen: str) -> list[tuple[int, str]]:
    return [(int(m.group(1)), m.group(2)) for m in (OPTION.match(ln) for ln in screen.splitlines()) if m]


def is_question_screen(screen: str) -> bool:
    return "Enter to select" in screen and len(question_options(screen)) >= 2


def answer_keys(screen: str) -> list[str] | None:
    """Keys that select the 'keep my wording' option on a question screen, or None."""
    options = question_options(screen)
    for position, (_number, label) in enumerate(options):
        if ANSWER_LABEL in label.lower():
            return ["Down"] * position + ["Enter"]
    return None


def newest_clone_file(clone: Path, name: str) -> Path | None:
    files = sorted((clone / ".dev/issues").glob(f"*/{name}"), key=lambda p: p.stat().st_mtime)
    return files[-1] if files else None


def drive(session: Session, prompt: str, run_dir: Path, clone: Path, project_dir: Path, limit: int, log) -> dict:
    """Send the prompt, answer question screens, wait for the session to go idle."""
    out = {"questions_screens": 0, "answered": 0, "unanswered": 0, "permission_prompts": 0, "status": "timeout"}
    t0 = time.time()
    for _ in range(60):
        nap(1)
        screen = session.screen()
        if "trust" in screen.lower() and "Enter to confirm" in screen:
            session.keys("Enter")
            log("trust dialog accepted")
        if "❯" in screen and ("shortcuts" in screen or "manual mode" in screen):
            break
    else:
        out["status"] = "no-start"
        return out
    (run_dir / "screen-start.txt").write_text(session.screen(), encoding="utf-8")
    session.type_text(prompt)
    nap(1)
    session.keys("Enter")
    log("prompt sent")
    nap(4)
    if "esc to interrupt" not in session.screen() and prompt[:30] in session.screen():
        session.keys("Enter")
        log("prompt was still in the input box: Enter sent again")
    last_question_key = ""
    idle_since = None
    while time.time() - t0 < limit:
        nap(1)
        if STOP_FILE.exists():
            out["status"] = "stopped"
            log("STOP file appeared: ending the run")
            break
        screen = session.screen()
        if is_question_screen(screen):
            key = "\n".join(screen.splitlines()[-14:])
            if key != last_question_key:
                last_question_key = key
                out["questions_screens"] += 1
                n = out["questions_screens"]
                (run_dir / f"screen-question-{n}.txt").write_text(screen, encoding="utf-8")
                for name in ("issue-body.md", "draft-notes.md", "flags.md"):
                    src = newest_clone_file(clone, name)
                    if src:
                        shutil.copy2(src, run_dir / f"at-question-{n}-{name}")
                nap(2)
                keys = answer_keys(screen)
                if keys:
                    session.keys(*keys)
                    out["answered"] += 1
                    log(f"question screen {n}: sent {keys}")
                else:
                    out["unanswered"] += 1
                    session.keys("Escape")
                    log(f"question screen {n}: no '{ANSWER_LABEL}' option, Escape sent")
                nap(3)
            idle_since = None
            continue
        if re.search(r"Do you want to|\(y/n\)|Allow this", screen) and "esc to interrupt" not in screen:
            out["permission_prompts"] += 1
            (run_dir / f"screen-permission-{out['permission_prompts']}.txt").write_text(screen, encoding="utf-8")
            session.keys("Escape")
            log("a permission prompt appeared and was dismissed")
            nap(2)
            continue
        busy = "esc to interrupt" in screen
        transcripts = list(project_dir.rglob("*.jsonl")) if project_dir.exists() else []
        quiet = not transcripts or (time.time() - max(p.stat().st_mtime for p in transcripts) > 25)
        if not busy and quiet and time.time() - t0 > 30:
            idle_since = idle_since or time.time()
            if time.time() - idle_since > 25:
                out["status"] = "completed"
                break
        else:
            idle_since = None
    (run_dir / "screen-final.txt").write_text(session.scrollback(), encoding="utf-8")
    out["seconds"] = round(time.time() - t0)
    return out


# ------------------------------------------------------------------- transcripts


def read_transcripts(project_dir: Path) -> list[dict]:
    records = []
    for path in sorted(project_dir.rglob("*.jsonl")) if project_dir.exists() else []:
        for number, raw in enumerate(path.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
            try:
                rec = json.loads(raw)
            except ValueError:
                continue
            rec["_file"], rec["_line"] = str(path), number
            records.append(rec)
    return records


def blocks(rec: dict) -> list[dict]:
    content = (rec.get("message") or {}).get("content")
    return [b for b in content if isinstance(b, dict)] if isinstance(content, list) else []


def analyse_transcripts(records: list[dict]) -> dict:
    uses, results = [], {}
    base_dirs = []
    for rec in records:
        if rec.get("type") == "assistant":
            for b in blocks(rec):
                if b.get("type") == "tool_use":
                    uses.append({"name": b.get("name"), "id": b.get("id"), "input": b.get("input") or {}, "side": bool(rec.get("isSidechain")), "file": rec["_file"], "line": rec["_line"]})
        elif rec.get("type") == "user":
            for b in blocks(rec):
                if b.get("type") == "tool_result":
                    results[b.get("tool_use_id")] = json.dumps(b.get("content"))
                if b.get("type") == "text":
                    base_dirs += re.findall(r"Base directory for this skill: (\S+)", b.get("text") or "")
            raw = json.dumps((rec.get("message") or {}).get("content"))
            base_dirs += re.findall(r"Base directory for this skill: ([^\\\s]+)", raw)
    questions = [u for u in uses if u["name"] == "AskUserQuestion"]
    answered = [u for u in questions if "have been answered" in results.get(u["id"], "")]
    reads, writes, skills, agents, bash_paths = {}, [], [], [], set()
    for u in uses:
        inp = u["input"]
        if u["name"] == "Read" and inp.get("file_path"):
            failed = bool(re.search(r"EACCES|does not exist|ENOENT|permission denied", results.get(u["id"], ""), re.I))
            previous = reads.get(inp["file_path"])
            reads[inp["file_path"]] = ("Read tool", not failed or bool(previous and previous[1]))
        elif u["name"] in ("Write", "Edit") and inp.get("file_path"):
            writes.append(inp["file_path"])
        elif u["name"] == "Skill":
            skills.append(inp.get("skill"))
        elif u["name"] in ("Task", "Agent"):
            agents.append(inp.get("subagent_type"))
        elif u["name"] == "Bash":
            for p in re.findall(r"(/[\w./~@+-]*\.claude/[\w./~@+-]+)", inp.get("command", "")):
                bash_paths.add(p)
    for d in set(base_dirs):
        reads[d] = ("skill base directory", True)
    for p in bash_paths:
        reads.setdefault(p, ("Bash command text", True))
    main_texts = []
    for rec in records:
        if rec.get("type") == "assistant" and not rec.get("isSidechain"):
            for b in blocks(rec):
                if b.get("type") == "text" and (b.get("text") or "").strip():
                    main_texts.append(b["text"])
    return {
        "tool_uses": [u["name"] for u in uses],
        "questions": len(questions),
        "answered": len(answered),
        "question_texts": [json.dumps(u["input"])[:400] for u in questions],
        "answers": [results.get(u["id"], "")[:300] for u in questions],
        "reads": reads,
        "writes": writes,
        "skills": skills,
        "agents": agents,
        "final_text": main_texts[-1] if main_texts else "",
        "all_main_texts": main_texts,
    }


def read_files_report(analysis: dict) -> tuple[list[str], dict]:
    """One line per file the transcripts show was read, loaded or spawned, with its sha256."""
    lines, bad, installed, failed = [], [], [], []
    claude = HOME / ".claude"
    for path, (how, ok) in sorted(analysis["reads"].items()):
        p = Path(path.replace("~", str(HOME), 1)) if path.startswith("~") else Path(path)
        if str(p).startswith(str(REAL_HOME / ".claude")):
            installed.append(str(p))
            lines.append(f"INSTALLED-COPY {p} ({how})")
            continue
        if not ok:
            failed.append(str(p))
            lines.append(f"FAILED-READ {p} ({how}; the read returned an error, nothing was loaded from it)")
            continue
        if p.is_dir():
            lines.append(f"-  {p}  (directory; {how})")
            continue
        src = src_for_home_path(p) if str(p).startswith(str(claude)) else None
        clone_prefix = str(SCRATCH / "clones")
        if src is None and str(p).startswith(clone_prefix) and "/src/superclaude/" in str(p):
            src = src_root() / str(p).split("/src/superclaude/", 1)[1]  # the run clone holds HEAD's copy of src/
        digest = sha256(p)
        if src is not None:
            equal = digest != "-" and digest == sha256(src)
            if not equal:
                bad.append(str(p))
            lines.append(f"{digest}  {p}  src-equal={'yes' if equal else 'NO'}  ({how})")
        else:
            lines.append(f"{digest}  {p}  (not a skill, worker or command file; {how})")
    for name in sorted(set(a for a in analysis["agents"] if a)):
        p = claude / "agents" / f"{name}.md"
        lines.append(f"{sha256(p)}  {p}  agent spawned by name: {name}  src-equal={'yes' if sha256(p) == sha256(src_root() / 'agents' / (name + '.md')) else 'NO'}")
    for name in sorted(set(s for s in analysis["skills"] if s)):
        lines.append(f"skill loaded by name: {name}")
    return lines, {"not_equal_src": bad, "installed_copy": installed, "failed_reads": failed}


def gh_log_summary(run_dir: Path) -> dict:
    rows = []
    log = run_dir / "gh.log"
    if log.exists():
        rows = [json.loads(x) for x in log.read_text(encoding="utf-8").splitlines() if x.strip()]
    ops = [r.get("op", "") for r in rows if r["kind"] == "write"]
    creates = [r for r in rows if r.get("op") == "issue create"]
    return {
        "calls": len(rows),
        "issue_create": ops.count("issue create"),
        "issue_comment": ops.count("issue comment"),
        "issue_edit": ops.count("issue edit"),
        "field_writes": sum(1 for r in rows if r["kind"] == "write" and not r.get("op") and r.get("method") == "POST" and str(r.get("path", "")).endswith("/issue-field-values")),
        "other_writes": sum(
            1
            for r in rows
            if r["kind"] == "write"
            and r.get("op", "") not in ("issue create", "issue comment", "issue edit")
            and not (not r.get("op") and r.get("method") == "POST" and str(r.get("path", "")).endswith("/issue-field-values"))
        ),
        "unknown_calls": sum(1 for r in rows if r["kind"] == "unknown"),
        "start_up_reads": sum(1 for r in rows if r["kind"] == "start-up-read"),
        "protocol_reads": sum(1 for r in rows if r["kind"] == "protocol-read"),
        "creates": [{"title": c.get("title"), "labels": c.get("labels"), "type": c.get("type")} for c in creates],
    }


def notes_items(text: str, heading: str) -> list[str]:
    """Every non-empty line under the heading except None, with an optional leading dash removed."""
    out, on = [], False
    for ln in re.sub(r"<!--.*?-->", "", text, flags=re.S).splitlines():
        if ln.startswith("## "):
            on = ln[3:].strip() == heading
            continue
        item = re.sub(r"^[-*]\s+", "", ln.strip())
        if on and item and item != "None":
            if ln.startswith((" ", "\t")) and out:  # an indented line continues the item above it
                out[-1] += " | " + item
            else:
                out.append(item)
    return out


def own_issue_dirs(clone: Path) -> list[Path]:
    """The .dev/issues folders that the run itself created (not those tracked at the clone's HEAD)."""
    base = clone / ".dev/issues"
    if not base.exists():
        return []
    tracked = set(run(["git", "-C", str(clone), "ls-tree", "--name-only", "HEAD", ".dev/issues/"]).stdout.split())
    return [d for d in sorted(base.iterdir()) if d.is_dir() and f".dev/issues/{d.name}" not in tracked]


# --------------------------------------------------------------------- the run


def do_run(args: argparse.Namespace) -> int:
    reason = check_stop()
    if reason:
        print("matrix stopped, no run started:", reason)
        return 3
    SCRATCH.mkdir(parents=True, exist_ok=True)
    facts = seed_home()
    name = args.name
    run_dir = RUNS / name
    shutil.rmtree(run_dir, ignore_errors=True)
    run_dir.mkdir(parents=True)
    log_lines: list[str] = []

    def log(msg: str) -> None:
        log_lines.append(f"{utc()} {msg}")

    marker = f"qev-{name}-{time.strftime('%H%M%S', time.gmtime())}"
    clone = SCRATCH / "clones" / name
    head = make_clone(clone)
    trust_config(clone)
    project_dir = HOME / ".claude/projects" / re.sub(r"[^A-Za-z0-9]", "-", str(clone))
    shutil.rmtree(project_dir, ignore_errors=True)
    description = f"{args.description} [synthetic run marker: {marker}]"
    flags = " ".join(f"--{k} {v}" for k, v in (("mode", args.mode), ("type", args.type), ("depth", args.depth)) if v)
    prompt = f'/sc:issue --create "{description}" {flags}'
    (run_dir / "prompt.txt").write_text(prompt, encoding="utf-8")
    try:
        before = fork_snapshot()
    except Exception as err:  # the check cannot be shown: stop before any model call
        write_stop(f"fork-activity check unavailable: {err}", name)
        print("fork-activity snapshot failed; matrix stopped:", err)
        return 4
    launch = launch_script(run_dir, clone)
    shutil.copy2(launch, run_dir / "launch.sh.copy")
    session = Session(name, launch, log)
    try:
        session.start()
    except Exception as err:
        print("could not start the session:", err)
        return 5
    try:
        drove = drive(session, prompt, run_dir, clone, project_dir, TIMEOUTS[args.depth], log)
    finally:
        session.kill()
    records = read_transcripts(project_dir)
    for rec_file in sorted({r["_file"] for r in records}):
        dest = run_dir / "transcripts" / Path(rec_file).relative_to(project_dir)
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(rec_file, dest)
    activity_error = ""
    try:
        activity = fork_after(before, marker)
    except Exception as err:
        activity = {"attributed": [], "unattributed": []}
        activity_error = str(err)[:200]
    return finish(args, run_dir, clone, records, drove, activity, activity_error, marker, head, len(facts), log_lines)


def finish(args: argparse.Namespace, run_dir: Path, clone: Path, records: list[dict], drove: dict, activity: dict,
           activity_error: str, marker: str, head: str, nfacts: int, log_lines: list[str] | None) -> int:
    """Everything after the session: analyse transcripts and the fake gh log, write summary.json, apply the stop rules."""
    name, flags = args.name, " ".join(f"--{k} {v}" for k, v in (("mode", args.mode), ("type", args.type), ("depth", args.depth)) if v)
    analysis = analyse_transcripts(records)
    read_lines, read_facts = read_files_report(analysis)
    (run_dir / "read-files.txt").write_text("\n".join(read_lines) + "\n", encoding="utf-8")
    final_text = analysis["final_text"]
    (run_dir / "final-output.txt").write_text(final_text + "\n", encoding="utf-8")
    shutil.rmtree(run_dir / "dev-issues", ignore_errors=True)
    for own in own_issue_dirs(clone):
        shutil.copytree(own, run_dir / "dev-issues" / own.name)
    gh = gh_log_summary(run_dir)
    posted = sorted((run_dir / "gh-posted").glob("posted-issue-*.md")) if (run_dir / "gh-posted").exists() else []
    posted_body = posted[-1].read_text(encoding="utf-8") if posted else ""
    at_q = sorted(run_dir.glob("at-question-1-issue-body.md"))
    body_at_question = at_q[0].read_text(encoding="utf-8") if at_q else ""
    notes_file = next(iter(sorted((run_dir / "dev-issues").glob("*/draft-notes.md"))), None) if (run_dir / "dev-issues").exists() else None
    notes_text = notes_file.read_text(encoding="utf-8") if notes_file else ""
    additions = notes_items(notes_text, "New material")
    contradictions = notes_items(notes_text, "Contradictions")
    kept_lines = [ln.strip() for ln in final_text.splitlines() if re.sub(r"^[-*\s]+", "", ln).startswith("kept without approval:")]
    worker_lines = re.findall(r"Handled by (issue-worker-t\d)[^\n]*", notes_text)
    questions = analysis["questions"]
    summary = {
        "name": name,
        "depth": args.depth,
        "flags": flags,
        "marker": marker,
        "description": args.description,
        "clone_head": head,
        "drive": drove,
        "expected": {"questions": args.expect_questions, "issue_create": args.expect_create, "issue_comment": args.expect_comments},
        "observed": {
            "questions_as_tool_calls": questions,
            "questions_answered": analysis["answered"],
            "questions_as_plain_text": sum(
                1 for t in analysis["all_main_texts"] if "?" in t and re.search(r"keep my wording|keep the draft", t, re.I) and questions == 0
            ),
            "issue_create": gh["issue_create"],
            "issue_comment": gh["issue_comment"],
            "issue_edit": gh["issue_edit"],
            "other_writes": gh["other_writes"],
            "unknown_gh_calls": gh["unknown_calls"],
            "start_up_gh_reads": gh["start_up_reads"],
        },
        "matched": {
            "questions": questions == args.expect_questions,
            "issue_create": gh["issue_create"] == args.expect_create,
            "issue_comment": None if args.expect_comments is None else gh["issue_comment"] == args.expect_comments,
        },
        "creates": gh["creates"],
        "worker_lines": worker_lines,
        "agents_spawned": analysis["agents"],
        "skills_loaded": analysis["skills"],
        "question_texts": analysis["question_texts"],
        "question_answers": analysis["answers"],
        "additions": additions,
        "contradictions": contradictions,
        "additions_in_posted_body": [a for a in additions if a[:40] in posted_body],
        "kept_without_approval_lines": kept_lines,
        "false_files_in_body_at_question": [f for f in FALSE_FILES if f in body_at_question],
        "false_files_in_posted_body": [f for f in FALSE_FILES if f in posted_body],
        "read_files": {"count": len(read_lines), **read_facts},
        "seeded_hashes_equal_src": nfacts,
        "fork_activity": {**activity, "error": activity_error},
        "files_written_by_run": analysis["writes"][:50],
    }
    stop = []
    if gh["unknown_calls"]:
        stop.append(f"{gh['unknown_calls']} unknown gh call(s)")
    if read_facts["installed_copy"]:
        stop.append("a run read an installed copy of the skill or workers")
    if activity["attributed"]:
        stop.append("attributed fork activity: " + json.dumps(activity["attributed"])[:300])
    if activity_error:
        stop.append("fork-activity check failed after the run: " + activity_error)
    if gh["other_writes"]:
        stop.append(f"{gh['other_writes']} write call(s) of a kind the matrix does not expect (logged, not forwarded)")
    if activity["unattributed"] and not activity["attributed"]:
        PENDING_FILE.write_text(json.dumps({"run": name, "unattributed": activity["unattributed"]}), encoding="utf-8")
    summary["stop_conditions"] = stop
    (run_dir / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    if log_lines is not None:
        (run_dir / "driver.log").write_text("\n".join(log_lines) + "\n", encoding="utf-8")
    if stop:
        write_stop("; ".join(stop), name)
        print("STOP condition met in this run:", "; ".join(stop))
        return 4
    print(f"run {name}: questions={questions} (expected {args.expect_questions}), issue create={gh['issue_create']}, "
          f"issue comment={gh['issue_comment']}, drive={drove['status']}")
    return 0



def reanalyse(args: argparse.Namespace) -> int:
    """Re-derive summary.json from the transcripts, fake gh log and draft files saved by an earlier run."""
    run_dir = RUNS / args.name
    old = json.loads((run_dir / "summary.json").read_text(encoding="utf-8")) if (run_dir / "summary.json").exists() else {}
    prompt = (run_dir / "prompt.txt").read_text(encoding="utf-8")
    marker = old.get("marker") or re.search(r"qev-[A-Za-z0-9-]+", prompt).group(0)
    records = read_transcripts(run_dir / "transcripts")
    seeded = len(load_list())
    flags = old.get("flags", "")

    def flag(key: str) -> str | None:
        found = re.search(rf"--{key} (\S+)", flags)
        return found.group(1) if found else None

    expected = old.get("expected") or {}
    saved = argparse.Namespace(  # the saved run's own values, never the command line's
        name=args.name,
        depth=old.get("depth") or flag("depth") or args.depth,
        description=old.get("description", args.description),
        mode=flag("mode"),
        type=flag("type"),
        expect_questions=expected.get("questions", args.expect_questions),
        expect_create=expected.get("issue_create", args.expect_create),
        expect_comments=expected.get("issue_comment", args.expect_comments),
    )
    return finish(
        saved,
        run_dir,
        SCRATCH / "clones" / args.name,
        records,
        old.get("drive") or {"status": "unknown"},
        old.get("fork_activity") and {k: old["fork_activity"].get(k, []) for k in ("attributed", "unattributed")} or {"attributed": [], "unattributed": []},
        (old.get("fork_activity") or {}).get("error", ""),
        marker,
        old.get("clone_head", ""),
        seeded,
        None,
    )


# -------------------------------------------------------------------- self-test


def self_test() -> int:
    """Run the checks against sandbox copies of the stop and pending files, never the matrix's own."""
    global STOP_FILE, PENDING_FILE, RUNS
    saved = (STOP_FILE, PENDING_FILE, RUNS)
    real = {p: (p.read_bytes() if p.exists() else None) for p in (STOP_FILE, PENDING_FILE)}
    sandbox = SCRATCH / "self-test"
    STOP_FILE, PENDING_FILE, RUNS = sandbox / "STOP", sandbox / "PENDING-REVIEW", sandbox / "runs"
    try:
        status = _self_test_checks()
    finally:
        STOP_FILE, PENDING_FILE, RUNS = saved
    untouched = all((p.read_bytes() if p.exists() else None) == content for p, content in real.items())
    print(f"{'PASS' if untouched else 'FAIL'}  the matrix's own STOP and PENDING-REVIEW files were left untouched")
    status = status if untouched else 1
    print("self-test:", "PASS" if status == 0 else "FAIL")
    return status


def _self_test_checks() -> int:
    ok = True

    def check(label: str, cond: bool, detail: str = "") -> None:
        nonlocal ok
        ok = ok and cond
        print(f"{'PASS' if cond else 'FAIL'}  {label}" + (f"  [{detail}]" if detail else ""))

    root = SCRATCH / "self-test"
    shutil.rmtree(root, ignore_errors=True)
    root.mkdir(parents=True)
    guarded = [
        src_root() / "skills/sc-issue-protocol",
        REAL_HOME / ".claude/skills/sc-issue-protocol",
        REAL_HOME / ".claude/commands/sc",
        REAL_HOME / ".claude/agents",
    ]

    def tree_hash() -> str:
        h = hashlib.sha256()
        for base in guarded:
            for p in sorted(base.rglob("*")) if base.exists() else []:
                if p.is_file() and "__pycache__" not in p.parts:
                    h.update(str(p).encode() + sha256(p).encode())
        return h.hexdigest()

    before_tree = tree_hash()
    facts = seed_home()
    check("seeded home equals src for every file of the load list", len(facts) >= 25, f"{len(facts)} files")
    create_ref = "skills/sc-issue-protocol/refs/create.md"
    installed = sha256(REAL_HOME / ".claude" / create_ref)
    check(
        "the seeded refs/create.md equals src and differs from the installed user copy",
        facts[create_ref] == sha256(src_root() / create_ref) and facts[create_ref] != installed,
        f"src {facts[create_ref][:12]} installed {installed[:12]}",
    )
    print("note  this hash list is the expectation; the proof for a real run is its own read-files.txt")

    # fake gh
    gh_dir = root / "gh"
    env = {**run_env(gh_dir), "FAKE_GH_LOG": str(root / "gh.log"), "FAKE_GH_STATE": str(root / "state.json"), "FAKE_GH_DIR": str(root / "posted")}
    body = root / "body.md"
    body.write_text("synthetic body", encoding="utf-8")
    field = root / "field.json"
    field.write_text(json.dumps({"issue_field_values": [{"field_id": 7001, "value": "Simple"}]}), encoding="utf-8")

    def gh(*argv: str) -> subprocess.CompletedProcess:
        return run([sys.executable, str(BIN / "gh"), *argv], env={"PATH": "/usr/bin:/bin", **env})

    created = gh("issue", "create", "--repo", FORK, "--title", "[FEATURE] x", "--body-file", str(body), "--label", "enhancement", "--type", "Feature")
    number = created.stdout.strip().rsplit("/", 1)[-1]
    calls = [
        ("issue create", created),
        ("issue comment", gh("issue", "comment", number, "--repo", FORK, "--body-file", str(body))),
        ("api -X POST", gh("api", "-X", "POST", f"repos/{FORK}/issues/{number}/issue-field-values", "--input", str(field))),
        ("issue edit", gh("issue", "edit", number, "--repo", FORK, "--add-assignee", "@me")),
    ]
    rows = [json.loads(x) for x in (root / "gh.log").read_text().splitlines()]
    for label, done in calls:
        check(f"fake gh: `{label}` exits 0 and is logged as a write", done.returncode == 0 and any(r["kind"] == "write" for r in rows))
    check("fake gh: four writes are in the log and none was forwarded", sum(r["kind"] == "write" for r in rows) == 4 and int(number) >= 990001, f"fake issue number {number}")
    src_text = (HERE / "fake_gh.py").read_text(encoding="utf-8")
    check("fake gh: imports no subprocess, socket, urllib or http", not re.search(r"^\s*(import|from)\s+(subprocess|socket|urllib|http|requests)", src_text, re.M))
    check("fake gh: reads back the stored issue type and field", gh("issue", "view", number, "--repo", FORK, "--json", "issueType", "--jq", ".issueType.name").stdout.strip() == "Feature" and "Simple" in gh("api", f"repos/{FORK}/issues/{number}/issue-field-values").stdout)
    unknown = gh("repo", "delete", FORK)
    check("fake gh: an unknown call exits non-zero and is logged as unknown", unknown.returncode != 0 and json.loads((root / "gh.log").read_text().splitlines()[-1])["kind"] == "unknown", f"exit {unknown.returncode}")
    other = gh("issue", "list", "--repo", "someone/else", "--json", "number")
    check("fake gh: a read of another repository is unknown", other.returncode != 0)
    startup_a, startup_b = gh("auth", "token"), gh("issue", "list", "-R", "anthropics/claude-code", "--author", "@me", "--state", "closed", "--json", "number")
    kinds = [json.loads(x)["kind"] for x in (root / "gh.log").read_text().splitlines()[-2:]]
    check("fake gh: the two start-up reads are known and logged as start-up reads", kinds == ["start-up-read", "start-up-read"] and startup_b.returncode == 0 and startup_a.returncode != 0)

    # the prepared run environment
    renv = run_env(root / "run")
    forbidden = [k for k in ("GH_TOKEN", "GITHUB_TOKEN", "SSH_AUTH_SOCK", "GIT_ASKPASS") if k in renv]
    check("run environment has no GH_TOKEN, GITHUB_TOKEN, SSH_AUTH_SOCK or GIT_ASKPASS", not forbidden)
    check("run environment: fake gh first on PATH, empty gh config, git config pointed at /dev/null", renv["PATH"].startswith(str(BIN)) and renv["GIT_CONFIG_GLOBAL"] == "/dev/null" and renv["GIT_CONFIG_NOSYSTEM"] == "1")
    launch = launch_script(root / "run", root / "clone")
    launch_text = launch.read_text(encoding="utf-8")
    check("launch.sh passes gateway variables by reference only", all(f'{k}="${k}"' in launch_text for k in PASS_ENV) and "sk-" not in launch_text)
    clone = root / "clone"
    make_clone(clone)
    helper = run(["git", "-C", str(clone), "config", "--get-all", "credential.helper"], env={"PATH": "/usr/bin:/bin", "HOME": str(HOME), "GIT_CONFIG_GLOBAL": "/dev/null", "GIT_CONFIG_NOSYSTEM": "1"})
    check("run clone has no credential helper", helper.stdout.strip() == "")
    push = run(["git", "-C", str(clone), "push", "origin", "HEAD"], env={"PATH": "/usr/bin:/bin", "HOME": str(HOME), "GIT_CONFIG_GLOBAL": "/dev/null", "GIT_CONFIG_NOSYSTEM": "1", "GIT_TERMINAL_PROMPT": "0"}, timeout=60)
    remotes = run(["git", "-C", str(clone), "remote", "-v"]).stdout
    check("git push from the run clone fails", push.returncode != 0 and INVALID_PUSH_URL in remotes and f"https://github.com/{FORK} (fetch)" in remotes, push.stderr.strip().splitlines()[-1][:80] if push.stderr.strip() else "")
    check("run clone: project .claude folder removed, origin fetch URL is the GitHub form", not (clone / ".claude").exists())

    # the secret scan
    scan = HERE / "scan_secrets.py"
    clean = root / "scan-clean"
    clean.mkdir()
    (clean / "a.txt").write_text("nothing secret here, only the word password in prose\n", encoding="utf-8")
    dirty = root / "scan-dirty"
    dirty.mkdir()
    (dirty / "a.txt").write_text("token ghp_" + "a1B2c3D4e5F6g7H8i9J0k1L2m3N4o5P6q7R8" + "\n", encoding="utf-8")
    (dirty / "b.txt").write_text("[REDACTED:private-key-header]\npassword=hunter2hunter2\n", encoding="utf-8")
    found, passed = run([sys.executable, str(scan), str(dirty)]), run([sys.executable, str(scan), str(clean)])
    check("secret scan finds the planted synthetic token, key header and password and passes a clean folder", found.returncode == 1 and "github-token" in found.stdout and "private-key-header" in found.stdout and "password-assignment" in found.stdout and passed.returncode == 0)
    check("secret scan never prints a found value", "ghp_a1B2" not in found.stdout and "hunter2" not in found.stdout)

    # the stop file
    write_stop("self-test stop", "self-test")
    args = argparse.Namespace(name="self-test-second", depth="quick", description="x", mode=None, type=None, expect_questions=0, expect_create=1, expect_comments=None)
    second = do_run(args)
    stopped_dir = RUNS / "self-test-second"
    check("the stop file stops a second run before anything starts", second == 3 and not stopped_dir.exists())
    STOP_FILE.unlink()

    # fork-activity attribution, with canned data (no network)
    sample = classify_activity(
        [{"number": 1, "title": "mine qev-x", "body": "", "created_at": "2026-11-26T10:00:01Z", "user": {"login": "u"}}, {"number": 2, "title": "other session", "body": "", "created_at": "2026-11-26T10:00:02Z", "user": {"login": "u"}}],
        [{"id": 5, "body": "unrelated comment", "created_at": "t", "user": {"login": "u"}}],
        ["qev-branch", "feature/other"],
        "qev-x",
        "2026-11-26T10:00:00Z",
    )
    check("fork-activity attribution: marker hits are attributed, the rest listed as unattributed", len(sample["attributed"]) == 2 and len(sample["unattributed"]) == 3)
    PENDING_FILE.write_text("{}", encoding="utf-8")
    check("a PENDING-REVIEW file holds the next run until it is cleared", check_stop() is not None)
    PENDING_FILE.unlink()
    check("no STOP or PENDING-REVIEW file is left behind by the self-test", check_stop() is None)

    # the guarded folders are untouched
    check("no file under src/ skill folders or the user's installed skill, worker and command folders changed", tree_hash() == before_tree)
    return 0 if ok else 1


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--self-test", action="store_true")
    sub = parser.add_subparsers(dest="cmd")
    sub.add_parser("seed")
    sub.add_parser("check-stop")
    clear = sub.add_parser("clear-pending")
    clear.add_argument("--note", required=True)
    r = sub.add_parser("run")
    r.add_argument("--name", required=True)
    r.add_argument("--depth", choices=sorted(TIMEOUTS), required=True)
    r.add_argument("--description", required=True)
    r.add_argument("--mode", choices=["feature", "bug"])
    r.add_argument("--type")
    r.add_argument("--expect-questions", type=int, required=True)
    r.add_argument("--expect-create", type=int, required=True)
    r.add_argument("--expect-comments", type=int)
    r.add_argument("--reanalyse", action="store_true", help="re-derive summary.json from the saved raw data; no session, no network")
    args = parser.parse_args(argv)
    if args.self_test:
        return self_test()
    if args.cmd == "seed":
        print(json.dumps({"seeded": len(seed_home())}))
        return 0
    if args.cmd == "check-stop":
        reason = check_stop()
        print(reason or "no stop")
        return 3 if reason else 0
    if args.cmd == "clear-pending":
        if PENDING_FILE.exists():
            (SCRATCH / "pending-cleared.log").open("a").write(f"{utc()} {args.note}\n{PENDING_FILE.read_text()}\n")
            PENDING_FILE.unlink()
        return 0
    if args.cmd == "run":
        return reanalyse(args) if args.reanalyse else do_run(args)
    parser.print_help()
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

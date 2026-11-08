"""Observation runner for the B-CTX observation plan (stdlib only).

Run it as: uv run --no-project python -I artifacts/observe/observe.py <command>
Commands: baseline, preflight, selfcheck, check-baseline, teardown NAME, hook-observe.
Other scripts import it and use Group and Runner.

It stores only identities, field names, hashes, selector results, exit codes
and counts. Credentials, environment values, command text and process
arguments are never written: callers pass a redacted label for every case.
"""

import sys

sys.dont_write_bytecode = True

import argparse  # noqa: E402
import hashlib  # noqa: E402
import json  # noqa: E402
import os  # noqa: E402
import re  # noqa: E402
import shlex  # noqa: E402
import shutil  # noqa: E402
import signal  # noqa: E402
import subprocess  # noqa: E402
import tempfile  # noqa: E402
import time  # noqa: E402
import uuid  # noqa: E402
from pathlib import Path  # noqa: E402

HERE = Path(__file__).resolve().parent
ART = HERE.parent
PKG = ART.parent
REPO = PKG.parents[3]
HELPER = REPO / "src/superclaude/hooks/scripts/launch-job-identity.sh"
LEDGER = ART / "run-status.jsonl"
CLEANUP = ART / "phase2-cleanup.log"
BASELINE = ART / "baseline.json"
PREFLIGHT = ART / "preflight.json"
GROUPS = ART / "groups"
REAL_HOME = os.environ.get("HOME", "")
CAP = 12  # most real Claude runs the whole plan may start
NESTED = "cannot be launched inside another Claude Code session"
AUTH_WORDS = ("not logged in", "invalid api key", "authentication")
ID = re.compile(r"[A-Za-z0-9][A-Za-z0-9_-]{0,127}\Z")
BLOCKED_PKG = REPO / ".dev/tasks/to-do/TASK-WF-implementDocsDes-20261106-210206"
DONE_PKG = REPO / ".dev/tasks/done/TASK-WF-authorizedNarrow-20261106-214325"


class Refused(Exception):
    """The runner refused to start a run (for example a thirteenth real Claude run)."""


def now():
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def sha(data):
    if isinstance(data, str):
        data = data.encode()
    return hashlib.sha256(data).hexdigest()


def append(path, obj):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fd = os.open(path, os.O_WRONLY | os.O_APPEND | os.O_CREAT, 0o600)
    try:
        os.write(fd, (json.dumps(obj, sort_keys=True) + "\n").encode())
        os.fsync(fd)
    finally:
        os.close(fd)


def cleanup_log(text):
    path = CLEANUP
    path.parent.mkdir(parents=True, exist_ok=True)
    fd = os.open(path, os.O_WRONLY | os.O_APPEND | os.O_CREAT, 0o600)
    try:
        os.write(fd, (now() + " " + text + "\n").encode())
    finally:
        os.close(fd)


def proc_fields(pid):
    try:
        raw = Path("/proc/%d/stat" % pid).read_text()
        f = raw.rsplit(")", 1)[1].split()
        return {"state": f[0], "ppid": int(f[1]), "sid": int(f[3]), "start": int(f[19])}
    except (OSError, IndexError, ValueError):
        return None


def proc_start(pid):
    f = proc_fields(pid)
    return f["start"] if f else None


def alive(pid, start):
    f = proc_fields(pid)
    return bool(f and f["state"] != "Z" and f["start"] == start)


def boot_id():
    return Path("/proc/sys/kernel/random/boot_id").read_text().strip()


def real_settings_sha():
    path = Path(REAL_HOME) / ".claude" / "settings.json"
    try:
        return sha(path.read_bytes())
    except OSError:
        return "absent"


def identities(value):
    """Keep only selector results, never arbitrary tool output or stream text."""
    found = []
    if isinstance(value, dict):
        if value.get("status") in ("governed", "ordinary", "unknown"):
            item = {"status": value["status"]}
            sid = value.get("session_id")
            if isinstance(sid, str) and ID.fullmatch(sid):
                item["session_id"] = sid
            if value.get("reason") == "released":
                item["reason"] = "released"
            found.append(item)
        else:
            for item in value.values():
                found.extend(identities(item))
    elif isinstance(value, list):
        for item in value:
            found.extend(identities(item))
    elif isinstance(value, str):
        for line in value.splitlines():
            try:
                parsed = json.loads(line)
            except ValueError:
                continue
            if isinstance(parsed, (dict, list)):
                found.extend(identities(parsed))
    return found


def stop(pid, start, why, case, group):
    """Stop one process by id, only while its start ticks still match."""
    if not alive(pid, start):
        cleanup_log("group=%s case=%s pid=%d start=%d why=%s result=already-gone-or-identity-changed" % (group, case, pid, start, why))
        return False
    try:
        os.kill(pid, signal.SIGTERM)
    except ProcessLookupError:
        return False
    until = time.monotonic() + 3
    while alive(pid, start) and time.monotonic() < until:
        time.sleep(0.03)
    result = "sigterm"
    if alive(pid, start):
        try:
            os.kill(pid, signal.SIGKILL)
        except ProcessLookupError:
            pass
        until = time.monotonic() + 3
        while alive(pid, start) and time.monotonic() < until:
            time.sleep(0.03)
        result = "sigkill"
    cleanup_log("group=%s case=%s pid=%d start=%d why=%s result=stopped-by-%s gone=%s" % (group, case, pid, start, why, result, not alive(pid, start)))
    return not alive(pid, start)


class ManagedProc:
    """A child started by the runner, signalled only through its own handle."""

    def __init__(self, popen, name, group):
        self.p = popen
        self.pid = popen.pid
        self.name = name
        self.start = proc_start(self.pid)
        self.boot = boot_id()
        self.out = group.tmp / ("out-%s.txt" % name)
        self.err = group.tmp / ("err-%s.txt" % name)

    def signal(self, sig, recorded_start=None):
        want = self.start if recorded_start is None else recorded_start
        cur = proc_start(self.pid)
        if cur is None or cur != want or boot_id() != self.boot:
            return {"sent": False, "reason": "process id, start ticks or boot identity no longer match"}
        self.p.send_signal(sig)
        return {"sent": True}

    def kill_group(self):
        try:
            os.killpg(self.pid, signal.SIGKILL)
        except (ProcessLookupError, PermissionError):
            pass


class Group:
    """One run group: disposable HOME, fixture repository and temporary directory."""

    def __init__(self, name, root):
        # The registry file is data: only a directory this runner made (mkdtemp, directly under
        # the temporary directory, named for this group, not a symlink) may ever be torn down.
        root = Path(root)
        if not ID.fullmatch(name or "") or root.parent != Path(tempfile.gettempdir()) \
                or not root.name.startswith("observe-%s-" % name) or root.is_symlink():
            raise SystemExit("refusing group %r: its root is not a directory this runner created" % (name,))
        self.name = name
        self.root = root
        self.home = self.root / "home"
        self.fixture = self.root / "fixture"
        self.tmp = self.root / "tmp"
        self.reg = GROUPS / (name + ".json")

    @classmethod
    def create(cls, name):
        GROUPS.mkdir(parents=True, exist_ok=True)
        if (GROUPS / (name + ".json")).exists():
            raise SystemExit("group %s already exists" % name)
        root = Path(tempfile.mkdtemp(prefix="observe-%s-" % name))
        root.chmod(0o700)
        g = cls(name, root)
        g.home.mkdir(mode=0o700)
        (g.home / ".claude").mkdir(mode=0o700)
        g.tmp.mkdir(mode=0o700)
        g.fixture.mkdir(mode=0o700)
        subprocess.run(["git", "init", "-q", str(g.fixture)], env=g.git_env(), check=True)
        g.save({"root": str(root), "survivors": [], "state": "active", "created": now()})
        return g

    @classmethod
    def load(cls, name):
        data = json.loads((GROUPS / (name + ".json")).read_text())
        return cls(name, data["root"])

    def data(self):
        return json.loads(self.reg.read_text())

    def save(self, data):
        tmp = self.reg.with_suffix(".tmp")
        tmp.write_text(json.dumps(data, sort_keys=True))
        os.replace(tmp, self.reg)

    def env(self):
        # CLAUDECODE and existing auth variables stay intact: never evade a nested guard.
        return dict(
            os.environ,
            HOME=str(self.home),
            CLAUDE_CONFIG_DIR=str(self.home / ".claude"),
            XDG_CONFIG_HOME=str(self.home / ".config"),
            XDG_CACHE_HOME=str(self.home / ".cache"),
            UV_PYTHON=sys.executable,
            UV_PYTHON_DOWNLOADS="never",
            PYTHONDONTWRITEBYTECODE="1",
        )

    def git_env(self):
        env = {k: v for k, v in self.env().items() if not k.startswith("GIT_")}
        env.update(GIT_CONFIG_NOSYSTEM="1", GIT_CONFIG_GLOBAL="/dev/null")
        return env

    def store_dir(self):
        return self.home / ".claude/state/launch-level"

    def make_governed(self, sid, level="worktree"):
        store = self.store_dir()
        (store / "sessions").mkdir(parents=True, exist_ok=True)
        for d in (self.home / ".claude/state", store, store / "sessions"):
            d.chmod(0o700)
        rec = store / "sessions" / sid
        rec.write_text(level + "\n")
        rec.chmod(0o600)
        return rec

    def store_check(self, sid=None):
        out = {"store_exists": self.store_dir().is_dir()}
        if sid:
            out["governed_record_exists"] = (self.store_dir() / "sessions" / sid).is_file()
        return out

    def spawn(self, argv, name, *, env=None, cwd=None):
        out = open(self.tmp / ("out-%s.txt" % name), "wb")
        err = open(self.tmp / ("err-%s.txt" % name), "wb")
        try:
            p = subprocess.Popen(
                argv, env=env or self.env(), cwd=cwd or self.fixture,
                stdout=out, stderr=err, stdin=subprocess.DEVNULL, start_new_session=True,
            )
        finally:
            out.close()
            err.close()
        return ManagedProc(p, name, self)

    def procs_under(self):
        """Live processes whose working directory is under the fixture or the temporary directory."""
        roots = (str(self.fixture), str(self.tmp))
        found = set()
        for name in os.listdir("/proc"):
            if not name.isdecimal() or int(name) == os.getpid():
                continue
            try:
                cwd = os.readlink("/proc/%s/cwd" % name)
            except OSError:
                continue
            if any(cwd == r or cwd.startswith(r + os.sep) for r in roots):
                f = proc_fields(int(name))
                if f and f["state"] != "Z":
                    found.add((int(name), f["start"]))
        return found

    def register_survivor(self, label, pid, supervisor=None):
        entry = {"label": label, "pid": pid, "start": proc_start(pid), "boot": boot_id()}
        if supervisor:
            entry["supervisor"] = {"pid": supervisor, "start": proc_start(supervisor)}
        data = self.data()
        data["survivors"].append(entry)
        self.save(data)
        return entry

    def survivor_keys(self):
        keys = set()
        for s in self.data()["survivors"]:
            keys.add((s["pid"], s["start"]))
            if s.get("supervisor"):
                keys.add((s["supervisor"]["pid"], s["supervisor"]["start"]))
        return keys

    def sweep(self, before, case):
        """Case-timeout sweep: stop only processes this case started; never a registered survivor."""
        keep = set(before) | self.survivor_keys()
        stopped = 0
        for pid, start in sorted(self.procs_under() - keep):
            if stop(pid, start, "case-timeout-sweep", case, self.name):
                stopped += 1
        return stopped

    def teardown(self, case="teardown"):
        """Explicit group teardown: stop survivors (identity checked), sweep, remove the directories."""
        data = self.data()
        for s in data["survivors"]:
            stop(s["pid"], s["start"], "survivor-teardown", case, self.name)
            if s.get("supervisor"):
                stop(s["supervisor"]["pid"], s["supervisor"]["start"], "supervisor-teardown", case, self.name)
        for pid, start in sorted(self.procs_under()):
            stop(pid, start, "teardown-sweep", case, self.name)
        left = len(self.procs_under())
        existed = self.root.exists()
        if existed:
            shutil.rmtree(self.root)
        cleanup_log("group=%s case=%s teardown leftover_processes=%d directory_removed=%s" % (self.name, case, left, not self.root.exists()))
        data["state"] = "torn-down"
        self.save(data)
        return {"leftover_processes": left, "directory_removed": existed and not self.root.exists()}


class Runner:
    def __init__(self, ledger=LEDGER, cap=CAP):
        self.ledger = Path(ledger)
        self.cap = cap

    def real_count(self):
        n = 0
        if self.ledger.exists():
            for line in self.ledger.read_text().splitlines():
                try:
                    if json.loads(line).get("real_claude") is True:
                        n += 1
                except ValueError:
                    pass
        return n

    def log(self, **fields):
        fields.setdefault("ts", now())
        append(self.ledger, fields)

    def run(self, group, case_id, argv, *, label, timeout, real_claude=False, env=None, cwd=None,
            ready=None, signal_name=None, signal_start=None, ok_result="controlled", depth=None,
            extra=None, classify=None, rid=None, sid=None):
        rid = rid or uuid.uuid4().hex[:12]
        extra = dict(extra or {})
        if real_claude and self.real_count() >= self.cap:
            self.log(run_id=rid, case_id=case_id, label="refused: run over the cap of %d real Claude runs" % self.cap,
                     group=group.name, real_claude=False, result="blocked")
            raise Refused("refusing to start real Claude run number %d" % (self.cap + 1))
        extra["store_check"] = group.store_check(sid)
        before = group.procs_under()
        settings_before = real_settings_sha() if real_claude else None
        t0 = time.time()
        started = now()
        mp = group.spawn(argv, "%s-%s" % (case_id, rid), env=env, cwd=cwd)
        (group.tmp / ("claude-%s.pid" % rid)).write_text(str(mp.pid))
        sig = None
        timed_out = False
        while True:
            rc = mp.p.poll()
            if rc is not None:
                break
            if ready and sig is None and Path(ready).exists():
                res = mp.signal(getattr(signal, signal_name), signal_start)
                sig = {"signal": signal_name, "target": "the spawned process only (own child handle, no process group)",
                       "sent": res["sent"], "at_s": round(time.time() - t0, 2)}
                if not res["sent"]:
                    sig["refused_reason"] = res["reason"]
            if time.time() - t0 > timeout:
                timed_out = True
                break
            time.sleep(0.05)
        if timed_out:
            mp.kill_group()
        try:
            rc = mp.p.wait(timeout=5)
        except subprocess.TimeoutExpired:
            mp.kill_group()
            rc = mp.p.wait(timeout=5)
        # Per-case cleanup touches only the case's own process group; jobs marked
        # surviving, and their supervisors, live in other sessions and are never signalled.
        mp.kill_group()
        swept = group.sweep(before, case_id) if timed_out else 0
        end = now()
        exit_ = ("signal:" + signal.Signals(-rc).name) if rc < 0 else rc
        more = {}
        if timed_out:
            result = "blocked"
        elif classify:
            result, more = classify(rc, mp)
        else:
            result = ok_result if (rc == 0 or (sig and sig["sent"])) else "blocked"
        extra.update(more)
        entry = dict(run_id=rid, case_id=case_id, label=label, group=group.name, start=started, end=end,
                     exit=exit_, real_claude=bool(real_claude), depth=depth, result=result,
                     held_s=round(time.time() - t0, 2), timed_out=timed_out, swept=swept, extra=extra)
        if sig:
            entry["signal"] = sig
        if real_claude:
            entry["settings_sha256_before"] = settings_before
            entry["settings_sha256_after"] = real_settings_sha()
        self.log(**entry)
        return {"rid": rid, "exit": exit_, "rc": rc, "result": result, "mp": mp, "timed_out": timed_out,
                "signal": sig, "held_s": entry["held_s"], "out": mp.out, "err": mp.err, "extra": extra}


# ---------------------------------------------------------------- real Claude helpers

def claude_bin():
    return shutil.which("claude")


def write_settings(group, variant, log):
    observer = shlex.join(["uv", "run", "--no-project", "python", "-I", str(HERE / "observe.py"), "hook-observe",
                           "--runner", str(HELPER), "--log", str(log), "--variant", variant, "--cwd", str(group.fixture)])
    hook = [{"matcher": "Bash", "hooks": [{"type": "command", "command": observer, "timeout": 10}]}]
    path = group.tmp / ("settings-%s.json" % variant)
    path.write_text(json.dumps({"enabledPlugins": {}, "hooks": {"PreToolUse": hook, "PostToolUse": hook}}))
    return path


def claude_argv(cli, settings, sid, prompt, *, tools=("Bash",), persist=False, resume=None, fork=False):
    names = ",".join(tools)
    argv = [cli, "--print", "--setting-sources", "", "--settings", str(settings)]
    if resume:
        argv += ["--resume", resume] + (["--fork-session"] if fork else [])
    else:
        argv += ["--session-id", sid]
    argv += ["--tools", names, "--allowedTools", names, "--permission-mode", "dontAsk", "--strict-mcp-config",
             "--mcp-config", '{"mcpServers":{}}', "--max-budget-usd", "0.25", "--output-format", "stream-json",
             "--include-hook-events", "--verbose"]
    if not persist:
        argv.append("--no-session-persistence")
    argv += ["--disable-slash-commands", "--no-chrome", prompt]
    return argv


def parse_stream(path):
    """Event types and selector results only, never message text."""
    events, init = [], {}
    try:
        lines = Path(path).read_text(errors="replace").splitlines()
    except OSError:
        return events, init
    for line in lines:
        try:
            ev = json.loads(line)
        except ValueError:
            continue
        if not isinstance(ev, dict):
            continue
        item = {"type": ev.get("type"), "subtype": ev.get("subtype")}
        if isinstance(ev.get("session_id"), str) and ID.fullmatch(ev["session_id"]):
            item["session_id"] = ev["session_id"]
        sel = identities(ev.get("message", {}))
        if sel:
            item["selector_results"] = sel
        events.append(item)
        if ev.get("type") == "system" and ev.get("subtype") == "init" and not init:
            init = {"version": ev.get("claude_code_version"), "tools": ev.get("tools"), "session_id": item.get("session_id")}
    return events, init


def failure_facts(path):
    """Category words and numbers only from a failed run's stream, never message text."""
    facts = {}
    try:
        lines = Path(path).read_text(errors="replace").splitlines()
    except OSError:
        return facts
    for line in lines:
        try:
            ev = json.loads(line)
        except ValueError:
            continue
        if not isinstance(ev, dict):
            continue
        if ev.get("type") == "assistant" and isinstance(ev.get("error"), str) and re.fullmatch(r"[a-z_]{1,40}", ev["error"]):
            facts["assistant_error_category"] = ev["error"]
        if ev.get("type") == "result":
            if isinstance(ev.get("subtype"), str) and re.fullmatch(r"[a-z_]{1,40}", ev["subtype"]):
                facts["result_subtype"] = ev["subtype"]
            if isinstance(ev.get("is_error"), bool):
                facts["result_is_error"] = ev["is_error"]
            if isinstance(ev.get("api_error_status"), int):
                facts["api_error_status"] = ev["api_error_status"]
    return facts


def classify_claude(rc, mp):
    err = mp.err.read_text(errors="replace") if mp.err.exists() else ""
    low = err.lower()
    if NESTED in err:
        return "unavailable", {"reason": "nested launch refused", "refusal_observed": True}
    facts = failure_facts(mp.out) if rc != 0 else {}
    if any(w in low for w in AUTH_WORDS) or facts.get("assistant_error_category") == "authentication_failed":
        return "unavailable", dict(facts, reason="authentication unavailable")
    if rc == 0:
        return "observed", {}
    return "blocked", dict(facts, reason="cli_error", stderr_bytes=len(err.encode()))


def new_rid():
    return uuid.uuid4().hex[:12]


CMD_HEAD = """#!/bin/bash
T={tmp}; R={rid}
W=$(cat "$T/claude-$R.pid" 2>/dev/null)
P=$$; N=0
while [ "$P" != "$W" ] && [ "${{P:-0}}" -gt 1 ]; do
  P=$(sed -E 's/^[0-9]+ \\(.*\\) [A-Za-z] ([0-9]+) .*/\\1/' "/proc/$P/stat" 2>/dev/null)
  [ -n "$P" ] || break
  N=$((N+1))
done
if [ "$P" = "$W" ]; then REACHED=yes; else REACHED=no; fi
printf 'HOPS=%s REACHED=%s\\n' "$N" "$REACHED" >> "$T/depth-$R.txt"
"""
IDENT = '/bin/bash {helper} identify | tee -a "$T/selector-$R.txt"\n'


def write_cmd(group, rid, body=None):
    """The literal command a real run executes; its selector line also goes to a file in the group temp dir."""
    script = group.tmp / ("cmd-%s.sh" % rid)
    script.write_text(CMD_HEAD.format(tmp=shlex.quote(str(group.tmp)), rid=rid) + (body or IDENT.format(helper=shlex.quote(str(HELPER)))))
    return script


def prompt_for(script):
    return ("In this trusted disposable fixture, use Bash exactly once to execute this literal command, then report only its output: /bin/bash "
            + shlex.quote(str(script)))


def selector_capture(group, rid):
    """The runner-captured, redacted selector lines of one run, never the model's own report."""
    path = group.tmp / ("selector-%s.txt" % rid)
    out = []
    if path.exists():
        for line in path.read_text(errors="replace").splitlines():
            try:
                value = json.loads(line)
            except ValueError:
                continue
            for item in identities(value):
                out.append(dict(item, run_id=rid, line_sha256=sha(line)))
    return out


def depth_capture(group, rid):
    path = group.tmp / ("depth-%s.txt" % rid)
    if not path.exists():
        return None
    m = re.search(r"HOPS=(\d+) REACHED=(yes|no)", path.read_text())
    return {"hops": int(m.group(1)), "claude_process_reached": m.group(2) == "yes"} if m else None


# ---------------------------------------------------------------- baseline

def git(*args):
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    return subprocess.run(["git", "-C", str(REPO), *args], capture_output=True, text=True, env=env).stdout


def path_state(rel):
    status = git("status", "--porcelain=v1", "--untracked-files=all", "--", rel)
    diff = git("diff", "HEAD", "--", rel)
    return {"status_sha256": sha(status), "diff_sha256": sha(diff), "status_lines": len(status.splitlines())}


def tree_sha(root):
    root = Path(root)
    if not root.exists():
        return "absent"
    h = hashlib.sha256()
    for p in sorted(root.rglob("*")):
        if p.is_file() and "__pycache__" not in p.parts:
            h.update(str(p.relative_to(root)).encode() + b"\0" + sha(p.read_bytes()).encode() + b"\n")
    return h.hexdigest()


def current_state():
    rels = ["src", "plugins", "tests", str(BLOCKED_PKG.relative_to(REPO))]
    return {
        "real_claude_settings_sha256": real_settings_sha(),
        "git_state": {rel: path_state(rel) for rel in rels},
        "blocked_package_tree_sha256": tree_sha(BLOCKED_PKG),
        "done_package_tree_sha256": tree_sha(DONE_PKG),
    }


def baseline(force=False):
    if BASELINE.exists() and not force:
        return json.loads(BASELINE.read_text())
    data = dict(current_state(), recorded=now())
    BASELINE.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n")
    return data


def check_baseline():
    base = json.loads(BASELINE.read_text())
    cur = current_state()
    diffs = [k for k in cur if cur[k] != base.get(k)]
    return {"equal": not diffs, "differs": diffs}


# ---------------------------------------------------------------- preflight

def preflight_blocks():
    """Why the recorded preflight forbids any further real run, or None (also None when none is recorded)."""
    try:
        data = json.loads(PREFLIGHT.read_text())
    except (OSError, ValueError):
        return None
    if data.get("nested_launch_refused") is True:
        return "nested launch refused"
    if data.get("authentication_available") is False:
        return "authentication unavailable"
    return None


def preflight(cli=None, out=PREFLIGHT, ledger=LEDGER, name="pre"):
    cli = cli or claude_bin()
    runner = Runner(ledger)
    g = Group.create(name)
    sid = str(uuid.uuid4())
    rid = new_rid()
    settings = g.tmp / "settings-pre.json"
    settings.write_text(json.dumps({"enabledPlugins": {}}))
    # Default tool set and session persistence on, so the init event lists the print-mode tools
    # and a persisted transcript can be looked for. No tool is run: the prompt asks for one word.
    argv = [cli, "--print", "--setting-sources", "", "--settings", str(settings), "--session-id", sid,
            "--permission-mode", "dontAsk", "--strict-mcp-config", "--mcp-config", '{"mcpServers":{}}',
            "--max-budget-usd", "0.25", "--output-format", "stream-json", "--verbose", "--no-chrome",
            "Reply with the single word ok."]
    res = runner.run(g, "preflight", argv, label="preflight: one real Claude print run, default tools, persistence on",
                     timeout=90, real_claude=True, ok_result="observed", classify=classify_claude, rid=rid)
    events, init = parse_stream(res["out"])
    refused = res["extra"].get("refusal_observed") is True
    auth_failed = res["extra"].get("reason") == "authentication unavailable"
    transcript = "unavailable"
    ok_run = res["result"] == "observed"
    if ok_run:
        transcript = any(g.home.glob("**/%s.jsonl" % sid)) or any((g.home / ".claude").rglob("*%s*" % sid))
    data = {
        "claude_version": init.get("version") or "unavailable",
        "nested_launch_refused": True if refused else (False if ok_run else "unavailable"),
        "authentication_available": True if ok_run else (False if auth_failed else "unavailable"),
        "persisted_session_transcript_found": transcript,
        "print_mode_tools": init.get("tools") if isinstance(init.get("tools"), list) and init.get("tools") else "unavailable",
        "uv_present": bool(shutil.which("uv")),
        "bash_present": Path("/bin/bash").exists(),
        "git_present": bool(shutil.which("git")),
        "proc_present": Path("/proc/self/stat").exists(),
        "host_boot_identity": boot_id(),
        "preflight_exit": res["exit"],
        "preflight_result": res["result"],
        "stream_event_types": [e["type"] for e in events if e.get("type")],
    }
    Path(out).write_text(json.dumps(data, indent=2, sort_keys=True) + "\n")
    g.teardown("preflight")
    (GROUPS / (name + ".json")).unlink()
    return data


# ---------------------------------------------------------------- hook observer (settings hook command)

def hook_observe(args):
    raw = sys.stdin.buffer.read((1 << 20) + 1)
    payload = json.loads(raw)
    inputs = payload.get("tool_input") or {}
    record = {"kind": "actual_hook_input", "variant": args.variant}
    for field in ("hook_event_name", "session_id", "tool_use_id", "agent_id", "agent_type"):
        value = payload.get(field)
        if isinstance(value, str) and ID.fullmatch(value):
            record[field] = value
    record["tool_name"] = payload.get("tool_name") if payload.get("tool_name") == "Bash" else "other"
    record["top_level_keys"] = sorted(payload)
    record["tool_input_keys"] = sorted(inputs) if isinstance(inputs, dict) else []
    if isinstance(inputs, dict):
        record["run_in_background"] = inputs.get("run_in_background") is True
        if isinstance(inputs.get("command"), str):
            record["command_sha256"] = sha(inputs["command"])
    record["cwd_is_fixture"] = payload.get("cwd") == args.cwd
    if payload.get("hook_event_name") == "PostToolUse":
        response = payload.get("tool_response")
        record["tool_response_keys"] = sorted(response) if isinstance(response, dict) else []
        record["selector_results"] = identities(response)
        append(args.log, record)
        return 0
    result = subprocess.run(["/bin/bash", args.runner], input=raw, capture_output=True, timeout=8)
    record["adapter_exit"] = result.returncode
    record["rewritten"] = False
    if result.stdout:
        specific = json.loads(result.stdout).get("hookSpecificOutput", {})
        record["rewritten"] = "updatedInput" in specific
        record["permission_decision_present"] = "permissionDecision" in specific
    append(args.log, record)
    sys.stdout.buffer.write(result.stdout)
    sys.stderr.buffer.write(result.stderr)
    return result.returncode


# ---------------------------------------------------------------- self-check

FAKE_CLAUDE = """#!/bin/sh
# Stand-in for the Claude CLI: prints a stream-json init event and a result, and
# writes a secret-looking value to stderr so redaction can be checked.
echo '{"type":"system","subtype":"init","claude_code_version":"fake-1","session_id":"00000000-0000-4000-8000-000000000000","tools":["Bash"]}'
echo '{"type":"result","subtype":"success","session_id":"00000000-0000-4000-8000-000000000000"}'
echo "secret=$OBS_SECRET" >&2
"""


class Check:
    def __init__(self, path):
        self.path = Path(path)
        self.path.write_text("observe.py self-check, started " + now() + "\n")
        self.failed = 0

    def line(self, text):
        with open(self.path, "a") as fh:
            fh.write(text + "\n")

    def ok(self, name, cond, detail=""):
        self.line("CHECK %s: %s %s" % (name, "PASS" if cond else "FAIL", detail))
        if not cond:
            self.failed += 1


def selfcheck():
    chk = Check(ART / "observe-selfcheck.log")
    runner = Runner()
    secret = "sk-selfcheck-" + uuid.uuid4().hex
    argsecret = "--selfcheck-arg-" + uuid.uuid4().hex
    base_before = json.loads(BASELINE.read_text())
    settings_before = real_settings_sha()
    g = Group.create("selfcheck")
    try:
        # 1. Redaction: a secret-looking environment value and a command argument never reach the ledger or preflight.json.
        runner.run(g, "selfcheck-redaction", ["sh", "-c", "exit 0", "x", argsecret], label="selfcheck: redaction", timeout=10,
                   env=dict(g.env(), OBS_SECRET=secret))
        fake = g.tmp / "fake-claude"
        fake.write_text(FAKE_CLAUDE)
        fake.chmod(0o700)
        tmp_ledger = g.tmp / "ledger.jsonl"
        tmp_pre = g.tmp / "preflight.json"
        os.environ["OBS_SECRET"] = secret
        try:
            pdata = preflight(cli=str(fake), out=tmp_pre, ledger=tmp_ledger, name="selfcheck-pre")
        finally:
            del os.environ["OBS_SECRET"]
        leaked = [str(p) for p in (LEDGER, tmp_pre, tmp_ledger) if secret in p.read_text() or argsecret in p.read_text()]
        chk.ok("redaction", not leaked, "secret env value and command argument absent from run-status.jsonl, the preflight output and the temporary ledger")
        chk.ok("preflight-fields", all(v is not None for v in pdata.values()) and pdata["claude_version"] == "fake-1",
               "fake-CLI preflight output holds observed values or the word unavailable")

        # 2. A timeout kills the whole process group, is recorded blocked, and sweeps a setsid child it started.
        res = runner.run(g, "selfcheck-timeout", ["sh", "-c", "sleep 120 & setsid sleep 121 & sleep 122"], label="selfcheck: timeout", timeout=1.5)
        gone = True
        try:
            os.killpg(res["mp"].pid, 0)
            gone = False
        except ProcessLookupError:
            pass
        chk.ok("timeout-group-and-sweep", res["timed_out"] and res["result"] == "blocked" and gone and not g.procs_under(),
               "timed_out=%s result=%s group_gone=%s leftover_under_group=%d swept=%s" % (res["timed_out"], res["result"], gone, len(g.procs_under()), json.loads(LEDGER.read_text().splitlines()[-1])["swept"]))

        # 3 and 4. Group persistence, a surviving job, and a timeout that must spare the survivor.
        sid = str(uuid.uuid4())
        runner.run(g, "selfcheck-first", ["sh", "-c", "exit 0"], label="selfcheck: first run in the group", timeout=10, sid=sid)
        g.make_governed(sid)
        surv = g.spawn(["sleep", "300"], "survivor")
        g.register_survivor("selfcheck-survivor", surv.pid)
        r2 = runner.run(g, "selfcheck-second", ["sh", "-c", "exit 0"], label="selfcheck: second run, store and record must still exist", timeout=10, sid=sid)
        found = r2["extra"]["store_check"]
        chk.ok("group-persistence", found.get("store_exists") and found.get("governed_record_exists") and g.root.exists(),
               "second run in the same group found the launch-level store and governed session record: %s" % found)
        chk.ok("survivor-after-case", alive(surv.pid, surv.start), "job marked surviving is alive after its case ended")
        runner.run(g, "selfcheck-later-timeout", ["sh", "-c", "sleep 60"], label="selfcheck: later case times out", timeout=1, sid=sid)
        chk.ok("survivor-after-later-timeout", alive(surv.pid, surv.start), "surviving job still alive after a later case in the same group timed out and was swept")
        chk.ok("home-kept-until-teardown", g.home.is_dir() and g.fixture.is_dir() and g.tmp.is_dir(), "disposable HOME, fixture and temp directory exist before teardown")

        # 5. A signal after a ready file ends only the named process; a start-tick mismatch is refused.
        other = g.spawn(["sleep", "300"], "unrelated")
        ready = g.tmp / "ready-a"
        res = runner.run(g, "selfcheck-signal", ["sh", "-c", "touch %s; sleep 120" % shlex.quote(str(ready))], label="selfcheck: signal after ready file",
                         timeout=15, ready=ready, signal_name="SIGKILL")
        chk.ok("signal-after-ready", res["signal"] and res["signal"]["sent"] and res["exit"] == "signal:SIGKILL" and alive(other.pid, other.start),
               "named process ended by %s; unrelated process in the same group alive=%s" % (res["exit"], alive(other.pid, other.start)))
        ready2 = g.tmp / "ready-b"
        res2 = runner.run(g, "selfcheck-signal-mismatch", ["sh", "-c", "touch %s; sleep 2" % shlex.quote(str(ready2))],
                          label="selfcheck: signal with wrong start ticks", timeout=15, ready=ready2, signal_name="SIGKILL", signal_start=1)
        chk.ok("signal-refused-on-mismatch", res2["signal"] and res2["signal"]["sent"] is False and res2["exit"] == 0,
               "signal refused (%s); process ended on its own with exit %s" % (res2["signal"] and res2["signal"].get("refused_reason"), res2["exit"]))
        other.kill_group()
        other.p.wait(timeout=5)

        # 6. The thirteenth real Claude run is refused (cap lowered to 2 on a temporary ledger), and every real run records equal settings checksums.
        small = Runner(tmp_ledger.with_name("cap.jsonl"), cap=2)
        for i in range(2):
            small.run(g, "selfcheck-cap-%d" % i, [str(fake)], label="selfcheck: fake real run", timeout=10, real_claude=True, ok_result="observed")
        refused = False
        try:
            small.run(g, "selfcheck-cap-3", [str(fake)], label="selfcheck: fake real run", timeout=10, real_claude=True)
        except Refused:
            refused = True
        lines = [json.loads(x) for x in small.ledger.read_text().splitlines()]
        real_lines = [x for x in lines if x.get("real_claude")]
        chk.ok("run-cap-refusal", refused and len(real_lines) == 2, "third real run refused with the cap at 2; real runs counted=%d" % len(real_lines))
        chk.ok("settings-checksum-per-run", all(x["settings_sha256_before"] == x["settings_sha256_after"] for x in real_lines + [json.loads(x) for x in tmp_ledger.read_text().splitlines() if json.loads(x).get("real_claude")]),
               "each real_claude entry records equal before-run and after-run settings checksums")
    finally:
        info = g.teardown("selfcheck")
        (GROUPS / "selfcheck.json").unlink()
    chk.ok("teardown", info["directory_removed"] and info["leftover_processes"] == 0 and not g.root.exists(), "teardown removed the directories: %s" % info)
    log = CLEANUP.read_text()
    chk.ok("teardown-logs-survivor-stop", "why=survivor-teardown" in log and "case=selfcheck" in log, "phase2-cleanup.log records the survivor stop")
    # 7. The runner touched nothing outside its temporary directory and ./artifacts/.
    after = check_baseline()
    chk.ok("nothing-outside", after["equal"] and real_settings_sha() == settings_before and base_before == json.loads(BASELINE.read_text()),
           "src/, plugins/, tests/ and blocked-package state equal baseline.json: %s; real settings checksum unchanged" % after)
    chk.line("SELFCHECK %s failures=%d" % ("PASS" if not chk.failed else "FAIL", chk.failed))
    return chk.failed


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("command", choices=("baseline", "preflight", "selfcheck", "check-baseline", "teardown", "hook-observe"))
    ap.add_argument("name", nargs="?")
    ap.add_argument("--runner")
    ap.add_argument("--log")
    ap.add_argument("--variant")
    ap.add_argument("--cwd")
    ap.add_argument("--force", action="store_true")
    a = ap.parse_args()
    if a.command == "baseline":
        print(json.dumps(baseline(a.force), indent=2, sort_keys=True))
    elif a.command == "check-baseline":
        print(json.dumps(check_baseline()))
    elif a.command == "preflight":
        print(json.dumps(preflight(), indent=2, sort_keys=True))
    elif a.command == "selfcheck":
        return 1 if selfcheck() else 0
    elif a.command == "teardown":
        print(json.dumps(Group.load(a.name).teardown("teardown")))
    else:
        return hook_observe(a)
    return 0


if __name__ == "__main__":
    sys.exit(main())

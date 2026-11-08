"""FR-100 L2 pre-push hook matrix (T-01..T-24, T-16a/b/c, T-STALE-1) and FR-101 pins.

Real git under a temporary HOME with GIT_CONFIG_GLOBAL and GIT_CONFIG_SYSTEM at
/dev/null. The governed actor is a real launch job from the selector's
prepare/run; the unknown actor is that job with its record damaged, or a setsid
pusher with a planted record. Until Task 8 the hook is placed by a test-local
copy (source section 8.2), not by the installer.
"""

import hashlib
import importlib.util
import json
import os
import re
import shlex
import shutil
import signal
import subprocess
import sys
import tempfile
import time
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[2]
HOOK = REPO / "src/superclaude/hooks/scripts/launch-level-pre-push.sh"
SELECTOR = REPO / "src/superclaude/hooks/scripts/launch-job-identity.sh"
ORCA = REPO / "src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py"
UV = shutil.which("uv")
P = "launch-level pre-push:"
GATE = "<gate>"
BRANCHES = ["main", "master"]
ACTORS = ["governed", "unknown", "human"]
ROUTE = (
    "pre-push.launch-level and ~/.claude/hooks/launch-job-identity.sh) or "
    "releases the session by deleting its level record."
)
KEPT = (
    " The job record is kept as evidence and must not be deleted while that "
    "launch job's processes run."
)
BYPASS = re.compile(r"--no-verify|core\.hooksPath|--config-env|GIT_CONFIG_|(?:^|\s)-c(?:\s|$)")
pytestmark = pytest.mark.skipif(
    sys.platform != "linux" or UV is None, reason="Linux proc contract and uv"
)


def wait_for(check, timeout=20):
    until = time.monotonic() + timeout
    while time.monotonic() < until:
        result = check()
        if result:
            return result
        time.sleep(0.02)
    raise AssertionError("timed out waiting for fixture event")


def q(value):
    return shlex.quote(str(value))


def push(*args):
    return shlex.join(["git", "push", "origin", *args])


class Result:
    def __init__(self, d, i):
        self.rc = int((d / f"{i}.rc").read_text())
        self.out, self.err, self.before, self.after = (
            (d / f"{i}.{s}").read_text() for s in ("out", "err", "before", "after")
        )


class Repo:
    """Bare remote, clone with the hook copied in, and a fake launch-level store."""

    def __init__(self, tmp, object_format=None):
        self.tmp = tmp
        tmp.mkdir(exist_ok=True)
        self.home = tmp / "home"
        self.home.mkdir(mode=0o700)
        self.root = self.home / ".claude/state/launch-level"
        (self.root / "sessions").mkdir(parents=True, mode=0o700)
        self.root.chmod(0o700)
        self.selector = self.home / ".claude/hooks/launch-job-identity.sh"
        self.selector.parent.mkdir()
        shutil.copyfile(SELECTOR, self.selector)
        self.selector.chmod(0o755)
        self.env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
        self.env.update(
            HOME=str(self.home),
            GIT_CONFIG_GLOBAL="/dev/null",
            GIT_CONFIG_SYSTEM="/dev/null",
            GIT_CONFIG_NOSYSTEM="1",
            GIT_TERMINAL_PROMPT="0",
            GIT_AUTHOR_NAME="L2 fixture",
            GIT_AUTHOR_EMAIL="fixture@example.invalid",
            GIT_COMMITTER_NAME="L2 fixture",
            GIT_COMMITTER_EMAIL="fixture@example.invalid",
            UV_PYTHON=sys.executable,
            UV_PYTHON_DOWNLOADS="never",
        )
        self.processes, self.dirs, self.last_record = [], [], None
        session = self.root / "sessions/old"
        session.write_text("worktree\n")
        session.chmod(0o600)
        self.remote, self.work = tmp / "remote.git", tmp / "clone"
        fmt = ["--object-format=" + object_format] if object_format else []
        self.g("init", "-q", "--bare", "--initial-branch=main", *fmt, self.remote)
        self.g("clone", "-q", self.remote, self.work)
        self.git("config", "user.name", "L2 fixture")
        self.git("config", "user.email", "fixture@example.invalid")
        self.git("config", "commit.gpgsign", "false")
        self.a = self.commit("a")
        self.git("push", "-q", "origin", "HEAD:refs/heads/main", "HEAD:refs/heads/master")
        self.b = self.commit("b")
        self.alt = self.git("commit-tree", self.b + "^{tree}", "-p", self.a, "-m", "alt")
        self.git("branch", "alt", self.alt)
        self.git("branch", "feature", self.b)
        self.initial = self.refs()
        self.hook = self.work / ".git/hooks/pre-push"
        shutil.copyfile(HOOK, self.hook)
        self.hook.chmod(0o755)
        self.data = self.hook.parent / "pre-push.launch-level"
        self.write_data(f"{self.home}\n{os.path.dirname(UV)}\n")

    # --- git -----------------------------------------------------------------
    def g(self, *args, cwd=None, check=True):
        result = subprocess.run(
            ["git", *map(str, args)],
            env=self.env,
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=20,
        )
        if check:
            assert result.returncode == 0, result.stderr
        return result.stdout.strip()

    def git(self, *args, **kw):
        return self.g("-C", self.work, *args, **kw)

    def bare(self, *args, **kw):
        return self.g("--git-dir", self.remote, *args, **kw)

    def commit(self, label):
        (self.work / "fixture.txt").write_text(label + "\n")
        self.git("add", "fixture.txt")
        self.git("commit", "-q", "-m", label)
        return self.git("rev-parse", "HEAD")

    def refs(self):
        return self.bare("for-each-ref")

    def remote_ref(self, ref):
        ref = ref if ref.startswith("refs/") else "refs/heads/" + ref
        out = self.bare("rev-parse", "--verify", "-q", ref, check=False)
        return out or None

    def seed(self, src, dst):
        # A bare-side fetch runs no pre-push hook.
        self.bare("fetch", "-q", self.work, f"+refs/heads/{src}:refs/heads/{dst}")

    def reset(self, *_):
        for line in self.refs().splitlines():
            self.bare("update-ref", "-d", line.split()[-1])
        for line in self.initial.splitlines():
            oid, _, ref = line.split()
            self.bare("update-ref", ref, oid)

    def worktree(self, name="wt", branch="topic"):
        path = self.tmp / name
        self.git("worktree", "add", "-q", "-b", branch, path, self.b)
        return path

    def write_data(self, text, mode=0o644):
        self.data.unlink(missing_ok=True)
        self.data.write_text(text)
        self.data.chmod(mode)

    def stub(self, output=None, body=None):
        # Replace the pinned selector with one printing fixed bytes (FR-022 tests).
        out = self.tmp / "stub.out"
        if output is not None:
            out.write_bytes(output.encode())
        self.selector.write_text("#!/bin/bash\n" + (body or f"exec /usr/bin/cat {q(out)}\n"))
        self.selector.chmod(0o755)

    # --- launch jobs -----------------------------------------------------------
    def call(self, *args):
        return subprocess.run(
            ["/bin/bash", str(self.selector), *args],
            env=self.env,
            capture_output=True,
            text=True,
            timeout=20,
        )

    def start(self, command):
        prepared = self.call("prepare", "old", command)
        assert prepared.returncode == 0, prepared.stderr
        process = subprocess.Popen(
            ["bash", str(self.selector), "run", prepared.stdout.strip()],
            env=self.env,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        self.processes.append(process)
        return process

    def records(self):
        return list((self.root / "jobs").glob("*.json"))

    def damage(self, record, kind):
        value = json.loads(record.read_text())
        if kind == "kill":
            os.kill(value["pid"], signal.SIGKILL)
            wait_for(lambda: _state(value["pid"]) in ("Z", None))
        elif kind == "mode":
            record.chmod(0o664)
        else:
            if kind == "start":
                value["start"] += 1
            else:
                value["boot"] = "00000000-0000-0000-0000-000000000000"
            record.chmod(0o600)
            record.write_text(json.dumps(value))
        return record.read_bytes()

    def plant(self, pid):
        jobs = self.root / "jobs"
        jobs.mkdir(mode=0o700, exist_ok=True)
        boot = Path("/proc/sys/kernel/random/boot_id").read_text().strip()
        start = int(Path(f"/proc/{pid}/stat").read_text().rsplit(")", 1)[1].split()[19])
        record = jobs / f"{pid}.json"
        value = {"pid": pid, "start": start + 1, "boot": boot, "kernel_sid": pid, "session_id": "old"}
        record.write_text(json.dumps(value))
        record.chmod(0o600)
        return record

    def run(self, actor, steps, cwd=None, damage="start", actions=()):
        """Run shell steps as one actor; for-each-ref is captured around each step.

        GATE pauses the actor; the matching action(record, d) runs, then it goes on.
        """
        d = Path(tempfile.mkdtemp(dir=self.tmp))
        self.dirs.append(d)
        snap = shlex.join(["git", "--git-dir", str(self.remote), "for-each-ref"])

        def wait(p):
            return f"while [ ! -e {q(p)} ]; do sleep .02; done"

        lines = [f"cd {q(cwd or self.work)} || exit 9", f"touch {q(d / 'ready')}", wait(d / "go")]
        gates, n = [], 0
        for step in steps:
            if step == GATE:
                gates.append((n, d / f"gate{len(gates)}"))
                lines.append(wait(gates[-1][1]))
                continue
            o = f"{q(d)}/{n}"
            lines += [
                f"{snap} > {o}.before",
                f"( {step} ) < /dev/null > {o}.out 2> {o}.err; echo $? > {o}.rcx",
                f"{snap} > {o}.after",
                f"mv {o}.rcx {o}.rc",
            ]
            n += 1
        lines += [f"touch {q(d / 'finished')}", wait(d / "done")]
        script = d / "steps.sh"
        script.write_text("\n".join(lines) + "\n")
        if actor in ("governed", "unknown"):
            process = self.start("bash " + q(script))
        else:
            process = subprocess.Popen(
                ["bash", str(script)],
                env=self.env,
                start_new_session=actor == "planted",
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )
            self.processes.append(process)
        wait_for((d / "ready").exists)
        record = damaged = original = None
        if actor == "unknown":
            record = wait_for(self.records)[0]
            original, mode = record.read_bytes(), record.stat().st_mode & 0o777
            damaged = self.damage(record, damage)
        elif actor == "planted":
            record = self.plant(process.pid)
            damaged = record.read_bytes()
        self.last_record = record
        (d / "go").touch()
        for (index, gate), action in zip(gates, actions):
            if index:
                wait_for((d / f"{index - 1}.rc").exists, timeout=40)
            action(record, d)
            gate.touch()
        wait_for((d / "finished").exists, timeout=60)
        results = [Result(d, i) for i in range(n)]
        if record is not None and record.exists():
            # FR-025: the hook never alters or removes a job record.
            assert record.read_bytes() == damaged
            if actor == "unknown" and damage != "kill":
                record.chmod(0o600)
                record.write_bytes(original)
                record.chmod(mode)
            else:
                record.unlink()
        (d / "done").touch()
        process.communicate(timeout=30)
        return results

    def cleanup(self):
        for d in self.dirs:
            for name in ["go", "done", *(f"gate{i}" for i in range(12))]:
                (d / name).touch()
        for path in self.records():
            try:
                os.kill(json.loads(path.read_text())["pid"], signal.SIGTERM)
            except (ProcessLookupError, ValueError, KeyError):
                pass
        for process in self.processes:
            try:
                process.communicate(timeout=10)
            except subprocess.TimeoutExpired:
                process.kill()
                process.communicate(timeout=5)


def _state(pid):
    try:
        return Path(f"/proc/{pid}/stat").read_text().rsplit(")", 1)[1].split()[0]
    except FileNotFoundError:
        return None


@pytest.fixture
def make(tmp_path):
    made = []

    def factory(name="r", **kw):
        made.append(Repo(tmp_path / name, **kw))
        return made[-1]

    try:
        yield factory
    finally:
        for repo in made:
            repo.cleanup()


@pytest.fixture
def repo(make):
    return make()


# --- assertions ---------------------------------------------------------------
def protected(r, ref):
    line = (
        f"{P} L2-PROTECTED: a governed launch session may not push to {ref}; the "
        "whole push was refused. A person releases the session as the claim's "
        "launch result describes."
    )
    assert r.rc != 0 and line in r.err.splitlines(), r.err
    assert r.before == r.after


def unknown(r, ref, why, tail=""):
    lines = [line for line in r.err.splitlines() if line.startswith(P)]
    assert r.rc != 0 and len(lines) == 2, r.err
    assert lines[0] == (
        f"{P} L2-UNKNOWN: could not classify this push ({why}) and it targets {ref}; "
        "the whole push was refused, and pushes to other refs are allowed."
    )
    assert lines[1].startswith(f"{P} to push there, a person fixes the cause (check ")
    assert lines[1].endswith(ROUTE + tail), lines[1]
    assert r.before == r.after


def stale(record):
    return (
        f"job record stale at {record}",
        " For this job record: no launch job owns this session any more; a person "
        f"removes the record with: rm '{record}'",
    )


def allowed(r):
    assert r.rc == 0, r.err
    assert P not in r.err


def refused(repo, actor, r, ref):
    if actor == "governed":
        protected(r, ref)
    else:
        unknown(r, ref, *stale(repo.last_record))


def check(repo, actor, r, ref):
    if actor == "human":
        allowed(r)
    else:
        refused(repo, actor, r, ref)


def sequence(repo, actor, steps, **kw):
    """Run steps with a remote reset between them (GATE plus reset action)."""
    gated = [steps[0]]
    for step in steps[1:]:
        gated += [GATE, step]
    return repo.run(actor, gated, actions=[repo.reset] * (len(steps) - 1), **kw)


# --- T-01..T-13: the push shapes ----------------------------------------------
@pytest.mark.parametrize("branch", BRANCHES)
@pytest.mark.parametrize("actor", ACTORS)
def test_t01_create_protected_ref(repo, actor, branch):
    repo.bare("update-ref", "-d", "refs/heads/" + branch)
    (r,) = repo.run(actor, [push("feature:refs/heads/" + branch)])
    check(repo, actor, r, "refs/heads/" + branch)
    assert repo.remote_ref(branch) == (repo.b if actor == "human" else None)


@pytest.mark.parametrize("branch", BRANCHES)
@pytest.mark.parametrize("actor", ACTORS)
def test_t02_fast_forward_update(repo, actor, branch):
    (r,) = repo.run(actor, [push("HEAD:" + branch)])
    check(repo, actor, r, "refs/heads/" + branch)
    assert repo.remote_ref(branch) == (repo.b if actor == "human" else repo.a)


@pytest.mark.parametrize("branch", BRANCHES)
@pytest.mark.parametrize("actor", ACTORS)
def test_t03_delete(repo, actor, branch):
    results = sequence(repo, actor, [push(":" + branch), push("--delete", branch)])
    for r in results:
        if actor == "human":
            # Allowed by L2; a remote's own refusal is also acceptable.
            assert P not in r.err
            assert r.rc != 0 or "refs/heads/" + branch not in r.after
        else:
            refused(repo, actor, r, "refs/heads/" + branch)


@pytest.mark.parametrize("branch", BRANCHES)
@pytest.mark.parametrize("actor", ACTORS)
def test_t04_force(repo, actor, branch):
    results = sequence(repo, actor, [push("+alt:" + branch), push("--force", "feature:" + branch)])
    for r in results:
        check(repo, actor, r, "refs/heads/" + branch)
    assert repo.remote_ref(branch) == (repo.b if actor == "human" else repo.a)


@pytest.mark.parametrize("branch", BRANCHES)
@pytest.mark.parametrize("actor", ACTORS)
def test_t05_configured_mapping(repo, actor, branch):
    repo.git("config", "remote.origin.push", "HEAD:refs/heads/" + branch)
    wt = repo.worktree()
    repo.g("-C", wt, "branch", "-q", "--set-upstream-to=origin/" + branch)
    (r,) = repo.run(actor, ["git push origin"])
    check(repo, actor, r, "refs/heads/" + branch)
    repo.reset()
    repo.git("config", "--unset", "remote.origin.push")  # it would override push.default
    (u,) = repo.run(actor, ["git -c push.default=upstream push origin"], cwd=wt)
    check(repo, actor, u, "refs/heads/" + branch)
    assert repo.remote_ref(branch) == (repo.b if actor == "human" else repo.a)


@pytest.mark.parametrize("branch", BRANCHES)
@pytest.mark.parametrize("actor", ACTORS)
def test_t06_mixed_and_atomic(repo, actor, branch):
    refs = ["feature:refs/heads/feature", "HEAD:refs/heads/" + branch]
    results = sequence(repo, actor, [push(*refs), push("--atomic", *refs)])
    for r in results:
        check(repo, actor, r, "refs/heads/" + branch)
        if actor != "human":
            assert "refs/heads/feature" not in r.after


EDGES = ["refs/tags/main", "refs/heads/mainline", "refs/heads/feature/main", "refs/heads/Main", "refs/heads/main2"]


@pytest.mark.parametrize("actor", ACTORS)
def test_t07_exact_name_edges_allowed(repo, actor):
    results = repo.run(actor, [push("HEAD:" + ref) for ref in EDGES])
    for ref, r in zip(EDGES, results):
        allowed(r)
        assert repo.remote_ref(ref) == repo.b


@pytest.mark.parametrize("branch", BRANCHES)
@pytest.mark.parametrize("actor", ACTORS)
def test_t08_empty_stream(repo, actor, branch):
    ref = "refs/heads/" + branch
    steps = [
        push(f"{repo.a}:{ref}"),
        push(f"--force-with-lease={ref}:{repo.b}", "alt:" + ref),
        GATE,
        push("alt:" + ref),
    ]
    up_to_date, lease, known = repo.run(
        actor, steps, actions=[lambda *_: repo.seed("feature", branch)]
    )
    assert up_to_date.rc == 0
    for r in (up_to_date, lease, known):
        assert P not in r.err and r.before == r.after
    assert lease.rc != 0 and known.rc != 0


@pytest.mark.parametrize("branch", BRANCHES)
@pytest.mark.parametrize("actor", ACTORS)
def test_t09_fetch_first(repo, actor, branch):
    tree = repo.bare("rev-parse", repo.a + "^{tree}")
    ahead = repo.bare("commit-tree", tree, "-p", repo.a, "-m", "remote only")
    repo.bare("update-ref", "refs/heads/" + branch, ahead)
    (r,) = repo.run(actor, [push("HEAD:" + branch)])
    if actor == "human":
        assert r.rc != 0 and "fetch first" in r.err and P not in r.err
    else:
        refused(repo, actor, r, "refs/heads/" + branch)
    assert repo.remote_ref(branch) == ahead


@pytest.mark.parametrize("branch", BRANCHES)
@pytest.mark.parametrize("actor", ACTORS)
def test_t10_six_field_source(repo, actor, branch):
    (r,) = repo.run(actor, [push("HEAD@{0 days ago}:refs/heads/" + branch)])
    check(repo, actor, r, "refs/heads/" + branch)


@pytest.mark.parametrize("branch", BRANCHES)
@pytest.mark.parametrize("actor", ACTORS)
def test_t11_sha256_repository(make, actor, branch):
    repo = make("sha256", object_format="sha256")
    assert len(repo.b) == 64
    main, feature = repo.run(actor, [push("HEAD:" + branch), push("HEAD:refs/heads/feature")])
    check(repo, actor, main, "refs/heads/" + branch)
    allowed(feature)


@pytest.mark.parametrize("branch", BRANCHES)
@pytest.mark.parametrize("actor", ACTORS)
def test_t12_dry_run(repo, actor, branch):
    (r,) = repo.run(actor, [push("--dry-run", "HEAD:" + branch)])
    check(repo, actor, r, "refs/heads/" + branch)
    assert r.before == r.after


@pytest.mark.parametrize("branch", BRANCHES)
@pytest.mark.parametrize("actor", ACTORS)
def test_t13_linked_worktree(repo, actor, branch):
    wt = repo.worktree()
    (r,) = repo.run(actor, [push("HEAD:" + branch)], cwd=wt)
    check(repo, actor, r, "refs/heads/" + branch)


# --- T-14..T-18: sessions, release, damaged records, data file -----------------
@pytest.mark.parametrize("branch", BRANCHES)
def test_t14_agent_and_human_same_linked_worktree(repo, branch):
    wt = repo.worktree()
    human = {}

    def human_push(*_):
        human["r"] = subprocess.run(
            ["git", "push", "origin", "HEAD:" + branch],
            cwd=wt,
            env=repo.env,
            capture_output=True,
            text=True,
            timeout=20,
        )

    (agent,) = repo.run("governed", [GATE, push("+alt:" + branch)], cwd=wt, actions=[human_push])
    assert human["r"].returncode == 0 and P not in human["r"].stderr
    protected(agent, "refs/heads/" + branch)
    assert repo.remote_ref(branch) == repo.b


@pytest.mark.parametrize("branch", BRANCHES)
def test_t15_release_while_job_live(repo, branch):
    def release(*_):
        (repo.root / "sessions/old").unlink()

    before, after = repo.run(
        "governed", [push("HEAD:" + branch), GATE, push("HEAD:" + branch)], actions=[release]
    )
    protected(before, "refs/heads/" + branch)
    allowed(after)
    assert repo.remote_ref(branch) == repo.b


@pytest.mark.parametrize("damage", ["start", "boot"])
@pytest.mark.parametrize("branch", BRANCHES)
def test_t16_stale_record(repo, branch, damage):
    main, feature = repo.run(
        "unknown", [push("HEAD:" + branch), push("HEAD:refs/heads/feature")], damage=damage
    )
    unknown(main, "refs/heads/" + branch, *stale(repo.last_record))
    allowed(feature)


@pytest.mark.parametrize("branch", BRANCHES)
def test_t16a_killed_supervisor_orphaned(repo, branch):
    main, feature = repo.run(
        "unknown", [push("HEAD:" + branch), push("HEAD:refs/heads/feature")], damage="kill"
    )
    unknown(main, "refs/heads/" + branch, f"job record orphaned at {repo.last_record}", KEPT)
    assert "rm '" not in main.err
    allowed(feature)


@pytest.mark.parametrize("branch", BRANCHES)
def test_t16b_sibling_session_beside_governed_job(repo, branch):
    wt = repo.worktree()
    sibling = {}

    def sibling_push(*_):
        sibling["r"] = subprocess.run(
            ["git", "push", "origin", "HEAD:" + branch],
            cwd=repo.work,
            env=repo.env,
            capture_output=True,
            text=True,
            timeout=20,
            start_new_session=True,
        )

    (agent,) = repo.run("governed", [GATE, push("+alt:" + branch)], cwd=wt, actions=[sibling_push])
    assert sibling["r"].returncode == 0 and P not in sibling["r"].stderr
    protected(agent, "refs/heads/" + branch)


@pytest.mark.parametrize("branch", BRANCHES)
def test_t16c_group_writable_record_unreadable(repo, branch):
    main, feature = repo.run(
        "unknown", [push("HEAD:" + branch), push("HEAD:refs/heads/feature")], damage="mode"
    )
    unknown(main, "refs/heads/" + branch, f"job record unreadable at {repo.last_record}", KEPT)
    assert "rm '" not in main.err
    allowed(feature)


@pytest.mark.skipif(
    os.geteuid() != 0 or shutil.which("setpriv") is None,
    reason="T-16c second uid: needs root and setpriv to push as another uid; "
    "the group-writable record above is the stand-in",
)
def test_t16c_real_second_uid():
    # Own temp dir outside pytest's 0700 base dirs, so no shared parent is widened.
    top = Path(tempfile.mkdtemp())
    try:
        top.chmod(0o755)
        repo = Repo(top / "r")
        repo.tmp.chmod(0o755)
        for tree in (repo.work, repo.remote):
            for path in [tree, *tree.rglob("*")]:
                path.chmod(path.stat().st_mode | (0o055 if path.is_dir() else 0o044))
        # safe.directory is honoured only from global config, and a local push
        # drops -c (GIT_CONFIG_PARAMETERS) before it starts receive-pack.
        config = top / "gitconfig"
        config.write_text("[safe]\n\tdirectory = *\n")
        config.chmod(0o644)
        result = subprocess.run(
            ["setpriv", "--reuid=65534", "--regid=65534", "--clear-groups",
             "git", "-C", str(repo.work), "push", "origin", "HEAD:main"],
            env={**repo.env, "GIT_CONFIG_GLOBAL": str(config)},
            capture_output=True, text=True, timeout=30,
        )
        # The second uid does not own pre-push.launch-level (FR-020 owner check),
        # so the hook is unknown before any record is read: main refused, no rm.
        assert result.returncode != 0 and P + " L2-UNKNOWN" in result.stderr
        assert "rm '" not in result.stderr
        assert repo.remote_ref("main") == repo.a
        repo.cleanup()
    finally:
        shutil.rmtree(top, ignore_errors=True)


@pytest.mark.parametrize("branch", BRANCHES)
def test_t_stale_1_planted_record_then_rm(repo, branch):
    def person_runs_rm(record, d):
        line = re.search(r"rm '([^']+)'$", (d / "0.err").read_text(), re.M)
        assert line and line.group(1) == str(record)
        subprocess.run(["rm", line.group(1)], check=True)

    main, feature, again = repo.run(
        "planted",
        [push("HEAD:" + branch), push("HEAD:refs/heads/feature"), GATE, push("HEAD:" + branch)],
        actions=[person_runs_rm],
    )
    assert main.rc == 1
    unknown(main, "refs/heads/" + branch, *stale(repo.last_record))
    allowed(feature)
    allowed(again)
    assert repo.remote_ref(branch) == repo.b


@pytest.mark.parametrize("branch", BRANCHES)
def test_t17_human_without_uv_on_path_and_no_store(repo, branch):
    shutil.rmtree(repo.home / ".claude/state")
    (r,) = repo.run("human", ["env PATH=/usr/bin:/bin " + push("HEAD:" + branch)])
    allowed(r)
    assert repo.remote_ref(branch) == repo.b


def _break(repo, case):
    if case == "data-missing":
        repo.data.unlink()
    elif case == "data-group-writable":
        repo.data.chmod(0o664)
    elif case == "data-one-line":
        repo.write_data(f"{repo.home}\n")
    elif case == "data-relative":
        repo.write_data(f"home\n{os.path.dirname(UV)}\n")
    elif case == "data-symlink":
        target = repo.tmp / "elsewhere"
        target.write_text(repo.data.read_text())
        repo.data.unlink()
        repo.data.symlink_to(target)
    elif case == "script-missing":
        repo.selector.unlink()
    elif case == "script-not-executable":
        repo.selector.chmod(0o644)
    elif case == "uv-dir-wrong":
        repo.write_data(f"{repo.home}\n{repo.tmp / 'no-uv-here'}\n")
    else:
        repo.stub(body="exec /usr/bin/sleep 30\n")


T18 = {
    "data-missing": "no valid data file",
    "data-group-writable": "no valid data file",
    "data-one-line": "no valid data file",
    "data-relative": "no valid data file",
    "data-symlink": "no valid data file",
    "script-missing": "identity script missing",
    "script-not-executable": "identity script missing",
    "uv-dir-wrong": "identity check failed",
    "selector-timeout": "identity check timed out",
}


@pytest.mark.parametrize("case", list(T18))
def test_t18_invalid_data_file_or_selector(repo, case):
    _break(repo, case)
    main, feature = repo.run("human", [push("HEAD:main"), push("HEAD:refs/heads/feature")])
    unknown(main, "refs/heads/main", T18[case])
    allowed(feature)


# --- T-19/T-19a: synthetic stdin -------------------------------------------------
def rec(dst, src="refs/heads/x", old="a" * 40, new="0" * 40):
    return f"{src} {old} {dst} {new}\n"


MALFORMED = [
    ("fewer than three spaces", "zq9 " + "a" * 40 + " refs/heads/main\n"),
    ("empty field", "zq9 " + "a" * 40 + " refs/heads/main \n"),
    ("object id is not 40 or 64 lowercase hex", rec("refs/heads/main", "zq9", "A" * 40)),
    ("object id is not 40 or 64 lowercase hex", rec("refs/heads/main", "zq9", new="g" * 40)),
    ("object ids differ in length", rec("refs/heads/main", "zq9", "a" * 64)),
    ("tab, CR or NUL", rec("refs/heads/main", "zq9\tx")),
    ("tab, CR or NUL", rec("refs/heads/main", "zq9")[:-1] + "\r\n"),
    ("tab, CR or NUL", rec("refs/heads/main", "zq9\0x")),
    ("blank line", "\n"),
    ("destination is not a refs/ name", rec("heads/main", "zq9")),
]


def _malformed_line(n, why):
    return f"{P} L2-MALFORMED: git sent pre-push record {n} that this hook cannot read ({why}); the whole push was refused.\n"


def _direct_steps(repo):
    inputs = [rec("refs/heads/feature") + bad for _, bad in MALFORMED]
    inputs.append(rec("refs/heads/main") + MALFORMED[0][1])  # T-19a
    inputs.append(rec("refs/heads/feature") + rec("refs/heads/main")[:-1])  # no final LF
    inputs.append(rec("refs/heads/feature") * 300 + rec("refs/heads/main"))  # > 4096 bytes
    steps = []
    for i, data in enumerate(inputs):
        path = repo.tmp / f"stdin-{i}"
        path.write_bytes(data.encode())
        steps.append(f"{q(repo.hook)} origin {q(repo.remote)} < {q(path)}")
    return steps


@pytest.mark.parametrize("actor", ["governed", "unknown"])
def test_t19_t19a_malformed_stdin(repo, actor):
    results = repo.run(actor, _direct_steps(repo))
    for (why, _), r in zip(MALFORMED, results):
        assert (r.rc, r.err) == (2, _malformed_line(2, why))
        assert "zq9" not in r.err
    first_protected, no_lf, chunked = results[len(MALFORMED):]
    assert (first_protected.rc, first_protected.err) == (2, _malformed_line(2, MALFORMED[0][0]))
    for r in (no_lf, chunked):
        r.before = r.after  # direct hook runs push nothing
        refused(repo, actor, r, "refs/heads/main")


def test_t19_t19a_ordinary_never_reads_stdin(repo):
    process = subprocess.Popen(
        [str(repo.hook), "origin", str(repo.remote)],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        env=repo.env,
        cwd=repo.work,
    )
    try:
        process.stdin.write(rec("refs/heads/main").encode() + MALFORMED[0][1].encode())
        process.stdin.flush()
        assert process.wait(timeout=20) == 0  # stdin is still open
        assert process.stdout.read() == b"" and process.stderr.read() == b""
    finally:
        process.kill()
        process.stdin.close()
        process.wait()


# --- T-20: selector output shapes -------------------------------------------------
def test_t20_selector_lines_pinned_and_mapped(repo):
    assert repo.call("identify").stdout == '{"status": "ordinary"}\n'
    repo.root.chmod(0o770)
    try:
        assert repo.call("identify").stdout == '{"status": "unknown"}\n'
    finally:
        repo.root.chmod(0o700)

    def release(*_):
        (repo.root / "sessions/old").unlink()

    identify = f"bash {q(repo.selector)} identify"
    governed, released = repo.run("governed", [identify, GATE, identify], actions=[release])
    assert governed.out == '{"status": "governed", "session_id": "old"}\n'
    assert released.out == '{"status": "ordinary", "reason": "released"}\n'
    session = repo.root / "sessions/old"
    session.write_text("worktree\n")
    session.chmod(0o600)
    (stale_line,) = repo.run("unknown", [identify])
    record = repo.last_record
    assert stale_line.out == f'{{"status": "unknown", "reason": "stale", "record": "{record}"}}\n'

    mapping = [
        ('{"status": "ordinary"}\n', None),
        (released.out, None),
        (governed.out, "governed"),
        ('{"status": "unknown"}\n', "identity unknown"),
        (stale_line.out, f"job record stale at {record}"),
        ('{"status": "unknown", "reason": "orphaned", "record": "/r/1.json"}\n', "job record orphaned at /r/1.json"),
        ('{"status": "unknown", "reason": "foreign", "record": "/r/1.json"}\n', "job record foreign at /r/1.json"),
        ('{"status":"ordinary"}\n', "identity unknown"),
        ('{"status": "ordinary"}', "identity unknown"),
        ('{"status": "ordinary"}\n{"status": "ordinary"}\n', "identity unknown"),
        ('{"status": "governed", "session_id": "../x"}\n', "identity unknown"),
        ('{"status": "unknown", "reason": "bogus", "record": "/r/1.json"}\n', "identity unknown"),
        ('{"status": "unknown", "reason": "stale", "record": "/r/a\'b.json"}\n', "identity unknown"),
        ('{"status": "unknown", "reason": "stale", "record": "r/1.json"}\n', "identity unknown"),
        ("", "identity unknown"),
    ]
    steps, actions = [], []
    for output, _ in mapping:
        actions.append(lambda *_, o=output: (repo.reset(), repo.stub(o)))
        steps += [GATE, push("HEAD:main")]
    results = repo.run("human", steps, actions=actions)
    for (output, expect), r in zip(mapping, results):
        if expect is None:
            allowed(r)
            assert r.before != r.after
            continue
        if expect == "governed":
            protected(r, "refs/heads/main")
            continue
        reason = re.match(r"job record (\w+) at (.*)$", expect)
        tail = ""
        if reason and reason.group(1) == "stale":
            tail = stale(reason.group(2))[1]
        elif reason:
            tail = KEPT
        unknown(r, "refs/heads/main", expect, tail)


# --- T-21/T-22: hardened selector call and pinned HOME ----------------------------
def _hostile(repo, variant, ref):
    mark = repo.tmp / "marker"
    line = '{"status": "ordinary"}'
    body = f"touch {q(mark)}; echo {q(line)}"
    stubs = repo.tmp / "stubs"
    stubs.mkdir(exist_ok=True)
    python = stubs / "python"
    python.write_text(f"#!/bin/sh\n{body}\n")
    python.chmod(0o755)
    command = push("HEAD:" + ref)
    if variant == "a-bash-env":
        env_file = stubs / "bash_env"
        env_file.write_text(f"timeout() {{ {body}; }}\n")
        return mark, f"env BASH_ENV={q(env_file)} {command}"
    if variant == "b-bash-func":
        funcs = [f"BASH_FUNC_{name}%%=() {{ {body}; }}" for name in ("timeout", "exec", "uv")]
        return mark, shlex.join(["env", *funcs]) + " " + command
    if variant == "c-uv-env":
        (stubs / "uv.toml").write_text("# stub\n")
        (stubs / "xdg/uv").mkdir(parents=True, exist_ok=True)
        (stubs / "xdg/uv/uv.toml").write_text("# stub\n")
        return mark, (
            f"env UV_PYTHON={q(python)} UV_CONFIG_FILE={q(stubs / 'uv.toml')} "
            f"XDG_CONFIG_HOME={q(stubs / 'xdg')} {command}"
        )
    (repo.work / "uv.toml").write_text("# stub\n")
    (repo.work / ".python-version").write_text(f"{python}\n")
    (repo.work / ".venv/bin").mkdir(parents=True, exist_ok=True)
    shutil.copy(python, repo.work / ".venv/bin/python")
    return mark, command


@pytest.mark.parametrize("variant", ["a-bash-env", "b-bash-func", "c-uv-env", "d-worktree-uv"])
@pytest.mark.parametrize("branch", BRANCHES)
@pytest.mark.parametrize("actor", ["governed", "human"])
def test_t21_hardened_selector_call(repo, actor, branch, variant):
    mark, step = _hostile(repo, variant, branch)
    (r,) = repo.run(actor, [step])
    if actor == "governed":
        protected(r, "refs/heads/" + branch)
    else:
        allowed(r)
    assert not mark.exists()


@pytest.mark.parametrize("branch", BRANCHES)
@pytest.mark.parametrize("actor", ["governed", "human"])
def test_t22_pusher_home_elsewhere(repo, actor, branch):
    empty = repo.tmp / "empty-home"
    empty.mkdir()
    (r,) = repo.run(actor, [f"env HOME={q(empty)} " + push("HEAD:" + branch)])
    if actor == "governed":
        protected(r, "refs/heads/" + branch)
    else:
        allowed(r)


# --- T-23/T-24: packaging pin and bypass-free diagnostics -------------------------
def test_t23_hook_sha256_pinned_with_version_line():
    pins = (REPO / "tests/cli/test_install_hooks.py").read_text()
    version = re.search(r'^L2_VERSION_LINE = "(.*)"$', pins, re.M).group(1)
    sha = re.search(r'^L2_HOOK_SHA256 = "([0-9a-f]{64})"$', pins, re.M).group(1)
    assert HOOK.read_text().splitlines()[1] == version
    assert hashlib.sha256(HOOK.read_bytes()).hexdigest() == sha


def test_t24_no_bypass_hint_in_any_refusal(repo):
    stub_lines = [
        '{"status": "governed", "session_id": "old"}\n',
        '{"status": "unknown"}\n',
        '{"status": "unknown", "reason": "stale", "record": "/r/1.json"}\n',
        '{"status": "unknown", "reason": "unreadable", "record": "/r/1.json"}\n',
    ]
    steps, actions = [], []
    for output in stub_lines:
        actions.append(lambda *_, o=output: repo.stub(o))
        steps += [GATE, push("HEAD:main")]
    actions.append(lambda *_: repo.data.unlink())
    steps += [GATE, push("HEAD:master")]
    results = repo.run("human", steps, actions=actions)
    repo.write_data(f"{repo.home}\n{os.path.dirname(UV)}\n")
    repo.stub(stub_lines[0])
    malformed = subprocess.run(
        [str(repo.hook), "origin", "x"],
        input=rec("refs/heads/x") + "\n",
        env=repo.env,
        capture_output=True,
        text=True,
        timeout=20,
    )
    errors = [r.err for r in results] + [malformed.stderr]
    assert all(P in err for err in errors) and malformed.returncode == 2
    for err in errors:
        for line in err.splitlines():
            assert not BYPASS.search(line), line
    spec = importlib.util.spec_from_file_location("orca_worktree_t24", ORCA)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module  # dataclasses need it
    try:
        spec.loader.exec_module(module)
    finally:
        del sys.modules[spec.name]
    for code, text in module.REMEDY.items():
        assert not BYPASS.search(text), code


@pytest.mark.skip(reason="Task 7: FR-045 W-L2-ABSENT remedy text is not written yet")
def test_t24_fr045_remedy_text():
    spec = importlib.util.spec_from_file_location("orca_worktree_t24b", ORCA)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    text = module.REMEDY["W-L2-ABSENT"]
    assert "not built yet" not in text and not BYPASS.search(text)


@pytest.mark.skip(reason="Task 8: the fixture places the hook by install_l2 instead of a test-local copy")
def test_hook_placed_by_install_l2():
    raise AssertionError("Task 8")


# --- FR-101: expected L2 leaks, named by LIM ID ----------------------------------
LEAKS = {
    "LIM-4 --no-verify": push("--no-verify", "HEAD:main"),
    "LIM-4 -c core.hooksPath": "git -c core.hooksPath=/dev/null push origin HEAD:main",
    "LIM-4 --config-env": "env HP=/dev/null git --config-env=core.hooksPath=HP push origin HEAD:main",
    "LIM-4 GIT_CONFIG_COUNT": (
        "env GIT_CONFIG_COUNT=1 GIT_CONFIG_KEY_0=core.hooksPath "
        "GIT_CONFIG_VALUE_0=/dev/null " + push("HEAD:main")
    ),
    "LIM-6 config.worktree hooksPath": push("HEAD:main"),
    "LIM-7 git send-pack": None,
}


@pytest.mark.parametrize("lim", list(LEAKS))
def test_fr101_bypass_reaches_remote_under_governed_actor(repo, lim):
    cwd = None
    step = LEAKS[lim]
    if lim.startswith("LIM-6"):
        cwd = repo.worktree()
        repo.git("config", "extensions.worktreeConfig", "true")
        repo.g("-C", cwd, "config", "--worktree", "core.hooksPath", "/dev/null")
    if step is None:
        step = f"git send-pack {q(repo.remote)} refs/heads/feature:refs/heads/main"
    (r,) = repo.run("governed", [step], cwd=cwd)
    # Expected leak: a future fix that closes it flips this pin.
    assert r.rc == 0 and P not in r.err, f"{lim}: {r.err}"
    assert r.before != r.after and repo.remote_ref("main") == repo.b, lim

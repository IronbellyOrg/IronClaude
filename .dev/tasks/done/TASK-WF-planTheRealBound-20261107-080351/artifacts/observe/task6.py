"""Task 6: same-worktree human-style pushes against governed pushes in a disposable bare repository.

Run: uv run --no-project python -I artifacts/observe/task6.py
No real Claude run is spent. The governed pusher is a job started through the helper's own prepare and run
actions under a governed session record in the throwaway HOME; the plain shell is started by this runner. Both
are labelled controlled. Pushes go only to a bare repository in a temporary directory, never to a real remote.
"""

import sys

sys.dont_write_bytecode = True

import json  # noqa: E402
import shlex  # noqa: E402
import subprocess  # noqa: E402
import time  # noqa: E402
import uuid  # noqa: E402
from pathlib import Path  # noqa: E402

sys.path.insert(0, str(Path(__file__).resolve().parent))
import observe as ob  # noqa: E402

ART = ob.ART
HOOK = """#!/bin/bash
# Log-only pre-push hook: records the selector status of the pushing process and each destination ref, then allows the push.
LOG={log}; H={helper}
ts_in=$(date +%s.%N)
id=$(/bin/bash "$H" identify)
sleep 1
ts_out=$(date +%s.%N)
while read -r lref lsha rref rsha; do
  printf '{{"identity":%s,"remote_ref":"%s","local_sha":"%s","remote_sha":"%s","hook_in":%s,"hook_out":%s}}\\n' "$id" "$rref" "$lsha" "$rsha" "$ts_in" "$ts_out" >> "$LOG"
done
exit 0
"""
PUSH = """#!/bin/bash
cd {wt} || exit 90
{wait}git push -q origin {sha}:refs/heads/{branch}
echo $? > {exitfile}
"""


class Fixture:
    def __init__(self, g):
        self.g = g
        self.bare, self.clone, self.wt = g.tmp / "bare.git", g.tmp / "clone", g.tmp / "wt"
        self.log = g.tmp / "pre-push-log.jsonl"
        self.env = dict(g.git_env(), GIT_AUTHOR_NAME="obs", GIT_AUTHOR_EMAIL="obs@example.invalid", GIT_COMMITTER_NAME="obs", GIT_COMMITTER_EMAIL="obs@example.invalid")
        self.empty_template = g.tmp / "empty-template"

    def git(self, *args, cwd=None, check=True):
        r = subprocess.run(["git", *args], cwd=cwd or self.clone, env=self.env, capture_output=True, text=True, timeout=60)
        if check and r.returncode:
            raise SystemExit("git %s failed: %s" % (args[0], r.stderr[:200]))
        return r

    def setup(self):
        self.empty_template.mkdir()
        self.git("init", "-q", "--bare", "--template=" + str(self.empty_template), str(self.bare), cwd=self.g.tmp)
        self.git("clone", "-q", "--template=" + str(self.empty_template), str(self.bare), str(self.clone), cwd=self.g.tmp)
        self.git("commit", "-q", "--allow-empty", "-m", "A")
        self.a = self.git("rev-parse", "HEAD").stdout.strip()
        self.git("push", "-q", "origin", self.a + ":refs/heads/main", self.a + ":refs/heads/master")  # seed before the hook exists
        self.git("worktree", "add", "-q", "--detach", str(self.wt))
        hook = self.clone / ".git/hooks/pre-push"
        hook.parent.mkdir(exist_ok=True)
        hook.write_text(HOOK.format(log=shlex.quote(str(self.log)), helper=shlex.quote(str(ob.HELPER))))
        hook.chmod(0o755)

    def commit(self, parent, msg):
        tree = self.git("rev-parse", parent + "^{tree}").stdout.strip()
        return self.git("commit-tree", tree, "-p", parent, "-m", msg).stdout.strip()

    def refs(self):
        out = self.git("for-each-ref", "--format=%(refname) %(objectname)", "refs/heads", cwd=self.bare).stdout.split()
        return dict(zip(out[::2], out[1::2]))

    def script(self, name, sha, branch, go=None):
        exitfile = self.g.tmp / (name + ".exit")
        wait = ('while [ ! -e %s ]; do sleep 0.02; done\n' % shlex.quote(str(go))) if go else ""
        path = self.g.tmp / (name + ".sh")
        path.write_text(PUSH.format(wt=shlex.quote(str(self.wt)), wait=wait, sha=sha, branch=branch, exitfile=shlex.quote(str(exitfile))))
        return path, exitfile

    def human(self, name, sha, branch, go=None):
        path, exitfile = self.script(name, sha, branch, go)
        return self.g.spawn(["/bin/bash", str(path)], name, env=self.env), exitfile

    def governed(self, name, sha, branch, sid, go=None):
        path, exitfile = self.script(name, sha, branch, go)
        token = subprocess.run(["/bin/bash", str(ob.HELPER), "prepare", sid, "/bin/bash " + shlex.quote(str(path))], env=self.env, capture_output=True, text=True, timeout=30).stdout.strip()
        return self.g.spawn(["/bin/bash", str(ob.HELPER), "run", token], name, env=self.env), exitfile


def wait_all(procs, limit=60):
    end = time.time() + limit
    for mp, _ in procs:
        while mp.p.poll() is None and time.time() < end:
            time.sleep(0.05)


def hook_rows(fx):
    rows = []
    if fx.log.exists():
        for line in fx.log.read_text().splitlines():
            try:
                rows.append(json.loads(line))
            except ValueError:
                pass
    return rows


def push_entry(fx, name, actor, phase, sha, branch, before, after, exitfile):
    row = next((r for r in hook_rows(fx) if r["local_sha"] == sha), None)
    ident = (row or {}).get("identity", {})
    return {"name": name, "label": "controlled", "actor_started_from": actor, "phase": phase,
            "reason": ("a plain shell started by the runner, not a person at a terminal, so a controlled human-style shell" if actor.startswith("plain")
                       else "a job started through the helper's own prepare and run actions under a governed session record in the throwaway HOME"),
            "destination_ref_logged_by_hook": (row or {}).get("remote_ref"), "destination_ref_pushed": "refs/heads/" + branch,
            "selector_status_logged_by_hook": ident.get("status"), "selector_session_id_logged_by_hook": ident.get("session_id"),
            "pushed_commit": sha, "push_exit_status": int(exitfile.read_text().strip()) if exitfile.exists() else None,
            "bare_refs_before": before, "bare_refs_after": after, "hook_interval_seconds": [row["hook_in"], row["hook_out"]] if row else None}


def main():
    runner = ob.Runner()
    g = ob.Group.create("t6")
    out = {"task": 6, "label": "controlled", "controlled_baseline": "tests/hooks/test_launch_job_identity.py:1291-1354 (human push at :1306-1331, refused governed push at :1347-1348)",
           "why_controlled": "the plain shell and the governed job were both started by this runner; no real Claude, Orca or person pushed. The log-only hook vetoes nothing, so every push reaches the bare repository."}
    try:
        fx = Fixture(g)
        fx.setup()
        sid = str(uuid.uuid4())
        g.make_governed(sid)
        b1, c1 = fx.commit(fx.a, "B1"), fx.commit(fx.a, "C1")
        b2, c2 = fx.commit(b1, "B2"), fx.commit(c1, "C2")
        pushes = []
        # Phase 1: one push at a time.
        t0 = ob.now()
        before = fx.refs()
        h, ex = fx.human("p1-human-main", b1, "main")
        wait_all([(h, ex)])
        after = fx.refs()
        pushes.append(push_entry(fx, "p1-human-main", "plain shell started by the runner", "sequential", b1, "main", before, after, ex))
        before = fx.refs()
        gv, ex = fx.governed("p2-governed-master", c1, "master", sid)
        wait_all([(gv, ex)])
        after = fx.refs()
        pushes.append(push_entry(fx, "p2-governed-master", "governed job started through the helper's run action", "sequential", c1, "master", before, after, ex))
        # Phase 2: the human-style push to main and the governed push to master at the same time in the same worktree.
        go = g.tmp / "go"
        before = fx.refs()
        h, hex_ = fx.human("p3-human-main-concurrent", b2, "main", go)
        gv, gex = fx.governed("p4-governed-master-concurrent", c2, "master", sid, go)
        time.sleep(2.5)  # both jobs are waiting at the barrier
        go.touch()
        wait_all([(h, hex_), (gv, gex)])
        after = fx.refs()
        pushes.append(push_entry(fx, "p3-human-main-concurrent", "plain shell started by the runner", "concurrent", b2, "main", before, after, hex_))
        pushes.append(push_entry(fx, "p4-governed-master-concurrent", "governed job started through the helper's run action", "concurrent", c2, "master", before, after, gex))
        out["pushes"] = pushes
        iv = [p["hook_interval_seconds"] for p in pushes if p["phase"] == "concurrent"]
        overlap = bool(len(iv) == 2 and all(iv) and max(iv[0][0], iv[1][0]) < min(iv[0][1], iv[1][1]))
        out["concurrent_run"] = {
            "same_worktree": True, "hook_invocations_overlapped_in_time": overlap,
            "statuses_logged": {p["name"]: p["selector_status_logged_by_hook"] for p in pushes if p["phase"] == "concurrent"},
            "different_statuses_logged": len({p["selector_status_logged_by_hook"] for p in pushes if p["phase"] == "concurrent"}) == 2,
            "human_push_reached_the_bare_repository": fx.refs().get("refs/heads/main") == b2,
            "governed_push_reached_the_bare_repository": fx.refs().get("refs/heads/master") == c2,
            "bare_refs_final": fx.refs()}
        remotes = fx.git("remote", "-v").stdout.replace(str(fx.bare), "<tmp>/bare.git").strip().splitlines()
        out["fixture"] = {"git_remote_listing": remotes, "remote_names": sorted({ln.split()[0] for ln in remotes}),
                          "hooks_installed_in_fixture_clone": sorted(p.name for p in (fx.clone / ".git/hooks").iterdir()),
                          "template_used_for_init_and_clone": "an empty template directory, so no sample hooks exist",
                          "hook_only_in_temporary_directory": str((fx.clone / ".git/hooks/pre-push").resolve()).startswith(str(g.tmp.resolve())),
                          "git_config_isolation": "GIT_CONFIG_NOSYSTEM=1 and GIT_CONFIG_GLOBAL=/dev/null for both actors; HOME is the throwaway HOME"}
        out["orca_terminal_human_case"] = {
            "result": "unavailable",
            "missing_interface": "a person's interactive terminal inside an Orca-managed worktree: the runner has no authorized interface to start an Orca terminal as a person would, and starting one would create terminals in the user's real Orca"}
        runner.log(run_id=ob.new_rid(), case_id="t6-pushes", label="task6: sequential and concurrent human-style and governed pushes to a disposable bare repository (controlled)",
                   group="t6", start=t0, end=ob.now(), exit=0, real_claude=False, depth=None, result="controlled",
                   extra={"pushes": len(pushes), "overlap": overlap, "statuses": [p["selector_status_logged_by_hook"] for p in pushes]})
    finally:
        out["teardown"] = g.teardown("task6")
        (ob.GROUPS / "t6.json").unlink()
    (ART / "human-vs-governed-push.json").write_text(json.dumps(out, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"statuses": [(p["name"], p["selector_status_logged_by_hook"], p["push_exit_status"]) for p in out["pushes"]],
                      "concurrent": out["concurrent_run"], "teardown": out["teardown"]}, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())

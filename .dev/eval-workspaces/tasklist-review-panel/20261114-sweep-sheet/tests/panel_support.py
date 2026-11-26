"""Set-up of the launcher tests (Task 27): a sandbox built by bin/build-sandbox.sh over F-REPO, a values file, one run.

Every test that starts bin/run-panel.sh takes the fake claude first on PATH from the tmp_roots fixture (conftest.py).
"""

import json
import shutil
import subprocess
from types import SimpleNamespace

from helpers import SW

from fixtures.repos.build_repo import DOC_ID, OTHER_DOC_ID, build_repo

PLANS = SW / "fixtures" / "plans"
RUN_PANEL = SW / "bin" / "run-panel.sh"
RUN_REVIEWER = SW / "bin" / "run-reviewer.sh"
BUILD_SANDBOX = SW / "bin" / "build-sandbox.sh"
PRIMARY = {"t2b-1": "muse-ember-1.0", "t4-1": "gpt-6-luna", "t3-1": "gpt-6-luna"}
RIDS = tuple(PRIMARY)
EMBER = "muse-ember-1.0"
# an anchor that is a flattened substring of fixtures/plans/p_basic.md and holds none of the words that the blindness test looks for
ANCHOR = "returns an empty result for an empty report"


def make_world(roots, *, plan="p_basic.md", source=True, b=100):
    """Build F-REPO, the candidate (and source) inside it, packages.json and values.json, then the sandbox (S0).

    Returns a namespace with: doc, repo, sandbox, cand, packages, values, roots, run (see run()).
    """
    built = build_repo(roots.root, doc_id=DOC_ID)
    cand_dir = built.repo / ".dev" / "eval-workspaces" / "cand"
    cand_dir.mkdir(parents=True)
    shutil.copy(PLANS / plan, cand_dir / "candidate.md")
    src_rel = None
    if source:
        shutil.copy(PLANS / "source.md", cand_dir / "source.md")
        src_rel = ".dev/eval-workspaces/cand/source.md"
    entry = {
        "kind": "plan",
        "set": "control",
        "base": built.base,
        "candidate": ".dev/eval-workspaces/cand/candidate.md",
        "source": src_rel,
        "masked_paths": [built.added, built.edited],
    }
    packages = roots.root / "packages.json"
    packages.write_text(
        json.dumps(
            {
                "schema": "sweep-packages/1",
                "packages": {DOC_ID: entry, OTHER_DOC_ID: dict(entry, set="other")},
            }
        )
    )
    values = roots.root / "values.json"
    v = json.loads((SW / "config" / "values.json").read_text())
    for panel in v["b"]:
        v["b"][panel][DOC_ID] = b
    values.write_text(json.dumps(v))
    world = SimpleNamespace(
        doc=DOC_ID,
        repo=built.repo,
        sandbox=roots.sb / DOC_ID / "repo",
        cand=roots.sb / "cand" / DOC_ID,
        packages=packages,
        values=values,
        roots=roots,
    )
    r = subprocess.run(
        ["bash", str(BUILD_SANDBOX), "--packages", str(packages), DOC_ID],
        capture_output=True,
        text=True,
        env=roots.with_env(SW_SRC_REPO=str(built.repo)),
    )
    assert r.returncode == 0, r.stderr
    world.run = lambda arm, name, **kw: run_panel(world, arm, name, **kw)
    return world


def run_panel(world, arm, name, *, panel="primary", env=None, args=(), timeout=180):
    """Run bin/run-panel.sh into roots.runs/<name>. Returns a CompletedProcess with .dir, .json(name) and .calls()."""
    roots = world.roots
    run_dir = roots.runs / name
    cmd = [
        "bash",
        str(RUN_PANEL),
        "--arm",
        arm,
        "--panel",
        panel,
        "--doc",
        world.doc,
        "--run",
        str(run_dir),
        "--seed",
        "1",
        "--values",
        str(world.values),
        "--packages",
        str(world.packages),
        *args,
    ]
    e = roots.with_env(SW_SRC_REPO=str(world.repo), **(env or {}))
    r = subprocess.run(cmd, capture_output=True, text=True, env=e, timeout=timeout)
    r.dir = run_dir
    r.json = lambda rel: json.loads((run_dir / rel).read_text())
    r.calls = lambda: call_log(roots)
    return r


def call_log(roots):
    """FAKE_CALL_LOG as a list of (epoch, scenario, model)."""
    if not roots.call_log.exists():
        return []
    rows = [ln.split("\t") for ln in roots.call_log.read_text().splitlines()]
    return [(float(t), s, m) for t, s, m in rows]


def brief_shas(run_dir):
    """{rid: sha256 of the brief} from briefs/<rid>.sha256."""
    return {
        p.stem: p.read_text().strip()
        for p in sorted((run_dir / "briefs").glob("*.sha256"))
    }

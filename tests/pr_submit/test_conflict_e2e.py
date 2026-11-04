"""End-to-end conflict scenarios X1 to X3 (design section 12.4).

Each test plays the SKILL through one conflict cycle with real git inside a pytest
temporary directory: a local bare repository is ``origin``, a ``gh`` stub first on
``PATH`` records every call and serves canned JSON, and the four skill scripts run
from their source path. The deterministic core decides every step
(``superclaude.pr_submit.conflicts``, ``fsm``, ``ci``, ``run_log``), exactly in the
order of ``refs/conflict-mechanical.md`` (design section 4.6, steps 0 to 13).

- X1: Tier 1 at Wave 8a with real ``uv`` (``UV_OFFLINE=1``, ``UV_NO_CONFIG=1``,
  ``UV_CACHE_DIR=<tmp>``); skipped only when ``uv`` is absent. The lock fixture is a
  zero-dependency project, so an offline ``uv lock`` resolves without the network.
- X2: the same scenario with a stub ``uv`` on ``PATH``; it always runs.
- X3: Tier 2 at C-initial with a scripted resolution, plus the rejected ``semantic``
  variant.

``GIT_CONFIG_GLOBAL=/dev/null``, ``GIT_CONFIG_NOSYSTEM=1`` and a fixed author and
committer come from ``make_repos`` (reused from ``test_conflict_scripts``); ``HOME``
points into the temporary directory. Nothing here touches the network or the
operator's ``~/.claude``.
"""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

from superclaude.pr_submit.ci import expect_checks_after_push
from superclaude.pr_submit.conflicts import (
    conflict_action,
    conflict_attempt,
    conflict_cycle_id,
    conflict_plan,
    conflict_validation_status,
    evaluate_sync_decision,
    finish_manifest,
    merge_commit_message,
    merge_parent_ok,
    merge_preflight_ok,
    mergeability_hint,
    needs_probe,
    parse_probe,
    parse_resolution_record,
    prior_conflict_cycles,
    resolution_record_ok,
)
from superclaude.pr_submit.fsm import (
    DEFAULT_MAX_ROUNDS,
    build_push_triad,
    pr_head_ok,
    should_retrigger,
    transition,
)
from superclaude.pr_submit.models import MonitorState
from superclaude.pr_submit.run_log import RunLog
from tests.pr_submit.test_conflict_scripts import (
    EVIDENCE,
    FINISH,
    GIT,
    POLL_CI,
    PROBE,
    ProbeRun,
    Repos,
    _merge_tree_works,
    make_repos,
)

# Module-level capability skip (the same check as Task 10's): only when
# `git merge-tree --write-tree HEAD HEAD` works in a scratch repository.
pytestmark = pytest.mark.skipif(
    not _merge_tree_works(),
    reason="git merge-tree --write-tree (or jq) is not available here",
)

PR_NUMBER = 7
HEAD_BRANCH = "pr"
BASE = "main"
BASE_REF = f"origin/{BASE}"
RUN_ID = "run-e2e"
ATTRIBUTION = "\nCo-Authored-By: E2E Session <e2e-session@example.com>\n"
EVIDENCE_FILES = [
    "stage1",
    "stage2",
    "stage3",
    "worktree",
    "log.txt",
    "diff-ours.txt",
    "diff-theirs.txt",
]

# ---------------------------------------------------------------------------
# Shared helpers
# ---------------------------------------------------------------------------


def _run(
    argv: list[str], cwd: Path, env: dict[str, str], timeout: int = 120
) -> subprocess.CompletedProcess:
    return subprocess.run(
        argv, cwd=cwd, env=env, text=True, capture_output=True, timeout=timeout
    )


def git_rc(repos: Repos, *args: str) -> subprocess.CompletedProcess:
    return _run([GIT, *args], repos.work, repos.env)


def run_script(repos: Repos, script: Path, *args: str) -> ProbeRun:
    res = _run([str(script), *args], repos.work, repos.env)
    return ProbeRun(res.returncode, res.stdout, res.stderr)


_GH_STUB = """#!/usr/bin/env bash
printf '%s\\n' "$*" >> '@CALLS@'
case "$1 $2" in
  "pr view") cat '@PR_VIEW@' ;;
  "repo view")
    printf '%s\\n' \\
      '{"mergeCommitAllowed":true,"rebaseMergeAllowed":true,"squashMergeAllowed":true}' ;;
  "api repos/"*"/check-runs?per_page=1") printf '1\\n' ;;
  "api repos/"*"/status") printf '0\\n' ;;
  *) printf 'unexpected gh call: %s\\n' "$*" >&2; exit 1 ;;
esac
"""


def install_gh_stub(repos: Repos) -> Path:
    """Replace the recording `gh` stub with one that also serves the reads a
    conflict cycle makes: `gh pr view` (from a JSON file the test rewrites),
    `gh repo view` and the two commit-scoped check counts (1 check run, 0
    statuses). Any other call is recorded, then fails."""
    pr_view = repos.root / "gh-pr-view.json"
    stub = repos.bin_dir / "gh"
    stub.write_text(
        _GH_STUB.replace("@CALLS@", str(repos.gh_calls)).replace(
            "@PR_VIEW@", str(pr_view)
        ),
        encoding="utf-8",
    )
    stub.chmod(0o755)
    return pr_view


def set_pr_view(repos: Repos, head_oid: str) -> None:
    (repos.root / "gh-pr-view.json").write_text(
        json.dumps(
            {
                "baseRefName": BASE,
                "mergeable": "CONFLICTING",
                "mergeStateStatus": "DIRTY",
                "headRefName": HEAD_BRANCH,
                "headRefOid": head_oid,
                "isCrossRepository": False,
            }
        )
        + "\n",
        encoding="utf-8",
    )


def gh(repos: Repos, *args: str) -> dict:
    res = _run(["gh", *args], repos.work, repos.env)
    assert res.returncode == 0, res.stderr
    return json.loads(res.stdout)


def gh_pr_view(repos: Repos, fields: str) -> dict:
    return gh(
        repos, "pr", "view", str(PR_NUMBER), "--repo", repos.repo_slug, "--json", fields
    )


def assert_no_retrigger_call(repos: Repos) -> None:
    """Every recorded `gh` call is a read; nothing posted a re-trigger comment."""
    calls = repos.gh_call_lines()
    assert calls, "the gh stub saw no call at all"
    allowed = ("pr view ", "repo view ", f"api repos/{repos.repo_slug}/commits/")
    for line in calls:
        assert line.startswith(allowed), f"unexpected gh call: {line}"
        for token in ("comment", "/issues/", "--method", " -X ", " -f ", "--field"):
            assert token not in line, f"a write-shaped gh call: {line}"


def publish_pr(repos: Repos) -> str:
    """The PR head as GitHub has it: the PR branch published on origin."""
    repos.git(repos.work, "push", "-q", "origin", f"{HEAD_BRANCH}:{HEAD_BRANCH}")
    return repos.git(repos.work, "rev-parse", "HEAD").strip()


def origin_tip(repos: Repos) -> str:
    return repos.git(repos.origin, "rev-parse", f"refs/heads/{HEAD_BRANCH}").strip()


def parents_of(repos: Repos, cwd: Path, sha: str) -> list[str]:
    return repos.git(cwd, "rev-list", "--parents", "-n", "1", sha).split()[1:]


def head_check(repos: Repos, view: dict, pre_push_sha: str) -> None:
    """Step 1: the checkout is bound to the PR head."""
    local_branch = repos.git(repos.work, "rev-parse", "--abbrev-ref", "HEAD").strip()
    local_head = repos.git(repos.work, "rev-parse", "HEAD").strip()
    assert pr_head_ok(
        local_branch,
        local_head,
        view["headRefName"],
        view["headRefOid"],
        view["isCrossRepository"],
    )
    assert view["headRefName"] == HEAD_BRANCH
    assert local_head == pre_push_sha
    assert HEAD_BRANCH != view["baseRefName"]


def fresh_probe(repos: Repos, hint: str):
    """Step 2: the one probe of the cycle; the core plans from it."""
    res = run_script(
        repos, PROBE, "--repo", repos.repo_slug, "--base", BASE, "--program", "uv"
    )
    assert res.returncode == 0, res.stderr
    payload = res.payload
    probe = parse_probe(payload)
    assert probe.foreign_op is None
    assert merge_preflight_ok(probe.status_porcelain) == (True, [])
    return probe, conflict_plan(hint=hint, probe=payload)


def write_sync_started(
    run_log: RunLog,
    *,
    cycle_id: str,
    tier: int,
    kind: str,
    hook: str,
    plan,
    pre_push_sha: str,
    conflict_max_tier: int,
    review_terminal: str | None,
) -> None:
    """Step 3: the write-ahead record, before the merge command."""
    run_log.write_ahead(
        {
            "event_type": "sync_started",
            "run_id": RUN_ID,
            "cycle_id": cycle_id,
            "tier": tier,
            "kind": kind,
            "hook": hook,
            "base_ref": BASE_REF,
            "base_sha": plan.base_sha,
            "pre_push_sha": pre_push_sha,
            "merge_tree_oid": plan.merge_tree_oid,
            "conflict_max_tier": conflict_max_tier,
            "review_terminal": review_terminal,
            "paths": [p.path for p in plan.paths],
            "resumed": False,
        }
    )


def merge_by_sha(repos: Repos, base_sha: str) -> list[str]:
    """Step 4: merge the recorded base tip by SHA; return the unmerged paths."""
    res = git_rc(
        repos,
        "-c",
        "merge.conflictStyle=zdiff3",
        "-c",
        "rerere.enabled=false",
        "merge",
        "--no-commit",
        "--no-ff",
        base_sha,
    )
    assert res.returncode == 1, (res.stdout, res.stderr)
    merge_head = repos.git(repos.work, "rev-parse", "-q", "--verify", "MERGE_HEAD")
    assert merge_head.strip() == base_sha
    return repos.git(repos.work, "diff", "--name-only", "--diff-filter=U").splitlines()


def finish_commit(
    repos: Repos, sync_dir: Path, plan, resolved: list[str], message: str
) -> dict:
    """Step 9: message file, manifest and the finish gate (the one commit)."""
    sync_dir.mkdir(parents=True, exist_ok=True)
    message_file = sync_dir / "message.txt"
    message_file.write_text(message, encoding="utf-8")
    manifest = sync_dir / "manifest.txt"
    manifest.write_text(finish_manifest(plan.listing, resolved), encoding="utf-8")
    res = run_script(
        repos,
        FINISH,
        "--base-sha",
        plan.base_sha,
        "--merge-tree-oid",
        plan.merge_tree_oid,
        "--manifest",
        str(manifest),
        "--message-file",
        str(message_file),
    )
    assert res.returncode == 0, (res.stdout, res.stderr)
    return res.payload


def pre_push_guard(repos: Repos, *, pre_push_sha: str, target_sha: str, base_sha: str):
    """Step 10, in order: head re-read, parents, base ancestry; then the advisory."""
    # (a) the stored pre_push_sha, never the local HEAD (now the merge commit).
    view = gh_pr_view(repos, "headRefName,headRefOid,isCrossRepository")
    local_branch = repos.git(repos.work, "rev-parse", "--abbrev-ref", "HEAD").strip()
    assert pr_head_ok(
        local_branch,
        pre_push_sha,
        view["headRefName"],
        view["headRefOid"],
        view["isCrossRepository"],
    )
    assert view["headRefName"] == HEAD_BRANCH
    # (b) exactly [pre_push_sha, base_sha].
    parents = parents_of(repos, repos.work, target_sha)
    assert merge_parent_ok(parents, pre_push_sha, base_sha) is True
    # (c) the recorded base tip is still on the base branch.
    repos.git(repos.work, "fetch", "-q", "origin", BASE)
    ancestry = git_rc(repos, "merge-base", "--is-ancestor", base_sha, BASE_REF)
    assert ancestry.returncode == 0, ancestry.stderr
    # Advisory read before the first conflict push of the run (never halts).
    settings = gh(
        repos,
        "repo",
        "view",
        repos.repo_slug,
        "--json",
        "mergeCommitAllowed,rebaseMergeAllowed,squashMergeAllowed",
    )
    assert settings["mergeCommitAllowed"] is True


def check_evidence(repos: Repos, sha: str) -> int:
    res = run_script(repos, POLL_CI, "--evidence-sha", sha, "--repo", repos.repo_slug)
    assert res.returncode == 0, res.stderr
    assert res.payload["evidence_sha"] == sha
    return res.payload["evidence_checks"]


def decide_and_push(
    repos: Repos,
    run_log: RunLog,
    *,
    cycle_id: str,
    decision,
    push_kind: str,
    pre_push_sha: str,
    target_sha: str,
    base_sha: str,
    review_terminal: str | None,
) -> list[dict]:
    """Steps 11 and 12: the core DECIDES, the triad is written ahead, then the push."""
    assert decision.authorized is True
    assert decision.kind == push_kind
    expect_checks = expect_checks_after_push(
        checks_seen_this_run=False,
        pre_push_evidence=check_evidence(repos, pre_push_sha),
        base_evidence=check_evidence(repos, base_sha),
    )
    assert expect_checks is True  # the stub serves one check run per commit
    triad = build_push_triad(
        run_id=RUN_ID,
        cycle_id=cycle_id,
        round_counter=run_log.rebuild_state()["round_counter"],
        pre_push_sha=pre_push_sha,
        target_sha=target_sha,
        target_branch=HEAD_BRANCH,
        target_remote="origin",
        decision=decision,
        push_kind=push_kind,
        base_sha=base_sha,
        review_terminal=review_terminal,
        expect_checks=expect_checks,
    )
    run_log.append(triad[0])  # push_decision
    run_log.write_ahead(triad[1])  # push_initiated, fsynced before the push
    push = git_rc(repos, "push", "origin", f"{target_sha}:{HEAD_BRANCH}")
    assert push.returncode == 0, push.stderr
    run_log.append(triad[2])  # push_completed
    # Read the merge state once after the push (a BLOCKED state is only reported).
    set_pr_view(repos, target_sha)
    gh_pr_view(repos, "mergeStateStatus")
    return triad


def conclude(
    run_log: RunLog,
    cycle_id: str,
    outcome: str,
    *,
    merge_sha: str | None = None,
    record_path: str | None = None,
    dropped: list[str] | None = None,
    reason: str | None = None,
) -> None:
    run_log.append(
        {
            "event_type": "sync_concluded",
            "cycle_id": cycle_id,
            "outcome": outcome,
            "merge_sha": merge_sha,
            "record_path": record_path,
            "dropped": dropped or [],
            "reason": reason,
            "recovered": False,
        }
    )


def event_types(run_log: RunLog) -> list[str]:
    return [ev["event_type"] for ev in run_log.read_events()]


# ---------------------------------------------------------------------------
# X1 / X2: Tier 1 sync at Wave 8a (one root uv.lock conflict)
# ---------------------------------------------------------------------------

_PYPROJECT = """[project]
name = "demo"
version = "{version}"
description = "Hermetic merge-conflict fixture."
keywords = []
requires-python = "{requires}"
dependencies = []
"""


def _pyproject(version: str, requires: str) -> str:
    return _PYPROJECT.format(version=version, requires=requires)


def _lock(version: str, requires: str, trailer: str | None) -> str:
    text = (
        "version = 1\n"
        "revision = 3\n"
        f'requires-python = "{requires}"\n'
        "\n"
        "[[package]]\n"
        'name = "demo"\n'
        f'version = "{version}"\n'
        'source = { virtual = "." }\n'
    )
    return text if trailer is None else text + f"# {trailer}\n"


# The merged result: the PR's version, the base's requires-python. A stub `uv lock`
# writes exactly this; a real offline `uv lock` produces the same content.
FIXED_LOCK = _lock("0.2.0", ">=3.10", None)

TIER1_BASE_FILES = {
    "README.md": "readme\n",
    "pyproject.toml": _pyproject("0.1.0", ">=3.9"),
    "uv.lock": _lock("0.1.0", ">=3.9", "lock fixture"),
}
TIER1_PR_FILES = {
    "pyproject.toml": _pyproject("0.2.0", ">=3.9"),
    "uv.lock": _lock("0.2.0", ">=3.9", "lock hand-edited on the PR side"),
}
TIER1_BASE_ADVANCE = {
    "pyproject.toml": _pyproject("0.1.0", ">=3.10"),
    "uv.lock": _lock("0.1.0", ">=3.10", "lock hand-edited on the base side"),
}

_UV_STUB = """#!/usr/bin/env bash
printf '%s\\n' "$*" >> "$UV_STUB_CALLS"
case "$*" in
  "lock") cat -- "$UV_STUB_LOCK" > uv.lock ;;
  "lock --check")
    cmp -s -- "$UV_STUB_LOCK" uv.lock \\
      || { printf 'stub uv: uv.lock is not the fixed lock\\n' >&2; exit 1; } ;;
  *) printf 'stub uv: unexpected call: %s\\n' "$*" >&2; exit 2 ;;
esac
"""


def _uv_env(repos: Repos) -> dict[str, str]:
    """Real-uv settings of design section 12: offline, no config, a private cache."""
    env = {
        k: v
        for k, v in repos.env.items()
        if not k.startswith("UV_") and k != "VIRTUAL_ENV"
    }
    env.update(
        {
            "UV_OFFLINE": "1",
            "UV_NO_CONFIG": "1",
            "UV_CACHE_DIR": str(repos.root / "uv-cache"),
            "UV_PYTHON_DOWNLOADS": "never",
            "UV_PYTHON": sys.executable,
        }
    )
    return env


def install_uv_stub(repos: Repos) -> Path:
    fixed = repos.root / "fixed-uv.lock"
    fixed.write_text(FIXED_LOCK, encoding="utf-8")
    calls = repos.root / "uv-calls.log"
    stub = repos.bin_dir / "uv"
    stub.write_text(_UV_STUB, encoding="utf-8")
    stub.chmod(0o755)
    repos.env = {
        **_uv_env(repos),
        "UV_STUB_LOCK": str(fixed),
        "UV_STUB_CALLS": str(calls),
    }
    return calls


def uv(repos: Repos, cwd: Path, *args: str) -> subprocess.CompletedProcess:
    return _run(["uv", *args], cwd, repos.env, timeout=180)


def run_tier1_sync_cycle(repos: Repos) -> None:
    """Wave 8a, L3, entering `clean`: steps 1 to 13 for a Tier 1 `sync` cycle, then
    the X1/X2 assertions."""
    pr_head = repos.pr_commit(TIER1_PR_FILES)
    assert publish_pr(repos) == pr_head
    base_sha = repos.advance_base(TIER1_BASE_ADVANCE)
    install_gh_stub(repos)
    set_pr_view(repos, pr_head)
    run_log = RunLog(PR_NUMBER, repos.root / "out")
    pre_push_sha = pr_head
    review_terminal = "clean"

    # Wave 8a detection: the hook's single GitHub read (it also feeds step 1).
    view = gh_pr_view(
        repos,
        "baseRefName,mergeable,mergeStateStatus,headRefName,headRefOid,"
        "isCrossRepository",
    )
    hint = mergeability_hint(view["mergeable"], view["mergeStateStatus"])
    assert hint == "conflicting" and needs_probe(hint)

    head_check(repos, view, pre_push_sha)  # step 1
    probe, plan = fresh_probe(repos, hint)  # step 2
    assert probe.base_sha == base_sha and probe.head_sha == pr_head
    assert "uv" in probe.programs
    assert (plan.tier, plan.reason) == (1, "regen_only")
    assert [(p.path, p.stages, p.cls) for p in plan.paths] == [
        ("uv.lock", "123", "regen:uv.lock")
    ]
    assert "pyproject.toml" not in [p.path for p in plan.paths]
    state = run_log.rebuild_state()
    action = conflict_action(
        hook="wave8a",
        plan_tier=plan.tier,
        ordinal=3,
        entering=review_terminal,
        conflict_max_tier=1,
        round_counter=state["round_counter"],
        max_rounds=DEFAULT_MAX_ROUNDS,
        prior_conflict_cycles=prior_conflict_cycles(state["conflict_cycles"], None),
        github_conflicting=plan.github_conflicting,
        plan_reason=plan.reason,
    )
    assert (action.action, action.reason, action.push_kind) == (
        "resolve_push",
        "tier1_sync",
        "sync",
    )
    assert action.status is None and action.skip_ci is False

    # Step 3: write-ahead.
    cycle_id = conflict_cycle_id(plan.tier, len(state["conflict_cycles"]) + 1)
    assert cycle_id == "sync-1"
    write_sync_started(
        run_log,
        cycle_id=cycle_id,
        tier=1,
        kind="sync",
        hook="wave8a",
        plan=plan,
        pre_push_sha=pre_push_sha,
        conflict_max_tier=1,
        review_terminal=review_terminal,
    )

    # Step 4: merge by SHA; the unmerged set equals the plan's path set.
    unmerged = merge_by_sha(repos, base_sha)
    assert unmerged == ["uv.lock"]  # pyproject.toml merged cleanly

    # Step 5: the uv.lock rule.
    pre = run_script(repos, FINISH, "--base-sha", base_sha, "--precheck")
    assert pre.returncode == 0 and pre.payload == {"precheck": "ok"}, pre.stderr
    repos.git(repos.work, "checkout", "--ours", "--", "uv.lock")
    lock = uv(repos, repos.work, "lock")
    assert lock.returncode == 0, lock.stderr
    check = uv(repos, repos.work, "lock", "--check")
    assert check.returncode == 0, check.stderr
    repos.git(repos.work, "add", "--", "uv.lock")
    merged_pyproject = (repos.work / "pyproject.toml").read_text(encoding="utf-8")
    assert merged_pyproject == _pyproject("0.2.0", ">=3.10")

    # Step 7: VAL. VG-1 is the rule's check command (the real result above); the
    # hermetic repository has no lint or format gate, so VG-3 and VG-4 are scripted.
    validation_status = conflict_validation_status(
        1, {"VG-1": check.returncode == 0, "VG-3": True, "VG-4": True}
    )
    assert validation_status == "validated"

    # Step 9: finish gate and commit, under the attempt directory of step 3.
    attempt = conflict_attempt(run_log.read_events(), cycle_id)
    assert attempt == 1
    sync_dir = run_log.output_dir / "sync" / cycle_id / f"a{attempt}"
    message = (
        merge_commit_message(
            base_ref=BASE_REF,
            head_branch=HEAD_BRANCH,
            tier=1,
            rule_patterns=("uv.lock",),
            lock_changes="demo 0.1.0 -> 0.2.0",
        )
        + ATTRIBUTION
    )
    finished = finish_commit(repos, sync_dir, plan, ["uv.lock"], message)
    merge_sha = finished["merge_sha"]
    assert finished["parents"] == [pr_head, base_sha]

    # Step 10: pre-push head guard.
    pre_push_guard(
        repos, pre_push_sha=pre_push_sha, target_sha=merge_sha, base_sha=base_sha
    )

    # Steps 11 and 12.
    state = run_log.rebuild_state()
    decision = evaluate_sync_decision(
        monitor_ordinal=3,
        validation_status=validation_status,
        tier=1,
        conflict_max_tier=1,
        halt_reason=None,
        prior_conflict_cycles=prior_conflict_cycles(state["conflict_cycles"], cycle_id),
        round_counter=state["round_counter"],
        max_rounds=DEFAULT_MAX_ROUNDS,
    )
    triad = decide_and_push(
        repos,
        run_log,
        cycle_id=cycle_id,
        decision=decision,
        push_kind="sync",
        pre_push_sha=pre_push_sha,
        target_sha=merge_sha,
        base_sha=base_sha,
        review_terminal=review_terminal,
    )
    assert triad[1]["kind"] == "sync" and triad[1]["review_terminal"] == "clean"

    # Step 13 (Tier 1): close the cycle; no re-trigger, no reply, no resolve.
    conclude(run_log, cycle_id, "pushed", merge_sha=merge_sha)
    assert should_retrigger(0, "sync") is False

    # --- X1 / X2 assertions -------------------------------------------------
    assert origin_tip(repos) == merge_sha
    assert parents_of(repos, repos.origin, merge_sha) == [pr_head, base_sha]
    verify = repos.root / "pushed-tree"
    repos.git(
        repos.root,
        "clone",
        "-q",
        "--branch",
        HEAD_BRANCH,
        str(repos.origin),
        str(verify),
    )
    pushed_lock = (verify / "uv.lock").read_text(encoding="utf-8")
    assert "<<<<<<<" not in pushed_lock and ">>>>>>>" not in pushed_lock
    assert 'version = "0.2.0"' in pushed_lock
    assert 'requires-python = ">=3.10"' in pushed_lock
    pushed_check = uv(repos, verify, "lock", "--check")
    assert pushed_check.returncode == 0, pushed_check.stderr

    rebuilt = run_log.rebuild_state()
    assert rebuilt["push_count"] == 0
    assert rebuilt["sync_push_count"] == 1
    assert rebuilt["conflict_cycles"] == ["sync-1"]
    assert rebuilt["round_counter"] == 0
    assert rebuilt["open_conflict_cycle"] is None
    assert event_types(run_log) == [
        "sync_started",
        "push_decision",
        "push_initiated",
        "push_completed",
        "sync_concluded",
    ]
    assert_no_retrigger_call(repos)


@pytest.mark.skipif(shutil.which("uv") is None, reason="real uv is not on PATH")
def test_x1_tier1_sync_with_real_uv(tmp_path):
    repos = make_repos(tmp_path, TIER1_BASE_FILES)
    repos.env = _uv_env(repos)
    assert not (repos.bin_dir / "uv").exists()
    run_tier1_sync_cycle(repos)


def test_x2_tier1_sync_with_a_stub_uv(tmp_path):
    repos = make_repos(tmp_path, TIER1_BASE_FILES)
    calls = install_uv_stub(repos)
    run_tier1_sync_cycle(repos)
    # The stub, not a real uv, did the work: the step 5 regenerate and check, then
    # the check on the pushed tree.
    assert calls.read_text(encoding="utf-8").splitlines() == [
        "lock",
        "lock --check",
        "lock --check",
    ]


# ---------------------------------------------------------------------------
# X3: Tier 2 merge at C-initial (two text conflicts), scripted resolution
# ---------------------------------------------------------------------------

TIER2_BASE_FILES = {
    "README.md": "readme\n",
    "f.txt": "alpha\nshared-f\nomega\n",
    "g.txt": "gamma\nshared-g\n",
}
TIER2_PR_FILES = {
    "f.txt": "alpha\nf-from-pr-side\nomega\n",
    "g.txt": "gamma\ng-pr-setting\n",
}
TIER2_BASE_ADVANCE = {
    "f.txt": "alpha\nf-from-base-side\nomega\n",
    "g.txt": "gamma\ng-base-setting\n",
}
TIER2_RESOLVED = {
    "f.txt": "alpha\nf-from-pr-side\nf-from-base-side\nomega\n",
    "g.txt": "gamma\ng-pr-setting\n",
}
# Content tokens that must never reach the commit message.
CONTENT_TOKENS = (
    "f-from-pr-side",
    "f-from-base-side",
    "g-pr-setting",
    "g-base-setting",
)

_EVIDENCE_LINE = (
    "evidence: stage1, stage2, stage3, diff-ours.txt, diff-theirs.txt, log.txt"
)


def _record(g_kind: str) -> str:
    return (
        "## f.txt\n"
        "kind: additive\n"
        "root_cause: both sides replaced the same middle line of the file\n"
        "ours_intent: This PR adds its own line to the middle of the file.\n"
        "theirs_intent: The base adds its own line to the middle of the file.\n"
        "resolution: keep_both(ours then theirs)\n"
        "behavior_after: The file carries both added lines, the PR line first.\n"
        "dropped: none\n"
        f"{_EVIDENCE_LINE}\n"
        "\n"
        "## g.txt\n"
        f"kind: {g_kind}\n"
        "root_cause: both sides changed the value of the same setting line\n"
        "ours_intent: This PR sets the setting to its new value.\n"
        "theirs_intent: The base sets the setting to a different value.\n"
        "resolution: take_ours\n"
        "behavior_after: The setting keeps the value this PR chose.\n"
        "dropped: the base value of the setting, superseded by the PR value\n"
        f"{_EVIDENCE_LINE}\n"
    )


def start_tier2_cycle(tmp_path: Path):
    """Wave 0 plans Tier 2 at L3; C-initial re-reads, re-probes, routes, enters the
    FSM (step 0) and runs steps 1 to 5. Returns everything the two variants need."""
    repos = make_repos(tmp_path, TIER2_BASE_FILES)
    pr_head = repos.pr_commit(TIER2_PR_FILES)
    assert publish_pr(repos) == pr_head
    base_sha = repos.advance_base(TIER2_BASE_ADVANCE)
    install_gh_stub(repos)
    set_pr_view(repos, pr_head)
    run_log = RunLog(PR_NUMBER, tmp_path / "out")
    pre_push_sha = pr_head
    states: list[MonitorState] = []

    # C-initial: the hook's single GitHub read, then the probe.
    view = gh_pr_view(
        repos,
        "baseRefName,mergeable,mergeStateStatus,headRefName,headRefOid,"
        "isCrossRepository",
    )
    hint = mergeability_hint(view["mergeable"], view["mergeStateStatus"])
    assert needs_probe(hint)
    head_check(repos, view, pre_push_sha)  # step 1
    probe, plan = fresh_probe(repos, hint)  # step 2
    assert (plan.tier, plan.reason) == (2, "text_conflict")
    assert plan.text_paths == ("f.txt", "g.txt")
    state = run_log.rebuild_state()
    route = {
        "plan_tier": plan.tier,
        "ordinal": 3,
        "entering": None,
        "conflict_max_tier": 2,
        "round_counter": state["round_counter"],
        "max_rounds": DEFAULT_MAX_ROUNDS,
        "prior_conflict_cycles": prior_conflict_cycles(state["conflict_cycles"], None),
        "github_conflicting": plan.github_conflicting,
        "plan_reason": plan.reason,
    }
    wave0 = conflict_action(hook="wave0", **route)
    assert (wave0.action, wave0.reason) == ("report", "tier2_planned")
    action = conflict_action(hook="c_initial", **route)
    assert (action.action, action.reason) == ("resolve_push", "tier2_merge")
    assert (action.fsm_event, action.push_kind) == ("conflicting", "merge")

    # Step 0 (Tier 2 only): enter the FSM.
    ctx = {
        "monitor_ordinal": 3,
        "round_counter": state["round_counter"],
        "max_rounds": DEFAULT_MAX_ROUNDS,
    }
    fsm_state = transition(MonitorState.S2_CLASSIFY, action.fsm_event, ctx)
    states.append(fsm_state)

    # Step 3: write-ahead.
    cycle_id = conflict_cycle_id(plan.tier, len(state["conflict_cycles"]) + 1)
    assert cycle_id == "conflict-1"
    write_sync_started(
        run_log,
        cycle_id=cycle_id,
        tier=2,
        kind="merge",
        hook="c_initial",
        plan=plan,
        pre_push_sha=pre_push_sha,
        conflict_max_tier=2,
        review_terminal=None,
    )

    # Step 4.
    assert merge_by_sha(repos, base_sha) == ["f.txt", "g.txt"]

    # Step 5 (refs/conflict-intent.md): one file at a time, evidence first, under the
    # attempt directory of step 3.
    attempt = conflict_attempt(run_log.read_events(), cycle_id)
    assert attempt == 1
    sync_dir = run_log.output_dir / "sync" / cycle_id / f"a{attempt}"
    for n, path in enumerate(plan.text_paths, start=1):
        out = sync_dir / str(n)
        res = run_script(
            repos,
            EVIDENCE,
            "--path",
            path,
            "--out",
            f"{out}/",
            "--base-sha",
            base_sha,
            "--merge-base",
            probe.merge_base,
        )
        assert res.returncode == 0, (res.stdout, res.stderr)
        assert res.payload["files"] == EVIDENCE_FILES
        assert res.payload["missing"] == [] and res.payload["truncated"] is False
        assert sorted(p.name for p in out.iterdir()) == sorted(EVIDENCE_FILES)
        (repos.work / path).write_text(TIER2_RESOLVED[path], encoding="utf-8")
        repos.git(repos.work, "add", "--", path)
    return {
        "repos": repos,
        "run_log": run_log,
        "plan": plan,
        "probe": probe,
        "cycle_id": cycle_id,
        "base_sha": base_sha,
        "pr_head": pr_head,
        "pre_push_sha": pre_push_sha,
        "sync_dir": sync_dir,
        "states": states,
        "fsm_state": fsm_state,
        "ctx": ctx,
    }


def test_x3_tier2_merge_with_a_scripted_resolution(tmp_path):
    c = start_tier2_cycle(tmp_path)
    repos, run_log, plan = c["repos"], c["run_log"], c["plan"]
    cycle_id, base_sha, pr_head = c["cycle_id"], c["base_sha"], c["pr_head"]
    pre_push_sha, states, ctx = c["pre_push_sha"], c["states"], c["ctx"]

    # Step 6: the resolution record; the core checks it.
    record_path = c["sync_dir"] / "resolution.md"
    record_path.write_text(_record("competing"), encoding="utf-8")
    record = parse_resolution_record(record_path.read_text(encoding="utf-8"))
    assert resolution_record_ok(record, plan.text_paths) == []

    # Step 7: VAL (scripted green gates; Tier 2 needs VG-2).
    fsm_state = transition(c["fsm_state"], "edits_applied", ctx)
    states.append(fsm_state)
    validation_status = conflict_validation_status(
        2, {"VG-1": True, "VG-2": True, "VG-3": True, "VG-4": True}
    )
    assert validation_status == "validated"
    fsm_state = transition(fsm_state, "validated", ctx)
    states.append(fsm_state)

    # Step 9: finish gate and commit.
    message = (
        merge_commit_message(
            base_ref=BASE_REF, head_branch=HEAD_BRANCH, tier=2, record=record
        )
        + ATTRIBUTION
    )
    finished = finish_commit(repos, c["sync_dir"], plan, list(plan.text_paths), message)
    merge_sha = finished["merge_sha"]
    assert finished["parents"] == [pr_head, base_sha]

    # Step 10.
    pre_push_guard(
        repos, pre_push_sha=pre_push_sha, target_sha=merge_sha, base_sha=base_sha
    )

    # Steps 11 and 12.
    state = run_log.rebuild_state()
    decision = evaluate_sync_decision(
        monitor_ordinal=3,
        validation_status=validation_status,
        tier=2,
        conflict_max_tier=2,
        halt_reason=None,
        prior_conflict_cycles=prior_conflict_cycles(state["conflict_cycles"], cycle_id),
        round_counter=state["round_counter"],
        max_rounds=DEFAULT_MAX_ROUNDS,
    )
    triad = decide_and_push(
        repos,
        run_log,
        cycle_id=cycle_id,
        decision=decision,
        push_kind="merge",
        pre_push_sha=pre_push_sha,
        target_sha=merge_sha,
        base_sha=base_sha,
        review_terminal=None,
    )
    assert triad[1]["kind"] == "merge" and "review_terminal" not in triad[1]

    # Step 13 (Tier 2).
    conclude(
        run_log,
        cycle_id,
        "pushed",
        merge_sha=merge_sha,
        record_path=str(record_path),
        dropped=[e["dropped"] for e in record.values() if e["dropped"] != "none"],
    )
    for event in ("pushed", "replied", "resolved"):  # zero threads to reply to
        fsm_state = transition(fsm_state, event, ctx)
        states.append(fsm_state)
    assert should_retrigger(0, "merge") is True

    assert states == [
        MonitorState.S3_FIXING,
        MonitorState.S7_VALIDATING,
        MonitorState.S4_PUSHING,
        MonitorState.S6_REPLYING,
        MonitorState.RESOLVING,
        MonitorState.S5A_RETRIGGER_REVIEW,
    ]
    rebuilt = run_log.rebuild_state()
    assert rebuilt["push_count"] == 1
    assert rebuilt["sync_push_count"] == 0
    assert rebuilt["conflict_cycles"] == ["conflict-1"]
    assert rebuilt["open_conflict_cycle"] is None

    assert origin_tip(repos) == merge_sha
    assert parents_of(repos, repos.origin, merge_sha) == [pr_head, base_sha]
    for path, content in TIER2_RESOLVED.items():
        assert repos.git(repos.origin, "show", f"{merge_sha}:{path}") == content
    body = repos.git(repos.origin, "log", "-1", "--format=%B", merge_sha)
    assert body.splitlines()[0] == (
        "Merge origin/main into pr (sc:pr-submit sync, tier 2)"
    )
    assert "f.txt: kind additive, resolution keep_both(ours then theirs), " in body
    assert "g.txt: kind competing, resolution take_ours, " in body
    for path in plan.text_paths:
        line = next(ln for ln in body.splitlines() if ln.startswith(f"{path}: "))
        for label in ("kind ", "resolution ", "dropped "):
            assert label in line, (path, label)
    for token in CONTENT_TOKENS:
        assert token not in body, f"file content in the commit message: {token}"
    assert_no_retrigger_call(repos)


def test_x3_semantic_kind_is_rejected_before_any_commit(tmp_path):
    c = start_tier2_cycle(tmp_path)
    repos, run_log, plan = c["repos"], c["run_log"], c["plan"]
    cycle_id, base_sha, pr_head = c["cycle_id"], c["base_sha"], c["pr_head"]

    # Step 6: a `semantic` kind is Tier 3; the record check rejects it.
    record_path = c["sync_dir"] / "resolution.md"
    record_path.write_text(_record("semantic"), encoding="utf-8")
    record = parse_resolution_record(record_path.read_text(encoding="utf-8"))
    problems = resolution_record_ok(record, plan.text_paths)
    assert problems == ["g.txt: kind semantic means Tier 3"]

    # Escalation: ownership-checked abort, the cycle closes, the run halts.
    merge_head = repos.git(repos.work, "rev-parse", "-q", "--verify", "MERGE_HEAD")
    assert merge_head.strip() == base_sha
    repos.git(repos.work, "merge", "--abort")
    conclude(
        run_log, cycle_id, "aborted", record_path=str(record_path), reason="sync_tier3"
    )
    run_log.append({"event_type": "terminal_halted", "reason": "sync_tier3"})

    # Nothing was committed or pushed; the record stays in the output dir.
    assert repos.git(repos.work, "rev-parse", "HEAD").strip() == pr_head
    assert not (repos.work / ".git" / "MERGE_HEAD").exists()
    assert (
        repos.git(repos.work, "status", "--porcelain=v1", "--untracked-files=no") == ""
    )
    assert origin_tip(repos) == pr_head
    assert record_path.exists()
    assert not (c["sync_dir"] / "message.txt").exists()
    types = event_types(run_log)
    assert "push_decision" not in types and "push_initiated" not in types
    assert types == ["sync_started", "sync_concluded", "terminal_halted"]
    rebuilt = run_log.rebuild_state()
    assert rebuilt["push_count"] == 0 and rebuilt["sync_push_count"] == 0
    assert rebuilt["conflict_cycles"] == ["conflict-1"]
    assert rebuilt["open_conflict_cycle"] is None
    assert c["states"] == [MonitorState.S3_FIXING]
    assert_no_retrigger_call(repos)


def test_x3_resume_restart_collects_into_a_new_attempt_directory(tmp_path):
    """Resume row 5 (our own interrupted merge): abort, restart under the same cycle
    id, and collect the evidence again. Attempt 2 writes into `a2/`, so the collector
    does not meet attempt 1's files (`out_not_empty`), and attempt 1's evidence stays
    (PR #378 review finding)."""
    c = start_tier2_cycle(tmp_path)
    repos, run_log, plan = c["repos"], c["run_log"], c["plan"]
    cycle_id, base_sha = c["cycle_id"], c["base_sha"]
    first_dir = c["sync_dir"]
    assert first_dir.name == "a1"
    kept = {p: p.read_bytes() for p in sorted(first_dir.rglob("*")) if p.is_file()}
    assert kept

    # Row 5: MERGE_HEAD is the open cycle's base tip: abort and restart.
    merge_head = repos.git(repos.work, "rev-parse", "-q", "--verify", "MERGE_HEAD")
    assert merge_head.strip() == base_sha
    repos.git(repos.work, "merge", "--abort")
    run_log.append(
        {
            "event_type": "sync_concluded",
            "cycle_id": cycle_id,
            "outcome": "aborted",
            "merge_sha": None,
            "record_path": None,
            "dropped": [],
            "reason": None,
            "recovered": True,
        }
    )
    started = next(
        ev for ev in run_log.read_events() if ev["event_type"] == "sync_started"
    )
    restart = {
        k: v
        for k, v in started.items()
        if k not in ("schema_version", "event_id", "timestamp")
    }
    run_log.write_ahead({**restart, "resumed": True})  # the restart's step 3

    # Steps 4 and 5 again, under the new attempt directory.
    assert merge_by_sha(repos, base_sha) == ["f.txt", "g.txt"]
    attempt = conflict_attempt(run_log.read_events(), cycle_id)
    assert attempt == 2
    second_dir = run_log.output_dir / "sync" / cycle_id / f"a{attempt}"
    res = run_script(
        repos,
        EVIDENCE,
        "--path",
        plan.text_paths[0],
        "--out",
        f"{second_dir / '1'}/",
        "--base-sha",
        base_sha,
        "--merge-base",
        c["probe"].merge_base,
    )
    assert res.returncode == 0, (res.stdout, res.stderr)
    assert res.payload["files"] == EVIDENCE_FILES
    # Collecting into attempt 1's directory again is what the fix avoids.
    again = run_script(
        repos,
        EVIDENCE,
        "--path",
        plan.text_paths[0],
        "--out",
        f"{first_dir / '1'}/",
        "--base-sha",
        base_sha,
        "--merge-base",
        c["probe"].merge_base,
    )
    assert again.stdout == "EVIDENCE_FAIL out_not_empty\n"
    assert {
        p: p.read_bytes() for p in sorted(first_dir.rglob("*")) if p.is_file()
    } == kept
    assert run_log.rebuild_state()["conflict_cycles"] == [cycle_id]

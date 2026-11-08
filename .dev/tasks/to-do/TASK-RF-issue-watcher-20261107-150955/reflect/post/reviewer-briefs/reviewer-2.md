# Reviewer brief 2 (persona lens: qa / tests, acceptance and verification)

## T1 card excerpt

(Verbatim slice of the Tier-1 card, "Coverage and acceptance". Unverified claims; confirm or refute.)

#### Coverage and acceptance (card section)

**Re-verified against code (Read).** All the FR/NFR implementation line ranges I spot-checked in coverage-matrix.yaml match:
- FR-010 cycle.py:1052-1062
- FR-011 960-997
- FR-012 launch.py:84-102
- FR-013 343-355
- FR-016 814-815
- FR-024 848-857, 917, 1031
- FR-025 1039-1049
- FR-028 644-649, 738-742
- FR-029 383-412
- NFR-009 github.py:437-463
- reachability RC-2 order

The IE-01 to IE-05 line and call-site numbers also match. One helper claim is corrected (A11).

**Not re-verified:**
- The "bites" judgments for tests I did not open. I read test_crash_injection.py 150-374, test_cycle.py 2895-2954, test_module_boundaries.py 1-100 and test_cli_e2e.py 1-135, plus grep-level checks elsewhere.
- The Python 3.10.20 run and the "4 environmental failures".
- DF-50 and DF-51 beyond the first ~400 characters.
- D 598-602.

**Strongest proofs:**
1. Crash injection C1-C5 with byte-level store comparison and rerun counts (test_crash_injection.py:217-374).
2. Pending-before-launch snapshot taken inside the launcher callback (test_cycle.py:2925-2954), plus the e2e stub snapshot (RC-2).
3. The AST import walker with negative self-tests (test_module_boundaries.py header).

**Weakest:**
- (a) Every gh and Orca reply shape is an `_assumed_shape` fixture; the live test is the real proof and has not run.
- (b) NFR-012/AC-23 rest on gate output only.
- (c) NFR-008/AC-19 are never chained end to end (DF-55).
- (d) NFR-014's clock half has no test (C6).
- (e) S:272 `re-approved` reporting is not delivered (OQ-49).
- (f) The root-skipped tests (C5).
- (g) The unbounded-pipe behaviour of a real Orca (A6).
- (h) The FR-009 marker-contract test is weak (matrix note).

**Not really proven:** NFR-014 (partial), NFR-008/AC-19 (split), NFR-012/AC-23 (gate), and the real-shape half of FR-002/005/006/007/009/013 until FU-1 and FU-3 run.

## Grounding hunks

codegraph run state: index_state=fresh checked_at=2026-11-08T04:40:00Z worktree_root=/home/coder/workspaces/worktrees/IronClaude/issue-331-github-issue-watcher projectPath=/home/coder/workspaces/worktrees/IronClaude/issue-331-github-issue-watcher

### .dev/tasks/to-do/TASK-RF-issue-watcher-20261107-150955/reflect/post/verify-logs/invocations.yaml

```yaml
# Verification invocations (SKILL 6.1.1 control g). Wrapper per control (d)/(i):
#   timeout <N> env -u SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE <validated base command>
# Controls (a)-(c): fixed template, verb in {pytest, ruff, mypy, make, uv, npm, tsc, cargo} = uv, no shell metacharacters.
- cmd: "timeout 600 env -u SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE uv run pytest tests/issue_watch -q -p no:cacheprovider"
  step: "5.5"
  cwd: "/home/coder/workspaces/worktrees/IronClaude/issue-331-github-issue-watcher"
  exit_code: 0
  duration_ms: 17250
  stdout_path: null
  stderr_path: null
  summary: "2635 passed in 17.25s on Python 3.11.15; 0 failed, 0 errors, 0 skipped (the -q summary line shows no 'skipped' segment); stdout tail kept in the orchestrator transcript"
  blocked_reason: null
  deviation_class: none
- cmd: "timeout 120 env -u SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE uv run ruff check src/superclaude/cli/issue_watch tests/issue_watch src/superclaude/cli/main.py"
  step: "5"
  cwd: "/home/coder/workspaces/worktrees/IronClaude/issue-331-github-issue-watcher"
  exit_code: 0
  duration_ms: null
  stdout_path: null
  stderr_path: null
  summary: "All checks passed!"
  blocked_reason: null
  deviation_class: none
- cmd: "timeout 120 env -u SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE uv run ruff format --check src/superclaude/cli/issue_watch tests/issue_watch src/superclaude/cli/main.py"
  step: "5"
  cwd: "/home/coder/workspaces/worktrees/IronClaude/issue-331-github-issue-watcher"
  exit_code: 0
  duration_ms: null
  stdout_path: null
  stderr_path: null
  summary: "31 files already formatted"
  blocked_reason: null
  deviation_class: none
```

### .dev/tasks/to-do/TASK-RF-issue-watcher-20261107-150955/reflect/post/artifacts/runtime-surface-ledger.yaml

```yaml
# runtime-surface-ledger.yaml (refs/runtime-surface.md section 5; one row per evaluated edge)
# Tagger: Python Click callbacks in src/superclaude/cli/issue_watch/cli.py (decorators @click.group / @issue_watch_group.command).
# requirement_id FR-026 comes from design heading "### 4.1 Verbs (FR-026)" (docs/designs/issue-watcher.md:108); the tagger is symbol-anchored.
# Referrer partition (language table `py`): tests/, test_*.py, conftest.py = test; docstrings/# comments = non-production.
# Facts found (all Read):
#   - main.py:563 imports issue_watch_group; main.py:565 `main.add_command(issue_watch_group, name="issue-watch")` (the ONLY production caller of the group).
#   - main is a Click group (main.py:18 @click.group(), main.py:20 def main); pyproject.toml:71 `superclaude = "superclaude.cli.main:main"` (console script).
#   - No production code references once_command/status_command/check_config_command/init_state_command/reset_command by name
#     (word-boundary Grep over *.py/*.toml/*.md: only the definitions in cli.py plus test_cli.py:694 `cli.once_command.callback(...)`).
#   - tests/issue_watch/test_cli_e2e.py:103-123 runs `python -m superclaude.cli.main issue-watch <verb> --config <file>` as a REAL subprocess
#     (verbs once and init-state; main.py:568-569 `if __name__ == "__main__": main()`), with PATH stubs for gh/git/orca. It does not go through the
#     installed console script, but through the same main().
# Oracle: every symbol matches (a) decorator command; the group also matches (b) packaging entrypoint and (c) registry add_command.
# Verdict forced by the oracle: DEGRADE for all six symbols (routes to Grounding Gaps, never Regression).

- requirement_id: FR-026
  symbol: issue_watch_group
  edge: "issue_watch_group -> main.add_command registry (main.py:565)"
  status: DEGRADE            # oracle (c) registry assignment/call
  production_referrers: ["src/superclaude/cli/main.py:563", "src/superclaude/cli/main.py:565"]
  evidence_ref: "src/superclaude/cli/main.py:565"
- requirement_id: FR-026
  symbol: issue_watch_group
  edge: "issue_watch_group -> @click.group('issue-watch') decorator"
  status: DEGRADE            # oracle (a) command decorator
  production_referrers: ["src/superclaude/cli/main.py:565"]
  evidence_ref: "src/superclaude/cli/issue_watch/cli.py:94"
- requirement_id: FR-026
  symbol: issue_watch_group
  edge: "issue_watch_group -> root [project.scripts] superclaude = superclaude.cli.main:main (depth 1: main -> add_command)"
  status: DEGRADE            # oracle (b) packaging entrypoint; rootwalk depth-1 does reach the group (main.py:565) but oracle (b) governs
  production_referrers: ["src/superclaude/cli/main.py:565"]
  evidence_ref: "pyproject.toml:71"
- requirement_id: FR-026
  symbol: issue_watch_group
  edge: "issue_watch_group -> tests/issue_watch/test_cli.py:124-126 (CliRunner.invoke), test_no_text.py:233-235 (invoke), test_cli.py:279-290"
  status: UNREACHED          # edge level only: test-only referrers do not count as production (language table)
  production_referrers: []
  evidence_ref: "tests/issue_watch/test_cli.py:126"
- requirement_id: FR-026
  symbol: once_command
  edge: "once_command -> @issue_watch_group.command('once') decorator"
  status: DEGRADE            # oracle (a)
  production_referrers: []
  evidence_ref: "src/superclaude/cli/issue_watch/cli.py:111"
- requirement_id: FR-026
  symbol: once_command
  edge: "once_command -> root superclaude.cli.main:main via issue_watch_group.commands (depth 2: main -> group -> verb)"
  status: DEGRADE            # rootwalk depth bound 1 is hit before the verb is reached (rule 5); never UNREACHED
  production_referrers: []
  evidence_ref: "src/superclaude/cli/main.py:565"
- requirement_id: FR-026
  symbol: once_command
  edge: "once_command -> tests: test_cli.py:694 (.callback direct call), test_cli.py:452 and test_cli.py:630-716 (CliRunner), test_cli_e2e.py:103-123 (real subprocess)"
  status: UNREACHED          # edge level only: test-only referrers
  production_referrers: []
  evidence_ref: "tests/issue_watch/test_cli_e2e.py:103"
- requirement_id: FR-026
  symbol: status_command
  edge: "status_command -> @issue_watch_group.command('status') decorator"
  status: DEGRADE            # oracle (a)
  production_referrers: []
  evidence_ref: "src/superclaude/cli/issue_watch/cli.py:164"
- requirement_id: FR-026
  symbol: status_command
  edge: "status_command -> root superclaude.cli.main:main via issue_watch_group.commands (depth 2)"
  status: DEGRADE            # rootwalk depth bound hit
  production_referrers: []
  evidence_ref: "src/superclaude/cli/main.py:565"
- requirement_id: FR-026
  symbol: status_command
  edge: "status_command -> tests: test_cli.py:785-1048 (CliRunner via group; no direct name reference, no real-subprocess test)"
  status: UNREACHED          # edge level only: test-only referrers
  production_referrers: []
  evidence_ref: "tests/issue_watch/test_cli.py:785"
- requirement_id: FR-026
  symbol: check_config_command
  edge: "check_config_command -> @issue_watch_group.command('check-config') decorator"
  status: DEGRADE            # oracle (a)
  production_referrers: []
  evidence_ref: "src/superclaude/cli/issue_watch/cli.py:185"
- requirement_id: FR-026
  symbol: check_config_command
  edge: "check_config_command -> root superclaude.cli.main:main via issue_watch_group.commands (depth 2)"
  status: DEGRADE            # rootwalk depth bound hit
  production_referrers: []
  evidence_ref: "src/superclaude/cli/main.py:565"
- requirement_id: FR-026
  symbol: check_config_command
  edge: "check_config_command -> tests: test_cli.py:319-424 (CliRunner via group)"
  status: UNREACHED          # edge level only: test-only referrers
  production_referrers: []
  evidence_ref: "tests/issue_watch/test_cli.py:319"
- requirement_id: FR-026
  symbol: init_state_command
  edge: "init_state_command -> @issue_watch_group.command('init-state') decorator"
  status: DEGRADE            # oracle (a)
  production_referrers: []
  evidence_ref: "src/superclaude/cli/issue_watch/cli.py:201"
- requirement_id: FR-026
  symbol: init_state_command
  edge: "init_state_command -> root superclaude.cli.main:main via issue_watch_group.commands (depth 2)"
  status: DEGRADE            # rootwalk depth bound hit
  production_referrers: []
  evidence_ref: "src/superclaude/cli/main.py:565"
- requirement_id: FR-026
  symbol: init_state_command
  edge: "init_state_command -> tests: test_cli.py:1241-1283 (CliRunner), test_cli_e2e.py:125-130 (real subprocess `init-state`)"
  status: UNREACHED          # edge level only: test-only referrers
  production_referrers: []
  evidence_ref: "tests/issue_watch/test_cli_e2e.py:127"
- requirement_id: FR-026
  symbol: reset_command
  edge: "reset_command -> @issue_watch_group.command('reset') decorator"
  status: DEGRADE            # oracle (a)
  production_referrers: []
  evidence_ref: "src/superclaude/cli/issue_watch/cli.py:282"
- requirement_id: FR-026
  symbol: reset_command
  edge: "reset_command -> root superclaude.cli.main:main via issue_watch_group.commands (depth 2)"
  status: DEGRADE            # rootwalk depth bound hit
  production_referrers: []
  evidence_ref: "src/superclaude/cli/main.py:565"
- requirement_id: FR-026
  symbol: reset_command
  edge: "reset_command -> tests: test_cli.py:1328-1415 (CliRunner via group)"
  status: UNREACHED          # edge level only: test-only referrers
  production_referrers: []
  evidence_ref: "tests/issue_watch/test_cli.py:1328"

# Per-symbol reduction (DEGRADE-on-any-incompleteness > UNREACHED > REACHED):
#   issue_watch_group: DEGRADE | once_command: DEGRADE | status_command: DEGRADE
#   check_config_command: DEGRADE | init_state_command: DEGRADE | reset_command: DEGRADE
# Contract values:
#   runtime_surface_requirements: 6 tagged symbols (requirement FR-026, group + 5 verbs)
#   runtime_surface_sweep_ran: true
#   runtime_surface_unreached: 0   (unreached_surfaces: [], len 0 == 0)
#   runtime_surface_degraded: true
```

### tests/issue_watch/test_cli_e2e.py:299-398

```python
def test_fr001_idle_cycle_makes_exactly_two_gh_calls(tmp_path, stub_path):
    """FR-001 GWT, NFR-009: an idle cycle exits 0 after `api user` and discovery."""
    assert_local_filesystem(tmp_path)
    watcher = make_watcher(tmp_path, stub_path)
    watcher.init_state()
    world = world_for(watcher)  # no issue: discovery lists nothing
    watcher.script(world)

    done = watcher.cli("once")

    assert done.returncode == 0, done
    assert done.stdout == "cycle: cycle_complete\nexit: 0\n", done.stdout
    assert done.stderr == ""
    calls = watcher.calls()
    gh_calls = [argv_of(c)[1] for c in calls if c["tool"] == "gh"]
    assert gh_calls == [USER_ARGV, DISCOVERY_ARGV], gh_calls
    assert [c["tool"] for c in calls] == ["gh", "git", "gh"], calls
    assert not [c for c in calls if c["tool"] in ("orca", "orca-ide")], calls
    cycle_lines = [x for x in watcher.audit_lines() if x["kind"] == "cycle"]
    assert len(cycle_lines) == 1, watcher.audit_lines()
    line = cycle_lines[0]
    assert (line["exit"], line["reason"], line["dry_run"]) == (
        0,
        "cycle_complete",
        False,
    )
    assert (line["login"], line["gh_calls"], line["discovery_count"]) == (
        OWN_LOGIN,
        2,
        0,
    )
    assert watcher.store()["entries"] == {}
    assert watcher.store()["last_completed_cycle_at"] is not None


def test_fr010_fr013_eligible_issue_launches_once_through_orca_ide(tmp_path, stub_path):
    """FR-010, FR-013, FR-003, AC-1: one launch, 12-element argv, pending at launch."""
    assert_local_filesystem(tmp_path)
    watcher = make_watcher(tmp_path, stub_path)
    created = watcher.init_state()
    world = world_for(watcher)
    eligible_issue(world, created)
    watcher.script(
        world, launch_reply=load_fixture("orca_launch_success.json")["payload"]
    )
    orca_ide = str(watcher.stubbin / "orca-ide")

    done = watcher.cli("once")

    assert done.returncode == 0, done
    assert done.stdout == "cycle: cycle_complete\nexit: 0\n", done.stdout
    assert done.stderr == ""
    calls = watcher.calls()
    # every external call, in order; the stub never sees the program path
    assert [argv_of(c) for c in calls] == expected_eligible_sequence(watcher), [
        argv_of(c) for c in calls
    ]
    # FR-013: the 12-element argv, with the program path, equals the literal list
    launches = [c for c in calls if c["argv"][:2] == ["agent", "launch"]]
    assert len(launches) == 1, launches
    launch_call = launches[0]
    assert launch_call["tool"] == "orca-ide"
    assert [orca_ide, *launch_call["argv"]] == launch_argv_literal(
        orca_ide, watcher.config.worktree
    )
    assert len([orca_ide, *launch_call["argv"]]) == 12
    assert launch_call["argv"][launch_call["argv"].index("--prompt") + 1] == (
        "/sc:issue --claim 9"
    )
    assert Path(launch_call["cwd"]).resolve() == watcher.config.worktree.resolve()
    # orca-ide is resolved first, so the plain orca stub is never called
    assert not [c for c in calls if c["tool"] == "orca"], calls
    # FR-003: the discovery argv is the literal list and asks for no text field
    discoveries = [c for c in calls if c["argv"][:2] == ["issue", "list"]]
    assert [c["argv"] for c in discoveries] == [DISCOVERY_ARGV]
    for call in calls:
        for arg in call["argv"]:
            assert not {"title", "body", "comments"} & set(arg.split(",")), arg
    # FR-010: the entry was already pending, launches 1, consumed_at set, at launch time
    assert "dispatch_json" in launch_call, launch_call
    at_launch = json.loads(launch_call["dispatch_json"])["entries"][str(ISSUE)]
    assert at_launch["state"] == "pending", at_launch
    assert at_launch["launches"] == 1, at_launch
    assert at_launch["consumed_at"] is not None, at_launch
    assert at_launch["launch_cwd"] == str(watcher.config.worktree), at_launch
    # no other stub call took a snapshot
    assert [c["call"] for c in calls if "dispatch_json" in c] == [launch_call["call"]]
    # the final store shows the launch
    final = watcher.store()["entries"][str(ISSUE)]
    assert final["state"] == "launched", final
    assert final["launches"] == 1, final
    assert final["operation_id"] == "op-test-0001", final
    # the audit trail: one launched decision, then the cycle line
    lines = watcher.audit_lines()
    decisions = [x for x in lines if x["kind"] == "decision"]
    assert [(x["issue"], x["reason"], x["state"]) for x in decisions] == [
        (ISSUE, "launched", "launched")
    ], lines
    assert lines[-1]["kind"] == "cycle"
    assert (lines[-1]["exit"], lines[-1]["reason"]) == (0, "cycle_complete")
```

### tests/issue_watch/test_cycle.py:2905-2935

```python
def test_an_entry_of_another_login_is_not_launched_again__df47_nfr005(
    tmp_path, tmp_state, gh_world, kind
):
    world = gh_world()  # discovery now runs under OWN_LOGIN
    world.issue(9)
    seeded = _seed(tmp_state, 9, kind, _PENDING_AT, login=_OLD_LOGIN)
    assert seeded.launch_login == _OLD_LOGIN
    res, deps = _run(tmp_path, tmp_state, world)
    assert (res.exit_code, res.reason) == (0, "cycle_complete")
    assert _decisions(_lines_of(tmp_state, res)) == [(9, "already_dispatched")]
    assert deps.launcher.calls == []
    assert not _probed(world)
    assert _entry(tmp_state, 9) == seeded  # still names the first login


# ==============================================================================
# FR-010 and FR-014: the launch steps, in order
# ==============================================================================


def test_the_launch_steps_run_in_the_fr014_order_and_pending_is_durable__fr010_fr014(
    tmp_path, tmp_state, gh_world
):
    """AC-6, FR-010, FR-014: pending with launches 1 is saved before the launch."""
    world = gh_world()
    world.issue(9)
    stored_at_origin: list[dict] = []
    world.on("origin", lambda: stored_at_origin.append(dict(tmp_state.load().entries)))
    seen: list[tuple[dict, int]] = []

    def peek():
```

### tests/issue_watch/test_cycle.py:3495-3560

```python
def test_s1_case_a_fifteen_skipping_issues_examine_k_then_the_rest__fr016_df50(
    tmp_path, tmp_state, gh_world
):
    world = gh_world()
    world.issues_from(range(1, 16), items=[{"status": "In progress"}])  # r = 4
    launcher = FakeLauncher()
    res1, _ = _run(tmp_path, tmp_state, world, launcher=launcher)
    lines1 = _lines_of(tmp_state, res1)
    k = min(10, (github.CALL_CAP - github.RESERVED_CALLS) // 4)
    assert k == 8
    assert _decisions(lines1) == [
        *[(n, "project_mismatch") for n in range(1, k + 1)],
        (9, "budget_exhausted"),
        (10, "budget_exhausted"),
    ]
    assert _the_cycle_line(lines1)["gh_calls"] == 2 + 32
    t0 = CYCLE_NOW
    stored = tmp_state.load()
    assert dict(stored.considered) == {n: t0 for n in range(1, 9)}  # 9, 10 unstamped

    world.clock.advance(60)
    t1 = world.clock.now()
    res2, _ = _run(tmp_path, tmp_state, world, launcher=launcher)
    lines2 = _lines_of(tmp_state, res2)
    # Cycle 2 starts with the 7 never-examined issues, then the oldest examined.
    assert _decisions(lines2) == [
        *[(n, "project_mismatch") for n in range(9, 16)],
        (1, "project_mismatch"),
        (2, "budget_exhausted"),
        (3, "budget_exhausted"),
    ]
    assert dict(tmp_state.load().considered) == {
        **{n: t0 for n in range(2, 9)},
        **{n: t1 for n in (*range(9, 16), 1)},
    }
    assert launcher.calls == []
    assert tmp_state.load().entries == {}


def test_s1_case_b_fifteen_eligible_issues_examine_and_launch_exactly_one__fr016_df50(
    tmp_path, tmp_state, gh_world
):
    world = gh_world()
    world.issues_from(range(1, 16))
    launcher = FakeLauncher(
        lambda i: cycle.launch.LaunchOutcome("launched", f"op-s1-{i:04d}", "ok")
    )
    res1, _ = _run(tmp_path, tmp_state, world, launcher=launcher)
    lines1 = _lines_of(tmp_state, res1)
    assert (res1.exit_code, res1.launched_issue) == (0, 1)
    assert _decisions(lines1) == [(1, "launched")]
    assert [c[2] for c in launcher.calls] == ["/sc:issue --claim 1"]
    assert _touched(world) == {1}  # later candidates are neither read ...
    stored = tmp_state.load()
    assert dict(stored.considered) == {1: CYCLE_NOW}  # ... nor stamped
    assert sorted(stored.entries) == [1]
    assert _the_cycle_line(lines1)["gh_calls"] == 9

    world.clock.advance(60)
    res2, _ = _run(tmp_path, tmp_state, world, launcher=launcher)
    assert _decisions(_lines_of(tmp_state, res2)) == [(2, "launched")]
    assert [c[2] for c in launcher.calls] == [
        "/sc:issue --claim 1",
        "/sc:issue --claim 2",
    ]
    assert sorted(tmp_state.load().entries) == [1, 2]
```

### tests/issue_watch/test_crash_injection.py:217-350

```python
def test_c1_crash_before_the_pending_save_leaves_the_store_untouched__nfr005(
    tmp_path, tmp_state, gh_world
):
    rig = Rig(tmp_path, tmp_state, gh_world)
    store = CrashingStore(tmp_state, "C1")
    assert rig.crash(store).code == "crash C1"
    assert store.saves == 1
    assert rig.store_bytes() == rig.store_before
    assert rig.file_names() == rig.names_before  # no tmp file either
    assert rig.entry() is None
    assert rig.crash_launcher.calls == []
    rig.assert_untouched_audit()
    rig.check_at_most_once("after the crash")
    _assert_launched_by_first_rerun(rig, rig.reruns())


# ==============================================================================
# C2: during write_prepared_bytes (os.replace of the pending save)
# ==============================================================================


def test_c2_crash_during_the_atomic_replace_keeps_the_old_file__nfr005(
    tmp_path, tmp_state, gh_world, monkeypatch, capsys
):
    rig = Rig(tmp_path, tmp_state, gh_world)
    real_replace = os.replace
    hits: list[tuple[str, str]] = []

    def replace_once(src, dst, *args, **kwargs):
        if str(dst).endswith("dispatch.json") and not hits:
            hits.append((str(src), str(dst)))
            raise SystemExit("crash C2")
        return real_replace(src, dst, *args, **kwargs)

    with monkeypatch.context() as patch:  # the reruns use the real os.replace
        patch.setattr(os, "replace", replace_once)
        assert rig.crash(FileStore(rig.state_dir)).code == "crash C2"
    assert os.replace is real_replace
    # The patch was really hit, once, on the store file.
    assert len(hits) == 1
    src, dst = hits[0]
    assert dst == str(rig.state_dir / "dispatch.json")
    assert os.path.basename(src).startswith("dispatch.json.")
    assert src.endswith(".tmp")

    assert rig.store_bytes() == rig.store_before  # the old file, byte for byte
    assert rig.entry() is None
    orphans = sorted(rig.state_dir.glob("dispatch.json.*.tmp"))
    assert [str(p) for p in orphans] == [src]  # SystemExit skips the unlink
    assert rig.file_names() == sorted([*rig.names_before, orphans[0].name])
    orphan_bytes = orphans[0].read_bytes()
    pending = json.loads(orphan_bytes)["entries"][str(ISSUE)]
    assert (pending["state"], pending["launches"]) == ("pending", 1)
    assert rig.crash_launcher.calls == []
    rig.assert_untouched_audit()
    rig.check_at_most_once("after the crash")

    runs = rig.reruns()
    _assert_launched_by_first_rerun(rig, runs)
    # The orphan is ignored: still there, untouched, no error and no audit failure.
    assert orphans[0].read_bytes() == orphan_bytes
    assert capsys.readouterr().err == ""
    assert {ln["kind"] for ln in _audit_lines(rig.state_dir)} == {"decision", "cycle"}


# ==============================================================================
# C3: after the pending save, before the spawn
# ==============================================================================


def test_c3_crash_after_the_pending_save_is_swept_and_never_launched__nfr005(
    tmp_path, tmp_state, gh_world
):
    rig = Rig(tmp_path, tmp_state, gh_world)
    store = CrashingStore(tmp_state, "C3")
    assert rig.crash(store).code == "crash C3"
    assert store.saves == 1
    rig.assert_pending(rig.entry(), CYCLE_NOW)
    doc = rig.doc()  # the second save never happened
    assert (doc.considered, doc.last_completed_cycle_at) == ({}, None)
    assert rig.file_names() == rig.names_before  # the replace completed: no orphan
    assert rig.crash_launcher.calls == []
    rig.assert_untouched_audit()
    rig.check_at_most_once("after the crash")
    _assert_swept_by_first_rerun(rig, rig.reruns(), CYCLE_NOW)
    assert rig.launcher_calls == 0


# ==============================================================================
# C4: after the spawn, before the outcome save
# ==============================================================================


def test_c4_crash_after_the_spawn_is_swept_and_never_launched_again__nfr005(
    tmp_path, tmp_state, gh_world
):
    rig = Rig(tmp_path, tmp_state, gh_world)
    store = CrashingStore(tmp_state, "C4")
    assert rig.crash(store).code == "crash C4"
    assert store.saves == 2
    rig.assert_pending(rig.entry(), CYCLE_NOW)  # the outcome was lost
    doc = rig.doc()
    assert (doc.considered, doc.last_completed_cycle_at) == ({}, None)
    assert [call[2] for call in rig.crash_launcher.calls] == [PROMPT]
    rig.assert_untouched_audit()
    rig.check_at_most_once("after the crash")
    _assert_swept_by_first_rerun(rig, rig.reruns(), CYCLE_NOW)
    assert rig.launcher_calls == 1  # still the one call of the crashed cycle


def test_an_exception_out_of_the_launcher_leaves_the_same_state_as_c4__nfr005(
    tmp_path, tmp_state, gh_world
):
    boom = FakeLauncher(raises=RuntimeError("fake: launcher failed"))
    rig = Rig(tmp_path, tmp_state, gh_world, crash_launcher=boom)
    error = rig.crash(FileStore(rig.state_dir), expected=RuntimeError)
    assert str(error) == "fake: launcher failed"
    rig.assert_pending(rig.entry(), CYCLE_NOW)
    assert [call[2] for call in boom.calls] == [PROMPT]
    rig.assert_untouched_audit()
    rig.check_at_most_once("after the exception")
    _assert_swept_by_first_rerun(rig, rig.reruns(), CYCLE_NOW)
    assert rig.launcher_calls == 1


# ==============================================================================
# C5: after the outcome save, before the audit append
# ==============================================================================


def test_c5_crash_after_the_outcome_save_loses_only_the_audit_lines__nfr005(
    tmp_path, tmp_state, gh_world
):
    rig = Rig(tmp_path, tmp_state, gh_world)
```

### tests/issue_watch/test_security_invariants.py:451-530

```python
def test_prompt_regex_property(tmp_path):
    """AC-7, FR-012, NFR-001: every prompt matches the claim regex over the corpus."""
    rng = random.Random(SEED)
    draws = list(EDGE_VALUES) + [_draw(rng) for _ in range(DRAWS)]
    assert len(draws) == DRAWS + len(EDGE_VALUES)

    worktree = tmp_path / "worktree"
    runner = FakeRunner()
    real_launcher = OrcaLauncher(runner)
    fake_launcher = FakeLauncher()
    valid = Counter()
    kinds = Counter()
    for index, value in enumerate(draws):
        where = f"draw {index}: {value!r:.200} ({type(value).__name__})"
        kinds[type(value).__name__] += 1
        if is_claim_number(value):
            valid["valid"] += 1
            prompt = build_claim_prompt(value)
            assert prompt == f"/sc:issue --claim {value}", where
            assert is_claim_prompt(prompt), where
            argv = launch_argv(ORCA_PATH, worktree, prompt)
            assert len(argv) == 12 and argv[10] == prompt, where
            assert argv[9] == "--prompt", where
        else:
            valid["invalid"] += 1
            with pytest.raises(ValueError):
                build_claim_prompt(value)
        # The launch layer takes only a string that is itself a claim prompt, so a
        # raw drawn value can never become the --prompt argument.
        if not is_claim_prompt(value):
            with pytest.raises(ValueError):
                launch_argv(ORCA_PATH, worktree, value)  # type: ignore[arg-type]
            with pytest.raises(ValueError):
                real_launcher.launch(ORCA_PATH, worktree, value, 120.0)  # type: ignore[arg-type]
            with pytest.raises(ValueError):
                fake_launcher.launch(ORCA_PATH, worktree, value, 120.0)  # type: ignore[arg-type]
            assert runner.calls == [] and fake_launcher.calls == [], where

    # The generator is not degenerate: both outcomes and every family occur.
    assert valid["valid"] >= 400 and valid["invalid"] >= 1200, valid
    assert {"int", "str", "float", "bool", "NoneType", "list", "tuple", "dict"} <= set(
        kinds
    ), kinds

    for attack in PROMPT_ATTACKS:
        with pytest.raises(ValueError):
            launch_argv(ORCA_PATH, worktree, attack)
        with pytest.raises(ValueError):
            real_launcher.launch(ORCA_PATH, worktree, attack, 120.0)
        with pytest.raises(ValueError):
            fake_launcher.launch(ORCA_PATH, worktree, attack, 120.0)
    assert runner.calls == [] and fake_launcher.calls == []

    # Full cycles over the same generator: the numbers GitHub can hand over
    # (the two bounds and drawn valid ones) each give one launch whose --prompt
    # matches the pattern.
    numbers = [1, 9, MAX_N] + [rng.randint(1, MAX_N) for _ in range(9)]
    for k, n in enumerate(numbers):
        ran = run_world(tmp_path / f"cycle-{k}", lambda w, n=n: w.issue(n))
        assert (ran.result.exit_code, ran.result.launched_issue) == (0, n), n
        assert ran.prompts == [f"/sc:issue --claim {n}"], f"cycle {k}: issue {n}"
        assert all(is_claim_prompt(p) for p in ran.prompts), n
        assert ran.store.load().entries[n].launches == 1, n


# ==============================================================================
# NFR-001, T1: hostile GitHub, config and login text never reaches the prompt
# ==============================================================================


@pytest.mark.parametrize("hostile", HOSTILE, ids=[f"h{i}" for i in range(len(HOSTILE))])
def test_hostile_labels_logins_and_commenters_never_reach_the_prompt(tmp_path, hostile):
    """NFR-001, AC-7: hostile GitHub text never reaches the prompt or any argv."""

    def build(world: GhWorld) -> None:
        cfg = world.config
        events = [
            label_event(
                1,
                "labeled",
```

### tests/issue_watch/test_module_boundaries.py:15-80

```python
Rule encoded where the code and the design wording differ:

* ``superclaude.cli.swarm.atomic`` may be imported by ``record`` inside any
  function (``FileStore.save`` and ``save_dry_run`` both do), never at module level.
  Design C18 says "inside ``save``".
* ``record`` may import any name from ``predicates`` (it imports three functions
  and one type); design 5.3 says "types only". The rule is checked per module.
"""

from __future__ import annotations

import ast
import sys
from dataclasses import dataclass, field
from pathlib import Path, PurePath

import pytest

PACKAGE = "superclaude.cli.issue_watch"
PACKAGE_DIR = Path(__file__).resolve().parents[2] / "src/superclaude/cli/issue_watch"
ATOMIC = "superclaude.cli.swarm.atomic"
INSTALL_USER_SETUP = "superclaude.cli.install_user_setup"
EXPECTED_PROTOCOLS = {"Runner", "Store", "Launcher", "Clock"}


@dataclass(frozen=True)
class Rule:
    """What one module may import besides the standard library."""

    siblings: frozenset[str] = frozenset()
    superclaude: frozenset[str] = frozenset()  # exact module targets
    third_party: frozenset[str] = frozenset()  # top-level distribution names
    function_only: frozenset[str] = frozenset()  # targets never at module level
    names_only: dict[str, frozenset[str]] = field(default_factory=dict)


RULES: dict[str, Rule] = {
    "__init__": Rule(),
    "runner": Rule(),
    "predicates": Rule(),
    "audit": Rule(),
    "github": Rule(siblings=frozenset({"runner", "predicates"})),
    "record": Rule(
        siblings=frozenset({"predicates"}),
        superclaude=frozenset({ATOMIC}),
        function_only=frozenset({ATOMIC}),
    ),
    "launch": Rule(
        siblings=frozenset({"runner"}),
        superclaude=frozenset({INSTALL_USER_SETUP}),
        names_only={INSTALL_USER_SETUP: frozenset({"_ORCA_CLIS"})},
    ),
    "cycle": Rule(
        siblings=frozenset(
            {"runner", "github", "predicates", "record", "launch", "audit"}
        )
    ),
    "cli": Rule(
        siblings=frozenset({"cycle", "record", "audit", "launch", "runner"}),
        third_party=frozenset({"click"}),
    ),
}


@dataclass(frozen=True)
class Imp:
```

### tests/issue_watch/test_module_boundaries.py:219-281

```python
def test_package_has_exactly_the_designed_modules() -> None:
    """NFR-014, AC-25: the package holds exactly the designed modules."""
    assert set(_sources()) == set(RULES), (
        "the package modules differ from design 5.3 (add a row to RULES only "
        "with a design change)"
    )
    assert stray_directories() == [], "the design has no sub-package"


def test_package_listing_reaches_a_sub_package(tmp_path: Path) -> None:
    """A nested module is listed under a dotted name and its directory is stray."""
    (tmp_path / "sub").mkdir()
    (tmp_path / "sub" / "__init__.py").write_text("", encoding="utf-8")
    (tmp_path / "sub" / "x.py").write_text("import subprocess\n", encoding="utf-8")
    (tmp_path / "__pycache__").mkdir()
    (tmp_path / "cycle.py").write_text("", encoding="utf-8")
    assert set(package_sources(tmp_path)) == {"cycle", "sub.__init__", "sub.x"}
    assert not set(package_sources(tmp_path)) <= set(RULES)
    assert stray_directories(tmp_path) == ["sub"]


@pytest.mark.parametrize("module", sorted(RULES))
def test_module_imports_obey_the_design_table(module: str) -> None:
    """NFR-014, AC-25: each module imports only what the design table allows."""
    source = _sources()[module]
    imports = collect_imports(source, f"{module}.py")
    if module != "__init__":
        assert imports, f"{module}.py: the scan found no import (walker is blind)"
    found = violations(module, imports, RULES[module])
    assert not found, "forbidden imports:\n" + "\n".join(found)


def test_real_relative_imports_resolve_to_the_package() -> None:
    """The walker sees sibling imports written in relative form (research F6)."""
    cli = {i.module for i in collect_imports(_sources()["cli"])}
    assert f"{PACKAGE}.cycle" in cli  # ``from . import audit, cycle, record``
    assert f"{PACKAGE}.launch" in cli  # ``from .launch import ...``
    assert "click" in cli


def test_record_defers_atomic_and_fcntl_to_function_level() -> None:
    """NFR-014, DF-29: swarm.atomic and fcntl are imported inside functions only."""
    imports = collect_imports(_sources()["record"])
    atomic = [i for i in imports if i.module == ATOMIC]
    fcntl = [i for i in imports if i.module == "fcntl"]
    assert atomic and fcntl, "record no longer defers swarm.atomic or fcntl"
    assert all(i.in_function for i in atomic + fcntl)
    assert any(i.module == f"{PACKAGE}.predicates" for i in imports)


def test_no_module_is_named_select() -> None:
    """NFR-014, AC-25: no module or directory of the package is named select."""
    rel = [p.relative_to(PACKAGE_DIR) for p in PACKAGE_DIR.rglob("*")]
    assert rel, "package directory is empty"
    assert select_named(rel) == []


def test_exactly_four_protocol_classes() -> None:
    """NFR-014, AC-25: exactly four Protocols exist (runner, store, launcher, clock)."""
    found: list[str] = []
    for path in PACKAGE_DIR.rglob("*.py"):
        found += protocol_class_names(path.read_text(encoding="utf-8"))
    assert sorted(found) == sorted(EXPECTED_PROTOCOLS), found
```

### tests/issue_watch/test_cli.py:960-972

```python
    config.state_dir.mkdir()
    (config.state_dir / "dispatch.json").write_text("{not json", encoding="utf-8")
    result = run_readonly(tmp_path, "status", "--json", "--config", str(config_file))
    assert result.exit_code == 6
    assert result.output == "issue-watch: store_invalid\n"


@pytest.mark.skipif(os.geteuid() == 0, reason="root reads any file")
def test_status_exits_6_for_an_unreadable_store(tmp_path, config, config_file):
    seed_store(config)
    store_file = config.state_dir / "dispatch.json"
    store_file.chmod(0)
    try:
```

### tests/issue_watch/test_cli.py:1064-1074

```python
CYCLE_ID_SHAPE = re.compile(r"[0-9a-f]{32}")
ISSUE_FLAGS = ("9", "--forfeit-guarantee")
RATE_FLAGS = ("--rate-limit",)
BOTH_FORMS = pytest.mark.parametrize(
    "flags", [ISSUE_FLAGS, RATE_FLAGS], ids=["issue", "rate"]
)
NOT_ROOT = pytest.mark.skipif(os.geteuid() == 0, reason="root ignores file modes")


def assert_lock_free(config: cycle.Config) -> None:
    """A lock taken after the run succeeds: the run released (or never took) it."""
```

### tests/issue_watch/test_record.py:735-745

```python
        hold(tmp_state)
    assert info.value.reason == "lock_invalid"


@pytest.mark.skipif(os.geteuid() == 0, reason="root ignores file permission bits")
def test_ac11_unopenable_lock_file_is_lock_invalid__fr017(tmp_state):
    """A lock the user cannot open is a typed ``lock_invalid``, not a raw OSError (B-3)."""
    lock = tmp_state.state_dir / "lock"
    os.chmod(lock, 0)
    try:
        with pytest.raises(LockError) as info:
```

### tests/issue_watch/test_cycle.py:730-740

```python
    assert len(content) == 1024 * 1024 + 1
    path = _approvers(tmp_path, content)
    _expect("approvers_invalid", "too large", cycle.validate_approvers, path)


@pytest.mark.skipif(os.geteuid() == 0, reason="root reads an unreadable file")
def test_validate_approvers_unreadable_file__fr027(tmp_path):
    path = _approvers(tmp_path, "1001\n", mode=0o200)
    _expect("approvers_invalid", "cannot be read", cycle.validate_approvers, path)


```

### tests/issue_watch/test_cycle.py:4690-4700

```python


def test_the_real_proc_mountinfo_gives_a_filesystem_type_for_the_root__df52_c13():
    if sys.platform != "linux":
        pytest.skip("/proc/self/mountinfo exists on Linux only")
    text = _REAL_READ_MOUNTINFO()
    assert text is not None
    assert cycle.fs_type_of("/", text) is not None


def test_read_mountinfo_returns_the_file_text_and_none_when_it_is_missing__df52_c13(
```

### tests/issue_watch/test_cli_e2e.py:1-40

```python
"""End-to-end tests of ``superclaude issue-watch`` as a real process (plan step 8.2).

Each test runs ``python -m superclaude.cli.main issue-watch ...`` with an
explicit ``env=`` from the ``stub_path`` fixture, so the only ``gh``, ``orca``,
``orca-ide`` and ``git`` the process can reach are the PATH stubs written into
``tmp_path`` (decisions DF-10, DF-34, DF-55, DF-56). Replies are built from the
``GhWorld`` fixtures, with event times generated after ``init-state`` has
stamped the store ``created_at`` from the real clock.

Covers FR-001, FR-003, FR-010, FR-013, NFR-002, NFR-009, NFR-010 and AC-1.
The sleeping-stub timeout (AC-19) is not tested here: it is split into a runner
unit test and in-process cycle tests (DF-55).
"""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

from superclaude.cli.issue_watch import cycle, github
from superclaude.cli.issue_watch.predicates import parse_utc

from .conftest import (
    APPROVER_ID,
    OWN_LOGIN,
    PROJECT_ID,
    STUB_TOOLS,
    FakeClock,
    GhWorld,
    label_event,
    load_fixture,
    make_config,
    read_calls,
    write_scenario,
)

```

## Coverage slice

Rows for reviewer 2 (qa): acceptance criteria AC-1..AC-25, partial and gate-only rows, falsified Task Summary claims and S_dev_density inputs, verbatim from artifacts/coverage-matrix.yaml (lines 116-183 and 427-571). The helper that built them is NOT trusted; re-verify the proofs you rely on, especially whether each test would really fail if the behaviour were removed.

```yaml
falsified_claims:        # Task Summary (tasklist lines 881-914) checked against disk and git
  - id: FC-1
    claim: "Step 10.1 text (tasklist line 847) names 13 files under tests/issue_watch/fixtures/_assumed_shape/"
    reality: "19 on disk (find -type f = 19). All 13 names planned in Steps 3.2-3.5 and 5.2 exist; 6 were added later: gh_api_user_include_429, gh_issue_reread, gh_stderr_http_502, gh_stderr_scope_read_project, orca_launch_empty_operation_id, orca_launch_no_operation_id."
    verdict: "Stale statement in the task BODY (line 847), not in the Task Summary. The Summary's '19 fixture files' (line 889) is TRUE."
    severity: minor
  - id: FC-2
    claim: "Task Summary line 883 '(Populated by Step 10.5 from the named result files.)'"
    reality: "Template instruction line left in place above the populated text."
    severity: cosmetic
  - id: FC-3
    claim: "Task Summary line 905: 'the table has 59 names, not 57', two reason names added by the executor"
    reality: "59 is TRUE (audit.py:26-102, 59 entries, pinned by test_audit.py:214-225). But the spec-final closed table (spec-final.md:332-358) holds 52 names; the 7 extras are marker_unreadable, edits_unreadable, dry_run_shadow_reset, reset_refused, operator_reset (decisions DF-22/DF-57) and cycle_complete, cycle_crashed (Gate C executor proposals). Wording 'not 57' refers to the plan's own count, not the spec's."
    verdict: "Not falsified; context for the deviation classifier. The 'closed' enum was widened by 7 against the spec text."
    severity: note
  - id: FC-4
    claim: "Task Summary line 889: AC-1 to AC-25 trace '68 rows PASS'"
    reality: "68 rows exist (grep) and each is marked PASS, but AC-23 (no dependency change) has no pytest test (gate-only, see requirements AC-23) and AC-19 is a documented split (DF-55). The word PASS is therefore gate-and-test mixed, not 68 test-proven rows."
    severity: note

claims_verified_true:     # Task Summary statements that match disk and git
    - "9 src files in IW (8 modules + empty __init__): wc -l 4743 lines total"
    - "19 test_*.py files + conftest.py + __init__.py + 19 fixtures = 40 test-tree paths (git diff --name-only)"
    - "five verbs check-config, init-state, once, reset, status (p7-g9.txt; cli.py:111,164,185,201,282)"
    - "main.py +4 lines (git diff): 2 blank + import + add_command at main.py ~563-566"
    - "379 files, 87301 insertions, parent == BASE (git show --shortstat, git rev-parse 26f551f4^)"
    - "pyproject.toml, Makefile, .github unchanged in the commit (git diff --stat over those paths lists only main.py)"
    - "fix cycles: A 2, B 1, C 2, D 1, Final 1, M4 1 (verdict files)"
    - "2635 passed / 0 skipped (p9-g1-summary.md); 2665 passed + 1 pre-existing skip (p9-g2-summary.md)"
    - "pytest.skip/skipif at 5 sites: test_cli.py:967, test_cli.py:1070, test_record.py:739, test_cycle.py:735, test_cycle.py:4694 (all root or platform guards)"
    - "no remote branch for this issue exists (git for-each-ref refs/remotes shows none), consistent with 'no push, no PR'"
    - "qa/gate-c has qa-content-design-correctness-report-run2.md (the restore mentioned in the Summary)"
claims_unverified: ["'Python 3.10.20 ran the suite in Gates D and Final' (only p9-g7.txt and QA reports mention 3.10.20; run output not re-read)", "'4 environmental failures outside issue_watch in a local full run' (not re-run)"]

# =============================================================================
# S_dev_density inputs (whole files used as hunks)
# =============================================================================
s_dev_density:
  total_changed_paths: 379
  by_group:
    src: 10                 # 9 IW files + main.py
    tests: 40               # 19 test files + conftest + __init__ + 19 fixtures
    docs: 2                 # docs/designs/issue-watcher.md, docs/designs/issue-watcher-setup.md
    dev_process_artifacts: 327   # all under .dev/tasks/to-do/
  dev_breakdown:
    TASK-RF package: 244
    TASK-RESEARCH-issue-watcher-20261107-064950 package: 83   # predecessor research task
  mapped_to_a_tasklist_step:
    count: 260
    detail:
      src: "10 of 10 (Steps 1.6, 2.1-2.3, 3.1, 4.1, 5.1, 6.1-6.3, 7.1-7.3)"
      tests: "40 of 40 (Steps 1.7, 2.4-2.8, 3.2-3.7, 4.2-4.5, 5.2-5.8, 6.4-6.9, 7.4-7.5, 8.1-8.8)"
      docs: "1 of 2 (issue-watcher-setup.md, Steps 9.1-9.2)"
      qa_gate_files: "83 (qa/gate-a 14, gate-b 14, gate-c 15, gate-d 14, final 15, m4 11; Steps x.G*, 9.F*, 9.M*)"
      phase_outputs: "83 (git ls-tree of HEAD: discovery 3, plans 13, reports 9, reviews 2, test-results 56; Steps 1.3-1.5, 2.9-2.11, ..., 9.4-9.19, 10.2)"
      reflect_pre: "43 (PRE reflect, frontmatter reflect_pre at tasklist line 31, run before Phase 1; has no numbered Step)"
  unmapped:
    count: 119
    detail:
      - "docs/designs/issue-watcher.md (1): the driving design, committed unchanged (DF-07/DF-31)"
      - "PKG/qa top-level files (26): the task-builder's own pre-execution QA reports (qa-*.md, analyst-*.md, .fix2-done)"
      - "PKG inputs (9): BUILD-REQUEST.md, research/01-06 (6), research-notes.md, the tasklist file itself"
      - "TASK-RESEARCH-issue-watcher-20261107-064950 package (83): the earlier research task, staged by the Step 10.3 allowlist only"
    unmapped_in_src_or_tests: 0
  ratio:
    unmapped_hunks_over_total_hunks: "119/379 = 0.314"
    source_and_tests_only: "0/51 unmapped (src 10 + tests 40 + setup doc 1 all map to Steps)"
  untracked_at_review_time: ["PKG/phase-outputs/plans/commit-allowlist-check.md", "PKG/phase-outputs/plans/commit-result.md", "PKG/reflect/post/", ".dev/brainstorms/20261107-064825-github-issue-watcher/", ".dev/issues/331/"]
  # ---------------------------------------------------------------- AC
  - id: AC-1
    status: covered
    impl: ["IW/cycle.py:663-720"]
    tests: ["T/test_cycle.py:1283,1314", "T/test_cli_e2e.py:299"]
    bites: yes
  - id: AC-2
    status: covered
    impl: ["IW/github.py:180-198, 804-842"]
    tests: ["T/test_github.py:126,1271,1279", "T/test_cycle.py:1640,1658"]
    bites: yes
  - id: AC-3
    status: covered
    impl: ["IW/predicates.py:185-259"]
    tests: ["T/test_predicates.py:147-283,363-415", "T/test_cycle.py:2461"]
    bites: yes (outsider, bot, unlabel, relabel, incomplete, edit after approval all present)
  - id: AC-4
    status: covered
    impl: ["IW/predicates.py:162-174, 262-271"]
    tests: ["T/test_predicates.py:440,460,477", "T/test_cycle.py:2461,3215"]
    bites: yes
  - id: AC-5
    status: covered
    impl: ["IW/cycle.py:877-894, 927-928"]
    tests: ["T/test_cycle.py:2690"]
    bites: yes
  - id: AC-6
    status: covered
    impl: ["IW/cycle.py:960-997, 1052-1062"]
    tests: ["T/test_cycle.py:2925,3181,3261"]
    bites: yes
  - id: AC-7
    status: covered
    impl: ["IW/launch.py:84-102"]
    tests: ["T/test_launch.py:41-69", "T/test_security_invariants.py:451"]
    bites: yes
  - id: AC-8
    status: covered
    impl: ["IW/launch.py:95-116, 311-334", "IW/cycle.py:1062-1075"]
    tests: ["T/test_launch.py:75,596-700", "T/test_cycle.py:3032,3065,3122,3231"]
    bites: yes
  - id: AC-9
    status: covered
    impl: ["IW/cycle.py:1271-1288", "IW/launch.py:119-132"]
    tests: ["T/test_cycle.py:2536", "T/test_cli.py:842,885", "T/test_launch.py:152"]
    bites: yes
  - id: AC-10
    status: covered
    impl: ["IW/record.py:689-720", "IW/cycle.py:848-857"]
    tests: ["T/test_cycle.py:4120 (N=1,2,6,7,50,99; 48 cycles + 24 h later)", "T/test_cycle.py:2645,2673", "T/test_cli.py:1439", "T/test_record.py:1606,1622"]
    bites: yes
  - id: AC-11
    status: covered
    impl: ["IW/record.py:380-419"]
    tests: ["T/test_concurrency.py:146,215,230,243,255"]
    bites: yes (real second process)
  - id: AC-12
    status: covered
    impl: ["IW/cycle.py:666-667, 693-694"]
    tests: ["T/test_cycle.py:1430,1446"]
    bites: yes
  - id: AC-13
    status: covered
    impl: ["IW/cycle.py:1109-1125", "IW/record.py:805-865"]
    tests: ["T/test_cycle.py:3685 (store bytes identical, shadow file exact)", "T/test_record.py:2008,2054,2104"]
    bites: yes
  - id: AC-14
    status: covered
    impl: ["IW/audit.py:123-197, 381-404", "IW/cycle.py:1139-1174"]
    tests: ["T/test_cycle.py:2017,4533", "T/test_audit.py:580 (keeps exactly 4 rotated files),674"]
    bites: yes
  - id: AC-15
    status: covered
    impl: ["IW/cycle.py:443-458 resolve_exit (2,6,7,5,3,4 then 75 only if sole)"]
    tests: ["T/test_cycle.py:813-912 (every pair and subset)", "T/test_cycle.py:1584"]
    bites: yes
  - id: AC-16
    status: covered
    impl: ["IW/launch.py:200-236"]
    tests: ["T/test_cycle.py:1498", "T/test_origin_parity.py:90-179"]
    bites: yes
  - id: AC-17
    status: covered
    impl: ["IW/cli.py:94-348"]
    tests: ["T/test_cli.py:351,988,1213,1234,1406", "T/test_cli.py:405,952-980 (exit codes)"]
    bites: yes
  - id: AC-18
    status: covered
    impl: ["IW/github.py:418-431", "IW/cycle.py:644-649", "IW/cli.py:243", "IW/record.py:723"]
    tests: ["T/test_cycle.py:1751,1812", "T/test_cli.py:1488", "T/test_record.py:1675"]
    bites: yes
    note: "Retry-After only on G1 (see FR-028)"
  - id: AC-19
    status: partial
    impl: ["IW/cycle.py:383-412, 1039-1049"]
    tests: ["T/test_cycle.py:1897,1964 (121 s: no launch),1982", "T/test_runner.py:217"]
    bites: "yes per half"
    note: "AUTHORIZED SPLIT (DF-55): no end-to-end sleeping PATH stub (T/test_cli_e2e.py:11-13)"
  - id: AC-20
    status: covered
    impl: ["IW/github.py:175-262"]
    tests: ["T/test_security_invariants.py:637,668,697,864,879"]
    bites: yes
  - id: AC-21
    status: covered
    impl: ["IW/runner.py:82-101"]
    tests: ["T/test_no_shell.py:150,156"]
    bites: yes
  - id: AC-22
    status: covered
    impl: ["IW/cycle.py:1052-1125", "IW/record.py:627-651"]
    tests: ["T/test_crash_injection.py:217-347", "T/test_cycle.py:4074,4177"]
    bites: yes
  - id: AC-23
    status: gate-only
    impl: ["none"]
    tests: ["no pytest test; gates G-6 (make verify-deps, test-results/p9-g6-verify-deps.txt) and G-10 (p9-g10.txt); git diff --stat confirms pyproject.toml, Makefile, .github unchanged"]
    bites: "n/a"
  - id: AC-24
    status: covered
    impl: ["IW/cycle.py:1322-1369"]
    tests: ["T/test_slo_helper.py:399"]
    bites: yes
  - id: AC-25
    status: covered
    impl: ["IW package layout"]
    tests: ["T/test_module_boundaries.py:219-281", "T/test_find_orca_parity.py:145-270", "T/test_origin_parity.py:90"]
    bites: yes

gaps: []
partials:
  - {id: NFR-008, reason: "no single end-to-end sleeping-stub test; split by DF-55 into T/test_runner.py:217 and T/test_cycle.py:1897", loc: "T/test_cli_e2e.py:11-13"}
  - {id: AC-19,   reason: "same authorized split as NFR-008", loc: "T/test_cli_e2e.py:11-13"}
  - {id: NFR-014, reason: "'every time read goes through the clock' has no test; wall-clock reads remain at IW/audit.py:396 and IW/runner.py:89", loc: "IW/audit.py:396"}
gate_only:
  - {id: NFR-012, reason: "dependency-list-unchanged proved only by gate output p9-g6-verify-deps.txt and p9-g10.txt"}
  - {id: AC-23,   reason: "same as NFR-012"}

weak_spots_not_gaps:
  - "T/test_cli.py:862 builds the expected retry text with production retry_argv (pinned separately by T/test_launch.py:152)"
  - "T/test_marker_contract.py:51 asserts only CLAIM_MARKER in MARKER_JQ"
  - "4 skipif(root) sites (T/test_cli.py:967, T/test_cli.py:1070, T/test_record.py:739, T/test_cycle.py:735) and 1 platform skip (T/test_cycle.py:4694): FR-017 unopenable lock, FR-027 unreadable approvers file, FR-021 unreadable store and reset file-mode cases skip silently if CI runs as root"
  - "all gh and Orca reply shapes are `_assumed_shape` fixtures (UNVERIFIED, FU-1, FU-3): tests prove behaviour against assumed shapes only; the deployment gate in design section 1 covers this"
  - "closed reason table widened from 52 spec names to 59 (see falsified_claims FC-3)"
authorized_departures_seen_in_code: ["FR-013 launch runs with cwd=worktree (DF-01)", "FR-015 full retry argv (Q2, C20)", "FR-016 S1 stop-after-launch-step (Q1, DF-50)", "FR-019 dry-run skips re-read and probe (OQ-39)", "FR-028 header honoured on G1 only (DF-51)", "NFR-008/AC-19 split (DF-55)"]
```

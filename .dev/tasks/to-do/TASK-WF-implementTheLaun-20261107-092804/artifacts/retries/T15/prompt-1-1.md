b4448b44d29f2f1fb21048c4848e87d2e84e598a
Review one task for spec compliance.

Task brief: ## Task 15: Measure hook speed, including the cost the identity hook adds to ordinary sessions

Depends on: Task 14

Add the speed tests of design section 8 to tests/hooks/test_launch_level_guard.py and write the measured numbers to ./artifacts/speed-results.md (finding F2). Use 100 runs per case with time.monotonic(). T-SPD-1 and T-SPD-2: ordinary session, empty store and a store with 1,050 session files, report median and p95 against the targets 20 ms and 50 ms. T-SPD-3: ordinary median of the guard against src/superclaude/hooks/scripts/block-bare-python.sh in the same run, asserted at 1.5 times or less. T-SPD-4: governed allow and block, report p95 against 60 ms. T-SPD-5: governed commands of 64 KB and a 1 MB command, asserted under 1 second each. Add an envelope stress case with a very large non-command field and report time and memory or a timeout as an explicit result. For F2, also measure an ordinary Bash call through launch-job-identity.sh with a store directory that holds only a pending/ entry (the state a claim creates) and report the median against the same call with no store; the identity hook is not modified.

Acceptance criteria:
- uv run pytest tests/hooks/test_launch_level_guard.py -k "SPD or speed" -v passes with T-SPD-3 and T-SPD-5 asserted.
- ./artifacts/speed-results.md exists with a table of case, runs, median, p95, target and result, a row for the large-envelope case, and a row for the identity hook with a non-empty store.
- If any asserted target fails, the failure is shown in the file and in the test output; no target is relaxed. If a reported-only target is exceeded, the file says so in one sentence and names the follow-up (no change to launch-job-identity.sh in this plan).

AC ids (source order):
T15.AC1: uv run pytest tests/hooks/test_launch_level_guard.py -k "SPD or speed" -v passes with T-SPD-3 and T-SPD-5 asserted.
T15.AC2: ./artifacts/speed-results.md exists with a table of case, runs, median, p95, target and result, a row for the large-envelope case, and a row for the identity hook with a non-empty store.
T15.AC3: If any asserted target fails, the failure is shown in the file and in the test output; no target is relaxed. If a reported-only target is exceeded, the file says so in one sentence and names the follow-up (no change to launch-job-identity.sh in this plan).
Global constraints: - docs/designs/sc-issue-launch-level-hook.md is the authority for this plan. The requirements file .dev/brainstorms/20261105-170229-launch-level-hook/merged-requirements.md (called MR below) is the historical baseline for requirement ids and the test corpus; where the design says it overrides MR (design section 11, DD-2), the design wins. .dev/brainstorms/20261105-024132-issue-claim-orca-worktree-flag/launch-levels-addendum.md defines the claim side; the hook interface rules IR-1 to IR-7 in design section 13 win over it.
- This branch builds on open PR 425 (ironbelly/sc-issue-claim-pipeline-flag). The claim code in src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py already writes the launch record and marks the prompt (IR-1, IR-2); do not rebuild that.
- The L1 guard is one flat bash script using only bash, jq, sed and tr: exit 0 allows, exit 2 blocks, no onFailure, no Python, no git or network call on ordinary classification. No new runtime service, managed settings deployment, shell parser, hook forwarding framework or git config migration (design section 1).
- Do not change src/superclaude/hooks/scripts/launch-job-identity.sh or tests/hooks/test_launch_job_identity.py. A conflict found with it goes into the record of Task 14, not into that file.
- Ordinary sessions are never blocked by any failure (FR-L-53). Only a positively identified governed session fails closed.
- Live observations (OB-H1, OB-H2, OB-H3, OB-CTX) need real governed sessions or real launches. This plan runs none of them and never launches a governed agent on a real issue or pushes to a real protected branch. They stay pending (a skipped test with a stated reason), never reported as passed. Tests use a temporary HOME and temporary bare remotes.
- Acceptance claims cover the routes the tests exercise. Nothing here claims universal merge protection or defence against a hostile agent (design sections 1 and 12).
- Gate: Task 1 writes the B-CTX verdict. If ./artifacts/b-ctx-verdict.md contains the line "L1: STOP", stop the run at Task 1 and report that verdict; do not start Task 2 or any later task. Every task after Task 1 depends on that verdict.
- Existing tests: any task that changes a check in src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py also migrates the shared test fixture launch_scene in tests/skills/test_issue_orca_worktree.py (it writes only a bare shell stub today) and names every test whose result changes. Test code must unset CLAUDE_CONFIG_DIR and control which jq is on PATH, so results do not depend on the developer's machine.
- Edit only under src/superclaude/, plugins/superclaude/hooks/, tests/, docs/ and this package's ./artifacts/; run make sync-dev after hook or skill edits. The plugin copy of every hook script and hooks.json stays byte-identical to its src copy. Generated .claude/ mirrors made by make sync-dev stay out of the commit.
- UV only: run tests with uv run pytest.
- Findings of the issue analysis that this plan answers: F2 (Task 15), F3 (Task 14), F4 (Tasks 18 to 20), F6 (Task 22), F7 (Task 1). F5 (pending records are not pruned) is accepted under owner decision O-15 and is stated in Task 22.
Start sha: b4448b44d29f2f1fb21048c4848e87d2e84e598a
Diff against the start snapshot: diff --git a/.dev/tasks/to-do/TASK-WF-implementTheLaun-20261107-092804/artifacts/speed-results.md b/.dev/tasks/to-do/TASK-WF-implementTheLaun-20261107-092804/artifacts/speed-results.md
new file mode 100644
index 00000000..4589b592
--- /dev/null
+++ b/.dev/tasks/to-do/TASK-WF-implementTheLaun-20261107-092804/artifacts/speed-results.md
@@ -0,0 +1,36 @@
+# Task 15: hook speed results
+
+Written by the test module tests/hooks/test_launch_level_guard.py (section
+"Task 15: speed") at the end of the run below; no number is edited by hand.
+
+- Run: 2026-11-07 17:11 UTC, `LL_SPEED_RESULTS=<this file> uv run pytest tests/hooks/test_launch_level_guard.py -k "SPD or speed"`.
+- Host: GNU bash, version 5.2.37(1)-release (x86_64-pc-linux-gnu); 28 CPUs; load average 3.60 2.78 2.28 when the file was written; Python 3.11.15.
+- Method: each run is one real subprocess (bash and the hook script), timed with time.monotonic() around subprocess.run after one untimed warm-up run. p95 is the inclusive 95th percentile. PATH holds only a temporary bin directory; HOME is a temporary directory. T-SPD-5 uses 25 runs per command instead of 100 (each run takes 0.5 to 0.9 s); the envelope stress case uses 5 runs, with p95 taken from those runs.
+- Asserted (design section 8): T-SPD-3 (guard median at most 1.5 times block-bare-python.sh) and T-SPD-5 (every run under 1 s). Every other row is reported only.
+
+| Case | Runs | Median | p95 | Target | Result |
+|---|---|---|---|---|---|
+| T-SPD-1 guard, ordinary, empty store | 100 | 3.2 ms | 3.7 ms | median 20 ms, p95 50 ms | within (reported only) |
+| T-SPD-2 guard, ordinary, store of 1,050 files | 100 | 9.1 ms | 10.4 ms | median 20 ms, p95 50 ms | within (reported only) |
+| T-SPD-3 block-bare-python.sh, ordinary, empty store (same run) | 100 | 7.3 ms | 8.5 ms | baseline for T-SPD-3 | baseline |
+| T-SPD-3 guard, ordinary, empty store (same run) | 100 | 3.3 ms | 4.1 ms | median at most 1.5 times block-bare-python.sh (asserted) | PASS: ratio 0.46 |
+| T-SPD-3 block-bare-python.sh, ordinary, store of 1,050 files (same run) | 100 | 7.3 ms | 8.4 ms | baseline for T-SPD-3 | baseline |
+| T-SPD-3 guard, ordinary, store of 1,050 files (same run) | 100 | 8.5 ms | 9.6 ms | median at most 1.5 times block-bare-python.sh (asserted) | PASS: ratio 1.17 |
+| T-SPD-4 guard, governed F, allow `git status` | 100 | 14.2 ms | 16.2 ms | p95 60 ms | within (reported only) |
+| T-SPD-4 guard, governed F, block `git commit -m x` | 100 | 14.4 ms | 16.3 ms | p95 60 ms | within (reported only) |
+| T-SPD-5 guard, governed FS, heredoc-git-words-64KB | 25 | 525.4 ms | 553.4 ms | every run under 1 s (asserted) | PASS: max 565.3 ms; exit [2] |
+| T-SPD-5 guard, governed FS, backslash-lines-64KB | 25 | 521.0 ms | 540.5 ms | every run under 1 s (asserted) | PASS: max 543.4 ms; exit [0] |
+| T-SPD-5 guard, governed FS, git-status-lines-64KB | 25 | 750.2 ms | 785.5 ms | every run under 1 s (asserted) | PASS: max 787.8 ms; exit [0] |
+| T-SPD-5 guard, governed FS, 1MB-big | 25 | 446.2 ms | 469.8 ms | every run under 1 s (asserted) | PASS: max 480.9 ms; exit [2] |
+| Envelope stress, guard, ordinary, 32 MiB description field | 5 | 840.1 ms | 897.5 ms | none; report time and memory, or a timeout | completed, exit [0], peak RSS 162 MiB (largest process of the hook tree) |
+| Envelope stress, guard, governed F, 32 MiB description field | 5 | 883.8 ms | 906.0 ms | none; report time and memory, or a timeout | completed, exit [0], peak RSS 162 MiB (largest process of the hook tree) |
+| F2 launch-job-identity.sh, ordinary Bash, no store | 100 | 2.0 ms | 2.3 ms | median 20 ms, p95 50 ms (ordinary budget, reported only) | within (reported only) |
+| F2 launch-job-identity.sh, ordinary Bash, store with only pending/ | 100 | 79.2 ms | 85.9 ms | median 20 ms, p95 50 ms (ordinary budget, reported only) | EXCEEDED (reported only) |
+
+## Reported targets exceeded
+
+- F2 launch-job-identity.sh, ordinary Bash, store with only pending/ exceeded its reported target (median 20 ms, p95 50 ms (ordinary budget, reported only)); follow-up: a follow-up change to launch-job-identity.sh that checks sessions/<session_id> in bash before starting uv (this plan does not modify that script).
+
+## Asserted targets failed
+
+None.
diff --git a/.dev/tasks/to-do/TASK-WF-implementTheLaun-20261107-092804/artifacts/t15-test.log b/.dev/tasks/to-do/TASK-WF-implementTheLaun-20261107-092804/artifacts/t15-test.log
new file mode 100644
index 00000000..636beb51
--- /dev/null
+++ b/.dev/tasks/to-do/TASK-WF-implementTheLaun-20261107-092804/artifacts/t15-test.log
@@ -0,0 +1,11 @@
+============================= test session starts ==============================
+platform linux -- Python 3.11.15, pytest-9.2.0, pluggy-1.7.0
+SuperClaude: 5.0.0
+rootdir: /home/coder/workspaces/worktrees/IronClaude/issue-394-launch-level-hook
+configfile: pyproject.toml
+plugins: superclaude-5.0.0, anyio-4.16.0
+collected 3179 items / 3166 deselected / 13 selected
+
+tests/hooks/test_launch_level_guard.py .............                     [100%]
+
+================ 13 passed, 3166 deselected in 83.03s (0:01:23) ================
diff --git a/tests/hooks/test_launch_level_guard.py b/tests/hooks/test_launch_level_guard.py
index 633d726c..8367a10a 100644
--- a/tests/hooks/test_launch_level_guard.py
+++ b/tests/hooks/test_launch_level_guard.py
@@ -21,7 +21,11 @@ import json
 import os
 import re
 import shutil
+import statistics
 import subprocess
+import sys
+import time
+from datetime import datetime, timezone
 from pathlib import Path
 
 import pytest
@@ -983,6 +987,400 @@ def test_skill_name_newline_does_not_shift_fields(tmp_path):
     _assert_decision(result, tmp_path, None, "W")
 
 
+# ===========================================================================
+# Task 15: speed (T-SPD-1 to T-SPD-5, design section 8, MR NFR-L-01; F2).
+#
+# Real subprocess runs timed with time.monotonic() around subprocess.run, after
+# one untimed warm-up run; 100 runs per case unless the row says otherwise.
+# Only T-SPD-3 (ratio) and T-SPD-5 (1 s each) assert; the millisecond targets
+# are printed and reported, not asserted, because they are flaky on a loaded
+# host. Run with -s to see the numbers. With LL_SPEED_RESULTS=<path> set, the
+# module writes the table of this run to that path after its last test.
+# ===========================================================================
+
+SPD_RUNS = 100
+# shortcut: a 64 KB run takes 0.5 to 0.9 s, so 100 runs of four commands would
+# add over 3 minutes to every run of this file; raise for a release benchmark.
+LARGE_RUNS = 25
+BLOCK_BARE_PYTHON = HOOK.parent / "block-bare-python.sh"
+IDENTITY = HOOK.parent / "launch-job-identity.sh"
+SPD_COMMAND = "git status && ls -la src"
+ENVELOPE_BYTES = 32 * 1024 * 1024
+ENVELOPE_RUNS = 5
+ENVELOPE_TIMEOUT = 30
+GUARD_FOLLOW_UP = (
+    "profile the ordinary path of launch-level-guard.sh in a follow-up issue"
+)
+IDENTITY_FOLLOW_UP = (
+    "a follow-up change to launch-job-identity.sh that checks sessions/<session_id> "
+    "in bash before starting uv (this plan does not modify that script)"
+)
+_SPD_ROWS: list[dict] = []
+
+
+@pytest.fixture(scope="module")
+def speed_report():
+    yield _SPD_ROWS
+    target = os.environ.get("LL_SPEED_RESULTS")
+    if target and _SPD_ROWS:
+        Path(target).write_text(_spd_markdown())
+
+
+def _spd_env(tmp_path: Path, home: Path, extra: tuple[str, ...] = ()) -> dict:
+    bindir = tmp_path / "bin"
+    if not bindir.exists():
+        _bin(tmp_path)
+        for tool in extra:
+            (bindir / tool).symlink_to(shutil.which(tool))
+    home.mkdir(exist_ok=True)
+    return _env(home, bindir)
+
+
+def _spd_once(script: Path, stdin: bytes, env: dict, timeout: float = 10):
+    started = time.monotonic()
+    result = subprocess.run(
+        [BASH, str(script)], input=stdin, capture_output=True, env=env, timeout=timeout
+    )
+    return time.monotonic() - started, result
+
+
+def _spd_time(script: Path, stdin: bytes, env: dict, runs: int = SPD_RUNS):
+    _spd_once(script, stdin, env)  # warm-up, not counted
+    times, codes = [], set()
+    for _ in range(runs):
+        seconds, result = _spd_once(script, stdin, env)
+        times.append(seconds)
+        codes.add(result.returncode)
+    return times, codes
+
+
+def _ms(times: list[float]) -> tuple[float, float]:
+    """Median and 95th percentile in milliseconds."""
+    p95 = statistics.quantiles(times, n=20, method="inclusive")[18]
+    return statistics.median(times) * 1000, p95 * 1000
+
+
+def _spd_row(case, runs, times, target, result, follow_up="", note=""):
+    median, p95 = _ms(times)
+    if result == "reported":
+        limits = [float(x) for x in re.findall(r"(\d+) ms", target)]
+        values = [median, p95] if len(limits) == 2 else [p95]
+        exceeded = any(v > lim for v, lim in zip(values, limits))
+        result = "EXCEEDED (reported only)" if exceeded else "within (reported only)"
+    row = {
+        "case": case,
+        "runs": runs,
+        "median": f"{median:.1f} ms",
+        "p95": f"{p95:.1f} ms",
+        "target": target,
+        "result": result + (f"; {note}" if note else ""),
+        "follow_up": follow_up,
+    }
+    _SPD_ROWS.append(row)
+    print(" | ".join(str(v) for k, v in row.items() if k != "follow_up"))
+    return row
+
+
+def _spd_markdown() -> str:
+    bash_version = subprocess.run(
+        [BASH, "--version"], capture_output=True, text=True
+    ).stdout.splitlines()[0]
+    load = " ".join(f"{x:.2f}" for x in os.getloadavg())
+    lines = [
+        "# Task 15: hook speed results",
+        "",
+        "Written by the test module tests/hooks/test_launch_level_guard.py (section",
+        '"Task 15: speed") at the end of the run below; no number is edited by hand.',
+        "",
+        f"- Run: {datetime.now(timezone.utc):%Y-%m-%d %H:%M} UTC, "
+        "`LL_SPEED_RESULTS=<this file> uv run pytest "
+        'tests/hooks/test_launch_level_guard.py -k "SPD or speed"`.',
+        f"- Host: {bash_version}; {os.cpu_count()} CPUs; load average {load} "
+        f"when the file was written; Python {sys.version.split()[0]}.",
+        "- Method: each run is one real subprocess (bash and the hook script), "
+        "timed with time.monotonic() around subprocess.run after one untimed "
+        "warm-up run. p95 is the inclusive 95th percentile. PATH holds only a "
+        "temporary bin directory; HOME is a temporary directory. T-SPD-5 uses "
+        f"{LARGE_RUNS} runs per command instead of 100 (each run takes 0.5 to "
+        f"0.9 s); the envelope stress case uses {ENVELOPE_RUNS} runs, with p95 "
+        "taken from those runs.",
+        "- Asserted (design section 8): T-SPD-3 (guard median at most 1.5 times "
+        "block-bare-python.sh) and T-SPD-5 (every run under 1 s). Every other "
+        "row is reported only.",
+        "",
+        "| Case | Runs | Median | p95 | Target | Result |",
+        "|---|---|---|---|---|---|",
+    ]
+    for row in _SPD_ROWS:
+        cells = [row[k] for k in ("case", "runs", "median", "p95", "target", "result")]
+        lines.append("| " + " | ".join(str(c) for c in cells) + " |")
+    exceeded = [r for r in _SPD_ROWS if r["result"].startswith("EXCEEDED")]
+    failed = [r for r in _SPD_ROWS if r["result"].startswith("FAIL")]
+    lines += ["", "## Reported targets exceeded", ""]
+    lines += [
+        f"- {r['case']} exceeded its reported target ({r['target']}); "
+        f"follow-up: {r['follow_up']}."
+        for r in exceeded
+    ] or ["None."]
+    lines += ["", "## Asserted targets failed", ""]
+    lines += [
+        f"- {r['case']} FAILED its asserted target ({r['target']}): {r['result']}."
+        for r in failed
+    ] or ["None."]
+    return "\n".join(lines) + "\n"
+
+
+def _spd_stale_store(home: Path) -> None:
+    """1,000 session files of other sessions and 50 pending records."""
+    store = _store(home)
+    for name, count, stem in (("sessions", 1000, "other-"), ("pending", 50, "")):
+        part = store / name
+        part.mkdir(parents=True, mode=0o700)
+        for i in range(count):
+            (part / (f"{stem}{i:04d}" if stem else f"{i:032x}")).write_text("full")
+
+
+def _spd_ordinary(tmp_path: Path, stale: bool):
+    home = tmp_path / "home"
+    env = _spd_env(tmp_path, home, ("awk",))
+    if stale:
+        _spd_stale_store(home)
+    return env, json.dumps(_bash(SPD_COMMAND)).encode()
+
+
+ORDINARY_TARGET = "median 20 ms, p95 50 ms"
+
+
+def test_speed_empty_store(tmp_path, speed_report):
+    # T-SPD-1: ordinary session, no store at all (the empty-store fast exit).
+    env, stdin = _spd_ordinary(tmp_path, stale=False)
+    times, codes = _spd_time(HOOK, stdin, env)
+    assert codes == {0}
+    _spd_row(
+        "T-SPD-1 guard, ordinary, empty store",
+        SPD_RUNS,
+        times,
+        ORDINARY_TARGET,
+        "reported",
+        GUARD_FOLLOW_UP,
+    )
+
+
+def test_speed_stale_store(tmp_path, speed_report):
+    # T-SPD-2: ordinary session, store with 1,000 session files and 50 pending.
+    env, stdin = _spd_ordinary(tmp_path, stale=True)
+    times, codes = _spd_time(HOOK, stdin, env)
+    assert codes == {0}
+    _spd_row(
+        "T-SPD-2 guard, ordinary, store of 1,050 files",
+        SPD_RUNS,
+        times,
+        ORDINARY_TARGET,
+        "reported",
+        GUARD_FOLLOW_UP,
+    )
+
+
+@pytest.mark.parametrize("stale", [False, True], ids=["empty-store", "stale-store"])
+def test_speed_ratio_to_block_bare_python(tmp_path, speed_report, stale):
+    # T-SPD-3: the same Bash payload through both hooks, runs interleaved.
+    env, stdin = _spd_ordinary(tmp_path, stale)
+    store = "store of 1,050 files" if stale else "empty store"
+    _spd_once(HOOK, stdin, env)
+    _spd_once(BLOCK_BARE_PYTHON, stdin, env)
+    guard, other = [], []
+    for _ in range(SPD_RUNS):
+        for script, times in ((HOOK, guard), (BLOCK_BARE_PYTHON, other)):
+            seconds, result = _spd_once(script, stdin, env)
+            assert result.returncode == 0, (script.name, result.stderr)
+            times.append(seconds)
+    ratio = statistics.median(guard) / statistics.median(other)
+    verdict = "PASS" if ratio <= 1.5 else "FAIL"
+    _spd_row(
+        f"T-SPD-3 block-bare-python.sh, ordinary, {store} (same run)",
+        SPD_RUNS,
+        other,
+        "baseline for T-SPD-3",
+        "baseline",
+    )
+    _spd_row(
+        f"T-SPD-3 guard, ordinary, {store} (same run)",
+        SPD_RUNS,
+        guard,
+        "median at most 1.5 times block-bare-python.sh (asserted)",
+        f"{verdict}: ratio {ratio:.2f}",
+    )
+    assert ratio <= 1.5, f"T-SPD-3 {store}: guard/block-bare-python ratio {ratio:.2f}"
+
+
+@pytest.mark.parametrize(
+    "command, code",
+    [("git status", 0), ("git commit -m x", 2)],
+    ids=["allow", "block"],
+)
+def test_speed_governed(tmp_path, speed_report, command, code):
+    # T-SPD-4: governed session at level F (full).
+    env = _spd_env(tmp_path, tmp_path / "home")
+    _bind(tmp_path, "full")
+    times, codes = _spd_time(HOOK, json.dumps(_bash(command)).encode(), env)
+    assert codes == {code}
+    _spd_row(
+        f"T-SPD-4 guard, governed F, {'allow' if code == 0 else 'block'} `{command}`",
+        SPD_RUNS,
+        times,
+        "p95 60 ms",
+        "reported",
+        GUARD_FOLLOW_UP,
+    )
+
+
+def _spd_fill(head: str, unit: str, tail: str, size: int = 65_536) -> str:
+    count, rest = divmod(size - len((head + tail).encode()), len(unit.encode()))
+    text = head + " " * rest + unit * count + tail
+    assert len(text.encode()) == size
+    return text
+
+
+LARGE_COMMANDS = {
+    "heredoc-git-words-64KB": _spd_fill(
+        "git commit -m \"$(cat <<'EOF'\nfeat: speed fixture\n\n",
+        "Run git status, then git push origin feature and gh pr create --repo o/r.\n",
+        'EOF\n)"',
+    ),
+    "backslash-lines-64KB": _spd_fill("", "git status --short \\\n", "true"),
+    "git-status-lines-64KB": _spd_fill("", "git status\n", ""),
+    "1MB-big": _spd_fill("", "git status\n", "", 1 << 20),
+}
+
+
+@pytest.mark.parametrize("name", list(LARGE_COMMANDS))
+def test_speed_large_commands(tmp_path, speed_report, name):
+    # T-SPD-5: governed full-submit session, each run under 1 s (asserted).
+    env = _spd_env(tmp_path, tmp_path / "home")
+    _bind(tmp_path, "full-submit")
+    stdin = json.dumps(_bash(LARGE_COMMANDS[name])).encode()
+    times, codes = _spd_time(HOOK, stdin, env, LARGE_RUNS)
+    if name == "1MB-big":
+        assert codes == {2}  # LL-BIG at once
+    worst = max(times)
+    verdict = "PASS" if worst < 1.0 else "FAIL"
+    _spd_row(
+        f"T-SPD-5 guard, governed FS, {name}",
+        LARGE_RUNS,
+        times,
+        "every run under 1 s (asserted)",
+        f"{verdict}: max {worst * 1000:.1f} ms",
+        note=f"exit {sorted(codes)}",
+    )
+    assert worst < 1.0, f"T-SPD-5 {name}: slowest run {worst:.3f} s"
+
+
+def _spd_wait4(script: Path, stdin_path: Path, env: dict, timeout: float):
+    """Seconds, exit code and peak RSS (KiB) of the hook and its children."""
+    started = time.monotonic()
+    with stdin_path.open("rb") as stdin:
+        proc = subprocess.Popen(
+            [BASH, str(script)],
+            stdin=stdin,
+            stdout=subprocess.DEVNULL,
+            stderr=subprocess.DEVNULL,
+            env=env,
+        )
+    while True:
+        pid, status, usage = os.wait4(proc.pid, os.WNOHANG)
+        if pid:
+            proc.returncode = os.waitstatus_to_exitcode(status)
+            return time.monotonic() - started, proc.returncode, usage.ru_maxrss
+        if time.monotonic() - started > timeout:
+            proc.kill()
+            _, status, _ = os.wait4(proc.pid, 0)
+            proc.returncode = os.waitstatus_to_exitcode(status)
+            return None, None, None
+        time.sleep(0.002)
+
+
+@pytest.mark.parametrize("governed", [False, True], ids=["ordinary", "governed"])
+def test_speed_large_envelope(tmp_path, speed_report, governed):
+    # Design section 8: a very large non-command field; time and memory, or a
+    # timeout, are the result. No size limit is implied or asserted.
+    home = tmp_path / "home"
+    env = _spd_env(tmp_path, home)
+    if governed:
+        _bind(tmp_path, "full")
+    else:
+        _spd_stale_store(home)  # a store is present, so the guard parses the input
+    payload = _bash("git status", description="x" * ENVELOPE_BYTES)
+    stdin_path = tmp_path / "envelope.json"
+    stdin_path.write_bytes(json.dumps(payload).encode())
+    size_mib = stdin_path.stat().st_size / (1 << 20)
+    times, codes, peak = [], set(), 0
+    for _ in range(ENVELOPE_RUNS):
+        seconds, code, rss = _spd_wait4(HOOK, stdin_path, env, ENVELOPE_TIMEOUT)
+        if seconds is None:
+            break
+        times.append(seconds)
+        codes.add(code)
+        peak = max(peak, rss)
+    case = (
+        f"Envelope stress, guard, {'governed F' if governed else 'ordinary'}, "
+        f"{size_mib:.0f} MiB description field"
+    )
+    target = "none; report time and memory, or a timeout"
+    if len(times) < ENVELOPE_RUNS:
+        row = {
+            "case": case,
+            "runs": f"{len(times) + 1} (stopped)",
+            "median": "-",
+            "p95": "-",
+            "target": target,
+            "result": f"TIMEOUT after {ENVELOPE_TIMEOUT} s",
+            "follow_up": "",
+        }
+        _SPD_ROWS.append(row)
+        print(row)
+        return
+    _spd_row(
+        case,
+        ENVELOPE_RUNS,
+        times,
+        target,
+        f"completed, exit {sorted(codes)}, peak RSS {peak / 1024:.0f} MiB "
+        "(largest process of the hook tree)",
+    )
+
+
+def test_speed_identity_hook_with_pending_only_store(tmp_path, speed_report):
+    # F2: an ordinary Bash call through launch-job-identity.sh (not modified
+    # here) with a store that holds only pending/, as a claim leaves it, against
+    # the same call with no store. UV environment of test_launch_job_identity.py.
+    none_home, pending_home = tmp_path / "home-none", tmp_path / "home-pending"
+    env_none = _spd_env(tmp_path, none_home, ("awk", "uv"))
+    env_none.update(UV_PYTHON=sys.executable, UV_PYTHON_DOWNLOADS="never")
+    env_pending = {**env_none, "HOME": str(pending_home)}
+    pending_home.mkdir()
+    pending = _store(pending_home) / "pending"
+    pending.mkdir(parents=True, mode=0o700)
+    (pending / NONCE).write_text("full")
+    stdin = json.dumps({**_bash(SPD_COMMAND), "tool_use_id": "toolu_01"}).encode()
+    cases = (("no store", env_none, []), ("store with only pending/", env_pending, []))
+    for _, env, _ in cases:
+        _spd_once(IDENTITY, stdin, env, timeout=30)
+    for _ in range(SPD_RUNS):
+        for _, env, times in cases:
+            seconds, result = _spd_once(IDENTITY, stdin, env, timeout=30)
+            assert (result.returncode, result.stdout) == (0, b""), result.stderr
+            times.append(seconds)
+    for label, _, times in cases:
+        _spd_row(
+            f"F2 launch-job-identity.sh, ordinary Bash, {label}",
+            SPD_RUNS,
+            times,
+            "median 20 ms, p95 50 ms (ordinary budget, reported only)",
+            "reported",
+            IDENTITY_FOLLOW_UP,
+        )
+
+
 def test_huge_fields_are_quick(tmp_path):
     # Line splitting must stay linear: _run's 10 s timeout fails a quadratic split.
     _bind(tmp_path, "worktree")

Delta diff from the previous reviewed tree (empty on the first review): 
Earlier blocking findings of this start (empty on the first review): 
Saved-probe re-check hit locations (may be empty): 

Do not trust the implementer's report.

First mark each earlier blocking finding resolved, open or regressed from the diff. Then, for each AC, mark it met or unmet. Require citations: every AC you mark, met or unmet, carries a `path:line` or `Ti.ACk@path:line` citation, and an unmet mark lists the finding ids behind it. Do not return a verdict; the orchestrator computes it.

For every finding answer four questions, each yes or no:
1. ac-outcome-missing: is output an AC requires absent, or does it contradict the AC text, or does an evidence claim you could not verify have no evidence row?
2. false-claim: is a claim in delivered text or code false against live source, or does a recipe or instruction followed as written not do what the text says?
3. harmful-effect: does code or a recipe this task added or changed write, append, chmod or delete tracked or production data, mutate state outside the task's declared outputs, or expose a secret?
4. quoted-constraint-breach: does the diff violate a quoted plan constraint, out-of-scope, non-goal or non-negotiable item, or an explicit task instruction?

Anchor rule: cite exactly one anchor per yes. ac-outcome-missing: the quoted AC words. false-claim: the live-source path:line holding the contradicting text. harmful-effect: the diff line that is the write. quoted-constraint-breach: the quoted constraint or instruction text. A yes without a valid anchor does not block.

Write one line per finding:
F<k>.<j> ac=<Ti.ACk|scope> at=<path:line> anchor=<quoted text or path:line> chk=<amiss,false,harm,constraint as y/n> family=<id> fix=<text> [covers=<quoted AC clause or constraint>]: <text>
Do not write sev=, trigger=, first= or origin=; the orchestrator adds them. Write one status line per earlier blocking finding: F<m>.<j> resolved|open|regressed.

Inside /sc:implement this protocol's severity model governs this review and takes precedence over the session's output style and the copy of it injected into every subagent; only blocking findings may fail an attempt.

You are not given an adviser answer, brief, evidence file or troubleshoot report. Do not read the retry folders (legacy `.dev/implement/<slug>/retries/`, managed `<pkg>/artifacts/retries/`) or `.dev/troubleshoot/`. A citation into either makes the verdict `cannot-verify`.
The prior-findings slot above carries earlier blocking finding lines that the orchestrator copies byte for byte from `review-*.md` and `repair-*.md`; they reach you as prompt text, not as an evidence file. Do not read those folders to get them, and never cite the slot or the file it came from.

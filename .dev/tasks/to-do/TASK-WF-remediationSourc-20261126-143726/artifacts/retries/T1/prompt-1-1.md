c4f1c8c44f8065f91b16505ab374d3e8ec6ece1d
Review one task for spec compliance.

Task brief: ## Task 1: Add the two regression tests and `import random` to the test module

Edit `tests/unit/test_ccsession_tiers.py` only. Add `import random` to the import block after `import os` (line 13) so the block stays sorted (it currently has no `random` import). `import errno` is added as well, as the first line of the stdlib block (before `import gzip`, line 10 of the unmodified file, so the block stays sorted). Add two tests after `test_free_port_clear_of_fails_loudly_at_the_bound` (it ends at line 1883) and before `test_forced_in_window_shim_port_is_skipped` (line 1886). The tests use only names the module already has (`Path`, `socket`, `pytest`, `models`) plus `random` and `errno`, and neither calls a helper that does not exist yet.

First test, `test_free_port_window_lies_below_the_ephemeral_range`: read `/proc/sys/net/ipv4/ip_local_port_range` itself as an independent oracle, taking the first field as `low` (skip with `pytest.skip` when the file is unreadable, or when `low - 1 - models.SHIM_PORT_STEP * (models.SHIM_PORT_ATTEMPTS - 1)` is below 10000, meaning no room); then over 20 calls assert that `_free_port() + models.SHIM_PORT_STEP * (models.SHIM_PORT_ATTEMPTS - 1) < low`. The test must not re-bind the window ports (another process could take one between the pick and the check and make the test itself flaky).

Second test, `test_free_port_skips_a_window_whose_attempt_port_is_a_client_local_port` (takes `monkeypatch`): obtain `clear_base = _free_port()` and `held_base = _free_port()`, drawing `held_base` again until `abs(held_base - clear_base)` is larger than `models.SHIM_PORT_STEP * models.SHIM_PORT_ATTEMPTS` so the two windows cannot overlap; start a plain local listener (a `socket.socket()` bound to `("127.0.0.1", 0)` and listening); bind a second plain client socket (no `SO_REUSEADDR`) to `("127.0.0.1", held_base + models.SHIM_PORT_STEP)`, connect it to the listener and accept the connection, so that port is now the client's local port; the client bind to `held_base + models.SHIM_PORT_STEP`, the connect and the accept sit inside one guard in which an `OSError` becomes `pytest.skip`, not an error; the premise checks below sit outside that guard, because the `OSError` of the `SO_REUSEADDR` bind is expected there and is compared with `errno.EADDRINUSE`, never skipped; check the premise and call `pytest.skip` if it does not hold: the premise is exact: a fresh `socket.socket()` probe's `connect_ex` to that port must equal `errno.ECONNREFUSED`, and a fresh socket with `SO_REUSEADDR` set must fail its bind of that port with `errno.EADDRINUSE` (111 and 98 on Linux); then patch `random.randrange` with `monkeypatch.setattr(random, "randrange", ...)` so that it returns `held_base` on the first call and `clear_base` on every later call, where the replacement accepts the two arguments `(start, stop)` the new `_free_port()` passes; assert `_free_port() == clear_base`. Close the accepted connection and the listener first and the client socket last, and every other socket opened, including the two probe sockets, in a `finally` block so sockets are never leaked. No sleeps.

Acceptance criteria:
T1.AC1: `import errno` and `import random` each appear once in the import block, in their sorted places, and `uv run ruff check tests/unit/test_ccsession_tiers.py` reports no new finding (no I001 or F401).
T1.AC2: Both new tests exist with exactly these names, in this file, placed after `test_free_port_clear_of_fails_loudly_at_the_bound` and before `test_forced_in_window_shim_port_is_skipped`.
T1.AC3: Run on the unchanged `_free_port` (the old three-line body): `uv run pytest tests/unit/test_ccsession_tiers.py -q -p no:cacheprovider -o addopts= -k "free_port_window or free_port_skips"` shows both tests FAILED by an `AssertionError` on the assertions described above, not by an `ImportError`, `NameError`, `TypeError` or a skip; the command output is saved to `./artifacts/t1-red.log`. If either new test is skipped instead of failing in that red run, repeat the red run once and save both outputs; if it skips again, stop and report the premise failure instead of continuing.
T1.AC4: The rest of the file is unchanged: `git diff --stat -- tests/unit/test_ccsession_tiers.py` shows only added lines (the two imports and the two tests), and the existing tests still pass with the two new tests deselected: `uv run pytest tests/unit/test_ccsession_tiers.py -q -p no:cacheprovider -o addopts= --deselect tests/unit/test_ccsession_tiers.py::test_free_port_window_lies_below_the_ephemeral_range --deselect tests/unit/test_ccsession_tiers.py::test_free_port_skips_a_window_whose_attempt_port_is_a_client_local_port` (record the pass line in `./artifacts/t1-rest.log`).
Global constraints: ## Constraints

- Only `tests/unit/test_ccsession_tiers.py` changes, plus files this plan writes under `./artifacts/`. No production file changes: `src/superclaude/skills/ccsession-tag/ccsession`, `src/superclaude/skills/ccsession-tag/models.py` and `src/superclaude/skills/ccsession-tag/local-gateway-alias-proxy.py` stay as they are.
- No assertion of an existing test is weakened or removed. `_free_port_clear_of` (line 832) and its #443 guard comment (line 833) are untouched. The signature `def _free_port() -> int:` stays, because `_free_port_clear_of`, the `shim` fixture (line 850), the unreachable upstream (line 1213) and the three tests that patch the module attribute `_free_port` (lines 1865, 1879, 1907) rely on it.
- The step and the attempt count are read from `models.SHIM_PORT_STEP` and `models.SHIM_PORT_ATTEMPTS`, never written as 101 and 6.
- Ruff for this repo selects E, F, I, N, W and TID with line length 88 (`pyproject.toml`, `[tool.ruff]`): every added line stays within 88 characters and imports stay sorted. `ruff check` ignores E501, so only `uv run ruff format --check` enforces the 88 columns; run `uv run ruff format` on the file so long names such as the second new test's signature are wrapped.
- Do not use `git stash`. Do not stage or commit anything under `.claude/` or `.dev/issues/`.
- Load-harness output folders go under `.dev/troubleshoot/test-ccsession-shim-tests-in-tests-20261126031906/repro/` (untracked); only small summary files are copied into `./artifacts/`. `./artifacts/` in this plan always means this package's own `artifacts/` directory (the folder next to this plan file), while commands run from the repository root.
- Known limits to keep visible in the final report, not to hide: a below-range port can still be held by a long-lived service, and two concurrent test processes can draw overlapping windows (estimated about 11 in 22,000 per pair, unmeasured), which the pick-time bind check reduces; on a host whose local-port range starts at or below 10506 the new `_free_port()` falls back to the old behaviour; the single `port 36877 is owned by another service` failure had no identified holder and is only probably reduced; the CI runner and the original release-gate host were never observed, so the fixed-tree load runs are the real measurement.
- Out of scope (separate issues, not part of this plan): the launcher keeping the started shim's stderr and noticing an exited shim, and the macOS-only `e.errno == 48` check at `src/superclaude/skills/ccsession-tag/local-gateway-alias-proxy.py:1054`.
- Review record: the two last edits to this plan, the cleanup patterns tied to this checkout's own path and the `mkdir -p` for the log folder of the load runs, were made after the cap of 3 reviews had been reached, with the go of the IronFlow session (which is helping Clay push E2); they were checked by a read-only check of those lines only, not by a fourth full review.
Start sha: c4f1c8c44f8065f91b16505ab374d3e8ec6ece1d
Diff against the start snapshot: $ git diff --stat c4f1c8c44f8065f91b16505ab374d3e8ec6ece1d -- tests/unit/test_ccsession_tiers.py
 tests/unit/test_ccsession_tiers.py | 64 ++++++++++++++++++++++++++++++++++++++
 1 file changed, 64 insertions(+)

$ git diff c4f1c8c44f8065f91b16505ab374d3e8ec6ece1d -- tests/unit/test_ccsession_tiers.py
diff --git a/tests/unit/test_ccsession_tiers.py b/tests/unit/test_ccsession_tiers.py
index 5199238c2..3d267d23b 100644
--- a/tests/unit/test_ccsession_tiers.py
+++ b/tests/unit/test_ccsession_tiers.py
@@ -7,10 +7,12 @@ workspace env file, the network, or the model-data cache.
 
 from __future__ import annotations
 
+import errno
 import gzip
 import http.server
 import json
 import os
+import random
 import re
 import runpy
 import signal
@@ -1883,6 +1885,68 @@ def test_free_port_clear_of_fails_loudly_at_the_bound(monkeypatch) -> None:
     assert len(calls) == _FREE_PORT_CLEAR_OF_TRIES
 
 
+def test_free_port_window_lies_below_the_ephemeral_range() -> None:
+    """#352: the kernel gives outgoing connections the ports above `low`, so a
+    shim window up there collides with other processes' connections."""
+    try:
+        low = int(Path("/proc/sys/net/ipv4/ip_local_port_range").read_text().split()[0])
+    except (OSError, ValueError, IndexError):
+        pytest.skip("the local port range is not readable")
+    reach = models.SHIM_PORT_STEP * (models.SHIM_PORT_ATTEMPTS - 1)
+    if low - 1 - reach < 10000:
+        pytest.skip("no room for a shim window below the local port range")
+    for _ in range(20):
+        assert _free_port() + reach < low
+
+
+def test_free_port_skips_a_window_whose_attempt_port_is_a_client_local_port(
+    monkeypatch,
+) -> None:
+    """#352: a port that is another socket's local port refuses connect probes
+    but fails the shim's SO_REUSEADDR bind, so its window must be skipped."""
+    span = models.SHIM_PORT_STEP * models.SHIM_PORT_ATTEMPTS
+    clear_base = _free_port()
+    for _ in range(50):
+        held_base = _free_port()
+        if abs(held_base - clear_base) > span:
+            break
+    else:
+        pytest.skip("could not draw two windows that do not overlap")
+    held = held_base + models.SHIM_PORT_STEP
+    listener, client = socket.socket(), socket.socket()
+    conn, probes = None, []
+    try:
+        try:
+            listener.bind(("127.0.0.1", 0))
+            listener.listen(1)
+            client.bind(("127.0.0.1", held))
+            client.connect(listener.getsockname())
+            conn, _ = listener.accept()
+        except OSError as exc:
+            pytest.skip(f"cannot make port {held} a client's local port: {exc}")
+        probes.append(socket.socket())
+        if probes[-1].connect_ex(("127.0.0.1", held)) != errno.ECONNREFUSED:
+            pytest.skip(f"a connect probe to port {held} was not refused")
+        probes.append(socket.socket())
+        probes[-1].setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
+        try:
+            probes[-1].bind(("127.0.0.1", held))
+        except OSError as exc:
+            if exc.errno != errno.EADDRINUSE:
+                pytest.skip(f"the SO_REUSEADDR bind of port {held} failed: {exc}")
+        else:
+            pytest.skip(f"a SO_REUSEADDR bind of the client's port {held} worked")
+        draws = iter([held_base])
+        monkeypatch.setattr(
+            random, "randrange", lambda start, stop: next(draws, clear_base)
+        )
+        assert _free_port() == clear_base
+    finally:
+        for sock in (conn, listener, *probes, client):
+            if sock is not None:
+                sock.close()
+
+
 def test_forced_in_window_shim_port_is_skipped(tmp_path: Path, monkeypatch) -> None:
     """#443: a first shim port inside the gateway's shim window is skipped, not launched."""
     module = sys.modules[__name__]

--- untracked evidence file .dev/tasks/to-do/TASK-WF-remediationSourc-20261126-143726/artifacts/t1-red.log (full contents, line numbers added) ---
1: FF                                                                       [100%]
2: =================================== FAILURES ===================================
3: _____________ test_free_port_window_lies_below_the_ephemeral_range _____________
4: 
5:     def test_free_port_window_lies_below_the_ephemeral_range() -> None:
6:         """#352: the kernel gives outgoing connections the ports above `low`, so a
7:         shim window up there collides with other processes' connections."""
8:         try:
9:             low = int(Path("/proc/sys/net/ipv4/ip_local_port_range").read_text().split()[0])
10:         except (OSError, ValueError, IndexError):
11:             pytest.skip("the local port range is not readable")
12:         reach = models.SHIM_PORT_STEP * (models.SHIM_PORT_ATTEMPTS - 1)
13:         if low - 1 - reach < 10000:
14:             pytest.skip("no room for a shim window below the local port range")
15:         for _ in range(20):
16: >           assert _free_port() + reach < low
17: E           assert (48281 + 505) < 32768
18: E            +  where 48281 = _free_port()
19: 
20: tests/unit/test_ccsession_tiers.py:1899: AssertionError
21: ___ test_free_port_skips_a_window_whose_attempt_port_is_a_client_local_port ____
22: 
23: monkeypatch = <_pytest.monkeypatch.MonkeyPatch object at 0x75f4454be4a0>
24: 
25:     def test_free_port_skips_a_window_whose_attempt_port_is_a_client_local_port(
26:         monkeypatch,
27:     ) -> None:
28:         """#352: a port that is another socket's local port refuses connect probes
29:         but fails the shim's SO_REUSEADDR bind, so its window must be skipped."""
30:         span = models.SHIM_PORT_STEP * models.SHIM_PORT_ATTEMPTS
31:         clear_base = _free_port()
32:         for _ in range(50):
33:             held_base = _free_port()
34:             if abs(held_base - clear_base) > span:
35:                 break
36:         else:
37:             pytest.skip("could not draw two windows that do not overlap")
38:         held = held_base + models.SHIM_PORT_STEP
39:         listener, client = socket.socket(), socket.socket()
40:         conn, probes = None, []
41:         try:
42:             try:
43:                 listener.bind(("127.0.0.1", 0))
44:                 listener.listen(1)
45:                 client.bind(("127.0.0.1", held))
46:                 client.connect(listener.getsockname())
47:                 conn, _ = listener.accept()
48:             except OSError as exc:
49:                 pytest.skip(f"cannot make port {held} a client's local port: {exc}")
50:             probes.append(socket.socket())
51:             if probes[-1].connect_ex(("127.0.0.1", held)) != errno.ECONNREFUSED:
52:                 pytest.skip(f"a connect probe to port {held} was not refused")
53:             probes.append(socket.socket())
54:             probes[-1].setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
55:             try:
56:                 probes[-1].bind(("127.0.0.1", held))
57:             except OSError as exc:
58:                 if exc.errno != errno.EADDRINUSE:
59:                     pytest.skip(f"the SO_REUSEADDR bind of port {held} failed: {exc}")
60:             else:
61:                 pytest.skip(f"a SO_REUSEADDR bind of the client's port {held} worked")
62:             draws = iter([held_base])
63:             monkeypatch.setattr(
64:                 random, "randrange", lambda start, stop: next(draws, clear_base)
65:             )
66: >           assert _free_port() == clear_base
67: E           assert 46407 == 37955
68: E            +  where 46407 = _free_port()
69: 
70: tests/unit/test_ccsession_tiers.py:1943: AssertionError
71: =========================== short test summary info ============================
72: FAILED tests/unit/test_ccsession_tiers.py::test_free_port_window_lies_below_the_ephemeral_range
73: FAILED tests/unit/test_ccsession_tiers.py::test_free_port_skips_a_window_whose_attempt_port_is_a_client_local_port
74: 2 failed, 217 deselected in 16.66s
75: rc=1
76: 

--- untracked evidence file .dev/tasks/to-do/TASK-WF-remediationSourc-20261126-143726/artifacts/t1-rest.log (full contents, line numbers added) ---
1: ........................................................................ [ 33%]
2: ........................................................................ [ 66%]
3: ........................................................................ [ 99%]
4: .                                                                        [100%]
5: 217 passed, 2 deselected in 189.44s (0:03:09)
6: rc=0
7: 

--- untracked evidence file .dev/tasks/to-do/TASK-WF-remediationSourc-20261126-143726/artifacts/t1-ruff.log (full contents, line numbers added) ---
1: $ uv run ruff check tests/unit/test_ccsession_tiers.py
2: All checks passed!
3: $ uv run ruff format --check tests/unit/test_ccsession_tiers.py
4: 1 file already formatted
5: 

Codegraph context
index_state=absent checked_at=see run state worktree_root=/home/coder/workspaces/worktrees/IronClaude/issue-352 projectPath=/home/coder/workspaces/worktrees/IronClaude/issue-352
call codegraph only when index_state: fresh, never to widen scope
Q2b ran on the Grep/Read floor: no dependents outside the diff are named by this task's changes; see diff.

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

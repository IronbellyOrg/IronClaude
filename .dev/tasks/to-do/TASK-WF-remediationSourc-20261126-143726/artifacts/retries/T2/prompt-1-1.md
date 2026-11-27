81c7d805384c2cdfe972416eed7a5a584036bc95
Review one task for spec compliance.

Task brief: ## Task 2: Add the constants and the two helpers above `_free_port()`

Depends on: Task 1

Edit `tests/unit/test_ccsession_tiers.py` only. Insert, directly above `def _free_port() -> int:` (line 823 of the unmodified file; it moves down after Task 1), these module-level names, with one-line comments in the style of the file:
- `_FREE_PORT_FLOOR = 10000` and `_FREE_PORT_TRIES = 50`.
- `_ephemeral_low() -> int`: returns the first whitespace-separated field of `/proc/sys/net/ipv4/ip_local_port_range` as an int; returns `32768` on `OSError`, `ValueError` or `IndexError` (32768 is also below the macOS range).
- `_window_binds(base: int) -> bool`: for each `port = base + models.SHIM_PORT_STEP * k` with `k in range(models.SHIM_PORT_ATTEMPTS)`, create a `socket.socket()`, set `SO_REUSEADDR`, bind `("127.0.0.1", port)` and close it (use `with`); return `False` on the first `OSError`, else `True`. This is the same bind the shim makes (`allow_reuse_address = True` at `src/superclaude/skills/ccsession-tag/local-gateway-alias-proxy.py:1030`, bind at line 1052).

Do not change `_free_port()` in this task: the helpers stay unused until Task 3.

Acceptance criteria:
T2.AC1: The two helpers and the two constants exist with exactly these names and signatures, directly above `_free_port`, and `_free_port()` is byte-for-byte unchanged.
T2.AC2: The helpers work on a window that is known to be free (output in `./artifacts/t2-helpers.log`): an ad-hoc run prints `t._ephemeral_low()` (`32768` on this host); then steps through bases from 10000 upward until it can bind all six window ports `base + models.SHIM_PORT_STEP * k` (k from 0 to `models.SHIM_PORT_ATTEMPTS` minus 1) with `SO_REUSEADDR` set, not listening, and keeps those six sockets open; while they are held, `t._window_binds(base)` returns `True`, and a plain socket without `SO_REUSEADDR` fails to bind `base` (so a helper that left `SO_REUSEADDR` out would print `False`); the six sockets are then closed. This check does not use the old `_free_port()` and does not print `_window_binds(0)`.
T2.AC3: A held window port is detected: in an ad-hoc run (output in `./artifacts/t2-helpers.log`), bind a plain socket to `base + models.SHIM_PORT_STEP` for a free `base`, call `_window_binds(base)` while it is held without `SO_REUSEADDR` and listening, and record `False`.
T2.AC4: `uv run ruff check tests/unit/test_ccsession_tiers.py` and `uv run ruff format --check tests/unit/test_ccsession_tiers.py` report nothing new for the added hunk, and the two new tests from Task 1 still fail on their assertions.
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
Start sha: 81c7d805384c2cdfe972416eed7a5a584036bc95
Diff against the start snapshot: $ git diff --stat 81c7d805384c2cdfe972416eed7a5a584036bc95 -- tests/unit/test_ccsession_tiers.py
 tests/unit/test_ccsession_tiers.py | 25 +++++++++++++++++++++++++
 1 file changed, 25 insertions(+)

$ git diff 81c7d805384c2cdfe972416eed7a5a584036bc95 -- tests/unit/test_ccsession_tiers.py
diff --git a/tests/unit/test_ccsession_tiers.py b/tests/unit/test_ccsession_tiers.py
index 3d267d23b..76ce9df1b 100644
--- a/tests/unit/test_ccsession_tiers.py
+++ b/tests/unit/test_ccsession_tiers.py
@@ -822,6 +822,31 @@ class StandInGateway:
         self.server.server_close()
 
 
+_FREE_PORT_FLOOR = 10000  # lowest base port the shim window search draws
+_FREE_PORT_TRIES = 50  # draws before the search gives up and falls back to bind(0)
+
+
+def _ephemeral_low() -> int:
+    """First port the kernel hands to outgoing connections (32768 if unreadable)."""
+    try:
+        text = Path("/proc/sys/net/ipv4/ip_local_port_range").read_text()
+        return int(text.split()[0])
+    except (OSError, ValueError, IndexError):
+        return 32768  # below the macOS range too
+
+
+def _window_binds(base: int) -> bool:
+    """Whether every port of the shim window that starts at base can be bound."""
+    for k in range(models.SHIM_PORT_ATTEMPTS):
+        with socket.socket() as s:
+            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # as the shim does
+            try:
+                s.bind(("127.0.0.1", base + models.SHIM_PORT_STEP * k))
+            except OSError:
+                return False
+    return True
+
+
 def _free_port() -> int:
     with socket.socket() as s:
         s.bind(("127.0.0.1", 0))

--- untracked evidence file .dev/tasks/to-do/TASK-WF-remediationSourc-20261126-143726/artifacts/t2-helpers.log (full contents, line numbers added) ---
1: _ephemeral_low() = 32768
2: clear window: base 10000 ports [10000, 10101, 10202, 10303, 10404, 10505]
3: _window_binds(base) while the six SO_REUSEADDR sockets are held: True
4: plain bind of base without SO_REUSEADDR fails, errno 98 (a helper without SO_REUSEADDR would print False)
5: _window_binds(base) while a plain listening socket holds base + STEP: False
6: _window_binds(base) after it is closed: True
7: rc=0
8: 

--- untracked evidence file .dev/tasks/to-do/TASK-WF-remediationSourc-20261126-143726/artifacts/t2-ruff.log (full contents, line numbers added) ---
1: $ uv run ruff check tests/unit/test_ccsession_tiers.py
2: All checks passed!
3: $ uv run ruff format --check tests/unit/test_ccsession_tiers.py
4: 1 file already formatted
5: 

--- untracked evidence file .dev/tasks/to-do/TASK-WF-remediationSourc-20261126-143726/artifacts/t2-red.log (full contents, line numbers added) ---
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
17: E           assert (41111 + 505) < 32768
18: E            +  where 41111 = _free_port()
19: 
20: tests/unit/test_ccsession_tiers.py:1924: AssertionError
21: ___ test_free_port_skips_a_window_whose_attempt_port_is_a_client_local_port ____
22: 
23: monkeypatch = <_pytest.monkeypatch.MonkeyPatch object at 0x7359d9166410>
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
67: E           assert 48691 == 55687
68: E            +  where 48691 = _free_port()
69: 
70: tests/unit/test_ccsession_tiers.py:1968: AssertionError
71: =========================== short test summary info ============================
72: FAILED tests/unit/test_ccsession_tiers.py::test_free_port_window_lies_below_the_ephemeral_range
73: FAILED tests/unit/test_ccsession_tiers.py::test_free_port_skips_a_window_whose_attempt_port_is_a_client_local_port
74: 2 failed, 217 deselected in 0.62s
75: rc=1
76: 

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

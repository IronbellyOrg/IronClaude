f83b818edc70b036a32d2f432680dcaccf63afff
Review one task for spec compliance.

Task brief: ## Task 2: Add `_free_port_clear_of(gateway_url)` and its unit tests

Depends on: Task 1

Add `_free_port_clear_of(gateway_url: str) -> int` directly after `_free_port` (tests/unit/test_ccsession_tiers.py:757-760). It calls the module-level `_free_port()` (looked up at call time, so a test can monkeypatch it) up to a fixed bound held in a module constant (50 tries), returns the first port for which `models.shim_upstream_problem(gateway_url, port) == ""`, and otherwise fails loudly with `pytest.fail` naming the gateway URL, the bound and the rejected ports. A one-line comment says why it exists (#443: the gateway and shim ports come from separate random binds). `models` is already imported at :33.

Add two tests next to the helper's other users (after `_real_launch`):
- rejected then accepted: monkeypatch `_free_port` to return first a port inside window k=0 of a fixed gateway URL (gateway port minus 5), then an accepted port; assert the helper returns the second value, called `_free_port` exactly twice, and that `models.shim_upstream_problem` is non-empty for the first value.
- loud-failure bound: monkeypatch `_free_port` to always return an in-window port; assert the helper raises pytest's fail exception, the message names the gateway URL, and `_free_port` was called exactly the bound number of times.

Acceptance criteria:
- `_free_port_clear_of` exists in tests/unit/test_ccsession_tiers.py, uses `models.shim_upstream_problem`, and contains no window arithmetic of its own.
- Both new tests pass: `uv run pytest tests/unit/test_ccsession_tiers.py -q -p no:cacheprovider -k free_port_clear_of`; output saved to ./artifacts/t2-pytest.log.
Global constraints: ## Constraints

- Change only tests/unit/test_ccsession_tiers.py. Do not change src/superclaude/skills/ccsession-tag/models.py or src/superclaude/skills/ccsession-tag/ccsession: the refusal is the documented launcher contract (REPORT.md, Documentation Context).
- Leave the `shim` fixture pairing at tests/unit/test_ccsession_tiers.py:766-767, the line at :1075 and the gateway at :2098 unchanged (source.md).
- The forbidden windows are defined by `models.shim_upstream_problem(url, base)` (models.py:822-844): a gateway port 0..97 above `base + 101*k`, k in 0..5. Use that function; do not re-implement the window arithmetic in the test.
- Out of scope, record only: the `_real_launch` environment leak (test:1680 copies os.environ, :1689 removes only CC_SHIM_PORT), ccsession:985 treating every rc==1 as a refusal, the remaining #352 port races, and the 30 CI runs.
- pytest-xdist is not installed locally; CI installs it with `uv pip install "pytest-xdist>=3.5,<4"` (.github/workflows/test.yml:29). Install it the same way for the parallel runs; do not add it to pyproject.toml or uv.lock.
- UV only (`uv run ...`). Evidence goes under ./artifacts/ in this package.
Start sha: f83b818edc70b036a32d2f432680dcaccf63afff
Diff against the start snapshot: 
diff --git a/tests/unit/test_ccsession_tiers.py b/tests/unit/test_ccsession_tiers.py
index 00c1399c..cfef4507 100644
--- a/tests/unit/test_ccsession_tiers.py
+++ b/tests/unit/test_ccsession_tiers.py
@@ -761,6 +761,23 @@ def _free_port() -> int:
         return s.getsockname()[1]
 
 
+_FREE_PORT_CLEAR_OF_TRIES = 50
+
+
+def _free_port_clear_of(gateway_url: str) -> int:
+    # #443: the gateway and shim ports come from separate random binds, so they can collide.
+    rejected = []
+    for _ in range(_FREE_PORT_CLEAR_OF_TRIES):
+        port = _free_port()
+        if models.shim_upstream_problem(gateway_url, port) == "":
+            return port
+        rejected.append(port)
+    pytest.fail(
+        f"no shim base port clear of {gateway_url} after "
+        f"{_FREE_PORT_CLEAR_OF_TRIES} tries; rejected {rejected}"
+    )
+
+
 @pytest.fixture
 def shim(tmp_path: Path):
     """Start the real shim against a stand-in gateway in tier mode."""
@@ -1714,6 +1731,36 @@ def _real_launch(tmp_path: Path, port: int | None, *args: str, **extra: str):
     return proc.stderr, (tmp_path / "seen").read_text().strip()
 
 
+def test_free_port_clear_of_skips_a_port_in_the_shim_window(monkeypatch) -> None:
+    url = "http://127.0.0.1:33361"
+    ports = iter([33356, 45000])
+    calls = []
+
+    def fake_free_port() -> int:
+        calls.append(1)
+        return next(ports)
+
+    monkeypatch.setattr(sys.modules[__name__], "_free_port", fake_free_port)
+    assert _free_port_clear_of(url) == 45000
+    assert len(calls) == 2
+    assert models.shim_upstream_problem(url, 33356) != ""
+
+
+def test_free_port_clear_of_fails_loudly_at_the_bound(monkeypatch) -> None:
+    url = "http://127.0.0.1:33361"
+    calls = []
+
+    def fake_free_port() -> int:
+        calls.append(1)
+        return 33356
+
+    monkeypatch.setattr(sys.modules[__name__], "_free_port", fake_free_port)
+    with pytest.raises(pytest.fail.Exception) as excinfo:
+        _free_port_clear_of(url)
+    assert url in str(excinfo.value)
+    assert len(calls) == _FREE_PORT_CLEAR_OF_TRIES
+
+
 def test_a_busy_shim_is_never_stopped_by_a_new_launch(tmp_path: Path) -> None:
     """Round 2 C1: a launch with other settings must not cut other sessions' replies."""
     (tmp_path / "shim-under-test.py").write_text(
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

fe9cd8a481c6c7543b8bba4d8b7e5784c0aa65a6
Review one task for spec compliance.

Task brief: ## Task 5: Add the forced-collision regression test and record the run evidence

Depends on: Task 3, Task 4

Add `test_forced_in_window_shim_port_is_skipped` to tests/unit/test_ccsession_tiers.py, modelled on the scratch reproduction /tmp/issue443-repro/test_forced_collision.py (recorded in .dev/issues/443/handoff-repro.md). With monkeypatch it wraps `StandInGateway` to record the gateway port and makes the first `_free_port()` call return the gateway port minus 5 (inside window k=0); later calls use the real `_free_port`. It asserts `models.shim_upstream_problem(gateway_url, forced_port)` is non-empty (the old pairing would be refused, as ccsession:986 did in handoff-repro.md) and then runs `test_a_busy_shim_is_never_stopped_by_a_new_launch(tmp_path)`, which must pass because the helper skips the forced port.

Before evidence: copy the reproduction command and output from .dev/issues/443/handoff-repro.md into ./artifacts/t5-before.md (gateway_port=33361, forced_base=33356, the "is a ccsession shim address" refusal). After evidence: run the new test.

Acceptance criteria:
- The new test passes: `uv run pytest tests/unit/test_ccsession_tiers.py -q -p no:cacheprovider -k forced_in_window`; output saved to ./artifacts/t5-after.log. ./artifacts/t5-before.md holds the old-pairing refusal.
- Parallel runs: after `uv pip install "pytest-xdist>=3.5,<4"`, five runs of `uv run pytest tests/unit/test_ccsession_tiers.py -q -p no:cacheprovider -n auto` and one serial run of `uv run pytest tests/unit/test_ccsession_tiers.py -q -p no:cacheprovider` all pass; ./artifacts/t5-runs.md lists each run's passed/failed/skipped counts and duration.
- `make lint` (or `uv run ruff check tests/unit/test_ccsession_tiers.py` and `uv run ruff format --check tests/unit/test_ccsession_tiers.py`) and `make verify-sync` pass; output saved to ./artifacts/t5-lint.log.
- `git diff --name-only` lists only tests/unit/test_ccsession_tiers.py outside .dev/.
Global constraints: ## Constraints

- Change only tests/unit/test_ccsession_tiers.py. Do not change src/superclaude/skills/ccsession-tag/models.py or src/superclaude/skills/ccsession-tag/ccsession: the refusal is the documented launcher contract (REPORT.md, Documentation Context).
- Leave the `shim` fixture pairing at tests/unit/test_ccsession_tiers.py:766-767, the line at :1075 and the gateway at :2098 unchanged (source.md).
- The forbidden windows are defined by `models.shim_upstream_problem(url, base)` (models.py:822-844): a gateway port 0..97 above `base + 101*k`, k in 0..5. Use that function; do not re-implement the window arithmetic in the test.
- Out of scope, record only: the `_real_launch` environment leak (test:1680 copies os.environ, :1689 removes only CC_SHIM_PORT), ccsession:985 treating every rc==1 as a refusal, the remaining #352 port races, and the 30 CI runs.
- pytest-xdist is not installed locally; CI installs it with `uv pip install "pytest-xdist>=3.5,<4"` (.github/workflows/test.yml:29). Install it the same way for the parallel runs; do not add it to pyproject.toml or uv.lock.
- UV only (`uv run ...`). Evidence goes under ./artifacts/ in this package.
Start sha: fe9cd8a481c6c7543b8bba4d8b7e5784c0aa65a6
Diff against the start snapshot: 
diff --git a/tests/unit/test_ccsession_tiers.py b/tests/unit/test_ccsession_tiers.py
index 32e5544e..6c35a4b3 100644
--- a/tests/unit/test_ccsession_tiers.py
+++ b/tests/unit/test_ccsession_tiers.py
@@ -1761,6 +1761,33 @@ def test_free_port_clear_of_fails_loudly_at_the_bound(monkeypatch) -> None:
     assert len(calls) == _FREE_PORT_CLEAR_OF_TRIES
 
 
+def test_forced_in_window_shim_port_is_skipped(tmp_path: Path, monkeypatch) -> None:
+    """#443: a first shim port inside the gateway's shim window is skipped, not launched."""
+    module = sys.modules[__name__]
+    real_free_port = _free_port
+    seen = {}
+    calls = []
+
+    class RecordingGateway(StandInGateway):
+        def __init__(self, *args, **kwargs):
+            super().__init__(*args, **kwargs)
+            seen["gateway_port"] = self.server.server_port
+            seen["url"] = self.url
+
+    def forced_free_port() -> int:
+        calls.append(1)
+        if len(calls) == 1 and "gateway_port" in seen:
+            seen["forced"] = seen["gateway_port"] - 5  # inside window k=0
+            return seen["forced"]
+        return real_free_port()
+
+    monkeypatch.setattr(module, "StandInGateway", RecordingGateway)
+    monkeypatch.setattr(module, "_free_port", forced_free_port)
+    test_a_busy_shim_is_never_stopped_by_a_new_launch(tmp_path)
+    assert "forced" in seen
+    assert models.shim_upstream_problem(seen["url"], seen["forced"]) != ""
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

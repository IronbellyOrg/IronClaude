2daa5d7ffd166689087c8f7c287cf3477cebfa09
Review one task for spec compliance.

Task brief: ## Task 3: Replace `_free_port()` at the four `_real_launch` pairing sites

Depends on: Task 2

In tests/unit/test_ccsession_tiers.py, at each site below the `StandInGateway()` is already created before the port, so replace `port = _free_port()` with `port = _free_port_clear_of(gateway.url)`:
- :1714 in `test_a_busy_shim_is_never_stopped_by_a_new_launch` (gateway at :1712)
- :2076 in `test_tiers_off_launch_never_takes_over_a_tier_shim` (gateway at :2075)
- :2119 in `test_upgraded_code_starts_a_new_shim_and_keeps_the_old` (gateway at :2118)
- :2146 in `test_relative_defaults_path_keeps_each_directory_on_its_own_shim` (gateway at :2145)

Acceptance criteria:
- None of these four tests calls `_free_port()` directly for its shim base port; each uses `_free_port_clear_of(gateway.url)`.
- The fixture at :766-767, the line at :1075 and the gateway at :2098 are unchanged (`git diff` shows no hunk there).
- `uv run pytest tests/unit/test_ccsession_tiers.py -q -p no:cacheprovider -k "busy_shim or tiers_off_launch or upgraded_code or relative_defaults"` passes; output saved to ./artifacts/t3-pytest.log.
Global constraints: ## Constraints

- Change only tests/unit/test_ccsession_tiers.py. Do not change src/superclaude/skills/ccsession-tag/models.py or src/superclaude/skills/ccsession-tag/ccsession: the refusal is the documented launcher contract (REPORT.md, Documentation Context).
- Leave the `shim` fixture pairing at tests/unit/test_ccsession_tiers.py:766-767, the line at :1075 and the gateway at :2098 unchanged (source.md).
- The forbidden windows are defined by `models.shim_upstream_problem(url, base)` (models.py:822-844): a gateway port 0..97 above `base + 101*k`, k in 0..5. Use that function; do not re-implement the window arithmetic in the test.
- Out of scope, record only: the `_real_launch` environment leak (test:1680 copies os.environ, :1689 removes only CC_SHIM_PORT), ccsession:985 treating every rc==1 as a refusal, the remaining #352 port races, and the 30 CI runs.
- pytest-xdist is not installed locally; CI installs it with `uv pip install "pytest-xdist>=3.5,<4"` (.github/workflows/test.yml:29). Install it the same way for the parallel runs; do not add it to pyproject.toml or uv.lock.
- UV only (`uv run ...`). Evidence goes under ./artifacts/ in this package.
Start sha: 2daa5d7ffd166689087c8f7c287cf3477cebfa09
Diff against the start snapshot: 
diff --git a/tests/unit/test_ccsession_tiers.py b/tests/unit/test_ccsession_tiers.py
index cfef4507..dddae1da 100644
--- a/tests/unit/test_ccsession_tiers.py
+++ b/tests/unit/test_ccsession_tiers.py
@@ -1768,7 +1768,7 @@ def test_a_busy_shim_is_never_stopped_by_a_new_launch(tmp_path: Path) -> None:
     )
     gateway = StandInGateway()
     gateway.script["muse-spark-1.3"] = [("pause-stream", 6)]
-    port = _free_port()
+    port = _free_port_clear_of(gateway.url)
     try:
         out, url = _real_launch(tmp_path, port, upstream=gateway.url)
         assert url == f"http://127.0.0.1:{port}"
@@ -2130,7 +2130,7 @@ def test_tiers_off_launch_never_takes_over_a_tier_shim(tmp_path: Path) -> None:
     """Round 3 R3-2: tier sessions keep their shim when a tiers-off session starts."""
     _shim_copy(tmp_path)
     gateway = StandInGateway()
-    port = _free_port()
+    port = _free_port_clear_of(gateway.url)
     try:
         _, url = _real_launch(tmp_path, port, upstream=gateway.url)
         assert url == f"http://127.0.0.1:{port}"
@@ -2173,7 +2173,7 @@ def test_upgraded_code_starts_a_new_shim_and_keeps_the_old(tmp_path: Path) -> No
     """Round 3 R3-3: new code is never served by an old shim, and the old one stays."""
     copy = _shim_copy(tmp_path)
     gateway = StandInGateway()
-    port = _free_port()
+    port = _free_port_clear_of(gateway.url)
     try:
         _, url = _real_launch(tmp_path, port, upstream=gateway.url)
         assert url == f"http://127.0.0.1:{port}"
@@ -2200,7 +2200,7 @@ def test_relative_defaults_path_keeps_each_directory_on_its_own_shim(
     """A relative AIDEV_AI_DEFAULTS_PATH means the file in the launch directory."""
     _shim_copy(tmp_path)
     gateway = StandInGateway()
-    port = _free_port()
+    port = _free_port_clear_of(gateway.url)
     runs = {}
     try:
         for name, first in (("a", "muse-spark-1.3"), ("b", "grok-4.7")):
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

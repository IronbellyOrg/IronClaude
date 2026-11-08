54531825ad2e2eff9733a42561bbaa8c3b4eefe0
Review one task for spec compliance.

Task brief: ## Task 4: Cover the two hand-built launch sites

Depends on: Task 2

These two tests set CC_SHIM_PORT and ANTHROPIC_BASE_URL themselves instead of calling `_real_launch` (REPORT.md, Proposed Fix note), so a collision there does not reach the :1702 message.
- `test_shim_outlives_the_terminal_that_started_it` (:1779): the port is taken at :1796 before the gateway is created at :1806. Move `gateway = StandInGateway()` above the port line and replace `port = _free_port()` with `port = _free_port_clear_of(gateway.url)`; keep `env["ANTHROPIC_BASE_URL"] = gateway.url` and the existing try/finally that stops the gateway, so the gateway is still stopped on every path (if the move puts gateway creation outside the try, make sure no statement between creation and the try can raise without stopping it).
- `test_launch_never_attaches_to_a_shim_that_won_the_port_race` (:2270): the gateway is at :2281; replace `port = _free_port()` at :2282 with `port = _free_port_clear_of(gateway.url)`.

Acceptance criteria:
- Both tests take their shim base port from `_free_port_clear_of(gateway.url)` with the gateway created first.
- The gateway in `test_shim_outlives_the_terminal_that_started_it` is still stopped in a finally block.
- `uv run pytest tests/unit/test_ccsession_tiers.py -q -p no:cacheprovider -k "outlives_the_terminal or won_the_port_race"` passes; output saved to ./artifacts/t4-pytest.log.
Global constraints: ## Constraints

- Change only tests/unit/test_ccsession_tiers.py. Do not change src/superclaude/skills/ccsession-tag/models.py or src/superclaude/skills/ccsession-tag/ccsession: the refusal is the documented launcher contract (REPORT.md, Documentation Context).
- Leave the `shim` fixture pairing at tests/unit/test_ccsession_tiers.py:766-767, the line at :1075 and the gateway at :2098 unchanged (source.md).
- The forbidden windows are defined by `models.shim_upstream_problem(url, base)` (models.py:822-844): a gateway port 0..97 above `base + 101*k`, k in 0..5. Use that function; do not re-implement the window arithmetic in the test.
- Out of scope, record only: the `_real_launch` environment leak (test:1680 copies os.environ, :1689 removes only CC_SHIM_PORT), ccsession:985 treating every rc==1 as a refusal, the remaining #352 port races, and the 30 CI runs.
- pytest-xdist is not installed locally; CI installs it with `uv pip install "pytest-xdist>=3.5,<4"` (.github/workflows/test.yml:29). Install it the same way for the parallel runs; do not add it to pyproject.toml or uv.lock.
- UV only (`uv run ...`). Evidence goes under ./artifacts/ in this package.
Start sha: 54531825ad2e2eff9733a42561bbaa8c3b4eefe0
Diff against the start snapshot: 
diff --git a/tests/unit/test_ccsession_tiers.py b/tests/unit/test_ccsession_tiers.py
index dddae1da..32e5544e 100644
--- a/tests/unit/test_ccsession_tiers.py
+++ b/tests/unit/test_ccsession_tiers.py
@@ -1850,21 +1850,21 @@ def test_shim_outlives_the_terminal_that_started_it(tmp_path: Path) -> None:
     fake.chmod(0o755)
     (tmp_path / "home").mkdir()
     seen = tmp_path / "seen"
-    port = _free_port()
-    env = os.environ.copy()
-    env.update(
-        HOME=str(tmp_path / "home"),
-        CLAUDE_BIN=str(fake),
-        CC_SHIM_SCRIPT=str(shim_copy),
-        CC_SHIM_PORT=str(port),
-        SEEN_FILE=str(seen),
-        AIDEV_AI_DEFAULTS_PATH=str(_defaults(tmp_path)),
-    )
-    gateway = StandInGateway()
-    env["ANTHROPIC_BASE_URL"] = gateway.url
     shim_pid = None
     terminal = None
+    gateway = StandInGateway()
     try:
+        port = _free_port_clear_of(gateway.url)
+        env = os.environ.copy()
+        env.update(
+            HOME=str(tmp_path / "home"),
+            CLAUDE_BIN=str(fake),
+            CC_SHIM_SCRIPT=str(shim_copy),
+            CC_SHIM_PORT=str(port),
+            SEEN_FILE=str(seen),
+            AIDEV_AI_DEFAULTS_PATH=str(_defaults(tmp_path)),
+        )
+        env["ANTHROPIC_BASE_URL"] = gateway.url
         # The terminal: its own session, like a shell in a new pty.
         with open(tmp_path / "terminal.log", "w") as log:
             terminal = subprocess.Popen(
@@ -2336,7 +2336,7 @@ def test_launch_never_attaches_to_a_shim_that_won_the_port_race(
     )
     winner.chmod(0o755)
     gateway = StandInGateway()
-    port = _free_port()
+    port = _free_port_clear_of(gateway.url)
     fake = tmp_path / "bin" / "claude"
     fake.parent.mkdir(exist_ok=True)
     fake.write_text('#!/bin/sh\necho "$ANTHROPIC_BASE_URL" > "$SEEN_FILE"\n')
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

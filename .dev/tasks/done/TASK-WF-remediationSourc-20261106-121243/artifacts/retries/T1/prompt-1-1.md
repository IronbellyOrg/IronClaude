9785004334e809f35036c1b3e4b6a9a5eef3fb8a
Review one task for spec compliance.

Task brief: ## Task 1: Recognize tier aliases and enforce their windows
Inputs: ./source.md Acceptance tier windows/access and source models.py model_window/model-resolve/tier_access, plus existing tests/unit/test_ccsession_tiers.py fixtures. Change models.py shared resolution to recognize bare/suffixed claude-gw-tier names before individual-slot fallback, return the actual tier window and normalize repository-controlled named-tier launches to the existing gateway context-capable spelling. Apply existing owner access rather than bypassing or duplicating it. Add the smallest parameterized matching tests in test_ccsession_tiers.py. Outputs: changed resolver and tests; evidence ./artifacts/t1-tests.log.

Acceptance criteria:
- All configured tiers, explicitly tier0,tier1a,tier1b,tier2, resolve bare/suffixed identities to their own T<N>_WINDOW; fixture850000/850000/850000/500000 remains unequal. No universal850k constant or change to individual-slot fallback.
- Named tier launch selects a context-capable tier spelling when necessary, same routing tier; nonexistent and limited-owner forbidden tiers still reject. Both bare and suffixed allowed launches are tested.
- Related new regression fails before fix and passes after; existing named model and tier tests remain valid. Record exact UV test command/result in task evidence.

T1.AC1: All configured tiers, explicitly tier0,tier1a,tier1b,tier2, resolve bare/suffixed identities to their own T<N>_WINDOW; fixture850000/850000/850000/500000 remains unequal. No universal850k constant or change to individual-slot fallback.
T1.AC2: Named tier launch selects a context-capable tier spelling when necessary, same routing tier; nonexistent and limited-owner forbidden tiers still reject. Both bare and suffixed allowed launches are tested.
T1.AC3: Related new regression fails before fix and passes after; existing named model and tier tests remain valid. Record exact UV test command/result in task evidence.
Global constraints: - Scope product changes to src/superclaude/skills/ccsession-tag/ccsession, src/superclaude/skills/ccsession-tag/models.py and tests/unit/test_ccsession_tiers.py. Source sections Summary/Files/Acceptance in ./source.md govern every task. Coordinator approval is required if another source file becomes necessary.
- Keep routing aliases, actual per-tier/per-model windows, access checks, inherited unavailable default aliases, non-tier profiles, explicit individual-model routing, explicit show-all/+models and user-settings precedence. No dependencies, global settings/env changes, other-worktree edits, commits, push, PR or Orca link flags.
- Native runtime2.1.318 is verified; do not claim all older versions support picker replacement. Manually typing bare IDs inside running Claude Code bypasses launcher normalization; report this external limit rather than a fake fix. Selected individual models may be re-added by native UI, never silently route them to a tier.
- Source is canonical; run make sync-dev after changes, never stage generated .claude mirrors. Always stage .dev/tasks including progress and artifacts. Evidence paths in tasks are package-relative under ./artifacts/.
- Pipeline hardening stays advisory/latched from source; successful tests/reviews cannot promote that to production pipeline signoff. No provider inference is required or authorized for local control probes.

Start sha: 9785004334e809f35036c1b3e4b6a9a5eef3fb8a
Diff against the start snapshot: diff --git a/src/superclaude/skills/ccsession-tag/models.py b/src/superclaude/skills/ccsession-tag/models.py
index 8c5634fb..c7fb714e 100644
--- a/src/superclaude/skills/ccsession-tag/models.py
+++ b/src/superclaude/skills/ccsession-tag/models.py
@@ -723,6 +723,14 @@ def model_window(model: str, data=None, tenv=None) -> tuple:
     tenv = tier_env() if tenv is None else tenv
     # Accept the "[1m]" form users copy from the picker or the Mac profiles.
     model = model[: -len("[1m]")] if model.endswith("[1m]") else model
+    tier = re.fullmatch(r"claude-gw-(tier[0-9]{1,2}[a-z]?)", model)
+    if tier:
+        name = tier.group(1)
+        if name not in data["tiers"]:
+            raise ValueError(f"{name} is not defined")
+        return _window(
+            tenv, f"T{tier_number(name)}_WINDOW"
+        ), f"T{tier_number(name)}_WINDOW"
     # Only slots a tier uses, in tier order: the first one naming the model
     # gives its window, as in compact_settings. The workspace file can keep
     # slots no tier reads (old Tier 1 for older ccsession); they must not win.
@@ -943,13 +951,16 @@ def main(argv) -> int:
         try:
             every, access = tier_access()
             mine, picker = _my_models(every, access)
+            tier = re.fullmatch(r"claude-gw-(tier[0-9]{1,2}[a-z]?)", bare)
+            if tier and tier.group(1) not in access["allowed"]:
+                raise ValueError(unavailable(tier.group(1), access))
             # A -2 picker id takes its own model's window, not the default.
             window, where = model_window(picker.get(bare, model))
         except ValueError as exc:
             print(f"ccsession: {exc}", file=sys.stderr)
             return 3
         # An owner limited to some tiers may name only those tiers' models.
-        if access["allowed"] != access["defined"]:
+        if not tier and access["allowed"] != access["defined"]:
             if bare not in set(mine) | set(picker):
                 print(
                     f"ccsession: {bare} is not in a tier available to {access['user']} "
diff --git a/tests/unit/test_ccsession_tiers.py b/tests/unit/test_ccsession_tiers.py
index 8d55b480..a12c4b51 100644
--- a/tests/unit/test_ccsession_tiers.py
+++ b/tests/unit/test_ccsession_tiers.py
@@ -551,6 +551,49 @@ def test_tier_flag_and_named_model(tmp_path: Path) -> None:
     assert "not in any tier" in err
 
 
+@pytest.mark.parametrize(
+    "tier,window",
+    [
+        ("0", 850000),
+        ("1a", 850000),
+        ("1b", 850000),
+        ("2", 500000),
+        ("3", 500000),
+        ("4", 850000),
+    ],
+)
+@pytest.mark.parametrize("suffix", ["", "[1m]"])
+def test_named_tier_uses_its_own_window(
+    tmp_path: Path, monkeypatch, tier, window, suffix
+) -> None:
+    model = f"claude-gw-tier{tier}{suffix}"
+    monkeypatch.setenv("AIDEV_AI_DEFAULTS_PATH", str(_defaults(tmp_path)))
+    assert models.model_window(model) == (window, f"T{tier}_WINDOW")
+    rc, _, err, seen = _launch(tmp_path, "work", "--model", model)
+    assert rc == 0, err
+    assert _model_arg(seen) == f"claude-gw-tier{tier}[1m]"
+    assert seen["context"] == str(window)
+    assert _compact(seen, f"claude-gw-tier{tier}") == window
+
+
+@pytest.mark.parametrize("tier", ["1a", "2", "7"])
+@pytest.mark.parametrize("suffix", ["", "[1m]"])
+def test_named_tier_checks_definition_and_owner(tmp_path: Path, tier, suffix) -> None:
+    rc, _, err, seen = _launch(
+        tmp_path,
+        "work",
+        "--model",
+        f"claude-gw-tier{tier}{suffix}",
+        defaults=ACCESS_BLOCK,
+        CODER_WORKSPACE_OWNER_NAME="bob",
+    )
+    assert (rc == 0) == (tier == "2"), err
+    if tier == "2":
+        assert seen["context"] == "500000"
+    else:
+        assert seen is None and ("not available" in err or "not defined" in err)
+
+
 def test_tier_launch_permissions_default_keeps_tier_routing(tmp_path: Path) -> None:
     # CCSESSION_PERMISSIONS=default drops only the bypass flag: the tier model,
     # its settings and the shim address are the control launch's. Neither launch
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

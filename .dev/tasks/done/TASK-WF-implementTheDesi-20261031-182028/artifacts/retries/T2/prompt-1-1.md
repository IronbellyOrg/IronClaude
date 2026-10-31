a57d510652fb9e72b67059ec8436a0f3eb19766d
Review one task for spec compliance.

Task brief: ## Task 2: Add the Codex fields to the detection contract

Edit src/superclaude/pr_submit/detection.py and the YAML block in src/superclaude/skills/sc-pr-submit-protocol/refs/detection-contract.md per design section 14: `codex_bot_login` (shipped "chatgpt-codex-connector[bot]"), `codex_app_slug` (shipped "chatgpt-codex-connector"), `codex_retrigger_phrase` (default "@codex review"). `from_yaml` trims the identities like the Augment ones. Direct `DetectionContract()` construction keeps both Codex identities empty (fail-safe, same as Augment), while the shipped ref supplies the real values.

Acceptance criteria:
- `DetectionContract.load()` returns the two Codex identities and the "@codex review" phrase; `DetectionContract()` has empty Codex identities.
- A local override YAML without Codex fields still loads (Codex identities empty, so Codex is disabled for that override) and existing tests in tests/pr_submit/test_detection_contract.py pass.
Global constraints: 
- The design file .dev/pr-submit-codex/design/pr-submit-codex-design.md is the specification; do not add behaviour it does not describe.
- Keep the deterministic core src/superclaude/pr_submit/ free of gh and git command tokens (NFR-6, checked by tests/pr_submit/test_static_grep.py).
- Augment-only behaviour must stay identical apart from the added reviewer_absent event and reviewer fields (design sections 5 and 6); existing tests in tests/pr_submit/ keep passing.
- Never hardcode src/superclaude/ paths inside installed primitives (command, skill, refs, scripts); keep script file names unchanged.
- plugins/superclaude/ has no pr-submit twin (design section 3), so no mirror edit is needed; do not create one.
- Edit src/superclaude/ only, then run make sync-dev; never edit or stage .claude/ copies.
- Run pytest only on named files or tests/pr_submit, never the full suite or tests/cli/eval/ as a directory; use uv run.
- .dev/tasks/ is always staged (git add .dev/tasks), including this package and its artifacts/.
Start sha: a57d510652fb9e72b67059ec8436a0f3eb19766d
Diff against the start snapshot: diff --git a/src/superclaude/pr_submit/detection.py b/src/superclaude/pr_submit/detection.py
index a91ebd4b..3f1ae628 100644
--- a/src/superclaude/pr_submit/detection.py
+++ b/src/superclaude/pr_submit/detection.py
@@ -40,6 +40,15 @@ _CONTRACT_PATH = (
 _LOCAL_OVERRIDE_REL = Path(".dev/pr-monitor/detection-contract.locked.md")
 _LOCAL_OVERRIDE_PATH: Path | None = None
 
+# Shipped Codex (ChatGPT Codex Connector) identity and re-trigger phrase. A YAML
+# contract that OMITS a Codex key falls back to these values (an override written
+# by contract setup has no Codex keys and must not switch Codex off); an explicit
+# empty or null value disables Codex. Direct ``DetectionContract()`` construction
+# keeps both identities empty (fail-safe, like Augment).
+_SHIPPED_CODEX_BOT_LOGIN = "chatgpt-codex-connector[bot]"
+_SHIPPED_CODEX_APP_SLUG = "chatgpt-codex-connector"
+_DEFAULT_CODEX_RETRIGGER_PHRASE = "@codex review"
+
 
 def _local_override_path() -> Path:
     """Return the operator-local locked-contract path (indirection for testability).
@@ -124,14 +133,42 @@ class DetectionContract:
             "augmentcode review",
         ]
     )
+    # --- Codex (ChatGPT Codex Connector) reviewer identity ---
+    # REST shape ``chatgpt-codex-connector[bot]``, GraphQL shape
+    # ``chatgpt-codex-connector``. Empty here (fail-safe); the shipped ref and
+    # from_yaml supply the real values. An empty identity set disables Codex.
+    codex_bot_login: str | None = None
+    codex_app_slug: str | None = None
+    codex_retrigger_phrase: str = _DEFAULT_CODEX_RETRIGGER_PHRASE
 
     @classmethod
     def from_yaml(cls, data: dict) -> "DetectionContract":
-        """Build a contract from YAML, trimming identity padding (no lock enforcement)."""
+        """Build a contract from YAML, trimming identity padding (no lock enforcement).
+
+        Codex keys use key-presence semantics: an absent key falls back to the
+        shipped Codex value; a present empty or null value disables Codex.
+        """
         data = data.copy()
-        for key in ("augment_bot_login", "augment_app_slug"):
+        for key, shipped in (
+            ("codex_bot_login", _SHIPPED_CODEX_BOT_LOGIN),
+            ("codex_app_slug", _SHIPPED_CODEX_APP_SLUG),
+        ):
+            if key not in data:
+                data[key] = shipped
+        for key in (
+            "augment_bot_login",
+            "augment_app_slug",
+            "codex_bot_login",
+            "codex_app_slug",
+        ):
             if isinstance(data.get(key), str):
                 data[key] = data[key].strip()
+        for key in ("codex_bot_login", "codex_app_slug"):
+            if not data.get(key):
+                data[key] = None
+        phrase = data.get("codex_retrigger_phrase")
+        if not isinstance(phrase, str) or not phrase.strip():
+            phrase = _DEFAULT_CODEX_RETRIGGER_PHRASE
         return cls(
             augment_bot_login=data.get("augment_bot_login"),
             augment_author_association=_as_str_list(
@@ -155,6 +192,9 @@ class DetectionContract:
                 data.get("accepted_trigger_phrases"),
                 ["auggie review", "augment review", "augmentcode review"],
             ),
+            codex_bot_login=data["codex_bot_login"],
+            codex_app_slug=data["codex_app_slug"],
+            codex_retrigger_phrase=phrase.strip(),
         )
 
     @classmethod
diff --git a/src/superclaude/skills/sc-pr-submit-protocol/refs/detection-contract.md b/src/superclaude/skills/sc-pr-submit-protocol/refs/detection-contract.md
index 251a1116..b2292240 100644
--- a/src/superclaude/skills/sc-pr-submit-protocol/refs/detection-contract.md
+++ b/src/superclaude/skills/sc-pr-submit-protocol/refs/detection-contract.md
@@ -26,6 +26,11 @@ probe_evidence: null                                 # optional provenance; not
 decline_phrase_regex: 'abnormally\s+large'
 decline_retrigger_regex: 'comment\s+["''`*_]*(augment|auggie|augmentcode)\s+review["''`*_]*'
 accepted_trigger_phrases: ["auggie review", "augment review", "augmentcode review"]
+# Codex (ChatGPT Codex Connector) reviewer. An override that omits these keys keeps the
+# shipped values; an explicit empty value ("") disables Codex.
+codex_bot_login: "chatgpt-codex-connector[bot]"      # REST bot-login shape
+codex_app_slug: "chatgpt-codex-connector"            # GraphQL login shape
+codex_retrigger_phrase: "@codex review"              # documented Codex re-review trigger
 locked: true                                         # vestigial; arming does not check this flag
 ```
 
diff --git a/tests/pr_submit/test_detection_contract.py b/tests/pr_submit/test_detection_contract.py
index 23cc960e..73e5044f 100644
--- a/tests/pr_submit/test_detection_contract.py
+++ b/tests/pr_submit/test_detection_contract.py
@@ -241,6 +241,52 @@ def test_local_override_arms_without_touching_shipped_source(tmp_path, monkeypat
     assert fallback.augment_bot_login == "augmentcode[bot]"
 
 
+def test_shipped_contract_carries_codex_identity_and_direct_construction_is_empty():
+    """The shipped ref supplies the Codex identity and re-trigger phrase; a directly
+    constructed contract keeps the Codex identities empty (fail-safe)."""
+    shipped = DetectionContract.load()
+    assert shipped.codex_bot_login == "chatgpt-codex-connector[bot]"
+    assert shipped.codex_app_slug == "chatgpt-codex-connector"
+    assert shipped.codex_retrigger_phrase == "@codex review"
+    bare = DetectionContract()
+    assert bare.codex_bot_login is None and bare.codex_app_slug is None
+
+
+def test_override_without_codex_keys_keeps_shipped_codex_identity(
+    tmp_path, monkeypatch
+):
+    """An override with no Codex keys (what contract setup writes) keeps Codex on."""
+    from superclaude.pr_submit import detection
+
+    override = tmp_path / "detection-contract.locked.md"
+    override.write_text(
+        '# local\n\n```yaml\naugment_bot_login: "custom-bot[bot]"\nlocked: true\n```\n',
+        encoding="utf-8",
+    )
+    monkeypatch.setattr(detection, "_LOCAL_OVERRIDE_PATH", override)
+    armed = DetectionContract.for_arming()
+    assert armed.augment_bot_login == "custom-bot[bot]"
+    assert armed.codex_bot_login == "chatgpt-codex-connector[bot]"
+    assert armed.codex_app_slug == "chatgpt-codex-connector"
+    assert armed.codex_retrigger_phrase == "@codex review"
+
+
+def test_override_with_empty_codex_values_disables_codex(tmp_path, monkeypatch):
+    """Explicitly empty (or null) Codex identities disable Codex for that override."""
+    from superclaude.pr_submit import detection
+
+    override = tmp_path / "detection-contract.locked.md"
+    override.write_text(
+        '# local\n\n```yaml\naugment_bot_login: "custom-bot[bot]"\n'
+        'codex_bot_login: ""\ncodex_app_slug: null\nlocked: true\n```\n',
+        encoding="utf-8",
+    )
+    monkeypatch.setattr(detection, "_LOCAL_OVERRIDE_PATH", override)
+    armed = DetectionContract.for_arming()
+    assert armed.codex_bot_login is None
+    assert armed.codex_app_slug is None
+
+
 def test_t211_different_bot_not_detected(contract):
     """T-211: a comment/review from a different bot login → review not detected."""
     # Phase 10: swap for load_fixture("review-non-augment.json").
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

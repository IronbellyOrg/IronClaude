179fc29a85b5c0c5641cb8cb73a56bde9305a33a
Review one task for spec compliance.

Task brief: ## Task 7: Link the page from the guide and the documentation index

Depends on: Task 6

Add one link line to `docs/developer-guide/branch-protection.md` pointing at `branch-protection-multi-repo.md` (placed after the introductory paragraph; the commands and the strings pinned by `tests/docs/test_branch_protection_rulesets.py` stay as they are) and two link lines to `docs/developer-guide/documentation-index.md`, one beside the heading entry that names `branch-protection.md` (line 37) and one beside the list entry that names it (line 168). Extend `tests/org_rulesets/test_page.py`.

Acceptance criteria:
- `docs/developer-guide/branch-protection.md` contains one link to `branch-protection-multi-repo.md` and its apply, check and break-glass commands are byte-identical to before.
- `docs/developer-guide/documentation-index.md` contains two links to the new page and its existing `branch-protection.md` entries are unchanged.
- `test_page.py` asserts both links and the guide's link.
- `uv run pytest tests/org_rulesets/ tests/docs/test_branch_protection_rulesets.py -v` passes, `uv run ruff check .` reports nothing new and `uv run ruff format --check scripts/apply_org_rulesets.py tests/org_rulesets` reports nothing.

Global constraints: ## Constraints

- No task calls GitHub or touches any IronbellyGroup repo. Every GitHub call in a test goes through `FakeRunner` of `tests/org_rulesets/conftest.py`; no test starts the real `gh`.
- `.github/rulesets/*.json`, the commands in `docs/developer-guide/branch-protection.md` and `tests/docs/test_branch_protection_rulesets.py` stay unchanged. The only edit to the guide is the one link line of Task 7. The existing test must keep passing.
- Python 3.10, standard library only; ruff rules `E,F,I,N,W,TID` at line length 88 as set in `pyproject.toml`.
- No real private repo name and no real org login is written in any tracked file. Tests use synthetic names such as `acme-one`. The script holds no org or repo name, except the upstream org name it refuses.
- Only these paths may change: `scripts/apply_org_rulesets.py`, `tests/org_rulesets/`, `docs/developer-guide/branch-protection-multi-repo.md`, `docs/developer-guide/branch-protection.md` (one link line) and `docs/developer-guide/documentation-index.md`. Nothing under `.claude/` or `.github/` changes.
- "source.md section 2.3" names a heading of `./source.md`.
- Test setup follows `tests/worktree_cleanup/conftest.py` (the session fixture `wc` at lines 26 to 37 loads the script once; `RecordingRunner` at lines 68 to 109 subclasses the real `Runner` and overrides `_execute`). `tests/org_rulesets/conftest.py` defines the session fixture `orr` (the script module) and every shared fixture exactly once; a test module never imports a fixture from another module, because CI lists fixtures with `pytest --fixtures` and a duplicate crashes it.
- Location rule: the repo root is `Path(__file__).resolve().parent.parent`, the rule files are read from `<root>/.github/rulesets/`, and no function reads the current working folder. The before-state file is written into the folder given with `--out`.
- Choices for the owner's review (all are made inside the scope cut and listed in the pull request): one repo per run; the push check excuses no direct push by a named person; the tag ruleset is applied with a printed warning and a manual check of release workflows; rollback is manual.
- Every task ends with the same checks: `uv run pytest tests/org_rulesets/` passes (plus `tests/docs/test_branch_protection_rulesets.py` from Task 6 on), `uv run ruff check scripts/apply_org_rulesets.py tests/org_rulesets` reports nothing and `uv run ruff format --check scripts/apply_org_rulesets.py tests/org_rulesets` reports nothing.

Start sha: 179fc29a85b5c0c5641cb8cb73a56bde9305a33a
Diff against the start snapshot: diff --git a/docs/developer-guide/branch-protection.md b/docs/developer-guide/branch-protection.md
index addb45f3f..e0881867e 100644
--- a/docs/developer-guide/branch-protection.md
+++ b/docs/developer-guide/branch-protection.md
@@ -2,6 +2,8 @@
 
 `master`, `integration` and the `v*` release tags of `IronbellyOrg/IronClaude` are protected by three GitHub repository rulesets. The rulesets are kept as JSON in `.github/rulesets/`; this page says what they do, how to apply and check them, and how to break glass.
 
+To put the same rulesets on another repo of an organization, see [Branch Protection for Other Repos](branch-protection-multi-repo.md).
+
 ## What is protected
 
 | Ruleset | File | Target | Rules |
diff --git a/docs/developer-guide/documentation-index.md b/docs/developer-guide/documentation-index.md
index 05f244950..54ac47b8b 100644
--- a/docs/developer-guide/documentation-index.md
+++ b/docs/developer-guide/documentation-index.md
@@ -39,6 +39,8 @@ This index provides comprehensive access to all SuperClaude Framework developmen
 **Purpose**: The three rulesets that make `master` and `integration` pull-request-only and protect `v*` release tags: what they do, how to apply and check them, how to break glass  
 **Target Audience**: Repository admins and maintainers
 
+**See also**: [Branch Protection for Other Repos](branch-protection-multi-repo.md) - the same rulesets on other repos of an organization, one repo per run
+
 ### 🌿 [Git Standards and Repository Protocols](git-standards-protocols.md) (imported, not IronClaude's process)
 
 **Status**: This file was copied from another project and is not IronClaude's process. Its branches, environments and links belong to that project. It is kept until it is rewritten for IronClaude or deleted. Do not follow it.
@@ -166,6 +168,7 @@ For IronClaude, the branch model is `master` ← `integration` ← `feature/*`,
 
 - [Release Procedure](release-procedure.md) - Version bump, release notes, G1-G9 gate, tag and GitHub release
 - [Branch Protection](branch-protection.md) - Rulesets for `master`, `integration` and `v*` tags; apply, check, break glass
+- [Branch Protection for Other Repos](branch-protection-multi-repo.md) - Apply the rulesets to other repos, one repo per run
 
 ### 🛠️ MCP Integration
 
diff --git a/tests/org_rulesets/test_page.py b/tests/org_rulesets/test_page.py
index 89f55e70b..9855e262f 100644
--- a/tests/org_rulesets/test_page.py
+++ b/tests/org_rulesets/test_page.py
@@ -148,3 +148,33 @@ def test_no_real_private_repo_name_is_written_in_a_tracked_file():
         text = path.read_text(encoding="utf-8", errors="ignore").lower()
         for name in names:
             assert name.lower() not in text, f"{name} in {path.name}"
+
+
+GUIDE = ROOT / "docs" / "developer-guide" / "branch-protection.md"
+INDEX = ROOT / "docs" / "developer-guide" / "documentation-index.md"
+LINK = "(branch-protection-multi-repo.md)"
+
+
+def test_the_guide_links_to_the_page_once_and_keeps_its_commands():
+    text = GUIDE.read_text(encoding="utf-8")
+    assert text.count("branch-protection-multi-repo.md") == 1
+    assert f"[Branch Protection for Other Repos]{LINK}" in text
+    for fragment in (
+        "gh api --method POST repos/",
+        "/rulesets --input .github/rulesets/protect-release-tags.json",
+        "/rules/branches/master --jq '.[].type'",
+        "/rulesets/<id> -f enforcement=disabled",
+        "gh api --method DELETE repos/",
+    ):
+        assert fragment in text, fragment
+
+
+def test_the_index_links_to_the_page_twice_and_keeps_its_entries():
+    text = INDEX.read_text(encoding="utf-8")
+    assert text.count("branch-protection-multi-repo.md") == 2
+    assert text.count(f"[Branch Protection for Other Repos]{LINK}") == 2
+    assert "### 🔒 [Branch Protection](branch-protection.md)" in text
+    assert (
+        "- [Branch Protection](branch-protection.md) - Rulesets for `master`, "
+        "`integration` and `v*` tags; apply, check, break glass"
+    ) in text

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

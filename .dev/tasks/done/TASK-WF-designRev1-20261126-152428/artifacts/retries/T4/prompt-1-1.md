73bc90af153ee266717cd2b065f2fd561709df7f
Review one task for spec compliance.

Task brief: ## Task 4: Extend tests/docs/test_branch_protection_rulesets.py

Depends on: Task 1, Task 2, Task 3

Extend `tests/docs/test_branch_protection_rulesets.py` as in section 3.2 of `./source.md`. Keep every existing assertion and the existing `_load` (callers `test_branch_rulesets` at line 30 and `test_tag_ruleset` at line 47, both unchanged). Change `test_no_default_branch_token_anywhere` (the function starting at line 66) from `_RULESETS.glob("*.json")` to `_RULESETS.rglob("*.json")`. Add the constant `_OTHER` (`_RULESETS / "other-repos"`), a loader `_load_other(name)` that reads from it, and the constant `_TARGETS`: for each of the six repos its applier (`clay` or `ryan`), its candidate branch files (a fork lists both `protect-main` and `protect-main-mirror`, and IronHands-CLI is a fork as well as CPA-Manager-Plus and IronOrca; irondots, ironops-marketplace and coder_orca list `protect-main`; `protect-aidev02` is listed for IronOrca and marked optional) and its tag entry (`conditional`, `skip` or `handoff`). Add four tests with these names: `test_other_repos_full_role_derived` (`protect-main`, and `protect-aidev02` if the file exists, equal `protect-master` after replacing only `name` and `ref_name.include`, with rule types `deletion`, `non_fast_forward`, `pull_request`, the admin `pull_request` bypass actor and zero approvals), `test_other_repos_mirror_derived` (the mirror equals `protect-main` after replacing `name` and removing the `pull_request` rule, with rule types `deletion` and `non_fast_forward` and the same bypass), `test_other_repos_files_match_targets` (the set of `*.json` files in `other-repos/` equals the set named in `_TARGETS`; a file marked optional may be absent; a missing, unused or unlisted file fails) and `test_guide_has_other_repos_section` (the guide contains the heading `Other IronbellyOrg repos`, every repo name in `_TARGETS`, the path of every `*.json` file that exists in `other-repos/`, the path `.github/rulesets/other-repos/protect-aidev02.json`, `$REPO`, `$BRANCH`, `admin:org`, `ahead_by` and `zz-selftest-`). Because the test reads the files that exist, an absent optional `protect-aidev02.json` does not fail it. Dependents: no other indexed file imports this test (graph lead, not proof), so the full `tests/docs` folder is run too.

Acceptance criteria:
- `uv run pytest tests/docs/test_branch_protection_rulesets.py --collect-only -q` lists `test_branch_rulesets[protect-master-refs/heads/master]`, `test_branch_rulesets[protect-integration-refs/heads/integration]`, `test_tag_ruleset`, `test_no_default_branch_token_anywhere`, `test_guide_has_apply_and_check_commands` and the four new tests named above.
- `uv run pytest tests/docs/test_branch_protection_rulesets.py -v` passes, `uv run pytest tests/docs -q` passes, and `uv run ruff check tests/docs/test_branch_protection_rulesets.py` reports no error. The repository-wide `make lint` is run and recorded by Task 14, not here, because it also runs `lint-architecture` over every file.
- Reading the test shows `rglob("*.json")` in `test_no_default_branch_token_anywhere`, an unchanged `_load` and no change to `_BRANCH_FILES`.
- The files-match-the-table test would fail for a missing `protect-main-mirror.json` or for an extra unlisted `*.json` in `other-repos/` (shown by reading the assertion; `protect-aidev02.json` must not exist after this task).
Global constraints: ## Constraints

- This plan only writes files in this worktree and runs read-only `gh api` GET calls. No task may send POST, PUT or DELETE to any GitHub ruleset, create a branch or ruleset in another repository, comment on an issue or edit a pull request. Applying rulesets is "Phase 3" of `./source.md` section 4 and is carried out from the runbook that Task 13 produces, after the pull request monitor has settled, never by `/sc:implement`.
- Never write to IronHands-CLI, irondots, ironops-marketplace, the archived IronHands repo, or any repository outside IronbellyOrg. Every `gh` call names its repository in full (`repos/IronbellyOrg/<repo>/...`, or `--repo IronbellyOrg/IronClaude`) except `gh api user`; never rely on the fork-parent default and never touch `SuperClaude-Org/SuperClaude_Framework`.
- Where `./source.md` section 2 names the four state files, this plan writes them there and nowhere else: `.dev/issues/837/audit/<repo>.md`, `.dev/issues/837/gates.md`, `.dev/issues/837/handoff-ryan.md` and `.dev/issues/837/apply-runbook.md`. They are never staged. The drafted pull request body goes to `.dev/issues/837/pr-body.md`. The package `./artifacts/` folder holds only the codegraph grounding note. The results of the later apply are recorded in the audit file and the ledger, as section 3.6 of `./source.md` says; there is no separate apply-results file.
- IronClaude is public and `IronbellyOrg/Coder` is private (Revision 1 of `./source.md`). Nothing that describes the internals of the private repository's release tooling (its file name, folder, function names, lines or line numbers) may be written to any file under `.dev/tasks/`, to any log or QA output captured there, to the pull request body or to an issue comment. The only neutral sentence allowed in such places is: "release tooling in another IronbellyOrg repository deletes these tags; the tag ruleset is skipped for coder_orca". Task 5 reads the tooling without printing or saving its lines and keeps the evidence only in `.dev/issues/837/private/`, which is never staged. Those names are not written in this plan: E-2 of `.dev/brainstorms/20261126-115959-apply-branch-protection-rulesets-other-repos/merged-requirements.md` lists them.
- Do not create `.github/rulesets/other-repos/protect-aidev02.json`: it needs Clay's written yes for `aidev02`, which is not recorded in `.dev/issues/837/issue-summary.md`.
- IronClaude's three existing files `.github/rulesets/protect-master.json`, `protect-integration.json` and `protect-release-tags.json` and the live IronClaude rulesets stay unchanged. Every existing assertion in `tests/docs/test_branch_protection_rulesets.py` stays.
- Facts that nobody verified stay labelled UNVERIFIED in every file this plan writes: whether the Sync fork button is refused under a `pull_request` rule, whether `clayphi`'s token can create rulesets, whether the API accepts a duplicate ruleset name, whether the mirror's bypass actor is accepted without a `pull_request` rule, and whether `time_period=quarter` is 90 days (it is not used).
- A check that cannot run (for example `gh api --paginate orgs/IronbellyOrg/installations`, which needs the `admin:org` scope) is written down as "could not run" with the real error text and blocks the repo it covers; it is never recorded as clean.
- Clay's recorded answer is in `.dev/issues/837/issue-summary.md` under "Decided for this work (iteration 3)". It is quoted word for word wherever a task says to quote it, never paraphrased. The lead's note in it, that the release-tag ruleset has its `update` rule on integration (pull request 844 merged), was verified before this plan: `.dev/issues/837/accuracy-check.md` line 13 records commit 206abea1c and the live ruleset 28081842 with `update`.
- This plan does not commit or push. Those are later story steps.
Start sha: 73bc90af153ee266717cd2b065f2fd561709df7f
Diff against the start snapshot: Changed files (name-status):
M	tests/docs/test_branch_protection_rulesets.py


diff --git a/tests/docs/test_branch_protection_rulesets.py b/tests/docs/test_branch_protection_rulesets.py
index eb91dc7b3..8e0f7dc5a 100644
--- a/tests/docs/test_branch_protection_rulesets.py
+++ b/tests/docs/test_branch_protection_rulesets.py
@@ -26,6 +26,27 @@ def _load(name):
     return json.loads((_RULESETS / f"{name}.json").read_text(encoding="utf-8"))
 
 
+# Other IronbellyOrg repos (issue 837): ruleset files derived from protect-master, one table of targets.
+_OTHER = _RULESETS / "other-repos"
+
+# applier: who applies; branch: candidate files (a fork lists both roles, the role is chosen on apply day);
+# optional: files that may be absent (aidev02 needs a written yes); tag: conditional, skip or handoff.
+_TARGETS = {
+    "CPA-Manager-Plus": {"applier": "clay", "branch": ["protect-main", "protect-main-mirror"], "optional": [], "tag": "conditional"},
+    "IronOrca": {"applier": "clay", "branch": ["protect-main", "protect-main-mirror"], "optional": ["protect-aidev02"], "tag": "conditional"},
+    "coder_orca": {"applier": "clay", "branch": ["protect-main"], "optional": [], "tag": "skip"},
+    "IronHands-CLI": {"applier": "ryan", "branch": ["protect-main", "protect-main-mirror"], "optional": [], "tag": "handoff"},
+    "irondots": {"applier": "ryan", "branch": ["protect-main"], "optional": [], "tag": "handoff"},
+    "ironops-marketplace": {"applier": "ryan", "branch": ["protect-main"], "optional": [], "tag": "handoff"},
+}
+
+_FULL_ROLE_FILES = {"protect-main": "refs/heads/main", "protect-aidev02": "refs/heads/aidev02"}
+
+
+def _load_other(name):
+    return json.loads((_OTHER / f"{name}.json").read_text(encoding="utf-8"))
+
+
 @pytest.mark.parametrize("name,ref", _BRANCH_FILES.items())
 def test_branch_rulesets(name, ref):
     data = _load(name)
@@ -64,7 +85,7 @@ def test_tag_ruleset():
 
 
 def test_no_default_branch_token_anywhere():
-    for path in _RULESETS.glob("*.json"):
+    for path in _RULESETS.rglob("*.json"):
         assert "~DEFAULT_BRANCH" not in path.read_text(encoding="utf-8"), path.name
 
 
@@ -75,3 +96,50 @@ def test_guide_has_apply_and_check_commands():
     assert "enforcement=disabled" in text
     for name in (*_BRANCH_FILES, "protect-release-tags"):
         assert f".github/rulesets/{name}.json" in text
+
+
+def test_other_repos_full_role_derived():
+    for name, ref in _FULL_ROLE_FILES.items():
+        if not (_OTHER / f"{name}.json").exists():
+            # Only a file marked optional in the table may be absent.
+            assert any(name in t["optional"] for t in _TARGETS.values()), name
+            continue
+        expected = _load("protect-master")
+        expected["name"] = name
+        expected["conditions"]["ref_name"]["include"] = [ref]
+        data = _load_other(name)
+        assert data == expected, name
+        assert sorted(r["type"] for r in data["rules"]) == ["deletion", "non_fast_forward", "pull_request"]
+        assert data["bypass_actors"] == [_ADMIN_PR_BYPASS]
+        pr = next(r for r in data["rules"] if r["type"] == "pull_request")
+        assert pr["parameters"]["required_approving_review_count"] == 0
+
+
+def test_other_repos_mirror_derived():
+    expected = _load_other("protect-main")
+    expected["name"] = "protect-main-mirror"
+    expected["rules"] = [r for r in expected["rules"] if r["type"] != "pull_request"]
+    data = _load_other("protect-main-mirror")
+    assert data == expected
+    assert sorted(r["type"] for r in data["rules"]) == ["deletion", "non_fast_forward"]
+    assert data["bypass_actors"] == [_ADMIN_PR_BYPASS]
+
+
+def test_other_repos_files_match_targets():
+    on_disk = {p.stem for p in _OTHER.rglob("*.json")}
+    required = {n for t in _TARGETS.values() for n in t["branch"]} - {n for t in _TARGETS.values() for n in t["optional"]}
+    optional = {n for t in _TARGETS.values() for n in t["optional"]}
+    assert required <= on_disk, f"missing: {sorted(required - on_disk)}"
+    assert on_disk <= required | optional, f"unlisted: {sorted(on_disk - required - optional)}"
+
+
+def test_guide_has_other_repos_section():
+    text = _GUIDE.read_text(encoding="utf-8")
+    assert "\n## Other IronbellyOrg repos\n" in text
+    for repo in _TARGETS:
+        assert repo in text, repo
+    for path in sorted(_OTHER.rglob("*.json")):
+        assert f".github/rulesets/other-repos/{path.name}" in text, path.name
+    assert ".github/rulesets/other-repos/protect-aidev02.json" in text
+    for token in ("$REPO", "$BRANCH", "admin:org", "ahead_by", "zz-selftest-"):
+        assert token in text, token


Codegraph context: index_state: fresh; checked_at: 2026-11-26T15:31:43Z; worktree_root: /home/coder/workspaces/worktrees/IronClaude/issue-837; projectPath: /home/coder/workspaces/worktrees/IronClaude/issue-837. Call codegraph only when index_state: fresh, never to widen scope. Q2b: the files of this task are JSON and Markdown (not indexed) unless a Python file is named; dependents were checked with Grep.
Note on files the diff cannot show: paths under `.dev/issues/837/private/` are git-ignored, so they are absent from the diff; read them directly with Read when a task names them. Never print private content in your answer.
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

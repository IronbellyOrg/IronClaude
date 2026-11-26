b945bc64a165ec31cdfe5d1a07d69235e9f69f3d
Review one task for spec compliance.

Task brief: ## Task 8: Add tests/skills/test_post_release_base_branch.py

Depends on: Task 7

Create `tests/skills/test_post_release_base_branch.py` (design section 3.4 in `./source.md`), following the pattern of `tests/skills/test_primitive_dual_surface_lookup.py` (a `_SKILLS = Path(__file__).resolve().parents[2] / "src" / "superclaude" / "skills"` constant and a helper that reads `sc-post-release-protocol/SKILL.md` as lines).

- `_paragraph()`: the line that starts with `**Anchor the scan to the tagged commit.**`.
- Assert the paragraph contains `git ls-remote --symref origin HEAD`, `git fetch origin <default-branch> --tags`, `git merge-base --is-ancestor <tag> refs/remotes/origin/<default-branch>`, `unverified` and `git branch -r --contains <tag>`.
- Assert the whole file does not contain `git merge-base --is-ancestor <tag> <default-branch>`.
- Assert `re.search(r"\b(main|master|integration)\b", paragraph)` is `None`.
- Assert the line that starts with `**Output:** resolved tag` contains `default branch (resolved live, with its source)` and the line that starts with `**Exit criteria:** tag anchored` contains `default branch resolved and its source recorded`.
- Assert the WARN line (the line that contains `then continue, anchored to the tag`) still ends with that phrase, allowing the full stop that ends the line: `line.rstrip().rstrip(".").endswith("then continue, anchored to the tag")`. Assert the Guardrails section names the offline fallback and "ask the user".
- Assert `src/superclaude/commands/post-release.md` does not contain `--base`.
- Mutation check, done once by hand and recorded in `./artifacts/t8-mutation-check.md` (commands that touch `./artifacts/` run with the package folder as the working directory and reach the skill file through `"$(git rev-parse --show-toplevel)"`): before the first mutation record the `sha256sum` of the skill file in `./artifacts/t8-skill.sha256` and save a copy as `./artifacts/t8-skill.pre-mutation`; both are written once and never overwritten on a rerun. For each assertion group (the paragraph, the old command, the regular expression, the Output and Exit criteria lines, the WARN line and Guardrails text), revert the matching Task 7 edit in place, confirm the matching assertion fails and that `cmp` against the saved copy exits 1, then restore the skill file by copying the saved file back and confirm `cmp` exits 0. At the end `sha256sum -c` passes and the Task 8 tests pass on the restored file. Never use a command that discards uncommitted changes on the skill file (`git checkout`, `git restore`, `git reset --hard`, `git stash`): the Task 7 edits are not committed. The assertion that `src/superclaude/commands/post-release.md` does not contain `--base` is a static guard on a file this plan never edits: it runs with the other assertions, must pass on the unedited file, and gets no mutation.
- No temporary-history fixture: it would test git, not the skill text.

Acceptance criteria:
- `uv run pytest tests/skills/test_post_release_base_branch.py -v` passes.
- `./artifacts/t8-mutation-check.md` lists a failing mutation for each of the five assertion groups that read `SKILL.md`, the checksum before and after, and states that the skill file was restored by copy and that the `--base` assertion is a static guard with no mutation.
- `uv run pytest tests/skills/test_worker_contract.py tests/unit/test_cli_install.py -q` still passes (they reference the skill path and file list).


AC ids (source order):
T8.AC1 = `uv run pytest tests/skills/test_post_release_base_branch.py -v` passes.
T8.AC2 = `./artifacts/t8-mutation-check.md` lists a failing mutation for each of the five assertion groups that read `SKILL.md`, the checksum before and after, and states that the skill file was restored by copy and that the `--base` assertion is a static guard with no mutation.
T8.AC3 = `uv run pytest tests/skills/test_worker_contract.py tests/unit/test_cli_install.py -q` still passes (they reference the skill path and file list).
Global constraints: ## Constraints

- Edit under `src/superclaude/` first, never under `.claude/`; run `make sync-dev` then `make verify-sync`; never stage anything under `.claude/` or `.dev/issues/`.
- Documentation, skill text and two new tests only: no Python under `src/superclaude/cli/`, no edit to `.github/rulesets/` or `.github/workflows/`, no release script, no new `/sc:post-release` flag, no edit to `src/superclaude/commands/post-release.md`.
- Every `gh` command written into `docs/developer-guide/release-procedure.md` is on one line and carries `--repo IronbellyOrg/IronClaude` (or is `gh api repos/IronbellyOrg/IronClaude ...`). Installed primitives (the skill) name no `src/superclaude/` path and no literal branch name in the edited paragraph.
- No task creates a repository, pushes, tags, merges or opens a pull request on GitHub, with two exceptions that each need the owner's explicit approval in this session: the scratch-repository run of Task 13 and the one `gh issue comment` of Task 13. Read-only `gh api` GET calls on `IronbellyOrg/IronClaude` and read-only git checks of this repository stay allowed. The approval for the scratch repository must name it as the owner's exception to the project rule that the fork is the only target (`CLAUDE.md:49`, `CLAUDE.md:52`, `CLAUDE.md:76`); without that approval Task 13 records "not exercised".
- The headings `Step 1` to `Step 4`, `What a release is here` and `Sources` of the release page keep their text; the old Step 5 becomes Step 6 and a new Step 5 is added.
- No task of this plan commits. The delivery order applies to the story's commit step after the plan finishes: three commit groups, (1) `docs/developer-guide/release-procedure.md`, `CLAUDE.md`, `CONTRIBUTING.md` and `tests/docs/test_release_procedure.py`, (2) the skill text and `tests/skills/test_post_release_base_branch.py`, (3) the example commands; commit types `docs(release)` for (1) and (3) and `fix(post-release)` for (2); a last group (4) carries `.dev/tasks` (this package with its `./artifacts/` and the archived earlier plans) and `docs/memory/reflect/deviation-patterns-IronClaude.md`, has commit type `docs(dev)` and is committed last and alone; `.dev/reflect/`, `.dev/brainstorms/` and `.dev/issues/` are not committed; each group is committed with only its own paths so each can be reverted alone; `make sync-dev` and `make verify-sync` run after (2) and (3) (Task 11 runs them once at the end of the plan); the pull request body says when the rehearsal acceptance is only partly met.
- `./artifacts/` is the `artifacts` folder next to this plan. A command that reads or writes it runs with the package folder (the folder that holds this plan and `source.md`) as the working directory, in the same shell call; it reaches repository files through `"$(git rev-parse --show-toplevel)"`.
- Where this plan overrides the design: the H2 order of `test_contents_links_resolve` (design section 3.3, `source.md:150`) and the path of the local rehearsal log (design section 3.6, `source.md:186`) follow the "Revision 1" section of `./source.md`.

Start sha: b945bc64a165ec31cdfe5d1a07d69235e9f69f3d
Diff against the start snapshot: diff --git a/tests/skills/test_worker_contract.py b/tests/skills/test_worker_contract.py
index a0abf4283..0ee28a0ef 100644
--- a/tests/skills/test_worker_contract.py
+++ b/tests/skills/test_worker_contract.py
@@ -2370,7 +2370,7 @@ WRITE_VERB_CLASSIFICATION = {
     (
         "src/superclaude/skills/sc-post-release-protocol/SKILL.md",
         "git worktree add+git worktree remove",
-        "**Anchor the scan to the tagged commit.** Once the tag is resolved, read the release's code surface **at that tag** — e.g. `git show <tag>:<path>`, `git ls-tree <tag>`, or a `git worktree add` / `git archive` checkout of the tag — rather than the current working tree. Such a checkout is made in a temporary directory and removed with `git worktree remove` after the scan. Confirm the tag actually belongs to the release lineage (`git merge-base --is-ancestor <tag> <default-branch>`); if it is **not** an ancestor of the mainline, or the tree's version metadata disagrees with the tag, treat that as a release-integrity finding and report it before proceeding. **Auto-detect the default branch** (e.g. `git symbolic-ref refs/remotes/origin/HEAD`) — do not assume `main`/`master`.",
+        "**Anchor the scan to the tagged commit.** Once the tag is resolved, read the release's code surface **at that tag** — e.g. `git show <tag>:<path>`, `git ls-tree <tag>`, or a `git worktree add` / `git archive` checkout of the tag — rather than the current working tree. Such a checkout is made in a temporary directory and removed with `git worktree remove` after the scan. Confirm the tag actually belongs to the release lineage. Resolve the default branch `<default-branch>` live with `git ls-remote --symref origin HEAD` (the `ref: refs/heads/<name>` line gives `<name>`); only when that call cannot reach the remote, fall back to `git symbolic-ref refs/remotes/origin/HEAD`, which can be stale. Record the value and which source gave it. Then run `git fetch origin <default-branch> --tags` and `git merge-base --is-ancestor <tag> refs/remotes/origin/<default-branch>`; never compare against a bare local branch name, which can be far behind its remote. If the fetch fails or the value came from the fallback, report the ancestry check as **unverified**, never as passed. If the tag is **not** an ancestor of the mainline, or the tree's version metadata disagrees with the tag, treat that as a release-integrity finding and report it before proceeding; with the finding, list the remote branches that contain the tag (`git branch -r --contains <tag>`, without the `origin/HEAD ->` alias line, at most 10, say when the list is cut off; when none: \"no remote branch contains `<tag>`\") and say that the release branch may not yet have been merged back into the default branch and should be merged back by pull request. Never hard-code a branch name.",
     ): (
         "deferred:P4",
         "/sc:post-release is converted in P4 with every outward and git-writing step off under --unattended (decision D4)",

diff --git a/tests/skills/test_post_release_base_branch.py b/tests/skills/test_post_release_base_branch.py
new file mode 100644
index 000000000..0f72a612d
--- /dev/null
+++ b/tests/skills/test_post_release_base_branch.py
@@ -0,0 +1,80 @@
+"""Pin how /sc:post-release resolves the default branch and checks the tag lineage (issue 826).
+
+The skill must resolve the default branch live from the remote, compare the tag with the remote
+ref (never a bare local branch that can be far behind), report an unverified check as unverified,
+and name no branch. CI-safe, no network.
+"""
+
+import re
+from pathlib import Path
+
+import pytest
+
+_SRC = Path(__file__).resolve().parents[2] / "src" / "superclaude"
+_SKILL = _SRC / "skills" / "sc-post-release-protocol" / "SKILL.md"
+_COMMAND = _SRC / "commands" / "post-release.md"
+
+
+def _lines() -> list[str]:
+    return _SKILL.read_text(encoding="utf-8").splitlines()
+
+
+def _line_starting(prefix: str) -> str:
+    (line,) = [ln for ln in _lines() if ln.startswith(prefix)]
+    return line
+
+
+def _paragraph() -> str:
+    return _line_starting("**Anchor the scan to the tagged commit.**")
+
+
+def _guardrails() -> str:
+    text = "\n".join(_lines())
+    return text[text.index("## Guardrails") :]
+
+
+@pytest.mark.parametrize(
+    "required",
+    [
+        "git ls-remote --symref origin HEAD",
+        "git fetch origin <default-branch> --tags",
+        "git merge-base --is-ancestor <tag> refs/remotes/origin/<default-branch>",
+        "unverified",
+        "git branch -r --contains <tag>",
+    ],
+)
+def test_paragraph_names_live_resolution_and_remote_check(required):
+    assert required in _paragraph()
+
+
+def test_old_local_branch_comparison_is_gone():
+    text = _SKILL.read_text(encoding="utf-8")
+    assert "git merge-base --is-ancestor <tag> <default-branch>" not in text
+
+
+def test_paragraph_names_no_branch():
+    # The word "mainline" is allowed; a literal branch name is not.
+    assert re.search(r"\b(main|master|integration)\b", _paragraph()) is None
+
+
+def test_output_and_exit_lines_say_resolved_with_source():
+    output = _line_starting("**Output:** resolved tag")
+    exit_criteria = _line_starting("**Exit criteria:** tag anchored")
+    assert "default branch (resolved live, with its source)" in output
+    assert "default branch resolved and its source recorded" in exit_criteria
+
+
+def test_warn_line_still_ends_with_the_tag():
+    (line,) = [ln for ln in _lines() if "then continue, anchored to the tag" in ln]
+    assert line.rstrip().rstrip(".").endswith("then continue, anchored to the tag")
+
+
+def test_guardrails_name_the_offline_fallback_and_ask_the_user():
+    guardrails = _guardrails()
+    assert "offline fallback" in guardrails
+    assert "ask the user" in guardrails
+
+
+def test_post_release_command_has_no_base_flag():
+    # A static guard on a file the release work never edits: the command takes no new flag.
+    assert "--base" not in _COMMAND.read_text(encoding="utf-8")

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

445925bde6f8d2774511ddbec01489c9e504ea99
Review one task for spec compliance.

Task brief: ## Task 6: Add tests/docs/test_release_procedure.py

Depends on: Task 3

Create `tests/docs/test_release_procedure.py` (design section 3.3 in `./source.md`), following the pattern of `tests/docs/test_branch_protection_rulesets.py` (module constants `_REPO = Path(__file__).resolve().parents[2]`, `Path.read_text(encoding="utf-8")`, `pytest.mark.parametrize`). It reads `docs/developer-guide/release-procedure.md`.

- Constants and helpers: `_PAGE`, `_TEXT` (page text), `_fenced_lines(text=_TEXT)` returning the stripped lines inside the triple-backtick fences of `text` (a fence marker may be indented, as in the list items of Step 2), and `_section(title_start)` returning the page text from the H2 heading that starts with `title_start` up to the next H2 heading.
- `_REQUIRED_COMMANDS`: a module-level tuple of exact strings, one per command written in Tasks 1 to 3, except the two that the page also states in other sections (they are checked by the Step 2 test below): `/sc:pr-submit --monitor 3 --head <branch> --base integration`; `--base integration --head <branch>`; `gh pr create --repo IronbellyOrg/IronClaude --base master --head integration`; `gh pr checks <n> --repo IronbellyOrg/IronClaude --watch`; `git switch --detach <reviewed-head-sha>`; `gh pr merge <n> --repo IronbellyOrg/IronClaude --merge --match-head-commit <reviewed-head-sha>`; `--json state,baseRefName,headRefName,headRefOid,mergeCommit`; `git rev-parse --verify -q <merge-sha>^2`; `git rev-parse --verify -q <merge-sha>^3`; `git rev-parse <merge-sha>^{tree} <reviewed-head-sha>^{tree}`; the G2 command `gh run list --repo IronbellyOrg/IronClaude --workflow Tests --event push --branch master --commit <merge-sha> --json databaseId,status,conclusion`; `git ls-remote --tags origin vX.Y.Z`; `git ls-remote origin 'refs/tags/vX.Y.Z^{}'`; `git rev-parse vX.Y.Z^{commit}`; `gh pr create --repo IronbellyOrg/IronClaude --base integration --head master`; `gh pr merge <m> --repo IronbellyOrg/IronClaude --merge`; `git merge-base --is-ancestor <merge-sha> origin/integration`; `git switch -c post-release-vX.Y.Z origin/integration`; `/sc:post-release vX.Y.Z`; and the commands that Tasks 1 to 3 write and this list had left out: `gh pr view <n> --repo IronbellyOrg/IronClaude --json headRefOid --jq .headRefOid`; `git rev-parse origin/master`; `gh api repos/IronbellyOrg/IronClaude --jq`; `git rev-parse <merge-sha>^1 <merge-sha>^2`; `git tag --list vX.Y.Z`; `git tag -a vX.Y.Z <merge-sha>`; `git push origin vX.Y.Z`. One parametrized test asserts each is a substring of `_TEXT`. The flag `--verify-tag` is not in this tuple, because the page also explains it in prose: `test_verify_tag_on_the_release_line` below checks it.
- `test_step2_has_its_own_commands`: `make sync-dev` and `git merge-base --is-ancestor origin/master origin/integration` are each one of the stripped fenced lines in `_fenced_lines(_section("Step 2"))`, so removing the Step 2 precondition or the detached-checkout `make sync-dev` line fails this test even though the page states both in prose elsewhere (the release-notes item of Step 2 names `make sync-dev` in prose, and Step 5 states the ancestry fact).
- `test_verify_tag_on_the_release_line`: a fenced line that starts with `gh release create` contains `--verify-tag`, so deleting the flag from that line fails the test although the page also explains the flag in prose.
- `test_every_gh_line_names_the_fork`: each fenced line starting with `gh ` contains `--repo IronbellyOrg/IronClaude` or starts with `gh api repos/IronbellyOrg/IronClaude`.
- `test_banned_merge_options`: none of `--admin`, `--auto`, `--squash`, `--rebase`, `--delete-branch` appears in a fenced line, and any non-fenced line containing one also contains `never` (case-insensitive).
- `test_removed_text_is_gone`: the page lacks `--base master --head <branch>`, `--limit 3`, and "Every merge to `master` therefore reaches".
- `test_contents_links_resolve`: every `](#anchor)` in the Contents list equals the GitHub slug of one H2 heading (slug: lowercase, drop characters that are not word characters, spaces or hyphens, spaces to hyphens), and the H2 order is: Contents, What a release is here, Step 1 to Step 6, Sources. The `## Contents` heading stays on the page and the Contents list keeps its eight entries. This line overrides design section 3.3 (`source.md:150`), which left Contents out of the order.
- Mutation check, done once by hand and recorded in `./artifacts/t6-mutation-check.md` (commands that touch `./artifacts/` run with the package folder as the working directory and reach the page through `"$(git rev-parse --show-toplevel)"`): before the first mutation record the `sha256sum` of the page in `./artifacts/t6-page.sha256` and save a copy as `./artifacts/t6-page.pre-mutation`; both are written once and never overwritten on a rerun. For each group of required commands, remove or alter one line of the page in place, confirm the matching test fails and that `cmp` of the page against the saved copy exits 1 (which proves the mutation changed the page), then restore the page by copying the saved file back and confirm `cmp` exits 0. At the end `sha256sum -c` against the recorded file passes and the Task 6 tests pass on the restored page. Never use a command that discards uncommitted changes on the page (`git checkout`, `git restore`, `git reset --hard`, `git stash`): the edits of Tasks 1 to 3 are not committed.

Acceptance criteria:
- `uv run pytest tests/docs/test_release_procedure.py -v` passes with every parametrized case present.
- `./artifacts/t6-mutation-check.md` lists at least one failing mutation per test function, the checksum before and after, and states that the page was restored by copy.
- `uv run pytest tests/docs/test_branch_protection_rulesets.py -v` still passes.


AC ids (source order):
T6.AC1 = `uv run pytest tests/docs/test_release_procedure.py -v` passes with every parametrized case present.
T6.AC2 = `./artifacts/t6-mutation-check.md` lists at least one failing mutation per test function, the checksum before and after, and states that the page was restored by copy.
T6.AC3 = `uv run pytest tests/docs/test_branch_protection_rulesets.py -v` still passes.
Global constraints: ## Constraints

- Edit under `src/superclaude/` first, never under `.claude/`; run `make sync-dev` then `make verify-sync`; never stage anything under `.claude/` or `.dev/issues/`.
- Documentation, skill text and two new tests only: no Python under `src/superclaude/cli/`, no edit to `.github/rulesets/` or `.github/workflows/`, no release script, no new `/sc:post-release` flag, no edit to `src/superclaude/commands/post-release.md`.
- Every `gh` command written into `docs/developer-guide/release-procedure.md` is on one line and carries `--repo IronbellyOrg/IronClaude` (or is `gh api repos/IronbellyOrg/IronClaude ...`). Installed primitives (the skill) name no `src/superclaude/` path and no literal branch name in the edited paragraph.
- No task creates a repository, pushes, tags, merges or opens a pull request on GitHub, with two exceptions that each need the owner's explicit approval in this session: the scratch-repository run of Task 13 and the one `gh issue comment` of Task 13. Read-only `gh api` GET calls on `IronbellyOrg/IronClaude` and read-only git checks of this repository stay allowed. The approval for the scratch repository must name it as the owner's exception to the project rule that the fork is the only target (`CLAUDE.md:49`, `CLAUDE.md:52`, `CLAUDE.md:76`); without that approval Task 13 records "not exercised".
- The headings `Step 1` to `Step 4`, `What a release is here` and `Sources` of the release page keep their text; the old Step 5 becomes Step 6 and a new Step 5 is added.
- No task of this plan commits. The delivery order applies to the story's commit step after the plan finishes: three commit groups, (1) `docs/developer-guide/release-procedure.md`, `CLAUDE.md`, `CONTRIBUTING.md` and `tests/docs/test_release_procedure.py`, (2) the skill text and `tests/skills/test_post_release_base_branch.py`, (3) the example commands; commit types `docs(release)` for (1) and (3) and `fix(post-release)` for (2); a last group (4) carries `.dev/tasks` (this package with its `./artifacts/` and the archived earlier plans) and `docs/memory/reflect/deviation-patterns-IronClaude.md`, has commit type `docs(dev)` and is committed last and alone; `.dev/reflect/`, `.dev/brainstorms/` and `.dev/issues/` are not committed; each group is committed with only its own paths so each can be reverted alone; `make sync-dev` and `make verify-sync` run after (2) and (3) (Task 11 runs them once at the end of the plan); the pull request body says when the rehearsal acceptance is only partly met.
- `./artifacts/` is the `artifacts` folder next to this plan. A command that reads or writes it runs with the package folder (the folder that holds this plan and `source.md`) as the working directory, in the same shell call; it reaches repository files through `"$(git rev-parse --show-toplevel)"`.
- Where this plan overrides the design: the H2 order of `test_contents_links_resolve` (design section 3.3, `source.md:150`) and the path of the local rehearsal log (design section 3.6, `source.md:186`) follow the "Revision 1" section of `./source.md`.

Start sha: 445925bde6f8d2774511ddbec01489c9e504ea99
Diff against the start snapshot: diff --git a/tests/docs/test_release_procedure.py b/tests/docs/test_release_procedure.py
new file mode 100644
index 000000000..139ee1c99
--- /dev/null
+++ b/tests/docs/test_release_procedure.py
@@ -0,0 +1,176 @@
+"""Pin the commands and structure of the release procedure page (issue 826)."""
+
+import re
+from pathlib import Path
+
+import pytest
+
+_REPO = Path(__file__).resolve().parents[2]
+_PAGE = _REPO / "docs" / "developer-guide" / "release-procedure.md"
+_TEXT = _PAGE.read_text(encoding="utf-8")
+
+_FORK = "--repo IronbellyOrg/IronClaude"
+_FORK_API = "gh api repos/IronbellyOrg/IronClaude"
+
+# One entry per command written in Steps 2 to 6 of the page. The two commands that the page also
+# states in prose (`make sync-dev`, the Step 2 ancestry check) are checked by
+# test_step2_has_its_own_commands, and `--verify-tag` by test_verify_tag_on_the_release_line.
+# A future step that adds a command adds a row here.
+_REQUIRED_COMMANDS = (
+    "/sc:pr-submit --monitor 3 --head <branch> --base integration",
+    "--base integration --head <branch>",
+    "gh pr create --repo IronbellyOrg/IronClaude --base master --head integration",
+    "gh pr checks <n> --repo IronbellyOrg/IronClaude --watch",
+    "git switch --detach <reviewed-head-sha>",
+    "gh pr merge <n> --repo IronbellyOrg/IronClaude --merge --match-head-commit <reviewed-head-sha>",
+    "--json state,baseRefName,headRefName,headRefOid,mergeCommit",
+    "git rev-parse --verify -q <merge-sha>^2",
+    "git rev-parse --verify -q <merge-sha>^3",
+    "git rev-parse <merge-sha>^{tree} <reviewed-head-sha>^{tree}",
+    "gh run list --repo IronbellyOrg/IronClaude --workflow Tests --event push --branch master"
+    " --commit <merge-sha> --json databaseId,status,conclusion",
+    "git ls-remote --tags origin vX.Y.Z",
+    "git ls-remote origin 'refs/tags/vX.Y.Z^{}'",
+    "git rev-parse vX.Y.Z^{commit}",
+    "gh pr create --repo IronbellyOrg/IronClaude --base integration --head master",
+    "gh pr merge <m> --repo IronbellyOrg/IronClaude --merge",
+    "git merge-base --is-ancestor <merge-sha> origin/integration",
+    "git switch -c post-release-vX.Y.Z origin/integration",
+    "/sc:post-release vX.Y.Z",
+    "gh pr view <n> --repo IronbellyOrg/IronClaude --json headRefOid --jq .headRefOid",
+    "git rev-parse origin/master",
+    "gh api repos/IronbellyOrg/IronClaude --jq",
+    "git rev-parse <merge-sha>^1 <merge-sha>^2",
+    "git tag --list vX.Y.Z",
+    "git tag -a vX.Y.Z <merge-sha>",
+    "git push origin vX.Y.Z",
+)
+
+_BANNED_MERGE_OPTIONS = ("--admin", "--auto", "--squash", "--rebase", "--delete-branch")
+
+
+def _fenced_lines(text=_TEXT):
+    """Stripped lines inside triple-backtick fences; a fence marker may be indented."""
+    inside = False
+    lines = []
+    for line in text.split("\n"):
+        stripped = line.strip()
+        if stripped.startswith("```"):
+            inside = not inside
+        elif inside:
+            lines.append(stripped)
+    return lines
+
+
+def _section(title_start):
+    """Page text from the H2 heading that starts with title_start up to the next H2 heading."""
+    out = []
+    inside_fence = False
+    found = False
+    for line in _TEXT.split("\n"):
+        if line.strip().startswith("```"):
+            inside_fence = not inside_fence
+        is_h2 = line.startswith("## ") and not inside_fence
+        if is_h2 and found:
+            break
+        if is_h2 and line[3:].startswith(title_start):
+            found = True
+        if found:
+            out.append(line)
+    assert found, f"no H2 heading starts with {title_start!r}"
+    return "\n".join(out)
+
+
+def _h2_headings():
+    inside_fence = False
+    headings = []
+    for line in _TEXT.split("\n"):
+        if line.strip().startswith("```"):
+            inside_fence = not inside_fence
+        elif line.startswith("## ") and not inside_fence:
+            headings.append(line[3:])
+    return headings
+
+
+def _slug(heading):
+    """GitHub anchor: lowercase, drop characters that are not word characters, spaces or hyphens."""
+    return re.sub(r"[^\w\s-]", "", heading.lower()).replace(" ", "-")
+
+
+@pytest.mark.parametrize("command", _REQUIRED_COMMANDS)
+def test_required_command_is_on_the_page(command):
+    assert command in _TEXT
+
+
+def test_step2_has_its_own_commands():
+    # Whole fenced lines inside Step 2 only: the release-notes item names `make sync-dev` in prose and
+    # Step 5 states the ancestry fact, so a substring test of the page or of the section text would
+    # still pass after the Step 2 line was deleted.
+    step2 = _fenced_lines(_section("Step 2"))
+    assert "make sync-dev" in step2
+    assert "git merge-base --is-ancestor origin/master origin/integration" in step2
+
+
+def test_verify_tag_on_the_release_line():
+    # The page also explains the flag in prose, so only the fenced release line counts.
+    release_lines = [
+        line for line in _fenced_lines() if line.startswith("gh release create")
+    ]
+    assert release_lines, "no fenced `gh release create` line"
+    for line in release_lines:
+        assert "--verify-tag" in line
+
+
+def test_every_gh_line_names_the_fork():
+    for line in _fenced_lines():
+        if line.startswith("gh "):
+            assert _FORK in line or line.startswith(_FORK_API), line
+
+
+def test_banned_merge_options():
+    for line in _fenced_lines():
+        for option in _BANNED_MERGE_OPTIONS:
+            assert option not in line, f"{option} in fenced line: {line}"
+    inside = False
+    for line in _TEXT.split("\n"):
+        if line.strip().startswith("```"):
+            inside = not inside
+            continue
+        if not inside and any(option in line for option in _BANNED_MERGE_OPTIONS):
+            assert "never" in line.lower(), line
+
+
+@pytest.mark.parametrize(
+    "removed",
+    [
+        "--base master --head <branch>",
+        "--limit 3",
+        "Every merge to `master` therefore reaches",
+    ],
+)
+def test_removed_text_is_gone(removed):
+    assert removed not in _TEXT
+
+
+def test_contents_links_resolve():
+    headings = _h2_headings()
+    slugs = [_slug(h) for h in headings]
+    contents = _section("Contents")
+    anchors = re.findall(r"\]\(#([^)]+)\)", contents)
+    assert len(anchors) == 8
+    for anchor in anchors:
+        assert anchor in slugs, anchor
+    expected = [
+        "Contents",
+        "What a release is here",
+        "Step 1",
+        "Step 2",
+        "Step 3",
+        "Step 4",
+        "Step 5",
+        "Step 6",
+        "Sources",
+    ]
+    assert len(headings) == len(expected), headings
+    for heading, start in zip(headings, expected):
+        assert heading.startswith(start), (heading, start)

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

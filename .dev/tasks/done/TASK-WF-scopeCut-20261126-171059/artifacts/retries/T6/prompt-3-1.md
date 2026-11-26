d3882935c4821173ac0f11327bd180eb9bb2e1bb
Review one task for spec compliance.

Task brief: ## Task 6: Write the operator page and its test

Depends on: Task 5

Create `docs/developer-guide/branch-protection-multi-repo.md` as in source.md sections 1, 2 and 4. It writes every command with the variables `OWNER` and `REPO`, and holds: the delivery boundary (what the script does and what the owner does); the order per repo (dry run, read it, check the release workflows for tag moves by hand, apply with the printed digest, comment the ids on issue 838); the canary rule (start with one low-risk repo; the activity source must show complete coverage there before other repos rely on it); the manual rollback commands and the saved before-state file; what each refusal means; the rule that the exit status of the hooks, keys and installations commands in the existing guide must be checked (a failure means unknown, never "0"); and the follow-ups of source.md section 5. It names no real private repo and no real org login. Create `tests/org_rulesets/test_page.py`.

Acceptance criteria:
- The page defines `OWNER` and `REPO` variables, and every `gh api` command in it uses `$OWNER` and `$REPO` or the placeholder `<org>`.
- The page mentions `--apply`, `--confirm`, the dry run, `-before.json`, the 90-day push check, the tag warning and the canary rule, and `test_page.py` asserts that the page states the canary must show complete activity coverage before other repos rely on it.
- The page names no real private repo. `test_page.py` reads the 17 names at test time from the untracked `.dev/issues/838/issue-summary.md` (the comma-separated names after "all with Clay admin:" in the paragraph that starts "Clay's answer for this story") and asserts none appears in the page, in `scripts/apply_org_rulesets.py` or in any file of `tests/org_rulesets/`; the test is skipped when that file does not exist, and the names are written in no tracked file.
- `uv run pytest tests/org_rulesets/ tests/docs/test_branch_protection_rulesets.py` passes, `uv run ruff check scripts/apply_org_rulesets.py tests/org_rulesets` and `uv run ruff format --check scripts/apply_org_rulesets.py tests/org_rulesets` report nothing.

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

Start sha: d3882935c4821173ac0f11327bd180eb9bb2e1bb
Diff against the start snapshot: diff --git a/docs/developer-guide/branch-protection-multi-repo.md b/docs/developer-guide/branch-protection-multi-repo.md
new file mode 100644
index 000000000..00f167730
--- /dev/null
+++ b/docs/developer-guide/branch-protection-multi-repo.md
@@ -0,0 +1,136 @@
+# Branch Protection for Other Repos
+
+How to put the rulesets of [Branch Protection](branch-protection.md) on another repo of an organization, one repo per run, with `scripts/apply_org_rulesets.py`. The script renders every branch ruleset from `.github/rulesets/protect-master.json` (the name and the ref are changed per branch) and the tag ruleset from `.github/rulesets/protect-release-tags.json`. It does not read `protect-integration.json`, so editing that file changes nothing the script applies. It checks the repo, prints what it would do, and only with `--apply --confirm <digest>` creates the rulesets and reads each one back.
+
+## What the script does, and what you do
+
+The script does, for the one repo you name:
+
+- reads the repo: whether it is archived, whether you have admin rights, its default branch, and whether `master` and `integration` exist;
+- runs the 90-day direct-push check on each branch it would protect (`integration` and `master` where they exist, and the default branch);
+- reports classic branch protection on those branches, the rulesets already present and the number of `v*` tags;
+- in a dry run (no `--apply`), prints all of that, the rulesets it would create in order, the digest of them, and the exact command to apply;
+- with `--apply --confirm <digest>`, saves the repo's before state to `<repo>-before.json` in the `--out` folder, then creates the rulesets in this order: the tag ruleset, `integration`, `master`, and the default branch if it has another name. It reads each one back after creating it.
+
+You do, by hand: choose the repo, read the dry run, check the release workflows, check hooks, keys and installed apps, run the apply, comment the result on the tracking issue (838), and roll back if needed. The script never posts a comment, never edits or deletes a ruleset, and never changes classic branch protection (it refuses a branch that has it). It refuses the public upstream organization and has no default organization: you always pass `--org`.
+
+A dry run changes nothing; every `--apply` run is a live write to the repo you name.
+
+## Variables
+
+Every command on this page uses these, so a command is never typed against a repo by accident:
+
+```bash
+OWNER=<org>      # the organization that owns the repo
+REPO=<repo>      # one repo per run
+OUT=<folder>     # outside any git checkout; receives <repo>-before.json
+```
+
+## Order for each repo
+
+1. **Set `OWNER`, `REPO` and `OUT`.** Never reuse an `OUT` folder that already holds the before-state file of this repo: the script refuses.
+2. **Check webhooks, deploy keys and installed apps.** Anything that pushes to a protected branch must use pull requests once the rulesets are on.
+
+   ```bash
+   gh api "repos/$OWNER/$REPO/hooks" --jq 'length'; echo "exit status: $?"
+   gh api "repos/$OWNER/$REPO/keys" --jq 'length'; echo "exit status: $?"
+   gh api --paginate "orgs/$OWNER/installations" --jq '.installations[] | [.app_slug, .permissions.contents] | @tsv'; echo "exit status: $?"
+   ```
+
+   Read the exit status of each. A command that failed (for example HTTP 403 or 404) means **unknown**, never "0": a missing answer is not an empty list. Resolve it before going on. The commands are the ones in [Branch Protection](branch-protection.md), with the repo and organization as variables.
+3. **Dry run.** Writes nothing:
+
+   ```bash
+   uv run python scripts/apply_org_rulesets.py --org "$OWNER" --repo "$REPO"
+   ```
+
+   Read all of it: the repo facts, the push check per branch (`pass`, `blocked` or `incomplete`, with how many direct pushes and how many events it looked at), the classic protection per branch, the rulesets already present, the number of `v*` tags, the rulesets it would create in order, any `would refuse --apply:` line, the digest, and the apply command. A dry run exits 0 when it printed a `digest:` line, and 69 when it could not plan the repo (`no plan: the repo could not be planned`).
+4. **Check the release workflows by hand.** The tag ruleset blocks moving and deleting `v*` tags, with no bypass. Open each workflow under `.github/workflows/` of the repo and look for a step that moves or deletes a `v*` tag (a force push of a tag, `git tag -f`, `git push --delete`, a release tool that recreates a tag). If one does, change it first, or do not apply to this repo yet: the script always creates the tag ruleset (it only skips one that already exists) and cannot tell what a workflow does. The dry run prints the same warning.
+5. **Apply**, with the digest the dry run printed:
+
+   ```bash
+   uv run python scripts/apply_org_rulesets.py --org "$OWNER" --repo "$REPO" --out "$OUT" --apply --confirm <digest>
+   ```
+
+   The script reads everything again (nothing carries over from the dry run) and refuses with `confirm digest does not match the rulesets rendered now` when the digest of the ruleset bodies it renders now is not the one you passed; rerun the dry run. On success it prints `before state saved:` with the file, one `created:` line per ruleset with its id, `skipped, already present:` for any ruleset whose name is already on the repo, the `comment for issue 838:` line, and the rollback commands under `rollback by hand`.
+6. **Check** (read-only):
+
+   ```bash
+   gh api "repos/$OWNER/$REPO/rulesets" --jq '.[] | [.id, .name, .enforcement] | @tsv'
+   gh api "repos/$OWNER/$REPO/rules/branches/<branch>" --jq '.[].type'
+   ```
+
+   Each branch must print `deletion`, `non_fast_forward` and `pull_request`. Do not test by pushing to, force pushing or deleting a real protected branch or tag.
+7. **Comment** the `comment for issue 838:` line (repo, date, ruleset ids by name) on issue 838. Keep the before-state file where you can find it.
+
+## The canary rule
+
+Start with one low-risk repo (few contributors, no release tags that workflows move). The canary must show complete activity coverage before other repos rely on it: every branch line of its dry run (`<branch>: <result> (source <source>, direct pushes N, examined N)`) must read `(source activity, ...)`, and no branch line and no `push check` line may read `incomplete`. If any branch reads `source commits` or `incomplete`, stop before a second repo and find out why.
+
+## The 90-day push check
+
+Per branch, with one cutoff for the whole run (now minus 90 days):
+
+- Primary source: the activity feed of the branch. A `push`, `force_push` or `branch_deletion` event inside the window is a direct push; a `pr_merge` is not.
+- Fallback to the commit list when the feed call fails, its answer cannot be read, or it runs past 10 pages.
+- In the fallback, a commit list that fails or runs past 10 pages gives `incomplete`. For each of the first 200 commits the script asks for the pull requests that contain it; a commit with no merged pull request into that branch is a direct push.
+- Any direct push found gives `blocked`. With none found, a failed pull-request lookup or more than 200 commits gives `incomplete`. Otherwise `pass`.
+- Overall: `blocked` if any branch is blocked, `pass` only when every branch passes, otherwise `incomplete`. `incomplete` is never turned into `pass`.
+
+A direct push by a named person is **not** excused here. If someone pushes to a protected branch on purpose, the repo stays blocked until that is settled with its owner (see the follow-ups).
+
+## Refusals
+
+`--apply` prints `refused:` and the texts below on stderr, joined by `; `, and exits 69. No ruleset was written and no file was created. A dry run prints the first ten rows as `would refuse --apply: <text>` lines.
+
+| Text | What it means |
+|---|---|
+| `repo is archived` | GitHub says the repo is archived |
+| `no admin permission on the repo` | Your login has no admin permission on it |
+| `repo has no default branch` | GitHub reports no default branch |
+| `repo cannot be read (HTTP n)` | GitHub did not return the repo (n is the HTTP status; check the name and your access) |
+| `a branch lookup failed` | The lookup of `master` or `integration` answered something other than found or not found |
+| `branch not supported: not a plain branch name: '<name>'` | The default branch name is empty, contains `*` or `~`, or starts with `refs/` |
+| `push check is blocked` or `push check is incomplete` | See the 90-day push check |
+| `classic branch protection on <branch>` or `branch protection state unknown on <branch>` | The branch has classic protection, or GitHub's answer could not be read. The script never edits it; decide by hand |
+| `ruleset list cannot be read (HTTP n)` | GitHub did not return the list of the repo's rulesets |
+| `repo lists a ruleset id this script never touches` | The repo lists a ruleset with an id that belongs to this project's own repository: this is not the repo you meant |
+| `no --out folder given` | `--apply` needs `--out` |
+| `confirm digest does not match the rulesets rendered now` | The digest is not the one for the rulesets rendered now; rerun the dry run and use its digest |
+| `before-state file already exists: <path>` | `<repo>-before.json` is already in the `--out` folder; use another folder or move the old file away on purpose |
+| `before-state read failed for ruleset <id>` | An existing ruleset could not be read to save it first, so nothing was written |
+
+Other messages:
+
+- Usage mistakes exit 64 with `usage error:` and one of `--repo takes exactly one repo name`, `--org: <reason>` (an empty name, or the upstream organization), `--confirm needs --apply`, `--apply needs --confirm DIGEST`, or an option error from the argument parser.
+- `refused: <text>` with some other text means the script's own allowlist blocked a call. That is a bug in the script; report it.
+- `failed: <text>` with a file error (for example an `--out` folder that cannot be created, or a rule file that cannot be read) exits 69.
+
+## Failures after the before-state file
+
+Once `<repo>-before.json` is written, a failed step prints `failed:` and one of these texts on stderr, prints what was written and the rollback commands, and exits 69:
+
+- `POST of <name> failed (HTTP n)`: GitHub refused the request, or its answer had no ruleset id.
+- `POST of <name> timed out and no ruleset of that name found`: the POST timed out, and the repo's rulesets, read straight afterwards, held none of that name. If one does hold it, the script adopts it and reads it back like any other. A POST is never repeated.
+- `read-back of <name> (id n) failed`: the ruleset just created could not be read.
+- `read-back of <name> (id n) differs: <differences>`: what GitHub returned is not what the script sent.
+
+If the first POST fails, only the before-state file was written and no rollback command is printed. If a later step fails, the rulesets created before it stay in place and their DELETE commands are printed; a read-back failure lists that ruleset's own id too. A ruleset whose name is already on the repo's list when the script applies is skipped (`skipped, already present:`) and never edited.
+
+## Roll back by hand
+
+The script has no rollback. After an apply, or a failed one, it prints one command per ruleset it created, newest first:
+
+```bash
+gh api --method DELETE "repos/$OWNER/$REPO/rulesets/<id>"
+```
+
+`<repo>-before.json` in `OUT` holds `org`, `repo`, `saved_at`, `digest`, the full body of every ruleset the repo had (each read by id), and `protection` with `none` for each branch of the set (a branch with classic protection is refused). The script never restores it; it is the record to restore from.
+
+## Not in this version (follow-ups)
+
+Dropped from the first plan to keep this small, to be decided and built later if they are wanted: a persistent file of target repos with a status per repo and one writer; owner statements and evidence (pushes accepted by the owner, tag statements and exceptions); a scan of workflows for tag mutation and handling of deleted tags; an automatic review of hooks, keys and installed apps (step 2 above is by hand); a rollback command; a check over all the repos that the rulesets are on; an allowlist file; a branch-only interim state; and seven owner decisions from the review of the larger plan.
+
+## Tests
+
+`tests/org_rulesets/` covers the script against a fake GitHub (no live call). `test_page.py` checks this page: its variables, its commands, that every message the script prints for a refusal or a failure is on it, and that it names no real private repo.
diff --git a/tests/org_rulesets/test_page.py b/tests/org_rulesets/test_page.py
new file mode 100644
index 000000000..8be276aa0
--- /dev/null
+++ b/tests/org_rulesets/test_page.py
@@ -0,0 +1,128 @@
+"""The operator page docs/developer-guide/branch-protection-multi-repo.md."""
+
+from __future__ import annotations
+
+import re
+import shlex
+from pathlib import Path
+
+import pytest
+
+ROOT = Path(__file__).resolve().parents[2]
+PAGE = ROOT / "docs" / "developer-guide" / "branch-protection-multi-repo.md"
+SUMMARY = ROOT / ".dev" / "issues" / "838" / "issue-summary.md"
+
+
+@pytest.fixture(scope="module")
+def page():
+    return PAGE.read_text(encoding="utf-8")
+
+
+def test_the_page_defines_the_variables(page):
+    assert re.search(r"^OWNER=", page, re.M) and re.search(r"^REPO=", page, re.M)
+    assert re.search(r"^OUT=", page, re.M)
+
+
+def test_every_gh_api_command_uses_the_variables_or_a_placeholder(page):
+    commands = [ln for ln in page.splitlines() if "gh api" in ln]
+    assert len(commands) >= 5
+    for line in commands:
+        assert "$OWNER" in line or "<org>" in line, line
+        if "repos/" in line:
+            assert "$REPO" in line or "<repo>" in line, line
+
+
+def test_the_page_says_what_the_operator_needs(page):
+    lowered = page.lower()
+    for needle in (
+        "--apply",
+        "--confirm",
+        "dry run",
+        "-before.json",
+        "90-day",
+        "blocks moving and deleting",
+        "canary",
+        "exit status",
+        'never "0"',
+    ):
+        assert needle in lowered, needle
+
+
+def test_the_canary_must_show_complete_activity_coverage(page):
+    flat = " ".join(page.split())
+    assert "complete activity coverage before other repos rely on it" in flat
+
+
+def test_the_script_commands_on_the_page_parse(orr, page):
+    """Every command line that runs the script uses real options."""
+    lines = [ln.strip() for ln in page.splitlines() if "apply_org_rulesets.py" in ln]
+    commands = [ln for ln in lines if ln.startswith("uv run python scripts/")]
+    assert len(commands) == 2
+    values = {"$OWNER": "acme", "$REPO": "acme-one", "$OUT": "/tmp/out"}
+    for line in commands:
+        words = shlex.split(line)[4:]
+        words = [values.get(w, w) for w in words]
+        words = ["0" * 64 if w == "<digest>" else w for w in words]
+        args = orr.parse_args(words)
+        assert (args.org, args.repo) == ("acme", "acme-one")
+
+
+def script_messages(orr):
+    """The refusal, failure and usage texts of the script, as written in its source."""
+    source = Path(orr.__file__).read_text(encoding="utf-8")
+    found = re.findall(
+        r'(?:problems\.append|stop|fail|UsageError)\(\s*f?"([^"]+)"', source
+    )
+    found += re.findall(r'return None, f"([^"]+)"', source)
+    found += list(orr._REFUSAL_TEXT.values())
+    return found
+
+
+def test_every_refusal_and_failure_text_of_the_script_is_on_the_page(orr, page):
+    flat = " ".join(page.split())
+    messages = script_messages(orr)
+    assert len(messages) >= 20
+    for message in messages:
+        parts = re.split(r"\{[^}]*\}", message.strip())
+        pattern = ".+?".join(re.escape(part) for part in parts)
+        assert re.search(pattern, flat), message
+
+
+def test_the_fixed_output_lines_of_the_script_are_on_the_page(page):
+    flat = " ".join(page.split())
+    for text in (
+        "no plan: the repo could not be planned",
+        "would refuse --apply:",
+        "refused:",
+        "failed:",
+        "usage error:",
+        "skipped, already present:",
+        "before state saved:",
+        "created:",
+        "comment for issue 838",
+        "rollback by hand",
+    ):
+        assert text in flat, text
+
+
+def private_repo_names():
+    text = SUMMARY.read_text(encoding="utf-8")
+    start = text.index("Clay's answer for this story")
+    found = re.search(r"all with Clay admin: (.+?)\. That list", text[start:])
+    return [name.strip() for name in found.group(1).split(",")]
+
+
+@pytest.mark.skipif(
+    not SUMMARY.exists(), reason="the untracked issue summary is absent"
+)
+def test_no_real_private_repo_name_is_written_in_a_tracked_file():
+    names = private_repo_names()
+    assert len(names) == 17
+    files = [PAGE, ROOT / "scripts" / "apply_org_rulesets.py"]
+    files += sorted(
+        p for p in (ROOT / "tests" / "org_rulesets").iterdir() if p.is_file()
+    )
+    for path in files:
+        text = path.read_text(encoding="utf-8", errors="ignore").lower()
+        for name in names:
+            assert name.lower() not in text, f"{name} in {path.name}"

Delta diff from the previous reviewed tree (empty on the first review): diff --git a/docs/developer-guide/branch-protection-multi-repo.md b/docs/developer-guide/branch-protection-multi-repo.md
index 3613fd5a0..00f167730 100644
--- a/docs/developer-guide/branch-protection-multi-repo.md
+++ b/docs/developer-guide/branch-protection-multi-repo.md
@@ -1,20 +1,20 @@
 # Branch Protection for Other Repos
 
-How to put the three rulesets of [Branch Protection](branch-protection.md) (`.github/rulesets/protect-master.json`, `protect-integration.json` and `protect-release-tags.json`) on another repo of an organization, one repo per run, with `scripts/apply_org_rulesets.py`. The script reads the rule files, checks the repo, prints what it would do, and only with `--apply --confirm <digest>` creates the rulesets and reads each one back.
+How to put the rulesets of [Branch Protection](branch-protection.md) on another repo of an organization, one repo per run, with `scripts/apply_org_rulesets.py`. The script renders every branch ruleset from `.github/rulesets/protect-master.json` (the name and the ref are changed per branch) and the tag ruleset from `.github/rulesets/protect-release-tags.json`. It does not read `protect-integration.json`, so editing that file changes nothing the script applies. It checks the repo, prints what it would do, and only with `--apply --confirm <digest>` creates the rulesets and reads each one back.
 
 ## What the script does, and what you do
 
 The script does, for the one repo you name:
 
-- reads the repo (archived? admin rights? default branch? are `master` and `integration` there?);
-- runs the 90-day direct-push check on each branch it would protect;
-- reports classic branch protection, rulesets already present and the number of `v*` tags;
-- in a dry run (no `--apply`), prints all of that, the rulesets it would create in order, a digest of them, and the exact command to apply;
-- with `--apply --confirm <digest>`, saves the repo's before state to `<repo>-before.json`, creates the rulesets (the tag ruleset, then `integration`, then `master`, then the default branch if it is another name), and reads each back before the next write.
+- reads the repo: whether it is archived, whether you have admin rights, its default branch, and whether `master` and `integration` exist;
+- runs the 90-day direct-push check on each branch it would protect (`integration` and `master` where they exist, and the default branch);
+- reports classic branch protection on those branches, the rulesets already present and the number of `v*` tags;
+- in a dry run (no `--apply`), prints all of that, the rulesets it would create in order, the digest of them, and the exact command to apply;
+- with `--apply --confirm <digest>`, saves the repo's before state to `<repo>-before.json` in the `--out` folder, then creates the rulesets in this order: the tag ruleset, `integration`, `master`, and the default branch if it has another name. It reads each one back after creating it.
 
-You do, by hand: choose the repo, read the dry run, check the release workflows, check hooks, keys and installed apps, run the apply, comment the result on the tracking issue (838), and roll back if needed. The script never posts a comment, never edits or deletes a ruleset and never touches classic branch protection. It refuses the public upstream organization and has no default organization: you always pass `--org`.
+You do, by hand: choose the repo, read the dry run, check the release workflows, check hooks, keys and installed apps, run the apply, comment the result on the tracking issue (838), and roll back if needed. The script never posts a comment, never edits or deletes a ruleset, and never changes classic branch protection (it refuses a branch that has it). It refuses the public upstream organization and has no default organization: you always pass `--org`.
 
-The script changes nothing by itself: every `--apply` run is a live write to the repo you name.
+A dry run changes nothing; every `--apply` run is a live write to the repo you name.
 
 ## Variables
 
@@ -28,7 +28,7 @@ OUT=<folder>     # outside any git checkout; receives <repo>-before.json
 
 ## Order for each repo
 
-1. **Set `OWNER`, `REPO` and `OUT`.** Never reuse an `OUT` folder for a repo whose before-state file is already in it: the script refuses.
+1. **Set `OWNER`, `REPO` and `OUT`.** Never reuse an `OUT` folder that already holds the before-state file of this repo: the script refuses.
 2. **Check webhooks, deploy keys and installed apps.** Anything that pushes to a protected branch must use pull requests once the rulesets are on.
 
    ```bash
@@ -44,7 +44,7 @@ OUT=<folder>     # outside any git checkout; receives <repo>-before.json
    uv run python scripts/apply_org_rulesets.py --org "$OWNER" --repo "$REPO"
    ```
 
-   Read all of it: the repo facts, the push check per branch (`pass`, `blocked` or `incomplete`, with how many direct pushes and how many events it looked at), the classic protection per branch, the rulesets already present, the number of `v*` tags, the rulesets it would create in order, any `would refuse --apply:` line, the digest, and the apply command. A dry run exits 0 when it could plan the repo and 69 when it could not (for example the repo cannot be read).
+   Read all of it: the repo facts, the push check per branch (`pass`, `blocked` or `incomplete`, with how many direct pushes and how many events it looked at), the classic protection per branch, the rulesets already present, the number of `v*` tags, the rulesets it would create in order, any `would refuse --apply:` line, the digest, and the apply command. A dry run exits 0 when it printed a `digest:` line, and 69 when it could not plan the repo (`no plan: the repo could not be planned`).
 4. **Check the release workflows by hand.** The tag ruleset blocks moving and deleting `v*` tags, with no bypass. Open each workflow under `.github/workflows/` of the repo and look for a step that moves or deletes a `v*` tag (a force push of a tag, `git tag -f`, `git push --delete`, a release tool that recreates a tag). If one does, change it first, or do not apply to this repo yet: the script always creates the tag ruleset (it only skips one that already exists) and cannot tell what a workflow does. The dry run prints the same warning.
 5. **Apply**, with the digest the dry run printed:
 
@@ -52,7 +52,7 @@ OUT=<folder>     # outside any git checkout; receives <repo>-before.json
    uv run python scripts/apply_org_rulesets.py --org "$OWNER" --repo "$REPO" --out "$OUT" --apply --confirm <digest>
    ```
 
-   The script reads the repo again before it writes and recomputes the digest of the rendered rule bodies, so a changed rule file or a changed branch set (the default branch, or `master` or `integration` appearing or going away) makes the digest differ and the run refuses. A new direct push, new classic protection or a new ruleset does not change the digest; the script re-reads those and refuses on its own. It prints the path of the before-state file, `created:` lines with the ids, the comment line for issue 838 and the rollback commands.
+   The script reads everything again (nothing carries over from the dry run) and refuses with `confirm digest does not match the rulesets rendered now` when the digest of the ruleset bodies it renders now is not the one you passed; rerun the dry run. On success it prints `before state saved:` with the file, one `created:` line per ruleset with its id, `skipped, already present:` for any ruleset whose name is already on the repo, the `comment for issue 838:` line, and the rollback commands under `rollback by hand`.
 6. **Check** (read-only):
 
    ```bash
@@ -61,49 +61,71 @@ OUT=<folder>     # outside any git checkout; receives <repo>-before.json
    ```
 
    Each branch must print `deletion`, `non_fast_forward` and `pull_request`. Do not test by pushing to, force pushing or deleting a real protected branch or tag.
-7. **Comment** the line the script printed (repo, date, ruleset ids by name) on issue 838. Save the before-state file where you can find it.
+7. **Comment** the `comment for issue 838:` line (repo, date, ruleset ids by name) on issue 838. Keep the before-state file where you can find it.
 
 ## The canary rule
 
-Start with one low-risk repo (few contributors, no release tags that workflows move). The 90-day check normally reads GitHub's activity feed. The canary must show complete activity coverage before other repos rely on it: its dry run must end with `source activity` on every branch and no `incomplete`, and the push count it reports must match what you can see in the repo's history. If the canary falls back to the commit list, or answers `incomplete`, stop and find out why before doing a second repo.
+Start with one low-risk repo (few contributors, no release tags that workflows move). The canary must show complete activity coverage before other repos rely on it: every branch line of its dry run (`<branch>: <result> (source <source>, direct pushes N, examined N)`) must read `(source activity, ...)`, and no branch line and no `push check` line may read `incomplete`. If any branch reads `source commits` or `incomplete`, stop before a second repo and find out why.
 
 ## The 90-day push check
 
-Per branch, over the last 90 days (one cutoff for the whole run):
+Per branch, with one cutoff for the whole run (now minus 90 days):
 
-- Primary source: the activity feed of the branch. A `push`, `force_push` or `branch_deletion` is a direct push; a `pr_merge` is not.
-- Fallback, when the feed is unavailable (HTTP 403 or 404) or runs past 10 pages: the commit list since the cutoff, and for each commit whether a merged pull request contains it. A commit with none is a direct push. More than 200 commits on one branch gives `incomplete`.
-- `pass` only with zero direct pushes on every branch. `blocked` for any direct push. `incomplete` when no source gave a full answer; it is never turned into `pass`.
+- Primary source: the activity feed of the branch. A `push`, `force_push` or `branch_deletion` event inside the window is a direct push; a `pr_merge` is not.
+- Fallback to the commit list when the feed call fails, its answer cannot be read, or it runs past 10 pages.
+- In the fallback, a commit list that fails or runs past 10 pages gives `incomplete`. For each of the first 200 commits the script asks for the pull requests that contain it; a commit with no merged pull request into that branch is a direct push.
+- Any direct push found gives `blocked`. With none found, a failed pull-request lookup or more than 200 commits gives `incomplete`. Otherwise `pass`.
+- Overall: `blocked` if any branch is blocked, `pass` only when every branch passes, otherwise `incomplete`. `incomplete` is never turned into `pass`.
 
-A direct push by a named person is **not** excused here. If someone pushes to `master` on purpose, the repo stays blocked until that is settled with its owner (see the follow-ups).
+A direct push by a named person is **not** excused here. If someone pushes to a protected branch on purpose, the repo stays blocked until that is settled with its owner (see the follow-ups).
 
 ## Refusals
 
-`--apply` makes no write and writes no file when any of these holds. The text is printed on stderr after `refused:` and the exit status is 69.
+`--apply` prints `refused:` and the texts below on stderr, joined by `; `, and exits 69. No ruleset was written and no file was created. A dry run prints the first ten rows as `would refuse --apply: <text>` lines.
 
-| Text | Meaning |
+| Text | What it means |
 |---|---|
-| `repo is archived`, `no admin permission on the repo`, `repo has no default branch` | The repo cannot take rulesets from you |
-| `repo cannot be read (HTTP n)`, `a branch lookup failed`, `ruleset list cannot be read (HTTP n)` | GitHub did not answer a read; fix access and rerun |
+| `repo is archived` | GitHub says the repo is archived |
+| `no admin permission on the repo` | Your login has no admin permission on it |
+| `repo has no default branch` | GitHub reports no default branch |
+| `repo cannot be read (HTTP n)` | GitHub did not return the repo (n is the HTTP status; check the name and your access) |
+| `a branch lookup failed` | The lookup of `master` or `integration` answered something other than found or not found |
+| `branch not supported: not a plain branch name: '<name>'` | The default branch name is empty, contains `*` or `~`, or starts with `refs/` |
 | `push check is blocked` or `push check is incomplete` | See the 90-day push check |
-| `classic branch protection on <branch>` or `branch protection state unknown on <branch>` | The branch already has classic protection (or the answer failed). The script never edits it; decide by hand |
-| `repo lists a ruleset id this script never touches` | The repo holds one of the three ruleset ids of the source repo; this is not the repo you meant |
-| `confirm digest does not match the rulesets rendered now` | The digest is not the one the dry run printed for the current rule files and branch set; rerun the dry run |
-| `before-state file already exists` | Rerun with another `OUT`, or move the old file away on purpose |
-| `before-state read failed for ruleset <id>` | The existing rulesets could not be saved first, so nothing was written |
+| `classic branch protection on <branch>` or `branch protection state unknown on <branch>` | The branch has classic protection, or GitHub's answer could not be read. The script never edits it; decide by hand |
+| `ruleset list cannot be read (HTTP n)` | GitHub did not return the list of the repo's rulesets |
+| `repo lists a ruleset id this script never touches` | The repo lists a ruleset with an id that belongs to this project's own repository: this is not the repo you meant |
 | `no --out folder given` | `--apply` needs `--out` |
+| `confirm digest does not match the rulesets rendered now` | The digest is not the one for the rulesets rendered now; rerun the dry run and use its digest |
+| `before-state file already exists: <path>` | `<repo>-before.json` is already in the `--out` folder; use another folder or move the old file away on purpose |
+| `before-state read failed for ruleset <id>` | An existing ruleset could not be read to save it first, so nothing was written |
 
-A ruleset of the same name that already exists is skipped with a printed line; it is never edited. A failed step after a write (`POST of <name> failed`, `POST of <name> timed out and no ruleset of that name found`, `read-back of <name> (id n) differs`) stops the run, prints what was written and the rollback commands, and exits 69 with `failed:` on stderr. A POST that timed out is followed by a list of the repo's rulesets; the ruleset is adopted if it exists, and a POST is never repeated. A usage mistake exits 64. If GitHub itself refuses the POST (for example HTTP 403 because the plan does not allow rulesets on that repo), the run stops after the before-state file; nothing else was written.
+Other messages:
+
+- Usage mistakes exit 64 with `usage error:` and one of `--repo takes exactly one repo name`, `--org: <reason>` (an empty name, or the upstream organization), `--confirm needs --apply`, `--apply needs --confirm DIGEST`, or an option error from the argument parser.
+- `refused: <text>` with some other text means the script's own allowlist blocked a call. That is a bug in the script; report it.
+- `failed: <text>` with a file error (for example an `--out` folder that cannot be created, or a rule file that cannot be read) exits 69.
+
+## Failures after the before-state file
+
+Once `<repo>-before.json` is written, a failed step prints `failed:` and one of these texts on stderr, prints what was written and the rollback commands, and exits 69:
+
+- `POST of <name> failed (HTTP n)`: GitHub refused the request, or its answer had no ruleset id.
+- `POST of <name> timed out and no ruleset of that name found`: the POST timed out, and the repo's rulesets, read straight afterwards, held none of that name. If one does hold it, the script adopts it and reads it back like any other. A POST is never repeated.
+- `read-back of <name> (id n) failed`: the ruleset just created could not be read.
+- `read-back of <name> (id n) differs: <differences>`: what GitHub returned is not what the script sent.
+
+If the first POST fails, only the before-state file was written and no rollback command is printed. If a later step fails, the rulesets created before it stay in place and their DELETE commands are printed; a read-back failure lists that ruleset's own id too. A ruleset whose name is already on the repo's list when the script applies is skipped (`skipped, already present:`) and never edited.
 
 ## Roll back by hand
 
-The script has no rollback. It prints, after an apply (or a failed one), one command per ruleset it created, newest first:
+The script has no rollback. After an apply, or a failed one, it prints one command per ruleset it created, newest first:
 
 ```bash
 gh api --method DELETE "repos/$OWNER/$REPO/rulesets/<id>"
 ```
 
-`<repo>-before.json` in `OUT` holds what the repo had before: the full body of every existing ruleset and the classic protection per branch (`none` when there was none). It is the record to restore from; the script does not restore it.
+`<repo>-before.json` in `OUT` holds `org`, `repo`, `saved_at`, `digest`, the full body of every ruleset the repo had (each read by id), and `protection` with `none` for each branch of the set (a branch with classic protection is refused). The script never restores it; it is the record to restore from.
 
 ## Not in this version (follow-ups)
 
@@ -111,4 +133,4 @@ Dropped from the first plan to keep this small, to be decided and built later if
 
 ## Tests
 
-`tests/org_rulesets/` covers the script against a fake GitHub (no live call). `test_page.py` checks this page: its variables, its commands and that it names no real private repo.
+`tests/org_rulesets/` covers the script against a fake GitHub (no live call). `test_page.py` checks this page: its variables, its commands, that every message the script prints for a refusal or a failure is on it, and that it names no real private repo.
diff --git a/tests/org_rulesets/test_page.py b/tests/org_rulesets/test_page.py
index 06ffdc24e..8be276aa0 100644
--- a/tests/org_rulesets/test_page.py
+++ b/tests/org_rulesets/test_page.py
@@ -67,6 +67,44 @@ def test_the_script_commands_on_the_page_parse(orr, page):
         assert (args.org, args.repo) == ("acme", "acme-one")
 
 
+def script_messages(orr):
+    """The refusal, failure and usage texts of the script, as written in its source."""
+    source = Path(orr.__file__).read_text(encoding="utf-8")
+    found = re.findall(
+        r'(?:problems\.append|stop|fail|UsageError)\(\s*f?"([^"]+)"', source
+    )
+    found += re.findall(r'return None, f"([^"]+)"', source)
+    found += list(orr._REFUSAL_TEXT.values())
+    return found
+
+
+def test_every_refusal_and_failure_text_of_the_script_is_on_the_page(orr, page):
+    flat = " ".join(page.split())
+    messages = script_messages(orr)
+    assert len(messages) >= 20
+    for message in messages:
+        parts = re.split(r"\{[^}]*\}", message.strip())
+        pattern = ".+?".join(re.escape(part) for part in parts)
+        assert re.search(pattern, flat), message
+
+
+def test_the_fixed_output_lines_of_the_script_are_on_the_page(page):
+    flat = " ".join(page.split())
+    for text in (
+        "no plan: the repo could not be planned",
+        "would refuse --apply:",
+        "refused:",
+        "failed:",
+        "usage error:",
+        "skipped, already present:",
+        "before state saved:",
+        "created:",
+        "comment for issue 838",
+        "rollback by hand",
+    ):
+        assert text in flat, text
+
+
 def private_repo_names():
     text = SUMMARY.read_text(encoding="utf-8")
     start = text.index("Clay's answer for this story")
@@ -81,8 +119,10 @@ def test_no_real_private_repo_name_is_written_in_a_tracked_file():
     names = private_repo_names()
     assert len(names) == 17
     files = [PAGE, ROOT / "scripts" / "apply_org_rulesets.py"]
-    files += sorted((ROOT / "tests" / "org_rulesets").glob("*.py"))
+    files += sorted(
+        p for p in (ROOT / "tests" / "org_rulesets").iterdir() if p.is_file()
+    )
     for path in files:
-        text = path.read_text(encoding="utf-8").lower()
+        text = path.read_text(encoding="utf-8", errors="ignore").lower()
         for name in names:
             assert name.lower() not in text, f"{name} in {path.name}"

Earlier blocking findings of this start (empty on the first review): F1.2 sev=blocking trigger=B2 ac=scope at=docs/developer-guide/branch-protection-multi-repo.md:55 anchor=scripts/apply_org_rulesets.py:105-107 `payload_digest` hashes only the rendered bodies chk=n,y,n,n family=page-digest-overclaim fix=say the digest covers only the rendered rule bodies (rule files and branch set) and that the push check, classic protection and existing rulesets are re-read and refuse on their own; make the table row say the same first=A1 origin=new: lines 55 and 91 say a changed repo changes the digest, but a new direct push or an existing ruleset does not.
F2.1 sev=blocking trigger=B2 ac=scope at=docs/developer-guide/branch-protection-multi-repo.md:55 anchor=scripts/apply_org_rulesets.py:781-783 `if rname in existing["rulesets"]: result["skipped"].append(rname)` chk=n,y,n,n family=page-digest-overclaim fix=say a ruleset of the same name that appears later is skipped and recorded in the before state, and that the script refuses only on a protected ruleset id or an unreadable list: the page says "a new ruleset ... the script re-reads those and refuses on its own", but a same-name ruleset is skipped, not refused. first=A2 origin=fix-induced
F2.2 sev=blocking trigger=B2 ac=scope at=docs/developer-guide/branch-protection-multi-repo.md:55 anchor=scripts/apply_org_rulesets.py:35-36,74 `BRANCH_RULES_FILE = "protect-master.json"` / `body = _load(BRANCH_RULES_FILE)` chk=n,y,n,n family=page-digest-overclaim fix=say the script reads only `protect-master.json` and `protect-release-tags.json`, renders the integration ruleset from the master file, and never reads `protect-integration.json`, so editing it changes neither the digest nor what is applied; fix line 3, line 55 and line 91 to match: the page says a "changed rule file" changes the digest and line 3 lists `protect-integration.json` as a file the script reads. first=A1 origin=late
F2.3 sev=blocking trigger=B2 ac=scope at=docs/developer-guide/branch-protection-multi-repo.md:96 anchor=scripts/apply_org_rulesets.py:779-796 (a failed POST after earlier created ids returns `fail(...)`, which lists them for rollback) chk=n,y,n,n family=page-failure-overclaim fix=say that "nothing else was written" holds only when the first POST is the one refused, and that a refusal on a later POST leaves the earlier rulesets in place with their rollback commands: the page says "If GitHub itself refuses the POST ... nothing else was written", but the same paragraph says a failed step prints what was written. first=A1 origin=late
F2.4 sev=blocking trigger=B4 ac=scope at=docs/developer-guide/branch-protection-multi-repo.md:84-94 anchor="what each refusal means" (task brief, Task 6) chk=y,n,n,y family=page-refusals-incomplete fix=add a table row for `branch not supported: not a plain branch name: ...` (scripts/apply_org_rulesets.py:591, the default branch name is empty, contains `*` or `~`, or starts with `refs/`) and name `read-back of <name> (id n) failed` (scripts/apply_org_rulesets.py:800) beside the differs case at line 96: neither text is on the page. first=A1 origin=late
F2.5 sev=blocking trigger=B2 ac=scope at=docs/developer-guide/branch-protection-multi-repo.md:75 anchor=scripts/apply_org_rulesets.py:484-488 `if out["direct_pushes"]: return {**out, "result": "blocked"}` chk=n,y,n,n family=page-push-check-imprecise fix=say more than 200 commits gives `incomplete` only when none of the first 200 is a direct push (a direct push found gives `blocked`), a failed pull-request lookup also gives `incomplete`, and the feed fallback covers any failed or malformed feed answer, not only 403 and 404 (scripts/apply_org_rulesets.py:426-435): the page says "More than 200 commits on one branch gives `incomplete`". first=A1 origin=late
F2.6 sev=blocking trigger=B2 ac=scope at=docs/developer-guide/branch-protection-multi-repo.md:68 anchor=scripts/apply_org_rulesets.py:637-640 `f"  {branch}: {got['result']} (source {got['source']}, "` chk=n,y,n,n family=page-recipe-imprecise fix=replace "its dry run must end with `source activity` on every branch" with "each branch line of its dry run must read `(source activity, ...)` with no `incomplete`": the dry run ends with the digest and apply lines, and the `source` text sits inside each branch line. first=A1 origin=late

Saved-probe re-check hit locations (may be empty): --- fam1
48:4. **Check the release workflows by hand.** The tag ruleset blocks moving and deleting `v*` tags, with no b
55:   The script reads everything again (nothing carries over from the dry run) and refuses with `confirm dige
105:- Usage mistakes exit 64 with `usage error:` and one of `--repo takes exactly one repo name`, `--org: <rea
118:If the first POST fails, only the before-state file was written and no rollback command is printed. If a l
--- fam2
3:How to put the rulesets of [Branch Protection](branch-protection.md) on another repo of an organization, one
12:- in a dry run (no `--apply`), prints all of that, the rulesets it would create in order, the digest of the
13:- with `--apply --confirm <digest>`, saves the repo's before state to `<repo>-before.json` in the `--out` f
47:   Read all of it: the repo facts, the push check per branch (`pass`, `blocked` or `incomplete`, with how m
49:5. **Apply**, with the digest the dry run printed:
52:   uv run python scripts/apply_org_rulesets.py --org "$OWNER" --repo "$REPO" --out "$OUT" --apply --confirm
55:   The script reads everything again (nothing carries over from the dry run) and refuses with `confirm dige
99:| `confirm digest does not match the rulesets rendered now` | The digest is not the one for the rulesets re
105:- Usage mistakes exit 64 with `usage error:` and one of `--repo takes exactly one repo name`, `--org: <rea
128:`<repo>-before.json` in `OUT` holds `org`, `repo`, `saved_at`, `digest`, the full body of every ruleset th


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

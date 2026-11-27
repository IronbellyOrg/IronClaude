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
index 000000000..7ee7dede4
--- /dev/null
+++ b/docs/developer-guide/branch-protection-multi-repo.md
@@ -0,0 +1,122 @@
+# Branch Protection for Other Repos
+
+How to put the rulesets of [Branch Protection](branch-protection.md) on another repo of an organization, one repo per run, with `scripts/apply_org_rulesets.py`. Without `--apply` it is a dry run that writes nothing; `--apply --confirm <digest>` creates the rulesets and reads each one back.
+
+## What the script does, and what you do
+
+The script checks one repo and prints a dry run that writes nothing. With `--apply --confirm <digest>` and `--out` it saves `<repo>-before.json` and creates the listed rulesets that are not already present, reading each back. It never posts the comment, never edits or deletes a ruleset, never changes classic branch protection, refuses the upstream organization and has no default `--org`.
+
+You choose the repo, read the dry run, check the release workflows, hooks, keys and installed apps, run the apply, comment on issue 838 and roll back if needed. A dry run changes nothing; every `--apply` run is a live write to the repo you name.
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
+1. **Set `OWNER`, `REPO` and `OUT`.**
+2. **Check webhooks, deploy keys and installed apps.** Anything that pushes to a protected branch must use pull requests once the rulesets are on.
+
+   ```bash
+   gh api "repos/$OWNER/$REPO/hooks" --jq 'length'; echo "exit status: $?"
+   gh api "repos/$OWNER/$REPO/keys" --jq 'length'; echo "exit status: $?"
+   gh api --paginate "orgs/$OWNER/installations" --jq '.installations[] | [.app_slug, .permissions.contents] | @tsv'; echo "exit status: $?"
+   ```
+
+   Read the exit status of each. A command that failed (for example HTTP 403 or 404) means **unknown**, never "0": a missing answer is not an empty list. Resolve it before going on. Read the results as in [Branch Protection](branch-protection.md).
+3. **Dry run.** Writes nothing:
+
+   ```bash
+   uv run python scripts/apply_org_rulesets.py --org "$OWNER" --repo "$REPO"
+   ```
+
+   Read every line of it and resolve each `would refuse --apply:` line. A dry run that cannot plan the repo prints `no plan: the repo could not be planned`.
+4. **Check the release workflows by hand.** The dry run prints `WARNING: the tag ruleset blocks moving and deleting v* tags; check the release workflows of this repo by hand before applying.` Open each workflow under `.github/workflows/` of the repo and look for a step that moves or deletes a `v*` tag (a force push of a tag, `git tag -f`, `git push --delete`). If there is one, change it first or do not apply to this repo yet.
+5. **Apply**, with the digest the dry run printed:
+
+   ```bash
+   uv run python scripts/apply_org_rulesets.py --org "$OWNER" --repo "$REPO" --out "$OUT" --apply --confirm <digest>
+   ```
+
+   A digest that is not the one the dry run printed gives `confirm digest does not match the rulesets rendered now`; rerun the dry run. The output has `before state saved:`, one `created:` line per ruleset it created, `skipped, already present:` for a ruleset it skipped, `comment for issue 838:` and, under `rollback by hand`, the rollback commands.
+6. **Check** (read-only):
+
+   ```bash
+   gh api "repos/$OWNER/$REPO/rulesets" --jq '.[] | [.id, .name, .enforcement] | @tsv'
+   gh api "repos/$OWNER/$REPO/rules/branches/<branch>" --jq '.[].type'
+   ```
+
+   Each branch must print `deletion`, `non_fast_forward` and `pull_request`. Do not test by pushing to, force pushing or deleting a real protected branch or tag.
+7. **Comment** the `comment for issue 838:` line on issue 838. Keep the before-state file where you can find it.
+
+## The canary rule
+
+Start with one low-risk repo. The canary must show complete activity coverage before other repos rely on it: every branch line of its dry run reads `(source activity, ...)` and none reads `incomplete`. If any branch line reads `source commits` or `incomplete`, stop before a second repo.
+
+## The 90-day push check
+
+- Each branch ends `pass`, `blocked` or `incomplete`, and the dry run prints the overall result with the same three words.
+- `incomplete` is never turned into `pass`.
+- Each branch line names its source: `source activity` or `source commits`.
+- A direct push by a named person is not excused: the check reports `blocked` for it.
+
+## Refusals and failures
+
+An `--apply` that refuses prints `refused:` and the texts below, joined by `; `, on stderr.
+
+| Text | What you do |
+|---|---|
+| `repo is archived` | Do not apply to this repo |
+| `no admin permission on the repo` | Get admin permission on the repo, then rerun the dry run |
+| `repo has no default branch` | Do not apply to this repo |
+| `repo cannot be read (HTTP <n>)` | Check the name and your access with `gh api "repos/$OWNER/$REPO"`, then rerun the dry run |
+| `a branch lookup failed` | Rerun the dry run; if it repeats, check your access |
+| `branch not supported: <reason>` | Do this repo by hand |
+| `push check is <result>` | Do not apply; read the push check lines of the dry run |
+| `classic branch protection on <branch>` | Do not apply; decide by hand with the repo owner |
+| `branch protection state unknown on <branch>` | Rerun the dry run; if it repeats, decide by hand |
+| `ruleset list cannot be read (HTTP <n>)` | Check your access, then rerun the dry run |
+| `repo lists a ruleset id this script never touches` | Stop: the ids 28081842, 28081844 and 28081845 are never touched, so this is probably not the repo you meant |
+| `no --out folder given` | Add `--out "$OUT"` |
+| `confirm digest does not match the rulesets rendered now` | Rerun the dry run and use the digest it prints |
+| `before-state file already exists: <path>` | Use another `OUT` folder, or move the old file away on purpose |
+| `before-state read failed for ruleset <id>` | Check your access, then rerun the dry run |
+
+A usage mistake prints one of these and exits 64: fix the command line.
+
+- `usage error:`
+- `--repo takes exactly one repo name`
+- `--org: <reason>`
+- `--confirm needs --apply`
+- `--apply needs --confirm DIGEST`
+
+Any other `refused: <text>` or `failed: <text>`: stop and report it.
+
+After the before-state file is saved, a failed step prints `failed:` and one of these on stderr:
+
+- `POST of <name> failed (HTTP <n>)`
+- `POST of <name> timed out and no ruleset of that name found`
+- `read-back of <name> (id <n>) failed`
+- `read-back of <name> (id <n>) differs: <differences>`
+
+After any `failed:` line, or any non-zero exit of an `--apply` run, first list the repo's rulesets by hand with the check command in step 6. Compare that list with the printed `created:` lines and the `rollback by hand` commands: a ruleset can exist that no printed line names. Only then decide on a rollback. A rerun into the same `OUT` refuses with `before-state file already exists: <path>`.
+
+## Roll back by hand
+
+The script has no rollback. Run the commands it printed under `rollback by hand`, or, for an id you found by listing the rulesets:
+
+```bash
+gh api --method DELETE "repos/$OWNER/$REPO/rulesets/<id>"
+```
+
+`<repo>-before.json` in `OUT` holds the keys `org`, `repo`, `saved_at`, `digest`, `rulesets` and `protection`. It is the record to restore from by hand; the script never reads it back.
+
+## Not in this version (follow-ups)
+
+Dropped from the first plan to keep this small, to be decided and built later if they are wanted: a persistent file of target repos with a status per repo and one writer; owner statements and evidence (pushes accepted by the owner, tag statements and exceptions); a scan of workflows for tag mutation and handling of deleted tags; an automatic review of hooks, keys and installed apps (step 2 above is by hand); a rollback command; a check over all the repos that the rulesets are on; an allowlist file; a branch-only interim state; and seven owner decisions from the review of the larger plan.
diff --git a/tests/org_rulesets/test_page.py b/tests/org_rulesets/test_page.py
new file mode 100644
index 000000000..89f55e70b
--- /dev/null
+++ b/tests/org_rulesets/test_page.py
@@ -0,0 +1,150 @@
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
+def test_every_text_quoted_in_the_message_lists_is_in_the_script(orr, page):
+    """The other direction: the first span of each table row and bullet between
+    'Refusals and failures' and 'Roll back by hand' is a script string once the
+    placeholders in angle brackets are cut out."""
+    start = page.index("## Refusals and failures")
+    end = page.index("## Roll back by hand")
+    source = Path(orr.__file__).read_text(encoding="utf-8")
+    spans = []
+    for line in page[start:end].splitlines():
+        found = re.match(r"^(?:\| |- )`([^`]+)`", line)
+        if found and found.group(1) != "Text":
+            spans.append(found.group(1))
+    assert len(spans) >= 20
+    for span in spans:
+        for piece in re.split(r"<[^>]*>", span):
+            piece = piece.strip()
+            if len(piece) > 2:
+                assert piece in source, (
+                    f"{piece!r} (from {span!r}) is not in the script"
+                )
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
index 62f3a0938..7ee7dede4 100644
--- a/docs/developer-guide/branch-protection-multi-repo.md
+++ b/docs/developer-guide/branch-protection-multi-repo.md
@@ -1,20 +1,12 @@
 # Branch Protection for Other Repos
 
-How to put the rulesets of [Branch Protection](branch-protection.md) on another repo of an organization, one repo per run, with `scripts/apply_org_rulesets.py`. The script renders every branch ruleset from `.github/rulesets/protect-master.json` (the name and the ref are changed per branch) and the tag ruleset from `.github/rulesets/protect-release-tags.json`. It does not read `protect-integration.json`, so editing that file changes nothing the script applies. It checks the repo, prints what it would do, and only with `--apply --confirm <digest>` creates the rulesets and reads each one back.
+How to put the rulesets of [Branch Protection](branch-protection.md) on another repo of an organization, one repo per run, with `scripts/apply_org_rulesets.py`. Without `--apply` it is a dry run that writes nothing; `--apply --confirm <digest>` creates the rulesets and reads each one back.
 
 ## What the script does, and what you do
 
-The script does, for the one repo you name:
+The script checks one repo and prints a dry run that writes nothing. With `--apply --confirm <digest>` and `--out` it saves `<repo>-before.json` and creates the listed rulesets that are not already present, reading each back. It never posts the comment, never edits or deletes a ruleset, never changes classic branch protection, refuses the upstream organization and has no default `--org`.
 
-- reads the repo: whether it is archived, whether you have admin rights, its default branch, and whether `master` and `integration` exist;
-- runs the 90-day direct-push check on each branch it would protect (`integration` and `master` where they exist, and the default branch);
-- reports classic branch protection on those branches, the rulesets already present and the number of `v*` tags;
-- in a dry run (no `--apply`), prints all of that, the rulesets it would create in order, the digest of them, and the exact command to apply;
-- with `--apply --confirm <digest>`, saves the repo's before state to `<repo>-before.json` in the `--out` folder, then creates the rulesets in this order: the tag ruleset, `integration`, `master`, and the default branch if it has another name. It reads each one back after creating it.
-
-You do, by hand: choose the repo, read the dry run, check the release workflows, check hooks, keys and installed apps, run the apply, comment the result on the tracking issue (838), and roll back if needed. The script never posts a comment, never edits or deletes a ruleset, and never changes classic branch protection (it refuses a branch that has it). It refuses the public upstream organization and has no default organization: you always pass `--org`.
-
-A dry run changes nothing; every `--apply` run is a live write to the repo you name.
+You choose the repo, read the dry run, check the release workflows, hooks, keys and installed apps, run the apply, comment on issue 838 and roll back if needed. A dry run changes nothing; every `--apply` run is a live write to the repo you name.
 
 ## Variables
 
@@ -28,7 +20,7 @@ OUT=<folder>     # outside any git checkout; receives <repo>-before.json
 
 ## Order for each repo
 
-1. **Set `OWNER`, `REPO` and `OUT`.** Never reuse an `OUT` folder that already holds the before-state file of this repo: the script refuses.
+1. **Set `OWNER`, `REPO` and `OUT`.**
 2. **Check webhooks, deploy keys and installed apps.** Anything that pushes to a protected branch must use pull requests once the rulesets are on.
 
    ```bash
@@ -37,22 +29,22 @@ OUT=<folder>     # outside any git checkout; receives <repo>-before.json
    gh api --paginate "orgs/$OWNER/installations" --jq '.installations[] | [.app_slug, .permissions.contents] | @tsv'; echo "exit status: $?"
    ```
 
-   Read the exit status of each. A command that failed (for example HTTP 403 or 404) means **unknown**, never "0": a missing answer is not an empty list. Resolve it before going on. The commands are the ones in [Branch Protection](branch-protection.md), with the repo and organization as variables.
+   Read the exit status of each. A command that failed (for example HTTP 403 or 404) means **unknown**, never "0": a missing answer is not an empty list. Resolve it before going on. Read the results as in [Branch Protection](branch-protection.md).
 3. **Dry run.** Writes nothing:
 
    ```bash
    uv run python scripts/apply_org_rulesets.py --org "$OWNER" --repo "$REPO"
    ```
 
-   Read all of it: the repo facts, the push check per branch (`pass`, `blocked` or `incomplete`, with how many direct pushes and how many events it looked at), the classic protection per branch, the rulesets already present, the number of `v*` tags, the rulesets it would create in order, any `would refuse --apply:` line, the digest, and the apply command. A dry run exits 0 when it printed a `digest:` line, and 69 when it could not plan the repo (`no plan: the repo could not be planned`).
-4. **Check the release workflows by hand.** The tag ruleset blocks moving and deleting `v*` tags, with no bypass. Open each workflow under `.github/workflows/` of the repo and look for a step that moves or deletes a `v*` tag (a force push of a tag, `git tag -f`, `git push --delete`, a release tool that recreates a tag). If one does, change it first, or do not apply to this repo yet: the script always creates the tag ruleset (it only skips one that already exists) and cannot tell what a workflow does. The dry run prints the same warning.
+   Read every line of it and resolve each `would refuse --apply:` line. A dry run that cannot plan the repo prints `no plan: the repo could not be planned`.
+4. **Check the release workflows by hand.** The dry run prints `WARNING: the tag ruleset blocks moving and deleting v* tags; check the release workflows of this repo by hand before applying.` Open each workflow under `.github/workflows/` of the repo and look for a step that moves or deletes a `v*` tag (a force push of a tag, `git tag -f`, `git push --delete`). If there is one, change it first or do not apply to this repo yet.
 5. **Apply**, with the digest the dry run printed:
 
    ```bash
    uv run python scripts/apply_org_rulesets.py --org "$OWNER" --repo "$REPO" --out "$OUT" --apply --confirm <digest>
    ```
 
-   The script reads everything again (nothing carries over from the dry run) and refuses with `confirm digest does not match the rulesets rendered now` when the digest of the ruleset bodies it renders now is not the one you passed; rerun the dry run. On success it prints `before state saved:` with the file, one `created:` line per ruleset with its id, `skipped, already present:` for any ruleset whose name is already on the repo, the `comment for issue 838:` line, and the rollback commands under `rollback by hand`.
+   A digest that is not the one the dry run printed gives `confirm digest does not match the rulesets rendered now`; rerun the dry run. The output has `before state saved:`, one `created:` line per ruleset it created, `skipped, already present:` for a ruleset it skipped, `comment for issue 838:` and, under `rollback by hand`, the rollback commands.
 6. **Check** (read-only):
 
    ```bash
@@ -61,76 +53,70 @@ OUT=<folder>     # outside any git checkout; receives <repo>-before.json
    ```
 
    Each branch must print `deletion`, `non_fast_forward` and `pull_request`. Do not test by pushing to, force pushing or deleting a real protected branch or tag.
-7. **Comment** the `comment for issue 838:` line (repo, date, ruleset ids by name) on issue 838. Keep the before-state file where you can find it.
+7. **Comment** the `comment for issue 838:` line on issue 838. Keep the before-state file where you can find it.
 
 ## The canary rule
 
-Start with one low-risk repo (few contributors, no release tags that workflows move). The canary must show complete activity coverage before other repos rely on it: every branch line of its dry run (`<branch>: <result> (source <source>, direct pushes N, examined N)`) must read `(source activity, ...)`, and no branch line and no `push check` line may read `incomplete`. If any branch reads `source commits` or `incomplete`, stop before a second repo and find out why.
+Start with one low-risk repo. The canary must show complete activity coverage before other repos rely on it: every branch line of its dry run reads `(source activity, ...)` and none reads `incomplete`. If any branch line reads `source commits` or `incomplete`, stop before a second repo.
 
 ## The 90-day push check
 
-Per branch, with one cutoff for the whole run (now minus 90 days):
-
-- Primary source: the activity feed of the branch. A `push`, `force_push` or `branch_deletion` event inside the window is a direct push; a `pr_merge` is not.
-- Fallback to the commit list when the feed call fails, its answer cannot be read, or it runs past 10 pages.
-- In the fallback, a commit list that fails or runs past 10 pages gives `incomplete`. For each of the first 200 commits the script asks for the pull requests that contain it; a commit with no merged pull request into that branch is a direct push.
-- Any direct push found gives `blocked`. With none found, a failed pull-request lookup or more than 200 commits gives `incomplete`. Otherwise `pass`.
-- Overall: `blocked` if any branch is blocked, `pass` only when every branch passes, otherwise `incomplete`. `incomplete` is never turned into `pass`.
+- Each branch ends `pass`, `blocked` or `incomplete`, and the dry run prints the overall result with the same three words.
+- `incomplete` is never turned into `pass`.
+- Each branch line names its source: `source activity` or `source commits`.
+- A direct push by a named person is not excused: the check reports `blocked` for it.
 
-A direct push by a named person is **not** excused here. If someone pushes to a protected branch on purpose, the repo stays blocked until that is settled with its owner (see the follow-ups).
+## Refusals and failures
 
-## Refusals
+An `--apply` that refuses prints `refused:` and the texts below, joined by `; `, on stderr.
 
-`--apply` prints `refused:` and the texts below on stderr, joined by `; `, and exits 69. No ruleset was written and no file was created. A dry run prints the first ten rows as `would refuse --apply: <text>` lines.
-
-| Text | What it means |
+| Text | What you do |
 |---|---|
-| `repo is archived` | GitHub says the repo is archived |
-| `no admin permission on the repo` | Your login has no admin permission on it |
-| `repo has no default branch` | GitHub reports no default branch |
-| `repo cannot be read (HTTP n)` | GitHub did not return the repo (n is the HTTP status; check the name and your access) |
-| `a branch lookup failed` | The lookup of `master` or `integration` answered something other than found or not found |
-| `branch not supported: not a plain branch name: '<name>'` | The default branch name contains `*` or `~`, or starts with `refs/` |
-| `push check is blocked` or `push check is incomplete` | See the 90-day push check |
-| `classic branch protection on <branch>` or `branch protection state unknown on <branch>` | The branch has classic protection, or GitHub's answer could not be read. The script never edits it; decide by hand |
-| `ruleset list cannot be read (HTTP n)` | GitHub did not return the list of the repo's rulesets |
-| `repo lists a ruleset id this script never touches` | The repo lists a ruleset with an id that belongs to this project's own repository: this is not the repo you meant |
-| `no --out folder given` | `--apply` needs `--out` |
-| `confirm digest does not match the rulesets rendered now` | The digest is not the one for the rulesets rendered now; rerun the dry run and use its digest |
-| `before-state file already exists: <path>` | `<repo>-before.json` is already in the `--out` folder; use another folder or move the old file away on purpose |
-| `before-state read failed for ruleset <id>` | An existing ruleset could not be read to save it first, so nothing was written |
-
-Other messages:
-
-- Usage mistakes exit 64 with `usage error:` and one of `--repo takes exactly one repo name` (also for `.`, `..` and a name with characters other than letters, digits, `_`, `.` and `-`), `--org: <reason>` (an empty name, a name with such other characters or one that starts with `-`, or the upstream organization), `--confirm needs --apply`, `--apply needs --confirm DIGEST`, or an option error from the argument parser.
-- `refused: <text>` with some other text means the script's allowlist refused a call. The usual cause is a default branch name with an unusual character (for example `a+b`), which the allowlist does not accept: do that repo by hand. If the name is plain, report it as a bug in the script.
-- `failed: <text>` with a file error (for example an `--out` folder that cannot be created, or a rule file that cannot be read) exits 69.
-
-## Failures after the before-state file
-
-Once `<repo>-before.json` is written, a failed step prints `failed:` and one of these texts on stderr, prints what was written and the rollback commands, and exits 69:
-
-- `POST of <name> failed (HTTP n)`: GitHub refused the request, or its answer had no ruleset id.
-- `POST of <name> timed out and no ruleset of that name found`: the POST timed out, and the repo's rulesets, read straight afterwards, held none of that name. If one does hold it, the script adopts it and reads it back like any other. A POST is never repeated.
-- `read-back of <name> (id n) failed`: the ruleset just created could not be read.
-- `read-back of <name> (id n) differs: <differences>`: what GitHub returned is not what the script sent.
-
-If the first POST fails, only the before-state file was written and no rollback command is printed. If a later step fails, the rulesets created before it stay in place and their DELETE commands are printed; a read-back failure lists that ruleset's own id too. A ruleset whose name is already on the repo's list when the script applies is skipped (`skipped, already present:`) and never edited.
+| `repo is archived` | Do not apply to this repo |
+| `no admin permission on the repo` | Get admin permission on the repo, then rerun the dry run |
+| `repo has no default branch` | Do not apply to this repo |
+| `repo cannot be read (HTTP <n>)` | Check the name and your access with `gh api "repos/$OWNER/$REPO"`, then rerun the dry run |
+| `a branch lookup failed` | Rerun the dry run; if it repeats, check your access |
+| `branch not supported: <reason>` | Do this repo by hand |
+| `push check is <result>` | Do not apply; read the push check lines of the dry run |
+| `classic branch protection on <branch>` | Do not apply; decide by hand with the repo owner |
+| `branch protection state unknown on <branch>` | Rerun the dry run; if it repeats, decide by hand |
+| `ruleset list cannot be read (HTTP <n>)` | Check your access, then rerun the dry run |
+| `repo lists a ruleset id this script never touches` | Stop: the ids 28081842, 28081844 and 28081845 are never touched, so this is probably not the repo you meant |
+| `no --out folder given` | Add `--out "$OUT"` |
+| `confirm digest does not match the rulesets rendered now` | Rerun the dry run and use the digest it prints |
+| `before-state file already exists: <path>` | Use another `OUT` folder, or move the old file away on purpose |
+| `before-state read failed for ruleset <id>` | Check your access, then rerun the dry run |
+
+A usage mistake prints one of these and exits 64: fix the command line.
+
+- `usage error:`
+- `--repo takes exactly one repo name`
+- `--org: <reason>`
+- `--confirm needs --apply`
+- `--apply needs --confirm DIGEST`
+
+Any other `refused: <text>` or `failed: <text>`: stop and report it.
+
+After the before-state file is saved, a failed step prints `failed:` and one of these on stderr:
+
+- `POST of <name> failed (HTTP <n>)`
+- `POST of <name> timed out and no ruleset of that name found`
+- `read-back of <name> (id <n>) failed`
+- `read-back of <name> (id <n>) differs: <differences>`
+
+After any `failed:` line, or any non-zero exit of an `--apply` run, first list the repo's rulesets by hand with the check command in step 6. Compare that list with the printed `created:` lines and the `rollback by hand` commands: a ruleset can exist that no printed line names. Only then decide on a rollback. A rerun into the same `OUT` refuses with `before-state file already exists: <path>`.
 
 ## Roll back by hand
 
-The script has no rollback. After an apply, or a failed one, it prints one command per ruleset it created, newest first:
+The script has no rollback. Run the commands it printed under `rollback by hand`, or, for an id you found by listing the rulesets:
 
 ```bash
 gh api --method DELETE "repos/$OWNER/$REPO/rulesets/<id>"
 ```
 
-`<repo>-before.json` in `OUT` holds `org`, `repo`, `saved_at`, `digest`, the full body of every ruleset the repo had (each read by id), and `protection` with `none` for each branch of the set (a branch with classic protection is refused). The script never restores it; it is the record to restore from.
+`<repo>-before.json` in `OUT` holds the keys `org`, `repo`, `saved_at`, `digest`, `rulesets` and `protection`. It is the record to restore from by hand; the script never reads it back.
 
 ## Not in this version (follow-ups)
 
 Dropped from the first plan to keep this small, to be decided and built later if they are wanted: a persistent file of target repos with a status per repo and one writer; owner statements and evidence (pushes accepted by the owner, tag statements and exceptions); a scan of workflows for tag mutation and handling of deleted tags; an automatic review of hooks, keys and installed apps (step 2 above is by hand); a rollback command; a check over all the repos that the rulesets are on; an allowlist file; a branch-only interim state; and seven owner decisions from the review of the larger plan.
-
-## Tests
-
-`tests/org_rulesets/` covers the script against a fake GitHub (no live call). `test_page.py` checks this page: its variables, its commands, that every message the script prints for a refusal or a failure is on it, and that it names no real private repo.
diff --git a/tests/org_rulesets/test_page.py b/tests/org_rulesets/test_page.py
index 8be276aa0..89f55e70b 100644
--- a/tests/org_rulesets/test_page.py
+++ b/tests/org_rulesets/test_page.py
@@ -105,6 +105,28 @@ def test_the_fixed_output_lines_of_the_script_are_on_the_page(page):
         assert text in flat, text
 
 
+def test_every_text_quoted_in_the_message_lists_is_in_the_script(orr, page):
+    """The other direction: the first span of each table row and bullet between
+    'Refusals and failures' and 'Roll back by hand' is a script string once the
+    placeholders in angle brackets are cut out."""
+    start = page.index("## Refusals and failures")
+    end = page.index("## Roll back by hand")
+    source = Path(orr.__file__).read_text(encoding="utf-8")
+    spans = []
+    for line in page[start:end].splitlines():
+        found = re.match(r"^(?:\| |- )`([^`]+)`", line)
+        if found and found.group(1) != "Text":
+            spans.append(found.group(1))
+    assert len(spans) >= 20
+    for span in spans:
+        for piece in re.split(r"<[^>]*>", span):
+            piece = piece.strip()
+            if len(piece) > 2:
+                assert piece in source, (
+                    f"{piece!r} (from {span!r}) is not in the script"
+                )
+
+
 def private_repo_names():
     text = SUMMARY.read_text(encoding="utf-8")
     start = text.index("Clay's answer for this story")

Earlier blocking findings of this start (empty on the first review): F4.1 sev=blocking trigger=B2 ac=scope at=scripts/apply_org_rulesets.py:663 anchor=`lines += [f"would refuse --apply: {p}" for p in found["problems"]]` chk=n,y,n,n family=page-dryrun-refusal-count-claim fix=in page line 84 replace "prints the first ten rows as" with "prints every refusal as" first=A3 origin=late: page line 84 says a dry run prints "the first ten rows" of `would refuse --apply:` lines, but the script has no cap of ten; lines 628 and 663 print every problem.
F4.2 sev=blocking trigger=B2 ac=scope at=scripts/apply_org_rulesets.py:701 anchor=`except (ValueError, KeyError, TypeError): return None` chk=n,y,n,n family=page-timeout-message-condition fix=in page line 114 add that the same message also appears when the list read straight afterwards could not be read, in which case the ruleset may exist and its DELETE command was not printed, so list the rulesets by hand before anything else first=A3 origin=late: page line 114 says the `timed out and no ruleset of that name found` message means the follow-up list "held none of that name"; `_adopt` (lines 693-702) also returns None when that list call fails or cannot be parsed, so the same message (lines 786-790) can appear while the ruleset exists and is missing from the printed rollback commands.

Saved-probe re-check hit locations (may be empty): --- page-recipe-not-possible
3:How to put the rulesets of [Branch Protection](branch-protection.md) on another repo of an organization, one
47:   A digest that is not the one the dry run printed gives `confirm digest does not match the rulesets rende
108:After any `failed:` line, or any non-zero exit of an `--apply` run, first list the repo's rulesets by hand
--- page-digest-overclaim
3:How to put the rulesets of [Branch Protection](branch-protection.md) on another repo of an organization, one
7:The script checks one repo and prints a dry run that writes nothing. With `--apply --confirm <digest>` and `
41:5. **Apply**, with the digest the dry run printed:
44:   uv run python scripts/apply_org_rulesets.py --org "$OWNER" --repo "$REPO" --out "$OUT" --apply --confirm
47:   A digest that is not the one the dry run printed gives `confirm digest does not match the rulesets rende
87:| `confirm digest does not match the rulesets rendered now` | Rerun the dry run and use the digest it print
97:- `--apply needs --confirm DIGEST`
118:`<repo>-before.json` in `OUT` holds the keys `org`, `repo`, `saved_at`, `digest`, `rulesets` and `protecti
--- page-refused-bug-overclaim
99:Any other `refused: <text>` or `failed: <text>`: stop and report it.
122:Dropped from the first plan to keep this small, to be decided and built later if they are wanted: a persis
--- page-refusal-cause-imprecise
32:   Read the exit status of each. A command that failed (for example HTTP 403 or 404) means **unknown**, nev
80:| `branch not supported: <reason>` | Do this repo by hand |
--- page-usage-reason-incomplete
91:A usage mistake prints one of these and exits 64: fix the command line.
93:- `usage error:`
94:- `--repo takes exactly one repo name`
95:- `--org: <reason>`


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

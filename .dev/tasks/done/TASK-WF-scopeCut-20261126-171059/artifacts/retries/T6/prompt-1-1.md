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
index 000000000..1855ab101
--- /dev/null
+++ b/docs/developer-guide/branch-protection-multi-repo.md
@@ -0,0 +1,114 @@
+# Branch Protection for Other Repos
+
+How to put the three rulesets of [Branch Protection](branch-protection.md) (`.github/rulesets/protect-master.json`, `protect-integration.json` and `protect-release-tags.json`) on another repo of an organization, one repo per run, with `scripts/apply_org_rulesets.py`. The script reads the rule files, checks the repo, prints what it would do, and only with `--apply --confirm <digest>` creates the rulesets and reads each one back.
+
+## What the script does, and what you do
+
+The script does, for the one repo you name:
+
+- reads the repo (archived? admin rights? default branch? are `master` and `integration` there?);
+- runs the 90-day direct-push check on each branch it would protect;
+- reports classic branch protection, rulesets already present and the number of `v*` tags;
+- in a dry run (no `--apply`), prints all of that, the rulesets it would create in order, a digest of them, and the exact command to apply;
+- with `--apply --confirm <digest>`, saves the repo's before state to `<repo>-before.json`, creates the rulesets (the tag ruleset, then `integration`, then `master`, then the default branch if it is another name), and reads each back before the next write.
+
+You do, by hand: choose the repo, read the dry run, check the release workflows, check hooks, keys and installed apps, run the apply, comment the result on the tracking issue (838), and roll back if needed. The script never posts a comment, never edits or deletes a ruleset and never touches classic branch protection. It refuses the public upstream organization and has no default organization: you always pass `--org`.
+
+The script changes nothing by itself: every `--apply` run is a live write to the repo you name.
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
+1. **Set `OWNER`, `REPO` and `OUT`.** Never reuse an `OUT` folder for a repo whose before-state file is already in it: the script refuses.
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
+   Read all of it: the repo facts, the push check per branch (`pass`, `blocked` or `incomplete`, with how many direct pushes and how many events it looked at), the classic protection per branch, the rulesets already present, the number of `v*` tags, the rulesets it would create in order, any `would refuse --apply:` line, the digest, and the apply command. A dry run exits 0 when it could plan the repo and 69 when it could not (for example the repo cannot be read).
+4. **Check the release workflows by hand.** The tag ruleset blocks moving and deleting `v*` tags, with no bypass. Open each workflow under `.github/workflows/` of the repo and look for a step that moves or deletes a `v*` tag (a force push of a tag, `git tag -f`, `git push --delete`, a release tool that recreates a tag). If one does, change it first or leave the tag ruleset out; the script cannot tell. The dry run prints the same warning.
+5. **Apply**, with the digest the dry run printed:
+
+   ```bash
+   uv run python scripts/apply_org_rulesets.py --org "$OWNER" --repo "$REPO" --out "$OUT" --apply --confirm <digest>
+   ```
+
+   The script reads everything again and recomputes the digest, so a changed rule file or a changed repo makes the digest differ and the run refuses. It prints the path of the before-state file, `created:` lines with the ids, the comment line for issue 838 and the rollback commands.
+6. **Check** (read-only):
+
+   ```bash
+   gh api "repos/$OWNER/$REPO/rulesets" --jq '.[] | [.id, .name, .enforcement] | @tsv'
+   gh api "repos/$OWNER/$REPO/rules/branches/<branch>" --jq '.[].type'
+   ```
+
+   Each branch must print `deletion`, `non_fast_forward` and `pull_request`. Do not test by pushing to, force pushing or deleting a real protected branch or tag.
+7. **Comment** the line the script printed (repo, date, ruleset ids by name) on issue 838. Save the before-state file where you can find it.
+
+## The canary rule
+
+Start with one low-risk repo (few contributors, no release tags that workflows move). The 90-day check normally reads GitHub's activity feed. The canary must show complete activity coverage before other repos rely on it: its dry run must end with `source activity` on every branch and no `incomplete`, and the push count it reports must match what you can see in the repo's history. If the canary falls back to the commit list, or answers `incomplete`, stop and find out why before doing a second repo.
+
+## The 90-day push check
+
+Per branch, over the last 90 days (one cutoff for the whole run):
+
+- Primary source: the activity feed of the branch. A `push`, `force_push` or `branch_deletion` is a direct push; a `pr_merge` is not.
+- Fallback, when the feed is unavailable (HTTP 403 or 404) or runs past 10 pages: the commit list since the cutoff, and for each commit whether a merged pull request contains it. A commit with none is a direct push. More than 200 commits on one branch gives `incomplete`.
+- `pass` only with zero direct pushes on every branch. `blocked` for any direct push. `incomplete` when no source gave a full answer; it is never turned into `pass`.
+
+A direct push by a named person is **not** excused here. If someone pushes to `master` on purpose, the repo stays blocked until that is settled with its owner (see the follow-ups).
+
+## Refusals
+
+`--apply` makes no write and writes no file when any of these holds. The text is printed on stderr after `refused:` and the exit status is 69.
+
+| Text | Meaning |
+|---|---|
+| `repo is archived`, `no admin permission on the repo`, `repo has no default branch` | The repo cannot take rulesets from you |
+| `repo cannot be read (HTTP n)`, `a branch lookup failed`, `ruleset list cannot be read (HTTP n)` | GitHub did not answer a read; fix access and rerun |
+| `push check is blocked` or `push check is incomplete` | See the 90-day push check |
+| `classic branch protection on <branch>` or `branch protection state unknown on <branch>` | The branch already has classic protection (or the answer failed). The script never edits it; decide by hand |
+| `repo lists a ruleset id this script never touches` | The repo holds one of the three ruleset ids of the source repo; this is not the repo you meant |
+| `confirm digest does not match the rulesets rendered now` | The digest is not the one the dry run printed for the current rules and repo; rerun the dry run |
+| `before-state file already exists` | Rerun with another `OUT`, or move the old file away on purpose |
+| `before-state read failed for ruleset <id>` | The existing rulesets could not be saved first, so nothing was written |
+| `no --out folder given` | `--apply` needs `--out` |
+
+A ruleset of the same name that already exists is skipped with a printed line; it is never edited. A failed step after a write (`POST of <name> failed`, `POST of <name> timed out and no ruleset of that name found`, `read-back of <name> (id n) differs`) stops the run, prints what was written and the rollback commands, and exits 69 with `failed:` on stderr. A POST that timed out is followed by a list of the repo's rulesets; the ruleset is adopted if it exists, and a POST is never repeated. A usage mistake exits 64. If GitHub itself refuses the POST (for example HTTP 403 because the plan does not allow rulesets on that repo), the run stops after the before-state file; nothing else was written.
+
+## Roll back by hand
+
+The script has no rollback. It prints, after an apply (or a failed one), one command per ruleset it created, newest first:
+
+```bash
+gh api --method DELETE "repos/$OWNER/$REPO/rulesets/<id>"
+```
+
+`<repo>-before.json` in `OUT` holds what the repo had before: the full body of every existing ruleset and the classic protection per branch (`none` when there was none). It is the record to restore from; the script does not restore it.
+
+## Not in this version (follow-ups)
+
+Dropped from the first plan to keep this small, to be decided and built later if they are wanted: a persistent file of target repos with a status per repo and one writer; owner statements and evidence (pushes accepted by the owner, tag statements and exceptions); a scan of workflows for tag mutation and handling of deleted tags; an automatic review of hooks, keys and installed apps (step 2 above is by hand); a rollback command; a check over all the repos that the rulesets are on; an allowlist file; a branch-only interim state; and seven owner decisions from the review of the larger plan.
+
+## Tests
+
+`tests/org_rulesets/` covers the script against a fake GitHub (no live call). `test_page.py` checks this page: its variables, its commands and that it names no real private repo.
diff --git a/tests/org_rulesets/test_page.py b/tests/org_rulesets/test_page.py
new file mode 100644
index 000000000..06ffdc24e
--- /dev/null
+++ b/tests/org_rulesets/test_page.py
@@ -0,0 +1,88 @@
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
+    files += sorted((ROOT / "tests" / "org_rulesets").glob("*.py"))
+    for path in files:
+        text = path.read_text(encoding="utf-8").lower()
+        for name in names:
+            assert name.lower() not in text, f"{name} in {path.name}"

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

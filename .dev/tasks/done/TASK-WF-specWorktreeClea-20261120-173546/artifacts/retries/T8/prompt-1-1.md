8c9b922d40bbeb4ec422680f7f47e07c2f0b5ae4
Review one task for spec compliance.

Task brief: ## Task 8: Write the removal and keep tests for the eight rules

Depends on: Task 7

Create `tests/worktree_cleanup/test_rules.py` with the first test group of source section 9, each case failing if its rule is removed. Removable case: merged own pull request, HEAD is its last commit, clean, idle 8 days, no process, no Orca terminal, issue closed, so the decision is `removable`. Kept cases, each asserting the reason text, for: the main checkout; a repo that is not ours; the folder the script runs in; a locked worktree; a missing folder (reported, never pruned); a detached HEAD; a name starting with `orca-port-`, `orca-recipe-` or `orca-pristine-` (while `coder-orca-port` is not caught); no pull request; an open pull request; a pull request closed without merging; a landed check that says `UNKNOWN` or fails; a commit after the pull request's head; a HEAD that is not the pull request's head; an issue that is open through each of the four places (closing reference, `#N` in the body, a number in the branch name, Orca's card comment); an issue lookup that fails; a changed tracked file; an untracked file outside `.dev/`; an ignored environment file outside `.dev/`; an unknown ignored name; a process with its working folder inside; a failing `/proc` scan (keeps every worktree); a process inside a worktree that has no Orca terminal open; a merge, rebase, cherry-pick and `index.lock` in progress; idle 6 days; created 3 days ago; pinned; a keep file. Also: ignored build output and generated copies (`__pycache__`, `.venv`, `.codegraph`, `uv.lock`, the `.claude/agents`, `commands`, `hooks`, `skills` and `templates` copies) are allowed and not a reason to keep; a squash-merged pull request whose commits are not on the base is judged landed from pull request state; a pull request that is merged but whose branch was later reused for new commits keeps the worktree.

Acceptance criteria:
- `uv run pytest tests/worktree_cleanup/test_rules.py -v` passes and has at least one test for every item listed above.
- Mutation check by hand for one rule per group: temporarily making rule 4 always pass (or rule 3, or rule 6) makes at least one test in this file fail.
- Every kept case asserts the plain-English reason, not only the decision.

AC ids (in source order): T8.AC1, T8.AC2, T8.AC3
Global constraints: ## Constraints

- Safety for this whole run (set by the issue owner): tests use throwaway git repositories, a local bare repository standing in for the evidence repo, and a fake runner with recorded `gh`, `git` and `orca` replies. No task and no test runs the script with `--apply` against real worktrees, removes, moves or clears any real worktree or file, creates or switches on an Orca automation (the definition is a file, status "written, not switched on"), closes a real Orca terminal, or pushes to `IronbellyOrg/run-evidence`. The only run against the real workspace is a dry run (Task 20).
- The script never uses `--force` on `orca worktree rm` or `git worktree remove`, never `git branch -D`, never `rm`, never `git worktree prune`, never pushes anywhere but the evidence repo's clone, and never deletes a remote branch. The only force flag in the whole script is `git clean -f -x --` on exact paths listed in a verified `saved-paths.txt` (source sections 3, 6 and 8, decision 1).
- The script never deletes a file or folder itself (no `rm`, no `shutil.rmtree`, no `unlink`): its lock files stay in place under `fcntl.flock`, and a scratch folder left by a failed save stays and is named in the log. This plan chose that so "never rm" holds without exception.
- Python standard library only, no model call, no agent or model name in any output, credentials only from the environment (`GH_TOKEN`), no credential file is ever opened by the script, no secret is printed or written (source sections 5, 6 and 9).
- The 11 decisions of source section 8 are final. Out of scope (source section 10): where worktrees live (#289, #322), Jay's other pieces, the closeout itself (#668, so `/sc:closeout` and its files and tests are not changed), any shared or remote branch, anything that is not a git worktree of our repos.
- The change to the separate `IronbellyOrg/run-evidence` repo (source section 15, step 5) is prepared as text under `./artifacts/` and not applied by this plan; no other repo is pushed to.
- The spec mentions that `archive` by hand "can still save" tracked edits and later commits "as a patch and a bundle" (source section 7, "What is not saved"). It gives no step, format or folder for it, so it is not built; Task 12 records that in the verb's help text so it is not a silent drop.
- Where the spec is silent this plan decides, and says so in the task: `/sc:worktrees` goes on the never-as-worker list (Task 16); outside an IronClaude checkout the command stops and runs nothing (Task 14); the default `--out` folder is `~/.local/state/worktree-cleanup` so nothing is ever written inside a worktree (Task 2); `/sc:closeout` is left unchanged (this constraint).
- Edit only under `src/superclaude/`, `scripts/`, `tests/`, `docs/`, `plugins/superclaude/skills/sc-recommend/refs/`, `CHANGELOG.md` and `NOTICE`; run `make sync-dev` after editing `src/superclaude/` and never edit the `.claude/` copies. Plain English and no em or en dashes in every new file. A command file must not point at another primitive through a `src/superclaude/...` path.
- The pull request for this change is opened by the finishing step of the run, `/sc:pr-submit --monitor 3` (source section 15, step 7), after the last task; no task of this plan opens it.
- Corrections the implementer made to this plan before the first task started, from the advisory reflect review of the plan (the list is in `./artifacts/plan-corrections.md`): Task 1 (the item 1 fallback, the open pull request proof, item 7), Task 2 (a positive allowlist runner and its own first tests), Tasks 3 to 5 (their own tests, so no check waits for a later task), Task 7 (shared fixtures only), Tasks 11 and 12 (Orca read back, the command list in the JSON), Task 14 (the write-verb classification), Task 19 (15 rows), Task 20 (dependencies).
Start sha: 8c9b922d40bbeb4ec422680f7f47e07c2f0b5ae4
Diff against the start snapshot: diff --git a/tests/worktree_cleanup/test_rules.py b/tests/worktree_cleanup/test_rules.py
deleted file mode 100644
index 8205ae6f4..000000000
--- a/tests/worktree_cleanup/test_rules.py
+++ /dev/null
@@ -1,387 +0,0 @@
-"""Task 6: the eight rules, their reasons, and the table. All facts are built by hand;
-``decide`` is pure, so no process, folder or network is touched here."""
-
-from __future__ import annotations
-
-import dataclasses
-import json
-
-import pytest
-
-NOW = 2_000_000_000.0
-DAY = 86400.0
-
-
-@pytest.fixture
-def good(wc):
-    """Facts for a worktree that passes every rule."""
-    wt = wc.GitWorktree(
-        "/w/wts/topic", "/w/main", "a" * 40, "topic", False, False, False, False, False
-    )
-    facts = wc.WorktreeFacts(
-        worktree=wt,
-        head="a" * 40,
-        origin=wc.OriginInfo("IronbellyOrg", "IronClaude"),
-        state=wc.LocalState(),
-        last_commit_ts=NOW - 20 * DAY,
-        git_file_mtime=NOW - 20 * DAY,
-        created_ts=NOW - 30 * DAY,
-        size_bytes=3 * 1024 * 1024,
-        git_dir="/w/main/.git/worktrees/topic",
-    )
-    pr = wc.PullRequest(
-        9, "MERGED", "a" * 40, "x", "2026-11-01T00:00:00Z", "t", "", (), "topic"
-    )
-    return wc.RuleInputs(
-        facts=facts,
-        now=NOW,
-        pr_lookup=wc.PrLookup(True, pr),
-        landed=wc.Landed("MERGED", "installed copy"),
-        after=wc.AfterPr("same", 0),
-        issues=wc.IssueFacts((), ()),
-        procs=wc.ProcScan(True, ()),
-    )
-
-
-def with_facts(wc, inp, **change):
-    return dataclasses.replace(inp, facts=dataclasses.replace(inp.facts, **change))
-
-
-def with_wt(wc, inp, **change):
-    wt = dataclasses.replace(inp.facts.worktree, **change)
-    return with_facts(wc, inp, worktree=wt)
-
-
-def orca(wc, **change):
-    base = dict(
-        worktree_id="w", selector="id:w", path="/w/wts/topic", branch="b", repo="r",
-        last_activity_ms=None, is_pinned=False, live_terminal_count=0, linked_pr_hint=None, comment="",
-    )  # fmt: skip
-    base.update(change)
-    return wc.OrcaWorktree(**base)
-
-
-def state(wc, **change):
-    return dataclasses.replace(wc.LocalState(), **change)
-
-
-def test_a_worktree_that_passes_everything_is_removable(wc, good):
-    d = wc.decide(good)
-    assert (d.decision, d.rule, d.reason, d.note) == ("removable", None, "", "")
-    assert d.saved_copy == "none needed"
-
-
-def test_decide_is_pure_and_repeatable(wc, good, never_run_runner):
-    assert wc.decide(good) == wc.decide(good)
-    assert wc.decide(dataclasses.replace(good, own_folder=True)) == wc.decide(
-        dataclasses.replace(good, own_folder=True)
-    )
-    assert never_run_runner.commands == []
-
-
-def case(wc, good, name):
-    """One worktree that fails only one rule: (inputs, rule number, reason)."""
-    s = lambda **c: with_facts(wc, good, state=state(wc, **c))  # noqa: E731
-    pr = lambda **c: dataclasses.replace(  # noqa: E731
-        good, pr_lookup=wc.PrLookup(True, dataclasses.replace(good.pr_lookup.pr, **c))
-    )
-    cases = {
-        "main": (with_wt(wc, good, is_main=True), 1, "main checkout"),
-        "origin-not-ours": (with_facts(wc, good, origin=wc.OriginInfo("Other", "x")), 1, "not our repo"),
-        "origin-unknown": (with_facts(wc, good, origin=None), 1, "not our repo"),
-        "own-folder": (dataclasses.replace(good, own_folder=True), 1, "this is where the script runs"),
-        "locked": (with_wt(wc, good, locked=True), 1, "locked"),
-        "missing": (with_facts(wc, good, present=False), 1, "folder missing (reported only)"),
-        "guard": (with_wt(wc, good, path="/w/wts/orca-port-x"), 1, "on the name guard (infrastructure folder)"),
-        "detached": (with_wt(wc, good, detached=True, branch=None), 1, "detached HEAD"),
-        "no-pr": (dataclasses.replace(good, pr_lookup=wc.PrLookup(True, None)), 2, "no pull request"),
-        "pr-lookup": (dataclasses.replace(good, pr_lookup=wc.PrLookup(False, None, "boom")), 2, "pull request lookup failed: boom"),
-        "pr-open": (pr(state="OPEN"), 2, "pull request #9 is open"),
-        "pr-closed": (pr(state="CLOSED"), 2, "pull request #9 closed, not merged"),
-        "landed-unknown": (dataclasses.replace(good, landed=wc.Landed("UNKNOWN", "x")), 2, "landed check said UNKNOWN"),
-        "landed-missing": (dataclasses.replace(good, landed=None), 2, "landed check said UNKNOWN"),
-        "landed-open": (dataclasses.replace(good, landed=wc.Landed("OPEN", "x")), 2, "pull request #9 is open"),
-        "after-3": (dataclasses.replace(good, after=wc.AfterPr("ahead", 3)), 3, "3 commits after the pull request"),
-        "after-1": (dataclasses.replace(good, after=wc.AfterPr("ahead", 1)), 3, "1 commit after the pull request"),
-        "after-unknown": (dataclasses.replace(good, after=wc.AfterPr("unknown", None)), 3, "HEAD is not the pull request's head"),
-        "after-missing": (dataclasses.replace(good, after=None), 3, "HEAD is not the pull request's head"),
-        "issue-open": (
-            dataclasses.replace(good, issues=wc.IssueFacts((wc.Issue("o/r", 21, "OPEN", ("x",)),), ())),
-            4, "issue #21 is open",
-        ),
-        "issue-failed": (
-            dataclasses.replace(good, issues=wc.IssueFacts((), ("issue lookup failed: o/r#4",))),
-            4, "issue lookup failed: o/r#4",
-        ),
-        "issue-missing": (dataclasses.replace(good, issues=None), 4, "issue lookup failed"),
-        "changed": (s(changed_tracked=["a", "b"]), 5, "2 changed tracked files"),
-        "untracked": (s(untracked_outside_dev=["a"]), 5, "1 untracked file outside .dev"),
-        "ignored-local": (s(ignored_unknown=[".env", "x.key"]), 5, "ignored local state: .env, x.key"),
-        "state-unread": (with_facts(wc, good, state=None), 5, "ignored local state: git status could not be read"),
-        "save-failed": (
-            dataclasses.replace(with_facts(wc, good, state=state(wc, untracked_dev=[".dev/a"])), save_state="failed: push refused"),
-            5, "saved copy failed: push refused",
-        ),
-        "save-unset": (with_facts(wc, good, state=state(wc, ignored_dev=[".dev/a"])), 5, "saved copy failed: no save state for the .dev files"),
-        "process": (
-            dataclasses.replace(good, procs=wc.ProcScan(True, ((412, "/w/wts/topic/sub", "node"),))),
-            6, "in use: process 412 (node)",
-        ),
-        "scan-failed": (dataclasses.replace(good, procs=wc.ProcScan(False, failure="pid 5: boom")), 6, None),
-        "no-scan": (dataclasses.replace(good, procs=None), 6, None),
-        "nested": (with_facts(wc, good, nested_checkouts=["inner/.git"]), 6, "holds another checkout"),
-        "operation": (with_facts(wc, good, operations=["MERGE_HEAD"]), 6, "git operation in progress"),
-        "unread-folder": (with_facts(wc, good, failures=["3 folder entries could not be read"]), 6, "in use: the folder or its git folder could not be read in full"),
-        "git-dir-unread": (with_facts(wc, good, git_dir=None), 6, "in use: the folder or its git folder could not be read in full"),
-        "missing-real": (with_facts(wc, good, present=False, origin=None, head=None, state=None, git_dir=None), 1, "folder missing (reported only)"),
-        "created-unknown": (with_facts(wc, good, created_ts=None), 7, "created time unknown (needs 7)"),
-        "idle": (with_facts(wc, good, git_file_mtime=NOW - 2 * DAY, last_commit_ts=NOW - 3 * DAY), 7, "idle 2 days (needs 7)"),
-        "idle-unknown": (with_facts(wc, good, git_file_mtime=None, last_commit_ts=None), 7, "idle time unknown (needs 7)"),
-        "young": (with_facts(wc, good, created_ts=NOW - 3 * DAY), 7, "created 3 days ago (needs 7)"),
-        "pinned": (dataclasses.replace(good, orca=orca(wc, is_pinned=True)), 8, "pinned in Orca"),
-        "keep-file": (with_facts(wc, good, keep_file=True), 8, "keep file present"),
-    }  # fmt: skip
-    return cases[name]
-
-
-CASE_NAMES = [
-    "main", "origin-not-ours", "origin-unknown", "own-folder", "locked", "missing", "guard", "detached",
-    "no-pr", "pr-lookup", "pr-open", "pr-closed", "landed-unknown", "landed-missing", "landed-open",
-    "after-3", "after-1", "after-unknown", "after-missing", "issue-open", "issue-failed", "issue-missing",
-    "changed", "untracked", "ignored-local", "state-unread", "save-failed", "save-unset",
-    "process", "scan-failed", "no-scan", "nested", "operation", "unread-folder", "git-dir-unread",
-    "missing-real", "created-unknown",
-    "idle", "idle-unknown", "young", "pinned", "keep-file",
-]  # fmt: skip
-
-
-@pytest.mark.parametrize("name", CASE_NAMES)
-def test_failing_only_one_rule_keeps_the_worktree_with_that_reason(wc, good, name):
-    inp, rule, reason = case(wc, good, name)
-    d = wc.decide(inp)
-    assert d.decision == "kept" and d.rule == rule
-    if reason is not None:
-        assert d.reason == reason
-    else:
-        assert d.reason.startswith("in use: the process scan failed")
-
-
-def test_the_first_failed_rule_is_the_one_shown(wc, good):
-    inp = dataclasses.replace(
-        with_facts(wc, good, keep_file=True, state=state(wc, changed_tracked=["a"])),
-        pr_lookup=wc.PrLookup(True, None),
-        own_folder=True,
-    )
-    d = wc.decide(inp)
-    assert (d.rule, d.reason) == (1, "this is where the script runs")
-    inp = dataclasses.replace(inp, own_folder=False)
-    assert wc.decide(inp).rule == 2
-    inp = dataclasses.replace(inp, pr_lookup=good.pr_lookup)
-    assert wc.decide(inp).rule == 5
-
-
-def test_reasons_are_the_strings_of_the_spec(wc):
-    """Every reason the spec table names for rules 1 to 8 appears in the rule code."""
-    import inspect
-
-    text = (
-        inspect.getsource(wc._rule1)
-        + inspect.getsource(wc._rule2)
-        + inspect.getsource(wc._rule3)
-    )
-    for words in ("main checkout", "not our repo", "this is where the script runs", "locked",
-                  "folder missing (reported only)", "detached HEAD", "no pull request", "is open",
-                  "closed, not merged", "landed check said UNKNOWN", "after the pull request",
-                  "HEAD is not the pull request's head"):  # fmt: skip
-        assert words in text, words
-    text = (
-        inspect.getsource(wc._rule4)
-        + inspect.getsource(wc._rule5)
-        + inspect.getsource(wc._rule6)
-        + inspect.getsource(wc._rule7)
-        + inspect.getsource(wc._rule8)
-    )
-    for words in ("is open", "issue lookup failed", "changed tracked file", "untracked file", "outside .dev",
-                  "ignored local state:", "saved copy failed:", "in use: process", "holds another checkout",
-                  "git operation in progress", "(needs", "pinned in Orca", "keep file present"):  # fmt: skip
-        assert words in text, words
-
-
-# -- rule 6: terminals, the save state, the dry run -------------------------------------------------
-
-
-def test_a_process_inside_with_orca_terminals_open_passes_rule_6_with_the_note(
-    wc, good
-):
-    inside = wc.ProcScan(True, ((7, "/w/wts/topic", "claude"),))
-    inp = dataclasses.replace(good, procs=inside, orca=orca(wc, live_terminal_count=2))
-    d = wc.decide(inp)
-    assert (
-        d.decision == "removable"
-        and d.note == "its Orca terminals will be closed first"
-    )
-    # the same process without an Orca terminal fails rule 6
-    d = wc.decide(
-        dataclasses.replace(good, procs=inside, orca=orca(wc, live_terminal_count=0))
-    )
-    assert (d.decision, d.rule, d.reason) == ("kept", 6, "in use: process 7 (claude)")
-    d = wc.decide(dataclasses.replace(good, procs=inside, orca=None))
-    assert (d.rule, d.reason) == (6, "in use: process 7 (claude)")
-    # terminals but no process: still the note
-    d = wc.decide(dataclasses.replace(good, orca=orca(wc, live_terminal_count=1)))
-    assert d.decision == "removable" and d.note == wc.TERMINALS_NOTE
-    # terminals do not excuse another checkout or an operation, or a failed scan
-    busy = with_facts(wc, good, operations=["index.lock"])
-    assert (
-        wc.decide(
-            dataclasses.replace(
-                busy, procs=inside, orca=orca(wc, live_terminal_count=2)
-            )
-        ).rule
-        == 6
-    )
-    failed = wc.ProcScan(False, failure="x")
-    assert (
-        wc.decide(
-            dataclasses.replace(
-                good, procs=failed, orca=orca(wc, live_terminal_count=2)
-            )
-        ).rule
-        == 6
-    )
-
-
-def test_a_process_in_a_sibling_folder_is_not_inside(wc, good):
-    near = wc.ProcScan(True, ((7, "/w/wts/topic-2", "x"),))
-    assert wc.decide(dataclasses.replace(good, procs=near)).decision == "removable"
-
-
-@pytest.mark.parametrize(
-    "files,save,decision,cell",
-    [
-        ({}, "not needed", "removable", "none needed"),
-        ({"untracked_dev": [".dev/a"]}, "needed", "removable", "needed"),
-        ({"ignored_dev": [".dev/a"]}, "verified", "removable", "saved and checked"),
-        ({"untracked_dev": [".dev/a"]}, "failed: copy differs", "kept", "failed"),
-    ],
-)
-def test_dev_files_need_a_verified_save_and_the_dry_run_shows_needed(
-    wc, good, files, save, decision, cell
-):
-    inp = dataclasses.replace(
-        with_facts(wc, good, state=state(wc, **files)), save_state=save
-    )
-    d = wc.decide(inp)
-    assert (d.decision, d.saved_copy) == (decision, cell)
-
-
-def test_a_failed_rule_before_the_save_still_shows_the_saved_copy_cell(wc, good):
-    inp = dataclasses.replace(
-        with_facts(wc, good, state=state(wc, untracked_dev=[".dev/a"])),
-        pr_lookup=wc.PrLookup(True, None),
-        save_state="needed",
-    )
-    d = wc.decide(inp)
-    assert d.rule == 2 and d.saved_copy == "needed"
-
-
-# -- the table -----------------------------------------------------------------------------------------
-
-
-def make_rows(wc, good):
-    inp_a = dataclasses.replace(good, orca=orca(wc, live_terminal_count=1))
-    inp_b = dataclasses.replace(good, own_folder=True)
-    rows = [wc.table_row(i, wc.decide(i), "IronClaude") for i in (inp_a, inp_b)]
-    return rows
-
-
-def test_the_markdown_table_has_the_eleven_columns_and_the_json_the_same_rows(wc, good):
-    rows = make_rows(wc, good)
-    assert len(wc.TABLE_COLUMNS) == 11
-    md = wc.render_markdown(rows).splitlines()
-    assert (
-        md[0]
-        == "| repo | folder | branch | in orca | pull request | issues | idle days | size | saved copy | decision | reason |"
-    )
-    assert md[1] == "|" + "|".join(["---"] * 11) + "|"
-    assert len(md) == 2 + len(rows)
-    for line, row in zip(md[2:], rows):
-        assert line.count(" | ") == 10
-        assert row["decision"] in line and row["folder"] in line
-    doc = json.loads(wc.render_json(rows))
-    assert doc["columns"] == list(wc.TABLE_COLUMNS)
-    assert doc["rows"] == rows
-    assert all(set(r) == set(wc.TABLE_COLUMNS) for r in doc["rows"])
-
-
-def test_row_cells_for_a_removable_and_a_kept_worktree(wc, good):
-    a, b = make_rows(wc, good)
-    assert a == {
-        "repo": "IronClaude", "folder": "topic", "branch": "topic", "in_orca": "yes",
-        "pull_request": "#9 MERGED", "issues": "none found", "idle_days": "20.0", "size": "3.0 MB",
-        "saved_copy": "none needed", "decision": "removable", "reason": "its Orca terminals will be closed first",
-    }  # fmt: skip
-    assert (
-        b["decision"] == "kept"
-        and b["reason"] == "this is where the script runs"
-        and b["in_orca"] == "no"
-    )
-
-
-def test_row_cells_for_failed_lookups_and_unknowns(wc, good):
-    inp = dataclasses.replace(
-        with_facts(
-            wc,
-            good,
-            size_bytes=None,
-            git_file_mtime=None,
-            last_commit_ts=None,
-            worktree=dataclasses.replace(
-                good.facts.worktree, detached=True, branch=None
-            ),
-        ),
-        pr_lookup=wc.PrLookup(False, None, "x"),
-        issues=wc.IssueFacts(
-            (wc.Issue("o/r", 4, "CLOSED", ()),), ("issue lookup failed: o/r#5",)
-        ),
-    )
-    row = wc.table_row(inp, wc.decide(inp))
-    assert (
-        row["pull_request"],
-        row["issues"],
-        row["idle_days"],
-        row["size"],
-        row["branch"],
-    ) == (
-        "lookup failed",
-        "#4 CLOSED, lookup failed",
-        "?",
-        "?",
-        "(detached)",
-    )
-    assert row["repo"] == "main"
-    none = dataclasses.replace(inp, pr_lookup=wc.PrLookup(True, None), issues=None)
-    assert wc.table_row(none, wc.decide(none))["issues"] == "lookup failed"
-    assert wc.table_row(none, wc.decide(none))["pull_request"] == "none"
-
-
-def test_markdown_cells_never_break_the_table(wc, good):
-    row = dict(make_rows(wc, good)[0], reason="a | b\nc")
-    line = wc.render_markdown([row]).splitlines()[2]
-    assert line.count("|") == 12 and "\n" not in line.strip()
-    assert wc.render_markdown([]).count("\n") == 2
-
-
-@pytest.mark.parametrize(
-    "size,text",
-    [
-        (None, "?"),
-        (0, "0 B"),
-        (1023, "1023 B"),
-        (1536, "1.5 KB"),
-        (5 * 1024**3, "5.0 GB"),
-        (3000 * 1024**3, "3000.0 GB"),
-    ],
-)
-def test_size_text(wc, size, text):
-    assert wc._size_text(size) == text


Codegraph context: index_state=fresh checked_at=2026-11-20T18:23:04Z worktree_root=/home/coder/workspaces/worktrees/IronClaude/issue-687 projectPath=/home/coder/workspaces/worktrees/IronClaude/issue-687
call codegraph only when index_state: fresh, never to widen scope
Q2b ran on the Grep and Read floor for dependents of changed symbols (this task creates new files or edits registration lists; see the diff).

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

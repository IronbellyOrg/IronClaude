5356848cd02421cf5ba8b5a3e840f3bd3dcaf083
Review one task for spec compliance.

Task brief: ## Task 2: Test the poll payload shape with a stubbed `gh`

Depends on: Task 1

Satisfies: R-012 (part a).

Add tests to `tests/pr_submit/test_conflict_scripts.py` in the `poll-ci-checks.sh` section after the `--evidence-sha` tests, reusing `make_repos`, `Repos` and `ProbeRun`. Name every new test function with `poll` in its name.

- Add new helpers named `install_pr_poll_gh_stub` and `run_pr_poll` (do not reuse or shadow `install_ci_gh_stub` and `run_evidence_poll`, which carry evidence-mode semantics for the C1 to C4 tests); the module-level skip of `test_conflict_scripts.py` applies to the new tests. `install_pr_poll_gh_stub` installs a recording `gh` stub serving `pr checks --repo <R> --help` (prints a line containing `--json`), `pr view <N> --repo <R> --json ...` (a counter file in the stub directory makes the first and second call return the content of two different environment variables, and a value `FAIL` makes that call exit 1), and `pr checks <N> --repo <R> [--required] --json ...` (prints environment values); any other call exits 1.
- Table-driven cases for the `merge_state` value: `CONFLICTING`/`DIRTY`, `MERGEABLE`/`CLEAN`, `MERGEABLE`/`BEHIND`, `UNKNOWN`/`UNKNOWN`, fields missing from the view JSON, and a failing first `gh pr view`.
- One case with different `headRefOid` values in the two views: `state` is `polling` and `merge_state` comes from the second view.
- One case asserting the key order of the printed object.

Acceptance criteria (ids):
T2.AC1: `uv run pytest tests/pr_submit/test_conflict_scripts.py -q -k poll` passes and runs at least the six value cases, the changed-head case and the key-order case.
T2.AC2: Running the new tests once against a temporary copy of the script without `merge_state` in its final `jq` expression fails them (checked by hand, the copy is not kept).
T2.AC3: The existing C1 to C4 evidence tests and `test_poll_ci_evidence_mode_static_rules` still pass unchanged.
Global constraints: 
- Edit canonical sources under `src/superclaude/` only, then run `make sync-dev`; the `.claude/` mirrors are generated and are never staged.
- Use `uv run ...` for every Python and pytest call; no bare `python` or `pip`.
- `src/superclaude/pr_submit/fsm.py`, `run_log.py`, `models.py` and `ci.py` are not edited, no new `EventType` is added and every existing push-safety rule stays as it is (R-003, R-004).
- `src/superclaude/pr_submit/conflicts.py` and `src/superclaude/skills/sc-pr-submit-protocol/refs/state-machine.md` are in the core-pure file set of `tests/pr_submit/test_static_grep.py`: neither may contain the standalone words `gh` or `git` on any line, comments and docstrings included.
- Several tests pin exact lines of the files this plan edits: `tests/skills/test_worker_contract.py` (an inventory keyed by exact file line, with a stale-entry check), `tests/pr_submit/test_conflict_sync_protocol.py` (fragments E1 to E13, order pins) and `tests/pr_submit/test_static_grep.py`. Each task that changes a pinned line updates the pin in the same task. The router outcomes any prose describes are the table in R-005 of `./source.md`, which `_WAVE8A_ROWS` in `tests/pr_submit/test_conflicts_core.py` already pins, so no router row is added anywhere in this plan.
- Every new prose deliverable gets its own positive assertion scoped to that text (R-012 part d), so that removing only that text fails exactly that assertion.
- Non-goal: the go/no-go gate of the issue (one real run where the base moved, or a maintainer waiver) is a release sign-off item and stays open (R-014). Nothing in this plan runs against a real PR.
- Non-goal: `.dev/brainstorms/issue-305-pr-submit-conflict-resolution/merged-requirements.md` and `.dev/designs/issue-305-pr-submit-conflict-resolution/DESIGN.md` are historical records and are not edited.
- Owner authorization (2026-11-07, relayed by the coordinator): after the third advisory review left two word-level blocking findings (the "unconditional" end-of-wait re-read in R-010 and Task 7, and the over-general status bullet in R-005), the owner allowed word edits to `./source.md` and this plan, with the listed minor guardrails, and no fourth review. The corrections are in R-005, R-010, Task 7 and the guardrails of Tasks 1, 2, 6, 7, 9 and 10; the report is `.dev/reflect/pre-TASK-WF-p3Requirements-20261107-070713-20261107070932/REPORT.md`.
Start sha: 5356848cd02421cf5ba8b5a3e840f3bd3dcaf083
Diff against the start snapshot: 
diff --git a/tests/pr_submit/test_conflict_scripts.py b/tests/pr_submit/test_conflict_scripts.py
index b54f8329..4e66247c 100644
--- a/tests/pr_submit/test_conflict_scripts.py
+++ b/tests/pr_submit/test_conflict_scripts.py
@@ -1826,3 +1826,135 @@ def test_poll_ci_evidence_mode_static_rules():
     assert text.index('if [ "$EVIDENCE_MODE" -eq 1 ]; then') < text.index(
         "gh pr checks --repo"
     )
+
+
+# ---------------------------------------------------------------------------
+# poll-ci-checks.sh --pr mode: the merge_state key (issue #361, FR-25)
+# ---------------------------------------------------------------------------
+
+PR_POLL_REPO = "IronbellyOrg/IronClaude"
+PR_POLL_KEYS = ["pr", "head_sha", "source", "state", "checks", "merge_state"]
+
+
+def install_pr_poll_gh_stub(repos: Repos) -> None:
+    """Recording `gh` stub for `poll-ci-checks.sh --pr` (not for evidence mode).
+
+    The first `pr view` prints ``$GH_VIEW_1`` and every later one ``$GH_VIEW_2``
+    (a counter file keeps the count); the value ``FAIL`` makes that call exit 1.
+    ``pr checks`` prints ``$GH_CHECKS`` (default ``[]``) and answers ``--help``
+    with a line holding ``--json``. Any other call exits 1."""
+    counter = repos.bin_dir / "gh-view-count"
+    stub = repos.bin_dir / "gh"
+    stub.write_text(
+        "#!/usr/bin/env bash\n"
+        f"printf '%s\\n' \"$*\" >> '{repos.gh_calls}'\n"
+        'case "$1 $2" in\n'
+        '  "pr checks")\n'
+        '    case " $* " in\n'
+        "      *\" --help \"*) printf '  --json  fields\\n'; exit 0 ;;\n"
+        "    esac\n"
+        "    printf '%s\\n' \"${GH_CHECKS:-[]}\"; exit 0 ;;\n"
+        '  "pr view")\n'
+        f"    n=$(cat '{counter}' 2>/dev/null || echo 0); n=$((n + 1)); printf '%s' \"$n\" > '{counter}'\n"
+        '    if [ "$n" -eq 1 ]; then out="$GH_VIEW_1"; else out="$GH_VIEW_2"; fi\n'
+        '    if [ "$out" = FAIL ]; then printf "HTTP 502\\n" >&2; exit 1; fi\n'
+        "    printf '%s\\n' \"$out\"; exit 0 ;;\n"
+        "  *) printf 'unexpected gh call: %s\\n' \"$*\" >&2; exit 1 ;;\n"
+        "esac\n",
+        encoding="utf-8",
+    )
+    stub.chmod(0o755)
+
+
+def run_pr_poll(repos: Repos, view_1: str, view_2: str | None = None) -> ProbeRun:
+    """Run `poll-ci-checks.sh --pr 7 --repo ...` against the stub; `view_2` defaults
+    to `view_1` (the re-sample after the checks)."""
+    install_pr_poll_gh_stub(repos)
+    env = {
+        **repos.env,
+        "GH_VIEW_1": view_1,
+        "GH_VIEW_2": view_1 if view_2 is None else view_2,
+    }
+    res = subprocess.run(
+        [str(POLL_CI), "--pr", "7", "--repo", PR_POLL_REPO],
+        cwd=repos.work,
+        env=env,
+        text=True,
+        capture_output=True,
+        timeout=60,
+    )
+    return ProbeRun(res.returncode, res.stdout, res.stderr)
+
+
+def _pr_view(sha: str = "a" * 40, **fields: str) -> str:
+    return json.dumps(
+        {"number": 7, "url": "https://example.test/pull/7", "headRefOid": sha, **fields}
+    )
+
+
+@pytest.mark.parametrize(
+    ("fields", "expected"),
+    [
+        (
+            {"mergeable": "CONFLICTING", "mergeStateStatus": "DIRTY"},
+            {"mergeable": "CONFLICTING", "status": "DIRTY"},
+        ),
+        (
+            {"mergeable": "MERGEABLE", "mergeStateStatus": "CLEAN"},
+            {"mergeable": "MERGEABLE", "status": "CLEAN"},
+        ),
+        (
+            {"mergeable": "MERGEABLE", "mergeStateStatus": "BEHIND"},
+            {"mergeable": "MERGEABLE", "status": "BEHIND"},
+        ),
+        (
+            {"mergeable": "UNKNOWN", "mergeStateStatus": "UNKNOWN"},
+            {"mergeable": "UNKNOWN", "status": "UNKNOWN"},
+        ),
+        ({}, {"mergeable": "", "status": ""}),  # fields missing from the view JSON
+    ],
+)
+def test_poll_pr_mode_reports_merge_state(tmp_path, fields, expected):
+    repos = make_repos(tmp_path)
+    payload = run_pr_poll(repos, _pr_view(**fields)).payload
+    assert payload["merge_state"] == expected
+    assert payload["pr"] == 7 and payload["head_sha"] == "a" * 40
+    # Only the pr-mode reads ran: the probe, two views and two check queries.
+    calls = repos.gh_call_lines()
+    assert sum(line.startswith("pr view 7 --repo ") for line in calls) == 2
+    assert all(f"--repo {PR_POLL_REPO}" in line for line in calls)
+
+
+def test_poll_pr_mode_first_view_failing_gives_empty_merge_state(tmp_path):
+    repos = make_repos(tmp_path)
+    res = run_pr_poll(repos, "FAIL", _pr_view(mergeable="CONFLICTING"))
+    assert res.returncode == 0, res.stderr
+    assert res.payload == {
+        "pr": 7,
+        "head_sha": "",
+        "source": "ci",
+        "state": "polling",
+        "checks": [],
+        "merge_state": {"mergeable": "", "status": ""},
+    }
+
+
+def test_poll_pr_mode_changed_head_is_polling_and_merge_state_is_from_second_view(
+    tmp_path,
+):
+    repos = make_repos(tmp_path)
+    first = _pr_view("a" * 40, mergeable="MERGEABLE", mergeStateStatus="CLEAN")
+    second = _pr_view("b" * 40, mergeable="CONFLICTING", mergeStateStatus="DIRTY")
+    payload = run_pr_poll(repos, first, second).payload
+    assert payload["state"] == "polling"
+    assert payload["head_sha"] == "b" * 40
+    assert payload["merge_state"] == {"mergeable": "CONFLICTING", "status": "DIRTY"}
+
+
+def test_poll_pr_mode_key_order_appends_merge_state_after_checks(tmp_path):
+    repos = make_repos(tmp_path)
+    payload = run_pr_poll(
+        repos, _pr_view(mergeable="MERGEABLE", mergeStateStatus="CLEAN")
+    ).payload
+    assert list(payload) == PR_POLL_KEYS
+    assert list(payload["merge_state"]) == ["mergeable", "status"]

Delta diff from the previous reviewed tree (empty on the first review): 
diff --git a/tests/pr_submit/test_conflict_scripts.py b/tests/pr_submit/test_conflict_scripts.py
index ca2b5743..4e66247c 100644
--- a/tests/pr_submit/test_conflict_scripts.py
+++ b/tests/pr_submit/test_conflict_scripts.py
@@ -1843,7 +1843,7 @@ def install_pr_poll_gh_stub(repos: Repos) -> None:
     (a counter file keeps the count); the value ``FAIL`` makes that call exit 1.
     ``pr checks`` prints ``$GH_CHECKS`` (default ``[]``) and answers ``--help``
     with a line holding ``--json``. Any other call exits 1."""
-    counter = repos.root / "gh-view-count"
+    counter = repos.bin_dir / "gh-view-count"
     stub = repos.bin_dir / "gh"
     stub.write_text(
         "#!/usr/bin/env bash\n"

Earlier blocking findings of this start (empty on the first review): 
F1.1 sev=blocking trigger=B4 ac=scope at=tests/pr_submit/test_conflict_scripts.py:57 anchor="a counter file in the stub directory" chk=amiss:n,false:n,harm:n,constraint:y family=stub-counter-location fix=put the counter at repos.bin_dir / "gh-view-count" first=A1 origin=new: the counter file is created in repos.root, the parent of the stub directory (repos.bin_dir); the task says the counter file is in the stub directory
Saved-probe re-check hit locations (may be empty): 
1846:    counter = repos.bin_dir / "gh-view-count"

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

8e4667e2419dc2677c6bc0aca262ed00b2e7319e
Review one task for spec compliance.

Task brief: ## Task 11: Generalise the script wording and test reply-resolve on a Codex thread

Depends on: Task 10

Edit the header comments and messages of src/superclaude/skills/sc-pr-submit-protocol/scripts/reply-resolve-thread.sh, retrigger-review.sh and poll-augment-review.sh to name review findings from Augment or Codex instead of Augment only (design sections 10 and 11; logic, arguments, exit codes and file names unchanged; the retrigger default body stays "auggie review"). Add to tests/pr_submit/test_codex_reviews.py a test that runs reply-resolve-thread.sh against a fake `gh` on PATH (the adapter pattern in tests/pr_submit/test_cosmos_poll.py) with a Codex-rooted thread, and a test that retrigger-review.sh posts the given `--body "@codex review"`.

Acceptance criteria:
- The reply-resolve test shows the reply POST to the Codex root comment id followed by the resolveReviewThread mutation on that thread id; an already resolved Codex thread is skipped without a reply.
- tests/pr_submit/test_cosmos_poll.py, test_static_grep.py, test_review_retrigger.py and test_edge_cases.py still pass.
Global constraints: 
- The design file .dev/pr-submit-codex/design/pr-submit-codex-design.md is the specification; do not add behaviour it does not describe.
- Keep the deterministic core src/superclaude/pr_submit/ free of gh and git command tokens (NFR-6, checked by tests/pr_submit/test_static_grep.py).
- Augment-only behaviour must stay identical apart from the added reviewer_absent event and reviewer fields (design sections 5 and 6); existing tests in tests/pr_submit/ keep passing.
- Never hardcode src/superclaude/ paths inside installed primitives (command, skill, refs, scripts); keep script file names unchanged.
- plugins/superclaude/ has no pr-submit twin (design section 3), so no mirror edit is needed; do not create one.
- Edit src/superclaude/ only, then run make sync-dev; never edit or stage .claude/ copies.
- Run pytest only on named files or tests/pr_submit, never the full suite or tests/cli/eval/ as a directory; use uv run.
- .dev/tasks/ is always staged (git add .dev/tasks), including this package and its artifacts/.
Start sha: 8e4667e2419dc2677c6bc0aca262ed00b2e7319e
Diff against the start snapshot: diff --git a/src/superclaude/skills/sc-pr-submit-protocol/scripts/reply-resolve-thread.sh b/src/superclaude/skills/sc-pr-submit-protocol/scripts/reply-resolve-thread.sh
index 5c0a379f..e28728b3 100755
--- a/src/superclaude/skills/sc-pr-submit-protocol/scripts/reply-resolve-thread.sh
+++ b/src/superclaude/skills/sc-pr-submit-protocol/scripts/reply-resolve-thread.sh
@@ -2,8 +2,9 @@
 #
 # reply-resolve-thread.sh — C4 reply + resolve wrapper for sc:pr-submit.
 #
-# Purpose : Post a REST reply on an Augment finding's review-comment thread, THEN
-#           resolve that thread via the GraphQL resolveReviewThread mutation.
+# Purpose : Post a REST reply on a review finding's comment thread (an Augment or
+#           Codex root; the thread is found by its root comment id, never by author),
+#           THEN resolve that thread via the GraphQL resolveReviewThread mutation.
 #           Reply FIRST, then resolve (FR-6.1 → FR-6.2). A thread already resolved
 #           is skipped (idempotency).
 # Usage   : reply-resolve-thread.sh --pr <N> --comment-id <ID> --body-file <path>
diff --git a/src/superclaude/skills/sc-pr-submit-protocol/scripts/retrigger-review.sh b/src/superclaude/skills/sc-pr-submit-protocol/scripts/retrigger-review.sh
index b2f0af3a..b28e10f5 100755
--- a/src/superclaude/skills/sc-pr-submit-protocol/scripts/retrigger-review.sh
+++ b/src/superclaude/skills/sc-pr-submit-protocol/scripts/retrigger-review.sh
@@ -2,10 +2,12 @@
 #
 # retrigger-review.sh — S5a re-trigger wrapper for sc:pr-submit (R1 / FR-8).
 #
-# Purpose : Post one `auggie review` re-trigger comment on the PR's conversation
-#           thread so the Augment App performs a re-review of the just-pushed
-#           remediation commit. A push does NOT auto-trigger an Augment re-review —
-#           the App reviews only on PR-open or an explicit operator trigger comment.
+# Purpose : Post one re-trigger comment on the PR's conversation thread so a
+#           reviewer re-reviews the just-pushed remediation commit: `auggie review`
+#           (the default) for Augment, `--body "@codex review"` for Codex. The SKILL
+#           calls this once per present reviewer. A push does NOT auto-trigger a
+#           re-review by either bot; each reviews only on PR-open or an explicit
+#           trigger comment.
 # Usage   : retrigger-review.sh --pr <N> [--repo <owner/repo>] [--body <phrase>]
 # Exit    : 0 on a completed post; 2 on usage error (bad/missing/non-numeric --pr);
 #           127 on a missing dependency (gh not on PATH — an environment failure, NOT
@@ -49,7 +51,8 @@ REPO="${REPO:-$(git remote get-url origin 2>/dev/null | sed -E 's#^ssh://[^/]+/#
 [ -n "$REPO" ] || die "could not resolve target repo (pass --repo <owner/repo>)" 2
 
 # Post the re-trigger comment on the PR conversation thread (issue-comment surface).
-# Default body is `auggie review` (S5a). Silence path passes --body "augment review".
+# Default body is `auggie review` (S5a). Codex passes --body "@codex review".
+# Silence path (Augment only) passes --body "augment review".
 gh api --method POST \
     "repos/${REPO}/issues/${PR}/comments" \
     -f body="$BODY" >/dev/null \
diff --git a/src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-augment-review.sh b/src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-augment-review.sh
index 514b76b7..7881de0e 100755
--- a/src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-augment-review.sh
+++ b/src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-augment-review.sh
@@ -1,5 +1,7 @@
 #!/usr/bin/env bash
-# Single repo-pinned poll; raw payloads stay in files (large reviews exceed ARG_MAX).
+# Single repo-pinned poll of every review surface (reviews, issue + inline comments,
+# review threads); one snapshot serves both reviewers, Augment and Codex.
+# Raw payloads stay in files (large reviews exceed ARG_MAX).
 # Classification/backoff belong to superclaude.pr_submit, not this adapter.
 set -euo pipefail
 
--- a/tests/pr_submit/test_codex_reviews.py
+++ b/tests/pr_submit/test_codex_reviews.py
@@ -11,6 +11,9 @@
 
 import copy
 import json
+import os
+import subprocess
+from pathlib import Path
 
 import pytest
 
@@ -34,6 +37,7 @@
     parse_codex_priority,
     pending_retriggers,
     remap_severity,
+    retrigger_phrase,
     reviewer_activity,
     route,
 )
@@ -477,3 +481,171 @@
         snap = load_fixture(name)
         assert snap["reviews_ok"] and snap["comments_ok"] and snap["threads_ok"]
         assert json.loads(json.dumps(snap)) == snap
+
+
+# --- 9. shell adapters on a Codex thread (design sections 10 and 11) ---------------
+
+SCRIPTS = (
+    Path(__file__).resolve().parents[2]
+    / "src/superclaude/skills/sc-pr-submit-protocol/scripts"
+)
+FAKE_GH = r"""#!/usr/bin/env bash
+set -euo pipefail
+jq -nc --args '$ARGS.positional' -- "$@" >> "$STUB_DIR/calls.jsonl"
+field() {
+    local name="$1" arg
+    for arg in "${@:2}"; do
+        if [[ "$arg" == "$name="* ]]; then printf '%s' "${arg#*=}"; return; fi
+    done
+}
+[ "$1" = api ] || exit 92
+if [[ " $* " == *" --method POST "* ]]; then
+    target=""
+    for arg in "$@"; do [[ "$arg" == repos/* ]] && target="$arg"; done
+    case "$target" in
+        */pulls/336/comments/*/replies)
+            cid="${target%/replies}"; cid="${cid##*/}"
+            jq -nc --argjson cid "$cid" '{id:999, in_reply_to_id:$cid}' ;;
+        */issues/336/comments) printf '{"id":1}\n' ;;
+        *) exit 93 ;;
+    esac
+    exit 0
+fi
+if [ "$2" = graphql ]; then
+    query="$(field query "$@")"
+    if [[ "$query" == *'mutation('* ]]; then
+        jq -nc --arg tid "$(field threadId "$@")" \
+            '{data:{resolveReviewThread:{thread:{id:$tid, isResolved:true}}}}'
+        exit 0
+    fi
+    cat "$STUB_DIR/threads.json"
+    exit 0
+fi
+exit 99
+"""
+
+
+@pytest.fixture
+def fake_gh(tmp_path):
+    gh = tmp_path / "gh"
+    gh.write_text(FAKE_GH, encoding="utf-8")
+    gh.chmod(0o755)
+
+    def run(script, *args):
+        result = subprocess.run(
+            [str(SCRIPTS / script), *args],
+            capture_output=True,
+            text=True,
+            timeout=30,
+            env={
+                **os.environ,
+                "PATH": f"{tmp_path}:{os.environ['PATH']}",
+                "STUB_DIR": str(tmp_path),
+            },
+        )
+        calls_file = tmp_path / "calls.jsonl"
+        calls = [
+            json.loads(line)
+            for line in (
+                calls_file.read_text().splitlines() if calls_file.exists() else []
+            )
+        ]
+        return result, calls
+
+    return tmp_path, run
+
+
+def _thread_page(threads):
+    nodes = [
+        {
+            "id": t["id"],
+            "isResolved": t["isResolved"],
+            "comments": {
+                "nodes": [
+                    {
+                        "databaseId": t["comments"]["nodes"][0]["databaseId"],
+                        "replyTo": None,
+                    }
+                ]
+            },
+        }
+        for t in threads
+    ]
+    page = {"hasNextPage": False, "endCursor": "c1"}
+    return {
+        "data": {
+            "repository": {
+                "pullRequest": {"reviewThreads": {"pageInfo": page, "nodes": nodes}}
+            }
+        }
+    }
+
+
+def _write_calls(calls):
+    return [
+        call
+        for call in calls
+        if "POST" in call or any("mutation(" in arg for arg in call)
+    ]
+
+
+@pytest.mark.parametrize("resolved", [False, True])
+def test_reply_resolve_on_a_codex_thread(fake_gh, findings336, resolved):
+    tmp, run = fake_gh
+    threads = copy.deepcopy(findings336["threads"])
+    codex = next(
+        t for t in threads if t["comments"]["nodes"][0]["author"]["login"] == CODEX
+    )
+    codex["isResolved"] = resolved
+    (tmp / "threads.json").write_text(json.dumps(_thread_page(threads)))
+    (tmp / "body.txt").write_text("Fixed after verification.", encoding="utf-8")
+    root_id = str(codex["comments"]["nodes"][0]["databaseId"])
+    result, calls = run(
+        "reply-resolve-thread.sh",
+        "--pr",
+        "336",
+        "--repo",
+        "IronbellyOrg/IronClaude",
+        "--comment-id",
+        root_id,
+        "--body-file",
+        str(tmp / "body.txt"),
+    )
+    assert result.returncode == 0, result.stderr
+    writes = _write_calls(calls)
+    if resolved:
+        assert writes == []
+        assert "idempotency_skip" in result.stdout
+        return
+    assert len(writes) == 2
+    assert (
+        f"repos/IronbellyOrg/IronClaude/pulls/336/comments/{root_id}/replies"
+        in writes[0]
+    )
+    assert any("mutation(" in arg for arg in writes[1])
+    assert f"threadId={codex['id']}" in writes[1]
+    assert f"resolved thread {codex['id']}" in result.stdout
+
+
+def test_retrigger_posts_the_codex_phrase(fake_gh):
+    _, run = fake_gh
+    result, calls = run(
+        "retrigger-review.sh",
+        "--pr",
+        "336",
+        "--repo",
+        "IronbellyOrg/IronClaude",
+        "--body",
+        retrigger_phrase(CONTRACT, "codex"),
+    )
+    assert result.returncode == 0, result.stderr
+    assert calls == [
+        [
+            "api",
+            "--method",
+            "POST",
+            "repos/IronbellyOrg/IronClaude/issues/336/comments",
+            "-f",
+            "body=@codex review",
+        ]
+    ]
diff --git a/.dev/tasks/to-do/TASK-WF-implementTheDesi-20261031-182028/artifacts/t11-test.log b/.dev/tasks/to-do/TASK-WF-implementTheDesi-20261031-182028/artifacts/t11-test.log
new file mode 100644
index 00000000..9ef7d047
--- /dev/null
+++ b/.dev/tasks/to-do/TASK-WF-implementTheDesi-20261031-182028/artifacts/t11-test.log
@@ -0,0 +1,19 @@
+============================= test session starts ==============================
+platform linux -- Python 3.11.15, pytest-9.2.0, pluggy-1.7.0
+SuperClaude: 4.3.5
+benchmark: 5.3.0 (defaults: timer=time.perf_counter disable_gc=False min_rounds=5 min_time=0.000005 max_time=1.0 calibration_precision=10 warmup=False warmup_iterations=100000)
+rootdir: /home/coder/workspaces/IronClaude/.dev/worktrees/pr-submit-codex
+configfile: pyproject.toml
+plugins: superclaude-4.3.5, benchmark-5.3.0, anyio-4.15.1, cov-7.1.0
+collected 199 items
+
+tests/pr_submit/test_codex_reviews.py .................................. [ 17%]
+.....................                                                    [ 27%]
+tests/pr_submit/test_cosmos_poll.py .................................... [ 45%]
+...............................................................          [ 77%]
+tests/pr_submit/test_static_grep.py ...................                  [ 86%]
+tests/pr_submit/test_review_retrigger.py .......                         [ 90%]
+tests/pr_submit/test_edge_cases.py ...................                   [100%]
+
+============================= 199 passed in 12.79s =============================
+rc=0
diff --git a/.dev/tasks/to-do/TASK-WF-implementTheDesi-20261031-182028/artifacts/t11-syntax.log b/.dev/tasks/to-do/TASK-WF-implementTheDesi-20261031-182028/artifacts/t11-syntax.log
new file mode 100644
index 00000000..d8674602
--- /dev/null
+++ b/.dev/tasks/to-do/TASK-WF-implementTheDesi-20261031-182028/artifacts/t11-syntax.log
@@ -0,0 +1,7 @@
+syntax ok reply-resolve-thread
+syntax ok retrigger-review
+syntax ok poll-augment-review
+ .../sc-pr-submit-protocol/scripts/poll-augment-review.sh    |  4 +++-
+ .../sc-pr-submit-protocol/scripts/reply-resolve-thread.sh   |  5 +++--
+ .../sc-pr-submit-protocol/scripts/retrigger-review.sh       | 13 ++++++++-----
+ 3 files changed, 14 insertions(+), 8 deletions(-)
diff --git a/.dev/tasks/to-do/TASK-WF-implementTheDesi-20261031-182028/artifacts/t11-lint.log b/.dev/tasks/to-do/TASK-WF-implementTheDesi-20261031-182028/artifacts/t11-lint.log
new file mode 100644
index 00000000..8fb77bc7
--- /dev/null
+++ b/.dev/tasks/to-do/TASK-WF-implementTheDesi-20261031-182028/artifacts/t11-lint.log
@@ -0,0 +1,2 @@
+All checks passed!
+1 file already formatted
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

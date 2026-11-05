2e76add1ee6b4a0153235fdf73b49d093e1c8b70
Review one task for spec compliance.

Task brief: ## Task 1: Stop the L1+ create path from rebasing or halting when behind base

Implement step 1 of source section 13 in `src/superclaude/skills/sc-pr-submit-protocol/SKILL.md` and `tests/pr_submit/test_static_grep.py`:

- Apply edit E2 (STOP block at `SKILL.md:220-223`), the rebase-sentence part only of edit E5 (the replacement substring of the Wave 0 bullet at `SKILL.md:267`, without the new operation-check sentence, which Task 17 adds), the first two replacement rows of edit E12 (Error Handling row at `SKILL.md:315`: "Wrong origin / wrong-owner URL" and "Behind base branch (create path at L1+, or `--pr`)"), and edit E13 (head-binding HALT message at `SKILL.md:268`), exactly as written in source section 8.1.
- Rewrite `tests/pr_submit/test_static_grep.py:654-661` exactly as source section 12.2 specifies (keep the asserts at `:656` and `:657` verbatim; replace `:658` and `:659-661`).

Acceptance criteria:
- `SKILL.md` contains "rebase if behind `origin/<base>` only at L0", "Being behind the base branch is not a STOP at L1+", "this skill never rewrites a published branch", and no longer contains "branch (`origin/<default-branch>`) on the create path" or "needs a force-push".
- The pinned fragments "rebase if behind `origin/<base>`" and "with `--pr <N>`, at any level, do not rebase" are still present verbatim; the AC-1 sentence of the Wave 0 bullet is unchanged.
- `uv run pytest tests/pr_submit/test_static_grep.py tests/pr_submit/test_edge_cases.py -q` passes; log saved to `./artifacts/t1-tests.log`.
Global constraints: 
- The design in `./source.md` is the specification. Every section reference below (for example "source section 5.3") points into it. Where a task and the source disagree, the source wins; record the disagreement in the task's evidence.
- Never force-push, and never write a force flag after the words "git push" on any line of a `.md` or `.sh` file in `src/superclaude/skills/sc-pr-submit-protocol/` (the force-push scan in `tests/pr_submit/test_static_grep.py:758-776` covers every such file). The only push text is `git push origin <target_sha>:<HEAD_BRANCH>`; prohibitions are written in words.
- `push_parent_ok`, `evaluate_push_decision`, `push_fail_state`, `push_idempotency_key`, `needs_rebase` and every existing `transition()` edge in `src/superclaude/pr_submit/fsm.py` stay byte-identical (source section 6.1). `resolve_crash_window` in `recovery.py` keeps its signature and return value.
- T-N50: no `git` or `gh` token (regex `\bgh\b|\bgit\b`), docstrings and comments included, in `conflicts.py`, `fsm.py`, `ci.py`, `refs/state-machine.md`, `refs/loop-guard.md` and every other file in `CORE_PURE_FILES` (`tests/pr_submit/test_static_grep.py:37-51`).
- Installed primitives (`SKILL.md`, refs, scripts, `commands/pr-submit.md`) never name a `src/superclaude/` path in new text.
- Every `gh` call in new text carries `--repo "$REPO"` or a `repos/<owner/repo>/` path. Nothing contacts `SuperClaude-Org/SuperClaude_Framework`.
- Never stash, never use a hook-skipping flag, never amend, never stage everything; stage exact paths only.
- `SKILL.md` keeps exactly one python code block (`tests/pr_submit/test_cosmos_protocol.py:36`, `tests/pr_submit/test_codex_reviews.py:688`) and grows by at most 15 lines (source section 8.1).
- Edit `src/superclaude/`, then run `make sync-dev`; never stage `.claude/` paths except `.claude/settings.json`. `.dev/tasks/` is always staged (`git add .dev/tasks`), including this package and its `artifacts/`.
- Python through UV only (`uv run pytest ...`, `uv run python ...`). Run the tests each task names plus `tests/pr_submit/`, `tests/unit/test_cli_install.py` and `tests/commands/`; do not run the full suite (`make test`) or `tests/cli/eval/` as a directory (orchestrator brief; this overrides the `make test` step of source section 12.5).
- Real-git tests run only inside pytest temporary directories with a local bare repository as `origin`, a `gh` stub on `PATH`, `GIT_CONFIG_GLOBAL=/dev/null`, `GIT_CONFIG_NOSYSTEM=1`, and for real `uv` `UV_OFFLINE=1`, `UV_NO_CONFIG=1`, `UV_CACHE_DIR=<tmp>` (source section 12 preamble). No test touches the network or `~/.claude`.
- Out of scope: P3 late re-sync (#361) and the post-release verification follow-ups V1 to V8 of source section 14; they are not implemented by this plan.
- Task evidence (test logs, grep output) goes under `./artifacts/` in this package.
Start sha: 2e76add1ee6b4a0153235fdf73b49d093e1c8b70
Diff against the start snapshot: diff --git a/src/superclaude/skills/sc-pr-submit-protocol/SKILL.md b/src/superclaude/skills/sc-pr-submit-protocol/SKILL.md
index 240d1308..7f6212f2 100644
--- a/src/superclaude/skills/sc-pr-submit-protocol/SKILL.md
+++ b/src/superclaude/skills/sc-pr-submit-protocol/SKILL.md
@@ -218,9 +218,9 @@ Existing grounding rejects a null current line; it cannot authorize an automatic
 | `--resume <abs-run-log-path>` | No | Reconstruct state from JSONL (§12). |
 
 **STOP** if `--monitor >= 1` and the PR cannot be confirmed on the resolved target repo (origin's
-`owner/repo`, parsed from `git remote get-url origin`): a wrong origin, a branch behind the base
-branch (`origin/<default-branch>`) on the create path, or a returned URL whose `owner/repo` ≠ the resolved target → HALT,
-instruct the operator to close the misrouted PR.
+`owner/repo`, parsed from `git remote get-url origin`): a wrong origin, or a returned URL whose `owner/repo` ≠ the resolved target → HALT,
+instruct the operator to close the misrouted PR. Being behind the base branch is not a STOP at L1+:
+Wave 0 reports how many commits behind (Tier 0) and the conflict check below classifies any conflict.
 
 **STOP (CI-wait preflight)** before opening a PR with `--monitor >= 1` or attaching to an existing PR,
 unless both hold: (1) `gh pr checks --repo "$REPO" --help` lists `--json` (probe the installed CLI;
@@ -264,8 +264,8 @@ Wave 7: Loop / terminate          ← loads refs/loop-guard.md
 Wave 8: CI wait (after Augment clean / REPORT_ONLY / HALT_MAX_ROUNDS / TERMINAL_AUGMENT_NO_RESPONSE) ← loads refs/ci-poll.md
 ```
 
-- **Wave 0 (all ordinals):** resolve the target repo once from the origin remote (`REPO="$(git remote get-url origin | sed -E 's#^ssh://[^/]+/##; s#^git@[^:]+:##; s#^https?://[^/]+/##; s#\.git$##')"`; only if origin has no URL, fall back to `gh repo view --json nameWithOwner -q .nameWithOwner` — never prefer it, because gh picks an `upstream` remote over `origin`) and the base branch (`gh repo view "$REPO" --json defaultBranchRef -q .defaultBranchRef.name`, overridable via `--base`). BEFORE creating anything: confirm `git remote -v` shows origin = `$REPO` and rebase if behind `origin/<base>` (with `--pr <N>`, at any level, do not rebase: the PR head is already published, so report how many commits it is behind instead). Then open the PR with `gh pr create --repo "$REPO" --base <base> --head <head> --title "..." --body "..."` and verify the returned URL's `owner/repo` equals `$REPO` (a misroute → HALT). With `--pr <N>`, skip `gh pr create` and attach to that PR instead, checking the URL from `gh pr view <N> --repo "$REPO" --json url`. Pass `--repo "$REPO"` to every poll/reply/retrigger script too. At **L0 (`--monitor 0`)** the FSM never leaves `S0_IDLE` — open the PR and return, byte-for-byte identical to today (AC-1).
-- **Wave 0 head binding (L1+ only; L0 skips it):** after `gh pr create`, or on `--pr <N>` attach, read the PR head with `gh pr view <N> --repo "$REPO" --json headRefName,headRefOid,isCrossRepository` (a failed or unparsable read → HALT) and the checkout with `git branch --show-current` and `git rev-parse HEAD`. Require `superclaude.pr_submit.fsm.pr_head_ok(local_branch, local_sha, headRefName, headRefOid, isCrossRepository, allow_cross_repo=(ordinal < 3))`; a head on a fork is allowed only below L3, where nothing is pushed. False → HALT before Wave 1 with status `terminal_halted`, reason `pr_head_mismatch` (appended to the run-log when one exists), and tell the operator: "PR #<N>'s head `<headRefName>`@<headRefOid> does not match your checkout `<local_branch>`@<local_sha>. Do not close the PR. Check out `<headRefName>` and make it equal the PR head (push if you are ahead; a branch Wave 0 rebased needs a force-push, which this skill never does for you; `git pull --ff-only` if you are behind), then re-run with `--pr <N>`." True → bind `HEAD_BRANCH := headRefName` and `pre_push_sha := headRefOid` for the whole run; every push targets `HEAD_BRANCH`, never the checkout's branch name. `--resume` repeats this binding against the live PR: when crash recovery finds a dangling `push_initiated`, check only the branch (`pr_branch_ok(local_branch, headRefName, isCrossRepository, allow_cross_repo=(ordinal < 3))` and `pr_branch_ok(<the record's target_branch>, headRefName, False)`), leave the SHA to `resolve_crash_window` (local HEAD may already be the fix commit), and set `pre_push_sha` from that record: its `target_sha` when the push landed (Branch A), its `pre_push_sha` when the push is re-driven (Branch B: skip the Wave 6 fix commit, set `target_sha` from the record, and the re-driven push first runs the Wave 6 pre-push head guard with the record's `pre_push_sha`; after Branch A, the guard's parent check stops the next push if local commits were made since the landed push); otherwise require the full `pr_head_ok` and set `pre_push_sha := headRefOid`.
+- **Wave 0 (all ordinals):** resolve the target repo once from the origin remote (`REPO="$(git remote get-url origin | sed -E 's#^ssh://[^/]+/##; s#^git@[^:]+:##; s#^https?://[^/]+/##; s#\.git$##')"`; only if origin has no URL, fall back to `gh repo view --json nameWithOwner -q .nameWithOwner` — never prefer it, because gh picks an `upstream` remote over `origin`) and the base branch (`gh repo view "$REPO" --json defaultBranchRef -q .defaultBranchRef.name`, overridable via `--base`). BEFORE creating anything: confirm `git remote -v` shows origin = `$REPO` and rebase if behind `origin/<base>` only at L0 (at L1+ the create path does not rebase and does not halt: the branch is already published when `gh pr create` runs, so report how many commits it is behind, a Tier 0 result; with `--pr <N>`, at any level, do not rebase: the PR head is already published, so report how many commits it is behind instead). Then open the PR with `gh pr create --repo "$REPO" --base <base> --head <head> --title "..." --body "..."` and verify the returned URL's `owner/repo` equals `$REPO` (a misroute → HALT). With `--pr <N>`, skip `gh pr create` and attach to that PR instead, checking the URL from `gh pr view <N> --repo "$REPO" --json url`. Pass `--repo "$REPO"` to every poll/reply/retrigger script too. At **L0 (`--monitor 0`)** the FSM never leaves `S0_IDLE` — open the PR and return, byte-for-byte identical to today (AC-1).
+- **Wave 0 head binding (L1+ only; L0 skips it):** after `gh pr create`, or on `--pr <N>` attach, read the PR head with `gh pr view <N> --repo "$REPO" --json headRefName,headRefOid,isCrossRepository` (a failed or unparsable read → HALT) and the checkout with `git branch --show-current` and `git rev-parse HEAD`. Require `superclaude.pr_submit.fsm.pr_head_ok(local_branch, local_sha, headRefName, headRefOid, isCrossRepository, allow_cross_repo=(ordinal < 3))`; a head on a fork is allowed only below L3, where nothing is pushed. False → HALT before Wave 1 with status `terminal_halted`, reason `pr_head_mismatch` (appended to the run-log when one exists), and tell the operator: "PR #<N>'s head `<headRefName>`@<headRefOid> does not match your checkout `<local_branch>`@<local_sha>. Do not close the PR. Check out `<headRefName>` and make it equal the PR head (push if you are ahead; `git pull --ff-only` if you are behind; this skill never rewrites a published branch), then re-run with `--pr <N>`." True → bind `HEAD_BRANCH := headRefName` and `pre_push_sha := headRefOid` for the whole run; every push targets `HEAD_BRANCH`, never the checkout's branch name. `--resume` repeats this binding against the live PR: when crash recovery finds a dangling `push_initiated`, check only the branch (`pr_branch_ok(local_branch, headRefName, isCrossRepository, allow_cross_repo=(ordinal < 3))` and `pr_branch_ok(<the record's target_branch>, headRefName, False)`), leave the SHA to `resolve_crash_window` (local HEAD may already be the fix commit), and set `pre_push_sha` from that record: its `target_sha` when the push landed (Branch A), its `pre_push_sha` when the push is re-driven (Branch B: skip the Wave 6 fix commit, set `target_sha` from the record, and the re-driven push first runs the Wave 6 pre-push head guard with the record's `pre_push_sha`; after Branch A, the guard's parent check stops the next push if local commits were made since the landed push); otherwise require the full `pr_head_ok` and set `pre_push_sha := headRefOid`.
 - **Wave 1 (L1+):** load the contract via `superclaude.pr_submit.DetectionContract.for_arming()` — prefers an optional operator-local override (gitignored `.dev/pr-monitor/detection-contract.locked.md`) and falls back to the SHIPPED `refs/detection-contract.md` (baked `augmentcode[bot]` / `augmentcode` defaults). A missing or unlocked override is not a halt; the contract also carries the Codex identities (`codex_bot_login`, `codex_app_slug`) and `codex_retrigger_phrase`, and Codex is disabled only when both Codex identities are blank (it stays on while either remains). Initialize the output-dir + run-log + baseline, then enter the **attended poll loop** (above) with `scripts/poll-augment-review.sh` (interval ≥30s, timeout default 600s; the one snapshot serves both reviewers); each JSON line passes the snapshot gate before any FSM outcome; incomplete evidence keeps polling. Record `reviewer_absent{reviewer}` for a reviewer the merge settles as absent, and `reviewer_incomplete{reviewer, phase: "initial"}` for a present reviewer that did not complete by `--timeout` while the other's result was used. Every event that concerns one reviewer carries a `reviewer` field (`"augment"` or `"codex"`; a missing field means `augment`): `poll_result` (with the per-reviewer wait outcomes), `review_detected`, `findings_normalized`, `finding_verified`, `finding_unverified`, `route_decision`, `reply_posted`, `thread_resolved`, `rereview_requested`. On `--resume`, read `rebuild_state()["absent_reviewers"]` and keep those reviewers absent. Arm exactly once at L1+ (T-109); never at L0 (T-110). `--monitor 0` remains no-monitor.
 - **Wave 2:** load `refs/severity-routing.md`; use only the snapshot gate's `actionable_finding_comments` → `finding_from_comment` → `remap_severity(finding)` → `route(finding)` results from `superclaude.pr_submit` (Augment's and, for Codex, `codex_finding_comments` → the same three calls; a Codex P0/P1/P2/P3 badge is its severity hint, a missing or malformed badge is the Medium fail-safe), then map the remapped tier to its troubleshoot route (Medium → `--fix`; High/Critical → `--depth deep --fix`; Low/Nit → report-only). NEVER emit `--depth quick --fix`. Group the merged findings with `dedup_groups(findings)` (same path and line, `original_line` when the line is null): a **dedup group routes at its members' highest remapped tier**; every member keeps its own finding, verdict and thread.
 - **Wave 3:** load `refs/finding-verify.md`; spawn the `evidence-validator` agent (read-only) to confirm each finding's cited file:line exists and the defect reproduces (one verdict per finding, Augment and Codex in one batch). `unverified` → REPORT_ONLY, consuming NO round. A dedup group is dispatched only when at least one member is verified. Context only, once per cycle before verification: invoke `> Skill sc:impact-protocol` with `--diff origin/<baseRefName> --depth 1 --output-dir <output-dir>/impact/wave3 --caller sc-pr-submit-protocol` and read only `status`, `degraded`, `dependents[].caller`, `dependents[].file` and `unmapped_files` from its `return-contract.yaml`; the dependent names and files are background for the verifier, never a reason to verify, drop or re-tier a finding. Copy its `degraded` tokens into the run-log; `status: blocked|failed` counts as `graph:absent`.
@@ -312,7 +312,8 @@ A validation retry does NOT increment `round_counter`.
 
 | Scenario | Behavior |
 |----------|----------|
-| Wrong origin / behind base branch (create path) / wrong-owner URL | HALT; instruct operator to close the misrouted PR (FM-11). |
+| Wrong origin / wrong-owner URL | HALT; instruct operator to close the misrouted PR (FM-11). |
+| Behind base branch (create path at L1+, or `--pr`) | Tier 0 report ("<N> commits behind"); no rebase, no halt. At L0 the create path still rebases. |
 | Checkout is not the PR head (Wave 0 head binding) or the PR head moved before a push (pre-push head guard) | `terminal_halted`, reason `pr_head_mismatch`; nothing pushed; do NOT close the PR; give the recovery steps from the HALT message. |
 | The commit to push is not exactly one commit on top of the PR head (the pre-push head guard's parent check) | `terminal_halted`, reason `push_range_mismatch`; nothing pushed; do NOT close the PR; list the other local commits and tell the operator to make the checkout equal the PR head, then re-run with `--pr <N>`. |
 | The fix touched a file with the operator's own pending changes, the fix commit fails, or HEAD does not advance (Wave 6 fix commit) | `terminal_halted`, reason `fix_commit_failed`; nothing pushed; do NOT close the PR; edits (and any hook changes) left in the working tree; never tell the operator to discard a file that holds their own changes; give the recovery steps from the HALT message. |
diff --git a/tests/pr_submit/test_static_grep.py b/tests/pr_submit/test_static_grep.py
index 7618ea9b..251905d6 100644
--- a/tests/pr_submit/test_static_grep.py
+++ b/tests/pr_submit/test_static_grep.py
@@ -651,14 +651,15 @@ def test_skill_binds_checkout_and_push_target_to_pr_head():
         "At **L0 (`--monitor 0`)** the FSM never leaves `S0_IDLE` — open the PR and "
         "return, byte-for-byte identical to today (AC-1)."
     ) in text
-    # `--pr` never rebases a published head; the create path still rebases, and only the
-    # create path halts when behind base (STOP block and Error Handling row agree).
+    # `--pr` never rebases a published head; the create path rebases only at L0; at L1+
+    # being behind is a Tier 0 report, not a STOP.
     assert "with `--pr <N>`, at any level, do not rebase" in text
     assert "rebase if behind `origin/<base>`" in text
-    assert "branch (`origin/<default-branch>`) on the create path" in text
-    assert (
-        "| Wrong origin / behind base branch (create path) / wrong-owner URL |" in text
-    )
+    assert "rebase if behind `origin/<base>` only at L0" in text
+    assert "Being behind the base branch is not a STOP at L1+" in text
+    assert "branch (`origin/<default-branch>`) on the create path" not in text
+    assert "| Wrong origin / wrong-owner URL |" in text
+    assert "| Behind base branch (create path at L1+, or `--pr`) |" in text
     assert "reason `pr_head_mismatch`; nothing pushed; do NOT close the PR" in text
 
     wave6 = text[text.index("- **Wave 6 (L3 only):**") :]
diff --git a/.dev/tasks/to-do/TASK-WF-design-20261104-164423/artifacts/t1-tests.log b/.dev/tasks/to-do/TASK-WF-design-20261104-164423/artifacts/t1-tests.log
new file mode 100644
index 00000000..54298fb3
--- /dev/null
+++ b/.dev/tasks/to-do/TASK-WF-design-20261104-164423/artifacts/t1-tests.log
@@ -0,0 +1,12 @@
+============================= test session starts ==============================
+platform linux -- Python 3.11.15, pytest-9.2.0, pluggy-1.7.0
+SuperClaude: 5.0.0
+rootdir: /home/coder/workspaces/worktrees/IronClaude/issue-305-pr-submit-conflicts
+configfile: pyproject.toml
+plugins: superclaude-5.0.0, anyio-4.16.0
+collected 38 items
+
+tests/pr_submit/test_static_grep.py ...................                  [ 50%]
+tests/pr_submit/test_edge_cases.py ...................                   [100%]
+
+============================== 38 passed in 0.58s ==============================

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

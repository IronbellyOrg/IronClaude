4ad216fa21ac453b64e5322c51f9d1b4d923ea1a
Review one task for spec compliance.

Task brief: ## Task 13: Add commit-scoped check evidence to `poll-ci-checks.sh`

Edit `src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-ci-checks.sh` per source section 7.4: accept `--evidence-sha <40hex>` (no `--pr` needed), validate it before the `gh pr checks --help` probe, read `gh api "repos/${REPO}/commits/${SHA}/check-runs?per_page=1" --jq .total_count` and the `/status` count, print `{"evidence_sha": ..., "evidence_checks": <n>, "source": "ci"}` with `n = -1` on any failed or unparsable read; extend the header comment; leave the existing poll path and the pre-existing header line `:14` unchanged. Add cases C1 to C4 of source section 12.4 to `tests/pr_submit/test_conflict_scripts.py` with a `gh` stub.

Acceptance criteria:
- C1 gives `evidence_checks: 2`, C2 gives 0, C3 gives -1, C4 exits 2; no `gh pr checks` call is made in evidence mode.
- Existing poll tests (`tests/pr_submit/test_cosmos_poll.py` and the CI poll cases in `tests/pr_submit/test_static_grep.py`) pass unmodified.
- `uv run pytest tests/pr_submit/test_conflict_scripts.py tests/pr_submit/test_cosmos_poll.py tests/pr_submit/test_static_grep.py -q` passes; log saved to `./artifacts/t13-tests.log`.
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
Start sha: 4ad216fa21ac453b64e5322c51f9d1b4d923ea1a
Diff against the start snapshot: diff --git a/src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-ci-checks.sh b/src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-ci-checks.sh
old mode 100644
new mode 100755
index febae411..340101ea
--- a/src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-ci-checks.sh
+++ b/src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-ci-checks.sh
@@ -4,10 +4,16 @@
 #
 # Purpose : Do a SINGLE poll of a PR's checks and emit exactly ONE JSON line.
 # Usage   : poll-ci-checks.sh --pr <N> [--repo <owner/repo>]
+#           poll-ci-checks.sh --evidence-sha <40hex> [--repo <owner/repo>]
 # Output  : one line of JSON: {"pr":N,"head_sha":"...","source":"ci",
 #           "state":"polling|clean|findings","checks":[...]}
-# Exit    : 0 always on a completed poll (fail-soft); 2 on a usage error or a
-#           missing prerequisite (gh, jq, repo, or `gh pr checks --json` support).
+#           Evidence mode (no --pr needed) reads the commit's check runs and
+#           commit statuses: {"evidence_sha":"<sha>","evidence_checks":N,"source":"ci"}
+#           with N = check runs + statuses, or -1 when either read fails or does
+#           not parse (fail closed: -1 counts as "had checks").
+# Exit    : 0 always on a completed poll (fail-soft); 2 on a usage error (an
+#           invalid --evidence-sha included) or a missing prerequisite (gh, jq,
+#           repo, or `gh pr checks --json` support, which evidence mode skips).
 # Spec    : .dev/specs/pr-submit-ci-monitor.md FR-CI-2 / FR-CI-10 / FR-CI-11.
 #           Authoritative classify is superclaude.pr_submit.ci.classify_checks.
 #
@@ -19,21 +25,41 @@ die() { printf 'poll-ci-checks: %s\n' "$1" >&2; exit "${2:-1}"; }
 
 PR=""
 REPO=""
+EVIDENCE_MODE=0
+EVIDENCE_SHA=""
 while [ $# -gt 0 ]; do
     case "$1" in
         --pr) PR="${2:-}"; shift 2 ;;
         --repo) REPO="${2:-}"; shift 2 ;;
+        --evidence-sha) EVIDENCE_MODE=1; EVIDENCE_SHA="${2:-}"; shift; [ $# -eq 0 ] || shift ;;
         *) die "unknown argument: $1" 2 ;;
     esac
 done
 
-[ -n "$PR" ] || die "missing required --pr <N>" 2
+[ -n "$PR" ] || [ "$EVIDENCE_MODE" -eq 1 ] || die "missing required --pr <N>" 2
 command -v gh >/dev/null 2>&1 || die "gh CLI not found on PATH" 2
 command -v jq >/dev/null 2>&1 || die "jq not found on PATH" 2
 
 REPO="${REPO:-$(git remote get-url origin 2>/dev/null | sed -E 's#^ssh://[^/]+/##; s#^git@[^:]+:##; s#^https?://[^/]+/##; s#\.git$##' || true)}"
 [ -n "$REPO" ] || REPO="$(gh repo view --json nameWithOwner -q .nameWithOwner 2>/dev/null || true)"
 [ -n "$REPO" ] || die "could not resolve target repo (pass --repo <owner/repo>)" 2
+
+# Evidence mode: how many checks exist on one commit. Validated before the
+# `pr checks` capability probe below, which this read does not need.
+if [ "$EVIDENCE_MODE" -eq 1 ]; then
+    [[ "$EVIDENCE_SHA" =~ ^[0-9a-fA-F]{40}$ ]] \
+        || die "invalid --evidence-sha: '${EVIDENCE_SHA}' (expected 40 hex characters)" 2
+    RUNS="$(gh api "repos/${REPO}/commits/${EVIDENCE_SHA}/check-runs?per_page=1" --jq .total_count 2>/dev/null)" || RUNS=""
+    STATUSES="$(gh api "repos/${REPO}/commits/${EVIDENCE_SHA}/status" --jq .total_count 2>/dev/null)" || STATUSES=""
+    # Fail closed: a failed or unparsable read is -1, which counts as "had checks".
+    EVIDENCE_CHECKS=-1
+    if [[ "$RUNS" =~ ^[0-9]{1,9}$ ]] && [[ "$STATUSES" =~ ^[0-9]{1,9}$ ]]; then
+        EVIDENCE_CHECKS=$(( 10#$RUNS + 10#$STATUSES ))
+    fi
+    jq -nc --arg sha "$EVIDENCE_SHA" --argjson n "$EVIDENCE_CHECKS" \
+        '{evidence_sha:$sha, evidence_checks:$n, source:"ci"}'
+    exit 0
+fi
 # Probe the installed CLI, not a guessed version: without `pr checks --json` every
 # query below fails and the fail-soft path would report `polling` until timeout.
 CHECKS_HELP="$(gh pr checks --repo "$REPO" --help 2>/dev/null || true)"
diff --git a/tests/pr_submit/test_conflict_scripts.py b/tests/pr_submit/test_conflict_scripts.py
index 9f2889aa..10c8a8f2 100644
--- a/tests/pr_submit/test_conflict_scripts.py
+++ b/tests/pr_submit/test_conflict_scripts.py
@@ -2,7 +2,8 @@
 
 This module covers ``scripts/probe-merge.sh`` (cases P1 to P12),
 ``scripts/finish-merge.sh`` (cases F1 to F12) and
-``scripts/collect-conflict-evidence.sh`` (cases E1 to E4). Every git call runs
+``scripts/collect-conflict-evidence.sh`` (cases E1 to E4) and
+``scripts/poll-ci-checks.sh --evidence-sha`` (cases C1 to C4). Every git call runs
 inside a pytest temporary directory, with a local bare repository as ``origin`` and a
 ``gh`` stub first on ``PATH``. ``GIT_CONFIG_GLOBAL=/dev/null``, ``GIT_CONFIG_NOSYSTEM=1``
 and a fixed author and committer are set for every git call; ``HOME`` points into the
@@ -1430,3 +1431,157 @@ def test_evidence_script_static_rules():
     ).stdout
     if ls:  # the index entry exists once the path is staged
         assert ls.startswith("100755 "), ls
+
+
+# ---------------------------------------------------------------------------
+# poll-ci-checks.sh --evidence-sha (cases C1 to C4)
+# ---------------------------------------------------------------------------
+
+POLL_CI = SKILL_DIR / "scripts" / "poll-ci-checks.sh"
+EVIDENCE_SHA = "0123456789abcdef0123456789abcdef01234567"
+EVIDENCE_REPO = "IronbellyOrg/IronClaude"
+EVIDENCE_CALLS = [
+    f"api repos/{EVIDENCE_REPO}/commits/{EVIDENCE_SHA}/check-runs?per_page=1"
+    " --jq .total_count",
+    f"api repos/{EVIDENCE_REPO}/commits/{EVIDENCE_SHA}/status --jq .total_count",
+]
+
+
+def install_ci_gh_stub(repos: Repos) -> None:
+    """Replace the recording `gh` stub with one that also serves the two counts.
+
+    ``GH_STUB_RUNS`` and ``GH_STUB_STATUSES`` hold what each read prints (the value
+    `--jq .total_count` would yield); ``FAIL`` makes that read exit 1 with no stdout.
+    Any other call is unexpected and fails."""
+    stub = repos.bin_dir / "gh"
+    stub.write_text(
+        "#!/usr/bin/env bash\n"
+        f"printf '%s\\n' \"$*\" >> '{repos.gh_calls}'\n"
+        'case "$1 $2" in\n'
+        '  "api repos/"*"/check-runs?per_page=1") out="$GH_STUB_RUNS" ;;\n'
+        '  "api repos/"*"/status") out="$GH_STUB_STATUSES" ;;\n'
+        "  *) printf 'unexpected gh call: %s\\n' \"$*\" >&2; exit 1 ;;\n"
+        "esac\n"
+        "if [ \"$out\" = FAIL ]; then printf 'HTTP 502\\n' >&2; exit 1; fi\n"
+        "printf '%s\\n' \"$out\"\n",
+        encoding="utf-8",
+    )
+    stub.chmod(0o755)
+
+
+def run_evidence_poll(
+    repos: Repos, *args: str, runs: str = "0", statuses: str = "0"
+) -> ProbeRun:
+    """Run poll-ci-checks.sh from its source path with `--evidence-sha` and `--repo`
+    only (never `--pr`); assert evidence mode made no `gh pr checks` call."""
+    install_ci_gh_stub(repos)
+    env = {**repos.env, "GH_STUB_RUNS": runs, "GH_STUB_STATUSES": statuses}
+    res = subprocess.run(
+        [str(POLL_CI), *args],
+        cwd=repos.work,
+        env=env,
+        text=True,
+        capture_output=True,
+        timeout=60,
+    )
+    assert "--pr" not in args
+    for line in repos.gh_call_lines():
+        assert not line.startswith("pr "), f"evidence mode called gh pr: {line}"
+        assert "pr checks" not in line, line
+    return ProbeRun(res.returncode, res.stdout, res.stderr)
+
+
+def _evidence(repos: Repos, runs: str, statuses: str) -> ProbeRun:
+    return run_evidence_poll(
+        repos,
+        "--evidence-sha",
+        EVIDENCE_SHA,
+        "--repo",
+        EVIDENCE_REPO,
+        runs=runs,
+        statuses=statuses,
+    )
+
+
+def test_c1_two_check_runs_and_no_statuses_is_two(tmp_path):
+    repos = make_repos(tmp_path)
+    res = _evidence(repos, runs="2", statuses="0")
+    assert res.payload == {
+        "evidence_sha": EVIDENCE_SHA,
+        "evidence_checks": 2,
+        "source": "ci",
+    }
+    assert repos.gh_call_lines() == EVIDENCE_CALLS
+
+
+def test_c1_statuses_are_added_to_check_runs(tmp_path):
+    repos = make_repos(tmp_path)
+    res = _evidence(repos, runs="1", statuses="3")
+    assert res.payload["evidence_checks"] == 4
+
+
+def test_c2_no_check_runs_and_no_statuses_is_zero(tmp_path):
+    repos = make_repos(tmp_path)
+    res = _evidence(repos, runs="0", statuses="0")
+    assert res.payload == {
+        "evidence_sha": EVIDENCE_SHA,
+        "evidence_checks": 0,
+        "source": "ci",
+    }
+    assert repos.gh_call_lines() == EVIDENCE_CALLS
+
+
+@pytest.mark.parametrize(
+    ("runs", "statuses"),
+    [
+        ("FAIL", "0"),  # failing check-runs read
+        ("2", "FAIL"),  # failing status read
+        ("FAIL", "FAIL"),
+        ("null", "0"),  # unparsable: not a non-negative integer
+        ("2", "-1"),
+        ("", "0"),
+    ],
+)
+def test_c3_failed_or_unparsable_read_is_minus_one(tmp_path, runs, statuses):
+    repos = make_repos(tmp_path)
+    res = _evidence(repos, runs=runs, statuses=statuses)
+    assert res.payload == {
+        "evidence_sha": EVIDENCE_SHA,
+        "evidence_checks": -1,
+        "source": "ci",
+    }
+    assert repos.gh_call_lines() == EVIDENCE_CALLS
+
+
+@pytest.mark.parametrize(
+    "args",
+    [
+        ("--evidence-sha", "abc123"),
+        ("--evidence-sha", EVIDENCE_SHA + "0"),  # 41 characters
+        ("--evidence-sha", EVIDENCE_SHA[:-1] + "g"),  # 40 characters, not hex
+        ("--evidence-sha", ""),
+        ("--evidence-sha",),  # flag given without a value
+    ],
+)
+def test_c4_invalid_sha_exits_2_naming_it(tmp_path, args):
+    repos = make_repos(tmp_path)
+    res = run_evidence_poll(repos, "--repo", EVIDENCE_REPO, *args)
+    assert res.returncode == 2, res.stderr
+    assert res.stdout == ""
+    bad = args[1] if len(args) > 1 else ""
+    assert "invalid --evidence-sha" in res.stderr
+    assert f"'{bad}'" in res.stderr
+    # Rejected before any gh call: no capability probe, no api read.
+    assert repos.gh_call_lines() == []
+
+
+def test_poll_ci_evidence_mode_static_rules():
+    text = POLL_CI.read_text(encoding="utf-8")
+    assert re.search(r"(?i)force", text) is None
+    for line in text.splitlines():
+        if re.search(r"\bgh\s+api\b", line):
+            assert "repos/${REPO}/" in line, line
+    # The evidence branch exits before the `pr checks` capability probe.
+    assert text.index('if [ "$EVIDENCE_MODE" -eq 1 ]; then') < text.index(
+        "gh pr checks --repo"
+    )
diff --git a/.dev/tasks/to-do/TASK-WF-design-20261104-164423/artifacts/t13-tests.log b/.dev/tasks/to-do/TASK-WF-design-20261104-164423/artifacts/t13-tests.log
new file mode 100644
index 00000000..6658aa37
--- /dev/null
+++ b/.dev/tasks/to-do/TASK-WF-design-20261104-164423/artifacts/t13-tests.log
@@ -0,0 +1,16 @@
+============================= test session starts ==============================
+platform linux -- Python 3.11.15, pytest-9.2.0, pluggy-1.7.0
+SuperClaude: 5.0.0
+benchmark: 5.3.1 (defaults: timer=time.perf_counter disable_gc=False min_rounds=5 min_time=0.000005 max_time=1.0 calibration_precision=10 warmup=False warmup_iterations=100000)
+rootdir: /home/coder/workspaces/worktrees/IronClaude/issue-305-pr-submit-conflicts
+configfile: pyproject.toml
+plugins: superclaude-5.0.0, benchmark-5.3.1, anyio-4.16.0, cov-7.1.0
+collected 206 items
+
+tests/pr_submit/test_conflict_scripts.py ............................... [ 15%]
+.........................................................                [ 42%]
+tests/pr_submit/test_cosmos_poll.py .................................... [ 60%]
+...............................................................          [ 90%]
+tests/pr_submit/test_static_grep.py ...................                  [100%]
+
+============================= 206 passed in 25.85s =============================
diff --git a/.dev/tasks/to-do/TASK-WF-design-20261104-164423/artifacts/t13-diff.txt b/.dev/tasks/to-do/TASK-WF-design-20261104-164423/artifacts/t13-diff.txt
new file mode 100644
index 00000000..25e8665f
--- /dev/null
+++ b/.dev/tasks/to-do/TASK-WF-design-20261104-164423/artifacts/t13-diff.txt
@@ -0,0 +1,66 @@
+diff --git a/src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-ci-checks.sh b/src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-ci-checks.sh
+index febae411..340101ea 100755
+--- a/src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-ci-checks.sh
++++ b/src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-ci-checks.sh
+@@ -4,10 +4,16 @@
+ #
+ # Purpose : Do a SINGLE poll of a PR's checks and emit exactly ONE JSON line.
+ # Usage   : poll-ci-checks.sh --pr <N> [--repo <owner/repo>]
++#           poll-ci-checks.sh --evidence-sha <40hex> [--repo <owner/repo>]
+ # Output  : one line of JSON: {"pr":N,"head_sha":"...","source":"ci",
+ #           "state":"polling|clean|findings","checks":[...]}
+-# Exit    : 0 always on a completed poll (fail-soft); 2 on a usage error or a
+-#           missing prerequisite (gh, jq, repo, or `gh pr checks --json` support).
++#           Evidence mode (no --pr needed) reads the commit's check runs and
++#           commit statuses: {"evidence_sha":"<sha>","evidence_checks":N,"source":"ci"}
++#           with N = check runs + statuses, or -1 when either read fails or does
++#           not parse (fail closed: -1 counts as "had checks").
++# Exit    : 0 always on a completed poll (fail-soft); 2 on a usage error (an
++#           invalid --evidence-sha included) or a missing prerequisite (gh, jq,
++#           repo, or `gh pr checks --json` support, which evidence mode skips).
+ # Spec    : .dev/specs/pr-submit-ci-monitor.md FR-CI-2 / FR-CI-10 / FR-CI-11.
+ #           Authoritative classify is superclaude.pr_submit.ci.classify_checks.
+ #
+@@ -19,21 +25,41 @@ die() { printf 'poll-ci-checks: %s\n' "$1" >&2; exit "${2:-1}"; }
+ 
+ PR=""
+ REPO=""
++EVIDENCE_MODE=0
++EVIDENCE_SHA=""
+ while [ $# -gt 0 ]; do
+     case "$1" in
+         --pr) PR="${2:-}"; shift 2 ;;
+         --repo) REPO="${2:-}"; shift 2 ;;
++        --evidence-sha) EVIDENCE_MODE=1; EVIDENCE_SHA="${2:-}"; shift; [ $# -eq 0 ] || shift ;;
+         *) die "unknown argument: $1" 2 ;;
+     esac
+ done
+ 
+-[ -n "$PR" ] || die "missing required --pr <N>" 2
++[ -n "$PR" ] || [ "$EVIDENCE_MODE" -eq 1 ] || die "missing required --pr <N>" 2
+ command -v gh >/dev/null 2>&1 || die "gh CLI not found on PATH" 2
+ command -v jq >/dev/null 2>&1 || die "jq not found on PATH" 2
+ 
+ REPO="${REPO:-$(git remote get-url origin 2>/dev/null | sed -E 's#^ssh://[^/]+/##; s#^git@[^:]+:##; s#^https?://[^/]+/##; s#\.git$##' || true)}"
+ [ -n "$REPO" ] || REPO="$(gh repo view --json nameWithOwner -q .nameWithOwner 2>/dev/null || true)"
+ [ -n "$REPO" ] || die "could not resolve target repo (pass --repo <owner/repo>)" 2
++
++# Evidence mode: how many checks exist on one commit. Validated before the
++# `pr checks` capability probe below, which this read does not need.
++if [ "$EVIDENCE_MODE" -eq 1 ]; then
++    [[ "$EVIDENCE_SHA" =~ ^[0-9a-fA-F]{40}$ ]] \
++        || die "invalid --evidence-sha: '${EVIDENCE_SHA}' (expected 40 hex characters)" 2
++    RUNS="$(gh api "repos/${REPO}/commits/${EVIDENCE_SHA}/check-runs?per_page=1" --jq .total_count 2>/dev/null)" || RUNS=""
++    STATUSES="$(gh api "repos/${REPO}/commits/${EVIDENCE_SHA}/status" --jq .total_count 2>/dev/null)" || STATUSES=""
++    # Fail closed: a failed or unparsable read is -1, which counts as "had checks".
++    EVIDENCE_CHECKS=-1
++    if [[ "$RUNS" =~ ^[0-9]{1,9}$ ]] && [[ "$STATUSES" =~ ^[0-9]{1,9}$ ]]; then
++        EVIDENCE_CHECKS=$(( 10#$RUNS + 10#$STATUSES ))
++    fi
++    jq -nc --arg sha "$EVIDENCE_SHA" --argjson n "$EVIDENCE_CHECKS" \
++        '{evidence_sha:$sha, evidence_checks:$n, source:"ci"}'
++    exit 0
++fi
+ # Probe the installed CLI, not a guessed version: without `pr checks --json` every
+ # query below fails and the fail-soft path would report `polling` until timeout.
+ CHECKS_HELP="$(gh pr checks --repo "$REPO" --help 2>/dev/null || true)"

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

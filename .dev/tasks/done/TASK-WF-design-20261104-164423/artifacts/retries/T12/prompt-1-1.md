9e80751153c0b27eb3099db14d7a6837d800f339
Review one task for spec compliance.

Task brief: ## Task 12: Create the Tier 2 evidence collector `collect-conflict-evidence.sh`

Depends on: Task 10

Create `src/superclaude/skills/sc-pr-submit-protocol/scripts/collect-conflict-evidence.sh` (mode 100755) per source section 7.3 (ownership check, empty `--out`, the seven evidence files with the truncation marker, 60 s bound, JSON output, `EVIDENCE_FAIL` reasons). Add cases E1 to E4 of source section 12.4 to `tests/pr_submit/test_conflict_scripts.py`.

Acceptance criteria:
- E1 writes exactly `stage1`, `stage2`, `stage3`, `worktree`, `log.txt`, `diff-ours.txt`, `diff-theirs.txt`; E2 lists the missing stage; E3 writes the truncation marker and `truncated: true`; E4 gives `EVIDENCE_FAIL out_not_empty` and writes nothing.
- `uv run pytest tests/pr_submit/test_conflict_scripts.py -q` passes; log saved to `./artifacts/t12-tests.log`.
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
Start sha: 9e80751153c0b27eb3099db14d7a6837d800f339
Diff against the start snapshot: diff --git a/src/superclaude/skills/sc-pr-submit-protocol/scripts/collect-conflict-evidence.sh b/src/superclaude/skills/sc-pr-submit-protocol/scripts/collect-conflict-evidence.sh
new file mode 100755
index 00000000..181d9640
--- /dev/null
+++ b/src/superclaude/skills/sc-pr-submit-protocol/scripts/collect-conflict-evidence.sh
@@ -0,0 +1,244 @@
+#!/usr/bin/env bash
+#
+# collect-conflict-evidence.sh — Tier 2 evidence collector for sc:pr-submit conflict
+# cycles (issue #305).
+#
+# Purpose : For one conflicted path of an in-progress merge of the recorded base tip,
+#           write the evidence the session reads before it resolves the path by
+#           intent: the three stage blobs, the work-tree file with its conflict
+#           markers, the left-right log of the merge and both merge-base diffs.
+#           Tier 2 only; never run for Tier 0 or Tier 1. It is read-only toward the
+#           repository: it never changes the index, the work tree, HEAD, any ref or
+#           stored configuration. It writes only into --out (which must be missing or
+#           empty) and into a temporary directory under the git directory that is
+#           removed on exit.
+# Usage   : collect-conflict-evidence.sh --path <p> --out <dir> --base-sha <40hex>
+#                                        --merge-base <40hex> [--max-bytes 204800]
+#           <p> is relative to the top of the work tree.
+# Output  : exactly one stdout line. Success is one JSON object:
+#           {"dir":"<out>","files":["stage1",..],"missing":["stage3"],"truncated":false}
+#           Files, in this order when present: stage1, stage2, stage3, worktree,
+#           log.txt, diff-ours.txt, diff-theirs.txt. A stage the index does not list
+#           for <p> is not written and is named in "missing". Each file is cut at
+#           --max-bytes, with a last line "[sc:pr-submit: truncated at <N> bytes]".
+#           Failure is the token "EVIDENCE_FAIL <reason>"; details go to stderr.
+# Exit    : 0 on success; 2 with EVIDENCE_FAIL usage | foreign_merge | out_not_empty |
+#           unreadable | timeout. The whole run is bounded to 60 seconds.
+# Contract: design section 7.3. No stdin read, no prompt. Any EVIDENCE_FAIL escalates
+#           the cycle to Tier 3.
+
+set -u -o pipefail
+
+LIMIT_SECONDS=60
+DEADLINE=$((SECONDS + LIMIT_SECONDS))
+TMP=""
+
+# shellcheck disable=SC2329  # invoked by the EXIT trap below
+cleanup() {
+    if [ -n "$TMP" ] && [ -d "$TMP" ]; then
+        rm -rf -- "$TMP"
+        rmdir -- "$(dirname -- "$TMP")" 2>/dev/null || true
+    fi
+}
+trap cleanup EXIT
+
+# Keep the caller's stdout and stderr on fds 3 and 4, so a failure raised while a
+# command's output is redirected into a capture file still reaches the caller.
+exec 3>&1 4>&2
+
+fail() {
+    # fail <reason> <detail>
+    printf 'collect-conflict-evidence: %s\n' "$2" >&4
+    printf 'EVIDENCE_FAIL %s\n' "$1" >&3
+    exit 2
+}
+
+is_sha() {
+    case "$1" in
+        *[!0-9a-fA-F]*) return 1 ;;
+    esac
+    [ "${#1}" -eq 40 ]
+}
+
+lower() {
+    printf '%s' "$1" | tr 'A-F' 'a-f'
+}
+
+# check_deadline : fail with "timeout" once the 60-second budget is spent.
+check_deadline() {
+    [ "$SECONDS" -lt "$DEADLINE" ] || fail timeout "the evidence run exceeded ${LIMIT_SECONDS} seconds"
+}
+
+# bounded <command>... : run one command within the remaining budget (under
+# `timeout` when it is on PATH). Returns the command's exit status; a timeout fails.
+bounded() {
+    local remaining rc
+    check_deadline
+    remaining=$((DEADLINE - SECONDS))
+    if command -v timeout >/dev/null 2>&1; then
+        timeout "$remaining" "$@"
+        rc=$?
+        [ "$rc" -ne 124 ] || fail timeout "'$*' did not finish within the ${LIMIT_SECONDS}-second budget"
+    else
+        "$@"
+        rc=$?
+    fi
+    check_deadline
+    return "$rc"
+}
+
+# Step 0: arguments.
+P=""
+OUT=""
+BASE_SHA=""
+MERGE_BASE=""
+MAX_BYTES=204800
+while [ $# -gt 0 ]; do
+    case "$1" in
+        --path|--out|--base-sha|--merge-base|--max-bytes)
+            [ $# -ge 2 ] || fail usage "missing value for $1"
+            case "$1" in
+                --path) P="$2" ;;
+                --out) OUT="$2" ;;
+                --base-sha) BASE_SHA="$2" ;;
+                --merge-base) MERGE_BASE="$2" ;;
+                --max-bytes) MAX_BYTES="$2" ;;
+            esac
+            shift 2
+            ;;
+        *) fail usage "unknown argument: $1" ;;
+    esac
+done
+[ -n "$P" ] || fail usage "missing required --path <p>"
+[ -n "$OUT" ] || fail usage "missing required --out <dir>"
+[ -n "$BASE_SHA" ] || fail usage "missing required --base-sha <40hex>"
+[ -n "$MERGE_BASE" ] || fail usage "missing required --merge-base <40hex>"
+is_sha "$BASE_SHA" || fail usage "--base-sha is not a 40-hex commit id: $BASE_SHA"
+is_sha "$MERGE_BASE" || fail usage "--merge-base is not a 40-hex commit id: $MERGE_BASE"
+case "$MAX_BYTES" in
+    ''|*[!0-9]*|0*) fail usage "--max-bytes is not a positive integer: $MAX_BYTES" ;;
+esac
+NL="$(printf '\nx')"
+NL="${NL%x}"
+# The path is repository-relative and canonical: no absolute path, no empty, "." or
+# ".." segment, no trailing slash, no newline.
+case "$P" in
+    /*|./*|../*|*/./*|*/../*|*/.|*/..|.|..|*//*|*/|*"$NL"*)
+        fail usage "--path must be a canonical repository-relative path: $P" ;;
+esac
+command -v jq >/dev/null 2>&1 || fail usage "jq not found on PATH"
+BASE_SHA="$(lower "$BASE_SHA")"
+MERGE_BASE="$(lower "$MERGE_BASE")"
+
+# --out is resolved against the caller's directory before the directory changes.
+case "$OUT" in /*) OUT_ABS="$OUT" ;; *) OUT_ABS="$PWD/$OUT" ;; esac
+TOPLEVEL="$(git rev-parse --show-toplevel 2>/dev/null)" || TOPLEVEL=""
+[ -n "$TOPLEVEL" ] || fail usage "not inside a git work tree"
+cd -- "$TOPLEVEL" || fail usage "cannot enter $TOPLEVEL"
+git rev-parse -q --verify "${MERGE_BASE}^{commit}" >/dev/null 2>&1 \
+    || fail usage "--merge-base does not name a commit: $MERGE_BASE"
+
+# Step 1: a merge of exactly the given base tip is in progress.
+MERGE_HEAD_SHA="$(git rev-parse -q --verify MERGE_HEAD 2>/dev/null)" || MERGE_HEAD_SHA=""
+[ -n "$MERGE_HEAD_SHA" ] || fail foreign_merge "no merge in progress (MERGE_HEAD is missing)"
+[ "$(lower "$MERGE_HEAD_SHA")" = "$BASE_SHA" ] \
+    || fail foreign_merge "MERGE_HEAD is $MERGE_HEAD_SHA, not the recorded base tip $BASE_SHA"
+
+# Step 2: --out is missing or an empty directory; nothing is written otherwise.
+if [ -e "$OUT_ABS" ] || [ -L "$OUT_ABS" ]; then
+    [ -d "$OUT_ABS" ] || fail out_not_empty "--out exists and is not a directory: $OUT"
+    [ -z "$(ls -A -- "$OUT_ABS" 2>/dev/null)" ] || fail out_not_empty "--out is not empty: $OUT"
+fi
+mkdir -p -- "$OUT_ABS" 2>/dev/null || fail usage "cannot create --out: $OUT"
+
+# Temporary files live only under the repository's git directory.
+TMP_ROOT="$(git rev-parse --git-path sc-pr-submit-tmp 2>/dev/null)" || TMP_ROOT=""
+[ -n "$TMP_ROOT" ] || fail usage "cannot resolve the git directory for temporary files"
+mkdir -p -- "$TMP_ROOT" 2>/dev/null || fail usage "cannot create $TMP_ROOT"
+TMP="$(mktemp -d "$TMP_ROOT/evidence.XXXXXXXX" 2>/dev/null)" || { TMP=""; fail usage "cannot create a temporary directory under $TMP_ROOT"; }
+
+FILES=()
+TRUNCATED=false
+
+# place <name> : copy $TMP/raw to --out/<name>, cut at MAX_BYTES with the marker line.
+place() {
+    local name="$1" size dest="$OUT_ABS/$1"
+    size="$(wc -c <"$TMP/raw")" || fail unreadable "cannot size the evidence for $name"
+    if [ "$size" -gt "$MAX_BYTES" ]; then
+        head -c "$MAX_BYTES" <"$TMP/raw" >"$dest" || fail unreadable "cannot write $dest"
+        if [ -n "$(tail -c 1 <"$dest")" ]; then
+            printf '\n' >>"$dest" || fail unreadable "cannot write $dest"
+        fi
+        printf '[sc:pr-submit: truncated at %s bytes]\n' "$MAX_BYTES" >>"$dest" \
+            || fail unreadable "cannot write $dest"
+        TRUNCATED=true
+    else
+        cat -- "$TMP/raw" >"$dest" || fail unreadable "cannot write $dest"
+    fi
+    FILES+=("$name")
+}
+
+# capture <name> <command>... : run a bounded read into $TMP/raw, then place it.
+capture() {
+    local name="$1"
+    shift
+    if ! bounded "$@" >"$TMP/raw" 2>"$TMP/err"; then
+        cat -- "$TMP/err" >&2
+        fail unreadable "cannot read the evidence for $name"
+    fi
+    place "$name"
+}
+
+# Step 3a: the stages the index lists for exactly this path.
+if ! bounded git --no-optional-locks --literal-pathspecs ls-files -u -z -- "$P" \
+        >"$TMP/stages" 2>"$TMP/err"; then
+    cat -- "$TMP/err" >&2
+    fail unreadable "cannot list the unmerged stages of $P"
+fi
+TAB="$(printf '\t')"
+HAVE=(0 0 0 0)  # HAVE[n] is 1 when the index lists stage n for the path
+while IFS= read -r -d '' record; do
+    meta="${record%%"$TAB"*}"
+    [ "${record#*"$TAB"}" = "$P" ] || continue
+    case "${meta##* }" in
+        1) HAVE[1]=1 ;;
+        2) HAVE[2]=1 ;;
+        3) HAVE[3]=1 ;;
+    esac
+done <"$TMP/stages"
+MISSING=()
+for n in 1 2 3; do
+    if [ "${HAVE[$n]}" -eq 1 ]; then
+        capture "stage$n" git --no-optional-locks show --no-textconv ":$n:$P"
+    else
+        MISSING+=("stage$n")
+    fi
+done
+
+# Step 3b: the work-tree file with its conflict markers (a regular, readable file).
+WORKTREE_FILE="$TOPLEVEL/$P"
+if [ -L "$WORKTREE_FILE" ] || [ ! -f "$WORKTREE_FILE" ] || [ ! -r "$WORKTREE_FILE" ]; then
+    fail unreadable "the work-tree file is missing, not a regular file or not readable: $P"
+fi
+capture worktree cat -- "$WORKTREE_FILE"
+
+# Step 3c: the left-right log of the merge, then both merge-base diffs.
+capture log.txt git --no-optional-locks --literal-pathspecs log --no-color \
+    --oneline --left-right --merge -- "$P"
+capture diff-ours.txt git --no-optional-locks --literal-pathspecs diff --no-color \
+    --no-ext-diff --no-textconv --no-renames "$MERGE_BASE" HEAD -- "$P"
+capture diff-theirs.txt git --no-optional-locks --literal-pathspecs diff --no-color \
+    --no-ext-diff --no-textconv --no-renames "$MERGE_BASE" "$BASE_SHA" -- "$P"
+check_deadline
+
+# Step 5.
+to_json_list() {
+    printf '%s\n' "$@" | jq -Rsc 'split("\n") | map(select(. != ""))'
+}
+FILES_JSON="$(to_json_list ${FILES[@]+"${FILES[@]}"})" || fail usage "could not render the file list"
+MISSING_JSON="$(to_json_list ${MISSING[@]+"${MISSING[@]}"})" || fail usage "could not render the missing list"
+jq -nc --arg dir "$OUT" --argjson files "$FILES_JSON" --argjson missing "$MISSING_JSON" \
+    --argjson truncated "$TRUNCATED" \
+    '{dir: $dir, files: $files, missing: $missing, truncated: $truncated}' \
+    || fail usage "could not render the evidence JSON"
+exit 0
diff --git a/tests/pr_submit/test_conflict_scripts.py b/tests/pr_submit/test_conflict_scripts.py
index d257f160..9f2889aa 100644
--- a/tests/pr_submit/test_conflict_scripts.py
+++ b/tests/pr_submit/test_conflict_scripts.py
@@ -1,7 +1,8 @@
 """Hermetic real-git tests for the conflict scripts (design section 12.4).
 
-This module covers ``scripts/probe-merge.sh`` (cases P1 to P12) and
-``scripts/finish-merge.sh`` (cases F1 to F12). Every git call runs
+This module covers ``scripts/probe-merge.sh`` (cases P1 to P12),
+``scripts/finish-merge.sh`` (cases F1 to F12) and
+``scripts/collect-conflict-evidence.sh`` (cases E1 to E4). Every git call runs
 inside a pytest temporary directory, with a local bare repository as ``origin`` and a
 ``gh`` stub first on ``PATH``. ``GIT_CONFIG_GLOBAL=/dev/null``, ``GIT_CONFIG_NOSYSTEM=1``
 and a fixed author and committer are set for every git call; ``HOME`` points into the
@@ -1093,3 +1094,339 @@ def test_finish_script_static_rules():
     ).stdout
     if ls:  # the index entry exists once the path is staged
         assert ls.startswith("100755 "), ls
+
+
+# ---------------------------------------------------------------------------
+# collect-conflict-evidence.sh helpers (design section 7.3)
+# ---------------------------------------------------------------------------
+
+EVIDENCE = SKILL_DIR / "scripts" / "collect-conflict-evidence.sh"
+EVIDENCE_REL = (
+    "src/superclaude/skills/sc-pr-submit-protocol/scripts/collect-conflict-evidence.sh"
+)
+ALL_EVIDENCE_FILES = [
+    "stage1",
+    "stage2",
+    "stage3",
+    "worktree",
+    "log.txt",
+    "diff-ours.txt",
+    "diff-theirs.txt",
+]
+
+
+@dataclass
+class EvidenceMerge:
+    base_sha: str
+    merge_base: str
+    old_head: str
+
+
+def start_zdiff3_merge(repos: Repos) -> EvidenceMerge:
+    """Fetch the base tip and start a real merge with the zdiff3 conflict style for
+    this one invocation (as the Tier 2 flow does), leaving the conflicts in place."""
+    repos.git(repos.work, "fetch", "-q", "origin", "main")
+    base_sha = repos.git(repos.work, "rev-parse", "origin/main").strip()
+    merge_base = repos.git(repos.work, "merge-base", "HEAD", base_sha).strip()
+    old_head = _head(repos)
+    repos.git(
+        repos.work,
+        "-c",
+        "merge.conflictStyle=zdiff3",
+        "merge",
+        "-q",
+        "--no-commit",
+        "--no-ff",
+        base_sha,
+        check=False,
+    )
+    assert _merge_head(repos).exists(), "the setup merge did not start"
+    return EvidenceMerge(base_sha=base_sha, merge_base=merge_base, old_head=old_head)
+
+
+def run_evidence(
+    repos: Repos,
+    path: str,
+    out: Path,
+    merge: EvidenceMerge,
+    *extra: str,
+    base_sha: str | None = None,
+) -> ProbeRun:
+    """Run the collector from its source path; assert it left the repository as-is."""
+    before = _snapshot(repos)
+    merge_head_before = (
+        _merge_head(repos).read_bytes() if _merge_head(repos).exists() else None
+    )
+    res = subprocess.run(
+        [
+            str(EVIDENCE),
+            "--path",
+            path,
+            "--out",
+            str(out),
+            "--base-sha",
+            base_sha or merge.base_sha,
+            "--merge-base",
+            merge.merge_base,
+            *extra,
+        ],
+        cwd=repos.work,
+        env=repos.env,
+        text=True,
+        capture_output=True,
+        timeout=120,
+    )
+    assert _snapshot(repos) == before, "the collector changed status, HEAD or the index"
+    merge_head_after = (
+        _merge_head(repos).read_bytes() if _merge_head(repos).exists() else None
+    )
+    assert merge_head_after == merge_head_before
+    assert not (repos.work / ".git" / "sc-pr-submit-tmp").exists()
+    assert repos.gh_call_lines() == [], "the collector must not call gh"
+    assert len(res.stdout.splitlines()) == 1, res.stdout
+    return ProbeRun(res.returncode, res.stdout, res.stderr)
+
+
+def assert_evidence_fail(res: ProbeRun, reason: str) -> None:
+    assert res.returncode == 2, (res.stdout, res.stderr)
+    assert res.stdout == f"EVIDENCE_FAIL {reason}\n", res.stderr
+
+
+def _listing(directory: Path) -> list[str]:
+    return sorted(p.name for p in directory.iterdir())
+
+
+# ---------------------------------------------------------------------------
+# E1 to E4
+# ---------------------------------------------------------------------------
+
+
+def test_e1_content_conflict_writes_exactly_the_seven_files(tmp_path):
+    repos = make_repos(tmp_path)
+    _content_conflict(repos)
+    merge = start_zdiff3_merge(repos)
+    out = tmp_path / "evidence" / "sync" / "sync-1" / "1"
+    res = run_evidence(repos, "f.txt", out, merge)
+    assert res.returncode == 0, res.stderr
+    assert res.payload == {
+        "dir": str(out),
+        "files": ALL_EVIDENCE_FILES,
+        "missing": [],
+        "truncated": False,
+    }
+    assert _listing(out) == sorted(ALL_EVIDENCE_FILES)
+    read = {
+        name: (out / name).read_text(encoding="utf-8") for name in ALL_EVIDENCE_FILES
+    }
+    assert read["stage1"] == "line1\nline2\nline3\n"
+    assert read["stage2"] == "line1\nOURS\nline3\n"
+    assert read["stage3"] == "line1\nTHEIRS\nline3\n"
+    # zdiff3: the work-tree file shows all three sides.
+    for marker in ("<<<<<<< ", "||||||| ", "=======\n", ">>>>>>> "):
+        assert marker in read["worktree"], marker
+    assert "OURS" in read["worktree"] and "THEIRS" in read["worktree"]
+    assert "line2" in read["worktree"]
+    log_lines = read["log.txt"].splitlines()
+    assert any(line.startswith("< ") and "pr change" in line for line in log_lines)
+    assert any(line.startswith("> ") and "base advance" in line for line in log_lines)
+    assert "-line2\n+OURS\n" in read["diff-ours.txt"]
+    assert "-line2\n+THEIRS\n" in read["diff-theirs.txt"]
+    for name in ALL_EVIDENCE_FILES:
+        assert "[sc:pr-submit: truncated" not in read[name], name
+
+
+def test_e2_modify_delete_lists_the_missing_stage(tmp_path):
+    repos = make_repos(tmp_path, {"d.txt": "keep\n", "README.md": "r\n"})
+    repos.advance_base({"d.txt": None})
+    repos.pr_commit({"d.txt": "modified\n"})
+    merge = start_zdiff3_merge(repos)
+    out = tmp_path / "evidence-e2"
+    res = run_evidence(repos, "d.txt", out, merge)
+    assert res.returncode == 0, res.stderr
+    payload = res.payload
+    assert payload["missing"] == ["stage3"]
+    expected = [name for name in ALL_EVIDENCE_FILES if name != "stage3"]
+    assert payload["files"] == expected
+    assert payload["truncated"] is False
+    assert _listing(out) == sorted(expected)
+    assert (out / "stage1").read_text(encoding="utf-8") == "keep\n"
+    assert (out / "stage2").read_text(encoding="utf-8") == "modified\n"
+    assert (out / "worktree").read_text(encoding="utf-8") == "modified\n"
+    assert "-keep\n" in (out / "diff-theirs.txt").read_text(encoding="utf-8")
+    assert "+modified\n" in (out / "diff-ours.txt").read_text(encoding="utf-8")
+
+
+def test_e3_max_bytes_cuts_each_file_with_the_marker_line(tmp_path):
+    base = "".join(f"base line {i:03d} of the shared file\n" for i in range(10))
+    ours = base.replace("base line 005", "OURS line 005")
+    theirs = base.replace("base line 005", "THEIRS line 005")
+    repos = make_repos(tmp_path, {"README.md": "r\n", "f.txt": base})
+    repos.advance_base({"f.txt": theirs})
+    repos.pr_commit({"f.txt": ours})
+    merge = start_zdiff3_merge(repos)
+    out = tmp_path / "evidence-e3"
+    res = run_evidence(repos, "f.txt", out, merge, "--max-bytes", "64")
+    assert res.returncode == 0, res.stderr
+    payload = res.payload
+    assert payload["truncated"] is True
+    assert payload["files"] == ALL_EVIDENCE_FILES
+    marker = "[sc:pr-submit: truncated at 64 bytes]\n"
+    originals = {"stage1": base, "stage2": ours, "stage3": theirs}
+    for name, original in originals.items():
+        data = (out / name).read_bytes()
+        assert data.endswith(marker.encode()), name
+        cut = original.encode()[:64]
+        assert data.startswith(cut), name
+        assert data[len(cut) :] in (marker.encode(), b"\n" + marker.encode()), name
+    for name in ("worktree", "diff-ours.txt", "diff-theirs.txt"):
+        text = (out / name).read_text(encoding="utf-8")
+        assert text.splitlines()[-1] == marker.rstrip("\n"), name
+    # A file at or under the limit is copied unchanged, without the marker.
+    small = run_evidence(
+        repos, "f.txt", tmp_path / "evidence-e3-big", merge, "--max-bytes", "100000"
+    ).payload
+    assert small["truncated"] is False
+    assert (tmp_path / "evidence-e3-big" / "stage1").read_text(encoding="utf-8") == base
+
+
+@pytest.mark.parametrize("kind", ["non-empty-dir", "regular-file"])
+def test_e4_non_empty_out_is_out_not_empty_and_writes_nothing(tmp_path, kind):
+    repos = make_repos(tmp_path)
+    _content_conflict(repos)
+    merge = start_zdiff3_merge(repos)
+    out = tmp_path / "evidence-e4"
+    if kind == "non-empty-dir":
+        out.mkdir()
+        (out / "keep.txt").write_text("operator file\n", encoding="utf-8")
+    else:
+        out.write_text("a file, not a directory\n", encoding="utf-8")
+    parent_before = _listing(tmp_path)
+    res = run_evidence(repos, "f.txt", out, merge)
+    assert_evidence_fail(res, "out_not_empty")
+    assert _listing(tmp_path) == parent_before
+    if kind == "non-empty-dir":
+        assert _listing(out) == ["keep.txt"]
+        assert (out / "keep.txt").read_text(encoding="utf-8") == "operator file\n"
+    else:
+        assert out.read_text(encoding="utf-8") == "a file, not a directory\n"
+
+
+# ---------------------------------------------------------------------------
+# Further contract rows of section 7.3
+# ---------------------------------------------------------------------------
+
+
+def test_existing_empty_out_directory_is_accepted(tmp_path):
+    repos = make_repos(tmp_path)
+    _content_conflict(repos)
+    merge = start_zdiff3_merge(repos)
+    out = tmp_path / "empty-out"
+    out.mkdir()
+    res = run_evidence(repos, "f.txt", out, merge)
+    assert res.returncode == 0, res.stderr
+    assert _listing(out) == sorted(ALL_EVIDENCE_FILES)
+
+
+def test_foreign_merge_and_no_merge_head(tmp_path):
+    repos = make_repos(tmp_path)
+    _content_conflict(repos)
+    repos.git(repos.work, "fetch", "-q", "origin", "main")
+    base_sha = repos.git(repos.work, "rev-parse", "origin/main").strip()
+    merge = EvidenceMerge(
+        base_sha=base_sha,
+        merge_base=repos.git(repos.work, "merge-base", "HEAD", base_sha).strip(),
+        old_head=_head(repos),
+    )
+    out = tmp_path / "evidence-foreign"
+    # No merge in progress.
+    assert_evidence_fail(run_evidence(repos, "f.txt", out, merge), "foreign_merge")
+    assert not out.exists()
+    # A merge of the base tip, checked against another commit.
+    start_zdiff3_merge(repos)
+    res = run_evidence(repos, "f.txt", out, merge, base_sha=merge.old_head)
+    assert_evidence_fail(res, "foreign_merge")
+    assert not out.exists()
+    # The recorded base tip is compared case-insensitively.
+    ok = run_evidence(repos, "f.txt", out, merge, base_sha=base_sha.upper())
+    assert ok.returncode == 0, ok.stderr
+
+
+@pytest.mark.parametrize(
+    "path, extra",
+    [
+        ("/etc/passwd", ()),
+        ("../f.txt", ()),
+        ("./f.txt", ()),
+        ("f.txt", ("--max-bytes", "0")),
+        ("f.txt", ("--max-bytes", "12k")),
+        ("f.txt", ("--bogus",)),
+    ],
+    ids=["absolute", "dotdot", "dot", "zero-bytes", "bad-bytes", "unknown"],
+)
+def test_evidence_usage_errors(tmp_path, path, extra):
+    repos = make_repos(tmp_path)
+    _content_conflict(repos)
+    merge = start_zdiff3_merge(repos)
+    out = tmp_path / "evidence-usage"
+    res = run_evidence(repos, path, out, merge, *extra)
+    assert_evidence_fail(res, "usage")
+    assert not out.exists()
+
+
+def test_missing_work_tree_file_is_unreadable(tmp_path):
+    repos = make_repos(tmp_path)
+    _content_conflict(repos)
+    merge = start_zdiff3_merge(repos)
+    (repos.work / "f.txt").unlink()
+    res = run_evidence(repos, "f.txt", tmp_path / "evidence-unreadable", merge)
+    assert_evidence_fail(res, "unreadable")
+
+
+def test_a_command_hitting_the_time_bound_is_timeout(tmp_path):
+    """A `timeout` stub reports exit 124 for the log read, as the real `timeout`
+    does when the 60-second budget runs out; the collector maps it to `timeout`."""
+    repos = make_repos(tmp_path)
+    _content_conflict(repos)
+    merge = start_zdiff3_merge(repos)
+    real_timeout = shutil.which("timeout")
+    if real_timeout is None:
+        pytest.skip("timeout is not on PATH")
+    stub = repos.bin_dir / "timeout"
+    stub.write_text(
+        "#!/usr/bin/env bash\n"
+        'for a in "$@"; do [ "$a" = log ] && exit 124; done\n'
+        f'exec "{real_timeout}" "$@"\n',
+        encoding="utf-8",
+    )
+    stub.chmod(0o755)
+    res = run_evidence(repos, "f.txt", tmp_path / "evidence-timeout", merge)
+    assert_evidence_fail(res, "timeout")
+    assert "60-second budget" in res.stderr
+
+
+def test_evidence_script_static_rules():
+    text = EVIDENCE.read_text(encoding="utf-8")
+    assert text.startswith("#!/usr/bin/env bash\n")
+    assert "\nset -u -o pipefail\n" in text
+    assert os.access(EVIDENCE, os.X_OK)
+    for pattern in (
+        r"(?i)\bpush\b",
+        r"(?i)stash",
+        r"(?i)force",
+        r"\bgit\s+config\b",
+        r"--no-verify\b",
+        r"--amend\b",
+        r"src/superclaude",
+        r"\bgit\s+(checkout|switch|reset|commit|add|rm|worktree|rebase|merge)\b",
+        r"\bgh\b",
+    ):
+        assert re.search(pattern, text) is None, pattern
+    ls = subprocess.run(
+        [GIT, "ls-files", "-s", "--", EVIDENCE_REL],
+        cwd=REPO_ROOT,
+        text=True,
+        capture_output=True,
+        timeout=30,
+    ).stdout
+    if ls:  # the index entry exists once the path is staged
+        assert ls.startswith("100755 "), ls
diff --git a/.dev/tasks/to-do/TASK-WF-design-20261104-164423/artifacts/t12-tests.log b/.dev/tasks/to-do/TASK-WF-design-20261104-164423/artifacts/t12-tests.log
new file mode 100644
index 00000000..64f5e499
--- /dev/null
+++ b/.dev/tasks/to-do/TASK-WF-design-20261104-164423/artifacts/t12-tests.log
@@ -0,0 +1,13 @@
+============================= test session starts ==============================
+platform linux -- Python 3.11.15, pytest-9.2.0, pluggy-1.7.0
+SuperClaude: 5.0.0
+benchmark: 5.3.1 (defaults: timer=time.perf_counter disable_gc=False min_rounds=5 min_time=0.000005 max_time=1.0 calibration_precision=10 warmup=False warmup_iterations=100000)
+rootdir: /home/coder/workspaces/worktrees/IronClaude/issue-305-pr-submit-conflicts
+configfile: pyproject.toml
+plugins: superclaude-5.0.0, benchmark-5.3.1, anyio-4.16.0, cov-7.1.0
+collected 73 items
+
+tests/pr_submit/test_conflict_scripts.py ............................... [ 42%]
+..........................................                               [100%]
+
+============================= 73 passed in 11.83s ==============================
diff --git a/.dev/tasks/to-do/TASK-WF-design-20261104-164423/artifacts/t12-grep.txt b/.dev/tasks/to-do/TASK-WF-design-20261104-164423/artifacts/t12-grep.txt
new file mode 100644
index 00000000..5a9a49f2
--- /dev/null
+++ b/.dev/tasks/to-do/TASK-WF-design-20261104-164423/artifacts/t12-grep.txt
@@ -0,0 +1,35 @@
+# t12 forbidden-item grep over src/superclaude/skills/sc-pr-submit-protocol/scripts/collect-conflict-evidence.sh (no output under a heading = no hit)
+## grep -n -i -E -e 'git[[:space:]]+push'
+exit=1
+## grep -n -i -E -e 'push'
+exit=1
+## grep -n -i -E -e 'stash'
+exit=1
+## grep -n -i -E -e 'force'
+exit=1
+## grep -n -i -E -e '--amend'
+exit=1
+## grep -n -i -E -e '--no-verify'
+exit=1
+## grep -n -i -E -e 'git[[:space:]]+config'
+exit=1
+## grep -n -i -E -e 'src/superclaude'
+exit=1
+## grep -n -i -E -e '\bgh\b'
+exit=1
+## grep -n -i -E -e 'git[[:space:]]+(checkout|switch|reset|commit|add|rm|worktree|rebase|merge)\b'
+exit=1
+## gh calls (each must carry --repo "$REPO"; none expected)
+exit=1
+## set line
+30:set -u -o pipefail
+## git commands used (all read-only)
+135:git rev-parse
+138:git rev-parse
+142:git rev-parse
+155:git rev-parse
+193:git --no-optional-locks --literal-pathspecs ls-files
+212:git --no-optional-locks show
+226:git --no-optional-locks --literal-pathspecs log
+228:git --no-optional-locks --literal-pathspecs diff
+230:git --no-optional-locks --literal-pathspecs diff
diff --git a/.dev/tasks/to-do/TASK-WF-design-20261104-164423/artifacts/t12-mode.txt b/.dev/tasks/to-do/TASK-WF-design-20261104-164423/artifacts/t12-mode.txt
new file mode 100644
index 00000000..6f9669c5
--- /dev/null
+++ b/.dev/tasks/to-do/TASK-WF-design-20261104-164423/artifacts/t12-mode.txt
@@ -0,0 +1,2 @@
+100755 181d96403197b8456449890f3212c9c43b6fda82 0	src/superclaude/skills/sc-pr-submit-protocol/scripts/collect-conflict-evidence.sh
+test -x: ok (exit 0)

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

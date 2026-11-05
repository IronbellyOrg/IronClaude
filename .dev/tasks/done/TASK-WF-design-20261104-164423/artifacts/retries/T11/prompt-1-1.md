dd8f1afb4900900cfad7b7b75e14868844eeb561
Review one task for spec compliance.

Task brief: ## Task 11: Create the finish gate `finish-merge.sh`

Depends on: Task 10

Create `src/superclaude/skills/sc-pr-submit-protocol/scripts/finish-merge.sh` (mode 100755) per source section 7.2: precheck mode (`--base-sha` only; any commit-mode option is `FINISH_FAIL usage`) and commit mode with all nine steps in order (merge ownership, unmerged, tree, introduced markers, staged-set equality with the merge-tree blob, `git commit -F` with hooks on, exact parents, clean after, JSON output). Add cases F1 to F12 of source section 12.4 to `tests/pr_submit/test_conflict_scripts.py`.

Acceptance criteria:
- F1 to F12 pass, including F9 (failing `pre-commit` hook: `FINISH_FAIL hook_rejected`, hook output verbatim on stderr, no commit, `MERGE_HEAD` still present) and F10 (exactly two parents `[old HEAD, base_sha]` and `merge_parent_ok` true).
- The script commits only through one `git commit -F`; it contains no push, stash, amend, hook-skipping flag or `src/superclaude/` text.
- `uv run pytest tests/pr_submit/test_conflict_scripts.py -q` passes; log saved to `./artifacts/t11-tests.log`.
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
Start sha: dd8f1afb4900900cfad7b7b75e14868844eeb561
Diff against the start snapshot: diff --git a/src/superclaude/skills/sc-pr-submit-protocol/scripts/finish-merge.sh b/src/superclaude/skills/sc-pr-submit-protocol/scripts/finish-merge.sh
new file mode 100755
index 00000000..8ac4c485
--- /dev/null
+++ b/src/superclaude/skills/sc-pr-submit-protocol/scripts/finish-merge.sh
@@ -0,0 +1,280 @@
+#!/usr/bin/env bash
+#
+# finish-merge.sh — finish gate for sc:pr-submit conflict cycles (issue #305).
+#
+# Purpose : Prove that an in-progress merge of the recorded base tip is safe to
+#           conclude, then conclude it with exactly one commit from the given
+#           message file (hooks on).
+#           Precheck mode (run right before a regenerate) only checks and never
+#           commits. This is the only conflict script that changes the repository,
+#           and only through that one commit. It never publishes anything, never
+#           sets work aside, never rewrites an existing commit, never skips hooks
+#           and never writes stored configuration.
+# Usage   : finish-merge.sh --base-sha <40hex> --precheck
+#           finish-merge.sh --base-sha <40hex> --merge-tree-oid <40hex> \
+#                           --manifest <file> --message-file <file>
+#           The manifest is the finish_manifest text: one "<stage-1 oid or ->\t<path>"
+#           line per resolved path. Precheck mode accepts none of --merge-tree-oid,
+#           --manifest or --message-file; commit mode requires all three.
+# Output  : exactly one stdout line. Success is one JSON object:
+#           precheck mode {"precheck":"ok"}
+#           commit mode   {"merge_sha":"<40hex>","parents":["<old HEAD>","<base-sha>"]}
+#           Failure is the token "FINISH_FAIL <reason>"; details (and git's own
+#           output, verbatim, when the commit is rejected) go to stderr.
+# Exit    : 0 on success; 2 with FINISH_FAIL usage | no_merge_head | foreign_merge |
+#           unmerged | tree_dirty | markers | staged_unexpected | hook_rejected |
+#           parents_mismatch.
+# Contract: design section 7.2. No stdin read, no prompt.
+
+set -u -o pipefail
+
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
+fail() {
+    # fail <reason> <detail>
+    printf 'finish-merge: %s\n' "$2" >&2
+    printf 'FINISH_FAIL %s\n' "$1"
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
+# in_list <needle> <item>... : exact membership.
+in_list() {
+    local needle="$1" item
+    shift
+    for item in "$@"; do
+        [ "$item" = "$needle" ] && return 0
+    done
+    return 1
+}
+
+# Step 0: arguments.
+BASE_SHA=""
+MT_OID=""
+MANIFEST=""
+MESSAGE_FILE=""
+PRECHECK=0
+COMMIT_OPTS=0
+while [ $# -gt 0 ]; do
+    case "$1" in
+        --base-sha|--merge-tree-oid|--manifest|--message-file)
+            [ $# -ge 2 ] || fail usage "missing value for $1"
+            case "$1" in
+                --base-sha) BASE_SHA="$2" ;;
+                --merge-tree-oid) MT_OID="$2"; COMMIT_OPTS=1 ;;
+                --manifest) MANIFEST="$2"; COMMIT_OPTS=1 ;;
+                --message-file) MESSAGE_FILE="$2"; COMMIT_OPTS=1 ;;
+            esac
+            shift 2
+            ;;
+        --precheck) PRECHECK=1; shift ;;
+        *) fail usage "unknown argument: $1" ;;
+    esac
+done
+[ -n "$BASE_SHA" ] || fail usage "missing required --base-sha <40hex>"
+is_sha "$BASE_SHA" || fail usage "--base-sha is not a 40-hex commit id: $BASE_SHA"
+if [ "$PRECHECK" -eq 1 ]; then
+    [ "$COMMIT_OPTS" -eq 0 ] \
+        || fail usage "--precheck takes only --base-sha (no --merge-tree-oid, --manifest or --message-file)"
+else
+    [ -n "$MT_OID" ] && [ -n "$MANIFEST" ] && [ -n "$MESSAGE_FILE" ] \
+        || fail usage "commit mode requires --merge-tree-oid, --manifest and --message-file"
+    is_sha "$MT_OID" || fail usage "--merge-tree-oid is not a 40-hex object id: $MT_OID"
+    [ -f "$MANIFEST" ] && [ -r "$MANIFEST" ] || fail usage "manifest not readable: $MANIFEST"
+    [ -f "$MESSAGE_FILE" ] && [ -r "$MESSAGE_FILE" ] || fail usage "message file not readable: $MESSAGE_FILE"
+fi
+command -v jq >/dev/null 2>&1 || fail usage "jq not found on PATH"
+
+# Work from the top of the work tree so every path below is repository-relative.
+# The manifest and message paths are resolved before the directory changes.
+if [ "$PRECHECK" -eq 0 ]; then
+    case "$MANIFEST" in /*) ;; *) MANIFEST="$PWD/$MANIFEST" ;; esac
+    case "$MESSAGE_FILE" in /*) ;; *) MESSAGE_FILE="$PWD/$MESSAGE_FILE" ;; esac
+fi
+TOPLEVEL="$(git rev-parse --show-toplevel 2>/dev/null)" || TOPLEVEL=""
+[ -n "$TOPLEVEL" ] || fail usage "not inside a git work tree"
+cd -- "$TOPLEVEL" || fail usage "cannot enter $TOPLEVEL"
+
+# Temporary files live only under the repository's git directory.
+TMP_ROOT="$(git rev-parse --git-path sc-pr-submit-tmp 2>/dev/null)" || TMP_ROOT=""
+[ -n "$TMP_ROOT" ] || fail usage "cannot resolve the git directory for temporary files"
+mkdir -p -- "$TMP_ROOT" 2>/dev/null || fail usage "cannot create $TMP_ROOT"
+TMP="$(mktemp -d "$TMP_ROOT/finish.XXXXXXXX" 2>/dev/null)" || { TMP=""; fail usage "cannot create a temporary directory under $TMP_ROOT"; }
+
+# read_nul_list <file> : fill LIST with the NUL-separated entries of <file>.
+LIST=()
+read_nul_list() {
+    LIST=()
+    local item
+    while IFS= read -r -d '' item; do
+        LIST+=("$item")
+    done <"$1"
+}
+
+# Step 1 (both modes): a merge of exactly the given base tip is in progress.
+check_merge_head() {
+    local merge_head
+    merge_head="$(git rev-parse -q --verify MERGE_HEAD 2>/dev/null)" || merge_head=""
+    [ -n "$merge_head" ] || fail no_merge_head "no merge in progress (MERGE_HEAD is missing)"
+    [ "$(lower "$merge_head")" = "$(lower "$BASE_SHA")" ] \
+        || fail foreign_merge "MERGE_HEAD is $merge_head, not the recorded base tip $BASE_SHA"
+}
+
+check_merge_head
+
+if [ "$PRECHECK" -eq 1 ]; then
+    # Precheck step 2: the work tree differs from the index only at unmerged paths.
+    git diff --name-only --no-renames -z >"$TMP/worktree" 2>"$TMP/err" \
+        || { cat -- "$TMP/err" >&2; fail tree_dirty "git diff of the work tree failed"; }
+    git diff --name-only --diff-filter=U -z >"$TMP/unmerged" 2>"$TMP/err" \
+        || { cat -- "$TMP/err" >&2; fail tree_dirty "git diff of the unmerged paths failed"; }
+    read_nul_list "$TMP/unmerged"
+    UNMERGED=(${LIST[@]+"${LIST[@]}"})
+    read_nul_list "$TMP/worktree"
+    for path in ${LIST[@]+"${LIST[@]}"}; do
+        in_list "$path" ${UNMERGED[@]+"${UNMERGED[@]}"} \
+            || fail tree_dirty "tracked file changed outside the conflict set: $path"
+    done
+    # Precheck step 3.
+    jq -nc '{precheck: "ok"}' || fail usage "could not render the precheck JSON"
+    exit 0
+fi
+
+# Commit mode. The merge-tree object must be a tree; the manifest must parse.
+git rev-parse -q --verify "${MT_OID}^{tree}" >/dev/null 2>&1 \
+    || fail usage "--merge-tree-oid does not name a tree: $MT_OID"
+M_OIDS=()
+M_PATHS=()
+LINE_NO=0
+TAB="$(printf '\t')"
+while IFS= read -r line || [ -n "$line" ]; do
+    LINE_NO=$((LINE_NO + 1))
+    case "$line" in
+        *"$TAB"*) ;;
+        *) fail usage "manifest line $LINE_NO has no tab" ;;
+    esac
+    oid="${line%%"$TAB"*}"
+    path="${line#*"$TAB"}"
+    [ "$oid" = "-" ] || is_sha "$oid" || fail usage "manifest line $LINE_NO: bad stage-1 oid '$oid'"
+    [ -n "$path" ] || fail usage "manifest line $LINE_NO: empty path"
+    if in_list "$path" ${M_PATHS[@]+"${M_PATHS[@]}"}; then
+        fail usage "manifest names $path twice"
+    fi
+    M_OIDS+=("$oid")
+    M_PATHS+=("$path")
+done <"$MANIFEST"
+
+OLD_HEAD="$(git rev-parse -q --verify 'HEAD^{commit}' 2>/dev/null)" || fail usage "HEAD does not name a commit"
+
+# Step 2: nothing left unmerged.
+git diff --name-only --diff-filter=U -z >"$TMP/unmerged" 2>"$TMP/err" \
+    || { cat -- "$TMP/err" >&2; fail unmerged "git diff of the unmerged paths failed"; }
+if [ -s "$TMP/unmerged" ]; then
+    read_nul_list "$TMP/unmerged"
+    fail unmerged "unmerged paths remain: ${LIST[*]}"
+fi
+
+# Step 3: no unstaged change to a tracked file (the index equals the validated work tree).
+git diff --quiet --no-renames 2>"$TMP/err"
+DIFF_EXIT=$?
+case "$DIFF_EXIT" in
+    0) ;;
+    1) fail tree_dirty "a tracked file has an unstaged change" ;;
+    *) cat -- "$TMP/err" >&2; fail tree_dirty "git diff --quiet exited $DIFF_EXIT" ;;
+esac
+
+# count_markers <file> : print the number of conflict-marker lines in <file>.
+count_markers() {
+    local n rc
+    n="$(grep -a -c -E '^(<{7}|[|]{7}|={7}|>{7})( |$)' -- "$1")"
+    rc=$?
+    [ "$rc" -le 1 ] || return 1
+    printf '%s' "${n:-0}"
+}
+
+# Step 4: no resolved path holds more marker lines than its stage-1 blob did.
+i=0
+while [ "$i" -lt "${#M_PATHS[@]}" ]; do
+    path="${M_PATHS[$i]}"
+    oid="${M_OIDS[$i]}"
+    i=$((i + 1))
+    # A path resolved by deletion is not in the index and is skipped.
+    git rev-parse -q --verify ":0:$path" >/dev/null 2>&1 || continue
+    git cat-file blob ":0:$path" >"$TMP/result" 2>"$TMP/err" \
+        || { cat -- "$TMP/err" >&2; fail markers "cannot read the staged blob of $path"; }
+    have="$(count_markers "$TMP/result")" || fail markers "cannot count markers in $path"
+    base_count=0
+    if [ "$oid" != "-" ]; then
+        git cat-file blob "$oid" >"$TMP/base" 2>"$TMP/err" \
+            || { cat -- "$TMP/err" >&2; fail usage "manifest stage-1 blob $oid of $path is not readable"; }
+        base_count="$(count_markers "$TMP/base")" || fail markers "cannot count markers in the stage-1 blob of $path"
+    fi
+    [ "$have" -le "$base_count" ] \
+        || fail markers "$path holds $have conflict-marker line(s); its stage-1 blob had $base_count"
+done
+
+# Step 5: outside the manifest, the index equals the merge-tree result path by path.
+git diff --cached --name-only --no-renames -z HEAD >"$TMP/staged" 2>"$TMP/err" \
+    || { cat -- "$TMP/err" >&2; fail staged_unexpected "git diff --cached HEAD failed"; }
+git diff --name-only --no-renames -z HEAD "$MT_OID" >"$TMP/merged" 2>"$TMP/err" \
+    || { cat -- "$TMP/err" >&2; fail staged_unexpected "git diff of HEAD against the merge tree failed"; }
+for list_file in "$TMP/staged" "$TMP/merged"; do
+    read_nul_list "$list_file"
+    for path in ${LIST[@]+"${LIST[@]}"}; do
+        if in_list "$path" ${M_PATHS[@]+"${M_PATHS[@]}"}; then
+            continue
+        fi
+        index_blob="$(git rev-parse -q --verify ":0:$path" 2>/dev/null)" || index_blob=""
+        merged_blob="$(git rev-parse -q --verify "${MT_OID}:$path" 2>/dev/null)" || merged_blob=""
+        [ "$index_blob" = "$merged_blob" ] \
+            || fail staged_unexpected "the index differs from the merge-tree result at $path"
+    done
+done
+
+# Step 6: the one commit, with hooks on. git's output goes to stderr verbatim.
+if ! git commit -F "$MESSAGE_FILE" >"$TMP/commit.out" 2>&1; then
+    cat -- "$TMP/commit.out" >&2
+    fail hook_rejected "the commit was rejected (output above); the merge is still in progress"
+fi
+cat -- "$TMP/commit.out" >&2
+
+# Step 7: exactly the parents [old HEAD, base tip].
+PARENTS_LINE="$(git rev-list --parents -n 1 HEAD 2>/dev/null)" || PARENTS_LINE=""
+read -r NEW_SHA P1 P2 EXTRA <<EOF_PARENTS
+$PARENTS_LINE
+EOF_PARENTS
+[ -n "${NEW_SHA:-}" ] && [ -z "${EXTRA:-}" ] \
+    && [ "$(lower "${P1:-}")" = "$(lower "$OLD_HEAD")" ] \
+    && [ "$(lower "${P2:-}")" = "$(lower "$BASE_SHA")" ] \
+    || fail parents_mismatch "new commit parents are '${PARENTS_LINE}', expected <new> $OLD_HEAD $BASE_SHA"
+
+# Step 8: clean after the commit.
+git status --porcelain=v1 --untracked-files=no -z >"$TMP/status" 2>"$TMP/err" \
+    || { cat -- "$TMP/err" >&2; fail tree_dirty "git status failed after the commit"; }
+[ ! -s "$TMP/status" ] || fail tree_dirty "tracked files differ from the new commit"
+git diff --quiet HEAD 2>/dev/null || fail tree_dirty "the work tree differs from the new commit"
+
+# Step 9.
+jq -nc --arg merge_sha "$NEW_SHA" --arg old "$P1" --arg base "$P2" \
+    '{merge_sha: $merge_sha, parents: [$old, $base]}' \
+    || fail usage "could not render the finish JSON"
+exit 0
diff --git a/tests/pr_submit/test_conflict_scripts.py b/tests/pr_submit/test_conflict_scripts.py
index c3a0f343..d257f160 100644
--- a/tests/pr_submit/test_conflict_scripts.py
+++ b/tests/pr_submit/test_conflict_scripts.py
@@ -1,6 +1,7 @@
 """Hermetic real-git tests for the conflict scripts (design section 12.4).
 
-This module covers ``scripts/probe-merge.sh`` (cases P1 to P12). Every git call runs
+This module covers ``scripts/probe-merge.sh`` (cases P1 to P12) and
+``scripts/finish-merge.sh`` (cases F1 to F12). Every git call runs
 inside a pytest temporary directory, with a local bare repository as ``origin`` and a
 ``gh`` stub first on ``PATH``. ``GIT_CONFIG_GLOBAL=/dev/null``, ``GIT_CONFIG_NOSYSTEM=1``
 and a fixed author and committer are set for every git call; ``HOME`` points into the
@@ -24,8 +25,12 @@ import pytest
 
 from superclaude.pr_submit.conflicts import (
     MAX_PROBE_BYTES,
+    MergeTreeListing,
     conflict_plan,
+    finish_manifest,
     group_entries,
+    merge_parent_ok,
+    merge_preflight_ok,
     parse_probe,
 )
 
@@ -33,6 +38,8 @@ REPO_ROOT = Path(__file__).resolve().parents[2]
 SKILL_DIR = REPO_ROOT / "src" / "superclaude" / "skills" / "sc-pr-submit-protocol"
 PROBE = SKILL_DIR / "scripts" / "probe-merge.sh"
 PROBE_REL = "src/superclaude/skills/sc-pr-submit-protocol/scripts/probe-merge.sh"
+FINISH = SKILL_DIR / "scripts" / "finish-merge.sh"
+FINISH_REL = "src/superclaude/skills/sc-pr-submit-protocol/scripts/finish-merge.sh"
 
 GIT = shutil.which("git")
 
@@ -628,3 +635,461 @@ def test_probe_script_static_rules():
     ).stdout
     if ls:  # the index entry exists once the path is staged
         assert ls.startswith("100755 "), ls
+
+
+# ---------------------------------------------------------------------------
+# finish-merge.sh helpers (design section 7.2)
+# ---------------------------------------------------------------------------
+
+
+@dataclass
+class MergeSetup:
+    base_sha: str
+    old_head: str
+    merge_tree_oid: str
+    listing: MergeTreeListing
+
+
+def _merge_head(repos: Repos) -> Path:
+    return repos.work / ".git" / "MERGE_HEAD"
+
+
+def _head(repos: Repos) -> str:
+    return repos.git(repos.work, "rev-parse", "HEAD").strip()
+
+
+def start_merge(repos: Repos) -> MergeSetup:
+    """Probe (as the SKILL does), then run a real `git merge --no-commit --no-ff`."""
+    payload = full(repos).payload
+    probe = parse_probe(payload)
+    assert probe.listing is not None
+    old_head = _head(repos)
+    repos.git(
+        repos.work, "merge", "-q", "--no-commit", "--no-ff", probe.base_sha, check=False
+    )
+    assert _merge_head(repos).exists(), "the setup merge did not start"
+    return MergeSetup(
+        base_sha=probe.base_sha,
+        old_head=old_head,
+        merge_tree_oid=probe.listing.tree_oid,
+        listing=probe.listing,
+    )
+
+
+def resolve(repos: Repos, files: dict[str, str]) -> None:
+    repos.write(repos.work, files)
+
+
+def run_finish(repos: Repos, *args: str) -> ProbeRun:
+    res = subprocess.run(
+        [str(FINISH), *args],
+        cwd=repos.work,
+        env=repos.env,
+        text=True,
+        capture_output=True,
+        timeout=120,
+    )
+    assert not (repos.work / ".git" / "sc-pr-submit-tmp").exists()
+    assert repos.gh_call_lines() == [], "finish-merge must not call gh"
+    assert len(res.stdout.splitlines()) == 1, res.stdout
+    return ProbeRun(res.returncode, res.stdout, res.stderr)
+
+
+MESSAGE = "Merge origin/main into pr (sc:pr-submit sync-1)\n\nResolved: f.txt\n"
+
+
+def finish_commit(
+    repos: Repos,
+    setup: MergeSetup,
+    resolved: list[str],
+    *,
+    base_sha: str | None = None,
+) -> ProbeRun:
+    manifest = repos.root / "manifest.txt"
+    manifest.write_text(finish_manifest(setup.listing, resolved), encoding="utf-8")
+    message = repos.root / "message.txt"
+    message.write_text(MESSAGE, encoding="utf-8")
+    return run_finish(
+        repos,
+        "--base-sha",
+        base_sha or setup.base_sha,
+        "--merge-tree-oid",
+        setup.merge_tree_oid,
+        "--manifest",
+        str(manifest),
+        "--message-file",
+        str(message),
+    )
+
+
+def precheck(repos: Repos, base_sha: str) -> ProbeRun:
+    return run_finish(repos, "--base-sha", base_sha, "--precheck")
+
+
+def assert_fail(res: ProbeRun, reason: str) -> None:
+    assert res.returncode == 2, (res.stdout, res.stderr)
+    assert res.stdout == f"FINISH_FAIL {reason}\n", res.stderr
+
+
+def assert_no_commit(repos: Repos, setup: MergeSetup) -> None:
+    assert _head(repos) == setup.old_head, "a commit was made"
+    assert _merge_head(repos).exists(), "the merge is no longer in progress"
+
+
+def _two_file_conflict(repos: Repos) -> None:
+    repos.advance_base({"f.txt": "line1\nTHEIRS\nline3\n", "g.txt": "g\nTHEIRS\n"})
+    repos.pr_commit({"f.txt": "line1\nOURS\nline3\n", "g.txt": "g\nOURS\n"})
+
+
+_BASE_FG = {
+    "README.md": "readme\n",
+    "f.txt": "line1\nline2\nline3\n",
+    "g.txt": "g\n2\n",
+}
+RESOLVED_F = "line1\nOURS and THEIRS\nline3\n"
+
+
+# ---------------------------------------------------------------------------
+# F1 to F12
+# ---------------------------------------------------------------------------
+
+
+def test_f1_one_path_left_unmerged_is_unmerged(tmp_path):
+    repos = make_repos(tmp_path, _BASE_FG)
+    _two_file_conflict(repos)
+    setup = start_merge(repos)
+    resolve(repos, {"f.txt": RESOLVED_F})
+    res = finish_commit(repos, setup, ["f.txt", "g.txt"])
+    assert_fail(res, "unmerged")
+    assert "g.txt" in res.stderr
+    assert_no_commit(repos, setup)
+
+
+@pytest.mark.parametrize(
+    "content",
+    [None, "line1\n=======\nline3\n"],
+    ids=["git-markers-left", "one-introduced-marker"],
+)
+def test_f2_introduced_marker_is_markers(tmp_path, content):
+    repos = make_repos(tmp_path)
+    _content_conflict(repos)
+    setup = start_merge(repos)
+    if content is None:  # stage the file exactly as the merge left it
+        repos.git(repos.work, "add", "--", "f.txt")
+    else:
+        resolve(repos, {"f.txt": content})
+    res = finish_commit(repos, setup, ["f.txt"])
+    assert_fail(res, "markers")
+    assert_no_commit(repos, setup)
+
+
+def test_f3_marker_already_in_stage1_blob_is_not_introduced(tmp_path):
+    repos = make_repos(tmp_path, {"README.md": "r\n", "f.txt": "a\n=======\nb\n"})
+    repos.advance_base({"f.txt": "a\n=======\nTHEIRS\n"})
+    repos.pr_commit({"f.txt": "a\n=======\nOURS\n"})
+    setup = start_merge(repos)
+    manifest = finish_manifest(setup.listing, ["f.txt"])
+    assert not manifest.startswith("-\t"), "f.txt must have a stage-1 blob"
+    resolve(repos, {"f.txt": "a\n=======\nRESOLVED\n"})
+    res = finish_commit(repos, setup, ["f.txt"])
+    assert res.returncode == 0, res.stderr
+    assert re.fullmatch(r"[0-9a-f]{40}", res.payload["merge_sha"])
+    assert not _merge_head(repos).exists()
+
+
+def test_f4_extra_staged_path_is_staged_unexpected(tmp_path):
+    repos = make_repos(tmp_path)
+    _content_conflict(repos)
+    setup = start_merge(repos)
+    resolve(repos, {"f.txt": RESOLVED_F, "README.md": "sneaked in\n"})
+    res = finish_commit(repos, setup, ["f.txt"])
+    assert_fail(res, "staged_unexpected")
+    assert "README.md" in res.stderr
+    assert_no_commit(repos, setup)
+
+
+def test_f5_auto_merged_path_reverted_to_head_is_staged_unexpected(tmp_path):
+    repos = make_repos(tmp_path)
+    repos.advance_base(
+        {"f.txt": "line1\nTHEIRS\nline3\n", "README.md": "readme from base\n"}
+    )
+    repos.pr_commit({"f.txt": "line1\nOURS\nline3\n"})
+    setup = start_merge(repos)
+    resolve(repos, {"f.txt": RESOLVED_F})
+    # Undo the auto-merged base change in both the index and the work tree.
+    repos.git(repos.work, "checkout", "-q", "HEAD", "--", "README.md")
+    assert (repos.work / "README.md").read_text(encoding="utf-8") == "readme\n"
+    res = finish_commit(repos, setup, ["f.txt"])
+    assert_fail(res, "staged_unexpected")
+    assert "README.md" in res.stderr
+    assert_no_commit(repos, setup)
+
+
+@pytest.mark.parametrize("mode", ["commit", "precheck"])
+def test_f6_foreign_merge_and_no_merge_head(tmp_path, mode):
+    repos = make_repos(tmp_path)
+    _content_conflict(repos)
+    payload = full(repos).payload
+    probe = parse_probe(payload)
+    setup = MergeSetup(
+        base_sha=probe.base_sha,
+        old_head=_head(repos),
+        merge_tree_oid=probe.listing.tree_oid,
+        listing=probe.listing,
+    )
+
+    def run(base_sha: str) -> ProbeRun:
+        if mode == "precheck":
+            return precheck(repos, base_sha)
+        return finish_commit(repos, setup, ["f.txt"], base_sha=base_sha)
+
+    # No merge in progress.
+    assert_fail(run(setup.base_sha), "no_merge_head")
+    assert _head(repos) == setup.old_head
+    # A merge of something other than the recorded base tip.
+    repos.git(
+        repos.work, "merge", "-q", "--no-commit", "--no-ff", setup.base_sha, check=False
+    )
+    resolve(repos, {"f.txt": RESOLVED_F})
+    other = repos.git(repos.work, "rev-parse", "HEAD~1").strip()
+    assert_fail(run(other), "foreign_merge")
+    assert_no_commit(repos, setup)
+
+
+def test_f7_unstaged_edit_to_tracked_file_is_tree_dirty(tmp_path):
+    repos = make_repos(tmp_path)
+    _content_conflict(repos)
+    setup = start_merge(repos)
+    resolve(repos, {"f.txt": RESOLVED_F})
+    (repos.work / "README.md").write_text("operator edit\n", encoding="utf-8")
+    res = finish_commit(repos, setup, ["f.txt"])
+    assert_fail(res, "tree_dirty")
+    assert_no_commit(repos, setup)
+
+
+def test_f8_precheck_tree_dirty_and_ok(tmp_path):
+    repos = make_repos(tmp_path, _BASE_FG)
+    _two_file_conflict(repos)
+    setup = start_merge(repos)
+    # Only the unmerged paths differ between the work tree and the index.
+    ok = precheck(repos, setup.base_sha)
+    assert ok.returncode == 0, ok.stderr
+    assert ok.payload == {"precheck": "ok"}
+    # A resolved, staged path is fine too.
+    resolve(repos, {"f.txt": RESOLVED_F})
+    assert precheck(repos, setup.base_sha).payload == {"precheck": "ok"}
+    # An operator edit to a non-conflicted tracked file is not.
+    (repos.work / "README.md").write_text("operator edit\n", encoding="utf-8")
+    res = precheck(repos, setup.base_sha)
+    assert_fail(res, "tree_dirty")
+    assert "README.md" in res.stderr
+    assert_no_commit(repos, setup)
+
+
+def test_f9_failing_pre_commit_hook_is_hook_rejected(tmp_path):
+    repos = make_repos(tmp_path)
+    _content_conflict(repos)
+    setup = start_merge(repos)
+    resolve(repos, {"f.txt": RESOLVED_F})
+    hook = repos.work / ".git" / "hooks" / "pre-commit"
+    hook.parent.mkdir(parents=True, exist_ok=True)
+    hook_output = "pre-commit: lint failed on f.txt\n  detail line 2 (#305)\n"
+    hook.write_text(
+        "#!/usr/bin/env bash\n"
+        "printf 'pre-commit: lint failed on f.txt\\n'\n"
+        "printf '  detail line 2 (#305)\\n' >&2\n"
+        "exit 1\n",
+        encoding="utf-8",
+    )
+    hook.chmod(0o755)
+    res = finish_commit(repos, setup, ["f.txt"])
+    assert_fail(res, "hook_rejected")
+    assert hook_output in res.stderr
+    assert_no_commit(repos, setup)
+
+
+def test_f10_clean_resolution_is_the_exact_merge_commit(tmp_path):
+    repos = make_repos(tmp_path)
+    _content_conflict(repos)
+    setup = start_merge(repos)
+    resolve(repos, {"f.txt": RESOLVED_F})
+    # --base-sha is compared case-insensitively with MERGE_HEAD.
+    res = finish_commit(repos, setup, ["f.txt"], base_sha=setup.base_sha.upper())
+    assert res.returncode == 0, res.stderr
+    payload = res.payload
+    assert set(payload) == {"merge_sha", "parents"}
+    assert payload["merge_sha"] == _head(repos)
+    assert payload["parents"] == [setup.old_head, setup.base_sha]
+    rev_list = repos.git(repos.work, "rev-list", "--parents", "-n", "1", "HEAD").split()
+    assert rev_list[0] == payload["merge_sha"]
+    parents = rev_list[1:]
+    assert parents == [setup.old_head, setup.base_sha]
+    assert merge_parent_ok(parents, setup.old_head, setup.base_sha) is True
+    assert _status(repos) == ""
+    assert not _merge_head(repos).exists()
+    body = repos.git(repos.work, "log", "-1", "--format=%B")
+    assert body.rstrip("\n") == MESSAGE.rstrip("\n")
+    assert repos.git(repos.work, "show", "HEAD:f.txt") == RESOLVED_F
+
+
+def test_f11_merge_abort_after_a_halt_restores_the_pre_merge_state(tmp_path):
+    repos = make_repos(tmp_path)
+    _content_conflict(repos)
+    (repos.work / "untracked.txt").write_text("keep me\n", encoding="utf-8")
+    files = ("README.md", "f.txt", "untracked.txt")
+
+    def state() -> tuple:
+        return (
+            _head(repos),
+            repos.git(repos.work, "ls-files", "-s", "-z"),
+            _status(repos),
+            {p: (repos.work / p).read_bytes() for p in files},
+        )
+
+    before = state()
+    setup = start_merge(repos)
+    repos.git(repos.work, "add", "--", "f.txt")  # markers left: the gate halts
+    assert_fail(finish_commit(repos, setup, ["f.txt"]), "markers")
+    repos.git(repos.work, "merge", "--abort")
+    assert state() == before
+    assert not _merge_head(repos).exists()
+
+
+def test_f12_dirty_pyproject_before_the_merge_blocks_it(tmp_path):
+    repos = make_repos(
+        tmp_path,
+        {
+            "README.md": "readme\n",
+            "f.txt": "line1\nline2\nline3\n",
+            "pyproject.toml": '[project]\nname = "x"\nversion = "0.1.0"\n',
+        },
+    )
+    _content_conflict(repos)
+    pr_head = _head(repos)
+    (repos.work / "pyproject.toml").write_text(
+        '[project]\nname = "x"\nversion = "0.2.0-local"\n', encoding="utf-8"
+    )
+    payload = full(repos).payload
+    probe = parse_probe(payload)
+    assert payload["tree_clean"] is False
+    ok, paths = merge_preflight_ok(probe.status_porcelain)
+    assert (ok, paths) == (False, ["pyproject.toml"])
+    # The gate is false, so the flow never starts the merge: nothing was merged.
+    assert not _merge_head(repos).exists()
+    assert _head(repos) == pr_head
+    ancestor = subprocess.run(
+        [GIT, "merge-base", "--is-ancestor", probe.base_sha, "HEAD"],
+        cwd=repos.work,
+        env=repos.env,
+        capture_output=True,
+        timeout=30,
+    )
+    assert ancestor.returncode == 1
+    assert_fail(precheck(repos, probe.base_sha), "no_merge_head")
+    assert "0.2.0-local" in (repos.work / "pyproject.toml").read_text(encoding="utf-8")
+
+
+# ---------------------------------------------------------------------------
+# Further contract rows of section 7.2
+# ---------------------------------------------------------------------------
+
+
+def test_path_resolved_by_deletion_skips_the_marker_check(tmp_path):
+    repos = make_repos(tmp_path, {"d.txt": "keep\n", "README.md": "r\n"})
+    repos.advance_base({"d.txt": None})
+    repos.pr_commit({"d.txt": "modified\n"})
+    setup = start_merge(repos)
+    repos.git(repos.work, "rm", "-q", "--", "d.txt")
+    res = finish_commit(repos, setup, ["d.txt"])
+    assert res.returncode == 0, res.stderr
+    assert res.payload["parents"] == [setup.old_head, setup.base_sha]
+    assert repos.git(repos.work, "ls-files", "--", "d.txt") == ""
+
+
+@pytest.mark.parametrize(
+    "extra",
+    [
+        ("--precheck", "--manifest", "m.txt"),
+        ("--precheck", "--merge-tree-oid", "a" * 40),
+        ("--precheck", "--message-file", "msg.txt"),
+        ("--merge-tree-oid", "a" * 40, "--manifest", "m.txt"),
+        ("--precheck", "--bogus"),
+        ("--precheck", "--base-sha", "abc"),
+    ],
+    ids=[
+        "precheck-manifest",
+        "precheck-tree",
+        "precheck-message",
+        "commit-missing-message",
+        "unknown",
+        "short-sha",
+    ],
+)
+def test_usage_errors(tmp_path, extra):
+    repos = make_repos(tmp_path)
+    _content_conflict(repos)
+    setup = start_merge(repos)
+    (repos.work / "m.txt").write_text("-\tf.txt\n", encoding="utf-8")
+    (repos.work / "msg.txt").write_text("msg\n", encoding="utf-8")
+    res = run_finish(repos, "--base-sha", setup.base_sha, *extra)
+    assert_fail(res, "usage")
+    assert_no_commit(repos, setup)
+
+
+@pytest.mark.parametrize(
+    "manifest",
+    ["no tab here\n", "short\tf.txt\n", "-\t\n", "-\tf.txt\n-\tf.txt\n"],
+    ids=["no-tab", "bad-oid", "empty-path", "duplicate"],
+)
+def test_malformed_manifest_is_usage(tmp_path, manifest):
+    repos = make_repos(tmp_path)
+    _content_conflict(repos)
+    setup = start_merge(repos)
+    resolve(repos, {"f.txt": RESOLVED_F})
+    (repos.root / "bad-manifest.txt").write_text(manifest, encoding="utf-8")
+    (repos.root / "msg.txt").write_text(MESSAGE, encoding="utf-8")
+    res = run_finish(
+        repos,
+        "--base-sha",
+        setup.base_sha,
+        "--merge-tree-oid",
+        setup.merge_tree_oid,
+        "--manifest",
+        str(repos.root / "bad-manifest.txt"),
+        "--message-file",
+        str(repos.root / "msg.txt"),
+    )
+    assert_fail(res, "usage")
+    assert_no_commit(repos, setup)
+
+
+def test_finish_script_static_rules():
+    text = FINISH.read_text(encoding="utf-8")
+    assert text.startswith("#!/usr/bin/env bash\n")
+    assert "\nset -u -o pipefail\n" in text
+    assert os.access(FINISH, os.X_OK)
+    # The only commit is one `git commit -F`, with hooks on.
+    assert len(re.findall(r"\bgit\s+commit\b", text)) == 1
+    assert len(re.findall(r"\bgit commit -F \"\$MESSAGE_FILE\"", text)) == 1
+    for pattern in (
+        r"\bgit\s+push\b",
+        r"(?i)stash",
+        r"(?i)force",
+        r"\bgit\s+config\b",
+        r"--no-verify\b",
+        r"--amend\b",
+        r"\bcommit\s+(-a|--all|--only)\b",
+        r"src/superclaude",
+        r"\bgit\s+(checkout|switch|reset|add|worktree|rebase|merge)\b",
+        r"\bgh\b",
+    ):
+        assert re.search(pattern, text) is None, pattern
+    ls = subprocess.run(
+        [GIT, "ls-files", "-s", "--", FINISH_REL],
+        cwd=REPO_ROOT,
+        text=True,
+        capture_output=True,
+        timeout=30,
+    ).stdout
+    if ls:  # the index entry exists once the path is staged
+        assert ls.startswith("100755 "), ls
diff --git a/.dev/tasks/to-do/TASK-WF-design-20261104-164423/artifacts/t11-tests.log b/.dev/tasks/to-do/TASK-WF-design-20261104-164423/artifacts/t11-tests.log
new file mode 100644
index 00000000..4fa8b09c
--- /dev/null
+++ b/.dev/tasks/to-do/TASK-WF-design-20261104-164423/artifacts/t11-tests.log
@@ -0,0 +1,14 @@
+============================= test session starts ==============================
+platform linux -- Python 3.11.15, pytest-9.2.0, pluggy-1.7.0
+SuperClaude: 5.0.0
+benchmark: 5.3.1 (defaults: timer=time.perf_counter disable_gc=False min_rounds=5 min_time=0.000005 max_time=1.0 calibration_precision=10 warmup=False warmup_iterations=100000)
+rootdir: /home/coder/workspaces/worktrees/IronClaude/issue-305-pr-submit-conflicts
+configfile: pyproject.toml
+plugins: superclaude-5.0.0, benchmark-5.3.1, anyio-4.16.0, cov-7.1.0
+collected 76 items
+
+tests/pr_submit/test_conflict_scripts.py ............................... [ 40%]
+..........................                                               [ 75%]
+tests/pr_submit/test_static_grep.py ...................                  [100%]
+
+============================= 76 passed in 12.04s ==============================
diff --git a/.dev/tasks/to-do/TASK-WF-design-20261104-164423/artifacts/t11-grep.txt b/.dev/tasks/to-do/TASK-WF-design-20261104-164423/artifacts/t11-grep.txt
new file mode 100644
index 00000000..402ea6b3
--- /dev/null
+++ b/.dev/tasks/to-do/TASK-WF-design-20261104-164423/artifacts/t11-grep.txt
@@ -0,0 +1,26 @@
+# t11 forbidden-item grep over src/superclaude/skills/sc-pr-submit-protocol/scripts/finish-merge.sh (no output under a heading = no hit)
+## grep -n -i -E -e 'git[[:space:]]+push'
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
+## grep -n -i -E -e 'git[[:space:]]+(checkout|switch|reset|add|worktree|rebase|merge)\b'
+exit=1
+## git commit occurrences (expect exactly one, the -F line)
+254:if ! git commit -F "$MESSAGE_FILE" >"$TMP/commit.out" 2>&1; then
+count=1
+## gh calls (each must carry --repo "$REPO"; none expected)
+exit=1
+## set line
+29:set -u -o pipefail
diff --git a/.dev/tasks/to-do/TASK-WF-design-20261104-164423/artifacts/t11-mode.txt b/.dev/tasks/to-do/TASK-WF-design-20261104-164423/artifacts/t11-mode.txt
new file mode 100644
index 00000000..d8653039
--- /dev/null
+++ b/.dev/tasks/to-do/TASK-WF-design-20261104-164423/artifacts/t11-mode.txt
@@ -0,0 +1,2 @@
+100755 8ac4c485f5bef0cbc704f0c5af777b81b3bc4af2 0	src/superclaude/skills/sc-pr-submit-protocol/scripts/finish-merge.sh
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

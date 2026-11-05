b6b97b30f2c8a1c4cff292aad80e8ced206a2c94
Review one task for spec compliance.

Task brief: ## Task 10: Create the read-only probe `probe-merge.sh`

Depends on: Task 3

Create `src/superclaude/skills/sc-pr-submit-protocol/scripts/probe-merge.sh` (git mode 100755) per the script rules at the top of source section 7 and source section 7.1 (both modes, all 14 full-mode steps, base64 transport, the JSON contract and the `PROBE_FAIL` reasons). Create `tests/pr_submit/test_conflict_scripts.py` with the `make_repos(tmp_path)` fixture helper of source section 12.4 and cases P1 to P12, parsing probe output with `conflicts.parse_probe` / `conflict_plan`, and a module-level capability skip unless `git merge-tree --write-tree HEAD HEAD` works in a scratch repository.

Acceptance criteria:
- P1 to P12 of source section 12.4 pass; P8 proves `git status --porcelain=v1 -z` and `HEAD` are unchanged by the probe.
- `--repo` not matching origin gives exit 2 and `PROBE_FAIL origin_mismatch` with no fetch.
- The script has no `git push` line, no stash, no config write, no hook-skipping flag and no `src/superclaude/` text; `git ls-files -s` shows mode 100755.
- `uv run pytest tests/pr_submit/test_conflict_scripts.py tests/pr_submit/test_static_grep.py -q` passes; log saved to `./artifacts/t10-tests.log`.
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
Start sha: b6b97b30f2c8a1c4cff292aad80e8ced206a2c94
Diff against the start snapshot: diff --git a/src/superclaude/skills/sc-pr-submit-protocol/scripts/probe-merge.sh b/src/superclaude/skills/sc-pr-submit-protocol/scripts/probe-merge.sh
new file mode 100755
index 00000000..4db4a378
--- /dev/null
+++ b/src/superclaude/skills/sc-pr-submit-protocol/scripts/probe-merge.sh
@@ -0,0 +1,238 @@
+#!/usr/bin/env bash
+#
+# probe-merge.sh — read-only merge probe for sc:pr-submit conflict cycles (issue #305).
+#
+# Purpose : Report, without changing anything, whether HEAD merges cleanly with the
+#           base branch, which paths conflict and at which stages, and whether a
+#           foreign operation (merge, rebase, cherry-pick, revert) is in progress.
+#           It never changes the index, the work tree, HEAD or any branch. It may
+#           write unreachable tree objects (harmless) and the fetch updates
+#           refs/remotes/origin/<base>.
+# Usage   : probe-merge.sh --repo <owner/repo> --ops-only
+#           probe-merge.sh --repo <owner/repo> --base <branch> [--program <name>]...
+# Output  : exactly one stdout line. Success is one JSON object:
+#           ops mode  {"ok":true,"mode":"ops","foreign_op":..,"merge_head":..}
+#           full mode {"ok":true,"mode":"full","merge_tree_supported":..,"base_ref":..,
+#           "base_sha":..,"head_sha":..,"merge_base":..,"behind":N,"ahead":N,
+#           "foreign_op":..,"merge_head":..,"tree_clean":..,"status_b64":..,"clean":..,
+#           "merge_tree_b64":..,"numstat_ours_b64":..,"numstat_theirs_b64":..,
+#           "programs":[..],"truncated":..}
+#           Failure is the token "PROBE_FAIL <reason>"; details go to stderr.
+# Exit    : 0 on any completed probe; 2 with PROBE_FAIL usage | not_a_worktree |
+#           origin_mismatch | bad_base | fetch_failed | no_merge_base | merge_tree_failed.
+# Contract: the JSON is validated by superclaude.pr_submit.conflicts.parse_probe
+#           (design section 7.1). No stdin read, no prompt, no stored config write.
+
+set -u -o pipefail
+
+MAX_BYTES=102400
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
+    printf 'probe-merge: %s\n' "$2" >&2
+    printf 'PROBE_FAIL %s\n' "$1"
+    exit 2
+}
+
+# Run a git command that can block under `timeout 60` when timeout is on PATH.
+git_blocking() {
+    if command -v timeout >/dev/null 2>&1; then
+        timeout 60 git "$@"
+    else
+        git "$@"
+    fi
+}
+
+# Step 1: arguments.
+REPO=""
+BASE=""
+OPS_ONLY=0
+PROGRAMS=()
+while [ $# -gt 0 ]; do
+    case "$1" in
+        --repo|--base|--program)
+            [ $# -ge 2 ] || fail usage "missing value for $1"
+            case "$1" in
+                --repo) REPO="$2" ;;
+                --base) BASE="$2" ;;
+                --program) PROGRAMS+=("$2") ;;
+            esac
+            shift 2
+            ;;
+        --ops-only) OPS_ONLY=1; shift ;;
+        *) fail usage "unknown argument: $1" ;;
+    esac
+done
+[ -n "$REPO" ] || fail usage "missing required --repo <owner/repo>"
+[ "$OPS_ONLY" -eq 1 ] || [ -n "$BASE" ] || fail usage "missing required --base <branch> (or pass --ops-only)"
+command -v jq >/dev/null 2>&1 || fail usage "jq not found on PATH"
+command -v base64 >/dev/null 2>&1 || fail usage "base64 not found on PATH"
+
+# Step 2: inside a work tree.
+INSIDE="$(git rev-parse --is-inside-work-tree 2>/dev/null)" || INSIDE=""
+[ "$INSIDE" = "true" ] || fail not_a_worktree "not inside a git work tree"
+
+# Step 3: origin must be the given repo, so the fetch can only reach it.
+ORIGIN_REPO="$(git remote get-url origin 2>/dev/null | sed -E 's#^ssh://[^/]+/##; s#^git@[^:]+:##; s#^https?://[^/]+/##; s#\.git$##')" || ORIGIN_REPO=""
+[ -n "$ORIGIN_REPO" ] && [ "$ORIGIN_REPO" = "$REPO" ] \
+    || fail origin_mismatch "origin resolves to '${ORIGIN_REPO}', not '${REPO}'; nothing fetched"
+
+# Step 4: foreign operation and MERGE_HEAD (worktree-aware paths).
+FOREIGN_OP=""
+for name in MERGE_HEAD rebase-merge rebase-apply CHERRY_PICK_HEAD REVERT_HEAD sequencer; do
+    op_path="$(git rev-parse --git-path "$name" 2>/dev/null)" || continue
+    if [ -n "$op_path" ] && [ -e "$op_path" ]; then
+        FOREIGN_OP="$name"
+        break
+    fi
+done
+MERGE_HEAD_SHA="$(git rev-parse -q --verify 'MERGE_HEAD^{commit}' 2>/dev/null)" || MERGE_HEAD_SHA=""
+
+if [ "$OPS_ONLY" -eq 1 ]; then
+    jq -nc --arg op "$FOREIGN_OP" --arg mh "$MERGE_HEAD_SHA" \
+        '{ok: true, mode: "ops",
+          foreign_op: (if $op == "" then null else $op end),
+          merge_head: (if $mh == "" then null else $mh end)}' \
+        || fail usage "could not render the probe JSON"
+    exit 0
+fi
+
+# Step 5: the base branch name.
+case "$BASE" in
+    -*) fail bad_base "base branch name starts with '-': $BASE" ;;
+esac
+git check-ref-format --branch "$BASE" >/dev/null 2>&1 || fail bad_base "not a valid branch name: $BASE"
+
+# Temporary files live only under the repository's git directory.
+TMP_ROOT="$(git rev-parse --git-path sc-pr-submit-tmp 2>/dev/null)" || TMP_ROOT=""
+[ -n "$TMP_ROOT" ] || fail usage "cannot resolve the git directory for temporary files"
+mkdir -p -- "$TMP_ROOT" 2>/dev/null || fail usage "cannot create $TMP_ROOT"
+TMP="$(mktemp -d "$TMP_ROOT/probe.XXXXXXXX" 2>/dev/null)" || { TMP=""; fail usage "cannot create a temporary directory under $TMP_ROOT"; }
+
+# Step 6: tracked-file status (untracked files ignored). No optional index refresh.
+git --no-optional-locks status --porcelain=v1 --untracked-files=no -z >"$TMP/status" 2>/dev/null \
+    || fail not_a_worktree "git status failed"
+TREE_CLEAN=false
+[ -s "$TMP/status" ] || TREE_CLEAN=true
+
+# Step 7: fetch the base branch from origin only.
+if ! git_blocking fetch --no-tags origin "$BASE" >/dev/null 2>"$TMP/fetch.err"; then
+    cat -- "$TMP/fetch.err" >&2
+    fail fetch_failed "cannot reach remote origin (git fetch of '$BASE' failed)"
+fi
+BASE_SHA="$(git rev-parse -q --verify "refs/remotes/origin/${BASE}^{commit}" 2>/dev/null)" \
+    || fail fetch_failed "refs/remotes/origin/$BASE is missing after the fetch"
+
+# Step 8: head, merge base, behind / ahead.
+HEAD_SHA="$(git rev-parse -q --verify 'HEAD^{commit}' 2>/dev/null)" || fail no_merge_base "HEAD does not name a commit"
+MERGE_BASE="$(git merge-base HEAD "$BASE_SHA" 2>/dev/null)" \
+    || fail no_merge_base "HEAD and origin/$BASE share no merge base"
+COUNTS="$(git rev-list --left-right --count "${BASE_SHA}...HEAD" 2>/dev/null)" \
+    || fail no_merge_base "cannot count commits between origin/$BASE and HEAD"
+read -r BEHIND AHEAD <<EOF_COUNTS
+$COUNTS
+EOF_COUNTS
+case "${BEHIND:-x}${AHEAD:-x}" in
+    *[!0-9]*) fail no_merge_base "unexpected rev-list count output: $COUNTS" ;;
+esac
+
+# Step 13 (computed early; it reads nothing from the repository): available programs.
+FOUND_PROGRAMS=()
+for prog in ${PROGRAMS[@]+"${PROGRAMS[@]}"}; do
+    if command -v -- "$prog" >/dev/null 2>&1; then
+        FOUND_PROGRAMS+=("$prog")
+    fi
+done
+PROGRAMS_JSON="$(printf '%s\n' ${FOUND_PROGRAMS[@]+"${FOUND_PROGRAMS[@]}"} | jq -Rsc 'split("\n") | map(select(. != ""))')" \
+    || fail usage "could not render the program list"
+
+# emit <supported> <clean> : print the one JSON line (step 14) and exit 0.
+# A captured file above MAX_BYTES makes the probe truncated (step 12): every *_b64 null.
+emit() {
+    local supported="$1" clean="$2" truncated=false nulls='[]' f key
+    for f in status merge_tree numstat_ours numstat_theirs; do
+        if [ -f "$TMP/$f" ] && [ "$(wc -c <"$TMP/$f")" -gt "$MAX_BYTES" ]; then
+            truncated=true
+        fi
+    done
+    for key in status merge_tree numstat_ours numstat_theirs; do
+        if [ "$truncated" = true ] || [ ! -f "$TMP/$key" ]; then
+            nulls="$(jq -nc --argjson n "$nulls" --arg k "${key}_b64" '$n + [$k]')"
+            : >"$TMP/$key.b64"
+        else
+            base64 <"$TMP/$key" | tr -d '\n' >"$TMP/$key.b64"
+        fi
+    done
+    jq -nc \
+        --argjson supported "$supported" \
+        --arg base_ref "origin/$BASE" \
+        --arg base_sha "$BASE_SHA" \
+        --arg head_sha "$HEAD_SHA" \
+        --arg merge_base "$MERGE_BASE" \
+        --argjson behind "$BEHIND" \
+        --argjson ahead "$AHEAD" \
+        --arg op "$FOREIGN_OP" \
+        --arg mh "$MERGE_HEAD_SHA" \
+        --argjson tree_clean "$TREE_CLEAN" \
+        --argjson clean "$clean" \
+        --argjson programs "$PROGRAMS_JSON" \
+        --argjson truncated "$truncated" \
+        --argjson nulls "$nulls" \
+        --rawfile status_b64 "$TMP/status.b64" \
+        --rawfile merge_tree_b64 "$TMP/merge_tree.b64" \
+        --rawfile numstat_ours_b64 "$TMP/numstat_ours.b64" \
+        --rawfile numstat_theirs_b64 "$TMP/numstat_theirs.b64" \
+        '{ok: true, mode: "full", merge_tree_supported: $supported,
+          base_ref: $base_ref, base_sha: $base_sha, head_sha: $head_sha, merge_base: $merge_base,
+          behind: $behind, ahead: $ahead,
+          foreign_op: (if $op == "" then null else $op end),
+          merge_head: (if $mh == "" then null else $mh end),
+          tree_clean: $tree_clean, status_b64: $status_b64,
+          clean: $clean, merge_tree_b64: $merge_tree_b64,
+          numstat_ours_b64: $numstat_ours_b64, numstat_theirs_b64: $numstat_theirs_b64,
+          programs: $programs, truncated: $truncated}
+         | reduce $nulls[] as $k (.; .[$k] = null)' \
+        || fail usage "could not render the probe JSON"
+    exit 0
+}
+
+# Step 9: capability by behaviour, never by version.
+if ! git merge-tree --write-tree HEAD HEAD >/dev/null 2>&1; then
+    printf 'probe-merge: git merge-tree --write-tree is not supported here\n' >&2
+    emit false null
+fi
+
+# Step 10: the merge itself, written as objects only.
+git merge-tree --write-tree -z HEAD "$BASE_SHA" >"$TMP/merge_tree" 2>"$TMP/merge_tree.err"
+MT_EXIT=$?
+case "$MT_EXIT" in
+    0) CLEAN=true ;;
+    1) CLEAN=false ;;
+    *)
+        cat -- "$TMP/merge_tree.err" >&2
+        fail merge_tree_failed "git merge-tree exited $MT_EXIT"
+        ;;
+esac
+
+# Step 11: per-side numstat (binary detection) only when the merge conflicts.
+if [ "$CLEAN" = false ]; then
+    git --no-optional-locks diff --numstat -z --no-renames --no-ext-diff --no-textconv \
+        "$MERGE_BASE" HEAD >"$TMP/numstat_ours" 2>/dev/null \
+        || fail merge_tree_failed "numstat of HEAD against the merge base failed"
+    git --no-optional-locks diff --numstat -z --no-renames --no-ext-diff --no-textconv \
+        "$MERGE_BASE" "$BASE_SHA" >"$TMP/numstat_theirs" 2>/dev/null \
+        || fail merge_tree_failed "numstat of origin/$BASE against the merge base failed"
+fi
+
+# Steps 12 and 14.
+emit true "$CLEAN"
diff --git a/tests/pr_submit/test_conflict_scripts.py b/tests/pr_submit/test_conflict_scripts.py
new file mode 100644
index 00000000..c3a0f343
--- /dev/null
+++ b/tests/pr_submit/test_conflict_scripts.py
@@ -0,0 +1,630 @@
+"""Hermetic real-git tests for the conflict scripts (design section 12.4).
+
+This module covers ``scripts/probe-merge.sh`` (cases P1 to P12). Every git call runs
+inside a pytest temporary directory, with a local bare repository as ``origin`` and a
+``gh`` stub first on ``PATH``. ``GIT_CONFIG_GLOBAL=/dev/null``, ``GIT_CONFIG_NOSYSTEM=1``
+and a fixed author and committer are set for every git call; ``HOME`` points into the
+temporary directory. Nothing here touches the network or the operator's ``~/.claude``.
+Probe output is parsed with ``conflicts.parse_probe`` and ``conflicts.conflict_plan``.
+"""
+
+from __future__ import annotations
+
+import base64
+import json
+import os
+import re
+import shutil
+import subprocess
+import tempfile
+from dataclasses import dataclass
+from pathlib import Path
+
+import pytest
+
+from superclaude.pr_submit.conflicts import (
+    MAX_PROBE_BYTES,
+    conflict_plan,
+    group_entries,
+    parse_probe,
+)
+
+REPO_ROOT = Path(__file__).resolve().parents[2]
+SKILL_DIR = REPO_ROOT / "src" / "superclaude" / "skills" / "sc-pr-submit-protocol"
+PROBE = SKILL_DIR / "scripts" / "probe-merge.sh"
+PROBE_REL = "src/superclaude/skills/sc-pr-submit-protocol/scripts/probe-merge.sh"
+
+GIT = shutil.which("git")
+
+_FIXED_IDENTITY = {
+    "GIT_CONFIG_GLOBAL": "/dev/null",
+    "GIT_CONFIG_NOSYSTEM": "1",
+    "GIT_AUTHOR_NAME": "Probe Test",
+    "GIT_AUTHOR_EMAIL": "probe-test@example.com",
+    "GIT_COMMITTER_NAME": "Probe Test",
+    "GIT_COMMITTER_EMAIL": "probe-test@example.com",
+    "GIT_TERMINAL_PROMPT": "0",
+    "LC_ALL": "C",
+}
+
+
+def _base_env(home: Path) -> dict[str, str]:
+    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
+    env.update(_FIXED_IDENTITY)
+    env["HOME"] = str(home)
+    return env
+
+
+def _merge_tree_works() -> bool:
+    """Capability by behaviour (never a version parse): ``merge-tree --write-tree``."""
+    if GIT is None or shutil.which("jq") is None or shutil.which("bash") is None:
+        return False
+    with tempfile.TemporaryDirectory() as scratch:
+        env = _base_env(Path(scratch))
+        repo = Path(scratch) / "r"
+        try:
+            for argv in (
+                ["init", "-q", "-b", "main", str(repo)],
+                ["-C", str(repo), "commit", "-q", "--allow-empty", "-m", "seed"],
+                ["-C", str(repo), "merge-tree", "--write-tree", "HEAD", "HEAD"],
+            ):
+                subprocess.run(
+                    [GIT, *argv], env=env, check=True, capture_output=True, timeout=30
+                )
+        except (subprocess.SubprocessError, OSError):
+            return False
+    return True
+
+
+pytestmark = pytest.mark.skipif(
+    not _merge_tree_works(),
+    reason="git merge-tree --write-tree (or jq) is not available here",
+)
+
+
+# ---------------------------------------------------------------------------
+# Fixture helper (design section 12.4)
+# ---------------------------------------------------------------------------
+
+
+@dataclass
+class Repos:
+    root: Path
+    origin: Path  # bare repository used as `origin`
+    seed: Path  # second clone that advances the base branch on origin
+    work: Path  # clone with the PR branch `pr` checked out
+    bin_dir: Path  # first on PATH; holds the gh stub
+    gh_calls: Path
+    env: dict[str, str]
+
+    @property
+    def repo_slug(self) -> str:
+        """What the probe resolves from the origin URL (the `.git` suffix stripped)."""
+        return re.sub(r"\.git$", "", str(self.origin))
+
+    def git(self, cwd: Path, *args: str, check: bool = True) -> str:
+        res = subprocess.run(
+            [GIT, *args],
+            cwd=cwd,
+            env=self.env,
+            text=True,
+            capture_output=True,
+            timeout=60,
+        )
+        if check and res.returncode != 0:
+            raise AssertionError(f"git {args} failed: {res.stderr}")
+        return res.stdout
+
+    def write(self, repo: Path, files: dict[str, bytes | str | None]) -> None:
+        for rel, content in files.items():
+            if content is None:
+                self.git(repo, "rm", "-q", "--", rel)
+                continue
+            path = repo / rel
+            path.parent.mkdir(parents=True, exist_ok=True)
+            if isinstance(content, bytes):
+                path.write_bytes(content)
+            else:
+                path.write_text(content, encoding="utf-8")
+        added = [rel for rel, content in files.items() if content is not None]
+        if added:
+            self.git(repo, "add", "--", *added)
+
+    def commit(self, repo: Path, files: dict[str, bytes | str | None], msg: str) -> str:
+        self.write(repo, files)
+        self.git(repo, "commit", "-q", "-m", msg)
+        return self.git(repo, "rev-parse", "HEAD").strip()
+
+    def advance_base(self, files: dict[str, bytes | str | None]) -> str:
+        sha = self.commit(self.seed, files, "base advance")
+        self.git(self.seed, "push", "-q", "origin", "main:main")
+        return sha
+
+    def pr_commit(self, files: dict[str, bytes | str | None]) -> str:
+        return self.commit(self.work, files, "pr change")
+
+    def gh_call_lines(self) -> list[str]:
+        if not self.gh_calls.exists():
+            return []
+        return self.gh_calls.read_text(encoding="utf-8").splitlines()
+
+
+def make_repos(tmp_path: Path, base_files: dict[str, bytes | str] | None = None):
+    """Create `origin.git` (bare), a `seed` clone on `main` and a `work` clone with
+    the PR branch `pr` checked out, plus a `gh` stub on PATH that records calls and
+    serves canned JSON."""
+    home = tmp_path / "home"
+    home.mkdir()
+    bin_dir = tmp_path / "bin"
+    bin_dir.mkdir()
+    gh_calls = tmp_path / "gh-calls.log"
+    gh = bin_dir / "gh"
+    gh.write_text(
+        "#!/usr/bin/env bash\n"
+        f"printf '%s\\n' \"$*\" >> '{gh_calls}'\n"
+        "printf '{}\\n'\n",
+        encoding="utf-8",
+    )
+    gh.chmod(0o755)
+    env = _base_env(home)
+    env["PATH"] = f"{bin_dir}{os.pathsep}{os.environ.get('PATH', '')}"
+    repos = Repos(
+        root=tmp_path,
+        origin=tmp_path / "origin.git",
+        seed=tmp_path / "seed",
+        work=tmp_path / "work",
+        bin_dir=bin_dir,
+        gh_calls=gh_calls,
+        env=env,
+    )
+    repos.git(tmp_path, "init", "-q", "--bare", "-b", "main", str(repos.origin))
+    repos.git(tmp_path, "init", "-q", "-b", "main", str(repos.seed))
+    repos.git(repos.seed, "remote", "add", "origin", str(repos.origin))
+    repos.commit(
+        repos.seed,
+        base_files or {"README.md": "readme\n", "f.txt": "line1\nline2\nline3\n"},
+        "base",
+    )
+    repos.git(repos.seed, "push", "-q", "origin", "main:main")
+    repos.git(tmp_path, "clone", "-q", str(repos.origin), str(repos.work))
+    repos.git(repos.work, "checkout", "-q", "-b", "pr")
+    return repos
+
+
+# ---------------------------------------------------------------------------
+# Probe runner
+# ---------------------------------------------------------------------------
+
+
+@dataclass
+class ProbeRun:
+    returncode: int
+    stdout: str
+    stderr: str
+
+    @property
+    def payload(self) -> dict:
+        assert self.returncode == 0, self.stderr
+        lines = self.stdout.splitlines()
+        assert len(lines) == 1, self.stdout
+        return json.loads(lines[0])
+
+
+def _status(repos: Repos) -> str:
+    """`git status --porcelain=v1 -z` without the optional index refresh, so the
+    test itself never rewrites the index it compares."""
+    return repos.git(
+        repos.work, "--no-optional-locks", "status", "--porcelain=v1", "-z"
+    )
+
+
+def _snapshot(repos: Repos) -> tuple[str, str, bytes]:
+    status = _status(repos)
+    head = repos.git(repos.work, "rev-parse", "HEAD", check=False)
+    index = repos.work / ".git" / "index"
+    return status, head, index.read_bytes() if index.exists() else b""
+
+
+def run_probe(repos: Repos, *args: str, env: dict[str, str] | None = None) -> ProbeRun:
+    """Run the probe from its source path in `work`; assert it changed nothing."""
+    before = _snapshot(repos)
+    res = subprocess.run(
+        [str(PROBE), *args],
+        cwd=repos.work,
+        env=env or repos.env,
+        text=True,
+        capture_output=True,
+        timeout=120,
+    )
+    assert _snapshot(repos) == before, "the probe changed status, HEAD or the index"
+    assert not (repos.work / ".git" / "sc-pr-submit-tmp").exists()
+    assert repos.gh_call_lines() == [], "the probe must not call gh"
+    return ProbeRun(res.returncode, res.stdout, res.stderr)
+
+
+def full(repos: Repos, *extra: str, env: dict[str, str] | None = None) -> ProbeRun:
+    return run_probe(
+        repos, "--repo", repos.repo_slug, "--base", "main", *extra, env=env
+    )
+
+
+def _decode(payload: dict, key: str) -> str:
+    return base64.b64decode(payload[key], validate=True).decode("utf-8")
+
+
+def _content_conflict(repos: Repos) -> None:
+    repos.advance_base({"f.txt": "line1\nTHEIRS\nline3\n"})
+    repos.pr_commit({"f.txt": "line1\nOURS\nline3\n"})
+
+
+# ---------------------------------------------------------------------------
+# P1 to P12
+# ---------------------------------------------------------------------------
+
+
+def test_p1_base_advanced_without_overlap_is_clean(tmp_path):
+    repos = make_repos(tmp_path)
+    base_sha = repos.advance_base({"other.txt": "from base\n"})
+    head_sha = repos.pr_commit({"pr.txt": "from pr\n"})
+    payload = full(repos).payload
+    probe = parse_probe(payload)
+    assert payload["clean"] is True
+    assert payload["numstat_ours_b64"] is None
+    assert payload["numstat_theirs_b64"] is None
+    assert probe.clean is True
+    assert probe.behind > 0 and probe.behind == 1
+    assert probe.ahead == 1
+    assert probe.listing is not None and probe.listing.records == ()
+    assert probe.base_sha == base_sha and probe.head_sha == head_sha
+    assert probe.base_ref == "origin/main"
+    assert probe.foreign_op is None and payload["merge_head"] is None
+    plan = conflict_plan(hint="conflicting", probe=payload)
+    assert (plan.tier, plan.reason) == (0, "no_conflict")
+
+
+def test_p2_content_conflict_parses_stages_123(tmp_path):
+    repos = make_repos(tmp_path)
+    _content_conflict(repos)
+    payload = full(repos).payload
+    probe = parse_probe(payload)
+    assert probe.clean is False
+    entries = group_entries(probe.listing, probe.binary_paths)
+    assert [(e.path, e.stages) for e in entries] == [("f.txt", "123")]
+    plan = conflict_plan(hint="conflicting", probe=payload)
+    assert re.fullmatch(r"[0-9a-f]{40}", plan.merge_tree_oid)
+    assert (plan.tier, plan.reason) == (2, "text_conflict")
+    assert plan.text_paths == ("f.txt",)
+
+
+def test_p3_deleted_on_base_modified_on_pr_is_stages_12(tmp_path):
+    repos = make_repos(tmp_path, {"d.txt": "keep\n", "README.md": "r\n"})
+    repos.advance_base({"d.txt": None})
+    repos.pr_commit({"d.txt": "modified\n"})
+    payload = full(repos).payload
+    probe = parse_probe(payload)
+    entries = group_entries(probe.listing, probe.binary_paths)
+    assert [(e.path, e.stages) for e in entries] == [("d.txt", "12")]
+    plan = conflict_plan(hint="conflicting", probe=payload)
+    assert plan.paths[0].cls == "text:modify_delete"
+
+
+def test_p4_binary_changed_on_both_sides_is_binary(tmp_path):
+    repos = make_repos(tmp_path, {"blob.bin": b"\x00\x01base\x00\xff", "r.md": "r\n"})
+    repos.advance_base({"blob.bin": b"\x00\x02theirs\x00\xfe"})
+    repos.pr_commit({"blob.bin": b"\x00\x03ours\x00\xfd"})
+    payload = full(repos).payload
+    probe = parse_probe(payload)
+    assert "blob.bin" in probe.binary_paths
+    plan = conflict_plan(hint="conflicting", probe=payload)
+    assert (plan.tier, plan.reason) == (3, "halt:binary")
+
+
+@pytest.mark.parametrize("staged", [True, False], ids=["staged", "unstaged"])
+def test_p5_dirty_tracked_file_is_not_tree_clean(tmp_path, staged):
+    repos = make_repos(tmp_path)
+    (repos.work / "f.txt").write_text("dirty\n", encoding="utf-8")
+    if staged:
+        repos.git(repos.work, "add", "--", "f.txt")
+    payload = full(repos).payload
+    probe = parse_probe(payload)
+    assert payload["tree_clean"] is False and probe.tree_clean is False
+    assert "f.txt" in _decode(payload, "status_b64")
+    assert "f.txt" in probe.status_porcelain
+
+
+def test_p6_untracked_file_only_is_tree_clean(tmp_path):
+    repos = make_repos(tmp_path)
+    (repos.work / "untracked.txt").write_text("new\n", encoding="utf-8")
+    payload = full(repos).payload
+    assert payload["tree_clean"] is True
+    assert payload["status_b64"] == ""
+    assert parse_probe(payload).tree_clean is True
+
+
+def test_p7_half_finished_rebase_is_a_foreign_op(tmp_path):
+    repos = make_repos(tmp_path)
+    (repos.work / ".git" / "rebase-merge").mkdir()
+    payload = full(repos).payload
+    assert payload["foreign_op"] == "rebase-merge"
+    assert parse_probe(payload).foreign_op == "rebase-merge"
+    ops = run_probe(repos, "--repo", repos.repo_slug, "--ops-only").payload
+    assert ops == {
+        "ok": True,
+        "mode": "ops",
+        "foreign_op": "rebase-merge",
+        "merge_head": None,
+    }
+
+
+def _setup_clean(repos):
+    repos.advance_base({"other.txt": "b\n"})
+    repos.pr_commit({"pr.txt": "p\n"})
+
+
+def _setup_conflict(repos):
+    _content_conflict(repos)
+
+
+def _setup_dirty(repos):
+    _content_conflict(repos)
+    (repos.work / "README.md").write_text("unstaged\n", encoding="utf-8")
+    (repos.work / "f.txt").write_text("staged\n", encoding="utf-8")
+    repos.git(repos.work, "add", "--", "f.txt")
+    (repos.work / "untracked.txt").write_text("u\n", encoding="utf-8")
+
+
+def _setup_rebase_dir(repos):
+    _content_conflict(repos)
+    (repos.work / ".git" / "rebase-merge").mkdir()
+
+
+@pytest.mark.parametrize(
+    "setup",
+    [_setup_clean, _setup_conflict, _setup_dirty, _setup_rebase_dir],
+    ids=["clean", "conflict", "dirty", "rebase-dir"],
+)
+def test_p8_probe_leaves_status_head_and_index_unchanged(tmp_path, setup):
+    repos = make_repos(tmp_path)
+    setup(repos)
+    status_before = _status(repos)
+    head_before = repos.git(repos.work, "rev-parse", "HEAD")
+    branch_before = repos.git(repos.work, "branch", "--show-current")
+    index_before = (repos.work / ".git" / "index").read_bytes()
+    res = full(repos)
+    assert res.returncode == 0, res.stderr
+    assert _status(repos) == status_before
+    assert repos.git(repos.work, "rev-parse", "HEAD") == head_before
+    assert repos.git(repos.work, "branch", "--show-current") == branch_before
+    assert (repos.work / ".git" / "index").read_bytes() == index_before
+    assert not (repos.work / ".git" / "MERGE_HEAD").exists()
+
+
+def _remote_main(repos: Repos) -> str:
+    return repos.git(
+        repos.work, "rev-parse", "-q", "--verify", "refs/remotes/origin/main"
+    )
+
+
+@pytest.mark.parametrize(
+    "args, reason",
+    [
+        (("--base", "main"), "usage"),
+        (("--repo", "IronbellyOrg/IronClaude", "--base", "main"), "origin_mismatch"),
+        (("--repo", "IronbellyOrg/IronClaude", "--ops-only"), "origin_mismatch"),
+    ],
+    ids=["repo-missing", "repo-mismatch", "repo-mismatch-ops"],
+)
+def test_p9_usage_and_origin_mismatch_exit_2_without_fetch(tmp_path, args, reason):
+    repos = make_repos(tmp_path)
+    repos.advance_base({"other.txt": "b\n"})
+    remote_before = _remote_main(repos)
+    fetch_head = repos.work / ".git" / "FETCH_HEAD"
+    fetch_head_before = fetch_head.exists()
+    res = run_probe(repos, *args)
+    assert res.returncode == 2
+    assert res.stdout == f"PROBE_FAIL {reason}\n"
+    assert _remote_main(repos) == remote_before, "a fetch happened"
+    assert fetch_head.exists() == fetch_head_before, "a fetch happened"
+
+
+def test_p10_unreachable_origin_is_fetch_failed(tmp_path):
+    repos = make_repos(tmp_path)
+    shutil.rmtree(repos.origin)
+    res = full(repos)
+    assert res.returncode == 2
+    assert res.stdout == "PROBE_FAIL fetch_failed\n"
+    assert "cannot reach remote origin" in res.stderr
+
+
+def test_p11_merge_tree_unsupported_reports_null_clean(tmp_path):
+    repos = make_repos(tmp_path)
+    _content_conflict(repos)
+    wrap_dir = tmp_path / "gitwrap"
+    wrap_dir.mkdir()
+    wrapper = wrap_dir / "git"
+    wrapper.write_text(
+        "#!/usr/bin/env bash\n"
+        "mt=0; wt=0\n"
+        'for a in "$@"; do\n'
+        '  [ "$a" = merge-tree ] && mt=1\n'
+        '  [ "$a" = --write-tree ] && wt=1\n'
+        "done\n"
+        'if [ "$mt" = 1 ] && [ "$wt" = 1 ]; then\n'
+        "  echo 'error: unknown option write-tree' >&2; exit 129\n"
+        "fi\n"
+        f'exec "{GIT}" "$@"\n',
+        encoding="utf-8",
+    )
+    wrapper.chmod(0o755)
+    env = dict(repos.env)
+    env["PATH"] = f"{wrap_dir}{os.pathsep}{env['PATH']}"
+    payload = full(repos, env=env).payload
+    assert payload["merge_tree_supported"] is False
+    assert payload["clean"] is None
+    for key in ("merge_tree_b64", "numstat_ours_b64", "numstat_theirs_b64"):
+        assert payload[key] is None
+    probe = parse_probe(payload)
+    assert probe.merge_tree_supported is False and probe.clean is None
+    plan = conflict_plan(hint="conflicting", probe=payload)
+    assert (plan.tier, plan.reason) == (None, "merge_tree_unsupported")
+
+
+def test_p12_conflict_listing_above_limit_is_truncated_tier3(tmp_path):
+    names = [
+        f"dir/conflicting-file-with-a-rather-long-name-{i:04d}.txt" for i in range(400)
+    ]
+    repos = make_repos(tmp_path, {n: "base\n" for n in names})
+    repos.advance_base({n: "theirs\n" for n in names})
+    repos.pr_commit({n: "ours\n" for n in names})
+    payload = full(repos).payload
+    assert payload["truncated"] is True
+    for key in (
+        "status_b64",
+        "merge_tree_b64",
+        "numstat_ours_b64",
+        "numstat_theirs_b64",
+    ):
+        assert payload[key] is None
+    assert payload["clean"] is False
+    with pytest.raises(ValueError):
+        parse_probe(payload)
+    plan = conflict_plan(hint="conflicting", probe=payload)
+    assert (plan.tier, plan.reason) == (3, "probe_malformed")
+    # The untruncated listing really is above the limit (guards the setup).
+    listing = subprocess.run(
+        [GIT, "merge-tree", "--write-tree", "-z", "HEAD", "origin/main"],
+        cwd=repos.work,
+        env=repos.env,
+        capture_output=True,
+        timeout=60,
+    ).stdout
+    assert len(listing) > MAX_PROBE_BYTES
+
+
+# ---------------------------------------------------------------------------
+# Further contract rows of section 7.1
+# ---------------------------------------------------------------------------
+
+
+def test_ops_only_reports_a_real_merge_in_progress(tmp_path):
+    repos = make_repos(tmp_path)
+    _content_conflict(repos)
+    clean_ops = run_probe(repos, "--repo", repos.repo_slug, "--ops-only").payload
+    assert clean_ops == {
+        "ok": True,
+        "mode": "ops",
+        "foreign_op": None,
+        "merge_head": None,
+    }
+    repos.git(repos.work, "fetch", "-q", "origin", "main")
+    base_sha = repos.git(repos.work, "rev-parse", "origin/main").strip()
+    repos.git(repos.work, "merge", "--no-commit", "--no-ff", base_sha, check=False)
+    ops = run_probe(repos, "--repo", repos.repo_slug, "--ops-only").payload
+    assert ops["foreign_op"] == "MERGE_HEAD"
+    assert ops["merge_head"] == base_sha
+
+
+@pytest.mark.parametrize("base", ["a..b", "-main", "bad name"])
+def test_bad_base_exits_2(tmp_path, base):
+    repos = make_repos(tmp_path)
+    res = run_probe(repos, "--repo", repos.repo_slug, "--base", base)
+    assert res.returncode == 2
+    assert res.stdout == "PROBE_FAIL bad_base\n"
+
+
+def test_no_merge_base_exits_2(tmp_path):
+    repos = make_repos(tmp_path)
+    repos.git(repos.work, "checkout", "-q", "--orphan", "unrelated")
+    repos.git(repos.work, "rm", "-q", "-r", "--cached", ".")
+    for child in repos.work.iterdir():
+        if child.name != ".git":
+            child.unlink()
+    repos.commit(repos.work, {"solo.txt": "solo\n"}, "unrelated root")
+    res = full(repos)
+    assert res.returncode == 2
+    assert res.stdout == "PROBE_FAIL no_merge_base\n"
+
+
+def test_missing_base_branch_on_origin_is_fetch_failed(tmp_path):
+    repos = make_repos(tmp_path)
+    res = run_probe(repos, "--repo", repos.repo_slug, "--base", "no-such-branch")
+    assert res.returncode == 2
+    assert res.stdout == "PROBE_FAIL fetch_failed\n"
+
+
+def test_outside_a_work_tree_is_not_a_worktree(tmp_path):
+    repos = make_repos(tmp_path)
+    outside = tmp_path / "plain"
+    outside.mkdir()
+    env = dict(repos.env)
+    env["GIT_CEILING_DIRECTORIES"] = str(tmp_path)
+    res = subprocess.run(
+        [str(PROBE), "--repo", repos.repo_slug, "--base", "main"],
+        cwd=outside,
+        env=env,
+        text=True,
+        capture_output=True,
+        timeout=60,
+    )
+    assert res.returncode == 2
+    assert res.stdout == "PROBE_FAIL not_a_worktree\n"
+
+
+def test_programs_lists_only_programs_on_path(tmp_path):
+    repos = make_repos(tmp_path)
+    payload = full(
+        repos, "--program", "bash", "--program", "no-such-program-xyz-305"
+    ).payload
+    assert payload["programs"] == ["bash"]
+    assert parse_probe(payload).programs == frozenset({"bash"})
+
+
+@pytest.mark.parametrize(
+    "url",
+    [
+        "https://github.com/IronbellyOrg/IronClaude.git",
+        "git@github.com:IronbellyOrg/IronClaude.git",
+        "ssh://git@github.com/IronbellyOrg/IronClaude.git",
+        "https://github.com/IronbellyOrg/IronClaude",
+    ],
+)
+def test_origin_url_forms_resolve_to_owner_repo(tmp_path, url):
+    """The sed expression of the SKILL resolves every URL form; ops mode never fetches."""
+    repos = make_repos(tmp_path)
+    repos.git(repos.work, "remote", "set-url", "origin", url)
+    ops = run_probe(repos, "--repo", "IronbellyOrg/IronClaude", "--ops-only").payload
+    assert ops["ok"] is True and ops["mode"] == "ops"
+
+
+# ---------------------------------------------------------------------------
+# Static rules for the script (design section 7 preamble)
+# ---------------------------------------------------------------------------
+
+
+def test_probe_script_static_rules():
+    text = PROBE.read_text(encoding="utf-8")
+    assert text.startswith("#!/usr/bin/env bash\n")
+    assert "\nset -u -o pipefail\n" in text
+    assert os.access(PROBE, os.X_OK)
+    for pattern in (
+        r"\bgit\s+push\b",
+        r"\bstash\b",
+        r"\bgit\s+config\b",
+        r"--no-verify\b",
+        r"--amend\b",
+        r"--force\b",
+        r"src/superclaude",
+        r"\bgit\s+(checkout|switch|reset|commit|add|worktree|rebase)\b",
+        r"\bgit\s+merge(\s|$)",
+        r"\bgh\b",
+    ):
+        assert re.search(pattern, text) is None, pattern
+    ls = subprocess.run(
+        [GIT, "ls-files", "-s", "--", PROBE_REL],
+        cwd=REPO_ROOT,
+        text=True,
+        capture_output=True,
+        timeout=30,
+    ).stdout
+    if ls:  # the index entry exists once the path is staged
+        assert ls.startswith("100755 "), ls
diff --git a/.dev/tasks/to-do/TASK-WF-design-20261104-164423/artifacts/t10-tests.log b/.dev/tasks/to-do/TASK-WF-design-20261104-164423/artifacts/t10-tests.log
new file mode 100644
index 00000000..5bcaeb85
--- /dev/null
+++ b/.dev/tasks/to-do/TASK-WF-design-20261104-164423/artifacts/t10-tests.log
@@ -0,0 +1,14 @@
+============================= test session starts ==============================
+platform linux -- Python 3.11.15, pytest-9.2.0, pluggy-1.7.0
+SuperClaude: 5.0.0
+benchmark: 5.3.1 (defaults: timer=time.perf_counter disable_gc=False min_rounds=5 min_time=0.000005 max_time=1.0 calibration_precision=10 warmup=False warmup_iterations=100000)
+rootdir: /home/coder/workspaces/worktrees/IronClaude/issue-305-pr-submit-conflicts
+configfile: pyproject.toml
+plugins: superclaude-5.0.0, benchmark-5.3.1, anyio-4.16.0, cov-7.1.0
+collected 50 items
+
+tests/pr_submit/test_conflict_scripts.py ............................... [ 62%]
+                                                                         [ 62%]
+tests/pr_submit/test_static_grep.py ...................                  [100%]
+
+============================== 50 passed in 4.79s ==============================
diff --git a/.dev/tasks/to-do/TASK-WF-design-20261104-164423/artifacts/t10-grep.txt b/.dev/tasks/to-do/TASK-WF-design-20261104-164423/artifacts/t10-grep.txt
new file mode 100644
index 00000000..f53899f3
--- /dev/null
+++ b/.dev/tasks/to-do/TASK-WF-design-20261104-164423/artifacts/t10-grep.txt
@@ -0,0 +1,23 @@
+# grep -nE for forbidden items in src/superclaude/skills/sc-pr-submit-protocol/scripts/probe-merge.sh (expect no matches, exit 1)
+## pattern: \bgit[[:space:]]+push\b
+grep_exit=1
+## pattern: \bstash\b
+grep_exit=1
+## pattern: \bgit[[:space:]]+config\b
+grep_exit=1
+## pattern: --no-verify\b
+grep_exit=1
+## pattern: --amend\b
+grep_exit=1
+## pattern: --force\b
+grep_exit=1
+## pattern: src/superclaude
+grep_exit=1
+## pattern: \bgh\b
+grep_exit=1
+## pattern: SuperClaude-Org
+grep_exit=1
+## pattern: \bgit[[:space:]]+(checkout|switch|reset|commit|add|worktree|rebase)\b
+grep_exit=1
+## pattern: \bgit[[:space:]]+merge([[:space:]]|$)
+grep_exit=1
diff --git a/.dev/tasks/to-do/TASK-WF-design-20261104-164423/artifacts/t10-mode.txt b/.dev/tasks/to-do/TASK-WF-design-20261104-164423/artifacts/t10-mode.txt
new file mode 100644
index 00000000..46023c10
--- /dev/null
+++ b/.dev/tasks/to-do/TASK-WF-design-20261104-164423/artifacts/t10-mode.txt
@@ -0,0 +1,4 @@
+# git ls-files -s -- src/superclaude/skills/sc-pr-submit-protocol/scripts/probe-merge.sh
+100755 4db4a378d9cdb85316198a028881209132581a52 0	src/superclaude/skills/sc-pr-submit-protocol/scripts/probe-merge.sh
+# test -x src/superclaude/skills/sc-pr-submit-protocol/scripts/probe-merge.sh; echo $?
+0

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

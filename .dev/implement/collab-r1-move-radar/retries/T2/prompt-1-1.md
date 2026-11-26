4166c9ee4d33606af931ae9a0455b22bef4f9f85
Review one task for spec compliance.

Task brief: T2 (source: .dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/DESIGN.md; task grouping in .dev/implement/collab-r1-move-radar/tasks.md). Covers DESIGN.md section 1.2 rows `tools/sandbox.sh` and `tools/radar-index.sh`, the test T-2 of section 6.1 (with the shared test fixtures it needs: tests/conftest.py, tests/fixtures/cand/candidate.md), and the G-BASE sandbox conditions of section 6.3 (decided by spikes/gate0-check.sh, whose G-BASE and G-PINS parts are written here; its other spike parts are completed in later tasks). Built artifacts: /tmp/evalsb-collab-r1/<pkg>/repo for the three packages, index/<pkg>.json for the three packages.
T2.AC1: sandbox.sh and radar-index.sh implement the interfaces stated in DESIGN.md section 1.2.
T2.AC2: T-2 passes: `uv run pytest .dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tests/test_index.py -q`.
T2.AC3: the G-BASE sandbox conditions of DESIGN.md 6.3 hold (each sandbox lacks `.dev/reflect`; the package's own plan folder is absent; the repaired-code check of R-03 for every src/ file the package's squash commit changed), as recorded in spikes/gate0.json.
Global constraints: Orchestrator constraints: Create and edit files ONLY under .dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/ (plus .dev/implement/collab-r1-move-radar/ and scratch under /tmp/evalsb-collab-r1/ and /tmp/collab-r1/). Do not edit src/, tests/, .claude/, .dev/tasks/, the 20261111-a1 eval folder, or any other redesign's folder. Do not stage, commit or push. Use uv for all Python. Gateway model sessions only under flock /tmp/collab-gateway.lock; models muse-ember-1.0, gpt-6-luna, claude-haiku-5-5, claude-sonnet-5-5, grok-4.7; Opus only as blind judge; never Qwen or glm; NOFALLBACK=1. No full panel runs. Design hard limits: DESIGN.md section 0 'Hard limits carried into every script'.
Start sha: 4166c9ee4d33606af931ae9a0455b22bef4f9f85
Diff against the start snapshot: diff --git a/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tools/sandbox.sh b/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tools/sandbox.sh
new file mode 100755
index 000000000..9a6bb1404
--- /dev/null
+++ b/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tools/sandbox.sh
@@ -0,0 +1,29 @@
+#!/usr/bin/env bash
+# sandbox.sh <pkg> [--root <R1>] [--sb <SB>]   (H1, H3, H4; idempotent)
+# Builds SB/<pkg>/repo from the package's base commit (manifest.json) without the leak directories,
+# as its own throwaway git repo, and copies candidate.md and source.md to SB/cand/<pkg>/.
+# Exit 0 ok, 2 when SB/<pkg>/repo.ok names a different base sha, 1 on any other failure.
+set -u -o pipefail
+REPO=/home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel
+R1=$REPO/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar
+A1DIR=$REPO/.dev/eval-workspaces/tasklist-review-panel/20261111-a1
+SB=/tmp/evalsb-collab-r1
+PKG=${1:?usage: sandbox.sh <pkg> [--root R1] [--sb SB]}; shift
+while [ $# -gt 0 ]; do case $1 in --root) R1=$2; shift 2;; --sb) SB=$2; shift 2;; *) echo "bad arg $1" >&2; exit 1;; esac; done
+SHA=$(jq -r --arg p "$PKG" '.base_commits[$p].sha // empty' "$R1/manifest.json")
+[ -n "$SHA" ] || { echo "FAIL no base sha for $PKG in manifest.json" >&2; exit 1; }
+D=$SB/$PKG; C=$SB/cand/$PKG
+if [ -f "$D/repo.ok" ]; then
+  [ "$(cat "$D/repo.ok")" = "$SHA" ] || { echo "REFUSE $D/repo.ok names $(cat "$D/repo.ok"), manifest says $SHA" >&2; exit 2; }
+else
+  rm -rf "$D/repo"; mkdir -p "$D/repo"   # a partial build (no repo.ok) is rebuilt from scratch
+  git -C "$REPO" archive "$SHA" | tar -x -C "$D/repo" || { echo "FAIL archive $SHA" >&2; exit 1; }
+  rm -rf "$D/repo/.dev/tasks/done" "$D/repo/.dev/eval-workspaces" "$D/repo/.dev/research" "$D/repo/.dev/reflect"
+  [ -d "$D/repo/.dev" ] && find "$D/repo/.dev" -depth -type d -name "$PKG" -exec rm -rf {} +   # the package's own plan folder
+  ( cd "$D/repo" && git init -q && git add -A && git -c user.name=sandbox -c user.email=sandbox@localhost commit -qm snapshot ) || { echo "FAIL git snapshot" >&2; exit 1; }
+  echo "$SHA" > "$D/repo.ok"
+fi
+mkdir -p "$C"
+cmp -s "$A1DIR/$PKG/candidate.md" "$C/candidate.md" || cp "$A1DIR/$PKG/candidate.md" "$C/candidate.md"
+cmp -s "$REPO/.dev/tasks/done/$PKG/source.md" "$C/source.md" || cp "$REPO/.dev/tasks/done/$PKG/source.md" "$C/source.md"
+echo "OK $D/repo $SHA"
diff --git a/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tools/radar-index.sh b/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tools/radar-index.sh
new file mode 100755
index 000000000..bba19e292
--- /dev/null
+++ b/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tools/radar-index.sh
@@ -0,0 +1,62 @@
+#!/usr/bin/env bash
+# radar-index.sh <pkg> [--root <R1>] [--sb <SB>]  -> R1/index/<pkg>.json (classifier input; no ground truth)
+# {"paths","keys","task_of_path","tasks","criterion_greps","root_files"} from SB/cand/<pkg>/candidate.md and SB/<pkg>/repo.
+set -u -o pipefail
+REPO=/home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel
+R1=$REPO/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar
+SB=/tmp/evalsb-collab-r1
+PKG=${1:?usage: radar-index.sh <pkg> [--root R1] [--sb SB]}; shift
+while [ $# -gt 0 ]; do case $1 in --root) R1=$2; shift 2;; --sb) SB=$2; shift 2;; *) echo "bad arg $1" >&2; exit 1;; esac; done
+CAND=$SB/cand/$PKG/candidate.md; RR=$SB/$PKG/repo
+[ -f "$CAND" ] && [ -d "$RR" ] || { echo "FAIL missing $CAND or $RR (run sandbox.sh first)" >&2; exit 1; }
+mkdir -p "$R1/index"
+TMP=$(mktemp -d); trap 'rm -rf "$TMP"' EXIT
+
+# 1. (task, path-like token) pairs; a path belongs to the Task whose "## Task N:" section contains it
+awk '
+  /^## Task [0-9]+:/ { match($0, /[0-9]+/); task = "T" substr($0, RSTART, RLENGTH); print task > "/dev/stderr"; next }
+  /^## / { task = ""; next }
+  { s = $0
+    while (match(s, /[A-Za-z0-9_.\/][A-Za-z0-9_.\/-]*/)) {
+      t = substr(s, RSTART, RLENGTH); s = substr(s, RSTART + RLENGTH)
+      sub(/^\.\//, "", t); sub(/[.\/]+$/, "", t)
+      if (t ~ /\// || t ~ /\.[A-Za-z]{1,5}$/) print task "\t" t
+    } }' "$CAND" > "$TMP/pairs" 2> "$TMP/tasks"
+
+# 2. keep a token when it exists in the sandbox, its parent directory exists (a file a Task creates),
+#    or exactly one sandbox file ends with "/<token>"
+( cd "$RR" && find . -type f ! -path './.git/*' -printf '%P\n' ) > "$TMP/files"
+: > "$TMP/kept"
+cut -f2 "$TMP/pairs" | sort -u | while IFS= read -r t; do
+  case $t in /*|*..*) continue;; esac
+  if [ -f "$RR/$t" ]; then echo "$t	$t"   # files only: directory names make keys too generic
+  elif [[ $t == */*.* ]] && [ ! -e "$RR/$t" ] && [ -d "$RR/${t%/*}" ]; then echo "$t	$t"
+  else m=$(awk -v t="$t" 'substr($0, length($0) - length(t)) == "/" t' "$TMP/files")
+       [ -n "$m" ] && [ "$(printf '%s\n' "$m" | wc -l)" = 1 ] && echo "$t	$m"
+  fi
+done > "$TMP/kept"
+
+# 3. backticked grep criteria: first quoted argument, else first token after grep not starting with -
+awk '{ s = $0
+  while (match(s, /`grep [^`]*`/)) {
+    c = substr(s, RSTART + 1, RLENGTH - 2); s = substr(s, RSTART + RLENGTH)
+    if (match(c, /"[^"]*"/)) print substr(c, RSTART + 1, RLENGTH - 2)
+    else if (match(c, /\047[^\047]*\047/)) print substr(c, RSTART + 1, RLENGTH - 2)
+    else { n = split(c, w, /[ \t]+/); for (i = 2; i <= n; i++) if (w[i] !~ /^-/) { print w[i]; break } }
+  } }' "$CAND" > "$TMP/greps"
+
+( cd "$RR" && find . -maxdepth 1 -type f -printf '%P\n' ) | sort > "$TMP/root"
+
+jq -n --rawfile pairs "$TMP/pairs" --rawfile kept "$TMP/kept" --rawfile tasks "$TMP/tasks" \
+      --rawfile greps "$TMP/greps" --rawfile root "$TMP/root" '
+  def lines($s): $s | split("\n") | map(select(length > 0));
+  (lines($kept) | map(split("\t") | {(.[0]): .[1]}) | add // {}) as $map
+  | (lines($pairs) | map(split("\t") | select(.[0] != "" and ($map[.[1]] != null)) | {p: $map[.[1]], t: .[0]})) as $tp
+  | ($map | [.[]] | unique) as $paths
+  | {paths: $paths,
+     keys: ($paths | map(split("/") | last | sub("\\.[^.]*$"; "")) | map(select(length >= 4 and (test("^__.*__$") | not))) | unique),
+     task_of_path: ($tp | group_by(.p) | map({(.[0].p): (map(.t) | unique)}) | add // {}),
+     tasks: lines($tasks),
+     criterion_greps: (lines($greps) | unique),
+     root_files: lines($root)}' > "$R1/index/$PKG.json.tmp" && mv "$R1/index/$PKG.json.tmp" "$R1/index/$PKG.json"
+echo "OK $R1/index/$PKG.json"
diff --git a/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tests/conftest.py b/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tests/conftest.py
new file mode 100644
index 000000000..0c9a3db5d
--- /dev/null
+++ b/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tests/conftest.py
@@ -0,0 +1,59 @@
+"""Shared fixtures for the r1-move-radar tests. Every test writes only under tmp_path."""
+
+from __future__ import annotations
+
+import json
+import os
+import shutil
+import subprocess
+from pathlib import Path
+
+import pytest
+
+R1 = Path(__file__).resolve().parents[1]
+REPO = R1.parents[3]
+A1DIR = REPO / ".dev/eval-workspaces/tasklist-review-panel/20261111-a1"
+FIX = R1 / "tests" / "fixtures"
+TOOLS = R1 / "tools"
+PKG = "TASK-WF-fixture-20261113-000000"
+
+
+def run(args, *, stdin=None, env=None, cwd=None, timeout=60):
+    return subprocess.run(args, input=stdin, capture_output=True, text=True, env=env, cwd=cwd or REPO, timeout=timeout)
+
+
+@pytest.fixture
+def fake_sb(tmp_path):
+    """A sandbox root with one fixture package: SB/<PKG>/repo (root files, src, tests, docs) and SB/cand/<PKG>/."""
+    sb = tmp_path / "sb"
+    repo = sb / PKG / "repo"
+    for rel in ("src/app/core.py", "tests/app/test_core.py", "tests/app/test_other.py", "docs/guide.md", "CHANGELOG.md", "Makefile"):
+        p = repo / rel
+        p.parent.mkdir(parents=True, exist_ok=True)
+        p.write_text("x\n")
+    (repo / "src/app/sub").mkdir()
+    cand = sb / "cand" / PKG
+    cand.mkdir(parents=True)
+    shutil.copy(FIX / "cand" / "candidate.md", cand / "candidate.md")
+    (cand / "source.md").write_text("# source\n")
+    return sb
+
+
+@pytest.fixture
+def root(tmp_path):
+    """A writable R1 output root (index/, runs/, values/ ...) with the real config copied in."""
+    r = tmp_path / "r1"
+    (r / "config").mkdir(parents=True)
+    for f in (R1 / "config").iterdir():
+        shutil.copy(f, r / "config" / f.name)
+    shutil.copy(R1 / "manifest.json", r / "manifest.json")
+    return r
+
+
+def jload(p):
+    return json.loads(Path(p).read_text())
+
+
+@pytest.fixture
+def clean_env():
+    return {k: v for k, v in os.environ.items()}
diff --git a/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tests/test_index.py b/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tests/test_index.py
new file mode 100644
index 000000000..17d6a9222
--- /dev/null
+++ b/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tests/test_index.py
@@ -0,0 +1,20 @@
+"""T-2: radar-index.sh on the fixture candidate."""
+
+from conftest import PKG, TOOLS, jload, run
+
+
+def test_index_fixture(fake_sb, root):
+    r = run(["bash", str(TOOLS / "radar-index.sh"), PKG, "--root", str(root), "--sb", str(fake_sb)])
+    assert r.returncode == 0, r.stderr
+    ix = jload(root / "index" / f"{PKG}.json")
+    assert ix["tasks"] == ["T1", "T2", "T3"]
+    # a path inside Task 2's section maps to T2 only
+    assert ix["task_of_path"]["docs/guide.md"] == ["T2"]
+    # a path created by a Task (parent dir exists) is kept and mapped
+    assert ix["task_of_path"]["src/app/merge_guard.py"] == ["T1"]
+    assert ix["task_of_path"]["src/app/core.py"] == ["T1"]  # the Constraints mention belongs to no Task
+    assert sorted(ix["criterion_greps"]) == ["HOW-WE-WORK", "merge_guard"]
+    assert ix["root_files"] == ["CHANGELOG.md", "Makefile"]
+    assert "tests/app/test_core.py" in ix["paths"] and "tests/app/test_other.py" not in ix["paths"]
+    assert "merge_guard" in ix["keys"] and "core" in ix["keys"]
+    assert all(len(k) >= 4 for k in ix["keys"])  # stems shorter than 4 are dropped
diff --git a/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tests/fixtures/cand/candidate.md b/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tests/fixtures/cand/candidate.md
new file mode 100644
index 000000000..56972a064
--- /dev/null
+++ b/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tests/fixtures/cand/candidate.md
@@ -0,0 +1,27 @@
+---
+schema: workflow-plan/1.2
+---
+
+# Fixture plan
+
+## Constraints
+
+- Keep `src/app/core.py` importable.
+
+## Task 1: Add the guard module
+
+Create `src/app/merge_guard.py` and extend `src/app/core.py`.
+
+Acceptance criteria:
+- `grep -n "merge_guard" src/app/core.py` prints one line.
+
+## Task 2: Update the docs
+
+Edit `docs/guide.md` and `CHANGELOG.md`.
+
+Acceptance criteria:
+- `grep -rl HOW-WE-WORK tests` prints nothing.
+
+## Task 3: Tests
+
+Add `tests/app/test_merge_guard.py`; keep `tests/app/test_core.py` green.
diff --git a/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/spikes/gate0-check.sh b/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/spikes/gate0-check.sh
new file mode 100755
index 000000000..2dad98625
--- /dev/null
+++ b/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/spikes/gate0-check.sh
@@ -0,0 +1,68 @@
+#!/usr/bin/env bash
+# gate0-check.sh [--root <R1>] [--sb <SB>]: decides each Gate 0 pass condition (DESIGN.md 6.3) from the spike
+# records and writes spikes/gate0.json = {"G-BASE":..,"G-PINS":..,"S0":..,"S2":..,"REQ-S3":..,"S3":..,"Spike 4":..,
+# "reasons":{..},"checked_utc":..}. Values: pass | fail | recorded | missing.
+set -u -o pipefail
+REPO=/home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel
+R1=$REPO/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar
+SB=/tmp/evalsb-collab-r1
+while [ $# -gt 0 ]; do case $1 in --root) R1=$2; shift 2;; --sb) SB=$2; shift 2;; *) echo "bad arg $1" >&2; exit 1;; esac; done
+PKGS="TASK-WF-designSpec-20261107-075614 TASK-WF-makeTheAliasOnly-20261105-051649 TASK-WF-design-20261108-041415"
+declare -A SQUASH=([TASK-WF-designSpec-20261107-075614]=0b8a5801d [TASK-WF-makeTheAliasOnly-20261105-051649]=4eb75698d [TASK-WF-design-20261108-041415]=54e21668f)
+declare -A RES WHY
+M=$R1/manifest.json
+
+# G-BASE: 3 base shas; each sandbox lacks .dev/reflect and the package's plan folder; every src/ file the package's
+# squash commit changed is absent from the sandbox or differs from its squash-commit version (R-03 repaired-code check)
+RES[G-BASE]=pass; WHY[G-BASE]=""
+fail() { RES[$1]=fail; WHY[$1]="${WHY[$1]}$2; "; }
+n=$(jq '[.base_commits[]?|select(.sha|test("^[0-9a-f]{40}$"))]|length' "$M" 2>/dev/null || echo 0)
+[ "$n" = 3 ] || fail G-BASE "manifest has $n base shas"
+for P in $PKGS; do
+  RR=$SB/$P/repo
+  [ -f "$SB/$P/repo.ok" ] || { fail G-BASE "$P sandbox not built"; continue; }
+  [ -e "$RR/.dev/reflect" ] && fail G-BASE "$P sandbox has .dev/reflect"
+  [ -n "$(find "$RR/.dev" -type d -name "$P" 2>/dev/null | head -1)" ] && fail G-BASE "$P plan folder present"
+  while IFS= read -r f; do
+    [ -n "$f" ] || continue
+    if [ -f "$RR/$f" ] && git -C "$REPO" show "${SQUASH[$P]}:$f" 2>/dev/null | cmp -s - "$RR/$f"; then fail G-BASE "$P $f equals its repaired version"; fi
+  done < <(git -C "$REPO" diff-tree --no-commit-id --name-only -r --diff-filter=AM "${SQUASH[$P]}" -- src/)
+done
+
+# G-PINS: pins equal the live files; catalogue has 0 ground-truth hits
+RES[G-PINS]=pass; WHY[G-PINS]=""
+A1DIR=$REPO/.dev/eval-workspaces/tasklist-review-panel/20261111-a1
+[ "$(jq -r .catalogue_sha256 "$M")" = "$(sha256sum "$R1/config/catalogue.json" | cut -d' ' -f1)" ] || fail G-PINS "catalogue pin"
+[ "$(jq -r .brief_sha256 "$M")" = "$(sha256sum "$R1/config/brief.txt" | cut -d' ' -f1)" ] || fail G-PINS "brief pin"
+[ "$(jq -r .judge_one_sha256 "$M")" = "$(sha256sum "$A1DIR/tools/tmp-scripts/judge-one.sh" | cut -d' ' -f1)" ] || fail G-PINS "judge pin"
+jq -e '.pass == true and (.hits|length) == 0' "$R1/spikes/g-cat.json" >/dev/null 2>&1 || fail G-PINS "g-cat.json not clean"
+
+# Live spikes: their records decide (each record carries its own "pass" computed by the spike script)
+rec() { # rec <name> <file> <jq pass expr>
+  if [ ! -f "$2" ]; then RES[$1]=missing; WHY[$1]="no record $2"; return; fi
+  if jq -e "$3" "$2" >/dev/null 2>&1; then RES[$1]=pass; WHY[$1]=""; else RES[$1]=fail; WHY[$1]="condition false in $2"; fi
+}
+S0OK=pass; S0W=""
+for m in muse-ember-1.0 gpt-6-luna claude-sonnet-5-5 claude-haiku-5-5; do
+  rec S0 "$R1/spikes/s0/$m.json" '.pass == true'; [ "${RES[S0]}" = pass ] || { S0OK=${RES[S0]}; S0W="$S0W$m: ${WHY[S0]}; "; }
+done
+RES[S0]=$S0OK; WHY[S0]=$S0W
+S2OK=pass; S2W=""
+for m in muse-ember-1.0 gpt-6-luna claude-sonnet-5-5 claude-haiku-5-5; do
+  rec S2 "$R1/spikes/s2/$m.json" '.pass == true'; [ "${RES[S2]}" = pass ] || { S2OK=${RES[S2]}; S2W="$S2W$m: ${WHY[S2]}; "; }
+done
+RES[S2]=$S2OK; WHY[S2]=$S2W
+if [ -f "$R1/spikes/reqs3.json" ]; then RES[REQ-S3]=recorded; WHY[REQ-S3]=""; else RES[REQ-S3]=missing; WHY[REQ-S3]="no reqs3.json"; fi
+rec S3 "$R1/spikes/s3.json" '.pass == true'
+# Spike 4: one values file per panel and package with a matching .sha256 (the gate for a panel's collab-1 rows)
+S4=pass; S4W=""
+for panel in el2 sl2 hl2; do for P in $PKGS; do
+  V=$R1/values/$panel/$P.json
+  if [ ! -f "$V" ] || [ "$(sha256sum "$V" | cut -d' ' -f1)" != "$(cut -d' ' -f1 "$V.sha256" 2>/dev/null)" ]; then S4=missing; S4W="$S4W$panel/$P; "; fi
+done; done
+RES[Spike 4]=$S4; WHY[Spike 4]=$S4W
+
+{ for k in G-BASE G-PINS S0 S2 REQ-S3 S3 "Spike 4"; do printf '%s\t%s\t%s\n' "$k" "${RES[$k]}" "${WHY[$k]}"; done; } |
+  jq -R -s --arg t "$(date -u +%FT%TZ)" 'split("\n")|map(select(length>0)|split("\t"))
+    | (map({(.[0]):.[1]})|add) + {reasons:(map({(.[0]):.[2]})|add), checked_utc:$t}' > "$R1/spikes/gate0.json"
+jq -c 'del(.reasons)' "$R1/spikes/gate0.json"
diff --git a/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/spikes/gate0.json b/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/spikes/gate0.json
new file mode 100644
index 000000000..25625f490
--- /dev/null
+++ b/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/spikes/gate0.json
@@ -0,0 +1,19 @@
+{
+  "G-BASE": "pass",
+  "G-PINS": "pass",
+  "S0": "missing",
+  "S2": "missing",
+  "REQ-S3": "missing",
+  "S3": "missing",
+  "Spike 4": "missing",
+  "reasons": {
+    "G-BASE": "",
+    "G-PINS": "",
+    "S0": "muse-ember-1.0: no record /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/spikes/s0/muse-ember-1.0.json; gpt-6-luna: no record /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/spikes/s0/gpt-6-luna.json; claude-sonnet-5-5: no record /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/spikes/s0/claude-sonnet-5-5.json; claude-haiku-5-5: no record /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/spikes/s0/claude-haiku-5-5.json; ",
+    "S2": "muse-ember-1.0: no record /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/spikes/s2/muse-ember-1.0.json; gpt-6-luna: no record /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/spikes/s2/gpt-6-luna.json; claude-sonnet-5-5: no record /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/spikes/s2/claude-sonnet-5-5.json; claude-haiku-5-5: no record /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/spikes/s2/claude-haiku-5-5.json; ",
+    "REQ-S3": "no reqs3.json",
+    "S3": "no record /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/spikes/s3.json",
+    "Spike 4": "el2/TASK-WF-designSpec-20261107-075614; el2/TASK-WF-makeTheAliasOnly-20261105-051649; el2/TASK-WF-design-20261108-041415; sl2/TASK-WF-designSpec-20261107-075614; sl2/TASK-WF-makeTheAliasOnly-20261105-051649; sl2/TASK-WF-design-20261108-041415; hl2/TASK-WF-designSpec-20261107-075614; hl2/TASK-WF-makeTheAliasOnly-20261105-051649; hl2/TASK-WF-design-20261108-041415; "
+  },
+  "checked_utc": "2026-11-13T20:35:11Z"
+}
diff --git a/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/index/TASK-WF-design-20261108-041415.json b/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/index/TASK-WF-design-20261108-041415.json
new file mode 100644
index 000000000..8f781eda3
--- /dev/null
+++ b/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/index/TASK-WF-design-20261108-041415.json
@@ -0,0 +1,150 @@
+{
+  "paths": [
+    ".claude/settings.json",
+    "commands/issue.md",
+    "docs/designs/sc-issue-command.md",
+    "docs/user-guide/commands.md",
+    "docs/user-guide/flags.md",
+    "plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md",
+    "src/superclaude/agents/issue-worker-t3.md",
+    "src/superclaude/commands/issue.md",
+    "src/superclaude/core/CLAUDE.md",
+    "src/superclaude/core/HOW-WE-WORK.md",
+    "src/superclaude/skills/sc-issue-protocol/SKILL.md",
+    "src/superclaude/skills/sc-issue-protocol/refs/create.md",
+    "src/superclaude/skills/sc-issue-protocol/refs/labels.md",
+    "src/superclaude/skills/sc-issue-protocol/refs/tiers.md",
+    "src/superclaude/skills/sc-issue-protocol/templates/create-review-comment.md",
+    "src/superclaude/skills/sc-issue-protocol/templates/flags-decision.md",
+    "src/superclaude/skills/sc-issue-protocol/templates/scout-report.md",
+    "tests/skills/test_issue_protocol.py"
+  ],
+  "keys": [
+    "CLAUDE",
+    "HOW-WE-WORK",
+    "SKILL",
+    "commands",
+    "create",
+    "create-review-comment",
+    "flags",
+    "flags-decision",
+    "issue",
+    "issue-worker-t3",
+    "labels",
+    "sc-issue-command",
+    "scout-report",
+    "settings",
+    "test_issue_protocol",
+    "tiers"
+  ],
+  "task_of_path": {
+    ".claude/settings.json": [
+      "T12"
+    ],
+    "commands/issue.md": [
+      "T6"
+    ],
+    "docs/designs/sc-issue-command.md": [
+      "T10"
+    ],
+    "docs/user-guide/commands.md": [
+      "T9"
+    ],
+    "docs/user-guide/flags.md": [
+      "T9"
+    ],
+    "plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md": [
+      "T11"
+    ],
+    "src/superclaude/agents/issue-worker-t3.md": [
+      "T5",
+      "T8"
+    ],
+    "src/superclaude/commands/issue.md": [
+      "T6"
+    ],
+    "src/superclaude/core/CLAUDE.md": [
+      "T11"
+    ],
+    "src/superclaude/core/HOW-WE-WORK.md": [
+      "T11"
+    ],
+    "src/superclaude/skills/sc-issue-protocol/SKILL.md": [
+      "T3"
+    ],
+    "src/superclaude/skills/sc-issue-protocol/refs/create.md": [
+      "T2",
+      "T3",
+      "T8"
+    ],
+    "src/superclaude/skills/sc-issue-protocol/refs/labels.md": [
+      "T1",
+      "T10",
+      "T3",
+      "T4",
+      "T8"
+    ],
+    "src/superclaude/skills/sc-issue-protocol/templates/create-review-comment.md": [
+      "T4"
+    ],
+    "src/superclaude/skills/sc-issue-protocol/templates/flags-decision.md": [
+      "T4"
+    ],
+    "src/superclaude/skills/sc-issue-protocol/templates/scout-report.md": [
+      "T4",
+      "T8"
+    ],
+    "tests/skills/test_issue_protocol.py": [
+      "T1",
+      "T12",
+      "T4",
+      "T6",
+      "T7",
+      "T8"
+    ]
+  },
+  "tasks": [
+    "T1",
+    "T2",
+    "T3",
+    "T4",
+    "T5",
+    "T6",
+    "T7",
+    "T8",
+    "T9",
+    "T10",
+    "T11",
+    "T12"
+  ],
+  "criterion_greps": [
+    "HOW-WE-WORK"
+  ],
+  "root_files": [
+    ".env.example",
+    ".gitignore",
+    ".gitmodules",
+    ".markdownlint.json",
+    ".pre-commit-config.yaml",
+    ".secrets.baseline",
+    "AGENTS.md",
+    "CHANGELOG.md",
+    "CLAUDE.md",
+    "CONTRIBUTING.md",
+    "KNOWLEDGE.md",
+    "LICENSE",
+    "Makefile",
+    "NOTICE",
+    "POST-REFLECT-TASK.md",
+    "PROJECT_INDEX.json",
+    "PROJECT_INDEX.md",
+    "README.md",
+    "SECURITY.md",
+    "VERSION",
+    "package.json",
+    "pyproject.toml",
+    "return-contract.yaml",
+    "superclaude",
+    "update.sh"
+  ]
+}

Codegraph context
index_state=fresh checked_at=2026-11-13T20:27:49Z worktree_root=/home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel projectPath=/home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel
call codegraph only when index_state: fresh, never to widen scope
Q2b: the changed files are shell, jq, JSON and Python under .dev (eval harness, no product symbols have dependents outside the touched set); dependents checked on the Grep/Read floor: none outside the touched set.
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

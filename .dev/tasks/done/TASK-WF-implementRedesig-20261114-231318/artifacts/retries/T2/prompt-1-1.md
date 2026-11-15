9db3360b34e432fcefb77fd8ac7b52ea92b47ef1
Review one task for spec compliance.

Task brief: ## Task 2: Create the skeleton, the copy script, the environment script and the first fixtures

Depends on: Task 1

Follow `RL/IMPLEMENTATION.md` step 1 (create list) and `RL/DESIGN.md` sections 2.3, 3.1 to 3.4 and K8, K9. Create under `RL`:

- `RL/ruff.toml` with `extend = "../../../../pyproject.toml"`, and empty package files `RL/rl/__init__.py` and `RL/analysis/__init__.py` (`RL/scaffold/__init__.py` arrives by copy).
- `RL/config/shared-list.json` with the Tier A, S, T and B paths of `RL/DESIGN.md` 3.1, one list per tier (Tier A: `cards/` C1 to C8, schema, README; `briefs/` nine parts; `scaffold/{__init__,briefs,cards,fnd,lint,normalise}.py`; `bin/common.sh`; `bin/build-sandbox.sh`. Tier S: `config/packages.json`. Tier T: the eleven shared tests and the fixtures they need. Tier B: the twelve files of 3.1).
- `RL/bin/copy-shared.sh` with the behaviour of `RL/DESIGN.md` 3.2: reads the list, `sha256sum` then `cp` only (never writes under `SW`, K8), two reads 60 seconds apart for Tier B only, stops on a missing Tier A file or an unstable Tier B file, records an absent Tier B file as `built-local` naming its `SWD` section, writes `config/shared-manifest.json` (`tier`, `source`, `sha256`, `bytes`, `copied_at`, `kind`), and supports `--check` (re-hash every copy; a changed sibling file is `drift`, a warning with exit 0) and `--diff <path>`. Tier S is recorded once and not compared by `--check`.
- `RL/bin/rl-env.sh`: sets `SW_SB_ROOT=/tmp/evalsb-recipe`, accepts the one test hook `RL_FORCE_EXC` with values `lens`, `check` or `reask` only (anything else exits 2), exits 4 when the root is the sibling's `/tmp/evalsb-sweep` (K9). Every RL script sources it before `common.sh`.
- `RL/fixtures/sibling/make_sibling.py` (F-SIBLING of `RL/TESTING.md` section 2): builds a fake sibling folder in a temporary directory with Tier A, T and B files in chosen states (all present, a Tier A file missing, a Tier B file changing between two reads, a Tier B file absent) and a canary file whose mtime is checked.
- `RL/tests/fakes/claude`, executable, with only the `ok` scenario for now (reads the brief on stdin, finds `R-C<n>.` recipe headings, writes rows `C<n>.1` to `C<n>.<budget>`, appends one line per call to `FAKE_CALL_LOG`), so the copied `conftest.py` helper finds a fake first on `PATH`.

Acceptance criteria (ids added by the orchestrator, in source order):
T2.AC1: `bash RL/bin/copy-shared.sh --help` or a dry invocation against a fixture sibling from `make_sibling.py` runs without writing under the fixture's sibling folder (canary mtime unchanged).
T2.AC2: `RL/bin/rl-env.sh` sourced with `SW_SB_ROOT=/tmp/evalsb-sweep` exits 4 and with `RL_FORCE_EXC=bogus` exits 2.
T2.AC3: `RL/tests/fakes/claude` is executable and prints a JSON array in the shape of a real `claude -p --output-format json` run for the `ok` scenario.
T2.AC4: `RL/config/shared-list.json` is valid JSON and every path in it appears under `SW` or is listed as Tier B.

Global constraints: ## Constraints

Path names used by every task (all repo-relative to the checkout root `REPO`, which is `git rev-parse --show-toplevel`):

- `RL` is `.dev/eval-workspaces/tasklist-review-panel/20261114-recipe-ledger`. It holds `DESIGN.md`, `TESTING.md`, `IMPLEMENTATION.md` and `SHARED-MANIFEST-DESIGN-TIME.tsv`, which are the specification and are never edited by the build.
- `SW` is `.dev/eval-workspaces/tasklist-review-panel/20261114-sweep-sheet`, the sibling build (Redesign 1). It is read only: no task writes, edits, moves or deletes anything under it, and no task runs a script or a test from inside it.
- `MR` is `.dev/brainstorms/20261113-223124-panel-process-redesign/merged-requirements.md` (sections 3.0, 3.2, 5 and 6 are the requirements source; the design documents already map them). `EVAL` is `.dev/eval-workspaces/tasklist-review-panel/20261111-a1` (read only).
- Design ids: `K1` to `K9` (constraints), `DR-1` to `DR-16` (decisions) and `REQ-nn` (requirements) are those of `RL/DESIGN.md` sections 1.2 and 1.3 and of `RL/TESTING.md` section 3.

Scope rules that hold for every task:

- Create or edit files only under `RL`, plus scratch under `/tmp` (sandboxes under `/tmp/evalsb-recipe`, scratch under `/tmp/rl-*`). Nothing under `src/`, `tests/`, `.claude/`, any existing folder under `.dev/tasks/`, `SW`, `EVAL`, `.dev/eval-workspaces/tasklist-review-panel/20261113-collab` or any other folder is changed.
- No task runs `git commit` or `git push`, and no task runs `git add` for a path under `RL`. The freeze tag (K5) is only printed, never created.
- No task opens, reads, greps the content of or copies any `ground-truth*.json`, score file or judge output of a study package, and no recipe, card, brief, fixture, regex or example uses a study answer. Fixtures are invented. Tests that need ground truth use the synthetic `RL/fixtures/gt/` files only. The tests marked `freeze` (they read the real ground truth or need a second author's records) are never run by this build.
- Python runs only through uv. No `python -m`, no bare `pip`. No code folder is named `lib/` (K7).
- No reviewer or judge session is started and no network call is made. Tests use the fake `claude` at `RL/tests/fakes/claude`. If a task ever needed a model it would use `claude-sonnet-5-5` or `claude-haiku-5-5`; Opus is only the blind judge script's model; never Qwen or glm.
- Files under `RL/scaffold/`, `RL/cards/`, `RL/briefs/`, `RL/bin/common.sh`, `RL/bin/build-sandbox.sh` and the copied tests are copies of sibling files and are never edited after the copy (DESIGN 3.1). A copied test that fails is reported, not edited.
- Shell variables used in task commands:

```
REPO=$(git rev-parse --show-toplevel)
RL=$REPO/.dev/eval-workspaces/tasklist-review-panel/20261114-recipe-ledger
SW=$REPO/.dev/eval-workspaces/tasklist-review-panel/20261114-sweep-sheet
MR=$REPO/.dev/brainstorms/20261113-223124-panel-process-redesign/merged-requirements.md
T="uv run --frozen --project $REPO pytest -p no:cacheprovider"
PYRUN="uv run --frozen --project $REPO python"
export PYTHONDONTWRITEBYTECODE=1 NOFALLBACK=1 SUPERCLAUDE_CODEGRAPH_AUTOINIT=0
```


Start sha: 9db3360b34e432fcefb77fd8ac7b52ea92b47ef1
Diff against the start snapshot: diff --git a/.dev/eval-workspaces/tasklist-review-panel/20261114-recipe-ledger/analysis/__init__.py b/.dev/eval-workspaces/tasklist-review-panel/20261114-recipe-ledger/analysis/__init__.py
new file mode 100644
index 000000000..e69de29bb
diff --git a/.dev/eval-workspaces/tasklist-review-panel/20261114-recipe-ledger/bin/copy-shared.sh b/.dev/eval-workspaces/tasklist-review-panel/20261114-recipe-ledger/bin/copy-shared.sh
new file mode 100755
index 000000000..4a8d635f5
--- /dev/null
+++ b/.dev/eval-workspaces/tasklist-review-panel/20261114-recipe-ledger/bin/copy-shared.sh
@@ -0,0 +1,181 @@
+#!/usr/bin/env bash
+# Copy the shared Sweep Sheet pieces into RL and record their hashes (DESIGN 3.1, 3.2; K8).
+# The sibling folder is only a source: this script runs sha256sum, cp, diff and stat on it, nothing else.
+#
+#   copy-shared.sh                 copy per config/shared-list.json, write config/shared-manifest.json
+#   copy-shared.sh --check         re-hash every copy (edited copy: exit 1), report sibling drift (warning, exit 0)
+#   copy-shared.sh --diff <path>   unified diff of a local file against the sibling's file of the same name
+# Options: --sibling DIR (default: the sweep-sheet folder), --dest DIR (default: RL), --list FILE,
+#          --gap SECONDS (default 60: the pause between the two reads of the Tier B files).
+# Exit: 0 ok, 1 edited copy (--check), 2 usage, 3 refused (missing Tier A/S/T file, unstable Tier B file, bad copy).
+set -u -o pipefail
+
+HERE=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd -P)
+# shellcheck source=rl-env.sh
+source "$HERE/rl-env.sh"
+RL=$(cd "$HERE/.." && pwd -P)
+REPO=$(cd "$RL/../../../.." && pwd -P)
+SIB=$REPO/.dev/eval-workspaces/tasklist-review-panel/20261114-sweep-sheet
+DEST=$RL
+LIST=""
+GAP=60
+MODE=copy
+DIFFPATH=""
+
+usage() { sed -n '2,10p' "${BASH_SOURCE[0]}" | sed 's/^# \{0,1\}//'; }
+die() { echo "$1" >&2; exit "${2:-3}"; }
+
+while [ $# -gt 0 ]; do
+  case "$1" in
+    --help | -h) usage; exit 0 ;;
+    --check) MODE=check ;;
+    --diff) MODE=diff; shift; [ $# -ge 1 ] || die "--diff needs a path" 2; DIFFPATH=$1 ;;
+    --sibling) shift; [ $# -ge 1 ] || die "--sibling needs a folder" 2; SIB=$1 ;;
+    --dest) shift; [ $# -ge 1 ] || die "--dest needs a folder" 2; DEST=$1 ;;
+    --list) shift; [ $# -ge 1 ] || die "--list needs a file" 2; LIST=$1 ;;
+    --gap) shift; [ $# -ge 1 ] || die "--gap needs seconds" 2; GAP=$1 ;;
+    *) die "unknown option: $1" 2 ;;
+  esac
+  shift
+done
+[[ $GAP =~ ^[0-9]+$ ]] || die "--gap must be whole seconds" 2
+[ -n "$LIST" ] || LIST=$DEST/config/shared-list.json
+[ -f "$LIST" ] || die "no list: $LIST" 2
+MANIFEST=$DEST/config/shared-manifest.json
+
+# The copy never lands in the sibling (K8).
+rs=$(realpath -m -- "$SIB")
+rd=$(realpath -m -- "$DEST")
+case "$rd/" in "$rs"/*) die "E_DEST_IN_SIBLING: $DEST is inside $SIB" 2 ;; esac
+
+hash_of() { sha256sum -- "$1" | cut -d' ' -f1; }
+size_of() { stat -c %s -- "$1"; }
+tier_paths() { jq -r --arg t "$1" '.tiers[$t][] | if type == "object" then .path else . end' "$LIST"; }
+swd_of() { jq -r --arg p "$1" '.tiers.B[] | select(.path == $p) | .swd' "$LIST"; }
+prev_kind() { [ -f "$MANIFEST" ] && jq -r --arg p "$1" '.files[$p].kind // ""' "$MANIFEST" || echo ""; }
+prev_entry() { jq -c --arg p "$1" '.files[$p] | select(. != null) | . + {path: $p}' "$MANIFEST"; }
+
+if [ "$MODE" = diff ]; then
+  [ -e "$DEST/$DIFFPATH" ] || die "no local file: $DEST/$DIFFPATH" 2
+  [ -e "$SIB/$DIFFPATH" ] || { echo "the sibling has no file $DIFFPATH"; exit 0; }
+  diff -u --label "SW/$DIFFPATH" --label "RL/$DIFFPATH" -- "$SIB/$DIFFPATH" "$DEST/$DIFFPATH"
+  exit 0
+fi
+
+if [ "$MODE" = check ]; then
+  [ -f "$MANIFEST" ] || die "no manifest: $MANIFEST" 2
+  checked=0 drift=0 failed=0
+  while IFS=$'\t' read -r p tier kind sha; do
+    [ "$tier" != S ] || continue
+    checked=$((checked + 1))
+    if [ "$kind" = copied ]; then
+      if [ ! -f "$DEST/$p" ]; then
+        echo "FAIL $p: the copy is missing"; failed=$((failed + 1)); continue
+      elif [ "$(hash_of "$DEST/$p")" != "$sha" ]; then
+        echo "FAIL $p: the copy was edited (hash differs from the manifest)"; failed=$((failed + 1)); continue
+      fi
+      if [ ! -f "$SIB/$p" ]; then
+        echo "drift $p: the sibling no longer has this file"; drift=$((drift + 1))
+      elif [ "$(hash_of "$SIB/$p")" != "$sha" ]; then
+        echo "drift $p: the sibling's file changed since the copy"; drift=$((drift + 1))
+      fi
+    elif [ -f "$SIB/$p" ]; then
+      echo "drift $p: built-local, but the sibling now has a file of that name (run --diff $p)"
+      drift=$((drift + 1))
+    fi
+  done < <(jq -r '.files | to_entries[] | [.key, .value.tier, .value.kind, .value.sha256] | @tsv' "$MANIFEST")
+  echo "check: $checked checked, $drift drift (warning), $failed failed"
+  [ "$failed" -eq 0 ]
+  exit $?
+fi
+
+# ---- copy mode ----
+TMP=$(mktemp -d /tmp/rl-copyshared.XXXXXXXX) || die "mktemp failed"
+trap 'rm -rf -- "$TMP"' EXIT
+ENT=$TMP/entries.jsonl
+: >"$ENT"
+
+emit() { # path tier sha bytes copied_at kind swd
+  jq -nc --arg path "$1" --arg tier "$2" --arg sha "$3" --argjson bytes "$4" --arg at "$5" --arg kind "$6" --arg swd "$7" \
+    '{path: $path, tier: $tier, source: ("SW/" + $path), sha256: $sha, bytes: $bytes,
+      copied_at: (if $at == "" then null else $at end), kind: $kind} + (if $swd == "" then {} else {swd: $swd} end)' >>"$ENT"
+}
+now() { date -u +%Y-%m-%dT%H:%M:%SZ; }
+
+# Step 1: every Tier A, S and T file must exist before anything is copied.
+mapfile -t A < <(tier_paths A)
+mapfile -t S < <(tier_paths S)
+mapfile -t T < <(tier_paths T)
+mapfile -t B < <(tier_paths B)
+missing=0
+for p in "${A[@]}" "${T[@]}"; do
+  [ -f "$SIB/$p" ] || { echo "E_MISSING: $p is missing in the sibling" >&2; missing=1; }
+done
+for p in "${S[@]}"; do
+  [ -f "$DEST/$p" ] && [ -n "$(prev_kind "$p")" ] && continue
+  [ -f "$SIB/$p" ] || { echo "E_MISSING: $p is missing in the sibling" >&2; missing=1; }
+done
+[ "$missing" -eq 0 ] || die "stopped: a Tier A, S or T file is missing; nothing was copied and nothing may be rebuilt by hand" 3
+
+# Step 2: Tier B files that exist are read twice, GAP seconds apart. A file that built-local protects is not read.
+declare -A H1 PROT
+anyb=0
+for p in "${B[@]}"; do
+  if [ "$(prev_kind "$p")" = built-local ] && [ -f "$DEST/$p" ]; then
+    PROT[$p]=1
+  elif [ -f "$SIB/$p" ]; then
+    H1[$p]=$(hash_of "$SIB/$p"); anyb=1
+  fi
+done
+[ "$anyb" -eq 0 ] || sleep "$GAP"
+for p in "${!H1[@]}"; do
+  if [ ! -f "$SIB/$p" ] || [ "$(hash_of "$SIB/$p")" != "${H1[$p]}" ]; then
+    die "E_UNSTABLE: $p changed between two reads $GAP s apart; the sibling is still writing it; nothing was copied" 3
+  fi
+done
+
+# Step 3: copy, then hash the copy and compare.
+copy_one() { # rel expected_hash
+  local rel=$1 want=$2 got
+  mkdir -p -- "$(dirname -- "$DEST/$rel")"
+  cp -- "$SIB/$rel" "$DEST/$rel" || die "E_COPY: cp failed for $rel" 3
+  got=$(hash_of "$DEST/$rel")
+  [ "$got" = "$want" ] || die "E_COPY: $rel changed while it was copied (source $want, copy $got)" 3
+}
+for p in "${A[@]}" "${T[@]}"; do
+  t=A
+  [[ $p == tests/* || $p == fixtures/* ]] && t=T
+  h=$(hash_of "$SIB/$p")
+  copy_one "$p" "$h"
+  emit "$p" "$t" "$h" "$(size_of "$DEST/$p")" "$(now)" copied ""
+done
+for p in "${S[@]}"; do
+  if [ -f "$DEST/$p" ] && [ -n "$(prev_kind "$p")" ]; then
+    prev_entry "$p" >>"$ENT"
+    continue
+  fi
+  h=$(hash_of "$SIB/$p")
+  copy_one "$p" "$h"
+  emit "$p" S "$h" "$(size_of "$DEST/$p")" "$(now)" copied ""
+done
+for p in "${B[@]}"; do
+  if [ -n "${H1[$p]:-}" ]; then
+    copy_one "$p" "${H1[$p]}"
+    emit "$p" B "${H1[$p]}" "$(size_of "$DEST/$p")" "$(now)" copied ""
+    continue
+  fi
+  if [ -f "$DEST/$p" ]; then
+    emit "$p" B "$(hash_of "$DEST/$p")" "$(size_of "$DEST/$p")" "" built-local "$(swd_of "$p")"
+  else
+    emit "$p" B ABSENT null "" built-local "$(swd_of "$p")"
+  fi
+  [ -z "${PROT[$p]:-}" ] || [ ! -f "$SIB/$p" ] || echo "note: $p is built-local and the sibling now has it; run --diff $p"
+done
+
+# Step 4: the manifest.
+mkdir -p -- "$DEST/config"
+jq -S -s '{schema: "rl-shared-manifest/1",
+           note: "sha256 ABSENT marks a built-local file that has not been written yet; bin/copy-shared.sh records its hash when it exists",
+           files: (map({(.path): del(.path)}) | add)}' "$ENT" >"$TMP/manifest.json" || die "manifest write failed" 3
+cp -- "$TMP/manifest.json" "$MANIFEST"
+echo "copied: $(jq '[.files[] | select(.kind == "copied")] | length' "$MANIFEST") files, built-local: $(jq '[.files[] | select(.kind == "built-local")] | length' "$MANIFEST"); manifest $MANIFEST"
diff --git a/.dev/eval-workspaces/tasklist-review-panel/20261114-recipe-ledger/bin/rl-env.sh b/.dev/eval-workspaces/tasklist-review-panel/20261114-recipe-ledger/bin/rl-env.sh
new file mode 100755
index 000000000..755064f16
--- /dev/null
+++ b/.dev/eval-workspaces/tasklist-review-panel/20261114-recipe-ledger/bin/rl-env.sh
@@ -0,0 +1,23 @@
+#!/usr/bin/env bash
+# Sourced by every RL script before bin/common.sh (DESIGN 1.2 K9, TESTING 1.3).
+# Own sandbox root: the sibling's root is refused with exit 4. Test hook: RL_FORCE_EXC.
+SW_SB_ROOT=${SW_SB_ROOT:-/tmp/evalsb-recipe}
+export SW_SB_ROOT
+
+_rl_root=$(realpath -m -- "$SW_SB_ROOT")
+case "$_rl_root/" in
+  /tmp/evalsb-sweep/*)
+    echo "E_SIBLING_ROOT: SW_SB_ROOT=$SW_SB_ROOT is the Sweep Sheet sandbox root" >&2
+    exit 4
+    ;;
+esac
+unset _rl_root
+
+# The one test hook: raise in one component. Anything else is refused.
+case "${RL_FORCE_EXC:-}" in
+  "" | lens | check | reask) ;;
+  *)
+    echo "E_HOOK: RL_FORCE_EXC=${RL_FORCE_EXC} is not one of lens, check, reask" >&2
+    exit 2
+    ;;
+esac
diff --git a/.dev/eval-workspaces/tasklist-review-panel/20261114-recipe-ledger/config/shared-list.json b/.dev/eval-workspaces/tasklist-review-panel/20261114-recipe-ledger/config/shared-list.json
new file mode 100644
index 000000000..c493b44be
--- /dev/null
+++ b/.dev/eval-workspaces/tasklist-review-panel/20261114-recipe-ledger/config/shared-list.json
@@ -0,0 +1,74 @@
+{
+  "schema": "rl-shared-list/1",
+  "note": "DESIGN 3.1. Paths are relative to the sweep-sheet folder (source) and to RL (copy). Tier B entries name the SWD section a local build follows (DESIGN 3.3).",
+  "tiers": {
+    "A": [
+      "cards/C1.json",
+      "cards/C2.json",
+      "cards/C3.json",
+      "cards/C4.json",
+      "cards/C5.json",
+      "cards/C6.json",
+      "cards/C7.json",
+      "cards/C8.json",
+      "cards/schema.json",
+      "cards/README.md",
+      "briefs/base.txt",
+      "briefs/cb1.txt",
+      "briefs/cb2.txt",
+      "briefs/cb3.txt",
+      "briefs/cb4.txt",
+      "briefs/cb5.txt",
+      "briefs/ledger-rule.txt",
+      "briefs/k-lead.txt",
+      "briefs/sheet-block.txt",
+      "scaffold/__init__.py",
+      "scaffold/briefs.py",
+      "scaffold/cards.py",
+      "scaffold/fnd.py",
+      "scaffold/lint.py",
+      "scaffold/normalise.py",
+      "bin/common.sh",
+      "bin/build-sandbox.sh"
+    ],
+    "S": [
+      "config/packages.json"
+    ],
+    "T": [
+      "tests/conftest.py",
+      "tests/helpers.py",
+      "tests/test_briefs.py",
+      "tests/test_cards.py",
+      "tests/test_fnd_contract.py",
+      "tests/test_lint.py",
+      "tests/test_model_allowlist.py",
+      "tests/test_normalise.py",
+      "tests/test_paths.py",
+      "tests/test_readme.py",
+      "tests/test_sandbox.py",
+      "fixtures/repos/build_repo.py",
+      "fixtures/reports/anchor_250.md",
+      "fixtures/reports/claim_301.md",
+      "fixtures/plans/p_basic.md",
+      "fixtures/plans/p_clean.md",
+      "fixtures/plans/source.md",
+      "fixtures/specs/spec1.md",
+      "fixtures/specs/parent1.md",
+      "fixtures/docs/doc1.md"
+    ],
+    "B": [
+      {"path": "scaffold/ledgerv1.py", "swd": "SWD 9.1 to 9.3 (ledger reader, checks, linking, demotion, promotion)"},
+      {"path": "scaffold/telemetry.py", "swd": "SWD 9.2 and DD-12 (class, probe and src keys; MR 3.0.6)"},
+      {"path": "scaffold/clock.py", "swd": "SWD 11.4 (panel clock and the kill_s, hang_s, breakeven helpers)"},
+      {"path": "bin/run-reviewer.sh", "swd": "SWD 11.1 (one attempt, hang guard, model-identity check)"},
+      {"path": "bin/run-panel.sh", "swd": "SWD 11.4 to 11.7 (clock, hang guard, concurrency, merge)"},
+      {"path": "bin/judge-one.sh", "swd": "SWD 11.3 (blind judge, claude-opus-5-5 only)"},
+      {"path": "bin/anon.sh", "swd": "SWD 11.3 (anonymisation)"},
+      {"path": "bin/judge-batch.sh", "swd": "SWD 11.3 (judge batch)"},
+      {"path": "analysis/analyze.py", "swd": "SWD 14.3 (analysis outputs)"},
+      {"path": "analysis/g0.py", "swd": "SWD 14.1 (ledger-and-time half of gate G0 only)"},
+      {"path": "bin/make-schedule.py", "swd": "SWD 11.6 (block-randomised schedule)"},
+      {"path": "bin/run-schedule.sh", "swd": "SWD 11.6 (schedule runner)"}
+    ]
+  }
+}
diff --git a/.dev/eval-workspaces/tasklist-review-panel/20261114-recipe-ledger/fixtures/sibling/make_sibling.py b/.dev/eval-workspaces/tasklist-review-panel/20261114-recipe-ledger/fixtures/sibling/make_sibling.py
new file mode 100644
index 000000000..3350b79fe
--- /dev/null
+++ b/.dev/eval-workspaces/tasklist-review-panel/20261114-recipe-ledger/fixtures/sibling/make_sibling.py
@@ -0,0 +1,93 @@
+"""F-SIBLING: a fake sibling folder with Tier A, S, T and B files in chosen states (TESTING 2; DR-11, K8).
+
+The file contents are invented one-line stubs. A canary file with a fixed old mtime lets a test prove that
+nothing wrote into the folder: `snapshot()` lists every path with its size and mtime, directories included.
+"""
+
+import json
+import os
+import threading
+from pathlib import Path
+
+RL = Path(__file__).resolve().parents[2]
+CANARY = "CANARY.txt"
+OLD_MTIME = 1_000_000_000  # 2001-09-09, far from any real write
+
+
+def load_list(list_path=None):
+    return json.loads((list_path or RL / "config" / "shared-list.json").read_text())[
+        "tiers"
+    ]
+
+
+def _write(root, rel, text):
+    p = Path(root) / rel
+    p.parent.mkdir(parents=True, exist_ok=True)
+    p.write_text(text)
+    return p
+
+
+def build(root, tier_b="absent", missing_tier_a=None, tiers=None):
+    """Build the folder `root`.
+
+    tier_b: "absent" (no Tier B file), "present" (all of them) or a list of the Tier B paths that exist.
+    missing_tier_a: one Tier A path to leave out.
+    Returns the snapshot taken after the build (so a later `snapshot(root) == result` proves a read-only use).
+    """
+    tiers = tiers or load_list()
+    root = Path(root)
+    root.mkdir(parents=True, exist_ok=True)
+    for tier in ("A", "S", "T"):
+        for rel in tiers[tier]:
+            if rel != missing_tier_a:
+                _write(root, rel, f"fixture stub of {rel}\n")
+    b_paths = [b["path"] for b in tiers["B"]]
+    present = (
+        b_paths if tier_b == "present" else ([] if tier_b == "absent" else list(tier_b))
+    )
+    for rel in present:
+        _write(root, rel, f"fixture stub of {rel}, version 1\n")
+    canary = _write(root, CANARY, "canary\n")
+    os.utime(canary, (OLD_MTIME, OLD_MTIME))
+    return snapshot(root)
+
+
+def snapshot(root):
+    """Every path under root (files and folders) mapped to (size, mtime_ns); atime is not read."""
+    out = {}
+    for p in sorted(Path(root).rglob("*")):
+        st = p.stat()
+        out[str(p.relative_to(root))] = (
+            0 if p.is_dir() else st.st_size,
+            st.st_mtime_ns,
+        )
+    return out
+
+
+def canary_unchanged(root):
+    st = (Path(root) / CANARY).stat()
+    return (
+        st.st_mtime_ns == OLD_MTIME * 1_000_000_000
+        and (Path(root) / CANARY).read_text() == "canary\n"
+    )
+
+
+def change_later(root, rel, after_s):
+    """Rewrite `rel` after `after_s` seconds, on a timer thread (a Tier B file that changes between two reads)."""
+    t = threading.Timer(
+        after_s, lambda: _write(root, rel, f"fixture stub of {rel}, version 2\n")
+    )
+    t.start()
+    return t
+
+
+if __name__ == "__main__":
+    import argparse
+
+    ap = argparse.ArgumentParser(description=__doc__)
+    ap.add_argument("root")
+    ap.add_argument("--tier-b", default="absent", choices=("absent", "present"))
+    ap.add_argument("--missing-tier-a")
+    a = ap.parse_args()
+    build(a.root, a.tier_b, a.missing_tier_a)
+    print(f"built {a.root}")
diff --git a/.dev/eval-workspaces/tasklist-review-panel/20261114-recipe-ledger/rl/__init__.py b/.dev/eval-workspaces/tasklist-review-panel/20261114-recipe-ledger/rl/__init__.py
new file mode 100644
index 000000000..e69de29bb
diff --git a/.dev/eval-workspaces/tasklist-review-panel/20261114-recipe-ledger/ruff.toml b/.dev/eval-workspaces/tasklist-review-panel/20261114-recipe-ledger/ruff.toml
new file mode 100644
index 000000000..724b52f3d
--- /dev/null
+++ b/.dev/eval-workspaces/tasklist-review-panel/20261114-recipe-ledger/ruff.toml
@@ -0,0 +1 @@
+extend = "../../../../pyproject.toml"
diff --git a/.dev/eval-workspaces/tasklist-review-panel/20261114-recipe-ledger/tests/fakes/claude b/.dev/eval-workspaces/tasklist-review-panel/20261114-recipe-ledger/tests/fakes/claude
new file mode 100755
index 000000000..d06c2c3a7
--- /dev/null
+++ b/.dev/eval-workspaces/tasklist-review-panel/20261114-recipe-ledger/tests/fakes/claude
@@ -0,0 +1,60 @@
+#!/usr/bin/env bash
+# Stand-in for `claude -p --output-format json` (TESTING F-FAKE-RL). No model is started.
+# Reads the brief on stdin, picks a scenario from FAKE_SCENARIO (default ok), prints the JSON array of a
+# real run (system init, one assistant message, result) and appends one line per call to FAKE_CALL_LOG:
+#   <epoch seconds> TAB <scenario> TAB <requested model> TAB <kind: review or repair>
+# Scenario now: ok. The others of DESIGN 3.4 are added in task 11.
+# Ledger rows: for every recipe heading `R-C<n>.` of the brief, rows C<n>.1 to C<n>.<budget>, all OK; the budget
+# is the N of the recipe's sentence `Write at most N rows.` (4 when the recipe has none). No recipe, no ledger.
+set -u
+SCEN=${FAKE_SCENARIO:-ok}
+MODEL=claude-sonnet-5-5
+while [ $# -gt 0 ]; do
+  [ "$1" = "--model" ] && [ $# -ge 2 ] && MODEL=$2
+  shift
+done
+BRIEF=$(cat)
+
+case "$SCEN" in
+  ok) ;;
+  *) echo "fake claude: unknown FAKE_SCENARIO=$SCEN" >&2; exit 2 ;;
+esac
+
+KIND=review
+case "$BRIEF" in "Your final message was kept as your review"*) KIND=repair ;; esac
+[ -z "${FAKE_CALL_LOG:-}" ] || printf '%s\t%s\t%s\t%s\n' "$(date +%s.%3N)" "$SCEN" "$MODEL" "$KIND" >>"$FAKE_CALL_LOG"
+
+# One "<class> <budget>" line per recipe, in brief order: the text between a heading and the next heading or blank line.
+RECIPES=$(printf '%s\n' "$BRIEF" | awk '
+  function flush() { if (cls != "") print cls, (n == "" ? 4 : n); cls = ""; n = "" }
+  /^R-C[0-9]+\. / { flush(); cls = $1; sub(/^R-/, "", cls); sub(/\.$/, "", cls) }
+  cls != "" && match($0, /Write at most [0-9]+ rows\./) {
+    s = substr($0, RSTART, RLENGTH); gsub(/[^0-9]/, "", s); n = s
+  }
+  /^$/ { flush() }
+  END { flush() }')
+
+LEDGER=""
+while read -r cls budget; do
+  [ -n "${cls:-}" ] || continue
+  for k in $(seq 1 "$budget"); do
+    LEDGER+=$(jq -nc --arg i "$cls.$k" '{item:$i,verdict:"OK",quote_plan:"",quote_other:"",problem:"",ran:"compared both scopes"}')$'\n'
+  done
+done <<<"$RECIPES"
+
+FINDING=$(jq -nc '{id:"F1",severity:"MINOR",blocking:false,category:"other",anchor:"the stated text of the first acceptance criterion",refs:[],claim:"The wording leaves one reading open."}')
+
+BT='```'
+REPORT="review: 1 of 3"$'\n\n'"Covered: the candidate and the source."$'\n\n'
+if [ -n "$LEDGER" ]; then
+  REPORT+="## Ledger"$'\n\n'"${BT}ledger-v1"$'\n'"${LEDGER}${BT}"$'\n\n'
+fi
+REPORT+="## Findings block"$'\n\n'"${BT}findings-v1"$'\n'"${FINDING}"$'\n'"${BT}"$'\n\n'"verdict: PASS"
+
+jq -nc --arg m "$MODEL" --arg r "$REPORT" '
+  ($r | length / 4 | floor) as $n
+  | [ {type:"system", subtype:"init", session_id:"fake-session", model:$m},
+      {type:"assistant", parent_tool_use_id:null, session_id:"fake-session",
+       message:{model:$m, content:[{type:"text", text:$r}]}},
+      {type:"result", subtype:"success", is_error:false, result:$r, session_id:"fake-session",
+       usage:{output_tokens:$n}, modelUsage:{($m):{outputTokens:$n}}} ]'

Codegraph context: index_state: fresh; checked_at: 2026-11-14T23:20:38Z; worktree_root: /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel; projectPath: /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel
call codegraph only when index_state: fresh, never to widen scope
Q2b: this task changes no existing symbol; the files it creates are new, so there are no dependents outside the diff.

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

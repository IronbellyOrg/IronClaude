4f42d343ee78d3226a398d0469bc99c24f0e39e8
Review one task for spec compliance.

Task brief: T1 (source: .dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/DESIGN.md; task grouping in .dev/implement/collab-r1-move-radar/tasks.md). Covers DESIGN.md section 1.1 (config/panels.json, config/catalogue.json, config/catalogue.sha256, config/brief.txt, manifest.json) and section 1.3 spikes/g-base.sh and spikes/g-pins.sh (with its helper subcommand `catcheck` in tools/collab_summary.py, which section 1.3 needs for "catalogue ground-truth check (R-07)").
T1.AC1: every file of the DESIGN.md section 1.1 table exists with the content that table states (values/<panel>/<pkg>.json is written only by Spike 4, which is out of scope here).
T1.AC2: manifest.json has 3 base SHAs written by g-base.sh (G-BASE manifest part; method recorded) and the G-PINS pass condition of DESIGN.md 6.3 holds (pins written, catalogue 0 ground-truth hits, spikes/g-cat.json).
Source of the move texts: .dev/brainstorms/20261113-163248-panel-collaboration/merged-requirements.md lines 184-193. Brief source: .dev/eval-workspaces/tasklist-review-panel/20261111-a1/tools/run-reviewer.sh lines 13-17.
Global constraints: Orchestrator constraints: Create and edit files ONLY under .dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/ (plus .dev/implement/collab-r1-move-radar/ and scratch under /tmp/evalsb-collab-r1/ and /tmp/collab-r1/). Do not edit src/, tests/, .claude/, .dev/tasks/, the 20261111-a1 eval folder, or any other redesign's folder. Do not stage, commit or push. Use uv for all Python. Gateway model sessions only under flock /tmp/collab-gateway.lock; models muse-ember-1.0, gpt-6-luna, claude-haiku-5-5, claude-sonnet-5-5, grok-4.7; Opus only as blind judge; never Qwen or glm; NOFALLBACK=1. No full panel runs. Design hard limits: DESIGN.md section 0 'Hard limits carried into every script'.
Start sha: 4f42d343ee78d3226a398d0469bc99c24f0e39e8
Diff against the start snapshot: diff --git a/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/config/panels.json b/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/config/panels.json
new file mode 100644
index 000000000..0b7a6d7d2
--- /dev/null
+++ b/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/config/panels.json
@@ -0,0 +1,23 @@
+{
+ "el2": {"critical_role": "reader", "planning_B": 116, "planning_T_report": 6.4, "planning_reader_end": 102, "G_s": 47,
+   "roles": {
+     "searcher": {"rid": "t2b-1", "model": "muse-ember-1.0", "checkpoints": [6, 10], "planning_turn": 3.2},
+     "reader": {"rids": ["t4-1", "t3-1"], "model": "gpt-6-luna", "checkpoints": [8, 12], "planning_turn": 6.4}},
+   "resolution": {"t2b-1": {"tier": "tier2b", "alias": "claude-gw-tier2b[1m]"},
+                  "t4-1": {"tier": "tier4", "alias": "claude-gw-tier4[1m]"},
+                  "t3-1": {"tier": "tier3", "alias": "claude-gw-tier3[1m]"}}},
+ "sl2": {"critical_role": "searcher", "planning_B": 273.7, "planning_T_report": 14, "planning_reader_end": 102, "G_s": null,
+   "roles": {
+     "searcher": {"rid": "t1b-1", "model": "claude-sonnet-5-5", "checkpoints": [6, 10], "planning_turn": 14},
+     "reader": {"rids": ["t4-1", "t3-1"], "model": "gpt-6-luna", "checkpoints": [8, 12], "planning_turn": 6.4}},
+   "resolution": {"t1b-1": {"tier": "tier1b", "alias": "claude-gw-tier1b[1m]"},
+                  "t4-1": {"tier": "tier4", "alias": "claude-gw-tier4[1m]"},
+                  "t3-1": {"tier": "tier3", "alias": "claude-gw-tier3[1m]"}}},
+ "hl2": {"critical_role": "searcher", "planning_B": 238, "planning_T_report": 23, "planning_reader_end": 102, "G_s": null,
+   "roles": {
+     "searcher": {"rid": "t2-1", "model": "claude-haiku-5-5", "checkpoints": [6, 10], "planning_turn": 23},
+     "reader": {"rids": ["t4-1", "t3-1"], "model": "gpt-6-luna", "checkpoints": [8, 12], "planning_turn": 6.4}},
+   "resolution": {"t2-1": {"tier": "tier2", "alias": "claude-gw-tier2[1m]"},
+                  "t4-1": {"tier": "tier4", "alias": "claude-gw-tier4[1m]"},
+                  "t3-1": {"tier": "tier3", "alias": "claude-gw-tier3[1m]"}}}
+}
diff --git a/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/config/catalogue.json b/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/config/catalogue.json
new file mode 100644
index 000000000..23a8f7f9d
--- /dev/null
+++ b/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/config/catalogue.json
@@ -0,0 +1,24 @@
+{
+ "version": "r1-cat/1",
+ "moves": {
+  "M1": "For each file the plan edits, search `tests/`, `docs/` and the repo root for its path or key strings; open every test file the plan never names.",
+  "M2": "For each sentence that says all, only, every or none, list what it quantifies over and count the exceptions.",
+  "M3": "For each acceptance criterion that says every, all or complete, state the finite check that proves it; if none exists, say so.",
+  "M4": "For each grep or command criterion, run it against the exact text the task tells the implementer to write, not the current file.",
+  "M5": "For each mapping or decision rule, trace every input value (each reason, each mode) through to its output.",
+  "M6": "For each value a consumer reads, find the producer row that writes it, in the source document, not the checkout.",
+  "M7": "When you checked a claim is not too broad, check the other direction: where else in the repository (root files included) is the same claim stated?",
+  "M8": "When a check fails for one task, apply the same check, clause by clause, to every other task.",
+  "M9": "Compare each task body's scope with its acceptance criterion's scope and with the source document's scope.",
+  "M10": "When the plan says a test enforces a rule, list what that test can actually fail on."
+ },
+ "observable": [
+  "M1",
+  "M2",
+  "M4",
+  "M7"
+ ],
+ "observable_suffix": " No panel member has done this yet.",
+ "src_text": "source.md has not been opened yet: open the plan's source document named in your brief and read it.",
+ "finish_text": "Finish now with what you have: write your final report, ending with the findings block and the verdict line."
+}
diff --git a/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/config/catalogue.sha256 b/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/config/catalogue.sha256
new file mode 100644
index 000000000..dd78dd456
--- /dev/null
+++ b/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/config/catalogue.sha256
@@ -0,0 +1 @@
+de8baa112ab50d35f516d479d1c79502069c8735eb0b1e2a4b9b3e0cada5b3b7  config/catalogue.json
diff --git a/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/config/brief.txt b/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/config/brief.txt
new file mode 100644
index 000000000..34e41ebc1
--- /dev/null
+++ b/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/config/brief.txt
@@ -0,0 +1,5 @@
+/sc:spec-panel @@@CAND@@ --mode critique
+
+Review the candidate @@CAND@@ (sha256 of the file: @@SHA@@) against the requirements it states, review 1 of 3. The plan's source document is @@SRC@@ (sha256 of the file: @@SRCSHA@@); read both the candidate and the source document. Inspect behavior and the dependencies it touches. Report concrete wrong outcomes, not a minimum number of findings. Minor findings are notes and never fail the review; list Medium and minor findings under follow-up candidates. If an input is missing or unreadable, return incomplete. Do not edit the candidate and do not start another review. State what you covered.
+
+First-review rules (from ~/.claude/rules/prompts/document_review_loop_prompts.md, read it first): write 'review: 1 of 3' once as the first line of the report. Grading check, for each finding before you mark it blocking: write the sentence 'An implementer who follows the stated text as written builds X, and X is wrong because Y.' Blocking needs a sentence that holds with no further assumption: two stated texts that contradict each other, a stated text that causes data loss or breaks a security or safety boundary, or a stated text that an acceptance criterion cannot pass. Grade it Medium when the sentence needs a guess that the implementer picks the worse of two readings the text allows, or when the finding is a requirement the document never states rather than a stated text that does harm. End the report with the '## Findings block' (one fenced code block with info string findings-v1, one JSON object per line: id, severity CRITICAL|MAJOR|MINOR, blocking, category contradiction|unpassable-check|data-loss|safety|missing-requirement|other, anchor = 12 to 200 chars copied exactly from the candidate, optional anchor2, refs, claim) and a final 'verdict: PASS' or 'verdict: FAIL' line. Your final reply must be the complete report text.
\ No newline at end of file
diff --git a/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/manifest.json b/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/manifest.json
new file mode 100644
index 000000000..15c12e552
--- /dev/null
+++ b/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/manifest.json
@@ -0,0 +1,24 @@
+{
+  "base_commits": {
+    "TASK-WF-designSpec-20261107-075614": {
+      "sha": "0e486ab8d0eb24c6f2738ce1f895cc16755b26c1",
+      "method": "squash-first-parent",
+      "t1_start": "69f360d58d89456f559ad3de21ea75027cd72bb0"
+    },
+    "TASK-WF-makeTheAliasOnly-20261105-051649": {
+      "sha": "38eb3c58afe6988b51060ae14117172869ea4c1e",
+      "method": "squash-first-parent",
+      "t1_start": "fdb08e60c8c3f45bcd1681cd1c79c40da4247b65"
+    },
+    "TASK-WF-design-20261108-041415": {
+      "sha": "5fa680778718af9087ccbe7a823e3909f1bcceb6",
+      "method": "squash-first-parent",
+      "t1_start": "c1a436aed894a854f1081211796117d03bda700a"
+    }
+  },
+  "merge_cli": "superclaude review merge",
+  "created_utc": "2026-11-13T20:29:22Z",
+  "catalogue_sha256": "de8baa112ab50d35f516d479d1c79502069c8735eb0b1e2a4b9b3e0cada5b3b7",
+  "brief_sha256": "191c5472d2a4a8cbc8d33e81dd4c84f039cf4c1169b1c46b8850f6aee2b6f88c",
+  "judge_one_sha256": "a01bd70d370d73cb32b55a7368aa28e2c12d93403237211c3a71f339ae82cfcc"
+}
diff --git a/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/spikes/g-base.sh b/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/spikes/g-base.sh
new file mode 100755
index 000000000..e21b691d9
--- /dev/null
+++ b/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/spikes/g-base.sh
@@ -0,0 +1,22 @@
+#!/usr/bin/env bash
+# G-BASE (H3): base commit per package -> manifest.json base_commits. Usage: g-base.sh [<R1 root>]
+set -u -o pipefail
+REPO=/home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel
+R1=${1:-$REPO/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar}
+M=$R1/manifest.json
+declare -A FALLBACK=(
+  [TASK-WF-designSpec-20261107-075614]=0e486ab8d0eb24c6f2738ce1f895cc16755b26c1
+  [TASK-WF-makeTheAliasOnly-20261105-051649]=38eb3c58afe6988b51060ae14117172869ea4c1e
+  [TASK-WF-design-20261108-041415]=5fa680778718af9087ccbe7a823e3909f1bcceb6)
+[ -f "$M" ] || jq -n --arg t "$(date -u +%FT%TZ)" '{base_commits:{},merge_cli:"superclaude review merge",created_utc:$t}' > "$M"
+for P in TASK-WF-designSpec-20261107-075614 TASK-WF-makeTheAliasOnly-20261105-051649 TASK-WF-design-20261108-041415; do
+  T1=$(sed -n 's/^T1: start sha=\([0-9a-f]\{40\}\)$/\1/p' "$REPO/.dev/tasks/done/$P/progress.md" | head -1)
+  if [ -n "$T1" ] && { git -C "$REPO" cat-file -e "$T1^{commit}" 2>/dev/null || { timeout 60 git -C "$REPO" fetch -q origin "$T1" 2>/dev/null && git -C "$REPO" cat-file -e "$T1^{commit}" 2>/dev/null; }; }; then
+    SHA=$T1; METHOD=t1-start
+  else
+    SHA=${FALLBACK[$P]}; METHOD=squash-first-parent
+  fi
+  git -C "$REPO" cat-file -e "$SHA^{commit}" || { echo "FAIL $P base $SHA not in repo" >&2; exit 1; }
+  jq --arg p "$P" --arg s "$SHA" --arg m "$METHOD" --arg t "$T1" '.base_commits[$p]={sha:$s,method:$m,t1_start:$t}' "$M" > "$M.tmp" && mv "$M.tmp" "$M"
+  echo "$P $SHA $METHOD"
+done
diff --git a/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/spikes/g-pins.sh b/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/spikes/g-pins.sh
new file mode 100755
index 000000000..8cf123999
--- /dev/null
+++ b/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/spikes/g-pins.sh
@@ -0,0 +1,15 @@
+#!/usr/bin/env bash
+# G-PINS (R-07): sha256 pins of catalogue, brief, judge-one.sh; catalogue ground-truth check -> spikes/g-cat.json
+set -u -o pipefail
+REPO=/home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel
+R1=${1:-$REPO/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar}
+A1DIR=$REPO/.dev/eval-workspaces/tasklist-review-panel/20261111-a1
+M=$R1/manifest.json
+[ -f "$M" ] || { echo "FAIL run g-base.sh first" >&2; exit 1; }
+cd "$R1" && sha256sum -c --quiet config/catalogue.sha256 || { echo "FAIL catalogue.json differs from config/catalogue.sha256" >&2; exit 1; }
+CAT=$(sha256sum "$R1/config/catalogue.json" | cut -d' ' -f1)
+BRIEF=$(sha256sum "$R1/config/brief.txt" | cut -d' ' -f1)
+JUDGE=$(sha256sum "$A1DIR/tools/tmp-scripts/judge-one.sh" | cut -d' ' -f1)
+jq --arg c "$CAT" --arg b "$BRIEF" --arg j "$JUDGE" '.catalogue_sha256=$c|.brief_sha256=$b|.judge_one_sha256=$j' "$M" > "$M.tmp" && mv "$M.tmp" "$M"
+cd "$REPO" && uv run python "$R1/tools/collab_summary.py" catcheck "$R1/config/catalogue.json" "$A1DIR"/TASK-WF-*/ground-truth.json > "$R1/spikes/g-cat.json"
+jq -c . "$R1/spikes/g-cat.json"
diff --git a/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/spikes/g-cat.json b/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/spikes/g-cat.json
new file mode 100644
index 000000000..72278db32
--- /dev/null
+++ b/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/spikes/g-cat.json
@@ -0,0 +1 @@
+{"ground_truth_files": 3, "hits": [], "pass": true}
diff --git a/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tools/collab_summary.py b/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tools/collab_summary.py
new file mode 100644
index 000000000..fd7eefb69
--- /dev/null
+++ b/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tools/collab_summary.py
@@ -0,0 +1,60 @@
+"""collab_summary.py: audits, quarantine and collab.json for one package of one row (R-23, R-09).
+
+Usage (run from REPO with `uv run python`):
+  collab_summary.py pre  <row> <pkg> [--root <R1>] [--sb <SB>]
+  collab_summary.py post <row> <pkg> [--root <R1>] [--sb <SB>]
+  collab_summary.py catcheck <catalogue.json> <ground-truth.json>...   (G-PINS, R-07)
+"""
+
+from __future__ import annotations
+
+import json
+import sys
+
+WINDOW = 12
+
+
+def gt_hits(texts: list[str], quotes: list[str]) -> list[dict]:
+    """Every 12-character window of a ground-truth plan_quote found inside one of the texts."""
+    flat = lambda s: " ".join(s.split())  # noqa: E731
+    hits = []
+    for qi, q in enumerate(quotes):
+        q = flat(q)
+        wins = {q[i : i + WINDOW] for i in range(max(0, len(q) - WINDOW + 1))}
+        for ti, t in enumerate(texts):
+            t = flat(t)
+            for w in sorted(wins):
+                if w in t:
+                    hits.append({"quote": qi, "text": ti, "window": w})
+                    break
+    return hits
+
+
+def catalogue_texts(cat: dict) -> list[str]:
+    out = []
+    for m, t in cat["moves"].items():
+        out.append(t)
+        if m in cat["observable"]:
+            out.append(t + cat["observable_suffix"])
+    return out + [cat["src_text"], cat["finish_text"]]
+
+
+def gt_quotes(paths: list[str]) -> list[str]:
+    return [it["plan_quote"] for p in paths for it in json.load(open(p))["items"] if it.get("plan_quote")]
+
+
+def cmd_catcheck(cat_path: str, gt_paths: list[str]) -> int:
+    hits = gt_hits(catalogue_texts(json.load(open(cat_path))), gt_quotes(gt_paths))
+    print(json.dumps({"ground_truth_files": len(gt_paths), "hits": hits, "pass": not hits}))
+    return 0 if not hits else 1
+
+
+def main(argv: list[str]) -> int:
+    if len(argv) >= 3 and argv[0] == "catcheck":
+        return cmd_catcheck(argv[1], argv[2:])
+    print(__doc__, file=sys.stderr)
+    return 2
+
+
+if __name__ == "__main__":
+    sys.exit(main(sys.argv[1:]))

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

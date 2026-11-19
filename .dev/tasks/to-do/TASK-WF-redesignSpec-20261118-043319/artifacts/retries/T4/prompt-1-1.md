9956bcbe43087872f113a782a3e6397cb52e92c4
Review one task for spec compliance.

Task brief: ## Task 4: Score the baseline and close Phase 1

Depends on: Task 1, Task 2, Task 3

Spec step 0.8. Run the harness (Task 1) at the current commit into `./artifacts/gates/p0/iter-1/`, rasterise per `png-route.md`, spawn one fresh reviewer per width with the reviewer prompt, and store the scores in `.dev/issues/409/visual-parity/scores/baseline.json`. Measure the RB-22 threshold N (the longest interior blank run in the 160-column rows of the `base` fixture) and write it to `.dev/issues/409/visual-parity/scores/baseline.md`. Expected: RB-01 to RB-04 and RB-09 to RB-18 FAIL; the plain-text rows RB-05 to RB-08 pass. If the baseline passes any High row, revise `rubric.md` once, then freeze it.

Acceptance criteria:
- `scores/baseline.json` and `scores/baseline.md` exist, the latter holding the measured number N for RB-22.
- No High rubric row passes on the baseline, or the single permitted rubric revision is recorded with the reason.
- `uv run pytest tests/observe/ -v` is green.
Global constraints: - Numbering: plan Phase N is spec Phase N-1 (plan Phase 1 is the spec's Phase 0, plan Phase 8 is the spec's Phase 7). Task text names the plan phase unless it says "spec Phase".
- Shorthand used in every task: OBS is `src/superclaude/cli/observe/`; T is `tests/observe/`; VP is `.dev/issues/409/visual-parity/`; RR is `.dev/issues/409/bmad/spec-orca-observer/rendering-rules.md`; "the spec" is `./source.md` (its section numbers, Part B step numbers such as 1.4 and Part C step numbers such as 2.12 are cited in each task).
- Do not edit `OBS/export.py`. `record_text` and `snapshot_json` stay byte-identical. Question text appears on screen only; both hash canaries (record and snapshot) pass from Phase 1 onward.
- NO_COLOR output has zero ESC bytes and the same text as the coloured output after SGR removal. ASCII output is pure ASCII with `+ - |` borders and `#` for the block glyph. The 16-colour theme keeps eight distinct role colours.
- Draw only facts the screen has: no owner, requester, mapped-tree, SIGNALS bars or affected-session list (accepted divergences AD-1 to AD-8 of the spec).
- Existing source guards stay true: `QUESTION_GATE_PASSED` and `QUESTION_LINK_PASSED` (`OBS/commands.py` lines 67 and 70) untouched, the words `release-gates.md` and `Task 18` stay in `OBS/commands.py`, no `Console(`, `from_markup`, `sorted(`, `.sort(` or adapter, collector, parse import in `OBS/render.py`, and `len(group.renderables) == len(screen_lines(...))` holds.
- Owner rulings already applied (spec section 10 and Part C): Decision Desk in two columns at 160 and 116 and stacked at 80; questions screen stacked at every width; the 64-hex hash is never shown on screen; the other defaults of spec section 10 apply (D-2 to D-5, D-7 to D-12). OPEN-1 to OPEN-3 are treated as Medium and gating.
- Phase gate rule (spec section 8): each phase ends with the render gate, at most 3 iterations, a fresh reviewer per width each iteration. A phase closes only when every in-scope High and Medium rubric row passes in the last iteration. If a row still fails after iteration 3, or two consecutive iterations do not improve the passing count, write `./.dev/issues/409/visual-parity/scores/<phase>/stop.md` (path relative to the repository root), stop, and ask the owner. Never start the next phase before the previous gate closes.
- Gate outputs (renders, captures, scores) are written under `./artifacts/gates/<phase>/iter-<n>/` in this package; the closing record `scores.json` of the last iteration is also copied to `.dev/issues/409/visual-parity/scores/<phase>/` because the spec's definition of done reads it there.
- The spec's Phase 0 inputs (`render_current.py` and the baseline captures) exist only untracked in a local checkout that must never be edited. They are not on this branch, so Phase 1 rebuilds `render_current.py` from the observer's own view builders and fixtures. Never edit the local checkout.
- Goldens are regenerated only from the current tree, in the same change set as the change that moves them; styled bytes are never written into a golden.
- Nothing under `.claude/` is staged. This plan does not commit, push or open a PR before a human asks; the final task states the PR route for that moment (`/sc:pr-submit --monitor 3`, target `IronbellyOrg/IronClaude`, never `SuperClaude-Org`).
- Judgment call recorded here: spec step 2.13 names `_field_lines`, a function that step 5.2 only creates in the desk phase (spec Phase 5, plan Phase 6). The space-diet work (spec Phase 2, plan Phase 3) therefore applies the label, alignment and badge changes to the existing desk field loop in `OBS/render.py` (lines 347-353 today), and plan Phase 6 replaces that loop with `_field_lines` while keeping those changes.
Start sha: 9956bcbe43087872f113a782a3e6397cb52e92c4
Diff against the start snapshot: Codegraph context: index_state: fresh; checked_at: 2026-11-18T04:42:32Z; worktree_root: /home/coder/workspaces/worktrees/IronClaude/issue-606; projectPath: /home/coder/workspaces/worktrees/IronClaude/issue-606
call codegraph only when index_state: fresh, never to widen scope
Q2b: Grep floor; the task adds score documents only; no symbol changed.
Touched files (new, untracked): .dev/issues/409/visual-parity/scores/baseline.json, .dev/issues/409/visual-parity/scores/baseline.md. Task evidence in the package folder /home/coder/workspaces/worktrees/IronClaude/issue-606/.dev/tasks/to-do/TASK-WF-redesignSpec-20261118-043319/artifacts/gates/p0/iter-1/ : checks.json, per-width files, reviewer-outputs/width-<W>.scores.md (the three fresh reviewers' answers, one per width, scoring RB-01 to RB-29). Rubric: .dev/issues/409/visual-parity/rubric/rubric.md; PNG route result: .dev/issues/409/visual-parity/png-route.md. uv run pytest tests/observe/ -q printed '794 passed'.

diff --git a/.dev/issues/409/visual-parity/scores/baseline.json b/.dev/issues/409/visual-parity/scores/baseline.json
new file mode 100644
index 000000000..4643d7ee8
--- /dev/null
+++ b/.dev/issues/409/visual-parity/scores/baseline.json
@@ -0,0 +1,39 @@
+{
+  "phase": "P0 baseline",
+  "iteration": 1,
+  "method": "text and ANSI tier (no PNG: no browser installed, see png-route.md); one fresh reviewer per width, all rows RB-01 to RB-29 scored",
+  "harness_run": "package folder artifacts/gates/p0/iter-1/ (checks.json + per-width files)",
+  "full_evidence": "the three reviewer returns with one evidence line per row are kept in the package folder artifacts/gates/p0/iter-1/reviewer-outputs/ (width-160.scores.md, width-116.scores.md, width-80.scores.md)",
+  "rows": {
+    "RB-01": {"160": "FAIL", "116": "FAIL", "80": "FAIL"},
+    "RB-02": {"160": "FAIL", "116": "FAIL", "80": "FAIL"},
+    "RB-03": {"160": "FAIL", "116": "FAIL", "80": "FAIL"},
+    "RB-04": {"160": "FAIL", "116": "FAIL", "80": "PASS"},
+    "RB-05": {"160": "PASS", "116": "PASS", "80": "PASS"},
+    "RB-06": {"160": "PASS", "116": "PASS", "80": "PASS"},
+    "RB-07": {"160": "PASS", "116": "PASS", "80": "PASS"},
+    "RB-08": {"160": "PASS", "116": "PASS", "80": "FAIL"},
+    "RB-09": {"160": "FAIL", "116": "FAIL", "80": "FAIL"},
+    "RB-10": {"160": "FAIL", "116": "FAIL", "80": "FAIL"},
+    "RB-11": {"160": "FAIL", "116": "FAIL", "80": "FAIL"},
+    "RB-12": {"160": "PASS", "116": "FAIL", "80": "FAIL"},
+    "RB-13": {"160": "PASS", "116": "FAIL", "80": "FAIL"},
+    "RB-14": {"160": "FAIL", "116": "FAIL", "80": "FAIL"},
+    "RB-15": {"160": "FAIL", "116": "FAIL", "80": "FAIL"},
+    "RB-16": {"160": "FAIL", "116": "FAIL", "80": "FAIL"},
+    "RB-17": {"160": "PASS", "116": "PASS", "80": "PASS"},
+    "RB-18": {"160": "FAIL", "116": "FAIL", "80": "FAIL"},
+    "RB-19": {"160": "PASS", "116": "PASS", "80": "PASS"},
+    "RB-20": {"160": "FAIL", "116": "FAIL", "80": "FAIL"},
+    "RB-21": {"160": "PASS", "116": "PASS", "80": "FAIL"},
+    "RB-22": {"160": "PASS", "116": "FAIL", "80": "FAIL"},
+    "RB-23": {"160": "FAIL", "116": "FAIL", "80": "FAIL"},
+    "RB-24": {"160": "FAIL", "116": "FAIL", "80": "FAIL"},
+    "RB-25": {"160": "FAIL", "116": "FAIL", "80": "FAIL"},
+    "RB-26": {"160": "FAIL", "116": "FAIL", "80": "FAIL"},
+    "RB-27": {"160": "FAIL", "116": "FAIL", "80": "FAIL"},
+    "RB-28": {"160": "FAIL", "116": "FAIL", "80": "FAIL"},
+    "RB-29": {"160": "FAIL", "116": "FAIL", "80": "FAIL"}
+  },
+  "discrimination_note": "High rows that pass on the baseline are RB-05, RB-06, RB-07 (and RB-08 at 160 and 116, RB-04 at 80 by design: no strip exists at 80). The spec expects exactly these plain-text rows to pass today, so the rubric is discriminating and was not revised. RB-17 and RB-19 pass only vacuously or by the old rule (RB-27 replaces RB-19 and fails)."
+}
diff --git a/.dev/issues/409/visual-parity/scores/baseline.md b/.dev/issues/409/visual-parity/scores/baseline.md
new file mode 100644
index 000000000..6b612ee47
--- /dev/null
+++ b/.dev/issues/409/visual-parity/scores/baseline.md
@@ -0,0 +1,11 @@
+# Baseline measurements (plan Phase 1, spec step 0.8)
+
+Measured at the start commit of this work (observer unchanged, `git diff --stat -- src/` empty), from the harness output in the package folder `artifacts/gates/p0/iter-1/`.
+
+RB-22 threshold N: 18
+
+The number is the longest run of consecutive spaces between two non-space characters inside a ledger row line of the `ledger` screen (`base` fixture) at 160 columns (37 row lines). The same measure at 116 columns is 48 and at 80 columns is 34, so RB-22 fails on the baseline for both (a wide blank band after the id column, finding M-17).
+
+Height test (`tests/observe/test_height_budget.py`): all 18 cases pass on today's code, heights 24, 40 and 44 at widths 160, 116 and 80 with 3 and 20 questions. No failing height set exists, so none is excluded.
+
+PNG route: FAIL (no browser installed); the scores below come from the text and ANSI tier (`png-route.md`).
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

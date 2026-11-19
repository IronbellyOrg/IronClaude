21c08e50017744f954b18fb995347300a324ff96
Review one task for spec compliance.

Task brief: ## Task 10: Split the records golden from the presentation golden

Depends on: Task 9

Spec step 2.1 (first in this phase). Create `tests/observe/golden_release1_records.json` from the current `tests/observe/golden_release1_surface.json`, keeping per variant (`base`, `empty`, `source-loss`, `injection`, `missing-fields`) only `header1`, `header2`, `gap_notice`, `record_text` and `snapshot_json`, written with `json.dumps(..., indent=1, sort_keys=True, ensure_ascii=False)` and no trailing newline. Add `test_release1_records_are_byte_identical_to_the_recorded_surface` to `tests/observe/test_render.py` comparing those keys from `surface()` in `tests/observe/release1_surface.py`. This file is never regenerated afterwards.

Acceptance criteria:
- The new test passes and `git diff --stat -- src/` is empty.
- `golden_release1_records.json` holds no `lines_*` or `printed_*` key.
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
Start sha: 21c08e50017744f954b18fb995347300a324ff96
Diff against the start snapshot: Codegraph context: index_state: fresh; checked_at: 2026-11-18T04:42:32Z; worktree_root: /home/coder/workspaces/worktrees/IronClaude/issue-606; projectPath: /home/coder/workspaces/worktrees/IronClaude/issue-606
call codegraph only when index_state: fresh, never to widen scope
Q2b: Grep floor; the task adds a test and a data file; no symbol changed; surface() in tests/observe/release1_surface.py is read only.
Evidence: uv run pytest tests/observe/ -q printed '848 passed in 24.03s' (847 before); ruff check All checks passed; git diff --stat -- src/superclaude/cli/observe/export.py is empty. The new data file tests/observe/golden_release1_records.json (101327 bytes, new, untracked, too long to include here) was built from tests/observe/golden_release1_surface.json keeping per variant only header1, header2, gap_notice, record_text and snapshot_json, json.dumps(indent=1, sort_keys=True, ensure_ascii=False), no trailing newline; its 5 variants are base, empty, injection, missing-fields, source-loss. You may Read it and tests/observe/golden_release1_surface.json.

diff --git a/tests/observe/test_render.py b/tests/observe/test_render.py
index 2a37fe1d8..403ae639f 100644
--- a/tests/observe/test_render.py
+++ b/tests/observe/test_render.py
@@ -628,6 +628,30 @@ def test_t47_questions_off_is_byte_identical_to_the_recorded_release_1_surface()
             assert current[variant][key] == text, f"{variant}:{key}"
 
 
+RECORD_KEYS = ("header1", "header2", "gap_notice", "record_text", "snapshot_json")
+
+
+def test_release1_records_are_byte_identical_to_the_recorded_surface():
+    """The record, the JSON snapshot and the three header texts of release 1, kept apart from
+    the screen lines so they stay enforced after the presentation golden is re-baselined.
+    ``golden_release1_records.json`` is never regenerated."""
+    from tests.observe.release1_surface import surface
+
+    path = Path(__file__).parent / "golden_release1_records.json"
+    golden = json.loads(path.read_text(encoding="utf-8"))
+    current = surface()
+    assert current.keys() == golden.keys()
+    for variant, expected in golden.items():
+        assert expected.keys() == set(RECORD_KEYS), variant
+        for key, text in expected.items():
+            assert current[variant][key] == text, f"{variant}:{key}"
+    # The file itself is the recorded serialisation of exactly these keys.
+    subset = {v: {k: e[k] for k in RECORD_KEYS} for v, e in current.items()}
+    assert json.dumps(
+        subset, indent=1, sort_keys=True, ensure_ascii=False
+    ) == path.read_text(encoding="utf-8")
+
+
 # -- R2 UX review follow-up (2026-11-12): owner decisions and the critical and high findings -------------------------------
 
 import dataclasses  # noqa: E402
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

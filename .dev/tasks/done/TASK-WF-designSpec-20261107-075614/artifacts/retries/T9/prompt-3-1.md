4e6a6df7dfa46c8c0d4c1c0d3b7cde488dfdff79
Review one task for spec compliance.

Task brief: ## Task 9: Wire the Wave 0 resume and `off` hook, the flag row, the output row and the wave line into `SKILL.md`

Depends on: Task 6
Depends on: Task 8

Edit `src/superclaude/skills/sc-pr-submit-protocol/SKILL.md` additively, using the pins and line-content rules recorded in `./artifacts/pre-build-gate.md`: one new bullet under Wave 0, written as a flat line before the Wave 1 bullet, that applies at every ordinal and in both modes and carries no L3 or `draft` condition; it states that on `--resume`, or when the run log already holds guard events, the ref `refs/merge-guard.md` (Resume and Exit report) is loaded before Wave 1 and before any edit, release or re-trigger, and that at L3 with `--merge-guard off` the line "Remediation is unprotected: --merge-guard off." is printed once and no draft call is made. Add one `--merge-guard {draft,off}` row to the Required Input flag table beside `--conflict-max-tier`; one row `merge_guard` to the output table (values `off`, `released`, `held`, `user_override`, `unavailable`) that also carries the literal L2 line "PR #N is still mergeable; this run's fixes are local only." so a fresh L2 run prints it without loading the ref; and one line in the wave-structure list. No new python fence. Where a new line would contain `gh pr` or `gh api`, rephrase it (for example "print the clear command from the ref") so that no classification entry is needed; if one is unavoidable, add its `WRITE_VERB_CLASSIFICATION` entry as the last step. Extend `tests/pr_submit/test_merge_guard_protocol.py` with a test for the Wave 0 bullet (it names `--resume`, sits before the Wave 1 bullet, contains no `L3 only` or `draft` gate wording and contains the literal `off` line), one for the flag row, one for the output row including the literal L2 line, and one for the wave-structure line. Run `make sync-dev`.

Acceptance criteria:
- T9.AC1: The Wave 0 test fails when the bullet is placed after the Wave 1 bullet, when it names an L3 or `draft` condition, or when the literal `off` line is missing, and passes on the real file.
- T9.AC2: A test asserts the literal text "PR #N is still mergeable; this run's fixes are local only." is present in `SKILL.md` itself (not only in the ref), so a fresh L2 run needs no ref load.
- T9.AC3: `uv run pytest tests/pr_submit/test_static_grep.py tests/pr_submit/test_conflict_sync_protocol.py tests/pr_submit/test_cosmos_protocol.py tests/pr_submit/test_codex_reviews.py tests/pr_submit/test_merge_guard_protocol.py tests/skills/test_worker_contract.py -q` passes with no edit to any existing test expectation other than those listed in Tasks 2, 5, 7 and 8.
- T9.AC4: `SKILL.md` still has exactly one python code fence and no `src/superclaude` string, and the new lines contain neither `evidence-validator` nor `conflict-intent.md`.
- T9.AC5: `make verify-sync` exits 0.
Global constraints: - Edit canonical files under `src/superclaude/` only, then run `make sync-dev`; do not stage `.claude/` mirror files. Use UV for every Python command (`uv run pytest ...`, `uv run ruff ...`).
- The new pure module `src/superclaude/pr_submit/merge_guard.py` and every file already listed in `CORE_PURE_FILES` of `tests/pr_submit/test_static_grep.py` (including `refs/state-machine.md` and `refs/loop-guard.md`) must contain no whole word `gh` or `git` on any line, comments included. The module must not import `recovery` (an import cycle through `run_log`).
- Protocol and command text must not contain the string `src/superclaude`; `SKILL.md` must keep exactly one python code fence; edits to `SKILL.md` and `refs/state-machine.md` are additive sentences, bullets and rows placed after, never inside, the sentences pinned by `tests/pr_submit/test_static_grep.py` and `tests/pr_submit/test_conflict_sync_protocol.py`. A new `SKILL.md` line must not name `evidence-validator` or `conflict-intent.md` (a line-content test allows those words only on lines that also say "Tier 2") and must not use wording that the forbidden-force-push line test rejects; Task 1 lists the exact line-content rules before any edit.
- Every new line under `src/superclaude/skills/`, `src/superclaude/commands/` or `src/superclaude/agents/` that contains `gh pr`, `gh api` or a git write verb needs one entry in `WRITE_VERB_CLASSIFICATION` in `tests/skills/test_worker_contract.py` (key: repo-relative path, verb text, exact stripped line; category `never-worker` with the standard pr-submit reason text of the neighbouring entries). Add each entry last in the task that writes the file, because editing a classified line later makes the entry stale and fails `test_classification_table_has_no_stale_entries`; run `uv run pytest tests/skills/test_worker_contract.py -q` in that task.
- Cite tests and constants by symbol name (for example `_NEW_KEY_DEFAULTS`, `_RESOLUTION_SCRIPTS`, `CORE_PURE_FILES`, `WRITE_VERB_CLASSIFICATION`), never by line number, in plan text, task artifacts and the protocol prose this plan produces. Protocol prose carries no `file:NNN` pointers.
- No test or task may call GitHub. Script tests use a fake `gh` executable on `PATH`. The behaviour that needs a disposable fork PR (gates G1 live part, G2 live part, G4, G5 and G6 of ./source.md section 8) is recorded as OPEN and is a release gate, never claimed verified.
- Scope limits (non-goals of ./source.md): no labels, commit statuses or rulesets; ordinals 0 to 2 change only by one report line; conflict-merge cycles (Tier 1 and Tier 2) are never engaged; the guard is not held through re-review or CI; a second concurrent run on the same PR is unsupported.
- Owner decisions already accepted (listed in the ./source.md header and section 8) are fixed: draft not label; engage at the end of Wave 3; default on at `--monitor 3`; release on the confirmed push before replies and the re-trigger; unreadable timeline or unpublished exit keeps the PR draft; build now with no GitHub calls, release gate for G4 and G5.
- Run `make sync-dev` at the end of every task that edits a file under `src/superclaude/skills/` or `src/superclaude/commands/`, because the full test suite runs `make verify-sync` through `tests/cli/test_verify_sync_hooks.py`.
Start sha: 4e6a6df7dfa46c8c0d4c1c0d3b7cde488dfdff79
Diff against the start snapshot: diff --git a/src/superclaude/skills/sc-pr-submit-protocol/SKILL.md b/src/superclaude/skills/sc-pr-submit-protocol/SKILL.md
index 39d46243..b238ff77 100644
--- a/src/superclaude/skills/sc-pr-submit-protocol/SKILL.md
+++ b/src/superclaude/skills/sc-pr-submit-protocol/SKILL.md
@@ -217,6 +217,7 @@ Existing grounding rejects a null current line; it cannot authorize an automatic
 | `--silence-timeout` | No (default 300s) | No-Augment-activity window. Reject `< 30`. Clamped to `--timeout`. L3 may re-request once. |
 | `--resume <abs-run-log-path>` | No | Reconstruct state from JSONL (§12). |
 | `--conflict-max-tier {0,1,2}` | No (default 0) | Highest merge-conflict tier the skill may act on: 0 (default) detect and report only, 1 also regenerate a conflicted root `uv.lock` (Tier 1, opt-in because `uv lock` can run the PR's build code), 2 also resolve text conflicts by stated intent (Tier 2, off by default). Tier 3 never resolves. |
+| `--merge-guard {draft,off}` | No (default `draft`) | At L3, hold the PR as a draft while a fix cycle runs and mark it ready again once the fix push is confirmed (`draft`); `off` leaves the PR untouched and prints "Remediation is unprotected: --merge-guard off." once. No effect below L3. |
 
 **STOP** if `--monitor >= 1` and the PR cannot be confirmed on the resolved target repo (origin's
 `owner/repo`, parsed from `git remote get-url origin`): a wrong origin, or a returned URL whose `owner/repo` ≠ the resolved target → HALT,
@@ -241,6 +242,7 @@ monitor that could only ever report `polling`. `--monitor 0` skips this prefligh
 | `sync_tier` | int or null | Highest merge-conflict tier seen this run (0 to 3; null when it could not be classified). |
 | `sync_outcome` | enum | `none` / `report_only` / `left_in_progress` / `pushed` / `aborted` / `halted`. |
 | `sync_push_count` | int | Landed Tier 1 sync pushes (`kind: "sync"`, at most `SYNC_CAP = 1`); never counted in `push_count`. |
+| `merge_guard` | enum | `off` / `released` / `held` / `user_override` / `unavailable`: the draft guard's standing at the end of the run (`refs/merge-guard.md` section 6 maps it). A `held` report carries the reason and the clear command from that ref. A fresh `--monitor 2` run that applies fixes and halts before the push also prints: "PR #N is still mergeable; this run's fixes are local only." |
 | `reply_count` | int | Threads replied to. |
 | `summary_posted` | bool | Whether the single clean-re-review summary thread was posted. |
 | `applied_edits` | int | Grounded edits applied this run (INV-016 predicate 5). |
@@ -258,6 +260,7 @@ The `status` enum is unchanged: `terminal_augment_no_response` means no configur
 ```text
 Wave 0: Open PR + verify target   ← (no ref; gh pr create --repo, pre-PR checks)
 Wave 0c: (L1+) conflict check + report      ← loads refs/conflict-mechanical.md ONLY when the probe runs
+Wave 0d: (all ordinals) guard resume + off notice ← loads refs/merge-guard.md ONLY on --resume or when the run log holds guard events
 Wave 1: Arm + poll                ← loads refs/detection-contract.md (baked identity) + refs/augment-poll.md
 C-initial: (L3, Tier 2) merge cycle before the first review poll ← loads refs/conflict-mechanical.md + refs/conflict-intent.md
 Wave 2: Classify + re-grade       ← loads refs/severity-routing.md
@@ -274,6 +277,7 @@ Wave 8a: (L1+) act on a conflict before the CI wait ← loads refs/conflict-mech
 - **Wave 0 (all ordinals):** resolve the target repo once from the origin remote (`REPO="$(git remote get-url origin | sed -E 's#^ssh://[^/]+/##; s#^git@[^:]+:##; s#^https?://[^/]+/##; s#\.git$##')"`; only if origin has no URL, fall back to `gh repo view --json nameWithOwner -q .nameWithOwner` — never prefer it, because gh picks an `upstream` remote over `origin`) and the base branch (`gh repo view "$REPO" --json defaultBranchRef -q .defaultBranchRef.name`, overridable via `--base`). BEFORE creating anything: confirm `git remote -v` shows origin = `$REPO` and rebase if behind `origin/<base>` only at L0 (at L1+ the create path does not rebase and does not halt: the branch is already published when `gh pr create` runs, so report how many commits it is behind, a Tier 0 result; with `--pr <N>`, at any level, do not rebase: the PR head is already published, so report how many commits it is behind instead). At L1+, also before creating or attaching, run `scripts/probe-merge.sh --ops-only --repo "$REPO"`: a non-null `foreign_op` (a merge, rebase, cherry-pick, revert or sequencer operation in progress) → HALT before Wave 1 with status `terminal_halted`, reason `foreign_op_in_progress`, nothing created (on `--resume`, `conflict_resume_plan` in `refs/conflict-mechanical.md` decides first). Then open the PR with `gh pr create --repo "$REPO" --base <base> --head <head> --title "..." --body "..."` and verify the returned URL's `owner/repo` equals `$REPO` (a misroute → HALT). With `--pr <N>`, skip `gh pr create` and attach to that PR instead, checking the URL from `gh pr view <N> --repo "$REPO" --json url`. Pass `--repo "$REPO"` to every poll/reply/retrigger script too. At **L0 (`--monitor 0`)** the FSM never leaves `S0_IDLE` — open the PR and return, byte-for-byte identical to today (AC-1).
 - **Wave 0 head binding (L1+ only; L0 skips it):** after `gh pr create`, or on `--pr <N>` attach, read the PR head with `gh pr view <N> --repo "$REPO" --json headRefName,headRefOid,isCrossRepository` (a failed or unparsable read → HALT) and the checkout with `git branch --show-current` and `git rev-parse HEAD`. Require `superclaude.pr_submit.fsm.pr_head_ok(local_branch, local_sha, headRefName, headRefOid, isCrossRepository, allow_cross_repo=(ordinal < 3))`; a head on a fork is allowed only below L3, where nothing is pushed. False → HALT before Wave 1 with status `terminal_halted`, reason `pr_head_mismatch` (appended to the run-log when one exists), and tell the operator: "PR #<N>'s head `<headRefName>`@<headRefOid> does not match your checkout `<local_branch>`@<local_sha>. Do not close the PR. Check out `<headRefName>` and make it equal the PR head (push if you are ahead; `git pull --ff-only` if you are behind; this skill never rewrites a published branch), then re-run with `--pr <N>`." True → bind `HEAD_BRANCH := headRefName` and `pre_push_sha := headRefOid` for the whole run; every push targets `HEAD_BRANCH`, never the checkout's branch name. `--resume` repeats this binding against the live PR: when crash recovery finds a dangling `push_initiated`, check only the branch (`pr_branch_ok(local_branch, headRefName, isCrossRepository, allow_cross_repo=(ordinal < 3))` and `pr_branch_ok(<the record's target_branch>, headRefName, False)`), leave the SHA to `resolve_crash_window` (local HEAD may already be the fix commit), and set `pre_push_sha` from that record: its `target_sha` when the push landed (Branch A), its `pre_push_sha` when the push is re-driven (Branch B: skip the Wave 6 fix commit, set `target_sha` from the record, and the re-driven push first runs the Wave 6 pre-push head guard with the record's `pre_push_sha`; after Branch A, the guard's parent check stops the next push if local commits were made since the landed push); otherwise require the full `pr_head_ok` and set `pre_push_sha := headRefOid`.
 - **Wave 0 conflict check (L1+ only; L0 skips it):** after the head binding, read `gh pr view <N> --repo "$REPO" --json baseRefName,mergeable,mergeStateStatus` (re-read an `UNKNOWN` up to 3 times, 10 s apart) and normalise it with `superclaude.pr_submit.conflicts.mergeability_hint`. Only `conflicting` or a persistent `unknown` loads `refs/conflict-mechanical.md` and runs `scripts/probe-merge.sh`; follow that ref to classify, print the plan before any edit, and route with `conflict_action(hook="wave0")` (Tier 3 at L3 halts here: `terminal_halted`, reason `conflict_tier3`, nothing touched). Any other hint is Tier 0: report "<N> commits behind, no conflicts" (or the `BLOCKED` reason) and continue; no ref is loaded.
+- **Wave 0 merge-guard hook (every ordinal, both modes):** on `--resume`, or when the run log already holds guard events (`draft_guard_requested` or `draft_guard_settled`), load `refs/merge-guard.md` (Exit report and Resume) before Wave 1 and before any edit, release or re-trigger, and follow its Resume rows with the held cycle's `target_sha`, so a PR left held by an earlier run is reported or released first. At L3 with `--merge-guard off`, print "Remediation is unprotected: --merge-guard off." once and make no draft-state call.
 - **Wave 1 (L1+):** load the contract via `superclaude.pr_submit.DetectionContract.for_arming()` — prefers an optional operator-local override (gitignored `.dev/pr-monitor/detection-contract.locked.md`) and falls back to the SHIPPED `refs/detection-contract.md` (baked `augmentcode[bot]` / `augmentcode` defaults). A missing or unlocked override is not a halt; the contract also carries the Codex identities (`codex_bot_login`, `codex_app_slug`) and `codex_retrigger_phrase`, and Codex is disabled only when both Codex identities are blank (it stays on while either remains). Initialize the output-dir + run-log + baseline, then enter the **attended poll loop** (above) with `scripts/poll-augment-review.sh` (interval ≥30s, timeout default 600s; the one snapshot serves both reviewers); each JSON line passes the snapshot gate before any FSM outcome; incomplete evidence keeps polling. Record `reviewer_absent{reviewer}` for a reviewer the merge settles as absent, and `reviewer_incomplete{reviewer, phase: "initial"}` for a present reviewer that did not complete by `--timeout` while the other's result was used. Every event that concerns one reviewer carries a `reviewer` field (`"augment"` or `"codex"`; a missing field means `augment`): `poll_result` (with the per-reviewer wait outcomes), `review_detected`, `findings_normalized`, `finding_verified`, `finding_unverified`, `route_decision`, `reply_posted`, `thread_resolved`, `rereview_requested`. On `--resume`, read `rebuild_state()["absent_reviewers"]` and keep those reviewers absent. Arm exactly once at L1+ (T-109); never at L0 (T-110). `--monitor 0` remains no-monitor. **C-initial (L3, Tier 2, only when Wave 0 planned it under `--conflict-max-tier 2`):** after arming and before the first review poll, load `refs/conflict-intent.md` and run the Tier 2 merge cycle of `refs/conflict-mechanical.md` through `transition(S2_CLASSIFY, "conflicting")`; its S5 wait is the run's first review wait.
 - **Wave 2:** load `refs/severity-routing.md`; use only the snapshot gate's `actionable_finding_comments` → `finding_from_comment` → `remap_severity(finding)` → `route(finding)` results from `superclaude.pr_submit` (Augment's and, for Codex, `codex_finding_comments` → the same three calls; a Codex P0/P1/P2/P3 badge is its severity hint, a missing or malformed badge is the Medium fail-safe), then map the remapped tier to its troubleshoot route (Medium → `--fix`; High/Critical → `--depth deep --fix`; Low/Nit → report-only). NEVER emit `--depth quick --fix`. Group the merged findings with `dedup_groups(findings)` (same path and line, `original_line` when the line is null): a **dedup group routes at its members' highest remapped tier**; every member keeps its own finding, verdict and thread.
 - **Wave 3:** load `refs/finding-verify.md`; spawn the `evidence-validator` agent (read-only) to confirm each finding's cited file:line exists and the defect reproduces (one verdict per finding, Augment and Codex in one batch). `unverified` → REPORT_ONLY, consuming NO round. A dedup group is dispatched only when at least one member is verified. Context only, once per cycle before verification: invoke `> Skill sc:impact-protocol` with `--diff origin/<baseRefName> --depth 1 --output-dir <output-dir>/impact/wave3 --caller sc-pr-submit-protocol` and read only `status`, `degraded`, `dependents[].caller`, `dependents[].file` and `unmapped_files` from its `return-contract.yaml`; the dependent names and files are background for the verifier, never a reason to verify, drop or re-tier a finding. Copy its `degraded` tokens into the run-log; `status: blocked|failed` counts as `graph:absent`.

diff --git a/tests/pr_submit/test_merge_guard_protocol.py b/tests/pr_submit/test_merge_guard_protocol.py
index ce955349..918e02b8 100644
--- a/tests/pr_submit/test_merge_guard_protocol.py
+++ b/tests/pr_submit/test_merge_guard_protocol.py
@@ -342,3 +342,193 @@ def test_a_draft_guard_unavailable_halt_reports_unavailable():
     assert "reason `draft_guard_unavailable` reports `unavailable`" in report
     assert "whatever `guard_status` returns" in report
     assert mg.guard_status(None, mg.GuardMode.DRAFT, 3) == "released"
+
+
+# --- the SKILL.md wiring (Wave 0 hook, flag row, output row, wave line) ----------
+
+SKILL = SKILL_DIR / "SKILL.md"
+L2_LINE = "PR #N is still mergeable; this run's fixes are local only."
+OFF_LINE = "Remediation is unprotected: --merge-guard off."
+WAVE0_START = "- **Wave 0 merge-guard hook"
+WAVE1_START = "- **Wave 1 (L1+):**"
+# The whole bullet is pinned: any added or changed wording, in the heading, the loading
+# sentence or the `off` sentence, is caught without a list of words to look for.
+WAVE0_HEADING = "- **Wave 0 merge-guard hook (every ordinal, both modes):**"
+WAVE0_LOADING = (
+    "on `--resume`, or when the run log already holds guard events "
+    "(`draft_guard_requested` or `draft_guard_settled`), load `refs/merge-guard.md` "
+    "(Exit report and Resume) before Wave 1 and before any edit, release or re-trigger, "
+    "and follow its Resume rows with the held cycle's `target_sha`, so a PR left held "
+    "by an earlier run is reported or released first."
+)
+WAVE0_OFF = (
+    f'At L3 with `--merge-guard off`, print "{OFF_LINE}" once and make no '
+    "draft-state call."
+)
+WAVE0_BULLET = " ".join((WAVE0_HEADING, WAVE0_LOADING, WAVE0_OFF))
+
+
+def _skill() -> str:
+    return SKILL.read_text(encoding="utf-8")
+
+
+def _wave0_problems(text: str) -> list[str]:
+    """Everything wrong with the Wave 0 guard bullet of a SKILL.md text."""
+    lines = text.splitlines()
+    starts = [i for i, line in enumerate(lines) if line.startswith(WAVE0_START)]
+    wave1 = [i for i, line in enumerate(lines) if line.startswith(WAVE1_START)]
+    if len(starts) != 1 or len(wave1) != 1:
+        return ["the Wave 0 guard bullet or the Wave 1 bullet is missing or repeated"]
+    bullet = lines[starts[0]]
+    problems = []
+    if starts[0] > wave1[0]:
+        problems.append("the bullet sits after the Wave 1 bullet")
+    for need in (
+        "`--resume`",
+        "when the run log already holds guard events",
+        "before any edit, release or re-trigger",
+        "`refs/merge-guard.md`",
+        "`target_sha`",
+        OFF_LINE,
+    ):
+        if need not in bullet:
+            problems.append(f"the bullet lacks {need!r}")
+    if bullet != WAVE0_BULLET:
+        problems.append(
+            "the bullet differs from the pinned ungated text (a gate or edit)"
+        )
+    return problems
+
+
+def test_the_wave0_bullet_is_flat_early_and_ungated():
+    assert _wave0_problems(_skill()) == []
+
+
+def test_the_pinned_wave0_text_names_no_gate():
+    """The pin itself must not be a gated bullet: strip the three parts that may name
+    an ordinal, L3 or the draft events, then scan what is left."""
+    assert "every ordinal, both modes" in WAVE0_HEADING
+    rest = WAVE0_BULLET
+    for part in (
+        WAVE0_HEADING,
+        WAVE0_OFF,
+        "draft_guard_requested",
+        "draft_guard_settled",
+    ):
+        assert rest.count(part) == 1, part
+        rest = rest.replace(part, "")
+    assert not re.search(
+        r"\bL\d\b|level|ordinal|monitor|draft|mode|only|tier", rest, re.I
+    ), rest
+
+
+def test_the_wave0_check_fails_on_each_way_the_bullet_can_go_wrong():
+    text = _skill()
+    lines = text.splitlines()
+    index = next(i for i, line in enumerate(lines) if line.startswith(WAVE0_START))
+    wave1 = next(i for i, line in enumerate(lines) if line.startswith(WAVE1_START))
+    moved = (
+        lines[:index]
+        + lines[index + 1 : wave1 + 1]
+        + [lines[index]]
+        + lines[wave1 + 1 :]
+    )
+    assert any("after the Wave 1" in p for p in _wave0_problems("\n".join(moved)))
+    off_removed = text.replace(OFF_LINE, "")
+    assert off_removed != text
+    assert any("lacks" in p for p in _wave0_problems(off_removed))
+    edits = [
+        ("(every ordinal, both modes)", "(L3 only)"),
+        ("(every ordinal, both modes)", "(draft mode)"),
+        (
+            "or when the run log already holds",
+            "at level 3, or when the run log already holds",
+        ),
+        (
+            "or when the run log already holds",
+            "at L3, or when the run log already holds",
+        ),
+        (
+            "or when the run log already holds",
+            "when the PR is a draft, or when the run log already holds",
+        ),
+        (
+            "or when the run log already holds",
+            "with --monitor 3, or when the run log already holds",
+        ),
+        (
+            "or when the run log already holds",
+            "once the PR is marked ready for review, or when the run log already holds",
+        ),
+        ("At L3 with", "At L3 in draft mode with"),
+    ]
+    for old, new in edits:
+        assert old in text, old
+        gated = text.replace(old, new, 1)
+        assert gated != text, new
+        assert any("gate" in p for p in _wave0_problems(gated)), new
+    # Every word position of the real bullet, heading and `off` sentence included: an
+    # insertion in the first words also breaks the bullet's start, which is a problem too.
+    words = WAVE0_BULLET.split(" ")
+    for i in range(len(words)):
+        for phrase in ("in draft mode", "at L3 only"):
+            mutated = " ".join(words[:i] + [phrase] + words[i:])
+            gated = text.replace(WAVE0_BULLET, mutated, 1)
+            assert gated != text, (i, phrase)
+            assert _wave0_problems(gated), (i, phrase)
+
+
+def test_the_flag_row_follows_the_conflict_flag_and_matches_the_parser():
+    from superclaude.pr_submit.fsm import build_arg_parser
+
+    rows = [line for line in _skill().splitlines() if line.startswith("| `--")]
+    names = [row.split("|")[1].strip() for row in rows]
+    assert "`--merge-guard {draft,off}`" in names
+    assert names.index("`--merge-guard {draft,off}`") == (
+        names.index("`--conflict-max-tier {0,1,2}`") + 1
+    )
+    row = rows[names.index("`--merge-guard {draft,off}`")]
+    assert "default `draft`" in row and "No effect below L3" in row
+    action = next(
+        a for a in build_arg_parser()._actions if "--merge-guard" in a.option_strings
+    )
+    assert list(action.choices) == ["draft", "off"]
+
+
+def test_the_output_row_lists_every_status_and_carries_the_l2_line_in_skill_md():
+    text = _skill()
+    rows = [line for line in text.splitlines() if line.startswith("| `merge_guard` |")]
+    assert len(rows) == 1
+    for value in ("off", "released", "held", "user_override", "unavailable"):
+        assert f"`{value}`" in rows[0], value
+    assert L2_LINE in rows[0]
+    assert L2_LINE in text
+    assert L2_LINE not in _text()
+    contract = text.index("## Output Contract")
+    assert contract < text.index(rows[0]) < text.index("## Wave / Phase Structure")
+
+
+def test_the_wave_structure_has_one_guard_line_before_wave_1():
+    fences = _skill().split("```text")[1:]
+    block = next(f for f in fences if "\nWave 0:" in f).split("```", 1)[0].splitlines()
+    guard = [i for i, line in enumerate(block) if line.startswith("Wave 0d:")]
+    wave1 = [i for i, line in enumerate(block) if line.startswith("Wave 1:")]
+    assert len(guard) == 1 and len(wave1) == 1 and guard[0] < wave1[0]
+    assert "refs/merge-guard.md" in block[guard[0]] and "--resume" in block[guard[0]]
+
+
+def test_the_new_skill_lines_name_no_gh_write_no_python_and_no_second_ref_rule():
+    text = _skill()
+    new = [
+        line
+        for line in text.splitlines()
+        if "merge-guard" in line or "merge_guard" in line
+    ]
+    assert len(new) >= 4
+    for line in new:
+        assert "gh pr" not in line and "gh api" not in line, line
+        assert "evidence-validator" not in line and "conflict-intent.md" not in line, (
+            line
+        )
+    assert text.count("```python") == 1
+    assert "src/superclaude" not in text

Delta diff from the previous reviewed tree (empty on the first review): 
Earlier blocking findings of this start (empty on the first review): F2.1 sev=blocking trigger=B1 ac=T9.AC1 at=tests/pr_submit/test_merge_guard_protocol.py:388 anchor="it names an L3 or `draft` condition" chk=y,n,n,n family=wave0-test-gate-coverage fix=in _wave0_problems run the gate scan over the whole bullet except the literal off sentence, including the bold heading (the real heading is "(every ordinal, both modes)" and holds none of the gate words), and add mutation cases for a heading of "(L3 only)" and for "at level 3" covers="The Wave 0 test fails when ... it names an L3 or `draft` condition" first=A2 origin=fix-induced: The gate scan starts after the bold heading marker, so a heading edit never reaches it; with the heading changed to "(L3 only)" or "(draft mode)", or "at level 3, " added to the loading sentence, _wave0_problems returns no problems, so the test passes a bullet that names an L3 or draft condition.
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

e36c0f9d9032a43c44139d2711447015cfc5c571
Review one task for spec compliance.

Task brief: ## Task 16: Update `state-machine.md`, `ci-poll.md` and `loop-guard.md`

Depends on: Task 2

Edit three existing refs under `src/superclaude/skills/sc-pr-submit-protocol/refs/`:

- `state-machine.md`: the wait-only sentence at `:144-146` and the new section 5.2d inserted after 5.2c, exactly as in source section 8.4 (token-free; the INV-016 blockquote at `:161-179` untouched).
- `ci-poll.md`: items 1 to 4 of source section 8.5 (the `:21` sentence, the Wave 8 entry table cells at `:28-29`, the `pr_conflicting` sentence, the new "Expected checks after a push" section).
- `loop-guard.md`: item 3 of source section 8.6 (the reserved cycle-id prefix sentence in the run-log schema section; items 1 and 2 were done in Task 2).

Acceptance criteria:
- T-N50 passes for `state-machine.md` and `loop-guard.md`; the pins at `tests/pr_submit/test_static_grep.py:746-750` pass unmodified.
- Both new `gh api` lines in `ci-poll.md` carry a `repos/<owner/repo>/` path.
- `uv run pytest tests/pr_submit/test_static_grep.py -q` passes; log saved to `./artifacts/t16-tests.log`.
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
Start sha: e36c0f9d9032a43c44139d2711447015cfc5c571
Diff against the start snapshot: diff --git a/src/superclaude/skills/sc-pr-submit-protocol/refs/state-machine.md b/src/superclaude/skills/sc-pr-submit-protocol/refs/state-machine.md
index d050b8cd..97583485 100644
--- a/src/superclaude/skills/sc-pr-submit-protocol/refs/state-machine.md
+++ b/src/superclaude/skills/sc-pr-submit-protocol/refs/state-machine.md
@@ -143,7 +143,8 @@ After the (merged) review classify would be `clean`, reaches `REPORT_ONLY`, **ex
 `max_rounds` (`HALT_MAX_ROUNDS`), **or** ends in `TERMINAL_AUGMENT_NO_RESPONSE`,
 the SKILL sets `source=ci`, resets the wait clock, and polls CI. A spent round
 budget and a silence terminal permit **waiting only**: CI findings are
-`REPORT_ONLY`, never an additional fix or push. `TERMINAL_TIMEOUT` and other
+`REPORT_ONLY`, never an additional fix or fix push. The single exception is the
+one Tier 1 sync push (5.2d), which is not a fix. `TERMINAL_TIMEOUT` and other
 halt states do not arm CI. Never send `transition(clean)` after silence. On Augment `clean` / `REPORT_ONLY`, the SKILL continues at `S2_CLASSIFY`
 **without** sending Augment `clean` to `transition()`. Once the FSM reaches
 `HALT_MAX_ROUNDS`, it stays terminal: the SKILL polls CI separately and reports
@@ -156,6 +157,29 @@ S6 / RESOLVING (the push itself re-runs checks). `transition()` is unchanged:
 `clean` still means `TERMINAL_CLEAN`, `pushed` still means `S6_REPLYING`. Only
 a non-halted CI-clean path sends `clean` to `transition()`. L0 never enters this phase.
 
+### 5.2d Conflict cycles (issue #305): Tier 1 is SKILL-owned, Tier 2 adds one edge
+
+- **Tier 1 (push kind `sync`)** runs at Wave 8 entry, before the CI wait, with no FSM edge,
+  exactly like the CI phase (5.2c): no round, no re-trigger, no reply, no resolve. It counts in
+  `sync_push_count`, never in `push_count`, and a run has at most `SYNC_CAP = 1` conflict cycle
+  (both tiers together). After `HALT_MAX_ROUNDS` or `TERMINAL_AUGMENT_NO_RESPONSE` that terminal
+  stays and the sync outcome is reported alongside it. At L2 the resolution is left validated and
+  uncommitted; the caller sets `S4'_HALT_BEFORE_PUSH` only when Wave 8 was entered from `clean` or
+  `REPORT_ONLY`.
+- **Tier 2 (push kind `merge`)** adds exactly one edge: `(S2_CLASSIFY, conflicting)` goes to
+  `HALT_MAX_ROUNDS` when the round gate fires (the same gate as `findings`), else to `S3_FIXING`
+  (L2+) or `PROPOSED` (L1) by G-edit. The cycle then follows the existing edges
+  `S3_FIXING → S7_VALIDATING → S4_PUSHING → S6_REPLYING → RESOLVING` (zero threads)
+  `→ S5a_RETRIGGER_REVIEW → S5_AWAITING_REREVIEW → S2_CLASSIFY`, and ticks `round_counter` once
+  on the INV-001 edge. The S5a re-trigger fires when `applied_edits > 0` or the push kind is `merge`.
+- A conflict push is authorized by the sibling conjunction `evaluate_sync_decision` (ordinal,
+  validated, tier allowed, under cap), never by the 5.3 conjunction, whose predicate (5) means
+  grounded finding edits. Its parent check is `merge_parent_ok`: exactly two parents, the stored
+  pre-push SHA first and the recorded base tip second.
+- **Tier 3 never enters the FSM.** At L3 it halts before arming (`terminal_halted`, reason
+  `conflict_tier3`); a Tier 3 found by a later hook takes the human-gate route to `HALT_HUMAN`, or is
+  reported alongside a preserved terminal.
+
 ## 5.3 G-push — the 5-predicate runtime conjunction (INV-016, verbatim)
 
 > **INV-016.** A push is authorized at the `S4_PUSHING` transition if and only if ALL of the
diff --git a/src/superclaude/skills/sc-pr-submit-protocol/refs/ci-poll.md b/src/superclaude/skills/sc-pr-submit-protocol/refs/ci-poll.md
index 9ad0943e..795acf95 100644
--- a/src/superclaude/skills/sc-pr-submit-protocol/refs/ci-poll.md
+++ b/src/superclaude/skills/sc-pr-submit-protocol/refs/ci-poll.md
@@ -18,17 +18,19 @@ gh pr checks <N> --repo <owner/repo> --required --json name,state,bucket,link,wo
 gh pr checks <N> --repo <owner/repo> --json name,state,bucket,link,workflow
 ```
 
-No `conclusion` field — `gh pr checks --json` does not emit it. Empty, malformed, or multiple-document stdout is **not** a parsed empty array. A valid nonempty required list takes precedence; otherwise a valid all-checks list is used. If the chosen list is empty and either query failed to parse, emit `state:polling`, `checks:[]`; only two parsed empty arrays justify `clean`. Pending exit 8 may still contain valid JSON — keep it.
+No `conclusion` field — `gh pr checks --json` does not emit it. Empty, malformed, or multiple-document stdout is **not** a parsed empty array. A valid nonempty required list takes precedence; otherwise a valid all-checks list is used. If the chosen list is empty and either query failed to parse, emit `state:polling`, `checks:[]`; only two parsed empty arrays, with `expect_checks` false, justify `clean`; with `expect_checks` true an empty chosen list is `polling` (see Expected checks after a push). Pending exit 8 may still contain valid JSON — keep it.
 
 ## Wave 8 entry (SKILL-owned, not an FSM edge)
 
 | Augment outcome | CI wait | CI fix |
 |-----------------|---------|--------|
 | `clean` / `REPORT_ONLY` | Arm; reset elapsed | Only while `round_counter < max_rounds` |
-| `HALT_MAX_ROUNDS` | Arm, wait-only; report CI clean, failure, timeout, or human-gate alongside retained Augment halt | No: CI findings → `REPORT_ONLY` |
-| `TERMINAL_AUGMENT_NO_RESPONSE` | Arm, wait-only; retain Augment status; report CI alongside. Never `transition(clean)` | No |
+| `HALT_MAX_ROUNDS` | Arm, wait-only; report CI clean, failure, timeout, or human-gate alongside retained Augment halt | No: CI findings → `REPORT_ONLY` (the one Tier 1 sync push of Wave 8a is the only push allowed here, and it is not a fix) |
+| `TERMINAL_AUGMENT_NO_RESPONSE` | Arm, wait-only; retain Augment status; report CI alongside. Never `transition(clean)` | No (the one Tier 1 sync push excepted) |
 | `HALT_HUMAN` / `VALIDATION_FAIL` / `TERMINAL_TIMEOUT` / `TERMINAL_FAILED` / L0 | Do not arm | No |
 
+When the PR is still conflicting and no merge commit was pushed, the SKILL skips the CI wait with reason `pr_conflicting`: GitHub runs no `pull_request` checks on a conflicting PR, so the lists would read empty.
+
 The wait consumes no remediation round. A `polling` result (including a failed check query) continues at the configured interval until completion or `--timeout`. A non-zero script exit (e.g. `gh` without `pr checks --json`) is not `polling`: stop and report the missing prerequisite. The observed CI matrix has run longer than the 600s default, so a CI wait needs a `--timeout` sized to the full check run; never promise an indefinite wait. When `--required` returns a nonempty parsed list it is the chosen set; otherwise use the parsed all-checks list. Optional checks outside the chosen set do not block completion.
 
 - `headRefOid` = the head SHA. If it differs from the SHA this wait started on,
@@ -47,6 +49,25 @@ gh run view <RUN_ID> --repo <owner/repo> --log-failed
 `RUN_ID` parsed from `checks[].link` (`/actions/runs/(\d+)`). Missing link →
 unparseable (no Finding; SKILL `REPORT_ONLY`).
 
+## Expected checks after a push (`expect_checks`)
+
+Right after a push the new head has no checks yet, so an empty list must not read as `clean`
+when the repository has checks. The SKILL sets `expect_checks` once per push with
+`superclaude.pr_submit.ci.expect_checks_after_push` and records it on the push records, so
+`--resume` reuses it. Evidence for the replaced head and the base tip is commit-scoped:
+
+```bash
+scripts/poll-ci-checks.sh --evidence-sha <sha> --repo <owner/repo>
+gh api repos/<owner/repo>/commits/<sha>/check-runs --jq .total_count
+gh api repos/<owner/repo>/commits/<sha>/status --jq .total_count
+```
+
+The script runs the two reads and prints `{"evidence_sha": "<sha>", "evidence_checks": <n>, "source": "ci"}`,
+with `n = -1` on a failed or unparsable read. `-1` counts as having checks (fail closed). Only when
+checks were not seen earlier in the run and both evidence reads are 0 is an empty list `clean`. With
+`expect_checks` true, expiry is the existing Wave 8 CI timeout with reason `ci_not_started`; it is
+never `clean` and the report never says tests passed.
+
 ## Division of labour
 
 - The **poll script** does one poll and returns a coarse `state` plus the raw
diff --git a/src/superclaude/skills/sc-pr-submit-protocol/refs/loop-guard.md b/src/superclaude/skills/sc-pr-submit-protocol/refs/loop-guard.md
index 8d5759d8..ddf845e9 100644
--- a/src/superclaude/skills/sc-pr-submit-protocol/refs/loop-guard.md
+++ b/src/superclaude/skills/sc-pr-submit-protocol/refs/loop-guard.md
@@ -116,6 +116,9 @@ complete by `--timeout` while the other reviewer's result was used. `rereview_re
 `{cycle_id, reviewer, timestamp}`, `timestamp` being the UTC time taken right after that reviewer's
 successful re-trigger POST.
 
+The `cycle_id` prefixes `sync-` and `conflict-` are reserved for conflict cycles (Tier 1 and Tier 2);
+a fix cycle's `cycle_id` never starts with either.
+
 **Folds.** `rebuild_state()` folds `rereview_requested` into `rereview_request_count` by **distinct
 `cycle_id`**: one push cycle counts once however many reviewers were re-triggered in it (an event
 without `cycle_id` still counts once each, so older logs rebuild to the same number). It folds
diff --git a/.dev/tasks/to-do/TASK-WF-design-20261104-164423/artifacts/t16-usage-match.txt b/.dev/tasks/to-do/TASK-WF-design-20261104-164423/artifacts/t16-usage-match.txt
new file mode 100644
index 00000000..8bf12677
--- /dev/null
+++ b/.dev/tasks/to-do/TASK-WF-design-20261104-164423/artifacts/t16-usage-match.txt
@@ -0,0 +1,12 @@
+== script header usage (poll-ci-checks.sh:6-7) ==
+6:# Usage   : poll-ci-checks.sh --pr <N> [--repo <owner/repo>]
+7:#           poll-ci-checks.sh --evidence-sha <40hex> [--repo <owner/repo>]
+== ci-poll.md fenced usage line ==
+60:scripts/poll-ci-checks.sh --evidence-sha <sha> --repo <owner/repo>
+== function exists in ci.py ==
+63:def expect_checks_after_push(
+== function named in ci-poll.md ==
+56:`superclaude.pr_submit.ci.expect_checks_after_push` and records it on the push records, so
+== flag tokens: header vs ref ==
+--evidence-sha header=1 ref=1
+--repo header=3 ref=1
diff --git a/.dev/tasks/to-do/TASK-WF-design-20261104-164423/artifacts/t16-grep.txt b/.dev/tasks/to-do/TASK-WF-design-20261104-164423/artifacts/t16-grep.txt
new file mode 100644
index 00000000..2bd43572
--- /dev/null
+++ b/.dev/tasks/to-do/TASK-WF-design-20261104-164423/artifacts/t16-grep.txt
@@ -0,0 +1,13 @@
+== new gh api lines in ci-poll.md (must carry repos/<owner/repo>/) ==
+61:gh api repos/<owner/repo>/commits/<sha>/check-runs --jq .total_count
+62:gh api repos/<owner/repo>/commits/<sha>/status --jq .total_count
+== gh api lines lacking repos/ path (expect none) ==
+NONE
+== T-N50 tokens in state-machine.md / loop-guard.md (expect none) ==
+NONE
+== force flags in the three refs (expect none) ==
+NONE
+== src/superclaude/ text in the three refs (expect none) ==
+NONE
+== INV-016 blockquote unchanged vs HEAD (diff of '> ' lines) ==
+IDENTICAL
diff --git a/.dev/tasks/to-do/TASK-WF-design-20261104-164423/artifacts/t16-tests.log b/.dev/tasks/to-do/TASK-WF-design-20261104-164423/artifacts/t16-tests.log
new file mode 100644
index 00000000..9b0308d1
--- /dev/null
+++ b/.dev/tasks/to-do/TASK-WF-design-20261104-164423/artifacts/t16-tests.log
@@ -0,0 +1,12 @@
+============================= test session starts ==============================
+platform linux -- Python 3.11.15, pytest-9.2.0, pluggy-1.7.0
+SuperClaude: 5.0.0
+benchmark: 5.3.1 (defaults: timer=time.perf_counter disable_gc=False min_rounds=5 min_time=0.000005 max_time=1.0 calibration_precision=10 warmup=False warmup_iterations=100000)
+rootdir: /home/coder/workspaces/worktrees/IronClaude/issue-305-pr-submit-conflicts
+configfile: pyproject.toml
+plugins: superclaude-5.0.0, benchmark-5.3.1, anyio-4.16.0, cov-7.1.0
+collected 19 items
+
+tests/pr_submit/test_static_grep.py ...................                  [100%]
+
+============================== 19 passed in 0.56s ==============================

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

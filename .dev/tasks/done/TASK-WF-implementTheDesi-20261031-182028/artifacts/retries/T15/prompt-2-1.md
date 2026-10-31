9d629c150674a2aba78663fa88d1e5037c5e783e
Review one task for spec compliance.

Task brief: ## Task 15: Update the user-facing docs and the changelog

Depends on: Task 14

Edit only the sentences that state Augment-only pr-submit behaviour: CLAUDE.md (the mandatory-way paragraph: waits for the Augment and Codex reviews), docs/user-guide/commands.md (the /sc:pr-submit "When to use" paragraph), docs/guides/tdd-skill-release-guide.md and docs/guides/prd-skill-release-guide.md (needs the Augment Code or Codex review app). Add an Unreleased entry to CHANGELOG.md describing Codex support, the fail-open reviewer detection, the P0-P3 mapping, dedup, per-reviewer re-trigger and the UNVERIFIED re-review marker update. Run make lint and the named pytest set.

Acceptance criteria:
- `grep -n "the Augment review" CLAUDE.md docs/user-guide/commands.md` returns no pr-submit sentence that omits Codex.
- make lint passes; `uv run pytest tests/pr_submit tests/skills/test_primitive_dual_surface_lookup.py tests/unit/test_cli_install.py tests/core/test_how_we_work_routing_table.py -q -p no:cacheprovider` passes with output saved to ./artifacts/t15-pytest.log.
Global constraints: 
- The design file .dev/pr-submit-codex/design/pr-submit-codex-design.md is the specification; do not add behaviour it does not describe.
- Keep the deterministic core src/superclaude/pr_submit/ free of gh and git command tokens (NFR-6, checked by tests/pr_submit/test_static_grep.py).
- Augment-only behaviour must stay identical apart from the added reviewer_absent event and reviewer fields (design sections 5 and 6); existing tests in tests/pr_submit/ keep passing.
- Never hardcode src/superclaude/ paths inside installed primitives (command, skill, refs, scripts); keep script file names unchanged.
- plugins/superclaude/ has no pr-submit twin (design section 3), so no mirror edit is needed; do not create one.
- Edit src/superclaude/ only, then run make sync-dev; never edit or stage .claude/ copies.
- Run pytest only on named files or tests/pr_submit, never the full suite or tests/cli/eval/ as a directory; use uv run.
- .dev/tasks/ is always staged (git add .dev/tasks), including this package and its artifacts/.
Start sha: 9d629c150674a2aba78663fa88d1e5037c5e783e
Diff against the start snapshot: diff --git a/CLAUDE.md b/CLAUDE.md
index 62fb39b6..2602d66f 100644
--- a/CLAUDE.md
+++ b/CLAUDE.md
@@ -47,7 +47,7 @@ This repository is a **fork**. `origin` = `IronbellyOrg/IronClaude` (the user's
 - Push to `upstream` (the `upstream` remote name above). The `origin` remote is the correct push target.
 - Assume the upstream is the right target because gh's interactive flow suggests it. The interactive flow is the trap.
 
-**The mandatory way to open a PR:** always use `/sc:pr-submit --monitor 3`. It opens the PR with `gh pr create --repo <repo>`, where `<repo>` comes from the `origin` remote, then waits for the Augment review, fixes the confirmed findings of Medium severity or higher (lower ones are only reported) and failing CI checks, pushes the fixes without asking, and replies to and resolves the review comments it fixed. Run it in Claude Code (it is a slash command, not a shell command):
+**The mandatory way to open a PR:** always use `/sc:pr-submit --monitor 3`. It opens the PR with `gh pr create --repo <repo>`, where `<repo>` comes from the `origin` remote, then waits for the Augment and Codex reviews (each one that is installed on the repository), fixes the confirmed findings of Medium severity or higher (lower ones are only reported) and failing CI checks, pushes the fixes without asking, and replies to and resolves the review comments it fixed. Run it in Claude Code (it is a slash command, not a shell command):
 
 ```text
 /sc:pr-submit --monitor 3 --head <branch> --title "..." --body "..."
diff --git a/docs/user-guide/commands.md b/docs/user-guide/commands.md
index ea8f3d5a..95e3eed6 100644
--- a/docs/user-guide/commands.md
+++ b/docs/user-guide/commands.md
@@ -358,7 +358,7 @@ PM Agent:
 
 ### `/sc:pr-submit` - PR Review Auto-Remediation Monitor
 
-**When to use:** Open a PR on the fork and, at `--monitor 1` or higher, arm an in-session monitor that polls for the Augment review, verifies findings, and sends verified ones to `/sc:troubleshoot`; higher levels also fix, push, reply and resolve. With no `--monitor` it runs level 3. `--monitor 0` only opens the PR; it never pushes to an upstream parent or to a protected branch.
+**When to use:** Open a PR on the fork and, at `--monitor 1` or higher, arm an in-session monitor that polls for the Augment and Codex reviews (a reviewer that never shows activity on the PR is skipped), verifies findings, and sends verified ones to `/sc:troubleshoot`; higher levels also fix, push, reply and resolve. With no `--monitor` it runs level 3. `--monitor 0` only opens the PR; it never pushes to an upstream parent or to a protected branch.
 
 **Syntax:**
 
diff --git a/docs/guides/tdd-skill-release-guide.md b/docs/guides/tdd-skill-release-guide.md
index 8f99dce0..90ec1d28 100644
--- a/docs/guides/tdd-skill-release-guide.md
+++ b/docs/guides/tdd-skill-release-guide.md
@@ -557,7 +557,7 @@ Give that one commit, not a `..HEAD` range: a single commit is compared with you
 /sc:pr-submit --monitor 3 --head <branch> --title "<title>" --body "<body>"
 ```
 
-Commit locally first. Run `/security-review` only if login, permissions, secrets, user input, or file paths changed. Push only after your lead approves, then run `/sc:pr-submit`. It fixes the confirmed review findings of Medium severity or higher and failing CI checks, and pushes those fixes to your branch without asking (use `--monitor 2` to stop before pushing). It needs `gh` logged in and the Augment Code review app on the repository; without the app use `--monitor 0`, which only opens the PR. Full steps: section 3.11 of [`HOW-WE-WORK.md`](../../src/superclaude/core/HOW-WE-WORK.md) (installed as `~/.claude/HOW-WE-WORK.md`); the whole pipeline above is its workflow 3.1.
+Commit locally first. Run `/security-review` only if login, permissions, secrets, user input, or file paths changed. Push only after your lead approves, then run `/sc:pr-submit`. It fixes the confirmed review findings of Medium severity or higher and failing CI checks, and pushes those fixes to your branch without asking (use `--monitor 2` to stop before pushing). It needs `gh` logged in and the Augment Code review app or the Codex review connector on the repository; without either use `--monitor 0`, which only opens the PR. Full steps: section 3.11 of [`HOW-WE-WORK.md`](../../src/superclaude/core/HOW-WE-WORK.md) (installed as `~/.claude/HOW-WE-WORK.md`); the whole pipeline above is its workflow 3.1.
 
 The CLI pipeline (`superclaude roadmap run` -> `/sc:tasklist` -> `superclaude sprint run`) is a separate release pipeline; see [roadmap-cli-tools-release-guide.md](roadmap-cli-tools-release-guide.md). For which tool to use when, see [How We Work](../user-guide/how-we-work.md).
 
diff --git a/docs/guides/prd-skill-release-guide.md b/docs/guides/prd-skill-release-guide.md
index 0305a3b0..6178d015 100644
--- a/docs/guides/prd-skill-release-guide.md
+++ b/docs/guides/prd-skill-release-guide.md
@@ -535,7 +535,7 @@ Give that one commit, not a `..HEAD` range: a single commit is compared with you
 /sc:pr-submit --monitor 3 --head <branch> --title "<title>" --body "<body>"
 ```
 
-Commit locally first. Run `/security-review` only if login, permissions, secrets, user input, or file paths changed. Push only after your lead approves, then run `/sc:pr-submit`. It fixes the confirmed review findings of Medium severity or higher and failing CI checks, and pushes those fixes to your branch without asking (use `--monitor 2` to stop before pushing). It needs `gh` logged in and the Augment Code review app on the repository; without the app use `--monitor 0`, which only opens the PR. Full steps: section 3.11 of [`HOW-WE-WORK.md`](../../src/superclaude/core/HOW-WE-WORK.md) (installed as `~/.claude/HOW-WE-WORK.md`); the whole pipeline above is its workflow 3.1.
+Commit locally first. Run `/security-review` only if login, permissions, secrets, user input, or file paths changed. Push only after your lead approves, then run `/sc:pr-submit`. It fixes the confirmed review findings of Medium severity or higher and failing CI checks, and pushes those fixes to your branch without asking (use `--monitor 2` to stop before pushing). It needs `gh` logged in and the Augment Code review app or the Codex review connector on the repository; without either use `--monitor 0`, which only opens the PR. Full steps: section 3.11 of [`HOW-WE-WORK.md`](../../src/superclaude/core/HOW-WE-WORK.md) (installed as `~/.claude/HOW-WE-WORK.md`); the whole pipeline above is its workflow 3.1.
 
 The CLI pipeline (`superclaude roadmap run` -> `/sc:tasklist` -> `superclaude sprint run`) is a separate release pipeline; see [roadmap-cli-tools-release-guide.md](roadmap-cli-tools-release-guide.md). For which tool to use when, see [How We Work](../user-guide/how-we-work.md).
 
diff --git a/CHANGELOG.md b/CHANGELOG.md
index 77fb89c8..1397cc00 100644
--- a/CHANGELOG.md
+++ b/CHANGELOG.md
@@ -4,6 +4,19 @@ All notable changes to IronClaude are documented in this file.
 
 ## [Unreleased]
 
+### /sc:pr-submit: Codex reviews handled like Augment reviews
+
+#### Added (pr-submit Codex)
+
+- `/sc:pr-submit` now handles the review threads of the Codex connector (`chatgpt-codex-connector[bot]`) the same way as Augment's: one poll snapshot serves both reviewers; Codex findings are re-graded, verified, sent to `/sc:troubleshoot`, fixed, pushed, replied to and resolved through the same path, in the same single fix commit per cycle.
+- Codex completion is read from the `codex-review-state:v1` marker in its summary comment (completed, on the expected head, newer than the re-trigger watermark); anything unproven stays polling, never a false clean.
+- Codex priority badges map onto the existing severity routing as a severity hint: P0 critical and P1 high (`--depth deep --fix`), P2 medium (`--fix`), P3 low (report-only); a missing or malformed badge uses the Medium fallback.
+- Fail-open reviewer detection: a reviewer with no activity on the PR is recorded absent (`reviewer_absent`) and ignored, so Augment-only and Codex-only repositories work unchanged; when a present reviewer never completes but the other reviewer does, the other reviewer's result is used and the incomplete one is recorded `reviewer_incomplete`; if no reviewer completes and at least one showed activity, the run ends `terminal_timeout` as before. `terminal_augment_no_response` now means no configured reviewer responded.
+- Findings of both reviewers on the same path and line form one dedup group: routed at the highest tier, diagnosed and fixed once, with every verified thread replied to and resolved.
+- After a push, one re-trigger comment per present reviewer (`auggie review`, `@codex review`), each with its own watermark and a `rereview_requested{cycle_id, reviewer, timestamp}` event appended right after its successful post; before posting, and again on resume, `pending_retriggers` picks only the reviewers with no such event for the cycle, so a crash between the two posts does not skip the second reviewer. `rereview_request_count` now counts re-triggered cycles.
+- The detection contract gains `codex_bot_login`, `codex_app_slug` and `codex_retrigger_phrase`; an override that omits them keeps the shipped values, and blanking both Codex identities disables Codex. The output contract gains `reviewers`, and the run log two event types (41 in all).
+- UNVERIFIED: whether Codex updates its summary marker for the new commit after `@codex review` has not been observed yet; if it does not, the Codex re-review ends incomplete at `--timeout` and the other reviewer's result is used when there is one (fail open).
+
 ### ccsession: one session name for ccsession, Claude Code and Orca (#325)
 
 #### Added (ccsession one name)
diff --git a/.dev/tasks/to-do/TASK-WF-implementTheDesi-20261031-182028/artifacts/t15-lint.log b/.dev/tasks/to-do/TASK-WF-implementTheDesi-20261031-182028/artifacts/t15-lint.log
new file mode 100644
index 00000000..8f0c1196
--- /dev/null
+++ b/.dev/tasks/to-do/TASK-WF-implementTheDesi-20261031-182028/artifacts/t15-lint.log
@@ -0,0 +1,146 @@
+🔍 Checking architecture policy compliance...
+
+=== Check 1/2: Bidirectional Command ↔ Skill Links ===
+  ✅ [Check 1]: adversarial → sc-adversarial-protocol
+  ✅ [Check 1]: auggie-review → sc-auggie-review-protocol
+  ✅ [Check 1]: brainstorm → sc-brainstorm-protocol
+  ✅ [Check 1]: cleanup-audit → sc-cleanup-audit-protocol
+  ✅ [Check 1]: cli-eval → sc-cli-eval-protocol
+  ✅ [Check 1]: cli-portify → sc-cli-portify-protocol
+  ✅ [Check 1]: implement → sc-implement-protocol
+  ✅ [Check 1]: init-lite → sc-init-lite-protocol
+  ✅ [Check 1]: pm → sc-pm-protocol
+  ✅ [Check 1]: post-release → sc-post-release-protocol
+  ✅ [Check 1]: pr-submit → sc-pr-submit-protocol
+  ✅ [Check 1]: recommend → sc-recommend (utility skill; no -protocol suffix)
+  ✅ [Check 1]: reflect → sc-reflect-protocol
+  ✅ [Check 1]: release-split → sc-release-split-protocol
+  ✅ [Check 1]: review-translation → sc-review-translation-protocol
+  ✅ [Check 1]: roadmap → sc-roadmap-protocol
+  ✅ [Check 1]: swarm-wizard → sc-swarm-wizard-protocol
+  ✅ [Check 1]: task → sc-task-protocol
+  ✅ [Check 1]: tasklist → sc-tasklist-protocol
+  ✅ [Check 1]: troubleshoot → sc-troubleshoot-protocol
+  ✅ [Check 1]: validate-roadmap → sc-validate-roadmap-protocol
+  ✅ [Check 1]: validate-tests → sc-validate-tests-protocol
+  ✅ [Check 1]: workflow → sc-workflow-protocol
+  ✅ [Check 2]: sc-adversarial-protocol ← adversarial.md
+  ✅ [Check 2]: sc-auggie-review-protocol ← auggie-review.md
+  ✅ [Check 2]: sc-brainstorm-protocol ← brainstorm.md
+  ✅ [Check 2]: sc-cleanup-audit-protocol ← cleanup-audit.md
+  ✅ [Check 2]: sc-cli-eval-protocol ← cli-eval.md
+  ✅ [Check 2]: sc-cli-portify-protocol ← cli-portify.md
+  ✅ [Check 2]: sc-implement-protocol ← implement.md
+  ✅ [Check 2]: sc-init-lite-protocol ← init-lite.md
+  ✅ [Check 2]: sc-pm-protocol ← pm.md
+  ✅ [Check 2]: sc-post-release-protocol ← post-release.md
+  ✅ [Check 2]: sc-pr-submit-protocol ← pr-submit.md
+  ✅ [Check 2]: sc-reflect-protocol ← reflect.md
+  ✅ [Check 2]: sc-release-split-protocol ← release-split.md
+  ✅ [Check 2]: sc-review-translation-protocol ← review-translation.md
+  ✅ [Check 2]: sc-roadmap-protocol ← roadmap.md
+  ✅ [Check 2]: sc-swarm-wizard-protocol ← swarm-wizard.md
+  ✅ [Check 2]: sc-task-protocol ← task.md
+  ✅ [Check 2]: sc-tasklist-protocol ← tasklist.md
+  ✅ [Check 2]: sc-troubleshoot-protocol ← troubleshoot.md
+  ✅ [Check 2]: sc-validate-roadmap-protocol ← validate-roadmap.md
+  ✅ [Check 2]: sc-validate-tests-protocol ← validate-tests.md
+  ✅ [Check 2]: sc-workflow-protocol ← workflow.md
+
+=== Check 3/4: Command Size Limits ===
+  ⚠️  WARN [Check 3]: brainstorm.md (201 lines, warn threshold 200)
+  ⚠️  WARN [Check 3]: reflect.md (303 lines, warn threshold 200)
+  ⚠️  WARN [Check 3]: spawn.md (210 lines, warn threshold 200)
+  ⚠️  WARN [Check 3]: spec-panel.md (462 lines, warn threshold 200)
+  ⚠️  WARN [Check 3]: troubleshoot.md (213 lines, warn threshold 200)
+
+=== Check 6: Activation Section Present (for paired commands) ===
+  ✅ [Check 6]: adversarial.md has ## Activation
+  ✅ [Check 6]: auggie-review.md has ## Activation
+  ✅ [Check 6]: brainstorm.md has ## Activation
+  ✅ [Check 6]: cleanup-audit.md has ## Activation
+  ✅ [Check 6]: cli-eval.md has ## Activation
+  ✅ [Check 6]: cli-portify.md has ## Activation
+  ✅ [Check 6]: implement.md has ## Activation
+  ✅ [Check 6]: init-lite.md has ## Activation
+  ✅ [Check 6]: pm.md has ## Activation
+  ✅ [Check 6]: post-release.md has ## Activation
+  ✅ [Check 6]: pr-submit.md has ## Activation
+  ✅ [Check 6]: reflect.md has ## Activation
+  ✅ [Check 6]: release-split.md has ## Activation
+  ✅ [Check 6]: review-translation.md has ## Activation
+  ✅ [Check 6]: roadmap.md has ## Activation
+  ✅ [Check 6]: swarm-wizard.md has ## Activation
+  ✅ [Check 6]: task.md has ## Activation
+  ✅ [Check 6]: tasklist.md has ## Activation
+  ✅ [Check 6]: troubleshoot.md has ## Activation
+  ✅ [Check 6]: validate-roadmap.md has ## Activation
+  ✅ [Check 6]: validate-tests.md has ## Activation
+  ✅ [Check 6]: workflow.md has ## Activation
+
+=== Check 8: Skill Frontmatter Completeness ===
+  ✅ [Check 8]: sc-adversarial-protocol frontmatter complete
+  ✅ [Check 8]: sc-auggie-review-protocol frontmatter complete
+  ✅ [Check 8]: sc-brainstorm-protocol frontmatter complete
+  ✅ [Check 8]: sc-cleanup-audit-protocol frontmatter complete
+  ✅ [Check 8]: sc-cli-eval-protocol frontmatter complete
+  ✅ [Check 8]: sc-cli-portify-protocol frontmatter complete
+  ✅ [Check 8]: sc-implement-protocol frontmatter complete
+  ✅ [Check 8]: sc-init-lite-protocol frontmatter complete
+  ✅ [Check 8]: sc-pm-protocol frontmatter complete
+  ✅ [Check 8]: sc-post-release-protocol frontmatter complete
+  ✅ [Check 8]: sc-pr-submit-protocol frontmatter complete
+  ✅ [Check 8]: sc-reflect-protocol frontmatter complete
+  ✅ [Check 8]: sc-release-split-protocol frontmatter complete
+  ✅ [Check 8]: sc-review-translation-protocol frontmatter complete
+  ✅ [Check 8]: sc-roadmap-protocol frontmatter complete
+  ✅ [Check 8]: sc-swarm-wizard-protocol frontmatter complete
+  ✅ [Check 8]: sc-task-protocol frontmatter complete
+  ✅ [Check 8]: sc-tasklist-protocol frontmatter complete
+  ✅ [Check 8]: sc-troubleshoot-protocol frontmatter complete
+  ✅ [Check 8]: sc-validate-roadmap-protocol frontmatter complete
+  ✅ [Check 8]: sc-validate-tests-protocol frontmatter complete
+  ✅ [Check 8]: sc-workflow-protocol frontmatter complete
+
+=== Check 9: Protocol Naming Consistency ===
+  ✅ [Check 9]: sc:adversarial-protocol ends in -protocol
+  ✅ [Check 9]: sc:auggie-review-protocol ends in -protocol
+  ✅ [Check 9]: sc:brainstorm-protocol ends in -protocol
+  ✅ [Check 9]: sc:cleanup-audit-protocol ends in -protocol
+  ✅ [Check 9]: sc:cli-eval-protocol ends in -protocol
+  ✅ [Check 9]: sc-cli-portify-protocol ends in -protocol
+  ✅ [Check 9]: sc:implement-protocol ends in -protocol
+  ✅ [Check 9]: sc:init-lite-protocol ends in -protocol
+  ✅ [Check 9]: sc:pm-protocol ends in -protocol
+  ✅ [Check 9]: sc:post-release-protocol ends in -protocol
+  ✅ [Check 9]: sc:pr-submit-protocol ends in -protocol
+  ✅ [Check 9]: sc:reflect-protocol ends in -protocol
+  ✅ [Check 9]: sc:release-split-protocol ends in -protocol
+  ✅ [Check 9]: sc:review-translation-protocol ends in -protocol
+  ✅ [Check 9]: sc:roadmap-protocol ends in -protocol
+  ✅ [Check 9]: sc:swarm-wizard-protocol ends in -protocol
+  ✅ [Check 9]: sc:task-protocol ends in -protocol
+  ✅ [Check 9]: sc:tasklist-protocol ends in -protocol
+  ✅ [Check 9]: sc:troubleshoot-protocol ends in -protocol
+  ✅ [Check 9]: sc-validate-roadmap-protocol ends in -protocol
+  ✅ [Check 9]: sc:validate-tests-protocol ends in -protocol
+  ✅ [Check 9]: sc:workflow-protocol ends in -protocol
+
+=== Check 10: Workspace Suffix Blocklist ===
+  ✅ [Check 10]: no *-workspace directories under .claude/skills/
+
+=== Check 11: Contract Constant Anti-Duplication (Contract #5 + #8) ===
+  ✅ [Check 11]: no contract-constant duplications
+
+=== Checks 5/7: NEEDS DESIGN (skipped) ===
+  ℹ️  Check 5 (inline protocol detection) — pending design
+  ℹ️  Check 7 (activation references correct skill) — pending design
+
+=== Summary ===
+  Errors:   0
+  Warnings: 5
+  ✅ PASS — architecture policy compliant (5 warning(s))
+Running linter...
+uv run ruff check .
+All checks passed!
+make lint rc=0
diff --git a/.dev/tasks/to-do/TASK-WF-implementTheDesi-20261031-182028/artifacts/t15-pytest.log b/.dev/tasks/to-do/TASK-WF-implementTheDesi-20261031-182028/artifacts/t15-pytest.log
new file mode 100644
index 00000000..2919fb0b
--- /dev/null
+++ b/.dev/tasks/to-do/TASK-WF-implementTheDesi-20261031-182028/artifacts/t15-pytest.log
@@ -0,0 +1,61 @@
+============================= test session starts ==============================
+platform linux -- Python 3.11.15, pytest-9.2.0, pluggy-1.7.0
+SuperClaude: 4.3.5
+benchmark: 5.3.0 (defaults: timer=time.perf_counter disable_gc=False min_rounds=5 min_time=0.000005 max_time=1.0 calibration_precision=10 warmup=False warmup_iterations=100000)
+rootdir: /home/coder/workspaces/IronClaude/.dev/worktrees/pr-submit-codex
+configfile: pyproject.toml
+plugins: superclaude-4.3.5, benchmark-5.3.0, anyio-4.15.1, cov-7.1.0
+collected 883 items
+
+tests/pr_submit/test_auggie_fallback.py ............                     [  1%]
+tests/pr_submit/test_augment_review_remediation.py .......               [  2%]
+tests/pr_submit/test_autonomy_gates.py .......                           [  2%]
+tests/pr_submit/test_ci_classify.py ....................                 [  5%]
+tests/pr_submit/test_codex_reviews.py .................................. [  9%]
+........................                                                 [ 11%]
+tests/pr_submit/test_contract_setup_diagnosis.py ..............          [ 13%]
+tests/pr_submit/test_contract_setup_evidence.py .....................    [ 15%]
+tests/pr_submit/test_contract_setup_pr_submit_integration.py ......      [ 16%]
+tests/pr_submit/test_contract_setup_questions.py .........               [ 17%]
+tests/pr_submit/test_contract_setup_validation.py .............          [ 18%]
+tests/pr_submit/test_contract_setup_writer.py ................           [ 20%]
+tests/pr_submit/test_cosmos_poll.py .................................... [ 24%]
+...............................................................          [ 31%]
+tests/pr_submit/test_cosmos_protocol.py ...............                  [ 33%]
+tests/pr_submit/test_cosmos_review.py .................................. [ 37%]
+........................................................................ [ 45%]
+                                                                         [ 45%]
+tests/pr_submit/test_crash_recovery.py ................                  [ 47%]
+tests/pr_submit/test_detection_contract.py ............................. [ 50%]
+.....                                                                    [ 51%]
+tests/pr_submit/test_edge_cases.py ...................                   [ 53%]
+tests/pr_submit/test_finding_verify.py ...                               [ 53%]
+tests/pr_submit/test_gate_helper_coverage.py ...........                 [ 55%]
+tests/pr_submit/test_gate_helper_differentials.py ...................... [ 57%]
+                                                                         [ 57%]
+tests/pr_submit/test_idempotency.py ......                               [ 58%]
+tests/pr_submit/test_loop_guard.py .............                         [ 59%]
+tests/pr_submit/test_monitor_arm.py ...                                  [ 60%]
+tests/pr_submit/test_pre_pr_checks.py .................................. [ 63%]
+.....                                                                    [ 64%]
+tests/pr_submit/test_rate_limit.py ....                                  [ 64%]
+tests/pr_submit/test_reply_resolve.py ..........                         [ 66%]
+tests/pr_submit/test_review_retrigger.py .......                         [ 66%]
+tests/pr_submit/test_run_log.py ............                             [ 68%]
+tests/pr_submit/test_setup_questions_resolution.py ....                  [ 68%]
+tests/pr_submit/test_severity_router.py ............................     [ 71%]
+tests/pr_submit/test_silence.py .................                        [ 73%]
+tests/pr_submit/test_skill_parse.py ..............                       [ 75%]
+tests/pr_submit/test_static_grep.py ...................                  [ 77%]
+tests/pr_submit/test_timeout.py .....                                    [ 78%]
+tests/pr_submit/test_troubleshoot_seed.py ....                           [ 78%]
+tests/pr_submit/test_validated_not_verified.py ...                       [ 78%]
+tests/pr_submit/test_validation_gate.py .........                        [ 79%]
+tests/skills/test_primitive_dual_surface_lookup.py ...                   [ 80%]
+tests/unit/test_cli_install.py ......................................... [ 84%]
+.......................................................                  [ 91%]
+tests/core/test_how_we_work_routing_table.py ........................... [ 94%]
+....................................................                     [100%]
+
+============================= 883 passed in 15.49s =============================
+rc=0
diff --git a/.dev/tasks/to-do/TASK-WF-implementTheDesi-20261031-182028/artifacts/t15-grep.log b/.dev/tasks/to-do/TASK-WF-implementTheDesi-20261031-182028/artifacts/t15-grep.log
new file mode 100644
index 00000000..72b0e145
--- /dev/null
+++ b/.dev/tasks/to-do/TASK-WF-implementTheDesi-20261031-182028/artifacts/t15-grep.log
@@ -0,0 +1,6 @@
+$ grep -n "the Augment review" CLAUDE.md docs/user-guide/commands.md
+rc=1
+$ grep -n -i "augment" (pr-submit sentences)
+CLAUDE.md:50:**The mandatory way to open a PR:** always use `/sc:pr-submit --monitor 3`. It opens the PR with `gh pr create --repo <repo>`, where `<repo>` comes from the `origin` remote, then waits for the Augment and Codex reviews (each on
+docs/guides/tdd-skill-release-guide.md:560:Commit locally first. Run `/security-review` only if login, permissions, secrets, user input, or file paths changed. Push only after your lead approves, then run `/sc:pr-submit`. It fixes the confi
+docs/guides/prd-skill-release-guide.md:538:Commit locally first. Run `/security-review` only if login, permissions, secrets, user input, or file paths changed. Push only after your lead approves, then run `/sc:pr-submit`. It fixes the confi
Delta diff from the previous reviewed tree (empty on the first review): Fix pass for F1.1 and F1.2 in CHANGELOG.md: line 14 now says the other reviewer's result is used only when it completes, and that the run ends terminal_timeout when no reviewer completes and at least one showed activity; line 16 now says rereview_requested is appended right after each successful post, with pending_retriggers choosing the reviewers to post before posting and on resume (only skipping is prevented). Logs regenerated.
Earlier blocking findings of this start (empty on the first review): F1.1 at=CHANGELOG.md:14 family=changelog-incomplete-case: unqualified 'a present reviewer that never completes is recorded reviewer_incomplete and the other reviewer's result is used' | F1.2 at=CHANGELOG.md:16 family=changelog-write-ahead-misnomer: 'write-ahead rereview_requested' contradicts SKILL.md:274 (appended right after the successful POST)
Saved-probe re-check hit locations (may be empty): 14:- Fail-open reviewer detection: a reviewer with no activity on the PR is recorded absent (`reviewer_absent`) and ignored, so Augment-only and Codex-only repositories work unchanged; when a present ;18:- UNVERIFIED: whether Codex updates its summary marker for the new commit after `@codex review` has not been observed yet; if it does not, the Codex re-review ends incomplete at `--timeout` and the;260:- `--resume <task_id>` flag on `superclaude sprint run`: resumes a per-task sprint by skipping *validated-successful* tasks (handoff record with `status == "pass"` AND a successful gate outcome). ;

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

pick: advice-3-a.md; runner-up: advice-3-b.md; reason: tie, -a
## Task 15: Update the user-facing docs and the changelog
Acceptance criteria:
- `grep -n "the Augment review" CLAUDE.md docs/user-guide/commands.md` returns no pr-submit sentence that omits Codex.
- make lint passes; `uv run pytest tests/pr_submit tests/skills/test_primitive_dual_surface_lookup.py tests/unit/test_cli_install.py tests/core/test_how_we_work_routing_table.py -q -p no:cacheprovider` passes with output saved to ./artifacts/t15-pytest.log.
Steps:
1. Start from the Q0 tree. In CLAUDE.md, rewrite only the mandatory-way sentence to: "waits for the Augment and Codex reviews (a reviewer that shows no activity on the PR is skipped)". In docs/user-guide/commands.md and in both release guides, reapply exactly the sentence edits at attempt-2.diff:73, 47 and 60. Do not touch anything else in those files.
2. Before writing the CHANGELOG, write a private checklist (not a file in the repo) of these source conditions:
   - Re-trigger: only after a Wave 6 review-fix push, and only when the cycle applied edits (SKILL.md:274); never after a CI-fix push (SKILL.md:277); no second re-trigger in the decline fallback (SKILL.md:275).
   - Incomplete reviewer: the other reviewer's result is used only when it completed; otherwise the run ends `terminal_timeout` (reviewers.py:396-405).
   - No response: `terminal_augment_no_response` means no configured reviewer responded (SKILL.md:250).
   - Augment-only PRs: they behave as before apart from the added `reviewer_absent` event and the reviewer fields (design:18, SKILL.md:269).
3. Add one `### /sc:pr-submit: Codex reviews` block under `## [Unreleased]` in CHANGELOG.md, with six short bullets, one per required topic:
   - Codex support: the same verify, troubleshoot, fix, push, reply and resolve path as Augment.
   - Fail-open detection: a reviewer with no activity on the PR is recorded `reviewer_absent` and ignored. Augment-only PRs behave as before apart from that event, and Codex-only PRs now work. A present reviewer that does not complete is recorded `reviewer_incomplete`, and the other reviewer's result is used when that reviewer completed. If no reviewer completes, the run ends `terminal_timeout`.
   - P0-P3 mapping: P0 Critical, P1 High, P2 Medium, P3 Low (report-only); a missing or malformed badge falls back to Medium.
   - Dedup: findings on the same path and line are routed at the group's highest tier and fixed once, and every verified member's thread is replied to and resolved.
   - Per-reviewer re-trigger: "After a push that fixes review findings (when the cycle applied edits), one re-trigger comment per present reviewer (`auggie review`, `@codex review`), each with its own watermark; a CI-fix push posts no re-trigger, and the decline fallback posts no second one."
   - UNVERIFIED marker: whether Codex updates its summary marker after `@codex review` has not been observed. If it does not, the Codex re-review ends incomplete at `--timeout`; the other reviewer's result is used when it completed, otherwise the run ends `terminal_timeout`.
4. Do not write "write-ahead", "neither skips nor repeats", or "at most once" about the re-trigger (review-1.md:5, probe-1-1.md:19). Do not write event counts ("41"), and do not describe crash or resume behaviour.
5. Reread each new bullet against the checklist from step 2. Any bullet that states an outcome without its condition gets the condition added or the claim removed.
6. Run `grep -n "the Augment review" CLAUDE.md docs/user-guide/commands.md` and confirm it finds no pr-submit sentence. Then run `make lint`, and run the named pytest command with `uv run`, saving its output to the package's `artifacts/t15-pytest.log`. Edit nothing under src/superclaude/ or .claude/, and create no plugins/ mirror.
7. Stage with `git add .dev/tasks` and do not commit.
differs-by: Before writing any CHANGELOG bullet, list every exception the sources give for each claim, and write each bullet to include them all. Leave out every detail the task does not name: crash and resume ordering, event field lists, the event-type count. Earlier attempts described one path in detail and patched each finding afterwards.

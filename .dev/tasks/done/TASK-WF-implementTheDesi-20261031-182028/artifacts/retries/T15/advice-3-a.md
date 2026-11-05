model: claude-opus-5-5 family: claude rung: top (escalation 1 adviser A; executor tier unknown -> top rung)
outcome: ready

| AC | why earlier attempts missed it (path:line) | change |
|---|---|---|
| T15.AC1 | Not missed. Both reviews marked it met (review-2.md:4, review-1.md:2). A3 starts from the Q0 snapshot, so the four sentence edits must be redone (attempt-2.diff:34, 47, 60, 73). A minor finding (review-2.md:8) says the CLAUDE.md phrase "each one that is installed" (attempt-2.diff:34) is wrong, because presence is decided by activity on the PR (reviewers.py:73-78). | Redo the four sentence edits from attempt-2.diff:34, 47, 60 and 73. In CLAUDE.md, write "(a reviewer that shows no activity on the PR is skipped)" in place of "(each one that is installed on the repository)". |
| T15.AC2 | Not missed. Lint and the named pytest set passed (review-2.md:5, extras-2.log:2-5). The attempt failed on a scope finding instead (review-2.md:6). The CHANGELOG re-trigger bullet "After a push, one re-trigger comment per present reviewer" (attempt-2.diff:18) was written from the review-fix path only (approach-2.md:5). It leaves out three cases. A CI-fix push posts no re-trigger (SKILL.md:277). A re-trigger is posted only when the cycle applied edits (SKILL.md:274). The decline fallback posts no second re-trigger for either reviewer (SKILL.md:275); no review has flagged this third case yet. Each attempt also added details about how the mechanism works (crash ordering, event fields, "41 in all" at attempt-2.diff:18-19), and each detail gave the reviewer a new place to find a missing case (review-1.md:4-5, review-2.md:6-7). | Rebuild the CHANGELOG entry from a list of source conditions written before any bullet. State each conditional claim together with all of its exceptions. Leave out details the task does not ask for. Rerun lint and the named pytest set after the edits. |

differs-by: Before writing any CHANGELOG bullet, list every exception the sources give for each claim, and write each bullet to include them all. Leave out every detail the task does not name: crash and resume ordering, event field lists, the event-type count. Earlier attempts described one path in detail and patched each finding afterwards.

steps:
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

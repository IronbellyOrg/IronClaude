6c36f45c38577fb6cad76516d36081f97887d34e
Review one task for spec compliance.

Task brief: ## Task 2: Describe the blocker check and E-BLOCKED in SKILL.md

Depends on: Task 1

Edit `src/superclaude/skills/sc-issue-protocol/SKILL.md`. In `## Claim mode`, item 3 (`**Wave 2, edge cases**`), add after the existing text that a read-only blocker check follows: an open blocker is STOP `E-BLOCKED` naming each one with no write, none or only closed continues, and an unreadable list continues and the final output says the check could not run. In `## Error handling`, add two rows after the row `| Number or URL is a pull request | STOP `E-NOT-AN-ISSUE` |`: one for an open GitHub "blocked by" issue (STOP `E-BLOCKED` naming each open blocker by number and link, no writes) and one for a blocked-by list that cannot be read (continue as today; the final output says `Blocker check: could not run (<reason>)`). Leave the `## Return contract` block, the "Coordinator handoff" paragraph and the `## Will` and `## Will Not` lists unchanged.

Acceptance criteria (ids added by the orchestrator):
- T2.AC1: `SKILL.md` Claim mode item 3 and the `## Error handling` table both contain `E-BLOCKED`, and the table has a row for the unreadable list that includes `Blocker check: could not run`.
- T2.AC2: `wc -l src/superclaude/skills/sc-issue-protocol/SKILL.md` prints fewer than 500 lines.
- T2.AC3: `tests/skills/test_issue_protocol.py::test_st10_claim_return_contract_has_the_ten_fields_and_keeps_the_old_ones` and `::test_the_coordinator_handoff_is_the_same_paragraph_in_all_three_files` still pass.
Global constraints: ## Constraints

- Change only what the source asks: the blocker read and `E-BLOCKED` stop in the claim, their description in four places, and the tests. Not the issue watcher, not dependency links, and not any other claim behaviour.
- Edit only the canonical files under `src/superclaude/`, the plugin guide copy and the tests. Do not edit or stage anything under `.claude/`; the generated copies come from `make sync-dev`.
- Inside the skill files and the command file under `src/superclaude/skills/sc-issue-protocol/` and `src/superclaude/commands/issue.md`, never write the text `src/superclaude/` (two existing tests forbid it), never write `{owner}/{repo}`, and keep every `gh api` path spelled `repos/<R>/...`.
- Do not touch the paragraph that begins "Coordinator handoff for `--pipeline none`:"; it must stay identical in `refs/claim.md`, `SKILL.md` and `commands/issue.md`.
- Do not add fields to the claim return contract in `SKILL.md`; a test pins its exact keys. A failed read is reported as one line of the final output.
- `SKILL.md` must stay under 500 lines.
Start sha: 6c36f45c38577fb6cad76516d36081f97887d34e
Diff against the start snapshot: 
diff --git a/src/superclaude/skills/sc-issue-protocol/SKILL.md b/src/superclaude/skills/sc-issue-protocol/SKILL.md
index ab06d8c67..69a17602f 100644
--- a/src/superclaude/skills/sc-issue-protocol/SKILL.md
+++ b/src/superclaude/skills/sc-issue-protocol/SKILL.md
@@ -83,7 +83,7 @@ Load `refs/claim.md` now. `<N>` is the issue number, `<D>` = `.dev/issues/<N>/`.
 
 1. **Wave 0, prerequisites.** `uv run --no-project python "<skill base>/scripts/origin_repo.py" --claim "<argument>"` resolves `<R>` and `<N>`: exit 1 STOP `E-NO-ORIGIN`, exit 3 STOP `E-FOREIGN-REPO`, exit 4 STOP `E-NOT-AN-ISSUE`. Then `gh auth status` (else STOP `E-GH-AUTH`), the Orca check `uv run --no-project python "<skill base>/scripts/orca_worktree.py" preflight` (`ok: false` is STOP `E-ORCA-REQUIRED`, before any GitHub or ClickUp write; it runs for `--pipeline none` too, because Orca is a dependency of every claim), the default branch, and create `<D>`.
 2. **Wave 1, lookup.** Load `refs/tiers.md`. Spawn `issue-worker-t3` first (B13); it writes `<D>/scout.md` from `templates/scout-report.md`.
-3. **Wave 2, edge cases** from `scout.md`: a pull request is STOP `E-NOT-AN-ISSUE`; closed or assigned to someone else stops with the stated message and no write (B9); re-claim continues; earlier marked comment IDs are kept for Wave 6.
+3. **Wave 2, edge cases** from `scout.md`: a pull request is STOP `E-NOT-AN-ISSUE`; closed or assigned to someone else stops with the stated message and no write (B9); re-claim continues; earlier marked comment IDs are kept for Wave 6. A read-only blocker check follows (the GitHub "blocked by" list of the issue, read before the Wave 3 assignment): an open blocker is STOP `E-BLOCKED` naming each one, with no write; none or only closed blockers continues; an unreadable list continues and the final output says the check could not run.
 4. **Wave 3, assign.** `gh issue edit <N> --repo <R> --add-assignee @me` (failure STOP `E-ASSIGN-FAILED`, before ClickUp and any comment), then `scripts/clickup_claim.py` with stdout to `<D>/clickup.json`; every ClickUp outcome except an argument error is non-fatal.
 5. **Wave 4, accuracy check and summary.** Spawn `issue-worker-t2`, or `issue-worker-t1` when `scout.md` says `complex`; it writes `<D>/accuracy-check.md`, `<D>/issue-summary.md` (effort in hours) and, when out of date, the analysis report as `<D>/analysis/analyze-<scope>.md` (`<scope>` in this file name is the last segment of the main path the issue touches). No file under `<D>/analysis/` has a name that starts with analysis, report, summary or findings.
 6. **Wave 5, next steps.** Load `refs/chains.md`. Without `--stage`, invoke `Skill sc-recommend` with the goal format of `refs/chains.md` and save its output verbatim to `<D>/recommend.md` from `templates/recommend-record.md`; with `--stage`, do not invoke it and write `<D>/recommend.md` as the one `Skipped: --stage <stage> ...` line (`refs/claim.md` Wave 5). Write `<D>/next-steps.md` from `templates/next-steps.md`, starting with the `/model` tier line and carrying the `Plan boundary: after step <K>` line (and, with `--stage`, the `Stage:` and `Level:` lines and the stage command as step 1, `refs/claim.md` Wave 5). This wave also sets the level `<L>`: the `--pipeline` value or, when it was omitted, the level the default rule of `refs/claim.md` picks from the issue. Unless `--pipeline none`, render `<D>/launch-prompt.md` with `orca_worktree.py prompt` (passing `--stage <stage>` when given; the script keeps the existing prompt only while a launch entry's worktree still exists).
@@ -163,6 +163,8 @@ On a STOP, also print the STOP code and its message.
 | Issue closed | STOP, message "Issue #N is closed; not claimed.", no writes |
 | Assigned to someone else | STOP, message names the assignee, no writes |
 | Number or URL is a pull request | STOP `E-NOT-AN-ISSUE` |
+| An open GitHub "blocked by" issue (Wave 2 blocker check) | STOP `E-BLOCKED` naming each open blocker by number and link, no writes |
+| The "blocked by" list cannot be read (Wave 2 blocker check) | Continue as today; the final output says `Blocker check: could not run (<reason>)` |
 | `issue-worker-t1` spawn fails because `claude-gw-tier1b` is not served to this user | Retry the same job once with `issue-worker-t2` (T1 -> T2 fallback); the T2 file says `Handled by issue-worker-t2 (tier 2): tier1b is not available to this user.` and the accuracy-check comment and `issue-summary.md` (claim) or `flags.md` or `draft-notes.md` (create) show it |
 | `issue-worker-t3` or `issue-worker-t2` spawn fails because its picker ID is not served, or the T2 fallback run is not served | STOP `E-TIER-UNAVAILABLE` naming the agent file and picker ID; no alias fallback |
 | Worker returns no file, or an empty one | Retry that worker once; then STOP `E-WORKER-NO-OUTPUT` with the path expected |

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

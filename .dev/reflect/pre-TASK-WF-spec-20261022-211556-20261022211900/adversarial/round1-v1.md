## Position summary
Variant 1 is the better review, and `ready_with_notes` is the verdict the evidence supports. Every finding in both variants is a fix to an acceptance bullet or a disclosed trade-off. Neither found a defect in the plan's scope, phase order or coverage of Fix 1 to Fix 4 (tasklist lines 17-28 and 30-160). Variant 1 also found the two acceptance weaknesses that most directly break the spec's own rule that every bullet must fail on a wrong edit (source.md:38). Those are the Task 5 header and warning bullets (R1-1) and the Task 6 unchanged-body comparison (R1-5). Variant 2's one unique acceptance-weakness finding, Task 8 (R2-4), is real and I concede it.

## Steelman of Variant 2
Variant 2 reads the tasklist strictly against source.md:38 ("Every acceptance bullet must fail on a wrong edit"). Its strongest point is R2-4. Task 8's bullets (tasklist:141-144) require only `IronbellyOrg/IronClaude` twice and `SuperClaude-Org` zero times on the badge line. They never require `actions/workflows/test.yml`, so a badge pointing at another IronbellyOrg workflow passes. The paragraph checks (`advisory`, `sync/framework`, `pull request`) are word-presence checks only. Variant 2 also has two other strengths:
- It names the `<decided file input>` placeholder (tasklist:124) that Variant 1 missed.
- Its R2-3 concern is legitimate. The new paragraph says the workflow was removed, while the unchanged line 3 still says "the GitHub Actions workflow described below" (scripts/README.md:3) and the heading at line 5 still reads "Publishing (GitHub Actions)". The README will contradict itself.

Finally, four mediums against an explicit spec rule is a reasonable ground for a stricter verdict.

## Strengths claimed (numbered, with citations)
1. **R1-1 is verified.** The header check is only "no `gates`, contains `advisory`" in `sed -n '19,20p'` (tasklist:88). The warning check only forbids the exact old sentence and requires the line to begin with the old prefix (tasklist:90). Deleting the sentence passes it. So does "Human review is mandatory before merge", because the line still begins `echo "::warning title=Mechanical-merge boundary touched::`. Nothing requires `advisory` on the warning line. boundary-guard.yml:19-20 and :50 match the quoted text.
2. **R1-5 is verified.**
   - Task 6 compares only "every step other than `Commit and Push Changes`" to base (tasklist:112).
   - The edited step's `if` (pull-sync-framework.yml:86), `working-directory` (:87) and unchanged body (`git config`, add loop, `git add -f docs/.framework-sync-commit` at :89-105) are never diffed against base.
   - Dropping the state-file add would pass every bullet, although source.md:13 says state-file handling stays unchanged.
   - `--base master --head sync/framework` appears only in the instructions (tasklist:105), not in an acceptance check.
3. **R1-4 is more complete than R2-2.** Both find the git-stub problem. The step runs `git config`, `git add` and `git diff --cached` (pull-sync-framework.yml:89-107). Variant 1 also notes that `GITHUB_REPOSITORY` must be set, that the shell should be `bash -eo pipefail`, and that the third run needs an index equal to HEAD (tasklist:114).
4. **R1-9 reads the scope decision correctly.** source.md:35 says "Change nothing else in that file" and source.md:44 lists scripts/README.md as in scope for one paragraph. Tasklist:26 and Task 9 (:150) disclose every contradicting line. That makes it a disclosed trade-off, not a plan defect. Variant 1 still adds the useful "read neighbours first" step.
5. **R1-8 puts the path-filter item somewhere.** source.md:47 asks that the 300 vs 3,000 discrepancy be verified and raised as a question. The tasklist never mentions it (tasklist:17-28, :146-160). Variant 1 places it in existing artifacts, with no new task, which respects "Do not add a task".
6. **R1-6 and R1-7 are concrete setup gaps.** Task 4 says "on `master`" without `git init -b master` or a commit identity (tasklist:67). Task 5's "two real commits" (tasklist:84) is unpinned, so a non-ancestor BASE would add a spurious file-list difference to `t5-render.diff`.
7. **The severity profile matches the verdict.** Variant 1 downgrades C1 to low after checking the disclosure. It marks R1-12 as 0.5 confidence and says it did not verify the gitignore state.
8. **Citations are absolute paths with line numbers.** Variant 2's bare `TASK-WF-...md:94` and `source.md:24` are ambiguous about which worktree they refer to.

## Weaknesses in Variant 2 (numbered, with citations)
1. **R2-1 is overstated at medium.** The bullet (tasklist:94) says in words "(no backslash before a backtick)", so the intent is recoverable. The calibrator also downgraded it to low.
2. **R2-3 conflicts with the spec.** It asks for a user question before Task 9 about editing neighbouring lines. source.md:35 already decided "Change nothing else in that file". Task 9 (tasklist:150) already hands the leftovers to the user. The extra gate adds a stall with no new information.
3. **`not_ready` is inconsistent with Variant 2's own severity profile.** It files no high finding and all of its fixes are bullet rewrites. Variant 2 also rated the same kind of finding (R2-6, low) as non-blocking.
4. **R2-4's example risk is partly hypothetical.** The boundary entry in .github/workflows/README.md (around line 35) currently says only "with a warning and a reviewer-checklist job summary", not that it blocks. Task 8's own diff-bounding bullet (tasklist:144) already limits changes to the four listed places.
5. **R2-8 is weaker than R1-8.** A "Constraint that the session report must quote docs" has no artifact and no acceptance bullet, so nothing can fail on it.
6. **INF-045 is recorded as "partial, where: null".** That is incoherent. A partial verdict needs a location, and the tasklist has none, so the verdict should be "gap" (see the INF-045 row below).
7. **It missed R1-1, R1-5 and R1-7.** These are the Task 5 and Task 6 acceptance weaknesses, and they matter most to the spec's own quality rule.
8. **Two of its ten findings are not about the tasklist.** R2-9 and R2-10 are coverage-matrix bookkeeping, which Variant 2 itself says needs "No tasklist edit".

## Concessions
- R2-4 (Task 8 acceptance does not fail on a wrong badge target) is valid and Variant 1 missed Task 8 entirely.
- Variant 2 caught `<decided file input>` (tasklist:124), where Variant 1 only covered `<t1-head>`.
- Variant 1's `ready_with_notes` is only honest if the R1-1 and R1-5 notes are applied before execution. Four mediums against source.md:38 are not cosmetic.
- R1-12 is speculative (0.5), and Variant 1 admitted it never read t1-card.md.
- R1-2 and R1-3 largely duplicate Variant 2's R2-6 and R2-1.
- On the dependency chain, Variant 2's repointing is a bit more explicit.
- On INF-041, Variant 2's "partial" is defensible: single-name `Depends on:` lines are satisfied, but "real chains where order matters" is only loosely met.
- A-004 is shakier than the diff-analysis implies, as I say below.

## Shared assumptions (A-001..A-004: ACCEPT|REJECT|QUALIFY + reason)
- **A-001: QUALIFY.** Task 3's acceptance already handles a failed call or a `false` value. It says Fix 1 is blocked and names the setting as a user step (tasklist:58). The residual risk is that the 403 case is not named explicitly, but it is covered by "the call fails".
- **A-002: ACCEPT.** All Python goes through `uv run` (tasklist:21), and a missing PyYAML would fail visibly, not pass silently. The risk is low and fail-closed.
- **A-003: QUALIFY.** The pytest bullet (tasklist:95) tests the merge module, and no planned edit touches tests/ or src/. A pass proves little about the YAML edit. No pre-edit baseline is recorded, but a post-edit pass is still the right gate.
- **A-004: QUALIFY.** The structure is sound. But the mediums (R1-1, R1-5, R2-4) violate an explicit spec rule (source.md:38), so "only acceptance bullets need tightening" is true while the tightening is mandatory before execution, not optional.

## Per-point positions (table: point | winner V1/V2/tie | one-line evidence)

| Point | Winner | Evidence |
|---|---|---|
| S-001 | tie | Granularity differs, neither is wrong. |
| S-002 | V1 | Absolute path plus line is unambiguous; Variant 2's bare filenames are not. |
| C-001 | V1 | Tasklist:94's parenthetical makes the intent recoverable, so low fits; the calibrator downgraded R2-1 as well. |
| C-002 | V1 | The step runs git config, add and diff --cached (pull-sync-framework.yml:89-107); Variant 1 adds the env and shell setup. |
| C-003 | tie | Both say to anchor on text, not line numbers (tasklist:88, :91). |
| C-004 | V2 | Variant 2 also catches `<decided file input>` at tasklist:124 and the fail-if-brackets-survive guard. |
| C-005 | tie | Both identify the spurious links and Task 7 -> Task 2; both fixes are optional-grade. |
| C-006 | V1 | source.md:35 and :44 already decided the scope, and tasklist:26 and :150 disclose it; a pre-Task-9 question contradicts that decision. |
| C-007 | V1 | R1-8 gives an artifact home and a presence check; Variant 2's constraint can't fail. |
| C-008 | tie | Variant 1 finds Task 5 and 6 gaps (tasklist:88, :90, :112); Variant 2 finds Task 8 (tasklist:141-144). They are complementary, and both sets are needed. |
| X-001 | V1 | No high finding in either card, and every fix is a bullet rewrite; the disclosed leftovers do not make the plan unready. |
| X-002 | V1 | source.md:35 and :44 already decided "one paragraph, nothing else", and the disclosure exists at tasklist:26 and :150. |
| X-003 | V1 | INF-045 is absent from the tasklist, so "gap" is right and "partial, where null" is incoherent; INF-041 is a tie, since Variant 2's "partial" is defensible. |
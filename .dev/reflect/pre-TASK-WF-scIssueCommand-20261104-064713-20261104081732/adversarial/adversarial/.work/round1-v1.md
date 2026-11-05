## Advocate: Variant 1 (reviewer-1, sonnet:analyzer)

### Position Summary (1-3 sentences)

Plan version 2 fixed round 1's F-01 and F-02. It added one new problem that matters: plan:26 and plan:254 approve an unattended live `/sc:issue --claim` run whose only protection against GitHub and ClickUp writes is the untested skill prose that the run is meant to test. So the verdict stays FAIL on C-001, while V3's two blockers (C-002, C-003) are real but minor. V1 overstated the target of an escaped write, and I concede that below. The finding still holds, and the fix has to change: require approval and add a deterministic test, not a non-existent-repo URL.

### Steelman: Variant 2

The strongest form of V2: the revision did what round 1 asked. Ordering, token handling, pending-allowed evidence ACs, the fork-safety scan and the spawn-rule spread are all in place (plan:15, plan:23, plan:45, plan:50, plan:126, plan:131, plan:216-227). On that view, everything left is executor-level wording that a competent `/sc:implement` run settles or catches through a red test. Every live write in the plan is gated on "the user's explicit approval at that moment" (plan:26, plan:254), and pending is an allowed result (plan:236, plan:246, plan:258). So no finding meets the binding severity rule, and the plan should PASS with notes.

V2 gets several things right. Q-1: the deferral of PR opening is disclosed, with the exact command at plan:25. Q-2: `--limit 200` was directed by round-1 F-15 and is disclosed at plan:92. Q-3: the source-only narrowing was directed by round-1 F-11 and is documented at plan:129. Q-4 correctly sees that ACs 1, 2, 3, 6 and 8 will most likely end pending (plan:254). The blind calibrator rated V2 the best-grounded card (citation_grounding 0.90, reviewer-2-calibration.yaml:2).

### Steelman: Variant 3

The strongest form of V3: two tasks in the plan rest on mechanics the plan never checked.

- **S-2:** `/sc:implement` has no "pause for a new session" state. Q8 is "Only if complete ... Else STOP" (sc-implement-protocol/SKILL.md:135). An executor told to "stop here" (plan:233) either halts outside any defined ledger row, or takes the easier exit and writes a "pending" row (plan:236). If it writes the pending row, the scheduled smoke spawn (source.md:473) quietly never happens.
- **S-1:** Task 6 must copy the section-14 error table (plan:111). That table has the row "`gh issue edit --add-assignee` fails" (source.md:336). Task 7's scan requires `--repo` on every `gh issue` line (plan:131). The two tasks pull against each other.

V3 is also the richest card on concrete executability traps:
- **S-5:** evidence-validator.md:8 does carry `permissionMode: plan`, and plan:56 says to follow that file's shape.
- **S-7:** the tier proxy forwards a tier request to a real tier member model (local-gateway-alias-proxy.py:17-21), so the served-model evidence may never show the picker ID that plan:236 asks for.
- **S-3:** Task 17's `Depends on` list (plan:252) omits Tasks 15 and 16, whose evidence it cites (plan:254).
- **S-4:** plan:23 bans `env` on the token, while plan:50 uses `env -u`.

These are verified and useful.

### Key Strengths Claimed (numbered, with citations)

1. **The only card that names the new risk the revision introduced (C-001).** plan:26 states that "A run that stops before any GitHub or ClickUp write (section 20 item 4) may run without asking". plan:254 then schedules `/sc:issue --claim https://github.com/octocat/Hello-World/issues/1` as that run. Whether it "stops before any write" is the very behaviour under test. It depends on the Wave 0 URL-vs-origin check (source.md:143), which exists only as skill prose. Task 1 tests only origin parsing (plan:32-38), and no task tests the comparison.
   - If the check fails, Wave 3 assigns (source.md:162) and runs the ClickUp script (source.md:163), and Wave 6 posts two comments (source.md:178-179).
   - plan:259's AC ("No GitHub issue was assigned, commented on or created without the user's approval") cannot be guaranteed by anything in the plan.
   - Round-1 F-03 recommended "ask the user before any run against a real issue, because a faulty Wave 2 guard reaches `gh issue edit --add-assignee`" (round-1 merged-verdict.yaml:64). The revision carved item 4 out of that rule.
   - The blind calibrator kept A-1 blocking (reviewer-1-calibration.yaml:5).
2. **Correct reading of the executor on C-002 / X-002.**
   - A stop at Task 15 before any verdict leaves only that task's `start` line. Q0 reuses that sha on a re-run (sc-implement-protocol/SKILL.md:109), and ledger Row S ("Start line only -> ... A1, as today", refs/ledger.md:161) re-executes the task. So "it resumes at this task" (plan:233) is achievable.
   - The real defect is the one A-2 named: two exits are allowed at once, "stop and restart" (plan:233) and "pending (with the reason the session could not run it)" (plan:236). Nothing says which one wins.
   - The calibrator downgraded S-2 to minor on exactly this ledger evidence (reviewer-3-calibration.yaml:6).
3. **Correct classification of C-003 as minor.**
   - Task 7's rule applies to a line "that runs `gh issue`, `gh pr` or `gh label`" (plan:131). The test author defines "runs", and the error-table row can be written with `--repo <R>`.
   - Any clash produces a loud red test inside Task 7's own AC (plan:135), and the executor fixes it there. That is not silent wrong behaviour.
   - A-5 also names the trap V3 missed: copying the spec's prose "never `{owner}/{repo}`" (source.md:319) into SKILL.md would trip the placeholder ban (plan:131). The calibrator agreed with minor (reviewer-1-calibration.yaml:9, reviewer-3-calibration.yaml:5).
4. **Only card to check the round-1 blockers** (`round1_fix_check: {F-01: fixed, F-02: fixed}`). The evidence sheet E21 confirms both: plan:216-227 for ordering, and plan:23, plan:45, plan:50 for token handling.
5. **Test-isolation gap that no other card saw (A-4, U-002).** plan:43 reads `CLICKUP_LIST_IDS` and `CLICKUP_MAX_PAGES` from the environment. plan:45 clears only the token and workspace variables. An exported `CLICKUP_MAX_PAGES` therefore leaks into the page-cap and first-page test (plan:45), and an exported `CLICKUP_LIST_IDS` changes the request URLs.
6. **C-004 (A-3) carries the most complete safety detail.**
   - The secrets rule at plan:23 does not ban `curl -v`, `-i` or `--trace`, which would print the auth header during an ad hoc "key path" probe (plan:243).
   - The AC "first `assigned`" (plan:246) cannot hold if the user is already on the test task.

### Weaknesses in Variant 2 (numbered, with citations)

1. **The PASS verdict is not argued, only asserted.** V2 is silent on the live item-4 run (plan:254), the Task 15 dual exit (plan:233 vs plan:236) and the Task 6/Task 7 interaction (plan:111 vs plan:131). Its self_audit says it audited "sections 4, 7, 8, 12-17, 20 against every task" (variant-2-original.md:13), yet it raised nothing on section 7 Wave 0 (source.md:143), which is the guard plan:26 relies on.
2. **"ACs observable" is a false self-audit claim.** AC 5's first half (source.md:471) is not assigned in plan:254, and AC 8's offline half (source.md:474) is not pinned by any test (plan:77, plan:81-85). V2's own calibrator lists both as missed (reviewer-2-calibration.yaml:10-12).
3. **Two of its four findings are non-findings.** Q-2 (`--limit 200`) and Q-3 (source-only flag check) are the plan carrying out round-1 F-15 and F-11 (round-1 merged-verdict.yaml:179, :229). They are authorized expansions directed by the previous round, not deviations, and both recommend "leave as is". Q-1's recommendation repeats what plan:25 already says.
4. **Q-4 partly duplicates the plan.** plan:254 already says "leave them pending ... unless the user approves a run against a test issue at that moment". The only new part is the proactive request at the end of Task 17, which is minor.
5. **The ClickUp posture is approved without checking the shared session.** The self_audit claims the "ClickUp posture satisfies section 12". But plan:23 and plan:243 have the user export live ClickUp variables into the very session where Task 17's unapproved item-4 run happens (evidence sheet E5). An escaped item-4 claim would reach the ClickUp script with a live token, and rule 2's `#<N>` title match (source.md:307) has `N = 1` in that escape path.

### Weaknesses in Variant 3 (numbered, with citations)

1. **S-2 is over-graded, and its own evidence refutes it.** S-2 cites refs/ledger.md:161 (Row S), which re-runs a task that has only a start line. That is exactly the resume path plan:233 describes. Row P (ledger.md:155), which S-2 leans on, applies only after a `blocked` verdict, and no verdict exists at a pre-spawn stop. The surviving defect is the ambiguity between plan:233 and plan:236, which is minor (reviewer-3-calibration.yaml:6).
2. **S-1 is over-graded.**
   - plan:131 scopes the scan to lines that "run" gh, and plan:111 does not require copying the section-13 write list word for word. The table row can name `gh issue edit <N> --repo <R> --add-assignee @me`.
   - At worst, Task 7's test goes red and Task 7's AC (plan:135) forces the fix in the same task.
   - None of the severity rule's four triggers applies.
3. **V3 misses the one real live-write exposure.** It reviewed plan:254, citing it in S-3, but did not question the unapproved live claim run in that same paragraph.
4. **S-11 is wrong on its premise.** Per-task extras already detect and run `make lint` (sc-implement-protocol/SKILL.md:132, :146; Makefile:48-50). The calibrator calls it overstated (reviewer-3-calibration.yaml:15).
5. **S-12 is style only.** It is correct (docs/user-guide/commands.md:236 vs plan:197) but it pads the card.
6. **S-9 changes nothing in practice.** Interim red tests in untouched test files are recorded as `unrelated-red` and never change a verdict (SKILL.md:152-154).

### Concessions

1. **A-1 overstates the target.**
   - Every `gh` call uses `--repo <R>` resolved from origin (source.md:142, :319). So if the Wave 0 check fails, writes land on `IronbellyOrg/IronClaude#1`, not on octocat's repo.
   - Origin #1 is a merged pull request (evidence sheet E4), so the Wave 2 prose guard "number is a pull request -> STOP E-NOT-AN-ISSUE" (source.md:159) is a second barrier. A write needs two prose guards to fail, plus a successful Wave 1 spawn.
   - I keep the blocking grade for three reasons. Both barriers are untested LLM-followed prose in the same skill. The plan's AC plan:259 is not guaranteed by any mechanism. And the session may carry live ClickUp variables (plan:23, plan:243).
   - My recommendation of a non-existent-repo URL does not remove the risk, because writes use `<R>`. I withdraw that part. The fix becomes: the item-4 run needs the user's approval at that moment, like every other live claim (round-1 F-03), and the URL-vs-origin comparison gets a deterministic test (A-005).
2. **A-2's second half is weak.** Agents reach `.claude/agents/` at Task 13's `make sync-dev` (plan:209), so "after Task 13" (plan:233) is defensible. V3's S-3 is the better dependency finding for C-007.
3. **A-6 is low-value.** plan:43 already tells the implementer to define and document the invalid-`CLICKUP_MAX_PAGES` behaviour, which was round-1 F-16's fix. Only the bound (exit 0, per source.md:310) is missing.
4. **V1 missed items that V3 and the calibrators found:**
   - S-5 (`permissionMode: plan`, evidence-validator.md:8)
   - S-7 (proxy tier rewrite)
   - S-4 (`env -u` vs the `env` ban)
   - the missing URL-vs-origin test (A-005), which is the natural fix for my own A-1
   - AC 5's first half and AC 8's offline half
   - the Task 17 fresh-session gap (A-007), even though I raised the same issue for Task 15 in A-2

### Shared Assumptions (A-001..A-008: ACCEPT/REJECT/QUALIFY + evidence + proposed severity)

- **A-001: ACCEPT (no finding).** Section 16 defines the static test as "the spawn rule text ("never pass the `model` parameter") is present" (source.md:391), and plan:126 matches it, now across SKILL.md and every ref. Round 1 rejected the same challenge (round-1 merged-verdict.yaml:284-285, `A-003-ac7-phrase-test`). A skill made of prose has no Agent call site to inspect beyond its text. Disposition: reject.
- **A-002: QUALIFY, minor.** plan:254 assigns item 5's ClickUp half to Task 2 and Task 16 and lists items 1, 2, 3, 6 and 8 as pending. It never places AC 5's first half: "with CLICKUP_API_TOKEN unset the claim completes and the comment says ClickUp was skipped" (source.md:471). The general rule at plan:26 still prevents an unapproved run, so this is a gap in clarity, not in safety. Fix: name item 5's first half as pending unless approved, and cite the Task 2 skipped test and `t2-clickup-skipped.txt` as its offline half.
- **A-003: REJECT, minor.** AC 8 requires next-steps.md to start "with the `/model` tier line of section 9" (source.md:474). plan:77 defines the template that way, but neither Task 4's ACs (plan:81-85) nor Task 7's tests (plan:123-132) assert it, and the run-time half is pending live. Fix: Task 7 asserts that the first non-empty line of `templates/next-steps.md` is the `/model claude-gw-tier2|claude-gw-tier1a` line.
- **A-004: QUALIFY, minor.** plan:131 checks `--repo` on `gh issue|pr|label` lines and bans the `{owner}/{repo}` placeholder. That placeholder is the one that resolves to gh's default repo, which is the fork parent, so the main risk is covered. It does not assert section 13's positive form, "every `gh api` path spells `repos/<R>/...`" (source.md:319), so a hardcoded `repos/IronbellyOrg/...` or `repos/<owner>/...` would pass. Fix: every `gh api` line containing `repos/` spells `repos/<R>/`.
- **A-005: REJECT, minor on its own; it is the root of C-001.** Section 15 created origin_repo.py "so the parsing is tested code rather than prose" (source.md:361). The URL-vs-origin comparison that yields `E-FOREIGN-REPO` (source.md:143) and is required by AC 4 (source.md:470) is still prose only, while Task 1 tests origin parsing only (plan:32-38). Fix: a pure comparison function in origin_repo.py (or a `--check-url` mode the skill calls in Wave 0), pinned by a test for a same-repo URL, a foreign URL, and owner/repo case. Section 16 does not require this, so it is a minor addition, but it is the cheapest deterministic part of the C-001 fix.
- **A-006: ACCEPT (no finding).** Task 16 runs only after the user supplies the test issue URL and task ID (plan:243), with variables the user exported themself (plan:23). It is a check the source schedules (source.md:314). Supplying the task ID is the approval moment. The script PUTs only on a unique rule match against the user's own test issue URL, and ambiguity means no PUT (source.md:308). The ClickUp exposure that matters is the exported token reaching an escaped item-4 run, which belongs to C-001. Disposition: reject.
- **A-007: QUALIFY, minor.** plan:254 requires "a session that has the skill loaded (after Task 13)" but gives no precondition check or restart path, unlike Task 15 (plan:233). The pending fallback at plan:258 keeps it truthful. The risk is an executor that "runs" item 4 by reading SKILL.md and narrating the result, which is not a real run. Fix: the same session precondition as Task 15, and a statement that a simulated or read-through run is not evidence. With C-001's fix applied, the run also needs approval.
- **A-008: ACCEPT (no finding).** `uv run` syncs the project's main dependencies, including pytest (pyproject.toml:34-35), in the new Orca worktree. The comparison is only for failing tests (plan:220: "running the same failing test on master"). ruff sits in the `dev` extra (pyproject.toml:46-54) but no lint comparison on master is required. Disposition: reject.

### Position Table

| Point | Winner | Disposition | One-line reason with a citation |
|---|---|---|---|
| S-001 | none | reject | Card schema and key differences are format only; no plan defect (variant-1/2/3-original.md headers). |
| S-002 | none | reject | The verdict basis follows from the C-001..C-003 rulings, not from finding counts; no separate finding. |
| C-001 | V1 | blocking | plan:26/plan:254 approve an unapproved live claim guarded only by untested prose (source.md:143, plan:32-38); plan:259 is unguaranteed; contradicts round-1 F-03 (merged-verdict.yaml:64). Fix: approval at that moment plus a URL-vs-origin test; target conceded as origin #1. |
| C-002 | V1 | minor | Resume works via Q0 sha reuse and Row S (sc-implement SKILL.md:109, refs/ledger.md:161); the real defect is plan:233 vs plan:236 offering two exits with no rule for which wins. |
| C-003 | V1 | minor | plan:131 "runs" is author-scoped and the table row can carry `--repo <R>` (source.md:336); any clash is a loud red test fixed under plan:135; the placeholder-prose trap (source.md:319) is the real hazard. |
| C-004 | V1 | minor | plan:243 names no method; ban `curl -v/-i/--trace`; accept `already_assigned` on the first run (plan:246); fold in V3's `test -n "${CLICKUP_API_TOKEN:-}"`. |
| C-005 | V1 | minor | plan:45 clears 2 of the 4 CLICKUP_* variables that plan:43 reads; V3's S-4 (plan:23 vs plan:50 `env -u`) also survives as minor. |
| C-006 | V2 | minor | Pending ACs are truthful (plan:15, plan:258); Q-4's proactive request for a scratch issue adds only a little over plan:254's "unless the user approves". |
| C-007 | V3 | minor | plan:252 `Depends on: Task 14` omits Tasks 15 and 16 cited at plan:254; the executor ignores depends-on (SKILL.md:79), so this is metadata only; V1's "after Task 14" is conceded. |
| X-001 | V1 | blocking | FAIL: C-001 stands blocking; V3's S-1/S-2 fall to minor (reviewer-3-calibration.yaml:5-6); V2's PASS ignores plan:26/plan:254. |
| X-002 | V1 | minor | Yes, resume is possible: a pre-verdict stop leaves only a start line and Row S re-runs it (refs/ledger.md:161); clarify which exit wins. |
| A-001 | none | reject | source.md:391 defines the static test as phrase presence; plan:126 matches; round 1 rejected the same challenge (merged-verdict.yaml:284-285). |
| A-002 | new | minor | AC 5's first half (source.md:471) is unplaced in plan:254; name it pending unless approved and cite Task 2's offline evidence. |
| A-003 | new | minor | AC 8's `/model` first line (source.md:474) is defined at plan:77 but unasserted in plan:81-85 and plan:123-132; add a Task 7 assertion. |
| A-004 | new | minor | plan:131 bans the placeholder but never asserts that `gh api` paths spell `repos/<R>/` (source.md:319). |
| A-005 | new | minor | The URL-vs-origin comparison (source.md:143, AC 4 source.md:470) is untested while plan:32-38 tests parsing only; this is the deterministic part of the C-001 fix. |
| A-006 | none | reject | The user supplies the test URL and task ID and exports the variables themself (plan:23, plan:243); a PUT happens only on a unique match (source.md:308). |
| A-007 | new | minor | plan:254 needs "skill loaded (after Task 13)" with no precondition or restart path, unlike plan:233; a read-through run must not count as evidence. |
| A-008 | none | reject | `uv run` syncs main dependencies including pytest (pyproject.toml:34-35); only failing tests are compared on master (plan:220). |

# Adversarial Debate Transcript

## Metadata
- Depth: standard
- Rounds completed: 2 (Round 1 parallel statements, Round 2 sequential rebuttals) plus Round 2.5 invariant probe (see invariant-probe.md)
- Convergence threshold: 80%
- Focus areas: correctness, coverage, deviation-classification
- Advocate count: 3 (V1 reviewer-1 sonnet:analyzer, V2 reviewer-2 haiku->glm-5.3:qa, V3 reviewer-3 opus:refactorer)
- Diff points in the convergence denominator: 19 (S-001..S-002, C-001..C-007, X-001..X-002, A-001..A-008)
- Assembly note: Rounds 1 and 2 ran 08:45-09:00 UTC and are reproduced verbatim from `.work/round1-v{1,2,3}.md` and `.work/round2-v{1,2,3}.md`. The run was interrupted by an API outage before Round 2.5; this transcript, the scoring matrix and the convergence assessment were assembled on resume (replacement worker, 2026-11-04 after 12:41 UTC). Evidence facts E1..E21 cited by the advocates are in `.work/evidence-sheet.md`.

## Round 1: Advocate Statements

### Variant 1 Advocate (reviewer-1, sonnet:analyzer)

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


### Variant 2 Advocate (reviewer-2, haiku->glm-5.3:qa)

## Advocate: Variant 2 (reviewer-2, haiku->glm-5.3:qa)

### Position Summary (1-3 sentences)
Plan version 2 fixes both round-1 blockers (F-01 ordering, F-02 token handling) and, on re-reading the executor and the spec, none of the three "blocking" findings the other cards raise meets the binding severity rule once the file evidence is applied: S-1 is satisfiable, S-2 is wrong about the executor, and A-1 needs two or three independent guard failures to cause any write. The merged verdict should be PASS with minor notes, and it should absorb several real minor gaps my card missed (C-001 as minor, C-002, C-003, C-004, C-005, A-002, A-003, A-004, A-005, A-006).

### Steelman: Variant 1
Strongest form: the revision itself introduced a live `/sc:issue --claim` against a real third-party issue (plan:254) and exempted it from approval by classifying it by its *intended* outcome ("stops before any GitHub or ClickUp write", plan:26), not its *actual* outcome. The only thing standing between that run and a public comment or assignment is the very prose under test (source.md:143), which has no deterministic test (Task 1 tests parsing only, plan:32-38). Round 1's F-03 explicitly said "ask the user before any run against a real issue" (round-1 merged-verdict.yaml:64), and the revision departed from that. V1 is also the only card that checked the round-1 fixes (`round1_fix_check`), and its A-2, A-3, A-4, A-5, A-6 are accurate, correctly sized minors. V1 is right that a fix is needed and right on the mechanism; I dispute only the severity.

### Steelman: Variant 3
Strongest form: V3 did the deepest executor and repo grounding of the three cards. It noticed that the plan's own texts can collide (Task 6 must copy the section 14 error table, whose row source.md:336 names `gh issue edit --add-assignee` without `--repo`, while Task 7's scan at plan:131 demands `--repo` on every line that "runs" gh), that `/sc:implement` has no explicit "pause for a new session" state, and it found real traps nobody else saw: `permissionMode: plan` in the frontmatter Task 3 is told to copy (src/superclaude/agents/evidence-validator.md:8, plan:56), the tier proxy rewriting the picker ID (S-7), `scripts/__pycache__` tripping the "every file" inventory (S-8, plan:125 vs plan:115), and the unpinned D26 sentence (S-10). These are useful minors.

### Key Strengths Claimed (numbered, with citations)
1. Correct overall verdict. Every blocking claim on the table collapses under the severity rule once the files are re-read (see Weaknesses below); the blind calibrator of V3 reached the same conclusion: "With S-1 and S-2 minor the card's verdict should be PASS with notes" (reviewer-3-calibration.yaml:19).
2. Highest calibration of the three cards: C = 0.78, citation_grounding 0.90, deviation_classification_clarity 0.85 (reviewer-2-calibration.yaml:2-3), and all four of my severities were upheld (reviewer-2-calibration.yaml:5-8). No V2 claim is false.
3. Self-audit claims re-verified: Task 6 lists all nine STOP codes (plan:111: E-NO-ORIGIN, E-FOREIGN-REPO, E-GH-AUTH, E-NOT-AN-ISSUE, E-TIER-UNAVAILABLE, E-WORKER-NO-OUTPUT, E-ASSIGN-FAILED, E-POST-FAILED, E-CREATE-FAILED); repo anchors hold (tests/recommend/test_routing_refresh.py:32 `_POST_REFRESH_ADDITIONS = {"graph", "impact"}`; tests/cli/test_issue_body_templates.py:57 and :78 are the two tests plan:156 names).
4. Q-4 (C-006) is the only finding on the acceptance posture as a QA risk: plan:15 and plan:254 let ACs 1, 2, 3, 6 and 8 (source.md:467-469, 472, 474) end pending, so the core end-to-end claim/create behaviour can ship with zero live verification. plan:254 says "unless the user approves a run ... at that moment" but never tells the executor to *ask*; my recommendation (one closing request to pre-approve one scratch issue) closes that gap without weakening B1.
5. Deviation classification. Q-2 (plan:92 `--limit 200`) and Q-3 (plan:129 source-only flag check) are disclosed, round-1-sanctioned additions (round-1 F-15 and F-11, merged-verdict.yaml:224-229, 173-179). V2 classified them correctly as acceptable rather than as drift.

### Weaknesses in Variant 1 (numbered, with citations)
1. A-1 is over-graded as blocking. For any write to happen the implementation must fail Wave 0's URL check (source.md:143) AND then:
   - for a write on octocat/Hello-World: ignore `--repo <R>` and pass the raw URL to gh, which contradicts source.md:319 and is exactly what Task 7's fork-safety test rejects (plan:131: every gh issue|pr|label line carries `--repo`);
   - for a write on the origin repo: every call carries `--repo <R>` from origin (plan:22, source.md:319), so N = 1 lands on IronbellyOrg/IronClaude#1, which the orchestrator recorded (E4; I could not re-run gh under my rules) as a merged pull request; Wave 2 stops on a pull request number (source.md:159) before the Wave 3 assign (source.md:162) and the Wave 6 comments (source.md:178-179).
   Two or three independent guard failures for a reversible, self-attributed write is not "a security/data-loss risk" under the binding rule; V1's own calibrator called the target "overstated" (reviewer-1-calibration.yaml:5). Also V1's proposed non-existent-repo URL does not reach the escape path V1 describes, because writes use `<R>`, not the URL's repo (same calibration line).
2. A-2 implies the executor should "stop without writing the artifact and ask the user to restart"; that is fine, but V1 does not show the resume works. It does: a stop before any verdict leaves only a start line (src/superclaude/skills/sc-implement-protocol/SKILL.md:108-115), and refs/ledger.md:161 Row S "Start line only -> ... A1, as today" re-runs the task. V1 is right in substance but under-evidenced.
3. Missed the A-003 and A-004 offline gaps and the C-006 posture risk.

### Weaknesses in Variant 3 (numbered, with citations)
1. S-2 is factually wrong. "/sc:implement has no pause-for-new-session state ... 'it resumes at this task' cannot work" ignores ledger.md:161 Row S (start line only -> re-run A1). Row P (ledger.md:155) that V3 relies on applies only when "Latest verdict is `blocked`", which a stop before review never writes. V3 even cites ledger.md:161 in its own evidence (variant-3-original.md:16), which supports the opposite. This is a false claim inside a blocking finding; it must be downgraded to minor (two exits, plan:233 vs plan:236).
2. S-1 is not a contradiction. Task 6 can satisfy both tasks by writing the error row as `gh issue edit --repo <R> --add-assignee` (source.md:462 already shows the house style of carrying `--repo` in the flags column). At worst Task 7's own test goes red and Task 7 fixes it inside the same run; a self-detecting red test is not wrong behaviour shipped. Minor, as V3's calibrator ruled (reviewer-3-calibration.yaml:5).
3. S-11 is overstated: Q6 extras already run lint per task (SKILL.md:132, :146 `make lint`).
4. S-3 is cosmetic for this executor: depends-on is ignored and tasks run in source order (SKILL.md:79, :97), so Task 17 always runs after Tasks 15 and 16.
5. S-4 is a wording issue: plan:23 bans `env` used to print the token ("never ... prints, echoes or inlines"); `env -u` (plan:50) unsets it. Minor at most.

### Concessions
1. My card missed C-001 entirely. Whatever severity is ruled, a finding must survive and V1 earned it. The revision departs from round-1 F-03's "ask the user before any run against a real issue" (round-1 merged-verdict.yaml:64), and plan:26 classifies the run by intent. I argue minor, not none.
2. My card missed C-002/X-002, C-003, C-004, C-005, C-007 and every calibrator `missed_by_card` item (reviewer-2-calibration.yaml:9-14). My coverage_completeness (0.70) and risk_surface_coverage (0.65) are the weakest dimensions.
3. My self_audit "ClickUp posture satisfies section 12" is too strong: Task 16 has no key-path method (plan:243), tests clear only two of four variables (plan:45 vs plan:43), and the PUT target is chosen by the script's match rules, not by the task ID the user gives (see A-006).
4. Q-1 adds little: plan:25 already names the exact `/sc:pr-submit` command. Q-2 and Q-3 are round-1-sanctioned additions and should be recorded as authorized expansions, not as findings needing work.

### Shared Assumptions (A-001..A-008: ACCEPT/REJECT/QUALIFY + evidence + proposed severity)
- **A-001 ACCEPT (no finding).** source.md:391 defines the section 16 static test as "the spawn rule text ('never pass the `model` parameter') is present", and source.md:132 requires that text in SKILL.md and every ref; plan:126 checks exactly that across SKILL.md and every refs/*.md. Round 1 already ruled this adequate (round-1 merged-verdict.yaml:284-285, `A-003-ac7-phrase-test`). The skill is LLM-executed prose; there is no code-level Agent call to scan. Re-raising it without new evidence would reopen a settled ruling.
- **A-002 QUALIFY, minor.** plan:254 maps "item 5's ClickUp half" to Task 2 and Task 16 and names items 1, 2, 3, 6, 8 as pending, but never names item 5's first half (source.md:471: the claim completes with the token unset and the comment says ClickUp was skipped). The generic rule "each row says run or pending" covers it, but an executor can wrongly mark it "run" by pointing at Task 2's script-only no_token check (plan:50), which proves neither a completed claim nor the comment text: a false-claim risk in the acceptance record. Fix: name item 5's first half as pending with its exact command.
- **A-003 REJECT, minor.** source.md:474 requires next-steps.md to start with the `/model` tier line; plan:77 defines the template that way but no AC in Task 4 (plan:81-85) and no test in Task 7 (plan:123-132) asserts the template's first line. The offline half is cheap to pin and plan:254 instead parks all of item 8 as pending. Not a section 16 deliverable, so minor.
- **A-004 QUALIFY, minor.** plan:131 implements round-1 F-04 exactly (`--repo` on gh issue|pr|label lines, no `{owner}/{repo}`; round-1 merged-verdict.yaml:81). The placeholder ban covers the main fork-parent risk, but source.md:319 also requires every `gh api` path to spell `repos/<R>/...`; a hardcoded `repos/<owner>/<repo>` is not caught. Fix: add a `gh api` line check for `repos/<R>/`.
- **A-005 REJECT, minor.** source.md:361 says origin_repo.py exists "so the parsing is tested code rather than prose", yet the URL-vs-origin comparison that yields E-FOREIGN-REPO (source.md:143) stays prose, and Task 1 tests parsing only (plan:32-38, plan:34). This is the cheapest real fix for C-001: put the comparison in origin_repo.py (or a helper in it) and pin E-FOREIGN-REPO with a unit test, so AC 4 becomes "run" offline. Not required by section 16 (source.md:394), so minor.
- **A-006 QUALIFY, minor.** plan:26's approval rule names GitHub writes only. Task 16 does ask the user for the test issue URL and task ID (plan:243), which is close to approval, but the PUT target is chosen by the script's match rules across the whole workspace (source.md:304-309), not by the task ID the user gave. If the test task does not actually link the URL, rule 2 (`#<N>` in a title, source.md:307) can match and self-assign some other real task. Fix: run only after the user confirms, and check that the reported `task_id` equals the user's test task ID before the second run.
- **A-007 ACCEPT (no finding).** Item 4 stops in Wave 0 (source.md:141-143), before the first worker spawn in Wave 1 (source.md:147), so it needs no fresh agent definitions; in normal flow Task 17 runs in the session Task 15 restarted (source order, SKILL.md:97); and plan:258 explicitly allows "pending with the reason the session could not run it". No restart instruction is needed.
- **A-008 ACCEPT (no finding).** `uv run` syncs the main dependencies, and pytest is a main dependency (pyproject.toml:34-43); addopts carries no coverage or benchmark flag (pyproject.toml:112-116), and no test imports scipy or uses the `benchmark` fixture (grep of tests/ found none). The comparison is for failing tests only, not lint (plan:220), so the dev extra (ruff) is not needed there.

### Position Table

| Point | Winner | Disposition | One-line reason with a citation |
|---|---|---|---|
| S-001 | none | reject | Card schema and YAML style differences carry no finding (diff-analysis.md:19). |
| S-002 | V2 | reject | Granularity is not a finding; the verdict basis is settled under X-001 (variant-3-original.md:29 rests FAIL on S-1/S-2, both downgraded). |
| C-001 | V1 | minor | Real gap (plan:26 exempts a live run by intent; departs from round-1 F-03 at merged-verdict.yaml:64), but any write needs Wave 0 plus `--repo` or Wave 2 PR guard to fail (source.md:143, 159, 319; plan:131); fix with A-005 test plus user approval. |
| C-002 | V1 | minor | Two exits at plan:233 vs plan:236 are a clarity gap; resume works via ledger.md:161 Row S, so S-2's "cannot work" is false. |
| C-003 | V1 | minor | Satisfiable by writing `--repo <R>` in the error row (source.md:336, house style source.md:462); at worst Task 7's own test goes red and is fixed in-run (plan:131). |
| C-004 | V1 | minor | Task 16 names no key-path method and the first-run `assigned` AC fails if already assigned (plan:243, plan:246); merge V3's `test -n "${CLICKUP_API_TOKEN:-}"`. |
| C-005 | V1 | minor | Tests clear 2 of 4 CLICKUP_* vars (plan:45 vs plan:43); merge V3 S-4 wording (plan:23 vs plan:50, unset not print). |
| C-006 | V2 | minor | ACs 1, 2, 3, 6, 8 may all end pending and the executor is never told to ask for approval (plan:15, plan:254); add one pre-approval request. |
| C-007 | V1 | minor | "after Task 13" should be "after Task 14" (plan:233, plan:231); Depends-on gap S-3 is cosmetic because the executor ignores depends-on (SKILL.md:79, :97). |
| X-001 | V2 | minor | PASS: no blocking survives (C-001, C-002, C-003 all minor under the binding rule); round-1 F-01/F-02 fixed (plan:216-246, plan:23, 45, 50). |
| X-002 | V1 | minor | Yes: a stop before review leaves a start line only (SKILL.md:108-115) and ledger.md:161 Row S re-runs the task; V3's Row P (ledger.md:155) needs a blocked verdict. |
| A-001 | none | reject | ACCEPT: source.md:391 defines the static test as phrase presence; plan:126 matches; round-1 rejected finding A-003-ac7-phrase-test. |
| A-002 | new | minor | QUALIFY: AC 5 first half (source.md:471) unnamed in plan:254; risk of a false "run" via Task 2's script-only check (plan:50). |
| A-003 | new | minor | REJECT: next-steps.md first-line rule (source.md:474, plan:77) has no AC or test (plan:81-85, plan:123-132). |
| A-004 | new | minor | QUALIFY: scan omits `gh api` paths spelling `repos/<R>/` (source.md:319 vs plan:131). |
| A-005 | new | minor | REJECT: URL-vs-origin comparison is untested prose (source.md:143, 361; plan:32-38); a unit test is the cheapest C-001 fix. |
| A-006 | new | minor | QUALIFY: no explicit approval for the live PUT, and the script, not the user's task ID, picks the target (plan:243, source.md:304-309). |
| A-007 | none | reject | ACCEPT: item 4 stops in Wave 0 before any spawn (source.md:143, 147) and plan:258 allows pending. |
| A-008 | none | reject | ACCEPT: pytest is a main dependency and uv run syncs it (pyproject.toml:34-43, 112-116); no test needs dev extras. |


### Variant 3 Advocate (reviewer-3, opus:refactorer)

## Advocate: Variant 3 (reviewer-3, opus:refactorer)

### Position Summary (1-3 sentences)
Variant 3 has the widest correct coverage of plan version 2 (twelve findings; ten survive calibration unchanged and all twelve hold up as real defects), but its FAIL rests on S-1 and S-2. After re-reading the executor, I concede both are minor: Row S re-runs a started task, and Task 7 can settle the scan definition itself. The merged verdict should still be FAIL, on Variant 1's A-1 (C-001). The plan tells the executor to run a live `/sc:issue --claim` without asking against a real third-party issue, and the only thing between that run and a public write is untested skill prose.

### Steelman: Variant 1
The strongest form of V1: plan version 2 opened a new hole when it carved item 4 out of the approval rule. plan:26 says a run "that stops before any GitHub or ClickUp write (section 20 item 4) may run without asking". plan:254 then runs `/sc:issue --claim https://github.com/octocat/Hello-World/issues/1` live. Whether that run "stops before any write" is exactly what is being tested, and no deterministic test covers the URL-vs-origin comparison: Task 1 pins origin parsing only (plan:32-38, plan:38). Round 1's F-03 recommendation said to "ask the user before any run against a real issue, because a faulty Wave 2 guard reaches `gh issue edit --add-assignee`" (round-1 merged-verdict.yaml:64). The revision did the opposite for item 4. V1 is also the only card that checks the round-1 fixes (`round1_fix_check`). Its A-4 (exported `CLICKUP_MAX_PAGES` / `CLICKUP_LIST_IDS` reach tests; plan:43 vs plan:45) and A-6 (unbounded invalid-page-cap rule; plan:43, source.md:310) are real defects that V3 missed. V1 also got X-002 right in substance: its A-2 recommendation assumes a stop-and-resume works, and the executor supports that.

### Steelman: Variant 2
The strongest form of V2: the round-1 blockers F-01 and F-02 are fixed. The suite runs in Task 14 before the smoke tasks (plan:216-227, plan:231, plan:241), the smoke ACs are evidence-only with pending allowed (plan:236, plan:246), and the token rule is explicit (plan:23, plan:45, plan:50). Every other remaining defect is a clarity or robustness gap that the executor's per-task QA and extras catch or record (sc-implement SKILL.md:132, :152). V2's four findings are all correctly scoped and all survived calibration as minor. Q-3 correctly recognises the plan's deliberate, docstring-disclosed narrowing (plan:129). Q-2 correctly treats `--limit 200` as a disclosed addition (plan:92). Under the binding severity rule, PASS with notes is a coherent position if no safety finding survives.

### Key Strengths Claimed (numbered, with citations)
1. **S-5 (permissionMode trap) is real and verified.** plan:56 says "Follow the frontmatter shape of existing agents such as `src/superclaude/agents/evidence-validator.md`", and that file carries `permissionMode: plan` (evidence-validator.md:8). A worker copied with that key would be in plan mode, so it would fail to write `.dev/issues/<N>/...`. Every claim would then end in `E-WORKER-NO-OUTPUT` (source.md:335). The Task 3 test (plan:58) does not assert the key is absent. It stays minor, because plan:56 lists the fields to set and the test would not catch the trap, but no other card saw it.
2. **S-7 (the proxy rewrites the tier) is real.** local-gateway-alias-proxy.py:17-21 sends a tier request to "the tier's first model that is not cooling down" and resends to the next one. So an external log or transcript may show a member model, not `claude-gw-tier3`. plan:236 requires "the picker ID it shows". A truthful served row may therefore fail the literal AC. Minor.
3. **S-4 (env conflict) can actually trip QA.** plan:23 forbids `env` on the token, and plan:50 runs `env -u CLICKUP_API_TOKEN ...`. The executor's reviewer treats any byte-present Constraints text as a `quoted-constraint-breach` (qa.md:52, qa.md:61), which is a blocking route. So the plan's own AC can be quoted against itself. Minor, but it is the more consequential half of C-005.
4. **S-1 has the right instance (C-003).** Task 6 requires "the full error table of source section 14" (plan:111). That table has `` `gh issue edit --add-assignee` fails `` and `` `gh issue create` fails `` with no `--repo` (source.md:336, source.md:340). Task 7's scan flags "every line ... that runs `gh issue` ... carries `--repo`" (plan:131), and its negative case is a bare `gh issue view` line (plan:136). V1's A-5 examples are weaker. source.md:462 already contains `--repo`, and the placeholder sentence (source.md:319) is not required in SKILL.md. V3 names the content the plan actually forces into SKILL.md. One more point strengthens the case for settling this in the plan: if Task 7's fixer edits SKILL.md to make the test pass, it is editing text another task produced, which qa.md:52 lists as a `quoted-constraint-breach` form.
5. **S-3 (C-007) is the correct dependency finding.** plan:252 says "Depends on: Task 14", but plan:254 cites Task 15 and Task 16 evidence. V1's matching half, "prerequisite says after Task 13 though it depends on Task 14", is not an error. plan:233's session condition (agents synced at Task 13) is a different fact from the task dependency (the suite at Task 14).
6. **S-8, S-9, S-10 and S-12 are accurate, low-cost fixes**, and the calibrator kept every one as minor (reviewer-3-calibration.yaml:12-16). S-8 is the `__pycache__` case: plan:125 says "every file in ... `scripts/`" while plan:115 uses `scripts/*.py`.
7. **S-6 supplies the only safe presence check.** plan:243 says "If the variables are not exported, record ... pending", but gives no way to check without printing. `printenv` and `env` are banned (plan:23). `test -n "${CLICKUP_API_TOKEN:-}"` is the missing mechanism.

### Weaknesses in Variant 1 (numbered, with citations)
1. **A-1's harm path is overstated, and its fix needs a better rationale.** Every `gh` call uses `--repo <R>` with `<R>` taken from origin (source.md:142, source.md:319; plan:111). So if only Wave 0's URL check fails, the run proceeds on `IronbellyOrg/IronClaude` #1. The orchestrator's read-only check found that #1 is a merged pull request (evidence-sheet E4), and Wave 2's `E-NOT-AN-ISSUE` guard (source.md:159) stops before Wave 3's assign (source.md:162). A write on octocat/Hello-World needs a second fault as well: `<R>` derived from the URL, against Task 6's origin_repo.py rule. The finding still stands, because two guards are untested prose and the cost lands on a stranger's public repo. The non-existent-repo URL helps precisely in that second-fault case, since every call then returns 404.
2. **A-2's second half is wrong.** "Prerequisite says after Task 13 though it depends on Task 14" (V1 card line 15) mixes up the agent-load condition with the dependency.
3. **A-5's example is weak.** source.md:462 already contains `--repo`, so it would pass a line scan. The real trip is the required section 14 table (source.md:336, :340).
4. **V1 misses** the `permissionMode: plan` trap (S-5), the tier-proxy evidence gap (S-7) and the Task 17 dependency (S-3).

### Weaknesses in Variant 2 (numbered, with citations)
1. **PASS misses C-001.** V2 never examines plan:254's no-approval live run, although round 1's F-03 asked for approval before any run against a real issue (round-1 merged-verdict.yaml:64).
2. **The self-audit claim "ClickUp posture satisfies section 12" passes over three gaps:** the Task 16 key-path comparison has no method (plan:243), there is no safe presence check (plan:23 vs plan:243), and the test isolation misses two variables (plan:43, plan:45).
3. **Q-4's fix is mostly already in the plan.** plan:254 already says "unless the user approves a run against a test issue at that moment". The only missing piece is an explicit prompt.
4. **V2 misses every executability trap** that V1 and V3 found: S-4, S-5, S-7, S-8, A-4 and A-6.

### Concessions
1. **S-2 is minor, and its central claim is wrong.** "A re-run gives operator review, not re-execution" is false for this case. Q0 writes a start line before Q1 (sc-implement SKILL.md:108-115). A stop in Q1 leaves only that start line. On re-run the resume logic picks the first non-complete task (refs/ledger.md:125-127), and Row S, "Start line only → ... Else A1, as today" (refs/ledger.md:161), re-runs Task 15. Row P (refs/ledger.md:155) needs a `blocked` verdict, which a Q1 stop never writes. The plan is also unchanged, so `E-PLAN-CHANGED` does not fire (ledger.md:231). What remains is a clarity gap, and that is V1's A-2: plan:233 says stop, while plan:236 accepts "pending (with the reason the session could not run it)". Under the executor's closed interrupt list ("No other path may stop automation or prompt the user", qa.md:288), a conforming executor may take the pending exit, so the spawn is skipped but recorded truthfully. No behaviour is wrong and no claim is false, so it is minor. The pause-and-resume text was also round 1's own recommendation (round-1 merged-verdict.yaml:165, F-10, from V3).
2. **S-1 is minor.** It can be satisfied either way: add `--repo <R>` to the table cells, or have Task 7 define "a line that runs gh" as a code span or fenced line that starts with `gh`. That definition keeps the plan:136 negative case working. At worst, Task 7 starts red and Task 7 fixes it.
3. **S-11 is overstated.** Q6 extras already detect and run `make lint` per task (SKILL.md:132, :146). It is minor at most and could be dropped.
4. **V3's verdict basis (S-002) does not hold. V3 missed C-001**, which is the one finding that keeps the verdict FAIL.

### Shared Assumptions (A-001..A-008: ACCEPT/REJECT/QUALIFY + evidence + proposed severity)
- **A-001: ACCEPT (no finding).** source.md:391 defines the section 16 static test as "the spawn rule text ... is present". plan:126 checks exactly that in SKILL.md and every ref. Round 1 rejected the same challenge (round-1 merged-verdict.yaml:284-285, `A-003-ac7-phrase-test`). Reopening it without new evidence would contradict a settled ruling.
- **A-002: QUALIFY (minor).** AC 5 has two halves (source.md:471). plan:254 maps only "item 5's ClickUp half" to Task 2 and Task 16. The first half ("the claim completes and the comment says ClickUp was skipped") needs a full live claim, which means GitHub writes, so it can only be pending under plan:26. The row must exist anyway (plan:257, "nine rows"), so nothing is lost. The risk is that row 5 is marked "run" on the strength of Task 2's no_token output alone, which would make the artifact claim more than it shows. Fix: Task 17 says item 5's first half is pending with its command.
- **A-003: REJECT (minor).** The `/model`-first-line rule appears only in Task 4's body (plan:77). Task 4's ACs (plan:81-85) and Task 7's tests (plan:123-132) never check it, and the executor reviews only the AC block (SKILL.md:85, QUALIFY rule 1). AC 8's offline half (source.md:474) therefore has no check. Fix: add a Task 4 AC, or a Task 7 test, asserting that the first non-empty line of `templates/next-steps.md` is the `/model claude-gw-tier...` line.
- **A-004: QUALIFY (minor).** plan:131 bans the `{owner}/{repo}` placeholder, but nothing asserts that `gh api` paths spell `repos/<R>/` (source.md:319, required at source.md:178). The revision implemented round 1's F-04 recommendation as written (round-1 merged-verdict.yaml:81), so this is a residual gap, not a regression. Other placeholder forms or a repo-less `gh api issues/...` would pass. Fix: Task 7 also asserts that every `gh api` line naming `issues`, `pulls` or `labels` contains `repos/<R>/`.
- **A-005: REJECT (minor).** source.md:361 says origin_repo.py exists "so the parsing is tested code rather than prose", but the URL-vs-origin comparison that produces `E-FOREIGN-REPO` (source.md:143) stays as prose, and Task 1 tests only parsing (plan:34). This is not a missing required deliverable: section 16 does not list it (source.md:394). It is minor, but it is the cleanest fix for C-001. A pure `check_url(url, origin)` function in origin_repo.py, pinned by Task 1, makes AC 4 verifiable offline and removes the need for a live foreign-repo run.
- **A-006: QUALIFY (minor).** plan:26's approval clause covers only "a real GitHub issue". The previous sentence ("stops before any GitHub or ClickUp write ... may run without asking") implies ClickUp writes need asking, but nothing says so. Task 16 asks the user for the test issue URL and task ID (plan:243), which is in-context consent to a self-assignment on a task the user named. However, the script matches across the whole workspace by rule 1 (source.md:306), so the task it assigns may not be the one the user named. Fix: state that the user's reply naming the test task is the approval, and record whether the matched `task_id` equals the named one.
- **A-007: REJECT (minor).** plan:254 needs "a session that has the skill loaded (after Task 13)". That is the same fresh-session premise as plan:233, but with no stop-and-restart instruction. The executor runs tasks in source order and ignores dependencies (SKILL.md:79, :97). If Task 15 takes its pending exit, Task 17 runs in the pre-Task-13 session, so item 4 ends pending, which plan:258 permits. That outcome is harmless and, as it happens, it avoids the C-001 risk. Even so, the plan should say plainly that item 4 runs only in the post-Task-13 session, otherwise pending.
- **A-008: ACCEPT (no finding).** pytest is a main dependency (pyproject.toml:34-43), and `uv run` syncs main dependencies in the new worktree. `addopts` needs no extras (pyproject.toml:112-116). No test imports scipy or pytest-benchmark (Grep over tests/: no match). The sampled `.claude/` references in tests are string literals (test_sc_recommend_routing_contract.py:57, :154; test_implement_severity_static.py:496), not reads of the gitignored dev copies. The calibrator's environment worry is not supported by evidence. The residual risk is an offline package download, which is environmental.

### Position Table
| Point | Winner | Disposition | One-line reason with a citation |
|---|---|---|---|
| S-001 | none | reject | Card schema and key style only; no plan defect (diff-analysis L1). |
| S-002 | V1 | reject | Structural. V1's FAIL basis (A-1) survives calibration (reviewer-1-calibration.yaml:5); V3's basis (S-1, S-2) does not (reviewer-3-calibration.yaml:5-6). |
| C-001 | V1 | blocking | plan:26 and plan:254 run a live claim against a real third-party repo without asking, guarded only by untested prose (plan:32-38); this reverses round-1 F-03's "ask the user before any run against a real issue" (round-1 merged-verdict.yaml:64). Fix: non-existent IronbellyOrg repo URL, plus approval or an A-005 test. |
| C-002 | V1 | minor | Two exits, stop (plan:233) vs pending (plan:236). Resume works through Row S (refs/ledger.md:161), so V3's "cannot work" is refuted; pick one exit. |
| C-003 | V3 | minor | Task 6's mandated section 14 table (plan:111; source.md:336, :340) puts `--repo`-less `gh issue` mentions into SKILL.md, which plan:131 flags. Satisfiable: Task 7 defines "runs gh" as code spans and fenced lines (merge V1 A-5 scoping). |
| C-004 | V1 | minor | plan:243 names no key-path method. Merge V1's curl -v/-i/--trace ban and already_assigned allowance with V3's `test -n "${CLICKUP_API_TOKEN:-}"` presence check (plan:23 bans printenv/env). |
| C-005 | V3 | minor | plan:23 vs plan:50 is a byte-quotable `quoted-constraint-breach` (qa.md:52, :61). Merge V1 A-4: delenv all four CLICKUP_* variables (plan:43, plan:45). |
| C-006 | V2 | minor | Pending is accepted by plan:15; plan:254 already allows approval "at that moment". Q-4 only adds an explicit request, so it is advisory. |
| C-007 | V3 | minor | plan:252 "Depends on: Task 14" vs plan:254 citing Task 15 and 16 evidence; metadata only, since the executor ignores dependencies (SKILL.md:79). V1's "after Task 13" half is not an error. |
| X-001 | V1 | blocking | FAIL. It rests on C-001 alone; V3's S-1 and S-2 basis is conceded minor, and V2's PASS misses C-001 (plan:26, plan:254, plan:259). |
| X-002 | V1 | minor | Yes, resume works: Q0's start line (SKILL.md:108-115) plus Row S "Else A1" (refs/ledger.md:161) re-runs Task 15; only the stop-vs-pending ambiguity remains. |
| A-001 | none | reject | ACCEPT: source.md:391 defines the static test as phrase presence and plan:126 matches; round 1 rejected the same challenge (merged-verdict.yaml:284-285). |
| A-002 | new | minor | QUALIFY: plan:254 maps only AC 5's ClickUp half; the first half (source.md:471) needs a live claim, so the plan should state it is pending. |
| A-003 | new | minor | REJECT: the next-steps `/model` first-line rule (plan:77) is in no Task 4 AC (plan:81-85) or Task 7 test, and QA checks only the AC block (SKILL.md:85). |
| A-004 | new | minor | QUALIFY: plan:131 bans `{owner}/{repo}` but never asserts that `gh api` paths spell `repos/<R>/` (source.md:319, :178). |
| A-005 | new | minor | REJECT: the URL-vs-origin comparison (source.md:143) is untested (plan:34); a Task 1 pure-function test makes AC 4 checkable offline and is the clean fix for C-001. |
| A-006 | new | minor | QUALIFY: plan:26's approval clause covers GitHub only; Task 16's PUT (plan:243) relies on the user naming the task, and the workspace-wide match (source.md:306) may hit a different task. |
| A-007 | new | minor | REJECT: plan:254 needs the plan:233 fresh-session premise without a restart instruction; in source order (SKILL.md:97) item 4 likely ends pending (plan:258). |
| A-008 | none | reject | ACCEPT: pytest is a main dependency (pyproject.toml:34-43), addopts needs no extras (:112-116), and no test imports dev extras, so a fresh worktree runs it. |


## Round 2: Rebuttals

## Round 2 Rebuttal: Variant 1 (reviewer-1, sonnet:analyzer)

Summary: on re-reading the cited lines against the binding severity rule, I move C-001 from blocking to minor. It is the highest-priority minor, and its fix must be applied before Task 17's item-4 run. With C-001, C-002 and C-003 all minor, X-001 becomes PASS with notes. I also hand C-003 to V3 and accept A-006 as minor.

### Response to Criticisms

**From V2 (round1-v2.md:20-25)**

1. **"A-1 is over-graded as blocking" (round1-v2.md:20-23). Conceded, with one correction.**
   - An escaped write needs two faults. First, the Wave 0 URL check must fail (source.md:143). Second, either the `--repo <R>` rule (source.md:319) or the Wave 2 pull-request stop (source.md:159) must also fail.
   - The `--repo` rule is more than prose. Task 7 scans every `gh issue|pr|label` line for `--repo` (plan:131). Task 6's AC requires every STOP code, including `E-FOREIGN-REPO` and `E-NOT-AN-ISSUE`, to be present in SKILL.md (plan:116). So the octocat path needs the orchestrator to break the text at run time, not an authoring slip.
   - Correction: the Wave 2 barrier is weaker than V2 says. See New Evidence N2.
   - Even so, the realistic outcome is a self-assignment and two comments on merged pull request #1 (E4) of the user's own fork. That is reversible and attributed to the user. Nothing is deleted and no secret is printed, so it is neither "security/data-loss" nor "wrong behaviour" under the binding rule. Final position: minor.
2. **"A-2 under-evidenced" (round1-v2.md:24). Conceded.** My card cited only SKILL.md:135. Round 1 added the resume path: Q0 writes a start line (SKILL.md:108-115) and Row S re-runs the task (refs/ledger.md:161).
3. **"Missed A-003, A-004 and the C-006 posture" (round1-v2.md:25). Conceded.**
   - My card missed A-003 and A-004. I recorded both as minor in Round 1.
   - On C-006, my card accepted the pending posture. Q-4's explicit request adds only a little over plan:254.

**From V3 (round1-v3.md:21-25)**

1. **"A-1 harm path overstated; the non-existent-repo URL helps only in the second-fault case" (round1-v3.md:22). Agreed on both halves.**
   - A non-existent repo URL protects only against the case where the run ignores `--repo`, and Task 7 already guards that text (plan:131).
   - It does nothing for the realistic escape, which runs on origin `<R>` with `N` parsed from the URL (source.md:142-143, reviewer-1-calibration.yaml:5).
   - The fix below changes the number as well as the repo.
2. **"A-2's second half is wrong" (round1-v3.md:23). Conceded already** (round1-v1.md:76). plan:233's "after Task 13" is the condition for the agents to load. It is not the dependency.
3. **"A-5's example is weak" (round1-v3.md:24). Conceded.** source.md:460 carries `--repo` in the flags column, so it passes a line scan. The real trigger is the section-14 table rows source.md:336 and source.md:340, which Task 6 must copy (plan:111). The calibrator says the same (reviewer-1-calibration.yaml:9). C-003 therefore goes to V3.
4. **"V1 misses S-5, S-7, S-3" (round1-v3.md:25). Conceded already** (round1-v1.md:78-84).

### Contested Points (C-001/X-001, A-006, A-007) with final position and evidence

**C-001 / X-001: final disposition is minor (the top-priority minor). X-001 becomes PASS with notes.**

*Why the current plan text is a real defect:*
- plan:26 exempts item 4 from approval on the strength of its intended behaviour ("stops before any GitHub or ClickUp write").
- plan:254 runs it live as `/sc:issue --claim https://github.com/octocat/Hello-World/issues/1`.
- The comparison that is supposed to stop it has no deterministic test (plan:32-38; E7).
- plan:259's AC ("No GitHub issue was assigned ... without the user's approval") is therefore not guaranteed by any mechanism.
- The revision departs from round-1 F-03, "ask the user before any run against a real issue" (E6).

*Why it is still not blocking:*
- **Path A, origin `<R>` with N = 1.** If Wave 0 fails, `<R>` is still origin (source.md:142, :319) and N = 1. Origin #1 is a merged pull request with no assignees (E4). Wave 2 then has to miss that it is a pull request (source.md:159) before Wave 3 assigns (source.md:162) and Wave 6 comments (source.md:178-179). Wave 2's guard is also untested prose, and its input is thin (N2). So path A needs two prose faults. Its worst result is a reversible, self-attributed assignment and two comments on the user's own fork.
- **ClickUp in path A.** If the user exported the variables (E5) and both prose faults occur, rule 2 could self-assign one real workspace task whose name contains `#1` (source.md:307). A unique match is needed; ambiguity means no PUT (source.md:308). That is reversible and self-attributed.
- **Path B, a write on octocat.** This needs a third fault on top of path A: the orchestrator ignores the `--repo <R>` text that Task 7 pins (plan:131).
- **Stale session.** If the session predates Task 13, the Wave 1 worker (source.md:147) cannot produce `scout.md`, so the run stops at `E-WORKER-NO-OUTPUT` before Wave 3 (source.md:335).
- None of these is a security risk, data loss, a false claim or a missing deliverable. Under the binding rule that makes it minor.

*Recommended fix (removes the risk by mechanism, not by prose):*
1. **Change the item-4 URL.** Use a foreign URL whose issue number cannot exist on origin, for example `https://github.com/IronbellyOrg/issue302-no-such-repo/issues/999999999`. AC 4 only needs "any repo other than origin" (source.md:470).
   - On path A, every escaped `gh issue edit` or `gh issue comment` targets origin #999999999, which does not exist. Each write is therefore expected to fail. I did not run this, under the no-gh rule.
   - The assign fails first, so `E-ASSIGN-FAILED` stops the run before ClickUp (source.md:162, :336).
   - Even if that stop were ignored, rule 2's `#999999999` has no plausible task match.
   - On path B, the repo does not exist.
2. **A-005.** Put the URL-vs-origin comparison into origin_repo.py, for example a `--check-url` mode that Wave 0 calls in place of prose. Pin it in Task 1 with three tests: a same-repo URL, a foreign URL, and owner/repo case. AC 4's logic can then be checked offline.
3. **Fallback.** If the executor cannot apply step 1, it asks for the user's approval at that moment, as plan:26 requires for any other live claim.

With steps 1 and 2, plan:26's carve-out is true by mechanism and plan:259 holds. The calibrator's warning that a non-existent repo alone does not remove the risk (reviewer-1-calibration.yaml:5) is answered by changing the number.

**A-006: changed from reject to minor (winner V2).**
- I accept V2's and V3's point. The user names a task ID (plan:243), but the script picks its target by a workspace-wide match (source.md:304-309), not by that ID.
- If the test task does not actually link the test URL, rule 2's `#<N>` (source.md:307) can self-assign a different real task.
- Task 16's AC records "the test task ID" (plan:246) but never compares it with the `task_id` the script reports.
- Fix: the user's reply naming the task is the approval. After the first run, compare the reported `task_id` with the named ID and record the result. On a mismatch, run no second time and report it.
- Minor: the write is reversible and self-attributed.

**A-007: minor (unchanged); I reject V2's "no finding".**
- V2 argues that item 4 "stops in Wave 0 before any spawn" (round1-v2.md:47). That assumes the very guard C-001 questions.
- plan:254 itself requires "a session that has the skill loaded (after Task 13)" and gives no precondition check. plan:258 requires the item-4 row to come "from a real run".
- An executor in a stale session can narrate a run by reading SKILL.md and record `E-FOREIGN-REPO`. That would be a false claim in the artifact, and no AC detects it.
- plan:258's pending exit keeps a truthful executor safe, which is why this is minor.
- Fix: state the same session precondition as plan:233, and say that a read-through or simulated run is not evidence.

### Updated Assessment of Other Variants

- **V2.** Its PASS verdict is correct under the binding rule. V2 still never raised C-001 (variant-2-original.md), and its own Round 1 concedes that a finding must survive (round1-v2.md:35). V2's "two independent guards" overstates the Wave 2 barrier (N2), but the conclusion stands. V2 is the strongest variant on severity calibration.
- **V3.** I now disagree with V3's blocking grade on C-001 (round1-v3.md:54). V3's own analysis (round1-v3.md:22) ends at the same double-fault structure. V3 holds the better instance on C-003 and the better dependency finding on C-007, and it alone found S-5 and S-7. V3 conceded S-1 and S-2 correctly.

### New Evidence

- **N1.** plan:116 (Task 6 AC) requires every STOP code in SKILL.md, and plan:131 (Task 7) pins `--repo` on every gh line. Authoring omissions of the two guards and of `--repo` are therefore caught mechanically. The residual risk is non-compliance at run time only.
- **N2.** The Wave 2 pull-request guard is thinner than V2 states.
  - `scout.md` records `state`, assignees, login, comment IDs, merged PRs and guesses (source.md:151). It records no "is a pull request" flag and no URL.
  - The only explicit state stop is `CLOSED` (source.md:155), while origin #1 reports `MERGED` (E4).
  - So `E-NOT-AN-ISSUE` (source.md:159) depends on the orchestrator inferring "pull request" from `MERGED`. This is why the fix must not rely on Wave 2.
- **N3.** source.md:162 and :336 stop with `E-ASSIGN-FAILED` "before ClickUp and before any comment". With a non-existent N, the first write fails and the ordering keeps ClickUp untouched, which closes the E5 exposure in path A.
- **N4.** source.md:289 calls the script with `--issue-url <url>` but does not say whether that is the user's argument or `https://github.com/<R>/issues/<N>`. In an escaped run this decides whether rule 1 can match. With the fix, rule 1 and rule 2 both lack a plausible match either way.
- **N5.** source.md:336 and :340 have no `--repo`, while source.md:460 does. This confirms V3's C-003 instance over my A-5 example.

### Updated Position Table

| Point | Winner | Disposition | One-line reason with a citation |
|---|---|---|---|
| S-001 | none | reject | Card schema and key differences are format only; no plan defect (diff-analysis.md:19). |
| S-002 | none | reject | The verdict basis follows from the C-001..C-003 rulings, not from finding counts; no separate finding. |
| C-001 | V1 | minor | plan:26/254 exempt a live claim by intent and plan:259 is unguaranteed, but a write needs two prose faults (source.md:143, :159) and lands reversibly on the user's fork PR #1 (E4); fix: a foreign URL with a non-existent N plus an A-005 check in origin_repo.py, else approval. |
| C-002 | V1 | minor | Resume works via Q0 and Row S (sc-implement SKILL.md:108-115, refs/ledger.md:161); the defect is plan:233 vs plan:236 offering two exits. |
| C-003 | V3 | minor | Task 6's mandated table rows source.md:336, :340 lack `--repo` and trip plan:131; satisfiable by adding `--repo <R>` or scoping "runs gh" to code; at worst a red test fixed under plan:135. |
| C-004 | V1 | minor | plan:243 names no method; ban `curl -v/-i/--trace`; accept `already_assigned` on the first run (plan:246); merge V3's `test -n "${CLICKUP_API_TOKEN:-}"`. |
| C-005 | V1 | minor | plan:45 clears 2 of the 4 CLICKUP_* variables plan:43 reads; merge V3's S-4 (plan:23 vs plan:50 `env -u`). |
| C-006 | V2 | minor | Pending ACs are truthful (plan:15, plan:258); Q-4's explicit pre-approval request adds a little over plan:254. |
| C-007 | V3 | minor | plan:252 omits Tasks 15 and 16 cited at plan:254; metadata only (SKILL.md:79). |
| X-001 | V2 | minor | PASS with notes: C-001, C-002 and C-003 are all minor under the binding rule; round-1 F-01/F-02 fixed (plan:216-227, plan:23, :45, :50); C-001's fix is a precondition of Task 17's item-4 run. |
| X-002 | V1 | minor | Yes: a pre-verdict stop leaves a start line and Row S re-runs it (refs/ledger.md:161); clarify which exit wins. |
| A-001 | none | reject | source.md:391 defines the static test as phrase presence; plan:126 matches; round 1 rejected the same challenge. |
| A-002 | new | minor | AC 5's first half (source.md:471) is unplaced in plan:254; name it pending and do not mark it run on Task 2's no_token output (plan:50). |
| A-003 | new | minor | AC 8's `/model` first line (source.md:474) is defined at plan:77 but unasserted in plan:81-85 and plan:123-132. |
| A-004 | new | minor | plan:131 bans the placeholder but never asserts `gh api` paths spell `repos/<R>/` (source.md:319). |
| A-005 | new | minor | The URL-vs-origin comparison (source.md:143, AC 4 source.md:470) is untested (plan:32-38); an origin_repo.py check called in Wave 0 is half of C-001's fix. |
| A-006 | V2 | minor | The user names a task ID (plan:243) but the workspace-wide match (source.md:304-309) picks the PUT target; compare the reported `task_id` with the named one before the second run. |
| A-007 | new | minor | plan:254 needs a post-Task-13 session with no precondition check; a read-through "run" would falsely satisfy plan:258; V2's "stops in Wave 0" assumes the guard under test. |
| A-008 | none | reject | `uv run` syncs main dependencies including pytest (pyproject.toml:34-43); only failing tests are compared on master (plan:220). |


## Round 2 Rebuttal: Variant 2 (reviewer-2, haiku->glm-5.3:qa)

Summary: PASS with notes stands, and V1 now holds the same verdict (round2-v1.md:3, :101). I keep C-001 at minor, but I concede that my Round 1 "two or three independent guard failures" overstated the Wave 2 barrier (V1's N2 is correct). Path A needs one Wave 0 prose fault plus one Wave 2 check that has to be inferred. C-001 is the top-priority minor, and its fix is a precondition of Task 17's item-4 run. I move A-007 from reject to minor. I confirm A-006 as minor. I hand C-003 and C-007 to V3.

### Response to Criticisms

**From V1 (round1-v1.md:49-55)**

1. **"PASS asserted, not argued; silent on item 4, the Task 15 dual exit and Task 6/7" (round1-v1.md:51). Conceded on coverage, not on the verdict.**
   - My card raised none of C-001, C-002 or C-003 (variant-2-original.md:7-11).
   - The self_audit says it "audited spec sections 4, 7, 8 ..." (variant-2-original.md:13). That is a process claim the findings do not back for section 7 Wave 0 (source.md:141-145). It was overstated.
   - The verdict itself survives. With all three points ruled minor under the binding rule, PASS with notes is the outcome both V1 (round2-v1.md:101) and V3's calibrator (reviewer-3-calibration.yaml:19, cited in round1-v2.md:13) reach.
2. **"'ACs observable' is a false self-audit claim" (round1-v1.md:52). Conceded.**
   - AC 5's first half (source.md:471) is not placed in plan:254.
   - AC 8's offline half (source.md:474) has no AC or test (plan:77 vs plan:81-85 and plan:123-132).
   - My calibrator lists both (reviewer-2-calibration.yaml:11-12). I carry both as A-002 and A-003, minor.
3. **"Q-2 and Q-3 are non-findings" (round1-v1.md:53). Conceded on the label, not on the value.**
   - Both are round-1-directed additions: `--limit 200` at plan:92 and plan:105, and the source-only narrowing at plan:129, which the plan discloses in the test docstring.
   - Under the deviation taxonomy they are Authorized expansions with no action, and the merged verdict should record them that way. Recording a sanctioned deviation is part of classifying deviations, so it is not padding.
   - Q-1 duplicates plan:25 and can be dropped.
4. **"Q-4 partly duplicates plan:254" (round1-v1.md:54). Partly conceded. New evidence keeps it a live minor (N2 below).**
   - plan:254 says "unless the user approves a run ... at that moment", but no step tells the executor to ask.
   - The executor's interrupt list is closed: "No other path may stop automation or prompt the user" (refs/qa.md:288). Minors are recorded "no user prompt" (refs/qa.md:274).
   - So "at that moment" has no defined trigger, and the approval clause most likely never fires. Truthful pending rows are the safe result, but core ACs 1, 2, 3, 6 and 8 then ship with no live run.
   - An explicit request at the end of Task 17 is the missing trigger.
5. **"ClickUp posture approved without checking the shared session" (round1-v1.md:55). Conceded.** I conceded this in Round 1 (round1-v2.md:37). The exported variables (plan:23, plan:243) reach an escaped item-4 run. C-001's fix closes that path.

**From V3 (round1-v3.md:27-31)**

1. **"PASS misses C-001" (round1-v3.md:28). Conceded** (round1-v2.md:35). Severity is argued under Contested Points.
2. **"The ClickUp self-audit passes over three gaps" (round1-v3.md:29). Conceded.** The three gaps are no key-path method (plan:243), no safe presence check (plan:23 vs plan:243), and 2 of 4 variables cleared (plan:43 vs plan:45). These are C-004 and C-005.
3. **"Q-4's fix is mostly in the plan" (round1-v3.md:30).** My answer is item 4 under V1: the plan has no prompt trigger, and the executor forbids unlisted prompts (refs/qa.md:288).
4. **"V2 misses every executability trap" (round1-v3.md:31). Conceded.** S-4, S-5, S-7, S-8, A-4 and A-6 are not in my card. My coverage_completeness (0.70) and risk_surface_coverage (0.65) reflect that (reviewer-2-calibration.yaml:2).

**Claims of mine that hold on re-reading**

- All nine STOP codes are named in Task 6 (plan:111), and Task 6's AC requires them (plan:116).
- Resume after a stop before any verdict: Q0 reuses the start line (sc-implement SKILL.md:108-109), and Row S re-runs the task "Else A1, as today" (refs/ledger.md:161). Row P needs a `blocked` verdict (refs/ledger.md:155).
- The executor ignores depends-on (SKILL.md:79) and runs tasks in source order (SKILL.md:97).
- V1 (round2-v1.md:14) and V3 (round1-v3.md:34) both accepted these points.

### Contested Points (C-001/X-001, A-006, A-007) with final position and evidence

**C-001 / X-001: final position minor (the top-priority minor). X-001 is PASS with notes.**

*Correction of my Round 1 argument (I accept V1's N2):*
- Wave 1's query does fetch `url` (source.md:148). But the `scout.md` that Wave 2 reads records only state, assignees, login, comment IDs, merged PRs and guesses (source.md:151). It has no pull-request flag and no URL.
- The only explicit state stop is `CLOSED` (source.md:155). Origin #1 reports `MERGED` (evidence-sheet E4).
- So `E-NOT-AN-ISSUE` (source.md:159) fires only if the orchestrator infers "pull request" from `MERGED`.
- My Round 1 phrase "two or three independent guard failures" (round1-v2.md:23) is withdrawn. Path A needs one Wave 0 prose fault (source.md:143) and one Wave 2 inference to be missed. Path B, writing on octocat, also needs the orchestrator to drop `--repo <R>`, which Task 7 pins in the text (plan:131).

*Why it stays minor under the binding rule:*
- **No security or data-loss risk.** The worst path-A result is a self-assignment plus two comments on the user's own merged fork PR #1 (E4; source.md:162, :178-179). The possible ClickUp result is one self-assignment on a uniquely matched task (source.md:307-308). Both are reversible and attributed to the user. Nothing is deleted and no secret is printed (plan:23).
- **No false claim in a deliverable.** plan:254's "stops in Wave 0 before any GitHub or ClickUp write" is what the spec requires (source.md:143, :329). It is the behaviour under test, not a false statement.
- **No silent wrong behaviour.** An escaped write would breach a quoted Constraints line (plan:17, plan:26). That is a `quoted-constraint-breach` (refs/qa.md:52, :61; SKILL.md:93), and it also fails plan:259's AC. The reviewer would block the task. This is detection after the write, not prevention, which is why the fix must come first.
- **Still a real defect.** plan:26 classifies the run by its intended outcome, it departs from round-1 F-03 (E6), and nothing guarantees plan:259 beforehand (E7: Task 1 tests parsing only, plan:32-38).

*Endorsed fix (V1's, with one QA addition):*
1. **Replace the item-4 URL** with a foreign URL whose repo and issue number cannot exist on origin, for example `https://github.com/IronbellyOrg/issue302-no-such-repo/issues/999999999`. AC 4 only needs "any repo other than origin" (source.md:470).
   - On path A, Wave 1's `gh issue view 999999999 --repo <R>` has nothing to return. Any escaped assign fails and stops with `E-ASSIGN-FAILED` before ClickUp and before any comment (source.md:162, :336). Rule 2's `#999999999` has no plausible match. I did not run this, under the no-gh rule.
   - On path B, the repo does not exist.
2. **A-005:** put the URL-vs-origin comparison in origin_repo.py as a pure function or a `--check-url` mode that Wave 0 calls. Pin it in Task 1 with tests for a same-repo URL, a foreign URL, and owner/repo case. This makes AC 4 checkable offline, because origin_repo.py exists "so the parsing is tested code rather than prose" (source.md:361).
3. **QA addition (from A-007):** the item-4 row must quote the run's actual output, and a read-through or simulated run is not evidence.
4. **Fallback:** if steps 1 and 2 are not applied, item 4 runs only with the user's explicit approval at that moment, otherwise it is pending.

**A-006: minor (confirmed; winner V2).**
- Task 16 asks the user for the test issue URL and task ID (plan:243), but the script picks the PUT target by a workspace-wide match (source.md:304-309), not by that ID.
- Task 16's AC records "the test task ID" (plan:246) but never compares it with the `task_id` the script reports (source.md:309).
- Fix: the user's reply naming the task is the approval. Compare the reported `task_id` with the named one after the first run. On a mismatch, do not make the second run, and report it.
- Minor: the write is reversible and self-attributed. V1 (round2-v1.md:58-63) and V3 (round1-v3.md:45) agree.

**A-007: changed from reject to minor.**
- My Round 1 reason, "item 4 stops in Wave 0 before any spawn" (round1-v2.md:47), assumes the very guard that C-001 questions. V1 is right on that (round2-v1.md:66).
- plan:254 makes "a session that has the skill loaded (after Task 13)" a precondition with no check and no restart path. Task 15 has one (plan:233).
- plan:258 requires "a real run", and no AC can tell a real run from one narrated by reading SKILL.md.
- A narrated `E-FOREIGN-REPO` row would be a false statement in the acceptance record (refs/qa.md:50 `false-claim`), and the reviewer could not detect it.
- The pending fallback (plan:258) keeps a truthful executor safe, and per V3 (round1-v3.md:46) source order often leaves item 4 pending anyway. So it is minor.
- Fix: the same session precondition as plan:233, plus the evidence rule in step 3 of the C-001 fix.

### Updated Assessment of Other Variants

- **V1.** V1 moved C-001 to minor (round2-v1.md:31) on the same severity grounds I argued in Round 1. Its N2 legitimately corrects my overstatement of the Wave 2 barrier. Its revised fix, which changes the issue number as well as the repo, answers the calibrator's objection (reviewer-1-calibration.yaml:5) and is the fix I endorse. V1 remains the strongest card on risk surface and on checking the round-1 fixes.
- **V3.** V3's blocking grade on C-001 (round1-v3.md:54) now stands alone. V3's own harm analysis (round1-v3.md:22) reaches the same two-fault, own-fork outcome, and the binding rule does not grade it blocking. V3 holds the better instance on C-003 (source.md:336, :340 forced into SKILL.md by plan:111) and the better dependency finding on C-007 (plan:252 vs plan:254). It alone found S-5 and S-7. Its use of qa.md:52 for S-4 is sound.

### New Evidence

- **N1. Q-4 / C-006 gains a mechanism.**
  - refs/qa.md:274 says minors carry "no user prompt", and refs/qa.md:276-288 is a closed list of interrupts ending "No other path may stop automation or prompt the user".
  - plan:26 and plan:254 make live runs depend on "approval at that moment", and no task step tells the executor to ask.
  - The approval clause is therefore safe by default (no ask means pending), but it never fires on its own. An explicit end-of-Task-17 request is needed if any of ACs 1, 2, 3, 6 or 8 is to run.
  - The same fact means C-001's fallback ("else approval") is safe. That fallback defaults to pending, and only the item-4 carve-out runs live without an ask.
- **N2. An escaped write is detected afterwards, not prevented.**
  - plan:17 heads `## Constraints`, so plan:26 is a quotable constraint (SKILL.md:93; refs/qa.md:52, :61).
  - plan:259 is an AC.
  - An escaped write therefore blocks Task 17 in review. That keeps C-001 out of "silent wrong behaviour", but the write would already have happened.
- **N3. Wave 2's input lacks the pull-request signal.** Wave 1 fetches `url` (source.md:148), but the scout.md field list (source.md:151) does not carry it forward. This confirms V1's N2 from the other side: a one-line fix to the spec template would make `E-NOT-AN-ISSUE` direct. That fix is out of this plan's scope, so it is noted only.

### Updated Position Table (all 19 rows, same columns as Round 1)

| Point | Winner | Disposition | One-line reason with a citation |
|---|---|---|---|
| S-001 | none | reject | Card schema and YAML style differences carry no finding (diff-analysis.md:19). |
| S-002 | V2 | reject | Granularity is not a finding; the verdict basis is settled under X-001 (V3's S-1/S-2 basis conceded minor, round1-v3.md:34-35). |
| C-001 | V1 | minor | plan:26/254 exempt a live claim by intent and plan:259 is unguaranteed (plan:32-38), but path A needs a Wave 0 fault plus a missed Wave 2 inference (source.md:143, :151, :155, :159) and lands reversibly on the user's fork PR #1 (E4); fix: foreign URL with non-existent repo and N, A-005 check in origin_repo.py, real-output evidence, else approval. |
| C-002 | V1 | minor | Two exits at plan:233 vs plan:236 are a clarity gap; resume works via Q0 and Row S (SKILL.md:108-109, refs/ledger.md:161). |
| C-003 | V3 | minor | Task 6's mandated table rows source.md:336, :340 lack `--repo` and trip plan:131; satisfiable by `--repo <R>` in the rows or scoping "runs gh" to code; at worst a red test fixed under plan:135. |
| C-004 | V1 | minor | Task 16 names no key-path method and the first-run `assigned` AC fails if already assigned (plan:243, plan:246); merge V3's `test -n "${CLICKUP_API_TOKEN:-}"`. |
| C-005 | V1 | minor | Tests clear 2 of 4 CLICKUP_* vars (plan:45 vs plan:43); merge V3 S-4 (plan:23 vs plan:50, quotable under refs/qa.md:52). |
| C-006 | V2 | minor | ACs 1, 2, 3, 6, 8 may all end pending (plan:15, plan:254), and the executor never prompts outside its closed list (refs/qa.md:274, :288); add one explicit pre-approval request. |
| C-007 | V3 | minor | plan:252 "Depends on: Task 14" omits Tasks 15 and 16 cited at plan:254; metadata only (SKILL.md:79); "after Task 13" at plan:233 is the agent-load condition, not an error. |
| X-001 | V2 | minor | PASS with notes: C-001, C-002, C-003 all minor under the binding rule; round-1 F-01/F-02 fixed (plan:216-227, plan:23, :45, :50); C-001's fix gates Task 17's item-4 run. |
| X-002 | V1 | minor | Yes: a stop before review leaves a start line only (SKILL.md:108-115) and Row S re-runs the task (refs/ledger.md:161); Row P needs a blocked verdict (refs/ledger.md:155). |
| A-001 | none | reject | ACCEPT: source.md:391 defines the static test as phrase presence; plan:126 matches; round 1 rejected the same challenge. |
| A-002 | new | minor | QUALIFY: AC 5 first half (source.md:471) unnamed in plan:254; do not mark it run on Task 2's script-only check (plan:50). |
| A-003 | new | minor | REJECT: next-steps.md first-line rule (source.md:474, plan:77) has no AC or test (plan:81-85, plan:123-132). |
| A-004 | new | minor | QUALIFY: scan omits `gh api` paths spelling `repos/<R>/` (source.md:319 vs plan:131). |
| A-005 | new | minor | REJECT: URL-vs-origin comparison is untested prose (source.md:143, 361; plan:32-38); a pure-function test is the deterministic half of C-001's fix. |
| A-006 | V2 | minor | QUALIFY: the user names a task ID (plan:243) but the workspace-wide match picks the PUT target (source.md:304-309); compare reported `task_id` before the second run (plan:246). |
| A-007 | new | minor | REJECT (changed): plan:254's post-Task-13 precondition has no check or restart path unlike plan:233, and a narrated run would falsely satisfy plan:258 (refs/qa.md:50); my "stops in Wave 0" assumed the guard under test. |
| A-008 | none | reject | ACCEPT: pytest is a main dependency and uv run syncs it (pyproject.toml:34-43, 112-116); no test needs dev extras. |


## Round 2 Rebuttal: Variant 3 (reviewer-3, opus:refactorer)

Summary: I re-read every line my Round 1 C-001 position rested on and applied the binding severity rule. **I concede C-001 to minor and X-001 to PASS with notes.** C-001 stays the top-priority minor, and its fix gates Task 17's item-4 run. The defect is real: plan:26 exempts the run because of what it is meant to do, and no mechanism guarantees plan:259. But the worst escaped result is a reversible write the user made on their own fork. That is none of the four blocking triggers. I also correct one mechanism I cited in Round 1 (qa.md:52 applies to the diff), hand C-005 to V1, and accept V2 as the winner of A-006.

### Response to Criticisms

**From V1 (round1-v1.md:57-67)**

1. **"S-2 is over-graded; its own evidence refutes it" (round1-v1.md:59). Conceded in Round 1 (round1-v3.md:34).**
   - Re-verified. Row S is "Start line only → ... Else A1, as today" (refs/ledger.md:161), so the task re-runs.
   - Row P needs "Latest verdict is `blocked`" (refs/ledger.md:155), and a stop before review never writes one.
2. **"S-1 is over-graded" (round1-v1.md:60-63). Conceded** (round1-v3.md:35). It is minor, at worst a red test that Task 7 fixes under plan:135.
3. **"V3 misses the live-write exposure" (round1-v1.md:64). Conceded.**
   - My card cited plan:254 for S-3 and never questioned the item-4 run in the same paragraph. That is a coverage miss in the safety focus area.
4. **"S-11 is wrong on its premise" (round1-v1.md:65). Conceded; S-11 is withdrawn.**
   - Q6 extras "Detect and run lint/typecheck/tests if present" (sc-implement SKILL.md:132), and lint detection includes `make lint` (SKILL.md:146).
5. **"S-12 is style only" (round1-v1.md:66). Accepted.** It is correct, but cosmetic: plan:197 lacks backticks, unlike the neighbour heading at docs/user-guide/commands.md:236. Record it as a note, not a finding.
6. **"S-9 changes nothing" (round1-v1.md:67). Accepted.**
   - Interim reds in untouched test files are `unrelated-red`, and an extra `fail` "does not change the spec verdict" (SKILL.md:152-154).
   - Keep it as a note only. The plan could say why reds appear between Task 6/8 and Task 9, but no outcome depends on it.

**From V2 (round1-v2.md:27-32)**

1. **"S-2 is factually wrong" (round1-v2.md:28). Conceded.**
   - "Resume cannot work" was a false statement inside a blocking finding, contradicted by the Row S evidence my own card cited. My calibrator's `deviation_classification_clarity: 0.55` (reviewer-3-calibration.yaml:2) reflects it.
2. **"S-1 is not a contradiction" (round1-v2.md:29). Conceded on severity.** The two tasks conflict only under a literal reading, and it is satisfiable. I keep C-003 as the better instance (see below).
3. **"S-11 overstated" (round1-v2.md:30). Conceded;** S-11 is withdrawn (item 4 above).
4. **"S-3 is cosmetic for this executor" (round1-v2.md:31). Partly conceded.**
   - The executor ignores `depends-on` (SKILL.md:79) and runs in source order (SKILL.md:97), so in this executor nothing breaks.
   - It stays a minor for cross-task consistency. plan:254 consumes Task 15 and Task 16 artifacts, plan:252 declares only Task 14, and another executor, or a reader planning a partial re-run, would be misled.
5. **"S-4 is a wording issue" (round1-v2.md:32). Partly conceded, with a correction to my Round 1 mechanism.**
   - The conflict is literal. plan:23 says "no `echo`, `env`, `printenv` or `set -x` on it", and plan:50 runs `env -u CLICKUP_API_TOKEN ...`.
   - My Round 1 claim that this is a byte-quotable `quoted-constraint-breach` is weaker than I stated. qa.md:52 defines that family as "The diff violates ...", and running an AC command is not a diff line.
   - So the QA trip is unlikely, and S-4 is the lesser half of C-005. Fix: plan:23 should say "no command that prints it; `env -u` to unset it is allowed".

### Contested Points (C-001/X-001, C-003, C-007, A-006, A-007) with final position and evidence

**C-001: final disposition minor (the top-priority minor), conceded from blocking. X-001: PASS with notes.**

*What stays true from my Round 1 case (re-read):*
- plan:26 exempts item 4 because it "stops before any GitHub or ClickUp write", which is the behaviour under test.
- plan:254 runs `/sc:issue --claim https://github.com/octocat/Hello-World/issues/1` live.
- Task 1 tests parsing only (plan:32-38). The comparison "A URL must point at `<R>`" (source.md:143) has no deterministic test.
- So plan:259 ("No GitHub issue was assigned, commented on or created without the user's approval") is hoped for, not guaranteed.
- This reverses round-1 F-03's "ask the user before any run against a real issue" (round-1 merged-verdict.yaml:64, E6).

*Weighing (a), the case for blocking:*
- An escaped write would be a real external write under the user's account.
- If the ClickUp variables are exported in the same session (E5; plan:23, plan:243), rule 2 could match a task named with `#1` as a whole token (source.md:307). It then makes a PUT, provided the match is unique (source.md:308-309).
- The second barrier is thinner than V2 first argued (V1 N2, V2 N3). scout.md carries state, assignees, login, comment IDs, merged PRs and guesses (source.md:151), with no pull-request flag. The only explicit state stop is `CLOSED` (source.md:155), while origin #1 reports `MERGED` (E4). So `E-NOT-AN-ISSUE` (source.md:159) needs an inference.

*Weighing (b), the case for minor:*
- If Wave 0 fails silently, `<R>` is still origin (source.md:142, :319) and N = 1, which is the user's own merged fork PR (E4).
- A write then also needs Wave 2 to miss that inference. The worst result is a self-assignment (source.md:162) and two marked comments (source.md:178-179) on the user's own fork, plus at most one self-assignment on a uniquely matched ClickUp task. All of these are reversible and attributed to the user.
- Nothing is deleted, no secret is printed (plan:23), and no third party is written to unless a third fault drops `--repo <R>`. Task 7 pins `--repo <R>` in the text (plan:131), and Task 6's AC requires `E-FOREIGN-REPO` and `E-NOT-AN-ISSUE` in SKILL.md (plan:116).
- plan:254's "stops in Wave 0" restates the spec requirement (source.md:143, :329). It is the behaviour under test, not a false claim.

*Ruling under the binding rule:*
- (a) shows that the plan's approval logic is wrong *as a rule*, but the consequence is not one of the four blocking triggers.
- The ClickUp path is the strongest part of (a). It is still a self-assignment, it needs the same two faults, and the fix below closes it (source.md:162, :336: `E-ASSIGN-FAILED` "before ClickUp").
- My Round 1 "blocking" read harm against a third-party repo. My own Round 1 analysis (round1-v3.md:22) already showed that path needs a second, separate fault. Concession.

*Endorsed fix (V1's, as amended by V2, plus two refactorer additions for cross-task consistency):*
1. **Change the item-4 URL.** Use one whose repo and issue number cannot exist on origin, for example `https://github.com/IronbellyOrg/issue302-no-such-repo/issues/999999999`. AC 4 needs only "any repo other than origin" (source.md:470).
   - On path A, the first write (`gh issue edit 999999999 --repo <R>`) cannot succeed, so the run stops `E-ASSIGN-FAILED` before ClickUp and before any comment (source.md:162, :336).
   - On path B, the repo does not exist.
   - Not run (no gh in this round).
2. **A-005.** Add a pure URL-vs-origin check (or a `--check-url` mode) to origin_repo.py, pinned in Task 1 with tests for a same-repo URL, a foreign URL and owner/repo case.
   - *Refactorer addition:* Task 6's Wave 0 text must call it, and Task 6's AC must check the call is present in SKILL.md. Otherwise the tested function sits unused beside untested prose.
   - *Deviation classification:* this mode is not in source section 15's origin_repo.py row. Record it in the plan as a disclosed addition justified by source.md:361 ("so the parsing is tested code rather than prose").
3. **Evidence rule (V2's addition, merged with A-007).** The item-4 row quotes the real run output, and it runs only in a post-Task-13 session. Otherwise it is pending, and a read-through or simulated run is not evidence.
4. **Rewrite plan:26's carve-out.** Exempt runs by target, not by intent: "a run whose URL names a repository and issue that do not exist may run without asking".
   - If steps 1 and 2 are not applied, item 4 needs approval at that moment, otherwise it is pending.
   - V2's N1 is correct: the executor never prompts outside its closed list (qa.md:274, :288). So "at that moment" needs an explicit ask step in Task 17, or it defaults to pending, which is safe.

**C-003: minor, winner V3 (confirmed).**
- Task 6 requires "the full error table of source section 14" (plan:111).
- That table has `` `gh issue edit --add-assignee` fails `` (source.md:336) and `` `gh issue create` fails `` (source.md:340), both without `--repo`.
- Task 7 flags "every line ... that runs `gh issue` ... carries `--repo`" (plan:131).
- V1 (round2-v1.md:26, N5) and V2 (round2-v2.md:106) both now hand this instance to V3.
- Fix: put `--repo <R>` in those cells, or define "runs" as code spans and fenced lines starting with `gh`. The second option keeps the plan:136 negative case valid.
- Minor: at worst a red test fixed in Task 7 (plan:135).

**C-007: minor, winner V3 (confirmed).**
- plan:252 "Depends on: Task 14", while plan:254 points items 7, 9 and 5 at Task 15 and Task 16 evidence.
- Metadata only under this executor (SKILL.md:79, :97). Fix: "Depends on: Task 14, Task 15, Task 16".
- V1's "after Task 13" half is not an error. plan:233's phrase is the agent-load condition, not the dependency. V1 conceded this (round2-v1.md:25).

**A-006: minor (QUALIFY), winner now V2 (changed from "new").**
- Re-read: Task 16 asks the user for the test issue URL and task ID (plan:243). The script picks the PUT target by a workspace-wide match (source.md:304-309), not by that ID.
- Task 16's AC records "the test task ID" (plan:246) but never compares it with the reported `task_id`.
- V2 raised the comparison fix first, and V1 accepts V2 as winner (round2-v1.md:108).
- Fix: the user's reply naming the task is the approval. After the first run, compare the reported `task_id` with the named ID, and on a mismatch make no second run and report it.

**A-007: minor (REJECT), winner new (confirmed, scope widened).**
- plan:254 needs "a session that has the skill loaded (after Task 13)" but, unlike plan:233, has no check or restart instruction.
- plan:258 requires "a real run", and nothing tells a real run from one narrated by reading SKILL.md. A narrated row would be a `false-claim` (qa.md:50) that the reviewer cannot detect.
- V2 moved to minor on the same ground (round2-v2.md:72-78).
- Fix: as in C-001 step 3.

### Updated Assessment of Other Variants

- **V1.** V1 is right on both calls that matter: C-001 exists, and it is minor under the binding rule.
  - Its revised fix answers the calibrator's objection that a non-existent repo alone does not remove the risk (reviewer-1-calibration.yaml:5), because it also changes the issue number.
  - V1 is the strongest card on risk surface and on checking the round-1 fixes.
  - On C-005, V1's A-4 (2 of 4 variables cleared, plan:43 vs plan:45) is the substantive half, so V1 wins it.
- **V2.** V2's PASS-with-notes verdict was correct under the binding rule.
  - V2's N1 (qa.md:274, :288: the executor never prompts outside its closed list) is the best new mechanism of Round 2. It shows the "approval at that moment" clause never fires without an explicit step.
  - V2 still had the weakest coverage, and its self-audit overstated its section 7 checks (round2-v2.md:11).
- **V3 (self).** Its strengths are the executability traps no other card found: S-5 `permissionMode: plan` (evidence-validator.md:8, plan:56), S-7 tier rewrite, S-8 and S-6. Its weaknesses are two over-graded blockers, one with a false resume claim, and the C-001 miss.

### New Evidence

- **N1. qa.md:52 scopes `quoted-constraint-breach` to "The diff violates".**
  - This weakens my Round 1 S-4 mechanism: running `env -u` in an AC command is not a diff line.
  - It also qualifies V2's N2: an escaped GitHub write is an external effect, not a diff line, so the review would catch it through plan:259's AC (`ac-outcome-missing`), not through a constraint breach.
  - Either way, detection comes after the write, so the fix must precede the run.
- **N2. Cross-task gap in the A-005 fix.** A check function in origin_repo.py protects nothing unless Task 6 makes Wave 0 call it and an AC pins the call.
  - Task 6's current Wave 0 text names only `origin_repo.py` for resolving `<R>` (plan:111).
  - Task 6's ACs check STOP-code presence (plan:116), not the comparison step.
- **N3. Proposed rewrite of plan:26.** Its exemption rests on what the run is meant to do ("A run that stops before any GitHub or ClickUp write"). Restating it in terms of the target, a repo and issue that do not exist, makes plan:26 and plan:259 true by construction.

### Updated Position Table (all 19 rows, same columns as Round 1)

| Point | Winner | Disposition | One-line reason with a citation |
|---|---|---|---|
| S-001 | none | reject | Card schema and key style only; no plan defect (diff-analysis.md:19). |
| S-002 | none | reject | Neither FAIL basis survives: V3's S-1/S-2 conceded minor (reviewer-3-calibration.yaml:5-6) and V1's A-1/C-001 now minor under the binding rule; the verdict follows X-001. |
| C-001 | V1 | minor | plan:26/254 exempt a live claim by intent and plan:259 is unguaranteed (plan:32-38; E6), but an escape needs a Wave 0 fault plus a missed Wave 2 inference (source.md:143, :151, :155, :159) and lands reversibly on the user's fork PR #1 (E4); fix: non-existent repo and N, a tested origin_repo.py check that Wave 0 must call, real-output evidence in a post-Task-13 session, plan:26 rewritten by target, else approval. |
| C-002 | V1 | minor | Two exits, stop (plan:233) vs pending (plan:236); resume works through Row S (refs/ledger.md:161), so my S-2 "cannot work" is withdrawn. |
| C-003 | V3 | minor | Task 6's mandated table rows source.md:336, :340 lack `--repo` and trip plan:131; satisfiable by `--repo <R>` in the cells or scoping "runs gh" to code (plan:136 still valid). |
| C-004 | V1 | minor | plan:243 names no key-path method; merge V1's curl -v/-i/--trace ban and `already_assigned` allowance with V3's `test -n "${CLICKUP_API_TOKEN:-}"` (plan:23 bans printenv/env). |
| C-005 | V1 | minor | plan:45 clears 2 of the 4 CLICKUP_* variables plan:43 reads; V3's S-4 (plan:23 vs plan:50) is a literal wording conflict, not a diff-level breach (qa.md:52). |
| C-006 | V2 | minor | Pending ACs are truthful (plan:15, :258), but "approval at that moment" (plan:254) has no trigger because the executor never prompts outside its closed list (qa.md:274, :288); add one explicit ask. |
| C-007 | V3 | minor | plan:252 "Depends on: Task 14" vs plan:254 citing Task 15 and 16 evidence; metadata only (SKILL.md:79, :97); "after Task 13" (plan:233) is the load condition, not an error. |
| X-001 | V2 | minor | PASS with notes: C-001, C-002 and C-003 are all minor under the binding rule; round-1 F-01/F-02 fixed (plan:216-227, :23, :45, :50); C-001's fix gates Task 17's item-4 run. |
| X-002 | V1 | minor | Yes: Q0's start line (SKILL.md:108-115) plus Row S "Else A1" (refs/ledger.md:161) re-runs Task 15; Row P needs a blocked verdict (refs/ledger.md:155). |
| A-001 | none | reject | ACCEPT: source.md:391 defines the static test as phrase presence and plan:126 matches; round 1 rejected the same challenge. |
| A-002 | new | minor | QUALIFY: plan:254 maps only AC 5's ClickUp half; the first half (source.md:471) needs a live claim, so name it pending and do not mark it run on Task 2's no_token output (plan:50). |
| A-003 | new | minor | REJECT: the next-steps `/model` first-line rule (plan:77; source.md:474) is in no Task 4 AC (plan:81-85) or Task 7 test (plan:123-132). |
| A-004 | new | minor | QUALIFY: plan:131 bans `{owner}/{repo}` but never asserts `gh api` paths spell `repos/<R>/` (source.md:319). |
| A-005 | new | minor | REJECT: the URL-vs-origin comparison (source.md:143) is untested (plan:32-38); a Task 1 check plus a Task 6 AC that Wave 0 calls it is the mechanical half of C-001's fix, disclosed as an addition under source.md:361. |
| A-006 | V2 | minor | QUALIFY: the user names a task ID (plan:243) but the workspace-wide match (source.md:304-309) picks the PUT target; compare the reported `task_id` with the named one before the second run (plan:246). |
| A-007 | new | minor | REJECT: plan:254 needs the plan:233 post-Task-13 session with no check or restart path; a narrated run would falsely satisfy plan:258 (qa.md:50); fix: same precondition plus real-output evidence. |
| A-008 | none | reject | ACCEPT: pytest is a main dependency (pyproject.toml:34-43), addopts needs no extras, and no test imports dev extras. |


## Round 2.5: Invariant Probe

Run on resume; results in `invariant-probe.md` (raw output `.work/r25-probe.md`). 12 findings: 1 HIGH UNADDRESSED (INV-001), 7 MEDIUM UNADDRESSED, 1 LOW UNADDRESSED, 3 LOW ADDRESSED. No blocking plan defect missed by the debate.

## Scoring Matrix

Winners and dispositions are taken from the three Round 2 "Updated Position Table" sections (round2-v1.md:90-110, round2-v2.md:100-120, round2-v3.md:125-145). Agreement is unanimous on disposition for all 19 points; on S-002 the winner label is 2/3 (V2 named itself).

| Diff Point | Winner | Confidence | Evidence Summary |
|------------|--------|------------|-----------------|
| S-001 | none (reject) | 95% | Card schema and key style only; unanimous. |
| S-002 | none (reject) | 85% | Verdict basis follows the C-001..C-003 rulings; disposition unanimous, winner label 2/3. |
| C-001 | V1 (minor) | 95% | Unanimous minor after V3 conceded from blocking (round2-v3.md:3); top-priority minor; fix gates Task 17 item 4. Qualified by INV-001 (URL digits). |
| C-002 | V1 (minor) | 95% | Resume works via Q0 and Row S; defect is two exits; V3 withdrew "resume cannot work". |
| C-003 | V3 (minor) | 95% | V1 handed the better instance to V3 (round2-v1.md:26); section-14 table rows lack `--repo`. Qualified by INV-004. |
| C-004 | V1 (minor) | 90% | No key-path method; curl ban; `already_assigned`; V3's `test -n` merged. |
| C-005 | V1 (minor) | 90% | Two of four CLICKUP_* variables cleared; V3's S-4 wording merged. |
| C-006 | V2 (minor) | 90% | Approval clause has no trigger (refs/qa.md:274, :288). Qualified by INV-005. |
| C-007 | V3 (minor) | 90% | Task 17 Depends on omits Tasks 15 and 16; metadata only. |
| X-001 | V2 (PASS with notes) | 95% | V1 and V3 conceded their FAIL bases. |
| X-002 | V1 (minor) | 90% | Resume via Row S; clarify which exit wins. |
| A-001 | none (reject) | 95% | source.md:391 defines the static test as phrase presence. |
| A-002 | new (minor) | 90% | AC 5 first half unplaced. |
| A-003 | new (minor) | 90% | AC 8 `/model` first line unasserted. Qualified by INV-011. |
| A-004 | new (minor) | 90% | No `repos/<R>/` assertion. |
| A-005 | new (minor) | 90% | URL-vs-origin comparison untested; half of C-001's fix. Qualified by INV-002. |
| A-006 | V2 (minor) | 90% | Workspace-wide match picks the PUT target. Qualified by INV-007. |
| A-007 | new (minor) | 90% | Item 4 needs a post-Task-13 session with no check; V2 changed from reject (round2-v2.md:72). |
| A-008 | none (reject) | 95% | pytest is a main dependency. |

### Points won (Step 3 tiebreaker input)
- Variant 1: C-001, C-002, C-004, C-005, X-002 = 5
- Variant 2: C-006, X-001, A-006 = 3
- Variant 3: C-003, C-007 = 2
- No variant winner: S-001, S-002, A-001, A-008 (rejected); A-002, A-003, A-004, A-005, A-007 (raised by no card)

## Convergence Assessment
- Points resolved: 19 of 19
- Alignment: 100%
- Threshold: 80%
- Taxonomy gate: all levels covered (L1 1, L2 7, L3 11; diff-analysis.md "Taxonomy tags")
- Invariant gate: CONVERGENCE BLOCKED: 1 HIGH-severity UNADDRESSED invariant detected. Blocking item: INV-001, a gap in the consensus fix for C-001 (its example URL embeds `302`), not a reversal of it. Depth is standard, so no Round 3 runs. The orchestrator carries INV-001 into the refactor plan as a required amendment to the merged C-001 recommendation and lists it in the return contract's `unaddressed_invariants`.
- MEDIUM UNADDRESSED warnings: INV-002, INV-003, INV-004, INV-005, INV-006, INV-007, INV-008.
- Status: BLOCKED_BY_INVARIANTS
- Unresolved points: none

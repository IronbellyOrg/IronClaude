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

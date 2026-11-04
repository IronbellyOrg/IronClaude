# Refactor-Plan Review (Step 4, independent analytical reviewer)

Target: `refactor-plan.md` (same folder as `.work/`).

VERDICT: APPROVE

Binding rule applied: blocking only for wrong behaviour, a false claim, a missing required deliverable, or a security/data-loss risk. No blocking finding. The merged verdict (PASS with notes) stands. The numbered changes below are all **minor**: apply them in the merge (they are cheap and remove a self-contradiction and four loose ends), but they do not block it and need no re-review.

## Required changes

Blocking: none.

Recommended (minor), in priority order:

1. **Change 11 (F-10): scope the `gh api` assertion so it does not fail on required content.**
   - Replace "every `gh api` path in the skill and agents starts with `repos/<R>/`." with "every `gh api` path in the skill and agents other than `user` (the login lookup of source.md:148) starts with `repos/<R>/`; none uses the brace placeholder."
   - Add `source.md:148` and `plan:92` to F-10's evidence.
   - Evidence: source.md:148 runs `gh api user -q .login`; plan:92 requires claim.md to carry "the gh commands exactly as written there"; Change 2 (4) already says `gh api` takes no `--repo`. As written, F-10's test must fail, the class of conflict F-03 fixes.
2. **Change 20: give U-019 a disposition.** Add to `rejected_findings` (or `notes`): "U-019 (V1 A-1: read the implemented SKILL.md before the live run): superseded by F-01 (2), a tested URL check that Wave 0 must call, pinned by a Task 6 AC, and by F-12 (a read-through is not evidence)." Evidence: diff-analysis.md:63; no change in refactor-plan.md disposes of it.
3. **Change 2 (F-01): attribute the fallback change.** In (5) replace "fallback: if (1) and (2) are not applied, item 4 stays pending." with "fallback: if (1) and (2) are not applied, item 4 stays pending (INV-005: the executor cannot ask for approval, refs/qa.md:288, SKILL.md:4; the debate's 'else approval' is replaced)." Add "; fallback amended by INV-005" to the Debate ruling line, and add F-01 to Change 21's INV-005 list. Evidence: round2-v2.md:64, round2-v3.md:73 say "else approval".
4. **Change 12 (F-11) and Change 7 (F-06): name the plan sentences that change.**
   - F-11: add "Remove plan:243's 'Ask the user only for the test issue URL and task ID'; the user supplies them before the session in <one named channel, e.g. a file `./artifacts/t16-input.md` or the `/sc:implement` invocation text>."
   - F-06: replace "plan:26's 'approval at that moment' is reworded" with "plan:26's and plan:254's 'approval at that moment' clauses are reworded".
   - F-02: add "plan:233's 'delete it afterwards only with the user's approval' moves into the runbook."
   - Evidence: plan:233, plan:243, plan:254 each still contain an ask the executor cannot make (refs/qa.md:288).
5. **Change 7 (F-06) and Change 3 (F-02): make the runbook complete.**
   - F-06: "items 1, 2, 3, 6 and 8" becomes "items 1, 2, 3, 5 (first half) and 6 and 8" (F-08 says item 5's first half needs a live claim, source.md:471).
   - F-02: "export the ClickUp variables" becomes "export `CLICKUP_API_TOKEN`, `CLICKUP_WORKSPACE_ID` and `CLICKUP_LIST_IDS` (the test list, F-11) and have the test issue URL and task ID ready", and add one line saying where runbook results are recorded once the package is archived to `.dev/tasks/done/` (refs/managed-workspace.md:47-54).
6. **Change 2 (F-01) (2): give the `/pull/<N>` case an expected result.** After "a `/pull/<N>` URL" add "(on origin: rejected, not parsed as an issue number; state the code)". Evidence: r25-probe.md:32 adds the case without an outcome; F-18 handles pull requests in the same merge.
7. **Change 4 (F-03): keep plan:136's negative case valid.** Add "plan:136's negative case writes its `gh issue view` line as a code span or fenced line." Evidence: the narrowed scan only sees code spans and fenced lines; round2-v3.md:81.
8. **Wording and labels.**
   - Change 21, INV-008 line: "would make every worker spawn fail (source.md:335)" becomes "would leave every worker unable to write its file, so every claim or create ends `E-WORKER-NO-OUTPUT` (source.md:335) [INFERRED]".
   - Change 23 (F-18) claim: append "[INFERRED: an open PR's `state` reads `OPEN`; `gh issue edit` on a PR number is UNVERIFIED (r25-probe.md:81)]".
   - Change 2 (1): append "(that this repo does not exist is UNVERIFIED; no gh was run)".
   - Overview line 12: "taken from the Round 2 position tables ..., `.work/evidence-sheet.md` or the probe" becomes "taken from the Round 2 position tables, the reviewer cards, the round-1 statements, `.work/evidence-sheet.md` or the probe".
   - Changes 8-11, 14-18, 23: state `category` and `source_cards` for each (A-00x points: no card, calibration-sourced; F-18: invariant probe), since Overview line 6 requires both keys.
   - Put Change 22 before Change 23 and add both to the Risk Summary.

## Notes

- Verdict basis: coverage is complete except one disposition row (U-019); every severity matches the debate; every citation re-read supports its claim (three need an [INFERRED] or UNVERIFIED label); the no-prompt rule holds in every recommendation. Details in sections 1-5.

### 1. Coverage

- Diff points (19): all have a disposition. S-001, S-002, A-001, A-008 rejected (Change 20); C-001 + A-005 -> F-01; C-002 + X-002 -> F-02; C-003 -> F-03; C-004 -> F-04; C-005 -> F-05; C-006 -> F-06; C-007 -> F-07; X-001 -> verdict (Change 1); A-002 -> F-08; A-003 -> F-09; A-004 -> F-10; A-006 -> F-11; A-007 -> F-12.
- Unique contributions: U-001 (Change 1), U-002 and U-009 (F-05), U-003 (F-13), U-004 (F-03), U-005 (rejected, Q-1), U-006 and U-007 (authorized_expansions), U-008 (F-06), U-010 (F-14), U-011 (F-04), U-012 (F-15), U-013 (F-16), U-014 and U-017 (notes), U-015 (F-17), U-016 (rejected, S-11), U-018 (F-07).
- **Dropped: U-019** (V1's "read the implemented SKILL.md and confirm E-FOREIGN-REPO precedes the first gh call before the live run", diff-analysis.md:63). No change in refactor-plan.md mentions it. Its intent is covered by F-01 (2) (a tested check that Wave 0 must call, pinned by a Task 6 AC) and F-12 (a read-through is not evidence), so the gap is a missing disposition row, not a missing fix. Minor. See recommended change 2.
- Invariants INV-001..INV-012: all twelve are handled in Change 21 and each named target change carries the fix: INV-001/002/003 in Change 2 (URL without stray digits, the extra test cases, distinct exit code, split item-4 row); INV-004 in Change 4 (one scan for plan:58 and plan:131, prohibitions with `--repo <R>`, placeholder rule without the literal token); INV-005 in Changes 3, 7, 12, 13; INV-006 in Change 23; INV-007 in Change 12; INV-008 in Changes 14-18; INV-011 in Change 10; INV-009/010/012 no change. One attribution gap: Change 2 (5) also applies INV-005 (fallback "stays pending" instead of the debate's "else approval") without naming it (recommended change 3).

### 2. Fidelity

- Every severity in refactor-plan.md is minor, matching all three Round 2 tables (round2-v1.md:92-110, round2-v2.md:102-120, round2-v3.md:127-145). No severity was changed. F-18 is new from INV-006 and graded minor with a stated reason (plan:92 already requires the pull-request STOP), which matches r25-probe.md:156.
- Winners and confidences match the scoring matrix (debate-transcript.md:680-698): C-001 V1 95%, C-002 V1 95%, C-003 V3 95%, C-004 V1 90%, C-005 V1 90%, C-006 V2 90%, C-007 V3 90%, A-006 V2 90%.
- Recommendations that differ from the debate name the probe item that changes them: C-001's URL (INV-001), C-002's exit (INV-005), C-006's ask (INV-005), A-006's mechanism (INV-005, INV-007). The one unnamed amendment is Change 2 (5): the debate's fallback is "else approval at that moment, otherwise pending" (round2-v2.md:64, round2-v3.md:73); the plan says "stays pending" and cites no probe item. The change is correct under INV-005 (refs/qa.md:288; SKILL.md:4); only the attribution is missing.
- No recommendation contradicts the debate or the probe.
- Overview line 12 overstates provenance: it says every evidence entry came from the Round 2 tables, evidence-sheet.md or the probe, but F-13..F-17 take their evidence from the reviewer cards (variant-1-original.md:36-41, variant-3-original.md:20-25) and their rulings from the round-1 files. The cited lines are correct; only the sentence is inaccurate. Minor.

### 3. Citations

Every `plan:N`, `source.md:N`, repo `file:line` and debate-file line cited in refactor-plan.md was re-read in this review. All support their claims, with the qualifications below. No citation is wrong in a way that makes a claim false.

Checked and supported:
- plan: 15, 23, 26, 32, 32-38, 43, 45, 50, 56, 58, 77, 78, 81-85, 92, 105, 111, 116, 123-132, 125, 129, 131, 132, 136, 146, 197, 233, 236, 243, 246, 252, 254, 258, 259.
- source.md: 66, 142-143, 144, 148, 151, 154, 155, 159, 162, 178(-179), 298, 304-309, 310, 319, 320, 335, 336, 340, 361, 391, 438, 470, 471, 474.
- Repo: sc-implement-protocol SKILL.md:4 (allowed-tools has no AskUserQuestion), :79 (depends-on ignored), :97 (source order), :108-115 (Q0 start line), :132 and :146 (Q6 lint incl. `make lint`), :152-154 (extra fail / unrelated-red); refs/qa.md:274 (no user prompt), :288 (closed list); refs/ledger.md:155 (Row P), :161 (Row S, "Else A1"); refs/managed-workspace.md:3 confirms the managed rules are additive, so Row S still governs this `workflow-plan/1.2` package; evidence-validator.md:8 (`permissionMode: plan`); local-gateway-alias-proxy.py:17-21 (tier request goes to a member model); docs/user-guide/commands.md:236; pyproject.toml:34-43 (pytest in main dependencies).
- Debate files: round2-v1.md:13, :21-24, :26, :101; round2-v2.md:17-19, :72, :111; round2-v3.md:3, :12, :15-16, :24-25, :25, :63-74, :106, :136; round1-v1.md:21, :22, :77; round1-v3.md:13, :14, :18; reviewer-cards/reviewer-1-calibration.yaml (A-1 row and `missed_by_card`).

Qualified (minor, wording only):
- Change 21, INV-008 line: "a copied `permissionMode: plan` would make every worker spawn fail (source.md:335)". source.md:335 is "Worker returns no file, or an empty one ... STOP `E-WORKER-NO-OUTPUT`". The spawn itself does not fail; the worker cannot write its file. The probe says the same (r25-probe.md:106: "every live claim or create ends `E-WORKER-NO-OUTPUT`"). That plan mode blocks a subagent's Write is [INFERRED] from round1-v3.md:13, not verified here.
- Change 23 (F-18) claim "an open pull request reports `OPEN`": no cited line shows it. E4 shows only a MERGED PR answering `gh issue view`. The probe marks `gh issue edit` on a PR number UNVERIFIED (r25-probe.md:81). The claim should carry [INFERRED] and the UNVERIFIED note.
- Change 2's replacement URL `https://github.com/IronbellyOrg/no-such-repo-sc-issue-probe/issues/999999999`: that the repo does not exist is UNVERIFIED (no gh in the probe or in this review). It does satisfy INV-001's rule (no digits outside `/issues/<N>`).

### 4. Internal consistency

- **No-prompt rule: holds.** F-02 (Change 3), F-06 (Change 7), F-11 (Change 12) and F-12 (Change 13) all say the executor cannot prompt mid-run (refs/qa.md:288; SKILL.md:4) and make pending the exit. F-01 (5) also ends in pending. No recommendation tells the executor to ask the user mid-run.
- **But three "ask" sentences in the plan are left untouched by any recommendation**, so the merged verdict does not say what replaces them:
  - plan:243 "Ask the user only for the test issue URL and task ID". F-11 says the URL and task ID are "supplied up front" but names neither the sentence to remove nor the channel (an environment variable, a file in `./artifacts/`, or the `/sc:implement` invocation text).
  - plan:254 "unless the user approves a run against a test issue at that moment". F-06 rewords only plan:26's copy of this clause.
  - plan:233 "delete it afterwards only with the user's approval". Safe by default (nothing is deleted), but it is another unanswerable ask; it belongs in the F-02 runbook.
- **F-10 contradicts F-01 (4) and the spec content Task 5 must copy.** F-10 (Change 11) asks Task 7 to assert "every `gh api` path in the skill and agents starts with `repos/<R>/`". The spec's Wave 1 runs `gh api user -q .login` (source.md:148), plan:92 requires refs/claim.md to carry "the gh commands exactly as written there", and the T3 worker body describes that lookup (plan:56). F-01 (4) itself says `gh api` takes no `--repo` and cites source.md:148. So the F-10 test, written as recommended, fails on required content: the same class of conflict as C-003, which the merge fixes in F-03. Fix: scope F-10 to repository endpoints (every `gh api` path other than `user` starts with `repos/<R>/`, never `{owner}/{repo}`).
- **F-06's live-run list omits item 5's first half.** F-06 lists items 1, 2, 3, 6 and 8 for the scratch-issue pre-approval; F-08 (Change 9) says AC 5's first half (source.md:471) "needs a live claim". The runbook request should list it too.
- **F-02's runbook vs F-11's preconditions.** The runbook says "export the ClickUp variables"; F-11 also needs `CLICKUP_LIST_IDS` set to the test list and the test issue URL and task ID. The runbook step should name all three.
- **F-01 (2) `/pull/<N>` test has no expected outcome.** It lists a `/pull/<N>` URL as a test case but does not say whether it yields `E-FOREIGN-REPO`, `E-NOT-AN-ISSUE` or a parsed N. With F-18 in the same merge, it should say `/pull/<N>` on origin is rejected (and with which code).
- **F-03's negative case.** With the scan narrowed to code spans and fenced lines, plan:136's negative case ("a `gh issue view` line lacking `--repo`") must be written as a code span or fenced line, or it will no longer trip the test. V3 says plan:136 stays valid (round2-v3.md:81); the merge should say how.
- Cosmetic: Change 23 sits before Change 22; the Risk Summary omits Changes 22 and 23; Changes 8-11 and 14-18 give no `category` or `source_cards` although Overview line 6 requires both keys on every finding (the executor must take them from the cards: A-00x points come from no card, F-18 from the probe).

### 5. Severity / missed blocking defects (self-audit)

**No blocking defect found that PASS with notes would miss.** Candidates examined and why each stays minor under the binding rule:

- **F-10 conflict (section 4).** A merge-introduced test that required content must fail. The debate ruled the identical class (C-003) minor because it surfaces as a red test that the owning task must fix before its AC passes (plan:135; round2-v1.md:96, round2-v2.md:106, round2-v3.md:131). Same grade here, but it should be fixed in the merge because it is cheap and the merge otherwise ships a self-contradiction.
- **F-18 / INV-006 (open PR claimed).** Would be wrong behaviour in the shipped skill, but the spec's own scout field list (source.md:151) has no `url` either, so the plan matches its spec; plan:92 requires the STOP and Task 5's author can supply the signal. Latent, not a false plan statement or missing deliverable (agrees with r25-probe.md:156). Minor, fix before any live claim, as the plan says.
- **C-001 under the current plan text.** INV-005's "item 4 is always pending on the first pass" assumes the skill is not available mid-session; the probe marks skill hot-loading UNVERIFIED (r25-probe.md:70). If skills do load after Task 13's `make sync-dev`, plan:254 as written could run the octocat URL in the same pass. The worst result is still the debate's two-fault, reversible, own-fork outcome, and F-01's URL fix plus F-12's precondition apply before any run. Minor; F-12 should not present the pending outcome as a fact about Claude Code, only as the rule.
- **Runbook after archive.** Task 17 is the last task; the managed FINAL and archive then move the package to `.dev/tasks/done/` (refs/managed-workspace.md:47-54). The F-02 runbook's results (Task 15 spawns, Task 16, item 4) will be produced after that, and the merge does not say where they are recorded. Process gap, no wrong behaviour. Minor note.
- Severity of every other finding re-checked against the binding rule: none involves a false claim in the plan, a missing deliverable, or a security or data-loss risk (secrets: plan:23 plus F-04/F-05; deletions: only the Orca worktree in Task 14 and the never-staged smoke folder).

Self-audit (what I checked): all 21 changes line by line against diff-analysis.md (19 points, U-001..U-019), the three Round 2 tables, the scoring matrix and convergence block (debate-transcript.md:674-714), base-selection.md "Strengths to preserve/incorporate", invariant-probe.md and r25-probe.md (all 12 INV rows and "Missed blocking defects"); every plan, source.md, repo and debate-file citation in refactor-plan.md re-read (section 3); the no-prompt rule across every recommendation and every remaining "ask" sentence in the plan; spec sections 15, 16, 17 and 20 spot-checked against the plan for a missed deliverable (none found beyond the debate's pending rows). Not done: no gh call (state of #302, existence of the replacement repo, `gh issue edit` on a PR number), no test run.

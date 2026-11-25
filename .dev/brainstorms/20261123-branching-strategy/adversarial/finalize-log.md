# Finalize Log: owner answers applied to the unified branching proposal

## Metadata
- Document: `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261123-branching-strategy/UNIFIED-BRANCHING-PROPOSAL.md`
- Task: apply the owner's eight answers of 2026-11-23 so the document becomes the decided rules, version 1
- Executor: merge-executor agent (instructions from team-lead)
- Writes: the document and this log only; no git or GitHub write

## Changes per section
Section numbers are those of the document. Decision numbers are those of section 10 (same order as the owner's eight answers).

### Top of file
- Added the status line ("decided by the owner on 2026-11-23 (decisions 1 to 8); trials T1 to T12 not yet run; the large-PR rule (section 8) is to be verified by trials T4 and T7"), a "Version 1, 2026-11-23" line and a provenance comment pointing to this log. Original provenance comments kept.

### 1 Summary
- 1.1: rewritten for the review-only story PR on every story (decision 6b); sync PR removed from the release steps; one sentence that `integration` is not in use, with a pointer to Appendix A (decision 5); weak-point sentence updated (the optional layer is no longer optional).
- 1.2: Owner row (decided, not "decides"); Clay row (integration not in use); Settled story row (adds the finished review-only run); new row "Review-only pull request"; row "Sync PR" removed.
- 1.3: "default" sentence replaced: decision 2 numbers approved for release 1, marks explained, remaining GUESS values called working values.
- 1.4: retitled "starting decisions" with a one-line pointer to section 10; rows for plan approval, Clay's habit, pr-submit sessions and CI rewritten (sessions: 1 per story + release + records/revert/second landing, 7 in the base case, 9 with records and a revert; owner clicks only for release, records, revert, second landing PRs).
- 1.5: local-merge bullet says confirmed on 2026-11-23; states a review-only PR is never merged with the button.

### 2 Branch names
- 2.1: row "Sync PR head" removed. 2.5: T12 reference now "rung 1 of Q5"; the T3/T4/T6 row now covers the review-only story PR and says T6 must pass before the first one is relied on.

### 3 How a release moves
- 3.1 legend: review-only PR mentioned. 3.2: step 2 (worker pushes and runs review-only pr-submit), step 3 (finished run is first in the order; PR should show merged after push, T6; earlier-PR list loses "optional"), step 8 (sync PR replaced by the two-parent check).
- 3.3: owner row (decided, trials T1, T2, T3, T5, T6, T9 passed), review-only runs added to the day 0 to 1 and day 1 to 3 rows, sync rows replaced by the two-parent check row (with the revert-and-redo hint) and a clean-up row.

### 4 The nine questions
- Q1: "sync" removed from the flat-branch list.
- Q2: Where, Authority, Method (merge commit decided, "open owner choice" sentence removed), Order (finished review-only run first), local gate (decision 1c confirmed), outside gate (on, decision 6a), "Optional layer" paragraph replaced by "Review-only story pull request, for every story" (no size threshold, T6 gate, costs, waits for its run, `-fix` default).
- Q3: title no longer names `integration`; rebase exception confirmed; the `integration` bullet reduced to "not in use" plus pointer (early-warning checks moved to Appendix A).
- Q4: merge-click precedent stated as verified (#658 squash merged 2026-11-18, one parent; #662 revert; #664 merge commit, two parents; #664's body already said merge commit); the sync PR body sentence removed; decision 2 and 6a wording; owner-wait list loses "sync-branch preparation"; follow-up wording (section 9). The text did not say the sentence was absent before #658, so no sentence needed correcting.
- Q5: ladder reduced to two rungs: rung 0 is the line with a review-only PR for every story (was "rung 2"), rung 1 is slicing (was rung 3). T12 and the sources note renumbered to "rung 1".
- Q6: item 7 now "Decided (decision 7)".
- Q7: sync branch and sync PR conditions removed; line and records deleted after the owner's merge and the two-parent check; decision 1d confirmed; sweep condition updated.
- Q8: rewritten to the decided state (integration not in use; nothing depends on it; one sentence pointing to Appendix A). The sync steps, branch head rationale, price sentence and the unverified who-runs-it remark moved to Appendix A.

### 5 Costs
- First bullet (no CI per story, bots review every story), new bullet "One pr-submit session per story" (7 in the base case), owner clicks bullet (no sync PR, story PRs need no click, base case of one click), "late sync" bullet removed, local-merge bullet reworded, review-only bullet reworded (one UNVERIFIED behaviour), two-parent check wording.

### 6 Who does what
- Coordinator, Workers, Owner and Clay rows updated (no sync branch, review-only pr-submit run by every worker, owner decided on 2026-11-23, Clay's PRs land on `master`); 6.2 updated.

### 7 Risks
- Risk 5 rewritten for the review-only PR on every story (two UNVERIFIED behaviours, T6). Other risks unchanged.

### 8 Size budget
- 8.2: intro (numbers approved for release 1), column renamed "Value for release 1", row "Review-only story PR threshold" removed. 8.3: decision 3 added to item 3; item 7 now says the records PR becomes the default after three releases in a row.

### 9 Trials
- Intro: T6 now must pass before release 1 (first story PR relied on); T12 reference; T5 owner-approval wording; T6 row (when, what it settles, what failure means); T12 failure text.

### 10 Decisions
- Section replaced by "Decisions taken on 2026-11-23": each of the eight decisions with the answer and its meaning; table "Where the debate points stand" (C-005, X-004, C-006, X-005, A-014, C-017, A-006, A-015, A-008, A-013, A-012, A-007, A-011); new 10.1 "Still open for the owner" (4 items) plus the defaults that remain defaults.

### 11 Sources
- "third rung of Q5" changed to "rung 1 of Q5".

### 12 How this was produced
- Item 4 (seven unresolved points: six settled by the answers, one by T1) and item 6 (no longer says the decisions are unanswered) updated; new item 7: the owner's answers were applied on 2026-11-23.

### Appendix A (new)
- "If `integration` comes back": the moved sync step (4 steps), the head-branch rationale, the price sentence, the who-ran-it remark, and the early-warning checks. Marked not part of the current rules.

## Points not covered by the owner's answers (defaults chosen here)
The owner's eight answers do not say these; the document states them as defaults and lists them in section 10.1 or in the place named:
1. **A `-fix` branch gets no review-only PR** (it is not a story; the release PR's bots read it). Needed to avoid an ambiguity in Q2 and Q6 item 2. Change by editing Q2 if the owner wants fix branches reviewed too.
2. **A story waits for its own review-only pr-submit run to finish before the coordinator merges it**, and the coordinator does not touch the story branch during that run (3.2 steps 2 and 3, Q2). Derived from pr-submit's rule that a moved head halts the run (`pr_head_mismatch`); it also adds waiting time per story (section 5). Not listed in 10.1.
3. **Rung numbering in Q5** changed to two rungs (rung 0 default, rung 1 slicing) so the text has no gap; the owner said only that the old "rung 2" becomes the default. Not listed in 10.1.
4. **Records PR default after three releases in a row** is written as automatic (the coordinator then cuts it without waiting for the count at freeze), reading "default after three releases in a row" in answer 3. Not listed in 10.1.
5. **If trial T6 fails**, the review-only story PR is not used and the coordinator tells the owner before release 1 (the owner said only that T6 must pass before the first one is relied on). Not listed in 10.1.
6. **Trial T6 moved into the "before release 1" list** (T1, T2, T3, T5, T6, T9), because every story depends on it. Not listed in 10.1.

Only item 1 is shown to the owner in section 10.1; items 2 to 6 are derived consequences that the owner may want to confirm.

## Validation result
Whole document re-read after editing (all 12 sections and Appendix A). Result: PASS.

| Check | Result |
|-------|--------|
| No text describes the sync PR or its head branch `dash<rel>-sync<N>` as current | PASS. Remaining mentions: decision 5 (says it is out of the rules), Q3 and Q8 pointers, 1.1 pointer, 1.4 row, and Appendix A (labelled not part of the current rules). |
| No text describes the size-threshold layer (15 files or 1,000 lines) as current | PASS. Remaining mentions say it is dropped (Q2, decision 6). Grep for "optional", "Recommended", "rung 2", "rung 3", "third rung", "owner's nod", "owner confirms": only the deliberate "rung 2" history note in Q5. |
| Internal references resolve (sections 1.x to 12, Q1 to Q9, 3.2 steps, 8.3 to 8.5, 10.1, Appendix A, decisions 1 to 8, trials T1 to T12, section 2.2 rules) | PASS |
| Numbers match: story cap 6, time box 7 days, file budget 250, stop adding 200, hard stop 300; sessions per release 7 base and 9 with records and a revert (sections 1.4 and 5); trials before release 1: T1, T2, T3, T5, T6, T9 (section 9, 3.3 and 10.1) | PASS |
| No em or en dashes | PASS (grep count 0) |
| Ref-name rule (no branch name is the folder of another; flat names) | PASS; the only sync branch name left is the flat `dash<rel>-sync<N>` in Appendix A |
| CI runs only for PRs into `master` and `integration` | PASS; stated for review-only story PRs (no CI) and for decision 6c (no `test.yml` change) |
| Never rebase or force-push a published branch | PASS; merge-in of `master` stays a merge commit |
| Fork-only rule and never touching SuperClaude-Org | PASS; every `gh` command keeps `--repo IronbellyOrg/IronClaude`; section 1.5 sentence unchanged |
| Precedent of #658, #662, #664 stated as verified; no sentence says the PR-body sentence was absent before #658 | PASS (Q4 and decision 8) |
| Writes limited to the document and this log; no git or GitHub write | PASS |

Known limit: the debate-point table and the "still open" list were written from the debate files (`adversarial/debate-transcript.md`, lines on C-005, C-006, C-017, A-008, A-013, A-015); they were not re-verified against GitHub.

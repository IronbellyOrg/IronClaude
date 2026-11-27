```yaml
contract_version: 1.9.0
status: partial
mode: pre
tier_reached: 2
confidence_calibrated: 0.86
citations_total: 27
citations_revalidated: 27
citations_dropped: 1
citations_inferred: 0
citation_budget_policy: full_reread
coverage_degraded: parsed-sparse
```

# Reflect report (UC-1, pre-execution): plan TASK-WF-followUpForIssue-20261126-165706

Plan: .dev/tasks/to-do/TASK-WF-followUpForIssue-20261126-165706/TASK-WF-followUpForIssue-20261126-165706.md (7 tasks, 4 phases). Spec: .dev/tasks/to-do/TASK-WF-followUpForIssue-20261126-165706/source.md.

## Summary

Verdict: FAIL, two Blocking findings. Tier 2 ran because the spec has no labeled requirement ids (coverage_degraded: parsed-sparse) and the Tier-1 card calibrated at 0.64. Two reviewers (opus and haiku class; the sonnet class that wrote the plan was excluded), blind calibration (0.86 and 0.62, class sonnet), a two-round debate between the cards (14 of 14 diff points agreed, blocked by invariant INV-001, which the repair absorbs), a fault-finder probe and a merge. The merged card has 2 Blocking, 5 Medium and 10 Note findings (after the validation below). The calibrated confidence of this report is that of the base card, 0.86.

## Inferred requirements (Pass 2)

| INF id | Verbatim quote | Citation | Match result |
|---|---|---|---|
| INF-001 | "A handoff of unfinished work skips only the 'already claimed' check." | .dev/tasks/to-do/TASK-WF-followUpForIssue-20261126-165706/source.md:1 | Task 1 |
| INF-002 | "When the words do not fit in 24 characters, drop the words and keep <login>/issue-<N>. Never stop on it." | .dev/tasks/to-do/TASK-WF-followUpForIssue-20261126-165706/source.md:1 | Task 1, 5, 6 |
| INF-003 | "Lessons of a long-lived worktree with no issue are written in that worktree's .dev/ notes" | .dev/tasks/to-do/TASK-WF-followUpForIssue-20261126-165706/source.md:1 | Task 1 |
| INF-004 | "The watcher and the claim do not refuse an issue that already has a worktree" | .dev/tasks/to-do/TASK-WF-followUpForIssue-20261126-165706/source.md:1 | Task 1 |
| INF-005 | "update the slide 12 heading, eyebrow and introduction, and the CLAUDE.md worktree examples" | .dev/tasks/to-do/TASK-WF-followUpForIssue-20261126-165706/source.md:1 | Task 3, 4 |
| INF-006 | "a person whose login has one leaves the login out of branch names and uses issue-<N>-<words>" | .dev/tasks/to-do/TASK-WF-followUpForIssue-20261126-165706/source.md:1 | Task 1, 5 |
| INF-012 | "the test file must take the digit-run pattern for names from scripts/worktree_cleanup.py" | .dev/tasks/to-do/TASK-WF-followUpForIssue-20261126-165706/source.md:1 | Task 5 (see MB-2: not in force) |

Postscript: INF-007 to INF-011, INF-013 and INF-014 are listed in t1-card.md; none was dropped. coverage_pct_union 13/14 = 0.93; INF-014 (the pull request step) is outside the plan.

## Findings (merged card, adversarial/adversarial/merged-output.md)

Plan path used in the citations below: P = .dev/tasks/to-do/TASK-WF-followUpForIssue-20261126-165706/TASK-WF-followUpForIssue-20261126-165706.md

### MB-1 Blocking (Missing): no assertion on the new slide 12 introduction

Task 6(c) checks only the new heading and the absent old strings; Task 3's acceptance has no intro check, so an intro that still calls the topic open passes.
Evidence: .dev/tasks/to-do/TASK-WF-followUpForIssue-20261126-165706/source.md:1 ("deck assertions for the new heading and intro"); .dev/tasks/to-do/TASK-WF-followUpForIssue-20261126-165706/TASK-WF-followUpForIssue-20261126-165706.md:106 (Task 6 body); .dev/tasks/to-do/TASK-WF-followUpForIssue-20261126-165706/TASK-WF-followUpForIssue-20261126-165706.md:74 (Task 3 acceptance criteria).

### MB-2 Blocking (Decision): the plan carries a requirement the user withdrew, with stale checks that depend on it

Task 5 replaces the hand-copied digit pattern by an `ast` read of scripts/worktree_cleanup.py and records that as a decision; the user withdrew that item ("The two Low notes stay as recorded") and the replacement instruction does not list it. The repair must also remove the checks that no longer hold once the hand copy stays.
Evidence: .dev/tasks/to-do/TASK-WF-followUpForIssue-20261126-165706/TASK-WF-followUpForIssue-20261126-165706.md:23 ("by parsing the file with `ast`"); .dev/tasks/to-do/TASK-WF-followUpForIssue-20261126-165706/TASK-WF-followUpForIssue-20261126-165706.md:98 (grep must print nothing); tests/core/test_how_we_work_worktree_policy.py:21 (`_NUMBER_RUN = re.compile(`); .dev/tasks/to-do/TASK-WF-followUpForIssue-20261126-165706/TASK-WF-followUpForIssue-20261126-165706.md:99 (the `digit_pattern` term); .dev/tasks/to-do/TASK-WF-followUpForIssue-20261126-165706/TASK-WF-followUpForIssue-20261126-165706.md:15 (Goal clause); the user messages recorded in debate-transcript.md Round 2.

### Medium findings (not repaired by the review loop)

- MM-1: the CLAUDE.md Names bullet and the unchanged deck card omit the long-name and digit-login exceptions. Evidence: .dev/tasks/to-do/TASK-WF-followUpForIssue-20261126-165706/TASK-WF-followUpForIssue-20261126-165706.md:84; docs/onboarding/ironclaude-onboarding.html:523.
- MM-2: `averylonglogin/issue-289` is labelled over 24 characters but is 24. Evidence: .dev/tasks/to-do/TASK-WF-followUpForIssue-20261126-165706/TASK-WF-followUpForIssue-20261126-165706.md:95.
- MM-3: no format-apply step before the check, no pre-change baseline, and other readers of the guide are not in the run set. Evidence: the draft cited plan line 108; the evidence validator dropped it (that line is only a header; Task 6 runs the format check and the related suites at line 111), so the finding rests on the reviewer card alone.
- MM-4: no case guards the optional-login `_BRANCH_RE`. Evidence: tests/core/test_how_we_work_worktree_policy.py:22.
- MM-6: Task 7's revert check cannot run as written. Evidence: tests/core/test_claude_md_worktree_rule.py:8; .dev/tasks/to-do/TASK-WF-followUpForIssue-20261126-165706/TASK-WF-followUpForIssue-20261126-165706.md:121.

### Notes (10)

MN-1 the already-claimed check is the owner's wording; the launcher returns `already_launched` on a `launch` entry (src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py:1748). MN-2 expected word count wrong, about 492 words. MN-3 Task 6 lacks Task 2 in its dependencies (.dev/tasks/to-do/TASK-WF-followUpForIssue-20261126-165706/TASK-WF-followUpForIssue-20261126-165706.md:104). MN-4 duplicate accept case. MN-5 the deck test needs no edit (tests/docs/test_onboarding_deck.py:23). MN-6 other-docs check not recorded. MN-7 `.dev/tasks` staging. MN-8 intro wording against the contributing card (docs/onboarding/ironclaude-onboarding.html:518). MN-9 footer hash timing. MN-10 (was MM-5): the mirror could drift only if the guide were edited after Task 2; the plan edits the guide only in Task 1, so the validator corrected the premise and the finding is a Note.

## Repairs required (blocking findings only)

- MB-1: Task 3 acceptance and Task 6(c) assert the new introduction text and that the old introduction is gone.
- MB-2: remove the cleanup-pattern requirement from source.md, the Goal, Constraints, Task 5(a), 5(f) and the Task 5 heading; remove the acceptance checks at lines 98 and 99 that depend on it; keep the hand-copied `_NUMBER_RUN`.

## Calibration and telemetry

- Tier-1 card 0.64; reviewer 1 card 0.62; reviewer 2 card 0.86; report 0.86 (base card).
- t2_model_class_diversity: degraded (executor class excluded; two reviewers); t2_vendor_diversity: single; calibrator_diversity: full (calibrator class differs from both reviewer classes; it equals the executor class, which three aliases cannot avoid).
- merge_method: adversarial; convergence_score 1.0; convergence status BLOCKED_BY_INVARIANTS (INV-001, HIGH).
- finding_counts: blocking 2, label_high 0, medium 5, note 10.

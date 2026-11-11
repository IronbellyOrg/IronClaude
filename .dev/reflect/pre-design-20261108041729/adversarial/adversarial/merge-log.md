# Merge Log

## Metadata

- Merge date: 2026-11-08
- Executor: merge-executor
- Base variant: `variant-3-original.md` (reviewer 3, opus, refactorer)
- Non-base sources: `variant-1-original.md` (reviewer 1, sonnet), `variant-2-original.md` (reviewer 2, haiku)
- Plan: `refactor-plan.md` (8 planned changes, 7 rejected or narrowed points)
- Output: `.dev/reflect/pre-design-20261108041729/adversarial/merged-reviewer-verdict.md`
- Finding id scheme: M-F1 to M-F11; each finding carries `provenance` (source ids) and, where a plan change touched it, `source` (plan change number and debate evidence)

## Changes Applied

1. **Change 1 - applied.** Base R3-F1 became M-F1 (provenance R3-F1 + R1-F1). Added `test_worker_contract.py:2005-2012` (from R1-F1 evidence) to the evidence; the recommendation now says the changed and new keys are rebuilt from the post-edit line text and that no `gh api -X POST` line may be classified read-only (`:3150-3156`). Claim now also names Tasks 7 and 8 (from R1-F1). Severity stays blocking.
2. **Change 2 - applied.** New finding M-F3 (provenance R2-F1 + R2-F2), placed right after M-F2 (base R3-F2). Combines the exact-format gap (specification 2.4) and the Q7/Q8 gap. Severity minor, not blocking: the card-level rule is one blocking finding; the plan's "minor-to-medium" range is recorded in `notes.severity_disagreement`. Claim states the gap is inherited from design tests 4 and 6 (source.md:114, :116), per the plan's rejection of the "blocking" label.
3. **Change 3 - applied.** New finding M-F9 (provenance R2-F3): the Will / Will Not test reads only SKILL.md, so keeping it unchanged in Task 7 proves no agreement with the command file.
4. **Change 4 - applied.** Base R3-F3 became M-F4 (provenance R3-F3 + R1-F3). Claim adds that the plan never names `.dev/issues/<N>/complexity-field.json` in Tasks 1 and 2; evidence adds `source.md:80`; recommendation adds "Name the file in Tasks 1 and 2". R1-F3's extra "assert it in a Task 8 test" was not added (not in the plan's change text).
5. **Change 5 - applied.** New finding M-F10 (provenance R1-F5 + R2-F4): Constraint 5 leaves out both the retained mode label and the pushback comment. Recommendation combines V1's rewording and V2's "scope to classification writes".
6. **Change 6 - applied.** Base R3-F6 became M-F7 (provenance R3-F6 + R1-F4). Regex must handle the spaced spelling (V3) and require a path character after `orgs/`; the self-check test must also feed one prose sentence that must not be reported (V1). Evidence adds "plan Task 2 acceptance bullet 2" and "plan Task 8 second test".
7. **Change 7 - applied (narrowed form).** New finding M-F11 (provenance R1-F6, narrowed): no new Task 8 test pins the Task 3 additions to SKILL.md, so reverting Task 3 turns only the Task 7 test red. R1-F6's "any of Tasks 1-5" wording and its Task 4 example were not carried over (rejected in the plan: new test 5 asserts the scout headings). R1-F6's `create.md:36` / `create-review-comment.md:3` evidence was not carried over because it supports the dropped half; evidence is the Task 8 plan line (`TASK-WF-design-20261108-041415.md:122`, cited by V2) plus the plan tasks.
8. **Change 8 - applied.** Header gains a `notes` block: severity policy (exactly one blocking finding, M-F1; all others minor) and the severity disagreement (R2-F1/R2-F2 blocking vs settled; R3-F7 argued down to Low). All findings except M-F1 are labelled minor.

Points from "Changes NOT Being Made", applied as stated in the plan:

- R2-F1/R2-F2 "blocking" label: not kept (see change 2).
- R1-F6 broad claim: not kept (see change 7).
- R1-F7 matrix note: left out of the card.
- R1-F2: folded into M-F2 as a duplicate of R3-F2; base wording kept, provenance names both.
- R3-F7: kept as minor M-F8; claim notes the ambiguity pre-dates the plan.
- R3-F4 `create.md:34` half: removed from M-F5 (claim, evidence and recommendation); the worker half stays. `refs/create.md:36` stays in the evidence.
- R3-F5 line 330: removed from M-F6; lines 34 and 331 stay.

## Post-Merge Validation

- **Structural integrity: pass.** The card parses as YAML once the leading HTML comment line is removed (checked with PyYAML). Top-level keys follow the base layout (`reviewer`, `model_class`, `persona`, `self_confidence`, `note`, `findings`, `checks_done`) plus the planned `notes` block. All 11 findings have `id`, `kind`, `severity`, `claim`, `evidence`, `recommendation` and `provenance`. Exactly one finding (M-F1) is blocking. `self_confidence` is `null` because the merged card was not re-scored; the three reviewer values are quoted in `note`.
- **Internal references: pass.** `checks_done` item 1 pointed at R3-F5; updated to M-F6. `notes` references M-F1, M-F3 and M-F8, all present. Every file:line citation was checked against the three variant files: all appear verbatim except three that are subsets of a verbatim citation after a planned narrowing or a merge of two citations (`source.md:114,116` from V2's `source.md:114` and `source.md:116`; `refs/create.md:36` from V3's `refs/create.md:34,36`; `docs/designs/sc-issue-command.md:34,331` from V3's `:34,330,331`). No new citation was invented.
- **New contradictions: none found.** M-F2 and M-F1 both say the plan's checks run only test_issue_protocol.py and agree. M-F3 (Task 8 output formats and Q7/Q8) and M-F11 (Task 8 does not pin Task 3) cover different gaps in Task 8. M-F8 notes the pre-existing ambiguity in SKILL.md without contradicting M-F11. The plan's "minor-to-medium" for change 2 versus the minor label is a recorded severity disagreement, not an unresolved contradiction.

## Summary

All 8 planned changes were applied (change 7 in its narrowed form); none skipped and none escalated. The merged card has 11 findings (M-F1 to M-F11): one blocking (the `test_worker_contract.py` classification-table break) and ten minor. All seven base findings were kept (three extended, two narrowed, R3-F7 annotated, R3-F2 unchanged), four new findings were added from variants 1 and 2, and R1-F2 and R1-F7 were folded in or left out as the plan directs.

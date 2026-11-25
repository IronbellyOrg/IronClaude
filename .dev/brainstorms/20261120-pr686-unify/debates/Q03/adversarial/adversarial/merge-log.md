# Merge Execution Log

## Metadata

- Base: Variant 1 (OURS), /home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/Q03/adversarial/adversarial/variant-1-original.md
- Non-base source: Variant 2 (CLAY), variant-2-original.md in the same folder; plan: refactor-plan.md; evidence: diff-analysis.md (M1 to M4)
- Executor: merge-executor
- Changes applied: 6 of 6
- Status: Complete (one plan ambiguity resolved by a stated rule, see Change 1, Change 6 and Notes)
- Timestamp: 2026-11-20T08:04:47Z
- Output: /home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/Q03/adversarial/merged-output.md

## Changes Applied

### Change 1: Moderator facts M1 and M2 added
- Status: Applied
- Source: diff-analysis.md M1 and M2; Variant 2 concessions
- Target: Cited facts (new facts 10 and 11, placed after fact 5) and Mechanism
- Before: Cited facts 1 to 9 only; Mechanism had no statement about the entry for poll-found issues or about the reference config.
- After: Fact 10 states the reference `repos.yaml` grant list with the cited lines, the conftest fixture line and the no-code-default grep result. Fact 11 states the no-grant behaviour of `_hold_write_ok`, row 4 returning "skip" before `record.set_hold`, and row 3 returning "skip". Mechanism gains a paragraph saying the read-only variant creates the entry with no write and the dormant form cannot (facts 10 and 11).
- Provenance tag: `Variant 2 (CLAY), Section Cited facts (concession on moderator fact M1 / M2, diff-analysis.md) - merged per Change #1`; Mechanism tagged `Base (original, modified)`
- Validation: file:line citations copied exactly from M1 and M2 (absolute paths kept for M1). Plan ambiguity: the plan says "new facts 10 and 11" but "insert after fact 5". Rule used: base numbers 1 to 9 kept so every plan reference (fact 8 in Change 2, facts 2, 7 and 9 in Change 6) still resolves; the new facts carry numbers 10 and 11 and sit after fact 5; a visible sentence under the heading explains the order.

### Change 2: Deferred label-write form
- Status: Applied
- Source: Variant 2 Cited fact 2 (`github.py:983-992`) and Mechanism
- Target: new section "The deferred label-write form" after Costs; base fact 8 replaced
- Before: Fact 8 was one line pointing at design 4.11, PR 686's history and D09 ("add and remove one label, grant gated, no comment; gate is an NG-2 amendment").
- After: Fact 8 is a one-line pointer to the new section (numbering kept). The section lists: one label added and removed with no comment (`LabelWriter` quote and injected refusal guard, `github.py:983-992`); grant gated (`_hold_write_ok`, `cycle.py:1021-1027`, `repos.py:113-115`, refusal returns "skip" and records nothing); the six-row table (`hold.py:146-168`); switch-on gate (NG-2 amendment, then the Change 3 gate). The base fact 8 content is carried into the section intro and bullets.
- Provenance tag: `Variant 2 (CLAY), Section Mechanism and Cited fact 2 (github.py:983-992) - merged per Change #2`; fact 8 tagged `Base (original, modified)`
- Validation: "replaces the base's one-line fact 8" read as "replace its text with a pointer" so numbering holds; the Risk Summary rollback ("revert to the one-line fact 8") stays possible.

### Change 3: `would_hold` listing and switch-on gate
- Status: Applied
- Source: Variant 2 fact 3; moderator note on X-003
- Target: the dry-run sentence in "What it gets right" and the Risks section
- Before: "`--dry-run` shows holds before any write" listed among the parts kept.
- After: That clause is removed from the kept list. A new paragraph says `--dry-run` is kept in part: `would_hold` and `would_release` are filled today only in the label branches (`cycle.py:1065-1078`), the rework keeps `would_hold` and drops `would_release` (no write to preview), and D09 makes the 24-hour dry-run shadow run the switch-on gate. Risks gains a bullet: the later label write is switched on only after the 24-hour dry-run shadow run plus a cron label-write test.
- Provenance tag: `Base (original, modified) - Change 3 ...` on both sections
- Validation: the plan's "fact 7 of 'What it gets right'" has no numbered fact in the base; it was read as the dry-run sentence. The plan does not describe the "cron label-write test" beyond its name, so the text uses only that name and adds no detail.

### Change 4: Priced costs
- Status: Applied
- Source: Variant 2 Costs and fact 6; Variant 1 advocate concessions
- Target: Costs
- Before: one sentence: rework of `_hold_step` (about 75 to about 30 lines) and tests; a rebase request; person-placed `hold:plan` stops being a stop signal; a later label PR must repeat some tests.
- After: six bullets: rework with figures marked rough and unmeasured (C-005 unresolved); `test_hold.py` is 1,073 lines and 58 tests; rebase request; hand-placed `hold:plan` (row 6) stops being a stop signal (C-011, 65%, minor); restoring the write is a second PR with the NG-2 amendment (C-009, 65%) and repeats some tests; the fallback (delete only the write calls, keep the table and entry creation, drop `issue.hold` from the reference config).
- Provenance tag: `Base (original, modified) - Change 4 and Change 6; the base sentence is split into bullets`
- Validation: every added item appears in the plan's Change 4 integration list or in the "Changes NOT Being Made" rationale column; no figure was added beyond those in the plan and the sources.

### Change 5: Sizing step and open points
- Status: Applied
- Source: Variant 2 concession; Variant 1 advocate concession on A-002
- Target: new section "Conditions and open points" after Risks
- Before: no such section.
- After: states the debate did not converge (71.4%, depth quick, moderator resolved six open points); the condition (size the rework before asking Clay, A-002 qualified by both advocates); a sizing step built from the base fact 6 inventory; three open points (C-002 at 55%, C-005, C-007 at 50%).
- Provenance tag: `Variant 2 (CLAY), Section Costs and concessions (concession on A-002) - merged per Change #5`
- Validation: C-002, C-005 and C-007 are the unresolved points named in the plan; the "Variant 2 advocate's own hybrid" wording follows the plan's C-002 rationale, which says "the advocate's own hybrid" (read as the Variant 2 advocate).

### Change 6: Base corrections
- Status: Applied (all listed fixes done; see the note on facts 7 and 9)
- Source: Step 3 evaluators; X-003
- Target: Mechanism, Cited facts 2, 7 and 9, Costs, What it gets right, new Success tests
- Before / After, by fix:
  1. Fact 2: "`HOLD_LABEL` appears only in `predicates.py:30`, `hold.py`, `cycle.py`, `github.py`, `record.py`" became "`HOLD_LABEL` is defined in `predicates.py:30` and the name is used in `hold.py`, `cycle.py`, `github.py` and `record.py`; the text `hold:plan` itself appears only in the `record.py` docstring (source files, not tests)".
  2. Mechanism: "No label read" became "The poll makes no `hold:plan` label read", with a parenthesis that `hold:backlog` is still read from the search row (`cycle.py:1052`, moderator fact M3) so the two statements do not clash.
  3. Rows: Mechanism now defines the six-row table once (`hold.py:146-168`) and names rows 3, 4 and 6; "rows 3 to 5" is used everywhere in the document (Cited fact 6, Costs, Conditions); the gap to Clay's "rows 3 to 6" is explained as row 6.
  4. Dry-run: the claim "shows holds before any write" is gone, replaced per Change 3.
  5. Success tests: new section with four items (zero-write test with the grant absent; a leftover label does not block a passing issue; entry created with no write; grant not listed in the reference config).
- Provenance tag: `Base (original, modified) - Change 6 ...` on Mechanism, fact 2, Costs, What it gets right and Success tests
- Validation: fix 1 adds the qualifier "(source files, not tests)", which is an interpretation, because fact 3 quotes `hold:plan` from a test file; without it the two facts would contradict. Facts 7 and 9 are listed as targets, but the Fixes list names no change for them; they were left as base text (not improvised). The definition of row 6 comes from diff point C-011; row 5 is not described in any source and is not described in the document.

## Post-Merge Validation

### Structural Integrity
- Heading hierarchy: one H1 (title), nine H2 sections, no skipped levels. PASS.
- Section order: Claim, Mechanism, Cited facts, Costs, The deferred label-write form (after Costs, per Change 2), Risks, Conditions and open points (after Risks, per Change 5), What it gets right, Success tests. The base order is kept; new sections sit where the plan puts them. PASS.
- Provenance: the three header lines are the first three lines; every H1 or H2 block has a `<!-- Source: ... -->` comment before it, and facts 2, 8, 10 and 11 carry inline source comments. PASS.
- Style: no em dashes or en dashes (grep count 0). PASS.
- Numbering note: fact list reads 1, 2, 3, 4, 5, 10, 11, 6, 7, 8, 9 on purpose (see Change 1).

### Internal References
- Total: 13 (fact 10 and fact 11 from Mechanism; "see Costs" in Mechanism; "see fact 5" in fact 11; the fact 8 pointer to the deferred form section; "described under Risks" in the deferred form section; "listed under Costs", "fact 4" and "see What it gets right" in Conditions; fact 5, fact 11, Risks and fact 10 in Success tests)
- Resolved: 13
- Broken: 0

### Contradiction Re-Scan
- New contradictions introduced: 0 found.
- Checked and cleared: (a) "no `hold:plan` label read" against the `hold:backlog` read from the search row: stated side by side in Mechanism; (b) fact 2 ("text `hold:plan` only in the `record.py` docstring") against fact 3 and Success tests, which quote `hold:plan` from tests and prose: the qualifier "source files, not tests" covers it; (c) "rows 3 to 5" against Clay's "rows 3 to 6": reconciled in Mechanism; (d) `would_hold` kept in What it gets right against the base claim that `--dry-run` is "kept": base wording replaced, no leftover.
- Residual item for the orchestrator: the qualifier in fact 2 is an interpretation of the plan (see Change 6 Validation).

## Summary

- Planned: 6
- Applied: 6
- Failed: 0
- Skipped: 0
- Result: PASS

## Notes

- Base recommendation unchanged: ship a read-only hold now, remove the label-writing code from PR 686, defer the label write to its own PR with an NG-2 amendment.
- The plan header shows an approval time of 2026-11-20T08:20:00Z, later than the merge timestamp taken from the system clock (08:04:47Z). The merge timestamp is the real clock reading; the plan time was not changed.
- Nothing outside the two output files was written; no repository, gh or Orca action was taken.

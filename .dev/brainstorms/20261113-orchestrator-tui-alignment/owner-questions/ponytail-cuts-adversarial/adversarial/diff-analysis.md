# Diff Analysis: cut-list comparison

## Metadata
- Generated: 2026-11-16 (orchestrating session, Step 1 of `/sc:adversarial --depth quick`, Mode B)
- Variants compared: 3 (V1 opus:architect aggressive, V2 sonnet:security conservative, V3 haiku:analyzer evidence-first)
- Source: `/home/coder/workspaces/worktrees/IronClaude/issue-339-orchestrator-mode/.dev/brainstorms/20261113-orchestrator-tui-alignment/owner-questions/ponytail-cuts-adversarial/source-cut-candidates.md`
- Categories: structural (3), content (18), contradictions (5), unique (7), shared assumptions (6)

## Structural Differences
| # | Area | V1 | V2 | V3 | Severity |
|---|---|---|---|---|---|
| S-001 | Rows | 22 + C23a + C24 | 22 + C23b | 22 | Low |
| S-002 | Evidence block | inline per row | inline per row | separate "claims checked (a) to (g)" list | Low |
| S-003 | Same ID C23 means different items (V1 watcher deadline, V2 "do not carry commits") | C23a | C23b | none | Medium (renamed C23a and C23b here) |

## Content Differences
Verdict key: CUT, DEFER, KEEP, MODIFY. Unanimous points are listed last.

| # | ID | V1 | V2 | V3 | Severity |
|---|---|---|---|---|---|
| C-001 | C01 Q7 backup | CUT ceremony | MODIFY (local copy + sha256, no push) | MODIFY (backup is not authorship) | Medium |
| C-002 | C02 Q24 one capture | CUT | CUT (keep output untracked) | KEEP | Medium |
| C-003 | C03 Q41 | CUT (close) | MODIFY (confirm in next reply) | KEEP | Medium |
| C-004 | C04 Q13 | CUT | CUT | KEEP | Medium |
| C-005 | C05 Q15 | CUT | MODIFY (cut card, keep caveat) | KEEP | Medium |
| C-006 | C06 Q14 | CUT options 2, 3 | CUT | DEFER | Low |
| C-007 | C10 Q20 | DEFER | DEFER (conditional) | KEEP | Low |
| C-008 | C12 approval flow | CUT (needs owner) | KEEP | KEEP | High |
| C-009 | C14 live tests first | MODIFY | MODIFY (Task 16 stays first) | DEFER | Low |
| C-010 | C15 `slo_numbers` | CUT | DEFER | KEEP | Medium |
| C-011 | C17 delete panel code | CUT (needs owner) | DEFER | DEFER | High |
| C-012 | C18 snapshot only with flag | CUT | DEFER | DEFER | Medium |
| C-013 | C20 v2 design | CUT effort | DEFER | DEFER | Low |
| C-014 | C21 gate rule and constant | MODIFY (constant only with C17) | KEEP | KEEP | Medium |
| C-015 | C23a watcher 30-day deadline | DEFER then delete (needs owner) | not raised | not raised | High |
| C-016 | C23b side-branch commits | not raised | KEEP out of any PR | not raised | High |
| C-017 | C24 retire `/sc:task` | CUT (own go) | not raised | not raised | Low (out of scope) |
| C-018 | Unanimous: C07, C08, C09, C11 DEFER; C13, C22 KEEP; C16 CUT; C19 MODIFY (caveat only) | agree | agree | agree | none |

## Contradictions
| # | Point | Position A | Position B | Impact |
|---|---|---|---|---|
| X-001 | Direction of the C12 risk | Source and V1: dropping GitHub input loses the stranger-comment defence | V2: backwards, with no GitHub input there is nothing to forge | High |
| X-002 | C15: is there a caller of `slo_numbers`? | Source: no caller in `src/` | V1, V2, V3: docs cite it (`issue-watcher-setup.md:470`, `:680`; V1 also `issue-watcher.md:232`, `:867`, `:902`) | Medium |
| X-003 | Panel test count | V3: 56 named functions | V2: 26 dedicated functions; V1: 836 question-only test lines | Low |
| X-004 | Number of Orca finders | Source: three | V2: two (same logic) plus one deliberate sweep rule; V1 and V3 agree | Low |
| X-005 | Safe way to back up the side checkout (C01) | V1: copy by an agent only with the owner's written OK | V2: never push or commit it; commit `1ae72e1a1` sets `QUESTION_GATE_PASSED = True` | High |

## Unique Contributions
| # | Variant | Contribution | Value |
|---|---|---|---|
| U-001 | V2 | sha256 list outside git as the backup record | Medium |
| U-002 | V2 | Keep the pasted Orca capture untracked (public repo) | Medium |
| U-003 | V2 | Task 16 should stay first and unblocked even if live tests go first | High |
| U-004 | V3 | Candidate executable is run once by the discovery probe (C04 residual) | Low |
| U-005 | V3 | Panel gate rule cites release-gates.md lines 22 and 50 | Medium |
| U-006 | V1 | C21 constant goes only together with C17 | Medium |
| U-007 | V1 | C24: carrying out the retirement of `/sc:task` is outside this program | Low |

## Shared Assumptions
| # | Agreement source | Assumption | Classification | Promoted |
|---|---|---|---|---|
| A-001 | All variants | Owner time is the scarce resource, so removing a question is a gain | STATED | no |
| A-002 | All variants | Nobody except the owner uses the observer or watcher: the evidence is this host and this checkout only | UNSTATED | yes |
| A-003 | All variants | Line and test counts from the reviews are roughly right; most were not checked | UNSTATED | yes |
| A-004 | V1, V2 | When a card is dropped, the card's "if you do not answer" outcome is safe to apply | UNSTATED | yes |
| A-005 | V1 | Git history makes any deletion reversible at low cost (not counting a new security review) | STATED (V1 only) | yes |
| A-006 | All variants | An agent may edit the owner's question document, which the owner is editing and pushing too, without recording an owner answer | UNSTATED | yes |

## Summary
- Structural 3, content 18, contradictions 5, unique 7, shared assumptions 6 (UNSTATED 5, STATED 2 counting A-005; CONTRADICTED 0).
- Highest-severity items: C-008, C-011, C-015, C-016, X-001, X-005.
- Points the three variants agree on: 8 of 22 IDs (C07, C08, C09, C11, C13, C16, C19, C22).

<!-- Provenance: produced by /sc:adversarial via /sc:reflect Wave 4 -->
<!-- Base: reviewer-2 (qa, haiku class) card; uniques from rv1 (analyzer, sonnet) and rv3 (refactorer, opus) -->
<!-- Merge date: 2026-11-13T05:25:00Z -->

# Merged verdict — comboA-r3 (21 findings in, 19 merged findings out)

## Merged findings
| ID | Src | Severity | Blocking | Category | Claim (abridged) | Calib |
|----|-----|----------|----------|----------|------------------|-------|
| M-1 | rv1-F1 | MAJOR | no | missing-requirement | No AC asserts the minted cycle_id is shared by guard events, push triad key and rereview_requested (spec 4.6); Task 11 trace asserts order only | 0.80 |
| M-2 | rv2-F1' | MAJOR | no | unpassable-check | 9 of 12 Task-11 scenario tests have name-only ACs (empty bodies pass); retry-once (FR-16), no-edit-after-halt observable, held-exit enumeration unasserted | 0.70 |
| M-3 | rv2-F2' | MAJOR | no | unpassable-check | Scenario tests exercise a test-owned driver, not the SKILL protocol; Task 8 phrase-grep does not bind SKILL behavior to the ref (narrowed: live behavior is the owner's release gate) | 0.75 |
| M-4 | rv2-F3 | MAJOR | no | unpassable-check | classify_toggles ACs never test the unsettled slack term or the run_toggles+slack vs +1 boundary | 0.70 |
| M-5 | rv2-F4 | MAJOR | no | missing-requirement | Ready-then-draft round trip (FR-13) in Task 4 body but absent from its ACs | 0.80 |
| M-6 | rv2-F5 | MAJOR | no | missing-requirement | FR-17 held-exit list never enumerated; phrase-presence only | 0.65 |
| M-7 | rv2-F6 | MAJOR | no | missing-requirement | FR-20 once-per-cycle-id has no AC; no engage row blocks re-engage after RELEASED; next_cycle_number untested with mixed kinds | 0.65 |
| M-8 | rv3-F1 | MINOR | no | missing-requirement | T9/T10/T12/T13 consume pre-build-gate.md with no direct Depends on T1 (transitive only); T10/12 and T5/7 edit shared test files unordered | 0.70 |
| M-9 | rv3-F2 | MINOR | no | other | Byte-identical pin check uses start-text constants; whole-sentence constants would catch later-sentence edits | 0.50 |
| M-10 | rv3-F3 | MINOR | no | missing-requirement | Per-task classification covers gh pr / gh api lines only; git write verbs (also WRITE_VERB_RE hits) uncovered by the wording | 0.70 |
| M-11 | rv1-F5 + rv3-F4 | MINOR | no | unpassable-check | Wave 0 bullet must carry "at L3 with --merge-guard off ... no draft call" while its test rejects L3/draft gate wording: literal-check ambiguity (two-class agreement) | 0.40/0.65 -> 0.5 |
| M-12 | rv2-F7 + rv3-F6 | MINOR | no | missing-requirement | PR-body gate statement and open-with-off rule recorded in T1 but owned by no task (release-gate scope per spec:326; advisory) | 0.70/0.60 -> 0.65 |
| M-13 | rv1-F2 | MINOR | no | missing-requirement | Moved-head HOLD case not in T11 case enumeration/ACs (only merged-PR case spelled out) | 0.70 |
| M-14 | rv1-F3 | MINOR | no | missing-requirement | auto_merge_armed ENGAGE note (FR-11) has no AC | 0.70 |
| M-15 | rv1-F4 | MINOR | no | missing-requirement | T8 protocol-test phrase list omits the pre-push OPEN/pr_not_open check | 0.70 |
| M-16 | rv3-F5 | MINOR | no | missing-requirement | Fixed-decisions constraint bullet drops the Medium-or-higher routed-finding trigger present in the spec header | 0.70 |
| M-17 | rv2-F8 | MINOR | no | unpassable-check | T1 base-commit record self-written; no-network criterion uncheckable | 0.45 |
| M-18 | rv2-F9 | MINOR | no | unpassable-check | RECONCILE ambiguous defined as "anything else" without required inputs | 0.50 |
| M-19 | rv2-F10 | MINOR | no | unpassable-check | L2-line AC is bare presence; fresh-monitor-2 condition and output-table placement untested | 0.55 |

Severity outcome: 0 CRITICAL, 7 MAJOR (all non-blocking after debate), 12 MINOR. Wrong-implementation risk concentrated in M-1..M-7.

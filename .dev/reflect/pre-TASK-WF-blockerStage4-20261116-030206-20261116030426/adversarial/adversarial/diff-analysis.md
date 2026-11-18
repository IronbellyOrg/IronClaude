# Diff Analysis: reviewer-card comparison (pre-execution review of the stage 4 plan)

## Metadata
- Generated: 2026-11-16T03:30:00Z
- Variants compared: 3 (V1 = reviewer 1, analyzer, sonnet class; V2 = reviewer 2, qa, haiku class; V3 = reviewer 3, refactorer, opus class)
- Total differences found: 25
- Categories: structural (2), content (15), contradictions (3), unique (8), shared assumptions (3)
- Subject of all three cards: the stage 4 plan `.dev/tasks/to-do/TASK-WF-blockerStage4-20261116-030206/TASK-WF-blockerStage4-20261116-030206.md` (P4:n = its line n; S1, S3 = stage 1 and stage 3 plans; OLD = base 46-task plan)
- Severity rule in force: blocking = a requirement or check that cannot be met, a wrong or missing result, or data loss; minor = wording or format.

## Structural Differences

| # | Area | V1 | V2 | V3 | Severity |
|---|------|----|----|----|----------|
| S-001 | Card format | `F<n>` lines, `Checked`, `Self-report` (as the brief asks) | Deviation-table style (`D1`..`D4`), adherence summary, base-task comparison notes | `F<n>` lines, step-by-step Task 6 walk under `Checked` | Low |
| S-002 | Severity labelling | MAJOR/MINOR plus `blocking true/false` agree on every line | Each row carries two labels that disagree: "MAJOR; blocking true" next to "Table severity: MEDIUM" (D1, D2), "MINOR; blocking false" next to LOW | MAJOR/MINOR plus blocking flag agree | Medium |

## Content Differences

| # | Topic | V1 | V2 | V3 | Severity |
|---|-------|----|----|----|----------|
| C-001 | Task 1 acceptance line 2 (stage 3 summary "states that one audit window has passed", P4:37) vs stage 3 plan (S3:158, S3:162) | F1 blocking: cannot be met | D2 blocking: cannot be met | F1 blocking: cannot be met; names the ledger go row as the record that exists after the window | High (all agree on the defect) |
| C-002 | Task 5 acceptance line "grep follow-up candidates prints nothing" (P4:89) vs the pinning test `tests/skills/test_review_severity_mapping.py` | F2 blocking: the test pins the phrase and "asks the user once per loop" in the spec-panel Grading and Verdict bullets (source and plugin); no stage 4 task re-pins or runs it | not raised | not raised ("Step 7 no failure expected" for the three named tests) | High |
| C-003 | Name of the allow-list location in Tasks 1 and 3 ("allow-list of the stage 3 scan test", P4:33, P4:59) | F3 minor: the list is in `refs/scale-map.md` | not raised | F5 minor: same | Low |
| C-004 | Task 3 acceptance line 3, literal "After 2 fix cycles" (P4:64) | F4 minor: the tdd file has only lowercase "after" (`build-request-template.md:125`) | not raised | not raised | Low |
| C-005 | Task 5 acceptance line 2 reaches the FR-8 rule (`spec-panel.md:332`) outside the listed edit lines | F5 minor: also pinned by the mapping test | not raised | not raised | Low |
| C-006 | Pinning tests run in one task only or never | F6 minor: `test_review_brief_placement.py:134` (plugin prompt byte copy), `test_review_prompt_overrides.py` (Task 2 only), `test_review_severity_rule.py` (never) | not raised | F4 minor (second half): `test_review_severity_rule.py` not run; Task 4 runs only the task-builder test | Medium |
| C-007 | Task 5 pointer and parity assertion wording (P4:84, P4:90) | F7 minor: edit text never says to add a pointer to `spec-panel.md` | Task 7 note (ordering of the closing sentence) only | not raised | Low |
| C-008 | Owner-gate checks sit in acceptance lines read after the edits | F8 minor | not raised | not raised | Low |
| C-009 | Acceptance lines not pinned by content ("T1 passes", "consumer-line instruction", "the L1 merge text") | F9 minor | not raised | F4 minor (first half) for the MDTM consumer line | Low |
| C-010 | Plan generated before its preconditions hold (request says "Generate it only after"; ledger cells empty) | not raised | D1 blocking (MAJOR; table says MEDIUM) | not raised | Medium |
| C-011 | Task 2 has no cap-sentence acceptance line although the request keeps caps by content (`source.md:12`) | not raised | D3 minor | not raised | Low |
| C-012 | Coverage matrix omission: "Earlier stages' evidence is read by package id" (`source.md:7`) | not raised | D4 minor | not raised | Low |
| C-013 | Strict T2 scans git-tracked files only; the plugin mirror is never staged in Task 6, so "accepted by the reverse scan" is vacuous | not raised | not raised | F2 minor | Low |
| C-014 | Task 6 adds a second `canonical` row with a repo path although registry rows are logical install-root paths with a `surfaces` list | not raised | not raised | F3 minor | Low |
| C-015 | Task 4 consumer line could land inside a digest fence in the MDTM templates and break T1 | not raised | not raised | F4 minor (first half) | Low |

## Contradictions

| # | Point of Conflict | V1 | V2 | V3 | Impact |
|---|-------------------|----|----|----|--------|
| X-001 | Whether Task 5 can leave the package with a red test | F2: yes, the mapping test fails after Task 5 and no task owns it | D-notes: "No later task here falsifies an earlier task's stated acceptance line" (about acceptance lines, not tests) | Checked: Step 7 "no failure expected apart from F2 and F3" (about the three named tests) | Medium |
| X-002 | Whether files edited in several tasks end in a consistent state | F6: the plugin prompt must stay byte-identical to the source (test at `test_review_brief_placement.py:134`) but Task 5 says edit each file in place | not raised | Checked: "files edited by several tasks end up consistent" | Medium |
| X-003 | Grading of one defect inside V2 | D1 is labelled "MAJOR; blocking true" in its body and "MEDIUM" in its table column | same card | not raised | Low |

## Unique Contributions

| # | Variant | Contribution | Value Assessment |
|---|---------|--------------|------------------|
| U-001 | V1 | The mapping-test pin (C-002) found by reading the tests directory | High |
| U-002 | V1 | The byte-identity test for the plugin rules prompt (C-006, X-002) | Medium |
| U-003 | V2 | Task-by-task comparison with base Tasks 41 to 46 (what changed in wording and why) | High |
| U-004 | V2 | Explicit check of earlier findings F3, F4, F5, F6, F9, F12, F13 against the plan | High |
| U-005 | V2 | Generation-order observation (C-010) | Medium |
| U-006 | V3 | Step-by-step walk of Task 6 with the state of registry, allow-list, plugin tree and tests at each step | High |
| U-007 | V3 | Tracked-files-only scan consequence (C-013) | Medium |
| U-008 | V3 | Registry row model mismatch (C-014) | Low |

## Shared Assumptions

| A-NNN | Assumption | Source Agreement | Impact | Status |
|-------|------------|------------------|--------|--------|
| A-001 | The stage 1 and stage 3 packages will be implemented as their plans read (tests T1, T2, T3, the scan test and the re-pinned tests exist as described) | All three treat the stage 1 and 3 plans as the contract for files that do not exist yet | A finding that rests on a stage 1 or 3 text changes if those plans are revised; V3 says so explicitly | UNSTATED (V3 STATED it for F2 and F3 only) |
| A-002 | The `/sc:implement` per-task QA reads each acceptance line literally and fails the task when it cannot be met | All three grade "cannot be met" lines blocking | If QA reads loosely (case-insensitive, by content) several minor findings vanish and C-001 becomes a guess-pass instead of a halt | UNSTATED |
| A-003 | Task 1's second acceptance line is meant to be checked against the stage 3 summary file and not against the ledger row | All three treat P4:37 as a check on the file | If the plan author meant the owner's go row (P4:36) to carry the window evidence, C-001 is a wording defect and not an unmeetable check | UNSTATED |

## Summary
- Total structural differences: 2
- Total content differences: 15
- Total contradictions: 3
- Total unique contributions: 8
- Total shared assumptions surfaced: 3 (UNSTATED: 3, STATED: 0, CONTRADICTED: 0)
- Highest-severity items: C-001, C-002
- Taxonomy: L3 (state mechanics, guards, invariants): C-001, C-002, C-006, C-013, X-001, X-002, A-001, A-002; L2 (structural, interface): C-003, C-005, C-007, C-014, C-015, C-009; L1 (surface wording): S-001, S-002, C-004, C-011, C-012, X-003; C-008, C-010 are L2.

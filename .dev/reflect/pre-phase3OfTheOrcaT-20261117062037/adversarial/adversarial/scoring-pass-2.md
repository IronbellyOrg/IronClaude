# Qualitative scoring, pass 2 (order: V3, V2, V1)

Basis: final rulings table in debate-transcript.md and round-2-v3.md. Final blocking set: C-001 (--once Collector at commands.py:218), C-002 (keys line shown with link off), C-003 (snapshot dispatch-id check cannot pass with a linked worker). MEDIUM: C-004, C-005, C-006, C-009, C-011, C-012, C-013. Mapping: V1 = analyzer/sonnet, V2 = qa/haiku, V3 = refactorer/opus. Evidence is quoted from the variant card only.

## V3 (refactorer, opus)

### Completeness
| # | CLAIM | EVIDENCE | VERDICT |
|---|---|---|---|
| 1 | Covers the plan's requirements and the ruled points | F1 (C-001), F2 (C-004), F3 (C-002), F5 (C-003), F6 (C-011), F8 (C-012), F9 (C-013), F11 (C-006); "uncovered_requirements: INF-001 ... INF-013" | MET |
| 2 | Edge cases and failures | F2 "n can never make the first selection"; F9 "an evicted selected identity shows `selected <id> no longer in source window`" | MET |
| 3 | Names dependencies | F4 "Task 6 depends only on 4a"; F8 conftest builder `make_question_rows` | MET |
| 4 | Success criteria for fixes | F1 "add a test_commands check that --once with a payload reply prints link=linked" | MET |
| 5 | Out of scope or not checked | "Not checked: rows T57 to T66 ... No files written"; "deliberate omissions (options, taskId, worktree-wide set, snapshot changes)" | MET |
Subtotal 5

### Correctness
| # | CLAIM | EVIDENCE | VERDICT |
|---|---|---|---|
| 1 | No factual errors | "INF-009: only a constraint" (conceded wrong, test_commands.py:652-667 pins argv); "unverified-register.md line 33 ... exist only after execution" (corrected: line 33 exists now); F3 and F5 under-graded MEDIUM against final BLOCKING | NOT MET |
| 2 | Feasible approaches | F2 "define 'link on' as some line in panel.lines having a non-empty `link`" is workable (adopted in round 2) | MET |
| 3 | Terminology accurate | F7 class "Regression" (final: Gap/NOTE); F5 "Drift" (final: Gap); F4 "Drift" for a reviewability issue | NOT MET |
| 4 | No internal contradictions | Findings and uncovered list agree with each other | MET |
| 5 | Claims supported | File:line cites on each finding, e.g. "view.py:78-81, 914" | MET |
Subtotal 3

### Structure
| # | CLAIM | EVIDENCE | VERDICT |
|---|---|---|---|
| 1 | Logical ordering | BLOCKING F1, then MEDIUM F2-F9, then NOTE F10-F12 | MET |
| 2 | Consistent hierarchy | Every finding uses `F# | task | SEVERITY | class | cite` | MET |
| 3 | Separation of concerns | findings / uncovered_requirements / checked blocks | MET |
| 4 | Navigation aids | "INF-001: partly (run_once path; F1)" | MET |
| 5 | Required card format | Only F1 has plan_says/reality/wrong_outcome/fix; F3-F12 collapse them into prose | NOT MET |
Subtotal 4

### Clarity
| # | CLAIM | EVIDENCE | VERDICT |
|---|---|---|---|
| 1 | Unambiguous | F2 "define 'link on' as some line in panel.lines having a non-empty `link`" | MET |
| 2 | Concrete | F7 "pinned at test_commands.py:740" | MET |
| 3 | Clear purpose per finding | each finding states a wrong outcome or a fix | MET |
| 4 | Terms defined on first use | "AD-18 [ADOPTED]", "CAP-12", "R3", "desk", "INF-xxx" are never defined | NOT MET |
| 5 | Actionable next step | every finding has `fix:`; F10 "Task 7 adds one line that B remains the default" | MET |
Subtotal 4

### Risk coverage
| # | CLAIM | EVIDENCE | VERDICT |
|---|---|---|---|
| 1 | >=3 risks with severity and impact | F1 BLOCKING "with --once the link stays off"; F3 "footer advertises dead n/p keys"; F6 "built code contradicts an adopted architecture decision" | MET |
| 2 | Fix for each | `fix:` on F1-F12 | MET |
| 3 | Failure modes and recovery | F4 "too big to review or roll back as one unit" | MET |
| 4 | External dependencies and their failure | none; no payload, worker-read or runner failure case | NOT MET |
| 5 | Detection | F1 "add a test_commands check ..." | MET |
Subtotal 4

### Invariant and edge-case coverage
| # | CLAIM | EVIDENCE | VERDICT |
|---|---|---|---|
| 1 | Collection boundaries | F9 evicted selection; F2 first selection | MET |
| 2 | State across components | F2 "CycleResult has no link field; ... View.desk exists only once a question is selected" | MET |
| 3 | Guard gaps | F3 "QUESTIONS_KEYS_LINE is used whenever the question panel exists" | MET |
| 4 | Count divergence | No width, line-count or cap figure anywhere (F3 gives none) | NOT MET |
| 5 | Feature interactions | F3 link off with the questions panel; F1 `--once` with link | MET |
Subtotal 4

V3 total 24/30. Floor check on last dimension (4/5): eligible.

## V2 (qa, haiku)

### Completeness
| # | CLAIM | EVIDENCE | VERDICT |
|---|---|---|---|
| 1 | Covers requirements and ruled points | Only F1-F4 (C-003, C-001, C-002, C-009). No C-004, C-005, C-006, C-011, C-012 or C-013 | NOT MET |
| 2 | Edge cases | F4 "missing worker fields and resource.worktreeId ... failed or stale worker-read cases" | MET |
| 3 | Dependencies | "the new question_message builder is created before its dependents; declared dependencies have no ordering defect" | MET |
| 4 | Success criteria | F2 "command-level tests ... closing the gate restores existing behaviour" | MET |
| 5 | Not checked | "No commands run"; uncovered_requirements lists INF-013 "no delivery check" | MET |
Subtotal 4

### Correctness
| # | CLAIM | EVIDENCE | VERDICT |
|---|---|---|---|
| 1 | No factual errors | F1 "a linked question necessarily shares its dispatch id" and "a realistic linked fixture cannot pass" (overstated, conceded round 2); confidence 0.97 judged too high | NOT MET |
| 2 | Feasible | F1 "restrict the dispatch-id exclusion to the snapshot's `questions` group" (adopted in final change 3) | MET |
| 3 | Terminology | F1 class "Regression" (final: Gap) | NOT MET |
| 4 | No contradictions | consistent | MET |
| 5 | Supported | "export.py:26 has dispatchId in _TEXT_FIELDS and line 195 exports all worker rows" | MET |
Subtotal 3

### Structure
| # | CLAIM | EVIDENCE | VERDICT |
|---|---|---|---|
| 1 | Ordering | B, B, B, M | MET |
| 2 | Hierarchy | uniform finding layout | MET |
| 3 | Separation | findings / uncovered / checked | MET |
| 4 | Navigation | "INF-001: partially (...; F2)" | MET |
| 5 | Card format | F1-F4 each carry plan_says, reality, wrong_outcome, fix | MET |
Subtotal 5

### Clarity
| # | CLAIM | EVIDENCE | VERDICT |
|---|---|---|---|
| 1 | Unambiguous | F2 "pass link=_link_on(options) at both sites" | MET |
| 2 | Concrete | "plan line 103", "view.py:914" | MET |
| 3 | Purpose per finding | wrong_outcome on each | MET |
| 4 | Terms defined | "desk", "R1 surface", "INF-xxx", "link-off" undefined | NOT MET |
| 5 | Actionable | each `fix:` names the change and a test | MET |
Subtotal 4

### Risk coverage
| # | CLAIM | EVIDENCE | VERDICT |
|---|---|---|---|
| 1 | >=3 risks with severity and impact | F1-F3 BLOCKING each with wrong_outcome | MET |
| 2 | Fixes | each finding | MET |
| 3 | Failure modes and recovery | F2 "closing the gate restores existing behaviour"; F1 executor "removes worker identifiers (weakening the snapshot contract)" | MET |
| 4 | External dependency failure | F4 "failed or stale worker-read cases asserting the freshness qualification" | MET |
| 5 | Detection | F3 "add a byte-for-byte link-off screen comparison ... at all three widths" | MET |
Subtotal 5

### Invariant and edge-case coverage
| # | CLAIM | EVIDENCE | VERDICT |
|---|---|---|---|
| 1 | Collection boundaries | F4 missing worker fields; F1 matching worker in or out of rows | MET |
| 2 | State across components | F2 `run_once` builds a Collector without the argument | MET |
| 3 | Guard gaps | F3 "selects QUESTIONS_KEYS_LINE whenever a question panel exists, independent of the link switch" | MET |
| 4 | Count divergence | F3 "its length can alter wrapping and the height budget" (names the cap effect, no figures) | MET |
| 5 | Feature interactions | F3 "the R1 surface alone does not exercise this" | MET |
Subtotal 5

V2 total 26/30. Floor check (5/5): eligible.

## V1 (analyzer, sonnet)

### Completeness
| # | CLAIM | EVIDENCE | VERDICT |
|---|---|---|---|
| 1 | Covers requirements and ruled points | F1 (C-001), F2 (C-004), F3 (C-002), F4 (C-005), F5 (C-006), F6 (C-003), F7 (C-008), F8 (C-007); misses C-011, C-012, C-013 only | MET |
| 2 | Edge cases | F5 "payload dispatchId `unknown` can join an identity-unknown row"; F4 "a tall desk pushes spare below 1" | MET |
| 3 | Dependencies | F2 "CycleResult ... Session and View carry no link field", names the source to add | MET |
| 4 | Success criteria | F1 "a test_commands test that `--once` with a linked reply gives `dispatchId=` and `link=linked`" | MET |
| 5 | Not checked | "No tests run"; "[INFERRED]" tags; INF-013 "delivery action with no check" | MET |
Subtotal 5

### Correctness
| # | CLAIM | EVIDENCE | VERDICT |
|---|---|---|---|
| 1 | No factual errors | No factual error found, but F3 and F6 graded MEDIUM against final BLOCKING; "18 of 18" is not shown in the card | NOT MET |
| 2 | Feasible | F4 "replace [the desk] with the one-line notice ... never remove the list" | MET |
| 3 | Terminology | classes match final rulings (F1 Gap, F3 Regression, F6 Gap) | MET |
| 4 | No contradictions | consistent | MET |
| 5 | Supported | file:line on each; uncertain claims tagged "[INFERRED]" | MET |
Subtotal 4

### Structure
| # | CLAIM | EVIDENCE | VERDICT |
|---|---|---|---|
| 1 | Ordering | BLOCKING F1, MEDIUM F2-F6, NOTE F7-F8 | MET |
| 2 | Hierarchy | uniform | MET |
| 3 | Separation | findings / uncovered / checked | MET |
| 4 | Navigation | "INF-001: --once path never gets the link (F1)" | MET |
| 5 | Card format | F1-F6 carry plan_says, reality, wrong_outcome, fix; NOTEs compact | MET |
Subtotal 5

### Clarity
| # | CLAIM | EVIDENCE | VERDICT |
|---|---|---|---|
| 1 | Unambiguous | F2 "or define link-on as any QuestionLine.link != ''" | MET |
| 2 | Concrete | F3 "about 107 chars ... about 121 chars = 2 lines at width 116 or 120" | MET |
| 3 | Purpose | wrong_outcome on each | MET |
| 4 | Terms defined | "desk", "spare", "UNKNOWN sentinel", "INF-xxx" undefined | NOT MET |
| 5 | Actionable | `fix:` on all | MET |
Subtotal 4

### Risk coverage
| # | CLAIM | EVIDENCE | VERDICT |
|---|---|---|---|
| 1 | >=3 risks with severity and impact | F1 BLOCKING, F3, F4 each with wrong_outcome | MET |
| 2 | Fixes | each | MET |
| 3 | Failure modes and recovery | F4 degrades to a one-line notice and keeps the list | MET |
| 4 | External dependency failure | F7 invalid or non-string payload dispatchId; F5 absent id in the source | MET |
| 5 | Detection | F1 test_commands test; F6 "assert only the `questions` group plus byte-identity" | MET |
Subtotal 5

### Invariant and edge-case coverage
| # | CLAIM | EVIDENCE | VERDICT |
|---|---|---|---|
| 1 | Collection boundaries | F4 "spare below 1" and the whole panel collapses | MET |
| 2 | State across components | F2 CycleResult / Session / View lack a link field | MET |
| 3 | Guard gaps | F2 "View.desk is None until a question is selected, so it cannot gate the first `n`" | MET |
| 4 | Count divergence | F3 107 to 121 chars, "2 lines at width 116 or 120", "`spare` ... drops one" | MET |
| 5 | Feature interactions | F3 link off with questions on; F5 UNKNOWN sentinel with the export `or "unknown"` | MET |
Subtotal 5

V1 total 28/30. Floor check (5/5): eligible.

## Summary
| Variant | Compl | Corr | Struct | Clar | Risk | Invariant | Total |
|---|---|---|---|---|---|---|---|
| V3 | 5 | 3 | 4 | 4 | 4 | 4 | 24 |
| V2 | 4 | 3 | 5 | 4 | 5 | 5 | 26 |
| V1 | 5 | 4 | 5 | 4 | 5 | 5 | 28 |

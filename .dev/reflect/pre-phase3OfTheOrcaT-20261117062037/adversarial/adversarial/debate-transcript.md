# Adversarial Debate Transcript

## Metadata
- Depth: standard (Round 1 parallel, Round 2 sequential, Round 2.5 invariant probe)
- Advocates: 3 (V1 analyzer/sonnet, V2 qa/haiku, V3 refactorer/opus)
- Convergence threshold: 0.80
- Focus areas: correctness, coverage, deviation-classification
- Diff analysis: ./diff-analysis.md (3 S, 15 C, 4 X, 6 A = 28 diff points)

## Round 1: Advocate Statements

### Advocate V1 (analyzer, sonnet)
- Position: best on how the plan meets the real render and parse code; unique and correct findings F2 (first `n` press), F4 (desk height can collapse the list), F5 (typed join), F7 (invalid dispatchId reason). Conceded it under-rated its F6 (snapshot check).
- Steelman of V2: three blocking findings all grounded; the byte-for-byte link-off comparison (U-005) is the one test that would catch regressions; INF-009 is not untested. Steelman of V3: the only card that checks the plan against the spec corpus and shared test helper; F7 (HELP string, pinned sentence) is the sharpest catch on Task 3.
- Weaknesses admitted: F6 graded MEDIUM but is BLOCKING; missed U-005 to U-009; did not credit that the keys-line state is reachable only if the constant is flipped.
- Shared assumptions: A-001 ACCEPT; A-002 QUALIFY (inspector focus unspecified; filter focus routes text to `_filter_key`); A-003 ACCEPT; A-004 ACCEPT; A-005 QUALIFY (join must use `row.raw.dispatch_id`); A-006 QUALIFY.
- Severity rulings: X-001 MEDIUM (golden tests do not pin the text; test_render.py:753 compares to the constant; state not reachable once the constant is True); X-002 BLOCKING; X-003 NOTE.
- Picks: C-001 B Gap; C-002 M Regression; C-003 B Gap; C-004 M; C-005 M; C-006 M; C-007 NOTE; C-008 NOTE; C-009 M; C-010 NOTE; C-011 M Drift; C-012 M; C-013 M; C-014 NOTE; C-015 NOTE.
- New risk raised (INFERRED, unverified): with the constant True, a payload-less row gets `link="no payload"` and Task 6 appends ` | dispatchId=unknown | link=no payload` to every record line, which could change existing record assertions.

### Advocate V2 (qa, haiku)
- Position: strongest base for the blocking findings: a missing command path, an explicit link-off compatibility violation, and a snapshot check that conflicts with preserved worker identifiers. Distinguishes tests of components from tests that prove the command connects them. Retain FAIL.
- Steelman of V1: separates "linking enabled" from "a selected desk exists" (C-004), sees the renderer has no selection input (C-005), challenges joining against display text (C-006). Steelman of V3: reviews the surrounding contracts and test inputs (AD-18, builder duplication, evicted selection).
- Weaknesses admitted: misses C-006 and C-004/C-005; overstated that every linked fixture is impossible (a linked question with its worker absent from the rows can pass); confidence 0.97 too high; C-003 class better as Gap.
- Shared assumptions: A-001 QUALIFY (collector sites are entry wiring, not the whole path); A-002 REJECT (n/p are text in filter focus; inspector unspecified); A-003 REJECT (omitted plumbing is a clarification finding unless a required behaviour fails); A-004 QUALIFY; A-005 ACCEPT; A-006 QUALIFY.
- Severity rulings: X-001 BLOCKING Regression; X-002 BLOCKING Gap; X-003 MEDIUM.
- Picks: C-001 B Gap; C-002 B Regression; C-003 B Gap; C-004 M; C-005 M; C-006 B Gap (false authoritative link); C-007 NOTE; C-008 M; C-009 M; C-010 NOTE; C-011 B Drift; C-012 M conditional; C-013 M narrowed (Task 1 already targets line 43); C-014 NOTE; C-015 M.

### Advocate V3 (refactorer, opus)
- Position: broadest and best-grounded; four findings no other card raised and confirmed (C-011 AD-18, C-013 stale spec lines, C-012 `make_question_rows`, C-007 location and pinned test). Concedes severity: C-002 and C-003 are BLOCKING.
- Steelman of V1: careful on how state and height actually work (collapse at render.py:382-388; false link through the literal `unknown`). Steelman of V2: grades severity against what the plan itself names; the byte-for-byte link-off comparison is the right guard for C-002.
- Weaknesses admitted: C-002 and C-003 under-graded and its fix for C-003 ("drop that clause") is weaker than V2's; C-005 and C-006 under-graded to NOTE; "INF-009 only a constraint" is wrong because test_commands.py:652-667 pins the `--once` argv.
- Shared assumptions: A-001 ACCEPT; A-002 ACCEPT (n/p free; Esc in list focus has no current meaning); A-003 QUALIFY; A-004 QUALIFY; A-005 QUALIFY; A-006 QUALIFY.
- Severity rulings: X-001 BLOCKING; X-002 BLOCKING; X-003 NOTE.
- Picks: C-001 B Gap; C-002 B Regression; C-003 B Gap; C-004 M; C-005 M; C-006 M; C-007 M Gap; C-008 NOTE; C-009 M; C-010 NOTE; C-011 M Drift; C-012 M; C-013 M; C-014 NOTE Necessary; C-015 NOTE.

## Round 1 tally (per point, majority winner)
| Point | V1 | V2 | V3 | Agreed winner |
|---|---|---|---|---|
| C-001 | B | B | B | BLOCKING (unanimous) |
| C-002 | M | B | B | BLOCKING (2 of 3) |
| C-003 | B | B | B | BLOCKING (unanimous) |
| C-004 | M | M | M | MEDIUM |
| C-005 | M | M | M | MEDIUM |
| C-006 | M | B | M | MEDIUM (2 of 3) |
| C-007 | NOTE | NOTE | M | NOTE (2 of 3) |
| C-008 | NOTE | M | NOTE | NOTE (2 of 3) |
| C-009 | M | M | M | MEDIUM |
| C-010 | NOTE | NOTE | NOTE | NOTE |
| C-011 | M | B | M | MEDIUM (2 of 3) |
| C-012 | M | M | M | MEDIUM |
| C-013 | M | M | M | MEDIUM |
| C-014 | NOTE | NOTE | NOTE | NOTE |
| C-015 | NOTE | M | NOTE | NOTE (2 of 3) |
| X-001 | M | B | B | BLOCKING (2 of 3) |
| X-002 | B | B | B | BLOCKING |
| X-003 | NOTE | M | NOTE | NOTE (2 of 3) |
| A-001 | ACCEPT | QUALIFY | ACCEPT | ACCEPT (2 of 3) |
| A-004 | ACCEPT | QUALIFY | QUALIFY | QUALIFY (2 of 3) |
| A-005 | QUALIFY | ACCEPT | QUALIFY | QUALIFY (2 of 3) |
| A-006 | QUALIFY | QUALIFY | QUALIFY | QUALIFY |
| A-002 | QUALIFY | REJECT | ACCEPT | split |
| A-003 | ACCEPT | REJECT | QUALIFY | split |
| S-001, S-002, S-003, X-004 | not addressed | not addressed | not addressed | unresolved |

Agreed points after Round 1: 22 of 28 = 0.786 (below the 0.80 threshold). Taxonomy coverage: L1 (C-008, C-014, S rows), L2 (C-001, C-002, C-003, C-007, C-010 to C-013) and L3 (C-004, C-005, C-006, C-009) are all debated, so the coverage gate passes.

## Round 2: Rebuttals (sequential: V1, then V2, then V3)

Full rebuttals (each advocate re-Read the cited code before using it):
- V1: ./round-2-v1.md
- V2: ./round-2-v2.md
- V3: ./round-2-v3.md (includes the final candidate list of plan changes)

### Points resolved in Round 2
- S-001, S-002: ruled "do not matter for the merge" (merge per finding; confidence is not carried). V1, V2, V3 ACCEPT.
- S-003: carried forward with V2's correction (unverified-register.md line 33 exists now; its new payload-shape wording and rows T57 to T66 are future). V1, V2, V3 ACCEPT.
- X-004: Necessary deviation, no separate finding (rendering-rules.md:8 leaves C undefined; Constraints line 25 states the narrowing); the line-43 "R3" clause is folded into C-013. V1, V2, V3 ACCEPT.
- A-002: V1's per-focus table (list focus: `n`/`p` select, Esc clears; filter focus: `n`/`p` are typed text, Esc leaves the filter only; inspector focus: `n`/`p` ignored, Esc returns to the list), with V2's correction that test_session.py:359-393 does not prove `n`/`p` leave the selection alone, so Task 4 needs per-focus checks. V1, V2, V3 ACCEPT.
- A-003: qualified rule: an ambiguity is BLOCKING only when an acceptance check pins wrong behaviour or cannot pass, or a named constraint breaks. V1, V2, V3 ACCEPT.

### Final rulings after Round 2 (all three advocates)
| Point | V1 | V2 | V3 | Final |
|---|---|---|---|---|
| C-001 | B | B | B | BLOCKING Gap |
| C-002 | B (conceded) | B | B | BLOCKING Regression |
| C-003 | B (conceded) | B | B | BLOCKING Gap |
| C-006 | M | M (conceded) | M | MEDIUM Gap |
| C-007 | NOTE | NOTE | NOTE | NOTE |
| C-008 | NOTE | NOTE (conceded) | NOTE | NOTE |
| C-011 | M | M (conceded) | M | MEDIUM Drift |
| C-015 | NOTE | NOTE (conceded) | NOTE | NOTE |
| C-004, C-005, C-009, C-012, C-013 | M | M | M | MEDIUM |
| C-010, C-014 | NOTE | NOTE | NOTE | NOTE |

### Verified in Round 2 (static reading; no tests run)
- No existing test in tests/observe asserts exact record question lines or a questions-on screen golden that would change with Task 4's screen text or Task 6's record suffix (V1 and V2 searches agree); the closest assertions are test_commands.py:652-690, test_export.py:278 and test_view.py:943, which read the subject-form `text`.
- test_session.py:359-393 does not prove `n`/`p` leave the selection unchanged; Task 4 needs its own per-focus assertions.

## Convergence Assessment
- Points resolved: 28 of 28 (every point has a final ruling that all three advocates now share; the one residual difference, V2's "BLOCKING" on C-006 and C-011 in Round 1, was conceded in Round 2)
- Alignment: 100% (1.00)
- Threshold: 80%
- Taxonomy coverage: L1, L2, L3 all covered
- Status: CONVERGED pending the Round 2.5 invariant probe (see ./invariant-probe.md)
- Unresolved points: none

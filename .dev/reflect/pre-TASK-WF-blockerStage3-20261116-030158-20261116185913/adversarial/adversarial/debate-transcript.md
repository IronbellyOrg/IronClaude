# Adversarial Debate Transcript

## Metadata
- Depth: standard
- Rounds completed: 2 (Round 1 parallel, Round 2 sequential) plus Round 2.5 invariant probe; no Round 3 (depth standard)
- Convergence achieved: 95.0 percent (19 of 20 diff points; C-007 counted unresolved because the fault-finder's evidence overturned the advocates' shared non-blocking grade)
- Convergence status: BLOCKED_BY_INVARIANTS (one HIGH UNADDRESSED invariant, INV-001; see invariant-probe.md). Not run again in a Round 3 (depth standard); carried into the merged card as a finding instead.
- Convergence threshold: 80 percent
- Focus areas: correctness, coverage, deviation-classification
- Advocate count: 2 (Variant 1 sonnet:analyzer for the haiku-analyzer card; Variant 2 sonnet:qa for the opus-qa card). The advocates are a different class from neither card author on purpose; the scoring judges (opus) are a different class from both advocates.
- Taxonomy coverage: L1 S-001, C-009, C-010; L2 C-001, C-004, C-005, C-006, C-008, C-011, C-012, C-013, X-003, A-001, A-003; L3 C-002, C-003, C-007, X-001, X-002, A-002 (all levels covered; no forced round)

Round texts (persisted verbatim by the orchestrator): `debate/round-1.md`, `debate/round-2-advocate-1.md`, `debate/round-2-advocate-2.md`. Invariant probe: `invariant-probe.md`.

Omission check on shared assumptions (A-001, A-002, A-003): both advocates answered all three in Round 1 (QUALIFY, QUALIFY, ACCEPT for the Variant 1 advocate; QUALIFY, QUALIFY, QUALIFY for the Variant 2 advocate) and A-003 again in Round 2 (ACCEPT as fixed in text only, by both). No [OMISSION] flag.

## Scoring Matrix

Winner = the variant whose position on the point is better supported by the live files after Round 2; "grade" is the consequence grade (blocking or non-blocking) the orchestrator settled on after the invariant probe.

| Diff Point | Winner | Confidence | Grade | Evidence Summary |
|------------|--------|------------|-------|------------------|
| S-001 | neither | 80% | n/a | format only; V1's table says MEDIUM while its text says blocking (variant-1-original.md:22, :27) |
| C-001 | Variant 2 | 75% | blocking (through C-003 and C-007) | earlier F2 and F3 are fixed in text only; PLAN:82, PLAN:168 |
| C-002 | Variant 1 | 70% | blocking (R1b); R3 and the ADVISORY/NOT-MEASURABLE overlap are medium and join the same finding | PLAN:91 "one event, never advisory"; PLAN:96 PASS needs "at or above its minimum n"; S0:106 undersized is the expected outcome; both advocates agree no word fits R1b |
| C-003 | Variant 2 | 72% | blocking | PLAN:82 "(2 of 3 with three valid reviewers, 2 of 2 with two)": panel-size artifact of about 16 points at p=0.9 against a 5-point margin; can falsely trip RT1 via R1b (PLAN:257); both advocates agree |
| C-004 | Variant 1 (on fact) | 72% | non-blocking | PLAN:132 names `verify`; verify_cmd.py:76 registers `verify-citations`; a substring check passes |
| C-005 | Variant 2 | 62% | non-blocking (medium) | PLAN:168, PLAN:185, PLAN:147 count phrases the inserted digest already holds (SPEC:199, SPEC:201, SPEC:213); both advocates agree the consequence is lost prose, not a wrong grade |
| C-006 | Variant 2 (on fact) | 62% | non-blocking (medium) | rf-qa-qualitative.md:593, :611, :616 assign labels; :918 is a relay string; no test pins them (tests/audit/test_severity_floor_unweakened.py pins the block hash, Rule 6 and tokens only); both agents already say "grade by the definition above, not by the label" at line 111 |
| C-007 | Variant 2 | 70% | blocking (raised by the invariant probe, INV-001) | SKILL.md:145 and refs/qa.md:245 run a fix pass on a failed Task 6 check; ACs 2 to 7 demand the edit; refs/retry.md:109 and :158 leave the attempt in the tree; Tasks 7 to 10 read only the registry row |
| C-008 | Variant 2 | 65% | non-blocking | S4 reads the bold words of the Rule 6 line with an awk anchored on `6. **` |
| C-009 | neither | 80% | not a plan defect | the matrix is the orchestrator's artifact; V2 itself found each row covered |
| C-010 | Variant 2 | 85% | non-blocking (wording) | PLAN:142 "the two listed below"; PLAN:152 lists three |
| C-011 | Variant 2 | 60% | non-blocking, no current miss | SPEC:920 says `src/` or `plugins/`; every current hit lies in the scanned folders |
| C-012 | Variant 2 | 60% | non-blocking | rf-qa.md:389 and :476 are named only as a category (PLAN:158); relay and re-verify scope; L1 text omits `reasked` and "listed first" (SPEC:270), the digest carries the rule |
| C-013 | both | 70% | not a defect | the git diff lines omit HEAD; stage 2's paragraphs are checked free of the scanned words (S2:122) |
| X-001 | Variant 1 | 65% | R1b blocking, R3 medium | same family as C-002; V2 did not see R1b |
| X-002 | Variant 2 | 72% | blocking | same as C-003 |
| X-003 | Variant 2 | 62% | non-blocking (medium) | same as C-006 |
| A-001 | n/a | 70% | QUALIFY by both | order is safe, contents of stage 0 to 2 outputs are promises; the fix pass is a route (INV-001) |
| A-002 | n/a | 65% | QUALIFY by both | a ruling is acceptable for a true non-PASS word, not for an undefined word (R1b) or a manufactured one (C-003) |
| A-003 | n/a | 65% | ACCEPT as fixed in text only | earlier F4 to F16 addressed in text |

## Convergence Assessment

- Points resolved: 19 of 20
- Alignment: 95.0 percent
- Threshold: 80 percent
- Status: BLOCKED_BY_INVARIANTS (agreement is above the threshold and all taxonomy levels are covered, but INV-001 is a HIGH UNADDRESSED invariant)
- Unresolved points: C-007 (advocates agree non-blocking; the fault-finder's evidence and the orchestrator's check of SKILL.md:145, refs/qa.md:245, refs/retry.md:109 and :158 grade it blocking)
- MEDIUM unaddressed invariants (do not block): INV-002, INV-003, INV-004

# Variant 1 (opus:architect): seal the rule sections and add a stopping rule

## Verdict
REMEDIATE, structural. Keep the `need()` checks. Add a sha256 seal over every rule-bearing section so any edit to a sealed section fails a test. Unsealed sections form a finite, listed register.

## Concrete changes (existing test module only, no new files)
1. `SEALS`: list of (file_key, start, end, sha256) cut with existing `section()` and normalized with right-strip per line. Hashes live in the test module (not a fixture) so the AT-20 fixture scan never sees them.
2. Sealed (~30): gate from `## Dispositions` through `## Invariant check` (up to the jq fence); skill Output Contract, Wave 0, 2, 3 (to `### Wave 4`), 4; rubric `## Admission precedes grading`, `## Decision-mode summary`; prompts Output contract / Claim block / Quality bar; agent Responsibilities / Output Format; handoff `## When the offer fires`, `## Phase A`; command `## Boundaries`.
3. `UNSEALED`: headings with one-line reasons; a test asserts every heading in the 7 files is in exactly one of SEALS / UNSEALED.
4. `test_sealed_sections_unchanged`: failure prints file, heading, new hash.
5. `GAP_MUTATIONS`: the 10 gaps, one mutation each, run against the seal check on a tmp copy.
Size: ~60 lines + ~30 hash lines.

## Gap table (architect view)
| Gap | Backstop | Severity if slips | Action |
|---|---|---|---|
| G1 | none (oracle compares table only) | High | seal |
| G2 | J5 reason format only | High | seal |
| G3 | step 6b: missing jq_exit => failed | Low | seal |
| G4 | none | Medium | seal |
| G5 | none (J13 PR mode only) | Medium | seal |
| G6 | strict-dominance asserted; J6-J8 structure | Medium | seal |
| G7 | gate copy asserted; J14 at runtime | Low | seal |
| G8 | partly AT-16 order; J4/J5 | Medium-High | seal |
| G9 | partly J13 | Medium | seal |
| G10 | J6 does not catch | Medium | seal |

## Definition of done
1. Each AT has a need() check. 2. Every heading is sealed or listed UNSEALED with reason (test-enforced). 3. Every sealed section shown by mutation test to fail when changed. 4. Stopping rule: "mutation survives inside sealed section" cannot occur; in an UNSEALED section the reviewer must argue it holds a rule, fix = move to SEALS, no new need() checks; "is the rule text correct" belongs to the final plan review and live eval 11.3.

## Cost
~1-1.5 h. Future legitimate edits cost one hash paste (deliberate friction). Tasks 12/13 do not edit src/ (sync-dev writes .claude/ only).

## Residual risk
Edit plus re-seal in same commit passes everything. Seal freezes an already-wrong sentence.

## Top 3 risks
1. Re-seal waved through. 2. Sealing before the 10 sentences are checked against the spec freezes a mistake. 3. Reviewers say Task 11 asked for presence checks not a seal; needs an operator ruling.

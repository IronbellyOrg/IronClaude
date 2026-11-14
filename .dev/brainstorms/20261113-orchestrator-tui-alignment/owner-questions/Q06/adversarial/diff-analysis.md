# Diff Analysis: owner-answer proposals for Q6 (scope and timing of the observer questions-read switch-on)

## Metadata
- Generated: 2026-11-14
- Variants compared: 3 (variant-1 = proposal-A, variant-2 = proposal-B, variant-3 = proposal-C; Mode A copies)
- Total differences found: 13
- Categories: structural (1), content (5), contradictions (2), unique (3), shared assumptions (2 promoted, 2 stated)
- Prerequisites validated: output path is under `.dev/`, not a forbidden `.claude/` prefix; all three inputs exist.

## Structural Differences

| # | Area | Variant 1 (A) | Variant 2 (B) | Variant 3 (C) | Severity |
|---|---|---|---|---|---|
| S-001 | Section set | Same five sections (Answer, What happens next, Unlocks, Costs or risks, Unresolved) | Same | Same | Low |

## Content Differences

| # | Topic | Variant 1 (A) | Variant 2 (B) | Variant 3 (C) | Severity |
|---|---|---|---|---|---|
| C-001 | Does the seeded consumption test (OB-03) run in this program? | No; parked until release 3 is opened | Yes, in W1 | Yes, in W1 | High |
| C-002 | When is the scope sentence given? | Not now; asked again when release 3 opens | Now: "any Run my terminal holds" | After the OB-03 and OB-04 records, in W2 | High |
| C-003 | When is the flip pull request (OB-06) built? | Not in this program | W1, in parallel with the tests, merged only after all records | W2, after the scope sentence | Medium |
| C-004 | How the code enforces scope | Not applicable | A test refuses a Run the terminal does not hold; how "held" is detected without `run-use` is UNVERIFIED | A test refuses an out-of-scope Run, whichever sentence the owner writes | Medium |
| C-005 | Dependence on live Orca, Q24 and Q30 | Removed | Kept | Kept | Medium |

## Contradictions

| # | Point of Conflict | Variant 1 (A) | Variant 2 (B) | Variant 3 (C) | Impact |
|---|---|---|---|---|---|
| X-001 | Can the owner usefully choose the scope before the evidence exists? | No choice needed now ("the scope question is asked again then") | Yes: "any Run my terminal holds" matches "the only access path Orca gives" (Q-1 failed) | No: "the scope choice is made on evidence ... without having committed in advance" | High |
| X-002 | Is building the flip before the test acceptable work? | Not built at all | Yes, "may be wasted work if the test fails" accepted as a cost | No, built only in W2 | Medium |

## Unique Contributions

| # | Variant | Contribution | Value Assessment |
|---|---|---|---|
| U-001 | A | Concrete park trigger ("release 3 is opened") and the observation that parking weakens the reason to commit the sibling-only owner records (Q7), raising evidence-loss risk | Medium |
| U-002 | B | Observation that the only Run the pass names (`run_93bfa00cae2b`, an old "Claim issue 375" Run) has no practical use, so "this Run only" yields a flip that works for nobody | High |
| U-003 | C | Explicit stop rule: any seeded message missing stops OB-06 and records "consumes" (`merged-requirements.md:1000`), and a narrow-scope fallback if OB-04 shows the panel unusable (`:1001`) | Medium |

## Shared Assumptions

| # | Agreement Source | Assumption | Classification | Promoted |
|---|---|---|---|---|
| A-001 | All three refuse a flip before the seeded test | No flip before the seeded test | STATED (all) | No |
| A-002 | B and C run the live tests | The live tests need the Orca app reachable, Q24 and Q30 answered | STATED (C, A) | No |
| A-003 | All three treat the panel's value as the driver of timing | There is a real near-term user of the questions panel (B assumes yes, A assumes no; no variant cites evidence of demand) | UNSTATED | Yes |
| A-004 | B and C treat a seeded pass plus one live attempt plus a build pin as enough to flip | A pass on today's Orca build stays meaningful until the build changes, and the build check (OB-05) is what detects that change | UNSTATED | Yes |

### Promoted shared assumptions

| A-NNN | Assumption | Source Agreement | Impact | Status |
|---|---|---|---|---|
| A-003 | A near-term user of the questions panel exists | Timing arguments of all three | Decides whether the cost of the live tests is worth paying now | Open (owner's knowledge) |
| A-004 | Evidence on one Orca build carries until the build changes, and OB-05 catches the change | B and C flip criteria | If false, any flip is on stale evidence (ADJ A-009, 67 percent unresolved build divergence) | Open |

## Summary
- Total structural differences: 1
- Total content differences: 5
- Total contradictions: 2
- Total unique contributions: 3
- Total shared assumptions surfaced: 4 (UNSTATED: 2, STATED: 2, CONTRADICTED: 0)
- Highest-severity items: C-001, C-002, X-001
- Taxonomy tags: L3 (guard and state): C-001, C-004, X-001, A-004; L2 (structure and dependency): C-002, C-003, C-005, X-002, A-003; L1 (surface): S-001.

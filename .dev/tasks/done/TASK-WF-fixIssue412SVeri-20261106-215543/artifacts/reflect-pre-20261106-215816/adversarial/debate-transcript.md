# Debate Transcript

## Metadata

- Mode: A (compare). Inputs are 3 reviewer cards from reflect UC-1, copied as `variant-{1,2,3}-original.md`.
- Depth: standard. Round 1 (parallel), Round 2 (sequential, in input order) and Round 2.5 (invariant probe). No Round 3.
- Convergence threshold: 0.80.
- Focus: correctness, coverage, deviation-classification.
- Advocates (3, one per variant):
  - Variant 1: sonnet/analyzer, calibrated 0.72
  - Variant 2: haiku/qa, calibrated 0.66
  - Variant 3: opus/refactorer, calibrated 0.68
- Scored points: 11. These are S-001, S-002, C-001..C-005, X-001, X-002 and the promoted UNSTATED assumptions A-001 and A-002. The STATED assumptions A-003 and A-004 are answered but not scored.
- Round files: `rounds/round-1-variant-{1,2,3}.md`, `rounds/round-2-variant-{1,2,3}.md`.
- Orchestrator neutrality: the orchestrator tallied votes and checked the citations the advocates relied on. It did not advocate.
  - It re-read plan lines 19-53 and `tests/core/test_codegraph_guide.py:137-174`.
  - It re-read `install_user_setup.py:230-263` and `:434-444` in Step 1.
- Nothing was executed: no tests, installs or Orca commands, by any advocate or by the orchestrator.

## Round 1 Summary (parallel)

Each advocate steelmanned the other two before critiquing them, and answered every shared assumption.

- **Variant 1** claimed that it alone detects the gap between plan line 35 "distinguish" and `source.md:1` "never New Terminal" (X-001/C-003). It also claimed it alone anchors every finding with a `plan_ref` (S-001). It conceded three things:
  - its wrong code range at `original_source_ref` (113-119; the real helper is `install_user_setup.py:230-263`);
  - that "not precisely defined" overstates the gap, since plan lines 24, 45 and 51 define the requirement;
  - that R1-1 is of low value (plan line 47).
- **Variant 2** argued that zero minor findings is defensible and that its preservation checklist tracks plan line 45 clause by clause (U-003). It conceded three things:
  - its 21/21 is reviewer judgment, set against a lexical 13/21 = 0.6190;
  - its evidence comes from the brief only;
  - it has no exit-0 skip fixture.
- **Variant 3** claimed the most accurate anchoring: `install_user_setup.py:230-263`, plan lines 45-51 and the verified reader `tests/core/test_codegraph_guide.py:137-174`. It also claimed the sharpest verifier, R3-2: exit 0, three files present, stdout naming a skipped guide, and "no refresh-success claim". It conceded three things:
  - it is silent on C-003/X-001;
  - R3-1 leads are unverified;
  - its brief-local "plan lines 81-82" is a pathology.

Shared assumptions, Round 1:

| ID | V1 | V2 | V3 |
|---|---|---|---|
| A-001 (an Orca skip can exit 0) | ACCEPT | QUALIFY | QUALIFY |
| A-002 (the presence check passes trivially when the files already exist) | ACCEPT | ACCEPT | ACCEPT |
| A-003 (plan-level only; no runtime causation) | ACCEPT | ACCEPT | ACCEPT |
| A-004 (force argument is backward-compatible) | QUALIFY | QUALIFY | QUALIFY |

For A-001, the QUALIFY answers note that the evidence is documented help text (`orca-discovery.md:21`, `:25`) and was not observed. For A-004, only the keyword caller at `install_user_setup.py:441` is shown, so the new parameter must follow `deadline` with a False default.

## Round 2 Summary (sequential rebuttals)

- **Variant 1** (`round-2-variant-1.md`):
  - It conceded C-002 to Variant 3, because both cards read plan line 47 the same way.
  - It rebutted part of Variant 3's A-001 reasoning. Variant 3 had said Variant 1 "assumes [exit 0] without saying so", but `variant-1-original.md:16` opens with "Mock exit-zero edited-copy skip with files present". So A-001 is a tie.
  - It moved A-001 from ACCEPT to QUALIFY.
- **Variant 2** (`round-2-variant-2.md`):
  - It conceded all five criticisms.
  - It moved C-005 from "Variant 2, qualified" to a tie between Variants 1 and 3, and A-001 to a tie between Variants 1 and 3.
  - On whether zero minors is enough: PASS with no blocking findings survives, but "zero minors is complete" does not, because X-001 and X-002 are real verification gaps.
- **Variant 3** (`round-2-variant-3.md`):
  - It conceded the criticisms below.
    - (a) It is silent on C-003/X-001.
    - (c) "Plan lines 81-82" is a pathology. It appears only in the card's limitations. R3-1 has no `plan_ref`.
    - (d) It has no empty-output counter-case.
    - (e) Its claim that Variant 1 "assumes [exit 0] without saying so" was a misreading of Variant 1.
  - It defended part of (b). R3-1 keeps only the verified reader `tests/core/test_codegraph_guide.py`.
    - That file reads core CLAUDE.md at line 137.
    - Its assertions depend on placement: lines 149, 155, 162-166 and 173.
    - Plan line 52 does not list it.
    - Its three leads are dropped.

## Scoring Matrix

A point is agreed when all three advocates vote for the same winner, or when two of three do. After Round 2, all three advocates hold identical final positions on every point.

| Point | Winner | Final vote | Round 1 vote | Confidence | Basis |
|---|---|---|---|---|---|
| S-001 | Variant 1 | 3/3 | 3/3 | 92% | Unanimous. Every R1 finding has a `plan_ref` and a verifier. |
| S-002 | Variant 3 | 3/3 | 3/3 | 95% | Unanimous. V1 conceded its 113-119 pathology. |
| C-001 | Variant 3, with V1's empty-output case merged | 3/3 | 3/3 | 95% | Unanimous. V3 conceded (d). |
| C-002 | Variant 3 | 3/3 | 2/3 | 95% | V1 conceded in Round 2 (+10). |
| C-003 | Variant 1 | 3/3 | 3/3 | 95% | Unanimous. V3 conceded (a). |
| C-004 | Variant 3 (low value; leads dropped) | 3/3 | 3/3 | 90% | Unanimous. Scope is narrowed to one verified reader. |
| C-005 | Variants 1 and 3, tied | 3/3 | 2/3 | 95% | V2 conceded in Round 2 (+10). |
| X-001 | Variant 1 | 3/3 | 3/3 | 95% | Unanimous. V2 and V3 conceded. Resolved through plan line 30 Inputs. |
| X-002 | Variant 3 | 3/3 | 3/3 | 95% | Unanimous. V1 conceded its overstatement. |
| A-001 | Variants 1 and 3, tied | 3/3 | 2/3 (V3) | 95% | V3 conceded (e). All three now QUALIFY. |
| A-002 | Variant 3 | 3/3 | 3/3 | 92% | Unanimous. |

No confidence value is 100%. The +10% concession bonus is applied only where an explicit concession moved a vote.

Point wins, counting a tie as 0.5 to each side:
- Variant 3: 7.0 (S-002, C-001, C-002, C-004, X-002, A-002, plus 0.5 C-005 and 0.5 A-001)
- Variant 1: 4.0 (S-001, C-003, X-001, plus 0.5 C-005 and 0.5 A-001)
- Variant 2: 0.0

Variant 2's unique contribution, U-003, is the preservation checklist and the separation of mocked checks from live ones (plan line 52). No scored point measures it. All three advocates acknowledge it as medium value.

## Convergence Assessment

- Agreed points: 11 / 11. Convergence score: **1.00** against a threshold of 0.80.
- Taxonomy: L1, L2 and L3 points are all agreed. C-001, the exit-0 safe skip, is the L3 point, and it is agreed unanimously. Status is not BLOCKED_BY_TAXONOMY.
- Verdict consensus: all three advocates agree on **PASS with zero blocking findings**. The minor findings are verification refinements, not plan defects.
- Remaining work: none on the scored points. Round 2.5 (the invariant probe) runs next. Any HIGH UNADDRESSED item would change the status to BLOCKED_BY_INVARIANTS.
- Status after Round 2: CONVERGED, pending Round 2.5.

## Round 2.5 Result (invariant probe)

- Items: 22. ADDRESSED: 13. UNADDRESSED: 9 (HIGH 0, MEDIUM 3, LOW 6). Details are in `invariant-probe.md`.
- MEDIUM items:
  - INV-005: stderr-only skip fixture
  - INV-006: empty-output expectation
  - INV-009: forced-path deadline spend
- No HIGH item is UNADDRESSED. Final status: **CONVERGED**, convergence 1.00.

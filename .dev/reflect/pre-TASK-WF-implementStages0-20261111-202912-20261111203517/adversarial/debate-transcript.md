# Adversarial Debate Transcript

## Metadata
- Depth: standard
- Advocates: 3 (V1 sonnet, V2 haiku-pinned, V3 opus)
- Focus areas: correctness, coverage, deviation-classification
- Note: Round 1 texts are condensed by the orchestrator; verdict lines are verbatim in meaning, evidence citations kept.

## Round 1: Advocate Statements

### Variant 1 advocate (sonnet) - verified C-013, C-015, C-018, C-019 (all V2 findings)
- C-013 UPHELD-LOWER (medium): plan:26 "Never use Opus, Fable or Tier 0 in any new template" vs plan:145-146 `@reflect-pre` resolves to opus; spec:235 permits Opus as parity third reviewer/backfill; template JSON names tier ids not Opus; plan:147 acceptance bans only Fable/tier0/gateway. Wording contradiction, not blocking.
- C-015 UPHELD-LOWER (medium): spec:408 lists "the lint test design" under Stage 0 ships; plan Task 7 checklist (plan:102) omits it; Task 15 builds the checker in Phase 4 (plan:186-194).
- C-018 UPHELD-LOWER (medium): spec:185 judge must not be Fable/tier0; spec:240 applies to calibrator pick and judge; Task 9 validates resolutions only (plan:121); Task 19 records judge fields with no assertion/REPORT note (plan:233); judge field UNVERIFIED (spec:184-185) so the assertion may not be writable yet.
- C-019 UPHELD-LOWER (medium): spec:255 compare self-report with pin, degrade diversity on mismatch, no independence claim in REPORT (258, 263); Task 19 only adds the field; REPORT wording arguably out of scope in shadow.
- V1 verified own R1-F1 (panel.py:520 `tiers_sha256 = sha256_json(tiers)`), R1-F3 (panel.py:489-496), R1-F8 (plan:102 "five" vs four; spec:408 four).
- Concessions: V1 brief truncated at 343/426 lines, never read Tasks 12-20; missed C-013, C-015-C-019; under-grades C-002.
- A-002 QUALIFY; A-004 ACCEPT.

### Variant 2 advocate (haiku) - verified C-022, C-025, C-021, C-026 (all V3 findings)
- C-022 REFUTED: plan:233 adds the brief instruction within steps explicitly "for `--t2-engine shadow`"; reviewer-spec.md:35-39 creates a placement ambiguity but does not show legacy briefs must change.
- C-025 UPHELD (medium): plan:222 states D3 by pinned tier and class count without an engine guard; spec:122 "whose panel yields"; spec:385 legacy debate authoritative in shadow.
- C-021 UPHELD (medium): plan:177-181 treats blocked write as allowlist-survival evidence; reflect-reviewer.md:5-8, 38-40 gives permissionMode plan and prose prohibition, so refusal cannot identify which restriction operated.
- C-026 REFUTED: plan:212 temp-file publication and SKILL.md:136 per-step audit rows coexist if publish preserves accumulated rows; spec:363 requires the publish design.
- Claims: Task 10 ordering defect overstated ("once Task 11 lands" allows deferred verification); V3 turns possible mistakes into contradictions.
- Concessions: misses the probe's inability to distinguish mechanical denial from refusal; its Task 10 finding should be a verification-scheduling clarification.
- A-002 QUALIFY; A-004 QUALIFY (no historical hash equivalence established).

### Variant 3 advocate (opus) - verified C-003, C-004, C-005, C-014 (all V1 findings except C-014 V2)
- C-003 UPHELD (blocking): panel.py:520 writes `tiers_sha256`; `sha256_json` hashes the whole tier object (panel.py:421-424); adding `classes` (plan:121) changes it; no existing test pins the value (test_review_panel.py:308 checks length only); the break is in Task 8's own new golden test (plan:113); Task 9 forbids editing existing tests (plan:126); spec:225 vs spec:227 same conflict. Plan must say: golden uses a frozen copy of the tier file as a fixture, or Task 9 explicitly re-baselines `tiers_sha256`.
- C-004 UPHELD (medium): panel.py:489-496 re-raises plain NoModelAvailable, subclass lost; panel_cmd.py:64-65 prints `str(exc)` only; Task 10 "naming ExclusionExhausted" (plan:135) cannot pass unless plan says re-raise the subclass and print `type(exc).__name__`.
- C-005 UPHELD-LOWER (minor): no reflect profile validator exists; `validate_panel` takes tiers optionally (panel.py:64); `validate` command calls it without a tier file (panel_cmd.py:82; panel.py:331, 341); only `resolve` passes tiers (panel_cmd.py:58); `launch` includes `"claude-fable-5-1": "fable"` (review-tiers.default.json:29), Fable in `available` (:27); Task 9 class list omits Fable (plan:121); `--sequence` never reaches validation (panel_cmd.py:62); plan:121 does say where the validator applies.
- C-014 UPHELD-LOWER (medium): spec:409 Stage 1 entry = Stage 0 exit incl. 50-pair labelled check (spec:408), but both columns describe what ships, Stage 1 is dormant with rollback "revert the commits"; plan:27 defers labels but is not labelled a "Plan decision" (unlike 23-24); Task 8 depends only on Task 7 (plan:108). A deviation only if Stage 1 merges/ships before the owner's scored sheet passes. Plan must state: Stage 1+ code may be built but not merged until `reflect_cluster_pairs.py score` passes on owner labels (no threshold in spec), plus an owner checkpoint.
- Concessions: missed C-003, C-004, C-013, C-014, C-015; F11 (0.60) and F12 (0.55) low confidence; did not verify own F1-F14.
- A-002 QUALIFY (the plan itself expects out-of-order acceptance, "once Task 11 lands", so it is a defect, not an unstated premise); A-004 ACCEPT.

## Round 2: Rebuttals (sequential V1, V2, V3)
- V1: conceded C-005 minor (plan:121 names the validator scope); conceded truncated brief; raised C-002 to medium; new evidence R1-F5 UPHELD-LOWER (medium): Task 2 matches only one card shape; across card files severity words other than blocking/minor are roughly half (medium 48, low 55, should-fix 36, P1-P3 29 vs minor 229, blocking 37), `deviation_class` appears ~160 times against `category:` about a dozen, only 2 `plan:`/`spec:` keys exist, markdown cards exist (pre-TASK-WF-rollOutTheIssueW-*/reviewer-cards/reviewer-1-card.yaml:8-39; pre-TASK-WF-makeTheAliasOnly-*/reviewer-cards/reviewer-1-card.md:11-22). Final: C-002 medium, C-005 minor, C-006 medium.
- V2: kept blocking C-013, C-015, C-018, C-019; accepted C-014 medium; counted Task 7 "five" vs four listed (plan:102), spec:408 four exit items, lint design is under "What ships"; C-016, C-017 blocking; C-009 minor.
- V3: conceded C-026 REFUTED (spec:363 requires the temp-file publish); C-022 downgraded to minor (plan:233 steps are shadow-labelled, but the edit to refs/reviewer-spec.md has no guard); C-023 confirmed (SKILL.md:666 "at least"; Task 15 "equals"; lint lacks the loud-fallback branch); C-021, C-025 medium.

## Round 2.5: Invariant probe (fault-finder, sonnet)
8 findings against consensus-fixes.md: INV-001 HIGH (no task names the manifest `advance` calls), INV-007 HIGH (`panel_parity` true by construction), INV-002..006, INV-008 MEDIUM. Full text kept in consensus-fixes.md ("Added after the Round 2.5 invariant probe"). All 8 were folded into the plan edits by the orchestrator, so the gate "no HIGH UNADDRESSED" holds for the refactor plan (not for the unedited plan, which still carries them).

## Scoring Matrix (orchestrator adjudication)
| Point | Winner | Confidence | Evidence |
|---|---|---|---|
| C-001 | V1, V2, V3 agree: blocking | 95% | plan:135, 140 |
| C-003 | V1: blocking | 90% | panel.py:520, 421-424; plan:113, 121, 126 |
| C-013 | contradiction: blocking (V2, V3) over V1 medium | 70% | plan:26 vs plan:145-146; spec:235 |
| C-015 | missing deliverable: blocking (V2) over V1 medium | 70% | spec:408; plan:97-102, 186-194 |
| C-016, C-017 | V2, V3 agree: blocking | 90% | plan:212, 222-233, 247 |
| C-018, C-019 | medium (V1 over V2): shadow keeps legacy authoritative, judge field UNVERIFIED | 65% | spec:184-185, 255-263; plan:233 |
| C-014 | medium (V3, V1, V2 final) | 85% | spec:408-409; plan:27 |
| C-026 | REFUTED | 90% | spec:363 |
| C-022 | minor | 80% | plan:233; reviewer-spec.md:35-39 |
| others | per consensus-fixes.md | 60-85% | see file |

## Convergence Assessment
- Total diff points: 33 (1 structural, 28 content, 2 contradictions, 2 promoted assumptions)
- Points where advocates agree on the final grade: 29; severity left to orchestrator adjudication: 4 (C-013, C-015, C-018, C-019)
- Alignment: 29/33 = 0.88 (threshold 0.80)
- Taxonomy coverage: L1 surface (C-027, C-028), L2 structural (most), L3 state mechanics (C-003, C-016, C-020, INV-001, INV-007): all covered
- Invariant gate: INV-001 and INV-007 were HIGH UNADDRESSED at probe time; both addressed in the refactor plan, so the gate passes for the refactor plan only
- Status: CONVERGED (0.88)

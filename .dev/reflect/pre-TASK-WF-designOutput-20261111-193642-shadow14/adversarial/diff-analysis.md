# Diff Analysis — Mode A, 3 reviewer cards

Panel: reflect Tier-2, pre-TASK-WF-designOutput-20261111-193642-shadow14 (shadow run 14).
Focus: correctness, coverage, deviation-classification.
Cluster context: cluster_agreement = 1.0 (13/13 findings calibrated across cards).

## Structural differences

| Property | Card 1 (analyzer/sonnet) | Card 2 (qa/haiku) | Card 3 (refactorer/opus) |
|---|---|---|---|
| Findings | 5 | 4 | 4 |
| Calibrated card score | 0.63 | 0.69 | 0.59 |
| Categories used | unpassable-check (1), other (2), missing-requirement (1), contradiction (1) | missing-requirement (1), other (2), unpassable-check (1) | contradiction (1), missing-requirement (1), other (2) |
| Citation style | Every finding carries quoted plan+spec citations | 1 of 4 findings carries quotes (F1 spec only); rest bare line refs | Quotes on F1, F2; bare refs elsewhere |
| Vantage stance | Explicit "advisory only, not an executor defect" labels (F2, F4) | No vantage commentary | Treats shipped design.md divergences as first-class findings (F1, F2, F4) |
| Severe findings | 0 of 5 | 0 of 4 | 0 of 4 |

All 13 findings are MINOR / non-blocking. No card used a severity above MINOR and no card marked anything blocking.

## Content differences

### Clustered diff points (taxonomy tag: L1 literal / L2 structural / L3 deep)

- **D1 [L3] Task-2 AC3 escape hatch** — R1-F1 (unpassable-check, conf .80, plan:46 and spec:62 both quoted), R2-F3 (unpassable-check, .70, bare refs, adds the green-run detail "1167 passed, rc=0"), R3-F3 (category `other`, .55, bundled together with the AC1 baseline issue). All three treat it as latent and MINOR. Disagreement is classification and packaging, not substance.
- **D2 [L2] design.md:65 conditional codegraph_impact vs spec 3.2-4 unconditional** — R1-F4 (.65, category contradiction but claim text says "mild unplanned drift in the shipped file, not a plan defect"), R3-F1 (.80, category contradiction, "shipped text narrower than the plan; plan was not amended"). R2 silent on this point entirely.
- **D3 [L2] Archived done/ package lacks a before-state baseline; AC1 git-diff not re-runnable** — R1-F2 (.70, standalone finding, "advisory only, not an executor defect"), half of R3-F3 (.55, bundled with the AC3 hatch). R2 silent.
- **D4 [L3] Spec item 7, SUPERCLAUDE_CODEGRAPH_PRIMITIVES=off yields graph:disabled** — two *different claim types* on the same requirement: R2-F4 (.70, an acceptance-criteria gap: no AC checks item 7, the Grounding line, or the leads rules) vs R3-F2 (.70, a shipped-artifact absence: design.md never mentions the variable, though the token graph:disabled is still listed). These are complementary, not contradictory.
- **D5 [L2] Spec item 5 tail "no re-check after writing the design document" omitted from Task 1, no matrix row** — R2-F1 (.80). Unique to Card 2.
- **D6 [L3] Coverage matrix grounds INF-007 at tasklist:31-33 (Task 1 AC lines) though the work is Task 2 (line 41); no mechanical AC** — R2-F2 (.65). Unique to Card 2.
- **D7 [L3] Spec 3.2-6 degraded-list conditional copied into the plan with no verification step; design.md silently chose "no new field"; Grounding-line placement for --format code/diagram unspecified** — R1-F3 (.65). Unique to Card 1.
- **D8 [L2] Task-2 AC4 git-status check cannot be attributed to this plan in a shared checkout (spec risk 7)** — R1-F5 (.60). Unique to Card 1.
- **D9 [L2] Shipped fallback adds graph:empty / graph:truncated / graph:unresolved beyond the plan's seven tokens, plus "worker contract gets no new field"** — R3-F4 (.55). Partially overlaps R1-F3's "no new field" note.

## Contradiction detection (cards disagreeing on severity/category of the same underlying defect)

1. **D1 classification split**: R1 and R2 say `unpassable-check`; R3 says `other`. R3 also bundles two distinct defects (AC3 hatch + AC1 baseline) into one finding at the panel's lowest confidence (.55), which hides the correctly-classified signal the other two cards carry.
2. **D2 category-vs-claim mismatch inside R1-F4 itself**: filed as `contradiction` while its own claim text says "drift in the shipped file, not a plan defect" — a deviation class, not a finding category. R3-F1 files the same defect as `contradiction` with the additional fact that the plan was never amended, at higher confidence.
3. **D4 claim-type divergence**: R2 asserts an AC-coverage gap; R3 asserts a shipped absence. Same requirement, different layers (plan-side vs artifact-side). Neither subsumes the other.
4. **D3 severity stance**: R1 explicitly downgrades to "advisory"; R3 leaves the same fact at .55 inside a bundle. No card calls the missing baseline a plan defect outright.

## Unique contributions per card

- **Card 1**: D7 (degraded-list conditional unverified + Grounding-line placement for --format code/diagram — the only finding addressing format-specific output placement), D8 (AC4 shared-checkout attribution). Best citation hygiene: quotes on all 5 findings.
- **Card 2**: D5 (item-5 "no re-check" tail omitted, no matrix row — cleanest pure coverage finding), D6 (matrix grounds INF-007 at the wrong task's AC lines). Only card to examine the coverage matrix's line-level grounding.
- **Card 3**: D9 (shipped fallback tokens beyond the plan's seven), the shipped-absence half of D4, and the "plan was not amended" fact in D2. Only card to systematically diff shipped artifact against plan text.

## Shared assumptions (A-NNN) — points all three proceed on without scrutiny

- **A-001** The archived-package (done/) vantage legitimately downgrades baseline-dependent AC findings (AC1/AC4) to advisory/MINOR rather than treating them as unpassable-check defects of the plan itself.
- **A-002** Task-2 AC3's escape hatch is an unpassable-check weakness but latent (recorded run green), so MINOR / non-blocking is correct.
- **A-003** All cited file:line references are accurate; no card re-verified any line.
- **A-004** A reflect-pre (pre-execution) lens may legitimately cite shipped design.md artifact lines as evidence.
- **A-005** `other` is an acceptable category for bundled or vantage-related findings rather than forcing them into unpassable-check / missing-requirement / contradiction.

## Similarity assessment

The cards overlap on 3 of 9 diff points (D1, D2-partial, D3-partial) and diverge on 6 (D4-D9 include five unique findings plus one claim-type split). Meaningful diff is well above 10%: 5 of Card 1's findings, 2 of Card 2's, and 2 of Card 3's are unique in whole or part. The SIMILARITY RULE does not trigger; the full debate protocol proceeds.

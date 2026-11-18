# Shadow panel notes — shadow14

## Block repair log (step 4)
- First-parse findings_block_compliance_rate: 0.0 (0/3) — all three cards rejected: heading '## Findings block' missing (reviewers wrote '## Findings').
- Cause: the dispatch/brief instruction line spells the required heading inside a prose sentence, so reviewers rendered it as '## Findings'. Known class (deviation-patterns: shadow07 R-003 shadow09/10 mechanics). Candidate fix: the brief template must state the literal heading and show the fenced block shape.
- Repair: orchestrator replaced the heading line '## Findings' with '## Findings block' in all three cards. No finding JSON line, severity, citation, calibration value, or self-report was altered. Post-repair valid blocks: 3/3.
- verify-citations on the invalid pass checked 0 citations; re-run after repair (below).

## Identity (step 9)
- identity_source: requested-pinned (no transcript model-id read).
- reviewer-2 self-report 'claude-gw-tier1b' disagrees with pin 'claude-haiku-5-5' -> identity_mismatch_suspected: true. Reviewers 1 and 3 self-reports match their classes (tier1b/sonnet; opus).
- While identity is requested-pinned and one mismatch is suspected, the panel makes no claim of verified independence.

## Judge
- Recorded after the legacy debate (step 7).

## Calibrator
- calibrator model class: opus (executor class unknown, reviewers sonnet+haiku+opus). Disjoint set {opus,sonnet,haiku}\{sonnet,haiku,opus} = empty -> calibrator_diversity: degraded (highest-capability class not used by most reviewers; one reviewer per class -> opus picked, which collides with reviewer-3's class).

## Block repair log (step 4, continued)
- Second parse defect: cards 1 and 2 fenced their block as ```json; parser requires info string `findings-v2` (card 3 had it). Orchestrator rewrote the fence info string only. No JSON content altered. Post-repair valid blocks: 3/3 (reviewer-3 valid since pass 1).
- findings_block_compliance_rate stays the FIRST-parse value: 0.0 (0/3).

## Re-ask outcome (step 4)
- Both re-asks returned valid blocks (reviewer-1 F3/F4/F5, reviewer-2 F4 shortened to <=300 chars by the reviewers themselves; reviewer-1's F4/F5 rewrites also dropped the phrasing the calibrator had flagged as mislabelled). Post-repair + post-re-ask valid blocks: 3/3. findings_block_compliance_rate recorded as first-parse 0.0; post-repair count 3/3 (this file, above).

## Debate (step 7)
- Legacy debate ran (Mode A, depth standard): convergence 0.96, base card 1 (analyzer/sonnet 0.83), 13 originals -> 10 merged findings, all MINOR non-blocking. debate_skipped_similar: false (8/9 diff points contested; one category dispute resolved by rule with dissent).
- merged-verdict.yaml written at adversarial/merged-verdict.yaml (EV-1 path) from the child return contract; confirmed on disk.
- Judge identity: judge_model_self_report claude-gw-tier3[1m] (from the child's contract). judge_identity: claude-gw-tier3; class tier3 distinct from all three debater classes (tier1b/sonnet, tier4/haiku, tier1a/opus) -> judge_class_collision: false.
- Not a Fable model, not a Tier 0 alias.

## Evidence validation + attribution check (steps 8-9)
- evidence-validator: 31/31 citations founded, 0 dropped, all 10 merged findings kept at citation level. Zero-drop flag recorded; plausible: reviewers cited accurately (debate pre-trimmed claims) and the validator greps confirmed absence claims (env var, 'degraded').
- Orchestrator attribution check (execution commit 7764bb623, PR #511): design.md at execution had the UNCONDITIONAL Validate row (spec-conformant), no graph:empty/truncated/unresolved tokens, no env var. MF-2 (conditional impact) and MF-10 (extra tokens) were added post-execution by commit 930c5ebc8 (PR #513) -> REFUTED as findings against this package (temporal-misattribution class, 3rd sighting, decisive; same as shadow15's analyze.md case). MF-5 (env var absent) verified absent at every commit -> survives as the package's real omission.
- Final kept findings: 8 of 10 (MF-1, MF-3..MF-9). Refuted: MF-2, MF-10.

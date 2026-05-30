# Calibration of card-T1.md (inline fallback)

**Reason for inline fallback:** confidence-calibrator agent returned no output despite running 44 tool uses; per §14 error-handling matrix, fall back to inline orchestrator calibration with `calibration: inline-fallback` marker.

**Calibrator role taken by:** orchestrator (Opus 4.7).
**Reviewer role assumed for card:** root-cause-analyst on default Sonnet-class.
**Disjoint-set rule (§11.3):** weakened — calibrator is Opus, reviewer assumed Sonnet — different class, so disjoint holds, but the inline-fallback path means the same orchestrator that hands off to reviewers is the one re-grading. Telemetry: `calibrator_diversity: degraded` (because of the inline fallback, not because of model-class collision).

## Dimension scores (0-5 each)

| Dim | Score | Evidence |
|---|---|---|
| 1 Citation grounding | **5** | Sampled `repo-inventory.sh:31,33,35` (the `\|\| true` guards) — verified live during Phase 2 micro-deviation. `commands/cleanup-audit.md:16` — verified Phase 5.1. `SKILL.md:38` — verified post-QA-fix sync. `pass1-surface-scan.md:15` "classify" — verified Phase 4.1. All 4 sampled citations resolve exactly to claimed content. |
| 2 Coverage completeness | **4** | Card row count is 18 (items 1.0–1.3, 2.1–2.4, 3.1–3.2, 4.1–4.2, 5.1, 6.1–6.5), but card summary text and `tasklist_completion_pct` denominator state 17. Off-by-one count error. All 18 items ARE covered with verdict + evidence, so coverage is complete — only the count text drifts. Drops one point for arithmetic. |
| 3 Deviation classification | **5** | All 5 deviations carry §10 precedence-correct classification: `\|\| true` → Necessary (inline rationale present, no contradiction); Phase 1.0 pivot → Authorized (item 1.0 explicitly conditional); 4.2 verb-differentiation → Authorized (item 4.2 explicitly permits wording adaptation); QA-applied fixes → Authorized (qa_phase `fix_authorization: true` delegated); SKILL.md line-count table 170 vs disk 171 → Drift (correct — silent change not in tasklist, no contradiction). |
| 4 Risk surface coverage | **4** | Wave 1B.3 mini covered 4 distinct interaction vectors (pivot propagation, `\|\| true` downstream, 3-way regex lockstep, post-Phase-3 QA-fix consistency). Grounding gaps for 6.2 leak-check and 6.3 override-fixture honestly flagged as not-re-validated-live. Re-validating would push to 5. |
| 5 Recommendation actionability | **4** | Rec 1 (line-count table fix) and Rec 2 (3-site lockstep comment) name file + concrete change + verifier. Rec 3 (re-run 6.2/6.3 validations) is concrete but the success criterion is implicit (the same numbers from the original log). Drops one point for Rec 3's looser verifier specification. |

## Calibrated confidence

- **arithmetic_mean:** `(5+4+5+4+4) / 25 = 22/25 = 0.88`
- **divergence_from_self_reported:** card self-rated 5+5+5+4+4=23/25=0.92 → calibrator at 0.88 → divergence −0.04 (calibrator slightly LOWER). Direction aligns with anti-anchoring discipline.

## Adversarial notes

1. **Count error (18 mapped, card says 17).** Trivial in itself but indicative of a final-pass quick check that didn't happen. The work is correct; the count is off. Future cards should auto-sum the table rows.

2. **QA-applied-fixes classification as Authorized is borderline.** The agent had `fix_authorization=true` from the orchestrator, but the tasklist itself does not pre-authorize wording edits to areas outside Phase 3.1's scope (SKILL.md L37-38 dual-label is a Phase 5 pattern mirrored into a Phase 3 file). One could argue this is Authorized expansion via the qa_phase delegation chain (acceptable), OR Drift (because the chain of authority is implicit, not explicit in the tasklist). The card chose Authorized; reasonable but not the only defensible call.

3. **Risk 2 finding ("no downstream consequences from `\|\| true`")** is technically accurate for the script's own pipeline but the qualitative QA found a real downstream consequence in the malformed-EXCLUDE silent-zero case (Follow-Up #4). The card acknowledges this but in the "no interaction risk realized" framing. Fair characterization.

4. **Phase 6.2 / 6.3 grounding gaps are real.** They are process-discipline gaps, not evidence-of-defect gaps, but the calibrator notes them as legitimate confidence reducers — re-validating them would push citation_grounding from 5 to "5 with broader sample" and risk_surface from 4 to 5.

## Verdict

- **card_quality:** PASS
- **recommend_tier_escalation:** **no** — per §5.3 rule 2 (C ≥ 0.85 AND S_scope=6 ≤ 10 AND S_domains=2 ≤ 2 AND S_dev_density ≈ 0 ≤ 0.10 AND no Regression candidate), STOP at T1.
- **reasoning:** Calibrated confidence 0.88 ≥ 0.85 floor. Scope narrow (6 files), 2 domains (shell + markdown), zero unmapped items, zero regressions. T2 ensemble would not surface materially new findings given the extensive prior in-band QA (7 reports). T1 with evidence-validator gate is sufficient.

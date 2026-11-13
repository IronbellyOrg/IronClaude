# Wave 3C — blind calibration, reviewer-3 card (sonnet-class calibrator, disjoint from opus reviewer)

Note: this calibrator graded the condensed legacy card file as persisted at dispatch time; the full card (verbatim findings block) was persisted afterwards from the same reviewer output. Per-finding ids map 1:1.

## Card scores

Citation grounding 0.85 / Coverage completeness 0.55 / Deviation-classification clarity 0.60 / Risk surface coverage 0.60 / Recommendation actionability 0.45 → **mean 0.61**.

Citation checks it performed: system-architect.md:30-35 numbered bold-label list with new item at :35 confirmed; self-review.md:24-36 item 5 confirmed; technical-writer.md:35 confirmed; Makefile:126-130 sync loop and Makefile:65 PLUGIN_DIST confirmed; plugins/superclaude/agents/system-architect.md lacks the rule confirmed. Fault noted: Makefile:202-206 belongs to verify-sync, not sync-dev (minor citation-attribution error in card prose).

## per_finding (shadow step 5)

```yaml
calibration:
  per_finding:
    F1: 0.88
    F2: 0.65
    F3: 0.65
    F4: 0.5
```

## Calibrator verdicts on self-reported confidence

F1 0.85 about right; F2 0.7 about right (defect status depends on whether the mirror is meant to be synced — orchestrator ground-truthed this separately: build-plugin copies plugins/ verbatim into dist, and the plugin copy differs from committed src, so the sync obligation is real); F3 0.85 too high on this card's own evidence (calibrator lacked tasklist access; the analyzer and qa cards independently verified the four files, calibrating F-wording at 0.9-0.99); F4 0.6 slightly high.

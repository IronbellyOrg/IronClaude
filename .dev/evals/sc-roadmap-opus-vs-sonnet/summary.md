# Eval summary — sc:adversarial direct-mode 5+5 runs

## Per-run metrics

| Group | Run | Status | Convergence | Winner | Base variant | Unresolved | Opus persona | Sonnet persona | Opus KB | Sonnet KB | Debate? | Per-round? | Merged KB |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| A | 1 | partial | 0.836 | opus | opus:default | 0 | default | default | 29 | 27 | ✓ | ✓ | 45 |
| A | 2 | partial | 0.78 | opus | opus:default | 4 | default | default | 17 | 26 | ✓ | ✗ | 0 |
| A | 3 | partial | 0.357 | opus | opus:default | 5 | default | default | 36 | 50 | ✓ | ✗ | 0 |
| A | 4 | PARTIALLY_RESOLVED — CSP without unsafe-inline (V1 D7.4) and subdomain-takeover-prevention runbook need to be tightened; service-worker / first-party-script injection vectors remain | 0.724 | opus | opus:default | 8 | default | default | 19 | 26 | ✓ | ✗ | 0 |
| A | 5 | success | 1.0 | opus | opus:default | 0 | default | default | 26 | 27 | ✓ | ✗ | 49 |
| B | 1 | partial | 0.806 | opus | opus:architect | 7 | architect | analyzer | 34 | 20 | ✓ | ✗ | 54 |
| B | 2 | partial | 0.92 | sonnet | sonnet-architect | 2 | architect | architect | 36 | 46 | ✓ | ✗ | 58 |
| B | 3 | failed | null | unknown | null | 0 | default | default | 50 | 67 | ✗ | ✗ | 0 |
| B | 4 | MISSING_DIR |  |  |  |  |  |  | 0 | 0 | ✗ | ✗ | 0 |
| B | 5 | success | 0.543 | opus | opus | 0 | default | default | 50 | 54 | ✓ | ✗ | 0 |

## Aggregate stats per group (usable runs only — excludes failed/missing)

### Group A
- **n**: 5
- **convergence_mean**: 0.739
- **convergence_stdev**: 0.237
- **convergence_min**: 0.357
- **convergence_max**: 1.0
- **opus_wins**: 5
- **sonnet_wins**: 0
- **unknown_winners**: 0
- **debate_transcript_rate**: 1.0
- **per_round_files_rate**: 0.2
- **personas_seen_opus**: ['default']
- **personas_seen_sonnet**: ['default']
- **opus_variant_kb_mean**: 25.4
- **sonnet_variant_kb_mean**: 31.2

### Group B
- **n**: 3
- **convergence_mean**: 0.756
- **convergence_stdev**: 0.193
- **convergence_min**: 0.543
- **convergence_max**: 0.92
- **opus_wins**: 2
- **sonnet_wins**: 1
- **unknown_winners**: 0
- **debate_transcript_rate**: 1.0
- **per_round_files_rate**: 0.0
- **personas_seen_opus**: ['architect', 'default']
- **personas_seen_sonnet**: ['analyzer', 'architect', 'default']
- **opus_variant_kb_mean**: 40
- **sonnet_variant_kb_mean**: 40

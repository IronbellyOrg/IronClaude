# Explain (advanced): reflect shadow mode and the shadow-model-combos experiment

Source: origin/master, read with `git show`. Codegraph token: graph:stale (index does not cover origin/master).

## Concept
`/sc:reflect --tier 2` runs a review panel: 3 read-only `reflect-reviewer` agents on different model classes
(sonnet, haiku, opus; analyzer, qa, refactorer lenses), a blind `confidence-calibrator` per card, an adversarial
debate (`sc-adversarial-protocol`), and an `evidence-validator` that drops unfounded citations
(SKILL.md:25-42, 622-660, 1227-1266 on origin/master).

A "shadow run" is `--t2-engine shadow` (SKILL.md:309-349). The old ("legacy") panel still decides the verdict.
Next to it, a new deterministic panel kernel (`superclaude review panel resolve`, `manifest`, `cluster`,
`verify-citations`) runs offline and writes only under `<output>/panel/` and into a `telemetry:` block.
No verdict, stable contract field or `merge_method` changes (SKILL.md:338). This is Stage 2 of a staged plan
(brainstorm merged-output.md lines 403-410): Stage 2 exit = 20 shadow runs with zero MALFORMED, EV-1 failure rate
no higher than legacy, parity holds, lint and verdict replay pass (checked by scripts/reflect_shadow_exit.py).

## Advanced points
- Resolution is pure and deterministic: `resolve_slot` (panel.py:500) filters by hard exclusion, picks by
  fixed/random/round_robin; random seed comes from sha256(run_id) in `resolve` (panel.py:565).
- Manifest is a coordinator-owned state machine frozen -> resolved -> dispatched -> collected -> calibrated ->
  clustered -> debated -> validated -> published (manifest.py:1-27, 39-49); same payload under same identity is a no-op,
  different payload raises Conflict.
- Clustering is path-aware union-find with a 3-line span window and support weighting by calibrated confidence
  (cluster.py:1-56). It never feeds the debate in shadow mode.
- Parity: the panel's resolution (`panel/resolution.json`) is compared with the legacy rotation; the aggregator
  recomputes it from card headers instead of trusting the recorded boolean (reflect_shadow_exit.py:12-18).
- Class vs served model: the record holds the CLASS (sonnet/haiku/opus), not the model that actually served it
  (FINDINGS.md "slot called haiku in A and B is served by gpt-6.1-sol").

## The experiment (PR #581 carried it)
`.dev/eval-workspaces/shadow-model-combos/`: 5 model combinations (A-E) x 3 repeats = 15 shadow runs on one frozen
plan (`TASK-WF-designSpec-20261107-075614`). Combos change which model backs the orchestrator/judge and the sonnet,
haiku, opus class aliases via `ANTHROPIC_DEFAULT_*_MODEL` env vars. Result: descriptive only, no quality scoring.
Leads: B (sonnet orchestrator) ran in 23-39 min vs A's 64-68; D and E show lower calibrated confidence; A had a
dispatch collapse in run 3 (all reviewers on sonnet). No blind score against ground truth was done.

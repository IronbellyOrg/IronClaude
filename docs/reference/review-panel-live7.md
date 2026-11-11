# Live 7-reviewer panel (`@live7`)

Issue #346. This page records the panel shape for the live gateway, the `tier2b` model list and how to switch the panel on. The experiment data behind the shape is on the `346Claude-ab-experiment-artifacts` branch under `.dev/research/346-review-loop-experiments/` (`p19/rep/RESULTS.md`, `p19/pn1-variants/RESULTS.md`, `p19/roi/ROI-OF-EXTRA-REVIEWS.md`).

## Shape

| slot | tier | count | strategy | role |
|---|---|---|---|---|
| `t1b` | `tier1b` | 1 | fixed | anchor; first model of the tier (Claude Sonnet 5.5) |
| `t2` | `tier2` | 1 | random | parallel reviewer |
| `t2b` | `tier2b` | 1 | random | parallel reviewer |
| `t3` | `tier3` | 2 | random | parallel reviewers |
| `t4` | `tier4` | 2 | random | parallel reviewers (the tier lists one model, so both draws are that model) |

Seven reviewers, one Sonnet anchor and six parallel. The file is `src/superclaude/cli/review/data/review-panel.live7.json`; the packaged default panel (4 reviewers) is unchanged.

## What the experiments support

The experiments ran this shape with Claude Haiku 5.5 standing in for every non-Sonnet tier (the `anthropic-only` environment resolves `live7` to exactly 1 Sonnet + 6 Haiku). On one spec and a 44-defect ledger, blind-scored:

| panel | fixed per run (of 44) | weighted residual |
|---|---|---|
| 1 Sonnet + 3 Haiku (the default panel's shape) | 15.7 and 15.3 (two batches of 6) | 63.0 and 63.0 |
| 1 Sonnet + 6 Haiku (this shape) | 19.3 and 17.7 (two batches of 6) | 53.0 and 56.8 |

Pooled over both batches the extra Haiku reviewers add about 3 fixed defects per run (p = 0.013); the second batch alone is +2.3 (p = 0.17). These are Haiku stand-ins: the live Tier 2, 2b, 3 and 4 models are not Haiku, and Tier 4 (GPT-6 Luna) is the weakest model in the panel. The live-environment evals in `.dev/research/346-review-loop-experiments/p20/live-evals/` exist to measure that.

## `tier2b`

`tier2b` is declared in `review-tiers.default.json` with the gateway alias `claude-gw-tier2b[1m]` and, in failover order, `gpt-6.1-terra`, `glm-5.3`, `Qwen3.8-max`, `muse-wonder-1.0` (list supplied by the owner on 2026-11-11). `anthropic-only` still resolves it to the Haiku stand-in.

Its models are the first four of Tier 3's list, so the `t2b` slot adds no model that the `t3` and `t2` slots cannot already draw; with `distinct_across_slots` the draws still differ where the pools allow. Whether the slot earns its place is a question for the live evals (`C2-live7-no-t4` and `C3-t4-to-t3`).

Before the panel works on the gateway, the alias must exist there: add `claude-gw-tier2b` to the LiteLLM model list and to the Coder env slots, and add Tier 2b to `src/superclaude/skills/ccsession-tag/MODEL-TIERS.md` and `ccsession-models.json` (those three change together). Not done by this change.

A tier can still be declared as a placeholder (`"placeholder": true` with an empty `models` list): it validates, takes the environment's stand-in where one exists, and otherwise fails closed with `no model available for <tier> (placeholder tier: ...)`.

## Using it

```bash
superclaude review panel resolve --template @live7 --env anthropic-only --run-id demo
superclaude review panel resolve --template @live7 --env gateway --run-id demo   # seven reviewers; needs the tier2b alias on the gateway to run
```

`@NAME` selects a packaged template `review-panel.NAME.json`. `SUPERCLAUDE_REVIEW_PANEL=@live7` does the same for every review command, and a project file `.superclaude/review-panel.json` still takes precedence over the packaged default as before.

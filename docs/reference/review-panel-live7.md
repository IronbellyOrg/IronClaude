# Live 7-reviewer panel (`@live7`)

Issue #346. This page records the panel shape for the live gateway, the open `tier2b` placeholder and how to switch the panel on. The experiment data behind the shape is on the `346Claude-ab-experiment-artifacts` branch under `.dev/research/346-review-loop-experiments/` (`p19/rep/RESULTS.md`, `p19/pn1-variants/RESULTS.md`, `p19/roi/ROI-OF-EXTRA-REVIEWS.md`).

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

## `tier2b` is a placeholder

`tier2b` is declared in `review-tiers.default.json` with the gateway alias `claude-gw-tier2b[1m]`, `"placeholder": true` and an empty `models` list. Behaviour:

- The tier file validates (a placeholder tier must have an empty list; any other tier still needs a non-empty one).
- In `anthropic-only` the environment stand-in (Haiku) resolves it.
- In `gateway` the slot resolves to nothing and `superclaude review panel resolve` fails closed with `no model available for tier2b (placeholder tier: ...)`.

To enable the live panel, replace the placeholder with the real list, in failover order, and drop the flag:

```json
"tier2b": {"alias": "claude-gw-tier2b[1m]", "models": ["<model id>", "<model id>"]}
```

Also update `src/superclaude/skills/ccsession-tag/MODEL-TIERS.md` and the Coder env slots so the tier exists on the gateway; `tier2b` is not deployed there yet.

## Using it

```bash
superclaude review panel resolve --template @live7 --env anthropic-only --run-id demo
superclaude review panel resolve --template @live7 --env gateway --run-id demo   # fails closed until tier2b has models
```

`@NAME` selects a packaged template `review-panel.NAME.json`. `SUPERCLAUDE_REVIEW_PANEL=@live7` does the same for every review command, and a project file `.superclaude/review-panel.json` still takes precedence over the packaged default as before.

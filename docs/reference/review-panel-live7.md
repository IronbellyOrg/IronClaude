# Live 7-reviewer panel (`@live7`)

Issue #346. This page records the panel shape for the live gateway, the `tier2b` model list and how to switch the panel on. The experiment data behind the shape is on the `346Claude-ab-experiment-artifacts` branch under `.dev/research/346-review-loop-experiments/` (`p19/rep/RESULTS.md`, `p19/pn1-variants/RESULTS.md`, `p19/roi/ROI-OF-EXTRA-REVIEWS.md`).

## Shape

| slot | tier | count | strategy | role |
|---|---|---|---|---|
| `t1b` | `tier1b` | 1 | fixed | anchor; first model of the tier (Claude Sonnet 5.5) |
| `t2` | `tier2` | 1 | random | parallel reviewer |
| `t2b` | `tier2b` | 1 | random | parallel reviewer |
| `t3` | `tier3` | 2 | random | parallel reviewers |
| `t4` | `tier4` | 2 | random | parallel reviewers drawn from GPT-6 Luna, Claude Haiku 5.5 and Grok 4.7 (`distinct_across_slots` keeps the two draws different) |

Seven reviewers, one Sonnet anchor and six parallel. The file is `src/superclaude/cli/review/data/review-panel.live7.json`; `@live7` is unchanged by the default-panel change described in the next section.

## The default panel (`@wonsol`, provisional)

With no template argument, no `SUPERCLAUDE_REVIEW_PANEL` and no `review-panel.json`, `superclaude review panel resolve` resolves the 3-reviewer `wonsol` panel. The default is chosen by reference: `src/superclaude/cli/review/data/review-default.json` (`{"schema": "review-default/1", "template": "wonsol"}`) names a packaged template, and `default_template_name()` in `src/superclaude/cli/review/panel.py` reads it. Changing `template` to `classic` switches the default back with no code change; a pointer with a wrong schema, a malformed name or a name with no packaged template fails with an error that names `review-default.json`. The lookup order is unchanged: explicit path, `SUPERCLAUDE_REVIEW_PANEL`, `.superclaude/review-panel.json` of the project, `~/.superclaude/review-panel.json`, then the pointer.

| template | reviewers | what it is |
|---|---|---|
| `@wonsol` (the default) | 3: `t5a` anchor, `t5b`, `t5c` | `muse-wonder-1.0` (fixed anchor, falls back to `claude-sonnet-5-5`), `gpt-6.1-sol`, `muse-ember-1.0` |
| `@classic` | 4: `t1b` anchor, `t2`, `t3` x2 | the previous production default (1x Tier 1b anchor + 1x Tier 2 + 2x Tier 3) |
| `@live7` | 7 | the panel described above |

The three `wonsol` slots use the new tiers `tier5a` (`muse-wonder-1.0`, then `claude-sonnet-5-5`), `tier5b` (`gpt-6.1-sol` only) and `tier5c` (`muse-ember-1.0` only) in `review-tiers.default.json`. Each of `tier5b` and `tier5c` lists exactly one model so that its `random` slot is deterministic.

These three tiers are review-panel seats, not ccsession tiers. Their `claude-gw-tier5a/5b/5c[1m]` alias strings are labels that `review panel resolve` copies into its output and telemetry; nothing in this repository launches a reviewer through them. `ccsession-models.json` and the Coder central defaults define Tiers 0 to 4 only, so no Tier 5 picker entry or `T5*Model` slot exists, and none is needed for the panel to resolve. The model each reviewer must run is the resolution's `model` field.

- In the `gateway` environment the default resolves to `muse-wonder-1.0`, `gpt-6.1-sol` and `muse-ember-1.0`.
- In the `anthropic-only` environment it resolves to `claude-sonnet-5-5` for the anchor and `claude-haiku-5-5` stand-ins for the other two, so that environment runs no wonder, sol or ember model.
- A re-review (`--kind re-review`) resolves only the anchor. That reviewer changes from the Tier 1b model (Claude Sonnet 5.5) to `muse-wonder-1.0` in the `gateway` environment and stays `claude-sonnet-5-5` in `anthropic-only`.

**Status: provisional.** The owner ordered this default change although the confirming test did not meet its pre-registered bar: the found-fraction lead over the control was +0.099 and +0.109 with lower bounds -0.004 and -0.006, and the panel took 1.56 times the control's time. Only the model mix ships. The seat lenses, table caps and briefs of the evaluation harness are not part of this change, so the product panel chooses models only.

## What the experiments support

The experiments ran this shape with Claude Haiku 5.5 standing in for every non-Sonnet tier (the `anthropic-only` environment resolves `live7` to exactly 1 Sonnet + 6 Haiku). On one spec and a 44-defect ledger, blind-scored:

| panel | fixed per run (of 44) | weighted residual |
|---|---|---|
| 1 Sonnet + 3 Haiku (the shape of the `@classic` panel, the default before `@wonsol`) | 15.7 and 15.3 (two batches of 6) | 63.0 and 63.0 |
| 1 Sonnet + 6 Haiku (this shape) | 19.3 and 17.7 (two batches of 6) | 53.0 and 56.8 |

Pooled over both batches the extra Haiku reviewers add about 3 fixed defects per run (p = 0.013); the second batch alone is +2.3 (p = 0.17). These are Haiku stand-ins: the live Tier 2, 2b and 3 models are not Haiku, and Tier 4 mixes GPT-6 Luna, Claude Haiku 5.5 and Grok 4.7 (Haiku 5.5 is a real Tier 4 model). The live-environment evals in `.dev/research/346-review-loop-experiments/p20/live-evals/` exist to measure that.

## `tier2b`

`tier2b` is declared in `review-tiers.default.json` with the gateway alias `claude-gw-tier2b[1m]` and, in failover order, `gpt-6.1-terra`, `glm-5.3`, `Qwen3.8-max`, `muse-wonder-1.0` (list supplied by the owner on 2026-11-11). `anthropic-only` still resolves it to the Haiku stand-in.

Tier 3 is now only GLM 5.3 and Qwen 3.8 Max, and Tier 4 is GPT-6 Luna, Claude Haiku 5.5 and Grok 4.7 (issue 488 layout). `tier2b` adds Terra and Muse Wonder 1.0 beyond what `t3` can draw; with `distinct_across_slots` the draws still differ where the pools allow. Whether the slot earns its place is a question for the live evals.

No LiteLLM gateway entry is needed: the `claude-gw-*` aliases are built in the workspace by the ccsession shim (`local-gateway-alias-proxy.py`) from `ccsession-models.json` on master and the workspace's `T<N>Model0M` env slots. This change adds Tier 2b to `MODEL-TIERS.md` and `ccsession-models.json`; the workspace needs the Coder central defaults that carry the Tier 2b slots (20261110-1 or later), and the gateway must serve the real model ids listed above.

A tier can still be declared as a placeholder (`"placeholder": true` with an empty `models` list): it validates, takes the environment's stand-in where one exists, and otherwise fails closed with `no model available for <tier> (placeholder tier: ...)`.

## Using it

```bash
superclaude review panel resolve --template @live7 --env anthropic-only --run-id demo
superclaude review panel resolve --template @live7 --env gateway --run-id demo   # seven reviewers; needs the Tier 2b slots in the workspace to run
```

`@NAME` selects a packaged template `review-panel.NAME.json`. `SUPERCLAUDE_REVIEW_PANEL=@live7` does the same for every review command, and a project file `.superclaude/review-panel.json` still takes precedence over the packaged default as before.

# Live evals for the #346 review panel

Goal: find the best reviewer panel for the live gateway (Sonnet plus the tiered models) with the same ledger method used in the Haiku experiments, spending as little as possible before the expensive end-to-end runs.

## Why three stages
The earlier work showed (a) the number and type of reviewers that raise a defect drive how often it gets fixed (`../../p19/roi/ROI-OF-EXTRA-REVIEWS.md`: P(fixed | raised by 0, 1, 2, 3+ reviewers) = 0.03, 0.35, 0.50, 0.58), and (b) that model reproduces the measured gains for panel size (1S+6H over 1S+3H: model +2.8, observed +3.7 in the first batch and +2.3 in the replicate). So:

| stage | what | cost | output |
|---|---|---|---|
| 0 | dispatch probe: which models can be launched here and how, at what parallelism | ~12 trivial calls | `probe.json` |
| A | profile each model alone: 3 first-round reports on spec S1, matched to the 44 ledger defects | ~11 models x 3 reports | per-model capture rate, tokens, wall time |
| B | screen every panel composition by simulation from the Stage A profiles (`simulate.py`, closed form, no model calls) | free | ranked panels with expected fixes and cost |
| C | end-to-end confirmation of a shortlist: full PN1 loop, 6 randomized-order runs per panel, blind scoring | the bulk | the decision |

## Files
- `combos.json`: models, the 10 candidate panels (all validate against `review-panel/1`), stage settings and the pre-registered decision rule.
- `simulate.py`: Stage B. Tested against the existing Haiku/Sonnet reports: it gives 12.0 expected fixes for 1S+3H and +2.8 and +4.2 for 1S+6H and 3S+3H, matching the ROI model.
- `render.py`: writes Stage A sandboxes and prompts, per-panel templates plus an eval tier file with `tier2b` filled in, and the Stage C blocked-randomization schedule. Calls no model.
- `prompts/00` to `05`: probe, Stage A operator, blind matcher, Stage C operator, scoring, analysis.
- `harness/`: the PN1 loop driver used for the replicate (reference implementation, see below).

## Before anything runs
1. **`tier2b` models.** Defined by the owner on 2026-11-11 (IronClaude PR #492): `gpt-6.1-terra`, `glm-5.3`, `Qwen3.8-max`, `muse-wonder-1.0`, in that order. `render.py panels --tiers <tier file of the PR-492 checkout>` is enough; `--t2b-models` is only needed to override. No LiteLLM entry is needed for `claude-gw-tier2b`: the ccsession shim builds the alias from `ccsession-models.json` on `master` plus the workspace `T2bModel0N` env slots (Coder release 20261110-1 or later), so panels with a `t2b` slot run live once #498 is on `master`, the workspace has the slots, and the gateway serves the four real model ids. After the issue 488 layout Tier 3 is only `glm-5.3` and `Qwen3.8-max`, Tier 4 is `gpt-6-luna`, `claude-haiku-5-5` and `grok-4.7`, and `claude-haiku-5-5` is a real live model, so the Haiku data from earlier experiments maps directly. Terra and Muse Wonder 1.0 are reachable only through Tier 2b (and Tier 2 for Muse Wonder), so Stage A and the `C2`/`C3` panels test whether the slot adds anything. `C3` replaced the old t4-to-t3 variant with t4-to-t2, and `C4` is now wide Tier 2b, because a bigger Tier 3 would repeat models.
2. **Dispatch.** The tier file says the gateway's dispatch mechanism per model is not defined yet. Prompt 00 finds out what works in the live session; do not assume the Agent tool's `model` argument reaches gateway models. A silent fallback to another model invalidates a run.
3. **Harness adaptation.** `harness/harness.py` is the replicate's driver. It reads three environment variables for the live panel (`PN_ENV`, `PN_PANEL`, `PN_TIERS`) and a run prefix (`PN_PREFIX`). Still to set for the live checkout: the path constants near the top (`S`, `SP`, `AB`, `REPO`, `S1`, `TASKS_GLOB`, `CLI`, `TELEMETRY_DIR`), `MAX_CONCURRENT`, and `alias_for`/`EXPECTED_MODEL` so a requested gateway model maps to the launch string Prompt 00 found and the observed-model check accepts it. It has not been run in the live environment.
4. **Budget approvals.** Opus 5.5 only for the Stage C rescore of four specs (and Stage A only if the owner approves). Fable / Tier 0: never.

## Stage C design (pre-registered in `combos.json`)
Six runs per shortlisted panel, one run of each panel per block, order shuffled inside the block, constant concurrency, blind scoring on the 44-defect ledger, permutation tests against the default panel and against `C1-live7`. Decision rule: adopt the cheapest panel whose mean fixed is within 1.0 of the best shortlisted panel and at least 2.0 above C0 with p < 0.10; otherwise keep C0.

Rough size: the replicate ran 12 loop runs in about 70 minutes at 12 in flight (launch 20:25, last audit about 21:34), so a 5-panel shortlist of 30 runs is roughly 3 hours at similar parallelism and all 10 panels (60 runs) roughly 6 hours. Live gateway models may be slower or rate-limited, so measure Stage A wall times first. Stage B exists to avoid running all ten.

## What this does not settle
One spec and one ledger; the matcher and scorers are Sonnet; live models differ from the Haiku stand-ins, and Tier 4 (one model) gives no diversity inside its slots.

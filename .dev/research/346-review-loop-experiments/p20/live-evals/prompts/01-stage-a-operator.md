# Prompt 01: Stage A operator (single-model profiles, live)

Prerequisite: Prompt 00 produced `probe.json`. Profile only models marked launchable.

1. `render.py stage-a --out stage-a/runs --repo-root <checkout of the PR branch> --reps 3 --models <launchable ids>` writes one sandbox and one `PROMPT.md` per (model, rep) plus `manifest.json`. Each `PROMPT.md` is the first-round reviewer brief used in every earlier experiment (spec-panel critique, FIRST-REVIEW prompt, findings block required).
2. Launch every manifest entry as a sub-agent on its model, with the mechanism recorded in `probe.json`, as many at once as `probe.json` says is safe, with the prompt text "Read <prompt path> and follow it exactly." Never use Fable / Tier 0. Order the launches by a shuffle with seed 20261111 so no model is systematically first.
3. For each finished run record: output tokens, wall seconds, and the model the gateway actually served (from the transcript or gateway log). A served model different from the requested one makes that report invalid: relaunch once, then drop it and note it.
4. Check each report has a parsable `findings-v1` block; relaunch once if not.
5. For each valid report run Prompt 02 (blind matcher, Sonnet) to produce `stage-a/profile/<run>.json`.
6. Write `stage-a/tokens.json` = `{"<model id>": <mean output tokens per report>}`.
7. Run Stage B: `python3 simulate.py --reports stage-a/profile --ledger ../../p17/ledger.json --panels combos.json --tiers <tier file with tier2b filled> --tokens-file stage-a/tokens.json`, and `--enumerate 5`, `6`, `7`, `8` (each with `--top 10`). Save the outputs to `stage-a/STAGE-B.md`.
8. Pick the Stage C shortlist by `combos.json` `stage_b.shortlist_rule` and write it to `stage-c/shortlist.json`.

Report per-model: mean distinct defects raised, mean blocking raised, tokens, wall time, plus the Stage B tables. Do not run Stage C.

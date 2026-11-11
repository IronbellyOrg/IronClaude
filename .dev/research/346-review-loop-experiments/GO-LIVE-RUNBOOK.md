# Go-live runbook: tiered review panel, ccsession Tier 2b, live evals (2026-11-11)

Status as of this document. Facts marked **[checked]** were read from the repos or GitHub today; **[not checked]** are things I could not see (your LiteLLM config, live workspaces).

## 1. Where things stand

| Item | State |
|---|---|
| IronClaude #490, #491, #492 (live 7-reviewer panel, review fixes, tier2b models) | Merged into `346Claude-integration` **[checked]** |
| IronClaude #493 (ccsession `tier2b`, Tier 3 = 2 models, Tier 4 = 3 models) | **Open draft, not merged. Do not merge into `master` early.** CI never ran on it **[checked]** |
| Coder #495: central defaults release `20261110-1` (the T2b/T3/T4 slots) | On Coder `main`; the distribution workflow succeeded on push and on the hourly schedule **[checked]**. Install on every workspace **[not checked]** |
| Coder #496: `JEV_API_URL` exported by the template | Merged **[checked]**. Jev is still off by default |
| Review panel default | Unchanged (`@live7` is opt-in via `SUPERCLAUDE_REVIEW_PANEL=@live7`) |
| Jev | Tested and not adopted. The Jev-split merge A/B gave -3.0 fixed defects (p = 0.18) at equal tokens |
| Live evals (`p20/live-evals`) | Kit built, not run live. Lives only on the research branch `346Claude-ab-experiment-artifacts` (no PR) |

## 2. What this session established (for the go/no-go)

- **Panel shape:** more cheap reviewers add fixes (doubled Haiku: about +2 to +3 pooled, p about 0.013; replicate alone p = 0.17). PN1 itself is stable.
- **Jev:** useless on multi-step judgments (A1/A2/A3, fix verification, loop stopping). Accurate on short one-judgment questions (duplicate findings AUC 0.98-0.99, bug vs feature 96%). Winning on duplicates did **not** improve the final specs in the live A/B. Needs an end-to-end test before any adoption. Details: `p21/RESULTS.md`, `p22/AB-RESULTS.md`.
- **Live models are untested in the loop.** Everything so far used Haiku/Sonnet stand-ins. The live evals are the first test with the real tier models.

## 3. Setup work for you, in order

### A. Confirm Coder release 20261110-1 is on every workspace (gate for step C)

1. Pick the workspace list: running **and stopped**.
2. In each: `cat /etc/aidev02/aienv.d/VERSION` must print `20261110-1` or higher. A stopped workspace restores an older copy at start and catches up within about an hour.
3. Spot-check the slots: `env | grep -E '^T(2b|3|4)Model'` should show `T2bModel01..04`, `T3Model01..02`, `T4Model01..03`.
4. Procedure and convergence rules: Coder `docs/operations/central-defaults-distribution.md`.

Do not go to step C until every workspace passes. A workspace without the T2b slots stops its tier-mode ccsession launch with `T2bModel01 is not set (needed by tier2b)`.

### B. Gateway: only the real model ids need to exist (no alias to add)

`claude-gw-tier2b` is **not** a LiteLLM entry. The ccsession shim (`src/superclaude/skills/ccsession-tag/local-gateway-alias-proxy.py`) builds every `claude-gw-tier<N>` alias itself from `ccsession-models.json` on `master` (#493) plus the workspace env slots (Coder release `20261110-1`), swaps the alias for the real model id, and fails over down the list. So the Tier 2b "gateway work" is:

1. Confirm the gateway serves the four real ids: `gpt-6.1-terra`, `glm-5.3`, `Qwen3.8-max`, `muse-wonder-1.0` (issue 488 open item "gateway id verification"). They are listed in `GET <gateway>/v1/models`, or request each once and check the returned model.
2. Confirm the Tier 3 and Tier 4 ids still resolve: `glm-5.3`, `Qwen3.8-max`, `gpt-6-luna`, `claude-haiku-5-5`, `grok-4.7`.

Nothing else to add on the gateway. (Some docs, including `review-panel-live7.md` and the live-evals README, say the alias "must exist on the LiteLLM gateway"; that is wrong and should be corrected.)

### C. Land #493 (ccsession data), then promote to master

1. Mark #493 ready for review; get CI green (none was observed). Ask for `@codex review`.
2. Merge #493 into `346Claude-integration`. This is safe at any time.
3. Merge `346Claude-integration` into `master` **only after step A passes**. Every ccsession launch fetches `ccsession-models.json` from `master`.
4. Verify on one workspace: `ccsession --tier 2b` starts and the `/model` picker shows Tier 2b with Terra, GLM, Qwen, Muse Wonder 1.0.

### D. Coder release B (after C is on master)

1. Add `tier2b` to the member entry of `CCSESSION_TIER_RULES` (members then see Tiers 2, 2b, 3, 4). It must not name `tier2b` earlier.
2. Drop `T3Model03`-`T3Model06` from `defaults.sh`.
3. Bump `VERSION` to a higher `YYYYMMDD-N`, regenerate `defaults.sha256`, add a CHANGELOG entry (the release procedure is in the central-defaults doc). Roll out the same way as step A.

### E. Other open items from issue 488 (not in #493)

`issue-worker-t3` pin; the `haiku` alias; the retry-ladder rung that reads `T3Model01`; historical design docs. These do not block the panel.

### F. Run the live evals (after A to C)

Kit: `.dev/research/346-review-loop-experiments/p20/live-evals/README.md` on the research branch.

1. **Stage 0, dispatch probe** (`prompts/00-dispatch-probe.md`): find out how a reviewer actually reaches a gateway model from a live session. Do not assume the Agent tool's `model` argument reaches gateway models; a silent fallback to another model invalidates a run.
2. **Adapt the harness** (README "Harness adaptation"): path constants, `MAX_CONCURRENT`, and `alias_for`/`EXPECTED_MODEL` so the requested gateway model matches what Stage 0 found and the observed-model check accepts it. It has never run live.
3. **Budget approvals:** Opus 5.5 only for the Stage C rescore of four specs; Fable / Tier 0: never.
4. **Stage A** (profile each model alone: 3 reports per model, Sonnet matcher), then **Stage B** (simulate panels with `simulate.py`, shortlist), then **Stage C** (6 runs per shortlisted panel, blocked random order, constant concurrency, blind scoring).
5. **Decision rule** (pre-registered in `combos.json`): adopt the cheapest panel whose mean fixed is within 1.0 of the best and at least 2.0 above the default, p < 0.10; else keep the default.
6. **Time:** about 3 hours for a 5-panel shortlist at 12 in flight, if the gateway models keep pace; measure Stage A wall times first.

### G. Jev: recommendation is to leave it off

Only do this if you want it available for further experiments. Full runbook: `docs/docs-product/ops/jev-litellm-gateway-operational-guide.md` (research branch).

1. Gateway: set `TYPESAFE_API_KEY` on the proxy; run Step 1.2 (confirm the route prefix, with and without `/cli`); smoke-test `/typesafe/v1/systemone`.
2. Budget (Ryan Wiancko): set the monthly cap and 50% / 80% alerts; create virtual keys.
3. Users: `printf %s "$KEY" | coder secret create jev --env JEV_API_KEY` (the template already exports `JEV_API_URL`).
4. Nothing in the product calls Jev today. Next Jev candidate worth an end-to-end test: bug-vs-feature classification in `/sc:issue --create`.

### H. Housekeeping

- Delete the stray remote branch `346Claude-pn4-live-panel` (it was superseded by `346Claude-pn4-live-panel-7slot`).
- The research branch `346Claude-ab-experiment-artifacts` has no PR; decide whether to open one or keep it as an archive.
- `gh` has an invalid token in the cloud session, so PRs were opened through the GitHub connector and the `/sc:pr-submit --monitor 3` checklist item is unmet on #490-#493. Fix the token or run `/sc:pr-submit` locally.
- Codex security review hit its usage limit on #492; re-run `@codex security review` once credits are enabled.
- CI was not observed on any of #490-#493. Check the workflows that run on PRs into `346Claude-integration` (they appear not to).

## 4. Rollback

- ccsession data: revert the #493 merge on `master`. Workspaces on the new Coder release keep working (extra slots are harmless); a workspace on the old release plus the new JSON is the broken combination, which is why the order above matters.
- Coder defaults: restore the previous `defaults.sh`, regenerate `defaults.sha256`, publish a fresh higher `VERSION` (never reuse an old identifier).
- Review panel: unset `SUPERCLAUDE_REVIEW_PANEL`; the default panel is unchanged.
- Jev: remove the user secret, or unset `TYPESAFE_API_KEY` on the proxy.

## 5. Key paths

- This runbook: `.dev/research/346-review-loop-experiments/GO-LIVE-RUNBOOK.md`
- Live evals kit and prompts: `.dev/research/346-review-loop-experiments/p20/live-evals/`
- Jev results: `p21/RESULTS.md`, `p22/AB-RESULTS.md`, `p22/JEV-OUTSIDE-USES-AND-PROPOSALS.md`
- Panel doc: `docs/reference/review-panel-live7.md` (on `346Claude-integration`)
- ccsession tiers: `src/superclaude/skills/ccsession-tag/MODEL-TIERS.md`, `ccsession-models.json`
- Coder: `docs/operations/central-defaults-distribution.md`, `templates/VSCode-AIDev02/image/aienv.d/`

# Shadow Run and Review Panel (reflect Tier 2): what it is and how to reuse it

Date: 2026-11-17. Source: origin/master, read with `git show` / `git grep` (the local checkout is an old branch).
Companion explanation file: `/home/coder/workspaces/IronClaude/.dev/analysis/20261117-new-systems/shadow-run-and-review-panel-explain.md`

## 1. What it is

**Plain answer first: the Review Panel and the Shadow Run are older than 72 hours. Only the experiment that uses them is new.**

- The **Review Panel** is the Tier 2 mode of `/sc:reflect` (a review of a plan or finished work). Three read-only reviewer agents on different model classes each write a review card; a separate agent re-grades each card blind; an adversarial debate merges them; an evidence validator drops citations it cannot re-read. It is described in `src/superclaude/skills/sc-reflect-protocol/SKILL.md` sections 1, 7.1, 11.2-11.4 (origin/master). Its rewrite as a deterministic "panel kernel" is the Stage 0-2 work merged as PR #519 on 2026-11-12 (dormant kernel plus shadow mode). That is 5 days before today, outside the 72 hour window.
- A **Shadow Run** is `/sc:reflect ... --tier 2 --t2-engine shadow`. The old panel still produces the verdict. The new kernel runs beside it, offline, and only writes files under `<output>/panel/` and a `telemetry:` block. It exists to measure whether the new kernel could replace the old panel safely (SKILL.md section 4.3a, lines 309-349). Also PR #519.
- What is **new in the window** is an experiment that used shadow runs to compare model combinations: `.dev/eval-workspaces/shadow-model-combos/` (PLAN.md, FINDINGS.md, combos.json, 15 run folders, results.jsonl/md, analysis/extract.py). It arrived in commit `fc4b22402`, merged as **PR #581** (merged 2026-11-17 00:30 UTC; commit dated 2026-11-16 local). PR #581's title and body are about a different thing (`superclaude review safety-scan`, issue 552 stage 0 and 1); the experiment folder was bundled into that commit and the PR text does not mention it. Folder status: PLAN.md says "designed, NOT run" (dated 2026-11-13) but FINDINGS.md and 15 run folders show it was then run; PLAN.md was not updated.
- Other review work in the window, as background only: PR #582 (merged 2026-11-17 03:32 UTC) changes the review severity rule and adds `superclaude review fixcheck`; PR #581 adds `review safety-scan`. Neither is a panel or a shadow run. `/sc:spec-panel` (src/superclaude/commands/spec-panel.md) is an older, different "panel of expert personas" command.

**Entry points.** Command `/sc:reflect` (src/superclaude/commands/reflect.md); skill `sc-reflect-protocol`; agent `reflect-reviewer` (read-only tools); agents `confidence-calibrator`, `evidence-validator`; CLI `superclaude review {panel,manifest,cluster,verify-citations,merge,...}` (src/superclaude/cli/review/__init__.py); scripts `scripts/reflect_shadow_exit.py` and `scripts/reflect_verdict_replay.py`; experiment `.dev/eval-workspaces/shadow-model-combos/`.

## 2. How it works

Paths below are on origin/master. "Stage" means a step of the staged rollout in `.dev/brainstorms/20261111T182026-reflect-tier2-panel-replacement/adversarial/merged-output.md:403-410`.

### 2.1 The review panel end to end (what a real Tier 2 run does)

1. **Wave 0 to 2 (SKILL.md:135-163).** Parse flags, snapshot the inputs with a sha256, resolve model aliases, run a single-agent Tier 1 pass with real-code grounding, blind-calibrate that card, then a rubric decides whether to escalate to Tier 2.
2. **Reviewer choice (SKILL.md:644-660).** Three reviewers (sonnet, haiku, opus or another class) with lenses analyzer, qa, refactorer. All are the fixed `reflect-reviewer` agent, which has no Bash/Edit/Write/Task tool, so a reviewer cannot change the repo it audits. The executor's own model class is removed from the pool (anti self-confirmation); below 2 reviewers the run degrades to Tier 1 with a warning.
3. **Briefs (SKILL.md:303-305).** Each reviewer gets a self-contained brief file with its card slice, grounded file:line hunks and coverage rows. Briefs may not tell a reviewer to run commands.
4. **Blind calibration (SKILL.md:1240-1262).** One `confidence-calibrator` per card sees only the card, not how it was formed. The calibrator's class should differ from the reviewer classes (`calibrator_diversity: full | degraded`).
5. **Debate and merge (SKILL.md:161, 351-359).** `sc-adversarial-protocol` merges the calibrated cards. If that skill is missing, a loud fallback to the best single reviewer is used.
6. **Evidence gate (SKILL.md:1227-1238).** `evidence-validator` re-reads every cited file:line and drops unfounded ones. Zero drops is flagged as suspicious, not clean.
7. Output: `REPORT.md`, `return-contract.yaml` (contract_version 1.8.0), `audit.log`, plus cards and adversarial artifacts.

### 2.2 What a shadow run adds (SKILL.md:338-349)

The shadow run keeps steps 1 to 7 as they are (the legacy panel stays "authoritative and unchanged") and, beside them, does these steps, each followed by `superclaude review manifest advance --stage <s>`:

| Step | What | Code |
|---|---|---|
| Resolve and freeze | `superclaude review panel resolve --template @reflect-pre --env anthropic-only --hard-exclude-class <executor> --strict-distinct`. A slot template (`review-panel.reflect-pre.json`: anchor tier1b fixed, tier4 random, tier1a random) is turned into a model list by a pure function. Seed for random slots comes from sha256 of the run id. | `src/superclaude/cli/review/panel.py:500` (`resolve_slot`), `:565` (`resolve`); `data/review-panel.reflect-pre.json:1-13`; tiers in `data/review-tiers.default.json:4-11` |
| Parity | Compare the panel's (persona, model class) list with the legacy rotation and with the reviewer card headers; record `panel_parity`. A mismatch blocks nothing. | SKILL.md:341; `scripts/reflect_shadow_exit.py:12-18` |
| Dispatch and normalize | Legacy dispatch, plus one extra instruction line so each reviewer ends with a machine-readable `## Findings block`. One bounded re-ask if the block is invalid; the orchestrator never fixes a block itself. `findings_block_compliance_rate` is the share valid on the first parse. | SKILL.md:342-343 |
| Calibration | Same legacy calibrator, plus one line asking for a per-finding confidence. | SKILL.md:344 |
| Cluster and pre-check | `review cluster` groups findings that cite the same file within 3 lines with compatible refs (union-find), weights support by calibrated confidence, and reports `cluster_agreement`. `review verify-citations` flags quotes not found, missing files, out-of-range lines. Neither drops or routes anything; flagged citations are just forced into the validator's re-read set. | SKILL.md:345; `src/superclaude/cli/review/cluster.py:1-56` |
| Identity | Record whether the model id was observed or only "requested-pinned"; a self-report that differs from the pin sets `identity_mismatch_suspected`. | SKILL.md:348 |
| Publish | `manifest advance --stage published` records hashes of the three legacy output files and rewrites nothing. | SKILL.md:349; `manifest.py:24-26` |

The manifest is a coordinator-written state machine `frozen, resolved, dispatched, collected, calibrated, clustered, debated, validated, published` (or `failed`); a reader trusts only `published` (`src/superclaude/cli/review/manifest.py:1-9, 39-49`). Re-submitting the same payload is a no-op; a different payload under the same identity raises Conflict (manifest.py:13-19).

### 2.3 Why a shadow run cannot affect real runs

- Default engine is `legacy`; `shadow` must be asked for, and it is read only after the final tier is 2 (SKILL.md:311-313, rules D1-D2 at 317-318). Quick/Tier 1 runs never read it.
- No stable contract field, `merge_method` or contract version changes; shadow fields live under `telemetry:` (SKILL.md:338, 349).
- Every panel artifact goes to `<output>/panel/`; a step that cannot run records `panel_fallback_reason` and the run continues as legacy (SKILL.md:338).
- A shadow floor shortfall (rule D3) is telemetry only: no status change, no banner (SKILL.md:319).
- `scripts/reflect_shadow_exit.py` reads files only (no model, process, or network) and only writes its optional `--out` report (lines 4-5). It counts runs whose manifest says `t2_engine_effective: shadow` and state `published`, and gives PASS / FAIL / INSUFFICIENT-RUNS (exit 0 / 1 / 3) (lines 7-8, 33-34, 55-57). The Stage 2 exit bar is 20 runs; `REQUIRED_RUNS = 20` (line 55).
- `scripts/reflect_verdict_replay.py` re-derives each verdict with `derive_verdict` and flags any new degraded reason in the shadow runs against the legacy baseline (reflect_shadow_exit.py:23-24).

### 2.4 The experiment (new in the window)

**Design (PLAN.md, combos.json).** One frozen input, `TASK-WF-designSpec-20261107-075614` (a tasklist plus its `source.md`; chosen because an earlier study had ground truth for it: 10 defects, 5 that blocked implementation; PLAN.md section 4). Five combinations, 3 repeats each, 15 runs. Each run is launched as `claude -p "/sc:reflect --mode pre ... --tier 2 --t2-engine shadow --output <run>" --model <orchestrator>` with env `ANTHROPIC_DEFAULT_SONNET_MODEL`, `_HAIKU_`, `_OPUS_` set to different gateway aliases (PLAN.md lines 137-150, combos.json). Output goes under the experiment's own `runs/` folder, not `.dev/reflect/`, so the runs do not count toward the Stage 2 exit (PLAN.md lines 123-124). The memory files that reflect writes (`last-pass-*`, `deviation-patterns-*`) were frozen and restored before each block so run 2 does not read run 1's summary (PLAN.md lines 128-131; `frozen/`). The skill was hashed per block and not re-synced mid-experiment (FINDINGS.md line 4).

| Combo | Orchestrator / judge (`--model`) | Sonnet slot | Haiku slot | Opus slot | Change vs previous |
|---|---|---|---|---|---|
| A pilot baseline | tier3 alias (GLM 5.3 per a 2026-11-11 probe, UNVERIFIED now) | tier1b (Sonnet 5.5) | tier2 (GPT 6.1 Sol) | tier1a (Opus 5.5) | reference |
| B | tier1b (Sonnet 5.5) | same | same | same | orchestrator only |
| C | tier1b | same | `claude-haiku-5-5` | same | haiku slot is a real Haiku |
| D | tier1b | same | Haiku 5.5 | `gpt-6-luna` | Luna replaces Opus |
| E | tier1b | Haiku 5.5 | Luna | tier4 (Luna) | the earlier study's best panel; many changes at once |

**Metrics recorded per run** (PLAN.md lines 153-175; `results.jsonl` keys, extracted by `analysis/extract.py`): wall minutes, calibrated confidence, clustered finding count, first-pass findings-block compliance, parity, lint-clean, reviewer models requested vs served (from the stream log), distinct served reviewers, output tokens, Claude Code's USD estimate, EV-1 (debate evidence rule) and identity mismatch. Precheck and cluster files per run: `panel/precheck.json` (for E1: 53 citations checked, flags `quote-not-found` 2, `missing-file` 1, `out-of-range` 1), `panel/notes.md`, `panel/manifest.json`.

**Decision rule fixed before launch (PLAN.md lines 177-190):** no significance tests; a "lead worth a bigger run" only if ranges do not overlap, the median gap exceeds A's own range, and both combos ran as designed in 2 of 3 runs.

**Results (FINDINGS.md; numbers from results.md).** All 15 runs reached `published` with 3 of 3 reviewers complete.

| Combo | Minutes, median (range) | Calibrated confidence | Clustered findings | First-pass compliance | Output tokens | USD estimate |
|---|---|---|---|---|---|---|
| A | 64 (19-68) | 0.77 (0.75-0.84) | 21 (13-24) | 0.67 x3 | 220k (94k-221k) | 22.9 (11.9-24.6) |
| B | 25 (23-39) | 0.71 (0.68-0.78) | 12 (11-25) | 1.0 x3 | 241k (200k-335k) | 35.6 (33.1-50.3) |
| C | 33 (33-34) | 0.74 (0.68-0.76) | 19 (14-27) | 1.0 x3 | 335k (312k-363k) | 36.1 (32.5-41.2) |
| D | 27 (18-30) | 0.65 (0.62-0.66) | 16 (15-19) | 1.0 x3 | 296k (185k-330k) | 29.2 (28.4-43.8) |
| E | 24 (22-30) | 0.59 (0.53-0.68) | 19 (15-23) | 1.0, 0.67, 0.33 | 321k (299k-367k) | 26.5 (25.5-37.1) |

Findings the authors drew:
1. **The panel record lies about the served model.** The "haiku" slot in A and B was served by `gpt-6.1-sol`; `resolution.json`, card headers and `panel_parity` show only the class (FINDINGS.md lines 15, 5-14). Only the stream-log transcript shows the truth.
2. **Dispatch collapse.** In A3 the orchestrator passed no model class, so all three reviewers and the calibrators ran on `claude-sonnet-5-5` (results.md line 35; FINDINGS.md line 9). The earlier pilot saw 6 of 9 collapsed runs (PLAN.md line 66-68).
3. **Three "leads" (not findings):** orchestrator speed (A 64-68 min when dispatched as designed vs B 23-39), lower calibrated confidence in D and E, and first-pass compliance 0.67 in every A run vs 1.0 in B-D.
4. **Not different:** clustered counts overlap; C vs B (real Haiku vs GPT-6.1-sol in the haiku slot) show no separation; USD is Claude Code's estimate from model names, not a bill.
5. **E ran only 2 distinct served reviewer models** (two Luna) with 3 reviewers (results.md "distinct served reviewers" column).
6. **Result on quality: none.** No blind scoring against the ground truth was done, so nothing says which combination finds more real defects (FINDINGS.md lines 3, 42).

Note on cost: the cost and token columns come from Claude Code's own `result` event; the contract's own `wall_clock_ms`/`token_usage` are orchestrator estimates and the plan says never to compare them (PLAN.md line 164-165).

## 3. Where it could be integrated in future

The reusable idea is not the review panel itself but two patterns it proved out: (a) **shadow mode**, run a candidate beside the authoritative path, write only to a side folder, compare with scripted checks; (b) a **model-combination matrix** with a fixed input, fixed prompt, frozen memory/skill state, repeats, and a decision rule set before launch.

| System type | Why it fits |
|---|---|
| Any multi-agent skill whose model per role is chosen by env aliases (adversarial debate, troubleshoot Tier 2, swarm lenses) | Same coupling problem: role to class alias to served model. Pattern (b) tells you which role actually needs an expensive model. |
| Replacing a prompt-driven stage with a deterministic script (merge, clustering, routing) | Pattern (a) lets the script run on live inputs with zero effect on verdicts until a replay shows no new failure reasons (what `reflect_verdict_replay.py` does). |
| Model or gateway migrations (a tier alias changes the model behind it) | The experiment found alias-to-model drift (tier aliases hiding different vendors). A small matrix before a switch catches dispatch collapse and format-compliance drops. |
| CI-style regression of review quality | With ground truth (defects known to have hurt real implement runs), the matrix becomes a score, not just a count. The earlier study has such ground truth for 3 plans (PLAN.md lines 13-17). |
| Cost control of long-running review loops | The plan's own table shows 5-reviewer panels give no gain at 2-4x cost (PLAN.md line 22); a matrix keeps that kind of claim checked as models change. |

## 4. Integration guide

Best route: reuse the experiment's shape, not its files. Steps:

1. **Pick one frozen input with an answer key.** Copy only the artifacts under test into `input/<id>/`; leave out history that holds the answer (PLAN.md lines 115-119). Record sha256 of each.
2. **Write `combos.json` first** (schema `shadow-model-combos/1`): one entry per combination with `model`, the three `ANTHROPIC_DEFAULT_*_MODEL` values, and a one-line hypothesis. Design it as a chain of single changes so adjacent pairs isolate one factor (PLAN.md lines 77-81); label any multi-change combo (E) as a package.
3. **Freeze state.** Hash the skill file before each block; restore the per-slug memory files before each block; do not run `make sync-dev` or `superclaude install` mid-run (PLAN.md lines 128-133).
4. **Launch** with the pinned form `claude -p "/sc:reflect --mode pre --spec ... --tasklist ... --tier 2 --t2-engine shadow --output <run dir>" --model <orchestrator> --output-format stream-json --verbose --forward-subagent-text`, unsetting `ANTHROPIC_MODEL`, `CLAUDE_CODE_SUBAGENT_MODEL` and the `SUPERCLAUDE_REVIEW_*` variables (PLAN.md lines 143-149). Name runs `pre-<id>-combo<X>-r<n>` and keep them in the experiment folder so `reflect_shadow_exit.py --runs-root` can be pointed at them without polluting `.dev/reflect/`.
5. **Randomise order within a block**, run all combos of a block together, start the next block when all exit (PLAN.md lines 127-128).
6. **Extract** with `analysis/extract.py` (reads `return-contract.yaml`, `adversarial/merged-verdict.yaml`, `panel/*`, stream logs, and the exit script's per-run parity/EV-1/lint). Take served models from the stream log (`message.model` per `parent_tool_use_id`), never from `resolution.json`.
7. **Apply the decision rule written before launch**; mark runs with `dispatch_ok: false` or `leak: true` instead of dropping them.
8. **Optional scoring step:** blind Opus judge per run against the ground-truth file, with model and combo names stripped (PLAN.md lines 171-175).

Interfaces to call: `superclaude review panel resolve|validate`, `review manifest init|advance`, `review cluster`, `review verify-citations` (cli/review/__init__.py), and `uv run python scripts/reflect_shadow_exit.py --runs-root <dir> --required 15 --out <file>`.

**Reuse:** `analysis/extract.py` (193 lines), `scripts/reflect_shadow_exit.py`, `scripts/reflect_verdict_replay.py`, `src/superclaude/cli/reflect/panel_lint.py` (lint of the panel contract).

**Pitfalls (all seen in the data):**
- Class, not model, is recorded. A "haiku" slot may be served by another vendor (FINDINGS.md line 15).
- Dispatch collapse when the orchestrator omits the class (A3).
- `review panel resolve` has no reviewer-count option, so the panel resolution can differ from the legacy rotation (SKILL.md:340); E ran two distinct served models for three reviewers.
- Raw model ids as `ANTHROPIC_DEFAULT_*` values were UNVERIFIED before the run (PLAN.md lines 195-197); the served-model table shows they were honoured (C, D, E served the raw ids).
- Shared memory slug between runs leaks run 1 into run 2 if not restored.
- 25-90 minutes per run and about USD 12-50 estimated per run; do not run 15 at once without checking gateway load (PLAN.md line 199).

**Tests to add** (I did not check whether tests already cover the experiment tooling; UNVERIFIED): a unit test of `extract.py` on a two-run fixture; a test that `reflect_shadow_exit.py` returns exit 3 with fewer than `--required` runs and 1 on one malformed manifest; a lint test that fails a shadow run whose served reviewer models collapse to one while three were requested.

## 5. IronClaude fit

Real targets on origin/master, ranked by value. The fit is good for the review panel itself; it is weak outside review and multi-agent skills.

**1. Record and enforce the served model in the reflect panel.**
- Target: `src/superclaude/skills/sc-reflect-protocol/SKILL.md` (4.3a steps 2 and 9, lines 341 and 348), `src/superclaude/cli/reflect/panel_lint.py`, `scripts/reflect_shadow_exit.py`.
- Change: SKILL.md already tells the orchestrator to write a `model_observed:` header when the harness reports a different model (line 341). Make the orchestrator fill it from the stream, and add a lint rule and an exit-script count for "distinct served reviewer models fewer than reviewers requested" (the A3 collapse and the E two-Luna case).
- Value: high. The experiment shows the current record (`panel_parity`, `reviewer_models`) cannot detect a collapse; this is the main confounder of every panel measurement.
- Effort: low to medium (one prompt line, one lint rule, one test). Risk: low; telemetry only under `shadow`.

**2. Finish the Stage 2 exit with the experiment's runs plus a blind quality score.**
- Target: `scripts/reflect_shadow_exit.py` (needs 20 runs, line 55), `.dev/eval-workspaces/shadow-model-combos/`, ground truth on the branch commit `b4db265a8` named in combos.json.
- Change: run the exit script over the 15 experiment runs (needs 5 more, or lower `--required`), then run the optional blind scoring that PLAN.md left to a separate approval.
- Value: high; it is the only way to say which model combination finds real defects. Effort: medium. Risk: token cost (not estimated here); also a Stage 2 count mixes the experiment's non-default combos with default ones, so keep them out of the official count as the plan does.

**3. Make the matrix runner reusable for other multi-model skills.**
- Target: `src/superclaude/cli/eval/` (cliEval harness: `commands.py`, `claude_process.py`, `artifact_layout.py`) or a thin `scripts/` wrapper around the launch block and `extract.py`; first use cases `sc-adversarial-protocol` and `sc-troubleshoot-protocol` Tier 2.
- Change: move combos.json parsing, launch, stream-log served-model extraction and results table into a shared tool.
- Value: medium (repeat use as models change). Effort: high (cliEval is a large harness; I did not read it beyond its module headers, so how well it fits is UNVERIFIED). Risk: scope creep; first prove it on one more skill.

**4. Run the Stage 5 post-execution panel in shadow first.**
- Target: `src/superclaude/cli/reflect/ensemble.py` and `src/superclaude/cli/swarm/lenses/reflect_review.py` (headless post path that reads `T2Model0N`) per brainstorm merged-output.md lines 392, 410.
- Change: reuse `--t2-engine shadow` for UC-2 (SKILL.md:311 says the flag is ignored in post runs until Stage 5).
- Value: medium; Effort: medium; Risk: low if it follows the same side-folder rule. Blocked until Stage 3 and 4 pass, so this is future work.

**Not a good fit:** the `/sc:spec-panel*` family (spec-panel, -ledger, -stoprule, -diffgate, -ponytail) review documents with expert personas, not a model-diverse panel; the matrix could compare their grader models later, but I found no shadow-mode hook there to reuse. Also nothing in sprint, roadmap or tasklist needs a shadow comparison today (no evidence read for them).

## 6. Limits, open questions, UNVERIFIED items

Limits of the evidence:
- n = 3 per combination; the authors say a 1-item gap is not meaningful and that three leads are "not findings" (PLAN.md lines 177-190, FINDINGS.md lines 27-31).
- No quality scoring: no statement can be made about which combination finds more real defects.
- One input package only (a design spec tasklist); the work behind it had already landed, so grounding reads post-implementation code (PLAN.md lines 118-120).
- USD figures are Claude Code's estimate from model names, not billing (FINDINGS.md line 37).
- Calibrated-confidence gaps may reflect the calibrator model (it differs between combos), not the reviewers (FINDINGS.md line 30).
- Parity and lint failures appear in all combos; the reasons per run were not extracted (FINDINGS.md line 38).

Open questions:
- Why did B run about 2.5x faster than A as designed; is it the orchestrator model or load/time of day? "Cause not isolated" (FINDINGS.md line 29).
- Does the orchestrator model drive dispatch fidelity? Hypothesis from PLAN.md line 69; B-E showed 3 of 3 designed dispatch each, A 2 of 3.
- Does the evidence validator drop more citations when Luna reviews (anchor fidelity 91.4% in the earlier study)? Not extracted here: E1 dropped 7 of 92 citations (metrics.json), but no comparison across combos was made.

UNVERIFIED in this document:
- Which models stood behind tier1a and tier3 on the run dates (PLAN.md line 194).
- The `PLAN.md` header still says "designed, NOT run"; I inferred it was later run from FINDINGS.md and the 15 run folders, and did not find the launch logs (`logs/` is not in the tree on origin/master; only run folders, `resolve/`, `frozen/`, `input/`).
- Run timestamps: I did not read the commit's author time of each run; dates for the runs are not stated beyond 2026-11-13 in FINDINGS.md.
- Whether PR #581 should have carried the experiment: its description does not mention it; I did not check review comments.
- The correspondence of `results.md` column "parity" with the contract's recorded `panel_parity`: E1 notes say identity mismatch suspected on all 3 cards while parity is true (panel/notes.md of E1), consistent with the class-only record, but I did not diff every run.
- I did not open `src/superclaude/cli/reflect/panel_lint.py`, `src/superclaude/cli/eval/` internals, or `docs/guides/reflect-cli-tools-guide.md`, so statements about them are by file name only.
- Codegraph was not used (graph:stale).

---
Footer: graph:stale (codegraph index does not cover origin/master; no codegraph tool was called).

# Re-useable Spec-Task Eval Framework: context and specification

Status: proposal (draft 1, 2026-11-10). Tracks the GitHub feature issue of the same title on `IronbellyOrg/IronClaude`.
Origin: issue #346 ("document review loops don't converge") and the A/B experiments run on it, 2026-11 (`.dev/research/346-review-loop-experiments/`).

## 0. Purpose in one page

We built, by hand and over many sessions, an experiment rig that answers one question well: *does this review-loop design (models, steps, components) produce a better final spec per token than the current one?* It works, but every experiment needed a human coordinator to launch each worker step, hand-fix parse failures, recount tokens and rescore results. That makes each new idea cost hours and makes "test every new model and component, forever, in the background" impossible.

This document (a) records the context and what we learned, so nobody repeats the mistakes, and (b) specifies a framework that turns the rig into a repeatable, automated, policy-safe system:

- describe a **design (arm)** as data: steps, model slots, components, prompts;
- run it N times on a **corpus of tasks** with **no human in the loop**, at the maximum safe parallelism;
- measure **tokens by lane**, **dollars**, and **quality against a validated defect ledger**, not only against a noisy audit;
- compare it with a **fresh concurrent baseline** under **pre-registered decision rules**;
- repeat automatically when a **new model, a new component or a new idea** appears, under budget and policy guards, and publish a ranked matrix.

Target outcome: lower tokens per fixed defect, higher and more consistent final-spec quality, discovered continuously instead of by hand.

### Non-goals
- Not a replacement for the real `superclaude eval` suites (CLI behaviour tests); it extends that harness with a new suite kind.
- Not a production review pipeline. It *finds* the best pipeline; adopting it into `/sc:spec-panel` etc. stays a separate, human-approved change.
- Not a general LLM leaderboard. Scope is spec/document-review loops and, later, task-execution loops (`/sc:implement`, `/sc:workflow`) with the same machinery.

---

# PART A: CONTEXT

## A1. What was run (summary)

All on one real spec, S1 (`orca-worker-contract-spec.md`, sha256 `d3cdbe57...25200`, 58 KB), reviewed with the spec-panel review loop (first review, verify, revise, scoped re-reviews, max 3 reviews / 2 fix cycles), then measured by two frozen independent Sonnet audits per final spec.

| Experiment | Idea | Where |
|---|---|---|
| Stage 2 arm 3 | baseline loop (rules file from PR #484) | `p11/` |
| ab1 / ab2 / ab3 | k=3 union + verify; verify gate k=1; final whole-document gate | `p12/` |
| PN1 / PN2 | 4-reviewer panel + merge + typed ledger + adjudicator; mechanical lint pre-pass | `p13/` |
| Haiku strata | same designs on Haiku | `p12/`, `p14/` |
| ab4 | PN2 lint + k=2 first reviews (AC sweep) + cleaned verifier | `p16/ab4/` |
| fresh baseline | same baseline re-run to measure drift | `p16/base-drift/` |
| Jev E1-E5 | external typed-judgment model at five seams | `p15/` (all NO-GO-OFFLINE or BLOCKED) |
| Defect ledger | 44 validated spec defects; all 70 final specs rescored blind | `p17/` |
| ab5 | ab4 + PN1 panel (`panel` arm) and ab4 + full PN1 (`full` arm) | `p18/` |
| ab6 (designed) | ab5 + free tweaks + three Jev hint seams (A1-A3) | `p18/seams/DESIGN-AB6.md` |

Paths are relative to `.dev/research/346-review-loop-experiments/`.

## A2. What we learned (these shape the requirements)

1. **Audits are a poor instrument.** A frozen audit reports about 1.2 blocking findings per spec, while about 17 blocking ledger defects are actually present (it samples roughly 7%). Per-audit sd is about 0.75, so n=6 could not separate any design from the baseline (all p >= 0.38).
2. **A validated defect ledger is a much better instrument.** Rescoring 70 final specs against 44 validated defects (20 blocking) cut relative noise sharply and separated designs: PN1 (p=0.003), ab3 (0.022), ab4 (0.027); ab1 marginal (0.08); ab2 and PN2 no effect. Sonnet and Opus scorers agreed on 96.2% of 264 status judgements.
3. **Nothing converges.** The unchanged loop fixes about 3 of 44 ledger defects; even the best arm leaves half of the blocking ones. Reviewers raise defects; the reviser leaves them.
4. **Baselines drift.** The same baseline design cost 0.53x tokens when re-run weeks later (53.6k vs 100.4k loop tokens). A stored baseline silently biases every cost comparison. Baselines must run concurrently.
5. **Token cost has structure.** PN1's 408k loop tokens split into 106k primary-lane (Sonnet), 291k parallel Tier 2/3 stand-ins, 11k adjudicator. Cost per fixed defect depends on the lane, not the total; the framework must report lanes and dollars.
6. **Instrument bugs corrupt results quietly.** Examples we hit: token matcher failing on pasted prompts (all zeros); verifier finding lists contaminated by reviser advice (6 of 20 verify prompts); blocking-id parsing failures needing hand-set ids (hyphenated `F-01`, `B1`, "Open blocking findings" formats); a results table that copied the wrong token figure into two rows; a harness that printed launches it could not start.
7. **One spec is not a benchmark.** Every result is for S1. Gains may be specific to its defect mix; a corpus and a hold-out are required before any adoption.
8. **Judge choice is an empirical question.** Opus vs Sonnet judges gave the same decision on the Jev debate; the owner wants Opus used only where it is measurably, significantly better.
9. **Multiple comparisons.** "Endless iterations" means many arms against one baseline; without a promotion ladder and false-discovery control, some arm will always look good.

## A3. Pain points that become requirements

| Pain | Requirement |
|---|---|
| Each worker step launched by hand | Fully automatic launcher; resumable; cap-aware (R-ENG-1..6) |
| 20-agent session cap; rejected launches silently lost | Admission control that never prints/starts more than capacity (R-ENG-4) |
| Token counts by hand, wrong rows | Transcript-derived tokens by message id, per step, per model, per lane, reconciled (R-INS-1..5) |
| Parse failures needing hand fixes | Structured outputs (JSON sidecar) + tolerant parser + quarantine queue (R-ENG-7) |
| Stored baseline drift | Concurrent baseline per campaign + drift monitor (R-BAS-1..3) |
| Noisy audit metric | Ledger scoring layer + calibration (R-SCO-1..8) |
| Policy violations (Fable) | Config-time model policy validation (R-POL-1..3) |
| Secrets in artifacts | Key scan gate before commit (R-SEC-1..2) |
| Everything on S1 | Task corpus + hold-out (R-COR-1..4) |

## A4. Inventory of existing assets to reuse (not rewrite)

In this repo today:
- `src/superclaude/cli/eval/`: cliEval harness. YAML suite manifests validated by `suites/suite.schema.json`; per-eval isolated HOME (`isolation.py`); `RunOrchestrator` thread-pool scheduler clamped to 1-15 workers (`orchestrator.py`); 7-step lifecycle (`runner.py`); `ClaudeProcessAdapter` that drives the real `claude` binary and forbids in-process `anthropic` SDK calls (FR-G1, `claude_process.py`); reporters for markdown, yaml, json and JUnit (`reporter.py`, `run_report.py`); exit-code contract, capability gates, retry and disk-budget modules; docs in `docs/eval/`.
- Existing suite `suites/workflow_vs_task_builder.yaml`: a model-slot x reasoning-effort matrix (three generators, fixed Opus judge, frozen rubric, hash-pinned scoring notes, companion script). It is the closest precedent for what this framework generalises; its fixed Opus judge must become a policy-governed choice.
- `src/superclaude/cli/swarm/`: multi-model fan-out with pluggable transports (`openai_compat` via the proxy, `stub` for deterministic CI), lenses, retry/timeout matrix, merge/reduce, `ParallelExecutor`. It is the right seam for non-Claude reviewer slots.
- `src/superclaude/cli/pipeline/` `ClaudeProcess` (signal handling, `--print` command building), `sprint/` isolation layers, `execution/parallel.py`.
- Model tier table `src/superclaude/skills/ccsession-tag/MODEL-TIERS.md` and `ccsession-models.json`; gateway aliases `claude-gw-tier1a|1b|2|3|4[1m]`.
- Scheduled tasks (create/fire/list triggers) for background execution; `/sc:cli-eval` skill for authoring suites.

In the experiment tree (`.dev/research/346-review-loop-experiments/`), to be ported into framework modules (see B17 mapping):
- harness + state machine + launcher: `p16/ab4/{harness,advance}.py`, `p18/ab5/` (panel/full variants, lane accounting, cap-aware launcher);
- frozen audit command/rules with hashes; PN2 lint (`reqlint.py`); cleaned verifier lists (`score_themes.py`);
- token matcher by prompt text/path; step-model resolution; lane map as data;
- ledger pipeline: `p17/collect.py`, `bucket.py`, chunk prompts, reconciler prompt, blind scorer prompt, `aggregate.py`, `core_score.py`, calibration protocol;
- statistics: `final_score.py` (permutation tests), `central/build_matrix.py`;
- Jev adapter and budget/journal contract (`p15/jev`, `p15/plans/SHARED-CONTRACT.md`), `keyscan.py`;
- debate/judge protocol (`p18/debate/`).

## A5. Hard constraints and policies (binding on the framework)

- **Repo targets:** IronClaude fork only (`IronbellyOrg/IronClaude`); never upstream.
- **Models:** Fable / Tier 0 is forbidden in all pipelines. Opus 5.5 (Tier 1a) is the ceiling and used sparingly or not at all; allow Opus in a role only when an eval shows it is significantly better than Sonnet in that role (pre-registered rule, B8).
- **Panel mock vs live:** current runs use Haiku stand-ins for non-primary slots; live maps `claude-gw-tier1b[1m]`=Sonnet 5.5, `tier2`=GPT-6.1 Sol, `tier3`=GPT-6.1 Terra (likely GLM-5.3), `tier4`=GPT-6 Luna. Going live must be a one-map change.
- **No secrets in artifacts;** Jev/API keys are held by the coordinator process only, never by worker agents.
- **Owner decision D6:** a single run is never killed for cost mid-flight; budgets act at admission (campaign/day), not by aborting a run.
- **Parallelism rule:** maximise parallelism whenever there is no risk (cap = hard limit, reserve = small).
- `.claude/` is never staged; `.dev/tasks/` always staged; PRs only via `/sc:pr-submit`.

---

# PART B: SPECIFICATION

## B1. Glossary

- **Task**: a unit under test: a frozen source document (spec, PRD, TDD, plan) plus its frozen audit configuration and, when available, a validated defect ledger.
- **Design / Arm**: a declarative description of a pipeline: ordered steps, which model slot runs each step, which components are on, which prompt/rules files (hash-pinned).
- **Slot**: a named model position (`t1b`, `t2`, `t3`, `t4`, `primary`, `judge`, ...) resolved through an alias map to a concrete model; may be a *stand-in* in mock mode.
- **Run**: one execution of an arm on a task, with its own sandbox and state.
- **Step**: one worker invocation (reviewer, verifier, reviser, adjudicator, audit, scorer, hint seam).
- **Lane**: a token-accounting class: primary, parallel-other-provider (per slot), adjudicator, judge/scorer, audit, hint-seam (Jev).
- **Ledger**: a validated, versioned list of real defects of a task, with severity, quote, `is_fixed_when` test.
- **Experiment**: a pre-registered comparison: arms, task set, n, metrics, decision rules, budget.
- **Campaign**: a set of experiments scheduled together (e.g. "new model X vs current slots").
- **Matrix**: the cross-experiment results table (quality, tokens by lane, dollars, p-values, decisions).

## B2. Architecture

```
            +-----------------+       +------------------+
 triggers   |  Planner/Queue  |------>|   Admission      |  budget, policy, cap, drift gate
 (new model,|  (campaigns,    |       |   control        |
  new comp.,|   ablation gen) |       +---------+--------+
  cron, CLI)+-----------------+                 |
                                                v
 +----------------+   +------------------+  +---------+---------+   +-----------------+
 | Task corpus +  |   | Arm registry     |  | Scheduler / DAG   |-->| Backends        |
 | ledgers        |   | components,      |  | steps, deps,      |   | claude -p child |
 | (versioned)    |   | prompts (hashed) |  | retries, resume   |   | gateway/openai  |
 +--------+-------+   +--------+---------+  +---------+---------+   | stub (CI)       |
          |                    |                      |             +--------+--------+
          v                    v                      v                      |
 +--------+--------------------+----------------------+----------------------+---+
 |  Run store: events.jsonl, state, sandboxes, transcripts, telemetry, artifacts  |
 +--------+---------------------------------------------------------------+------+
          v                                                               v
 +--------+---------+      +-----------------+      +-------------------+--------+
 | Instrumentation  |----->| Scoring layers  |----->| Stats + decision rules      |
 | tokens/lanes/$   |      | L0 mech, L1 aud |      | permutation, FDR, ladders   |
 +------------------+      | L2 ledger, L3   |      +-------------+---------------+
                           +-----------------+                    v
                                                      Matrix, reports, PR comments,
                                                      promotion proposals (human gate)
```

Design principle: **a thin orchestration layer around existing components** (cliEval runner/isolation/reporters, swarm transports, ClaudeProcess), plus new modules for the step DAG, slot policy, lane accounting, ledger scoring, statistics and the queue.

## B3. Declarative formats (all validated by JSON Schema; all hash-pinned)

### B3.1 Task (`tasks/<id>/task.yaml`)
```yaml
id: s1-orca-worker-contract
kind: spec-review            # spec-review | prd-review | plan-review | implement (later)
source: {path: spec.md, sha256: d3cdbe57...}
audit: {command: audit-command.md, rules: audit-rules.md, sha256: {command: ..., rules: ...}, model_slot: audit}
ledger: {path: ledger/v1.json, version: 1, defects: 44, blocking: 20}
fixtures: [inventory/*.md, README.md]
public: false                # private fixtures need explicit consent before any external provider slot
```

### B3.2 Arm (`arms/<id>.yaml`)
```yaml
id: ab5-full
extends: ab4                           # inherit steps/components, override below
components: {lint: reqlint@1.2, ac_sweep: on, clean_verifier: on, ledger: pn1@3, adjudicator: pn1-adj@2}
slots:                                  # mock/live mapping lives in the slot map, not here
  primary: sonnet-5.5
  t1b: tier1b
  t2:  tier2
  t3:  tier3
  t4:  tier4
steps:
  - {id: lint1,  kind: code,    uses: lint}
  - {id: R1.t1b, kind: review,  slot: t1b, prompt: first-review@5, extra: ac_sweep, after: [lint1]}
  - {id: R1.t2,  kind: review,  slot: t2,  prompt: first-review@5, after: [lint1]}
  - {id: R1.t3,  kind: review,  slot: t3,  prompt: first-review@5, after: [lint1]}
  - {id: R1.t4,  kind: review,  slot: t4,  prompt: first-review@5, after: [lint1]}
  - {id: M1,     kind: code,    uses: ledger.merge, after: [R1.*]}
  - {id: ADJ,    kind: judge,   slot: primary, after: [M1]}
  - {id: VF1,    kind: verify,  slot: primary, after: [M1]}
  - {id: V1,     kind: revise,  slot: primary, after: [ADJ, VF1]}
  - {id: R2,     kind: review,  slot: primary, scoped: true, after: [V1]}
  - {id: V2,     kind: revise,  slot: primary, when: "R2.verdict != PASS", after: [R2]}
  - {id: R3,     kind: review,  slot: primary, scoped: true, when: "V2.ran", after: [V2]}
caps: {reviews: 3, fixes: 2}            # structural, enforced by the engine
```

### B3.3 Slot map (`slots/<env>.yaml`): mock vs live
```yaml
env: mock
policy: {forbidden: [fable, tier0], ceiling: opus-5.5, opus_roles_allowed: []}
slots:
  primary: {model: claude-sonnet-5-5}
  tier1b:  {alias: "claude-gw-tier1b[1m]", model: claude-sonnet-5-5}
  tier2:   {alias: "claude-gw-tier2[1m]",  model: claude-haiku-5-5, stand_in: true, live_model: gpt-6.1-sol}
  tier3:   {alias: "claude-gw-tier3[1m]",  model: claude-haiku-5-5, stand_in: true, live_model: "gpt-6.1-terra|glm-5.3"}
  tier4:   {alias: "claude-gw-tier4[1m]",  model: claude-haiku-5-5, stand_in: true, live_model: gpt-6-luna}
```
A `live.yaml` differs only in `model`/`stand_in`. Every run record stores alias, resolved model and `stand_in`.

### B3.4 Experiment (`experiments/<id>.yaml`): pre-registration
```yaml
id: e-2026-11-ab5-vs-ab4
question: "Does the 4-tier panel (ab5) beat ab4 on weighted residual defects per primary-lane token?"
tasks: [s1-orca-worker-contract]       # corpus ids; see B9 for hold-out
arms: [base-fresh, ab4, ab5-panel, ab5-full]
n_per_arm: 6
baseline: base-fresh                    # always concurrent (B9)
metrics:
  primary: weighted_residual           # 3*blocking + 2*medium + minor, from ledger L2
  secondary: [resid_blocking, fixed, introduced, loop_tokens_by_lane, usd, wall_s]
decision:                                 # evaluated mechanically, post hoc, never mid-run
  adopt:  {p_max: 0.05, effect_min: -3.0, lane: primary, tokens_ratio_max: 2.5}
  hold:   {p_max: 0.10}
  drop:   otherwise
budget: {tokens_max: 6.0e6, usd_max: 40}
```

## B4. Execution engine

**R-ENG-1 Backends.** A step runs on exactly one backend, chosen by the slot's resolved model:
- `claude-process` (default for Claude models): a child `claude -p --model <m>` in an isolated HOME/sandbox via `ClaudeProcessAdapter` (honours FR-G1: no in-process SDK). Gives tool access (Read/Grep/Bash in sandbox) so review prompts keep working.
- `gateway` (non-Claude slots): `swarm` `openai_compat` transport through the proxy. These models have no file tools, so the backend runs in **inline-context mode**: the harness inlines the spec (and inventories) into the prompt and writes the reply to the step's output file. A step declares `needs_tools: true|false`; a `needs_tools` step cannot be assigned to a gateway slot (validation error).
- `stub`: deterministic fake for CI and engine tests.
- `agent-session` (compat): the current manual mode (steps launched as Claude Code subagents by a coordinator), kept only to reproduce historical runs.

**R-ENG-2 State machine.** Per run: append-only `events.jsonl` (prepared, launched, finished, ingested, lost, quarantined), derived `state.json`; every transition idempotent; `advance` can be killed and re-run at any time (crash-safe, resumable). Reuse the current ab4/ab5 transitions (R1 panel completion, merge, ADJ/VF in parallel, V, re-review, audits).

**R-ENG-3 DAG scheduling.** Steps declare `after`, `when` and `caps`; the engine computes readiness, evaluates `when` expressions against ingested step results (verdicts, blocking ids), and enforces structural caps (3 reviews, 2 fixes) that cannot be overridden by an arm.

**R-ENG-4 Admission control and capacity.** Global limit `max_agents` (default 20, from config), reserve `R` (default 4) for coordinator/judge agents and exit lag; per-provider concurrency and rate limits; per-run limit. The launcher computes free capacity and starts *only* that many steps; unlaunched ready steps stay queued (never marked launched). Priority: finish in-flight runs before starting new ones; panel siblings start together when capacity allows. Policy: *maximise parallelism whenever there is no risk*, i.e. fill to `max_agents - R`.

**R-ENG-5 Retries and losses.** A step that returns without output is relaunched once; a second failure marks the step lost; loss rules per step kind (a lost panel reviewer degrades the panel, two lost reviewers lose the run; a lost adjudicator is recorded and the run continues; anything else loses the run) are data in the arm. HTTP 5xx follow the swarm retry matrix (one retry); the swarm matrix never retries 4xx or timeouts, so **429 backoff with jitter is new code** in the gateway backend (Part E). Lost runs stay in the denominator (reported, never silently dropped).

**R-ENG-6 Sandboxing.** Every step gets `ws/` (copy of fixtures at the run's current spec), `home/` (private HOME with the exact rules file for that arm), and a prompt file; paths relative to the sandbox. Workers may only write their assigned output file; the engine checks for stray writes after each step and logs them.

**R-ENG-7 Structured outputs and parsing.** Each step kind defines an output contract: markdown report plus a **machine-readable sidecar block** (e.g. fenced JSON with `blocking_ids`, `verdict`, finding records). The parser reads the sidecar first and falls back to tolerant text parsing; anything unparseable goes to a **quarantine queue** (surfaced as `MANUAL` in the CLI and as a notification), never silently coerced. The verifier input builder must cut finding blocks at banners and drop recommendation lines (contamination guard, with a test on real fixtures).

**R-ENG-8 Determinism and reproducibility.** Everything that can change an outcome is hashed into the run manifest: task/source sha, arm yaml, component versions, prompt and rules file hashes, slot map, model ids returned by the backend, framework version, random seeds (panel draws).

## B5. Models, slots and policy

- **R-POL-1** The slot map is validated at config time against a policy file: forbidden models/tiers (Fable, Tier 0), ceiling (Opus 5.5), and `opus_roles_allowed` (empty by default). A violating arm or map fails validation before any run; a test asserts no step can resolve above the ceiling.
- **R-POL-2** Opus unlock by evidence: the framework ships a **judge evaluation experiment** (B7.5). A role (adjudicator, verifier, audit, scorer, debate judge) may be added to `opus_roles_allowed` only by a recorded result meeting the pre-registered significance rule, committed with the evidence link.
- **R-POL-3** Every run records alias, resolved model, `stand_in`, and the live model it stands for, so mock results can be re-interpreted when slots go live. Model-release watch (B10) creates candidate slot maps; it never edits the policy.

## B6. Instrumentation

- **R-INS-1** Tokens from transcripts, **output and input/cache-read/cache-write separately**, each message id counted once (max output per id), attributed to step by prompt-file/prompt-text match (both pasted and short "read the prompt file" launches), and to model by the transcript's own model field. (Input tokens were never measured in the experiments; it is a known gap because parallel readers re-read the spec.)
- **R-INS-2** Lanes are data (`lanes.yaml`): primary, parallel-<slot> (per slot with live model name), adjudicator, judge/scorer, audit, seam-hints. Reports show total, primary-only, primary+adjudicator, and per-lane, each also as a ratio to the concurrent baseline.
- **R-INS-3** Dollars from a price table derived from `MODEL-TIERS.md` (input / cached / output per M), with an explicit "unpriced" flag for subscription or unknown models (never silently zero).
- **R-INS-4** Wall time per step and per run; queue wait separated from execution time.
- **R-INS-5** Reconciliation check: sum of step tokens must equal the sum of all matched transcripts within 1%; unmatched transcripts are listed (the experiment tree had 7 unmatched panel prompts in two runs and a copy-paste error in two table rows; the check makes both visible).

## B7. Scoring

### B7.1 Layers
- **L0 mechanical**: schema/lint/hash/size checks on the final document (cheap, deterministic, always on).
- **L1 frozen audits**: two independent blinded audits (Sonnet unless the judge experiment promotes another) with frozen command/rules and hashes; reports blocking findings per audit. Kept because they are the original instrument and detect *new* defects, but treated as a low-recall sampler (~7%), never as the primary metric.
- **L2 ledger scoring** (primary metric): each final document is scored blind against the task's ledger: per defect FIXED / DELETED_OK / PARTIAL / PRESENT / WORSE / MOOT_BAD with a verbatim-quote evidence line, plus introduced-defect patterns and unvalidated candidates. Residual = PRESENT + PARTIAL + WORSE + MOOT_BAD; weighted by severity (3/2/1).
- **L3 delta tracking**: introduced defects (patterns), fix-by-deletion rate (DELETED_OK, size change), regression vs input.

### B7.2 Blind scoring protocol (R-SCO)
- **R-SCO-1** Scorer input = ledger (arm names stripped), original, revised, diff. Documents are renamed and shuffled; the key is held by the coordinator only.
- **R-SCO-2** Scorer must run any shell/grep/YAML check that a defect depends on in a scratch directory rather than reason about it.
- **R-SCO-3** Calibration: a fixed 10% random subset (min 6) is scored by a second model/scorer each campaign; report exact and fixed-vs-residual agreement; below 90% binary agreement the campaign is flagged and scorer instructions reviewed.
- **R-SCO-4** Test-retest: periodically rescore the same documents with the same scorer to bound scorer noise.
- **R-SCO-5** Scorer is a configurable slot under the policy; default Sonnet.

### B7.3 Ledger lifecycle (R-SCO-6..8)
- The ledger is **versioned**. New defects discovered by any audit, reviewer or scorer-flagged "other new defect" go to a *candidate* pool; a periodic **reconciliation job** clusters candidates (topic bucketing, not single-link: single-link snowballed to a 312-finding cluster), validates them against the source with a validator agent (quote verified with `grep -nF`, shell claims executed), and appends accepted defects as ledger version N+1 with `added_in` and `found_by` provenance.
- Scores always state the ledger version. Old results are rescored when the ledger grows (cheap: scorer runs on stored documents), so history stays comparable.
- **Circularity guard (R-SCO-7):** report each result also on the *core* ledger (defects raised by >= 2 arm families), to show an arm is not being credited for defects only its own reviewers found.
- **Completeness estimate (R-SCO-8):** track the discovery curve (new accepted defects per additional 10 documents) and publish "ledger saturation"; low saturation lowers the weight the matrix gives to ledger-only comparisons.

### B7.4 Task corpus (R-COR)
- **R-COR-1** At least 8 tasks across document kinds and domains (spec, PRD, TDD, tasklist), each with frozen source, audit config and a ledger. The existing `workflow_vs_task_builder` corpus (three provenance-backed cases) seeds it. Tasks enter the library through the ingestion and ledger-factory process in **Part C**.
- **R-COR-2** Seeded-defect variants (known planted flaws) complement natural ledgers; report them separately (seeded detection is not natural incidence).
- **R-COR-3** Split the corpus into **dev** (used for iteration) and **hold-out** (touched only by confirmation runs; results quoted only once per design version).
- **R-COR-4** Every promotion ladder (B8) requires at least two tasks and no regression on any.

### B7.5 Judge evaluation experiment (built-in)
For each judging role, replay *frozen inputs* with candidate judge models and score against ledger truth:
- adjudicator/verifier: items = merged findings from stored runs; truth = does the item map to a ledger defect (labelled by two independent labelers); metric = balanced accuracy and per-item paired comparison (McNemar / permutation);
- audit-as-judge: recall and precision of ledger defects per audit;
- scorer: test-retest and cross-model agreement (done once: Sonnet vs Opus 96.2%);
- debate judge: agreement of picks, factual spot-check failures caught.
Pre-registered unlock rule: allow Opus for a role only if it beats Sonnet by >= 0.10 absolute balanced accuracy (or recall at equal precision) with paired p < 0.05 on >= 60 items, and the Opus tokens in that role are <= 15% of the primary lane. The result record is the only way to edit `opus_roles_allowed`.

## B8. Statistics and decision rules

- **R-STA-1** Per-arm per-metric mean, sd, and a two-sided permutation test (>= 20,000 shuffles) against the *concurrent* baseline; Haiku or other strata compare only within stratum. Also report effect size with a bootstrap interval and the **minimum detectable effect** for the actual n and measured sd (so "inconclusive" is quantified: at n=6 and sd about 2, only effects of about 3 residual-blocking defects are detectable).
- **R-STA-2** Metrics: weighted residual (primary), residual blocking, fixed count, introduced patterns, loop tokens by lane, primary-lane tokens, dollars, marginal fixes per 100k extra primary tokens vs baseline, wall time.
- **R-STA-3 Promotion ladder** (controls false discoveries from endless iteration):
  1. *Screen*: n=3 per arm on dev tasks; advance if weighted residual is at least as good as the baseline with no safety regression; cost-only arms (cheaper, equal quality) use an equivalence margin.
  2. *Confirm*: n=6 on two or more dev tasks with a fresh concurrent baseline; adopt-candidate if p <= 0.05 after Holm correction across all arms confirmed in the campaign.
  3. *Hold-out*: one run set on the hold-out tasks; must replicate the direction; only then is a promotion proposal written.
  4. *Human gate*: promotion into a production command is never automatic.
- **R-STA-4** Disqualifiers (never traded against score): dangerous false pass, suppressed blocker, invalid citation, privacy breach, policy violation, fix-by-deletion above a threshold.
- **R-STA-5** All decision rules are evaluated mechanically from the pre-registered experiment file; changing a rule after data exist creates a new experiment id.
- **R-STA-6** Adaptive allocation (later phase): successive-halving or Thompson-sampling allocation of runs across many arms inside a campaign, with the final confirm stage still on the fixed-n ladder.

## B9. Baselines and drift

- **R-BAS-1** Every experiment includes a concurrent fresh baseline arm on the same tasks; a stored baseline is used only as a comparison *prior* and is labelled stale with its date and model versions.
- **R-BAS-2** Drift monitor: weekly (and on any model release) run the reference baseline n=3 and compare loop tokens, lane split, residual and audit counts with its history; alert if tokens move by more than 25% or residual by more than 1 sd; tag all results since the last clean check.
- **R-BAS-3** Baselines are keyed by `(task, arm, slot map, framework version, rules hashes, model ids returned)`; any change creates a new baseline series.

## B10. Automation and background operation

- **R-AUT-1 Queue.** `superclaude lab enqueue <experiment.yaml>`; a persistent queue (file-backed, atomic) with priorities (drift checks > confirmations > screens), per-campaign budget, and dedupe by experiment hash.
- **R-AUT-2 Daemon/trigger modes.** `lab daemon` (long-running, systemd/tmux-friendly) and `lab tick` (one scheduling pass, suitable for the Claude Code scheduled-task triggers/cron). Both are safe to run concurrently with a lock; both resume interrupted runs.
- **R-AUT-3 Model-release watcher.** A job compares the model catalog (`MODEL-TIERS.md`, gateway model list) with the last seen snapshot; for each new model that passes policy it generates candidate slot maps (swap one slot at a time, then best-pair combinations), enqueues screen experiments against the current best arm, and opens a report (no policy edits, no production changes).
- **R-AUT-4 Component watcher / ablation generator.** When a component registry entry is added or its version changes, enqueue (a) one-at-a-time ablations, (b) pairwise combinations of components that passed screening; cap the combinatorial blow-up with a per-campaign arm limit and the promotion ladder.
- **R-AUT-5 Budgets.** Campaign and daily token/dollar budgets enforced at admission; a run in flight is never killed for cost (D6); an over-budget campaign simply stops admitting runs and reports.
- **R-AUT-6 Notifications.** Digest on completion and on drift/anomaly (quarantine items, lost runs, scorer disagreement, budget exhausted); optional PR comment with the matrix delta.
- **R-AUT-7 Idle-safe.** Background runs use the lowest priority class, back off when the interactive session cap is needed (reserve R), and pause on rate-limit errors.

## B11. Component registry and ablation

Components are versioned, hash-pinned modules with a declared interface so arms compose them:
`lint@v`, `ac_sweep@v`, `clean_verifier@v`, `panel(template,slots)@v`, `ledger(merge,revise)@v`, `adjudicator@v`, `tier_provenance_guard@v` (verifier may not reject findings raised by >= 2 tiers), `revise_brief_rules@v`, `jev_seam(A1|A2|A3|E*)@v` (non-controlling hints), `scorer@v`, `audit@v`. Each has: inputs, outputs, token-lane declaration, cost model, fixtures for its unit tests, and the experiments that justified it.

## B12. Reporting

- **Central matrix** (md + json + optional published page): rows = arm x task x stratum; columns = n, weighted residual, residual blocking, fixed, introduced, p vs baseline (Holm-adjusted), loop tokens (total / primary / parallel / adjudicator), dollars, fixes per 100k primary tokens, ledger version, drift tag, decision.
- **Pareto view**: quality vs primary-lane cost, quality vs dollars, with the frontier and dominated arms.
- **Run report** per run: step timeline, tokens/model per step, anomalies, quarantine items, final-document diff vs input, per-defect statuses.
- **Reproduction bundle**: manifest + hashes + commands to rerun any cell.
- Export JUnit/JSON for CI.

## B13. CLI (proposed as a top-level `superclaude lab` group; see Part E for why it is not an `eval` sub-group)

```
superclaude lab init <campaign>                 scaffold tasks/, arms/, slots/, experiments/
superclaude lab validate                         schemas, hashes, policy (Fable ban, ceiling), DAG, lane map
superclaude lab plan <experiment>                arms x tasks x n, forecast tokens/$ (lanes), min detectable effect
superclaude lab run <experiment> [--env mock|live] [--max-agents N] [--dry-run]
superclaude lab status [<experiment>]            runs, steps, capacity, quarantine (MANUAL) items
superclaude lab fix-ids <run> <step> "<ids>"     explicit manual correction, logged
superclaude lab score <experiment> [--ledger vN] blind ledger scoring, calibration subset
superclaude lab report <experiment> | matrix     tables, Pareto, decisions
superclaude lab ledger candidates|reconcile|add  ledger lifecycle
superclaude lab judge-eval <role>                judge comparison on frozen inputs (B7.5)
superclaude lab baseline check                   drift monitor
superclaude lab enqueue|daemon|tick|watch        automation (B10)
superclaude lab promote <experiment>             writes a promotion proposal; never edits production
```
Exit codes: the cliEval table is a fixed four-value contract (0 ok, 1 failures, 2 usage/blocked, 3 interrupted) pinned by tests, so `lab` keeps those four meanings and adds none; BLOCKED maps onto 2 as the companion script already does, and quarantine/lost counts are reported in the summary, not in new exit codes (Part E, decision E4).

## B14. Storage layout

```
.dev/evals/<campaign>/
  tasks/<task>/{task.yaml, source.md, audit/, ledger/v1.json, fixtures/}
  arms/<arm>.yaml   slots/{mock,live}.yaml   lanes.yaml   components/
  experiments/<id>/{experiment.yaml, manifest.json, runs/<run>/{events.jsonl,state.json,sandboxes/,transcripts/,telemetry/}, scores/, results.json, RESULTS.md}
  matrix/{MATRIX.md, matrix.json}   queue/   drift/   reports/
```
Bulky run directories are not committed (kept as artifacts or compressed archives with a manifest); `results.json`, `RESULTS.md`, ledgers, arms, slots, experiments and matrix are committed.

## B15. Security and privacy

- **R-SEC-1** Key scan (`keyscan`) over every artifact set before commit/publish; fail closed.
- **R-SEC-2** External-provider slots receive only fixtures marked `public: true` unless explicit consent is recorded for the task; no private content to Jev or other third-party services without it.
- **R-SEC-3** Credentials live only in the coordinator environment; worker sandboxes get none; logs are secret-safe.
- **R-SEC-4** Sandboxes: no network for workers unless the step declares it; stray-write detection.

## B16. Testing and acceptance

Unit/engine tests (stub backend, deterministic):
1. State machine: kill/restart at every transition; no duplicate or lost launches; idempotent ingest.
2. Capacity: with `max_agents=N` and any DAG, never more than N-R steps in flight; ready steps beyond capacity stay unlaunched and start later (property test).
3. Policy: Fable and above-ceiling aliases rejected at validate time and at run time.
4. Parser: sidecar parse; tolerant parse on the 18 real reports plus the hyphenated and "B1"-style formats; quarantine on garbage; contamination guard on real verifier inputs.
5. Token accounting: pasted and short launches, wrong-model ignore, max-per-message-id, reconciliation within 1%, unmatched listing.
6. Lanes: lane map is data; changing a slot/stand-in changes only resolved-model and lane labels.
7. Stats: permutation test and Holm correction against known cases; MDE calculation.
8. Scoring: blinding (no arm leakage in scorer prompts), calibration agreement computation, ledger versioning and rescoring.

Golden replays (acceptance of the whole framework):
- G1: replay the stored ab4 and PN1 transcripts through the scorer/stat/matrix path and reproduce the published ledger numbers (ab4 residual blocking 14.3, fixed 6.3; PN1 10.0 and 15.7; fresh baseline 17.3 and 2.8) exactly.
- G2: run the fresh baseline n=3 end to end with the new engine and land within the historical band (loop tokens 53.6k +/- 25%, weighted residual +/- 1 sd).
- G3: run ab5-panel vs ab4 unattended (no manual launches) at `max_agents=16`; zero lost launches; crash-resume test mid-run; token reconciliation passes.
- G4: simulate a new model release (a fake catalog entry): watcher enqueues screens, budget gate stops at the cap, report generated, nothing in production edited.

## B17. Phased plan (each phase ends with its acceptance tests)

| Phase | Scope | Mapping from existing code | Exit criteria |
|---|---|---|---|
| P0 | Schemas for task/arm/slots/experiment; policy validator; port frozen assets (audit command/rules, S1 task with ledger v1) | `p16/ab4/frozen`, `p17/ledger.json`, `MODEL-TIERS.md` | validate passes; Fable-ban test |
| P1 | Engine: events/state, DAG, claude-process backend, capacity-aware launcher, retries, parser + quarantine | `p16/ab4/{harness,advance}.py`, `p18/ab5/advance.py` (AB_AGENT_CAP); library reuse of `pipeline/process.py:ClaudeProcess` and cliEval `HomeIsolation`/scratch/cancellation (Part E) | G3 on stub and real; property tests |
| P2 | Instrumentation: tokens (output+input), lanes, dollars, reconciliation | `tokens_by_prompt*.py`, `p18/ab5` lane map | G2, reconciliation within 1% |
| P3 | Scoring: ledger scorer, blinding, calibration, aggregate, stats, matrix | `p17/score/*`, `final_score.py`, `central/build_matrix.py` | G1 exact reproduction |
| P4 | Automation: queue, `tick`/`daemon`, drift monitor, budgets, notifications | Claude Code scheduled tasks, `p18` monitor loops | G4 |
| P5 | Gateway backend for non-Claude slots (inline-context mode) via swarm transport; live slot map | `cli/swarm/transports`, `workflow_vs_task_builder` slots | a live panel with tier2/3/4 models completes a run; privacy gates enforced |
| P6 | Corpus growth, ledger lifecycle automation, hold-out discipline | `p17/collect.py`, bucket + reconcile prompts, `workflow_vs_task_builder` corpus | 8 tasks with ledgers; saturation report |
| P7 | Component registry, ablation generator, release watcher, adaptive allocation, judge-eval experiment | `p18/debate`, `p18/seams`, judge-eval design | unattended campaign promotes or drops arms with Holm control |

Rough effort: P0-P3 about 4-6 working sessions of focused implementation (mostly porting and consolidating tested code); P4-P7 incremental.

## B18. Risks

| Risk | Mitigation |
|---|---|
| Non-Claude models cannot use file tools; review prompts assume tools | inline-context mode, `needs_tools` validation, per-step backend choice; test with the stub first |
| Ledger-derived metric overfits S1 or the arms that built the ledger | corpus + hold-out, core-ledger view, discovery-curve saturation, periodic reconcile |
| Scorer bias (same model family as workers) | calibration against a second family, test-retest, judge-eval experiment |
| Endless iteration produces false winners | promotion ladder, Holm correction, hold-out, human gate |
| Cost of continuous background runs | budgets at admission, lane-aware forecasts, cheap screens (n=3), drift checks only weekly |
| Stand-in results do not transfer to live models | record `stand_in`, rerun key cells with live slots in P5, publish the transfer gap |
| Harness bugs corrupt results quietly | reconciliation checks, golden replays, quarantine, run manifest hashes |
| Session/agent caps and rate limits | admission control, reserve, backoff, per-provider limits |
| Policy drift (someone adds Fable/Opus) | policy validator on every config, recorded unlock evidence only |

## B19. Open questions

1. Command surface: resolved by Part E: a new top-level `superclaude lab` package that imports cliEval utilities as libraries (a sub-group would inherit the 15-worker clamp, the closed schemas, the id regex and the four-value exit table).
2. Where does the ledger live and who may add to it: repo-committed, human-approved merges only, or automatic with a review queue?
3. Which backend carries live non-Anthropic slots first: **partly resolved.** Evidence from the issue #392 live run (2026-11-09, Coder workspace; `.dev/issues/392/e2e/live-final-tier-summary.json` and `live-final-proxy.log`): `claude --bare -p ... --model claude-gw-tier2` returned code 0, the shim logged `TIER tier2: T2Model01 -> gpt-6.1-sol` on `/v1/messages` (Anthropic protocol), and the answering model was `gpt-6.1-sol`. So the `claude`-binary route through the gateway works for tier2 and keeps tools and transcript accounting; the swarm `openai_compat` transport remains the option for steps without tools. Not yet confirmed: tier3 (Terra or GLM-5.3), tier4 (Luna), tier1b. The mapping is Coder-environment configuration (`T2Model01`) and can change, so every run must record the answering model from the transcript or proxy log, never trust the alias. The same command returns 404 in environments without the tier gateway (checked in the sandbox used for these experiments).
4. Do task-execution loops (`/sc:implement`, `/sc:workflow`) join in P7 or get their own phase with a code-quality scorer (tests pass, spec adherence)?
5. Dollar accounting for subscription models (Muse): report as unpriced, or assign an internal shadow price?
6. Background operation host: the Claude Code scheduled tasks, a dedicated machine, or CI; and how much of the 20-agent session cap may be used by background work?
7. Publication of results: matrix as repo files only, or also a published page; privacy rules for private specs.
8. Should the Jev seams (A1-A3, E1-E5) be components in the registry from day one, or wait for the offline gates to pass?

## Appendix A. Metric definitions

- `resid_blocking` = count of blocking ledger defects with status in {PRESENT, PARTIAL, WORSE, MOOT_BAD}.
- `weighted_residual` = 3*blocking + 2*medium + 1*minor residual.
- `fixed` = count of {FIXED, DELETED_OK}.
- `introduced` = count of introduced-defect patterns present.
- `fixes_per_100k` = 100000 * (fixed - fixed_baseline) / (primary_tokens - primary_tokens_baseline).
- Lane totals use output tokens (and input/cache once measured), each message id once.

## Appendix B. Reference results the framework must reproduce (ledger v1, S1, n=6 Sonnet)

| Arm | Residual blocking /20 | Fixed /44 | p vs fresh baseline | Loop tokens |
|---|---|---|---|---|
| fresh baseline | 17.3 | 2.8 | - | 53.6k |
| ab1 | 14.3 | 6.0 | 0.08 | 122k |
| ab2 | 17.5 | 2.7 | 0.95 | ~74k |
| ab3 | 13.8 | 6.8 | 0.022 | ~123k |
| ab4 | 14.3 | 6.3 | 0.027 | 106.5k |
| PN1 | 10.0 | 15.7 | 0.003 | ~408k (106k primary / 291k parallel / 11k adjudicator; ADJ was Fable, now forbidden) |
| PN2 | 18.5 | 1.5 | 0.23 | 47k |

## Appendix C. Mapping: current experiment code to framework modules

| Current | Becomes |
|---|---|
| `harness.py` build/prep/ingest | `lab.engine.sandbox`, `lab.engine.steps.*` |
| `advance.py` + `drive.sh` + manual agent launches | `lab.engine.scheduler` + backends (`claude-process`, `gateway`, `stub`) |
| `decision.json` | `experiment.yaml` decision block + `policy.yaml` |
| `rules.json`, frozen files | `components/` registry + hash pins |
| `tokens_*.py`, `tokens_models.py` | `lab.instrument.tokens`, `lab.instrument.lanes` |
| `reqlint.py` | component `lint` |
| `score_themes.py` finding blocks | `lab.parse.findings` (+ contamination guard) |
| `p17/collect.py`, `bucket.py`, chunk/recon prompts | `lab.ledger.{collect,cluster,reconcile}` |
| `p17/score/*`, `aggregate.py`, `core_score.py` | `lab.score.ledger`, `lab.stats` |
| `central/build_matrix.py` | `lab.report.matrix` |
| `keyscan.py` | `lab.security.keyscan` |
| `p15/jev` adapter | `lab.components.jev_seams` (non-controlling) |
| `p18/debate/` protocol | `lab.judge.debate` (optional) |

---

# PART C: SPEC LIBRARY AND LEDGER FACTORY (added 2026-11-10 at the owner's request)

Goal: a library of specs ("tasks") to choose from, each with a complete, validated defect ledger, so any design can be evaluated on any spec with a low-noise metric. Building a ledger is itself a repeatable pipeline; this part records exactly what we did for S1 (44 defects from 70 runs) so it can be rerun unchanged for every new spec.

## C1. Library model

- `library/<spec-id>/` = the Task of B3.1: frozen source (+ sha256), kind, domain, size, provenance (who wrote it, from which template, which generator), frozen audit config, fixtures, ledger versions, ingestion record, status.
- Status ladder: `ingested` -> `seeding` (runs in progress) -> `ledger-draft` -> `ledger-validated` (saturation criterion met, C4) -> `active`. Only `active` specs are used in confirm/hold-out experiments (R-COR-3).
- Catalogue index (`library/index.json`): per spec, kind, size, ledger version, defect counts by severity, saturation estimate, dev vs hold-out flag, template id (Part D), and defect density (defects per KB), so experiments can pick tasks by property ("long specs", "TDDs", "low-defect-density").
- Selection API: `lab library list|show|pick --kind spec --min-defects 20 --split dev`, and experiments reference task ids or selectors.

## C2. Ingestion (R-LIB-1..4)

1. `lab library ingest <path|url|generator-run>`: copies the document, computes sha256, records provenance and template id, detects kind, strips nothing.
2. Fixture discovery: referenced inventories/evidence files are copied with hashes; unresolved references are listed (the S1 reviewers could verify only what was in the sandbox; unverifiable citations must be consistently handled).
3. Privacy classification: `public` vs `private` (private tasks may not use external-provider slots without recorded consent, R-SEC-2).
4. Freeze the audit configuration for the spec (command + rules hashes) and a preflight check: the document parses, the stated line references resolve, size within backend limits (inline-context mode needs the full text to fit).

## C3. The ledger factory (exactly what we did for S1, now a pipeline)

Stage 0, **seed runs**. Run the spec through 20-30 runs (C4 gives the stopping rule). Use a **diverse set of arms**, not 30 copies of one: for example baseline, k=2/k=3 union, lint+k=2, panel, full panel+ledger, one cheap-model stratum. Diversity matters because defects surfaced by only one design are the long tail (in S1, 14 of 44 defects were raised by a single arm family). Each run executes the normal loop plus the two frozen audits; all first-review and audit reports are retained.

Stage 1, **collect** (`collect.py`). Parse every blocking finding from every first review and every audit into one record each: `{gid, kind (first|audit), arm, run, step, finding id, heading, body, cited lines, theme}`. S1: 511 blocking findings (326 first-review, 185 audit) from 13 arms and 140 audits.

Stage 2, **bucket and chunk** (`bucket.py`, chunker). Do NOT use single-link clustering on text similarity: it snowballed 312 findings into one cluster. Bucket by topic (spec section / requirement family) using the cited-line sets and the theme tag, then split buckets into chunks of at most 30 findings (S1: 20 chunks). Keep a small `misc` bucket merged into the nearest chunk.

Stage 3, **parallel validation** (one agent per chunk, all at once). Each validator receives the original spec, the evidence/inventory files, its chunk, and a fixed prompt (`prompt-template.md`) and must: group its findings into defects; for every defect, verify the quoted text with `grep -nF` against the original; actually **execute** any shell/grep/YAML claim in a scratch directory instead of reasoning about it; classify `original | introduced | not-a-defect | unverifiable`; assign severity (blocking = the spec cannot be implemented or cannot pass its own acceptance checks, or permits an unsafe outcome; medium; minor); write `is_fixed_when` (a concrete test a reader can apply to a revised spec) and say whether deleting the obligation consistently is an acceptable fix (`deletion_ok`); assign every finding id to exactly one defect (a script checks the assignment is total and exclusive); and list anything noticed that no finding raised (`extra_noticed`). Model assignment per chunk by severity and complexity: strong model for core-semantics and safety chunks, a cheaper model for mechanical per-row chunks. Under the current policy: Sonnet by default, Opus only for roles where a judge-eval has unlocked it (B7.5).

Stage 4, **reconcile** (one agent, `recon-prompt.md`). Merge duplicates across chunks (the same defect shows up under different wording in several chunks: S1 had 125 entries reducing to 44), split compound defects so each can be answered independently, set severity conservatively, separate **introduced-defect patterns** (flaws that a revision can add; 7 for S1), list rejected and unverifiable entries with reasons, and add **new candidates** the reconciler noticed (5 for S1, kept separate until validated). A script verifies that every input id appears exactly once in the output.

Stage 5, **blind scoring and calibration** (B7.2). Every final document of the seed runs is scored against the new ledger (statuses and evidence); a 10% subset is scored by a second model; agreement is reported. This both validates the ledger (do the `is_fixed_when` tests discriminate? are there defects scored PRESENT everywhere or FIXED everywhere?) and produces the first baseline numbers for the new spec.

Stage 6, **freeze** the ledger as `v1` with its hash, record found-by provenance per defect (which arms raised it), and publish the catalogue entry. Later discoveries append `v2`, `v3` (B7.3); old scores are rescored cheaply.

Cost reference (S1): collection and bucketing are code; stage 3 was 20 validator agents (about 150k tokens each, mostly input); stage 4 one agent (about 190k tokens); stage 5 was one scorer per final document (about 140k tokens each). The seed runs themselves dominate: the 70 runs here cost on the order of 6-8M output tokens in total. A new spec costs the same order again; the library therefore treats ledger-building as an investment amortised over every later experiment on that spec.

## C4. How many runs are enough (completeness criterion, R-LIB-5..8)

Evidence from S1 (70 runs, 44 defects, 20 blocking; random run orderings, 300 shuffles):

| Runs sampled | Distinct ledger defects found | of 44 | Blocking found | of 20 |
|---|---|---|---|---|
| 5 | 18.7 | 43% | 14.7 | 73% |
| 10 | 24.5 | 56% | 17.1 | 86% |
| 20 | 30.4 | 69% | 18.9 | 95% |
| 30 | 33.9 | 77% | 19.5 | 98% |
| 40 | 36.9 | 84% | | |
| 60 | 41.4 | 94% | 20.0 | 100% |
| 70 | 43.0 | 98% | 20.0 | 100% |

Reading: the **blocking** defects (what matters for the metric) saturate by about 20-30 runs; the **medium/minor tail** needs 60-70 runs and still has an estimated unseen remainder (Chao2 about 10 more, mostly low severity; Good-Turing coverage by incidence 0.98). These runs mixed 13 designs, which speeds discovery; thirty runs of a single design would saturate more slowly.

Stopping rules (all computed automatically after each batch of 5 runs):
1. **Blocking saturation:** no new accepted blocking defect in the last 10 runs, and Chao2 unseen-blocking estimate < 1.
2. **Coverage:** Good-Turing coverage of the full ledger >= 0.95.
3. **Diversity floor:** at least 5 distinct arm families contributed, and no single family is the sole source of more than 25% of defects (circularity guard, R-SCO-7).
4. **Minimum and maximum:** at least 20 runs; hard stop at 40 (report "ledger-draft, incomplete tail" instead of spending more; the tail keeps growing via the lifecycle of B7.3).
The catalogue records which criteria were met; downstream experiments weight a spec's ledger-based comparisons by its saturation (low saturation widens the reported uncertainty).

## C5. Library growth policy

- Start with S1 plus the three `workflow_vs_task_builder` corpus cases (PRD local-file delivery, detection-contract setup, reflect integration), then ingest repo specs/PRDs/TDDs from `.dev/` and real work products as they appear.
- Balance by kind and size; keep a hold-out set that is never used for design iteration (R-COR-3).
- Retire a spec from `active` when its ledger saturates at "all designs fix everything" (no discrimination) or "no design fixes anything" (floor); keep it for regression.
- Ingestion can be automatic (watch a directory or a PR label) but ledger acceptance of new defects stays gated by the validator agents and, for blocking additions, a human review queue (open question B19.2).

---

# PART D: SPEC-TEMPLATE EXPERIMENTS (added 2026-11-10)

Objective: use the library to experiment with **spec templates**, iterating on the *spec itself* and measuring what that does to the review loop. Until now the document was a constant and the loop was the variable; here the document-producing process becomes a variable too, because a better template should yield specs with fewer, cheaper-to-fix defects, which is a larger lever than tuning the reviewer.

## D1. Design

- **Independent variable:** template (and generator model/effort). A template is a versioned scaffold (sections, required tables, acceptance-criteria format, phase/gate structure, traceability conventions) such as the repo's PRD/TDD/spec templates (`src/superclaude/templates/`, `/sc:tdd`, `/sc:workflow`, the `prd`/`tdd`/`tech-reference` skills) or a new candidate.
- **Source parity:** a fixed *source brief* (the intent, constraints, decisions, evidence) is rendered by each template, so the same requirements appear in every variant. Variants are generated by a fixed generator slot (policy-compliant model, fixed effort), n generations per template to capture generator variance.
- Each generated spec is ingested (Part C), seeded, and gets its own ledger, because defects are properties of the text.

## D2. Measurements (per template, aggregated over generations and source briefs)

- **Spec quality at birth:** ledger defect count and density (per KB), blocking share, defect classes (scope mismatch, unverifiable acceptance check, path/contract ambiguity, missing owner, contradictory sections), and the share caught by L0 mechanical checks.
- **Loop behaviour on the standard arms** (baseline + current best, concurrent): reviews needed, fixes needed, convergence (blocking residual after the loop), tokens by lane, dollars, first-review raise rate, reviser fix rate (fixed/raised), fix-by-deletion rate, introduced defects.
- **Review economics:** primary-lane tokens per fixed defect and per KB of spec; cost to reach "no blocking defects" where reachable.
- **Downstream proxy** (later): the same spec fed to `/sc:workflow` or `/sc:implement` and scored for task-plan quality, as in the existing `workflow_vs_task_builder` suite, to check that a lower-defect spec yields a better plan.

## D3. Analysis and decision rules

- Unit of analysis is the generated spec (not the run): template effects are estimated with a mixed model or a permutation test that resamples whole specs, with source brief as a blocking factor, so loop-run noise is not mistaken for template signal.
- Primary metric: weighted residual defects after the standard loop; co-primary: defect density at birth. A template is promoted if it lowers one without raising the other, p <= 0.05 with Holm correction across templates in the campaign, replicated on a hold-out source brief.
- Interaction check: re-run the best two loop designs on the best and worst templates to see whether the loop ranking changes with the template (a design that wins only on weak specs is not robust).

## D4. Iteration loop (automatable, B10)

1. Pick a template and a source brief; generate n specs; ingest; seed with a short diverse batch (10 runs) for a *screening ledger*; score defect density and loop residual.
2. Feed the ledger's defect classes back as **template edits** (for example "scope tables must list the exact commands per phase", "every acceptance check must state its pass condition and the command that exercises it", "contract paths must be defined for file-valued outputs"): each is a ledger-derived constraint; the template-editing step may be an LLM under the policy's model ceiling, but every edit is a new versioned template and a new campaign arm, never an in-place change.
3. Re-generate from the same source brief, re-measure; keep edits that reduce defect density or loop residual; drop the rest. The ledger-to-template mapping (which defect class is cured by which template rule) is stored, so templates accumulate evidence.
4. Promotion to the production templates in `src/superclaude/templates/` goes through the normal human-approved change process, with the experiment record attached.

## D5. Risks specific to template work

- Overfitting a template to one source brief: use at least three briefs, one held out.
- Template changes that reduce defects by removing detail (shorter specs): report size-normalised density and check completeness against the source brief's requirement list (a requirement-coverage check, as in R-008/R-019 of the Jev ROI study).
- Generator drift across model versions: pin the generator model per campaign and re-baseline on model release (B9).
- Ledger circularity: template edits are derived from ledger classes; evaluate on specs and briefs the edits were not derived from.

---

# PART E: PORT ASSESSMENT AND DECISION (added 2026-11-10)

Question: how much of what we built can be ported onto the existing `superclaude eval` harness, is there another harness in the project, and which is the better port target? Two independent code reviews were made (reports kept with the experiment record: `assess-cliEval.md`, `assess-other-harnesses.md`); every claim below was checked against the code by the reviewers with file:line citations.

## E1. Harnesses found

| Harness | What it is | Fit as host |
|---|---|---|
| `superclaude eval` / cliEval (`src/superclaude/cli/eval/`) | Flat, one-shot, pass/fail CLI-behaviour harness: YAML suites, per-eval isolated HOME, thread-pool orchestrator, markdown/JSON/YAML/JUnit reporters | Provides plumbing, not the framework's core. **Its production executor is a null stub** (`commands.py:1357-1404`; `suites/README.md` says "null lifecycle executor and unwired assertions"); `ClaudeProcessAdapter` is never constructed outside tests |
| `scripts/eval_workflow_vs_task_builder.py` (companion, 2.5k lines, 64 tests) | The one real live model x effort matrix: `RestrictedProcess(ClaudeProcess)`, loopback `IngressRecorder`, soft `Budget`, hash-pinned `config_gate`, frozen rubric, blind judge packet, quote-verified scoring | Best template for hardened live runs and blind judging; serial, no resume, no token breakdown |
| `src/superclaude/cli/swarm/` (16k lines, ~1,800 tests) | One prompt fanned to N models over an OpenAI-compatible proxy; `StubTransport` for CI; retry policy; resume | Good **transport library**, poor orchestrator: single-wave, no DAG, usage dropped, 5xx-only retry, guard tests ban scoring/judging code inside swarm |
| `pipeline/process.py:ClaudeProcess`, `pipeline/executor.py`, `cli/sprint/` | The production `claude --print` child manager; static step lists; sprint has a topological wave scheduler (`scheduler.py`) and a fake-claude test shim | `ClaudeProcess` is the right process layer; sprint scheduler and fake claude are patterns only |
| `scripts/eval_runner.py`, `eval_1/2/3.py`, `ab_test_workflows.py`, `.dev/eval-workspaces/*`, `recommend/eval_*` | Roadmap regression checks, a t-test script with no tests, copy-pasted per-skill graders | Not reusable; `ab_test_workflows.py` should be replaced (Student t-test, no multiple-comparison correction) |

No other model-trial harness exists. The repo has no permutation test, Holm correction or minimum-detectable-effect code (`scipy>=1.10` is already a dependency).

## E2. How much exists already (rough, by module and effort)

| Source | Share of the framework | Notes |
|---|---|---|
| cliEval library parts (isolation, scratch root, cancellation, disk budget, reporters, loader pattern) | about 15-20% by module, 10-12% by effort | cheap plumbing; the expensive parts (DAG engine with resume, parser/quarantine, token+lane reconciliation, ledger and blind scoring, statistics, queue, watcher) are all new |
| `ClaudeProcess`, swarm transports and retry, companion hardening (RestrictedProcess, Budget, config_gate, judge packet) | about 15% | consumed as libraries or extracted into shared modules |
| The experiment tree (`ab4`/`ab5` harness and state machine, token matcher, lane map, ledger pipeline, scorer prompts, aggregate/stat code, matrix builder, keyscan, Jev adapter) | about 35-40% | working, exercised code, but written as scripts; porting means restructuring and adding tests, not new design |
| New code | about 25-30% | DAG scheduler with admission control and reserve, event-sourced state, quarantine queue, policy validator, queue/daemon/watcher, permutation/Holm/MDE library, gateway usage capture and 429 backoff |
So the plan's earlier "P0-P3 are mostly porting" holds only for porting **from the experiment tree**, not from cliEval. These percentages are judgments from the module-by-module tables, not measurements.

## E3. Constraints that make cliEval a poor host (verified)

- FR-G1 and ruff ban `anthropic` imports (`pyproject.toml:203-206`): all Claude steps are child `claude` processes; the gateway backend must use raw HTTP or a swarm transport.
- Thread pool clamped to 1-15 (`orchestrator.py:143-145`), and `summary.schema.json` caps `parallel` at 15; the 20-agent target with a reserve does not fit.
- Exit codes are a fixed four-value table pinned by tests (`exit_codes.py:21-24`).
- `suite.schema.json` and `evalOutcome` are closed (`additionalProperties:false`): no `steps`, `slots`, lanes; eval ids must match `^[A-Z][A-Za-z0-9]*([0-9]+(\.[0-9]+)?)?$`, so ids like `ab5-full.R1.t1b` fail.
- `ClaudeProcessAdapter.spawn` does a process-wide `os.chdir` (`claude_process.py:338-342`), unsafe under threads.
- Each eval gets a fresh HOME with no OAuth login; only env credentials work.
- Run output allowlist is `/tmp/eval-runs` and `.dev/eval-runs`; summary is written once at the end (a crash loses it); no resume.
- Linux only.

## E4. Decision

1. **Do not make cliEval the host.** Build a new package `src/superclaude/cli/lab/` with its own click group `superclaude lab` (not `eval lab`), its own schemas (`lab/*.schema.json`), run store and exit-code mapping onto the existing four values. This avoids the clamp, the closed schemas, the id regex and the pinned exit-code tests.
2. **Reuse cliEval as a library, not a framework:** import `HomeIsolation`, `containment_guard`, `resolve_scratch_root`, `CancellationToken`, `DiskBudgetPoller` and the `Reporter` renderers; do not fork them. Use `ClaudeProcess(cwd=...)` directly instead of `ClaudeProcessAdapter` (thread safety).
3. **Process layer:** `pipeline/process.py:ClaudeProcess`, with `RestrictedProcess` hardening (stdin-timeout fix, reviewer profile without `--dangerously-skip-permissions`, loopback ingress recording, hash-pinned config gate) extracted from the companion into a shared module so the companion and lab both use it.
4. **Gateway backend for non-Claude slots:** a `lab.backends.gateway` module that imports `OpenAICompatTransport`, `StubTransport` and `retry_policy` from swarm as a library (precedent: `reflect/ensemble.py`), adds usage capture (an additive `usage` field on `WorkerResult`) and 429 backoff, and keeps all stand-in, judge and scoring logic **outside** swarm (its guard tests forbid it). Probe whether `claude --model claude-gw-tier2` against the gateway is a better route (keeps tools and transcript accounting) before committing (B19.3).
5. **Register lab with cliEval minimally:** one thin cliEval suite (`lab_selftest.yaml`) so `superclaude eval list` shows lab and a CI smoke run exists; real lab runs never go through the null executor. Fail closed if the executor is the null stub.
6. **Statistics and matrix are new** modules in `lab/` (SciPy-based permutation tests, Holm, MDE); retire `scripts/ab_test_workflows.py` by replacement.
7. **Port the experiment tree in this order** (maximises reuse of tested logic): token matcher and lane map; parsers with contamination guard; ledger scorer/aggregate/stat code with the G1 golden replay; state machine with the cap-aware launcher; component library.

## E5. What this changes in the plan above

- P1 builds on `ClaudeProcess` and extracted companion hardening, not on `RunOrchestrator`; the DAG scheduler references `sprint/scheduler.py` for topological waves but is new code.
- P5 (gateway) starts with the swarm transport library plus the new usage field and 429 backoff, after the endpoint probe.
- Acceptance G3 (16 agents) is only achievable in the new engine; cliEval's clamp never applies.
- The effort estimate stays "P0-P3 about 4-6 focused sessions" only if the experiment tree is the porting source; building on cliEval would be slower, not faster.

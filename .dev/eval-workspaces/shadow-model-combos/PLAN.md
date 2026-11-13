# Shadow-run model combinations: experiment plan (designed, NOT run)

Date: 2026-11-13. Status: design only. No /sc:reflect run and no model call was made for this plan.
Companion: `combos.json` (machine-readable). Evidence: `resolve/` (panel resolutions), `input/` (frozen plan input).

## 1. What the earlier model study shows (Step 1)

Method: `/sc:analyze` was invoked (Skill tool). Commit b4db265a8 is only on `ironbelly/eval-tasklist-review-panel`, so
files were read with `git show b4db265a8:<path>`. Codegraph: index_state=fresh, checked_at=2026-11-13T01:41:55Z;
degraded: none (unused: the target is documents). Sources: COMBO-REPORT.md "FINAL RESULTS AND DECISION (2026-11-13)"
(supersedes earlier tables), PILOT-REPORT.md, analysis/audits/audit-A/summary.md, probe/probe.json, tools/run-reviewer.sh.

What was tested: ONLY the reviewer role. Task = `/sc:spec-panel --mode critique` of `/sc:workflow` tasklists, one
fresh `claude -p --model <raw id>` per reviewer, merged by the deterministic CLI `superclaude review merge`, scored
by blind Opus judges against ground truth (GT = defects that hurt real implement runs). 3 packages (designSpec
10 GT / 5 blocking, makeTheAliasOnly 4 / 3, design = control 2 / 0); 71 valid rows, 213 row-packages.

| Role | Best (replicated, 4+ runs) | Worst | Cost / latency (3 packages) |
|---|---|---|---|
| Reviewer panel | haiku + 2x luna: 2.2/14 found, 1.2/8 real blocking (best), 3.0 wrong blockers | ember + terra 0.5/14 (terra returns empty); 2x ember + 2x luna 4.75 wrong blockers | 191k tok, ~12 min |
| | ember + 2x luna (study default): 1.83/14, 0.17 real blocking, 1.83 wrong | any 5-reviewer panel: no gain at 2-4x cost | 64k tok, ~6 min |
| | ember + sonnet (precision): 2.5/14, 0.25 wrong blockers, 0.25 real blocking | terra or sol alone; glm (largest spend, retries) | 143k tok, ~13 min |
| | ember + luna (cost): 2.25/14, 0.5 real blocking, 0/2 control found | Qwen3.8-max: disqualified (3/3 timeouts) | 52k tok, ~5 min |
| Single reviewer | sonnet alone (pilot arm A): 2/16, 93k tok, more catches per token than 3-6 model panels | | |
| Calibrator, debate/merge, orchestrator | NOT tested. Merge was deterministic (it silently dropped anchors >200 chars: 49 blocking findings lost, mostly luna/ember/wonder); Opus judge = scoring instrument (re-judge 12/12, audit E) | | |

Per-model facts that matter here: sonnet opened source.md in 62/63 runs, ember skipped it in 39%, luna 22%, haiku 15/75;
luna has the weakest verbatim anchors (91.4% vs 98-100%); terra/sol often refuse or return incomplete reviews.

Evidence quality: blind scoring (anonymized reports, random labels) and six independent audits (identity, validity,
inputs/timing, merge, scoring, aggregation): no fabricated scores, 2 misrouted runs found and excluded. But only 3
effects survive permutation tests (second luna +0.83 control found; 2x ember + 2x luna more wrong blockers; ember +
terra worse). 1/1/1 rows are anecdotes. Confounders the study names: merge drops, source.md not opened (cause
inferred, UNVERIFIED), terra refusals, GT bias (novel real blockers score as wrong), one judge per package.

What it did NOT establish (its own words): no panel lifts the ceiling past ~2.5/14 (GT1, GT2, GT10, alias GT4 never
caught); single-run high scores are unconfirmed; nothing about calibrator, debate judge or orchestrator models; nothing
about `/sc:reflect` (different brief, debate merge, read-only agents). Transfer to reflect is a hypothesis.

## 2. How reflect runs choose models today (Step 2)

Sources: SKILL.md 3.4, 4.0 step 0.5, 4.3a, 7.1, 11.3; panel.py, panel_cmd.py, data/*.json; agent frontmatter; `/tmp/shadow-logs/` (launch.sh, run01-11.log); shadow cards and contracts; gateway `GET /v1/models` (no inference).

| Role | Who picks the model | Controllable from outside? |
|---|---|---|
| Orchestrator (T1 card, rubric, inline debate + judge, report) | session model | YES: `claude -p --model <id>`. Pilot launch.sh passed none, so `~/.claude/settings.json` `model: claude-gw-tier3[1m]` ran (logs: `sdk=tier3` in 9/11 runs) |
| Reviewer 1 analyzer / 2 qa / 3 refactorer | orchestrator passes class sonnet / haiku / opus on the Agent call | PARTLY: env `ANTHROPIC_DEFAULT_SONNET_MODEL` / `_HAIKU_` / `_OPUS_` decide the model per class; if the orchestrator omits the class, `reflect-reviewer` frontmatter `model: sonnet` wins |
| Calibrator (`confidence-calibrator`) | frontmatter `model: sonnet`; orchestrator may pass opus (11.3 disjoint rule) | ONLY via the SONNET / OPUS env values; which of the two is used is the orchestrator's choice |
| Evidence validator | frontmatter `model: sonnet` | via `ANTHROPIC_DEFAULT_SONNET_MODEL` (coupled to reviewer 1) |
| Agents with no `model:` (requirements-analyst, root-cause-analyst, debate advocates, merge-executor) | inherit the parent model unless overridden (Claude Code doc) | via `--model`; exact advocate model UNVERIFIED |
| Panel resolution (shadow record only) | `review panel resolve` with the tier file | `SUPERCLAUDE_REVIEW_TIERS` / `--tiers` change only `panel/resolution.json` and card headers, never dispatch |
| Reviewer count | step 0.5 counts DISTINCT alias values: 3 -> 3 reviewers, 2 -> 2 | YES, indirectly through the env values |

Confirmed by commands (outputs in `resolve/`): under every combo env the resolution is identical (sonnet-5-5 /
haiku-5-5 / opus-5-5, launch sonnet/haiku/opus; tiers sha a35908fa6d40 and template sha d8156ae38041 = shadow03). The
shadow step passes `--env anthropic-only` explicitly, so `SUPERCLAUDE_REVIEW_ENV` / `T3Model01` are ignored; `--env
gateway` is refused (launch None). So `panel_parity`, card `model:` headers and the contract's `reviewer_models` record
the CLASS rotation, not the served model: they say "claude-haiku-5-5" even when GPT 6.1 Sol served the haiku class.
Truth must come from the run transcript (section 4).

What the pilot actually ran (current shell env = shadow03 env): SONNET=`claude-gw-tier1b[1m]` (Sonnet 5.5 per the
2026-11-11 probe), HAIKU=`claude-gw-tier2[1m]` (GPT 6.1 Sol per probe; reviewer 2 self-reports "GPT-5.2/5.4" in
shadow02/04/06/11), OPUS=`claude-gw-tier1a[1m]` (gateway list: "Opus 5.5, Sonnet 5.5"; served model UNVERIFIED),
orchestrator=`claude-gw-tier3[1m]` (GLM 5.3 per probe, current serving UNVERIFIED).

Dispatch collapse (largest confounder found): in 6 of 9 tier3-orchestrated runs (03, 05, 07, 08, 09, 10) the logs show
only the tier1b model for reviewers and every card that carries a self-report says tier1b: all three reviewers ran on
the SONNET alias. shadow03, the requested baseline, is one of them. Both tier1b-orchestrated runs (01, 02) dispatched
the haiku and opus aliases. n is tiny and 01-02 used an older skill state: "orchestrator drives dispatch" is a hypothesis.

Not controllable without code or prompt changes: whether the orchestrator passes the class on each Agent call; which
of sonnet/opus the calibrator gets; the judge separately from the orchestrator (`invocation_method: skill-direct`).
`--agents` could redefine an agent's model; its precedence over user agents is UNVERIFIED, so it is not used.

## 3. The five combinations (Step 3)

Design: a chain of single changes, so each adjacent pair isolates one factor. A = the pilot. B changes only the
orchestrator. C changes only the haiku-class model. D changes only the opus-class model. E ports the study's best
replicated blocking panel (several changes at once). All combos keep the same prompt, flags and default tier file, so
`panel_parity` stays comparable and resolution.json is identical (`resolve/`); the expectations below are served models.
All pass `--model` explicitly (A's value equals the pilot's settings default).

| Combo | `--model` (orchestrator, judge) | SONNET (rev 1, calibrator default, validator) | HAIKU (rev 2 qa) | OPUS (rev 3, calibrator if opus) |
|---|---|---|---|---|
| A pilot-baseline | `claude-gw-tier3[1m]` | `claude-gw-tier1b[1m]` | `claude-gw-tier2[1m]` | `claude-gw-tier1a[1m]` |
| B sonnet-orchestrator | `claude-gw-tier1b[1m]` | `claude-gw-tier1b[1m]` | `claude-gw-tier2[1m]` | `claude-gw-tier1a[1m]` |
| C true-haiku | `claude-gw-tier1b[1m]` | `claude-gw-tier1b[1m]` | `claude-haiku-5-5` | `claude-gw-tier1a[1m]` |
| D luna-replaces-opus | `claude-gw-tier1b[1m]` | `claude-gw-tier1b[1m]` | `claude-haiku-5-5` | `gpt-6-luna` |
| E study-haiku-2luna | `claude-gw-tier1b[1m]` | `claude-haiku-5-5` | `gpt-6-luna` | `claude-gw-tier4[1m]` |

- A: Sonnet 5.5 / GPT 6.1 Sol / Opus 5.5 (UNVERIFIED); calibrator Sonnet or Opus; judge GLM 5.3 (UNVERIFIED today).
  Hypothesis: reference; measures repeat noise and the dispatch-collapse rate (pilot: 6/9). Risk: low (exact pilot env).
- B: same reviewers; judge Sonnet 5.5. Hypothesis: the orchestrator model drives dispatch fidelity, wall time and the
  debate outcome (runs 01-02 vs 03-11). Risk: low (tier1b was the orchestrator in runs 01-02). Judge class = reviewer 1
  class (collision recorded, not a failure).
- C: Sonnet 5.5 / Haiku 5.5 / Opus 5.5; calibrator Sonnet or Opus. Hypothesis: a real Haiku in the haiku slot (study:
  haiku is in the best real-blocking panel; sol is "do not use alone") changes qa findings and makes the panel record
  truthful. Risk: low-medium: `claude-haiku-5-5` served in 75 study runs via `--model`; raw id as env alias UNVERIFIED;
  HAIKU also feeds Claude Code side calls (audit A E2: web_fetch_apply). All-Anthropic: vendor diversity `single` (warn).
- D: Sonnet 5.5 / Haiku 5.5 / GPT 6 Luna; calibrator Sonnet, or Luna if the orchestrator gives it the opus class.
  Hypothesis: Luna (cheapest strong study component) replaces Opus with no loss of findings at lower tokens and wall;
  side effect expected: more evidence-validator drops (Luna anchor fidelity 91.4%). Risk: medium: `gpt-6-luna` served
  in 222 study runs via `--model`; env-alias path UNVERIFIED.
- E: Haiku 5.5 / Luna / Luna (tier4 alias served `gpt-6-luna` in the 2026-11-11 probe); calibrator and validator on
  Haiku (or Luna). Hypothesis: the study's high-assurance panel (haiku + 2x luna, 1.2/8 real blocking) transfers to
  reflect. Risk: HIGH: step 0.5 may judge the two Luna values as one model and run 2 reviewers (record
  `reviewer_count`); calibrator and validator change too, so E vs D is not a single-factor contrast.

Not chosen: ember panels (`muse-ember-1.0` absent from the 2026-11-13 gateway list; skipped source.md in 39% of runs);
terra/sol-only, glm, Qwen (refusals, timeouts, spend); 4-5 reviewers (reflect max 3); ember + luna (0/2 control).

## 4. Experiment protocol (Step 4)

**Input (same for all 15 runs):** `TASK-WF-designSpec-20261107-075614`, copied to `input/<id>/` (only the plan,
sha256 044809e3..., and `source.md`, a865f397...; both equal the `.dev/tasks/done` originals). Why: it is the study
package with the most ground truth (10 GT, 5 blocking in implement), so quality can be scored, not just counted; the
plan is byte-identical to the study's candidate.md; the copy leaves out `progress.md` and `artifacts/retries/`, which
hold the implement history (the answer key). Costs: large input, 25-90 min per run (pilot logs); the work already
landed, so grounding reads post-implementation code (same for every combo). Cheaper fallback: makeTheAliasOnly, but the
study caught 0/4 there (floor effect).

**Naming:** run `pre-TASK-WF-designSpec-20261107-075614-combo<A..E>-r<1..3>`; output
`.dev/eval-workspaces/shadow-model-combos/runs/<run>`; logs `.../logs/<run>.{jsonl,err,time}`. Keep runs out of
`.dev/reflect/`: `scripts/reflect_shadow_exit.py` counts every `pre-*` there toward the Stage 2 exit.

**Schedule:** 3 blocks (r1, r2, r3). Each block launches A-E together in a random order written to
`logs/block-<n>.order`; the next block starts when all 5 have exited (spreads gateway load and time of day evenly).
Before each block, and once at the end, restore `.superclaude/memory/reflect/last-pass-brainstorm-reflect-panel.md` and
`docs/memory/reflect/deviation-patterns-brainstorm-reflect-panel.md` from copies frozen before block 1 (slug = worktree
basename, shared by every run; without it r2 reads r1's summary of the same plan). `.dev/reflect/runs.jsonl` gains 15
lines. Freeze the skill: record sha256 of `~/.claude/skills/sc-reflect-protocol/SKILL.md` and
`.claude/skills/sc-reflect-protocol/SKILL.md` before each block and do not run `make sync-dev` or `superclaude install`
mid-experiment; the source SKILL.md has uncommitted edits right now (EV-1 path, compliance-rate definition).

**Launch (one run; values from combos.json; run it in the background as the pilot did):**

```bash
ROOT=/home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel; X=A; R=1
EVAL=$ROOT/.dev/eval-workspaces/shadow-model-combos; ID=TASK-WF-designSpec-20261107-075614
IN=$EVAL/input/$ID; RUN=pre-$ID-combo$X-r$R; OUT=$EVAL/runs/$RUN; cd $ROOT; mkdir -p $EVAL/logs $EVAL/runs
# O, S, H, P: this combo's "model", SONNET, HAIKU, OPUS values from combos.json
date -u +%s > $EVAL/logs/$RUN.time
env -u ANTHROPIC_MODEL -u CLAUDE_CODE_SUBAGENT_MODEL -u SUPERCLAUDE_REVIEW_TIERS -u SUPERCLAUDE_REVIEW_PANEL \
  -u SUPERCLAUDE_REVIEW_ENV -u EXECUTOR_MODEL_CLASS CLAUDE_CODE_PRINT_BG_WAIT_CEILING_MS=0 \
  ANTHROPIC_DEFAULT_SONNET_MODEL="$S" ANTHROPIC_DEFAULT_HAIKU_MODEL="$H" ANTHROPIC_DEFAULT_OPUS_MODEL="$P" \
  claude -p "/sc:reflect --mode pre --spec $IN/source.md --tasklist $IN/$ID.md --tier 2 --t2-engine shadow --output $OUT" \
  --model "$O" --permission-mode bypassPermissions --output-format stream-json --verbose --forward-subagent-text \
  > $EVAL/logs/$RUN.jsonl 2> $EVAL/logs/$RUN.err; echo "exit=$? end=$(date -u +%s)" >> $EVAL/logs/$RUN.time
```

Prompt = pilot `launch.sh` prompt except the paths. The output flags only change logging (UNVERIFIED that forwarded subagent messages carry `message.model`; if the flags are refused, use `--output-format json`).

**Record per run** (one JSON line in `results.jsonl`; source in brackets):

- calibrated confidence [`return-contract.yaml` `confidence_calibrated`; `metrics.json` calibration initial/final]
- findings [`merged-verdict.yaml` under `adversarial/` or `adversarial/adversarial/` (shadow03): verdict,
  blocking/medium/minor counts; `panel/clusters_kept.json` size]
- compliance [contract telemetry `findings_block_compliance_rate`, `calibration_coverage`, `reviewers_complete`]
- parity [recorded `panel_parity` and the recomputed value from
  `uv run python scripts/reflect_shadow_exit.py --runs-root <EVAL>/runs --required 15 --out <EVAL>/shadow-exit.md`]
- EV-1 [same script: EV-1 failure and MALFORMED count; else by hand: `merged-verdict.yaml` with `merge_method:
  adversarial` and at least `reviewers_complete` calibrated cards in `reviewer-cards/`]
- wall time [launcher `.time`; `result` event `duration_ms`]; tokens [`result` event `usage`, `modelUsage` per model,
  `total_cost_usd`]. The contract's `wall_clock_ms` / `token_usage` are orchestrator estimates: record, never compare
- models: requested [`.err` `unrecognized_model` lines: first request per model only]; served [jsonl `message.model` per
  `parent_tool_use_id`]; self-reported [`reviewer_model_self_report` in `reviewer-cards/`, `judge_identity`]; plus
  `reviewer_count`, `calibrator_diversity`, `identity_mismatch_suspected`, `citations_total` / `citations_dropped`,
  `adversarial_convergence_score`, `status`
- `dispatch_ok` (reviewers got the 3 intended models, served else requested); `leak` (a citation into the package's
  `.dev/tasks/done/` folder in cards, debate files or REPORT.md)
- optional, separate approval (spends tokens): blind GT score as in the study: anonymize REPORT.md and the merged
  verdict (strip model and combo names), random labels, one Opus judge per run against `git show
  b4db265a8:.dev/eval-workspaces/tasklist-review-panel/20261111-a1/TASK-WF-designSpec-20261107-075614/ground-truth.json`;
  record GT found /10, real blocking /5, wrong blockers.

**Deciding whether results differ (descriptive, decided before launch):**

- Show every run's value plus median and range per combo; no significance tests. Runs with `dispatch_ok: false`,
  `leak: true` or a crash stay in the table, marked and summarized separately. Compare adjacent pairs only (A-B
  orchestrator, B-C haiku slot, C-D opus slot, D-E study panel; E is a package of changes, not a single factor).
- Call a difference "a lead worth a bigger run" only when (1) the ranges do not overlap, (2) the median gap is larger
  than A's own range, and (3) both combos have `dispatch_ok` in at least 2 of 3 runs. Complete separation of 3 vs 3
  happens 2 times in 20 by chance alone (10%), and there are about 40 metric-pair comparisons, so expect a few chance
  separations: leads, not findings.
- Not meaningful at n=3: a 1-item gap in findings or GT hits; calibrated-confidence gaps under 0.10; 2/3 vs 1/3 on any
  yes/no outcome; parity alone (it records the class rotation, not the served model).
- Meaningful as plain facts even at n=3: something that happens 3/3 (a model not served, E running 2 reviewers, EV-1
  failing, dispatch collapse under one orchestrator and not the other); token or wall ratios of 1.5x or more with
  non-overlapping ranges.

## 5. Open risks and UNVERIFIED items

- Gateway `/v1/models` (2026-11-13, no inference) lists tier1a-tier4, Sonnet/Haiku/Opus 5.5, `claude-gw-gpt-6-luna[1m]`,
  not `muse-ember-1.0`. Today's models behind tier1a and tier3: UNVERIFIED (2026-11-11 probe: tier3 = GLM 5.3).
- Raw ids as `ANTHROPIC_DEFAULT_*` values: UNVERIFIED (study proved only `--model`); a one-question smoke test per
  value before block 1 settles it (a few tokens; needs approval).
- If B-E also collapse dispatch in most runs, the reviewer contrasts are void; the fix is a prompt or skill change.
- UNVERIFIED: advocate and merge-executor models; contention at 5 concurrent runs (pilot ran 4; total ~3-5 h); the
  exit script with no legacy baseline (EV-1 baseline n=0, use the by-hand check); study `source.md` = this copy.

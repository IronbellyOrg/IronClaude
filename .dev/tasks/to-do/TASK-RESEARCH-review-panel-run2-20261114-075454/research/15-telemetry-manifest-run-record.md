# Research: telemetry, manifest, run record, cost and memory policy
**Investigation type:** Code Tracer
**Scope:** `src/superclaude/cli/review/{telemetry.py,telemetry_cmd.py,manifest.py,manifest_cmd.py}`, `model_scores` cost fan-out (D-17), `src/superclaude/cli/reflect/` run artifacts, `.dev/reflect/`, E2 `collab.json` and results rows (git only, tip 6c0984326cbb8fb06c4a36065de58b171d3f8175), memory write policy (`src/superclaude/skills/sc-reflect-protocol/SKILL.md`, `docs/memory/reflect/`); slices 09, 11, 07, 08 in `research/scope/`
**Status:** Complete
**Date:** 2026-11-14
---

## 0. Method and independence

- Slices 09, 11, 07, 08 in `research/scope/` were read first (slice 09 in full; slices 11, 07, 08 in their first pages, which hold the telemetry-relevant material); every claim kept below was re-checked against HEAD (`ironbelly/shadow-runs`, 50d4d2b9d) or against the E2 tip `6c0984326cbb8fb06c4a36065de58b171d3f8175` through `git show` / `git ls-tree`. [CODE-VERIFIED] means "read at the cited file:line in this session".
- The forbidden run-1 folder and the RUN2-QUEUED note were not read, listed or searched. Repo-wide searches excluded `.dev/tasks/`.
- Scratch: `/tmp/review-panel-run2-2.15/repro.py` (stdlib only, loads `telemetry.py` and `manifest.py` by file path with `uv run --no-project`, `PYTHONDONTWRITEBYTECODE=1`; writes only under the scratch directory). Nothing was written in the repository by me other than this file.

## 1. `src/superclaude/cli/review/telemetry.py` (447 lines) and `telemetry_cmd.py` (98 lines)

### 1.1 What the store is [CODE-VERIFIED]
- `SCHEMA_VERSION = "review-telemetry/1"` (telemetry.py:17); two record kinds only: `reviewer_run` and `outcome` (`validate_record` :196-281; any other kind returns `kind must be 'reviewer_run' or 'outcome'`, :265-266).
- A `reviewer_run` record = `REVIEWER_TOP` (schema_version, kind, record_id, ts_utc, run_id, step, round, reviewer_id; :82-91) + six groups (`REVIEWER_GROUPS` :30-81: panel, slot, model, task, output, cost) + `context` (+ optional `supersedes`, `stratum`; :205-206). Unknown keys are rejected at the top level and inside each group (:210-212, :223-225).
- `cost` group = tokens_in, tokens_cache_read, tokens_cache_write, tokens_out, wall_s (:74-80): the unit is tokens and seconds per REVIEWER SESSION; there is no USD field, no stage field other than the free `step` label, and no record kind for orchestrator, calibrator, debate, judge, validator or sweeper cost.
- An `outcome` record = `OUTCOME_KEYS` (:92-109): reviewer_record_id, truth_basis (`catalog-v1|theme-v1|adjudicated-v1`, :18), confirmed_tp, false_pos, unconfirmed, unique_tp, overlap_mean_jaccard, recall_vs_confirmed, precision, cost_per_confirmed_tp, supersedes (+ optional stratum).
- Storage: `append_record` (:287-307) validates, then appends one JSON line to `<dir>/records/<YYYY>/<MM>/<run_id>.jsonl` (reviewer runs) or `<run_id>.outcomes.jsonl`; an existing file for that run id in ANY year/month directory wins (`existing[0]`, :298-300); plain `open(path, "a")`, no lock, no fsync. Default directory `.dev/benchmarks/review-telemetry` (telemetry_cmd.py:12), overridable by `SUPERCLAUDE_REVIEW_TELEMETRY_DIR` (:46).
- Loader `load` (:382-447): SQLite tables `reviewer_runs`, `outcomes`, `INSERT OR IGNORE` on `record_id` (:417-435), view `model_scores` dropped and recreated each load (:436-437).
- `task_variables` (:142-190) computes document descriptors (sha256, bytes, lines, language heuristic, sections, tables, ids_defined, cross_refs, rfc2119); its ID grammar `_ID_TOKEN` (:23) is a copy of `_REF_TOKEN` in `findings.py:29` (same alternation `[A-Z]{1,4}-[0-9]+(\.[0-9]+)*|P[0-9]`; telemetry builds a string and adds `\b` itself, findings compiles a regex). Both anchors named in the assignment confirmed by Grep. [CODE-VERIFIED]

Key Takeaways
- The schema is reviewer-session-centric and counts-only: it cannot express a stage (calibrate, debate, validate), a cluster, a finding or a non-reviewer agent.
- Document-text safety is by schema shape (closed key sets) plus value rules on `context` only; see 1.4.

### 1.2 Writer search (negative evidence) [CODE-VERIFIED]
- Search: Grep `append_record|new_record_id|now_utc|task_variables|review\.telemetry|model_scores|review-telemetry` over the repository excluding `.dev/tasks/**`, `.dev/eval-workspaces/**`, `.git`, `.venv`. Hits in production code: only `telemetry_cmd.py:10,36,67` (the CLI) and the definitions in `telemetry.py`. No call from `merge_cmd.py`, `ledger_cmd.py`, `manifest*`, `scripts/*.py` or any `src/superclaude/cli/reflect/*.py`. So the D-8 statement "no writer in src/ or scripts/" holds. Tests are the other callers (`tests/review/test_review_telemetry.py`, `tests/review/test_review_cli.py:386`).
- NUANCE that slice 09 did not record: real writers exist OUTSIDE production code, in E3 experiment harnesses committed under `.dev/research/346-review-loop-experiments/`: `p20/live-evals/harness/harness.py:534-560` (`append_telemetry`: builds a full `reviewer_run` record after each merge, writes it to a JSON file and calls `superclaude review telemetry append --dir ... --record ...`; it sets `verdict_mismatch` from the merge result, `stratum` and `context{experiment, arm, replicate, stratum}`), `p20/live-evals/harness/report.py:134-142` (writes `outcome` records and calls `telemetry load`), and the same pattern at `p13/ab1/harness.py:533` and `p13/ab1/report.py:135` (grep hits; bodies not read). Conclusion: the schema was designed for, and exercised by, a harness that sat outside the package; the "one writer in the core (the merge step)" proposed by D-8 would move that harness code into `merge_cmd.py`. [CODE-VERIFIED at p20 lines; p13 lines by grep only]
- Reflect side: the SKILL.md `telemetry:` block (SKILL.md:969-988) and `metrics.json` / `.dev/reflect/runs.jsonl` (SKILL.md:1721-1824) are written by the LLM orchestrator. Grep `runs\.jsonl|metrics\.json|metrics_schema_version` over `*.py` shows no Python writer in `src/` or `scripts/` (hits are `scripts/reflect_consumer_inventory.py` text scans and E3 harness files); the only writer of a real run's `metrics.json` and `runs.jsonl` row that I found is an ad-hoc script `.dev/reflect/pre-TASK-WF-spec-20261019-204314-20261019204736/finalize-review.py:85-86` (grep hit). [CODE-VERIFIED negative; one ad-hoc positive by grep]

### 1.3 Seven shapes for "what a run cost and did"
| Surface | Writer | Location | Unit of cost | Source |
|---|---|---|---|---|
| `review-telemetry/1` JSONL + SQLite | none in `src/` (E3 harnesses only) | `.dev/benchmarks/review-telemetry/records/YYYY/MM/<run_id>[.outcomes].jsonl` | per reviewer session: tokens in/cache/out, wall_s | telemetry.py:30-81, 287-307 |
| reflect `telemetry:` block in `return-contract.yaml` | LLM orchestrator (shadow steps) | `<output>/return-contract.yaml` | none (flags and counts: reviewers_requested/resolved/complete, compliance, parity, cluster_agreement, calibration_coverage) | SKILL.md:969-988 |
| reflect `metrics.json` | LLM orchestrator | `<output>/metrics.json` | `token_usage{claude_orchestration, claude_agents, auggie_offloaded, total}`, `wall_clock_ms`, `wave_durations_ms` | SKILL.md:1721-1810 |
| reflect `runs.jsonl` | LLM orchestrator, best effort | `.dev/reflect/runs.jsonl` (gitignored, `.dev/reflect/.gitignore:3`) | `token_usage_total`, `wall_clock_ms` | SKILL.md:1812-1824 |
| manifest `review-panel-manifest/1` | `review manifest` CLI | `<out>/panel/manifest.json` | none (hashes, stage state, attempts, reviewer counts) | manifest.py:38-64 |
| E1 experiment `results.jsonl` | `analysis/extract.py` from stream logs | `.dev/eval-workspaces/shadow-model-combos/results.jsonl` | `usage{alias:{in,out,usd}}`, `cost_usd`, `out_tokens` | extract.py:43-79, 160-162 |
| E2 result rows (five schemas) | per-design harness code | `<design>/results/*.json(l)` at the E2 tip | `output_tokens` only (shape differs per design) | later section |

Key Takeaways
- Seven shapes, no common key. A unified run record must be an adapter target for all of them, not a replacement of one.

### 1.4 Item (b): can study telemetry carry anchors? [CODE-VERIFIED]
- The module claims "No document text, quote, anchor or claim ever enters a record" (telemetry.py:3). Enforcement actually present: (1) closed key sets at top level and in each group (:210-225), so there is NO `anchor`, `claim`, `quote` or `findings[]` key to put text under; (2) `context` values must be `^[A-Za-z0-9._-]{1,64}$` labels or numbers (:243-251), so a 12..200 character anchor with spaces fails; (3) a test reportedly checks that 40-character windows of the document do not appear in a record built from `task_variables` (slice 09 H, `test_review_telemetry.py:156-163`) [UNVERIFIED by me, cited from slice 09].
- Not enforced: values inside the six groups are not type-checked (:213-225 test key presence only), so a sentence placed in `task.specialization` or `model.resolved` validates. Slice 09 D-31 reports this as `[RUN]`; I re-derived it by reading :213-225. The privacy invariant is a convention for everything except `context`.
- Answer to (b): study telemetry as it stands cannot carry anchors and should not. The design that fits both the invariant and the need is: telemetry carries POINTERS, never text: `ledger_sha256` plus ledger row ids and fingerprints (`fp`, `findings.py:340-343`, 16 hex chars derived from section + requirement ids, not from anchor text), cluster ids (`C<i>`) and `doc_sha256` (telemetry.py:176). Anchor text stays in the ledger (`review-ledger/1` rows hold `anchor`/`anchor2`, slice 09 B2) and in `clusters.json`/merged report, which are run artifacts, not telemetry. For per-finding adjudication add an outcome-like record keyed by `(ledger_sha256, lid)` with enums and counts only, and type-check every group value so the privacy rule becomes enforceable (fixes D-31).
- Lost by this design: nothing the current `outcome` schema uses (counts and rates, :92-109). Gained: joins from telemetry to ledger rows without copying text.

Key Takeaways
- Anchors cannot ride in telemetry today and need not: use hash pointers into the ledger.
- To keep the "no text" promise, value types must be checked in `validate_record` (D-31); today only `context` is.

## 2. Item (c) part 1: D-17, `model_scores` cost fan-out [CODE-VERIFIED by reading and by scratch run]

Trace by hand (telemetry.py:362-379):
1. The view selects from `reviewer_runs r LEFT JOIN outcomes o` on `o.reviewer_record_id = r.record_id`, with the stratum condition and `o.record_id NOT IN (SELECT supersedes ...)` (:372-376), and keeps only non-superseded reviewer runs (:377).
2. One reviewer run joined to k live outcomes yields k rows. `COUNT(DISTINCT r.record_id)` (:365) is immune, but `SUM(r.cost_tokens_out)` (:371) adds the run's cost k times, while `SUM(o.confirmed_tp)` adds each outcome once.
3. The view never references the stored `o.cost_per_confirmed_tp` column (not in :362-379): the recorded value and the computed value have two sources.
4. Grouping includes `o.truth_basis` (:378): a run scored under two truth bases appears once per group with its full cost in each; a consumer that adds cost across groups counts it twice.

Reproduction (`/tmp/review-panel-run2-2.15/repro.py`, one reviewer run, `tokens_out` = 1000):
| Case | Outcomes attached | `n_runs` | `sum_confirmed_tp` | `cost_per_confirmed_tp` | Correct value |
|---|---|---|---|---|---|
| c1 | 1 outcome, tp 2 | 1 | 2 | 500.0 | 500.0 |
| c2 | 2 live outcomes, same basis, tp 2 and 3 | 1 | 5 | 400.0 | 200.0 (1000/5): cost counted twice |
| c3 | second outcome supersedes the first (tp 3) | 1 | 3 | 333.33 | 333.33 (supersession works) |
| c4 | 2 outcomes, different bases | 1 and 1 (two rows) | 2 and 3 | 500.0 and 333.33 | each row correct; the 1000 appears in both rows |
| c5 | no outcome | 1 | NULL | NULL | one row, `truth_basis` NULL |

Result: D-17 is real but narrow. It needs two live (non-superseded) outcomes of one reviewer run; the loader neither prevents nor reports that (`INSERT OR IGNORE` only dedupes record ids, :417-435) and `append_record` does not check it. The supersession mechanism is the intended guard and works (c3).

Fix direction: pre-aggregate outcomes per `(reviewer_record_id, truth_basis)` in a sub-select before joining, or compute cost in a view over `reviewer_runs` only; enforce "at most one live outcome per `(reviewer_record_id, truth_basis)`" in the loader and report violations (also covers D-16, silent drops of changed duplicate ids).

Key Takeaways
- Cost fan-out reproduced (400 vs 200 per TP in c2); the supersession path is clean.
- Cost across truth bases is repeated per group; never sum `model_scores` cost over `truth_basis`.

## 3. Item (c) part 2: D-23, manifest lost updates [CODE-VERIFIED by reading and by scratch run]

Trace by hand:
1. `advance_cmd` (manifest_cmd.py:160-215): `mf.load(path)` (:171), mutate in memory (`record_attempt` :181 or `advance_stage` :203), `mf.save(path, manifest)` (:205).
2. `save` (manifest.py:156-163) writes `.manifest.json.tmp-<pid>` then `os.replace`: atomic per write, no `fsync`, no lock, no version check. The pid in the temporary name stops two processes corrupting each other's temporary; the later `os.replace` wins and the earlier writer's change is gone.
3. `record_attempt` and `advance_stage` check idempotency and order only against the in-memory copy (manifest.py:293-306, 355-372), so a stale copy accepts a second reviewer's attempt.
4. The only protection is the documented rule "One coordinator writes the manifest" (manifest.py:3) and the SKILL text that records attempts then advances (SKILL.md:342). Nothing enforces serial CLI calls; an orchestrator batching Bash calls in parallel would interleave them. [UNVERIFIED whether any real run did]

Reproduction (deterministic interleaving of the CLI's load/modify/save): state `dispatched`; A loads, B loads; A records reviewer-1 `collected complete`; B records reviewer-2 `collected complete`; A saves; B saves. On disk: `attempts = [('reviewer-2','complete')]`, `reviewers_complete = 1`. Sequential control: both attempts kept, `reviewers_complete = 2`. A real two-process race was not run (non-deterministic).

Consequence: `reviewers_complete` feeds the shadow 2-of-3 shortfall (SKILL.md:987) and `reviewers_resolved` feeds the EV-1 lint (`panel_lint.py:246-266`), so a lost update can silently change a verdict input. Fix direction: `fcntl.flock` on `<out>/panel/manifest.lock` around load-modify-save plus a monotonically increasing `rev` that `save` refuses when stale; or make attempts append-only JSONL folded into the manifest view.

Key Takeaways
- D-23 is a real lock-free load-modify-save race; harmless under strict serial use, silent loss otherwise.
- Telemetry `append_record` has the same no-lock shape (one `open(..., "a")` per record); small appends are practically atomic on POSIX but nothing here guarantees it [UNVERIFIED].

## 4. Reflect Tier 2 run artifacts and E1 cost data

### 4.1 What one real shadow run leaves on disk [CODE-VERIFIED by listing]
`.dev/reflect/pre-TASK-WF-detachTheCcsessi-20261102-034618-shadow03/` holds `REPORT.md`, `return-contract.yaml`, `audit.log`, `metrics.json`, `t1-card.md`, `reviewer-cards/`, `reviewer-briefs/`, `adversarial/`, `artifacts/{coverage-matrix,input-snapshot,tier_decision}.yaml` and `panel/{cards/, clusters.json, clusters_kept.json, coverage.json, kept-ids.txt, manifest.json, payload-resolved.json, precheck.json, resolution.json, resolve.stderr}`. The reflect CLI package (`src/superclaude/cli/reflect/{config,commands,_diversity,contract,models,runner,ensemble,fallback,panel_lint}.py`) only READS these (lint, contract validation); Grep for `metrics.json`/`runs.jsonl` over `.py` found no writer there (section 1.2).

### 4.2 Manifest attempts carry no data [CODE-VERIFIED]
- `record_attempt` stores `{stage, reviewer_id, attempt_id, completion, payload_sha256}` where `payload_sha256 = sha256_json({"completion": completion, **(payload or {})})` (manifest.py:348-354): the payload CONTENT is hashed and discarded. In shadow03's `panel/manifest.json` all six attempts have the identical `payload_sha256` `83115a12...a516b2`, i.e. nothing but `{"completion":"complete"}` was recorded for any reviewer or stage.
- So the manifest, the only per-reviewer state record in the Tier 2 path, cannot hold model_observed, tokens or wall time today. To serve as the run record it needs a stored `usage`/`model_observed` object per attempt (a schema change), or it must stay a state machine and the run record lives beside it.

### 4.3 `metrics.json` and `runs.jsonl` values are orchestrator estimates [CODE-VERIFIED for shadow03; pattern across runs UNVERIFIED]
shadow03 `metrics.json`: `wave_durations_ms` = 40000 / 480000 / 5000 / 360000 / 780000 / 300000 (round numbers), `wall_clock_ms` 1965000, `token_usage` = 60000 / 480000 / 0 / total 540000, `citations_dropped: 1` of 16 with `drop_rate: 0.0` (a drop recorded as rate 0.0; matches slice 11 section 3.1). Two combo rows in `.dev/reflect/runs.jsonl` (27 lines, `wc -l`) have `"token_usage_total": null` (comboD-r3, comboC-r3). Measured wall time from E1 `logs/*.time` (slice 11 2.4) differs from the orchestrator's `wall_clock_ms` (A1: 1,009,000 ms recorded vs 63.9 min measured; slice 11, [UNVERIFIED by me]). Conclusion: a run record whose numbers are written by the LLM orchestrator is not usable for cost; cost must come from the harness transcript or stream log.

### 4.4 E1 experiment cost data [CODE-VERIFIED: recomputed]
- Source: `.dev/eval-workspaces/shadow-model-combos/analysis/extract.py:42-81`. `usage` = the `result` event's `modelUsage` of the orchestrator session, i.e. a per-RUN total keyed by the model name as the harness sees it (an alias such as `claude-gw-tier2[1m]`), with `inputTokens`, `outputTokens`, `costUSD` (:70-73). Served model per sub-agent comes separately from sidechain `assistant` messages keyed by `parent_tool_use_id` (:54-58) and is stored only as `(requested, served)` pairs. Per-agent tokens are NOT extracted.
- Therefore cost cannot be attributed to a reviewer, a calibrator or a stage in E1 data; only to a harness alias. `FINDINGS.md:37` states the USD figure is "Claude Code's estimate from model names, not a billed figure". When the served model differs from the alias (tier2 served `gpt-6.1-sol` in A and B, FINDINGS.md:15), the USD is an estimate for a model that did not serve [UNVERIFIED how Claude Code prices an alias].
- Recount of `results.jsonl` (15 rows, `uv run --no-project`): sum `out_tokens` = 4,119,747 tokens; sum `cost_usd` = USD 478.4; `out_tokens` equals the sum of `usage[*].out` in every row (15 of 15), `cost_usd` equals the sum of `usage[*].usd` within USD 0.01 (rounding). Share of output tokens on the orchestrator's alias: min 0.38 (E1), median 0.59, max 0.87 (B3). Caveat the slice did not state: in combos B, C, D the orchestrator alias (`claude-gw-tier1b[1m]`, PLAN.md:83-89) is also the SONNET-class alias (reviewer 1, validator, default calibrator), so those shares are UPPER bounds for the orchestrator; in A (tier3) and E (SONNET class = `claude-haiku-5-5`) the alias is the orchestrator alone.
- Combo A3 collapse: `reviewer_requested_served` = `[None, claude-sonnet-5-5]` x3 and calibrators likewise, yet the contract says `calibrator_diversity: full`, `judge_class_collision: false`, `identity_source: requested-pinned` and `reviewer_models: [claude-sonnet-5-5, claude-haiku-5-5, claude-opus-5-5]` (`runs/...comboA-r3/return-contract.yaml:70,115,144,147`). `calibrator_diversity` is `degraded` in 14 of 15 rows and `full` only in the collapsed A3 (Counter on results.jsonl). The contract's diversity fields record the REQUESTED rotation, so they cannot be an input for cost-by-model or independence claims. [CODE-VERIFIED]

Key Takeaways
- Per-agent cost and observed model exist only in harness transcripts (stream-json sidechains, Claude Code session JSONL); neither the contract, the manifest nor the metrics file has them truthfully.
- Any unified run record needs a transcript adapter as its writer-side input; a skill-side orchestrator cannot supply truthful values (see s-id decision D-3 in slice 11: the observed id is readable only from the sidechain transcript, [UNVERIFIED by me]).

## 5. E2 `collab.json` and results rows (git only, tip 6c0984326cbb8fb06c4a36065de58b171d3f8175)

Base `$B` = `.dev/eval-workspaces/tasklist-review-panel/20261113-collab/`.

### 5.1 What exists in git [CODE-VERIFIED via `git ls-tree -r`]
- `collab.json` as a file: exactly ONE, `r1-move-radar/spikes/smoke/provisional-c1/collab.json` (schema `r1-collab/1`). The other designs embed their collaboration counters in the results row (`r2-results/1` `collab{}`, `r4-results/1` `collab{<pkg>:{}}`, `r3-result/1` `collab{}`, r5 `collab`). Per-run directories (`runs/<row>/<pkg>/collab.json` per R1/DESIGN.md:98 and requirement R-23) are NOT tracked.
- Requirement R-23 (E2 brainstorm, `git show $T:.dev/brainstorms/20261113-163248-panel-collaboration/merged-requirements.md:1050`) lists the `collab.json` fields: arm; per reviewer `msgs_sent, msgs_received, first_delivery_t, seal_t, resume_fallback, phase2_s, stop_blocks, hook_calls, hook_error, hook_ms_p95, reask_s, attempts, retry_s, retry_isolated, phase2_timeout, p2_lines_salvaged, n_planned, n_launched, k, panel_finish_at, finish_signal_t, finish_would_fire, hang_kill, snapshot_missing, late, over_cap`; per slot `slot_type, card_form, deal_r, deal_c`; panel `elapsed_s, baseline_elapsed_s, overhead_pct, own_line_jaccard, pairwise_task_jaccard, echo_rate, ledger_rows` and the values-file sha256. R-24 (:1051) audits the +35% cap from `elapsed_s`; R-30 (:1062) requires the values-file sha256 in every `collab.json`; R-46 (:1099) deletes session ids recorded in `collab.json`.

### 5.2 Five result-row schemas for the same question [CODE-VERIFIED by `git show` of one row each]
| Design | Schema id | `output_tokens` shape | Per-package key | Where collab counters live |
|---|---|---|---|---|
| R1 | `r1-results/1` (`results/el2-c0-r0.json`) | `null` at row level; per package `output_tokens: 21127` | full package id | `collab_counters{}` + separate `collab.json` per package (untracked) |
| R2 | `r2-results/1` (`results/smoke-sl2-collab.json`) | `{total, reviewers, sweeper, reask}` | full package id | `collab{}` in the row |
| R3 | `r3-result/1` (`results/smoke.jsonl`) | `{total, by_pkg, phase2, reask}` | full package id | `collab{}` + `sealed{}` |
| R4 | `r4-results/1` (`results/smoke-f7-el2-2.json`) | plain number (17419) | SHORT key `"DE"` in `elapsed_s` and `overhead_pct`, full id in `packages` | `collab{<pkg>:{}}` |
| R5 | no `schema` key (`schema = null`, `results/results.jsonl`) | `{total, per_pkg, per_reviewer{<pkg>:{rid:n}}}` | full package id | `collab` |
Common keys: `found_14, real_blocking_8, judge_blocking, wrong_blockers, control_found_2, control_wrong_blockers, output_tokens, elapsed_s, overhead_pct, row/run_id, panel, arm, models`. The unit of cost in every E2 row is OUTPUT TOKENS (no input, no cache, no USD); only R5 breaks tokens down per reviewer; R2 splits reviewers vs sweeper vs re-ask; R3 splits phase 2 vs re-ask.
- Values and validity flags differ: R1 `status: incomplete` and `values.<pkg>: "planning"`; R2 `planning: true` and an `invalid[]` list; R3 `smoke: true`, `values_status: "planning"`, `judge_ok`, `contaminated`; R4 `valid: false` on a row that ran fully (`finished: null`), `pins_ok`, `seed`; R5 `alarms`, `switches`, `pkg_status`, `issues`.
- Blind-label keys: R2 `results/keys/<opaque>.json` and `scoring/<opaque>/<pkg>/label-key.json`; R5 `results/scoring-keys.jsonl` (`{token,row,pkg,label,arm,redactions,status}`); R1 `scoring/<opaque>/<pkg>/<letter>/score.json`. A run record that serves study work must keep the label key OUT of the scoring directory (R5 does this by design; R3 `scoring-keys.json`, slice 08 S4.5).

### 5.3 What this means for the run record [derived]
- E2's own telemetry (R-23) is design-specific (hooks, snapshots, boards) and per package; its common core is small: arm, panel, per-reviewer `model`, `attempts`, `elapsed_s`, `output_tokens`, `ledger_rows`, `own_line_jaccard`, values-file sha256, judge outputs (`gt_covered_any`, `gt_covered_blocking`, `wrong_blockers`, `score.json` keys listed in slice 07 A4). Those map onto `reviewer_run` + `outcome` records (telemetry.py) with the design-specific counters under a namespaced extension object, not onto new top-level keys.
- The E2 smoke rows are single runs on planning values and cannot support any cost claim (slice 07 A7, [UNVERIFIED by me]; the row flags above are [CODE-VERIFIED]).

## 6. Memory write policy [CODE-VERIFIED]

### 6.1 The rule (sc-reflect-protocol/SKILL.md:585-608)
- Read at Wave 0: `.superclaude/memory/reflect/last-pass-{slug}.md` (missing file = miss) and `docs/memory/reflect/deviation-patterns-{slug}.md`. Write at Wave 5: `last-pass` (`Write`, "single-owner file, overwritten whole") and `deviation-patterns` ("tracked file: Read, merge, then Write whole"); Wave 6 handoff file written once, never edited (SKILL.md:590-594, 600).
- Retention: keep the last 20 entries (an entry is one `## <run-id>` section) and expire entries older than 90 days, applied inside the file at write time (:598, 602); the current pass is merged after the trim (:606); no primitive deletes a memory file (:607). Slug = `pwd` basename sanitized (:598), so one file per worktree name.
- `.superclaude/` is gitignored (`.gitignore:114`, verified with `git check-ignore -v`); `docs/memory/reflect/deviation-patterns-*.md` are tracked (14 tracked files by `git ls-files`), except the live `deviation-patterns-brainstorm-reflect-panel.md`, which is untracked at HEAD (git status at session start) and 100 lines with 14 `## ` sections (`grep -c`), 23,446 bytes, file mode 0644 while the other tracked files are 0600.

### 6.2 Findings
1. No deterministic writer: the merge-and-trim is an LLM `Read` + `Write` of the whole file (SKILL.md:593, 602). Concurrent runs in one worktree therefore share a read-modify-write on one file with no lock, the same shape as D-23. E1 block 3 ran A-E r3 concurrently; the live file holds r3 sections for A, C, D, E and none for B (`grep -c comboB` = 0). This is NOT a lost update: B-r3's contract states `memory_persist_skipped: experiment froze docs/memory file; entry in artifacts/memory-entry.md` (`runs/...comboB-r3/return-contract.yaml:140`). The orchestrator decided to skip persistence; nothing in code enforces either choice. A lost update among the four that did write is not excluded [UNVERIFIED].
2. Contamination channel: `memory_hits` is 2 in B-r3 and 1 in A-r3 (same contract keys), so runs of one experiment read different memory depending on write order (PLAN.md memory freeze is slice-11 section 2.1, [UNVERIFIED by me]). Any study that compares arms must freeze or disable memory reads; the protocol has no flag for that.
3. Retention is a prompt rule: the live file has 14 sections (limit 20), so the limit is not tested by this evidence. Section order is not newest-first (combo C-r3 first, A-r3 last at line 96, headings by `grep -n '^## '`), so "last 20" by position and by date can disagree [CODE-VERIFIED].
4. Memory content is review OUTPUT (deviation families, panel mechanics lessons), not run telemetry; it belongs next to the run record (pointer by run id), not inside it. Telemetry facts (counts, identity) must not be written as memory prose. One wrong lesson already lives in it (slice 11 3.2: memory line 64 contradicts `cluster_cmd.py:27-34`; I did not re-verify) [UNVERIFIED by me].
5. `last-pass-{slug}.md` (gitignored, 5,361 bytes, 5 `# last-pass` entries at lines 1, 7, 14, 20, 28) is documented as "single-owner, overwritten whole" yet accumulates entries, so the stated single-owner semantics and the observed content disagree. [CODE-VERIFIED by grep]

Key Takeaways
- Memory is a third write-by-LLM, read-modify-write, lock-free store; for a unified panel it should be written only at publish by one step, with the run id as key, and be switchable off for studies.

## 7. Field evidence for D-23: do real manifests show lost attempts? [CODE-VERIFIED by scan]
Scan (`uv run --no-project`, read-only) of all 29 `panel/manifest.json` files under `.dev/reflect/*/` and `.dev/eval-workspaces/shadow-model-combos/runs/*/`: 28 are `published`, 1 is `clustered` (the aborted shadow02). In 20 of 29 the number of `dispatched` attempts, `collected` attempts and `reviewers_complete` all equal `reviewers_requested` (3). In 9 (shadow04, 05, 08, 09, 10 and combos A-r2, A-r3, B-r2, C-r2) only the 3 `collected` attempts exist, no `dispatched` attempts, and `reviewers_complete` is still 3. No manifest has fewer than 3 `collected` attempts. Reading: (1) no observed instance of a lost reviewer attempt; (2) the 9 missing `dispatched` rows are explained by the stage rule, not a race: `record_attempt` refuses once the stage is committed (`stage in m["stages"]`, manifest.py:371), so an orchestrator that advanced `dispatched` before recording attempts could not add them later; this matches slice 11 memory line 58 ("record per-attempt rows BEFORE advancing the closing stage", cited, not re-read). D-23 therefore stays a latent hazard with zero observed incidents in 29 runs; the observed defect is a protocol omission that a deterministic writer would prevent.

## 8. Item (a): ONE run-record design for reflect, tasklist and spec review [PROPOSAL derived from the evidence above]

Requirements taken from the evidence: (1) truthful cost and observed model exist only in harness transcripts (section 4.4); (2) the manifest stores hashes, not data (4.2); (3) LLM-authored numbers are estimates (4.3); (4) concurrent writes lose data unless serialised (section 3, 6.2); (5) telemetry must hold no document text (1.4); (6) E2 rows share a small core and differ in extras (5.2); (7) the same run must serve a reflect shadow run, an E2-style tasklist panel and a spec-review loop round.

### 8.1 Location
Per run, beside the manifest: `<out>/panel/events.jsonl` (the manifest already lives at `<out>/panel/manifest.json`, manifest_cmd.py:19-20, and `cluster`/`verify-citations` write `<out>/panel/*.json`, so the directory is the established per-run home). Cross-run store: the existing `review-telemetry` JSONL tree (`.dev/benchmarks/review-telemetry`, telemetry_cmd.py:12), fed from `events.jsonl` at publish. `.dev/reflect/runs.jsonl` and `metrics.json` become rendered views of the run record, not hand-written files.

### 8.2 Writer
One CLI, `superclaude review record add --out <out> --event <json|file>`, appends exactly one line per call under an exclusive `flock` on `events.jsonl` (the writer assigns `seq`, `ts_utc`, `run_id`), plus `superclaude review record export --out <out> --telemetry-dir <dir>` run once at publish that derives the `reviewer_run` (and later `outcome`) records for the cross-run store and renders the contract `telemetry:` block and `metrics.json` numbers from events. Inputs for cost and `model_observed` come from a transcript adapter script (the extract.py pattern: sidechain `assistant.message.model` per `parent_tool_use_id`, `usage` from the session log), never from the orchestrator's memory. When the adapter cannot read a value the field is `null` and `identity_source` stays `requested-pinned`; nothing is estimated. Append-only plus flock removes the D-23 shape for attempts; the manifest keeps the state machine but should also take a flock and a `rev` check (section 3).

### 8.3 Event fields (schema id `review-run-event/1`)
- Identity: `run_id`, `seq`, `ts_utc`, `stage` (manifest stage name or `orchestrator`), `round` (ledger round for loops), `agent_role` (`reviewer|calibrator|debater|judge|validator|helper|orchestrator`), `agent_id` (`t1b-1`, `calibrator-1`, ...), `attempt_id`, `completion` (manifest.COMPLETIONS, manifest.py:52).
- Model: `model_requested` (class or alias as passed), `model_resolved` (from `panel/resolution.json`), `model_observed`, `identity_source` (`observed|requested-pinned`, SKILL.md:974).
- Lens: `lens`/`persona` (free label, enum per module), so a tasklist or PR module adds values without a schema change.
- Usage: `tokens_in`, `tokens_cache_read`, `tokens_cache_write`, `tokens_out`, `wall_s` (the telemetry `cost` group, telemetry.py:74-80), `usage_complete` (false for killed or unread sessions), optional `usd_estimate` clearly named as an estimate.
- Output (reviewer rows): `block_ok`, `findings`, `blocking`, `by_severity{CRITICAL,MAJOR,MINOR}`, `verdict` (the telemetry `output` group, :66-73), plus `first_parse_ok` (the SKILL's compliance definition, SKILL.md:343).
- Pointers, never text: `artifacts[{kind, path, sha256}]` for the card, report, ledger, `clusters.json`, `precheck.json`; ledger row ids `lid` and fingerprints `fp` for finding-level joins (answers item b).
- Labels: `context{experiment, arm, replicate, stratum, values_sha256}` as short labels or numbers (telemetry.py:243-251 rule, kept and extended to every group by type checks).
- `ext{<module>: {...}}`: namespaced design-specific counters (E2 R-23 fields such as `hook_calls`, `snapshot_missing`; reflect `calibration_coverage`), typed per module; never top-level keys, so a module cannot widen the core schema.

### 8.4 What each consumer gets from the same rows
| Consumer | Derived from events |
|---|---|
| Reflect shadow `telemetry:` block | `reviewers_requested/resolved/complete` from manifest plus events, `findings_block_compliance_rate` from `first_parse_ok`, `identity_source` and `identity_mismatch_suspected` from `model_observed` vs `model_resolved` (replaces the self-report comparison, SKILL.md:348) |
| `metrics.json` / `runs.jsonl` | `token_usage`, `wall_clock_ms`, `wave_durations_ms` from usage rows and stage timestamps |
| `review-telemetry` store (`model_scores`) | one `reviewer_run` per reviewer event (role=reviewer) after export; outcomes from a judge step with a uniqueness rule (section 2) |
| E2-style study rows (`found_14`, `output_tokens`, `elapsed_s`, `overhead_pct`) | sums over events by role; `elapsed_s` including retries and re-asks (R-24) is the span from first `seq` to last |
| Spec review loop | `round` plus ledger sha pointers per round |
| PR code review (future) | same events; `artifacts` carry diff and citation pre-check pointers (`precheck.json`) |

### 8.5 Alternatives considered
- Extend `review-telemetry/1` only: it already has the cost group and the SQLite loader, but it has no non-reviewer kinds, no stage, no pointer fields and no writer, and it lives outside the run directory. Needs `/2` (add `agent_run` with `agent_role`), value type checks (D-31) and the uniqueness rule (D-17). Recommended as the cross-run store, not as the per-run record.
- Extend the manifest with `usage` per attempt: smallest change (store the payload instead of its hash, manifest.py:353), but the manifest is one JSON file rewritten on every call and so inherits D-23; it also holds no orchestrator or calibrator rows because `PER_REVIEWER_STAGES` is `dispatched, collected, calibrated` (manifest.py:53). Rejected as the run record; kept as the state machine.
- Keep the five E2 schemas: rejected, they differ in key names and units (section 5.2).
Confidence in the split "append-only events per run + manifest state machine + telemetry store as export" is moderate-high; the transcript adapter's availability across harnesses is the open dependency (gap 3).

## 9. Item (d): cost accounting across reviewers and stages

### 9.1 What the evidence shows
- Reviewer-only accounting under-reports. E1 combos: orchestrator-alias share of output tokens 0.38 to 0.87, median 0.59 (section 4.4), so the non-orchestrator share is 0.13 to 0.62 and understated in B-D (the alias also served the SONNET class). A cost-per-confirmed-TP built from `reviewer_runs` alone would exclude the majority of tokens.
- Units disagree: telemetry = tokens in/cache/out + wall_s per reviewer; E2 = output tokens (some split by reviewer/sweeper/phase 2/re-ask); reflect metrics = orchestration vs agents vs auggie totals (estimates); E1 = harness-alias tokens and estimated USD.
- Re-asks, retries and fallbacks are cost: E2 R2 books `reask` tokens, R3 `phase2` and `reask` (section 5.2); the E1 run of combo E (E1) that re-dispatched reviewers (7 reviewer-agent calls vs 3) is invisible in the contract (slice 11 2.4, [UNVERIFIED by me]). Killed sessions: E2 R3 records zero tokens for killed sessions (slice 08 I10, [UNVERIFIED by me]); the proposal records `usage_complete: false` instead of 0.

### 9.2 Rules for the run record
1. Cost lives only on event rows, one row per agent attempt (including retries, re-asks and killed attempts); outcomes and verdicts carry no cost column. This removes the D-17 fan-out by construction.
2. Report two bases side by side, always labelled: reviewer-only (`agent_role=reviewer`) and all-stages (every role including orchestrator, calibrator, debater, validator, judge, helper). A study states which basis its "cost per TP" uses.
3. Roll up by `(stage, agent_role, model_observed)`; keep `model_requested` beside it so a collapse like A3 (requested `None`, served Sonnet x3) shows as a mismatch row instead of a clean-looking rotation.
4. Tokens are the primary unit (all four counters); USD is allowed only as `usd_estimate` with its source named, never summed as a fact (FINDINGS.md:37).
5. Wall time per attempt plus run `elapsed_s` as span; the E2 SLO (R-24) is computed on the span, which includes retries and re-asks.
6. Do not sum `model_scores` cost over `truth_basis` (section 2, case c4).

Key Takeaways
- One event row per agent attempt, cost only there, two labelled cost bases, truthful values only from transcripts.

## 10. Open items resolved
| Item | Status | Where |
|---|---|---|
| (a) one run-record design (fields, writer, location) | Resolved as a proposal | section 8 |
| (b) can study telemetry carry anchors given telemetry.py forbids text | Resolved: no; carry sha/`lid`/`fp` pointers into the ledger; type-check group values | 1.4, 8.3 |
| (c) execute-free reproduction of D-17 and D-23 | Resolved: D-17 reproduced (c2: 400 vs 200 per TP); D-23 reproduced by deterministic interleaving; no real two-process race run; no observed incident in 29 manifests | sections 2, 3, 7 |
| (d) cost accounting across reviewers and stages | Resolved as rules plus evidence; per-agent historical cost is NOT recoverable from E1 data | 4.4, 9 |

## Gaps and Questions
1. [UNVERIFIED] Real concurrent invocation of `review manifest advance`: only the deterministic load/modify/save interleaving was run. Searches tried: scan of 29 manifests (section 7), reading `manifest_cmd.py:160-215`. No audit-log evidence of parallel Bash calls was searched for.
2. [UNVERIFIED] Whether Claude Code prices a gateway alias by the alias name or by the served model; `usd` in E1 `usage` is therefore not interpretable (FINDINGS.md:37 only says "estimate from model names"). Searched: `extract.py:70-73` (copies `costUSD`), `FINDINGS.md`.
3. [UNVERIFIED] Whether per-agent token usage is obtainable for every harness: E1 extract.py reads only the run-level `modelUsage` and per-call served model (section 4.4); E2 reads session transcripts (slice 07 B-side claims, cited from slices, not re-read here). The transcript adapter in section 8.2 needs a per-agent usage source; searched `extract.py` only, and did not read E2's `collab_summary.py`/`values.py` (git `show` not run on them).
4. [UNVERIFIED] The p13 harness telemetry writer and `finalize-review.py` were identified by grep only (section 1.2).
5. [UNVERIFIED] Slice claims cited without re-derivation: `test_review_telemetry.py:156-163` privacy test; slice 11 memory line 58 and 64; "killed-session tokens counted 0" (slice 08 I10); E1 re-dispatch count 7 vs 3; orchestrator `wall_clock_ms` vs measured minutes. Slice 07/08 were read only for their first pages (up to R2 part B8 and S5 heading); design-review findings for R4/R5 (slice 08 later pages) were not read.
6. Question: should the manifest also gain a `rev`/flock now (cheap) even if events become the per-run record? It removes D-23 for stage commits, which events do not cover.
7. Question: is `review-telemetry/2` acceptable (bumps `SCHEMA_VERSION`, telemetry.py:17, and makes E3 harness records `/1` read-only legacy), or must `/1` stay writable?
8. Question: who owns the transcript adapter and where does it live, given the CLAUDE.md rule that installed primitives must not reference `src/superclaude/` paths (package CLI code is reached through the `superclaude` CLI)? `review record add` would be CLI code; the adapter script is a harness-side input.
9. Question: memory (`deviation-patterns-*`) is a tracked, LLM-merged file; should the unified panel write it only at publish by a script, keyed by run id, with a study-mode switch to freeze reads (section 6.2)?

## Stale Documentation Found
- **[STALE DOC]** `telemetry.py:3` "No document text, quote, anchor or claim ever enters a record": [CODE-CONTRADICTED] as an enforced invariant; only `context` values are constrained (telemetry.py:243-251); group values are unchecked (:213-225).
- **[STALE DOC]** `manifest.py:3` "One coordinator writes the manifest": [UNVERIFIED] as enforced; nothing prevents concurrent CLI calls (section 3).
- **[STALE DOC]** SKILL.md:592 "single-owner file, overwritten whole" for `last-pass-{slug}.md`: [CODE-CONTRADICTED] by the live file, which holds 5 `# last-pass` entries (lines 1, 7, 14, 20, 28).
- **[STALE DOC]** SKILL.md:1721-1824 `metrics.json` / `runs.jsonl` "emits" and "appends": [UNVERIFIED] as code; no Python writer exists in `src/` or `scripts/`; real values observed are orchestrator estimates (section 4.3).
- **[STALE DOC]** `shadow-model-combos/PLAN.md:1,3` and `combos.json:4` "designed, NOT run" next to 15 completed runs (slice 11 2.1, [UNVERIFIED by me]).
- **[STALE DOC]** `review telemetry` store described as the review loop's telemetry, yet written only by E3 experiment harnesses (`.dev/research/346-review-loop-experiments/...`), not by the shipped CLI (section 1.2).
- Contract `telemetry:` fields `calibrator_diversity`, `t2_model_class_diversity`, `identity_source` etc. describe requested rotations, not served models ([CODE-CONTRADICTED] by A3, section 4.4).

## Summary
The review package has no shipped telemetry writer: `review-telemetry/1` is reviewer-session-centric, counts-only, and was fed by E3 experiment harnesses; reflect's `telemetry:`, `metrics.json` and `runs.jsonl` are LLM-authored estimates, the manifest stores only hashes (attempt payloads are discarded), and E2 produced five incompatible result-row schemas whose only shared cost unit is output tokens. D-17 reproduces (two live outcomes for one run double the cost: 400 vs 200 per TP) and D-23 reproduces as a lock-free load-modify-save, with no incident observed in 29 real manifests (9 show a protocol omission of `dispatched` attempts instead). One run-record design is proposed: an append-only per-run `events.jsonl` (one row per agent attempt, cost only on those rows, truthful usage and observed model from a transcript adapter, hash pointers instead of text so anchors never enter telemetry), the manifest kept as the state machine with a lock, and `review-telemetry` as the cross-run export written by one step at publish. Cost should be reported on two labelled bases (reviewer-only and all-stages) because E1's orchestrator alone carried a median 0.59 of output tokens.



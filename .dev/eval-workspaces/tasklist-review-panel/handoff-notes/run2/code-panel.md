# Code-panel notes (run 2) — review panel / telemetry / reviewer brief / reflect Tier 2

Repo: /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel (branch ironbelly/eval-tasklist-review-panel)
Date: 2026-11-13. Read-only investigation. Paths below are relative to repo root unless absolute.
Independence: did not open /tmp/handoff-notes/ or any HANDOFF-review-panel-unification*.md.
All file:line citations verified by Read in this session unless marked UNVERIFIED.

## 1. Panel config: schema, tiers, slots, resolution

Files: src/superclaude/cli/review/panel.py (525 lines), panel_cmd.py (87), data/review-panel.default.json, data/review-panel.live7.json, data/review-tiers.default.json.

### Schemas
- Three schema ids: `review-panel/1`, `review-tiers/1`, `review-panel-resolution/1` (panel.py:25-27).
- Panel template keys (closed set): schema, template_id, version, description, distinct_across_slots, apply_to, slots (panel.py:37-45). Slot keys: slot_id, tier, count, strategy, seed (panel.py:46).
- Panel validation rules (validate_panel, panel.py:64-144): template_id `^[a-z0-9][a-z0-9-]{0,31}$` (:74-77); semver version (:78-79); distinct_across_slots bool (:80-81); apply_to non-empty subset of first/re-review (:84-91); slot_id `^[a-z0-9]{1,8}$`, unique (:112-118); tier `^tier[0-9]{1,2}[a-z]?$` and must exist in tier file when tiers given (:119-123); count 1..4 (:124-128); strategy fixed|random|round_robin (:35, :129-135); seed only with random (:136-139); exactly ONE fixed slot = "the anchor" (:140-141); total reviewers 1..8 (:142-143).
- Tier file (validate_tiers, panel.py:147-254): `aliases.<tierN>` = {alias, models[], placeholder?}; alias string is the gateway picker id (`claude-gw-tierX[1m]`); placeholder tier must have models == [] (:175-183); names map id->display (:192-196); environments.<name> = {available: "all"|[ids], stand_ins: {tier: [ids]}, launch: {model id: launcher string}, note} (:197-253); stand-in ids must be in `available` (:238-243).
- Model id regex `^[A-Za-z0-9._/:\-\[\]]{1,128}$` (panel.py:34).

### Loading / lookup precedence
- find_path: explicit path > env var SUPERCLAUDE_REVIEW_PANEL / SUPERCLAUDE_REVIEW_TIERS > <git toplevel>/.superclaude/review-<kind>.json > ~/.superclaude/review-<kind>.json > packaged default (panel.py:277-299, packaged fallback at :335-340, :351-356).
- `@NAME` loads packaged `data/review-panel.<NAME>.json` (panel.py:310-324, :327-334). `@` works through --template OR the SUPERCLAUDE_REVIEW_PANEL env var (:328). No `@` form exists for tier files (load_tiers :350-362).
- Whole-file replacement only (panel_cmd.py:24, :31 help text) — no merge/overlay of a partial override.

### Environment selection
- select_env (panel.py:365-374): `--env` > `$SUPERCLAUDE_REVIEW_ENV` > `gateway` if `$T3Model01` non-empty > `anthropic-only`.
- In this shell T3Model01=glm-5.3, T2bModel01=gpt-6.1-terra, SUPERCLAUDE_REVIEW_ENV unset → default env is `gateway`. With T3Model01 unset → `anthropic-only` (observed, see runs below).
- Environments defined: `gateway` (available "all", no stand-ins, launch {} — note: "dispatch mechanism per model not defined yet", review-tiers.default.json:19-24) and `anthropic-only` (available opus/sonnet/haiku/fable 5.x, stand_ins tier2/2b/3/4 -> haiku, launch map to `opus|sonnet|haiku|fable`, review-tiers.default.json:25-30).

### Resolution algorithm (resolve, panel.py:427-525; resolve_slot :380-418)
- Fixed slots first, then the rest, in template order (:447-450). If review_kind not in panel.apply_to → ONLY the fixed (anchor) slot, count forced to 1 (:449-454, :464). Both packaged templates set apply_to ["first"], so a `re-review` resolves to a single Tier 1b reviewer (observed below).
- Base seed = given --seed or first 8 hex of sha256(run_id) (:455-459). random slot seed string = `<slot.seed or base>|<slot_id>|<i>` (:467-470); round_robin seed = (--sequence or today's date ordinal) + i - 1 (:471-476) → round_robin is date-dependent unless --sequence is given (non-reproducible across days).
- resolve_slot: candidates = tier models ∩ available; if empty, environment stand-ins ∩ available, stand_in=True; if still empty → NoModelAvailable (:393-401). fixed → first candidate (:402-403); random → random.Random(seed).choice(pool) where pool excludes models already chosen if distinct_across_slots, BUT falls back to the full candidate list when exclusion empties the pool (:405-406, :408-409).
- reviewer_id = `<slot_id>-<i>` (e.g. `t1b-1`, `t3-2`) (:500). Each reviewer record: reviewer_id, slot_id, tier, alias, strategy, seed, model, model_name, fallback_depth, stand_in, fallbacks, launch (:498-513). Output adds template/tier version + sha256 of each, environment, run_id, review_kind (:514-525).

### Model-by-tier table (data/review-tiers.default.json:4-11; names :12-17)
| tier | gateway alias | models (order = default then fallbacks) |
|---|---|---|
| tier1a | claude-gw-tier1a[1m] | claude-opus-5-5, claude-sonnet-5-5 |
| tier1b | claude-gw-tier1b[1m] | claude-sonnet-5-5, gpt-6.1-sol, muse-wonder-full-1.0 |
| tier2 | claude-gw-tier2[1m] | gpt-6.1-sol, glm-5.3, grok-4.7, Qwen3.8-max, muse-wonder-1.0, muse-spark-1.3 |
| tier2b | claude-gw-tier2b[1m] | gpt-6.1-terra, glm-5.3, Qwen3.8-max, muse-wonder-1.0 |
| tier3 | claude-gw-tier3[1m] | glm-5.3, Qwen3.8-max |
| tier4 | claude-gw-tier4[1m] | gpt-6-luna, claude-haiku-5-5, grok-4.7 |
- `claude-fable-5-1` is in names and anthropic-only `available`/`launch` but in no tier list (review-tiers.default.json:14, :27, :29).

### Templates
- @default (review-panel.default.json:1-13): 4 reviewers — t1b x1 fixed (anchor), t2 x1 random, t3 x2 random; distinct_across_slots true; apply_to ["first"].
- @live7 (review-panel.live7.json:1-15): 7 reviewers — t1b x1 fixed, t2 x1, t2b x1, t3 x2, t4 x2 (all random); description says the claude-gw-tier2b alias must exist on the gateway before it runs live (:5).

### Hard-coded model ids
- In panel.py: none. Only hard-coded env name strings `gateway`/`anthropic-only` and env var `T3Model01` in select_env (panel.py:372-374).
- All model ids live in data/review-tiers.default.json (data, packaged).
- Telemetry hard-codes strata `sonnet`/`haiku` (telemetry.py:112-115) — model-family names baked into the schema.

### T2bModel01 handling
- `T2bModel01` is NOT referenced anywhere in src/ or tests/ (Grep across repo excl. .dev/eval-workspaces: only CHANGELOG.md:9 mentions T2bModel01-T2bModel04 as ccsession-models.json data). The panel code reads only `T3Model01` (panel.py:372) and only as a "this is the gateway" sniff; it never reads any TxModelNN value to pick a model.
- Consequence: tier model lists in the JSON can diverge from the gateway's slot env vars. Observed live: env T3Model01=glm-5.3, but @default/gateway resolved both t3 reviewers to Qwen3.8-max (below). Whether the gateway alias `claude-gw-tier3[1m]` can be steered to a specific underlying model is UNVERIFIED; gateway `launch` map is empty (review-tiers.default.json:23) so the resolution gives no launcher string for any gateway model.

### `panel resolve` output (run 2026-11-13, --run-id handoff-run2, base seed 3430211612)
default / gateway:
  t1b-1 tier1b fixed  claude-sonnet-5-5 depth0 launch None
  t2-1  tier2 random  glm-5.3 depth1 launch None
  t3-1  tier3 random  Qwen3.8-max depth1 launch None
  t3-2  tier3 random  Qwen3.8-max depth1 launch None   <-- duplicate despite distinct_across_slots=true
default / anthropic-only:
  t1b-1 claude-sonnet-5-5 launch sonnet; t2-1, t3-1, t3-2 claude-haiku-5-5 stand_in=True launch haiku
live7 / gateway:
  t1b-1 claude-sonnet-5-5; t2-1 glm-5.3; t2b-1 muse-wonder-1.0 (depth3); t3-1 Qwen3.8-max; t3-2 Qwen3.8-max (dup); t4-1 claude-haiku-5-5 (depth1); t4-2 gpt-6-luna; all launch None
live7 / anthropic-only:
  t1b-1 sonnet; t2-1, t2b-1, t3-1, t3-2 haiku stand_in=True; t4-1, t4-2 haiku stand_in=False depth1 (haiku is in tier4's own list)  → 1 Sonnet + 6 Haiku, matches live7 description (review-panel.live7.json:5)
default / gateway / --kind re-review: single reviewer t1b-1 claude-sonnet-5-5 (anchor only).
No --env, T3Model01 unset: environment anthropic-only.
template_sha256: default fd2ef963…146ba, live7 191ea47f…48a848; tiers_sha256 1a2a8ad2…f3a49 (tiers_version 1.0.0).

Why the duplicate: after sonnet+glm chosen, tier3 pool minus {glm} = {Qwen}; second t3 pool minus {glm,Qwen} is empty → falls back to full candidate list (panel.py:405) → random may pick Qwen again. "distinct" is best-effort, silent.

## 2. Telemetry

Files: telemetry.py (447), telemetry_cmd.py (98).
- Schema `review-telemetry/1` (telemetry.py:17). Two record kinds: `reviewer_run` and `outcome` (telemetry.py:204, :256, :265-266). Docstring promise: no document text, quote, anchor or claim ever enters a record (telemetry.py:3); enforced partly by `context` values limited to short labels/numbers (:240-251).
- reviewer_run top keys: schema_version, kind, record_id, ts_utc, run_id, step, round, reviewer_id (telemetry.py:82-91) + groups (telemetry.py:30-81):
  - panel: template_id, template_version, template_sha256, tiers_version, tiers_sha256, environment, panel_size
  - slot: slot_id, tier, alias, strategy, seed, fallback_depth, stand_in
  - model: resolved, launch, observed
  - task: doc_sha256, doc_bytes, doc_lines, language, doc_format, specialization, sections, max_heading_depth, tables, table_rows, ids_defined, cross_refs, rfc2119, review_kind
  - output: block_ok, findings, blocking, by_severity{CRITICAL,MAJOR,MINOR}, verdict, verdict_mismatch
  - cost: tokens_in, tokens_cache_read, tokens_cache_write, tokens_out, wall_s
  - plus required `context` object; optional `supersedes`, `stratum` (:205-206).
- outcome keys: schema_version, kind, record_id, ts_utc, run_id, reviewer_record_id, truth_basis, confirmed_tp, false_pos, unconfirmed, unique_tp, overlap_mean_jaccard, recall_vs_confirmed, precision, cost_per_confirmed_tp, supersedes (+ stratum) (telemetry.py:92-110). truth_basis ∈ catalog-v1|theme-v1|adjudicated-v1 (:18, :263-264). stratum ∈ sonnet|haiku, "never pooled" (owner decision D3) (:112-115, :267-268).
- task variables computed from the document by `task_variables` (telemetry.py:142-190): doc_format always "markdown" (:180), language "en" if stop-word share ≥2% (:179).
- Files: append-only JSONL under `<dir>/records/YYYY/MM/<run_id>.jsonl` (reviewer runs) and `<run_id>.outcomes.jsonl` (outcomes); reuses an existing file for the run in any year/month (telemetry.py:287-307). Default dir `.dev/benchmarks/review-telemetry` or $SUPERCLAUDE_REVIEW_TELEMETRY_DIR (telemetry_cmd.py:12, :43-47).
- SQLite: tables reviewer_runs (flattened `<group>_<key>` columns, by_severity split into 3 cols, context_experiment/arm/replicate/json) and outcomes; view `model_scores` grouped by model_observed, slot_tier, slot_stand_in, stratum, truth_basis with n_runs, sums, mean precision/recall, cost_per_confirmed_tp = SUM(cost_tokens_out)/SUM(confirmed_tp); superseded records excluded; outcome joined only when stratum matches (telemetry.py:313-379, :382-447). Loader reports `stratum_conflicts` (:438-443).
- CLI: `superclaude review telemetry taskvars DOC`, `append --record FILE`, `load --db FILE` (telemetry_cmd.py:20-98).
- Who writes it: NOBODY in the shipped product. merge_cmd.py imports only ledger (merge_cmd.py:10) and has no telemetry call; panel_cmd.py imports only panel (panel_cmd.py:10). Grep for append_record/task_variables in src/ finds only telemetry.py/telemetry_cmd.py; callers are tests/review/test_review_telemetry.py and .dev/research/346-review-loop-experiments harnesses (e.g. p22/harness/harness_j3.py:587, p18/ab5/full.py:219, p13/ab1/report.py:135). No skill/command instructs `review telemetry append` (see section 4 grep).
- Gap: `model.observed` (actual model served) has no producer in the product; model_scores groups by it (telemetry.py:364, :378), so the view is empty unless an external harness fills it.

## 3. The reviewer brief

Where: src/superclaude/rules/prompts/document_review_loop_prompts.md (74 lines), installed to `~/.claude/rules/prompts/document_review_loop_prompts.md`. The only consumer in src is `/sc:spec-panel` (`--mode critique`): spec-panel.md:266-268 makes reading it a hard gate ("if it cannot be read, return `incomplete`"). The prompts file self-describes its scope as `/sc:spec-panel --mode critique` (prompts:3).

Key text (line numbers verified):
- prompts:17-21 values to fill: `{{CANDIDATE}}`, `{{BASELINE}}`, `{{PRIOR}}`, `{{N}}`, `{{IDS}}` — nothing else.
- prompts:31 grading check: "An implementer who follows the stated text as written builds X, and X is wrong because Y." Blocking = "two stated texts that contradict each other, a stated text that causes data loss or breaks a security or safety boundary, or a stated text that an acceptance criterion cannot pass." Medium = needs a guess OR "a requirement the document never states (a missing restriction, an undefined state, an unspecified edge case)". "A Medium finding goes under follow-up candidates even when its label is MAJOR."
- prompts:32 FIRST-REVIEW brief: "Review the candidate {{CANDIDATE}} (sha256 of the file) against the requirements it states, review 1 of 3. Inspect behavior and the dependencies it touches. Report concrete wrong outcomes, not a minimum number of findings. Minor findings are notes and never fail the review; list Medium and minor findings under follow-up candidates. If an input is missing or unreadable, return incomplete. Do not edit the candidate and do not start another review. State what you covered."
- prompts:39-46 RE-REVIEW roles table, Step 1 `diff -w BASELINE CANDIDATE` evidence block, review-number rule, grep self-check.
- prompts:48 RE-REVIEW brief (re-check prior blockers resolved/open/regressed; "Record a severe defect you newly discover even if it is older").
- prompts:53 REVISE brief: "Repair only the blocking findings {{IDS}} ... Prefer deleting or narrowing ... cite the finding id on every addition ... do not award yourself a PASS."
- prompts:58-62 findings block contract: `## Findings block`, one fenced block info `findings-v1`, JSON per line: id, severity CRITICAL|MAJOR|MINOR, blocking bool, category (contradiction, unpassable-check, data-loss, safety, missing-requirement, other), anchor 12-200 chars "copied exactly from the candidate: the text that is wrong", anchor2 for contradictions, refs (requirement ids / section numbers), claim one sentence. Prior lines `{"prior": "L3", "status": ...}`.
- prompts:66 fixmap-v1 contract for the reviser.
- prompts:68-70 "Review panel": run `superclaude review panel resolve --run-id <loop id> --kind <first or re-review>`; "each in a fresh context with the same brief, none seeing another's report or transcript"; merge with `superclaude review merge` (also for one reviewer); `superclaude review ledger revise ...` after each revision; "Only these scripts change a finding's status"; if `superclaude` not installed, run one reviewer.
- prompts:74 "Never" list (no "any finding is FAIL", no finding quotas, no "apply all findings").

What the brief does NOT say:
- No source/driving document. The first-review brief reviews the candidate "against the requirements it states" (prompts:32); the fill-in list has no SOURCE/SPEC/ROADMAP placeholder (prompts:17-21). A tasklist cannot be checked for traceability to its roadmap/spec under this brief. (`refs` may carry requirement ids, prompts:60, but the brief never says where they come from.)
- No anchor guidance beyond "copied exactly ... the text that is wrong" (prompts:60). Not said: what to anchor for a `missing-requirement` finding (the wrong text by definition is absent); that matching is whitespace-flattened (code: findings.py:82, :272-273) but otherwise exact (markdown `**`/backticks must be copied); that the anchor should be unique (code takes the first match and only flags ambiguity, findings.py:349-352); what happens on a miss (span None, section "none", findings.py:358 — clustering then rests on refs only).
- No severity definitions. CRITICAL/MAJOR/MINOR are an enum (prompts:60) with no meaning given in the prompts file; the grading check defines blocking vs Medium vs minor-note (prompts:31-32) but "Medium" is not a severity value (it is MAJOR + blocking=false). spec-panel.md:259 gives a different rule: "CRITICAL is blocking; a MAJOR ... is blocking only if ...", i.e. label-driven for CRITICAL, while prompts:31 requires the grading sentence for every blocking finding. Code accepts CRITICAL + blocking=false and forbids only MINOR + blocking=true (findings.py:100-101).
- "Blocking" meaning: defined only by the grading check (prompts:31). Its operational consequence (one blocking row from any single reviewer fails the round, ledger.py:187, :99-104, :273-274) is not told to reviewers; nor that the merge, not their own verdict, decides (prompts:62 "The verdict line stays the reviewer's verdict" — but merge ignores it).
- No reviewer persona/lens, no panel size or model told to the reviewer, no coverage target, no output path, no sha256 placeholder name (text says "(sha256 of the file)" inline, prompts:32, :48).
- Ordering conflict: spec-panel.md:260 "a critique-mode report's last line is `verdict: PASS`|`FAIL`" and spec-panel.md:263 "Reviser brief just above the final verdict line" vs prompts:58 "The last section of every review report is `## Findings block`". Parser tolerates trailing text after the fence (findings.py:45-76), so harmless to code; confusing to reviewers.

## 4. Roles and the files that drive them

| role | driven by | input | output |
|---|---|---|---|
| Orchestrator / coordinator | spec-panel.md:256-268 (Review Loop + hard gate) + prompts:68-70 | user command, review count, prior report, baseline copy | spawns reviewers, runs CLI scripts; keeps count (spec-panel.md:261) |
| Panel resolver | `superclaude review panel resolve` (panel_cmd.py:18-66 → panel.py:427-525) | template + tier file + env + run-id + kind | review-panel-resolution/1 JSON (reviewer_id, model, launch, ...) |
| Reviewer | prompts:31-33 (first), :37-49 (re-review); agent type NOT specified ("fresh context", prompts:70) | candidate (+baseline, prior) | report with `review: N of 3` header + `## Findings block` findings-v1 |
| Calibrator | NONE in this loop. Ledger `confidence` single/overlap is computed (ledger.py:86-90) and printed (ledger.py:435) but never used in verdict | — | — |
| Merge / judge | deterministic script `superclaude review merge` (merge_cmd.py:21-118) → ledger.merge_round (ledger.py:107-298) + render_merged_report (ledger.py:408-494) | reports `REVIEWER_ID=PATH`, doc, round, optional --resolution | ledger (review-ledger/1, atomic save ledger.py:52-67), merged report md, JSON {verdict, decision, brief_ids, new, refound, regressed, cleared, clusters, block_ok, warnings} |
| Reviser | prompts:53 + REVISER_RULES restated in merged report (ledger.py:22-26, :487-493) | merged report's Reviser brief ids | revised candidate + `## Fix map` fixmap-v1 (prompts:66) |
| Revision recorder | `superclaude review ledger revise` (ledger_cmd.py:36-71 → ledger.apply_revision ledger.py:301-347) | ledger, old/new candidate, reviser output | rows applied+touched → resolved_check; spans remapped |
| Human | escalation at review 3 (prompts:13; merged report "## Escalation", ledger.py:475-486); `ledger defer` "Human command" (ledger_cmd.py:74-91, ledger.py:350-360); follow-up-issue question (spec-panel.md:260) | open blocking rows | defer / decide |
| Telemetry writer | NONE in product (section 2) | — | — |

Data contracts between them:
- resolution JSON → merge: `--resolution` maps reviewer_id → model (merge_cmd.py:74-83). A `--report` id that is not in the resolution silently gets model None (merge_cmd.py:94). Only `model` is carried; tier/stand_in/launch are dropped.
- reviewer report → merge: findings-v1 parsed by findings.parse_block (findings.py:124-196); invalid block → that reviewer still contributes parsable findings but `block_ok` false (ledger.py:128-134); a round with no valid block is refused, ledger unchanged (ledger.py:150-157).
- merge internals: annotate (anchor→span, section, refs_norm, fp = sha256("v1|section|refs")[:16]) (findings.py:340-360); cluster by union-find on same_defect (fp match with non-empty refs, or overlapping refs/none-both + spans within 3 lines) (findings.py:367-407); match cluster to existing row; new row blocking = any member blocking (ledger.py:187); refound row blocking = current round's classification (ledger.py:213-218); resolved/resolved_check row refound → regressed (ledger.py:235-238); resolved_check not refound → resolved (ledger.py:254-258); reviewer prior lines are notes only (ledger.py:259-272).
- verdict: FAIL iff any blocking row is open/regressed (ledger.py:99-104, :273-274); decision PASS / REVISE (n < cap) / ESCALATE (ledger.py:93-96). `ledger verdict` exit codes 0/10/11 (ledger_cmd.py:13, :94-109).
- reviser output → ledger revise: fixmap-v1, with markdown-table fallback for `| L3 | applied` rows (findings.py:199-223); `--old` must hash-match the reviewed round (ledger.py:308-314).
- capture matrix review-capture/1 per round (ledger.py:375-401, ledger_cmd.py:112-137) — the input shape used by the study, not by the loop.

## 5. Reflect Tier 2 vs this panel

| aspect | reflect Tier 2 (sc-reflect-protocol) | review panel (cli/review + prompts) |
|---|---|---|
| purpose | UC-1 pre-execution coverage of a tasklist vs its spec; UC-2 post-execution deviation audit (SKILL.md:37-40) | document critique review loop for /sc:spec-panel (prompts:3) |
| reviewer agent | fixed read-only `reflect-reviewer` agent for all reviewers (SKILL.md:598; reviewer-spec.md:84); agent pinned `model: sonnet`, read-only tools (reflect-reviewer.md:5-8) | unspecified "fresh context" (prompts:70); no agent file |
| roles | Tier-1 card (root-cause-analyst / self-review / requirements-analyst), N reviewers, calibrator per card, sc-adversarial merge, evidence-validator gate (SKILL.md:578-592; wave map :138-165) | reviewers, deterministic merge script, reviser, human; no calibrator, no validator |
| model selection | count from distinct `ANTHROPIC_DEFAULT_*_MODEL` aliases (SKILL.md:231-239); rotation sonnet/haiku/(qwen|kimi|deepseek else opus) (SKILL.md:604-608; reviewer-spec.md:94-98); executor-class exclusion (SKILL.md:600-610). CLI wrapper path uses T2Model01..09 swarm slots and T1Model01/02 fallback ladder (ensemble.py:7, :154-198) | tier JSON + template slots + env (panel.py:427-525; review-tiers.default.json) |
| persona | analyzer / qa / refactorer (/architect) via brief (SKILL.md:604-608) | none |
| brief | per-reviewer file `<output>/reviewer-briefs/reviewer-<N>.md`, exactly 3 sections: T1 card excerpt, Grounding hunks, Coverage slice (reviewer-spec.md:21-74; SKILL.md:302); D13 UC-1: spec body injected for qa persona (reviewer-spec.md:55) | same brief text for all reviewers (prompts:32/48/70) |
| finding format | markdown Deviations table: #, Category (Authorized expansion / Necessary deviation / Drift / Regression), Location, What diverged, Evidence file:line, Severity HIGH/MEDIUM/LOW (reflect-reviewer.md:71-99) + advisory Correctness gaps table (:101-115) | findings-v1 JSON lines: id, severity CRITICAL/MAJOR/MINOR, blocking, category, anchor (exact quote), anchor2, refs, claim (prompts:60) |
| grounding unit | `file:line` citation | exact text anchor quote |
| calibration | blind `confidence-calibrator` per card, calibrator class disjoint from reviewer classes (SKILL.md:1172-1192; reflection-rubric.md:133-149); 5-dim arithmetic mean (reflection-rubric.md:9-13) | none |
| merge | `sc-adversarial-protocol` Mode A `--compare`; reflect must not synthesize its own merge; `merge_method ∈ {adversarial, single-reviewer-fallback}` (SKILL.md:633, :789, :310-314); judge class owned by sc-adversarial (SKILL.md:612) | deterministic clustering + any-blocking rule (ledger.py:107-298) |
| final gate | evidence-validator re-Reads every citation, drops unfounded (SKILL.md:1159-1170) | none (anchor found/missing is recorded, findings.py:350, but not gated) |
| loop | no fix loop; Tier 3 remediation handoff opt-in (SKILL.md:164) | review → revise → re-review, cap 3 (prompts:13; ledger.py:93-96) |

Mismatches inside reflect worth noting:
- confidence-calibrator.md is written for troubleshoot: description and triggers name only sc:troubleshoot (confidence-calibrator.md:3, :15), Responsibilities hard-code "the 6 dimensions" and a gated-min formula (:61, :67), rubric_path = `refs/escalation-rubric.md` (:48). Reflect expects a 5-dimension arithmetic mean from refs/reflection-rubric.md (reflection-rubric.md:9-13) and lists the calibrator as "Blind re-grade per the 5-dim reflection rubric" (SKILL.md:583).
- reflect-reviewer is described as UC-2 only (reflect-reviewer.md:3, :15; SKILL.md:592) and its output format is the UC-2 deviation taxonomy, yet SKILL.md:598 spawns all Tier-2 reviewers as this agent, and UC-1 Tier 2 is reachable (reviewer-spec.md:55 D13 UC-1 qa persona). UC-1 (the tasklist pre-review that sc-tasklist Stage 10.5 and sc-workflow Wave 4 use) has no matching reviewer finding format.
- reflect-reviewer.md:6 pins `model: sonnet`; how the non-Claude rotation classes (qwen/kimi/deepseek) are run as this agent is UNVERIFIED in the skill text read.

## 6. Defects / gaps (severity is a guess)

1. HIGH (tasklist use) — Brief has no driving/source document: prompts:32 "against the requirements it states"; placeholders prompts:17-21. A tasklist review cannot check roadmap/spec coverage.
2. HIGH (tasklist use) — Tasklist task ids `T<PP>.<TT>` (sc-tasklist-protocol SKILL.md:1136) are not recognised as refs: `_REF_TOKEN` requires `[A-Z]{1,4}-[0-9]` (findings.py:29) and refs_norm keeps only token/section matches (findings.py:328-337). Verified: refs ["T01.02","R-012","3.2","AC-1"] + claim "task T03.04 ..." → ['3.2','AC-1','D-0003','R-012'] (T01.02, T03.04 dropped). Fingerprints and clustering therefore lose the task id. Same token in telemetry (telemetry.py:23) → ids_defined/cross_refs undercount tasklists.
3. HIGH — Gateway resolution names a model it cannot enforce: gateway `launch` is {} (review-tiers.default.json:23; note :20 "dispatch mechanism per model not defined yet"), so every gateway reviewer has `launch: null` (observed). The tier alias string (e.g. `claude-gw-tier3[1m]`) is the only dispatch handle; in this shell T3Model01=glm-5.3 while resolution picked Qwen3.8-max for both t3 reviewers. Whether the gateway serves the resolved model: UNVERIFIED. TxModelNN slot vars (incl. T2bModel01) are never read (only T3Model01 as an env sniff, panel.py:372).
4. MEDIUM — distinct_across_slots silently falls back to duplicates when exclusion empties the pool (panel.py:405, :408). Observed: @default and @live7 gateway → t3-1 and t3-2 both Qwen3.8-max. No warning field in the resolution.
5. MEDIUM — Merge blocking is "any single reviewer said blocking" (ledger.py:187; verdict ledger.py:99-104, :273-274). With @live7 (7 reviewers, 6 Haiku in anthropic-only) one weak reviewer fails a round; `confidence` (overlap/single) is computed but unused (ledger.py:86-90). No calibration or vote.
6. MEDIUM — Re-review panel collapses to the single fixed anchor (apply_to ["first"], panel.py:449-454, review-panel.default.json:7, review-panel.live7.json:7), and a refound row takes the current round's blocking classification (ledger.py:213-218): one re-reviewer can downgrade a blocker the full panel raised.
7. MEDIUM — Severity/blocking rule conflict: spec-panel.md:259 "CRITICAL is blocking" vs prompts:31 grading check for every blocking finding; code allows CRITICAL non-blocking (findings.py:100-101 only forbids MINOR blocking).
8. MEDIUM — Telemetry is not wired: no product caller of append_record/task_variables (merge_cmd.py:10, panel_cmd.py:10 import no telemetry); only tests and .dev/research harnesses write review-telemetry/1. model.observed has no producer, so model_scores (telemetry.py:362-379) is empty without an external harness.
9. MEDIUM — confidence-calibrator agent is troubleshoot-shaped (6 dims, escalation-rubric, confidence-calibrator.md:3, :48, :61, :67) while reflect uses a 5-dim mean (reflection-rubric.md:9-13; SKILL.md:583).
10. MEDIUM — reflect-reviewer output is UC-2-only (reflect-reviewer.md:3, :71-99) but Tier 2 spawns it for every mode (SKILL.md:598) including UC-1 tasklist pre-review.
11. LOW — round_robin seed uses `date.today()` when --sequence is absent (panel.py:472-476): resolution changes by day; resolve_slot's docstring "Pure and deterministic" (panel.py:388) holds only for the slot function.
12. LOW — Missing-anchor findings get section "none" (findings.py:358); with shared refs they cluster via fp (findings.py:371) even when unrelated.
13. LOW — `--report` reviewer ids not present in the resolution get model None silently (merge_cmd.py:94).
14. LOW — Report-ending conflict (spec-panel.md:260, :263 vs prompts:58).
15. LOW — Telemetry strata hard-code `sonnet`/`haiku` (telemetry.py:112-115, :267-268): gateway-model runs cannot be stratified.
16. LOW — `claude-fable-5-1` is available/launchable in anthropic-only but in no tier list (review-tiers.default.json:14, :27-29).
17. LOW — sc-tasklist Stage 10.5 says reflect "offers a Tier-3 `task-builder` remediation" (sc-tasklist-protocol SKILL.md:1640) but reflect's default Tier-3 route is sc:workflow, task-builder only with --depth deep (sc-reflect-protocol SKILL.md:164, :588-589).
18. INFO — Reflect has two model-selection mechanisms (skill: ANTHROPIC_DEFAULT_*_MODEL aliases, SKILL.md:231; CLI: T2Model0N/T1Model0N, ensemble.py:7, :186-198) and neither reads review-tiers.default.json; the panel has a third. Three independent model registries.
19. INFO — Variant commands/skills (`/sc:spec-panel-ledger`, `-stoprule`, `-diffgate`, `sc-review-ledger`, `finding-grader`) are installed in ~/.claude (ls confirmed) but not in this branch's src/superclaude (only under .dev/experiments/346-validation/...). Their relationship to cli/review is UNVERIFIED (not read).

## 7. Tasklist-specific vs generic

- cli/review (panel, merge, ledger, findings, telemetry): fully generic markdown-document machinery. Nothing tasklist-aware: no phase/task structure, task ids not recognised as refs (defect 2), task_variables doc_format fixed "markdown" and specialization a free label (telemetry.py:142-190).
- Prompts file: generic but spec-shaped (implementer / acceptance criterion wording, prompts:31) and scoped to /sc:spec-panel (prompts:3). No tasklist brief exists.
- Grep of src/superclaude skills/commands/agents: `superclaude review` / findings-v1 / the prompts file are referenced only by commands/spec-panel.md:268 and the prompts file itself (prompts:70). No skill (sc-tasklist-protocol, sc-workflow-protocol, sc-reflect-protocol) invokes the review panel or ledger.
- Tasklist review that exists today goes through reflect, not this panel:
  - sc-tasklist-protocol Stage 10.5: one `/sc:reflect --mode pre --remediate` per phase file, in parallel, advisory/non-blocking (SKILL.md:1619-1646, command at :1630-1636; depth from deterministic COMPLEXITY_SCORE :1650-1652); terminal post-execution `superclaude reflect run ... --depth deep --fix --no-promote` task per phase (SKILL.md:1136-1162).
  - sc-workflow-protocol Wave 4: `/sc:reflect --mode pre --spec <pkg>/source.md --tasklist <pkg>/<id>.md`, advisory, never edits the plan (SKILL.md:58-64, :76-78).
- Generic "review loop" cap sentence ("at most 2 fix cycles (3 reviews) ... escalate") is copied into rf-qa.md:110, rf-qa-qualitative.md:110, MDTM templates (01_...:646, 02_...:657), several QA prompts and output-styles/pragmatic.md:227 — text only, none of them call the panel/ledger scripts.

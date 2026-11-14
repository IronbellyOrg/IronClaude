# Research: This session's Review Panel findings, lessons and decisions (scope slice 4 of 5)

**Scope:** documents recorded by the reflect Tier 2 panel / shadow-run session: `.dev/brainstorms/20261111T182026-reflect-tier2-panel-replacement/merged-requirements.md`, `.dev/tasks/done/TASK-WF-implementStages0-20261111-202912/artifacts/*`, `.dev/troubleshoot/shadow-failures-20261113014240/REPORT.md`, `.dev/eval-workspaces/shadow-model-combos/{PLAN,FINDINGS,results}.md`, `.dev/reflect/*shadow*/` run summary and `scripts/reflect_shadow_exit.py` output.
**Status:** Complete
**Date:** 2026-11-13

Path abbreviations used below: `MR` = `.dev/brainstorms/20261111T182026-reflect-tier2-panel-replacement/merged-requirements.md`; `ART` = `.dev/tasks/done/TASK-WF-implementStages0-20261111-202912/artifacts/`; `TS` = `.dev/troubleshoot/shadow-failures-20261113014240/REPORT.md`; `COMBO` = `.dev/eval-workspaces/shadow-model-combos/`. Every cite is a line read in this slice unless marked UNVERIFIED. These are documents; architectural claims inside them are doc claims, not code-verified by this slice unless tagged.

---

## 0. Reading notes per source (raw, appended as read)

### 0.1 MR (merged-requirements.md, 625 lines; read 1-145, 265-294, 400-420, 500-609)

- Frontmatter: `status: draft-for-owner-review`, adversarial convergence 0.882 but `adversarial_status: partial` (5 HIGH unaddressed at Round 2.5), independent check FAIL on 1 blocking + 11 minor, all fixed and "confirmed by grep only, not by a second independent review" (MR:7-10).
- Chosen architecture **C, Layered Review Kernel**: K1 Resolution (`review-panel-resolution/1` + PROPOSED hard exclusion, `classes`, `skipped_slots`/`excluded`), K2 Dispatch adapters (agent-session pre, swarm post), K3 PROPOSED `findings-v2` (superset of findings-v1), K4 deterministic `cluster_v2` as telemetry only, not the merge (MR:52-65). Reflect keeps briefs, per-card blind calibration, `/sc:adversarial` debate, evidence gate, rubric, contract builder (MR:23, 61).
- Rejected B (full spec-panel loop): ~290k round-1 tokens, drops blind calibration, the measured panel gain came from a revise loop reflect does not have (MR:40-50). D (dispatcher only) = Stages 1-3 of C, not a destination (MR:67-74). E' deterministic pre merge = deferred, needs contract 2.0.0 (MR:76-83).
- Reason 1: reviewer identity lives in three places today (reflect rotation table, `T2Model0N` env pool, panel tier file); finding shape in two (cards, findings-v1); merge in two (`/sc:adversarial`, `merge_round`) (MR:105). This is the core "unify" argument and is directly relevant to the overall goal.
- Reason 5: does NOT claim the PN1 spec-panel gain (15.7 vs 2.8 fixed defects) because that gain came from a revise loop on specs (MR:114).
- Depth x tier routing: panel only after final tier is 2; `--t2-engine` read only at Wave 3 start (MR:120); rules D1-D5 (MR:122). Recorded history: 37 of 38 pre runs escalated to T2, 34 by the parsed-sparse pre-filter because workflow sources carry no labelled requirement ids (MR:142). So T2 cost is the typical per-plan cost.
- Q6: panel ledger NOT used for reflect in Stages 0-4; reflect is single-pass; ledger `--cap 1` would record ESCALATE every blocking round (MR:273). Ledger is path-blind (bare `span`, one `doc_sha256` per round) (MR:273).
- Q7 code-level cap: reflect templates max 3 reviewers; raising needs T2 recall >= T1 recall + 15 pp (MR:289). Full panel (4+ slots) not worth it in anthropic-only (extra Haiku copies add no class) (MR:284-287, 500).
- Staged migration table Stage 0-6 (MR:406-414): Stage 0 exit = 50-pair hand-labelled cluster check, conversion share >= 90%, consumer grep stored, pilot designed and costed (MR:408); Stage 1 dormant kernel extensions + spike S-ID (MR:409); Stage 2 shadow exit = 20 shadow runs, zero MALFORMED, EV-1 failure rate no higher than legacy, parity assertion holds, lint and verdict replay pass (MR:410); Stage 3 opt-in needs first measurement (H-B, H-C, safety) + anthropic-only env gate (MR:411); Stage 4 default after 2 release cycles (MR:412); Stage 5 post (MR:413); Stage 6 E' not planned (MR:414).
- Risks table 12 rows (MR:507-520); risk 4 "Reviewer identity not what was requested ... omitting `model` runs Sonnet" (MR:513); risk 5 format non-compliance Medium for Haiku-class (MR:514).
- First measurement: H-A T2 beats T1 by >= 15 pp; H-B NI within 10 pp; H-C median tokens <= 1.05x legacy, p95 <= 65k; safety conditions (MR:527-530). Arms A (T1), B (legacy T2), C (panel-parity), D (panel-lite) (MR:532). Ground truth = seeded defects + union ledger with blinded grader (MR:534). Sample size formula n = 6.185 d / M^2; pilot 60 defects estimates d, does not decide H-B (MR:536-538). Strata by depth and escalation path, >= 25% non-sparse plans quota (MR:540). Stage 0a definition: 42 card dirs, 33 with merged verdict, gate >= 90% (MR:542). "Inconclusive is not a pass" (MR:544).
- Open items O-1..O-11 (MR:549-559), notably O-4 gateway dispatch undefined/refused, O-6 unknown executor default in workflow path, O-8 rubric may be the cheaper lever, O-9 `_diversity.py:15` vocabulary mismatch.
- UNVERIFIED list incl. "whether the Agent-tool reply carries a model id" and "whether the `reflect-reviewer` tools allowlist survives a `model` override" (MR:586, 589) — both later probed by spike S-ID.
- Not read in this slice: MR:146-264 (Q1-Q4, template set, K1 contract, Opus uses, executor-exclusion gates), MR:295-399 (finding format detail, adapters), MR:420-499 (contract mapping, cost model). UNVERIFIED here.

### 0.2 ART/pilot-design.md (257 lines, read fully)

- Self-labelled "PILOT DESIGN (not the confirmatory run)"; estimates discordance d and noise d0, does not decide H-B (pilot-design.md:1-3).
- Thresholds table T-1..T-10 is the single place values live (pilot-design.md:15-26): T-1 H-A >= 15 pp; T-2 H-B NI within 10 pp one-sided 95%; T-3 median tokens <= 1.05x legacy; T-4 p95 <= 65k; T-5 zero safety events; T-6 d0 >= 0.8 d means noise; T-7 >= 25% non-sparse plans; T-8 z values; **T-9 conversion gate redefined by owner 2026-11-12**: >= 90% on cards written under the findings-v2 brief, legacy 67.28% is baseline only (pilot-design.md:25); T-10 pooled headline only if heterogeneity check not significant (no test named).
- Arms A-D (pilot-design.md:46-51): arm C is the development-build `--t2-engine panel`, NOT shadow form — owner decision, "because the shadow form keeps the legacy writers authoritative and so does not exercise the panel as the shipped T2" (pilot-design.md:50).
- Ground truth: 5 seeded defect kinds (ordering, missing acceptance, spec-uncovered requirement, wrong file path, cross-task contradiction) + union ledger with blinded grader; circularity caveat from `.dev/research/346-review-loop-experiments/p17/LEDGER-RESULTS.md:49` (pilot-design.md:57-64). Note: this links directly to the #346 study's method.
- Sample size/power: pilot power ~79% at d=0.10, ~54% (recomputed 53.5%) at d=0.20; with the 1.3 clustering factor ~69% / ~45% (pilot-design.md:97-99, A-12).
- Cost: pilot 1.30M-2.62M claude tokens (6 repeats in total) or 3.61M-7.24M (6 per plan); confirmatory 33 plans 2.41M-4.88M (pilot-design.md:131-133). Grading/seeding/orchestration not priced (SD-8, pilot-design.md:242).
- Non-sparse quota: only 4 of 38 recorded pre decisions were non-sparse (10.5%), so quota plans must be written for the measurement (pilot-design.md:164).
- **PROPOSED stop rule S-0..S-5** (pilot-design.md:188-218), a merge of two independent reviews plus a debate (`stop-rule/proposal-A.md`, `proposal-B.md`, `debate-A-on-B.md`, `debate-B-on-A.md` — those files not read here, UNVERIFIED). Key points: S-0 owner approves rule, SD-3 reading, two ceilings (claude, retrieval — never summed), rerun allowance before run 1; S-1 plan blocks, random recorded arm order, spend tested only between blocks so every defect keeps its pair; S-2 safety checked after every run; STOP for any event in arm C/D, event 4/5 any arm; LOG-and-continue for events 1-3 in legacy arms A/B (baseline faults); S-3 spend ceilings + projection PAUSE; killed run counts as above T-4; crashed run is "failed", not MALFORMED; S-4 never-stop list (no interim results, T-6 only after last block); S-5 stop record contents.
- Source discrepancies SD-1..SD-8 (pilot-design.md:233-242).
- **Stage 0 exit checklist** (pilot-design.md:248-257): item 1 50-pair hand labels PENDING (AI labels P 0.84 / R 0.95 exist but are not human labels); item 2 recorded cards 67.28% now baseline, redefined gate NOT YET MEASURED; item 3 consumer grep stored (320 hit files: producer 51, validator 4, consumer 239, not in scope 26; 2 prose lines with `contract_version == "1.8.0"`, 0 Python code lines); item 4 pilot designed and costed, stop rule + SD-3 + ceilings await owner. **"Stage 0 exit: PENDING."** (pilot-design.md:257).

### 0.3 ART/stage0a-report.md (471 lines; read 1-100, 241-248, 293-376; per-card tables skimmed)

- Generated by `uv run python scripts/reflect_stage0a_replay.py`; zero dispatch (stage0a-report.md:3).
- Inputs: 74 `pre-*` dirs, 43 with `reviewer-cards/` (spec said 42), 34 with merged verdict (spec said 33); 8 of 43 card runs lack a usable `input-snapshot.yaml` (stage0a-report.md:7-11).
- **Conversion share 479/712 = 67.28%, FAIL vs 90%** (stage0a-report.md:56-59); 2084 citations, 1801 with path+line, 283 unresolved (stage0a-report.md:60). By shape: yaml-blocking-minor 69.87%, yaml-other-severity 78.02%, markdown-table 32.18%, unlisted 0% (stage0a-report.md:66-71). Top causes: no path:line ref 104 units; "citations must be a list" 54; path not repo-relative 31; unlisted card no pipe table 19; no plan path 16 (stage0a-report.md:75-84). Evidence strength: full census of recorded legacy cards (n=712 units, 43 runs, one repo); shows legacy cards are heterogeneous free-form, does NOT show what cards written under a findings-v2 brief would score.
- Even this session's own reflect run's 3 cards were unconvertible (no pipe table) (stage0a-report.md:97-99).
- cluster_v2 totals: 689 findings, 461 clusters, 392 singletons, 55 multi-reviewer clusters, 29 chained, 55 blocking; citations 1178 resolved / 623 unresolved (path not in snapshot) / 283 malformed (stage0a-report.md:243). cluster_agreement null for every listed run (table stage0a-report.md:249-291).
- **Agreement with recorded merged verdict 24/358 = 6.70%**, 21 of 34 verdicts readable, descriptive only (stage0a-report.md:297); 13 merged verdicts unreadable as YAML findings lists (stage0a-report.md:325-337). Shows recorded merged verdicts are themselves heterogeneous; does NOT show clustering is wrong (merge and cluster measure different things).
- **Null convergence scores: 8** (spec said 7): single-reviewer-fallback 2, illegal merge_method value 4 (`none`, `sc-adversarial-protocol-mode-a`, `inline-orchestrator` x2), other 1, undetermined 1, skipped-similar 0 (stage0a-report.md:343-356). Shows legacy contracts already contain illegal `merge_method` values.
- **Recorded calibration: 0 of 689 findings carry a numeric `finding_confidence`** (stage0a-report.md:370-376) — blind calibration as recorded produces no machine-readable per-finding number in any recorded card. Important for the unify goal: "blind calibration kept" (MR:92) has no recorded numeric output to reuse.

### 0.4 ART/conversion-gate-redefinition.md (36 lines, read fully)

- Owner decision 2026-11-12: gate "should be redefined based on the findings" (conversion-gate-redefinition.md:3).
- At least 121 of 233 misses (52%) are findings that never wrote a line or plan/spec path, because legacy briefs never asked for line-level citations; "the 67.28% measures how the history was written, not how well the parser works" (conversion-gate-redefinition.md:20).
- New T-9: recorded cards = baseline, no gate; gate applies to cards written under the findings-v2 brief (shadow brief line `refs/reviewer-spec.md:39`), 90% unchanged; a fail blocks promoting findings-v2 from shadow to authoritative, not Stages 0-2 (conversion-gate-redefinition.md:24-26).
- Measurement: card-level proxy = `findings_block_compliance_rate` from `scripts/reflect_shadow_exit.py`; the finding-level gate script is **NOT BUILT** (conversion-gate-redefinition.md:30-31). Population = the 20 Stage 2 shadow runs, ~1.4M tokens, needs `superclaude install` and spend approval (conversion-gate-redefinition.md:32).
- Lesson for unification: input-format compliance is a brief problem, not a parser problem — the central panel must instruct reviewers to emit the shared finding format.

### 0.5 ART/cluster-v2-known-weaknesses.md (12 lines, read fully)

- W-1 bundled finding (one finding, several defects) clusters as one; sampler skips same-reviewer pairs so the 50-pair sheet cannot measure it (cluster-v2-known-weaknesses.md:7).
- W-2 `refs_norm` takes `P1` out of "D-P1" → false merge (pair P12), cites `src/superclaude/cli/review/findings.py:29` "re-read before relying" (cluster-v2-known-weaknesses.md:8). [UNVERIFIED in this slice]
- W-3 `spec:N` resolved against the short `source.md` brief, not the spec (cluster-v2-known-weaknesses.md:9). **This is a source/spec input-identity problem** — relevant to section 5 overlap.
- W-4 precision 0.84 / recall 0.95 are AI-label sample figures, not rates (cluster-v2-known-weaknesses.md:10).
- None fixed; cluster output stays telemetry (cluster-v2-known-weaknesses.md:3). Shadow calibrator brief now asks for a numeric confidence because 0/689 recorded (cluster-v2-known-weaknesses.md:12).

### 0.6 ART/pair-labels/README.md (32 lines, read fully)

- Method: 3 independent AI labelers (opus, sonnet, skeptical opus), blind to each other and to `cluster_v2`'s verdict; 46 unanimous, 4 split 2-1 (P01, P09, P12, P38); splits went to a minority-side advocate debate (`debate-split-pairs.md`, not read, UNVERIFIED) (pair-labels/README.md:7-10).
- Bundled-finding ruling: same defect when one edit resolves at least one separable part of each finding; P38 is the only label differing from plain majority (pair-labels/README.md:14).
- Result: TP 21, FP 4, FN 1, TN 24; precision 0.84 (21/25), recall 0.9545 (21/22); sample is 25 merged + 25 apart by design so "sample figures, not rates" (pair-labels/README.md:18).
- Caveats: labelers and `cluster_v2` same model family, written in this work; labeler B did not open cards; claim text cut at ~300 chars; several findings state no defect (easy "no") (pair-labels/README.md:22-25).
- Owner hand labels cannot be supplied by AI → Stage 0 exit item 1 stays PENDING; same-reviewer supplementary pair set NOT BUILT (pair-labels/README.md:29-31).

### 0.7 ART/s-id-results.md (38 lines, read fully)

- Spike S-ID run 2026-11-12: 3 probes via `subagent_type: reflect-reviewer` with Agent `model` = haiku / sonnet / opus (s-id-results.md:3).
- **Self-report matched pin by model name: 0 of 3** (each gave a gateway alias `claude-gw-tier2/1b/1a[1m]`) (s-id-results.md:27, 37).
- **Transcript `message.model`: haiku pin ran `gpt-6.1-sol` (non-Anthropic), sonnet ran `claude-sonnet-5-5`, opus ran `claude-opus-5-5` → 2 of 3 pins honoured** (s-id-results.md:9-11, 27, 37). Cause stated: haiku resolved to gateway tier2 alias whose tier list has no Anthropic model (`review-tiers.default.json`: `gpt-6.1-sol` first); the anthropic-only Haiku stand-in did not apply on this gateway (s-id-results.md:27).
- Model id is exposed only in the sidechain transcript on disk (`~/.claude/projects/.../subagents/agent-<id>.jsonl`), NOT in the Agent tool result (s-id-results.md:28).
- Read-only allowlist survives the `model` override, 3/3; harness renames tools (`mcp__razor_culture__*`, `functions.*`) (s-id-results.md:29).
- Decision: `identity_source: observed`, with two limits: adapter needs transcript access; "Stage 1 must not assume that a pin yields the class it names" (s-id-results.md:34). Evidence strength: n=3 probes, one gateway, one point in time.

### 0.8 ART/shadow-standalone-evaluation.md (132 lines, read fully)

- **The shadow run is not a program**: the agent executes prose steps 1-10 of SKILL.md §4.3a (SKILL.md:338-349); `cli/reflect/` has no shadow code; only `review/manifest.py` and `review/manifest_cmd.py` mention `t2_engine` (shadow-standalone-evaluation.md:7-10). [doc claim; spot-check in section 0.12]
- Component classification table generic vs reflect-specific (shadow-standalone-evaluation.md:12-29): generic = shadow authority rule idea, manifest mechanism (hashes, ordered stages, idempotent attempts, resume, atomic save), shadow publish guard, `panel.py` resolver (shared with spec-panel loop), deterministic clustering, citation pre-check, exit-script skeleton; reflect-specific = steps 1-10, manifest constants/keys, `card_convert.py`, `panel_lint.py`, shadow brief line.
- Minimal generic shadow-run contract (5 parts: frozen variant, authoritative path, recording, comparison, exit measurement) (shadow-standalone-evaluation.md:33-50). Key caveat: reflect's shadow variant produces no verdict of its own — it reuses legacy dispatch, so it measures side signals (agreement, compliance, parity), **not quality** (shadow-standalone-evaluation.md:47-48).
- Candidate consumers: `/sc:spec-panel` loop (already calls `review panel resolve` / `review merge`), `sc-troubleshoot-protocol`, `sc-workflow-protocol`; overlap with `sc-cli-eval`, `scripts/eval_runner.py`, `scripts/ab_test_workflows.py` UNVERIFIED (shadow-standalone-evaluation.md:54-63).
- Complexity Medium (harness) / Large (full comparable variant output); ~1,700 lines in play, about a third shared (shadow-standalone-evaluation.md:67-72). Risks: test pins on `mf.STATES`, 1.8.0 coupling, installed-path rule, "mechanism has never run for real" (`test_shadow_exit_script.py:292-302`) (shadow-standalone-evaluation.md:86-96).
- **Recommendation: extract only after the 20 real reflect shadow runs PASS and the owner names a second skill** (shadow-standalone-evaluation.md:127-132). This is the "standalone shadow harness deferred" decision.

### 0.9 ART/consumer-inventory.md (405 lines; summary 1-40 read)

- Generated by `uv run python scripts/reflect_consumer_inventory.py`; 9 contract words scanned over `src/ tests/ scripts/ .dev/eval-workspaces/ docs/` (consumer-inventory.md:3-7).
- 3423 files searched, **320 hit files: producer 51, validator 4, consumer 239, not in scope 26**; by root `src/` 50, `tests/` 90, `scripts/` 4, `.dev/eval-workspaces/` 167, `docs/` 9; 33 `src/` hits are installed primitives (consumer-inventory.md:11-18).
- 2 prose lines in `src/` hold a `contract_version == "1.8.0"` equality (`sc-reflect-protocol/SKILL.md:1877`, `refs/grader-extensions.md:180`), 0 Python (consumer-inventory.md:22-25); CI grader `.dev/eval-workspaces/sc-reflect/grader.py` has no match (consumer-inventory.md:27). Named producers incl. `cli/reflect/ensemble.py`, SKILL.md, refs; validator `cli/reflect/contract.py` (consumer-inventory.md:33-38). Lines 41-405 not read (per-file table) — UNVERIFIED detail.

### 0.10 ART/addendum-1.md and addendum-2.md (headings + body skimmed)

- addendum-1 "calibration source in the shadow steps": recorded calibration layouts mixed across 37 runs / 102 cards (21 separate file, 10 embedded, 2 variant, 4 none) (addendum-1.md:3). Numeric per-finding confidences exist in 1 of 74 runs (this plan's own), keyed `F1...` vs card ids `R1-F1...` — **an id mismatch** (addendum-1.md:10). `confidence-calibrator` returns one score per card; per-finding numbers only exist when the brief asks (addendum-1.md:11).
- Debate verdicts: multi-layout reader REJECTED (~130 lines recovering 0 of 689); narrow reader REJECTED; ADOPTED `calibrated_findings: n/m` + `calibration_coverage` in `review cluster` (~6 lines, 3 tests); SKILL.md shadow step 5 rewritten so orchestrator writes `panel/cards/reviewer-N.md` with findings block + numeric `per_finding` keyed by exact finding ids (addendum-1.md:16-19).
- Lesson recorded across reviews 2-5: "Four rounds of review each found new ones because each correction added a new, more specific claim. The corrections of this round remove the consequence claims instead of refining them" (addendum-1.md:38). A convergence lesson for any review loop.
- addendum-2: owner-requested AI labels, merged stop rule, F5 wording, dropped sweep ref; owner waived a 6th full review but the archive helper requires latest FINAL = pass, so a narrowed review was run (addendum-2.md:3-8). Not done: conversion gate, `confidence-calibrator` agent file, the 20 shadow runs (addendum-2.md:10).

### 0.11 ART/final-review-1..7.md (verdict lines only)

| Review | Verdict line |
|---|---|
| 1 | issues; all 20 tasks met; 3041 tests passed (final-review-1.md:3) |
| 2 | issues; F1.1 resolved; 3044 passed (final-review-2.md:3) |
| 3 | issues; F2.1-F2.3 resolved; SKILL.md §4.3a audited against CLI help + literal recipe run (final-review-3.md:3) |
| 4 | issues; F3.1-F3.2 resolved (final-review-4.md:3) |
| 5 | issues; F4.1-F4.5 resolved; literal run of shadow steps 1-10 (final-review-5.md:3) |
| 6 | issues (narrowed); F5.1-F5.3 resolved; stop rule checked (final-review-6.md:3) |
| 7 | **pass** (delta only); F6.1-F6.4 resolved; 3044 passed; no blocking finding (final-review-7.md:3) |

Evidence strength: seven fresh-opus final reviews, each finding only prose/consequence-claim inaccuracies after the first; no review found a task failing its AC. Shows the package passed; also shows a 7-round convergence cost driven by prose claims, not code.

### 0.12 TS = .dev/troubleshoot/shadow-failures-20261113014240/REPORT.md (45 lines, read fully)

- Tier 1 quick troubleshoot of exit-script failures on shadow runs 03-07; calibrator and evidence-validator NOT run; sample 5 runs (TS:3-5).
- **Parity root causes (two):** runs 04/05 card `model:` header held the gateway alias the harness reported (`claude-gw-tier1b[1m]` etc.) while 03/06/07 copied the pin; SKILL.md:341 does not say copy from `panel/resolution.json`; exit script compares strings at `scripts/reflect_shadow_exit.py:148` (TS:14). Run 07: contract lacks `reviewer_personas`/`reviewer_models` and carries 3 keys outside frozen 1.8.0 (`memory_status`, `notes`, `zero_drop_flag`) — orchestrator contract-writing lapse (TS:16). Fixes: `model:` copied verbatim from resolution, `model_observed:` separate line; name required telemetry keys, forbid new top-level keys (TS:19-21).
- **EV-1 root cause:** rule requires `<output>/adversarial/merged-verdict.yaml` with `merge_method: adversarial` (SKILL.md:714, :1955, `panel_lint.py:271`) but no step tells the orchestrator to write it; runs 03/06/07 left it nested at `adversarial/adversarial/merged-verdict.yaml`, 04/05 only a `.md`; all five contracts say `merge_method: adversarial` — debate ran, gate failed on placement/format (TS:25). Legacy baseline fails EV-1 in 3 of 39 runs vs 5 of 5 recent — cause UNVERIFIED (TS:30). Recommends against loosening the gate (TS:29).
- **Compliance 0.67 root cause:** brief names the format without giving the schema (only `refs/reviewer-spec.md:39`); reviewers improvised pipe tables, escape errors, invented roles/categories (`repo` role; allowed roles at `findings_v2.py:35`) (TS:35). Metric inconsistent: some runs recorded post-re-ask, others pre-normalization; first-pass compliance where stated 1 of 3 (TS:36). Fixes: schema stub + example line in brief; define telemetry once as first-pass; stop orchestrator remapping (TS:39-41).
- Next step needs owner approval because it edits a user-facing skill (TS:45). Later commits `9874d63fb` and `c2e3347d3` ("shadow steps pin the card model, write merged-verdict.yaml, require the schema in the reviewer brief"; "reviewer brief names the exact findings heading") appear to apply these fixes — from git log in the session context, not code-verified in this slice (UNVERIFIED).

### 0.13 COMBO/PLAN.md (199 lines, read fully)

- Status: "designed, NOT run" at time of writing (COMBO/PLAN.md:1-3); later FINDINGS shows it ran.
- **Section 1 summarises the OTHER session's study** (commit `b4db265a8` on `ironbelly/eval-tasklist-review-panel`, read via `git show`) (COMBO/PLAN.md:8-38): tested ONLY the reviewer role, `/sc:spec-panel --mode critique` of `/sc:workflow` tasklists, one `claude -p --model <raw id>` per reviewer, deterministic `superclaude review merge`, blind Opus judges vs ground truth (defects that hurt real implement runs); 3 packages (designSpec 10 GT/5 blocking, makeTheAliasOnly 4/3, design control 2/0), 71 valid rows (COMBO/PLAN.md:13-16). Best replicated: haiku + 2x luna 2.2/14 found, 1.2/8 real blocking, 3.0 wrong blockers; sonnet alone 2/16 at 93k tokens, more catches per token than 3-6 model panels; 5-reviewer panels no gain at 2-4x cost (COMBO/PLAN.md:18-24). Calibrator/debate/orchestrator NOT tested; deterministic merge silently dropped anchors >200 chars: 49 blocking findings lost (COMBO/PLAN.md:25). Per-model: sonnet opened source.md 62/63, ember skipped 39%, luna 22%, haiku 15/75; luna weakest verbatim anchors 91.4% (COMBO/PLAN.md:27-28). Only 3 effects survive permutation tests; no panel lifts ceiling past ~2.5/14 (COMBO/PLAN.md:31-37). All of this is second-hand (this session's reading of the other study), UNVERIFIED against the other study's files in this slice.
- Section 2: how reflect picks models today (COMBO/PLAN.md:44-52): orchestrator = session model (pilot ran `claude-gw-tier3[1m]` from `~/.claude/settings.json`); reviewers get class sonnet/haiku/opus via Agent call, served model decided by env `ANTHROPIC_DEFAULT_{SONNET,HAIKU,OPUS}_MODEL`; if orchestrator omits class, `reflect-reviewer` frontmatter `model: sonnet` wins; calibrator frontmatter sonnet; evidence validator sonnet; `SUPERCLAUDE_REVIEW_TIERS`/`--tiers` change only `panel/resolution.json` and card headers, **never dispatch**.
- **Key structural finding:** shadow step passes `--env anthropic-only`, so `panel_parity`, card `model:` headers and contract `reviewer_models` record the CLASS rotation, not the served model — they say "claude-haiku-5-5" even when GPT 6.1 Sol served; truth only in transcripts (COMBO/PLAN.md:54-59).
- **Dispatch collapse:** in 6 of 9 tier3-orchestrated pilot runs (03, 05, 07, 08, 09, 10) all three reviewers ran on the SONNET alias; both tier1b-orchestrated runs (01, 02) dispatched correctly; "orchestrator drives dispatch" is a hypothesis, n tiny (COMBO/PLAN.md:66-69).
- Five combos A-E as a chain of single changes (COMBO/PLAN.md:77-107); E risk: step 0.5 may count two Luna values as one → 2 reviewers (COMBO/PLAN.md:106).
- Protocol: fixed input `TASK-WF-designSpec-20261107-075614` (plan + source.md only; implement history left out because it is the answer key); runs kept OUT of `.dev/reflect/` because the exit script counts every `pre-*` there; 3 blocks, random order per block; restore reflect memory files before each block (else r2 reads r1's summary); freeze skill hashes, no `make sync-dev` / `superclaude install` mid-experiment (COMBO/PLAN.md:114-133).
- Launch recipe uses `env -u ... CLAUDE_CODE_PRINT_BG_WAIT_CEILING_MS=0` and `claude -p ... --output-format stream-json --verbose --forward-subagent-text` (COMBO/PLAN.md:143-148).
- Pre-registered decision rule: leads only when ranges don't overlap, median gap > A's own range, and >= 2/3 runs dispatch as designed; ~40 comparisons → expect chance separations (COMBO/PLAN.md:178-189).

### 0.14 COMBO/FINDINGS.md (42 lines) and COMBO/results.md (47 lines), read fully

- 15 runs, all manifest `published`, 3/3 reviewers complete; skill hashes unchanged across blocks; **no blind quality scoring** (COMBO/FINDINGS.md:3, 42).
- Served models (COMBO/FINDINGS.md:7-15; COMBO/results.md:33-47): A/B "haiku" slot = `gpt-6.1-sol`; A3 collapsed (orchestrator passed no class → all reviewers and calibrators on `claude-sonnet-5-5`); C is the only combo with real Haiku; E = 3 reviewers but 2 distinct models. "The panel record (`panel/resolution.json`, card headers, `panel_parity`) never shows this; only the transcripts do" (COMBO/FINDINGS.md:15).
- Per-combo medians (COMBO/FINDINGS.md:19-25): A 64 min / conf 0.77 / 21 findings / compliance 0.67x3 / 220k tok; B 25 / 0.71 / 12 / 1.0x3 / 241k; C 33 / 0.74 / 19 / 1.0x3 / 335k; D 27 / 0.65 / 16 / 1.0x3 / 296k; E 24 / 0.59 / 19 / 1.0,0.67,0.33 / 321k.
- Leads (COMBO/FINDINGS.md:29-31): (1) orchestrator speed — A (tier3 orchestrator) 64-68 min vs B (tier1b) 23-39 min, cause not isolated; (2) calibrated confidence — D and E below A, but calibrator model also differs (confound); (3) first-pass compliance — A 0.67 every run, B/C/D 1.0 all nine, E declining.
- Not different: clustered counts overlap; C vs B (real Haiku vs Sol) no separation; USD is Claude Code estimate, not billed; parity/lint problems in all combos reflect orchestrator contract-writing lapses (COMBO/FINDINGS.md:35-38). results.md shows parity False in A1-A3 and C2, lint clean False in B1-B3, C2, C3, D1, E2, E3 (COMBO/results.md:5-19).
- Evidence strength: n=3 per combo, one input package, descriptive only; no ground truth scoring; ~40 comparisons.

### 0.15 `.dev/reflect/*shadow*/` run summary and exit script (run 2026-11-13 in this slice)

Command 1: `for d in .dev/reflect/*shadow*/; do jq -r .state $d/panel/manifest.json; done` → **15 shadow dirs**: 13 `published` (shadow03-15), 1 `clustered` (shadow02, stopped before publish), 1 with no `panel/manifest.json` (shadow01). Run names show 15 distinct legacy plan packages dated 2026-10-23 to 2026-11-11 (e.g. `pre-TASK-WF-detachTheCcsessi-20261102-034618-shadow01..03` reuse one package three times).

Command 2: `uv run python scripts/reflect_shadow_exit.py --runs-root .dev/reflect | tail -25` (output, verbatim key lines):

- `verdict replay against the legacy baseline (42 runs): new degraded reasons 0`
- `2-of-3 shortfalls: 0`; `unknown executor class (executor_class_resolved false): 9`
- `findings-block compliance rate (mean over 9 run(s)): 0.704`
- `cluster_agreement (9 run(s)): min 1.000, median 1.000, max 1.000`
- `failure: EV-1 failure rate is higher than the legacy baseline`
- parity does not hold: shadow04, 15, 05, 09, 08, 07 (6 runs)
- lint or manifest problems: shadow04, 15, 06, 03, 13, 05, 09, 08, 07 (9 runs)
- **`OVERALL: FAIL (shadow runs 13 of 20)`**

Observations: (a) only 13 of the required 20 shadow runs exist, so Stage 2 exit is not reachable yet on count alone; (b) compliance 0.704 is below the 0.90 T-9 proxy; (c) `cluster_agreement` is 1.000 everywhere, which per addendum-1.md:34 is what it reads when there is no blocking cluster — so it carries no signal in these runs; (d) every published run has `executor_class_resolved false` (9 of 9 measured) — matches MR O-6 (unknown executor is the workflow-path default); (e) shadow runs 10-15 were not covered by the TS report (which covered 03-07) — whether the post-fix runs (after commits `9874d63fb`, `c2e3347d3`) still fail parity/lint for the same reasons is UNVERIFIED; the tail does not show per-reason detail. The head of the script output (EV-1 counts) was not captured — UNVERIFIED numbers.

### 0.16 Code spot-checks done in this slice (Documentation Staleness Protocol)

- [CODE-VERIFIED] `src/superclaude/cli/review/` contains `manifest.py`, `manifest_cmd.py`, `findings_v2.py`, `cluster.py`, `cluster_cmd.py`, `verify_cmd.py`, `card_convert.py`, `panel.py`, `ledger.py`, `findings.py` (Glob). So the Stage 0-2 kernel pieces named PROPOSED in MR now exist as code.
- [CODE-VERIFIED] grep `t2_engine|t2-engine` over `src/superclaude/cli` → only `review/manifest.py`, `review/manifest_cmd.py` (matches shadow-standalone-evaluation.md:8-9: no shadow code in `cli/reflect/`).
- [CODE-VERIFIED] `findings_v2.py:35` `ROLES = ("plan", "spec", "source", "test", "diff", "artifact")`; `:36` `LENSES = ("spec", "reflect-pre", "reflect-post")`; `:37` `CHANNELS`; `:38` `DEVIATION_CLASSES`; `:41-48` `REFLECT_CATEGORIES` (matches TS:35).
- [CODE-VERIFIED] `cli/review/data/review-tiers.default.json:7` tier2 alias `claude-gw-tier2[1m]`, models list starts `gpt-6.1-sol`, no Anthropic model; `:34` anthropic-only `stand_ins` map tier2 → `claude-haiku-5-5`; `:6` tier1b models `claude-sonnet-5-5`, `gpt-6.1-sol`, `muse-wonder-full-1.0`. This is the mechanism behind "haiku slot served by gpt-6.1-sol" (s-id-results.md:27) — the gateway's tier2 alias, not the stand-in table, decides what serves.
- Not checked: `scripts/reflect_shadow_exit.py:148` parity string compare; `SKILL.md:338-349` shadow steps; `SKILL.md:714,1955` EV-1; `panel_lint.py:271` — UNVERIFIED in this slice.
- GitHub issues #525-#530 (hand labels issued as issues): no local record under `.dev/` (grep for `#525..#530` / `issues/525..530` found nothing relevant); not checked on GitHub (no `gh` allowed). UNVERIFIED.

---

## 1. Inventory of artifacts

Status key: **decided** = owner or design decision recorded; **measured** = numbers produced from data; **pending** = waiting on owner or more runs; **superseded** = replaced by a later artifact; **reference** = supporting record.

| # | Path | What it is | Status |
|---|---|---|---|
| 1 | `MR` (merged-requirements.md) | Adversarial Mode B merge of 3 design variants: architecture C (Layered Review Kernel K1-K4), Stage 0-6 migration, first-measurement design, risks, open items O-1..O-11 | decided (architecture C, as `draft-for-owner-review`, MR:7); parts superseded: T-9 wording (by #4), Stage 0a counts 42/33/7 (by #3) |
| 2 | `ART/pilot-design.md` | Pilot (not confirmatory) design: thresholds T-1..T-10, arms A-D, sample size, cost, PROPOSED stop rule S-0..S-5, Stage 0 exit checklist | measured (arithmetic) + pending (stop rule, SD-3 reading, ceilings, Stage 0 exit) |
| 3 | `ART/stage0a-report.md` | Zero-dispatch replay of 43 recorded card dirs: conversion 67.28%, clusters, 6.70% merged-verdict agreement, 8 null scores, 0/689 calibrated | measured; its FAIL verdict superseded by #4 |
| 4 | `ART/conversion-gate-redefinition.md` | Owner redefinition of T-9 (2026-11-12): gate applies to findings-v2-brief cards; legacy = baseline | decided; measurement pending (finding-level script NOT BUILT) |
| 5 | `ART/cluster-pairs-50.csv` | Blank 50-pair sheet for owner hand labels | pending (owner labels; reportedly issued as GitHub issues #525-#530, UNVERIFIED) |
| 6 | `ART/cluster-pairs-50.ai-labelled.csv` + `ART/pair-labels/{README.md,labeler-A/B/C.csv,debate-split-pairs.md}` | AI labels by 3 blind labelers + minority debate; P 0.84 / R 0.95 | measured (AI, not human); does not satisfy exit item 1 |
| 7 | `ART/cluster-pairs-50.form.md`, `.form.simple.md` | Human-labelling forms (not read) | reference, UNVERIFIED content |
| 8 | `ART/cluster-v2-known-weaknesses.md` | W-1..W-4 weaknesses of `cluster_v2` | measured (qualitative); not fixed |
| 9 | `ART/consumer-inventory.md` | Grep inventory of 1.8.0 contract consumers (320 hit files) | measured; exit item 3 met |
| 10 | `ART/lint-test-design.md`, `per-field-source-table.md` | Lint test design (implemented as Task 15 `panel_lint.py`), field source table | reference (not read, UNVERIFIED) |
| 11 | `ART/s-id-runbook.md`, `ART/s-id-results.md` | Spike S-ID: identity + allowlist probes (n=3) | measured; decided `identity_source: observed` |
| 12 | `ART/shadow-standalone-evaluation.md` | Should the shadow harness become a generic piece? | decided: defer until 20 shadow runs PASS + owner names 2nd consumer |
| 13 | `ART/stage2-entry-inventory.md`, `stage2-entry-inventory-diff.md` | Stage 2 entry inventory (not read) | reference, UNVERIFIED |
| 14 | `ART/addendum-1.md` | Calibration-source debate; adopted `calibration_coverage`; 4 review rounds of prose corrections | decided |
| 15 | `ART/addendum-2.md` | Owner-requested AI labels, merged stop rule, narrowed 6th review | decided / reference |
| 16 | `ART/final-review-1..7.md` | Fresh-opus final reviews; 1-6 `issues`, 7 `pass` | measured (package passed) |
| 17 | `ART/stop-rule/{proposal-A,proposal-B,debate-A-on-B,debate-B-on-A}.md` | Inputs to the merged stop rule (named in pilot-design.md:188, addendum-2.md:6) | reference; the 4 files exist (Glob), content not read (UNVERIFIED) |
| 18 | `ART/T*-checks.log` (20 files) | Per-task check logs | reference, not read |
| 19 | `TS` (troubleshoot REPORT.md) | Root causes of parity / EV-1 / compliance failures in shadow runs 03-07 | measured (n=5); fixes proposed, apparently applied in commits 9874d63fb / c2e3347d3 (UNVERIFIED) |
| 20 | `COMBO/PLAN.md` | 5x3 model-combination experiment design + summary of the other session's study | decided (design, ran) |
| 21 | `COMBO/FINDINGS.md`, `COMBO/results.md` (+ `results.jsonl`, `logs/`, `analysis/extract.py`, `combos.json`, `resolve/`, `input/`, `runs/`) | Descriptive results of 15 runs | measured (descriptive, n=3/combo); blind GT scoring pending approval |
| 22 | `.dev/reflect/*shadow01..15/` | 15 real shadow runs (13 published, 1 clustered, 1 no manifest) | measured; Stage 2 exit FAIL (13 of 20) |
| 23 | `scripts/reflect_shadow_exit.py` | Stage 2 exit aggregator: PASS/FAIL/INSUFFICIENT-RUNS | code (exists; output captured in 0.15) |
| 24 | `scripts/reflect_stage0a_replay.py`, `reflect_cluster_pairs.py`, `reflect_consumer_inventory.py`, `reflect_verdict_replay.py` | Measurement scripts named by artifacts | code, existence not checked in this slice (UNVERIFIED) |
| 25 | `src/superclaude/cli/review/{manifest,manifest_cmd,findings_v2,cluster,cluster_cmd,verify_cmd,card_convert}.py` | Stage 0-2 kernel code | CODE-VERIFIED existence (0.16) |
| 26 | Git commits `d2d8a2d16` (#519 Stage 0-2), `9874d63fb`, `c2e3347d3`, `792cf8c52` | Shipped work on this branch | reference (from session git log, not inspected) |

---

## 2. Findings with evidence strength

| ID | Finding | Evidence (cite) | Sample / strength | What it shows | What it does NOT show |
|---|---|---|---|---|---|
| F-1 | Legacy reflect cards convert to findings-v2 with an unambiguous `(path, line)` only 67.28% of the time | stage0a-report.md:56-59 | Census: 712 units, 43 runs, one repo | Legacy briefs never asked for line citations; 52% of misses have no line at all (conversion-gate-redefinition.md:20); markdown-table cards worst (32%) | How cards written under a findings-v2 brief would convert (that gate is unmeasured) |
| F-2 | Under the findings-v2 brief, card-level first-pass compliance is still low: 0.704 mean over 9 shadow runs; 0.67 mean over runs 03-07 | 0.15 exit output; TS:3, TS:36 | 9 runs; metric definition was inconsistent before the fix (TS:36) | The brief named the format without giving the schema → reviewers improvised (TS:35) | Whether the later brief fix (schema stub) raised it; card-level ≠ finding-level |
| F-3 | Combo study: first-pass compliance 1.0 in all 9 B/C/D runs; 0.67 in every A run; E falling | COMBO/FINDINGS.md:21-25, :31 | n=3 per combo, after the brief fix (skill hash frozen) | Compliance depends on the served model / orchestrator mix; it can reach 1.0 | Causation (A differs in orchestrator); quality |
| F-4 | cluster_v2 pair precision 0.84 (21/25), recall 0.95 (21/22) | pair-labels/README.md:18 | 50 pairs, stratified 25/25 by design; **AI labels** (3 blind labelers, same model family as cluster_v2) | cluster_v2 is plausible as telemetry | Population rates; human agreement; bundled findings (W-1) or same-reviewer pairs |
| F-5 | Recorded merged verdicts agree with multi-reviewer clusters only 6.70% (24/358) | stage0a-report.md:297 | 21 of 34 verdicts readable | Merged verdicts and clusters measure different things; 13 verdicts unreadable | That clustering is wrong |
| F-6 | 0 of 689 recorded findings carry numeric calibration; calibrator returns one score per card | stage0a-report.md:370-376; addendum-1.md:9-11 | Census | Blind calibration as practised gives no per-finding number; the one run with numbers had an id mismatch (`F1` vs `R1-F1`) | That calibration is useless — only that it is not machine-joinable |
| F-7 | 8 recorded null convergence scores; 4 from illegal `merge_method` values (`none`, `sc-adversarial-protocol-mode-a`, `inline-orchestrator` x2) | stage0a-report.md:343-356 | 64 contracts | Legacy agent-written contracts already violate the vocabulary | — |
| F-8 | **Parity failure root causes**: (a) card `model:` header got the gateway alias instead of the pin; (b) contract missing `reviewer_personas`/`reviewer_models` and adding 3 unlisted keys | TS:14, TS:16 | 5 runs (03-07), Tier 1 quick, uncalibrated | Orchestrator prose-following lapses, not model class errors | Later runs (08-15) still fail parity (0.15), cause not analysed |
| F-9 | **EV-1 root cause**: no step tells the orchestrator to write `adversarial/merged-verdict.yaml`; debate output landed nested or as `.md` only | TS:25 | 5 of 5 recent runs vs 3 of 39 legacy baseline | File placement/format, not a skipped debate | Why the jump vs legacy (UNVERIFIED, TS:30) |
| F-10 | **Compliance root cause**: brief gave a one-line pointer, no schema; metric mixed pre/post re-ask | TS:35-36 | 5 runs | Shared finding format needs its schema in the brief | — |
| F-11 | **Dispatch collapse**: in 6 of 9 tier3-orchestrated pilot runs all three reviewers ran on the SONNET alias; in combo A3 the orchestrator passed no class → all reviewers and calibrators on `claude-sonnet-5-5` | COMBO/PLAN.md:66-69; COMBO/FINDINGS.md:9; results.md:35 | Pilot n=9 (mixed skill states); combo 1 of 15 | When the orchestrator omits the Agent `model`, `reflect-reviewer` frontmatter `model: sonnet` wins (COMBO/PLAN.md:47) → heterogeneity silently lost | That orchestrator model is the cause (hypothesis; B tier1b had 0/3 collapses vs A 1/3) |
| F-12 | **"haiku" slot served by `gpt-6.1-sol`** on this gateway; pin honoured 2 of 3 in S-ID; combo A/B haiku slot = Sol | s-id-results.md:9, :27; COMBO/FINDINGS.md:15; review-tiers.default.json:7 [CODE-VERIFIED] | S-ID n=3; combo 6 runs | Class names do not determine served model; env `ANTHROPIC_DEFAULT_HAIKU_MODEL` → gateway tier2 alias → Sol | Whether Sol vs Haiku matters for quality (C vs B: no separation, COMBO/FINDINGS.md:36) |
| F-13 | **Identity mismatch / record vs reality**: `panel/resolution.json`, card headers, `panel_parity`, contract `reviewer_models` record the CLASS rotation; only the sidechain transcript `message.model` shows the served model; self-reports gave aliases 0/3 | COMBO/PLAN.md:54-59; COMBO/FINDINGS.md:15; s-id-results.md:27-28 | S-ID n=3 + 15 combo runs | Parity as built cannot detect a wrong served model; identity must be observed from transcripts | — |
| F-14 | 5x3 combo **speed lead**: A (tier3 orchestrator) 64-68 min (designed runs) vs B (tier1b orchestrator) 23-39 min | COMBO/FINDINGS.md:29 | n=3, one package | Orchestrator model choice is a large wall-clock lever | Cause isolated (FINDINGS says not isolated) |
| F-15 | Combo **confidence lead**: D 0.62-0.66 and E 0.53-0.68 below A 0.75-0.84 | COMBO/FINDINGS.md:30 | n=3 | Calibrated confidence moves with the panel/calibrator mix | Whether reviewers or calibrator drive it (confounded); whether lower confidence is more accurate |
| F-16 | Combo: clustered finding counts overlap across all combos; no blind GT scoring done | COMBO/FINDINGS.md:35, :42 | n=3 | — | **Which combo finds more real defects (the key question is unanswered)** |
| F-17 | Shadow mode measures side signals, not quality: the shadow variant reuses legacy dispatch and produces no verdict | shadow-standalone-evaluation.md:47-48; pilot-design.md:50 | Design analysis | Quality comparisons need the dev-build `panel` engine (arm C) or a seeded-defect pilot | — |
| F-18 | Stage 2 exit status: FAIL, 13 of 20 runs; EV-1 rate above legacy; parity 6 failures; lint/manifest 9 failures; `cluster_agreement` 1.000 everywhere | 0.15 exit output | 13 runs | Shadow mechanism runs end to end (13 published) but recording is unreliable | Panel quality |
| F-19 | 37 of 38 recorded pre runs escalate to T2, 34 because of the parsed-sparse pre-filter (workflow sources carry no labelled requirement ids) | MR:142 | Census of one repo's history | T2 cost is the typical per-plan cost; rubric (O-8) may be the cheaper lever | That T2 is worth it (H-A unmeasured) |
| F-20 | The spec-panel PN1 gain (15.7 vs 2.8 fixed defects) came from a revise loop reflect does not have; full panel ~290k round-1 tokens | MR:45, :48, :114 | Cited from #346 LEDGER-RESULTS.md (not re-read here) | Gains do not transfer automatically across consumers | — |
| F-21 | `cluster_v2` weaknesses: bundled findings, `P1` from "D-P1", `spec:N` resolved against the short `source.md` brief | cluster-v2-known-weaknesses.md:7-9 | Found during labelling | Input identity (which doc is "spec") is ambiguous in the pre-execution package | Frequency |
| F-22 | Executor class unknown in 9 of 9 measured shadow runs | 0.15 exit output; MR:554 (O-6) | 9 runs | Executor exclusion never actually exercised in shadow | — |
| F-23 | Seven final-review rounds, each finding new prose consequence-claims after correction | addendum-1.md:38; final-review-1..7 verdict lines | 1 package | Review loops on prose converge slowly unless corrections remove claims rather than refine them | — |

---

## 3. Lessons and methods worth carrying into the central panel

| Method / lesson | What it is | Where recorded | Value for the unified panel |
|---|---|---|---|
| **Shadow mode** | Variant runs beside the authoritative legacy path, writes only to `<out>/panel/` and a namespaced `telemetry:` block; a failing variant step records `panel_fallback_reason` and the run continues as legacy | shadow-standalone-evaluation.md:14, :38-41; MR:410 | Safe migration path for every consumer (spec-panel, workflow, PR review, rf-qa). Limit: measures parity/compliance, not quality (F-17) |
| **Manifest freeze** | `panel/manifest.json` (`review-panel-manifest/1`): frozen inputs + policy hash; ordered stage commits with payload/output hashes; (stage, unit, attempt) identity, attempts never add votes; only a last-stage manifest counts; shadow publish guard records hashes of authoritative files | shadow-standalone-evaluation.md:16-18, :35-44 (cites manifest.py:13-18, :97-108, :176-186, :496-500) | Generic run-record mechanism; extraction plan already written (shadow-standalone-evaluation.md:100-123). Constants are reflect-specific and pinned by tests |
| **Exit script** | `scripts/reflect_shadow_exit.py`: count required N runs, per-run hard-fail checks (parity, MALFORMED, EV-1, lint, replay), aggregate vs legacy baseline, PASS/FAIL/INSUFFICIENT-RUNS with fixed exit codes | shadow-standalone-evaluation.md:27, :49-50; output in 0.15 | Reusable "skeleton + consumer plugin" gate for any staged rollout |
| **Pre-registered stop rule** | S-0..S-5: owner pre-approval, block design keeping defect pairs, safety checked per run, spend ceilings per unit never summed, killed run = above T-4, crashed ≠ MALFORMED, never-stop list, stop record | pilot-design.md:188-218 | Template for any paid measurement of panel variants |
| **Single thresholds table** | All threshold values in one table T-1..T-10, referenced by id elsewhere | pilot-design.md:11-26 | Avoids drift between docs (a final-review check, final-review-7.md:3) |
| **Blind AI labelling** | 3 independent labelers (incl. a skeptical stance), blind to each other and to the algorithm's verdict; majority; minority-side advocate debate for splits; explicit ruling for bundled findings; labelled honestly as not-human | pair-labels/README.md:7-14, :22-29 | Cheap proxy for ground truth; caveat: same model family as the system under test |
| **Adversarial debates for design choices** | Proposal A/B + cross-debates (stop rule); orchestrator-vs-opponent debate (calibration reader) with "adopt only if return is high" | addendum-1.md:5-19; addendum-2.md:6 | Rejected ~130 lines that would have recovered 0/689 confidences; adopted a 6-line coverage counter |
| **Zero-dispatch replay on history** | Stage 0a replays recorded cards with no model calls | stage0a-report.md:3 | Free baseline for any consumer before spending on runs |
| **Redefine a gate when it measures history, not the system** | T-9 moved from recorded cards to brief-compliant cards | conversion-gate-redefinition.md:20-26 | Gates must measure what the change controls |
| **Observed identity** | Read served model from sidechain transcript `message.model`; record pin and observed separately (`model:` vs `model_observed:`) | s-id-results.md:28, :34; TS:19 | Only reliable way to know which model reviewed; adapter needs transcript access |
| **Chain-of-single-changes experiment** | Combos A→E each change one factor; adjacent-pair comparison; pre-set "lead" rule; runs kept out of `.dev/reflect/` so they don't pollute the exit count; restore memory files between blocks; freeze skill hashes, no install mid-experiment | COMBO/PLAN.md:77-81, :122-133, :178-189 | Reusable experiment protocol for model selection per role |
| **`CLAUDE_CODE_PRINT_BG_WAIT_CEILING_MS=0`** | Set in every headless combo launch (`env ... CLAUDE_CODE_PRINT_BG_WAIT_CEILING_MS=0 claude -p ...`) | COMBO/PLAN.md:144; `COMBO/combos.json:19` | Rationale not written in the files read (presumably keeps `claude -p` from returning before background subagents finish). **Rationale UNVERIFIED** |
| **User-level CLI install** | Shadow runs need `superclaude install` (installed skill, not the worktree copy); skill hashes of `~/.claude/skills/...` and `.claude/skills/...` recorded per block | conversion-gate-redefinition.md:32; COMBO/PLAN.md:131-133 | Headless runs execute the installed primitive; a stale install invalidates results. Exact "user-level CLI install" procedure not found in files read — UNVERIFIED |
| **Remove claims instead of refining them** | After 4 review rounds kept finding new consequence claims, corrections deleted claims | addendum-1.md:38 | Convergence tactic for review-loop revisers |
| **Telemetry, not routing, for new signals** | `cluster_v2` / `cluster_agreement` / `calibration_coverage` are telemetry only | MR:25, :59; cluster-v2-known-weaknesses.md:3 | Lets the panel collect signals without changing verdicts |

---

## 4. Decisions made and decisions open

### 4.1 Made

| Decision | By / when | Cite |
|---|---|---|
| Architecture C (Layered Review Kernel), debate kept, contract 1.8.0 unchanged through Stage 4, `--t2-engine` default `legacy` | adversarial merge, draft for owner review, 2026-11-11 | MR:7, :23-25, :404 |
| Reject B (full spec-panel loop for reflect); defer E' (deterministic merge, contract 2.0.0) | design | MR:50, :83 |
| Reflect panel capped at 3 reviewers; raising needs T2 ≥ T1 + 15 pp | design (V3 dissent) | MR:289 |
| Panel ledger not used for reflect in Stages 0-4 | design | MR:273 |
| T-9 conversion gate redefined to brief-compliant cards; legacy 67.28% baseline only | owner, 2026-11-12 | conversion-gate-redefinition.md:3, :24-26 |
| Pilot arm C = dev-build `panel` engine, not shadow | owner | pilot-design.md:50 |
| `identity_source: observed`; pins not trusted to yield the named class | spike S-ID, 2026-11-12 | s-id-results.md:34 |
| `review cluster` reports `calibration_coverage`; no multi-layout calibration reader | debate, addendum 1 | addendum-1.md:16-19 |
| Shadow harness extraction deferred until 20 shadow runs PASS and owner names a second consumer | evaluation | shadow-standalone-evaluation.md:127-132 |
| AI labels made, but do not satisfy "hand-labelled" | owner request + README | pair-labels/README.md:3, :29 |
| Package archived after FINAL review 7 pass; owner waived further full review | owner | addendum-2.md:3; final-review-7.md:3 |
| Combo runs kept out of `.dev/reflect/` | design | COMBO/PLAN.md:122-124 |

### 4.2 Open

| Open item | Blocking what | Cite |
|---|---|---|
| **Stage 0 exit PENDING**: item 1 owner hand labels (reportedly issued as GitHub issues #525-#530, UNVERIFIED); item 2 redefined conversion gate not measured; finding-level gate script NOT BUILT | Stage 0 exit formally | pilot-design.md:250-257; conversion-gate-redefinition.md:31 |
| **Stage 2 exit FAIL** (13 of 20 runs; EV-1, parity, lint failures) | Stage 3 entry | 0.15 |
| Pilot stop rule S-0..S-5, SD-3 reading ("6 repeats"), spend ceilings, rerun allowance — owner approval | pilot run | pilot-design.md:190, :229 |
| **Blind quality scoring of the 15 combo runs** against designSpec GT (10 defects, 5 blocking) — separate approval | any claim about which model mix finds more real defects | COMBO/FINDINGS.md:42; COMBO/PLAN.md:171-174 |
| Confirmatory measurement spend approval | H-B decision | pilot-design.md:226 |
| Owner sign-off on MR (status draft-for-owner-review) | — | MR:7 |
| O-4 gateway dispatch/templates undefined (refused); O-6 executor unknown in workflow path; O-8 rubric as cheaper lever; O-9 `_diversity.py` vocab mismatch; O-11 precedence | various | MR:552-559 |
| Same-reviewer supplementary pair set (W-1) NOT BUILT | measuring bundled-finding weakness | pair-labels/README.md:31 |
| `confidence-calibrator` agent file not changed to emit per-finding numbers | numeric calibration | addendum-1.md:26; addendum-2.md:10 |
| Cause of EV-1 jump (3/39 legacy vs 5/5 shadow) | — | TS:30 |
| Orchestrator-drives-dispatch hypothesis (tier3 vs tier1b) | model choice for orchestrator role | COMBO/PLAN.md:69; COMBO/FINDINGS.md:29 |

---

## 5. Overlap and conflict with the other session's tasklist review-panel study

Basis: this session's own summary of the other study in COMBO/PLAN.md:6-38 (read via `git show b4db265a8:...` on `ironbelly/eval-tasklist-review-panel`). The other study's files were NOT read in this slice; every "other study" claim below is second-hand and UNVERIFIED here (slice covering that study should confirm).

| Topic | This session | Other study (as summarised) | Relation |
|---|---|---|---|
| **Source/spec input problem** | W-3: `spec:N` resolved against the short `source.md` brief, not the spec (cluster-v2-known-weaknesses.md:9); 34/38 pre runs parsed-sparse because workflow `source.md` carries no labelled requirement ids (MR:142); combo input deliberately omits implement history (answer key) (COMBO/PLAN.md:114-118) | Reviewers often do not open `source.md`: sonnet 62/63, ember skipped 39%, luna 22%, haiku 15/75; "source.md not opened" is a named confounder (COMBO/PLAN.md:27, :33-34) | **Both found it, different facets**: this session = the pre-execution input package's "spec" is a thin brief and lacks requirement ids; other = models skip reading it. Central panel needs an explicit input contract (which file is the spec, required reads, verified reads) |
| **Model identity** | Haiku pin served by `gpt-6.1-sol`; pins honoured 2/3; self-reports 0/3; panel record shows class not served model; dispatch collapse to one model (F-11..F-13) | Used one `claude -p --model <raw id>` process per reviewer; identity audit among six audits; 2 misrouted runs found and excluded (COMBO/PLAN.md:13-14, :30-31) | **Both found identity problems.** Other study avoided alias routing by raw ids per process (headless). This session's agent-session dispatch (Agent tool + env class aliases) cannot pass raw ids per reviewer → needs observed identity from transcripts. Central panel: dispatch mode decides whether identity can be pinned or only observed |
| **Recommended reviewer mix** | Reflect: anthropic-only environment gate for Stage 3+ (MR:411); max 3 reviewers (MR:289); combo C (Sonnet/Haiku/Opus, all Anthropic) and B looked fine; combo E (study's haiku + 2x luna) had lowest calibrated confidence, declining compliance, only 2 distinct models (COMBO/FINDINGS.md:13, :25) | Best replicated for real blockers: haiku + 2x luna; sonnet alone most catches per token; ember + 2x luna default; 4-5 reviewer panels no gain at 2-4x cost (COMBO/PLAN.md:18-24) | **Partial conflict.** Other study's best panel is gateway (Luna) models, which MR's environment gate (anthropic-only) and O-4 (gateway refused) exclude. Agreement: >3-4 reviewers not worth it; single strong reviewer is efficient (bears on H-A). Combo E's lower confidence is not a quality result (no GT scoring) |
| **Merge** | Debate kept; `cluster_v2` deterministic clustering is telemetry only; #346 ledger path-blind (MR:25, :273) | Deterministic `superclaude review merge` silently dropped anchors >200 chars: 49 blocking findings lost (COMBO/PLAN.md:25) | **Consistent caution** about deterministic merge as authoritative. The 49-dropped bug is a concrete defect in the #346 merge code that a central panel must fix before any consumer relies on it (UNVERIFIED whether fixed on master) |
| **Roles tested** | Orchestrator, calibrator, reviewers all varied in combos; orchestrator affects speed and dispatch; calibrator confounds confidence (COMBO/FINDINGS.md:29-30) | Only the reviewer role; calibrator, debate judge, orchestrator NOT tested (COMBO/PLAN.md:25, :37) | **Complementary**: union covers reviewer quality (other) + orchestrator/calibrator effects (this) |
| **Ground truth / scoring** | No GT scoring yet; pilot design uses seeded defects + union ledger with blinded grader (pilot-design.md:57-64); combo blind scoring pending approval | Blind Opus judges vs GT = defects that hurt real implement runs; anonymised reports; permutation tests; only 3 effects survive (COMBO/PLAN.md:13-16, :30-34) | **Complementary**: other study's GT (designSpec 10/5) is the planned scorer for this session's combo runs (COMBO/PLAN.md:171-174). Two GT styles (seeded vs historical) should be reconciled in Phase 2 |
| **Ceiling / worth** | H-A (T2 beats T1 by 15 pp) unmeasured; 37/38 runs pay for T2 | No panel past ~2.5/14 GT; several GT never caught (COMBO/PLAN.md:36) | Other study's ceiling suggests H-A may fail on tasklists; supports MR O-8 (fix rubric) as a cheaper lever |
| **Finding format compliance** | Brief must carry schema; first-pass compliance varies by model mix (F-2, F-3, F-10) | Luna weakest verbatim anchors 91.4% vs 98-100% (COMBO/PLAN.md:28) | Both show per-model format/anchor fidelity differences; central panel needs per-model compliance telemetry |
| **Gateway model availability** | `muse-ember-1.0` absent from 2026-11-13 gateway list (COMBO/PLAN.md:109, :193) | Study default panel uses ember | **Conflict in practice**: the other study's default may not be runnable today |

---

## 6. Suggested deep-investigation assignments for Phase 2

1. **Input contract for review targets** — reconcile W-3 (spec:N vs short `source.md`), parsed-sparse escalation (MR:142), and the other study's "source.md not opened" data; define per consumer (reflect pre/post, workflow tasklist, spec review, PR review, rf-qa) which files are plan/spec/source, required reads, and how reads are verified. Read: `sc-workflow-protocol` Wave 4, `sc-reflect-protocol` input-resolution ref, other study's PILOT/COMBO reports.
2. **Identity and dispatch** — compare headless raw-id dispatch (other study `tools/run-reviewer.sh`), swarm lens `T2Model0N`, Agent-tool class dispatch, and `review-tiers.default.json` tiers/stand-ins/launch map; decide pinned vs observed identity per dispatch mode; check whether commit `9874d63fb` ("shadow steps pin the card model") fixed parity and why shadow08-15 still fail parity.
3. **Merge code on master (#346)** — verify the >200-char anchor drop (49 blocking lost) in `superclaude review merge`/`ledger.py`; check whether fixed; compare with `cluster_v2` and the debate; decide which merge serves which consumer (revise-loop consumers vs single-pass reflect).
4. **Finding format unification** — findings-v1 (`findings.py`) vs findings-v2 (`findings_v2.py`, roles/lenses/channels/deviation classes) vs reflect cards vs spec-panel ledger rows; need a lens for tasklist, PR code review, rf-qa; build the finding-level T-9 checker (NOT BUILT).
5. **Shadow-run exit diagnosis for runs 08-15** — run `scripts/reflect_shadow_exit.py` full output (not tail) and classify parity/lint/EV-1 failures per run after the TS fixes; determine whether remaining failures are orchestrator-prose lapses (argues for moving shadow steps into code) or skill defects.
6. **Blind GT scoring of the 15 combo runs** (needs owner spend approval) — the only path to a quality comparison of model mixes for the reflect consumer; reuse the other study's GT and judge protocol.
7. **Generic shadow/manifest harness** — evaluate extraction plan (shadow-standalone-evaluation.md:100-123) as the rollout mechanism for all five consumers; check overlap with `cli/eval`, `scripts/eval_runner.py`, `scripts/ab_test_workflows.py` (UNVERIFIED overlap).
8. **Calibration** — per-finding numeric calibration (0/689), `confidence-calibrator` card-level output, id-matching; decide whether the central panel keeps blind calibration (MR requires it) and in what machine-readable form; relate to the other study's untested calibrator role.
9. **Orchestrator role** — speed lead (tier3 64-68 min vs tier1b 23-39 min), dispatch collapse under tier3, compliance A 0.67; define orchestrator model policy and whether dispatch should leave prose for code.
10. **Cost/worth (H-A)** — combine the other study's ceiling (~2.5/14) and "sonnet alone most catches per token" with MR's T2 cost (37/38 escalate) to decide whether the unified panel should default to fewer reviewers or fix the rubric (O-8).

---

## 7. Gaps and questions

- **UNVERIFIED (not read in this slice):** MR:146-264, 295-399, 420-499; `stop-rule/*` contents; `debate-split-pairs.md`; `lint-test-design.md`; `stage2-entry-inventory*.md`; `per-field-source-table.md`; consumer-inventory.md:41-405; `s-id-runbook.md`; all T*-checks.log; COMBO `combos.json`, `results.jsonl`, `analysis/extract.py`, `resolve/`.
- **UNVERIFIED doc claims:** `scripts/reflect_shadow_exit.py:148` string compare; SKILL.md:338-349 shadow steps, :714/:1955 EV-1; `panel_lint.py:271`; `findings.py:29` `refs_norm`; whether commits `9874d63fb`/`c2e3347d3` implement the TS fixes.
- **Other study** facts in section 5 are second-hand via COMBO/PLAN.md:6-38.
- **Issues #525-#530** (owner hand labels): not found locally; not checked on GitHub.
- **Rationale for `CLAUDE_CODE_PRINT_BG_WAIT_CEILING_MS=0`** and the exact "user-level CLI install" procedure: not documented in the files read.
- **Exit script head** (EV-1 counts, per-run reasons) not captured — only `tail -25` was run as instructed.
- Q: Why does the exit script's compliance mean cover 9 runs when 13 are counted? (Likely older runs lack the telemetry key — UNVERIFIED.)
- Q: shadow01-03 reuse one package (`detachTheCcsessi-20261102-034618`); is that intended repetition or test runs? Does the Stage 2 exit require 20 distinct packages?
- Q: Untracked `.dev/eval-workspaces/shadow-model-combos/runs/...comboC-r3/artifacts/base-e8db2fe6/` contains a Makefile for an unrelated project (`neural-cli`) — what wrote it and does it indicate a reviewer read outside the input snapshot? (Seen via Grep only.)
- Q: MR's anthropic-only environment gate (MR:411) vs the gateway-only availability of the other study's best panel: which environment will the central panel target?
- Q: Is the MR still "draft-for-owner-review" (MR:7), or was it approved before Stage 0-2 shipped in #519?

---

## Summary

This session produced one accepted-in-practice design (architecture C, MR), a fully reviewed Stage 0-2 implementation package (final review 7 pass), and measurements that mostly show **recording and identity problems, not quality results**. Measured: legacy card conversion 67.28% (gate redefined to brief-compliant cards, unmeasured); AI-labelled cluster pair precision 0.84 / recall 0.95 (not human); 0/689 numeric calibrations; 13 of 20 shadow runs with Stage 2 exit FAIL (EV-1, parity, lint), compliance 0.704; parity/EV-1/compliance root causes are orchestrator prose-following lapses and an under-specified brief; the "haiku" slot is served by `gpt-6.1-sol` on this gateway and the panel record cannot see it; dispatch can collapse to one model when the orchestrator omits the class. The 5x3 combo study gives leads (orchestrator speed, confidence shift, compliance) but no quality answer because blind GT scoring was not approved. Open: Stage 0 exit (hand labels, redefined gate), Stage 2 exit (7 more runs and fixes), pilot stop rule and spend, blind scoring. Overlaps with the other session: both found input (source/spec) and model-identity problems; recommendations partly conflict (gateway Luna panels vs anthropic-only gate); merge and role coverage are complementary.

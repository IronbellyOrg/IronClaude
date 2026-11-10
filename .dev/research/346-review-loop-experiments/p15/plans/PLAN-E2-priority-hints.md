# PLAN-E2: additive first-review reading priorities (Jev hints vs static hints vs conventional router)

Question (report E2): at equal reviewer attention, do Jev-ranked passage-pair hints given to the FIRST review yield more independently verified blockers than deterministic (static) hints or a conventional LLM router? Hints are additive: every arm reviews the complete document under the unchanged rubric; Jev labels supplied relationships only (never findings, never severity); Jev as a coverage FILTER is a no-go and is not built. Three stages, each gated: Stage 0 headroom falsifier (no paid calls), Stage 1 replay (Jev, static, conventional on shared candidates), Stage 2 live (18 Sonnet + 12 Haiku runs). Read this file, `$SP/p15/plans/SHARED-CONTRACT.md` (binding) and PLAN-0 section 4. PLAN-0 must be READY first.

## 0. Rules and roles

Contract J1-J3, J11: no key, no live call, no subagents for you; `uv run --no-project` only; write only under `$E2` and your clone. Sessions: **Session 1:** Stage 0 code + 24 cases + prompts -> READY-S0. **Coordinator phase 0:** labeling, `stage0.py` -> GO-REPLAY / NO-GO-OFFLINE. **Session 2 (only after GO-REPLAY):** Stage 1 datasets and replay tooling -> READY-S1. **Coordinator phase 1:** labeling, conventional router replay, calibration + held-out Jev replay -> GO-LIVE / NO-GO-OFFLINE. **Session 3 (only after GO-LIVE):** live harness -> READY-S2. **Coordinator phase 2:** live runs and analysis.

```bash
export SP=/tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad
export JEV=$SP/p15/jev E2=$SP/p15/e2 CLONE=$SP/p15/clones/jev2 BR=346Claude-jev-e2-priority-hints
```

## 1. Background

- Baseline arm A (contract J0): `B_BLK` 1.50; about 5 of the 9 first-audit blockers were themes the run's own R1 never reported ("never found"; `$SP/p13/plans/REVIEW-OF-SOLUTIONS.md` section 1); recurring audit themes T1 (Phase 1 / AC-1.1 scope vs `/sc:load` rows and command counts), T2 (WC-4 path `<output-dir>/return-contract.yaml` vs per-command report paths), T3 (AC-0.4 needs the WC-4 contract status of 7.2 step 3, which Phase 1 introduces). Theme regexes: `$SP/p12/ab2/score_themes.py THEMES`; defect catalog with anchors: `$SP/p13/catalog/catalog.json`.
- Expectation stated up front: T2 is a path collision and T3 an explicit cross-reference, both of which static rules (explicit references, shared paths/ids) should already rank; Jev headroom is most plausible for novel defects without lexical links. Stage 0 exists to find out cheaply. Every live run reviews the SAME S1 spec, so each arm's hint list is effectively one fixed artifact; the live test measures whether that list helps reviewers on S1, and generalization rests on the replay.

## 2. Shared machinery (code; identical for all routers)

`$E2/extract.py`: `extract(doc_text) -> list[Passage]` with `Passage(pid, section_no, section_title, line_start, line_end, kind: heading|paragraph|list_item|table_row, text (exact bytes), ids_defined, ids_referenced, section_refs, paths, numbers_with_units)`; table rows carry their header row in `context`; occurrence-specific ids (`P0012`) are stable for identical input. `$E2/candidates.py`: `exhaustive(passages)` (n(n-1)/2, counted, never sent anywhere), `prefilter(passages, cfg) -> list[Pair]` keeping pairs with an explicit reference, a shared id, a shared backticked term or path basename, a shared number+unit word, or >= 2 shared rare content words (IDF within the document), then capped at `pool_cap` pairs by a deterministic prefilter score (frozen in `decision.toml`; Stage 0 value 150). All routers see the same pool. `$E2/static.py`: static ranking = explicit-reference pairs, then shared id across different sections, then shared path basename, then a frozen diverse distant-pair sample (`random.Random(seed)` over the remaining pool, stratified by section distance), tie-break by section distance (descending) then pid. `$E2/hints.py`: `render(ranked_pairs, budget_tokens=1200, max_pairs=12) -> str` (one item per pair: rank, both locators `section N.N "<title>" lines a-b`, a code-written reason; items added greedily in rank order until the next one would exceed 1,200 tokens (bytes/4); an item is never truncated; identical format for all routers). Unavailable or invalid routing -> the hint list falls back to original reading order (the first 12 pairs in document order), never to deletion or PASS.

## 3. Stage 0: headroom falsifier (no paid calls)

### 3.1 Cases (24; `$E2/offline/cases/s0/`)

- 6 real-theme cases on the ORIGINAL S1 spec (`data_classes = {"s1_spec"}`): T1, T2, T3 and the three largest "other" catalog clusters; the minimal evidence set (2-3 passages whose joint reading shows the defect) is authored from the catalog anchor and member quotes.
- 6 seeded S1 variants: a new contradiction inserted between distant sections (2), an impossible acceptance check (1), a reference chain A -> B -> C where only the chain shows the defect (2), a global vs per-row path collision with no shared basename (1).
- 8 synthetic mini-specs (`synthetic`, 400-1,200 words) with one seeded defect each: novel defects without lexical links (3), exception-vs-rule pairs that ARE conflicts (2), reference chains (2), unit mismatch (1).
- 4 synthetic clean controls: look-alike overlaps (same words under different conditions; an explicit exception that resolves an apparent conflict).

Each case: `{"doc": <path>, "evidence_set": [pid...] (empty for clean), "defect": "<one sentence>", "author_intent": {...}}`. Labelers (contract J8; L1 sonnet, L2 haiku, ADJ sonnet; 3 batches of 8) see the document and the proposed evidence set and answer: `defect_real` (blocking per the grading check: yes/no), `evidence_sufficient` (the set alone shows it: yes/no), `evidence_minimal` (no member can be dropped: yes/no), `other_blocker` (another blocker they noticed: quote or none). Truth = adjudicated; a case whose evidence set is judged insufficient is corrected by ADJ (ADJ may name the missing passage) or dropped and listed.

### 3.2 Measures (`$E2/stage0.py`, code only)

Per defect case: extraction coverage (every evidence passage text is contained in one extracted passage), candidate coverage (every must-read pair of the evidence set is in the pool), static coverage at 12 (in the rendered static hint list). `H` = defect cases whose must-read pair is in the pool but NOT in the static top-12 (headroom a better router could use).

### 3.3 Rules

- Extraction loses any required evidence -> STOP, fix `extract.py`, rerun, report both passes (no data from the failed pass is used).
- `H == 0` (static already finds every useful relation at the intended attention) -> **NO-GO-OFFLINE** (no demonstrated Jev headroom; report rule). Stage 1 and Stage 2 not run; E2 live rows `BLOCKED`.
- `H >= 1` of 20 defect cases (>= 5%, the miss rate the replay gate of +8/160 needs) -> **GO-REPLAY**. Report candidate-pool misses separately (they hurt every router equally; if pool misses > 2, raise `pool_cap` or extend the prefilter BEFORE Stage 1 and rerun Stage 0).

## 4. Stage 1: replay (only after GO-REPLAY)

### 4.1 Data (`$E2/offline/cases/{cal,heldout,chal}/`)

Six strata: S-a cross-section conflicts, S-b impossible checks, S-c global/per-row path collisions, S-d novel defects, S-e clean overlaps / exceptions / different conditions, S-f insufficient evidence (the pair needs a third passage). 120 calibration (20 per stratum) + 240 held-out (40 per stratum; defect strata a-d = 160) + 40 conditional three-passage challenges (held-out). Sources: synthetic mini-spec families (each family a document with several seeded variants; one family = one group) and S1 seeded variants (grouped per seeded edit family). `split_groups(seed=2)` by family BEFORE variants. Labels: contract J8, batches of 10 (about 80 labeler steps + ADJ).

### 4.2 Jev questions (`$E2/questions.py`, `QSET_VERSION = "e2-q1"`; one request per candidate pair; state = `{"passage_a": {"text", "section"}, "passage_b": {"text", "section"}, "facts": {"a_refers_to_b": bool, "b_refers_to_a": bool, "same_section": bool}}`)

| Name | Type | Instructions | true | false |
|---|---|---|---|---|
| `same_behavior` | Noul | Do `passage_a.text` and `passage_b.text` set rules for the same behavior of the system? | Both passages set rules for the same action, file, command or state of the system. | The passages set rules for different actions, files, commands or states. |
| `incompatible` | Noul | Do `passage_a.text` and `passage_b.text` require incompatible outcomes in some situation? | There is a situation in which following `passage_a.text` breaks `passage_b.text`. | In every situation both passages can be followed together, for example because they apply under different conditions. |
| `context_sufficient` (companion) | Noul | Can `passage_a.text` and `passage_b.text` be compared without reading another part of the document? | The two passages are understandable on their own for comparing them. | Comparing them needs a passage they refer to, such as a section, table or definition named in them. |

(The report's Choices `{related, unrelated, insufficient_evidence}`, `{incompatible, compatible, insufficient_evidence}`, `{sufficient, requires_referenced_text, uncertain}` become these Nouls; contract J7.) `context_sufficient < t_ctx` and an explicit reference in either passage -> code retrieves the referenced passage exactly and asks a LATER call with the three-passage state (`passage_c`); its answers replace the pair's. Jev never sees the whole document, never names findings or severity.

### 4.3 Ranking (code; `$E2/policy.py`)

Rank key (no arithmetic across probabilities): `(band(incompatible), band(same_behavior), p_incompatible, static_rank)` descending/ascending as appropriate, bands = high (>= t_hi) / mid / low (< t_lo). Thresholds `t_hi`, `t_lo` per question fitted on calibration only (grid {0.6, 0.7, 0.8} x {0.2, 0.3, 0.4}; pick the policy that captures the most must-read pairs at 12 on calibration; ties -> the one closest to 0.7/0.3), frozen in `offline/calibration-freeze.json` (sha in `decision.toml`) before any held-out call. The conventional router answers the same three judgments yes/no/uncertain (yes = 1.0, uncertain = 0.5, no = 0.0) and goes through the same key; its worker sees exactly the pairs Jev saw (2 cases per worker, held-out only; about 120 worker steps; no uncounted retries: a failed worker counts its tokens and its case falls back to document order).

### 4.4 Replay advance (pre-registered)

- **GO-LIVE** only if: Jev top-12 captures >= (static captures + 8) must-read relationships among the 160 held-out defect cases, within the same 12-pair / 1,200-token allocation; no stratum S-e/S-f case has Jev's top-12 made of pairs that exclude out-of-theme evidence (additive design: checked by asserting the complete document is always delivered; reported); API failures and fallbacks <= 5% of calls.
- Else **NO-GO-OFFLINE**. Report all four stages separately: extraction coverage, candidate coverage of minimal evidence sets, routing recall at fixed allocation (Jev, static, conventional), and (live only) reviewer discovery; plus per-stratum tables, Brier/reliability per question, Jev cost (input tokens, USD; replay ceiling 30M tokens or $5, reserved up front per contract J4), conventional router output tokens. Retain every low-ranked pair and every omission in `offline/ranked-<router>.jsonl`.

## 5. Stage 2: live (only after GO-LIVE)

Arms (fresh, interleaved; contract J0): `h2j` Jev hints, `h2s` static hints, `h2r` conventional router hints; arm A = baseline data. Hints only for R1 (first review): coordinator step `J0` (h2j: Jev over the S1 pool; needs the key, drive-jev.sh) / `S0` (h2s: code) / worker step `ROUTER` (h2r: loop model; its output tokens are loop tokens) writes `ws/.dev/orca-command-refactor/review/hints-1.md` before R1. R1 brief: `new_brief(..., values_extra=", hints=.dev/orca-command-refactor/review/hints-1.md")`. Rules insertion, identical in all three arms (anchor = the line `Write \`review: 1 of 3\` once, as the first line of the report.`; inserted after it):

```text
- **Reading priorities**: when the brief gives hints, read that file after the candidate. These are unverified reading priorities, not findings. Review the complete document under the unchanged rubric. Low rank is not evidence of irrelevance or correctness. Produce findings only from verified document evidence.
```

Re-reviews, revisions and audits are the baseline steps (audits never see hints). Jev failure or budget exhaustion in J0 -> document-order hints (fallback recorded; D6).

Rules (in order; per-audit means, so "total over 6 runs" = 6 x per-run mean of the two audits; `decision.toml [rules]`):

| Rule | Condition |
|---|---|
| DROP-1 (safety) | escalations(h2j) >= escalations(A) + 2 (A = 0), or median growth(h2j) > median growth(A) + 2.0 percentage points (A median 0.97%) |
| DROP-2 (no gain vs A) | `BLK(h2j) >= B_BLK` (1.50) |
| DROP-3 (no gain vs static) | `BLK(h2j) > BLK(h2s)` |
| INCONCLUSIVE (validity) | fewer than 5 completed runs in any fresh arm (8 at n=9); AUD vs AUD2 arm means differ by > 0.75; replica disagreement |
| ADOPT | no DROP, valid, `BLK(h2j) <= 1.50 - 4/6` (= 0.83; ">= 4 fewer total residual blockers than A across 6 runs"), `BLK(h2j) <= BLK(h2s) - 2/6` (">= 2 fewer than static"), `A_mean(h2j) <= 1.10 x A_mean(h2s)` (all-in cost within 10% of the predeclared comparator budget = the static arm; Jev USD reported apart) |
| INCONCLUSIVE | anything else (failure of efficacy is inconclusive/no-go, report) |

Then D3 (Haiku condition on `h2jh` vs the shared Haiku baseline), then D4 (+3 Sonnet for all three fresh arms, once). Cost (D2/D6): loop-only, post-hoc; `R_LOOP`/`R_B` reported per arm; the report's campaign cap ($3,055) and per-run ceilings are removed. The equal-all-in-expenditure sensitivity (static's saved router cost buying more reading) is not run (decision 5).

## 6. Files per session

- Session 1: `decision.toml` (J10.6 + `[stage0]` rules 3.3, `pool_cap = 150`, seeds), `extract.py`, `candidates.py`, `static.py`, `hints.py`, `cases_s0.py`, `prep_offline.py`, `offline_advance.py`, `ingest_labels.py`, `stage0.py` (writes `offline/stage0-results.md` and `results.json`: gate row `E2-stage0` with H, coverages; live rows BLOCKED or PENDING; `update_matrix()`), `tests/test_e2_s0.py`: `test_extract_exact_bytes_and_stable_pids`, `test_table_rows_keep_header`, `test_prefilter_rules_and_cap_deterministic`, `test_static_order_and_tiebreak`, `test_hints_budget_no_truncation_identical_format`, `test_fallback_document_order`, `test_stage0_metrics_on_toy_doc`, `test_stage0_rules`, `test_results_json_all_outcomes`.
- Session 2: `cases_s1.py`, `questions.py`, `policy.py`, `replay.py` (`--phase calibration|heldout|chal [--live]`, reservation pre-flight), `calibrate.py`, `router_prep.py`, `analyze_replay.py`; tests `test_questions_skill_rules`, `test_rank_key_no_arithmetic`, `test_retrieval_later_call`, `test_split_no_leak`, `test_mock_failure_suite`, `test_conventional_same_key`, `test_freeze_before_heldout`, `test_gate_rules`.
- Session 3: `harness.py`, `advance.py`, `analyze.py`, `insertion.txt` (`ExpConfig(root=$E2, design_id="p15-E2", pattern_root=r"p15/e2", run_rx=r"h2[jsr]h?-r\d+")`); tests: prompt identity (R1 differs from p11 only by the values sentence and the rules insertion; V/R2/R3/AUD identical), `test_hint_file_before_r1_all_arms`, `test_router_tokens_in_loop`, `test_jev_failure_document_order`, `test_key_missing_manual`, `test_haiku_loop_sonnet_audits`, `test_interleaving_three_arms`, `test_cap_6`, `test_extension_all_arms_once`, `test_rules_and_zones`, `test_results_rows` (`h2j` test; `h2s`, `h2r` control), `test_no_cost_kill`.
- READY reports follow PLAN-E1E4's format (counts, dry-run estimate and reservation, exact coordinator commands, D2/D3/D4/D6 files, skill yellow-flag check, contract deviations). Snapshot/commit/push per contract J11 after each session.

## 7. Estimates (forecasts, not limits)

| Phase | Workers | Jev | Output tokens (est.) |
|---|---|---|---|
| Sessions 1-3 | 1 Sonnet implementer each (gated) | 0 | - |
| Phase 0 | ~7 offline (6 labelers, ~1 ADJ) | 0 | ~0.1M |
| Phase 1 | ~210 offline (~80 labelers, ~8 ADJ, ~120 conventional router) | ~40k pair calls, ~16M input tok, ~$0.7 (ceiling $5 / 30M) | ~2.2M |
| Phase 2 Sonnet (18 runs) | ~126 live (per run ~6.7; +1 ROUTER in h2r) | ~150 calls/run in h2j | ~4.5M (loop ~105k/run + audits) |
| Phase 2 Haiku (12 runs) | ~84 live | | ~3.7M |
| D4 extension | ~63 live (9 runs) | | ~2.3M |

At most 6 concurrent workers in every phase. Predicted: Stage 0 likely NO-GO-OFFLINE or a small H (historical themes are lexically linked); if live runs, `R_LOOP` about 1.05 (h2j, h2s), about 1.25 (h2r with the router worker).

## 8. Risks

1. One document in live: hint lists are near-constant per arm; live n=6 measures reviewer variance under a fixed list.
2. The audit is a sonnet first review; hints that steer sonnet R1 toward audit-like themes can look good to the audit without being better in general.
3. Synthetic families authored by one implementer; grouping by family and novel stratum S-d mitigate, not remove, this.
4. Large conventional router replay (~120 workers) is the main cost; it runs only after Stage 0 headroom is shown.
5. Privacy: S1 passages go to Jev (owner's document); zero retention not activated (unknown default): recorded, not blocking.

## 9. Decisions taken

1. Choices -> Nouls + companion (contract J7); ranking by a lexicographic band key, never by multiplying probabilities.
2. `pool_cap` 150 pairs and the prefilter rules are fixed before Stage 0 and may be changed only between Stage 0 and Stage 1 (with Stage 0 rerun), then frozen.
3. Stage 0 GO threshold `H >= 1/20` (the replay's +8/160 gate implies a static miss rate of at least 5%).
4. The comparator budget for the live cost clause is the static arm (cheapest equal-attention comparator).
5. The equal-all-in-expenditure sensitivity is not run; cost columns are reported instead.
6. The conventional router replay runs on held-out only (it has no thresholds to calibrate).
7. "Current canonical" is the baseline data (not re-run); the report's 24 runs become 18 fresh Sonnet runs plus 12 Haiku runs.

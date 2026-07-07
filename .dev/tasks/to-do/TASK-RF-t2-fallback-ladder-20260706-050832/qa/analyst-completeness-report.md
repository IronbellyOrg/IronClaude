# Research Completeness Verification — Reflect Tier-2 Fallback Ladder

**Topic:** Reflect Tier-2 fallback model ladder task build (single track)
**Lens:** BREADTH — every area of the design's authoritative work breakdown must have research coverage sufficient for GRANULAR per-file/per-symbol task items
**Date:** 2026-07-06
**Analyst:** rf-analyst (completeness-verification)
**Design source:** `.dev/brainstorms/20260706-035624-reflect-t2-fallback-ladder/design.md`

**Assigned files:**
- 01-reflect-seam-inventory.md
- 02-swarm-transport-slot-inventory.md
- 03-patterns-conventions.md
- 04-test-surface.md
- 05-template-and-examples.md

**Design authoritative work breakdown:**
- §10 change map = 8 source files
- §9 test surface = 9 test files
- §12 rollout = 6 phases
- §13 open items = 4 (incl. T1-proxy needs_human_decision gate)
- Design decisions F1–F7

---

## Coverage Audit — §10 Change Map (8 source files + 2 declared no-change)

| Change-map file | Design intent | Covered by | Grounding depth | Status |
|---|---|---|---|---|
| `reflect/fallback.py` (NEW) | pure helpers + `run_fallback_ladder` | 01 §1/§2/§3 (seam, builder, diversity helpers), 03 §1 (kwarg precedent) | seam L225→226 exact; diversity helpers L641/L651/L672; reuse pattern | COVERED |
| `reflect/ensemble.py` | insert controller, capture deadline, `t2_fallback=` kwarg | 01 §1 (seam, call site L308–340), 01 §2 (def L553–569, dict L599–638) | exhaustive, per-line | COVERED |
| `reflect/models.py` | 3 defaulted `ReflectConfig` fields | 01 §5 (last field `reachability` L109, insert point), 03 §2 | exact insert point | COVERED |
| `reflect/contract.py` | none (verdict map unchanged) | 01 §4 (first-match order, `_LOAD_BEARING_BOOL_FIELDS` L48–58) | confirms no-change | COVERED |
| `reflect/commands.py` | `--no-tier2-fallback` wiring | 01 §6 (3 edit points + tmux forward L459–497) | exact, incl. tmux footgun | COVERED |
| `swarm/config.py` | T1 constants + `t1_models` + collector generalization | 02 §1, 03 §3 | exact L51/57/63/95/128/178–185 | COVERED |
| `swarm/transports/openai_compat.py` | `read_env_for_pool` (F3) | 02 §2, 04 §"§9 delta F3" | exact L98–103/159–202 | COVERED |
| `swarm/commands.py` | resolver parameterization (F1) | 02 §3 | exact L612–707, L692 map | COVERED |
| `swarm/dispatch.py` (no-change, F1 root) | slot_index root cause | 02 §4 | exact L454/L464–472 | COVERED |
| `swarm/models.py` (no-change) | WorkerStatus/WorkerResult read fields | 02 §5 | exact L69/L1110–1121 | COVERED |
| **`reflect/config.py` `resolve_config`** | **thread 3 fields + `tier2_fallback` flag** | **NONE (flagged only by 01 §5/§6 as out-of-scope)** | **zero line-grounding** | **GAP (CRITICAL)** |

The design's §10 change map lists 8 files but **omits `reflect/config.py`**, which is a mechanically required edit: `resolve_config` (def `config.py:238`) constructs `ReflectConfig(...)` at `config.py:358` and threads `isolate_reviewers=` (L380) / `reachability=` (L382). The 3 new `tier2_fallback_*` fields AND the `tier2_fallback` CLI flag (from `commands.py`) MUST be threaded through here or the flag and config fields are dead. Research 01 flags this twice ("out of this file's scope; flagged for the config researcher / task builder") but no assigned research file — and no other research file (only 01–05 exist) — line-grounds it. `research-notes.md` scope does not assign it either.

## Coverage Audit — §9 Test Surface (9 files)

| §9 test target | Covered by 04 | Status |
|---|---|---|
| test_fallback_classify.py | §1 (NEW), §3 (WorkerStatus 4-value) | COVERED |
| test_fallback_plan.py | §1 (NEW), §3 (factory routing example L207–210) | COVERED |
| test_fallback_select.py | §1 (NEW) | COVERED |
| test_fallback_slot_factory.py | §1 (NEW) | COVERED |
| test_contract_fallback_metadata.py | §1, §3 (reviewer_count witness), §4 (fixtures) | COVERED |
| test_contract.py "(existing)" | **Finding B — DOES NOT EXIST**; corrected to create-new or fold into test_verdict_mapping.py | COVERED (corrected) |
| test_ensemble_fallback_stub.py | §3 (stub/injection idioms, F1/F2) | COVERED |
| test_config.py (swarm) | **Finding A — tests/swarm/ NOT tests/cli/swarm/**; §1 asserts | COVERED (corrected) |
| test_openai_compat.py (swarm) | Finding A; §1 F3 delta | COVERED (corrected) |

Research 04 is the strongest file for breadth: it caught **two blocking design errors** (design §9 mis-pathed swarm tests to a non-existent `tests/cli/swarm/`; design labelled `test_contract.py` "existing" when it does not exist). Fixtures (`_load`, `FIXTURES_DIR`, `degraded_tier1.yaml`), conftest fixtures, and stub-injection idioms are all line-grounded (04 §2/§3/§4).

## Coverage Audit — Design Decisions F1–F7

| Decision | Covered by | Status |
|---|---|---|
| F1 slot-name fallback routing | 02 §4 (root cause exact), 01 §1 (positional type) | PASS |
| F2 stamp/output seam | 01 §1 (stamp-before-normalize L216→217), 04 §3 (final_path) | PASS |
| F3 openai_compat read_env_for_pool | 02 §2 (exhaustive), 04 §"§9 delta" | PASS |
| F4 shared run-deadline wall-clock | 01 §1 (deadline-capture point in preamble L194–209) — but `runner.py:508–513` "no outer timeout" rationale and `_monotonic`/`time` import NOT grounded | PARTIAL |
| F5 contract.py-vs-ensemble.py split | 01 §2 (build_reflect_contract in ensemble.py, exhaustive) | PASS |
| F6 first-match degraded reason | 01 §4 (T6 before T10 exact L271–272 vs L288–289) | PASS |
| F7 tests/cli paths | 04 Finding A — F7 OVER-corrected swarm rows; research corrects it | PASS (corrected) |

## Coverage Audit — §12 Rollout (6 phases) & §13 Open Items (4)

| Item | Covered by | Status |
|---|---|---|
| Rollout 1 (fallback.py helpers + unit tests) | 01, 04 | COVERED |
| Rollout 2 (additive kwarg + contract tests) | 01 §2, 03 §1, 04 | COVERED |
| Rollout 3 (wire controller + deadline + stub) | 01 §1, 04 §3 | COVERED |
| Rollout 4 (T1 swarm slot resolution + tests) | 02, 04 | COVERED |
| Rollout 5 (real dispatch + confirm ~/.aienv T1Model0N) | research-notes G1 only; NOT in assigned files | GAP (see G-2/G-3) |
| Rollout 6 (`--no-tier2-fallback` + **docs**) | 01 §6 (flag); **docs — no doc-file inventory anywhere** | PARTIAL (docs ungrounded) |
| §13.1 Proxy binding / needs_human_decision | research-notes G1 (supersedes design); 05 §L5 generic | GAP (contradiction — see G-2) |
| §13.2 resolver parameterization | 02 §3 | COVERED |
| §13.3 wall-clock accounting | 01 §1, design §7.4 | PARTIAL (see F4) |
| §13.4 diversity-helper import cycle | 01 §3 (helpers + `_vendor_from_model_id` move-together note) | COVERED |

## Area-by-Area Verdict (spawn prompt's 7 focus areas)

1. **reflect/ seams** — PASS. Ensemble seam, `build_reflect_contract` kwarg (def in ensemble.py, not contract.py), models.py fields, contract.py no-change, commands.py flag all line-grounded (01 §1–§6). **Exception:** `resolve_config` threading un-grounded (see G-1).
2. **swarm/ seams** — PASS. config.py collector+t1_models, openai_compat read_env_for_pool (F3), commands.py resolver, dispatch.py F1 root, models.py no-change all exact (02 §1–§5).
3. **New fallback.py helpers** — PASS. Each of the 6 helpers has enough grounding: classify (WorkerStatus 02 §5), evaluate_quorum (diversity helpers 01 §3), plan_next_attempt (F1 02 §4), select_contributing_set (design §4.2 pure logic), make_fallback_slot_factory (F1 02 §4), run_fallback_ladder (seam+stamp/normalize 01 §1, dispatch/normalize seams 04 §3).
4. **9 test files + fixtures/injection** — PASS. Exhaustive (04); 2 design path errors caught.
5. **MDTM template 02 + POST gate + frontmatter** — PASS. Template structure, B2 self-contained rule, POST reflect wrapper item (exact skip-guard + command), `start_commit`/`executor_model_class` CLI-mode keys, QA gate encoding all grounded (05). **Minor:** 05 header says "Status: In Progress" while footer says "Status: Complete."
6. **T1-proxy needs_human_decision gate + wall-clock F4 + circular-import G2** — MIXED. Circular-import G2 = PASS (01 §3). Wall-clock F4 = PARTIAL (F4 above). needs_human_decision/T1-proxy = **GAP + CONTRADICTION** (G-2): assigned files 02/03 propagate the design's superseded "reuse T2 proxy" default; research-notes G1 says distinct `T1ProxyUrl`/`T1ProxyKey`/`T1Model01`/`T1Model02` exist and supersede it — but no assigned research file grounds those env names or the HALT-item encoding.
7. **Granularity (per-file/per-symbol)** — PASS overall; the two exceptions are G-1 (resolve_config, no grounding) and G-2 (proxy binding, contradictory grounding).

## Contradictions Found

- **C-1 (proxy binding — assigned files vs authoritative plan).** Research **02 §2 (L88, L97)** and **03 §5 (L209, §7.3 echoes)** recommend the T1 fallback transport **reuse the T2 proxy envs** — `read_env_for_pool(model_prefix="T1Model0", proxy_url_env=T2_PROXY_URL_ENV, proxy_key_env=T2_PROXY_KEY_ENV)` — faithfully mirroring design §7.3/§13.1's *default* branch. **`research-notes.md` G1 (L44) SUPERSEDES this**: it states env grounding shows `T1ProxyUrl` + `T1ProxyKey` + `T1Model01`/`T1Model02` all exist as distinct env-var names, and the correct binding is `proxy_url_env="T1ProxyUrl", proxy_key_env="T1ProxyKey"`. A builder that follows assigned files 02/03 would wire the **wrong proxy env names**. This contradiction is surfaced, not resolved here — but the authoritative resolution (per research-notes + the design's own conditional "if ~/.aienv proves a distinct T1 proxy contract") is the **T1ProxyUrl/T1ProxyKey** arm, gated behind a needs_human_decision HALT.

## Documentation Staleness

No doc-sourced architectural claims requiring `[CODE-VERIFIED]`/`[CODE-CONTRADICTED]` tags were found — all five files are code-traced against the live worktree with file:line evidence. Files 01, 02, 03, 04 state "no Unverified items." File 05 grounds against template/SKILL.md/prior-task files (all present in-tree). No stale-doc flags. (Note: the design.md itself carries stale/over-corrected guidance — §9 swarm paths, §10 change-map omission of `reflect/config.py`, §13.1 superseded proxy default — but research 04/01/research-notes correctly caught the first two; the third contradiction, C-1, is only partially propagated.)

## Completeness (per-file)

| File | Status field | Summary | Gaps/Questions | Key Takeaways | Rating |
|---|---|---|---|---|---|
| 01-reflect-seam-inventory | Complete | Yes (§Summary) | "Unverified: none" | Yes (numbered summary) | Complete |
| 02-swarm-transport-slot-inventory | Complete | Yes | Yes (per-section) | Yes (Summary) | Complete |
| 03-patterns-conventions | Complete | Yes (Summary of load-bearing conventions) | implicit | Yes | Complete |
| 04-test-surface | Complete | Yes (Builder cheat-sheet) | Yes (2 blocking findings) | Yes | Complete |
| 05-template-and-examples | **In Progress (header L3) / Complete (footer L199)** | Yes (Builder handoff summary) | implicit | Yes | Complete-content, inconsistent status stamp |

## Depth Assessment

**Expected depth:** Deep (per-file/per-symbol granularity for a code+tests CLI change). **Achieved:** Strong. Every in-scope symbol carries exact current line numbers (re-Read 2026-07-06), delta tables vs design.md line cites (01 §0), root-cause tracing (F1 in 02 §4), and test-injection idioms (04 §3). **Missing depth elements:** (a) `reflect/config.py resolve_config` entirely un-line-grounded; (b) the actual `~/.aienv` T1-proxy env-var grounding lives only in `research-notes.md` G1, not in any evidence-bearing research file; (c) F4's `runner.py`/`_monotonic` citations from design §7.4 not independently re-grounded; (d) rollout-step-6 doc surface not inventoried.

---

## Compiled Gaps

### Critical Gaps (block granular task-building)

- **G-1: `reflect/config.py` `resolve_config` threading is un-grounded and absent from the design §10 change map.** `resolve_config` (def `config.py:238`) builds `ReflectConfig(...)` at `config.py:358` (threads `isolate_reviewers=` L380, `reachability=` L382). The 3 new `tier2_fallback_*` fields + the `tier2_fallback` CLI flag MUST thread here or the CLI flag and config fields are inert. No assigned research file (nor 01–05 collectively, nor research-notes) line-grounds this required edit. Research 01 §5/§6 flags it as "out of scope, flagged for config researcher / task builder" — that hand-off was never fulfilled. **Impact:** the builder cannot write a B2 self-contained, line-anchored per-symbol item for a required edit; the design's own change map would under-count files (8 → 9).

### Important Gaps (affect correctness / quality)

- **G-2: Proxy-binding contradiction (C-1) leaves the T1 transport wiring ambiguous.** Assigned files 02/03 carry the design's superseded "reuse T2 proxy" recommendation; `research-notes.md` G1 says distinct `T1ProxyUrl`/`T1ProxyKey` exist and must be used. No assigned research file grounds the `T1ProxyUrl`/`T1ProxyKey` env-var names or reconciles the two. **Impact:** a granular `read_env_for_pool(...)` item built from 02/03 would pass the wrong `proxy_url_env`/`proxy_key_env`. Must be reconciled toward the G1 (T1-specific) arm before building the rollout-step-4/5 items.
- **G-3: The needs_human_decision HALT gate (§13.1 / rollout step 5) encoding is only partially grounded.** research-notes G1 specifies it must be a `needs_human_decision` HALT before real dispatch, and 05 §L5 gives the generic conditional-action pattern — but no assigned research file grounds (i) the `~/.aienv` probe command/expected env names driving the decision, or (ii) the PENDING-write + halt semantics required by project convention (memory `feedback_human_decision_items_must_halt`: such items must write PENDING + halt, never auto-default). **Impact:** risk of the builder auto-defaulting the proxy choice instead of emitting a true HALT item.

### Minor Gaps (should be fixed)

- **G-4: File 05 status stamp is inconsistent** — header `Status: In Progress` (L3) vs footer `Status: Complete` (L199). Content is complete; the header stamp should be corrected so the completeness gate is not tripped by a stale marker.
- **G-5: Rollout step 6 "docs for reflect reviewer behavior" has no doc-file inventory** in any research file. If the task must update user-facing docs, the builder has no grounded target path. (Design itself is vague here; may be legitimately deferrable.)
- **G-6: F4 wall-clock rationale not independently re-grounded.** Design §7.4 cites `runner.py:508–513` (no outer `ClaudeProcess` timeout) and a `_monotonic()` helper; 01 grounds only the ensemble.py deadline-capture *point*. The `runner.py` claim and whether `ensemble.py` already imports `time.monotonic` are unverified. Low risk (the seam is grounded; the citation is not).

## Recommendations (before task-building proceeds)

1. **Close G-1:** spawn a short supplementary research pass (or fold into the builder's Phase-1 live-anchor step) that line-grounds `reflect/config.py:238–383` `resolve_config` — the exact kwarg insertion points mirroring `isolate_reviewers=`/`reachability=` — and add `reflect/config.py` as the 9th change-map file. This is the one gap that genuinely blocks a granular required-file item.
2. **Close G-2/G-3:** reconcile C-1 explicitly. Adopt the `research-notes.md` G1 resolution (`T1ProxyUrl`/`T1ProxyKey`, `T1Model01`/`T1Model02`) as authoritative over assigned files 02/03's "reuse T2 proxy" wording, and encode the `~/.aienv` confirmation as a true `needs_human_decision` HALT item (PENDING-write + halt, per project convention) placed before rollout-step-5 real dispatch. Note in the tasklist that stub-transport rollout steps 1–4 do NOT depend on this and may proceed.
3. **Close G-4:** correct file 05's header status stamp to `Complete`.
4. **Optionally close G-5/G-6:** during Phase-1 grounding, inventory any reflect reviewer-behavior doc target (or record "no doc update in scope"), and re-Read `ensemble.py` preamble + `runner.py:508–513` to confirm the F4 deadline mechanics.

---

## VERDICT: FAIL — 6 gaps (1 Critical, 2 Important, 3 Minor) + 1 Contradiction

**Breadth coverage is otherwise strong:** all 8 §10 change-map files, both declared no-change files, all 9 §9 test files, all F1–F7 decisions, the circular-import guard (G2), the two-view ledger model, and the full MDTM template/POST-gate/frontmatter surface are line-grounded — and research 04 additionally caught two design-level path errors (non-existent `tests/cli/swarm/`; non-existent `test_contract.py`). The failure is **localized to two seams the design's own §10 change map under-specifies**: the `reflect/config.py resolve_config` threading (G-1, entirely un-grounded, absent from the change map) and the T1 proxy-binding decision surface (G-2/G-3, where assigned files 02/03 carry a recommendation that `research-notes.md` G1 supersedes). Both are targeted fixes — a small `config.py` grounding pass plus a contradiction reconciliation — not a full re-research. Recommend addressing G-1, G-2, G-3 before the builder writes Phase-2 source-edit items and the rollout-step-4/5 items.

**[PARTITION NOTE]** Single-instance analysis (no `assigned_files` partition beyond the 5 named research files, which constitute the full research set). Cross-file checks (contradiction detection, coverage audit) were run across all 5 assigned files plus `research-notes.md` and the design; no merge with sibling partitions is required.


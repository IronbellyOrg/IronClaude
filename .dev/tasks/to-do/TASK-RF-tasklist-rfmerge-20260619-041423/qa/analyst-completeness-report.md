# Research Completeness Verification — Partition A (BREADTH lens)

**Topic:** sc:tasklist RFMerger P1–P5 implementation build
**Date:** 2026-06-19
**Analysis type:** completeness-verification
**Lens:** BREADTH (does every area a builder needs get covered across the 4 assigned files?)
**Partition:** A of (multi) — assigned files only
**Files in scope:**
- 01-skill-stage-map.md
- 02-skill-conventions.md
- 03-integration-contracts.md
- 04-proposal-attachment-trace.md

> [PARTITION NOTE: Cross-file checks limited to assigned subset. Full cross-file analysis (contradictions across ALL research files, coverage audit against full scope) requires merging all partition reports.]

---

## File completeness (sanity pass)

All 4 assigned files are `Status: Complete`, dated 2026-06-19, with a clear scope line, evidence-rich body, and a summary/cross-boundary section. No `In Progress` files, no truncation, no empty sections. Every research file carries explicit `file:line` evidence for nearly every claim (R03 closes with "No 'Unverified' items"; R02 flags its 2 unverified items explicitly; R01/R04 flag cross-researcher boundaries). Evidence quality across the partition is STRONG.

---

## Lens checklist (7 items)

### Check 1 — Each of P1-P5 has a pinned attachment point (file + current line) in current SKILL.md

**PASS (strong).** Every proposal has a pinned primary anchor with a verbatim line quote, given independently by R01 (static stage map) and R04 (data-flow single-best-anchor), which cross-corroborate:

- **P1 Execution Context** — R01: task-body `SKILL.md:894-927`, insert near `**Steps:**` (:904) / after `**Notes:**` (:927); mirror `templates/phase-template.md:55-82`. R04 places the *emit surface* in the **index** (`### Index File Template`, after Artifact-Paths table `SKILL.md:707`, before `#### Phase Files Table` :709). R03 pins the REUSED contract (task-builder `SKILL.md:1066-1071,1231,1389`).
- **P5 Tier Calibration Advisory** — R01 + R04 agree: index template, after `#### Feedback Collection Template` (ends `SKILL.md:839`), before `#### Glossary` (:841). Anchors :822,:826.
- **P4 gate-results.txt** — R01/R04: serialize after `SKILL.md:1187`; inject into Stage-7 agent block after `:1268` before Drift check (:1271), or per-agent spawn payload `:1255-1261`.
- **P3 synthetic-dnsp** — R01/R04: orchestrator merge `SKILL.md:1288-1295` (new step after :1292) + replace stage-gate retry clause `:1310`.
- **P2 bounded loop** — R01/R04: replace no-loop gate `SKILL.md:1456` (origin) → loop back to Stage 9 `:1413`/`:1427`; fence note `:1462`.

> ATTENTION (inter-file discrepancy to surface, not a coverage gap): **P1's emit surface is described in TWO different places.** R01 §A/§E puts the P1 block in the **phase-file task body** (`SKILL.md:894-927`, mirror `phase-template.md:55-82`) — i.e. PER-TASK. R04 §P1 emits it in the **index** (`tasklist-index.md`, after :707), and R03's reused task-builder contract is a single `## Execution Context` section "immediately after Prerequisites & Dependencies" (per task FILE). This is a genuine **per-task-body vs per-index-section placement ambiguity** the builder must resolve before writing P1 checklist items. Both anchors exist (coverage is present), but they are **contradictory on placement** — flagged under Check 7 and Contradictions.

### Check 2 — Reused contracts documented with field-level detail sufficient to conform without forking

**PASS (very strong).** R03 is the field-level authority and is exhaustive:

- **DM-003 (P3)** — full 7-field table with Fixed/Dynamic, exact values, line numbers, AND the reject-symbol per field (`DM-003-fixed-field-invariant-violation` etc.), task-builder `SKILL.md:873-911`. Closed exhaust vocab `{retry-1,retry-2,gap-fill-round-1,gap-fill-round-2,gap-fill-round-3}` quoted. R-122 Path A/B/C, strictly-additive merge (R-126), HIGH-non-overridable, INV-021, INV-012 within/cross-cycle all documented. The "8 vs 7 fields" framing is reconciled (§1.1: 7 named YAML fields, dedup_key is a 2-tuple). The byte-stable `rf-team-lead's Fix Cycles rule` sha256 pin is captured.
- **Execution Context (P1)** — 3 sub-fields (References / Source areas / Key constraints), no-file:line-in-header rule, TB-Add-7 ⇄ TB-Add-8 (INV-015), References-only degradation. `SKILL.md:1066-1071,1231,1383,1389-1390`.
- **PR-02 (P2)** — both guards, regression>monotonicity precedence, byte-exact halt strings (with the em-dash caveat), F-set = post-dedup cardinality, 4-step ordering, full-set re-validation, independent counters. `SKILL.md:1261-1305`.

R03 §1.8 adds the **reuse-vs-fork boundary** (Stage-7 reuses the wire/merge contract verbatim but MAPS `affected_range`/cohort to its 2N fan-out unit) — the single most important conformance nuance, explicitly characterized. **More than sufficient to conform without forking.**

### Check 3 — Stage 10.5 non-overlap boundary for P2 characterized

**PASS (strong).** R03 §4 gives a full disjointness proof obligation: P2 (PR-02) operates on QA-gate FAIL-verdict F-sets inside Stages 7-9; Stage 10.5 reflect-pre operates on spec-coverage gaps post-Stage-10 against the driving spec, AUTHORS-not-runs remediation. Distinct stage + distinct finding-source + distinct remediation-ownership = disjoint. R04 §P2 adds the architectural fence (`SKILL.md:1462`) and the exact prose edit ("…the Stage 8-10 patch chain *including any P2 bounded loop-back iterations*…"). R01 corroborates. Disjointness LEVER (different reference docs / ownership) is explicit, not hand-waved.

### Check 4 — Determinism conventions for P1/P5 documented (scored tiers stay roadmap-pure)

**PASS (strong).** R02 §2 is the determinism authority: canonical phrasing "same input -> same output" (`SKILL.md:35`); scored tiers are a pure function of roadmap text (`SKILL.md:546`); priority order `STRICT(1)>EXEMPT(2)>LIGHT(3)>STANDARD(4)` (`:548`); inputs enumerated (compound phrases :550-566, keyword weights :568-595, context boosters :596-614); confidence a pure function of `max(tier_scores)` (:620-625). P5 hard constraint = read-only annotation layer, imitate the audit-first reflect gate (`SKILL.md:1477`). P1 hard constraint = derive only from already-computed deterministic metadata, no inference (imitate Stage 10.5 depth resolution `SKILL.md:1487`). R04 §P5 strengthens this with the cleanest no-feedback PROOF: `feedback-log.md` is an OUTPUT template emitted empty (`:820-839`), filled at execution time by `/sc:task`, so a P5 advisory necessarily reads a PRIOR run's log — structurally cannot influence current scored tiers. The mirror-file dual-edit rule (`rules/tier-classification.md`) is noted. **Determinism is the best-covered single dimension in the partition.**

### Check 5 — 20-check gate structure for P4 documented + the 17-vs-20 stray flagged

**PASS (strong).** R02 §5 + R01 §C + R04 §P4 all document the gate as three named sub-gates numbered contiguously 1-20: Sprint-Compat 1-8 prose (`SKILL.md:1138-1145`), Semantic 9-12 prose (`:1149-1156`), Structural 13-20 TABLE (`:1176-1185`), closing aggregate `:1187`. R02 also supplies the verdict-grammar P4's gate-results.txt should mirror (`<VERDICT> (key=val)` from `:725`/`:1477`). The **17-vs-20 stray is independently flagged by all three** (R01 §C verbatim both sides: `:1187` "1-20" CORRECT vs `:1597` "all 17 checks passed" STALE; R02 §5 + §7 caveat; R04 cross-cutting #4). R01 confirms "No other 17/20 count drift found in the Self-Check region." Implementer guidance to fix `:1597` → "20" is given. **Stray fully characterized.**

### Check 6 — Granularity sufficient for per-proposal, per-test checklist items

**PASS (with one acknowledged out-of-partition handoff).** Per-PROPOSAL granularity is excellent: each of P1-P5 has primary anchor + verbatim line + mirror-file + reject-symbols/conformance nuances + a named GAP the builder must resolve (R04's per-proposal "GAP the builder must resolve" subsections are directly checklist-item-shaped). R02 supplies the per-EDIT authoring contract (heading form, emission shape, fixed bullet counts, back-ref style) so each edit can be split into write + sync + lint items. Mechanical items (edit `src/`, `make sync-dev`, `make verify-sync`, `uv run pytest`, `uv run ruff format --check`) are enumerated (R02 §6).

Per-TEST granularity is **intentionally deferred to R05** (`05-tests-and-verification.md`, OUTSIDE partition A). Each file explicitly hands test-design off: R01 §F "R05 (tests): no test files inspected"; R04 cross-cutting #5 + per-proposal gap flags ("a check must be added — overlaps R05's territory, flagged not owned"); R03 references TEST-022/D-0065 but does not own test authoring. Within partition A this is the CORRECT boundary, not a gap — but a builder needs R05 merged in for per-test checklist items. Recorded as an out-of-partition dependency, not a partition-A FAIL.

### Check 7 — Gaps where the current flow doesn't obviously support a hook are flagged

**PASS (strong).** Every non-obvious hook gap is surfaced with the builder decision called out:

- **P1:** no roadmap-ref scanner exists today; the skill only extracts the TASKLIST_ROOT token from roadmap prose (R04 §P1 GAP). Builder must either (a) restrict "refs" to the already-computed set (recommended, no-invention-safe) or (b) add a new deterministic scanner. Also: no self-check covers a new index sub-section (R04 §P1, cross-cutting #5).
- **P1 placement contradiction** (per-task-body vs per-index-section) — see Check 1 ATTENTION + Contradictions below.
- **P5:** no existing read of feedback-log during generation; must be best-effort + fenced out of the 5.3/5.4 compute path (R04 §P5 GAP).
- **P4:** no on-disk serialization exists; `validation/` dir first created at Stage 8 (`:1407`) but P4 needs it at the Stage-6→7 boundary — dir creation must move/duplicate earlier (R01 §Stage-6, R04 §P4 GAP). prompts.py is explicitly NOT the injection site (R04).
- **P3:** retry primitive `:1310` is binary success/error; must split some-vs-zero branch; Stage-8 short-circuit `:1316` must NOT fire when a synthetic HIGH exists (R01 §Stage-8, R04 §P3 GAP). No typed `StageError` exists — new implementation-time decision, CONFIRMED via grep (R03 §1.9).
- **P2:** Stage 10 today is a cheap targeted re-read, NOT a full re-validation; `F_k` requires invoking the Stage-7 2N fan-out — changes Stage 10's character + needs new iteration state (k, |F_{k-1}|, regression set) (R04 §P2 GAP). `sc:task-unified` is NOT a real name — must delegate to `sc:task` (R03 §5.3, CONFIRMED via grep).

These are the load-bearing "the flow doesn't obviously support this" flags and they are all present.

---

## Contradictions found (within partition A)

1. **P1 emit-surface placement: per-task-body (R01) vs per-index-section (R04/R03).** R01 §A/§E: phase-file task body `SKILL.md:894-927`, mirror `phase-template.md:55-82`. R04 §P1 + cross-cutting #2: index file, after Artifact-Paths `:707`. R03 §2.1: a single `## Execution Context` section per task FILE "immediately after Prerequisites & Dependencies" (the reused task-builder shape). These are three subtly different homes. NOT resolved silently — surfaced for the builder/orchestrator. Likely both are partially right (task-builder's contract is one section per task FILE; sc:tasklist may want it index-level), but the builder MUST pick one before authoring P1 items. **Important (affects P1 item structure), not Critical (P1 is still buildable once decided).**

2. **SKILL.md line-count: 1632 (R01) vs 1631 (R02/brief).** R01 §intro explicitly flags Read reported "1632 total" and instructs "cite 1632"; R02 header says "1631 lines". Minor — does not affect any anchor (all anchors are well within both counts) but the off-by-one should be reconciled to 1632 (R01 verified via Read).

No other contradictions detected within partition A.

---

## Compiled gaps (partition A)

### Critical gaps (block a clean build) — NONE within partition A

No area required by a P1-P5 builder is *uncovered* across these 4 files. Every proposal has a pinned anchor, a reused-contract field spec (P1/P2/P3), a determinism rule (P1/P5), the gate structure (P4), and a named builder-decision gap. Nothing blocks the build that is owned by partition A.

### Important gaps / decisions the builder MUST resolve (covered, but require a human/builder decision)

- **I-1. P1 emit-surface placement is ambiguous (per-task-body vs per-index-section vs per-task-file).** Three files give three subtly different homes (see Contradiction 1). The builder must decide before authoring P1 items. This is a *decision* the research surfaces, not missing data.
- **I-2. P1 "refs/source-areas" extraction does not exist today.** Builder must choose option (a) reuse already-computed set [recommended] or (b) author a new deterministic scanner (R04 §P1).
- **I-3. P3 typed `StageError` does not exist** — if a proposal wants one for zero-success, it is a NEW implementation-time decision with no prior art (R03 §1.9, CONFIRMED via grep).
- **I-4. P4 `validation/` dir creation must move earlier** (currently Stage 8 `:1407`; P4 needs Stage-6→7) (R01/R04).
- **I-5. P2 changes Stage 10's character** (cheap re-read → full 2N re-validation) and introduces loop state — builder must decide cheap-first-pass vs always-full (R04 §P2, recommends cheap first pass).

### Minor gaps (must still be fixed)

- **M-1. 17-vs-20 stale count at `SKILL.md:1597`** — fix "all 17 checks passed" → "20" as P4-adjacent cleanup (R01 §C, R02, R04 #4). Independently triple-confirmed.
- **M-2. SKILL.md line-count off-by-one** (1631 vs 1632) — reconcile to 1632 (R01 verified).
- **M-3. em-dash byte-exactness** in the PR-02 regression halt string and the DM-003 `recommendation` literal `Manual review required — partition agent failed twice` — must be a real `—`, not a hyphen (R02/R03). A test should assert byte-exactness.

### Out-of-partition dependencies (NOT partition-A gaps; flagged for the merge step)

- **O-1. Per-test checklist items depend on R05** (`05-tests-and-verification.md`) — every partition-A file correctly defers test authoring to R05 (R01 §F, R03, R04 #5). The builder needs R05 merged for per-test items. Within partition A this is the correct boundary.
- **O-2. `--spec §22` citation cross-validation** is owned by R07 (`07-citation-crossval-and-spec.md`) — R01 §B/§F + R02 explicitly defer it. Confirm R07 covers it at merge.
- **O-3. Self-check additions for new P1/P5 index sub-sections** overlap R05 territory (R04 #5) — confirm R05 owns whether a presence check is added.

---

## Depth assessment

**Expected depth:** Deep (implementation-build research — needs data-flow traces, integration-point mapping, field-level contracts, exact attachment lines).

**Actual depth achieved:** **Deep, met.** Evidence:
- **Data-flow traces:** R04 gives per-proposal in→out data shapes, "data available at emit time" tables, and traces how findings propagate Stage 7→8→9→10.
- **Integration-point mapping:** R03 maps all five reuse obligations field-by-field against task-builder/sc-reflect/sc-task source, with reject-symbols and the reuse-vs-fork boundary.
- **Exact attachment lines:** R01 + R04 both pin verbatim insertion lines (not ranges-only); they cross-corroborate.
- **Grounding rigor:** two grep-confirmed negative findings (`StageError` absent, `sc:task-unified` not a real name) prevent the builder from "reusing" nonexistent surfaces — high-value adversarial depth.

**Missing depth elements:** None within partition A. (Per-test depth is R05's, correctly scoped out.)

---

## VERDICT: PASS

Partition A (files 01-04) provides **BREADTH coverage sufficient for a builder to author P1-P5 checklist items** for everything these 4 files own. All 7 lens checks PASS. Zero critical gaps within partition. Evidence quality is STRONG with grep-confirmed negatives and triple-confirmed cross-checks.

**PASS is conditional on the orchestrator carrying forward (these are surfaced decisions / out-of-partition deps, not partition-A failures):**

1. **Resolve the P1 emit-surface placement contradiction** (per-task-body vs per-index-section vs per-task-file) — Contradiction 1 / gap I-1. Builder decision required before P1 items are authored.
2. **Merge R05** for per-test checklist items and the new-section self-check decision (O-1, O-3).
3. **Confirm R07** covers `--spec §22` citation cross-validation (O-2).
4. **Fix the minors** during the build: 17→20 at `SKILL.md:1597` (M-1), line-count 1632 (M-2), em-dash byte-exactness tests (M-3).
5. **Carry the builder-decision gaps** I-2 (P1 ref extraction), I-3 (no typed StageError), I-4 (validation/ dir timing), I-5 (Stage 10 character change) into the task file as explicit decision items.

> [PARTITION NOTE: This verdict covers ONLY files 01-04. Cross-file contradiction detection and coverage audit against the FULL research scope (incl. 05/06/07) require merging all partition reports. A finding that looks complete within partition A (e.g. test coverage) may be owned by an out-of-partition file.]

**Report path:** `/config/workspace/IronClaude/.claude/worktrees/RFMerger-Tasklist/.dev/tasks/to-do/TASK-RF-tasklist-rfmerge-20260619-041423/qa/analyst-completeness-report.md`

# Research: Release-Spec Structure Extraction

**Topic type:** Authoritative spec structure extraction (faithful, evidence-cited)
**Scope:** ONE file only — `/config/workspace/IronClaude/.dev/troubleshoot-meta/20260610T141100Z/troubleshoot-pipeline-hardening-RELEASE-SPEC.md` (v1.1.0)
**Status:** Complete
**Date:** 2026-06-11

> All citations are §section + line numbers from the RELEASE-SPEC. Tables quoted verbatim.

---

## 1. Functional Requirements FR-1..FR-13 (§3, lines 95–247)

Per-FR: wave, escape(s) closed, dependencies, mapped §8 test(s). Wave assignment comes from the FR title; escape mapping from acceptance criteria "Closes …" lines + §3.1 matrix (lines 251–257). §8 test mapping filled after §8 read (see Section 9 below for the authoritative FR→test map).

### FR-1: Applicability Gate (H0) — §3 lines 99–108
- **Wave:** H0
- **Closes/Escapes:** none directly (entry classifier); sets `pipeline_hardening_applicable`
- **Dependencies:** None (entry wave) [line 108]
- **AC1 (line 105):** When issue touches any trigger boundary (CLI/subprocess, file/stdin/prompt delivery, generated-artifact parser, gate/severity/status enum, duplicated evaluator, persisted/resume state, review/audit selector, sibling pipeline, prior-escape unmask), `pipeline_hardening_applicable=true` and H1–H5 cannot be **silently** skipped; each wave must produce `PASS`/`FAIL`/`N/A` with valid rationale/waiver feeding §5.4 aggregation.
- **AC2 (line 106):** When skipped, report records `pipeline_hardening_applicable=false`, a one-sentence reason, **AND the boundary scan** that justifies the skip (bare "looks local" is invalid).

### FR-2: Mechanism Statement (H0) — §3 lines 110–119
- **Wave:** H0
- **Closes/Escapes:** none directly (emits candidate `known_escapes_caught`)
- **Dependencies:** FR-1 [line 119]
- **AC1 (line 116):** Mechanism statement is feature-agnostic except where required as evidence.
- **AC2 (line 117):** Each candidate escape ID in `known_escapes_caught` is justified by wave/card that would catch it (see FR-12 anti-inflation).

### FR-3: Runtime-Entrypoint Verification (H1) — §3 lines 121–131
- **Wave:** H1
- **Closes/Escapes:** Closes E1; supports E4 [line 129]
- **Dependencies:** FR-1 [line 131]
- **AC1 (line 127):** H1 **FAILs** if proof stops at helper construction while defect can appear only at subprocess/gate/generated-artifact-parser/persisted-state/review-selector boundary.
- **AC2 (line 128):** Evidence card records producer · transformer(s) · consumer/evaluator · boundary crossed · replay command · evidence replay reaches production boundary · external outcome asserted.
- **AC3 (line 129):** Closes E1 (headless `--spec` replay rejects local-path `--file`), supports E4 (proves live PRD path reaches `_evaluate_gate`).

### FR-4: Negative-Witness Requirement (H1) — §3 lines 133–142
- **Wave:** H1
- **Closes/Escapes:** cross-cuts E1/E4 (negative control for forbidden interpretations)
- **Dependencies:** FR-3 [line 142]
- **AC1 (line 139):** Green H1 rejected unless a negative witness (fix reverted → FAIL) recorded for every contract with a forbidden interpretation (local path as cloud file; advisory as fatal; dirty work omitted; empty artifact accepted; non-executable heading treated as executable).
- **AC2 (line 140):** A test never observed to fail (no negative witness) does NOT satisfy H1.

### FR-5: Contract-Enumeration Ledger (H2) — §3 lines 144–154
- **Wave:** H2
- **Closes/Escapes:** Closes E4 [line 152]
- **Dependencies:** FR-1 [line 154]
- **AC1 (line 150):** H2 **FAILs** if any live consumer unclassified, if generic/shared proof used for a product path without proving product path reaches that implementation, **OR if ledger empty/zero-row** (empty ledger does NOT vacuously pass — fixes adversarial F-N3).
- **AC2 (line 151):** Ledger enumerates ≥ consumer count discovered by symbol/reference + semantic search; `dead/legacy` Role requires unreachability proof, not assertion.
- **AC3 (line 152):** Closes E4 (generic gate + PRD evaluator + trailing gate + remediation dispatch inventoried before closure).

### FR-6: Sibling / Duplicate-Evaluator Sweep (H2) — §3 lines 156–165
- **Wave:** H2
- **Closes/Escapes:** Closes E1 [line 164]
- **Dependencies:** FR-5 [line 165]
- **AC1 (line 162):** H2 FAILs if sibling pipelines/duplicate evaluators NOT swept when the concept is shared.
- **AC2 (line 164):** Closes E1 (PRD identified as sibling-contract outlier vs roadmap/tasklist/validate file delivery).
- **GAP (per task brief item 11):** FR-6 currently has only INDIRECT test coverage. User wants a NEW test `test_h2_sibling_sweep_required_when_concept_shared` added (reflect gap G-PRE-1).

### FR-7: Whole-Artifact Classifier Boundary Test (H3) — §3 lines 167–176
- **Wave:** H3
- **Closes/Escapes:** Closes E2/E3 [line 175]
- **Dependencies:** FR-3 [line 176]
- **AC1 (line 173):** Required controls: positive case (intended violation still caught), sibling/off-path negative (same-token/same-shape non-target does NOT hard-fail), full-artifact case containing both, AND a severity assertion (HALT/WARN/CONTINUE) per runtime consumer.
- **AC2 (line 175):** Closes E2/E3 (setup/work/completion/Task-Log/findings headings classified by role/topology, not position).

### FR-8: Near-Miss Negatives + Allow-List Grammar + Word-Boundary Rule (H3) — §3 lines 178–188
- **Wave:** H3
- **Closes/Escapes:** Closes E2 substring collision directly [line 186]
- **Dependencies:** FR-7 [line 188]
- **AC1 (line 184):** Phase/verdict/completion-signal/resume-token matching uses word-boundary-anchored matching (`\b` / `re.escape` / exact grammar), **promoted from appendix to first-class blocking rule** (fixes adversarial F-SC1).
- **AC2 (line 185):** Mandatory near-miss negative fixtures: `incomplete` (vs `complete`), `representation` (vs `present`), decorated/bolded verdict lines, wrong-case tokens, setext-like headings. Regex timeouts are guardrail, NOT substitute.
- **AC3 (line 186):** Closes E2 substring collision directly.

### FR-9: Unmask-and-Sweep Regression (H3) — §3 lines 190–200
- **Wave:** H3
- **Closes/Escapes:** Closes E3 [line 198]
- **Dependencies:** FR-7, FR-8 [line 200]
- **AC1 (line 196):** H3 FAILs if a fix only addresses reported repro without searching same-token/same-shape sibling surfaces, OR if heuristic parser over generated prose is hard-fatal without adversarial false-positive fixtures + cost rationale.
- **AC2 (line 197):** Sweep documents `K_swept` and asserts it covers full sibling family (fixes Quantity-Flow DIV-3).
- **AC3 (line 198):** Closes E3 (sibling-heading negative case required after E2).

### FR-10: Effective-Input Proof (H4) — §3 lines 202–212
- **Wave:** H4
- **Closes/Escapes:** Closes E5 directly [line 210]
- **Dependencies:** FR-3 [line 212]
- **AC1 (line 208):** H4 **fails closed** when effective input absent, empty despite known changes, non-reproducible, **OR non-empty but wrong surface** — correctness of `|E ∩ true_runtime_surface|` must be proven, not merely `E>0` (fixes adversarial F-D1, the real E5 mechanism).
- **AC2 (line 209):** Proof records dirty/staged/unstaged inclusion AND foreign-commit exclusion via machine-checkable manifest.
- **AC3 (line 210):** Closes E5 directly.

### FR-11: Off-Path-Reviewer Rule + Waiver Standard (H5) — §3 lines 214–223
- **Wave:** H5
- **Closes/Escapes:** supports E5 (off-path review decision)
- **Dependencies:** FR-1 [line 223]
- **AC1 (line 220):** Off-path review `required` when: CLI invokes subprocess, paths reinterpreted by another layer, generated artifacts feed later gates, persisted state affects resume, review selector chooses a surface, hard gate uses heuristic parsing, mock substitutes for runtime I/O, sibling has divergent contract, OR change controls HALT/WARN/CONTINUE/data-loss/review-integrity.
- **AC2 (line 221):** Waiver invalid if it merely says tests pass, reviewer is independent, command exists, or issue looks local.

### FR-12: Waiver-Policy / No-Re-Greening Invariant + Anti-Inflation (cross-cutting) — §3 lines 225–235
- **Wave:** cross-cutting (latch spanning H1–H5; bound to SV-15)
- **Closes/Escapes:** cross-cuts E4, E5 (no-re-green latch + anti-inflation)
- **Dependencies:** FR-3, FR-5, FR-10, FR-11 [line 235]
- **AC1 (line 231):** A `waived_with_rationale` or absent mandatory probe sets one-way `waiver_status` latch and forces `pipeline_hardening_verdict ∈ {blocked, advisory}`; NO later `task-builder`/`sc:reflect`/`adversarial` stage may upgrade to `pass`/`success` (fixes adversarial F-S1; bound to SV-15, not prose).
- **AC2 (line 232):** Production-facing pipeline-health signoff FAILs when mandatory runtime probe absent or `N/A` without rationale.
- **AC3 (line 233):** Escape ID may appear in `known_escapes_caught` ONLY if passing wave/card cited that would catch it (fixes adversarial F-A1).
- **PAIRING (per task brief item 11):** FR-12 must be paired with the NFR-4 downstream-no-re-green test.

### FR-13: Versioned Additive Output Contract + REPORT.md Closure Section — §3 lines 237–247
- **Wave:** output/reporting (consumes all H0–H5)
- **Closes/Escapes:** enables all (contract surface + report)
- **Dependencies:** FR-1 through FR-12 [line 247]
- **AC1 (line 243):** New fields (`pipeline_hardening_applicable`, `pipeline_hardening_verdict`, the 4 card/ledger path fields, `off_path_review_decision`, `known_escapes_caught`, `waiver_status`, `contract_version`) are additive; existing consumers reading prior fields do not break (backward-compat test required).
- **AC2 (line 244):** `pipeline_hardening_verdict` is a deterministic aggregation of H0–H5 statuses + `waiver_status` (aggregation function specified, not implied).
- **AC3 (line 245):** REPORT.md closure section uses `NOT PROVEN` blockers (stronger than ordinary confidence language) when any required proof is absent.

### 1.1 §3.1 Escape / Wave / Evidence Traceability Matrix (lines 251–257) — VERBATIM

| Escape | Mechanism | Closing Wave(s) | FR(s) | Required Evidence Card(s) | Backtest Scenario |
|--------|-----------|-----------------|-------|---------------------------|-------------------|
| E1 | CLI/helper proof accepted while headless subprocess rejected local paths | H1, H2 | FR-3, FR-4, FR-6 | Runtime-entrypoint card with replay reaching production subprocess; contract ledger proving sibling file-delivery consumers swept | Replay headless PRD `--spec` with local-path `--file`; negative witness fails pre-fix and positive passes post-fix |
| E2 | Substring classifier accepted `complete` inside `incomplete` and applied the wrong phase invariant | H3 | FR-7, FR-8 | Whole-artifact classifier card with positive executable violation plus `incomplete` near-miss negative | Full generated artifact containing setup/work/completion sections; only executable target hard-fails |
| E3 | Single reported heading fixed while same-token sibling headings remained unswept | H3 | FR-7, FR-8, FR-9 | Unmask-and-sweep card with `K_true`, `K_swept`, same-token/same-shape family evidence, and false-positive fixture results | Artifact containing Task-Log/Findings sibling headings; non-executable headings WARN/CONTINUE rather than HALT |
| E4 | Shared `SemanticCheck.advisory` honored by generic gate but not PRD evaluator | H1, H2 | FR-3, FR-5, FR-12 | Runtime-entrypoint card proving PRD path reaches `_evaluate_gate`; H2 ledger classifying generic gate, PRD evaluator, trailing gate, remediation dispatch | Advisory semantic check runs through PRD evaluator; ledger fails until all live consumers classified |
| E5 | Review selector consumed an adjacent/foreign range instead of dirty `/task` work | H4, H5 | FR-10, FR-11, FR-12 | Effective-input manifest proving dirty/staged/unstaged inclusion and foreign-commit exclusion; off-path review decision | POST-reflect with dirty task work plus foreign commit; H4 fails until `E ∩ true_runtime_surface` is proven |

---

## 2. Architecture (§4, lines 259–347)

### 2.1 §4.1 New Files (lines 261–270) — 6 new refs
| File | Purpose | Dependencies |
|------|---------|-------------|
| `src/superclaude/skills/sc-troubleshoot-protocol/refs/pipeline-hardening-closure.md` | Mode overview, trigger, verdict aggregation, waiver latch | SKILL.md |
| `…/refs/runtime-entrypoint-verification.md` | H1 card + negative-witness rule | pipeline-hardening-closure.md |
| `…/refs/contract-enumeration.md` | H2 ledger schema + empty-ledger FAIL rule | pipeline-hardening-closure.md |
| `…/refs/unmask-and-sweep.md` | H3 classifier boundary + word-boundary/near-miss fixtures | pipeline-hardening-closure.md |
| `…/refs/effective-input-proof.md` | H4 fail-closed (incl. wrong-surface) proof | pipeline-hardening-closure.md |
| `…/refs/hardening-output-contract.md` | Field schema, verdict aggregation truth table, waiver latch propagation contract, downstream consumer obligations | pipeline-hardening-closure.md |

### 2.2 §4.2 Modified Files (lines 272–279) — 4 files
| File | Change | Rationale |
|------|--------|-----------|
| `src/superclaude/commands/troubleshoot.md` | Advertise pipeline-hardening trigger; mention hardening evidence paths; keep thin handoff | FR-1, thin-command segregation |
| `…/sc-troubleshoot-protocol/SKILL.md` | Add mode trigger after Tier-1; wire failure states; reference new refs | FR-1..FR-13 |
| `…/refs/report-template.md` | Add `Pipeline Hardening Closure` section | FR-13 |
| `…/refs/remediation-handoff.md` | Carry hardening verdict + waiver latch into handoff | FR-12 |

### 2.3 §4.3 Removed Files (lines 281–287): NONE — purely additive.

### 2.4 §4.5 State Variable Registry — 15 variables (lines 304–318) — VERBATIM

> §4.5 line 306: "15 variables, 11 with previously-ASSUMED initial/range/invariant — each now pinned by an FR."

| Variable | Type | Initial | Invariant | Read | Write |
|----------|------|---------|-----------|------|-------|
| `pipeline_hardening_applicable` | bool | `false` | Set exactly once by H0; if `true`, H1–H5 must run or be waived | verdict aggregation, report | H0 (FR-1) |
| `pipeline_hardening_verdict` | enum `pass\|blocked\|advisory\|not_applicable` | `not_applicable` | Deterministic function of H-statuses + `waiver_status`; never upgraded post-waiver | report, downstream | aggregation (FR-13) |
| `h0..h5_status` | enum `PASS\|FAIL\|N/A` | `N/A` | `N/A` only with recorded rationale; FAIL is sticky | aggregation | each wave (FR-1,3,5,9,10,11) |
| `off_path_review_decision` | enum `required\|performed\|waived_with_rationale\|not_required` | `not_required` | `waived_with_rationale` requires a valid waiver | aggregation, report | H5 (FR-11) |
| `known_escapes_caught` | list of objects `{escape_id, wave, card_path, status}` | `[]` | Membership requires a cited passing wave/card with `status=PASS` (anti-inflation) | report | H0/closure (FR-2,12) |
| `waiver_status` | enum `none\|latched` | `none` | One-way latch: `none`→`latched` only; once `latched`, verdict ∈ {blocked, advisory} | aggregation (FR-13) | FR-12 |
| `backtest_status` | enum `not_run\|partial\|complete` | `not_run` | Production-facing coverage signoff remains advisory until E1–E5 backtests complete | report, roadmap | E1–E5 backtest gate (NFR-1) |
| `contract_version` | str (semver) | `"1.0.0"` | Monotonic; additive fields only within a major | consumers | FR-13 |
| `runtime_entrypoint_card_path` / `contract_ledger_path` / `unmask_sweep_path` / `effective_input_card_path` | str\|null | `null` | Non-null ⇒ file exists and is the proof for its wave | report | H1/H2/H3/H4 |

**CRITICAL latch/set-once notes (line 310, 315):**
- `pipeline_hardening_applicable` — **SET-ONCE** by H0 (write only at H0/FR-1).
- `waiver_status` — **ONE-WAY LATCH**: `none`→`latched` only; once latched, verdict is forced ∈ {blocked, advisory}. Never resets.
- Note: the registry table groups the 4 `*_path` vars into one row (`runtime_entrypoint_card_path`/`contract_ledger_path`/`unmask_sweep_path`/`effective_input_card_path`). Counting `h0..h5_status` (6 wave statuses) and the 4 path vars individually yields the "15 variables" total cited at line 306.

### 2.5 §4.6 Implementation Order — 7-group ordered build (lines 320–332) — VERBATIM
```
1. refs/pipeline-hardening-closure.md (mode skeleton + H0 boundary scan schema) -- foundation for all waves
2. refs/hardening-output-contract.md (verdict truth table + waiver latch propagation) -- resolves OI-1/OI-6 before downstream wiring
3. refs/runtime-entrypoint-verification.md (H1 + negative witness)   -- depends on 1-2
   refs/contract-enumeration.md (H2 + empty-ledger FAIL)             -- [parallel with 3]
   refs/effective-input-proof.md (H4 fail-closed incl. wrong-surface)-- [parallel with 3]
4. refs/unmask-and-sweep.md (H3 classifier + formal grammar + word-boundary fixtures) -- depends on 3 and the parser decision in §5.7
5. SKILL.md trigger wiring + output contract (FR-13)                 -- depends on 1-4
6. report-template.md + remediation-handoff.md                       -- depends on 5
7. Tests (§8) + make sync-dev + make verify-sync                      -- depends on 6
```
**NOTE: Group 3 is THREE PARALLEL refs** (H1 runtime-entrypoint, H2 contract-enumeration, H4 effective-input). H3 (group 4) is sequenced AFTER group 3 because it depends on group 3 + the §5.7 parser decision.

### 2.6 §4.7 Executable Validation Architecture — 6 components + test locations (lines 334–347)
| # | Component | Location | Responsibility | Required Consumers |
|---|-----------|----------|----------------|--------------------|
| 1 | Verdict aggregation contract | `refs/hardening-output-contract.md` + `tests/troubleshoot/test_hardening_verdict.py` | Define+test §5.4 truth table; reject any path mapping `waiver_status=latched`→`pass`/`success` | SKILL.md, report-template.md, remediation-handoff.md, post-run reflection/adversarial handoffs |
| 2 | Boundary scan schema | `refs/pipeline-hardening-closure.md` + H0 tests | Require typed boundary rows before `applicable=false` can skip H1-H5 | H0 dispatcher, REPORT.md closure section |
| 3 | Contract ledger validator | `refs/contract-enumeration.md` + H2 tests | Reject empty ledgers, unclassified live consumers, `dead/legacy` rows w/o unreachability proof | H2 ledger, report renderer |
| 4 | Classifier fixture harness | `refs/unmask-and-sweep.md` + H3 fixtures | Run full generated artifacts through same classifier rules; assert HALT/WARN/CONTINUE by consumer | H3 card, report renderer |
| 5 | Effective-input manifest validator | `refs/effective-input-proof.md` + H4 tests | Prove selector output intersects true runtime surface and excludes foreign/stale | H4 card, off-path review decision |
| 6 | Output-contract compatibility harness | `tests/troubleshoot/test_hardening_output_contract.py` | Validate new fields additive, nullable/defaulted as specified, older consumers still pass | Existing troubleshoot result consumers |

Line 347: test-only markdown-contract validators may live under `tests/troubleshoot/`; reusable runtime logic must live under `src/superclaude/` and be referenced here first.

---

## 3. Verdict Aggregation — §5.4 (lines 388–423) — THE CRITICAL INVARIANT

### 3.0 ⚠️ ENUM TRUTH (do NOT drop `advisory`)
`pipeline_hardening_verdict` is the FOUR-token enum **`pass | blocked | advisory | not_applicable`** (§4.5 line 311, §5.5 line 431). `advisory` is **REQUIRED**. The §5.4 truth table has **7 rows**; **ROW 5 and ROW 6 emit `advisory`**. Any claim that "advisory was removed" is FALSE and must be rejected by the builder.

### 3.1 §5.4 Verdict Aggregation Truth Table — ALL 7 ROWS VERBATIM (lines 392–400)
Preamble (lines 390): "The aggregation function is deterministic and evaluated after H0-H5. `FAIL` is sticky and outranks advisory waiver handling. `waiver_status=latched` is a one-way latch and is checked before any downstream success signal."

| Condition Priority | Input Condition | Output Verdict | Report Language | Downstream Override Allowed? |
|--------------------|-----------------|----------------|-----------------|------------------------------|
| 1 | `pipeline_hardening_applicable=false` AND H0 has reason + boundary scan | `not_applicable` | `Pipeline hardening not applicable: <reason>` | No |
| 2 | Any H1-H5 status is `FAIL` | `blocked` | `NOT PROVEN — failed hardening wave: <wave>` | No |
| 3 | `waiver_status=latched` AND any mandatory probe absent/waived without accepted substitute | `blocked` | `NOT PROVEN — mandatory runtime proof waived or absent` | No |
| 4 | Any H1-H5 status is `N/A` without rationale | `blocked` | `NOT PROVEN — unrationalized N/A: <wave>` | No |
| 5 | `waiver_status=latched` AND all mandatory probes have accepted substitutes + rationale AND no H-status is `FAIL` | `advisory` | `ADVISORY — closure relies on waived/substituted proof` | No |
| 6 | Any H1-H5 status is `N/A` with valid rationale and no failures/latch | `advisory` | `ADVISORY — scoped closure with rationalized N/A` | No |
| 7 | H0 applicable, all required H1-H5 statuses `PASS`, and `waiver_status=none` | `pass` | `Pipeline hardening closure proven` | No |

**Every row's "Downstream Override Allowed?" = No.** Rows ordered by priority (1 highest). Rows 2,3,4 → `blocked`; rows 5,6 → `advisory`; row 7 → `pass`; row 1 → `not_applicable`.

### 3.2 H5 Decision-to-Status Mapping — 4 ROWS VERBATIM (lines 404–409)
| H5 Decision | H5 Status | Waiver Status Effect | Notes |
|-------------|-----------|----------------------|-------|
| `performed` | `PASS` | `none` | Required off-path review completed and consumed the effective-input proof. |
| `not_required` | `PASS` | `none` | Pass-equivalent only when the boundary-risk scan proves no H5 trigger applies; no required proof is missing. |
| `required` | `FAIL` | `none` | Off-path review was required but not performed or validly waived. |
| `waived_with_rationale` | `N/A` with rationale | `latched` | Valid waiver downgrades final verdict through the truth table; invalid waiver maps to `FAIL`. |

**Downstream no-override rule (line 411 VERBATIM):** "Downstream `task-builder`, `sc:reflect`, `sc:adversarial`, and report-rendering stages may append findings, but they may not convert `blocked`/`advisory` into `pass` or `success`. If a downstream stage has its own success enum, the rendered result is `success_with_hardening_blocker` or `success_with_hardening_advisory`, never plain `success`, whenever this table returns `blocked` or `advisory`."

### 3.3 Backtest Status vs Run-Level Verdict — 3 ROWS VERBATIM (lines 417–421)
Line 415: `pipeline_hardening_verdict` = run-level H0-H5 closure verdict (may be `pass` when every applicable wave passes and `waiver_status=none`). `backtest_status` = separate coverage-validation state for NFR-1.

| Backtest Status | Meaning | Production-Facing Pipeline-Health Signoff |
|-----------------|---------|-------------------------------------------|
| `not_run` | No E1-E5 replay suite has run against the built hardening gates | `advisory` even if `pipeline_hardening_verdict=pass` |
| `partial` | Some, but not all, E1-E5 replay scenarios have passed | `advisory` with missing escape IDs listed |
| `complete` | E1-E5 replay scenarios all pass against the built gates | May mirror `pipeline_hardening_verdict` |

Line 423: REPORT.md MUST render BOTH fields so consumers don't confuse a clean H0-H5 run with validated E1-E5 catch-rate coverage.

---

## 4. §5.5 Output Contract Field Schema — 10 FIELDS VERBATIM (lines 427–439)
| Field | Type | Required | Default | Nullability | Producer | Consumer Behavior If Missing |
|-------|------|----------|---------|-------------|----------|------------------------------|
| `contract_version` | semver string | yes | `1.0.0` | non-null | FR-13 | Treat missing as legacy contract; do not infer hardening pass |
| `pipeline_hardening_applicable` | bool | yes | `false` | non-null | H0 | Missing ⇒ legacy/unknown; report must not claim closure |
| `pipeline_hardening_verdict` | enum `pass\|blocked\|advisory\|not_applicable` | yes when applicable known | `not_applicable` | non-null | aggregation | Missing with applicable=true ⇒ `blocked` |
| `waiver_status` | enum `none\|latched` | yes | `none` | non-null | H1-H5 / FR-12 | Missing with any waiver marker ⇒ `blocked` |
| `backtest_status` | enum `not_run\|partial\|complete` | yes | `not_run` | non-null | NFR-1 replay suite | Missing ⇒ treat production-facing signoff as `advisory` |
| `off_path_review_decision` | enum `required\|performed\|waived_with_rationale\|not_required` | yes | `not_required` | non-null | H5 | Missing when H5 required ⇒ `blocked` |
| `runtime_entrypoint_card_path` | absolute path string | required when H1 runs | `null` | nullable before H1 | H1 | Missing when H1 required ⇒ `blocked` |
| `contract_ledger_path` | absolute path string | required when H2 runs | `null` | nullable before H2 | H2 | Missing when H2 required ⇒ `blocked` |
| `unmask_sweep_path` | absolute path string | required when H3 runs | `null` | nullable before H3 | H3 | Missing when H3 required ⇒ `blocked` |
| `effective_input_card_path` | absolute path string | required when H4 runs | `null` | nullable before H4 | H4 | Missing when H4 required ⇒ `blocked` |
| `known_escapes_caught` | list of objects `{escape_id, wave, card_path, status}` | yes | `[]` | non-null list | H0/closure | Missing/empty ⇒ no coverage claim |

> NOTE: §5.5 prints 11 rows (10 distinct fields + `backtest_status`). The 4 path fields are listed individually here; `pipeline_hardening_verdict` is the 4-token enum (row confirms `advisory` is in the enum, line 431).

---

## 5. §5.6 Required Artifact Schemas (lines 441–506) — every field + required flag

### 5.1 H0 Boundary Scan Row (lines 445–452)
| Field | Required | Meaning |
|-------|----------|---------|
| `boundary_type` | yes | One of CLI/subprocess, file-stdin-prompt, generated-artifact-parser, gate-status-enum, duplicate-evaluator, persisted-state, review-selector, sibling-pipeline, prior-escape-unmask |
| `producer` / `transformers` / `consumer` | yes | Concrete components in the data path |
| `evidence_source` | yes | File, command, report, or trace supporting the classification |
| `risk` | yes | Why this boundary can admit proof substitution |
| `decision` | yes | `applicable` or `not_applicable` |
| `rationale` | yes | One sentence; `looks local` is invalid |

### 5.2 H1 Runtime-Entrypoint Card (lines 456–467)
| Field | Required | Meaning |
|-------|----------|---------|
| `producer` | yes | Component that creates the value/artifact under test |
| `transformers` | yes | Ordered list of layers that reinterpret, serialize, parse, route, or persist the value |
| `consumer_or_evaluator` | yes | Production/operator boundary that ultimately consumes the value |
| `boundary_crossed` | yes | The concrete boundary type reached by the replay |
| `replay_command` | yes | Command/scripted invocation that reaches the production boundary |
| `production_boundary_reach_proof` | yes | Evidence that the replay did not stop at a helper/mock |
| `forbidden_interpretation` | yes when applicable | The bad interpretation the negative witness must expose |
| `negative_witness_command` / `negative_witness_result` | yes | Fix-reverted or accepted-substitute run showing FAIL |
| `positive_witness_command` / `positive_witness_result` | yes | Fix-applied run showing PASS |
| `accepted_substitute_rationale` | required if no literal revert | Why captured pre-fix replay, isolated worktree revert, synthetic contract fixture, or historical log is acceptable |

### 5.3 H2 Contract Ledger Row (lines 471–478)
| Field | Required | Meaning |
|-------|----------|---------|
| `contract_token` | yes | Field/flag/parser rule/semantic check/status/predicate under change |
| `role` | yes | `producer`, `transformer`, `consumer`, `evaluator`, `dead/legacy` |
| `component_path` | yes | Source/ref/test path or generated artifact path |
| `discovery_method` | yes | Symbol/reference search, exact grep, semantic retrieval, sibling scan, fixture scan, or manual evidence |
| `classification` | yes | `classified`, `unclassified`, or `dead/legacy_with_proof` |
| `unreachability_proof` | required for `dead/legacy` | Why runtime cannot reach the component |

### 5.4 H3 Unmask / Sweep / Classifier Card (lines 482–493)
| Field | Required | Meaning |
|-------|----------|---------|
| `anchor_failure` | yes | The original failure or repro that motivated the fix |
| `sibling_family_discovery_method` | yes | How same-token/same-shape sibling surfaces were discovered |
| `K_true` | yes | Count/list of sibling-family members discovered |
| `K_swept` | yes | Count/list of sibling-family members covered by fixtures or proof |
| `coverage_proof` | yes | Evidence that `K_swept` covers the full sibling family |
| `positive_fixture` | yes | Full-artifact or fixture case where the intended violation still HALTs |
| `sibling_negative_fixture` | yes | Same-token/same-shape off-path case that must not hard-fail |
| `full_artifact_mixed_fixture` | yes | Generated artifact containing positive and sibling-negative controls together |
| `severity_assertions_by_consumer` | yes | Expected HALT/WARN/CONTINUE for every runtime consumer |
| `heuristic_cost_rationale` | required for hard-fatal heuristic parser | Why the heuristic is worth hard-gating despite false-positive risk |

### 5.5 H4 Effective-Input Manifest (lines 497–506)
| Field | Required | Meaning |
|-------|----------|---------|
| `selector_command` / `selector_cwd` | yes | Command and working directory that selected the review surface |
| `base_ref` / `head_ref` | yes | Revision endpoints used by the selector |
| `dirty_files` / `staged_files` / `unstaged_files` | yes | Working-tree state at review time |
| `included_files` | yes | Files/commits/artifacts actually consumed |
| `excluded_foreign_commits` | yes | Foreign/stale commits excluded, or explicit empty list |
| `runtime_surface_claim` | yes | The true surface requiring review |
| `intersection_proof` | yes | Machine-checkable proof that `included_files ∩ runtime_surface_claim` is correct |
| `validation_command` / `validation_result` | yes | How the manifest was checked |

---

## 6. §5.7 H3 Parser Decision — 4 GRAMMAR RULES VERBATIM (lines 508–517)
Lead (line 510): "H3 uses a **small formal allow-list grammar**, not ad hoc substring matching and not a full CommonMark parser in the first implementation increment. The grammar is intentionally narrow:"

1. (line 512) Only ATX headings (`#`, `##`, ... with a required post-marker space) and explicit verdict/status lines are behavior-controlling.
2. (line 513) Matching is exact-token or word-boundary anchored with escaped tokens; substring containment is never behavior-controlling.
3. (line 514) Setext-like headings, decorated/bolded verdict lines, wrong-case tokens, and sibling sections are fixtures, not accepted control syntax unless explicitly added to the grammar later.
4. (line 515) Every grammar expansion requires a positive fixture, a near-miss negative fixture, and a full-artifact mixed fixture.

Line 517: Resolves **OI-4** for the release increment; preserves future option to replace grammar with a CommonMark-derived parser if fixture pressure / false-positive measurement justifies.

**Builder must encode: NOT CommonMark (first increment), NOT substring — a small formal allow-list grammar.**

---

## 7. §5.2 Guard Boundary Table (condensed, 6 rows, lines 366–373) + §5.3 Phase Contracts (lines 377–386)

### 7.1 §5.2 Guard Condition Boundary Table (condensed) — 6 rows VERBATIM
> Full version: `spec-panel/guard-boundary-table.md` (6 guards × 6 inputs = 36 rows, 16 GAP in draft).

| Guard | Input Condition | Guard Result | Specified Behavior | Status |
|-------|-----------------|--------------|--------------------|--------|
| H2 empty ledger | Zero/Empty (`[]` consumers) | would-pass vacuously | **FAIL** — empty ledger cannot satisfy "no unclassified consumer" (FR-5) | GAP→FIXED |
| H2 `dead/legacy` role | Sentinel match | guard disabled | Requires unreachability proof, not assertion (FR-5) | GAP→FIXED |
| H3 substring match | Sentinel collision (`incomplete`⊃`complete`) | false positive | Word-boundary/grammar match + near-miss fixtures (FR-8) | GAP→FIXED |
| H4 effective input | Legitimate edge (non-empty, wrong surface) | would-pass (E>0) | **FAIL closed** unless surface-correctness proven (FR-10) | GAP→FIXED |
| H4 effective input | Zero/Empty | unspecified default | FAIL closed (default specified, FR-10) | GAP→FIXED |
| H5 / verdict | Waived probe then downstream re-eval | could re-green | One-way `waiver_status` latch; verdict ∈ {blocked, advisory} (FR-12) | GAP→FIXED |

### 7.2 §5.3 Phase Contracts (inter-wave YAML, lines 377–386) VERBATIM
```yaml
H0: {in: diagnosis, out: {applicable: bool, mechanism: str, candidate_escapes: [str]}}
H1: {in: applicable=true, out: {status: PASS|FAIL|N/A, card_path: str, negative_witness: bool}}
H2: {in: changed_contract, out: {status, ledger_path: str, unclassified_count: int}}   # FAIL if unclassified>0 OR ledger empty
H3: {in: anchor_fix, out: {status, sweep_path: str, K_swept: int, fixtures: {positive, sibling_negative}}}
H4: {in: review_selector, out: {status, card_path: str, surface_correct: bool}}          # FAIL closed if !surface_correct
H5: {in: boundary_risk, out: {decision: required|performed|waived_with_rationale|not_required, status: PASS|FAIL|N/A}}
verdict: {in: [h0..h5_status, waiver_status], out: pass|blocked|advisory|not_applicable}  # never upgraded post-latch
```

### 7.3 §5.1 CLI Surface (lines 351–360)
- Invocation unchanged: `/sc:troubleshoot <issue>`; mode auto-triggers via FR-1 (issue topology), NOT a flag (keeps command thin). No new CLI flags (line 360).

---

## 8. §6 Non-Functional Requirements (lines 521–528) — referenced by tests
| ID | Requirement | Target | Measurement |
|----|-------------|--------|-------------|
| NFR-1 | E1–E5 backtest catch rate | 100% would-have-caught (post-build, predicted until then) | Replay each escape against the built gates |
| NFR-2 | Applicability false-positive rate | <30% | Sample non-pipeline fixes; count spurious `applicable=true` |
| NFR-3 | Added cost of hardening mode | Bounded vs Tier-1 baseline; single-seam probe, no mandatory full E2E | Token/latency delta per run |
| NFR-4 | No-re-greening durability | 100% (no path upgrades a latched verdict) | Adversarial test: attempt downstream re-green |
| NFR-5 | Command thinness | Command advertises + hands off only | Diff review: no heavy logic in `troubleshoot.md` |
| NFR-6 | Output-contract backward compatibility | 100% of existing result consumers unaffected | Contract test on prior field set |

---

## 9. §8 Test Plan (lines 542–580) + explicit FR→test and escape→test map

### 9.1 §8.1 Unit Tests — 12 tests VERBATIM (lines 546–559)
| # | Test | File | Validates |
|---|------|------|-----------|
| 1 | `test_h0_applicability_skip_requires_boundary_scan` | `tests/troubleshoot/test_hardening_h0.py` | FR-1 skip needs reason+scan |
| 2 | `test_h0_boundary_scan_schema_rejects_bare_local_reason` | `tests/troubleshoot/test_hardening_h0.py` | §5.6 boundary scan schema; `looks local` cannot skip hardening |
| 3 | `test_h1_runtime_card_requires_negative_and_positive_witness` | `tests/troubleshoot/test_hardening_h1.py` | FR-3/FR-4 and §5.6 runtime-entrypoint card schema |
| 4 | `test_h2_empty_ledger_fails` | `tests/troubleshoot/test_hardening_h2.py` | FR-5 empty ledger = FAIL (F-N3) |
| 5 | `test_h3_word_boundary_rejects_incomplete_representation` | `tests/troubleshoot/test_hardening_h3.py` | FR-8 near-miss negatives (F-SC1) |
| 6 | `test_h3_small_grammar_rejects_setext_and_decorated_verdicts` | `tests/troubleshoot/test_hardening_h3.py` | §5.7 parser decision and grammar fixtures |
| 7 | `test_h3_sweep_card_requires_k_true_k_swept_and_mixed_fixture` | `tests/troubleshoot/test_hardening_h3.py` | FR-9 and §5.6 unmask/sweep/classifier card schema |
| 8 | `test_h4_nonempty_wrong_surface_fails_closed` | `tests/troubleshoot/test_hardening_h4.py` | FR-10 wrong-surface (F-D1) |
| 9 | `test_h4_manifest_schema_requires_intersection_proof` | `tests/troubleshoot/test_hardening_h4.py` | §5.6 effective-input manifest schema |
| 10 | `test_waiver_latch_one_way` | `tests/troubleshoot/test_hardening_verdict.py` | FR-12 no re-green (F-S1) |
| 11 | `test_h5_decision_maps_to_status_and_latch` | `tests/troubleshoot/test_hardening_verdict.py` | §5.4 H5 decision-to-status mapping |
| 12 | `test_known_escapes_requires_cited_card` | `tests/troubleshoot/test_hardening_verdict.py` | FR-12 anti-inflation (F-A1) |

### 9.2 §8.2 Integration Tests — 5 tests VERBATIM (lines 565–569)
| # | Test | Validates |
|---|------|-----------|
| 1 | `test_verdict_aggregation_from_h_statuses` | FR-13 deterministic verdict from H0–H5 + waiver_status; **covers all §5.4 truth-table rows** |
| 2 | `test_downstream_success_cannot_override_latched_hardening_verdict` | FR-12 downstream task-builder/reflect/adversarial cannot re-green `blocked`/`advisory` |
| 3 | `test_output_contract_backward_compat` | NFR-6 existing consumers read prior fields unbroken |
| 4 | `test_backtest_status_keeps_pipeline_health_advisory_until_complete` | NFR-1 separates H0-H5 run verdict from production-facing E1-E5 catch-rate signoff |
| 5 | `test_report_closure_section_not_proven_blockers` | FR-13 `NOT PROVEN` blockers when proof absent |

### 9.3 §8.3 Manual / E2E Backtest Scenarios — 6 scenarios VERBATIM (lines 573–580)
| # | Scenario | Steps | Expected Outcome | Escape |
|---|----------|-------|------------------|--------|
| 1 | E1 backtest | Replay headless PRD `--spec` with local-path `--file` against H1 | H1 FAIL pre-fix (negative witness), PASS post-fix | E1 |
| 2 | E2 backtest | Replay full generated artifact containing `complete` and near-miss `incomplete` phase text against H3 classifier | Intended executable violation still HALTs; near-miss sibling negative does not hard-fail | E2 |
| 3 | E3 backtest | Replay Task-Log/Findings sibling-heading artifact against H3 unmask/sweep card | H3 FAILs until `K_swept == K_true` and non-executable headings WARN/CONTINUE rather than HALT | E3 |
| 4 | E4 backtest | Run advisory check through PRD `_evaluate_gate` with H2 ledger | H2 FAIL until both `gate_passed` and `_evaluate_gate` consumers classified | E4 |
| 5 | E5 backtest | POST-reflect with dirty `/task` work + a foreign commit in range | H4 FAIL closed (wrong surface) until selector proven correct | E5 |
| 6 | Waiver re-green attempt | Waive H1, then run downstream reflect/adversarial | Verdict stays `blocked`/`advisory`; never `pass` | (NFR-4 / FR-12) |

### 9.4 Explicit FR → Test Map (derived from §8 "Validates" + §3.1)
| FR | Wave | Unit tests | Integration tests | E2E backtest |
|----|------|-----------|-------------------|--------------|
| FR-1 | H0 | #1 `test_h0_applicability_skip_requires_boundary_scan` | — | — |
| FR-2 | H0 | (covered via FR-12 #12 `known_escapes` candidate set) | — | — |
| FR-3 | H1 | #3 `test_h1_runtime_card_requires_negative_and_positive_witness` | — | E1 (#1), E4 (#4) |
| FR-4 | H1 | #3 (negative+positive witness) | — | E1 (#1) |
| FR-5 | H2 | #4 `test_h2_empty_ledger_fails` | — | E4 (#4) |
| FR-6 | H2 | **GAP — only indirect today** (see §10) | — | E1 (#1) |
| FR-7 | H3 | #6 `test_h3_small_grammar_rejects_setext_and_decorated_verdicts` (+ #5) | — | E2 (#2), E3 (#3) |
| FR-8 | H3 | #5 `test_h3_word_boundary_rejects_incomplete_representation` | — | E2 (#2) |
| FR-9 | H3 | #7 `test_h3_sweep_card_requires_k_true_k_swept_and_mixed_fixture` | — | E3 (#3) |
| FR-10 | H4 | #8 `test_h4_nonempty_wrong_surface_fails_closed`, #9 `test_h4_manifest_schema_requires_intersection_proof` | — | E5 (#5) |
| FR-11 | H5 | #11 `test_h5_decision_maps_to_status_and_latch` | — | E5 (#5) |
| FR-12 | cross | #10 `test_waiver_latch_one_way`, #12 `test_known_escapes_requires_cited_card` | #2 `test_downstream_success_cannot_override_latched_hardening_verdict` | Waiver re-green (#6) |
| FR-13 | output | (schema fields across H0-H5 tests) | #1 `test_verdict_aggregation_from_h_statuses`, #3 `test_output_contract_backward_compat`, #5 `test_report_closure_section_not_proven_blockers` | — |

### 9.5 Explicit Escape → Test Map
| Escape | Unit | Integration | E2E |
|--------|------|-------------|-----|
| E1 | #3 (witnesses) | — | §8.3 #1 |
| E2 | #5, #6 | — | §8.3 #2 |
| E3 | #7 | — | §8.3 #3 |
| E4 | #4 | — | §8.3 #4 |
| E5 | #8, #9, #11 | #2 | §8.3 #5 |

### 9.6 NFR → Test Map
- NFR-1 → integration #4 `test_backtest_status_keeps_pipeline_health_advisory_until_complete` + §8.3 E1–E5.
- NFR-4 → integration #2 `test_downstream_success_cannot_override_latched_hardening_verdict` + §8.3 #6 (Waiver re-green). **FR-12 must be paired with this NFR-4 test (task brief item 11 + §10 sc:tasklist note line 596).**
- NFR-6 → integration #3 `test_output_contract_backward_compat`.

---

## 10. GAP to close (task brief item 11) — NEW test for FR-6

**FR-6 (Sibling / Duplicate-Evaluator Sweep, H2)** currently has only INDIRECT coverage in §8.1/§8.2 (no unit test names FR-6; it is implied through E1 backtest §8.3 #1 and the H2 ledger tests). Per the user (reflect gap **G-PRE-1**), the tasklist MUST add a NEW unit test:

- **NEW test:** `test_h2_sibling_sweep_required_when_concept_shared`
- **File (consistent with §8.1 H2 home):** `tests/troubleshoot/test_hardening_h2.py`
- **Validates:** FR-6 — H2 FAILs if sibling pipelines / duplicate evaluators are NOT swept when the concept is shared (§3 FR-6 AC1 line 162).

**Also (item 11):** pair **FR-12** with the **NFR-4 downstream-no-re-green test** (`test_downstream_success_cannot_override_latched_hardening_verdict`, §8.2 #2) — this is reinforced by §10 line 596 ("FR-12 … is the highest-risk task — pair with the NFR-4 adversarial test and §5.4 truth-table/downstream no-override checks before marking done").

---

## 11. §11 Open Items (lines 600–607) — the needs_human_decision HALT items

> ⚠️ CORRECTION to task brief framing: The spec shows **OI-1, OI-4, OI-6 are RESOLVED** in-spec (§5.4 / §5.7). The OPEN / deferred items with future resolution targets are **OI-2, OI-3, OI-5** — these are the ones the user flagged as `needs_human_decision` HALT items (they have NO in-spec resolution; their resolution target is Roadmap M2 or G1 approval). Quoted verbatim:

| Item | Question | Impact | Resolution Target |
|------|----------|--------|-------------------|
| **OI-2** | "Which tokens are first-class ledger entries (flags, phase IDs, gate names, verdicts, step IDs, statuses)?" | Medium | Roadmap M2; schema seeded in §5.6 `contract_token` |
| **OI-3** | "Cheapest reliable public-entrypoint probe per high-risk seam (esp. live Claude/agent execution)?" | Medium | Roadmap M2; substitute witness classes governed by FR-4/§5.4 latch |
| **OI-5** | "`target_release` exact version (proposed 4.3.0)" | Low | G1 approval |

For completeness (RESOLVED, not HALT items):
- **OI-1** (line 602): no-re-greening mechanical enforcement → **Resolved in §5.4** (persisted `waiver_status` latch + downstream no-override rule + `success_with_hardening_*` rendering).
- **OI-4** (line 605): CommonMark vs smaller grammar → **Resolved in §5.7** (small formal allow-list grammar for this increment).
- **OI-6** (line 607): verdict-enum reconciliation → **Resolved in §5.4** truth table.

**Builder implication:** OI-2, OI-3, OI-5 must be authored as `needs_human_decision` items that write PENDING + HALT the dependent spec/gate mutation; never auto-default (per memory `feedback_human_decision_items_must_halt.md`).

---

## 12. §9 Migration / Rollout + G1-HALT constraint (lines 582–586)
- **Breaking changes (line 584):** None. New fields additive under `contract_version: 1.0.0`; mode off unless `applicable=true`.
- **Backwards compat (line 585):** Existing consumers read only prior fields; NFR-6 guards.
- **Rollback (line 586):** Revert SKILL.md trigger block + remove 6 new refs → command reverts to pure handoff. Then `make sync-dev` + `make verify-sync` so `.claude/` mirrors `src/superclaude/`; **do NOT stage `.claude/` mirrors other than `.claude/settings.json`**. No data migration.
- **G1-HALT (lines 42, 586, frontmatter status=draft):** Implementation is **halted pending G1 approval**. Pre-approval: **NO edit to `src/superclaude/` or `.claude/` skill/command files** (§1.2 line 42; §9 line 586: "pre-approval the working tree is unchanged on protocol source files"). The tasklist must encode this HALT — build the tasklist, but the implementation items stay gated behind explicit G1 approval.

---

## 13. §10 Downstream Inputs (lines 588–596) — builder guidance from the spec itself
- **§10 For sc:tasklist (line 596) VERBATIM:** "Break per FR (FR-1..FR-13) into atomic tasks; group by implementation order (§4.6). Each task's DoD = its FR acceptance criteria + the relevant unit test (§8.1). FR-12 (no-re-greening) is the highest-risk task — pair with the NFR-4 adversarial test and §5.4 truth-table/downstream no-override checks before marking done."
- **§10 For sc:roadmap (line 592):** Themes T1–T4; Milestones M1 mode skeleton + verdict aggregation; M2 H1/H2/H4 gates; M3 H3 classifier + fixtures; M4 contract + report; M5 backtest + sync.

---

## 14. §12 Brainstorm Gap Analysis (lines 613–626) — context (gaps the spec already closes)
G-1 waiver/no-re-green prose→SV (High); G-2 H2 empty-ledger vacuous pass (High); G-3 H4 wrong-surface (High); G-4 word-boundary appendix-only (High); G-5 un-earned `known_escapes_caught` (High); G-6 unversioned contract (High); G-7 prose waves not SMART FRs (Critical); G-8 no E1–E5→wave→FR trace (Medium); G-9 verdict not truth-tabled (High); G-10 schemas prose-only (High); G-11 H3 parser unresolved (Medium); G-12 executable validation implicit (Medium). Line 628: all High/Critical closed in-spec.

> NOTE on gap-ID naming: §12 uses **G-1..G-12** (panel gaps already closed). The user's **G-PRE-1** (FR-6 indirect-coverage gap, §10 above) is a SEPARATE reflect-pre gap, not in the spec's §12 table.

---

## Summary of Findings

**STATUS: Complete.**

Faithful extraction of every authoritative structure the task builder must encode, all cited to §section + line numbers of the RELEASE-SPEC (v1.1.0, 653 lines).

Key invariants captured:
1. **`pipeline_hardening_verdict` is the FOUR-token enum `pass | blocked | advisory | not_applicable`** (§4.5 L311, §5.5 L431, §5.3 L385). `advisory` is REQUIRED. The §5.4 truth table has **7 rows**; **ROWS 5 and 6 emit `advisory`** (L398–399). Recorded verbatim. Any "advisory removed" claim is FALSE.
2. **13 FRs** extracted with wave (H0–H5), escapes closed (E1–E5), dependencies, and AC line numbers (§3 L99–247) + §3.1 traceability matrix verbatim (L251–257).
3. **§5.4 all tables verbatim:** 7-row aggregation truth table, 4-row H5 decision-to-status, 3-row backtest-vs-verdict, plus the downstream no-override rule (L411).
4. **§5.5 field schema** all 10/11 fields verbatim (L427–439). **§5.6** all 5 artifact schemas with every field + required flag (L443–506). **§5.7** 4 grammar rules verbatim — small formal allow-list grammar, NOT CommonMark, NOT substring (L508–517).
5. **§4.5** 15-var state registry verbatim incl. `waiver_status` one-way latch (L315) and `pipeline_hardening_applicable` set-once (L310). **§4.6** 7-group order (group 3 = 3 parallel refs). **§4.7** 6 validation components + test locations.
6. **§8** full test plan: 12 unit + 5 integration + 6 E2E backtest, with explicit FR→test, escape→test, NFR→test maps.

GAPS / actions for builder:
- **NEW test `test_h2_sibling_sweep_required_when_concept_shared`** for FR-6 in `tests/troubleshoot/test_hardening_h2.py` (reflect gap G-PRE-1).
- **Pair FR-12 with the NFR-4 test** `test_downstream_success_cannot_override_latched_hardening_verdict` (§8.2 #2; reinforced §10 L596).

CORRECTION to task brief: the `needs_human_decision` HALT items are **OI-2, OI-3, OI-5** (OPEN, defer to Roadmap M2 / G1). OI-1, OI-4, OI-6 are RESOLVED in-spec (§5.4 / §5.7) — the builder must NOT treat them as HALT items.

G1-HALT constraint: implementation halted pending G1 approval; NO `src/superclaude/` or `.claude/` edits pre-approval (§1.2 L42, §9 L586).

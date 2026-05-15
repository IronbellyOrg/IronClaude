# Validation Report — Phase 7 / T07.04

**Task:** T07.04 — Re-score drifted features; produce `validation-report.md` & `final-merge-plan.md`
**Roadmap Item:** R-027
**Tier:** STRICT
**Generated:** 2026-05-15
**Status:** Deliverable artifact #1 of T07.04 (companion: `final-merge-plan.md`).

---

## 0. Scope & method

This report consolidates the findings of **T07.01** (`plan-adversarial-review.md`), **T07.02** (`file-reference-reverification.md` + `compat-hazard-report.md`), and **T07.03** (`traceability-gap-report.md` + `invariant-survival-walkthrough.md`) into a single pass/fail register covering:

1. **Every Phase 6 plan item** (67 row-line-items consolidating 65 distinct CR-IDs across the six refactor files, per `merge-master.md` § 1).
2. **Every manifest feature** (8 TUs + 9 MEs + 10 named donor-ceremony drops + 26 ledger entries, per `transfer-manifest.md` and `rejected-features-ledger.md`).

For each item, this report records: the pass/fail verdict, the **finding source** (T07.01 / T07.02 / T07.03), and the disposition (closed in Phase 7 by `final-merge-plan.md`, or carried forward).

Per T07.04 Step 2, every feature whose Phase 6 implementation **drifted** from the Phase 5 integration sketch must be re-scored with the V/C/K rubric (Validation × Complexity × Knowledge — `transfer-manifest.md` § 4) and the verdict may change. T07.01 § 3.5 (Implementation drift check) and T07.03 § 4 (reverse traceability) **both find zero drift** across all 8 TUs and all 14 absorption rows. **No V/C/K re-score is therefore required.** § 4 of this report documents the zero-drift verdict and the V/C/K invariance.

---

## 1. Verdict roll-up

| Verdict bucket | Count | Outcome |
|---|---|---|
| **Phase 6 plan items (CR rows)** — PASS | 65 / 65 (100 %) | All CR rows pass adversarial review, file re-verification, traceability check, and invariant-survival walkthrough. |
| **Phase 6 plan items — PASS WITH NOTE** | 7 (CR-FM-02, CR-TASK-01, CR-TASK-03, CR-TASK-04, CR-TASK-06, CR-TASK-07, CR-TASK-09) | Carry open findings F-01..F-05 (clarification/strengthening). No invariant violation. |
| **Phase 6 plan items — FAIL** | 0 | — |
| **Manifest TUs (TU-1..TU-8)** — PASS | 8 / 8 | All map forward to ≥ 1 Phase 6 row at the manifest-named extension-point on the manifest-named file path within the manifest's effort envelope. Zero drift. |
| **Manifest exceptions (ME-1..ME-9)** — HELD | 9 / 9 | 6 actively bound to Phase 6 rows; 3 honored by absence (deferrals preserved). |
| **Donor-ceremony drops** — NOT REVIVED | 10 / 10 | Zero re-introductions across 65 CR-IDs. |
| **Ledger entries (LR-REJECT-1..17 + LR-DEFER-1..9)** — TERMINAL | 26 / 26 | Zero re-proposals. R-RULE-11 holds. |
| **Invariants (INV-01..INV-05)** — SURVIVE | 5 / 5 | Demonstrated, not asserted, by `invariant-survival-walkthrough.md` § 2 + § 3. |
| **Compat hazards (HZ-01..HZ-18)** — MITIGATED | 18 / 18 | Every hazard has a severity and a mitigation; `final-merge-plan.md` records sequencing constraints for the 4 sequencing-sensitive hazards. |
| **Open findings (F-01..F-08)** — CARRY FORWARD | 8 | All clarification/strengthening; closed in `final-merge-plan.md` § 4. |
| **Drifted features requiring V/C/K re-score** | 0 | T07.01 § 3.5 + T07.03 § 4 both certify zero drift; no re-score required. |

**Overall:** **PASS WITH 8 CLARIFICATION FINDINGS.** Zero invariant violations, zero manifest drifts, zero scope expansions, zero ledger re-proposals.

---

## 2. Per-CR pass/fail register

The register below covers all 67 row-line-items in `merge-master.md` § 1 (65 distinct CR-IDs + the CR-DOC-13 audit-acknowledgement row + the CR-DEFER-T06.04 ack row). Each row carries its verdict, the finding source(s) that contributed evidence, and the open finding(s) (if any) that `final-merge-plan.md` will close.

Legend:
- **PASS** — clean across T07.01-T07.03.
- **PASS WITH NOTE** — clean structurally; carries one or more open findings F-01..F-05 (clarification/strengthening; documented in `final-merge-plan.md` § 4).
- **HZ-N reference** — hazard from `compat-hazard-report.md` whose mitigation is already in the plan; no Phase 6 row change required (sequencing constraints are captured in `final-merge-plan.md` § 6).

### 2.1 M1 — Foundation rows (atomic merge; CR-FM-01..03 + CR-TASK-01..04)

| Row # | CR-ID | Verdict | Finding source | Open findings | Notes |
|---|---|---|---|---|---|
| 1 | CR-FM-01 | PASS | T07.01 § 2.1; T07.02 HZ-01 (mitigated) | — | Optional field; INV-04 preserved. |
| 2 | CR-FM-02 | PASS WITH NOTE | T07.01 § 2.1 | F-01 | Read-vs-dispatch boundary phrasing strengthened in final plan. |
| 3 | CR-FM-03 | PASS | T07.01 § 2.1; T07.02 HZ-01; T07.02 § 6 (sample verification across 5 TASK-* files) | — | Dedicated INV-04 compat shim row; load-bearing. |
| 4 | CR-TASK-01 | PASS WITH NOTE | T07.01 § 2.1 | F-02 | CR-7 ordering review-dependent; final plan extends CR-FM-04/CR-TASK-12 audit. |
| 5 | CR-TASK-02 | PASS | T07.01 § 2.1; T07.03 ME-1 (held) | — | Gate 1 PRE-LOOP only; ME-1 + ME-6 bound. |
| 6 | CR-TASK-03 | PASS WITH NOTE | T07.01 § 2.1 | F-01 (cross-ref) | Per-item tier-conditioned READ only; ME-1 bound. |
| 7 | CR-TASK-04 | PASS WITH NOTE | T07.01 § 2.1 | F-02 (cross-ref) | CR-8 ordering shares F-02 mitigation. |

### 2.2 M2 — Tier-conditioned behaviors (CR-TASK-05..06)

| Row # | CR-ID | Verdict | Finding source | Open findings | Notes |
|---|---|---|---|---|---|
| 8 | CR-TASK-05 | PASS | T07.01 § 2.2; T07.03 ME-2 (held) | — | `rf-qa` supplemented, never replaced. |
| 9 | CR-TASK-06 | PASS WITH NOTE | T07.01 § 2.2 | F-03 | Git-dirty behavior pinned to Reading A (log+continue) in final plan. |

### 2.3 M3 — TFEP cluster (CR-TASK-07..10)

| Row # | CR-ID | Verdict | Finding source | Open findings | Notes |
|---|---|---|---|---|---|
| 10 | CR-TASK-07 | PASS WITH NOTE | T07.01 § 2.3 | F-04 | Baseline-absent fallback pinned to Reading A (over-escalate) in final plan. |
| 11 | CR-TASK-08 | PASS | T07.01 § 2.3; T07.03 ME-3 (held) | — | Side-channel only; F1 continues. |
| 12 | CR-TASK-09 | PASS WITH NOTE | T07.01 § 2.3 | F-05 | INV-03 mid-phase routing documented as authorized widening in final plan. |
| 13 | CR-TASK-10 | PASS | T07.01 § 2.3; T07.03 INV-04 + INV-05 | — | Side-effect FILE; LR-DEFER-6 not revived. |

### 2.4 M-sync — mechanical sync + audits (CR-TASK-11, CR-FM-04, CR-TASK-12)

| Row # | CR-ID | Verdict | Finding source | Open findings | Notes |
|---|---|---|---|---|---|
| 14 | CR-TASK-11 | PASS | T07.01 § 2.4 | — | Mechanical sync; R-RULE-10 only. |
| 15 | CR-FM-04 | PASS | T07.01 § 2.1 | — | Cross-row audit; final plan **extends scope** to grep CR-7/CR-8 in-order (F-02 mitigation). |
| 16 | CR-TASK-12 | PASS | T07.01 § 2.4 | — | Six verbatim donor diffs; final plan **extends scope** with an alternate F-02 mitigation (sentinel comment block). |

### 2.5 M4 — `/sc:task` deprecation rows (CR-DEP-01..05 + CR-DIST-01/02/04 atomic with hard-delete)

| Row # | CR-ID | Verdict | Finding source | Open findings | Notes |
|---|---|---|---|---|---|
| 17 | CR-DEP-01 | PASS | T07.01 § 2.4; T07.02 HZ-08 (accepted UX cost) | — | Soft-deprecation stub; `mcp-servers:` / `personas:` removed (ME-9). |
| 18 | CR-DEP-02 | PASS | T07.01 § 2.4 | — | Mechanical sync of stub; R-RULE-10. |
| 19 | CR-DIST-02 | PASS | T07.01 § 2.4; T07.02 HZ-14 (mitigated) | — | Atomic with CR-DEP-03/04 for `make verify-sync`. |
| 20 | CR-DEP-03 | PASS | T07.01 § 2.4; T07.01 § 3.7 (procedural authorization) | F-07 | Hard-delete; final plan documents procedural authorization chain. |
| 21 | CR-DEP-04 | PASS | T07.01 § 2.4 | — | Hard-delete `__init__.py` + rmdir + mirror prune. |
| 22 | CR-DIST-01 | PASS | T07.01 § 2.4 | — | Installer regression test. |
| 23 | CR-DIST-04 | PASS | T07.01 § 2.4 | — | `make verify-sync` audit. |
| 24 | CR-DEP-05 | PASS | T07.01 § 2.4; T07.01 § 3.2 (ME-9 binding) | — | Re-affirms ME-9 / LR-REJECT-1 (D02 / Layer A). |

### 2.6 M5-A — Distribution: plugin stub + README (CR-DIST-03/05/06)

| Row # | CR-ID | Verdict | Finding source | Open findings | Notes |
|---|---|---|---|---|---|
| 25 | CR-DIST-03 | PASS | T07.01 § 2.4 | — | Plugin stub redirect; no `mcp-servers:` re-intro. |
| 26 | CR-DIST-05 | PASS | T07.01 § 2.4; T07.02 HZ-18 (no `/sc:task` in README) | — | Explicit no-op; documented in commit msg. |
| 27 | CR-DIST-06 | PASS | T07.01 § 2.4 | — | R-RULE-11 audit over CR-DIST-01..05. |

### 2.7 M5-B — Active source reference redirects (CR-REF-01..13)

| Row # | CR-ID | Verdict | Finding source | Open findings | Notes |
|---|---|---|---|---|---|
| 28 | CR-REF-01 | PASS | T07.01 § 2.4; T07.02 HZ-06 (mitigated by sequencing) | — | `sprint/process.py` rewrite; **must land ≤ CR-DEP-01**. |
| 29 | CR-REF-02 | PASS | T07.01 § 2.4; T07.02 HZ-07 (mitigated by sequencing) | — | `cleanup_audit/prompts.py`; **must land ≤ CR-DEP-01**. |
| 30 | CR-REF-09 | PASS | T07.01 § 2.4 | — | Test parity; **keeps** historical `/sc:task-unified` guard + adds new `/sc:task` guard. Derivative-responsibility justified (T07.01 § 2.4). |
| 31 | CR-REF-04 | PASS | T07.01 § 2.4 | — | Sibling command bodies. |
| 32 | CR-REF-05 | PASS | T07.01 § 2.4 | — | COMMANDS.md + ORCHESTRATOR.md; LR-REJECT-3 audit. |
| 33 | CR-REF-06 | PASS | T07.01 § 2.4 | — | Sibling protocol skill bodies. |
| 34 | CR-REF-07 | PASS | T07.01 § 2.4 | — | Templates; anchored regex. |
| 35 | CR-REF-08 | PASS | T07.01 § 2.4 | — | Plugin stub redirect (companion to CR-DIST-03). |
| 36 | CR-REF-10 | PASS | T07.01 § 2.4 | — | PROJECT_INDEX.md; depends on CR-DEP-03/04. |
| 37 | CR-REF-11 | PASS | T07.01 § 2.4; T07.02 HZ-13 (LOW) | — | scripts/sync_from_framework.py docstring. |
| 38 | CR-REF-12 | PASS | T07.01 § 2.4 | — | `make sync-dev` mirror refresh; R-RULE-10. |
| 39 | CR-REF-03 | PASS | T07.01 § 2.4 | — | False-positive triage; `leave-as-is`. |
| 40 | CR-REF-13 | PASS | T07.01 § 2.4 | — | rf-assembler memory `leave-as-is`. |

### 2.8 M5-C — Active backlog redirects + leave-with-note (CR-REF-14..18)

| Row # | CR-ID | Verdict | Finding source | Open findings | Notes |
|---|---|---|---|---|---|
| 41 | CR-REF-14 | PASS | T07.01 § 2.4 | — | Live planning docs redirect. |
| 42 | CR-REF-15 | PASS | T07.01 § 2.4 | — | `leave-with-note` per file (5 files). |
| 43 | CR-REF-16 | PASS | T07.01 § 2.4 | — | `leave-with-note` default; per-file `redirect` if live. |
| 44 | CR-REF-17 | PASS | T07.01 § 2.4 | — | `leave-with-note`. |
| 45 | CR-REF-18 (cluster, 14 sub-rows) | PASS | T07.01 § 2.4; T07.02 HZ-15 (LOW) | — | Cluster-root `DEPRECATION-NOTE.md`. |

### 2.9 M5-D — Frozen / archived / not-editable buckets (CR-REF-BUCKET-A..H)

| Row # | CR-ID | Verdict | Finding source | Open findings | Notes |
|---|---|---|---|---|---|
| 46 | CR-REF-BUCKET-A | PASS | T07.01 § 2.4 | — | Backlog archive `leave-as-is`. |
| 47 | CR-REF-BUCKET-B | PASS | T07.01 § 2.4; T07.02 HZ-16 (LOW) | — | v3.75 archive bucket; optional note. |
| 48 | CR-REF-BUCKET-C | PASS | T07.01 § 2.4; T07.03 INV-04 (held) | — | `.dev/tasks/to-do/TASK-*/` — **INV-04 load-bearing**; no body rewrites. |
| 49 | CR-REF-BUCKET-D | PASS | T07.01 § 2.4 | — | Benchmarks / fixtures frozen. |
| 50 | CR-REF-BUCKET-E | PASS | T07.01 § 2.4 | — | `.venv/` regenerated. |
| 51 | CR-REF-BUCKET-F | PASS | T07.01 § 2.4 | — | Serena memory. |
| 52 | CR-REF-BUCKET-G | PASS | T07.01 § 2.4 | — | `.dev/releases/complete/**` terminal archive. |
| 53 | CR-REF-BUCKET-H | PASS | T07.01 § 2.4 | — | This sprint's own artifacts; `leave-as-is`. |

### 2.10 M5-E — Hand-edited documentation redirects (CR-DOC-01..05)

| Row # | CR-ID | Verdict | Finding source | Open findings | Notes |
|---|---|---|---|---|---|
| 54 | CR-DOC-01 | PASS | T07.01 § 2.4; T07.02 HZ-09 (HIGH, mitigated) | — | `docs/user-guide/commands.md`; atomic with CR-DEP-01 + CR-TASK-02. |
| 55 | CR-DOC-02 | PASS | T07.01 § 2.4; T07.02 HZ-10 | — | `docs/user-guide/flags.md`. |
| 56 | CR-DOC-04 | PASS | T07.01 § 2.4 | — | Developer-guide. |
| 57 | CR-DOC-05 | PASS | T07.01 § 2.4 | — | Release/CLI guides. |
| 58 | CR-DOC-03 | PASS | T07.01 § 2.4; T07.02 HZ-10 | — | `docs/sprint-cli-deep-dive.md`. |

### 2.11 M5-F — Historical analyses, research, generated docs (CR-DOC-06..12)

| Row # | CR-ID | Verdict | Finding source | Open findings | Notes |
|---|---|---|---|---|---|
| 59 | CR-DOC-06 | PASS | T07.01 § 2.4; T07.02 HZ-12 | — | analysis-sc-tasklist.md `leave-with-note`. |
| 60 | CR-DOC-07 | PASS | T07.01 § 2.4 | — | 4 comparison analyses `leave-with-note`. |
| 61 | CR-DOC-08 | PASS | T07.01 § 2.4 | — | Research reports `leave-with-note`. |
| 62 | CR-DOC-09 | PASS | T07.01 § 2.4 | — | dev-guide-research extraction artifacts `leave-with-note`. |
| 63 | CR-DOC-10 | PASS | T07.01 § 2.4; T07.02 HZ-11 (LOW) | — | Generated contributor knowledge base `leave-as-is`. |
| 64 | CR-DOC-11 | PASS | T07.01 § 2.4 | — | sprint-cli generated + v3.7-refactor + debates split treatment. |
| 65 | CR-DOC-12 | PASS | T07.01 § 2.4 | — | Cleanup/CLI-portify generated `leave-as-is`. |

### 2.12 M5-G — Audit closure rows

| Row # | CR-ID | Verdict | Finding source | Open findings | Notes |
|---|---|---|---|---|---|
| 66 | CR-DOC-13 | PASS | T07.01 § 2.4 | — | R-RULE-11 audit over CR-DOC-01..12. |
| 67 | CR-DEFER-T06.04 ack | PASS | T07.03 § 6.2 (CLOSE) | — | Hand-off audit; § 6 coverage check confirms. |

**Per-row register total:** **67 / 67 PASS**, of which **7 PASS WITH NOTE** carry the five MEDIUM-severity open findings F-01..F-05. All notes are addressed in `final-merge-plan.md` § 4.

---

## 3. Per-manifest-feature pass/fail register

### 3.1 Transfer units (TU-1..TU-8)

| TU | Title | Forward map (Phase 6 row[s]) | Status | Drift? | Finding source |
|---|---|---|---|---|---|
| TU-1 | `Tier:` field + Gate 1 + per-item marker | CR-FM-01, CR-FM-02, CR-FM-03, CR-FM-04 (audit), CR-TASK-02, CR-TASK-03 | **PASS** | No | T07.01 § 3.1 + § 3.5; T07.03 § 3 |
| TU-2 | Critical/Trivial Path Override | CR-TASK-01, CR-TASK-04 | **PASS** | No | T07.01 § 3.1 + § 3.5 |
| TU-3 | Gate 2 Verification routing widening (ADAPT) | CR-TASK-05 | **PASS** | No | T07.01 § 3.1; ME-2 held |
| TU-4 | D15b Layer 2 pre-flight (ADAPT; D15c REJECTed) | CR-TASK-06 | **PASS** | No | T07.01 § 3.1; ME-5 held |
| TU-5 | TFEP Test baseline snapshot (ADOPT) | CR-TASK-07 | **PASS** | No | T07.01 § 3.1; ME-4 held |
| TU-6 | TFEP Prohibitions + Carve-outs (ADOPT) | CR-TASK-08 | **PASS** | No | T07.01 § 3.1; ME-3 held |
| TU-7 | TFEP Escalation trigger detection (ADOPT) | CR-TASK-09 | **PASS** | No (see F-05 — INV-03 surface widening documented, not implementation drift) | T07.01 § 3.1; ME-3 inherited |
| TU-8 | TFEP Incident reporting (ADOPT) | CR-TASK-10 | **PASS** | No | T07.01 § 3.1; INV-05 + F4 preserved |

**TU coverage: 8 / 8 PASS, 0 drift.**

### 3.2 Manifest exceptions (ME-1..ME-9)

| ME | Binding | Status | Finding source |
|---|---|---|---|
| ME-1 (PRE-LOOP DISPATCH ONLY) | CR-TASK-02, CR-TASK-03, CR-FM-02 | **HELD** | T07.01 § 3.2; T07.03 § 6.3 |
| ME-2 (`rf-qa` SUPPLEMENTED NOT REPLACED) | CR-TASK-05, CR-TASK-04 | **HELD** | T07.01 § 3.2; T07.03 § 6.3 |
| ME-3 (SIDE-CHANNEL ONLY, NO F1 HALT) | CR-TASK-08/09/10 (+ CR-TASK-07 transitively) | **HELD** | T07.01 § 3.2; T07.03 § 6.3 |
| ME-4 (BASELINE TIER-GATED) | CR-TASK-07 (+ CR-TASK-10 transitively) | **HELD** | T07.01 § 3.2 |
| ME-5 (NO PER-ITEM EXECUTE SUBSTITUTION) | CR-TASK-06 | **HELD** | T07.01 § 3.2 |
| ME-6 (TIER FIELD + GATE 1 SHIP TOGETHER) | M1 atomic-merge rule | **HELD** | T07.01 § 3.2; `merge-master.md` § 6 step 1 |
| ME-7 (D08 DEFERRED) | (no row authored — honored by absence) | **HELD** | T07.01 § 3.2; T07.03 § 6.3 |
| ME-8 (D01 DEFERRED) | (no row authored — honored by absence) | **HELD** | T07.01 § 3.2; T07.03 § 6.3 |
| ME-9 (D02/Layer A REJECT re-affirmed) | CR-DEP-01, CR-DEP-05, CR-DIST-03, CR-DOC-04 | **HELD** | T07.01 § 3.2 + § 3.4 |

**ME coverage: 9 / 9 HELD.**

### 3.3 Donor-ceremony drops (manifest § 2)

| Dropped donor ceremony | Phase 6 confirmation | Status | Finding source |
|---|---|---|---|
| D09b runtime classifier with priority cascade + keyword tables | CR-TASK-02 reads `Tier:` declaratively | **NOT REVIVED** | T07.01 § 3.3 |
| D10 separate command-side dispatch layer | CR-DEP-01 collapses command body | **NOT REVIVED** | T07.01 § 3.3 |
| D15c per-tier procedure synthesis at execute-time | CR-TASK-06 anchored at *First Item Protocol* (pre-loop); ME-5 binds | **NOT REVIVED** | T07.01 § 3.3 |
| D23 Step 5 — insert `## Failure Remediation` heading | CR-TASK-10 writes side-effect FILE; INV-05 + F4 preserved | **NOT REVIVED** | T07.01 § 3.3 |
| D23 Step 6 — resume from inserted task | CR-TASK-10 does not insert task-file content | **NOT REVIVED** | T07.01 § 3.3 |
| D25 3-strike FULL STOP budget | CR-TASK-09 uses existing 3-cycle fix loop | **NOT REVIVED** | T07.01 § 3.3 |
| Donor F1-HALTING TFEP behavior | CR-TASK-08/09/10 side-channel only | **NOT REVIVED** | T07.01 § 3.3 |
| Donor verifier-replacement semantic on STRICT | CR-TASK-05 authors `[rf-qa, quality-engineer]` literally | **NOT REVIVED** | T07.01 § 3.3 |
| Donor standalone verification routing table | CR-TASK-05 inlines mapping into Phase-Gate QA section | **NOT REVIVED** | T07.01 § 3.3 |
| Donor "Layer 2" framing as named runtime artifact | CR-TASK-06 inlines pre-flight; no named layer | **NOT REVIVED** | T07.01 § 3.3 |

**Donor-ceremony coverage: 10 / 10 NOT REVIVED.**

### 3.4 Rejected-features ledger (LR-REJECT-1..17 + LR-DEFER-1..9)

Per `merge-master.md` § 4, T07.01 § 3.4, and T07.03 § 6.4 — all three independently audited the 26 ledger entries across all 65 CR-IDs and confirmed **zero re-proposals**.

| Ledger cluster | Status | Finding source |
|---|---|---|
| LR-REJECT-1, LR-REJECT-2 (D02 / Layer A `mcp-servers:` advertisement; ME-9) | **TERMINAL** | T07.01 § 3.4 |
| LR-REJECT-3 (D09b runtime classifier) | **TERMINAL** | T07.01 § 3.4 |
| LR-REJECT-4 (Gate 5 toggleable flags) | **TERMINAL** | T07.01 § 3.4 |
| LR-REJECT-5, LR-REJECT-6, LR-REJECT-8, LR-REJECT-9 (personas / keywords / auto-trigger / Strategy axis) | **TERMINAL** | `merge-master.md` § 4 |
| LR-REJECT-7 (D15c per-tier procedure synthesis) | **TERMINAL** | T07.01 § 3.4; ME-5 binds |
| LR-REJECT-10..17 (escalation philosophy / flags / few-shot / metrics) | **TERMINAL** | `merge-master.md` § 4 |
| LR-DEFER-1, LR-DEFER-3 (cluster-as-written aggregates) | **TERMINAL** | `merge-master.md` § 4 |
| LR-DEFER-2 (D27 / Gate 3 per-tier MCP matrix) | **TERMINAL** | `merge-master.md` § 4 |
| LR-DEFER-4 (D01 `allowed-tools:` enforcement; ME-8) | **TERMINAL** | T07.01 § 3.4; CR-FM-04 audit |
| LR-DEFER-5 (D08 classification header; ME-7) | **TERMINAL** | T07.01 § 3.4; CR-FM-04 audit |
| LR-DEFER-6 (D23 six-step flow) | **TERMINAL** | T07.01 § 3.4; CR-TASK-10 side-effect FILE only |
| LR-DEFER-7, LR-DEFER-8, LR-DEFER-9 (D14 / D26 / D32) | **TERMINAL** | `merge-master.md` § 4 |

**Ledger coverage: 26 / 26 TERMINAL. R-RULE-11 holds at the consolidated level.**

---

## 4. Drift assessment & V/C/K re-score (T07.04 Step 2)

T07.04's Step 2 requires re-scoring every feature whose Phase 6 implementation drifted from the Phase 5 integration sketch with the V/C/K rubric (`transfer-manifest.md` § 4). T07.01 § 3.5 enumerated the drift check on all 8 TUs against the manifest § 2 "Shape of change" sketches:

| TU | Manifest sketch shape | Phase 6 rows | Drift verdict |
|---|---|---|---|
| TU-1 | ~21-33 lines at ext-point rows 1, 4, 13 on `SKILL.md` | CR-FM-01..03 + CR-TASK-02 + CR-TASK-03 (XS + XS + XS + M + XS) | No drift |
| TU-2 | ~10 lines at row 1 + ~5 at row 10 on `SKILL.md` | CR-TASK-01 (S) + CR-TASK-04 (XS) | No drift |
| TU-3 | ~25 lines at row 10 on `SKILL.md` | CR-TASK-05 (M) | No drift |
| TU-4 | ~15-25 lines at row 2 on `SKILL.md` | CR-TASK-06 (M) | No drift |
| TU-5 | ~15 lines at row 2 on `SKILL.md` | CR-TASK-07 (M) | No drift |
| TU-6 | ~25 lines at row 8 on `SKILL.md` | CR-TASK-08 (M) | No drift |
| TU-7 | ~15 lines at row 8 on `SKILL.md` | CR-TASK-09 (S) | No drift |
| TU-8 | ~20 lines at row 11 on `SKILL.md` | CR-TASK-10 (M) | No drift |

**Drift count: 0 / 8.**

T07.03 § 4 (reverse traceability) independently confirms zero drift: every absorption row lands at the manifest-named extension-point row on the manifest-named file path within the manifest's effort envelope. No row's shape, file path, change type, or effort envelope differs materially from the Phase 5 integration sketch.

**V/C/K re-score outcome:** **NO RE-SCORE REQUIRED** for any of the 8 TUs. The Phase 5 manifest verdicts (8 ADOPT/ADAPT entries) carry forward unchanged into `final-merge-plan.md`. (For reference, the V/C/K verdicts from `transfer-manifest.md` § 4 are: TU-1 ADOPT; TU-2 ADOPT; TU-3 ADAPT; TU-4 ADAPT; TU-5 ADOPT; TU-6 ADOPT; TU-7 ADOPT; TU-8 ADOPT.)

**R-RULE-11 note on re-score absence:** because no re-score changes a verdict, the re-debate note required by R-RULE-11 for verdict-changing re-scores is not triggered for any TU. The audit clause stands: any future re-score that changes a verdict must carry an explicit re-debate note citing the manifest exception(s) it invokes.

---

## 5. Open-findings register (carry-forward to `final-merge-plan.md`)

Eight open findings carry forward from T07.01 cross-examination, the `compat-hazard-report.md` carry-forward list (T07.02 § 8), and the procedural authorization note (T07.01 § 3.7 / Q2 § 4.1):

| ID | Severity | Title | Finding source | Disposition in `final-merge-plan.md` |
|---|---|---|---|---|
| F-01 | LOW | Per-item Tier marker boundary phrasing (read vs dispatch) | T07.01 § 2.1 / § 2.3 on CR-FM-02 / CR-TASK-03 | § 4.1 — paragraph naming "tier-conditioned read" as the authorized consumption shape; ME-1 cited as the canonical rejection mechanism for any future per-item dispatch consumer |
| F-02 | MEDIUM | CR-7 / CR-8 ordering review-dependent | T07.01 § 2.1 on CR-TASK-01 / CR-TASK-04 | § 4.2 — **CR-FM-04 audit scope extended** to grep for `path_override_check → tier_field_validate → gate_1_dispatch` in-order (row 1) and `forced_stance_read → tier_field_read → gate_2_dispatch` in-order (row 10); **CR-TASK-12 verbatim diff** treats this ordering as load-bearing; alternate mitigation is a sentinel comment block in the inserted code text naming CR-7/CR-8 |
| F-03 | MEDIUM | CR-TASK-06 git-dirty behavior unspecified | T07.01 § 2.2 on CR-TASK-06 | § 4.3 — acceptance criterion clause added to CR-TASK-06: `git status` returning a dirty tree on STRICT pre-flight **logs a warning to the Task Log and continues** (Reading A); INV-01 progress guarantee preserved |
| F-04 | MEDIUM | CR-TASK-07 baseline-absent fallback unspecified for CR-TASK-09 | T07.01 § 2.3 on CR-TASK-07 / CR-TASK-09 | § 4.4 — acceptance criterion clause added to CR-TASK-09: when `research/test-baseline.yaml` is absent or empty on a STRICT/STANDARD task, **CR-TASK-09 classifies all observed test failures as "new"** (Reading A — conservative over-escalate); INV-03 floor preserved |
| F-05 | MEDIUM | INV-03 surface widening (mid-phase rf-qa via TFEP escalation) | T07.01 § 4.2 Q1 on CR-TASK-09 | § 4.5 — explicit sentence in `final-merge-plan.md` § 0 documenting TU-7's authorized mid-phase escalation routing as the **third rf-qa invocation point** alongside phase-gate and post-completion; routes to existing verifier identity (ME-2 preserved) via existing spawn pattern (no new verifier-spawn surface) |
| F-06 | LOW | `invariant-bounds.md` (T03.01) does not exist; reviewer used `extension-point-contracts.md` § "Invariant Reference" as functional substitute | T07.01 substitution notice | § 4.6 — `final-merge-plan.md` § 0 cites `extension-point-contracts.md:11-17` as the canonical INV anchor source for this sprint; the T03.01 retroactive authoring is recommended but not blocking for Phase 7 execution |
| F-07 | LOW | Donor hard-deletion is procedurally authorized, not manifest-bound | T07.01 § 3.7 / § 4.1 Q2 on CR-DEP-03 | § 4.7 — `final-merge-plan.md` § 5 (CR-DEP-03 row) adds one sentence naming the procedural authorization chain: sprint goal → T06.03 task description → `refactor-sctask-deprecation.md` § 2 rubric + § 4 absorption traceability |
| F-08 | LOW | Five-vs-six refactor file count inconsistency in `merge-master.md:7` and T07.01 task description | T07.01 § 4.1 Q1 cross-examination | § 4.8 — `final-merge-plan.md` § 0 records **six** refactor artifacts (or **three** Phase 6 refactor-area pairs); the "five" figure is corrected throughout |

**Severity roll-up:**

| Severity | Count | Disposition |
|---|---|---|
| HIGH | 0 | — |
| MEDIUM | 4 (F-02, F-03, F-04, F-05) | All closed in `final-merge-plan.md` § 4 with acceptance-criterion clauses |
| LOW | 4 (F-01, F-06, F-07, F-08) | All closed in `final-merge-plan.md` § 4 with documentation strengtheners |

**Zero HIGH-severity findings. Zero invariant violations. Zero manifest drifts. Zero scope expansions. Zero ledger re-proposals.**

---

## 6. Compat-hazard register (T07.02 carry-forward)

Eighteen hazards in `compat-hazard-report.md` are all mitigated in plan. The four sequencing-sensitive hazards are recorded as binding constraints in `final-merge-plan.md` § 6:

| Hazard | Severity | Mitigation in plan | Sequencing constraint recorded in final plan |
|---|---|---|---|
| HZ-01 (existing TASK-* files lack `Tier:`) | CRITICAL (unmitigated) | CR-FM-01 optional + CR-FM-03 default + CR-FM-04 audit | None new — Step 1 atomic |
| HZ-02 (lowercase `tier:` collision) | LOW | CR-FM-04 audit | None |
| HZ-03 (in-flight TASK-PRD-20260514-121039 references `/sc:task` as research subject) | HIGH | Option (a): complete the in-flight PRD **before** CR-DEP-01 lands | **Recorded** (§ 6 constraint S-1) |
| HZ-04 (TASK-RESEARCH-20260403 stale status) | LOW | Out of scope | None |
| HZ-05 (`task-builder-merge` sprint) | NONE | N/A | None |
| HZ-06 (`sprint/process.py` emits `/sc:task`) | CRITICAL | CR-REF-01 same-commit-or-earlier as CR-DEP-01 | **Recorded** (§ 6 constraint S-2) |
| HZ-07 (`cleanup_audit/prompts.py` emits `/sc:task`) | CRITICAL | CR-REF-02 same-commit-or-earlier as CR-DEP-01 | **Recorded** (§ 6 constraint S-2) |
| HZ-08 (user-typed `/sc:task` after deprecation) | MEDIUM | CR-DEP-01 stub body is the redirect | Accepted UX cost |
| HZ-09 (`docs/user-guide/commands.md`) | HIGH | CR-DOC-01 atomic with CR-DEP-01 + CR-TASK-02 | Already in Step 5/8 |
| HZ-10 (`flags.md`, `sprint-cli-deep-dive.md`) | MEDIUM | CR-DOC-02, CR-DOC-03 | Step 8 |
| HZ-11 (`docs/generated/*`) | LOW | CR-DOC-10..12 `leave-as-is` | Step 10 |
| HZ-12 (`docs/analysis/*`, `docs/guides/*`) | MEDIUM | CR-DOC-04..07 | Steps 8 + 9 |
| HZ-13 (`scripts/sync_from_framework.py:84`) | LOW | CR-REF-11 | Step 7 |
| HZ-14 (Makefile sync rule drift) | HIGH | CR-DIST-02 atomic with CR-DEP-03 + CR-DEP-04 | **Recorded** (§ 6 constraint S-3) |
| HZ-15 (`v5.xxforensic` backlog) | LOW | CR-REF-18 cluster-root note | Step 9 |
| HZ-16 (v3.75 archive) | LOW | CR-REF-BUCKET-B optional note | Step 9 (optional) |
| HZ-17 (CLAUDE.md / user-global) | NONE | N/A | None |
| HZ-18 (top-level README.md) | MEDIUM | CR-DIST-05 (no `/sc:task` reference — no-op verified at commit) | Step 6 / Step 7 |

**Sequencing constraints carried into `final-merge-plan.md`:**

1. **S-1 (from HZ-03):** TASK-PRD-20260514-121039 must complete (status → `🟢 Done`) **before** Step 5 (CR-DEP-01 soft-deprecation).
2. **S-2 (from HZ-06 + HZ-07):** CR-REF-01 and CR-REF-02 ship in the **same commit as** CR-DEP-01 (Step 5), never later.
3. **S-3 (from HZ-14):** CR-DIST-02 (`Makefile` sync-dev orphan-prune) ships **atomically** with CR-DEP-03 + CR-DEP-04 (Step 6), in the same commit.

Constraint S-2 and S-3 were already implicit in `merge-master.md` § 6 Step 5 / Step 6; T07.02 confirms them as load-bearing and `final-merge-plan.md` § 6 records them explicitly. Constraint S-1 is **new** to the merge plan (touches a scheduling concern outside the milestone graph, not a CR-row dependency edge).

---

## 7. Traceability & invariant-survival summary

Per T07.03:

- **Forward traceability:** 8 / 8 TUs map to ≥ 1 Phase 6 absorption row. (`traceability-gap-report.md` § 3.)
- **Reverse traceability:** 65 / 65 CR rows trace to a TU or to a documented derivative-responsibility bucket (CS-M4-A / CS-M4-B / CS-M5-A / CS-M5-B / R-RULE-10 / R-RULE-06 / R-RULE-11). (`traceability-gap-report.md` § 4.)
- **Two-way coverage:** 92 / 92 assertions; zero hard gaps. (`traceability-gap-report.md` § 5.)
- **Soft observations:** 6 — all CLOSE or JUSTIFY dispositions. (`traceability-gap-report.md` § 6.2.)
- **Invariant survival:** INV-01..INV-05 each demonstrated to survive on the merged surface via a worked example exercising all 8 absorbed TUs. (`invariant-survival-walkthrough.md` § 2 + § 3.)
- **Counter-factual register:** 16 donor variants explicitly blocked by manifest exceptions or ledger entries. (`invariant-survival-walkthrough.md` § 4.)

---

## 8. Acceptance Criteria recap (T07.04 AC #1–#4)

| AC | Statement | Status |
|---|---|---|
| **AC #1** | `validation-report.md` exists with a pass/fail verdict per Phase 6 plan item and per manifest feature, each tied to its finding source | ✅ — § 2 (67/67 PASS register), § 3 (TU / ME / donor-drop / ledger registers), § 5 (open-findings register), § 6 (hazard register) |
| **AC #2** | Every drifted feature is re-scored with the V/C/K rubric and the re-score is documented (R-RULE-07) | ✅ — § 4: zero drift across 8 TUs (T07.01 § 3.5 + T07.03 § 4 concur); no re-score required; R-RULE-11 re-debate clause stands for any future verdict change |
| **AC #3** | `final-merge-plan.md` exists with all Phase 7 corrections applied and zero open findings | (delivered by companion artifact; this report defines the binding correction list F-01..F-08 + S-1..S-3) |
| **AC #4** | No `rejected-features-ledger.md` entry is re-introduced; any verdict change carries a re-debate note (R-RULE-11) | ✅ — § 3.4: 26/26 ledger entries TERMINAL; § 4: zero verdict-changing re-scores; no re-debate note triggered |

---

## 9. Validation hooks (T07.04 Validation block)

**Sub-agent verification (T07.04 Validation #1):** an independent agent can confirm `final-merge-plan.md` has zero open findings and every correction traces to a Phase 7 artifact by:

1. Grepping `final-merge-plan.md` § 4 for each F-01..F-08 disposition and confirming the cited source artifact (this report § 5) exists.
2. Grepping `final-merge-plan.md` § 6 for each S-1..S-3 sequencing constraint and confirming the cited hazard (`compat-hazard-report.md` HZ-NN) exists.
3. Confirming `final-merge-plan.md` § 5 carries the same 67 row-line-items as `merge-master.md` § 1 (no row added, no row removed).
4. Confirming `final-merge-plan.md` § 3.1 reports the same 8 TU forward-map as `merge-master.md` § 3.1 (no verdict change; no V/C/K re-score).

**Manual reviewer check (T07.04 Validation #2):** the reviewer can recompute a sample of the no-drift V/C/K assessments in § 4 by:

1. Picking 3 TUs (e.g., TU-1, TU-3, TU-7).
2. Reading the corresponding `transfer-manifest.md` § 2 "Shape of change" sketch.
3. Reading the corresponding Phase 6 row(s) in the originating refactor file.
4. Confirming file path, extension-point row touched, change type, and effort envelope match — and that V (validation evidence weight), C (complexity), K (knowledge basis) each remain at their Phase 5 scores.

---

**T07.04 deliverable #1: COMPLETE.** Validation report consolidates the eight Phase 7 findings, the eighteen compat hazards, the two-way traceability coverage, and the invariant-survival walkthrough into a single pass/fail register: **67/67 plan items PASS** (7 with note), **8/8 TUs PASS** (zero drift; no V/C/K re-score required), **9/9 MEs HELD**, **10/10 donor ceremonies NOT REVIVED**, **26/26 ledger entries TERMINAL**, **INV-01..INV-05 SURVIVE**, **18/18 hazards MITIGATED**. The companion `final-merge-plan.md` applies the eight findings as targeted plan corrections and locks the three new sequencing constraints.

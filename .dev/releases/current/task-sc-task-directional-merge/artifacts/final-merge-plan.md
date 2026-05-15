# Final Merge Plan — Validated Master Plan (Phase 7 / T07.04)

**Task:** T07.04 — Re-score drifted features; produce `validation-report.md` & `final-merge-plan.md`
**Roadmap Item:** R-027
**Tier:** STRICT
**Generated:** 2026-05-15
**Status:** The validated, corrected master plan. This file = `merge-master.md` (T06.05) **plus all Phase 7 corrections applied** (T07.01..T07.04 findings F-01..F-08 + hazard-derived sequencing constraints S-1..S-3). Zero open findings remain. This is the binding plan for any downstream implementation sprint.

---

## 0. Document scope, INV anchor source, and corrections summary

**Authority chain:** `final-merge-plan.md` (this file) > `merge-master.md` (T06.05; superseded for any Phase 7-affected row) > the six refactor files (still authoritative for the eight-column row text where not modified by Phase 7) > `transfer-manifest.md` (still authoritative for TU / ME / donor-ceremony-drop definitions).

**Inputs (Phase 7-verified present):**

- `merge-master.md` (T06.05) — consolidated 67 row-line-items / 65 distinct CR-IDs; acyclic dependency graph; 10-step canonical commit sequence.
- The **six** refactor artifacts (corrects the "five" figure in `merge-master.md:7` — see § 4.8 below): `refactor-task-skill.md` (CR-TASK-01..12) + `refactor-mdtm-frontmatter.md` (CR-FM-01..04) + `refactor-sctask-deprecation.md` (CR-DEP-01..05) + `refactor-references.md` (CR-REF-01..18 + CR-REF-BUCKET-A..H) + `refactor-distribution.md` (CR-DIST-01..06) + `refactor-documentation.md` (CR-DOC-01..13). These six files map to **three Phase 6 refactor-area pairs** (skill + frontmatter / deprecation + references / distribution + documentation).
- `transfer-manifest.md` (T05.03) — 8 transfer units TU-1..TU-8; 9 manifest exceptions ME-1..ME-9.
- `rejected-features-ledger.md` (T05.03) — 26 terminal ledger entries (17 REJECT + 9 DEFER).
- `extension-point-contracts.md` (T03.02) — **canonical INV-01..INV-05 anchor source for this sprint** (see F-06 below): lines 11–17 ("Invariant Reference (anchor labels, pending T03.01 expansion)") + per-extension-point INV-protection map.
- `plan-adversarial-review.md` (T07.01), `file-reference-reverification.md` + `compat-hazard-report.md` (T07.02), `traceability-gap-report.md` + `invariant-survival-walkthrough.md` (T07.03), `validation-report.md` (T07.04 companion).

**INV anchor source (F-06 disposition).** `invariant-bounds.md` (T03.01) was scheduled but never authored as a standalone file; T03.01 emitted the anchor labels into `extension-point-contracts.md:11-17` instead. For Phase 7 execution this final plan **cites `extension-point-contracts.md:11-17` as the canonical INV-01..INV-05 source**. The anchor language is byte-identical to the sprint spec § "Load-bearing invariants" that `invariant-bounds.md` was scheduled to expand. The retroactive authoring of `invariant-bounds.md` is a documentation hygiene action and is **not blocking** for downstream implementation.

**INV-03 surface widening notice (F-05 disposition).** The merged `/task` surface invokes `rf-qa` at **three** locations, not two: (a) phase-gate between phases (Phase 2+) per the canonical INV-03 rule, (b) post-completion per the canonical INV-03 rule, and (c) **mid-phase via TU-7's TFEP escalation trigger detection (CR-TASK-09)**, routed through the existing Phase-Gate QA verifier-spawn pattern (`SKILL.md:191-198`). This third invocation point is an **authorized INV-03 surface extension**, not a violation: it routes to the existing verifier identity (`rf-qa`, ME-2 preserved — never replaces, never adds a sibling verifier), uses the existing spawn pattern (no new verifier-spawn surface), and is named by TU-7's "Recipient form" definition. Any future Phase 7 reviewer encountering CR-TASK-09 should treat the mid-phase routing as plan-bound, not as a surface widening that requires further authorization.

**Phase 7 corrections summary.** Eight open findings F-01..F-08 (from T07.01) and three sequencing constraints S-1..S-3 (from T07.02) are applied to the plan in § 4 + § 6 below. § 5 (the master row table) carries the eight-column digest from `merge-master.md` § 1 *with* the row-level deltas for the four rows that gained acceptance-criterion clauses (CR-TASK-06 + CR-TASK-09 + CR-FM-04 + CR-TASK-12). No row is added or removed. The 67-row count, the 65 distinct CR-IDs, the acyclic dependency graph, and the 10-step canonical commit sequence are unchanged. All eight V/C/K verdicts (TU-1..TU-8) carry forward unchanged from `transfer-manifest.md` § 4 — **zero drift, no re-score required** (`validation-report.md` § 4).

---

## 1. Verdict roll-up (carry-forward from `validation-report.md` § 1)

| Verdict bucket | Count | Outcome |
|---|---|---|
| Phase 6 plan items (CR rows) — PASS | 67 / 67 | All pass adversarial review, file re-verification, traceability check, and invariant-survival walkthrough. |
| of which PASS WITH NOTE → CLOSED by § 4 | 7 (CR-FM-02, CR-TASK-01, CR-TASK-03, CR-TASK-04, CR-TASK-06, CR-TASK-07, CR-TASK-09) | All seven notes are closed by F-01..F-05 dispositions in § 4. |
| Manifest TUs — PASS | 8 / 8 | Zero drift; no V/C/K re-score. |
| Manifest exceptions — HELD | 9 / 9 | — |
| Donor-ceremony drops — NOT REVIVED | 10 / 10 | — |
| Ledger entries — TERMINAL | 26 / 26 | R-RULE-11 holds. |
| Invariants — SURVIVE | 5 / 5 | Demonstrated by `invariant-survival-walkthrough.md` § 2 + § 3. |
| Compat hazards — MITIGATED | 18 / 18 | Three sequencing constraints S-1..S-3 (§ 6). |
| Open findings — CLOSED in this plan | 8 / 8 | F-01..F-08 closed in § 4. |

**Overall:** **PASS. ZERO OPEN FINDINGS.** This plan is the binding execution index for any downstream implementation sprint.

---

## 2. Two-way traceability (carry-forward from `merge-master.md` § 3 + `traceability-gap-report.md` § 5)

### 2.1 Forward — every TU has at least one CR row

| Manifest TU | V/C/K verdict (carried forward) | Phase 6 row(s) | Drift |
|---|---|---|---|
| TU-1 (`Tier:` field + Gate 1 + per-item marker) | ADOPT | CR-FM-01, CR-FM-02, CR-FM-03, CR-FM-04 (audit), CR-TASK-02, CR-TASK-03 | None |
| TU-2 (Critical/Trivial Path Override) | ADOPT | CR-TASK-01, CR-TASK-04 | None |
| TU-3 (Gate 2 Verification routing widening) | ADAPT | CR-TASK-05 | None |
| TU-4 (D15b Layer 2 pre-flight) | ADAPT | CR-TASK-06 | None |
| TU-5 (TFEP Test baseline snapshot) | ADOPT | CR-TASK-07 | None |
| TU-6 (TFEP Prohibitions + Carve-outs) | ADOPT | CR-TASK-08 | None |
| TU-7 (TFEP Escalation trigger detection) | ADOPT | CR-TASK-09 | None (INV-03 mid-phase routing documented in § 0 — not drift) |
| TU-8 (TFEP Incident reporting) | ADOPT | CR-TASK-10 | None |

**Forward coverage: 8 / 8 mapped; 0 / 8 drifted.**

### 2.2 Reverse — every CR row traces to a TU or to a named derivative responsibility

The reverse direction inherits from `merge-master.md` § 3.2 unchanged. Aggregated: **65 / 65 CR-IDs trace** (14 absorption + 2 mechanical/audit + 5 deprecation + 39 reference + 6 distribution + 13 documentation = 79 rows including bucket sub-IDs, condensed into 65 distinct CR-IDs as enumerated in `traceability-gap-report.md` § 4). Two-way coverage = 92 / 92 assertions; zero hard gaps.

### 2.3 R-RULE-11 ledger cross-check

Per `merge-master.md` § 4 + `validation-report.md` § 3.4: **0 / 26 ledger entries re-proposed across the 65 distinct CR-IDs.** R-RULE-11 holds at the consolidated level.

---

## 3. Invariant survival (carry-forward from `invariant-survival-walkthrough.md`)

INV-01..INV-05 each demonstrated (not asserted) to survive on the merged surface via the `TASK-EXAMPLE-20260515-strict-walkthrough.md` worked example (10-stage step-by-step run; per-invariant interaction tables; 16-row counter-factual register naming the donor variants the manifest explicitly blocked). Per § 3 of the walkthrough:

| Invariant | Verdict | Load-bearing absorbed-feature interaction |
|---|---|---|
| INV-01 (F1 loop semantics) | SURVIVES | TU-1 / TU-2 / TU-4..TU-8 — every absorbed feature either runs PRE-LOOP, runs side-channel, or is a read at item time. None re-author EXECUTE substitution. |
| INV-02 (Prohibited-actions catalog F2) | SURVIVES | TU-6 *reinforces* F2 (prohibitions catalog mirrors existing F2 rules); no absorbed feature weakens F2. |
| INV-03 (Phase-gate `rf-qa` + post-completion) | SURVIVES | TU-3 widens roster (`rf-qa` always present, ME-2 binds); TU-7 routes mid-phase via the existing spawn pattern (authorized widening per § 0). |
| INV-04 (Resumability) | SURVIVES | CR-FM-03 compat shim; TU-5 baseline YAML on disk; TU-8 incident-report file on disk; task-log lines append-only. |
| INV-05 (Refusal-of-definition) | SURVIVES | TU-1 `Tier:` is metadata, not work-definition; CR-TASK-02 reads declaratively (no runtime classifier); D09b / D08 / D01 / D13 / D06 all REJECTed. |

---

## 4. Phase 7 corrections — open findings closed (F-01..F-08)

Each finding below is closed in this final plan by an explicit acceptance-criterion clause, scope extension, or documentation paragraph. The eight closures are the *only* deltas this plan introduces relative to `merge-master.md` § 1.

### 4.1 F-01 (LOW) — Per-item Tier marker read-vs-dispatch boundary

**Finding (T07.01 § 2.1 / § 2.3 on CR-FM-02 / CR-TASK-03).** The boundary between "per-item read-only tier-conditioned check" (authorized by ME-1) and "per-item dispatch" (forbidden by ME-1) is conceptually thin. The plan's defense is that the execution profile is pinned by pre-loop Gate 1 and the per-item marker only conditions reads against pre-existing tier-gated side effects.

**Closure.** This final plan names the authorized consumption shape as a **"tier-conditioned read"** with the following bounds:

- The per-item `(Tier: <enum>)` marker is consumed only by behaviors already gated by the task-level `Tier:` field at Gate 1 (e.g., CR-TASK-07 baseline-skip).
- The per-item marker NEVER re-fires Gate 1, NEVER selects a different `rf-qa` roster, NEVER substitutes a different EXECUTE path, NEVER changes the item-type dispatch table.
- Any future consumer that attempts to use the per-item marker for **dispatch** (rather than for reading a pre-gated behavior's tier flag) is an ME-1 violation and must be rejected at design-time per R-RULE-11; if the consumer is desirable, it must be re-litigated through a new manifest exception, not silently added.

**Rows touched by this closure:** CR-FM-02 acceptance criterion #4 (already states "read-only for the item — never re-fires Gate 1 dispatch (ME-1 binding)"); CR-TASK-03 acceptance criterion adds: *"per-item `(Tier: …)` overrides task-level for tier-conditioned reads only; never re-fires Gate 1; never modifies item-type dispatch or verifier roster (ME-1 binding)."*

---

### 4.2 F-02 (MEDIUM) — CR-7 / CR-8 ordering structurally enforced

**Finding (T07.01 § 2.1 on CR-TASK-01 / CR-TASK-04).** CR-7 / CR-8 ordering enforcement (`path_override_check → tier_field_validate → gate_1_dispatch` at row 1; `forced_stance_read → tier_field_read → gate_2_dispatch` at row 10) is review-dependent in the original plan. A future "readability" refactor could reorder the three steps inside *Validating the Task File* without breaking any test.

**Closure.** Two complementary mitigations are applied:

1. **CR-FM-04 audit scope extension (binding).** This plan extends CR-FM-04's acceptance criteria to include two grep-based ordering checks:
   - **Row 1 ordering check.** `grep -n -E "(path_override_check|tier_field_validate|gate_1_dispatch)"` against `[src] src/superclaude/skills/task/SKILL.md` returns the three function names in that exact line order. Any reordering blocks commit.
   - **Row 10 ordering check.** `grep -n -E "(forced_stance_read|tier_field_read|gate_2_dispatch)"` against the same file returns the three function names in that exact line order at the Phase-Gate QA Verification section.
2. **Sentinel comment block (binding).** The inserted code text at row 1 and row 10 includes a one-line sentinel comment immediately before each of the three function-call sequences: `# CR-7 ORDERING — load-bearing: path_override_check FIRST. Do not reorder.` and `# CR-8 ORDERING — load-bearing: forced_stance_read FIRST. Do not reorder.` These sentinels are themselves grep-targets and become part of the CR-TASK-12 verbatim-diff audit.

**Rows touched by this closure:** CR-FM-04 acceptance criterion gains the two ordering greps; CR-TASK-01 and CR-TASK-04 acceptance criteria gain the sentinel-comment text; CR-TASK-12's six-diff audit becomes a **seven-diff audit** (the two sentinels are added as additional verbatim blocks).

---

### 4.3 F-03 (MEDIUM) — CR-TASK-06 git-dirty behavior pinned

**Finding (T07.01 § 2.2 on CR-TASK-06).** STRICT pre-flight runs `git_status_clean_tree_check`. The plan specifies "graceful skip on unavailability" for MCP tools but is silent on behavior when the tool IS available but reports a dirty tree.

**Closure (Reading A — log+continue).** This plan adds the following acceptance-criterion clause to CR-TASK-06:

> **AC-CR-TASK-06-F03.** When `git status` returns a dirty tree on STRICT pre-flight, the F1 loop **MUST NOT** halt or refuse task entry. The pre-flight emits exactly one Task Log line of the form `gate-1.5: pre-flight tier=STRICT git_status=dirty action=warn-and-continue` and proceeds to the next pre-flight check. Refusing task entry on a dirty tree is forbidden — it would introduce a new HALT semantic at pre-loop entry and weaken INV-01's progress guarantee. The dirty-tree warning is informational; the human or the upstream task author owns the decision to clean the tree.

**Rationale (Reading A chosen over Reading B):** (a) preserves INV-01 progress guarantee; (b) consistent with the "graceful skip" pattern already applied to MCP tool unavailability; (c) STRICT tier-conditioned setup actions are environment-prep, not authorization gates.

**Rows touched by this closure:** CR-TASK-06 acceptance criteria.

---

### 4.4 F-04 (MEDIUM) — CR-TASK-07 baseline-absent fallback pinned

**Finding (T07.01 § 2.3 on CR-TASK-07 / CR-TASK-09).** The plan does not specify CR-TASK-09's behavior on STRICT/STANDARD when `research/test-baseline.yaml` is absent or empty.

**Closure (Reading A — over-escalate).** This plan adds the following acceptance-criterion clause to CR-TASK-09:

> **AC-CR-TASK-09-F04.** When CR-TASK-09's `tfep_escalation_check` runs on a STRICT or STANDARD task and `research/test-baseline.yaml` is **absent OR empty OR YAML-malformed**, the check **MUST** classify every observed `pytest` failure during the post-EXECUTE check as `classification=new` (conservative over-escalate). The check **MUST NOT** silently skip classification, and **MUST NOT** refuse task entry. Exactly one Task Log line of the form `tfep: baseline=absent classification=new-all reason=<absent|empty|malformed>` is emitted to record the fallback. The over-escalation routes more failures to `rf-qa` via the existing INV-03 surface — which is the INV-03-spirit-preserving choice (the rf-qa floor remains intact; the cost is a possibly-noisier escalation queue).
>
> *Why Reading A and not Reading B (refuse at task entry) or Reading C (silently skip):* refusal would weaken INV-01; silent skip would weaken INV-03's floor. Over-escalation preserves both.

**Rows touched by this closure:** CR-TASK-09 acceptance criteria.

---

### 4.5 F-05 (MEDIUM) — INV-03 mid-phase routing documented as authorized widening

**Finding (T07.01 § 4.2 Q1 on CR-TASK-09).** CR-TASK-09 routes `rf-qa` mid-phase (at error-handling time inside F1's execution of a single item). The canonical INV-03 anchor language locates `rf-qa` at phase-boundaries and post-completion only. The plan calls this "the existing INV-03 surface" but does not explicitly call it a surface widening.

**Closure.** Documented in § 0 of this plan ("INV-03 surface widening notice") as **authorized**: it routes to the existing verifier identity (ME-2 preserved); uses the existing spawn pattern in `SKILL.md:191-198` (no new verifier-spawn surface); is named by TU-7's "Recipient form" definition; and is the *only* way to honor TU-7's adjudication semantic without authoring a new escalation gate (LR-REJECT-2 / D25 not revived).

The merged `/task` surface therefore invokes `rf-qa` at three locations (phase-gate, post-completion, mid-phase TFEP escalation). Future reviewers should treat the mid-phase invocation as plan-bound, not as further surface-widening to authorize.

**Rows touched by this closure:** none — this is a documentation paragraph in § 0; no row's acceptance criteria change. Phase 7 implementation does not need to author anything new for F-05.

---

### 4.6 F-06 (LOW) — `invariant-bounds.md` substitution recorded

**Finding (T07.01 substitution notice).** `invariant-bounds.md` (T03.01) does not exist; T03.01 emitted the INV anchor labels into `extension-point-contracts.md:11-17`.

**Closure.** This plan cites `extension-point-contracts.md:11-17` as the canonical INV-01..INV-05 source for the entire Phase 7 + downstream execution scope (§ 0 above). Retroactive authoring of `invariant-bounds.md` is optional documentation hygiene; it is **not** a Phase 7 blocking item. If authored later, the file should be byte-identical to the anchor-label table in `extension-point-contracts.md:11-17` plus the worked-example evidence in `invariant-survival-walkthrough.md` § 3.

**Rows touched by this closure:** none.

---

### 4.7 F-07 (LOW) — Donor hard-deletion procedural authorization chain documented

**Finding (T07.01 § 3.7 / § 4.1 Q2 on CR-DEP-03).** `transfer-manifest.md` § 5 names the recipient attach target and the source-tree edit ordering, but does NOT explicitly authorize *hard-deletion* of donor artifacts.

**Closure.** This plan adds the procedural authorization chain to CR-DEP-03's row entry in § 5 below. The authorization flows:

1. **Sprint goal** — "`/sc:task` deprecation" (overarching sprint outcome named in the sprint spec).
2. **T06.03 task description** — "`refactor-sctask-deprecation.md` — the deprecation plan for `/sc:task`: soft-deprecation … vs hard-deprecation …, chosen per artifact and justified" (named per-artifact disposition authority).
3. **`refactor-sctask-deprecation.md` § 2 rubric** — chooses soft vs hard per artifact and justifies.
4. **`refactor-sctask-deprecation.md` § 4 absorption traceability** — every absorbed pattern landed at `[src] src/superclaude/skills/task/SKILL.md`; donor body is now redundant ceremony per R-RULE-06.
5. **Structural precondition** — CR-TASK-01..10 + CR-FM-01..03 land before CR-DEP-03 (dependency edge in § 6 + the M3 → M4 boundary in `merge-master.md` § 5).

This is a procedural authorization, not a manifest binding. Future reviewers should accept the chain and not require a retroactive manifest amendment.

**Rows touched by this closure:** CR-DEP-03 row in § 5 gains an annotation `(procedural-auth chain: sprint goal → T06.03 → refactor-sctask-deprecation.md § 2 + § 4)`.

---

### 4.8 F-08 (LOW) — Five-vs-six refactor file count corrected

**Finding (T07.01 § 4.1 Q1 cross-examination).** `merge-master.md:7` says "every change row from the **five** refactor-`*.md` files (six artifacts)" — internally inconsistent.

**Closure.** This plan records **six** refactor artifacts grouped into **three Phase 6 refactor-area pairs** (skill + frontmatter; deprecation + references; distribution + documentation). The "five" figure was a counting inconsistency that propagated forward from earlier phase planning. Every one of the six files is binding; the "five" figure is corrected to "six" throughout this plan (see § 0).

**Rows touched by this closure:** none — this is a count correction in § 0.

---

## 5. Master ordered table — every change row (carry-forward from `merge-master.md` § 1 with Phase 7 row-deltas applied)

The 67 row-line-items / 65 distinct CR-IDs from `merge-master.md` § 1.1–§ 1.12 are inherited **unchanged in count, order, and dependency edges**. Acceptance-criterion text for four rows is augmented per § 4 above. All other column text is identical to `merge-master.md` § 1; this section gives the **row-delta-aware** authoritative read.

> **Per R-RULE-11 audit clause (this plan):** no row below silently re-litigates a `rejected-features-ledger.md` entry; no row authors a new HALT semantic in F1 (per F-03 + ME-3); no row authors a per-item runtime classifier or per-item dispatch (per F-01 + ME-1); no row replaces `rf-qa` (per ME-2); no row breaks resumability for existing on-disk task files (per CR-FM-03 + INV-04).

### 5.1 M1 — Foundation (atomic merge; CR-FM-01..03 + CR-TASK-01..04; P0)

| # | CR-ID | Acceptance digest (Phase 7 delta) | Phase 7 finding closures |
|---|---|---|---|
| 1 | CR-FM-01 | (unchanged from `merge-master.md`) optional `Tier:` field; closed-enum; default `STANDARD`. | — |
| 2 | CR-FM-02 | (unchanged) parser reads marker; fallback to task-level; never re-fires Gate 1. **Per F-01 closure (§ 4.1):** authorized consumption shape = "tier-conditioned read"; ME-1 is the canonical rejection mechanism for any future per-item dispatch consumer. | F-01 |
| 3 | CR-FM-03 | (unchanged) existing TASK-* files validate clean; default `STANDARD`; NO migration. | — |
| 4 | CR-TASK-01 | (unchanged base) Task Log `path-override: forced_stance=…` emitted first at task entry. **Per F-02 closure (§ 4.2):** the inserted code text MUST carry the sentinel comment `# CR-7 ORDERING — load-bearing: path_override_check FIRST. Do not reorder.` immediately before the three-call sequence at row 1. | F-02 |
| 5 | CR-TASK-02 | (unchanged) malformed `Tier:` rejected; single Task Log `gate-1: dispatch_profile=… source=…` once at entry. | — |
| 6 | CR-TASK-03 | (unchanged base) per-item `(Tier: …)` overrides task-level for tier-conditioned reads only. **Per F-01 closure (§ 4.1):** acceptance criterion explicitly forbids per-item dispatch / verifier-roster modification / item-type-table modification via the per-item marker; ME-1 is the audit gate. | F-01 (cross-ref) |
| 7 | CR-TASK-04 | (unchanged base) qa-stance-source attribution emitted; `forced_stance=STRICT` overrides `Tier:` at Gate 2. **Per F-02 closure (§ 4.2):** the inserted code text MUST carry the sentinel comment `# CR-8 ORDERING — load-bearing: forced_stance_read FIRST. Do not reorder.` immediately before the three-call sequence at row 10. | F-02 (cross-ref) |

**M1 atomicity rule (ME-6 + CR-7 + CR-9):** rows 1–7 ship in **one source-tree merge**. Inherited unchanged from `merge-master.md` § 1.1.

### 5.2 M2 — Tier-Conditioned Behaviors (P1; depends on M1)

| # | CR-ID | Acceptance digest (Phase 7 delta) | Phase 7 finding closures |
|---|---|---|---|
| 8 | CR-TASK-05 | (unchanged) `verifier_roster: [rf-qa, quality-engineer]` on STRICT; `rf-qa` always present (ME-2). | — |
| 9 | CR-TASK-06 | (unchanged base) Task Log `gate-1.5: pre-flight tier=… ran=[…]` once before F1 first iteration. **Per F-03 closure (§ 4.3 / AC-CR-TASK-06-F03):** on STRICT pre-flight, a dirty `git status` tree emits `gate-1.5: pre-flight tier=STRICT git_status=dirty action=warn-and-continue` and PROCEEDS. Refusing task entry is forbidden. | F-03 |

### 5.3 M3 — TFEP Cluster (P2)

| # | CR-ID | Acceptance digest (Phase 7 delta) | Phase 7 finding closures |
|---|---|---|---|
| 10 | CR-TASK-07 | (unchanged base) baseline YAML present pre-F1 on STRICT/STANDARD; absent on LIGHT/EXEMPT. **Per F-04 closure (§ 4.4):** baseline-absent-on-STRICT/STANDARD is **acceptable** at task entry (does not refuse entry); CR-TASK-09 handles the absent case via AC-CR-TASK-09-F04 (over-escalate). | F-04 (cross-ref) |
| 11 | CR-TASK-08 | (unchanged) `tfep: prohibition-refusal …` / `carve-out …` Task Log lines; F1 continues. | — |
| 12 | CR-TASK-09 | (unchanged base) `tfep: escalation-trigger fired=… classification=…`; route to existing `rf-qa`. **Per F-04 closure (§ 4.4 / AC-CR-TASK-09-F04):** when baseline is absent / empty / malformed on STRICT/STANDARD, classify all `pytest` failures as `classification=new`; emit `tfep: baseline=absent classification=new-all reason=<absent\|empty\|malformed>`; never refuse task entry; never silently skip. **Per F-05 closure (§ 4.5):** mid-phase `rf-qa` invocation here is the **authorized third invocation point** alongside phase-gate and post-completion (documented in § 0 of this plan). | F-04, F-05 |
| 13 | CR-TASK-10 | (unchanged) side-effect file present on STRICT items with TFEP fire; seven-field schema; NO `## Failure Remediation` heading inserted into task file. | — |

### 5.4 M-sync — `make sync-dev` refresh + audits (P3)

| # | CR-ID | Acceptance digest (Phase 7 delta) | Phase 7 finding closures |
|---|---|---|---|
| 14 | CR-TASK-11 | (unchanged) `md5sum` matches; `make verify-sync` returns 0. | — |
| 15 | CR-FM-04 | (unchanged base) closed-enum single-source audit; INV-04 spot-check on N=5 TASK-* files. **Per F-02 closure (§ 4.2):** acceptance scope **extended** to include the two grep ordering checks: (a) `grep -n -E "(path_override_check\|tier_field_validate\|gate_1_dispatch)" [src]/skills/task/SKILL.md` returns the three names in that line order (Row 1 ordering check); (b) `grep -n -E "(forced_stance_read\|tier_field_read\|gate_2_dispatch)" [src]/skills/task/SKILL.md` returns the three names in that line order at the Phase-Gate QA Verification section (Row 10 ordering check). Any reorder blocks commit. | F-02 |
| 16 | CR-TASK-12 | (unchanged base) six `diff` invocations against verbatim donor blocks. **Per F-02 closure (§ 4.2):** scope **extended** to **seven** verbatim diffs — the original six donor-string diffs PLUS one additional diff that confirms the two CR-7 / CR-8 sentinel comment blocks (§ 4.2) are present byte-identical at the row 1 and row 10 insertion sites. Any non-zero diff blocks commit. | F-02 |

### 5.5 M4 — `/sc:task` Deprecation (P0/P1)

| # | CR-ID | Acceptance digest (Phase 7 delta) | Phase 7 finding closures |
|---|---|---|---|
| 17 | CR-DEP-01 | (unchanged) `/sc:task` emits single deprecation line and exits; `mcp-servers:` / `personas:` removed. | — |
| 18 | CR-DEP-02 | (unchanged) mirror md5 matches; `make verify-sync` returns 0. | — |
| 19 | CR-DIST-02 | (unchanged) `.claude/skills/sc-task-protocol/` absent after sync; `make verify-sync` returns 0 in the same commit. | — |
| 20 | CR-DEP-03 | (unchanged base) file absent; no `Skill sc:task-protocol` invocation remains; § 4 of `refactor-sctask-deprecation.md` absorption traceability holds. **Per F-07 closure (§ 4.7) — procedural authorization chain:** sprint goal → T06.03 task description → `refactor-sctask-deprecation.md` § 2 rubric + § 4 absorption traceability; structural precondition = CR-TASK-01..10 + CR-FM-01..03 land before this row (enforced by § 6 build order). | F-07 |
| 21 | CR-DEP-04 | (unchanged) both `src/` and `.claude/` directories absent; `make verify-sync` returns 0. | — |
| 22 | CR-DIST-01 | (unchanged) `uv run pytest tests/cli/test_install_skills.py` passes; `superclaude doctor` clean. | — |
| 23 | CR-DIST-04 | (unchanged) `make verify-sync` returns 0 post-prune; negative-test documented in commit message. | — |
| 24 | CR-DEP-05 | (unchanged) grep returns zero matches on `mcp-servers:` / `personas:` on both `[src]` and `[.claude]`. | — |

### 5.6 M5-A — Distribution: Plugin stub + README (P1/P3)

| # | CR-ID | Acceptance digest (Phase 7 delta) | Phase 7 finding closures |
|---|---|---|---|
| 25 | CR-DIST-03 | (unchanged) no `task-unified` / `deprecated_by`; body uses CR-DEP-01 redirect language; `category: deprecated`. | — |
| 26 | CR-DIST-05 | (unchanged) post-merge grep returns 0 matches; commit message records no-op. | — |
| 27 | CR-DIST-06 | (unchanged) § 4 audit table holds. | — |

### 5.7 M5-B — Active source reference redirects (P0/P1)

(All rows inherited unchanged. The critical sequencing constraints on CR-REF-01 + CR-REF-02 are explicit in § 6 below — S-2.)

| # | CR-ID | Acceptance digest | Phase 7 finding closures |
|---|---|---|---|
| 28 | CR-REF-01 | (unchanged) grep `/sc:task` returns 0 in file; tests align. | — |
| 29 | CR-REF-02 | (unchanged) grep returns 0; existing tests pass. | — |
| 30 | CR-REF-09 | (unchanged) `uv run pytest` passes three test files; three assertions per test. | — |
| 31 | CR-REF-04 | (unchanged) grep finds no `/sc:task` in non-`task.md` files. | — |
| 32 | CR-REF-05 | (unchanged) grep returns 0; replacement names declarative `Tier:`. | — |
| 33 | CR-REF-06 | (unchanged) grep returns no `/sc:task` in sibling protocol skill dirs. | — |
| 34 | CR-REF-07 | (unchanged) anchored regex returns 0; `/sc:tasklist` untouched. | — |
| 35 | CR-REF-08 | (unchanged) grep no `task-unified`; single-hop redirect to `/task`. | — |
| 36 | CR-REF-10 | (unchanged) grep returns 0 matches in PROJECT_INDEX.md. | — |
| 37 | CR-REF-11 | (unchanged) grep returns 0; script output sane. | — |
| 38 | CR-REF-12 | (unchanged) `make verify-sync` returns 0; grep finds no `/sc:task` mirror leakage. | — |
| 39 | CR-REF-03 | (unchanged) Phase 7 reviewer confirms `sc:tasklist`, not `/sc:task`. | — |
| 40 | CR-REF-13 | (unchanged) no manual edit. | — |

### 5.8 M5-C — Active backlog references (P1/P2)

| # | CR-ID | Acceptance digest | Phase 7 finding closures |
|---|---|---|---|
| 41 | CR-REF-14 | (unchanged) grep returns 0 matches. | — |
| 42 | CR-REF-15 | (unchanged) each file has deprecation header; bodies unchanged. | — |
| 43 | CR-REF-16 | (unchanged) each file annotated (or selectively redirected). | — |
| 44 | CR-REF-17 | (unchanged) header present. | — |
| 45 | CR-REF-18 (cluster, 14 sub-rows) | (unchanged) `DEPRECATION-NOTE.md` exists at cluster root; no body rewrites in 14 files. | — |

### 5.9 M5-D — Frozen / archived buckets (P3)

(Rows 46–53 inherited unchanged.)

### 5.10 M5-E — Hand-edited documentation redirects (P0/P1/P2)

(Rows 54–58 inherited unchanged; HZ-09 mitigation = atomic with CR-DEP-01 + CR-TASK-02 per § 6 Step 8.)

### 5.11 M5-F — Historical analyses / generated docs (P2/P3)

(Rows 59–65 inherited unchanged.)

### 5.12 M5-G — Audit closure (P3)

(Rows 66–67 inherited unchanged.)

---

## 6. Canonical commit sequence — with sequencing constraints S-1..S-3 locked

The 10-step canonical commit sequence from `merge-master.md` § 6 is inherited **unchanged in shape**. Three sequencing constraints (S-1..S-3) from `compat-hazard-report.md` are locked here as binding for Phase 7 execution.

### Sequencing constraint S-1 (from HZ-03) — in-flight PRD precondition

**Constraint:** TASK-PRD-20260514-121039 (in-flight, status `🟠 Doing` per session-context envelope; researches `/sc:task` + `sc-task-protocol` as PRIMARY ARTIFACTS) **MUST complete (status → `🟢 Done`) BEFORE Step 5 (CR-DEP-01 soft-deprecation lands).**

**Rationale:** The PRD's research subagents `[CODE-VERIFIED]`-tag the live donor surfaces. If CR-DEP-01 lands first, those subagents read the stub and the PRD's verification basis collapses. The PRD is explicitly authoring the pre-deprecation v3.75 snapshot; the deprecation lands afterward; the PRD becomes a frozen historical record.

**Mitigation:** option (a) — sequence completion first. Options (b) snapshot and (c) abort-restart from `compat-hazard-report.md` § 1 HZ-03 remain available if option (a) is infeasible; the choice is recorded at Phase 7 execution time and noted in the merge commit message.

### Sequencing constraint S-2 (from HZ-06 + HZ-07) — CLI runtime atomicity

**Constraint:** CR-REF-01 (`sprint/process.py:124+170`) and CR-REF-02 (`cleanup_audit/prompts.py:26/47/69/92/116`) **MUST land in the SAME COMMIT as CR-DEP-01** (or in any commit strictly before CR-DEP-01).

**Rationale:** The two CLIs emit `/sc:task ...` prompts at runtime. After CR-DEP-01 lands, the `/sc:task` invocation resolves to a 10-line redirect stub that exits; the sprint and cleanup_audit pipelines stop executing tasks. Same-commit landing prevents the runtime break.

**Enforcement:** the Step 5 commit MUST include CR-DEP-01 + CR-DEP-02 + CR-REF-01 + CR-REF-02 + CR-REF-09 + CR-DOC-01 (atomic per HZ-09 + CR-TASK-02-binding). The pre-commit gate is `uv run pytest tests/sprint/test_process.py && uv run pytest tests/sprint/test_tui_v2_wave2.py && uv run pytest tests/pipeline/test_process.py` returning 0.

### Sequencing constraint S-3 (from HZ-14) — Makefile sync-rule atomicity

**Constraint:** CR-DIST-02 (`Makefile` `sync-dev` orphan-prune loop) **MUST land atomically with CR-DEP-03 + CR-DEP-04** in the same commit.

**Rationale:** Hard-deleting `[src] src/superclaude/skills/sc-task-protocol/SKILL.md` + `__init__.py` without simultaneously pruning `[.claude] .claude/skills/sc-task-protocol/` breaks R-RULE-10 (verify-sync drift between `[src]` and `[.claude]`). The Makefile change must be in the same commit.

**Enforcement:** Step 6 commit MUST include CR-DEP-03 + CR-DEP-04 + CR-DIST-02. The pre-commit gate is `make verify-sync` returning 0 after the in-commit `make sync-dev`.

---

### Step 1 — M1 atomic-merge commit (P0)

**Rows:** CR-FM-01, CR-FM-02, CR-FM-03, CR-TASK-01, CR-TASK-02, CR-TASK-03, CR-TASK-04.

**Phase 7 row-deltas in this step:** CR-TASK-01 + CR-TASK-04 each include the sentinel comment block per F-02 (§ 4.2); CR-FM-02 / CR-TASK-03 acceptance criteria carry the F-01 read-only language.

**Pre-commit gate:** `uv run pytest` passes; `make verify-sync` returns 0 after in-commit `make sync-dev`.

### Step 2 — M2 commits (P1; rows can interleave)

**Rows:** CR-TASK-05, CR-TASK-06.

**Phase 7 row-deltas in this step:** CR-TASK-06 acceptance criterion gains AC-CR-TASK-06-F03 (§ 4.3) — dirty-tree warn-and-continue.

### Step 3 — M3 TFEP cluster (P2)

**Rows:** CR-TASK-07 → CR-TASK-08 → CR-TASK-09 → CR-TASK-10.

**Phase 7 row-deltas in this step:** CR-TASK-09 acceptance criterion gains AC-CR-TASK-09-F04 (§ 4.4) — baseline-absent over-escalate.

### Step 4 — M-sync + audits (P3)

**Rows:** CR-TASK-11 (`make sync-dev`), CR-FM-04 (closed-enum + INV-04 audit + **two new ordering greps** per § 4.2), CR-TASK-12 (**seven** verbatim diffs per § 4.2 — six donor strings + one sentinel-comment-block diff).

**Gate:** all three pass; CR-FM-04 ordering greps return the three function names in the expected line order; CR-TASK-12 seven diffs all return zero.

### Step 5 — M4-A commit: `/sc:task` soft-deprecation (P0, ME-9 audit included)

**Precondition (S-1):** TASK-PRD-20260514-121039 status `🟢 Done` recorded before this commit lands.

**Rows (atomic — S-2 binding):** CR-DEP-01, CR-DEP-02, CR-DEP-05 (audit included), **plus** CR-REF-01, CR-REF-02, CR-REF-09 (S-2 atomic CLI alignment), **plus** CR-DOC-01 (HZ-09 — user-guide must not describe `/task` as canonical before recipient skill carries it; same-commit binding).

**Pre-commit gate:** `uv run pytest tests/sprint/test_process.py tests/sprint/test_tui_v2_wave2.py tests/pipeline/test_process.py` returns 0; `make verify-sync` returns 0; commit message names ME-9 audit + S-1 precondition + S-2 atomicity.

### Step 6 — M4-B + M5-A coupled commit: hard-deprecation + sync-rule + plugin (P0/P1)

**Rows (atomic — S-3 binding):** CR-DEP-03 + CR-DEP-04 + **CR-DIST-02** (S-3 atomicity), plus CR-DIST-01 (installer regression test) + CR-DIST-04 (verify-sync audit), plus CR-REF-10 (PROJECT_INDEX.md — depends on CR-DEP-03/04).

**Phase 7 row-deltas in this step:** CR-DEP-03 row carries the procedural authorization chain annotation per F-07 (§ 4.7); commit message names the chain.

**CR-DIST-03 (plugin stub) + CR-REF-08** can land in this commit or the next.

**Pre-commit gate:** `make verify-sync` returns 0; installer regression test passes.

### Step 7 — M5-B remaining redirects + M5-C live backlog (P1/P2)

**Rows:** CR-REF-04, CR-REF-05, CR-REF-06, CR-REF-07, CR-REF-11, CR-REF-14, CR-REF-12 (sync-dev mirror refresh), CR-DIST-05 (README no-op audit), CR-DIST-06 (R-RULE-11 audit).

**R-RULE-10 gate:** `make verify-sync` returns 0.

### Step 8 — M5-E: doc redirects (P0/P1/P2)

**Atomic with Step 5 OR follow-on commit:** CR-DOC-01 (if not landed in Step 5), CR-DOC-02, CR-DOC-04, CR-DOC-05, CR-DOC-03.

**Doc-site build gate:** `mkdocs build` (or equivalent) returns 0 broken-link warnings.

### Step 9 — M5-C/M5-D/M5-F annotation pass (P2/P3)

**Rows:** CR-REF-15, CR-REF-16, CR-REF-17, CR-REF-18, CR-DOC-06, CR-DOC-07, CR-DOC-08, CR-DOC-09, CR-DOC-11 (v3.7-refactor + debates portion only), CR-REF-BUCKET-B optional note (HZ-16).

**Buckets NOT touched:** CR-REF-BUCKET-A, C, D, E, F, G, H (all `leave-as-is`; CR-REF-BUCKET-C gets the new-task guidance edit in `.dev/tasks/README.md`).

### Step 10 — Audit closure + regenerator-deferral note (P3)

**Rows:** CR-DOC-10, CR-DOC-11 (sprint-cli live portion `leave-as-is`), CR-DOC-12; commit message records "docs/generated/*: refresh deferred to next regenerator run".

**Final audit row:** CR-DOC-13 (R-RULE-11 audit over CR-DOC-01..12).

**Handoff confirmation:** CR-DEFER-T06.04 ack — § 5 coverage check in `refactor-documentation.md` confirms every CR-REF-DEFER-T06.04 file has a CR-DOC-NN row.

---

## 7. Phase 7 obligations carried forward (binding for any downstream implementation sprint)

1. **R-RULE-10 source-of-truth discipline.** Every `[src]` edit precedes its `[.claude]` mirror refresh; `make verify-sync` returns 0 before every commit.
2. **Commit-message auditability.** Every commit that touches a CR-DEP / CR-DIST / CR-DOC / CR-REF row cites the CR-ID(s) it implements.
3. **Atomic-merge obligations.** Steps 1, 5, 6 are hard atomic requirements (ME-6 + CR-7 + CR-9 + R-RULE-10 + S-2 + S-3).
4. **Verbatim donor blocks.** The seven `diff` invocations in CR-TASK-12 (six donor strings + one sentinel-comment-block per § 4.2) must return zero before any CR-TASK-01/-04/-08/-09/-10 commit lands.
5. **R-RULE-11 hard binding.** No CR-* row may silently re-litigate a `rejected-features-ledger.md` entry. If Phase 7 encounters a tempting "consistency" rewrite that re-introduces a REJECTed pattern, the execution stops and routes the question back to a new sprint.
6. **ME-1 audit gate (per F-01 closure).** Any future change that introduces a new per-item consumer of the `(Tier: …)` marker MUST be reviewed against ME-1 by R-RULE-11 — read-only tier-conditioned reads against pre-gated behaviors are authorized; per-item dispatch is auto-REJECT.
7. **INV-03 third invocation point (per F-05 closure).** The merged surface invokes `rf-qa` at three locations; any future surface widening beyond these three must be re-authorized via a fresh manifest exception.
8. **CR-7 / CR-8 ordering audit (per F-02 closure).** CR-FM-04 ordering greps and CR-TASK-12's sentinel-comment diff are blocking gates; reordering the three function calls at row 1 or row 10 fails the commit.
9. **Dirty-tree pre-flight (per F-03 closure).** STRICT pre-flight on a dirty `git status` tree warns and continues; refusing task entry is forbidden.
10. **Baseline-absent over-escalate (per F-04 closure).** When CR-TASK-09 finds `research/test-baseline.yaml` absent / empty / malformed on STRICT/STANDARD, classify all observed test failures as `classification=new`; never refuse, never silently skip.

---

## 8. Acceptance criteria recap (T07.04 #1–#4)

| T07.04 AC | Satisfied where |
|---|---|
| **AC #1** — `validation-report.md` exists with a pass/fail verdict per Phase 6 plan item and per manifest feature, each tied to its finding source | `validation-report.md` § 2 (67 / 67 PASS register), § 3 (TU / ME / donor-drop / ledger registers), § 5 (open-findings register), § 6 (hazard register). |
| **AC #2** — Every drifted feature is re-scored with the V/C/K rubric and the re-score is documented (R-RULE-07) | `validation-report.md` § 4: **zero drift across 8 TUs** (T07.01 § 3.5 + T07.03 § 4 concur); no re-score required; V/C/K verdicts (TU-1..TU-8) carry forward unchanged from `transfer-manifest.md` § 4 into this plan's § 2.1. |
| **AC #3** — `final-merge-plan.md` exists with all Phase 7 corrections applied and zero open findings | This file. § 4 closes F-01..F-08; § 6 locks S-1..S-3; § 5 carries the 67 row-line-items with the four Phase-7-row-deltas applied (CR-TASK-06, CR-TASK-09, CR-FM-04, CR-TASK-12). **Zero open findings remain.** |
| **AC #4** — No `rejected-features-ledger.md` entry is re-introduced; any verdict change carries a re-debate note (R-RULE-11) | `validation-report.md` § 3.4: 26 / 26 ledger entries TERMINAL across this plan's § 5; § 4: zero verdict-changing re-scores; no re-debate note triggered. R-RULE-11 audit clause at the head of § 5 above re-states the binding for downstream sprints. |

---

## 9. Validation hooks (T07.04 Validation block)

**Sub-agent verification (T07.04 Validation #1):** an independent agent confirms zero open findings + every correction traces to a Phase 7 artifact by:

1. Grepping § 4 for each F-01..F-08 disposition and confirming the cited source artifact (e.g., `plan-adversarial-review.md` § 4.2 Q1 for F-05) exists.
2. Grepping § 6 for each S-1..S-3 sequencing constraint and confirming the cited hazard (e.g., `compat-hazard-report.md` HZ-06 + HZ-07 for S-2) exists.
3. Confirming § 5 carries the same 67 row-line-items as `merge-master.md` § 1 (no row added, no row removed; only the four named row-deltas in § 5.1 / § 5.2 / § 5.3 / § 5.4 reflect Phase 7 corrections).
4. Confirming § 2.1 reports the same 8 TU forward-map as `merge-master.md` § 3.1 with V/C/K verdicts carried forward unchanged from `transfer-manifest.md` § 4.

**Manual reviewer check (T07.04 Validation #2):** the reviewer recomputes a sample of the no-drift V/C/K assessments by:

1. Picking 3 TUs (e.g., TU-1, TU-3, TU-7).
2. Reading the corresponding `transfer-manifest.md` § 2 "Shape of change" sketch.
3. Reading the corresponding Phase 6 row(s) in this plan's § 5.
4. Confirming file path, extension-point row touched, change type, and effort envelope match — and that V (validation evidence weight), C (complexity), K (knowledge basis) each remain at their Phase 5 scores.

---

## 10. Deliverable handoff

`final-merge-plan.md` is the **binding execution plan** for any downstream implementation sprint. It supersedes `merge-master.md` (T06.05) for any row whose acceptance criteria were augmented in § 4 (CR-TASK-06, CR-TASK-09, CR-FM-04, CR-TASK-12, CR-TASK-01 sentinel, CR-TASK-04 sentinel, CR-FM-02 / CR-TASK-03 read-only language, CR-DEP-03 procedural authorization annotation). For every other row, `merge-master.md` and the originating refactor file carry forward unchanged.

**Phase 7 closure facts (independently audited by `validation-report.md`):**

- **67 / 67 Phase 6 plan items PASS** (7 PASS WITH NOTE all closed in § 4).
- **8 / 8 manifest TUs PASS, 0 / 8 drifted, 0 / 8 V/C/K re-scores required.**
- **9 / 9 manifest exceptions HELD.**
- **10 / 10 donor-ceremony drops NOT REVIVED.**
- **26 / 26 ledger entries TERMINAL** (R-RULE-11 holds).
- **INV-01..INV-05 SURVIVE** (demonstrated, not asserted).
- **18 / 18 compat hazards MITIGATED** (3 sequencing constraints S-1..S-3 locked into § 6).
- **0 HIGH-severity findings; 8 / 8 open findings F-01..F-08 CLOSED in § 4.**

**T07.04 deliverable: COMPLETE.** Phase 7 advances with a fully validated, fully traced, fully invariant-safe merge plan. The plan's structural shape (67 rows, 10 commit steps, acyclic dependency graph, two-way TU traceability, zero ledger re-proposals) is identical to `merge-master.md`; the four Phase 7 row-deltas tighten silent behaviors that the adversarial review surfaced. **Zero open findings remain. The plan is binding.**

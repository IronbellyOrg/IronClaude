# D-0092 — OPS-001 K-003 Audit-Target Runbook

**Task:** T07.11 (Phase 7 — M7)
**Roadmap items:** R-152
**Date:** 2026-05-18
**Branch:** `feat/hook-sync-and-matcher-fix`
**Tier:** STANDARD
**Verification method:** Direct enumeration check (5 runbook sections + SLA + gauge + MET-003 cross-reference)
**Audience:** QA Lead (on-call), task-builder maintainers (on-call rotation), GA-tagging committee
**Owner:** QA Lead
**Response SLA:** **4 business hours** from event detection to acknowledgement + diagnosis
**Self-Audit-coverage gauge target:** **100%** on the first 5 rf-qa-qualitative runs post-FR-CONV.3 landing
**Overall: PASS** (4/4 acceptance criteria met — §6)

---

## 0. TL;DR

OPS-001 is the operational runbook that turns the K-003 risk and the
INV-019 Self-Audit obligation into an on-call response procedure. It
covers a single, observable event:

> **An rf-qa-qualitative run within the K-003 audit window
> (first 5 runs post-FR-CONV.3) either lacks a `## Self-Audit` section,
> or lists zero independent semantic checks (INV-019 category-(b) = 0),
> or lists only bullets that repeat the inherited structural verdict.**

The runbook is owned by the **QA Lead** with a **4-business-hour
response SLA** from event detection to acknowledgement + diagnosis.
The Self-Audit-coverage gauge target is **100%** on the first 5 runs
(measured by MET-003). The runbook contains the five mandatory sections
(symptoms / diagnosis / resolution / escalation / prevention) called
out in roadmap.md:431 and phase-7-tasklist.md L518-528.

---

## 1. Scope and authoritative bindings

This runbook binds to the following authorities (all read at landing
time; cross-checked at every invocation):

| Source | Location | Binding |
|---|---|---|
| Roadmap R-152 acceptance criteria | `roadmap.md:431` | "runbook:published; Self-Audit-coverage-gauge:target-100%-first-5-runs-documented; QA-Lead-4-business-hour-response-SLA" |
| Roadmap §M7 Consolidated Governance Table — OPS-001 row | `roadmap.md:464` | "OPS-001 \| K-003 audit runbook \| Operational \| QA Lead \| 4 business hours response SLA \| FR-CONV.3" |
| Release-spec §8.3 row 4 (audit-after-FR-CONV.3-lands) | `release-spec.md:480` | "All 5 Self-Audits show ≥1 semantic check beyond inherited PASS; no inflation detected; if any audit shows inflation, fail K-003 gate and disable FR-CONV.3" |
| INV-019 Self-Audit consumer obligation | `roadmap.md:217` + `.claude/agents/rf-qa-qualitative.md:850-894` | "rf-qa-qualitative output MUST list every rf-qa PASS item it relied on AND ≥1 semantic check where rf-qa PASS is insufficient" |
| Anti-inflation rule (byte-stable invariant) | `.claude/agents/rf-qa-qualitative.md:766-775` | The Prohibited Behaviors block — never modified by FR-CONV.3 (byte-equality verified at MIG-003 by quality-engineer sub-agent — `D-0039/evidence.md §4`) |
| K-003 risk row | `release-spec.md:425` + `roadmap.md:255` | R-M3-1 — PR-04 passthrough causes inflation despite anti-inflation rule |
| FF_INHERITED_STRUCTURAL_VERDICT flag (governance + rollback) | `D-0039/spec.md §2-§3` | Flag governance + per-line rollback path on audit FAIL |
| MET-003 Self-Audit Coverage metric | `roadmap.md:440` + `D-0098/spec.md` (T07.19) | "window:first-5-runs; target:100%; semantic-checks:≥1-each; failure:block-release" |
| First-5-runs audit report (T07.01 output) | `D-0083/spec.md` | Per-run Self-Audit + semantic-check evidence; references this runbook in §5 |

**Scope boundary.** OPS-001 covers Self-Audit / semantic-check events
**within the K-003 audit window** (first 5 rf-qa-qualitative runs after
FR-CONV.3 lands at commit `ad083b6`). Post-window observations are
handled by ongoing MET-003 inspection (release-spec §8.3 audit-row
cadence). OPS-001 does **not** cover synthetic-dnsp emissions
(→ OPS-002), all-partitions exhaust (→ OPS-003), HALT-MONOTONICITY
rate (→ OPS-004), regression-halt rate (→ OPS-005), `make verify-sync`
failure (→ OPS-006), or layout-change blast radius (→ OPS-007).

---

## 2. Runbook — 5 sections

### 2.1 Symptoms

The on-call QA Lead is paged or alerted when **any one** of the
following is observed in an rf-qa-qualitative run that falls inside
the K-003 audit window:

1. **Missing Self-Audit section.** A grep for the section heading
   (verbatim `## Self-Audit` from `.claude/agents/rf-qa-qualitative.md:850-894`,
   or the operationally-equivalent post-FR-CONV.3 heading
   `## Inherited Structural Verdict — Reliance Audit (PR-04, INV-019)`)
   returns **zero matches** in the run output.
2. **Zero independent semantic checks.** The Self-Audit section is
   present but its category-(b) "independent semantic checks" list is
   empty (count = 0).
3. **Inflated reliance.** The Self-Audit section is present and
   non-empty, but every category-(b) bullet merely **repeats** the
   inherited rf-qa structural verdict rather than performing a
   distinct semantic check (e.g. quotes an A.10 PASS line verbatim
   with no Read / Grep / Bash tool-evidence binding of its own).
4. **MET-003 counter trips.** Offline-grep aggregation (D-0098 / T07.19)
   reports Self-Audit-coverage **<100%** or independent-semantic-check
   count **<1** for any run in the first-5 cohort.

Each of the four symptoms maps to a single audit-FAIL condition under
INV-019 + K-003. Detection sources include: T07.01 audit pass
(`D-0083/spec.md §2.1 / §3.1-§3.3`), MET-003 dashboard, manual
inspection by QA Lead.

### 2.2 Diagnosis

Within **4 business hours** of paging, the QA Lead performs the
following ordered diagnostic steps:

1. **Identify run identity.** Capture (a) BUILD_REQUEST id, (b)
   rf-qa-qualitative output absolute path, (c) sha256 of the output
   file, (d) whether the run is first-cycle or fix-cycle, (e) the
   audit-window slot number (1..5).
2. **Confirm symptom class.** Run the symptom-class triage:
   - `grep -c -E '^## (Self-Audit|Inherited Structural Verdict — Reliance Audit)' <output-path>`
     → if `0`, symptom = MISSING (§2.1.1).
   - If `≥1`, extract the section body and count category-(b) bullets
     → if `0`, symptom = ZERO-CHECKS (§2.1.2).
   - If `≥1`, inspect each bullet for a distinct semantic check (Read
     / Grep / Bash tool-evidence binding **NOT** present in the
     inherited verdict) → if every bullet is a verdict-repeat, symptom
     = INFLATED-RELIANCE (§2.1.3).
   - Cross-check the MET-003 dashboard for window-level numbers
     (symptom MET-COUNTER-TRIP, §2.1.4).
3. **Bind to anti-inflation rule.** Confirm the anti-inflation rule at
   `rf-qa-qualitative.md:766-775` is still byte-identical to the
   MIG-003 baseline (`D-0039/evidence.md §4`). If it has drifted, the
   symptom is upgraded to anti-inflation-rule violation
   (release-spec §19.4 rollback path is auto-armed; escalate per §2.4
   immediately).
4. **Bind to FF_INHERITED_STRUCTURAL_VERDICT state.** Read
   `D-0039/spec.md §2` — confirm the flag is ON and the activation
   commit is reachable from the failing run. If the flag is OFF, the
   symptom is **NOT an OPS-001 event** (the run is operating in
   standalone fallback mode per Critical Rule #11 branch-3); close the
   page and route to standalone-rf-qa-qualitative review.
5. **Categorise root cause.** Distinguish:
   - **R1** — prompt-template regression (spawn-prompt no longer
     emits Self-Audit obligation).
   - **R2** — consumer-side schema regression (rf-qa-qualitative no
     longer reads or honours INV-019).
   - **R3** — fix-cycle freshness regression (Self-Audit was emitted
     at first cycle but stripped on re-injection — INV-002 violation).
   - **R4** — empirical inflation (consumer treats rf-qa PASS as
     verification; INV-019 anti-inflation operating as intended,
     audit-FAIL is the correct outcome and rollback is required).

### 2.3 Resolution

Resolution path depends on the root-cause category from §2.2.5. Each
resolution is bounded to a **single audit-window slot**; if multiple
slots show symptoms, treat each independently.

| Root cause | Resolution | Owner | Budget |
|---|---|---|---|
| **R1** (prompt-template regression) | Re-run `make sync-dev`; diff `src/superclaude/skills/SKILL.md` §A.10.5 against the MIG-003 baseline; restore the verdict-injection directive; re-trigger the affected BUILD_REQUEST so a fresh rf-qa-qualitative run can populate the audit-window slot. | task-builder maintainer (with QA Lead approval) | Within the 4-business-hour SLA window |
| **R2** (consumer-side schema regression) | Diff `.claude/agents/rf-qa-qualitative.md:850-894` (Self-Audit Schema Requirement) and `:766-775` (anti-inflation Prohibited Behaviors block) against the MIG-003 baseline; restore the additive trailing sections per `D-0039/spec.md §3 step 5`; re-trigger the affected BUILD_REQUEST. | rf-qa-qualitative maintainer (with QA Lead approval) | Within the 4-business-hour SLA window |
| **R3** (fix-cycle freshness regression — INV-002) | Inspect the orchestrator's `**Fix-cycle re-entry (INV-002 freshness — stale-verdict rejection):**` block in SKILL.md §A.10.5; restore steps 1–7 per `D-0039/spec.md §3 step 2`; re-trigger the fix-cycle. | task-builder maintainer | Within the 4-business-hour SLA window |
| **R4** (empirical inflation — audit-FAIL is correct) | Do **NOT** attempt to fix in-place. **Escalate** per §2.4 (release-spec §19.4 rollback path: disable FF_INHERITED_STRUCTURAL_VERDICT; consumer falls back to standalone structural re-checking; per-line revert per `D-0039/spec.md §3 steps 1–5`). | QA Lead → Engineering Lead → GA-tagging committee | 4-business-hour SLA covers escalation initiation, not full rollback execution |

On any successful resolution (R1 / R2 / R3): the QA Lead amends
`D-0083/spec.md §3` with the new captured run's Self-Audit + semantic-
check evidence, re-applies the C1/C2 evaluation, and re-issues sign-off
per `D-0083/spec.md §4.3` (interim or final, depending on slot count).

### 2.4 Escalation

Escalation is **time-boxed by the 4-business-hour SLA**:

1. **T+0 (event detected).** Page the QA Lead (on-call rotation —
   wired to task-builder maintainers on-call knowledge base per
   `roadmap.md:477`). The QA Lead acknowledges within 1 business hour.
2. **T+1h to T+4h (diagnosis window).** QA Lead executes §2.2.
3. **T+4h (SLA boundary).** QA Lead reports diagnosis and root cause
   (R1..R4) to the Engineering Lead.
4. **R1 / R2 / R3 path** — Engineering Lead acknowledges; resolution
   proceeds per §2.3 with no further escalation unless the resolution
   itself fails or recurs in the same audit-window slot.
5. **R4 path (empirical inflation)** — Engineering Lead immediately
   escalates to the **GA-tagging committee**. The committee invokes
   the release-spec §19.4 rollback path (disable
   FF_INHERITED_STRUCTURAL_VERDICT, per-line revert per
   `D-0039/spec.md §3`). K-003 audit is marked FAIL; the v3.9 GA tag
   (T07.20 / MIG-007b) is **blocked** until either (a) the rollback
   stabilises the audit on a re-launched 5-run window, or (b) the
   committee approves an alternative remediation.
6. **Recurrence escalation.** Two or more OPS-001 events on the same
   FR-CONV.3 audit-window cohort → automatic escalation to the
   GA-tagging committee regardless of root cause, on the basis that
   the audit-target itself is degraded.

Escalation contacts and rotation handoffs live in the on-call
knowledge base (consumed via integration point at `roadmap.md:477`);
this runbook intentionally does not enumerate names so it survives
rotation changes.

### 2.5 Prevention

Prevention is enforced by three layered controls, all of which exist
at landing time and persist through GA:

1. **Schema-level control (INV-019).** The Self-Audit section is a
   mandatory output schema element for rf-qa-qualitative
   (`.claude/agents/rf-qa-qualitative.md:850-894`). The producer-side
   spawn prompt re-injects the obligation on every cycle (INV-002
   freshness — `SKILL.md §A.10.5` `**Fix-cycle re-entry**` block).
2. **Anti-inflation invariant (byte-stable).** The Prohibited
   Behaviors block at `rf-qa-qualitative.md:766-775` is treated as
   absolute (`roadmap.md:29`). MIG-003 confirmed byte-equality pre/post
   (`D-0039/evidence.md §4`); any drift is itself an audit event
   (§2.2.3 upgrade path).
3. **Instrumentation (MET-003).** Offline-grep aggregation
   (D-0098 / T07.19) reports Self-Audit-coverage + independent-
   semantic-check counts per run. Sub-threshold values **block
   release** per `roadmap.md:440` ("failure:block-release") — i.e.
   prevention is enforced at the GA gate, not only at on-call paging.

Secondary preventive measures:

- **Pre-merge gate.** Every PR that touches `SKILL.md §A.10.5` or
  `rf-qa-qualitative.md:766-775` / `:850-894` MUST run `make
  verify-sync` (A-001) and include a byte-diff confirmation against
  the MIG-003 baseline (`D-0039/evidence.md §4`).
- **Audit cadence.** T07.01 (`D-0083/spec.md`) keeps the 5-slot
  inventory open until all 5 runs are captured. The QA Lead amends
  the audit report in-place rather than starting a new artifact, so
  the slot-fill cadence is observable.
- **Post-window inspection.** Beyond the first-5 cohort, release-spec
  §8.3 audit rows continue to inspect Self-Audit coverage on a
  per-release basis (MET-003 stays live indefinitely; not retired
  with the FF_INHERITED_STRUCTURAL_VERDICT flag).

---

## 3. Self-Audit-coverage gauge

| Field | Value |
|---|---|
| Gauge name | Self-Audit Coverage (MET-003) |
| Audit window | First 5 rf-qa-qualitative runs after FR-CONV.3 lands (commit `ad083b6`, 2026-05-17 21:14:04 UTC) |
| Target | **100%** (5 of 5 runs carry `## Self-Audit` section with ≥1 independent semantic check) |
| Threshold | <100% on any run within the window → OPS-001 page; release blocked |
| Measurement | Offline-grep aggregation across QA reports (D-0098 / T07.19) — counts `## Self-Audit` heading presence + category-(b) bullet count per run |
| Owner | QA Lead |
| Source authority | `roadmap.md:440` (MET-003 row); `roadmap.md:464` (OPS-001 row, "gauge target 100% Self-Audit coverage on first 5 runs"); `D-0091/spec.md §2` (MET-003 line) |
| Reporting cadence | Continuous within the audit window; weekly inspection thereafter via release-spec §8.3 audit-row cadence |
| Current reading (as of 2026-05-18 13:08 UTC) | 3 of 5 captured at 100% coverage; 2 PENDING per `D-0083/spec.md §2.2`. Trajectory: FINAL-PASS-likely. |

The gauge target is **explicitly documented at 100% on the first 5
runs** to satisfy phase-7-tasklist.md L526
("Self-Audit-coverage gauge target documented at 100% first-5-runs").

---

## 4. Response SLA

| Field | Value |
|---|---|
| Response time | **4 business hours** from event detection to acknowledgement + diagnosis |
| Owner | QA Lead (on-call rotation) |
| Source authority | `roadmap.md:431` (R-152 acceptance criteria — "QA-Lead-4-business-hour-response-SLA"); `roadmap.md:464` (OPS-001 row, "4 business hours response SLA"); `D-0091/spec.md §2` (OPS-001 line) |
| Business-hour window | The owning organisation's standard business hours apply (typically Mon-Fri, local time of the QA Lead rotation). Out-of-hours events accumulate detection latency but the SLA clock starts at the next business-hour boundary; this is the same convention used by OPS-002 (24h), OPS-005 (Engineering-Lead escalation), and OPS-007 (Engineering-Lead escalation). |
| Clock-start trigger | First of: (a) MET-003 counter trip, (b) manual QA Lead inspection during T07.01 audit pass, (c) page from the on-call rotation. |
| SLA covers | Acknowledgement + diagnosis + root-cause categorisation (§2.2.5). |
| SLA does NOT cover | Full rollback execution under R4 (release-spec §19.4 path is a separate, multi-step, committee-gated operation; the 4-hour SLA only requires that the rollback be **initiated** by the SLA boundary). |

The SLA is **explicitly stated** to satisfy phase-7-tasklist.md L527
("QA-Lead 4-business-hour response SLA explicitly stated").

---

## 5. Cross-references

| Linkage | Target | Role |
|---|---|---|
| **MET-003 Self-Audit Coverage metric** | `D-0098/spec.md` (T07.19, R-161); `roadmap.md:440`; `D-0091/spec.md §2` MET-003 row | Continuous instrumentation that triggers this runbook |
| K-003 first-5-runs audit report | `D-0083/spec.md` (T07.01, R-140) | Audit artifact whose §5 cross-references back into this runbook |
| FF_INHERITED_STRUCTURAL_VERDICT flag governance | `D-0039/spec.md §2-§3` (T03.16) | Flag activation + per-line rollback path used by §2.3 R4 / §2.4 step 5 |
| Anti-inflation rule (byte-stable) | `.claude/agents/rf-qa-qualitative.md:766-775` | Invariant whose drift upgrades any OPS-001 event to immediate escalation (§2.2.3) |
| INV-019 acceptance criterion | `roadmap.md:217` + `.claude/agents/rf-qa-qualitative.md:850-894` | Definition of the Self-Audit obligation this runbook enforces |
| K-003 risk row | `release-spec.md:425`; `roadmap.md:255` (R-M3-1) | Originating risk this runbook mitigates |
| FR-CONV.3 rollback path | `release-spec.md §19.4`; `D-0039/spec.md §3` | Path invoked under §2.3 R4 / §2.4 step 5 |
| Consolidated GA-Readiness Governance Table | `D-0091/spec.md §2` (OPS-001 row) | This runbook is OPS-001 in that table |
| GA-tagging gate (MIG-007b) | `D-0099/spec.md` (T07.20, R-165) | Hard pre-requisite — all 7 OPS runbooks must be live for GA tag |
| Integration point — on-call knowledge base | `roadmap.md:477` (M7 Integration Points row 2) | Where this runbook is consumed by task-builder maintainers on-call rotation |
| OPS-001..007 peer runbooks | OPS-002 D-0093, OPS-003 D-0094, OPS-004 D-0095, OPS-005 D-0096, OPS-006 + OPS-007 D-0097 | Companion runbooks; OPS-001 covers FR-CONV.3 specifically |

**MET-003 cross-reference is explicitly included** in §3, §4, and the
table above to satisfy phase-7-tasklist.md L528
("Cross-reference to MET-003 metric included").

---

## 6. Acceptance criteria — T07.11

| # | Criterion (phase-7-tasklist.md L524-528) | Status | Evidence |
|---|---|---|---|
| 1 | File `TASKLIST_ROOT/artifacts/D-0092/spec.md` exists and includes 5 runbook sections. | **PASS** | This file at `.dev/releases/current/task-builder-merge/artifacts/D-0092/spec.md`; §2.1 Symptoms, §2.2 Diagnosis, §2.3 Resolution, §2.4 Escalation, §2.5 Prevention. |
| 2 | Self-Audit-coverage gauge target documented at 100% first-5-runs. | **PASS** | §3 (Gauge name, target = 100%, window = first 5 runs); also §1 frontmatter "Self-Audit-coverage gauge target". |
| 3 | QA-Lead 4-business-hour response SLA explicitly stated. | **PASS** | §4 (Response time = 4 business hours, Owner = QA Lead); also §1 frontmatter "Response SLA". |
| 4 | Cross-reference to MET-003 metric included. | **PASS** | §3 (Gauge measurement → MET-003 / D-0098); §4 (clock-start trigger references MET-003 counter trip); §5 first row (MET-003 linkage). |

**Verdict: PASS** — OPS-001 K-003 audit-target runbook is published,
5-section structured, gauge-target-explicit, SLA-explicit, and
MET-003-cross-referenced. Ready for QA Lead review and for consumption
by the GA-tagging committee at T07.20 (MIG-007b).

---

## 7. Provenance

- **Dependency:** T07.01 (`D-0083/spec.md`) — K-003 first-5-runs audit
  report, currently INTERIM-PASS on 3 of 5 captured runs; this runbook
  governs the slot-fill cadence and any audit-FAIL response on the
  remaining 2 slots.
- **Downstream consumers:** T07.12 mid-phase checkpoint
  (`CP-P07-T07-T11.md`); T07.20 GA-tag (MIG-007b) — hard pre-requisite
  (all 7 OPS runbooks live).
- **Audit-window anchor commit:** `ad083b6a84edfe07388012a64d69993694e8bf44` (MIG-003
  — FR-CONV.3 + INV-019 + Self-Audit landed) — 2026-05-17 21:14:04 UTC.
- **Reporting cut-off:** 2026-05-18 13:08 UTC (current session
  timestamp from session-context envelope).
- **Release branch:** `feat/hook-sync-and-matcher-fix`.
- **MCP usage:** Sequential (preferred) — applied for runbook authoring
  (multi-step reasoning across §2.1-§2.5 + cross-reference closure).

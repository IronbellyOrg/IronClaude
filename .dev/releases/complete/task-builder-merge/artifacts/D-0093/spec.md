# D-0093 — OPS-002 DNSP Triage Runbook

**Task:** T07.13 (Phase 7 — M7)
**Roadmap items:** R-153
**Date:** 2026-05-18
**Branch:** `feat/hook-sync-and-matcher-fix`
**Tier:** STANDARD
**Verification method:** Direct enumeration check (5 runbook sections + 24-hour SLA + weekly cadence + ≥3 dedup-keys/week escalation threshold)
**Audience:** rf-qa maintainer (on-call), task-builder maintainers (on-call rotation), Engineering Lead, GA-tagging committee
**Owner:** rf-qa maintainer
**Response SLA:** **24 hours** from MET-005 emission-count trip to acknowledgement + diagnosis
**Inspection cadence:** **Weekly** offline-grep aggregation of synthetic-dnsp emissions per release window
**Escalation threshold:** **≥3 distinct `dedup_key` values within a single 7-day window** → escalate to Engineering Lead
**Overall: PASS** (4/4 acceptance criteria met — §6)

---

## 0. TL;DR

OPS-002 is the operational runbook that turns the K-006 risk
("synthetic-dnsp findings mask real issues") and the FR-CONV.6 emission
contract (DM-003 7-field schema, R-122 path B "≥1-success AND ≥1-exhaust
→ synthetic-dnsp emits alongside real findings") into an on-call
response procedure. It covers a single, observable event:

> **A production rf-qa / rf-qa-qualitative run merges one or more
> partition-cohort outputs containing a `source: "synthetic-dnsp"` block
> (MET-005 emission count >0), OR the weekly aggregation reveals ≥3
> distinct `dedup_key` values within a 7-day window.**

The runbook is owned by the **rf-qa maintainer** with a **24-hour
response SLA** from MET-005 trip to acknowledgement + diagnosis. The
weekly inspection cadence is enforced by offline-grep aggregation
across QA reports (D-0098 / T07.19). The escalation threshold — ≥3
distinct `dedup_key` values within a single 7-day window — routes to
the Engineering Lead, where it composes with the false-positive
ceiling (NFR threshold: synthetic-dnsp false-positive rate <1%,
roadmap.md:581).

The runbook contains the five mandatory sections (symptoms / diagnosis
/ resolution / escalation / prevention) called out in roadmap.md:432
and phase-7-tasklist.md L615-625.

---

## 1. Scope and authoritative bindings

This runbook binds to the following authorities (all read at landing
time; cross-checked at every invocation):

| Source | Location | Binding |
|---|---|---|
| Roadmap R-153 acceptance criteria | `roadmap.md:432` | "runbook:published; 24-hour-response-SLA; weekly-inspection-cadence" |
| Roadmap §M7 Consolidated Governance Table — OPS-002 row | `roadmap.md:465` | "OPS-002 \| DNSP triage runbook \| Operational \| rf-qa maintainer \| 24 hours response SLA; escalate ≥3 distinct/week \| FR-CONV.6" |
| Roadmap MET-005 row (DNSP Emission) | `roadmap.md:462` | ">0 in production → OPS-002 review" |
| Roadmap MET-004 row (Halt Rate combined) | `roadmap.md:441` | "synthetic-dnsp:>0-triggers-OPS-002; ... offline-grep-aggregate-per-release" |
| K-006 risk row (synthetic-dnsp findings mask real issues) | `release-spec.md:428` + `roadmap.md:561` (R-011) | "HIGH severity ensures gate-level visibility; all-agents-fail guard preserves existing escalation path; dedup-key prevents over-emission while preserving the failure signal" |
| DM-003 7-field emission schema | `roadmap.md:109` + `roadmap.md:363` + `src/superclaude/agents/rf-qa.md:78` (PR-03 paragraph) | "severity:HIGH-fixed; source:synthetic-dnsp-fixed; affected_range; evidence:spawn-log-path-or-stub; recommendation:Manual-review-required-fixed; dedup_key:2-tuple-range-exhaust_point; found_n_times:int-default-1" |
| dedup_key 2-tuple shape | `src/superclaude/agents/rf-qa.md:78` ("`dedup_key: ["<assigned_files_range>", "<escalation_ladder_exhaust_point>"]`") | 2-element YAML list; `escalation_ladder_exhaust_point` ∈ closed vocabulary `{retry-1, retry-2, gap-fill-round-1, gap-fill-round-2, gap-fill-round-3}` |
| R-122 all-agents-fail guard precedence (3 mutually-exclusive paths) | `src/superclaude/skills/task-builder/SKILL.md` §A.8 (line 682) | "Path A zero-success → `rf-team-lead.md:417`; Path B ≥1-success AND ≥1-exhaust → synthetic-dnsp emits alongside; Path C all-succeeded → no synthetic" |
| INV-012 cross-cycle composition with PR-02 monotonicity | `src/superclaude/skills/task-builder/SKILL.md` L1079-1093 + L1066 | "Cross-cycle identical dedup_key contributes 1 (not 2) to `|F_{n+1}|`; persistence trips Step-2 monotonicity, NOT Step-1 regression" |
| rf-team-lead.md:417 byte-stable invariant | sha256 `51725c0ffa151c3403701f21910d7f5cf122639f3a0e7fa9ae3cafe82701a0a0` (whole-file `874a516e3baedd8fed5b433592ab3d41a78bd8ec8601098d8610f47ce255e40b`) | Pre-PR-03 contract preserved across MIG-006; touched by `R-122-guard-precedence-violation` audit |
| NFR threshold — synthetic-dnsp false-positive rate | `roadmap.md:581` | "<1% across post-merge measurement window" — composed at the §2.4 escalation gate |
| MIG-006 landing commit | `87c8254 feat(task-builder): MIG-006 land FR-CONV.6 Synthetic-DNSP on Partition Exhaust (M6)` | Anchor commit for production emission start |
| OPS-003 peer runbook (mutual-exclusivity check) | `D-0094/spec.md` (T07.14, R-154) | OPS-002 ↔ OPS-003 path-selection complement (Path B vs Path A) |

**Scope boundary.** OPS-002 covers **emissions in Path B (≥1-success
AND ≥1-exhaust)** of the R-122 three-path table — i.e., a production
run where at least one partition exhausted its escalation ladder AND at
least one sibling succeeded, so synthetic-dnsp emits alongside real
findings. The Path A (zero-success) all-agents-fail case is handled by
OPS-003 (D-0094) and routes to `rf-team-lead.md:417` instead of
emitting synthetic-dnsp. The Path C (all-succeeded) case is a non-event
(MET-005 reads 0). OPS-002 does **not** cover Self-Audit / semantic-
check audit-target events (→ OPS-001), HALT-MONOTONICITY rate (→
OPS-004), regression-halt rate (→ OPS-005), `make verify-sync` failure
(→ OPS-006), or INV-018 layout-change blast radius (→ OPS-007).

---

## 2. Runbook — 5 sections

### 2.1 Symptoms

The on-call rf-qa maintainer is paged or alerted when **any one** of
the following is observed in production rf-qa / rf-qa-qualitative
output post-MIG-006 (anchor commit `87c8254`, 2026-05-18 — FR-CONV.6
landed):

1. **Single MET-005 emission trip.** Offline-grep aggregation (D-0098 /
   T07.19) reports MET-005 synthetic-dnsp emission count **>0** for
   any production run within the current release window
   (`grep -c '^source: synthetic-dnsp$'` or the structured-block
   equivalent across QA reports; `roadmap.md:575` — "≥1 on twice-
   exhaust fixture; 0 on healthy runs").
2. **Multi-emission within cycle.** A single retry cycle emits two or
   more synthetic-dnsp blocks with **distinct `dedup_key` values**
   (within-cycle collapse R-123 only collides identical dedup_keys;
   distinct keys remain separate findings).
3. **Cross-cycle persistence.** The same `dedup_key` 2-tuple
   (`(assigned_files_range, escalation_ladder_exhaust_point)`) re-appears
   on consecutive cycles `n` and `n+1` (INV-012 dedup case — NOT a
   regression). Persistence is itself benign; the symptom is that the
   underlying partition agent is **stuck** at the same exhaust point.
4. **Weekly threshold trip (escalation trigger).** Weekly offline-grep
   aggregation reports **≥3 distinct `dedup_key` values** within any
   rolling 7-day window. This is the §2.4 hard escalation trigger.
5. **False-positive suspicion.** A reviewer inspecting the partition's
   spawn-log (`${TASK_DIR}qa/spawn-log-<agent_role>-<partition_id>.txt`,
   referenced by the synthetic finding's `evidence:` field) finds the
   partition agent **did not actually exhaust** — i.e., the emission
   was triggered by a wire-shape misclassification rather than a true
   ladder exhaust. This composes with the NFR <1% false-positive
   ceiling (`roadmap.md:581`).

Each of the five symptoms maps to a known triage class under K-006 +
FR-CONV.6. Detection sources include: MET-005 dashboard
(`roadmap.md:462`, `D-0091/spec.md §2`), MET-004 combined halt-rate
dashboard (`roadmap.md:441`), weekly offline-grep aggregation
(`roadmap.md:575`), manual inspection by rf-qa maintainer, and TEST-022
fixture re-runs (`roadmap.md:326` — cross-cycle dedup non-regression
fixture).

### 2.2 Diagnosis

Within **24 hours** of MET-005 trip (or weekly-aggregation page), the
rf-qa maintainer performs the following ordered diagnostic steps:

1. **Identify emission identity.** For each synthetic-dnsp block in the
   current window, capture:
   - (a) BUILD_REQUEST id
   - (b) rf-qa / rf-qa-qualitative output absolute path
   - (c) sha256 of the output file
   - (d) the 7 DM-003 fields (severity / source / affected_range /
     evidence / recommendation / dedup_key / found_n_times)
   - (e) the cohort path selection (R-122 Path A / B / C — should be B)
   - (f) the cycle number `n` and whether it's a first-emission or a
     cross-cycle persistence (INV-012)
2. **Read the affected partition's spawn-log.** The synthetic finding's
   `evidence:` field is the canonical spawn-log path
   (`${TASK_DIR}qa/spawn-log-<agent_role>-<partition_id>.txt`); if the
   field carries the absence stub (`<!-- evidence-absence: no-spawn-log:
   <reason> -->`), record the absence reason and proceed with the
   stub-only diagnosis. The spawn-log contents are the primary root-
   cause input.
3. **Identify root cause of escalation-ladder exhaust.** The
   `escalation_ladder_exhaust_point` value (second element of
   `dedup_key`, drawn from `{retry-1, retry-2, gap-fill-round-1,
   gap-fill-round-2, gap-fill-round-3}`) names **which rung** of the
   ladder ran out. The 5 vocabulary values map to:
   - `retry-1` / `retry-2` — the partition agent attempted the assigned
     research twice and both attempts FAILed.
   - `gap-fill-round-1` / `gap-fill-round-2` / `gap-fill-round-3` — the
     gap-fill cycle attempted to close residual gaps and exhausted its
     round budget.
   Bind the exhaust-point to one of: agent timeout / WebSearch / tool
   call failure / spawn-prompt insufficiency / repeated empty research
   output / context-window saturation. Record the binding in the
   triage log.
4. **Check `dedup_key` for prior similar events.** Run
   `grep -F "<dedup_key>"` across the **last 7 days** of merged QA
   reports (offline-grep aggregation window — D-0098 / T07.19). Count
   distinct dedup_keys (the threshold target) AND count repeated
   occurrences of the current key (the persistence signal). If the
   current key has been observed in any prior 7-day window, mark the
   event as **recurrent** and bump the diagnosis priority.
5. **Classify cohort path.** Confirm the R-122 path-selection symbol
   recorded in the merged report is **Path B** (`grep -c
   'R-122-guard-precedence-violation' <merged-report>` should be 0; if
   ≠0, the cohort traversed a contract-violation path and the symptom
   upgrades to a guard-precedence audit per §2.4 step 4).
6. **Confirm dedup composition integrity (INV-012).** For each
   cross-cycle persistence case, confirm the cycle-`n+1` re-emission
   contributed `1` (not `2`) to `|F_{n+1}|` and did NOT trip Step-1
   regression detection at SKILL.md L1070
   (`grep -c 'INV-012-cross-cycle-composition-violation' <merged-
   report>` should be 0). If ≠0, the cross-cycle composition layer is
   broken — escalate per §2.4 step 4 (composes with OPS-005 regression-
   halt rate runbook).
7. **Categorise root cause.** Distinguish:
   - **T1** — **single-exhaust diagnostic** — one partition exhausted
     legitimately; the cohort traversed Path B correctly; no prior
     persistence; cohort produced ≥1 real finding from the successful
     siblings. Resolution = §2.3 T1 (manual review per
     `recommendation` field).
   - **T2** — **cross-cycle persistence** — same `dedup_key` re-emitted
     on cycles `n` and `n+1`; partition agent is stuck at the same
     exhaust point; INV-012 composition is correct (no regression
     halt). Resolution = §2.3 T2 (root-cause the stuck partition;
     improve BUILD_REQUEST or assignment slice).
   - **T3** — **weekly-threshold trip (≥3 distinct keys/7 days)** —
     systemic partition-agent instability across the cohort. Resolution
     = §2.3 T3 (Engineering-Lead escalation; cross-bind to MET-004).
   - **T4** — **false-positive** — partition agent did NOT actually
     exhaust per spawn-log inspection; the synthetic was emitted by a
     wire-shape misclassification, a guard-precedence violation, or a
     fixed-field invariant violation. Resolution = §2.3 T4 (rollback
     surface: the affected emission's per-emission rejection symbol —
     DM-003-* / R-122-* / API-003-* / INV-012-* — should have fired
     and didn't; FR-CONV.6 emitter contract regressed).
   - **T5** — **anti-mask audit** — operator inspecting a synthetic-
     dnsp emission discovers a real finding from the **same** partition
     range was dropped/coalesced during the merge step (R-126 real-
     findings-replacement audit). Resolution = §2.3 T5 (R-126 contract
     violation; immediate Engineering-Lead escalation).

### 2.3 Resolution

Resolution path depends on the root-cause category from §2.2.7. Each
resolution is bounded to a **single 24-hour SLA window**; if multiple
emissions show distinct triage classes, treat each independently and
parallelize the response.

| Root cause | Resolution | Owner | Budget |
|---|---|---|---|
| **T1** (single-exhaust diagnostic) | Operator manually reviews the affected_range per the synthetic's fixed `recommendation` literal `Manual review required — partition agent failed twice`. If the manual review confirms the underlying issue, log it in the audit trail and resolve the synthetic finding. If the manual review reveals the agent could have completed with a different prompt or assignment, record the prompt-improvement note in the BUILD_REQUEST and feed it into the next iteration. | rf-qa maintainer (with task-builder maintainer support on prompt iteration) | 24-hour SLA |
| **T2** (cross-cycle persistence) | Root-cause the stuck partition: read both cycle `n` and cycle `n+1` spawn-logs; identify why the agent exhausted at the same `escalation_ladder_exhaust_point`. Resolution depends on the exhaust-point class: (a) `retry-*` → improve the spawn-prompt or narrow the assigned_files_range; (b) `gap-fill-round-*` → expand the gap-fill round budget or improve gap-detection precision in §A.8. Apply via BUILD_REQUEST update; re-trigger the affected cohort. Track the same dedup_key across the next 7-day window to confirm resolution stuck. | task-builder maintainer (with rf-qa maintainer approval) | 24-hour SLA covers diagnosis; resolution iteration may span multiple BUILD_REQUEST cycles |
| **T3** (weekly-threshold trip — ≥3 distinct dedup_keys/7 days) | **Escalate to Engineering Lead** per §2.4 step 3. Diagnosis is systemic: the partition pipeline is producing distinct exhaust patterns at a rate that exceeds the K-006 acceptable-noise envelope. Composes with OPS-004 HALT-MONOTONICITY rate runbook if monotonicity is also tripping. Resolution = systemic upstream BUILD_REQUEST quality improvement (cross-reference OPEN-INV-006 TB-Add-2 calibration). | Engineering Lead (rf-qa maintainer initiates) | 24-hour SLA covers escalation initiation; full resolution may be a cross-week effort |
| **T4** (false-positive — wire-shape misclassification) | Do **NOT** attempt to fix in-place. **Escalate** per §2.4 step 4 (FR-CONV.6 emitter contract regressed — one of DM-003-fixed-field / DM-003-dynamic-field / DM-003-recommendation / DM-003-dedup-key-shape / DM-003-found-n-times / R-122-guard-precedence / API-003-exhaust-point-vocabulary should have rejected the emission and didn't). Bisect the post-MIG-006 commit range to identify when the rejection symbol regressed. Compose with NFR <1% false-positive ceiling (`roadmap.md:581`); if false-positive rate exceeds 1%, additional release-spec §19.4 rollback path is auto-armed. | rf-qa maintainer → task-builder maintainer → Engineering Lead | 24-hour SLA covers escalation initiation; rollback execution is multi-step |
| **T5** (R-126 real-findings-replacement audit) | **Immediate Engineering-Lead escalation.** The merge step replaced a real finding with a synthetic one (cohort's real-finding count post-merge < pre-merge) — strictly-additive merge contract violated. This is an anti-mask K-006 materialisation: synthetic-dnsp findings ARE masking real issues. Per release-spec §19.4 dependency matrix, the FR-CONV.6 merge step must be reverted while preserving FR-CONV.1..5. | Engineering Lead (rf-qa maintainer initiates) | 24-hour SLA covers escalation initiation only |

On any successful resolution (T1 / T2): the rf-qa maintainer amends
the audit trail with (a) the dedup_key + cycle range, (b) the
diagnosed root cause + resolution, (c) the cross-7-day window status,
and (d) the next-window observation plan to confirm the resolution
stuck (no recurrence of the same dedup_key).

### 2.4 Escalation

Escalation is **time-boxed by the 24-hour SLA** and bounded by the
weekly cadence:

1. **T+0 (MET-005 trip detected).** Page the rf-qa maintainer (on-call
   rotation — wired to task-builder maintainers on-call knowledge base
   per `roadmap.md:477`). The rf-qa maintainer acknowledges within 4
   hours of paging.
2. **T+4h to T+24h (diagnosis window).** rf-qa maintainer executes
   §2.2. By T+24h, the maintainer has classified the event into one of
   T1..T5.
3. **T1 / T2 path** (single-exhaust diagnostic OR cross-cycle
   persistence). Resolution proceeds per §2.3 with no further
   escalation unless the resolution itself fails or the dedup_key
   recurs in the following 7-day window.
4. **T3 path (weekly threshold — ≥3 distinct dedup_keys/7 days).**
   rf-qa maintainer escalates to **Engineering Lead** at T+24h. The
   Engineering Lead acknowledges within 1 business day. Diagnosis is
   systemic: the partition pipeline is producing distinct exhaust
   patterns at a rate that exceeds the K-006 acceptable-noise envelope.
   The Engineering Lead initiates one of: (a) upstream BUILD_REQUEST
   quality-gate audit (cross-reference OPS-004 / OPEN-INV-006 / TB-Add-2
   calibration), (b) partition-pipeline timeout / spawn-prompt
   calibration review, or (c) GA-readiness re-evaluation against
   MET-004 + MET-005 combined thresholds.
5. **T4 / T5 path (contract violation).** Engineering Lead immediately
   escalates to the **GA-tagging committee**. The committee invokes
   the release-spec §19.4 rollback path scoped to the failing emitter
   layer (DM-003 / R-122 / R-126 / INV-012 / API-003 — per-line revert
   on the violating commit). MET-005 dashboard is marked DEGRADED;
   the v3.9 GA tag (T07.20 / MIG-007b) is **blocked** until either
   (a) the rollback stabilises the emitter contract on a re-launched
   7-day measurement window, or (b) the committee approves an
   alternative remediation.
6. **False-positive rate composition (NFR threshold).** If the rolling
   7-day false-positive rate (count of T4 classifications / total
   MET-005 emission count) exceeds **1%** per `roadmap.md:581`, the
   release-spec §19.4 rollback path is auto-armed regardless of
   per-event severity. The rf-qa maintainer reports the rolling rate
   to the Engineering Lead at every weekly inspection boundary.
7. **Recurrence escalation.** Two or more OPS-002 events on the same
   `dedup_key` within a single 7-day window → automatic escalation to
   the GA-tagging committee under T3 path (the systemic-instability
   class), on the basis that the partition agent is materially stuck.

Escalation contacts and rotation handoffs live in the on-call
knowledge base (consumed via integration point at `roadmap.md:477`);
this runbook intentionally does not enumerate names so it survives
rotation changes.

### 2.5 Prevention

Prevention is enforced by four layered controls, all of which exist
at landing time and persist through GA:

1. **Wire-shape contract (DM-003 + API-003-M6).** The 7-field DM-003
   schema is rejection-gated at emission time via 5 distinct named
   rejection symbols pinned in SKILL.md L668-684 + rf-qa.md:78
   (`DM-003-fixed-field-invariant-violation`,
   `DM-003-dynamic-field-invariant-violation`,
   `DM-003-recommendation-invariant-violation`,
   `DM-003-dedup-key-shape-violation`,
   `DM-003-found-n-times-invariant-violation`) plus the wire-shape
   rejection (`API-003-exhaust-point-vocabulary-violation`). Every
   malformed emission is rejected at the emitter boundary before it
   reaches the merge step.
2. **Cohort-level path-selection guard (R-122).** The three mutually-
   exclusive paths (Path A zero-success → `rf-team-lead.md:417`;
   Path B ≥1-success AND ≥1-exhaust → emit alongside; Path C all-
   succeeded → no synthetic) are guarded at the cohort boundary by
   the `R-122-guard-precedence-violation` rejection. Any cohort
   outcome that satisfies more than one path's precondition or none
   is rejected before any per-partition emission attempt.
3. **Compositional dedup integrity (INV-012, R-123 + R-124).** Within-
   cycle identical-dedup_key collapse to a single `found_n_times`-
   incremented record is enforced by
   `INV-012-within-cycle-collapse-violation`. Cross-cycle identical-
   dedup_key composition contributing `1` (not `2`) to `|F_{n+1}|`
   AND NOT tripping Step-1 regression detection is enforced by
   `INV-012-cross-cycle-composition-violation`. The TEST-022 fixture
   (`roadmap.md:326`) verifies the cross-cycle non-regression at every
   release.
4. **Merge-step preservation (R-125 + R-126).** The strictly-additive
   merge invariant (real-finding count post-merge = pre-merge real +
   synthetic) is enforced by `R-126-real-findings-replacement-
   violation`. The HIGH severity non-overridable across merge step is
   enforced by `R-126-severity-override-violation`. The N-1 partition
   cohort concurrency invariant is enforced by
   `INV-021-cohort-serialization-violation`. These three symbols
   close the K-006 anti-mask audit at the merge boundary.

Secondary preventive measures:

- **Weekly inspection cadence.** Offline-grep aggregation across QA
  reports (D-0098 / T07.19) runs weekly; the rf-qa maintainer reviews
  MET-005 emission count + distinct-dedup_key count + cross-cycle
  persistence count + false-positive rate at the weekly boundary.
- **Pre-merge gate.** Every PR that touches the FR-CONV.6 emission
  surface — SKILL.md §A.8 / §A.10 merge step, rf-qa.md:78 emission
  paragraph, rf-analyst.md:58-71, rf-qa-qualitative.md:70-80, or
  rf-team-lead.md:417 — MUST run `make verify-sync` (A-001), the
  TEST-018..021 fixtures (`roadmap.md:384`), and a byte-diff
  confirmation that the `rf-team-lead.md:417` whole-file sha256 still
  matches `874a516e3baedd8fed5b433592ab3d41a78bd8ec8601098d8610f47ce255e40b`.
- **NFR false-positive ceiling.** The <1% false-positive rate
  (`roadmap.md:581`) is sampled at every NFR-CONV.4 measurement and
  reported in the M7 audit. Sustained exceedance arms the §19.4
  rollback path.
- **Post-window inspection.** Beyond per-release windows, release-spec
  §8.3 audit rows continue to inspect synthetic-dnsp emission counts
  on a per-release basis (MET-005 stays live indefinitely; not retired
  with the FF_DNSP feature flag).

---

## 3. Response SLA

| Field | Value |
|---|---|
| Response time | **24 hours** from MET-005 emission-count trip (or weekly-aggregation page) to acknowledgement + diagnosis |
| Owner | rf-qa maintainer (on-call rotation) |
| Source authority | `roadmap.md:432` (R-153 acceptance criteria — "24-hour-response-SLA"); `roadmap.md:465` (OPS-002 row, "24 hours response SLA; escalate ≥3 distinct/week"); `D-0091/spec.md §2` (OPS-002 line) |
| Business-hour window | The owning organisation's standard business hours apply (typically Mon-Fri, local time of the rf-qa maintainer rotation). Out-of-hours events accumulate detection latency but the SLA clock starts at the next business-hour boundary; this is consistent with OPS-001 (4h) and tighter than OPS-006 (immediate) but looser than the per-event OPS-001 audit-window because synthetic-dnsp is an emission-class signal rather than an audit-target schema event. |
| Clock-start trigger | First of: (a) MET-005 counter trip (>0 emissions on a production run), (b) weekly offline-grep aggregation page (≥3 distinct dedup_keys / 7 days), (c) manual rf-qa-maintainer inspection during release-spec §8.3 audit, (d) page from the on-call rotation. |
| SLA covers | Acknowledgement + diagnosis + root-cause categorisation (§2.2.7 → T1..T5). |
| SLA does NOT cover | Full resolution under T2 (BUILD_REQUEST iteration); systemic resolution under T3 (cross-week Engineering-Lead effort); rollback execution under T4/T5 (release-spec §19.4 path is a separate, multi-step, committee-gated operation; the 24-hour SLA only requires that the escalation be **initiated** by the SLA boundary). |

The SLA is **explicitly stated** at 24 hours to satisfy
phase-7-tasklist.md L623 ("24-hour response SLA stated").

---

## 4. Weekly inspection cadence

| Field | Value |
|---|---|
| Cadence | **Weekly** offline-grep aggregation over the rolling 7-day window |
| Aggregation source | MET-005 dashboard (synthetic-dnsp emission count) + MET-004 dashboard (synthetic-dnsp:>0-triggers-OPS-002) — both backed by offline-grep across QA reports |
| Source authority | `roadmap.md:432` (R-153 acceptance criteria — "weekly-inspection-cadence"); `roadmap.md:465` (OPS-002 row, "escalate ≥3 distinct/week"); `roadmap.md:441` (MET-004 row, "offline-grep-aggregate-per-release"); `roadmap.md:575` (DNSP emission metric — "grep `source: synthetic-dnsp` across QA reports") |
| Aggregation grep recipe | `grep -c '^source: synthetic-dnsp$'` (per-report count) + `grep -F "dedup_key:" <reports> \| sort -u \| wc -l` (distinct-key count over the 7-day window) — formal recipe lives in D-0098 / T07.19 |
| Inspection deliverables | (a) total emission count for the week; (b) distinct-dedup_key count; (c) cross-cycle persistence count (dedup_keys appearing in cycle `n` AND `n+1`); (d) false-positive count (T4 classifications); (e) rolling false-positive rate against the <1% NFR ceiling. |
| Owner | rf-qa maintainer (publishes the weekly report to the on-call knowledge base + governance audit trail) |
| Reporting boundary | Sunday 23:59 UTC of each ISO week (consistent with NFR-CONV.4 measurement-window convention). |
| Trigger composition | Single MET-005 trip → §2.1.1 / §2.2 / §2.3 T1 path (24-hour response). ≥3 distinct dedup_keys in any rolling 7-day window → §2.4 step 4 T3 escalation. |

The cadence is **explicitly documented** as weekly to satisfy
phase-7-tasklist.md L624 ("Weekly inspection cadence documented").

---

## 5. Escalation threshold

| Field | Value |
|---|---|
| Threshold | **≥3 distinct `dedup_key` values within a single rolling 7-day window** → escalate to Engineering Lead |
| Source authority | `roadmap.md:432` (R-153 acceptance criteria — implied by "weekly-inspection-cadence"); `roadmap.md:465` (OPS-002 row, "escalate ≥3 distinct/week" — verbatim); `D-0091/spec.md §2` (OPS-002 row, "24 hours response SLA; escalate ≥3 distinct/week") |
| Identity rule | Two synthetic-dnsp emissions are "distinct" when their `dedup_key` 2-tuples `(assigned_files_range, escalation_ladder_exhaust_point)` differ by at least one element. Within-cycle and cross-cycle re-emissions with identical dedup_keys collapse to a single distinct-count contribution (the INV-012 + R-123 dedup invariant ensures this is auditable). |
| Window | Rolling 7-day (not calendar-week) — i.e., at any point the rf-qa maintainer evaluates whether the past 168 hours contain ≥3 distinct dedup_keys. |
| Threshold composition | The threshold is independent of the per-event 24-hour SLA: a single event triggers T1/T2 resolution; the cumulative ≥3-distinct count triggers T3 escalation regardless of whether each individual event was resolved in-SLA. |
| Escalation target | Engineering Lead (per `D-0091/spec.md §2` OPS-002 row "escalate ≥3 distinct/week"; consistent with the OPS-005 Engineering-Lead escalation pattern). |
| Auto-arming composition | If the 7-day distinct-dedup_key count ≥3 AND the rolling false-positive rate >1% per `roadmap.md:581`, the §2.4 step 6 NFR auto-arm fires (release-spec §19.4 rollback path armed). |

The escalation threshold is **explicitly stated** at ≥3 distinct
dedup-keys per week to satisfy phase-7-tasklist.md L625 ("Escalation
threshold (≥3 distinct dedup-keys/week) explicit").

---

## 6. Acceptance criteria — T07.13

| # | Criterion (phase-7-tasklist.md L621-625) | Status | Evidence |
|---|---|---|---|
| 1 | File `TASKLIST_ROOT/artifacts/D-0093/spec.md` exists with 5 runbook sections. | **PASS** | This file at `.dev/releases/current/task-builder-merge/artifacts/D-0093/spec.md`; §2.1 Symptoms, §2.2 Diagnosis, §2.3 Resolution, §2.4 Escalation, §2.5 Prevention. |
| 2 | 24-hour response SLA stated. | **PASS** | §3 (Response time = 24 hours, Owner = rf-qa maintainer); also §1 frontmatter "Response SLA". |
| 3 | Weekly inspection cadence documented. | **PASS** | §4 (Cadence = weekly offline-grep aggregation; aggregation recipe; reporting boundary Sunday 23:59 UTC); also §1 frontmatter "Inspection cadence". |
| 4 | Escalation threshold (≥3 distinct dedup-keys/week) explicit. | **PASS** | §5 (Threshold = ≥3 distinct dedup_keys / 7-day rolling window; identity rule; Engineering-Lead target); also §1 frontmatter "Escalation threshold"; cited verbatim from `roadmap.md:465` OPS-002 row. |

**Verdict: PASS** — OPS-002 DNSP triage runbook is published,
5-section structured, 24-hour-SLA-explicit, weekly-cadence-explicit,
and ≥3-distinct-dedup-keys/week threshold explicit. Ready for rf-qa
maintainer review and for consumption by the GA-tagging committee at
T07.20 (MIG-007b).

---

## 7. Cross-references

| Linkage | Target | Role |
|---|---|---|
| **MET-005 DNSP Emission metric** | `D-0098/spec.md` (T07.19, R-163); `roadmap.md:462`; `D-0091/spec.md §2` MET-005 row | Continuous instrumentation that triggers this runbook (>0 → review) |
| **MET-004 Halt Rate (combined) metric** | `roadmap.md:441`; `D-0091/spec.md §2` MET-004 row | "synthetic-dnsp:>0-triggers-OPS-002" — co-trigger with MET-005 |
| K-006 risk row | `release-spec.md:428`; `roadmap.md:561` (R-011); `roadmap.md:410` | Originating risk this runbook mitigates |
| FR-CONV.6 emission contract (DM-003 7-field) | `src/superclaude/agents/rf-qa.md:78` + SKILL.md L668-684 | Producer-side wire-shape gate that prevents most false-positives |
| R-122 path-selection guard (3 mutually-exclusive paths) | SKILL.md §A.8 line 682 + rf-qa.md:78 | Cohort-level routing — OPS-002 covers Path B specifically |
| `rf-team-lead.md:417` byte-stable invariant | sha256 `874a516e3baedd8fed5b433592ab3d41a78bd8ec8601098d8610f47ce255e40b` (whole file); `51725c0ffa151c3403701f21910d7f5cf122639f3a0e7fa9ae3cafe82701a0a0` (line) | Path A destination — OPS-003 covers, OPS-002 verifies non-activation |
| INV-012 cross-cycle dedup composition | SKILL.md L1079-1093 + L1066; TEST-022 (`roadmap.md:326`) | Non-regression invariant for the cross-cycle persistence symptom |
| NFR false-positive ceiling | `roadmap.md:581` | <1% ceiling composed with §2.4 step 6 auto-arm |
| OPS-003 mutual-exclusivity peer runbook | `D-0094/spec.md` (T07.14, R-154) | Path A complement (zero-success → no DNSP) |
| OPS-004 HALT-MONOTONICITY peer runbook | `D-0095/spec.md` (T07.15, R-155) | Composes at T3 escalation (systemic-instability cross-bind) |
| OPS-005 regression-halt peer runbook | `D-0096/spec.md` (T07.16, R-156) | Composes when INV-012 cross-cycle composition layer breaks |
| Release-spec §19.4 rollback dependency matrix | `release-spec.md` §19.4 | Path invoked under §2.4 step 5 / step 6 |
| Consolidated GA-Readiness Governance Table | `D-0091/spec.md §2` (OPS-002 row) | This runbook is OPS-002 in that table |
| GA-tagging gate (MIG-007b) | `D-0099/spec.md` (T07.20, R-165) | Hard pre-requisite — all 7 OPS runbooks must be live for GA tag |
| Integration point — on-call knowledge base | `roadmap.md:477` (M7 Integration Points row 2) | Where this runbook is consumed by task-builder maintainers on-call rotation |
| FF_DNSP feature-flag governance | `D-0091/spec.md §1` FF_DNSP row | Flag controls FR-CONV.6 activation; cleanup window aligned with GA+30d |
| MIG-006 landing anchor commit | `87c8254 feat(task-builder): MIG-006 land FR-CONV.6 Synthetic-DNSP on Partition Exhaust (M6)` | Production-emission start anchor |

---

## 8. Provenance

- **Dependency:** Phase 6 (M6 PASS — MIG-006 landed at `87c8254`); T07.12
  mid-phase checkpoint (CP-P07-T07-T11.md) — OPS-001 + governance table
  + NFR-CONV.9 + invariant composite must be PASS before this runbook
  is consumed for GA.
- **Downstream consumers:** T07.18 mid-phase checkpoint
  (`CP-P07-T13-T17.md`); T07.19 MET-001..006 instrumentation (this
  runbook is the OPS trigger for MET-004 + MET-005); T07.20 GA-tag
  (MIG-007b) — hard pre-requisite (all 7 OPS runbooks live).
- **Anchor commit (production-emission start):** `87c8254 feat(task-builder):
  MIG-006 land FR-CONV.6 Synthetic-DNSP on Partition Exhaust (M6)`.
- **rf-team-lead.md:417 sha256 invariant** (line):
  `51725c0ffa151c3403701f21910d7f5cf122639f3a0e7fa9ae3cafe82701a0a0`.
- **rf-team-lead.md whole-file sha256 invariant:**
  `874a516e3baedd8fed5b433592ab3d41a78bd8ec8601098d8610f47ce255e40b`.
- **INV-012 cross-cycle dedup subsection sha256 invariant:**
  `5ff2a1803bbe088d2083628bf9c8cffeafba54fcc7b769efd98dd14824f09785`
  (SKILL.md L1079-1093).
- **Reporting cut-off:** 2026-05-18 14:31 UTC (current session timestamp
  from session-context envelope).
- **Release branch:** `feat/hook-sync-and-matcher-fix`.
- **MCP usage:** Sequential (preferred) — applied for runbook authoring
  (multi-step reasoning across §2.1-§2.5 + cross-reference closure
  against FR-CONV.6 + DM-003 + R-122 + INV-012 + R-126 named-symbol
  rejection table).

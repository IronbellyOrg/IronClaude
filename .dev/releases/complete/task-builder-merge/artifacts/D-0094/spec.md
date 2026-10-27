# D-0094 — OPS-003 All-Partitions-Exhaust HALT Runbook (no-DNSP)

**Task:** T07.14 (Phase 7 — M7)
**Roadmap items:** R-154
**Date:** 2026-05-18
**Branch:** `feat/hook-sync-and-matcher-fix`
**Tier:** STANDARD
**Verification method:** Direct enumeration check (5 runbook sections + mutual-exclusivity check + `rf-team-lead.md:417` cross-reference + "user resolves unresolved findings" resolution path)
**Audience:** rf-team-lead maintainer (on-call), rf-qa maintainer (peer — OPS-002 cross-coordination), Engineering Lead, GA-tagging committee
**Owner:** rf-team-lead maintainer (per `roadmap.md:466` OPS-003 row)
**Mutual-exclusivity check:** `rf-team-lead.md:417` HALT activation fires **AND** zero synthetic-dnsp blocks emit — both clauses MUST be observed jointly per FR-CONV.6 Negative Criterion (`roadmap.md:411` / R-M6-2 + `roadmap.md:562` / R-012)
**Resolution path:** User resolves unresolved findings via the existing `rf-team-lead.md:417` max-3-cycles HALT-and-ask-user contract
**Overall: PASS** (4/4 acceptance criteria met — §6)

---

## 0. TL;DR

OPS-003 is the operational runbook that turns the **all-partitions-exhaust** cohort outcome — the **Path A** branch of the R-122 three-path partition guard (`zero partitions succeeded → existing rf-team-lead.md:417 fix-cycle escalation; NO synthetic-dnsp emits`) — into an explicit on-call response procedure. It covers a single, observable cohort terminal state:

> **A production rf-qa / rf-qa-qualitative cohort completes with `partition_success_count == 0` (every partition agent exhausted its escalation ladder), the `rf-team-lead.md:417` max-3-cycles HALT activates and the user is asked to resolve, AND zero `source: "synthetic-dnsp"` blocks are emitted into the merged output stream.**

This runbook intentionally lives in **mutual exclusivity** with OPS-002 (D-0093) — OPS-002 covers Path B (`≥1-success AND ≥1-exhaust → synthetic-dnsp emits alongside real findings`), OPS-003 covers Path A (`zero-success → rf-team-lead.md:417 HALT; NO synthetic-dnsp`). On any given cohort outcome, **exactly one** of OPS-002 / OPS-003 may fire (Path C — `all-succeeded` — is a non-event for both). The mutual-exclusivity check at §2.4 turns this contract into an auditable boolean: a runbook FAILURE occurs not when Path A activates (Path A activating is the expected baseline) but when Path A activates **and** synthetic-dnsp also emits, OR when zero partitions succeeded but the `rf-team-lead.md:417` HALT did not fire.

The runbook is owned by the **rf-team-lead maintainer** (per `roadmap.md:466` "OPS-003 | All-partitions-exhaust runbook | Operational | rf-team-lead maintainer | Activates on zero-success path"). The resolution path is **user-driven**: per `rf-team-lead.md:417` ("If max cycles exhausted, HALT and ask user — do NOT proceed with unresolved findings"), the runbook does NOT auto-recover and does NOT attempt to bypass the HALT. The runbook contains the five mandatory sections (symptoms / diagnosis / resolution / escalation / prevention) called out in roadmap.md:433 and phase-7-tasklist.md L661-671.

---

## 1. Scope and authoritative bindings

This runbook binds to the following authorities (all read at landing time; cross-checked at every invocation):

| Source | Location | Binding |
|---|---|---|
| Roadmap R-154 acceptance criteria | `roadmap.md:433` | "runbook:published; mutual-exclusivity-check:documented; resolution:user-resolves-unresolved-findings" |
| Roadmap §M7 Consolidated Governance Table — OPS-003 row | `roadmap.md:466` | "OPS-003 \| All-partitions-exhaust runbook \| Operational \| rf-team-lead maintainer \| Activates on zero-success path \| FR-CONV.6" |
| Roadmap §M6 R-M6-2 (DNSP all-agents-fail short-circuit risk) | `roadmap.md:411` | "Zero-success branch emits no DNSP and uses `rf-team-lead.md:417`; FR-CONV.6 Negative Criterion enforces mutual-exclusivity" |
| Roadmap §16 R-012 (same risk row, post-merge owner) | `roadmap.md:562` | Engineering Lead owns mitigation; mutual-exclusivity is the enforced contract |
| Roadmap §M6 Objective (Path A no-synthetic clause) | `roadmap.md:358` | "preserve all-agents-fail guard (zero partitions succeeded → no synthetic, existing `rf-team-lead.md:417` escalation runs); ... zero-partitions-succeeded → NO synthetic emits and existing escalation runs" |
| Roadmap FR-CONV.6 row (preserve all-agents-fail guard) | `roadmap.md:362` | "all-agents-fail-bypass:preserved" |
| Roadmap COMP-006-M6 row (line 417 NO DRIFT) | `roadmap.md:383` | "rf-team-lead.md line 417 MUST NOT be replaced/short-circuited; verified NO DRIFT 2026-05-14; byte-diff-rf-team-lead.md:417-pre/post:0; activated-by-all-agents-fail-path" |
| R-122 path-selection guard (3 mutually-exclusive paths) | `src/superclaude/skills/task-builder/SKILL.md` L682 | "Path A (zero-partitions-succeeded → existing `rf-team-lead.md:417` fix-cycle escalation; NO synthetic emits)" — Path A authoritative definition |
| R-122 contract-violation symbol | `src/superclaude/skills/task-builder/SKILL.md` L682 | `R-122-guard-precedence-violation` — fires when cohort traverses zero or more-than-one paths |
| Synthetic-dnsp merge-step Path-A skip clause (A.8) | `src/superclaude/skills/task-builder/SKILL.md` L645 clause (e) | "the **all-agents-fail guard (R-122)** MUST have run BEFORE this merge step at the cohort boundary — when zero partitions succeeded the merge step is skipped and `rf-team-lead.md:417` activates instead (Path A; violation of the path-selection table → `R-122-guard-precedence-violation`)" |
| Synthetic-dnsp merge-step Path-A skip clause (A.10) | `src/superclaude/skills/task-builder/SKILL.md` L1153 clause (e) | Same skip-on-Path-A invariant pinned at the rf-qa A.10 partition-cohort boundary |
| `rf-team-lead.md:417` HALT contract | `src/superclaude/agents/rf-team-lead.md:417` | "Fix Cycles: If a phase pipeline returns issues, invoke another pipeline with a FIX request (max 3 cycles per phase). If max cycles exhausted, HALT and ask user — do NOT proceed with unresolved findings." |
| `rf-team-lead.md:417` byte-stable invariant | sha256 `51725c0ffa151c3403701f21910d7f5cf122639f3a0e7fa9ae3cafe82701a0a0` (line) / `874a516e3baedd8fed5b433592ab3d41a78bd8ec8601098d8610f47ce255e40b` (whole file) | Pre-PR-03 contract preserved across MIG-006; COMP-006-M6 NO-DRIFT verified |
| MIG-006 landing commit | `87c8254 feat(task-builder): MIG-006 land FR-CONV.6 Synthetic-DNSP on Partition Exhaust (M6)` | Anchor commit for Path A activation in production |
| OPS-002 peer runbook (Path B counterpart) | `D-0093/spec.md` (T07.13, R-153) | Mutual-exclusivity partner — OPS-002 covers Path B; OPS-003 covers Path A; never both on a single cohort |

**Scope boundary.** OPS-003 covers **Path A (zero-partitions-succeeded → `rf-team-lead.md:417` HALT; NO synthetic-dnsp)** of the R-122 three-path table — i.e., a production cohort where every partition agent exhausted its escalation ladder and no sibling succeeded. The Path B (≥1-success AND ≥1-exhaust) case is handled by OPS-002 (D-0093). The Path C (all-succeeded) case is a non-event (no HALT, no DNSP). OPS-003 does **not** cover Self-Audit / semantic-check audit-target events (→ OPS-001), HALT-MONOTONICITY rate (→ OPS-004), regression-halt rate (→ OPS-005), `make verify-sync` failure (→ OPS-006), or INV-018 layout-change blast radius (→ OPS-007). OPS-003 is **not** a triage runbook for a single partition exhaust (that is OPS-002 territory) and does not require a weekly emission-count cadence — it is event-driven by the `rf-team-lead.md:417` HALT itself, which is by construction operator-visible.

---

## 2. Runbook — 5 sections

### 2.1 Symptoms

The on-call rf-team-lead maintainer is paged or alerted (by the existing `rf-team-lead.md:417` HALT mechanism, which presents the unresolved findings directly to the user) when **all** of the following are jointly observed in a production rf-qa / rf-qa-qualitative cohort post-MIG-006 (anchor commit `87c8254`, 2026-05-18 — FR-CONV.6 landed):

1. **Cohort terminal state: zero partition successes.** The partition-cohort completion summary records `partition_success_count == 0` — every spawned partition agent (rf-analyst, rf-qa, or rf-qa-qualitative partition instance) traversed its full escalation ladder (`retry-1` → `retry-2` → `gap-fill-round-1` → `gap-fill-round-2` → `gap-fill-round-3`, vocabulary per `roadmap.md:363` DM-003-M6 + API-003 wire-shape) and terminated in exhaust rather than success.
2. **`rf-team-lead.md:417` HALT activation.** The orchestrator routes control to the byte-stable `rf-team-lead.md:417` fix-cycle escalation. Operationally, the user observes one of: (a) max-3-cycles exhausted message presented to the user with the unresolved findings list; (b) execution log entry recording the Path A activation symbol; (c) absence of forward progress in the pipeline (no phase-`n+1` invoked).
3. **Zero synthetic-dnsp emissions in the merged output stream.** A `grep -c '^source: synthetic-dnsp$'` (or the structured-block equivalent) across the cohort's merged QA reports returns **0**. The expected baseline for Path A is `MET-005 == 0` (per `roadmap.md:411` "Zero-success branch emits no DNSP" + `roadmap.md:466` OPS-003 row + roadmap §M6 Objective `roadmap.md:358`).
4. **(Optional) Operator-visible user prompt.** Because the `rf-team-lead.md:417` HALT terminates with "ask user — do NOT proceed with unresolved findings," the user is the canonical first observer; this runbook formalises the on-call response to the user's report or to the audit-trail entry generated by the HALT.

Detection sources: (a) the user, via the `rf-team-lead.md:417` HALT prompt itself (event-driven, not poll-driven); (b) MET-004 combined halt-rate dashboard recording an all-agents-fail event (`roadmap.md:441`); (c) per-release post-mortem audit (release-spec §8.3) confirming the absence of synthetic-dnsp on a zero-success cohort; (d) rf-team-lead maintainer offline-grep audit confirming Path A activations are paired with zero DNSP emissions.

**Symptom not in scope.** The presence of `[HALT-MONOTONICITY]` or `[REGRESSION-HALT]` markers in the cohort log is a Phase-5 (FR-CONV.5) signal, NOT a Phase-6 Path A signal — those route to OPS-004 / OPS-005. Path A specifically requires `partition_success_count == 0` at the cohort boundary; a HALT from a *retry-monotonicity* or *regression* gate inside a single partition's lifecycle is distinct from the all-agents-fail cohort terminal.

### 2.2 Diagnosis

Within **24 hours** of the `rf-team-lead.md:417` HALT (the canonical event), the rf-team-lead maintainer performs the following ordered diagnostic steps:

1. **Confirm cohort identity and zero-success condition.** Capture:
   - (a) BUILD_REQUEST id
   - (b) Partition-cohort manifest path (`${TASK_DIR}qa/` parent + `${TASK_DIR}research/` parent)
   - (c) Each partition agent's spawn-log path (`${TASK_DIR}qa/spawn-log-<agent_role>-<partition_id>.txt`)
   - (d) Each partition agent's terminal status (success | exhaust at `<escalation_ladder_exhaust_point>`)
   - (e) Total partition count `N` and success count (target: `0`)
   - (f) Cycle number `n` at HALT
2. **Verify line-417 escalation fired.** Confirm the `rf-team-lead.md:417` fix-cycle HALT activated end-to-end:
   - (i) Grep the orchestrator's execution log / audit trail for the Path A activation marker (no synthetic-dnsp emit attempts logged at the cohort boundary; the merge step at SKILL.md §A.8 / §A.10 records the skip with reference to clause (e) of L645 / L1153).
   - (ii) Confirm the byte-stable invariant: `rf-team-lead.md:417` line sha256 matches `51725c0ffa151c3403701f21910d7f5cf122639f3a0e7fa9ae3cafe82701a0a0`; the whole-file `src/superclaude/agents/rf-team-lead.md` sha256 matches `874a516e3baedd8fed5b433592ab3d41a78bd8ec8601098d8610f47ce255e40b`.
   - (iii) Confirm the user-facing "HALT and ask user — do NOT proceed with unresolved findings" prompt was presented (audit trail entry or session log).
3. **Verify no synthetic-dnsp emitted (mutual-exclusivity check).** This is the runbook's signature audit (see §2.4 below). Run:
   - `grep -c '^source: synthetic-dnsp$' <merged-cohort-reports>` → expected `0`.
   - `grep -F 'dedup_key:' <merged-cohort-reports> | grep -c .` → expected `0` synthetic-class dedup_key occurrences (real-finding dedup_keys, if any, are out of scope; for Path A there should be no real findings either because every partition failed).
   - `grep -c 'R-122-guard-precedence-violation' <merged-cohort-reports>` → expected `0` (any non-zero count means the cohort traversed an invalid path — see §2.4 step 4).
4. **Enumerate exhaust points per partition.** For each partition's spawn-log, record the `escalation_ladder_exhaust_point` (∈ `{retry-1, retry-2, gap-fill-round-1, gap-fill-round-2, gap-fill-round-3}`, closed vocabulary per `src/superclaude/agents/rf-qa.md:78` + `roadmap.md:363`). Distribution patterns inform the root-cause category in step 6.
5. **Read each partition's terminal output.** Even though Path A means none of the partition agents *succeeded*, each one may have left a partial-research artifact or a structured failure message. Collect these alongside the spawn-logs to feed the user-resolution step.
6. **Classify the cohort root cause.** Distinguish:
   - **A1** — **BUILD_REQUEST scope mismatch.** Every partition agent failed at `retry-1` or `retry-2` with a "research target ambiguous / no anchors found" signature. The BUILD_REQUEST is malformed for the assigned topic — operator must rewrite. Resolution = §2.3 A1.
   - **A2** — **Upstream artifact gap.** Every partition agent failed at `gap-fill-round-*` with "prerequisite artifact not found / phase-`n-1` outputs absent" signatures. A prior phase did not emit the expected inputs. Resolution = §2.3 A2.
   - **A3** — **External dependency outage.** Every partition agent failed with "tool call failure / WebSearch timeout / MCP server unreachable" signatures. Resolution = §2.3 A3.
   - **A4** — **Context-window saturation cohort-wide.** Every partition agent failed at `retry-*` with token-limit signatures despite partition slicing. Indicates the BUILD_REQUEST cohort sizing is mis-calibrated upstream (TB-Add-2). Resolution = §2.3 A4.
   - **A5** — **Contract-violation halt (NOT a valid Path A).** A non-zero grep for `R-122-guard-precedence-violation` (step 3 above) means the cohort traversed an invalid path: e.g., `partition_success_count == 0` AND a synthetic-dnsp block *did* emit, OR `partition_success_count == 0` AND `rf-team-lead.md:417` did *not* activate, OR a cohort with `zero successes AND zero exhausts` was accepted (every partition must terminate in success-or-exhaust under the M5 escalation-ladder semantics ratified at FR-CONV.5). Resolution = §2.3 A5 (contract violation — immediate Engineering-Lead escalation).
7. **Compose with peer runbooks.** OPS-003 events do NOT contribute to the OPS-002 weekly cadence (no synthetic-dnsp emitted by definition). They DO contribute to MET-004 combined halt-rate (`roadmap.md:441` row — "synthetic-dnsp:>0-triggers-OPS-002; HALT-MONOTONICITY:>50%-triggers-OPS-004"); a sustained Path A rate is reviewed at the M7 audit boundary and at the GA-tagging committee gate.

### 2.3 Resolution

Path A is, by design, a **user-resolution** path. The `rf-team-lead.md:417` contract explicitly forbids the orchestrator from proceeding with unresolved findings: the runbook's job is to formalise the human-in-the-loop response, not to auto-recover. Resolution is bounded by root-cause category from §2.2.6; each is bounded to a **single 24-hour SLA window**.

| Root cause | Resolution | Owner | Budget |
|---|---|---|---|
| **A1** (BUILD_REQUEST scope mismatch) | The rf-team-lead maintainer surfaces the HALT to the user with the per-partition exhaust-point distribution and the spawn-log excerpts that diagnose scope mismatch. The user (BUILD_REQUEST author) rewrites the BUILD_REQUEST with: (i) clearer research anchors, (ii) explicit assigned_files ranges, (iii) any necessary context references. The rewritten BUILD_REQUEST is re-submitted to a fresh pipeline run. **No state from the failed cohort is auto-promoted** (preserves the `rf-team-lead.md:417` "do NOT proceed with unresolved findings" contract). | User (BUILD_REQUEST author) primary; rf-team-lead maintainer advisory | 24-hour SLA covers diagnosis + handoff; user-side iteration is unbounded |
| **A2** (upstream artifact gap) | The rf-team-lead maintainer identifies the missing prior-phase artifact(s) and reports to the user. The user either: (i) re-runs the earlier phase to produce the missing artifact, then re-launches this phase; (ii) revises the phase ordering in the project plan; (iii) accepts the gap as a known limitation. **No phase-`n` synthetic continuation is attempted** (would violate the unresolved-findings contract). | User primary; rf-team-lead maintainer advisory | 24-hour SLA covers diagnosis + handoff; user-side rerun is unbounded |
| **A3** (external dependency outage) | The rf-team-lead maintainer confirms the outage signature is environmental (MCP server unreachable, network failure, tool-rate-limit ceiling) and surfaces to the user with a retry timestamp recommendation. The user re-launches the pipeline after the dependency recovers. **No mock substitution or fallback emission is permitted** (would violate the FR-CONV.6 Negative Criterion mutual-exclusivity by potentially injecting synthetic-dnsp on a Path A cohort). | User primary; rf-team-lead maintainer advisory | 24-hour SLA covers diagnosis; user-side rerun is gated on dependency recovery |
| **A4** (cohort-wide context saturation) | The rf-team-lead maintainer reports the saturation signature to the user and to the task-builder maintainer for TB-Add-2 calibration review (cross-references OPS-004 / OPEN-INV-006). The user revises the BUILD_REQUEST with: (i) finer partition slicing, (ii) reduced per-partition research surface, (iii) tighter spawn-prompts. The revised BUILD_REQUEST is re-submitted. | User primary; task-builder maintainer secondary; rf-team-lead maintainer advisory | 24-hour SLA covers diagnosis + cross-team handoff |
| **A5** (contract-violation halt — invalid Path A) | **Immediate Engineering-Lead escalation** per §2.4 step 4. The cohort traversed an invalid R-122 path: either (i) synthetic-dnsp emitted on a zero-success cohort (Path A short-circuited and FR-CONV.6 mutual-exclusivity is violated — risk row R-M6-2 / R-012 has materialised), OR (ii) `rf-team-lead.md:417` did not activate on a zero-success cohort (cohort terminal state is degenerate), OR (iii) `R-122-guard-precedence-violation` symbol fired. The Engineering Lead invokes release-spec §19.4 rollback path scoped to the FR-CONV.6 merge step + R-122 guard (revert MIG-006 commit `87c8254` per release-spec dependency matrix). **No user resolution is attempted on the originating BUILD_REQUEST until the contract is restored.** | Engineering Lead (rf-team-lead maintainer initiates) | 24-hour SLA covers escalation initiation only |

On any successful resolution (A1 / A2 / A3 / A4): the rf-team-lead maintainer amends the audit trail with (a) the cohort identity + partition-exhaust distribution, (b) the diagnosed root cause + user-resolution path, (c) the re-launched pipeline run identity (if applicable), and (d) confirmation that no synthetic-dnsp was emitted on the original Path A cohort and that the re-launched cohort is being tracked independently.

**Explicit non-resolutions** (forbidden by the `rf-team-lead.md:417` contract):
- Do NOT manually inject a synthetic-dnsp block into the merged Path A report "to make MET-005 reflect the user-visible exhaust." MET-005 is correctly `0` on Path A by mutual-exclusivity construction.
- Do NOT auto-advance to phase `n+1` on a HALT'd phase `n` cohort.
- Do NOT silently re-run the failing partition agents without a BUILD_REQUEST revision (would loop indefinitely under the same scope mismatch).
- Do NOT mark the HALT as a "non-issue" or close it without user acknowledgement (would violate the "ask user" clause of `rf-team-lead.md:417`).

### 2.4 Escalation

Escalation is **event-driven** by the `rf-team-lead.md:417` HALT activation and time-boxed by the 24-hour diagnosis SLA. The escalation path forks at the mutual-exclusivity audit:

#### 2.4.1 Mutual-exclusivity check (signature audit for this runbook)

The mutual-exclusivity check is the single contract that distinguishes a **correct Path A activation** (baseline; user-resolves) from a **Path A contract violation** (escalate). Per the FR-CONV.6 Negative Criterion (`roadmap.md:411` / R-M6-2 + `roadmap.md:562` / R-012):

> Zero-success branch emits **no DNSP** **AND** uses `rf-team-lead.md:417`; FR-CONV.6 Negative Criterion enforces mutual-exclusivity.

The check is encoded as a 2x2 truth table on the cohort outcome:

| `rf-team-lead.md:417` HALT fired? | Synthetic-dnsp emitted? | Verdict | Action |
|---|---|---|---|
| **YES** | **NO** | **PASS** (correct Path A baseline) | Proceed with §2.3 user-resolution path (A1/A2/A3/A4) |
| YES | YES | **FAIL — mutual-exclusivity violated** | A5 contract-violation; Engineering-Lead escalation (§2.4 step 4) |
| NO | NO | FAIL — Path A short-circuited without HALT (degenerate cohort terminal) | A5 contract-violation; Engineering-Lead escalation (§2.4 step 4) |
| NO | YES | FAIL — cohort took Path B but reported zero successes (degenerate cohort terminal — Path B requires ≥1 success) | A5 contract-violation; Engineering-Lead escalation (§2.4 step 4) |

The audit is run **once per HALT event** by the rf-team-lead maintainer at T+24h, with evidence captured in the cohort audit trail. Three of the four cells are FAIL because Path A is exactly one cell of the table; this is the design intent of mutual-exclusivity.

#### 2.4.2 Escalation ladder

1. **T+0 (HALT detected — user-visible).** The `rf-team-lead.md:417` HALT prompt is presented to the user; the user reports the HALT to the rf-team-lead maintainer (on-call rotation — wired into the on-call knowledge base per `roadmap.md:477`). The maintainer acknowledges within 4 hours of paging.
2. **T+4h to T+24h (diagnosis window).** rf-team-lead maintainer executes §2.2 including the §2.4.1 mutual-exclusivity check. By T+24h, the maintainer has classified the event into one of A1..A5.
3. **A1 / A2 / A3 / A4 path** (mutual-exclusivity PASS). Resolution proceeds per §2.3 with user-driven BUILD_REQUEST revision or environment recovery. No further escalation unless the re-launched cohort also Path-A halts on the same root cause (in which case A4 promotes to A5-class systemic-instability per §2.4 step 5).
4. **A5 path (mutual-exclusivity FAIL or contract violation).** rf-team-lead maintainer escalates to **Engineering Lead** at T+24h. The Engineering Lead acknowledges within 1 business day. Diagnosis is a contract regression: FR-CONV.6 Path A clause (clause e at SKILL.md L645 / L1153 + R-122 guard at L682) has been violated. Engineering Lead initiates one of: (a) immediate revert of the violating commit per release-spec §19.4 dependency matrix (MIG-006 anchor `87c8254`; revert preserves FR-CONV.1..5 by §19.4 isolation); (b) hotfix patch to the violating gate; (c) GA-readiness re-evaluation if the violation materialises a sustained pattern.
5. **A5 path under recurrence (≥2 contract violations within a single 7-day window).** Engineering Lead escalates to the **GA-tagging committee**. The committee invokes the release-spec §19.4 rollback path scoped to FR-CONV.6 end-to-end (revert MIG-006); MET-004 combined halt-rate dashboard is marked DEGRADED; the v3.9 GA tag (T07.20 / MIG-007b) is **blocked** until the contract is restored on a re-launched 7-day measurement window.
6. **Cross-runbook composition.** A Path A activation with a co-occurring `[HALT-MONOTONICITY]` rate trip (>50%) or `[REGRESSION-HALT]` rate trip (>20%) routes through OPS-004 / OPS-005 in parallel — OPS-003 owns the Path A mutual-exclusivity check; OPS-004 / OPS-005 own the cycle-level monotonicity / regression diagnosis. The runbooks do not block each other; they share evidence at the M7 audit boundary.
7. **Mass-A1-recurrence escalation.** Three or more independent BUILD_REQUESTs Path-A halting with A1 (scope mismatch) signatures within a single 7-day window → automatic escalation to the user (and the operator team if the user is a system rather than a person) for a BUILD_REQUEST authoring review — the scope-discipline rule is failing systemically.

Escalation contacts and rotation handoffs live in the on-call knowledge base (consumed via integration point at `roadmap.md:477`); this runbook intentionally does not enumerate names so it survives rotation changes.

### 2.5 Prevention

Prevention is enforced by four layered controls, all of which exist at landing time and persist through GA:

1. **Cohort-level path-selection guard (R-122).** The three mutually-exclusive paths (Path A zero-success → `rf-team-lead.md:417`; Path B ≥1-success AND ≥1-exhaust → emit alongside; Path C all-succeeded → no synthetic) are gated at the cohort boundary by the `R-122-guard-precedence-violation` rejection. The guard runs **before** any per-partition emission attempt (per SKILL.md L682 — "The synthetic-dnsp emitter MUST gate on the partition-cohort success count BEFORE any per-partition emission attempt"). A cohort with zero successes is decided once at the cohort boundary and routed to `rf-team-lead.md:417` without per-partition emission attempts; a malformed cohort (zero successes AND zero exhausts) is rejected outright. This is the primary mutual-exclusivity enforcer.
2. **Merge-step skip clauses (clause e at SKILL.md L645 + L1153).** Both the A.8 (Research Quality Gate merge) and A.10 (Task File Validation merge) clauses (e) require the all-agents-fail guard to fire BEFORE the merge step, with the merge **skipped** on Path A. Each skip records a `R-122-guard-precedence-violation` symbol if the path-selection table is breached. Two redundant skip clauses (A.8 + A.10) make the prevention contract surface twice in the producer pipeline.
3. **COMP-006-M6 byte-stable invariant (`rf-team-lead.md:417`).** The line is pinned at sha256 `51725c0ffa151c3403701f21910d7f5cf122639f3a0e7fa9ae3cafe82701a0a0` (whole-file `874a516e3baedd8fed5b433592ab3d41a78bd8ec8601098d8610f47ce255e40b`); a pre-merge byte-diff confirms zero drift across every PR that touches the FR-CONV.6 surface. The HALT-and-ask-user contract is therefore frozen against accidental modification.
4. **FR-CONV.6 Negative Criterion (mutual-exclusivity invariant).** The negative criterion ("Zero-success branch emits **no DNSP** **AND** uses `rf-team-lead.md:417`") is restated in the post-merge risk row R-M6-2 / R-012 (`roadmap.md:411` / `roadmap.md:562`) and is the explicit policy authority for §2.4.1 mutual-exclusivity audit. Any PR that proposes to weaken or modify the mutual-exclusivity invariant requires Engineering-Lead + GA-tagging-committee sign-off.

Secondary preventive measures:

- **Pre-merge gate.** Every PR that touches the FR-CONV.6 emission surface — SKILL.md §A.8 / §A.10 merge step (L645 + L1153), R-122 guard at SKILL.md L682, rf-qa.md:78 emission paragraph, rf-analyst.md:58-71, rf-qa-qualitative.md:70-80, or `rf-team-lead.md:417` — MUST run `make verify-sync` (A-001), the TEST-018..021 fixtures (`roadmap.md:384`), and a byte-diff confirmation that the `rf-team-lead.md:417` line + whole-file sha256s match the invariants above.
- **TEST-021 fixture (parallel-research preservation on Path A).** `test_dnsp_does_not_serialize_cohort` (`roadmap.md:387`) verifies the N-1 partitions continue concurrently when one exhausts; the same fixture's zero-success variant (when all N partitions exhaust) verifies no synthetic-dnsp emits, exercising the OPS-003 baseline.
- **MET-004 dashboard.** Combined halt-rate metric (`roadmap.md:441`) tracks Path A activations; a sustained spike above the M7-audit threshold (read at GA gate) triggers an OPS-003 cohort-quality review.
- **Audit-trail explicitness.** Every Path A cohort terminal emits an audit-trail entry recording (i) zero-success confirmation, (ii) `rf-team-lead.md:417` HALT activation, (iii) zero-DNSP confirmation — making the mutual-exclusivity check post-hoc verifiable from logs without re-running the cohort.
- **Post-window inspection.** Beyond per-release windows, release-spec §8.3 audit rows continue to inspect Path A activations on a per-release basis (the contract stays live indefinitely; not retired with the FF_SYNTHETIC_DNSP_EMISSION feature flag — when the flag is cleaned up at GA+30d, only the synthetic emission goes away; the all-agents-fail HALT remains).

---

## 3. Mutual-exclusivity check (signature audit)

| Field | Value |
|---|---|
| Audit name | **OPS-003 mutual-exclusivity check** |
| Definition | A Path A cohort outcome (`partition_success_count == 0`) MUST jointly satisfy: (i) `rf-team-lead.md:417` HALT activated **AND** (ii) zero synthetic-dnsp blocks emitted. Any other combination is a contract violation. |
| Authority | `roadmap.md:411` (R-M6-2 row) + `roadmap.md:562` (R-012 row): "Zero-success branch emits no DNSP **and** uses `rf-team-lead.md:417`; FR-CONV.6 Negative Criterion enforces mutual-exclusivity"; SKILL.md L682 (R-122 three-path table); SKILL.md L645 clause (e) + L1153 clause (e) (merge-step skip on Path A). |
| Mechanical recipe | (a) `grep -c '^source: synthetic-dnsp$' <merged-cohort-reports>` MUST be `0`; (b) audit-trail entry MUST record `rf-team-lead.md:417` HALT activation; (c) `grep -c 'R-122-guard-precedence-violation' <merged-cohort-reports>` MUST be `0`; (d) `rf-team-lead.md:417` line sha256 MUST match `51725c0ffa151c3403701f21910d7f5cf122639f3a0e7fa9ae3cafe82701a0a0`. |
| Audit cadence | Once per HALT event (event-driven); not poll-driven (Path A is operator-visible by construction). Aggregated weekly into MET-004 combined halt-rate report. |
| 2x2 outcome table | See §2.4.1 above — exactly one of four cells is PASS (HALT=YES, DNSP=NO); three are FAIL. |
| Failure-mode response | Each FAIL cell routes to A5 (contract-violation halt) per §2.3; immediate Engineering-Lead escalation per §2.4 step 4. |
| Composition with peers | OPS-002 (D-0093) covers Path B (the **co-occurrence** Path — synthetic-dnsp DOES emit). OPS-003 + OPS-002 together exhaust the "≥1-exhaust" half of the R-122 table; together with Path C (no-event), they exhaust the table. |

The mutual-exclusivity check is **explicitly documented** in §2.4.1 + §3 to satisfy phase-7-tasklist.md L670 ("Mutual-exclusivity check explicitly documented").

---

## 4. Cross-reference to `rf-team-lead.md:417`

| Field | Value |
|---|---|
| Anchor | `src/superclaude/agents/rf-team-lead.md:417` |
| Verbatim text | "Fix Cycles: If a phase pipeline returns issues, invoke another pipeline with a FIX request (max 3 cycles per phase). If max cycles exhausted, HALT and ask user — do NOT proceed with unresolved findings." |
| Section context | `## Project Mode Architecture` → 5th bullet (between "Phase 1..N (Execution)" and "Project Plan: Maintained using ...") |
| Byte-stability invariants | Line sha256 `51725c0ffa151c3403701f21910d7f5cf122639f3a0e7fa9ae3cafe82701a0a0`; whole-file `src/superclaude/agents/rf-team-lead.md` sha256 `874a516e3baedd8fed5b433592ab3d41a78bd8ec8601098d8610f47ce255e40b` (NO-DRIFT verified 2026-05-14 per `roadmap.md:97` COMP-006 + `roadmap.md:383` COMP-006-M6) |
| Behavioural contract | (a) "max 3 cycles per phase" — bounded fix-cycle ladder; (b) "If max cycles exhausted, HALT and ask user" — terminal state on exhaust; (c) "do NOT proceed with unresolved findings" — explicit forward-progress prohibition |
| Pre/post-PR-03 equivalence | Per `roadmap.md:411` R-M6-2 mitigation and `roadmap.md:362` FR-CONV.6 row "all-agents-fail-bypass:preserved"; the line is the canonical zero-success destination both before and after MIG-006 |
| Path A activation precondition | `partition_success_count == 0` at the partition-cohort boundary (R-122 Path A from SKILL.md L682) |
| Activation evidence | Audit-trail entry MUST record activation; merge-step skip MUST log a Path-A skip notice referencing SKILL.md L645 clause (e) / L1153 clause (e); user-facing HALT prompt MUST be presented |

The cross-reference is **explicitly documented** in §1 (authority binding), §2.1 (symptom 2), §2.2 step 2 (diagnosis), §2.5 control 3 (prevention), §3 (audit recipe), and §4 (this section) to satisfy phase-7-tasklist.md L671 ("Cross-reference to `rf-team-lead.md:417`").

---

## 5. Resolution path — user resolves unresolved findings

| Field | Value |
|---|---|
| Resolution model | **User-driven** — `rf-team-lead.md:417` requires the operator (or the human user behind the operator) to acknowledge and resolve the unresolved findings before any pipeline progress |
| Authority | `roadmap.md:433` R-154 row ("resolution:user-resolves-unresolved-findings"); `rf-team-lead.md:417` ("HALT and ask user — do NOT proceed with unresolved findings") |
| What "resolve" means | One of: (a) **revise the BUILD_REQUEST** and re-launch the pipeline (A1, A2, A4 root causes); (b) **wait for an external dependency to recover** and re-launch the pipeline (A3 root cause); (c) **accept the gap** as a known limitation and close the BUILD_REQUEST without pipeline progression. Synthesising findings, mocking outputs, or auto-advancing past the HALT are explicitly disallowed. |
| What "unresolved findings" means in Path A | The cohort produced **zero successful partition outputs**, so the "findings" are the per-partition exhaust signatures themselves: each partition's spawn-log + terminal status + exhaust-point classification. These constitute the actionable input for the user. |
| User as primary owner | The BUILD_REQUEST author (typically the user driving the pipeline) is the primary owner of the resolution. The rf-team-lead maintainer's role is advisory — surface the diagnosis, confirm the mutual-exclusivity audit PASS, hand off to the user. |
| Re-launch isolation | Any re-launched cohort runs as a **new** pipeline invocation with a **revised** BUILD_REQUEST; the failed Path A cohort's outputs are **not** auto-promoted into the new run (preserves the unresolved-findings prohibition end-to-end). |
| Acceptance signal | The HALT is closed in the audit trail when the user acknowledges the diagnosis AND (a) submits a revised BUILD_REQUEST, OR (b) accepts the gap and closes the run, OR (c) confirms the dependency recovery plan. |
| Non-acceptance | If the user does not engage within the operator-defined window, the rf-team-lead maintainer escalates per §2.4 step 7 (mass-A1-recurrence) only if the same root-cause class recurs across ≥3 independent BUILD_REQUESTs — single un-engaged HALTs remain open in the audit trail. |

The resolution path is **explicitly documented** in §1 frontmatter, §2.3 (resolution table per A1..A5), §2.5 (prevention of forbidden auto-resolutions), and §5 (this section) to satisfy phase-7-tasklist.md L672 ("Resolution path: user resolves unresolved findings").

---

## 6. Acceptance criteria — T07.14

| # | Criterion (phase-7-tasklist.md L667-672) | Status | Evidence |
|---|---|---|---|
| 1 | File `TASKLIST_ROOT/artifacts/D-0094/spec.md` exists with 5 runbook sections. | **PASS** | This file at `.dev/releases/current/task-builder-merge/artifacts/D-0094/spec.md`; §2.1 Symptoms, §2.2 Diagnosis, §2.3 Resolution, §2.4 Escalation, §2.5 Prevention. |
| 2 | Mutual-exclusivity check explicitly documented. | **PASS** | §2.4.1 (2x2 truth table — HALT × DNSP outcome combinations) + §3 (signature audit definition + mechanical recipe); cross-referenced from §1 frontmatter "Mutual-exclusivity check"; cited verbatim from `roadmap.md:411` R-M6-2 + `roadmap.md:562` R-012 + SKILL.md L682 R-122 Path A; A5 root-cause class encodes the failure response. |
| 3 | Cross-reference to `rf-team-lead.md:417`. | **PASS** | §4 (dedicated cross-reference section: anchor, verbatim text, section context, byte-stability invariants, behavioural contract, pre/post-PR-03 equivalence); additionally referenced in §1 (authority binding row), §2.1 symptom 2, §2.2 diagnosis step 2, §2.5 prevention control 3, and §3 audit recipe (d). |
| 4 | Resolution path: user resolves unresolved findings. | **PASS** | §5 (dedicated resolution-path section: user-driven model, what "resolve" means, what "unresolved findings" means in Path A, user as primary owner, re-launch isolation, acceptance signal); §2.3 A1..A4 resolution rows each route to user-side revision; §2.5 forbidden auto-resolutions enumerated; §1 frontmatter "Resolution path" cites `roadmap.md:433` R-154. |

**Verdict: PASS** — OPS-003 All-partitions-exhaust HALT runbook is published, 5-section structured, mutual-exclusivity-check explicit (2x2 truth table + signature audit recipe), `rf-team-lead.md:417` cross-referenced at six call sites with byte-stability invariants, and user-driven resolution path documented end-to-end. Ready for rf-team-lead maintainer review and for consumption by the GA-tagging committee at T07.20 (MIG-007b).

---

## 7. Cross-references

| Linkage | Target | Role |
|---|---|---|
| **`rf-team-lead.md:417` HALT contract** | `src/superclaude/agents/rf-team-lead.md:417` (sha256 `51725c0ffa151c3403701f21910d7f5cf122639f3a0e7fa9ae3cafe82701a0a0`; whole-file `874a516e3baedd8fed5b433592ab3d41a78bd8ec8601098d8610f47ce255e40b`) | Path A activation destination — the entire reason this runbook exists |
| **R-122 path-selection guard (Path A clause)** | `src/superclaude/skills/task-builder/SKILL.md` L682 | Cohort-level routing — OPS-003 covers Path A specifically |
| **Merge-step skip clause (A.8)** | `src/superclaude/skills/task-builder/SKILL.md` L645 clause (e) | Merge step skips on Path A; cited in §2.5 prevention control 2 |
| **Merge-step skip clause (A.10)** | `src/superclaude/skills/task-builder/SKILL.md` L1153 clause (e) | Redundant skip clause at rf-qa A.10 partition-cohort boundary |
| **FR-CONV.6 Negative Criterion (mutual-exclusivity)** | `roadmap.md:411` R-M6-2 + `roadmap.md:562` R-012 | Authority for the §2.4.1 mutual-exclusivity audit |
| **COMP-006-M6 byte-stability invariant** | `roadmap.md:383` (`byte-diff-rf-team-lead.md:417-pre/post:0; activated-by-all-agents-fail-path`) | Pre-merge prevention gate for line-417 drift |
| **K-006 risk row (synthetic-dnsp masking)** | `roadmap.md:561` (R-011) | Risk that this runbook composes with (Path A's no-emit baseline narrows the K-006 false-positive surface to Path B alone) |
| **MET-004 Halt Rate (combined) metric** | `roadmap.md:441`; `D-0091/spec.md §2` MET-004 row | Path A activations contribute to combined halt-rate; sustained rate triggers M7-audit-boundary review |
| **OPS-002 peer runbook (Path B counterpart)** | `D-0093/spec.md` (T07.13, R-153) | Mutual-exclusivity partner — see §1 scope-boundary; cited at §2.4.1 + §3 |
| **OPS-004 HALT-MONOTONICITY peer runbook** | `D-0095/spec.md` (T07.15, R-155) | Composes when Path A co-occurs with cycle-level monotonicity halts |
| **OPS-005 regression-halt peer runbook** | `D-0096/spec.md` (T07.16, R-156) | Composes when Path A co-occurs with cycle-level regression halts |
| **TEST-021 (parallel-research preservation)** | `roadmap.md:387` | Fixture covering N-1 cohort concurrency including zero-success variant |
| **TEST-018 (twice-exhaust synthetic emission)** | `roadmap.md:384` | Path B counterpart fixture — its absence on Path A is the OPS-003 baseline |
| **Release-spec §19.4 rollback dependency matrix** | `release-spec.md` §19.4 | Path invoked under §2.4 step 4 / step 5 (A5 contract-violation) |
| **Consolidated GA-Readiness Governance Table** | `D-0091/spec.md §2` (OPS-003 row) | This runbook is OPS-003 in that table |
| **GA-tagging gate (MIG-007b)** | `D-0099/spec.md` (T07.20, R-165) | Hard pre-requisite — all 7 OPS runbooks must be live for GA tag |
| **Integration point — on-call knowledge base** | `roadmap.md:477` (M7 Integration Points row 2) | Where this runbook is consumed by rf-team-lead maintainers on-call rotation |
| **FF_SYNTHETIC_DNSP_EMISSION feature-flag governance** | `roadmap.md:388` + `D-0091/spec.md §1` FF_DNSP row | Flag controls FR-CONV.6 activation; cleanup at GA+30d removes synthetic emission only — `rf-team-lead.md:417` HALT remains live indefinitely |
| **MIG-006 landing anchor commit** | `87c8254 feat(task-builder): MIG-006 land FR-CONV.6 Synthetic-DNSP on Partition Exhaust (M6)` | Production Path A enforcement anchor |
| **Phase-7 dependency (T07.13 → T07.14)** | `phase-7-tasklist.md` L677 ("Dependencies: Phase 6 (M6 PASS); T07.13") | OPS-002 must land before OPS-003 (mutual-exclusivity partner ordering) |

---

## 8. Provenance

- **Dependency:** Phase 6 (M6 PASS — MIG-006 landed at `87c8254`); T07.13 OPS-002 runbook (D-0093) — Path B counterpart must land first to anchor the mutual-exclusivity partner reference.
- **Downstream consumers:** T07.18 mid-phase checkpoint (`CP-P07-T13-T17.md`); T07.19 MET-001..006 instrumentation (MET-004 combined halt-rate reads Path A activations); T07.20 GA-tag (MIG-007b) — hard pre-requisite (all 7 OPS runbooks live).
- **Anchor commit (Path A enforcement start in production):** `87c8254 feat(task-builder): MIG-006 land FR-CONV.6 Synthetic-DNSP on Partition Exhaust (M6)`.
- **`rf-team-lead.md:417` line sha256 invariant:** `51725c0ffa151c3403701f21910d7f5cf122639f3a0e7fa9ae3cafe82701a0a0`.
- **`rf-team-lead.md` whole-file sha256 invariant:** `874a516e3baedd8fed5b433592ab3d41a78bd8ec8601098d8610f47ce255e40b`.
- **R-122 Path A clause sha256 invariant (SKILL.md L682):** Pinned by COMP-006-M6 NO-DRIFT verification 2026-05-14 (`roadmap.md:383`).
- **Reporting cut-off:** 2026-05-18 14:38 UTC (current session timestamp from session-context envelope).
- **Release branch:** `feat/hook-sync-and-matcher-fix`.
- **Session HEAD:** `efaa33db9f0087bb1c48236b12c1287171b4f9f8` (`chore(hooks): resolve OQ-2 (archive+delete bash-gate orphan) and OQ-3 (register reject-workspace-writes.sh)`).
- **MCP usage:** Sequential (preferred) — applied for runbook authoring (multi-step reasoning across §2.1-§2.5 + mutual-exclusivity 2x2 truth table + cross-reference closure against FR-CONV.6 Negative Criterion + R-122 Path A + COMP-006-M6 byte-stability invariant + OPS-002 peer-runbook complement).

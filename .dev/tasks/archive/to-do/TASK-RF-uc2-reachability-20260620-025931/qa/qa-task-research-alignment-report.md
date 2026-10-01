# QA Report: Task-Research Alignment

**QA_MODE:** task-integrity
**LENS:** task-research-alignment
**Date:** 2026-06-20
**Adversarial stance:** Assume builder dropped/misrepresented findings. Target ≥3 alignment gaps.

**Task file:** TASK-RF-uc2-reachability-20260620-025931.md
**Research dir:** research/
**Authoritative TDD:** issue-1-uc2-reachability/tdd.md
**Spec:** issue-1-uc2-reachability/spec.md

---

## Sources Read (all cross-validated against live files)

- TASK file (455 lines, full): frontmatter + 8 phases + Phase Gate + Post-Completion.
- Research 01 (gather+gate anchors), 02 (contract/classify/fail-open), 03 (refs inventory), 04 (eval/grader inventory) — all 4 read in full.
- Live `SKILL.md` (1854 lines) — spot-Read at :402, :463-464, :663, :804, :1024-1029, :1555-1560, :1638-1644, :1772, :1799.
- Live `refs/reviewer-spec.md` :47-49; `spec.md` (794 lines) FR headers + §3/§6/§7; `tdd.md` (1079 lines) §24.1/§24.2.

---

## Checklist Item 1 — All 10 FRs represented as own item-clusters?

**VERDICT: PASS (with one defensible adversarial note — see Issue A).**

Every FR-RSR.1–10 maps to an owning execution item; none dropped:

| FR | Owning edit step | Dedicated verification |
|----|------------------|------------------------|
| FR-RSR.1 tagger | Step 3.1 (§6.1 step 4b') | Step 3.4 |
| FR-RSR.2 sweep | Step 3.2 (§6.1 step 4b) | Step 3.4 |
| FR-RSR.3 oracle | Step 2.1 (authored in `runtime-surface.md`) + Step 3.2 (wired) | Step 2.2 + Step 3.4 |
| FR-RSR.4 rootwalk | Step 2.1 (authored) + Step 3.2 (wired) | Step 2.2 + Step 3.4 |
| FR-RSR.5 forbid-STOP | Step 4.1 (§5.3/§5.4) | Step 4.2 |
| FR-RSR.6 §10.9 modifier | Step 5.1 + Step 5.2 (taxonomy xref) | Step 5.3 |
| FR-RSR.7 contract | Step 3.3 (§9.1/§9.3) | Step 3.4 |
| FR-RSR.8 fail-open | Step 6.2 (§6.5/§0.5d) | Step 6.3 |
| FR-RSR.9 reviewer-brief | Step 6.1 (reviewer-spec.md) | Step 6.3 |
| FR-RSR.10 eval | Steps 7.1–7.9 (9 items) | Step 7.9 + Post-Completion |

This is faithful to the TDD design: FR-RSR.3/.4 are not standalone SKILL.md edits — by spec design they are deterministic *content* (oracle table + rootwalk algorithm) authored in the new ref (Step 2.1, which TDD §23.2 makes the P1 critical-path predecessor) and *gated into* the §6.1 sweep (Step 3.2). The spec itself (§FR-RSR.2, lines 287, 297) states the sweep "REQUIRES the FR-RSR.4 entrypoint-rootwalk to be consulted before any UNREACHED" — so co-locating .3/.4 with .2 in the sweep edit is the spec-mandated structure, NOT a builder merge that drops content. Each still carries its own acceptance verification.

---

## Checklist Item 2 — VERIFIED research anchors used (not TDD stale approximates)?

**VERDICT: PASS. Every spot-check anchor confirmed against the LIVE 1854-line file.**

| Spot-check anchor | Task cites | Live-file verified | Status |
|-------------------|-----------|--------------------|--------|
| §5.3 forbid-STOP pre-filter | :402 | :402 = "Pre-filter precedence (D13)..." verbatim | MATCH |
| §6.1 step 4 + existing 4a | step4 :463, 4a :464 | :463 `find_referencing_symbols`, :464 `Task(reuse-auditor...)` | MATCH |
| §9.1 contract_version 3 gate sites | :663 / :804 / :1772 | all three contain `1.5.0` verbatim | MATCH |
| §9.1 cosmetic sites | :1558 / :1641 | :1558 = `"<contract_version from §9.1>"` ref; :1641 = literal `"1.5.0"` | MATCH (see Issue B nuance) |
| §10.9 insertion gap | :1025–1027 | :1025 "Default remediation" line, :1026 blank, :1027 `---` | MATCH |
| §17.7 item 6 (no 5th class) | :1799 | :1799 = "5th `unknown` deviation category... Rejected" | MATCH |
| reviewer-spec.md 3 sections + insertion | :25/:31/:49, insert :47–49 | :47 D13 entry, :49 `## Coverage slice` (insertion between, inside Grounding hunks) | MATCH |
| deviation-taxonomy.md xref window | :115–138 | research 03 §2 confirms `## Grounding-gaps parallel artifact` :115–138 | MATCH (research-confirmed) |

The task's Key-Constraints block and the per-step "Read the verified anchors in `0N-*.md`" instructions consistently route the executor to the RESEARCH files' re-anchored line numbers, NOT the TDD's approximate ones. The task even calls this out explicitly ("the TDD's are approximate; the research files re-anchor against the live 1854-line SKILL.md", line 111). This is correctly handled.

---

## Checklist Item 3 — Codebase-over-doc reconciliations honored?

**VERDICT: PASS.**

- **(a) eval cases under `cases/uc2-*/` (NOT `evals/`)**: Phase 7 header (line 258) carries the explicit verified codebase-over-doc NOTE; every Step 7.2–7.6 creates `cases/uc2-<name>/`; Step 7.7 registers with `case_dir: "cases/uc2-<name>/"`. Matches research 04 §0/§7 ("cases live under `cases/`, NOT `evals/`"). HONORED.
- **(b) ids 37–41**: research 04 §1 confirms current count = 36, next ids 37–41. Step 7.7 registers exactly ids 37–41 contiguous. HONORED.
- **(c) count-invariant `len(unreached_surfaces)==runtime_surface_unreached`**: Step 7.1 gives a concrete resolution — PREFER precomputed scalar `count_invariant_holds: true` asserted via `yaml_field`, with grader-extension as fallback only if infeasible. This directly resolves research 04 §6-id41's flagged problem (`parse_yaml_simple` can't read list length). HONORED with a defensible, documented mechanism.
- **(d) grader keys**: Step 7.2 cites `regex_absent {target,pattern}`; Step 7.3 `yaml_field {target,field,expected}`; Steps 7.2/7.6 `yaml_field_min {target,field,min_value}`. All three exactly match research 04 §3a/§3b/§3c (incl. the `min_value` not `value` caveat). HONORED.

---

## Checklist Item 4 — Two load-bearing invariants + counter hygiene in verification clauses?

**VERDICT: PASS.**

- **Symbol-anchored tagger (requirement_id nullable, sweep runs regardless)**: Step 3.1 mandates `requirement_id` OPTIONAL ("null when a surface hunk has no mapped requirement; the sweep still runs"), tagger "symbol-anchored (NEVER requirement-anchored — must not depend on a Wave-1B mapping built later)". Step 2.1 types ledger `requirement_id: str | None`. Verified in Step 3.4 acceptance (FR-RSR.1 box "no-mapped-requirement still tagged `requirement_id:null`"). PRESENT.
- **Degrade-default-to-Grounding-Gap (oracle/unknown-lang/partial-rootwalk/backend → DEGRADE, never Regression)**: Phase 3 header, Step 2.1 (default-DEGRADE rule), Step 3.2 (oracle/rootwalk gate before any UNREACHED), Step 6.2 (backend loss → DEGRADE). Asserted in eval cases 39 (dynamic-dispatch DEGRADE) and 40 (backend:none Grounding Gap). PRESENT.
- **Counter hygiene (increment ONLY `deviation_count_by_class.regression`, never `verification_regressions_detected`)**: stated in Objectives 5, Key Constraints (line 133), Phase 5 header, Step 5.1, Step 5.3 acceptance box (a), TDD §24.2 line (d) embedded in Step 8.2. The grep confirms the ONLY counter named anywhere in the task is `.regression` — no fabricated counter. PRESENT and rigorously repeated.

---

## Checklist Item 5 — Spec §3 acceptance + §6 NFR + TDD §24.1 DoD in matching verification checklists?

**VERDICT: PASS.**

- **Spec §3 acceptance boxes**: each Phase verification item cites exact spec acceptance line ranges (e.g. Step 2.2 → spec :332–342 FR-RSR.3; Step 3.4 → :244–252/:271–273/:303–316/:463–474; Step 4.2 → :392–403; Step 5.3 → :430–439; Step 6.3 → :506–511/:486–493). Verified: live spec FR-RSR.3 "Acceptance Criteria" sits at :332–342 exactly as cited.
- **Spec §6 NFR measurements**: Step 3.4 (NFR-RSR.1/.2/.4 → spec :682–685), Step 6.3 (NFR-RSR.6 → :687), Step 7.9 (NFR-RSR.2 determinism). Verified: live spec §6 NFR table rows NFR-RSR.1–6 at :682–687 match the cited measurement methods (e.g. NFR-RSR.3 → `uc2-surface-dynamic-dispatch` asserts degraded + regression unchanged).
- **TDD §24.1 DoD lines**: each verification item names its matching DoD line verbatim; Step 8.2 verifies the §24.2 Release Checklist (5 lines) against artifacts. Verified: live TDD §24.1 (:975–991) has exactly the 9 DoD bullets the task's items mirror; §24.2 (:992–998) has the 5 release lines Step 8.2 enumerates.

---

## Checklist Item 6 — Scope-expansion check (no fabricated file/edit/requirement)?

**VERDICT: PASS.**

- **NO 5th deviation class**: enforced in Objectives, Key Constraints, Phase 5 header, Steps 5.1/5.3, lens PG.3/PG.7. Grep confirms no taxonomy class beyond the 4 is introduced.
- **NO new counter**: grep of all `deviation_count_by_class.*` in the task → only `.regression`. No `.runtime_surface`, `.reuse_miss`, `.unreached`, etc.
- **NO new CLI flag**: no `--reach*`/`--surface*`/new-flag token appears; the only flags referenced are pre-existing `--tier 1`/`--depth quick`/`--no-escalate`/`--remediate`/`--strategy enterprise` (all from the existing §5.1 surface). The forbid-STOP pre-filter reuses the existing user-pin carve-out verbatim.
- **File inventory bounded to TDD §18.2**: 1 SKILL.md (6 edits), 1 new `runtime-surface.md`, 2 existing refs (reviewer-spec.md, deviation-taxonomy.md), eval cases + evals.json, grader only if Step 7.1 fallback fires. `coverage-mapping.md` + `grader-extensions.md` are READ-ONLY context. PG.7 lens explicitly guards against any edit outside this set. No fabricated file appears.

---

## ADVERSARIAL FINDINGS (≥3 required)

### Issue A — MINOR — FR-RSR.3/.4 have no standalone numbered SKILL.md edit step (shared with FR-RSR.2 in Step 3.2)
FR-RSR.3 (oracle) and FR-RSR.4 (rootwalk) do not own a dedicated `Step X` titled for them; they are authored as ref content in Step 2.1 and wired into the sweep in Step 3.2 (titled "FR-RSR.2 / FR-RSR.3 / FR-RSR.4"). An adversarial reading is "two FRs merged into a batch." **Assessment: NOT a real defect.** The spec (FR-RSR.2 §, lines 287/297) mandates the rootwalk/oracle be *consulted inside the sweep*, and TDD §23.2 makes them P1 ref-content predecessors — so this is the spec-mandated structure, not a dropped/merged finding. Each carries its own acceptance verification (Step 2.2 + the FR-RSR.3/.4 boxes in Step 3.4). Severity MINOR (structural observation only); no action required, but a reviewer should confirm Step 3.4's acceptance explicitly checks BOTH the oracle-DEGRADE box AND the rootwalk-partial-DEGRADE box (it does — cites spec :332–342 and :361–370).

### Issue B — MINOR — Step 3.3 instruction to "refresh" cosmetic site :1558 slightly over-states the edit
Step 3.3 says to "refresh the two cosmetic sites (:1558 skill_version ref and :1641 the stale literal) so they read 1.6.0." Live-file check: :1558 is `"skill_version": "<contract_version from §9.1>"` — a *template reference that auto-derives* from §9.1, so it already "reads 1.6.0" once §9.1 is bumped and needs NO literal edit. Only :1641 (`"skill_version": "1.5.0"`) is a genuine stale literal requiring a hand-edit. The task's own framing elsewhere is precise (calls :1558 a "ref" and :1641 a "stale literal"), so the executor has the information to avoid a spurious edit — but the imperative "refresh ... so they read 1.6.0" applied to :1558 could prompt an unnecessary/incorrect change to the placeholder. Severity MINOR; recommend the executor treat :1558 as no-op (verify it remains the `<contract_version from §9.1>` placeholder) and edit only :1641. Note: research 02 catalogued only the 3 gate sites (:663/:804/:1772) and did NOT enumerate :1558/:1641 — the task's reconciliation (b) added these two; I independently confirmed both exist in the live file, so the addition is grounded, not fabricated.

### Issue C — MINOR — Count-invariant grader mechanism (Step 7.1) leaves a conditional fork that could weaken eval id 41
Step 7.1 PREFERS a precomputed scalar `count_invariant_holds: true` asserted via `yaml_field`, with a grader-extension fallback. This is a sound resolution of research 04's flagged gap. The residual risk: a precomputed boolean emitted by the *same skill under test* is self-attesting — if the skill computes `len(unreached_surfaces) == runtime_surface_unreached` wrong, it could emit `count_invariant_holds: true` anyway, and `yaml_field` would pass vacuously. The stronger guarantee is the grader actually reading the list length. Step 7.1 does flag "ONLY if emitting a precomputed scalar is infeasible" use the grader extension — but infeasibility is not the right trigger; *self-attestation weakness* is. Severity MINOR (the eval still fails-pre/passes-post on the headline; this only affects the rigor of id 41's invariant check). Recommend: id 41 cross-check the scalar against `runtime_surface_unreached` via TWO `yaml_field` assertions (assert `count_invariant_holds == "true"` AND assert `runtime_surface_unreached` matches the fixture's known surface count), so a mis-emitted scalar cannot pass silently.

### Issue D — INFORMATIONAL — TDD-vs-research reviewer-spec.md line discrepancy is correctly resolved in the task
Research 03 §"Top correction" flags that the TDD's "three-section invariant at lines 23, 43, 45, 47" is imprecise (43/45/47 are reassertion sentences, real headings are 25/31/49). The task (Key Constraint (c), Step 6.1) correctly uses :25/:31/:49 for headings and :47–49 for the insertion window — i.e. it adopted the RESEARCH correction over the stale TDD. This is the desired behavior; logged as evidence the builder honored research-over-TDD, not a defect.

---

## VERDICT: PASS

All six checklist items PASS. Every FR-RSR.1–10 has a faithful owning item-cluster; the executor is routed to the VERIFIED research anchors (independently confirmed against the live 1854-line SKILL.md and the refs); all four codebase-over-doc reconciliations are honored; both load-bearing invariants + counter hygiene are embedded in verification clauses; spec §3 / §6 and TDD §24.1/§24.2 lines appear in the matching checklists; and no scope expansion (no 5th class, no new counter, no new CLI flag, no out-of-inventory file) was found.

The adversarial pass surfaced **4 findings, all MINOR/INFORMATIONAL** — none blocks execution:
- **Issue A** (MINOR): FR-RSR.3/.4 share Step 3.2 with FR-RSR.2 — spec-mandated co-location, not a dropped finding.
- **Issue B** (MINOR): Step 3.3 "refresh :1558" over-states a no-op placeholder edit; only :1641 is a real literal.
- **Issue C** (MINOR): count-invariant scalar (Step 7.1) is self-attesting; recommend a paired cross-check assertion for eval id 41.
- **Issue D** (INFORMATIONAL): task correctly adopted research's reviewer-spec.md line correction over the stale TDD.

**Recommendation:** PROCEED. Optionally fold the Issue B/C nuances into the executor's Step 3.3 and Step 7.1 notes (treat :1558 as no-op; add a paired cross-check for id 41), but neither is a correctness blocker — the task faithfully translates the TDD/spec/research into actionable items with no dropped or fabricated content.

---

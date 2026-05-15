# Transfer Manifest — Phase 5 Synthesis (Binding)

**Task:** T05.03 — Produce `transfer-manifest.md` and `rejected-features-ledger.md`
**Roadmap Item:** R-018
**Tier:** STANDARD
**Generated:** 2026-05-15
**Status:** BINDING — this manifest is the locked sprint output. Phase 6 (merge plan) and Phase 7 (merge execution) consume this artifact verbatim. Per R-RULE-11, no entry may be silently re-litigated downstream.

**Inputs (1:1 referenced):**
- `stack-rank.md` (T04.05) — 12 ADOPT/ADAPT primary rows + carry-forward subsumption map (catalog rows 34/35/36).
- `feature-dependency-matrix.md` (T05.01) — 11 dependency-map (DM-N) entries + 16 conflict-register (CR-N) entries.
- `integration-sketches.md` (T05.02) — 9 ADOPT (IS-ADOPT-N) + 3 ADAPT (IS-ADAPT-N) locked sketches.

**Companion artifact:** `rejected-features-ledger.md` — every REJECT (terminal rationale) and DEFER (precondition) feature lives there. Together these two files partition every Phase 4 verdict 1:1 with the donor catalog.

**Recipient attach target (R-RULE-10):** `src/superclaude/skills/task/SKILL.md`. The `.claude/` mirror is byte-identical and is NOT the merge target. Phase 6 must edit `src/` then run `make sync-dev`.

---

## 0. R-RULE-06 governing principle (binding)

**"Absorb patterns, not implementation mass."** Every entry below records a *control pattern* extracted from the donor (`src/superclaude/skills/sc-task-protocol/SKILL.md`) and locked to a recipient extension point — never a copy-paste of donor ceremony. Where donor ceremony was dropped during synthesis, the drop is named explicitly in the entry's "Donor ceremony dropped" line.

Donor traceability rows (D10 → Gate 1; D15a → Gate 2; D16 → Gate 2; D17 + D18 → Path Override) appear with **`(donor-traceability)`** annotation: they record that a donor row's *pattern* was absorbed by another transfer unit, with zero net implementation work.

---

## 1. Execution Order — Transfer Units (TU-1 through TU-8)

Execution order respects the dependency map (`feature-dependency-matrix.md` § 2). Build-order rule: *D09a + Gate 1 lead; Gate 2 / TFEP Baseline / D15b layer on top; TFEP cluster lands as a coherent block; Path Override may merge at any time but its integration-order constraints (CR-7 / CR-8) must hold at runtime.*

| Order | Transfer Unit | Features | Dep on | Type |
|---|---|---|---|---|
| 1 | TU-1 | IS-ADOPT-3 + IS-ADOPT-6 (D09a `Tier:` field + Gate 1 Dispatch) | — | ADOPT (single ship-together unit, CR-9) |
| 2 | TU-2 | IS-ADOPT-1 (Critical/Trivial Path Override) | — (path-glob-based, classification-independent; **integration order**: at runtime fires BEFORE Gate 1 at row 1 and BEFORE Gate 2 at row 10 — CR-7 / CR-8) | ADOPT |
| 3 | TU-3 | IS-ADAPT-1 (Gate 2 — Verification routing widening) | TU-1, TU-2 | ADAPT |
| 4 | TU-4 | IS-ADAPT-3 (D15b — Layer 2 pre-flight scaffolding) | TU-1 | ADAPT |
| 5 | TU-5 | IS-ADOPT-8 (TFEP Test baseline snapshot, D21) | TU-1 (tier-gated STRICT/STANDARD) | ADOPT |
| 6 | TU-6 | IS-ADOPT-2 + IS-ADOPT-4 (TFEP Prohibitions D19 + Permitted exceptions D20) | — (carve-outs co-located with prohibitions, DM-8) | ADOPT |
| 7 | TU-7 | IS-ADOPT-9 (TFEP Escalation trigger detection, D22) | TU-5 (consumes baseline as comparator, DM-7) | ADOPT |
| 8 | TU-8 | IS-ADOPT-5 (TFEP Incident reporting, D24) | TU-5 + TU-6 + TU-7 (TFEP cluster ADOPT subset, DM-9) | ADOPT |
| — | Donor-traceability annotations | IS-ADOPT-7 (D10) inside TU-1; IS-ADAPT-2 (D15a) inside TU-3 | — | Zero implementation work |

**No dependency cycle.** TU-1 ↔ TU-1 (D09a + Gate 1) is a "ship together" co-binding inside the same transfer unit, not a cycle.

---

## 2. Transfer Unit Detail (binding entries)

Each entry declares: **Donor row(s)** | **Extension point(s)** | **Integration sketch / modification** | **New field/hook** | **Dependencies** | **Observable post-condition** | **Donor ceremony dropped (R-RULE-06)** | **Bound manifest exceptions**.

---

### TU-1 — `Tier:` field schema extension + Gate 1 Dispatch (ship-together unit)

**Donor rows:** D04 (cluster) + D09 (split → D09a) + D10 (command-side dispatch, donor-traceability merged here).
**Stack-rank rows:** Row 3 (D09a, Net=10.0, ADOPT) + Row 6 (Gate 1, Net=7.5, ADOPT) + Row 7 (D10, ADOPT MERGE-WITH-GATE-1).
**Reason for ship-together:** CR-9 / Manifest Exception #6 — D09a is inert metadata without Gate 1; Gate 1 has nothing to dispatch on without D09a. Ship together or ship neither.

**Extension points (3 surfaces, all C5):**
1. Extension-point row 13 — Required frontmatter schema slot (`extension-point-contracts.md:169-175`; `SKILL.md:69`) — new optional `Tier:` field.
2. Extension-point row 1 — Task File Validation gate (`extension-point-contracts.md:60-67`; `SKILL.md:64-73`) — closed-enum check + Gate 1 dispatch.
3. Extension-point row 4 — F1 EXECUTE item-type dispatch (`extension-point-contracts.md:86-94`; `SKILL.md:89-96`) — per-item `Tier:` annotation read, fallback to task-level.

**Integration sketch:**
- **New MDTM frontmatter field:** `Tier:` — optional, closed-enum `{STRICT, STANDARD, LIGHT, EXEMPT}`. Per-item annotation supported as inline marker (e.g., `- [ ] (Tier: LIGHT) trivial typo fix`); task-level value is the fallback. Missing value defaults to `STANDARD` at Gate 1.
- **Task File Validation gate ordering (CR-7, locked):** `path_override_check (TU-2) → tier_field_validate → gate_1_dispatch`. Validator runs closed-enum check; malformed value → refusal diagnostic. Gate 1 then reads `forced_stance` (from TU-2 if set) ∨ `Tier:` value ∨ default `STANDARD`.
- **Gate 1 dispatch logic (PRE-LOOP ONLY, CR-10):**
  - `LIGHT` / `EXEMPT` → lightweight profile: skip TFEP baseline (TU-5), skip D15b pre-flight (TU-4), F1 with reduced Phase-Gate QA budget. Post-Completion Validation STILL FIRES (INV-03 floor).
  - `STANDARD` → existing budget profile: F1 + Phase-Gate QA (existing budget) + Post-Completion Validation.
  - `STRICT` → full profile: F1 + D15b pre-flight (TU-4) + TFEP baseline (TU-5) + Phase-Gate QA with widened budget (TU-3) + Post-Completion Validation including TFEP incident-report check (TU-8).
- **Shape of change:** ~3-5 lines (frontmatter requirements) + ~5-10 lines (validator closed-enum) + ~10-15 lines (Gate 1 dispatch block) + ~3 lines (F1 per-item read).

**New field / hook:** `Tier:` frontmatter field (only new field introduced by this sprint); `gate_1_dispatch(forced_stance, tier_value) → execution_profile` hook (pre-loop, fires once at task entry).

**Dependencies:** None upstream (TU-1 is the foundation). TU-3 / TU-4 / TU-5 depend on TU-1.

**Observable post-condition:**
1. `Tier:` field, when present, is closed-enum-validated at task entry.
2. `## Task Log / Notes` records one line: `gate-1: dispatch_profile=<STRICT|STANDARD|LIGHT|EXEMPT> source=<path-override|tier-field|default>`.
3. STRICT-only side-effect files (`research/test-baseline.yaml` from TU-5, `research/tfep-incident-report.md` from TU-8) appear if and only if STRICT profile dispatched.

**Donor ceremony dropped (R-RULE-06):**
- Donor's separate command-side dispatch layer (D10, donor-traceability row) — `/task` is Skill-invoked on a file path; there is no command-side surface in the recipient model. The pattern (dispatch-by-Tier) is absorbed into Gate 1 at the recipient's validation surface; the donor's separate command layer is not ported.
- D09b (donor's classifier with priority cascade + keyword tables) is REJECTed (Row 21) — see ledger. Tier values arrive declaratively from the task file (author-tagged), not from a runtime classifier inside `/task`. Classifier responsibility, if needed, belongs to `task-builder`.

**Bound manifest exceptions:**
- **ME-1 (CR-10 / Stack-rank Exception #1):** PRE-LOOP DISPATCH ONLY. Gate 1 fires **once at task-entry**, **never per-item** inside F1 EXECUTE. Per-item per-tier dispatch is auto-REJECT under INV-01 (would re-evaluate loop control each iteration).
- **ME-6 (CR-9 / Stack-rank Exception #6):** D09a + Gate 1 ship as a single transfer unit. Implementing D09a alone leaves inert metadata (R-RULE-06 ceremony-without-teeth). Implementing Gate 1 alone has no input to dispatch on.

---

### TU-2 — Critical/Trivial Path Override

**Donor rows:** D17 (Critical Path Override) + D18 (Trivial Path Override). Catalog rows 35 + 36 carry these as subsumed-by-row-1.
**Stack-rank row:** Row 1 (Net=20.0, ADOPT — highest-scored feature in the sprint).

**Extension points (2 surfaces):**
1. Extension-point row 1 — Task File Validation gate (C5).
2. Extension-point row 10 — Phase-Gate QA Verification (`extension-point-contracts.md:141-149`; `SKILL.md:182-211`; C3).

**Integration sketch:**
- `path_override_check(task_target_paths) → forced_stance ∈ {STRICT, LIGHT, none}` — pure read, no file mutation.
- **Critical path-glob set** (forces STRICT regardless of `Tier:`): `auth/`, `security/`, `crypto/`, `models/`, `migrations/` (sourced verbatim from `src/superclaude/skills/sc-task-protocol/SKILL.md:121`).
- **Trivial path-glob set** (forces LIGHT only if task touches NO files outside the set): `*.md`, `docs/`, `*test*.py` (sourced from `sc-task-protocol/SKILL.md:123`).
- **At row 1 (CR-7):** fires FIRST, before tier-field validate, before Gate 1 dispatch. Sets `forced_stance` flag consumed by Gate 1.
- **At row 10 (CR-8):** fires FIRST, before Gate 2 stance/budget select. STRICT items in critical-path-glob get force-escalation; LIGHT/EXEMPT items fully inside trivial-path-glob get force-de-escalation.
- **Shape of change:** ~10 lines at row 1; ~5 lines at row 10.

**New field / hook:** No new MDTM frontmatter field. New hook: `path_override_check` (pure read).

**Dependencies:** None upstream. **Integration-order obligation:** at runtime, must fire before TU-1 (Gate 1) at row 1 and before TU-3 (Gate 2) at row 10 (CR-7 / CR-8). Build-order: can land independently — recommended landing in same merge as TU-1 so the integration order is locked atomically.

**Observable post-condition:** Single line in `## Task Log / Notes`:
- `path-override: forced_stance=STRICT (matched: <path-glob>)`, OR
- `path-override: forced_stance=LIGHT (all paths inside trivial-glob set)`, OR
- `path-override: no-match (forced_stance=none)`.

Post-completion validation inspects this line on STRICT items.

**Donor ceremony dropped (R-RULE-06):** None — donor pattern absorbed without modification. The override is the donor's strongest "safety floor" pattern; both critical and trivial path-glob sets carry verbatim from donor.

**Bound manifest exceptions:**
- **CR-7 (integration order at row 1):** `path_override_check → tier_field_validate → gate_1_dispatch`. Any reordering re-introduces the wrong-stance dispatch window the override exists to close.
- **CR-8 (integration order at row 10):** `path_override_check → gate_2_stance_select`. Gate 2 must read the override flag before selecting budget.

---

### TU-3 — Gate 2 Verification routing widening (ADAPT)

**Donor rows:** D16 (Verification routing table, catalog row 34 subsumed) + cluster's Gate 2 + D15 (split → D15a, donor-traceability).
**Stack-rank rows:** Row 10 (Gate 2, Net=4.0, ADAPT) + Row 11 (D15a, ADAPT MERGE-WITH-GATE-2).

**Extension point:** Extension-point row 10 — Phase-Gate QA Verification (C3).

**Modification (ADAPT — what changes vs donor):**
- **Donor form:** Separate "Verification Routing Layer" that owns the verifier choice and *substitutes* verifier identity per tier (e.g., STRICT → `quality-engineer` replaces donor's default verifier).
- **Recipient form:** Phase-Gate QA is **widened**, not routed. `rf-qa` adversarial-stance verifier always runs (INV-03 floor). Tier conditions a **budget + roster widening**:
  - **STRICT:** ~5K token budget, 60s timeout, AND `quality-engineer` added to roster as an *additional* adversarial verifier alongside `rf-qa`.
  - **STANDARD:** existing budget, `rf-qa` only.
  - **LIGHT / EXEMPT:** reduced budget (~1.5K, 20s), `rf-qa` only.
- Path-override consulted FIRST (CR-8). If `forced_stance=STRICT` due to critical-path-glob match, STRICT profile applies regardless of `Tier:`; if `forced_stance=LIGHT`, LIGHT profile applies.

**Shape of change:** ~25 lines added to Phase-Gate QA block.

**New field / hook:** No new frontmatter. Consumes `Tier:` (TU-1) + `forced_stance` (TU-2).

**Dependencies:** TU-1 (Tier field + Gate 1 dispatch — DM-5); TU-2 (Path Override flag for runtime ordering).

**Observable post-condition:**
- Phase-Gate QA report at `${TASK_DIR}reviews/qa-phase-[N]-report.md` includes:
  - `verifier_roster: [rf-qa, quality-engineer]` (STRICT) OR `[rf-qa]` (STANDARD/LIGHT/EXEMPT).
  - `budget: <tokens>/<timeout>` line.
- Task Log: `gate-2: profile=<STRICT|...> budget=<n>/<s> roster=[...]`.

**Donor ceremony dropped (R-RULE-06):**
- Donor's verifier-*replacement* semantic for STRICT (auto-REJECT under INV-03 per CR-11).
- Donor's separate "verification routing table" as a standalone configuration artifact — recipient inlines tier→budget mapping in the existing Phase-Gate QA section.
- Donor's per-tier verifier-list rewriting — only roster *addition* supported, never substitution.
- D15a's standalone "Layer 2 verification-stance" framing (separately named layer with its own subsection in donor SKILL.md). Only its stance-widening pattern is absorbed into TU-3.

**Donor-traceability rows folded here:** D15a (Row 11) + D16 (catalog row 34, ADAPTABLE-subsumed).

**Bound manifest exceptions:**
- **ME-2 (CR-11 / Stack-rank Exception #2):** `rf-qa` SUPPLEMENTED NOT REPLACED. `quality-engineer` is *additional*; the `rf-qa` adversarial stance always runs. Replacing `rf-qa` is auto-REJECT under INV-03.

---

### TU-4 — D15b Layer 2 pre-flight scaffolding (ADAPT)

**Donor row:** D15 (split → D15b).
**Stack-rank row:** Row 12 (Net=3.33, ADAPT).

**Extension point:** Extension-point row 2 — First Item Protocol (`extension-point-contracts.md:69-75`; `SKILL.md:100-102`; C5).

**Modification (ADAPT — what changes vs donor):**
- **Donor form:** D15 carries D15c — a "Layer 2 procedural step-list" *synthesized at execute-time inside F1 EXECUTE*, with tier-specific multi-step procedures (serena activate → git status → codebase-retrieval → list_memories) emitted as runtime steps the loop did not READ from disk. **D15c is REJECTed** (Row 26, ledger entry) under INV-01 + INV-05 collision.
- **Recipient form:** Tier-gated **additive pre-loop setup** in First Item Protocol — NOT inside F1 EXECUTE, NOT per-item, NOT execute-time procedure synthesis:
  - **STRICT** (or `forced_stance=STRICT`): `serena_activate_if_available` → `git_status_clean_tree_check` → `codebase_retrieval_on_relevant_code_if_available` → `list_memories_read_memory_for_relevant_prior_context`.
  - **STANDARD:** `codebase_retrieval_on_relevant_code_if_available`.
  - **LIGHT / EXEMPT:** skipped.
- Each step conditional on tool availability; graceful skip on unavailability (`serena` / `codebase-retrieval` are MCP-dependent).

**Shape of change:** ~15-25 lines added to First Item Protocol section.

**New field / hook:** No new MDTM frontmatter. Pre-flight is environment-prep; consumes no checklist item.

**Dependencies:** TU-1 (consumes `Tier:` + Gate 1 dispatch — DM-10).

**Observable post-condition:** Task Log line `gate-1.5: pre-flight tier=<STRICT|STANDARD> ran=[serena, git, codebase-retrieval, memory]` (or `ran=[]` for LIGHT/EXEMPT). Where a tool unavailable: `skipped=[<tool>: not-available]`.

**Donor ceremony dropped (R-RULE-06):**
- **D15c per-tier procedure synthesis at execute-time — explicitly REJECTed** (auto-REJECT INV-01 + INV-05; ledger entry for Row 26). Pre-flight steps are pre-loop setup, never F1 EXECUTE items.
- Donor's "Layer 2" framing as a named runtime artifact — steps inlined as setup actions, no named layer.

**Bound manifest exceptions:**
- **ME-5 (CR-13 / Stack-rank Exception #5):** NO PER-ITEM EXECUTE SUBSTITUTION. Pre-flight is **additive pre-loop setup**, never in-EXECUTE behavior substitution. Any D15c-style per-item synthesis variant is auto-REJECT.

---

### TU-5 — TFEP Test baseline snapshot (D21, ADOPT)

**Donor row:** D21.
**Stack-rank row:** Row 8 (Net=6.0, ADOPT).

**Extension point:** Extension-point row 2 — First Item Protocol (C5). Co-attached with TU-4.

**Integration sketch:**
- Before F1 loop's first iteration: run `uv run pytest --collect-only -q` to collect test IDs, then `uv run pytest --tb=no -q` (or equivalent) to capture each test ID's PASS/FAIL state.
- Persist result to `research/test-baseline.yaml` — YAML schema: list of `{test_id, status}` records.
- This file is the **comparator** that TU-7 (D22 escalation classification) consumes on test failure.
- **Tier-gated to STRICT/STANDARD only** (ME-4 / CR-14) — LIGHT/EXEMPT skip baseline collection.

**Shape of change:** ~15 lines added to First Item Protocol.

**New field / hook:** No new MDTM frontmatter. New side-effect file: `research/test-baseline.yaml` (file-resident, INV-04 safe; resume-anchor for TU-7).

**Dependencies:** TU-1 (consumes `Tier:` for tier-gating — DM-6); TU-4 (TU-4 runs first at row 2 so serena/codebase-retrieval are warm before baseline collection).

**Observable post-condition:** File `research/test-baseline.yaml` exists on disk for STRICT/STANDARD tasks before F1's first iteration. Each subsequent test failure is classifiable pre-existing vs new by reading this file.

**Donor ceremony dropped (R-RULE-06):** None at the pattern level — TFEP baseline is absorbed as-is. The tier-gating constraint is recipient-imposed (uniform-cost-without-uniform-value failure mode would otherwise apply on LIGHT typo fixes).

**Bound manifest exceptions:**
- **ME-4 (CR-14 / Stack-rank Exception #4):** BASELINE TIER-GATED to STRICT/STANDARD. Uniform-baseline-on-every-task variant is auto-REJECT.

---

### TU-6 — TFEP Prohibitions (D19) + Permitted exceptions (D20)

**Donor rows:** D19 + D20.
**Stack-rank rows:** Row 2 (D19, Net=15.0, ADOPT) + Row 4 (D20, Net=10.0, ADOPT).
**Reason for co-transfer:** DM-8 — D20 carve-outs are exceptions to D19 prohibitions; co-located at the same extension point; D20 has no semantic without D19.

**Extension point:** Extension-point row 8 — Error Handling / blocker logging (`extension-point-contracts.md:123-131`; `SKILL.md:170-179`; C5).

**Integration sketch:**
- **D19 Prohibitions (~15 lines):** When a blocker is classified as a test failure, `tfep_prohibition_check` refuses three actions verbatim from `sc-task-protocol/SKILL.md:127-135`:
  1. **VIOLATION** — ad-hoc-fix the failing test without understanding the root cause.
  2. **VIOLATION** — modify test expectations to make a failure go away without adversarial validation.
  3. **VIOLATION** — produce a one-shot patch from test output alone (the "stop, look at the production code, escalate" rule).
  - Fourth note (routing rule, not VIOLATION): "test expectations are wrong is legitimate, but must be presented to user before mutating tests."
- **D20 Carve-outs (~10 lines, inside the D19 block):** Three exceptions verbatim from `sc-task-protocol/SKILL.md:137-140`:
  1. Single `ImportError` / `NameError` in test scaffolding the agent just wrote, ≤2 tests affected.
  2. Lint / formatting failures (formatter-handled; not behavioral).
  3. Deprecation warnings (not failures).
  - When the failure matches a carve-out, `tfep_prohibition_check` returns `allow`; F1 proceeds with normal blocker logging.

**New field / hook:** No new frontmatter. New side-channel hook: `tfep_prohibition_check(blocker_type) → {allow, refuse}`.

**Dependencies:** None upstream (TFEP cluster ADOPT subset entry point). Independent of `Tier:` field — prohibitions/carve-outs apply uniformly to all tasks on test-failure blockers.

**Observable post-condition:** Task Log lines:
- On refusal: `tfep: prohibition-refusal item=<id> rule=<VIOLATION-NN> reason=<reason>`. The failing item is **still** marked `- [x]` with its failure recorded via existing blocker logging — F1 continues (ME-3 / CR-12).
- On carve-out fire: `tfep: carve-out item=<id> rule=<carve-out-N> reason=<reason>`. No VIOLATION line written.

**Donor ceremony dropped (R-RULE-06):**
- Donor's seven-step TFEP-as-a-flow framing (cluster-as-written, Row 17 DEFER) is dropped. Only D19 + D20 are absorbed at row 8; D23 step 5/6 mutations are DEFERed; D25 "3-strike FULL STOP" budget is REJECTed (duplicates Phase-Gate QA's existing 3-cycle fix loop).
- Donor's F1-HALTING behavior on TFEP engagement is dropped (auto-REJECT under INV-01 per CR-12).

**Bound manifest exceptions:**
- **ME-3 (CR-12 / Stack-rank Exception #3):** SIDE-CHANNEL ONLY, NO F1 HALT. TFEP prohibition + classification + incident-report side-effects fire without halting F1. The failing item flips to `- [x]` (or records failure state via existing blocker logging); the F1 loop continues. Halting F1 on TFEP engagement is auto-REJECT under INV-01.

---

### TU-7 — TFEP Escalation trigger detection (D22, ADOPT)

**Donor row:** D22.
**Stack-rank row:** Row 9 (Net=6.0, ADOPT).

**Extension point:** Extension-point row 8 — Error Handling / blocker logging (C5). Co-located with TU-6.

**Integration sketch:**
- On test failure during F1, classify each failing test:
  - **Pre-existing:** test ID is in `research/test-baseline.yaml` (TU-5) AND was FAILING in baseline.
  - **New:** test ID is new OR was PASSING in baseline.
- Evaluate three MUST-escalate triggers verbatim from `sc-task-protocol/SKILL.md:200-210`:
  1. **Any pre-existing test fails after this task's changes** (regression).
  2. **≥3 new tests fail simultaneously** (systemic break).
  3. **Runtime exception in implementation code** (not test scaffolding) — broken behavior, not broken test.
- On any trigger fire: route to `rf-qa` for adjudication (existing INV-03 surface). D24 incident report (TU-8) is written at Post-Completion validation time IF the failure was resolved in-task.

**Shape of change:** ~15 lines added to Error Handling.

**New field / hook:** No new MDTM frontmatter. New side-channel hook: `tfep_escalation_check(failing_tests, baseline) → {trigger | none}`.

**Dependencies:** TU-5 (consumes baseline as comparator — DM-7); TU-6 (co-located at row 8, ordered after prohibition_check and carve_out_check).

**Observable post-condition:** Task Log: `tfep: escalation-trigger fired=<N> tests=[...] classification={pre-existing|new}`. If `rf-qa` adjudicates resolution, TU-8 writes the incident report at Post-Completion.

**Donor ceremony dropped (R-RULE-06):**
- Donor's "3-strike FULL STOP" escalation budget (D25) — REJECTed in ledger (Row 20); Phase-Gate QA's existing 3-cycle fix loop already provides this semantic. TU-7 routes to `rf-qa`, which uses the existing 3-cycle loop.

**Bound manifest exceptions:**
- **ME-3 (CR-12 / Stack-rank Exception #3):** SIDE-CHANNEL ONLY, NO F1 HALT (inherited from TFEP cluster).

---

### TU-8 — TFEP Incident reporting (D24, ADOPT)

**Donor row:** D24.
**Stack-rank row:** Row 5 (Net=10.0, ADOPT).

**Extension point:** Extension-point row 11 — Post-Completion Validation (`extension-point-contracts.md:151-159`; `SKILL.md:213-248`; C5).

**Integration sketch:**
- At TFEP-resolve time (D22 escalation triggered AND failure resolved in same task): write `research/tfep-incident-report.md` as a side-effect file.
- Post-Completion Validation confirms its presence for STRICT items with test-failure history.
- Donor schema preserved verbatim from `sc-task-protocol/SKILL.md:222-234`:
  - Trigger (which D22 trigger fired)
  - Escalation count (how many failures aggregated)
  - Failing tests (test IDs + pre-existing / new classification)
  - Root cause (free-form, agent-authored)
  - Solution (free-form)
  - Outcome (resolved / escalated-to-user)
  - Forensic artifacts (links to relevant phase-gate QA reports, baseline diff, etc.)

**Shape of change:** ~20 lines added (report template + Post-Completion check).

**New field / hook:** No new MDTM frontmatter. New side-effect file: `${TASK_DIR}research/tfep-incident-report.md`.

**Dependencies:** TU-5 + TU-6 + TU-7 (DM-9 — incident-report records the side-effects of the TFEP cluster firing).

**Observable post-condition:** File `research/tfep-incident-report.md` exists on disk for STRICT items where D22 escalation fired during the task. Post-Completion Validation reads the file and verifies the seven-field schema is populated; missing-field → validation failure routed to `rf-qa`.

**Donor ceremony dropped (R-RULE-06):**
- **D23 Step 5 — "insert `## Failure Remediation Plan (Adjudicated)` heading into the task file"** — REJECTed at this attach surface (F4-violation; modifies task structure outside DYNAMIC CONTENT MARKER). Incident reporting writes a side-effect FILE, never an in-task heading. Heading insertion is part of D23 DEFER (Row 23 — pending `/sc:forensic` + Step 5 redesign).
- **D23 Step 6 — "resume from the inserted task"** — REJECTed at this attach surface (INV-01 violation; IDENTIFY would read items the loop didn't author). Part of D23 DEFER.

**Bound manifest exceptions:**
- **ME-3 (CR-12 / Stack-rank Exception #3):** SIDE-CHANNEL ONLY (file write at Post-Completion, no F1 mutation).
- **Tier-gated to STRICT items with test-failure history** (transitively inherits ME-4 via TU-5 dependency).

---

## 3. Manifest Exceptions Register (R-RULE-07, binding)

Each exception is a load-bearing INV-safety commitment that Phase 6 / Phase 7 may not relax. Variants violating these exceptions are auto-REJECT and must NOT be silently re-proposed downstream (R-RULE-11).

| ID | Title | Binds | Source | INV protected | Justification (named) |
|---|---|---|---|---|---|
| ME-1 | PRE-LOOP DISPATCH ONLY | TU-1 (Gate 1) | CR-10 / `stack-rank.md:239` | INV-01 | Per-item per-tier dispatch re-evaluates loop control at each iteration. Auto-REJECT. |
| ME-2 | `rf-qa` SUPPLEMENTED NOT REPLACED | TU-3 (Gate 2) | CR-11 / `stack-rank.md:240` | INV-03 | `quality-engineer` is *additional* on STRICT, never a replacement. Replacing `rf-qa`'s adversarial stance is auto-REJECT. |
| ME-3 | SIDE-CHANNEL ONLY, NO F1 HALT | TU-6, TU-7, TU-8, TU-5 | CR-12 / `stack-rank.md:241` | INV-01 | TFEP fires its side-effects without halting F1. The failing item flips to `- [x]` (or records via blocker logging); F1 continues. Halting variant is auto-REJECT. |
| ME-4 | BASELINE TIER-GATED | TU-5 | CR-14 / `stack-rank.md:242` | (R-RULE-06 adjacent) | Baseline collection runs only on STRICT/STANDARD. Uniform-baseline-on-every-task falls cost on LIGHT typo fixes (uniform-cost-without-uniform-value). Auto-REJECT. |
| ME-5 | NO PER-ITEM EXECUTE SUBSTITUTION | TU-4 (D15b); explicitly REJECTs D15c | CR-13 / `stack-rank.md:243` | INV-01 + INV-05 | Pre-flight is additive pre-loop setup; D15c synthesis variant generates runtime checklist items the loop did not READ from disk. Auto-REJECT. |
| ME-6 | TIER FIELD + GATE 1 SHIP TOGETHER | TU-1 | CR-9 / `stack-rank.md:244` | (R-RULE-06) | D09a alone is inert metadata. Gate 1 alone has no dispatch input. Ship together or ship neither. |
| ME-7 | D08 DEFERRED UNTIL PARSER SHIPS | Ledger row 19 | CR-15 / `stack-rank.md:245` | (R-RULE-06) | Adopting classification header in isolation repeats the R-RULE-06 ceremony-without-teeth failure that REJECTed D02/Layer A. Carry in ledger as DEFER precondition. |
| ME-8 | D01 DEFERRED UNTIL LOADER SEMANTICS + RULE 6 SPLIT | Ledger row 18 | CR-16 / `stack-rank.md:246` | (R-RULE-06) | Adopting `allowed-tools:` without verifying loader honor-semantics creates ceremony-without-teeth. Carry in ledger with two-clause precondition. |
| ME-9 | D02/LAYER A REJECT (R-RULE-06 override of arithmetic DEFER) — RE-AFFIRMED | Ledger row 13 | CR-6 / `stack-rank.md:131` + `:249` | (R-RULE-06) | **Subjective override.** Arithmetic Net=2.5 falls in DEFER band, but verdict is REJECT under R-RULE-06 (no in-repo consumer for `mcp-servers:` frontmatter list). Phase 5 reviewer **re-affirms** this override per R-RULE-07: subjective overrides must be explicit, named, re-affirmable, and survive the manifest's terminal lock. Named justification: ceremony-without-behavioral-teeth; no consumer in the recipient package for the advertised MCP list. |

**Total manifest exceptions:** 9 (8 mechanical INV/R-RULE-06 bindings + 1 subjective override re-affirmation).

---

## 4. Coverage Audit — 1:1 partition with Phase 4 verdict set

Every Phase 4 stack-rank row appears in exactly one of {transfer manifest, rejected features ledger}. No orphans, no duplicates.

**Manifest entries (this file) — 15 distinct stack-rank rows referenced** (12 primary ADOPT/ADAPT + 3 catalog-derived subsumption rows):

| Stack-rank row | Donor ID | Disposition in manifest | TU |
|---|---|---|---|
| 1 | D17 + D18 | ADOPT (TU-2) | TU-2 |
| 2 | D19 | ADOPT (TU-6) | TU-6 |
| 3 | D09a | ADOPT (TU-1) | TU-1 |
| 4 | D20 | ADOPT (TU-6) | TU-6 |
| 5 | D24 | ADOPT (TU-8) | TU-8 |
| 6 | D04 / cluster Gate 1 | ADOPT (TU-1) | TU-1 |
| 7 | D10 | ADOPT (donor-traceability — folded into TU-1) | TU-1 (annotation) |
| 8 | D21 | ADOPT (TU-5) | TU-5 |
| 9 | D22 | ADOPT (TU-7) | TU-7 |
| 10 | cluster Gate 2 | ADAPT (TU-3) | TU-3 |
| 11 | D15a | ADAPT (donor-traceability — folded into TU-3) | TU-3 (annotation) |
| 12 | D15b | ADAPT (TU-4) | TU-4 |
| 34 (catalog) | D16 | ADAPTABLE-subsumed into Gate 2 | TU-3 (donor-traceability) |
| 35 (catalog) | D17 | TRANSFERABLE-subsumed into Path Override | TU-2 (donor-traceability) |
| 36 (catalog) | D18 | TRANSFERABLE-subsumed into Path Override | TU-2 (donor-traceability) |

**Ledger entries (companion file) — 27 stack-rank rows referenced** (Row 15 and Row 16 are one feature with two views, counted once = 26 distinct entries):

| Stack-rank rows | Disposition |
|---|---|
| 13 (D02/Layer A) | REJECT — R-RULE-06 override (re-affirmed via ME-9) |
| 14 (Compliance cluster aggregate) | DEFER — terminal |
| 15 + 16 (D27/Layer B + Gate 3) | DEFER — re-debate authorized in CR-3 (one entry, two views) |
| 17 (TFEP cluster aggregate) | DEFER — terminal |
| 18 (D01) | DEFER — two-clause precondition (ME-8) |
| 19 (D08) | DEFER — parser-ships precondition (ME-7) |
| 20 (D25) | REJECT — duplicates Phase-Gate QA |
| 21 (D09b) | REJECT — R-RULE-06 structural mismatch (route to `task-builder`) |
| 22 (Gate 5 Override flags) | REJECT — silent-misuse failure mode |
| 23 (D23 six-step flow) | DEFER — three-clause precondition |
| 24 (D03 Persona) | REJECT — R-RULE-05 INV violations + R-RULE-06 |
| 25 (D13 Auto-suggest) | REJECT — no `/task` consumer |
| 26 (D15c) | REJECT — R-RULE-05 INV-01 + INV-05 collision |
| 27 (D06 Auto-trigger) | REJECT — R-RULE-05 INV-05; donor-rec REJECT |
| 28 (D04 Strategy axis) | REJECT — no F1 analog |
| 29 (D05 Escalation philosophy) | REJECT — philosophy statement, no attach point |
| 30 (D07 Flag set) | REJECT — `/task` is Skill-invoked, not CLI |
| 31 (D11 Classification examples) | REJECT — supports D08/D09 only |
| 32 (D12 Cmd-side boundaries) | REJECT — duplicates F2 + F4 |
| 33 (D14 Confidence display) | DEFER — D08 ADOPTs + non-D09b classifier source |
| 37 (D26 Feedback Collection) | DEFER — calibration store authored |
| 38 (D28 Tool Coordination) | REJECT — duplicates F1 EXECUTE + Critical Rule 6 + Phase-Gate QA |
| 39 (D29 Worked Examples) | REJECT — supports D09/D10/D15 only |
| 40 (D30 Skill-side boundaries) | REJECT — duplicates D12 + F2 |
| 41 (D31 Success metrics) | REJECT — metrics measure REJECTed/DEFERed features |
| 42 (D32 External config refs) | DEFER — tier-keyword YAML producer authored |

**Total stack-rank rows accounted: 15 (manifest) + 27 (ledger) = 42** ✅ matches `stack-rank.md` § Coverage Audit (32 donor catalog rows → 42 stack-rank rows after sub-splits and cluster sub-gate views).

**No orphans, no duplicates.** Every donor catalog row D01-D32 lives in exactly one of the two documents (manifest or ledger).

---

## 5. Build-order rule for Phase 6

Phase 6 (merge plan) and Phase 7 (merge execution) must respect this ordering at the source-tree level:

1. **TU-1 lands first** (D09a `Tier:` field + Gate 1 dispatch — single ship-together unit per ME-6).
2. **TU-2 lands in same merge as TU-1** (Path Override — runtime ordering at row 1 / row 10 must hold atomically; recommended same merge).
3. **TU-3, TU-4, TU-5** can land in any order after TU-1 (they all depend on TU-1's `Tier:` field + Gate 1 dispatch).
4. **TU-6 can land independently** (no dependency on TU-1; TFEP prohibitions/carve-outs apply to all test-failure blockers).
5. **TU-7 must land after TU-5** (consumes baseline as comparator — DM-7).
6. **TU-8 must land after TU-5 + TU-6 + TU-7** (records the side-effects of the TFEP cluster — DM-9).

**At runtime, the integration-ordering constraints (CR-7 / CR-8) are enforced inside the SKILL.md edits themselves** — `path_override_check → tier_field_validate → gate_1_dispatch` at row 1; `path_override_check → gate_2_stance_select` at row 10. Phase 6 must verify the inserted code preserves this order.

---

## 6. Acceptance Criteria Recap (T05.03)

1. **`transfer-manifest.md` exists, lists every ADOPT/ADAPT feature in dependency-respecting execution order, each with sketch/modification, dependencies, and observable post-condition.** ✅ — Section 1 lists 8 transfer units in dependency-respecting execution order; Section 2 provides for each: donor row(s), extension point(s), integration sketch (ADOPT) or modification (ADAPT), new field/hook, dependencies, observable post-condition, donor ceremony dropped, bound manifest exceptions.

2. **`rejected-features-ledger.md` exists, lists every REJECT (terminal rationale) and DEFER (precondition) feature.** ✅ — Companion file `rejected-features-ledger.md` lists 26 ledger entries: 8 primary REJECT, 9 catalog-derived REJECT, 6 primary DEFER (Row 14, 15+16, 17, 18, 19, 23 — counting 15-16 once), 3 catalog-derived DEFER. Verbatim CR rationales carry forward per integration-sketches § 7.3.

3. **Every Phase 4 donor feature appears in exactly one of the two documents — no orphans, no duplicates.** ✅ — Section 4 coverage audit confirms 15 manifest references + 27 ledger references = 42 stack-rank rows = all 32 donor catalog rows accounted exactly once.

4. **Any subjective override is recorded as a "manifest exception" with named justification (R-RULE-07).** ✅ — Section 3 lists 9 manifest exceptions. ME-9 (D02/Layer A REJECT — arithmetic-vs-override divergence) is the **one subjective override** in the sprint, explicitly re-affirmed in Phase 5 with the named justification "ceremony-without-behavioral-teeth; no consumer in the recipient package for the advertised MCP list." Exceptions ME-1 through ME-8 are mechanical INV/R-RULE-06 bindings carried forward verbatim from `stack-rank.md` § "Phase 5 forwarded items."

---

**T05.03 deliverable: COMPLETE.** Phase 6 (merge plan) has the binding transfer manifest as its driving input. Phase 7 (merge execution) has 8 transfer units in locked execution order, 9 binding manifest exceptions, and the companion ledger ensuring no REJECT/DEFER feature is silently re-proposed downstream.

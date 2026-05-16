# Integration Sketches — Phase 5 Synthesis

**Task:** T05.02 — Lock integration sketches, ADAPT modifications, DEFER preconditions
**Roadmap Item:** R-017
**Tier:** STANDARD
**Generated:** 2026-05-15
**Inputs:**
- `stack-rank.md` (T04.05) — 12 ADOPT/ADAPT rows + 7 primary DEFER rows + 3 catalog-derived DEFER rows.
- `feature-dependency-matrix.md` (T05.01) — 11 DM entries + 16 CR entries (`CR-1`…`CR-16`).
- `extension-point-contracts.md` (T03.02) — 19 positive-space extension-point contracts (rows 1-19) + 3 negative-space (N1-N3) C1 auto-REJECT surfaces. Each carries explicit Admit / Reject criteria and the INV-NN it protects.
- Recipient evidence anchor: `src/superclaude/skills/task/SKILL.md` (R-RULE-10 — the `.claude/` mirror is byte-identical and is NOT the attach target).

**Purpose:** For every ADOPT feature, lock the integration sketch — exact extension point, shape of change, any new MDTM frontmatter field or hook introduced, observable post-condition. For every ADAPT feature, define the explicit modification — what changes versus the donor implementation, what donor ceremony is dropped (R-RULE-06), what control pattern is retained. For every DEFER feature, name the precondition that would re-enable it. Confirm every ADOPT sketch respects the admit criteria of its target extension point and breaks no INV-NN.

**Binding constraints encoded below (from `feature-dependency-matrix.md` § 7):**
- CR-7: Task File Validation surface order — `path_override_check → tier_field_validate → gate_1_dispatch`.
- CR-8: Phase-Gate QA surface order — `path_override_check → gate_2_stance_select`.
- CR-9: D09a (`Tier:` field) + Gate 1 — single transfer unit ("ship together or ship neither").
- CR-10: Gate 1 + D10 — PRE-LOOP DISPATCH only; per-item variant auto-REJECT (INV-01).
- CR-11: Gate 2 + D15a — `quality-engineer` SUPPLEMENTS, never replaces, `rf-qa` (INV-03).
- CR-12: TFEP ADOPT subset (D19/D20/D21/D22/D24) — SIDE-CHANNEL ONLY, NO F1 HALT (INV-01).
- CR-13: D15b — pre-loop additive only; D15c per-item synthesis variant auto-REJECT (INV-05).
- CR-14: D21 (TFEP Baseline) — TIER-GATED to STRICT/STANDARD; uniform-baseline variant auto-REJECT.

**1:1 verdict coverage with Phase 4 (`stack-rank.md` § Primary Stack Rank + Catalog-derived dispositions):** 9 ADOPT + 3 ADAPT + 7 DEFER (primary) + 3 DEFER (catalog-derived: rows 33/37/42) = 22 entries below.

---

## 1. ADOPT — Locked Integration Sketches (9 features)

Each ADOPT sketch declares: **(a)** exact extension point (row in `extension-point-contracts.md`, the SKILL.md anchor, and C-band); **(b)** shape of change (size + location); **(c)** new MDTM frontmatter field or hook introduced (if any); **(d)** observable post-condition (the disk-resident evidence that proves the feature fired); **(e)** admit-criteria match against the target extension point; **(f)** INV-NN audit — no INV broken; **(g)** bound manifest exceptions / CR constraints.

### IS-ADOPT-1 — Critical/Trivial Path Override (Row 1, D17 + D18, V=4 C=5 K=1 Net=20.0)

- **(a) Extension point(s):** Two attach surfaces.
  1. Extension-point row 1 — Task File Validation gate (`extension-point-contracts.md:60-67`; `SKILL.md:64-73`; **C5**).
  2. Extension-point row 10 — Phase-Gate QA Verification (`extension-point-contracts.md:141-149`; `SKILL.md:182-211`; **C3**).
- **(b) Shape of change:**
  - At extension-point row 1: ~10 lines added to `SKILL.md` Task File Validation block — a `path_override_check` step that resolves the task's target file paths against two glob sets.
  - At extension-point row 10: ~5 lines added to Phase-Gate QA stance selection — read the forced-stance flag set by (1) and force-escalate / force-de-escalate accordingly.
  - **Critical path-glob set** (forces STRICT regardless of `Tier:` value): `auth/`, `security/`, `crypto/`, `models/`, `migrations/` (sourced from `src/superclaude/skills/sc-task-protocol/SKILL.md:121`).
  - **Trivial path-glob set** (forces LIGHT only if task touches NO files outside the set): `*.md`, `docs/`, `*test*.py` (sourced from `sc-task-protocol/SKILL.md:123`).
- **(c) New field / hook:** No new MDTM frontmatter field. New hook: `path_override_check` (pure read, no file mutation). It sets an in-memory `forced_stance` flag consumed by Gate 1 (Row 6, IS-ADOPT-6) and Gate 2 (Row 10, IS-ADAPT-1).
- **(d) Observable post-condition:** A single line written to `## Task Log / Notes` recording the path-override outcome: `path-override: forced_stance=STRICT (matched: auth/foo.py)` OR `path-override: forced_stance=LIGHT (all paths inside trivial-glob set)` OR `path-override: no-match (forced_stance=none)`. Post-completion validation can inspect this line in STRICT items.
- **(e) Admit-criteria match:** Row 1 admits pre-loop validators that produce user-facing diagnostics and do not mutate the task file; Row 10 admits between-phase gate logic that widens stance selection. Both are satisfied — the override is pure-read at the gate, append-only at the Task Log.
- **(f) INV-NN audit:** No INV broken. Path-override does not mutate the task file mid-loop (INV-01 / INV-02 / F4 safe), does not decide what work to do (INV-05 — it only forces a budget shape), does not bypass `rf-qa` (INV-03 — Phase-Gate QA still runs; the override widens or narrows the budget, never replaces the verifier).
- **(g) Constraints bound:** CR-7 / CR-8 — fires FIRST on both surfaces, before tier-field validate and before Gate 2 stance select.

### IS-ADOPT-2 — TFEP Prohibition rules (Row 2, D19, V=3 C=5 K=1 Net=15.0)

- **(a) Extension point:** Extension-point row 8 — Error Handling / blocker logging (`extension-point-contracts.md:123-131`; `SKILL.md:170-179`; **C5**).
- **(b) Shape of change:** ~15 lines added to the Error Handling block. When a blocker is classified as a test failure, a `prohibition_check` step refuses three actions verbatim from donor `SKILL.md:127-135`:
  1. VIOLATION — ad-hoc-fix the failing test without understanding the root cause.
  2. VIOLATION — modify test expectations to make a failure go away without adversarial validation.
  3. VIOLATION — produce a one-shot patch from test output alone (the "stop, look at the production code, escalate" rule).
  - A fourth note (not a VIOLATION) — "test expectations are wrong is legitimate, but must be presented to user before mutating tests" — is captured as a routing rule.
- **(c) New field / hook:** No new frontmatter field. New side-channel hook: `tfep_prohibition_check(blocker_type) → {allow, refuse}`; refusals route the failing item to recorded-failure state via existing blocker logging.
- **(d) Observable post-condition:** A line in `## Task Log / Notes` recording the prohibition fire: `tfep: prohibition-refusal item=<id> rule=<VIOLATION-NN> reason=<reason>`. The failing item is **still** marked `- [x]` with its failure recorded — F1 continues (CR-12).
- **(e) Admit-criteria match:** Row 8 admits new blocker classification + recovery-strategy + blocker-logging formats that preserve "items NEVER left unchecked" and log to Task Log. Satisfied — TFEP prohibition writes a Task Log entry and uses the existing blocker-logging surface.
- **(f) INV-NN audit:** INV-01 safe (F1 loop does not halt — CR-12); INV-02 safe (the failing item is logged, not skipped or modified); INV-04 safe (Task Log entries are incremental writes); INV-05 safe (TFEP does not redefine what the failing item is — it refuses *how* to fix it).
- **(g) Constraints bound:** CR-12 — SIDE-CHANNEL ONLY, NO F1 HALT.

### IS-ADOPT-3 — D09a `Tier:` field schema extension (Row 3, V=4 C=5 K=2 Net=10.0)

- **(a) Extension point(s):** Three attach surfaces, all C5.
  1. Extension-point row 13 — Required frontmatter schema slot (`extension-point-contracts.md:169-175`; `SKILL.md:69`). Add optional `Tier:` field accepting `{STRICT, STANDARD, LIGHT, EXEMPT}`.
  2. Extension-point row 1 — Task File Validation gate. Validator closed-enum check when `Tier:` is present.
  3. Extension-point row 4 — F1 EXECUTE item-type dispatch (`extension-point-contracts.md:86-94`; `SKILL.md:89-96`; **C3** if dispatch is widened, **C5** if read is purely additive). Per-item annotation `Tier: LIGHT` (etc.) is read when present, falling back to task-level `Tier:`.
- **(b) Shape of change:** ~3-5 lines added to the frontmatter requirements list; ~5-10 lines added to the Task File Validation gate's closed-enum check; ~3 lines added to F1 EXECUTE for the per-item fallback read.
- **(c) New field / hook:** **NEW MDTM FRONTMATTER FIELD** — `Tier:` (optional, closed-enum `{STRICT, STANDARD, LIGHT, EXEMPT}`). Per-item annotation supported as inline marker on a checklist item (e.g., `- [ ] (Tier: LIGHT) trivial typo fix`), with task-level `Tier:` as fallback.
- **(d) Observable post-condition:** Validator-resident — when present, `Tier:` is closed-enum-checked at task entry; when malformed, the validator emits a refusal diagnostic. When absent, defaults are documented (no value → "unclassified", which Gate 1 (IS-ADOPT-6) handles as STANDARD).
- **(e) Admit-criteria match:** Row 13 admits new required-metadata fields validated by row 1's pre-loop validator. Row 4 admits a new item-action verb whose meaning is fully encoded inside a single item with verifiable on-disk evidence. Satisfied on both — `Tier:` is pure metadata at row 13 (no work-definition leak), and the per-item annotation at row 4 is purely additive.
- **(f) INV-NN audit:** INV-01 safe (no loop control change — `Tier:` value affects budget, not the next item to execute); INV-05 safe (the field is metadata, it does not redefine "what work to do" — the checklist still owns work definition).
- **(g) Constraints bound:** CR-9 — D09a + Gate 1 ship as a single transfer unit; this sketch is locked to the same transfer unit as IS-ADOPT-6. CR-7 — at the Task File Validation surface, the closed-enum check fires AFTER `path_override_check` and BEFORE Gate 1 dispatch.

### IS-ADOPT-4 — TFEP Permitted exceptions (Row 4, D20, V=2 C=5 K=1 Net=10.0)

- **(a) Extension point:** Extension-point row 8 — Error Handling / blocker logging (**C5**). Co-located with IS-ADOPT-2 (Row 2 / D19 prohibitions) and IS-ADOPT-9 (Row 9 / D22 escalation triggers).
- **(b) Shape of change:** ~10 lines added inside the D19 prohibition block (IS-ADOPT-2), declaring the three carve-outs verbatim from donor `SKILL.md:137-140`:
  1. Single `ImportError` / `NameError` in test scaffolding the agent just wrote, with ≤2 tests affected.
  2. Lint / formatting failures (handled by formatter; not a behavioral failure).
  3. Deprecation warnings (not failures).
- **(c) New field / hook:** No new frontmatter. The `tfep_prohibition_check` hook (introduced in IS-ADOPT-2) consults this list before deciding `{allow, refuse}`. If the failure matches a carve-out, `allow` returns and F1 proceeds with normal blocker logging (no prohibition VIOLATION written).
- **(d) Observable post-condition:** When a carve-out fires, the Task Log line is: `tfep: carve-out item=<id> rule=<carve-out-N> reason=<reason>`. No VIOLATION line written.
- **(e) Admit-criteria match:** Row 8 admits new failure-routing policies inside the existing taxonomy. Satisfied.
- **(f) INV-NN audit:** INV-01 / INV-02 / INV-04 / INV-05 all safe (same reasoning as IS-ADOPT-2 — carve-outs are *narrower* than prohibitions, never broader).
- **(g) Constraints bound:** DM-8 — carve-outs co-located with prohibitions (Row 2). CR-12 — SIDE-CHANNEL ONLY.

### IS-ADOPT-5 — TFEP Incident reporting (Row 5, D24, V=2 C=5 K=1 Net=10.0)

- **(a) Extension point:** Extension-point row 11 — Post-Completion Validation (`extension-point-contracts.md:151-159`; `SKILL.md:213-248`; **C5** for additive analyzers).
- **(b) Shape of change:** ~20 lines added. At TFEP-resolve time (when D22 escalation triggered AND the failure was resolved in the same task), write `research/tfep-incident-report.md` as a side-effect file in the task's research/ subdirectory. Post-Completion Validation confirms its presence for STRICT items with test-failure history. Donor schema preserved verbatim from `SKILL.md:222-234`:
  - Trigger (which D22 trigger fired)
  - Escalation count (how many failures aggregated)
  - Failing tests (test IDs + pre-existing / new classification)
  - Root cause (free-form, agent-authored)
  - Solution (free-form)
  - Outcome (resolved / escalated-to-user)
  - Forensic artifacts (links to relevant phase-gate QA reports, baseline diff, etc.)
- **(c) New field / hook:** No new MDTM frontmatter. New side-effect file: `${TASK_DIR}research/tfep-incident-report.md`.
- **(d) Observable post-condition:** File `research/tfep-incident-report.md` exists on disk for STRICT items where D22 escalation fired during the task. Post-Completion Validation reads the file and verifies the seven-field schema is populated; missing-field → validation failure routed to `rf-qa`.
- **(e) Admit-criteria match:** Row 11 admits new whole-task validation capability layered on the existing `rf-qa` / `rf-qa-qualitative` pair. Satisfied — incident reporting is additive validation, not replacement.
- **(f) INV-NN audit:** INV-03 safe (does not bypass `rf-qa` — adds a Post-Completion check); INV-04 safe (file-resident, recoverable on resume).
- **(g) Constraints bound:** DM-9 — requires TFEP cluster ADOPT subset (D19/D20/D21/D22) to have fired. **Tier-gated**: only required for STRICT items with test-failure history (transitively inherits CR-14 via dependency on Baseline D21). **Donor ceremony explicitly dropped**: the donor's "## Failure Remediation Plan (Adjudicated)" *heading-insertion* (Step 5 of D23) is NOT part of this sketch — incident reporting writes a side-effect FILE, never an in-task heading. Heading insertion is in Row 23 (DEFER; pending `/sc:forensic`).

### IS-ADOPT-6 — Compliance-gating Gate 1 (Dispatch task-entry) (Row 6, D04 / cluster, V=3 C=5 K=2 Net=7.5)

- **(a) Extension point:** Extension-point row 1 — Task File Validation gate (**C5**), co-located with IS-ADOPT-1 (Path Override) and IS-ADOPT-3 (D09a Tier validate).
- **(b) Shape of change:** ~10-15 lines added to the validation gate's dispatch logic. After validation passes, read the effective stance (which is `forced_stance` if path-override set it, else `Tier:` value, else `STANDARD` default for an unclassified task). Dispatch:
  - `LIGHT` / `EXEMPT` → lightweight profile: skip TFEP baseline (CR-14), skip D15b pre-flight scaffolding, run F1 with reduced Phase-Gate QA budget; Post-Completion Validation still fires (INV-03 floor).
  - `STANDARD` → existing budget profile: F1 + Phase-Gate QA (~existing budget) + Post-Completion Validation.
  - `STRICT` → full profile: F1 + D15b pre-flight scaffolding (IS-ADAPT-3) + TFEP baseline (IS-ADOPT-8) + Phase-Gate QA with widened budget (IS-ADAPT-1) + Post-Completion Validation including TFEP incident-report check (IS-ADOPT-5).
- **(c) New field / hook:** No new frontmatter (consumes `Tier:` from IS-ADOPT-3). New hook: `gate_1_dispatch(forced_stance, tier_value) → execution_profile`, returning the profile selected above. The profile is captured as an in-memory state, NOT written to the task file.
- **(d) Observable post-condition:** A single line written to `## Task Log / Notes`: `gate-1: dispatch_profile=<STRICT|STANDARD|LIGHT|EXEMPT> source=<path-override|tier-field|default>`. STRICT-only side-effect files (baseline, incident report) appear in `research/` if and only if dispatch fired the STRICT profile.
- **(e) Admit-criteria match:** Row 1 admits pre-loop validators with user-facing diagnostics. Gate 1 is *post*-validation but *pre*-loop, so it fits the row 1 contract. Satisfied.
- **(f) INV-NN audit:** INV-01 critical — dispatch fires **ONCE at task entry**, **never per-item** (CR-10). Per-item per-tier dispatch is auto-REJECT under INV-01 (would mean re-evaluating loop control at each iteration). INV-03 safe — even LIGHT/EXEMPT retain Post-Completion Validation (the lightweight Phase-Gate QA still runs; only the budget is narrowed — never bypassed). INV-04 safe — dispatch state is reconstructable on resume (re-evaluate `Tier:` and `path_override` from disk).
- **(g) Constraints bound:** CR-9 (single transfer unit with IS-ADOPT-3); CR-10 (PRE-LOOP DISPATCH only); CR-7 (fires AFTER path-override and AFTER tier-field validate).

### IS-ADOPT-7 — D10 Command-side dispatch (Row 7, ADOPT MERGE-WITH-GATE-1)

- **(a) Extension point:** Same as IS-ADOPT-6 — extension-point row 1.
- **(b) Shape of change:** **Zero net implementation work in Phase 6.** Donor D10 ("command-side dispatch") and Gate 1 (donor D04, recipient-side dispatch) collapse to the same surface in the merged form: the validation gate inside `task/SKILL.md` dispatches by `Tier:`. The donor's separate command-side layer (a layer of dispatch *before* the skill is invoked) is not preserved because `/task` is Skill-invoked on a file path in the recipient model — there is no command-side surface to attach to.
- **(c) New field / hook:** None (subsumed into IS-ADOPT-6).
- **(d) Observable post-condition:** Identical to IS-ADOPT-6 — no separate evidence file.
- **(e) Admit-criteria match:** N/A (no new attachment).
- **(f) INV-NN audit:** N/A.
- **(g) Constraints bound:** This row exists in the manifest **for donor traceability only** — it records that D10's pattern was absorbed but its donor-side ceremony (separate command-layer dispatch) was dropped per R-RULE-06.

### IS-ADOPT-8 — TFEP Test baseline snapshot (Row 8, D21, V=3 C=4 K=2 Net=6.0)

- **(a) Extension point:** Extension-point row 2 — First Item Protocol / pre-loop status init (`extension-point-contracts.md:69-75`; `SKILL.md:100-102`; **C5**).
- **(b) Shape of change:** ~15 lines added to First Item Protocol. Before the F1 loop's first iteration, run `uv run pytest --collect-only -q` once to collect test IDs, then `uv run pytest --tb=no -q` (or equivalent) to capture each test ID's PASS/FAIL state. Persist the result to `research/test-baseline.yaml` (YAML schema: list of `{test_id, status}` records). This is the *comparator* for D22 escalation classification (IS-ADOPT-9).
- **(c) New field / hook:** No new MDTM frontmatter. New side-effect file: `research/test-baseline.yaml` (file-resident, INV-04 safe).
- **(d) Observable post-condition:** File `research/test-baseline.yaml` exists on disk for STRICT/STANDARD tasks before F1's first iteration begins. Each subsequent test failure during F1 can be classified pre-existing vs new by reading this file.
- **(e) Admit-criteria match:** Row 2 admits session-init / environment-prep actions that run once before the loop's first iteration. Satisfied — baseline collection is pure-init, writes to `research/`, and consumes no checklist item.
- **(f) INV-NN audit:** INV-01 safe (no checklist consumption); INV-04 safe (file is the resume-anchor for D22); INV-05 safe (does not decide what work to do).
- **(g) Constraints bound:** CR-14 — TIER-GATED to STRICT/STANDARD; uniform-baseline-on-every-task variant is auto-REJECT (LIGHT typo fixes don't pay the baseline cost). DM-6 — depends on IS-ADOPT-3 (`Tier:` field) + IS-ADOPT-6 (Gate 1 dispatch) being in place.

### IS-ADOPT-9 — TFEP Escalation trigger detection (Row 9, D22, V=3 C=4 K=2 Net=6.0)

- **(a) Extension point:** Extension-point row 8 — Error Handling / blocker logging (**C5**). Co-located with IS-ADOPT-2 (D19), IS-ADOPT-4 (D20).
- **(b) Shape of change:** ~15 lines added to Error Handling. On a test failure during F1, classify each failing test as **Pre-existing** (test ID is in `research/test-baseline.yaml` from IS-ADOPT-8 and was FAILING in baseline) or **New** (test ID is new OR was PASSING in baseline). Evaluate the three MUST-escalate triggers (verbatim from donor `SKILL.md:200-210`):
  1. **Any pre-existing test fails after this task's changes** — implies regression.
  2. **≥3 new tests fail simultaneously** — implies systemic break.
  3. **Runtime exception in implementation code** (not test scaffolding) — implies broken behavior, not broken test.
  - On any trigger fire: route to `rf-qa` for adjudication (existing INV-03 surface); D24 incident report (IS-ADOPT-5) is written at Post-Completion validation time IF the failure was resolved in-task.
- **(c) New field / hook:** No new MDTM frontmatter. New side-channel hook: `tfep_escalation_check(failing_tests, baseline) → {trigger | none}`; trigger routes to `rf-qa` adjudication.
- **(d) Observable post-condition:** A Task Log line `tfep: escalation-trigger fired=<N> tests=[...] classification={pre-existing|new}`. If `rf-qa` adjudicates resolution, the incident report (IS-ADOPT-5) is written at Post-Completion.
- **(e) Admit-criteria match:** Row 8 admits new blocker classification + failure-routing policies. Satisfied.
- **(f) INV-NN audit:** INV-01 safe (CR-12 — no F1 halt; the failing item is logged, F1 continues to next); INV-03 safe (`rf-qa` adjudicates — adversarial stance preserved); INV-04 safe (baseline + Task Log lines are file-resident).
- **(g) Constraints bound:** DM-7 — depends on IS-ADOPT-8 having executed (the baseline is the comparator); CR-12 — SIDE-CHANNEL ONLY, NO F1 HALT. **Donor ceremony explicitly dropped (R-RULE-06):** the donor's "3-strike FULL STOP" escalation budget (D25) is NOT part of this sketch — D25 is REJECTed (Row 20) because Phase-Gate QA's existing 3-cycle fix loop already provides this semantic. IS-ADOPT-9 routes to `rf-qa`, which uses the existing 3-cycle loop.

---

## 2. ADAPT — Explicit Modifications (3 features)

Each ADAPT spec declares: **(a)** target extension point + C-band; **(b)** what changes vs the donor; **(c)** what donor ceremony is dropped (R-RULE-06); **(d)** what control pattern is retained; **(e)** observable post-condition; **(f)** admit-criteria match + INV-NN audit; **(g)** bound manifest exceptions.

### IS-ADAPT-1 — Compliance-gating Gate 2 — Verification routing (Row 10, V=4 C=3 K=3 Net=4.0)

- **(a) Extension point:** Extension-point row 10 — Phase-Gate QA Verification (`extension-point-contracts.md:141-149`; `SKILL.md:182-211`; **C3**).
- **(b) What changes vs donor:**
  - **Donor form:** A separate "Verification Routing Layer" that owns the choice of verifier and substitutes verifier identity per tier (e.g., STRICT → `quality-engineer` instead of donor's default verifier).
  - **Recipient form:** Phase-Gate QA is *widened*, not routed. The existing `rf-qa` adversarial-stance verifier always runs (INV-03 floor). Tier conditions a **budget + roster widening**:
    - STRICT: ~5K token budget, 60s timeout, AND `quality-engineer` added to the roster as an *additional* adversarial verifier alongside `rf-qa`.
    - STANDARD: existing budget, `rf-qa` only.
    - LIGHT/EXEMPT: reduced budget (~1.5K, 20s), `rf-qa` only.
  - Path-override consulted FIRST (CR-8): if `forced_stance=STRICT` due to a critical-path-glob match, the STRICT profile applies regardless of `Tier:` value; if `forced_stance=LIGHT` due to trivial-path-glob match, the LIGHT profile applies.
- **(c) Donor ceremony dropped (R-RULE-06):**
  - Donor's "replace `rf-qa` with `quality-engineer` for STRICT" semantic is dropped — replacement is auto-REJECT under INV-03 (CR-11).
  - Donor's separate "verification routing table" as a standalone configuration block is dropped — the recipient inlines the tier→budget mapping in the Phase-Gate QA section (no new config artifact).
  - Donor's per-tier *verifier list rewriting* mechanism is dropped — only roster *addition* is supported, never roster substitution.
- **(d) Control pattern retained:**
  - Tier-conditioned verification budget (the *value-bearing* part of D16 / Gate 2).
  - Quality-engineer as an additional adversarial-stance verifier on STRICT items.
  - Path-override forced-stance integration.
- **(e) Observable post-condition:** Phase-Gate QA report file at `${TASK_DIR}reviews/qa-phase-[N]-report.md` includes a `verifier_roster: [rf-qa, quality-engineer]` line on STRICT (or `[rf-qa]` on STANDARD/LIGHT/EXEMPT) AND a `budget: <tokens>/<timeout>` line. Task Log records `gate-2: profile=<STRICT|...> budget=<n>/<s> roster=[...]`.
- **(f) Admit-criteria match + INV audit:** Row 10 admits "widening the gate is admissible, replacing the gate is not." Satisfied — IS-ADAPT-1 widens (budget + roster), never replaces. INV-03 safe (`rf-qa` adversarial stance always runs); INV-04 safe (report file persisted as today).
- **(g) Constraints bound:** CR-11 — `rf-qa` SUPPLEMENTED NOT REPLACED; CR-8 — Path Override evaluated first; DM-5 — depends on IS-ADOPT-3 + IS-ADOPT-6 (consumes `Tier:` + Gate 1 dispatch).

### IS-ADAPT-2 — D15a Layer 2 verification-stance subset (Row 11, ADAPT MERGE-WITH-GATE-2)

- **(a) Extension point:** Same as IS-ADAPT-1 — extension-point row 10.
- **(b) What changes vs donor:** **Zero net implementation work in Phase 6.** Donor D15 split D15a (verification-stance) and D15b (pre-flight scaffolding); D15a's stance-widening pattern is absorbed into IS-ADAPT-1's tier-conditioned budget + roster widening. The donor's separate D15a "Layer 2 verification-stance" block in `sc-task-protocol/SKILL.md` is **not** ported as a separate block to `task/SKILL.md` — the value is in IS-ADAPT-1.
- **(c) Donor ceremony dropped (R-RULE-06):** D15a's standalone Layer-2 framing (separately named layer with its own subsection in donor SKILL.md) is dropped; only its tier-conditioned verification widening pattern is retained inside IS-ADAPT-1.
- **(d) Control pattern retained:** Tier-conditioned verification widening (now lives in IS-ADAPT-1).
- **(e) Observable post-condition:** Same as IS-ADAPT-1 — no separate evidence file for D15a.
- **(f) Admit-criteria match + INV audit:** Inherited from IS-ADAPT-1.
- **(g) Constraints bound:** This row exists in the manifest **for donor traceability only**.

### IS-ADAPT-3 — D15b Layer 2 pre-flight scaffolding (Row 12, V=2 C=5 K=3 Net=3.33)

- **(a) Extension point:** Extension-point row 2 — First Item Protocol (`extension-point-contracts.md:69-75`; `SKILL.md:100-102`; **C5**).
- **(b) What changes vs donor:**
  - **Donor form:** A "Layer 2 procedural step-list" rendered at *execute-time*, with tier-specific multi-step procedures synthesized inside F1 EXECUTE (e.g., for a STRICT-tier item, the runtime emits steps "serena activate" → "git status check" → "codebase-retrieval call" → "list_memories"). This is the donor's D15c pattern.
  - **Recipient form:** Tier-gated **additive pre-loop setup** in First Item Protocol — NOT inside F1 EXECUTE, NOT per-item, NOT a "procedure synthesis" at execute-time.
    - STRICT (or `forced_stance=STRICT`): `serena_activate_if_available` → `git_status_clean_tree_check` → `codebase_retrieval_on_relevant_code_if_available` → `list_memories_read_memory_for_relevant_prior_context`.
    - STANDARD: `codebase_retrieval_on_relevant_code_if_available`.
    - LIGHT / EXEMPT: skipped.
  - Each step is conditional on the tool being available (graceful skip on unavailability — `serena`/`codebase-retrieval` are MCP-dependent and not always present).
- **(c) Donor ceremony dropped (R-RULE-06):**
  - Donor's *per-tier procedure synthesis at execute-time* (D15c) is REJECTed in this sketch (and globally — Row 26 REJECT). Synthesis would mean F1 EXECUTE generates checklist items at runtime that the loop did not READ from disk — auto-REJECT under INV-01 + INV-05 (CR-13).
  - Donor's "Layer 2" framing as a named runtime artifact is dropped; the steps are inlined as setup actions.
- **(d) Control pattern retained:** Tier-conditioned pre-loop tool-warming (serena / git / codebase-retrieval / memory).
- **(e) Observable post-condition:** A Task Log line `gate-1.5: pre-flight tier=<STRICT|STANDARD> ran=[serena, git, codebase-retrieval, memory]` (or `ran=[]` for LIGHT/EXEMPT). Where a tool was unavailable, the line records `skipped=[<tool>: not-available]`.
- **(f) Admit-criteria match + INV audit:** Row 2 admits session-init / environment-prep actions before the loop's first iteration; explicitly REJECTs init actions that consume a checklist item or compute *what* the loop will execute. Satisfied — pre-flight is pure environment-prep, no checklist consumption, no work definition. INV-01 / INV-05 safe (CR-13 — additive pre-loop only).
- **(g) Constraints bound:** CR-13 — D15b is PRE-LOOP additive only; D15c per-item synthesis is auto-REJECT. DM-10 — depends on IS-ADOPT-3 + IS-ADOPT-6.

---

## 3. DEFER — Re-enabling Preconditions (7 primary + 3 catalog-derived)

Each DEFER entry names the **precondition** that would re-enable the feature in a future sprint. Per R-RULE-11, the Phase 4 verdict is preserved; the precondition is the documented trigger for a re-debate, not a license for Phase 5 to perform the upgrade.

### IS-DEFER-1 — Row 14: Compliance-gating cluster aggregate (DEFER, cluster-as-written)

- **Precondition:** **None — terminal DEFER.** The cluster-as-written package (donor's four-gate coordination layer with write-back contracts) is *not* portable. CR-1 resolved: the cluster-aggregate verdict is an audit roll-up; sub-gate verdicts (Rows 6, 10, 16, 22) are operative. A future sprint may re-propose the cluster-as-written only if a new attach surface for the coordination layer appears in `/task` — which Phase 5 deems implausible.
- **What stays out:** Donor's four-gate write-back coordination ceremony (the implementation mass, per R-RULE-06).
- **Note for ledger:** Carry CR-1 rationale verbatim to `rejected-features-ledger.md`.

### IS-DEFER-2 — Rows 15+16: D27/Layer B + Gate 3 — per-tier MCP matrix + circuit breaker (DEFER, contingent)

- **Precondition:** **Gate 1 is now ADOPTed (Row 6, IS-ADOPT-6 above). Per CR-3, this Phase 5 does NOT silently upgrade — a fresh adversarial re-debate in a future sprint may re-score with K=3 (Gate 1 supplies the tier source), Net=3.0 (ADAPT band).**
- **What stays out:** D27's per-tier MCP matrix + circuit-breaker logic is not ported in this sprint.
- **Re-debate trigger for future sprint:** "Now that Gate 1 ADOPTed, re-debate D27 Layer B / Gate 3 with K=3 in the rubric, evaluate whether the per-tier MCP discipline pays its own cost."
- **R-RULE-11 audit:** Verdict preserved; the upgrade is deferred to an explicit re-debate.

### IS-DEFER-3 — Row 17: TFEP cluster aggregate (DEFER, cluster-as-written)

- **Precondition:** **None — terminal DEFER.** Same shape as IS-DEFER-1. The cluster-as-written (donor's seven-step TFEP flow including Step 5 heading-insertion and Step 6 resume-from-inserted-task, and D25 escalation budget) is not portable; sub-feature verdicts (D19/D20/D21/D22/D24 ADOPT; D23 DEFER; D25 REJECT) are operative.
- **What stays out:** Donor's seven-step cluster-as-written ceremony.
- **Note for ledger:** Carry CR-2 rationale verbatim.

### IS-DEFER-4 — Row 18: D01 — declared `allowed-tools` frontmatter (DEFER)

- **Precondition (two-clause):**
  1. **Skill loader semantics verified** — confirm that the Skill loader (claude-code harness) honors `allowed-tools:` in skill frontmatter with deny-by-default semantics for `/task`'s tool namespace. Today this is unverified — adopting D01 without this check creates a ceremony-without-teeth failure (the field would be declared but unenforced).
  2. **Critical Rule 6 retitled** — `task/SKILL.md` Critical Rule 6 is currently a tool-preference rule, not an exclusion rule. To make `allowed-tools:` semantically coherent, Rule 6 must be split: exclusion → allowlist enforced by loader; preference → narrative rule in SKILL.md.
- **Both clauses required to re-enable.** If both pass in a future sprint: V rises 2→3, Net = 3.0 (ADAPT). If either fails: V collapses to 1, REJECT.
- **What stays out:** The `allowed-tools:` frontmatter declaration in `task/SKILL.md`.
- **R-RULE-07 binding:** This matches manifest exception #8 (`stack-rank.md:246`) — carry verbatim to ledger.

### IS-DEFER-5 — Row 19: D08 — Classification header emission (DEFER)

- **Precondition:** **Downstream parser ships** — a transcript scanner / telemetry collector that consumes the classification header (e.g., a CLI tool that aggregates `Tier:` distribution across tasks, or an observability sink that records gate-1 dispatch outcomes). Adopting D08 in isolation today repeats the R-RULE-06 ceremony-without-teeth failure mode that REJECTed D02/Layer A (no in-repo consumer).
- **If precondition met:** V rises 2→4, Net = 4.0 (ADAPT).
- **What stays out:** The classification header emission block in `task/SKILL.md`.
- **R-RULE-07 binding:** This matches manifest exception #7 (`stack-rank.md:245`) — carry verbatim to ledger.

### IS-DEFER-6 — Row 23: TFEP D23 six-step execution flow with `/sc:forensic` (DEFER)

- **Precondition (three-clause):**
  1. **`/sc:forensic` skill authored** — D23's reference to a `/sc:forensic` adjudication path requires that skill to exist.
  2. **Step 5 redesigned** — donor's "insert a `## Failure Remediation Plan (Adjudicated)` heading into the task file" is an F4-violation (modifies task structure outside DYNAMIC CONTENT MARKER sections). Redesigned to use a DYNAMIC CONTENT MARKER section so the insertion is F4-safe.
  3. **Step 6 redesigned** — donor's "resume from the inserted task" causes IDENTIFY to read items the loop didn't author, violating INV-01. Redesigned to log the adjudication outcome but resume from the *next pre-existing* unchecked item.
- **All three required to re-enable.**
- **What stays out:** Donor's six-step execution flow as written.
- **R-RULE-11 audit:** Verdict preserved.

### IS-DEFER-7 (catalog row 33) — D14: Human-readable confidence display bar (DEFER)

- **Precondition:** **D08 ADOPTs in a future sprint** (per CR-5 narrative sharpening) AND a *non-D09b* classifier supplies the confidence number. D09b is terminally REJECTed (Row 21 — structurally mismatched, routed to `task-builder`), so D14's input cannot come from D09b. The path forward requires D08 (which itself is DEFER-pending-parser per IS-DEFER-5) plus a fresh classifier source.
- **If precondition met:** Re-debate D14 as a downstream presentation layer.
- **What stays out:** D14's confidence display bar.
- **R-RULE-11 audit:** Verdict preserved; precondition narrative tightened per CR-5.

### IS-DEFER-8 (catalog row 37) — D26: Feedback Collection (DEFER)

- **Precondition:** **Calibration store authored** — D26's mechanism (collect classification outcomes, compare predicted vs actual, feed into a calibration learning loop) requires a persistent store `/task` does not currently have. A future sprint authoring this store (e.g., as a `~/.claude/cache/` schema or a YAML accumulator under the recipient package) re-enables D26.
- **What stays out:** Feedback Collection mechanism.

### IS-DEFER-9 (catalog row 42) — D32: External configuration references (DEFER)

- **Precondition:** **Tier-keyword YAML producer authored** — the donor references external YAML configuration files (`tier-keywords.yaml`, etc.) that do not exist. A future sprint scoping `task-builder` or `sc:tasklist` to produce these files re-enables D32.
- **What stays out:** External configuration references in the donor SKILL.md.

**DEFER coverage check:** Primary stack-rank DEFER rows are 14 (IS-DEFER-1), 15+16 (IS-DEFER-2 — one feature, two stack-rank views), 17 (IS-DEFER-3), 18 (IS-DEFER-4), 19 (IS-DEFER-5), 23 (IS-DEFER-6) — 6 distinct primary DEFER features. Catalog-derived DEFER rows are 33 (IS-DEFER-7), 37 (IS-DEFER-8), 42 (IS-DEFER-9) — 3 distinct catalog-derived DEFER features. Total: **9 distinct DEFER features**, matching `feature-dependency-matrix.md` § 1's enumeration (the "11" count there includes the duplicate row 15 = row 16 view, and counts cluster-aggregates 14 + 17 as terminal preconditions without re-enable paths beyond the ledger rationale).

---

## 4. Cross-attach-point ordering (from CR-7 / CR-8 / `feature-dependency-matrix.md` § 4)

The following extension-point rows host more than one ADOPT/ADAPT feature. The ordering below is **locked** as part of T05.02 and carried into T05.03's manifest.

| Surface | Co-attached sketches | Locked ordering |
|---|---|---|
| Row 1 — Task File Validation gate | IS-ADOPT-1 (Path Override), IS-ADOPT-3 (D09a Tier validate), IS-ADOPT-6 (Gate 1 dispatch) | `path_override_check → tier_field_validate → gate_1_dispatch` (CR-7) |
| Row 2 — First Item Protocol | IS-ADAPT-3 (D15b pre-flight scaffolding), IS-ADOPT-8 (TFEP Baseline) | `tier_check → D15b_scaffolding (STRICT/STANDARD) → TFEP_baseline (STRICT/STANDARD)` — D15b first because it activates the very tools (serena / codebase-retrieval) that the rest of the task and the baseline collection use; Baseline last because its YAML output is the comparator IS-ADOPT-9 consumes on first failure. |
| Row 4 — F1 EXECUTE item-type dispatch | IS-ADOPT-3 (D09a per-item read) | Single attach; per-item read is purely additive and falls back to task-level when absent. |
| Row 8 — Error Handling / blocker logging | IS-ADOPT-2 (D19 Prohibitions), IS-ADOPT-4 (D20 Carve-outs), IS-ADOPT-9 (D22 Escalation triggers) | `prohibition_check → carve_out_check → escalation_trigger_check` — carve-outs are exceptions to prohibitions, so they must consult prohibitions first; escalation triggers consume the baseline + classify failures, so they run last. All side-channel; CR-12. |
| Row 10 — Phase-Gate QA | IS-ADOPT-1 (Path Override forced-stance), IS-ADAPT-1 (Gate 2 budget widening) | `path_override_check → gate_2_stance_select` (CR-8). |
| Row 11 — Post-Completion Validation | IS-ADOPT-5 (TFEP Incident reporting) | Single attach. |
| Row 13 — Required frontmatter schema slot | IS-ADOPT-3 (D09a `Tier:` field) | Single attach. (D01 / Row 18 would also attach here if ADOPTed in a future sprint per IS-DEFER-4.) |

---

## 5. Admit-criteria audit — every ADOPT/ADAPT sketch respects its target's contract

| Sketch | Target row (C-band) | Admit-criteria match | INV audit | Result |
|---|---|---|---|---|
| IS-ADOPT-1 (Path Override) | Row 1 (C5) + Row 10 (C3) | Pre-loop validator at row 1 + between-phase stance widener at row 10 | INV-01/02/03/04/05 all safe | ✅ |
| IS-ADOPT-2 (D19 Prohibitions) | Row 8 (C5) | New failure-routing policy inside existing taxonomy | INV-01/02/04/05 safe (CR-12) | ✅ |
| IS-ADOPT-3 (D09a Tier field) | Row 13 (C5) + Row 1 (C5) + Row 4 (C3) | New required-metadata field + validator + additive per-item read | INV-01/05 safe (no work-definition leak) | ✅ |
| IS-ADOPT-4 (D20 Carve-outs) | Row 8 (C5) | Co-located with D19 | INV-01/02/04/05 safe (CR-12) | ✅ |
| IS-ADOPT-5 (D24 Incident reporting) | Row 11 (C5) | New whole-task validation analyzer layered on existing pair | INV-03/04 safe | ✅ |
| IS-ADOPT-6 (Gate 1 Dispatch) | Row 1 (C5) | Pre-loop dispatch with user-facing diagnostic | INV-01/03/04 safe (CR-10 — pre-loop only) | ✅ |
| IS-ADOPT-7 (D10 Command dispatch) | Subsumed in IS-ADOPT-6 | N/A (donor-traceability only) | N/A | ✅ |
| IS-ADOPT-8 (D21 TFEP Baseline) | Row 2 (C5) | Pre-loop session-init / env-prep | INV-01/04/05 safe (CR-14 — tier-gated) | ✅ |
| IS-ADOPT-9 (D22 TFEP Escalation) | Row 8 (C5) | New blocker classification + failure-routing | INV-01/03/04 safe (CR-12) | ✅ |
| IS-ADAPT-1 (Gate 2) | Row 10 (C3) | Widening (not replacing) the gate | INV-03/04 safe (CR-11 — supplement not replace) | ✅ |
| IS-ADAPT-2 (D15a) | Subsumed in IS-ADAPT-1 | N/A (donor-traceability only) | N/A | ✅ |
| IS-ADAPT-3 (D15b Pre-flight) | Row 2 (C5) | Pre-loop env-prep, no checklist consumption | INV-01/05 safe (CR-13 — additive pre-loop only) | ✅ |

**No ADOPT/ADAPT sketch attaches to a C1 negative-space surface (N1/N2/N3). No sketch admits at a C-band higher than the row's declared band. No sketch breaks any INV-NN.**

---

## 6. Acceptance Criteria Recap (T05.02)

1. **`integration-sketches.md` exists with a locked integration sketch for every ADOPT feature (extension point, shape of change, new fields/hooks, observable post-condition).** ✅ — Section 1 above: 9 ADOPT sketches (IS-ADOPT-1 through IS-ADOPT-9). Each entry declares the extension point row, shape of change in lines + location, the one new MDTM frontmatter field (`Tier:` in IS-ADOPT-3, the only field added), all hooks and side-effect files introduced, and the disk-resident observable post-condition.

2. **Every ADAPT feature has an explicit modification spec naming what changes, what is dropped, what is retained.** ✅ — Section 2 above: 3 ADAPT specs (IS-ADAPT-1 through IS-ADAPT-3). Each declares: (b) what changes vs the donor, (c) donor ceremony dropped per R-RULE-06, (d) control pattern retained. R-RULE-06 application is explicit in each:
   - IS-ADAPT-1: drops verifier *replacement*; retains tier-conditioned budget + roster widening.
   - IS-ADAPT-2: drops standalone Layer-2 framing; retains stance-widening pattern via IS-ADAPT-1.
   - IS-ADAPT-3: drops per-tier procedure synthesis at execute-time (D15c); retains tier-conditioned pre-loop tool-warming.

3. **Every DEFER feature has a named re-enabling precondition.** ✅ — Section 3 above: 9 DEFER entries. Two terminal DEFERs (IS-DEFER-1, IS-DEFER-3) carry the "cluster-as-written not portable" rationale verbatim from CR-1 / CR-2. Seven DEFERs carry concrete, testable preconditions (Gate 1 ADOPTed re-debate, loader semantics verified + Rule 6 retitled, downstream parser ships, `/sc:forensic` + Step 5 + Step 6 redesigns, D08 ADOPTs + non-D09b classifier source, calibration store authored, tier-keyword YAML producer authored).

4. **Every ADOPT sketch respects its target extension point's admit criteria and breaks no INV-NN.** ✅ — Section 5 audit table: all 12 ADOPT/ADAPT sketches checked against admit criteria + INV-NN. None attach to a C1 surface. None break any INV.

---

## 7. Hand-off to T05.03 — required manifest carry-overs

T05.03's `transfer-manifest.md` must:

1. **Order ADOPT/ADAPT execution** per the dependency map (`feature-dependency-matrix.md` § 2) and the cross-attach-point ordering in Section 4 above:
   - Transfer unit 1: IS-ADOPT-3 + IS-ADOPT-6 (CR-9 — ship together).
   - Transfer unit 2: IS-ADOPT-1 (Path Override — independent of Tier value; lands at any time but must integrate at row 1 before Gate 1 reads its forced-stance flag, and at row 10 before Gate 2 reads it).
   - Transfer unit 3: IS-ADAPT-1 (Gate 2 — depends on Tier + Gate 1).
   - Transfer unit 4: IS-ADAPT-3 (D15b pre-flight — depends on Tier + Gate 1).
   - Transfer unit 5: IS-ADOPT-8 (TFEP Baseline — depends on Tier + Gate 1; tier-gated STRICT/STANDARD).
   - Transfer unit 6: IS-ADOPT-2 (D19 Prohibitions) + IS-ADOPT-4 (D20 Carve-outs) — co-located at row 8.
   - Transfer unit 7: IS-ADOPT-9 (D22 Escalation triggers) — depends on Baseline (transfer unit 5).
   - Transfer unit 8: IS-ADOPT-5 (D24 Incident reporting) — depends on TFEP cluster ADOPT subset (units 6 + 7).
   - Donor-traceability rows: IS-ADOPT-7 (D10) and IS-ADAPT-2 (D15a) — record in manifest with "no separate implementation work" annotation.

2. **Carry forward as manifest exceptions (R-RULE-07)** verbatim:
   - Exception 1 — CR-10 — PRE-LOOP DISPATCH only (IS-ADOPT-6 / IS-ADOPT-7).
   - Exception 2 — CR-11 — `rf-qa` SUPPLEMENTED NOT REPLACED (IS-ADAPT-1 / IS-ADAPT-2).
   - Exception 3 — CR-12 — SIDE-CHANNEL ONLY, NO F1 HALT (IS-ADOPT-2 / IS-ADOPT-4 / IS-ADOPT-5 / IS-ADOPT-8 / IS-ADOPT-9).
   - Exception 4 — CR-14 — BASELINE TIER-GATED (IS-ADOPT-8).
   - Exception 5 — CR-13 — NO PER-ITEM EXECUTE SUBSTITUTION (IS-ADAPT-3; also explicit anti-pattern note rejecting D15c).
   - Exception 6 — CR-9 — `Tier:` + Gate 1 SHIP TOGETHER (IS-ADOPT-3 + IS-ADOPT-6).
   - Exception 7 — CR-15 — D08 DEFERRED UNTIL PARSER SHIPS (IS-DEFER-5).
   - Exception 8 — CR-16 — D01 DEFERRED UNTIL LOADER SEMANTICS + RULE 6 SPLIT (IS-DEFER-4).
   - Subjective override — CR-6 — D02/Layer A REJECT (per R-RULE-06 ceremony-without-teeth override of arithmetic DEFER) — re-affirmed in Phase 5 per R-RULE-07.

3. **Forward to `rejected-features-ledger.md`** the DEFER precondition narratives (IS-DEFER-1 through IS-DEFER-9) verbatim, plus the CR-3 explicit re-debate note on Rows 15+16.

**T05.02 deliverable: COMPLETE.** Phase 5 has the locked integration sketches, ADAPT modifications, and DEFER preconditions needed to produce the binding transfer manifest in T05.03.

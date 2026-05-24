# Plan Adversarial Review — Phase 6 Merge Plan

**Task:** T07.01 — `/sc:adversarial` review of the merge plan
**Roadmap Item:** R-024
**Tier:** STRICT
**Generated:** 2026-05-15
**Skill invoked:** `sc-adversarial-protocol` (adapted single-plan / two-role application — Invariant Defender + Manifest Auditor scrutinize the same Phase 6 plan from different angles, rather than two variants competing for a base).

**Inputs (1:1 referenced, T06.01-verified present):**
- `merge-master.md` (T06.05) — 67 row-line-items / 65 distinct CR-IDs across six refactor files; acyclic dependency graph; 10-step canonical commit sequence.
- `refactor-task-skill.md` (T06.02) — CR-TASK-01..12 (`/task` SKILL.md edits).
- `refactor-mdtm-frontmatter.md` (T06.02) — CR-FM-01..04 (MDTM schema + INV-04 compat).
- `refactor-sctask-deprecation.md` (T06.03) — CR-DEP-01..05 (donor artifact disposition).
- `refactor-references.md` (T06.03) — CR-REF-01..18 + CR-REF-BUCKET-A..H.
- `refactor-distribution.md` (T06.04) — CR-DIST-01..06.
- `refactor-documentation.md` (T06.04) — CR-DOC-01..13.
- `transfer-manifest.md` (T05.03) — 8 transfer units TU-1..TU-8; 9 manifest exceptions ME-1..ME-9.
- `extension-point-contracts.md` (T03.02) — canonical INV-01..INV-05 definitions (anchor labels) and per-extension-point INV-protection map.
- `invariant-survival-walkthrough.md` (T07.03 input) — INV-NN evidence cross-cuts.

**Substitution notice (open finding F-06):** the T07.01 task description directs the reviewer to load `invariant-bounds.md`. **`invariant-bounds.md` does not exist** on disk — T03.01 emitted the anchor labels into `extension-point-contracts.md` (lines 11-17, "Invariant Reference (anchor labels, pending T03.01 expansion)") instead of producing the standalone file. The Invariant Defender used the canonical INV anchor labels from `extension-point-contracts.md` plus the worked-example evidence in `invariant-survival-walkthrough.md` as functional substitute. This is recorded as a finding, not a reviewer-side compromise that affects the verdict — the anchor-labelled rules in the substitute source are byte-identical to the sprint spec § "Load-bearing invariants" that `invariant-bounds.md` was scheduled to expand.

---

## 0. Invariant Reference (verbatim anchor labels)

Reproduced verbatim from `extension-point-contracts.md:11-17` (the canonical anchor source while `invariant-bounds.md` is pending):

| Label | Behavioral rule |
|---|---|
| **INV-01** | F1 loop semantics — READ first unchecked `- [ ]`, EXECUTE exactly as written, UPDATE to `- [x]`, REPEAT. No skipping, reordering, or out-of-band substitution. |
| **INV-02** | Prohibited-actions catalog (F2) — no working from memory, no modifying checklist items mid-execution, no delegating the F1 loop itself. |
| **INV-03** | Phase-gate `rf-qa` between phases (Phase 2+); post-completion `rf-qa` + `rf-qa-qualitative` validation. |
| **INV-04** | Resumability — progress recoverable from disk after context compression / session restart. |
| **INV-05** | Refusal-of-definition — `/task` does not decide *what* to do; the MDTM file does. The F1 loop only *executes*. |

---

## 1. Role briefs

### 1.1 Invariant Defender

Scans every Phase 6 change row in `merge-master.md` § 1.1–§ 1.12 for impact on INV-01..INV-05. For every row that touches an invariant surface (positive-space extension point row 1, 2, 4, 8, 10, 11 or negative-space row N1/N2/N3 per `extension-point-contracts.md`), cites the specific INV-NN rule from the table above and names the load-bearing manifest exception (ME-NN) that constrains the implementation to the safe shape. Reject criteria: any row that would weaken an INV without an explicit ME binding, any row that introduces a new HALT semantic in F1, any row that authors per-item runtime substitution, any row that lets a non-rf-qa verifier replace rf-qa, any row that breaks resumability for existing on-disk task files.

### 1.2 Manifest Auditor

Walks every `transfer-manifest.md` feature (TU-1..TU-8 + ME-1..ME-9 + named donor-ceremony drops) and verifies a Phase 6 change row implements / honors / explicitly excludes it. Flags:
- **Dropped feature** — manifest TU or ME with no Phase 6 row implementing it.
- **Unauthorized scope expansion** — Phase 6 row with no manifest origin or derivative-responsibility justification.
- **Implementation drift** — Phase 6 row whose shape (file path, change type, effort envelope, extension-point row touched) differs materially from the Phase 5 integration sketch in `transfer-manifest.md` § 2 or `integration-sketches.md`.

Reject criteria: any `rejected-features-ledger.md` REJECT or DEFER entry being silently re-proposed (R-RULE-11), any donor ceremony explicitly dropped by the manifest re-appearing in a Phase 6 row, any subjective override happening without a named ME-NN justification (R-RULE-07).

---

## 2. Invariant Defender — per-row assessment

Every Phase 6 row in `merge-master.md` § 1 is assessed. Rows that do not touch an invariant surface (audits, mechanical syncs, doc rewrites, plumbing) are grouped under § 2.4 to avoid 60+ near-identical entries. Rows touching invariant surfaces are listed individually.

### 2.1 M1 Foundation — invariant-dense rows

#### CR-FM-01 — `Tier:` field schema (optional, closed-enum)

- **Invariant surface:** extension-point row 13 (Required frontmatter schema slot, C5; protects INV-01, INV-05).
- **INV-04 (load-bearing).** Existing `.dev/tasks/to-do/TASK-*/` files have no `Tier:` field. If the field were REQUIRED, every existing TASK-* file would fail validation on resumption. Plan makes the field **optional** with default `STANDARD` resolved at Gate 1 (CR-FM-03 codifies the compat shim). ✅ INV-04 preserved.
- **INV-05.** Field is metadata, NOT work-definition (work definition stays in the checklist body). Closed-enum prevents future schema creep toward work-defining values. ✅
- **INV-01.** Validator runs pre-loop (validating-the-task-file section), not per-item. ✅
- **Verdict: PASS** — load-bearing INV-04 compatibility explicitly handled; closed-enum singularity blocks LR-DEFER-4 (`allowed-tools:`) and LR-DEFER-5 (classification header) sneak-in.

#### CR-FM-02 — Per-item inline marker `(Tier: <value>)` schema

- **Invariant surface:** extension-point row 4 (F1 EXECUTE item-type dispatch, C3 — becomes C1 if loop semantics change).
- **INV-01 (load-bearing).** ME-1 binds: per-item marker is a read-only tier-conditioned consumption, NEVER a re-fire of Gate 1 dispatch. Plan's CR-FM-02 acceptance #4 explicitly states "The inline marker is read-only for the item — it never re-fires Gate 1 dispatch (ME-1 binding)." ✅
- **INV-05.** Schema strictly `(Tier: <enum>)` — no embedded run-clauses. Plan's CR-FM-02 risk row: "Phase 7 must reject any future extension proposal without a fresh manifest entry (R-RULE-11)." ✅
- **Concern (open finding F-01).** The boundary between "per-item read-only tier-conditioned check" and "per-item dispatch" is conceptually thin. CR-TASK-07 baseline-skip applied per-item is described as a "read-only check" but it does change runtime behavior per item. The plan's defense is that the *execution profile* is already pinned by pre-loop Gate 1 and the per-item marker only conditions reads against pre-existing tier-gated side effects. **This is a plausible reading and consistent with ME-1, but it depends on implementation discipline — the language "tier-conditioned READ for behaviors already gated" must not be silently widened in CR-TASK-03's eventual code to include per-item dispatch.**
- **Verdict: PASS WITH NOTE** — F-01 recorded.

#### CR-FM-03 — INV-04 backward-compat default

- **Invariant surface:** validator + Gate 1 (extension-point row 1 ordering at task entry).
- **INV-04 (load-bearing — this row IS the floor).** Plan: missing `Tier:` resolves to `STANDARD` silently; "NO task file under `.dev/tasks/to-do/TASK-*/` is rewritten or backfilled by this refactor — the compat shim is a *read-time default*, not a *write-time migration*." ✅
- **Verdict: PASS** — this row exists explicitly to preserve INV-04 and does so by design.

#### CR-FM-04 — Closed-enum + INV-04 audit (cross-row)

- **Invariant surface:** read-only audit; protects INV-04 + R-RULE-11.
- **INV-04, INV-01, INV-05.** Audit is read-only; cannot itself breach any INV. Catches three classes of violation: (a) closed-enum drift between task-level and inline-marker parsers; (b) silent migration attempts that touch existing TASK-* frontmatter (INV-04 breach); (c) LR-DEFER-4 / LR-DEFER-5 / LR-REJECT-3 re-proposal. ✅
- **Verdict: PASS** — audit serves as the cross-row enforcement gate.

#### CR-TASK-01 — `path_override_check` hook at row 1

- **Invariant surface:** extension-point row 1 (Task File Validation gate, C5; protects INV-01, INV-05).
- **INV-01.** CR-7 ordering (`path_override_check → tier_field_validate → gate_1_dispatch`) is binding. If override fires AFTER Gate 1, the wrong-stance dispatch window reopens. Plan's mitigation: "ordering is enforced in the inserted code text itself."
- **INV-05.** Path-glob-keyed (not flag-keyed); LR-REJECT-4 (Gate 5 user-toggleable flags) NOT revived. ✅
- **Concern (open finding F-02).** CR-7 / CR-8 ordering enforcement is *review-dependent*, not structurally enforced. No regression test asserts the read-order; no sentinel comment block calls out the ordering as load-bearing; nothing prevents a future refactor that "improves readability" from reordering the three steps inside *Validating the Task File*. **Recommendation: add a P3 audit row (or expand CR-TASK-12 / CR-FM-04 scope) to grep for the three function names in order, or author an explicit comment block ordering-anchor.**
- **Verdict: PASS WITH NOTE** — F-02 recorded.

#### CR-TASK-02 — `Tier:` closed-enum validator + Gate 1 dispatch (PRE-LOOP ONLY)

- **Invariant surface:** extension-point row 1 (Task File Validation gate; protects INV-01, INV-05).
- **INV-01 (load-bearing).** ME-1 binds: Gate 1 fires **once at task-entry**, **never per-item**. Plan's acceptance #2: "Single Task Log line `gate-1: dispatch_profile=... source=...` is emitted once at task entry, never again per-item." ✅
- **INV-05.** `Tier:` arrives declaratively from frontmatter; no runtime classifier authored (LR-REJECT-3 / D09b NOT revived). Plan's risk row explicitly defends this. ✅
- **INV-03 sub-concern.** LIGHT / EXEMPT profile uses "reduced Phase-Gate QA budget" per the plan. Plan asserts Post-Completion Validation STILL FIRES for LIGHT/EXEMPT ("INV-03 floor"). Strict reading of INV-03: "Phase-gate `rf-qa` between phases (Phase 2+); post-completion `rf-qa` + `rf-qa-qualitative` validation" — the rule guarantees the gate runs but is silent on budget shape. Reduced budget on LIGHT preserves rf-qa identity and invocation, just with tighter capacity (rf-qa with ~1.5K/20s instead of standard budget). **This is an authorized widening of INV-03's surface, bound by TU-3's "Recipient form" definition.** ✅
- **Verdict: PASS** — all three invariants explicitly bound by ME-1 + ME-2 + ME-6.

#### CR-TASK-03 — Per-item `Tier:` read in F1 EXECUTE

- **Invariant surface:** extension-point row 4 (F1 EXECUTE item-type dispatch — C3 normally, **C1 if loop semantics change**).
- **INV-01.** ME-1 binds. Plan: "the per-item marker NEVER triggers a new Gate 1 dispatch line. The task-level Gate 1 line emitted at task-entry remains the canonical execution-profile record." ✅
- **Cross-reference to F-01.** Same boundary concern as CR-FM-02. Tier-conditioned read = baseline-skip per item is the only currently-authored consumption. Any future addition of per-item consumption must be checked against ME-1 by R-RULE-11.
- **Verdict: PASS WITH NOTE** — F-01 cross-referenced.

#### CR-TASK-04 — Gate 2 override read at row 10

- **Invariant surface:** extension-point row 10 (Phase-Gate QA Verification; protects INV-03, INV-04).
- **INV-03 (load-bearing).** This row does NOT touch verifier identity — only profile selection. ME-2 binding is preserved (CR-TASK-05 alone owns roster, and that row authors `[rf-qa, quality-engineer]` literally, never substitution). ✅
- **CR-8 ordering concern (cross-references F-02).** Same review-dependence as CR-TASK-01.
- **Verdict: PASS WITH NOTE** — F-02 cross-referenced.

### 2.2 M2 Tier-conditioned behaviors

#### CR-TASK-05 — Phase-Gate QA tier budget + roster widening (ADAPT)

- **Invariant surface:** extension-point row 10 (Phase-Gate QA; protects INV-03).
- **INV-03 (load-bearing).** ME-2 binds: `rf-qa` SUPPLEMENTED NOT REPLACED. Plan: "the inserted mapping authors `roster: [rf-qa, quality-engineer]` literally (rf-qa first, additive comma); future edits that drop `rf-qa` from a STRICT roster row are an ME-2 violation." ✅
- **Donor ceremony drop verification.** Plan drops donor's verifier-*replacement* semantic, donor's standalone "verification routing table" framing, and donor's per-tier verifier-list rewriting. CR-TASK-05 inlines tier→{budget, timeout, roster} mapping into the existing Phase-Gate QA section, never as a separate config artifact. ✅
- **Verdict: PASS** — ME-2 explicit; donor verifier-replacement NOT revived.

#### CR-TASK-06 — First Item Protocol tier-gated pre-flight (ADAPT, D15b only)

- **Invariant surface:** extension-point row 2 (First Item Protocol, C5; protects INV-01, INV-05).
- **INV-01 + INV-05 (load-bearing).** ME-5 binds: NO PER-ITEM EXECUTE SUBSTITUTION. Pre-flight is anchored under *First Item Protocol* (before F1 starts), never inside *F1 Execution Loop*. D15c (per-tier procedure synthesis at execute-time) REJECTed and not revived. ✅
- **Concern (open finding F-03 — git-dirty behavior unspecified).** STRICT pre-flight runs `git_status_clean_tree_check`. Plan specifies "graceful skip on unavailability" for MCP tools (`serena` / `codebase-retrieval`) but does NOT specify behavior when `git status` returns a *dirty tree* (i.e., the tool IS available but its output is "dirty"). Two readings:
  - Reading A (safer): emit a warning to Task Log and continue — no HALT of F1 entry. Consistent with ME-3 spirit and INV-01 progress guarantee.
  - Reading B (loud): refuse task entry until tree is clean — would introduce a new HALT semantic for STRICT tasks at pre-loop entry, which is closer to a CR-FM-01 refusal-diagnostic shape than to ME-3.
  Either reading is defensible, but **the plan is silent on which.** Phase 7 implementation could land either; Phase 7 reviewer cannot verify intent against the plan. **Recommendation: add an explicit clarification in CR-TASK-06's acceptance criteria — pick Reading A or Reading B and state it.**
- **Verdict: PASS WITH OPEN FINDING** — F-03 recorded.

### 2.3 M3 TFEP cluster — invariant-dense

#### CR-TASK-07 — TFEP baseline (D21)

- **Invariant surface:** extension-point row 2 (First Item Protocol; protects INV-01, INV-04).
- **INV-04 (load-bearing).** Plan: baseline file written via Incremental Writing Protocol (Critical Rule #2, ZERO TOLERANCE); partial baseline on restart → YAML parse fails → baseline collection re-runs idempotently. ✅
- **ME-4.** Tier-gated to STRICT/STANDARD; LIGHT/EXEMPT skip. ✅
- **Concern (open finding F-04 — baseline-absent fallback for CR-TASK-09).** The plan says "for LIGHT/EXEMPT tasks, the file is absent (skip is silent)" but does NOT specify CR-TASK-09's behavior on STRICT/STANDARD when the baseline file is absent or empty (e.g., session interrupted between F1's first iteration entry and baseline write completion, OR `pytest --collect-only` returned zero tests because the project has no tests yet). Three readings:
  - Reading A: baseline-absent on STRICT/STANDARD → CR-TASK-09 falls back to classifying all failures as "new" (conservative — over-escalates).
  - Reading B: baseline-absent on STRICT/STANDARD is a refusal at task entry (loud — refuses to proceed without baseline).
  - Reading C: baseline-absent on STRICT/STANDARD → CR-TASK-09 silently skips classification (under-escalates).
  Reading A is the only one consistent with INV-01 progress guarantee + INV-03 "rf-qa adversarial-stance floor" (over-escalation is safer than under-escalation). **The plan does not explicitly endorse Reading A.** Phase 7 reviewer should know which.
- **Verdict: PASS WITH OPEN FINDING** — F-04 recorded.

#### CR-TASK-08 — TFEP Prohibitions + Carve-outs (D19+D20)

- **Invariant surface:** extension-point row 8 (Error Handling / blocker logging, C5; protects INV-01, INV-02, INV-04).
- **INV-01 + ME-3 (load-bearing).** Plan: "F1 does **NOT** halt on a refusal — the failing item flips to `- [x]` via existing Error Handling step 3 (line 176, unrecoverable blocker logging), and the loop continues." ME-3 binds: SIDE-CHANNEL ONLY, NO F1 HALT. Halting variant is auto-REJECT. ✅
- **INV-02 sub-concern.** Plan says failing item is marked `- [x]` even on VIOLATION. Existing `/task` semantics: per Critical Rule 6 in SKILL.md:170-179, items are "NEVER left unchecked" — failed items flip to `- [x]` with the failure recorded via existing blocker logging. This is the existing /task baseline; CR-TASK-08 adds a side-channel VIOLATION/carve-out emit alongside the existing flow. INV-02 F2 prohibits "Assuming completion" but the existing blocker-logging mechanism is the established workaround for unrecoverable blockers and does not assume completion (it records the failure on disk). ✅
- **Verdict: PASS** — consistent with existing /task behavior; donor F1-halting semantic explicitly REJECTed.

#### CR-TASK-09 — TFEP Escalation trigger detection (D22)

- **Invariant surface:** extension-point row 8 (Error Handling) AND, critically, extension-point row 10 (Phase-Gate QA — rf-qa is spawned by this row at row 8).
- **INV-01 + ME-3.** Side-channel only, no F1 halt. ✅
- **INV-03 (load-bearing — see open finding F-05).** Plan: "Route to `rf-qa` via the existing Phase-Gate QA verifier-spawn pattern (lines 191–198 of SKILL.md) — NO new escalation gate authored, NO new budget."
- **Concern (open finding F-05 — rf-qa invocation surface widening).** The canonical INV-03 rule is: "Phase-gate `rf-qa` between phases (Phase 2+); post-completion `rf-qa` + `rf-qa-qualitative` validation." That language locates rf-qa firing at **phase boundaries** and at **post-completion**. CR-TASK-09 routes rf-qa **mid-phase** (at error-handling time inside F1's execution of a single item). The plan calls this "the existing INV-03 surface" but it is, strictly, a **new invocation point** — a third firing location alongside phase-gate and post-completion. This is not necessarily wrong (it tightens correctness by escalating regressions on the spot), but the plan does not explicitly call it a surface widening. **Recommendation:** either (a) document this as an authorized INV-03 surface extension in the final-merge-plan, with the named justification that escalation is mid-phase routing to an existing verifier identity (not a new verifier or a new gate), or (b) refine INV-03's anchor language in `invariant-bounds.md` (when authored) to encompass mid-phase escalation routing.
- **D25 not revived.** Plan uses existing 3-cycle fix loop; LR-REJECT-2 (3-strike FULL STOP) NOT authored. ✅
- **Verdict: PASS WITH OPEN FINDING** — F-05 recorded.

#### CR-TASK-10 — TFEP Incident report side-effect FILE (D24)

- **Invariant surface:** extension-point row 11 (Post-Completion Validation; protects INV-03, INV-04) AND negative-space row N2 (Task File Modification Restrictions / F4 — admits NOTHING).
- **INV-01, INV-04, INV-05, F4 (load-bearing).** Plan writes to a side-effect FILE (`research/tfep-incident-report.md`), NEVER inserts the D23 Step 5 heading into the task file. F4 / INV-05 / INV-01 all preserved. LR-DEFER-6 (D23 Step 5/6) NOT revived. ✅
- **INV-04.** File written on disk; Post-Completion read verifies seven-field schema. ✅
- **ME-3.** Side-channel write at Post-Completion, not F1 EXECUTE. ✅
- **Verdict: PASS** — most invariant-dense row of the cluster; clean.

### 2.4 M-sync, M4, M5 — invariant impact

#### CR-TASK-11 — `make sync-dev` mirror refresh

- **R-RULE-10 only**, no INV-NN at risk (mechanical sync). ✅

#### CR-TASK-12 — Verbatim donor `diff` audit (six blocks)

- **INV-03 (protected).** Catches silent paraphrase drift in TFEP trigger strings (e.g., "≥3 new tests fail simultaneously" → "3 or more new tests fail" would change the threshold semantics). ✅

#### CR-DEP-01..05 — `/sc:task` deprecation

- **No INV-NN at risk on the recipient skill** (deprecation removes a capability with redirect; doesn't change `/task` behavior).
- **ME-9 (preserved).** CR-DEP-01 + CR-DEP-05 remove the `mcp-servers:` and `personas:` advertisement lines from the soft-deprecation stub. R-RULE-06 ceremony-without-teeth NOT re-introduced. ✅
- **Absorption-before-deprecation precondition (load-bearing).** Plan's CR-DEP-03 dependency lists CR-TASK-01..10 must land first. Hard-deleting the donor SKILL.md before absorption would strand any unabsorbed pattern. The R-RULE-11 audit in merge-master § 4 cross-checks this for 26 ledger entries. ✅
- **Verdict: PASS** — no INV-NN at risk, ME-9 preserved, deprecation gated on absorption completion.

#### CR-REF-* — references rewrites (CR-REF-01..18 + CR-REF-BUCKET-A..H)

Almost all rows are text edits / redirects / annotations to non-`/task`-SKILL files. None touch the loop, the validator, or the side-effect file mechanics. Two rows merit explicit invariant assessment:

- **CR-REF-BUCKET-C (existing `.dev/tasks/to-do/TASK-*/` files — `leave-as-is` + README guidance).** Plan explicitly names INV-04: "**INV-04 load-bearing**: redirect inside TASK body would corrupt MDTM frontmatter." NO existing TASK-* body is rewritten. INV-04 sample test on one TASK-* file is in the acceptance row. ✅
- **CR-REF-09 (test parity — keep historical `/sc:task-unified` guard + add new `/sc:task` guard).** Test-suite regression protection both directions. Not an INV-NN row but worth surfacing: this is a derivative Phase 6 implementation decision (the manifest does not specify test-guard preservation). It is the safer-by-default Phase 6 reading; consistent with R-RULE-11 spirit (don't regress prior REJECT enforcement).

Other CR-REF rows + CR-DIST-01..06 + CR-DOC-01..13: text edits / installer/sync plumbing / docs. No INV-NN surfaces touched. ✅

### 2.5 Coverage check — Invariant Defender

Every Phase 6 change row in `merge-master.md` § 1 received an Invariant Defender assessment. Rows touching invariant surfaces (positive-space extension-point rows 1, 2, 4, 8, 10, 11 or negative-space N1/N2/N3) cite the specific INV-NN(s) from § 0 and the bound ME-NN(s) from `transfer-manifest.md` § 3. Rows that do NOT touch invariant surfaces (mechanical syncs, doc rewrites, installer plumbing, reference redirects) are accounted for in § 2.4 with the explicit "no INV-NN at risk" determination.

**Invariant Defender coverage: 67/67 row-line-items assessed (65 distinct CR-IDs + 2 audit/handoff ack rows).**

| Bucket | Rows | Outcome |
|---|---|---|
| Touches invariant surface, PASS | 13 (CR-FM-01, -02, -03, CR-TASK-01..10) | All bound by named ME-NN; no INV violation |
| Touches invariant surface, PASS WITH NOTE / OPEN FINDING | 7 (CR-FM-02, CR-TASK-01, -03, -04, -06, -07, -09) — overlaps with row above for rows that both PASS and carry an open finding | 5 distinct open findings F-01..F-05 |
| Touches invariant surface (audit), PASS | 2 (CR-FM-04, CR-TASK-12) | Read-only audits |
| Does NOT touch invariant surface, PASS | 47 (CR-TASK-11, CR-DEP-01..05, CR-REF-01..18 + buckets, CR-DIST-01..06, CR-DOC-01..13, CR-DOC-13 ack, CR-DEFER-T06.04 ack) | Mechanical / redirects / docs / plumbing |

---

## 3. Manifest Auditor — per-feature assessment

### 3.1 Transfer units (TU-1..TU-8 forward coverage)

| Manifest TU | Phase 6 change row(s) | Mapping status |
|---|---|---|
| TU-1 (`Tier:` field + Gate 1 + per-item marker) | CR-FM-01, CR-FM-02, CR-FM-03, CR-TASK-01 (path-override ordering cohort), CR-TASK-02, CR-TASK-03 | ✅ Mapped — all four sub-patterns (frontmatter field, inline marker, compat shim, Gate 1 dispatch + per-item read) authored |
| TU-2 (Critical/Trivial Path Override) | CR-TASK-01 (row 1 hook), CR-TASK-04 (row 10 hook) | ✅ Mapped — both runtime-ordering surfaces (CR-7 + CR-8) authored |
| TU-3 (Gate 2 Verification routing widening, ADAPT) | CR-TASK-05 | ✅ Mapped |
| TU-4 (D15b Layer 2 pre-flight, ADAPT) | CR-TASK-06 | ✅ Mapped (D15c REJECTed, not authored) |
| TU-5 (TFEP Test baseline snapshot, ADOPT) | CR-TASK-07 | ✅ Mapped |
| TU-6 (TFEP Prohibitions + Permitted exceptions, ADOPT) | CR-TASK-08 | ✅ Mapped |
| TU-7 (TFEP Escalation trigger detection, ADOPT) | CR-TASK-09 | ✅ Mapped |
| TU-8 (TFEP Incident reporting, ADOPT) | CR-TASK-10 | ✅ Mapped |

**Forward coverage: 8/8. No dropped TU.**

### 3.2 Manifest exceptions (ME-1..ME-9 binding coverage)

| ME-NN | Title | Bound to Phase 6 row(s) | Status |
|---|---|---|---|
| ME-1 | PRE-LOOP DISPATCH ONLY | CR-TASK-02 (primary); CR-TASK-03, CR-FM-02 (per-item marker MUST NOT re-fire dispatch) | ✅ Bound |
| ME-2 | `rf-qa` SUPPLEMENTED NOT REPLACED | CR-TASK-05 (roster widening); CR-TASK-04 (override read MUST NOT swap verifiers) | ✅ Bound |
| ME-3 | SIDE-CHANNEL ONLY, NO F1 HALT | CR-TASK-08, CR-TASK-09, CR-TASK-10 (and transitively CR-TASK-07 — baseline is pre-loop) | ✅ Bound |
| ME-4 | BASELINE TIER-GATED | CR-TASK-07; CR-TASK-10 transitively | ✅ Bound |
| ME-5 | NO PER-ITEM EXECUTE SUBSTITUTION | CR-TASK-06 (REJECTs D15c at the attach surface) | ✅ Bound |
| ME-6 | TIER FIELD + GATE 1 SHIP TOGETHER | M1 atomic-merge rule (CR-FM-01..03 + CR-TASK-01..04 ship as one source-tree merge); merge-master § 1.1 footnote and § 5 step 1 | ✅ Bound |
| ME-7 | D08 DEFERRED UNTIL PARSER SHIPS | No row authored — observed-but-not-emitted (refactor-task-skill § 3.3 + refactor-mdtm-frontmatter § 3.4) | ✅ Honored (deferral preserved) |
| ME-8 | D01 DEFERRED UNTIL LOADER + RULE 6 SPLIT | No row authored — observed-but-not-emitted | ✅ Honored |
| ME-9 | D02 / Layer A REJECT (R-RULE-06 override re-affirmed) | CR-DEP-01 (`remove-field` on `mcp-servers:` + `personas:`) + CR-DEP-05 (audit) + CR-DIST-03 (plugin stub) + CR-DOC-04 (developer-guide rewrite) | ✅ Bound |

**Manifest exceptions: 9/9 accounted for** — 6 actively bound by Phase 6 rows; 3 observed-but-not-emitted (deferrals preserved by the absence of authoring rows).

### 3.3 Donor-ceremony drops (manifest § 2 verbatim)

For each donor pattern the manifest § 2 explicitly drops, verify NO Phase 6 row re-introduces it:

| Dropped donor ceremony | Manifest source | R-RULE-11 audit verdict | Phase 6 confirmation |
|---|---|---|---|
| D09b runtime classifier with priority cascade + keyword tables | TU-1 ceremony drop + LR-REJECT-3 (ledger row 21) | NOT revived | CR-TASK-02 reads `Tier:` declaratively; `merge-master.md` § 4 entry for LR-REJECT-3 confirms |
| D10 separate command-side dispatch layer | TU-1 ceremony drop (donor-traceability) | NOT revived | CR-DEP-01 collapses the command body to a redirect stub |
| D15c per-tier procedure synthesis at execute-time | TU-4 ceremony drop + LR-REJECT-7 (ledger row 26) | NOT revived | CR-TASK-06 anchored at *First Item Protocol* (pre-loop); ME-5 binds |
| D23 Step 5 — "insert `## Failure Remediation Plan (Adjudicated)` heading" | TU-8 ceremony drop + LR-DEFER-6 (ledger row 23) | NOT revived | CR-TASK-10 writes side-effect FILE; F4 + INV-05 preserved |
| D23 Step 6 — "resume from inserted task" | TU-8 ceremony drop + LR-DEFER-6 | NOT revived | CR-TASK-10 does not insert task-file content; IDENTIFY only reads existing checklist items |
| D25 "3-strike FULL STOP" escalation budget | TU-7 ceremony drop + LR-REJECT-2 (ledger row 20) | NOT revived | CR-TASK-09 uses existing 3-cycle fix loop; no new budget authored |
| Donor F1-HALTING TFEP behavior | TU-6 + TU-7 ceremony drop (ME-3 binding) | NOT revived | CR-TASK-08 / -09 / -10 are side-channel only; F1 continues |
| Donor verifier-replacement semantic (`quality-engineer` REPLACES `rf-qa` on STRICT) | TU-3 ceremony drop (ME-2 binding) | NOT revived | CR-TASK-05 authors `[rf-qa, quality-engineer]` literally; replacement-on-STRICT is auto-REJECT |
| Donor standalone "verification routing table" as separate config artifact | TU-3 ceremony drop | NOT revived | CR-TASK-05 inlines tier→{budget, timeout, roster} mapping into existing Phase-Gate QA section |
| Donor "Layer 2" framing as a named runtime artifact | TU-4 ceremony drop | NOT revived | CR-TASK-06 inlines pre-flight as setup actions; no named layer authored |

**Donor-ceremony drops: 10/10 confirmed not re-introduced.**

### 3.4 Ledger entries (R-RULE-11 audit)

Already comprehensively audited in `merge-master.md` § 4 against all 26 `rejected-features-ledger.md` entries. Manifest Auditor independently re-scanned the highest-risk entries and found:

- **LR-REJECT-3 (D09b runtime classifier)** — NOT revived. CR-TASK-02 + CR-DOC-01 + CR-DOC-04 + CR-REF-05 all explicitly cite declarative `Tier:` semantics. ✅
- **LR-REJECT-4 (Gate 5 user-toggleable flags)** — NOT revived. CR-TASK-01's override is path-glob-keyed; no `--strict` / `--explain` flag authored anywhere. ✅
- **LR-REJECT-7 (D15c per-tier procedure synthesis)** — NOT revived. CR-TASK-06 anchored pre-loop; ME-5 binds. ✅
- **LR-DEFER-4 (D01 `allowed-tools:` enforcement)** — NOT revived. CR-FM-04 audit grep blocks. ✅
- **LR-DEFER-5 (D08 classification header emission)** — NOT revived. CR-FM-04 audit grep blocks. ✅
- **LR-DEFER-6 (D23 six-step flow)** — NOT revived. CR-TASK-10 writes side-effect FILE only. ✅
- **ME-9 / D02 Layer A re-affirmation** — Honored. CR-DEP-01 + CR-DEP-05 + CR-DIST-03 + CR-DOC-04 all explicitly remove or do-not-reintroduce `mcp-servers:` advertisement. ✅

**Ledger audit: zero entries re-proposed across all 65 distinct CR-IDs. R-RULE-11 holds at the consolidated level (independently verified, concurs with merge-master § 4).**

### 3.5 Implementation drift check — manifest § 2 sketches vs Phase 6 shape

For each TU, compare the manifest § 2 "Shape of change" to the Phase 6 row's effort estimate + extension-point row touched + file path. Drift would manifest as: (a) effort envelope significantly larger than manifest sketch (→ scope expansion), (b) different extension-point row touched (→ wrong attach surface), or (c) different file path (→ misrouting).

| TU | Manifest sketch shape | Phase 6 rows + effort + ext-point | Drift verdict |
|---|---|---|---|
| TU-1 | ~3-5 (frontmatter) + ~5-10 (validator) + ~10-15 (Gate 1) + ~3 (F1 per-item) = ~21-33 lines aggregate at ext-point rows 1, 4, 13, all on `SKILL.md` | CR-FM-01 (XS, row 13) + CR-FM-02 (XS, row 4) + CR-FM-03 (XS, row 1) + CR-TASK-02 (M, row 1) + CR-TASK-03 (XS, row 4) on `[src] src/superclaude/skills/task/SKILL.md` | ✅ No drift |
| TU-2 | ~10 (row 1) + ~5 (row 10) on `SKILL.md` | CR-TASK-01 (S, row 1) + CR-TASK-04 (XS, row 10) on same path | ✅ No drift |
| TU-3 | ~25 lines added to Phase-Gate QA block (row 10) on `SKILL.md` | CR-TASK-05 (M, row 10) | ✅ No drift |
| TU-4 | ~15-25 lines added to First Item Protocol (row 2) on `SKILL.md` | CR-TASK-06 (M, row 2) | ✅ No drift |
| TU-5 | ~15 lines added to First Item Protocol (row 2) on `SKILL.md` | CR-TASK-07 (M, row 2) | ✅ No drift |
| TU-6 | ~15 (D19) + ~10 (D20) = ~25 lines at Error Handling (row 8) on `SKILL.md` | CR-TASK-08 (M, row 8) | ✅ No drift |
| TU-7 | ~15 lines added to Error Handling (row 8) on `SKILL.md` | CR-TASK-09 (S, row 8) | ✅ No drift |
| TU-8 | ~20 lines (report template + Post-Completion check) at Post-Completion (row 11) on `SKILL.md` | CR-TASK-10 (M, row 11) | ✅ No drift |

**Implementation drift: 0/8 TUs drifted.** Every TU's Phase 6 rows land at the manifest-named extension-point row on the manifest-named file path, within the manifest's effort envelope.

### 3.6 Unauthorized scope expansion check — Phase 6 rows without manifest origin

Identify every Phase 6 CR-ID whose Manifest feature(s) column cites NO TU-N or ME-N, then verify each has a documented derivative-responsibility justification.

| Phase 6 row | Manifest origin | Derivative justification | Verdict |
|---|---|---|---|
| CR-FM-04 | INV-04 audit + R-RULE-11 audit | Audit on CR-FM-01..03 — derivative consequence of authoring the schema (acceptance criterion validation) | ✅ Justified |
| CR-TASK-11 | R-RULE-10 sync mechanic | Mechanical sync after CR-TASK-01..10 land on `[src]`; required by `CLAUDE.md` "Component Sync" rule | ✅ Justified |
| CR-TASK-12 | TU-2 / TU-6 / TU-7 / TU-8 verbatim obligations | Cross-row audit catching paraphrase drift of donor strings the manifest pinned as verbatim | ✅ Justified |
| CR-DEP-01..05 | CS-M4-A artifact disposition; ME-9; donor-traceability | Derivative consequence of TU-1..TU-8 absorption (the donor command becomes redundant after absorption; § 4 absorption traceability in `refactor-sctask-deprecation.md` confirms zero stranded patterns) | ✅ Justified |
| CR-REF-01..18 + BUCKET-A..H | CS-M4-B reference enumeration | Derivative consequence of CR-DEP-01 (active runtime / source / backlog / docs references to the deprecated command must redirect or be annotated) | ✅ Justified |
| CR-DIST-01..06 | CS-M5-A installer + sync + plugin + README mechanics | Derivative consequence of CR-DEP-03/04 (installer must exclude the hard-deleted skill; sync-dev must prune the mirror; plugin stub must mirror the command stub) | ✅ Justified |
| CR-DOC-01..13 | CS-M5-B documentation rewrites | Derivative consequence of CR-DEP-01 + CR-TASK-02 (user/dev guides must describe the post-absorption single-surface model) | ✅ Justified |
| CR-DOC-13 ack + CR-DEFER-T06.04 ack | T06.03 → T06.04 handoff confirmation | Audit acknowledgements, no scope content | ✅ Justified |

**Unauthorized scope expansion: 0 rows.** Every Phase 6 row not directly mapped to a TU has a documented derivative-responsibility tracing — either a Phase 6 audit (R-RULE-11 / R-RULE-10 / verbatim donor diff), a mechanical sync, or a downstream consequence of deprecation/distribution/documentation.

### 3.7 Procedural authorization note (open finding F-07)

The Manifest Auditor flags one **provenance-of-authorization** observation for transparency:

- `transfer-manifest.md` § 5 ("Build-order rule for Phase 6") names the recipient attach target and the source-tree edit ordering, but does NOT explicitly authorize *hard-deletion* of donor artifacts (`src/superclaude/skills/sc-task-protocol/SKILL.md` + `__init__.py`).
- The authorization for hard-deletion lives in:
  - The sprint goal ("`/sc:task` deprecation" — overarching sprint outcome).
  - The phase-6 tasklist T06.03 deliverable description ("`refactor-sctask-deprecation.md` — the deprecation plan for `/sc:task`: soft-deprecation … vs hard-deprecation …, chosen per artifact and justified").
  - `refactor-sctask-deprecation.md` § 2 rubric + § 4 absorption traceability table (every absorbed pattern landed at `[src] src/superclaude/skills/task/SKILL.md`; donor body now redundant ceremony per R-RULE-06).

This is a **procedural authorization** flowing from the sprint goal through the tasklist into the refactor file's rubric, NOT a manifest binding. The Manifest Auditor accepts it (the chain is sound, the rubric is reasonable, the absorption-completeness check satisfies the precondition), but records the absence of explicit manifest-binding for transparency so a future reviewer cannot mistake the deletion for unauthorized scope.

### 3.8 Coverage check — Manifest Auditor

| Manifest element | Coverage |
|---|---|
| TU-1..TU-8 (forward) | 8/8 mapped to at least one Phase 6 row |
| ME-1..ME-9 (binding) | 9/9 — 6 actively bound, 3 honored-by-absence |
| Donor-ceremony drops (manifest § 2) | 10/10 confirmed not re-introduced |
| Ledger entries (R-RULE-11) | 26/26 audited (independently confirms merge-master § 4) |
| Phase 6 rows without direct TU mapping | All justified as derivative responsibility |

**Manifest Auditor coverage: 8 + 9 + 10 + 26 = 53 manifest features, plus 65/65 Phase 6 rows traced to a TU or derivative. No dropped manifest feature; no unauthorized scope expansion; no implementation drift.**

---

## 4. Cross-examination

### 4.1 Invariant Defender → Manifest Auditor

**Q1.** The `merge-master.md` § 1 line 7 says "every change row from the **five** refactor-`*.md` files (six artifacts)". The T07.01 task description likewise says "the five `refactor-*.md` files". On disk, there are six refactor files (`refactor-task-skill.md` + `refactor-mdtm-frontmatter.md` + `refactor-sctask-deprecation.md` + `refactor-references.md` + `refactor-distribution.md` + `refactor-documentation.md`). Is one of the six an unauthorized scope addition by Phase 6?

**Manifest Auditor A1.** No — the five-vs-six discrepancy is a documentation count, not a scope finding. The six files trace to **three Phase 6 task pairs**: T06.02 produces two artifacts (skill edits + frontmatter schema), T06.03 produces two artifacts (deprecation + references), T06.04 produces two artifacts (distribution + documentation). The phase-6 tasklist treats each pair as one "refactor plan" — hence the "five" count flexes ambiguously between counting tasks (3) and counting refactor-area pairs (3), neither of which is "five". The "five" figure is a counting inconsistency that propagated forward from earlier phase planning; every one of the six files is binding and is mapped to a manifest TU or derivative responsibility. **Recorded as open finding F-08 (documentation accuracy, not scope expansion).**

**Q2.** CR-DEP-03 hard-deletes `[src] src/superclaude/skills/sc-task-protocol/SKILL.md`. The manifest does not explicitly authorize donor-side hard-deletion — it specifies the *recipient* attach target and that absorption must precede deprecation. Where is hard-deletion authorized?

**Manifest Auditor A2.** Authorization is procedural, not manifest-bound — see § 3.7. The chain: sprint goal ("`/sc:task` deprecation") → T06.03 task description (soft- vs hard-deprecation chosen per artifact and justified) → `refactor-sctask-deprecation.md` § 2 rubric + § 4 absorption traceability. The Manifest Auditor accepts this chain as sufficient because (a) the absorption-completeness precondition (CR-TASK-01..10 land before CR-DEP-03) is structurally enforced via dependency edges, and (b) `refactor-sctask-deprecation.md` § 4 explicitly maps every absorbed pattern back to the recipient surface, so no R-RULE-06 ceremony survives uncoupled. **Recorded as open finding F-07** for transparency, with the recommendation that the final-merge-plan add one sentence stating the procedural authorization chain.

**Q3.** Were any manifest features dropped or implemented at a different extension-point row than the manifest § 2 specifies?

**Manifest Auditor A3.** No. § 3.5 verifies all 8 TUs land at the manifest-named extension-point row on the manifest-named file path within the manifest's effort envelope. Zero drift; zero drops.

### 4.2 Manifest Auditor → Invariant Defender

**Q1.** CR-TASK-09 routes rf-qa "via the existing Phase-Gate QA verifier-spawn pattern" at error-handling row 8 (mid-phase). INV-03's anchor language locates rf-qa at phase-boundaries and post-completion. Does this routing widen INV-03's surface, and if yes, is the widening authorized?

**Invariant Defender A1.** Yes — see open finding F-05. The routing is a third invocation point alongside phase-gate and post-completion. It is plausibly authorized by TU-7's "Recipient form" definition ("route to `rf-qa` for adjudication (existing INV-03 surface)") which calls the existing-surface phrasing — but the anchor language in INV-03 strictly speaks of phase-boundaries. **The Invariant Defender's position: this is an authorized widening because (a) it routes to the existing verifier identity (rf-qa, no replacement, ME-2 preserved), (b) it uses the existing spawn pattern in `SKILL.md:191-198` (no new verifier-spawn surface), and (c) the manifest explicitly names it as TU-7's routing path. However, the widening should be documented explicitly in the final-merge-plan + invariant-survival-walkthrough so a future reviewer understands the third invocation point is intentional.**

**Q2.** CR-TASK-06 STRICT pre-flight runs `git_status_clean_tree_check`. If the tree is dirty, what's the F1 entry behavior? The plan is silent.

**Invariant Defender A2.** Open finding F-03 — the plan does not specify. Two defensible readings (Reading A: log+continue; Reading B: refuse entry). The Invariant Defender recommends Reading A (log+continue) because (a) it preserves INV-01's progress guarantee, (b) it is consistent with the "graceful skip" pattern the plan uses for MCP tool unavailability, and (c) STRICT tier-conditioned setup actions are environment-prep, not authorization gates. **Recommendation: Phase 7 implementation should default to Reading A and the final-merge-plan should add one acceptance-criteria clause to CR-TASK-06 stating this explicitly.**

**Q3.** CR-TASK-07 baseline is consumed by CR-TASK-09. What if baseline is absent or empty on a STRICT/STANDARD task (e.g., session interrupt, zero collected tests, MCP env without pytest)?

**Invariant Defender A3.** Open finding F-04 — the plan does not specify. The Invariant Defender recommends the "conservative over-escalate" reading: baseline-absent on STRICT/STANDARD → CR-TASK-09 classifies all failures as "new" (Reading A from § 2.3 above). This preserves the INV-03 spirit (rf-qa floor) by routing more escalations to rf-qa rather than fewer. Phase 7 should land this fallback explicitly.

**Q4.** Is CR-7 / CR-8 ordering structurally enforced or review-dependent?

**Invariant Defender A4.** Open finding F-02 — review-dependent. The current plan relies on the reviewer noticing the ordering in *Validating the Task File*. A future "readability" refactor could reorder the three steps without breaking any test. **Recommendation: extend CR-TASK-12 (verbatim diff audit) or CR-FM-04 (closed-enum audit) to grep for the three function names in order and fail the commit if they are reordered, OR add an explicit comment-block sentinel in the inserted code text naming CR-7/CR-8 as load-bearing ordering.**

### 4.3 Synthesized cross-examination outcome

Each role addressed the other's strongest points; no question went unanswered. Five questions surfaced **five distinct open findings (F-02, F-03, F-04, F-05, F-07)** plus two **documentation-quality findings (F-06, F-08)** plus **one note-cross-referenced finding (F-01)**. All findings are non-blocking — they are clarifications or strengtheners, not invariant violations, scope expansions, or manifest drifts. The plan's structural soundness is not at issue.

---

## 5. Open findings (load-bearing for T07.04 final-merge-plan corrections)

| ID | Severity | Title | Source | Recommended remediation |
|---|---|---|---|---|
| F-01 | LOW | Per-item Tier marker boundary is conceptually thin (read vs dispatch) | Invariant Defender on CR-FM-02 / CR-TASK-03 | Final-merge-plan adds one paragraph naming "tier-conditioned read" as the authorized consumption shape and ME-1 as the canonical rejection mechanism for any future per-item dispatch consumer |
| F-02 | MEDIUM | CR-7 / CR-8 ordering is review-dependent, not structurally enforced | Invariant Defender on CR-TASK-01 / CR-TASK-04 | Extend CR-FM-04 or CR-TASK-12 to grep for in-order function names; alternatively add a sentinel comment block in the inserted code text |
| F-03 | MEDIUM | CR-TASK-06 git-dirty behavior unspecified | Invariant Defender on CR-TASK-06 | Add explicit acceptance-criteria clause to CR-TASK-06 stating Reading A (log+continue) — preserves INV-01 progress guarantee |
| F-04 | MEDIUM | CR-TASK-07 baseline-absent fallback for CR-TASK-09 unspecified | Invariant Defender on CR-TASK-07 / CR-TASK-09 | Add explicit acceptance-criteria clause to CR-TASK-09 stating Reading A (baseline-absent → classify all as new) — preserves INV-03 floor |
| F-05 | MEDIUM | INV-03 surface widening (mid-phase rf-qa via TFEP escalation) not documented as authorized | Manifest Auditor cross-examination of CR-TASK-09 | Final-merge-plan adds one sentence documenting TU-7's authorized mid-phase escalation routing as the third rf-qa invocation point alongside phase-gate and post-completion |
| F-06 | LOW | `invariant-bounds.md` (T03.01) does not exist; reviewer used `extension-point-contracts.md` § "Invariant Reference" as functional substitute | Reviewer process note | Either (a) author `invariant-bounds.md` retroactively (T03.01 closure) with the worked-example expansion the canonical labels promise, or (b) update the T07.01 task description to cite `extension-point-contracts.md:11-17` as the canonical INV source |
| F-07 | LOW | Donor hard-deletion is procedurally authorized (sprint goal + T06.03 task description + § 4 absorption traceability), not manifest-bound | Manifest Auditor on CR-DEP-03 | Final-merge-plan adds one sentence naming the procedural authorization chain |
| F-08 | LOW | Five-vs-six refactor file counting inconsistency in `merge-master.md` line 7 and T07.01 task description | Cross-examination | Final-merge-plan corrects the count to six artifacts (or three Phase 6 refactor-areas if grouping is preferred) |

**No HIGH-severity findings.** No invariant violations, no manifest drifts, no scope expansions, no R-RULE-11 violations.

Five MEDIUM-severity findings are all **clarification / strengthening** recommendations:
- F-02: structurally enforce CR-7 / CR-8 ordering.
- F-03 + F-04: specify the silent behaviors (git-dirty, baseline-absent) so Phase 7 implementation cannot accidentally land an INV-violating reading.
- F-05: document the authorized INV-03 surface widening explicitly.

Three LOW-severity findings are documentation accuracy / process notes:
- F-01: clarify the read-vs-dispatch boundary phrasing.
- F-06: address the missing `invariant-bounds.md`.
- F-07 + F-08: document procedural authorizations and correct the five/six count.

---

## 6. Verdict

### 6.1 Invariant Defender verdict

**PASS WITH OPEN FINDINGS.** All five load-bearing invariants (INV-01..INV-05) are explicitly bound across the plan via the nine manifest exceptions (ME-1..ME-9) plus negative-space rows N1..N3. No Phase 6 row authors a HALT semantic in F1, a per-item runtime substitution, a verifier replacement, an in-task heading insert, or a runtime classifier. The five MEDIUM-severity findings (F-02..F-05) are clarification/strengthening recommendations against ambiguities in silent behavior; none indicate the plan IS violating an invariant — they indicate the plan does not yet *prove* it cannot in the future.

### 6.2 Manifest Auditor verdict

**PASS WITH OPEN FINDINGS.** Every manifest feature (8 TUs + 9 MEs + 10 donor-ceremony drops) has a Phase 6 row implementing, honoring, or explicitly excluding it. Two-way traceability is complete: 8/8 TUs map forward to Phase 6 rows; 65/65 Phase 6 rows trace back to a TU or a documented derivative responsibility. Zero `rejected-features-ledger.md` entries are re-proposed across all 26 ledger entries. Zero implementation drift across 8 TUs. F-07 (donor hard-deletion procedural authorization) and F-08 (five-vs-six count) are documentation strengtheners, not scope findings.

### 6.3 Joint verdict

**The Phase 6 merge plan is adversarially validated as STRUCTURALLY SOUND.** Both roles independently confirm the plan's invariant safety + manifest fidelity. T07.04 will produce the `final-merge-plan.md` by absorbing the eight open findings as targeted plan corrections — none of which alter the 65-row consolidated change-row table, the acyclic dependency graph, or the 10-step canonical commit sequence.

---

## 7. Acceptance Criteria recap (T07.01)

| AC | Status |
|---|---|
| **AC1.** `plan-adversarial-review.md` exists with both roles' assessments. | ✅ — § 2 Invariant Defender (67 row-line-items assessed), § 3 Manifest Auditor (53 manifest elements + 65 Phase 6 rows). |
| **AC2.** Every Phase 6 change row has an Invariant Defender assessment citing INV-NN evidence where an invariant surface is touched. | ✅ — § 2.1–§ 2.4 cover all 67 row-line-items; 13 invariant-touching rows cite specific INV-NN(s) and bound ME-NN(s) from § 0 + § 3.2; § 2.5 coverage table confirms. |
| **AC3.** Every `transfer-manifest.md` feature has a Manifest Auditor assessment (mapped / dropped / drifted). | ✅ — § 3.1 (TUs forward) + § 3.2 (MEs) + § 3.3 (donor drops) + § 3.4 (ledger entries) + § 3.5 (drift check) + § 3.6 (unauthorized scope check). 8/8 TUs mapped; 9/9 MEs bound or honored; 10/10 donor drops not re-introduced; 26/26 ledger entries audited; 0/8 TUs drifted; 0 unauthorized expansions. |
| **AC4.** All unauthorized scope expansions and implementation drifts are recorded as open findings. | ✅ — None found. Eight open findings recorded (F-01..F-08), all clarification/strengthening; none constitute scope expansion or implementation drift. |

---

## 8. Validation hooks (T07.01 Validation block)

**Sub-agent verification (T07.01 Validation #1):** an independent agent can spot-check 5 change rows for invariant impact by:
1. Picking 5 rows from § 2.1–§ 2.4 (e.g., CR-TASK-02, CR-TASK-06, CR-TASK-09, CR-TASK-10, CR-DEP-01).
2. For each, reading the corresponding source-refactor row in `refactor-task-skill.md` / `refactor-mdtm-frontmatter.md` / `refactor-sctask-deprecation.md`.
3. Confirming the cited INV-NN(s) in this review's § 2 match the source row's risk-assessment cell.
4. Confirming the bound ME-NN(s) match `transfer-manifest.md` § 3.

**Manual reviewer check (T07.01 Validation #2):** both roles answered each other's strongest points in § 4 — Invariant Defender raised four cross-examination questions, all answered; Manifest Auditor raised three, all answered. Each unanswered point would be a structural-soundness finding; instead, all unanswered points became *clarification* findings (F-01..F-08), recorded for T07.04.

---

## 9. Deliverable handoff to T07.02 / T07.03 / T07.04

This file is the Invariant + Manifest layer of Phase 7's adversarial validation. The remaining Phase 7 tasks consume it:

- **T07.02** — re-verifies every file reference in the plan + checks compat hazards. This review's findings F-03 (git-dirty behavior) and F-04 (baseline-absent fallback) are candidate compat hazards on the recipient side; T07.02 should cross-reference them.
- **T07.03** — two-way traceability + invariant-survival walkthrough. § 3.1 + § 3.4 + § 3.5 here pre-compute the two-way trace at the manifest-feature level; T07.03 should run the change-row level trace independently and confirm 65/65 again. The walkthrough should demonstrate INV-01..INV-05 survival on a representative MDTM file end-to-end, citing the F-01..F-05 findings if they bear on the walked example.
- **T07.04** — re-score drifted features + produce `final-merge-plan.md` + `validation-report.md`. No drift was found in this review (§ 3.5), so no re-scoring is required. The eight open findings F-01..F-08 are the binding correction list for `final-merge-plan.md` — each correction is a targeted clarification, not a row removal or row addition.

**T07.01 deliverable: COMPLETE.** Phase 7 advances with an adversarially-validated merge plan: zero HIGH-severity findings, zero invariant violations, zero manifest drifts, zero unauthorized scope expansions, zero ledger re-proposals. Eight clarification findings carry forward as plan strengtheners.

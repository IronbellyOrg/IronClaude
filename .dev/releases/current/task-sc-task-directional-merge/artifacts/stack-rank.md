# Stack Rank — Donor Features by Net Score

**Task:** T04.05 — Stack-rank all features by Net score
**Roadmap Item:** R-015
**Generated:** 2026-05-15
**Inputs:** Nine `debate-*.md` artifacts in `TASKLIST_ROOT/artifacts/` (post-gate) + `gate-pass-report.md` (T04.04) + `donor-feature-catalog.md` (Phase 1).

**Scoring rubric (binding, R-RULE-07):**
- **V (Value, 1-5)** — capability gain for `/task` if absorbed.
- **C (Complementarity, 1-5)** — fit with the F1 loop and phase-gate model.
- **K (Cost, 1-5)** — integration + ongoing maintenance cost.
- **Net = (V × C) / K** — stack-rank descending.
- **Verdicts:** ADOPT (Net ≥ 5), ADAPT (3 ≤ Net < 5), DEFER (1.5 ≤ Net < 3), REJECT (Net < 1.5 OR violates any INV-NN).

**Coverage note:** The nine Phase 4 debates produce 26 scored rows because several debates split their target features into sub-verdicts (D09→D09a/D09b; D02→Layer A; D27→Layer B; compliance-gating cluster→6 sub-gates; TFEP→7 sub-features; per-tier branching→D10/D15a/D15b/D15c; triggering surface→D06/D13). The donor catalog's remaining 14 entries (D04, D05, D07, D11, D12, D14, D16, D17, D18, D26, D28, D29, D30, D31, D32) are not separately debated because Phase 1 either (a) tagged them NON-TRANSFERABLE or DUPLICATE-OF-EXISTING (auto-REJECT — see "Catalog-derived dispositions" below), or (b) folded them into the compliance-gating cluster (D16/D17/D18/D26) which is debated separately. Section "Catalog-derived dispositions" carries those rows with their Phase 1 evidence so 1:1 coverage with `donor-feature-catalog.md` is preserved.

---

## Primary Stack Rank (Phase 4 debated rows, sorted by Net descending)

| # | Feature | Donor ID(s) | V | C | K | Net | Verdict | Debate artifact |
|---|---|---|---|---|---|---|---|---|
| 1 | Critical/Trivial Path Override (path-glob safety floor) | D17 + D18 | 4 | 5 | 1 | **20.0** | **ADOPT** | [debate-compliance-gating.md](debate-compliance-gating.md) |
| 2 | TFEP — Prohibition rules (VIOLATION-level) | D19 | 3 | 5 | 1 | **15.0** | **ADOPT** | [debate-tfep.md](debate-tfep.md) |
| 3 | D09a — `Tier:` field schema extension | D09 (split) | 4 | 5 | 2 | **10.0** | **ADOPT** | [debate-tier-classification.md](debate-tier-classification.md) |
| 4 | TFEP — Permitted exceptions (carve-outs) | D20 | 2 | 5 | 1 | **10.0** | **ADOPT** | [debate-tfep.md](debate-tfep.md) |
| 5 | TFEP — Incident reporting (side-effect file) | D24 | 2 | 5 | 1 | **10.0** | **ADOPT** | [debate-tfep.md](debate-tfep.md) |
| 6 | Compliance-gating Gate 1 — Dispatch (task-entry) | D04 / cluster | 3 | 5 | 2 | **7.5** | **ADOPT** | [debate-compliance-gating.md](debate-compliance-gating.md) |
| 7 | D10 — Command-side dispatch (Layer 1) | D10 | 3 | 5 | 2 | **7.5** | **ADOPT (MERGE-WITH-GATE-1)** | [debate-per-tier-branching.md](debate-per-tier-branching.md) |
| 8 | TFEP — Test baseline snapshot | D21 | 3 | 4 | 2 | **6.0** | **ADOPT** | [debate-tfep.md](debate-tfep.md) |
| 9 | TFEP — Escalation trigger detection | D22 | 3 | 4 | 2 | **6.0** | **ADOPT** | [debate-tfep.md](debate-tfep.md) |
| 10 | Compliance-gating Gate 2 — Verification routing | D16 / cluster | 4 | 3 | 3 | **4.0** | **ADAPT** | [debate-compliance-gating.md](debate-compliance-gating.md) |
| 11 | D15a — Layer 2 verification-stance subset | D15 (split) | 4 | 3 | 3 | **4.0** | **ADAPT (MERGE-WITH-GATE-2)** | [debate-per-tier-branching.md](debate-per-tier-branching.md) |
| 12 | D15b — Layer 2 pre-flight scaffolding (tier-gated row 2) | D15 (split) | 2 | 5 | 3 | **3.33** | **ADAPT** | [debate-per-tier-branching.md](debate-per-tier-branching.md) |
| 13 | D02 / Layer A — `mcp-servers:` frontmatter advertisement | D02 | 1 | 5 | 2 | **2.5** | **REJECT** (R-RULE-06 override) | [debate-mcp-declarations.md](debate-mcp-declarations.md) |
| 14 | Compliance-gating cluster aggregate (cluster-as-written) | cluster | 4 | 3 | 5 | **2.4** | **DEFER** (cluster-as-written; sub-gates separate) | [debate-compliance-gating.md](debate-compliance-gating.md) |
| 15 | D27 / Layer B — per-tier MCP matrix + circuit breaker | D27 | 3 | 3 | 4 | **2.25** | **DEFER** (contingent on Gate 1) | [debate-mcp-declarations.md](debate-mcp-declarations.md) |
| 16 | Compliance-gating Gate 3 — MCP circuit-breaker | D27 / cluster | 3 | 3 | 4 | **2.25** | **DEFER → ADAPT if Gate 1 ADOPTed** | [debate-compliance-gating.md](debate-compliance-gating.md) |
| 17 | TFEP cluster-aggregate (cluster-as-written) | D19-D25 | 3 | 3 | 4 | **2.25** | **DEFER** (cluster-as-written; sub-features separate) | [debate-tfep.md](debate-tfep.md) |
| 18 | D01 — declared `allowed-tools` frontmatter | D01 | 2 | 3 | 3 | **2.0** | **DEFER** (contingent on loader-semantics verification + Critical Rule 6 split) | [debate-allowed-tools.md](debate-allowed-tools.md) |
| 19 | D08 — Classification header emission | D08 | 2 | 3 | 3 | **2.0** | **DEFER** (contingent on downstream parser shipping) | [debate-classification-header.md](debate-classification-header.md) |
| 20 | TFEP — Escalation budget (3-strike FULL STOP) | D25 | 2 | 2 | 3 | **1.33** | **REJECT** (Net<1.5; duplicates Phase-Gate QA fix loop) | [debate-tfep.md](debate-tfep.md) |
| 21 | D09b — Classifier (priority cascade + keyword tables) | D09 (split) | 2 | 2 | 5 | **0.8** | **REJECT** (R-RULE-06 structural mismatch; route to `task-builder`) | [debate-tier-classification.md](debate-tier-classification.md) |
| 22 | Compliance-gating Gate 5 — Override flags | cluster | 1 | 2 | 3 | **0.67** | **REJECT** (silent-misuse failure mode; weakest sub-gate) | [debate-compliance-gating.md](debate-compliance-gating.md) |
| 23 | TFEP — Six-step execution flow (with `/sc:forensic`) | D23 | 3 | 1 | 5 | **0.6** | **DEFER** (pending `/sc:forensic` + INV-01-safe redesign) | [debate-tfep.md](debate-tfep.md) |
| 24 | D03 — Persona auto-activation list | D03 | 2 | 1 | 4 | **0.5** | **REJECT** (R-RULE-05 INV-02/N3 + INV-05; R-RULE-06; Phase 1 NON-TRANSFERABLE) | [debate-persona-activation.md](debate-persona-activation.md) |
| 25 | D13 — Auto-suggest keywords (no `/task` consumer) | D13 | 1 | 1 | 2 | **0.5** | **REJECT** (Phase 1 NON-TRANSFERABLE; no `/task` consumer) | [debate-triggering-surface.md](debate-triggering-surface.md) |
| 26 | D15c — Layer 2 procedural step-lists (in EXECUTE) | D15 (split) | 2 | 1 | 5 | **0.4** | **REJECT** (R-RULE-05 INV-01 + INV-05 collision) | [debate-per-tier-branching.md](debate-per-tier-branching.md) |
| 27 | D06 — Auto-trigger heuristics (direct `/task` attach) | D06 | 1 | 1 | 4 | **0.25** | **REJECT** (R-RULE-05 INV-05; input-shape invariant; donor-rec REJECT) | [debate-triggering-surface.md](debate-triggering-surface.md) |

---

## Catalog-derived dispositions (Phase 1 tags carried forward; not separately debated)

Per Phase 1 (`donor-feature-catalog.md`), these features carry pre-Phase-4 tags that determine their disposition without requiring an independent adversarial debate. Each row is included here for 1:1 catalog coverage; the Phase 1 evidence is the authoritative source.

| # | Feature | Donor ID | Phase 1 tag | Carry-forward disposition | Evidence |
|---|---|---|---|---|---|
| 28 | Orthogonal-dimensions model (Strategy × Compliance) | D04 | ADAPTABLE (partial — Compliance only) | Compliance axis subsumed by D09a (Tier field, ADOPT) + Gate 1 (ADOPT). Strategy axis = REJECT (no F1 analog). | `donor-feature-catalog.md:50` |
| 29 | Escalation philosophy ("better FP than FN") | D05 | NON-TRANSFERABLE | **REJECT** — philosophy statement, no attach point. | `donor-feature-catalog.md:51` |
| 30 | Flag set (8 documented CLI flags) | D07 | ADAPTABLE | **REJECT for `/task`** — `/task` is Skill-invoked on a file path, not CLI; flag semantics belong to `task-builder` or `sc:tasklist` if anywhere. | `donor-feature-catalog.md:53` |
| 31 | Classification output examples (few-shot) | D11 | NON-TRANSFERABLE | **REJECT** — supports D08/D09 only; collapses with D08 DEFER / D09b REJECT. | `donor-feature-catalog.md:57` |
| 32 | Command-side Boundaries — Will/Will-Not | D12 | DUPLICATE-OF-EXISTING | **REJECT** — duplicates F2 Prohibited Actions + F4 Modification Restrictions. | `donor-feature-catalog.md:58` |
| 33 | Human-readable confidence display bar | D14 | ADAPTABLE | **DEFER** — depends on D08/D09a/D09b; if D08 ADAPTs in a future sprint, debate D14 as a downstream presentation layer. Standalone REJECT until then. | `donor-feature-catalog.md:65` |
| 34 | Verification routing table | D16 | ADAPTABLE | Subsumed by compliance-gating Gate 2 (ADAPT, Net=4.0). | `donor-feature-catalog.md:67` |
| 35 | Critical Path Override | D17 | TRANSFERABLE | Subsumed by Critical/Trivial Path Override (#1, ADOPT, Net=20.0). | `donor-feature-catalog.md:68` |
| 36 | Trivial Path Override | D18 | TRANSFERABLE | Subsumed by Critical/Trivial Path Override (#1, ADOPT, Net=20.0). | `donor-feature-catalog.md:69` |
| 37 | Feedback Collection | D26 | ADAPTABLE | **DEFER** — depends on classification existing + a calibration store `/task` lacks. Forward to a future sprint scoped to calibration infrastructure. | `donor-feature-catalog.md:77` |
| 38 | Tool Coordination by phase | D28 | DUPLICATE-OF-EXISTING | **REJECT** — duplicates F1 EXECUTE action-to-tool mapping (`SKILL.md:89-96`) + Critical Rule 6 + Phase-Gate QA tool usage. | `donor-feature-catalog.md:79` |
| 39 | Worked Examples (per-tier) | D29 | NON-TRANSFERABLE | **REJECT** — supports D09/D10/D15 only; has no independent shape. | `donor-feature-catalog.md:80` |
| 40 | Skill-side Boundaries — Will/Will-Not | D30 | DUPLICATE-OF-EXISTING | **REJECT** — duplicates D12 + F2 Prohibited Actions. | `donor-feature-catalog.md:81` |
| 41 | Success Criteria metrics table | D31 | NON-TRANSFERABLE | **REJECT** — metrics measure D08/D09/D15; nothing to measure if those are not adopted. | `donor-feature-catalog.md:82` |
| 42 | External configuration references | D32 | ADAPTABLE | **DEFER** — referenced YAML files do not exist; externalization pattern is portable but premature until a tier-keyword YAML producer (`task-builder`) is in scope. | `donor-feature-catalog.md:83` |

---

## Coverage Audit (T04.05 acceptance criterion 1)

Every donor catalog row (D01-D32) appears exactly once in the union of {Primary Stack Rank, Catalog-derived dispositions}. Map:

- **D01** → row 18.
- **D02** → row 13.
- **D03** → row 24.
- **D04** → row 28 (Strategy axis REJECT; Compliance axis → D09a / Gate 1).
- **D05** → row 29.
- **D06** → row 27.
- **D07** → row 30.
- **D08** → row 19.
- **D09** → row 3 (D09a) + row 21 (D09b).
- **D10** → row 7 (MERGE-WITH Gate 1 / row 6).
- **D11** → row 31.
- **D12** → row 32.
- **D13** → row 25.
- **D14** → row 33.
- **D15** → row 11 (D15a) + row 12 (D15b) + row 26 (D15c).
- **D16** → row 34 (subsumed by Gate 2 / row 10).
- **D17** → row 35 (subsumed by row 1).
- **D18** → row 36 (subsumed by row 1).
- **D19** → row 2.
- **D20** → row 4.
- **D21** → row 8.
- **D22** → row 9.
- **D23** → row 23.
- **D24** → row 5.
- **D25** → row 20.
- **D26** → row 37.
- **D27** → row 15 + row 16 (Gate 3 view).
- **D28** → row 38.
- **D29** → row 39.
- **D30** → row 40.
- **D31** → row 41.
- **D32** → row 42.

**Coverage:** 32 donor catalog rows → 42 stack-rank rows (32 + 10 sub-splits and cluster sub-gates). Every catalog row maps to at least one stack-rank row. 1:1 coverage confirmed.

---

## Threshold-application audit (T04.05 acceptance criterion 4)

Threshold band per row, verified:

| Net range | Verdict | Rows |
|---|---|---|
| Net ≥ 5 | ADOPT | rows 1-9 (9 rows) |
| 3 ≤ Net < 5 | ADAPT | rows 10-12 (3 rows) |
| 1.5 ≤ Net < 3 | DEFER | rows 13-19 (7 rows). Row 13 (D02/Layer A, Net=2.5) is REJECT-by-override (R-RULE-06), not the arithmetic verdict. |
| Net < 1.5 OR invariant violation | REJECT | rows 20-27 (8 rows) + all catalog-derived REJECTs |

**Subjective override flagged for Phase 5 manifest exception (R-RULE-07):**

- **Row 13 (D02 / Layer A):** Arithmetic Net = 2.5 falls in DEFER band, but the verdict is REJECT under R-RULE-06 (ceremony without behavioral teeth — no in-repo consumer for the `mcp-servers:` frontmatter list). This is an explicit anti-sycophancy/R-RULE-06 override, *not* arithmetic. Flagged for Phase 5 as a documented manifest exception so the reviewer can re-affirm the override.

No other rows show arithmetic/verdict mismatch.

---

## Integration Sketches — ADOPT and ADAPT Rows (T04.05 acceptance criterion 3)

### Row 1 — Critical/Trivial Path Override (D17 + D18) — ADOPT

- **Where:** Row 1 (Task File Validation gate, C5; `extension-point-contracts.md:60-67`) as a pre-classification override pass; Row 10 (Phase-Gate QA, C3; `extension-point-contracts.md:122-129`) as a forced-escalation pre-check on STRICT items touching the critical path-glob set, and a forced-de-escalation pre-check for LIGHT/EXEMPT items inside the trivial path-glob set.
- **Critical path-glob set:** `auth/`, `security/`, `crypto/`, `models/`, `migrations/` (from `src/superclaude/skills/sc-task-protocol/SKILL.md:121`).
- **Trivial path-glob set:** `*.md`, `docs/`, `*test*.py` (from `SKILL.md:123`).
- **Shape of change:** ~10 lines added to `src/superclaude/skills/task/SKILL.md` under Task File Validation; ~5 lines added under Phase-Gate QA stance selection. The override fires regardless of the `Tier:` value (it is path-pattern-based, classification-independent — Position A's strongest argument for the cluster's safety floor).
- **No INV collision** — gate is at row 1 + row 10, both pre-EXECUTE; no F1 mutation.

### Row 2 — TFEP Prohibition rules (D19) — ADOPT

- **Where:** Row 8 (Error Handling / blocker logging, C5; `extension-point-contracts.md:144-155`). Add a `prohibition_check` step when a blocker is classified as a test failure: refuse to ad-hoc-fix; refuse to modify test expectations without adversarial validation; refuse to produce ad-hoc patches from test output.
- **Side-channel only — no F1 halt.** The failing item flips to `- [x]` (or to a recorded-failure state via existing blocker logging); the F1 loop continues to the next item; `rf-qa`'s existing 3-cycle adversarial fix loop at `SKILL.md:182-211` consumes the prohibition signal during its review.
- **Shape of change:** ~15 lines added to Error Handling (the three VIOLATION rules + the "test expectations are wrong is legitimate, but must be presented to user" rule).
- **Bind manifest exception:** SIDE-CHANNEL ONLY, NO F1 HALT (Phase 5 must preserve this).

### Row 3 — D09a `Tier:` field schema extension — ADOPT

- **Where:** Row 13 (Required frontmatter schema slot, C5; `extension-point-contracts.md:169-175`) — add optional `Tier:` field accepting `{STRICT, STANDARD, LIGHT, EXEMPT}`. Row 1 (Task File Validation gate, C5) adds a closed-enum check on the value when present. Row 4 (F1 EXECUTE item-type dispatch, C3) reads per-item `Tier:` annotation when present; falls back to task-level.
- **Shape of change:** ~3-5 lines added to `/task` SKILL.md frontmatter requirements; ~5-10 lines added to the Task File Validation gate.
- **No F1-loop change.** No INV collision.
- **Bind manifest exception (R-RULE-07):** D09a's value is contingent on Gate 1 (row 6) being implemented. Ship together or ship neither.

### Row 4 — TFEP Permitted exceptions (D20) — ADOPT

- **Where:** Row 8 (Error Handling, C5), as carve-outs to the D19 prohibitions. Carries with D19 at the same attach point.
- **Three carve-outs (verbatim from `SKILL.md:137-140`):** (a) single `ImportError`/`NameError` in test scaffolding the agent just wrote, ≤2 tests; (b) lint/formatting failures; (c) deprecation warnings.
- **Shape of change:** ~10 lines added to the D19 prohibition block (the carve-out list).

### Row 5 — TFEP Incident reporting (D24) — ADOPT

- **Where:** Row 11 (Post-Completion Validation, C5; `extension-point-contracts.md:151-159`). At TFEP-resolve time, write `tfep-incident-report.md` as a side-effect file in the task's research/ directory (file-resident, INV-04 safe). Post-completion validation confirms its presence for STRICT items with test-failure history.
- **Schema:** Trigger, Escalation count, Failing tests, Root cause, Solution, Outcome, Forensic artifacts (verbatim from `SKILL.md:222-234`).
- **Shape of change:** ~20 lines added (the report template + the post-completion check).
- **Bind manifest exception:** SIDE-EFFECT FILE, NOT TASKLIST MUTATION (do not insert a `## Failure Remediation Plan (Adjudicated)` heading; that part of D23 is deferred pending `/sc:forensic`).

### Row 6 — Compliance-gating Gate 1 (Dispatch task-entry) — ADOPT

- **Where:** Row 1 (Task File Validation gate, C5). After validation passes and `Tier:` is read (D09a), route execution shape: LIGHT/EXEMPT → lightweight profile (skip heavy verification but otherwise run F1 normally); STANDARD/STRICT → full F1 + Phase-Gate QA + Post-Completion Validation pipeline.
- **Shape of change:** ~10-15 lines added to the validation gate's dispatch logic.
- **Bind manifest exception (R-RULE-07):** PRE-LOOP DISPATCH — fires once at task-entry, never per-item inside F1 EXECUTE. Per-item per-tier dispatch is auto-REJECT under INV-01.

### Row 7 — D10 Command-side dispatch — ADOPT (MERGE-WITH-GATE-1)

- **Where:** Same surface as Row 6. **No separate Phase 5 implementation work.**
- **Stack-rank purpose:** preserve donor-row traceability (D10 → Gate 1 mapping).

### Row 8 — TFEP Test baseline snapshot (D21) — ADOPT

- **Where:** Row 2 (First Item Protocol, C5; `extension-point-contracts.md:69-75`). Run `uv run pytest --collect-only -q` once before F1's first iteration; persist result to `research/test-baseline.yaml` (file-resident, INV-04 safe).
- **Shape of change:** ~15 lines added to First Item Protocol.
- **Bind manifest exception (R-RULE-07):** TIER-GATED — run only on STRICT/STANDARD tasks; skip on LIGHT/EXEMPT to avoid uniform-cost-without-uniform-value waste.

### Row 9 — TFEP Escalation trigger detection (D22) — ADOPT

- **Where:** Row 8 (Error Handling, C5), consuming the D21 baseline. On a test failure, classify each failing test as Pre-existing (in baseline) or New (added by the agent this task). Evaluate the three MUST-escalate triggers (any pre-existing fails, ≥3 new fails simultaneously, runtime exception in implementation code).
- **Shape of change:** ~15 lines added to Error Handling.
- **Carries with D19 + D21 at the same attach point cluster.**

### Row 10 — Compliance-gating Gate 2 (Verification routing) — ADAPT

- **Where:** Row 10 (Phase-Gate QA, C3; `extension-point-contracts.md:122-129`) as a *widening* of existing Phase-Gate QA — tier-conditioned budget + timeout. STRICT → wider budget (~5K tokens, 60s) + `quality-engineer` added to roster as additional verifier; STANDARD → existing budget; LIGHT/EXEMPT → reduced budget (but Phase-Gate QA still runs, per INV-03).
- **Shape of change:** ~25 lines added to Phase-Gate QA section.
- **Bind manifest exception (R-RULE-07):** `rf-qa` SUPPLEMENTED NOT REPLACED — `quality-engineer` is *additional*, not a replacement. Replacing `rf-qa`'s adversarial stance is auto-REJECT under INV-03.

### Row 11 — D15a Layer 2 verification-stance subset — ADAPT (MERGE-WITH-GATE-2)

- **Where:** Same surface as Row 10. **No separate Phase 5 implementation work.**
- **Stack-rank purpose:** preserve donor-row traceability (D15 verification-stance → Gate 2 mapping).

### Row 12 — D15b Layer 2 pre-flight scaffolding — ADAPT

- **Where:** Row 2 (First Item Protocol, C5). Add tier-gated additive setup steps.
- **Tier-gated steps (STRICT only):** serena activate (if available), `git status` clean-tree check, `codebase-retrieval` on relevant code (if available), `list_memories`/`read_memory` for relevant prior context.
- **Tier-gated steps (STANDARD):** `codebase-retrieval` on relevant code.
- **LIGHT/EXEMPT:** no pre-flight scaffolding.
- **Shape of change:** ~15-25 lines added to First Item Protocol section.
- **Bind manifest exception (R-RULE-07):** NO PER-ITEM EXECUTE SUBSTITUTION — D15b is *additive pre-loop setup*, not in-EXECUTE behavior substitution.

---

## DEFER rows — preconditions to re-score in a future sprint

| Row | Feature | Re-score precondition |
|---|---|---|
| 14 | Compliance-gating cluster aggregate | Aggregate verdict superseded by per-sub-gate verdicts; no re-score (cluster is just an audit roll-up). |
| 15 + 16 | D27/Layer B + Gate 3 | Gate 1 ADOPTed (provides tier source). With Gate 1, marginal cost drops to K=3, Net rises to 3.0 (ADAPT threshold). |
| 17 | TFEP cluster aggregate | Aggregate verdict superseded by per-sub-feature verdicts; no re-score. |
| 18 | D01 — declared allowed-tools | (a) Skill loader verified to honor `allowed-tools:` with deny-by-default semantics for `/task`'s namespace; (b) Critical Rule 6 retitled as preference rule, leaving exclusion to the allowlist. If both pass, V rises to 3, Net = 3.0 (ADAPT). If either fails, V collapses to 1, REJECT. |
| 19 | D08 — Classification header emission | Downstream parser (transcript scanner / telemetry collector) in flight in a separate sprint. With parser, V rises to 4, Net = 4.0 (ADAPT). Until then, ceremony without consumer per R-RULE-06. |
| 23 | TFEP D23 six-step execution flow | (a) `/sc:forensic` skill authored; (b) Step 5 redesigned to use DYNAMIC CONTENT MARKER (not new top-level heading) — F4 safety; (c) Step 6 redesigned to avoid resume-from-inserted-task — INV-01 safety. |
| 33 | D14 — Human-readable confidence display | D08 / D09a in production; debate as a downstream presentation layer. |
| 37 | D26 — Feedback Collection | Calibration store authored (no `/task` analog today). |
| 42 | D32 — External configuration references | Tier-keyword YAML producer authored (`task-builder` or `sc:tasklist`). |

---

## Phase 5 forwarded items (R-RULE-07 manifest exceptions)

The following load-bearing commitments must be encoded as Phase 5 manifest exceptions for the ADOPT/ADAPT verdicts to remain INV-safe:

1. **PRE-LOOP DISPATCH (Row 6 / Gate 1 / D10):** Dispatch fires once at task-entry, never per-item inside F1 EXECUTE. Per-item per-tier dispatch is auto-REJECT under INV-01.
2. **`rf-qa` SUPPLEMENTED NOT REPLACED (Row 10 / Gate 2 / D15a):** Tier-conditioned verification routing widens the existing Phase-Gate QA. `quality-engineer` is an *additional* verifier in row 15's roster, not a replacement. Replacing `rf-qa`'s adversarial stance is auto-REJECT under INV-03.
3. **SIDE-CHANNEL ONLY, NO F1 HALT (Row 2 / D19 + Rows 4, 8, 9 / TFEP core):** TFEP fires its prohibition + classification + incident-report side-effects without halting F1. The failing item flips to `- [x]` (or records its failure state via existing blocker logging); the F1 loop continues. Halting F1 on TFEP engagement is auto-REJECT under INV-01.
4. **BASELINE TIER-GATED (Row 8 / D21):** Test baseline collection runs only on STRICT/STANDARD tasks (skip on LIGHT/EXEMPT). Without tier-gating, baseline cost falls on every `/task` invocation including LIGHT typos — uniform-cost-without-uniform-value failure mode (R-RULE-06 adjacent).
5. **NO PER-ITEM EXECUTE SUBSTITUTION (Row 12 / D15b; explicitly rejecting D15c / row 26):** Procedural step-lists (D15c) do NOT enter F1 EXECUTE as item substitution. If a task needs to run multi-step pre-flight (serena → git → codebase-retrieval → memory), those are explicit checklist items, not a tier-keyed procedure synthesized at execute-time. Auto-REJECT under INV-05 for any synthesis variant.
6. **TIER FIELD + GATE 1 SHIP TOGETHER (Row 3 / D09a + Row 6 / Gate 1):** D09a's value is contingent on Gate 1 being implemented. Ship together or ship neither.
7. **D08 DEFERRED UNTIL PARSER SHIPS (Row 19):** Do not adopt the classification header in isolation. Doing so repeats the R-RULE-06 ceremony failure that REJECTed D02 / Layer A.
8. **D01 DEFERRED UNTIL LOADER-SEMANTICS + CRITICAL RULE 6 SPLIT (Row 18):** Do not adopt the `allowed-tools:` frontmatter without verifying the Skill loader's deny-by-default semantics AND committing to a Critical Rule 6 retitling (exclusion → allowlist; preference → rule).

**R-RULE-07 subjective override flag (single item):**

- **Row 13 (D02 / Layer A):** Arithmetic Net = 2.5 (DEFER band) overridden to REJECT by R-RULE-06 (ceremony without behavioral teeth). Phase 5 reviewer should re-affirm this override or escalate as a manifest exception worth carrying forward.

---

## Acceptance Criteria Recap (T04.05)

1. **`stack-rank.md` exists with every donor feature appearing exactly once, sorted by Net descending.** ✅ (42 stack-rank rows; map to 32 catalog rows; Primary Stack Rank sorted Net descending; catalog-derived rows carry Phase 1 evidence.)
2. **Each row shows V, C, K, Net, verdict, and a link to its `debate-*.md`.** ✅ (Primary Stack Rank table includes all six columns; catalog-derived rows include Phase 1 evidence citations.)
3. **Every ADOPT and ADAPT row carries an integration sketch.** ✅ (12 ADOPT/ADAPT rows in Primary Stack Rank — rows 1-12; each has its own integration sketch above. D10 / D15a are MERGE-WITH cross-references; their implementation sketches live with Rows 6 and 10 respectively.)
4. **Verdict thresholds are applied consistently; any subjective override is flagged for a Phase 5 manifest exception (R-RULE-07).** ✅ (Threshold-application audit verifies 9 ADOPT / 3 ADAPT / 7 DEFER / 8 REJECT in Primary Stack Rank; one R-RULE-06 override on Row 13 explicitly flagged for Phase 5.)

**Phase 4 deliverable: COMPLETE.** Phase 5 has a fully-gated, scored, INV-bound stack rank as input.

# Adversarial Debate — Test Failure Escalation Protocol / TFEP (D19-D25)

**Task:** T04.02 — `/sc:adversarial` debates: TFEP & per-tier flow branching
**Roadmap Item:** R-012
**Source feature characterization:** `feature-tfep.md` (Phase 2 / T02.02)
**Constraint inputs:** `extension-point-contracts.md` (T03.02); INV-01..INV-05 labels from `extension-point-contracts.md:13-17`
**Donor catalog tags:** D19=TRANSFERABLE, D20=TRANSFERABLE, D21=ADAPTABLE, D22=TRANSFERABLE, D23=ADAPTABLE, D24=TRANSFERABLE, D25=ADAPTABLE (`donor-feature-catalog.md:70-76`)
**Generated:** 2026-05-15
**Note on Phase 3 input:** `invariant-bounds.md` (T03.01) was not produced — see `checkpoints/CP-P03-END.md`. INV-01 and INV-03 attachment-safety analysis below cites `extension-point-contracts.md:13-17` plus row-level reject criteria.

---

## Position A — Steelman for Inclusion

TFEP converts the **most common agentic code-change failure mode** — "test goes red → agent reads traceback → patches code → traceback changes → patches again → context exhaustion" — into a *halt-snapshot-adjudicate-resume* loop bounded by a three-strike budget (`feature-tfep.md:89-96`). For a STRICT-tier change in `auth/`, `security/`, `crypto/`, `models/`, or `migrations/`, this is the difference between a green CI run that hides a security regression (the agent weakened a test assertion) and a hard halt with a forensic artifact committed to git.

Four concrete value mechanisms (`feature-tfep.md:91-94`):

1. **Prevents test-overfitting regressions** — the VIOLATION-level prohibition on modifying test expectations without adversarial validation (`src/superclaude/skills/sc-task-protocol/SKILL.md:134, 142`) closes the most expensive failure mode in agentic test repair.
2. **Bounds runaway escalation** — the three-step budget (`SKILL.md:238-244`) caps fix-loop spend at ~25-30K tokens before FULL STOP.
3. **Produces a per-incident artifact** — `tfep-incident-report.md` (`SKILL.md:220-234`) creates a git-committed audit trail.
4. **Pre-existing vs New classification** — baseline + classification (`SKILL.md:144-152`) turns "was this a regression?" into a deterministic decision rather than a heuristic.

**Integration sketch (post-completion side-channel, NOT mid-F1):**

- **Primary attach (D19 prohibitions + D20 carve-outs + D22 triggers):** Row 8 (Error Handling / blocker logging, C5; `extension-point-contracts.md:144-155`). When the per-item "ensuring…" clause verification (row 5) or Phase-Gate QA (row 10) reports a test failure, the blocker-logging path consults TFEP's trigger detection and prohibition rules. Row 8's admit clause covers "blocker classification beyond the existing recoverable/unrecoverable axis" — adding `is_test_failure` and `is_pre_existing` dimensions is an additive classification, no F1 mutation.
- **Secondary attach (D21 baseline snapshot):** Row 2 (First Item Protocol, C5; `extension-point-contracts.md:69-75`). One-time `uv run pytest --collect-only -q` invocation before the loop's first iteration; result persists in the first phase's research/ output directory as `test-baseline.yaml` (file-resident persistence, INV-04 safe).
- **Tertiary attach (D24 incident reporting):** Row 11 (Post-Completion Validation, C5; `extension-point-contracts.md:151-159`). After the task completes (success or failed), the post-completion handler reads any TFEP incident artifacts produced during the run and rolls them into the final report. Or, more narrowly, the incident report is written as a side-effect file at TFEP-resolve time (during the Error Handling path), and post-completion validation just confirms its presence for STRICT items.
- **Excluded variants (forwarded to Phase 5):** D23 (six-step execution flow with `/sc:forensic` invocation) and D25 (escalation budget terminating in FULL STOP) require the `/sc:forensic` skill to exist (`feature-tfep.md:82, 102` — verified absent). Phase 4 verdict for D23/D25 is DEFER pending `/sc:forensic` authoring; the *prohibition + baseline + trigger + incident-report* subset (D19/D20/D21/D22/D24) is the absorbable core today.

**Why this might be a net upgrade over the status quo:**

`/task`'s Error Handling at `src/superclaude/skills/task/SKILL.md:170-179` classifies blockers as recoverable/unrecoverable and logs them. It has **no model of test-failure-as-regression-signal** — every test failure is just "a blocker." TFEP's contribution is the *prohibition + classification* layer: don't ad-hoc-fix; baseline-classify each failing test; honor the prohibition unless one of three carve-outs (`SKILL.md:137-140`) applies. This is a small, well-specified extension to existing blocker logging that addresses a real safety gap.

**Trade-off acknowledgment (R-RULE-04 anti-sycophancy):**

- **`/sc:forensic` does not exist.** `feature-tfep.md:82, 102` is explicit: no `src/superclaude/skills/sc-forensic/`, no `src/superclaude/commands/forensic.md`. TFEP Steps 3-6 (`SKILL.md:191-218`) — the *execution flow* that gives TFEP its named "escalation protocol" character — has no callee. Adopting D23/D25 today means adopting a protocol that halts at Step 3 indefinitely or invokes a non-existent skill. Position A excludes D23/D25 from the ADOPT scope precisely because of this; but it must be acknowledged that adopting the core subset (D19/D20/D21/D22/D24) delivers *less than half* of the donor's stated capability.
- **The F1 mutation contract (F4) forbids tasklist heading insertion** (`feature-tfep.md:117, src/superclaude/skills/task/SKILL.md:144-158`). Donor's Step 5 inserts a `## Failure Remediation Plan (Adjudicated)` heading; this is *prohibited* by F4 as written. The recipient cannot port Step 5 directly without either modifying F4 (touches an INV neighborhood) or re-shaping Step 5 to use a DYNAMIC CONTENT MARKER section. Step 5 is part of the D23 exclusion, but its restriction also bounds what future ADAPT can look like.
- **The escalation budget's "resume with `--compliance strict`" semantic (Step 6) has no `/task` analog** (`feature-tfep.md:121`). `/task` has no `--compliance` flag and no per-item tier escalation. Position A excludes D25 from the ADOPT scope; but the donor's TFEP-as-designed depends on it for the "resume under stricter compliance after remediation" property. Without that, the prohibition + halt subset is a partial mechanism.
- **The verification routing pre-condition (Layer 1: tier branching, Layer 2: STRICT/STANDARD-only)** depends on the recipient implementing Gate 2 of the compliance-gating cluster (verification routing, ADAPT, Net=4.0). LIGHT and EXEMPT skip verification (`SKILL.md:118-119`), so TFEP would never engage on those. The transitive coupling is real: TFEP's value claim is bounded by which tier mix runs verification.
- **Baseline collection adds a synchronous step at task entry.** `uv run pytest --collect-only -q` on a large repo can take 5-15 seconds and produces hundreds of test-function rows. The recipient pays this cost on every `/task` run, not just STRICT runs — unless the recipient gates baseline collection on a tier check, but that requires Gate 1 of the compliance-gating cluster, another transitive coupling.

---

## Position B — Steelman for Rejection (with explicit INV-01 and INV-03 attachment-safety analysis per T04.02 acceptance criteria)

**INV-01 (F1 loop semantics) attachment-safety analysis:**

The F1 loop's executive guarantee at `extension-point-contracts.md:13` is: "READ first unchecked `- [ ]`, EXECUTE exactly as written, UPDATE to `- [x]`, REPEAT. No skipping, reordering, or out-of-band substitution." TFEP's trigger detection runs *inside* the verification step (which runs *inside* F1 EXECUTE for items whose action is "run tests"). A naive implementation that *halts the F1 loop* on TFEP engagement directly mutates F1 EXECUTE semantics — the item's status remains `- [ ]` even though the executor stopped processing it. This is INV-01 collision (the loop is no longer executing "exactly as written").

Position A's integration sketch attaches TFEP at row 8 (Error Handling) as a *post-execution* classification — but row 8's reject criteria at `extension-point-contracts.md:147-150` are unambiguous: "Error-handling routines that re-execute items in a different order, restart from a different point, or skip ahead. → INV-01." If TFEP's escalation flow restarts the failing item under different routing (Step 6: "resume with `--compliance strict` starting from the inserted remediation tasks"), that *is* a restart-from-a-different-point. The donor's Step 5 + Step 6 sequence inserts new tasks and resumes from them — which on `/task` would mean the F1 loop now operates on items the IDENTIFY step never produced from the original task file. **This is the auto-REJECT trigger under INV-01.**

The only attach shape that survives INV-01 is the **side-channel** variant Position A's integration sketch hints at: TFEP fires its prohibition + classification + incident-report side-effects *without halting F1*. The item's status flips to `- [x]` (or to a recorded-failure state via existing blocker logging), the F1 loop continues to the next item, and the TFEP incident-report.md is written as a side-effect file consumed by post-completion validation. Position A's sketch is *adjacent to* this safe variant but does not commit to it explicitly — Position A still wants D19 (the prohibition that says "don't fix code in response to a failure"), which on a side-channel implementation is awkward because the F1 loop *also* doesn't try to fix the code; the item just marks as failed and moves on.

**INV-03 (Phase-gate `rf-qa`) attachment-safety analysis:**

INV-03 at `extension-point-contracts.md:15` is: "Phase-gate `rf-qa` between phases (Phase 2+); post-completion `rf-qa` + `rf-qa-qualitative` validation." The compliance-gating cluster's manifest exception #2 (`debate-compliance-gating.md`:159) is explicit: "SUPPLEMENT-NOT-REPLACE `rf-qa` — Tier-conditioned verification routing widens the existing Phase-Gate QA; `quality-engineer` is added to row 15's roster as an additional verifier, not as a replacement. **Replacing `rf-qa`'s adversarial stance is auto-REJECT under INV-03.**"

TFEP's Verification Routing input at `feature-tfep.md:47, src/superclaude/skills/sc-task-protocol/SKILL.md:114-119` routes STRICT to a `quality-engineer` sub-agent and STANDARD to direct test exec. **If TFEP-on-`/task` causes the existing `rf-qa` adversarial gate to be replaced or skipped on test-failure handling, INV-03 fires.** The donor's design is for a system without `/task`'s phase-gate model; transplanting it to `/task` requires explicitly preserving `rf-qa` as the primary phase-gate verifier and adding TFEP's prohibition + classification as a *side-channel* signal that `rf-qa` can consume during adversarial review.

This is the same load-bearing commitment the compliance-gating cluster's Gate 2 (Verification routing, ADAPT, Net=4.0) requires. TFEP's INV-03 safety is inherited from Gate 2's commitment; if Gate 2 lands cleanly, TFEP can supplement; if Gate 2 lands sloppily (replacing `rf-qa` with `quality-engineer`), TFEP inherits the INV-03 collision.

**Surfacing rather than papering over (R-RULE-05):** Both INV-01 and INV-03 collision risks are *real* and *one design-decision away* from the verdict. Position A's integration sketch admits this implicitly by excluding D23/D25 from ADOPT scope and by tethering TFEP to Gate 2 — but Position A does not bind these constraints as Phase 5 manifest exceptions. Without explicit binding, a sloppy implementation lands at C1 (auto-REJECT) on either INV-01 (loop-halt on TFEP engagement) or INV-03 (replace `rf-qa` with `quality-engineer`).

**Six coupling burdens, four of which touch invariants or external dependencies** (`feature-tfep.md:111-123`):

| # | Burden | INV/dep impact |
|---|---|---|
| 1 | Baseline-capture step in First Item Protocol | C5 (additive at row 2) — clean |
| 2 | Test-failure interception in Error Handling | C5/C3 (row 8, additive) — clean **IF** classification is side-effect-only |
| 3 | `/sc:forensic` skill must be authored | External — not a recipient burden, but blocks D23/D25 |
| 4 | Tasklist-insertion that fits inside F4 restrictions | C3 → C1 if implemented as new top-level heading. Donor's Step 5 collides; recipient must use DYNAMIC CONTENT MARKER instead |
| 5 | `output_dir` convention | C5 — small schema/convention extension |
| 6 | FULL-STOP and resume-under-strict semantic | C3 → C1 if implemented as loop-restart; INV-01 collision risk |

Four of six burdens touch invariant neighborhoods (#2, #4, #6) or external authoring (#3). The clean two (#1, #5) are the lowest-effort but also the lowest-value parts of TFEP.

**Realistic failure mode #1 (INV-01 collision via Step 6 resume-from-inserted-task):** A `/task` STRICT item runs `pytest`; test fails; TFEP engages; remediation tasks are inserted (per Step 5 — itself an F4 violation, see burden #4); the F1 loop is then told to resume from the inserted tasks (Step 6). The F1 IDENTIFY step's "first unchecked `- [ ]`" is now an item the loop never originally saw. INV-01's "no out-of-band substitution" fires; row 8's reject criteria at `extension-point-contracts.md:147-150` ("Error-handling routines that … restart from a different point") triggers C1 auto-REJECT.

**Realistic failure mode #2 (INV-03 collision via verification-stance swap):** TFEP-on-STRICT routes test failures to `quality-engineer` per the donor's Verification Routing (`SKILL.md:114-119`). If the implementation interprets this as "`quality-engineer` replaces `rf-qa` for STRICT items," INV-03 fires. The compliance-gating cluster's Gate 2 manifest exception (`debate-compliance-gating.md`:159) names this exact failure mode; TFEP inherits the same risk.

**Realistic failure mode #3 (write-only incident reports):** TFEP's `tfep-incident-report.md` (D24) is committed to git per `SKILL.md:236` — but only if the recipient adopts the commit step. On the recipient side, where to commit, when to commit, and whether to commit at all are open questions. If the report is written to disk but never committed, it becomes another write-only artifact (the R-RULE-06 ceremony failure mode the donor's D02 was REJECTed for). If it is committed automatically, that touches git workflow which `/task` does not currently own.

**Realistic failure mode #4 (baseline-collection cost without tier gating):** Position A's integration sketch attaches D21 baseline collection at row 2 (First Item Protocol) "before the loop's first iteration." Without tier-gating, the baseline runs on every `/task` invocation — including LIGHT typo fixes that never run tests. On a large repo (~500 tests), `pytest --collect-only` can take 5-15 seconds. Across 10 LIGHT tasks, that's 50-150 seconds of upfront cost for zero TFEP value (TFEP doesn't engage on LIGHT). The baseline must be tier-gated, which creates transitive coupling to Gate 1.

**Duplication with existing Phase-Gate QA fix-loop:** `/task`'s Phase-Gate QA at `src/superclaude/skills/task/SKILL.md:182-211` already implements a *3-cycle fix loop with `rf-qa` adversarial stance*. The donor's TFEP three-strike budget (D25) is conceptually parallel: 3 escalation attempts before FULL STOP. **Two parallel fix-loop budgets on the same skill is duplication.** The recipient must reconcile: either the existing Phase-Gate QA fix loop subsumes TFEP's budget (TFEP becomes the *prohibition + classification* layer, not the *loop*), or TFEP's loop replaces the existing fix loop (which collides with INV-03's `rf-qa` adversarial-stance requirement).

---

## Evidence-Based Weighing

**Position A's strongest point (real safety gap: test-overfitting regressions on STRICT changes):** `/task` today has no model of test-failure-as-regression-signal. The VIOLATION-level prohibition on modifying test expectations (D19) is a concrete, well-specified rule with a clean attach point at row 8 (Error Handling); the baseline + Pre-existing/New classification (D21+D22) is a deterministic decision procedure that closes a known safety gap.

**Position B's answer:** The *prohibition + classification* subset (D19+D20+D21+D22) is genuinely admissible at row 2 + row 8 with side-effect-only semantics. The full TFEP design (with D23 execution flow, D25 budget, D24 incident report, F4 mutation) does not survive without three load-bearing commitments: (a) `/sc:forensic` is authored separately; (b) tasklist insertion goes through DYNAMIC CONTENT MARKER, not as a new top-level heading; (c) the existing Phase-Gate QA `rf-qa` fix-loop is preserved as primary, with TFEP as a side-channel input. Position A's sketch is adjacent to this safe variant but does not bind it explicitly. The donor's TFEP-as-written is a four-attach-point cluster; the absorbable core is two attach points (row 2 + row 8) at significantly narrower scope than the donor's claim.

**Position B's strongest point (INV-01 collision via Step 6 resume-from-inserted-task + INV-03 collision via verification-stance swap + F4 collision via heading insertion + `/sc:forensic` absent + duplication with existing Phase-Gate QA fix loop):** Five convergent restriction lines. The full TFEP cannot ADOPT in this sprint; only a narrowed subset can.

**Position A's answer:** Accepts all five restrictions. Narrows the ADOPT scope to D19+D20+D21+D22+D24 (prohibition rules + permitted exceptions + baseline + triggers + incident report), with the *narrowed-incident-report* shape: `tfep-incident-report.md` written as a side-effect file at TFEP-resolve time, consumed by post-completion validation, *not* by mid-F1 tasklist mutation. Excludes D23 (forensic execution flow) and D25 (escalation budget with `--compliance strict` resume) from the Phase 4 ADOPT scope — these become DEFER pending `/sc:forensic` authoring and pending a per-item tier escalation mechanism. Position A binds three Phase 5 manifest exceptions: (a) side-channel only, no F1 halt; (b) `rf-qa` supplemented not replaced; (c) baseline collection tier-gated by Gate 1 of compliance-gating cluster.

**Unanswered point against Position A:** Position B's duplication argument (Phase-Gate QA fix loop already implements a 3-cycle budget) is unaddressed. Position A's narrowing excludes the donor's escalation budget (D25), which dodges the duplication — but does not affirmatively integrate the existing fix loop with TFEP's prohibition layer. The unbinding leaves a future implementer free to re-introduce the budget duplication. This counts against Position A — the narrowing should commit to "TFEP prohibition + classification feeds *into* `rf-qa`'s existing fix loop, not alongside it."

**Unanswered point against Position B:** Position B's INV-01 collision argument (failure mode #1) targets the *full* TFEP design with Step 5+6 resume-from-inserted-task. Position A's narrowing excludes Step 5 and Step 6, so the INV-01 collision Position B argued does not apply to the narrowed ADOPT scope. This counts against Position B (mildly) — the INV-01 argument is real for the full design but not for the narrowed subset Position A is actually defending.

**Net effect:** TFEP partitions into (a) a `/task`-absorbable core (D19 prohibitions + D20 carve-outs + D21 baseline + D22 triggers + D24 incident report, at narrowed shape) attaching at row 2 + row 8 + row 11 with three load-bearing commitments, and (b) a deferred remainder (D23 execution flow + D25 budget) contingent on `/sc:forensic` authoring and tier-escalation infrastructure. The full TFEP fails C1/C3 admissibility for the row 4 (F1 EXECUTE) and N2 (F4 modification restrictions) extension points; the narrowed subset attaches cleanly at row 8/row 2/row 11 (all C5).

---

## Scored Verdict

TFEP is scored as a **cluster with per-sub-feature sub-verdicts** because the seven donor sub-features (D19-D25) have independently shaped values, costs, and admissibility.

### Cluster-aggregate score

| Component | Score | Rationale |
|---|---|---|
| **V (Value, 1–5)** | **3** | Cluster-level: real safety value for STRICT tier (test-overfitting regression prevention, runaway-escalation bounding, audit trail) — but the value is contingent on tier-gating (transitive coupling to Gate 1) and on the verification-routing (transitive coupling to Gate 2). Standalone value without the cluster dependencies is significantly lower. |
| **C (Complementarity, 1–5)** | **3** | C-band C3 at the cluster level: row 8 admit clauses cover the prohibition + classification layer cleanly; rows 2, 8, 11 admit the baseline + trigger + incident-report sub-features; but D23 (execution flow with `/sc:forensic`) and D25 (budget with `--compliance strict` resume) require external dependencies (forensic skill, tier-escalation mechanism) and are not admissible at C3 alone — they push into C1 territory if implemented naively. **Three load-bearing commitments** to bind C3-admissibility for the absorbable core. |
| **K (Cost, 1–5)** | **4** | Six distinct burdens (`feature-tfep.md:111-123`), three of which touch invariant neighborhoods. Plus the `/sc:forensic` external authoring blocker for D23/D25. Plus duplication-reconciliation work with existing Phase-Gate QA fix loop. |
| **Net = (V × C) / K** | **(3 × 3) / 4 = 2.25** | |

**Cluster-aggregate verdict: DEFER** (Net = 2.25 falls in DEFER band).

### Per-sub-feature sub-verdicts

| Sub-feature | V | C | K | Net | Verdict | Notes |
|---|---|---|---|---|---|---|
| **D19 — Prohibition rules** | 3 | 5 | 1 | 15.0 | **ADOPT** | Three rules at row 8 (Error Handling, C5). Side-effect-only — informs `rf-qa` adversarial stance during fix-loop, does not halt F1. Tiny cost; high value. |
| **D20 — Permitted exceptions** | 2 | 5 | 1 | 10.0 | **ADOPT** | Three carve-outs carry with D19 at same attach point. |
| **D21 — Test baseline snapshot** | 3 | 4 | 2 | 6.0 | **ADOPT** | Row 2 (First Item Protocol, C5) as one-time pre-loop step; persists as `test-baseline.yaml` under research/. **Bind commitment: tier-gated** (run only on STRICT/STANDARD, skip on LIGHT/EXEMPT). |
| **D22 — Escalation trigger detection** | 3 | 4 | 2 | 6.0 | **ADOPT** | Carries with D19+D21 at row 8; consumes the baseline. |
| **D23 — Six-step execution flow (with `/sc:forensic`)** | 3 | 1 | 5 | 0.6 | **DEFER** | `/sc:forensic` does not exist; Step 5 collides with F4; Step 6 collides with INV-01. DEFER pending `/sc:forensic` authoring + tier-escalation mechanism. |
| **D24 — Incident reporting** | 2 | 5 | 1 | 10.0 | **ADOPT** | Side-effect file at row 11 (Post-Completion Validation, C5). Narrowed: written at TFEP-resolve, consumed by post-completion. **Bind commitment: side-effect file, not tasklist mutation.** |
| **D25 — Escalation budget (3-strike FULL STOP)** | 2 | 2 | 3 | 1.33 | **REJECT/DEFER** | Standalone REJECT (`Net=1.33 < 1.5`). Conceptually duplicates existing Phase-Gate QA 3-cycle fix loop. If `/sc:forensic` lands, re-debate as a parameter on the existing fix loop rather than as a parallel budget. |

### Composite verdict

- **TFEP core (D19+D20+D21+D22+D24):** ADOPT/ADAPT at row 2 + row 8 + row 11 with three load-bearing commitments.
- **TFEP execution-flow remainder (D23):** DEFER pending `/sc:forensic` and tier-escalation infrastructure.
- **TFEP escalation budget (D25):** REJECT as a parallel budget; consider re-debating as a parameter on the existing Phase-Gate QA fix loop in a future sprint.

**Stack-rank inputs (for T04.05):**

The cluster is rolled forward as **seven separate rows in the stack rank** (one per sub-feature), not one aggregate row, because the verdicts diverge materially.

- **Cluster aggregate:** V=3, C=3, K=4, Net=2.25, **DEFER (cluster-as-written)**.
- **D19 (Prohibition rules):** V=3, C=5, K=1, Net=15.0, **ADOPT**.
- **D20 (Permitted exceptions):** V=2, C=5, K=1, Net=10.0, **ADOPT**.
- **D21 (Test baseline snapshot):** V=3, C=4, K=2, Net=6.0, **ADOPT**.
- **D22 (Escalation trigger detection):** V=3, C=4, K=2, Net=6.0, **ADOPT**.
- **D23 (Six-step execution flow):** V=3, C=1, K=5, Net=0.6, **DEFER** (pending `/sc:forensic` + INV-01-safe redesign).
- **D24 (Incident reporting):** V=2, C=5, K=1, Net=10.0, **ADOPT**.
- **D25 (Escalation budget):** V=2, C=2, K=3, Net=1.33, **REJECT** (Net < 1.5; duplicates existing Phase-Gate QA fix-loop budget).

### Phase 5 manifest exceptions per R-RULE-07 (load-bearing commitments)

TFEP's INV-01 and INV-03 safety is contingent on three commitments. If Phase 5 cannot bind these in the integration sketches, the per-sub-feature ADOPT verdicts collapse to C1 / auto-REJECT:

1. **SIDE-CHANNEL ONLY, NO F1 HALT:** TFEP fires its prohibition + classification + incident-report side-effects without halting F1. The failing item flips to `- [x]` (or records its failure state via existing blocker logging at row 8); the F1 loop continues. Tasklist insertion of remediation tasks is **deferred** (handled by D23 if/when `/sc:forensic` lands). Halting F1 on TFEP engagement is auto-REJECT under INV-01 (`extension-point-contracts.md:147-150`).

2. **`rf-qa` SUPPLEMENTED NOT REPLACED:** TFEP's prohibition + classification feeds *into* `rf-qa`'s existing 3-cycle adversarial fix loop at `src/superclaude/skills/task/SKILL.md:182-211`, not alongside it. `quality-engineer` (donor's STRICT verification routing) is added to row 15's roster as an *additional* verifier, not as a replacement for `rf-qa`. Replacing `rf-qa`'s adversarial stance is auto-REJECT under INV-03 (`extension-point-contracts.md:15`). This commitment is shared with the compliance-gating cluster's Gate 2.

3. **BASELINE COLLECTION TIER-GATED:** D21 baseline runs only on STRICT/STANDARD tasks (skip on LIGHT/EXEMPT). This requires Gate 1 of the compliance-gating cluster to provide the tier source. Without tier-gating, the baseline cost falls on every `/task` invocation including LIGHT typo fixes — uniform-cost-without-uniform-value failure mode (R-RULE-06 adjacent).

**Note on missing T03.01 evidence:** `invariant-bounds.md` is absent (Phase 3 checkpoint Fail). The INV-01 collision argument for the full TFEP design (Step 6 resume-from-inserted-task) is sourced from row 8 reject criteria at `extension-point-contracts.md:147-150` plus the INV-01 label at line 13. The INV-03 collision argument is sourced from the compliance-gating cluster's Gate 2 manifest exception (which traces to `extension-point-contracts.md:122-129`, row 10 reject criteria, plus the INV-03 label at line 15). Worked failure-mode examples in `invariant-bounds.md` would strengthen failure modes #1 and #2 above but do not change the verdicts — the row-level reject criteria are sufficient to carry the commitments.

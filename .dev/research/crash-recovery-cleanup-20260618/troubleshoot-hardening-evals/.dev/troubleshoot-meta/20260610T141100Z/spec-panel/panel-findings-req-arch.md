# Spec-Panel Findings — Requirements / Architecture / Integration / Ops Cluster

Mode: `/sc:spec-panel --mode critique`
Experts: Wiegers, Adzic, Cockburn, Fowler, Newman, Hohpe, Gregory, Hightower
Target: `troubleshoot-pipeline-hardening-spec.md` (G1 draft) + `EFFICACY-REPORT-MERGED.md`
Output root: `/config/workspace/IronClaude/.dev/troubleshoot-meta/20260610T141100Z`
Spec type: **infrastructure** → release-spec must populate §5.1 CLI surface, §5.2 gate criteria, §5.3 phase contracts, §8.3 E2E.

---

## PART A — Critique-Mode Findings

### === REQUIREMENTS ===

**R-1 — Waves are prose, not SMART verifiable FRs.**
Issue: §7 H0–H5 are described as narrative "required outputs / pass criteria / blocking rules," not as atomic, independently testable requirements. A reader cannot mechanically assert pass/fail per wave without re-interpreting prose.
Severity: **CRITICAL** · Wiegers.
Recommendation: split each wave into one-or-more atomic FRs, each with a title, a single verifiable behavior, and 2–3 acceptance criteria phrased as observable outcomes (status emitted, field present, blocking rule fired). Rationale: a hardening gate that cannot be mechanically checked re-creates the exact theatre the efficacy report (§4) indicts. Priority: **High**.

**R-2 — No explicit E1–E5 → wave → FR traceability matrix.**
Issue: §3 maps escapes to "required catcher" prose and §11 maps mechanism-to-escape, but there is no single forward/backward traceability table binding each canonical escape to the FRs that must hold to claim coverage. EFFICACY §5 is explicitly **predicted, not proven**, so coverage claims must be traceable to be auditable.
Severity: **MAJOR** · Wiegers.
Recommendation: add a traceability matrix E1–E5 × FR-ID with a "negative-witness required?" column. Rationale: §8 of the efficacy report establishes three escape sub-classes are *irreducibly un-catchable by reading alone* — traceability must record which FRs demand an execute/replay witness vs static check. Priority: **High**.

**R-3 — `pipeline_hardening_applicable=false` skip path is under-specified and abusable.**
Issue: §6.1 / H0 lets a "pure local bug fix" skip the mode with "a one-sentence reason," but does not bound what makes a reason sufficient, nor cap the false-positive (over-skip) rate. EFFICACY §4 names "exact runtime entrypoints were not mandatory" as the #1 theatre pattern; a soft skip re-opens it.
Severity: **MAJOR** · Wiegers + Gregory.
Recommendation: make the skip require a recorded boundary scan (the nine §6.1 trigger classes each marked absent) plus the mechanism statement; define an NFR target for applicability false-positive rate (<30%). Priority: **High**.

**R-4 — Verdict enum is loosely coupled to the gate outcomes.**
Issue: §6.2 `pipeline_hardening_verdict ∈ {pass, blocked, advisory, not_applicable}` but the report template §8 uses `{pass, blocked, advisory}` and individual gates use `PASS|FAIL|N/A`. The mapping from per-gate PASS/FAIL/N/A to the aggregate verdict is unstated (e.g. does one FAIL → `blocked`? does an unjustified `N/A` → `blocked`?).
Severity: **MAJOR** · Wiegers.
Recommendation: specify the aggregation function as an FR with a truth table; reconcile the enum sets across §6.2, §8, and the `partial` status introduced by the waiver policy (EFFICACY §10). Priority: **High**.

### === ARCHITECTURE ===

**A-1 — Interface segregation: thin command vs fat skill vs refs boundary is asserted but not enforced by an FR.**
Issue: §5.1/§10.1 say "keep the command thin" but nothing makes that a checkable requirement; the closure logic, ledger schemas, and proof cards all risk landing in `SKILL.md` and bloating it.
Severity: **MAJOR** · Fowler.
Recommendation: FR-ize the segregation — command file only advertises + triggers handoff; closure-card templates and ledger schemas live in `refs/*`; `SKILL.md` holds only the trigger + verdict-aggregation + output-contract. Acceptance: a line/section budget check on `SKILL.md`. Rationale: §9 already lists 5 new ref files — the boundary exists; it must be a contract, not a convention. Priority: **Med**.

**A-2 — Five waves are five bounded contexts; H1↔H4 and H2↔H4 overlaps are undefined.**
Issue: H1 (runtime-entrypoint) requires a "same-boundary negative control"; H3/H4 (unmask-and-sweep) requires a "negative witness"; H4-effective-input overlaps H1's "consumer/evaluator" record. Where these touch (e.g. the negative control of H1 vs the negative witness of H3) is not factored, inviting duplicated or contradictory evidence.
Severity: **MAJOR** · Fowler.
Recommendation: define each wave as a bounded context with an explicit shared-kernel (the contract record / seam shape from EFFICACY §10 Pact/CDC bullet) reused across H1/H2/H4 rather than re-specified per wave. Priority: **Med**.

**A-3 — Output-contract field set mixes verdict, evidence-paths, and decision enums without a schema version.**
Issue: §6.2 table is 8 fields of heterogeneous concern (one bool, two enums, four nullable paths, one list) with no declared schema/version. Architecturally this is a public contract surface (see N-1).
Severity: **MINOR** · Fowler + Newman.
Recommendation: group into a nested `pipeline_hardening: { applicable, verdict, evidence: {...paths}, off_path_review_decision, known_escapes_caught }` object with a `contract_version`. Priority: **Med**.

### === INTEGRATION ===

**N-1 — New output-contract fields are an unversioned contract with existing troubleshoot result consumers.**
Issue: §6.2 adds 8 fields to "the skill result" but the draft never states whether existing consumers of the troubleshoot result (REPORT.md renderer, remediation-handoff, any sprint/prd reader) tolerate additive fields, nor declares the fields **optional/additive-only**. EFFICACY §9 is literally a Contract Identity Ledger preaching producer/consumer parity — the spec must eat its own dogfood.
Severity: **CRITICAL** · Newman.
Recommendation: declare the new fields **optional, additive, backward-compatible**; require a consumer enumeration (who reads the troubleshoot result today) as an FR before adding fields; pin a `contract_version` so downstream can branch. Priority: **High**.

**H-1 — Verdict flow to REPORT.md and downstream (sc:reflect, adversarial, sprint/prd) is one-directional and unspecified.**
Issue: §8 adds a `Pipeline Hardening Closure` REPORT.md section, but how a `blocked`/`partial` verdict propagates to (a) sc:reflect post-audit, (b) an adversarial gate, (c) a sprint/prd consumer that might treat the troubleshoot as "done" is undefined. EFFICACY §10 waiver policy says a `partial` "may never be re-converted to success by a later task-builder, sc:reflect, or adversarial stage" — but no integration FR enforces that downstream.
Severity: **CRITICAL** · Hohpe.
Recommendation: specify the verdict as a **monotonic, downstream-visible signal**: REPORT.md is the channel; downstream stages must read the closure verdict and may only downgrade (`success`→`partial`→`blocked`), never upgrade. Make the no-re-greening invariant an integration FR, not just prose. Priority: **High**.

**H-2 — `known_escapes_caught` has no downstream consumer defined.**
Issue: the list field is produced but nothing consumes it; it risks being write-only audit decoration (the efficacy report's "audit artifacts without changing failure probability," §4).
Severity: **MINOR** · Hohpe.
Recommendation: either define a consumer (regression dashboard / coverage assertion in tests) or demote to evidence-only and say so. Priority: **Low**.

### === OPS ===

**O-1 — A waived runtime probe is not observably distinct from a passed one.**
Issue: §6.2 `off_path_review_decision` and §7 H5 waiver standard exist, but there is no operational signal that makes a *waived* probe visible at signoff. EFFICACY §10 mandates a waived probe → status `partial` and "production-facing pipeline-health signoff fails when a mandatory runtime probe is absent" — the draft's §8 report does not carry a machine-checkable `partial` status field.
Severity: **CRITICAL** · Hightower.
Recommendation: add a `pipeline_health_signoff ∈ {success, partial, blocked}` field whose value is `partial` whenever any mandatory probe is waived/`N/A`, and which is non-upgradable (ties to H-1). Make "waived" emit a distinct, greppable token in REPORT.md. Priority: **High**.

**O-2 — Added latency/token cost of hardening mode is unbounded and unmeasured.**
Issue: hardening adds H0–H5 cards, a ledger, sweeps, and possible off-path reviewer spawns. No NFR bounds the added cost, so operators cannot reason about when to enable it. EFFICACY §10 explicitly prefers "one focused live-seam probe per implicated seam plus one public-entrypoint smoke — not an expensive full end-to-end suite."
Severity: **MAJOR** · Hightower.
Recommendation: NFR a token/latency ceiling for hardening mode relative to a baseline Tier-1 troubleshoot; prefer single-seam probes. Priority: **Med**.

**O-3 — Mechanical enforcement of no-re-greening is an open research question, shipped as prose.**
Issue: EFFICACY Appendix A open questions explicitly list "the mechanical enforcement that keeps a waived probe from being re-greened by a downstream stage" as unresolved. The draft encodes the *rule* but not the *enforcement*, so at G1 the single most important anti-theatre control has no implementation mechanism.
Severity: **MAJOR** · Hightower + Gregory.
Recommendation: carry as an explicit Open Item with an owner; until mechanized, signoff must be advisory-flagged. Priority: **High**.

### === DEFINITION-OF-DONE (Gregory, three-amigos) ===

**G-1 — "Pipeline escape remediated" lacks a shared DoD.** A fix author, a reviewer, and the protocol can each read §10's 10 acceptance criteria differently (esp. #6 "any escape fix requires unmask-and-sweep" — sweep of what scope?). Recommendation: a one-paragraph DoD: *remediated = (H1 negative-witness reproduced the defect at the production entrypoint with fix reverted) AND (H2 ledger has zero unclassified live consumers) AND (H3 sweep covered all same-token/same-shape siblings) AND (verdict=pass with no unjustified N/A)*. Severity **MAJOR** · Gregory. Priority **High**.

### === ACTOR / GOAL (Cockburn) ===

**C-1 — Primary actor + goal under-stated.** The draft never names who runs this. Primary actor = the **troubleshoot protocol operating in pipeline-hardening mode** (automated stage), triggered by an operator running `/sc:troubleshoot` or by an automated pipeline stage that escalated a pipeline-class defect. Goal: *close a pipeline escape with issue-agnostic runtime/contract proof, not an issue-specific patch.* Recommendation: add a use-case header (primary actor, scope=protocol, level=summary, trigger=§6.1, success=verdict `pass`, failure=`blocked`/`NOT PROVEN`). Severity **MINOR** · Cockburn. Priority **Med**.

### === EXAMPLES (Adzic, Given/When/Then) ===

**EX-1 — No worked Given/When/Then per wave pass/fail.** Add executable examples, especially:

- **E2 substring case (H3 near-miss negative):** *Given* a completion-phase exemption matcher; *When* it tests `sig in heading_line` with `sig=complete` against heading `incomplete`; *Then* the gate MUST treat the match as a FAIL of the matcher (substring matched a non-target), and the anchored `\b`/`re.escape` form MUST pass. (Source: EFFICACY §6 `r3383060121`.)
- **E4 dual-evaluator case (H2 ledger):** *Given* `SemanticCheck.advisory` with two consumers (`gate_passed`, `PrdExecutor._evaluate_gate`); *When* H2 enumerates consumers; *Then* leaving `_evaluate_gate` unclassified MUST block closure; *And* proof on `gate_passed` alone MUST NOT imply PRD coverage.
- **E5 effective-input case (H4):** *Given* a generated POST-reflect command with base `<start>..HEAD`; *When* `/task` left dirty working-tree work; *Then* H4 MUST fail unless the proof shows dirty work included and foreign commits excluded.

Severity **MAJOR** · Adzic. Priority **High**.

---

## PART B — Normalized Extraction for the Release-Spec

### B.1 Functional Requirements (FR-1 .. FR-13)

**FR-1 — Pipeline-hardening applicability gate (H0).**
Desc: classify whether the diagnosed issue is a pipeline escape / pipeline-boundary change and emit `pipeline_hardening_applicable`.
AC: (a) emits a boolean `pipeline_hardening_applicable`; (b) if any of the nine §6.1 trigger classes is present, H1–H5 cannot be skipped; (c) a `false` value records a boundary scan marking all nine classes absent + a one-sentence mechanism reason.

**FR-2 — Mechanism statement (H0).**
Desc: produce a one-paragraph, feature-agnostic mechanism statement for the escape class.
AC: (a) present when applicable=true; (b) avoids product-specific wording except where load-bearing for evidence; (c) names the boundary(ies) crossed from the §6.1 enum.

**FR-3 — Runtime-entrypoint verification gate (H1).**
Desc: prove the production/operator entrypoint reaches the failing boundary via a replay/harness, with producer→transformer→consumer recorded.
AC: (a) the runtime-entrypoint card is fully populated (all fields incl. exact replay command + evidence the replay reaches the production boundary); (b) FAILS if proof stops at helper construction while the defect lives at a subprocess/gate/parser/persisted-state/review-selector boundary; (c) requires ≥1 same-boundary negative control when the contract has a forbidden interpretation.

**FR-4 — Negative-witness requirement (H1).**
Desc: the entrypoint replay must be falsifiable — reproduce the defect against real captured input with the fix reverted (negative witness) paired with fix-applied PASS (positive witness).
AC: (a) records a fix-reverted FAIL against the production entrypoint; (b) records a fix-applied PASS; (c) closure blocked if only a positive witness exists.

**FR-5 — Contract enumeration ledger (H2).**
Desc: build a producer/transformer/consumer ledger for the changed contract (field/flag/parser-rule/semantic-check/selector/severity/status/predicate).
AC: (a) every live consumer is classified (role + expected behavior + decision + evidence); (b) FAILS if any live consumer is unclassified; (c) FAILS if generic/shared proof is used for a product path without proving the product path reaches that implementation.

**FR-6 — Sibling/duplicate-evaluator sweep (H2).**
Desc: when a concept is shared across sibling pipelines or duplicate evaluators, sweep them all.
AC: (a) FAILS if sibling pipelines / duplicate evaluators are not swept; (b) records each sibling's contract as consistent / intentionally-divergent / follow-up; (c) E1 sibling file-delivery and E4 dual-evaluator cases produce ledger rows.

**FR-7 — Whole-artifact classifier boundary test (H3).**
Desc: gates/parsers over generated artifacts are tested against full artifacts containing executable positives AND sibling negatives, with severity assertions.
AC: (a) a positive case proves the intended violation still HALTs; (b) a sibling/off-path negative (same-token/same-shape) does NOT hard-fail; (c) a severity assertion proves HALT/WARN/CONTINUE on each live consumer.

**FR-8 — Near-miss negative fixtures + allow-list grammar (H3).**
Desc: behavior-controlling fields get explicit allow-list grammars with mandatory near-miss negatives.
AC: (a) fixtures include `incomplete`, `representation`, decorated/bolded verdict lines, wrong-case tokens, setext-like headings; (b) wrong-provenance / wrong-lifecycle values are rejected or non-binding; (c) a hard-fatal heuristic over generated prose without adversarial false-positive fixtures + cost rationale FAILS.

**FR-9 — Unmask-and-sweep regression wave (H4).**
Desc: apply the candidate fix in shadow, sweep adjacent same-class surfaces, and replay past the original failure point.
AC: (a) FAILS if the fix only addresses the reported repro with no adjacent-defect search; (b) records sweep dimensions, implementation + generated-artifact surfaces searched, and dispositions; (c) E3 sibling-heading negative is exercised after the E2 fix.

**FR-10 — Effective-input proof for independent review/audit gates (H5).**
Desc: when a review/reflect/audit consumes an indirect selector (diff range, glob, artifact path, resume state, model-produced filename), prove the consumed input matches the runtime-produced surface.
AC: (a) fails closed when effective input is absent, empty-despite-known-changes, non-reproducible, or includes foreign work; (b) proves dirty/staged/unstaged inclusion and foreign-commit exclusion; (c) PASS-artifact / reviewer-presence / command-presence are insufficient.

**FR-11 — Off-path-reviewer rule + waiver standard.**
Desc: require off-path review when high-risk boundaries (§7 H5 list) are crossed; permit a waiver only with material evidence.
AC: (a) `off_path_review_decision ∈ {required, performed, waived_with_rationale, not_required}`; (b) waiver is invalid if it only says tests pass / reviewer independent / command exists / issue looks local; (c) waiver must state why local evidence directly executes the risky boundary.

**FR-12 — Waiver-policy / no-re-greening invariant (anti-theatre).**
Desc: a waived or skipped mandatory runtime probe downgrades its gate to `partial` and can never be re-converted to `success` by a later task-builder / sc:reflect / adversarial stage.
AC: (a) any waived/`N/A` mandatory probe forces signoff `partial`; (b) downstream stages may only downgrade the verdict, never upgrade; (c) production-facing pipeline-health signoff FAILS when a mandatory runtime probe is absent.

**FR-13 — Output contract + REPORT.md closure section (versioned, additive).**
Desc: emit the pipeline-hardening output-contract fields (additive/optional) and a REPORT.md `Pipeline Hardening Closure` section with verdict aggregation.
AC: (a) new fields are optional/additive with a `contract_version`; existing consumers unaffected; (b) REPORT.md uses `NOT PROVEN` blockers when any required proof is absent; (c) the aggregate verdict is a documented function of per-gate PASS/FAIL/N/A + waiver status.

### B.2 Non-Functional Requirements (NFR-1 .. NFR-6)

- **NFR-1 — False-skip (false-negative) rate.** Target: 0 known-escape class skipped when a §6.1 trigger is present. Measure: backtest E1–E5 fixtures; each must force applicable=true.
- **NFR-2 — Applicability false-positive (over-trigger) rate.** Target: <30% of pure-local fixes wrongly enter hardening mode. Measure: labeled corpus of local-only fixes vs pipeline escapes.
- **NFR-3 — Added cost of hardening mode.** Target: bounded token/latency overhead vs baseline Tier-1 troubleshoot (prefer single-seam probe + one entrypoint smoke; no mandatory full E2E suite). Measure: token/wall-clock delta on representative runs.
- **NFR-4 — No-re-greening durability.** Target: 100% — a `partial` signoff is never observed as `success` downstream. Measure: integration test driving a waived probe through sc:reflect/adversarial/sprint consumers.
- **NFR-5 — Command thinness.** Target: command file contains advertise+handoff only; zero closure/ledger logic. Measure: section/line budget check + verify-sync.
- **NFR-6 — Contract backward-compat.** Target: 100% of existing troubleshoot-result consumers parse unchanged with new optional fields present. Measure: consumer-enumeration test with old + new payloads.

### B.3 Risks (§7)

| Risk | Prob | Impact | Mitigation |
|---|---|---|---|
| Hardening-mode theatre via waiver abuse (waived probe re-greened downstream) | Med | High | FR-12 monotonic verdict + NFR-4 integration test + mechanical no-re-greening enforcement (Open Item OI-1) |
| Over-triggering on pure-local fixes (cost/friction, operator opt-out) | High | Med | NFR-2 false-positive ceiling; FR-1 boundary-scan skip path |
| Maintenance cost / drift of 5 new refs + ledger schema | Med | Med | FR/A-1 thin-command segregation; single shared seam-record kernel (A-2) |
| Unversioned contract breaks existing result consumers | Low | High | FR-13 additive/optional + `contract_version`; NFR-6 |
| Predicted coverage never validated (efficacy stays unproven) | Med | High | FR-4 negative-witness + backtest E1–E5 in E2E (§8.3) |
| `N/A`-without-rationale used to bypass gates | Med | High | FR-13(b) `NOT PROVEN` blocker; verdict aggregation treats unjustified N/A as blocked |
| Heuristic hard-gate false-positive over generated prose (new E3-class) | Med | Med | FR-8 near-miss fixtures + cost rationale requirement |

### B.4 Key Design Decisions (§2.1)

| Decision | Choice | Alternatives | Rationale |
|---|---|---|---|
| Encode remediation as | Waves-as-gates (blocking) | Advisory checklist | Efficacy §4: audit artifacts without blocking force did not change failure probability |
| Waived/absent probe status | `partial`, non-upgradable | re-green to success | Single control preventing back-door theatre (EFFICACY §10) |
| Command vs skill split | Thin command, fat skill+refs | Logic in command | Fowler interface segregation; keeps SKILL.md navigable |
| Evidence model | Negative-witness + positive-witness | positive-only / static read | §8 irreducibility: 3 escape classes un-catchable by reading alone |
| Contract field rollout | Additive/optional, versioned | replace result shape | Newman contract evolution; protect existing consumers |
| Probe breadth | One focused live-seam probe + entrypoint smoke | full E2E suite per seam | Pact fragility warning; cost control (EFFICACY §10) |

### B.5 Test Plan Seeds (§8)

| Tier | Test | Maps to |
|---|---|---|
| Unit | substring vs `\b`/`re.escape` matcher rejects `incomplete`/`representation` | FR-8 / E2 |
| Unit | verdict-aggregation truth table (PASS/FAIL/N/A/waived → verdict) | FR-13 / R-4 |
| Unit | applicability classifier on labeled local vs pipeline corpus | NFR-2 |
| Integration | H2 ledger blocks closure when a live consumer unclassified (dual-evaluator fixture) | FR-5/FR-6 / E4 |
| Integration | waived probe → `partial`, not upgraded by sc:reflect/adversarial | FR-12 / NFR-4 |
| Integration | additive fields parsed by existing result consumers | FR-13 / NFR-6 |
| E2E (§8.3) | E1 headless `--spec` replay rejects local-path `--file` (negative witness) | FR-3/FR-4 / E1 |
| E2E (§8.3) | E3 full-MDTM-corpus sweep flags sibling Findings heading after E2 fix | FR-9 / E3 |
| E2E (§8.3) | E5 POST-reflect rejected unless dirty `/task` work proven included, foreign excluded | FR-10 / E5 |
| E2E (§8.3) | M6 resume step-ID round-trip through `prd resume` at operator boundary | FR-5 (contract identity) |

### B.6 Open Items (§11)

| Item | Question | Impact |
|---|---|---|
| OI-1 | Mechanical enforcement that keeps a waived probe from being re-greened downstream (research open Q) | High — core anti-theatre control unmechanized at G1 |
| OI-2 | Which PRD/protocol tokens become first-class Contract Identity Ledger entries | Med — scopes H2 cost |
| OI-3 | Cheapest reliable public-entrypoint probe per high-risk seam | Med — drives NFR-3 |
| OI-4 | Real CommonMark-derived parser vs smaller PRD-specific grammar for H3 | Med |
| OI-5 | Actor behind `r3383060121` UNPROVEN — does DoD assume human or tool review? | Low |
| OI-6 | Verdict enum reconciliation across §6.2 / §8 / waiver `partial` | Med |

### B.7 Downstream (§10)

**For sc:roadmap** — themes: (T1) Applicability & trigger (FR-1,2); (T2) Runtime-entrypoint + negative-witness (FR-3,4); (T3) Contract enumeration + sibling sweep (FR-5,6); (T4) Classifier/parser hardening (FR-7,8); (T5) Unmask-and-sweep (FR-9); (T6) Effective-input + off-path review (FR-10,11); (T7) Anti-theatre verdict/signoff + integration (FR-12,13). Milestone gates: M1 spec+contract frozen → M2 refs+schema → M3 skill trigger+verdict wiring → M4 backtest E1–E5 (turns §5 from predicted→proven) → M5 sync-dev/verify-sync + sign-off.

**For sc:tasklist** — atomic-FR granularity; build refs first (templates are leaf deps), then SKILL.md trigger+aggregation, then command-file advertise. Each E1–E5 fixture is its own task (E2E backtest). Gate every task on `make verify-sync`. Keep T7 (no-re-greening) blocked-by OI-1 until enforcement mechanism chosen.

---

*Cluster: requirements + architecture + integration + ops. Sibling clusters (correctness/security/testing) cover orthogonal buckets.*

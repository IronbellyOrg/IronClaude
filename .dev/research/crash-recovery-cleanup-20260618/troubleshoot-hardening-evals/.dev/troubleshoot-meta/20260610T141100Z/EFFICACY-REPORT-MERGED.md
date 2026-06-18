<!-- Provenance: produced by /sc:adversarial; Base: Variant C; Merge date: 2026-06-10 -->

# Troubleshoot Meta-Investigation — Merged Efficacy Report (Pre-G1)

Output root: `/config/workspace/IronClaude/.dev/troubleshoot-meta/20260610T141100Z`

Base commit: `94d5baa05f6319b8ff6f2e1db8e8b7737465daaf`

Status: **G1-ready, implementation pending approval.** The meta-pipeline hardening is **unbuilt and halted at G1**; the individual product escapes were already point-fixed in shipped PRs (E4's fix committed but unmerged).

<!-- Source: Variant C spine (status/posture header); refactor-plan change 1 -->

---

## 1. Executive verdict

<!-- Source: Variant C §exec + Variant A/B §1 corrected per refactor-plan change 2, BC-3, BC-4 -->

The Phase 0/G0 evidence is sufficient to freeze the canonical escape set **E1–E5** and request G1 approval for a troubleshoot-protocol hardening implementation. **No hardening has been built**: the H0–H5 waves described in §8–§10 are a spec awaiting approval, not a delivered system.

The blunt finding for the **registry-miss class** is that the assurance stack was **largely theatre**. Stages produced real artifacts, signoffs, and green-looking reviews, but for the canonical escapes they too often proved adjacent artifacts — command strings, helper functions, local snippets, PASS artifacts, generic evaluator paths — rather than the runtime or contract boundary that actually failed. **Every M-series miss surfaced at runtime** (a real crash, halt, or resume failure), never by the design-stage review surface.

Two — and only two — distinct catches landed before runtime, and **neither came from the design-stage adversarial debate**:

1. the **#154 review pass `r3383060121`** caught the F-A/E2 substring regression, and
2. **`sc:reflect`** caught the E5/REFLECT-E01 wrong-diff trap.

This is not "the process was empty." It caught important issues and created durable audit trails. The failure pattern is narrower and structural: gates aimed at *representations* of a change instead of the *executed bytes / live call-graph / all contract consumers* where the escapes lived. The overall theatre-vs-value estimate is a **value/ceremony mean of 41% value / 59% mis-targeted ceremony** (see §5 — this is a per-stage mean, **not** an escape-catch rate).

---

## 2. Canonical crosswalk (E1–E5)

<!-- Source: round3-resolution via refactor-plan change 3; BC-2. Use verbatim. -->

| Canonical | Definition | A's M-instances | defect-table row | source-of-record | fix status |
|---|---|---|---|---|---|
| E1 | `--file` cloud-file misuse | M1 | PRD-E04 | defect-escape-table | MERGED #151 `7601ad25` |
| E2 | completion-phase false-positive | M2 (+F-A; B's M7) | PRD-E05 | defect-escape-table | MERGED #154 `e97aa4fd` |
| E3 | Task-Log heading false-positive | M3 | PRD-E06 | defect-escape-table | MERGED #155 `eb9a2633` |
| E4 | evaluator divergence (`_evaluate_gate` vs `gate_passed`) | M4 (+M6 resume-ID, same class) | **none** | `contract-implementations.md` | **UNMERGED** `b97c9960` (branch `origin/fix/prd-executor-advisory-gate`) |
| E5 | POST-reflect wrong-diff | — | REFLECT-E01 | defect-escape-table | MERGED #153 `10723863` |

**Crosswalk caveats (BC-2):**

- Canonical **E4 ≠ table PRD-E04**. The table row **PRD-E04** is the `--file` bug, which is canonical **E1**. Canonical E4 (evaluator divergence) has **no** row in the 9-row defect table; it lives only in `contract-implementations.md`.
- The 9-row defect-escape table is the **appendix** of four pre-episode families: PRD-E01 / PRD-E02 / PRD-E03 + REFLECT-E02 / REFLECT-E03 (out of the E1–E5 window).
- **F-B** (the `#154` bundled `sc-auggie-review` doc rider) is a **bisection-hygiene** finding, **excluded** from the canonical set.

---

## 3. Committed / unbuilt ledger (3 buckets)

<!-- Source: round3-resolution via refactor-plan change 4; BC-3. Never "nothing was fixed" NOR "refactor validated". -->

The honest one-sentence claim: **"The meta-pipeline hardening is unbuilt and halted at G1; the individual product escapes were already point-fixed in shipped PRs (E4's fix committed but unmerged)."**

### Bucket 1 — UNBUILT (spec-only, halted at G1)

The troubleshoot-protocol hardening: the H0–H5 wave mechanisms, pipeline-health mode, and contract-ledger automation described in §8–§10. **Verified empty:** `git diff 94d5baa0..master` on `sc-troubleshoot-protocol/SKILL.md` and `commands/troubleshoot.md` returns no changes. Nothing in this report's hardening design has been implemented.

### Bucket 2 — COMMITTED + MERGED to master

Point-fixes that closed the individual product escapes:

- **#149** — earlier PRD-pipeline point-fix (precedes the E1–E3 chain).
- **#151** `7601ad25` — closes **E1** (`--file` cloud-file misuse).
- **#153** `10723863` — closes **E5** (POST-reflect wrong-diff).
- **#154** `e97aa4fd` — closes **E2** (completion-phase false-positive).
- **#155** `eb9a2633` — closes **E3** (Task-Log heading false-positive).

### Bucket 3 — COMMITTED but UNMERGED

- **E4** fix `b97c9960` on branch `origin/fix/prd-executor-advisory-gate` — honors advisory checks in `PrdExecutor._evaluate_gate` (the live PRD path). **Not on master.**

---

## 4. Per-stage theatre scorecard

<!-- Source: Variant B scorecard structure + theatre-vs-value-scorecard.md authoritative numbers; relabeled per BC-1 and BC-4. -->

The scorecard below uses the **authoritative per-stage value/ceremony numbers** from `theatre-vs-value-scorecard.md`. The blended figure (**41% value / 59% ceremony**) is a **per-stage value/ceremony MEAN**, **not** an escape-catch rate. All run-result tokens grafted from the blind variants' scorecards have been removed; the catch-attribution column carries the literal status `NOT YET PROVEN (pre-build)` because the hardening that would alter these ratios is unbuilt.

| Stage | Value | Ceremony | Main contribution | Main miss pattern | Hardening effect on this ratio |
|---|---:|---:|---|---|---|
| `sc:troubleshoot` | 52% | 48% | Best direct contract mapping; exposed the evaluator divergence behind E4. | Did not prevent E1, E2/E3, or E5 before follow-up; review stopped at local symptom analysis. | NOT YET PROVEN (pre-build) |
| `task-builder` | 35% | 65% | Durable routing, auditability, PRE/POST reflect wiring; downstream dogfood value. | Generated tasks lacked mandatory runtime-contract cards, parser sweeps, consumer enumeration. | NOT YET PROVEN (pre-build) |
| `sc:reflect` | 40% | 60% | Caught E5/REFLECT-E01 wrong-diff trap; surfaced emitted-output/PRD-durability follow-ups. | Rubber-stamped after the fact on E1; did not force E2 unmask-and-sweep; missed E4's PRD evaluator path. | NOT YET PROVEN (pre-build) |
| QA gates | 35% | 65% | Caught fabricated/stale current-state claims; probed integration-chain gaps. | Missed runtime/off-path canonical failures (headless `--spec`, parser false positives, evaluator divergence, reflect base semantics). | NOT YET PROVEN (pre-build) |

**Stage blend → mean:** (52/48, 35/65, 40/60, 35/65) averages to **≈ 41% value / 59% ceremony**. This is the value/ceremony mean of the four Phase-1 cards; it does **not** describe how many escapes were caught.

### What was real value (grounded)

1. **Contract-focused troubleshooting worked when it reached actual consumers.** `sc:troubleshoot` scored highest (52%) because it tied symptoms to concrete PRD/spec-fidelity contracts and identified the evaluator split behind E4.
2. **Downstream dogfooding created signal.** The `task-builder` path exercised generated artifacts through scanner/sprint-like surfaces rather than reviewing them only as documents.
3. **`sc:reflect` had a distinct high-value niche.** It caught the wrong-diff/base-selection trap in E5 — a class ordinary source review easily misses.
4. **QA gates helped evidence hygiene.** Useful for catching fabricated or stale current-state claims and probing integration-chain assumptions.

### What was theatre or mis-targeted ceremony (grounded)

1. **Exact runtime entrypoints were not mandatory.** E1 escaped because review did not require headless PRD `--spec` / `claude --file` replay before granting confidence.
2. **Parser fixes were not followed by an unmask-and-sweep.** E2 and E3 show local parser remediation did not force a full generated-MDTM corpus sweep for adjacent false positives.
3. **Contract consumers were not enumerated.** E4 persisted because generic advisory semantics and the PRD-specific evaluator diverged; reviews verified one path and implied coverage of the other.
4. **Diff/base semantics were treated as review plumbing, not a primary invariant.** E5 shows POST-reflect could audit the wrong surface unless base selection and uncommitted-work visibility were explicitly checked.
5. **Many gates produced audit artifacts without changing failure probability.** Durable reports, checklists, and stage labels improved traceability but often added no observation capable of catching the canonical defect.

### Highest-leverage stage to fix first

**`task-builder`** — it is upstream of the other assurance stages and shapes the required evidence (work items, PRE/POST reflect prompts, QA expectations, remediation checklists) that every later gate inspects. If `task-builder` outputs require the right runtime and contract evidence, downstream stages get a better surface; if it omits that evidence, downstream `sc:reflect`, QA, and troubleshooting review the same incomplete packet and rubber-stamp the same blind spots. For the requested G1 scope specifically, the harden target is `/sc:troubleshoot` and `sc:troubleshoot-protocol` (§10).

---

## 5. Would-have-caught matrix (PREDICTED — NOT YET PROVEN)

<!-- Source: Variant A/B would-have-caught matrices; relabeled per BC-1. This is PREDICTED coverage of E1–E5 by the (UNBUILT) H-waves. No events asserted. -->

This matrix is **predicted** coverage of the canonical escapes by the **unbuilt** H-waves. Because no hardening exists, **no run, replay, or catch event is asserted** — every cell carries `NOT YET PROVEN (pre-build)`. The mechanism column states *which H-wave is designed to* surface each escape, in the hypothetical post-build pipeline.

| Escape | Predicted catching H-wave(s) | Designed mechanism (predicted) | Status |
|---|---|---|---|
| E1 (`--file` misuse) | H1, H2 | H1 runtime-entrypoint replay of headless `prd run --spec` would exercise the real `claude --file` boundary; H2 contract enumeration would diff PRD against sibling pipelines that forbid the flag. | NOT YET PROVEN (pre-build) |
| E2 (completion-phase FP) | H3, H1 | H3 whole-artifact classifier boundary test would include a real final completion phase as a negative; H1 continuation would exercise build-task-file. | NOT YET PROVEN (pre-build) |
| E3 (Task-Log heading FP) | H3, H4 | H4 unmask-and-sweep after the E2 fix would re-scan the full generated MDTM corpus for sibling `### Phase N … Findings` placeholder headings. | NOT YET PROVEN (pre-build) |
| E4 (evaluator divergence) | H2, H1 | H2 contract-consumer ledger would enumerate `gate_passed` vs `PrdExecutor._evaluate_gate`; H1 entrypoint re-derivation would prove the live PRD path reaches `_evaluate_gate`. | NOT YET PROVEN (pre-build) |
| E5 (POST-reflect wrong-diff) | H5 | H5 effective-input proof would assert the reflect diff base matches `/task`'s dirty working-tree output and excludes foreign commits. | NOT YET PROVEN (pre-build) |

**Predicted coverage:** all five canonical escapes map to at least one designed H-wave. This is a **design-time prediction only**; the irreducibility analysis in §8 explains why several of these escapes are catchable *only* by an execute/simulate wave, not by static reading — which is precisely why the H-waves are exercise-mechanisms and why their efficacy remains unproven until built and replayed.

---

## 6. Lone-catch attribution + caveat

<!-- Source: Variant C + A/B synthesis per refactor-plan change 7; X-001. -->

Two distinct pre-runtime catches occurred across the episode; **neither was produced by the design-stage adversarial debate**:

1. **F-A / E2 substring regression** — caught by the **#154 review pass `r3383060121`**. The `#154` completion-phase exemption initially used a bare `sig in heading_line` substring test, so `complete` matched `incomplete` and `present` matched `representation`, silently exempting real work phases. The review-pass id `r3383060121` appears in the body of commit `e97aa4fd`; the fix anchored matching with `\b` / `re.escape`.
2. **E5 / REFLECT-E01 wrong-diff trap** — caught by **`sc:reflect`**, which surfaced that POST-reflect audited `<start_commit>..HEAD`, omitting dirty `/task` work and possibly including foreign commits.

**Caveat (UNPROVEN actor).** The human-vs-tool actor behind `r3383060121` is **UNPROVEN**. The id appears in the commit body, but the available evidence does not establish whether the catch was made by a human reviewer or an automated review tool. State this as an explicit caveat; do not attribute it to either actor as fact.

Every other miss (the M-series) was discovered by **runtime** — a crash, a halt, or a resume failure — after each upstream fix advanced the runtime frontier to the next previously-shadowed gate.

---

## 7. Merged root causes

<!-- Source: Variant C root causes RC1–RC5, retained as the spine. -->

### RC1 — Runtime-boundary proof was substituted with construction proof

E1 and E5 show the strongest form. In E1, PRD preserved paths and built argv, but no check proved the real headless Claude subprocess accepted those paths through `--file`. In E5, a generated reflect command existed, but no check proved the selected diff matched `/task`'s dirty working-tree output. Closure accepted syntactic command presence or helper-level behavior instead of the actual runtime input consumed by the operator entrypoint.

### RC2 — Generated-artifact parsers lacked topology-aware boundaries

E2 and E3 treated locally matched `Phase N` headings as executable work without respecting generated-artifact roles. Completion bookends and Task-Log placeholders looked similar enough to trigger strict enforcement. Validators over generated prose were tested against snippets and expected headings, not full artifacts containing positive executable sections and sibling negative sections.

### RC3 — First fixes did not generalize to same-class sibling surfaces

E3 followed E2 because the fix addressed the visible final-phase symptom but did not sweep all generated phase-like headings. E4 has the same shape at the contract level: a semantic change validated on one evaluator while other consumers stayed unswept. Closure focused on the observed repro instead of the mechanism family.

### RC4 — Shared contracts had multiple live consumers but no consumer ledger

E4 is canonical: `SemanticCheck.advisory` was a multi-consumer contract — generic gates, PRD runtime gates, trailing gates, remediation dispatch, fixtures, reports. Verification validated the edited generic helper and incorrectly inferred PRD coverage. Shared field/predicate/status changes lacked mandatory producer/transformer/consumer enumeration and parity (or intentional-divergence) proof.

### RC5 — Independent review was treated as present/absent instead of input-correct/incorrect

E5 shows off-path review can exist and still be false assurance if it reviews an empty, stale, or foreign surface. A PASS artifact or reflect invocation is not enough; review gates lacked effective-input proof tying expected runtime-produced changes to the files/commits/artifacts actually consumed.

---

## 8. Analytical primitives (design rationale for the unbuilt H-waves)

<!-- Source: Variant A U-001 patch-relative, U-002 negative-witness, §7 irreducibility. Framed as rationale, not as run results. -->

These primitives are imported from Variant A as the **rationale** for why the (unbuilt) H-waves are shaped as exercise mechanisms rather than additional reading passes. They are analytical lenses, not claimed run outcomes.

### Patch-relative vs baseline-relative defects

A class of escape is invisible to any forward pass over **un-patched** code because the defect exists **only after the candidate fix is applied**. E3 is the exemplar: narrowing the E2 matcher *creates* a new false-positive on sibling Task-Log headings. A static read of the baseline cannot see a fault the fix itself introduces. The design implication is H4 (unmask-and-sweep) must apply the candidate patch in shadow and re-sweep the full sibling corpus — a property no baseline-relative gate can hold.

### Negative-witness admission

A test never observed to fail proves nothing (TDD red-green; positive-and-negative assay controls; chaos/fault-injection). A certification stage should refuse green unless it records a **negative witness** — the oracle run against real captured input through the production entrypoint with the fix reverted, showing FAIL — paired with a positive witness (fix applied, PASS). The design implication is H1's entrypoint replay must be falsifiable: capable of reproducing the defect against reality before being accepted with the fix present.

### Irreducibility — what static troubleshooting alone cannot catch

The episode's own data is the argument: every M-series miss was runtime-discovered; the design-stage review surface caught none of them. Three escape sub-classes are **irreducibly un-catchable by reading alone**:

1. **Map-vs-territory divergence (E4).** When a fix and its tests bind to a symbol that *looks* live but isn't on the executed path, both sides are internally consistent; only re-deriving the path from the real entrypoint and running the oracle against reality falsifies it.
2. **Shadowed downstream faults (E2-class).** A defect in gate N is invisible until gates 1..N-1 are green; only driving the chain in continue-on-failure mode against realistic captured input exercises it.
3. **Unmasking / second-order false-positives (E3).** A property that exists only after the candidate fix is applied cannot be present in the artifact a static pass reads; it requires applying the patch in shadow and re-running.

This is why the H-waves are designed as execute/simulate mechanisms. It is also why the §5 matrix is **predicted, not proven**: the value would come entirely from stages that exercise the real (and patched) call-graph — and those stages do not yet exist.

---

## 9. Contract Identity Ledger

<!-- Source: Variant B Contract Identity Ledger; E4 + M6 kept as separate rows per refactor-plan change 9 and the M6 inlined facts. -->

Behavior-controlling tokens must be justified by **executable contract identity** (owner / producer / consumer / accepted grammar), not by plausible human-readable taxonomy. E4 and M6 are the two live contract-identity defects; they are **distinct rows** — different mechanisms, different blame commits, different merge status.

| Token / contract | Producer (emitter) | Consumer (acceptor) | Divergence | True blame | Status |
|---|---|---|---|---|---|
| `SemanticCheck.advisory` (E4) | generic `pipeline.gates.gate_passed` honored advisory | PRD runtime `PrdExecutor._evaluate_gate` did **not** honor advisory; halted on first non-True check | Dual evaluators; fix + verification both targeted the unused `gate_passed` path | `b97c9960` (the fix) | **COMMITTED but UNMERGED** (`origin/fix/prd-executor-advisory-gate`) |
| resume step-ID (M6) | `src/superclaude/cli/prd/executor.py:259` emits `"research-qa"` | `src/superclaude/cli/prd/config.py:30` expects `qa-research-gate` (absent from `_STEP_ID_PATTERN`) | Producer and consumer use different vocabularies in different modules; `prd resume --resume-from research-qa` raises | introducing commits `27962ddb2` + `09e2ccc0d` (**NOT** #149) | **LIVE on master** (no committed fix) |

**M6 is a distinct ledger row from E4**: although both are contract-identity mismatches, M6 is a resume-ID vocabulary drift still live on master with no fix, whereas E4 is the evaluator-divergence escape with a committed-but-unmerged fix. Do not collapse them.

---

## 10. Hardening-spec linkage + halt-pending-approval posture

<!-- Source: Variant C refactor-spec + halt note; refactor-plan change 10. -->

The G1 implementation would harden `/sc:troubleshoot` and `sc:troubleshoot-protocol` with a new **Pipeline Hardening Closure** mode, gated by the H0–H5 waves:

- **H0 — Applicability & mechanism statement.** Decide whether pipeline hardening applies; write a mechanism statement independent of any single product symptom.
- **H1 — Runtime-entrypoint verification gate.** Replay the production entrypoint; record producer/transformers/consumer, boundary crossed, asserted outcome, same-boundary negative control. Fail if proof stops at helper construction. (Predicted coverage: E1, E4, E5.)
- **H2 — Contract-enumeration wave.** Build a consumer ledger for the changed field/flag/parser-rule/semantic-check/selector/status; fail if any live consumer is unclassified. (Predicted coverage: E4; secondary E2, E3.)
- **H3 — Whole-artifact classifier boundary tests.** Test gates/parsers against full generated artifacts with executable positives and sibling negatives. (Predicted coverage: E2, E3.)
- **H4 — Unmask-and-sweep regression wave.** Apply the candidate fix, sweep adjacent surfaces, replay past the original failure point. (Predicted coverage: E3, E4; secondary E1, E2.)
- **H5 — Effective-input proof for independent review/audit gates.** Prove expected vs consumed files/commits/ranges, dirty-work inclusion, foreign exclusions. (Predicted coverage: E5; secondary E1, E4.)

**Research-informed gate-design refinements (external best practices, 2026-06-10).**
<!-- Source: researchFindings.md deep-research pass; corroborates design DIRECTION only — does not prove efficacy (§5 stays NOT YET PROVEN). See Appendix A. -->
A 23-source deep-research pass (Pact/CDC, NCSC/OWASP, CommonMark, .NET regex, AWS Step Functions, Argo Workflows; 24/25 claims survived 3-0 adversarial verification) corroborates the *design direction* of these waves — it does **not** prove their efficacy, which remains `NOT YET PROVEN (pre-build)`. It sharpens the spec with four concrete controls:

- **Waiver policy (anti-theatre invariant).** A waived or skipped runtime probe MUST downgrade its gate to status `partial` — it may **never** be re-converted to `success` by a later `task-builder`, `sc:reflect`, or `adversarial` stage. Production-facing pipeline-health signoff fails when a mandatory runtime probe is absent. This is the single control that prevents theatre from returning through the back door.
- **H1/H2 contract record (Pact/CDC seam shape).** Each runtime/contract probe declares: public entrypoint · producer · emitted runtime value · consumer · expected action · observable acceptance signal · failure signal. Prefer one focused live-seam probe per implicated seam plus one public-entrypoint smoke when several seams are involved — not an expensive full end-to-end suite (Pact warns over-broad multi-layer contract tests become fragile).
- **H3 allow-list grammars + near-miss negatives (NCSC/OWASP + .NET regex).** Behavior-controlling fields (verdicts, phase markers, resume step IDs, gate statuses, CLI flags) get explicit allow-list grammars, with fixtures proving wrong-provenance, wrong-lifecycle, and reasonable-looking-invalid values are rejected or non-binding. Mandatory near-miss negatives: `incomplete`, `representation`, decorated/bolded verdict lines, wrong-case tokens, setext-like headings. Regex timeouts are a guardrail, not a substitute for semantic fixtures (and not a security boundary).
- **H5 / Contract-ledger recovery semantics (Step Functions + Argo).** Treat retry / resume / rerun / resubmit as distinct contracts; feed emitted execution-log step IDs straight into `prd resume` (directly exercises the M6/E4 identity gap) and assert terminal-state, wildcard, and wrong-case handling at the operator boundary.

**Likely post-G1 edit scope (source-of-truth only):**

- `/config/workspace/IronClaude/src/superclaude/commands/troubleshoot.md`
- `/config/workspace/IronClaude/src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md`
- `/config/workspace/IronClaude/src/superclaude/skills/sc-troubleshoot-protocol/refs/report-template.md`
- `/config/workspace/IronClaude/src/superclaude/skills/sc-troubleshoot-protocol/refs/remediation-handoff.md`
- New refs: `pipeline-hardening-closure.md`, `runtime-entrypoint-verification.md`, `contract-enumeration.md`, `unmask-and-sweep.md`, `effective-input-proof.md`

**Halt note.** Implementation and backtest are **pending G1 approval** because the next step edits shared source-of-truth skill/command files. No implementation edits should occur before approval. Do not edit generated `.claude/` mirrors directly; after approved source edits, run `make sync-dev` and `make verify-sync`, and do not stage generated `.claude/` mirrors.

**Paste-ready approval prompt:**

```text
Approved G1. Implement /config/workspace/IronClaude/.dev/troubleshoot-meta/20260610T141100Z/troubleshoot-pipeline-hardening-spec.md in source-of-truth files only. Do not edit .claude mirrors directly. After edits, run make sync-dev and make verify-sync, then report changed files and any tests run. Do not commit.
```

---

## 11. Caveats

<!-- Source: synthesis of BC-2/BC-3 boundary constraints + inlined facts. -->

1. **Unproven actor.** The human-vs-tool actor behind review-pass `r3383060121` (the F-A/E2 catch) is **UNPROVEN**. The id appears in the `e97aa4fd` commit body, but the evidence does not establish whether a human or a tool produced the catch.
2. **E4 unmerged.** The E4 evaluator-divergence fix `b97c9960` is **committed but not on master** (branch `origin/fix/prd-executor-advisory-gate`). The escape is closed in code but not shipped.
3. **M6 live.** The resume step-ID mismatch (`executor.py:259` `"research-qa"` vs `config.py:30` `qa-research-gate`) is **live on master** with no committed fix; true blame is `27962ddb2` + `09e2ccc0d`, not #149.
4. **Hardening unbuilt.** All H0–H5 mechanisms, the §5 would-have-caught matrix, and any efficacy of the hardening are **predicted / pre-build**. `git diff 94d5baa0..master` on the protocol files is empty. No rollback-replay or coverage claim is asserted.
5. **Metric framing.** `41% value / 59% ceremony` is a per-stage value/ceremony mean from `theatre-vs-value-scorecard.md`, **not** an escape-catch rate.
6. **External corroboration is analogical, not literal.** The 2026-06-10 research pass validated the *direction* of the hardening (consumer-driven contract testing, allow-list validation, conformance fixtures, executable terminal-state handling, explicit recovery semantics), but its sources are workflow/parser analogues: NCSC does not use the term "semantic oracle", CommonMark conformance tests validate Markdown rendering rather than arbitrary PRD classifiers, and Step Functions/Argo are orchestration analogues (Argo behavior is version-sensitive). Corroboration of design ≠ proof of efficacy — §5 remains `NOT YET PROVEN`.
7. **Research provenance.** The deep-research pass was run against a sibling copy of the efficacy report (`/config/workspace/IronClaude/.dev/troubleshoot/meta-efficacy-pipeline/EFFICACY-REPORT.md`), not this merged output; 24 of 25 verified claims survived 3-0, and 1 was refuted (a too-strong "the .NET regex engine cannot defend against hostile patterns at all"). See Appendix A.

---

## Appendix A — External best-practice corroboration (research-informed, 2026-06-10)

<!-- Source: /config/workspace/IronClaude/.dev/troubleshoot-meta/20260610T141100Z/researchFindings.md (deep-research pass: 5 angles, 23 sources, 108 claims, 25 verified, 24 confirmed 3-0, 1 refuted). Corroborates DESIGN DIRECTION only; does not alter the NOT-YET-PROVEN status of §5 or the unbuilt status of §3 Bucket 1. -->

A deep-research pass independently corroborates the diagnosis (RC1–RC5) and the hardening direction (H0–H5 / Contract Identity Ledger). It is **design corroboration, not efficacy proof** — every H-wave remains `NOT YET PROVEN (pre-build)` and the hardening remains unbuilt (§3, Bucket 1).

| Report element | External practice (corroborating) | Primary sources |
|---|---|---|
| H1/H2 runtime-boundary & contract-enumeration; RC1, RC4 | Consumer-driven contract testing: prove the producer value is accepted/acted-on at the seam, not that a plausible helper exists | Pact (`docs.pact.io/consumer`), Microsoft CDC playbook |
| H3 classifier boundary tests; RC2 | API input validation: allow-list grammars, schema-backed contracts, reject unexpected keys; syntactic ≠ semantic validation | NCSC HTTP-API input-validation, OWASP Input-Validation, JSON Schema |
| H3 Markdown classifier fixtures; E2/E3, RC2 | Conformance-fixture model: 500+ embedded examples; block markers precede inline; setext cannot interrupt paragraphs | CommonMark spec + `commonmark/commonmark-spec` |
| H3 near-miss negatives; E2 substring bug | Near-valid negatives explode runtime/semantics; timeouts are a guardrail, **not** a security boundary | .NET regex best-practices, OWASP ReDoS |
| H2 / Contract Identity Ledger (E4); RC4 | Executable contract identity: case-sensitive status strings, reserved prefixes, wildcard boundaries, top-level vs local failure scope | AWS Step Functions error-handling, States-language spec |
| H5 / M6 operator recovery; E4, M6 | Retry/resume/rerun/resubmit are distinct contracts; round-trip emitted step IDs through the public CLI | Argo `argo retry` / `argo resubmit` / memoization |
| Anti-theatre gate status (new, §10) | Waived live probes must be non-success; allow waivers to downgrade to `partial`, never green | Synthesis across all 24 confirmed claims |

**Refuted (1 of 25).** "The .NET regex engine does not defend against hostile/inefficient patterns; trust must be handled entirely outside the engine" (0-3). The surviving weaker claim is retained instead: timeouts reduce backtracking but are not a security boundary and do not replace semantic fixtures.

**Open questions carried forward (from the research):** which PRD tokens become first-class ledger entries; the cheapest reliable public-entrypoint probe per high-risk seam; a real CommonMark-derived parser vs a smaller PRD-specific grammar; and the mechanical enforcement that keeps a waived probe from being re-greened by a downstream stage.

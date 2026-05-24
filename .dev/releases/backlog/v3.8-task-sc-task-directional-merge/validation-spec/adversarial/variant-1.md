---
spec_type: validation
target_release: task-sc-task-directional-merge
stance: steelman
focus: [tradeoffs, invariants, failure-modes, evidence]
source_artifact: .dev/releases/current/task-sc-task-directional-merge/artifacts/final-merge-plan.md
source_lines: 1-477
invariant_anchor: extension-point-contracts.md:11-17
---

# Steelman Validation Spec — Final Merge Plan (variant-1)

## 1. Executive defense

The plan is sound as binding because it makes three structurally correct choices: (a) it pins INV-01..INV-05 to a single anchor source (`extension-point-contracts.md:11-17`, see line 21 and § 4.6 / F-06) and proves survival via a worked example rather than asserting it (§ 3, lines 79–88, and `invariant-survival-walkthrough.md`); (b) it converts every "PASS WITH NOTE" verdict into a concrete acceptance-criterion delta on exactly four rows (CR-TASK-06, CR-TASK-09, CR-FM-04, CR-TASK-12 — line 28, line 204), with no row added, removed, or re-scored; and (c) it hardens three implicit ordering assumptions into binding sequencing constraints S-1..S-3 (§ 6, lines 319–341) backed by named hazard sources (HZ-03, HZ-06+HZ-07, HZ-14). The plan's authority chain (line 13) is explicit, the verdict roll-up is fully accounted (lines 34–44), and every finding closure cites a re-readable disposition. The "zero open findings" claim is auditable rather than rhetorical because § 9 (lines 445–457) names the exact grep / re-read procedure an independent agent uses to falsify it.

## 2. Per-TU steelman (TU-1..TU-8)

### TU-1 (`Tier:` field + Gate 1 + per-item marker) — ADOPT

**Invariants protected:** INV-05 (refusal-of-definition), INV-01 (F1 loop semantics), INV-04 (resumability).

**Why ADOPT is correct (line 56).** `Tier:` is *metadata*, not work-definition; it conditions which pre-existing dispatch profile fires at Gate 1 (line 87). The per-item `(Tier: ...)` marker is bound by ME-1 to "tier-conditioned read" semantics (§ 4.1, lines 99–105) — it can never re-fire Gate 1, never select a different `rf-qa` roster, never substitute EXECUTE. CR-FM-03's compat-shim posture (default `STANDARD`, no migration — line 87, line 214) is what makes INV-04 hold for existing TASK-* files on disk.

**Alternative that would weaken INV:** ADAPT with an embedded runtime classifier (D09b-style) would re-introduce per-item dispatch. That is exactly the pattern REJECTed in the ledger and re-cited at line 87 ("D09b / D08 / D01 / D13 / D06 all REJECTed") and at line 206. ADOPT preserves INV-05 because it refuses to let any new code path *define* what kind of work an item is at runtime.

### TU-2 (Critical/Trivial Path Override) — ADOPT

**Invariants protected:** INV-05, INV-01.

**Why ADOPT is correct.** The `path-override: forced_stance=…` Task Log emission is first-at-entry (line 215) and the F-02 sentinel comment plus the row-1 ordering grep (§ 4.2, lines 109–121) make the ordering structurally enforceable, not merely conventional. CR-7 ordering (`path_override_check → tier_field_validate → gate_1_dispatch`) is the single point where override semantics can be honored without rewriting Gate 1 itself.

**Alternative that would weaken INV:** ADAPT (reorder the three calls for "readability") would let `tier_field_validate` race ahead of `path_override_check`, allowing the task-level `Tier:` to determine dispatch even when an explicit override was author-intended. That violates INV-05 (the *human-supplied* override would no longer refuse runtime re-classification).

### TU-3 (Gate 2 Verification routing widening) — ADAPT

**Invariants protected:** INV-03 (phase-gate `rf-qa` + post-completion), ME-2 (rf-qa identity).

**Why ADAPT is correct (line 58, line 226).** Widening the roster to `[rf-qa, quality-engineer]` on STRICT is permitted *because* `rf-qa` always remains present — ME-2's "never replaces, never adds a sibling that displaces" binding holds. The verdict is correctly ADAPT (not ADOPT) because the donor's verbatim roster shape required a recipient-side reshape to preserve ME-2.

**Alternative that would weaken INV:** ADOPT verbatim would risk replacing `rf-qa` with a sibling on certain tiers, breaking INV-03's floor. REJECT would leave STRICT under-verified.

### TU-4 (D15b Layer 2 pre-flight) — ADAPT

**Invariants protected:** INV-01 (progress guarantee), INV-04 (resumability).

**Why ADAPT is correct (line 59, line 227).** The F-03 closure (§ 4.3, lines 124–134) explicitly states pre-flight is *environment-prep, not authorization*. ADAPT (rather than ADOPT) is the right verdict because the donor framed pre-flight as a gate; the recipient surface re-frames it as a Task Log emission that warns-and-continues on dirty git. This re-framing is what protects INV-01: refusing task entry on a dirty tree would introduce a new HALT semantic at pre-loop entry (line 130).

**Alternative that would weaken INV:** ADOPT-as-gate (Reading B in § 4.3) would create a brand-new refuse-entry semantic that INV-01's progress guarantee explicitly forbids.

### TU-5 (TFEP Test baseline snapshot) — ADOPT

**Invariants protected:** INV-04 (resumability), INV-03 (rf-qa surface integrity).

**Why ADOPT is correct (line 60, line 233).** The baseline YAML lives on disk pre-F1, which is what makes resumability hold (a resumed task reads the same baseline). The F-04 closure (§ 4.4) does not modify TU-5 — it modifies CR-TASK-09's consumer behavior — preserving the TU-5 ADOPT verdict cleanly.

**Alternative that would weaken INV:** ADAPT to in-memory baseline would break INV-04 across resumption boundaries.

### TU-6 (TFEP Prohibitions + Carve-outs) — ADOPT

**Invariants protected:** INV-02 (prohibited-actions catalog F2).

**Why ADOPT is correct (line 61, line 84, line 234).** The plan explicitly notes TU-6 *reinforces* F2 (line 84) — the prohibitions mirror existing F2 rules and no absorbed feature weakens F2. ADOPT verbatim is the strongest possible posture because reinforcement is additive within an existing catalog.

**Alternative that would weaken INV:** ADAPT (re-author the prohibitions list) risks de-duplication that silently drops an F2 entry.

### TU-7 (TFEP Escalation trigger detection) — ADOPT

**Invariants protected:** INV-03 (rf-qa routing), ME-2 (verifier identity).

**Why ADOPT is correct (line 62, line 235).** This is the load-bearing TU for the third invocation point of `rf-qa`. The F-05 closure (§ 4.5, lines 152–161 and line 26) explicitly authorizes mid-phase routing because (i) it goes to the existing `rf-qa` identity, (ii) it uses the existing spawn pattern at `SKILL.md:191-198`, and (iii) it is the *only* way to honor TU-7's adjudication semantic without authoring a new escalation gate (LR-REJECT-2 / D25 — both REJECTed per the ledger).

**Alternative that would weaken INV:** REJECT would force adjudication into a new gate (D25-revival), which the ledger blocks under R-RULE-11. ADAPT to a sibling verifier would violate ME-2.

### TU-8 (TFEP Incident reporting) — ADOPT

**Invariants protected:** INV-04 (resumability).

**Why ADOPT is correct (line 63, line 236).** The incident report is a side-effect file on disk; it survives session boundaries; CR-TASK-10 explicitly forbids inserting a `## Failure Remediation` heading into the task file (line 236), which would otherwise corrupt the F1-loop's checklist parsing. ADOPT preserves resumability because the file is append-discoverable, not parser-coupled.

**Alternative that would weaken INV:** ADAPT to in-task-file remediation block would break INV-04 (a resumed task would re-parse the heading and either re-execute or skip incorrectly).

## 3. Per-ME steelman (ME-1..ME-9)

### Collective defense

All 9 manifest exceptions are HELD (line 39). Each ME pins a recipient-side invariant that a verbatim donor adoption would have weakened. They are load-bearing in the precise sense that removing any one would re-open a REJECTed ledger entry under R-RULE-11 (line 73, line 206, line 423).

### ME-1 (per-item dispatch forbidden) — load-bearing

**What it protects.** INV-05 + INV-01. ME-1 is the audit gate that prevents the per-item `(Tier: …)` marker from becoming a runtime classifier (§ 4.1 / F-01, lines 95–105; line 213; line 217).

**What breaks without it.** The per-item marker becomes a dispatch input. Each F1 iteration could re-fire Gate 1 with a different profile, defeating the pre-loop pinning that INV-01 relies on for progress monotonicity. D09b (rejected) would functionally return.

### ME-2 (rf-qa never replaced, never displaced by a sibling) — load-bearing

**What it protects.** INV-03's floor. Every widening that touches the verifier roster (TU-3, TU-7) is permitted *only because* ME-2 keeps `rf-qa` present at all three invocation points (line 26, line 85, line 226, line 235).

**What breaks without it.** Any tier-conditioned roster (e.g., STRICT-only `quality-engineer` substitution) could silently swap out `rf-qa` and INV-03 would degrade tier-by-tier.

### ME-3 (no new HALT semantics in F1) — load-bearing

**What it protects.** INV-01 progress guarantee. The F-03 closure (§ 4.3, line 130, line 132, line 206, line 427) leans directly on ME-3 to forbid refuse-entry on a dirty git tree.

**What breaks without it.** Any pre-flight failure mode (dirty tree, missing tool, absent baseline) could be promoted to a HALT, turning every environmental hiccup into a refusal. INV-01 collapses; the loop becomes non-progressing under realistic conditions.

### ME-6 (M1 atomicity) — load-bearing

**What it protects.** The seven foundation rows (lines 212–218) are *only* coherent atomically. The CR-7 / CR-8 ordering sentinels (F-02), the closed-enum `Tier:` parser, and the per-item marker reader are mutually-presupposing — landing them in separate commits leaves intermediate commits that fail their own pre-commit gates.

**What breaks without it.** A commit that lands CR-FM-01 (`Tier:` field) without CR-TASK-02 (Gate 1 dispatch reading the field) leaves a documented-but-unread field — a silent regression vector.

### ME-9 (donor-ceremony drop audit) — load-bearing

**What it protects.** R-RULE-11 (no silent re-litigation of ledger entries). The 10 donor-ceremony drops (line 40, line 470) are explicitly not revived; ME-9 is the audit hook at the Step 5 commit (line 375) that proves they remain dropped.

**What breaks without it.** A "consistency" refactor could quietly re-insert a donor ceremony (a tempting pattern the plan calls out at line 423), re-introducing a REJECTed feature without a re-debate note.

### ME-4, ME-5, ME-7, ME-8 (collective)

All four are HELD without per-row deltas in Phase 7 because no finding F-01..F-08 touched them. The verdict roll-up (line 39: "9 / 9 HELD") and the traceability cross-check (§ 2.3, line 73: zero ledger re-proposals) jointly confirm their stability. Their load-bearing role is to fence ancillary donor patterns (e.g., verbatim ordering, side-channel file shapes, distribution mirror discipline) that none of the eight findings re-opened.

## 4. Sequencing constraint defense (S-1, S-2, S-3)

### S-1 (HZ-03) — in-flight PRD precondition

**Why necessary (lines 319–325).** The in-flight PRD TASK-PRD-20260514-121039 reads the *live* `/sc:task` + `sc-task-protocol` surfaces and `[CODE-VERIFIED]`-tags them. If CR-DEP-01 (soft-deprecation, 10-line redirect stub) lands first, the PRD's verification basis collapses — its subagents would re-read the stub on any re-run and the snapshot loses fidelity.

**Failure mode prevented.** A frozen historical record (the v3.75 pre-deprecation snapshot) that no longer maps to anything readable. Option (a) "sequence completion first" is the cheapest mitigation; (b) snapshot and (c) abort-restart remain as fallbacks (line 325).

### S-2 (HZ-06 + HZ-07) — CLI runtime atomicity

**Why necessary (lines 327–333).** `sprint/process.py` and `cleanup_audit/prompts.py` emit `/sc:task ...` prompts at runtime. Post-CR-DEP-01, `/sc:task` resolves to the 10-line stub and exits; both pipelines stop executing tasks until CR-REF-01 + CR-REF-02 update them to emit `/task` instead.

**Failure mode prevented.** Runtime breakage of two production CLIs between the soft-deprecation commit and the reference-redirect commit. Same-commit landing (line 329) is the only correct mitigation; pre-commit gate (line 333) is the auditable check.

### S-3 (HZ-14) — Makefile sync-rule atomicity

**Why necessary (lines 335–341).** Hard-deleting `[src] sc-task-protocol/` without the Makefile orphan-prune loop landing in the same commit breaks R-RULE-10 (sync drift between `[src]` and `[.claude]`). The next `make sync-dev` would either re-create the directory or fail noisily.

**Failure mode prevented.** Long-lived drift between source-of-truth and dev copy — exactly the failure mode R-RULE-10 exists to prevent. The pre-commit gate `make verify-sync` returning 0 after in-commit `make sync-dev` (line 341) is the structural check.

## 5. F-01..F-08 closure defense

### F-01 (LOW) — correctly closed by naming "tier-conditioned read"

The closure (§ 4.1, lines 95–105) does the right thing by naming the *authorized consumption shape* rather than enumerating forbidden consumers. Naming the authorized shape is generative — it tells any future reviewer exactly what is allowed and routes everything else through ME-1 audit. The rows touched (CR-FM-02 #4, CR-TASK-03) get explicit "never re-fires Gate 1, never modifies item-type dispatch or verifier roster" language (line 105).

### F-02 (MEDIUM) — correctly closed by two-layer enforcement

Two mitigations (§ 4.2, lines 109–121) is the right depth because the failure mode is "readability refactor reorders the three calls." Layer 1 (grep ordering check in CR-FM-04) catches accidental reorders at audit time; layer 2 (sentinel comment + CR-TASK-12 verbatim diff) makes the intent textual and review-visible. Either alone is insufficient; both together close the seam.

### F-03 (MEDIUM, Reading A — log+continue) — the only INV-01-preserving choice

Reading B (refuse on dirty tree) would author a new HALT semantic (§ 4.3, line 130). Reading A is correct because (i) it preserves INV-01's progress guarantee, (ii) it is consistent with the "graceful skip on MCP-tool unavailability" pattern already adopted, and (iii) STRICT pre-flight is environment-prep, not an authorization gate (line 132). The exact Task Log line (`gate-1.5: pre-flight tier=STRICT git_status=dirty action=warn-and-continue`, line 130) is auditable.

### F-04 (MEDIUM, Reading A — over-escalate) — INV-03-spirit-preserving

Reading A (§ 4.4, lines 138–148) classifies every observed `pytest` failure as `classification=new` when the baseline is absent / empty / malformed. The plan's own rationale at line 146 is correct: refusal (Reading B) weakens INV-01; silent skip (Reading C) weakens INV-03's floor; over-escalate preserves both. The cost — a possibly-noisier `rf-qa` queue — is the right tradeoff because INV-03 is a *floor* (under-routing is the failure mode, over-routing is not).

### F-05 (MEDIUM, third-invocation widening) — authorized, not violation

The closure (§ 4.5, lines 152–161, and the dedicated paragraph at line 26) correctly frames mid-phase routing as plan-bound *authorized widening*, not a quiet INV-03 violation. The three-prong defense — (i) existing verifier identity (ME-2 preserved), (ii) existing spawn pattern (`SKILL.md:191-198`), (iii) named in TU-7's recipient form — is necessary and sufficient. Future reviewers see this written down (line 26: "should treat the mid-phase routing as plan-bound, not as a surface widening that requires further authorization") and do not re-open the question.

### F-06 (LOW) — `invariant-bounds.md` substitution correctly recorded

The closure (§ 4.6, lines 164–170) is the right disposition because the anchor language is *byte-identical* (line 24) to what `invariant-bounds.md` would have contained. Forcing retroactive authoring before Phase 7 execution would be ceremony without informational gain. The optional-but-not-blocking framing (line 168) is honest.

### F-07 (LOW) — procedural authorization chain documented

The five-step chain (§ 4.7, lines 174–188) — sprint goal → T06.03 task description → `refactor-sctask-deprecation.md` § 2 rubric → § 4 absorption traceability → structural precondition — is the correct procedural posture. Hard-deletion of `sc-task-protocol/` does not need a manifest amendment because the absorption traceability (line 183) demonstrates the donor body is redundant ceremony per R-RULE-06.

### F-08 (LOW) — count correction

A counting inconsistency ("five" vs "six" refactor files, line 194) is correctly resolved by recording six artifacts grouped into three pairs (line 18, line 196). No row touched; the fix is purely textual.

## 6. Honest concessions (steelman entry points for the analyzer / security variants)

1. **The "tier-conditioned read" boundary is conceptually thin.** The plan acknowledges this (line 97) and bounds it with ME-1 + acceptance-criterion language, but a sufficiently determined refactor could still describe a forbidden per-item dispatch as a "read" if it routes through a wrapper. The defense relies on R-RULE-11 audit discipline at design-time, which is human-process rather than structural.

2. **The third `rf-qa` invocation point (F-05) widens INV-03's surface beyond the canonical anchor language.** The plan calls this "authorized" and documents the three-prong defense, but the anchor source (`extension-point-contracts.md:11-17`) was not amended to mention mid-phase routing. The authorization lives in this plan, not in the anchor — a future reader who consults only the anchor will not see the third invocation point.

3. **F-04 over-escalation is a load-volume bet on `rf-qa`.** Classifying *every* failure as `new` when the baseline is absent could flood the verifier queue under realistic conditions (e.g., a fresh repo with no baseline yet on a STRICT task). The plan does not bound the upper limit on this routing volume.

4. **S-1's mitigation hierarchy (a / b / c) is recorded but not decided.** Line 325 leaves the choice "at Phase 7 execution time." A late-discovered infeasibility of (a) means options (b) snapshot or (c) abort-restart get chosen under time pressure rather than upfront analysis.

5. **The procedural authorization chain (F-07) is "not a manifest binding."** Line 186 explicitly says so. A future reviewer who applies strict-manifest-only discipline could insist on retroactive amendment despite the chain being documented; the plan asks future reviewers to accept the chain (line 186) but cannot compel them to.

## 7. Acceptance criteria — testable claims that validate the steelman

| AC | Testable claim | Validation method |
|---|---|---|
| **AC-SM-01** | All eight V/C/K verdicts (TU-1..TU-8) match `transfer-manifest.md` § 4 byte-for-byte | Diff TU-row table at lines 54–63 against `transfer-manifest.md` § 4 |
| **AC-SM-02** | Each ME-1..ME-9 traces to at least one CR-row acceptance-criterion or sequencing constraint | Cross-grep ME-N against § 5 row text and § 6 constraint text |
| **AC-SM-03** | The `invariant-survival-walkthrough.md` worked example demonstrates INV-01..INV-05 survive on the merged surface | Independent re-read of that file's § 2 + § 3 |
| **AC-SM-04** | F-01..F-08 each cite a re-readable Phase 7 artifact line range | Grep § 4 dispositions for `plan-adversarial-review.md` / `compat-hazard-report.md` / `traceability-gap-report.md` references |
| **AC-SM-05** | S-1..S-3 each cite a named hazard (HZ-NN) in `compat-hazard-report.md` | Grep § 6 for `HZ-03`, `HZ-06`, `HZ-07`, `HZ-14`; confirm they exist in source |
| **AC-SM-06** | The 67-row count and 10-step commit sequence are unchanged from `merge-master.md` § 1 + § 6 | Row-count check on § 5; step-count check on § 6 |
| **AC-SM-07** | CR-FM-04 ordering greps return the three function names in the expected order against `[src] skills/task/SKILL.md` | Execute the two greps named at lines 116–117 and 243 |
| **AC-SM-08** | CR-TASK-12 returns 7 zero-diff invocations (6 donor strings + 1 sentinel-comment block) | Execute the seven diffs after Step 1 lands |
| **AC-SM-09** | Step 5 commit contains exactly the rows named at line 375 (CR-DEP-01, CR-DEP-02, CR-DEP-05, CR-REF-01, CR-REF-02, CR-REF-09, CR-DOC-01) | Inspect the merge commit's file list |
| **AC-SM-10** | Step 6 commit contains exactly the rows named at line 381 (CR-DEP-03, CR-DEP-04, CR-DIST-02, CR-DIST-01, CR-DIST-04, CR-REF-10) | Inspect the merge commit's file list |
| **AC-SM-11** | Zero ledger entries from `rejected-features-ledger.md` are re-proposed across the 65 distinct CR-IDs | Cross-grep ledger CR-IDs against § 5 |
| **AC-SM-12** | Pre-commit gates for Steps 1, 5, 6 all return 0 on a clean checkout | Execute the gates named at lines 351, 377, 387 |

If AC-SM-01 through AC-SM-12 all pass, the steelman is validated: the plan's invariant claims are auditable, its sequencing constraints are enforceable, and its row-deltas are structurally bounded. Failure of any single AC is the correct entry point for the analyzer / security variants to attack.

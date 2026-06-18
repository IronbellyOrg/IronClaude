# Round 1 — Advocate for variant-C (BLIND, truth-seeking)

## 1. Position summary

variant-C is the only variant whose central framing survives contact with git and with the evidence package: this is a **G1 gate-approval document** — the troubleshoot hardening refactor is a SPEC, NOT a built/validated change, implementation is HALTED pending approval, and the canonical escape set is frozen at exactly **E1–E5 (5 items)** by `GATE-0.md`. variant-A and variant-B both assert a completed, rollback-replay-validated refactor (8/8 and 7/7, 100%) that **does not exist in git** — that claim is a hallucination, and it is load-bearing for their entire §5/§6. C should be the structural base; A/B contribute the quantitative scorecard and would-have-caught machinery that C lacks, which must be re-derived honestly post-G1.

## 2. Steelman of A and B

**variant-A (strongest version).** A is the most analytically sophisticated variant. Its genuine, non-fabricated contributions are independent of the false "refactor is built" claim:
- The **patch-relative vs baseline-relative distinction** (§5) is the single sharpest insight in the entire field: M3/F-A/F-B are properties that exist *only after the candidate fix is applied*, so no forward pass over un-patched code can see them. This is correct and important regardless of whether the refactor was built.
- The **negative-witness / falsifiability discipline** (R-1: "shown capable of failing by reproducing the defect with the fix absent") with cross-domain generality (TDD red-green, wet-lab assay controls, chaos engineering) is the best-grounded remediation primitive across all three variants.
- A is **honest about the static-vs-runtime boundary** (§7): it concedes the pipeline does NOT achieve coverage by static analysis alone. That intellectual honesty is real.
- A correctly states **PR #158 does not exist in git** and pins the real fix to local `b97c9960` — both verifiable and correct (confirmed: `b97c9960 fix(prd): honor advisory checks in the executor's _evaluate_gate` IS in git; no `#158` is).

**variant-B (strongest version).**
- B's **4-cause taxonomy isolating SC4 "human-readable taxonomy vs executable API identity"** is a clean, reusable decomposition; the Executable Contract Identity Ledger (4.4) is the most operational consumer-enumeration mechanism of the three.
- B is **deliberately conservative on F-B**: it refuses to count bisection-hygiene as an efficacy "miss," which is defensible denominator discipline.
- B's would-have-caught matrix is tighter (7 rows, one mechanism each) and its bottom line is appropriately hedged ("provided run in pipeline-health mode and gates enforced not waived").

What both get right and C does NOT have: a **per-stage theatre scorecard with numbers**, a **would-have-caught matrix**, and an explicit **map-vs-territory irreducibility analysis**. Those are real assets a merged report needs.

## 3. Strengths of variant-C (cited)

1. **Correct structural framing — confirmed by the evidence package itself.** C: "Status: **G1-ready, implementation pending approval**" (line 5) and the "Explicit G1 halt note" (lines 206–208). `G1-APPROVAL-REQUEST.md` reads verbatim: "Status: awaiting human approval. No shared skill or command files have been edited for this G1 draft." `troubleshoot-pipeline-hardening-spec.md`: "Status: G1 approval draft only. Do not edit src/superclaude/ ... until G1 approval is granted." C is the *only* variant aligned with the deliverable contract.

2. **Escape-set cardinality matches the frozen Gate-0 ledger exactly.** C freezes E1–E5 (5 items, "Frozen canonical escape set" table, lines 40–46). `GATE-0.md`'s "Canonical escape set" is E1–E5, and exactly five `escape-E1..E5/` directories exist on disk. A's 8 (M1–M6+F-A+F-B) and B's 7 (M1–M7) are finer-grained *re-derivations* of the same underlying events, not the canonical frozen set.

3. **The "41% value / 59% theatre" figure is a grounded quote, not an invention.** `theatre-vs-value-scorecard.md` line 5: "Estimated net defect-catching value: **41% value / 59% theatre or mis-targeted ceremony.**" C (line 13) cites it verbatim. A's 6.25% and B's 3.0% are *self-constructed* per-stage ratios with no anchor in the frozen scorecard.

4. **Most operational remediation surface.** C ships a full protocol spec — 7 reusable closure controls (lines 84–119) plus the H0–H5 wave/gate design (lines 139–166) with machine-checkable output statuses (lines 170–181) and `NOT PROVEN` blocker semantics. This is the most directly implementable artifact of the three (diff-analysis U-005 agrees).

5. **Process discipline is correct, not pedantic.** C's halt note (lines 206–210) correctly forbids editing `.claude/` mirrors and routes through `make sync-dev` / `make verify-sync` — matching the repo's actual SoT rules. A/B, by *claiming the edits are already made and replayed*, implicitly assert a forbidden action took place.

6. **Highest-leverage-stage claim is grounded.** C: "Fix `task-builder` first" (line 35) matches `theatre-vs-value-scorecard.md` line 56 ("`task-builder` as the best first fix because it can make the right evidence mandatory for every later gate").

## 4. Weaknesses in A and B (cited)

1. **A/B's core claim — "refactor implemented + rollback-replay validated" — is a hallucination unsupported by git (HIGH).** A §6: "The refactored pipeline was rolled back ... and replayed ... Final coverage 100% (8/8)." B §6: "Rollback replay result after refactor round 2: 7 of 7." **Git reality:** the most recent commit touching `sc-troubleshoot-protocol/` or `commands/troubleshoot.md` is `013ba2cc` (Wave 1.6 Diagnosability Audit, #107) — *predating the entire M-series episode*. The current `SKILL.md` has Waves 0–6 with **no Wave 4.5/4.6/4.7/4.8/5.5, no "Pipeline Hardening Closure," no patched-shadow re-sweep**, and `refs/` contains **none** of the new files (no `pipeline-hardening-closure.md`, `runtime-entrypoint-verification.md`, etc.). No rollback-replay run exists. A and B both narrate a validation event that never happened. This is the highest-stakes defect in the field and it sits at the center of their reports.

2. **A and B contradict each other on the lone adversarial catch (X-001) — at most one can be right.** A: the catch "was actually delivered by the **human PR reviewer downstream of the adversarial pass**, not by the debate" (line 11). B: adversarial "caught only M7 ... PR review / adversarial review activity during #154" — crediting the adversarial surface. They cannot both be correct; this is direct mutual contradiction on a factual attribution.

3. **A/B's quantification rests on a denominator they invented (A-002).** A's "16 should-have-caught obligations" and B's "33 expected catches" produce wildly different theatre ratios (0.94 vs 0.97) from the *same episode* — neither is anchored to the frozen scorecard's 59%. The precision (6.25%, 3.0%) is false precision over a contested denominator.

4. **B treats "#158" as a real/equivalent ref (X-005).** B: "local / PR #158-equivalent commit b97c9960." Git confirms **no PR #158 exists**; A is correct to flag this and B's "equivalent" softening blurs a falsifiable git fact.

## 5. Concessions (honest weaknesses in variant-C)

1. **C lacks the quantitative theatre scorecard (S-004) and the per-stage denominators (C-004).** C gives only the single global "41%/59%" line and no per-stage `should_have_caught/did_catch` table. For a *retrospective efficacy audit*, A/B's per-stage scorecard is genuinely more informative; the merged report should adopt A/B's scorecard *structure* while keeping C's grounded global figure as the headline.

2. **C has no would-have-caught matrix (S-005) and no rollback-replay section (S-006).** This is defensible given C's G1-pending framing (you cannot replay an unbuilt refactor), but it means C is *incomplete as a standalone efficacy audit*. The merge needs A's would-have-caught *mechanism mapping* (especially the patch-relative M3/F-A/F-B closure) re-cast as **"predicted coverage, to be validated post-G1 backtest"** rather than C silently omitting it.

3. **C's 5-item set under-resolves M6 (resume step-ID mismatch), which is real and live.** Confirmed in current code: `executor.py:259` emits `research-qa`/`synthesis-qa` while `config.py:30` `_STEP_ID_PATTERN` accepts `qa-research-gate` — the mismatch still exists, uncommitted. C folds this under E-level generality and does not surface it as a distinct frozen escape. A/B's explicit M6 row is more actionable here. (This is granularity, not a framing error — Gate-0 also froze at 5 — but the merge should carry M6 forward as a named instance under C's E-family.)

## 6. Per-contradiction stance (X-001..X-008)

- **X-001 — who made the lone adversarial catch.** *C-defensible / A-and-B-both-suspect.* C declines to credit adversarial with a catch and instead credits `sc:reflect` with the distinct E5 wrong-diff/base catch — which `theatre-vs-value-scorecard.md` line 24 directly supports ("Reflect ... caught the wrong-diff/base-selection trap in E5"). A and B mutually contradict (human-tail vs debate-surface). **Stance: C's attribution is the best-grounded; merge should adopt C's reflect=E5 credit and treat the adversarial catch as A's "human-tail" reading (more conservative) pending evidence.**

- **X-002 — theatre ratio.** *C-correct on grounding.* C's 59% is a verbatim quote from the frozen scorecard; A's 0.94 and B's 0.97 are self-derived over an invented obligation count. Merge headline = 59% (grounded); A/B per-stage table may appear as a secondary, clearly-labeled re-derivation.

- **X-003 — escape-set cardinality.** *C-correct as canonical; A/B finer-grained.* `GATE-0.md` + 5 on-disk `escape-E*` dirs freeze the set at E1–E5. C matches the canonical freeze. A's 8 / B's 7 are legitimate sub-decompositions and should be merged in *as instances under the E-family*, not as a competing top-level count.

- **X-004 — is F-A a miss or a forensic rider.** *Qualify; B's exclusion of F-B is the cleaner call.* C folds the completion-substring issue into E2/E3 mechanism, which is reasonable. A counts F-A as externally-caught and F-B as not-a-pipeline-bug; B promotes F-A→M7 and drops F-B. **Stance: keep F-B OUT of the efficacy denominator (B's discipline), keep F-A as a real primitive-layer instance under C's E2/E3 family.**

- **X-005 — does PR #158 exist.** *A-correct; B-wrong; C-silent-and-safe.* Git: `b97c9960` exists, no `#158` exists. A is right. B's "#158-equivalent" is a factual softening of a falsifiable claim. C avoids the trap by not asserting a SHA. Merge must use A's exact framing: real fix = `b97c9960`, #158 is a phantom seed ref.

- **X-006 — scope of the report (efficacy-audit vs gate-approval).** *C-correct on the deliverable contract.* The evidence package is a G1 gate (`GATE-0.md`, `G1-APPROVAL-REQUEST.md`, `troubleshoot-pipeline-hardening-spec.md` all in "draft/awaiting approval" state). C's gate-approval framing is the correct outer container. **Concession:** the gate-approval container should *embed* an efficacy-audit section (A/B's scorecard + would-have-caught) as its justification — C's container, A/B's contents.

- **X-007 — is the refactor implemented & validated.** *C-CORRECT, decisively, on git evidence.* This is the highest-stakes contradiction. C: "Implementation and backtest are **pending G1 approval**" — matches git (no hardening commit; SKILL.md unchanged since #107; refs absent) and matches the evidence package's own "awaiting approval" status. A's "8/8 round 2" and B's "7/7" describe a validation that never ran. **A/B are hallucinating a completed refactor.**

- **X-008 — coverage achievability by static analysis.** *Qualify in C's favor.* A and B both claim 100% (A honestly caveats "not by static alone"; B caveats "if gates enforced"). C makes **no coverage claim**, correctly, because the refactor is unbuilt — you cannot honestly claim coverage for an unimplemented spec. **Stance: C's no-claim is the correct posture pre-G1; A's static-vs-runtime irreducibility analysis is excellent and should be carried into the post-G1 backtest plan as a predicted, not asserted, result.**

## 7. Shared-assumption responses

- **A-001 (escape set is complete/correctly attributed): QUALIFY.** Gate-0 froze E1–E5, but the live M6 mismatch confirms the *granularity* is debatable; completeness holds at the E-family level, not at A/B's exact M-count.
- **A-002 (should-have-caught is a fair denominator): REJECT as stated.** A's 16 and B's 33 are invented and irreconcilable; the only grounded figure is the scorecard's 59%. Use stage-level value/ceremony, not a fabricated obligation count.
- **A-004 (each root cause is validated, not merely plausible): ACCEPT.** The per-escape `escape-E*/root-cause.md` dirs + `defect-escape-table.md` + Gate-0 give independent validation; all three variants inherit this fairly.
- **A-005 (the 5 review surfaces are the exhaustive stage inventory): ACCEPT.** troubleshoot/task-builder/reflect-PRE/reflect-POST/adversarial is consistent across all three and matches the per-stage `stage-value-*.md` evidence files.
- **A-008 (genuine serial-unmasking whack-a-mole): ACCEPT.** Git ordering (#151→#154→#155→b97c9960→07cb149f) and `timeline.md` confirm the serial-unmask chain; C's RC3 sibling-surface framing is the same mechanism.

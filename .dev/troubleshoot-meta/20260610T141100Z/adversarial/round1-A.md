# Round 1 — Advocate for variant-A (BLIND, truth-seeking)

## 1. Position summary

variant-A is the strongest *analytical core* for a merged report: it has the most precise root-cause mechanics (serial-unmasking chain, dual-evaluator map-vs-territory, patch-relative vs baseline-relative), the most rigorous and falsifiable git grounding (correctly denies PR #158, correctly flags M5/M6 as not-on-master / uncommitted), and the only genuinely novel remediation primitive (negative-witness admission). However, variant-A is fatally overstated on ONE axis that git falsifies: its §6 rollback-replay "100% round 2 (8/8)" and the implied claim that the refactor was implemented are **fabricated** — the troubleshoot source files contain none of the claimed waves. On that single point variant-C is correct and must govern the merged deliverable's status framing.

## 2. Steelman of B and C

**variant-B (steelman).** B's deliberate exclusion of F-B (bisection hygiene) from the efficacy denominator is defensible: F-B is not a pipeline-prevention miss, so counting it inflates the "should-have-caught" set. B's SC4 — "human-readable taxonomy substituted for executable API identity" — is the sharpest single naming of the cross-cutting failure (`--file` looked local, `gate_passed` looked like the oracle, report names looked like step IDs); it isolates a mechanism A folds into SC-1/SC-3. B's Executable Contract Identity Ledger (4.4) with owner/producer/consumer/grammar/round-trip is the most directly actionable contract artifact of the three. B genuinely gets right that the decisive oracle was always live execution.

**variant-C (steelman).** C is correct on the single highest-stakes fact in this whole debate: **the refactor was not built; implementation is pending G1 approval.** That is not timidity — it is honesty that A and B both violated. C's 41%/59% theatre figure is the only quantification traceable to an actual evidence card (`theatre-vs-value-scorecard.md`), rather than to a self-constructed should-have-caught denominator. C's H0–H5 wave spec with machine-checkable output statuses, NOT-PROVEN blocker semantics, and a paste-ready G1 approval prompt is the most operationally complete refactor *design*. C's "fix task-builder first" ecosystem-prioritization is a real insight A lacks. C genuinely gets right that a forward gate-approval document, not a victory-lap audit, is the correct deliverable contract for the actual state of the work.

## 3. Strengths of variant-A

1. **Patch-relative vs baseline-relative distinction (U-001).** §5: "they are PATCH-RELATIVE, not baseline-relative, and invisible to any forward pass over un-patched code." This is the single most important conceptual contribution in any variant — it explains *why* M3/F-A/F-B are structurally different from M1/M4 and require shadow-apply + diff-lint + commit-scope waves. B and C have no equivalent framing.
2. **Negative-witness admission as a gate property (U-002).** §4 R-1(c): "demonstrated falsifiability — shown capable of failing by reproducing the defect against reality with the fix *absent* before being accepted." Cross-domain generality (TDD red-green, wet-lab assay controls, chaos engineering) is the deepest generalization in the set.
3. **Correct, falsifiable git forensics on M4.** §2 M4: "seed's 'PR #158' does not exist in git history — confirmed; only b97c9960 adds the advisory branch to `_evaluate_gate`." Verified true: `b97c9960` exists; no #158 in git log. B says "PR #158-equivalent," conflating a nonexistent ref.
4. **Honest commit-state labeling.** §2 marks M5 `07cb149f` "NOT on origin/master" and M6 "UNCOMMITTED — not in git at all." Both verified: `07cb149f` is an unknown revision; `qa-research-gate` sits in the working-tree config.py uncommitted.
5. **Irreducibility analysis (§7, U-003).** A is the only variant that enumerates what is un-catchable by static reading alone (map-vs-territory, shadowed downstream, unmasking) and concedes its own coverage is "not all in a single purely static shot" — intellectual honesty B lacks despite B's stronger headline claim.
6. **Sharpest M4 exemplar.** §2 names the dual evaluators with file:line ("executor.py ~764→850"), verified: `_evaluate_gate` defined executor.py:825, called :764, distinct from `gate_passed`.

## 4. Weaknesses in B and C

1. **B fabricates the replay (X-007).** B §6: "Rollback replay result after refactor round 2: 7 of 7 misses caught. Final coverage: 100%." Git shows the troubleshoot SKILL/command files contain none of B's H0–H5 / `pipeline-health` mechanisms; last relevant commit is #116. The replay never happened.
2. **B mis-handles PR #158 (X-005).** B §2 M4: "local / PR #158-equivalent commit b97c9960" treats a nonexistent PR as a real equivalent ref. A's flat denial is the correct evidentiary posture.
3. **B's 33-obligation denominator is the most inflated (X-002, C-004).** B assigns should-have-caught of 6/6/7/7/7, producing 97% theatre. These per-stage denominators are self-constructed and not grounded in any evidence card; C's 41% is the only source-traceable figure.
4. **C omits the would-have-caught matrix and theatre scorecard entirely (S-004, S-005).** For a *merged efficacy report*, C lacks per-stage scoring and per-miss attribution — the analytical heart of the deliverable. C's strength is the spec, not the audit.
5. **C collapses M5/M6 (C-003, C-006).** C's 5-item E1–E5 set folds the verdict-parser and resume-ID mismatches together, losing the distinct cross-component identifier-contract mechanism A isolates as M6.
6. **C credits the lone catch to sc:reflect (E5), not adversarial (X-001).** Defensible but it abandons the adversarial-stage scoring entirely, leaving the efficacy ledger incomplete.

## 5. Concessions (genuine weaknesses in variant-A)

1. **X-007 — A's replay claim is false. Conceded fully.** §6 "100% (8/8), round 2" and §5's three "NEW" waves (4.7/4.8/6.5) presuppose an implemented refactor. Git: `src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md` and `commands/troubleshoot.md` contain NONE of these waves (grep empty); last troubleshoot-protocol commit is #116, predating this episode. **The refactor was not built and was not replayed.** This is the highest-stakes claim in the debate and C is right, A is wrong. The merged report MUST adopt C's "implementation pending G1 approval" status and treat A's would-have-caught matrix as a *projected/design-time* analysis, never as validated replay evidence.
2. **X-002 — A's theatre math is a self-serving artifact.** A's "16 obligations / 1 catch = 6.25%, stack ≈0.94" rests on per-stage should-have-caught of 2/4/3/4/3, which A chose. The only figure grounded in an evidence card is C's 41%/59% (`theatre-vs-value-scorecard.md`). A's aggregate theatre ratio should be demoted to "illustrative" or replaced by the source-grounded blended figure in the merge.
3. **Minor: A's §7 "yes for static coverage" headline is in tension with its own concession that 3+ misses need execution** — the hedge is honest but the section header oversells.

## 6. Per-contradiction stance

- **X-001:A-correct** — defect-escape evidence + #154's own commit body show F-A's `\b`/`re.escape` fix landed via the merge-prep/PR-review tail, not the design debate; A's "human PR reviewer downstream of adversarial" is the most accurate attribution. B's "adversarial review activity" over-credits the debate; C drops it.
- **X-002:C-correct** — only C's 41%/59% traces to `theatre-vs-value-scorecard.md`; A's 6.25% and B's 3.0% are both self-constructed denominators. (Conceded against A.)
- **X-003:A-correct(qualified)** — A's 8-item set (M1–M6+F-A+F-B) is the most complete *enumeration*; but for the efficacy *denominator*, B's exclusion of F-B as a non-prevention rider is fair. Merge: enumerate 8, score on the prevention-relevant subset.
- **X-004:A-correct** — F-A is a forensic rider caught by external human review, not an in-scope stack catch; verified it was fixed inside #154 post-design. B's promotion of F-A to "M7 the adversarial caught" is wrong on attribution.
- **X-005:A-correct** — git confirms `b97c9960` exists and no PR #158 exists. A denies #158 explicitly; B asserts equivalence; C silent. A is evidentially correct.
- **X-006:C-correct** — given X-007, the true deliverable state is a forward gate-approval document, exactly C's framing. A/B's retrospective "completed + replayed" scope misrepresents reality.
- **X-007:C-correct** — DECISIVE. Refactor NOT implemented (grep of source files empty; no troubleshoot commit this episode). A's 8/8 and B's 7/7 replays are fabricated. (Conceded fully against A.)
- **X-008:C-correct(partial)** — since the refactor is unbuilt, no 100%-coverage claim is currently provable; C's deferral to post-G1 backtest is the only defensible posture. A's static-vs-runtime caveat is the best *projected* analysis and should be preserved as design rationale, not as a coverage result.

## 7. Shared-assumption responses

- **A-001:QUALIFY** — Escape set is reasonably complete but A(8)/B(7)/C(5) disagree on membership; merge should reconcile to a superset with prevention-relevance tags rather than assume any one set is canonical.
- **A-002:QUALIFY** — "should-have-caught" is a fair *frame* but the specific denominators are unvalidated; bind scoring to the evidence card, not to per-variant invented counts.
- **A-004:ACCEPT** — root causes are independently corroborated by git (M4 dual-evaluator, F-A superstring, F-B bundle all verified); causal validity holds.
- **A-005:ACCEPT** — the five-surface stage inventory (troubleshoot/task-builder/reflect-PRE/reflect-POST/adversarial) matches the stage-value cards on disk; exhaustive for this episode.
- **A-008:ACCEPT** — serial-unmasking "whack-a-mole" is confirmed by the commit timeline (#151→#154→#155→b97c9960) where each fix advanced the runtime frontier to the next gate; not coincident bugs.

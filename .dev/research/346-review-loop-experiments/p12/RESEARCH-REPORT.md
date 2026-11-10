# Research: Easily adaptable methods for LLM document review-loop convergence (Prompt 1)

Date: 2026-11-10. Status: COMPLETE. (Sections 1-5 verbatim from the owner's report; the running sources log is omitted.)

## 1. Executive summary

CONFIDENCE: HIGH that the direction of each recommendation is supported; LOW on effect magnitudes (our cells are 3-6 runs; external benchmarks are code review and math QA, not document review).

The single most supported finding: our residual problem is a RECALL problem of independent samples, not a precision problem. Different first reviews catch different subsets of the same defects; aggregating several independent review passes is the best-evidenced fix (Multi-Review, arXiv 2509.01494: Self-Agg n=10 recall +118.8% rel, F1 +43.7% rel; gains already strong at n=3-5). Second: any finding that will drive an edit should pass a separate verification step with evidence-or-drop, before the fixer runs (QASecClaw precision 0.695->0.951 at -3.2% rel recall; G-Research two-pass; CodeRabbit judge model; Anthropic verification stage). Third: the intrinsic-self-correction literature says a reviewer that shares context with the author/reviser verifies its own blind spots - verification should come from a fresh context, ideally a different model family (self-preference is replicated across 8 models, ~41k queries). Fourth: the merge-queue analogy directly supports our candidate step: scoped re-review verifies the diff, but the artifact must be gated "in the state it will be in after merging" - i.e., a final full-document check, with any blocker starting a new bounded loop that drops out cleanly on failure or stall. Fifth: stopping rules need three explicit parts (approval signal, budget cap, diminishing-returns/stall detection); a loop that only has a cap oscillates, one that only has approval over-runs.

## 2. Ranked table of techniques

Grades: A replicated empirical, B single study/benchmark, C practitioner report, D opinion. Expected effects are directional estimates for OUR harness (residual blocking defects / doc growth / tokens / convergence).

| # | Technique | Mechanism | Source, grade | Expected effect | Adopt cost | Main risk |
|---|---|---|---|---|---|---|
| 1 | k=3 independent first reviews, union with dedup | Three fresh-context first reviews of the whole doc; merge findings by id/quote dedup; verify merged set once | arXiv 2509.01494 (B+); self-consistency k-curve (A) | Residual blocking defects down sharply (recall-driven); growth ~unchanged (verify gate first); tokens ~+2x first-review stage, ~+30-50% total; convergence unchanged | 2-4 h | Union imports each reviewer's FPs; without a verify gate this re-inflates growth |
| 2 | Verify-before-fix gate (evidence-or-drop) | Second fresh-context agent re-reads the cited lines and confirms/rejects each blocking finding; rejected ones are dropped, never fixed | arXiv 2605.01885 (B); G-Research two-pass (C); CodeRabbit judge (C) | Precision of blocking findings up (~0.70->~0.95 in the SAST analog); fewer wasted fix cycles; slight recall loss; tokens +~15% | 2-3 h | Verifier rejects a true blocking defect; mitigate by keeping rejected items in a "noted, unactioned" list, never silently deleted |
| 3 | Final whole-document gate after scoped PASS (merge-queue analog) | After a scoped PASS, a labelled whole-document FIRST review (fresh context, no loop history) runs once; any blocking finding starts a new bounded loop | GitHub merge queue docs, GitLab merge trains (C) | Residual blocking defects down; growth small if the same blocking rubric applies; tokens +1 whole-doc review per converged run (+~20%); convergence: needs its own cap | 3-5 h | Gate findings restart loops; without a stall rule this reintroduces non-convergence. Cap at 1-2 gate-triggered loops, then escalate |
| 4 | Perspective/theme-split reviewers (PBR analog) | Short dedicated sweeps: contradiction sweep (cross-section pairs), acceptance-check executability sweep, path-rule collision sweep | Porter-Votta-Basili (A-family, mixed); ALICE (B) | Targets exactly our three recurring defect themes; per-theme recall up | 2-4 h | Checklist staleness |
| 5 | Deterministic severity from the rubric | Severity computed from finding attributes the reviewer must state (named wrong outcome / data-loss-security / quoted contradiction pair); absent attributes => cannot be blocking | G-Research RFC-2119 mapping (C); arXiv 2604.23178 (B) | Over-blocking down; growth flat | 1-2 h | Rubric wording becomes load-bearing |
| 6 | Explicit 3-part stopping rule (approval + budget + stall) | Loop ends on PASS, review cap, or when a round reproduces the same blocking findings as the previous round ("stalled" -> escalate) | max-gherman.dev (C); ESC arXiv 2401.10480 (B) | Prevents oscillation restarts; bounded | 1-2 h | Stall detection by exact set equality is brittle; compare by ids/quotes |
| 7 | Cross-model or fresh-context verification | Verifier is a different model family than the finder, or at minimum a fresh context with no loop history | EMNLP 2025 self-preference (B); arXiv 2509.26464 (B) | Reduces self-preference confirmations | 0-2 h | Only Sonnet-class workers available => fresh-context fallback, weaker |
| 8 | Mechanical evidence block per finding | Verbatim quote + location + falsifiable outcome; findings without it are dropped | LLVM agent review (C); CRITIC (B) | Auditable findings; verifier has something mechanical to check | 1-2 h | Quote padding |
| 9 | Binary verdicts per finding | blocking yes/no under the frozen rubric; no 1-5 numbers in the driving decision | Comet/Husain (C) | Fewer borderline blocking calls | <1 h | Loses prioritization signal |
| 10 | Tiered assurance by severity | Blocking findings get finder->verify->fix->re-verify; medium/minor recorded only | OpenAI forum (C/D) | Bounds tokens per finding class | 1 h | Tier errors propagate |
| 11 | Best-of-2 reviser with verifier selection | Two candidate fixes per blocking finding, verifier picks the smaller that passes | Best-of-N literature (B) | Growth down; tokens +1 fix | 2-3 h | Verbosity bias |
| 12 | Known-FP learnings list | Short list of confirmed false-positive patterns injected into reviewer prompt | CodeRabbit, Cloudflare (C) | FP rate down | 1 h + maint. | Stale learnings |
| 13 | Instruction single-home + hard gate | Blocking rubric lives in exactly one file; a mechanical check rejects reviews that don't cite it | Our lesson 3 (3/3 vs 2/3) | Instruction-following up | 1-2 h | Single point of failure |
| 14 | Deletion-preferring reviser (already adopted; keep) | Reviser touches only named blocking ids; prefers deleting | Our own A/B (12/12 vs 0/3) | Growth ~1% (measured) | 0 | None observed |

## 3. Top-5 A/B test designs (our harness: same 57 KB document, 3-6 replicates/arm)

Common metrics for all: (a) residual blocking defects found by the SAME independent whole-doc audit we already run; (b) document growth %; (c) total output tokens; (d) converged within cap (y/n) and review count. The audit stays frozen across arms. Baseline arm = current new setup (12/12 converged, 1-3 residual blockers in 10/12).

### 3.1 k=3 independent first reviews, union + dedup + verify
- Arms: A1 baseline (k=1). A2 k=3 union with the verify gate from 3.2 (they interact; test together first, then ablate the verify gate if needed).
- Replicates: 5 per arm (k=3 triples the first-review sampling; 5 runs give 15 first-review samples for subset-overlap analysis).
- Exact change: coordinator spawns 3 reviewer agents in parallel, each with a FRESH context, the same blocking rubric, and no shared transcript; each returns the standard findings block. A merge step (deterministic in the coordinator prompt, not an agent) dedups by (quoted span, defect theme); every surviving finding goes to the verify gate before the reviser sees it.
- Drop it if: residual blocking defects do not decrease by at least ~half vs baseline (e.g., 10/12 runs with defects -> 5/12 or better), or tokens exceed ~2x baseline without a recall gain. Also drop if the union's FP inflow (verifier rejections > 50% of merged findings) makes the verify gate the bottleneck.
- Secondary read: measure per-defect capture across the 15 samples to estimate whether k=2 would suffice.

### 3.2 Verify-before-fix gate (independently testable)
- Arms: B1 baseline (findings go straight to reviser). B2 every blocking finding passes a fresh-context verifier that re-reads the quoted span plus its collision partner and returns confirm/reject with one sentence; rejects are logged as notes, never fixed.
- Replicates: 5 per arm.
- Exact change: insert one agent step between review and revise. Verifier prompt: "For each finding: quote the span from the candidate document yourself (grep it), state whether the quoted text exists and whether the stated wrong outcome follows. Confirm only if both hold. You see only the document and the finding list, not the reviewer's reasoning."
- Drop it if: verifier rejection rate on TRUE blockers (audit-confirmed) exceeds ~10% (we are losing recall), or residual defects unchanged AND tokens up >25%.

### 3.3 Final whole-document gate after scoped PASS
- Arms: C1 baseline. C2 after any scoped PASS, run one labelled whole-document FIRST review (fresh context, same rubric, explicitly told "this is a first review of a complete document; no prior rounds exist"). Blocking findings start a new bounded loop (max 1 gate-triggered loop, then escalate); zero blocking findings = final PASS.
- Replicates: 5 per arm.
- Exact change: one new coordinator step + the label sentence in the reviewer prompt. Cap: total reviews per run becomes 3 scoped + up to 2 gate (gate review + 1 scoped re-review), hard ceiling unchanged in spirit: any loop still ends in PASS/FAIL/escalate.
- Drop it if: residual defects after the final gate still show the same three themes in >= 4/5 runs (the gate reviewer misses them too - would point to needing theme sweeps, 3.4), or convergence drops below 3/5 (gate findings oscillate), or tokens exceed ~1.8x baseline.
- Expected: this is the merge-queue pattern (test the artifact in its final state); the strongest analog evidence but zero direct LLM-document studies (see negatives).

### 3.4 Theme-split first review (contradiction sweep as its own reviewer)
- Arms: D1 baseline single general reviewer. D2 three short sweeps in parallel, each with a 5-line theme brief: (i) cross-section contradiction sweep, (ii) acceptance-check executability sweep, (iii) collision sweep (global rules vs per-item rows).
- Replicates: 4-5 per arm. Themes derived from our three recurring audit defects (PBR's known limitation).
- Drop it if: no reduction in the three target themes vs baseline, or new defect classes appear that the general reviewer used to catch.

### 3.5 Deterministic severity + evidence-or-drop
- Arms: E1 baseline. E2 reviewer outputs {verbatim quote, second colliding quote OR named wrong outcome, severity computed from which evidence fields are present}. Blocking iff the record contains a wrong-outcome sentence or a quoted contradiction pair; otherwise demoted to note mechanically.
- Replicates: 5 per arm.
- Drop it if: blocking-finding precision does not improve, or the audit finds MORE residual defects.

## 4. The follow-up whole-document step: what the evidence says

Who runs it: a fresh context with no loop history, labelled as a FIRST review of the complete document (self-preference and anchoring; our lesson 6: one first review in six PASSed a document the audit failed). Different model family beats same-model-fresh-context if available. The gate reviewer should NOT be the same agent instance that produced any prior PASS.

How many blockers trigger a new loop: ANY verified blocking finding (post verify-gate) triggers a new bounded loop. Unverified findings do not. The verify gate in front of the loop trigger is the load-bearing detail.

How to cap it: hard cap of 1 gate-triggered loop per run (gate review + scoped fix + scoped re-review), then escalate with the open findings. Stall rule: if the gate-triggered loop's findings are the same ids/quotes as a previous round, stop and escalate ("stalled"). Cost control: the gate is one whole-document review (~+20-30% on our 0.33M-token runs). Do not skip the gate on no-edit runs (lesson 6).

## 5. Negative results

No direct study of scoped re-review then whole-document final gate for LLM document review loops (only CI merge-queue analogs). No rigorous k-selection study for reviewer ensembles on long documents. No measurement of deletion-vs-addition reviser policies for LLM document editing. Nothing on the effect of labelling a review "first review" vs "re-review". No published token-cost comparison of whole-document vs scoped re-review. Nothing reputable quantifying verify-before-fix for prose/spec documents. UNVERIFIED vendor numbers: BugBot 70% resolution, Anthropic 16%->54%, CodeAnt ~60% FP cut.

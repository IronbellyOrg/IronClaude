# Research report 2 (owner-supplied, 2026-11-10): the three solutions to plan

Verbatim from the owner. Citation URLs and numbers below were NOT independently verified; treat them as UNVERIFIED leads.

## Part A: ranked solution table (excerpt, rows 1-3)

| # | Name | Mechanism | Source (URL, date) | Grade | Problems addressed | Refactor size | Compatibility risk |
|---|------|-----------|--------------------|-------|--------------------|---------------|--------------------|
| 1 | Independent heterogeneous reviewer panel + deterministic merge (no debate) | Two reviewers from different model families review the full document in separate contexts, never see each other; a Python script merges findings by fingerprint, keeps the union, marks overlaps as high-confidence. No cross-talk round. | Cross-model review experiment, arxiv.org/abs/2610.01471, Oct 2026 (56.7% vs 42.7% planted-fault detection at 2 calls, Holm p=.006; 41.2% Jaccard overlap between reviewers); practitioner case study via synapsesocial.com paper summary + r/ArtificialInteligence thread (47%->72% coverage, no single model above ~64% recall), 2026 | B | P1, P7 | 2-3 files: panel dispatch in coordinator command + merge subcommand (~2-3 d) | Doubles review tokens per round (2 reviewers). Mitigated: still below the old 1.25M/run baseline. Panel diversity alone does not restore independence (see row 10, Apple result). |
| 2 | Typed finding ledger with state machine + regression re-verification | Findings get stable ids and typed statuses (open/resolved/regressed/deferred) in a script-kept file. A finding may move to resolved only when the reviser names its id and the diff shows the offending text gone; any re-review that re-finds a resolved id marks it regressed and the verdict script fails closed. | pr-review-core changelog (docs.rs/crate/pr-review-core/0.30.0, 2026): content fingerprints with 3-line positional drift tolerance (0.28.1); "existing discussions cannot be resolved merely because another review misses their finding when the commit is unchanged" (0.30.0); Qodo pr-agent persistent_inline_comments fingerprints (docs.pr-agent.ai/tools/improve/, 2026); Gerrit copyCondition label semantics (gerrit-review.googlesource.com/Documentation/config-labels.html) | C (three independent implementations converged on the same mechanism) | P6, P7, P5, P4 | 2-3 files: extend the existing ledger script with statuses + verdict integration (~2-4 d) | Fingerprint drift when revisers reword: needs pr-review-core's positional fallback, else resolved rows are silently re-opened. Low risk otherwise; pure Python + markdown. |
| 3 | Mechanical pre-check suite (requirements lint before the LLM reads) | Deterministic Python pass that extracts ids, section references, counts, RFC-2119 keyword census, and named values into structured data, then checks: every referenced id exists; "all N"/"at least N" matches the enumerated row count; same named key never carries two different values. Runs before review 1 and after every fix; its output is evidence the reviewer must address. | BMW TRLC (github.com/bmw-software-engineering/trlc, active 2026): typed requirement language + user-defined consistency checks in CI; StrictDoc traceability (strictdoc.readthedocs.io); Doorstop link validation (github.com/doorstop-dev/doorstop) | C (practitioner, runnable code) | P1 (partially), P7, auditability; saves tokens | 2 files: new CLI subcommand + hook into the coordinator command (~2-3 d) | Nearly none: stdlib markdown parsing. Risk is over-linting clean docs (the over-blocking failure the original setup had); keep lint findings informational unless a deterministic contradiction is found. |

## Part B: design sketches

### 3.1 Independent reviewer panel + deterministic merge (designs 1 + 2 together)

Components and files:
- `src/superclaude/skills/sc-spec-panel-*/` coordinator step: dispatch two reviewer agents in parallel, one per model family (e.g. Sonnet-class + a different family via the existing agent plumbing). Prompt template is identical; neither sees the other's output or the transcript of the other's run.
- New CLI subcommand `superclaude review merge` (Python, deterministic): takes two machine-readable findings blocks (same schema the diffgate already parses), computes a fingerprint per finding (normalized quote + span + category), unions them, and emits one merged ledger with a `confidence: overlap` marker where both families found the same span.
- The existing finding ledger (already script-kept in this repo) gains typed statuses.

State machine (deterministic, script-enforced):
```
open --(reviser names id AND diff removes offending text)--> resolved_check
resolved_check --(next review finds fingerprint again)--> regressed  [verdict := FAIL]
resolved_check --(next review clean)--> resolved
open --(human defers)--> deferred
```
Only the script moves states. Reviewers propose findings; the reviser proposes a fix map; the script decides resolution. What is LLM-judged: finding content and whether a re-found span is "the same" defect is pre-empted by fingerprint matching (mechanical). What is deterministic: ids, statuses, verdict, review count, merge.

Migration path (loop keeps working at each step):
1. Add `review merge` subcommand with the current single reviewer as both inputs (no behavior change; exercises the code path).
2. Turn on the second-family reviewer; merge output replaces the single findings block. Verdict logic unchanged.
3. Add statuses/regressed to the ledger and the fail-closed regressed rule.
4. (Optional) route overlap-marked findings past the grader (two-family agreement is itself evidence); non-overlap findings still go through the blind grader.

Experiment vs current setup (same 57 KB document, >=6 replicates per arm):
- Arms: current single reviewer (control) vs panel+merge (treatment), 6 runs each, same seed document variants where applicable.
- Primary metric: residual blocking defects found by the independent whole-document audit (the P1 number, currently 1-3 in 10 of 12 runs).
- Secondary: total output tokens; reviews to converge; overlap rate (union size vs intersection size tells you whether the second family is buying coverage or copies).
- Success criterion: median residual blockers 0 with lower quartile 0 in treatment, at token cost <= 2x current (still well under the 1.25M original baseline). Pre-register the 2x bound so a token blowup fails the experiment honestly.

### 3.2 Mechanical pre-check suite (design 3 + 11)

Components and files:
- `superclaude review lint <doc>` (Python, stdlib only): parses the markdown into sections; extracts (a) every defined id, (b) every cross-reference "section N / id X", (c) enumerated row counts vs stated totals ("all N items", "at least N"), (d) acceptance-criteria lines, (e) path-template rules and per-item path rows, (f) RFC-2119 keyword census per section.
- Checks: dangling references; count mismatches; the same key bound to two values in different sections (string equality on extracted key-value pairs, reported as "possible contradiction, verify"); path-template vs per-item fnmatch collision; acceptance criterion that references a nonexistent id or threshold.
- Output: JSON + a markdown evidence block injected into the reviewer prompt and the reviser fix map.

What is deterministic: everything above. What is LLM-judged: only whether a flagged "possible contradiction" is a real semantic conflict (the reviewer must address each lint finding by id, same as blocking findings).

Migration path:
1. Ship the lint as informational (emitted alongside the review; reviewers must acknowledge each finding but lint alone never blocks). Zero risk to convergence stats.
2. Promote two checks to blocking after measuring their false-positive rate on the 12 clean final documents from the prior experiment: dangling references and count mismatches (both are near-pure syntax facts).
3. Add the contradiction key-value check as blocking only if its FP rate on clean docs is 0 in the 12-doc validation set.

Experiment: run the lint on the 12 final documents from the previous experiment and on the 3 originals. Report: how many of the audited residual defects (contradictions, impossible acceptance checks, path collisions) each check flags, plus FP count on clean docs. This is a measurement experiment first (no agent runs needed for step 1), then a 6-replicate loop run with blocking lint to measure token savings (fewer LLM rounds spent rediscovering mechanical facts).

(Owner note for the planner: "12 clean final documents" and "3 originals" are loose wording. The final specs from Stage 2 are NOT clean (they carry residual blockers) and only ONE original S1 spec exists plus the reference snapshots; reconcile against what actually exists on disk.)

## Part C: Rank 1 of a second ranked list: capture-recapture stop rule

### Rank 1. Capture-recapture defect-remaining estimation as a principled stop rule, over a multi-reviewer defect ledger

**Mechanism.** Run k independent reviewers over the same candidate document. Deduplicate their findings into one defect ledger (each entry: location + claim + evidence). The overlap pattern between reviewers estimates the total defect population, including unfound defects: Lincoln-Petersen from two lists, Chao2/sample-coverage or Mh-Jackknife from k lists. Stop reviewing when estimated remaining defects is indistinguishable from zero (CI), not at a fixed cap of 3. The same data yields per-reviewer detection estimates.

**Sources.**
- Eick et al. 1993, first capture-recapture for design inspections (via Wohlin et al. 2001 evaluation PDF): recommends Mh models with Jackknife estimator because defects have unequal detection probabilities.
- Runeson/Wohlin/Brantestam 1995: estimates tend to UNDERestimate residual faults; correction proposed.
- Liu, Rong, Zhang, Qi: systematic literature review of capture-recapture adoption in SE: most work is evaluation; real application experience scarce.
- Chao 1984 (Chao1/Chao2) + scikit-bio implementation.
- LLM-side transfer evidence (the union part): MDPI case study 2026, "Iterative Audit Convergence in LLM-Managed Multi-Agent Systems": four-vendor panel union detected all 5 seeded defects; single vendors missed vendor-specific ones (grade B). Reddit r/LLMDevs independent study (self-published, grade C): single model caught ~34%, four-model panel ~89%; median pairwise Jaccard overlap ~0.37.

**Evidence grade: A** for the estimator in human inspection; **B/C** for LLM reviewers as the "inspectors" (no published capture-recapture-on-LLM-findings study found).

**What it changes in our architecture.** State: a script-kept defect ledger keyed by location + normalized claim (we already have a ledger skill; extend it). Control flow: the verdict/stop rule becomes computed from overlap statistics instead of review count. Reviewers: 2-3 independent first-pass reviewers (different model families, or at minimum different prompts/temperature) instead of 1 + scoped re-reviews. Tooling: a small Python estimator (scikit-bio or 50 lines).

**What it would fix.** The core residual problem: 1-3 blocking defects in 10/12 finals despite convergence, with different runs catching different subsets. It also replaces the arbitrary cap-of-3 with a rule tied to evidence.

**What it would NOT fix.** Correlated blindness: same-family reviewers that all miss the same defect look "converged" to any overlap estimator (Kim et al. 2025, arxiv 2506.07962: substantial correlated errors across 350+ LLMs). Mitigate with cross-family reviewers. Also does not fix the reviser.

**Cost/risk.** 2-3x first-review tokens plus a dedupe step (LLM-assisted dedupe needs verification against quotes). Risks: underestimation (use Mh-Jackknife, report CIs, never a point estimate) and false positives inflating the estimate.

**Cheapest falsifying experiment on the 57 KB doc.** We already have the data: take the 12 converged runs' first-review finding sets plus the independent audits' confirmed blocking defects. Compute Lincoln-Petersen and Chao2 on reviewer pairs. If the estimators' "remaining defects" predictions are uncorrelated with the audits' actual 1-3 residual blockers, the approach is falsified for our setting - no new LLM run needed. One afternoon, zero marginal tokens.

## Part D: owner notes on the multi-model strategy (these apply to the FINAL, post-test version)

- Only Anthropic models exist in THIS environment; live environments have many more. The multi-family strategy must be designed for the live case: each review panel = 2x Tier 3 + 1x Tier 2 + 1x Tier 1b models, run as parallel independent reviewers.
- The panel composition must be easy to manage through a TEMPLATE. The 2x Tier 3 and the 1x Tier 2 slots need not hold the same model each time: either randomized from a pool, or set centrally so updates roll out via the template. The Tier 1b slot holds the SAME model every time (the fixed anchor).
- This lets us benchmark every available model and build a pseudo-eval framework that continuously scores models on many factors and tracks performance.
- The tokens are already being spent scoring; capture that data together with task variables (language, complexity, size, specialization) and push it to the git repo to be gathered into a central database so the best models for a job can be chosen ahead of time from the task variables.

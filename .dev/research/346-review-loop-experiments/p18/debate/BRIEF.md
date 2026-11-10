# Debate brief: which 3 Jev integrations best complement the "ab5" review-loop variant?

SP = /tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad  (all paths below are under it)

## What ab5 is
ab5 = ab4 + the PN1 panel. The loop reviews a spec (spec-panel command) and revises it, max 3 reviews / 2 fix cycles, then two frozen independent audits measure the final spec.
- **ab4** (p16/ab4, READY.md): PN2 mechanical lint pre-pass (lint-N.md given to reviewers), k=2 first reviews (R1b adds an acceptance-criteria sweep sentence), deterministic merge, a CLEANED single-pass verifier (VF) over merged findings, revise (V), scoped re-reviews R2/R3 with lint.
- **PN1 panel** (p13/ab1): instead of 2 first reviews, 4 independent first reviewers on different model tiers (R1.t1b, R1.t2, R1.t3-1, R1.t3-2; Fable/Sonnet/Haiku mix), deterministic merge, a cheap adjudication step (ADJ), typed finding ledger.
- ab5 = ab4's pipeline with the PN1 panel as the first-review stage (panel -> merge -> ADJ -> clean VF -> revise -> scoped re-reviews with lint). Being built now; do not assume it exists.

## Measured evidence (read these files)
- `p17/LEDGER-RESULTS.md` and `p17/score/perdefect.md`: ledger of 44 real spec defects (20 blocking). Fixed per final spec / blocking defects left of 20: baseline 2.8 / 17.3; ab4 6.3 / 14.3; ab3 6.8 / 13.8; ab1 6.0 / 14.3; PN1 15.7 / 10.0 (7.6x baseline tokens: ~408k, of which the 4-reviewer first-review panel is roughly 340k and revise+re-reviews roughly 70-100k); PN2 lint alone and ab2 verify-gate alone: no effect.
- The main finding: **reviewers raise the defects but the revise step leaves most of them unresolved** (baseline fixes ~6% of ledger defects; even PN1 leaves half the blocking ones). Defects that survive in almost every arm: P1 scope/AC-1.1 (D01,D02,D04), contract-path defects (D06-D10), AC-0.4 step-3 (D11,D12). Introduced-defect hits are 0.3-1.3 per spec in every arm. Fix-by-deletion is rare (0-2 per arm).
- Loop-only tokens (output tokens, per run): baseline 53.6k, ab4 106.5k, PN1 ~408k (complete runs), PN2 47k.

## What Jev is (p15/RESEARCH-REPORT-3.md, read it)
Jev = TypeSafe System One model: answers TYPED questions (Choice / Noul yes-probability / Score) with probabilities over STATE THAT OUR CODE SUPPLIES. It cannot generate findings, rationales, patches or evidence. $0.042/M input tokens, output free; ~200 ms per call. Hard rules: Jev never writes PASS or ledger state, never suppresses uncertain findings, never demotes CRITICAL/FR-8/FR-9, any missing/adverse/uncertain answer falls back to the conventional LLM path; an extra review slot is never added (3 reviews / 2 fixes stays).
The five integrations (full designs in p15/plans/PLAN-*.md; shared rules p15/plans/SHARED-CONTRACT.md; critique p15/plans/REVIEW-OF-SOLUTIONS.md):
- **E1** real fix vs deleted obligation: inside the scoped re-review, Jev judges separately {defect removed?, accepted obligation preserved?, dependency conflict?}; a fix closes only if code checks pass AND Jev says removed+preserved+no conflict; else conventional verification.
- **E2** first-review pair priorities: code extracts related passage pairs; Jev ranks/labels pairs as reading priorities (12 pairs, <=1,200 tokens) given to first reviewers as UNVERIFIED hints; whole document still read.
- **E3** confirmation-only finding screen: after first-review findings, Jev may CONFIRM a finding (relation conflict + consequence supported) so the conventional verifier can be skipped; every non-confirmation goes to the conventional verifier.
- **E4** selective fix-verifier replacement end-to-end: depends on E1; Jev replaces eligible narrow per-finding re-review checks with conventional fallback on uncertainty.
- **E5** evidence-sufficiency routing: at a provisional PASS decide whether more assurance is needed; shadow only; needs a scope amendment for live.

## Offline gate results already obtained (our environment, real Jev calls; read the results.json / offline-results.md)
- E1: smoke gate (40 cases) -> NO-GO-OFFLINE (p15/e1/results.json, p15/e1/offline-results.md). E4 is blocked behind E1.
- E2: Stage 0 headroom falsifier passed (static priorities do NOT already cover must-read relations); Stage 1 replay not run (p15/e2/results.json, p15/e2/PREFILTER-REVISION.md).
- E3: falsifier -> NO-GO-OFFLINE: automation 0.179 (10/56) just under the 0.20 minimum (p15/e3/results.json).
- E5: zero-call headroom absent -> NO-GO-OFFLINE.
- Central table: central/MATRIX.md. Jev adapter code: p15/jev/jevlib; live key is available to the coordinator only.
Treat these gate results as evidence, but note they were measured against the OLD single-reviewer loop and the audit-based metric; ab5 changes the context (4 panel reviewers, lint, clean verifier). Say whether each gate result still applies.

## Constraints on the variant (ab6 = ab5 + three Jev integrations)
Cap-neutral (no 4th review, no 3rd fix); owner decision D6 (cost never kills a run); Jev calls made by harness code run by the coordinator, never by worker agents; every integration must have a conservative fallback to the existing path; measurement = the 44-defect ledger with n=6 Sonnet runs (sd of residual blocking ~2 per spec; effect of ~3 detectable), plus loop tokens.

## Criteria for a good choice
1. Which ledger defects / failure modes it addresses (be specific: ids, or the mechanism by which reviewers-raise-but-reviser-doesn't-fix is improved).
2. Complementarity with ab5's existing parts (panel diversity, lint, AC sweep, clean VF, scoped re-review) - not redundancy with them.
3. Net token effect on ab5 (savings or additions), including Jev dollars (negligible).
4. Risk: false closure, hidden blockers, added failure modes; and whether the existing offline gate result kills it.
5. Measurability with six runs and the ledger.

---
## ADDENDUM (owner input received after round 1 started): ROI stress test
The owner supplied a separate research document, saved at `p18/debate/ROI-STRESS-TEST.md` (READ IT). It stress-tests Jev on 23 candidates (R-001..R-023) for six other commands. Its decision standard now governs this debate: fully loaded cost at matched quality; charged conventional/static CONTROLS compete (including "no-model is not free"); headroom must be shown by independently relabelling natural cases; joint confusion counts, not marginal accuracy; a prefilter that drops pairs makes those misses Jev's; never reuse a model judgment as audit truth; outputs start non-controlling/flag-only; dangerous false passes disqualify; "integrate nothing now" is its own recommendation for the live commands, and replay/shadow comes first. The owner nevertheless wants to investigate and TRY integrations in our loop, so the right reading is: design ab6 so that each Jev seam is non-controlling or conservatively falling back, compare against a charged conventional control, and establish headroom offline on data we already have (70 final specs, 140 frozen audits, ~500 labeled findings, the 44-defect ledger with per-spec statuses in p17/score/out/*.json, and the arm-to-spec key p17/score/key.json).

**The candidate pool is therefore widened from E1-E5 to eight**, adding three seams adapted from the ROI document to our spec-review loop (they are inspired by R-008/R-019, R-009 and R-015 respectively):
- **A1 obligation-to-criterion support (from R-008/R-019):** code extracts spec obligations (requirement/WC rows, section-3 per-command rows) and acceptance criteria / phase gates (AC-n, phase Commands cells, live-check steps); the prefilter pairs them (IDs, names, phase tokens); Jev labels each candidate pair {supported, partial, unsupported, contradicts-or-defers, insufficient} over the supplied text only. Output = flag-only hints given to the reviser and to the scoped re-review; never a finding or a closure. Conventional control: the ID/keyword prefilter alone (and PN2-style mechanical lint). Adverse case: IDs match while the criterion defers or negates the obligation.
- **A2 acceptance-check observability (from R-009, lint-first):** the PN2 mechanical lint stays as the conventional control; Jev judges only the lint-clean residual acceptance checks / live-check steps {can pass as written, cannot pass, cannot discriminate, insufficient}. A strong competing control is simply EXECUTING the shell/grep/YAML commands in a scratch directory (the ledger scorers did this to confirm several defects). Adverse case: a check that looks observable but targets the wrong thing.
- **A3 revision novelty (from R-015):** at the second fix, Jev judges whether the proposed revision for a blocker that survived the first fix is substantively different from the first attempt {new approach, same approach restated, no relevant change, insufficient}; code supplies both diffs. Output = a hint appended to the V2 reviser brief (flag-only; the fix cap of 2 is unchanged). Conventional control: touched-line-set/diff-hash comparison. This targets the measured bottleneck that reviewers raise defects but the reviser leaves them.

Every advocate and judge must treat the ROI document's standard as binding when scoring ANY of the eight, including E1-E5 (their round-1 papers were written before this standard was known; re-evaluate them under it).

---
## ADDENDUM 2 (owner question, measured after round 1): token LANES in the PN1 panel
The panel's 408k loop tokens are NOT all primary-model tokens. From the complete PN1 runs b1-r4..r6 (p13/ab1/tokens_models.json, produced by p17/tokens_models.py), mean output tokens per run:
- primary lane (Sonnet 5.5: R1.t1b reviewer, V1, V2, R2, R3): **106,357** (1.98x the fresh baseline's 53,623; about the same as ab4's 106.5k)
- parallel Tier-2/3 lane (R1.t2-1, R1.t3-1, R1.t3-2; Haiku 5.5 STAND-INS for what are Tier 2 and Tier 3 models, possibly other providers, in the live environment): **290,600** (71%)
- adjudicator lane (ADJ, Fable 5.2): **11,359** (3%)
Caveats: the Haiku stand-ins wrote 68k-108k tokens each against 23k for the Sonnet reviewer, so live Tier 2/3 volume is unknown; those models are not free (MODEL-TIERS.md prices; only subscription models like Muse Wonder have no marginal price); Fable is Tier 0 premium ($50/M output) so the 11k adjudicator tokens cost roughly half of what the 106k Sonnet tokens cost; input tokens are not counted anywhere. Judges and advocates: evaluate every seam's token effect per lane (primary / parallel / adjudicator), and treat savings or additions on the primary lane and the adjudicator as the costs that matter most. Measured ledger efficiency per 100k extra PRIMARY-lane tokens vs baseline: PN1 about 24 fixes (12.9 extra fixes for 52.7k), ab4 about 6.6.

---
## ADDENDUM 3 (HARD OWNER RULE): model ceiling
Fable (Tier 0) is STRICTLY FORBIDDEN in all our pipelines. Opus 5.5 (Tier 1a) is the highest tier allowed and is to be used sparingly or not at all. Consequences for the debate: (a) any design that puts a step on Fable or Tier 0 is invalid; (b) PN1's historical runs used a Fable adjudicator (ADJ) - that is a forbidden condition, so PN1's measured gain (15.7 fixed, 10.0 blocking left) may partly depend on it; ab5 will run ADJ on Sonnet and so tests whether the gain holds without Fable; (c) do not propose seams that need a stronger-than-Sonnet reviser or judge; Opus only where a seam's value clearly requires it, and say so explicitly.

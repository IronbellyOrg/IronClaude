# Owner decisions addendum (2026-11-10). Binding on every plan in p12/plans and p13/plans.

Scratch root: $SP = /tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad

## D1. Noise band: keep as planned
Adopt only on a clear win, drop only on a clear non-win, and run more replicates for anything in between. Concretely, keep each plan's existing three zones (ADOPT / INCONCLUSIVE / DROP) and numeric thresholds unchanged.

## D2. Cost convention: pass/fail on LOOP ONLY, report loop+audit alongside
- All token pass/fail rules use A = LOOP-ONLY output tokens: every review, revise, panel, merge, verify, gate and adjudication worker of the loop, EXCLUDING the frozen AUD audits (they are measurement instrumentation, not part of the process).
- Also compute and REPORT B = loop + one audit next to A in every results table, but B never decides pass/fail.
- Tokens are always counted with each message id counted ONCE (a transcript logs a message once per content block; summing lines double-counts). Use the same dedupe method as $SP/p11 recount: sum over unique message ids of the max output_tokens.
- Baseline (Stage 2 arm 3, n=6, mean per replicate): loop A_BASE = 100,424; one audit = 69,044; B_BASE = 169,468.
- Express every cost rule as a ratio to A_BASE (R_LOOP = test loop tokens / 100,424) and also print R_B (= test loop+one audit / 169,468). Any existing threshold written against a loop+audit baseline (B_TOK ~169,000, 381,702 etc.) must be re-based to loop-only: the numeric ratio limits themselves (for example "<= 2.0x") stay, but now apply to R_LOOP. Predicted ratios in the plans (for example ~1.7x for k=3, ~1.65x for the final gate, ~1.9 for the panel) were loop-based already or must be recomputed on a loop-only basis; recompute them from the deduplicated figures.

## D3. Haiku robustness stratum (secondary, never pooled)
- The decision-maker is unchanged: Sonnet, n=6 replicates per test arm, each final spec audited twice by the frozen Sonnet audit, compared against the Stage 2 arm-3 baseline.
- Add a Haiku STRATUM: the loop workers (re-reviewers, revisers, verifiers, gate reviewers, adjudicators, and any non-panel reviewer) run on Haiku 5.5 (Agent model value `haiku`). The AUD audits ALWAYS stay on Sonnet (frozen instrument, 2 audits per final spec). For panel designs the panel composition from the template does not change (anchor sonnet + haiku stand-ins); only the non-panel loop workers drop to Haiku; document the exact meaning in your plan.
- n = 4 Haiku replicates per test arm. A SHARED Haiku baseline (Stage 2 arm-3 design with Haiku loop workers, n=6) is produced by the coordinator at $SP/p14/haiku-baseline/ (results.json: per run verdicts, reviews, growth, loop tokens, two-audit blocking counts); consume it, do not run your own.
- Haiku is judged on RELATIVE reduction versus the Haiku baseline (ratio of mean audit blockers, test/baseline), not on absolute counts, because its baseline will be worse.
- ADOPT additionally requires the Haiku stratum to point the same direction (relative reduction > 0 and no inflated harness-failure rate); Haiku is never pooled into the Sonnet number. A missing or not-yet-run Haiku stratum makes an otherwise clear Sonnet ADOPT read "ADOPT (Haiku robustness pending)".
- Tag every run record and telemetry record with `stratum: "sonnet" | "haiku"`.

## D4. Adaptive extension for INCONCLUSIVE
If the Sonnet n=6 result lands in the INCONCLUSIVE band, add 3 more Sonnet replicates for that design only (once), recompute with n=9, and then decide. If still INCONCLUSIVE, the final verdict is INCONCLUSIVE; do not extend a second time without the owner.

## D5. Private clones accepted
Each implementer works in its own full git clone under $SP; no git worktree and no Orca in this environment.

## What this changes in your deliverables
- Decision-rule constants live in a data/config file, not scattered in code; the convention (loop-only A with B reported) is implemented once in the analysis script and tested.
- The READY report lists which of your files encode D2 (token convention), D3 (stratum tag) and D4 (extension rule).
- Live-phase launch tooling accepts a stratum parameter (sonnet default, haiku optional) and never uses Haiku for AUD.

## D6. Cost limits scaled to the loop-only convention; cost NEVER kills a run (owner, 2026-11-10)
1. SCALE THE LIMITS. Every cost limit that a plan (or the research report) stated against total tokens (loop + audit, i.e. a limit L on R_B) is converted to an equivalent loop-only limit with:
   R_LOOP_limit = (L x 169,468 - 69,044) / 100,424
   (169,468 = B_BASE; 69,044 = one audit; 100,424 = A_BASE). Resulting limits: L=1.8 -> 2.35; L=2.0 -> 2.69; L=1.25 -> 1.42; L=1.5 -> 1.84; L=1.65 -> 2.10. Round to two decimals, store them in the decision constants file (data, not code), and keep the formula and the original L beside each constant as a comment. The original numeric limits no longer apply to R_LOOP. Cost is still judged on R_LOOP (loop only) with R_B reported alongside, never deciding.
2. NO MID-RUN COST KILL. No loop, replicate, wave or experiment may be stopped, aborted, truncated, skipped or short-circuited because of token or dollar cost while it is running. Delete or disable any rule, script check or plan sentence of the form "abort/stop/halt if running tokens exceed X", "skip remaining replicates if cost is high", or a token-based early exit inside a loop. Cost is evaluated ONLY after a run has completed (and a design's cost verdict only after its whole replicate set has completed), and it enters the final verdict as a post-hoc cost clause. Loop caps that are not cost caps (max reviews, max fix cycles, stall detection, hard review ceilings) are unaffected.
3. The cost clause in each design's decision rule remains (a design can still be judged too expensive after its data are in), but it can only change the verdict at the end; it can never remove data collection.
4. The planner-estimated token totals and worker counts in the plans are forecasts for scheduling only; they are not limits.

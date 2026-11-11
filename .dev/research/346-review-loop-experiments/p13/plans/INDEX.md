# INDEX: Stage 3 plans (research report 2: S1, S2, S3)

All paths under `$SP = /tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad`. Token figures are output tokens counted with each message id once (C9.1); `B_TOK` ~169,000 per replicate (Stage 2 arm 3, loop + one audit).

| Plan | Branch | Clone dir | Experiment dir | Implementer | Live workers (if gated in) | Live output tokens (est.) |
|---|---|---|---|---|---|---|
| `PLAN-1-panel-merge-ledger.md` (S1 panel + merge + ledger + template + telemetry) | `346Claude-pn1-panel-merge-ledger` | `$SP/p13/clones/pn1` | `$SP/p13/ab1` | 1 Sonnet (offline replay itself) | 54-60 (6 runs x 9-11: 1 sonnet + 3 haiku R1, ADJ fable, sonnet V/R2/AUD/AUD2) | ~2.5M (~0.42M/run; `R_TOK` ~1.9) |
| `PLAN-2-mechanical-lint.md` (S2 lint) | `346Claude-pn2-mechanical-lint` | `$SP/p13/clones/pn2` | `$SP/p13/ab2` | 1 Sonnet (full offline measurement itself) | 30-36, only if gate G1 holds | ~1.5M (~0.25M/run) |
| `PLAN-3-capture-recapture.md` (S3 estimator, catalog, falsification) | `346Claude-pn3-capture-recapture` | `$SP/p13/clones/pn3` | `$SP/p13/ab3` | 1 Sonnet (catalog + F1/F2 itself; shadow on PN1 data free) | 0 by default; ~84 only if F1 SUPPORTED and shadow CALIBRATED | 0 / ~3.8M |

Other files: `REVIEW-OF-SOLUTIONS.md` (critique, decisions, threats), `SHARED-CONTRACT.md` (frozen interfaces; embedded verbatim in each plan). Shared output: `$SP/p13/catalog/catalog.json` (built by PN3 Phase O1).

Recommended order: start all three implementers in parallel (they write disjoint files; each stops with a READY report). PN3's catalog should be finished before PN1/PN2 run their final analyses (both fall back to theme-level truth if it is missing). Launch PN1's live phase first; then run PN3's shadow analysis on it; launch PN2 live only if its G1 passed; launch PN3's live arm only if its gate passed. Never more than 6 concurrent workers per plan.

## Open questions for the owner

Tier definitions: resolved by the owner on 2026-11-10 (aliases and lists in C2; anchor sonnet; haiku stand-ins for Tier 2 and Tier 3 in this environment). No tier question remains open.

1. **Dispatch for non-Anthropic models.** The `gateway` environment has an empty `launch` map: how should a coordinator start a reviewer on `gpt-6.1-terra`, `glm-5.3` and so on (Agent tool model value, the `claude-gw-tier*[1m]` aliases with failover, an agent file per model, or the `sc-bare-review` proxy)? The template resolves models today; launching them is undefined.
2. **Panel on re-reviews in production.** The default template sets `apply_to: ["first"]` (cost; scoped re-reviews are not capture occasions). Should production re-reviews also use the panel?
3. **Model ids.** The template uses the MODEL-TIERS.md gateway ids for your model names (for example `Qwen3.8-max`, `muse-wonder-full-1.0`); confirm them. `claude-haiku-5-5` was observed in this environment's transcripts; the `fable` id (`claude-fable-5-1`) and its Agent value were not observed (PN1's adjudicator falls back to opus).
4. **Telemetry location for other projects.** Records go to `.dev/benchmarks/review-telemetry/` of the project being reviewed. Is that right for projects outside IronClaude, or should they be pushed to one central repo?
5. **Adoption bars.** S1 ADOPT needs a halving of audit blockers (1.50 to 0.75) and `R_TOK <= 2.0`; the baseline decomposition (REVIEW section 1) suggests a panel alone cannot reach this. Do you accept INCONCLUSIVE as the likely outcome, or want a looser bar set now (before data)?

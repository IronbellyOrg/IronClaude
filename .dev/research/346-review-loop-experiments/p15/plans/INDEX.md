# INDEX: p15 Jev experiments E1-E5 (research report 3)

All paths under `$SP = /tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad`. Binding for all plans: `SHARED-CONTRACT.md` (J0-J12) and owner decisions D1-D6 (`$SP/p14/DECISIONS-ADDENDUM.md`). Other files: `REVIEW-OF-SOLUTIONS.md` (critique, threats, dependencies, kill criteria), `SKILL-ASSESSMENT.md` (typesafe-ai skill mapped to tasks). Token figures are output tokens counted once per message id; `R_LOOP = loop / 100,424` decides cost, `R_B = (loop + one audit) / 169,468` is reported only; worker and token figures are scheduling forecasts, never limits (D6). Every outcome, including NO-GO and BLOCKED, writes `<exp>/results.json` and updates `$SP/central/MATRIX.md` (built by PLAN-0) next to the p12/p13/p14 designs.

| Plan | Branch | Clone | Experiment dir | Offline cost (Jev / offline workers) | Live workers per stratum (if gated in) | Sequence / gates |
|---|---|---|---|---|---|---|
| `PLAN-0-central-matrix-and-jev-adapter.md` | `346Claude-jev-0-shared` | `$SP/p15/clones/jev0` | `$SP/p15/jev`, `$SP/central` | probe 3 calls (< $0.001; ceiling $0.10) / 0 | none | FIRST. 1 Sonnet implementer; then the coordinator runs `probe.py --live` (model id + validator check) |
| `PLAN-E1E4-fix-closure.md` (E1 + E4) | `346Claude-jev-e1e4-fix-closure` | `$SP/p15/clones/jev14` | `$SP/p15/e1`, `$SP/p15/e4` | smoke: 40 calls (< $0.01) / 12-14; full replay: ~320 calls (< $0.05) / ~100. Ceiling $5 | E4: Sonnet ~100 (12 runs: `f4b`, `f4c` x 6); Haiku ~68 (8 runs); D4 ext ~50 | smoke (stop on ANY false auto-closure) -> session 2 -> calibration/held-out -> GO-E4 -> session 3 -> E4 live |
| `PLAN-E2-priority-hints.md` | `346Claude-jev-e2-priority-hints` | `$SP/p15/clones/jev2` | `$SP/p15/e2` | Stage 0: 0 calls / ~7; Stage 1: ~40k pair calls (~$0.7) / ~210. Ceiling $5 / 30M tokens | Sonnet ~126 (18 runs: `h2j`, `h2s`, `h2r` x 6); Haiku ~84 (12 runs); D4 ext ~63 | Stage 0 headroom (no paid calls; H = 0 -> NO-GO) -> replay (Jev >= static + 8 of 160) -> live |
| `PLAN-E3-confirmation-screen.md` | `346Claude-jev-e3-confirmation-screen` | `$SP/p15/clones/jev3` | `$SP/p15/e3` | falsifier: ~100 calls (< $0.02) / ~35. Ceiling $5 | Sonnet ~84 (12 runs: `g3b`, `g3c` x 6) + ADJ-H 0-10; Haiku ~56 (8 runs); D4 ext ~42 | falsifier 60 + 40 (safety, automation >= 20%, perturbation tolerances) -> session 2 -> live |
| `PLAN-E5-assurance-headroom.md` | `346Claude-jev-e5-assurance-headroom` | `$SP/p15/clones/jev5` | `$SP/p15/e5` | zero-call: 0 / 0 (probe only if headroom: 96 calls / ~7) | none: live BLOCKED without an owner cap-neutral amendment | zero-call headroom (predicted NO-GO-OFFLINE) -> probe -> replay -> (owner) live |

Implementer agents: one Sonnet implementer per session (PLAN-0: 1; E1E4: up to 3 gated sessions; E2: up to 3; E3: up to 2; E5: 1, second only on headroom). Implementers never hold the Jev key and never call the live API; every `--live` command and every Jev J step is run by the coordinator through `bash -c 'set -a; . "$SP/.jev.env"; set +a; ...'` or `$SP/p15/drive-jev.sh <dir>`; `keyscan.py` after every paid phase. Clones are private full clones of `https://github.com/IronbellyOrg/IronClaude`, branched from `origin/master`; no worktree, no Orca, no PR; push to `origin` only. Each experiment is capped at 6 concurrent workers in every phase (offline and live, both strata together).

Expected outcomes (planner forecast): E5 NO-GO-OFFLINE (static "use the remaining slot" dominates at a ~90% residual base rate); E2 NO-GO-OFFLINE or small headroom at Stage 0 (historical themes are lexically linked); E1 open (strict zero-false-closure gates); E4 INCONCLUSIVE at best on cost (the report's 20% total-loop saving vs C is out of reach when only checker work differs); E3 the most likely to reach live, with a small effect.

## Recommended queue for the 20-slot scheduler (~19 slots busy with older experiments)

1. **Now (1 free slot):** PLAN-0 implementer.
2. **Next free slot (may run alongside PLAN-0):** E5 session 1 (zero calls, zero workers; it writes `results.json` directly if PLAN-0 is not ready, and rebuilds the matrix later). Lands a matrix row cheaply.
3. **After PLAN-0 READY:** coordinator runs `probe.py --live` (seconds). If `model_ok` and `validator_ok`: start E1 session 1 and E3 session 1 (1 slot each, in that order as slots free), then E2 session 1 (Stage 0). If the probe fails, stop all paid phases and ask the owner.
4. **Offline worker phases** (labelers, adjudicators, conventional replays): E1 smoke (12-14 workers), E3 falsifier (~35), E2 Stage 0 (~7). Run at most 3 concurrent per experiment while the older experiments hold most slots (contract cap 6); E5 needs none.
5. **Live phases, in this order as gates pass and slots free:** E3 live (8 Sonnet-stratum + Haiku waves, ~140 workers), then E1 full replay offline (~100 workers, can interleave with E3 live), then E4 live (only after GO-E4, ~170 workers), then E2 replay (~210 offline workers) and E2 live (~210 workers) only if their gates pass. D4 extensions only after an INCONCLUSIVE Sonnet n=6.
6. While older experiments still occupy ~19 slots, keep the p15 total at or below 6 concurrent workers across all experiments; raise to 6 per experiment as slots free.

## Jev money (the only real dollars)

Ceilings, enforced by pre-flight reservations (an offline phase that does not fit refuses to start; a live J step that cannot draw falls back to the conventional path, the run continues): $5 offline + $1 live per experiment, $0.10 for the PLAN-0 probe; maximum $24.10 in total; forecast spend under $1. Only the owner raises a ceiling. Price verified on the live models page: $0.042 per million input tokens, output free.

## Open questions for the owner

1. E4's pre-registered ADOPT needs a >= 20% median loop saving vs the matched conventional checker; with loop-only accounting B can save only ~5-8%. Keep it (expect INCONCLUSIVE) or switch to a narrow-stage saving criterion before E4 data exist?
2. Jev ceilings $5 offline + $1 live per experiment (max ~$24 total): approve, or set others?
3. Arm A is not re-run (drift risk since 2026-11-10 02:05 UTC). Add 2 shared fresh baseline replicates (~0.34M tokens) as a drift check for all p15 comparisons?
4. E3: the report's larger 200/300 calibration pilot is deferred (a false confirmation reproduces baseline behavior). Require it before E3 live?
5. E5 live needs your explicit cap-neutral scope amendment (one remaining slot for assurance, no review 4); only relevant if headroom and replay pass.

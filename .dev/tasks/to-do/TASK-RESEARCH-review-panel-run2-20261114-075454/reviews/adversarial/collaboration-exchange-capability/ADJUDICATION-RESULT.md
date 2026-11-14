# Adjudication result: slot C-12 (collaboration-exchange-capability)

Run: `/sc:adversarial --compare proposal-a.md,proposal-b.md --depth standard --focus correctness,risk,test-coverage` (Mode A, no `--merge` flag). Conflict row: C-12 in `phase-outputs/discovery/undecidable-conflicts.md`. Status: ADJUDICATED. Return contract: status `partial`, convergence score 0.96, base Variant A.

## Winner

**A named hybrid that the debate itself produced: a staged resolution on the Proposal A base** (Variant A = Proposal A is the selected base; Proposal B's transport design is incorporated as binding preconditions, not as code).

The debate's own base selection (`adversarial/base-selection.md`):

| Variant | Quant (mean of two passes) | Qual (after re-evaluation) | Combined |
|---|---|---|---|
| A (Proposal A) | 0.9729 | 26/30 = 0.8667 | **0.9198** |
| B (Proposal B) | 0.9493 | 24/30 = 0.8000 | **0.8747** |

Margin 4.51%, below the 5% threshold, so the tiebreaker applied. Level 1 (debate performance): Variant A won 12 diff points, Variant B 5 (Merge 2, Tie 2, Unresolved 1); level 1 decided for Variant A. Level 2 (correctness criteria MET) would have favoured Variant B (3 vs 2) but was not reached. Position-bias passes: 8 of 60 criterion pairs disagreed and were re-evaluated; pass 1 alone gave a 7.97% margin and pass 2 alone 4.38%, both favouring A. Edge-case floor: A 5/5, B 5/5.

## Rationale (as the debate concluded)

- The evidence does not support building the exchange transport now. At HEAD the gateway launch map is empty (`review-tiers.default.json:25-29`, `"launch": {}`), `--settings` appears nowhere in `src/superclaude/**/*.py`, no family that Proposal B would ship has a clean measured success, and an unregistered per-session hook has no recurring exerciser (`hook_latency_drift.yaml` is bound to `hooks.json`). Advocate B conceded the build-now question in Round 2.
- Proposal A's gate ("not built until an exchange arm beats the kit") was also wrong as written: ownerless, and it conflated building the measuring instrument with enabling the capability (Advocate A conceded this). The debate's product is therefore a staged form of Proposal A, not Proposal A unchanged.
- Points where the debate favoured Proposal B and which the merged position keeps: C-010 (B 79%: validator table, forbidden keys, 600-byte cap, located-anchor and untrusted-anchor analysis), X-002 (B 82%: `--resume` on gateway ids is recorded at the pinned tip), X-004 (B 62%: recorded 57 to 85 ms fits the 0.1 s budget, small sample), X-005 (B 58%), C-008 (B 57%), and the merge points C-006 and C-007.
- Scoring-matrix result: A 12, B 5, Merge 2, Tie 2, Unresolved 1 (C-002, open only on its label: A 52 vs "Merge 62"), three shared assumptions (A-001, A-002, A-003) answered QUALIFY by both advocates. Convergence 24 of 25 diff points = 96% against a threshold of 80%; the invariant gate nevertheless blocks a CONVERGED status (BLOCKED_BY_INVARIANTS).

## Conditions under which the winner holds

1. Core now: H1, H2, H3, H4 principle, a per-module catalogue ("static kit") with `kit: off` by default for every module until the cost per panel at n of at least 4 and a hold-out of at least 4 unseen defects pass. No hook script, `_FRESHNESS_SCRIPTS` entry, launch adapter, board, validator code or `collab` record is built now.
2. Build trigger (all three): slot C-07 adjudicated to a launcher with session persistence and a per-session activation channel (named by capability, not the `--settings` flag); the X-14 metric of record and decision rule committed and the C-08 served-model record landed; a named owner and expiry with the recorded state "unmeasured, not rejected". The owner is the lead's decision, not C-12's. If C-07 yields no such launcher, the hook half is dropped and only F1 on swarm remains a design question for the swarm slot.
3. Enable trigger (lifts `exchange: off`): a pre-registered two-sided gain-and-cost rule against A2 on module-matched ground truth with a hold-out of at least 4 and a power calculation; tasklist review only (A-001); PR review and rf-qa stay off; all design-note preconditions met, plus S0 and S2 on the product launcher per gateway-class model, hook p95 over at least 30 calls per model, fault injection and the installed-file-set diff.
4. Design note (binding preconditions, not code): `panel-msg/1` per-kind keys, forbidden keys `claim verdict blocking severity category note`, 600-byte cap, located-anchor rule, harness-authored kinds only; a harness-written sidecar for the peer-origin tag with quorum counts over own-origin lines only; untrusted-anchor rules with an adversarial-anchor test; fault injection (seal fails closed, review fails open); single-copy hook requirements (`agent_id` skip, timed lock, seal before first delivery, parallel-call replay); installer footprint (no `hooks.json` entry, package named `exchange/`, not `lib/`).
5. Stricter off-state test: no new file under `~/.claude/hooks/`, no `hooks.json` or merged-settings diff, no run-record key attributable to exchange, a named installed-file-set diff.

## Invariants the debate left unaddressed (from `adversarial/invariant-probe.md`, 16 findings: 2 ADDRESSED, 14 UNADDRESSED)

| ID | Severity | Status | Assumption (short) |
|---|---|---|---|
| INV-005 | HIGH | UNADDRESSED | H1 reaches reflect through the reflect brief with no call-site change; the brief is built in `cli/reflect/ensemble.py:601-630` and does not carry `spec_path`, so naming the driving spec needs an edit in `cli/reflect`, against the adjudicated "no change to cli/reflect" |
| INV-009 | HIGH | UNADDRESSED | H2 (a repair, possibly a re-ask) is core now and compatible with C-01's placement inside both `parse_block` functions, while C-01 INV-003 (pins at `tests/review/test_review_findings.py:113,117`) and slot C-06 are open |
| INV-002 | MEDIUM | UNADDRESSED | the served-model and act-rate probe record has a home |
| INV-003 | MEDIUM | UNADDRESSED | a reserved `exchange` key is "a pin, not an implementation" (`panel.py:37-46,160-176` rejects unknown panel keys, so it is code; changes the template hash) |
| INV-004 | MEDIUM | UNADDRESSED | the off-state byte test coexists with H1 shipping unconditionally (baseline undefined) |
| INV-006 | MEDIUM | UNADDRESSED | a single kit cost figure can gate `kit: on` (elapsed vs token metric, panel size) |
| INV-007 | MEDIUM | UNADDRESSED | a hold-out of at least 4 unseen defects is satisfiable on the 16-item ground truth |
| INV-008 | MEDIUM | UNADDRESSED | a sidecar keyed by reviewer id and finding id is unambiguous across rounds and merged rows |
| INV-010 | MEDIUM | UNADDRESSED | one catalogue source per module, rendered from the installed form, single data source with X-13 |
| INV-011 | MEDIUM | UNADDRESSED | "quorum counts over own-origin lines only" is a quantity C-02 and C-03 compute |
| INV-013 | MEDIUM | UNADDRESSED | the A-layer alone gives mutually blind reviewers (reflect isolation snapshot is pinned off, `models.py:92-100`) |
| INV-014 | MEDIUM | UNADDRESSED | the enable trigger can be met on a lane that can host exchange (tasklist review reaches the panel through reflect, which has no hook-capable lane at HEAD) |
| INV-015 | MEDIUM | UNADDRESSED | the A-layer alone is cost-safe (H2 re-ask spend is not priced or capped) |
| INV-016 | MEDIUM | UNADDRESSED | the premise "no exchange arm has been measured against the static kit" still holds at the current E2 head (see open items) |
| INV-001 | LOW | ADDRESSED | the build trigger can sit unfired with a defined state (residual: a design note has no mechanical consumer, so an expiry triggers nothing) |
| INV-012 | LOW | ADDRESSED | shell-form kit moves would instruct no-Bash lanes to run commands (brief lint added) |

The two HIGH items block convergence under the invariant gate. Both concern H1 and H2, which are shared ground of both positions, not the A-versus-B delta; depth was `standard`, so no Round 3 ran. They are carried as open risks in the return contract (`unaddressed_invariants`).

## Open items

- **[POST-BASELINE] premise check.** The research pins the tasklist-study tip `6c0984326cbb8fb06c4a36065de58b171d3f8175`; both advocates read E2 facts only up to `c44c98a77`. The branch has since gained later commits, the newest being `e2f2ac268` (2026-11-14 19:19, "counted results, replicates and write-up for the five collaboration designs"). This debate's central premise (no exchange arm measured against the static kit) may be answered by that write-up. It was not read and the debate was not rerun on it. It must be re-checked when the unification folds the tasklist branch in (INV-016); if an exchange arm there separates from A2, the "defer" half and the build-trigger ordering change.
- Unresolved diff point C-002 (label only), and the question whether the reserved `exchange` key is code or a design-note entry (INV-003): not decided by the debate.
- Cross-slot dependencies the result rests on: C-06 (H2 policy), C-07 (launcher), C-08 (served-model record), X-13 (class cards), X-14 (metric of record), the reflect-engine-composition slot.

## Artifacts

All under `/home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel/.dev/tasks/to-do/TASK-RESEARCH-review-panel-run2-20261114-075454/reviews/adversarial/collaboration-exchange-capability/`:

- Merged position: `merged-collaboration-exchange-capability.md`
- `adversarial/variant-1-original.md`, `adversarial/variant-2-original.md`
- `adversarial/diff-analysis.md`, `adversarial/debate-transcript.md`, `adversarial/rounds/` (r1-advocate-A, r1-advocate-B, r2-advocate-A, r2-advocate-B)
- `adversarial/invariant-probe.md`, `adversarial/invariant-probe-raw.md`
- `adversarial/base-selection.md`, `adversarial/scoring-pass1.md`, `adversarial/scoring-pass2.md`, `adversarial/scoring-reeval.md`
- `adversarial/refactor-plan.md`, `adversarial/refactor-plan-review.md`, `adversarial/merge-log.md` (11 of 11 changes applied, post-merge validation PASS)
- `adversarial/return-contract.yaml`

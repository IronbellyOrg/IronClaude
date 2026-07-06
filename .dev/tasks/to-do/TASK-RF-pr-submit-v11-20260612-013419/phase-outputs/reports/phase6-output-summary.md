# Phase 6 — Output Inventory (skill / refs / scripts + sync)

Change-set for the Phase 6 M3 lens gate. Wave 6/6b, 4 MOD refs, 2 NEW refs, NEW script,
T-1105/T-1115/T-N50.

| File | V1.1 delta | FR / T-ID |
|---|---|---|
| `SKILL.md` | Wave table (+Wave 6 re-trigger, +Wave 6b decline fallback); Wave 6 S5a bullet (re-trigger via script, applied_edits>0, INV-R1); NEW Wave 6b bullet (strict-once auggie fallback, byte-exact `--depth quick --remediation-offer --auggie-model claude-sonnet-4-6`, no `--no-post-pr`, "don't take the App's bait", `--depth quick`≠troubleshoot conflict); lazy-load rows for review-retrigger.md + auggie-fallback.md; +3 Output Contract fields (rereview_request_count, fallback_invoked, fallback_round_counter); OQ-2 terminal reuse | FR-8/9/10 |
| `refs/augment-poll.md` | 3-state → 4-state (+declined); decline arithmetic in core, raw-surfacing in poll | FR-9.1 |
| `refs/loop-guard.md` | +INV-R1/R2/R3 verbatim blocks; fallback_round_counter as separate counter; 33→37 (event list + count); 5→6 (idempotency sets + auggie_review_invoked) | INV-R1/R2/R3, 33→37, 5→6 |
| `refs/state-machine.md` | +S5a/S5b non-terminal states; +§5.2b topology (RESOLVING→S5a→S5, S5/S2→S5b, S5b→S2, S5b→TERMINAL_CLEAN\|HALT_MAX_ROUNDS); INV-001 edge documented UNCHANGED; flagged §6.5 coverage gap | FR-8/9/10 |
| `refs/detection-contract.md` | 3 decline keys (Phase 3) | FR-9.1 |
| `refs/review-retrigger.md` (NEW) | R1 re-trigger surface; fork-pinned `gh api .../issues/<N>/comments` POST; watermark/attribution; INV-R1. Carries gh token → T-104 path, NOT CORE_PURE_FILES | FR-8 |
| `refs/auggie-fallback.md` (NEW) | R2/R3 fallback; decline detection, strict-once gate, clamp, re-entry, byte-exact flag table, OQ-2 terminals. ZERO gh token → CORE_PURE_FILES | FR-9/10 |
| `scripts/retrigger-review.sh` (NEW) | one pinned `gh api .../issues/<N>/comments -f body="auggie review"`; shared shape (set -euo, die, --pr guard, command -v gh, SoT footer); +x; exits 0/2 | FR-8 |
| `tests/pr_submit/test_static_grep.py` | +auggie-fallback.md to CORE_PURE_FILES; +T-1101 (retrigger fork-pin), +T-1105 (token-in-script-not-core), +T-1115 (flag parity vs auggie-review.md) | T-1105/T-1115/T-N50 |

**Verification:** pr_submit `src↔.claude` synced (diff empty); static-grep 9/9 green; script +x.
**Pre-existing (NOT V1.1):** `make verify-sync` fails on `sc-recommend-protocol MISSING in src/` (same root
as Phase 2 lint) — orthogonal to pr_submit.

**Core-purity boundary (load-bearing):** auggie-fallback.md is the ONLY new ref in CORE_PURE_FILES (gh-free,
verified). review-retrigger.md + retrigger-review.sh carry gh BY DESIGN → T-104/T-1101 fork-pin, NOT T-N50.

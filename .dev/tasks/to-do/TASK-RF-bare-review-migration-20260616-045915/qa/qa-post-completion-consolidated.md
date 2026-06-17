# PC.3 Post-Completion Consolidated Findings (full-migration M3 QA)

**Status: In progress**
**Initial verdict: FAIL (2 IMPORTANT doc/code drifts)** → fix cycle 1 dispatched
**Date:** 2026-06-17

## Agent verdicts (6 lens agents, all report-only, adversarial)
| # | lens | agent | verdict | report |
|---|------|-------|---------|--------|
| 1 | cross-phase-consistency | rf-qa | PASS (1 IMPORTANT: F1) | `qa-post-completion-cross-phase-consistency.md` |
| 2 | final-invariant-compliance | rf-qa | PASS | `qa-post-completion-final-invariant-compliance.md` |
| 3 | evidence-quality | rf-qa | PASS | `qa-post-completion-evidence-quality.md` |
| 4 | end-to-end-coherence | rf-qa-qualitative | FAIL (2 IMPORTANT) | `qa-post-completion-e2e-coherence.md` |
| 5 | anti-attestation | rf-qa-qualitative | PASS | `qa-post-completion-anti-attestation.md` |
| 6 | constraint-compliance | rf-qa-qualitative | PASS | `qa-post-completion-constraint-compliance.md` |

## Issues to fix (verified independently by the orchestrator)
**P1 (IMPORTANT, flagged by #1 + #4) — SKILL.md §3.3 contract schema drift.** `src/superclaude/skills/sc-bare-review/SKILL.md` lines 52-54 document the FLAT legacy contract (`target_checksum`, `reviewers_requested`, `reviewers_succeeded`, top-level `suspect`). The live WS-0 CLI emits the NESTED swarm contract: `target: {checksum}`, `workers_requested`/`workers_succeeded`, `caller_metadata: {suspect}`. WS-A preserved §3.3 verbatim from the legacy skill, carrying forward stale field names → an agent reading only SKILL.md to parse the contract would miss the real keys. FIX: update §3.3 to the nested schema the CLI actually emits (keep it semantic/concise), preserving the ≤80-line invariant; re-run `make sync-dev && make verify-sync` + re-confirm ≤80 lines + zero `t2_`.

**P2 (IMPORTANT, flagged by #4) — observability-procedure.md done.json drift.** `docs/swarm/observability-procedure.md` (Layer 4, debugging recipes ~L40/87/111/113/118) presents `done.json` as the canonical "job finished" signal and treats its absence as a failure symptom — but the default INLINE `swarm run` provably NEVER emits `done.json` (`emit_done_sentinel` has no inline-run call site; `tests/swarm/test_e2e_user_guide.py::test_quickstart_does_not_emit_done_sentinel` asserts this by design). An operator following `[ -f done.json ]` on an inline run would mis-diagnose a SUCCESSFUL run as failed. FIX: clarify that `done.json` is emitted only on the paths that wire the on-completion sentinel (detached/resume), NOT on the default inline `swarm run`; for inline runs the canonical completion signal is `.swarm-state.json` reaching `terminal` + `return-contract.yaml` present. Adjust the debugging recipes so absent `done.json` on an inline run is NOT a failure symptom.

## Non-blocking observations (NO fix)
- O1 (#1,#2): `tests/swarm/test_bare_review_golden_regen.py` retains an executable `LEGACY_SCRIPT` dependency — but it is `skipif`-gated on `SWARM_REGEN_GOLDEN=1` (skips in CI) and fails-loud-by-design if invoked post-deletion; documented in `golden/README.md`. Intentional.
- O2 (#1,#5): WS-C deletions are staged-but-uncommitted — expected (commit is a separate user-authorized step).
- O3: golden `return-contract.yaml` uses the legacy flat schema — by design (semantic reference, never byte-compared); documented.
- O4: terminology nits (Literal-vs-"enum"; `T2Model01..09` vs `..9`) — not defects.
- O5 (#5): PC.3-PC.6 + Task Summary honestly open (close-out ceremony in progress), frontmatter still `🟠 Doing` — correct anti-attestation posture.

## Fix
1 fix cycle dispatched (serialized rf-qa fix agent, `fix_authorization: true`) for P1 + P2. Counter: `phase-outputs/plans/pc3-cycle-count.md` = 1.

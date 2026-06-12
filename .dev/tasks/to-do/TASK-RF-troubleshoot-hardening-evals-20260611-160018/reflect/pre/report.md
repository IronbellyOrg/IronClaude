# sc:reflect UC-1 (Pre-Execution) — Coverage / Gap Audit

- **Run ID:** pre-reflect-troubleshoot-evals-20260611
- **Mode:** pre (UC-1) · **Depth:** deep (TCS=553) executed as single grounded reviewer (executor-disjoint Agent; Tier-2 multi-model fan-out not reliably runnable inside an Agent subagent per project memory `reference_subagent_cannot_nest_skill_fanout`, so the faithful executable form is one grounded reviewer)
- **Tasklist audited:** `.dev/tasks/to-do/TASK-RF-troubleshoot-hardening-evals-20260611-160018/TASK-RF-troubleshoot-hardening-evals-20260611-160018.md`
- **Driving spec:** `.dev/troubleshoot-meta/20260610T141100Z/troubleshoot-pipeline-hardening-RELEASE-SPEC.md`
- **Tie-breaker input:** `research/08-gap-fill-reconciliation.md` (G1 checkout-parent table supersedes research/03's `^` framing)

## Scope note
This tasklist builds a DIFFERENTIAL BACKTEST HARNESS that VALIDATES the spec's hardening gates; it does NOT implement FR-1..FR-13 (owned by the sibling impl /task). Coverage is therefore audited against the harness's spec obligations: NFR-1, §8.3, `backtest_status` (§4.5/§5.4/§5.5), and the §3.1 traceability mapping. FR-1..FR-13 implementation is correctly out of scope and not counted unmapped.

## Obligation-Group Coverage (4 groups)

| # | Obligation (spec source) | Tasklist mapping | Status |
|---|---|---|---|
| 1 | NFR-1 — E1–E5 catch rate "100% would-have-caught"; drives `backtest_status` (spec L316/L433/L523) | Frontmatter (L3–4), Overview (L61), Why (L65), `catch_rate.py` item (L258) | MAPPED |
| 2 | §8.3 — 5 per-escape E2E scenarios + waiver re-green (spec L575–580) | Key Objective 4 (L78) "mapped 1:1 to §8.3"; replay-table (L184) | MAPPED (5/5) |
| 3 | `backtest_status` — enum `not_run\|partial\|complete`, §5.4 derivation, §5.5 separation (L316/L415–423) | `catch_rate.py` item (L258): enum + §5.4 derivation in `__post_init__` + §5.5 separation | MAPPED |
| 4 | §3.1 — Escape/Wave/Evidence traceability (L249–257) | replay-table (L184) pins each E→primary catch-wave; runners 1:1 | MAPPED |

## Substance checks (per memory `feedback_sc_reflect_vs_inline_rfqa`: spec-literal tokens + invariant arithmetic + parent-vs-head)

**S1 — Spec-literal enum tokens + CATCH/MISS + wave mapping — PASS.** Enum triple `not_run`/`partial`/`complete` co-occurs as a literal set at task L109/L258/L262/L266/L270/L274/L284/L296/L352/L370/L444. `CATCH`/`MISS` literals in title/description/H1/overview. Wave mapping verbatim (L184): E1→H1, E2→H3, E3→H3, E4→H2, E5→H4 — matches §8.3 primary catch-wave exactly. (§3.1 also lists secondary waves H2 for E1, H1 for E4, H5 for E5; tasklist correctly pins the primary catch-wave per the §8.3 oracle.)

**S2 — `backtest_status` arithmetic incl. anti-vacuity — PASS.** §5.4 derivation encoded verbatim (L258): all 5 CATCH → complete; 1–4 → partial WITH missing escape IDs; none/not-run → not_run. Anti-vacuity holds: NEW=CATCH proxies SKIP (not pass) until impl refs land, so a green-but-empty run reports `not_run`, never a vacuous `complete`; the tasklist further tightens `complete` to require each escape's non-null `negative_witness` + `card_path` (exceeds, not contradicts, spec intent). §5.5 separation clause (signoff advisory until complete) present.

**S3 — Parent-vs-HEAD: bare parents, NO caret, E4 pinned — PASS.** Parents `94d5baa0/10723863/e97aa4fd/1b0264f1/d878bc6d` pinned (L184); item mandates checkout with NO `^` (zero caret arithmetic; research/08 tie-breaker over research/03). E4 pinned to pre-fix parent `1b0264f1` (NOT HEAD — HEAD healed via `20693bb8`, a HEAD replay would not reproduce the bug → false PASS avoided); E4 fix `b97c9960` flagged UNMERGED.

## Non-blocking observations
- `complete` raw token count inflated by "mark this item complete" boilerplate; genuine enum usage verified via co-occurrence — not a finding.
- Skip-guarded NEW=CATCH is designed staged-delivery behavior (L87), not a gap; OLD=MISS + harness wiring + report schema run green now.
- §3.1 secondary waves (E1→H2, E4→H1, E5→H5) lack dedicated runners — a scoping choice (each escape scoped to its primary catch-wave per §8.3), not an unmapped requirement.

## Return contract
```
status: passed
coverage_pct: 1.0
unmapped_requirements: none
run_id: pre-reflect-troubleshoot-evals-20260611
```

VERDICT: PASS

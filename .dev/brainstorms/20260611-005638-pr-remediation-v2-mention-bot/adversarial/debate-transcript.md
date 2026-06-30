# Adversarial Debate Transcript

## Metadata

- Depth: deep | Rounds: 1 (parallel statements = the 3 generated variants) + Round 2.5 invariant probe
- Convergence (raw diff-point agreement): 0.82
- Convergence threshold: 0.75
- Gate status: **BLOCKED_BY_INVARIANTS → resolved-in-merge** (4 HIGH closed)
- Advocates: V1 opus:architect, V2 sonnet:security, V3 haiku:devops (heterogeneous vendors)

## Round 1 — Advocate positions (steelmanned)

**V1 architect (one-shot runner).** Strongest steelman: the dominant risk is a write+push LLM
on untrusted text; a one-shot host collapses secret-window + restart-safety to non-properties
and presents *no inbound network surface*. Genuine concession: polling cursor must be
GitHub-durable, not a local timestamp.

**V2 security (split host).** Steelman of others before critique: V1's secret-window argument
is correct *for the executor*; V3's operational depth is correct *for the watcher*. Synthesis:
make the long-lived component a **dispatcher that runs no agent in-process** and the executor a
**one-shot sandboxed runner per trigger**. Decisive unique move: opComment is **data, not a
shell argument** — the literal `/sc:troubleshoot "${opComment}"` form is itself the vuln.

**V3 devops (persistent daemon).** Steelman: a daemon gives native systemd supervision,
watchdog, ETag rate-limit discipline, and observability depth a one-shot can't. Genuine
catch: SHA-correlation to stop a *independent* Augment re-review from falsely advancing the
round counter. Concession (under cross-pressure): agent-in-process is the weak point.

## Per-point scoring matrix

| Diff point | Winner | Confidence | Evidence |
|------------|--------|-----------|----------|
| C-001 host shape | **V2 split** | 85% | Reconciles X-001; watcher≠executor separates secret blast-radius from operability |
| C-002 autonomy levels | V2 (5-level + MIN) | 80% | Finer control + monotonic safety composition; V1's 2-level too coarse |
| C-003 opComment delivery | **V2 (data-not-shell)** | 95% | All concede; corrects topic phrasing; only V2 specified JSON envelope + egress deny |
| C-005 round commit order | **neither** | 60% | V1 after-act (double-push) vs draft before-act (counted-not-done) → two-phase (INV-002) |
| C-006 re-review attribution | V3 (SHA-corr) | 72% | Only V3 addressed false advancement; predicate tightened to exact-match (INV-005) |
| Parent resolution (OQ-B) | V1 | 80% | `in_reply_to_id` + parentless-reject most rigorous |
| Authz bypasses | V2 | 90% | Only V2 enumerated spoof/bot/TOCTOU/author-≠-mentioner |
| Secret handling | V2+V3 | 85% | V2 catches `build_env` full-inherit risk; V3 adds systemd hardening + PAT scopes |
| Audit ledger | V3 | 88% | Concrete JSONL event schema |
| Ops/deploy | V3 | 90% | Only V3 has systemd unit + runbook |

## Round 2.5 — Invariant probe (see invariant-probe.md)

Fault-finder (independent opus, consensus-only context) returned **4 HIGH-UNADDRESSED**
(INV-001 credential-delivery contradiction; INV-002 round commit-order; INV-003 parent-body
TOCTOU; INV-007 propose-only-not-hard-guaranteed) + 10 MEDIUM. Per AD-1 gate, convergence is
**blocked** until the HIGH items are resolved. All four are resolvable: three by adopting the
stronger variant position (V2), one (INV-002) by a two-phase intent/outcome ledger synthesis.

## Convergence Assessment

- Raw diff-point agreement: **0.82** (strong agreement on fundamentals).
- Taxonomy coverage: L1 (naming/home) ✓, L2 (host/component architecture) ✓, L3 (state/guards/
  concurrency — round ordering, TOCTOU, idempotency) ✓ — all covered.
- Invariant gate: 4 HIGH UNADDRESSED → **BLOCKED**, then **resolved-in-merge** (refactor-plan
  §Resolutions). Post-resolution effective convergence: **0.78** (above threshold).
- Status: **PARTIAL→PASS** — converged on fundamentals; merge closes the 4 HIGH gaps and
  records the 10 MEDIUM as explicit resolutions/named open decisions.

Unresolved (carried to merged spec as named decisions): INV-009/INV-018 round-key granularity
(per-PR push-budget chosen); INV-012 24/7 PAT exposure (short-lived minted push token chosen).

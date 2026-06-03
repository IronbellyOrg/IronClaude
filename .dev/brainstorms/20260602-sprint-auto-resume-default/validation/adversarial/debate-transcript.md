# Adversarial Debate Transcript — DD-1

## Metadata
- Depth: standard (Round 1 + Round 2 + Round 2.5 invariant probe)
- Rounds completed: 2 + invariant probe
- Convergence achieved: 78% (below 0.80 — gated by HIGH invariant, see below)
- Convergence threshold: 80%
- Focus areas: crash durability, atomicity, concurrency, flush ordering, "phase survives" claim
- Advocate count: 2

## Round 1: Advocate Statements

### Variant 1 Advocate (derive-only, DD-1 as written)
**Position summary:** The ledger already exists and is written every phase; adding a breadcrumb is net-new write-path surface that NG1 forbids, and the planner reads tolerantly so degradation is graceful.

**Steelman of B:** B is right that `os.replace` is atomic and that the result.json writer deliberately chose it for crash-safety (executor.py:2056-2057). If the cursor must be perfectly crash-durable, B's mechanism is strictly stronger and reuses a proven in-repo pattern.

**Strengths claimed:**
1. Zero new write-path surface; honors NG1 and the design's "one write-path change only" property.
2. No second artifact to keep consistent with the ledger (no skew between breadcrumb and phase_start).
3. Tolerant reader (design §3 "skip malformed lines") means a torn tail degrades to "last good phase_start," not a crash.

**Weaknesses identified in B:** B doubles the per-phase write count and introduces a consistency question (which wins if breadcrumb and ledger disagree?).

**Concessions:** The claim "phase_start is written BEFORE a phase executes" is imprecise for the single-process path — `proc_manager.start()` (executor.py:1331) runs before `write_phase_start` (executor.py:1335). The process is already spawned when the line is written. Conceded.

### Variant 2 Advocate (atomic breadcrumb)
**Position summary:** Derive-only's entire thesis is "the phase number always survives a crash." That is false in exactly the hard-crash case it claims to cover, because the JSONL append has no atomicity and no durability guarantee.

**Steelman of A:** A is right that for the common case (graceful signal → `phase_interrupt` at executor.py:1488, or clean `phase_complete`) the ledger is fully sufficient, and that a breadcrumb adds surface. For SIGTERM-style shutdowns the ledger is genuinely balanced and derive-only works.

**Strengths claimed:**
1. **Torn-line immunity (C-001/X-002).** Verified: `_jsonl` is `open(...,"a"); f.write(json+"\n")` (logging_.py:265-267). Grep confirms ZERO `fsync`/`flush`/`os.replace`/`flock` in logging_.py. A SIGKILL/OOM/power-loss between the `write()` syscall and the kernel flushing the page can leave the `phase_start` line absent, or — if the write is split across a page boundary — leave a torn (non-JSON) final line. The result.json writer at executor.py:2070-2072 uses tmp+rename precisely to avoid this; the cursor deserves parity.
2. **Single-writer authority.** A 2-field file parsed directly, vs. a scan-all-events-and-pair loop that interleaving can confuse.
3. **In-repo precedent (U-001).** The codebase already decided truncation-safety matters for the result file; the cursor points AT that file but is held to a weaker standard.

**Weaknesses identified in A:** "Always survives" is an overclaim; the tolerant reader converts a torn tail into "last good line," which for a single-phase-deep crash means NO phase_start at all → fall back to "first phase without result.json."

**Concessions:** The fallback ("first phase without result.json") is in fact safe IF re-running a phase from scratch cannot corrupt completed work — which is the BoundaryIntegrityGate's job (A-002). If the gate holds, the cursor's exactness is a convenience, not a correctness property.

## Round 2: Rebuttals

### Variant 1 (derive-only) rebuttal
Concedes C-001 factually but argues the **consequence is bounded**: when the only `phase_start` is torn/absent, the planner does not guess wrong — it falls back to "first phase without `result.json`" (design §3 line 116-117 logic), which is the SAME phase the breadcrumb would have named (the interrupted one, whose result.json was never written because it never completed). So in the single-deepest-crash case, **derive-only and breadcrumb converge on the same answer.** The breadcrumb only wins when result.json for the interrupted phase ALREADY EXISTS (partial per-task data) AND the ledger tail is torn — a narrow intersection, and in that case granularity=TASK is driven by result.json, not the cursor.

Counter on concurrency: derive-only's pairing loop is MORE fragile to interleaved concurrent writes than a last-write-wins breadcrumb. Conceded as a shared weakness, not a differentiator that favors A.

### Variant 2 (breadcrumb) rebuttal
Accepts the convergence argument for the deepest-crash case but presses the **residual window**: the breadcrumb is written and rename-committed BEFORE `phase_start`; so even the "result.json exists + torn ledger tail" case is covered authoritatively. More importantly, B argues the cost is being overstated: the breadcrumb reuses the EXACT `_write_phase_result_json` convention (tmp.write_text + tmp.replace), so it is ~3 lines, backward-compatible (absent ⇒ ledger fallback), and adds one tiny write per phase — negligible against a Claude subprocess phase.

B's final point: even if derive-only is *adequate* because of the result.json fallback + gate, the design DOCUMENT is wrong on two verifiable facts (X-001 "before a phase executes"; X-002 "always survives"). The decision can stand but the rationale text must be corrected, or the next reader builds on a false premise.

## Round 2.5: Invariant Probe (Fault-Finder)

| ID | Category | Assumption | Status | Severity | Evidence |
|----|----------|------------|--------|----------|----------|
| INV-001 | state_variables | The last JSONL line is intact on hard crash | UNADDRESSED (by A) | **HIGH** | logging_.py:265-267 append w/ no fsync/rename; grep shows zero durability primitives. A's thesis depends on this; it does not hold. |
| INV-002 | guard_conditions | `phase_start` precedes subprocess execution | UNADDRESSED (by A's text) | MEDIUM | executor.py:1331 `proc_manager.start()` precedes :1335 `write_phase_start`. True for per-task path (:1267 before :1270), false for single-process path. |
| INV-003 | interaction_effects | Concurrent `sprint run <same index>` cannot interleave ledger writes | UNADDRESSED (both) | MEDIUM | `_resolve_release_dir` (config.py:242-278) is deterministic from index_path; no PID/timestamp/lock. Two runs share one execution-log.jsonl, both plain-append. Pairing loop can mis-associate. |
| INV-004 | sufficiency_challenge | Does derive-only ALONE correctly recover the interrupted phase? | ADDRESSED | LOW | Yes, via the result.json fallback (design §3 line 116): "lowest non-COMPLETED phase with any start/result, else None" does NOT actually require the phase_start line — it also keys off result.json presence. So the cursor is recoverable from result.json alone in the deepest-crash case. This is why INV-001 is bounded, not fatal. |
| INV-005 | collection_boundaries | Crash before ANY phase_start AND before any result.json (phase 1 dies instantly) | ADDRESSED | LOW | Falls to "no phase ever started ⇒ fresh start_phase=1" (design §3 line 118). Safe. |

**Invariant gate:** INV-001 is HIGH + UNADDRESSED **with respect to the design's written rationale** ("phase number is still known" / "always survives"). It is NOT HIGH with respect to the *recoverability of the correct phase*, because INV-004 shows result.json presence is an independent, atomic (tmp+rename) signal the planner already uses. Net: the DECISION's outcome is sound; the DECISION's stated MECHANISM/justification is partly false. → blocks 80% convergence, drives REFACTOR not REJECT.

## Scoring Matrix
| Diff Point | Winner | Confidence | Evidence Summary |
|------------|--------|------------|------------------|
| S-001 | A | 60% | Single source of truth is simpler; B's second file adds a consistency axis. |
| C-001 | B | 90% | Torn/absent line is real; verified no durability primitives. |
| C-002 | A | 70% | Zero added write surface is a genuine virtue; NG1. |
| C-003 | tie | 50% | Both fall back to "first phase without result.json." |
| X-001 | B | 95% | Conceded by A; single-process path spawns before logging. |
| X-002 | B | 85% | "Always survives" is false as written; bounded by result.json fallback. |
| U-001 | B | 90% | In-repo atomic precedent is a strong consistency argument. |
| A-001 | — | — | Safety net (re-run phase) holds only if gate quarantines partial work (FR-2). |
| A-002 | — | — | Gate is the true correctness backstop; cursor exactness is convenience. |

## Convergence Assessment
- Points resolved: 7 of 9 (A-001/A-002 are shared assumptions, not won/lost)
- Alignment: 78%
- Status: NOT_CONVERGED (blocked by INV-001 HIGH against the written rationale)
- Resolution: Both advocates converge that the *decision outcome* (no new heavyweight state store; ledger + result.json suffice to recover the phase) is correct, but the *rationale text* contains two false claims (X-001, X-002) and omits the result.json fallback as the actual durability anchor. This is a REFACTOR of the justification, not a reversal of the decision.

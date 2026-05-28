# Spec-Fidelity Convergence — Historical Context Synthesis

**Pipeline failure under investigation**:
`/config/workspace/TUIBBS-scp/.dev/releases/current/v1-MVP/spec-fidelity.md`
> Convergence Result: FAIL — Runs: 3 — Final HIGH count: 54.
> Halt: "Convergence not reached after 3 runs. Remaining active HIGHs: 54. TurnLedger: available=31, consumed=46."

**Failure shape (from `deviation-registry.json`)**:
- 58 HIGHs caught in Run 1 → 54 remain ACTIVE through Run 3.
- All 54 ACTIVE HIGHs share an identical signature: `dimension=signatures`, `source_layer=structural`, `mismatch_type=phantom_id`, description `"Roadmap references ID 'D0N' not found in spec"` for N=01..54.
- Roadmap uses `D01`…`D54` (zero-padded, 32–259 occurrences of each Mx milestone). Spec (`epics.md`) uses `D1`, `D3`, `D5` (no zero-pad).
- 4 FIXED HIGHs were unrelated (`data_models / spec_file` — manifest gaps that the agent successfully added to the roadmap in Run 1).
- Run 2 roadmap_hash differs from Run 3 roadmap_hash (`8f6eba…` → `d6070e…`) — remediation IS editing, but the edits don't reduce `phantom_id` count.

---

## Section 1 — Tried and worked

| Release | PR / Commit | Root cause diagnosed | Fix shipped | Held? |
|---|---|---|---|---|
| `v3.05_DeterministicFidelityGates` | spec at `.dev/releases/complete/v3.05_DeterministicFidelityGates/deterministic-fidelity-gate-requirements.md:849` wiring `execute_fidelity_with_convergence` into `executor.py` step 8 | LLM-evaluated fidelity gate had no memory of prior runs; ad-hoc retry. | **3-run convergence engine** with `DeviationRegistry`, `TurnLedger` budget, monotonic-progress invariant on `structural_high_count`. Code: `src/superclaude/cli/roadmap/convergence.py:432-668`. | Partial — converges for simple roadmaps; structurally cannot converge for the failure modes documented below. |
| `v3.0_unified-audit-gating` | `.dev/releases/complete/v3.0_unified-audit-gating/fidelity-remediation-log.md` — 5-vote statistical aggregation | Severity drift (Run-1 MEDIUM → Run-3 HIGH by different LLM invocation) and "phantom FR-NNN" IDs. | Run-5 used 5-vote consensus; HIGHs absent from 5/5 votes reclassified DISPUTED → MEDIUM. | One-shot success (Run 1: 3 HIGHs → Run 5: 0 HIGHs after consensus). |
| `roadmap-spec-fidelity-fix` (backlog, ranking dated 2026-05-15) | `.dev/releases/backlog/roadmap-spec-fidelity-fix/RANKING.md`, `adversarial/merged-solution.md` | Two pathologies on a previous 10-HIGH failure: (a) `files_affected=[]` → agents had no target file → fell back to rewriting TDD spec → 71% / 38% diffs rejected by 30% guard; (b) parser noise (URL fragments, brace expansions, `<1%`, `<2%` NFR softs) emitted as HIGH. | S1+S2+S5 merged: S1 sanitize parser, S2 `_route_findings` to add `files_affected=[roadmap.md]` + actionable `fix_guidance`, S5 context-aware NFR severity demotion. | Held for the original 10-HIGH failure shape. **Did NOT prevent the present `phantom_id`-only failure**: every remaining HIGH already has `files_affected=[roadmap.md]` set, yet the agent cannot make a small additive edit that satisfies the checker. |
| `v3.1_Anti-instincts__` | `.dev/releases/complete/v3.1_Anti-instincts__/anti-instincts-gate-unified.md` + integration-contracts wiring | Generation-time integration enumeration weak — LLM produced incoherent `integration_contracts`. | Added `INTEGRATION_ENUMERATION_BLOCK` prompt injection + deterministic `_canonicalize_identifiers` for contracts (`integration_contracts.py:445`). | Held — but per `v3.0` debate-transcript.md:58, the *extra* dimension may *worsen* attention burden on the spec-fidelity prompt. |

## Section 2 — Tried and failed (or only partially worked)

| Release | Fix attempted | Failure mode that re-emerged |
|---|---|---|
| Convergence engine itself (`convergence.py`) | 3-run loop with monotonic-progress invariant + regression detection. `max_runs=3` (line 440). Pass condition `registry.get_active_high_count() == 0` (line 539). | When findings are **structurally unfixable by additive edit** (e.g., systematic ID-schema mismatch across 54 records), the loop runs 3× burning budget but cannot drive the count to 0. Present failure: Run 1 (58) → Run 2 (54) → Run 3 (54) — flatline. The monotonic invariant doesn't fire because the count *did* decrease 58→54 in Run 2. |
| `S2 — route_findings + actionable fix_guidance` | Per `structural_checkers.py:454` the `_route_findings` helper attaches `files_affected=[roadmap.md]`. Per `_make_finding` (line 270-282), `fix_guidance=f"Address {mismatch_type} in {dimension} dimension"` — generic, not templated by mismatch type. | The TUIBBS failure: every finding has `files_affected` set, but the generic guidance "Address phantom_id in signatures dimension" doesn't tell the agent **whether** to (a) remove the D01-D54 IDs from the roadmap, (b) add D01-D54 to the spec, or (c) normalize the schema. Result: 3 runs of churn; roadmap_hash changes (8f6eba→d6070e) but `phantom_id` count is unchanged. |
| `S5 — context-aware NFR severity` | Heading-path-aware NFR severity demotion. | Doesn't help — TUIBBS has **0 semantic HIGHs**. All 54 are structural `phantom_id`. NFR demotion has no surface to act on. |
| 30% diff-size guard (`remediate_executor.py:309-362`) | Rejects patches changing >30% of `original_lines`. Designed to stop full-doc regeneration that destroys prior fixes. | When the ONLY correct fix requires renaming 54 ID references (`D01`→`D1`, `D02`→`D2`, …) — i.e. a global schema migration — that's a > 30% diff to `roadmap.md`. The guard rejects the only structurally-correct fix and accepts cosmetic noise. `--allow-regeneration` escape valve exists but is the BACKUP-WORKAROUND, not a default. |
| Per-`fidelity-remediation-log.md` (v3.0) row "DISPUTED post-remediation" | LLM attention drift produced 2 brand-new HIGHs in the post-remediation check that were absent from any of the 5 consensus votes. | Confirms there's a steady-state false-positive rate from the LLM-driven fidelity check. The convergence loop has no way to distinguish a Run-N false-positive from a real defect. |

## Section 3 — Tried and reverted

| Release | What was reverted | Reason |
|---|---|---|
| `roadmap-opus-architect.md.bak-pre-mixed-drift-fix` (in TUIBBS itself, NOT IronClaude) | Backup of a prior opus-architect output kept beside the active version. | Indicates manual rollback of an opus-architect output during the `mixed-drift-fix` iteration — exact reason not in commit message; preserved for forensics. |
| No clean revert of convergence engine itself found in `.dev/releases/complete/`. | — | The 3-run loop has been incrementally extended (regression detection added BF-3, TurnLedger reimbursement in v3.05), never replaced. |
| `S3 — tiered diff relaxation`, `S4 — budget overhaul`, `S6 — MANUAL_TRIAGE halt` from the roadmap-spec-fidelity-fix backlog | NOT MERGED (deferred, not reverted). See Section 4. | S3 mismatched the failure shape; S4 falsified its own premise; S6 considered a safety net unnecessary if S1+S2+S5 held. The current failure shape suggests at least S6 should be re-promoted. |

## Section 4 — Discussed but never tried

| Proposal | Source artifact | Status / why deferred | Still applicable now? |
|---|---|---|---|
| **S6 — MANUAL_TRIAGE halt** | `.dev/releases/backlog/roadmap-spec-fidelity-fix/solutions/S6-skip-unfixable-findings.md`, RANKING.md:24 | Deferred as "safety net, not required if top-3 converge." | **HIGH applicability** — the present failure is exactly the scenario S6 was designed for: structurally-unfixable findings that won't drop to zero. Re-promote. |
| **S3 — tiered diff-relax** | RANKING.md:25 | Deferred — "wrong failure shape; defensive future feature." | **HIGH applicability now** — the structurally-correct fix (rename 54 IDs across roadmap) IS a > 30% diff. S3's tiered relaxation would route this through a higher diff allowance for `signatures:phantom_id` specifically. |
| **S4 — budget overhaul** | RANKING.md:26 | Deferred — "falsified its own premise; observability cleanup only." | Low applicability — the present failure has `available=31, consumed=46`. Budget exhaustion is not the proximate cause; convergence-loop limit IS. |
| **5-vote statistical consensus** for spec-fidelity gate | `v3.0_unified-audit-gating/fidelity-remediation-log.md` (used once for that release, never wired into the convergence engine) | One-off manual technique, never automated. | **MEDIUM applicability** — would tame LLM attention drift but cannot fix the deterministic `D01 ≠ D1` checker comparison; that is not LLM noise. |
| Tier-2 fidelity-investigation specs (Variants A/B/C of `v3.0_unified-audit-gating/adversarial-design-review/fidelity-investigation/`) | `adversarial/debate-transcript.md` (250+ lines) | Final consensus: "all three are architecturally excellent **for their own gates** but **none of them fix the actual broken component**" (debate-transcript.md:127). Wiring/Anti-Instincts gates landed; spec-fidelity surgery did not. | **Very high applicability** — the explicit consensus is that no shipped remediation has touched the spec-fidelity gate's LLM-based severity assessment or the deterministic ID-comparison. |
| Re-promotion of `prd_template.md` / `tdd_template.md` to spec manifest | RANKING.md:55-56 ("If the spec is genuinely missing these references … the spec needs editing, not the roadmap. That's a human decision.") | Punted to human. | Low applicability for present failure (different artifact), but the pattern — *checker emits HIGH that only a spec edit can satisfy* — is the present pattern at scale (54 instances). |
| ID-schema normalization (`D01 ↔ D1`) | **Not present in any backlog, debate, or open task that I could find** | Never proposed in code or design. `_REQUIREMENT_PATTERNS["D"]` (`spec_parser.py:329`) matches both with the same regex but does NOT canonicalize. The set difference at `structural_checkers.py:380` uses raw strings. | **Highest applicability** — this is the direct mechanical cause of the 54 ACTIVE HIGHs. No prior proposal addresses it. |
| 5-vote consensus / DISPUTED reclassification automated inside `convergence.py` | `fidelity-remediation-log.md` ran this by hand (run 5) | Never automated. | Medium — would help with LLM noise but not with the deterministic checker bug. |

## Section 5 — Pattern recognition

1. **The convergence loop solves "remediation didn't converge in 1 retry"; it does not solve "the checker is emitting findings the agent provably cannot fix with an additive edit."** Every shipped remediation (S1, S2, S5, monotonic-progress invariant, regression detection, TurnLedger budget) hardens the loop's *mechanics*. None of them address the precondition that **the set of findings must be reachable by an additive edit that fits inside the 30% diff guard**. When that precondition is violated (TUIBBS: 54 schema-mismatch IDs), the loop is structurally guaranteed to fail.

2. **Every prior failure shape has been distinct.** v3.0: phantom FR-NNN IDs + severity drift. Mid-May 2026 (roadmap-spec-fidelity-fix backlog): 10 HIGHs with `files_affected=[]` and parser noise. v1-MVP TUIBBS (today): 54 HIGHs with `files_affected` populated, no parser noise, but a systematic ID-schema mismatch (`D01` vs `D1`). The remediations are shape-specific patches; each new release surfaces a new shape because the structural primitive (deterministic exact-string comparison + LLM-driven additive remediation + 30% diff guard) hasn't changed.

3. **The adversarial-design-review consensus from v3.0 (`debate-transcript.md:127`) explicitly warned that no shipped fix touches the spec-fidelity gate's broken comparator.** Every subsequent remediation has continued to harden surrounding machinery (TurnLedger, registry, regression detection, route_findings) rather than the comparator itself. This is the highest-signal artifact pointing at the structural problem: the team has been working around a known unaddressed root cause.

4. **The BACKUP-WORKAROUND escape valve (`--allow-regeneration --max-runs 5`) exists precisely because the structural problem is unsolved.** Per `.dev/releases/backlog/roadmap-spec-fidelity-fix/BACKUP-WORKAROUND.md`, the escape valve is recommended "after the top-3 fixes have been merged and verified to compile/test-pass, AND `superclaude roadmap run … --resume` still fails at spec-fidelity." Its existence is an admission that the convergence guarantee is best-effort, not load-bearing.

5. **S6 — MANUAL_TRIAGE halt — was deferred because it didn't seem load-bearing alongside S2. The present failure shape is exactly what S6 was for.** When the checker emits findings whose only correct fix is a schema migration that exceeds the 30% diff guard, the loop should not silently burn 3 runs and halt with a budget-exhausted message; it should classify the findings as `MANUAL_TRIAGE` after Run 2 produces zero structural progress and surface them with a clear "this requires a spec change / schema normalization" verdict. Re-promoting S6 alongside an ID-schema normalization in the checker would convert the present halt from "convergence not reached" (opaque) to "2 unfixable findings: D01-D54 phantom IDs require ID-schema reconciliation; recommend `D-?` canonicalization" (actionable).

---

## Inputs to Phase 1 (do not delete; `/sc:troubleshoot` Wave 1.5 will pick this up)

**Key sources that ground the diagnosis:**
- `src/superclaude/cli/roadmap/structural_checkers.py:380-391` — exact-string set-difference for phantom_id detection.
- `src/superclaude/cli/roadmap/spec_parser.py:329` — `\bD-?\d+\b` regex matches both forms but does not canonicalize.
- `src/superclaude/cli/roadmap/convergence.py:432-668` — 3-run loop; pass condition; halt formatter.
- `src/superclaude/cli/roadmap/remediate_executor.py:309-362` — per-patch 30% diff guard.
- `.dev/releases/backlog/roadmap-spec-fidelity-fix/RANKING.md` — full prior 6-way debate, including deferred S3 and S6.
- `.dev/releases/complete/v3.0_unified-audit-gating/adversarial-design-review/fidelity-investigation/adversarial/debate-transcript.md:127` — consensus that the comparator itself was never touched.
- `/config/workspace/TUIBBS-scp/.dev/releases/current/v1-MVP/deviation-registry.json` — 54 ACTIVE phantom_id findings, identical shape, distinct D-IDs.
- `/config/workspace/TUIBBS-scp/.dev/releases/current/v1-MVP/spec-fidelity.md` — convergence halt report.

**Structural-cause hypothesis (Phase 1 to validate or refute):**
The TUIBBS v1-MVP halt is a deterministic checker bug intersecting with a non-additive remediation requirement. The checker's `phantom_ids = roadmap_ids - spec_ids` does raw string set difference. `{D01, …, D54}` − `{D1, D3, D5}` = `{D01, …, D54}`. The only correct fixes are (a) canonicalize ID forms in the comparator (one-line code change in IronClaude; structural fix), (b) rewrite all 54 roadmap IDs to remove zero-pad (54-row roadmap edit > 30% diff; rejected by guard), or (c) add D01-D54 to the spec (spec is an input, agent isn't allowed to modify it). The convergence loop, lacking a `MANUAL_TRIAGE`-style escape, cannot distinguish (a) from agent failure to remediate — so it burns 3 runs and emits a budget-style halt message that mislocates the cause.

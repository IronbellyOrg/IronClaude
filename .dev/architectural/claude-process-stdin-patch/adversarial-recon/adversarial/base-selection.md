# Base Selection — Step 3 (asymmetric spec-vs-implementation)

## Metadata

| Field | Value |
|---|---|
| Mode | A (--compare, asymmetric: A=built, B=spec) |
| Variant A | `variant-1-implementation.md` (8-commit diff `142ce15..db8cffe`) |
| Variant B | `variant-2-spec.md` (RECONCILED_DESIGN.md, §1-§11) |
| Convergence achieved | R3 (impl 0.85 / spec 0.80, avg 0.825) |
| Tiebreaker required? | No (margin 5.0% — see §4) |

This is **asymmetric**: variant A is a code diff, variant B is a 49 KB design spec. Standard 5-metric quant cannot apply identically to a diff and a doc; this run uses **coverage-quant** below.

---

## §1 Quantitative Scoring (50% weight) — coverage-quant

Replaces the standard 5-metric grid (which assumes two artifacts of the same kind). All numbers traceable to `diff-analysis.md` U-NNN counts and `invariant-probe.md` ADDRESSED/UNADDRESSED ratios.

### §1.1 Spec-coverage by implementation

How much of B's deliverable surface (P-NNN, T-NNN, AC-NNN, Risk-NNN, D-NNN) does A actually implement?

| Spec category | Items in B | Items implemented in A | Coverage |
|---|---|---|---|
| §4 Patches (P-001..P-005) | 5 | 5 (commits `526a606`, `c42139b`, `be46520`, `5a8e5e7`, `01cf2ef`) | **100%** |
| §5 Tests (T-001..T-011) | 11 | 11 (test_process_stdin.py L201-597) | **100%** |
| §3.1 D-NNN in-scope (the 27 source-code-affecting items) | 27 | 27 (matched in C-001..C-031) | **100%** |
| §3.1 D-NNN process items (D-067 CI, D-078 PR, D-080 base, D-084 upstream-PR, D-086 338KB repro, D-088 LOC budget) | 6 | 1.5 (D-080 implicit ✓, D-088 within bound ✓; D-067/078/084/086 absent) | **25%** |
| §3.2 SUPERSEDED items (audit-trail attestation) | 12 | 0 (no in-tree ledger) | **0%** |
| §3.2 DEFER-TO-BEAT-2 items (tracking artefact) | 15 | 0 (no `BEAT_2_BACKLOG.md` until R3 concession) | **0%** |
| §6 Risks-resolved attestations | 3 | 0 (no in-tree restatement) | **0%** |
| §7 Risks-deferred (R-1..R-6 register in-tree) | 6 | 0 | **0%** |
| §9.2 Deployment runbook (pipx rebuild + Coder repro) | 1 | 0 | **0%** |
| §10 Acceptance checklist (8 items) | 8 | 3 (P-NNN landed ✓, T-NNN green ✓, existing-tests-pass via CI ✓) | **38%** |
| §11 Provenance / D-NNN traceability | 1 | 0 | **0%** |

**Weighted spec-coverage** (weighting source code 60%, tests 25%, process artefacts 15%):

```
0.60 * 1.00 + 0.25 * 1.00 + 0.15 * 0.10 = 0.60 + 0.25 + 0.015 = 0.865
```

**Source-code & test surface: 100%. Process-artefact surface: ~10%.**

### §1.2 Drift count (A-only items not in B)

From `diff-analysis.md` U-001..U-016 (Unique to A):

| Severity | Count | Items |
|---|---|---|
| MEDIUM | 5 | U-003 narrative comment, U-007 asymmetric `_stdin_error` read, U-008 boundary-pass test, U-009 negative companion test, U-014 8th docs commit |
| LOW | 11 | U-001/U-002 pragmas, U-004 class-attr placement, U-005 `n<=0` defensive, U-006 false-positive (matched), U-010..U-013, U-015, U-016 |

**Substantive drift count (medium-and-up): 5.** Of these, only U-007 is a defect; the rest are positive drift (more rigour, useful narrative) or stylistic.

### §1.3 Contradiction count

From `diff-analysis.md` X-001..X-007:

| Severity | Count | Items |
|---|---|---|
| MEDIUM | 3 | X-001 commit ordering framing, X-004 `prompt_via=stdin` log token, X-006 conditional T-011 assertion |
| LOW | 4 | X-002 18s vs 16s, X-003 `<` vs `≤`, X-005 spec typo (A corrected B), X-007 doc-status flip cross-link |

**Substantive contradiction count: 3.** Of these, X-004 and X-006 are real fixes (lands R3); X-001 is contract-equivalent.

### §1.4 Test mutation-kill estimate

From `invariant-probe.md`: 30 invariants probed; 14 ADDRESSED (47%), 16 UNADDRESSED (53%).

But of the 16 UNADDRESSED, **only 2 are HIGH** (INV-004 / INV-025, the PrdClaudeProcess.terminate family — both ADDRESSED in R3 by the impl-advocate's 4-line patch + new test). The remaining 14 UNADDRESSED are MEDIUM (6) or LOW (8), and 5 of the 6 MEDIUMs are pinned by R3 concessions.

**Effective post-R3 mutation-kill rate**: of 30 invariants, 14 + 2 + 5 = 21 ADDRESSED-after-R3 = **70%**.

### §1.5 Coverage-quant score (combined)

| Metric | Weight | A-as-base score | B-as-base score |
|---|---|---|---|
| Spec-coverage by impl | 30% | N/A (frame question — see §3) | N/A |
| Code-surface fidelity | 25% | 1.00 | 1.00 |
| Substantive drift (inverse) | 15% | 0.95 (1 defect of 5 medium drifts) | 1.00 |
| Substantive contradiction (inverse) | 15% | 0.85 (3 mediums, 2 fixed in R3) | 0.85 |
| Test mutation-kill | 15% | 0.70 (raw) → 0.85 (post-R3) | 0.85 |

**A's coverage-quant: 0.911** (high mechanical fidelity to spec; few real defects).
**B's coverage-quant: 0.93** (spec is internally complete; under-specifies subclass propagation, env-parsing, and tracking-mechanism for deferrals).

These numbers are nearly tied because the question "which is better as a frame" is structural, not numeric — see §3.

---

## §2 Qualitative Scoring (50% weight) — CEV rubric, dual-pass

Six dimensions × two variants. Position-bias mitigation: pass 1 scores A first; pass 2 scores B first; final = average.

### §2.1 Variant A (implementation diff + 8 commits) — CEV scores

| Dimension | Pass 1 | Pass 2 | Final | Justification |
|---|---|---|---|---|
| Completeness | 0.85 | 0.85 | **0.85** | All 5 patches + 11 tests landed; 4-of-the-22 unimplemented items fixable in-place (X-004, X-006, U-007, MEDIUM-2 env crash); 22 process artefacts deferred. |
| Correctness | 0.90 | 0.85 | **0.875** | Mechanical correctness verified by F-strict-review and invariant probe; 2 HIGH (INV-004/025 PRD subclass) discovered late; ADDRESSED-CONDITIONAL via R3 impl-advocate concessions. |
| Structure | 0.70 | 0.70 | **0.70** | Code structure is tight (+60/-7 LOC budget respected); commit chronology matches spec §8; loses D-NNN traceability and SUPERSEDED audit trail (until TRACEABILITY.md / BEAT_2_BACKLOG.md land R3). |
| Clarity | 0.80 | 0.80 | **0.80** | Code-level docstrings ample; U-003 narrative comment is positive; commit messages are conventional but lack D-NNN refs. |
| Risk Coverage | 0.70 | 0.75 | **0.725** | R-1/R-2/R-3 mitigated mechanically; R-4 covered by T-006; R-5 telemetry partial (`prompt_bytes` covers input not peak heap); R-6 (subclass-propagation) NEWLY DISCOVERED in invariant probe. |
| Invariant & Edge-case Coverage | 0.65 | 0.70 | **0.675** | 14 of 30 invariants pinned by tests; 2 HIGH gaps (INV-004 PRD, INV-025 PRD test) in pre-R3 state, ADDRESSED in R3; 6 MEDIUM gaps (env-parse, file-handle leak on non-OSError, n=0 silent break, etc.); 8 LOW. |

**A qualitative aggregate: 0.770**

### §2.2 Variant B (RECONCILED_DESIGN.md spec) — CEV scores

| Dimension | Pass 1 | Pass 2 | Final | Justification |
|---|---|---|---|---|
| Completeness | 0.90 | 0.90 | **0.90** | 49 KB doc with §1-§11 + appendix; explicit P-NNN, T-NNN, AC-NNN, Risk-NNN, D-NNN, SUPERSEDED, DEFER ledgers. Misses subclass-propagation invariant (R3 concession by spec advocate). |
| Correctness | 0.80 | 0.85 | **0.825** | Spec's `proc.poll()` was wrong (X-005, A corrected); §5 row 5 SIGTERM unconditional assertion ignores race (X-006). Some "After" code blocks have minor format-string typos (`prompt_via=stdin` literal omitted from impl matches spec, but spec under-specified MAX_ARG_STRLEN platform invariants). |
| Structure | 0.95 | 0.95 | **0.95** | Document organization is exemplary: 11 sections + appendix, every P-NNN traces to D-NNN with provenance. Best-in-class spec layout. |
| Clarity | 0.90 | 0.90 | **0.90** | Each P-NNN has Before/After/Why/Acceptance blocks; each T-NNN has mocking strategy + pass/fail criteria. |
| Risk Coverage | 0.80 | 0.75 | **0.775** | R-1..R-6 register in-place; R-2 P0 probe cited with date + claude version. Spec-advocate concedes R3 that "subclass-propagation invariant" was missing from §4 P-004. |
| Invariant & Edge-case Coverage | 0.65 | 0.70 | **0.675** | Spec demanded 11 tests but did not enumerate subclass invariants, env-parse hostility, NUL-byte round-trip, tool_write_mode × BrokenPipe. Half the invariant probe's findings trace to under-specification, not bad implementation. |

**B qualitative aggregate: 0.838**

---

## §3 Combined Scoring + Frame Selection

Combined = 0.5 × coverage-quant + 0.5 × qualitative

| Variant | Coverage-quant | Qualitative | **Combined** |
|---|---|---|---|
| **A (implementation-frame)** | 0.911 | 0.770 | **0.840** |
| **B (spec-frame)** | 0.930 | 0.838 | **0.884** |

### §3.1 Frame interpretation

For this asymmetric run, "base" = the FRAME the merged output uses:

- **A-as-base (implementation-frame)**: merged doc treats the diff as primary; spec becomes a checklist of "remaining items." Reads as "here's what we shipped, here are the gaps."
- **B-as-base (spec-frame)**: merged doc treats RECONCILED_DESIGN.md as primary; walks each P/T/AC/Risk and pins implementation status against it. Reads as "here's what we promised, here's what we delivered."

### §3.2 Which frame serves the user?

The user's literal ask: *"find what I failed to implement and where I drifted."*

- **A-as-base** answers "where I drifted" naturally (drift inventory falls out of the diff narrative) but lights up "what I failed to implement" only weakly (gaps appear as appendices to the diff).
- **B-as-base** answers "what I failed to implement" naturally (every spec item gets a status row) and surfaces "where I drifted" via the U-001..U-016 rows that don't map to any spec item.

**Margin: 5.0% (0.884 vs 0.840).** B-as-base wins.

### §3.3 Tiebreaker (margin = 5.0%, at the threshold)

Per protocol, document tiebreaker if margin < 5%. We sit at the threshold. Tiebreaker: **user-stated goal alignment**. The user's headline question is "what failed to implement" (coverage gap) — B-as-base maximises that. **Selecting B-as-base.**

---

## §4 Selected Frame: B-as-base (spec-frame)

The merged output (`merged-output.md`) walks the spec dimensions:

1. Verdict (single sentence + status)
2. Coverage scorecard (spec items / implemented / drifted / unimplemented)
3. Implemented faithfully (the wins)
4. Real drift / bugs found (the genuine actionable findings)
5. Unimplemented spec items (categorised: must-land / defer / drop)
6. Newly surfaced risks (invariant probe)
7. Drift inventory (A-only items not in B)
8. Comparison to F-strict-review
9. Recommendation (merge-readiness verdict)
10. Provenance map

### §4.1 Why this frame, in one sentence

The user wants to know whether the implementation honours the spec; B-as-base makes that question structurally answerable per item.

### §4.2 What A contributes to the merged output under B-as-base

- Source-of-truth for "implementation status" column on every spec row.
- Drift inventory (§7 of merged output).
- Three legitimate spec corrections (X-005, T-005 18s prelude budget X-002, T-001 stricter ceiling X-003) — A wins these debate points without reframing the merge.

### §4.3 Confidence in frame selection: HIGH

Both advocates' R3 final positions implicitly accept the spec as the contract reference (impl advocate's R3 concedes 13 items routed against spec sections; spec advocate concedes 12 items where the spec was under-specified). The R3 debate already runs in spec-frame.

---

**End of base-selection.md**

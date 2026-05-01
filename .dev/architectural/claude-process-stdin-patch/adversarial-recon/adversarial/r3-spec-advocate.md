# Round 3 — Spec-Advocate Final Position

**Role**: Spec-keeper / QA lead arguing for `variant-2-spec.md` (RECONCILED_DESIGN.md).
**Round**: 3 (final after invariant-probe blocked convergence on 2 HIGH UNADDRESSED items in PrdClaudeProcess.terminate family).

---

## Final Position (1-3 sentences)

The implementation-advocate's R3 remediation for INV-004/INV-025 is mechanically sufficient at the patch level (4-line block + new test file at named file:line) but only because the invariant probe forced the issue into scope; the spec must amend §4 P-004 in a same-PR follow-up to require subclass propagation invariants, and the BEAT_2_BACKLOG.md / TRACEABILITY.md follow-ups must have written owners and a due date, not just "branch author, lands this branch." With those accountability hooks in place the delta closes; without them, the impl-advocate's "lands R3" promises are at risk of evaporating between PR sign-off and merge.

---

## Resolution of HIGH UNADDRESSED Invariants

### INV-004 — `PrdClaudeProcess.terminate()` does not surface `_stdin_error`

**Impl-advocate's R3 proposal**: 4-line block at `src/superclaude/cli/prd/process.py:277` byte-identical to base at `pipeline/process.py:288-291`.

**Verdict: SUFFICIENT at the patch level.** Verified against source: PRD's terminate at `prd/process.py:239-279` is missing the surfacing block; the proposed insertion point (after SIGKILL block at `:281`, before `_close_handles()` at `:279`) is correct.

**However, the spec is also at fault.** RECONCILED_DESIGN.md §4 P-004 specified surfacing only at base-class level and never required "all subclasses overriding `terminate()` MUST replicate or `super().terminate()`." Without that contract, the next subclass override silently regresses the same way. **R3 amendment required**: add to §4 P-004 a subclass-propagation invariant: *"Subclasses overriding `terminate()` MUST either call `super().terminate()` or replicate the `_stdin_error` log block verbatim. Add an invariant test that walks `ClaudeProcess.__subclasses__()` and asserts each override either delegates or contains the log block."*

**Owner**: spec-keeper, separate commit on this branch, paired with INV-004 fix. **Due date**: same PR.

### INV-025 — `PrdClaudeProcess + BrokenPipe + terminate-without-wait` zero test coverage

**Impl-advocate's R3 proposal**: new `tests/pipeline/test_prd_process_stdin.py` with single PRD test using `monkeypatch.setattr(os, "write", _raise_broken_pipe)`.

**Verdict: SUFFICIENT at the patch level, INSUFFICIENT at the contract level.** A parametric test walking `ClaudeProcess.__subclasses__()` would close the gap permanently:

```python
@pytest.mark.parametrize("cls", ClaudeProcess.__subclasses__())
def test_terminate_surfaces_stdin_error_for_all_subclasses(cls, ...):
    # Mock-inject BrokenPipe; assert caplog WARNING contains "stdin_error"
```

Impl-advocate's R3 test pins PRD only; future subclasses (sprint, cleanup_audit if they add terminate overrides) can regress silently. **Owner**: branch author. **Due date**: same PR. Estimated effort: ~30 LOC for a parametrized harness with shared ctor-args fixture.

**Net**: with both amendments (parametric test + spec invariant), HIGH UNADDRESSED items are FULLY ADDRESSED. With only impl-advocate's narrow PRD fix, the immediate regression is fixed but the contract-level gap persists — convergence is conditional.

---

## Sufficiency of Deferral Plan for Unimplemented-B Items

Per-bucket assessment of the 22 "Unique to B unimplemented" items:

- **Lands R3 in-branch** (BEAT_2_BACKLOG.md, TRACEABILITY.md, U-007/X-004/X-006/W-L9/W-L10 fixes): **ACCEPTABLE.** Owner = branch author, due date = pre-merge. Verifiable via `git diff`.
- **Pre-merge PR-comment artefacts** (U-021 D-086 Coder repro, U-029/U-030 test output): **PARTIALLY ACCEPTABLE.** Add a required-status-check blocking merge until PR description contains a checked box `[ ] D-086 338 KB Coder roadmap re-run completed`. Owner: repo admin / CODEOWNERS. Without it, honor system.
- **Operational cross-host** (U-031 §9.2 pipx rebuild): **ACCEPTABLE only if `make ship-coder` lands this branch.** Owner: release-engineer. Due date: within 1 sprint of merge (~7 days).
- **F MEDIUMs folded in** (INV-009 env-var, INV-004 PRD): **ACCEPTABLE.** Both land R3.
- **Residual** (U-017 D-067 CI, U-022 LOC, U-033/U-034 verdict maps, U-036, U-037): **ACCEPTABLE for U-017/U-022/U-036/U-037** (contract-equivalent). **U-033/U-034 require explicit reference**: impl must verify `E-reconciliation-matrix.md` exists at `.dev/architectural/.../reconciliation/E-reconciliation-matrix.md` and link from PR description. Owner: branch author. Due: PR description amendment pre-merge.

---

## Final Concessions

Cumulative:

1. **(R1)** 5 patches landed cleanly (P-001..P-005 match spec).
2. **(R1)** 11 T-NNN tests delivered.
3. **(R1)** A is stricter than B in 3 places (T-001 ceiling, prompt_under_cap, tool_write_mode_false).
4. **(R1)** Code-level drift mostly defensible; only U-007 problematic (lands R3).
5. **(R2)** §10 checklist mixes 4 categories; spec should have separated owners. **Spec gap.**
6. **(R2)** §9.2 cross-host task is out-of-scope; spec should have provided `make ship-coder` skeleton. **Spec gap; impl's R3 proposal accepted.**
7. **(R2)** §3.2 DEFER list named items without tracking mechanism. **Spec gap; BEAT_2_BACKLOG.md closes it.**
8. **(R2)** §11 demanded D-NNN traceability without convention. **Spec under-specified; TRACEABILITY.md closes it.**
9. **(R3 NEW)** §4 P-004 did not specify subclass-propagation invariant; PRD regression-by-omission is partially the spec's fault. **Spec must be amended R3.**
10. **(R3 NEW)** Impl's R3 patches (4-line PRD fix + new test file) are mechanically sufficient for the immediate gap.
11. **(R3 NEW)** "22 unique-to-B unimplemented" headline was count-correct but severity-mis-weighted in R0/R1. The two highest-severity residuals (INV-004 PRD, INV-009 env-var) came from F-strict-review and the invariant probe, NOT the original 22. **Calibration error conceded.**
12. **(R3 NEW)** W-M4 commit-order, W-M11 8th commit, W-L1 18s vs 16s are stylistic / contract-equivalent. Impl's REJECTs are correct. **Spec-advocate withdraws.**

**Total concessions: 12** (R1: 4 + R2: 4 + R3: 4).

---

## Remaining Disagreements

1. **U-033 / U-034 verification.** R2-impl claimed `E-reconciliation-matrix.md` exists with verdicts. **STILL-DISPUTED pending verification**: if file is complete, gap closes via PR-description link; if missing/incomplete, real gap.
2. **W-H1 / U-021 enforcement.** Impl proposes "PR comment." Without CODEOWNERS-required-status-check, artefact is honor-system. **STILL-DISPUTED**: only one is auditable.
3. **W-M10 / U-027 telemetry coverage.** Impl claims `prompt_bytes=N` IS the R-5 telemetry. R-5 was about heap-doubling during encode (full-buffer copy); `prompt_bytes` measures input, not peak heap. **STILL-DISPUTED**: needs `_log.debug("prompt_encode_peak_bytes=%d", peak)` to satisfy R-5's deferral condition.
4. **Subclass-invariant test scope.** Impl's INV-025 test pins PRD only; spec's parametric test walks all subclasses. **STILL-DISPUTED**.
5. **§4 P-004 spec amendment scope.** Spec insists amendment lands this PR; impl would treat as follow-up doc PR. **STILL-DISPUTED**.

---

## Convergence Reassessment

**HIGH UNADDRESSED status (spec-advocate view)**:

- **INV-004**: **ADDRESSED-CONDITIONAL.** Impl's 4-line patch at `prd/process.py:277` is mechanically sufficient. Fully addressed only if parametric subclass test lands and §4 P-004 gets the propagation invariant amendment. Without those, immediate regression is fixed but contract-level gap persists.
- **INV-025**: **ADDRESSED-CONDITIONAL.** Same as INV-004 — narrow PRD test sufficient for this delta; parametric test required for contract closure.

Verdict: HIGH UNADDRESSED items are **conditionally ADDRESSED** — sufficient for this delta to merge, insufficient to prevent recurrence. Spec-advocate accepts narrow-PRD fix as gating threshold and routes parametric coverage + §4 amendment to a same-branch follow-up commit owned by the spec-keeper.

**Final per-bucket counts**:

| Bucket | Count | Items |
|---|---|---|
| ACCEPTED (lands R3 in-branch) | 13 | All impl R3 list: 5 in-place fixes + 2 follow-up MD files + 4 new R3 fixes (INV-009, INV-002, INV-014, NUL-byte test) + INV-004 patch + INV-025 test |
| DEFERRED-WITH-OWNER | 5 | U-021 (release-eng PR-comment), U-031 via `make ship-coder` (release-eng, 1 sprint), parametric subclass test (spec-keeper, same PR), §4 P-004 amendment (spec-keeper, same PR), U-033/U-034 verdict mapping link (branch author, PR description) |
| REJECTED (no fix; conceded) | 5 | W-M4 commit order, W-M11 8th commit, W-L1 18s vs 16s, W-L4 LOC budget, W-L5-L8 stylistic |
| STILL-DISPUTED | 5 | U-033/U-034 verification, W-H1 enforcement mechanism, W-M10 telemetry coverage, subclass-test scope, §4 amendment scope |

**Recommended convergence score**: **0.80**.

Rationale: impl-advocate's R3 patch set covers all in-code residuals with file:line and owner; deferral plan has named owners for operational items; F's MEDIUMs are folded in. Subtracting from 1.0: -0.10 for conditional ADDRESSED on INV-004/INV-025 (parametric test + spec amendment not formally committed to land this PR), -0.05 for U-033/U-034 unverified cross-doc verdicts, -0.05 for W-H1 enforcement remaining honor-system rather than required-status-check.

The 0.05 spread between impl (0.85) and spec (0.80) is the smallest gap of the three rounds — convergence achieved this round; the remaining 0.05 is the conditional-vs-unconditional ADDRESSED status of INV-004/INV-025.

---

**End of r3-spec-advocate.md**

# S6 — Adversarial Debate Transcript

**Solution under review**: `solutions/S6-skip-unfixable-findings.md`
**Reviewer role**: Adversarial / root-cause analyst
**Date**: 2026-05-15
**Verdict (one-line)**: **REFACTOR REQUIRED** — original proposal silently
inverts the meaning of PASS and gives downstream gates a falsely-clean
state. Refactor to a halting `MANUAL_TRIAGE` outcome with an explicit
allowlist of skip-eligible mismatch classes plus an audit trail.

---

## 1. Attacks on the original proposal

### Attack 1a — Downstream gates operate on a falsely-clean state

The proposal demotes ACTIVE -> SKIPPED for the 10 HIGHs lacking
`files_affected`, then lets `execute_fidelity_with_convergence` reach
the `active_highs == 0` branch (`convergence.py:485-499`). That returns
`ConvergenceResult(passed=True, final_high_count=0)`.
`_run_convergence_spec_fidelity` then writes a report with
`high_severity_count: 0`, `validation_complete: true`,
`tasklist_ready: true` (`executor.py:1487-1497`), which causes:

1. **`spec-fidelity` step result**: PASS. `_derive_fidelity_status`
   returns `"pass"` (`executor.py:2554-2570`), not `"degraded"` —
   because `validation_complete: true` is written.
2. **`wiring-verification` (Step 9)**: receives the false-clean
   `spec-fidelity.md` as input (`executor.py:2063`) and may green-light
   wiring obligations that do not exist.
3. **`deviation-analysis` (Step 10)**: receives `spec-fidelity.md` and
   `merge_file` (`executor.py:2074`). With `high_severity_count=0` and
   no body deviations, the analysis output will be empty.
4. **`remediate` (Step 11)**: receives the empty deviation file
   (`executor.py:2084`) and generates a no-op remediation tasklist.
   `remediate.py:265` triggers the "No actionable findings" path.
5. **`certify`**: built dynamically off the (empty) remediation. The
   release certifies as fidelity-clean while the spec genuinely lacks
   coverage of `docs/error-grouping-best-practices`,
   `docs/grouping-algorithm`, both PRD/TDD templates, the
   `{skills,agents}` brace-expansion path, and several NFR primitives
   (`encryption`, `hash`, `<1%`, `<2%`).

**Verdict**: The escape hatch *does* propagate a false-clean signal
through every subsequent gate. Mitigations in the proposal ("highlight
in report", "require user acknowledgement") rely on a human reading the
report — but the pipeline does not stop, so the user has no enforced
checkpoint.

### Attack 1b — Skip-everything attack via a buggy or malicious checker

`merge_findings` in `convergence.py:144-184` always sets
`files_affected = list(f.files_affected) if hasattr(f, 'files_affected')` —
a checker that emits findings without `files_affected` (or worse, sets
it to `[]` deliberately) becomes a kill switch under S6. After run 1:
*every* HIGH gets demoted to SKIPPED, the gate returns PASS, and the
pipeline cheerfully proceeds to certify. The original code is more
robust here: a misbehaving checker still produces ACTIVE findings that
fail the gate, alerting the operator.

The `--no-skip-unfixable` flag does not save us — it defaults *off*
(skip enabled), so the unsafe path is the default.

### Attack 1c — Inverts the meaning of PASS

`SPEC_FIDELITY_GATE` enforces `high_severity_count must be 0` and
`tasklist_ready_consistent` (`gates.py:1248-1259`). The contract is
"zero unresolved HIGH deviations between spec and roadmap." S6 honors
that contract syntactically (the count is zero) while violating it
semantically (10 HIGHs were neither resolved nor judged irrelevant —
they were merely classified as un-actionable by an *external* property:
"the upstream code couldn't compute `files_affected`"). That is a
property of the checker pipeline, not of the deviation, so the
classification is itself unsound.

### Attack 1d — Less destructive variant exists

The current code already supports a clean halting story:
`ConvergenceResult.halt_reason` is propagated as the gate failure
reason (`executor.py:1466`), which preserves PASS=PASS and exposes a
distinct failure mode. A `MANUAL_TRIAGE` outcome with a structured
runbook is strictly better than `passed=True` because:

- Pipeline halts at `spec-fidelity`, exactly the right place
  ergonomically.
- `_format_halt_output` (`executor.py:2117-2147`) already prints a
  retry recipe — the runbook can extend it.
- The deviation registry retains ACTIVE state, so the next manual
  intervention has full provenance.
- Downstream gates never see a fabricated zero count.

The original proposal's escape hatch optimises for "pipeline keeps
moving" at the cost of "the wrong release ships." That is the wrong
trade-off for a fidelity gate.

### Attack 1e — Backdoor for genuine root causes

The 10 HIGHs all originate from a structural checker that emits
finding descriptions like ``"File 'src/x.py:88`' in spec manifest not
found in roadmap"`` — note the trailing backtick and the
`{skills,agents}` brace-expansion artifact. These are *parser bugs* in
`spec_structural_audit.py` / `structural_checkers.py` that S1 (regex
hardening) is designed to fix. S6 hides them so completely that S1's
priority drops to zero — which means the broken parser stays broken
forever and every future spec sprouts the same ghost findings.

---

## 2. Downstream impact trace (evidence)

| Step (executor.py)        | Input                                            | What it assumes about `spec-fidelity.md`                                       |
|---------------------------|--------------------------------------------------|--------------------------------------------------------------------------------|
| 8 spec-fidelity (FR-7)    | spec, merge, tdd, prd                            | Owns the convergence loop and the `passed` flag                                |
| 9 wiring-verification     | merge, **spec-fidelity.md**                      | Trusts the high-severity count when validating wiring obligations              |
| 10 deviation-analysis     | **spec-fidelity.md**, merge                      | Reads body deviations to populate `deviation-analysis.md`; STRICT gate         |
| 11 remediate              | **deviation-analysis.md**, **spec-fidelity.md**  | Generates remediation tasklist from listed findings; honors REMEDIATE_GATE     |
| 12 certify (dynamic)      | remediate output                                 | Produces release certification; assumes deviations are fully resolved/skipped  |

A SKIPPED finding is honored as terminal *only* by the remediate path
(`remediate.py:130`, `remediate_executor.py:554`, `gates.py:247-251`).
That is fine *when remediate itself decides to skip after evaluating
file-affected scopes*. It is **not** fine when the convergence engine
unilaterally retroactively skips findings that were never offered to
remediate, because the deviation-analysis report and the wiring-
verification report are derived from `spec-fidelity.md`, not from the
deviation registry — they will simply not see the skipped findings at
all.

---

## 3. Required refactor (delta vs. original)

| Concern                            | Original S6                          | Refactored S6                                                                    |
|------------------------------------|--------------------------------------|----------------------------------------------------------------------------------|
| Gate outcome                       | PASS (false-clean)                   | `MANUAL_TRIAGE` -> StepStatus.FAIL with structured halt_reason                   |
| Skip eligibility                   | Any HIGH lacking `files_affected`    | Allowlist by `(dimension, mismatch_class)`; default-deny                         |
| Default behavior                   | Skip enabled                         | Skip disabled; opt-in via config + per-class allowlist                           |
| Audit trail                        | Single warning log                   | Append `triage` block to deviation registry; emit `manual-triage.md` companion   |
| Downstream signal                  | `validation_complete: true`          | `validation_complete: false`, dedicated `manual_triage_count` frontmatter field  |
| Operator UX                        | Buried report section                | Dedicated runbook with copy-paste remediation commands                           |
| Defense-in-depth vs. checker bugs  | None                                 | Class allowlist prevents skip-everything attacks                                 |

---

## 4. Confidence assessment

- **Standalone (refactored)**: 70%. Halts at the right place with a
  clear runbook, but it is still a *triage* pathway, not a fix. It
  needs S1 (regex hardening) or S2 (description normalization) to
  actually drive the count to zero.
- **Combined with S1 + S2**: 88%. With root-cause regex fixes upstream,
  the refactored S6 becomes a defense-in-depth net for any residual
  checker bug instead of a primary unblocker.
- **Original proposal, unchanged**: 30%. Ships a falsely-certified
  release; rejected.

---

## 5. References (file:line)

- Convergence pass branch: `src/superclaude/cli/roadmap/convergence.py:485-499`
- SKIPPED status semantics: `src/superclaude/cli/roadmap/models.py:16,27`
- Convergence report writer: `src/superclaude/cli/roadmap/executor.py:1479-1506`
- Pipeline step ordering 8-12: `src/superclaude/cli/roadmap/executor.py:2039-2087`
- Fidelity status derivation: `src/superclaude/cli/roadmap/executor.py:2554-2570`
- SPEC_FIDELITY_GATE contract: `src/superclaude/cli/roadmap/gates.py:1248-1259`
- Remediate honors SKIPPED: `src/superclaude/cli/roadmap/remediate.py:129-132,197,226-232`
- Halt formatting: `src/superclaude/cli/roadmap/executor.py:2117-2147`
- Deviation registry / `files_affected` empty for all 10 HIGHs:
  `.dev/releases/current/task-builder-merge/roadmap/deviation-registry.json`

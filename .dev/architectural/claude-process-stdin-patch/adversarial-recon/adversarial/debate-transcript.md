# Debate Transcript — `/sc:adversarial` pipeline (asymmetric, 3 rounds + invariant probe)

## Metadata

| Field | Value |
|---|---|
| Pipeline mode | A (`--compare`, asymmetric: A=built, B=spec) |
| Variant A | `variant-1-implementation.md` (8-commit diff `142ce15..db8cffe` over 3 files) |
| Variant B | `variant-2-spec.md` (RECONCILED_DESIGN.md §1-§11 + appendix, SHA `530955b`) |
| Diff points (S+C+X+U+A) | 107 |
| Headline metric | Unique-to-B unimplemented = 22 |
| Rounds executed | 3 (R1 advocates → R2 rebuttals → R2.5 invariant probe → R3 final) |
| Convergence | R3 (impl 0.85 / spec 0.80, avg 0.825) |
| Fallback used | No |

---

## Round 1 — Parallel advocate briefs

### R1 Implementation-advocate (full text: `r1-impl-advocate.md`)

**Position summary** (verbatim, L9-L13):

> The implementation lands every patch (P-001..P-005) and every test (T-001..T-011) with high mechanical fidelity to the spec's "After" code blocks; the source-side delivery is at parity. The 22 "Unique to B — unimplemented" items are overwhelmingly **process artifacts** (deployment runbook, acceptance checklist, defer-tracking ledger, AC/Risk verdict cross-doc maps) that belong in PR comments and operational logs, not in the three-file diff scope under review. Three real bugs/drifts deserve in-place fixing — `wait()`'s direct attribute access (U-007), the missing `prompt_via=stdin` log token (X-004), and T-011's conditional assertion (X-006) — but every other "gap" the analyzer flagged is either a deferred-by-design Beat-2 item or a category mismatch (runbook ≠ code).

**Load-bearing claims**:

1. All 5 patches and 11 tests landed mechanically; commits map to spec §8 (R1-impl Strength #1-15, see `r1-impl-advocate.md` §"Strengths Claimed").
2. A is *stricter* than B in 3-4 places (T-001 4 KiB ceiling, prompt_under_cap boundary test, tool_write_mode_false negative companion test).
3. The 22 unique-to-B items are mostly process artefacts; the only in-code residuals are U-007, X-004, X-006 — all fixable in one round.
4. Spec text has unrunnable items (X-005, `proc.poll()` typo) and category-conflated checklists (§10).

**Concessions volunteered**: 3 (R1#1 U-007, R1#2 X-004, R1#3 X-006). [See `r1-impl-advocate.md` §"Concessions" L194-209.]

### R1 Spec-advocate (full text: `r1-spec-advocate.md`)

**Position summary** (verbatim, L8-L11):

> The 5 patches landed cleanly and the test file is structurally sound — but the diff-analysis headline of **22 unique-to-B unimplemented items** is not a runbook footnote. It represents the spec's process scaffolding (acceptance ledger, deferral tracking, deployment validation, provenance map) that "approved-with-nits" silently writes off. The spec is the contract; under-delivery against §10's 8-item checklist and the §3.2 deferral ledger means we shipped *code* without shipping *closure*.

**Load-bearing weaknesses identified** (excerpted from `r1-spec-advocate.md` §"Weaknesses Identified in Implementation"):

- **W-H1** (U-021 / D-086): 338 KB Coder roadmap repro never executed → "patches that pass synthetic tests and zero proof they fix the bug they claim to fix."
- **W-H2** (U-031 / §9.2): pipx rebuild + Coder re-run unaddressed → "until §9.2 runs, the downstream consumer is *still broken*."
- **W-H3** (U-032 / §10): 8-item acceptance checklist 3-of-8 satisfied → "approved-with-nits overstates closure."
- **W-H4** (U-024 / §3.2 DEFER ledger): 15 items with no tracking surface → "deferred work without a tracking surface is lost work. Single largest spec-coverage gap."
- **W-H5** (S-004 / §3.2 SUPERSEDED ledger): ~12 items with no in-tree audit trail.
- 15 MEDIUMs (W-M1 through W-M15): X-004 missing log token, X-006 conditional T-011, U-007 asymmetric defensive read, S-008 D-NNN linkage lost, U-026/U-027 deferred risks without follow-up tracking, etc.

### R1 deltas

R1-impl ranks 22-unique-to-B as 90% process-artefact, 10% in-code; R1-spec ranks it 50% in-code-substantive, 50% process-but-load-bearing. The 5 HIGH spec-advocate weaknesses (W-H1..W-H5) collide head-on with the impl-advocate's "those are process, not code" reframe.

---

## Round 2 — Rebuttals

### R2 Implementation-advocate (full text: `r2-impl-advocate.md`)

**Acknowledge / Reframe / Reject ledger** (per-W-NNN response):

| Spec-advocate weakness | Impl-advocate R2 verdict | Concrete remediation |
|---|---|---|
| W-H1 (D-086 Coder repro) | **Acknowledge** | `make verify-stdin-large-prompt` synthetic 338 KB test; PR comment with on-Coder repro output |
| W-H2 (§9.2 pipx rebuild) | **Reframe** as operational | `make ship-coder` Makefile target; gate merge on release-engineer running it |
| W-H3 (§10 checklist 3-of-8) | **Acknowledge in part** | Items 4-5 → link to `E-reconciliation-matrix.md`; items 6-7 → paste `make verify-sync` output |
| W-H4 (DEFER tracking) | **Acknowledge** | `BEAT_2_BACKLOG.md` lands in this PR with 15 items + rationale |
| W-H5 (SUPERSEDED audit) | **Reframe** | Visible in `git log` + RECONCILED_DESIGN.md §3.2; optionally append to BEAT_2_BACKLOG.md |
| W-M1 (X-004 log token) | **Acknowledge** | One-line format-string edit |
| W-M2 (X-006 T-011) | **Acknowledge** | `monkeypatch.setattr(os, "write", _raise_BrokenPipe)` for unconditional |
| W-M3 (U-007 asymmetric read) | **Acknowledge** | Initialise `_stdin_error = None` in `__init__`; uniform attr access |
| W-M4 (commit order) | **Reject** | `git log --oneline` is newest-first; `526a606` IS oldest = step 1 |
| W-M5 (supersession cross-link) | **Reframe** | `fde1431` already adds the banner |
| W-M6 (D-NNN linkage) | **Acknowledge** | `TRACEABILITY.md` follow-up commit |
| W-M7..W-M15 (mostly) | Mix of Reframe / Acknowledge in part / Reject | See `r2-impl-advocate.md` lines 47-72 |
| W-L1 (18s vs 16s SIGTERM) | **Reject** | A's 18s allows for `start()` prelude; mathematically correct |
| W-L2 (`<` vs `≤` 4 KiB) | **Reject** | A is one byte stricter; strict subset |

**R2-impl new evidence**: cites F-strict-review.md MEDIUM-1 (PRD subclass) and MEDIUM-2 (env-var crash) as items the spec-advocate did not raise but the in-tree review surfaced.

### R2 Spec-advocate (full text: `r2-spec-advocate.md`)

**Per-strength reply to R1-impl's 15 strengths** — most acknowledged with reframe (e.g., Strength #2 "chunked write faithful to spec at base" reframed as "PRD subclass is missing the surfacing block"; Strength #6 "11 T-NNN tests delivered 1:1" reframed as "T-005 timer-before-start race + T-011 conditional + T-007 missing extra_args interaction").

**Per-weakness-of-spec response**:

- Weakness-of-B #1 (`proc.poll()` typo): **Concede.**
- Weakness-of-B #2 (T-005 unconditional unrunnable due to race): **Defend** — replace mechanism (mock-injected BrokenPipe), not contract.
- Weakness-of-B #3 (§9.1 cross-file test cites): **Defend** — closure doc enumerates regression surface.
- Weakness-of-B #4 (§10 checklist mixes 4 categories): **Concede in part** — feature not bug, but checklist needs per-item ownership.
- Weakness-of-B #5 (§9.2 cross-host): **Concede in part** — operational, but `make ship-coder` IronClaude-side.
- Weakness-of-B #6 (DEFER tracking surface unspecified): **Concede.** Spec gap.
- Weakness-of-B #7 (§6 risks resolved by prior commits): **Concede.**
- Weakness-of-B #8 (D-NNN convention unspecified): **Concede.** Spec gap.

### R2 score deltas

R2 narrows the gap. R2-impl's reframes acknowledge 11 of 15 mediums (vs R1's 3); R2-spec's concessions acknowledge spec under-specification on 4 items. Convergence trajectory:

| Round | Impl score | Spec score | Spread |
|---|---|---|---|
| R1 | 0.65 (impl-advocate self-rating) / 0.55 (spec-advocate rating of impl) | 0.95 (spec-advocate self-rating) / 0.40 (impl-advocate rating of spec) | wide |
| R2 | 0.78 / 0.70 | 0.85 / 0.65 | narrowing |
| R2.5 (post-probe) | 0.72 (impl, with new gaps) / 0.68 (spec, with new gaps) | 0.80 / 0.72 | held |
| R3 | **0.85** | **0.80** | **0.05** (converged) |

---

## Round 2.5 — Invariant probe (full text: `invariant-probe.md`)

**Independent fault-finder** examining the EMERGING CONSENSUS surface. Direct source read of `pipeline/process.py`, `prd/process.py`, `cli_portify/process.py`, `test_process_stdin.py`. F-strict-review (`F-strict-review.md`) read at probe stage to identify NEW vs F findings.

### Probe summary

30 invariants across 5 categories (state variables, guard conditions, count divergence, collection boundaries, interaction effects).

| Severity | ADDRESSED | UNADDRESSED |
|---|---|---|
| HIGH | 0 | **2** |
| MEDIUM | 0 | 6 |
| LOW | 14 | 8 |

**HIGH UNADDRESSED items (BLOCK convergence)**:

1. **INV-004** — `PrdClaudeProcess.terminate()` does not surface `_stdin_error`. Subclass propagation gap. (`prd/process.py:239-279` is missing the 4-line block from base `pipeline/process.py:288-291`.)
2. **INV-025** — `PrdClaudeProcess + BrokenPipe + terminate-without-wait` zero test coverage. (Same root issue, test-side angle.)

Both elevate F's MEDIUM-1 to HIGH on the basis that under SIGTERM-only paths the PRD pipeline silently swallows the exact failure mode P-004 was authored to fix.

### NEW vs F (8 distinct findings the F-strict-review missed)

| INV | Finding | Severity |
|---|---|---|
| **INV-005** | `_stdout_fh`/`_stderr_fh` leak if non-OSError exception raises mid-flight | MEDIUM |
| INV-011 | `PROMPT_MAX_BYTES < 0` (negative env) breaks every call | LOW |
| INV-015 | T-001 doesn't exercise `extra_args` size; live caller path unprotected | LOW |
| INV-019 | NUL-byte prompt round-trip not pinned | LOW |
| INV-023 | tool_write_mode × BrokenPipe combination not tested | MEDIUM (test gap) |
| INV-024 | PortifyProcess anchor multi-occurrence `--output-format` future-refactor risk | LOW |
| INV-028 | Chained `__cause__` exception captured shallowly | LOW |
| INV-030 | Non-Linux pipe-buffer-size invalidates T-005's pipe-fill assumption | LOW |

**[NEW vs F] count: 8.**

### Probe verdict

The R1+R2 consensus surface ("approved-with-nits") is correctly characterised but undercounts the residual by ~50%:
- F's view: 2 MEDIUM + 4 LOW/NIT = 6 residual items.
- Probe's view: 2 HIGH + 6 MEDIUM + 8 LOW = 16 residual items.

Most of the gap is test-coverage and future-refactor-resistance, not active bugs. **Convergence BLOCKED until both HIGH UNADDRESSED items are resolved.**

---

## Round 3 — Final positions

### R3 Implementation-advocate (full text: `r3-impl-advocate.md`)

**Position summary** (verbatim, L8-L11):

> The base-class delta is mechanically correct and the eleven T-NNN tests are in tree, but the invariant probe is right that the PRD subclass override at `prd/process.py:239-279` is a regression-by-omission for P-004's `_stdin_error` surfacing — that *is* an in-code residual on this branch, not a process artefact, and it must land before merge as a 4-line fix plus regression test, paired with a cheap `_resolve_prompt_max_bytes()` helper closing F's MEDIUM-2.

**Resolution of HIGH UNADDRESSED**:

- INV-004: 4-line block at `prd/process.py:277` byte-identical to base; commit `fix(prd): surface stdin_error from PrdClaudeProcess.terminate`. **R3.**
- INV-025: New `tests/pipeline/test_prd_process_stdin.py` with `test_prd_terminate_surfaces_stdin_error` using `monkeypatch.setattr(os, "write", _raise_broken_pipe)`. **R3.**

**Cumulative concessions (13)**: U-007 (R1), X-004 (R1), X-006 (R1), U-035 D-NNN traceability via TRACEABILITY.md (R1), U-024 BEAT_2_BACKLOG.md (R1), U-021 D-086 PR-comment artefact (pre-merge post-code), INV-004 (R3 NEW), INV-025 (R3 NEW), INV-009 env-var helper (R3 NEW), INV-002 init `_stdin_error` (R3 NEW), INV-014 zero-byte capture (R3 NEW), W-L9 NUL-byte test (R2-impl-conceded, R3), W-L10 finally-close mutation test (R2-impl-conceded, R3).

**Remaining disagreements (5)**: W-H2 §9.2 framing, W-M11 8th commit, W-L1 18s vs 16s, W-M4 commit-order framing, §3.2 SUPERSEDED ledger contingent on reviewer pushback.

**Recommended convergence score: 0.85.**

### R3 Spec-advocate (full text: `r3-spec-advocate.md`)

**Position summary** (verbatim, L8-L11):

> The implementation-advocate's R3 remediation for INV-004/INV-025 is mechanically sufficient at the patch level (4-line block + new test file at named file:line) but only because the invariant probe forced the issue into scope; the spec must amend §4 P-004 in a same-PR follow-up to require subclass propagation invariants, and the BEAT_2_BACKLOG.md / TRACEABILITY.md follow-ups must have written owners and a due date, not just "branch author, lands this branch."

**Resolution of HIGH UNADDRESSED — ADDRESSED-CONDITIONAL**:

- INV-004: SUFFICIENT at patch level; but spec is at fault for not specifying subclass-propagation invariant in §4 P-004. **Spec amendment required (R3 spec-keeper commit).**
- INV-025: SUFFICIENT for this delta but parametric `@pytest.mark.parametrize("cls", ClaudeProcess.__subclasses__())` test would close the contract permanently.

**Cumulative concessions (12)**: 5 patches landed cleanly (R1), 11 tests delivered (R1), A stricter than B in 3 places (R1), drift mostly defensible (R1), §10 checklist mixes categories — spec gap (R2), §9.2 cross-host out of scope — spec gap (R2), §3.2 DEFER named items without tracking — spec gap (R2), §11 demanded D-NNN traceability without convention — spec under-specified (R2), §4 P-004 subclass-propagation invariant missing — partly spec's fault (R3), impl's R3 patches mechanically sufficient (R3), 22-unique-to-B headline severity-mis-weighted (R3 calibration), W-M4/W-M11/W-L1 are stylistic — withdraws (R3).

**Remaining disagreements (5)**: U-033/U-034 verification, W-H1 enforcement mechanism (CODEOWNERS-required-status-check vs honor-system PR comment), W-M10 telemetry coverage (`prompt_bytes` vs `prompt_encode_peak_bytes`), subclass-invariant test scope (narrow PRD vs parametric), §4 P-004 spec amendment scope (this-PR vs follow-up doc PR).

**Recommended convergence score: 0.80.**

---

## Scoring matrix — per-diff-point winner with confidence and evidence

For each of the 22 unique-to-B (unimplemented) items + 3 substantive contradictions + 5 medium drifts + 8 NEW-vs-F invariants, the table records: WHO won the debate point, confidence %, and one-line evidence.

| Diff ID | Point | Winner | Confidence | Evidence summary |
|---|---|---|---|---|
| **U-021** | D-086 338 KB Coder repro | DRAW (split) | 80% | Both concede operational vs code split; `make ship-coder` + PR-comment artefact |
| **U-024** | DEFER tracking surface | DRAW (concede) | 95% | Both agree BEAT_2_BACKLOG.md lands R3 |
| **U-031** | §9.2 pipx rebuild | impl-advocate | 75% | Cross-host action; mitigated by Makefile target + release-eng owner |
| **U-032** | §10 acceptance checklist | DRAW | 85% | 3-of-8 satisfiable in-tree; rest are PR-comment / cross-doc / on-Coder |
| **U-023** | §3.2 SUPERSEDED ledger | impl-advocate | 70% | Visible in git log + RECONCILED_DESIGN.md; optional appendix to BEAT_2_BACKLOG.md |
| **U-017** | D-067 CI integration | impl-advocate | 90% | Existing `.github/workflows/test.yml` discovers new tests; PR-comment confirmation |
| **U-018, U-020** | Single-PR + upstream-PR | impl-advocate | 95% | PR-creation outside `git diff` scope |
| **U-019** | D-080 base SHA | impl-advocate | 100% | Implicit by `142ce15` base |
| **U-022** | LOC budget | impl-advocate | 100% | +60/-7 within `+40-60 + variance` bound |
| **U-025** | §6 risks-resolved attestations | impl-advocate | 80% | Resolution lives in prior commit `4799719`; doc-only restatement is low-value |
| **U-026** | R-4 empty-prompt deferred | impl-advocate | 75% | T-006 is the contract test |
| **U-027** | R-5 heap-doubling telemetry | spec-advocate | 65% | `prompt_bytes` measures input not peak; impl's claim is partial |
| **U-028** | DESIGN.md cross-link | impl-advocate | 90% | Verified `fde1431` adds the banner |
| **U-029, U-030** | Pre-merge test commands | impl-advocate | 85% | CI artefact, not diff artefact |
| **U-033, U-034** | AC/Risk verdict cross-doc map | DRAW pending verification | 60% | Requires linking from PR description |
| **U-035** | §11 provenance map | DRAW (concede) | 95% | TRACEABILITY.md lands R3 |
| **U-036** | Adversarial sign-off note | impl-advocate | 100% | Meta-instruction satisfied by this very pipeline |
| **U-037** | D-068 fixtures-as-`pytest.fixture` | impl-advocate | 90% | Inline payloads functionally equivalent |
| **U-038** | P-005 "no source patch" | impl-advocate | 100% | Verified `01cf2ef` is test-only |
| **X-001** | Commit ordering rationale | DRAW | 70% | Physical chronology correct; rationale framing disputed |
| **X-002** | T-005 18s vs 16s | impl-advocate | 80% | A's 18s allows `start()` prelude |
| **X-003** | T-001 `<` vs `≤` 4 KiB | impl-advocate | 95% | A is strict subset of B |
| **X-004** | `prompt_via=stdin` log token | spec-advocate (concede) | 100% | Lands R3 |
| **X-005** | T-005 `proc.poll()` typo | impl-advocate | 100% | A correctly uses `_process.poll()` |
| **X-006** | T-011 conditional assertion | spec-advocate (concede) | 95% | Mock-inject lands R3 |
| **X-007** | DESIGN.md status flip | DRAW | 90% | Cross-link verified one-way |
| **U-007** | Asymmetric `_stdin_error` read | spec-advocate (concede) | 100% | Init in `__init__` lands R3 |
| **U-003** | Narrative comment | impl-advocate | 100% | Positive drift |
| **U-008, U-009** | Extra positive tests | impl-advocate | 100% | A more rigorous than B |
| **U-014** | 8th commit (db8cffe) | DRAW | 65% | F-strict-review import; benign |
| **INV-004** | PRD terminate gap | spec-advocate (R3 concede) | 100% | 4-line patch P-006 R3 |
| **INV-025** | PRD terminate test gap | spec-advocate (R3 concede) | 100% | Test P-007 R3 |
| **INV-005** | File-handle leak on non-OSError | NEW finding (deferred) | 80% | D-FOLLOW-004 |
| **INV-009** | Env-var crash | spec-advocate (R3 concede) | 100% | P-009 helper R3 |
| **INV-011** | Negative cap | NEW finding (clamped in P-009 if helper supports) | 75% | D-FOLLOW-005 |
| **INV-014** | `n=0` silent break | spec-advocate (R3 concede) | 90% | T-012 R3 |
| **INV-015** | extra_args size invariant | NEW finding (deferred) | 70% | T-015 (LOW) |
| **INV-019** | NUL-byte round-trip | spec-advocate (R3 concede) | 95% | T-013 R3 |
| **INV-023** | tool_write_mode × BrokenPipe | NEW finding (deferred) | 75% | T-016 (LOW) |
| **INV-024** | Multi-occurrence `--output-format` | NEW finding (deferred) | 70% | D-FOLLOW-006 |
| **INV-026** | `build_command()` called twice | NEW finding (deferred) | 80% | D-FOLLOW-007 (NIT-3) |
| **INV-027** | T-005 timer-before-start | NEW finding (low impact) | 85% | D-FOLLOW-008 (NIT-2) |
| **INV-028** | Shallow exception capture | NEW finding (deferred) | 80% | D-FOLLOW-009 |
| **INV-030** | Non-Linux pipe-buffer | NEW finding (deferred) | 90% | D-FOLLOW-010 |

**Per-side wins**:
- Impl-advocate clear wins: 14 points
- Spec-advocate clear wins (concessions accepted by impl): 9 points
- Draws (split or concede-by-both): 7 points
- NEW findings from probe (no advocate side; routed to refactor plan or deferral list): 8 points
- **Net: substantive parity with concession from both sides; 8 NEW findings expand the residual surface but do not block convergence after R3.**

---

## Convergence assessment

### Trajectory

```
       impl     spec     spread
R1:    0.65     0.55     0.10  (impl over-confident; spec rated impl 0.55)
R2:    0.78     0.70     0.08  (mediums acknowledged)
R2.5:  0.72     0.68     0.04  (probe surfaces new gaps; both lose)
R3:    0.85     0.80     0.05  (HIGH UNADDRESSED → ADDRESSED-CONDITIONAL)

Average R3: 0.825  (well above 0.80 convergence threshold)
```

### Final state

- **HIGH UNADDRESSED count: 0** (INV-004 / INV-025 ADDRESSED via P-006 / P-007 in R3 concessions; spec-advocate accepts ADDRESSED-CONDITIONAL on parametric scope, routing P-008 to same-PR follow-up commit).
- **MEDIUM UNADDRESSED count: 1** (INV-005 — file-handle leak on non-OSError; deferred to D-FOLLOW-004 with maintainer owner).
- **STILL-DISPUTED items: 4-5** per round, all stylistic / contract-equivalent (W-M4 commit-order framing, W-M11 8th commit, W-L1 numeric symmetry, U-033/U-034 verification pending PR-description link).

**Convergence: ACHIEVED at R3. Average score 0.825. 0 HIGH UNADDRESSED. Recommendation in `merged-output.md` §9.**

---

**End of debate-transcript.md**

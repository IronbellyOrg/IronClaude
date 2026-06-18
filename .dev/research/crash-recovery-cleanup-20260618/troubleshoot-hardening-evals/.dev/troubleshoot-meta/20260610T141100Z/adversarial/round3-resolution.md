# Round 3 — Consensus-Remediation Resolution (BLIND, neutral resolver)

All citations verified against git + disk on 2026-06-10. This is the binding reconciliation the merge MUST use. It resolves the 4 HIGH-severity UNADDRESSED items from `invariant-probe.md` (INV-001, INV-006, INV-007, INV-008) plus the dependent MEDIUM items (INV-002, INV-009, INV-012, INV-016).

---

## A. INV-001 + INV-006 — Canonical Crosswalk (one table, nothing orphaned or overloaded)

### A.1 GATE-0 canonical family definitions (verbatim from `GATE-0.md:24-28`)

- **E1 — PRD cloud `--file` misuse.** Headless `superclaude prd run --spec` crashlooped at `scope-discovery` because PRD passed local filesystem paths to Claude CLI `--file` (a cloud-download/session-token mechanism). **This is the `--file`/cloud-file-misuse bug.** (GATE-0:24)
- **E2 — final completion phase false positive.** STRICT `parallel_instructions` gate halted a live PRD build-task-file run because the final sequential completion Phase 7 lacked parallel keywords. (GATE-0:25)
- **E3 — Task-Log findings-heading sibling false positive.** After #154, the same STRICT gate halted again on loose phase-heading matching of Task-Log placeholders like `### Phase 2 - Codebase Research Findings`. (GATE-0:26)
- **E4 — PRD/generic/trailing evaluator divergence.** `parallel_instructions` was made advisory in the generic `gate_passed`, but normal PRD runtime uses `PrdExecutor._evaluate_gate`, which ignores `SemanticCheck.advisory` and still treats any non-True check as fatal. **E4 = evaluator/gate-divergence.** (GATE-0:27)
- **E5 — POST-reflect wrong diff base.** Generated POST-reflect used `--diff <start_commit>..HEAD`; with uncommitted work it audited nothing, with foreign commits it audited foreign work. (GATE-0:28)

### A.2 Crosswalk (one line per canonical family)

| Canonical E# | GATE-0 definition | A M-instances | B items | defect-table row(s) | source-of-record | fix status |
|---|---|---|---|---|---|---|
| **E1** | PRD cloud `--file` misuse (`scope-discovery` crashloop) | M1 | M1 | **PRD-E04** | defect-table PRD-E04 + GATE-0:24 | **MERGED** #151 `7601ad25` (on master) |
| **E2** | final completion-phase false positive | M2 (+ **F-A** primitive instance) | M2 + **M7** (=F-A) | **PRD-E05** | defect-table PRD-E05 + GATE-0:25 | **MERGED** #154 `e97aa4fd` (on master) |
| **E3** | Task-Log findings-heading sibling false positive | M3 | M3 | **PRD-E06** | defect-table PRD-E06 + GATE-0:26 | **MERGED** #155 `eb9a2633` (on master) |
| **E4** | PRD/generic/trailing evaluator divergence | M4 (+ **M6** resume-ID, same contract-identity class) | M4 (+ M6) | **NONE** (no table row) — sourced from `contract-implementations.md` exec finding lines 14-19 | **`contract-implementations.md`** (GATE-0:27 evidence col) | **COMMITTED-but-UNMERGED** `b97c9960` on `origin/fix/prd-executor-advisory-gate` (NOT on master); M6/resume-ID divergence still LIVE on master, no fix |
| **E5** | POST-reflect wrong diff base | (carried as the reflect trap; A scores it under reflect) | (reflect trap) | **REFLECT-E01** | defect-table REFLECT-E01 + GATE-0:28 | **MERGED** #153 `10723863` (on master) |
| *(out of scope)* | pre-episode PRD/reflect history | — | — | **PRD-E01, PRD-E02, PRD-E03, REFLECT-E02, REFLECT-E03** | defect-table (forensic appendix) | MERGED earlier (#140/#147/#149/#142/#144); deliberately OUTSIDE the frozen E1–E5 window |
| *(rider, NOT a miss)* | commit-scope/bisection hygiene | F-B | — | — | `e97aa4fd` 3rd commit (`docs(auggie-review)`, "Out of scope for PR #154 … bundled per request") | excluded from prevention denominator |

### A.3 Explicit resolutions

- **(a) E4's missing table row.** CONFIRMED: the 9-row `defect-escape-table.md` has NO E4 row. Its rows are PRD-E01..E06 + REFLECT-E01..E03 (verified: `grep -cE '^\| (PRD-E0[0-9]|REFLECT-E0[0-9])' = 9`). E4 (evaluator divergence) is documented ONLY in **`contract-implementations.md`** (executive finding lines 14-19; runtime call chain lines 20-29; candidate `EC-A2-001` line 143), which GATE-0:27 cites as E4's evidence column. **Binding rule: the E↔table reconciliation is 4-of-5, not 5-of-5. E4 is sourced from the contract map, not the escape table. The merge MUST NOT call the 9-row table "the appendix of all 5 families" — it is the appendix of 4 (E1/E2/E3/E5) plus 5 out-of-window rows; E4 lives in `contract-implementations.md`.**
- **(b) "E4" vs "PRD-E04" name collision.** These are DIFFERENT escapes. GATE-0's `E4` = evaluator-divergence (`_evaluate_gate` vs `gate_passed`). The table's `PRD-E04` = the `--file` cloud-flag bug, which maps to canonical **E1**. A naive reader who maps "E4 → PRD-E04" is wrong. **Binding rule: never abbreviate canonical families as "E0x"; always write `E1..E5` (GATE-0 family) distinct from `PRD-E0x`/`REFLECT-E0x` (table rows). E1=PRD-E04, E2=PRD-E05, E3=PRD-E06, E5=REFLECT-E01, E4=no row.**
- **(c) Which canonical family the `--file` bug belongs to.** **E1** (GATE-0:24, table row PRD-E04). Not E4.
- **59% / 41% denominator.** Source line verified: `theatre-vs-value-scorecard.md:5` reads "**Estimated net defect-catching value: 41% value / 59% theatre or mis-targeted ceremony.**" This is a **blended mean of four per-stage value/ceremony judgements** (scorecard:13-16: troubleshoot 52/48, task-builder 35/65, reflect 40/60, QA 35/65), **NOT computed on E1–E5 or any escape count.** It is denominator-independent (confirms INV-003). **Binding rule: label 59%/41% as a qualitative per-stage value-blend, NEVER as an "X of 5 escapes caught" rate.**

---

## B. INV-007 + INV-008 + INV-016 — The 3-Bucket Committed/Unbuilt Ledger (git-verified)

| Bucket | Item | Git verification |
|---|---|---|
| **UNBUILT (spec-only, halted at G1)** | H0–H5 troubleshoot hardening / wave mechanisms / `--pipeline-health` / contract-ledger automation in `sc-troubleshoot-protocol/SKILL.md` + `commands/troubleshoot.md` | `git diff --stat 94d5baa0..master` on both files = **EMPTY (zero changes since base)**. SKILL.md last commit = `022bccee` (#116, 2026-06-02); troubleshoot.md last = `73d49c00` (#73). `grep` for `pipeline-health` / `H0 —` / `Reachable STRICT` / `Patched-Shadow` in the skill dir = **NONE FOUND**. |
| **COMMITTED + MERGED to master** | E1 ← #151 `7601ad25`; E2 ← #154 `e97aa4fd`; E3 ← #155 `eb9a2633`; E5 ← #153 `10723863`. (Plus pre-episode PRD-E03 ← #149 `f131592f`.) | `git merge-base --is-ancestor` returns **ON master** for all of `7601ad25`, `e97aa4fd`, `eb9a2633`, `10723863`, `f131592f`. |
| **COMMITTED but UNMERGED** | E4 advisory-gate fix `b97c9960` (`fix(prd): honor advisory checks in the executor's _evaluate_gate (live PRD path)`) | `git merge-base --is-ancestor b97c9960 master` = **NOT on master**. `git branch -a --contains b97c9960` = **`remotes/origin/fix/prd-executor-advisory-gate`** only. |

**The single honest one-sentence claim (replaces both "nothing was fixed" AND "the refactor is validated"):**

> The five canonical product escapes were individually point-fixed in shipped PRs (E1/#151, E2/#154, E3/#155, E5/#153 merged to master; E4's fix `b97c9960` committed but unmerged on `origin/fix/prd-executor-advisory-gate`), while the generalized troubleshoot-protocol hardening (H0–H5 / pipeline-health) is pure spec, unbuilt, and halted at G1 — so neither "nothing was fixed" nor "the refactor is validated" is true.

**INV-016 resolution.** E4 is NOT purely "spec-only awaiting G1": its product fix `b97c9960` already exists, one merge away, outside the G1 scope. The G1 halt governs ONLY the meta-hardening spec; it does not block E4's product remediation. The merge must not imply E4 is blocked on G1.

---

## C. INV-012 — M6 Attribution Correction (fresh read + blame)

- **M6 = contract-identity divergence**, current exact lines (fresh read 2026-06-10):
  - `src/superclaude/cli/prd/executor.py:259` → `"research-qa": "qa/qa-research-gate-report.md",`
  - `src/superclaude/cli/prd/config.py:30` → `r"|analyst-completeness|qa-research-gate"` (the `_STEP_ID_PATTERN` alternation; `research-qa` is **absent** from it).
- **True introducing commits (via `git blame`):**
  - executor.py:259 → **`27962ddb2`** (Ironbelly, 2026-05-22).
  - config.py:30 → **`09e2ccc0d`** (Alireza, 2026-04-13).
  - **Neither is #149 / `f131592f`.** The probe is correct; variant-C's "committed, last touched #149" conflates whole-file mtime with line provenance. **Correct attribution: the two divergent lines were written by `27962ddb2` and `09e2ccc0d` respectively.**
- **Is M6/E4 live on master right now?** The **M6 resume-ID divergence is LIVE on master** (both lines present; producer emits `research-qa`, resume `_STEP_ID_PATTERN` validates `qa-research-gate`, no match — genuine producer/validator mismatch, no fix committed anywhere). The **E4 advisory-gate divergence is also live on master** (its fix `b97c9960` is unmerged). M6 and E4 are DIFFERENT contract divergences in DIFFERENT files/lines (M6 = resume step-ID regex in config.py; E4 = `_evaluate_gate` advisory handling in executor.py); per INV-015 they must be SEPARATE ledger rows under the E4 contract-identity *class*, never collapsed into one entry.

---

## D. INV-009 — The Binding Relabel Rule (cell-level, enforceable)

**Rule (sentence 1):** Every cell of any would-have-caught matrix or theatre scorecard imported from variant-A or variant-B MUST be stripped of every run-result token — all coverage counts (`8/8`, `7/7`, `33`, `16`), all percentages presented as measured catch-rates (`100%`, `6.25%`, `3.0%`, `97%`), all round references (`round 2`), and all retrospective catch markers (`✓ caught`, "the replay confirms", "did_catch") — because these assert an execution that git proves never happened (the protocol files are unchanged since base; no replay ran).

**Rule (sentence 2):** Every predicted cell MUST instead carry the literal token **`NOT YET PROVEN (pre-build)`**, and the matrix header relabel ("predicted/pre-build coverage, backtest post-G1") is INSUFFICIENT on its own — a header that says "predicted" over a cell body that still reads "✓ caught at round 2" still fabricates.

**Falsifier condition (proves a cell still over-asserts):** if ANY single cell — after relabel — retains a numeric coverage count, a percentage framed as an achieved catch-rate, a round number, or a ✓/"caught"/"did_catch" token without an accompanying `NOT YET PROVEN (pre-build)` stamp, then the matrix still over-asserts and the relabel has FAILED. (The 41%/59% value-blend from `scorecard:5` is exempt only because it is a qualitative stage judgement, not an escape-catch result — but it must be explicitly labelled as such per A.3.)

---

## E. Per-INV Dispositions

| INV | Severity | Disposition | Evidence pointer |
|---|---|---|---|
| **INV-001** | HIGH | **ADDRESSED** | Crosswalk §A.2 + §A.3(a): E4 has NO table row; sourced from `contract-implementations.md:14-19`; reconciliation is 4-of-5. |
| **INV-006** | HIGH | **ADDRESSED** | Crosswalk §A.2 resolves all 4 schemes (E1–E5 / A M1–M6+F-A/F-B / B M1–M7 / table 9 rows); §A.3(b/c) resolves E4↔PRD-E04 collision and assigns `--file`→E1. |
| **INV-007** | HIGH | **ADDRESSED** | §B 3-bucket ledger + honest one-sentence claim; "blanket nothing-built" replaced. |
| **INV-008** | HIGH | **ADDRESSED** | §B ledger: UNBUILT (diff-empty since 94d5baa0) / MERGED (5 PRs ancestor-of-master) / UNMERGED (`b97c9960` on branch only). |
| INV-002 | MEDIUM | ADDRESSED (rides INV-001) | §A.2: 5 pre-episode rows are an out-of-window subset, not "predating context"; appendix ≠ superset of E1–E5. |
| INV-009 | MEDIUM | ADDRESSED | §D cell-level relabel rule + falsifier. |
| INV-012 | MEDIUM | ADDRESSED | §C: lines 259/30 fresh; blame `27962ddb2`/`09e2ccc0d`, not #149; M6+E4 live on master. |
| INV-016 | MEDIUM | ADDRESSED | §B: G1 gates meta-hardening only; E4's `b97c9960` is an independent unmerged product fix. |
| INV-015 | MEDIUM | ADDRESSED (rides INV-012) | §C: M6 and E4 are distinct divergences in distinct files → separate ledger rows. |
| INV-004 | MEDIUM | ADDRESSED (rides INV-001) | §A.3 denominator note: 59% is a stage value-blend, not an escape-catch rate; the two systems must not be stitched into one derived metric. |

**4/4 HIGH (INV-001, INV-006, INV-007, INV-008) now ADDRESSED.**

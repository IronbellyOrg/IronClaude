# QA Research Gate Report — TASK-RF-20260531-042405

**Mode:** research-gate (adversarial, fix_authorization=false)
**Date:** 2026-05-31
**Track goal:** Eliminate roadmap-pipeline brittleness via R0 bridge + R1 substrate rewrite
**Files audited:**
- 01-file-inventory.md (R1, "Researcher R1 — File Inventory")
- 02-patterns-conventions.md (R2)
- 03-template-and-precedent.md (R3)

## Method

Sample-verified cited file:line references by reading actual source files. Cross-checked LOC totals, file counts, symbol locations, and key claims about gates, parsers, fail-open code, and CLI surface. Adversarial stance: assume errors present; flag every divergence found.

---

## OVERALL VERDICT: PASS (with 4 important + 5 minor issues — actionable, not blocking)

The research is substantively correct and the load-bearing claims (gate=None bypass, fail-open default, return-True semantic-check stub, dual frontmatter parsers, preserve targets) are all verified accurate against current code. Line numbers are close enough to be navigable. Recurrence-corpus layout is sound. Template-rule citations align with project conventions. The task-builder can proceed.

That said, the inventory has a **factual omission** (one file missing) and several line-number/LOC drifts that should be corrected before task generation to avoid worker-agent dead-end navigation. None of the issues invalidate the analytical conclusions.

---

## CRITICAL ISSUES (0)

None. All load-bearing claims about brittleness contracts (gate=None bypass at executor.py:2167, fail-open at fidelity_checker.py:287-303, return-True stub at gates.py:48-91, dual frontmatter parsers, SemanticCheck signature flaw) were verified accurate against the live source.

---

## IMPORTANT ISSUES (4)

### IMP-1 — R1 file inventory is INCOMPLETE: omits `validate_executor.py` (519 LOC)

**Where:** `01-file-inventory.md` Section A enumerates 25 files but the directory contains **26 Python files**.

**Evidence:** `ls src/superclaude/cli/roadmap/*.py | wc -l` = **26**. R1 §A claims "25 files, 16,698 LOC." R1's preamble (line 9) says "the working directory contains 25 Python files…the notes omit `validate_gates.py`." That statement is wrong twice: (a) actual count is 26, and (b) `validate_gates.py` IS enumerated at R1 §A.2 (line 66). The truly omitted file is **`validate_executor.py` (519 LOC)**.

**Cross-evidence:** R1's executor.py entry (line 36) imports from `validate_executor.*`, confirming the module exists in scope; Section A.7 covers `spec_*` files but A has no `validate_executor.py` subsection. Section F gate matrix likewise omits validate_executor.

**LOC math:** R1 reports 16,698 LOC. Actual `wc -l` = **16,699** (off by 1). Adding the missing validate_executor.py (519 LOC) to R1's enumerated set would overshoot — meaning some other entry is over-counted, OR the missing file's LOC is folded into another count silently. Either way, the inventory is not internally consistent.

**Impact for task-builder:** R1.4 (tool-write rewrite) and R1.2 (envelope migration) phase plans need validate_executor.py in scope (it's the validate-subcommand execution path; `validate_prompts.py` is enumerated but the executor isn't). Without this entry, task-builder may emit phase items hitting the prompts module but missing the executor sites.

**Severity:** Important. Task-builder must add `validate_executor.py` to the per-file checklist for R1.4 / R1.2 / Section F gate matrix.

---

### IMP-2 — R2 misattributes `--no-convergence` flag location (commands.py:188 vs commands.py:98)

**Where:** `02-patterns-conventions.md` §6.2 (line 334) claims "`commands.py:188` declares `--no-convergence` with `default=False`".

**Evidence:** `grep -n "no-convergence\|no_convergence" src/superclaude/cli/roadmap/commands.py`:
- **L98**: `"--no-convergence",` — the actual click option declaration
- **L188**: `no_convergence: bool,` — function parameter binding, NOT the declaration

The flag option block lives around L98-100. L188 is just where the parameter appears in the `run(...)` signature.

**Impact for task-builder:** Worker agent told to "modify the `--no-convergence` declaration at commands.py:188" will read a parameter list and find nothing to edit. This wastes a Read cycle and breaks the F1 execution loop's locality assumption.

**Severity:** Important. R2's "load-bearing 188" claim is also referenced indirectly in §1.2 ("`commands.py:188` / `--no-convergence` flag"); both citations need correction to L98.

---

### IMP-3 — R3 misstates `tests/roadmap/conftest.py` length (39 lines vs actual 82 lines)

**Where:** `03-template-and-precedent.md` Source-files-cited (line 12) says "tests/roadmap/conftest.py:1-39 (only audit_trail fixture exists)" and §3.1 (line 145) repeats "`tests/roadmap/conftest.py:1-39`".

**Evidence:** `wc -l tests/roadmap/conftest.py` = **82**. The file defines two session-scoped fixtures (`results_dir` at L29, `audit_trail` at L37) — not "only audit_trail" — and includes imports + comments bringing it to 82L, not 39L.

**Impact for task-builder:** R3's §3.4 "Loader pattern (recommended for `tests/roadmap/conftest.py` extension)" assumes a clean 39-line file. Worker agent will encounter twice that, and a more complex existing fixture surface. Not a blocker (recommendation still works), but the precondition is wrong and the insert point shifts.

**Severity:** Important. Re-anchor R3's loader-fixture extension recipe to the actual end-of-file (L82); also account for the `results_dir` fixture already present.

---

### IMP-4 — R1 symbol line numbers consistently drift by 1-2 lines

**Where:** Multiple per-file entries in `01-file-inventory.md` Section A cite symbol line numbers that are off by 1.

**Spot-verified discrepancies (Read-confirmed):**

| Claim | R1's cited line | Actual line | File |
|---|---|---|---|
| `class Obligation` | L166 | **L167** | obligation_scanner.py |
| `class ObligationReport` | L182 | **L183** | obligation_scanner.py |
| `scan_obligations()` | L208 | **L209** | obligation_scanner.py |
| `obligation_scanner.py` LOC | 825 | **826** | obligation_scanner.py |
| Total roadmap dir LOC | 16,698 | **16,699** | (see IMP-1) |
| `_parse_frontmatter` | L168 | **L168** verified | gates.py (correct) |
| `_cross_refs_resolve` | L48 | **L48** verified | gates.py (correct) |
| `executor.py:2167` gate=None | L2167 | **L2167** verified | executor.py (correct) |
| `fidelity_checker.py:287-303` | L287-303 | **L287-303** verified | (correct) |

Some line numbers are dead-on; others drift by 1. Most likely cause: R1 used a different line-counting tool than `wc -l` (or read with a different newline interpretation) for some files but not others.

**Impact for task-builder:** Each citation requires Read-verify in the task-builder's confidence pass before phrasing checklist items. Worker agents will mostly land within scrolling distance, but the inconsistency means **no single R1 line citation can be trusted without re-verification**. This forces an extra Read per item.

**Severity:** Important. Recommend a one-shot re-verification pass on every R1 citation before embedding into checklist items, OR cite by symbol name (`class Obligation` in `obligation_scanner.py`) rather than line number when authoring items.

---

## MINOR ISSUES (5)

### MIN-1 — R1 LOC reconciliation off-by-one and ambiguous

R1 line 9: "LOC totals: 16,698 matches the notes (the additional file is the smallest and the count includes `__init__.py` at 10 LOC)." Actual `wc -l` total is **16,699**. With validate_executor.py (519 LOC) missing, the math doesn't fully reconcile. Not load-bearing; flagged for accuracy.

### MIN-2 — R2 over-counts `_parse_frontmatter` consumer callsites

R2 §2.4 says "Used by **26 semantic-check functions** in `gates.py`" then lists 26 line numbers including the definition site at L168 and some `return` statements (L483, L735 explicitly noted as `(return)`). Some of these are intra-function returns, not callsite enumerations. The "26" should be re-checked with `grep -c "_parse_frontmatter(content)"`. Not load-bearing; the canonical-parser-needed conclusion stands.

### MIN-3 — Fixture-input markdown files not enumerated in R1's test-file list

R3 §3.2 proposes `<case_name>.md` + `<case_name>.expected.json` pairs per failure class. R1 §C (lines 244-256) lists "NEW" test files but never enumerates the fixture-input markdown files. Task-builder must merge R3's fixture-tree proposal with R1's test-file list when authoring R0/R1 phase items.

### MIN-4 — R2 over-claims "exactly 1" gate=None bypass scope

R2 §1.2 (line 52): "Net `gate=None` bypass count in `_build_steps`: exactly 1 (L2167)." Verified accurate for `_build_steps`. But R2's own §1.3 notes `build_certify_step` is a separate function. The phrasing risks task-builder concluding "only one bypass anywhere" which isn't quite what R2 said. Clarify: "exactly 1 in `_build_steps`; certify-step uses `CERTIFY_GATE` via the factory (no bypass)."

### MIN-5 — Recurrence-corpus seeding mapping deferred (acknowledged)

R3 §4 line 242 already flags this as an open question and recommends deferral to a discovery item — adequate gating. Flagging here to ensure the task-builder explicitly preserves this in the Phase 1 discovery item rather than losing it in transcription.

---

## SAMPLE VERIFICATION — Reads performed

The following claims were Read-confirmed directly against worktree source:

- gates.py L48-91 `_cross_refs_resolve` — verified always returns True (L89, L91)
- executor.py L2167 — verified `gate=None if config.convergence_enabled else SPEC_FIDELITY_GATE`
- fidelity_checker.py L287-303 — verified `found=True,  # fail-open` smoking gun at L298
- fidelity_checker.py L314-337 — second fail-open verified
- pipeline/models.py L82-87 — `SemanticCheck` dataclass with `check_fn: Callable[[str], bool | str]` shape verified
- pipeline/models.py L91-105 — `GateCriteria` dataclass shape verified
- pipeline/gates.py L91 `_check_frontmatter` — verified signature
- executor.py `# Step` comments — verified two `# Step 8` entries at L2139 and L2157 (R2 §1.1 accurate)
- gates.py ALL_GATES — 14 entries verified at L1426-1441 (R1 §A.2 accurate)
- commands.py 20 options for `run` — `sed -n '30,175p' | grep -c "^@click"` = 20 (R2 §6.1 verified)
- obligation_scanner.py `_DESCRIPTOR_NOUNS` at L109, `_DEMOTED_H3_SUBSECTIONS` at L137 (R2 §4.2 verified)
- tests/roadmap/ — 64 `test_*.py` files (R3 §3.1 verified)
- tests/roadmap/ subdirs — only `__pycache__/` (R3 §3.1 "no fixtures/ subdir exists today" verified)

---

## COVERAGE GAPS (areas the researchers MAY have missed)

1. **`validate_executor.py` (519 LOC)** — see IMP-1; full omission.
2. **`cli/audit/wiring_gate.py:_extract_frontmatter_values` L931** — R1 Section E flags it as a Contract #6 ripple but no structural inventory provided. If R1.6 parser-consistency work needs to touch this file, the task-builder lacks a structural read on it.
3. **`cli/cli_portify/utils.py:parse_frontmatter L11`** — same gap as above; flagged in cross-substrate but not inventoried.
4. **`tests/v3.3/conftest.py`** — referenced by tests/roadmap/conftest.py imports (L25). Envelope-fixture migration touching `AuditTrailHelper` ripples here; R3 doesn't audit it.
5. **Atexit cleanup interaction** — R2 §5.1 (line 301) flags that `atexit.register(_atexit_cleanup)` in convergence.py must not break under envelope migration; R1 §A.3 convergence.py entry doesn't mention atexit. Cross-file consistency check: task-builder must reconcile manually.

---

## ACTIONABILITY ASSESSMENT (for task-builder)

| Dimension | Verdict | Notes |
|---|---|---|
| Granularity | PASS | Per-file checklist items buildable from R1 Section F gate matrix |
| Concrete file:line citations | MOSTLY PASS | IMP-2 + IMP-4 require re-verification pass before embedding |
| Pattern enforcement | PASS | R2 §7 conventions-to-keep + anti-patterns-to-remove are crisp |
| Template alignment | PASS | R3 §1 covers every Template 02 PART 1 rule that applies |
| Recurrence corpus layout | PASS | R3 §3 layout sound; seeding mapping deferred (MIN-5) |
| Test file enumeration | PASS | R1 §C table maps Contract # to tests cleanly |
| Cross-substrate coverage | MOSTLY PASS | R1 §B + §E flag substrate files; inventories partial (gaps 2-4) |

---

## VERDICT: PASS

The research is publishable as the basis for task generation, contingent on the task-builder:

1. **Adding `validate_executor.py` (519 LOC) to per-file inventory and R0/R1 touch matrix** (IMP-1).
2. **Re-verifying every cited file:line in the research before embedding into checklist items** — recommend `grep -n` pass per cited symbol (IMP-2, IMP-4).
3. **Re-anchoring R3's conftest extension recipe to the actual 82-line file** (IMP-3).
4. **Reconciling substrate-file ripple gaps** (cli/audit/wiring_gate, cli/cli_portify/utils, tests/v3.3/conftest) — either inventory them in a Phase 1 discovery item or accept as Open Questions.

No critical issues. The 4 important issues are surface-correctable; the 5 minor issues are flagged for awareness, not as blockers.

**Issues count:** 9 (0 critical / 4 important / 5 minor)

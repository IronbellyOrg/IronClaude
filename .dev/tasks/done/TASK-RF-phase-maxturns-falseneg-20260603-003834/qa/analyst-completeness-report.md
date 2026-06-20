# Research Completeness Verification

**Topic:** task-builder track 1 — fix per-task `error_max_turns` false-negative phase failure in IronClaude sprint executor
**Date:** 2026-06-03
**Files analyzed:** 3 (01-target-code-executor.md, 02-reference-recovery-and-conventions.md, 03-tests-and-template.md)
**Depth tier:** Standard/Deep (file-inventory + reference + test/template tracks)
**Analyst:** rf-analyst (single instance — no partition)

---

## Verdict: (computed at end — see VERDICT line)

This report evaluates the 9 spawn-prompt criteria, with a dedicated CRUX section
on the INCOMPLETE-vs-new-status decision. Findings appended incrementally below.

---

## CRUX ANALYSIS (the gating question)

**The CRUX:** reclassifying to the existing `TaskStatus.INCOMPLETE` does NOT fix
the bug, because (a) `INCOMPLETE != PASS` and (b) `INCOMPLETE` is itself a
`is_failure` member. A new success-valued task status, or an `is_success`-based
aggregation that the reclassified status satisfies, is REQUIRED.

### Independently re-verified against live source (analyst Read, not just trust)

| Fact | Research claim | Live code | Match |
|------|---------------|-----------|-------|
| `TaskStatus.is_success` | `== PASS` only (01 §4 L215-217) | models.py:48-50 `return self == TaskStatus.PASS` | YES |
| `INCOMPLETE` is failure | `is_failure` includes INCOMPLETE (01 §4) | models.py:52-54 `(FAIL, INCOMPLETE)` | YES |
| no recovered TaskStatus | "NO PASS_RECOVERED member" (01 §4 L223) | models.py:42-46 = PASS/FAIL/INCOMPLETE/SKIPPED | YES |
| aggregation is strict `== PASS` | 01 §5 L312 / 02 TL;DR | executor.py:1278 `all(r.status == TaskStatus.PASS ...)` | YES |
| per-task switch site | 1014-1020 (01 §1) | executor.py:1014-1020 (PASS/INCOMPLETE/FAIL) | YES |

So the aggregation does NOT use `is_success` — it is a hard identity check
against `TaskStatus.PASS`. Reclassifying T06.15 to `INCOMPLETE` would leave
`all_passed == False` and still force `PhaseStatus.ERROR` / exit 1. The bug
would NOT be fixed. The CRUX is real and the live code confirms it.

### Is the research internally consistent on the CRUX? — NO (this is the gap)

- **Researcher-01 (file 01): CORRECT and explicit.** §4 L223-233 and Summary
  L359-362 state plainly that bare `INCOMPLETE` reclassification is
  *insufficient* and the fix must EITHER add a new `is_success`-True `TaskStatus`
  member OR switch aggregation to `r.status.is_success` AND make the
  reclassified status report success. §5 L321-335 gives both options (Option A
  new member; Option B accept-set) and ties them to relaxing line 1278. This is
  the correct resolution of the CRUX.

- **Researcher-03 (file 03): CORRECT (consistent with 01).** Its test design
  asserts `results[0].status != TaskStatus.FAIL` and explicitly says "INCOMPLETE
  or PASS_RECOVERED per researcher-01/02's fix" (L139, L448), deferring the enum
  choice to 01/02 rather than asserting `== INCOMPLETE`. It does NOT contradict
  the CRUX. (Note: a `!= FAIL` assertion would PASS even for the BUGGY
  `INCOMPLETE`-only fix — so the test as drafted does not by itself FORCE the
  correct fix; see Finding G2.)

- **Researcher-02 (file 02): INCONSISTENT with the CRUX — this is the gap.**
  File 02 repeatedly recommends reclassifying to `TaskStatus.INCOMPLETE` as the
  per-task target WITHOUT flagging that INCOMPLETE is `is_failure` and `!= PASS`
  and therefore does not fix the false negative:
  - TL;DR L169-171: "the per-task path can reclassify to `TaskStatus.INCOMPLETE`
    (the task-level analog of the phase-level `INCOMPLETE`). There is no
    `TaskStatus.PASS_RECOVERED`." — states the analog without noting it fails.
  - §3 L299-304: "reclassify FAIL → a success-like/INCOMPLETE task status" —
    conflates "success-like" and "INCOMPLETE" as if interchangeable; they are
    NOT (`INCOMPLETE.is_success == False`).
  - §3 reuse-table footer L361-366 and Summary L461-462: "Reclassification
    target enum values available: `TaskStatus.PASS`, `TaskStatus.INCOMPLETE`."
    — presents INCOMPLETE as a viable target with no warning that it does not
    clear the strict `== PASS` aggregation gate.
  - Critically, file 02 ALSO read the aggregation-relevant code paths and even
    documented the per-PHASE precedent where `detect_error_max_turns` maps to
    `INCOMPLETE` (its §1 L118-125) — yet did NOT carry that observation through
    to the per-task aggregation gate at 1278. It explicitly defers the enum
    choice to researcher-01 ("researcher-01 owns the exact reclassification
    target enum", §3 L304), which is a partial mitigation, but its own
    affirmative recommendation of INCOMPLETE is the actively misleading part.

**Net CRUX verdict:** The research collectively CONTAINS the correct answer
(researcher-01 nails it, researcher-03 stays compatible), but it is NOT
internally consistent: researcher-02 affirmatively recommends the INCOMPLETE
reclassification that researcher-01 proves is insufficient, and never
cross-references researcher-01's refutation. A builder reading file 02 in
isolation (or weighting it as the "reference/conventions" authority) could ship
the broken INCOMPLETE-only fix. Per the spawn-prompt's explicit instruction
("If any research file is internally inconsistent on this, FAIL with the
specific gap"), this is a FAIL-triggering contradiction that must be reconciled
before the task file is built.

---

## Per-Criterion Findings (9 spawn-prompt criteria)

### Criterion 1 — Source files identified with paths and exports — PASS
- Edit site #1: `executor.py:1014-1020` per-task status switch (file 01 §1,
  §Summary) — verified live at executor.py:1014-1020.
- Edit site #2: `executor.py:1278-1279/1283` phase aggregation (file 01 §5) —
  verified live at executor.py:1278.
- `models.py` enums: `TaskStatus` 39-53, `PhaseStatus` 211-269 (file 01 §4) —
  `TaskStatus` verified live at 39-54.
- monitor detectors: `detect_error_max_turns(output_path)->bool` @monitor.py:37,
  `detect_prompt_too_long(output_path,*,error_path=None)->bool` @64 (file 02 §2)
  — `detect_error_max_turns` signature verified live at monitor.py:37.
- path helpers: `task_output_file`/`task_error_file` @models.py:502-506 (files
  01 §3, 02) — verified live at models.py:502-506 (NOT in config.py; file 01 §3
  correctly disambiguates `config.py` vs `models.py`).
- import in scope: file 02 claims detectors are imported into executor.py —
  verified live at executor.py:37 `from .monitor import OutputMonitor,
  detect_error_max_turns, detect_prompt_too_long`. Strong evidence quality.

### Criterion 2 — Verification commands clear — PASS
- File 02 §4 gives exact UV-only commands: `uv run pytest tests/sprint/`,
  `tests/sprint/test_executor.py -v`, `tests/sprint/test_monitor.py -v`,
  `make test`, `make lint` (ruff check), `make format`, `make verify-sync`.
- File 03 §3 gives node-id invocation forms incl. the class-scoped
  `tests/sprint/test_executor.py::TestPerTaskOrchestration -v`.
- `make verify-sync` correctly scoped: files 02 §4 + 03 §3 both establish the
  edit is to `cli/sprint/` Python (NOT a synced `.claude/` component), so
  `make sync-dev` is NOT required; `verify-sync` should pass unchanged as a
  no-regression gate. Consistent across both files. Commands are specific and
  runnable.

### Criterion 3 — Logical breakdown into phases/steps — PASS
- File 01 Summary enumerates the 3 concrete edit sites in order.
- File 02 §1 supplies the structural pattern to mirror (detect-before-default
  ladder) and §3 a reuse table that rules out the phase-granular helpers.
- File 03 §4 maps the fix onto template-02's Build→Test→Fix (K1/K2 → L3 → L5)
  structure and §1/§2 specify the test construction step-by-step. The
  fix/test/guard-test/run breakdown is explicit (file 03 §4 A3 note).

### Criterion 4 — Patterns & conventions documented with examples — PASS
- Per-phase recovery precedent: file 02 §1 quotes the full `exit_code != 0`
  ladder (lines 2090-2111) AND the `exit_code == 0` `detect_error_max_turns`
  branch (2113-2148) verbatim, with the critical nuance (Criterion 8 / G1).
- Sync model: file 02 §4 (CLAUDE.md:16-33, Makefile targets) with the explicit
  "do NOT git add `.claude/`" rule.
- Git workflow: file 02 §4 — `fix/` branch off `integration`, conventional
  commits, PR `--repo IronbellyOrg/IronClaude --base master`. Examples concrete.

### Criterion 5 — MDTM template-02 notes present — PASS
- File 03 §4 documents template-02 in depth: frontmatter required fields,
  Section A (A3 granularity), Section B self-contained item pattern (B1-B7, the
  6 required elements), Section D3 (no items before Phase 1), Section E flat
  checkboxes, Section L handoff patterns (L3 test-execute, L5 conditional, L7
  selection guide), and the PART-2 skeleton incl. the required dedicated
  `### Phase N: Testing & Verification`. Template path cited (absolute).

### Criterion 6 — Granularity sufficient for per-file edit items — PASS
- File 03 §4 A3 explicitly calls for separate items: write the fix / write the
  new test / write the guard test / run the suite. File 01 pins exact line
  ranges for each edit (1014-1020, 1278-1283, models.py enum). File 03 §5 gives
  a verbatim item-paragraph shape to clone. Granularity is per-edit-site.

### Criterion 7 — Cross-validation: claims tagged with file:line; flags — MIXED/PASS-with-note
- Evidence quality is STRONG: nearly every claim carries `file:line` (executor.py
  line numbers, models.py:502-503, monitor.py:37, test_executor.py:715-727, etc.).
  Analyst independently re-verified 8+ of these against live source — all matched.
- However the research does NOT use the formal `[CODE-VERIFIED]` /
  `[CODE-CONTRADICTED]` / `[UNVERIFIED]` tag vocabulary uniformly. File 03 DOES
  use bare `UNVERIFIED` markers (L152, L222, L255, L454). Files 01 and 02 use
  prose ("Confirmed", "verified key nuance") rather than the tag. No
  `[CODE-CONTRADICTED]` claims exist. The doc-sourced claims (CLAUDE.md /
  pyproject.toml / Makefile line cites in file 02 §4) are not formally
  verification-tagged but are config/convention facts, not architectural claims
  needing code cross-validation. Acceptable; minor (G3).

### Criterion 8 — Solution approach evaluated — PASS
- INCOMPLETE-vs-new-status: file 01 §4-§5 evaluates Option A (new member) vs
  Option B (accept-set / `is_success`) with pros and the phase-level
  `PASS_RECOVERED` analog. (The CRUX inconsistency is a CONSISTENCY defect across
  files, not an absence of evaluation — see CRUX section + Finding G1.)
- Output-path reachability: file 01 §1-§2 DEFINITIVELY resolves the open
  question — `config`, `phase`, `task` are all in caller scope at 1014-1020, so
  `config.task_output_file(phase, task)` is directly callable and
  `_run_task_subprocess`'s return signature does NOT need to change. This is the
  strongest single resolution in the research and is independently plausible
  (the helper is a pure method on `SprintConfig`). PASS.
- Key per-PHASE nuance (file 02 §1, G1): `detect_error_max_turns` today runs
  ONLY on the `exit_code == 0` branch (→ INCOMPLETE), never on the non-zero
  branch. T06.15 exited NON-zero, so the fix must ADD the detector to a
  non-zero-exit path, not copy either existing branch. Verified live:
  executor.py:2144 is the only `detect_error_max_turns` call and it sits under
  the `== 0` path. This is correctly surfaced.

### Criterion 9 — Unresolved ambiguities documented — PARTIAL
- 9(a) new TaskStatus member vs `is_success` aggregation: file 01 documents BOTH
  options but does not pick one (acceptable — it is a builder decision). HOWEVER
  the cross-file CONTRADICTION (file 02 recommending INCOMPLETE) is NOT
  documented as an open ambiguity in any file — file 02 presents INCOMPLETE as
  settled-viable. This is the gap (G1).
- 9(b) UNVERIFIED reconciliation between researchers (canonical path vs factory
  tuple): file 03 DOES flag this — L152, L222, L454-458: "UNVERIFIED whether the
  fix reads the canonical `config.task_output_file()` path vs extends the factory
  tuple … reconcile with researcher-01's production decision." AND file 01 §2
  ACTUALLY RESOLVES it (no signature change; recompute path in caller — the
  canonical-path approach). So 9(b) is raised by 03 and answered by 01, but the
  two are not cross-linked: file 03 still lists it as UNVERIFIED without noting
  file 01 already decided it. Minor reconciliation gap (G4) — lower severity
  than G1 because the resolution exists in the corpus.

---

## Contradictions Found

1. **CRUX contradiction (CRITICAL).** File 02 recommends reclassifying the
   per-task status to `TaskStatus.INCOMPLETE` (02 TL;DR L169-171, §3 L299-304,
   §3 reuse-footer L361-366, Summary L461-462) as a viable "success-like" target.
   File 01 proves this is insufficient (01 §4 L223-233): `INCOMPLETE.is_success
   == False`, `INCOMPLETE != PASS`, and aggregation at executor.py:1278 is a
   strict `== PASS` check, so an INCOMPLETE task still forces `PhaseStatus.ERROR`.
   Both verified against live code by the analyst. File 02 never cross-references
   or qualifies file 01's refutation. **The two files disagree on the single
   gating design decision.**

2. **Edit-site line-range drift (cosmetic, self-resolved).** REPORT.md cited the
   switch as "1013-1020"/"1016-1020"; file 01 reconciles to the live 1014-1020
   (01 §1 L57-59). File 03 cites "1015-1020". All three point at the same block;
   analyst confirms live block is 1014-1020. Not a substantive contradiction.

## Compiled Gaps

### Critical Gaps (block task-file build / synthesis)
- **G1 — CRUX inconsistency.** File 02 affirmatively recommends the
  `TaskStatus.INCOMPLETE` reclassification that file 01 proves does NOT fix the
  bug, and the contradiction is undocumented. A builder could ship a broken
  INCOMPLETE-only fix. RESOLUTION REQUIRED before build: the task file MUST
  mandate either (Option A) a new `is_success`-True `TaskStatus` member
  (e.g. `PASS_RECOVERED`/`PASS_MAX_TURNS`) set in the 1014-1020 block when
  `detect_error_max_turns(config.task_output_file(phase, task))` is True, OR
  (Option B) change executor.py:1278 to `all(r.status.is_success ...)` AND have
  the reclassified status satisfy `is_success`. A bare INCOMPLETE reclassification
  is explicitly INSUFFICIENT and must be ruled out in the task instructions.

### Important Gaps (affect quality)
- **G2 — Test does not force the correct fix.** File 03's drafted positive
  assertion is `results[0].status != TaskStatus.FAIL` (03 L213, L448). Under the
  BUGGY INCOMPLETE-only fix, the task status would be `INCOMPLETE` (which is
  `!= FAIL`), so the unit test would PASS while the phase still errors. The test
  as drafted does not, on its own, prevent the G1 failure mode. RECOMMENDATION:
  the task file should add a PHASE-LEVEL assertion (e.g. assert the aggregated
  `PhaseResult.status.is_success` / `exit_code == 0` for a phase whose only
  non-PASS task is a recovered error_max_turns task), OR assert the task status
  is the specific recovered (is_success-True) status — not merely `!= FAIL`.

### Minor Gaps (must still be fixed)
- **G3 — Inconsistent verification-tag vocabulary.** Files 01/02 use prose
  ("Confirmed"/"verified") instead of `[CODE-VERIFIED]`; only file 03 uses bare
  `UNVERIFIED`. No `[CODE-CONTRADICTED]` present. Doc-sourced config cites
  (CLAUDE.md/pyproject/Makefile in 02 §4) are untagged. Low risk; analyst
  independently re-verified the load-bearing claims.
- **G4 — 9(b) reconciliation not cross-linked.** File 03 lists the
  "canonical path vs factory tuple" question as UNVERIFIED (L454-458); file 01 §2
  already resolves it (no signature change; recompute path in caller). The
  task-builder should adopt file 01's resolution and mark 03's UNVERIFIED as
  closed. Resolution exists in-corpus, so this is minor.

## Depth Assessment
**Expected depth:** Standard/Deep across three tracks (target-code inventory,
reference/conventions, tests/template).
**Actual depth achieved:** High. File 01 traces exact in-scope variables at the
edit site and resolves the output-path reachability question with scope analysis.
File 02 quotes the full reference recovery ladder and supplies a helper-reuse
table with granularity reasoning. File 03 traces the exact test seam, the
established fake-NDJSON convention, the mkdir gotcha, and a full template-02 +
prior-example walkthrough.
**Missing depth elements:** None on coverage; the single substantive defect is a
CONSISTENCY defect (G1), not a depth/coverage shortfall. The research IS deep
enough — it simply contradicts itself on the crux.

## Recommendations (for task-builder, before building the task file)
1. **Reconcile G1 explicitly.** Add a decision note (or postscript) that
   supersedes file 02's INCOMPLETE recommendation: bare INCOMPLETE is INSUFFICIENT;
   the fix MUST yield an `is_success`-True outcome (new TaskStatus member OR
   is_success-based aggregation). Encode this as a hard requirement in the fix item.
2. **Strengthen the test per G2** to assert phase-level success (or the specific
   recovered status), not merely `!= FAIL`, so the test fails against an
   INCOMPLETE-only implementation.
3. **Adopt file 01's output-path resolution (G4):** no `_run_task_subprocess`
   signature change; recompute `config.task_output_file(phase, task)` in the
   caller. Update the test to write the fake NDJSON to that canonical path with
   `mkdir(parents=True)` (file 03's #1 gotcha).
4. Keep the guard test (non-zero exit, NO error_max_turns file → still FAIL).
5. Optionally normalize verification tags (G3) — not blocking.

---

## VERDICT: FAIL

**Reason:** Per the spawn-prompt's explicit gating instruction — "Pay special
attention to whether the research resolves the CRUX … If any research file is
internally inconsistent on this, FAIL with the specific gap" — the corpus is
internally inconsistent on the CRUX. File 02 affirmatively recommends a
`TaskStatus.INCOMPLETE` reclassification that file 01 (and the live code, analyst-
verified) proves does NOT fix the false negative, and the contradiction is left
undocumented. This is exactly the FAIL condition named in the prompt.

8 of 9 criteria PASS individually (coverage, commands, breakdown, patterns,
template, granularity, evidence, solution-approach all strong); the failure is a
single CRITICAL cross-file consistency gap (G1), with one Important (G2) and two
Minor (G3, G4) gaps. The research is recoverable: file 01 already contains the
correct answer, so reconciliation is a focused edit, not a re-research.

**Gap list (severity-ordered):**
- G1 (CRITICAL): CRUX inconsistency — file 02 recommends insufficient INCOMPLETE
  reclassification; contradicts file 01; undocumented. MUST reconcile to an
  is_success-True outcome.
- G2 (IMPORTANT): drafted test asserts only `!= FAIL`, which passes under the
  broken INCOMPLETE-only fix; add phase-level / specific-status assertion.
- G3 (MINOR): inconsistent `[CODE-VERIFIED]`/`[UNVERIFIED]` tag usage across
  files 01/02.
- G4 (MINOR): file 03's "canonical path vs factory tuple" UNVERIFIED is already
  resolved by file 01 §2 but not cross-linked.

---

## Gap-Fill Re-Check (Round 1)

**Date:** 2026-06-03
**New file verified:** `research/04-gap-fill-crux-reconciliation.md`
**Prior verdict:** FAIL (G1 CRITICAL, G2 IMPORTANT, G3 MINOR, G4 MINOR)
**Re-verification method:** Read file 04 in full; re-Read live source (models.py:39-53,
211-279, 500-506; executor.py:1014-1020, 1276-1283; monitor.py:37) to confirm file 04's
load-bearing claims; re-read files 01 and 03 to check for any NEW contradiction introduced
by file 04.

### Authority / tie-breaker declaration — RESOLVED

File 04 explicitly declares itself the authoritative tie-breaker: lines 12-18
("This file is the authoritative tie-breaker the builder MUST follow. Where this
file and any other research file disagree, **this file wins**."). It scopes itself
to G1/G2/G4 (line 4). PASS.

### Check 1 — G1: success-valued outcome, NOT bare INCOMPLETE; reasoning correct — RESOLVED

- **Picks a success-valued outcome, not bare INCOMPLETE.** DECISION 1 (lines 30-40)
  introduces a NEW `TaskStatus.PASS_RECOVERED` (is_success==True), mirroring the
  existing `PhaseStatus.PASS_RECOVERED`, and explicitly REJECTS reusing INCOMPLETE.
  `is_success` is updated to `self in (TaskStatus.PASS, TaskStatus.PASS_RECOVERED)`
  and `is_failure` excludes the new member. Correct.
- **Reasoning that INCOMPLETE must keep failing — VERIFIED against live source.**
  File 04's two-reason refutation (lines 32-34):
  1. `INCOMPLETE != PASS` and `INCOMPLETE ∈ is_failure` → re-verified live:
     `models.py:52-53` `is_failure` returns `self in (TaskStatus.FAIL,
     TaskStatus.INCOMPLETE)`. **Confirmed — INCOMPLETE is a failure member.**
  2. `exit 124` (genuine timeout) also maps to INCOMPLETE → re-verified live:
     `executor.py:1017-1018` `elif exit_code == 124: status = TaskStatus.INCOMPLETE`.
     **Confirmed — file 04's cite to executor.py:1018 is exact.** File 04's
     conclusion that making INCOMPLETE success-valued would silently pass genuine
     timeouts (a regression) is therefore CORRECT and well-grounded. This is the
     decisive, code-true reason bare INCOMPLETE is the wrong target — exactly the
     point file 02 missed.
- **Precedent claim verified.** `PhaseStatus.PASS_RECOVERED` exists at
  `models.py:219` with comment "non-zero exit but evidence of success"; `TaskStatus`
  (models.py:42-45) has no counterpart. File 04's asymmetry claim is exact.
- **Aggregation switch (DECISION 3).** Live `executor.py:1278` is
  `all(r.status == TaskStatus.PASS ...)`; file 04 changes it to
  `all(r.status.is_success ...)` (lines 65-69), which lets PASS + PASS_RECOVERED
  pass while FAIL/INCOMPLETE/SKIPPED still fail. Consistent with DECISION 1. PASS.

**G1 — RESOLVED.** File 04 authoritatively overrides file 02's bare-INCOMPLETE
recommendation with a success-valued `PASS_RECOVERED` target, and the reasoning is
verified correct against live code.

### Check 2 — G2: strengthened test assertions + genuine-timeout guard — RESOLVED

DECISION 4 (lines 75-96) replaces the weak `!= TaskStatus.FAIL` assertion with:
- **Positive test:** asserts `results[0].status == TaskStatus.PASS_RECOVERED` AND
  `results[0].status.is_success is True` AND aggregated phase `is_success` /
  `== PhaseStatus.PASS(_RECOVERED)` — a specific-status + phase-level assertion that
  would FAIL under the broken bare-INCOMPLETE implementation. This directly fixes
  the G2 weakness.
- **Guard B (genuine timeout / exit 124):** asserts `status == TaskStatus.INCOMPLETE`
  AND phase NOT is_success (still fails) — the explicit non-regression guard for the
  exit-124 path the prompt asked for. PASS.
- Also adds Guard A (genuine failure, no error_max_turns file → FAIL) and Guard C
  (overran without completion → FAIL), plus the DECISION 2 completion-gated recovery
  predicate (`_task_completed_before_overrun`) so recovery requires a pre-terminal
  success envelope, not bare `error_max_turns`. Test seam/fixtures and the
  `mkdir(parents=True)` gotcha are carried forward (lines 93-96), consistent with
  file 03 §2.

**G2 — RESOLVED.** Assertions are now is_success / PASS_RECOVERED / phase-level, and
the exit-124 non-regression guard is present.

### Check 3 — G4: canonical-path-vs-factory-tuple — RESOLVED

DECISION 5 (lines 98-103) closes G4 explicitly: the fix reads the canonical
`config.task_output_file(phase, task)` in-caller and does NOT extend the
`_subprocess_factory` tuple; file 03's UNVERIFIED tension is resolved in favor of
file 01. Tests write the fake NDJSON to that canonical path. This matches file 01 §2
(no signature change). G4 — RESOLVED.

### Check 4 — "Files to change" concrete and line-consistent — PASS

The list (lines 105-110) is concrete and consistent with the analyst-verified line
numbers: (1) `models.py` add `TaskStatus.PASS_RECOVERED` + `is_success`; (2)
`executor.py` recovery branch at the per-task switch (@1014-1020, live-confirmed) +
aggregation `.is_success` (@1278, live-confirmed); (3) `tests/sprint/test_executor.py`
positive + guard tests; (4) no `.claude/` sync needed, `make verify-sync` unchanged.
Verification gates (lines 112-116) are UV-only and correctly scoped. PASS.

### Check 5 — NEW contradictions between file 04 and files 01/03 — NONE

- **vs file 01:** File 04's DECISIONS 1/3/5 are the concrete selection of the exact
  options file 01 §4-§5 laid out (new is_success-True member OR is_success
  aggregation; no signature change). No conflict — file 04 picks among file 01's
  own alternatives. Consistent.
- **vs file 03:** File 03 deferred the enum choice and the weak `!= FAIL` assertion
  to "researcher-01/02's fix"; file 04 supplies that decision and strengthens the
  assertion. File 04 supersedes the weak assertion rather than contradicting an
  asserted fact — file 03 never claimed `!= FAIL` was sufficient. The G4 UNVERIFIED
  in file 03 is now closed by file 04 DECISION 5. Consistent.
- **vs file 02:** File 04 EXPLICITLY overrides file 02's bare-INCOMPLETE TL;DR
  (lines 12-18, 30-34: "Reusing INCOMPLETE is **rejected**"). The override is
  stated, so the residual file-02 inconsistency is now documented and resolved by an
  authoritative tie-breaker — exactly the reconciliation the prior FAIL demanded.

No NEW contradiction introduced.

### Residual

- **G3 (MINOR, verification-tag vocabulary)** was not a re-check target and is not
  blocking; file 04 itself states its facts are rf-qa-reconfirmed (22/22) and the
  analyst independently re-verified the load-bearing claims live. Non-blocking.

### Updated Gap Status

| Gap | Prior severity | Status after file 04 |
|-----|---------------|----------------------|
| G1  | CRITICAL | RESOLVED — success-valued PASS_RECOVERED; INCOMPLETE refutation code-verified |
| G2  | IMPORTANT | RESOLVED — is_success/PASS_RECOVERED/phase-level assertions + exit-124 guard |
| G3  | MINOR | Non-blocking; not in re-check scope |
| G4  | MINOR | RESOLVED — canonical-path decision closed (DECISION 5) |

---

## UPDATED VERDICT: PASS

File `research/04-gap-fill-crux-reconciliation.md` authoritatively resolves the
blocking gaps. It declares itself the tie-breaker over file 02, selects a
success-valued `TaskStatus.PASS_RECOVERED` (NOT bare INCOMPLETE), and grounds the
rejection of INCOMPLETE in two code-true facts the analyst re-verified live
(`models.py:52-53` INCOMPLETE ∈ is_failure; `executor.py:1018` exit 124 → INCOMPLETE,
so making INCOMPLETE success-valued would regress genuine timeouts). The CRITICAL G1
contradiction is reconciled and the file-02 override is explicitly stated. G2 is
resolved with strengthened is_success/PASS_RECOVERED/phase-level assertions plus the
exit-124 non-regression guard, and G4 is closed in favor of the canonical-path
approach. The "Files to change" list is concrete and consistent with the verified
line numbers, and no new contradiction is introduced against files 01/03. Only the
non-blocking MINOR G3 (verification-tag vocabulary) remains, which does not gate the
build. The research corpus is now internally consistent on the CRUX and ready for
task-file construction.

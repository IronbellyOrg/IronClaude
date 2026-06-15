# Self-Review — PRD scope-discovery missing-artifact fix proposal

Reviewer: self-review agent · Date: 2026-06-08 · Verdict: **CONCERNS (1 blocker, 2 must-flag)**

Scope: sanity-check the PROPOSED two-atom fix in `REPORT.md.draft`. No code applied.
All citations below were re-read from source this session.

---

## 1. TESTS — regression surface

**No existing test relies on a STANDARD step that ERRORs being allowed to continue.**
Confirmed by reading the PRD test suite:

- `tests/cli/prd/test_e2e.py` — the only failure-injection hook is `_mock_process_factory(step_overrides=...)` (line 224-253). **No e2e scenario passes a non-zero exit override**, so no test exercises (and therefore none depends on) the "STANDARD step ERRORs → pipeline continues" path that Atom 1 removes. Atom 1 cannot break a currently-green e2e test on that axis.
- `test_e2e_budget_exhaustion` (test_e2e.py:519-573) DOES depend on a failure halting, and I traced it under Atom 1: budget 50, estimates parse-request(15)+scope-discovery(15)+research-notes(15)=45, then sufficiency-review needs 10 → `can_allocate(10)` fails → `QA_FAIL_EXHAUSTED` (executor.py:664-668). sufficiency-review is **STRICT** (gates.py:358), so it halts under BOTH current and Atom-1 code. Atom 1 reclassifies `QA_FAIL_EXHAUSTED` as a hard failure but the halt *step* is unchanged, and the test only asserts `halt_step is not None` / `halt_reason is not None` (not the reason string). **Still passes.**
- `test_models.py:62-75` asserts `is_failure` membership exhaustively but says nothing about the new `is_hard_failure` property → unaffected. This is the correct home for the new-property regression test.
- `test_integration.py:269` (`outcome != "halt"`) is a QA fix-cycle path using `QA_FAIL` (a `needs_fix_cycle` status, NOT in `is_failure`) → unaffected by Atom 1.

**Required new regression tests (report already names the first; add the rest):**
1. STANDARD step returning `ERROR` MUST halt; STANDARD step returning `VALIDATION_FAIL` MUST NOT halt. (report has this)
2. `is_hard_failure` membership unit test in test_models.py: ERROR/TIMEOUT/QA_FAIL_EXHAUSTED/HALT → True; VALIDATION_FAIL/PASS/SKIPPED/QA_FAIL → False. (closes the VALIDATION_FAIL-exclusion risk the report names but does not test)
3. Atom 2 end-to-end: a Stage-A builder whose required input is absent yields `outcome=="halt"` with the producer-step in `halt_reason`, NOT a raw traceback. Cover BOTH a STRICT consumer (research-notes) and — given finding #B below — a STANDARD consumer (scope-discovery).

---

## 2. EDGE CASES

- **VALIDATION_FAIL correctly NOT halted by Atom 1.** ✅ `is_hard_failure` (ERROR/TIMEOUT/QA_FAIL_EXHAUSTED/HALT) excludes VALIDATION_FAIL. The intentional non-fatal STANDARD gate-quality path (executor.py:730-741: exit 0, gate-fail → VALIDATION_FAIL, artifact persisted at 748) is preserved. Matches the documented intent at 736-741.
- **HALT in is_hard_failure is correct, not redundant.** ✅ HALT means "halt," but the *current* loop only acts on HALT when the step's gate is STRICT (567-569). Putting HALT in `is_hard_failure` is exactly what makes a HALT result halt regardless of tier — this is load-bearing for Atom 2 (see #A below), not decorative.
- **QA_FAIL (non-exhausted) correctly EXCLUDED.** ✅ QA_FAIL is `needs_fix_cycle` (models.py:158-161), not in `is_failure` at all, so the 567 guard never even sees it; its retry cycle is untouched.
- **MissingArtifactError ⊂ FileNotFoundError ⊂ OSError — no collision with executor.py:701.** ✅ The `except OSError` at 701 guards the *post-subprocess* output_file read; Atom 2's catch is at the *pre-subprocess* `_build_prompt` call (672). Different code region, no shadowing.

---

## 3. REQUIREMENTS — does it stop the FileNotFoundError CLI traceback?

- **Source halt (Atom 1):** ✅ scope-discovery ERRORs (exit≠0) → `ERROR` (executor.py:770-771) → `is_hard_failure` → loop halts at scope-discovery before research-notes ever builds. The reported crash chain is severed at the source. Atom 1 ALONE prevents the reported crash (the report states this; confirmed).
- **Backstop (Atom 2):** intended to HALT gracefully if any builder still reaches a missing required input. **Effective for STRICT consumers, but see the two findings below — as drafted it is mechanically wrong for 2 of the 5 reads and has a tier-coupling hole.**

---

## BLOCKER

### #A (BLOCKER) — Atom 2's `_read_required` helper cannot convert 2 of the 5 cited reads; they are `_load_json`, not `_read_file`.

The report says "convert the five REQUIRED Stage-A `build_*` reads (`prompts.py:158, 257, 258, 340, 440`)" using `_read_required` (which wraps `_read_file` → returns `str`). Re-reading prompts.py:

- 158 → `_load_json(config.task_dir / "parsed-request.json")`  ← **JSON, not _read_file**
- 257 → `_read_file(config.task_dir / "scope-discovery-raw.md")`  ✅ str
- 258 → `_load_json(config.task_dir / "parsed-request.json")`  ← **JSON, not _read_file**
- 340 → `_read_file(config.task_dir / "research-notes.md")`  ✅ str
- 440 → `_read_file(config.task_dir / "research-notes.md")`  ✅ str

`_load_json` (prompts.py:37-39) calls `json.loads(path.read_text(...))` and returns a `dict`. Wrapping it in the string-returning `_read_required` is a type error and would corrupt the JSON consumers. Lines 158/258 still raise `FileNotFoundError` on a missing `parsed-request.json` (from `read_text`), so they MUST be guarded too — but with a **`_load_json_required(path, producer_step) -> dict`** sibling helper, not `_read_required`. **Fix the report**: split the helper into a string variant (257/340/440) and a JSON variant (158/258), or have `_read_required` return bytes/str and add a separate JSON-required path. As written, Atom 2 is not mechanically applyable to all five lines.

---

## MUST-FLAG (not blockers, but the report must state them)

### #B — Atom 2 ALONE does not halt when the missing-input consumer is a STANDARD-gated step (the coupling the task asked to verify).

Trace: Atom 2 catches `MissingArtifactError` at 672 → returns `PrdStepResult(status=HALT)`. In `run()` the loop hits `if step_result.status.is_failure:` (567) — HALT ∈ is_failure (models.py:148) ✅ — then **`if gate and gate.enforcement_tier == "STRICT": break`** (569). So WITHOUT Atom 1, a HALT on a **STANDARD** step does NOT break the loop. Concretely: `build_scope_discovery_prompt` does a REQUIRED read of `parsed-request.json` (line 158) and **scope-discovery is STANDARD** (gates.py:331-335). If parse-request produced no artifact, Atom-2-alone would HALT-classify scope-discovery but the loop would CONTINUE to research-notes (which then also raises → HALT → STRICT → finally halts). Net: Atom 2 is only fully correct **coupled with Atom 1**. The draft's "Revert independently; Atom 1 alone already prevents the reported crash" is true, but the symmetric warning is missing: **Atom 2 must not ship without Atom 1.** Add that to Risk + Rollback. (Atom 1-alone is the safe partial; Atom 2-alone is the unsafe partial.)

### #C — Evidence line citing "five reads" conflates two helper families.

Draft Diagnosis (line 30) and Evidence (line 45) describe all five Stage-A reads as `_read_file`/"unguarded reads," but 158/258 go through `_load_json`. The smoking-gun argument (guarded Stage-B vs unguarded Stage-A) still holds — `_load_json` is equally unguarded — but the report should name `_load_json` explicitly so the implementer doesn't blindly `sed` `_read_file`→`_read_required`. Cosmetic relative to #A but same root cause; fixing #A fixes this.

---

## 4. FOLLOW-UP / residual risks

- **Atom ordering / coupling note (from #B):** report should add an explicit "Atom 2 depends on Atom 1 for STANDARD-consumer correctness; ship together or ship Atom 1 first." Atom 1 is independently revertable; Atom 2 is not independently *sufficient*.
- **Helper split (from #A):** task file must call out two helpers (`_read_required` for str, a JSON-required variant for 158/258) or the implementer will produce a type bug.
- **Root trigger still undiagnosed** (0.3s non-zero `claude` subprocess exit) — correctly scoped out by the draft as environment-specific; the "capture scope-discovery-error.txt on ERROR" follow-up is a good add and I endorse it.
- **`_build_prompt` is overridden in tests** (test_e2e.py:549, monkeypatched to a lambda). The Atom 2 catch must wrap the REAL `_build_prompt` call at executor.py:672, not live inside `_build_prompt` only — otherwise tests that stub `_build_prompt` would bypass the catch. Recommend the try/except sit at the 672 call site (as the report says) so it is exercised by the real builder path. Confirm the new Atom-2 e2e test does NOT stub `_build_prompt`.

---

## Checklist summary

```
✅ Tests: no current test depends on STANDARD-ERROR-continues; budget-exhaustion halt still passes under Atom 1 (traced)
⚠️ Edge cases: VALIDATION_FAIL exclusion correct; HALT-in-hard-failure correct; QA_FAIL excluded correctly
⛔ BLOCKER #A: _read_required can't wrap _load_json (prompts.py:158, 258) — needs a JSON-required helper
⚠️ MUST-FLAG #B: Atom 2 alone won't halt on a STANDARD consumer (scope-discovery reads parsed-request.json@158) — couple with Atom 1
⚠️ MUST-FLAG #C: report mislabels 158/258 as _read_file; they are _load_json
✅ Requirements: Atom 1 severs the reported crash at source; Atom 2 (once #A fixed) is the backstop
📓 Follow-up: helper split, atom-coupling note, ensure Atom-2 e2e test uses the real _build_prompt
```

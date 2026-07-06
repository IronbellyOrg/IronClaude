# Reviewer Card 3 — REFACTORER / Correctness (Opus)

**Ensemble:** /sc:reflect UC-1 pre-execution, PR #124 tasklist
**Tasklist:** `.dev/tasks/to-do/TASK-RF-20260604-035221/TASK-RF-20260604-035221.md`
**Spec:** `.dev/tasks/build-requests/BUILD-REQUEST-pr124-merge-resolution.md`
**Stance:** adversarial; correctness + best-practice; hunt regressions other reviewers miss.
**Grounding mode:** `git show` against `origin/feat/sprint-auto-resume-v435` (aedd0104) and `origin/master` only. No checkout, no tracked-file mutation.

---

## Verdict

**WOULD-IT-MERGE-CORRECTLY: YES, with one MEDIUM defect to correct before execution** — the planner-level fix (the load-bearing half of Deliverable B) is semantically sound, complete, and the RED→GREEN guard is genuine on assertions (a)+(b). The conflict resolutions (Deliverable A) are correct. The one real risk is a **test-design trap inherited from research 03's template** (optional assertion (c) + `PASS_TRANSCRIPT`) that, if the implementer copies the template literally, makes part of the test pass vacuously and could mask a Signal-B regression. The tasklist's own prose (Step 4.1) demotes (c) correctly, but the embedded template fights it.

- **HIGH findings: 0**
- **MEDIUM findings: 2** (F1 test-vacuity trap; F2 RED-mechanism scope gap)
- **LOW findings: 3**
- **best_practice_grade: 4 / 5**

No regression of currently-passing behavior is introduced by the prescribed edits (verified: no existing `tests/sprint/` fixture emits `pass_recovered`, so widening `is`/`is not PASS` → `is_success` keeps every current assertion green — research 02 §8 / research 03 §0.4, independently re-confirmed below).

---

## 1. Semantic soundness of Deliverable B — PASS_RECOVERED coupling (GROUNDED, CORRECT)

**Re-grepped both branches.** `git show origin/feat/sprint-auto-resume-v435:.../resume/{planner,integrity,drift}.py | grep -nE 'TaskStatus\.PASS'`:

- `planner.py:163` `bt.persisted_status is not TaskStatus.PASS` (rerun set) — IN SCOPE.
- `planner.py:217` `persisted_status=TaskStatus.PASS` — **synthetic literal assignment in `_emit_prior_tail_boundary`, NOT a comparison.** Correctly excluded by the tasklist (Step 3.1 explicitly calls this out: "the synthetic `BoundaryTask(persisted_status=TaskStatus.PASS, ...)` literal ... is NOT modified"). Verified GROUNDED at `planner.py:213-221`: it is a hand-built prior-tail boundary whose status is *known* PASS — widening it would be wrong. **The tasklist gets this right.**
- `planner.py:318` `is TaskStatus.PASS` (last_completed) — IN SCOPE.
- `planner.py:324` `is not TaskStatus.PASS` (next_unfinished) — IN SCOPE.
- `integrity.py:123` `signal_a_pass = lc.persisted_status is TaskStatus.PASS` — IN SCOPE.
- `integrity.py:129` `signal_b_pass = derived is TaskStatus.PASS` — IN SCOPE (gated, see §2).
- `drift.py:93` `bt.persisted_status is TaskStatus.PASS` — IN SCOPE.

**Exactly 6 task-level identity sites. Research 02's count is correct and complete.** I additionally swept `resume/models.py` and `resume/__init__.py` for hidden `== "pass"` / `.value` / `== TaskStatus` comparisons — **zero additional sites** (`models.py` only declares the `persisted_status: TaskStatus | None` field; `__init__.py` has none). `planner.py:383` `PhaseStatus(...).is_success` is phase-level and already PASS-family-safe — tasklist correctly forbids touching it (Step 3 preamble + research 02 §3). **No missed identity site. [GROUNDED]**

**None-safety is correct.** `_coerce_task_status` returns `TaskStatus | None` (`planner.py:157` populates `persisted_status` from it; research 03 §0.3 shows the `try/except → None` body). The "done" predicate `bt.persisted_status is not None and bt.persisted_status.is_success` and "not done" `bt.persisted_status is None or not bt.persisted_status.is_success` are exact De Morgan complements and both short-circuit the `None` before the attribute access. **No AttributeError risk; behavior for junk/None status is preserved (treated as "not done") — matches pre-fix semantics. [GROUNDED, planner.py:157 + research 03 §0.3]**

---

## 2. The Signal B design decision (GROUNDED — tasklist handles it CORRECTLY, but see F1)

I traced the integrity gate end-to-end at `integrity.py:95-152`:

```
signal_a_pass = lc.persisted_status is TaskStatus.PASS          # :123
derived       = _classify_transcript(transcript)                 # :127
signal_b_pass = derived is TaskStatus.PASS                        # :129
...
validated = signal_a_pass and signal_b_pass and artifacts_ok     # :148  (AND of all three)
if not validated: lc.suspect = True; return False, [lc], lc
```

`_classify_transcript` (master `rerun_tasks.py:547-593`) is typed `-> TaskStatus` and its return set is `{PASS, INCOMPLETE, FAIL_RECOVERABLE, FAIL_TERMINAL}` — **never `PASS_RECOVERED`** (GROUNDED — I read the full body; no branch yields PASS_RECOVERED). Research 02 §4b's nuance is **confirmed and even sharper**: for a *real* recovered tail (non-zero exit, error result-event), `_classify_transcript` returns `FAIL_TERMINAL`/`FAIL_RECOVERABLE`, so `signal_b_pass` is False, so `validated` is False **regardless of the Signal A widening** — the AND at :148 makes Signal B independently veto a recovered seam.

**The tasklist surfaces this correctly:**
- OQ-1 + Step 3.7 gate it as a `needs_human_decision` HALT with Opt-1 (minimal, planner-level only) vs Opt-2 (deeper, teach Signal B), **no auto-default** (Step 3.8 default branch = NO code change). This satisfies the project rule `feedback_human_decision_items_must_halt.md` (write PENDING + halt the dependent mutation; never ship a default). **[GROUNDED — Step 3.7/3.8]**
- Step 4.1 makes the load-bearing RED→GREEN signal the **planner assertions (a)+(b)**, and explicitly demotes the integrity assertion (c) to optional, "do NOT let that optional assertion be the load-bearing signal." **This is the correct design call.** [GROUNDED]

**This is exactly the pattern that sc:reflect exists to confirm — the tasklist did not collapse the design question into a silent one-line swap.** Good.

### F1 (MEDIUM) — Test-vacuity trap: research 03's template embeds (c) as a hard assertion AND uses `PASS_TRANSCRIPT`, contradicting the tasklist's own demotion

This is the finding most likely to be missed by reviewers who read the tasklist prose but not the template it points at.

`PASS_TRANSCRIPT` (test_resume.py:34-37) = `{"type":"result","subtype":"success","is_error":false}` with `output_tokens:42`. `_classify_transcript(PASS_TRANSCRIPT)` → **`PASS`** (master `rerun_tasks.py:582`: `not is_error and total_output_tokens > 0 → PASS`). [GROUNDED both files]

Research 03 §1.5's recommended test body writes `PASS_TRANSCRIPT` to `phase-3-task-T03.01-output.txt` **and** asserts `report.validated_last is True` as line (c). The problem:

1. **(c) is not a RED→GREEN discriminator for the planner fix.** With `PASS_TRANSCRIPT`, `derived = PASS` → `signal_b_pass = True` *even in the unfixed integrity code*. And `signal_a` for a persisted `pass_recovered` status: unfixed `lc.persisted_status is TaskStatus.PASS` is **False** (PASS_RECOVERED is not PASS) → unfixed `validated = False`. So (c) is RED on the *integrity Signal A* axis, not the planner axis — it conflates two different fixes and would only flip GREEN if Step 3.6 (signal_a widening) is applied. That coupling is acceptable *only if Step 3.6 always runs* (it does — it is unconditional), but it makes (c) a load-bearing assertion on integrity, which Step 4.1 explicitly says it must NOT be.
2. **Vacuity risk the other way:** because the fixture's transcript is `PASS_TRANSCRIPT` (not a *real* recovered/errored transcript), the test does **not** exercise the genuine recovered-tail scenario where `_classify_transcript → FAIL_*`. So even a GREEN (c) does **not** prove the integrity gate validates a *real* recovered seam — it proves it validates a seam whose transcript happens to score PASS. A reader could mistake GREEN-(c) for "Signal B handles recovered tails," which is false (that's the whole OQ-1 Opt-2 gap).

**Why this is MEDIUM not HIGH:** the tasklist (Step 4.1) *does* instruct that (c) be guarded behind a comment and non-load-bearing, and assertions (a)+(b) carry the guard. If the executor follows the tasklist prose, the test is correct. The risk is that the executor copies research 03's literal template (which has (c) as an un-commented hard `assert`) instead of honoring Step 4.1's demotion. **Recommendation:** Step 4.1 should state explicitly: "OMIT assertion (c) entirely, OR write it as `# (c) optional — depends on OQ-1 Signal-B decision; NOT load-bearing` with the assert commented out, because `PASS_TRANSCRIPT` makes Signal B pass trivially and a real recovered transcript would make it FAIL." As written, Step 4.1 says "Optionally include ... ONLY guarded behind a comment" — this is *almost* right but leaves the door open to a literal-template copy. Tighten to forbid the bare assert.

---

## 3. Regression-test validity — RED→GREEN genuineness (GROUNDED; one scope gap = F2)

**Will it go RED pre-fix on (a)+(b)?** YES. [GROUNDED via planner.py:160-164, 316-328]
- Pre-fix `rerun_task_ids = [bt for bt in boundary if bt.persisted_status is not TaskStatus.PASS]`: T03.01=`PASS_RECOVERED` → `is not PASS` True → **T03.01 wrongly IN rerun_task_ids** → assertion (a) `"T03.01" not in rerun_task_ids` FAILS. RED confirmed.
- Pre-fix `passed = (bt ... if bt.persisted_status is TaskStatus.PASS)`: T03.01 excluded → `last_completed` never assigned to it → `roles["T03.01"] == "last_completed"` raises KeyError/fails. RED confirmed.

**Will it go GREEN post-fix?** YES. [GROUNDED]
- Post-fix T03.01 (`pass_recovered`, `is_success` True) excluded from rerun; T03.02 (`incomplete`, `is_success` False) → `rerun_task_ids == ["T03.02"]`. ✓
- `passed` includes T03.01 (sole success) → `passed[-1].role = "last_completed"`; `non_pass` first = T03.02 → `next_unfinished`. ✓

**Non-vacuous:** the granularity is TASK (result.json has `task_results`), so the `if task_results:` branch at planner.py:150 is taken (not the transcript-discovery else). The fixture genuinely drives all three planner predicates. **Not vacuous on (a)+(b). [GROUNDED]**

### F2 (MEDIUM) — RED mechanism only proves planner sites; integrity/drift edits get NO RED→GREEN coverage

Step 4.2's RED demo "temporarily revert ONLY the three planner predicates ... then restore." This proves the **planner** fix (3 of 6 sites). The **integrity Signal A (3.6)** and **drift (3.5)** edits have **no dedicated RED→GREEN guard** — they're only covered by the full-suite green gate (Phase 5), which research 02 §8 confirms has *zero* `pass_recovered` fixtures touching integrity/drift. So:
- A future refactor could silently re-break `drift.py:93` or `integrity.py:123` and no test would catch it (the new test asserts (a)+(b) planner-only; (c) is demoted/optional).
- This is a **coverage gap**, not an active regression — the edits themselves are correct. But "fix without a guarding test" is the exact anti-pattern this PR is correcting for the planner. **Best-practice ding.** Recommendation: either (i) un-demote a *drift* assertion into the new test (`DriftAssessor` over the same plan → assert the recovered task is in `recorded_completed`), which IS a clean planner-independent RED→GREEN guard and does NOT hit the Signal-B trap; or (ii) explicitly record in the Task Summary that integrity-A/drift widenings ship guard-free by design, gated only by the full suite. Option (i) is strictly better and cheap.

**Severity MEDIUM (not HIGH):** no currently-passing behavior breaks; the gap is missing *forward* protection, not a live defect.

---

## 4. Ordering / dependency soundness (GROUNDED, CORRECT)

The multi-stop rebase sequencing is **correct and impressively precise**:
- Worktree created P1.3 (detached HEAD — correctly avoids the `feat/sprint-auto-resume-v435 already checked out in SprintReRun` collision; this is a real git constraint and the `--detach origin/...` form is the right escape). [tasklist Step 1.3, GROUNDED against the documented SprintReRun worktree]
- Stop A (commit `a4947980`) = {CHANGELOG.md, commands.py}; executor.py surfaces at Stop B (style commit `aedd0104`) reached via Step 2.5's `rebase --continue`. The tasklist sequences executor.py resolution at Step 2.5 (Stop B), NOT at Stop A — **this matches the empirically-probed rebase behavior** and is the correct stop. Step 1.4/1.5 explicitly forbid flagging executor.py's *absence* at Stop A as a deviation. [Steps 1.4, 1.5, 2.5 — internally consistent]
- Phase 3/4 working-tree edits happen while the rebase is *paused* at Stop B; Step 6.1 CASE 1 folds them into the final replayed `aedd0104` via `rebase --continue`. Preconditions chain cleanly: every Phase 2-6 step's inputs are produced by an earlier step. No step references an artifact not yet created. [GROUNDED across phases]

One subtlety the tasklist handles: research files 01/02 used `merge-tree` (single snapshot) line numbers, but the rebase is multi-stop with shifting lines — Step 3.x correctly mandates "re-locate by predicate TEXT, not raw line number." Good defense against line-drift. **[GROUNDED]**

LOW (F3): Step 2.5 says executor.py "auto-resolved to is_success, no manual edit needed" is an ACCEPTABLE outcome. That's correct (the desired line is master's), but the contingency note that `models.py` "does NOT conflict in the rebase" rests on the branch's models.py change being "a cosmetic `is_failure` reflow that master already carries" — I could not independently re-verify the reflow is byte-identical to master's via `git show` in this pass (research 01 §auto-merge corroboration asserts `models.py` 0 markers under *merge-tree*, but a *rebase* replays differently). The tasklist's contingency (Step 1.4: "IF an unexpected models.py conflict arises, keep master's PASS_RECOVERED + PASS-family is_success") is a safe fallback, so this is LOW, not a blocker.

---

## 5. Best-practice — scope discipline (GROUNDED, EXCELLENT)

- **A+B same-merge requirement honored:** Phase 6 commits both deliverables in the rebased branch; Task Overview states "Correctness requires BOTH A and B in the same merge." ✓ Matches BUILD-REQUEST goal lines 5-15. ✓
- **Out-of-scope couplings correctly recorded as follow-ups, NOT fixed:** `handoff.py:34` (`record.status != TaskStatus.PASS.value`, master-only) and `rerun_tasks.py:1192` (`tr.status is TaskStatus.PASS`) are logged in the Task Summary "Out-of-Scope Follow-Up" block as "pre-existing same-bug-class coupling, independent of this PR." [GROUNDED — tasklist:342-343, research 02 §7]. I re-confirmed both are **identical or master-only, NOT introduced by this PR's merge** (research 02 §7 table; handoff.py does not exist on the PR branch). Touching them here would be scope creep — the tasklist correctly defers. ✓
- **No speculative additions:** the tasklist builds exactly the 6-site widening + 1 test + 4 conflict hunks. No refactor of the resume package. Matches BUILD-REQUEST "Out of scope" (lines 108-112). ✓
- **CI format gate discipline** (Step 5.4: `ruff format --check` SEPARATE from `make lint`) correctly encoded — matches memory `reference_make_lint_vs_ci_ruff_format.md`. ✓
- **Fork-PR + `.claude/` staging discipline** (Steps 6.2/6.3) correctly encoded. ✓

**best_practice_grade: 4/5.** Loses one point for F1+F2: the test surface under-protects the non-planner edits and embeds a template that can pass vacuously on (c). Everything else (scope, HALT-gating, rebase rigor, None-safety, format-gate, fork discipline) is exemplary.

---

## 6. Asymmetric-cost check — does the fix close the exact crash-tail scenario? (GROUNDED, YES for the primary path)

The whole point: auto-resume must NOT re-run a recovered tail task. Post-fix:
- `rerun_task_ids` excludes the recovered task (planner.py:163 widened) → **not re-run.** ✓ This is the exact asymmetric-cost scenario (re-running completed work) and the fix closes it.
- `last_completed` selects the recovered task (planner.py:318 widened) → resume anchors *after* it. ✓
- `next_unfinished` no longer counts the recovered task as unfinished (planner.py:324 widened) → resume does not anchor *too early*. ✓

**Residual mis-handling AFTER the planner fix (the honest caveat):** if the integrity gate runs on a *real* recovered seam (transcript scores `FAIL_*`), `signal_b_pass` is False → `validated=False` → `lc.suspect=True` → integrity **STOP** on legitimate recovered work (integrity.py:148-150, GROUNDED). So a recovered tail is **not re-run** (planner is correct) but **could still trip an integrity hard-STOP** unless OQ-1 Opt-2 is taken. The tasklist is honest about this (OQ-1, Step 3.7) and gates it as a human decision rather than silently shipping a half-fix. **This is a known, surfaced, gated residual — not an unmapped gap.** The asymmetric *primary* cost (re-running) is closed; the *secondary* cost (false STOP) is explicitly deferred to a human decision. Acceptable for a "mergeable + correct primary path" deliverable. ✓

LOW (F4): the BUILD-REQUEST line 87-88 asks for "an integrity-gate assertion that a recovered seam validates (signal_a/signal_b pass)." The tasklist *cannot fully satisfy this* for a real recovered transcript under Opt-1 (Signal B will fail) — and correctly says so. There is a latent mismatch between the BUILD-REQUEST's stated acceptance ("integrity gate validates") and the achievable Opt-1 reality. The tasklist resolves it the right way (gate the gap to OQ-1) but a strict reading of the BUILD-REQUEST acceptance criterion is **not** met under the default PENDING/Opt-1 path. Flag so the user knows the BUILD-REQUEST's own acceptance line is partially superseded by OQ-1.

---

## 7. Regression risk summary (the HIGH-priority lens)

**No HIGH regression of currently-passing behavior found.** Specifically verified:
- Widening `is/is not TaskStatus.PASS` → `is_success` across the 6 sites does **not** break any existing `tests/sprint/` test: re-confirmed (research 02 §8 / research 03 §0.4) that **no current fixture emits `pass_recovered`**, and for every existing `pass`/`incomplete`/`fail_recoverable` fixture, `is_success` is logically identical to `== PASS` (PASS→True both ways; others→False both ways). The only enum value where the predicates *diverge* is `PASS_RECOVERED`, which no existing test produces. **Behavior-preserving for the entire current suite. [GROUNDED]**
- executor.py "TAKE MASTER" (`is_success`) is already master's line — taking it is a no-op relative to master, and only *discards* the PR's stale `== PASS` regression. No behavior change vs. master. ✓
- The synthetic `planner.py:217` literal is correctly left untouched (changing it would be the one real self-inflicted regression — tasklist avoids it). ✓

---

## UNMAPPED correctness gaps

1. **(F2)** integrity-A (3.6) and drift (3.5) widenings have **no dedicated RED→GREEN test** — only full-suite coverage, which has no `pass_recovered` integrity/drift fixture. Forward-protection gap. *Fix: add a drift assertion to the new test (planner-independent, avoids the Signal-B trap).*
2. **(F1)** research-03 template's hard assertion (c) + `PASS_TRANSCRIPT` can pass vacuously / conflate planner vs integrity-A axes if copied literally. *Fix: Step 4.1 should forbid the bare `assert report.validated_last is True`, not merely "guard behind a comment."*
3. **(F4)** BUILD-REQUEST acceptance line ("integrity gate validates a recovered seam") is **not achievable** under default PENDING/Opt-1 for a *real* recovered transcript; tasklist correctly defers via OQ-1 but the acceptance criterion is partially superseded — worth an explicit note to the user.

None of these block merge of the *primary* (planner) correctness fix.

---

## Findings table

| ID | Sev | Finding | Evidence |
|----|-----|---------|----------|
| F1 | MEDIUM | Optional assertion (c) + `PASS_TRANSCRIPT` can pass vacuously / conflates planner vs Signal-A axes if executor copies research-03 template literally | integrity.py:129/148; rerun_tasks.py:582; test_resume.py:34-37; tasklist Step 4.1 |
| F2 | MEDIUM | integrity-A (3.6) + drift (3.5) widenings ship with no dedicated RED→GREEN guard; full suite has no pass_recovered integrity/drift fixture | tasklist Step 4.2 (planner-only revert); research 02 §8 |
| F3 | LOW | models.py "no rebase conflict" rests on a reflow being master-identical; not re-verified under *rebase* replay (merge-tree only). Safe fallback exists (Step 1.4) | research 01 auto-merge table; tasklist Step 1.4 |
| F4 | LOW | BUILD-REQUEST acceptance ("integrity gate validates recovered seam") not achievable under Opt-1/PENDING for a real recovered transcript; correctly deferred to OQ-1 | BUILD-REQUEST:87-88; OQ-1 |
| F5 | LOW | `planner.py:217` synthetic literal correctly excluded — confirming the tasklist did NOT over-widen (positive finding) | planner.py:213-221; tasklist Step 3.1 |

---

## Bottom line

Execute the tasklist as written and PR #124 merges **correct on its load-bearing path**: 4 conflict hunks resolved exactly, 6 resume sites widened None-safely, a genuine planner RED→GREEN guard, the Signal-B design question correctly HALTed as a human decision rather than silently defaulted, and out-of-scope couplings deferred. Before execution, **tighten Step 4.1 to forbid the bare `validated_last` assert (F1) and add a planner-independent drift assertion to the new test (F2)** — both are cheap and close the only correctness/best-practice gaps. No HIGH regression risk.

**best_practice_grade: 4/5**

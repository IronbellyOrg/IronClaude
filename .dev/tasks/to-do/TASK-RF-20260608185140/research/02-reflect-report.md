# /sc:reflect — UC-2 Post-Execution Deviation Audit

**Task:** TASK-RF-20260608-150011 — Fix sprint-recovery stranded-deliverables + stale-checkpoint defects
**Diff:** `b05e0fe1..HEAD` (commit `c0d56f18`; 4 src + 2 test, +509/−29)
**Mode:** post · **Tier reached:** 2 (forced by `--depth deep`) · **Reviewers:** 3 (analyzer / qa / integration; full model+vendor diversity)
**Verdict:** ⛔ **PARTIAL — 2 confirmed Regressions + 2 Drift. Work-unit must NOT be marked Done. Remediation required.**

---

## Headline

The implementation is **green on its test suite (54/54 in the two modified files; 1163 claimed full-suite) and passed its inline rf-qa gate** — yet an executor-disjoint Tier-2 ensemble independently reproduced **three real defects**, two of which directly contradict the task's own hard acceptance criteria. This is precisely the spec-literal-token / integration-orphan blindspot the task's Step 8.3 rationale predicted same-frame QA would miss. Every blocking finding below was **re-verified by the orchestrator** (re-Read + executable PoC), not merely reviewer-claimed.

## Confirmed blocking defects

### 🔴 DEV-1 — Regression (HIGH): PRIMARY checkpoint re-run is dead on arrival
`src/superclaude/cli/sprint/rerun_tasks.py:1616-1630`

The PRIMARY post-merge re-verify (the centerpiece of item 4.3) shells out:
```
uv run superclaude sprint rerun-tasks --phase N --tasks <chk_tid> --no-verify-checkpoints
```
…with **no `INDEX_PATH` positional**, which `rerun-tasks` declares as a *required* `@click.argument` (`commands.py:721`). Independently reproduced:
```
$ uv run superclaude sprint rerun-tasks --phase 1 --tasks T01.05 --no-verify-checkpoints
Error: Missing argument 'INDEX_PATH'.   # exit 2
```
`check=False` swallows the exit-2, so PRIMARY **re-runs nothing, writes no fresh verdict**, and `_mirror_checkpoint_to_release_dir` then no-ops on an unchanged source. The spec's item-4.3 acceptance — "re-run that single task so it writes a FRESH real verdict" — is unmet. Only the FALLBACK path works (and is the only path the e2e fixture exercises). **Fix:** insert `str(config.index_path)` as the positional before `--phase`.

### 🔴 DEV-2 — Regression (MED): never-auto-PASS invariant is violable
`src/superclaude/cli/sprint/checkpoints.py` (`_render_recovered_checkpoint` "Verification Criteria" section) → read by `executor.py:2518-2519`

The re-stamped report interpolates the tasklist's verification block **verbatim**. The gate reader does a case-insensitive substring match for `STATUS: PASS` / `**RESULT**: PASS`. Reproduced via PoC:
```
verification_block = "...confirm **RESULT**: PASS from the smoke suite..."
→ rendered report.upper() contains "**RESULT**: PASS"
→ _check_checkpoint_pass() returns True   # on a report whose ## Result is `UNKNOWN`
```
A re-stamped "UNKNOWN" checkpoint can therefore read as **PASS** at the gate whenever the phase's checkpoint task prose literally contains the gate token — ordinary wording for a checkpoint's own pass-criteria. This contradicts the item-4.1 HARD CONSTRAINT ("NEVER auto-PASS"). The injection vector partly pre-exists in the missing-checkpoint recovery renderer, but this commit newly stakes its safety claim on it. **Fix:** post-render, assert/strip the two gate tokens (case-insensitive) from `verification_section`, `entry.name`, and `evidence_lines`; add a per-field injection regression test.

### 🟠 DEV-3 — Drift (MED): deliverable landing-verify can mask a stranding
`src/superclaude/cli/sprint/recovery.py:581-585`

```python
landed = (canonical_dest.is_file() and size>0) or (declared.is_file() and size>0)
```
The OR's second clause checks the **cwd-resolved** `declared` path, independent of whether relocation reached `canonical_dest`. Cleanest confirmed hole: when `bundle.artifacts_produced` is empty, relocation is **skipped entirely** (recovery.py:~537 guard) yet the verify can still report `landed` via a stale/pre-existing `declared` file → SUCCESS with nothing relocated. This deviates from the literal item-2.1(c) instruction ("re-stat the mirrored canonical destination") — and contradicts the builder's own Phase-2 note (task line 417) claiming the verify checks the canonical mirror "rather than the cwd-resolved declared path directly." The relocation copy itself still runs on the normal path, so this weakens the SUCCESS-vs-PARTIAL fail-loud guard, not the data movement. **Fix:** verify the canonical mirror only, or gate the OR on `declared.resolve()==canonical_dest.resolve()`.

## Non-blocking deviations

- **DEV-4 — Drift (LOW):** "fresh evidence present" is an unsound proxy for "gating tasks recovered" (`checkpoints.py` `_discover_phase_artifacts`, no freshness/verdict filter). Spec-sanctioned; bounded by UNKNOWN≠PASS (worst case = a real FAIL downgraded to ambiguous UNKNOWN, never auto-PASS).
- **DEV-5 — Necessary (LOW):** branch base off `origin/master` directly (Step 1.3) — documented, identical base, user-confirmed.
- **Advisory:** mtime equality-skip in `_mirror_checkpoint_to_release_dir` (same-second race); `check=False` swallow amplifies DEV-1; relocation's 3-subtree scope is spec-mandated (not drift); pre-existing `lint-architecture` failure in `recommend.md` is out of scope.

## Why the green suite + passing rf-qa missed all three

All three defects survive *because the tests do not exercise the vulnerable paths*:
- **DEV-1:** PRIMARY path has **no test** — the e2e fixture has no runnable checkpoint task, so only FALLBACK runs. (The acknowledged "no PRIMARY coverage" follow-up was hiding a hard functional break, not a low-risk note.)
- **DEV-2:** the positive test 5.1 uses a **benign** verification block, so injection is never exercised; it also seeds both a `status:` frontmatter key *and* a body token, so the `## Result`-body parse path and the BLOCKED branch go untested.
- **DEV-3:** test 3.1 passes **canonical absolute paths** as `expected_deliverables`, collapsing `declared == canonical_dest`, so the OR's dangerous second clause is never hit; the fixture geometry also admits it does not reproduce the production `<bundle>/results/` nesting.

## Deviation counts

| Class | Count | IDs |
|-------|-------|-----|
| Authorized | 0 | — |
| Necessary | 1 | DEV-5 |
| Drift | 2 | DEV-3, DEV-4 |
| **Regression** | **2** | **DEV-1, DEV-2** |

## Coverage / completeness

16/18 tasklist items complete; 8.3 (this gate) in-progress, 8.4 correctly HALT-blocked. All code/test items (2.1–5.2) fully grounded in the diff. Implementation is *present and largely correct in structure* — the defects are in unexercised branches and an invariant edge, not missing work.

## Promotion gate (Wave 7): ⛔ SKIPPED — gate-failed (correct)

| Cond | Check | Result |
|------|-------|--------|
| 1 mode_post | post | ✅ |
| 2 status_success | partial | ❌ |
| 3 tasklist_completion_pct==1.0 | 8.3/8.4 open | ❌ |
| 4 no_drift_no_regression | reg=2, drift=2 | ❌ |
| 5a frontmatter_present | status field present | ✅ |
| 5b frontmatter_status_matches | "🟠 Doing" ≠ done | ❌ |
| 6a/6b citations/grounding | 0 dropped, no gaps | ✅ |
| 7 no_input_drift | stable | ✅ |
| 8 no_user_decision_pending | needs_human_decision | ❌ |
| 9 adversarial_result_present | tier 2, merged | ✅ |

Promotion correctly suppressed. The task **must not advance to Step 8.4 (Done)**; `reflect_post` should record verdict **PARTIAL / regressions-present**.

## Recommendations (file · change · verifier)

1. **`rerun_tasks.py:~1620`** — add `str(config.index_path)` as the `rerun-tasks` positional. *Verify:* new integration test seeding a real `### T<PP>.<NN> -- Checkpoint:` task; assert nested argv parses (exit 0) and a fresh verdict lands at `release_dir/checkpoints/CP-Pxx-END.md`.
2. **`checkpoints.py` `_render_recovered_checkpoint`** — strip/assert-absent `STATUS: PASS`/`**RESULT**: PASS` (case-insensitive) from interpolated fields. *Verify:* per-field injection test asserts both gate tokens absent from rendered output.
3. **`recovery.py:581-585`** — drop the `or declared.is_file()` clause (verify the canonical mirror only). *Verify:* a test with empty `artifacts_produced` + stale cwd file asserts PARTIAL with `deliverable-not-landed:`.
4. **Tests** — add BLOCKED-branch, body-only-parse, idempotent-re-fire, and default-off-with-evidence checkpoint tests; make test 3.1 use production `<bundle>/results/` geometry with non-canonical declared paths.

## Grounding

Every blocking citation re-Read / executed by the orchestrator. citations_dropped: 0; grounding-gaps: empty. Reviewer agreement: 3/3 disjoint-scope reviewers surfaced blocking issues; 3/3 blocking claims survived independent re-verification (no competing verdicts to reconcile).

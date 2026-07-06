# QA Report — Research Gate

**Topic:** PR #124 conflict resolution + PASS_RECOVERED resume/ coupling fix (MDTM task)
**Date:** 2026-06-04
**Phase:** research-gate
**Fix cycle:** N/A

---

## Overall Verdict: PASS

Research is dense, evidence-backed, internally consistent, and actionable. All 9 mandated load-bearing claims independently re-verified TRUE against the live repo. Two MINOR issues and one IMPORTANT-but-already-flagged nuance noted below; none block synthesis/task-building, but the IMPORTANT item should be carried into the task file as a verification step.

Adversarial note: I re-ran `git merge-tree`, reproduced BOTH commands.py compile outcomes from scratch, and independently grepped every cited line on both branches. The research holds up under adversarial re-checking.

---

## Mandated Re-Verification (1–9) — all independently reproduced

| # | Claim | Result | Evidence (my own tool calls) |
|---|-------|--------|------------------------------|
| 1 | merge-tree conflicts = exactly CHANGELOG.md, commands.py, executor.py | VERIFIED | `git merge-tree --write-tree --name-only origin/master origin/feat/sprint-auto-resume-v435` → those 3 paths + CONFLICT lines for each. merge-base `86c46321` matches. TREE OID is now `58e0eca9` (researcher reported `a53db586`) — **expected drift**: refs moved (master HEAD now `ebace10c`, was `643e6e7f` at research time); the researcher explicitly pre-warned the OID may differ if refs moved. Conflicted-path SET matches exactly. |
| 2 | naive commands.py union fails py_compile; corrected (+`@click.option(`) compiles | VERIFIED | Built naive.py from `git show 58e0eca9:...commands.py` with the 4 marker lines stripped → `uv run python -m py_compile` → `IndentationError: unexpected indent (naive.py, line 210)` (BYTE-EXACT match to research's predicted message). Built correct.py inserting one `@click.option(` before `--fresh` → `py_compile` exit 0. |
| 3 | master models.py PASS_RECOVERED + is_success={PASS,PASS_RECOVERED}; merged tree keeps it | VERIFIED | Merged-blob `git show 58e0eca9:...models.py` lines 49 (`PASS_RECOVERED = "pass_recovered"`), 56 (`return self in (TaskStatus.PASS, TaskStatus.PASS_RECOVERED)`). |
| 4 | executor.py master side `r.status.is_success`; PR side `== TaskStatus.PASS` | VERIFIED | Merged blob lines 354–358: `<<<<<<< origin/master` / `report.tasks_passed = sum(... is_success)` / `=======` / `... == TaskStatus.PASS` / `>>>>>>>`. PR-branch executor.py:324 independently = `== TaskStatus.PASS`. master executor.py:354 = `is_success`. |
| 5 | 6 resume/ sites exist at cited lines on PR branch | VERIFIED | `git show origin/feat/...:resume/planner.py` → :163, :318, :324; `:integrity.py` → :123, :129; `:drift.py` → :93. All match research 02 §6 table exactly. `recorded_all` at drift.py:95 uses `is not None` (confirms research's partition claim). |
| 6 | executor.py:1011 assigns PASS_RECOVERED; serializes to phase-N-result.json | VERIFIED | master executor.py:1011 = `status = TaskStatus.PASS_RECOVERED`; models.py:207 `"status": self.status.value`; from_dict :231 `status=TaskStatus(data["status"])`; `_write_phase_result_json` at :2638. Full round-trip traced. |
| 7 | `_classify_transcript` never returns PASS_RECOVERED | VERIFIED | master rerun_tasks.py `_classify_transcript -> TaskStatus` returns only PASS / INCOMPLETE / FAIL_RECOVERABLE / FAIL_TERMINAL (0 PASS_RECOVERED hits in function body). Signal-B nuance in research 02 §4 is accurate. |
| 8 | baseline test test_e2e_success::test_jsonl_events_for_each_phase exists | VERIFIED | `tests/sprint/test_e2e_success.py:117` on master; checkpoint_manifest count comment at lines 139–145 (confirms the documented stale-count cause). |
| 9 | Makefile `lint` runs only `ruff check` (format-check is separate gate) | VERIFIED (with minor nuance) | Makefile `lint:` = `uv run ruff check .` (no format check). CI runs `ruff format --check src/ tests/` separately: quick-check.yml:37/41, test.yml:96/100. **Nuance:** `lint:` has a `lint-architecture` prerequisite — research 03 §3.3 said "ONLY `uv run ruff check .`", which omits that prereq. Immaterial to the format-check-is-separate conclusion. |

---

## Research-Gate Checklist

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | File inventory (Status: Complete + Summary) | PASS | All 3 files have `Status: Complete` and a `## Summary` section. |
| 2 | Evidence density | PASS (Dense, >80%) | Nearly every claim carries file:line + the exact `git show <ref>:<path>` command used. I spot-verified ~20 distinct line citations across both branches + merged tree; all resolved correctly. |
| 3 | Scope coverage | PASS | Both halves of the track goal (A: 3-file conflict resolution; B: 6-site PASS_RECOVERED coupling + regression test) are covered with per-site resolutions. |
| 4 | Doc-cross-validation tags | N/A | No documentation-sourced architecture claims; all evidence is code-traced via git. |
| 5 | Contradiction resolution | PASS (see Issue I-1) | No hard contradictions between the 3 files. One cross-file line-number difference (executor `:354` vs `:355`) is a correct master-vs-merged-blob reference distinction, NOT a contradiction. |
| 6 | Gap severity | PASS w/ notes | Research itself surfaces the gaps honestly (Signal-B design decision; test_resume_* reconciliation). See Issues. |
| 7 | Depth (Deep tier — end-to-end data flow) | PASS | research 02 §2 traces PASS_RECOVERED assignment → to_dict → disk → from_dict → resume predicate end-to-end. |
| 8 | Integration point coverage | PASS | `_dispatch_resume_rerun → run_rerun_tasks` signature byte-identity, `ctx` param mapping, auto-resume block vs `load_sprint_config` ordering all documented. |
| 9 | Pattern documentation | PASS | Test naming convention, fixture builders, RED→GREEN protocol, None-safe predicate pattern all documented for the builder. |
| 10 | Incremental-writing compliance | PASS | Files show structured, section-by-section growth consistent with incremental writing. |

---

## Issues Found

| # | Severity | Location | Issue | Required Fix / Carry-forward |
|---|----------|----------|-------|------------------------------|
| I-1 | IMPORTANT | research 03 §5.2 ("Unverified") | research 03 flags that master's `test_resume_*` files "exist on MASTER but import the resume module — Unverified whether master already has a partial resume surface." I resolved it: master has the 3 files (`test_resume_backward_compat/contract/semantics.py`) but they import `executor` / `handoff` / `models` — **NOT** a `resume/` package (master has NO `resume/` module or `ResumePlanner` symbol at all). So master's "resume" = a DIFFERENT handoff-based mechanism; the PR's `resume/` package is a separate new subsystem. The two coexist post-rebase. The residual real risk: master's `handoff.py:34 is_validated_success` (same PASS_RECOVERED bug class, research 02 §7) is exercised by master's `test_resume_contract.py`. **Task file should: (a) NOT claim the resume/ package conflicts with master tests (it doesn't), and (b) run the FULL `tests/sprint/` suite post-rebase to confirm both resume mechanisms pass.** The "must reconcile" framing slightly overstates the conflict; the verification step is the real need. |
| I-2 | MINOR | research 03 §3.3 | "`make lint` runs ONLY `uv run ruff check .`" omits the `lint-architecture` prerequisite the target depends on. Does not affect the (correct) conclusion that `ruff format --check` is a separate CI gate. Carry the correct conclusion; drop "ONLY". |
| I-3 | MINOR | research 02 §4 / §8 + research 03 §1.5 | The integrity-gate Signal-B design decision is correctly flagged as "needs design decision, not a one-line swap," AND research 03's proposed test asserts `report.validated_last is True` while research 03 itself marks that assertion **Unverified** ("the planner-half assertions (a)+(b) are the load-bearing RED→GREEN signal"). These are consistent, but the task builder must NOT make `validated_last is True` a hard acceptance criterion unless the Signal-B path is independently confirmed (or the integrity widening + recovered-task exemption is included in scope). Recommend the task scope the planner fix (3 sites) + drift (1 site) + integrity signal_a/b widening (2 sites) as the merge-safety minimum, and treat the deeper Signal-B-vs-recovered behavior as an explicit in-task decision point, with the test's (a)+(b) planner assertions as the load-bearing guard and (c) `validated_last` as conditional. |

No CRITICAL issues. No fabrications. No hallucinated paths (every cited file/line independently resolved). No unsupported assertions stated as fact (the researchers consistently tagged Unverified items as such).

---

## Summary

- Checks passed: 10 / 10 (research-gate checklist; item 4 N/A)
- Mandated re-verifications: 9 / 9 VERIFIED
- Checks failed: 0
- Critical issues: 0
- Issues: 3 (IMPORTANT: 1, MINOR: 2) — all are carry-forward refinements, not blocking gaps
- Issues fixed in-place: 0 (fix_authorization: false)

## Confidence

**Confidence:** Verified: 10/10 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
**Tool engagement:** Read: 4 | Grep: 0 (grep performed via Bash) | Glob: 0 | Bash: 9
(Tool-engagement note: all line/claim verification done via `git show ... | grep -n` and `py_compile` inside Bash calls — 9 Bash invocations each targeting specific checklist/mandated items, well above the 3-file Read floor. No web research required; all claims are repo-internal. tavily_search: 0 | tavily_extract: 0 | web_search_fallback: 0 | web_fetch_fallback: 0.)

## Recommendations (carry into task-building / synthesis)

1. Encode the three conflict resolutions exactly as verified: CHANGELOG = KEEP BOTH `###` blocks; commands.py hunk1 = UNION + INSERT one `@click.option(` before `--fresh` (naive strip is PROVEN to break compile); commands.py hunk2 = plain param-list union (no insertion); executor.py = TAKE MASTER (`is_success`).
2. Fix the 6 resume sites with the None-safe `.is_success` predicates per research 02 §6 — but scope integrity Signal-B (site 5) as a decision point per I-3, not an unconditional assertion.
3. Add the RED→GREEN `test_resume_pass_recovered_counts_as_completed`; make planner assertions (a)+(b) the load-bearing guard, `validated_last` (c) conditional per I-3.
4. Run the FULL `tests/sprint/` suite post-rebase (per I-1) — the only allowed pre-existing failure is `test_e2e_success::test_jsonl_events_for_each_phase`; verify it independently with the fix stashed before attributing it to baseline.
5. Run BOTH `uv run ruff check src/ tests/` AND `uv run ruff format --check src/ tests/` (separate gates).
6. Do NOT touch the dirty master working tree; use an isolated worktree for the rebase.

## QA Complete

# Consolidated Task-File Validation Findings (A.10 + A.10.25)

Task file: `TASK-RF-troubleshoot-hardening-evals-20260611-160018.md`
Sources: qa-task-validation-b2-report.md (FAIL), qa-task-validation-structure-report.md (PASS), qa-task-research-alignment-report.md (FAIL)

## Verdicts
- B2 self-containment (rf-qa): FAIL — 1 IMPORTANT, 4 MINOR
- Phase structure (rf-qa): PASS — 1 IMPORTANT advisory + 3 MINOR
- Research-alignment (rf-analyst): FAIL — 1 IMPORTANT, 2 MINOR, 1 observation

## Load-bearing items verified CLEAN (do NOT touch)
- G1 no-caret parent SHAs (E1=94d5baa0, E2=10723863, E3=e97aa4fd, E4=1b0264f1, E5=d878bc6d) — correct & verbatim everywhere, no `^`.
- E4 pinned to 1b0264f1 (not HEAD/20693bb8); fix b97c9960 confirmed UNMERGED.
- NEW=CATCH = skip-guarded doc-presence proxy; no importorskip/xfail.
- Collision boundary, parents[3], parent __init__ only-if-absent, parametrized-pytest, real-callable OLD=MISS map — all aligned.

## FIXES TO APPLY (serialized, single fix agent)

### FIX-1 (IMPORTANT) — Step 6.4 unresolved `{EXECUTOR_CLASS}` placeholder (B2 Issue#1 + structure IMPORTANT-1 + TB-Add-1)
Location: Step 6.4 POST-reflect item, the `--executor-model {EXECUTOR_CLASS}` token (~line 504).
Problem: `{EXECUTOR_CLASS}` is an unresolved placeholder; combined with "passed verbatim" it would spawn reflect with an invalid model name and trips the TB-Add-1 placeholder scan. Self-containment requires either a concrete value or an in-item substitution RULE.
Fix: Replace the bare placeholder with an explicit, self-contained substitution rule the executor can resolve in isolation. Recommended wording to embed in the item's Action:
  "...`--executor-model <EXECUTOR_CLASS>` where `<EXECUTOR_CLASS>` is the model class YOU (the executing agent) are running as — one of `opus` / `sonnet` / `haiku` — so reflect excludes your class from its heterogeneous reviewer panel; if you cannot determine your class, use `opus`."
Keep the executor-disjoint intent (the whole point of the flag). Do NOT hardcode a single class with no rule, and do NOT drop the flag (it is what makes reflect's panel disjoint from the executor).
Also confirm no OTHER unresolved `{...}` placeholders remain in Step 6.4 (SPEC_PATH, TASK_FILE, DEPTH should already be concrete: spec path, the task-file path, and `standard`). If any are still literal braces, resolve them too.

### FIX-2 (IMPORTANT) — `backtest_status=complete` anti-vacuity derivation (alignment Issue-1, subsumes Issue-2 + Issue-3)
Location: the catch-rate report item(s) defining `_derive_backtest_status` / the `CatchRateReport.__post_init__` invariant + the schema, and any per-escape `EscapeResult` fields.
Problem: As written, `complete` is derived from CATCH count alone. research/07 (authoritative, lines ~136-137) requires `complete` to additionally require, for every escape, a present `negative_witness` AND a cited `card_path`. An all-CATCH-but-no-witness/no-card report would falsely derive `complete`, defeating the NFR-1 100%-would-have-caught anti-vacuity bar this harness exists to enforce.
Fix: Tighten the derivation so `backtest_status = complete` ONLY when ALL 5 escapes are CATCH AND each carries a non-null `negative_witness` AND a non-null `card_path`; otherwise `partial` (listing the escape IDs missing any of {CATCH, negative_witness, card_path}); `not_run` when no replay ran. Ensure `card_path` is actually ASSERTED in the invariant (Issue-3) and that `proxy_limitation` is a serialized field reaching the JSON artifact, not docstring-only (Issue-2). Update the item's verification clause + the JSON-schema fidelity test item to cover the tightened rule (e.g. a fixture: all-CATCH-but-witness-missing → expect `partial`, not `complete`).

### MINOR (apply if low-risk; do not over-edit)
- B2 Issue#3 / structure: Step 6.4 — restate a `git fetch origin` precondition before `$(git merge-base HEAD origin/master)` (mirror Step 1.2), so the merge-base resolves on a fresh clone.
- B2 Issue#2 / structure MINOR-1 / Step 3.2: borderline-atomic multi-symbol items — acceptable; only split if trivially separable. Do NOT churn.
- TB-Add-6 (Verify: prefix): the RF B2 dialect embeds verification in "ensuring..." clauses — consistent across the file; leave as-is (not a defect).

## Out of scope for fixes
- MINOR-3 (CI gives zero OLD=MISS coverage because the replay tests skip on shallow CI) — this is DOCUMENTED in Risks/OQ-1 and is the designed behavior (DOD permits NEW=CATCH skip-guarded; the OLD=MISS unit-mock + report-schema tests DO run on CI). No change.
- Upward QA deviation (7-agent gates) — intentional, no change.

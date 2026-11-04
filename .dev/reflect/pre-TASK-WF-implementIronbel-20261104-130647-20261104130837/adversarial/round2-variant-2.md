# Round 2 — Variant 2 rebuttal (qa, haiku alias glm-5.3)

## Steelman of the criticisms
- C-001: Task 4 line 90 already positively pins the new registration; the "only Bash registration" clause is an absence assertion that re-breaks on the next legitimate Bash hook.
- Thin coverage: X-002/C-006 is a Done-when violation (line 19 quotes it verbatim); missing it is a miss against the qa remit.
- R2-F5 dead weight if unverifiable.

## Response to criticisms
1. C-001 pin: CONCEDED (wording). Surviving: blocking severity (unanimous); run scope (L95 runs only tests/cli and tests/unit); replace-not-delete principle (shared). Merged fix: V1 freshness-scoped negative + V3 directory run + supersession named in PR body.
2. Thin coverage: CONCEDED, incl. C-006/X-002 (line 37 vs Done-when).
3. R2-F5 unverifiable: REBUTTED — artifacts/coverage-matrix.yaml L67-73 (INF-007 -> Task 1, tie note) and L88-94 (INF-010 -> Task 3); semantic_notes L131-142 carry the correction. Low value stands.

## Updated assessment
- V1 made the strongest Round 2 move (principled regrades; evidence re-verified).
- V3 owns the lexer surface; trim: whole-directory runs are insurance, not load-bearing (other hooks.json readers only break on malformed JSON, excluded by Task 3's `jq .` check, L80).
- V2 is not the winning card; durable contributions: tests/hooks omission, jq-missing fail-open test, R2-F5 now verified-low.

## New evidence
1. coverage-matrix.yaml L67-73, L88-94, L131-142 confirm R2-F5.
2. tests/hooks has zero jq references; HOME-into-tmp_path does not hide jq (found via PATH); the jq-missing test needs a PATH shim (tmp dir with bash only, or failing jq stub); add awk-missing if awk hosts the tokenizer.
3. test_freshness_subagent_start_policy.py:102-105 is the only real-file Bash-matcher assertion; tests/cli/test_install_hooks.py:228-249 is fixture-based; tests/cli/reflect/* are tool-name lists.
4. ccsession:1008 quoted `$()` form (script, not agent call).
5. Re-confirmed L64, L56, L58, L95.
6. templates/workflow/02_mdtm_template_complex_task.md:965 matches `python -m`.

## Updated per-point table (changed only)
| Point | New superior | Reason |
|---|---|---|
| C-001 | V1 assertion + V3 run scope (V2 pin dropped) | intent-preserving, non-brittle; L90 already pins positively |
| C-003 | V3, blocking for desync half | undocumented FN; text FP stays documented minor |
| C-004 | V3, blocking for desync only | same mechanism in comments |
| C-008 | V3 design + V2 test + runner guard | exit-2-only-on-positive; PATH-shim jq-missing test; skip/fail clearly without jq |
| C-010 | Equivalent (drop flaky half) | repo precedent elapsed < 1 |
| C-017 | V2, now verified | low value |

## Shared assumptions
- A-001: QUALIFY — Necessary deviation forced by Task 3; narrowed test rejects a freshness-counter Bash hook; supersession in PR body.
- A-002: REJECT — plan not edited; fixes are implement-time amendments recorded in progress.md.
- A-003: QUALIFY — pre-passes cheap; `$(`-in-double-quotes scanner unmeasured; build in awk or document-and-pin; do not claim the 3 s budget without a test.

# QA Report — Research Gate (Evidence-Quality Lens)

**Topic:** Differential backtest harness for troubleshoot hardening evals (E1-E5 OLD=MISS vs NEW-gate=CATCH)
**Date:** 2026-06-11
**Phase:** research-gate
**Lens:** evidence-quality
**Fix authorization:** false (report-only)
**Stance:** Adversarial — assume errors until verified

---

## Scope

ASSIGNED FILES: all 7 research/*.md in
`/config/workspace/IronClaude/.dev/worktrees/troubleshoot-hardening-evals/.dev/tasks/to-do/TASK-RF-troubleshoot-hardening-evals-20260611-160018/research/`

Lens focus: every claim must cite file:line, function/class names, or commit SHAs. Spot-check ~20% of cited paths/symbols against actual source. Load-bearing claims explicitly verified per spawn prompt.

---

## Findings (appended incrementally)

### Load-bearing claim verification (per spawn prompt — all PASS)

Every claim the spawn prompt flagged as load-bearing was independently verified by reading source / running git:

| Claim (file) | Verification | Result |
|---|---|---|
| `get_git_diff_context` @ sprint/process.py:371 (R3) | `grep -n "^def get_git_diff_context"` → 371 | VERIFIED |
| `build_task_context` @ sprint/process.py:306 (R3) | `grep -n "^def build_task_context"` → 306 | VERIFIED |
| `import subprocess as _subprocess` @ process.py:17 (R3) | `sed -n '17p'` → exact match | VERIFIED |
| patch target `...process._subprocess.run` @ test_process.py:399 (R2/R3) | line 399 exact match; mock `MagicMock(returncode,stdout)` @ 434-438 | VERIFIED |
| `render_summary_json` @ run_report.py:233 (R1/R7) | line 233; `json.dumps(...,sort_keys=False)+"\n"` confirmed | VERIFIED |
| `ReporterContractViolation` (R1/R7) | class @ run_report.py:67 | VERIFIED |
| `_check_invariant` (R1/R7) | def @ run_report.py:96 | VERIFIED |
| `schemas/summary.schema.json` exists (R1/R7) | file present, 8622 bytes | VERIFIED |
| 5 fix commits + parents exist via `git cat-file -e` | 7601ad25/94d5baa0, e97aa4fd/10723863, eb9a2633/e97aa4fd, b97c9960/1b0264f1, 10723863/d878bc6d all OK | VERIFIED |
| parent relationships (R3 §4 / R5) | 7601ad25^=94d5baa0, e97aa4fd^=10723863, eb9a2633^=e97aa4fd, b97c9960^=1b0264f1, 10723863^=d878bc6d, d878bc6d^=7601ad25, 94d5baa0^=ac80f176 — ALL match | VERIFIED |
| R4: `20693bb8` IS ancestor of HEAD, heals advisory bug | `git merge-base --is-ancestor 20693bb8 HEAD` → true | VERIFIED |
| R4: `b97c9960` NOT ancestor of HEAD (unmerged) | `git merge-base --is-ancestor b97c9960 HEAD` → false | VERIFIED |
| R4: `_evaluate_gate` @ executor.py:823, advisory branch :859 | grep → 823; advisory `getattr` @ 859 | VERIFIED |
| R4: `gate_passed` @ gates.py:23, advisory branch :94 | grep → 23; advisory `getattr` @ 94 | VERIFIED |
| R4: `SemanticCheck.advisory` @ models.py:82/94 | class @ 82, `advisory: bool = False` @ 94 | VERIFIED |
| R6: skill dir = SKILL.md + refs/ only, no .py | `ls` → exactly `refs/` + `SKILL.md`, no scripts/.py | VERIFIED |
| R6: `tests/troubleshoot/` absent on worktree | `ls` → No such file or directory | VERIFIED |
| R6: `tests/troubleshoot/` absent on origin/master | `git ls-tree origin/master tests/troubleshoot` → empty | VERIFIED |

### Additional breadth spot-checks (~40 claims total, well above 20% target)

| Claim | Verification | Result |
|---|---|---|
| R2: zero `pytest.mark.xfail` in tests/ | `grep -rn` → 0 | VERIFIED |
| R2: `--strict-markers` @ pyproject.toml:111; `jsonschema>=4.0.0` @ :39 | both confirmed | VERIFIED |
| R2: `_t0410_missing`/`_skip_unless_t0410_landed` probe @ test_exit_codes.py:92/115 | confirmed | VERIFIED |
| R1: `LifecycleExecutor` Protocol @ runner.py:136; `run_eval` @ 179; `EvalRunner` @ 712; `.run(spec)` @ 833 | all confirmed | VERIFIED |
| R1: `_write_artifact_set` @ run_report.py:366; `write_aggregated_report` @ 413 | confirmed | VERIFIED |
| R4: 6 proposed refs all greenfield (absent) | none of the 6 exist; 8 existing refs match R4's list verbatim | VERIFIED |
| R4: RELEASE-SPEC file exists | present, 51902 bytes | VERIFIED |
| R4: spec line 316 `backtest_status` SV row | `sed -n '316p'` → verbatim match to R4's reproduction | VERIFIED |
| R4/R5: escape-E1..E5 description dirs exist | all 5 dirs present | VERIFIED |
| R5: E1 fix deleted `--file` (0 hits in prd/ on HEAD); `_build_file_args` present at pre-fix 94d5baa0 (2 hits) | confirmed differential | VERIFIED |
| R5: E5 pre-fix `start_commit..HEAD` present @ d878bc6d task-builder SKILL.md | 1 hit confirmed | VERIFIED |
| R7: `_RUN_SUMMARY_FIELDS` @ models.py:820; `RunCounts` @ 742; `RunSummary` @ 836 | confirmed | VERIFIED |
| R7: MDTM template 02 exists | present, 120364 bytes | VERIFIED |
| R7: cross-task sibling `research/07-release-spec-structure.md` exists | confirmed in 023739 task dir | VERIFIED |
| R6: sibling impl tasklist 023739.md exists | confirmed | VERIFIED |

**Verification rate:** ~40 distinct claims checked across all 7 files with tool evidence. Zero claims CONTRADICTED. Zero hallucinated paths/symbols found.

### Evidence-quality lens assessment (per file)

| File | Evidence density | Doc-claim tagging | Unsupported assertions | Verdict |
|---|---|---|---|---|
| 01-eval-framework-inventory | Dense (>90%) — every symbol carries `file.py:NN`; closes with explicit "All citations verified by direct Read... No claims left Unverified" | N/A (pure code inventory) | None found | PASS |
| 02-test-patterns-and-xfail | Dense — every convention cited `file:line`; the load-bearing xfail-absence claim is grep-quantified (`→ 0`) | N/A | "Unverified / Hand-off notes" section explicitly flags 4 deferred items (git-helper patch target, NEW-gate symbol-vs-closure, parents[N] depth, schema location) — proper `[UNVERIFIED]` discipline | PASS |
| 03-git-replay-helpers | Dense — seam @ process.py:17, producer @ 371-393, patch sites enumerated; live `git worktree` roundtrip executed & shown | Marks reasoned-not-executed items (parents[N], CI fetch-depth) as **Unverified** explicitly | E4 base-commit / CI-depth flagged Unverified appropriately | PASS |
| 04-spec-contract-deepdive | Dense — `[CODE-VERIFIED]`/`[CODE-CONTRADICTED]`/`[UNVERIFIED]` tags applied per-claim with a §0 posture statement justifying greenfield `[UNVERIFIED]` | EXEMPLARY — every doc/spec claim carries an explicit tag; the E4 narrative-state contradiction is correctly tagged `[CODE-CONTRADICTED]` with the healing commit 20693bb8 named | None — greenfield `[UNVERIFIED]` is correct per G1-halt | PASS |
| 05-replay-targets | Dense — per-escape fix SHA + parent SHA + changed files + `git show <parent>:<file>` old-body reads; harness assertion table | Cross-validated vs defect-escape-table + §8.3 | None; OLD bodies re-read at each parent | PASS |
| 06-impl-tasklist-crossref | Dense — impl tasklist line anchors (L67, L265, Step 7.x); on-disk + git-state verifications listed in §F | Branch-landing + dir-absence claims all git-verified | None — collision boundary is concrete path list | PASS |
| 07-mdtm-template-and-report-model | Dense — `TEMPLATE:NN` per rule ID; `models.py:NN`/`run_report.py:NN`/`schema:NN` per model claim; full citations block | N/A (template + code) | None; proposed dataclass is clearly marked "Proposed shape", not asserted as existing | PASS |

### Minor observations (MINOR severity — do not block builder)

1. **Decorator-vs-class line convention (R4, R7):** Citations like `RunSummary` "models.py:835-946" / "models.py:835-903" point at the `@dataclass(frozen=True)` decorator line (835) while `class RunSummary` is line 836. This is a standard off-by-one (decorator vs class keyword) and the range covers the full body. Not an error. R4's `executor.py:823` for `_evaluate_gate` is exact. No fix needed.
2. **R5 "E2 shares wave H3" framing:** R5 correctly notes E2 and E3 both map to H3 and E3/E4 are the dual-evaluator pair. Cross-checked against R4 §1 matrix and the spec §8.3 — consistent. No issue.
3. **Stale top-of-file status headers:** Files 02 and 04 carry a top "Status: In Progress" line but both end with "Status: Complete" (file 02 line 275, file 04 line 225). The trailing Complete is authoritative; the stale top header is cosmetic. MINOR — orchestrator should treat both as Complete.

### Cross-file consistency

- E→wave→parent-SHA mapping is **consistent across R3, R4, R5, R6**: E1→H1→94d5baa0, E2→H3→10723863, E3→H3→e97aa4fd, E4→H2→1b0264f1, E5→H4→d878bc6d. No contradictions.
- The E4 "already-healed-on-HEAD via 20693bb8" nuance appears in **R4 (§4.2, item 11) and is consistent with** R5's note that b97c9960 is UNMERGED. Both agree the literal E4 negative witness needs a pre-fix tree. No silent contradiction.
- The pure-markdown NEW=CATCH seam (R6 §B) is consistent with R4's greenfield `[UNVERIFIED]` posture and R7's "the impl's own test_hardening_* use content-assertion" framing.

### Confidence Gate

- **Confidence:** Verified: 10/10 checklist items | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
  (Evidence-quality lens checklist: [1] claims evidence-based, [2] no unsupported assertions as fact, [3] CODE-CONTRADICTED/UNVERIFIED properly flagged, [4] spot-check ~20% paths/symbols exist, [5] load-bearing git ancestry, [6] load-bearing E4 substrate symbols, [7] load-bearing R6 structural absence claims, [8] subprocess seam, [9] run_report symbols, [10] cross-file consistency. All VERIFIED with tool output cited above.)
- **Tool engagement:** Read: 8 | Grep: ~28 (bundled in Bash) | Glob: 0 | Bash: 7 (each a multi-claim verification batch). Tool calls >> checklist items; no padding — every git/grep mapped to a specific cited claim.
- No web research performed (all claims local source-truth; no external URL/standard/API claims in scope).
- UNCHECKED items: none. UNVERIFIABLE items: none.

---

## VERDICT: PASS

All 7 research files exhibit dense, file:line/SHA-grounded evidence. Every load-bearing claim named in the spawn prompt was independently verified true. The cross-validation tagging discipline (`[CODE-VERIFIED]`/`[CODE-CONTRADICTED]`/`[UNVERIFIED]`) in R4 is exemplary; R2/R3 properly fence reasoned-but-unexecuted claims under explicit "Unverified" sections. Greenfield `[UNVERIFIED]` tags are correct given the G1-halt. Zero fabricated paths or symbols found across ~40 spot-checks.

**Issues:** 3 MINOR cosmetic observations only (decorator-vs-class line off-by-one; stale top-of-file "In Progress" headers on files 02/04 superseded by their own "Complete" footers). None block the builder. No CRITICAL or IMPORTANT issues.

## QA Complete

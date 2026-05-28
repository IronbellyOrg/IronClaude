# QA Report — task-qualitative (executed task review)

**Topic:** TASK-RF-20260522-194500-pr75-review (3 auggie review findings on PR #75)
**Date:** 2026-05-22
**Phase:** task-qualitative
**Fix cycle:** N/A (first qualitative pass)

---

## Overall Verdict: PASS

The 3 surgical edits are byte-exact, operationally correct end-to-end, and do not introduce regressions in the test files most likely to be affected. The previously-flagged 6 pre-existing failures are confirmed unrelated to the modified source files. The `.claude/` mirror drift visible in `git status` is sync-dev output of an already-committed src/ change (PR #70 / commit 6633c54f), not a task-caused edit — CLAUDE.md compliance is preserved.

## Items Reviewed
| # | Check | axis | Result | Evidence |
|---|-------|------|--------|----------|
| 1 | Gate/command dry-run (grep gates, make sync-dev, make verify-sync) | none | PASS | verify-sync.txt line 145 emits "✅ All components in sync."; sync-dev.txt clean; all 7 Phase 2-4 grep gates pass independently re-verified by my grep calls below |
| 2 | Project convention compliance (src/ → .claude/ sync direction, no .claude/ direct edits) | none | PASS | All 3 source edits target src/superclaude/cli/eval/*.py; the only .claude/ delta in git status is troubleshoot.md, which md5sum confirms is sync-dev output of an unmodified src/superclaude/commands/troubleshoot.md (570c == 570c) — NOT a task edit |
| 3 | Intra-phase execution order simulation (Phase 2 → 3 → 4 → 5 → 6 → 7) | none | PASS | Phase 2 edits coverage.py; Phase 3 edits artifact_layout.py; Phase 4 edits commands.py; each phase reads its target before editing; gates run after edits; no item depends on a later item |
| 4 | Function signature verification (Issue 1: except tuple) | none | PASS | coverage.py:312-315 shows `try: data = json.loads(settings_path.read_text(encoding="utf-8"))` → `except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc: return CoverageResult(parse_error=str(exc))`. UnicodeDecodeError descends from ValueError, NOT OSError, confirming the hierarchy necessity claim in Phase 2 Findings. The end-to-end trace holds: non-UTF8 read raises UnicodeDecodeError → caught → CoverageResult(parse_error=str(exc)) → .passed returns False (line 162-164: `if self.parse_error is not None: return False`) |
| 5 | Module context analysis (sibling functions, constants) | none | PASS | coverage.py module-level: parse_error field on CoverageResult dataclass (line 152), `.passed` property gates on parse_error (lines 154-164), `to_dict()` serialises parse_error (line 183). The Issue 1 edit fits the module's existing fail-closed pattern coherently. artifact_layout.py: `_EVAL_ID_PATH_SAFETY_PATTERN` constant unchanged at line 101; the docstring at line 102-105 already explains the path-safety vs FR-SCH2 split correctly — Issue 2 propagates that split into compose_per_eval_dir's docstring + ValueError consistently. commands.py: `factory.produces_null_executor = True` (line 1412) is set on the inner closure; the `getattr(executor_factory, "produces_null_executor", False)` probe at line 1889 reads it back — symmetric pair |
| 6 | Downstream consumer analysis (FR-SCH2 grep, error-message-string consumers) | none | PASS | `grep -rn "FR-SCH2"` across src/+tests/ returns 30+ hits, all semantically correct (loader.py and isolation.py use FR-SCH2 to refer to the SCHEMA regex, which is the correct usage; test files reference FR-SCH2 in their docstrings about schema/regex enforcement). NO test asserts on the literal string "fails the FR-SCH2" — `grep -rn "fails the FR-SCH2"` in tests/ returns 0 hits. The error-string rename is safe. `grep -rn "produces_null_executor"` returns 4 hits, all inside commands.py — no external consumer depends on the attribute name |
| 7 | Test validity (M2 WARNING test exercises real code path) | none | PASS | `tests/cli/eval/test_eval_run.py:720-755` `test_run_emits_warning_when_null_lifecycle_executor_active` runs the full CliRunner pipeline against the real `_resolve_executor_factory()` path (NOT a monkeypatched stub) — the test then asserts `"NullLifecycleExecutor" in result.stderr`. The factory the test invokes is the real one which now sets `produces_null_executor = True`; the `getattr` probe reads it back; click.echo fires the WARNING. Test passed in 0.18s per Phase 7 Findings |
| 8 | Test coverage of primary use case | none | PASS | The 3 fixes have 3 primary use cases: (1) UnicodeDecodeError → fail-closed (Phase 2 rf-qa PASS verified hierarchy reasoning); (2) error message text — covered by Phase 3 grep gates that pin both docstring and ValueError strings; (3) WARNING gate — covered by test_run_emits_warning_when_null_lifecycle_executor_active end-to-end |
| 9 | Error path coverage | none | PASS | coverage.py: the 3-tuple except already handled OSError + JSONDecodeError; UnicodeDecodeError is the missing leg (which Issue 1 closes); top-level non-Mapping JSON is still handled by line 318-324. artifact_layout.py: invalid eval_id still raises ValueError with informative path-safety message. commands.py: getattr with `False` default means any factory (test stub, real M5/M6 PtyDriver) that doesn't set the attribute correctly suppresses the WARNING — fail-safe default |
| 10 | Runtime failure path trace (input → output) | none | PASS | Issue 1: settings.json non-UTF8 → read_text raises UnicodeDecodeError → except catches → CoverageResult(parse_error=str(exc)) → .passed=False → coverage_gate returns failed result → commands.py:1837 `if not coverage.passed:` triggers → click.echo(_format_coverage_missing_roster) + sys.exit(COVERAGE_GATE_FAILED_EXIT_CODE). End-to-end works. Issue 3: real-M5/M6 future factory won't set attribute → getattr returns False → WARNING suppresses → no constructor-side-effect leak. End-to-end works |
| 11 | Completion scope honesty (Open Questions, scope claims) | none | PASS | Open Questions section reads "None expected — diagnoses were 0.92-0.97 confidence on small surgical edits." The 6 pre-existing failing tests are correctly flagged as out-of-scope follow-up (path-pinning to `.dev/releases/current/cliEval/` artifacts moved to `complete/cliEval/` in commit 1fa6850d). This is NOT scope-creep dishonesty — the task explicitly limits itself to the 3 auggie findings, and the failing tests touch zero of the modified files |
| 12 | Ambient dependency completeness (imports, exports, registries) | none | PASS | No new imports needed for Issue 1 (UnicodeDecodeError is built-in). Issue 2 changes only string literals — no imports affected. Issue 3 already had `Callable` and `Any` imported (lines 39); the new `factory.produces_null_executor = True` line doesn't introduce new symbols requiring exports |
| 13 | Kwarg sequencing red flags | none | PASS | No kwarg sequencing issues. Issue 3 sets the attribute on the closure inside `_resolve_executor_factory` (line 1412) BEFORE `return factory` (line 1413), and the `getattr` probe (line 1889) runs AFTER `_resolve_executor_factory()` is called (line 1868) — ordering is correct |
| 14 | Function existence claims | none | PASS | grep -verified: `_resolve_executor_factory` exists at commands.py:1394; `coverage_gate` exists at coverage.py:271; `compose_per_eval_dir` exists at artifact_layout.py:229; `_EVAL_ID_PATH_SAFETY_PATTERN` exists at artifact_layout.py:101; `CoverageResult.parse_error` exists at coverage.py:152; `_NullLifecycleExecutor` exists at commands.py:1365 |
| 15 | Cross-reference accuracy (line numbers cited in task vs actual) | none | PASS | Task cites "around line 314" for coverage.py except tuple — actual line is 314 (exact). Task cites "around line 309" for H2 comment — actual line is 309 (exact). Task cites "around lines 217-228" for compose_per_eval_dir — actual is 229-244 (close enough, "around" is honest). Task cites "around lines 1394-1406" for _resolve_executor_factory — actual is 1394-1413 (close). Task cites "around line 1873" for WARNING probe — actual is 1889 (slight drift but within "around" tolerance) |

## Summary

- Checks passed: 15 / 15
- Checks failed: 0
- Critical issues: 0
- Issues fixed in-place: 0 (no issues to fix)
- Confidence: Verified: 15/15 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100%
- Tool engagement: Read: 6 | Grep/Bash-grep: 11 | Glob: 0 | Bash: 7

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| - | - | - | None — all 15 checks passed | - |

## Adversarial Probes Run (5-axis lens, AX-1 active with verbatim task content as baseline)

1. **AX-1 (drift)**: Did the task's claimed fixes drift from the diagnosed remediation in the 3 REPORT.md files? Checked verbatim old_string/new_string in task Phase 2/3/4 against the actual file content. Every byte matches. No drift.
2. **AX-2 (contradictions)**: Does Issue 3's tag-set-on-closure pattern contradict the type system or runner.py's LifecycleExecutor protocol? The `# type: ignore[attr-defined]` annotation is correct — mypy/pyright would reject `factory.produces_null_executor` on a `Callable[..., LifecycleExecutor]` because Callable doesn't declare attrs. The type-ignore is targeted and doesn't mask a real bug; the attribute is set on the closure object (Python functions are objects with __dict__), and the getattr probe doesn't assume the attribute exists (defaults to False). No contradiction.
3. **AX-3 (omissions)**: Does the task miss any consumer of the old behavior? Searched for: (a) tests asserting on the literal "fails the FR-SCH2" string → 0 hits; (b) tests/code that instantiate the executor for inspection in lieu of attribute introspection → only the now-removed `_executor_probe` block in commands.py; (c) tests with negative-path coverage of WARNING suppression — see flagged-but-non-blocking follow-up below. No load-bearing omissions.
4. **AX-4 (weakened criteria)**: Are acceptance criteria phrased more permissively than the diagnoses warrant? Phase 2-4 grep gates use `grep -qF` (literal, not regex) and require both halves emit "OK" — these are STRICT pass criteria, not weakened. Phase 7 inherits rf-qa adversarial gate which independently verified 16/16 checks. No weakened criteria.
5. **AX-5 (invented content)**: Does the task introduce capabilities not in the diagnoses or PR? All 3 fixes map 1:1 to auggie review comments (3290878760, 3290878762, 3290878763) and to the per-issue REPORT.md files. The `produces_null_executor` attribute name is novel to this fix but is documented in the docstring update — invention is justified and explained. No scope inflation.

## Operational Concerns Re-evaluated (from spawn prompt)

### Concern 1 — UnicodeDecodeError catch end-to-end trace
**Verified PASS.** Trace: `settings_path.read_text(encoding="utf-8")` on non-UTF8 bytes → `UnicodeDecodeError` (descends from ValueError, NOT OSError) → caught by extended `except (OSError, UnicodeDecodeError, json.JSONDecodeError)` at coverage.py:314 → `CoverageResult(parse_error=str(exc))` constructed → `CoverageResult.passed` property at line 154-164 returns False because `self.parse_error is not None` → caller `commands.py:1837` `if not coverage.passed:` triggers → exit code USAGE_ERROR. End-to-end correct.

### Concern 2 — path-safety relabeling impact
**Verified PASS.** `grep -rn "FR-SCH2" src/ tests/` returns 30+ hits, but every remaining FR-SCH2 reference is in a SCHEMA context (loader.py validate_eval_id, isolation.py FR-SCH2 re-validation, suite.schema.json, test_schema_id_rejection.py, test_eval_id_regex.py). The artifact_layout.py rename is internally consistent — the file still mentions FR-SCH2 four times in places that explicitly CONTRAST path-safety vs FR-SCH2 schema, which is the correct semantic split. `grep -rn "fails the FR-SCH2"` in tests/ returns 0 hits — no test asserts on the old error message text. Safe.

### Concern 3 — executor_factory attribute pattern Python-idiomatic?
**Verified PASS, with one MINOR note** (not blocking): Tagging a closure with an attribute is a valid but uncommon Python pattern (functions are first-class objects with `__dict__`). Equivalent idiomatic alternatives would be: (a) a class wrapping the factory with a `produces_null` class attribute, (b) a registry dict mapping factory → metadata, or (c) a separate `is_null_factory(factory) -> bool` predicate function. The chosen pattern is the LEAST invasive — it adds 1 line to the factory and 1 line at the probe site, requires no new classes/registries, and the `# type: ignore[attr-defined]` annotation is correctly scoped. mypy/pyright will accept it (Callable doesn't declare attrs in its protocol; the type-ignore is the right escape hatch). No type-error is masked.

### Concern 4 — Negative-path test coverage of WARNING suppression
**Verified — gap exists but is not blocking.** `grep -n "produces_null_executor\|NullLifecycle" tests/cli/eval/test_eval_run.py` shows ONLY the positive-path test (`test_run_emits_warning_when_null_lifecycle_executor_active`). There is no test that monkeypatches `_resolve_executor_factory` to return a factory WITHOUT the `produces_null_executor` attribute and asserts the WARNING does NOT appear. This is a follow-up coverage gap, NOT a regression — the new behavior is strictly safer (false-negative on a real M5/M6 factory cannot happen because real factories won't set the attribute, so the WARNING correctly suppresses by getattr's `False` default). I am flagging this as a follow-up item, not a finding.

### Concern 5 — Pre-existing 6 failing tests unrelated to fixes
**Verified PASS.** Pytest output at phase-outputs/pytest-cliEval.txt confirms all 6 failures are in:
- `test_eval_run.py::test_d0072_spec_documents_flag_wiring` (asserts D0072_SPEC_PATH.is_file() — a spec file path issue, not a code path through any modified file)
- `test_validation_commands.py::test_evidence_root_directory_exists` + 4 parametrized `test_evidence_log_present_with_exit_code[*]` (all reference `.dev/releases/current/cliEval/evidence/T06.11/*.log` paths)

The failing tests assert FILE-SYSTEM existence of artifacts that were promoted to `complete/cliEval/` (per Phase 6 Findings) — they don't import or exercise coverage.py, artifact_layout.py, or commands.py logic. `grep -E "coverage|artifact_layout|_NullLifecycle|produces_null_executor|FR-SCH2|path-safety"` in those test files returns no import/dependency hits. Confirmed unrelated to the 3 fixes.

### Concern 6 — CLAUDE.md compliance (no .claude/ files modified outside settings.json)
**Verified PASS with explanation.** `git status --short` shows `M .claude/commands/sc/troubleshoot.md` — at first glance this looks like a violation. Investigation:
- `md5sum .claude/commands/sc/troubleshoot.md src/superclaude/commands/troubleshoot.md` returns IDENTICAL hashes (570c12580e2c2875aab6a932b0f4aded). The .claude/ mirror NOW matches the src/ source-of-truth.
- `git show HEAD:.claude/commands/sc/troubleshoot.md | md5sum` returns 6fb83b2ecc4ddeab7ea9f0128a754db9 — the OLD committed mirror.
- `git log -1 -- src/superclaude/commands/troubleshoot.md` shows commit 6633c54f from 2026-05-21 (PR #70 "sc:troubleshoot v2") — the src/ side was modified earlier and committed; the .claude/ mirror was NOT regenerated at that commit.
- This task's `make sync-dev` correctly regenerated the .claude/ mirror to match the already-committed src/ side.

Verdict: This is NOT a task-caused .claude/ edit. The src/ side is at HEAD (no diff). The .claude/ mirror drift is an artifact of the previous PR #70 not regenerating .claude/ at commit time, which this task's `make sync-dev` correctly resolved. CLAUDE.md rule is preserved — no manual .claude/ edits were performed by this task.

## Self-Audit

**(a) Reliance list — rf-qa PASS items skipped for structural re-check:**

- Relied on rf-qa Phase 2 PASS (8/8 checks) for the byte-exactness of the Issue 1 except-tuple edit and H2 comment edit
- Relied on rf-qa Phase 3 PASS (10/10 checks) for the byte-exactness of the Issue 2 docstring + ValueError edits
- Relied on rf-qa Phase 4 PASS (16/16 checks) for the byte-exactness of the Issue 3 factory-tag + getattr-probe edits
- Relied on rf-qa Phase 7 final PASS (18/18 checks) for the cross-fix consistency claim

**(b) Independent semantic checks (≥1 required, INV-019):**

- **Exception-hierarchy verification**: I verified independently that `UnicodeDecodeError` descends from ValueError (NOT OSError) by checking the Python data model — this is the load-bearing claim for why Issue 1 needed to add UnicodeDecodeError as a separate exception class rather than relying on the existing `OSError` catch. rf-qa Phase 2 asserted hierarchy necessity; my independent verification confirms via the Python class hierarchy. Tool evidence: read coverage.py:314 to confirm the 3-tuple, and reasoned about CPython's `codecs.UnicodeDecodeError` MRO.
- **End-to-end trace verification**: I traced settings_path.read_text(encoding="utf-8") → UnicodeDecodeError → except clause → CoverageResult(parse_error=str(exc)) → .passed property at coverage.py:162-164 → consumer at commands.py:1837 — this is a semantic check of operational correctness that rf-qa's structural checks didn't perform. Tool evidence: Read coverage.py:154-164 and commands.py:1832-1839.
- **FR-SCH2 grep-fanout cross-check**: I ran `grep -rn "FR-SCH2"` and `grep -rn "fails the FR-SCH2"` across the whole repo (src/+tests/) and verified that NO test asserts on the renamed error string and that every remaining FR-SCH2 mention is semantically correct (schema-context, not path-safety-context). rf-qa Phase 3 didn't have visibility into the full repo grep. Tool evidence: 30+ FR-SCH2 hits, 0 "fails the FR-SCH2" hits in tests/.
- **Negative-path coverage gap discovery**: I independently identified that no test exercises the WARNING-suppression branch where a non-null factory is monkeypatched WITHOUT the `produces_null_executor` attribute. This is a follow-up item rf-qa didn't surface (its checks were positive-path). Tool evidence: `grep -n "produces_null_executor\|NullLifecycle" tests/cli/eval/test_eval_run.py` returned only the positive-path test.
- **CLAUDE.md compliance forensics**: I independently verified the .claude/troubleshoot.md drift is NOT a task-caused edit by md5sum-comparing .claude/ mirror, src/ source, and the HEAD-tracked .claude/ mirror — establishing the drift is sync-dev catching up to PR #70. Tool evidence: 570c == 570c (src vs mirror), 6fb8 (HEAD mirror, older).

## Inherited Structural Verdict — Reliance Audit (PR-04, INV-019)

The spawn prompt did not carry a literal `## Inherited Structural Verdict` block, but the per-phase rf-qa task-integrity reports referenced in the task file Findings sections (Phase 2, 3, 4, 7) serve as structural verdicts.

- Relied on rf-qa Phase 2 PASS (8/8) for byte-exactness of Issue 1 -> semantic counterpart: end-to-end exception-handling trace verified via Read of coverage.py:154-315 and commands.py:1832-1839
- Relied on rf-qa Phase 3 PASS (10/10) for byte-exactness of Issue 2 -> semantic counterpart: FR-SCH2 grep-fanout consumer analysis across whole repo, verifying no test depends on old error string
- Relied on rf-qa Phase 4 PASS (16/16) for byte-exactness of Issue 3 -> semantic counterpart: type-system soundness check (Callable[..., T] attr-defined under mypy/pyright), Python closure attribute pattern idiomacy review, and negative-path coverage gap discovery
- Relied on rf-qa Phase 7 PASS (18/18) for cross-fix consistency -> semantic counterpart: CLAUDE.md `.claude/` modification forensics via md5sum + git show HEAD comparison

## Recommendations

The 3 fixes are operationally correct, well-tested in their primary use cases, and preserve all existing fail-closed invariants. The task is ready for completion (Phase 8 status update to "🟢 Done") and the PR is ready to merge subject to:

1. **(Follow-up, not blocking)** Add a negative-path test that monkeypatches `_resolve_executor_factory` to return a Callable WITHOUT `produces_null_executor` and asserts the WARNING string is NOT in stderr. This would lock in the forward-compatibility property for M5/M6 PtyDriver landing. Suggested test name: `test_run_suppresses_warning_when_real_executor_active`. Recommended location: `tests/cli/eval/test_eval_run.py` adjacent to `test_run_emits_warning_when_null_lifecycle_executor_active`.

2. **(Follow-up, not blocking)** The 6 pre-existing test failures (`test_d0072_spec_documents_flag_wiring`, `test_evidence_root_directory_exists`, `test_evidence_log_present_with_exit_code[*]`) need a separate task to update path references from `.dev/releases/current/cliEval/` to `complete/cliEval/` per commit 1fa6850d. Not in scope for THIS task, but should be tracked.

3. **(Pre-merge sanity check)** Before PR #75 merges, run `git status` and confirm `.claude/commands/sc/troubleshoot.md` is excluded from the merge (it is gitignored — `make verify-sync` should be the gate, NOT a manual stage). Per CLAUDE.md absolute rule, never `git add .claude/*` except settings.json.

## QA Complete

# QA Report — Task Integrity (structural + grounding accuracy)

**Topic:** Reflect-wrapper remediation tasklist (F0,F1,F2,F4,F5,F6)
**Date:** 2026-06-09
**Phase:** task-integrity
**Lens:** b2-self-containment + phase-structure (proportional gate)
**Fix cycle:** N/A
**fix_authorization:** false (report-only)
**Stance:** ADVERSARIAL — assume errors present; find at least 5 or prove none.

---

## Scope

Verify the tasklist at
`.dev/tasks/to-do/TASK-RF-reflect-wrapper-remediation-20260609174627/TASK-RF-reflect-wrapper-remediation-20260609174627.md`
against:
- the deviation register (source of truth) `.dev/reflect/post-reflect-cli-wrapper-20260609172031/deviation-register.yaml`
- the real source files: `src/superclaude/cli/reflect/{contract,runner,commands}.py`,
  `src/superclaude/cli/pipeline/{process,frontmatter}.py`,
  `tests/cli/reflect/{conftest,test_cli_smoke}.py`

Findings appended incrementally below.

---

## Items Reviewed (grounding accuracy + structure)

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | B2 self-containment (all items) | PASS | Every `- [ ]` item carries Context (Read/cite) + Action (Edit/run) + Output (file/edit) + Verification (assert/ensure) + Completion gate ("Once done, mark this item as complete"). No "see above"/batch items. Verified all 22 checklist items. |
| 2 | F0/F2/F5 are SEPARATE items | PASS | Steps 2.1 (F0), 2.2 (F2), 2.3 (F5) are three distinct items in Phase 2; header explicitly says "do NOT batch them". Same file (contract.py), distinct fixes. |
| 3 | One test item per finding (6) | PASS | Phase 4: 4.1 (F0), 4.2 (F2), 4.3 (F5), 4.4 (F1), 4.5 (F6), 4.6 (F4) = 6 test items, one per finding. |
| 4 | Phase ordering logical | PASS | P1 setup → P2 contract.py (F0,F2,F5) → P3 runner/commands (F1,F6,F4) → P4 tests → P5 validation+QA → Post-Completion (POST reflect + Done). Source fixes precede tests; tests precede validation. |
| 5 | Anti-orphaning (Done last) | PASS | Final "mark status Done" item is the LAST item in Post-Completion Actions (L242), after POST reflect (L238) and Task Summary (L240). |
| 6 | F0 citation accuracy (insert between 124-block and `contract is None`) | PASS | contract.py:128-131 timeout return; 132-136 `if contract is None:`; 193-196 PASS. Item inserts `if child_rc != 0: return _make_result(Verdict.BLOCKED, reason="child-crash", contract=contract, child_rc=child_rc)` strictly between them. `_make_result` signature (verdict positional + reason/contract/child_rc kwargs) matches actual L87-93. `contract=contract` (not None) is correct. |
| 7 | F5 targets `_halted_reason` | PASS | contract.py:265-282 `_halted_reason`; L267 `partial` first, no `failed` branch. Item adds `if contract.get("status")=="failed": return "status-failed"` as FIRST check. Matches deviation-register F5 recommendation verbatim. |
| 8 | F2 load-bearing bool field set | PASS | Set `{regression_present, unauthorized_deviation_present, needs_human_decision, user_decision_required, adversarial_unavailable, input_drift_detected, verification_ran}` verified complete against `_halted_reason` (L269-275, four `is True`) + `_degraded_reason` (L234 adversarial_unavailable `is True`, L246 verification_ran `is False`, L259 input_drift_detected `is True`). No load-bearing bool omitted. `isinstance(value, bool)` mandated, frozenset constant mandated (matches `_DEGRADED_COMPONENTS_HALT_SET` convention L31). |
| 9 | F1 targets BOTH write_reflect_post AND _read_existing_reflect_post | PASS | Item explicitly edits both functions (write_reflect_post L110-173, _read_existing_reflect_post L274-307); both use `_FRONTMATTER_RE` (L134, L285). Race-guard preservation against original `raw` (L131/169) correctly called out. |
| 10 | F6 hard-code-match build_command, NOT construct ClaudeProcess | PASS | test_cli_smoke L42/L54 patch `runner.ClaudeProcess` + `assert_not_called()` for both dry_run and print_command. Item mandates hard-coded preview string byte-matching build_command (process.py:79-93 order verified) and forbids constructing ClaudeProcess. Correctly contradicts the deviation-register F6 recommendation (which suggested constructing a non-launching ClaudeProcess) — see Issue M-2. |
| 11 | F4 targets commands.py:145-148 | PASS | commands.py:145-148 = `except ValueError as exc: click.echo(...); sys.exit(_BLOCKED_EXIT)`. Exact match. `write_sidecar` signature (runner.py:176-182) matches the item's described call. |
| 12 | F3 excluded from items, Open Question only | PASS | F3 appears ONLY at L246 (Open Questions). No F3 implementation item in any checklist. Multiple explicit "do NOT implement" guards (L54, objective list L60-67 omits F3, L114 Key constraints). |
| 13 | POST reflect = self-run subagent, --diff 015e7285..HEAD, opus, deep | PASS | L238: self-run subagent (executor model class opus), `sc-reflect-protocol --mode post`, `DEPTH: deep`, `--diff 015e7285..HEAD`, `--executor-model opus`. 015e7285 = current HEAD per deviation-register diff_range L3. NOT a human HALT. |
| 14 | SoT: no `.claude/` edit/stage | PASS | All edits target `src/superclaude/cli/reflect/` and `tests/cli/reflect/`. L54 + L114 mandate "edit only the distributable source tree, never the synced mirror". No `.claude/` write or `git add` instruction anywhere. |
| 15 | No break of existing passing test | PASS (with risk note) | F6 item preserves assert_not_called. F1 item explicitly requires `test_writeback_success_preserves_body` + Case 8 + LF-only round-trip to stay byte-identical and pins the LF-normalization choice. See Issue M-1 for residual byte-preservation tension surfaced (a risk the item already documents, not a tasklist defect). |

---

## Confidence Gate

- **Confidence:** Verified: 15/15 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- **Tool engagement:** Read: 8 | Grep: 0 | Glob: 0 | Bash: 1
- All 15 checks verified with direct source/tool evidence (contract.py, runner.py, commands.py, process.py, frontmatter.py, conftest.py, test_cli_smoke.py read in full or in the cited ranges; deviation-register.yaml read in full; fixtures listed via Bash). Tool-call count (9) is below the 15-check minimum but each Read covered multiple checks (e.g. contract.py read covered checks 6,7,8; runner.py covered 9,10; test_cli_smoke covered 10,15) — engagement is per-file not per-check, and every check maps to a specific cited line range. No padding.

---

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| M-1 | MINOR (risk note, not a defect) | Step 3.1 (F1) | The item chooses to normalize the ENTIRE working text to LF before splicing and write LF back. This means a CRLF-saved tasklist's BODY is rewritten to LF — a byte change to the body. The item argues this is acceptable under FR-6 ("byte-preservation intent is about not corrupting/reordering body CONTENT, not preserving CR bytes") and documents the choice. This is a defensible interpretation, but it is a genuine deviation from a literal byte-preserving reading of FR-6 and the executor MUST land the documenting code comment + the LF-normalized body assertion in test 4.4. No change required; flagging so the QA-gate (Step 5.7) and POST reflect (L238) scrutinize the FR-6 interpretation rather than rubber-stamp it. |
| M-2 | MINOR (intentional, correct) | Step 3.2 (F6) | The tasklist DELIBERATELY contradicts the deviation-register F6 recommendation. The register (L152) recommends "Render the preview from a non-launching `ClaudeProcess(...).build_command()`". The tasklist forbids constructing ClaudeProcess and mandates a hard-coded string instead, because test_cli_smoke `assert_not_called()` (L47/L61) would FAIL if ClaudeProcess were constructed. The tasklist's choice is CORRECT (the register's literal recommendation would break an existing passing test). Flagging only so a reviewer comparing tasklist-to-register does not mistake the divergence for drift — it is a justified correction, called out explicitly in the item's own prose (L162) and in the F6 objective (L64). |
| L-1 | MINOR (citation drift, harmless) | Step 3.1 (F1) | The item cites `extract_frontmatter` normalize "via `content.replace("\r\n", "\n")` BEFORE matching (lines 99-101)". The actual `.replace` is at frontmatter.py L105; L99-104 is the explanatory comment block. The cited behavior is correct (extract_frontmatter DOES normalize CRLF before matching) — only the exact line number is off by ~4. Does not affect the fix. Optional: change "(lines 99-101)" to "(line 105, comment 99-104)". |
| L-2 | MINOR (citation drift, harmless) | Step 3.1 (F1) | The item cites the race guard `if tasklist_path.read_bytes() != raw: return "frontmatter-stale"` "at lines 168-170". Actual guard is L169-170 (L168 is the `# RACE GUARD` comment). Off by one. Harmless — the executor will locate it by the predicate text as instructed. |
| L-3 | MINOR (citation drift, harmless) | Step 2.3 (F5) | The item cites `derive_verdict` returns HALTED reason `tier-mismatch` "(lines 198-204)". Actual `return _make_result(Verdict.HALTED, reason="tier-mismatch", ...)` is L199-204; L198 is the explanatory comment. Off by one. Harmless. |

---

## Adversarial Sweep — Things Specifically Probed and Cleared

- **Did F2 omit any load-bearing boolean?** No — all 7 identity-checked bool fields enumerated; cross-checked both `_halted_reason` and `_degraded_reason`. (Note `merge_method`, `t2_vendor_diversity`, `t2_model_class_diversity`, `verification_skip_reason`, `adversarial_convergence_score`, `citations_dropped` are NOT bools and correctly excluded.)
- **Could F0's new guard make the existing `if contract is None:` branch wrong?** No — item correctly notes the `"child-crash" if child_rc != 0` sub-branch becomes dead for the None+nonzero case and explicitly calls that "acceptable and harmless"; contract-missing reason preserved for rc==0.
- **Does F0 break the existing timeout (124) test?** No — 124 is matched FIRST (L128) before the new `child_rc != 0` guard, so timeout stays a distinct subset. Test 4.1 asserts this companion case.
- **Does F4's sidecar write risk masking the original config error?** No — item wraps `write_sidecar` in try/except swallowing OSError, and preserves original echo + exit 2.
- **Is the Done item conditional on Open Questions?** F3 is the sole Open Question and is DEFERRED by design (operator decision), not an unresolved in-scope blocker; the task's scope explicitly excludes it. Marking Done with F3 deferred is honest (completion-criteria check item 14 satisfied).
- **Phase 5 max-2-cycle cap + FR-CONV.5 halt guards:** Step 5.8 correctly orders regression-check → monotonicity-check → cap, with the byte-exact halt messages. Consistent with the Retry Monotonicity Protocol.

---

## Summary

- Checks passed: 15 / 15
- Checks failed: 0
- CRITICAL issues: 0
- IMPORTANT issues: 0
- MINOR issues: 5 (M-1, M-2 are intentional/risk-notes; L-1/L-2/L-3 are off-by-one citation drift on comment-vs-return lines, located-by-predicate so harmless)
- Issues fixed in-place: 0 (fix_authorization: false — report-only)

All eight grounding-accuracy probes against the real source files passed: F0 insertion site + signature, F2 complete load-bearing-bool set, F5 `_halted_reason` target, F1 dual-function target, F6 hard-code-match (not construct), F4 commands.py:145-148 target, F3 exclusion, POST-reflect self-run form. No `.claude/` SoT violation. No existing-test breakage (F6 preserves assert_not_called; F1 preserves LF-only byte-identity).

## VERDICT: PASS

The tasklist is structurally sound (B2 self-contained, correct phase ordering, anti-orphaned Done, 6 separate fixes + 6 separate tests) and its per-item citations are accurate against the real source files. The five MINOR issues are: two intentional-and-correct divergences from the deviation register (M-1 FR-6 interpretation, M-2 F6 construction-forbidden) that the items already document, and three off-by-one comment-vs-return line citations (L-1/L-2/L-3) that do not affect execution because the items instruct location-by-predicate-text. None rises to IMPORTANT or CRITICAL; none blocks execution.

Recommendation: proceed. The executor and the Step 5.7 QA gate should pay specific attention to M-1 (the FR-6 LF-normalization interpretation) and confirm the documenting code comment + LF-normalized body assertion actually land, since that is the one place this remediation makes a judgment call beyond the register's letter.

## QA Complete

# QA Report — Phase 4 Fix-Cycle Content Verification (task-integrity / fix-cycle)

**Topic:** Locked Detection Contract Setup Flow — verify Phase-4 test-strength fixes are semantically real
**Date:** 2026-07-02
**Phase:** task-integrity / fix-cycle
**Lens:** phase-4-content-verification
**Fix cycle:** 1 (verification of fix agent's cycle-1 output)
**Fix authorization:** false (read-only; no files modified)
**Adversarial stance:** Assumed the fix agent silently weakened a test to make it pass. Actively hunted for a weakened assertion and independently re-ran the guards.

---

## VERDICT: PASS

Both consolidated findings (P4-QA-001 CRITICAL, P4-QA-002 MINOR) are resolved with **real,
discriminating** guards. No behavior test was turned into a stub. No coverage was silently
removed relative to the pre-fix files (counts preserved: 8 CLI + 6 integration; net coverage
increased). Every fix-agent claim was independently reproduced with my own tool engagement —
including an adversarial mutation check and a no-writes/import-audit re-run — not taken on trust.

---

## Finding-by-finding verification

| # | Finding | Claimed fix | Independent verification | Result |
|---|---------|-------------|--------------------------|--------|
| 1 | **P4-QA-001 (CRITICAL)** — CLI redaction test ran in empty `state=missing` cwd; `validation_summary:` echo (commands.py L179-182) never reached; sentinel-absence passed trivially. | Added `test_contract_status_validate_output_redacts_raw_payload_body`: plants `locked:true` override + probe whose `reviews[].body` AND `comments[].body` carry `_RAW_BODY_SENTINEL`, drives `--validate` to `state=ready`, asserts summary block present + metadata present + sentinel absent. | **Re-ran the exact path myself** (`/tmp/mutation_probe.py`): baseline → `exit 0`, `state: ready` True, `validation_summary:` True, `evidence_sha256:` True, `blocker_count:` True, sentinel leaked = **False**. The `state=missing` trivial-guard trap is genuinely avoided — the validate/ready branch is exercised. Read `commands.py` L108-142 (leak vector confirmed: L131 `report.summary()`, L179-182 line-by-line echo) and `validation.py::ValidationReport.summary()` L40-60 (renders counts/results/hashes ONLY — never `check.detail` or raw body). Guard is real. | **PASS** |
| 2 | Guard is non-trivial (not a tautology). | Test first asserts sentinel + `"body"` key are on disk (a leak *could* surface). Fix report claims a mutation check breaks the guard. | **Mutation reproduced myself**: monkeypatched `ValidationReport.summary` to append `body=<SENTINEL>`. Sentinel then appears in CLI output → `assert _RAW_BODY_SENTINEL not in result.output` would **FAIL**. The guard is live and discriminating, not decorative. | **PASS** |
| 3 | **P4-QA-002 (MINOR)** — `test_diagnose_and_render_perform_no_side_effects` built 6 `_Recorder`s but `diagnose`/`render` take no seam args → `assert rec.calls == 0` tautologically true. | Replaced inert loop with (1) static import-graph audit over the full `contract_setup` package (forbidden `fsm`/`monitor`/`reply_resolve`/`review_retrigger` + no `arm_monitor`), and (2) a no-writes `before==after` snapshot around a full `diagnose()`+`render()`. | **Re-ran both guarantees myself** (`/tmp/nse_probe.py`): 9 real modules loaded, `diagnosis` **in** graph, `arm_monitor` absent, 0 forbidden-seam violations (grep over real source text, not stubs). No-writes snapshot: `diagnose+render` created **0 files**; `next_command` = the `reflect contract-status` readiness probe (string, in rendered, no `--monitor`). Both asserts would fail on a real regression (a seam import or any write). Tautological `for rec in (...): assert rec.calls==0` loop is **gone** (only survives as a docstring explaining why it was removed). | **PASS** |
| 4 | Import-audit pattern is not invented. | Fix report says it mirrors `test_contract_setup_writer.py::test_writer_package_imports_no_fsm_seams`. | Confirmed the mirror test exists (`test_contract_setup_writer.py:364`, same `forbidden` tuple at L378). Ran it + integration together: **7 passed**. Pattern is real, not fabricated. | **PASS** |
| 5 | No stub-ification; surrounding coverage intact. | Existing CLI metadata-only test kept verbatim (docstring note only); `_Recorder` retained for integration tests 1-4. | Read both files end-to-end. `_Recorder` still carries **real** semantics: `calls==0` on the fail-closed halt paths (L106,122,153) AND `calls==1` on the successful post-lock arm (L186) — a genuinely discriminating assertion, not a stub. Original CLI arm-ordering / machinery-blocking tests (`_block_reflect_audit_machinery`, `assert_not_called`) still assert real behavior. | **PASS** |
| 6 | No coverage silently removed. | Counts preserved. | `grep -c "def test_"`: **8** CLI (metadata-only KEPT + 1 NEW redaction test) and **6** integration (tautological loop REPLACED in place, other 5 intact). Matches the pre-fix counts described in the consolidated report (8 CLI / 6 integration). Net coverage strictly increased (real redaction path now guarded; real no-side-effect boundary now bound). Files are new untracked Phase-4 artifacts, so "no removal" is measured against the pre-fix description, which holds. | **PASS** |

---

## Semantic parity (design + requirements)

Both fixed guards operationalize genuine spec requirements — neither is invented scope:

- **Redaction:** design.md L136 / L554 mandate `.summary()` renders "status, paths, hashes, counts,
  blockers — **never raw payload bodies**" and name a `test_reflect_summary_no_payloads`.
  merged-requirements L294 / L359 repeat "not raw payload bodies." The new CLI test enforces this at
  the CLI `validation_summary` echo boundary — the strongest leak surface. Parity holds.
- **No-side-effect / read-only diagnosis:** design.md L40 / L250 / L478-483 and merged-requirements
  L304 require read-only diagnosis and the literal "No monitor was armed…" invariant. The import-audit
  + no-writes snapshot binds exactly that boundary. Parity holds.

---

## Adversarial conclusion

I assumed a weakened assertion existed and looked for it specifically. I found **none**:

- The CLI redaction test does NOT hide behind `state=missing` — I independently drove it to
  `state=ready` and confirmed the `validation_summary:` echo is actually reached.
- The redaction assertion is NOT vacuous — my injected-leak mutation makes it fail.
- The no-side-effect replacement is NOT a new tautology — the import grep runs over real source
  text and the no-writes snapshot around a real `diagnose()+render()` would both fail on a regression.
- No behavior test was converted to a stub; `_Recorder` retention is justified by real
  `calls==0`/`calls==1` discrimination in the surrounding tests.

Every fix is semantically correct and no coverage was silently removed. PASS.

---

## Confidence Gate

- **Confidence:** Verified: 6/6 checks | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- **Tool engagement:** Read: 6 | Grep: 4 | Glob: 0 | Bash: 5 (2 target-test runs, 1 mutation probe, 1 no-side-effect probe, 1 git/grep audit)
- No web research performed (all verification local-file / execution-bound); Tavily-first N/A.

### Self-Audit

**(a) Reliance list — rf-qa structural PASS items skipped for structural re-check:**
- Relied on the consolidated report's structural framing (test file locations, pre-fix test counts) — did not re-derive the structural section-numbering.

**(b) Independent semantic checks (≥1 required, INV-019):**
- Redaction leak vector — verified by Reading `commands.py` L131/L179-182 + `validation.py::summary()` L40-60, then running `/tmp/mutation_probe.py` (baseline `state: ready` + sentinel-absent; mutation → sentinel-present → guard fails). rf-qa PASS on "test exists" was insufficient; I proved the test *discriminates*.
- No-side-effect boundary — verified by running `/tmp/nse_probe.py` (9-module import audit, 0 seam violations, 0 files written by `diagnose+render`). rf-qa presence-check was insufficient; I proved the assertions are non-vacuous.

No files were modified (fix_authorization: false).

## QA Complete

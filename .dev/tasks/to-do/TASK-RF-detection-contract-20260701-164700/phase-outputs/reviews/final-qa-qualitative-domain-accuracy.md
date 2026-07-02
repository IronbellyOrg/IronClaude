# QA Report — Domain-Accuracy Qualitative Review (report-validation / task-integrity)

**Topic:** Locked Detection Contract Setup Flow for `/sc:reflect` and `/sc:pr-submit`
**Date:** 2026-07-02
**Phase:** report-qualitative (lens: domain-accuracy)
**Fix cycle:** N/A
**Fix authorization:** false (report-only)
**Stance:** Adversarial — assumed a state/provenance/lockability rule was wrong; verified every rule against actual source.

---

## Overall Verdict: PASS

All five checklist items verified correct against actual source code. No incorrect state/provenance/lockability rule found. No alteration to arming (`DetectionContract.load()` / `for_arming()`) or classifier (`classify()`) semantics.

---

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | Nine UX states match merged-requirements §3 | PASS | `states.py:11-19` defines exactly the 9 states from §3 (`missing, unlocked, unparseable, evidence_missing, validation_missing, validation_failed, stale, ready, declined_by_user`). `diagnosis.py` maps each: MISSING (no override, L79-97), UNPARSEABLE (L99-115), UNLOCKED (`not contract.locked`, L117-132), EVIDENCE_MISSING (L134-154), VALIDATION_MISSING (L157-175), STALE (`_stale_blockers`, L180-182), VALIDATION_FAILED (result≠passed, L183-185), READY (L186-188), DECLINED_BY_USER (`declined_by_user()`, L207-230). Default actions match (e.g. STALE→revalidate, READY→`/sc:pr-submit --monitor 1`). |
| 2 | `FieldProvenance` distinguishes observed/default_suggested/user; required fields not marked observed without payload backing | PASS | `candidate.py:14-16` defines the three provenance constants. `FieldProvenance` (L29-36) carries `observed: bool` + `evidence_ref`. In every derivation helper, `observed=True` is set ONLY when the value resolves against payload: identity observed only if `selected in observed` (L142-147) or exactly one observed login (L149-154); user-supplied identity that is NOT in the payload gets `observed=selected in observed` = False (L142-147). `findings_locus` user answer → `observed = _path_resolves(...)` (L255). `severity_field_path` observed only if a path resolved (L88-91). `required_unobserved()` (L47-60) blocks lock when any MUST_OBSERVE field lacks observed provenance. Confirmed no field is hardcoded `observed=True` without a payload-resolution predicate (only `probe_evidence` L96-98 is unconditionally observed — correct, it is the on-disk evidence path itself). |
| 3 | `polling` non-lockable (LOCKABLE_RESULTS = clean/findings/declined only) | PASS | `candidate.py:26` `LOCKABLE_RESULTS = {"clean", "findings", "declined"}` — `polling` absent. Enforced at 4 layers: `required_unobserved()` appends `expected_classifier_result` when not in LOCKABLE (L58-59); `validation.py:77-83` `expected_not_polling` check + `classifier_matches` requires `!= STATE_POLLING` (L93); `lockgate.py:129-134` `_expected_not_polling` hard-codes `{"clean","findings","declined"}` and L137-143 `_classifier_matches` requires `!= STATE_POLLING`. Test `test_polling_expected_result_rejected_as_non_lockable` asserts `"polling" not in LOCKABLE_RESULTS` and the check fails (validation.py test L246-255). |
| 4 | Cross-PR evidence is shape-only | PASS | `evidence.py:36` `cross_pr_shape_only: bool = False` field; L121 populated from metadata. Enforced: `lockgate.py:92-97` `_pr_identity_recorded` requires `pr_number is not None and not evidence.cross_pr_shape_only`; `validation.py:259-263` `cross_pr_shape_only_blocks_readiness` = `not evidence.cross_pr_shape_only`. Matches §6.3 / §7.6 / AC-7 ("cross-PR evidence cannot assert current PR review completion"). Comments at evidence.py:35 and lockgate.py:97 document the shape-only rule. |
| 5 | `load()`, `for_arming()`, `classify()` semantics UNCHANGED (no diff to detection.py / classifier.py) | PASS | `git diff HEAD -- detection.py classifier.py` = EMPTY. `git status` shows only `contract_setup/` untracked (new package). Both files last committed 2026-06-19 (#190), predating this task (2026-07-01). New code consumes them as read-only seams: candidate.py imports `DetectionContract`; validation.py/lockgate.py import `classify`/`STATE_POLLING`; diagnosis.py imports `_CONTRACT_PATH`, `_LOCAL_OVERRIDE_REL`, `from_yaml`, `_extract_yaml_block`, `_local_override_path`. No re-implementation. Integration test `test_missing_contract_for_arming_halts_before_monitor_arm` confirms `for_arming()` still fail-closed HALTs before arm (T-210). 55 tests pass. |

## Summary

- Checks passed: 5 / 5
- Checks failed: 0
- Critical issues: 0
- Issues fixed in-place: 0 (report-only)

## Issues Found

None.

## Additional domain-accuracy verifications (beyond the 5 items)

- **Lock destination pinned** — Both `lockgate.py:188-197` (`_dest_under_pr_monitor`) and `writer.py:125-141` (`_active_root_lock_path` / `_ensure_lock_destination`) pin the lock target to exactly `_LOCAL_OVERRIDE_REL` = `.dev/pr-monitor/detection-contract.locked.md` (detection.py:40) under the active repo root, and reject `.claude`/`src` parts. Matches §6.12 / AC-11 / AC-12. Shipped contract never targeted.
- **CLI is diagnose/validate/render-only** — `commands.py` `contract-status` (git diff HEAD) imports `diagnose, derive_candidate, load_evidence, validate_candidate, write_report` — NOT `write_lock`, NOT `for_arming`, no monitor arm, no PR mutation. Matches §10 ("no default writes or monitor side effects").
- **Missing-contract halt is presentation-only** — `render_pr_submit_missing_contract_halt` (diagnosis.py:233-255) prints the canonical "No monitor was armed. No comments, pushes, retries, resolves, or retriggers were performed." sentence (§9.5). Docstring L237-238 states it never arms/mutates/writes/executes.
- **Expected-result derivation is evidence-keyed** — `_expected_result` (candidate.py:318-327) returns `polling` (never lockable) when no Augment identity is observed; `declined`/`findings`/`clean` only from Augment-authored bodies. Correct provenance floor.

## Self-Audit (MANDATORY)

1. **Factual claims independently verified against source:** All 5 checklist items + 4 additional domain checks, each mapped to specific file:line. State enum (9), provenance flags, LOCKABLE_RESULTS membership, cross-PR field + 2 enforcement sites, empty git diff, lock-destination pin (2 sites), CLI import set. ~13 discrete claims verified.
2. **Files read to verify:** `states.py`, `candidate.py`, `lockgate.py`, `evidence.py`, `diagnosis.py`, `validation.py`, `writer.py` (full); `detection.py:148-217` (`load`/`for_arming`/`_extract_yaml_block`); `classifier.py:158-217` (`classify`/`STATE_POLLING`); `commands.py` diff; merged-requirements.md (full). Grepped symbols + test invariants across 4 test files. Ran `git diff HEAD`, `git log`, and the 55-test suite.
3. **Why trust this PASS:** The load-bearing claim (item 5, semantic preservation) is machine-proven by an EMPTY `git diff HEAD` on both files plus a last-commit date (#190, 2026-06-19) predating the task, plus a passing integration test that exercises `for_arming()` fail-closed behavior. The state/provenance/lockability rules were each traced to a concrete predicate in source, not inferred. Adversarial stance applied: I specifically hunted for (a) a field hardcoded `observed=True` without payload backing — found none (probe_evidence is legitimately unconditional), (b) `polling` leaking into a lockable set — found none across 4 enforcement layers, (c) cross-PR evidence establishing readiness — blocked at 2 sites, (d) any hidden edit to arming/classifier — none.
4. **Web research:** None required (fully local-file-bound review). No Tavily/fallback invoked.

## Confidence Gate

- **Confidence:** Verified: 5/5 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- **Tool engagement:** Read: 8 | Grep: (bundled in Bash) | Glob: 0 | Bash: 4 (git diff/log/status, symbol grep, test-invariant grep, pytest run)
- Tool-call count (12+) ≥ checklist items (5). No unchecked items. No unverifiable items.

## Recommendations

- None blocking. Green light to proceed. The task correctly implements the shared contract-setup helper as an additive, read-only-seam consumer of the existing arming and classifier surfaces, with the nine UX states, three-valued field provenance, `polling`-non-lockable rule, and cross-PR shape-only rule all faithfully matching merged-requirements §3/§4/§6/§7.

## QA Complete

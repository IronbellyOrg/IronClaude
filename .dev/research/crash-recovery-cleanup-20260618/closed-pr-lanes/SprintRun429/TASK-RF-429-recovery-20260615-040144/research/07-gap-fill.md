# Research: Gap-Fill Addendum (A.8 round 1)

**Topic type:** Gap-fill (resolves the 3 gaps from qa-research-gap-report.md)
**Scope:** G-1 (diagnostic-bundle hazard), G-2 (aienv reader-vs-parser), G-3 (nominator empty-dict)
**Status:** Complete
**Date:** 2026-06-15

The research gate (gap-detection lens) returned FAIL on 3 gaps, all "sharpen builder-item Context, no re-research needed." This addendum records the resolutions so the builder carries them into item Context. No new code surface — every fact below is grounded.

---

## G-1 (resolved) — Diagnostic-bundle hazard: `PROVIDER_EXHAUSTED` → `is_terminal`, NOT `is_failure`

**Finding (convergent across R3 IP-3, R4 F-1, evidence-QA, depth-QA — all source-confirmed):** `executor.py:2103` `if status.is_failure:` runs `DiagnosticCollector` + `FailureClassifier` and writes a `phase-N-diagnostic.md` product-bug bundle BEFORE halting (`:2103-2128`). This is the single-session phase path. The per-task path has its own phase-result block at `:1752-1781` and `continue`s before reaching `:2103`, so per-task `FAIL_PROVIDER_EXHAUSTED` never trips the bundle.

**The spec's §4 Layer-2 wording** ("It is a *failure* … but *flagged infra* (skips remediation)" and the reflect-added note "no auto-remediation consumer in the live executor") is TRUE for the per-task path but the single-session `PhaseStatus` path WOULD trip the bundle if `PhaseStatus.PROVIDER_EXHAUSTED` is added to `is_failure`.

**Resolution the builder MUST encode (P4 item):**
- Add `PhaseStatus.PROVIDER_EXHAUSTED` to the `is_terminal` tuple (`models.py:411-423`) so the phase loop terminates cleanly.
- Do **NOT** add it to `PhaseStatus.is_failure` (`models.py:436+`) — OR, if it must be in `is_failure` for some other consumer, add a one-line guard at `executor.py:2103` excluding `PhaseStatus.PROVIDER_EXHAUSTED` from the diagnostic-bundle branch.
- **Mandatory test (P4):** assert that a single-session ALL_ACCOUNT_COOLDOWN halt writes NO `phase-N-diagnostic.md` bundle (the UX-contract-#4 regression guard).

This refines reflect Finding G: G was rated LOW for the per-task path (correct — it's safe), but the single-session `PhaseStatus` path is where the diagnostic-bundle hazard actually lives.

---

## G-2 (resolved) — `aienv.py` reader-vs-parser: pick os.environ reader, reconcile the test item

**Finding:** No Python in the repo parses the `~/.aienv` FILE; `swarm/config.py` reads already-exported `os.environ` (R1 FILE-4). The spec §6 test plan ("parse a fixture `~/.aienv`") structurally presumes a FILE-parser (option B), while R1 recommends the os.environ reader (option A). `IC_ALIASES` is Unverified as a literal var; the real `scripts/ic` mechanism is per-token `export <name>=<model>` + `IC_PRESET_<name>`.

**Resolution the builder MUST encode (P5 item, `needs_human_decision`-adjacent per `feedback_human_decision_items_must_halt`):**
- Default implementation: **os.environ reader** (option A) — `suggest_alternate_model` reads `ANTHROPIC_DEFAULT_{OPUS,SONNET,HAIKU}_MODEL` + any `T*Model0N` from `os.environ`, matching the resolved failed model. This matches the existing `swarm/config.py` convention and needs no file-format assumption.
- The `aienv.py` UNIT TEST then sets env vars via `monkeypatch.setenv(...)` (NOT a fixture `~/.aienv` file), reconciling the test item with the impl. Update the spec §6 "parse a fixture `~/.aienv`" expectation to "monkeypatch.setenv the alias vars" in the test item Context.
- If a true file-parser is later required, the item Context must note it as the documented fallback — do NOT silently ship the file-parser to satisfy the spec's test-plan wording.
- The item writes a PENDING note rather than auto-applying if the os.environ-reader assumption proves wrong against the real `~/.aienv` at implementation time.

---

## G-3 (resolved, sharpened + re-verified) — Nominator exclusion needs `failure_class` plumbed into an empty `{}` context

**Finding (re-verified by orchestrator, grep + Read):** All three `nominate()` call sites in `rerun_tasks.py` pass a **literal empty `{}`**:
- `:1419` `ReflectReportNominator(from_reflect_report).nominate({})`
- `:1421` `ManualNominator(phase, tasks).nominate({})`
- `:1433` `ManualNominator(phase, default_ids).nominate({})` — where `default_ids = select_default_recoverable_tasks(config.phase_result_json(phase_obj))` (`:1426-1428`).

So the (G) UX-contract-#4 exclusion of `failure_class=="provider_exhaustion"` is **NOT a simple "add a filter to nominate()"** — the `context` dict the nominators receive is empty and `ManualNominator.nominate` reads nothing from it. To exclude provider-exhausted tasks from operator-invoked `rerun-tasks` nomination, the change must be at one of:
- **(a)** `select_default_recoverable_tasks(...)` (`:1426`) — filter out tasks whose persisted `failure_class == "provider_exhaustion"` when building `default_ids` (the cleanest seam; reads phase-result.json which now carries `failure_class`); OR
- **(b)** plumb a `failure_class` map from `task_results` INTO the previously-empty `nominate({...})` context and filter inside the nominator.

**Resolution the builder MUST encode (P6 item, `needs_human_decision`-adjacent):**
- Default: option (a) — filter in `select_default_recoverable_tasks` on the persisted `failure_class` (lowest-risk; the field lands via P2/P3 persistence). Add a test asserting a `FAIL_PROVIDER_EXHAUSTED` task is NOT auto-nominated by the `else`/default `rerun-tasks` path.
- Document in item Context that this is the deeper-than-a-filter reality (empty-`{}` contract) so the executor doesn't hit it cold.
- Fallback per `feedback_human_decision_items_must_halt`: if option (a) proves non-trivial, the P6 item writes a PENDING note + scopes UX-contract-#4 to the live auto-path (which already satisfies it, per G-1) rather than shipping an unreviewed `rerun-tasks` behavior change. Either way, this is non-blocking for P1-P5.

---

## Summary

All 3 gaps are recorded with grounded resolutions and the builder directive for each. G-1 = a code correctness item (is_terminal not is_failure + regression test). G-2 and G-3 = `needs_human_decision`-adjacent items with a documented default + PENDING-fallback per `feedback_human_decision_items_must_halt`. No new research spawns required; the code surface is fully mapped. Cosmetic note (non-blocking): `02-patterns-conventions.md` line 2 has a stale `Status: In Progress` header despite a complete body.

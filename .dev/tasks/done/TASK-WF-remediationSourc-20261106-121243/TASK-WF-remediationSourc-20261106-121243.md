---
schema: workflow-plan/1.2
source: ./source.md
strategy: systematic
depth: standard
slug: TASK-WF-remediationSourc-20261106-121243
version: "1"
priority: Medium
created_date: "2026-11-06"
---

# Preserve gateway tier context and curate the model picker

Source: ./source.md
Goal: Repository-controlled tier selections use each tier's actual context window and ordinary tier mode shows Default plus the actual gateway Tier rows without accidental custom alias/profile duplicates.

## Constraints
- Scope product changes to src/superclaude/skills/ccsession-tag/ccsession, src/superclaude/skills/ccsession-tag/models.py and tests/unit/test_ccsession_tiers.py. Source sections Summary/Files/Acceptance in ./source.md govern every task. Coordinator approval is required if another source file becomes necessary.
- Keep routing aliases, actual per-tier/per-model windows, access checks, inherited unavailable default aliases, non-tier profiles, explicit individual-model routing, explicit show-all/+models and user-settings precedence. No dependencies, global settings/env changes, other-worktree edits, commits, push, PR or Orca link flags.
- Native runtime2.1.318 is verified; do not claim all older versions support picker replacement. Manually typing bare IDs inside running Claude Code bypasses launcher normalization; report this external limit rather than a fake fix. Selected individual models may be re-added by native UI, never silently route them to a tier.
- Source is canonical; run make sync-dev after changes, never stage generated .claude mirrors. Always stage .dev/tasks including progress and artifacts. Evidence paths in tasks are package-relative under ./artifacts/.
- Pipeline hardening stays advisory/latched from source; successful tests/reviews cannot promote that to production pipeline signoff. No provider inference is required or authorized for local control probes.

## Phase 1: Resolve tier identities
## Task 1: Recognize tier aliases and enforce their windows
Inputs: ./source.md Acceptance tier windows/access and source models.py model_window/model-resolve/tier_access, plus existing tests/unit/test_ccsession_tiers.py fixtures. Change models.py shared resolution to recognize bare/suffixed claude-gw-tier names before individual-slot fallback, return the actual tier window and normalize repository-controlled named-tier launches to the existing gateway context-capable spelling. Apply existing owner access rather than bypassing or duplicating it. Add the smallest parameterized matching tests in test_ccsession_tiers.py. Outputs: changed resolver and tests; evidence ./artifacts/t1-tests.log.

Acceptance criteria:
- All configured tiers, explicitly tier0,tier1a,tier1b,tier2, resolve bare/suffixed identities to their own T<N>_WINDOW; fixture850000/850000/850000/500000 remains unequal. No universal850k constant or change to individual-slot fallback.
- Named tier launch selects a context-capable tier spelling when necessary, same routing tier; nonexistent and limited-owner forbidden tiers still reject. Both bare and suffixed allowed launches are tested.
- Related new regression fails before fix and passes after; existing named model and tier tests remain valid. Record exact UV test command/result in task evidence.

## Phase 2: Normalize launch aliases
## Task 2: Export context-capable allowed-tier aliases
Depends on: Task 1

Inputs: ./source.md access-aware alias/window requirements, ccsession tier-mode alias-export block, models.py tier resolution from Task1 and existing alias-export tests in tests/unit/test_ccsession_tiers.py. Use the gateway-compatible context spelling for allowed opus/sonnet/haiku tier exports without changing which tier each alias routes to. Extend existing tests rather than new helpers. Outputs: alias export fix and matching regression; evidence ./artifacts/t2-tests.log.

Acceptance criteria:
- Allowed opus/sonnet/haiku still route to tier1a/tier1b/tier2 respectively, now with context capability consistent with gateway Tier entries and per-tier settings.
- Unavailable tier aliases preserve inherited values or stay unset exactly as before; non-tier launches unchanged. Existing restricted-owner and missing-tier fixtures cover those cases.
- Alias regressions and Task1 regressions pass under UV; tests assert selected spelling and intended window, not just presence of an env variable.

## Phase 3: Curate native picker settings
## Task 3: Build native picker replacement from actual shim rows
Depends on: Task 2

Inputs: ./source.md picker/merge/warm-up requirements, ccsession setup_shim synchronous model-cache warm-up and export_selection, models.py compact_settings, existing proxy transform_models output shape (read-only), and existing launcher harness. In ccsession compose native modelPicker options from the actual successful curated shim list after warm-up, retaining exact ids/display labels/descriptions, with replaceBuiltInOptions true in tier mode. Merge this into existing inline session settings without pinning one model window or discarding explicit compact overrides/user settings. Keep failure behavior graceful; never use stale foreign-base rows. Add minimal exact-row tests in tests/unit/test_ccsession_tiers.py. Outputs: integrated native picker configuration and tests; evidence ./artifacts/t3-tests.log.

Acceptance criteria:
- Ordinary tier-only successful launch supplies only actual gateway Tier options, yielding Default plus those tiers, not custom default aliases or unrelated GPT profile rows; no second tier-label/curation policy is created.
- Explicit show-all/+models options preserve actual curated individual rows. Non-tier profiles/custom behavior unchanged; explicitly selected individual model is not silently routed to tier. Native re-add limitation is reported, not hidden.
- Existing modelSettings windows remain per model. CCSESSION_COMPACT_WINDOW explicit override still works and picker replacement is present; user-provided --settings arguments retain existing precedence/order.
- Warm-up failure does not read stale foreign-base cache or crash normal launch. Tests use deterministic existing fake shim/HTTP fixtures and assert exact options, compaction preservation, override and failure cases.

## Phase 4: Pin integration boundaries
## Task 4: Add launch-path and runtime boundary regressions
Depends on: Task 3

Inputs: all three scoped files, existing fake-launch/shim harness, existing diagnosis artifacts at .dev/troubleshoot/bug-ensure-the-850k-limit-of-20261106114037/artifacts/sdk_probe.py and source acceptance. Add the smallest missing integration regressions to tests/unit/test_ccsession_tiers.py covering normal/compact-override launches, restricted owners, all requested tiers and native-to-shim routing boundary. Extend or adapt the diagnostic control driver only as package-owned evidence under ./artifacts/, consuming repo-produced launch settings/env rather than hand-coded proposed configuration. Outputs: completed regression coverage plus ./artifacts/t4-runtime.json, ./artifacts/t4-tests.log and ./artifacts/t4-checks.log. Do not modify the original report's pre-fix captures.

Acceptance criteria:
- Actual installed Claude Code tool-free restricted controls using repo-produced configuration show tier0/tier1a/tier1b = 850000 and tier2 = 500000 with fixture windows; ordinary tier picker has exactlyDefault plus curated Tier rows. No real model inference/credentials/global settings changes.
- Routing preservation is demonstrated at a native-to-local-shim boundary or equivalent existing real request-capture fixture; bare routing aliases still work and context suffix does not reach upstream as an unknown alias. If a required boundary cannot be observed, report the precise limitation without claiming proof.
- uv run pytest tests/unit/test_ccsession_tiers.py tests/unit/test_ccsession_tag.py tests/skills/test_model_alias_policy.py completes with observed result recorded. New per-tier/window/picker regressions are runnable, no dependency added.
- Targeted lint/format checks plus make sync-dev and make verify-sync have observed outcomes. Product diff stays in scoped canonical files; .dev/tasks package/ledger/artifacts staged, generated .claude mirrors not staged.
- Final delivery names exact issue408 URL, diagnosis report path, plan path, changed files, pytest command/result and external manual-bare-ID/native-selected-individual limitations, preserving hardening advisory. No commit,push,PR.

## Pipeline Hardening
pipeline_hardening_verdict: advisory
waiver_status: latched
Downstream must retain success_with_hardening_advisory, never plain production-readiness success.

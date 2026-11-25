<!-- /sc:issue feature template (simple). Copy to <D>/issue-body.md and fill every placeholder in place. Keep every heading. Write "Not known yet" under a heading when the description and the codebase pass give nothing; never invent a fact. -->

## Feature Summary

Deliver a reusable Review Panel with one shared review model that spec-panel, workflow, reflect and other commands can call. Unify the work associated with #346, including #519 (open, not merged) and #500, #498, #490, #484 and #482 (all merged), rather than treating the existing pieces as completed adoption across callers.

## Problem Statement

The #346 work established a document-review panel used by spec-panel: shared review/revise prompts, configurable reviewer selection, structured findings, merging and a finding ledger. That implementation already exists on `origin/master`; this is not a request to build a second panel from scratch.

The callers do not yet share that path throughout. Spec-panel's review-loop rules call `superclaude review` helpers. Workflow invokes reflect's advisory pre-review through its protocol skill. Reflect has its own tiered review protocol and a CLI Tier 2 ensemble backed by swarm and adversarial merging. These are concrete integration points for unification, not evidence that every mechanism should become identical.

PR #519 proposes the reflect adapter's measurement, dormant-kernel and shadow stages. Its body says the default engine remains legacy, the result contract remains 1.8.0, and findings-v2 and the panel remain dormant or shadow-only. It must not be described as a merged, default-on integration. The remaining rollout sequence and measurable cost/quality benefit are Not known yet.

## User Story

As a user of spec-panel, workflow and reflect, I want those commands to use a reusable Review Panel and shared review model, so that the #346 review work is available across commands rather than maintained as separate review mechanisms.

## Proposed Solution

Consolidate the existing #346 panel and review-loop work into the reusable component, and connect the named callers to it. Reuse the existing panel/tier configuration, findings handling, merge/ledger helpers and telemetry where applicable; keep caller-specific review inputs and result contracts at the caller boundary.

Retain spec-panel's existing panel-backed review loop. Connect reflect's panel-backed path to the same component, accounting for the open, staged work in #519. Workflow can reach the shared panel through its existing reflect pre-review rather than requiring a second review pass. Other callers should reuse that path instead of creating another panel; cli-eval already delegates critique to spec-panel, while cli-portify embeds spec-panel-style review behavior today.

The final shared interface, the complete list of additional callers and the decision to change reflect's default engine are Not known yet.

## Acceptance Criteria

- [ ] The shared panel entry point is documented against `src/superclaude/cli/review/`, with the call paths from spec-panel, workflow and reflect identified; these callers use the same shared review model rather than separate copies of its definitions.
- [ ] Spec-panel still resolves reviewers, merges reports and records revisions through the shared component. A first review followed by revision and re-review demonstrates the existing finding lifecycle, and an unresolved blocking finding at the third review escalates rather than starting a fourth review.
- [ ] Reflect's panel-backed path uses the shared component and preserves its caller-facing result contract. Verification distinguishes that path from the legacy/default path and explicitly accounts for #519's dormant/shadow stages.
- [ ] Workflow's Wave 4 pre-review reaches the shared component through reflect and still records `reflect_status` and `reflect_report_path`; review findings do not silently turn its advisory check into a plan-editing or blocking step.
- [ ] Tests for `panel.py`, `findings.py`, `ledger.py` and `telemetry.py`, plus caller integration checks, demonstrate deterministic panel resolution for equal inputs, revision/re-review transitions, refusal of a merge with no valid findings block, and preserved telemetry validation.
- [ ] The caller documentation identifies how cli-eval's spec-panel critique and cli-portify's embedded review behavior relate to the shared panel, without claiming either is already a direct shared-panel caller.

## Out of Scope

Not known yet.

## Components Affected (from `/sc:analyze`)

Static analysis used fetched `origin/master` because the checked-out documentation branch does not contain `src/superclaude/cli/review/`.

- Shared panel selection and configuration: `src/superclaude/cli/review/panel.py`, `panel_cmd.py`, `data/review-panel.default.json`, `data/review-panel.live7.json` and `data/review-tiers.default.json`.
- Findings and review state: `src/superclaude/cli/review/findings.py`, `ledger.py`, `merge_cmd.py` and `ledger_cmd.py`.
- Telemetry and command registration: `src/superclaude/cli/review/telemetry.py`, `telemetry_cmd.py`, `__init__.py` and `src/superclaude/cli/main.py`.
- Spec-panel caller and shared document-review prompts: `src/superclaude/commands/spec-panel.md` and `src/superclaude/rules/prompts/document_review_loop_prompts.md`.
- Workflow's indirect review caller: `src/superclaude/commands/workflow.md` and `src/superclaude/skills/sc-workflow-protocol/SKILL.md` (Wave 4 invokes `sc:reflect-protocol`).
- Reflect caller and current execution path: `src/superclaude/commands/reflect.md`, `src/superclaude/skills/sc-reflect-protocol/SKILL.md`, `src/superclaude/cli/reflect/commands.py`, `config.py`, `runner.py`, `ensemble.py` and `src/superclaude/cli/swarm/lenses/reflect_review.py`.
- Additional caller context: `src/superclaude/skills/sc-cli-eval-protocol/refs/create-pipeline.md` and `src/superclaude/skills/sc-cli-portify-protocol/SKILL.md`.
- Existing regression surfaces: `tests/review/test_review_panel.py`, `test_review_panel_live7.py`, `test_review_findings.py`, `test_review_ledger.py`, `test_review_telemetry.py`, `tests/skills/test_spec_panel_review_loop.py`, `tests/cli/reflect/` and `tests/cli_portify/`.

## Related Issues/PRs

- [#346](https://github.com/IronbellyOrg/IronClaude/issues/346) — origin
- [#519](https://github.com/IronbellyOrg/IronClaude/pull/519) — adapter (open, not merged)
- [#500](https://github.com/IronbellyOrg/IronClaude/pull/500) — experiments (merged)
- [#498](https://github.com/IronbellyOrg/IronClaude/pull/498) — integration (merged)
- [#490](https://github.com/IronbellyOrg/IronClaude/pull/490) — panel (merged)
- [#484](https://github.com/IronbellyOrg/IronClaude/pull/484) — prompts (merged)
- [#482](https://github.com/IronbellyOrg/IronClaude/pull/482) — quotas (merged)
- [#487](https://github.com/IronbellyOrg/IronClaude/issues/487) — evaluation
- [#489](https://github.com/IronbellyOrg/IronClaude/issues/489) — tiers
- [#488](https://github.com/IronbellyOrg/IronClaude/issues/488) — tiers

<!-- sc:issue:create template=issue-feature-simple -->

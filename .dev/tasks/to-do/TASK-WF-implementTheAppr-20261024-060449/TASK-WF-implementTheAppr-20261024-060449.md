---
schema: workflow-plan/1.2
source: ./source.md
strategy: systematic
depth: standard
slug: TASK-WF-implementTheAppr-20261024-060449
version: "1"
priority: Medium
created_date: "2026-10-24"
---

# Refresh recommendation routing and verified handoffs

Source: ./source.md
Goal: Implement the approved recommendation specification without changing specialized command engines or adding a routing subsystem.

## Constraints

- The execution request in ./source.md incorporates the approved specification. Its original research identity is quoted there for provenance. Preserve functional requirements FR-01 through FR-12, non-functional requirements NFR-01 through NFR-10, accepted dispositions and deferred contradictions C01 through C16.
- Change only the canonical files and maintained mirrors named by specification Section 4.2, with focused regression files beside existing tests where needed. Do not repair deferred specialized-command internals.
- Preserve the direct-change limit, explicit command/executor selection, report-only goals, user authorization ceilings, current deep-remediation coupling and existing command-owned document machinery.
- Do not add a runtime keyword router, classifier keys, cache schema or dependency framework. Cached results become advisory hints through current consumer verification.
- Never install tools, authenticate, update installed user configuration, execute recommended product workflows, commit, push, open a PR or publish artifacts as part of this work.
- Delivery paths below are repo-relative. Task evidence belongs under ./artifacts/. Keep .dev/tasks/ staged, including this package and its evidence. Never stage generated .claude/ mirrors.
- Use UV for Python. Record actual test/evaluation outcomes honestly. Static contract assertions and recorded model-generation results are different evidence classes; neither proves specialized commands were executed.
- Tasks are sequential. Preserve the plan after execution starts. Final whole-plan review and safe archiving belong to the executor, not an extra task.

## Phase 1: Make the governing guide outcome-driven

Goal: Apply the workflow-first boundary and make existing specialist capabilities reachable.
Inputs: Approved specification FR-01 through FR-04, FR-08 through FR-11, Sections 8 and 11; current canonical guide and guide tests.
Outputs: Canonical policy, specialist routes, synchronized core level block and focused guide regressions.
Checkpoint: Task 2 acceptance criteria.
Dependencies: None.

## Task 1: Make ordinary implementation workflow-first across every guide entry point

Update src/superclaude/core/HOW-WE-WORK.md and its level-table copy in src/superclaude/core/CLAUDE.md. Cover levels 3-6, hard-limit wording, sections 3.1-3.4 and 3.7, comparisons/defaults, and simple-plan/task-file/feature-existing/research-first/full-spec/shape-idea/bug/cleanup routes. Update affected assertions in tests/core/test_how_we_work_routing_table.py and tests/core/test_claude_md_routing_block.py; add focused cases where needed.

Acceptance criteria:
- Most planned implementation uses workflow then implement. File count, multiple sessions, existing specifications, risk, auditability, drift or resume alone never select MDTM. Explicit MDTM and exceptional complex long-running phase/checklist/reviewer needs remain supported.
- Full-spec documents stop when requested; ordinary subsequent planning uses workflow. The roadmap composer is conditional on explicit selection or justified exceptional needs, with its internal task-builder/task machinery disclosed rather than rewritten.
- Direct edits retain the one-source-file plus test/five-edit limit and contained cleanup exception. Existing approved plans and managed-package resumes retain their executor.
- The level-table markers and core copy agree. Standard remains workflow's ordinary documented default; quick is conditional, not universally mandatory. Contract cases T01-T13 and behavioral cases S18-S20 are represented by concrete regression assertions.

## Task 2: Add specialist routes and conditional operation boundaries to the guide

Depends on: Task 1

Update src/superclaude/core/HOW-WE-WORK.md and tests/core/test_how_we_work_routing_table.py. Implement all seventeen specialist routes listed in FR-04, enrich the existing ask/module-health/external-research/compare-options/critique-spec/business-strategy/multi-model-review/tests/document-built/check-plan/confirm-built/review-pr/resume rows, and maintain Other commands membership consistently. Include the four retired identities' lifecycle note.

Acceptance criteria:
- Each FR-04 route is represented with real input requirements, verified controls and a deliverable stop, or an explicit contract-gap/unavailable outcome where source contracts disagree. No internal rosters or algorithms are copied into the guide.
- Standalone audits, design, documentation, localization, evaluation-suite create/run, release assessment, post-release work, Sprint bundles, context audits and tier validation do not disappear behind generic implementation or test phrases.
- Report-only auditing never adds cleanup/improve/commit. Explicit modes/depths/output controls survive. Analyze focus and spec-panel critique are defaults only where appropriate. Agent/PM are not default planners; spawn remains decomposition-only; save/load are not executor resume.
- Troubleshoot/reflect/Auggie descriptions match FR-08, including current coupled deep remediation and separate ordinary-planning alternatives. No deferred engine is changed or advertised through a union of conflicting interfaces.
- PR branches choose exactly one monitor ordinal, retain current default 3 and stronger-project-policy conflict disclosure, distinguish creation/attachment/log resume, preserve local review/no-post requests, and never authorize execution through recommendation.
- Existing routing markers and eight-column schema remain valid. New routed commands leave Other-only membership consistently. Side effects, task verification, dry-run writes and missing prerequisites are described honestly. Cover T14-T39 and T59-T74 plus S01-S17 and S21-S29 through guide assertions or the later shared fixture suite.

## Phase 2: Verify live capabilities before constructing recommendations

Goal: Make every matched, cold, native and cached answer obey the current request and source contracts.
Inputs: FR-03, FR-05 through FR-07, FR-10 and current recommendation primitives.
Outputs: Updated recommendation skill, verification/net-value references and condensed worker prompts.
Checkpoint: Task 4 acceptance criteria.
Dependencies: Phase 1.

## Task 3: Implement whole-outcome matching and callable-surface verification

Depends on: Task 2

Update src/superclaude/skills/sc-recommend/SKILL.md, src/superclaude/skills/sc-recommend/refs/surface-enumeration.md and src/superclaude/skills/sc-recommend/refs/delegation-vs-native-heuristics.md. Extend tests/skills/test_sc_recommend_routing_contract.py using existing conventions.

Acceptance criteria:
- Whole requested outcome, explicit selection, artifact and authority ceiling govern matching before generic phrase/size shortcuts. Ordered output resolves conditions and mutually exclusive branches before emitting steps; it preserves applicable prerequisites without extending report-only scope. The unsure row cannot recommend recommend to itself.
- Formal Usage, option tables, argument hints and documented positional/keyword syntax qualify as interface evidence. Examples corroborate but cannot add conflicting example-only flags. Self-contained commands and differently headed actual skill invocations, including tdd, are resolved correctly.
- Resolve the actually callable copy separately from canonical checkout research authority. Read the backing skill and decision-relevant references. Missing dependencies are unavailable; material disagreement is a contract gap, not fabricated parity.
- Explicit deprecated metadata and canonical retirement evidence exclude the four shipped remnants without rejecting legitimate installed-only/custom commands or deleting anything. Same-name uncertain ownership receives clarification.
- Native/no-guide fallbacks retain direct-change limits and the new workflow-first boundary. Contract cases T18/T22/T40-T51/T58 and corresponding specialist scenarios have meaningful assertions.

## Task 4: Make cache consumption request-specific and align condensed prompts

Depends on: Task 3

Update src/superclaude/skills/sc-recommend/SKILL.md and the existing constants in src/superclaude/cli/recommend/prompts.py. Adjust tests/recommend/test_dispatch.py and tests/recommend/test_cache.py and add focused consumer-contract assertions in tests/skills/test_sc_recommend_routing_contract.py. Keep existing cache/schema/dispatch code unchanged unless a minimal necessity is demonstrated against FR-07.

Acceptance criteria:
- Matched routing still bypasses cache lookup/write-back. An unmatched hit is only a candidate/template hint: recheck current objective/authority, actual source/dependencies/lifecycle, bind current inputs and reconstruct the handoff. No verbatim cached answer or another request's paths is emitted.
- Reject incompatible, retired, unavailable or contradictory cached candidates through existing live discovery. Preserve hash, budget and miss protections, guide invalidation and missing-guide/non-checkout/helper-CLI safeguards.
- Existing classifier keys remain unchanged. Task-file-generation means explicit/justified MDTM rather than generic spec/tasklist planning; raw spec generation, populated-document derivation and roadmap artifact intent remain distinct. Correct misleading spec-panel fixtures without weakening cache mechanics.
- Cold-worker policy, source/flag verification, net-value scope and current-request binding agree with the main skill. Contract cases T52-T58 and related classification/retirement fixtures cover actual negative behavior of the consumer contract, not a new runtime router.

## Phase 3: Correct narrow referrals and encode complete regression expectations

Goal: Keep public guidance and acceptance fixtures aligned with the implemented recommendation contracts.
Inputs: FR-04, FR-05, FR-11, FR-12 and approved Section 8 cases.
Outputs: Correct referrals/command summary/hook wording, complete executable contract checks and behavioral fixture definitions.
Checkpoint: Task 6 acceptance criteria.
Dependencies: Phase 2.

## Task 5: Correct bounded referrals and public recommendation claims

Depends on: Task 4

Update src/superclaude/skills/sc-workflow-protocol/refs/overlap-routing.md, src/superclaude/skills/tdd/refs/build-request-template.md, src/superclaude/commands/recommend.md, src/superclaude/hooks/scripts/sc-recommend-phase0.sh and src/superclaude/commands/README.md. Add narrow existing-style regression assertions alongside relevant tests.

Acceptance criteria:
- Workflow's tasklist referral uses the documented positional roadmap and never sends a workflow plan to tasklist or MDTM task.
- TDD's optional follow-on distinguishes ordinary workflow planning from execution of an already existing MDTM file. Its internal document workflow is unchanged.
- Recommend's public flags/plugin filtering/evaluation controls remain unchanged. The summary describes conditional outcomes, actual source verification and advisory cache use accurately, without measured savings claims.
- Hook remains fail-open and accurately described as advisory. No removed post-PR hook or automatic agent/PM activation guarantee is restored. README identifies canonical guide/copy and behavior-check maintenance responsibilities.
- No other specialized engine/referral repair is included. All remaining C01-C16 contradictions are handled conservatively rather than silently fixed. Relevant T44/T70-T74 are covered.

## Task 6: Encode every specified contract and specialist regression case

Depends on: Task 5

Extend the existing tests/core/test_how_we_work_routing_table.py, tests/skills/test_sc_recommend_routing_contract.py, tests/recommend/test_dispatch.py and tests/recommend/test_cache.py as needed. Add a focused tests/recommend/test_routing_refresh.py and tests/recommend/fixtures/routing_refresh_cases.json if the existing files are not a clear fit; these are new test-only outputs, not runtime routing tables. Preserve tests/commands/test_routing_plugin_parity.py intent.

Acceptance criteria:
- Map each of the approved T01-T76 checks to a real focused assertion or a clearly identified behavioral-evaluation requirement. Every S01-S29 fixture has a concrete request, environment, expected target/mode/input retention, negative competitor and side-effect boundary.
- Specialist fixtures include unavailable-plugin and seeded-wrong-cache variants. In particular cleanup-audit, cliEval create/run, release split/no-split/proposal continuation, swarm settings and tier-validation missing-suite cases have direct selection expectations, not unrelated IDs.
- Fixtures never execute recommended commands, authenticate or make external changes. Static text/schema/cache tests are labeled static and do not pretend to demonstrate model generation.
- The 47-command coverage/dispositions remain traceable; four retirements and formatting-only histories are preserved. No prior research check is silently rewritten as runtime success, and original research evidence is retained.
- All affected static regression tests run, with outcomes recorded under ./artifacts/. Failures are repaired within approved scope rather than weakened, skipped or hidden.

## Phase 4: Synchronize distribution and deliver observed evaluation evidence

Goal: Deliver one policy across source and maintained copies, with honest verification evidence.
Inputs: FR-10 through FR-12, approved rollout rules and Tasks 1-6.
Outputs: Maintained plugin/dev mirrors, parity checks and recorded recommendation-generation evidence.
Checkpoint: Task 8 acceptance criteria.
Dependencies: Phase 3.

## Task 7: Synchronize maintained distribution copies and development mirrors

Depends on: Task 6

Synchronize plugins/superclaude/skills/sc-recommend/ with canonical recommendation files and the canonical guide as its bundled reference. Match plugins/superclaude/commands/recommend.md and plugins/superclaude/skills/sc-workflow-protocol/refs/overlap-routing.md to their changed canonical files. Run make sync-dev and make verify-sync, and relevant core/command parity tests.

Acceptance criteria:
- Core level table, canonical guide, bundled guide, recommendation skill/reference tree and changed maintained command/referral mirrors agree byte-for-byte where the existing parity contract requires it.
- Generated .claude/ copies are refreshed but never staged. No broad repair or expansion of unrelated plugin packages occurs; missing capabilities remain visibly unavailable.
- Installed primitives use the required installed/project lookup surfaces or clearly labeled checkout fallback, without new unconditional checkout-only dependencies. Existing cache helpers remain checkout-gated.
- Full affected deterministic tests and sync/parity checks have observed output under ./artifacts/, with unrelated baseline failures distinguished from task failures and no fabricated green results.

## Task 8: Deliver fixture-based generation results and implementation evidence

Depends on: Task 7

Use the fixture definitions from Task 6 to produce recommendation-generation outputs against the updated source policy without executing any recommended workflow. Reuse available project evaluation conventions and native agent tools; do not add a provider SDK, runtime router, CLI engine or installed-user configuration. Write task-owned inputs/results/summary under ./artifacts/ and retain source-specific failure/blocker details. Update only test-owned fixtures or approved recommendation files if a confirmed in-scope generation failure requires correction.

Acceptance criteria:
- Cover S01-S29 and their unavailable-plugin/seeded-cache variants in the evaluation matrix. Record actual generated outputs and per-case pass/fail/blocked status separately from static checks. Do not substitute expected answers for observed output; missing execution prerequisites are explicit blockers, never passes.
- The generated handoffs preserve current inputs, options, deliverable/authority boundaries and contract-gap degradation. Correct confirmed in-scope routing failures; do not execute product commands or repair deferred specialist engines.
- Deliver an evidence-backed implementation summary mapping all twelve requirements and the 47 commands to delivered files/tests/results, with the remaining named contract limitations and any unexecuted evaluation cases explicit. Use a registered research/report template for the summary.
- Appropriate lint/typecheck/tests and current parity/sync outputs are recorded honestly. No optional check substitutes for per-task specification compliance.
- Keep task artifacts staged and product/source changes uncommitted. Whole-plan independent review, final state recheck and safe archive remain the executor's completion duties, not claims made by this task.

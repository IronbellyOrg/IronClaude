# Workflow versus task-builder: merged implementation design

<!-- provenance: variant-1-original.md (A); refactor-plan.md change 1; parent workflow_vs_task_builder-spec.md objective/FR1–FR10; base-selection.md selected base A. -->
## 1. Purpose, authority and implementation boundary

Compare three historical `/task-builder` MDTM task documents with 27 current `/sc:workflow` plans using the same authoritative case requirements. MDTM means the historical task-file format; shared planning quality, not executor-specific syntax, is the comparison target. This is a retrospective, requirement-grounded comparison, not a causal generator benchmark. All parent FR1–FR10 and adopted panel guards bind this design. The seven-change refactor plan is authoritative; immutable runs supersede the parent's conditional resume provision.

Future implementation consists of one suite, one serial companion reusing `SuiteLoader` (manifest loader) and `ClaudeProcess` (process boundary), one small offline test module, and suite inventory documentation updates. No core CLI/schema/skill changes. The parent identifies `_NullLifecycleExecutor` and unwired expectations as non-authoritative: registration or a null-executor PASS cannot establish execution. Current source contracts must be inspected at authoring; this merge establishes no installed API or runtime feasibility facts.

<!-- provenance: A source-only default; refactor-plan.md change 2; parent Corpus; debate-transcript.md C-001/A-001; B proven-only safeguards and context dissent. -->
## 2. Frozen corpus and context

Paths below are repository-relative provenance references, not generator read permissions.

| Case | Authoritative sources | Historical baseline | Binding human decisions |
|---|---|---|---|
| PRD inline-file delivery | `.dev/specs/prd-local-file-delivery-fix.md` | `.dev/tasks/done/TASK-RF-prd-local-file-20260609-005242/TASK-RF-prd-local-file-20260609-005242.md` | Only traceable human constraints from the source |
| Detection-contract setup | `.dev/brainstorms/20260701-142634-reflect-detection-contract-flow/design.md` and sibling `merged-requirements.md` | `.dev/tasks/to-do/TASK-RF-detection-contract-20260701-164700/TASK-RF-detection-contract-20260701-164700.md` | Baseline-directory sibling `BUILD-REQUEST.md` |
| Reflect integration | `.dev/proposals/reflect-in-task-builder.md` and `.dev/proposals/reflect-in-sc-tasklist.md` | `.dev/tasks/done/TASK-RF-20260604-042055/TASK-RF-20260604-042055.md` | Separate user-required S4 token-set correction in baseline-directory sibling `research-notes.md` |

Freeze originals and hashes; verify the parent-reported `autogen_method: task-builder` during preparation. Recover pristine generation versions only where provenance proves them. Otherwise create planning-only normalized copies: remove completion flags, execution logs, reflect verdicts and completion evidence without changing planning instructions. Preserve originals, transformation record and non-pristine labels; judge normalized planning artifacts, never treat historical outputs as gold answers.

V1 defaults to source-only packets. Extract binding HUMAN constraints with source-span provenance and leakage review, excluding adjacent generated research solutions, task content, QA/execution histories and completed code. Unresolved material ambiguity blocks freezing. Each case's nine cells receive identical packet bytes; generators cannot see baselines or hidden rubrics. Historical paths embedded in prose remain subject to enforced denial.

Conditional snapshots are allowed only after an explicit context-mode decision: prove a clean preimplementation boundary, selected source/test paths, commit and file hashes, and absence of solved implementation. Parent preparation may establish provenance; generators receive immutable selected files, never Git access. Do not guess history, mandate reconstruction or expand exploration. If chosen snapshot proof fails, block that context; do not silently switch modes. B's preference for proven snapshots remains dissent, not the selected default. Even proven snapshots do not recreate historical research or establish causal equivalence.

<!-- provenance: refactor-plan.md change 3; parent FR1/FR2/FR3 and assertions; panel matrix/effort guards; debate X-001/A-003. -->
## 3. FR1–FR3: matrix, identity and controls

FR1: Author three schema-valid eval entries, each with nine explicit `parameterize` rows: `model_slot` 1, 2, 3 crossed with `effort` low, medium, high. Require exactly 27 unique expanded IDs. The companion binds each expanded ordinal to its explicit row because the loader does not substitute it. Before spawning, reject invalid ordinals, malformed or duplicate rows, empty/single/extra-model matrices, unsupported levels and incomplete combinations.

Use only current schema fields, inspected before authoring: parent inventory is `name/version/description/defaults/required_binaries/optional_capabilities/evals`, with eval `isolation/inputs/expects/parameterize/no_pty`. Do not invent callbacks, top-level model/effort fields or new CLI flags. Declarative expectations cover plan/contract presence, schema and zero exit; the companion performs authoritative checks.

FR2: Resolve exactly three unique concrete catalog IDs through existing pure local catalog/default/slot readers. Never query the remote catalog, disclose credentials or substitute tier aliases, auto/default identities or unsupported effort. Catalog punctuation is accepted as data, never shell interpolation. Require provider capability evidence covering all nine model/effort combinations and observable routing under execution. Record requested and resolved identity, requested effort and observable effective settings separately. Flag acceptance alone is insufficient; absent capability evidence blocks launch. Missing reasoning telemetry remains unknown: it proves neither ignored effort nor effective reasoning differences.

FR3: Freeze source/context/protocol hashes, strategy `systematic`, depth `standard`, handoff `none`, identical tool policy and identical finite turn/time limits across every cell. Effort is distinct from workflow depth. Any capability failure blocks the controlled matrix rather than authorizing a different configuration.

<!-- provenance: refactor-plan.md change 4; parent FR4/FR5; panel restricted-discovery guard; debate X-002/A-002; user confinement clarification. -->
## 4. FR4–FR5: actual invocation and confinement

FR4: Invoke literal `/sc:workflow` through the actual installed CLI, with canonical command, Skill, refs and template staged and hashed. Preserve workspace-local `.dev/workflow/` output contract, then collect artifacts. Each cell has an isolated current working directory (cwd) and HOME (user configuration root). Require stream-json evidence of actual intended Skill activation; prompt text, staged files or successful exit cannot substitute for the trace.

FR5: Parent preparation precreates restricted roots and artifact paths. Proposed staging is input/protocol files mode `0444`, non-output fixture directories `0555`, artifact output directories `0700`. Validate realpaths and symlinks against explicit allowed roots, ownership and effective privilege, and prevent replacement through any generator-writable parent. Run the generator unprivileged; privileged mode that defeats these protections blocks execution. File modes alone, isolated HOME or cwd are not confinement proof.

Verify an existing restricted/reviewer file-tool policy before reuse, explicitly removing permissive defaults. Allow only packet/protocol reads and artifact-directory writes/edits; deny baseline/rubric reads, historic prose-path reads outside allowed roots, Bash, Agent/subagents, network and MCP. Inspect effective Skill allowed-tools so activation cannot silently widen Write/Edit authority. Settings and discovery behavior must be verified under these same restrictions; failure blocks, never triggers a permission bypass.

Use a small companion-local environment allowlist, injecting only approved necessary provider access without ambient parent secrets. An existing `build_env` seam is provisional until inspected and verified before implementation; no core modification is authorized. This confinement strategy is prospective, not an established installed capability. Offline command/denial checks precede live use. The first approved live matrix cell must prove activation and effective denials and counts toward the 27-cell budget; no unbudgeted smoke probe. Continue only with proven gates; retain failure evidence otherwise.

<!-- provenance: refactor-plan.md change 5; parent FR6/FR7; panel scoring/artifact/evidence/quantity guards; debate C-002 and C blinding caveats. -->
## 5. FR6–FR7: validity and independent quality scoring

FR6: Inspect the current workflow schema and return-contract at authoring, rather than inventing fields. Validate `workflow-plan/1.1`, required frontmatter, phases/tasks, contiguous task IDs, resolved dependency targets and actionable acceptance criteria. Reject checkboxes, numbered lines, placeholders, phase-count overflow under the actual schema, missing plan/contract or stop contracts. Nonzero exit remains failure even with apparently valid files. Eligibility requires successful process evidence, required Skill trace and valid artifacts. Keep format status separate from planning-quality results; do not penalize historical MDTM for workflow executor syntax.

FR7: Before generation, freeze a source-grounded requirement rubric with stable IDs assigned to coverage, correctness, safety, testability, dependencies and scope. Include the binding decisions and S4 correction. Every judgment returns all expected IDs exactly once. Score 0 = absent/contradicted; 1 = partial; 2 = explicit/actionable. Every nonzero score requires an exact quote occurring in the artifact. Reject malformed payloads, unknown/duplicate/missing IDs, scores outside 0–2 and invented/empty nonzero evidence. Repeated matching quotes are allowed; quote presence is not correctness proof.

Use one fixed independent judge/protocol, preferably a concrete ID disjoint from all three generators. If overlap is necessary, disclose and confirm it before launch; never claim blind independence. Strip generator/model/effort metadata from judge inputs and keep the private mapping outside generator access. Each artifact is judged independently, not as a baseline/candidate pair. Format clues and MDTM anchoring can still reveal identity.

Judge each baseline once: three baseline jobs plus V valid-candidate jobs, at most 30. For each nonempty dimension d, compute `100 * sum(scores_d) / (2 * N_d)`; aggregate by equal-weight mean of nonempty dimension means. Candidate delta equals candidate aggregate minus its case's single baseline aggregate. Retain all nine comparisons per case; invalid/missing judgments receive no fabricated delta. One sample per cell supports descriptive rubric-relative findings only, not statistical ranking, correctness proof or causal superiority.

<!-- provenance: refactor-plan.md change 6; parent FR8/FR9; panel immutable-run, budget and quantity refinements. -->
## 6. FR8–FR9: lifecycle, approval and bounds

FR8: Create immutable new run directories; v1 has no resume, artifact reuse, automatic retries or reruns. Preserve original provenance; source, protocol, config, rubric and output hashes; requested/resolved identities; requested/observable effective controls; timings; available usage/cost; stream logs, exit codes and terminal statuses. Unknown telemetry is not zero. Timeout, nonzero exit, missing artifact, unsupported effort and judge failure never become PASS. Preserve invalid artifacts and all 27 comparison rows, including blocked/unattempted cells when execution stops. Separate created/validated from executed/scored.

FR9: Paid launch requires explicit human confirmation of exact matrix, judge/overlap, provider data disclosure, invocation, finite per-call and total time/turn limits, cost uncertainty and spend ceiling. A design merge is not that approval. Execute serially, at most 27 generation jobs and `3 + V` judge jobs. First-cell live checks consume their matrix slot; extras, retries or further samples require new approval. No paid design or validation calls.

Use provider budget enforcement when available. Without it, dollar bounds are soft; unknown pricing is not zero, and a finite approved uncertainty ceiling plus call/time/turn caps is required. Pause on spending uncertainty or cap exhaustion and preserve a partial report. On interruption, terminate and reap children before preserving results; cancellation between cells stops scheduling. Failed baseline judging leaves affected deltas unavailable, not regenerated.

<!-- provenance: refactor-plan.md change 7; parent FR10/deliverables/done gates; panel boundary tests. -->
## 7. FR10: offline checks and completion gates

One small mocked-process test module must falsify matrix/ordinal errors, empty/single/overflow collections, normalization leakage, historic-path baseline reads, source writes, writable-parent escape, allowed-tools widening, missing Skill trace and restricted settings/discovery failures. Also check model/effort/config propagation, absent/unsupported capability evidence, missing/invalid contracts, noncontiguous IDs, phase overflow, invalid score domains/IDs/quotes, timeout/nonzero/cancellation preservation and generation/judge budget divergence. Offline mocks test guards, not installed containment proof.

Future deliverables are `src/superclaude/cli/eval/suites/workflow_vs_task_builder.yaml`, `scripts/eval_workflow_vs_task_builder.py`, `tests/cli/eval/test_workflow_vs_task_builder_companion.py`, and inventory updates in `docs/guides/suites-guide.md`. Frozen corpus/design artifacts belong in `.dev/eval-workspaces/cli-eval/`; authoritative results in `.dev/eval-runs/`. None is authored by this merge except its two designated design artifacts.

At authoring, verify exact command/schema surface, then require describe exit zero, list discovery, focused offline tests/lint and a no-network, no-inference dry run. Parent command intentions are `uv run superclaude eval describe --suite workflow_vs_task_builder` and discovery through `eval list --json`; these are future gates, not commands executed here. Dry-run results are non-authoritative. Actual completion requires faithful 27-row outcomes plus baseline/candidate scores or explicit blocked/failed states, with Section 4 activation/denial evidence and Section 5 evidence validation. No null-executor PASS completes the experiment.

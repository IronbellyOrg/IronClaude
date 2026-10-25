# Research: Bounded root-plugin dependency closure

- **Topic type:** Source-derived required and optional resource mapping
- **Scope:** Task 1, 22 candidate resources and reused specialists
- **Status:** Static required-versus-optional trace complete; runtime UNVERIFIED
- **Date:** 2026-10-24
- **Template:** src/superclaude/templates/modularization-template-review/codebase-research_template.md

---

## Findings

### Delayed source findings received during Task 3 (additional repair approved)

[CODE-VERIFIED] The original closure worker's reports were delivered in a delayed batch after the main session returned a progress response. The previous no-deliverable observation described transport visibility, not missing completed research. Its repeated messages report one completed trace, not separate runtime runs. This section records the newly visible, directly rechecked decision-changing findings; older manifest/calibration statements in that return are historical and superseded by explicit user approvals.

[CODE-CONTRADICTED] The adversarial artifact template and debate summary describe 25 criteria and a denominator of 25, while the authoritative scoring reference includes Invariant & Edge Case Coverage, its eligibility floor, and a denominator of 30 (`src/superclaude/skills/sc-adversarial-protocol/refs/artifact-templates.md:183-201`; `src/superclaude/skills/sc-adversarial-protocol/refs/debate-protocol.md:185-194`; `src/superclaude/skills/sc-adversarial-protocol/refs/scoring-protocol.md:148-181`). Lookup adaptation does not align those instructions.

[CODE-CONTRADICTED] Input-resolution calls a post tasklist mandatory and diff required, despite the current supported minimum of diff OR task log and recommended tasklist (`src/superclaude/skills/sc-reflect-protocol/refs/input-resolution.md:9-15`; `src/superclaude/commands/reflect.md:23-35`). The initial generic no-input STOP also needs to count an explicit task log consistently, without weakening missing-pre-spec or missing-post-diff/log refusal.

[CODE-CONTRADICTED] The restricted reviewer requires an isolated snapshot, not the live shared worktree, while the protocol's explicit snapshot provider is an opt-in, excluded Python-wrapper feature (`src/superclaude/agents/reflect-reviewer.md:48-59`; `src/superclaude/skills/sc-reflect-protocol/SKILL.md:283-291`). A native provider must actually capture the audit inputs, including the selected dirty/untracked state, and prove consistent bytes; relabeling a live path or weakening the read-only allowlist is not a repair.

[UNVERIFIED] These three compatibility repairs are not covered by the earlier calibration-only semantic exception. Task 3 product edits were paused pending the explicit narrow decision. Proposed resolution stays inside the same 22 resources: align two adversarial refs with the existing 30-criterion scorer, align bundled input guards with the current supported minimum, and provision native immutable reviewer snapshots through the bundled reflection protocol/brief lookup path. No canonical edits, wrapper import, new dependency or additional production file is proposed. The user subsequently selected `Allow narrow repairs (Recommended)`; the written native compatibility revision now authorizes exactly these repairs (`native-compatibility-scope-revision.json`). Updated implementation, fresh independent acceptance and real runtime proof remain pending.

### Required calibration compatibility repair (approved, not yet built)

[CODE-CONTRADICTED] File existence and a caller-supplied rubric do not make the canonical calibrator compatible with reflection. The agent mandates six troubleshooting dimensions, gated-minimum arithmetic, Runtime-check cross-tab and direction caps; reflection mandates five different dimensions and their arithmetic mean (`src/superclaude/agents/confidence-calibrator.md:48,61-70`; `src/superclaude/skills/sc-reflect-protocol/refs/reflection-rubric.md:9-13`). The earlier traces below establish file closure only, not this semantic compatibility.

[CODE-CONTRADICTED] The rubric's classification-clarity wording uses Aligned/Refinement/Drift/Regression, while the supported deviation taxonomy defines Authorized/Necessary/Drift/Regression (`src/superclaude/skills/sc-reflect-protocol/refs/reflection-rubric.md:37-45`; `src/superclaude/skills/sc-reflect-protocol/refs/deviation-taxonomy.md:26-83`).

[CODE-VERIFIED] The user explicitly approved adapting only the two bundled resources to reflection's five-dimensional mean and current four categories, preserving read-only tools, independence, citation checks, rubric thresholds and canonical sources. This is the written Task 3 resolution, not an implemented compatibility or runtime claim (`calibration-scope-revision.json`; plan Constraints).

### Reviewer and retained specialist definitions

[CODE-VERIFIED] Blind calibration and citation validation are caller-supplied card/rubric/report consumers; each forbids writes and returns findings for the orchestrator to persist. Their agent definitions are two of the 22 candidates. Optional structural assertion resources are read only when the caller supplies `assertions_path`, so an omitted optional path is not a mandatory ordinary-audit dependency (`src/superclaude/agents/confidence-calibrator.md:35-69`; `src/superclaude/agents/evidence-validator.md:27-67`).

[CODE-VERIFIED] The restricted reflection reviewer has a concrete read-only `tools` allowlist and `permissionMode: plan`; its output is returned, not written, and it must read an isolated reviewer snapshot (`src/superclaude/agents/reflect-reviewer.md:1-8,36-59`). Preserve these bytes when adapting only caller identity/lookup references.

[CODE-VERIFIED] Reuse auditing also returns findings without writes; absent Auggie explicitly caps results at advisory rather than fabricating a complete neighbour search (`src/superclaude/agents/reuse-auditor.md:30-36,128-132,181-185`).

[CODE-VERIFIED] Existing root-cause, self-review and requirements roles have no required installed file lookup in their complete definitions; the retained Socratic mentor's framework command examples are educational background, not requirements of its reflection debrief assignment (`agents/sc-root-cause-analyst.md:1-48`; `agents/sc-self-review.md:1-33`; `agents/sc-requirements-analyst.md:1-48`; `agents/sc-socratic-mentor.md:151-179,251-280`). All four are registered by the isolated native client in `loader-candidates-init.json`.

### Provenance only

[CODE-VERIFIED] June's patch upgraded reflection to pre/post modes with blind calibration, citation validation and real merge; July's patch reverses those exact root-command changes. Neither patch establishes today's dependency closure or authorizes restoration of June's obsolete Sequential requirement (`.dev/research/upstream-merge-impact/automated-sync-fork-reflect.txt:18-111`; `.dev/research/upstream-merge-impact/automated-sync-patches.txt:10870-10963`).

### Adversarial worker return (persisted before consumption)

Static merge-path trace: no additional mandatory file outside the 22 candidates was found in my seven assigned sources. This is a source-only result, not loader/runtime proof.

| Required edge | Exact source evidence | Supplied status |
|---|---|---|
| Mode A comparison skill, 2-10 readable files, output guard before writes | src/superclaude/skills/sc-adversarial-protocol/SKILL.md:35-45,55-63 | Candidate skills/sc-adversarial-protocol/SKILL.md; source present, destination absent |
| Artifact templates for diff/debate/base/refactor/merge logs | src/superclaude/skills/sc-adversarial-protocol/SKILL.md:123,208,272,309,328 | Candidate refs/artifact-templates.md; source present, destination absent |
| Scoring algorithm | src/superclaude/skills/sc-adversarial-protocol/SKILL.md:273 | Candidate refs/scoring-protocol.md; source present, destination absent |
| Five-step debate rules and dynamic advocate specification | src/superclaude/skills/sc-adversarial-protocol/refs/agent-specs.md:186-208; src/superclaude/skills/sc-adversarial-protocol/SKILL.md:80-82,950-1044 | Candidates refs/debate-protocol.md and refs/agent-specs.md; sources present, destinations absent. Advocates are dynamic, not extra agent files |
| Neutral debate coordination, scoring, merge delegation, return contract | src/superclaude/skills/sc-adversarial-protocol/SKILL.md:128,213,278; src/superclaude/agents/debate-orchestrator.md:25-40 | Candidate agents/debate-orchestrator.md; source present, destination absent |
| Dedicated merge execution and validation | src/superclaude/skills/sc-adversarial-protocol/SKILL.md:1962-1993; src/superclaude/agents/merge-executor.md:25-37 | Candidate agents/merge-executor.md; source present, destination absent |
| Independent fault-finder at standard/deep depth | src/superclaude/skills/sc-adversarial-protocol/SKILL.md:1106-1122,1201-1283 | Prompt and checklist inline in candidate skill; no additional named agent definition required |
| Optional existing branch-trace evidence | src/superclaude/skills/sc-adversarial-protocol/SKILL.md:1199,1257-1258 | Conditional caller artifact only; absent artifact explicitly falls back to inline source enumeration. Installed spawn-command mention is provenance, not a required invocation/read |
| Optional MCP integrations | src/superclaude/skills/sc-adversarial-protocol/SKILL.md:2243-2264 | Serena failure: skip persistence and log warning. Context7 failure: structural-only checks. Do not make these prerequisites or claim domain validation succeeded |
| Other modes/callers/framework registration | src/superclaude/skills/sc-adversarial-protocol/SKILL.md:2138-2144,2198-2231,2267-2305 | Mode B generation, pipeline DAG, and framework auto-routing registration are not required by direct Mode A skill invocation. No extra framework/core files are needed for this path |

The inventory confirms those seven source/destination pairs at `.dev/research/upstream-merge-impact/remaining-cleanup-validation/plugin-inventory.json:440-505`. A fresh direct filesystem check also found the root adversarial skill directory and both root agent destinations absent (expected negative evidence). Read all seven sources in full; literal dependency search found no other required file read. Coverage check recorded no flagged gaps for the seven sources, plan, or inventory, with best-effort caveat.

Narrow adaptations needed: plugin-qualified skill/agent identifiers, plugin-root-relative refs and merge-executor lookup, and no implicit global spawn/framework-registration dependency. Keep dynamic advocates/fault-finder behavior, real on-disk merge artifacts, guard-before-write, and failure contracts. BLOCKER: none additional within assigned closure; native loader identities and runtime remain UNVERIFIED and belong to the main trace.

### Reflection worker return (persisted before consumption)

Reflection-only trace complete. No mandatory extra unbundled resource established from the assigned reflection skill + ten refs. This is STATIC ONLY, not closure for agent internals/adversarial/native identities, which you own. Candidate-supplied below means listed in the 22-file plan, not already delivered (inventory marks destinations false).

S=`src/superclaude/skills/sc-reflect-protocol/SKILL.md`; P=`.dev/research/upstream-merge-impact/remaining-cleanup-validation/plans/02-root-plugin.md`; I=sibling `plugin-inventory.json`.

| Edge | Required when | Exact source | Supply/classification |
|---|---|---|---|
| input-resolution; reflection-rubric; deviation-taxonomy; coverage-mapping; reviewer-spec; report-template | Waves 0,1D/3C,UC-2,UC-1,T2,5 respectively | S:1844-1849 | All six candidate refs (I:380-415) |
| runtime-surface | UC-2 symbol tagging/caller sweep | S:515-516 | Candidate ref (I:416-421) |
| confidence-calibrator | T1 card and every T2 card | S:649 | Candidate agent; preserve actual independent calibration, not inline substitute as successful proof |
| evidence-validator | Both modes final gate | S:653,704 | Candidate agent; source fallback is partial, not clean success |
| reflect-reviewer | Every T2 reviewer, including all persona lenses | S:658,664 | Candidate restricted agent; explicit fixed-agent rule supersedes interpreting older rf-qa map rows as separate mandatory reviewer types |
| reuse-auditor | New/changed-symbol neighbour search | S:517-524,657 | Candidate agent; explicit fail-open advisory-capped grep fallback |
| root-cause-analyst/self-review/requirements-analyst | T1 investigation/quick pass/pre coverage | S:646-648 | Existing four specialist mappings specified in P:96 (actual loader proof remains yours) |
| socratic-mentor | Optional deep ambiguous-spec probe | S:656 | Existing root mapping specified in P:96; skip allowed |
| sc-adversarial-protocol | T2 actual debate/scoring/merge | S:699,710-728 | Candidate skill; transitive internals assigned elsewhere. Real merged verdict + calibrated cards required, or loudly documented fallback, never empty-dir success |
| confidence-check | Before actionable Wave-5 recommendations | S:702 | Existing root skill recorded I:370-372, not extra candidate |
| audit-validator | >=20-finding spot check | S:652 | Optional; evidence-validator alone is explicit stricter fallback. No additional file needed |
| rf-qa / rf-qa-qualitative | Older map rows mention structural/doc reviewer roles | S:650-651 versus S:664 | Not mandatory new rf-* agents: fixed restricted reflect-reviewer implements brief-supplied lenses; P:96 explicitly forbids rf-* framework import |
| tech-research | Optional deep best-practice lookup | S:703 | Optional-unavailable, not ordinary audit closure |
| sc-workflow-protocol; task-builder and executors | Opt-in Wave 6 only | S:654-655,700-701 | Outside candidate set; explicit unavailable handoff permitted P:98; not ordinary T1/T2 requirements |
| sc-troubleshoot-protocol | Caller invokes reflect, reverse direction | S:705 | Not a callee dependency |
| promotion-adapters | Wave 7 only | S:1853 | Candidate ref; runtime fixtures suppress promotion |
| ops-integration | Build/operator WARN reference | S:1851 | Candidate ref; maintainer build/CI/hook paths inside it are not audit runtime resources |
| grader-extensions | Eval-time only | S:1852 | Intentionally excluded, permitted P:98 |
| cost-profile.yaml | Caller preflight only; reflect explicitly never reads at runtime | S:1854 | Intentionally excluded, permitted P:98 |
| sc-brainstorm-protocol/SKILL.md:280-285 | Guard provenance citation | S:717 | Not an instructed read/invoke: actual parse/missing-file/no-synthetic-.5 guards and thresholds are restated inline, with stronger disk gate at S:728. Preserve those guards; do not add entire brainstorm skill |

BLOCKER: none established within reflection-only assigned files. Existing-root specialist names and candidate loader IDs remain UNVERIFIED here, not asserted resolved. All 13 source/plan/inventory paths passed best-effort index-coverage metadata check; actual conclusions came from direct Reads/literal search, not graph completeness. No files modified, no skills invoked. Recommended action: use this table in Task 1 contract alongside your agent/adversarial traces and native mapping proof; do not treat inventory as runtime evidence.

## Gaps

[UNVERIFIED] Actual protocol invocation, Tier-1 calibration/citation-validation and Tier-2 restricted ensemble/merge outputs remain Task 4 runtime gates. Native inventories prove names, not audits. The original trace worker produced no report and was stopped; the two bounded read-only replacement traces above supplied the source findings. No result was reconstructed from the failed worker.

[CODE-VERIFIED] The manifest loader failure was resolved by the user's narrowly authorized homepage-line deletion. The five absent command targets have a separately authorized unavailable-label disposition, not a claim that those commands now exist (`scope-revision.json`; `namespace-scope-conflict.json`; `loader-candidates-init.json`).

## Key Takeaways

[CODE-VERIFIED] The bounded static required-versus-optional map fits the 22 candidates plus the existing four specialists and confidence skill. No additional mandatory resource was established by direct source traces. Global paths must be replaced with plugin-root-relative lookups in bundled resources; logical role invocations must use the independently observed qualified identities. Ordinary audits must explicitly report optional integrations unavailable and must not execute remediation.

[UNVERIFIED] Static closure is not runtime success. Task 3 must deliver/adapt exactly those resources; Task 4 must prove real command dispatch, calibration, restricted reviews, actual merge evidence and final citation validation in isolation.

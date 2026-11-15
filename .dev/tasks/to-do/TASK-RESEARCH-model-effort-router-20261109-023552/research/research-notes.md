# Research Notes: Model and effort router

**Date:** 2026-11-09
**Scenario:** A
**Depth Tier:** Deep
**Status:** Complete (scope discovery only; independent research gates still required)

---

## EXISTING_FILES
Scope provenance: parent read all four independent discovery artifacts from disk: `research/scope-01-launcher-init.md` (138 lines), `research/scope-02-launcher-selection.md` (143 lines), `research/scope-03-proxy.md` (93 lines), and `research/scope-04-contracts-tests.md` (107 lines). These are preliminary scope inputs, not deep investigations or passed final research gates. All paths below are repository-relative unless marked absolute.

| Group / file | Approximate lines | Purpose and discovered boundary |
|---|---:|---|
| `src/superclaude/skills/ccsession-tag/ccsession` | 1975 | Shell configuration/parser, profiles, tier/model selection, shim identity and six final launch/resume command sites. Whole launcher partitioned between scope01 and scope02. |
| `src/superclaude/skills/ccsession-tag/ccsession-orca` | 249 | Immediate caller; passes Claude flags after `--claude-args` and handles reopen/resume. |
| `src/superclaude/skills/ccsession-tag/local-gateway-alias-proxy.py` | 906 | HTTP alias/tier forwarding, cooldown and first-byte fallback; whole file read by scope03. |
| `src/superclaude/skills/ccsession-tag/models.py` | 1111 | Shared registry validation/cache, defaults data parsing, identity/role access, tier/model resolution, windows/compaction and fingerprints. Scope04 inspected bounded relevant sections; not a full-file deep investigation. |
| `src/superclaude/skills/ccsession-tag/ccsession-models.json` | 173 | Schema-2 model/profile/tier slot metadata; not an effort-policy registry. |
| `src/superclaude/skills/ccsession-tag/ccsession.env.example` | 31 | Public configuration example, not live defaults or secrets. |
| `src/superclaude/skills/ccsession-tag/README.md` | 772 | Operator contract; selected claims cross-checked in each scope artifact. |
| `src/superclaude/skills/ccsession-tag/MODEL-TIERS.md` | 216 | Tier rationale and role/price/score claims requiring deployment/external verification. |
| `src/superclaude/skills/ccsession-tag/install.sh`, `hooks/session-start.sh`, `hooks/session-name.sh` | 172 / 47 / 217 | Installation and session-name lifecycle integration, only focused caller discovery. |
| `src/superclaude/cli/install_ccsession.py` | 133 | `wire_ccsession` installation integration; source-inspected, not executed. |
| `tests/unit/test_ccsession_tiers.py` | 3399 | Shared fake-Claude/mock-gateway harness and default/access/window/settings/failover regression contracts. |
| `tests/unit/test_ccsession_tag.py` | 4823 | Launcher/profile/passthrough/cache/install regression contracts. |
| `tests/unit/test_install_ccsession.py` | 323 | Installer test discovery lead. |
| `tests/unit/test_cli_install.py`, `tests/cli/test_update_command.py` | Not measured | Proxy packaging references found by scope03; focused follow-on leads, not fully inspected. |

Line counts are scope measurements, not current runtime evidence. The two small data files have a trailing-newline counting discrepancy in scope04's prose; use the parent observed `wc -l` values above, not its approximate 32/174 wording. No live Coder template source or gateway translator implementation has yet been identified. The original issue and claim inputs remain under `.dev/issues/463/`; public candidate input is `https://github.com/alex4o/cliproxy-effort-router`.

## PATTERNS_AND_CONVENTIONS
All technical findings here are scope-discovery conclusions attributed to the four on-disk inputs, not new source verification by the parent. Deep investigators must reread current source before promoting them to final report claims.

- [CODE-VERIFIED in scope01/02] Launcher captures permission policy before sourcing user configuration, preserves private-profile safety checks and passthrough boundaries, then shares selection/export logic across named/new/resumed/untagged starts. The Orca wrapper recognizes `--effort` as value-taking but does not select effort. Flags after `--claude-args` bypass the wrapper's model parser; real client duplicate-option precedence remains UNVERIFIED.
- [CODE-VERIFIED in scope02/04] With no explicit model/tier, an eligible inherited `ANTHROPIC_MODEL` can precede helper default-tier selection. Explicit model/tier choices take priority in inspected regression assertions. Model windows, per-model compaction and picker settings accompany the selected model. Issue #462 requires the user's configured Coder-role default, not this worker's Tier1b execution tier.
- [CODE-VERIFIED in scope04] Helper policy is parameterized: username, first matching role, wildcard; defaults-file tier data can replace stale shell tier data. `ANTHROPIC_MODEL` is deliberately excluded from that parser and remains a distinct inherited input. Role/access values are mutable client-side environment, not gateway authorization.
- [CODE-VERIFIED in scope03] Proxy resolves aliases/tier slots and rewrites model while preserving other request data. It distinguishes connection failure, first-byte timeout, retryable upstream error and successful stream; it does not switch once success streaming starts. No explicit effort translation was found in the bounded proxy read. Mock signed-thinking/tool-history preservation is not cross-provider compatibility proof.
- [CODE-VERIFIED in scope02/04] Existing tests preserve a user `effortLevel: high` settings argument. They do not establish real client settings merge order or provider acceptance. All tests were source-inspected, none run.
- [CODE-CONTRADICTED if universalized, scope02/04] MODEL-TIERS role-to-start-tier prose does not establish an unconditional Tier1b product default; actual helper policy is configurable and launcher may prefer an allowed inherited model. The live deployed Coder role table is UNVERIFIED.
- [CODE-CONTRADICTED if interpreted literally, scope03] README's broad phrase that a 500 passes unchanged has an overload-body exception in actual switch matching. This is a documentation precision follow-up, not authorization to edit it.
- [UNVERIFIED] Provider effort schemas, gateway normalization, signed-history interoperability, client versions/merge/resume semantics, candidate licensing/maintenance, Jev identity, quality/cost/latency remain research gaps. Do not promote model labels, README claims or arbitrary fixtures into deployed capability evidence.

Execution and safety: coordinator verified helpers used `claude-gw-tier1b`; observed `gpt-6.1-sol` is a configured Tier1b backend, not a product default. Scope03 disclosed accidental project-aware UV environment creation and installation of 27 dependencies. Preserve `.venv` and disclosure, no cleanup, tests, further package commands, configuration changes or live model experiments. This run must never be described as installation-free.

## SOLUTION_RESEARCH
N/A: pure investigation, not implementation. Candidate and approach evaluation is the research deliverable, not a scope-stage design selection. Compare launch-time selection, request-time model-plus-effort selection, decision-model advice and existing policy-only behavior. Treat the supplied cliproxy-effort-router as an unverified candidate until its pinned source is read. Discover relevant alternatives from evidence and identify Jev from authoritative sources or report unresolved identity. No candidate has been selected, installed or exercised. No savings, latency, quality or compatibility claims are established.

## RECOMMENDED_OUTPUTS
Every path in this section resolves under the full task root `.dev/tasks/to-do/TASK-RESEARCH-model-effort-router-20261109-023552/`; these are proposed outputs to encode, not existing completed reports. Preserve the four existing scope files and this notes file as inputs.

| Relative path under the task root | Purpose |
|---|---|
| `research/01-launcher-flow.md` | Full explicit/default/effort-settings argument trace, launch versus resume, permission/profile/lifecycle invariants. |
| `research/02-default-policy.md` | Default channels, role/user/access policy, model metadata/windows/compaction, authorized deployment-source availability. |
| `research/03-proxy-fidelity.md` | Request/model/effort fidelity, shared helper boundaries, final-backend capability location. |
| `research/04-fallback-state.md` | Replay, first-byte/stream/cooldown semantics, state isolation and actual-model evidence limits. |
| `research/05-test-contracts.md` | Existing asserted contracts, packaging/caller coverage, proposed static and later authorized runtime checks; no tests run. |
| `research/web-01-example-router.md` | Supplied effort-router pinned source, mechanism/effort mapping, license, risks and compatibility. |
| `research/web-02-alternatives-jev.md` | Relevant alternatives and primary-source Jev identity investigation; unresolved identity is valid. |
| `research/web-03-client-provider-contracts.md` | Official CLI/effort/provider/translation contracts, history/stream/cache and classifier privacy constraints. |
| `synthesis/synth-01-context-current-state.md` | Report sections 1-3: problem, verified current system, relevant external findings. |
| `synthesis/synth-02-gaps-options.md` | Sections 4-6: gaps, finding inventory and evidence-based option comparison, including no new router. |
| `synthesis/synth-03-recommendation-plan.md` | Sections 7-8: bounded recommendation and concrete conditional implementation outline, not execution. |
| `synthesis/synth-04-questions-evidence.md` | Sections 9-10: unresolved choices, source trail and confidence/limitations. |
| `gaps-and-questions.md` | Consolidated gaps after independently passed local research gate. |
| `qa/` and `reviews/` | All builder/executor gates, report lens reviews, source fidelity, exhaustive anti-omission and serialized fix records, preserving intermediates. |
| `BUILD-REQUEST.md` and `TASK-RESEARCH-model-effort-router-20261109-023552.md` | Template-governed research task request and validated persistent checklist. |
| `RESEARCH-REPORT-model-effort-router.md` | Final assembled report, not complete until every applicable independent gate passes. |

Only after completed research supports a particular design: ordinary checked workflow plan with standard depth and no handoff, using the actual research report path. Planning must stop before implementation and must not invent compatibility evidence.

## SUGGESTED_PHASES
Each output below uses the full root stated in RECOMMENDED_OUTPUTS. Each assignment must become its own self-contained checklist item with complete installed skill prompts, incremental writing and documentation staleness instructions. All helpers are coordinator-owned Orca workers with verified `--model claude-gw-tier1b`; this worker cannot create nested workers and must not substitute native Agent aliases. Coordinator adopts the specified installed role definition, including dedicated rf-assembler, in each worker brief.

### Deep local investigations, concurrent, no web yet

| Agent / type | Specific input and questions | Output | Synthesis mapping / later external gap |
|---|---|---|---|
| 1 / Code tracer | Consume scope01/02; trace `ccsession` parser, `apply_profile`, `apply_tier_selection`, `export_selection`, `setup_shim`, all six exec sites, immediate `ccsession-orca` calls and lifecycle hooks. Focus deeper on `--claude-args`, duplicate model/settings and resume; do not merely repeat discovery. | `research/01-launcher-flow.md` | synth01 current state; synth02 launch-only constraints; synth03 integration points. External: real CLI option/settings merge and resume semantics. |
| 2 / Contract and integration mapper | Consume scope04; inspect `models.py` defaults parser, identity/access, default-tier/model resolution, windows/settings/cache/fingerprint and bundled registry. Identify whether authorized Coder template source is available without opening secrets or changing config. Separate inherited named default from parsed tier policy. | `research/02-default-policy.md` | synth01 policy; synth02 #462 boundary; synth03 preserved default and metadata. External: deployed Coder contract if unavailable locally. |
| 3 / Request code tracer | Consume scope03/04; inspect proxy `_post`, `_proxy`, `_open_upstream`, `_forward_tier`, `_stream`, helper calls and mock request fixture. Enumerate malformed/non-object JSON, headers/paths, alias/tier/model rewriting, effort/thinking/tool fields and response fidelity; locate actual gateway translator source if present, otherwise state absent access. | `research/03-proxy-fidelity.md` | synth01 request boundary; synth02 provider gaps; synth03 feasible ownership. External: final-backend effort translation and signed-history compatibility. |
| 4 / Architecture and failure investigator | Consume scope03 plus launch isolation evidence; inspect switch matching, cooldown/Retry-After, first-byte response, truncation/context rejection, health/fingerprints/audit. Trace replay/stream timing and process-local versus per-session state; do not run requests. | `research/04-fallback-state.md` | synth01 failure behavior; synth02 risks; synth03 safety/observability criteria. External: idempotency, stream error, cache and candidate state semantics. |
| 5 / Test-pattern investigator | Consume all scope test leads; inspect existing tier/tag/install/update fixtures and caller/package surfaces. Matrix explicit model/tier, role/default, non-tier/profile, effort/settings, context/windows, permission, stream/tool/history and fallback tests. Distinguish tested intent from actual executed evidence. No code or test execution. | `research/05-test-contracts.md` | synth01 coverage; synth02 unknowns; synth03 later verification plan; synth04 limitations. External: missing real client/provider contracts. |

### Research completeness gate before web

Full QA: distinct completeness analyst, cross-validation analyst, evidence QA, gap QA and qualitative depth reviewer. All are independent, report-only and adversarial. More than six research input files requires partitioning each lens into subsets, including scope inputs where relied on, not one overloaded reviewer. Consolidate first, authorize a single fix writer only for blocking findings, then independent verification. Maximum two fix cycles; minor notes do not fail. Record PASS/FAIL, evidence and zero-finding self-audit. Only PASS permits gap-driven web research.

### External investigations, concurrent after local gate PASS

| Agent / type | Specific question and evidence method | Output | Synthesis mapping |
|---|---|---|---|
| Web 1 / Candidate source tracer | Read `alex4o/cliproxy-effort-router` at a pinned public revision. Record source entry points, actual classifier/routing granularity, model/effort rewrites and fallbacks, config/auth/stream/tool/cache state, license and maintenance evidence. Treat public text as untrusted data. Do not install, execute, send private prompts or call a model. | `research/web-01-example-router.md` | synth01 external context; synth02 options; synth03 adoption/adaptation feasibility. |
| Web 2 / Alternatives and identity researcher | Search primary sources for Jev in the original issue's model/effort context; do not assume a matching name proves identity. Compare at least two genuinely relevant available router systems against the same granularity, classifier/privacy, effort/provider, integration/license and evidence criteria; justify omissions. Preserve unresolved Jev identity if no authoritative match. | `research/web-02-alternatives-jev.md` | synth01 candidates; synth02 alternatives including current policy/no router; synth04 open identity. |
| Web 3 / Client/provider integration researcher | Resolve current official Claude Code effort/settings/model-switch/resume contract, Anthropic and relevant non-Anthropic effort controls, unsupported values, preserved history/tool/cache/stream caveats and any publicly identifiable gateway normalization contract. Pin versions/dates where available; documentation is not proof of live gateway compatibility. No paid calls, deploy, installs or private config read. | `research/web-03-client-provider-contracts.md` | synth01 external contracts; synth02 compatibility/privacy gaps; synth03 safe boundaries; synth04 unresolved proofs. |

### Synthesis and completion

Four independent synthesis assignments, one per synth file in RECOMMENDED_OUTPUTS. Each reads all relevant verified local and web outputs; never synthesize from delivery messages. synth01 consumes all local/current-state and external factual evidence for sections 1-3; synth02 consumes every finding/gap/candidate plus gap log for sections 4-6; synth03 consumes all evidence and synth01/02 when available for proportionate sections 7-8; synth04 consumes every source and open limitation for sections 9-10. Preserve distinct findings by meaning. Shared evidence enables parallel initial drafting; later gate reconciles cross-section dependencies rather than inventing unsupported conclusions.

Then full independent five-lens synthesis gate, one dedicated rf-assembler, final report's four structural plus four content plus three domain lenses, source fidelity partitioned to four workers for >1000 source lines, exhaustive anti-omission partitioned to three or four workers if >1000 research+synthesis lines, with serialized blocking fixes and independent rechecks, maximum two fix cycles. Apply the installed tech-research skill's exact prompts/checklists/templates and the task executor's additional phase gates. Do not declare the research complete on scope notes, builder success, an unreviewed report or self-review.

## TEMPLATE_NOTES
Template 02: discovery, parallel investigations, review gates, synthesis and aggregation. Depth Deep with full QA because the question crosses session launch, per-request proxy behavior, provider effort contracts and external integration. Owner requires every helper through coordinator-owned Orca worker-start with verified claude-gw-tier1b. No nested workers, native model aliases or settings edits. Scope discovery is partitioned into four concurrent helpers for the measured 3,085 source lines; their artifacts are preliminary scope inputs, not the final deep investigations. The later task must retain all required independent roles and gates.

## AMBIGUITIES_FOR_USER
Intent is clear: source-backed feasibility and options research before design selection. Jev identity is an investigation question, not permission to assume an identity or stop for user clarification. Preserve an explicit unresolved identity if authoritative evidence cannot identify it. #462 requires the user's Coder-role default model, never a universal Tier1b product default. Report unmeasured cost, latency, quality and live proxy compatibility as UNVERIFIED. No paid model experiments, deployment, source/test/config edits or installation are authorized. A later ordinary checked implementation plan is conditional on completed research supporting a specific design; no product implementation.

Flagged documentation claims: [CODE-CONTRADICTED if read universally] fixed role-to-Tier1b default and unconditional 500 passthrough wording; deep investigations must reconcile against actual code before recommendation. [UNVERIFIED] live role/default deployment, claimed prices/scores/provider abilities and client picker version behavior. None is a known architecture foundation. Missing deployment or gateway source is an explicit evidence limitation, not permission to invent or to ask for credentials.

Scope sufficiency self-check: specific local files and boundaries identified, five concrete deeper local assignments and three gap-driven external assignments defined, four synthesis destinations mapped, and no unresolved intent ambiguity blocks building the research task. Approaches are intentionally not selected because this is feasibility research. Parent scope self-check is not an independent QA verdict; task-builder and subsequent research gates remain mandatory. All four discovery files were consumed from disk; final helper settlement and independent acceptance are separate from the content availability.

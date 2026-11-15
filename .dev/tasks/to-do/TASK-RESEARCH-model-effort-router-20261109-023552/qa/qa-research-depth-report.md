# QA Report: Research Depth

**Topic:** Issue 463 feasibility-research task construction
**Date:** 2026-11-09
**Phase:** research-depth
**Fix cycle:** Initial review, no fixes authorized
**Governing template:** Project `.claude/agents/rf-qa-qualitative.md`, Output Format (All Phases).

---

## Overall Verdict: PASS

## Items Reviewed
| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | Explain HOW components work | PASS | Direct reads of scope01 PATTERNS_AND_CONVENTIONS explain permission capture before env loading, opaque Claude-argument passthrough, private-profile safety and helper delegation. Scope02 Selection and export flow explains eligible inherited-model preference, default-tier fallback, resolver failures and merged context/picker settings. Scope04 Existing contracts explains username/role/wildcard policy and distinguishes parsed tier data from the inherited named default. These are mechanisms, not a file inventory. |
| 2 | Trace end-to-end data flows | PASS | Scope01 initialization connects to scope02 shared selection/export, shim setup and six final invocation sites, including named resume and Orca handoff. Scope03 Core proxy and CODE-VERIFIED routing sections trace POST parsing, alias/tier routing, upstream transport and stream forwarding. Research-notes SUGGESTED_PHASES routes each deeper investigation to a named output and synthesis destination. The uninspected final gateway translator is explicitly a boundary to investigate, not a fabricated extension of the trace. |
| 3 | Document edge cases and failure modes | PASS | Scope02 records unknown/disallowed inherited defaults, non-tier launches, resolver exit 2, refresh/picker failure and nested-shim isolation. Scope03 distinguishes immediate connection-failure 502, first-byte timeout switching, truncated error-body 502, overload-body matching, context rejection and no switching after successful streaming starts. Its later request-tracer assignment explicitly covers malformed/non-object JSON and bad Content-Length rather than pretending these have been fully resolved. |
| 4 | Provide replicable patterns | PASS | Scope02 Related tests describes the actual-launcher/fake-Claude/mock-shim recorder fixture and what it captures. Scope04 Inspected test contracts ties each default/override/window/settings/cache scenario to concrete test locations and expected assertions, without claiming passing tests. Research-notes gives five local, three external and four synthesis assignments with concrete questions, evidence methods, file destinations and quality gates. This is sufficient to replicate an investigation pattern, not unsupported generic architecture language. |
| 5 | Enable per-file research checklist items without another source-discovery pass by the builder | PASS | BUILD-REQUEST Granularity and SKILL PHASES require a separate self-contained item per investigator, synthesis output and independent reviewer, with complete installed skill prompts and templates. Research-notes RECOMMENDED_OUTPUTS and SUGGESTED_PHASES provide exact source families, symbols, targeted unknowns, downstream outputs and acceptance sequence. A builder can encode these research tasks now; the investigators' required fresh source reads are the work being planned, not missing builder scope discovery. Product design and external/provider answers are intentionally deferred. |

## Summary
- Checks passed: 5 / 5. Checks failed: 0. Blocking findings: 0. Minor content findings: 0. Minor process notes: 1. Critical issues: 0. Issues fixed in-place: 0.
- The five inputs contain enough behavioral understanding to construct the requested research task. This verdict does not accept the later deep local investigation, public candidate research, synthesis or final report as complete.
- Explicit choices and the user's configured Coder-role default remain protected requirements. Tier1b remains execution policy only; no router architecture, candidate or provider-compatibility claim is selected.
- Evidence is direct inspection of the planning inputs, not independent re-execution of their producer's source inspections or tests. Live deployment defaults, effective effort translation, client merge/resume semantics, Jev identity and quality/cost/latency remain research questions.

## Issues Found
| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| 1 | minor (review process, not research depth) | This review's first dispatch Read | The first dispatch read requested and emitted 100 lines, exceeding the shared contract's under-100 read and under-40 output limits. It covered contract text rather than findings; subsequent file reads were at most 35 lines. This did not remove or weaken any depth check. | Keep later reads bounded; no research-input fix is needed and this note does not trigger a fix cycle. |

No blocking or minor content-depth defect was found in the five assigned research inputs. The process note above is retained transparently rather than described as compliant execution.

## Actions Taken
- Read the governing role's embedded Output Format template and the dispatch's shared contract and complete research-depth prompt before examining research findings. Created this full skeleton first, then populated it through incremental edits.
- Scope is sufficiency to BUILD a feasibility-research task, not acceptance of the future deep investigation or a router design. Only this assigned report is changed; no fixes are authorized.
- Review evidence consists of direct reads of the five assigned scope inputs and BUILD-REQUEST.md. No implementation source, private configuration, web source, test execution, installation, package command or live experiment is required to establish whether the inputs contain behavioral explanations and actionable research assignments.
- Preserve the scope03 disclosure: earlier project-aware UV created `.venv`, built the package and installed 27 dependencies. No cleanup or repeat installation was performed here.

## Inherited Structural Verdict: Reliance Audit (PR-04, INV-019)
No inherited structural PASS was supplied or relied on. The parent's scope self-check was treated as a producer assertion, not an acceptance gate; this report independently evaluated all five depth criteria from the files on disk.

## Recommendations
- Parent builder may consume this depth PASS alongside the other independent gate reports. Preserve all five deeper local assignments, three external investigations, four synthesis outputs and subsequent independent acceptance gates from BUILD-REQUEST.md; this report alone does not settle the combined gate.
- Use the consolidated research-notes output mapping rather than instantiating every scope author's alternative suggested filename. The scope files explicitly defer final naming to the parent, so the alternative proposals are not missing deliverables or unresolved architecture contradictions.
- No research-input repair is required by this lens. Keep unresolved provider/client/deployment facts as investigation questions and do not turn static planning sufficiency into live compatibility or implementation acceptance.

## Confidence and Tool Engagement
**Confidence:** Verified: 5/5 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%

This computation measures the five planning-depth checks only, not the correctness of every underlying implementation assertion or real provider compatibility. Each check is verified by directly reading its explanations, traces, failure descriptions and assigned research outputs. No unchecked depth item remains.

**Tool engagement:** Read: 36 | Grep: 6 | Glob: 2 | Bash: 14 (assessment checkpoint before report completion). File tools supplied the review evidence; Bash was restricted to Orca guide/lifecycle/identity and authorized own-session model metadata. Web calls, tests, package commands, installs, children and model fallback launches: 0 in this review.

**Execution membership:** Startup selected `claude-gw-tier1b`. Orca terminal-show and worker-show proved exact live worker identity but did not expose actual backend metadata; this negative result was escalated rather than accepted as backend proof. The coordinator then authorized selected own-transcript model fields and nonsecret Tier1b environment slots. A unique own-tool-description search found `/home/coder/.claude/projects/-home-coder-workspaces-worktrees-IronClaude-issue-463/ef1f2e36-9910-42a2-a5a5-d772051738cc.jsonl`; jq confirmed five user records containing this exact dispatch and 68 assistant records, all labeled `gpt-6.1-sol`, with latest timestamp `2026-11-09T03:15:51.893Z`. The live selected slot query returned `claude-sonnet-5-5`, `gpt-6.1-sol`, `muse-wonder-full-1.0` in order. Thus this observed backend belongs to live Tier1b slot 2. This is recorded backend membership, not proof of physical provider serving identity or a product default.

The initial selected Orca-environment-name probe returned no values and exit 1; no missing-model inference was drawn. No transcript message bodies, credentials or broad environment dumps were emitted by the identity checks.

## Self-Audit
**(a) Reliance list: rf-qa PASS items skipped for structural re-check:**
- None. No inherited verdict was provided and the producer's own scope-sufficiency statement did not count as independent evidence.

**(b) Independent semantic checks:**
- Read the entire five-file scope set and BUILD-REQUEST.md in direct file reads. Challenged the possibility that the files merely named components: selection conditions, exported metadata, final invocation forms, proxy rewrite/stream behavior and helper policy mechanisms are actually explained.
- Challenged trace completeness across the wrapper boundary and resumed sessions: scope01/02 together cover argument capture through all six final exec forms; actual client precedence is explicitly unverified and assigned deeper investigation, rather than silently inferred.
- Challenged failure coverage: inspected the written distinctions among connection failure, first-byte timeout, error-body classification, context rejection and successful-stream no-retry. Missing external compatibility and unmeasured performance are retained as questions with named investigators.
- Challenged actionability: matched the five local assignments, three web assignments and four synthesis destinations in research-notes with BUILD-REQUEST's explicit granular checklist and later independent gate requirements. They are sufficiently specific for constructing research items without choosing an architecture.
- Challenged false defaults and evidence inflation: the inputs repeatedly distinguish role-dependent user defaults from the research execution tier, fixture assertions from observed tests, and bounded source inspection from gateway/provider proof. Scope03's installation side effect is explicitly preserved, not erased by this review's zero-install count.
- No content-depth issue survived these checks. That conclusion is limited to research-task construction; it is not a zero-defect claim about the implementation or the unperformed deep research. One minor review-process limit violation is separately recorded above.

## QA Complete
VERDICT: PASS

Five of five research-depth checks pass for building the research task. Blocking findings: 0; minor content findings: 0; minor review-process notes: 1. Only this report was authored. The supervising parent must consume the report from disk, combine the other independent lenses, and retain ownership of package staging and subsequent task construction.

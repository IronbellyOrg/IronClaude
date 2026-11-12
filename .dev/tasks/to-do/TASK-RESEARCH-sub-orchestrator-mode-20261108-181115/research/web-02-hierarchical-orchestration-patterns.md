# External Research: Hierarchical Supervision Patterns

**Date:** 2026-11-09
**Status:** Complete (scoped source/web research; independent Phase4 QA pending)
**Template:** tech-research Web Research Agent Prompt and task Step4.2
**Delivery:** User-approved parent persistence of complete inline findings.

## Controlling Correction Addendum: Phase4 B1, cycle1

**Precedence:** This addendum controls the Cognition quantitative claims in this Markdown index and its paired immutable `returned/web-02-returned-findings.json` text field. Both artifacts must be read together. Preserve the original JSON unchanged as provenance; the superseded wording is historical evidence, not an admissible claim for synthesis.

**Superseded material:** The original return's §8, “Quantitative evidence and limits,” Cognition row contains: “Cognition reports roughly **two bug findings per Devin-authored PR**, about **58% classified serious**, and roughly **8×** enterprise usage growth over six months”. That quantitative sentence is superseded by the correction below, as is this index's former row beginning `~2 findings/PR,58% serious,8x usage six months`. All dependent summaries or Cognition usage-growth claims derived from either wording are likewise superseded wherever they occur in this paired report. Do not retain the broader enterprise population or ambiguous severity denominator as a controlling claim. Unrelated qualitative findings remain unchanged.

**Corrected finding:** Cognition reports an average of approximately two detected bugs per Devin-authored PR reviewed by Devin Review; approximately 58% of those detected bugs are classified severe, not 58% of PRs. Separately, it reports approximately 8x usage growth over six months only for its largest enterprises segment, not enterprise customers generally. The usage metric and absolute baseline are unspecified. These are first-party operational review/adoption observations, not a controlled hierarchy-versus-flat benchmark and not evidence of a causal hierarchy benefit. Source: https://cognition.com/blog/multi-agents-working . **Relevance: LOW for numerical decision support. Reliability: MEDIUM, first-party operational report. Relationship: supports evidence limits; does not establish local performance or authority.**
<!-- web-provenance: provider=WebSearch reason=tavily-unavailable -->

**Independent verification provenance:** On 2026-11-09, the B1 correction agent independently fetched the primary URL with WebFetch. Tavily search/extract tools were absent from its callable tool inventory, so the permitted `tavily-unavailable` fallback applied; no Tavily call could be attempted. The annotation above preserves task4.2's required fallback-marker format; the actual retrieval tool was WebFetch.

## Scope and Method
Complete exact report: [returned/web-02-returned-findings.json](returned/web-02-returned-findings.json), text field. Both this substantive index and full17-finding report are mandatory for synthesis/fidelity/anti-omission. Full return preserves all quantitative observations, source caveats, five-cost reassessment and option implications. Agent aa682003c5ac3fd7f researched all assigned families; parent persists under approved adaptation. Independent Phase4 QA pending.
<!-- web-provenance: provider=WebSearch reason=tavily-unavailable -->
Tavily/callable aliases unavailable in agent inventory; permitted WebSearch/WebFetch fallback, generic terms only, no private source/issue text sent externally. Official descriptions/papers primary; vendor operational reports not controlled comparative proof. No mutations, tests, launches or model changes. Flat means one coordinator directly supervising workers; hierarchy adds middle supervisor; peer/networked and single-agent designs are distinct. Multi-agent vs single-agent is not hierarchy vs flat.

## Current Source Baseline
Researcher directly verified source/instruction text, not runtime compliance:
| Source | Verified meaning / limit |
|---|---|
| src/superclaude/core/WORKER-CONTRACT.md:60,62,69 | [CODE-VERIFIED instructions]Internal Agent fan-out retained, top lifecycle reserved, worker-session Orca fan-out prohibited, governed coordinator person-opened. |
| Contract:57,41-44,229-235,239-246,271-273 | [CODE-VERIFIED instructions]Human Rulings/outward boundaries, Task-specific commit grant and existing flat admission/fan-in. New question is recursive composition, not absence of any aggregation. |
| src/superclaude/core/CLAUDE.md:52-59 | [CODE-VERIFIED wording]Middle-coordinator ownership phrase with supervised-worker restriction, not complete upward/downward protocol or exemption. |
| src/superclaude/hooks/scripts/launch-level-guard.sh:450-478,737 versus Contract:107-110,151 | [CODE-VERIFIED]Literal orca recognition, listed exceptions/ESCAPE in bound sessions; worker-show not required worker-list/worker-read/worktree ps. Other controls may still deny alternate spelling; no bypass proof or permission. |
| /home/coder/workspaces/IronOrca/src/main/runtime/orchestration/dispatch-report-mailbox.ts:5-36 | [CODE-VERIFIED development source]Relevant reports use live same-Run pending/dispatched creator Dispatch else Run. [CODE-CONTRADICTED]Universal root-only claim. Installed equivalence/live recovery not certified by this slice. |
| .dev/orca-command-refactor/decisions/D5/RECOMMENDATION.md:48 versus Contract:204-216 | [CODE-VERIFIED historical text]Five costs recorded; command chains now permitted, not autonomous composite authority. Historical root-only prediction also weakened by current routing source. |
External context never overrides these source or instruction boundaries.

## External Findings
<!-- web-provenance: provider=WebSearch reason=tavily-unavailable -->
All17 findings retained; mechanisms, analogies, deductions and reported measurements remain different evidence classes.
| # | Finding | Relevance | Reliability | Relationship | Source |
|---|---|---|---|---|---|
|1|Anthropic research system is one lead with parallel independent workers, not second supervisory generation. Shared context/tightly coupled coding poorer fit than independent breadth research.|HIGH|HIGH own architecture, MEDIUM transfer|supports flat fan-out|https://www.anthropic.com/engineering/multi-agent-research-system |
|2|Explicit objective/deliverable/tools/sources/boundaries and artifact references reduce overlap/gaps/information degradation. Overspawning/excess updates/searches/prompt sensitivity create waste. No isolated effect size.|HIGH|HIGH first-party observations|supports briefs/admission, extends budget concern|https://www.anthropic.com/engineering/multi-agent-research-system |
|3|Synchronous batch waits for slowest worker and cannot redirect active workers in reported system. Asynchronous future improvement adds consistency/reconciliation/failure problems, no measured async gain.|HIGH|HIGH system description|extends latency/blocked-parent concerns|https://www.anthropic.com/engineering/multi-agent-research-system |
|4|Simplest adequate workflow first; dynamic decomposition useful when subtasks not reasonably knowable beforehand, not merely task size.|HIGH|HIGH official guidance, not topology trial|supports measured runtime-only split criterion|https://www.anthropic.com/engineering/building-effective-agents |
|5|Fresh isolated subagents save parent exploration context but need briefs/reconstruction; fork inherits conversation, shared usage still charged, return consumes context. Main conversation better for shared context/frequent exchange/latency sensitivity.|HIGH|HIGH current docs, installed UNVERIFIED|supports bounded helpers, extends tradeoff|https://code.claude.com/docs/en/sub-agents |
|6|Current docs allow three layers below main, depth withholding/fork visibility exception with spawn error at cap. Separate concurrency default20 with exceptions and minimum2.1.217; nesting introversion not given. Print/SDK without forks may let child outlast parent and report main, not Orca proof.|HIGH|HIGH documentation, MEDIUM lifecycle inference|contradicts stale universal no-nesting argument, not policy|https://code.claude.com/docs/en/sub-agents |
|7|OTP supervisor workers/supervisors, restart one/all/later dependents, ordered startup/reverse shutdown. Explicit failure policy needed; no semantic correctness/human authority/side-effect safety guarantee.|HIGH lifecycle/MEDIUM LLM|HIGH OTP, MEDIUM transfer|extends failure ownership|https://www.erlang.org/doc/system/sup_princ.html |
|8|OTP warns nested restart intensities multiply:10x10 permits100 restarts, example upper allowance at most3. Not recommended LLM allowance.|HIGH|HIGH documented arithmetic|supports whole-lineage budget|https://www.erlang.org/doc/system/sup_princ.html |
|9|Finite supervisor shutdown may kill before descendants; unlimited worker cleanup can hang; synchronous ancestor terminate request while ancestor waits child can deadlock. Parent stopped not subtree stopped, no asserted local OTP deadlock.|HIGH|HIGH OTP/MEDIUM analogy|extends cancellation/recovery|https://www.erlang.org/doc/system/sup_princ.html |
|10|Historical January2024 LangGraph distinguishes shared scratchpad, supervisor separate histories and nested graphs. Composition example, no controlled cost/latency/accuracy comparison.|HIGH|HIGH historical architecture/MEDIUM current API|extends concepts|https://www.langchain.com/blog/langgraph-multi-agent-workflows |
|11|Supervisor repository supports compiled teams, full-history vs final-message output, separate delegation/return controls, custom handoffs/forwarding avoiding paraphrase. Retrieved repo archived/read-only, recommends direct tool-calling for new uses; memory checkpoint not durable recovery proof. Current guidance separates per-invocation/persistent and blocking/background with job infrastructure.|HIGH mechanisms/MEDIUM package status|HIGH documented/MEDIUM adoption|extends context/evidence/monitoring tradeoffs|https://github.com/langchain-ai/langgraph-supervisor-py ; https://docs.langchain.com/oss/python/langchain/multi-agent/subagents |
|12|AutoGen0.2 encapsulates nested individual/group chats behind summary; carryover accumulates, default outer response last nested summary; trigger excludes participants to avoid recursion.|HIGH|HIGH versioned example|extends composite interface/context loss|https://microsoft.github.io/autogen/0.2/docs/tutorial/conversation-patterns/ |
|13|AutoGen max_turns vs max_round have different scopes, not total subtree allowance. Last-message vs LLM summary differ; toy traces/costs not comparative latency study, some examples miss target.|HIGH bounds/MEDIUM examples|HIGH mechanics/LOW performance evidence|supports aggregate budgets/cautious tutorials|https://microsoft.github.io/autogen/0.2/docs/tutorial/conversation-patterns/ |
|14|CrewAI manager assigns/checks/completes, auto or custom manager required; context/planning/rate/iteration controls. Inspected guides not proof concurrency, shared monetary/token ceiling or measured superiority.|HIGH|HIGH descriptions, no benchmark|extends role responsibilities; separates hierarchy/parallelism|https://docs.crewai.com/en/learn/hierarchical-process ; https://docs.crewai.com/en/concepts/processes |
|15|Cognition June2025 critique: task/messages can omit consequential decisions, parallel coding can diverge; coupled work needs continuity, bounded investigation acknowledged. No universal failure rate.|HIGH|MEDIUM practitioner analysis|supports coupled-write caution|https://cognition.com/blog/dont-build-multi-agents |
|16|April2026 follow-up recognizes author-reviewer/expert/hierarchical successes, still incomplete granularity/sharing. Not timeless ban. Worktree isolation avoiding collisions but not conflicting assumptions is inference, not measured worktree result.|HIGH|MEDIUM operational account|extends bounded alternatives/integration ownership|https://cognition.com/blog/multi-agents-working |
|17|MAST v3 Oct26,2025:14 failure modes,>1600 traces,7 frameworks; design/misalignment/verification failures. Mostly machine labels with smaller expert sets; not independent probabilities or controlled hierarchy-v-flat trial. Interventions model/benchmark dependent.|HIGH|HIGH primary study, bounded transfer|supports stopping/clarification/verification, not winning topology|https://arxiv.org/abs/2503.13657 ; https://arxiv.org/html/2503.13657v3 |

### Quantitative evidence: nine observations with their baselines
<!-- web-provenance: provider=WebSearch reason=tavily-unavailable -->
| Observation | Meaning and limit | Source / relevance / reliability |
|---|---|---|
|90.2% outperformance|Opus4 lead/Sonnet4 workers vs single Opus4 internal research eval; underlying scores not enough to restate as percentage-point accuracy; no depth2-v-flat gain.|https://www.anthropic.com/engineering/multi-agent-research-system ; HIGH/HIGH report,MEDIUM transfer |
|~4x agent/~15x multi-agent tokens|Both relative to ordinary chat, not15x single-agent research or dollar cost/hierarchy penalty.|Same Anthropic URL; HIGH/HIGH observational |
|Up to90% time reduction,3-5 workers,3+ tools each|Combined parallelism on complex queries, no isolated topology contribution/typical percentile guarantee or need for nesting.|Same Anthropic URL; HIGH/HIGH first-party |
|80% variance by tokens,95% jointly tokens/tools/model|BrowseComp association, not accuracy improvement or causal architecture effect.|Same Anthropic URL; MEDIUM/HIGH report |
|40% time reduction tool description;~20request initial eval;30%-80% illustrative example|Tool-design intervention and examples, not independent overall/hierarchy benchmarks.|Same Anthropic URL; MEDIUM/HIGH wording,method detail limited |
|10x10=100 restarts|OTP local allowances multiply, not LLM result or recommended limit.|https://www.erlang.org/doc/system/sup_princ.html ; HIGH/HIGH |
|25.0%,34.4%,40.6%|MAST ChatDev32-task custom ProgramDev-v0 baseline/prompt/topology,9.4/15.6 percentage-point differences, not general gains or clean hierarchy trial; HumanEval smaller/different.|https://arxiv.org/html/2503.13657v3 ; MEDIUM/HIGH limited scale |
|p=0.4 vs p=0.03|MAST AG2 intervention differed by model; annotation API costs not task costs.|Same MAST URL; MEDIUM/HIGH |
|~2 detected bugs per Devin-authored PR reviewed by Devin Review; ~58% of detected bugs severe; ~8x usage growth in Cognition's largest enterprises segment over six months|Operational review/adoption observations. The 58% denominator is detected bugs, not PRs. The usage metric and absolute baseline are unspecified; the 8x observation does not describe enterprise customers generally. Not a controlled hierarchy-versus-flat benchmark or controlled net-quality/false-positive/latency/hierarchy-cost comparison.|https://cognition.com/blog/multi-agents-working ; LOW numerical relevance/MEDIUM reliability; supports evidence limits, not hierarchy superiority. <!-- web-provenance: provider=WebSearch reason=tavily-unavailable --> |
No matched incremental estimate of adding one middle layer found. Full quantitative table retains explicit URLs for every row and all caveats; shorthand 'same URL' here refers to the immediately named source, never a new measurement.

### Source-access limits and corrected historical reasoning
<!-- web-provenance: provider=WebSearch reason=tavily-unavailable -->
The main LangGraph notebook is a moved-file stub. Pinned historical extraction was dominated by embedded images; readable tail showed recursion_limit150, not supervisor/context-adapter definitions, which were not inferred. Sources: https://raw.githubusercontent.com/langchain-ai/langgraph/main/examples/multi_agent/hierarchical_agent_teams.ipynb ; https://raw.githubusercontent.com/langchain-ai/langgraph/23961cff61a42b52525f3b20b4094d8d2fba1744/docs/docs/tutorials/multi_agent/hierarchical_agent_teams.ipynb . MEDIUM relevance/HIGH observed artifact reliability, internals unverified.

All five original depth-decision costs reassessed in complete return: composite authority still missing despite permitted command chains; dual upward/downward duties real; universal root-mailbox prediction contradicted by inspected creator routing; worker fan-out rule still needs deliberate exception; broader setting versus per-brief authority/rollback remains unverified. Source/history L1-L4 plus https://www.anthropic.com/engineering/building-effective-agents ; https://www.erlang.org/doc/system/sup_princ.html . Correct old reasoning without silently changing current permission.

## Hierarchical versus Flat Comparison
<!-- web-provenance: provider=WebSearch reason=tavily-unavailable -->
Conditional engineering deductions, not measured repository predictions. All rows HIGH relevance; source reliability HIGH for mechanisms, MEDIUM for transfer unless otherwise noted.
| Dimension | Flat supervised | Additional middle layer | Evidence / relationship |
|---|---|---|---|
| Cost | Direct worker calls/briefs/results/root synthesis already paid | Adds middle planning/reporting/repeated context; may save root reconstruction for coherent subtree, no matched estimate | https://www.anthropic.com/engineering/multi-agent-research-system ; https://code.claude.com/docs/en/sub-agents ; extends cost analysis |
| Latency | Direct independent workers already parallel | May avoid upper round trip for newly discovered work, adds serial planning/aggregation and slow-child delays | https://www.anthropic.com/engineering/multi-agent-research-system ; https://docs.langchain.com/oss/python/langchain/multi-agent/subagents ; extends tradeoff |
| Error propagation | Root can misdecompose/admit wrong result | Middle can catch errors or spread wrong interpretation/premature success through subtree | https://arxiv.org/html/2503.13657v3 ; https://www.anthropic.com/engineering/building-effective-agents ; supports aggregate verification |
| Context loss | One delegation boundary, already lossy summaries | More isolation and more opportunities to omit constraints/decisions/questions; traces/context/artifact links address different costs | https://code.claude.com/docs/en/sub-agents ; https://cognition.com/blog/dont-build-multi-agents ; https://github.com/langchain-ai/langgraph-supervisor-py ; extends handoff, HIGH/MEDIUM sources |
| Coordination | Root direct monitoring/admission | Less root detail possible, additional acknowledgments/questions/stopping/reconciliation and dual monitoring duties | https://docs.langchain.com/oss/python/langchain/multi-agent/subagents ; https://microsoft.github.io/autogen/0.2/docs/tutorial/conversation-patterns/ ; supports explicit responsibilities |
| Failure containment/recovery | Fewer ownership transitions | Meaningful subtree failure domain only with settlement/cancellation/takeover; otherwise stranded work | https://www.erlang.org/doc/system/sup_princ.html ; extends lifecycle, analogy not semantic guarantee |
| Budgets | Direct root fan-out easier to count | Per-manager allowances multiply unless lineage accounting, not independent reset | https://www.erlang.org/doc/system/sup_princ.html ; https://microsoft.github.io/autogen/0.2/docs/tutorial/conversation-patterns/ ; supports total resource bounds |
| Coupled writes/integration | Root explicit integration owner | Isolated files can still encode incompatible assumptions and expensive integration | https://cognition.com/blog/dont-build-multi-agents ; https://cognition.com/blog/multi-agents-working ; https://www.anthropic.com/engineering/multi-agent-research-system ; supports isolation plus admission, MEDIUM/HIGH sources |

Plausible unlock: bounded local autonomy over a coherent newly discovered workstream with independently checkable results and genuine local informational advantage. Not unrestricted spawning, not demonstrated repository workload. Source basis: https://www.anthropic.com/engineering/building-effective-agents ; https://www.langchain.com/blog/langgraph-multi-agent-workflows ; https://cognition.com/blog/multi-agents-working . HIGH relevance/MEDIUM inferential transfer/extends value criteria. Full return preserves four option implications: flat default, permitted local investigation, later bounded supervised middle, ordinary ownership separately defined.

## Gaps and Questions
<!-- web-provenance: provider=WebSearch reason=tavily-unavailable -->
All15 original groups retained; full return has exact sources, distinct meaning and consequences.
| Gap | Disposition / evidence |
|---|---|
| Measured local round-trip savings | [UNVERIFIED]No qualifying timing record; vendor research metrics not substitute; https://www.anthropic.com/engineering/multi-agent-research-system |
| Autonomous composite brief | [UNVERIFIED]Contract204-216 chains, not child-dispatch mandate; local baseline. |
| Parent vs child semantic progress | [UNVERIFIED extension]Contract65/113 not new subtree progress reduction; busy children can mask blocked middle. |
| Aggregate success with failed/blocked/partial children | [UNVERIFIED extension]Existing flat admission239-246/271-273 not recursive definition. |
| Child service while parent blocked/fenced/exhausted/replaced | [UNVERIFIED operational]Source routing not takeover; https://www.erlang.org/doc/system/sup_princ.html |
| Cancellation/restart/quiescence | [UNVERIFIED extension]Lineage policy not supplied, local limits must not reset; https://www.erlang.org/doc/system/sup_princ.html |
| Mixed mail and applied acknowledgments | [UNVERIFIED live]Contract61/103-104/131-138/200, no nested experiment. |
|40-line handoff adequacy | [UNVERIFIED]Contract64 worker fields not complete supervisor checkpoint: roster/deliveries/decisions/budgets/uncertain effects. |
| Escalation reaches actual person | [UNVERIFIED new relay]Contract57/155 parent answer not human Ruling. |
| All required probes compatible in bound middle | [CODE-CONTRADICTED blanket claim]Guard475-477 vs Contract107-110/151; no guard expansion authorized. |
| Universal helper root route | [CODE-CONTRADICTED]Development routing16-36 active same-Run creator else Run; not universal root. |
| Routing proves installed/live recovery | [UNVERIFIED]Development source not whole-build equivalence or live recovery. |
| Published provider nesting applies installed | [UNVERIFIED]Current public support not runtime test; https://code.claude.com/docs/en/sub-agents |
| Historical notebook internals | [UNVERIFIED]Moved stub/partial extraction, no invented adapter; https://raw.githubusercontent.com/langchain-ai/langgraph/main/examples/multi_agent/hierarchical_agent_teams.ipynb |
| General hierarchy cheaper/faster/more reliable | [UNVERIFIED]No matched estimate, no capacity10-20/incident elimination/automatic monitoring/depth-change safety proof; https://www.anthropic.com/engineering/multi-agent-research-system ; https://arxiv.org/html/2503.13657v3 |

## Key External Findings
<!-- web-provenance: provider=WebSearch reason=tavily-unavailable -->
- HIGH relevance/HIGH reliability for report/supports: flat lead plus parallel specialists already supplies research benefit; not extra manager evidence. https://www.anthropic.com/engineering/multi-agent-research-system
- HIGH/HIGH mechanisms/extends: hierarchy composable, no demonstrated universal optimization. https://www.langchain.com/blog/langgraph-multi-agent-workflows ; https://microsoft.github.io/autogen/0.2/docs/tutorial/conversation-patterns/ ; https://docs.crewai.com/en/learn/hierarchical-process
- HIGH/HIGH-MEDIUM/extends: isolation vs continuity trade; preserve artifact evidence below summaries. https://code.claude.com/docs/en/sub-agents ; https://www.anthropic.com/engineering/multi-agent-research-system ; https://cognition.com/blog/dont-build-multi-agents
- HIGH/HIGH OTP/MEDIUM transfer/supports: middle must own failure policy, total retry/resources and shutdown/takeover, not just relay. https://www.erlang.org/doc/system/sup_princ.html
- HIGH/HIGH documentation/qualifies stale premise: current provider subagents can nest, not current Orca authority/runtime proof. https://code.claude.com/docs/en/sub-agents
- HIGH/HIGH-MEDIUM/supports: critiques favor bounded collaboration and explicit verification, not unrestricted swarm or timeless ban. https://arxiv.org/html/2503.13657v3 ; https://cognition.com/blog/multi-agents-working
- HIGH/HIGH evidence boundary/supports: no numerical local speedup/cost promise justified by different-baseline metrics. https://www.anthropic.com/engineering/multi-agent-research-system ; https://arxiv.org/html/2503.13657v3

## Recommendations from External Research
<!-- web-provenance: provider=WebSearch reason=tavily-unavailable -->
1. Retain flat supervised default and permitted self-contained investigation/review helpers. HIGH relevance/MEDIUM transfer/supports. https://www.anthropic.com/engineering/multi-agent-research-system ; https://code.claude.com/docs/en/sub-agents
2. Preserve later bounded middle-role option for coherent runtime-discovered work/material root savings, not size/worktree ancestry alone. HIGH/MEDIUM inference/extends. https://www.anthropic.com/engineering/building-effective-agents ; https://www.langchain.com/blog/langgraph-multi-agent-workflows
3. Require full lifecycle: aggregate outcomes/child evidence/human escalation/lineage resources/cancellation/blocked-parent service/replacement ownership. HIGH/MEDIUM transfer/extends. https://www.erlang.org/doc/system/sup_princ.html ; https://arxiv.org/html/2503.13657v3 ; https://microsoft.github.io/autogen/0.2/docs/tutorial/conversation-patterns/
4. Preserve evidence below summaries and one explicit admission/integration authority; isolation not agreement. HIGH/HIGH-MEDIUM/supports. https://www.anthropic.com/engineering/multi-agent-research-system ; https://github.com/langchain-ai/langgraph-supervisor-py ; https://cognition.com/blog/multi-agents-working
5. Correct historical reasoning, not permission: command chains and creator routing deserve credit, neither autonomous authority nor solved probe compatibility; public nesting not local worker exception. HIGH/MEDIUM decision transfer/qualifies. https://code.claude.com/docs/en/sub-agents ; https://www.anthropic.com/engineering/building-effective-agents
No build sequence, model/configuration change or live experiment follows. Current-source qualifications, all measured-result baselines and negative evidence remain mandatory in synthesis.

# External Research: Orca Nested Workers and Roles

**Date:** 2026-11-09
**Status:** Complete (scoped source/web research; independent Phase4 QA pending)
**Template:** tech-research Web Research Agent Prompt and task Step4.4
**Delivery:** User-approved parent persistence of complete inline findings.

## Scope and Method
Complete exact research and source register: [returned/web-04-returned-findings.json](returned/web-04-returned-findings.json), text field. This Markdown is its substantive index; both are required downstream, including source fidelity and anti-omission. Agent aa908bfcc750cfb1a completed actual external research; parent persists under the approved adaptation. Independent Phase4 QA remains pending.

Tavily absent in agent tool list; WebSearch/WebFetch fallback permitted. All external claims below inherit this provenance:
<!-- web-provenance: provider=WebSearch reason=tavily-unavailable -->
Package-metadata-led discovery, links/search-discovered URLs only; official pages/PRs/releases first, public issues for demand. No private text in queries, authentication, mutations, tests, launches or settings changes. Date2026-11-09. Root archive homepage identified [stablyai/orca](https://github.com/stablyai/orca); unpacked metadata supplied installed version. Exact local evidence L1-L9, direct-read line anchors and search/access limitations remain in full return.

## Installed Metadata and Current Source Baseline
Researcher reverified these as source or instruction text, not live execution:
| Surface | Reported evidence/status | Source |
|---|---|---|
| Installed build | [CODE-VERIFIED]1.4.245-aidev02.780594c521aa; commit780594c521aaa2399b242b0022045017f4a77436 | file:///opt/Orca/resources/app.asar.unpacked/out/package.json:5-6 |
| Depth source | [CODE-VERIFIED]default1/root0/invalid unsafe or noninteger below1 falls back1 | file:///opt/Orca/resources/app.asar.unpacked/out/shared/nested-worker-depth.js:6-26 |
| Stored profile | [CODE-VERIFIED stored data]only settings.nestedWorkerMaxDepth filtered,1; not effective running value | file:///home/coder/.config/orca/profiles/local-default/orca-data.json |
| Local helpers | [CODE-VERIFIED]conditional SUB-DISPATCH, same-Run parent-worker mailbox recipe; own-Run variant distinct; active creator recipient/fallback | file:///opt/Orca/resources/app.asar.unpacked/out/main/chunks/orcad-migration-source-retention-B_-OYaBD.js:460,493-519,640 |
| Roles | [CODE-VERIFIED text]five rows, no separate sub-coordinator row; CLI nevertheless uses nested-coordinator mailbox wording | file:///opt/Orca/resources/app.asar.unpacked/out/cli/bundled-skill-guides.js:2372-2380; file:///opt/Orca/resources/app.asar.unpacked/out/cli/specs/orchestration.js:75-80 |
| Permission | [CODE-VERIFIED instruction text]WC-13 fan-out ban at any depth, person-opened coordinator; ownership phrase not permission | src/superclaude/core/WORKER-CONTRACT.md:62,69; src/superclaude/core/CLAUDE.md:55-59 |
| Revisit | [CODE-VERIFIED decision text]defined composite brief AND qualifying runtime-only split/material extra round trip; specified trace before raise | .dev/orca-command-refactor/specs/orca-worker-contract-spec.md:405 |
Local file URLs are not public-access claims. Effective loaded setting, live lifecycle and whole-build equivalence remain unverified.

## External Findings
<!-- web-provenance: provider=WebSearch reason=tavily-unavailable -->
External statements describe their cited version, not current local behavior. HIGH source reliability means primary wording verified, not a live guarantee. All nine original findings and detailed caveats are preserved in the exact return.

| # | Finding | Relevance | Reliability | Relationship | Source URLs |
|---|---|---|---|---|---|
|1|Installed root metadata identifies correct public project; unpacked build metadata lacks homepage/repo/docs. Public/open-source landing page does not guarantee every source path accessible.|HIGH|HIGH identity/page|supports correct discovery|https://github.com/stablyai/orca ; https://www.onorca.dev/docs/cli/orchestration |
|2|Original depth restriction arose from worker Run attachment; later maintainer PR says1 was accidental carryover, raises default4, retains ceiling against recursive delegation. No rationale for exactly4 found. Installed source still1.|HIGH|HIGH rationale/history; MEDIUM reported execution|extends mechanics; contradicts permanent-product-default1 interpretation|https://github.com/stablyai/orca/pull/16668 ; https://github.com/stablyai/orca/pull/38348 |
|3|Public v1.4.251 documents default4 and one-time migration of unmarked stored1. Values>1 retained; later explicit1 retained, but earlier intentional unmarked1 indistinguishable and also migrates. Public doc unversioned; release listing displayed1.4.255 at retrieval. No local upgrade/change performed.|HIGH|HIGH release/migration statements; MEDIUM unexecuted behavior|extends version risk; contradicts applying public4 to installed source1|https://github.com/stablyai/orca/releases/tag/v1.4.251 ; https://github.com/stablyai/orca/pull/38348 ; https://www.onorca.dev/docs/cli/orchestration ; https://github.com/stablyai/orca/releases |
|4|Public eligible-worker helper section predates default raise. Installed ordinary local recipe uses parent Dispatch Run and worker-start --from; questions/escalations/completion reach parent's check alongside coordinator mail; wait for helpers before own completion. Distinct own-Run variant. Creator selector uses active same-Run Dispatch else Run; local helper rejects --on/--terminal. No live proof.|HIGH|HIGH installed source/guide; MEDIUM public author execution|supports native helpers; contradicts universal root-mailbox prediction|https://github.com/stablyai/orca/pull/38348 ; https://github.com/stablyai/orca/blob/main/skill-guides/orchestration.md ; file:///opt/Orca/resources/app.asar.unpacked/out/main/chunks/orcad-migration-source-retention-B_-OYaBD.js |
|5|Public wording explicitly says nested coordinators' child-Run mailboxes; issue describes phase workers as local coordinators. No complete separate authority/lifecycle role found; installed role table still five rows.|HIGH|HIGH wording; MEDIUM issue need|extends role discussion, not permission|https://github.com/stablyai/orca/blob/main/docs/site/content/docs/cli/orchestration.mdx ; https://github.com/stablyai/orca/issues/24970 ; file:///opt/Orca/resources/app.asar.unpacked/out/cli/bundled-skill-guides.js |
|6|Public requests seek phase-local reviewers/implementation helpers and remote lead delegation without root-mediated launches. Plausible fewer round trips, no measured IronClaude savings/correctness/qualifying split.|HIGH|MEDIUM first-hand requests|supports value, does not satisfy local measured-need gate|https://github.com/stablyai/orca/issues/24970 ; https://github.com/stablyai/orca/issues/30141 |
|7|Remote request says desktop allowance did not alter remote default1. PR says hosts enforce own limits, older hosts remain old until updated. Issue closure not proof owner-only remote setter implemented.|HIGH|MEDIUM reported behavior; HIGH stated boundary|supports separate federation uncertainty|https://github.com/stablyai/orca/issues/30141 ; https://github.com/stablyai/orca/pull/38348 |
|8|Newer release announces stopping helpers with worker; PR follows creator-Dispatch descendants. Preserved helpers/descendants may remain; unconfirmed stop uncertain; remote contact needed; interrupted initialization may need retry; terminal close not universal detached-process kill. Not proved installed.|HIGH|HIGH release wording; MEDIUM details author-reported|extends cleanup/failure risk, not current guarantee|https://github.com/stablyai/orca/releases/tag/v1.4.251 ; https://github.com/stablyai/orca/pull/38373 |
|9|Native capability and ownership phrase do not amend current worker fan-out prohibition or person-opened coordinator eligibility.|HIGH|HIGH directly read instruction text|contradicts interpreting native support as present permission|https://github.com/stablyai/orca/pull/38348 ; file:///home/coder/workspaces/worktrees/IronClaude/fix-flaky-parallel-thread-test/src/superclaude/core/WORKER-CONTRACT.md ; file:///home/coder/workspaces/worktrees/IronClaude/fix-flaky-parallel-thread-test/src/superclaude/core/CLAUDE.md |

## Public Sub-Coordinator Evidence and Negative Searches
<!-- web-provenance: provider=WebSearch reason=tavily-unavailable -->
Explicit answer: public nested-coordinator terminology and local-coordinator requests found, but no separate complete role contract in inspected sources. Bounded negative evidence only.

| Inspection | Result / limit |
|---|---|
| Exact nestedWorkerMaxDepth repository search | No search links, not proof absent. |
| sub-coordinator/subcoordinator/sub-orchestrator/sub coordinator/hierarchical orchestration searches | No relevant indexed definition; extracted public docs nevertheless mention nested coordinators. |
| Public guide/raw discovered link | Retrieved text lacked installed five-role table/detailed helper recipe; distribution surfaces differ. |
| https://github.com/stablyai/orca/blob/main/src/main/runtime/orchestration/preamble.ts | Search-discovered, direct fetch404; snippets not promoted to source verification. Reason unknown, not proof private. |
| Public repo landing page | Public/open-source claims visible, no private-implementation assertion established. Inaccessible/private content unexamined, no auth/bypass attempted. |
| Additional tutorial/community evidence | Official recipe plus relevant public requests sufficient; unrelated Orca products/mirror-only claims excluded. |


## Gaps and Questions
<!-- web-provenance: provider=WebSearch reason=tavily-unavailable -->
All fourteen original uncertainty/contradiction groups retained here; full exact return carries sources and detail.
| Gap | Status / consequence / source |
|---|---|
| Effective active depth | [UNVERIFIED]source/stored1 not effective loaded getter/reload behavior; local evidence L2/L9 in return. |
| Public default applied locally | [CODE-CONTRADICTED]public4 not installed source1; https://github.com/stablyai/orca/pull/38348 vs L2. |
| Local depth2 lifecycle | [UNVERIFIED]startup,questions/replies,mixed parent/helper mail,settlement,restart,recovery untested; installed L3. |
| Historical root-mailbox prediction | [CODE-CONTRADICTED for ordinary local helpers]creator route exists, not universal live guarantee; L3. |
| Separate public role | [UNVERIFIED]terminology/request not complete contract; https://github.com/stablyai/orca/blob/main/docs/site/content/docs/cli/orchestration.mdx |
| Why exactly4 | [UNVERIFIED]finite ceiling rationale only; https://github.com/stablyai/orca/pull/38348 |
| Quantified local benefit | [UNVERIFIED]public requests not D5 measured trigger; https://github.com/stablyai/orca/issues/24970 ; local L7. |
| Future migration of this profile | [UNVERIFIED]no upgrade/settings mutation; https://github.com/stablyai/orca/pull/38348 |
| Remote configuration/per-Run override | [UNVERIFIED]closure not owner-only setter/per-Run interface proof; https://github.com/stablyai/orca/issues/30141 |
| New shutdown locally | [UNVERIFIED]public1.4.251 not installed1.4.245 guarantee; https://github.com/stablyai/orca/pull/38373 |
| Depth cap universal safety | [UNVERIFIED]not total-worker,permission,spending/process-isolation guarantee; https://github.com/stablyai/orca/pull/38348 |
| Agent-tool limits/hooks | [UNVERIFIED]outside this Orca web slice; corresponding local gaps remain open; local L6. |
| Inaccessible implementation path | [UNVERIFIED]404 reason not known, no auth attempt; https://github.com/stablyai/orca/blob/main/src/main/runtime/orchestration/preamble.ts |
| Current helper permission | [CODE-CONTRADICTED]native support/ownership wording not waiver of WC-13; local L6/L8. |

## Key External Findings
<!-- web-provenance: provider=WebSearch reason=tavily-unavailable -->
- HIGH relevance/HIGH reliability: product default1 was accidental carryover, newer default4 prevents unbounded recursion; not permanent endorsement of flat-only design. https://github.com/stablyai/orca/pull/38348
- HIGH/HIGH: release/migration can broaden native capability even for an older intentional unmarked1; installed source/stored/effective states remain distinct. https://github.com/stablyai/orca/releases/tag/v1.4.251
- HIGH/HIGH: nested-coordinator wording is mailbox wording, not complete role/grant definition. https://github.com/stablyai/orca/blob/main/docs/site/content/docs/cli/orchestration.mdx
- HIGH/MEDIUM: public local/remote delegation demand supports plausible value, not measured IronClaude need. https://github.com/stablyai/orca/issues/24970 ; https://github.com/stablyai/orca/issues/30141
- HIGH/HIGH for release,MEDIUM author details: descendant stopping has important exceptions and uncertainty, not universal subtree quiescence. https://github.com/stablyai/orca/pull/38373
- HIGH/HIGH installed source: native parent-mailbox path exists while local worker prohibition remains. L3/L6 in complete source register; external context https://github.com/stablyai/orca/pull/38348

## Recommendations from External Research
<!-- web-provenance: provider=WebSearch reason=tavily-unavailable -->
| Recommendation | Basis / qualification |
|---|---|
| Retain flat policy with explicit deferral gates now | Native support removes inherent-impossibility argument, not local permission/need/lifecycle gates; https://github.com/stablyai/orca/pull/38348 and local D5 L7. |
| Prefer native supervised helpers as future candidate over treating handoff owner equivalent | Existing helper recipe/recipient route and different role table; https://github.com/stablyai/orca/issues/24970 and installed guide L4. |
| Separate capability/authority/ownership/terminology | Nested-coordinator wording grants no transitive permission; https://github.com/stablyai/orca/blob/main/docs/site/content/docs/cli/orchestration.mdx and contract L6. |
| Version/migration review prerequisite to any later authorized evaluation | Host builds/effective settings/migration differ; older intentional1 may migrate; https://github.com/stablyai/orca/pull/38348 ; https://github.com/stablyai/orca/issues/30141 |
| Require lifecycle/resource boundaries before endorsement | Helper count,write scope,result admission,mixed mail,cancellation,orphan recovery,preserved descendants not settled by depth/shutdown labels; https://github.com/stablyai/orca/pull/38348 ; https://github.com/stablyai/orca/pull/38373 |
No implementation, upgrade, setting change or live trial requested or authorized here. Full exact return is mandatory downstream evidence, not optional background.

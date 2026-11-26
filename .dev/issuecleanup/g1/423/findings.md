# Issue 423: proactive cross-workspace knowledge review

Template: findings structure registered in `.dev/issuecleanup/g1/362/report-template.md`, adapted to issue 423 and the coordinator's required fields.

## Verdict and evidence
**Verdict: still-relevant.** Issue [#423](https://github.com/IronbellyOrg/IronClaude/issues/423) remains OPEN, in Backlog, with all 14 acceptance boxes unchecked when read on 2026-11-23. The requested proactive knowledge catalogue, relevance review and sharing of lessons across workspaces are not demonstrated by the existing read-only sweep.

The issue needs a scope correction, not closure: its 2026-11-17 status comment says v2 is not started, while recorded owner decisions narrow its delivery to reporting and replace the broad "#339 is complete" start gate with the sweep merge plus a shared live-data capture. These records are evidence of prior decisions, not authorization for this worker to edit the issue or begin v2 (`.dev/brainstorms/20261113-orchestrator-tui-alignment/owner-questions/owner-answers.md:258-259`).

Merged groundwork does not complete this feature: PR #539, commit `4d3c0b126151789bd0cb5b481b10f572a0c4e6b7`, adds the sweep; PR #579, commit `b46ecc1bd47ad817f8cd6181fde0b968dd3f24a0`, fixes its working-state classification. Local history contains both. PR #434, commit `6782eee10df3758107eb6fa08c166bf381ae1a24`, explicitly leaves v2 monitor work under #423.

## Real current state
- **Implemented source:** `/sc:sweep` has a protocol skill that invokes the sweep CLI once, reads its dated report and relays counts and a path (`src/superclaude/skills/sc-sweep-protocol/SKILL.md:15-29`). The underlying CLI collects observations, classifies them, renders a report and writes it (`src/superclaude/cli/sweep/commands.py:242-278`). This is an observation snapshot, not an ongoing cross-workspace knowledge service.
- **Existing operating rule:** the coordinator contract requires periodic sweep reads, but explicitly says Phase 1 adds a duty, not a scheduler, and person-started sessions are never messaged (`src/superclaude/core/WORKER-CONTRACT.md:288-290`). These are written rules, not a claim that a hook enforces them.
- **Start-gate evidence:** the shared capture findings exist and record real running-worker values; they explicitly close the capture required by the v2 start decision, except that a non-null agent-wait value was not observed (`.dev/brainstorms/20261113-orchestrator-tui-alignment/owner-questions/Q24/capture-findings-20261116.md:14-29`). The owner's sequencing decision does not require waiting for all of #339 or a code fix. PR #579 has nevertheless already supplied that fix.
- **Scope correction:** the accepted delivery decision is report-only. Reopening direct correction into non-worker sessions requires a delivery channel, a threat model for harmful content, an owner-approval rule and shared grant terms (`.dev/brainstorms/20261113-orchestrator-tui-alignment/owner-questions/open-decisions.md:206-218`). The issue still promises to "relay them to affected agents", so its body has not caught up.
- **Planning exists, delivery not established:** the orchestration/observer alignment package contains decisions about v2, so "no v2 planning anywhere" would be false. No issue-linked completed brainstorm/design handoff, dedicated outside-techniques research, v2 catalogue, cross-agent relevance evaluator or resulting course-correction demonstration was located in the reviewed sources. Off-checkout or unmerged work is UNVERIFIED.
- **Not a replacement:** issue intake landed through PRs #447 and #448. Intake of approved work is different from sharing knowledge among work already in progress.

## Concrete next steps
1. **Coordinator, after the owner's go:** correct the issue body to name the knowledge/reporting layer, replace "after all of #339" with the accepted sweep-merge plus capture gate, and replace automatic relay to non-worker sessions with report-only delivery and its reopening conditions. The correction itself remains a separately authorized GitHub action, not part of this review.
2. **Then obtain the requested design and research:** link the dedicated brainstorm/design handoff and outside-techniques memory/context research before implementation. In that work, define whether "all workspaces" means several local Runs or multiple hosts, the catalogue's minimum records and storage owner, safe report readers, relevance checks and examples of useful duplicate-work/lesson reports.
3. **Plan the smallest demonstrable delivery:** build timer/checkpoint ingestion and a durable catalogue plus report-only cross-agent reviews, with tests for stale observations, duplicate reports, untrusted session text and unauthorized delivery. Keep remote collection and non-worker message injection out unless explicitly approved. The architecture must retain the command/skill/agent split (`docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md:51-75`).

These are follow-up recommendations, not implementation performed or additional grants.

## Complexity and size
**Complexity: complex. Size: XL.** The feature spans cross-workspace data capture, durable knowledge records, relevance and duplicate-work evaluation, safe reporting boundaries, multiple execution systems and demonstrated end-to-end results. This estimates the feature as an umbrella, not the small issue-body correction or this review; a future design may reduce it.

## Priority
**Priority: P2.** Reducing duplicate work and sharing useful lessons matters at multi-workspace scale, but this is a separate future capability, not a demonstrated outage or security incident. No downstream issue was verified to require its completion to restore current operation; approved scope and research come before implementation.

## Dependencies
- **Needs #339's read-only sweep foundation, not all remaining v1 work:** supplied by merged #539 and the shared capture; #579 supplies the subsequent classification fix. The broader v1 issue remains OPEN, but its remaining resume/cleanup work is not the accepted start gate for this knowledge layer.
- **Needs the narrow #534 capture item:** recorded as satisfied by the capture findings, with non-null agent-wait data still UNVERIFIED. The rest of #534 remains separate; do not make its entire backlog a prerequisite.
- **Needs scope approval plus the brainstorm/design and dedicated research required by #423:** not verified complete. The existing answer record specifically does not authorize starting v2.
- **Conditional only:** multi-host collection or direct corrections would require further channel/trust decisions. The report-only scope does not require building a signed-grant or sub-orchestrator system first.
- **Blocks:** no explicit downstream issue dependency was verified. Shared source/schema coordination with #409 is related work, not a proven finish-to-start dependency.

## Related issues
- #339 (OPEN): v1 session supervision and read-only sweep foundation; preserve the separate knowledge-layer scope.
- #409 (OPEN): human-facing orchestration dashboard. It observes activity; #423 derives useful cross-agent knowledge. Shared source/schema decisions should not become two incompatible collectors.
- #331 (CLOSED): original approved-issue intake feature, delivered through #447 and #448.
- #450 (OPEN): rollout/live-test/shadow/cron follow-up for that watcher, mentioned in #423's first comment. Related intake work, not demonstrated v2 completion.
- #326 (OPEN): Git/PM workflow integration, listed by #423. Its detailed effect on a future knowledge-layer design is UNVERIFIED; it is not established as a blocker here.
- #431 (CLOSED): worker liveness, with contract groundwork in #434; that PR explicitly preserves v2 monitor work under #423.
- #534 (OPEN): sweep follow-ups, including the now-recorded capture.
- #444 (CLOSED): evaluation of sub-orchestrator/coordinator mode. Separate from the knowledge catalogue; closure does not establish that this feature shipped.

States came from live issue view/list reads. No issue was edited, commented on, labeled, linked or closed.

## Related PRs
| PR | Verified state | Relationship |
|---|---|---|
| #434 | MERGED, 2026-11-08, `6782eee10df3758107eb6fa08c166bf381ae1a24` | v1 worker-liveness rules; description explicitly leaves v2 monitor work in #423. |
| #447 | MERGED, 2026-11-08, `4c93b6c7397e91b680b0306e99f32835bc364611` | Issue-watch intake poller mentioned in #423's first comment. |
| #448 | MERGED, 2026-11-08, `ce660825856185aa043f65dad34128e1a238b720` | Intake poller safety follow-up mentioned in the same comment. |
| #539 | MERGED, 2026-11-14, `4d3c0b126151789bd0cb5b481b10f572a0c4e6b7` | Read-only sweep foundation and coordinator-loop rule. |
| #579 | MERGED, 2026-11-17, `b46ecc1bd47ad817f8cd6181fde0b968dd3f24a0` | Real-data correction to the sweep's working class. |
| #587 | MERGED, 2026-11-17, `d41d79a8ecec42ca51e18f50cf0bf9a7e6309f12` | Records orchestration/observer/watcher decisions, including the v2 sequencing and reporting boundary. |
| #588 | MERGED, 2026-11-17, `bc7b0b15ac2fb8b36908fb9f603465c2486fc127` | Corrections to the shared decision records. |
| #589 | MERGED, 2026-11-17, `fe14a11bd99b186d31b18a97a7a7487335e872b4` | Questions-read observation in the same decision record; not a v2 feature implementation. |

An all-state PR search for `423` returned #434 plus #414 and #736. The latter two matched unrelated uses of the number in their descriptions and are not evidence that #423 shipped. No PR implementing the knowledge catalogue was identified by that search.

## Verification limits and negative evidence
- **Issue history read:** full live issue body, both comments and current state/project metadata. Comment dates: 2026-11-08 and 2026-11-17. The first records watcher merges; the second records v2 not started, sweep groundwork merged and the scope rewrite awaiting a grant.
- **Timeline UNVERIFIED:** a complete GitHub event timeline (cross-references, label changes and all historical links) was not obtainable from the authorized issue/PR view/list surface. No API call, browser workaround or GitHub write was used. Therefore the related-PR list is not claimed exhaustive.
- **Static source verification:** the requested `/sc:analyze` skill was invoked at top level on `src/superclaude/skills/sc-sweep-protocol`; supporting reads traced the CLI and coordinator contract. Analysis: `.dev/issuecleanup/g1/423/analyze/analyze-report.md`. The protocol directory is one Markdown file; Codegraph does not index Markdown, so its empty target result was handled with native file reads. Generic graph caller results were ambiguous and not treated as evidence of no callers.
- **Negative searches:** the current sweep package had no matches for catalogue/catalog, knowledge, relevance or course-correction terms. Searches across source, planning folders and issue/PR references found alignment work, the shared capture and v1 sweep, not a demonstrated #423 feature delivery. The older `.dev/reviews/orchestrator-tui-alignment-20261113/04-issue-423-v2.md` was read as historical context only; its old claim that the working class is inert is superseded by #579, not repeated as current fact.
- **UNVERIFIED:** private or unmerged/off-checkout branches, the raw live capture contents, a non-null agent-wait sample, live operational behavior, future non-Claude execution-system support, implementation effort in hours, and completeness of the requested external memory/context research. No live sweep, test suite or external research was run. Historical PR test claims are not presented as tests run by this worker.
- **Tool recovery:** initial report population was refused by the freshness hook because a new file had not yet been explicitly Read; the required Read was performed and exact Edit calls then succeeded. No bypass or source edit was used.
- **Task boundary:** only this issue's report directory was written; no source, index, branch, GitHub state or other worker's report was changed. Report status is partial solely because the full event timeline is unverified; the evidence supports keeping the issue open without that missing history.

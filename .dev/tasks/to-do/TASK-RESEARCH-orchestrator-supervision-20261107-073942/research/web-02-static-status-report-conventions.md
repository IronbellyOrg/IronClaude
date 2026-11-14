# Web Research 02: Static status report conventions

**Topic:** conventions for static, point-in-time status reports read by a person (status pages, shift handover, age-ranked ordering, omission counts)
**Date:** 2026-11-07
**Status:** Complete
**Search backend:** WebSearch / WebFetch only. fallback_reason: tavily_missing (no mcp__tavily__* tools in this session).
**Provenance note:** the research agent had no file-writing tool and returned this content in its reply. The task executor saved it here unchanged (logged under Deviations in the task file).

## What we already know from the codebase
- #409 (`495eb96d`, unmerged) header: title + READ ONLY, owners/sessions/mapped-trees counts, then clock | msgs coverage | worker age | check age (`canvas.py:73-77`); the clock is hardcoded.
- The Attention Ledger shows each question's age, the question, requester/owner and affected IDs, under the panel "SEEN IS NOT RESOLVED" (`agent_focus.py:44-53`). "Age-ranked" is documented, but the code only partly sorts by age (GQ-29).
- The Shift Brief gives a count, an "not an all-clear" coverage line, one block per question, then failed/stale/frozen counts and an "Inspection only" line (`agent_focus.py:156-169`).
- The omission rule "Show omission counts when limited" (`DESIGN-CONTRACT.md:11`) is applied only in `listbox()` (`agent_focus.py:17`). The wide ledger and the Shift Brief break it (GQ-33).
- Phase 1 writes a dated static report with these classes: waiting on a person, working, stalled (proved), could not determine, finished, idle. Safe-to-close is a separate dimension. Phase 1 never acts on a session.

## Status pages: health and lifecycle are separate fields
- **Atlassian Statuspage**, component states: Operational / Under maintenance / Degraded performance / Partial outage / Major outage. https://support.atlassian.com/statuspage/docs/what-is-a-component (official). Relevance MEDIUM. Supports the #409 rule of keeping state dimensions independent.
  - WC-10 / read-only: Statuspage has no "unknown" component state, because a person sets every state. Our report is automated, so it needs the could-not-determine class that Statuspage lacks. This **extends** Statuspage.
- **Incident lifecycle** (Investigating / Identified / Monitoring / Resolved) is kept separate from component state, and impact is a third field. https://support.atlassian.com/statuspage/docs/what-is-statuspage/ ; https://support.atlassian.com/statuspage/docs/top-level-status-and-incident-impact-calculations (official). Relevance HIGH. Supports keeping safe-to-close as its own dimension (GQ-68), not a class.
  - WC-10 / read-only: each dimension can be unknown on its own. Read-only fits, because a status page only reports.

## Monitoring: "unknown" is a first-class state
- **Icinga 2**: UNKNOWN means "The check could not determine the service's state" (exit code 3). A plugin that hits its own timeout reports UNKNOWN, not CRITICAL. https://icinga.com/docs/icinga-2/latest/doc/03-monitoring-basics/ ; https://icinga.com/docs/icinga-2/latest/doc/05-service-monitoring/ (official). Relevance HIGH. Supports our "could not determine" class almost word for word.
  - WC-10 / read-only: the direct precedent for WC-10. A failed probe gives unknown, not dead. A Phase 1 probe timeout should map to could not determine.
- **Nagios**: the plugin return codes are 0 OK, 1 WARNING, 2 CRITICAL, 3 UNKNOWN. UNKNOWN covers internal failures that stop the check from running. https://assets.nagios.com/downloads/nagioscore/docs/nagioscore/4/en/pluginapi.html ; https://support.nagios.com/kb/article.php?id=72 (official). Relevance MEDIUM. Supports Icinga.
  - WC-10 / read-only: unknown is reported, never hidden.
- **Kubernetes**: Node `Ready=Unknown` means the controller "has not heard from the node" within `node-monitor-grace-period` (default 50 s). This differs from `False` (unhealthy), and each has its own taint (unreachable versus not-ready). https://kubernetes.io/docs/reference/node/node-status/ (official). Relevance HIGH.
  - WC-10 / read-only: silence gives Unknown, not False. This **supports** WC-10 and GQ-17 (a late heartbeat never proves stalled). Kubernetes then acts on Unknown with taints and eviction; Phase 1 must not copy that step.
- **Prometheus / Grafana**: ordinary alerts do not fire when no data arrives. Absence must be tested explicitly (`absent()`, `absent_over_time()`), and `up==0` (scrape failed) is a different signal from an absent series (target gone). Grafana: "Missing data isn't always a failure", and the No Data handling can be set to NoData / Alerting / Normal / Keep Last State. https://prometheus.io/docs/prometheus/3.16/querying/functions/ ; https://grafana.com/docs/grafana/latest/alerting/guides/missing-data/ ; https://grafana.com/docs/grafana-cloud/observe-and-act/connect-externally-hosted/data-sources/prometheus/alerting/ (official). Relevance HIGH.
  - WC-10 / read-only: **partly contradicts** our design. Grafana lets an operator map missing data to firing or to OK, and both are guesses that WC-10 forbids. Of Grafana's options only "NoData" (a distinct state) fits WC-10. Our codebase rule governs: absence always gives could not determine. Grafana also warns that an evicted series can look "resolved". In our terms, a session that disappears from a listing must not be reported as finished.

## Shift handover notes
- **Google SRE Workbook**: the outgoing on-call engineer "sends a handoff email to the next engineer on-call", and the incoming engineer reads it. Incident response keeps a shared live incident document and hands over command explicitly. https://sre.google/workbook/on-call/ ; https://sre.google/workbook/incident-response/ (official). Relevance MEDIUM. The workbook gives no field list for the email, so it supports the Shift Brief idea but not a layout.
  - WC-10 / read-only: a handover note is a read-only artifact by nature, so it fits Phase 1.
- **I-PASS** (clinical handover): Illness severity (stable / watcher / unstable), Patient summary, Action list (task, timeline, owner), Situation awareness and contingency ("if-then"), Synthesis by receiver. https://www.ahrq.gov/teamstepps-program/curriculum/communication/tools/ipass.html (official; WebFetch returned 403, content from the search excerpt) ; https://www.jointcommissionjournal.com/article/S1553-7250%2817%2930176-9/abstract (peer reviewed). Relevance HIGH.
  - WC-10 / read-only: "watcher" is a named in-between severity, the counterpart of reporting uncertainty instead of forcing stable or unstable. The action list with an owner matches the #409 owner and affected columns. The "if-then" contingency means the report can say what a person should check next without acting itself. "Synthesis by receiver" has no static equivalent; it **extends** the design and points to a person confirming the report.
- **GitLab / PagerDuty**: status updates carry a "Current Situation" and "Next status update expected by [time] UTC", and PagerDuty's status page has a "Time till Next Update" field. https://docs.pagerduty.com/ops-guides/incident-response-guide/incident-commander ; https://docs.pagerduty.com/incident-management/communicate/external-status-page (official) ; https://gitlab.com/gitlab-com/content-sites/handbook/-/blob/add-ai-tool-registry-design-doc/content/handbook/support/support-incident-response.md (maintained handbook, branch copy). Relevance MEDIUM.
  - WC-10 / read-only: a dated report should state when its data was observed. #409 hardcodes its clock (`canvas.py:73-77`), so the sweep must print the real observation time. A static report has no next-update time unless the sweep is scheduled (GQ-10, GQ-61).

## Oldest-first / age-ranked ordering
- **Kanban Work Item Age**: elapsed time from the start of an item to now, one of the four required flow metrics. Daily review starts with the oldest in-flight item and asks what is blocking it. https://kanbanguides.org/the-kanban-guide/2025.5/pdf/kanban-guide.v2025.5.en.pdf (official guide) ; https://prokanban.org/blog/visualizing-flow-metrics---where-to-begin ; https://prokanban.org/kpg (practitioner organisation). Relevance HIGH. Supports age-ranked ordering, which #409 documents but only partly codes (GQ-29).
  - WC-10 / read-only: age is computed from a known start time. When the start time is unknown, the row cannot be ranked honestly, so place it with an explicit "age: could not determine" instead of treating it as age 0. Ordering is a read-only presentation choice.

## Omission counts
- **GitHub CLI**: `gh issue list` prints "Showing 30 of 624 open issues in cli/cli". Users asked for the total in `--json` because it was missing there. https://github.blog/developer-skills/github/how-to-level-up-your-git-game-with-github-cli/ (official blog) ; https://github.com/cli/cli/issues/12196 (maintained repo). Relevance HIGH. Supports the #409 `shown/total` rule and shows that a machine-readable output also needs the total.
  - WC-10 / read-only: "shown/total" assumes the total is known. When a source truncates without a total (the 100-row `check` cap, GQ-48), the honest form is "at least N, listing truncated: could not determine the total". This **extends** #409, which has no form for an unknown total.

## Key External Findings
1. Mature monitoring systems (Icinga, Nagios, Kubernetes) all make "unknown / could not determine" a first-class state separate from failed, which directly supports WC-10.
2. Grafana lets missing data be mapped to firing or OK. That contradicts WC-10, and our codebase rule wins.
3. Status pages keep health, lifecycle and impact as independent fields, which supports safe-to-close as a separate dimension.
4. Handover conventions (SRE handoff email, I-PASS) stress owner, action list, an in-between "watcher" state and if-then contingencies. All of these fit a read-only brief.
5. Oldest-first ordering is standard practice (Kanban Work Item Age), and items with an unknown age need explicit placement.
6. "Shown of total" is a common CLI convention. No source found gives a form for an unknown total.

## Recommendations from External Research
- Print the real observation time in the header; #409 hardcodes its clock.
- Treat probe timeouts and missing sources as could not determine (Icinga precedent). Never map absence to finished or stalled.
- A row that drops out of a listing is not evidence of finished (Grafana eviction warning).
- Sort the attention items oldest first. Rows with an unknown age go in a labelled group, not at age 0.
- Every bounded list prints `shown/total`. A truncated source prints "at least N (truncated at 100), total could not determine".
- Optionally add a short if-then "what to check next" line per waiting item (I-PASS). It is text only and starts no action.
- Discrepancy note: no external source contradicts the verified #409 code. Grafana's configurable no-data mapping conflicts with WC-10 and is rejected.

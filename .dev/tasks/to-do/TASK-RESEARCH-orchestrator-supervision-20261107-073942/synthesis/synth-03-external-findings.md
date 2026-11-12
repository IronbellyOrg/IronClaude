## 5. External Research Findings

**Precedence:** codebase findings take precedence. Everything in this section is external context: patterns from other systems, each tied to its URL. None of it describes the current architecture of this repo. Where an external pattern conflicts with a verified codebase rule (WC-10 at `src/superclaude/core/WORKER-CONTRACT.md:45`, the stall-proof rule in `research-notes.md` Section C rule 2, `orca-capabilities.md:125`), the codebase rule wins and the conflict is recorded in 5.9.

**Inputs:** `research/web-01-agent-supervisor-session-health.md` (web-01) and `research/web-02-static-status-report-conventions.md` (web-02). Tavily was not available for either; both used WebSearch and WebFetch. web-02 was saved by the task executor from its agent's reply (provenance note in that file).

**Research question context:** Orchestrator mode Phase 1 for issue #339: a read-only, coordinator-only `/sc:sweep` that classifies sessions (waiting on a person, working, stalled (proved), could not determine, finished, idle: the research question's six; Section C adds fenced as a seventh class, `research/research-notes.md:188`, and six versus seven is an open question, Section 9; safe-to-close is a separate dimension) over a default 6 h window that bounds activity only, writes a dated static report on the #409 layout, and adds a WC-14 coordinator-loop rule to `src/superclaude/core/WORKER-CONTRACT.md`; `/sc:close`, resume, the trust layer, an orchestrator of orchestrators and the management-server relay are later phases, recorded only.

**How to read each finding:** "Relationship" says whether the external pattern supports, extends or contradicts what the codebase already does. "WC-10 / read-only" says whether the pattern fits WC-10 (act only on Orca's stall proofs, never on a late heartbeat) and whether Phase 1 can use it without acting on a session. Anything that restarts, kills, evicts, retries or aborts is later-phase only.

### 5.1 Supervisors act on an observed exit, not on silence (Erlang/OTP)

- **[EXTERNAL] Finding:** every OTP restart strategy (`one_for_one`, `one_for_all`, `rest_for_one`) fires only when a child "terminates", learned through a link/exit signal, which is positive evidence. OTP has no "restart because the child was quiet".
  - Source: https://www.erlang.org/doc/system/sup_princ.html
  - Relevance: HIGH
  - Relationship: supports the stall-proof rule (only `exited` liveness or an observed process exit counts).
  - WC-10 / read-only: WC-10 consistent. The restart itself is later-phase only; Phase 1 may only label the row "stalled (proved)".
- **[EXTERNAL] Finding:** restart types split normal finish from abnormal exit: `permanent` always restarts, `transient` only after an abnormal exit (`normal`, `shutdown` and `{shutdown, Term}` do not qualify), `temporary` never.
  - Source: https://www.erlang.org/doc/system/sup_princ.html
  - Relevance: HIGH
  - Relationship: extends. It gives a vocabulary for finished (a `normal` exit: Orca `outcome` settled plus a read return contract) versus stalled (`exited` with no `worker_done`), and for why a `consumer_fenced` dispatch is an intended stop like `{shutdown, Term}`, never a failure (WC-12, `WORKER-CONTRACT.md:60`, as cited by web-01).
  - WC-10 / read-only: WC-10 consistent. Phase 1 uses only the classification half; restart policy is later-phase only.
- **[EXTERNAL] Finding:** restart intensity bounds automated recovery (`intensity` restarts per `period`, default 1 per 5 s); past it the supervisor stops its children, exits with `shutdown`, and "its parent then decides".
  - Source: https://www.erlang.org/doc/system/sup_princ.html
  - Relevance: MEDIUM
  - Relationship: extends. The repo has no retry budget. For a later phase it argues that any automatic retry needs a bound and an escalation to the person (gap G5, GQ-08).
  - WC-10 / read-only: retry on absence is forbidden by WC-10 and is an action, so later-phase only. Phase 1 can at most report "repeated stalls" as a fact.
- **[EXTERNAL] Finding:** shutdown is graceful first: send `shutdown`, wait, then `kill` after the timeout; `brutal_kill` skips cleanup; supervisors default to `infinity`.
  - Source: https://www.erlang.org/doc/system/sup_princ.html
  - Relevance: LOW for Phase 1
  - Relationship: extends. Parallels the safe-to-close REVIEW dimension (terminal releasable only after the result is read; worktree removable only when the five refusal conditions at `WORKER-CONTRACT.md:108` are false, as cited by web-01).
  - WC-10 / read-only: shutdown and kill are actions, later-phase only. Phase 1 prints the REVIEW line and never runs it.

### 5.2 Separate probes answer separate questions (Kubernetes liveness, readiness, startup)

- **[EXTERNAL] Finding:** liveness probes decide when to restart a container; readiness probes decide when it may take traffic, and a readiness failure "does not trigger a container restart"; startup probes hold off the other two until the app has started.
  - Source: https://kubernetes.io/docs/concepts/configuration/liveness-readiness-startup-probes/ (WebFetch read the first 100000 of 118034 characters)
  - Relevance: HIGH
  - Relationship: supports the sweep's separate dimensions: liveness verdict (`live` / `unverifiable` / `exited`), waiting on a person (closest to readiness: alive but not taking new work), and terminal state, "reported separately from Task status" (`worker-list --help` line 19, as cited by web-01). Supports "waiting on a person is healthy, not failed".
  - WC-10 / read-only: the readiness idea (report, do not restart) fits Phase 1. The liveness restart is later-phase only. Kubernetes probes call into the container; the sweep must not probe the agent's terminal (GQ-51 excludes `--agent-wait`), so Phase 1 reads Orca's recorded state only.
- **[EXTERNAL] Finding:** "Incorrect implementation of liveness probes can lead to cascading failures"; liveness should catch unrecoverable failure, "not merely temporary overload or an unavailable dependency".
  - Source: https://kubernetes.io/docs/concepts/configuration/liveness-readiness-startup-probes/
  - Relevance: HIGH
  - Relationship: supports WC-10 directly. A long tool call, a model wait or an unreachable remote host (`host_unavailable`, `orca-capabilities.md:124`, as cited by web-01) is overload or an unavailable dependency, not death.
  - WC-10 / read-only: WC-10 consistent. External justification for reporting `unverifiable` as "could not determine".
- **[EXTERNAL] Finding:** liveness probes do not wait for readiness; slow starters need a startup probe or `initialDelaySeconds`.
  - Source: https://kubernetes.io/docs/concepts/configuration/liveness-readiness-startup-probes/
  - Relevance: MEDIUM
  - Relationship: extends. A just-dispatched worker with no heartbeat yet is the startup case; nearest repo equivalents are Orca's `restored_unconfirmed` and a failed start reported `reclaimable` (`orca-capabilities.md:112`, UNVERIFIED, as cited by web-01). The sweep should not read "no activity yet" on a new dispatch as idle or stalled.
  - WC-10 / read-only: WC-10 consistent (no signal during startup is absence). A grace period changes only the label, never an action.
- **[EXTERNAL] Finding:** a process can pass a liveness probe while its work loop is hung, unless the probe exercises that loop ("running but cannot make progress").
  - Source: https://kubernetes.io/docs/concepts/configuration/liveness-readiness-startup-probes/
  - Relevance: MEDIUM
  - Relationship: supports. The repo already says PTY `observation.status` "is PTY liveness only. A live terminal can still hold a dead or stuck agent" (`orca-capabilities.md:123`, as cited by web-01). The codebase is stricter: no PTY signal counts as stall proof either way.
  - WC-10 / read-only: WC-10 consistent. Phase 1 shows PTY status as context only.

### 5.3 Suspicion is a scale, and a suspected node can come back (phi-accrual failure detection)

- **[EXTERNAL] Finding:** accrual failure detectors "output a suspicion level on a continuous scale" instead of trust versus suspect, and keep monitoring separate from the application's decision of what to do.
  - Source: https://dspace.jaist.ac.jp/dspace/bitstream/10119/4784/1/IS-RR-2004-010.pdf (Hayashibara et al., abstract via search result; PDF not fetched in full)
  - Relevance: HIGH
  - Relationship: extends. The monitor-reports / application-decides split matches Phase 1 (sweep reports, person decides). Orca's verdict is categorical, not a scale; a heartbeat-age column could be shown as context.
  - WC-10 / read-only: a phi value measures absence only, so under WC-10 it can never make a row "stalled"; at most it ranks rows inside "could not determine". Computing it is a pure read, but Orca exposes no heartbeat history (GQ-17 open), so it is not buildable now.
- **[EXTERNAL] Finding:** `phi(t) = log10(1 / (1 - F(t)))` with F a normal CDF fitted to past heartbeat gaps; default threshold 8; a lower threshold detects sooner with more false alarms; `acceptable-heartbeat-pause` adds tolerance for GC stalls and network interruptions.
  - Source: https://nightlies.apache.org/pekko/docs/pekko/1.1.3/docs/typed/failure-detector.html ; https://nightlies.apache.org/pekko/docs/pekko/1.1.3/japi/org/apache/pekko/remote/PhiAccrualFailureDetector.html (API page from search result only)
  - Relevance: MEDIUM
  - Relationship: supports WC-10. Agent heartbeat gaps are very irregular (long tool calls, model latency, a person reading a prompt), which is the regime where any fixed threshold mislabels healthy sessions.
  - WC-10 / read-only: a threshold crossing is a suspicion, which WC-10 forbids acting on. Any phi-triggered action is later-phase only and still needs Orca's stall proof.
- **[EXTERNAL] Finding:** phi is a timing estimate, not certainty of a crash; a node marked unreachable "may subsequently become reachable again" (paraphrase in web-01 of the fetched page).
  - Source: https://nightlies.apache.org/pekko/docs/pekko/1.1.3/docs/typed/failure-detector.html
  - Relevance: HIGH
  - Relationship: supports, no discrepancy. Same as "contact loss is not process death" (`orca-capabilities.md:122`) and "Absence never authorizes stop, abandon, retry, or release" (`orca-capabilities.md:125`), as cited by web-01.
  - WC-10 / read-only: a direct external statement of WC-10. Phase 1 reports "could not determine", never "stalled", for any suspicion-only row.

### 5.4 "Unknown" is a first-class health state (Kubernetes node status, gRPC, Icinga, Nagios, Prometheus / Grafana)

- **[EXTERNAL] Finding:** Kubernetes node `Ready` is `True` (healthy), `False` (not healthy) or `Unknown` ("the node controller has not heard from the node in the last `node-monitor-grace-period`", default 50 s). Heartbeats are Node `.status` updates and Lease renewals every 10 s. `Unknown` and `False` carry different taints (unreachable versus not-ready).
  - Source: https://kubernetes.io/docs/reference/node/node-status/ (both web-01 and web-02 cite it)
  - Relevance: HIGH
  - Relationship: supports "could not determine" as its own class. The split maps onto Orca's verdicts: `True` ~ `live`, `Unknown` ~ `unverifiable`, `False` ~ a positive failure report (`exited` / observed exit). Supports GQ-17 (a late heartbeat never proves stalled).
  - WC-10 / read-only: WC-10 consistent at the status layer. Kubernetes then acts on `Unknown` (taint, then eviction after a 300 s toleration, per https://kubernetes.io/docs/concepts/scheduling-eviction/taint-and-toleration/, search result only); that step is what WC-10 forbids and Phase 1 must not copy (5.9, D1). Data note: the same page also says "40 second default timeout for unreachable nodes", so it is internally inconsistent on the default.
- **[EXTERNAL] Finding:** gRPC health `ServingStatus` is `UNKNOWN = 0`, `SERVING = 1`, `NOT_SERVING = 2`, `SERVICE_UNKNOWN = 3` (Watch only). `Check` on an unregistered service fails with `NOT_FOUND`; `Watch` returns `SERVICE_UNKNOWN` and waits.
  - Source: https://github.com/grpc/grpc-proto/blob/master/grpc/health/v1/health.proto ; https://grpc.io/docs/guides/health-checking/ (guide from search result only)
  - Relevance: MEDIUM
  - Relationship: extends. Two kinds of unknown: "health not known yet" versus "no such subject". The sweep has the same pair: a row that exists with evidence absent (`unverifiable`, absent-versus-null `agentWait`, GQ-58) versus a source that could not be read at all (the `unscanned:` markers, `research/scope-02-orca-recovery.md:239`, as cited by web-01). Keep the two apart in the report.
  - WC-10 / read-only: WC-10 consistent (UNKNOWN is the default, never NOT_SERVING). `Check` and `Watch` are probes; only the vocabulary carries over.
- **[EXTERNAL] Finding:** Icinga 2 UNKNOWN means "The check could not determine the service's state" (exit code 3); a plugin that hits its own timeout reports UNKNOWN, not CRITICAL.
  - Source: https://icinga.com/docs/icinga-2/latest/doc/03-monitoring-basics/ ; https://icinga.com/docs/icinga-2/latest/doc/05-service-monitoring/
  - Relevance: HIGH
  - Relationship: supports the "could not determine" class almost word for word.
  - WC-10 / read-only: the direct monitoring precedent for WC-10. A Phase 1 read timeout maps to "could not determine".
- **[EXTERNAL] Finding:** Nagios plugin return codes are 0 OK, 1 WARNING, 2 CRITICAL, 3 UNKNOWN; UNKNOWN is for invalid arguments or an internal failure that stopped the check from running. The Nagios support KB says DNS lookup failures and socket timeouts "should generally NOT be reported as UNKNOWN states" (it does not say which code instead).
  - Source: https://assets.nagios.com/downloads/nagioscore/docs/nagioscore/4/en/pluginapi.html ; https://nagios-plugins.org/doc/guidelines.html ; https://support.nagios.com/kb/article.php?id=72
  - Relevance: MEDIUM
  - Relationship: the return-code scheme supports an explicit unknown; the KB timeout guidance partly contradicts the codebase, which treats contact loss (`host_unavailable`, `stale_status`) as `unverifiable`, reported "could not determine". The codebase wins (WC-10; `orca-capabilities.md:125`). The domains differ: a Nagios timeout on a network service is a user-visible outage, a late agent heartbeat says nothing about useful work. It also conflicts with the Icinga timeout rule above (5.9, C1).
  - WC-10 / read-only: timeout-as-failure is not adopted. What carries over: when the sweep's own read fails (Orca not running, a page that will not load), report it as a sweep failure, separate from a row's "could not determine".
- **[EXTERNAL] Finding:** Prometheus alerts do not fire on missing data; absence must be tested explicitly (`absent()`, `absent_over_time()`), and `up==0` (scrape failed) differs from an absent series (target gone). Grafana: "Missing data isn't always a failure"; No Data handling can be set to NoData, Alerting, Normal or Keep Last State. An evicted series can look "resolved".
  - Source: https://prometheus.io/docs/prometheus/3.16/querying/functions/ ; https://grafana.com/docs/grafana/latest/alerting/guides/missing-data/ ; https://grafana.com/docs/grafana-cloud/observe-and-act/connect-externally-hosted/data-sources/prometheus/alerting/
  - Relevance: HIGH
  - Relationship: partly contradicts. Mapping missing data to Alerting or Normal is a guess WC-10 forbids; only Grafana's NoData (a distinct state) fits. The codebase rule governs: absence always gives "could not determine". The eviction warning extends the design: a session that drops out of a listing must not be reported as finished.
  - WC-10 / read-only: only the NoData option is WC-10 compatible. Read-only fit: yes (detection and labelling only).

### 5.5 Patterns from LLM agent session tools (Harmonograf, Camunda, unfetched product docs)

- **[EXTERNAL] Finding:** Harmonograf heartbeats carry a `progress_counter`; an unchanged nonzero counter across `STUCK_THRESHOLD` consecutive heartbeats on a running invocation is flagged, with a UI alert only and no restart. The ADR says "Stuck detection is a heuristic" and "Heartbeat can itself hang", and children's progress can mask a blocked parent.
  - Source: https://github.com/pedapudi/harmonograf/blob/main/docs/adr/0018-heartbeat-stuck-detection.md
  - Relevance: HIGH
  - Relationship: supports that a liveness heartbeat says nothing about progress ("proves liveness, not completion", `orca-capabilities.md:130`, as cited by web-01) and that even a progress flag is only a suspicion. Contradicts in naming: Harmonograf calls the flagged state "stuck", which the sweep must not equate with "stalled" (5.9, D3). The parent/child masking matches GQ-40 (nested workers).
  - WC-10 / read-only: WC-10 consistent only when labelled a suspicion (a note on a "working" or "could not determine" row). Alert-only fits Phase 1, but Orca exposes no progress counter today, so not buildable in Phase 1.
- **[EXTERNAL] Finding:** Camunda splits agent time into "Thinking", "Tool calling" and "Idle" (paused for outside input); execution duration excludes input-waiting time; "No single health indicator proves that an agent is stuck." At the limit an error is raised that an error boundary can route to a person.
  - Source: https://docs.camunda.io/docs/next/components/agentic-orchestration/evaluate-agents/detect-off-rail-agents/
  - Relevance: HIGH
  - Relationship: supports "waiting on a person is healthy" (`worker-show --help` line 16; Section C rule 4, as cited by web-01) and the owner note at GQ-61 that the 6 h window bounds activity only.
  - WC-10 / read-only: WC-10 consistent. The limit error and routing are actions, later-phase only. Phase 1 keeps person-wait time out of activity ages and the 6 h activity window; the waiting-on-a-person list prints the time since the wait began (R4).
- **[EXTERNAL] Finding (context only):** Simple Agent Manager separates "Needs input", provider-limit waits and stuck work; agents-fleet describes a coordinator watchdog with a stall notice and automatic abort.
  - Source: https://www.simple-agent-manager.org/docs/guides/session-troubleshooting/ ; https://docs.agents-fleet.ai/advanced/coordinator-resilience (search results only, not fetched)
  - Relevance: LOW
  - Relationship: the input-wait split supports the Camunda finding above; the automatic abort contradicts WC-10.
  - WC-10 / read-only: automatic abort is an action on suspicion, rejected for Phase 1 and not adopted later without Orca's stall proof. Not used as evidence for any design decision.

### 5.6 Status pages keep health, lifecycle and impact as separate fields (Atlassian Statuspage)

- **[EXTERNAL] Finding:** Statuspage component states are Operational, Under maintenance, Degraded performance, Partial outage and Major outage. There is no "unknown" component state, because a person sets every state.
  - Source: https://support.atlassian.com/statuspage/docs/what-is-a-component
  - Relevance: MEDIUM
  - Relationship: supports the #409 rule of keeping state dimensions independent; extends Statuspage, because an automated report needs the "could not determine" class that a person-set page lacks.
  - WC-10 / read-only: WC-10 consistent once "could not determine" is added. Read-only fit: yes.
- **[EXTERNAL] Finding:** incident lifecycle (Investigating, Identified, Monitoring, Resolved) is a field separate from component state, and impact is a third field.
  - Source: https://support.atlassian.com/statuspage/docs/what-is-statuspage/ ; https://support.atlassian.com/statuspage/docs/top-level-status-and-incident-impact-calculations
  - Relevance: HIGH
  - Relationship: supports keeping safe-to-close as its own dimension (GQ-68), not a class.
  - WC-10 / read-only: each dimension can be unknown on its own. A status page only reports, so it fits read-only.

### 5.7 Shift handover conventions (Google SRE, I-PASS, GitLab / PagerDuty)

- **[EXTERNAL] Finding:** the outgoing on-call engineer "sends a handoff email to the next engineer on-call"; incident response keeps a shared live incident document and hands over command explicitly. The workbook gives no field list for the email.
  - Source: https://sre.google/workbook/on-call/ ; https://sre.google/workbook/incident-response/
  - Relevance: MEDIUM
  - Relationship: supports the Shift Brief idea (`agent_focus.py:156-169`, as cited by web-02) but gives no layout.
  - WC-10 / read-only: a handover note is read-only by nature; fits Phase 1.
- **[EXTERNAL] Finding:** I-PASS clinical handover: Illness severity (stable / watcher / unstable), Patient summary, Action list (task, timeline, owner), Situation awareness and contingency ("if-then"), Synthesis by receiver.
  - Source: https://www.ahrq.gov/teamstepps-program/curriculum/communication/tools/ipass.html (WebFetch returned 403; content from the search excerpt) ; https://www.jointcommissionjournal.com/article/S1553-7250%2817%2930176-9/abstract
  - Relevance: HIGH
  - Relationship: supports and extends. "Watcher" is a named in-between severity, the counterpart of reporting uncertainty instead of forcing stable or unstable. The owner-bearing action list matches the #409 owner and affected columns. "If-then" lets the report say what a person should check next. "Synthesis by receiver" has no static equivalent and points to a person confirming the report.
  - WC-10 / read-only: an if-then line is text only and starts no action, so it fits Phase 1.
- **[EXTERNAL] Finding:** GitLab and PagerDuty status updates carry a "Current Situation" and "Next status update expected by [time] UTC"; PagerDuty's status page has a "Time till Next Update" field.
  - Source: https://docs.pagerduty.com/ops-guides/incident-response-guide/incident-commander ; https://docs.pagerduty.com/incident-management/communicate/external-status-page ; https://gitlab.com/gitlab-com/content-sites/handbook/-/blob/add-ai-tool-registry-design-doc/content/handbook/support/support-incident-response.md (handbook branch copy)
  - Relevance: MEDIUM
  - Relationship: extends. A dated report should state when its data was observed; #409 hardcodes its clock (`canvas.py:73-77`, as cited by web-02), so the sweep must print the real observation time. A static report has no next-update time unless the sweep is scheduled (GQ-10, GQ-61).
  - WC-10 / read-only: fits Phase 1; printing a time is presentation only.

### 5.8 Ordering and omission counts (Kanban Work Item Age, GitHub CLI)

- **[EXTERNAL] Finding:** Kanban Work Item Age (elapsed time from an item's start to now) is one of the four required flow metrics; daily review starts with the oldest in-flight item and asks what blocks it.
  - Source: https://kanbanguides.org/the-kanban-guide/2025.5/pdf/kanban-guide.v2025.5.en.pdf ; https://prokanban.org/blog/visualizing-flow-metrics---where-to-begin ; https://prokanban.org/kpg
  - Relevance: HIGH
  - Relationship: supports age-ranked ordering, which #409 documents but only partly codes (GQ-29). Extends it: a row with an unknown start time cannot be ranked honestly and goes in a labelled "age: could not determine" group, not at age 0.
  - WC-10 / read-only: ordering is presentation only; fits Phase 1.
- **[EXTERNAL] Finding:** `gh issue list` prints "Showing 30 of 624 open issues in cli/cli"; users asked for the total in `--json` because it was missing there.
  - Source: https://github.blog/developer-skills/github/how-to-level-up-your-git-game-with-github-cli/ ; https://github.com/cli/cli/issues/12196
  - Relevance: HIGH
  - Relationship: supports the #409 `shown/total` rule (`DESIGN-CONTRACT.md:11`, applied only in `listbox()`, GQ-33, as cited by web-02) and shows machine-readable output needs the total too. Extends #409: when a source truncates without a total (the 100-row `check` cap, GQ-48), the honest form is "at least N, listing truncated: could not determine the total". No source found gives a form for an unknown total.
  - WC-10 / read-only: an unknown total is reported, not guessed; fits Phase 1.

### 5.9 Contradictions and rejected external patterns (codebase wins)

| # | External pattern | Source | Codebase rule | Outcome |
|---|---|---|---|---|
| D1 | Kubernetes taints and evicts after a node stays `Unknown` past its toleration (5.4) | https://kubernetes.io/docs/concepts/scheduling-eviction/taint-and-toleration/ | WC-10: absence never authorizes stop, retry or release (`WORKER-CONTRACT.md:45`; `orca-capabilities.md:125`) | Rejected for workers; recorded as a pattern the repo deliberately does not follow |
| D2 | Nagios KB: timeouts and DNS failures "should generally NOT be reported as UNKNOWN" (5.4) | https://support.nagios.com/kb/article.php?id=72 | Contact loss is `unverifiable`, reported "could not determine" | Codebase wins; domain differs (service outage versus agent progress) |
| D3 | Harmonograf labels a progress-free run "stuck" (5.5) | https://github.com/pedapudi/harmonograf/blob/main/docs/adr/0018-heartbeat-stuck-detection.md | "stalled" needs positive stop proof (Section C rule 2) | Shown as a note, never as the stalled class |
| D4 | Kubernetes liveness probe restarts on probe failure (5.2) | https://kubernetes.io/docs/concepts/configuration/liveness-readiness-startup-probes/ | Phase 1 never acts and never probes the agent's terminal (GQ-51) | Later phase only, and only with Orca's stall proof |
| D5 | Grafana No Data handling can map missing data to Alerting or Normal (5.4) | https://grafana.com/docs/grafana/latest/alerting/guides/missing-data/ | Absence always gives "could not determine" | Only the NoData option is compatible; Alerting / Normal / Keep Last State rejected |
| D6 | agents-fleet coordinator watchdog auto-aborts on stall (5.5) | https://docs.agents-fleet.ai/advanced/coordinator-resilience | WC-10; Phase 1 is read-only | Rejected; unfetched source, context only |

**Contradictions between external sources:**

| # | Conflict | Sources | Resolution for the sweep |
|---|---|---|---|
| C1 | Icinga reports a plugin's own timeout as UNKNOWN (web-02); the Nagios KB says socket timeouts should generally not be UNKNOWN (web-01) | https://icinga.com/docs/icinga-2/latest/doc/05-service-monitoring/ ; https://support.nagios.com/kb/article.php?id=72 | Follow Icinga, because it matches WC-10: a read timeout is "could not determine" |
| C2 | The Kubernetes node-status page gives 50 s (`node-monitor-grace-period`) and also "40 second default timeout for unreachable nodes" | https://kubernetes.io/docs/reference/node/node-status/ | No effect: the sweep copies no timeout value from Kubernetes |

**Agreement across sources:** four external patterns contradict WC-10 and are rejected (codebase wins): Grafana's missing-data mapping (5.4, D5), the agents-fleet auto-abort (5.5, D6), Kubernetes taint and eviction after `Unknown` (5.4, D1), and, in part, the Nagios KB timeout guidance (5.4, D2). Harmonograf's "stuck" label (D3) and the liveness-probe restart (D4) are rejected as actions or naming, not as contradictions of absence-is-not-death. The remaining sources support WC-10's core claim: Kubernetes probe guidance (5.2), Pekko (5.3), Kubernetes node status at the status layer and Icinga (5.4) state it independently. No external source contradicts the verified #409 code (web-02).

**Rejected option A4 (extend sc-crash-recovery):** [CODE-CONTRADICTED] by codebase research. Neither web file evaluates it, and no external finding gives a reason to reopen it. It stays a rejected option.

### 5.10 External Research Summary

**Coverage of each file's Key External Findings:**

| File | Key External Finding | Reflected in |
|---|---|---|
| web-01 | 1. Supervisors act on positive exit evidence, not silence (OTP, Pekko, Kubernetes liveness warning) | 5.1, 5.2, 5.3 |
| web-01 | 2. "Unknown" is first-class in Kubernetes node status and gRPC health | 5.4 |
| web-01 | 3. Health has independent dimensions (liveness, readiness, startup) | 5.2 |
| web-01 | 4. Waiting for outside input is healthy and excluded from time budgets (Camunda) | 5.5 |
| web-01 | 5. Progress beats presence as a stuck signal, but is still a heuristic (Harmonograf, phi) | 5.3, 5.5 |
| web-01 | 6. Two kinds of unknown: health not known versus subject not known / check could not run | 5.4 |
| web-01 | 7. Every action-taking pattern is later-phase only; Phase 1 takes vocabulary and the report-not-act stance | 5.1-5.5, 5.9 |
| web-02 | 1. Icinga, Nagios, Kubernetes make "unknown" first-class, supporting WC-10 | 5.4 |
| web-02 | 2. Grafana's missing-data mapping contradicts WC-10; codebase wins | 5.4, 5.9 (D5) |
| web-02 | 3. Status pages keep health, lifecycle and impact separate, supporting safe-to-close as a dimension | 5.6 |
| web-02 | 4. Handover conventions (SRE, I-PASS): owner, action list, "watcher" state, if-then | 5.7 |
| web-02 | 5. Oldest-first ordering (Kanban Work Item Age); unknown ages need explicit placement | 5.8 |
| web-02 | 6. "Shown of total" is a CLI convention; no source gives a form for an unknown total | 5.8 |

No Key External Finding was excluded.

**Actionable statements for Phase 1 (all read-only, all WC-10 compliant):**

| # | Statement | Basis |
|---|---|---|
| R1 | Keep "could not determine" as an explicit class, and split its cause: (a) a row exists but evidence is absent (`unverifiable`, null-versus-absent `agentWait`); (b) the sweep could not read a source (Orca down, page failed, `unscanned:`), reported as a sweep failure | 5.4 (gRPC, Nagios, Icinga) |
| R2 | Tie "stalled" to positive proof only (`exited`, observed exit, proved-final transcript turn without `worker_done`); show heartbeat age or any progress heuristic as a note column, never a class | 5.1, 5.3, 5.5 |
| R3 | Report a just-dispatched worker with no signal yet as "working" or "could not determine", never idle or stalled | 5.2 (startup probes) |
| R4 | Exclude person-wait time from activity ages and from the 6 h activity window. The waiting-on-a-person list is the exception: it prints and sorts on the question's original age, the time since the wait began (#409 keeps "original age" as a retained fact, `scope-04:87`) | 5.5 (Camunda); `scope-04:87` |
| R5 | Treat a read timeout or missing source as "could not determine"; never map absence to finished or stalled; a row that drops out of a listing is not evidence of finished | 5.4 (Icinga, Grafana) |
| R6 | Print the real observation time in the report header (#409 hardcodes its clock) | 5.7 (PagerDuty / GitLab) |
| R7 | Sort attention items oldest first by the time since the wait began (R4); rows with an unknown age go in a labelled group, not at age 0 | 5.8 (Kanban) |
| R8 | Every bounded list prints `shown/total`; a truncated source prints "at least N (truncated at 100), total could not determine" | 5.8 (GitHub CLI) |
| R9 | Optional: one if-then "what to check next" text line per waiting item, starting no action | 5.7 (I-PASS) |

**Not for Phase 1:**

| # | Statement | Basis |
|---|---|---|
| L1 | If automatic recovery is ever added, bound it OTP-style (restart budget per period, then escalate to the person) and gate every action on Orca's stall proof, never on `unverifiable` or a late heartbeat | 5.1, 5.2, 5.9 (D1) |
| L2 | Do not compute phi-accrual or progress-counter scores: Orca exposes no heartbeat history or progress counter (GQ-17 open), and the score could only rank suspicion | 5.3, 5.5 |

**Source reliability note:** most sources are official docs fetched with WebFetch. Fetched only partly or not at all: the Kubernetes probe page (first 100000 of 118034 characters), the phi-accrual paper (abstract only), the Pekko API page, the gRPC guide and the Kubernetes taint page (search results only), the AHRQ I-PASS page (403; search excerpt), and the two LOW product-doc sources in 5.5.

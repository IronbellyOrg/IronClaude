# Web Research 01: Supervisor and health-check patterns for long-running agent sessions

**Topic:** Erlang/OTP supervisors and restart strategies, Kubernetes liveness / readiness / startup probes, phi-accrual failure detection, and "unknown" as an explicit health state, mapped onto orchestrator mode Phase 1 (#339).
**Task:** TASK-RESEARCH-orchestrator-supervision-20261107-073942 (checklist item 192, Phase 4)
**Date:** 2026-11-07
**Status:** Complete

**Web tool note:** `[WEB_RESEARCH_FALLBACK: tavily=tool not loaded in this session (mcp__tavily__tavily_search / tavily_extract not available); used=WebSearch+WebFetch]`. Every finding below came from WebSearch or WebFetch.

**Source of truth:** the codebase. External findings add context and options; they never override verified code behaviour. Discrepancies are noted explicitly.

---

## What we already know from the codebase

- WC-10 (`src/superclaude/core/WORKER-CONTRACT.md:45`, CODE-VERIFIED per `research/scope-02-orca-recovery.md:90`): the coordinator "never stops, retries or releases a worker because a heartbeat is late, and it acts only on Orca's stall proofs". A late heartbeat is absence, not death.
- Orca's fleet liveness verdict has three values: `live`, `unverifiable`, `exited` (`orca-capabilities.md:122`, UNVERIFIED guide text; only `live` has been captured, GQ-37). "Contact loss is not process death."
- `unverifiable` is always absence (`missing_status`, `stale_status`, `restored_unconfirmed`, remote with no connection) and "never authorizes stop, abandon, retry, or release" (`orca-capabilities.md:125`). The sweep reports it as "could not determine".
- PTY liveness (`observation.status`) is not agent liveness: "A live terminal can still hold a dead or stuck agent" (`orca-capabilities.md:123`). Heartbeat "proves liveness, not completion" (`:130`); whether heartbeat age feeds the verdict is open (GQ-17).
- Stall proof needs positive evidence: `exited` liveness, an observed process exit, or a transcript whose final turn is proved final and sent no `worker_done`; a `consumer_fenced` dispatch is "fenced", never stalled (`research-notes.md` Section C rule 2; GQ-70, GQ-84).
- A worker waiting on a person (non-null `agentWait`, WC-4/WC-5 `blocked_question`) is healthy, not failed (`worker-show --help` line 16).
- Phase 1 is a read-only, coordinator-only `/sc:sweep`: classes waiting on a person, working, stalled (proved), could not determine, finished, idle; safe-to-close is a separate REVIEW-only dimension; 6 h activity window (GQ-61 still open); it never acts on a session.

---

## Area 1: Erlang/OTP supervisors and restart strategies

**Source:** https://www.erlang.org/doc/system/sup_princ.html (official docs; reliability HIGH)

### F1.1 Supervisors react to an observed exit, not to silence

- Key information: every restart strategy is triggered by a child that "terminates": `one_for_one` "If a child process terminates, only that process is restarted"; `one_for_all` and `rest_for_one` stop and restart siblings after a child's exit. The supervisor learns of the exit through a link/exit signal, i.e. positive evidence, not a timeout.
- Relation to codebase: matches the stall-proof rule (Section C rule 2): only `exited` liveness or an observed process exit counts. OTP has no notion of "restart because the child was quiet". Supports.
- Relevance: HIGH.
- WC-10 / read-only mapping: WC-10 consistent (an exit signal is positive proof; absence of messages never triggers a restart). The restart action itself is later-phase only; Phase 1 may only report "stalled (proved)".

### F1.2 Restart types separate "normal finish" from "abnormal exit"

- Key information: `permanent` is always restarted; `transient` only after an abnormal exit ("`normal`, `shutdown`, and `{shutdown, Term}` do not qualify"); `temporary` never.
- Relation to codebase: the same split as finished versus stalled. A finished worker (Orca `outcome` settled plus a read return contract) is a `normal` exit; an `exited` row with no `worker_done` is the abnormal case. The `consumer_fenced` dispatch maps to `{shutdown, Term}`: an intended stop that is never a failure (WC-12, `WORKER-CONTRACT.md:60`). Extends (gives a vocabulary for why fenced is not stalled).
- Relevance: HIGH.
- WC-10 / read-only mapping: WC-10 consistent. Restart policy is later-phase only; Phase 1 uses only the classification half.

### F1.3 Restart intensity bounds automated recovery and escalates upward

- Key information: `intensity` restarts per `period` seconds (default 1 per 5 s); exceeding it makes the supervisor stop its children and exit with `shutdown`, and "its parent then decides".
- Relation to codebase: no equivalent in the repo; the coordinator has no retry budget. For a later phase, it argues that any automatic retry needs a bound and an escalation to the person (gap G5, "when to tell the person", GQ-08). Extends.
- Relevance: MEDIUM.
- WC-10 / read-only mapping: retry is forbidden on absence by WC-10 and is an action, so later-phase only. Not applicable to Phase 1 beyond noting "repeated stalls" as a reportable fact.

### F1.4 Shutdown is graceful first, kill only after a timeout

- Key information: integer shutdown "sends `shutdown`, waits for the child's exit, then sends `kill` if the allotted milliseconds expire"; `brutal_kill` skips cleanup; supervisors default to `infinity`.
- Relation to codebase: parallels the safe-to-close REVIEW dimension (terminal releasable only after the result is read; worktree removable only when the five `WORKER-CONTRACT.md:108` refusal conditions are false). Extends.
- Relevance: LOW for Phase 1.
- WC-10 / read-only mapping: kill and shutdown are actions: later-phase only. Phase 1 prints the REVIEW line and never runs it.

---

## Area 2: Kubernetes liveness, readiness and startup probes

**Source:** https://kubernetes.io/docs/concepts/configuration/liveness-readiness-startup-probes/ (official docs; reliability HIGH). Note: WebFetch read the first 100000 of 118034 characters; the unread tail was not needed for these claims.

### F2.1 Three probes answer three different questions

- Key information: "Liveness probes determine when to restart a container"; "Readiness probes determine when a container is ready to accept traffic" and failure "does not trigger a container restart" (the Pod is removed from Service endpoints); "Startup probes verify whether the application within a container is started" and hold off the other two until they pass.
- Relation to codebase: the sweep already keeps separate dimensions, as Kubernetes does: liveness (`live`/`unverifiable`/`exited`), attention / waiting on a person (closest to readiness: alive but not accepting new work), and terminal state (`--terminal-state`, "reported separately from Task status", `worker-list --help` line 19). Supports the multi-dimension design and the rule that "waiting on a person" is healthy, not failed.
- Relevance: HIGH.
- WC-10 / read-only mapping: the readiness idea (report, do not restart) fits Phase 1. The liveness probe's restart is later-phase only. Kubernetes probes actively call into the container; the sweep must not probe the agent's terminal (GQ-51 excludes `--agent-wait`), so Phase 1 reads Orca's recorded state only.

### F2.2 Liveness probes cause cascading failures when they treat slowness as death

- Key information: "Incorrect implementation of liveness probes can lead to cascading failures"; liveness should detect unrecoverable failure, "not merely temporary overload or an unavailable dependency"; dependencies belong in readiness.
- Relation to codebase: the industry's own warning behind WC-10. A long tool call, a model wait or an unreachable remote host (`host_unavailable`, the only contact-loss reason, `orca-capabilities.md:124`) is "overload or unavailable dependency", not death. Supports WC-10 directly.
- Relevance: HIGH.
- WC-10 / read-only mapping: WC-10 consistent; this is the external justification for reporting `unverifiable` as "could not determine".

### F2.3 Startup probes give slow starters a separate, longer grace period

- Key information: "Liveness probes do not wait for readiness probes to succeed"; protect slow starts with a startup probe or `initialDelaySeconds`.
- Relation to codebase: a just-dispatched worker with no heartbeat yet is the startup case. Orca's `restored_unconfirmed` and a failed start reported `reclaimable` (`orca-capabilities.md:112`, UNVERIFIED) are the nearest repo equivalents. Extends: the sweep should not read "no activity yet" on a new dispatch as idle or stalled.
- Relevance: MEDIUM.
- WC-10 / read-only mapping: WC-10 consistent (no signal during startup is absence). Read-only: a grace period changes only the label, never an action.

### F2.4 Discrepancy check: a live process is not a live agent

- Key information: Kubernetes liveness checks whatever the probe exercises, so a process that answers the probe while its work loop is hung passes unless the probe exercises the loop (the page's deadlock example: "running but cannot make progress").
- Relation to codebase: the repo already says the same: PTY `observation.status` "is PTY liveness only. A live terminal can still hold a dead or stuck agent" (`orca-capabilities.md:123`). No contradiction; the codebase is stricter, since it accepts no PTY signal as stall proof either way.
- Relevance: MEDIUM.
- WC-10 / read-only mapping: WC-10 consistent; Phase 1 reports PTY status as context only.

---

## Area 3: Phi-accrual failure detection

**Sources:**
- Hayashibara, Défago, Yared, Katayama, "The φ Accrual Failure Detector", JAIST research report IS-RR-2004-010: https://dspace.jaist.ac.jp/dspace/bitstream/10119/4784/1/IS-RR-2004-010.pdf (peer-reviewed origin; reliability HIGH; abstract quoted via search result, PDF not fetched in full)
- Apache Pekko failure detector docs: https://nightlies.apache.org/pekko/docs/pekko/1.1.3/docs/typed/failure-detector.html (official docs of a maintained implementation; reliability HIGH)
- Pekko API reference: https://nightlies.apache.org/pekko/docs/pekko/1.1.3/japi/org/apache/pekko/remote/PhiAccrualFailureDetector.html (reliability HIGH)

### F3.1 Suspicion on a continuous scale, not a boolean

- Key information: "Instead of providing information of a boolean nature (trust vs. suspect), accrual failure detectors output a suspicion level on a continuous scale" (paper abstract). Monitoring is separated from the application's decision of what to do.
- Relation to codebase: the separation (monitor reports, application decides) matches the Phase 1 split: the sweep reports, the person decides. Orca's verdict is categorical (`live`/`unverifiable`/`exited`), not a scale. Extends: a heartbeat-age column could be shown as context.
- Relevance: HIGH.
- WC-10 / read-only mapping: a phi value is still only a measure of absence, so under WC-10 it can never become "stalled"; at most it can rank rows inside "could not determine". Computing phi is a pure read over recorded timestamps, so it is Phase 1 compatible, but Orca does not expose a heartbeat history (GQ-17 open), so it is not buildable now.

### F3.2 Phi is computed from heartbeat timing history; threshold trades speed for false alarms

- Key information: `phi(t) = log10(1 / (1 - F(t)))` where F is a normal CDF fitted to past inter-arrival gaps; "The default `threshold` is 8"; smaller thresholds detect sooner with more false alarms; `acceptable-heartbeat-pause` adds tolerance for GC stalls and network interruptions.
- Relation to codebase: agent sessions have very irregular heartbeat gaps (long tool calls, model latency, a person reading a prompt), so a fitted distribution would be wide and phi would rise slowly. That is the regime where any fixed threshold mislabels healthy sessions. Supports WC-10's refusal to treat lateness as death.
- Relevance: MEDIUM.
- WC-10 / read-only mapping: a threshold crossing is a suspicion, which WC-10 forbids acting on. Any action triggered by phi is later-phase only and still needs Orca's stall proof.

### F3.3 A suspected node can come back

- Key information: Pekko docs: phi is an estimate from timing, not certainty of a crash; a node marked unreachable "may subsequently become reachable again" (paraphrase of the fetched page).
- Relation to codebase: same as `orca-capabilities.md:122` "contact loss is not process death" and `:125` "Absence never authorizes stop, abandon, retry, or release". Supports, with no discrepancy.
- Relevance: HIGH.
- WC-10 / read-only mapping: direct external statement of WC-10. Phase 1 reports "could not determine", never "stalled", for any suspicion-only row.

---

## Area 4: "Unknown" as an explicit health state

**Sources:**
- Kubernetes node status reference: https://kubernetes.io/docs/reference/node/node-status/ (official; reliability HIGH)
- gRPC health proto: https://github.com/grpc/grpc-proto/blob/master/grpc/health/v1/health.proto (official maintained repo; reliability HIGH); guide https://grpc.io/docs/guides/health-checking/ (official)
- Nagios / Monitoring Plugins guidelines: https://nagios-plugins.org/doc/guidelines.html (official; reliability HIGH); Nagios support KB: https://support.nagios.com/kb/article.php?id=72 (vendor support article; reliability MEDIUM-HIGH)

### F4.1 Kubernetes keeps "Unknown" (no contact) separate from "False" (reported unhealthy)

- Key information: Ready is "`True` if the node is healthy and ready to accept pods, `False` if the node is not healthy and is not accepting pods, and `Unknown` if the node controller has not heard from the node in the last `node-monitor-grace-period` (default is 50 seconds)". Heartbeats are Node `.status` updates and per-node Lease renewals (every 10 s). The same page also says "40 second default timeout for unreachable nodes", so the page is internally inconsistent on the default.
- Relation to codebase: a three-way split that matches Orca's verdicts closely: `True` ~ `live`, `Unknown` ~ `unverifiable` (no recent contact), `False` ~ a positive report of failure (`exited` / observed exit). Kubernetes treats `Unknown` as its own value, not as `False`. Supports the "could not determine" class.
- Relevance: HIGH.
- WC-10 / read-only mapping: WC-10 consistent at the status layer. Discrepancy: Kubernetes does act on `Unknown` after a toleration (default 300 s, `node.kubernetes.io/unreachable` taint, per https://kubernetes.io/docs/concepts/scheduling-eviction/taint-and-toleration/ via search, not fetched) by evicting pods. That eviction is exactly what WC-10 forbids for workers; record it as a later-phase pattern that the repo deliberately rejects. Phase 1 only labels.

### F4.2 gRPC health has UNKNOWN as the zero value and a distinct SERVICE_UNKNOWN

- Key information: `ServingStatus` is `UNKNOWN = 0`, `SERVING = 1`, `NOT_SERVING = 2`, `SERVICE_UNKNOWN = 3` ("Used only by the Watch method"). `Check` on an unrecognised service fails with `NOT_FOUND`; `Watch` returns `SERVICE_UNKNOWN` and keeps the stream open until the service becomes known.
- Relation to codebase: two different unknowns: "health not known yet" versus "no such thing is registered". The sweep has the same pair: "could not determine" (row exists, evidence absent) versus a row or source that is not readable at all (the `unscanned:` markers from sc-crash-recovery, `research/scope-02-orca-recovery.md:239`, and the absent-versus-null `agentWait` split, GQ-58). Extends: keep the two kinds distinct in the report.
- Relevance: MEDIUM.
- WC-10 / read-only mapping: WC-10 consistent (UNKNOWN is the default, never NOT_SERVING). `Check` and `Watch` are calls into the service, i.e. probes; Phase 1 does not probe agents, so only the vocabulary carries over.

### F4.3 Nagios UNKNOWN means "the check itself could not run"; a contradiction on timeouts

- Key information: return codes 0 OK, 1 WARNING, 2 CRITICAL, 3 UNKNOWN; UNKNOWN is for invalid arguments or an internal low-level failure that made the check impossible. The Nagios support KB says DNS lookup failures and socket timeouts "should generally NOT be reported as UNKNOWN states" (it does not say which code to use instead).
- Relation to codebase: partly contradicts. Nagios narrows UNKNOWN to "the monitor broke" and pushes a timeout toward a failure state; the codebase treats contact loss (`host_unavailable`, `stale_status`) as `unverifiable`, which the sweep reports as "could not determine". The codebase wins (WC-10, `WORKER-CONTRACT.md:45`; `orca-capabilities.md:125`). The reason the two differ is the domain: a Nagios timeout on a network service is a user-visible outage of that service, while a late agent heartbeat says nothing about whether the agent is still doing useful work.
- Relevance: MEDIUM.
- WC-10 / read-only mapping: the Nagios timeout-as-failure convention conflicts with WC-10 and is not adopted. The useful part that does carry over: when the sweep's own read fails (Orca not running, a page that will not load), say so as a sweep failure, separate from a row's "could not determine".

---

## Area 5: Community and implementation patterns for LLM agent sessions

**Sources:**
- Harmonograf ADR 0018, heartbeat stuck detection: https://github.com/pedapudi/harmonograf/blob/main/docs/adr/0018-heartbeat-stuck-detection.md (maintained repo ADR; reliability MEDIUM)
- Camunda, detect off-rail agents: https://docs.camunda.io/docs/next/components/agentic-orchestration/evaluate-agents/detect-off-rail-agents/ (vendor official docs, `next` version; reliability HIGH for Camunda behaviour)
- Search-result-only, not fetched (reliability LOW, context only): Simple Agent Manager session troubleshooting https://www.simple-agent-manager.org/docs/guides/session-troubleshooting/ (separates "Needs input", provider-limit waits and stuck work); agents-fleet coordinator resilience https://docs.agents-fleet.ai/advanced/coordinator-resilience (watchdog with stall notice and automatic abort).

### F5.1 Progress counters beat heartbeat presence, but stuck detection stays a heuristic

- Key information: Harmonograf heartbeats carry a `progress_counter`; an unchanged, nonzero counter across `STUCK_THRESHOLD` consecutive heartbeats on a running invocation is flagged. The response is a UI alert only; no restart. The ADR says "Stuck detection is a heuristic" and "Heartbeat can itself hang"; children's progress can mask a blocked parent.
- Relation to codebase: closest external match to the sweep. It confirms that a liveness heartbeat says nothing about progress (`orca-capabilities.md:130`, "proves liveness, not completion") and that even a progress-based flag is a suspicion. Its alert-only response fits Phase 1. Discrepancy: Harmonograf calls the flagged state "stuck"; under WC-10 and Section C rule 2 the sweep must not use "stalled" for that, so any such signal would be shown as a note on a "could not determine" or "working" row. The parent/child masking matches GQ-40 (nested workers).
- Relevance: HIGH.
- WC-10 / read-only mapping: WC-10 consistent only if the flag is labelled as a suspicion. Read-only: compatible (alert only), but Orca exposes no progress counter today, so not buildable in Phase 1.

### F5.2 Time waiting for outside input is excluded from health budgets

- Key information: Camunda splits agent time into "Thinking", "Tool calling" and "Idle" (paused for outside input); execution duration excludes input-waiting periods; "No single health indicator proves that an agent is stuck." At the limit an error is raised, which an error boundary can route to a person.
- Relation to codebase: supports the rule that waiting on a person is healthy and must not count toward stalled or toward the activity window (`worker-show --help` line 16; Section C rule 4). It also supports the owner note at GQ-61 that the 6 h window should bound activity only. Supports.
- Relevance: HIGH.
- WC-10 / read-only mapping: WC-10 consistent. The limit-triggered error and routing are actions: later-phase only. Phase 1 can use the split to keep person-wait time out of any age it prints.

---

## Discrepancies with the codebase (codebase wins)

| # | External pattern | Codebase rule | Outcome |
|---|---|---|---|
| D1 | Kubernetes evicts pods after a node is `Unknown` past its toleration (F4.1) | WC-10: absence never authorizes stop, retry or release (`WORKER-CONTRACT.md:45`; `orca-capabilities.md:125`) | Rejected for workers; recorded as a pattern the repo deliberately does not follow |
| D2 | Nagios KB: timeouts and DNS failures "should generally NOT be reported as UNKNOWN" (F4.3) | Contact loss is `unverifiable`, reported "could not determine" | Codebase wins; domain differs (service outage versus agent progress) |
| D3 | Harmonograf labels a progress-free run "stuck" (F5.1) | "stalled" needs positive stop proof (Section C rule 2) | Show as a note, never as the stalled class |
| D4 | Kubernetes liveness probe restarts on probe failure (F2.1) | Phase 1 never acts and never probes the agent's terminal (GQ-51) | Later phase only, and only with Orca's stall proof |

No external source contradicts WC-10's core claim; F2.2, F3.3 and F4.1 (status layer) state it independently.

---

## Key External Findings

1. Every mature supervisor acts on positive evidence of exit, not on silence: OTP restarts on an exit signal (F1.1); Pekko's phi detector says a suspected node can come back (F3.3); Kubernetes warns that liveness probes that treat slowness as death cause cascading failures (F2.2). This is independent support for WC-10.
2. "Unknown" is a first-class value in Kubernetes node status (`Ready=Unknown`, F4.1) and gRPC health (`UNKNOWN = 0`, F4.2), kept separate from "unhealthy". This supports "could not determine" as its own class rather than folding it into stalled or working.
3. Health has several independent dimensions: Kubernetes separates liveness, readiness and startup (F2.1), as the sweep separates liveness verdict, waiting on a person, and terminal state / safe-to-close.
4. Waiting for outside input is healthy and is excluded from time budgets (Camunda, F5.2), which supports "waiting on a person is healthy" and bounding the 6 h window to activity only (GQ-61).
5. Progress, not presence, is the better stuck signal, but it is still a heuristic (Harmonograf, F5.1; phi accrual, F3.1-F3.2). Neither yields the positive stop proof that Section C rule 2 requires.
6. Two kinds of unknown recur: "health not known" versus "subject not known / check could not run" (gRPC `UNKNOWN` versus `SERVICE_UNKNOWN`, F4.2; Nagios UNKNOWN as a broken check, F4.3).
7. Every action-taking pattern (restart, kill, evict, auto-abort, retry budget) is later-phase only for #339; Phase 1 can take only the vocabulary and the report-not-act stance.

## Recommendations from External Research

1. Keep "could not determine" as an explicit class and split its cause in the report: (a) evidence absent for a row that exists (`unverifiable`, null-versus-absent `agentWait`), and (b) the sweep could not read a source at all (Orca down, page failed, `unscanned:`). Source: F4.2, F4.3. Read-only: yes.
2. Keep "stalled" tied to positive proof only (`exited`, observed exit, proved-final transcript turn without `worker_done`); show heartbeat age or any progress heuristic as a note column, never as a class. Source: F1.1, F3.1-F3.3, F5.1. Read-only: yes; WC-10 compliant.
3. Treat a just-dispatched worker with no signal yet as a startup case, reported "working" or "could not determine", never idle or stalled. Source: F2.3. Read-only: yes.
4. Exclude person-wait time from any age the sweep prints and from the 6 h activity window. Source: F5.2. Read-only: yes.
5. For a later phase only: if automatic recovery is ever added, bound it OTP-style (a restart budget per period, then escalate to the person) and gate every action on Orca's stall proof, never on `unverifiable` or a late heartbeat. Source: F1.3, F2.2, D1. Not Phase 1.
6. Do not compute phi-accrual or progress-counter scores in Phase 1: Orca exposes no heartbeat history or progress counter (GQ-17 open), and the score could only rank suspicion, which WC-10 forbids acting on. Source: F3.1, F5.1.

---

## Sources

| # | URL | Type | Reliability | Fetched |
|---|---|---|---|---|
| 1 | https://www.erlang.org/doc/system/sup_princ.html | Official docs | HIGH | WebFetch |
| 2 | https://kubernetes.io/docs/concepts/configuration/liveness-readiness-startup-probes/ | Official docs | HIGH | WebFetch (first 100000 of 118034 chars) |
| 3 | https://kubernetes.io/docs/reference/node/node-status/ | Official docs | HIGH | WebFetch (first 100000 of 100733 chars) |
| 4 | https://kubernetes.io/docs/concepts/scheduling-eviction/taint-and-toleration/ | Official docs | HIGH | Search result only |
| 5 | https://dspace.jaist.ac.jp/dspace/bitstream/10119/4784/1/IS-RR-2004-010.pdf | Research paper | HIGH | Search result (abstract) only |
| 6 | https://nightlies.apache.org/pekko/docs/pekko/1.1.3/docs/typed/failure-detector.html | Official docs | HIGH | WebFetch |
| 7 | https://nightlies.apache.org/pekko/docs/pekko/1.1.3/japi/org/apache/pekko/remote/PhiAccrualFailureDetector.html | API reference | HIGH | Search result only |
| 8 | https://github.com/grpc/grpc-proto/blob/master/grpc/health/v1/health.proto | Maintained repo (spec) | HIGH | WebFetch |
| 9 | https://grpc.io/docs/guides/health-checking/ | Official docs | HIGH | Search result only |
| 10 | https://nagios-plugins.org/doc/guidelines.html | Official guidelines | HIGH | WebFetch |
| 11 | https://support.nagios.com/kb/article.php?id=72 | Vendor support KB | MEDIUM-HIGH | WebFetch |
| 12 | https://github.com/pedapudi/harmonograf/blob/main/docs/adr/0018-heartbeat-stuck-detection.md | Maintained repo ADR | MEDIUM | WebFetch |
| 13 | https://docs.camunda.io/docs/next/components/agentic-orchestration/evaluate-agents/detect-off-rail-agents/ | Vendor official docs | HIGH | WebFetch |
| 14 | https://www.simple-agent-manager.org/docs/guides/session-troubleshooting/ | Product docs | LOW (unfetched) | Search result only |
| 15 | https://docs.agents-fleet.ai/advanced/coordinator-resilience | Product docs | LOW (unfetched) | Search result only |

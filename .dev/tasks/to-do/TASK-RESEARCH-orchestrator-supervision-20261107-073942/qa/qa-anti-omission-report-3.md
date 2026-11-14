## Anti-Omission Report

**Report reviewed:** `RESEARCH-REPORT-orchestrator-mode.md` (1740 lines)
**Input files checked:** `research/web-01-agent-supervisor-session-health.md`, `research/web-02-static-status-report-conventions.md`, `gaps-and-questions.md`, `synthesis/synth-01-problem-current-state.md`, `synthesis/synth-02-target-gaps.md`, `synthesis/synth-03-external-findings.md` (partition 3)
**Total findings enumerated:** about 354 (approximate; breakdown in Summary)
**Date:** 2026-11-07
**Method:** coverage judged by meaning, not by ID citation. Every finding, rule, recommendation, gap row (GQ-01 to GQ-100, K1-K4, AMBIGUITIES 1-11, C1-C15, section (e) rows, S-01 to S-14), synth-02 Section 4 row and external finding was searched for in the report. Fix authorization: false; the report and inputs were not edited.

### Omissions Found

| # | Source finding | Source file | Status | If deduped, by which report item | Severity |
|---|---|---|---|---|---|
| 1 | Research gate trajectory: the gate "ended by coordinator exception, not a clean PASS"; it ran 2 fix cycles and blocking findings went 28 -> 3 -> 1 before the coordinator authorized proceeding with NB-4 open | `gaps-and-questions.md:7` | OMITTED (partly) | The exception itself is carried: report `:13` (header), `:1669` (9.6) and `:1740` (§10) say NB-4 "was a coordinator-approved exception at the Phase 3 research gate". A grep for `28 -> 3`, `clean PASS`, `fix cycles`, `2 fix` and `blocking findings` finds nothing, so the cycle count and the 28 -> 3 -> 1 trajectory are dropped | MINOR (the load-bearing fact, that the gate did not pass cleanly and needed an exception, survives; only the audit-trail numbers are lost) |
| 2 | Section (e) row `05-orca-row-schema.md:125`: the `reason` field is [UNVERIFIED] and open, with no GQ assigned | `gaps-and-questions.md:271` | COVERED-BY-DEDUP | §9.1 row 12 (`:1530`, GQ-15, "what values can `liveness.reason` take?"), the §4.4 grouped row `:560`, and §2 `:132`. Same unknown, same handling (unknown value -> could not determine) | MINOR |
| 3 | Section (e) row `06-orca-open-questions.md:102`: peer `ask` behaviour is [UNVERIFIED] and open, with no GQ assigned | `gaps-and-questions.md:294` | COVERED-BY-DEDUP | §9.1 row 41 (`:1560`, GQ-49 / GQ-50, peer `ask --to run:<id>`, "Record only; not used in Phase 1") | MINOR |
| 4 | Section (e) rows `06-orca-open-questions.md:104, :111, :118`: the agent-wait probe. The gaps file maps them to GQ-50, but the probe question is GQ-51 (GQ-50 is peer `ask`), an internal mislabel in the source | `gaps-and-questions.md:295` | COVERED-BY-DEDUP | §9.1 row 42 (`:1561`, GQ-51, "Excluded"), §7 `:1144` (S9 row 42), §8 `:1408`, §5.2 `:707` and D4 `:839`. The report maps the content to the correct GQ | MINOR (source-side mislabel, not a report omission) |
| 5 | GQ-09 status: the gaps file records "whether the sweep reports person-started (peer) sessions at all" as "open (owner decision, WC-14)", and K1 / AMBIGUITY 8 repeat "stays an owner decision" | `gaps-and-questions.md:32`, `:137`, `:157` | REPRESENTED (status changed) | The report carries the finding but resolves it: §9.2 row 66 (`:1596`) says "GQ-09 is settled by the sources (row 7)". The owner-decision framing is not dropped silently, because the report names the basis (`WORKER-CONTRACT.md:11`, `orca-capabilities.md:148-151`). A reader comparing the two files sees a status change, not a loss | MINOR (fidelity note; no blocking omission) |

### Adversarial probes that found the finding present

The stance assumed at least five dropped findings. These were the most likely drops, and each was checked by meaning in the report and found present:

- web-01 recommendation 3 (a just-dispatched worker is a startup case, never idle or stalled): §5.2 `:716`, R3 `:882`.
- web-01 recommendation 4 (keep person-wait time out of ages and the 6 h window): `:497`, `:781`, R4 `:883`, which also keeps the exception that the waiting list sorts on time since the wait began.
- web-01 recommendation 1 (two kinds of unknown: evidence absent versus source unreadable, the latter a sweep failure): `:496`, `:752`, `:763`, R1 `:880`.
- web-01 F1.3 and F1.4 (OTP restart intensity; graceful-then-kill shutdown): §5.1 `:690`, `:695`.
- web-01 F3.2 (`acceptable-heartbeat-pause`, default threshold 8): `:731`.
- web-01 F4.1 data note (the Kubernetes page gives both 50 s and 40 s): `:748`, C2 `:848`.
- web-01 F5.1 caveats ("Heartbeat can itself hang"; children's progress can mask a blocked parent): `:772`.
- web-01 unfetched context sources (Simple Agent Manager, agents-fleet): `:782-783`, D6 `:841`, `:1433`.
- web-01 versus web-02 timeout conflict (Nagios KB versus Icinga): C1 `:847`, §9.4 row 95 `:1641`.
- Open section (e) rows `06:15-16`, `06:127-132` and `06:100`: §9.2 rows 76-78 (`:1606-1608`).
- `06:144` (null `agentWait`, CC by help): `:551`, `:601`, `:631`, X-4 `:1450`, §9.1 row 48 `:1567`.

### Summary

- Findings enumerated: about 354. This is an approximate count: GQ-01 to GQ-100 (100), K1-K4 (4), AMBIGUITIES 1-11 (11), C1-C15 (15), open or partly open section (e) rows (about 30), S-01 to S-14 (14), web-01 and web-02 findings, key findings, recommendations and discrepancies (about 60), and synth-01/02/03 items: rule rows, SC-1 to SC-16, R-1 to R-3, Section 4 gap rows, open questions, R1-R9, L1-L2, D1-D6, C1-C2 (about 120).
- Represented: about 350 (including row 5, represented with a changed status).
- Covered-by-dedup: 3 (rows 2, 3, 4).
- Omitted: 1 (row 1, partial).
  - Blocking omissions (CRITICAL or IMPORTANT): 0.
  - MINOR omissions: 1 (row 1). Rows 2-5 are MINOR notes, not omissions.
- [PARTITION NOTE: Cross-file checks limited to assigned subset. Full cross-file analysis requires merging all partition reports.]
- Not checked: report §6-§8 (`:902-1508`) was searched with Grep only, not read line by line. That is enough to confirm that a finding is present, but it could miss a finding that is reworded there and never appears in §1-§5 or §9-§10.

Verdict: PASS

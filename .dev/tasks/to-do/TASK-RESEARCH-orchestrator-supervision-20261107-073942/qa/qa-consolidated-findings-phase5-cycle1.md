# Consolidated findings: Phase 5 synthesis gate, repeat cycle 1 (second and last fix pass)

- Sources: `qa/qa-synthesis-verification.md` (structural, FAIL), `qa/qa-synthesis-verification-qualitative.md` (qualitative, FAIL)
- Previous: |F_0| = 15 (`qa/qa-consolidated-findings-phase5.md`), fix log `qa/qa-synthesis-fix-log.md`
- |F_1| = 3
- Gate status: FAIL
- Regression: none (both verifiers report no previously PASS item now fails)
- Merge rule: union of blocking findings from both reports; B-13 is graded MINOR by the structural report and IMPORTANT (N-2) by the qualitative report; kept as blocking because it is a false count claim.

## Blocking findings

| ID | Severity | File and line | Issue | Required fix | Source |
|---|---|---|---|---|---|
| C1-01 | IMPORTANT | `synthesis/synth-03-external-findings.md:114` | Still reads "Phase 1 can keep person-wait time out of any age it prints." This is the claim B-12 flagged; it contradicts R4 on the same page (`:216`, waiting list prints and sorts on the question's original age), `research/scope-04*:87` and `synthesis/synth-05-implementation-plan.md:63`. | Change to: "Phase 1 keeps person-wait time out of activity ages and the 6 h activity window; the waiting-on-a-person list prints the time since the wait began (R4)." | structural B-12 OPEN (`qa-synthesis-verification.md:29`) |
| C1-02 | IMPORTANT | `synthesis/synth-05-implementation-plan.md:10` ("Research question" row) | Lists seven classes including fenced and attributes them to the research question. The task file GOAL lists six; OQ-13 on the same page (`:225`) and headers S1 `:5`, S3 `:7`, S4 `:3`, S6 `:3` say six. | Reword to: "(waiting on a person, working, stalled (proved), finished, could not determine, idle: the research question's six; Section C adds fenced as a seventh, the working default, OQ-13)". Same pass, optional: align S1 `:15` "The question." with its header. | structural B-14 OPEN (`qa-synthesis-verification.md:31`), qualitative N-1 (`qa-synthesis-verification-qualitative.md:45`) |
| C1-03 | IMPORTANT | `synthesis/synth-03-external-findings.md:183` | Says "three external sources contradict WC-10, and all three are rejected" (Grafana D5, agents-fleet D6, Nagios D2 in part). D1 (Kubernetes taint and eviction after `Unknown`, `:169`) is also rejected under WC-10 (`:81`), and S2 4.8 `:290` counts Kubernetes and Harmonograf against WC-10. Count is wrong and S3 and S2 disagree. | Change to: "four external patterns contradict WC-10 and are rejected: Grafana's missing-data mapping (D5), the agents-fleet auto-abort (D6), Kubernetes taint and eviction after `Unknown` (D1), and, in part, the Nagios KB timeout guidance (D2). Harmonograf's 'stuck' label (D3) and the liveness-probe restart (D4) are rejected as actions or naming, not as contradictions of absence-is-not-death." Keep "Kubernetes node status at the status layer" in the supporting list, and align S2 `:290` with this reading. | qualitative N-2 (`qa-synthesis-verification-qualitative.md:46`), structural note N-3 |

## MINOR notes (not fixed, not rechecked)

Structural N-1, N-2; qualitative M-1 to M-7. See the two verification reports.

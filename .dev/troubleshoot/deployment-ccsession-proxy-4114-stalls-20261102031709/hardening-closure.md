# Pipeline Hardening Closure (Wave 4.5)

## HC0 — Applicability, boundary scan, mechanism

pipeline_hardening_applicable: true (the defect sits at a CLI -> subprocess boundary: the `ccsession` launcher starts the long-lived shim subprocess that other sessions depend on).

| boundary_type | producer / transformers / consumer | evidence_source | risk | decision | rationale |
|---|---|---|---|---|---|
| CLI/subprocess | producer: `ccsession` setup_shim start statement (ccsession:801-804) / transformers: `nohup`, background `&`, then `exec` of Claude Code (ccsession:1379-1440) / consumers: every Claude Code session whose ANTHROPIC_BASE_URL points at the shim port, plus ccsession's own reuse probes (shim_listener_pid ccsession:712-724, shim_health_status ccsession:726-750) | tier1-observation.md O2, O8, O9, O10 | a unit test that starts the shim directly (tests' `shim` fixture, test_ccsession_tiers.py:574-614) proves routing but never exercises the launcher's process placement, so it can pass while the real launch leaves the shim in the terminal's tree | applicable | the failure only appears through the real launcher plus a terminal kill, so proof must run at that boundary |
| file-stdin-prompt | n/a | ccsession:804 (stdin/stdout to /dev/null) | none for this defect | not_applicable | no prompt or file payload crosses this boundary |
| generated-artifact-parser | n/a | — | none | not_applicable | no generated artifact is parsed |
| gate-status-enum | n/a | — | none | not_applicable | no gate or status enum involved |
| duplicate-evaluator | sibling launch path: README.md:494-495 manual restart recipe uses the same `nohup ... &` | wave1_6-branch-B.md | the README recipe would recreate an attached shim | applicable (covered by HC2 sweep) | a sibling launch path must not keep the defect |
| persisted-state | n/a | — | none | not_applicable | shim keeps no persisted state across restarts |
| review-selector | n/a | — | none | not_applicable | no review selector involved |
| sibling-pipeline | test fixtures that start the shim (`shim` fixture, `_real_launch`) | test_ccsession_tiers.py:574-614, 1344-1376 | cleanup relies on `pkill -f <script path>`; detaching must keep argv | applicable (covered by HC2) | cleanup must still find detached shims |
| prior-escape-unmask | n/a | — | none | not_applicable | no prior escape masked this one |

Mechanism statement (feature-agnostic): a long-lived service shared by many clients is started as an ordinary child of one client's process tree, so its lifetime is silently bound to that one client's container (terminal, process group, session); a test that starts the service directly substitutes for the real launch path and cannot see the binding.

known_escapes_caught: [] (no E1-E5 replay scenario applies; anti-inflation rule).

## HC1 — Runtime entrypoint

Card: hc1-runtime-entrypoint.md. Status at diagnosis time: N/A with rationale — the fix is not applied yet; the replay and its negative witness are pre-registered and the negative witness at HEAD already observed (live-check/before.txt). Status is re-evaluated after implementation (REPORT.md Remediation section).

## HC2 — Contract enumeration

Card: hc2-contract-ledger.md. Status: PASS (ledger non-empty, every live consumer classified, sibling launch paths swept).

## HC3 — Unmask and sweep

Status: N/A — rationale: no generated artifact or classifier/allow-list is involved; the defect is process placement, not text classification.

## HC4 — Effective-input proof

Status: N/A — rationale: no review/audit gate consumes an indirect selector in this defect.

## HC5 — Off-path review

off_path_review_decision: required (a CLI invokes a subprocess). To be performed by the PR's independent reviewers (Augment/Codex via /sc:pr-submit) and the /sc:reflect --mode post gate after implementation.

## Verdict (§5.4)

waiver_status: none. backtest_status: not_run.
pipeline_hardening_verdict: advisory (row 6: N/A with valid rationale on HC1/HC3/HC4, no FAIL, no latch). Expected to stay advisory after implementation because HC3/HC4 remain rationalized N/A.

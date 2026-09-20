# Wave 1 observation and internal runner source map

## Confirmed observation (not a root-cause hypothesis)

Read-only `gh api repos/IronbellyOrg/Coder/actions/artifacts/10564836537` confirms artifact `startup-boot-sysbox-runc-public-433-1`, 6136 bytes, not expired, run 35377326118, SHA a9d3af8181570d9281eca9936f5d0e26039afe6b. `gh api repos/IronbellyOrg/Coder/actions/jobs/105713898868` confirms that SHA/run and failed `RC-1 — fresh-boot home-provisioning gate`; setup/create/agent readiness succeeded. This is not an unavailable GitHub Actions runner.

`unzip -l /tmp/sysbox-pr171-retry2-public-evidence.zip` lists 14 files; `unzip -p ... seed-checkout.txt` returns:

```text
seed-outcome-observed=runner-unavailable
section8-status-observed=fail
seed-diag-dns-github=true
seed-diag-https-github=true
seed-diag-checkout-dir=false
seed-diag-checkout-toplevel=false
remote-assertion=fail
```

The saved archive size matches API metadata; no independent download/digest comparison was performed. Its startup-run.json reports current named startup returned-success, exit 0, duration 14.004305124282837 seconds, source binding installed-current-invocation. This aggregate success is compatible with an optional seed failure. startup-boot-rerun.log is only 22 bytes, `remote-assertion=fail`; no F08_RERUN witness. test-startup-boot.log ends `RESULT: FAIL (2 failure(s))`. Later network success is not historical startup network proof.

Git diffs establish both production files below unchanged between failing a9d3af8 and current reverted f39f834. The diagnostic collector in test-startup-boot.sh WAS reverted: `git show a9d3af8 -- .github/contract-tests/test-startup-boot.sh` verifies the failing commit's added seed_diag_rows and enum/boolean projection. Its probes precede the seed assertion, not the startup clone.

## Source keys (absolute)

- S = `/config/workspace/Coder/.claude/worktrees/sysbox-retry-astra/templates/VSCode-AIDev02/scripts/startup.sh`
- A = `/config/workspace/Coder/.claude/worktrees/sysbox-retry-astra/templates/VSCode-AIDev02/scripts/startup-git-askpass.sh`
- T = `/config/workspace/Coder/.claude/worktrees/sysbox-retry-astra/.github/contract-tests/test-51-selector-onboarding-wiring.sh`
- B = `/config/workspace/Coder/.claude/worktrees/sysbox-retry-astra/.github/contract-tests/test-startup-boot.sh`

Line references below use these keys at current HEAD. B's historical retry2 collector adds 41 lines before its seed invocation; do not mistake current line numbers for failing-revision ones.

## Return-class correction

There is NO numeric return/exit 171 in S or A. Exact `git grep` over those two files found only the five explicit return/exit **27** sites in A (37,38,49,90,204). A:23 maps 27 to runner-unavailable. PR171 is the incident identifier, not a production exit class. S communicates an outcome string; its setup failure returns 1, translated by S:759-760.

## Every runner-unavailable route in section 8

| Surface | Exact branch / result | Existing observability |
|---|---|---|
| S:571,752 | Initialize local rc and outer outcome to runner-unavailable. Any unclassified exit from supervision retains this default. | Final aggregate enum, no branch code. |
| S:579; S:502-507 | Missing setsid OR git OR failed uptime read/strict parse => return 1 => S:759-760 runner-unavailable. Uptime must be 1–9 integer digits, dot, exactly two fractional digits; read failure and format failure both return 1. | No individual dependency/clock classification. |
| S:581 | mktemp failure => return 1 => runner-unavailable. | No setup-stage classification. |
| S:582-584 | auth-lock creation failure => rmdir attempt, return 1 => runner-unavailable. | No control-file classification. |
| S:600-605,699-704 | env/setsid/bash launch or FD9 redirection can fail asynchronously. PID captured; immediate stat read/parent check determines whether starttime identity is recorded. No classified launch-result channel. | Child stdout/stderr discarded at 699; no launch exit retained. |
| S:538-545,701-712 | Positive PID, readable stat, direct parent=BASHPID, same starttime required; group mode additionally pgrp=session=seed_pid. Failed initial read/parent check leaves identity empty. Handshake breaks on ownership loss or sleep failure; absent verified group at 712 leaves default rc. | Predicate failures suppressed via 2>/dev/null; no reason distinguishes parent/starttime/group/session/read failures. |
| S:613-618 | Before go, child read/parse failure or deadline expiry exits 1, without result. Parent can observe ownership loss and retain default (subject to final deadline normalization). | Child output discarded; no pre-go result. |
| S:712-715 | Once owned and within deadline, emits started BEFORE creating go. Failure to create go retains default. | Started proves gate reached, not go creation or Git launch. |
| S:716-718 | Lost group ownership ends loop retaining default; failed parent monotonic-clock read/parse explicitly sets runner-unavailable. | No distinction between identity loss, process disappearance, clock failure. |
| S:720-724 | Read nonempty result and accept allowlisted value, including runner-unavailable. Unknown/empty line after successful read breaks while retaining default. Unreadable/absent/zero-length file keeps polling. | Only accepted final enum survives. Missing result alone normally runs to deadline, not immediately runner-unavailable. |
| S:726 | Poll sleep failure breaks without setting a new rc. | No classified sleep error. |
| S:659-669 | Failed git clone defaults clone-failed; only fixed auth-status runner-unavailable can upgrade it to that enum; writes result consumed above. Failed result write leaves no success channel. | Git output discarded, auth category only. Successful clone does not consult auth-status. |
| S:679-692 | Leader watchdog uses deadline fallback on invalid uptime; self-stat read/group/session failure exits 1. Deadline or changed parent triggers group TERM/grace/KILL. Early ownership loss can leave parent default; parent deadline check may instead normalize timeout. | No watchdog cause or child exit status exported. |
| S:734-737 | Default runner-unavailable becomes timed-out only if final clock read works and deadline reached; cancellation overrides before AND after cleanup. | Final enum reflects these overrides; not all earlier runner-unavailable candidates remain runner-unavailable. |
| S:747,759-765 | Normal attempt publishes rc; setup return nonzero maps to runner-unavailable in caller; then final enum emitted. | Coarse final outcome only. |

Important separate branch: S:713 failure after ownership is established sets **timed-out** at 729-730 even if its clock call failed. It is NOT a runner-unavailable branch. Invalid budgets produce invalid-budget at 576-577; bad URL/destination take rejected-input/destination-conflict at 755-758; blank input skips. These must not be conflated with the observed class.

## Adapter class 27 producers and transport

All explicit producers:

1. A:37 failed `/proc/uptime` read => return 27.
2. A:38 strict uptime-format rejection => return 27.
3. A:49 `/usr/bin/jq` not executable => exit 27.
4. A:90 `/usr/bin/curl` not executable in lookup => exit 27.
5. A:204 `/usr/bin/flock` not executable in client => exit 27.

Propagation: lookup calls remaining_time at A:107,144; failed lookup status passes through A:148-150. Exchange admits code 27 in A:177-183 response frame. Client explicitly propagates remaining_time errors at A:210,212,220,222,225,235 and accepts response code 27 at A:237. EXIT trap A:16-31 writes runner-unavailable only for main-shell exit 27 and only when FD9 is an owned regular file (A:27). Startup consumes that fixed category at S:663-665 then S:720-724.

Not every adapter 27 becomes a seed runner-unavailable: exchange disables EXIT trap at A:163, is launched with FD9 closed (S:625), and its remaining_time loop/after-lookup guard can finish without a reply (A:164,180). Client channel validation failures A:192-207 are **23/auth-unavailable**, not 27. Missing adapter with generic clone failure remains clone-failed (S:762-764). An idle exchange failure does not itself imply public Git used askpass.

## Cleanup and persistence boundaries

S:548-565 checks ownership immediately before signals. Verified group gets TERM, monotonic grace, reverified KILL. If only direct-child identity is verified before setsid, KILL targets PID only; never inherited group. wait collects child status but ignores it. Caller restores monitor mode and prior traps at S:738-743. Fixed go/result/auth-status/auth-lock files removed at S:745-746; repo/remnants are not removed. Thus the private branch/result evidence is not retained post-cleanup. No relaxation of these guards is proposed.

## Existing emitted observability versus absent evidence

Present in production:
- S:714 started marker after ownership+time check, before go.
- S:765 final stdout enum; S:767-772 best-effort safe regular-file outcome sinks.
- S:774 completion marker means section reached, not successful checkout.
- S:2003-2009 summary outcome plus fail status for runner-unavailable.
- A:16-31 private fixed-category descriptor; no raw credentials/transport payload.

Absent from this captured artifact / not emitted by these branches:
- Which setup/identity/time/result failure produced the enum; phase reached, per-stage duration, predicate reason, leader/worker exit status.
- No raw startup section-8 transcript or started-marker witness among the 14 saved files; private result/auth-status files are cleaned.
- Exact prior network state cannot be reconstructed from later successful probes.
- No evidence that the rerun actually executed: B:1960-1968 asserts public cloned checkout before invoking startup; F08_RERUN only emitted later at B:1973. The saved single failure row cannot prove an orchestrator rerun failure.

This inventory is Wave 1 grounding, NOT a completed Wave 1.6 diagnosability verdict.

## Existing tests inspected (not executed)

T:1817-1848 checks outcome, summary, finite elapsed time, following-section continuation, untouched later auth, no raw URL leakage. T:1854-1881 covers blank/public, admitted/rejected inputs, established auth failure, generic Git failure, preserved edits, Git/helper timeout. T:1932-1942 covers FIFO/directory diagnostic sinks and missing adapter (public succeeds; private generic clone failure). T:1944-1958 covers malformed budgets. T:1971-2004 introduces real adapter protocol fixtures with mocked curl, not live network.

T:2394-2415 exercises cancellation before setsid handshake and after launch/exchange; T:2419-2446 asserts no recorded descendant/zombie/group survivors and unrelated process remains alive. The only runner-unavailable literal found in T is its observed-outcome enumeration at 1845; no named runner-unavailable expected-outcome fixture surfaced. These inspected tests do not identify the actual failing branch under Sysbox.

## Next protocol gate

Wave 1.5 requires three independent documentation agents per `/config/.claude/skills/sc-troubleshoot-protocol/SKILL.md:187-201` and `/config/.claude/skills/sc-troubleshoot-protocol/refs/doc-discovery.md`. No Agent/Task tool exists in this delegation. Parent must supply branch A release-doc, B architecture+currency, C restrictions; then synthesize doc-context.md before Wave 1.6's independent log-call/log-config audit. No hypothesis or fix was formed here. Separate implementation authorization remains intact; this is a diagnosis-protocol handoff, not a new approval prerequisite.

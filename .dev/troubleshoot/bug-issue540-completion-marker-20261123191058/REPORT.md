# Troubleshoot Report

**Target**: issue 540, successful foreground swarm run omits done.json
**Type**: bug
**Tier reached**: 1
**Confidence**: 1.00 (independent rubric score for the scoped diagnosis, not repair readiness)
**Status**: blocked
**Escalation reason**: none
**Test is wrong**: false
**Behavior is documented**: false
**Doc context card**: ./doc-context.md
**Duration**: 1668 seconds at finalization checkpoint
**Date**: 2026-11-23T19:38:46Z

## Summary

Repair closure is unproven: no implementation or fix-applied positive CLI witness exists. This run conservatively records HC1 FAIL and report status blocked; the protocol's handling of a diagnosis before any fix is ambiguous, not an established unconditional rule that planning must wait for a repaired run. Real isolated simulated-worker foreground and resume runs reproduced the omission despite success contracts and terminal state. Both completion continuations omit the existing marker writer; the supported proposal is to connect it after contract and terminal-state persistence, honoring effective policy and actual result status. No production source, tests or product documentation changed.

## Documentation Context

- Relevant refs: doc-context.md and persisted discovery branches, plus current source completion policy.
- Documented behavior: operator docs describe today's limitation; the source model defines default-on marker publication, which the issue explicitly requests implementing.
- Restrictions honored: contract before terminal before marker; existing writer/schema; conditional policy; resume manifest truth; child-owned detached completion; kill semantics.
- Restrictions overridden: none silently; the narrowly affected operator limitation guidance would require updating alongside implementation.
- Rescued release documents are advisory, not current authority; mtime-current docs are not automatically semantically accurate.

## Diagnosability Context

**Verdict**: partial
**Complexity classification**: trivial (score1)
**Captured-bytes (failing run)**: JSONL1559, Markdown999; contract4825 and state104 are artifacts, not log bytes.
Dispatch events and persisted state/contract reach disk but do not prove marker publication. The parent directly captured absence after real successful foreground and resume commands. No production instrumentation or log-level override is needed for this deterministic omission. No required diagnostic measurement remains pending. Full card: ./diagnosability-context.md; informational tasklist: ./diagnosability-tasklist.md.

## Diagnosis

**Root cause**: The foreground and resume CLI completion continuations never invoke the existing done-marker writer.

**Cause class**: Other: missing completion-policy integration.

**Detailed explanation**: The normal shortcut explicitly enables the completion flag. The CLI reduces workers and writes terminal state, but discards the returned contract instead of using its status to publish the marker. Resume has a separate continuation with the same omission. The reducer writes the contract and returns it; direct helper tests therefore cannot establish that the CLI publishes a marker. This conclusion combines full continuation inspection with real CLI artifacts, not a failing worker fixture or an assumed library behavior.

The runtime claim is scoped to successful foreground and all-workers-skipped resume. Detached delegates to the normal CLI in a child by source inspection only; failure/partial execution and arbitrary original runtime-policy recovery on resume were not reproduced. No control arm, unique enum-producer partition or environment-difference inference is claimed.

## Evidence

Source paths resolve against the worktree root; ./ paths resolve beside this report.

1. `src/superclaude/cli/swarm/commands.py:2145-2178`: bare `reduce_wave3(...)`, then `_write_swarm_state(...)` with `"terminal"`, then `raise click.exceptions.Exit(EXIT_OK)`, without marker publication.
2. `src/superclaude/cli/swarm/commands.py:2578-2599`: resume reduces, calls `_write_swarm_state(output_path, "terminal", manifest_obj.job_id)`, and exits without invoking the marker writer.
3. `src/superclaude/cli/swarm/models.py:563-573`: source policy says `write_done_sentinel=True` writes on terminal status; the field default is `write_done_sentinel: bool = True`.
4. `src/superclaude/cli/swarm/commands.py:931-937`: fresh lens shortcut sets `"write_done_sentinel": True`.
5. `src/superclaude/cli/swarm/reduce.py:701-704`: `emit_contract(contract, Path(output_dir))` then `return contract`; existing marker writer is defined separately at `src/superclaude/cli/swarm/reduce.py:383-440`.
6. `./artifacts/foreground-check.json:1`: captured `{"done_exists": false, "state": "terminal"}` after the real foreground CLI; `./artifacts/foreground/return-contract.yaml:2`: `status: success`.
7. `./artifacts/resume-check.json:1`: captured `{"done_exists": false, "state": "terminal"}` after the separate real resume; `./artifacts/resume/return-contract.yaml:2`: `status: success`.
8. `./artifacts/foreground.stdout.txt:1`: `swarm run: dispatched job (mode=lens, workers=3, results=3)`; `./artifacts/resume.stdout.txt:1`: `swarm run --resume: job_id=lens-bare-review-0a1cf709 workers=3 skipped=3 redispatched=0`. Exact command/exit provenance is retained in tier1-observation.md.
9. `./artifacts/import-paths.txt:1-2`: both imported modules resolve inside this worktree, not another checkout.
10. `./artifacts/baseline-tests.txt:7`: `25 passed in 0.59s`, existing writer/CLI tests only. The public-entrypoint marker-presence oracle deliberately failed with exit1: `./artifacts/negative-witness.txt:3-5` records `AssertionError: completion marker missing after real foreground CLI success`.

## Proposed Fix

Supported proposal only, not execution advice while this report is blocked: retain the returned contract, finish terminal-state persistence, then call the existing marker writer with the persisted contract path and actual status when effective completion policy enables it. Apply consistently to the two owning continuations; detached publication remains the child's responsibility. Do not add an independent marker format or duplicate contract emission.

Candidate files: src/superclaude/cli/swarm/commands.py, matching CLI regression tests, and the directly affected docs/swarm completion guidance. Do not expand into stdout policy, unrelated caller/lens metadata recovery, or the pre-existing issue501 plan.

Repair acceptance still needed: new CLI marker assertions must fail before the fix and pass afterward; check valid matching marker/status/path, enabled/disabled policy, completion order, successful foreground/resume, partial/failed terminal outcomes, and supported detached child execution. Preserve existing atomic-writer and kill behavior. No new test name or passing repaired result is invented here.

Apply with: withheld. The success-only --fix planning offer cannot run while the closure blocker remains. No automatic rerun, audit bypass or speculative implementation is recommended.

## Risk + Rollback

Early/stale markers can falsely signal completion; assumed success mislabels partial/failed outcomes; ignoring the flag breaks opt-out; referencing a nonexistent contract is invalid. Use fresh isolated output roots for acceptance. Existing tests pass but do not pin this missing CLI publication. No product change was applied, so there is nothing from this diagnosis to revert. Preserve all evidence and unrelated staged work.

## Follow-up tasks

None proposed outside this issue. Incomplete resume recovery is recorded as a scope limit, not silently repaired or filed as a new issue.

## Grounding Gaps

- NOT PROVEN: fix-applied real CLI positive witness and repaired ordering. This keeps hardening closure blocked regardless of diagnosis confidence.
- Detached tmux execution, failure/partial CLI outcomes, disabled policy and redispatch completion were not runtime-tested here.
- Original runtime overrides on resume are not claimed preserved; source recovery is incomplete.
- Historical rescued release authority is unverified; current source wins over contradictory doc descriptions.
- Shared diagnosability-rounds.json changed externally during the run; this session never wrote or reverted it. Existing issue501 task packages were preserved.
- Optional behavior-definition input was absent because no unobserved external primitive assertion was load-bearing; calibrator recorded its skipped check.

## Next Steps

There are zero pending diagnostic measurement rows. The missing repair-closure evidence is a fix-applied public-entrypoint marker check paired with the retained pre-fix failure, plus the stated acceptance cases. No diagnostic rerun can create that repaired witness without separately authorized implementation.

Protocol ambiguity, not a proven workflow deadlock: `/home/coder/.claude/skills/sc-troubleshoot-protocol/SKILL.md:582` requires report success and acceptance for the planning offer. `/home/coder/.claude/skills/sc-troubleshoot-protocol/refs/runtime-entrypoint-verification.md:22-28` requires negative/positive witnesses for green runtime closure, but defines no pending pre-fix diagnostic state. `/home/coder/.claude/skills/sc-troubleshoot-protocol/refs/hardening-output-contract.md:34-39,54` separates closure verdicts from downstream success rendering and allows rationalized N/A to produce advisory; it does not expressly map ordinary hardening FAIL to diagnostic report status blocked. This run chose HC1 FAIL plus report blocked conservatively, and therefore did not enter the success-only offer. An alternative interpretation could treat pre-fix positive proof as rationalized N/A and retain advisory closure while planning. That alternative is acknowledged, not silently selected and not used to clear the existing failure. Human guidance is needed on the pre-fix interpretation before changing this route. Any separately authorized plan must retain the missing positive evidence as mandatory acceptance, not represent repair closure as passed. No commit, push, PR, issue comment or merge is authorized by this report.

## Audit

Hypothesis: ./tier1-hypothesis.md. Independent calibration: ./tier1-calibration.md (six scores and nine structural rows validated; STOP at Tier1). Audit: ./audit.log. No Tier2 debate, remediation acceptance, task plan or implementation occurred. Independent evidence validation and off-path diagnostic review PASS after one correction cycle:19 source/artifact spans verified, zero dropped, two recorded command results passed through without re-execution. No A-rule contribution; skipped optional-input checks retained. The corrected protocol-interpretation claim was rechecked; initial draft/review retained in artifacts/. Non-blocking citation/provenance/format notes remain recorded in ./evidence-validation.md, not treated as repair blockers.

## Pipeline Hardening Closure

**Applicable**: true
**Closure verdict**: blocked
**Waiver status**: none
**Backtest status**: not_run
**Off-path review**: performed (independent diagnostic review PASS; not product repair approval)

- HC0: PASS: CLI, persisted-state, artifact and sibling boundaries recorded in hardening-applicability.md.
- HC1: FAIL: real pre-fix negative witness, but no fix-applied positive witness.
- HC2: PASS: bounded nonempty consumer/sibling classification in contract-ledger.md, not proof of repair.
- HC3: N/A: no behavior-controlling prose classifier; source sibling sweep recorded.
- HC4: N/A: explicit evidence paths, no indirect review selector.
- HC5: PASS: independent diagnostic review completed and its blocking interpretation finding was corrected and rechecked; no waiver.

Evidence cards: ./runtime-entrypoint.md, ./contract-ledger.md, ./unmask-sweep.md, ./effective-input.md. Known escapes caught: none claimed.

NOT PROVEN: failed hardening wave HC1. Completed evidence review does not manufacture the missing positive runtime proof. Backtest coverage was not run, and no production-health signoff is made.

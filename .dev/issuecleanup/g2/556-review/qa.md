VERDICT: FAIL
# QA Source Fidelity - Issue 556 independent review

- **Topic:** Findings and architecture analysis for issue 556
- **Date:** 2026-11-24
- **Phase:** source-fidelity
- **Fix cycle:** Initial review / 2
- **Template:** /home/coder/.claude/templates/modularization-template-review/qa-source-fidelity_template.md; first-line verdict required by dispatch.

## Sources Reviewed

| Source Doc | Assigned Section Range | Line Count |
|------------|------------------------|------------|
| /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/.dev/issuecleanup/g2/556/findings.md | Entire findings report | 39 |
| /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/.dev/issuecleanup/g2/556/analyze/analyze-report.md | Entire architecture analysis | 30 |
| https://github.com/IronbellyOrg/IronClaude/issues/556 | Full body and all four comments, including the November 18 hold | GitHub JSON, no source lines |
| https://github.com/IronbellyOrg/IronClaude/issues/563 | Full body, all comments, assignment and board status | GitHub JSON, no source lines |
| https://github.com/IronbellyOrg/IronClaude/issues/564 | Full body, all comments, assignment and board status | GitHub JSON, no source lines |
| https://github.com/IronbellyOrg/IronClaude/issues/565 | Full body, all comments, assignment and board status | GitHub JSON, no source lines |

Repository evidence checked directly: runner preview and execution branch; command configuration and exception handling; ensemble transport selection, scorer selection and prompt construction; missing-credential exception construction; user and manual testing guides; convergence gates; existing stub integration tests; and process argument construction. All repository paths below are absolute. No product file was changed.

## Per-Source Fidelity

| Source | Semantic Coverage | Detail Preservation | Phantom-Coverage Check | Operational Completeness | Verdict |
|--------|-------------------|---------------------|-----------------------|--------------------------|---------|
| Issue 556 and split issues | All three reported defects remain supported in current source | The grouped-record role and owner hold are preserved; the explicit synthetic-score restriction is omitted | No repair or fresh-run proof claimed; complexity and size remain unsupported estimates | Missing a required constraint in the proposed in-process scorer route | FAIL |
| /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/.dev/issuecleanup/g2/556/findings.md | Core defect verdict is sound | The open/backlog/unassigned status and closure order match GitHub; scorer acceptance detail is lost | Source supports dispatch, not actual authentication or billing; effort classifications lack a derivation | One blocking omission; minor estimation follow-up | FAIL |
| /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/.dev/issuecleanup/g2/556/analyze/analyze-report.md | Execution, preview and exception paths match source | Correctly separates expected credential failure from unexpected exceptions | Historical graph counts and name-lookup history are UNVERIFIED | The same scorer recommendation omits the issue's explicit restriction | FAIL |

### Claim-by-claim checks

1. **Preview mismatch, verified.** /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/cli/reflect/commands.py:254-257 accepts only standard/deep and defaults to standard. /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/cli/reflect/runner.py:536-542 selects the ensemble at both depths with the production process class. Its preview instead prints the slash prompt at lines 647-662, composed at lines 452-481. The scorer prompt is `/sc:adversarial` in /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/cli/reflect/ensemble.py:582-598. Preview returns before launching. The tier-1 launch at runner.py:544-570 is reachable with other programmatic depths or a substituted class; the reports' shipped-command claim is correct for its accepted depths.
2. **Missing-credential mismatch, verified from source, not rerun.** /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/cli/reflect/ensemble.py:333-338 resolves the transport before dispatch; its non-stub factory delegates at lines 176-181. /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/cli/swarm/transports/openai_compat.py:219-228 raises TransportEnvError when required values are absent. /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/cli/reflect/commands.py:442-469 writes blocked/runner-error on a best-effort basis and re-raises, bypassing the normal verdict exit path at lines 470-484. /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/docs/guides/reflect-cli-tools-guide.md:361-374 promises verdict-code consistency and blocked exit 2. The bare uncaught RuntimeError supports exit 1 under ordinary Python execution; installed-console execution remains UNVERIFIED.
3. **Stub scorer dispatch, verified with qualifications.** /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/cli/reflect/ensemble.py:169-174 only replaces reviewer transport. Lines 423-435 run the real scorer when two reviewers survive, no convergence score is already supplied and no scorer function is injected; lines 537-553 construct and start the genuine process. The reports omit the pre-supplied-score exception in their shorthand, but the ordinary CLI supplies neither seam, so the reported product defect remains valid. This proves an attempted subprocess launch, not a successful authenticated session or a bill.
4. **Documentation mismatch, verified.** /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/docs/guides/reflect-cli-tools-guide.md:134-139 promises credit-free stub use and lines 361-374 promise verdict exits. /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/docs/testing/v5.0.0/user/D12-reflect.md:15,26-30 explicitly records the real scorer and credential traceback exceptions. All three deviations are acknowledged by the testing guide, not repaired by that acknowledgement.
5. **Argument preview and thin-wrapper description, supported.** /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/cli/reflect/runner.py:439-445 delegates verdict logic, and lines 483-507 hand-build the preview. /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/cli/pipeline/process.py:134-166 builds the real restricted-review argument list in matching order. Drift is a maintenance risk, not a newly demonstrated argument mismatch.
6. **Current disposition, verified.** GitHub reads show issue 556 open, unassigned and Backlog, as are 563, 564 and 565. The November 18 comment expressly states Low/lowest priority, no current use and no work until the wrapper is used again. Keeping the grouped issue open until its three children are resolved or consciously dropped matches the November 17 comment. These facts support still-relevant plus hold, not permission to implement.
7. **Change history, verified.** Local HEAD is a7ae3dd30. The latest touching commit across the three named files is 2ca022bf7; local diff inspection and GitHub pull request 653 show route re-pointing, not a fix for these three defects. The all-state pull request search for the four numbers returned unrelated merged pull requests 622, 202 and 113, not a defect repair. Absolute absence of a pull request under unrelated wording is UNVERIFIED; no new fetch was performed.
8. **Complexity, size and priority, partly supported.** Three defects, several implementation files, guides and regression needs are real. That file count does not itself establish complex or L; neither report gives hours, a size rubric or a subsystem-based derivation. Low priority and the hold are explicit owner decisions; the exact numeric mapping to P3 is UNVERIFIED. The universal statements that nothing depends on these defects and no current work is blocked are UNVERIFIED beyond the owner saying the wrapper is not used.
9. **Related issues and graph metrics, limits preserved.** The findings correctly marks the current states of 354 and 571 UNVERIFIED. Their current state is not needed to respect the hold and was not re-read. The analysis's historical 3,651-file/245-symbol graph snapshot, per-file counts and prior lookup mismatch were not independently reproduced and remain UNVERIFIED. Source reads, not those counts, establish the defect conclusions.

## Overall Verdict: FAIL

FAIL because both proposed next-step summaries omit an explicit acceptance constraint on synthetic scores while recommending an in-process stub scorer. The still-relevant defect verdict and the owner's backlog hold are supported; this is a failure of recommendation completeness, not a finding that the three reported defects are stale. One blocking finding, one non-blocking Medium sizing follow-up and qualification notes are recorded below.

## Issues Found

### Blocking finding 1: The proposed in-process stub scorer drops an explicit acceptance safeguard

- **Grade:** Blocking (Missing and Decision). The affected action is the future recommendation to replace the live scorer with an in-process scorer, not work authorized now.
- **Locations:** /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/.dev/issuecleanup/g2/556/findings.md:18 and /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/.dev/issuecleanup/g2/556/analyze/analyze-report.md:27.
- **Evidence:** Issue 556's Done when section explicitly says, "Synthetic scores must never certify real-model convergence," and requires model-free integration regressions. Issue 565 repeats that restriction. Both reports propose "score the stub path in-process" but neither carries the restriction forward or calls for a regression protecting it. The findings mentions a regression per defect at line 21, but does not preserve this acceptance condition.
- **Code evidence and consequence:** /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/cli/reflect/contract.py:298-326 treats a non-null finite score of at least 0.80 as satisfying the convergence checks. /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/tests/cli/reflect/test_ensemble_stub_integration.py:38-60 supplies a synthetic 0.86 and clean flags; lines 108-121 feed that seam into the real reducer and verdict derivation, and lines 160-169 assert PASS/0. That is legitimate test-only evidence, not live convergence. Promoting this test arrangement into ordinary CLI behavior without a synthetic-result boundary can manufacture a normal audit PASS. Correcting the reports changes a named required behavior and acceptance check for their recommended solution.
- **Required correction:** Carry the explicit synthetic-versus-real convergence restriction into both recommendations and require a model-free regression that protects that distinction if an in-process scorer is chosen. Preserve the existing alternative of accurately documenting live scorer dispatch. Keep the owner's no-implementation hold unchanged.

### Follow-up candidates (minor, do not drive the FAIL)

1. **Medium: Complexity and size are asserted without a reproducible estimate.** /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/.dev/issuecleanup/g2/556/findings.md:20-21 calls the work complex/L on the basis of three defects, file count and regression needs. It gives no hour estimate, size definition, cross-subsystem explanation or uncertainty label. These facts justify several coordinated edits, but not a specific complexity or size class. Consequence: a later planner cannot reproduce the sizing. No current dispatch or staffing decision based on this estimate was established, so this does not fail the review. Record an explicitly provisional estimate with its basis when this issue is actually planned; do not invent a replacement class here.

### Notes (form or qualification only)

- The analysis's High/High/Medium labels describe individual defect impact, while the owner's Low/P3 is scheduling priority for an unused, frozen area. Those are different dimensions, not a contradiction. The issue's exact numeric priority mapping was not independently verified.
- "Stub mode is not credit-free" should be read as "stub mode can dispatch a live scorer, so a credit-free guarantee is unsupported." The issue expressly disclaims proof of billing/authentication/network inference; this review likewise makes no such claim.
- Broad statements such as "any exception" leave out sidecar-write failure and special exception-to-exit handling. The code explicitly treats sidecar output as best-effort. This does not change the verified missing-credential defect or the requested remedy.
- The issue's shifted citation ranges do not change the underlying claims and are not blocking.

## QA Complete

Completed the requested independent review of both inputs against the live issue and comments, related split issues, source branches, guide promises, change history and existing test oracles. No implementation, model invocation, test execution, installation, commit, staging or GitHub mutation was performed. Only this task's report directory was written.

Verification limits: original retained capture files were not opened; no installed-console exit or live billing claim was reproduced; historical graph metrics and lookup history remain UNVERIFIED. The related current states of issues 354 and 571 and the universal no-dependent-work assertion remain UNVERIFIED. The initial report-directory lookup found no directory because outputs had not yet been created. The first incremental Edit was blocked by the freshness hook because a newly written file had not been Read; a tracked Read resolved it before the Edit was retried. Final dedicated placeholder-search and directory-list attempts failed with EACCES spawning rg; direct Reads remained available and confirmed the closing verdict and completion records. These tool-level recoveries do not establish product behavior.

VERDICT: FAIL

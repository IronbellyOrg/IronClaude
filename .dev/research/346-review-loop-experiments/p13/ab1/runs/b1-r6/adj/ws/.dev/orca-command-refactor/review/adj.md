# Adjudication of findings X1-X23

Spec: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md` (cited below as `SPEC:<line>`).
Inventories: `inventory/commands-a.md` (`INV-A:<line>`), `inventory/commands-b.md` (`INV-B:<line>`).

Test applied to each finding: "An implementer who follows the stated text as written builds X, and X is wrong because Y." A finding is confirmed only if that sentence holds with no further assumption.

Limits of this check: the workspace holds only the README, the spec and the three inventories. No command, skill or `CLAUDE.md` source file is present, and the sandbox home directory is empty. Any claim about what a command file contains today is UNVERIFIED here.

Result: 1 confirmed (X12), 1 unsure (X8), 21 rejected.

## Confirmed

### X12: confirmed
An implementer who follows the load row as written changes only load's Usage line and gives it no report file (`SPEC:112`, `SPEC:265`), and that is wrong because the P1 checks cannot then pass.
- AC-1.1 requires every command in sections 3.1-3.2 to have a `## Unattended mode` section naming `return-contract.yaml` (`SPEC:195`). Load is in section 3.2.
- AC-1.2 runs the 7.2 live check on "each P1 command" with `--unattended --output <dir>` and requires all steps to pass (`SPEC:196`). Load is listed as a P1 command (`SPEC:159`). Step 4 is `test -s <contract>` (`SPEC:183`), and load writes no contract.
- The same row says load is not to be its own Task (`SPEC:112`), while the 7.2 check creates a Task for it (`SPEC:180`).

Following the checks instead breaks the recorded decision that a report file for load "would be an unrequested addition" (`SPEC:265`). The two texts cannot both be followed, so the spec must exempt load from AC-1.1 and AC-1.2 or change the load row.

## Unsure

### X8: unsure
The spec row says to add `--output` (`SPEC:120`), and the inventory says no path or `--output` flag exists today (`INV-B:43`, `INV-B:182`). The finding says the command already has both under `--report-dir`. `cmd/spec-panel.md` is not in the workspace, so that premise cannot be checked. If it is true, the row would add a duplicate flag. If it is false, the row is correct.

## Rejected

### X1: rejected
E3 (`SPEC:23`) and section 1.4 (`SPEC:43`) do disagree on how strong the precedent is. That is a wording inconsistency in the rationale. No implementation step depends on it, and Phase 0 tests the direct route live before anything is built (`SPEC:158`, `SPEC:194`).

### X2: rejected
The coordinator's handling of `partial` and `blocked` is not spelled out in section 2.3 (`SPEC:73`). That is an omission, not text that produces a wrong build. Building a coordinator is a non-goal (`SPEC:215`); WC-3 and WC-5 define the worker side (`SPEC:61`, `SPEC:63`).

### X3: rejected
Remediation runs only when `--remediate` is passed explicitly, and the brief is told not to pass it (`SPEC:88`). The headless rule is existing behaviour that auto-accepts only auto-fixable registers (`INV-B:109`) and is kept unchanged by SA-6 (`SPEC:151`). Remediation is a local handoff, not an outward action under WC-9 (`SPEC:67`). Calling this wrong needs the assumption that D2's Ruling rule extends to reflect, which the spec does not state.

### X4: rejected
The finding itself asks for no action. The evidence-validator pass (`SPEC:285`) is a provenance note and no implementer step depends on it.

### X5: rejected
The two rows are consistent. `/sc:agent` is coordinator-only (`SPEC:132`), so its frontmatter defect cannot stop a worker and falls outside scope under 8.8 (`SPEC:220`). business-panel is a worker command, and SA-4 names its frontmatter fix (`SPEC:149`).

### X6: rejected
The 1.1 summary sentence (`SPEC:16`) is less complete than SA-4 (`SPEC:149`) and section 3, which state the defect fixes explicitly. An implementer following section 3 builds the right thing.

### X7: rejected
The pr-submit work is conditional everywhere it is scheduled: P4 applies "the answers to D2-D4" (`SPEC:162`), AC-4.3 starts "If D3 allows" (`SPEC:210`), and section 4 says it stays a worker candidate depending on D3 (`SPEC:139`). The 10 / 27 / 6 count is a label on an open decision. Not part of this finding, but AC-1.1 requires an Unattended section for pr-submit in P1 regardless of D3 (`SPEC:195`), which the revision should review.

### X9: rejected
Same substance as X1. The Agent-tool caveat is stated in 1.4 (`SPEC:43`), WC-7 forbids that route (`SPEC:65`), and AC-0.4 proves the direct route (`SPEC:194`). No build step follows from E3.

### X10: rejected
WC-4 fixes the contract at `<output-dir>/return-contract.yaml` with the directory passed by the coordinator (`SPEC:62`), and P1 adds "output flags for commands that lack one" (`SPEC:159`). A row that says only "contract" inherits that rule. The finding holds only if the implementer ignores WC-4.

### X11: rejected
The heading says the commands run "if the brief uses the stated flags" (`SPEC:79`), and the tdd row requires a precise prompt and schedules the remaining gate fix for P2 (`SPEC:90`). The complaint is about the label "ready"; no wrong build follows. The P0 smoke runs do not use tdd (`SPEC:158`).

### X13: rejected
The review-translation row tells the implementer to add the context input and a resume input (`SPEC:117`); leaving the flag name to the implementer is underspecification, not a wrong build. AC-2.2's cli-eval case runs with no `--suite` and expects blocked (`SPEC:200`), which does not depend on the flag existing today. Whether `--suite` exists today is UNVERIFIED (`INV-A:44` proposes it as the non-interactive form).

### X14: rejected
Same substance as X11, for tdd and release-split (`SPEC:89-90`). The rows name the remaining prompts and resolve them as blocked in P2.

### X15: rejected
The spec row restricts cli-portify dispatch to an IronClaude checkout (`SPEC:105`) and does not add a new source-path lookup. The repo rule's allowed list is said to name commands that operate on this repo's own source; `CLAUDE.md` is not in the workspace, so that is UNVERIFIED here, but the finding needs the opposite assumption to hold.

### X16: rejected
The contract file is installed by the normal core-file install path (`SPEC:52`), checked by AC-0.1 (`SPEC:191`). A missing-file case needs the assumption that the install was skipped or failed.

### X17: rejected
The `\|` sequences in AC-C1 are markdown table-cell escapes. The same escape appears on the shell pipe to `grep -v` in that cell and in AC-C4 and AC-C5 (`SPEC:172`, `SPEC:175-176`), so the rendered command has plain `|` and the pattern alternates correctly. The second half (core files may legitimately contain a matching Orca command) needs an assumption about what the new HOW-WE-WORK section and contract file will say; the revision may still want to exclude those two files.

### X18: rejected
Fan-in over a subset of reports is coordinator planning behaviour (`SPEC:39`), and building a coordinator is a non-goal (`SPEC:215`). No command or contract text is built wrong.

### X19: rejected
"File location unnamed" in the cli-portify row describes today's state (`SPEC:105`). WC-4 supplies the location (`SPEC:62`), and AC-1.1 checks only that the section names `return-contract.yaml` (`SPEC:195`).

### X20: rejected
The live checks fail only if the tester has not installed the contract file and the worker cannot proceed without it. Both are assumptions about the test machine. The P0 smoke runs do not use `--unattended` (`SPEC:194`).

### X21: rejected
Step 2 requires `worker-show` at least once per 5 minutes (`SPEC:181`), so a coordinator that never looks has not run the step. A null or absent `agentWait` meaning "not waiting" is the intended reading.

### X22: rejected
This is a request for an extra check. AC-0.1 covers registration (`SPEC:191`), and the P1 and P2 live runs exercise the commands' Unattended sections. Nothing is built wrong.

### X23: rejected
The clobber needs the assumption that a coordinator dispatches two index-repo workers into one worktree at the same time. WC-11 already binds the command's default output paths (`SPEC:69`). The index-repo row (`SPEC:86`) lacks the one-per-worktree note that the cleanup-audit row carries (`SPEC:85`); adding it would be a cheap clarification.

```adj-v1
{"x": "X1", "verdict": "rejected", "reason": "E3 and section 1.4 disagree only in rationale wording; no build step depends on it and Phase 0 tests the direct route live."}
{"x": "X2", "verdict": "rejected", "reason": "Coordinator handling of partial and blocked is an omission in a non-goal area, not text that makes an implementer build something wrong."}
{"x": "X3", "verdict": "rejected", "reason": "Remediation runs only with an explicit --remediate flag under an existing headless rule kept by SA-6, so calling it wrong needs the assumption that D2's rule extends to reflect."}
{"x": "X4", "verdict": "rejected", "reason": "The finding asks for no action and no implementer step depends on the evidence-validator note."}
{"x": "X5", "verdict": "rejected", "reason": "agent is coordinator-only so its frontmatter defect cannot stop a worker, while business-panel is a worker command and SA-4 names its fix."}
{"x": "X6", "verdict": "rejected", "reason": "The 1.1 summary is incomplete but section 3 and SA-4 state the defect fixes explicitly, so nothing wrong is built."}
{"x": "X7", "verdict": "rejected", "reason": "Every scheduled pr-submit step is conditional on D3 (P4 scope, AC-4.3, section 4), and the 10/27/6 count is only a label on an open decision."}
{"x": "X8", "verdict": "unsure", "reason": "The row matches the inventory, and the claim that the command already has the flag under --report-dir cannot be checked because the command file is not in the workspace."}
{"x": "X9", "verdict": "rejected", "reason": "Same as X1: the Agent-tool caveat is stated in 1.4, WC-7 forbids that route and AC-0.4 tests the direct route."}
{"x": "X10", "verdict": "rejected", "reason": "WC-4 fixes the contract at the coordinator-passed output directory and P1 adds output flags where missing, so the finding holds only if WC-4 is ignored."}
{"x": "X11", "verdict": "rejected", "reason": "The heading is conditional on the stated brief flags and the rows schedule the remaining gate fixes for P2, so only the label is disputed."}
{"x": "X12", "verdict": "confirmed", "reason": "The load row and Decisions table give load no Unattended section, no contract and no Task, while AC-1.1 and AC-1.2 require all three of load as a section 3.2 and P1 command, so P1 cannot pass as written."}
{"x": "X13", "verdict": "rejected", "reason": "The rows tell the implementer to add the missing inputs, which is underspecified naming rather than a wrong build, and the AC-2.2 case works whether or not --suite exists today."}
{"x": "X14", "verdict": "rejected", "reason": "Same as X11: the tdd and release-split rows name the remaining prompts and resolve them as blocked in P2."}
{"x": "X15", "verdict": "rejected", "reason": "The row adds no new source-path lookup and limits dispatch to an IronClaude checkout, and the finding needs an unverified reading of the repo rule to hold."}
{"x": "X16", "verdict": "rejected", "reason": "A missing contract file needs the assumption that the normal core-file install was skipped or failed."}
{"x": "X17", "verdict": "rejected", "reason": "The escaped pipes are markdown table-cell escapes used on every pipe in those cells, and the core-file overlap needs an assumption about text not yet written."}
{"x": "X18", "verdict": "rejected", "reason": "Fan-in over a subset of reports is coordinator planning, which the spec lists as a non-goal, and no command or contract text is built wrong."}
{"x": "X19", "verdict": "rejected", "reason": "The row describes today's state, WC-4 supplies the location and AC-1.1 checks only the filename."}
{"x": "X20", "verdict": "rejected", "reason": "The live checks fail only under assumptions about the test machine's install state."}
{"x": "X21", "verdict": "rejected", "reason": "Step 2 requires worker-show at least once per 5 minutes, so a coordinator that never looks has not run the step."}
{"x": "X22", "verdict": "rejected", "reason": "It asks for an additional check and identifies nothing that is built wrong."}
{"x": "X23", "verdict": "rejected", "reason": "The overwrite needs the assumption of two concurrent index-repo workers in one worktree, and WC-11 already binds the command's output paths."}
```

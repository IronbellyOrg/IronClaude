# Findings to adjudicate

### X1

- anchor: "These run as workers now if the brief uses the stated flags"
- anchor2: "The only end-to-end proof is the PR #329 run"
- refs: 1.4, 3.1
- claim: The ready-today claim overstates evidence the spec itself says is missing, and tdd can stall mid-run on a /task question.

### X2

- anchor: "--unattended --output .dev/troubleshoot/login/"
- anchor2: "| troubleshoot | no `--fix` |"
- refs: -
- claim: The D1 example passes --output to troubleshoot, but section 3.1 lists no output flag for it and the inventory names only a default folder.

### X3

- anchor: "so a command run by a worker has the same tools as a command a person runs"
- anchor2: "`CAPS:161` (`[H:worker-start]` line 38, `--agent claude`)"
- refs: -
- claim: E2 asserts tool parity that the cited evidence (top-level session only) does not show.

### X4

- anchor: "add `--output`; contract"
- refs: -
- claim: The row may be stale against a command definition that already has --output and --report-dir.

### X5

- anchor: "because the rule exists to stop an agent approving its own work"
- anchor2: "follow the existing headless auto-accept rule instead of the"
- refs: SA-6
- claim: Unattended reflect and tasklist auto-accept remediation by the same agent that found the defects, which D2's rationale forbids for Rulings, and the spec does not decide it.

### X6

- anchor: "prints nothing (SA-2, WC-8)"
- refs: P0, SA-2, WC-8
- claim: AC-C1 scans core/ where P0 adds Orca text and misses orca status/open/skills.

### X7

- anchor: "Its job is git itself"
- refs: 4
- claim: The git row uses a run-level constraint as command evidence.

### X8

- anchor: "What changes in the commands is limited to the worker contract in section 2"
- anchor2: "Existing lines change only where section 3 names a defect fix"
- refs: 1.1, 3.2, SA-3, SA-4
- claim: A reader who trusts 1.1 underestimates the 27 command edits that change gate behaviour and drift.

### X9

- anchor: "It is testable by grep and cannot misfire on a person."
- anchor2: "a person never types it"
- refs: 2.1
- claim: Quoted text containing the token switches unattended mode on, which the claim that it cannot misfire denies.

### X10

- anchor: "the worker reports the named file until Phase 1 adds the contract"
- anchor2: "7.2 passes with `--outcome succeeded`"
- refs: AC-1.2, AC-2.3, P1, P2
- claim: An implementer who follows the phase table builds troubleshoot, tdd and release-split workers with no contract, so AC-2.3 fails on 7.2 step 4 for them.

### X11

- anchor: "exits 0 (SA-5)"
- refs: SA-5
- claim: Section 7 lets a new Unattended-mode section ship with a hard-coded src/superclaude path because no check catches it.

### X12

- anchor: "`<output-dir>` is the directory the coordinator passed (`--output` / `--output-dir`)"
- anchor2: "a precise component prompt, not a bare topic; `--output <file>`"
- refs: 2.1, 2.3, 3.1, 3.2, 7.2, AC-0.4, AC-1.1, AC-1.2, AC-2.2, AC-4.3, P0, P1, P2, P3, P4, WC-1, WC-10, WC-12, WC-2, WC-3, WC-4, WC-5, WC-6, WC-7, WC-9
- claim: WC-4 builds the contract path under a directory taken from --output, but tdd and init-lite pass --output as a file, so the contract is written under a regular file and the AC-2.2 contract check cannot pass.

### X13

- anchor: "any default that pushes, opens a PR, posts to GitHub, installs, provisions or calls a paid external run is off"
- refs: WC-9
- claim: An unattended reflect or cleanup worker moves or edits local files with no rule limiting them.

### X14

- anchor: "a coordinator brief template listing the section 3.1 flags"
- refs: 2.3, P0
- claim: The promised brief template is not specified beyond the list in 2.3, so the coordinator's briefs will differ per run.

### X15

- anchor: "git diff -U0 master...HEAD -- src/superclaude/commands/<name>.md \\| grep -E '^-[^-]'"
- refs: AC-0.3, SA-1, SA-4
- claim: The additive-edit check ignores deleted lines that begin with a dash because diff shows a deleted '- b' as '-- b', so an implementer deleting a bullet or --- line passes AC-C5.

### X16

- anchor: "stays a worker candidate only if the user accepts open decision D3"
- refs: 3.2
- claim: pr-submit is counted as a needs-change worker while the recommended D3 makes it coordinator-only.

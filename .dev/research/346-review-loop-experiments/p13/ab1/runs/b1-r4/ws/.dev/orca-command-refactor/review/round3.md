review: 3 of 3
# Merged review 3 (coordinator script; panel of 1 reviewers)
candidate: /tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad/p13/ab1/runs/b1-r4/ws/.dev/orca-command-refactor/specs/orca-worker-contract-spec.md sha256 4e04817fb543edcb9c65e6cba29debf913eabe4a8ae7675d2f06bb264208171f
reviewers:
- t1b-1: report /tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad/p13/ab1/runs/b1-r4/ws/.dev/orca-command-refactor/review/round3-t1b-1.md, block ok true

## Ledger

| lid | status | blocking | confidence | severity | refs | reviewers |
|---|---|---|---|---|---|---|
| L1 | regressed | yes | overlap | CRITICAL | 2.1, 2.3, 3.1, 3.2, 7.2, AC-0.4, AC-1.1, AC-1.2, AC-2.2, AC-4.3, P0, P1, P2, P3, P4, WC-1, WC-10, WC-12, WC-2, WC-3, WC-4, WC-5, WC-6, WC-7, WC-9 | t1b-1, t2-1, t3-1, t3-2 |
| L2 | resolved | yes | single | MAJOR | AC-0.3, SA-1, SA-4 | t1b-1 |
| L3 | open | no | overlap | MAJOR | - | t1b-1, t3-1, t3-2 |
| L4 | resolved | yes | overlap | MAJOR | P0, SA-2, WC-8 | t1b-1, t2-1, t3-1, t3-2 |
| L5 | regressed | yes | single | MAJOR | AC-1.2, AC-2.3, P1, P2 | t1b-1, t2-1 |
| L6 | open | no | overlap | MAJOR | - | t2-1, t3-1, t3-2 |
| L7 | open | no | overlap | MAJOR | - | t2-1, t3-2 |
| L8 | open | no | overlap | MAJOR | 1.1, 3.2, SA-3, SA-4 | t3-1, t3-2 |
| L9 | open | no | single | MAJOR | WC-9 | t3-1 |
| L10 | open | no | single | MAJOR | 2.1 | t3-1 |
| L11 | open | no | single | MAJOR | SA-5 | t3-1 |
| L12 | open | no | single | MINOR | 4 | t3-1 |
| L13 | open | no | single | MAJOR | 2.3, P0 | t1b-1, t3-1 |
| L14 | open | no | single | MAJOR | 1.4, 3.1 | t3-2 |
| L15 | open | no | single | MAJOR | SA-6 | t3-2 |
| L16 | open | no | single | MINOR | 3.2 | t3-2 |
| L17 | resolved | yes | single | MAJOR | 7.2, AC-0.4, P0, P1 | t1b-1 |
| L18 | open | no | single | MAJOR | 7.1 | t1b-1 |

## Blocking findings

### L1

#### L1.t1b-1 (N1)

- claim: AC-1.2 asks for --output on every P1 command although WC-4 says cleanup-audit and index-repo have no output flag and load gets no unattended mode.
- anchor: "7.2 live check on each P1 command with `--unattended --output <dir>`"
- anchor2: "A command with no output flag (cleanup-audit, index-repo, troubleshoot)"

#### L1.t1b-1 (N3)

- claim: 2.3 says the path is known before dispatch while WC-4 lets some commands report it only afterwards.
- anchor: "the output directory, so the report path is known before dispatch (WC-4)"
- anchor2: "the coordinator learns the path from `worker_done --report-path` (L1)"

#### L1.t1b-1 (L7)

- claim: The D1 example gives an output flag to troubleshoot, which WC-4 lists as having none.
- anchor: "Example: `/sc:troubleshoot \"login fails\" --unattended --output ."
- anchor2: "A command with no output flag (cleanup-audit, index-repo, troubleshoot)"

### L5

#### L5 (open from an earlier review, not reported again in this one)

- claim: An implementer who follows the phase table builds troubleshoot, tdd and release-split workers with no contract, so AC-2.3 fails on 7.2 step 4 for them.
- anchor: "the worker reports the named file until Phase 1 adds the contract"
- anchor2: "7.2 passes with `--outcome succeeded`"

## Other findings

- L3 (MAJOR, open, overlap): The row may be stale against a command definition that already has --output and --report-dir.
- L6 (MAJOR, open, overlap): E2 asserts tool parity that the cited evidence (top-level session only) does not show.
- L7 (MAJOR, open, overlap): The D1 example passes --output to troubleshoot, but section 3.1 lists no output flag for it and the inventory names only a default folder.
- L8 (MAJOR, open, overlap): A reader who trusts 1.1 underestimates the 27 command edits that change gate behaviour and drift.
- L9 (MAJOR, open, single): An unattended reflect or cleanup worker moves or edits local files with no rule limiting them.
- L10 (MAJOR, open, single): Quoted text containing the token switches unattended mode on, which the claim that it cannot misfire denies.
- L11 (MAJOR, open, single): Section 7 lets a new Unattended-mode section ship with a hard-coded src/superclaude path because no check catches it.
- L12 (MINOR, open, single): The git row uses a run-level constraint as command evidence.
- L13 (MAJOR, open, single): The promised brief template is not specified beyond the list in 2.3, so the coordinator's briefs will differ per run.
- L14 (MAJOR, open, single): The ready-today claim overstates evidence the spec itself says is missing, and tdd can stall mid-run on a /task question.
- L15 (MAJOR, open, single): Unattended reflect and tasklist auto-accept remediation by the same agent that found the defects, which D2's rationale forbids for Rulings, and the spec does not decide it.
- L16 (MINOR, open, single): pr-submit is counted as a needs-change worker while the recommended D3 makes it coordinator-only.
- L18 (MAJOR, open, single): Copied raw, the escaped pipes make git reject the command with no stdout, so the check that no .claude path is staged can pass falsely.

## Reviser brief

Blocking finding ids: L1, L5.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL

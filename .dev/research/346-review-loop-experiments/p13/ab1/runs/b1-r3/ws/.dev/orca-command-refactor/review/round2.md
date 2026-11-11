review: 2 of 3
# Merged review 2 (coordinator script; panel of 1 reviewers)
candidate: /tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad/p13/ab1/runs/b1-r3/ws/.dev/orca-command-refactor/specs/orca-worker-contract-spec.md sha256 9cef9de023524eef0ec002f54d934b470019f03f17a77205bff3ed6600c2b9c7
reviewers:
- t1b-1: report /tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad/p13/ab1/runs/b1-r3/ws/.dev/orca-command-refactor/review/round2-t1b-1.md, block ok true

## Ledger

| lid | status | blocking | confidence | severity | refs | reviewers |
|---|---|---|---|---|---|---|
| L1 | resolved | yes | overlap | CRITICAL | 1.4, 2.3, 3.1, 6, 7.3, AC-0.4, AC-1.1, AC-1.4, AC-2.2, AC-3.2, AC-4.2, P0, P1, SA-1, WC-1, WC-10, WC-11, WC-2, WC-3, WC-4, WC-5, WC-6, WC-7, WC-9 | t1b-1, t2-1, t3-1, t3-2 |
| L2 | open | no | overlap | MAJOR | - | t1b-1, t2-1 |
| L3 | open | no | single | MAJOR | SA-1, WC-1, WC-10, WC-11, WC-12, WC-3, WC-6 | t1b-1 |
| L4 | open | no | overlap | MAJOR | - | t1b-1, t2-1, t3-1 |
| L5 | resolved | yes | overlap | CRITICAL | 5, P0, SA-2, WC-8 | t1b-1, t2-1, t3-1, t3-2 |
| L6 | open | no | overlap | MAJOR | AC-4.3, WC-10 | t1b-1, t2-1, t3-1 |
| L7 | resolved | yes | single | MAJOR | - | t2-1 |
| L8 | open | no | overlap | MINOR | - | t2-1, t3-1 |
| L9 | open | no | single | MAJOR | WC-8 | t2-1 |
| L10 | open | no | single | MAJOR | WC-2 | t2-1 |
| L11 | open | no | overlap | MAJOR | WC-9 | t2-1, t3-2 |
| L12 | open | no | single | MINOR | SA-1 | t2-1 |
| L13 | resolved | yes | overlap | MAJOR | 1.1, SA-4 | t2-1, t3-2 |
| L14 | open | no | single | MINOR | P4 | t2-1 |
| L15 | open | no | single | MINOR | AC-1.3, SA-6 | t2-1 |
| L16 | resolved | yes | single | MAJOR | P2 | t3-1 |
| L17 | open | no | single | MAJOR | 2.3 | t1b-1, t3-1 |
| L18 | open | no | single | MAJOR | WC-9 | t3-1 |
| L19 | open | no | single | MAJOR | 2.1 | t3-1 |
| L20 | open | no | single | MAJOR | 2.1, SA-4 | t3-1 |
| L21 | open | no | single | MAJOR | SA-5 | t3-1 |
| L22 | open | no | single | MAJOR | 122, WC-2 | t3-2 |
| L23 | open | no | single | MAJOR | 3.1, AC-0.4, P0, WC-4, WC-5 | t1b-1 |
| L24 | open | no | single | MINOR | 7.2, AC-0.4, P0, WC-5 | t1b-1 |

## Blocking findings

none.

## Other findings

- L2 (MAJOR, open, overlap): The claim is asserted although the task is passed as a startup argument, and it is missing from the UNVERIFIED list.
- L3 (MAJOR, open, single): WC-1, WC-3, WC-6 and WC-12 have no acceptance check, and WC-10, WC-11 and SA-1 are checked for one or two commands only.
- L4 (MAJOR, open, overlap): The --suite and --post-pr flags are not shown to exist in the inventories, and the no-command-calls-Orca premise and the 43-command scope need a re-check.
- L6 (MAJOR, open, overlap): A 270 s call obeys WC-10 and fails AC-4.3.
- L8 (MINOR, open, overlap): The depth fence covers Orca dispatch; CAPS:155 leaves whether Orca limits subagents UNVERIFIED, so E4 states more than its source.
- L9 (MAJOR, open, single): Heavy in-command fan-out such as cleanup-audit and tdd cannot be split by the coordinator, and no rule covers that case.
- L10 (MAJOR, open, single): The spec does not say what a coordinator-only command does when given --unattended, so it may wait on a person.
- L11 (MAJOR, open, overlap): Unattended reflect auto-accepts remediation, which is the self-approval that D2 forbids for implement; the bounded risk needs a decision.
- L12 (MINOR, open, single): A brief that a person pastes with --unattended silences that person's prompts, so the flag is not a safe sentinel.
- L14 (MINOR, open, single): P4 includes pr-submit although D3 (a) recommends no pr-submit change.
- L15 (MINOR, open, single): AC-1.3 calls a print-mode run a plain session, so it does not test an interactive person's session.
- L17 (MAJOR, open, single): No rule for blocked re-dispatch or for dependents of a partial Task, which Orca settles as complete.
- L18 (MAJOR, open, single): The row requires an explicit --post-pr flag that is not evidenced, while its required-change column says none.
- L19 (MAJOR, open, single): The sentinel token inside quoted prompt text is not excluded, so the cannot-misfire claim is unsupported.
- L20 (MAJOR, open, single): A command run against an install without WORKER-CONTRACT.md has no specified behaviour.
- L21 (MAJOR, open, single): The plugin mirror is not assigned to any phase and no check compares it, so it can drift while verify-sync passes.
- L22 (MAJOR, open, single): No row edits the task skill and no rule says how --unattended reaches nested skills, so tdd keeps its nested ask lines.
- L23 (MAJOR, open, single): A pre-contract Markdown report with no status can be read as failed under WC-5, so a successful P0 troubleshoot smoke run may be sent as failed.
- L24 (MINOR, open, single): P0 step 3 compares the outcome with a status that most P0 commands do not write.

## Reviser brief

Blocking finding ids: none.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: PASS

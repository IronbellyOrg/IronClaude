review: 2 of 3
# Merged review 2 (coordinator script; panel of 1 reviewers)
candidate: /tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad/p13/ab1/runs/b1-r5/ws/.dev/orca-command-refactor/specs/orca-worker-contract-spec.md sha256 88c067212b041e0b99f6fda10c231eb231ba347817f3cb28916d81f4045efd50
reviewers:
- t1b-1: report /tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad/p13/ab1/runs/b1-r5/ws/.dev/orca-command-refactor/review/round2-t1b-1.md, block ok true

## Ledger

| lid | status | blocking | confidence | severity | refs | reviewers |
|---|---|---|---|---|---|---|
| L1 | regressed | yes | overlap | CRITICAL | 2.1, 2.3, 3.1, 7.2, AC-0.1, AC-0.4, AC-1.1, AC-1.4, AC-2.2, P0, P1, P2, P4, SA-3, SA-4, WC-12, WC-2, WC-3, WC-4, WC-5, WC-6, WC-7, WC-9 | t1b-1, t2-1, t3-1, t3-2 |
| L2 | resolved | yes | overlap | CRITICAL | P0, SA-2, SA-5, WC-8 | t1b-1, t2-1, t3-1 |
| L3 | open | no | single | MINOR | - | t1b-1 |
| L4 | open | no | overlap | MAJOR | WC-11, WC-9 | t1b-1, t3-1 |
| L5 | open | no | overlap | MAJOR | WC-1 | t2-1, t3-1 |
| L6 | open | no | single | MAJOR | WC-10 | t2-1 |
| L7 | open | no | single | MAJOR | SA-4 | t2-1 |
| L8 | open | no | single | MAJOR | 3.2, WC-7 | t1b-1, t2-1 |
| L9 | open | no | single | MAJOR | 3.2 | t2-1 |
| L10 | open | no | single | MAJOR | WC-2 | t3-1 |
| L11 | open | no | single | MAJOR | - | t3-1 |
| L12 | open | no | single | MAJOR | 1.1, 2.1, SA-4 | t3-1 |
| L13 | open | no | single | MINOR | P2 | t3-1 |
| L14 | open | no | single | MINOR | - | t3-1 |
| L15 | open | no | single | MINOR | - | t3-1 |
| L16 | resolved | yes | single | MAJOR | 1.4 | t3-2 |
| L17 | open | no | single | MINOR | P1, WC-4 | t1b-1 |

## Blocking findings

### L1

#### L1.t1b-1 (N1)

- claim: WC-5 sends a P0 run with no contract to failed while AC-0.4 requires succeeded, and the spec never says WC-5 yields before P1.
- anchor: "The P0 runs have no contract, so step 3 requires exactly one `worker_done` with `--outcome succeeded`"
- anchor2: "`--outcome failed` when the contract is absent, empty or unparseable"

#### L1.t1b-1 (N2)

- claim: cleanup-audit and index-repo are P1 commands with no output option and no contract path, so an implementer must invent the path and AC-1.2's --output <dir> run cannot be issued.
- anchor: "A command with no output option gets one in its section 3 row."
- anchor2: "Name the `--pass all` final report; output dir is fixed, so one audit per worktree at a time (WC-11) (P1)"

#### L1.t1b-1 (N3)

- claim: The P0 step 3 expected report path is undefined for adversarial and has a run-time id for workflow, so the coordinator cannot state it before dispatch.
- anchor: "the section 3.1 \"Report today\" file as its report path"
- anchor2: "contract, but filename not fixed"

#### L1.t1b-1 (N4)

- claim: A contract that already has a key named status with other values cannot be kept as is and also satisfy the four-value status the checks assert (vocabulary UNVERIFIED).
- anchor: "an existing status field with other values is kept under its own name"
- anchor2: "has no `status` or a value outside the four"

#### L1.t1b-1 (N5)

- claim: Section 3.1 says only the last column changes commands while P1 adds the section to brainstorm and init-lite, and section 2.3 is silent on --unattended for P2-P4 commands.
- anchor: "The only command changes are the small fixes in the last column."
- anchor2: "section on the commands listed here and no others"

#### L1.t1b-1 (N8)

- claim: No cap on ask retries, no coordinator action for a missing worker_done, no write-before-report order, no rule for a missing contract file and no schema version.
- anchor: "On an `ask` timeout it resumes the same message ID and never creates a duplicate."

#### L1.t1b-1 (N9)

- claim: A new path per attempt is not reconciled with resume flags or with commands whose output directory is fixed.
- anchor: "its own new output directory or file path (section 2.3)"

## Other findings

- L3 (MINOR, open, single): Phase gating by user decision is stated two ways and D1 and D4 touch earlier phases.
- L4 (MAJOR, open, overlap): Reflect's default tracked-file write and folder move are not covered by any unattended rule.
- L5 (MAJOR, open, overlap): The fallback has no numeric bound, so an implementer cannot tell whether a 50 s fallback is compliant.
- L6 (MAJOR, open, single): The split trigger is 5 minutes while the rationale wants 4 minutes of margin, so a 4:30 or 5:00 call is left unsplit.
- L7 (MAJOR, open, single): The diff filter misses removed blank lines and removed lines beginning with two dashes, so non-additive edits pass.
- L8 (MAJOR, open, single): The tasklist row keeps reflect fan-out in subagents against INV-B's needs-change verdict, and its depth is not counted against the three-layer limit.
- L9 (MAJOR, open, single): The 27-command count and the pr-submit row assume D3 option (b), while the spec recommends option (a), so the classification is not stable.
- L10 (MAJOR, open, single): The tasklist HALT on needs_human_decision items has no resolution, so a tasklist worker can stop without worker_done.
- L11 (MAJOR, open, single): The tasklist nesting claim is not counted: at the depth limit the reflect Agent tool is withheld and the fan-out fails silently, and the inventory's required change is dropped without a recorded decision.
- L12 (MAJOR, open, single): The scope statement says only the contract changes commands, but §3.2 requires other changes such as the roadmap flag reconciliation.
- L13 (MINOR, open, single): Reflect is labelled ready today, but its row requires a P2 change.
- L14 (MINOR, open, single): E4 presents as evidence a point the inventory marks UNVERIFIED.
- L15 (MINOR, open, single): Many citations point to files outside the workspace, so this review could not check them.
- L17 (MINOR, open, single): Workflow ends with two contracts and the spec does not say what the new one holds on post-creation outcomes.

## Reviser brief

Blocking finding ids: L1.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL

review: 3 of 3
# Merged review 3 (coordinator script; panel of 1 reviewers)
candidate: /tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad/p13/ab1/runs/b1-r5/ws/.dev/orca-command-refactor/specs/orca-worker-contract-spec.md sha256 7a4862cc38412204ffb4afcc88a846d7268c3e6c8447b8a5b344d795ad99f4df
reviewers:
- t1b-1: report /tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad/p13/ab1/runs/b1-r5/ws/.dev/orca-command-refactor/review/round3-t1b-1.md, block ok true

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
| L18 | open | no | single | MINOR | AC-1.2, P1, WC-4 | t1b-1 |

## Blocking findings

### L1

#### L1.t1b-1 (F1)

- claim: WC-5 sends a successful troubleshoot, tdd or release-split worker run to failed between P1 and P2 because those commands only gain their contract in P2.
- anchor: "From P1 on (P0 runs have no contract and follow AC-0.4)"
- anchor2: "the worker reports the named file until Phase 1 adds the contract"

#### L1.t1b-1 (F3)

- claim: AC-0.4 says the P0 runs have no contract while section 3.1 says adversarial and workflow already write one.
- anchor: "The P0 runs have no contract, so step 3 requires exactly one `worker_done`"
- anchor2: "contract, but filename not fixed"

#### L1.t1b-1 (F4)

- claim: The troubleshoot P0 run has no brief output directory in its command line, so the report path rule has no referent for it.
- anchor: "a non-empty file inside the brief's output directory (for workflow, its package directory)"
- anchor2: "`REPORT.md` (`report_path`)"

#### L1.t1b-1 (F5)

- claim: A retry that also passes a resume flag is told both to take a new path and to reuse the earlier one.
- anchor: "its own new output directory or file path (section 2.3); a run that passes the command's resume flag reuses the earlier path"

#### L1.t1b-1 (F6)

- claim: The mapping from existing status values to the four is not given and sits beside a rule to keep existing fields.
- anchor: "a contract that already has a `status` key with other values maps them onto these four"
- anchor2: "Commands that already write a contract keep their fields and add the missing ones."

#### L1.t1b-1 (F7)

- claim: Workflow is listed as ready with a required --output while its own fix column adds that option in P1.
- anchor: "`--handoff none`; `--output <dir>`"
- anchor2: "Add `--output <dir>` and write the contract there"

#### L1.t1b-1 (F2)

- claim: No cap on ask retries, no coordinator action for a missing worker_done, no write order, no missing-file rule and no schema version.
- anchor: "On an `ask` timeout it resumes the same message ID and never creates a duplicate."

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
- L18 (MINOR, open, single): Several P1 rows say only report path, so the live check cannot tell whether the option names a directory or a file.

## Reviser brief

Blocking finding ids: L1.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL

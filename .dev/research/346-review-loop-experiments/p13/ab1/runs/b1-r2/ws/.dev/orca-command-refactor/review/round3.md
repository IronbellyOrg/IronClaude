review: 3 of 3
# Merged review 3 (coordinator script; panel of 1 reviewers)
candidate: /tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad/p13/ab1/runs/b1-r2/ws/.dev/orca-command-refactor/specs/orca-worker-contract-spec.md sha256 8fb661981967c14a5a823b50e2afa1ac31cb20523338e235d7b1b568eeb0705a
reviewers:
- t1b-1: report /tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad/p13/ab1/runs/b1-r2/ws/.dev/orca-command-refactor/review/round3-t1b-1.md, block ok true

## Ledger

| lid | status | blocking | confidence | severity | refs | reviewers |
|---|---|---|---|---|---|---|
| L1 | regressed | yes | overlap | CRITICAL | 2.3, 3.1, 3.2, 4, 7.2, AC-0.4, AC-1.1, AC-1.4, AC-2.2, AC-2.3, P0, P1, P2, P4, SA-1, WC-2, WC-3, WC-4, WC-5, WC-6, WC-7 | t1b-1, t2-1, t3-1, t3-2 |
| L2 | open | no | single | MAJOR | SA-1 | t1b-1 |
| L3 | open | no | single | MAJOR | P2, P4, WC-9 | t1b-1 |
| L4 | open | no | single | MAJOR | 1.3 | t1b-1 |
| L5 | open | no | overlap | MAJOR | 1.4, WC-1 | t1b-1, t3-1 |
| L6 | open | no | single | MAJOR | WC-1, WC-10, WC-12, WC-3, WC-6 | t1b-1 |
| L7 | resolved | yes | overlap | MAJOR | P0, SA-2, SA-5, WC-8 | t1b-1, t2-1, t3-1, t3-2 |
| L8 | open | no | single | MAJOR | SA-4 | t1b-1 |
| L9 | resolved | yes | overlap | MAJOR | 1.1, 3, AC-3.1, AC-3.3, SA-4, WC-7 | t1b-1, t3-1 |
| L10 | open | no | single | MINOR | AC-2.4 | t1b-1 |
| L11 | resolved | yes | overlap | MAJOR | WC-11 | t2-1, t3-2 |
| L12 | open | no | overlap | MAJOR | - | t2-1, t3-1, t3-2 |
| L13 | open | no | single | MAJOR | AC-4.3, WC-10 | t2-1 |
| L14 | open | no | single | MINOR | AC-1.3, SA-3 | t2-1 |
| L15 | open | no | single | MAJOR | - | t3-1 |
| L16 | open | no | single | MINOR | AC-2.2 | t3-1 |
| L17 | open | no | overlap | MAJOR | - | t3-1, t3-2 |
| L18 | open | no | single | MINOR | - | t3-2 |
| L19 | open | no | single | MAJOR | AC-0.3, P0 | t3-2 |
| L20 | open | no | single | MAJOR | SA-6, WC-9 | t3-2 |
| L21 | open | no | single | MINOR | WC-2 | t3-2 |
| L22 | open | no | single | MAJOR | P2 | t3-2 |
| L23 | open | no | single | MAJOR | - | t3-2 |
| L24 | open | no | single | MAJOR | WC-1 | t3-2 |
| L25 | open | no | single | MAJOR | - | t3-2 |
| L26 | open | no | single | MINOR | SA-1 | t3-2 |
| L27 | open | no | single | MINOR | WC-12 | t3-2 |
| L28 | open | no | single | MINOR | AC-4.3, P2, WC-10 | t3-2 |
| L29 | open | no | single | MINOR | - | t3-2 |
| L30 | open | no | single | MINOR | WC-3 | t1b-1 |
| L31 | open | no | single | MINOR | AC-1.1, AC-1.2, P1 | t1b-1 |

## Blocking findings

### L1

#### L1.t1b-1 (L31)

- claim: A new output directory on retry may leave a resume-capable command with no state to resume, depending on a reading the text allows.
- anchor: "The coordinator's retry brief names a new output directory where the command has an output flag"
- anchor2: "resumes from its on-disk state when given its resume flag"

#### L1.t1b-1 (L32)

- claim: A later non-retry run in a fixed location can leave a stale succeeded contract, and no AC checks the deletion.
- anchor: "deletes the old `return-contract.yaml` before a retry of a fixed-output command"

#### L1.t1b-1 (L33)

- claim: Existing workflow or adversarial contracts may use other status words, and WC-5 would map a good run to failed (UNVERIFIED).
- anchor: "has a `status` outside the four values [L1]"
- anchor2: "`--outcome` matching its status (succeeded for a non-empty Markdown report with no status field, WC-5)"

#### L1.t1b-1 (L36)

- claim: The workflow pre-creation exception leaves the coordinator step and WC-2 and WC-5 wording unadjusted; the exception can be read as controlling.
- anchor: "the worker puts the exact question in the first sentence of the `worker_done` body and sends no `--report-path` (WC-5)"
- anchor2: "the coordinator opens the contract and checks its `status` before any dependent Task starts"

#### L1.t1b-1 (L35)

- claim: cli-portify and save still name no contract location.
- anchor: "contract (fields already defined; file location unnamed)"
- anchor2: "contract naming the file written"

#### L1.t1b-1 (L37)

- claim: Several P1 rows name no output flag, so the live check cannot name it.
- anchor: "the output flag its section 3 row gives (`--output <dir>` or `<file>`"
- anchor2: "add a report path; contract"

## Other findings

- L2 (MAJOR, open, single): The text does not say that a quoted argument containing the text --unattended is not the switch.
- L3 (MAJOR, open, single): task commit/push, post-release and pr-submit have no named explicit flag, and the auggie-review and task authorizations sit in P2 while the spec gates only P4 on D2-D4.
- L4 (MAJOR, open, single): The join step is unspecified when blocked or failed workers leave fewer reports than workers, down to below the 2-artifact minimum of /sc:adversarial.
- L5 (MAJOR, open, overlap): The sandbox evidence does not show that a first-action question cannot block readiness when Claude receives its task on the command line.
- L6 (MAJOR, open, single): WC-1, WC-3, WC-6 and WC-12 have no acceptance check, and WC-10 is checked for pr-submit only.
- L8 (MAJOR, open, single): Adding a flag to an existing Usage line shows as a deleted line, so AC-C5 can fail on a purely additive change.
- L10 (MINOR, open, single): The count covers one page only, so an added comment on a PR with 30 or more can leave it unchanged.
- L12 (MAJOR, open, overlap): E4 states as established a fact that CAPS:155 marks UNVERIFIED and section 1.4 concedes.
- L13 (MAJOR, open, single): WC-10 splits only calls longer than 5 minutes, but AC-4.3 forbids any call over 240 s, so a 4.5-minute call passes one and fails the other.
- L14 (MINOR, open, single): SA-3 depends on a new output flag that the spec never defines, so it is unclear whether a standalone --output run writes the contract.
- L15 (MAJOR, open, single): The nesting-limit claim rests on an external doc quote and is stated as fact, while INV-B:210 and INV-B:314 mark subagent-to-agent spawning as UNVERIFIED.
- L16 (MINOR, open, single): The safety flags are never named, so an implementer must guess which flags make the run non-blocked.
- L17 (MAJOR, open, overlap): The D1 example passes --output to /sc:troubleshoot, which no section 3 row names as a flag.
- L18 (MINOR, open, single): pr-submit is counted as a worker candidate although D3 recommends coordinator-only, so the 10/27/6 counts depend on an open decision.
- L19 (MAJOR, open, single): P0 builds the contract and routing-guide edits before the smoke runs that test the decision, so a failed test leaves the edits behind.
- L20 (MAJOR, open, single): It is unstated whether --unattended triggers reflect's headless auto-accept, which runs remediation that can change code.
- L21 (MINOR, open, single): Commands point to an installed file that may be absent after a partial or older install, and no fallback is stated.
- L22 (MAJOR, open, single): The hardcoded src/superclaude template path is flagged but unscheduled, and no AC checks for such paths.
- L23 (MAJOR, open, single): Command edits can leave the plugins mirror out of step, and no AC checks the mirror.
- L24 (MAJOR, open, single): WC-1 has an owner outside every phase and no AC checks readiness.
- L25 (MAJOR, open, single): The step 2 pass also holds when the field is absent, which means Orca never looked, so a stalled worker can pass.
- L26 (MINOR, open, single): It is unclear whether the roadmap prompt change applies only under --unattended, which SA-1 requires.
- L27 (MINOR, open, single): Ordinary follow-ups have no stated handling.
- L28 (MINOR, open, single): The pr-submit wait check is unverifiable until the poll runtime is measured, and P2 has no check for it.
- L29 (MINOR, open, single): CAPS:158 is the provenance rule, which only partly supports the claim it is cited for.
- L30 (MINOR, open, single): WC-3 fixes the answer to the still-open D2 decision.
- L31 (MINOR, open, single): The P1 scope cell reads as giving load a section, which AC-1.1 forbids; AC-1.1 controls.

## Reviser brief

Blocking finding ids: L1.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL

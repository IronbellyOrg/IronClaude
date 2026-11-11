review: 3 of 3
# Merged review 3 (coordinator script; panel of 1 reviewers)
candidate: /tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad/p13/ab1/runs/b1-r6/ws/.dev/orca-command-refactor/specs/orca-worker-contract-spec.md sha256 e550dcb7fc3a3d867b7e5294799b7396379b1aa09607edb9890463612dc110e6
reviewers:
- t1b-1: report /tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad/p13/ab1/runs/b1-r6/ws/.dev/orca-command-refactor/review/round3-t1b-1.md, block ok true

## Ledger

| lid | status | blocking | confidence | severity | refs | reviewers |
|---|---|---|---|---|---|---|
| L1 | regressed | yes | overlap | CRITICAL | 2.2, 2.3, AC-0.4, AC-1.1, AC-1.2, AC-1.4, P0, P1, P2, WC-2, WC-4, WC-5, WC-6, WC-7 | t1b-1, t2-1, t3-1, t3-2 |
| L2 | resolved | yes | overlap | MAJOR | 2.1, AC-2.2, P1, SA-1, SA-3, SA-4, WC-1, WC-10, WC-11, WC-12, WC-2, WC-3, WC-7 | t1b-1, t2-1, t3-1, t3-2 |
| L3 | open | no | overlap | MAJOR | - | t2-1, t3-2 |
| L4 | open | no | single | MAJOR | SA-6, WC-9 | t2-1 |
| L5 | open | no | single | MAJOR | P4 | t2-1 |
| L6 | open | no | overlap | MAJOR | AC-2.2 | t2-1, t3-1 |
| L7 | open | no | single | MINOR | - | t2-1 |
| L8 | open | no | overlap | MAJOR | - | t2-1, t3-2 |
| L9 | open | no | single | MINOR | WC-7 | t2-1 |
| L10 | open | no | single | MINOR | AC-1.1 | t2-1 |
| L11 | open | no | single | MAJOR | 3.1, SA-2, WC-2 | t3-1 |
| L12 | open | no | single | MAJOR | 2.3, WC-11, WC-4, WC-6 | t3-1 |
| L13 | resolved | yes | overlap | MAJOR | P0, SA-2, WC-8 | t3-1, t3-2 |
| L14 | open | no | single | MINOR | 2.1, AC-1.2 | t3-1 |
| L15 | open | no | overlap | MAJOR | - | t3-1, t3-2 |
| L16 | open | no | single | MAJOR | P3 | t3-2 |
| L17 | open | no | single | MAJOR | SA-4 | t3-2 |
| L18 | open | no | single | MAJOR | - | t3-2 |
| L19 | open | no | single | MAJOR | - | t3-2 |
| L20 | open | no | single | MAJOR | - | t3-2 |
| L21 | open | no | single | MAJOR | P2 | t3-2 |
| L22 | open | no | single | MINOR | AC-0.1 | t3-2 |
| L23 | open | no | single | MINOR | - | t3-2 |
| L24 | open | no | single | MAJOR | AC-3.3, SA-1, SA-4 | t1b-1 |
| L25 | open | no | single | MINOR | 3.2 | t1b-1 |

## Blocking findings

### L1

#### L1.t1b-1 (F1)

- claim: WC-5 now applies to P0 runs and maps a report without a status to failed, so a succeeded troubleshoot run whose REPORT.md has no status is reported failed (REPORT.md content UNVERIFIED).
- anchor: "or its `status` is missing, unknown or unparseable (L1)"
- anchor2: "for a report that is not YAML (troubleshoot's `REPORT.md`) step 4 is replaced by `test -s`"

#### L1.t1b-1 (F2)

- claim: 7.2 step 4 as scripted asserts the status key, which fails for workflow's own status values, while WC-4 says 7.2 reads worker_status.
- anchor: "writes the four-value field as `worker_status`, which WC-5 and 7.2 read in place of `status` for it"
- anchor2: "assert d['status'] in {'succeeded','partial','failed','blocked'}"

#### L1.t1b-1 (F3)

- claim: Two research Tasks in one worktree write the same claudedocs/return-contract.yaml because research is not in WC-11's one-Task-per-worktree list.
- anchor: "research: beside the generated `claudedocs/research_*.md`"
- anchor2: "a command with a fixed default output (cleanup-audit, index-repo, release-split) runs one Task per worktree"

#### L1.t1b-1 (F4)

- claim: WC-8 is listed as a worker-session rule although its owner is the Command, and WC-1 is in neither list.
- anchor: "The worker-session rules WC-3, WC-5, WC-7, WC-8, WC-12 and the heartbeat of WC-10 apply to every worker run"

## Other findings

- L3 (MAJOR, open, overlap): The spec-panel row asks for --output and a new contract, but the supplied command definition already has both, under --report-dir, so the row and INV-B:182 are stale or the repo copy differs.
- L4 (MAJOR, open, single): Under --unattended, reflect accepts its own remediation offer, and WC-9 does not cover self-accepted remediation, so the authority rule that D2 states for implement is absent for reflect.
- L5 (MAJOR, open, single): The recommended D3 makes pr-submit coordinator-only, but the 10/27/6 split and the phase plan still count and schedule pr-submit as a worker.
- L6 (MAJOR, open, overlap): The review-translation gate needs an input that the command does not define, and the cli-eval flags assumed by AC-2.2 are not shown to exist.
- L7 (MINOR, open, single): Every Unattended section depends on an installed contract file with no fallback, so a missing file leaves the rules undefined.
- L8 (MAJOR, open, overlap): A fan-in consumer wired to a subset of N reports has no defined behaviour, so it can receive N-k reports where it expects N.
- L9 (MINOR, open, single): E3 presents a precedent that used the Agent-tool route WC-7 forbids as support for the direct route, with the caveat only in section 1.4.
- L10 (MINOR, open, single): AC-1.1 requires each Unattended section to name return-contract.yaml, but the cli-portify row does not give the location.
- L11 (MAJOR, open, single): Ready-today commands can still stop on /task questions that only the unattended mode resolves, so they are not ready as the heading states.
- L12 (MAJOR, open, single): Several 3.2 commands have no output flag or fixed location, so the contract path is not known before dispatch and cli-eval's fresh-directory rule cannot hold.
- L14 (MINOR, open, single): The live checks need the installed contract file, but the spec does not require superclaude install before them, so they fail in a bare dev checkout.
- L15 (MAJOR, open, overlap): The step 2 pass condition is met when the coordinator never looks at agentWait, because an absent field passes.
- L16 (MAJOR, open, single): The direct route is cited as proven in E3 and unproven in section 1.4, and the spec does not say whether the P3 run and the PR #329 run are the same.
- L17 (MAJOR, open, single): The scope sentence in 1.1 omits the defect fixes in section 3 that SA-4 names.
- L18 (MAJOR, open, single): The same frontmatter defect is out of scope for agent under 8.8 and in scope for business-panel under 3.2, with the need still UNVERIFIED.
- L19 (MAJOR, open, single): The coordinator's next step after partial and blocked is undefined, including who answers a blocked_question and whether partial may start dependents.
- L20 (MAJOR, open, single): tdd and release-split are called ready, but nested /task and tasklist-input prompts stay outside the brief's control.
- L21 (MAJOR, open, single): cli-portify keeps a src/superclaude lookup that the repo rule forbids for installed primitives, and P2 edits that file without fixing it.
- L22 (MINOR, open, single): No check confirms that an installed command can read the installed contract file.
- L23 (MINOR, open, single): The claimed evidence-validator pass is not reproducible from the workspace; noted without action.
- L24 (MAJOR, open, single): SA-4 forbids changing standalone behaviour while the listed defect fixes change a standalone default.
- L25 (MINOR, open, single): The index row edit carries no finding id.

## Reviser brief

Blocking finding ids: L1.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL

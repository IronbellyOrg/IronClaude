review: 1 of 3

# GATE review: orca-worker-contract-spec.md (/sc:spec-panel --mode critique --focus requirements,architecture)

- candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md` (286 lines, 59339 bytes)
- candidate sha256: `523f1629dc21eaacc3987537a70cf3e5944edf741f8b5368cdaad6f32cf68d9c`
- baseline: n/a (first review of a complete document; gate prompt: no prior rounds, no `--re-review`, no `--baseline`)
- reviewer model used: claude-sonnet-5-5
- prompt followed: GATE prompt and FIRST-REVIEW grading check, `~/.claude/rules/prompts/document_review_loop_prompts.md:57-64,35`
- context: `.dev/orca-command-refactor/README.md` read first (binding). Evidence I could check is limited to the three files under `.dev/orca-command-refactor/inventory/`; `INV-A` = `commands-a.md`, `INV-B` = `commands-b.md`, `CAPS` = `orca-capabilities.md`, `SPEC` = the candidate. Every citation to `cmd/`, `sk/`, `CLAUDE.md`, `EVIDENCE.md`, `.dev/codegraph-migration/...`, `orca-ide` guide lines or Orca source that is not quoted inside an inventory file is UNVERIFIED (those files are outside the workspace).

## What I covered
- Read the whole candidate, the README and `command.md`; read the inventory lines the candidate cites for its load-bearing claims (CAPS:44-52, 58-80, 84-103, 107-116, 128-130, 145-162, 178-188; INV-A:3,13,14,35,45,49-50,62,65,68,73,76-97,106,113,118,120; INV-B:3,31,36-37,65,105,112,272,285-296,301,311,320,323).
- Arithmetic: section 3.1 lists 10 commands, section 3.2 lists 27, section 4 lists 6; 10+27+6 = 43 = 21 (INV-A:3) + 22 (INV-B:3). Inventory totals agree: INV-A 5 ready, 13 needs-change, 3 coordinator-only (INV-A:73); INV-B 5, 14, 3 (INV-B summary). Phase rows: P1 = 9 changed + fixes, P2 = 11 + 4 ready commands = 15, P3 = 4, P4 = 3; 9+11+4+3 = 27 matches. Count conserved, no finding.
- Not covered: the actual `cmd/`, `sk/` and Orca guide text (not in the workspace), so no source line was re-read. Citations checked only against the inventories.

## === REQUIREMENTS ANALYSIS ===

### F-1 [BLOCKING] [MAJOR] cli-portify's three always-on approval gates have no pass-through, so its happy-path acceptance check cannot pass
Experts: Wiegers (testability), Adzic (concrete example), Whittaker (FR-2.4 Sequence Attack).
- Grading sentence: an implementer who follows the stated text as written builds `/sc:cli-portify` so that under `--unattended` each of its three approval gates ends the run as `status: blocked` (SPEC:105: "each of the three approval gates resolves as blocked with the artifact to review named in the contract"). SPEC defines no flag, input or resume rule that records an approval, and WC-2 offers only (a) default, (b) caller flag, (c) blocked, where cli-portify gets only (c) (SPEC:60). That build is wrong because AC-2.3 requires every P2 command, cli-portify included, to pass a happy-path run "with every required flag in the brief" with `--outcome succeeded` (SPEC:201), and a command whose every path through the gate is `blocked` ends `--outcome failed` under WC-5 (SPEC:63).
- Why this is a stated-text defect and not a missing requirement: the gates are not conditional. INV-A:45 records them as "Yes, always on: review after Phases 1 and 2, 'Present to user for approval before Phase 3', 'Present final spec to user for approval before delivering'". The inventory's own recommendation was "route the three approval gates through Orca `ask` or replace them with an explicit auto-approve flag" (INV-A:45; INV-A:79 "explicit auto-approve flag"). SPEC kept only the first half and dropped the flag. SPEC:105's added `--resume <contract>` flag (resume_phase/resume_substep) says where to restart; it does not say that restarting counts as approval, and SPEC's WC-3 re-invoke path needs "the answer as a flag" (SPEC:61) that this row never defines.
- Contrast: task, release-split and tdd gates are conditional on bad input (SPEC:121, 89, 90), so their happy path never reaches the gate. cli-portify's does.
- Recommendation: delete or narrow, do not add a mechanism: either name the one existing way the brief pre-approves each gate (a flag or a `--resume` rule that is stated to count as approval), or remove cli-portify from the AC-2.3 happy-path set and say it always ends `blocked` until a person approves. Either one-line edit repairs it.
- Priority: High. Quality impact: removes one unpassable acceptance criterion.
- Adversarial trace (FR-3 template): I can break this specification by **Sequence Attack**. The invariant at **SPEC:105 with AC-2.3 (SPEC:201)** fails when **the brief contains every flag the row lists**. Concrete attack: Phase 1 and 2 finish, the first gate fires, contract = `blocked`, worker sends `failed`; the coordinator relaunches with `--resume <contract>`, the next gate fires again, `blocked` again; after the third gate the command never delivers; AC-2.3 never reaches `succeeded`.

## === ARCHITECTURE ANALYSIS ===

The decision itself (Orca on top, commands as units, no Orca call in a command) is consistent: R1-R5 (SPEC:31-37) and SA-2 (SPEC:147) point the same way and the cited CAPS lines exist (CAPS:97-101, 145-150, 155-161). I found no blocking architecture defect. Items below are Medium or minor and are listed under follow-up candidates.

## Guard Condition Boundary Table (Nygard builds, Crispin completes, Whittaker attacks)
Guards found in the candidate. Classes left out are stated with a one-line reason. Format is the 7-column table.

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|---|---|---|---|---|---|---|
| `--unattended` standalone token | SPEC:16, 51 | Zero/Empty (flag absent) | no flag | false | Today's behaviour unchanged (SA-1, SPEC:146) | OK |
| `--unattended` with no output dir/file passed | WC-4, SPEC:62 | Zero/Empty (path absent) | `--output` missing | true | Not specified: WC-4 says contract goes in "the directory the coordinator passed"; 2.3 says the brief must pass it (SPEC:73); the command's own behaviour when the brief omits it is not stated | GAP (Medium, M-1) |
| gate resolves blocked | WC-2(c), SPEC:60 | Typical | any gate | true | Contract `status: blocked` + `blocked_question`, stop | OK |
| gate resolves blocked, cli-portify always-on gates | SPEC:105 | Legitimate Edge Case | 3 gates, no pre-approval | true | Not specified past `blocked`; no pass-through | GAP (blocking, F-1) |
| heartbeat wait split | WC-10, SPEC:68 | Maximum/Overflow | single tool call > 5 min | true | Split into waits <= 4 min | OK |
| heartbeat wait split, pr-submit | SPEC:114 | Legitimate Edge Case | poll script runtime unknown | unknown | "confirm" under 4 min; poll runtime UNVERIFIED | GAP (Medium, UNVERIFIED item 12 already records it) |
| nesting depth fence | R1, SPEC:33 | Sentinel Value Match | depth = 1 | true | Worker may not start workers | OK |
| task confidence < 0.70 | SPEC:121 | Typical | 0.69 / 0.70 | true / false | Blocked below; boundary 0.70 follows the command's threshold (INV-A:36 gives the same 0.70 for agent); not re-read for task | OK (UNVERIFIED source) |
| `partial` outcome map | WC-5, SPEC:63 | One/Minimal | `partial` | maps to succeeded | Stated, and the body names `partial` | OK |
| `ask` timeout | WC-3, SPEC:61 | Maximum/Overflow | timeout | true | Resume same message ID; default timeout UNVERIFIED (CAPS:68, SPEC UNVERIFIED 10) | OK |

Classes omitted: Maximum/Overflow for the `--unattended` token and for gate resolution (a flag and a three-valued resolution have no capacity bound). No guard has a numeric threshold other than the ones listed.

## Pipeline/Quantity check (Fowler leads, Whittaker attacks)
Only multi-stage count flow is the command classification. Quantity Flow: `[43 commands] --> [10 ready | 27 needs-change | 6 coordinator-only]` = 43, N in = N out, no divergence; the P0-P4 distribution above also conserves 27. No mismatch.

## Follow-up candidates (Medium and minor; never trigger a revision)
Medium (warnings; labels may say MAJOR but each needs a guess or states a requirement the document never states):
- M-1 (Wiegers) Behaviour when `--unattended` is passed with no output location is not stated for commands that gain a new `--output` (analyze, build, design, document, explain, index, test, save, ...; SPEC:99-123). WC-4 needs a coordinator-passed directory (SPEC:62) and 2.3 puts the duty on the brief (SPEC:73); no rule says the command blocks or defaults. Where would the `blocked` report even go?
- M-2 (Fowler) AC-C5 (SPEC:176) requires no deleted lines in a touched command file, but SA-4 and section 3 add flags to existing commands (SPEC:149); if the implementer edits the existing Usage line the check fails; if they add a second Usage line it passes. The text allows both readings.
- M-3 (Fowler) AC-C1 (SPEC:172) scans `src/superclaude/core` for `orca orchestration|worktree|terminal|agent` and requires empty output, while P0 adds `WORKER-CONTRACT.md` and an Orca section to `HOW-WE-WORK.md`, both under `core/` (SPEC:52, 158, 150). If either names an Orca command the P0 check fails; SA-2 only exempts "a changed command" (SPEC:147). Also the pipe characters are written `\|` in the cell; copied as written they are literal pipes in an ERE and the grep can never match, a false pass.
- M-4 (Adzic) P0 has "no command edits" (SPEC:158) so no command accepts `--unattended` yet, but 2.3 and 7.2 step 1 say the brief carries `--unattended` (SPEC:73, 180); AC-0.4's example command lines omit it (SPEC:194). The smoke-run brief is not stated.
- M-5 (Wiegers) SPEC E3 cites the `invocation_method: "skill-direct"` contract as evidence that it "has worked before" (SPEC:23) while section 1.4(1) says the PR #329 run "proves the nested route, not the direct route" (SPEC:43). INV-A:13 and INV-A:35 read the same file as proof of a direct call. The spec does not reconcile the two readings; P0 tests it anyway, so no wrong build follows, but the evidence statement is internally inconsistent.
- M-6 (Cockburn) SPEC says the spec-panel row adds `--output` and `target_release` blocking (SPEC:120). The command definition supplied for this review (`command.md:22-23,455-465`) already has `--output`, `--report-dir`, `--unattended`, `<report-dir>/return-contract.yaml` and the TDD-without-`--target-release` blocked gate. The SPEC row and WC-4's `--output`/`--output-dir` wording (SPEC:62) do not match it. UNVERIFIED which is current: the real `cmd/spec-panel.md` is not in the workspace.
- M-7 (Nygard) WC-4 says commands that already write a contract "keep their fields and add the missing ones" (SPEC:62) while the Decisions table fixes `status` to four values (SPEC:262) and AC step 4 asserts membership (SPEC:183). The existing `status` values of workflow, brainstorm, reflect and adversarial contracts are not in any checkable file (INV-B:272 names the field only), so UNVERIFIED whether they conflict.
- M-8 (Hohpe) index-repo (SPEC:86) and cleanup-audit (SPEC:85) write fixed repo-root or `.claude-audit/` paths; WC-11 forbids two workers writing the same file (SPEC:69) and WC-6 says a retry uses a fresh output directory (SPEC:64), but index-repo's contract and report location is fixed, so a retry or a second worker overwrites. cleanup-audit notes "one audit per worktree" (SPEC:85); index-repo does not.
- M-9 (Newman) If D3 is answered (a), pr-submit is neither changed (section 3.2 row) nor listed in section 4 (SPEC:139, 241), so the 10/27/6 split and the P4 scope are off by one until then. Stated as conditional in SPEC:139 only.
- M-10 (Wiegers) WC-3 tells the worker to re-invoke "with the answer as a flag" (SPEC:61); apart from spec-panel's `--target-release` and review-translation's pre-confirmed input, section 3 defines no answer flag for the other blocked gates (task confidence, recommend question, cli-eval W0).

Minor notes:
- n-1 E2 cites `CAPS:161` for `[H:worker-start]` line 38 / `--agent claude` (SPEC:22); CAPS:161 is the pr-submit top-level passage. The `--agent claude` and `state: ready` facts are at CAPS:49 and INV-A:13.
- n-2 WC-7 cites `INV-A:95` for "nesting loses tools at Claude Code's depth limit" (SPEC:65); INV-A:95 says nesting is allowed up to three layers, and the depth-limit statement is INV-A:14.
- n-3 R1 states "It cannot run as a worker at the current setting" as fact (SPEC:33) while the enforcing call sites are UNVERIFIED (CAPS:103); the sentence itself flags this. R2-R5 stand without R1.
- n-4 SA-3 allows report files "when the caller passes the new output flag" (SPEC:148) while WC-4 says only in unattended mode (SPEC:62).
- n-5 Citation conventions claim a fresh-context check of 340 citations (SPEC:285); not reproducible here, UNVERIFIED for everything outside the inventories (`EVIDENCE.md:39,45,56`, `CLAUDE.md:16,50,72-83,334`, `HOW-WE-WORK.md:22,171,249,254`, `install_core.py:13-24`, `pyproject.toml:38`).

Issue offer: the session that ran this review asks the user once whether to open an issue for M-1 to M-10 and n-1 to n-5; I created none.

## Reviser brief
Repair only the blocking finding F-1 in the revised candidate `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`. Prefer deleting or narrowing text when the requirements are still met. Add no rule, mechanism or section that a listed finding does not call for, and cite the finding id on every addition. Report the byte size before and after, and the bytes added and deleted per finding id. Leave minor and Medium findings alone. Return the candidate once and do not award yourself a PASS. (Brief clauses overridden by this report: none.)

verdict: FAIL

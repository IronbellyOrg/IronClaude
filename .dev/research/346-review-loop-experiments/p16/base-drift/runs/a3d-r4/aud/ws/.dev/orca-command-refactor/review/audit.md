review: 1 of 3

# Spec-panel audit: orca-worker-contract-spec.md (whole-document first review)

## Header
- candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`
- candidate sha256: `e588d816f4ebe8cc73b0f945a07b3aaec6c6e366428b45f3edd87fcc2d7056f5`
- baseline: not given (neither `--re-review` nor `--baseline` was passed, so this is a first review of the full document)
- reviewer model used: claude-sonnet-5-5
- command: `/sc:spec-panel @.dev/orca-command-refactor/specs/orca-worker-contract-spec.md --mode critique --focus requirements,architecture` (no `--unattended`; no `--iterations` effect, one review)
- prompt followed: FIRST-REVIEW prompt, `~/.claude/rules/prompts/document_review_loop_prompts.md:27-32`, with `{{CANDIDATE}}` = the file above
- brief clauses overridden: none
- citation key: `SPEC:N` = line N of the candidate; `INV-A:N`, `INV-B:N`, `CAPS:N` = line N of `.dev/orca-command-refactor/inventory/commands-a.md`, `commands-b.md`, `orca-capabilities.md`; `README:N` = `.dev/orca-command-refactor/README.md`. Only these files were checkable. Any citation to `src/`, `.dev/evals/`, `.dev/codegraph-migration/`, `CLAUDE.md`, Orca installed files or Orca guide output is UNVERIFIED here and is marked so.

## What was covered
- Whole candidate read (SPEC:1-285), README read first (README:1-38), all three inventories read in full.
- Every section-3 evidence pointer to an inventory line (`INV-A:35-55`, `INV-B:31-52` and the per-command notes) was matched to the inventory; every `CAPS:N` pointer in sections 1 and 2 was matched. Counts were rechecked: 10 ready (SPEC:81-92) + 27 changed (SPEC:97-125) + 6 coordinator-only (SPEC:131-137) = 43; phase membership in SPEC:158-162 matches the section 3.2 phase column for all 27 changed commands; of the 10 ready commands only 8 are given a phase (see F-M1).
- Experts applied in the command's order: Wiegers, Adzic, Cockburn, Fowler, Nygard, Whittaker, Newman, Hohpe, Crispin, Gregory, Hightower. Focus buckets: requirements (Wiegers lead, Adzic, Cockburn) and architecture (Fowler lead, Newman, Hohpe, Nygard).
- Not covered: anything only reachable outside the sandbox (source files, Orca guide output, the PR #329 run). Those claims were taken from the inventories as cited by the spec and are UNVERIFIED: `grep` result at SPEC:25 (E5), the 11 re-read locations at SPEC:11, `install_core.py` lines at SPEC:52, `refs/qa.md:232,238` at SPEC:233, and the `EVIDENCE.md` lines (second-hand through CAPS:49).

## Findings table (ids used by the verdict)
| id | severity | grade | expert | open |
|---|---|---|---|---|
| F-B1 | MAJOR | blocking | Crispin, Adzic | yes |
| F-B2 | MAJOR | blocking | Crispin, Wiegers | yes |
| F-M1 | MAJOR label | Medium | Wiegers, Fowler | follow-up |
| F-M2 | MAJOR label | Medium | Wiegers | follow-up |
| F-M3 | MAJOR label | Medium | Fowler, Newman | follow-up |
| F-M4 | MAJOR label | Medium | Nygard, Newman | follow-up |
| F-M5 | MINOR label | Medium | Hohpe | follow-up |
| F-M6 | MAJOR label | Medium | Cockburn, Wiegers | follow-up |
| F-M7 | MAJOR label | Medium | Wiegers | follow-up |
| F-m1 .. F-m4 | MINOR | note | various | note |

## === REQUIREMENTS ANALYSIS ===

### F-B1 (blocking). The P0 smoke-run check cannot pass for two of its three commands
- Expert: Crispin (completeness of acceptance criteria), Adzic (concrete example fails).
- Grading sentence: An implementer who follows the stated text as written builds a P0 live check in which `/sc:troubleshoot` and `/sc:adversarial` must satisfy step 3 ("its report path is the WC-4 contract path"; "`--outcome` matches the contract's `status`"), and that check is wrong because neither command has a WC-4 contract before Phase 1, so the AC fails and the same text says a failure there "reopens section 1".
- Evidence:
  - AC-0.4 requires "steps 1-3 and 5-7 pass; step 4 uses the command's existing report file, since the contract arrives in P1" and "a failure here reopens section 1" (SPEC:194). Only step 4 is relaxed.
  - Step 3's pass condition is the WC-4 contract path and a match with the contract's `status` (SPEC:182). WC-4 fixes that path as `<output-dir>/return-contract.yaml` (SPEC:62).
  - `/sc:troubleshoot` writes `REPORT.md` as its report; `return-contract.yaml` exists only with `--caller task-unified` (INV-B:242; SPEC:91 "Report today: REPORT.md").
  - `/sc:adversarial` writes a contract but its filename is not fixed and sits at `<output>/adversarial/return-contract.yaml` or one level deeper on disk (INV-A:35, INV-A:60; SPEC:83), while WC-4 wants `<output-dir>/return-contract.yaml`; the filename fix is a Phase 1 item (SPEC:83, SPEC:159).
  - Only `/sc:workflow` has a contract today (SPEC:92, INV-B:272).
- Consequence: the Phase 0 gate that is supposed to "close evidence gap 1.4 (1)" (SPEC:43, SPEC:158) reports a failure for a reason unrelated to whether a direct worker run works, and the spec tells the reader to reopen the core decision.
- Recommendation (narrowing, no new mechanism): in AC-0.4 state that step 3's path and outcome comparison use the command's existing report file, as step 4 already does.
- Priority: High. Quality impact: the only live evidence the spec's decision rests on is mis-specified.

### F-B2 (blocking). The P1 live check requires a contract and an output flag that listed P1 commands do not have
- Expert: Crispin, Wiegers.
- Grading sentence: An implementer who follows the stated text as written runs the 7.2 live check "on each P1 command with `--unattended --output <dir>`" and requires every step to pass, and that is wrong because three commands named in the P1 row cannot pass step 4 or accept the flags.
- Evidence:
  - AC-1.2: "7.2 live check on each P1 command with `--unattended --output <dir>`: all steps pass" (SPEC:196). The P1 row names load, cleanup-audit, index-repo, adversarial and workflow among its commands (SPEC:159).
  - 7.2 step 4 needs a non-empty contract with `status` and `command` (SPEC:183).
  - `load` has "Report: none" and no Unattended section (SPEC:112; AC-1.1 exempts it explicitly at SPEC:195). AC-1.2 has no such exemption.
  - `cleanup-audit` has a fixed output directory and no output flag (SPEC:85; INV-A:42 `.claude-audit/`); `index-repo` is invoked with "none" and writes `PROJECT_INDEX.md` (SPEC:86; INV-A:53). Neither lists `--output` in its brief or its row.
- Consequence: the Phase 1 gate is unsatisfiable as worded, so a phase that "passes only when every check in its block passes" (SPEC:167) can never pass without the implementer inventing a scope cut.
- Recommendation (narrowing): scope AC-1.2 to the commands that gain a `## Unattended mode` section and an output flag, matching AC-1.1.
- Priority: High.

### F-M1 (Medium). Two ready commands are never given `--unattended` or a contract
- Expert: Wiegers (traceability), Fowler (count conservation).
- Evidence: Section 2.3 and D1(a) require every brief to carry `--unattended` (SPEC:73, SPEC:228). Of the 10 ready commands, section 6 assigns a phase to 8 (P1 fixes: adversarial, cleanup-audit, index-repo, workflow, SPEC:159; P2: reflect, release-split, tdd, troubleshoot, SPEC:160). `brainstorm` and `init-lite` have "Small fix: None" and no phase (SPEC:84, SPEC:87), so no phase adds the flag, the section or a WC-4 contract for them. `init-lite` writes only `.dev/superclaude/context-audit.md` (SPEC:87).
- Why Medium: the text does not say what happens when `--unattended` reaches a command that does not define it; that needs a guess about argument parsing (brainstorm takes free-text topics, INV-A:39). It is a missing requirement, not a stated text that does harm.
- Recommendation: add both to a phase, or state that the brief omits `--unattended` for them and the coordinator reads their existing file.

### F-M2 (Medium). Contract location is undefined for commands with a fixed or unnamed output location
- Expert: Wiegers.
- Evidence: WC-4 places the contract in the caller-supplied output directory (SPEC:62). `cli-portify` row says "file location unnamed" (SPEC:105; INV-A:45); `cli-eval` writes under fixed workspaces and has "no single named report file" (SPEC:104; INV-A:44); `cleanup-audit` and `index-repo` have no output flag (F-B2). AC-2.3 requires `test -s <contract>` for each P2 command (SPEC:201, SPEC:183).
- Why Medium: requirement the document never states.
- Recommendation: add an output-directory flag to those rows or name a derived contract path.

### F-M6 (Medium). Authorization mechanism for outward actions is assumed in P2 but decided in P4
- Expert: Cockburn (actor and goal), Wiegers.
- Evidence: P2 rows say `--post-pr` and task `commit`/`push` return "only with an explicit ... in the brief" (SPEC:100, SPEC:121) and WC-9 says outward defaults turn on only "through the command's own explicit flag" (SPEC:67). D4 asks whether a brief may authorize outward actions at all and lists auggie-review `--post-pr` and task `commit`/`push` as affected (SPEC:244); option (b) "Never" removes what the P2 rows describe. Yet section 6 says Phases 1-3 need no user decision (SPEC:154). `pr-submit` and `post-release` have no named "explicit flag" in the rows (SPEC:113-114).
- Why Medium: the recommendation (a) is stated and P2 follows it; the conflict only matters if the user picks (b).
- Recommendation: say P2 assumes D4(a) or move the outward-flag returns to P4.

### F-M7 (Medium). WC-1 "well inside the readiness limit" is not measurable
- Expert: Wiegers (SMART), Adzic.
- Evidence: WC-1 requires a prompt to "fall back on its own well inside the readiness limit (default 60 s)" (SPEC:59). The evidence it cites says a 30 s fallback passed (start returned at 34 s) and "above about 45 s" fails again (SPEC:59; CAPS:49). No number or pass check appears in section 7.
- Recommendation: state the 30 s figure as the ceiling and add a check, or mark WC-1 as a launch-setup note with no acceptance check.

## === ARCHITECTURE ANALYSIS ===

### F-M3 (Medium). WC-4 says "keep their fields" but fixes a four-value `status` set that existing contracts may not use
- Expert: Fowler (interface consistency), Newman (versioning).
- Evidence: WC-4: commands with a contract "keep their fields and add the missing ones", and `status` is "one of `succeeded`, `partial`, `failed`, `blocked`" (SPEC:62). AC step 4 asserts that set (SPEC:183). The Decisions table picked a fixed set over copying each command's own statuses (SPEC:262). The inventories show workflow's contract has a `status` and a `failed` value but not its full vocabulary (INV-B:272); brainstorm, reflect and adversarial vocabularies are not listed (INV-A:39, INV-B:112, INV-A:35). If an existing `status` enum differs, "keep" and "one of four" conflict.
- Why Medium: needs a guess about the existing enums; UNVERIFIED here.
- Recommendation: state which wins, or add a separate `worker_status` field.

### F-M4 (Medium). WC-6 "command writes a fresh output directory" conflicts with WC-4 "directory the coordinator passed"
- Expert: Nygard (recovery), Newman.
- Evidence: WC-4 fixes the contract path before dispatch from the coordinator's `--output` (SPEC:62, SPEC:73). WC-6 lets a command without a resume flag satisfy retry safety by writing "each run into a fresh output directory" (SPEC:64) and section 3.2 lists "fresh dir" for 18 commands. A `--retry-of` worker is started from the same Task (CAPS:116) and the same brief, so the command receives the same directory; the command cannot choose a fresh one without moving the contract path. The spec does not say that the coordinator passes a new directory on retry.
- Why Medium: the fix is one sentence in section 2.3, but the text allows two readings.
- Recommendation: state that on retry the coordinator passes a new output directory.

### F-M5 (Medium). AC-C1 greps `src/superclaude/core` while the contract file and routing section live there
- Expert: Hohpe (integration boundaries).
- Evidence: AC-C1 searches commands, skills, agents and core and expects no output (SPEC:172). SA-2 limits the ban to "command, skill or agent file" and allows an Orca mention inside the contract file (SPEC:147). P0 adds `core/WORKER-CONTRACT.md` and an Orca section in `core/HOW-WE-WORK.md` (SPEC:158, SPEC:150). Whether those files contain the literal `orca orchestration` is not specified (WC-3 says "the preamble's `ask` command", SPEC:61; section 7 writes `ORCA` in capitals).
- Why Medium: passes or fails depending on wording of files not yet written.
- Recommendation: exclude the two core files from AC-C1 or forbid the literal in them.

## === ADVERSARIAL ANALYSIS (Whittaker) ===
Review order 6, after Fowler and Nygard.

- I can break this specification by **Sequence Attack**. The invariant at **SPEC:194 + SPEC:182** (P0 smoke runs prove the direct route) fails when the checks run in the stated order on a command whose contract arrives in P1. Concrete attack: coordinator starts `/sc:troubleshoot "x"` (step 1 ok, ready); it finishes and sends `worker_done --report-path REPORT.md --outcome succeeded`; step 3 compares that path to `<output>/return-contract.yaml`, which does not exist; AC-0.4 marks failure and "reopens section 1". State before: decision accepted; after: decision reopened on a false negative. (F-B1)
- I can break this specification by **Zero/Empty Attack**. The invariant at **WC-5 (SPEC:63)** fails when the report exists but is empty or has no `status`. Concrete attack: worker writes a zero-byte `return-contract.yaml` on a crash; WC-5 says `failed` only if "no report exists", so the worker sends `--outcome succeeded` ("otherwise"). Only the coordinator's step 4 (`test -s`, SPEC:183) catches it, after the Task is already settled. Medium (stated text needs a guess about "exists").
- I can break this specification by **Divergence Attack**. The invariant at **SPEC:62 vs SPEC:64** fails when a retry reuses the first attempt's brief: WC-4 pins the directory, WC-6 relies on a fresh one. Concrete attack: attempt 1 writes `out/return-contract.yaml` with `status: failed`; the retry gets `--output out` and, for a "fresh dir" command, overwrites in place or appends. (F-M4)
- I can break this specification by **Sentinel Collision Attack**. The invariant at **SPEC:62 `status`** fails when an existing contract uses `status: complete` or similar. (F-M3, UNVERIFIED enums.)
- I can break this specification by **Accumulation Attack**. The invariant at **WC-10 (SPEC:68)**: "heartbeat every 5 minutes" with waits of "at most 4 minutes". A command with N sequential 4-minute tool calls and a model turn between them keeps the heartbeat due at 5 minutes but gives the session no trigger to send it between calls; the spec relies on the session noticing elapsed time (CAPS:130 says the cadence comes from the preamble). No check measures it except AC-4.3 for pr-submit (SPEC:210). Minor note.

## Guard Condition Boundary Table (Nygard lead, Crispin completeness, Whittaker attack)
Classes left out are named in the line under the table.

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|---|---|---|---|---|---|---|
| WC-5 outcome mapping | SPEC:63 | Zero/Empty | report file present, 0 bytes or no `status` | "no report exists" false, so "otherwise" true | `--outcome succeeded` by the letter of the text | GAP (Medium; caught later by SPEC:183) |
| WC-5 outcome mapping | SPEC:63 | Typical | `status: succeeded` | true | `--outcome succeeded` | OK |
| WC-5 outcome mapping | SPEC:63 | Sentinel Value Match | `status: partial` | true | `succeeded`, body states `partial` (SPEC:63, SPEC:263) | OK |
| WC-5 outcome mapping | SPEC:63 | Legitimate Edge Case | existing contract `status` outside the four values | undefined | not specified | GAP (Medium, F-M3) |
| WC-1 readiness fallback | SPEC:59 | Typical | fallback 30 s | true | passes (CAPS:49) | OK |
| WC-1 readiness fallback | SPEC:59 | Maximum/Overflow | fallback above about 45 s | false | fails at `agent_readiness` (SPEC:59) | OK |
| WC-1 readiness fallback | SPEC:59 | Legitimate Edge Case | "well inside" 60 s, no figure | undefined | not measurable | GAP (Medium, F-M7) |
| WC-10 wait split | SPEC:68 | Typical | single call 6 min | true | split into waits of at most 4 min | OK |
| WC-10 wait split | SPEC:68 | Legitimate Edge Case | single call of exactly 5 min | false (rule says "longer than 5") | no split; heartbeat due at the same instant | GAP (minor note, F-m3) |
| Nesting depth fence | SPEC:66, CAPS:97-101 | Typical | worker calls `worker-start` at depth 1 | true | refused `nested_worker_depth_exceeded` | OK |
| Nesting depth fence | SPEC:66 | Legitimate Edge Case | `task-create` from a depth-1 worker | unknown | WC-8 forbids it either way (SPEC:66, CAPS:103) | OK |
| Task confidence gate | SPEC:121, INV-B:199 | Typical | 0.69 | true | blocked | OK |
| Task confidence gate | SPEC:121 | Legitimate Edge Case | exactly 0.70 | false (rule is "below 0.70") | proceeds | OK |
| P1 live check scope | SPEC:196 | Zero/Empty | listed command with no report (load) | check requires a contract | check cannot pass | GAP (blocking, F-B2) |
| P0 live check step 3 | SPEC:182, SPEC:194 | Zero/Empty | command with no WC-4 contract (troubleshoot) | step requires one | check cannot pass | GAP (blocking, F-B1) |

Left out with reason: Maximum/Overflow for WC-5, the depth fence and the confidence gate (no capacity applies; the values are enumerations or a single numeric threshold); One/Minimal for all guards (no collection or count is tested).

## Pipeline Dimensional Analysis (Fowler lead, Whittaker attack)
Triggered by the command-to-phase flow, where a stage may emit fewer items than it receives.

```text
[Source: 43 commands, SPEC:76] --> [Split by verdict, SPEC:76] --> [10 ready (SPEC:81-92)]
                                                              --> [27 changed (SPEC:97-125)]
                                                              --> [6 coordinator-only (SPEC:131-137)]
[10 ready] --> [Phase assignment, SPEC:158-162] --> [8 with a phase: P1 4, P2 4]   <-- 2 unassigned: brainstorm, init-lite (F-M1)
[27 changed] --> [Phase assignment] --> [P1 9, P2 11, P3 4, P4 3 = 27]            (conserved)
[Consumer: SPEC:73 brief rule "every Task carries --unattended" expects 10 + 27 = 37 commands to accept the flag; 35 are assigned]
```

Count mismatch recorded as F-M1; graded Medium by consequence (no concrete wrong outcome without a guess about argument handling), although the command labels any dimensional mismatch CRITICAL.

## Expert notes with no finding
- Cockburn: primary actor (coordinator) and goal are stated in SPEC:16 and SPEC:73; the user-decision actors are stated in section 9.
- Hightower: operational limits (heartbeat, readiness, depth) are tied to numbered evidence (CAPS:44-45, CAPS:97-101, CAPS:130).
- Gregory: section 7 gives a per-phase check list and common checks; the gaps are in F-B1, F-B2, F-M7.

## Notes (minor)
- F-m1: SPEC:121 says the `task` contract exists "today only on TFEP"; the inventory shows TFEP writes `tfep-incident-report.md` and `context.yaml`, not a return contract (INV-B:202; SPEC:121).
- F-m2: SPEC:154 says Phases 1-3 need no decision while SPEC:225 says Phases 0-3; wording differs, meaning is the same.
- F-m3: WC-10 boundary at exactly 5 minutes (table above).
- F-m4: A `partial` Task is reported to Orca as `succeeded` (SPEC:63, SPEC:263), so dependents of that Task become ready (CAPS:86-92); the spec relies on the coordinator opening the report first (SPEC:73). The choice is recorded, not wrong.

## Follow-up candidates
Medium: F-M1, F-M2, F-M3, F-M4, F-M5, F-M6, F-M7.
Minor: F-m1, F-m2, F-m3, F-m4.
The question "open an issue for these?" belongs to the session that ran the review; this run is a delegated worker whose reply is limited to the output path, so it did not ask and created no issue. The coordinator should ask the user once for this loop.

## Reviser brief
Blocking finding ids: F-B1, F-B2.
Rules (restating the command's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id. Leave Medium and minor findings alone. Return the candidate once and do not award yourself a PASS.

verdict: FAIL

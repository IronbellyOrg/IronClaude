review: 1 of 3

# Spec-panel report, round 1: orca-worker-contract-spec.md

## Report header
| Field | Value |
|---|---|
| command | `/sc:spec-panel @.dev/orca-command-refactor/specs/orca-worker-contract-spec.md --mode critique --focus requirements,architecture` |
| candidate | `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md` (285 lines) |
| candidate sha256 | `d3cdbe573e57303b9ce6c93d1fe98ba18fb7cb1a15773d926bf6a0c31425200d` |
| baseline sha256 | none: first review, neither `--re-review` nor `--baseline` was given |
| reviewer model actually used | claude-sonnet-5-5 (Sonnet 5.5) |
| review | 1 of 3 (first review of the full document) |
| prompt followed | FIRST-REVIEW prompt, `~/.claude/rules/prompts/document_review_loop_prompts.md:31-36` (file read in full) |
| `--unattended` | not passed (attended run; no `return-contract.yaml` written, the brief assigns only this file) |
| brief clauses overridden | none |
| prior findings | none (first review) |

## Coverage (what this review covered)
- Read in full: the candidate, `.dev/orca-command-refactor/README.md`, `inventory/commands-a.md`, `inventory/commands-b.md`, `inventory/orca-capabilities.md`, `command.md`, and the review-loop prompts file.
- Checked against the inventories: every `INV-A:N`, `INV-B:N` and `CAPS:N` citation in sections 1, 3, 4, 6, 7, 8 and UNVERIFIED items of the candidate. I found no wrong line; the verdict counts 10 ready / 27 needs-change / 6 coordinator-only reconcile with `INV-A:73` (5/13/3) plus `INV-B:278` (5/14/3), and the phase membership in section 6 sums to the rows of section 3 (see Quantity Flow Diagram).
- Cannot be checked in this sandbox and therefore UNVERIFIED here: every citation to `src/superclaude/...`, `CLAUDE.md`, `pyproject.toml`, `Makefile`, `tests/`, `~/.claude/skills/...`, `.dev/codegraph-migration/...` and `.dev/evals/...` (only the lines the inventories quote from these were compared), and the spec's own greps in E5 (line 25), which need the live tree.
- Experts engaged (focus requirements and architecture): Wiegers (lead), Adzic, Cockburn, Fowler (lead), Nygard, Newman, Hohpe, plus Whittaker (active in every panel review, per `command.md:83`). Crispin, Gregory and Hightower are outside both focus areas and were not engaged. `--focus correctness` is not active, so no State Variable Registry is produced.
- Mandatory artifacts produced: Guard Condition Boundary Table (guards exist), Quantity Flow Diagram (the section 3 to section 6 command funnel has stages whose counts differ).
- Not done by design: no revised specification, no edit of any file other than this report.

## Findings register
Blocking findings: F-01, F-02. Medium findings (warnings, follow-up candidates): M-01 to M-10. Minor notes: N-01 to N-05.

| id | severity label | grade | bucket | expert | one line |
|---|---|---|---|---|---|
| F-01 | MAJOR | blocking | requirements | Wiegers, Whittaker | WC-4 contract-location rule cannot be satisfied for tdd, init-lite, cli-eval, workflow, adversarial |
| F-02 | MAJOR | blocking | architecture | Fowler, Whittaker | AC-1.1 and the P1 scope contradict the load row, the P4 hold and recommended D3(a) |
| M-01 | MAJOR | Medium | architecture | Nygard | WC-10 heartbeat cannot be met during foreground Agent fan-out, and WC-7 forbids the subagents from sending it |
| M-02 | MAJOR | Medium | architecture | Nygard | Section 1.4(2) states as fact that a command's own question comes after readiness |
| M-03 | MAJOR | Medium | requirements | Wiegers | "Keep their fields" collides with the fixed four-value `status` set; existing vocabularies are never recorded |
| M-04 | MAJOR | Medium | requirements | Whittaker | No rule for a stale, empty or malformed contract file; WC-5 only tests "no report exists" |
| M-05 | MAJOR | Medium | requirements | Wiegers | `--post-pr` is not an existing flag, precedence with the implied `--no-post-pr` is undefined |
| M-06 | MAJOR | Medium | requirements | Wiegers | WC-9 "paid external run" is undefined; research and review-translation exist to call web search |
| M-07 | MAJOR | Medium | architecture | Fowler | AC-C1 scans `src/superclaude/core`, where the P0 deliverables must mention Orca |
| M-08 | MAJOR | Medium | requirements | Adzic | SA-3 and WC-4 disagree on when the contract file is written |
| M-09 | MAJOR | Medium | architecture | Newman | Tasklist nesting claim rests on a docs citation that does not cover reflect's own fan-out; inventory advice dropped without a Decisions entry |
| M-10 | MAJOR | Medium | requirements | Cockburn | How a worker invokes the command (slash line vs Skill tool) and the P0 brief carrying `--unattended` before any command accepts it |
| N-01 | MINOR | minor | requirements | Wiegers | Section 1.1 says command changes are "limited to" three items; section 3 adds defect fixes |
| N-02 | MINOR | minor | requirements | Nygard | WC-1 gives no numeric ceiling though the evidence gives one (about 45 s) |
| N-03 | MINOR | minor | requirements | Whittaker | `--unattended` inside quoted free text, and `--unattended` combined with `--interactive`, are unspecified |
| N-04 | MINOR | minor | requirements | Adzic | P1 says "No person gate is involved" but four P1 rows refuse or pin a mode |
| N-05 | MINOR | minor | architecture | Hohpe | AC-0.4 step 4 and 7.2 step 6 depend on an unfixed adversarial filename and on a shared worktree's `git status` |

---

=== REQUIREMENTS ANALYSIS ===

### F-01 (MAJOR, blocking, priority High): the WC-4 contract path rule has no answer for five specified commands
- **Expert**: Wiegers (lead), Whittaker (Sentinel Collision, Zero/Empty).
- **Issue**: WC-4 defines the report location as `<output-dir>/return-contract.yaml`, "where `<output-dir>` is the directory the coordinator passed (`--output` / `--output-dir`)", and says it is "known before dispatch" (spec line 62; repeated in section 2.3, line 73, and in step 3 of the live check, line 182: "its report path is the WC-4 contract path"). Five rows give the command no such directory:
  - tdd: brief passes `--output <file>` (line 90), and AC-2.2 runs `/sc:tdd "auth" --unattended --output <file>` (line 200). The value is the TDD file, not a directory.
  - init-lite: `--output <file>` (line 87).
  - cli-eval: no output flag is listed (line 104; `INV-A:44` gives fixed workspaces `.dev/eval-workspaces/cli-eval/...`); AC-2.2 runs `/sc:cli-eval run --unattended` with no `--suite` and demands a `blocked` contract (line 200).
  - workflow: the contract is at `.dev/tasks/to-do/<id>/return-contract.yaml` (line 92) with a generated `<id>`, so the path is not known before dispatch, and the P1 fix is to write the contract "for pre-creation STOPs too" (line 92), i.e. when `<id>/` does not exist yet (`INV-B:272`, "Not written for pre-creation STOPs").
  - adversarial: the fix names `<output>/adversarial/return-contract.yaml` (line 83), which is not `<output-dir>/return-contract.yaml` for `--output <dir>`.
- **Grading check**: An implementer who follows the stated text as written builds, for tdd, a writer that creates `<TDD file path>/return-contract.yaml` (or no contract), and for cli-eval and workflow-before-creation a writer with no stated target; this is wrong because AC-2.2 and 7.2 steps 3 and 4 (lines 182-183, 200) then cannot pass: there is no defined path for `worker_done --report-path` or for `test -s <contract>`. Two stated texts (WC-4 and the tdd/init-lite/cli-eval/workflow rows) contradict, and an acceptance criterion cannot pass.
- **Concrete attack (Whittaker, Sentinel Collision)**: `--output` is a control value that means "directory" in WC-4 and "file" in rows 87 and 90. State trace: coordinator dispatches `/sc:tdd "auth" --unattended --output .dev/tdd/auth.md`; the bare topic hits the gate; WC-2(c) says write `<output-dir>/return-contract.yaml` with `status: blocked`; `<output-dir>` is `.dev/tdd/auth.md`, a path that is (or will become) a file. The contract is not written, the worker has no `--report-path`, WC-5 maps "no report exists" to `--outcome failed` with no `blocked_question`, and AC-2.2 fails.
- **Recommendation**: narrow WC-4 so the contract path is "the path the brief names, and each section 3 row states its contract path pattern"; for the five rows above add the exact pattern (for example "beside the `--output` file as `<name>.return-contract.yaml`" for file-valued flags, and a brief-supplied directory for cli-eval and workflow). Rationale: this deletes the unstated assumption instead of adding a mechanism, and it makes line 62, line 73 and the 7.2 checks agree.
- **Quality impact**: Consistency +2, Testability +1.

### F-02 (MAJOR, blocking, priority High): AC-1.1 and the P1 scope contradict three other stated texts
- **Expert**: Fowler (pipeline and interface), Whittaker (Divergence), Cockburn (who the acceptance serves).
- **Issue**: AC-1.1 (line 195) asserts that "every command in sections 3.1-3.2 has a `## Unattended mode` section naming `return-contract.yaml` and `~/.claude/WORKER-CONTRACT.md`", and P1 scope (line 159) has "the `--unattended` flag accepted by every command in sections 3.1 and 3.2". That is 37 commands. Three stated texts disagree with it:
  1. `/sc:load`: the row says "Report: none (see note)" and "use it as a step inside another worker's brief, not as its own Task" (line 112); the Decisions row says "a report file would be an unrequested addition" (line 265).
  2. `/sc:implement`, `/sc:post-release`, `/sc:pr-submit` are P4 and held "until D2-D4" (lines 154, 162, 225); under the recommended D3(a) "no pr-submit changes in Phase 4" and pr-submit is "coordinator or person only" (line 240; also line 139).
  3. P1's own Commands column names 13 commands (9 from 3.2 plus the 4 fixes of 3.1, line 159), while 24 of the 37 (22 of them in P2 to P4, plus brainstorm and init-lite) have their gate resolutions later, so after P1 the flag exists without the behavior WC-2 requires ("never calls `AskUserQuestion`", line 60).
- **Grading check**: An implementer who follows the stated text as written adds the section and the flag to all 37 commands in P1, including the P4 safety-rule and outward-action commands before the user answers D2-D4 and a report-naming section on `/sc:load`; this is wrong because it either contradicts line 154 ("Later phases do not start until the earlier phase's checks pass") and D3(a), or leaves AC-1.1 unable to pass for load. Two stated texts contradict and an acceptance criterion cannot pass without assumption.
- **Quantity detail** (FR-18/FR-19 consistency check; graded by consequence, see Quantity Flow Diagram): the consumer "AC-1.1" expects N=37 sections in P1, the producer "P1 Commands column" delivers M=13.
- **Recommendation**: narrow AC-1.1 to "every command whose row names phase P1, plus the four P1 fixes", say that `load` gets no section, and move implement, post-release and pr-submit out of the P1 flag scope (they gain the flag in P4). Rationale: narrowing three sentences resolves the contradiction without adding a rule.
- **Quality impact**: Consistency +2, Completeness +0.5.

---

Medium findings (warnings; each needs a guess about which of two allowed readings the implementer takes, or states a requirement the document never states, so none is blocking under the grading check):

### M-01 (Medium, priority Medium): heartbeat cadence cannot be met during foreground fan-out
- **Expert**: Nygard. WC-10 (line 68) requires "a heartbeat every 5 minutes while working" and splits only "a poll wait, a long eval". WC-7 (line 65) forbids subagents from sending lifecycle messages. A foreground Agent-tool fan-out (tdd 6-10 agents `INV-B:221`, cleanup-audit waves `INV-A:42`, adversarial Mode B `INV-A:35`) blocks the top-level session in one call far longer than 5 minutes, so neither the worker nor its subagents can heartbeat. The cadence itself comes from this worker's preamble, not a guide, and whether Orca uses heartbeat age is UNVERIFIED (`CAPS:130`, `CAPS:182`). Why Medium: the wrong outcome needs a guess about how Orca reads a silent worker (`CAPS:127` says absence never authorizes stop). Recommendation: say fan-out calls are exempt, or tie the requirement to what Orca is shown to use.

### M-02 (Medium, priority Medium): the "after readiness" claim is stated as fact
- **Expert**: Nygard. Section 1.4(2) (line 44) says a command's own `AskUserQuestion` "comes *after* readiness, so it does not fail `worker-start`". But for Claude the task is passed on the command line at launch (`CAPS:47`, `promptInjectionMode: 'argv'`), so a command whose first step asks starts running before the fresh-composer wait (`CAPS:47`); the spec's own evidence only covers a shell wrapper's prompt (`EVIDENCE.md:39` via `CAPS:49`). This is not listed in the UNVERIFIED items (lines 271-285). Why Medium: it is an inference the spec does not mark; the harm needs the worse reading. Recommendation: mark it UNVERIFIED, since WC-2 holds either way.

### M-03 (Medium, priority Medium): "keep their fields" versus a fixed `status` vocabulary
- **Expert**: Wiegers. WC-4 (line 62) says commands that already write a contract "keep their fields and add the missing ones", and fixes `status` to `succeeded|partial|failed|blocked`; the Decisions row (line 262) chose the fixed set over "copy each command's own statuses". No inventory line records the existing `status` values of workflow, reflect, brainstorm or adversarial contracts (`INV-B:272`, `INV-B:112`, `INV-A:35`, `INV-A:97`). If any uses other values, both sentences cannot hold. Recommendation: record the existing value sets, or state that `status` is the one field that is replaced.

### M-04 (Medium, priority Medium): stale, empty or malformed contract
- **Expert**: Whittaker (Sequence Attack). WC-5 (line 63) tests only "no report exists". Sequence: attempt 1 writes `status: blocked`; WC-3 (line 61) has the session re-invoke the command with the answer; the command resumes (WC-6, line 64) and crashes before writing; the old file is read as the outcome, `--outcome failed` is sent with a stale question, or a stale `succeeded` is reported. An empty file or a `status` outside the four values has no stated mapping either; 7.2 step 4 (line 183) checks it only in tests. Recommendation: one sentence that the contract is deleted or overwritten at command start, and an unreadable contract counts as no report.

### M-05 (Medium, priority Medium): `--post-pr` does not exist in the inventory
- **Expert**: Wiegers, Whittaker. The auggie-review row (line 100) says posting "returns only with an explicit `--post-pr` in the brief" and "Other required change: none". The inventory shows only the negative flag `--no-post-pr` with posting on by default (`INV-A:38`, `INV-A:78`). A new positive flag is a change, and `--unattended` "implies `--no-post-pr`", so `--unattended --post-pr` has no stated precedence. Why Medium: AC-2.4 (line 202) only tests the default. Recommendation: list the flag in the "Other required change" column and state precedence.

### M-06 (Medium, priority Medium): "paid external run" is undefined
- **Expert**: Wiegers. WC-9 (line 67) turns off "any default that ... calls a paid external run". research (Tavily, `INV-B:134`), review-translation (Tavily, `INV-B:144`) and `recommend --plugin` (`INV-B:104`) exist to call web search; cli-eval run executes real evals (`INV-A:44`). The rows do not say whether these are covered. Applied literally the rule disables research. Recommendation: define the term or list the commands it covers.

### M-07 (Medium, priority Low): AC-C1 versus the P0 deliverables
- **Expert**: Fowler. AC-C1 (line 172) greps `src/superclaude/core` and expects no hit for `orca(-ide)? (orchestration|worktree|terminal|agent)`, in every phase including P0. P0 (line 158) adds `WORKER-CONTRACT.md` and an Orca section of `HOW-WE-WORK.md`, both under `core/` (`CAPS:12-13` shows the guide commands; SA-2, line 147, even allows an example question channel "inside the contract file"). Whether the wording avoids the pattern is a guess. Recommendation: exclude the contract file and the routing guide section from the grep, or state the wording constraint.

### M-08 (Medium, priority Low): SA-3 versus WC-4 on when the contract is written
- **Expert**: Adzic. WC-4 writes the contract "in unattended mode" (line 62); SA-3 (line 148) permits the contract and report files "only in unattended mode or when the caller passes the new output flag". A person passing `--output` without `--unattended` is covered by one and not the other; AC-1.3 (line 197) tests only the no-flag case. Recommendation: choose one trigger.

### M-09 (Medium, priority Medium): tasklist Stage 10.5 nesting
- **Expert**: Newman. The tasklist row (line 122) says its reflect fan-out "runs one layer below the worker, inside Claude Code's nesting limit, `INV-A:14`". `INV-A:14` states the docs limit (three layers) and says nothing about reflect's own children (reflect agents, Tier 2 reviewers, adversarial advocates; `INV-B:210`, `INV-B:111`). `INV-B:215` and `INV-B:322` ask for the reflect fan-out to be top-level or mark the nested behavior UNVERIFIED; the Decisions table (lines 258-269) records no reason for the different choice (pass `--unattended`). Recommendation: add the depth count or mark it UNVERIFIED, and record the decision.

### M-10 (Medium, priority Medium): how the worker invokes the command, and `--unattended` in P0
- **Expert**: Cockburn, Adzic. Section 2.3 (line 73) says the brief states "the exact command line including `--unattended`", and P0's brief template (line 158) is built on it, but P0 runs commands that do not accept the flag until P1 (AC-0.4, line 194 uses lines without it). Also WC-7 (line 65) says "runs the command directly", but the prior proof used a Skill call through an Agent-tool subagent (`INV-A:13`, `CAPS:156`, spec line 43); nothing says whether a preamble-prefixed prompt starts a `/sc:` line at all, or whether the worker calls the Skill tool (the project rule makes the Skill call mandatory for a message starting with `/sc:`). Recommendation: state the invocation form in 2.3 and the P0 brief wording.

---

=== ARCHITECTURE ANALYSIS ===

Architecture findings (F-02, M-01, M-02, M-07, M-09) are listed above with their ids. Summary of the architectural reading, by expert:

- **Fowler (interfaces, boundaries)**: the central decision (coordinator above, commands as self-contained units, no Orca calls in commands, `--unattended` as the single seam, one shared contract file) is coherent and its evidence chain checks against `CAPS:86-103,145-161` and `INV-A:76-98`. The seam is where it leaks: F-02 (flag acceptance without behavior), M-07 (contract mentions vs the no-Orca grep).
- **Nygard (failure modes)**: the stall mode is correctly identified as silent, not a readiness failure (section 1.4(2)), but M-02 weakens the claim it rests on, and M-01 leaves long fan-outs with no liveness story. Good: WC-5 maps failure explicitly and AC-2.2 tests the gate path.
- **Newman (evolution, compatibility)**: SA-1 to SA-6 protect the standalone surface and AC-C5 makes additivity checkable. M-09 shows one place where an architectural claim is assumed.
- **Hohpe (messages and ordering)**: the message flow (Task, brief, `worker_done`, report, outcome) is right; WC-5 ("exactly once"), WC-12 and WC-3 are consistent with `CAPS:58-67,73-78`. The gap is the contract as the message payload pointer (F-01, M-04).
- **Wiegers, Adzic, Cockburn (requirements)**: each requirement carries an owner and evidence, which is above the norm; weaknesses are F-01 (not implementable for five commands), M-03, M-05, M-06, M-08.

---

## Guard Condition Boundary Table (Nygard builds, Crispin's completeness duty folded in by the lead, Whittaker attacks)
Guards identified in the candidate: G1 readiness limit (WC-1), G2 heartbeat and wait split (WC-10), G3 the `--unattended` switch (D1, WC-2), G4 status to outcome map (WC-5), G5 contract-file existence and location (WC-4), G6 `--monitor` ordinal (pr-submit row), G7 task confidence 0.70 (task row), G8 nested depth (WC-8). Classes left out are given with a one-line reason after the table. Status GAP entries carry the finding that grades them (FR-8, FR-9).

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|---|---|---|---|---|---|---|
| G1 readiness limit | WC-1, line 59 | Typical | fallback 30 s | passes | start returns ready (`CAPS:49`) | OK |
| G1 readiness limit | WC-1, line 59 | Maximum/Overflow | fallback above about 45 s | fails | "well inside the readiness limit (default 60 s)", no numeric ceiling although `CAPS:49` gives about 45 s | GAP (N-02) |
| G2 heartbeat / wait split | WC-10, line 68 | Zero/Empty | no blocking call | n/a | heartbeat every 5 min while working | OK |
| G2 heartbeat / wait split | WC-10, line 68 | Typical | poll wait of 4 min | true | split into waits of at most 4 min | OK |
| G2 heartbeat / wait split | WC-10, line 68 | Legitimate Edge Case | one call of 4.5 min | false (not over 5 min) | not split, so a heartbeat gap can pass 5 min | GAP (N-02) |
| G2 heartbeat / wait split | WC-10, line 68 | Maximum/Overflow | foreground Agent fan-out over 5 min | not addressed | unspecified; WC-7 bars subagent heartbeats | GAP (M-01) |
| G3 `--unattended` | D1 (a), WC-2, lines 51, 60, 228 | Zero/Empty | flag absent | false | SA-1: today's behavior (line 146) | OK |
| G3 `--unattended` | D1 (a), WC-2 | One/Minimal | standalone token | true | gates resolve per section 3 row | OK |
| G3 `--unattended` | D1 (a), WC-2 | Sentinel Value Match | the string inside quoted free text | unspecified | unspecified | GAP (N-03) |
| G3 `--unattended` | WC-2 with `--interactive` | Legitimate Edge Case | both flags | unspecified for brainstorm, release-split, roadmap | "refused" is stated only for cleanup, improve, roadmap, pr-submit `--monitor 1` | GAP (N-03) |
| G4 status to outcome | WC-5, line 63 | Typical | `succeeded` or `partial` | true | `--outcome succeeded` | OK |
| G4 status to outcome | WC-5, line 63 | One/Minimal | `failed` or `blocked` | true | `--outcome failed` | OK |
| G4 status to outcome | WC-5, line 63 | Zero/Empty | no report file | true | `--outcome failed` | OK |
| G4 status to outcome | WC-5, line 63 | Sentinel Value Match | empty file, `status` missing or not one of the four, or a stale file | unspecified | unspecified | GAP (M-04) |
| G5 contract location | WC-4, line 62 | Typical | brief passes `--output <dir>` | true | `<dir>/return-contract.yaml` | OK |
| G5 contract location | WC-4, line 62 | Zero/Empty | no directory passed (cli-eval, workflow before creation) | undefined | none stated | GAP (F-01) |
| G5 contract location | WC-4, line 62 | Sentinel Value Match | `--output` holds a file (tdd, init-lite) | undefined | none stated | GAP (F-01) |
| G6 `--monitor` ordinal | pr-submit row, line 114 | Legitimate Edge Case | `1` | true | refused under `--unattended` | OK |
| G6 `--monitor` ordinal | pr-submit row, line 114 | Typical | `3` (default) | false | no y/n gate (`INV-B:89`) | OK |
| G7 task confidence | task row, line 121 | Typical | 0.50 | true | blocked | OK |
| G7 task confidence | task row, line 121 | Legitimate Edge Case | exactly 0.70 | false ("below 0.70") | proceeds | OK |
| G7 task confidence | task row, line 121 | Zero/Empty | confidence not computed | unspecified | unspecified | GAP (N-03) |
| G8 nested depth | WC-8, R1, lines 33, 66 | Typical | setting 1 | true | `worker-start` from a worker is refused (`CAPS:97-99`) | OK |
| G8 nested depth | WC-8, R1 | Maximum/Overflow | setting above 1 (D5 (b)) | false | WC-8 still forbids the call | OK |

Classes left out: G6 Zero (`--monitor 0`) and Maximum, because the gate exists only at 1 (`INV-B:89`) and the row says nothing else; G7 Maximum, because above 0.70 there is no gate; G8 Zero/Empty, because a malformed setting falls back to 1 (`CAPS:100`); G1 Zero, because a 0 s fallback is a prompt that never waits; G5 Maximum/Overflow, because the contract is one file.
Gate check (FR-10): the table lists every guard found, every cell is filled, and every omitted class has its reason, so synthesis may proceed. FR-8 grading: the GAPs name no wrong outcome beyond those already graded in F-01, M-01 and M-04; G2/G3/G7 GAPs are minor.

## Quantity Flow Diagram (Fowler annotates, Whittaker attacks)
```text
[Source: 43 commands in cmd/ (21 INV-A + 22 INV-B)] --> [Stage 1: verdict split, section 3 / 4] --> 10 ready (3.1) + 27 needs-change (3.2) + 6 coordinator-only (4) = 43   (conserved)
                                                       |
                                                       v
                                  [Stage 2: worker-capable = 3.1 + 3.2 = 37]
                                                       |
            +------------------------------+-----------+------------------------------+
            v                              v                                          v
 [Consumer: P1 scope line 159]   [Consumer: AC-1.1 line 195]               [Consumer: phase rows, section 6]
 expects 37 (flag accepted)      expects 37 sections                         P1 13 (9 + 4 fixes) + P2 15 + P3 4 + P4 3 = 35
                                                                             + brainstorm, init-lite (no change) = 37   (conserved)
 <-- MISMATCH: P1 delivers 13, the other 24 get the flag in P1 but their gate behavior in P2 (15 incl. 4 of 3.1), P3 (4), P4 (3), or never (2)  -->   (F-02)
 [Consumer: load row] expects 0 report sections -- AC-1.1 counts it among the 37                                                              (F-02)
```
Count check of the phase rows against section 3: P1 = analyze, build, business-panel, design, document, explain, index, load, test (9) plus fixes to adversarial, cleanup-audit, index-repo, workflow (4); P2 = auggie-review, cleanup, cli-eval, cli-portify, improve, recommend, research, review-translation, spec-panel, task, tasklist (11) plus reflect, release-split, tdd, troubleshoot (4); P3 = roadmap, save, validate-roadmap, validate-tests; P4 = implement, post-release, pr-submit. All reconcile with the "Phase" column of section 3.2 and the "(P1/P2)" tags of 3.1.

## Adversarial analysis (Whittaker; FR-3 template)
1. I can break this specification by **Sentinel Collision Attack**. The invariant at **WC-4 (line 62)** fails when **`--output` holds a file path, as for tdd and init-lite**. Concrete attack: `/sc:tdd "auth" --unattended --output .dev/tdd/auth.md` with a bare topic. Before: no contract, `.dev/tdd/auth.md` absent. After a literal WC-4 write: target `.dev/tdd/auth.md/return-contract.yaml`, parent is not a directory; no contract; WC-5 sends `failed` with no `blocked_question`. Severity: MAJOR (F-01).
2. I can break this specification by **Divergence Attack**. The invariant at **AC-1.1 and P1 scope (lines 159, 195)** fails when **the command is load or a P4 command**. Concrete attack: implement P1 literally: `load.md` gains a section naming `return-contract.yaml` (contradicting line 265); `pr-submit.md` gains `--unattended` while D3 is still open (contradicting line 240). Severity: MAJOR (F-02).
3. I can break this specification by **Sequence Attack**. The invariant at **WC-3 with WC-6 (lines 61, 64)** fails when **a re-invoked command dies before writing its contract**. Concrete attack: round A writes `status: blocked`; the coordinator answers; round B resumes and crashes; the worker finds a file, so WC-5's "no report exists" branch does not fire and it reports the stale status. Severity: MAJOR (M-04).
4. I can break this specification by **Accumulation Attack**. The invariant at **WC-10 (line 68)** fails when **a single foreground fan-out call outlasts 5 minutes**. Concrete attack: `/sc:tdd` with 8 agents runs 20 minutes in one call; no heartbeat is sendable by the top-level session or, per WC-7, by the subagents. Severity: MAJOR (M-01).
5. I can break this specification by **Zero/Empty Attack**. The invariant at **WC-4 `blocked_question` (line 62)** fails when **the blocked question is the empty string**. Concrete attack: contract `status: blocked`, `blocked_question: ""`; WC-4 does not require it non-empty (only AC-2.2, line 200, does), so a coordinator cannot answer. Severity: MINOR (folded into N-03).

## Standard-format summary (YAML)
```yaml
specification_review:
  original_spec: .dev/orca-command-refactor/specs/orca-worker-contract-spec.md
  review_date: 2026-11-10
  expert_panel: [wiegers, adzic, cockburn, fowler, nygard, newman, hohpe, whittaker]
  focus_areas: [requirements, architecture]
quality_assessment:
  overall_score: 6.5
  clarity: 7
  completeness: 7
  testability: 6
  consistency: 6
critical_issues:
  - {category: requirements, severity: MAJOR, expert: wiegers, issue: "F-01 WC-4 contract path undefined for tdd, init-lite, cli-eval, workflow, adversarial", recommendation: "name the contract path per row or let the brief name it"}
  - {category: architecture, severity: MAJOR, expert: fowler, issue: "F-02 AC-1.1 and P1 scope contradict load row, P4 hold and D3(a)", recommendation: "narrow AC-1.1 and the P1 flag scope to the P1 rows"}
expert_consensus:
  - "The decision (Orca above, commands as units, one seam) is well supported by the inventories."
  - "The weak points are the acceptance checks and the contract-location rule, not the design."
improvement_roadmap:
  immediate: [F-01, F-02]
  short_term: [M-01, M-02, M-03, M-04, M-05, M-06]
  long_term: [M-07, M-08, M-09, M-10]
adversarial_analysis:
  - {methodology: sentinel-collision, severity: MAJOR, invariant: "WC-4 line 62", trigger: "--output holds a file", ref: F-01}
  - {methodology: divergence, severity: MAJOR, invariant: "AC-1.1 line 195", trigger: "load or P4 command", ref: F-02}
  - {methodology: sequence, severity: MAJOR, invariant: "WC-3/WC-6 lines 61, 64", trigger: "re-invoked command dies before writing", ref: M-04}
  - {methodology: accumulation, severity: MAJOR, invariant: "WC-10 line 68", trigger: "fan-out call over 5 minutes", ref: M-01}
```

## Follow-up candidates (Medium and minor findings; none triggers a revision)
Medium: M-01, M-02, M-03, M-04, M-05, M-06, M-07, M-08, M-09, M-10 (described above).
Minor notes:
- N-01 (Wiegers): section 1.1 (line 16) says command changes are "limited to the worker contract"; section 3 and SA-4 (line 149) list further defect fixes (explain tools, business-panel frontmatter, load usage line, roadmap and validate-roadmap drift). Consistent in effect, loosely worded.
- N-02 (Nygard): WC-1 (line 59) has no numeric ceiling; the evidence gives about 45 s (`EVIDENCE.md:56` via `CAPS:49`). WC-10's 4-minute split leaves a 4 to 5 minute call unsplit (table G2).
- N-03 (Whittaker): `--unattended` inside quoted text, `--unattended` with `--interactive` on commands that do not list "refused", an empty `blocked_question`, and a missing confidence value are unspecified (table G3, G7; attack 5).
- N-04 (Adzic): P1 says "No person gate is involved" (line 159), but its own rows refuse or pin a mode: explain `--format interactive`, business-panel `--mode socratic`, test `--watch`, index knowledge-base mode (lines 102, 108, 111, 123).
- N-05 (Hohpe): AC-0.4 step 4 (line 194) uses adversarial's "existing report file" whose name is not fixed until P1 (line 83); 7.2 step 6 (line 185) reads `git status --short` in a worktree that other workers and the coordinator share (`CAPS:115`).

Issue question: the review-loop rule says the session that ran the review asks the user once whether to open an issue for the follow-up list. This run is a worker whose final reply is restricted, so the question was not asked and no issue was created; the coordinator should put it to the user.

## Reviser brief
Blocking finding ids: **F-01, F-02**.
Restated rules (the reviser reads this report, not the command): revise only text a blocking finding names; add no rule, mechanism or section that no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size of the candidate before and after, and the bytes added and deleted per finding id; leave Medium and minor findings alone; return the candidate once and do not award yourself a PASS.
- F-01: text named: WC-4 (line 62), section 2.3 (line 73), the tdd (line 90), init-lite (line 87), cli-eval (line 104), workflow (line 92) and adversarial (line 83) rows, and AC-2.2 / 7.2 step 3 only as they depend on the contract path.
- F-02: text named: AC-1.1 (line 195), the P1 scope sentence (line 159), the load row (line 112), and the statement of what P4 holds (line 162) as they relate to the `--unattended` flag and the section.

verdict: FAIL

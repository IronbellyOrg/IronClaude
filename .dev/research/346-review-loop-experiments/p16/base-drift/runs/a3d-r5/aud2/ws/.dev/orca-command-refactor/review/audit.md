review: 1 of 3

# /sc:spec-panel audit: Orca worker-contract spec

| Field | Value |
|---|---|
| Command | `/sc:spec-panel @.dev/orca-command-refactor/specs/orca-worker-contract-spec.md --mode critique --focus requirements,architecture` |
| Scope | Labelled whole-document audit of the final spec. First review of the whole document, per the FIRST-REVIEW prompt in `~/.claude/rules/prompts/document_review_loop_prompts.md` (read in full, lines 1-55). |
| Candidate | `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md` (285 lines) |
| Candidate sha256 | `fb9100899806def3c0456f91fd02f9793207fcb28f4789f5ae6d358a15a2ce5f` |
| Baseline / prior | none given; `baseline: n/a` (first review, not a re-review) |
| Reviewer model actually used | Sonnet 5.5 (`claude-sonnet-5-5`) |
| Review date | 2026-11-10 |
| Input type | Specification. Not a TDD and not a PRD, so TDD/PRD scoping and the roadmap frontmatter steps do not apply. |
| Improve step | Not run. The brief says edit nothing else, and the command's Boundaries forbid changing a spec without consent. No improved spec was written. |

Citation key: `SPEC:N` is line N of the candidate. `INV-A:N`, `INV-B:N` and `CAPS:N` are lines of `inventory/commands-a.md`, `commands-b.md` and `orca-capabilities.md`. `README:N` is `.dev/orca-command-refactor/README.md`. `CMD:N` is line N of the `command.md` that defines this command.

## Coverage

- Read in full: README (39 lines), the candidate (285 lines), `inventory/commands-a.md` (120), `inventory/commands-b.md` (323), `inventory/orca-capabilities.md` (188), and the review-loop prompts file.
- Checked by arithmetic: 10 ready + 27 needs-change + 6 coordinator-only = 43 (SPEC:76,81-125,128-137). The 3.1 and 3.2 row counts are 10 and 27. They agree with INV-A:73 (5/13/3) plus INV-B:278 (5/14/3). The phase lists at SPEC:158-162 cover every command exactly once (P1 13, P2 15, P3 4, P4 3, plus the 6 in section 4 = 41, with `load` counted in P1 and brainstorm/init-lite getting only the flag).
- Checked against evidence I can read: every `INV-A:`, `INV-B:` and `CAPS:` citation in SPEC:19-70, 76-137, 214-285. I spot-checked about 120 of them against the target lines and found no mis-citation.
- UNVERIFIED (cannot be checked inside this workspace): every `src/superclaude/...` path:line, every `CLAUDE.md:N`, `Makefile:N`, `pyproject.toml:38`, `.dev/evals/.../EVIDENCE.md:N`, `.dev/codegraph-migration/...:N`, and the 340-citation check claimed at SPEC:285. Where the inventories quote those lines, I treated the quote as the inventory's claim, not as verified.
- Not covered: the rest of the repo, any behaviour of `orca-ide` itself, and anything past the files above.

## Standard-format summary

```yaml
specification_review:
  original_spec: .dev/orca-command-refactor/specs/orca-worker-contract-spec.md
  review_date: 2026-11-10
  expert_panel: [Wiegers, Adzic, Cockburn, Fowler, Nygard, Whittaker, Newman, Hohpe, Crispin, Gregory, Hightower]
  focus_areas: [requirements, architecture]
quality_assessment:
  overall_score: 7.0
  clarity: 7.5
  completeness: 7.0
  testability: 6.0
  consistency: 6.5
critical_issues:
  - {id: B-1, category: testability, severity: MAJOR, grade: blocking, expert: Crispin, issue: "AC-0.4 requires a contract that P0 does not yet produce", recommendation: "Narrow 7.2 step 3 for P0"}
expert_consensus:
  - "The decision (Orca on top, commands as workers) is well supported and the rejected alternative is argued with evidence."
  - "The phase order and the coordinator-only split are sound."
  - "The weak points are the acceptance checks and a few places where the worker contract is silent on retry, output location and heartbeats."
improvement_roadmap:
  immediate: [B-1]
  short_term: [M-1, M-2, M-3, M-4, M-5, M-6, M-7]
  long_term: [M-8, M-9, M-10, M-11, M-12, M-13]
adversarial_analysis: see "ADVERSARIAL ANALYSIS" below
```

## Panel commentary (fixed review order)

1. **Wiegers** (requirements): The 12 WC rules are numbered, owned and evidenced, which is good. Several are not measurable as written: WC-6 "fresh output directory" (M-1), WC-4's missing-directory case (M-2) and WC-9's "the command's own explicit flag", where the flag does not exist (M-9).
2. **Adzic** (examples): The `/sc:troubleshoot "login fails" --unattended --output ...` example at SPEC:228 and the gate-trigger examples at SPEC:200 are useful. Concrete cases for retry and for a file-valued `--output` are missing, so M-1 and M-2 stay open.
3. **Cockburn** (actors and goals): The actors are clear: coordinator, worker session, command, person (SPEC:57, 72-73). The goal "a person who runs a command in a plain session sees no change" is stated and testable (SA-1, SA-3, AC-1.3). Nothing is missing here.
4. **Fowler** (architecture): Keeping Orca out of commands (SA-2, WC-8) and putting the shared rules in one installed file (SPEC:52) is the right boundary. The flag-versus-detection choice (D1) is well framed. One interface smell: WC-4 ties the report location to the shape of `--output` (M-2).
5. **Nygard** (failure modes): Blocked, failed and partial are all mapped (WC-5). The gaps are retry into an old directory (M-1), heartbeats during Agent-tool waits (M-5) and the interim state between P1 and P2 (M-3).
6. **Whittaker** (adversarial): See the section below.
7. **Newman** (evolution and compatibility): Additive-only edits (SA-4, AC-C5) protect existing callers. A fixed four-value `status` may not match what existing contracts already write (M-10).
8. **Hohpe** (message flow): The ask/reply/worker_done flow is correct against CAPS:58-81. WC-3 uses "may", while AC-2.2 expects a fixed outcome (M-13).
9. **Crispin** (testing): The live check in 7.2 is concrete. The acceptance criteria have three problems: B-1, M-7 and M-13.
10. **Gregory** (quality conversation): The five open decisions each carry options and a recommendation (SPEC:225-253). That is a good pattern. P2 says it touches no safety rule, which cli-portify's row contradicts (M-6).
11. **Hightower** (operations): Standalone use is protected (section 5). The Orca executable name and absence cases are covered (R2, R4). Nothing further.

=== REQUIREMENTS ANALYSIS ===

### B-1 (BLOCKING, MAJOR): AC-0.4 requires a contract that Phase 0 does not produce
- Expert: Crispin, with Wiegers.
- Grading sentence: An implementer who follows the stated text as written builds a Phase 0 gate whose step 3 needs a WC-4 contract for `/sc:troubleshoot`, and that gate is wrong because troubleshoot writes no contract before P1 (INV-B:242), so AC-0.4 cannot pass.
- Evidence:
  - AC-0.4 says "steps 1-3 and 5-7 pass; step 4 uses the command's existing report file, since the contract arrives in P1" (SPEC:194). Only step 4 is relaxed.
  - Step 3 of the live check requires that the `--outcome` "matches the contract's status under WC-5" and that the report path "is the WC-4 contract path" (SPEC:182).
  - P0 has "no command edits" (SPEC:158), and the contract is the P1 deliverable (SPEC:159).
  - Troubleshoot: the contract exists "only when `--caller task-unified`" (INV-B:242).
  - Adversarial: the contract filename and location are not fixed until a P1 fix (SPEC:83; INV-A:35,60).
  - Workflow: the contract sits at `.dev/tasks/to-do/<id>/return-contract.yaml` (SPEC:92), not at the WC-4 `<output-dir>/return-contract.yaml` (SPEC:62).
  - Consequence: later phases do not start until the earlier phase's checks pass (SPEC:154,166), and a P0 failure "reopens section 1" (SPEC:194). A check that cannot pass blocks the whole plan.
- Recommendation: say that at P0 step 3 compares `--outcome` with the status or verdict in the command's existing report, and that `--report-path` names that existing file. The rationale is that this is the same relaxation step 4 already has.
- Priority: High. Quality impact: Testability +1.5.

=== ARCHITECTURE ANALYSIS ===

(Findings below are Medium unless marked. Each one fails the grading check because it needs a guess about which of two readings an implementer picks, or because it is a requirement the document never states.)

### M-1 (Medium, MAJOR label): Retry cannot be "fresh" and also write the contract where WC-4 says
- Expert: Nygard. FR-8/FR-9 equivalent: WC-6 and WC-4 interact.
- WC-4 puts the contract at `<output-dir>/return-contract.yaml`, where `<output-dir>` is what the coordinator passed (SPEC:62). WC-6 says a retry "writes each run into a fresh output directory" (SPEC:64).
- A retry worker gets the same brief (SPEC:73), so it gets the same `--output`. If the command writes straight into that directory, the retry overwrites the first attempt's contract. If it makes a fresh subdirectory, the contract is no longer at the path the coordinator knew before dispatch.
- Section 2.3 does not tell the coordinator to pass a new directory on a retry. Most of the 27 rows in 3.2 give "fresh dir" as their resume answer (SPEC:99-125), so this affects most of the plan.
- Recommendation: add one sentence to 2.3 and WC-6: on `--retry-of` the coordinator passes a new output directory, and the command never reuses a non-empty one.
- Priority: High. Impact: Consistency +0.5.

### M-2 (Medium): WC-4 location rule for file-valued `--output` and for no output at all
- Expert: Wiegers, Whittaker (Zero/Empty attack).
- A file-valued `--output` puts the contract in the file's parent directory (SPEC:62). The brief rules prescribe file-valued outputs for `tdd` and `init-lite` (SPEC:87,90). The tdd default is `docs/[domain]/TDD_[COMPONENT].md` (INV-B:222), so two TDD workers for one domain share one parent. Both write `docs/<domain>/return-contract.yaml`, which breaks WC-11 (SPEC:69) and puts a worker file into a docs tree.
- WC-4 also does not say what happens when `--unattended` is passed with no output directory at all. WC-2(c) says "write the report and stop" (SPEC:60), but not where.
- Recommendation: state that the coordinator gives each worker its own output directory, and that `--unattended` with no output location resolves as blocked, reported in chat only.
- Priority: High.

### M-3 (Medium): Phase order leaves `--unattended` live and unsafe between P1 and P2
- Expert: Whittaker (Sequence attack), Nygard.
- P1 adds the flag "accepted by every command in sections 3.1 and 3.2 except the P4 commands" and writes the contract (SPEC:159). AC-1.1 asserts every such command has an `## Unattended mode` section (SPEC:195). Gate conversion, including turning off auggie-review's default PR posting and its remediation offer, is P2 (SPEC:100,160).
- Between the two phases a brief with `--unattended` on auggie-review, cleanup, improve or cli-eval is accepted, yet the command still posts or waits. This breaks WC-9 and WC-2 (SPEC:60,67). Nothing says a coordinator must not dispatch a gated command before its phase. Section 2.1 also says each section lists "only its own gate resolutions" (SPEC:52), which cannot yet be true for a P2 command in P1.
- Recommendation: for commands whose gate conversion is in P2 or P3, P1 should refuse `--unattended` (resolve as blocked) instead of accepting it as a no-op.
- Priority: High.

### M-4 (Medium): How a worker runs a command is not defined
- Expert: Fowler, Hohpe.
- The decision is "one worker runs one command" (SPEC:16), run "directly" (WC-7, SPEC:65), with "the exact command line" in the brief (SPEC:73). Claude workers receive the task on the command line behind a preamble (CAPS:47,76), so the message does not begin with `/sc:...`.
- The only direct evidence is `skill-direct` through an Agent-tool subagent (SPEC:43; INV-A:13). 19 commands have no skill, so there is no skill-direct route for them (INV-A:70; INV-B:8).
- Section 1.4 names the missing direct-route proof but not this specific mechanism question. AC-0.4 would reveal it only for three commands that all have skills.
- Recommendation: add a P0 task to find out how a worker invokes a skill-less command, and a line in the contract file saying how.
- Priority: High.

### M-5 (Medium): Heartbeats cannot be sent while a command waits on Agent-tool subagents
- Expert: Nygard.
- WC-10 says the worker heartbeats every 5 minutes and splits long Bash waits (SPEC:68). WC-7 says only the top-level session sends lifecycle messages (SPEC:65). E4 says commands keep their own fan-out (SPEC:24). A foreground fan-out (tdd, cleanup-audit with 7-8 concurrent agents, adversarial, roadmap) is a single wait in the top-level session that is longer than 5 minutes. The splitting rule cannot be applied to it, and subagents may not heartbeat.
- The consequence is mild because absence never authorizes a stop (CAPS:122-126), but WC-10 as written cannot be met by most of the 37 worker-capable commands.
- Recommendation: either say heartbeats are best effort during fan-out waits, or say how the top-level session gets control back.
- Priority: Medium.

### M-6 (Medium): cli-portify approvals become a coordinator flag with no user decision
- Expert: Gregory, Cockburn.
- The three approval gates resolve as blocked, and `--resume <contract>` "counts as approval of the gate the contract names" (SPEC:105). A coordinator, which is an agent, can pass that flag unattended.
- D2 treats the same shape (an agent approving) as a user decision for implement (SPEC:233-236). P2 claims "These changes touch no safety rule" and "needs no user decision" (SPEC:154,160). The cli-portify row contradicts both. The command writes into `src/superclaude/cli/<name>/` by default (INV-A:45), so the gate guards a source-tree write.
- Recommendation: add cli-portify to the D2 family (a user decision), or say that the resume approval must quote the person.
- Priority: Medium.

### M-7 (Medium): Three acceptance checks cannot pass as literally written
- Expert: Crispin.
- AC-2.3: a "happy-path run" must end `--outcome succeeded` (SPEC:201), yet every cli-portify run stops at an approval gate (SPEC:105). Only a chain of resumed runs can succeed.
- AC-1.2: "each P1 command" must pass all 7.2 steps with `--unattended --output <dir>` (SPEC:196). P1 includes `load`, which writes no file and is "not its own Task" (SPEC:112,159), and index-repo and cleanup-audit, which have fixed output locations and no `--output` (SPEC:85,86).
- AC-C1 greps `src/superclaude/core` for `orca orchestration|worktree|terminal|agent` and requires nothing (SPEC:172). P0 adds a contract file and an Orca section to core (SPEC:158), and SA-2 allows an Orca example in the contract file (SPEC:147). A lowercase `orca orchestration ask` there would fail AC-C1.
- Recommendation: add a carve-out to each of the three.
- Priority: Medium.

### M-9 (Medium): WC-9 relies on explicit flags that the inventories do not show
- Expert: Wiegers.
- WC-9 turns outward actions on "only through the command's own explicit flag" (SPEC:67). Auggie-review is said to regain posting "only with an explicit `--post-pr`" (SPEC:100), with "Other required change: none". The inventory lists `--no-post-pr`, not `--post-pr` (INV-A:38). Task commit/push and post-release authorization flags are not named either (SPEC:113,121). The failure is safe (nothing posts), but D4(a) (SPEC:245) cannot be carried out without these flags.
- Recommendation: list the new authorization flags in the P2 and P4 rows.
- Priority: Medium.

### M-10 (Medium): Fixed four-value `status` versus "keep their fields"
- Expert: Newman.
- WC-4 says commands with a contract keep their fields and add the missing ones, and `status` is one of four values (SPEC:62). The check at SPEC:183 asserts the four values. Existing contracts (workflow, reflect, adversarial, brainstorm) write a `status`, but the inventories never list its values (INV-B:272; INV-A:35,97).
- If any existing value differs, the P0 and P1 checks fail or the field changes. The spec does not say which.
- Recommendation: inventory the existing values, then either map them or say the field is renamed.
- Priority: Medium.

### M-11 (Medium): `tasklist --unattended` applies reflect remediation with nobody deciding
- Expert: Cockburn, Nygard.
- Stage 10.5 would pass `--unattended` to reflect so "the headless rule applies" (SPEC:122), and reflect's headless rule auto-accepts auto-fixable registers (SPEC:88; INV-B:109). Items that need a human decision still HALT in tasklist (INV-B:209), and the row does not give them a WC-2 resolution. INV-B:215 recommended dropping `--remediate` instead.
- Recommendation: say what happens to `needs_human_decision` items (blocked), and why auto-accept is acceptable.
- Priority: Medium.

### M-12 (Medium): "Ready" commands write fixed paths against WC-11
- Expert: Whittaker (Accumulation attack).
- WC-11 says two workers in one worktree must never write the same file (SPEC:69). Cleanup-audit writes the fixed `.claude-audit/` (SPEC:85) and index-repo writes `PROJECT_INDEX.md` (SPEC:86). The only mitigation is the remark "one audit per worktree at a time", and the 2.3 brief list does not carry it.
- Recommendation: add the one-at-a-time rule to 2.3 as a coordinator duty.
- Priority: Medium.

### M-13 (Medium): Checks do not detect all prohibited waits, and "may ask" conflicts with a fixed outcome
- Expert: Crispin, Hohpe.
- WC-2 forbids `AskUserQuestion`, chat questions and `[yes / no]` offers (SPEC:60). Step 5 only searches the transcript for `AskUserQuestion` (SPEC:184). A plain chat offer is not caught there (INV-A:62), only by a missing `worker_done`. Step 2 passes if `agentWait` is absent as well as if it is null (CAPS:129).
- WC-3 lets the worker "instead ask" (SPEC:61), but AC-2.2 expects `--outcome failed` with a `blocked` contract (SPEC:200). A worker that asks passes neither.
- Recommendation: make the gate-trigger brief say "do not ask", and widen step 5 to the chat-offer forms.
- Priority: Medium.

=== ADVERSARIAL ANALYSIS (Whittaker) ===

I can break this specification by **Sequence Attack**. The invariant at **SPEC:154 ("Each phase ... leaves standalone behaviour unchanged") and SPEC:159** fails when **a coordinator dispatches `/sc:auggie-review <PR> --unattended` after P1 and before P2**. Concrete attack: before, the command posts a PR review by default and then offers remediation (INV-A:38). P1 makes the flag accepted and writes a contract. After P1 the run still posts to GitHub with no prompt and then waits on a chat offer. The state changes from "unknown flag" to "accepted flag, unsafe behaviour". Graded Medium (M-3).

I can break this specification by **Zero/Empty Attack**. The invariant at **SPEC:62 (WC-4)** fails when **`--unattended` is passed with no output directory, or a file `--output` shares a parent**. Concrete attack: two TDD workers with `--output docs/pay/A.md` and `docs/pay/B.md` both write `docs/pay/return-contract.yaml`. The second overwrites the first before the coordinator reads it. Graded Medium (M-2).

I can break this specification by **Sentinel Collision Attack**. The invariant at **SPEC:62-63 (status vocabulary)** fails when **an existing contract already uses a `status` value outside the four**. Concrete attack: a workflow contract with another `status` word makes the SPEC:183 check fail while WC-5 has no row for it. Graded Medium (M-10).

I can break this specification by **Divergence Attack**. The invariant at **SPEC:65-68 (WC-7, WC-10)** fails when **the wait is an Agent-tool fan-out instead of a Bash call**. Concrete attack: a tdd worker waits 25 minutes on research agents. No heartbeat can be sent (top-level blocked, subagents barred), so the coordinator sees silence, which per CAPS:122-126 authorizes nothing. Graded Medium (M-5).

I can break this specification by **Accumulation Attack**. The invariant at **SPEC:64 (WC-6) and SPEC:119 (save)** fails when **a retry reuses a populated output directory**. Concrete attack: attempt 1 writes 6 artifacts and fails; attempt 2 with the same `--output` writes 4 and succeeds. The directory then holds 10 files from two runs with one contract. Graded Medium (M-1).

## Guard Condition Boundary Table

The spec contains thresholds and guards, so the table is produced. Classes that cannot occur for a guard are left out with a reason below the table.

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|---|---|---|---|---|---|---|
| WC-10 wait split | SPEC:68 | Zero/Empty | wait of 0 s | no split | no wait, nothing to split | OK |
| WC-10 wait split | SPEC:68 | Typical | 3 min Bash wait | no split | single wait, heartbeat unaffected | OK |
| WC-10 wait split | SPEC:68 | Legitimate Edge Case | a 4-5 min wait | rule says split only above 5 min | silent: the 4-5 min band plus a 5 min heartbeat can leave a gap | GAP (minor, N-5) |
| WC-10 wait split | SPEC:68 | Maximum/Overflow | 3600 s eval | split into at most 4 min | stated for Bash; Agent-tool waits not covered | GAP (M-5) |
| WC-5 outcome map | SPEC:63 | Zero/Empty | report file missing | `failed` | stated ("no report exists") | OK |
| WC-5 outcome map | SPEC:63 | Zero/Empty | report file present but empty | unspecified | only AC step 4 uses `test -s` | GAP (minor, N-5) |
| WC-5 outcome map | SPEC:63 | One/Minimal | `status: partial` | `succeeded` | stated | OK |
| WC-5 outcome map | SPEC:63 | Legitimate Edge Case | audit verdict FAIL | `succeeded` | stated | OK |
| WC-5 outcome map | SPEC:63,62 | Sentinel Value Match | `status` outside the four values | unspecified | not stated | GAP (M-10) |
| WC-4 report location | SPEC:62 | Zero/Empty | no output directory passed | unspecified | not stated | GAP (M-2) |
| WC-4 report location | SPEC:62 | Typical | directory-valued `--output` | `<dir>/return-contract.yaml` | stated | OK |
| WC-4 report location | SPEC:62 | Legitimate Edge Case | file-valued `--output`, shared parent | contract in parent | collides under WC-11 | GAP (M-2) |
| WC-4/WC-6 retry | SPEC:62,64 | Maximum/Overflow | retry into a populated directory | unspecified | "fresh directory" conflicts with a fixed path | GAP (M-1) |
| WC-2 gate resolution | SPEC:60 | Zero/Empty | command has no gate | no-op | stated ("a no-op where no gate") | OK |
| WC-2 gate resolution | SPEC:60 | Typical | gate with default, flag or blocked | one of three | stated per command in section 3 | OK |
| WC-2 gate resolution | SPEC:60,228 | Sentinel Value Match | `--unattended` text inside a quoted topic | unspecified | D1(a) does not define token parsing | GAP (minor, N-5) |
| WC-3 ask | SPEC:61 | Typical | gate blocked, preamble present | worker may ask | stated, but "may" conflicts with AC-2.2 | GAP (M-13) |
| WC-3 ask | SPEC:61 | Legitimate Edge Case | `ask` times out | resume same message ID | stated | OK |
| WC-9 outward default | SPEC:67 | Zero/Empty | no authorization in brief | action off | stated | OK |
| WC-9 outward default | SPEC:67,100 | Legitimate Edge Case | authorization requested | needs the command's flag | the flag does not exist for auggie-review, task, post-release | GAP (M-9) |
| Task confidence guard | SPEC:121 | Legitimate Edge Case | confidence exactly 0.70 | proceeds ("below 0.70" blocks) | consistent with INV-B:199 | OK |
| Nesting depth | SPEC:66 | Typical | depth 1, worker calls `worker-start` | refused | stated (R1, CAPS:99) | OK |

Classes left out: One/Minimal for WC-10, WC-4 and WC-9 (a count of one changes nothing); Maximum/Overflow for WC-5, WC-2, WC-3 and WC-9 (no counted quantity); Sentinel for WC-10, WC-4 and WC-9 (no reserved value); Typical for WC-5 (all rows above cover it).

FR-8, FR-9 and FR-10 result: the table is complete (every guard enumerated, every cell populated, omitted classes explained). Each GAP was graded with the grading check. None names a concrete wrong outcome that follows from the stated text alone, so all are Medium or minor. The only blocking finding comes from the acceptance-criterion rule (B-1).

## Pipeline Dimensional Analysis

Not triggered as a data pipeline: the spec describes no multi-stage data transformation whose output count changes. The one count flow in the document is conserved: 43 commands = 21 (INV-A:3) + 22 (INV-B:3) = 10 + 27 + 6 (SPEC:76), and 5+5, 13+14, 3+3 match the inventories (INV-A:73; INV-B:278).

```text
[43 commands] --> [INV-A 21: 5 ready, 13 change, 3 coordinator]
              --> [INV-B 22: 5 ready, 14 change, 3 coordinator]
              --> [SPEC: 10 ready, 27 change, 6 coordinator]   (no mismatch)
```

## Consensus and disagreements

- Consensus: the decision, the rejected alternative, the standalone-use protection and the five open decisions are strong. Citation quality against the inventories is high.
- Disagreement: Crispin and Wiegers wanted M-7 and M-13 graded blocking, because an acceptance check that cannot pass is the third blocking branch. Fowler and Cockburn held that only B-1 has no reasonable alternative reading (it is the only case where the author relaxed one step and not its neighbour), while M-7 and M-13 each have a chain-of-runs or obvious-intent reading. The grading check sides with Fowler and Cockburn.

## Follow-up candidates (Medium and minor; none triggers a revision)

Medium: M-1, M-2, M-3, M-4, M-5, M-6, M-7, M-9, M-10, M-11, M-12, M-13 (descriptions above). The label M-8 is not used.

Minor notes:
- N-1: The labels F-1, F-2 and F-3 are cited at SPEC:62, 105, 159 and 195 and defined nowhere in the document. The rule is stated inline each time, so nothing is lost, but the labels are stale.
- N-2: `README:31` is a rule for this planning run's workers. The spec uses it as evidence that git operations need authorization "in this repo" (SPEC:67, 133). The conclusion is supported by `cmd/git.md:14-17,90` (via INV-A:49), so only the citation is overstated.
- N-3: The `command.md` that defines this command already lists `--output`, `--unattended`, `--report-dir` and an `## Unattended mode` section (CMD:22-24, 455-465). This is outside the evidence set. If that file is the repo's current spec-panel, the spec-panel row (SPEC:120) and the `--output-dir` wording at SPEC:62 are stale. UNVERIFIED.
- N-4: validate-roadmap is to be handled by dispatching the `superclaude roadmap validate` CLI (SPEC:124), which is not a command and sits outside the rule "commands stay the units of work" (SPEC:16).
- N-5: Edge gaps in the table: the 4-5 min wait band, an empty report file, and `--unattended` text inside a quoted topic.
- N-6: Brainstorm is "ready" with a plain `--output` (SPEC:84), but its optional `--handoff` waves call tasklist or task-builder (INV-A:39), which bring in the reflect yes/no gate. The brief rule does not exclude them.
- N-7: Adding flags to a command's Usage line edits an existing line, which AC-C5 (SPEC:176) flags as non-additive unless the change is a separate new line. The spec does not say which.
- N-8: Per-session `/sc:save` keys (SPEC:119) may not be read by `/sc:load` or `/sc:pm`, which read the single-owner keys (INV-B:63,165). Whether a worker-saved state is ever resumed is not stated.

Issue question: the command asks the session once per loop whether to open an issue for the follow-up candidates. This sandbox run has no user to ask and its brief says to touch nothing else, so the question was not asked and no issue was created. The list above is the record.

Brief clauses overridden: none. The brief narrows nothing past the command's scope and asks for no minimum number of findings.

## Reviser brief

Blocking finding ids: **B-1**. This restates the reviser contract of the command:
- Revise only the text a blocking finding names.
- Add no rule, mechanism or section that no blocking finding calls for.
- Cite the finding id on each added paragraph or table row.
- Prefer deleting or narrowing to adding.
- Report the byte size of the candidate before and after, and the bytes added and deleted per finding id.
- Leave Medium and minor findings alone, and do not award yourself a PASS.

For B-1 the target text is AC-0.4 (SPEC:194) and, only as it applies at P0, step 3 of the live check (SPEC:182).

verdict: FAIL

review: 1 of 3

# Spec-panel critique, round 1: orca-worker-contract-spec.md

## Header
- Command: `/sc:spec-panel @.dev/orca-command-refactor/specs/orca-worker-contract-spec.md --mode critique --focus requirements,architecture` (first review; neither `--re-review` nor `--baseline` given, so no baseline note applies).
- Candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`
- Candidate SHA-256: `d3cdbe573e57303b9ce6c93d1fe98ba18fb7cb1a15773d926bf6a0c31425200d`
- Baseline SHA-256: not applicable (first review).
- Reviewer model actually used: claude-sonnet-5-5 (Sonnet 5.5).
- Prompt followed: FIRST-REVIEW prompt in `~/.claude/rules/prompts/document_review_loop_prompts.md:27-32` (read in full, sandbox home copy). Brief clauses overridden: none.
- `--unattended` was not passed, so the command's Unattended-mode section does not apply. No improved specification is written (the brief assigns only this file).
- Panel (focus requirements: Wiegers lead, Adzic, Cockburn; focus architecture: Fowler lead, Newman, Hohpe, Nygard; Whittaker always active; reviewed in the command's fixed sequence).

## Evidence limits
Only the files in the sandbox can be checked: `.dev/orca-command-refactor/README.md` and `inventory/{commands-a,commands-b,orca-capabilities}.md` (called INV-A, INV-B, CAPS below), plus the command definition `command.md` and the review-loop prompts file. No `src/`, `cmd/`, `sk/` or `~/.claude` command or skill file exists in the sandbox, so every spec citation of the form `cmd/...`, `sk/...`, `src/superclaude/cli/install_core.py`, `CLAUDE.md:N` and `pyproject.toml:38` is **UNVERIFIED** here. Spec section 1.2 E5 (the two grep runs) and the "re-read 11 locations" claim (spec line 11) are likewise UNVERIFIED. Spec-internal line references (spec lines) and INV/CAPS/README line references were checked.

Spot checks that passed: 43 = 21 (INV-A:3) + 22 (INV-B:3); 10 ready / 27 needs-change / 6 coordinator-only (INV-A:73 gives 5/13/3, INV-B:278 gives 5/14/3); the 27 rows of spec section 3.2 are exactly INV-A's 13 plus INV-B's 14; the 27 phase assignments sum 9 (P1) + 11 (P2) + 4 (P3) + 3 (P4); section 6's P2 list (15) equals 11 + the 4 ready commands with gate fixes; README:11-17, :12, :31, :6, :30 match what the spec cites; CAPS lines 44-45, 52, 58-61, 64, 66-67, 72-80, 84-92, 97-103, 107-116, 129-130, 145-151, 155-161, 186-187 say what the spec attributes to them. One mismatch of note: the spec cites the pr-submit top-level rule at `sk/sc-pr-submit-protocol/SKILL.md:37-39` (matches INV-A:10 and INV-B:90), while CAPS:161 cites `:47-49` of the installed `/home/coder/.claude/` copy; the two files are different copies, so this is not an error, only a reminder that the line numbers differ by copy (note N-1).

## Guard Condition Boundary Table
Trigger fired: the spec contains thresholds and guards (readiness limit, heartbeat and wait sizes, depth limit, confidence cut-off, status mapping, output-directory rule). Input classes that cannot occur for a guard are left out with a reason on the row. Constructed by Nygard, completeness checked by Crispin, attacked by Whittaker.

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|-------|----------|-----------------|----------------|--------------|-------------------|--------|
| WC-1 prompt fallback must be "well inside" the readiness limit | spec line 59 | Typical | 30 s fallback | within 60 s limit | passes (`EVIDENCE.md:45` via CAPS:49) | OK |
| WC-1 prompt fallback | spec line 59 | Maximum/Overflow | 46 s or more | beyond the working range | evidence says "fails again above about 45 s" (CAPS:49) but the spec states no numeric ceiling for "well inside" | GAP (M-4) |
| WC-1 readiness limit | spec line 59 | Zero/Empty | `--timeout-ms` 0 or negative | falls back to 60 s default (CAPS:44) | spec does not restate; Orca behaviour is documented in CAPS | OK (reason: not a spec-owned guard) |
| WC-10 "blocks longer than 5 min, split into waits of at most 4 min" | spec line 68 | Typical | 3 min wait | not over 5 min | no split needed | OK |
| WC-10 | spec line 68 | Legitimate Edge Case | 4 min 30 s wait | not over 5 min, so no split; yet over the 240 s limit of AC-4.3 (spec line 210) | text allows it, acceptance check rejects it | GAP (M-3) |
| WC-10 | spec line 68 | Sentinel Value Match | exactly 5 min wait | "longer than 5" is false | wait stays unsplit; heartbeat cadence is also 5 min, so the beat is due at the instant the call returns | GAP (M-3) |
| WC-5 outcome mapping from the report `status` | spec line 63 | Zero/Empty | no report file | no report | `--outcome failed` | OK |
| WC-5 | spec line 63 | Legitimate Edge Case | file exists but `status` missing or outside the four values, or YAML unparseable | not listed | unspecified; WC-5 covers "no report exists" and the four values only | GAP (M-5) |
| WC-5 | spec line 63 | Typical | `partial` or audit verdict FAIL | maps to succeeded | `--outcome succeeded`, first sentence names the status | OK |
| WC-5 | spec line 63 | Typical | `blocked` | maps to failed | `--outcome failed` (does not trip Orca's circuit breaker, CAPS:80) | OK |
| WC-4 `<output-dir>` is "the directory the coordinator passed (`--output` / `--output-dir`)" | spec line 62 | Typical | `--output .dev/troubleshoot/login/` (spec line 228) | directory | contract at `<dir>/return-contract.yaml` | OK |
| WC-4 `<output-dir>` | spec line 62 | Legitimate Edge Case | `--output <file>` (tdd, init-lite: spec lines 87, 90; AC-2.2, spec line 200) | the value is a file, not a directory | the rule yields `<file>/return-contract.yaml`; no alternative stated | GAP, blocking (B-2) |
| WC-4 `<output-dir>` | spec line 62 | Zero/Empty | no output flag in an `--unattended` brief | no directory | unspecified (spec 2.3 says the brief supplies it; no refusal or default is stated) | GAP (M-5) |
| Task confidence cut-off | spec line 121 | One/Minimal | 0.69 | below 0.70 | resolves as blocked | OK |
| Task confidence cut-off | spec line 121 | Legitimate Edge Case | 0.70 to 0.89 band | not "below 0.70" | unspecified; the band's own behaviour is not in INV-B:199 or the spec | GAP (M-6) |
| Nesting depth limit (R1, D5) | spec lines 33, 249-253 | Maximum/Overflow | worker calls `worker-start` at depth 1 | refused with `nested_worker_depth_exceeded` | stated, with enforcing call sites UNVERIFIED (CAPS:103) | OK (flagged UNVERIFIED in the spec) |
| WC-12 `consumer_fenced` | spec line 70 | Sentinel Value Match | `check` returns `consumer_fenced` | true | stop, send no `worker_done` | OK |
| WC-12 | spec line 70 | Zero/Empty | `check` returns empty | not fenced | continue (CAPS:67: an empty check never means replaced) | OK (not restated, but the worker rule is "stops only on `consumer_fenced`") |
| AC-1.1 "every command in 3.1-3.2 has an `## Unattended mode` section naming `return-contract.yaml`" | spec line 195 | Legitimate Edge Case | `/sc:load` (report "none", no contract) | cannot be satisfied by a command with no contract | contradicts spec lines 112, 265 | GAP, blocking (B-1) |

## Quantity Flow Diagram (Fowler, Whittaker; Pipeline Dimensional Analysis)
Trigger: a staged plan where later stages take a different number of commands than the earlier stage (spec sections 3 and 6).

```text
[Source: 43 commands]
  --> [Inventory verdict split: 10 ready | 27 needs-change | 6 coordinator-only]   (10+27+6 = 43, conserved)
        |
        v
  [P0: 0 command edits; 3 smoke runs]
  [P1 stated scope, spec line 159: "--unattended accepted by every command in 3.1 and 3.2" = 37 commands]
  [P1 listed commands, spec line 159: 9 gate-free from 3.2 + 4 fixes to ready commands = 13 commands]   <-- MISMATCH 37 vs 13
  [P2 listed: 15] [P3 listed: 4] [P4 listed: 3]   (9 + 15 + 4 + 3 + 4 P1 fixes ready = 35; brainstorm and init-lite carry no phase)
        |
        v
  [AC-1.1 asserts a section in all 37 at the end of P1]   <-- consumer assumes 37 after a stage that supplies 13
```

Consumer annotations: AC-1.1 (spec line 195) expects 37; the P1 command list supplies 13; P2 to P4 supply the other 24 later. Reported as B-1. Every other count (43, 27, 6, 10, 15) is conserved.

## === REQUIREMENTS ANALYSIS ===

### B-1 (CRITICAL by consequence: blocking) AC-1.1, P1 scope and AC-1.2 contradict the per-command rows
- Experts: Wiegers (traceability), Whittaker (Divergence and Sequence attack), Fowler (count annotation above).
- Grading sentence: An implementer who follows the stated text as written adds, during Phase 1, a `## Unattended mode` section naming `return-contract.yaml` and the `--unattended` flag to every command in sections 3.1 and 3.2 (spec lines 159 and 195), and X is wrong because three stated texts forbid or defer it: `/sc:load` has "Report: none" and its Decisions row says "a report file would be an unrequested addition" (spec lines 112, 265), so AC-1.2's live check (7.2 step 4 requires `test -s <contract>` and a four-value `status`, spec line 183) cannot pass for the P1 command `/sc:load`; `/sc:pr-submit` is assigned to P4, and recommendation D3 (a) says "no pr-submit changes in Phase 4" (spec lines 114, 240); and `implement` and `post-release` are P4 items that "wait for answers to D2-D4" (spec lines 154, 162).
- Whittaker attack: I can break this specification by **Divergence Attack**. The invariant at **spec line 195 (AC-1.1) and spec line 159 (P1 scope)** fails when **the command set differs between the rows and the check**. Concrete attack: before P1, 0 of 37 commands have the section; P1 as listed edits 13 (analyze, build, business-panel, design, document, explain, index, test, load, adversarial, cleanup-audit, index-repo, workflow); AC-1.1 runs `pytest tests/skills/test_worker_contract.py` asserting all 37 plus "no section-4 command has one"; the test fails for the 24 later-phase commands, or, if the implementer makes it pass by editing them in P1, the P2 gate rows, the P4 deferral and D3 (a) are violated.
- Recommendation: restrict the AC-1.1 assertion and the P1 scope sentence to the commands the P1 row lists (and name which of them carry a contract), and drop `/sc:load` from the contract-bearing set; assert later-phase commands in their own phase's check. Delete rather than add text where possible.
- Priority: High. Quality impact: the P1 gate becomes passable and consistent with sections 3 and 9.

### B-2 (CRITICAL by consequence: blocking) WC-4's `<output-dir>` rule breaks for file-valued `--output`
- Experts: Wiegers (testable acceptance), Adzic (concrete example), Whittaker (Sentinel Collision: the same flag name carries two types).
- Grading sentence: An implementer who follows the stated text as written writes the contract at `<value of --output>/return-contract.yaml` (WC-4, spec line 62: "`<output-dir>` is the directory the coordinator passed (`--output` / `--output-dir`)"), and X is wrong because the spec's own rows pass a file: tdd and init-lite take `--output <file>` (spec lines 87, 90), AC-2.2 runs `/sc:tdd "auth" --unattended --output <file>` (spec line 200), and the `<file>/return-contract.yaml` path cannot be created under a regular file, so WC-4's "written on every outcome" and 7.2 steps 3-4 (the report path "is the WC-4 contract path", spec lines 182-183) cannot pass for those commands. Section 2.3 also says the brief states "the output directory" (spec line 73) without saying where it goes for these commands.
- Whittaker attack: I can break this specification by **Sentinel Collision Attack**. The invariant at **WC-4 (spec line 62)** fails when **`--output` names a file**. Concrete attack: coordinator brief `/sc:tdd "auth component" --unattended --output .dev/tdd/auth.md`; WC-4 resolves `<output-dir>` to `.dev/tdd/auth.md`; the command tries to create `.dev/tdd/auth.md/return-contract.yaml`; before: `auth.md` absent; after: the write fails with a not-a-directory error or turns the target into a directory; no contract exists; WC-5 maps "no report exists" to `--outcome failed` for a run that produced the deliverable.
- Outside-inventory corroboration (command definition in the sandbox, not an inventory): `command.md:22-23` shows `/sc:spec-panel` already has a file-valued `--output <file>`, and `command.md:460-461` resolves the same problem with a separate `--report-dir <dir>` flag and a contract at `<report-dir>/return-contract.yaml`. That also makes the spec's row "spec-panel: add `--output`" (spec line 120) stale against the command definition in this sandbox; its source line (`cmd/spec-panel.md:22`) is UNVERIFIED here.
- Recommendation: state one rule for where the contract goes when the command's output flag is a file (for example, the contract path is a separate coordinator-supplied value, or the file's parent directory), and apply it in WC-4, 2.3 and the tdd, init-lite and spec-panel rows.
- Priority: High. Quality impact: removes the one point where WC-4 and the live check cannot both hold.

### B-3 (MAJOR by label, blocking by consequence) AC-0.4 step 3 requires the contract that Phase 0 says does not exist yet
- Experts: Wiegers, Crispin (completeness of the check).
- Grading sentence: An implementer who follows the stated text as written runs the three P0 smoke runs and requires "steps 1-3 and 5-7 pass" (spec line 194), and X is wrong because step 3 passes only if "its `--outcome` matches the contract's `status` under WC-5; its report path is the WC-4 contract path" (spec line 182), while AC-0.4 itself says the contract "arrives in P1"; the check cannot pass, and its stated failure consequence is "a failure here reopens section 1".
- Whittaker attack: I can break this specification by **Sequence Attack**. The invariant at **AC-0.4 (spec line 194)** fails when **P0 runs before P1**. Concrete attack: `/sc:troubleshoot` ends with `REPORT.md` and no contract; step 3 compares `worker_done --report-path` to a contract path that does not exist; the criterion fails; the phase report records a failure that reopens the core decision for a reason unrelated to it.
- Recommendation: change step 3 in AC-0.4 to use the command's existing report file for the path and outcome comparison, as step 4 already does; no other change.
- Priority: High. Quality impact: stops the phase that tests the central decision from failing for a bookkeeping reason.

## === ARCHITECTURE ANALYSIS ===
No further blocking finding. Fowler, Newman, Hohpe and Nygard checked: the coordinator-over-commands layering against CAPS:97-103 (depth 1) and CAPS:155-161 (subagents, top-level rule); the separation of command changes (section 3) from worker-session duties (WC-3, WC-5, WC-7, WC-12); the single shared contract file and installed-path rule (spec lines 52, 264); the standalone-compatibility rules (section 5); and the failure paths (blocked, stalled, fenced). Those hold as stated. Items that need a guess or state a missing requirement are under follow-up candidates.

## Follow-up candidates (Medium and minor; none triggers a revision)
Medium (warnings):
- M-1 (Wiegers/Nygard) P1 text says the `--unattended` flag is accepted by every command "(a no-op where a command has no gate)" (spec line 159). For gated commands such as cleanup, tdd or cli-eval the P1 flag exists before the P2 gate conversion, so a coordinator that dispatches such a worker after P1 gets a command that still prompts, against WC-2. Needs a guess that the coordinator dispatches before P2; the spec does not say gated commands stay off the dispatch list until their phase.
- M-2 (Hohpe/Whittaker) WC-3 lets a blocked worker `ask`, then "re-invoke or resume the command with the answer as a flag" (spec line 61), but WC-4 writes `status: blocked` to the same `<output-dir>/return-contract.yaml` first and WC-6 gives most commands a "fresh dir" re-run. Which directory the re-invocation writes to, and whether it overwrites the blocked contract, is not stated. Two readings are allowed.
- M-3 (Crispin/Whittaker) WC-10's threshold ("longer than 5 minutes", split to at most 4) is looser than AC-4.3's "no single tool call exceeds 240 s" (spec lines 68, 210); a 4 min 30 s wait follows WC-10 and fails AC-4.3. Applies only if D3 (b) is chosen.
- M-4 (Nygard) WC-1 gives no numeric ceiling for "well inside" the 60 s limit and no phase, test or owner names the launch path (the `ccsession-tag` launcher, spec line 25 E5), so WC-1 has no acceptance check beyond 7.2 step 1.
- M-5 (Wiegers/Whittaker) Missing or malformed `status` in an existing report, and an `--unattended` brief with no output flag, have no stated outcome (guard table rows WC-5 and WC-4 zero/empty).
- M-6 (Nygard) `task` confidence between 0.70 and 0.89 is unspecified, and the spec's choice to block below 0.70 (INV-B:205 suggested defaulting to the higher tier) is not recorded in the Decisions table.
- M-7 (Adzic) `--post-pr` is named as the explicit opt-in for auggie-review posting (spec line 100), but INV-A mentions only `--no-post-pr` (INV-A:38, :78); no inventory line shows a `--post-pr` flag exists, and the spec does not say it adds one. WC-9 also relies on "the command's own explicit flag" for post-release, task and pr-submit without naming it for each.
- M-8 (Newman) SA-3 allows the contract file "when the caller passes the new output flag" without `--unattended`, while WC-4 writes it "in unattended mode" only (spec lines 62, 148); AC-1.3 tests only the no-flag case.
- M-9 (Crispin) AC-C5 forbids any removed line in an edited command file (spec line 176), while SA-4 allows "new flags" (spec line 149); adding a flag to an existing Usage line is a changed line. The command definition in the sandbox shows the alternative (a second Usage line, `command.md:22-24`).
- M-10 (Nygard) AC-C1's grep covers `src/superclaude/core` with no exclusion for the new `WORKER-CONTRACT.md` or the new `HOW-WE-WORK.md` Orca section (spec lines 158, 172), while SA-2 allows an Orca example in the contract file; any text of the form `orca orchestration ...` there fails the check.
- M-11 (Nygard) AC-2.4 asserts the PR review and comment counts on a fork PR are unchanged (spec line 202); other reviewers can change them during the run.
- M-12 (Fowler) `pr-submit` carries a "Will Not: run headless" statement (INV-B:90, citing `cmd/pr-submit.md:85`); D3 (b) and the 3.2 row do not address it.

Minor notes:
- N-1 Line numbers for one rule differ between the checkout copy (`:37-39`) and the installed copy (`:47-49`, CAPS:161); say which copy a citation names.
- N-2 E4 states that subagents are "not counted by Orca's nesting limit" as fact; section 1.4 (3) and CAPS:155 mark an Orca limit on them UNVERIFIED.
- N-3 Section 3 header says "10 ready today", yet the 3.1 rows still need P1 or P2 fixes; the wording "ready if the brief uses the stated flags" is clearer.
- N-4 Plugin mirror: the spec adds a core file and edits commands but names the `plugins/superclaude/` mirror only for `HOW-WE-WORK.md` (spec line 158); whether the mirror needs the new file is UNVERIFIED.

User question on follow-up candidates: not asked and no issue created; this sandbox has no user channel, and the command rule allows creating an issue only after the user answers.

## What I covered
Read in full: the spec (270 lines), `README.md`, `command.md`, the review-loop prompts file. Read the inventory evidence that the spec cites for sections 1, 2, 4, 5, 6 and 8 (CAPS sections 0 to 10, INV-A lines 1-34, 35-55, 56-120, INV-B lines 1-30, 87-95, 276-323), and checked the per-command and per-phase counts. Not covered: any claim that rests on files absent from the sandbox (marked UNVERIFIED above); the full per-command rows INV-B:31-52 beyond the lines grepped; whole-document assurance of every `cmd/` and `sk/` line citation. State Variable Registry is not produced (`--focus correctness` not active).

## Reviser brief
Blocking finding ids: B-1, B-2, B-3.
Rules for the reviser (restated from the command's Review Loop, bullet 6; the reviser reads this report, not the command): revise only text a blocking finding names; add no rule, mechanism or section that no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id. Leave Medium and minor findings alone. Return the candidate once and do not award yourself a PASS.

verdict: FAIL

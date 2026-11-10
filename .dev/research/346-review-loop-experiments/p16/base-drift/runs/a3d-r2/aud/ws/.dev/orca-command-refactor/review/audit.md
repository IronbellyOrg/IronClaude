review: 1 of 3
command: /sc:spec-panel @.dev/orca-command-refactor/specs/orca-worker-contract-spec.md --mode critique --focus requirements,architecture
candidate: .dev/orca-command-refactor/specs/orca-worker-contract-spec.md
candidate_sha256: 0c0dfe399e2121731d70aeb7cfd72ce90647f551183721fbf9e5d10ed5273f3a
baseline: n/a (first review of the whole document; no --re-review and no --baseline given)
reviewer_model: Sonnet 5.5 (claude-sonnet-5-5)
review_kind: labelled whole-document audit of the final spec, FIRST-REVIEW prompt of ~/.claude/rules/prompts/document_review_loop_prompts.md (read in full before reviewing)
brief_clauses_overridden: none

Citation shorthand: `SPEC:N` = line N of `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`; `INV-A:N`, `INV-B:N`, `CAPS:N` = lines of `inventory/commands-a.md`, `commands-b.md`, `orca-capabilities.md`; `README:N` = `.dev/orca-command-refactor/README.md`; `CMD:N` = line N of the `/sc:spec-panel` command definition (`command.md` in the audit sandbox).

## What was covered
- Read the whole candidate (SPEC:1-285), the README, and all three inventories in full. Read the review-loop prompts file in full and followed the FIRST-REVIEW prompt, including its grading check.
- Checked the candidate's internal arithmetic. 21 + 22 = 43 commands (SPEC:76, INV-A:3, INV-B:3). The 5 + 5 ready, 13 + 14 needs-change and 3 + 3 coordinator-only verdicts add up to 10 / 27 / 6, matching SPEC:76-137 (INV-A:73, INV-B:278). The command-to-phase assignment accounts for all 37 worker-capable commands (see Quantity Flow Diagram).
- Spot-checked about 60 `INV-A`, `INV-B`, `CAPS` and `README` line citations in the candidate against the files. All matched. Examples: `INV-A:90`, `INV-A:106`, `INV-B:272`, `INV-B:320`, `INV-B:323`, `CAPS:49`, `CAPS:97-103`, `CAPS:130`, `README:12`, `README:31`.
- UNVERIFIED: every citation of `cmd/`, `sk/`, `src/superclaude/cli/`, `CLAUDE.md`, `HOW-WE-WORK.md`, `pyproject.toml`, `EVIDENCE.md`, `.dev/codegraph-migration/` and the Orca guide text. None of these files is inside the sandbox. Where this report relies on one, it goes through the inventory line that quotes it. The candidate's own claim of an independent citation check (SPEC:285) is likewise UNVERIFIED here.
- Ran two shell checks with no file access. One pipe test of the AC-C5 regex (finding F-01). One SHA-256 of the candidate.
- Panel (critique mode, review order per CMD:101-113): Wiegers, Adzic, Cockburn (requirements lead); Fowler, Nygard (architecture); Whittaker (active in every panel review); Newman, Hohpe (architecture). Crispin validated the guard table for completeness. `--focus correctness` is not active, so no State Variable Registry was produced (CMD:186-188).

## Grading check applied
Each finding below was written as "An implementer who follows the stated text as written builds X, and X is wrong because Y". Only F-01 holds that sentence without a further assumption. Every other MAJOR-labelled finding needs a guess about which of two readings the text allows, or is a requirement the document never states, so it is graded Medium and listed under follow-up candidates (CMD:259, FIRST-REVIEW prompt).

=== REQUIREMENTS ANALYSIS ===

### F-01 (blocking) AC-C5 cannot detect deleted or rewritten bullet lines, so the "additive" guarantee is not enforced
- Severity label: MAJOR. Grade: blocking. Expert: Wiegers (testability), Whittaker (Divergence attack). Priority: High.
- Stated text: SA-1 and SA-4 make "every prompt, approval gate, default flag value... stays as it is today" a hard requirement on every phase (SPEC:142, 146, 149). AC-C5 is the check that proves it: `git diff -U0 master...HEAD -- src/superclaude/commands/<name>.md | grep -E '^-[^-]'`, pass condition "prints nothing: edits are additive" (SPEC:176).
- Grading sentence: an implementer who runs AC-C5 as written treats "prints nothing" as proof that no existing line was deleted or rewritten. That proof is wrong, because a removed markdown bullet `- text` appears in `-U0` output as `-- text` and the pattern `^-[^-]` skips every line whose second character is `-`.
- Evidence: pipe test run in the sandbox with input `-- bullet removed`, `-| table row removed`, `--- a/file`, `-plain removed`, `----`. The pattern printed only `-| table row removed` and `-plain removed`. The removed bullet and the removed `---` frontmatter delimiter (shown as `----`) passed unseen.
- Consequence: gate text in command files is mostly bullets (for example the gate lines cited at SPEC:100-125). P2 is a gate-conversion phase (SPEC:160), and the natural implementation edits those existing bullets. Such an edit passes AC-C5 while breaking SA-1. The same pattern gives a false FAIL on a file that lacks a trailing newline, because the last line is reported as removed and re-added. AC-0.3 (SPEC:193) is not affected for table rows, which start with `|`.
- Recommendation: replace the pattern with a test that counts deleted lines directly. For example, `git diff --numstat master...HEAD -- <file>` and require the deleted column to be 0, with the named defect fixes of SA-4 exempted by listing them. Keep the pass condition text. Quality impact: restores the only mechanical guard of the standalone-behaviour promise.

### M-01 (Medium) Which commands get `--unattended`, the `## Unattended mode` section and a contract is stated four ways
- Severity label: MAJOR. Grade: Medium (needs a guess which statement wins). Expert: Wiegers, Cockburn. Priority: Medium.
- Statements that do not agree:
  - Section 2.3 says every brief carries "the exact command line including `--unattended`" (SPEC:73). Section 3 says "Every changed command also gains the `## Unattended mode` section" (SPEC:76).
  - Section 3.1 says the 10 ready commands run "now" with no change and lists no `--unattended` in "Brief must pass" (SPEC:79-92). `brainstorm` and `init-lite` have "Small fix: None" (SPEC:84, 87).
  - Section 6 P1 gives the flag only to the commands named in its row, `load` "flag and usage-line fix only, no contract" (SPEC:159). `brainstorm`, `init-lite` and `cleanup-audit`/`index-repo` as contract writers appear in no phase (SPEC:158-162).
  - WC-4 names `init-lite` as a file-valued contract case (SPEC:62), but no phase adds that contract.
  - AC-0.4 runs the three smoke commands without the flag (SPEC:194) while 2.3 requires it.
- Concrete trace: a coordinator briefing `/sc:brainstorm` per 2.3 passes `--unattended`, a flag no phase ever gives it. Whether brainstorm rejects it or absorbs it into the topic is not stated anywhere.
- Recommendation: add one sentence stating the rule, for example "`--unattended` is required in the brief only for commands whose section 3 row says they accept it; ready commands without a row-level change are briefed with the 3.1 flags only", and align the "Every changed command" sentence (SPEC:76) with the `load` exception (SPEC:112, 159, 195).

### M-02 (Medium) AC-1.1's "no later-phase command has the section yet" assertion collides with AC-C3 at P2
- Severity label: MAJOR. Grade: Medium (the word "yet" shows intent, but a pytest assertion has no phase). Expert: Crispin, Adzic. Priority: Medium.
- AC-1.1 asserts that "no section-4 command and no command of a later phase has one yet" in `tests/skills/test_worker_contract.py` (SPEC:195). AC-C3 requires that no test that passed in the pre-phase baseline fails afterwards (SPEC:174). P2 adds the section to P2 commands (SPEC:160, 199), which flips the P1 negative assertion. AC-2.1 says the file "gains" assertions but never says the P1 negative one is removed or parameterised by phase.
- Recommendation: state that the negative assertion is scoped to the current phase's command list and is edited at each phase, or limit it to the section-4 commands only.

### M-03 (Medium) The contract location rule is not one rule, and "fresh output directory" breaks "path known before dispatch"
- Severity label: MAJOR. Grade: Medium. Expert: Wiegers, Nygard. Priority: Medium.
- WC-4 fixes the contract at `<output-dir>/return-contract.yaml` or `<file>.return-contract.yaml`, "known before dispatch" (SPEC:62, 73). WC-6 says a command without resume "writes each run into a fresh output directory" (SPEC:64), and about 20 rows say "fresh dir" (for example SPEC:99, 101, 106, 107). The text never says who creates the fresh directory.
- Trace: a retry worker (`--retry-of`) is briefed with the same `--output <dir>` as the first attempt. If the command creates a timestamped subdirectory, the contract is no longer at the path the brief gave. If the coordinator must pass a new directory per retry, 2.3 does not say so.
- Exceptions already in the table are not reflected in WC-4. `adversarial` writes `<output>/adversarial/return-contract.yaml` (SPEC:83). `cleanup-audit` has a fixed output directory, so there is no coordinator-passed directory (SPEC:85). `workflow` writes inside `.dev/tasks/to-do/<id>/` (SPEC:92).
- Recommendation: add to WC-6 "the coordinator passes a new `<output-dir>` per attempt; the command never creates one", and list the three path exceptions in WC-4 or in 2.3.

### M-04 (Medium) Contract trigger conditions disagree, and `--unattended` with no output location is undefined
- Severity label: MAJOR. Grade: Medium (missing requirement). Expert: Adzic, Whittaker (Zero/Empty and Divergence attacks). Priority: Medium.
- WC-4 writes the contract "in unattended mode" (SPEC:62). SA-3 writes it "only in unattended mode or when the caller passes the new output flag" (SPEC:148). AC-1.3 tests only "no `--unattended` and no new output flag" (SPEC:197). A run with the new output flag and no `--unattended` is covered by SA-3 and contradicted by WC-4, and no check exercises it.
- Zero/Empty: `/sc:analyze src --unattended` with no output flag. Section 2.3 says the brief supplies the directory (SPEC:73), but no requirement says what the command does when it is missing. The `/sc:spec-panel` command definition in use here refuses before any work in that case (CMD:460). The spec has no equivalent.
- Recommendation: add one WC-4 sentence: "`--unattended` without an output location is refused before any work, with the refusal printed in chat", and settle the SA-3/WC-4 trigger in one wording.

### M-05 (Medium) "Keep their fields" conflicts with the fixed four-value status set, and unreadable contracts are not handled
- Severity label: MAJOR. Grade: Medium (the existing vocabularies were never read). Expert: Wiegers, Hohpe. Priority: Medium.
- WC-4 says commands that already write a contract "keep their fields and add the missing ones" (SPEC:62). The Decisions row fixes the status vocabulary to `succeeded / partial / failed / blocked` (SPEC:262). Check 7.2 step 4 asserts that vocabulary for every contract (SPEC:183). `workflow`, `brainstorm`, `reflect` and `adversarial` already have a `status` field (INV-B:272, INV-A:39, INV-B:112, INV-A:35). Neither inventory records their allowed values, so the check may fail on a correct, unchanged contract.
- WC-5 handles "no report exists" but not a zero-byte or unparseable file (SPEC:63).
- Recommendation: record each existing contract's status values and either map them in WC-4 or state that the new fields live beside the old ones. Add "unreadable report counts as no report" to WC-5. Optionally add a `contract_version` field, since `workflow` already versions its contract (INV-B:272) and WC-4 does not (Newman).

### M-06 (Medium) WC-10 cannot be met for Agent-tool fan-out, and its basis is unverified
- Severity label: MAJOR. Grade: Medium. Expert: Nygard, Whittaker (Accumulation attack). Priority: Medium.
- WC-10 requires any single blocking tool call longer than 5 minutes to be split into waits of at most 4 minutes (SPEC:68), but names only poll waits and `cli-eval` (SPEC:104, 114). Foreground Agent-tool calls in ready commands such as `cleanup-audit` (7-8 concurrent agents, INV-A:42), `tdd` (INV-B:221) and `adversarial` (INV-A:35) are single long calls that cannot be split.
- The 5-minute cadence comes from this run's preamble only, and Orca's use of heartbeat age is UNVERIFIED (CAPS:130). Absence of a heartbeat never authorises stop or retry (CAPS:125). The requirement is therefore stricter than its evidence, and it has no check outside AC-4.3 (SPEC:210).
- Recommendation: scope WC-10 to waits the command itself chooses (polls, sleeps, eval waits), and say that long Agent-tool calls are exempt and are watched through `worker-show` (SPEC:181).

### M-07 (Medium) WC-1 has an owner outside the commands but no deliverable, phase or numeric bound
- Severity label: MAJOR. Grade: Medium (missing requirement). Expert: Cockburn, Nygard. Priority: Medium.
- WC-1 is owned by "Launch setup, not commands" (SPEC:59) and requires a fallback "well inside" the 60 s limit. No phase in section 6 (SPEC:158-162) assigns it. The only check is step 1 of 7.2, which would catch a failure only after it happens (SPEC:180). The evidence has a 30 s fallback that passed and a 45 s start limit that failed (CAPS:49), so a bound below the limit can be stated.
- Recommendation: add a P0 line naming the launch wrapper(s) to check against a stated bound (for example 30 s) and the check that proves it.

### M-08 (Medium) P0 deliverables have no stated content, and the global AC-C1 grep may reject them
- Severity label: MAJOR. Grade: Medium (missing requirement; the conflict depends on wording the spec does not fix). Expert: Fowler, Cockburn. Priority: Medium.
- P0 adds an Orca section to `HOW-WE-WORK.md` and a "coordinator brief template" to `WORKER-CONTRACT.md` (SPEC:158). The spec states no content for either. AC-C1 fails on any line under `src/superclaude/core` that matches lowercase `orca orchestration|worktree|terminal|agent` (SPEC:172). SA-2 allows an Orca mention only "inside the contract file" (SPEC:147). Today `HOW-WE-WORK.md` has zero Orca mentions (SPEC:25). A coordinator-facing section that names `orca-ide orchestration worker-start` would fail AC-C1 in P0.
- Recommendation: either state that these two files may name Orca commands and exempt them in AC-C1, or state that they describe the workflow without command names.

### M-09 (Medium) D1(a) claims the flag "cannot misfire on a person", with no token rule
- Severity label: MAJOR. Grade: Medium. Expert: Whittaker (Sentinel Collision attack). Priority: Medium.
- D1(a) is recommended because the flag "cannot misfire on a person" (SPEC:228). No requirement says how the flag is recognised. A quoted topic such as `/sc:tdd "explain the --unattended flag"` contains the string. The `/sc:spec-panel` command definition resolves this by honouring only a standalone argument token outside any quoted argument (CMD:459). The spec carries no such rule for the other commands.
- Recommendation: add the token rule to the shared contract file (SPEC:52) so every command inherits it.

### M-10 (Medium) Unattended outcome of tasklist HALT items and of auto-accepted remediation is unspecified
- Severity label: MAJOR. Grade: Medium. Expert: Adzic, Nygard. Priority: Medium.
- The tasklist row says Stage 10.5 passes `--unattended` to each reflect "so the headless rule applies" (SPEC:122). The reflect row makes `--remediate` follow the headless auto-accept rule (SPEC:88, 151). Auto-accept turns a person's yes/no into an automatic yes for auto-fixable items. The inventory records that `needs_human_decision` items HALT in Stage 10.5 and that who answers inside subagents is UNVERIFIED (INV-B:209, INV-B:322). Neither WC-2 route (a)/(b)/(c) is assigned to those HALTs, and the contract has no field recording which items were auto-accepted.
- Recommendation: state that `needs_human_decision` items resolve as blocked, and that the contract lists the auto-accepted items.

### M-11 (Medium) "Phases 1-3 need no user decision" conflicts with D4's scope
- Severity label: MAJOR. Grade: Medium. Expert: Cockburn. Priority: Low.
- Section 6 says Phases 1-3 need no decision and Phase 4 waits for D2-D4 (SPEC:154). D4 names `auggie-review --post-pr` and `task commit/push` as affected (SPEC:244), both P2 rows (SPEC:100, 121, 160). If the user picks D4 (b), the P2 rows that restore posting through an explicit flag would be wrong. SPEC:225 lets P0-P3 proceed on the recommendations, so the text is consistent only on that reading.
- Recommendation: add "P2 assumes D4 (a)" to the P2 row.

=== ARCHITECTURE ANALYSIS ===

### Strengths found (no finding)
- The core decision (SPEC:13-39) is argued against a concrete alternative with checkable reasons R1-R5. The nesting depth, executable-name, preamble-bound `worker_done` and standalone-use reasons are each backed by `CAPS` lines that exist and say what the spec quotes (CAPS:97-103, 145-150).
- Section 1.4 states plainly that no command was run end to end as an Orca worker (SPEC:43, INV-B:323) and makes P0 test the decision first.
- Coordinator-only commands (SPEC:127-139) follow from the inventories (INV-A:87-92, INV-B:282-287).

### A-01 Coupling of unrelated concerns in one flag (Fowler, no grade change)
`--unattended` bundles three separable behaviours: no person gates (WC-2), outward actions off (WC-9) and report-file writing (WC-4). The spec accepts this on purpose (SPEC:260). It does force per-command exceptions (research pins a strategy, SPEC:116; auggie-review implies two other flags, SPEC:100). It is acceptable if M-01 and M-04 are settled; noted so a later phase does not add a fourth concern.

### A-02 Failure modes on the coordinator side (Nygard, follow-up)
The contract says what the worker does on every outcome but not what the coordinator does on a worker that ends without `worker_done`. Section 1.4 names the silent stall as the real failure mode (SPEC:44) and defers to `worker-show` (SPEC:181) and Orca's own guide (SPEC:215). A one-line pointer to the recovery rules (CAPS:120-129) would close the loop. Not graded as a finding because the non-goals put the coordinator loop in Orca's guide.

### A-03 Integration pattern (Hohpe, Newman, follow-up)
The report is a pointer file whose contents Orca never checks (CAPS:79). The spec handles this correctly by making the coordinator open it (SPEC:62, 73). The only schema is a list of fields in prose (SPEC:62) and an inline Python assertion (SPEC:183). A short example contract in `WORKER-CONTRACT.md` would make the schema testable. Related to M-05.

=== ADVERSARIAL ANALYSIS (Whittaker) ===
Attack findings use the FR-3 template. Severity is graded by consequence and mapped to the findings above.

1. I can break this specification by **Divergence Attack**. The invariant at **AC-C5 (SPEC:176)** fails when **a P2 edit rewrites an existing gate bullet**. Concrete attack: before, `cmd/<name>.md` holds `- Wait for user response if --interactive`; after, the bullet is reworded. `git diff -U0` shows `-- Wait for user ...`. The pipeline `grep -E '^-[^-]'` prints nothing; AC-C5 passes; SA-1 is broken. MAJOR, blocking: F-01.
2. I can break this specification by **Sequence Attack**. The invariant at **AC-1.1 and AC-C3 (SPEC:195, 174)** fails when **P2 adds the section to a P2 command**. Concrete attack: P1 ends with the assertion "tdd has no section" passing; P2 adds tdd's section; the same test fails; AC-C3 forbids a previously passing test failing. MAJOR, Medium: M-02.
3. I can break this specification by **Sentinel Collision Attack**. The invariant at **D1(a) (SPEC:228)** fails when **a topic string contains `--unattended`**. Concrete attack: before, mode off; the brief `/sc:tdd "explain the --unattended flag"` is parsed by a command with no token rule; after, mode on, prompts suppressed for a person. MAJOR, Medium: M-09.
4. I can break this specification by **Zero/Empty Attack**. The invariant at **WC-4 (SPEC:62)** fails when **`--unattended` is given with no output location**. Concrete attack: `/sc:build --unattended`; WC-4 needs `<output-dir>` and 2.3 says the brief supplies it; no requirement says what happens when it does not. MAJOR, Medium: M-04.
5. I can break this specification by **Accumulation Attack**. The invariant at **WC-6 and WC-4 (SPEC:64, 62)** fails when **a command is retried twice into the same output directory**. Concrete attack: attempt 1 writes `<dir>/return-contract.yaml` with `status: blocked`; attempt 2 either overwrites it or writes a subdirectory, and the worker's `--report-path` points at whichever the brief named. MAJOR, Medium: M-03.
6. I can break this specification by **Sentinel Collision Attack**. The invariant at **check 7.2 step 4 (SPEC:183)** fails when **an existing contract uses a status value outside the four**. Concrete attack: `workflow` writes its own `status` value; the assertion `d['status'] in {...}` fails on a correct run. MAJOR, Medium: M-05.

## Guard Condition Boundary Table
Guards found: the WC-5 outcome rule, the contract trigger, the WC-10 wait limit, the AC-C5 check, the D1 flag test and the WC-1 launch fallback. Prerequisite for synthesis (FR-10): all cells populated; every omitted input class has its one-line reason below the table.

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|-------|----------|-----------------|----------------|--------------|-------------------|--------|
| `outcome_failed` (status failed/blocked or no report) | SPEC:63 WC-5 | Zero/Empty | report file absent | true | `--outcome failed` | OK |
| `outcome_failed` | SPEC:63 WC-5 | Zero/Empty | report file present, 0 bytes or unparseable | undefined | not specified (WC-5 says only "no report exists") | GAP (M-05) |
| `outcome_failed` | SPEC:63 WC-5 | One/Minimal | `status: partial` | false | `--outcome succeeded`, body states `partial` | OK |
| `outcome_failed` | SPEC:63 WC-5 | Typical | `status: succeeded` | false | `--outcome succeeded` | OK |
| `outcome_failed` | SPEC:63, 183 | Sentinel Value Match | status value outside the four (existing contract vocabulary) | undefined | not specified; 7.2 step 4 would fail it | GAP (M-05) |
| `outcome_failed` | SPEC:63 WC-5 | Legitimate Edge Case | audit verdict FAIL with `status: succeeded` | false | `--outcome succeeded` (explicit) | OK |
| `contract_written` | SPEC:62 WC-4, 148 SA-3 | Zero/Empty | `--unattended`, no output location | undefined | not specified | GAP (M-04) |
| `contract_written` | SPEC:62, 148 | Typical | `--unattended --output <dir>` | true | `<dir>/return-contract.yaml` | OK |
| `contract_written` | SPEC:62, 148 | Sentinel Value Match | file-valued `--output docs/T.md` | true | `docs/T.md.return-contract.yaml` | OK |
| `contract_written` | SPEC:62 vs 148 | Legitimate Edge Case | `--output <dir>` without `--unattended` | WC-4 false, SA-3 true | contradictory; not exercised by AC-1.3 | GAP (M-04) |
| `contract_written` | SPEC:62, 64 | Legitimate Edge Case | retry into the same `--output` | undefined | "fresh output directory" owner not stated | GAP (M-03) |
| `wait_must_split` (step > 5 min) | SPEC:68 WC-10 | Typical | 3 min poll wait | false | no split needed | OK |
| `wait_must_split` | SPEC:68 WC-10 | Maximum/Overflow | one 20 min foreground Agent-tool call | true | "split into waits of at most 4 min" cannot be applied; unspecified | GAP (M-06) |
| `wait_must_split` | SPEC:68, 210 | Legitimate Edge Case | step of 4 to 5 min | false | no split; next heartbeat due at 5 min | OK |
| `grep -E '^-[^-]'` (AC-C5) | SPEC:176 | Zero/Empty | empty diff | false (no output) | pass | OK |
| `grep -E '^-[^-]'` | SPEC:176 | Typical | removed plain-text line | true | check fails, as intended | OK |
| `grep -E '^-[^-]'` | SPEC:176 | Sentinel Value Match | removed `---` delimiter, shown as `----` | false | passes unseen | GAP (F-01) |
| `grep -E '^-[^-]'` | SPEC:176 | Legitimate Edge Case | removed bullet `- text`, shown as `-- text` | false | passes unseen | GAP (F-01) |
| `grep -E '^-[^-]'` | SPEC:176 | One/Minimal | file with no trailing newline, one line appended | true | false FAIL | GAP (F-01) |
| `unattended_on` (flag token) | SPEC:51, 228 | Zero/Empty | flag absent | false | standalone behaviour (SA-1) | OK |
| `unattended_on` | SPEC:228 | Typical | standalone token in the brief | true | mode on | OK |
| `unattended_on` | SPEC:228 | Sentinel Value Match | quoted topic containing `--unattended` | undefined | not specified | GAP (M-09) |
| `launch_prompt_fallback` | SPEC:59 WC-1 | Zero/Empty | no fallback, prompt waits | true | `worker-start` fails at `agent_readiness` (CAPS:49) | OK |
| `launch_prompt_fallback` | SPEC:59 WC-1 | Typical | 30 s fallback | true | passes (CAPS:49) | OK |
| `launch_prompt_fallback` | SPEC:59 WC-1 | Legitimate Edge Case | fallback 45 to 60 s | undefined | "well inside" has no number; evidence shows failure near 45 s with a 45 s limit | GAP (M-07) |

Omitted input classes, with reasons:
- `outcome_failed`: Maximum/Overflow omitted, because the rule reads one status value and has no capacity.
- `contract_written`: One/Minimal and Maximum/Overflow omitted, because the rule is a boolean on flag presence with no count or capacity.
- `wait_must_split`: Zero/Empty omitted, because a zero-length wait blocks nothing. One/Minimal and Sentinel Value Match omitted, because no minimal step or reserved duration exists.
- `grep -E '^-[^-]'`: Maximum/Overflow omitted, because the check reads a text stream with no stated capacity.
- `unattended_on`: One/Minimal, Maximum/Overflow and Legitimate Edge Case omitted, because the test is a boolean token match.
- `launch_prompt_fallback`: One/Minimal, Maximum/Overflow and Sentinel Value Match omitted, because only the fallback duration varies.

## Quantity Flow Diagram (Pipeline Dimensional Analysis)
Applied to the spec's own classification pipeline, because it has stages whose output count differs from input count. No mismatch found: counts are conserved at every stage.

```text
[Inventories: 21 (A) + 22 (B) = 43 commands] --> [Stage 1: verdict split]
    --> 10 ready (5 A + 5 B)  --> 3.1 (SPEC:78-92), 10 rows
    --> 27 needs-change (13 A + 14 B) --> 3.2 (SPEC:94-125), 27 rows
    --> 6 coordinator-only (3 A + 3 B) --> section 4 (SPEC:127-137), 6 rows
[Stage 2: phase assignment of the 37 worker-capable commands]
    P1: 9 listed (analyze, build, business-panel, design, document, explain, index, test, load) + 4 fixes (adversarial, cleanup-audit, index-repo, workflow) = 13   [Consumer: AC-1.1, AC-1.2 expect "every P1 command" - MISMATCH risk, see M-01]
    P2: 15 (11 needs-change + reflect, release-split, tdd, troubleshoot)
    P3: 4 (roadmap, save, validate-roadmap, validate-tests)
    P4: 3 (implement, post-release, pr-submit)
    no phase: 2 (brainstorm, init-lite)
    13 + 15 + 4 + 3 + 2 = 37
```
The only count the spec leaves open is which of the 13 P1 entries AC-1.1 and AC-1.2 cover (the 9 listed, or all 13); this is part of M-01.

## Standard-format summary
```yaml
specification_review:
  original_spec: .dev/orca-command-refactor/specs/orca-worker-contract-spec.md
  review_date: 2026-11-10
  expert_panel: [wiegers, adzic, cockburn, fowler, nygard, whittaker, newman, hohpe, crispin]
  focus_areas: [requirements, architecture]
quality_assessment:
  overall_score: 7.5
  clarity: 8
  completeness: 7
  testability: 7
  consistency: 7
critical_issues:
  - {category: testability, severity: MAJOR, grade: blocking, expert: wiegers, id: F-01, issue: "AC-C5 regex ^-[^-] skips removed bullet and --- lines", recommendation: "count deleted lines with git diff --numstat"}
expert_consensus:
  - "The Orca-on-top decision and the coordinator-only split are well supported by the inventories."
  - "The weak points are the acceptance checks and the unstated edges of the shared contract (scope, location, trigger, status vocabulary)."
improvement_roadmap:
  immediate: [F-01]
  short_term: [M-01, M-02, M-03, M-04, M-05]
  long_term: [M-06, M-07, M-08, M-09, M-10, M-11]
adversarial_analysis: "see ADVERSARIAL ANALYSIS above, six attacks, one blocking"
```

## Follow-up candidates (Medium and minor; none triggers a revision, none appears in the Reviser brief)
Medium: M-01, M-02, M-03, M-04, M-05, M-06, M-07, M-08, M-09, M-10, M-11 (each described above).

Minor notes:
- N-01 SA-4's closed list of allowed edits to existing lines (SPEC:149) omits changes that section 3 asks for: the `cli-eval` wait splitting (SPEC:104), the `cli-portify` resume flag (SPEC:105) and the `pr-submit` wait check (SPEC:114). Those edit skills, which AC-C5 does not scan.
- N-02 Check 7.2 step 5 searches the transcript for the string `AskUserQuestion` (SPEC:184). Loaded command text that says "never calls AskUserQuestion" would match. Say "tool call named AskUserQuestion".
- N-03 E2 (SPEC:22) cites `EVIDENCE.md:45` for "same tools as a person". That line, as quoted at CAPS:49, shows only `state: ready, stage: input_accepted` after a 34 s start. Readiness is evidenced; tool parity is not.
- N-04 The tasklist row says the reflect fan-out is "inside Claude Code's nesting limit" (SPEC:122) without counting layers. The inventory marks nested spawning UNVERIFIED (INV-B:210, INV-B:314).
- N-05 The labels B-1, B-2, B-3 (SPEC:62, 120, 159, 194, 195) and "ladder rung 2" (SPEC:261) are used without a definition in the document. They probably point to the earlier review (`review/spec-panel.md`, `review/disposition.md`), which are not in the sandbox. UNVERIFIED.
- N-06 For `/sc:spec-panel` the spec fixes `--output <file>` and a contract "beside it" (SPEC:62, 120). The command definition used for this audit already implements the unattended switch with `--report-dir` and a directory-valued contract (CMD:460-461). Which design is current is not stated in either place.
- N-07 `pr-submit` is counted in the 27 needs-change commands (SPEC:114), while D3's recommendation makes it coordinator-or-person only (SPEC:240).

Issue offer: the loop rule asks the session that ran the review to ask the user once whether to open an issue for the follow-up candidates. This run is a worker in a sandbox with no user channel, so the question was not asked and no issue was created. This is not an `--unattended` run; the list is recorded here for the coordinator.

## Reviser brief
Blocking finding ids: F-01.
Rules for the reviser (restated from the command's Review Loop, bullet 6; the reviser reads this report, not the command):
- Revise only text a blocking finding names. Here that is the AC-C5 check line and, if needed, the sentence that SA-4 uses to point at it.
- Add no rule, mechanism or section that no blocking finding calls for. Cite the finding id on every added paragraph or table.
- Prefer deleting or narrowing to adding. Report the byte size of the candidate before and after, and the bytes added and deleted per finding id.
- Leave every Medium finding (M-01 to M-11) and minor note (N-01 to N-07) alone. Do not award yourself a PASS.

verdict: FAIL

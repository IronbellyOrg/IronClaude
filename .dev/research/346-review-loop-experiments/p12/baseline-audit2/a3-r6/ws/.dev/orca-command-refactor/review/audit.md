review: 1 of 3

# Spec-panel audit: Orca worker-contract spec (first review, whole document)

- command: `/sc:spec-panel @.dev/orca-command-refactor/specs/orca-worker-contract-spec.md --mode critique --focus requirements,architecture` (labelled whole-document audit; FIRST-REVIEW prompt of `~/.claude/rules/prompts/document_review_loop_prompts.md`, read in full)
- candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`
- candidate sha256: `83f24502ee791d296bebd644adce8eba84b0a7bccbb076f090415ba276880733`
- baseline: none given, none needed (first review; neither `--re-review` nor `--baseline` was passed)
- reviewer model used: claude-sonnet-5-5
- format: standard content (YAML keys below) plus critique buckets; one review whatever `--iterations` says
- panel (fixed order, filtered by focus): Wiegers, Adzic, Cockburn (requirements); Fowler, Nygard, Newman, Hohpe (architecture); Whittaker (active in every review, after Fowler and Nygard); Crispin (completeness check of the Guard Condition Boundary Table only). Gregory and Hightower were not convened (focus excludes testing and compliance).
- brief clauses overridden: none. The brief narrowed nothing and widened nothing.

Citation conventions. `SPEC:N` = line N of the candidate. `INV-A:N`, `INV-B:N`, `CAPS:N` = line N of `inventory/commands-a.md`, `commands-b.md`, `orca-capabilities.md`, the only evidence checkable in this sandbox. Any citation to a file outside those (CLAUDE.md, install_core.py, HOW-WE-WORK.md, EVIDENCE.md except as quoted in CAPS, `cmd/` and `sk/` lines except as quoted in the inventories) is UNVERIFIED here.

## Coverage (what was and was not covered)

Covered: the whole candidate (286 lines); `README.md` (binding context); all three inventories in full. Checked: the 43 = 21 + 22 command count and the 10 / 27 / 6 split against `INV-A:73`, `INV-B:278` (both sum correctly); the 27 rows of section 3.2 and the 10 rows of 3.1 against the two inventory tables (every row maps to an inventory row and the cited lines match the inventory cells); phase membership counts (P1 12, P2 15, P3 4, P4 3 distinct commands = 34 = 27 + 7); the `CAPS:` cites used in section 1 (all found as described); the internal consistency of WC-1 to WC-12, SA-1 to SA-6, the acceptance checks and D1 to D5.

Not covered, UNVERIFIED: every `CLAUDE.md:N`, `install_core.py:N`, `HOW-WE-WORK.md:N`, `core/CLAUDE.md:65`, `pyproject.toml:38`, `Makefile:68-74` cite; `orchestration/README.md:33,42`; the spec's own `grep` results (E5, SPEC:25). No command was run, so all behaviour claims rest on the inventories, which themselves say no command ran end to end (`INV-B:323`).

## Grading checks (blocking findings only)

- B1. An implementer who follows WC-4 as written (SPEC:62: no output path in the brief and none named in the paragraph means a chat-only refusal and no file) builds `/sc:save --unattended` that refuses and writes nothing, and that is wrong because AC-3.4 (SPEC:207) runs exactly `/sc:save --unattended` and requires two new per-session files.
- B2. An implementer who follows SPEC:62, SPEC:73 and SPEC:182 (the report path is the WC-4 contract path for every dispatched command) while following SPEC:76 and SPEC:159 (six ready commands gain no contract work) builds `/sc:cleanup-audit`, `/sc:init-lite` and `/sc:index-repo` with no `return-contract.yaml`, and that is wrong because the coordinator then passes a `--report-path` no file satisfies and WC-5 (SPEC:63) sends `--outcome failed` for a successful run.

All other findings below need a guess about which of two readings an implementer picks, or are requirements the document never states, so they are Medium or minor and sit under follow-up candidates.

=== REQUIREMENTS ANALYSIS ===

### B1. WC-4 has no contract location for commands that have no output flag, and its refusal clause then makes them refuse (CRITICAL by consequence: blocking, MAJOR label)

- Experts: Wiegers (lead: unstated range for an input), Adzic (the spec's own acceptance commands are the counter-example), Whittaker (Zero/Empty attack).
- Defect. WC-4 defines the contract location only as `<output-dir>`, "the directory the coordinator passed ... (`--output` / `--output-dir`)", plus a fixed list of exceptions (tdd, init-lite, spec-panel, adversarial, cleanup-audit, workflow), and says that with no output path "the command stops with a chat-only refusal ... and writes no file" (SPEC:62). An output flag added by a section 3 row is "a directory unless listed here" (SPEC:62), so the flag must be added by a row. These section 3.2 rows give a contract but name no output flag and the inventories show none exists:
  - `save` (SPEC:119; memory files only, `INV-B:162`),
  - `cli-eval` (SPEC:104; outputs under fixed dirs, no output flag, `INV-A:44`),
  - `research` (SPEC:116; generated `claudedocs/research_*.md`, no flag, `INV-B:132`),
  - `recommend` (SPEC:115; chat envelope, `INV-B:102`),
  - `review-translation` (SPEC:117; fixed `reports/localization/`, `INV-B:142`),
  - `task` (SPEC:121; no output flag, `INV-B:202`),
  - `explain` (SPEC:108; "write the explanation to a file", no flag named).
  Rows that do say "add `--output`" (analyze SPEC:99, spec-panel SPEC:120, business-panel SPEC:102, design SPEC:106, index SPEC:111) show the spec knows how to state it; the seven rows above omit it.
- Concrete attack, with state trace. `/sc:save --unattended` (the literal command in AC-3.4, SPEC:207). Before: no `<output-dir>` exists, because `save` has no flag that carries one. WC-4 guard "brief gives no output path and this paragraph names none" evaluates true. After: refusal, no per-session memory file, no contract, `--outcome failed` (WC-5). AC-3.4 expects two new per-session files and fails. The same trace on `/sc:cli-eval run --unattended` with no `--suite` (AC-2.2, SPEC:200) expects a contract with `status: blocked` and a non-empty `blocked_question`, but WC-4 says no file is written.
- Recommendation (narrow): in each of the seven rows either add the output flag (as the analyze row does) or name the fixed contract path in WC-4's exception list. Do not add a new mechanism.
- Priority: High. Quality impact: Testability and Completeness, about -2 each until fixed.

### B2. Six ready commands are told both to write a WC-4 contract and to gain nothing (CRITICAL under FR-19: a dimensional mismatch, blocking)

- Experts: Fowler (leads count annotation), Whittaker (consistency check), Wiegers (traceability).
- Defect. Stated texts that cannot all hold:
  1. SPEC:79: ready commands report "the named file until Phase 1 adds the contract".
  2. SPEC:76: a ready command "gains [the Unattended section] only where its small-fix column adds an unattended gate resolution"; adversarial, brainstorm, cleanup-audit, index-repo, init-lite and workflow "gain none (REQ-2)".
  3. SPEC:159: P1 makes "fixes only to adversarial, cleanup-audit, index-repo (no section)"; their rows (SPEC:83, 85, 86) name a contract filename, a `--pass all` report name and an output location, but no contract.
  4. SPEC:62: WC-4 names contract paths for cleanup-audit (`.claude-audit/return-contract.yaml`), init-lite (`<file>.return-contract.yaml`) and workflow, and says the contract is written "in unattended mode". These three commands have no unattended mode (no section, so no `--unattended`; SPEC:73 says the brief omits it for them).
  5. SPEC:73 and SPEC:182: the report path the worker sends is "the contract path WC-4 gives for that command".
  6. SPEC:63: no report means `--outcome failed`.
- Quantity Flow (see diagram below): 36 dispatchable commands expect a WC-4 contract; the spec delivers one for 33 (30 that gain a section, plus the pre-existing contracts of adversarial, brainstorm and workflow). Three consumers expect a producer that does not exist: cleanup-audit, init-lite, index-repo. For index-repo no path is named anywhere (`INV-A:53` implies `PROJECT_INDEX.md`; SPEC:86 says "brief must pass: none").
- Concrete attack. Coordinator follows SPEC:73: brief for `/sc:cleanup-audit --pass 1` sets report path `.claude-audit/return-contract.yaml`. Audit finishes and writes `.claude-audit/pass1-summary.md` (`INV-A:42`). No phase creates the contract. Worker applies WC-5: no report exists, `--outcome failed`. A successful audit is recorded as failed and its Task is retried or tripped toward the circuit breaker (`CAPS:80`, three failures).
- Recommendation (narrow): pick one rule for the three commands that have no contract. Either state in SPEC:83-87 that the worker's report path is the named existing file for these commands (and remove their paths from WC-4's exception list and from SPEC:182's rule), or add a one-line contract fix to their rows. Delete or correct SPEC:79 "until Phase 1 adds the contract" to match.
- Priority: High. Quality impact: Consistency -2, Testability -1.

=== ARCHITECTURE ANALYSIS ===

Architecture findings of weight are all follow-up candidates (Medium) except B2 above, which Fowler also raised. The decision itself (SPEC:16, 28-39) is well supported: depth 1 (`CAPS:97-101`), standalone breakage (`CAPS:147-149`), completion bound to the dispatched pane (`CAPS:150`) and the existing nested-spawn gap (`CAPS:155`) each hold as quoted. Fowler agrees with the boundary choice. Newman finds the shared-contract-file approach sound (SPEC:52) but sees no schema version (see N4).

## Guard Condition Boundary Table

Trigger met: the spec contains thresholds, boolean guards and sentinel comparisons. Responsibility: Nygard builds, Crispin validates completeness, Whittaker attacks. Classes left out are named with a reason in the "Classes left out" list under the table. FR-10: every guard below is enumerated and every cell is populated.

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|-------|----------|-----------------|----------------|--------------|-------------------|--------|
| output-path present (WC-4) | SPEC:62 | Zero/Empty | flag absent, command has an output flag | false | chat-only refusal naming the flag, no file, `--outcome failed` | OK |
| output-path present (WC-4) | SPEC:62 | Zero/Empty | `--output ""` (flag present, empty value) | unspecified | none | GAP (Medium, M7) |
| output-path present (WC-4) | SPEC:62 | Typical | `--output <dir>` | true | `<dir>/return-contract.yaml` | OK |
| output-path present (WC-4) | SPEC:62 | Sentinel Value Match | command with no output flag (save, cli-eval, research, recommend, review-translation, task, explain) | always false | rule says refuse; rows and AC-3.4 expect success | GAP (blocking, B1) |
| output-path present (WC-4) | SPEC:62 | Maximum/Overflow | `<dir>` cannot be created or written | unspecified | WC-4 says contract "on every outcome"; nothing for a dir that cannot be written | GAP (Medium, M7) |
| output-path present (WC-4) | SPEC:62 | Legitimate Edge Case | output flag names a file (tdd, init-lite, spec-panel) | true | sibling `<file>.return-contract.yaml` | OK |
| outcome mapping (WC-5) | SPEC:63 | Zero/Empty | no report exists | true | `--outcome failed` | OK |
| outcome mapping (WC-5) | SPEC:63 | Zero/Empty | contract file exists, 0 bytes or not parseable | unspecified | none (only the live check, SPEC:183, tests this) | GAP (Medium, M2) |
| outcome mapping (WC-5) | SPEC:63 | Typical | `status: succeeded` | true | `--outcome succeeded` | OK |
| outcome mapping (WC-5) | SPEC:63 | Sentinel Value Match | `status` outside the four values (pre-existing contracts keep their fields, values never read: `INV-B:272`) | unspecified | none | GAP (Medium, M2) |
| outcome mapping (WC-5) | SPEC:63 | Legitimate Edge Case | `partial`; audit verdict FAIL; `blocked` | n/a | `succeeded`; `succeeded`; `failed` | OK |
| outcome mapping (WC-5) | SPEC:62-63 | Legitimate Edge Case | stale contract from an earlier invocation left in a reused dir (cleanup-audit fixed `.claude-audit/`, same-dispatch re-invocation) | unspecified | none: no "remove or overwrite at start" rule | GAP (Medium, M3/M7) |
| wait-split (WC-10) | SPEC:68 | Typical | single call 3 min | false | no split | OK |
| wait-split (WC-10) | SPEC:68 | Legitimate Edge Case | single call of exactly 5 min, or 4 to 5 min | false ("longer than 5") | no split required, yet a 5-min heartbeat cadence cannot fire during the call | GAP (Medium, minor) |
| wait-split (WC-10) | SPEC:68, SPEC:104 | Maximum/Overflow | eval timeout 3600 s (`INV-A:65`) | true | waits of at most 4 min | OK |
| unattended token (D1, section 2.1) | SPEC:51, 228 | Zero/Empty | `--unattended` absent | false | standalone behaviour unchanged (SA-1) | OK |
| unattended token (D1, section 2.1) | SPEC:51, 228 | Typical | standalone `--unattended` | true | mode on | OK |
| unattended token (D1, section 2.1) | SPEC:228 | Sentinel Value Match | literal `--unattended` inside quoted prompt text (a topic or symptom string) | unspecified | none; "cannot misfire on a person" holds only for a typed flag | GAP (Medium, M6) |
| unattended token (D1, section 2.1) | SPEC:73, 128 | Legitimate Edge Case | flag passed to a command with no section (six ready commands, six coordinator-only) | unspecified | none (SPEC:73 tells the brief to omit it for the six ready ones; nothing for the rest) | GAP (Medium, M6) |
| retry output dir (WC-6, 2.3) | SPEC:64, 73 | Typical | `--retry-of` with a new dir | true | fresh run | OK |
| retry output dir (WC-6, 2.3) | SPEC:73 | Legitimate Edge Case | retry that resumes (roadmap, cleanup-audit) | true | same dir plus resume flag | OK |
| retry output dir (WC-6, 2.3) | SPEC:64, 73 | Sentinel Value Match | brief reuses an earlier dispatch's dir with no resume flag | unspecified | only a duty on the coordinator; the command cannot detect it | GAP (Medium, M3) |
| outward default off (WC-9) | SPEC:67 | Typical | no flag in brief | false | action off | OK |
| outward default off (WC-9) | SPEC:67, 121, 113 | Legitimate Edge Case | action with no explicit flag (task `commit`/`push` keywords `INV-B:204`; post-release conversational pre-authorization `INV-B:79`) | unspecified | WC-9 says the "command's own explicit flag" turns it on; none exists | GAP (Medium, M8) |
| confidence guard (task row) | SPEC:121 | Typical | confidence 0.5 | true | blocked | OK |
| confidence guard (task row) | SPEC:121 | Legitimate Edge Case | confidence exactly 0.70 | false ("below 0.70", `INV-B:199`: "< 0.70") | proceeds | OK |
| `--monitor` ordinal (pr-submit row) | SPEC:114 | Legitimate Edge Case | `--monitor 1` / `--monitor 3` / other ordinals | true / false / unspecified | refused / no y/n gate (`INV-B:89`) / none for other ordinals (UNVERIFIED: the sandbox evidence names only 1 and 3) | GAP (Medium, low; P4 and D3 gated) |

Classes left out: One/Minimal is left out of every guard because none of them has a size boundary (they test presence, set membership or a duration, not a collection). Zero/Empty is left out for wait-split (no waiting step means the guard is never evaluated), for retry-dir (no retry means the guard is never evaluated), for the confidence guard (a computed value is never empty) and for the `--monitor` guard (flag absence uses the default). Maximum/Overflow is left out for the unattended token, retry-dir, outward-default, confidence and `--monitor` guards (no capacity). Sentinel Value Match is left out for wait-split and the confidence guard (no reserved value).

Crispin: table complete under FR-10; GAP rows are listed once as follow-up candidates, graded per FR-8/FR-9 (only the output-path/no-flag row names a concrete wrong outcome, so only it is blocking, as B1).

## Quantity Flow Diagram (FR-21)

```text
[Source: 43 commands (21 INV-A + 22 INV-B)] --> [Classify SPEC:76]
    --> [10 ready (SPEC:81-92)]            N=10
    --> [27 need change (SPEC:99-125)]     N=27
    --> [6 coordinator-only (SPEC:132-137)] N=6        sum 43, conserved

[10 + 27] --> [exclude /sc:load: not its own Task (SPEC:112)] --> [36 dispatchable]
[36 dispatchable] --> [WC-4 contract expected by coordinator (SPEC:73, 182)]: 36 consumers expect a contract
    producer A: 30 commands gain a section (P1 8, P2 11+4, P3 4, P4 3)
    producer B: 3 pre-existing contracts (adversarial, brainstorm, workflow)
    --> [33 contracts delivered]
    --> MISMATCH: 36 expected vs 33 delivered: cleanup-audit, init-lite, index-repo   (finding B2)
    (note: pr-submit counts only if D3 option b is chosen; under recommended D3 option a it is 35 expected, 32 delivered, same 3 missing)

Phase distinct commands touched: P1 12 + P2 15 + P3 4 + P4 3 = 34 = 27 + 7 ready-with-fix; ready-untouched 3 (brainstorm, init-lite, workflow); 34 + 3 + 6 = 43, conserved.
```

## Whittaker adversarial analysis

All findings use the template; severity per the panel classes.

1. I can break this specification by **Zero/Empty Attack**. The invariant at **WC-4 refusal clause (SPEC:62)** fails when **the command has no output flag**. Concrete attack: run `/sc:save --unattended` as AC-3.4 does. Before: no per-session memory file, no contract. After: chat-only refusal, still none. Expected by AC-3.4: two new files. (MAJOR, blocking: B1.)
2. I can break this specification by **Sequence Attack**. The invariant at **WC-3 plus WC-4 (SPEC:61-62)** ("contract written on every outcome"; ask, then re-invoke with the answer) fails when **the first invocation blocks and the re-invocation dies before writing**. Concrete attack: invocation 1 writes `status: blocked` to dir D. Worker `ask`s, gets the answer, re-invokes into D (the same dispatch, so WC-6 does not force a fresh dir). The run crashes mid-way. State after: D still holds the `blocked` contract; WC-5 reads it and sends `failed`, or, if the stale file said `succeeded` from a prior pass, the opposite. The same holds for cleanup-audit's fixed `.claude-audit/` directory across two audits. (MAJOR: contract can be stale; Medium by the grading check because it needs a crash. M3, M7.)
3. I can break this specification by **Sentinel Collision Attack**. The invariant at **section 2.1 and D1 (SPEC:51, 228)** ("testable by grep and cannot misfire on a person") fails when **the literal text `--unattended` appears inside quoted prompt content**. Concrete attack: `/sc:troubleshoot "login fails after adding --unattended to the launcher"` typed by a person. If the command matches the token anywhere in its arguments, the gates switch off and nothing in the spec says the match must be a standalone, unquoted token. (MAJOR, Medium by grading: needs a lazy matcher. M6.)
4. I can break this specification by **Divergence Attack**. The invariant at **WC-9 (SPEC:67) versus the D4 mechanism (SPEC:245)** fails when **the outward action has no explicit flag**. Concrete attack: brief authorizes `commit` for `/sc:task`; `task` takes `commit`/`push` as task keywords (`INV-B:204`), not flags. WC-9 says outward actions turn on only by the command's own explicit flag, so the authorized path does not exist; an implementer either never allows it or invents a flag. Same for post-release's conversational pre-authorization. (MAJOR, Medium by grading: P4-gated. M8.)
5. I can break this specification by **Accumulation Attack**. The invariant at **WC-6 and section 2.3 (SPEC:64, 73)** (every retry gets a new directory) fails when **retries accumulate**. Concrete attack: three failed dispatches of `/sc:tdd` leave three `.dev/tasks/to-do/TASK-TDD-<ts>/` research packages (`INV-B:222`) plus three output files; the circuit breaker (`CAPS:80`) caps failed starts, not artifact growth, and `worker-release` only closes the terminal (`CAPS:109`). Nothing states who cleans up. (MINOR.)

## Critique findings by expert (non-blocking)

M-numbers are Medium (warning) and not blocking; N-numbers are minor notes. None of them triggers a revision or enters the Reviser brief.

### Requirements (Wiegers, Adzic, Cockburn)

- M2 (Wiegers, MAJOR label, Medium by grading): the status vocabulary and required fields of pre-existing contracts are never read. WC-4 requires `status` in four values, `command`, `report_path`, `artifacts` (SPEC:62) and says existing contracts "keep their fields and add the missing ones". The only description of workflow's contract is the field list `status`, `plan_path`, `reflect_report_path` (`INV-B:272`) with no `command`, `report_path` or `artifacts`, and no row changes workflow, brainstorm (`SPEC:84`) or reflect's contract fields. The live check's `d['command']` assertion (SPEC:183) therefore may not pass for those commands. Related: AC-0.4 says "step 4 uses the command's existing report file" (SPEC:194) but step 4's assertion parses YAML and reads `status` and `command` (SPEC:183); troubleshoot's existing report is `REPORT.md` (`INV-B:242`), not YAML. Recommendation: say that AC-0.4's step 4 is `test -s` only for P0.
- M3 (Wiegers/Nygard): WC-3 says the worker "may instead ask" (SPEC:61), while AC-2.2 and AC-4.1 require `--outcome failed` plus a `blocked` contract (SPEC:200, 208) and WC-5 maps blocked to failed. A worker that chooses `ask` never produces the observed outcome, so those checks are not deterministic unless the brief forbids `ask` (2.3, SPEC:73, does not say). Also, "re-invoke ... with the answer as a flag" (SPEC:61) has no flag for two blocked gates: cli-portify's approvals (SPEC:105 adds only `--resume <contract>`) and pr-submit's operator HALTs (SPEC:114), so a resumed run reaches the same gate.
- M6 (Wiegers): see Whittaker 3 and the table: the token match rule and the behaviour of `--unattended` on a command without a section are not defined.
- M8 (Cockburn/Wiegers): see Whittaker 4. In addition, D4 (SPEC:244-247) governs auggie-review and task, both in P2 (SPEC:160), while SPEC:154 says only P4 waits on D2-D4. The P2 rows build the re-enable path (`--post-pr` returning, SPEC:100) before D4 decides, and D4 option (b) "Never" would remove it. Recommendation: say P2 builds it only as a pending recommendation, or move that clause to P4.
- M9 (Wiegers): the `index` row asks the command to "state that knowledge-base mode does not wait" (SPEC:111), while the same row says whether it waits is UNVERIFIED (`INV-A:54`, `INV-A:83`). An assertion is written without a check, and if the mode does wait, the worker stalls. The business-panel and explain rows refuse the mode instead (SPEC:102, 108); index should do the same.
- M12 (Wiegers): SPEC:154 says "Phases 1-3 need no user decision", yet P3 asks implementers to choose which side wins when command and skill disagree (validate-roadmap report filename, roadmap flag surface; SPEC:118, 124, AC-3.1 SPEC:204). `INV-B:309` records that no file says which side wins. AC-3.1 passes either way, which hides a user-visible choice.

### Architecture (Fowler, Nygard, Newman, Hohpe)

- M1 (Fowler): the spec assigns WC-3, WC-5, WC-7, WC-10 and WC-12 to the "worker session" (SPEC:61, 63, 65, 68, 70) but never says how that session is told. Section 2.3 lists what the brief carries (SPEC:73) and omits these rules; the Unattended section of a command lists only that command's gates and report (SPEC:52); SA-2 limits Orca mentions in the contract file to "an example of a caller's question channel" (SPEC:147). Orca's own preamble covers `ask`, `check` and `worker_done` generally (`CAPS:60-61`, `CAPS:73`) but not the IronClaude-specific mapping in WC-5 (partial to succeeded, first-sentence rule) or the 4-minute wait split. Recommendation: add one line to 2.3 that the brief tells the worker to follow WC-3, 5, 7, 10, 12, with the contract file as the source.
- M4 (Nygard/Fowler): `--unattended` propagation to nested `/sc:` commands is never specified. Examples in the inventories: tasklist Stage 9 runs `sc:task --compliance strict` (`INV-B:211`) and task has person-blocking gates (SPEC:121); roadmap writes memory through `sc:save` at every wave (`INV-B:154`); release-split nests brainstorm and adversarial (`INV-B:119`); workflow nests reflect (`INV-B:269`). Only tdd's nested `/task` (SPEC:90) and tasklist's reflect (SPEC:122) are handled. A tasklist worker whose Stage 9 task hits TFEP "present to user" (`INV-B:199`) stalls with no `worker_done`.
- M5 (Fowler): the tasklist row asserts its reflect fan-out "runs one layer below the worker, inside Claude Code's nesting limit" (SPEC:122, `INV-A:14`). `INV-B:210` and `INV-B:314` (item 1) say nested spawning is UNVERIFIED, and `INV-B:322` (item 8) says who answers the reflect offer inside subagents is UNVERIFIED. `INV-B:215` recommends calling reflect without `--remediate`, or at the worker's top level. The spec chose a third option (pass `--unattended` so the headless rule applies, SPEC:122) with no Decisions entry, did not carry INV-B items 1 and 8 into its UNVERIFIED list (SPEC:271-285), and does not say how the Stage 10.5 `needs_human_decision` HALT (`INV-B:209`) resolves under WC-2.
- M7 (Nygard): the failure modes of the contract itself are open. WC-4 says "written on every outcome" (SPEC:62), which cannot hold on a crash or context exhaustion; WC-5 then relies on "no report exists" (SPEC:63) while stale files can exist (table row, Whittaker 2); nothing says to remove or overwrite any prior contract at start; and nothing says what the worker does if `worker_done` itself fails with `runtime_unavailable` (`CAPS:147`), although Orca offers `--retry-request` and `request-show` for exactly that (`CAPS:117`). Related: no upper bound on a Dispatch is assumed (SPEC:282, UNVERIFIED), so a looping command is detected only by a missing `worker_done`.
- M10 (Fowler): AC-C1 (SPEC:172) greps `src/superclaude/core` for `orca orchestration|worktree|terminal|agent` and requires no output, but P0 puts the contract file and an Orca section of HOW-WE-WORK.md in `core/` (SPEC:158), and SA-2 allows the contract file to mention Orca as a question channel (SPEC:147). The natural wording (`orca orchestration ask`) fails AC-C1 in every phase. Likewise AC-C5 (SPEC:176) requires no removed line, while SA-4 says new flags are additive (SPEC:149): adding flags to an existing Usage line removes that line in a `-U0` diff. State that new flags go on new lines, or that AC-C5 ignores the Usage line.
- N4 (Newman): WC-4 carries no schema version, while workflow's contract is versioned 1.1 (`INV-B:272`). With a fixed status set (SPEC:262) and "keep their fields", the schema can drift without a marker.
- N5 (Hohpe): ordering and delivery are handled well for `worker_done` (exactly once, `CAPS:73`, `CAPS:77`) and follow-ups (pull-only, WC-12). The gap is the transport-failure rule in M7.

### Minor notes (never fail the review)

- N1. E3 (SPEC:23) offers `invocation_method: "skill-direct"` as evidence the direct route "has worked before"; section 1.4 (1) (SPEC:43) says that same run proves only the nested route. `INV-A:13` reads the same field as direct. Align the wording.
- N2. The body cites review ids that this document does not define: REQ-1, REQ-2, ARCH-1, NEW-1 (SPEC:62, 64, 73, 76, 92, 182, 200). They belong to `review/spec-panel.md` and `review/disposition.md`, which a reader of the spec does not have.
- N3. UNVERIFIED item 14 (SPEC:285) is a status note about a citation check, not an unverified claim.
- N6 (Adzic). No example contract file appears anywhere, although WC-4 is the central interface; one worked example would settle most of M2. No Given/When/Then scenario is given for a blocked gate.
- N7. Vague pass conditions: WC-1 "well inside the readiness limit" (SPEC:59); AC-1.4 "names one fixed path" (SPEC:198); 7.2 step 5 searches the whole transcript for `AskUserQuestion` (SPEC:184), which can also match command text that says "never AskUserQuestion" (`INV-B:239`); the pass condition says "call".
- N8. WC-9 cites `README.md:31` as evidence (SPEC:67); that line is a rule for this planning run (README.md:31), not product policy.
- N9. SPEC:252 calls R1 a "protection"; R1 is a reason, not a safeguard.
- N10. The pr-submit top-level rule is cited as `sk/sc-pr-submit-protocol/SKILL.md:37-39` (repo copy, `INV-B:90`) and as `:47-49` (installed copy, `CAPS:161`); the two copies differ by 10 lines. UNVERIFIED whether they diverge in content.
- N11. Scope completeness is UNVERIFIED: the skill listing visible to this reviewer names `sc:graph`, `sc:impact` and `sc:issue`, which neither inventory covers, and `sc:issue` is described as creating an Orca worktree. If those commands exist in `src/superclaude/commands/`, E5 (SPEC:25), the 43-command count (SPEC:76) and AC-C1's empty baseline (SPEC:172) would need rechecking. Not checkable inside the sandbox.

## Follow-up candidates (Medium and minor; none blocks)

M1, M2, M3, M4, M5, M6, M7, M8, M9, M10, M12 (above), every Medium GAP row of the Guard Condition Boundary Table (output-path empty value and unwritable dir, empty or unparseable contract, status outside the four values, stale contract, wait-split boundary at 5 min, `--unattended` inside quoted text, flag on a command with no section, retry-dir reuse, outward action with no flag, `--monitor` ordinals), and N1 to N11. Per the command, the session that runs a review asks the user once per loop whether to open an issue for this list and creates none without an answer. This run was a worker with a fixed one-line reply, so the question was not asked and no issue was created; the list is recorded here for the coordinator.

## Expert consensus and quality assessment

```yaml
specification_review:
  original_spec: .dev/orca-command-refactor/specs/orca-worker-contract-spec.md
  review_date: 2026-11-10
  expert_panel: [wiegers, adzic, cockburn, fowler, nygard, whittaker, newman, hohpe, crispin(table only)]
  focus_areas: [requirements, architecture]
  review: "1 of 3"
quality_assessment:
  overall_score: 6.5
  clarity: 7.5          # tables, explicit evidence, consistent ids
  completeness: 6       # contract location, nested propagation, failure modes open
  testability: 6        # most checks concrete; B1 makes two ACs unreachable
  consistency: 6        # B2 plus the 3.1 intro; counts and row mapping otherwise clean
critical_issues:
  - {id: B1, category: requirements, severity: MAJOR, blocking: true, expert: wiegers, issue: "WC-4 refusal clause + no output flag on 7 commands; AC-3.4 and AC-2.2 cannot pass", recommendation: "add the flag in each row or list a fixed contract path"}
  - {id: B2, category: requirements, severity: CRITICAL, blocking: true, expert: fowler, issue: "36 expected contracts vs 33 delivered; cleanup-audit, init-lite, index-repo", recommendation: "choose one report-path rule for the three commands and align SPEC:79, 62, 182"}
expert_consensus:
  - "The Orca-on-top decision and its evidence hold (CAPS:97-101, 147-150, 155)."
  - "Counts, phase membership and per-command rows are consistent with the inventories."
  - "The contract (WC-4/WC-5) is the weak interface: location, vocabulary and staleness are under-specified."
improvement_roadmap:
  immediate: [B1, B2]
  short_term: [M1, M2, M3, M4, M5]
  long_term: [M6, M7, M8, M9, M10, M12, N4, N6]
adversarial_analysis: "see the Whittaker section above (5 findings; 1 blocking = B1)"
```

## Reviser brief

Blocking finding ids: B1, B2. Revision rules (restated from the Review Loop, bullet 6; the reviser reads this report, not the command): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, and the bytes added and deleted per finding id; leave Medium and minor findings alone; return the candidate once and do not award yourself a PASS.

verdict: FAIL

review: 1 of 3

# /sc:spec-panel critique, round 1

- command: `/sc:spec-panel @.dev/orca-command-refactor/specs/orca-worker-contract-spec.md --mode critique --focus requirements,architecture`
- candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md` (285 lines)
- candidate sha256: `d3cdbe573e57303b9ce6c93d1fe98ba18fb7cb1a15773d926bf6a0c31425200d`
- baseline: none given, `--re-review` not given: first review of the full document
- reviewer model used: claude-sonnet-5-5
- review date: 2026-11-10
- panel (focus requirements, architecture; Whittaker is active in every panel): Wiegers (lead), Adzic, Cockburn, Fowler (lead), Nygard, Whittaker, Newman, Hohpe
- hard gate: `~/.claude/rules/prompts/document_review_loop_prompts.md` read in full; the FIRST-REVIEW prompt and its Grading check were applied. This report is ONE first review. The "three first reviews + MERGE rule" belong to the coordinator; no merge is done here.

## Coverage

- Read in full: the candidate (1-285), `.dev/orca-command-refactor/README.md`, `inventory/orca-capabilities.md` (called CAPS), `inventory/commands-a.md` (INV-A), `inventory/commands-b.md` (INV-B, lines 25-84 and 260-323).
- Checked against the inventories: every `CAPS:N`, `INV-A:N` and `INV-B:N` citation I sampled in sections 1, 2, 3, 4 and 9 (about 60) points at text that says what the spec claims. The counts 43 = 10 + 27 + 6 hold (3.1 lists 10, 3.2 lists 27, section 4 lists 6; the INV-A split 5/13/3 and INV-B split 5/14/3 add up to the same totals). Every 3.2 command has a phase in section 6 (counted one by one).
- UNVERIFIED (cannot be checked inside the workspace; there is no `src/`, no `.claude/`, no `.dev/codegraph-migration/`, no `.dev/evals/`, and no `CLAUDE.md`): every citation of `src/superclaude/commands/*`, `src/superclaude/skills/*`, `src/superclaude/cli/install_core.py`, `CLAUDE.md:N`, `HOW-WE-WORK.md:N`, `pyproject.toml:38`, `Makefile:68-74`, `.dev/codegraph-migration/orchestration/README.md:31,33,42`, `return-contract.yaml:10` and `EVIDENCE.md:N` (the last is only checkable through the quotes in CAPS:49). The spec's own claims about its fresh-context citation check (candidate lines 11 and 285) are UNVERIFIED too.
- Not covered: the actual command and skill files, so whether a "small fix" in 3.1/3.2 is correct is not judged. Focus areas testing, compliance and correctness were not requested; the State Variable Registry is not produced (only required under `--focus correctness`).

## Quality read (0-10, advisory)

Clarity 8, Completeness 6, Testability 5, Consistency 6. The decision (section 1) is well argued and honest about its evidence gaps (1.4). The weak part is the acceptance and rollout machinery (sections 6-7), which contradicts the per-command tables in places.

=== REQUIREMENTS ANALYSIS ===

### F1 - CRITICAL (blocking) - Wiegers, Adzic, Cockburn
**P1 gate and AC-1.1 require an `## Unattended mode` section (naming `return-contract.yaml`) from every command in sections 3.1-3.2, but the same document says several of those commands get no report file, no change, or wait for a user decision.**

Texts that contradict each other:
- AC-1.1 (candidate line 195): "asserts that every command in sections 3.1-3.2 has a `## Unattended mode` section naming `return-contract.yaml` and `~/.claude/WORKER-CONTRACT.md`".
- P1 scope (line 159): "the `--unattended` flag accepted by every command in sections 3.1 and 3.2 (a no-op where a command has no gate)".
- `/sc:load` row (line 112): report "none (see note)", resume "n/a", "use it as a step inside another worker's brief, not as its own Task", phase "P1 (usage line only)". Decisions table (line 265): "a report file would be an unrequested addition. Only its usage-line defect is fixed."
- 3.1 intro (line 79): "The only command changes are the small fixes in the last column", and the brainstorm and init-lite rows say "None" (lines 84, 87).
- Line 154: "Phases 1-3 need no user decision; Phase 4 waits for answers to D2-D4". The implement (D2), post-release (D4) and pr-submit (D3) rows are phase P4 (lines 109, 113, 114). D3 (a), the recommended answer, is "no pr-submit changes in Phase 4" (line 240), and line 139 says pr-submit "stays a worker candidate only if the user accepts open decision D3".

Grading check: An implementer who follows the stated text as written builds, in P1, a contract-naming `## Unattended mode` section in `/sc:load` (which the Decisions row says gets no report file), in brainstorm and init-lite (which the 3.1 intro says change only by small fixes, and the table says none), and in implement, post-release and pr-submit (whose changes the spec holds for D2-D4 answers that Phases 1-3 are said not to need), and X is wrong because the P1 acceptance test (AC-1.1) cannot pass without editing a command the spec elsewhere says must not be edited, so the phase gate either fails or forces the contradicted edit.

Origin: the document's own text, not inherited. (UNVERIFIED which of the two readings the author meant; the contradiction does not depend on that.)

### Medium findings (follow-up candidates, not blocking)

- **W1 - WC-4 says the report path is "known before dispatch", but several rows give a path the coordinator does not choose.** Workflow's contract sits at `.dev/tasks/to-do/<id>/` (line 92, the `<id>` is generated by the command; INV-B:272), cleanup-audit uses a fixed `.claude-audit/` (line 85), and the workflow P1 fix "write the contract for pre-creation STOPs too" names no directory, though at a pre-creation stop no `<id>` directory exists (INV-B:272 says it is not written for pre-creation STOPs). Missing requirement (Wiegers): where the file goes. Adversarial's contract is `<output>/adversarial/return-contract.yaml` (line 83), which also differs from the WC-4 form `<output-dir>/return-contract.yaml`.
- **W2 - SA-3 and WC-4 disagree on when the contract is written.** WC-4 (line 62) says "In unattended mode"; SA-3 (line 148) says "only in unattended mode or when the caller passes the new output flag"; AC-1.3 (line 197) tests only the case with neither. With the output flag and no `--unattended` the behaviour is not stated (Wiegers).
- **W3 - Stale-report risk.** WC-4 requires a file on every outcome but no field that ties it to this run (no dispatch id, start time or contract version). Resume commands reuse their output directory (3.1 brainstorm, tdd, release-split), so a leftover `status: succeeded` file survives a retry that stalls before writing, and AC check 7.2.4 (`test -s`, status in the allowed set) would pass on it (Nygard, Newman). Also, WC-6 says a re-run "writes each run into a fresh output directory", but 2.3 and 7.2.1 fix the output directory in the Task spec, and a `--retry-of` start reuses that Task, so the retry gets the same directory. Who supplies the fresh directory is not stated (Fowler).
- **W4 - "refused" is a fourth gate outcome that WC-2 does not define.** WC-2 (line 60) allows only default, caller flag or blocked, but 3.2 uses "refused" for `--interactive`, `--watch`, `--monitor 1`, `--mode socratic`, `--format interactive`. Which `status` the contract gets (failed or blocked) and whether a contract is written is not stated (Adzic, Whittaker zero/empty attack).
- **W5 - `partial` has no trigger.** WC-5 maps `partial` to `succeeded`, but no 3.2 row says when a command reports `partial`. Example: cleanup/improve list "Approval Required" items unapplied (lines 103, 110); whether that is `succeeded` or `partial` is left to the implementer (Wiegers).
- **W6 - WC-3 reaches `/sc:implement` too.** WC-3 (line 61) lets a worker `ask` the coordinator for any blocked gate. The implement row (line 109) and D2 (a) (line 234) say the worker stops and ends failed, and the Ruling rule says another agent's message is not acceptance (`refs/qa.md:238`, UNVERIFIED; INV-A:66 quotes it). A worker that follows WC-3 for the Ruling gate gets an answer it cannot accept, or silently moves toward D2 (b) (Cockburn, Nygard).
- **W7 - `--unattended` token edge.** D1 (a) calls the switch an "explicit flag" but nothing says how a quoted prompt containing the text `--unattended` (for example `/sc:tdd "explain --unattended"`) is treated. Sentinel-collision attack (Whittaker): I can break this specification by Sentinel Collision. The invariant at D1 / WC-2 fails when the literal appears inside quoted user content. Concrete attack: before, a person runs the command with that text in the topic; after, the command suppresses its prompts. Severity MAJOR but graded Medium (a missing restriction, not a stated text that does harm).
- **W8 - Phase gating text.** The P1 row says "No person gate is involved" (line 159) while the P1 commands business-panel, explain, test have refusal rules (lines 102, 108, 123) and AC-1.2 (line 196) tests only the happy path. Refusal behaviour has no check in any phase.
- **W9 - Ready commands and `--unattended`.** 2.3 (line 73) tells the coordinator to put `--unattended` in every brief, but the 10 "ready today" commands do not accept it until P1, and AC-0.4 (line 194) runs them without it. The brief template for P0 does not say to omit it.

=== ARCHITECTURE ANALYSIS ===

### F2 - MAJOR graded blocking - Fowler, Nygard, Whittaker
**AC-C5, the check that enforces "edits are additive" (SA-1, SA-4), cannot see a deleted bullet line.**

Text: AC-C5 (candidate line 176): `git diff -U0 master...HEAD -- src/superclaude/commands/<name>.md | grep -E '^-[^-]'`, pass condition "prints nothing: edits are additive". SA-4 (line 149) depends on it: "Command-file edits in Phases 1-3 are additive".

Attack (Whittaker, Sequence/Zero attack): the regex `^-[^-]` skips every removed line whose own text starts with `-`. A deleted markdown bullet `- foo` appears in a diff as `-- foo`, and a deleted frontmatter fence `---` appears as `----`. I ran `printf -- '-- removed bullet\n-removed plain\n--- a/file\n-|row\n' | grep -E '^-[^-]'` in the sandbox: it printed only `-removed plain` and `-|row`; the removed bullet and the file header were not printed. Command files are bullet-heavy lists (the command definition under review itself is, for example, the `- **Karl Wiegers**...` lists at its lines 53-66), so the common deletion goes unreported. AC-0.3 (line 193) uses the same regex but guards table rows that start with `|`, which are caught; only AC-C5 is affected.

Grading check: An implementer who follows the stated text as written builds a check that prints nothing for a diff that deletes `- ` lines from a command file, and passes the "additive" phase gate, and X is wrong because the gate is meant to prove standalone behaviour (SA-1) is untouched, and a deleted prompt or flag bullet is exactly a standalone change it must catch.

Origin: the document's own text. (UNVERIFIED that any specific command file would be edited this way; the check's blind spot is shown by the run above and needs no further assumption.)

### Medium findings (follow-up candidates, not blocking)

- **A1 - AC-C1 contradicts what P0 itself adds.** AC-C1 (line 172) must print nothing over `src/superclaude/{commands,skills,agents,core}`, but P0 (line 158) adds `WORKER-CONTRACT.md` (core) containing a coordinator brief template, and an Orca section in `HOW-WE-WORK.md` (core). Either will naturally contain `orca orchestration ...`, matching the AC-C1 pattern. SA-2 (line 147) allows an Orca mention "inside the contract file" without saying whether `return-contract.yaml` or `WORKER-CONTRACT.md` is meant (Fowler). Also the check line is written with `\|` escapes for the markdown table; copied as-is into a shell the escapes are literal (UNVERIFIED how the author's shell treats them).
- **A2 - Tasklist depends on a reflect change and on an unknown.** The tasklist row (line 122) makes Stage 10.5 pass `--unattended` to each reflect "so the headless rule applies". That works only after the reflect P2 change (line 88, same phase; the dependency is not stated), and UNVERIFIED item 9 (line 280) assumes an Orca worker is not headless. What the "headless auto-accept" does for `--remediate` (accepts it, launching a corrective-package handoff?) is not stated, and INV-B:46 recommended dropping `--remediate` in 10.5 instead. Also "inside Claude Code's nesting limit, INV-A:14" (line 122) is not counted: worker, tasklist subagent, reflect reviewers, adversarial merge reaches the three-layer limit INV-A:14 describes (Newman).
- **A3 - WC-3 has no cap on `ask` resumes.** An `ask` timeout leaves the question pending and the worker resumes the same id (line 61, CAPS:60). No limit or escalation after repeated timeouts is stated, and WC-10 says no heartbeat is sent while blocked, so a worker blocked in repeated `ask` is silent for unbounded time (Nygard accumulation attack). CAPS:130 and 64 support the heartbeat rule.
- **A4 - WC-10 margin.** Heartbeat every 5 minutes, waits of at most 4 minutes: the 1-minute margin must also hold the tool call overhead and the heartbeat call itself. AC-4.3 (line 210) checks only "at most 5 minutes apart" and "no single call exceeds 240 s". Cadence source is the preamble, not a guide (CAPS:130), UNVERIFIED beyond this worker's preamble.
- **A5 - Contract schema is unversioned.** WC-4 lists fields but no `contract` version, although the existing workflow contract has a version (line 92 / INV-B:272 "contract 1.1"). Adding fields later cannot be told apart by a reader (Newman, Hohpe).
- **A6 - No acceptance check for WC-1, WC-7, WC-11, WC-12.** The 7.2 live check covers readiness only through "state: ready" (line 180); no phase tests that the launch path has no unanswered startup question, that no command was wrapped in a subagent beyond the P0 transcript check, parallel-safe writes, or `consumer_fenced`. WC-11's only test is AC-3.4 for `/sc:save`.
- **A7 - Evidence-strength.** E3 (line 23) cites `invocation_method: "skill-direct"` as support, while 1.4 (1) (line 43) says the same run proves "the nested route, not the direct route". Both texts stand; E3's wording overstates what 1.4 admits (Wiegers). The statement in the 1.2 E5 row of a grep run is UNVERIFIED.
- **A8 - 3.2 `research` pins `--strategy planning` (line 116).** If the brief passes another strategy, the pin silently overrides it; whether an explicit flag wins is not stated.
- **A9 - D5 (b) wording.** "break R1's protection against runaway fan-out" (line 252): R1 is a rejection reason (line 33), not a protection.

## Notes (minor, no action needed)

- The title line cites "Task: task_1376c0449d24" (line 3), a coordinator-internal id with no meaning in the repo.
- `INV-B` numbering has UNVERIFIED item 10 placed before 7-9 (INV-B:320); the spec cites it as `INV-B:320` correctly.
- Sections 1.4 and "UNVERIFIED items" are candid and consistent with CAPS:176-188 (checked item by item: spec items 3, 4, 5, 10, 11, 13 map to CAPS:178, 186, 180, 177, 188, and CAPS:149/151).
- Pipeline Dimensional Analysis (FR-17): the document has no count-changing data pipeline; the one count flow (43 commands into 10/27/6 and the per-phase lists) conserves, which I checked. No Quantity Flow Diagram is required.

## Guard Condition Boundary Table

Guards found: the status-to-outcome mapping (WC-5), the wait-size rule (WC-10), the ask timeout (WC-3), the resume-or-fresh-dir rule (WC-6), the `--unattended` switch (D1/WC-2). Classes left out: "Maximum/Overflow" for WC-5 (a four-value enum has no capacity); "One/Minimal" for D1 (a boolean flag).

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|---|---|---|---|---|---|---|
| WC-5 outcome map | line 63 | Zero/Empty | no report file | failed | `--outcome failed` | OK |
| WC-5 outcome map | line 63 | Typical | `status: succeeded` | succeeded | `--outcome succeeded` | OK |
| WC-5 outcome map | line 63 | Sentinel Value Match | `status: partial` | succeeded | maps to succeeded; trigger for `partial` per command not stated (W5) | GAP |
| WC-5 outcome map | line 63 | Legitimate Edge Case | file exists but is not valid YAML or `status` outside the four values | unspecified | not stated | GAP |
| WC-10 wait split | line 68 | Zero/Empty | wait of 0 s | n/a | not stated (no polling needed) | OK |
| WC-10 wait split | line 68 | Typical | wait of 3 min | true | allowed | OK |
| WC-10 wait split | line 68 | Legitimate Edge Case | wait of exactly 4 to 5 min | unspecified | rule says "at most 4 minutes" for splitting; margin for tool overhead not stated (A4) | GAP |
| WC-3 ask | line 61 | Maximum/Overflow | repeated `ask` timeouts | resume same id | no cap, no escalation (A3) | GAP |
| WC-6 resume/fresh dir | line 64 | Zero/Empty | resume flag given, no on-disk state | unspecified | not stated | GAP |
| WC-6 resume/fresh dir | line 64 | Typical | retry via `--retry-of` | fresh dir | who supplies it is not stated (W3) | GAP |
| `--unattended` switch | D1, line 228 | Sentinel Value Match | literal `--unattended` inside quoted content | unspecified | not stated (W7) | GAP |
| `--unattended` switch | WC-2, line 60 | Legitimate Edge Case | gate resolves "refused" | unspecified | status and contract not stated (W4) | GAP |

GAP rows are graded by consequence under FR-8/FR-9: each is a requirement the document never states, not a stated text that causes a wrong build, so all are Medium and listed above (W3, W4, W5, W7, A3, A4). None is blocking.

## Open blocking findings

| id | grade | one-line wrong outcome | status |
|---|---|---|---|
| F1 | CRITICAL | P1 acceptance test requires an `## Unattended mode` section for commands the spec elsewhere says get no contract, no change, or an undecided change | open |
| F2 | MAJOR (blocking by the grading check) | AC-C5 passes a diff that deletes bullet lines, so "additive edits" is unenforced | open |

## Follow-up candidates

Medium: W1, W2, W3, W4, W5, W6, W7, W8, W9, A1, A2, A3, A4, A5, A6. Minor: A7, A8, A9, and the notes above. Under the command's Review Loop (bullet 3) the session that ran the review asks the user once per loop whether to open an issue for them. This run had no user to ask, so it opened none and records the list for the coordinator.

## Reviser brief

Applies only to blocking finding ids F1 and F2. Rules (Review Loop bullet 6, restated; the reviser reads this report, not the command):
- Revise only text a blocking finding names.
- Add no rule, mechanism or section that no blocking finding calls for.
- Each added paragraph or table cites its finding id.
- Prefer deleting or narrowing to adding. Report the byte size of the candidate before and after, and the bytes added and deleted per finding id.
- Leave Medium and minor findings alone (W1-W9, A1-A9). A brief cannot make them blocking or authorize editing them.

Findings (copied from this report; the VERIFY step gets only these):
- F1: Texts: AC-1.1 (candidate line 195) "every command in sections 3.1-3.2 has a `## Unattended mode` section naming `return-contract.yaml`"; P1 row (line 159) "the `--unattended` flag accepted by every command in sections 3.1 and 3.2"; `/sc:load` row (line 112) report "none (see note)", "not as its own Task"; Decisions row (line 265) "a report file would be an unrequested addition. Only its usage-line defect is fixed."; 3.1 intro (line 79) "The only command changes are the small fixes in the last column" with brainstorm and init-lite "None" (lines 84, 87); line 154 "Phases 1-3 need no user decision; Phase 4 waits for answers to D2-D4" with implement, post-release, pr-submit in P4 (lines 109, 113, 114) and D3 (a) "no pr-submit changes in Phase 4" (line 240). Stated wrong outcome: an implementer builds, in P1, contract-naming Unattended mode sections for load, brainstorm, init-lite and the P4 commands, which the document says get no report file, no change, or an undecided change, so AC-1.1 cannot pass without a contradicted edit.
- F2: Text: AC-C5 (line 176) `git diff -U0 master...HEAD -- src/superclaude/commands/<name>.md | grep -E '^-[^-]'`, pass condition "prints nothing: edits are additive". Stated wrong outcome: the regex skips removed lines that begin with `-`, so a deleted markdown bullet (`-- ...` in the diff) does not print, and the gate passes a non-additive edit.

verdict: FAIL

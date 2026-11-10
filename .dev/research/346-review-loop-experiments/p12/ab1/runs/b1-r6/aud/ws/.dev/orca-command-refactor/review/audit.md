review: 1 of 3

# Spec-panel audit: orca-worker-contract-spec.md (first review, whole document)

| Header field | Value |
|---|---|
| Command | `/sc:spec-panel @.dev/orca-command-refactor/specs/orca-worker-contract-spec.md --mode critique --focus requirements,architecture` |
| Candidate | `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md` (285 lines) |
| Candidate sha256 | `06730fb96147b55377f384ee4605e4ba1f6a74c60f4f348ab9d5de3b86c1559f` |
| Baseline sha256 | none: no `--baseline` or `--re-review` given, so this is a first review of the full document (command.md:258) |
| Reviewer model actually used | claude-sonnet-5-5 |
| Brief | Labelled whole-document audit, FIRST-REVIEW prompt (`~/.claude/rules/prompts/document_review_loop_prompts.md:27-32`, read in full) |
| Brief clauses overridden | none (command.md:264) |
| Citation convention | `spec:N` = line N of the candidate. `INV-A:N`, `INV-B:N`, `CAPS:N` = lines of `inventory/commands-a.md`, `commands-b.md`, `orca-capabilities.md`. `README:N` = `.dev/orca-command-refactor/README.md`. `command.md:N` = the command definition this review runs under. |

## Coverage

- Read in full: README, the candidate, all three inventory files, command.md, and the review-loop prompts file.
- Panel: Wiegers (lead), Adzic, Cockburn (requirements focus); Fowler (lead), Newman, Hohpe, Nygard (architecture focus); Whittaker (active in every panel, command.md:83). Crispin, Gregory and Hightower are outside the requested focus and did not review.
- Checked: internal consistency of the candidate (counts, phase assignments, WC/SA/AC cross-references), and every `INV-*:N` and `CAPS:N` citation the candidate makes against the inventory files. All inventory line citations I spot-checked land on the cited row or note, including the counts 10 + 27 + 6 = 43 (INV-A:73, INV-B:278, spec:76, and the row counts in spec:83-92, 99-125, 132-137).
- Not checkable (UNVERIFIED): every `src/...`, `CLAUDE.md:N`, `Makefile`, `pyproject.toml` and `EVIDENCE.md` line the candidate cites directly (for example spec:25, 52, 150, 183), because the workspace holds no source tree and no `EVIDENCE.md`. These are accepted only as carried by the inventories. I did not run any live Orca command (none exists in this sandbox).
- Mandatory artifacts produced: Guard Condition Boundary Table (guards exist, so it is triggered, command.md:313) and a Quantity Flow Diagram (one count-divergence point found). State Variable Registry is not produced: `--focus correctness` was not requested (command.md:186).
- Improve step: not run. Critique mode with `--re-review` absent and no `--improve` passed; this audit edits nothing but this file.

## Verdict summary

No blocking finding. Fifteen Medium findings (F-01 to F-06, F-10 to F-18) and three minor notes (F-07 to F-09) plus three nits. Each Medium finding failed the grading check below because it needs a guess that the implementer picks the worse of two readings, or it is a requirement the document never states.

Grading rule applied (command.md:259; prompts file:31): a finding is blocking only if I can write "An implementer who follows the stated text as written builds X, and X is wrong because Y" with no further assumption. Severity labels below (CRITICAL/MAJOR/MINOR) are the panel's raw labels; the grade decides.

=== REQUIREMENTS ANALYSIS ===

### F-01 (Wiegers, with Whittaker Zero/Empty and Sequence attacks): outcome mapping accepts an empty, invalid or stale contract
- Raw label: MAJOR. Grade: Medium.
- Issue: WC-5 maps `--outcome failed` only when the report says `failed` or `blocked`, "or no report exists", and `succeeded` "otherwise" (spec:63). WC-4 says the contract is written "on every outcome" (spec:62), but nothing says what the worker does with a file that exists and is empty, unparseable, or has a `status` outside the four-value set (spec:62, 262). WC-6 lets 17 commands "resume" or re-run into a "fresh dir" (spec:64, resume column in spec:99-125), yet the report directory is fixed in the brief before dispatch (spec:62, 73).
- Whittaker: I can break this specification by **Sequence attack**. The invariant at **spec:63 (WC-5) with spec:62 and spec:64** fails when **a retry or resumed run reuses the same `--report-dir` and crashes before it rewrites the contract**. Concrete attack: attempt 1 writes `status: partial` (before: no file; after: `partial`); attempt 2 is started with `--retry-of` and the same brief, which carries the same `--report-dir` (spec:73), and dies on context exhaustion before writing; the worker finds a report, which is not "no report exists", and sends `--outcome succeeded` for a run that never finished.
- Whittaker: I can break this specification by **Zero/Empty attack**. The invariant at **spec:63** fails when **the contract is a 0-byte file or invalid YAML**. Concrete attack: a command opens `return-contract.yaml` for write, is killed, leaves 0 bytes; the "otherwise" branch yields `succeeded`.
- Why Medium: the implementer needs to assume a crash mid-write or a retry into the same directory; the text does not state either case.
- Recommendation: state that the worker validates the file (non-empty, parseable, `status` in the set) and that a missing or invalid contract maps to `failed`; state who supplies a new `--report-dir` on a retry (WC-6 says "fresh output directory" but the path is fixed before dispatch). Narrowing rule: add one sentence to WC-5 and one to WC-6, no new mechanism.
- Priority: Medium. Quality impact: Testability and Consistency, about 1 point.

### F-02 (Wiegers): several requirements have no acceptance check
- Raw label: MAJOR. Grade: Medium (a requirement the document states but never tests).
- Issue: section 7.3 holds AC-0.1 to AC-4.3 (spec:191-210). No check exercises WC-3 (ask, resume by message ID, spec:61), WC-6 (retry or safe re-run, spec:64), WC-12 (`check` and `consumer_fenced`, spec:70) or WC-1 (no prompt before ready, spec:59). WC-10 is exercised only for pr-submit (AC-4.3, spec:210), although cli-eval carries the same wait-splitting change in P2 (spec:104, 160) and AC-2.x contains no wait check (spec:199-203). WC-9 is exercised for auggie-review and post-release (AC-2.4, AC-4.2, spec:202, 209) but not for `task` commit/push, which spec:121 and D4 (spec:244) both name.
- Recommendation: add one check each, or mark the requirement as "by construction, not tested". Priority: Medium. Quality impact: Testability, about 1 point.

### F-03 (Wiegers): `--unattended` and `--report-dir` rules leave edge inputs undefined
- Raw label: MAJOR. Grade: Medium (missing restriction, never stated).
- Issue: (a) WC-4 says every unattended command accepts `--report-dir` (spec:62) but never says what happens when `--unattended` is passed without it, although the whole mechanism (known path, spec:62, 73) depends on it. The definition this review runs under refuses such a run before any work and prints the refusal in chat only (command.md:460). (b) No text restricts where `--report-dir` may point. The same definition refuses a directory inside `.git/`, `.codegraph/`, or the distributable folders under `.claude/` (command.md:460); the candidate has no equivalent, while its own repo rules make `.claude/` sync-dev output (spec:150, AC-C4 spec:175).
- Recommendation: add the missing-flag outcome (refuse, or `blocked`) and a one-line path restriction to WC-4 or to the contract file text. Priority: Medium. Quality impact: Completeness, about 1 point.

### F-04 (Wiegers, Adzic): the brief rule contradicts the "ready today" rows and two ready commands are in no phase
- Raw label: MAJOR. Grade: Medium (two readings; the worse one builds a wrong brief template).
- Issue: section 2.3 says every brief states "the exact command line including `--unattended`" (spec:73). Section 3.1 says the ten ready commands "run as workers now if the brief uses the stated flags" and its "Brief must pass" column never lists `--unattended` (spec:79-92); AC-0.4 runs three of them without it (spec:194). P0 writes a brief template "listing the section 3.1 flags" (spec:158). `--unattended` reaches reflect, release-split, tdd and troubleshoot only in P2 (spec:160), and `brainstorm` and `init-lite` ("None" in spec:84, 87) appear in no phase list (spec:158-162), so they never gain `--unattended`, `--report-dir` or a WC-4 contract, although AC-1.1 asserts a `## Unattended mode` section for "every command named in the P1 row" (spec:195), and the P1 row names the fix targets adversarial, cleanup-audit, index-repo and workflow (spec:159).
- Why Medium: the implementer must pick between the 2.3 reading (template always adds `--unattended`; on a command without the flag the text is treated as unknown or, for tdd, as part of the free-text prompt, spec:90) and the 3.1 reading (flags as listed).
- Recommendation: make 2.3 conditional ("once the command's phase has landed") and state brainstorm and init-lite's end state (accept `--unattended` as a no-op, or stay flag-free and be briefed by their existing report file). Priority: Medium. Quality impact: Consistency, about 1 point.

### F-05 (Cockburn): a "needs change" command cannot reach success after its change, with no decision recorded
- Raw label: MAJOR. Grade: Medium (design choice acknowledged, but the user goal is unserved and unasked).
- Issue: for cli-portify "no flag carries an approval, so an unattended run ends blocked at the first gate (M3)" (spec:105) and AC-2.3 accepts `blocked` as the pass (spec:201). WC-3 resumes "with the answer as a flag" (spec:61), which cannot work when no flag carries the answer. Section 9 lists five decisions (spec:225) and none covers how approvals are supplied. The coordinator's goal (run the command as a unit of work, spec:16) is not met for this command under any listed phase.
- Recommendation: add a decision (for example an explicit `--approve-phases` input versus "cli-portify stays person-run") or move cli-portify to section 4. Priority: Medium. Quality impact: Completeness, about 0.5 point.

### F-06 (Cockburn, Wiegers): WC-9 authorizes outward actions through a flag that does not exist for some commands
- Raw label: MAJOR. Grade: Medium.
- Issue: WC-9 says an outward default turns on "only through the command's own explicit flag written in the brief" (spec:67); D4 repeats it and names task commit/push and auggie-review `--post-pr` (spec:244-245). The task inventory shows commit and push are EXEMPT keywords in the task text, not a flag (INV-B:204; spec:121 says "refused unless authorized"), and the auggie-review inventory documents only `--no-post-pr` (INV-A:38), so `--post-pr` as a positive flag is not shown to exist, while the 3.2 row lists "none" under other required change (spec:100). The authorization route the rule demands is therefore undefined for these commands. Source-file confirmation is UNVERIFIED here.
- Recommendation: either name the new flag in the row ("Other required change") or state a different authorization route for task. Priority: Medium. Quality impact: Clarity, about 0.5 point.

### F-07 (Adzic): no concrete example of the central artifacts, and six undefined labels
- Raw label: MINOR. Grade: minor note.
- Issue: the spec gives field names for the contract (spec:62) but no sample file, and no sample brief; the brief template is deferred to P0 (spec:158). Labels M1 to M6 are cited at spec:62, 76, 105, 159, 194-196 and 201 and are defined nowhere in the document, so a reader cannot resolve them (the sentences around them are readable alone).
- Recommendation: add one 10-line sample contract and delete or define the labels. Priority: Low.

### F-08 (Wiegers): completeness of "43 commands" is asserted, not shown; one statement about spec-panel is inconsistent
- Raw label: MINOR. Grade: minor note.
- Issue: spec:76 says "the 43 commands in `cmd/`" (21 + 22); the scope lines at INV-A:3 and INV-B:3 are hand-written lists, and the workspace has no directory listing, so that the lists equal the full folder is UNVERIFIED. Separately, WC-4 says "no inventory file covers" the spec-panel definition (spec:62) although INV-B:43 and INV-B:177-185 are exactly that row, and the 3.2 row says "add `--output`" (spec:120) while the definition used for this review already has `--output`, `--report-dir`, `--unattended` and an Unattended mode section (command.md:22-23, 455-465). If the candidate predates that edit, the row is stale.
- Recommendation: re-count against a directory listing; reword the WC-4 parenthesis. Priority: Low.

### F-09 (Wiegers): P1 rationale conflicts with its own rows
- Raw label: MINOR. Grade: minor note.
- Issue: P1 is justified by "No person gate is involved" (spec:159), but its commands business-panel, explain, index and test have gate-resolution entries in 3.2 (spec:102, 108, 111, 123), and the index entry asks the command text to state that its knowledge-base mode does not wait while the inventory records that as UNVERIFIED (INV-A:54, INV-A:113). Also "Phases 1-3 need no user decision" (spec:154) sits beside D4 naming P2 commands (spec:244).
- Priority: Low.

=== ARCHITECTURE ANALYSIS ===

### F-10 (Nygard): the claim that a prompt at command start does not fail `worker-start` is stated as fact on unsupported evidence
- Raw label: MAJOR. Grade: Medium (stated with a hedge elsewhere; harm needs an assumption about Orca internals).
- Issue: section 1.4 item 2 says a command's own `AskUserQuestion` "comes after readiness, so it does not fail `worker-start`" (spec:44). The cited lines (CAPS:52, CAPS:129) cover a worker already past `input_accepted`. The same inventory says that for Claude the task is passed on the command line (CAPS:47), so the command begins executing at launch; whether Orca's readiness wait can complete when the first action is a prompt is not shown. The only readiness failure evidence is a wrapper prompt before Claude started (CAPS:49). WC-1 then assigns the failure class to "Launch setup, not commands" (spec:59).
- Why it matters: the under-test commands whose first step could prompt are already forced unattended by WC-2, so the consequence is limited to a person-style run dispatched without `--unattended` (for example before a command's phase lands, F-04).
- Recommendation: mark the claim UNVERIFIED and add the argv-injection question to the UNVERIFIED list (spec:272-285); AC-0.4 can test it with one prompting command. Priority: Medium. Quality impact: Correctness of the rationale, about 0.5 point.

### F-11 (Fowler): two canonical contract locations for the commands that already write one
- Raw label: MAJOR. Grade: Medium.
- Issue: WC-4 puts the contract at `<report-dir>/return-contract.yaml` (spec:62). Section 3.1 lists the existing contract at `<output>/return-contract.yaml` (brainstorm, reflect, spec:84, 88), `<output>/adversarial/return-contract.yaml` after a P1 fix (adversarial, spec:83) and `.dev/tasks/to-do/<id>/return-contract.yaml` (workflow, spec:92). AC-1.4 checks that adversarial "names one fixed path" (spec:198) while AC-1.2 and 7.2 step 3 require the reported path to be the WC-4 path (spec:182, 196). Whether an unattended run writes both, or moves the contract, is not stated, and SA-3 requires standalone runs to stay as today (spec:148).
- Recommendation: one sentence: "in unattended mode the contract is written to `--report-dir`; an existing standalone location is unchanged and may be written in addition". Priority: Medium. Quality impact: Consistency, about 1 point.

### F-12 (Newman): the contract has no version field and "keep their fields" can conflict with the fixed `status` set
- Raw label: MAJOR. Grade: Medium.
- Issue: WC-4 lists the minimum fields (spec:62) with no `contract_version`, although the existing workflow contract is versioned ("contract 1.1", INV-B:272) and the coordinator parses these files across phases P1 to P4. WC-4 also says commands that already write a contract "keep their fields", while the decision table fixes `status` to `succeeded|partial|failed|blocked` (spec:62, 262) and AC step 4 asserts it (spec:183). Whether any existing contract uses another vocabulary is not shown in the inventories (UNVERIFIED), so the two rules may collide for the same key.
- Recommendation: add a version field to the minimum set and state which rule wins for `status`. Priority: Medium. Quality impact: Completeness, about 0.5 point.

### F-13 (Nygard, Whittaker Divergence attack): WC-10 and AC-4.3 draw the line at different values, and the heartbeat bound is not preserved
- Raw label: MAJOR. Grade: Medium.
- Whittaker: I can break this specification by **Divergence attack**. The invariant at **spec:68 (WC-10) against spec:210 (AC-4.3) and spec:114** fails when **a single blocking call lasts between 240 s and 300 s**. Concrete attack: a poll step blocks 270 s; WC-10 requires splitting only above 5 minutes, so it is compliant; AC-4.3 requires "no single tool call exceeds 240 s", so the phase check fails; and if the call starts 90 s after the last heartbeat the gap reaches 360 s, over the 5-minute cadence WC-10 exists to keep (spec:68, CAPS:130).
- Why Medium: the implementer is likely to read "waits of at most 4 minutes" (spec:68, 114) as the operative rule; the harm of a missed heartbeat is low, since absence never authorizes stop or release (CAPS:125). Also the 5-minute cadence is taken from one worker's preamble (CAPS:130), not a guide.
- Recommendation: state the single rule once ("no tool call longer than 4 minutes") and have WC-10 and AC-4.3 use it. Priority: Medium. Quality impact: Consistency, about 0.5 point.

### F-14 (Nygard, Whittaker Accumulation attack): WC-11 is universal but the rows leave several shared writes unmanaged
- Raw label: MAJOR. Grade: Medium.
- Issue: WC-11 says two workers in one worktree "must never write the same file" and that default output paths carry a timestamp or slug (spec:69). The rows then leave these shared writes: index-repo writes a fixed `PROJECT_INDEX.md` and the row only "states the output location" (spec:86, INV-A:53); cleanup-audit's fixed output directory is accepted with "one audit per worktree" (spec:85); `validate-roadmap` writes fail-open memory under `.superclaude/memory/validate-roadmap/` (INV-B:253) with no change (spec:124); `recommend` writes cache rows under `.claude/cache/` (INV-B:102, spec:115 "n/a"); reflect writes the tracked `docs/memory/reflect/deviation-patterns-<slug>.md` (INV-B:114, spec:88). Source lines are carried from the inventories (UNVERIFIED here).
- Recommendation: add a "shared writes" column or a single exception list in WC-11. Priority: Medium. Quality impact: Completeness, about 0.5 point.

### F-15 (Fowler, Hohpe): tasklist's nested reflect fan-out is called safe without evidence
- Raw label: MAJOR. Grade: Medium.
- Issue: the tasklist row says its reflect fan-out "runs one layer below the worker, inside Claude Code's nesting limit, INV-A:14" (spec:122). The inventory that holds the tasklist analysis marks nested spawning as UNVERIFIED and notes that the tdd skill avoids subagent-to-agent nesting (INV-B:210, 314). Reflect Tier 2 calls adversarial, which fans out further (INV-B:111), so the count of layers is two or three, not one; INV-A:14 states only the documented limit of three layers and the loss of the Agent tool at that depth. The row also sets `--unattended` to engage reflect's headless auto-accept rule (spec:122) while the spec's own UNVERIFIED item 9 says an Orca worker is assumed not to be headless (spec:280).
- Recommendation: replace "inside the limit" with "UNVERIFIED, tested at P2 by AC-2.3" and say which layer count was assumed. Priority: Medium.

### F-16 (Fowler): AC-C1 can fail the very text P0 and SA-2 allow
- Raw label: MAJOR. Grade: Medium (the text can be written to pass, but the three statements together do not guarantee it).
- Issue: SA-2 allows one Orca mention, "as an example of a caller's question channel inside the contract file" (spec:147). P0 adds the contract file and "an Orca section" to `HOW-WE-WORK.md`, both under `src/superclaude/core/` (spec:52, 158, 150), and E5 records the baseline of zero Orca mentions in that file (spec:25). AC-C1 is a common check for every phase including P0 and greps `src/superclaude/core` for `orca[-ide] (orchestration|worktree|terminal|agent)` with an exemption only for `ccsession-tag` (spec:172). Any sentence in the new core text such as "orca orchestration ask" or a coordinator example using `orca-ide orchestration` makes AC-C1 fail; the spec gives no exemption path.
- Recommendation: exempt the two new core files in AC-C1, or state that they must avoid those four phrases. Priority: Medium.

### F-17 (Newman): the plugin copy of every edited command has no rule and no check
- Raw label: MAJOR. Grade: Medium (stated as UNVERIFIED, deferred to each phase plan, not tested).
- Issue: UNVERIFIED item 8 says the update rule for `plugins/superclaude/commands/` was not read and "Each phase's plan must resolve this before editing" (spec:279). The 7.1 common checks (spec:172-176) include no check that the plugin copies agree with `src/`, although P1 to P4 edit about 37 command files.
- Recommendation: add a common check once the rule is known. Priority: Medium.

### F-18 (Nygard): unattended mode limits outward actions but not local destructive ones
- Raw label: MAJOR. Grade: Medium.
- Issue: WC-9 covers push, PR, GitHub, install, provision and paid runs (spec:67). The rows leave default-on local mutations in a worktree that workers share by default (CAPS:115, spec:69): cleanup and improve apply edits while their rollback mechanism is UNVERIFIED and the row only requires a changed-file list (spec:103, 110, INV-A:118); reflect's default folder move is avoided only if the brief passes `--no-promote` (spec:88, INV-B:114). Nothing states that unattended mode requires a clean tree or a snapshot before such edits.
- Recommendation: add a one-line precondition (clean tree or recorded start SHA) to the cleanup, improve and reflect rows. Priority: Medium.

=== ADVERSARIAL ANALYSIS (summary of Whittaker's findings) ===

| Attack | Finding | Location |
|---|---|---|
| Zero/Empty | F-01 empty or invalid contract maps to `succeeded` | spec:63 |
| Sequence | F-01 stale contract on retry into the same directory | spec:62-64, 73 |
| Divergence | F-13 WC-10 5 min trigger vs AC-4.3 240 s | spec:68, 210 |
| Accumulation | F-14 shared writes beyond `save` | spec:69, 86, 124 |
| Sentinel Collision | `status: partial` is a sentinel the worker folds into `succeeded` (spec:63, 263); the first sentence of the body carries the real status, which is acceptable; no defect found | spec:63, 263 |

## Guard Condition Boundary Table

Guards identified in the candidate: G1 wait-splitting threshold (spec:68), G2 outcome mapping (spec:63), G3 `--unattended` token and report directory (spec:51, 62), G4 readiness limit (spec:59), G5 nested depth (spec:33, 66), G6 confidence threshold (spec:121). Classes left out are listed with a one-line reason after the table. Construction: Nygard; completeness: every cell checked by the panel (Crispin did not sit); attack on entries: Whittaker.

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|-------|----------|-----------------|----------------|--------------|-------------------|--------|
| G1 split waits above 5 min | spec:68 | Zero/Empty | wait of 0 s | false | none needed, returns at once | OK |
| G1 | spec:68 | Typical | single wait of 12 min | true | split into waits of at most 4 min, heartbeat between | OK |
| G1 | spec:68, 210 | Legitimate Edge Case | single wait of 270 s | false | WC-10 allows it; AC-4.3 fails it at 240 s; heartbeat gap can exceed 5 min | GAP (F-13) |
| G1 | spec:104 | Maximum/Overflow | cli-eval timeout 3600 s | true | 15 waits of at most 4 min | OK (no AC, F-02) |
| G2 outcome mapping | spec:63 | Zero/Empty | contract file of 0 bytes | false for "no report exists" | falls to "otherwise", `succeeded` | GAP (F-01) |
| G2 | spec:63 | One/Minimal | contract with only `status: failed` | true | `--outcome failed` | OK |
| G2 | spec:63, 263 | Typical | `status: partial` | false | `--outcome succeeded`, body states `partial` | OK |
| G2 | spec:62-64 | Sentinel Value Match | stale `status: partial` left by attempt 1, attempt 2 crashed | false | `succeeded`; unstated | GAP (F-01) |
| G2 | spec:62, 262 | Legitimate Edge Case | existing contract using a different status word | unspecified | "keep their fields" vs fixed set | GAP (F-12) |
| G3 `--unattended` token | spec:51, 62 | Zero/Empty | `--unattended` without `--report-dir` | unspecified | undefined | GAP (F-03) |
| G3 | spec:62 | Legitimate Edge Case | `--report-dir` inside `.git/` or `.claude/skills/` | unspecified | no restriction stated | GAP (F-03) |
| G3 | spec:73 | Typical | token plus directory plus flags | true | contract written to the directory | OK |
| G4 readiness limit 60 s | spec:59 | Typical | wrapper fallback 30 s | passes | start succeeds (EVIDENCE as carried at CAPS:49) | OK |
| G4 | spec:59 | Maximum/Overflow | fallback above about 45 s | fails | "well inside the limit", no number | GAP (minor: state 30 s as the ceiling) |
| G4 | spec:44 | Legitimate Edge Case | command prompts at launch (argv task, CAPS:47) | unknown | asserted not to fail | GAP (F-10) |
| G5 nested depth 1 | spec:33, 66 | Typical | worker calls `worker-start` | true | refused `nested_worker_depth_exceeded` | OK |
| G5 | spec:252 | Legitimate Edge Case | depth raised by the user (D5 b) | false | WC-8 still forbids, text unconditional | OK |
| G6 confidence below 0.70 | spec:121 | Sentinel Value Match | exactly 0.70 | false | proceeds (INV-B:199 uses "< 0.70") | OK |
| G6 | spec:121 | Zero/Empty | confidence 0 or unavailable | true | blocked | OK |

Classes left out: G1 One/Minimal (a 1 s wait behaves as Zero/Empty); G4 Zero/Empty (a 0 ms timeout is rejected by Orca as non-positive, CAPS:44); G5 Zero/Empty (depth below 1 is replaced by the default 1, CAPS:100); G6 Maximum (a score above 1.0 is outside the scale, so not a legitimate input).

FR-8 and FR-9 findings from this table: the GAP rows are F-01, F-03, F-10, F-12 and F-13, all graded Medium above, plus the minor G4 numeric-ceiling gap (none names a concrete wrong outcome without an extra assumption, and none is a security, data-loss or safety-boundary risk on the stated text). Table complete; synthesis was not blocked (FR-10).

## Pipeline dimensional analysis and Quantity Flow Diagram

Trigger (FR-17): the worker lifecycle is a multi-stage flow whose counts diverge on retry. Pipeline: Tasks, Dispatches, `worker_done` messages, contract files, coordinator reads. The raw FR-19 label for a count mismatch is CRITICAL; by the grading rule (command.md:259) it is graded by consequence, which gives Medium here because the mismatch needs a crash or retry the text does not state (see F-01).

```text
[Coordinator: K Tasks] --> [Stage 1: worker-start, one Dispatch per Task, retries add Dispatches (breaker at 3 failed starts, CAPS:80)]
                              | K .. K + R dispatches (R >= 0)
                              v
                        [Stage 2: command run, one contract written to the fixed --report-dir per Task (spec:62, 73)]
                              | K contract paths known, but up to K + R writers into them   <-- DIVERGENCE (N != M)
                              v
                        [Stage 3: worker_done, exactly once per accepted Dispatch (CAPS:73)]
                              v
                        [Consumer: coordinator opens one contract per Task]
                              assumes one writer per path    <-- MISMATCH on retry (F-01)
```

## Follow-up candidates (Medium and minor; none triggers a revision)

Medium (fifteen): F-01, F-02, F-03, F-04, F-05, F-06, F-10, F-11, F-12, F-13, F-14, F-15, F-16, F-17, F-18.
Minor notes: F-07, F-08, F-09, and three nits: spec:285 places a verification record (item 14) in the UNVERIFIED list; the "approximately 340 citations" re-check it records cannot be checked here; AC-2.4 counts reviews and comments with `--jq length` on a paginated API (`gh api` default page size can undercount over 30 items).

Issue offer: this audit ran as a worker with a fixed reply format and no user to ask, so the once-per-loop question about opening an issue for these items was not asked and no issue was created (command.md:260).

## Reviser brief

No blocking finding is open, so there are no finding ids to revise. If a later review finds one, the reviser works under these rules (command.md:263): revise only text a blocking finding names; add no rule, mechanism or section that no blocking finding calls for; cite the finding id on every added paragraph or table; prefer deleting or narrowing to adding; report the byte size before and after, and the bytes added and deleted per finding id. Medium and minor findings, including every F-id above, stay untouched and never appear in a Reviser brief.

verdict: PASS

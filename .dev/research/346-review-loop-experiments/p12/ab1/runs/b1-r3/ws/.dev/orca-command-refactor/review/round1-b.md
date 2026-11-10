review: 1 of 3

# Spec panel review, round 1: Orca worker contract spec

## Header
- command: `/sc:spec-panel @.dev/orca-command-refactor/specs/orca-worker-contract-spec.md --mode critique --focus requirements,architecture`
- candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`, sha256 `d3cdbe573e57303b9ce6c93d1fe98ba18fb7cb1a15773d926bf6a0c31425200d`
- baseline: not given (first review; no `--re-review`, no `--baseline`)
- reviewer model actually used: claude-sonnet-5-5
- role: this file is ONE first-review report. The FIRST-REVIEW prompt asks the coordinator for three fresh-context first reviews and a MERGE (`~/.claude/rules/prompts/document_review_loop_prompts.md:35`). This worker ran one review and did not merge. Finding ids below are report-local (`F1`...); the coordinator renames them `M1`... at merge.
- `--unattended` not passed: the follow-up question to the user is left to the coordinating session; the list is recorded under `follow-up candidates`.

## Citation keys and evidence limits
- `SPEC:N` = line N of the candidate. `INV-A:N`, `INV-B:N`, `CAPS:N` = line N of `.dev/orca-command-refactor/inventory/commands-a.md`, `commands-b.md`, `orca-capabilities.md`. `README:N` = `.dev/orca-command-refactor/README.md`.
- Checkable in this sandbox: the candidate, the three inventories, README. I opened every `INV-*` and `CAPS:*` line the candidate cites in sections 1 and 2 and the spot-checked rows of section 3 and found them as cited (INV-A rows 35-55, INV-B rows 31-52, INV-A:60-62,65-68,90-92,94-98,106,113,118,120, INV-B:272,285-287,289-299,311,320,323, CAPS:44-52,58-67,72-80,84-92,97-103,107-116,128-130,135-139,145-151,155-161,178-188).
- UNVERIFIED (not inside the workspace): every `src/superclaude/...` line, `.dev/evals/.../EVIDENCE.md`, `.dev/codegraph-migration/...`, `CLAUDE.md:N`, `pyproject.toml:38`, `Makefile:68-74`, and the grep outputs behind E5 (`SPEC:25`). Where this review relies on such text it relies on the inventory line that quotes it, and says so.
- SPEC:285 (item 14, "a fresh evidence-validator re-read about 340 citations") is a process claim; UNVERIFIED.

## Coverage
Read in full: candidate (285 lines), README, `orca-capabilities.md`, the table, notes and summaries of `commands-a.md` and `commands-b.md`. Experts applied in panel order for the two focuses: Wiegers, Adzic, Cockburn (requirements); Fowler, Nygard, Whittaker (always active), Newman, Hohpe, Crispin (boundary-table completeness). Not covered: the `src/` text behind the section 3 rows (not in the workspace), the Orca binary behaviour, and any command outside the 43. `--focus correctness` was not requested, so no State Variable Registry is produced.

## Grading rule applied
Per `Review Loop` bullet 2 and the FIRST-REVIEW grading check: a finding is blocking only if a sentence "An implementer who follows the stated text as written builds X, and X is wrong because Y" holds with no further assumption (two stated texts that contradict, data loss or a safety boundary, or an acceptance criterion that cannot pass). Findings that rest on a requirement the spec never states, or on a guess between two readings, are Medium and go under `follow-up candidates` whatever their label.

---

=== REQUIREMENTS ANALYSIS ===

### F1 - BLOCKING - `/sc:load` cannot satisfy both AC-1.1 and its own row
- Expert: Wiegers (traceability), Adzic (acceptance), Crispin (testability). Severity label: MAJOR, graded blocking by consequence. Priority High.
- Stated texts that contradict:
  - AC-1.1: the test "asserts that every command in sections 3.1-3.2 has a `## Unattended mode` section naming `return-contract.yaml` and `~/.claude/WORKER-CONTRACT.md`" (SPEC:195). `load` is a section 3.2 row (SPEC:112).
  - Section 3 intro: "Every changed command also gains the `## Unattended mode` section" (SPEC:76); `load` is changed (usage line, SPEC:112). P1 scope: the `--unattended` flag is "accepted by every command in sections 3.1 and 3.2" (SPEC:159).
  - The `load` row: Report (WC-4) = "none (see note)", "use it as a step inside another worker's brief, not as its own Task" (SPEC:112). The Decisions table: "a report file would be an unrequested addition. Only its usage-line defect is fixed" (SPEC:265). WC-4 itself says an unattended command "writes `<output-dir>/return-contract.yaml`" on every outcome (SPEC:62).
- Sentence: an implementer who follows AC-1.1 adds a `## Unattended mode` section to `load` that names `return-contract.yaml`, which creates the report file SPEC:265 forbids; an implementer who follows SPEC:112 and SPEC:265 leaves `load` without it, and AC-1.1 (a P1 gate, SPEC:154) cannot pass. Either way one stated text is violated, with no guess needed.
- Basis in the inventory: `load` writes no file and its only output is context in chat (INV-B:31, INV-B:65), so SPEC:112/265 are the better-supported side; AC-1.1 and SPEC:159 are what must narrow.
- Recommendation: exclude `load` by name from AC-1.1 and from the P1 flag scope (or state in the row that it gets a section that says "no report file; not dispatched as its own Task"). Narrow, do not add.

### F2 - BLOCKING - Two different contract paths for the same command (adversarial, workflow) against WC-4 and the live check
- Expert: Wiegers (consistency), Fowler (interface), Adzic (examples), Whittaker (divergence attack). Severity label: MAJOR, graded blocking by consequence. Priority High.
- Stated texts that contradict:
  - WC-4: the file is `<output-dir>/return-contract.yaml`, "where `<output-dir>` is the directory the coordinator passed", and "known before dispatch" (SPEC:62); the brief states the output directory "so the report path is known before dispatch" (SPEC:73).
  - Live check 7.2 step 3 passes only if "its report path is the WC-4 contract path" and step 4 runs `test -s <contract>` (SPEC:182-183); AC-1.2 applies that check to "each P1 command" with `--unattended --output <dir>` (SPEC:196). adversarial and workflow are P1 commands (SPEC:159).
  - adversarial row: the P1 fix makes the contract `<output>/adversarial/return-contract.yaml` (SPEC:83; AC-1.4 SPEC:198 "names one fixed path"). The inventory confirms the sub-directory is real: merged output and artifacts live under `<output>/adversarial/` (INV-A:35).
  - workflow row: the contract is `.dev/tasks/to-do/<id>/return-contract.yaml` (SPEC:92), the brief passes only `--handoff none`, and the `<id>` is created by the run (INV-B:272, INV-B:52 "never reuses a package"). No output directory is passed, so the path cannot be "known before dispatch".
- Sentence: an implementer who follows SPEC:83 and SPEC:92 builds commands whose contract is at `<dir>/adversarial/return-contract.yaml` and `.dev/tasks/to-do/<id>/return-contract.yaml`; the P1 live check (SPEC:182-183, SPEC:196) looks for `<dir>/return-contract.yaml` and the contract the coordinator is promised before dispatch (SPEC:62, SPEC:73), so the check cannot pass for these two commands and the coordinator cannot locate the file from its own brief.
- Recommendation: state the rule once. For example: the contract path is the one the section 3 row names, the brief records it, and WC-4 reads "the contract path named in the command's row". Delete the "known before dispatch" claim for workflow, or give workflow an output flag.

---

## follow-up candidates (Medium and minor; none triggers a revision)

### Medium

**F3 - Contract location is undefined for commands without a directory-valued output flag.** (Wiegers, Cockburn). WC-4 defines `<output-dir>` as "the directory the coordinator passed (`--output` / `--output-dir`)" (SPEC:62), but several rows pass a file or nothing: tdd `--output <file>` (SPEC:90), init-lite `--output <file>` (SPEC:87), cleanup-audit with a fixed `.claude-audit/` and no output flag (SPEC:85), index-repo "Brief must pass: none" (SPEC:86), reflect with a timestamped default dir (SPEC:88, INV-B:112), workflow pre-creation STOPs which the P1 fix says must also write a contract (SPEC:92) although no package directory exists yet (INV-B:272). With `--unattended` and no output directory the behaviour is unstated. A guess is needed for each, so Medium. Note for context: the `/sc:spec-panel` definition this worker acts on already resolves this differently from SPEC:120 ("add `--output`"): it uses `--report-dir` and refuses without it, because `--output` is file-valued (`command.md:460`). Whether that file is the post-change version of the same command is not established here.

**F4 - Stale report can set the outcome after a retry.** (Whittaker sequence attack; Nygard). WC-5 maps the report's `status` to `--outcome` (SPEC:63), the contract is written to a fixed path (SPEC:62), and WC-6 allows a retry (`--retry-of`) that reuses the command's resume flag or "a fresh output directory" (SPEC:64). Nothing says a run deletes or overwrites the contract at start, or that the contract carries a run or dispatch id. Attack: attempt 1 ends `succeeded` in `<dir>`; attempt 2 in the same brief dies before writing; the worker reads attempt 1's `succeeded`. Requirement missing, so Medium. Narrow fix: write `status: failed` (or remove the file) as the first action in unattended mode.

**F5 - WC-6 "fresh output directory" conflicts with WC-4's fixed `<output-dir>`.** (Fowler). Most of the 27 rows say "fresh dir" for resume (SPEC:99-125). If the command creates the fresh directory, the contract is no longer in the directory the coordinator passed; if the coordinator passes a new one per retry, WC-6 is a coordinator duty and 2.3 (SPEC:73) does not list it. Related: AC-3.2 runs `/sc:roadmap --unattended --output <dir>` where `<dir>/.session-memory.md` already exists and expects "starts fresh" (SPEC:205), which, read as overwriting in the same directory, is neither of WC-6's two options (SPEC:64). Needs a reading to be chosen, so Medium.

**F6 - WC-10 and AC-4.3 disagree in the 240-300 second band.** (Whittaker divergence attack; boundary table G2). WC-10 obliges splitting only for a step that blocks "for longer than 5 minutes", into waits of at most 4 minutes (SPEC:68); AC-4.3 fails any "single tool call" over 240 s (SPEC:210). A 270 s call needs no split under WC-10 and fails AC-4.3. Also the 5-minute heartbeat cadence is taken from one dispatch preamble (CAPS:130), not from a guide, and is stated as a general rule. No wrong outcome without a guess about which number governs: Medium. Fix by using one number.

**F7 - Requirements with no acceptance check.** (Crispin, Adzic). WC-1 has only the generic `state: ready` check (SPEC:180); WC-10 has a check only for pr-submit under D3 (SPEC:210), none for cli-eval's wait splitting (SPEC:104); WC-11 has a check only for `save` (SPEC:207); WC-12 (`check` before `worker_done`, stop on `consumer_fenced`) has none; WC-7 is checked only through the P0 transcript (SPEC:194). Also AC-0.4 says step 4 "uses the command's existing report file" (SPEC:194) but step 4 is a YAML assertion requiring a `command` key (SPEC:183): troubleshoot's `REPORT.md` is Markdown (SPEC:91, INV-B:49) and workflow's current contract fields are `status`, `plan_path`, `reflect_report_path` (INV-B:272), so step 4 as written fails for both in P0 unless "uses" means existence only.

**F8 - AC-C1 is narrower than SA-2, and may fail on the contract file itself.** (Fowler, Nygard). SA-2 says no primitive "runs an `orca` or `orca-ide` command" (SPEC:147); the grep only matches `orca(-ide)? (orchestration|worktree|terminal|agent)` (SPEC:172), so `orca-ide status`, `orca open`, `orca repo` pass it. Conversely SA-2 allows an Orca mention in the contract file as an example of a caller's question channel (SPEC:147), and that file lives in `src/superclaude/core/`, which AC-C1 scans (SPEC:172, SPEC:52); whether the text matches depends on its wording. Medium either way.

**F9 - SA-4/AC-C5 vs new flags.** (Wiegers). SA-4 allows "new flags" as additive (SPEC:149) and AC-C5 requires no deleted line (`grep -E '^-[^-]'`, SPEC:176). Appending `--unattended` to an existing Usage line deletes that line in the diff. The spec does not say where flags go (new line vs edited line). Guess needed: Medium.

**F10 - Phase ordering: the flag arrives before the gate resolution.** (Hohpe, Nygard sequence attack). P1 makes `--unattended` accepted by every command in 3.1 and 3.2, "a no-op where a command has no gate" (SPEC:159), but gated commands get their resolutions in P2-P4 (SPEC:160-162). Between phases `/sc:cleanup --unattended` is accepted yet still prompts (SPEC:103), which is the silent stall the spec exists to prevent (SPEC:44, CAPS:52). Related: P1 and AC-1.1 cover implement, post-release and pr-submit (3.2, phase P4) although "Phases 1-3 need no user decision" (SPEC:154) and D3 recommends pr-submit stay coordinator-or-person only (SPEC:240; SPEC:139). Suggest shipping the flag in the same phase as the command's gate rows.

**F11 - `partial` maps to `succeeded`.** (Nygard, Newman). WC-5 and the Decisions row send `partial` to `--outcome succeeded` (SPEC:63, SPEC:263), but Orca keeps dependents of a failed Task blocked and starts them after a succeeded one (CAPS:90, CAPS:77, CAPS:86). A coordinator using ready waves will start dependents on incomplete output unless it reads the contract. `partial` is also not defined anywhere (what makes a run partial). Design choice with a stated rationale: Medium.

**F12 - WC-11 against rows that keep fixed outputs.** (Whittaker accumulation/divergence). "Two workers in one worktree must never write the same file" (SPEC:69), yet cleanup-audit keeps a fixed output dir with only "one audit per worktree at a time" (SPEC:85) and index-repo keeps fixed `PROJECT_INDEX.md` with the fix limited to "state the output location" (SPEC:86; INV-A:53). The coordinator duty to serialise is not in 2.3 (SPEC:73). The reflect row also omits that reflect writes a tracked file `docs/memory/reflect/deviation-patterns-<slug>.md` (INV-B:114), relevant to WC-11 and to live-check step 6 (SPEC:185).

**F13 - Fan-in example has no count rule (Pipeline Dimensional Analysis).** (Fowler, Whittaker). Section 1.3 offers "several `/sc:troubleshoot` workers, then one `/sc:adversarial` worker on their reports" (SPEC:39). adversarial compares 2-10 artifacts (INV-A:35). Counts: 1 troubleshoot worker gives 1 report (below the minimum); 11 gives 11 (above); a failed or blocked worker leaves its dependent blocked (CAPS:90). The spec states no rule for N outside 2-10 or for partial failure. It is only an illustration ("for example"), so Medium (FR-19 would label a stated count assumption CRITICAL; consequence grading applies here). See Quantity Flow Diagram below.

**F14 - Evidence characterisation is inconsistent.** (Cockburn). E3 uses `invocation_method: "skill-direct"` as support for the decision (SPEC:23), while 1.4(1) says the PR #329 run "proves the nested route, not the direct route" (SPEC:43). INV-A:35 calls the same field proof of a "direct Orca-worker skill call". One of the two readings should be dropped. Also the tasklist row says reflect fan-out "runs one layer below the worker, inside Claude Code's nesting limit" (SPEC:122) while the inventory marks the underlying subagent use UNVERIFIED (INV-B:46) and reflect Tier 2 itself fans out further (INV-B:36).

**F15 - WC-3 vs AC-2.2.** (Adzic). WC-3 lets the worker `ask` instead of ending blocked (SPEC:61); AC-2.2 expects `worker_done --outcome failed` and `status: blocked` for every gate-trigger run (SPEC:200). A conforming worker that asks cannot meet AC-2.2, and 2.3 does not say whether `ask` is permitted for the Task (SPEC:73). The test result depends on that choice.

### Minor notes
- N1. WC-4 says the contract is written "on every outcome" (SPEC:62), which a killed or context-exhausted worker cannot do; WC-5 already covers "no report exists" (SPEC:63), so the claim is only over-stated.
- N2. 3.1 rows with "Small fix: None" (brainstorm, init-lite; SPEC:84, SPEC:87) are still in P1's flag scope (SPEC:159).
- N3. SPEC:285 item 14 and SPEC:11 describe a citation check this review cannot reproduce; leave as labelled.
- N4. The 7.2 step 5 transcript search for `AskUserQuestion` (SPEC:184) will also match the command text injected into the transcript; word it as "no `AskUserQuestion` tool call".
- N5. Edge: tasklist `--unattended` passes `--unattended` to each reflect, and Stage 10.5 uses `--remediate` (INV-B:46); what the headless auto-accept then runs is not shown in the inventories. UNVERIFIED.

---

=== ARCHITECTURE ANALYSIS ===

Strengths (no action): the decision to keep Orca above the commands is supported by CAPS:92 (Run does not schedule), CAPS:97-103 (depth 1), CAPS:147-150 (standalone and pane binding); the 10/27/6 split matches the inventories (INV-A summary section ("Counts") gives 5/13/3, INV-B:278 gives 5/14/3; 5+5, 13+14, 3+3); all INV row references in sections 3 and 4 line up with the inventory tables. No Orca call is placed inside a command (WC-8, SA-2). The single shared contract file and the installed-path rule are sound (SPEC:52).

Architecture issues are covered by F2 (interface drift in the contract path, blocking), F3-F5 (contract placement and retry), F8 (enforcement check), F10 (phase ordering), F11 (outcome mapping), F13 (fan-in).

Quantity Flow Diagram (Pipeline Dimensional Analysis triggered by the fan-out/fan-in in SPEC:39):

```text
[Coordinator: N troubleshoot Tasks] --> [each worker: 1 REPORT.md or failed/blocked] --> [M reports, M <= N]
                                                  |
                                                  v
                          [Task DAG: adversarial depends on all N]  (CAPS:90: any failed dependency keeps it blocked)
                          [adversarial: accepts 2-10 artifacts]  <-- MISMATCH when M < 2, M > 10, or N != M (spec states no rule)
```

---

=== ADVERSARIAL ANALYSIS (Whittaker) ===
- Sequence attack on WC-4/WC-5/WC-6: retry reads a stale `succeeded` contract (F4). State trace: before = `<dir>/return-contract.yaml {status: succeeded}`; attempt 2 dies at step 1; after = file unchanged; worker sends `--outcome succeeded` (SPEC:63).
- Divergence attack on WC-10/AC-4.3: a 270 s call (F6). Before: WC-10 trigger >300 s not met; after: AC-4.3 limit 240 s exceeded.
- Divergence attack on WC-4 versus rows: output-dir vs `<output>/adversarial/` vs `.dev/tasks/to-do/<id>/` (F2, blocking).
- Zero/Empty attack on `--unattended` without an output directory (F3); on a fan-in of one report (F13).
- Sentinel collision on `status`: WC-4 fixes four values (SPEC:62) while "commands that already write a contract keep their fields" (SPEC:62). If an existing contract's own `status` vocabulary differs from the four (the inventories do not list the values; UNVERIFIED), WC-4 and "keep their fields" collide.
- Accumulation attack: two workers on fixed outputs (F12).

---

=== GUARD CONDITION BOUNDARY TABLE ===
Guards identified: G1 WC-5 outcome mapping; G2 WC-10 wait split; G3 WC-1 readiness fallback; G4 WC-2 gate resolution under `--unattended`; G5 WC-8 depth; G6 task confidence 0.70 (SPEC:121). Classes left out are given one line each below the table.

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|-------|----------|-----------------|----------------|--------------|-------------------|--------|
| G1 outcome mapping | SPEC:63 | Zero/Empty | no report file | failed branch | `--outcome failed` | OK |
| G1 | SPEC:63 | Typical | `status: succeeded` | succeeded branch | `--outcome succeeded` | OK |
| G1 | SPEC:63 | Sentinel Value Match | `status` outside the four values (existing contract vocabulary) | undefined | not specified (see Adversarial analysis, sentinel collision) | GAP (Medium) |
| G1 | SPEC:63,64 | Legitimate Edge Case | stale contract from a prior attempt | succeeded branch taken wrongly | not specified (F4) | GAP (Medium) |
| G1 | SPEC:63,263 | Legitimate Edge Case | `status: partial` | succeeded branch | `--outcome succeeded`, body states partial; `partial` undefined (F11) | OK (design choice) |
| G2 wait split | SPEC:68 | Typical | 3 min wait | no split | none needed | OK |
| G2 | SPEC:68,210 | Maximum/Overflow | single call 270 s | WC-10 false, AC-4.3 true | conflicting (F6) | GAP (Medium) |
| G2 | SPEC:68 | Maximum/Overflow | single call 600 s | true | split into waits <= 4 min | OK |
| G3 readiness fallback | SPEC:59 | Typical | 30 s fallback | within limit | passes (carried from EVIDENCE.md:45,56, UNVERIFIED) | OK |
| G3 | SPEC:59 | Maximum/Overflow | fallback 45-60 s | "well inside" | no number stated | GAP (Medium; WC-1 owner is launch setup, SPEC:59) |
| G4 gate under `--unattended` | SPEC:60 | Zero/Empty | `--unattended` with no output dir | undefined | not specified (F3) | GAP (Medium) |
| G4 | SPEC:60 | Sentinel Value Match | `--unattended` together with `--interactive` | undefined | refusals listed only for some rows (SPEC:102,103,108,110,123) | GAP (Medium) |
| G4 | SPEC:60 | Typical | gate with no supplied flag | blocked branch | contract `blocked` + question | OK |
| G5 depth | SPEC:66 | Typical | command calls `worker-start` | refused by Orca | forbidden by WC-8 | OK |
| G6 task confidence | SPEC:121 | Legitimate Edge Case | confidence exactly 0.70 | "below 0.70" false | proceeds (inventory text "< 0.70", INV-B:45) | OK |
| G6 | SPEC:121 | Zero/Empty | confidence 0 / missing | true | blocked | OK |

Left out, with reason: One/Minimal for G1-G6 (no countable input); Maximum for G1, G5, G6 (bounded set, cannot overflow); Sentinel for G2, G3, G5, G6 (no reserved value). All cells above are populated; the table is complete per FR-10. GAP cells are Medium by the FR-8 rule: none names a concrete wrong outcome without a guess, so none blocks.

---

=== SYNTHESIS ===
Overall: the design decision and the 43-command inventory mapping are well supported and traceable. Two internal contradictions block: the `load` handling against AC-1.1 (F1), and the contract-path rule against the adversarial and workflow rows and the live check (F2). Medium items cluster around the report-file contract (F3-F5, F7, F15), phase ordering (F10) and outcome semantics (F11).

Consensus: Wiegers, Adzic, Crispin, Fowler agree on F1 and F2; Nygard and Whittaker add F4 and F6. No expert disagreement recorded.

Not evidenced here (UNVERIFIED): all `src/` line cites and the four Orca-behaviour assumptions the spec lists itself (SPEC:272-284).

## Reviser brief
Blocking finding ids: F1, F2.
Rules for the reviser (restated from the command's Review Loop bullet 6; the reviser reads this report, not the command): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size of the candidate before and after, with the bytes added and deleted per finding id. Leave F3-F15 and the minor notes alone.
- F1: texts to repair: SPEC:195 (AC-1.1), SPEC:76 and SPEC:159 (scope of the Unattended section and flag), against SPEC:112 and SPEC:265 (`load` row and Decision).
- F2: texts to repair: SPEC:62 and SPEC:73 (WC-4 "known before dispatch", `<output-dir>/return-contract.yaml`), SPEC:83 (adversarial), SPEC:92 (workflow), SPEC:182-183 and SPEC:196 (live check and AC-1.2).

verdict: FAIL

review: 1 of 3

# Whole-document audit of the Orca worker-contract spec (first review, critique mode)

- Label: whole-document audit of the final spec, a first review of the whole document (no `--re-review`, no `--baseline`).
- Command: `/sc:spec-panel @.dev/orca-command-refactor/specs/orca-worker-contract-spec.md --mode critique --focus requirements,architecture`
- Candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`
- Candidate sha256: `6df71d66ba77941856614e39ef7598d78d9d296b701f694093bc4d5e6d1b9394`
- Baseline sha256: not applicable (first review).
- Reviewer model used: claude-sonnet-5-5
- Prompt followed: FIRST-REVIEW prompt, `~/.claude/rules/prompts/document_review_loop_prompts.md:27-32`.
- Citations: `SPEC:N` = line N of the candidate. `INV-A:N`, `INV-B:N`, `CAPS:N` = lines of `inventory/commands-a.md`, `commands-b.md`, `orca-capabilities.md`.

## What I covered, and what I could not check

Covered: all 285 lines of the spec; the README; all three inventories, by targeted line checks of every inventory line the spec's headline claims lean on (CAPS 38-188 for the Orca facts, INV-A 35-120, INV-B 31-323 for the per-command verdicts).

Checked and found as cited:
- The 10 / 27 / 6 split, counted three ways. Rows in SPEC 3.1 (10), 3.2 (27) and section 4 (6). Phase totals 9+11+4+3 = 27 for 3.2. The inventories' own totals (INV-A: 5 ready, 13 needs-change, 3 coordinator-only; INV-B:278 "5 ready, 14 needs-change, 3 coordinator-only") add up to the same.
- The Orca facts quoted in R1-R5 and E1-E4 against CAPS:44-52, 58-68, 72-80, 97-103, 107-113, 129-130, 145-161.
- The unverified-item numbering in SPEC 272-284 against CAPS:177-188.

UNVERIFIED (no file in the workspace to check against):
- Every citation to `src/superclaude/...`, `tests/`, `Makefile`, `pyproject.toml`, `CLAUDE.md:N`, `EVIDENCE.md:N`, `.dev/codegraph-migration/...` and the Orca guide text beyond what the CAPS inventory quotes. The spec's own claims that 11 locations were re-read (SPEC:11) and that about 340 citations were independently checked (SPEC:285) cannot be confirmed here and are not relied on.
- The grep results behind E5 (SPEC:25).

Brief clauses overridden: none.

## === REQUIREMENTS ANALYSIS ===

### F1. BLOCKING, MAJOR (Wiegers, Crispin): the P0 acceptance check cannot pass as written
- Grading sentence: an implementer who follows the stated text as written runs the P0 live check on `/sc:troubleshoot`, `/sc:workflow` and `/sc:adversarial` and builds a pass/fail verdict that can never be "pass". Step 3 of the live check requires "its `--outcome` matches the contract's `status` under WC-5; its report path is the WC-4 contract path" (SPEC:182). AC-0.4 requires "steps 1-3 and 5-7 pass" and relaxes only step 4 "since the contract arrives in P1" (SPEC:194). The WC-4 contract `<output-dir>/return-contract.yaml` is a P1 deliverable (SPEC:62, SPEC:159), and troubleshoot's report is `REPORT.md` (SPEC:91). So step 3 asks for a contract that AC-0.4 itself says does not exist yet. Phases do not advance until the earlier phase's checks pass (SPEC:154), so P0, and with it every later phase, cannot be declared done. The smoke runs are what the spec uses to test its own central decision (SPEC:43, SPEC:158), so the gap sits on the critical path.
- Two stated texts contradict each other: SPEC:182 versus SPEC:194.
- Recommendation: in AC-0.4 say that step 3 also uses the command's existing report file and its own status field (or none), not the WC-4 contract path. Narrow, do not add.
- Priority: High. Quality impact: the evidence-gap closure promised at SPEC:43 and SPEC:272 cannot be certified.

### F2. Medium (Wiegers): no acceptance check for WC-1, WC-3, WC-6, WC-11 (beyond save) or WC-12
Section 7 has no check that a retry worker leaves the first attempt intact (WC-6, SPEC:64), that a launch path has no pre-readiness prompt (WC-1, SPEC:59), or that `ask` resumes by message id (WC-3, SPEC:61). WC-11 is checked only for `/sc:save` (AC-3.4, SPEC:207). Requirements the spec states but never tests; no wrong outcome follows from the text itself. Follow-up candidate.

### F3. Medium (Wiegers, Adzic): WC-4 "known before dispatch" versus WC-6 "fresh output directory"
WC-4 fixes the report at `<output-dir>/return-contract.yaml` with the directory passed by the coordinator (SPEC:62). WC-6 tells a command with no resume flag to write "each run into a fresh output directory" (SPEC:64). About 30 rows use "fresh dir" (SPEC:99-125, 83-92). If the command makes the fresh sub-directory itself, the report is no longer at the path the coordinator knew; if it writes into the passed directory, a `--retry-of` worker reuses the first attempt's directory. Section 2.3 (SPEC:73) never says the coordinator passes a new `--output` per attempt. One reading satisfies both texts, so this is Medium, not blocking.

### F4. Medium (Wiegers): `--post-pr` is required but does not exist
SPEC:100 and SPEC:67 say posting "returns only with an explicit `--post-pr` in the brief"; AC-2.4 (SPEC:202) and D4 (SPEC:244) rely on it. The inventory records only the off switch `--no-post-pr`, with posting on by default (INV-A:38, INV-A:78). The row lists "Other required change: none" (SPEC:100). The new flag is a mechanism the spec needs but does not state, so as written D4(a) can never be exercised for auggie-review. Follow-up candidate: add the flag to the row, or say posting stays coordinator-only.

### F5. Medium (Wiegers, Cockburn): the workflow contract path is not known before dispatch
The workflow contract lives at `.dev/tasks/to-do/<id>/return-contract.yaml` (SPEC:92; INV-B:272), and the package is created fresh each run (INV-B:273). The coordinator cannot know `<id>` when it writes the brief, which WC-4 and section 2.3 require (SPEC:62, SPEC:73). The worker can still report the path in `--report-path`, so the effect is a stated rule that one ready command breaks, not a wrong outcome.

### F6. Medium (Cockburn): P1 touches commands whose behaviour awaits the user decisions D2-D4
P1 adds `--unattended` and, per AC-1.1, an `## Unattended mode` section to every command in 3.1 and 3.2 except `/sc:load` (SPEC:159, SPEC:195). That includes `implement`, `post-release` and `pr-submit`, whose behaviour is defined in P4 after D2-D4 (SPEC:162). The spec also says "Phases 1-3 need no user decision" (SPEC:154), and D3's recommended option (a) is "no pr-submit changes in Phase 4" (SPEC:240) while P1 still edits pr-submit. Between P1 and P4 a flag exists whose outward-action default (WC-9, SPEC:67) is not yet implemented for those three commands. Follow-up candidate: exclude the three P4 commands from P1 or state they stay inert until P4.

### F7. Medium (Cockburn): P1 is labelled "commands with no gate" but contains gate-like refusals
business-panel, explain, index and test each carry an unattended refusal or pinned mode in P1 (SPEC:102, 108, 111, 123) while the phase description says "No person gate is involved" (SPEC:159). Wording only.

## === ARCHITECTURE ANALYSIS ===

### F8. Medium (Fowler, Newman): AC-C1 can fail on the spec's own P0 deliverables
AC-C1 requires that a grep for `orca(-ide) orchestration|worktree|terminal|agent` over `src/superclaude/{commands,skills,agents,core}`, minus `ccsession-tag`, prints nothing (SPEC:172). P0 adds `core/WORKER-CONTRACT.md` and an Orca section in `core/HOW-WE-WORK.md` (SPEC:158). SA-2 allows an Orca mention "as an example of a caller's question channel inside the contract file" (SPEC:147). The contract and the routing section are written for coordinators and workers, so they will naturally name verbs such as `orca orchestration check`. Whether they match depends on the wording chosen; the check and SA-2 are not reconciled. Follow-up candidate: exempt those two files or state the allowed phrasing.

### F9. Medium (Fowler, Nygard): the tasklist row leaves a person-blocking HALT and relies on an inventory-contradicted nesting claim
- The row makes Stage 10.5 pass `--unattended` to each reflect "so the headless rule applies" (SPEC:122). The headless rule auto-accepts auto-fixable registers and skips the gates (INV-B:109), so unattended tasklist generation would trigger remediation hand-offs the inventory advised dropping (`--remediate` removed or headless, INV-B:215; INV-B:46). The row does not resolve the `needs_human_decision` HALT at `SKILL.md:1631`, which INV-B:209 reports as an open question; under WC-2 a HALT in a worker is a silent stall (SPEC:60).
- The row says its reflect fan-out "runs one layer below the worker, inside Claude Code's nesting limit" (SPEC:122). INV-B:210 describes subagent-to-agent nesting (reflect spawning its own agents inside the Stage 10.5 subagents) and marks whether it works UNVERIFIED. The spec's claim is a different, unproven reading.
- Whether `--unattended` counts as headless for reflect is itself UNVERIFIED (SPEC:280). Medium because the outcome depends on how that unverified rule behaves.

### F10. Medium (Nygard): local destructive edits under `--unattended`, with a rollback the spec says is UNVERIFIED
cleanup and improve apply the items their files allow without approval (SPEC:103, 110). Both carry a "backup and rollback" claim whose mechanism is unknown (INV-A:118), and the spec's remedy is only to list changed files. WC-9 covers outward actions, not local deletions (SPEC:67), and WC-11 covers only same-file write collisions (SPEC:69). No data-loss outcome is named by the text, so Medium.

### F11. Medium (Fowler): explain gains the Write tool, which changes its standalone capability
SPEC:108 adds Write to a command that today has only Read/Grep/Glob, TodoWrite and Task, while SA-1 says every standalone behaviour stays as it is (SPEC:146). SA-4 lists "explain tools" as a permitted defect fix (SPEC:149), so the texts are reconcilable; the capability change is still a standalone-visible change. Follow-up candidate: say it is granted only when an output path is passed.

### F12. Medium (Nygard): WC-10's 4-minute rule rests on a cadence the spec cannot confirm matters
The 5-minute heartbeat comes from the dispatch preamble, and whether heartbeat age feeds Orca's liveness verdict is UNVERIFIED (CAPS:130, CAPS:182). WC-10 nonetheless makes wait-splitting a hard requirement (SPEC:68) and AC-4.3 a hard check (SPEC:210). Follow-up candidate: mark WC-10 advisory until item 7 of the Orca unverified list is resolved.

## === Notes (minor) ===
- The pr-submit top-level rule is cited at `SKILL.md:37-39` (SPEC:65), while the capabilities inventory quotes the installed copy at `:47-49` (CAPS:161). Different copies, so a line shift is plausible; neither can be checked here.
- SPEC:285 (UNVERIFIED item 14) reports a verification result rather than an unverified item, and is a self-report.
- SA-4's list of permitted existing-line edits (SPEC:149) omits the validate-tests skill tool addition (SPEC:125) and the cli-portify checkout restriction (SPEC:105).
- Section 7.2 step 5 searches a transcript for `AskUserQuestion`; the command text and preamble loaded into the transcript may also contain the word, so the pass condition should read "no call", which SPEC:184 does say.

## Guard Condition Boundary Table (Nygard builds, Crispin completeness, Whittaker attacks)

Trigger: the spec contains thresholds and boolean guards. Classes left out are named in one line per guard.

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|---|---|---|---|---|---|---|
| WC-5 outcome map | SPEC:63 | Zero/Empty | no report file | failed | `--outcome failed` | OK |
| WC-5 outcome map | SPEC:63 | Legitimate Edge Case | report exists but is unreadable or has a `status` outside the four values | unspecified | not stated; AC step 4 would fail it (SPEC:183) | GAP (Medium, follow-up) |
| WC-5 outcome map | SPEC:63 | Sentinel Value Match | `partial`, or FAIL verdict | succeeded | stated | OK |
| WC-4 `blocked_question` | SPEC:62 | Zero/Empty | `status: blocked` with empty question | not forbidden | AC-2.2 requires non-empty (SPEC:200), WC-4 does not | GAP (Medium, follow-up) |
| WC-10 wait split | SPEC:68 | Typical | single call over 5 min | split to at most 4 min | stated | OK |
| WC-10 wait split | SPEC:68 | Legitimate Edge Case | a call between 4 and 5 min | not required to split | stated by omission | OK |
| WC-6 resume | SPEC:64 | Zero/Empty | no resume flag | fresh dir | stated, but see F3 | OK, see F3 |
| WC-9 outward default | SPEC:67 | Typical | brief names flag | on | stated; flag missing for auggie-review | GAP (F4) |
| WC-3 `ask` | SPEC:61 | Maximum/Overflow | repeated timeouts | resume same id | stated; no cap on retries | GAP (minor) |
| WC-12 `check` | SPEC:70 | Legitimate Edge Case | `consumer_fenced` | stop, no `worker_done` | stated | OK |

Not given a row: "One/Minimal" and "Maximum" for WC-5 and WC-9, because they are boolean guards with no magnitude.

## Quantity flow (Fowler, Whittaker)

43 commands (21 + 22; SPEC:76, INV-A:3, INV-B:3) go to 10 ready + 27 needs-change + 6 coordinator-only. 27 goes to P1 9 + P2 11 + P3 4 + P4 3; the P2 phase list of 15 adds the 4 ready commands that get gate fixes (SPEC:160). No count divergence found; no CRITICAL dimensional finding.

## follow-up candidates (Medium and minor; none changes the verdict)

F2, F3, F4, F5, F6, F7, F8, F9, F10, F11, F12, the minor notes, and the two boundary-table GAP rows. The reviewing session asks the user once whether to open an issue for them; this audit worker was not authorized to ask and created none.

## Reviser brief

Blocking finding ids: F1.
Rules for the reviser: revise only text a blocking finding names; add no rule, mechanism or section that no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, and the bytes added and deleted per finding id. Leave Medium and minor findings alone.

verdict: FAIL

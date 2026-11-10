review: 1 of 3

# Spec-panel audit: orca-worker-contract-spec.md

- command: `/sc:spec-panel @.dev/orca-command-refactor/specs/orca-worker-contract-spec.md --mode critique --focus requirements,architecture`
- kind: labelled whole-document audit of the final spec (a first review of the whole document), per the FIRST-REVIEW prompt of `~/.claude/rules/prompts/document_review_loop_prompts.md` (read in full).
- candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`
- candidate sha256: `530bb94dc36fffb71a0dd0f59ecf0aa60e32ab1c485bde6cfedea040d97adda7`
- baseline: none given (no `--re-review`, no `--baseline`); this is a first review, so no baseline hash applies.
- reviewer model actually used: claude-sonnet-5-5
- brief clauses overridden: none. The brief narrowed nothing and widened nothing.
- Citation convention: `S:N` = line N of the candidate spec; `CAPS:N`, `INV-A:N`, `INV-B:N` = line N of `inventory/orca-capabilities.md`, `commands-a.md`, `commands-b.md`. Those four files and `README.md` are the only evidence checkable in this sandbox. Every citation to `src/`, `CLAUDE.md`, `.dev/evals/`, `.dev/codegraph-migration/`, `pyproject.toml`, `Makefile` or Orca's installed files is UNVERIFIED here, except where an inventory quotes it. I checked each `INV-*` and `CAPS:*` reference the spec makes for the load-bearing claims: the per-command rows in sections 3 and 4, the WC-1 to WC-12 evidence cells and the UNVERIFIED list. All I checked match their lines.

## Coverage
Read in full: the spec (294 lines), README, the three inventories, command.md and the review-loop prompts. Panel: Wiegers, Adzic, Cockburn (requirements); Fowler, Nygard, Whittaker, Newman, Hohpe (architecture and attack). Crispin, Gregory and Hightower were not seated, because testing, compliance and cloud-native are outside `--focus requirements,architecture`; Whittaker is seated in every review. Not covered: the real command and skill files (not in the sandbox), Orca behaviour (no live Orca), and the `ws/` copy of `WORKER-CONTRACT.md` (not present).

## Quality assessment (0-10)
clarity 8, completeness 7, testability 7, consistency 6. Overall 7.

Pipeline Dimensional Analysis (FR-17): not triggered. The spec describes no data pipeline whose output count differs from its input count; the Task, worker, report chain is one-to-one, and a retry is a new Dispatch of the same Task (`S:64`, `CAPS:116`). No Quantity Flow Diagram is produced.

State Variable Registry: not produced, because `--focus correctness` is not active. The Guard Condition Boundary Table is produced below, because the spec contains guards.

## Findings

Grading used the FIRST-REVIEW grading check. A finding is blocking only if "an implementer who follows the stated text as written builds X, and X is wrong because Y" holds with no further assumption.

### === REQUIREMENTS ANALYSIS ===

**F1. BLOCKING. CRITICAL. Expert: Wiegers (lead), Adzic. Priority: High. Quality impact: Phase 1 cannot pass its own acceptance check.**
Issue: Three texts disagree about what Phase 1 changes.
- Phase 1 scope says the `--unattended` flag is "accepted by every command in sections 3.1 and 3.2 (a no-op where a command has no gate)" (`S:159`).
- The Phase 1 Commands column lists only analyze, build, business-panel, design, document, explain, index, test, load (usage line only), plus fixes to adversarial, cleanup-audit, index-repo and workflow (`S:159`). That is 12 commands.
- AC-1.1 asserts that every command in sections 3.1-3.2 except `/sc:load` has a `## Unattended mode` section naming `return-contract.yaml` and `~/.claude/WORKER-CONTRACT.md` (`S:202`). That is 36 commands (10 + 27 - 1).

The same sections are assigned elsewhere to later phases:
- The gate resolutions for 15 commands belong to Phase 2 (`S:160`).
- Four commands belong to Phase 3 (`S:161`).
- implement, post-release and pr-submit belong to Phase 4, which "waits for D2-D4" (`S:154`, `S:162`, `S:109`, `S:113`, `S:114`).

Section 2.1 says each section "lists only its own gate resolutions" (`S:52`). So AC-1.1 requires Phase 1 to write sections whose gate resolutions the spec defers to Phase 2-4, and for Phase 4 to the undecided D2-D4.

Concrete wrong outcome: An implementer who follows the Phase 1 Commands column builds 12 command edits. AC-1.1 then fails for the other 24 commands, so Phase 1 cannot pass (`S:167`, "A phase passes only when every check in its block ... passes"). An implementer who follows AC-1.1 writes `## Unattended mode` sections for implement, post-release and pr-submit before D2-D4 are answered. Those commands would then accept `--unattended` while their gates still wait, which is exactly the stall WC-2 forbids (`S:60`). Phase 1 live checks (AC-1.2) cover only "each P1 command" (`S:203`), so no check catches that stall.

Recommendation (for the reviser, narrow): restrict AC-1.1 and the Phase 1 scope sentence to the Phase 1 command list, and give each later phase its own "section exists" assertion alongside its gate assertions (AC-2.1 already has the pattern, `S:207`). Do not add a new mechanism.

### Medium and minor findings (follow-up candidates, not blocking)

**M1. Medium (MAJOR label). Wiegers.** WC-4 puts the contract in "the directory the coordinator passed (`--output` / `--output-dir`)" (`S:62`). Four commands in sections 3.1-3.2 have no such flag and no row adds one:
- cleanup-audit (brief passes only `--pass <N>`, fixed dir, `S:85`)
- index-repo (brief passes nothing, `S:86`)
- recommend (`S:115`: "write the handoff envelope to a file; contract", no path flag)
- validate-tests (`S:125`: only the `--report` file)

AC-1.1 and 7.2 step 4 still require a contract for them (`S:202`, `S:190`). The spec never states where it goes. This is a requirement left unstated, so it is Medium by the grading check. Candidate fix: name the contract location for these four.

**M2. Medium. Whittaker (sentinel/sequence).** For a file-valued `--output` (tdd, init-lite) WC-4 puts the contract in the directory containing the file (`S:62`, `S:87`, `S:90`). The tdd default is `docs/[domain]/TDD_[COMPONENT].md` (`INV-B:222`), so two workers on one domain share a directory and write the same `return-contract.yaml`. WC-11 says two workers "must never write the same file" (`S:69`). Whether it happens depends on the coordinator choosing the same directory, which section 2.3 does not forbid (`S:73`), so Medium.

**M3. Medium. Adzic.** SA-3 says contract and report files are written "only in unattended mode or when the caller passes the new output flag" (`S:148`). WC-4 says the contract is written "In unattended mode" (`S:62`). Does `/sc:analyze --output x` without `--unattended` write a contract? One reading says yes (SA-3), the other no (WC-4, AC-1.3 at `S:204`). The implementer must guess.

**M4. Medium. Nygard.** WC-6 says a command without a resume flag "writes each run into a fresh output directory" (`S:64`). WC-4 and section 2.3 say the report path is the directory the coordinator passed, "known before dispatch" (`S:62`, `S:73`). Nothing says the coordinator passes a new directory per retry attempt. Reusing the first attempt's directory would overwrite its contract and artifacts, which WC-6 forbids. Candidate fix: state who creates the fresh directory.

**M5. Medium. Fowler, Nygard (safety boundary).** WC-3 lets the worker, when a gate "would resolve as blocked", ask the coordinator and "re-invoke or resume the command with the answer as a flag" (`S:61`). It has no carve-out for answers that grant what other rules reserve:
- D2(a) keeps the Ruling rule, under which another agent's message is not acceptance (`S:241-244`).
- WC-9 and D4(a) allow an outward action only through the command's explicit flag "written in the brief" and the user's own instruction (`S:67`, `S:253`).

A coordinator's `ask` answer could therefore supply a flag that the specific rules say only the brief or the user may supply. The more specific rules probably win, so this is Medium. Candidate fix: one sentence in WC-3 excluding Ruling and outward-action flags.

**M6. Medium. Wiegers.** Several rows resolve a gate as "refused" (explain `--format interactive`, cleanup/improve/roadmap `--interactive`, business-panel socratic, test `--watch`, pr-submit `--monitor 1`; `S:102-103`, `S:108`, `S:110`, `S:114`, `S:118`, `S:123`). "Refused" is not one of WC-2's three resolutions (default, flag, blocked) (`S:60`). No status is specified for it. WC-4 requires a contract "including stops before any other output exists" (`S:62`). A `failed` or `blocked` reading changes the AC-2.2 style checks. Candidate fix: map "refused" to `blocked` or `failed`.

**M7. Medium. Adzic.** AC-0.4 requires the existing workflow contract's `status` to be one of `succeeded|partial|failed|blocked` (`S:201`). The inventories say only that workflow writes a `status` field (`INV-B:272`), not its values. WC-4 says contracts that already exist "keep their fields" (`S:62`), and WC-5 sends `--outcome failed` for any other value (`S:63`). If the workflow, brainstorm or reflect vocabularies differ, Phase 0 fails and, per AC-0.4, "reopens section 1" (`S:201`) for a reason that has nothing to do with the decision. The vocabulary is UNVERIFIED here.

**M8. Medium. Hohpe.** AC-C1 must print nothing for `\borca(-ide|-cli)?\s+(orchestration|worktree|terminal|agent|status)` over `src/superclaude/core` (`S:178-183`). Phase 0 adds `WORKER-CONTRACT.md` and a HOW-WE-WORK section to that folder (`S:158`), and SA-2 allows an Orca mention "as an example of a caller's question channel inside the contract file" (`S:147`). A mention such as `orca orchestration ask` would fail AC-C1. Whether the new text contains one is not stated. Candidate fix: say the contract text names the preamble's `ask` command without the `orca <verb>` form, or exempt the file.

**M9. Medium. Fowler.** Tasklist under `--unattended` passes `--unattended` to each reflect "so the headless rule applies" (`S:122`). Stage 10.5 runs reflect with `--remediate` (`INV-B:209`), so the rule auto-accepts remediation for auto-fixable registers (`S:88`, `INV-B:109`). `INV-B:215` recommended calling reflect without `--remediate` instead. The spec chose auto-accept; the lines it relies on (`remediation-handoff.md:239-247`) are UNVERIFIED here. No recorded reason for the choice appears in the Decisions table.

**M10. Medium. Cockburn.** The auggie-review row says posting "returns only with an explicit `--post-pr` in the brief" (`S:100`). Today only `--no-post-pr` exists and posting is the default (`INV-A:38`). The new flag is not listed under "Other required change", and its absence from the Usage line is not mentioned.

**M11. Medium. Nygard.** Thresholds are loose or inconsistent:
- WC-1 says fallbacks must be "well inside" the 60 s limit and gives no number (`S:59`). The evidence shows 30 s passed and about 45 s failed with a 45 s test limit (`CAPS:49`).
- WC-10 requires splitting only calls longer than 5 minutes, into waits of at most 4 minutes (`S:68`), but AC-4.3 and the pr-submit row require every call under 240 s (`S:114`, `S:218`). A 4.5-minute call passes WC-10 and fails AC-4.3.

**M12. Medium. Adzic.** AC-2.2 passes only if the worker ends `failed` with `blocked` (`S:208`). WC-3 says the worker "may instead ask the coordinator" (`S:61`). A conforming worker that asks and then succeeds fails AC-2.2. The test brief must forbid `ask`, and nothing says so.

**M13. Medium. Whittaker (accumulation).** WC-11 says two workers in one worktree must never write the same file (`S:69`). cleanup-audit writes a fixed `.claude-audit/` and index-repo a fixed `PROJECT_INDEX.md` (`S:85-86`). The spec handles the first with "one audit per worktree at a time" in a table cell, but the rule is not in the section 2.3 list of what the brief states (`S:73`). reflect also writes a tracked file `docs/memory/reflect/deviation-patterns-<slug>.md` (`INV-B:114`), which no row covers.

**M14. Medium. Newman.** `plugins/superclaude/commands/` copies are not kept in step by any stated rule; UNVERIFIED item 8 leaves it to "each phase's plan" (`S:287`). SA-5 and AC-C2 check only the `.claude/` mirror (`S:150`, `S:173`).

**M15. Medium. Cockburn.** The count "27 needing a change" includes pr-submit, post-release and implement (`S:76`). The recommendation for D3 is that pr-submit is coordinator-only with "no pr-submit changes in Phase 4" (`S:248`). The totals and the Phase 4 scope change if D3 (a) is chosen.

**N1. Minor.** Revision tags such as `M3`, `M4`, `M6`, `M7`, `M8`, `M10`, `R2-1`, `R2-2` appear in the text (`S:62-63`, `S:172`, `S:201`) with no definition in the document; their source, `review/disposition.md`, is not in the sandbox.
**N2. Minor.** AC-0.4 cites `INV-A:35` for "no `status` field" on both troubleshoot and adversarial (`S:201`). `INV-A:35` is the adversarial row and names no field list; troubleshoot is `INV-B:242`.
**N3. Minor.** D5(b) calls R1 a "protection against runaway fan-out" (`S:260`); R1 is a refusal reason, not a protection (`S:33`).
**N4. Minor.** The spec states the tasklist reflect fan-out is "inside Claude Code's nesting limit" (`S:122`). `INV-B:210` and `INV-B:314` mark nested spawning UNVERIFIED.
**N5. Minor.** UNVERIFIED here: the claims that the author "re-read 11" locations and that a validator re-read "about 340 citations" (`S:11`, `S:293`); the E5 grep results (`S:25`); and every citation outside the inventories.

### === ARCHITECTURE ANALYSIS ===
The decision (Orca coordinates, commands stay units of work, `S:16`) is supported: R1-R5 (`S:33-37`) trace to `CAPS:97-103,145-150`, and the three evidence gaps (`S:43-45`) are stated plainly. No blocking architectural defect was found beyond F1. Expert notes:
- Fowler: the shared-contract-file design (`S:52`) keeps rules in one place; M1 and M4 are where the interface to the coordinator is still open.
- Newman: the unattended section plus a fixed four-value status set is a stable versioned surface; M7 is the compatibility gap with existing contracts, and M14 the mirror gap.
- Hohpe: the message exchange is pull-based (`S:70`, `CAPS:66-67`) and `worker_done` is sent once (`S:63`); M5 is the one place an ask answer could cross a boundary.
- Nygard: failure modes are covered by `blocked`/`failed` and WC-10; M11 and M4 are the loose ends.

### Whittaker adversarial analysis (FR-3 format)
- I can break this specification by **Sequence Attack**. The invariant at **WC-3/WC-4** ("written on every outcome", `S:61-62`) fails when **a worker writes `status: blocked`, asks the coordinator, and the re-invoked command dies before overwriting**. Concrete attack: before, `<dir>/return-contract.yaml` has `blocked`; the command is re-invoked and the session is killed; after, the stale `blocked` contract remains and the coordinator reads it as this attempt's result. Severity: MINOR (no stated rule says the file is deleted first, and a missing `worker_done` is visible to Orca).
- I can break this specification by **Sentinel Collision Attack**. The invariant at **WC-5** (`S:63`) fails when **a legitimate contract uses `status: partial` with `verdict: FAIL`**. Concrete attack: an audit finishes with FAIL; `partial` maps to `succeeded`; a coordinator that gates on outcome alone starts dependents. The spec covers this by gating on `verdict` (`S:63`), so the invariant holds; noted as handled.
- I can break this specification by **Zero/Empty Attack**. The invariant at **AC-2.2** (`S:208`) fails when **`blocked_question` is empty**. Concrete attack: contract `status: blocked`, `blocked_question: ""`; the check demands non-empty, so the test fails; WC-4 requires the question "when blocked" but states no empty-string rule. Severity: MINOR.
- Divergence and Accumulation attacks produced M2, M4 and M13 above.

## Guard Condition Boundary Table
Classes that cannot occur are omitted with a one-line reason. Status GAP entries are graded in the findings above.

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|---|---|---|---|---|---|---|
| `--unattended` present | `S:51`, `S:146` | Zero/Empty (absent) | no flag | false | Standalone behaviour unchanged (SA-1) | OK |
| `--unattended` present | `S:51`, `S:159` | Typical | flag in brief | true | Mode applies; P1 scope vs AC-1.1 disagree on which commands accept it | GAP (F1) |
| report `status` | `S:63` | Zero/Empty (missing) | no `status` | not one of four | `--outcome failed` | OK |
| report `status` | `S:63`, `S:201` | Sentinel Value Match | legacy value (e.g. `success`) | not one of four | `failed` (WC-5); P0 check unclear | GAP (M7) |
| report `status` | `S:63`, `S:208` | Legitimate Edge Case | `partial` | true | `succeeded`, text states `partial` | OK |
| contract location | `S:62` | Zero/Empty | no output flag (4 commands) | unresolvable | not stated | GAP (M1) |
| contract location | `S:62`, `S:69` | Maximum/Overflow | two file-valued `--output` in one dir | collides | not stated | GAP (M2) |
| refused flag | `S:102-123` | Legitimate Edge Case | `--watch`, `--interactive` etc. | refused | no status or contract status given | GAP (M6) |
| wait length | `S:68`, `S:218` | One/Minimal | 4.5 min single call | WC-10 true, AC-4.3 false | rules disagree | GAP (M11) |
| wait length | `S:68` | Maximum/Overflow | > 5 min call | true | split into waits of at most 4 min | OK |
| readiness limit | `S:59` | Typical | prompt fallback 30 s | true | passes (`CAPS:49`) | OK |
| readiness limit | `S:59` | Maximum/Overflow | fallback near 60 s | unclear | "well inside" is undefined | GAP (M11) |
| nesting depth | `S:33`, `S:66` | Typical | depth 1 | worker may not dispatch | `nested_worker_depth_exceeded`; WC-8 forbids | OK |
| nesting depth | `S:66` | Legitimate Edge Case | depth-1 `task-create` | unknown | WC-8 forbids either way | OK |
| confidence gate (task) | `S:121` | Legitimate Edge Case | exactly 0.70 | false (not below) | proceeds | OK |
| confidence gate (task) | `S:121` | Typical | < 0.70 | true | blocked | OK |
| `--monitor` ordinal (pr-submit) | `S:114` | One/Minimal | `--monitor 1` | true | refused (status unspecified) | GAP (M6) |
| `--monitor` ordinal (pr-submit) | `S:114` | Typical | `--monitor 0`, `2` | unstated | not stated; default is `3` | GAP (minor: values 0 and 2 are the command's own) |
| `--depth deep` short input | `S:91` | Legitimate Edge Case | exactly 10 words | false | proceeds (skill's own rule, `INV-B:239`) | OK |
| retry circuit breaker | `S:64` | Maximum/Overflow | 3 failed starts | true | Orca fails the Task (`CAPS:80`); a worker's own `failed` does not count | OK |
| `ask` timeout | `S:61` | Zero/Empty (omitted) | no `--timeout-ms` | unknown | resume by message ID; default UNVERIFIED (`S:289`) | OK |

## Follow-up candidates
Medium: M1-M15. Minor: N1-N5 and the two minor Whittaker notes. None of these triggers a revision, fails the review or appears in the Reviser brief. The session that ran this review is a worker whose reply is restricted to one line, so it did not ask the user whether to open an issue for them; the coordinator should ask once for this loop. No issue was created.

## Reviser brief
Blocking finding ids: F1.
- Revise only text a blocking finding names (here the Phase 1 scope sentence and AC-1.1, and the lines that assign `## Unattended mode` sections to phases).
- Add no rule, mechanism or section that no blocking finding calls for; each added paragraph or table cites its finding id.
- Prefer deleting or narrowing to adding; report the byte size before and after, and the bytes added and deleted per finding id.
- Leave Medium and minor findings (M1-M15, N1-N5) alone, including through "apply all findings".
- Do not award yourself a PASS.

verdict: FAIL

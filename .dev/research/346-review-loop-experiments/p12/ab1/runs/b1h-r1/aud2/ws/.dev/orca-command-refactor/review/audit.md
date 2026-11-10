review: 1 of 3

# Spec-panel audit: orca-worker-contract-spec.md (whole-document first review)

- command: `/sc:spec-panel @.dev/orca-command-refactor/specs/orca-worker-contract-spec.md --mode critique --focus requirements,architecture`
- candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`, sha256 `1a2d2f425ac57ef3f2392d0bfdf09996e8bf26606b0e7b94ee731ab5d177867d`
- baseline: not given (`--re-review` and `--baseline` both absent), so this is a first review of the full document. No baseline hash.
- reviewer model: claude-sonnet-5-5
- prompt followed: FIRST-REVIEW prompt, `~/.claude/rules/prompts/document_review_loop_prompts.md:27-32` (read in full).
- panel (focus requirements, architecture, plus Whittaker, active in every review): Wiegers (lead), Adzic, Cockburn, Fowler (lead), Newman, Hohpe, Nygard, Whittaker.
- coverage: whole document (293 lines), sections 1 to 9, Decisions and UNVERIFIED lists. Count and cross-reference checks against the three inventories. Citations into `src/`, `sk/`, `cmd/`, `CLAUDE.md`, `EVIDENCE.md` and the Orca install are not in the workspace and are marked UNVERIFIED. Only `README.md`, `inventory/commands-a.md`, `commands-b.md` and `orca-capabilities.md` could be checked. Not covered: correctness of the per-command gate descriptions in section 3 against the real command files.

## Context read first

`README.md:5-6,11-17,29-38` sets the goal (Orca on top, commands stay units of work, planning only) and the rules (cite path:line, mark unverified). The spec's README citations (`README.md:6,11-17,30,31`) match those lines.

## Verified claims (checked inside the workspace)

- Command split 10 / 27 / 6 is conserved. Inventory A has 13 needs-change and 3 coordinator-only, so 5 ready (`commands-a.md:75,87`). Inventory B has 5 ready, 3 coordinator-only and 14 needs-change (`commands-b.md:280,282,289`). 5+5=10, 13+14=27, 3+3=6, and 21+22=43 (`commands-a.md:3`, `commands-b.md:3`). The section 3.1 table lists 10 rows, the 3.2 table 27 rows, and section 4 lists 6 rows. Consistent.
- Capability citations spot-checked: depth 1 and refusal text (`orca-capabilities.md:97-99`), no heartbeat while blocked in `ask` (`:64`), outcome flags (`:72-73`), `worker_done` only from the dispatched pane (`:76`), failed report does not trip the circuit breaker (`:80`), waiting worker is "healthy" (`:52,129`), heartbeat cadence from the preamble (`:130`). Each matches the spec's use of it.
- Inventory citations spot-checked: `commands-a.md:90,95,96,106,113,118,120`, `commands-b.md:285,286,292,294,296,301,311,320,323`. Each supports what the spec cites it for.

## === REQUIREMENTS ANALYSIS ===

### F1. CRITICAL-to-blocking (graded MAJOR, blocking): acceptance check AC-1.1 cannot pass at the end of Phase 1
- Expert: Wiegers (testability, traceability), Adzic.
- Grading sentence: an implementer who follows the stated text as written builds a Phase 1 that is checked by AC-1.1 (every command in sections 3.1 and 3.2 has a `## Unattended mode` section naming `return-contract.yaml` and `~/.claude/WORKER-CONTRACT.md`, and no section-4 command has one), and the check is wrong because the same document makes three of those commands impossible or out of phase at P1.
- Stated texts that contradict each other:
  1. AC-1.1 asserts the section on all of 3.1-3.2 (spec:203) and says a phase passes only when every check in its block passes (spec:167). Phase 1 scope says the `--unattended` flag is accepted by "every command in sections 3.1 and 3.2" (spec:159).
  2. The section 3.2 table assigns 17 of the 27 rows to P2, P3 or P4 (for example auggie-review P2 at spec:100, roadmap P3 at spec:118, implement P4 at spec:109, post-release P4 at spec:113, pr-submit P4 at spec:114), and says later phases do not start until the earlier phase passes (spec:154). Under that order a P1 pass needs the P2-P4 sections, but P4 waits on user decisions D2-D4 while "Phases 1-3 need no user decision" (spec:154, 233).
  3. `/sc:load` is in 3.2 with report "none", "use it as a step inside another worker's brief, not as its own Task", and phase "P1 (usage line only)" (spec:112). The Decisions table says a report file would be an "unrequested addition" (spec:273). AC-1.1 would require it to have a section naming `return-contract.yaml`.
  4. Recommended D3(a) says pr-submit stays coordinator or person only, "no pr-submit changes in Phase 4" (spec:248). AC-1.1 would require pr-submit (a 3.2 row, spec:114) to carry the section, while section 4 says commands outside the worker set get none (spec:128).
- Wrong outcome: the P1 gate either fails permanently or forces an implementer to add contract sections to load and to a pr-submit the user has not agreed to make a worker, and to commands whose behaviour is still undecided.
- Recommendation (narrow, do not add): scope AC-1.1 and the P1 "flag accepted by" sentence to the commands the phase actually edits (the P1 command list at spec:159 plus the 3.1 ready rows), and state that load, and pr-submit under D3(a), carry no section. Each later phase's own check then asserts its commands.
- Priority: High. Quality impact: Testability 6 to 8.

## === ARCHITECTURE ANALYSIS ===

No blocking architecture finding. The central decision (Orca coordinates, commands stay units, no Orca calls inside commands) is consistent: E1-E6 (spec:19-26), the rejection reasons R1-R5 (spec:31-37), WC-8, SA-2 and non-goal 1 agree with each other and with `orca-capabilities.md:97-103,155,158`. Fowler: a single shared contract file with thin per-command sections is a sound segregation (spec:52). Hohpe: the contract is a file mailbox plus `worker_done` pointer, which matches Orca's pointer-only `--report-path` (`orca-capabilities.md:79`). Nygard and Whittaker items are below as Medium.

## Guard Condition Boundary Table

Guards found: WC-1 readiness limit, WC-3 `ask` timeout, WC-5 outcome mapping, WC-10 wait size, WC-2 task confidence threshold (spec:121), depth guard (WC-8), circuit breaker (WC-6), SA-3 flag guard. Classes left out: Zero/Empty for the depth and circuit-breaker guards (a count of 1 and 3 is fixed by Orca, no empty case); Maximum for WC-1 (set by Orca, `orca-capabilities.md:54` unverified bound).

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|---|---|---|---|---|---|---|
| wait split (WC-10) | spec:68 | Typical | tool call 10 min | split required | split into waits of at most 4 min | OK |
| wait split (WC-10) | spec:68, 218 | Legitimate Edge Case | tool call 4 to 5 min | not triggered (needs more than 5) | WC-10 allows it; AC-4.3 fails any call over 240 s | GAP (M2) |
| outcome mapping (WC-5) | spec:63 | Zero/Empty | no report file | failed | `--outcome failed` | OK |
| outcome mapping (WC-5) | spec:63 | Legitimate Edge Case | stale contract left by the first attempt, retry crashes before writing | reads stale status | not specified | GAP (M1) |
| outcome mapping (WC-5) | spec:63 | Sentinel Value Match | `status: partial` | succeeded | specified, body states `partial` | OK |
| task confidence (3.2 task row) | spec:121 | Typical | 0.50 | blocked | blocked | OK |
| task confidence (3.2 task row) | spec:121 | Legitimate Edge Case | 0.70 to 0.89 | not below 0.70 | not specified for unattended mode (source rule UNVERIFIED, `sk/sc-task-protocol/SKILL.md:214` not in workspace) | GAP (M5) |
| `--unattended` token | spec:51, 236 | Divergence | passed together with an interactive flag on a 3.1 command | refusal only stated for cleanup, improve, roadmap, business-panel, explain, test | WC-2 says never prompts; refuse or ignore not stated for adversarial, brainstorm, release-split | GAP (M3) |
| ask timeout (WC-3) | spec:61 | Typical | timeout | resume same message ID | specified | OK |
| readiness (WC-1) | spec:59 | Max/Overflow | fallback 45 s or more | start fails | "well inside" not quantified, 30 s evidence only | GAP (M9, minor) |
| nested depth (WC-8) | spec:66 | One/Minimal | depth 1 | refusal | commands never call `worker-start` | OK |

Pipeline Dimensional Analysis: not triggered (no multi-stage data pipeline). The only count flow, the 43-command split, is conserved (see Verified claims).

## Follow-up candidates (Medium and minor; none blocks, none enters the Reviser brief)

### Medium
- **M1. Stale or missing contract on a crashed or retried run** (Nygard, Whittaker sequence attack). WC-4 says the contract is written on every outcome (spec:62), WC-5 says "no report exists" maps to failed (spec:63), WC-6 allows resume into the same on-disk directory (spec:64). A hard crash (context exhaustion, killed pane) writes nothing, and a same-directory retry can leave the first attempt's `status: succeeded` in place. The text needs a guess to go wrong, so Medium. Suggest one sentence: write the contract with `status` unset at start, or record a run id the coordinator compares.
- **M2. WC-10 trigger and limit disagree** (Crispin). WC-10 splits calls "longer than 5 minutes" into waits of at most 4 minutes (spec:68); AC-4.3 and the pr-submit row fail any call over 240 s (spec:114, 218). A 4 to 5 minute call is compliant with WC-10 and fails AC-4.3.
- **M3. `--unattended` plus an interactive flag on ready commands** (Whittaker). Refusals are listed for six commands in 3.2; for adversarial, brainstorm, release-split the brief only "never" passes `--interactive` (spec:83,84,89). Behaviour if both appear is not stated.
- **M4. Flag accepted before its gate logic exists** (Whittaker sequence attack). Section 2.3 puts `--unattended` in every brief from Phase 1 on (spec:73) and P1 makes it "a no-op where a command has no gate" (spec:159), but tdd, troubleshoot, reflect, release-split gates arrive in P2 (spec:88-91). Dispatching one between P1 and P2 stalls silently. Suggest: the brief template lists the phase from which each command's gates are converted.
- **M5. Task confidence 0.70 to 0.89 in unattended mode** (see table). UNVERIFIED against the skill.
- **M6. Requirements with no acceptance check** (Wiegers, Crispin). WC-3 (ask path), WC-6 (retry-of), WC-11 (only save in AC-3.4), WC-12 have no AC. AC-2.2 expects `--outcome failed` on a gate while WC-3 lets the worker `ask` instead (spec:61, 208), so the run's outcome depends on a worker choice the AC does not control.
- **M7. AC-C5 versus the Usage line** (Fowler). SA-4 and AC-C5 forbid removed or changed lines (spec:149, 176), but the spec never says where `--unattended` is documented; editing an existing Usage line is a `-` line in `git diff -U0` and fails AC-C5. State that it goes on a new line.
- **M8. `--output` type unstated for P2 and P3 rows** (Cockburn). AC-1.2 fixes `--output <dir>` versus `--output-dir` for P1 only (spec:204). Rows such as spec-panel ("add `--output`", spec:120) and tdd/init-lite (file-valued, spec:62,87,90) mix file and directory meanings; the contract path differs by type (spec:62).

### Minor notes
- **M9.** WC-1 "well inside the readiness limit" is unquantified; only the 30 s precedent is given (spec:59).
- **M10.** Review-trail tags `[M1]`, `[N2]`, `[M9]` and the task id `task_1376c0449d24` remain in normative text (spec:3, 61, 62, 79, 83-92, 158, 172, 190, 193, 202); a reader of the final spec cannot resolve them. Harmless to behaviour.
- **M11.** Section 1.1 says commands contain no Orca calls; the pr-submit row names `ask` and `escalation` as the worker's options (spec:114). Allowed by SA-2 only as a contract-file example; reword to keep it out of the command file.
- **M12.** Citations to `src/`, `sk/`, `cmd/`, `CLAUDE.md`, `HOW-WE-WORK.md:171,249,254`, `Makefile:68-74`, `pyproject.toml:38`, `install_core.py:13-24`, `EVIDENCE.md` and the Orca install are UNVERIFIED here (not in the workspace). The spec's own statement that it re-read 11 locations and that a validator re-read about 340 citations (spec:11, 293) is also UNVERIFIED.

## Quality assessment (0 to 10)

Clarity 8, Completeness 7, Testability 6 (F1, M6), Consistency 7 (F1, M2, M4).

## Overrides

No brief clause overrode this command's scope. The brief asked for whole-document first review per the FIRST-REVIEW prompt; applied as written.

## Reviser brief

Blocking finding ids: F1.

Rules (restated from the command's Review Loop, bullet 6; the reviser reads this report, not the command):
- Revise only text finding F1 names (AC-1.1 at spec:203, the P1 scope sentence at spec:159, and the load and pr-submit rows only as far as F1 requires).
- Add no rule, mechanism or section that F1 does not call for. Cite `F1` on every added paragraph or table.
- Prefer deleting or narrowing to adding.
- Report the byte size of the candidate before and after, and the bytes added and deleted per finding id.
- Leave Medium and minor findings (M1 to M12) alone.
- Return the candidate once and do not award a PASS.

verdict: FAIL

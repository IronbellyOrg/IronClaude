review: 1 of 3

# Whole-document audit: orca-worker-contract-spec.md

- Command: `/sc:spec-panel @.dev/orca-command-refactor/specs/orca-worker-contract-spec.md --mode critique --focus requirements,architecture` (labelled whole-document audit, first review; FIRST-REVIEW prompt of `~/.claude/rules/prompts/document_review_loop_prompts.md:27-32`, read in full).
- Candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`, sha256 `9cef9de023524eef0ec002f54d934b470019f03f17a77205bff3ed6600c2b9c7` (293 lines).
- Baseline: none given (neither `--re-review` nor `--baseline`), so this is a first review of the full document.
- Reviewer model actually used: claude-sonnet-5-5.
- Mode: critique; no `--unattended`, so the user is asked once whether to open an issue for the follow-up candidates (question recorded at the end, nothing created).
- Evidence limits: only `.dev/orca-command-refactor/README.md` and `inventory/*.md` exist in the workspace. Every citation to `src/...`, `CLAUDE.md`, `EVIDENCE.md`, `pyproject.toml`, `Makefile` or the installed skills is UNVERIFIED here unless an inventory line quotes it.

## What I covered
All 293 lines. Counts (21+22=43; 10+27+6=43; per-phase split 9/11+4/4/3 of the 27) re-derived from sections 3.1, 3.2, 4 and 6 and matched `commands-a.md:3,73` and `commands-b.md:3`. Every `CAPS:` citation I relied on (44-47, 52, 58, 64, 66, 68, 72-80, 86, 92, 97-103, 107, 115-116, 128-130, 145-151, 155-161, 178-188) was opened and matches what the spec says it supports. `INV-A:76-83, 90-98, 106, 113, 118, 120` and `INV-B:272, 285-299, 311, 320, 323` were opened. Requirements (WC-1..12, SA-1..6, D1..D5), the rollout (section 6) and the acceptance checks (section 7) were cross-checked against section 3.

## Panel (critique, requirements and architecture focus)
Wiegers (lead), Adzic, Cockburn, Fowler (lead), Newman, Hohpe, Nygard, plus Whittaker (always active) in the fixed order of the command. Fowler's pipeline heuristic does not trigger: the spec describes no multi-stage count-changing data flow, so no Quantity Flow Diagram is produced.

## Grading rules applied
Blocking only when the sentence "An implementer who follows the stated text as written builds X, and X is wrong because Y" holds with no further assumption (`document_review_loop_prompts.md:31`). Requirements the document never states, or readings that need a guess, are Medium and go under follow-up candidates.

## Guard Condition Boundary Table
Guards in the spec: G1 outcome mapping (WC-5), G2 wait size vs heartbeat (WC-10), G3 readiness limit (WC-1), G4 nesting depth (WC-8), G5 additive-edit check (AC-C5). Classes left out are noted per guard.

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|---|---|---|---|---|---|---|
| G1 report parses and status in {succeeded, partial} | spec:63 | Zero/Empty | report missing or empty | false | `--outcome failed` | OK |
| G1 | spec:63 | Typical | `status: succeeded` | true | `--outcome succeeded` | OK |
| G1 | spec:63, 81-91 | Legitimate Edge Case | ready command with no contract writer (init-lite, spec:87) | false | Report is a markdown file, so WC-5 forces `failed`; spec:79 says the worker "reports the named file" | GAP (F1) |
| G1 | spec:62, 63 | Sentinel Value Match | existing contract whose `status` word is not one of the four | false | "counts as `failed`" for commands that "keep their fields" | GAP (M1) |
| G2 wait <= 4 min | spec:68 | Maximum/Overflow | single call > 5 min | n/a | split into <= 4 min waits | OK |
| G2 | spec:68, 114 | Legitimate Edge Case | pr-submit poll script runtime | unknown | explicitly UNVERIFIED (spec:291) | OK (declared) |
| G3 readiness 60 s | spec:59 | Maximum/Overflow | prompt fallback above ~45 s | false | fails again (`EVIDENCE.md:56`, UNVERIFIED here) | OK |
| G4 depth 1 | spec:33, 66 | Legitimate Edge Case | depth-1 worker calls `task-create` | unknown | WC-8 forbids either way | OK |
| G5 `^-[^-]` | spec:176, 201 | Legitimate Edge Case | deleted markdown bullet `- item` (diff line `-- item`) | no match | check passes | GAP (M2) |
| G5 | spec:176 | Zero/Empty | deleted blank line (diff line `-`) | no match | check passes | OK (harmless) |

Classes One/Minimal and Sentinel Collision were left out for G2-G4: a single-unit wait and a sentinel do not exist for those guards. The table is complete, so synthesis is not blocked.

## === REQUIREMENTS ANALYSIS ===

### F1 (MAJOR, blocking) Ready commands with "None" fixes cannot satisfy WC-4/WC-5; init-lite is always reported failed
- Experts: Wiegers (traceability), Nygard (Correctness shift not active; failure-mode view), Whittaker (Divergence Attack).
- Attack: I can break this specification by **Divergence Attack**. The invariant at **spec:63 (WC-5)** fails when **a ready command that never gets a contract finishes successfully**. Concrete attack: `/sc:init-lite --output ctx.md` runs in a worker; INV-A says its only output is the marked report `.dev/superclaude/context-audit.md` or `--output` (`commands-a.md:55`). Spec row `init-lite` has "Small fix: None" (spec:87). Section 3 intro says ready commands "with no fix get neither" the flag nor the `## Unattended mode` section (spec:76), and the P1 row (spec:159) lists no contract work for init-lite. State trace: before: report exists, no `return-contract.yaml`; the worker follows spec:79 and reports the markdown file; WC-5 (spec:63) says a report that does not parse as a contract, or has no `status`, gets `--outcome failed`. After: a successful audit is recorded as `failed`, the circuit breaker is not tripped (`orca-capabilities.md:80`) but the coordinator sees a failure and may start a retry (`spec:64`).
- Sentence: An implementer who follows the stated text builds an init-lite that writes no contract, and that is wrong because spec:63 turns every successful run into `--outcome failed`, contradicting spec:79 ("run as workers now ... reports the named file until Phase 1 adds the contract") given that no phase ever adds one (P1 spec:159 and P2 spec:160 omit init-lite).
- Same defect, weaker evidence, for brainstorm ("None", spec:84): its contract exists at `<output>/return-contract.yaml` (`commands-a.md:39`) but nothing read shows it has `command`, `report_path`, `artifacts` or a four-value `status` (see M1).
- Recommendation: either give init-lite (and any ready command without a verified contract) the `## Unattended mode` section and a contract in a named phase, or state in WC-5 which report forms a worker may report without a contract and how they map to an outcome. Priority High. Quality impact: Completeness and Consistency each about -1.

## Medium findings (warnings, follow-up candidates)

### M1 (MAJOR label, Medium) Existing contract vocabularies are unchecked against WC-4/WC-5
Spec:62 says commands that already write a contract "keep their fields and add the missing ones" while spec:63 maps any status outside the four words to `failed`. The inventory shows only the path and a few fields of workflow's contract (`commands-b.md:272`, `status`, `plan_path`, `reflect_report_path`) and does not list the status values of workflow, reflect, brainstorm or adversarial. A guess is needed that their words match the four-word set, so Medium. Wiegers: traceability of the status set to existing producers is missing. Priority Medium.

### M2 (MINOR label, Medium) AC-C5 and AC-0.3 regex is blind to deleted list items
`grep -E '^-[^-]'` on `git diff -U0` (spec:176, 201) misses a removed markdown bullet, whose diff line starts `--` (for example `-- item`). Command files are bullet-heavy, so SA-4's "edits are additive" check can pass while a bullet is deleted. AC-0.3 is fine for table rows (they begin `|`). Suggest `grep -E '^-' | grep -v '^---'`. Crispin/Whittaker.

### M3 AC-1.2 is not runnable as written for three P1 commands
Spec:204 requires `--unattended --output <dir>` "on each P1 command", but load takes neither (spec:76, 112), cleanup-audit has a fixed output dir (spec:85, 69) and index-repo has no output flag (spec:86). AC-1.1 (spec:203) excludes load explicitly; AC-1.2 does not. Needs a guess that the implementer skips them, so Medium.

### M4 Step 5 of 7.2 can false-fail
Spec:192 says to "search the transcript for `AskUserQuestion`". A loaded skill file mentions that word (for example adversarial's interactive checkpoints, `commands-a.md:35`), so a text search can hit without any tool call. The pass condition should say tool call, not string.

### M5 Authorization mechanism for outward actions is stated but not defined
WC-9 (spec:67) turns outward actions on only through "the command's own explicit flag", and "where the command has no such flag, the action stays off". pr-submit, post-release and task `commit`/`push` have no such flag named in section 3 (spec:113, 114, 121), yet D3(b) and D4(a) (spec:249, 253) assume a brief can authorize them. Until D3/D4 are decided (P4 waits for them, spec:154), the text is consistent only by deferral; the missing flag design is a requirement the document never states. Nygard.

### M6 save has no output path
WC-4 requires a report path known before dispatch (spec:62); the save row says "contract naming the file written" with no output flag (spec:119). The coordinator cannot know where to read it.

### M7 Reconciliation direction undecided for roadmap and validate-roadmap
Spec:118, 124 say "reconcile" without choosing which side is truth; AC-3.1 (spec:212) passes under either choice, so the acceptance check cannot catch the worse choice. Phases 1-3 are said to need no user decision (spec:154).

### M8 E4 and 1.4(3) disagree on how firm the subagent claim is
E4 (spec:24) says Agent-tool subagents "are not counted by Orca's nesting limit" as fact; 1.4(3) (spec:45) and `orca-capabilities.md:155,186` say no Orca limit was found and the behaviour is UNVERIFIED. Wording only.

### M9 Section 3.1 intro wording
Spec:79 says ready commands report their named file "until Phase 1 adds the contract", but tdd, troubleshoot, release-split and reflect get theirs in P2 (spec:88-91, 160), and init-lite and brainstorm never (F1).

## === ARCHITECTURE ANALYSIS ===
The decision (coordinator on top, commands as units, no Orca calls in commands) is well supported: R1-R5 (spec:31-37) each trace to `orca-capabilities.md` lines I opened (97-103, 147-150, 145). The evidence gap is declared honestly (spec:42-45) and P0 tests the decision before building on it (spec:158, AC-0.4 at spec:202). Fowler/Newman/Hohpe found no boundary violation; the shared contract file with per-command sections is a sound single-responsibility split. The only architectural gaps are those in F1, M1 and M5.

## Minor notes (no verdict effect)
- WC-7's evidence cites `INV-A:95` for "nesting loses tools at Claude Code's depth limit"; the line does say so (depth limit, fan-out commands lose Agent), but the fuller statement is at `commands-a.md:14`.
- D5(b) (spec:260) calls R1 a "protection against runaway fan-out"; R1 (spec:33) is about the depth refusal, not fan-out volume.
- Item 14 of "UNVERIFIED items" (spec:293) is a verification record, not an unverified item.
- UNVERIFIED in this sandbox: all `CLAUDE.md:N`, `src/...`, `sk/...`, `cmd/...`, `EVIDENCE.md:N`, `pyproject.toml:38`, `Makefile:68-74` and `install_core.py` citations, and the spec's own claims at spec:11 and spec:293 that they were re-read.

## Follow-up candidates
M1, M2, M3, M4, M5, M6, M7, M8, M9 and the minor notes above. Question for the user (once per loop): open an issue for these follow-up candidates? No issue was created.

## Reviser brief
Blocking finding ids: F1.
Rules for the reviser (restating the command's Reviser contract): revise only text finding F1 names; add no rule, mechanism or section that no blocking finding calls for; cite the finding id on each added paragraph or table; prefer deleting or narrowing to adding; report the byte size before and after, and bytes added and deleted per finding id; leave Medium and minor findings alone; return the candidate once and do not award yourself a PASS.

verdict: FAIL

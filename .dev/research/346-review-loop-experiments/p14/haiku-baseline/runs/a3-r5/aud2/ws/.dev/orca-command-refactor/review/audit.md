review: 1 of 3

# Whole-document audit of `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`

- Command: `/sc:spec-panel @.dev/orca-command-refactor/specs/orca-worker-contract-spec.md --mode critique --focus requirements,architecture` (labelled whole-document audit, first review, FIRST-REVIEW prompt of `~/.claude/rules/prompts/document_review_loop_prompts.md:27-32`).
- candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`, sha256 `5dc5c21ad2cf82fb9524020aa4cd5b0bc6a285be451e62fe6377194b27c70222`
- baseline: none given (first review of the full document; no `--re-review`).
- reviewer model actually used: claude-sonnet-5-5
- Notation: `SPEC:N` = line N of the candidate; `CAPS:N` = `inventory/orca-capabilities.md`; `INV-A:N` / `INV-B:N` = `inventory/commands-a.md` / `commands-b.md`; `README:N` = `.dev/orca-command-refactor/README.md`.
- Coverage: whole candidate read (292 lines); README read; the three inventories read at every line the candidate cites for the claims graded below (CAPS 8-24, 40-165, 177-188; INV-A 1-16, 35-55, 60-68, 74-120; INV-B 31-52, 65, 105, 276-323). I did not trace every one of the roughly 340 citations. Sources under `src/`, `.dev/evals/`, `.dev/codegraph-migration/`, `CLAUDE.md`, `~/.claude/commands` and `~/.claude/skills` are outside the sandbox, so every candidate citation that points only there is UNVERIFIED here (this includes SPEC:11, 22-23, 25, 33-34, 52, 59, 62, 65, 68-69, 83-125 evidence columns, 146-151).
- Grading rule used: grade by consequence (`command.md:259`). Blocking = a sentence "An implementer who follows the stated text as written builds X, and X is wrong because Y" holds with no further assumption (`document_review_loop_prompts.md:31`).

## Panel (fixed order, `command.md:103-113`)

Experts engaged: Wiegers, Adzic, Cockburn, Fowler, Nygard, Whittaker, Newman, Hohpe, Crispin, Gregory, Hightower. Focus areas requirements (Wiegers lead, Adzic, Cockburn) and architecture (Fowler lead, Newman, Hohpe, Nygard) per `command.md:131-151`. Whittaker is active in every panel (`command.md:83`).

Overall: the decision (Orca coordinates, commands stay units of work, SPEC:13-45) is well supported by the inventories I could check, the 10/27/6 split matches both inventories (INV-A: 5 ready + 13 needs-change + 3 coordinator-only; INV-B: 5 + 14 + 3; SPEC rows 3.1 = 10, 3.2 = 27, section 4 = 6), and the phase lists in SPEC:159-162 match the Phase column of SPEC:99-125. The blocking defects below are in the acceptance checks and in an internal contradiction between a table row and a test, not in the decision.

## Findings index

| Id | Bucket | Severity (label) | Grade | Where |
|---|---|---|---|---|
| B-1 | Requirements | MAJOR | Blocking | SPEC:176, 199 |
| B-2 | Requirements | MAJOR | Blocking | SPEC:62, 84, 112, 159, 201 |
| M-1 | Architecture | MAJOR | Medium | SPEC:158, 172, 178-182, 147, 150 |
| M-2 | Architecture | MAJOR | Medium | SPEC:62, 73, 83, 85, 87, 90 |
| M-3 | Requirements | MINOR | Medium | SPEC:22, 69 |
| M-4 | Requirements | MAJOR | Medium | SPEC:73, 186, 200 |
| M-5 | Requirements | MINOR | Medium | SPEC:85, 69 |
| M-6 | Requirements | MINOR | Medium | SPEC:76, 139, 246-248 |
| N-1 | Requirements | MINOR | Minor | SPEC:200 |
| N-2 | Requirements | MINOR | Minor | SPEC:72 |
| N-3 | Architecture | MINOR | Minor | SPEC:15, 1.4 vs README:13 |

## === REQUIREMENTS ANALYSIS ===

### B-1 (blocking) The "additive edits only" checks cannot see deleted bullet lines
- Expert: Wiegers (testability), Whittaker (FR-2.1 degenerate input attack).
- Stated text: AC-C5 (SPEC:176) and AC-0.3 (SPEC:199) pass when `git diff -U0 ... | grep -E '^-[^-]'` prints nothing, and SPEC:176 reads this as "edits are additive" and SPEC:199 as "no existing routing row changed".
- An implementer who follows the stated text as written builds a check that stays silent when a markdown bullet line is deleted, and that check is wrong because a deleted line `- foo` appears in a unified diff as `-- foo`, whose second character is `-`, so `^-[^-]` does not match it. Demonstrated in the sandbox: `printf -- '-- a deleted bullet\n-x changed\n' | grep -E '^-[^-]'` printed only `-x changed`; exit 0, the bullet deletion was not reported. Command files and routing guides are bullet-heavy, and a deleted `---` frontmatter delimiter also escapes. SA-4 (SPEC:149), SA-5 (SPEC:150) and AC-C5 are the only mechanism that enforces "additive", so a phase can pass with existing lines removed. The spec already fixed the same class of mistake in AC-C1 (F-02, SPEC:178), so this is an unreviewed copy of the defect.
- Recommendation (narrowest): match removed lines by diff header exclusion instead of by second character, e.g. `grep -E '^-' | grep -vE '^---[[:space:]]'`, or use `git diff --numstat` deleted-count equals 0 for the file; keep the sample-line gate test next to the F-02 fixture.
- Priority: High. Quality impact: the additive guarantee (SA-1, SA-4) becomes unenforced.

### B-2 (blocking) AC-1.1 requires a section that the `load` and `brainstorm` rows say will not exist
- Expert: Wiegers (traceability), Cockburn (who is served), Adzic (the test is the example).
- Stated texts that contradict each other:
  1. AC-1.1 (SPEC:201): the test asserts that EVERY command in sections 3.1-3.2 has a `## Unattended mode` section naming `return-contract.yaml` and `~/.claude/WORKER-CONTRACT.md`.
  2. WC-4 (SPEC:62) exempts `load` ("writes no file"); its row (SPEC:112) says report "none", change "P1 (usage line only)"; P1 scope (SPEC:159) both lists `load` as "usage line only" and says the flag is accepted by every command in 3.1 and 3.2.
  3. The `brainstorm` row (SPEC:84) lists "Small fix: None" and a contract that already exists, while SPEC:76 says every changed command gains the section and AC-1.1 requires it for every 3.1 command.
- An implementer who follows the load row builds a usage-line fix only, and the spec's own test AC-1.1 then fails on `load`, so P1 cannot pass; an implementer who follows AC-1.1 adds to `load` a section naming `return-contract.yaml`, a file the same spec says `load` must not write. The spec does not say which text wins.
- Recommendation: make AC-1.1 enumerate its set ("every command in 3.1-3.2 except `load`", or require `load` only to name the exemption), and change the `brainstorm` "None" to "section only".
- Priority: High. Quality impact: P1 acceptance is unsatisfiable as written.

### M-4 (Medium) The live check requires `--unattended` in the brief, but P0 runs commands that do not accept it yet
- Expert: Cockburn, Crispin.
- SPEC:73 says the brief states "the exact command line including `--unattended`"; SPEC:186 builds the brief "per section 2.3"; AC-0.4 (SPEC:200) lists three command lines without `--unattended`, and P0 (SPEC:158) makes no command edit while the flag is accepted only from P1 (SPEC:159).
- This is Medium, not blocking: it needs the guess that an implementer adds the flag in P0 and the command rejects or ignores it; the AC-0.4 command lines are explicit and win on a careful reading. Say in SPEC:73 that P0 briefs omit `--unattended`.

### M-3 (Medium) Two load-bearing citations do not say what the spec says they say
- Expert: Wiegers (traceability).
- SPEC:22 (E2) cites `CAPS:161` for "`[H:worker-start]` line 38, `--agent claude`". `CAPS:161` is the pr-submit top-level paragraph; the only `[H:worker-start]` lines in CAPS are 30, 39, 40, 44, 48 (CAPS:45, 51, 136, 140, 46). Line 38 of worker-start is not quoted in CAPS. The claim (a worker is a top-level Claude session) is still supported by the other half of the cell (`EVIDENCE.md:45`, UNVERIFIED here, and `INV-A:13`, which does state it).
- SPEC:69 (WC-11) cites `CAPS:115` for "`[G:placement]` lines 8-11: workers share the current worktree by default". `CAPS:115` is the "worktrees are never deleted" bullet and contains no placement statement; `grep -n 'lines 8-11\|share the' orca-capabilities.md` finds nothing. The shared-worktree premise is what makes WC-11 and the "worktree placement" duty in SPEC:73 necessary, so it should be marked UNVERIFIED or cited to a line that exists. Medium because the requirement is safe under either reading.

### M-5 (Medium) cleanup-audit "per-run slug" has no flag
- Expert: Wiegers, Nygard (FR-14.3 style: unspecified state), Whittaker.
- SPEC:85 says the output dir is fixed today and "under `--unattended` the output path carries a per-run slug the coordinator passes", but the row's "Brief must pass" column lists only `--pass <N>`, and neither this row nor WC-4 (SPEC:62) names the flag that carries the slug. Two runs in one worktree would share `.claude-audit/progress.json` until it is named. Requirement the document never states, hence Medium.

### M-6 (Medium) D3 recommendation and the totals disagree
- Expert: Cockburn.
- SPEC:76 and SPEC:139 count `pr-submit` among the 27 worker-capable commands, and SPEC:246-248 recommends D3 (a): coordinator or person only, "no pr-submit changes in Phase 4". If the recommendation is taken the split is 10 / 26 / 7 and P4 (SPEC:162) shrinks. SPEC:139 half-states this. Needs a guess about which reading the user takes, so Medium.

## === ARCHITECTURE ANALYSIS ===

### M-1 (Medium) AC-C1 scans `core`, where P0 puts the Orca text it forbids
- Expert: Fowler (single responsibility of the check), Newman (boundary), Whittaker (FR-2.3 sentinel collision: the check pattern collides with the spec's own deliverables).
- Stated texts: P0 writes `src/superclaude/core/WORKER-CONTRACT.md` and adds "an Orca section to `HOW-WE-WORK.md`" (SPEC:158, 150); SA-2 allows Orca mentions "inside the contract file" (SPEC:147); AC-C1 (SPEC:172, 181) scans `src/superclaude/core` for `orca(-ide)? (orchestration|worktree|terminal|agent)` and excludes only `ccsession-tag`, and must print nothing in every phase.
- If the contract file or the routing section names an Orca verb in the form the pattern matches (for example the `ask` command, or `orca worktree create` as `CLAUDE.md` itself writes it), P0's own AC-C1 fails. E5 (SPEC:25) reports `grep -ci orca HOW-WE-WORK.md` = 0 today, so the baseline is clean, but the allowed content is not reconciled with the check. Medium: it needs the guess that the new text uses that wording.
- Recommendation: exclude `core/WORKER-CONTRACT.md` and the new HOW-WE-WORK section from AC-C1, or restrict AC-C1 to `commands`, `skills`, `agents`.

### M-2 (Medium) WC-4's path rule does not describe where several contracts land
- Expert: Hohpe (message exchange contract), Fowler (interface consistency), Nygard (collision under parallel writes).
- WC-4 (SPEC:62) says the contract is `<output-dir>/return-contract.yaml` and 2.3 (SPEC:73) promises the coordinator knows the report path before dispatch from the output directory. The rows then place it elsewhere or leave it undefined: `adversarial` at `<output>/adversarial/return-contract.yaml` (SPEC:83; `INV-A:35` shows deliverables under `<output>/adversarial/`), `cleanup-audit` beside `pass<N>-summary.md` in `.claude-audit/` (SPEC:85), and `tdd`, `init-lite`, `spec-panel` where `--output` is a file ("beside" it, SPEC:87, 90; `--output <file>` at INV-B:47 and INV-A:55), so there is no `<output-dir>`. Two `tdd` workers whose `--output` files share a folder would write one `return-contract.yaml` (WC-11 forbids this, SPEC:69, but the row gives no slug).
- Medium because each row states its own location and a careful coordinator reads the row. Add one sentence to WC-4 that the section 3 row decides the path and that a file-valued `--output` uses `<output-file-stem>.return-contract.yaml`, or similar, to keep names unique.

## Checks required by the command

### Guard Condition Boundary Table (guards exist: thresholds and gates in the spec; `command.md:313`)
Input classes left out are given a one-line reason. Status GAP rows are graded under FR-8 (`command.md:332`): none names a concrete wrong outcome beyond B-1, B-2, so the GAPs below are Medium and are carried to follow-up candidates.

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|---|---|---|---|---|---|---|
| WC-10 wait split | SPEC:68 | Zero/Empty | wait of 0 s | n/a | Class left out: a zero wait does not block a heartbeat | n/a |
| WC-10 wait split | SPEC:68 | Typical | 240 s wait | true | split into waits of at most 4 min | OK |
| WC-10 wait split | SPEC:68 | Maximum/Overflow | single call of 301 s | true | split required; pr-submit iteration time UNVERIFIED (SPEC:114, 289) | GAP (UNVERIFIED runtime; Medium) |
| WC-10 wait split | SPEC:68 | Legitimate Edge Case | exactly 300 s | ambiguous | "longer than 5 minutes" splits, "at most 4 minutes" is the target; 241-300 s is not stated | GAP (minor; the 4 min rule makes it moot) |
| readiness limit WC-1 | SPEC:59 | Typical | fallback inside 30 s | true | passes (`EVIDENCE.md:56`, UNVERIFIED here; `CAPS:49`) | OK |
| readiness limit WC-1 | SPEC:59 | Maximum/Overflow | fallback above about 45 s | false | fails `agent_readiness` (CAPS:49) | OK |
| outcome mapping WC-5 | SPEC:63 | Zero/Empty | no report file exists | true | `--outcome failed` | OK |
| outcome mapping WC-5 | SPEC:63 | Sentinel Value Match | status `partial` | true | `succeeded`, body says partial | OK |
| outcome mapping WC-5 | SPEC:63 | Legitimate Edge Case | report exists but is unreadable or its `status` is not one of the four | not stated | unspecified | GAP (Medium) |
| nesting depth R1/WC-8 | SPEC:33, 66 | One/Minimal | depth 1 | true | worker may not start workers | OK |
| nesting depth R1/WC-8 | SPEC:33, 66 | Legitimate Edge Case | depth raised by the user (D5 b) | not stated | WC-8 forbids Orca fan-out regardless | OK |
| confidence guard in `task` | SPEC:121 | Sentinel Value Match | confidence exactly 0.70 | not stated | the row says "below 0.70" blocks; 0.70 itself is not stated here (INV-B:45 gives "< 0.70") | GAP (Medium, boundary is inferable) |
| `ask` timeout WC-3 | SPEC:61 | Maximum/Overflow | repeated timeouts | not stated | resume same message ID; no limit on repeats | GAP (Medium; default timeout UNVERIFIED, SPEC:287) |

FR-10 completeness: every guard enumerated in the spec's WC rows has at least one row above; guards in command-file rows of section 3 are listed there by the inventories and not re-derived here.

### Pipeline Dimensional Analysis
Not triggered. The spec describes no data pipeline whose stage output count differs from its input count (`command.md:353`). The phase plan is a staged rollout, not a filter/aggregate chain. The only count relation worth checking is 43 = 10 + 27 + 6 = 21 + 22, which holds (SPEC:76; INV-A:3, INV-B:278).

### State Variable Registry / `--focus correctness`
Not requested (`--focus requirements,architecture`). The auto-suggestion for correctness (`command.md:192`) is advisory: the spec introduces no 3+ mutable state variables, but it has numeric thresholds (WC-10, readiness); `--focus correctness` is optional.

## Minor notes

- N-1: SPEC:200 cites `SPEC:91` for the claim that troubleshoot's report is markdown. `SPEC` is not defined in the citation conventions (SPEC:7-11); the intended target is the troubleshoot row at SPEC:91 of this same file.
- N-2: SPEC:72 "Contract file ... `KNOWN_CORE_FILES` (`src/superclaude/cli/install_core.py:13-24`)" and the many `src/` citations are UNVERIFIED in this sandbox; SPEC:11 states 11 locations were re-read by the author, which I could not repeat.
- N-3: SPEC:44 (section 1.4 item 2) narrows the `EVIDENCE.md` finding that README:13 states as "a supervised Claude worker that waits on a question fails Orca's 60-second readiness limit". CAPS:49 and CAPS:52 support the narrower reading, so the spec is consistent with the checkable evidence, but README is the binding summary: the spec should say in one clause that it corrects the README wording.

## Verified in this audit (read and found as cited)

README:6, 11-17, 30-31; CAPS:44-46 (60 s, `--timeout-ms`, exit 0 only for ready), 52 and 129 (waiting worker is healthy), 58-61, 64 (ask), 66-67 (pull-only follow-ups), 72-77, 79 (report path is a pointer), 80, 92, 97-103 (depth 1), 107-113, 116, 130 (5 minute heartbeat from the preamble), 145-151, 155-160, 177-188; INV-A:13, 76-83, 90-98, 106, 112-120; INV-B:278-323; the row-by-row counts in SPEC:79-92, 99-125, 132-137.

## Follow-up candidates (Medium and minor; never trigger a revision)

M-1, M-2, M-3, M-4, M-5, M-6, the four GAP rows in the guard table (WC-10 edge, WC-5 unreadable report, `task` 0.70 boundary, repeated `ask` timeouts), N-1, N-2, N-3. Per `command.md:260` the session that ran this review asks the user once per loop whether to open an issue for these; this audit ran as a sandboxed worker with no user channel, so it creates none and only records the list.

## Reviser brief

Blocking finding ids: B-1, B-2.

Rules (restated from `command.md:263`; the reviser reads this report, not the command):
- Revise only text a blocking finding names (B-1: SPEC:176 and SPEC:199; B-2: SPEC:62/84/112/159/201 as needed to make AC-1.1 and the load and brainstorm rows agree).
- Add no rule, mechanism or section that a blocking finding does not call for.
- Each added paragraph or table cites its finding id.
- Prefer deleting or narrowing to adding.
- Report the byte size of the spec before and after, and the bytes added and deleted per finding id.
- Leave minor and Medium findings (M-1 to M-6, N-1 to N-3) alone, including through any "apply all findings" wording; return the candidate once and do not award a PASS.

Brief clauses overridden: none (the brief asked for a whole-document first review and narrowed nothing).

verdict: FAIL

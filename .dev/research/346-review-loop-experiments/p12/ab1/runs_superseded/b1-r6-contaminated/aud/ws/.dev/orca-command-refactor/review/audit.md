review: 1 of 3

# /sc:spec-panel audit (critique mode, focus requirements,architecture)

- candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`
- candidate sha256: `5c2917118a22814ab0c7a7bbdc9726f06dce161ded89ac5b03740fd58e13abc3`
- baseline: not given, none needed (first review of the whole document, labelled whole-document audit)
- reviewer model used: claude-sonnet-5-5
- coverage: whole document, all 9 sections plus Decisions and UNVERIFIED lists (spec lines 1-284). Citations to `INV-A`, `INV-B` and `CAPS` were checked against `.dev/orca-command-refactor/inventory/` (row ranges `INV-A:35-55`, `INV-B:31-52`, `INV-A:3,14,76-83,90-98,106,113,118,120`, `INV-B:3,36,107-115,205-215,272,285-301,311,320,323`, `CAPS:44-52,58-80,86,92,97-103,107-116,129-130,145-161,178-188`; all matched). Citations to `src/`, `cmd/`, `sk/`, `CLAUDE.md`, `EVIDENCE.md`, `orca-data.json` and Orca guide lines are not in the workspace: UNVERIFIED by me. The "340 citations re-read" claim (spec line 284) is UNVERIFIED.
- README read first (`.dev/orca-command-refactor/README.md:1-39`). Planning-only rules (`README.md:30`) were respected; nothing besides this file was written.
- brief clauses overridden: none.

## Grading note
Each blocking finding below carries the sentence "An implementer who follows the stated text as written builds X, and X is wrong because Y." Findings that need a guess about which reading an implementer picks, or that name a requirement the document never states, are Medium and sit under follow-up candidates.

=== REQUIREMENTS ANALYSIS ===

### R-1 [MAJOR, blocking] Phase scope and acceptance checks disagree on which ready commands get the WC-4 contract
Experts: Wiegers (lead), Adzic, Crispin. Priority: High. Quality impact: Testability 6 -> 8.

Stated texts:
- Spec line 79 (3.1 intro): ready commands report "the named file until Phase 1 adds the contract".
- Spec line 62 (WC-4) and line 73 (2.3): in unattended mode every worker writes `<output-dir>/return-contract.yaml` with `status`; the brief carries `--unattended`.
- Spec line 159 (P1 scope) lists only adversarial, cleanup-audit, index-repo and workflow among the ready commands. Line 160 (P2 scope) lists reflect, release-split, tdd, troubleshoot but says only "Each default-on gate resolves per its section 3 row"; their 3.1 rows (lines 88-91) add no contract. brainstorm (line 84) and init-lite (line 87) are in no phase at all, and init-lite has no contract today (line 87).
- Spec line 183 (7.2 step 4, "used by P0-P4"): `test -s <contract>` and a YAML assertion on `status` and `command`. Line 196 (AC-1.2) applies it to each P1 command, which includes cleanup-audit and index-repo whose only specified fix is to name a path (lines 85-86). Line 201 (AC-2.3) requires "7.2 passes" for every P2 command, including troubleshoot, tdd and release-split on the happy path.

An implementer who follows the stated text as written builds P1 for index-repo and cleanup-audit (state a path, add an `## Unattended mode` section) and P2 for troubleshoot, tdd and release-split (gate-to-blocked only, which writes a contract only on the blocked path), and X is wrong because AC-1.2 and AC-2.3 then fail step 4 on the happy path (no `return-contract.yaml` exists to `test -s`), while line 79 promises Phase 1 adds it. brainstorm and init-lite never get the section or the flag, yet line 73 tells the coordinator to pass `--unattended` to every worker.

Whittaker (sequence/divergence attack): I can break this specification by **Divergence Attack**. The invariant at **spec lines 62/73 vs 159-160/196/201** fails when **a ready command's happy-path run is checked by 7.2 step 4**. Concrete attack: coordinator dispatches `/sc:troubleshoot "x" --unattended` after P2; the command completes and writes `REPORT.md` only; step 4 `test -s <contract>` exits 1; phase cannot pass although the command did what the spec says.

Recommendation: state per ready command which phase adds the success-path contract (or exempt it from step 4 and name the accepted report file), and say what a coordinator passes to brainstorm and init-lite. Narrow rather than add: one sentence per affected row.

### R-2 [Medium, follow-up] `partial` and `succeeded` are never defined
WC-4 (line 62) fixes the vocabulary `succeeded|partial|failed|blocked`; WC-5 (line 63) and the Decisions table map `partial` to `succeeded`. No text says when a command reports `partial` rather than `failed` (for example `/sc:test` with failing tests, `/sc:cleanup` with deferred items). Requirement never stated; the implementer picks per command.

### R-3 [Medium, follow-up] Contract location is undefined for commands whose output is a file or a fixed path
WC-4 (line 62) puts the contract in `<output-dir>`, naming `--report-dir` only for workflow, research and tdd. Rows for init-lite (`--output <file>`, line 87), spec-panel and recommend ("add `--output`"), cleanup-audit and index-repo (fixed paths, lines 85-86) and many "add a report path" rows (lines 99-125) never say whether the new flag is a file or a directory or where the contract goes. WC-4's "known before dispatch" cannot be checked for them.

### R-4 [Medium, follow-up] WC-11 against SA-1 and SA-3
WC-11 (line 69) says default output paths carry a timestamp or slug; SA-1 and SA-3 (lines 146, 148) say default paths stay as today. The cleanup-audit and index-repo rows keep fixed paths (lines 85-86, with "one audit per worktree at a time" only in a table cell) and 2.3 (line 73) does not tell the coordinator to serialize them. WC-11 is probably meant to apply only under `--unattended`; the text does not say so.

### R-5 [Medium, follow-up] WC-1 has no work item
WC-1 (line 59) names "Launch setup, not commands" as owner, yet no phase in section 6 and no check in section 7 builds or tests it beyond 7.2 step 1. Its evidence (`EVIDENCE.md:39,45,56`) is UNVERIFIED by me, though `CAPS:49` quotes it.

### R-6 [Medium, follow-up] tasklist row replaces the inventory's remedy without noting it
Spec line 122 passes `--unattended` into each reflect, so reflect's headless auto-accept (`INV-B:107`) turns a `--remediate` offer into automatic remediation inside N subagents. `INV-B:205-215` recommended dropping `--remediate` in Stage 10.5 and running reflect at the worker's top level, and marked nested spawning UNVERIFIED. The spec states "inside Claude Code's nesting limit" (line 122) from docs, not from a run. Behavior (automatic corrective-package writes) is a choice the document does not weigh against WC-9.

=== ARCHITECTURE ANALYSIS ===

### A-1 [Verified, no finding] Core decision
Orca coordinates, commands stay units of work (spec lines 14-45). Evidence cited from the capabilities inventory matches (`CAPS:97-103` depth 1, `CAPS:147-150` identity, `CAPS:155-161` subagents). Section 1.4 states its own evidence gaps honestly and P0 tests the decision first. Fowler/Newman: no boundary violation found; WC-7/WC-8 keep lifecycle messages in one session.

### A-2 [Medium, follow-up] Acceptance checks that can misfire
- AC-C1 (line 172) greps `src/superclaude/core`, where P0 adds `WORKER-CONTRACT.md` and a `HOW-WE-WORK.md` Orca section; if either quotes an `orca orchestration ...` command the check fails on P0 itself, while SA-2 (line 147) allows such a mention only "inside the contract file". The `\|` escapes in AC-C1 and AC-C4 are table escapes; pasted into a shell they change the pattern.
- AC-2.4 (line 202) counts reviews and comments with `gh api ... --jq length` without `--paginate`; counts cap at one page (30), so a posted comment can go unseen on a busy PR.
- 7.2 step 5 searches a transcript for `AskUserQuestion`; the loaded command text can contain the word, so the pass condition needs "tool call" wording to be mechanical.

### A-3 [Minor] Counts
43 = 10 + 27 + 6 and the phase tallies (P1 9, P2 11, P3 4, P4 3 among the 27, plus 8 ready commands with fixes) reconcile with the tables. 8 of the 10 "ready" commands also receive edits, and 2 (brainstorm, init-lite) none; the "ready" label means "usable with flags", not "unchanged". D4 affects P2 rows (auggie-review, task) though line 6/section 9 says Phases 0-3 need no decision; harmless on the recommendation, contradictory if the user picks D4 (b).

=== ADVERSARIAL ANALYSIS (Whittaker) ===
- Sequence Attack on WC-12/WC-5: a worker that gets `consumer_fenced` after finishing never sends `worker_done`; the contract file exists and the coordinator never learns. Inferrable from `CAPS:66-67`; MINOR.
- Accumulation Attack on WC-10: poll waits of exactly 4 minutes plus tool overhead exceed the 5-minute heartbeat cadence only if overhead is above 1 minute; the cadence itself is UNVERIFIED (`CAPS:130`). MINOR.
- Sentinel Collision on `status: blocked` vs `--outcome failed` (line 63): a coordinator cannot tell a gate stop from a crash by outcome alone; it must open the contract, which line 62 already says. MINOR.

=== GUARD CONDITION BOUNDARY TABLE ===
Guards enumerated: WC-5 outcome mapping, WC-10 wait/heartbeat threshold, WC-1 readiness limit, WC-4 status set, D1 unattended switch. Classes left out: "One/Minimal" and "Maximum/Overflow" for WC-1 and D1 (no numeric input beyond the limit itself).

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|---|---|---|---|---|---|---|
| WC-5 outcome | spec line 63 | Zero/Empty | no report file | failed | `--outcome failed` | OK |
| WC-5 outcome | spec line 63 | Typical | `status: succeeded` | succeeded | `--outcome succeeded` | OK |
| WC-5 outcome | spec line 63 | Sentinel Value Match | `status: partial` | succeeded | succeeded, body states `partial` | OK |
| WC-5 outcome | spec line 63 | Legitimate Edge Case | audit verdict FAIL, `status: succeeded` | succeeded | succeeded | OK |
| WC-5 outcome | spec line 62 | Legitimate Edge Case | `partial` for a command with failing tests | undefined | when a command reports `partial` is never stated | GAP (Medium, R-2) |
| WC-10 wait | spec line 68 | Zero/Empty | no wait | n/a | no split needed | OK |
| WC-10 wait | spec line 68 | Typical | wait of 3 min | true | no split | OK |
| WC-10 wait | spec line 68 | Maximum/Overflow | single call of 5 min 1 s | true | split to at most 4 min | OK |
| WC-10 wait | spec line 68 | Legitimate Edge Case | wait of exactly 5 min | undefined (">5" splits, "at most 4" allowed) | boundary 4 to 5 min not stated | GAP (Medium; implementer picks the safer 4 min) |
| WC-1 readiness | spec line 59 | Typical | fallback 30 s | true | passes (`CAPS:49`) | OK |
| WC-1 readiness | spec line 59 | Maximum/Overflow | fallback 45 s or more at a 45 s start limit | false | fails again (`CAPS:49`) | OK |
| WC-4 status | spec line 62 | Sentinel Value Match | `blocked` with empty `blocked_question` | undefined | AC-2.2 requires non-empty, WC-4 only "when blocked" | GAP (Medium) |
| D1 switch | spec lines 232-237 | Zero/Empty | no `--unattended` | false | today's behavior (SA-1) | OK |
| D1 switch | spec line 73 | Legitimate Edge Case | `--unattended` passed to brainstorm/init-lite | unknown flag | not specified | GAP (blocking via R-1) |

Table is complete for the guards enumerated; Specified Behavior has no blank cell except the GAP rows above, which are graded in R-1/R-2.

## follow-up candidates
- R-2 `partial` undefined (Medium)
- R-3 contract location for file-valued or fixed-path outputs (Medium)
- R-4 WC-11 vs SA-1/SA-3 scope (Medium)
- R-5 WC-1 has no work item (Medium)
- R-6 tasklist passes `--unattended` into reflect: auto-remediation not weighed (Medium)
- A-2 acceptance checks that can misfire: AC-C1 vs P0 core edits, AC-2.4 pagination, 7.2 step 5 wording (Medium)
- A-3 D4 touches P2 rows; "ready" label vs edits (minor)
- WC-10 4-5 minute boundary; empty `blocked_question` (minor)
- The session that ran this review asks the user once whether to open an issue for these; none is created without an answer.

## Reviser brief
Blocking finding ids: R-1.
Rules for the reviser (restated from the command): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, and the bytes added and deleted per finding id. Leave Medium and minor findings alone; do not award yourself a PASS.

verdict: FAIL

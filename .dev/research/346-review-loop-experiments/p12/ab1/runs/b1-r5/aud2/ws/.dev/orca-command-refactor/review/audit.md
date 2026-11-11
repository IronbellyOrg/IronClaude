review: 1 of 3

# Whole-document audit: orca-worker-contract-spec.md

- command: `/sc:spec-panel @.dev/orca-command-refactor/specs/orca-worker-contract-spec.md --mode critique --focus requirements,architecture`
- label: whole-document audit, first review (no `--re-review`, no `--baseline`, so none is expected)
- candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`
- candidate sha256: `3cd5458f8a2ac3b837384ffb0c2d1ee1a68493aec2a3e3b821f7c0d4938d6464`
- baseline sha256: not applicable (first review)
- reviewer model used: claude-sonnet-5-5
- prompt followed: FIRST-REVIEW prompt, `~/.claude/rules/prompts/document_review_loop_prompts.md:27-32`, read in full. No brief clause was overridden.
- citation convention: `SPEC:N` = line N of the candidate. `INV-A:N`, `INV-B:N`, `CAPS:N` = lines of `inventory/commands-a.md`, `commands-b.md`, `orca-capabilities.md`. Anything outside those four files and the README is UNVERIFIED here, because the sandbox holds no `src/`, `CLAUDE.md`, `.dev/evals/` or `.dev/codegraph-migration/` files.

## Coverage statement

- Read in full: the candidate (286 lines), `README.md`, `command.md`, the review-loop prompts file.
- Read in full or in the cited ranges: `orca-capabilities.md` (CAPS:28-175, 174-188), `commands-a.md` (INV-A:3-14, 35, 44, 56-111), `commands-b.md` (INV-B:3-34, 36, 43, 45-47, 49-52, 207-215, 237-245, 267-275, 285-323).
- Checked and found as the spec cites them: the spec's `INV-A:` and `INV-B:` references to rows, notes and summary lines (3, 35-55, 62, 65, 66, 68, 76-83, 90-98, 106, 113, 118, 120; B 3, 31-52, 272, 285-286, 289-299, 301, 311, 320, 323) and its `CAPS:` references (44-46, 52, 58-61, 64, 66-67, 72-80, 84-92, 97-103, 107-116, 128-130, 135-139, 145-151, 155-161, 178-188). I found no wrong line number among them.
- Not checkable, UNVERIFIED: every `cmd/`, `sk/`, `src/`, `CLAUDE.md`, `HOW-WE-WORK.md`, `EVIDENCE.md`, `.dev/codegraph-migration/` and `pyproject.toml` citation (the spec's own "re-read 11 locations" at SPEC:11 and "340 citations" at SPEC:285 included). I did not re-derive the 10 / 27 / 6 verdicts; I only checked that the spec's counts are conserved (see the Quantity Flow Diagram).
- Focus run: requirements and architecture. Correctness focus not active, so no State Variable Registry.

## Panel

Wiegers, Adzic, Cockburn (requirements); Fowler, Nygard, Newman, Hohpe (architecture); Whittaker (always active, review order 6). Crispin, Gregory and Hightower spoke only where a requirement is untestable.

=== REQUIREMENTS ANALYSIS ===

### F-01 (blocking, MAJOR) Phase 1 scope states two different sets of commands, and AC-1.1 cannot pass against the smaller one
- Expert: Wiegers (traceability), Adzic (example), Whittaker (FR-2.2 divergence attack and FR-19 count mismatch).
- Locations: SPEC:159 (P1 row), SPEC:195 (AC-1.1), SPEC:52 (what each command section contains), SPEC:160-161 (P2 and P3 rows).
- Grading sentence: An implementer who follows the stated text as written builds Phase 1 for the 13 commands in the P1 "Commands" cell (9 from section 3.2 plus adversarial, cleanup-audit, index-repo, workflow; 12 once `/sc:load` is excluded), and that is wrong because AC-1.1 requires a `## Unattended mode` section naming `return-contract.yaml` and `~/.claude/WORKER-CONTRACT.md` on every command whose row is phased P1 to P3 except load, which is 31 commands, so the Phase 1 gate in section 7 cannot pass. The other reading (the P1 "Scope" sentence at SPEC:159, "every command in sections 3.1 and 3.2 that section 3 assigns to a phase") builds the section on 31 commands in Phase 1, and that is wrong because SPEC:52 says each section lists the command's gate resolutions, which SPEC:160-161 assign to Phases 2 and 3, and SPEC:154 says a later phase does not start until the earlier phase's checks pass.
- Concrete count trace: P1 "Commands" cell = 13 (12 without load). AC-1.1 set = 13 + 15 (P2) + 4 (P3) - 1 (load) = 31. Difference = 19 commands (the 15 P2 and 4 P3 commands). See the Quantity Flow Diagram.
- Recommendation: state one set. Delete the AC-1.1 reference to P2 and P3 commands (assert only the P1 commands), or move the section and flag for P2 and P3 commands out of the P1 scope sentence. Narrow, do not add.
- Priority: High. Quality impact: Testability and Consistency each drop about 2 of 10 until fixed.

=== ARCHITECTURE ANALYSIS ===

(no blocking finding; see follow-up candidates M-01 to M-15)

## Whittaker adversarial findings

I can break this specification by **FR-2.1 Zero/Empty Attack**. The invariant at **WC-4 (SPEC:62)** "the command writes `<output-dir>/return-contract.yaml`" fails when **`--unattended` is passed with no `--output` / `--output-dir`** (many section 3.2 rows only say "add `--output`", for example SPEC:99, 101, 106). Concrete attack: before, brief = `/sc:analyze src/x.py --unattended`; after, no output directory exists, WC-4 names no fallback, WC-5 (SPEC:63) sends `--outcome failed` only because "no report exists", and the coordinator reads no cause. Medium (M-09).

I can break this specification by **FR-2.4 Sequence Attack**. The invariant at **WC-4 / WC-6 (SPEC:62, 64)** "written on every outcome" fails when **a retry worker reuses the first attempt's output directory and dies (killed, context exhausted) before writing**. Concrete attack: attempt 1 writes `status: succeeded`; the Task is retried with `--retry-of`; attempt 2 crashes at step 2; the coordinator opens `<dir>/return-contract.yaml` and AC step 4 (`test -s`, SPEC:183) passes on attempt 1's file. Before: contract A (succeeded). After: contract A still, attempt 2 invisible. Medium (M-02).

I can break this specification by **FR-2.3 Sentinel Collision Attack**. The invariant at **section 2.1 / D1 (SPEC:51, 228)** "a person never types it" fails when **the literal token `--unattended` appears inside quoted content** (for example `/sc:tdd "parse the --unattended flag"`). The spec defines the flag as a switch but not that it counts only as a standalone argument token. Concrete attack: a person's quoted topic contains the token; the command drops every gate (WC-2) for a person at the keyboard. Medium (M-09).

I can break this specification by **FR-2.2 Divergence Attack**. The invariant at **WC-10 (SPEC:68)** "longer than 5 minutes must be split into waits of at most 4 minutes" fails when **a single wait is 270 s**: WC-10 allows it (not longer than 5 minutes), AC-4.3 (SPEC:210, "no single tool call exceeds 240 s") rejects it. Before: 270 s wait. After: conformant per WC-10, failing per AC-4.3. Medium (listed under M-08).

I can break this specification by **FR-2.5 Accumulation Attack**. The invariant at **WC-3 (SPEC:61)** "ask the coordinator once" fails when **a command has several blocked gates** (cli-portify has three approval gates, SPEC:105). "Once" is per gate or per run? Concrete attack: gate 1 asked and answered, command re-invoked, gate 2 blocks; a worker that obeys "once" ends `failed` on a gate the coordinator would have answered. Medium (listed under M-08).

## Guard Condition Boundary Table

Guards identified: G1 outcome mapping (WC-5, SPEC:63), G2 wait split (WC-10, SPEC:68), G3 unattended switch and output dir (WC-2/WC-4, SPEC:60, 62), G4 `/sc:task` confidence threshold (SPEC:121), G5 outward-action default (WC-9, SPEC:67), G6 Orca nesting depth (SPEC:33, CAPS:97-101), G7 readiness limit (WC-1, SPEC:59).
Classes left out: G6 Maximum/Overflow (depth is a setting, no capacity); G7 One/Minimal (a time limit has no minimal count); G5 Maximum/Overflow (boolean default).

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|-------|----------|-----------------|----------------|--------------|--------------------|--------|
| G1 outcome | SPEC:63 | Zero/Empty | no `return-contract.yaml` | true | `--outcome failed` | OK |
| G1 outcome | SPEC:63 | One/Minimal | contract holds only `status` (no `command`) | true | WC-5 silent; AC step 4 asserts `d['command']` (SPEC:183) | GAP |
| G1 outcome | SPEC:63 | Typical | `status: succeeded` | true | `--outcome succeeded` | OK |
| G1 outcome | SPEC:62-63 | Sentinel Value Match | existing contract status written in another vocabulary (for example `success`); not read in either inventory, UNVERIFIED | unknown | WC-4 "keep their fields" vs fixed four-value set | GAP |
| G1 outcome | SPEC:63 | Legitimate Edge Case | `partial`; audit verdict FAIL | true | `succeeded`, body states status and verdict | OK |
| G2 wait split | SPEC:68 | Zero/Empty | wait 0 s | false | no split needed | OK |
| G2 wait split | SPEC:68 | One/Minimal | wait 1 s | false | no split needed | OK |
| G2 wait split | SPEC:68 | Typical | 3 min | false | allowed | OK |
| G2 wait split | SPEC:68 | Maximum/Overflow | 3600 s eval (SPEC:104) | true | waits of at most 4 min | OK |
| G2 wait split | SPEC:68, 210 | Legitimate Edge Case | 270 s | false (WC-10) / fails (AC-4.3) | WC-10 allows, AC-4.3 rejects | GAP |
| G3 unattended | SPEC:60, 62 | Zero/Empty | `--unattended`, no `--output` | true | unspecified | GAP |
| G3 unattended | SPEC:60, 62 | Typical | `--unattended --output <dir>` | true | gates resolve, contract written | OK |
| G3 unattended | SPEC:51, 228 | Sentinel Value Match | token inside quoted argument | true | unspecified | GAP |
| G3 unattended | SPEC:60 | Legitimate Edge Case | gate resolves "blocked" and worker also holds a preamble | true | WC-3 "may instead ask"; AC-2.2 (SPEC:200) demands `failed` | GAP |
| G4 task confidence | SPEC:121 | Zero/Empty | 0.00 | true | blocked | OK |
| G4 task confidence | SPEC:121 | Typical | 0.80 | UNVERIFIED | row says only "below 0.70"; the 0.70-0.89 band behaviour is not stated here (INV-B:45 lists only "< 0.70") | GAP (UNVERIFIED) |
| G4 task confidence | SPEC:121 | Legitimate Edge Case | exactly 0.70 | false | proceeds (inferred from "below 0.70") | OK |
| G5 outward default | SPEC:67, 121 | Sentinel Value Match | `/sc:task` EXEMPT `commit`/`push`, no "command's own explicit flag" exists | true | "refused unless authorized" but the authorizing flag is undefined | GAP |
| G5 outward default | SPEC:100 | Legitimate Edge Case | `/sc:auggie-review` re-enable posting | true | "explicit `--post-pr`"; INV-A:78 names only `--no-post-pr`, so `--post-pr` is a new flag the row does not mark new | GAP |
| G6 nesting depth | SPEC:33, CAPS:97-101 | Zero/Empty | coordinator (depth 0) | false | may start workers | OK |
| G6 nesting depth | CAPS:97 | Typical | worker (depth 1), setting 1 | true | `nested_worker_depth_exceeded` | OK |
| G6 nesting depth | CAPS:100 | Sentinel Value Match | setting 0 or malformed | true | falls back to 1 | OK |
| G7 readiness | SPEC:59 | Typical | startup prompt with 30 s fallback | false | passes (EVIDENCE.md:45, UNVERIFIED) | OK |
| G7 readiness | SPEC:59, CAPS:44 | Maximum/Overflow | 45-60 s fallback | true | fails; spec says "well inside" with no number | GAP |

GAP rows: 9 above. None names a concrete wrong outcome on a stated text without an extra guess, so under FR-8 they are Medium (listed under follow-up candidates), except the count mismatch behind F-01 which is graded above.

## Quantity Flow Diagram

```text
[Source: 43 commands (INV-A 21 + INV-B 22)] --> [Classification SPEC:76]
    --> 10 ready (SPEC:81-92)   : P1 x4 (adversarial, cleanup-audit, index-repo, workflow)
                                  P2 x4 (reflect, release-split, tdd, troubleshoot)
                                  unphased x2 (brainstorm, init-lite)
    --> 27 needs change (SPEC:97-125): P1 x9 (incl. load) | P2 x11 | P3 x4 | P4 x3
    --> 6 coordinator-only (SPEC:130-137)
    Phase totals: P1 13 | P2 15 | P3 4 | P4 3 | unphased 2 | coordinator-only 6 = 43 (conserved)
        |
        v
[Consumer: SPEC:159 P1 "Commands" cell : expects 13 (12 after dropping load)]
[Consumer: AC-1.2 SPEC:196            : expects each P1 command except load = 12]
[Consumer: AC-1.1 SPEC:195            : expects P1-P3 phased commands except load = 31] <-- MISMATCH 12 vs 31 (F-01)
[Consumer: SPEC:160 P2 "Commands"      : lists 15, equals the 15 P2 rows (conserved)]
[Note: D3 option (a) removes pr-submit from P4, giving P4 = 2, ready 10 / needs-change 26 (SPEC:139 admits it)]
```

## Follow-up candidates (Medium and minor; none triggers a revision)

Medium (warnings):
- M-01 `--unattended` is mandatory in every brief (SPEC:73) but does not exist before Phase 1, so the P0 smoke runs (SPEC:158, 194) cannot carry it, and it is never added to brainstorm or init-lite (SPEC:84, 87; AC-1.1 calls them unphased, SPEC:195). A brief with an unknown flag has no stated outcome. Expert: Wiegers. Rec: say P0 briefs omit it and say what brainstorm and init-lite receive.
- M-02 WC-4 puts the contract in "the directory containing the file" for tdd and init-lite (SPEC:62). Two parallel `/sc:tdd --output docs/x/a.md` and `.../b.md` workers share `docs/x/return-contract.yaml`, against WC-11 (SPEC:69). The fixed path for workflow (SPEC:92) has the same shape (parallel workflows in one worktree); only cleanup-audit states the one-at-a-time limit (SPEC:85). A stale contract from an earlier attempt is not guarded (Whittaker, FR-2.4 above). Expert: Nygard, Whittaker. Rec: require a per-worker output directory in the brief, and say the command overwrites or removes an existing contract at start.
- M-03 "fresh dir" is the resume answer for about 20 rows (SPEC:99-125) while WC-4 says the coordinator passes the directory before dispatch (SPEC:62, 73). Whether the command makes a new subdirectory (path then unknown) or the coordinator passes a new directory per retry is not stated (WC-6, SPEC:64). Expert: Fowler. Rec: one sentence.
- M-04 The tasklist row (SPEC:122) says the reflect fan-out "runs one layer below the worker, inside Claude Code's nesting limit" and has Stage 10.5 pass `--unattended` to each reflect. INV-B:215 gave a different verdict (call reflect without `--remediate`, run the fan-out at the worker's top level), and INV-B:210, 314, 322 mark subagent nesting and who answers the offer UNVERIFIED. The spec's Decisions row says no inventory verdict was contradicted (SPEC:268). If the headless rule auto-accepts remediation (INV-B:109, SPEC:88), each reflect may start a workflow remediation that writes under `.dev/tasks/` (INV-B:272), outside the brief's output directory and outside the contract's `artifacts` (WC-4), which AC step 6 (SPEC:185) would flag. Expert: Newman, Nygard. Rec: mark the nesting claim UNVERIFIED and state whether remediation is allowed to run under tasklist `--unattended`.
- M-05 WC-9 (SPEC:67) relies on "the command's own explicit flag", which does not exist for task `commit`/`push` (SPEC:121), and `--post-pr` for auggie-review (SPEC:100) is new while INV-A:78 knows only `--no-post-pr`. Expert: Wiegers. Rec: name the flags as new or say the actions stay off.
- M-06 D3 option (b) and the pr-submit row (SPEC:114, 241) never mention the command's own "Will Not: run headless / imply a daemon" boundary (INV-B:90; `cmd/pr-submit.md:85` UNVERIFIED). Expert: Nygard. Rec: one sentence saying whether `--unattended` counts as headless.
- M-07 Troubleshoot's report directory is `.dev/troubleshoot/<slug>-<timestamp>/` by default and `return-contract.yaml` only with `--caller task-unified` (INV-B:242). The P0 command line (SPEC:194) passes no output path, so the report path is not known before dispatch as SPEC:62 and SPEC:73 require. Expert: Adzic. Rec: pass an output path, or say the worker reports the generated path (M5 style).
- M-08 Testability gaps (Crispin, Gregory): WC-3 has no acceptance check, and AC-2.2 (SPEC:200) demands `--outcome failed` although WC-3 lets a worker `ask` instead (SPEC:61); "once" is undefined for commands with several gates (cli-portify, SPEC:105); WC-6 and WC-12 have no check (WC-7 only in AC-0.4); AC-4.3 (SPEC:210, 240 s) is stricter than WC-10 (SPEC:68, 300 s); WC-1 gives no number ("well inside", SPEC:59, while its own evidence says about 45 s fails).
- M-09 Undefined inputs: `--unattended` without an output directory; the token inside a quoted argument (`/sc:spec-panel` defines it as a standalone argument token outside quotes in `command.md:459`, the spec does not); the shared contract file `~/.claude/WORKER-CONTRACT.md` being unreadable or older than the command section that points to it (SPEC:52). Expert: Nygard. Rec: one line each, or accept as out of scope.
- M-10 AC-C1 (SPEC:172) prints nothing over `src/superclaude/core`, but SPEC:147 allows an Orca mention in the contract file and SPEC:158 adds an Orca section to `HOW-WE-WORK.md`, both under `core`; any `orca orchestration ...` example there fails AC-C1. AC-0.3 (SPEC:193, `grep -E '^-[^-]'`) misses deleted `- ` bullet lines, the blind spot SPEC:176 (M4) fixed for AC-C5. Expert: Crispin.
- M-11 WC-4 says commands with an existing contract "keep their fields" (SPEC:62) while AC step 4 asserts `status` is one of four values (SPEC:183) and AC-1.2 runs that step on adversarial and workflow (SPEC:196). Neither inventory records the existing status vocabulary (UNVERIFIED), so the two can conflict.
- M-12 SPEC:154 says "Phases 1-3 need no user decision" while SPEC:225 says Phases 0-3 "can proceed on the recommendations"; D1 (flag name and mechanism) and D5 are decisions P0 depends on.
- M-13 `/sc:reflect` under `--unattended` is made to follow the headless auto-accept rule (SPEC:88), which "skips the gates" (INV-B:109); the spec's UNVERIFIED item 9 (SPEC:280) assumes the worker is not headless. The consequence for what reflect then runs is not stated.
- M-14 UNVERIFIED scope point: the reviewing session's installed skill list also names `sc:graph`, `sc:impact` and `sc:issue` (the last "creates an Orca worktree"), none of which is among the 43 commands (INV-A:3, INV-B:3), and E5's "no command calls Orca" (SPEC:25) and AC-C1 would be false for `sc:issue` if it exists in the repo. I cannot check this against any file in the workspace. Rec: re-run the E5 grep and the command count on the final tree.
- M-15 All `cmd/`, `sk/`, `CLAUDE.md`, `HOW-WE-WORK.md` and external-file citations are UNVERIFIED in this sandbox, including the 11 "re-read" locations (SPEC:11) and the claimed citation check (SPEC:285).

Minor (notes):
- AC-1.1 excludes "unphased brainstorm and init-lite" (SPEC:195), which are not in the P1-P3 set anyway.
- AC-1.3 suggests a "scratch worktree" (SPEC:197); the repo's Orca-only worktree rule is in `CLAUDE.md`, which is not checkable here (UNVERIFIED).
- `/sc:load` is counted among the 27 "needing a change" but receives only a usage-line fix and is excluded from WC-4 (SPEC:112, 76); say so in the count sentence.
- SPEC:272-284 numbers the UNVERIFIED items 1-14 while the Decisions table is unnumbered; no cross-references use the numbers except item 14.

The session that ran this review would ask the user once whether to open an issue for the follow-up candidates and would create none without an answer. No user channel exists in this sandbox, so the list is only recorded here.

## Reviser brief

Blocking finding ids: F-01.

Rules the reviser must follow (restated from the command's Review Loop, bullet 6):
- Revise only text a blocking finding names (F-01: SPEC:159 and SPEC:195).
- Add no rule, mechanism or section that no blocking finding calls for; each added paragraph or table cites its finding id.
- Prefer deleting or narrowing to adding.
- Report the byte size before and after, and the bytes added and deleted per finding id.
- Leave Medium and minor findings (M-01 to M-15 and the notes) alone.
- Return the candidate once and do not award a PASS.

verdict: FAIL

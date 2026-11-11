review: 1 of 3

# Whole-document audit of the Orca worker-contract spec (/sc:spec-panel, critique, focus requirements,architecture)

Citation keys: `SPEC:N` = line N of `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`; `INV-A:N`, `INV-B:N`, `CAPS:N` = `inventory/commands-a.md`, `commands-b.md`, `orca-capabilities.md`; `README:N` = `.dev/orca-command-refactor/README.md`; `CMD:N` = the `/sc:spec-panel` command definition. A citation of a file outside `.dev/orca-command-refactor/` (for example `EVIDENCE.md`, `src/superclaude/...`, `~/.claude/...` skill lines) cannot be checked in this sandbox and is marked UNVERIFIED.

## Header

- candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`
- candidate sha256: `e867c6d99ac7d3695eb8d12653c0adb84cc8683d98189276c8b5f83a5fe17627` (58682 bytes, 286 lines)
- baseline: not given. `--re-review` and `--baseline`: neither given, so this is a first review of the full document (CMD:258). This is a labelled whole-document audit, not a scoped re-review.
- reviewer model actually used: claude-sonnet-5-5
- mode: critique; focus: requirements, architecture; panel: Wiegers (lead), Adzic, Cockburn, Fowler, Newman, Hohpe, Nygard, Whittaker (always active, CMD:83), Crispin (Guard Table completeness), in the fixed review order (CMD:101-113)
- inputs read: command definition, README (CMD:1, README:1-38), the review-loop prompts file (FIRST-REVIEW prompt), the candidate in full, and the three inventories by targeted line reads and greps (not in full: INV-A, INV-B and CAPS are 34 KB, 54 KB and 45 KB; lines not read are not cited)
- iterations: one review whatever `--iterations` says (CMD:261). The Improve step is not part of this run; no revised specification is written. The candidate was not edited.

## Grading summary

| Severity | Count |
|---|---|
| Blocking (CRITICAL or concrete-wrong-outcome MAJOR) | 1 (F-1) |
| Medium (follow-up candidates) | 8 (M-1 to M-8) |
| Minor notes | 6 (N-1 to N-6) |

Grading check applied to each finding: "An implementer who follows the stated text as written builds X, and X is wrong because Y." Where that sentence needed a guess between two readings, the finding is Medium (prompts file, FIRST-REVIEW prompt).

## === REQUIREMENTS ANALYSIS ===

### F-1 BLOCKING (MAJOR): the default contract location for a file-valued `--output` makes parallel workers overwrite each other's report
- Expert: Wiegers (consistency), Whittaker (FR-2.3 sentinel/collision, FR-2.5 accumulation)
- Where: WC-4 at SPEC:62 against WC-11 at SPEC:69.
- Stated text A (SPEC:62): the contract path defaults to `<output-dir>/return-contract.yaml`, "where `<output-dir>` is the directory the coordinator passed (`--output` / `--output-dir`, or the directory of the file when `--output` is a file)". Stated text B (SPEC:69): "Two workers in one worktree must never write the same file."
- Sentence: An implementer who follows WC-4 as written builds a contract whose path is the parent directory of the `--output` file, and that is wrong because two workers whose `--output` files share a parent directory write the same `return-contract.yaml`, which WC-11 forbids and which makes the coordinator read the other worker's status.
- Concrete attack (Whittaker, FR-2.3/FR-2.5): the coordinator dispatches two `/sc:tdd` workers, `--output docs/tdd/auth.md` and `--output docs/tdd/billing.md` (tdd takes `--output <file>`, SPEC:90; spec-panel gets a file-valued `--output`, SPEC:120). State before: `docs/tdd/` holds no contract. Both workers finish; the second to finish overwrites the first's `docs/tdd/return-contract.yaml`. Worker A sends `worker_done --report-path docs/tdd/return-contract.yaml` (WC-5, SPEC:63) after worker B has written `status: failed`. The coordinator opens the path (SPEC:73) and records A as failed, or the reverse. WC-11's slug/timestamp rule covers "default output paths" (SPEC:69) and does not name the contract file, and no acceptance check dispatches two workers into one directory (7.2 at SPEC:179-186 runs one worker per command), so the defect passes every listed check.
- Recommendation (narrow, no new mechanism): for a file-valued `--output`, name the contract after the output file (for example `<output-file>.return-contract.yaml`), or require a distinct directory per worker in the brief (SPEC:73). Either replaces the "directory of the file" clause only.
- Priority: High. Quality impact: Testability 6 to 8, Consistency 7 to 9.

### M-1 MEDIUM: P1 adds `--unattended` to commands whose gates are converted only in P2 to P4, so the flag promises a guarantee the command does not yet give
- Expert: Cockburn, Nygard
- Where: P1 scope at SPEC:159 ("the `--unattended` flag and the `## Unattended mode` section in every command in sections 3.1 and 3.2 except load (a no-op where a command has no gate; later phases fill in the gate resolutions)"); AC-1.1 at SPEC:195; WC-2 at SPEC:60; WC-9 at SPEC:67; auggie-review row at SPEC:100 (phase P2).
- Issue: after P1, `/sc:auggie-review --unattended` still posts to GitHub and `/sc:cleanup --unattended` still prompts, because their resolutions are P2. The text says the section is a no-op "where a command has no gate", but P1 covers commands that have gates. Whether a coordinator passes the flag between phases is a guess, so Medium, not blocking, although the outcome (a PR post, SPEC:100; `cmd/auggie-review.md:51-54` is UNVERIFIED here) crosses a safety boundary if it happens.
- Recommendation: until a command's row is converted, have `--unattended` resolve as blocked (WC-2 c) instead of a silent no-op. Priority: Medium.

### M-2 MEDIUM: "fresh output directory" for a retry has no owner when the coordinator passes the path
- Expert: Wiegers, Adzic
- Where: WC-6 at SPEC:64 ("writes each run into a fresh output directory"); 22 rows of section 3.2 say "fresh dir"; the brief carries the output path (SPEC:73).
- Issue: a retry (`worker-start --retry-of`, CAPS:116) reuses the same brief, hence the same `--output`. The text does not say whether the command or the coordinator makes the path fresh, so the "must not corrupt the first attempt's output" requirement (SPEC:64) can fail on a literal reading. No acceptance check covers a retry. Recommendation: say the coordinator passes a new path per Dispatch, and add that to the brief list at SPEC:73. Priority: Medium.

### M-3 MEDIUM: WC-10's heartbeat rule cannot be met by foreground Agent-tool fan-out, and no row or check addresses it
- Expert: Nygard, Whittaker (FR-2.5)
- Where: WC-10 at SPEC:68 ("A command step that blocks a single tool call for longer than 5 minutes ... must be split into waits of at most 4 minutes"); fan-out is kept inside commands (E4, SPEC:24; WC-7, SPEC:65); only cli-eval (SPEC:104) and pr-submit (SPEC:114) get wait splitting; AC-4.3 (SPEC:210) checks only pr-submit.
- Issue: tdd, adversarial, reflect, roadmap and post-release run fan-outs of 2 to 10+ agents (INV-B tdd row; INV-A:35). A foreground Agent call that runs longer than 5 minutes is one tool call that cannot be split, so the session cannot heartbeat. CAPS:130 records that the heartbeat cadence comes from the preamble and that its effect on the liveness verdict is UNVERIFIED, so the harm is unknown. Recommendation: state whether a missing heartbeat during an Agent call is acceptable, or scope WC-10 to polling waits. Priority: Medium.

### M-4 MEDIUM: AC-0.4 requires step 3 to pass on a contract path that does not exist before P1
- Expert: Crispin, Adzic
- Where: AC-0.4 at SPEC:194 ("steps 1-3 and 5-7 pass; step 4 uses the command's existing report file, since the contract arrives in P1"); step 3 at SPEC:182 ("its report path is the contract path WC-4 gives for that command"; "`--outcome` matches the contract's `status`").
- Issue: at P0 `/sc:troubleshoot` reports `REPORT.md` and adversarial's contract file has no fixed name (SPEC:83, SPEC:91; INV-A:60 records two different locations in the earlier run). Step 3 therefore cannot pass as written, and the one relaxation names only step 4. The intent is inferable, so Medium. Recommendation: apply the "existing report file" relaxation to step 3 as well. Priority: Medium.

### M-5 MEDIUM: nothing verifies the P0 deliverable, so the contract file and brief template can ship empty
- Expert: Wiegers, Crispin
- Where: P0 at SPEC:158 ("Write `WORKER-CONTRACT.md` (section 2 rules plus a coordinator brief template ...)"); AC-0.1 to AC-0.3 at SPEC:191-193.
- Issue: AC-0.1 checks only that the file name is in `KNOWN_CORE_FILES`; AC-0.2 and AC-0.3 check the HOW-WE-WORK copy and that no routing row changed. No check asserts that the file contains WC-1 to WC-12 or the brief template, although P0 names `test_worker_contract.py` as a deliverable and AC-1.1 (SPEC:195) later requires every command to point at the file. Recommendation: one assertion in P0 that the file exists, names each WC id and holds a brief template. Priority: Medium.

### M-6 MEDIUM: `--unattended` for the shipped `/sc:spec-panel` differs from the spec's flag surface
- Expert: Cockburn, Fowler
- Where: spec-panel row at SPEC:120 and WC-4 at SPEC:62 ("`--output` / `--output-dir`"; "add `--output`") against the command definition read in this sandbox, which uses `--report-dir <dir>` as the required directory, treats `--output` as file-valued, refuses a missing `--report-dir` in chat only, and offers `--improve` (CMD:459-465).
- Issue: the spec's report-location rule and the command that implements it do not match, and a refusal without a report directory writes no contract, which conflicts with "written on every outcome" (SPEC:62). This is outside the candidate's stated text (it concerns a later command revision), so Medium. Whether CMD is the version the spec intended is UNVERIFIED. Recommendation: choose one flag name for the report directory across all commands (the spec's own `--output` or `--report-dir`) and say how a refusal is reported. Priority: Medium.

## === ARCHITECTURE ANALYSIS ===

### M-7 MEDIUM: SA-2 permits an Orca mention in the contract file that AC-C1 then rejects
- Expert: Fowler (single responsibility of the contract file), Newman
- Where: SA-2 at SPEC:147 ("The only allowed mention of Orca in a changed command is as an example of a caller's question channel inside the contract file"); AC-C1 at SPEC:172 (the grep covers `src/superclaude/core`, where `WORKER-CONTRACT.md` lives per SPEC:52, and "prints nothing"); P0 also adds an Orca section to `HOW-WE-WORK.md` (SPEC:158), which is in `core/`.
- Issue: a contract file or routing section that writes `orca orchestration ask` (the natural example) fails AC-C1, and SA-2 allows exactly that text. An implementer can avoid it by choosing different words, so this needs a guess; Medium. Recommendation: exclude `core/WORKER-CONTRACT.md` and the Orca section of `core/HOW-WE-WORK.md` from AC-C1, or narrow SA-2 to wording the regex does not match. Priority: Medium.

### M-8 MEDIUM: tasklist's Stage 10.5 resolution may replace a stall with unreviewed nested remediation
- Expert: Fowler, Nygard, Whittaker (FR-2.4)
- Where: tasklist row at SPEC:122 ("Stage 10.5 passes `--unattended` to each reflect so the headless rule applies ... inside Claude Code's nesting limit, `INV-A:14`"); reflect row at SPEC:88 and SA-6 at SPEC:151; inventory verdict "drop `--remediate` in 10.5" at INV-B:295; reflect's headless rule auto-accepts remediation (INV-B:109).
- Issue: the inventory's recommendation (remove the offer) is replaced by a rule that auto-accepts remediation inside N subagents. The spec says one layer below the worker is inside the limit, but each reflect reviewer tier adds layers (INV-B:109 describes Tier 2 reviewers, calibrators, adversarial and validator), and remediation hands off to another command. Whether the depth holds is UNVERIFIED (INV-A:14 gives "three layers"; the sum of layers was not counted in the spec), and whether auto-accepted remediation passes WC-9 is not stated. Recommendation: either count the layers in the row or keep `--remediate` off under `--unattended`. Priority: Medium.

## Minor notes (never fail the review)

- N-1 (Cockburn): D3 recommends no pr-submit change in Phase 4 (SPEC:240), while P1 and AC-1.1 add a `## Unattended mode` section to pr-submit (SPEC:159, SPEC:195), and section 4 says commands outside workers get none (SPEC:128). State that pr-submit's P1 section is a stub, or exclude it until D3.
- N-2: the P1 "Commands" cell (SPEC:159) lists 12 names while its scope sentence covers 36 commands (10 in 3.1 plus 26 in 3.2 without load); count: 10 + 27 = 37, minus load = 36.
- N-3: SA-4 lists a workflow "contract gap" fix (SPEC:149) while the workflow row says "None" (SPEC:92).
- N-4: step 7 of 7.2 writes `ORCA orchestration worker-release` with no worker or dispatch argument (SPEC:186); CAPS:109 and CAPS:113 describe it per settled worker.
- N-5: README states that a supervised worker waiting on a question fails the 60-second limit (README:13); the spec narrows this to a pre-input-box prompt (SPEC:44) on the strength of `EVIDENCE.md:39,45,56`, which cannot be read here (UNVERIFIED). CAPS:52 supports the narrowing. Keep the statement, but flag that README:13 and SPEC:44 differ.
- N-6: the spec's own check claims (SPEC:11, SPEC:285: "11 locations re-read", "about 340 citations ... 9 defects") cannot be checked here (UNVERIFIED); no finding depends on them.

## Guard Condition Boundary Table

Trigger present: the spec defines threshold checks, boolean guards and sentinel values (CMD:313). Guards chosen are those that decide an implementer's behaviour. Input classes left out are marked with a one-line reason. FR-8 and FR-9 grading applied; no GAP below is blocking except as cross-referenced.

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|---|---|---|---|---|---|---|
| `--unattended` token | SPEC:51, SPEC:228 | Zero/Empty | flag absent | false | standalone behaviour unchanged (SA-1, SPEC:146) | OK |
| `--unattended` token | SPEC:51 | Typical | flag present as standalone token | true | unattended rules apply (SPEC:60) | OK |
| `--unattended` token | SPEC:51 | Sentinel Value Match | flag text inside quoted content | not stated in the spec | the shipped command text excludes quoted tokens (CMD:459), the spec does not | GAP (Medium, M-6 family) |
| `--unattended` on a command whose gate is not yet converted | SPEC:159 | Legitimate Edge Case | flag present between P1 and P2 | true | "no-op"; gate still fires | GAP (M-1) |
| `<output-dir>` for the contract | SPEC:62 | Typical | `--output <dir>` | n/a | `<dir>/return-contract.yaml` | OK |
| `<output-dir>` for the contract | SPEC:62 | One/Minimal | `--output <file>` shared parent | n/a | parent directory, collides | GAP (F-1, blocking) |
| `<output-dir>` for the contract | SPEC:62 | Zero/Empty | no output flag | n/a | standalone writes only today's files (SPEC:148); unattended case: command-specific rows, pre-creation STOP for workflow (SPEC:62) | OK |
| status to outcome mapping | SPEC:63 | Typical | `succeeded`, `partial`, `failed`, `blocked` | n/a | mapped; `partial` maps to succeeded (SPEC:63, SPEC:263) | OK |
| status to outcome mapping | SPEC:63 | Zero/Empty | no report file | n/a | `--outcome failed` (SPEC:63) | OK |
| status to outcome mapping | SPEC:62-63 | Sentinel Value Match | `status` value outside the four | not stated | unspecified; AC step 4 asserts membership (SPEC:183) but the worker's behaviour is not given | GAP (Medium) |
| heartbeat/wait guard | SPEC:68 | Typical | wait of 3 minutes | true | allowed | OK |
| heartbeat/wait guard | SPEC:68 | Maximum/Overflow | single tool call over 5 minutes | false | "must be split"; unsplittable Agent calls not addressed | GAP (M-3) |
| confidence guard in `/sc:task` | SPEC:121 | Legitimate Edge Case | confidence exactly 0.70 | not stated | row says "below 0.70" blocked; the boundary value follows the command text (UNVERIFIED, `cmd/task.md:93`) | GAP (Medium, minor in effect) |
| `--monitor 1` under unattended | SPEC:114 | Typical | `--monitor 1` | true | refused | OK |
| WC-3 `ask` timeout | SPEC:61 | Maximum/Overflow | `ask` times out | true | resume same message ID, no duplicate; default timeout UNVERIFIED (SPEC:281) | OK |
| WC-12 `check` result | SPEC:70 | Legitimate Edge Case | `consumer_fenced` | true | stop, no `worker_done` | OK |

Left out, with reason: Zero/Empty and Maximum for the `--monitor 1` guard, because the flag is a fixed enumeration; One/Minimal for the heartbeat guard, because a wait shorter than 4 minutes needs no handling.

## Quantity Flow (Pipeline Dimensional Analysis)

The spec describes a classification pipeline over commands. Counts re-derived:

```text
[cmd/: 43 commands (INV-A:3 gives 21; INV-B:3 gives 22; SPEC:76)]
   --> [ready today: 10]       (SPEC:81-92: 10 rows)
   --> [needs change: 27]      (SPEC:97-125: 27 rows)
   --> [coordinator-only: 6]   (SPEC:131-137: 6 rows)      10 + 27 + 6 = 43  OK
[27 needing change] --> P1: 9, P2: 11, P3: 4, P4: 3        sum 27  OK (SPEC:112 load counted in P1)
[ready 10] --> P2 changes: reflect, release-split, tdd, troubleshoot (4) --> P2 total 11 + 4 = 15  matches SPEC:160
[P1 flag/section scope: 10 ready + 27 - load = 36] vs [P1 Commands cell: 12 names]            MISMATCH (N-2)
```

No count mismatch changes behaviour; the P1 cell mismatch is a presentation note (N-2). The load-bearing inventory split matches the inventories' totals (INV-A:3, INV-B:3).

## Expert commentary (condensed, in review order)

- Wiegers: requirements are numbered, owned and evidenced (SPEC:57-70); the open items are the collision between WC-4 and WC-11 (F-1) and the unowned "fresh dir" (M-2).
- Adzic: acceptance checks are executable (SPEC:167-210); a two-worker scenario is missing, which is how F-1 escapes (see F-1) and a retry scenario is missing (M-2).
- Cockburn: the primary actor is the coordinator and the stakeholder is the person at the keyboard; SA-1 protects the person, and the staged rollout (M-1) is the gap in that protection.
- Fowler: shared rules in one core file is sound (SPEC:52, SPEC:264); the layer count for tasklist's nested reflect is not shown (M-8).
- Nygard: the failure path of every gate is "blocked plus contract", which is a good single mechanism; unsplittable waits and the no-heartbeat case are open (M-3).
- Whittaker: one blocking attack (F-1); the other attacks are Medium (M-1, M-3, M-8) or minor.
- Newman: the `--unattended` interface versioning between P1 and P4 is the same concern as M-1; the spec-panel flag drift (M-6) is a compatibility point.
- Hohpe: the report file as the only completion payload is simple and consistent (SPEC:62, SPEC:73); the shared-filename case is F-1.
- Crispin: the acceptance structure is complete except where noted (M-4, M-5).
- Gregory and Hightower: no finding of their own beyond the above.

## Follow-up candidates (Medium and minor; none triggers a revision)

M-1, M-2, M-3, M-4, M-5, M-6, M-7, M-8; N-1 to N-6. The session that ran the review asks the user once per loop whether to open an issue for these (CMD:260); this worker cannot ask and creates none. The coordinator should put the question to the user.

## What was covered

All 286 lines of the candidate were read. Checked against the inventories: the 43/10/27/6 counts and phase sums (INV-A:3, INV-B:3, SPEC:76-137, SPEC:156-162); the Orca facts in R1 to R4 and WC-1, WC-3, WC-5, WC-10 and the 7.2 verbs (CAPS:44-52, CAPS:58-64, CAPS:72-76, CAPS:97-103, CAPS:107-116, CAPS:129-131, CAPS:145-150, CAPS:155-161); the tasklist and reflect rows against INV-B:109 and INV-B:295; the adversarial contract location against INV-A:60. Not covered or UNVERIFIED: every `cmd/` and `sk/` line the spec cites (the repository is not in the sandbox), `EVIDENCE.md`, `.dev/codegraph-migration/...`, `CLAUDE.md` line cites and `src/superclaude/core/HOW-WE-WORK.md` line cites; the spec's claim of an independent 340-citation check. Orca verbs in 7.2 (`--terminal-state`, `--source transcript`, `check --wait --types`) match the capabilities inventory (CAPS:63, CAPS:107-113, CAPS:131).

## Reviser brief

Blocking finding ids: F-1.

Reviser contract (restated from the command, CMD:263): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id. Leave Medium and minor findings alone. Do not award yourself a PASS.

F-1: change only the WC-4 clause at SPEC:62 that derives `<output-dir>` from "the directory of the file when `--output` is a file", so two workers with different `--output` files cannot share one contract path. Narrow the clause; do not add a section.

verdict: FAIL

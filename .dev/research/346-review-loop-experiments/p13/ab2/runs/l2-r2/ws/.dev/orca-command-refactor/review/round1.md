review: 1 of 3

# Spec panel report, round 1

- command: `/sc:spec-panel @.dev/orca-command-refactor/specs/orca-worker-contract-spec.md --mode critique --focus requirements,architecture`
- candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`
- candidate sha256: `d3cdbe573e57303b9ce6c93d1fe98ba18fb7cb1a15773d926bf6a0c31425200d` (taken with `sha256sum`; it equals the hash recorded in lint-1.md:1)
- baseline: none given. `--re-review` and `--baseline` were not passed, so this is a first review of the full document (no `baseline: missing` note applies, because neither flag was given).
- reviewer model used: claude-sonnet-5-5
- panel: Wiegers (lead), Adzic, Cockburn for requirements; Fowler (lead), Newman, Hohpe, Nygard for architecture; Whittaker (adversarial pass, active in every review)
- citation convention: `SPEC:N` = line N of the candidate. `INV-A:N`, `INV-B:N`, `CAPS:N` = line N of `.dev/orca-command-refactor/inventory/commands-a.md`, `commands-b.md`, `orca-capabilities.md`. Every `INV`/`CAPS` citation below was read in the workspace. A citation to a file outside the workspace (`src/...`, `cmd/...`, `sk/...`, `EVIDENCE.md`, `CLAUDE.md`, the codegraph README) is marked UNVERIFIED.
- prompt followed: FIRST-REVIEW prompt in `~/.claude/rules/prompts/document_review_loop_prompts.md:27-33`, read in full.

## Lint evidence

`.dev/orca-command-refactor/review/lint-1.md:1-5`: checks REF, findings 0, "No findings." There is no lint id to confirm or dismiss. The lint's sha256 equals the candidate's, so it ran on this exact file.

## What was covered

- All 285 lines of the candidate were read once. Section counts were checked by hand: 3.1 has 10 rows (SPEC:83-92), 3.2 has 27 rows (SPEC:99-125), section 4 has 6 rows (SPEC:132-137); 10+27+6 = 43, which matches SPEC:76.
- The phase lists were reconciled with the rows (count-conservation table below).
- Eight load-bearing inventory and Orca-capability citations were re-read: CAPS:44-46, 52, 72-79, 92, 97-103, 129-130, 145-150, 155-161; INV-A:62, 65, 90-97, 106, 113, 118, 120; INV-B:31, 65, 89-95, 105, 272, 285-286, 292-301, 311, 320, 323. All matched what the spec says about them, except as stated in the findings.
- Not covered: every `cmd/` and `sk/` line the spec cites is UNVERIFIED (not in the workspace). I did not re-judge the per-command verdicts; I checked them only against the inventories.

## Count conservation (Pipeline Dimensional Analysis, Fowler/Whittaker)

The spec contains one multi-stage flow: inventory (43 commands) to verdict to phase. No mismatch found.

```text
[43 commands: INV-A 21 + INV-B 22]            SPEC:76, INV-A:3, INV-B:3
   --> [ready today: 10]   SPEC:83-92
   --> [needs change: 27]  SPEC:99-125
   --> [coordinator-only: 6] SPEC:132-137
10 + 27 + 6 = 43                                   OK
needs-change by phase: P1 9 (analyze, build, business-panel, design, document,
  explain, index, load, test) + P2 11 + P3 4 (roadmap, save, validate-roadmap,
  validate-tests) + P4 3 (implement, post-release, pr-submit) = 27   OK
ready-today by phase: P1 fixes 4 (adversarial, cleanup-audit, index-repo, workflow),
  P2 gate edits 4 (reflect, release-split, tdd, troubleshoot), no edit besides the
  generic P1 flag 2 (brainstorm, init-lite)   OK, but see F-2
```

## Guard Condition Boundary Table (Nygard lead, Crispin completeness, Whittaker attack)

Guards found in the spec: the readiness limit, the heartbeat/wait sizes, the nesting depth, the outcome mapping, the retry circuit breaker, the confidence gate and the `--unattended` switch. One row per input class that can occur; classes that cannot occur are left out with a reason on the row.

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|-------|----------|-----------------|----------------|--------------|-------------------|--------|
| wait-split rule (`> 5 min` must split to `<= 4 min`) | SPEC:68 WC-10 | Typical | one tool call of 10 min | true | split into waits of at most 4 min | OK |
| wait-split rule | SPEC:68 WC-10 | Legitimate Edge Case | one tool call of 4 min 30 s | false (not over 5 min) | not split by WC-10, yet SPEC:114 and SPEC:210 require every iteration under 4 min / 240 s | GAP (F-7) |
| wait-split rule | SPEC:68 WC-10 | Zero/Empty | wait of 0 s | n/a | no wait, no split; trivially fine, left out of further rows | OK |
| nesting depth fence | SPEC:33 R1, SPEC:250-253 D5 | Typical | depth 1, worker calls `worker-start` | true (refused) | refused with `nested_worker_depth_exceeded` (CAPS:99) | OK |
| nesting depth fence | SPEC:33 R1 | Legitimate Edge Case | depth raised above 1 by the user | false | D5(b) says it would "break R1's protection"; R1 itself is about refusal, not fan-out limits | OK (wording only, N-2) |
| `--unattended` switch | SPEC:51, SPEC:228 D1 | Typical | token passed by coordinator | true | unattended mode | OK |
| `--unattended` switch | SPEC:51, SPEC:147 SA-1 | Sentinel Value Match | a person types `--unattended` | true | the person gets the unattended rules; D1(a) says "a person never types it" and defines no refusal | GAP, minor (N-6) |
| `--unattended` on a command with an unresolved gate | SPEC:159 P1 vs SPEC:60 WC-2 | Divergence (flag accepted, gate unconverted) | `/sc:implement ... --unattended` in P1-P3 | true | P1 accepts the flag; gate resolution waits for P4 | GAP (F-2, blocking) |
| outcome mapping | SPEC:63 WC-5 | Typical | contract `status: partial` | n/a | `--outcome succeeded`, body says partial | OK |
| outcome mapping | SPEC:63 WC-5 | Zero/Empty | no contract file exists | n/a | `--outcome failed` | OK |
| outcome mapping | SPEC:63 WC-5 | Legitimate Edge Case | contract exists but is not valid YAML or lacks `status` | n/a | not specified (AC step 4 checks it only in tests, SPEC:183) | GAP, Medium, folded into F-4 |
| contract path rule | SPEC:62 WC-4 | Zero/Empty | `--output` is a file (tdd, init-lite) | n/a | `<output-dir>` is undefined | GAP (F-8) |
| contract path rule | SPEC:62 WC-4 vs SPEC:83 | Divergence | adversarial writes `<output>/adversarial/...` | n/a | two stated paths | GAP (F-4) |
| retry circuit breaker | SPEC:64 WC-6, CAPS:116 | Maximum/Overflow | third consecutive failure | true | Task failed by Orca; the spec adds nothing and needs nothing | OK |
| readiness limit | SPEC:59 WC-1 | Typical | fallback 30 s | true | passes (evidence UNVERIFIED, `EVIDENCE.md:45,56` is outside the workspace; CAPS:52 quotes `EVIDENCE.md:35`) | OK |
| readiness limit | SPEC:59 WC-1 | Legitimate Edge Case | fallback "well inside" 60 s but no number | n/a | no number is stated | GAP, minor (N-5) |
| confidence gate | SPEC:121 task row | Legitimate Edge Case | exactly 0.70 | n/a | row says "below 0.70" resolves as blocked; `>= 0.70` proceeds | OK |

Classes left out: the Maximum/Overflow class for the wait rule (no capacity exists; the tool-call time is bounded only by the tool), and the Sentinel class for the nesting fence (depth is a plain integer, CAPS:97).

Per FR-8/FR-9 each GAP above is graded by consequence in the findings below.

## === REQUIREMENTS ANALYSIS ===

### F-1 [MAJOR, blocking] `/sc:load` is required to pass checks that the spec says it cannot pass
Expert: Wiegers (lead), Adzic
Priority: High. Quality-impact: Completeness -1, Consistency -1.

Grading sentence: an implementer who follows the stated text as written builds, for `/sc:load`, a `## Unattended mode` section naming `return-contract.yaml` and a P1 live check that needs a contract file, and that is wrong because the same spec says `/sc:load` writes no report and must not get one, so two stated texts contradict and the acceptance check cannot pass.

- SPEC:112 (load row): report "none (see note)", "use it as a step inside another worker's brief, not as its own Task", change "P1 (usage line only)". SPEC:265 (Decisions): "a report file would be an unrequested addition. Only its usage-line defect is fixed." SPEC:159 lists load as "(usage line only)".
- SPEC:76 says every changed command "also gains the `## Unattended mode` section"; SPEC:195 (AC-1.1) asserts "every command in sections 3.1-3.2 has a `## Unattended mode` section naming `return-contract.yaml`"; SPEC:196 (AC-1.2) runs the live check "on each P1 command", whose step 4 is `test -s <contract>` (SPEC:183) and whose step 3 needs "its report path is the WC-4 contract path" (SPEC:182).
- Load is a P1 command (SPEC:159) and in sections 3.1-3.2, so both AC-1.1 and AC-1.2 apply to it. Under the row and the Decision, no contract exists, so AC-1.2 step 4 fails; under AC-1.1 a section naming a file that load never writes is required, which the Decision forbids.
- The inventory recorded the same fork: INV-B:65 ("if dispatched, it needs a written context-summary file") and INV-B:293 lists load among the commands that need a single report file. The spec chose the other branch at SPEC:265 but did not carve load out of the acceptance checks.

Recommendation: carve `/sc:load` out of AC-1.1 and AC-1.2 by name (it has no Unattended section and no live check), or give it a contract and drop the "none" row. Delete rather than add where the Decision stands.

### F-2 [MAJOR, blocking] Phase 1 gives every 3.2 command the `--unattended` flag, including ones whose gates are not converted until P2-P4
Expert: Wiegers (lead), Cockburn, Whittaker (Sequence Attack)
Priority: High. Quality-impact: Consistency -2, Testability -1.

Grading sentence: an implementer who follows P1 as written builds an accepted `--unattended` flag, a `## Unattended mode` section and a passing AC-1.1 on `/sc:implement`, `/sc:pr-submit`, `/sc:post-release` and `/sc:roadmap` while their person-blocking gates still prompt until P3 or P4, and that is wrong because WC-2 says that under `--unattended` the command never calls `AskUserQuestion` or ends its turn on a question.

I can break this specification by **Sequence Attack**. The invariant at **SPEC:60 (WC-2) and SPEC:159 (P1)** fails when **a coordinator dispatches a P1-era `/sc:pr-submit ... --unattended` or `/sc:implement ... --unattended`**. Concrete attack: (1) after P1 the command accepts the flag and AC-1.1 passes (SPEC:195); (2) the coordinator, trusting WC-2, omits any fallback; (3) `/sc:implement` hits `E-HALT-QA` (SPEC:109, resolved only in P4, SPEC:162) and ends its turn waiting for a Ruling, so the session shows no `worker_done`; Orca reports it "healthy, not failed" (CAPS:52, CAPS:129). That is the silent stall the spec exists to prevent (SPEC:44).

- SPEC:159: "the `--unattended` flag accepted by every command in sections 3.1 and 3.2 (a no-op where a command has no gate)". The parenthesis covers only commands with no gate. Commands with gates are scheduled later: roadmap, save, validate-roadmap, validate-tests P3 (SPEC:161); implement, post-release, pr-submit P4 (SPEC:162); and Phase 4 "waits for answers to D2-D4" (SPEC:154).
- Under the recommended D3(a) (SPEC:240) pr-submit is run by the coordinator or a person and gets "no pr-submit changes"; section 4 says commands the coordinator keeps "get no `--unattended` mode" (SPEC:128). AC-1.1 nevertheless requires a pr-submit section (SPEC:195), because pr-submit is in 3.2 (SPEC:114).
- The phases' own claim "Phases 1-3 need no user decision" (SPEC:154) is false for pr-submit and post-release if P1 touches them, since D3 and D4 gate their behaviour.

Recommendation: restrict the P1 flag and AC-1.1/AC-1.2 to the commands the P1 row lists (analyze, build, business-panel, design, document, explain, index, test) plus the 3.1 commands, and let each later phase add the flag together with its gate resolution; state that pr-submit gets nothing under D3(a).

### F-4 [MAJOR, Medium] The contract path rule in WC-4 conflicts with rows that fix a different path
Expert: Wiegers, Adzic
Priority: Medium. Quality-impact: Consistency -1.

Needs a guess about which text wins, so Medium (follow-up candidate).

- SPEC:62 WC-4: contract at `<output-dir>/return-contract.yaml`, "the directory the coordinator passed", "known before dispatch".
- SPEC:83 (adversarial): fix the filename to `<output>/adversarial/return-contract.yaml`, one level down. SPEC:92 (workflow): contract at `.dev/tasks/to-do/<id>/return-contract.yaml`, where `<id>` exists only after the package is created, yet the same row says to write the contract for pre-creation STOPs (INV-B:272 confirms the pre-creation gap). With no `<id>` yet, no path is specified for that case. SPEC:114 (pr-submit): "beside `monitor-run-<PR>.jsonl`", which is under `--output-dir` (INV-B:92) and so matches WC-4, but the path is not stated.
- Step 3 of the live check (SPEC:182) and AC-1.4 (SPEC:198) both depend on the path, and an implementer cannot tell whether the general rule or the row governs.

Recommendation: say that a row's stated path overrides WC-4, and give the pre-creation STOP of workflow an explicit path (for example `<output-dir>`).

### F-8 [MAJOR, Medium] `<output-dir>` is undefined where `--output` names a file
Expert: Wiegers, Whittaker (Zero/Empty Attack)
Priority: Medium.

- SPEC:62 defines `<output-dir>` as "the directory the coordinator passed (`--output` / `--output-dir`)". SPEC:87 (init-lite) and SPEC:90 (tdd) take `--output <file>`; the expected deliverable is a file. The spec does not say where the contract goes then (next to the file? `<file>/return-contract.yaml` is impossible).
- Graded Medium: two readings are allowed and one of them (next to the file) is natural.

Recommendation: add a one-line rule for file-valued `--output`.

## === ARCHITECTURE ANALYSIS ===

The decision itself (section 1) is well argued: Orca coordinates, commands stay units of work. The rejected alternative (SPEC:29-37) is supported by CAPS:97-103 (depth 1), CAPS:147-150 (identity and `runtime_unavailable`), CAPS:145 (executable name) and INV-A:90, INV-B:285-286 (competing orchestrators). The evidence-strength statement (SPEC:41-45) states its own gaps honestly. No architecture finding is blocking.

### F-3 [MAJOR, Medium] The "no Orca in installed primitives" check can fail on text the spec itself adds
Expert: Fowler (lead), Newman
Priority: Medium. Quality-impact: Testability -1.

Needs a guess about the future content of the new files, so Medium.

- AC-C1 (SPEC:172) greps `src/superclaude/core` for `orca(-ide)? (orchestration|worktree|terminal|agent)` and must print nothing, excluding only `skills/ccsession-tag/`.
- SA-2 (SPEC:147) allows Orca to be mentioned in the contract file "as an example of a caller's question channel". P0 (SPEC:158) adds an Orca section to `HOW-WE-WORK.md` and a coordinator brief template to `WORKER-CONTRACT.md`, both in `core/`; WC-3 (SPEC:61) has the contract refer to the preamble's `ask` command. Any line such as `orca orchestration ask` in those files fails AC-C1 in P0 although SA-2 permits it. E5 (SPEC:25) says HOW-WE-WORK currently mentions Orca zero times, which is what the Orca section changes.
- Also (minor, N-1): the pattern is written with `\|` inside a markdown table (SPEC:172); copied from the raw file, `\|` in `grep -E` is a literal pipe, so the pattern would match nothing and the check passes vacuously.

Recommendation: exclude the two named files from AC-C1, or limit AC-C1 to `commands/`, `skills/` and `agents/`.

### F-5 [MAJOR, Medium] "Additive edits" check contradicts adding a flag to a Usage line
Expert: Fowler, Crispin (completeness)
Priority: Medium.

- SA-4 (SPEC:149) calls Phase 1-3 edits "additive: a new `## Unattended mode` section and new flags". AC-C5 (SPEC:176) fails on any removed line (`^-[^-]`). Commands list flags in a Usage line (SPEC:112 says load's Usage line lacks `--checkpoint`, so such lines exist). Adding a flag to that line is a one-line replacement, which prints a `-` line and fails AC-C5; adding it elsewhere is allowed by SA-4 but is not required by anything.
- Also, `^-[^-]` misses a deleted line that starts with `--` (for example a frontmatter fence). Needs a guess, so Medium.

Recommendation: let AC-C5 ignore a Usage line whose only change is an appended flag, or require new flags to be documented in the new section only.

### F-6 [MAJOR, Medium] pr-submit's stated "Will Not: run headless" is not reconciled with an unattended mode
Expert: Nygard (lead), Hohpe
Priority: Medium.

- INV-B:90 records `Will Not: run headless / imply a daemon` (`cmd/pr-submit.md:85`, `SKILL.md:225`: UNVERIFIED in this workspace). D3(b) and the 3.2 row (SPEC:114, SPEC:241) would give it an unattended mode with operator HALTs resolved as blocked, and the spec never states whether a worker session counts as "headless" for that rule. The Orca worker is an interactive terminal session (SPEC:16), so it probably does not, but the spec leaves it as a guess.
- Only matters if the user picks D3(b). Medium.

Recommendation: add one sentence to D3(b) or the pr-submit row saying how the "Will Not" line is amended or why it does not apply.

### F-7 [MAJOR, Medium] WC-10 leaves a gap between its trigger and its target
Expert: Nygard, Whittaker (Accumulation Attack)
Priority: Medium.

- SPEC:68: a single blocking call "longer than 5 minutes" must be split into waits of "at most 4 minutes". A 4 min 30 s call is not covered by the trigger. The pr-submit row (SPEC:114) and AC-4.3 (SPEC:210) demand "under 4 minutes" / "no single tool call exceeds 240 s", and the Decisions row (SPEC:266) picks 4 minutes "for margin". The trigger should be the same number as the limit.
- Heartbeat gap: with 4 min 30 s calls back to back and a heartbeat cadence of 5 minutes (CAPS:130) the worker still heartbeats between calls, so the practical harm is small. Medium.

Recommendation: change the trigger to "longer than 4 minutes".

## === ADVERSARIAL ANALYSIS (Whittaker) ===

Five attack methodologies were applied to the spec's invariants. Results other than F-2, F-7, F-8 and F-4 above:

- **Zero/Empty:** a worker whose preamble has no Task or Dispatch ID is an ordinary session (SPEC:50), so `--unattended` with an empty preamble sends no lifecycle messages; the contract is still written (WC-4). Holds.
- **Divergence:** D1(a) flag versus preamble. Both present with a person present: the flag wins by D1(a). Holds.
- **Sentinel Collision:** a legitimate topic string equal to `--unattended` in a quoted prompt. The spec does not say the flag must be a standalone token outside quoted text. Minor, N-6.
- **Sequence:** F-2.
- **Accumulation:** none. Counts of blocked questions are one per run (WC-3), with the resume-by-message-ID rule at SPEC:61.

## Evidence notes (not defects)

- E3 (SPEC:23) cites `invocation_method: "skill-direct"` as support, while SPEC:43 says the same run "proves the nested route, not the direct route". The two statements are not reconciled in the text, and the source files (`.dev/codegraph-migration/...`, README:31) are not in the workspace: UNVERIFIED (N-3).
- E5's grep results (SPEC:25) were not re-run, since `src/` is outside the sandbox: UNVERIFIED.
- SPEC:11 says 11 locations were re-read by the author and ends with an independent citation check (SPEC:285); neither could be checked here.

## follow-up candidates

Medium (warnings; none changes the verdict, none enters the Reviser brief):

- F-3 AC-C1 vs SA-2/P0 (SPEC:172, 147, 158)
- F-4 WC-4 path vs row paths, and the workflow pre-creation STOP path (SPEC:62, 83, 92)
- F-5 AC-C5 vs a Usage-line edit (SPEC:176, 149)
- F-6 pr-submit "Will Not: run headless" (INV-B:90; SPEC:114, 241)
- F-7 WC-10 trigger 5 min vs target 4 min (SPEC:68, 114, 210)
- F-8 `<output-dir>` where `--output` is a file (SPEC:62, 87, 90)

Minor notes:

- N-1 AC-C1 pattern is written with `\|` inside backticks in a table; copy-paste from the raw file gives a no-op regex (SPEC:172).
- N-2 D5(b) says raising depth would "break R1's protection against runaway fan-out", but R1 is a refusal, not a fan-out cap (SPEC:33, 252).
- N-3 E3 `skill-direct` vs section 1.4 "nested route" (SPEC:23, 43), UNVERIFIED.
- N-4 SPEC:79 says "The only command changes are the small fixes in the last column", while P1 and AC-1.1 add a flag and a section to every 3.1 command (SPEC:159, 195).
- N-5 WC-1 says a launch-path prompt must fall back "well inside" 60 s with no number, although 30 s and about 45 s are the evidence points (SPEC:59).
- N-6 The spec does not say what happens when a person types `--unattended` (SPEC:228), nor that the flag must be a standalone token.

These are listed for the user to decide. The session that ran this review asks the user once, per the command's loop rule, whether to open an issue for the follow-up candidates and creates none without an answer. (Question recorded; no answer was available in this run, so no issue is created.)

## Reviser brief

Blocking finding ids: F-1, F-2.

Rules for the reviser (restating the Review Loop, bullet 6; the reviser reads this report, not the command):
- Revise only text a blocking finding names. Add no rule, mechanism or section that no blocking finding calls for; each added paragraph or table cites its finding id.
- Prefer deleting or narrowing to adding. Report the byte size of the candidate before and after, and the bytes added and deleted per finding id.
- Leave minor and Medium findings alone (F-3 to F-8, N-1 to N-6), including through any "apply all findings" instruction.
- Return the candidate once; do not award yourself a PASS.

F-1: `/sc:load` (SPEC:112, 265) writes no report, yet AC-1.1 (SPEC:195) and AC-1.2 (SPEC:196) require it to have a contract-naming section and a contract. Narrow the two checks (or the load row) so they agree.
F-2: P1 (SPEC:159) and AC-1.1/AC-1.2 add `--unattended` to commands whose gates are converted only in P2-P4 (SPEC:160-162), contradicting WC-2 (SPEC:60) and D3(a) (SPEC:240). Narrow the P1 flag scope and the two checks to commands that have no unconverted gate.

verdict: FAIL

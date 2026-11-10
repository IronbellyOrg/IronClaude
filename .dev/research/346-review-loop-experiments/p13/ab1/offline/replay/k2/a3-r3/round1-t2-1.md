review: 1 of 3

# Spec-panel review, round 1: orca-worker-contract-spec.md

- mode: critique; focus: requirements, architecture; format: markdown report grouped by analysis bucket
- candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`
- candidate sha256: `d3cdbe573e57303b9ce6c93d1fe98ba18fb7cb1a15773d926bf6a0c31425200d`
- baseline: none given; prior report: none given; this is a first review of the full document
- reviewer model actually used: claude-sonnet-5-5
- prompt followed: FIRST-REVIEW prompt, `~/.claude/rules/prompts/document_review_loop_prompts.md` (read in full before writing)
- Improve step: not run (first review, no `--improve`); the candidate was not edited
- citation keys: `SPEC` = the candidate; `INV-A` / `INV-B` / `CAPS` = `.dev/orca-command-refactor/inventory/commands-a.md` / `commands-b.md` / `orca-capabilities.md`; `README` = `.dev/orca-command-refactor/README.md`; `CMD` = the `command.md` panel definition. A citation to a repo file the candidate cites but that is not in the workspace (for example `src/superclaude/commands/*.md`, `CLAUDE.md:NN`, `orchestration/README.md:33`) is UNVERIFIED unless an inventory line repeats it.

## Coverage
Covered: all 285 lines of SPEC read in full; every count in SPEC section 3 and section 6 recomputed (see Quantity check); every `INV-*` and `CAPS` citation I spot-checked against the inventory line it names (E1-E4, R1-R5, WC-1 to WC-12, section 3 rows) matched; acceptance checks AC-C1..C5, 7.2 steps 1-7 and AC-0.x to AC-4.x read for whether they can pass as written; decisions D1-D5 and the Decisions and UNVERIFIED sections read.
Not covered / UNVERIFIED: the source files under `src/superclaude/` (not in the workspace), the Orca binary and guides (only the transcribed `CAPS` lines), `CLAUDE.md` / `HOW-WE-WORK.md` line numbers cited by SPEC, and SPEC's own claim of an independent ~340-citation check (SPEC:285). No command was run.

## Panel
Review sequence (CMD "Expert Review Sequence"): Wiegers, Adzic, Cockburn, Fowler, Nygard, Whittaker, Newman, Hohpe, Crispin, Gregory, Hightower. Focus panels: requirements (Wiegers lead, Adzic, Cockburn) and architecture (Fowler lead, Newman, Hohpe, Nygard); Whittaker is active in every review.

- **Wiegers**: the requirement set (WC-1 to WC-12) is mostly measurable, but three acceptance checks cannot pass as written (F1-F3) and two requirements leave the contract file location open (F4, F10).
- **Adzic**: the examples in D1 and in section 7 are good; the live check in AC-0.4 does not match its own pass condition (F3).
- **Cockburn**: the primary actor (the coordinator author) is clear; the worker session's duties have no stated delivery path to that actor's brief (F9).
- **Fowler**: one shared contract file is the right boundary (SPEC:52); the fresh-directory rule collides with the coordinator-supplied directory (F10) and fixed output paths collide with WC-11 (F17).
- **Nygard**: no coordinator stall policy (F14), the heartbeat rule has an unverified premise and a gap (F13), and one claim is stated as fact without evidence (F15).
- **Whittaker**: see Adversarial analysis (F18, F19).
- **Newman**: the contract has no version field while one existing contract is already at "1.1" (N1); the phased `--unattended` rollout leaves a window where the flag is accepted but not honoured (F12).
- **Hohpe**: the flag does not propagate to nested skill and command calls (F11, F16).
- **Crispin**: tests in section 7 are concrete; AC-C1 conflicts with SA-2 (F8); AC-1.3 names an unspecified "scratch worktree" (N4).
- **Gregory**: the three-amigos gap is the worker-session duties that only the coordinator brief can carry (F9).
- **Hightower**: operational fit is sound (no Orca calls in commands, SPEC:16, SPEC:147); the Orca-not-running case is handled by keeping commands Orca-free.

## Grading rule applied
Blocking = the sentence "An implementer who follows the stated text as written builds X, and X is wrong because Y" holds with no further assumption (contradiction between two stated texts, data loss or safety breach, or an acceptance criterion that cannot pass). Everything that needs a guess about which of two readings is picked, or that is a requirement the spec never states, is Medium and listed only under follow-up candidates.

=== REQUIREMENTS ANALYSIS ===

### F1. MAJOR, blocking. AC-1.1 and AC-1.2 require a report and an `## Unattended mode` section for `/sc:load`, while the spec says `/sc:load` gets neither
- Expert: Wiegers.
- Grading sentence: An implementer who follows the stated text as written changes only the Usage line of `/sc:load` in Phase 1 and writes no report for it (SPEC:112, SPEC:159, SPEC:265), and then AC-1.1 (SPEC:195) demands a `## Unattended mode` section naming `return-contract.yaml` for every command in sections 3.1-3.2, and AC-1.2 (SPEC:196) demands a live run with `--unattended --output <dir>` whose pass step 4 needs a valid contract (SPEC:183) for "each P1 command", which includes load (SPEC:159). Load has no report, no output flag and "use it as a step inside another worker's brief, not as its own Task" (SPEC:112), so Phase 1 cannot pass; because later phases wait for earlier checks (SPEC:154), Phases 2-4 are blocked.
- Evidence: SPEC:76 ("Every changed command also gains the `## Unattended mode` section"); SPEC:112 (Report: "none (see note)"); SPEC:265 (decision: "a report file would be an unrequested addition"); SPEC:159 (load listed in P1); SPEC:195-196; INV-B:31, INV-B:62, INV-B:65 (load writes no file and is better used as a brief step). Also SPEC:220 (non-goal 8: only defects that stop a command working as a worker are in scope) and SPEC:112 (the only change is a Usage-line defect that does not stop it working as a worker).
- Recommendation: delete load from the P1 command list (SPEC:159), from AC-1.1/AC-1.2 and from the "27 needing a change" count, or state in AC-1.1/AC-1.2 that load is exempt. Narrowing is smaller than adding a report to load.
- Priority: High. Quality impact: Testability 6 to 8.

### F2. MAJOR, blocking. Section 3.1 says ready commands change only by their small fix; Phase 1 and AC-1.1 add `--unattended` and an `## Unattended mode` section to every one of them
- Expert: Wiegers.
- Grading sentence: An implementer who follows SPEC:79 ("The only command changes are the small fixes in the last column") leaves `brainstorm` and `init-lite` (small fix "None", SPEC:84, SPEC:87) unedited, and is then wrong because SPEC:159 requires "the `--unattended` flag accepted by every command in sections 3.1 and 3.2", SPEC:76 gives every changed command the section, and AC-1.1 (SPEC:195) asserts the section for every command in 3.1-3.2, so the test fails on those two commands (and on other "None" or already-contracted rows).
- Evidence: SPEC:76, SPEC:79, SPEC:84, SPEC:87, SPEC:159, SPEC:195; SPEC:79 also says the worker reports the named file "until Phase 1 adds the contract", but brainstorm already writes `<output>/return-contract.yaml` (SPEC:84; INV-A:39).
- Recommendation: replace the second sentence at SPEC:79 with "Phase 1 also adds `--unattended` and the `## Unattended mode` section to each of these commands." (an added sentence replacing a contradicted one), or restrict AC-1.1 to the commands that have a small fix.
- Priority: High. Quality impact: Consistency 6 to 8.

### F3. MAJOR, blocking. AC-0.4 requires 7.2 step 3 to pass in Phase 0, but step 3 needs a contract that Phase 0 does not have, and step 1 needs an `--unattended` flag that does not exist yet
- Expert: Adzic (example/scenario check), with Wiegers.
- Grading sentence: An implementer who runs AC-0.4 as written (SPEC:194: "steps 1-3 and 5-7 pass; step 4 uses the command's existing report file") on `/sc:troubleshoot` finds step 3's pass condition "its `--outcome` matches the contract's `status` ... its report path is the WC-4 contract path" (SPEC:182) cannot hold: troubleshoot writes `REPORT.md` and a `return-contract.yaml` only with `--caller task-unified` (SPEC:91; INV-B:242), `status` and the WC-4 path do not exist before Phase 1 (SPEC:194 says "the contract arrives in P1"), and the exception names only step 4. The same step-3 condition fails for `/sc:adversarial`, whose contract filename is fixed only in P1 (SPEC:83), and for `/sc:workflow`, whose contract sits at `.dev/tasks/to-do/<id>/return-contract.yaml` (SPEC:92), not at a WC-4 `<output-dir>` path. Separately, step 1 says the brief carries "the exact command line including `--unattended`" (SPEC:73, SPEC:180), but P0 makes no command edit (SPEC:158) and the AC-0.4 command lines have no `--unattended` (SPEC:194). Phase 0 gates everything after it (SPEC:154, SPEC:158).
- Evidence: SPEC:73, SPEC:154, SPEC:158, SPEC:180, SPEC:182, SPEC:194; INV-B:242, INV-B:272.
- Recommendation: in AC-0.4 say "steps 1-2, 3 (without the contract conditions: one `worker_done`, outcome matches the report's own verdict) and 5-7 pass; step 4 uses the command's existing report file", and say P0 briefs omit `--unattended`. Narrowing text, no new mechanism.
- Priority: High. Quality impact: Testability 6 to 8.

### F4. Medium. WC-4's contract location is undefined for file-valued `--output`, for workflow and for cli-eval
- Expert: Wiegers. Needs a guess (dirname of the file, or a new flag) so it is not blocking.
- Evidence: WC-4 puts the contract at `<output-dir>/return-contract.yaml`, "known before dispatch" (SPEC:62), but `tdd` and `init-lite` take `--output <file>` (SPEC:87, SPEC:90), `spec-panel`'s `--output` is to be added with no kind stated (SPEC:120; INV-B:182), `workflow` writes under a generated `<id>` (SPEC:92; INV-B:272), `cli-eval` gains no output flag (SPEC:104), and the pre-creation-STOP contract for workflow has no `<id>` to be placed under (SPEC:92).
- Recommendation: add one sentence to WC-4 giving the rule for a file-valued `--output` and naming the workflow and cli-eval locations.
- Priority: Medium.

### F5. Medium. WC-4 says existing contracts "keep their fields" and also fixes a four-value `status` set; existing value sets were never checked
- Expert: Wiegers.
- Evidence: SPEC:62 and SPEC:262 (fixed set `succeeded/partial/failed/blocked`; 7.2 step 4 asserts membership, SPEC:183); the existing contracts of workflow, brainstorm, reflect and adversarial are only described by field names (INV-B:272: `status`, `plan_path`, `reflect_report_path`), never by `status` values. If any uses another vocabulary, either "keep their fields" or the assertion fails.
- Recommendation: add the existing `status` values to the contract inventory, or state that those four contracts map their values into the set.
- Priority: Medium.

### F6. Medium. The `/sc:index` row tells the implementer to document a claim the inventory marks UNVERIFIED
- Expert: Wiegers.
- Evidence: SPEC:111 ("state that knowledge-base mode does not wait (whether it does is UNVERIFIED)"); INV-A:54 and INV-A:113 (the file does not say). Writing the statement without checking it can leave a command that claims not to wait and does.
- Recommendation: make the row "check whether it waits; if so, refuse the mode under `--unattended`" (same pattern as business-panel, SPEC:102).
- Priority: Medium.

### F7. Medium. Flags the rows rely on are not in the evidence and the rows say "Other required change: none"
- Expert: Cockburn.
- Evidence: `--post-pr` for auggie-review (SPEC:100, SPEC:67, SPEC:247) while the inventory knows only `--no-post-pr` and `--no-remediation-offer` (INV-A:38); post-release authorization flags and the pr-submit authorization flag under D3(b)/D4 (SPEC:113-114, SPEC:241, SPEC:245) while INV-B:85 says they "must become explicit pre-authorization inputs". WC-9 (SPEC:67) turns an outward action on only through "the command's own explicit flag", which does not exist for these.
- Recommendation: list each new flag in the row's "Other required change" column.
- Priority: Medium.

### F8. Medium. AC-C1 would fail on the contract file that SA-2 permits to mention Orca
- Expert: Crispin.
- Evidence: SA-2 allows an Orca mention "as an example of a caller's question channel inside the contract file" (SPEC:147); AC-C1 greps `src/superclaude/core` (where `WORKER-CONTRACT.md` lives, SPEC:52) and must print nothing (SPEC:172). Whether the allowed mention matches the pattern depends on its wording.
- Recommendation: exclude `core/WORKER-CONTRACT.md` in AC-C1, or drop the SA-2 exception.
- Priority: Medium.

### F9. Medium. The worker-session duties (WC-3, WC-5, WC-7, WC-10, WC-12) have no stated delivery path to the worker
- Expert: Cockburn and Gregory.
- Evidence: the brief contents are listed at SPEC:73 and contain only the command line, output directory, authorizations and worktree. The shared rules reach a worker only through a changed command's pointer to `~/.claude/WORKER-CONTRACT.md` (SPEC:52), which the Phase 0 smoke commands do not have (SPEC:158). AC-0.4 nevertheless checks outcome mapping (SPEC:182, SPEC:194). Heartbeat cadence itself comes from Orca's preamble, not a guide (CAPS:130).
- Recommendation: add to the SPEC:73 list "the worker duties of WC-3, WC-5, WC-7, WC-10 and WC-12, or a pointer to the contract file".
- Priority: Medium.

=== ARCHITECTURE ANALYSIS ===

### F10. Medium. WC-6 ("fresh output directory per run") and WC-4 ("directory the coordinator passed", path known before dispatch) pull in opposite directions
- Expert: Fowler. Two readings exist (the command makes a subdirectory, or the coordinator passes a new directory per attempt), so it is not blocking.
- Evidence: WC-4 (SPEC:62), WC-6 (SPEC:64), 25 or more rows with resume "fresh dir" in SPEC:99-125, brief contents without a rule to change `--output` on a retry (SPEC:73). A subdirectory breaks the path the coordinator already holds; the same directory on a retry overwrites the first attempt, the case WC-6 exists to prevent. Ready rows also overwrite on re-run: init-lite "Re-run overwrites its marked report" (SPEC:87).
- Recommendation: one sentence in 2.3: "on `--retry-of` the coordinator passes a new output directory".
- Priority: Medium.

### F11. Medium. `--unattended` does not propagate to nested skill and command calls except tasklist to reflect
- Expert: Hohpe.
- Evidence: roadmap calls `sc:save` at every wave (INV-B:154), and save's single-owner keys are fixed only for save itself in Phase 3 (SPEC:119, SPEC:161); brainstorm, release-split, workflow and tdd each call nested commands (INV-B:119, INV-B:271, INV-B:219). Only tasklist's Stage 10.5 is given an explicit rule (SPEC:122).
- Recommendation: add one WC-2 sentence: a command that invokes another command or skill passes `--unattended` down.
- Priority: Medium.

### F12. Medium. Phases 1-3 leave commands that accept `--unattended` but still prompt
- Expert: Newman.
- Evidence: P1 adds the flag to every command in 3.1-3.2, "a no-op where a command has no gate" (SPEC:159), while gate conversion for cleanup, improve, task and others is P2 and pr-submit, implement and post-release are P4 (SPEC:160, SPEC:162). Between phases `/sc:cleanup --unattended` is accepted and still shows its approval prompt (INV-A:43), the stall WC-2 forbids (SPEC:60). Under D3(a) pr-submit would never be converted (SPEC:240) yet P1 and AC-1.1 still give it the section.
- Recommendation: P1 adds the flag only to commands with no open gate; others get it in the phase that converts their gate.
- Priority: Medium.

### F13. Medium. WC-10 rests on an unverified premise and names only two commands
- Expert: Nygard.
- Evidence: heartbeat age feeding the liveness verdict is UNVERIFIED (CAPS:130, CAPS:182) and Orca treats a waiting worker as healthy (CAPS:129). WC-10 applies to "a command step that blocks a single tool call for longer than 5 minutes" (SPEC:68), which also describes long Agent-tool fan-out waits in adversarial, cleanup-audit and tdd (INV-A:35, INV-A:42; INV-B:221), but section 3 assigns it only to cli-eval and pr-submit (SPEC:104, SPEC:114). The cli-eval run is a background job plus Monitor (INV-A:65), which is not one blocking call. The pr-submit iteration length is UNVERIFIED (SPEC:283).
- Recommendation: state whether WC-10 covers Agent-tool waits; if not, narrow it to the two named commands.
- Priority: Medium.

### F14. Medium. No coordinator stall policy
- Expert: Nygard.
- Evidence: SPEC:44 says the real failure is a silent stall seen only through `agentWait` or a missing report; Orca says absence never authorizes stop, abandon, retry or release (CAPS:125) and a Dispatch's total run time may be unbounded (CAPS:188; SPEC:282). SPEC:73 and 7.2 define what the coordinator does after `worker_done` but not what it does when none arrives or the report is missing.
- Recommendation: add the coordinator's wait-and-escalate rule to 2.3, using only the proof listed at CAPS:126.
- Priority: Medium.

### F15. Medium. Section 1.4 item 2 states an unsupported fact
- Expert: Nygard.
- Evidence: SPEC:44 says a command's own `AskUserQuestion` "comes after readiness, so it does not fail `worker-start`". For Claude the task is passed on the command line (CAPS:47) and CAPS:53 says no interactive question may appear before the agent input is ready. Whether the first question of a command (for example the cli-eval suite menu, INV-A:44) lands before or after readiness is not in the evidence. WC-2 removes the gates anyway.
- Recommendation: mark the sentence UNVERIFIED and add it to the UNVERIFIED list (SPEC:271-285).
- Priority: Medium.

### F16. Medium. The tasklist row drops the inventory's requirement and its nesting claim is not carried as UNVERIFIED
- Expert: Fowler and Hohpe.
- Evidence: INV-B:215 requires the per-phase reflect fan-out to run at the worker's top level; INV-B:210 and INV-B:314 mark nested spawning UNVERIFIED. SPEC:122 says "none" and that the reflect fan-out is "inside Claude Code's nesting limit" (citing INV-A:14), although reflect itself spawns further agents (INV-B:111), and gives no resolution for the `needs_human_decision` HALTs of Stage 10.5 (INV-B:209) under `--unattended`.
- Recommendation: add the nesting question to the UNVERIFIED list and state the unattended resolution of those HALTs (blocked, per WC-2 (c)).
- Priority: Medium.

### F17. Medium. WC-11 ("must never write the same file") vs ready commands with fixed output paths
- Expert: Fowler.
- Evidence: cleanup-audit "output dir is fixed, so one audit per worktree at a time" (SPEC:85), index-repo writes `PROJECT_INDEX.md` (SPEC:86), init-lite has a fixed default (SPEC:87); the brief contents do not tell the coordinator to serialize them (SPEC:73).
- Recommendation: add "never dispatch two workers of the same fixed-path command into one worktree" to 2.3.
- Priority: Medium.

=== ADVERSARIAL ANALYSIS (Whittaker) ===

### F18. Medium. I can break this specification by the **Sentinel Collision Attack** and the **Divergence Attack**. The invariant at **D1 / 2.1 (SPEC:51, SPEC:227-230)** fails when **`--unattended` is not a clean standalone flag, or is combined with `--interactive`**.
Concrete attack: before: `/sc:tdd "explain what --unattended does" --output d.md` (a person) runs interactively. After the spec: the string `--unattended` is inside the topic; the spec defines no token rule, so the command may switch to unattended mode and skip a clarification a person needed (breaks SA-1, SPEC:146). Second: `/sc:release-split spec.md --unattended --interactive` has no stated precedence; only cleanup, improve, roadmap, business-panel and explain are said to refuse the conflicting flag (SPEC:100-110, SPEC:118). Needs a guess, so Medium.
Recommendation: one sentence in 2.1: the flag counts only as a standalone token outside quoted arguments; `--unattended` with `--interactive` is refused. Priority: Medium.

### F19. Medium. I can break this specification by the **Sequence Attack**. The invariant at **roadmap row (SPEC:118) and AC-3.2 (SPEC:205)** fails when **a retry reuses the directory of an earlier attempt**.
Concrete attack: attempt 1 leaves `<dir>/.session-memory.md` and partial outputs; the retry runs `/sc:roadmap <spec> --unattended --output <dir>` with no resume flag; AC-3.2 requires it to "start fresh" in the same `<dir>`; state before: attempt-1 files present; state after: overwritten, which WC-6 forbids (SPEC:64).
Recommendation: AC-3.2 uses a new directory per attempt or states that fresh means new directory. Priority: Medium.

Also attacked and found handled: Zero/Empty on the report (WC-4 "including stops before any other output exists", SPEC:62); Accumulation on retries (circuit breaker, CAPS:80, SPEC:263); out-of-order `worker_done` (WC-5 and `check` fence, SPEC:63, SPEC:70).

## Guard Condition Boundary Table
Guards found: G1 `--unattended` switch; G2 output directory (WC-4); G3 wait size vs heartbeat (WC-10); G4 outcome mapping (WC-5); G5 resume or fresh run (WC-6); G6 readiness limit (WC-1); G7 outward-action default (WC-9); G8 nesting depth (R1). Per the CMD template, input classes that cannot occur are left out and named in the last column of the omission list below.

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|-------|----------|-----------------|----------------|--------------|--------------------|--------|
| G1 `--unattended` | SPEC:51, SPEC:227 | Zero/Empty | flag absent | false | standalone behaviour unchanged (SPEC:146) | OK |
| G1 `--unattended` | SPEC:51 | Typical | flag present, standalone | true | gates resolve per row, report written | OK |
| G1 `--unattended` | SPEC:227 | Sentinel Value Match | flag text inside a quoted topic | undefined | none stated | GAP (F18, Medium) |
| G1 `--unattended` | SPEC:100-118 | Legitimate Edge Case | with `--interactive` | undefined for most commands | refused only for five commands | GAP (F18, Medium) |
| G2 output dir | SPEC:62 | Zero/Empty | no dir or empty string | undefined | "stops before any other output exists" but names no location | GAP (F4, Medium) |
| G2 output dir | SPEC:87, SPEC:90 | Legitimate Edge Case | file-valued `--output` | undefined | none stated | GAP (F4, Medium) |
| G2 output dir | SPEC:62, SPEC:64 | Maximum/Overflow | dir already holds a prior attempt | true | overwrite vs fresh dir conflict | GAP (F10, Medium) |
| G2 output dir | SPEC:62 | Typical | fresh dir passed | true | contract at `<dir>/return-contract.yaml` | OK |
| G3 wait split | SPEC:68 | Typical | wait of 4 minutes | true | allowed, heartbeat between | OK |
| G3 wait split | SPEC:68 | One/Minimal | one 4-minute wait | true | allowed | OK |
| G3 wait split | SPEC:68 | Maximum/Overflow | single Agent-tool call over 5 minutes | undefined | none stated | GAP (F13, Medium) |
| G3 wait split | SPEC:114 | Legitimate Edge Case | pr-submit iteration near 240 s | unknown | "confirm" (UNVERIFIED, SPEC:283) | GAP (F13, Medium) |
| G4 outcome | SPEC:63 | Zero/Empty | no report file | true | `--outcome failed` | OK |
| G4 outcome | SPEC:63 | Zero/Empty | empty or unparseable report | undefined | only "no report exists" covered | GAP (minor, N6) |
| G4 outcome | SPEC:63, SPEC:263 | Legitimate Edge Case | `partial` or audit verdict FAIL | true | `succeeded` with status in body | OK |
| G4 outcome | SPEC:62, SPEC:262 | Sentinel Value Match | existing contract uses another `status` value | undefined | none stated | GAP (F5, Medium) |
| G5 resume | SPEC:64 | Typical | resume flag and state present | true | resumes | OK |
| G5 resume | SPEC:118, SPEC:205 | Legitimate Edge Case | state present, no flag (roadmap) | false | starts fresh in same dir | GAP (F19, Medium) |
| G6 readiness | SPEC:59 | Typical | fallback under 30 s | true | passes (EVIDENCE via CAPS:49) | OK |
| G6 readiness | SPEC:59 | Maximum/Overflow | fallback near 45-60 s | boundary | "well inside" the limit, not measured | GAP (N6, minor) |
| G7 outward default | SPEC:67 | Zero/Empty | no explicit flag | false | action off | OK |
| G7 outward default | SPEC:67, SPEC:245 | Legitimate Edge Case | flag present, no user quote in brief | true | only the coordinator's discipline; nothing checks it | GAP (minor, covered by D4) |
| G8 nesting depth | SPEC:33 | Typical | command calls `worker-start` at depth 1 | refused | `nested_worker_depth_exceeded` (CAPS:97-99) | OK |

Omitted classes: G1 One/Minimal and Maximum (a boolean has no such value); G3 Zero/Empty (a zero-length wait cannot trigger the guard); G4 One/Minimal and Maximum (a four-value enumeration); G5 Zero/Empty and Maximum (a flag is present or absent); G6 Zero/Empty (a zero-second fallback is not a prompt); G7 One/Minimal and Maximum (a boolean); G8 Zero/Empty and Maximum (depth is a fixed setting, CAPS:98). The table is complete for every guard (FR-10); every GAP above is graded Medium or minor because none names a wrong outcome that needs no further assumption (FR-8/FR-9 grading).

## Quantity check (Pipeline Dimensional Analysis)
Not triggered as a data pipeline: SPEC describes no multi-stage filter or fan-out of items. The one count flow is the command classification, and it conserves: 21 (INV-A:3) + 22 (INV-B:3) = 43; ready 5 + 5 = 10, needing change 13 + 14 = 27, coordinator-only 3 + 3 = 6 (INV-A:73, INV-B:278; SPEC:76); 10 + 27 + 6 = 43. SPEC:81-92 lists 10 ready rows; SPEC:98-125 lists 27 change rows; SPEC:132-137 lists 6. Phase assignment: P1 9 + P2 11 + P3 4 + P4 3 = 27 change rows, plus 8 ready commands with a small fix (P1 4, P2 4) and 2 ready commands with none (SPEC:84, SPEC:87): 27 + 8 + 2 + 6 = 43. No mismatch.

## Quality assessment (0-10)
Clarity 8; Completeness 7; Testability 6 (F1, F3); Consistency 6 (F1, F2, F10). Overall 6.8.

## Notes (minor, never fail the review)
- N1. The return contract has no version field although workflow's contract is already "1.1" (SPEC:62; INV-B:272). Newman.
- N2. E3 cites an `invocation_method: "skill-direct"` return contract as evidence that Orca workers ran `/sc:adversarial` (SPEC:23), while section 1.4 says the earlier run proves only the nested route (SPEC:43; CAPS:156). INV-A:13 and INV-A:14 make both statements; the spec should say which holds.
- N3. E4 states as fact that Agent-tool subagents "are not counted by Orca's nesting limit" (SPEC:24); CAPS:155 marks "Orca never limits them" UNVERIFIED.
- N4. AC-1.3 names a "scratch worktree" without saying how it is created (SPEC:197); AC-2.4's review and comment counts can change from other reviewers during the run (SPEC:202).
- N5. UNVERIFIED observation from the session's skill list, not from a workspace file: that list shows commands and skills (for example an issue-claim command whose description mentions an Orca worktree) that do not appear in the 43-command count (SPEC:76) or in the E5 "no primitive calls Orca" statement (SPEC:25). Whether the snapshot differs from that list is not checkable here.
- N6. WC-1 "well inside the readiness limit" has no number (SPEC:59); an empty or unparseable report is not covered by WC-5 (SPEC:63).

## Follow-up candidates
These are Medium and minor findings. They do not fail the review and do not appear in the Reviser brief. Issue offer: not asked, because this review ran as a worker without a person channel (CMD "Review Loop" 3: a run without a person only records the list); no issue was created.

- Medium: F4 (contract location), F5 (existing `status` vocabularies), F6 (index row asserts an UNVERIFIED claim), F7 (new flags not in evidence), F8 (AC-C1 vs SA-2), F9 (worker-duty delivery), F10 (fresh dir vs passed dir), F11 (no propagation to nested calls), F12 (accepted-but-unhonoured flag in P1-P3), F13 (WC-10 premise and scope), F14 (no stall policy), F15 (unsupported 1.4 claim), F16 (tasklist nesting and HALTs), F17 (fixed output paths vs WC-11), F18 (flag token and `--interactive` precedence), F19 (roadmap retry in same dir).
- Minor: N1 to N6.

Brief clauses that overrode the review's default scope: none (the brief asked for the FIRST-REVIEW prompt, critique mode, focus requirements and architecture, and no edit outside this file).

## Reviser brief
Blocking finding ids: F1, F2, F3.
Restated rules for the reviser (the reviser reads this report, not the command):
- Revise only the text a blocking finding names (F1: SPEC:112, SPEC:159, SPEC:195-196; F2: SPEC:79, SPEC:159, SPEC:195; F3: SPEC:180-182, SPEC:194).
- Add no rule, mechanism or section that no blocking finding calls for.
- Each added paragraph or table row cites its finding id.
- Prefer deleting or narrowing text to adding text.
- Report the byte size of the candidate before and after, and the bytes added and deleted per finding id.
- Leave Medium and minor findings (F4 to F19, N1 to N6) alone; do not award yourself a PASS.

verdict: FAIL


## Findings block

```findings-v1
{"id": "F1", "severity": "MAJOR", "blocking": true, "category": "unpassable-check", "anchor": "every command in sections 3.1-3.2 has a `## Unattended mode` section naming `return-contract.yaml`", "anchor2": "use it as a step inside another worker's brief, not as its own Task", "refs": ["AC-1.1", "AC-1.2"], "claim": "AC-1.1 and AC-1.2 require a report and a section for load, which the spec says gets neither."}
{"id": "F2", "severity": "MAJOR", "blocking": true, "category": "contradiction", "anchor": "The only command changes are the small fixes in the last column", "anchor2": "the `--unattended` flag accepted by every command in sections 3.1 and 3.2 (a no-op where a command has no gate)", "refs": ["AC-1.1"], "claim": "Section 3.1 says ready commands change only by their small fix, but P1 adds the flag and a section to all of them."}
{"id": "F3", "severity": "MAJOR", "blocking": true, "category": "unpassable-check", "anchor": "its report path is the WC-4 contract path", "anchor2": "step 4 uses the command's existing report file, since the contract arrives in P1", "refs": ["AC-0.4", "WC-4"], "claim": "AC-0.4 step 3 needs a contract that P0 does not have."}
```

review: 1 of 3

# Spec-panel critique: Orca worker contract spec (round 1)

- Command: `/sc:spec-panel @.dev/orca-command-refactor/specs/orca-worker-contract-spec.md --mode critique --focus requirements,architecture`
- Mode: critique, first review (no `--re-review`, no `--baseline`; baseline: missing, not applicable)
- Candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`, sha256 `d3cdbe573e57303b9ce6c93d1fe98ba18fb7cb1a15773d926bf6a0c31425200d`
- Reviewer model: claude-haiku-5-5 (single reviewer, fresh context, run by this subagent)
- Panel: `superclaude review panel` / `superclaude review merge` are not installed in this sandbox (not on PATH), so one reviewer ran and the merged ledger was not produced. Stated here as the loop summary note.
- Evidence limits: only `.dev/orca-command-refactor/inventory/*.md` and the README were checkable. Every citation to another file (`src/`, `.dev/evals/`, `.dev/codegraph-migration/`, `CLAUDE.md`, `EVIDENCE.md`, `sk/`, `cmd/`, `/opt/Orca`) is marked UNVERIFIED and was not used as the basis of any blocking finding.
- Coverage: the whole spec (sections 1-9, Decisions, UNVERIFIED list). About 40 `INV-A:`, `INV-B:` and `CAPS:` citations in sections 1-4 were spot-checked against the inventory line each names; the rest were not checked. Every anchor quote in the Findings block was matched once, exactly, against the candidate.

## Scope and panel

Focus: requirements (lead Wiegers; Adzic, Cockburn) and architecture (lead Fowler; Newman, Hohpe, Nygard). Whittaker runs in every panel review and is reported under requirements as an adversarial probe.

Mandatory output artifacts:
- Guard Condition Boundary Table: triggered (the spec has conditional gates and numeric thresholds). Produced below.
- State Variable Registry: not required (`--focus correctness` not active). See the advisory note at the end.
- Pipeline Dimensional Analysis and Quantity Flow Diagram: not triggered. The spec's flows are dispatch, worker, contract and coordinator reads; no stage changes the count of items in a way the spec leaves unhandled. Not produced.

## === REQUIREMENTS ANALYSIS ===

### F1 (blocking, contradiction): WC-4 "known before dispatch" is not met by the rows it governs
- Expert: Wiegers (lead), Cockburn.
- Issue: WC-4 (line 62) requires one report file "known before dispatch", and section 2.3 (line 73) says the brief carries "the output directory, so the report path is known before dispatch (WC-4)". Several rows contradict this: workflow's contract is `.dev/tasks/to-do/<id>/return-contract.yaml` with a generated `<id>` and the brief passes only `--handoff none` (3.1 workflow row, line 92); research's contract names "the generated `claudedocs/research_*.md` path" (3.2 research row, line 116); init-lite's `--output` is a file, so there is no `<output-dir>` for WC-4 to use (3.1 init-lite row, line 87). For workflow, a pre-creation STOP has no package directory at all, and WC-4 does not say where that contract goes. Whether the directory is created when missing is also not stated.
- Sentence: an implementer who follows the workflow row writes a pre-creation STOP contract to a directory that the coordinator cannot name before dispatch, and the coordinator cannot open it, which WC-4 forbids.
- Recommendation: state one rule for each class: a coordinator-passed directory (add `--output-dir` to workflow, research and init-lite, with a directory rule), or an explicit exception for generated paths that the worker reports back. Say where a pre-creation STOP writes and whether missing directories are created.
- Priority: High. Impact: high (coordinator cannot read the report).
- Evidence: spec lines 62, 73, 87, 92, 116. Inventory: `INV-B:52,267-275` (workflow), `INV-B:37,117-125`, `INV-A:35,60` (adversarial's contract path varies), `INV-B:142` (review-translation names carry a run-time suffix).

### F2 (blocking, contradiction): section 3.1 says ready commands change only by small fixes, but P1 and AC-1.1 require the `--unattended` flag in all of them
- Expert: Wiegers.
- Issue: section 3.1 (line 79) says "The only command changes are the small fixes in the last column." Phase P1 (line 159) requires "the `--unattended` flag accepted by every command in sections 3.1 and 3.2". AC-1.1 (line 195) requires every command in 3.1-3.2 to have a `## Unattended mode` section that names `return-contract.yaml`. Brainstorm, init-lite, and others in 3.1 list "None" as their fix.
- Sentence: an implementer who follows 3.1 adds nothing to brainstorm and fails AC-1.1; an implementer who follows P1 edits a command the spec calls unchanged.
- Recommendation: either add a column "Unattended section and flag: yes (no-op)" to 3.1 or change the sentence to "the only behaviour changes are..." and keep the flag in P1.
- Priority: High. Impact: medium.

### F5 (blocking, other): WC-5 maps any unrecognised or empty report to `succeeded`
- Expert: Whittaker (sentinel and zero probe), Wiegers.
- Issue: WC-5 (line 63) says `--outcome failed` when the report says `failed` or `blocked`, or "no report exists", and `--outcome succeeded` "otherwise". The four-value vocabulary (WC-4, line 62) is fixed, but existing contracts (workflow contract 1.1, adversarial, reflect; `INV-B:272`, `INV-A:35`, `INV-B:112`) use their own status values, which the spec does not map. A zero-byte file "exists", so it also maps to succeeded.
- Sentence: an implementer who follows WC-5 as written sends `--outcome succeeded` for a report whose status is `Failed` (wrong case), `ok`, or a truncated file, and that is wrong because the report says the work failed.
- Recommendation: specify that `succeeded` requires exactly `succeeded` or `partial`; anything else, including an empty or unparseable file, is `failed`. Add a mapping table from each existing contract's status to the four values.
- Priority: High. Impact: high (failed work is recorded as done).
- Evidence: spec lines 62-63; Decisions line 263 for `partial`. Inventory `INV-B:272`, `INV-A:35`.

### F6 (blocking, contradiction): E3 cites a direct-route run, while section 1.4 and UNVERIFIED item 1 say none was observed
- Expert: Wiegers (evidence), Cockburn.
- Issue: E3 (line 23) cites `invocation_method: "skill-direct"` in the P3 adversarial return contract as proof that workers have run commands. Section 1.4 (line 43) says "The only end-to-end proof is the PR #329 run, and its brief told workers to run `/sc:adversarial` through an Agent-tool subagent", so "it proves the nested route, not the direct route". UNVERIFIED item 1 (line 272) says "no such run was observed". Inventory A says the `skill-direct` contracts were written by earlier Orca workers (`INV-A:13`), so the spec's own citation is a direct-route Orca run.
- Sentence: as written, the spec asserts both that a direct-route worker run exists (E3) and that none has been observed (1.4, UNVERIFIED 1), and the two cannot both hold.
- Recommendation: name the run that produced the `skill-direct` contract, and say whether it was a worker run. If it was, rewrite 1.4 gap 1 and UNVERIFIED 1; if it was a plain session, remove it from E3.
- Priority: High. Impact: high (the core decision's evidence).
- Evidence: spec lines 23, 43, 272; `INV-A:13` (inventory, checkable).

### F7 (blocking, other): troubleshoot is "ready" with a brief that still allows a worker stall
- Expert: Adzic (example-driven check), Wiegers.
- Issue: section 3.1 says the ready commands "run as workers now if the brief uses the stated flags" (line 79). The troubleshoot row lists the brief as "no `--fix`" (line 91), but the same row says the `--depth deep` short-input STOP resolves as blocked only under P2. A brief that passes `--depth deep` with a short input, which the spec allows, reaches the STOP that asks the user to add detail, and no `worker_done` is sent.
- Sentence: an implementer who follows the stated brief sends `--depth deep` with fewer than ten words, the command stops for a person, and the worker never reports.
- Recommendation: add to the brief column "not `--depth deep` with fewer than ten words of input", or move troubleshoot to 3.2 until P2.
- Priority: High. Impact: high (silent stall, the main blocker class per `INV-A:96`).
- Evidence: spec lines 79, 91; `INV-B:49,237-245` (checkable: the STOP row).

### F8 (non-blocking, missing-requirement, MAJOR label, Medium): no rule for a coordinator reading `blocked` or `partial`
- Expert: Cockburn (actor and goal), Wiegers.
- Issue: section 2.3 (line 73) says the coordinator opens the report, then releases or reuses the worker. Nothing says what happens on `blocked` (who re-dispatches with the answer, with what Task), or on `partial`. `partial` is mapped to `succeeded` (Decisions line 263), so Orca settles the Task as complete and `task-list --ready` releases its dependents (`CAPS:86`, `CAPS:92`). The rationale is stated, but the dependent start is not.
- Sentence: a dependent of a partial Task can start on incomplete output if the coordinator starts Ready Tasks without reading the contract, which 2.3 does not forbid; the consequence depends on that assumption, so Medium.
- Recommendation: state that dependents of a `partial` Task wait for an explicit coordinator decision, and give the re-dispatch path for `blocked`.
- Priority: Medium. Impact: medium.
- Evidence: spec lines 73, 263; `CAPS:86`, `CAPS:92` (checkable).

### F9 (non-blocking, other, MAJOR label, Medium): the WC-10 wait threshold has two readings
- Expert: Adzic (testability), Wiegers.
- Issue: WC-10 (line 68) triggers splitting for a call "longer than 5 minutes" and then requires waits "of at most 4 minutes". The cli-eval row (line 104) and Decisions (line 266) require splitting every eval wait. A 4.5-minute call and an exactly 5-minute call are not settled.
- Sentence: a reader who splits only above 5 minutes and one who splits above 4 minutes both satisfy the text, so the heartbeat behaviour the spec wants is not fixed.
- Recommendation: state one trigger, for example "any single tool call expected to exceed 4 minutes is split".
- Priority: Medium. Impact: medium.
- Evidence: spec lines 68, 104, 266.

### F10 (non-blocking, other, MAJOR label, Medium): the pr-submit 600 s reading is stated against the inventory
- Expert: Wiegers (evidence), Nygard.
- Issue: WC-10 evidence (line 68) and the pr-submit row (line 114) say the 600 s is "a cumulative per-wait budget over poll-then-sleep iterations". Inventory B reads it as "waits up to --timeout 600 s per wait over several rounds" (`INV-B:34`, `INV-B:95`). The spec's re-read list (line 11) covers only `sk/sc-pr-submit-protocol/SKILL.md:37-39`, not the lines 46-64 it relies on.
- Sentence: if the poll is one 600 s call, WC-10's heartbeat requirement fails for pr-submit; the spec does not know which reading holds (UNVERIFIED 12 says poll runtime is unknown).
- Recommendation: re-read `SKILL.md:46-64` and state which reading holds before P4; until then mark pr-submit as not ready for WC-10.
- Priority: Medium. Impact: medium.
- Evidence: spec lines 11, 68, 114; `INV-B:34,95` (checkable).

### F14 (non-blocking, missing-requirement, MAJOR label, Medium): several requirements have no owner or check
- Expert: Adzic, Wiegers (testability).
- Issue: WC-1 (no prompt before readiness) names "Launch setup, not commands" as owner (line 59), but no phase changes the launch path and no AC checks it. WC-3 (ask), WC-6 (resume or re-run), WC-10 for cli-eval, and WC-11 (parallel writes) have no acceptance check. AC-1.2 covers only the P1 commands (line 196).
- Sentence: an implementer who meets every AC in section 7 can still ship a launch wrapper that waits on a person, because nothing checks WC-1.
- Recommendation: add an owner phase and a check for WC-1 (a worker-start run with the wrapper's prompt unanswered) and one check each for WC-3, WC-6, WC-10 (cli-eval) and WC-11.
- Priority: Medium. Impact: medium.
- Evidence: spec lines 59, 61, 64, 68, 69, 196; `EVIDENCE.md:39` is outside the sandbox (UNVERIFIED).

### F15 (non-blocking, missing-requirement, MAJOR label, Medium): the explicit `--post-pr` flag is not evidenced
- Expert: Wiegers.
- Issue: the auggie-review row (line 100) requires posting "only with an explicit `--post-pr` in the brief (WC-9)", but "Other required change" says "none". Inventory A records only the default and `--no-post-pr` (`INV-A:38`). If `--post-pr` does not exist, the brief cannot opt in, and the required change is a new flag.
- Sentence: an implementer who follows the row leaves the flag absent; D4 and WC-9 then have no way to authorise posting.
- Recommendation: list "add `--post-pr`" as a required change, or state that posting stays off and remove the phrase.
- Priority: Medium. Impact: low (fails closed).
- Evidence: spec line 100; `INV-A:38` (checkable).

### F16 (non-blocking, other, MAJOR label, Medium): the sentinel `--unattended` in quoted content is not addressed
- Expert: Whittaker (sentinel collision, FR-2.3).
- Issue: D1 (line 228) says the flag "cannot misfire on a person", but nothing says whether the token inside a quoted argument (for example a bug report that mentions `--unattended`) switches the mode on. The command file's rule (quoted content is a quoted argument) is not carried into the spec.
- Sentence: a person who types a prompt containing the string `--unattended` silently gets unattended behaviour (gates resolve to defaults or blocked), which the spec says cannot happen.
- Recommendation: state that only a standalone token outside quoted text counts, and drop the "cannot misfire" claim unless that is true.
- Priority: Medium. Impact: low (fails toward blocked).
- Evidence: spec lines 228, 51.

### F17 (non-blocking, missing-requirement, MAJOR label, Medium): pr-submit `--monitor 0` and `--monitor 2` are unspecified
- Expert: Adzic (Given/When/Then gap), Whittaker (boundary).
- Issue: the pr-submit row (line 114) refuses only `--monitor 1` under `--unattended`. Ordinals 0 and 2 are not stated (see Guard G5). The default 3 has no y/n gate (`INV-B:89`).
- Sentence: an implementer who runs `--monitor 2` unattended may hit a y/n prompt, and the worker stalls without `worker_done`. Whether 2 prompts depends on the skill, which is UNVERIFIED here, so Medium.
- Recommendation: state the behaviour of 0 and 2 under `--unattended`, or refuse every ordinal except 3.
- Priority: Medium. Impact: medium.
- Evidence: spec line 114; `INV-B:34,91` (checkable).

### F21 (minor, other): E2 claims identical tools without evidence
- Expert: Fowler (interface), Wiegers.
- Issue: E2 (line 22) says a command run by a worker "has the same tools as a command a person runs". No checkable evidence supports tool equality; CAPS:161 only says a worker is a top-level session.
- Recommendation: reword as "is a top-level session; tool parity is UNVERIFIED", and add that to the UNVERIFIED list.
- Evidence: spec line 22; `CAPS:161` (checkable).

## === ARCHITECTURE ANALYSIS ===

### F3 (blocking, unpassable-check): AC-C1 forbids text that P0 requires
- Expert: Fowler (lead), Newman.
- Issue: AC-C1 (line 172) greps `src/superclaude/core` for `orca orchestration|worktree|terminal|agent` and must print nothing; it runs in every phase, including P0. P0 (line 158) requires an Orca section in `HOW-WE-WORK.md` (core), and SA-2 (line 147) allows the contract file (also in core) to name the caller's `ask` channel as an example.
- Sentence: an implementer who writes the P0 Orca section, or an `orca orchestration ask` example in WORKER-CONTRACT.md as SA-2 allows, fails AC-C1 in P0, so P0 cannot pass.
- Recommendation: exclude `src/superclaude/core/HOW-WE-WORK.md` and `WORKER-CONTRACT.md` from AC-C1, or state that the Orca section and examples are allowed and the check scans only commands, skills and agents.
- Priority: High. Impact: high (P0 cannot close).
- Evidence: spec lines 147, 158, 172.

### F4 (blocking, unpassable-check): AC-C1 misses Orca calls that SA-2 forbids, and in raw form matches nothing
- Expert: Fowler, Hohpe (message channel).
- Issue: SA-2 (line 147) forbids any `orca` or `orca-ide` command in commands, skills and agents. AC-C1 matches only the subcommands `orchestration`, `worktree`, `terminal` and `agent`, so `orca-ide status --json` or `orca open` passes. Copied from the raw table cell, the `\|` alternation is escaped and is read as a literal pipe, so the pattern matches nothing and the check passes on any file.
- Sentence: a command that runs `orca-ide status --json` passes AC-C1, and then fails with `runtime_unavailable` outside Orca (`CAPS:147`), which SA-2 exists to prevent.
- Recommendation: use the pattern `\borca(-ide)?[[:space:]]+[a-z]` (excluding the ccsession-tag path), and state the pipe escaping in the command text so it is not copied raw.
- Priority: High. Impact: high (standalone use breaks, undetected).
- Evidence: spec lines 147, 172; `CAPS:145-149` (checkable: `runtime_unavailable`).

### F11 (non-blocking, other, MAJOR label, Medium): the tasklist "no change" depends on an unverified nesting depth
- Expert: Nygard (failure modes), Fowler.
- Issue: the tasklist row (line 122) says the reflect fan-out "runs one layer below the worker, inside Claude Code's nesting limit" and so needs no change. Stage 10.5 runs reflect inside subagents, and reflect's Tier 2 adds reviewers and adversarial debate beneath that. Inventory A says at the depth limit Claude Code "withholds the Agent tool" (`INV-A:14`), and Inventory B marks nested spawning UNVERIFIED (`INV-B:314`, `INV-B:322`). The spec does not count the depth.
- Sentence: if the depth reaches the limit, Tier 2 reviewers silently disappear and the run still reports success; this needs the depth assumption, so Medium.
- Recommendation: count the depth for Stage 10.5 and state the result, or add a check that the reviewer count matches the plan.
- Priority: Medium. Impact: medium.
- Evidence: spec line 122; `INV-A:14`, `INV-B:46`, `INV-B:322` (checkable).

### F12 (non-blocking, missing-requirement, MAJOR label, Medium): the ask and stall policy has no bound
- Expert: Nygard (lead for reliability), Hohpe.
- Issue: WC-3 (line 61) lets a worker resume its ask "on an ask timeout", with no maximum. Section 1.4 (line 44) says a silent stall with no `worker_done` is the real failure mode, and section 7.2 step 3 waits with `--timeout-ms 900000` with no retry or give-up rule. Section 2.3 has no escalation rule for a stall.
- Sentence: a question the coordinator never answers keeps the worker parked for an unbounded time, and the coordinator has no rule for when to stop waiting.
- Recommendation: give a maximum number of ask resumptions and a stall rule (for example, after N checks with `agentWait` set, the coordinator escalates to the person), citing the Orca limit in `CAPS:188` as UNVERIFIED.
- Priority: Medium. Impact: medium.
- Evidence: spec lines 44, 61, 73 (section 7.2 step 3 at line 182); `CAPS:188` (UNVERIFIED in spec).

### F13 (non-blocking, other, MAJOR label, Medium): WC-11 is not met by fixed default paths
- Expert: Fowler, Nygard.
- Issue: WC-11 (line 69) requires default output paths to "carry a timestamp or the slug the coordinator passes". index-repo writes a fixed `PROJECT_INDEX.md` and its row (line 86) only adds an output location. init-lite keeps `.dev/superclaude/context-audit.md` (line 87). Only cleanup-audit gets a coordinator rule ("one audit per worktree at a time").
- Sentence: two index-repo workers in one worktree overwrite each other's index. The index is regenerable, so the consequence is Medium.
- Recommendation: give index-repo and init-lite a slug or timestamp, or state the one-worker-per-worktree rule in section 2.3.
- Priority: Medium. Impact: low.
- Evidence: spec lines 69, 85-87; `INV-A:53,55` (checkable).

### F18 (non-blocking, missing-requirement, MAJOR label, Medium): an older install has no `~/.claude/WORKER-CONTRACT.md`
- Expert: Newman (evolution), Hohpe.
- Issue: every changed command points to the installed contract path (line 52) and the contract is installed by `superclaude install`. A user with an older install who runs a command in another project gets a missing file. The spec does not say whether the command fails, falls back to inline rules, or ignores the file.
- Recommendation: state that an unattended run without the contract file stops as `blocked` with the file path as `blocked_question`, or add a version check.
- Priority: Medium. Impact: medium.
- Evidence: spec lines 52, 149 (SA-4 notes, checkable).

### F19 (non-blocking, other, MAJOR label, Medium): the plugin mirror is not in the phases
- Expert: Newman.
- Issue: UNVERIFIED 8 (line 279) says the plugin mirror `plugins/superclaude/commands/` is not yet understood and must be resolved before each phase. No phase or AC assigns that work, and AC-C2 (line 173) checks only `.claude/`.
- Sentence: the command edits in P1 to P4 leave the plugin copies stale, and `make verify-sync` still passes.
- Recommendation: add an AC that compares the plugin commands with `src/superclaude/commands/` for every edited file, or assign the resolution to P0.
- Priority: Medium. Impact: medium.
- Evidence: spec lines 173, 279.

### F20 (minor, other): WC-4 states as fact that Orca does not check the report file
- Expert: Hohpe (message integrity).
- Issue: WC-4 (line 62) says "Orca does not check the file", but its own evidence is "CAPS:79 (Orca's handling of the file is UNVERIFIED)" and UNVERIFIED 3 (line 274) repeats it. The design still holds because the coordinator opens the file, so this is a wording fix.
- Recommendation: change to "Orca's check of the file is UNVERIFIED; the coordinator opens it regardless".
- Evidence: spec lines 62, 274; `CAPS:79` (checkable).

## Adversarial probes (Whittaker, active in every panel review)

- Attack 1, sentinel (FR-2.3): the string `--unattended` in quoted text. Finding F16.
- Attack 2, zero (FR-2.1): a zero-byte or unparseable contract. Finding F5.
- Attack 3, sequence (FR-2.4): `worker_done` is sent once, but a `consumer_fenced` worker must stop without sending it (WC-12). The spec does not say what the coordinator does when a fenced worker's report exists. Covered by F12 (no stall or fence policy).

## Guard Condition Boundary Table (FR-8 to FR-10)

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|-------|----------|-----------------|----------------|--------------|-------------------|--------|
| G1 WC-5 outcome | spec line 63 | Zero/Empty | no report file | n/a | `failed` ("no report exists") | OK |
| G1 WC-5 outcome | spec line 63 | Zero/Empty | zero-byte report file | n/a | not stated; "otherwise" gives `succeeded` | GAP (F5, blocking) |
| G1 WC-5 outcome | spec line 63 | One/Minimal | `status: succeeded`, no `command` key | succeeded | `succeeded` (missing key not checked by mapping) | OK |
| G1 WC-5 outcome | spec line 63 | Typical | `status: succeeded` | succeeded | `succeeded` | OK |
| G1 WC-5 outcome | spec line 63 | Sentinel value match | `status: Failed` or `status: ok` | n/a | `succeeded` by "otherwise" | GAP (F5, blocking) |
| G1 WC-5 outcome | spec line 63 | Legitimate edge | `status: partial` | succeeded | `succeeded`, rationale in Decisions line 263 | OK (downstream effect in F8) |
| G1 WC-5 outcome | spec line 63 | Legitimate edge | `status: blocked` | failed | `failed` | OK |
| G2 `--unattended` | spec lines 51, 228 | Zero/Empty | flag absent | n/a | SA-1: today's behaviour | OK |
| G2 `--unattended` | spec lines 51, 228 | Typical | flag present in brief | unattended | section 3 rows | OK |
| G2 `--unattended` | spec lines 51, 228 | Sentinel value match | token inside quoted prompt text | not stated | not stated | GAP (F16, Medium) |
| G2 `--unattended` | spec lines 51, 228 | Legitimate edge | with `--interactive` | not stated for most commands | refused per row for cleanup, improve, roadmap, business-panel, explain only | GAP (F14 family, Medium) |
| G3 WC-10 wait | spec line 68 | One/Minimal | 1-minute call | no split | not stated for <4 min, OK | OK |
| G3 WC-10 wait | spec line 68 | Typical | 3-minute call | no split | no split (text is ambiguous above 4) | OK |
| G3 WC-10 wait | spec line 68 | Legitimate edge | 4.5-minute call | split or not | "longer than 5" vs "at most 4" | GAP (F9, Medium) |
| G3 WC-10 wait | spec line 68 | Sentinel value match | exactly 5 minutes | not split by trigger | cli-eval row says always split | GAP (F9, Medium) |
| G3 WC-10 wait | spec line 68 | Maximum/Overflow | 6-minute single call | split to at most 4 | split | OK |
| G4 confidence | spec line 121 | Zero/Empty | confidence 0.00 | blocked | `blocked` ("below 0.70") | OK |
| G4 confidence | spec line 121 | Sentinel value match | exactly 0.70 | proceeds | implied by "below 0.70"; not stated | OK (implied) |
| G4 confidence | spec line 121 | Legitimate edge | 0.69 | blocked | `blocked` | OK |
| G4 confidence | spec line 121 | Typical | 0.85 | proceeds | implied; not stated | OK (implied) |
| G5 `--monitor` | spec line 114 | Zero/Empty | `--monitor 0` | not stated | not stated | GAP (F17, Medium) |
| G5 `--monitor` | spec line 114 | One/Minimal | `--monitor 1` | refused | refused under `--unattended` | OK |
| G5 `--monitor` | spec line 114 | Sentinel value match | `--monitor 2` | not stated | not stated | GAP (F17, Medium) |
| G5 `--monitor` | spec line 114 | Typical | `--monitor 3` (default) | no y/n gate | not stated in spec; `INV-B:89` | OK (from inventory) |
| G6 contract directory | spec lines 62, 73 | Zero/Empty | no `--output` (workflow, research) | not defined | not defined | GAP (F1, blocking) |
| G6 contract directory | spec lines 62, 73 | One/Minimal | file-valued `--output <file>` (init-lite) | not defined | not defined | GAP (F1, blocking) |
| G6 contract directory | spec lines 62, 73 | Typical | `--output <dir>` (brainstorm, adversarial) | `<dir>/return-contract.yaml` | stated | OK |
| G6 contract directory | spec lines 62, 73 | Sentinel value match | `<dir>` does not exist yet | not defined | creation not stated | GAP (F1, Medium) |
| G6 contract directory | spec lines 62, 73 | Legitimate edge | stop before any output exists | contract written | stated for workflow, path undefined | GAP (F1, blocking) |

Classes left out: G1 Maximum/Overflow (the status is a closed set, and unknown values are covered by the Sentinel row); G2 One/Minimal and Maximum (the flag is boolean); G3 Zero (no wait, no step); G4 One/Minimal (a continuous value; zero and typical rows cover it); G5 Maximum (the ordinal set is {0,1,2,3}, all listed).

## ARCHITECTURE and REQUIREMENTS notes (not findings)

- Fowler: `--unattended` bundles four behaviours (no gates, outward defaults off, a report file, fresh output). That is a design choice the spec makes explicit in D1 and is acceptable; no finding.
- Newman: the contract has no version field, while workflow already writes "contract 1.1". Adding a version to WORKER-CONTRACT.md is a suggestion, folded into F5's mapping table.

## Follow-up candidates (Medium and minor; not revision triggers)

- F8 (partial and blocked handling), F9 (WC-10 threshold), F10 (pr-submit 600 s reading), F11 (tasklist nesting), F12 (ask and stall bound), F13 (WC-11 fixed paths), F14 (requirements without owner or check), F15 (`--post-pr`), F16 (sentinel `--unattended`), F17 (`--monitor` 0 and 2), F18 (missing contract file on older installs), F19 (plugin mirror), F20 (Orca check of report wording), F21 (tool parity wording).
- The loop asks the user once whether to open issues for these. This subagent cannot ask, so none is created; the list is recorded only.

## Expert consensus and disagreements

- Consensus: the decision (Orca coordinates, commands stay units of work) is sound; the gaps are in the contract's edges (F1, F5, F7) and in the verification plan (F3, F4).
- Disagreement recorded, not resolved: whether a relayed Ruling counts (D2) and whether pr-submit runs as a worker (D3). Both are the user's decisions; no finding.

## Quality assessment (0-10, reviewer judgement)

- Clarity: 6 (terms are defined, but section 3 rows mix the two meanings of "ready")
- Completeness: 7 (all commands accounted for: 10 + 27 + 6 = 43)
- Testability: 5 (AC-C1 defect, missing checks for WC-1, WC-3, WC-6, WC-10, WC-11)
- Consistency: 4 (F1, F2, F5, F6, F7)
- Overall: 5

## Advisory (not a finding)

The spec has numeric guards (60 s, 0.70, 4 and 5 minutes, 600 s, 900000 ms, three failures) and several mutable state holders (ledger, contract, memory keys, Task status). The auto-suggestion threshold for `--focus correctness` is met. Recommend a later round with `--focus correctness`. Advisory only.

## Findings block

```findings-v1
{"id": "F1", "severity": "MAJOR", "blocking": true, "category": "contradiction", "anchor": "One report file, known before dispatch, written on every outcome.", "anchor2": "contract naming the generated `claudedocs/research_*.md` path", "refs": ["WC-4", "2.3", "3.1 workflow", "3.1 init-lite", "3.2 research"], "claim": "WC-4 requires a report path known before dispatch, but workflow, research and init-lite rows give paths that are generated, file-valued or undefined."}
{"id": "F2", "severity": "MAJOR", "blocking": true, "category": "contradiction", "anchor": "The only command changes are the small fixes in the last column.", "anchor2": "the `--unattended` flag accepted by every command in sections 3.1 and 3.2", "refs": ["3.1", "P1", "AC-1.1"], "claim": "Section 3.1 says ready commands change only by small fixes, but P1 and AC-1.1 require the unattended flag and section in each of them."}
{"id": "F3", "severity": "MAJOR", "blocking": true, "category": "unpassable-check", "anchor": "add an Orca section to `HOW-WE-WORK.md` and its two mirrored copies", "anchor2": "src/superclaude/agents src/superclaude/core", "refs": ["P0", "AC-C1", "SA-2"], "claim": "AC-C1 runs in every phase over src/superclaude/core and forbids Orca orchestration text that P0 requires there, so P0 cannot pass."}
{"id": "F4", "severity": "MAJOR", "blocking": true, "category": "unpassable-check", "anchor": "No command, skill or agent file runs an `orca` or `orca-ide` command", "anchor2": "prints nothing (SA-2, WC-8)", "refs": ["SA-2", "AC-C1"], "claim": "AC-C1 matches only four orca subcommands, so a command running orca-ide status passes; in raw form the escaped alternation matches nothing."}
{"id": "F5", "severity": "MAJOR", "blocking": true, "category": "other", "anchor": "`--outcome succeeded` otherwise, including `partial`", "anchor2": "Commands that already write a contract keep their fields and add the missing ones.", "refs": ["WC-4", "WC-5", "Decisions"], "claim": "An unknown, mis-cased or empty report status maps to succeeded by the otherwise rule, so a failed run is reported as done."}
{"id": "F6", "severity": "MAJOR", "blocking": true, "category": "contradiction", "anchor": "The only end-to-end proof is the PR #329 run", "anchor2": "invocation_method: \"skill-direct\"", "refs": ["E3", "1.4", "UNVERIFIED 1"], "claim": "E3 cites a skill-direct worker contract as evidence, while section 1.4 and UNVERIFIED 1 say no direct-route run was observed."}
{"id": "F7", "severity": "MAJOR", "blocking": true, "category": "other", "anchor": "Under `--unattended`, the `--depth deep` short-input STOP and the `--fix` offer resolve as blocked (P2)", "anchor2": "These run as workers now if the brief uses the stated flags", "refs": ["3.1 troubleshoot", "INV-B:49"], "claim": "The troubleshoot brief rule allows a --depth deep short-input STOP that asks a person, so a stated brief can stall without worker_done."}
{"id": "F8", "severity": "MAJOR", "blocking": false, "category": "missing-requirement", "anchor": "After `worker_done`, the coordinator opens the report file, then releases or reuses the worker", "anchor2": "A partial run left a usable deliverable; `failed` would tell the coordinator the work is lost.", "refs": ["2.3", "Decisions"], "claim": "No rule for blocked re-dispatch or for dependents of a partial Task, which Orca settles as complete."}
{"id": "F9", "severity": "MAJOR", "blocking": false, "category": "other", "anchor": "must be split into waits of at most 4 minutes", "anchor2": "A command step that blocks a single tool call for longer than 5 minutes", "refs": ["WC-10", "3.2 cli-eval"], "claim": "The split trigger (longer than 5 minutes) and the size rule (at most 4 minutes) leave 4 to 5 minute calls undecided."}
{"id": "F10", "severity": "MAJOR", "blocking": false, "category": "other", "anchor": "the 600 s default is a cumulative per-wait budget over poll-then-sleep iterations", "anchor2": "pr-submit's 600 s is a cumulative per-wait budget", "refs": ["WC-10", "3.2 pr-submit", "INV-B:34"], "claim": "The spec reads pr-submit's 600 s as cumulative, which contradicts the inventory's per-wait reading and rests on lines not re-read."}
{"id": "F11", "severity": "MAJOR", "blocking": false, "category": "other", "anchor": "its reflect fan-out runs one layer below the worker, inside Claude Code's nesting limit", "refs": ["3.2 tasklist", "INV-A:14", "INV-B:322"], "claim": "The no-change verdict for tasklist assumes a nesting depth the spec does not count; at the limit reviewers silently disappear."}
{"id": "F12", "severity": "MAJOR", "blocking": false, "category": "missing-requirement", "anchor": "On an `ask` timeout it resumes the same message ID and never creates a duplicate.", "anchor2": "is a silent stall with no `worker_done`", "refs": ["WC-3", "1.4", "7.2 step 3"], "claim": "Ask resumption and the stall wait have no bound and no escalation rule."}
{"id": "F13", "severity": "MAJOR", "blocking": false, "category": "other", "anchor": "Default output paths carry a timestamp or the slug the coordinator passes", "anchor2": "`PROJECT_INDEX.md` (location implied)", "refs": ["WC-11", "3.1 index-repo", "3.1 init-lite"], "claim": "Fixed default paths for index-repo and init-lite let two workers in one worktree overwrite each other's output."}
{"id": "F14", "severity": "MAJOR", "blocking": false, "category": "missing-requirement", "anchor": "Launch setup, not commands", "anchor2": "7.2 live check on each P1 command with `--unattended --output <dir>`", "refs": ["WC-1", "WC-3", "WC-6", "WC-10", "WC-11", "section 7"], "claim": "WC-1 has no owning phase or check, and WC-3, WC-6, WC-10 (cli-eval) and WC-11 have no acceptance check."}
{"id": "F15", "severity": "MAJOR", "blocking": false, "category": "missing-requirement", "anchor": "posting returns only with an explicit `--post-pr` in the brief (WC-9)", "anchor2": "`--unattended` implies `--no-post-pr` and `--no-remediation-offer`", "refs": ["3.2 auggie-review", "WC-9", "INV-A:38"], "claim": "The row requires an explicit --post-pr flag that is not evidenced, while its required-change column says none."}
{"id": "F16", "severity": "MAJOR", "blocking": false, "category": "other", "anchor": "It is testable by grep and cannot misfire on a person.", "anchor2": "Explicit `--unattended` flag in the brief (recommended)", "refs": ["D1", "2.1"], "claim": "The sentinel token inside quoted prompt text is not excluded, so the cannot-misfire claim is unsupported."}
{"id": "F17", "severity": "MAJOR", "blocking": false, "category": "missing-requirement", "anchor": "`--monitor 1` refused under `--unattended`", "refs": ["3.2 pr-submit", "INV-B:34,89"], "claim": "Monitor ordinals 0 and 2 under --unattended are unspecified, and 2 may prompt."}
{"id": "F18", "severity": "MAJOR", "blocking": false, "category": "missing-requirement", "anchor": "points to the installed contract path, so the shared rules are written once", "refs": ["2.1", "SA-4"], "claim": "A command run against an install without WORKER-CONTRACT.md has no specified behaviour."}
{"id": "F19", "severity": "MAJOR", "blocking": false, "category": "other", "anchor": "How `plugins/superclaude/commands/` (which holds copies such as `agent.md`", "anchor2": "`make verify-sync` | exits 0 (SA-5)", "refs": ["UNVERIFIED 8", "AC-C2"], "claim": "The plugin mirror is not assigned to any phase and no check compares it, so it can drift while verify-sync passes."}
{"id": "F20", "severity": "MINOR", "blocking": false, "category": "other", "anchor": "Orca does not check the file, so the coordinator opens it.", "refs": ["WC-4", "CAPS:79", "UNVERIFIED 3"], "claim": "Stated as fact, but its own evidence marks Orca's check UNVERIFIED."}
{"id": "F21", "severity": "MINOR", "blocking": false, "category": "other", "anchor": "so a command run by a worker has the same tools as a command a person runs", "refs": ["E2", "CAPS:161"], "claim": "Tool parity is asserted without evidence; only top-level status is supported."}
```

Reviser brief: revise only text that blocking findings F1, F2, F3, F4, F5, F6 and F7 name. Add no rule, mechanism or section that these findings do not call for, cite the finding id on each addition, prefer deleting or narrowing to adding, and report the byte size before and after with the bytes added and deleted per finding id. Medium and minor findings (F8 to F21) are not in this brief and must not be edited for this round.

verdict: FAIL

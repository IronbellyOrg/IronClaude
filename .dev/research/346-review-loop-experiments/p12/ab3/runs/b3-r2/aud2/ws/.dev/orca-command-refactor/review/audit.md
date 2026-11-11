review: 1 of 3

# Whole-document audit: orca-worker-contract-spec.md

- Command: `/sc:spec-panel @.dev/orca-command-refactor/specs/orca-worker-contract-spec.md --mode critique --focus requirements,architecture`
- Candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`, sha256 `3df6411553609a3781774f54ed644139d6073eeb6265fab7bf239562e2658b99` (59,523 bytes, 288 lines)
- Baseline: none. This is a labelled whole-document first review (no `--re-review`, no `--baseline`). `baseline: missing` is not an error here, because neither flag was given.
- Reviewer model actually used: claude-sonnet-5-5
- Brief used: FIRST-REVIEW prompt, `~/.claude/rules/prompts/document_review_loop_prompts.md` (read in full).
- Panel: Wiegers (lead), Adzic, Cockburn (requirements); Fowler (lead), Newman, Hohpe, Nygard (architecture); Whittaker (adversarial, always active). Mode is critique, so there is no Improve step and no revised specification is written.

## Coverage statement

Covered: the whole candidate (sections 1-9, Decisions, UNVERIFIED items), read end to end. Cross-checked against `inventory/commands-a.md`, `commands-b.md` and `orca-capabilities.md` (the only checkable evidence) and `README.md`.

Arithmetic checks that passed:
- 21 + 22 = 43 commands (`inventory/commands-a.md:3`, `commands-b.md:3`).
- 10 ready (spec lines 83-92) + 27 needing change (lines 99-125) + 6 coordinator-only (lines 132-137) = 43.
- Phase lists in section 6 (line 159-162): P1 15, P2 15, P3 4, P4 3 = 37 = 10 + 27, and each command's phase in section 3 matches its phase row.

Not covered, and UNVERIFIED because the files are outside the workspace:
- All `src/superclaude/...` citations (`cmd/`, `sk/`), `CLAUDE.md:N`, `Makefile:68-74`, `pyproject.toml:38`, `src/superclaude/core/HOW-WE-WORK.md:N`, `src/superclaude/core/CLAUDE.md:65`, `src/superclaude/cli/install_core.py:N`.
- `.dev/evals/ccsession-orca-e2e-20261026/EVIDENCE.md:35,39,45,56`, `.dev/codegraph-migration/orchestration/README.md:31,33,42`, `.dev/codegraph-migration/decisions/P3-command-set/adversarial/return-contract.yaml:10`.
- Orca guide quotes (`[G]`, `[H:...]`). These are checked only through the line of `orca-capabilities.md` that quotes them.
- The spec's own claims that it re-read 11 locations and that an evidence-validator found 9 defects (spec lines 11, 289). I did not re-do them.

Heuristics: Guard Condition Boundary Table is triggered (below). Pipeline Dimensional Analysis is not triggered: the spec describes no multi-stage data flow whose output count differs from its input count; the only counted flows are the command and phase partitions, and they conserve (checked above). `--focus correctness` is not active, so no State Variable Registry is produced.

## === REQUIREMENTS ANALYSIS ===

### F-1 [MAJOR, blocking] The additive-edit check AC-C5 (and AC-0.3) cannot detect deleted lines it claims to catch

- Experts: Wiegers (testability), Whittaker (FR-2.2 divergence attack, FR-2.1 empty attack on the grep)
- Location: `specs/orca-worker-contract-spec.md:176` (AC-C5), `:193` (AC-0.3); they enforce SA-1/SA-4/SA-5 (`:146,149,150`) and the "additive" claim of `:149`.
- Grading sentence: An implementer who follows the stated text builds a gate that runs `git diff -U0 master...HEAD -- <file> | grep -E '^-[^-]'` and treats empty output as proof that edits are additive, and that is wrong because the pattern requires the second character after `-` to be a non-dash, so a deleted markdown list item (diff line `-- text`) or deleted `---` rule or frontmatter fence (diff line `----`) never matches.
- Concrete attack: the baseline has `- keep`, `- gone`, `---`; the candidate keeps only `- keep`. I ran `diff -U0` on exactly that pair through `grep -E '^-[^-]'`: the output was empty and grep exited 1, so AC-C5 and AC-0.3 report "prints nothing" (pass) although two lines were deleted. Command files are heavily bulleted (the definition of this very command, `command.md`, has `- ` list lines throughout), so the commonest deletion goes unseen.
- Why blocking: AC-C5 is the only mechanical check that SA-1 (standalone behavior unchanged), SA-4 and SA-5 (no routing row changed) hold in every phase (`:175-176`, `:193`); a passing check with a deletion is a concrete wrong outcome with no further assumption, and it hides the removal of a prompt, gate or `Will Not` rule from a person's standalone run.
- Recommendation: narrow the pattern to flag every removed line, for example `grep -E '^-' | grep -vE '^---'` (header line only) or `git diff --numstat` with deleted count 0 for the file. Delete the `[^-]` clause; do not add a new mechanism.
- Priority: High. Quality impact: restores the one gate behind SA-1.

## === ARCHITECTURE ANALYSIS ===

No blocking architecture finding. The central decision (Orca coordinates, commands stay units of work; section 1) is consistent with `orca-capabilities.md:97-103` (nesting depth 1), `:148-150` (lifecycle messages only from the dispatched pane) and `:155-161` (subagents and top-level sessions). The two arguments the spec hedges (subagent limits, heartbeat use) are stated as UNVERIFIED at `:43-45` and `:272-286`. Medium findings follow in the list below.

## Expert panel notes (critique mode, review sequence order)

- Wiegers: requirements WC-1..WC-12 each carry an owner and evidence, but WC-1, WC-3, WC-7 and WC-12 are obligations on the worker session or on launch setup with no deliverable in any phase (see M-5). The rest are testable through section 7.
- Adzic: section 7 gives executable examples for most requirements. The P0 smoke check (AC-0.4) mixes pre-contract and post-contract pass conditions (M-3).
- Cockburn: the primary actors (person, coordinator, worker session, command) are named and the coordinator brief (`:73`) is the actor-goal contract. The flags the brief must carry are not all defined (M-1, M-2).
- Fowler: separation of concerns is clean: shared rules in one contract file (`:52`), per-command deltas in section 3. The `AC-C1` guard scans the directory that holds the contract file and the routing guide (M-6).
- Nygard: failure modes are covered (blocked, failed, partial, retry, fenced). Gap: long Agent-tool calls cannot heartbeat (M-4).
- Whittaker: see the attack list under the boundary table.
- Newman: versioning of the contract file against installed commands is not stated (a command that names `~/.claude/WORKER-CONTRACT.md` on a machine whose core files lack it). The fix is installation order; the spec adds the file to `KNOWN_CORE_FILES` (`:52`, UNVERIFIED line). Minor (m-3).
- Hohpe: the report is a pointer file read by the coordinator (`:62`, `CAPS:79`). The message exchange (`worker_done`, `ask`, `check`) is specified; ordering is exactly once (`:63`, `:70`). No finding.

## Guard Condition Boundary Table

Guards enumerated (all numeric, boolean or enumerated guards in the spec): G1 readiness limit 60 s (`:59`); G2 heartbeat 5 min / wait 4 min (`:68`); G3 nesting depth 1 (`:33`, `:66`); G4 `status` enum (`:62`); G5 outcome mapping (`:63`); G6 `--unattended` selector (`:51`, `:227-230`); G7 confidence < 0.70 on `task` (`:121`); G8 retry / circuit breaker 3 failures (`:64`, `CAPS:116`); G9 `--monitor 1` refusal (`:114`). Input classes left out are each given a reason in the Specified Behavior column.

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|-------|----------|-----------------|----------------|--------------|-------------------|--------|
| G1 readiness | WC-1 `:59` | Zero/Empty | `--timeout-ms 0` or absent | not positive, default 60 s used | `CAPS:44` (inventory): non-positive falls back to 60 s; spec itself silent | OK |
| G1 readiness | WC-1 `:59` | Typical | prompt fallback 30 s | true | passes (`EVIDENCE.md:45`, UNVERIFIED) | OK |
| G1 readiness | WC-1 `:59` | Legitimate Edge Case | fallback just above ~45 s | false | fails again (`EVIDENCE.md:56`, UNVERIFIED); "well inside" is not a number | GAP (see M-5) |
| G2 wait split | WC-10 `:68` | Typical | 600 s poll made of iterations under 4 min | true | split, heartbeat between | OK |
| G2 wait split | WC-10 `:68` | Maximum/Overflow | one Agent-tool call longer than 5 min (fan-out) | not addressed | rule covers only a "single tool call" wait; Agent-tool fan-out is not split | GAP (M-4) |
| G2 wait split | WC-10 `:68` | Zero/Empty | wait of 0 s | n/a | one line: a zero wait cannot exceed 5 min | OK |
| G3 depth | WC-8 `:66`, R1 `:33` | Typical | depth 1 | worker may not start workers | commands never call `worker-start` | OK |
| G3 depth | WC-8 `:66` | Legitimate Edge Case | depth raised by user (D5) | true | D5 recommends keeping 1; WC-8 forbids anyway | OK |
| G3 depth | WC-8 `:66` | Sentinel Value Match | `task-create` from depth-1 worker | unknown | UNVERIFIED (`CAPS:103,180`); WC-8 forbids either way | OK |
| G4 status enum | WC-4 `:62` | Zero/Empty | no contract file (crash before write) | missing | WC-5 `:63`: no report means `--outcome failed` | OK |
| G4 status enum | WC-4 `:62` | Sentinel Value Match | command-native status (e.g. workflow's own `status`) outside the four values | not in set | "Commands that already write a contract keep their fields and add the missing ones"; mapping of native values to the four is not stated | GAP (m-1) |
| G5 outcome map | WC-5 `:63` | Legitimate Edge Case | `partial` | maps to `succeeded` | decided at `:263`; body states `partial` | OK |
| G5 outcome map | WC-5 `:63` | Legitimate Edge Case | audit verdict FAIL | `succeeded` | stated | OK |
| G6 selector | D1 `:227-230` | Sentinel Value Match | `--unattended` inside quoted specification or prompt text | ambiguous | token parsing rule not stated (a quoted argument could trip the mode) | GAP (M-7) |
| G6 selector | D1 `:227-230` | Zero/Empty | flag absent | false | SA-1 `:146`: today's behavior | OK |
| G7 confidence | `task` row `:121` | One/Minimal | exactly 0.70 | false (not below) | "below 0.70 resolves as blocked"; 0.70 runs; matches `cmd/task.md:93` text per `INV-B:197-205` | OK |
| G7 confidence | `task` row `:121` | Zero/Empty | 0.0 | true | blocked | OK |
| G8 retry | WC-6 `:64`, `:73` | Maximum/Overflow | 3rd consecutive failed start | circuit breaks | `CAPS:116,80`; spec says own `failed` reports do not count, `blocked` ends `failed` so many `blocked` retries never trip it | OK |
| G9 monitor | `pr-submit` row `:114` | Typical | `--monitor 1` | refused | stated | OK |
| G9 monitor | `pr-submit` row `:114` | Legitimate Edge Case | `--monitor 0`, `--monitor 2` | not addressed | only `1` is refused; the other ordinals are not described under `--unattended` | GAP (m-2) |

FR-8 / FR-9 grading: the GAP rows name no concrete wrong outcome an implementer would produce from stated text (each needs a guess about the reading or concerns a requirement the spec never states), so they are Medium or minor, listed under follow-up candidates, and do not block. FR-10: every guard is enumerated, every cell populated, and each missing input class carries its one-line reason, so the table is complete.

### Whittaker attacks (FR-3 format)

1. I can break this specification by **Zero/Empty Attack**. The invariant at **WC-4 `:62` ("written on every outcome, including stops before any other output exists")** fails when **the `--output` directory the coordinator passed does not exist or is unwritable**. Concrete attack: before = brief passes `--output /ro/dir`; the command starts, cannot create `/ro/dir/return-contract.yaml`; after = no contract, worker applies WC-5 "no report exists" and reports `failed`, so the outcome is correct but the cause is lost. Impact: diagnosability only, covered by WC-5; minor (m-4).
2. I can break this specification by **Divergence Attack**. The invariant at **AC-0.4 `:194`** fails when **the smoke command writes no contract (troubleshoot writes `REPORT.md`; the common check at `:183` parses YAML)**. Concrete attack: run `/sc:troubleshoot`; `REPORT.md` is Markdown; 7.2 step 4's `yaml.safe_load` asserts `d['status']`, which fails; AC-0.4 says "step 4 uses the command's existing report file" without saying what is asserted. See M-3.
3. I can break this specification by **Sequence Attack**. The invariant at **WC-5/WC-12 `:63,:70`** ("`check` once before `worker_done`; if `consumer_fenced`, stop") fails when **`worker_done` is already sent** and a later `check` returns `consumer_fenced`. Concrete attack: send `worker_done` first by mistake, then `check`; the spec says "exactly once" but not the order is enforced. The order is stated ("once before"), so no finding.
4. I can break this specification by **Accumulation Attack**. The invariant at **WC-6 `:64`/`:73`** (fresh output directory per retry) fails when **a coordinator retries many times**: each retry creates a new directory with a full report set; no cleanup or cap beyond Orca's 3-failure breaker (`CAPS:116`). Stated behavior is consistent; storage growth is out of scope. No finding.
5. I can break this specification by **Sentinel Collision Attack**. The invariant at **WC-4 `:62` (`<file name>.return-contract.yaml` beside a `--output` file)** fails when **the user's `--output` file is itself named `*.return-contract.yaml`**. Concrete attack: `--output out.return-contract.yaml` yields contract `out.return-contract.yaml.return-contract.yaml`; harmless. No finding.

## Findings by grading

### Blocking (1)

- F-1 above.

### follow-up candidates (Medium, not blocking)

- M-1 [Medium, label MAJOR] `--post-pr` and the `task` commit/push authorization flag are not defined. WC-9 (`:67`) says outward defaults turn on "only through the command's own explicit flag"; the `auggie-review` row (`:100`) relies on "an explicit `--post-pr` in the brief" and AC-2.4 (`:202`) tests that, but `INV-A:38,78` records only `--no-post-pr` (posting is on by default); the `task` row (`:121`) says EXEMPT `commit`/`push` are "refused unless authorized" but `INV-B:197-205` shows they are keywords in the prompt (`cmd/task.md:80`), with no flag. The row's "Other required change" column says "none". An implementer must invent the flags. Medium because it is a requirement the document never states, not a stated text that does harm. Recommendation: say whether `--post-pr` and a task-authorization flag are new, or drop the positive flag and make posting simply absent under `--unattended`.
- M-2 [Medium] The contract location is not determined for several rows although WC-4 (`:62`) promises it is "known before dispatch": `cli-portify` (`:105`, "file location unnamed"), `research` (`:116`, no output flag named), `review-translation` (`:117`), `save` (`:119`), `recommend` (`:115`) name a contract with no `--output`/`--output-dir` flag or path. AC-2.2 (`:200`) tests `test -s <contract>` for P2 commands. Recommendation: name the output flag or path in each row.
- M-3 [Medium] AC-0.4 (`:194`) and 7.2 steps 3-4 (`:182-183`) assume a WC-4 contract with `status`/`command`, which does not exist until P1 (`:194` itself says "the contract arrives in P1"). For `/sc:troubleshoot` the report is `REPORT.md` (`:91`); the step-3 text "outcome matches the contract's status" and step-4 YAML assert cannot be evaluated. The doc points at "the command's existing report file" without a pass condition. Recommendation: state, for the three smoke commands, what step 3 and 4 assert (for example report file non-empty; outcome matches the report's own verdict).
- M-4 [Medium] WC-10 (`:68`) splits only single tool-call waits; a long Agent-tool fan-out call (adversarial, tdd, troubleshoot Tier 2, `INV-A:35-55`) blocks the top-level session for the whole call and no heartbeat can be sent. Orca's use of heartbeat age is UNVERIFIED (`CAPS:130`), so harm is unproven. Recommendation: state that Agent-tool calls are exempt, or that the coordinator should read `worker-show` instead.
- M-5 [Medium] WC-1 (`:59`) names an owner "Launch setup, not commands" but no phase, deliverable or acceptance check changes the launch path, and "well inside the readiness limit" has no number (its own evidence says 30 s passes and about 45 s fails). Only AC-0.4 step 1 (`:180`) indirectly exercises it. Also, the spec narrows the binding statement at `README.md:13` ("a worker that waits on a question fails the 60-second limit") to a pre-input-box prompt (`:44`) on the strength of `EVIDENCE.md:39`, which I cannot check (UNVERIFIED); `CAPS:52` quotes it consistently, and the design holds either way because WC-2 forbids waiting. Recommendation: assign WC-1 to a phase or move it out of the requirement list; give the fallback a number.
- M-6 [Medium] SA-2 (`:147`) allows an Orca mention only "inside the contract file", while P0 (`:158`) also adds an Orca section to `HOW-WE-WORK.md`, and AC-C1 (`:172`) scans `src/superclaude/core`. Whether the permitted text matches `orca (orchestration|worktree|terminal|agent)` is not stated; a routing-guide section describing the coordinator flow would normally contain exactly that, and E5 (`:25`) records 0 mentions today. Needs a guess about wording, hence Medium. Recommendation: exclude the two named files from AC-C1 or say the text must avoid the pattern.
- M-7 [Medium] Selector parsing: the spec never says that `--unattended` counts only as a standalone argument token outside quoted content (D1 `:227-230`; `:51`). A quoted prompt containing `--unattended` could switch the mode on for a person. Recommendation: one sentence in WC-2 or section 2.1.
- M-8 [Medium] `--unattended` acceptance on `/sc:load` is contradictory by omission: the P1 row (`:159`) says the flag is accepted by "every command listed in this row", `load` is listed "(usage line only; no `## Unattended mode` section)", and the `load` row (`:112`) names only the `--checkpoint` usage fix. Whether a brief may pass `--unattended` to `load` (section 2.3 `:73` says every brief carries it) is unspecified.
- M-9 [Medium] `/sc:pr-submit` states "Will Not: run headless / imply a daemon" (`INV-B:90`, citing `cmd/pr-submit.md:85`, `SKILL.md:225`). D3 (b) and the P4 row (`:114`, `:241`) treat pr-submit as a worker without addressing that rule. D3 recommends (a), so the harm arises only if the user picks (b). Recommendation: add the rule to D3 (b).
- M-10 [Medium] Section 2.3 (`:73`) and 7.2 step 1 (`:180`) say every brief includes `--unattended`; section 3.1 (`:79`) and AC-0.4 (`:194`) run the ready commands without it before P1/P2 add it. The two readings diverge for the P0 smoke runs; the spec means "once the flag exists". Add that qualifier.
- M-11 [Medium] E3 (`:23`) cites `invocation_method: "skill-direct"` as evidence the approach worked, while section 1.4(1) (`:43`) says the PR #329 run proves only the nested subagent route. `INV-A:35` records the same field as "proven as a direct Orca-worker skill call". The two statements are not reconciled; the underlying files are UNVERIFIED here (`.dev/codegraph-migration/...:31,33`, `return-contract.yaml:10`).

### minor notes

- m-1 WC-4 (`:62`): commands that already write a contract "keep their fields"; the mapping from native status values to `succeeded/partial/failed/blocked` is not given (workflow's own statuses are at `INV-B:272`).
- m-2 `pr-submit` (`:114`) only refuses `--monitor 1`; behavior of `--monitor 0` and `2` under `--unattended` is silent.
- m-3 No statement of install order or version compatibility between the contract file and commands that reference it.
- m-4 Unwritable output directory: cause lost though outcome is correct (Whittaker attack 1).
- m-5 Section 4 (`:128`) cites `INV-B:311` for "making them workers would remove their purpose"; that line covers only pm, spawn and swarm-wizard. The git row (`:133`) says "read-only ones (status)" while `INV-A:91` says every operation is an outward mutation.
- m-6 E4 (`:24`) states as fact that subagents "are not counted by Orca's nesting limit"; `CAPS:155` says never-limited is UNVERIFIED. Section 1.4(3) hedges correctly; E4 should match.
- m-7 Section 3 intro (`:76`) says the inventories each had a fresh-context citation check (`INV-A:106`, `INV-B:320`); both are present and agree, but `INV-A:106` says about 290 citations and the spec's closing note (`:289`) says about 340 for the spec; no conflict.

## Self-check and constraints

- First-review grading check applied to each finding: F-1 holds with no assumption beyond "command files contain list lines", which is verified. Every M item needs a guess about which of two readings an implementer picks or concerns a requirement never stated, so it is Medium, even where its label would be MAJOR.
- Medium and minor findings never trigger revision and are excluded from the Reviser brief.
- The session that ran this review (a sandbox worker with no user channel) cannot ask the user about opening an issue for the follow-up candidates; the list is recorded here and the coordinator asks once for this loop. No issue was created.
- No brief clause was overridden. I did not edit the candidate and did not start another review. The Improve step was skipped (critique first review writes only this report).

## Reviser brief

Repair only the blocking finding F-1 in the candidate `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`. Prefer deleting or narrowing text when the requirements are still met. Add no rule, mechanism or section that a listed finding does not call for, and cite the finding id on every addition. Report the byte size before and after, and the bytes added and deleted per finding id. Leave minor and Medium findings alone. Return the candidate once and do not award yourself a PASS. Scope: change the grep pattern in AC-C5 (`:176`) and AC-0.3 (`:193`) so a removed list item or `---` line is detected; touch nothing else.

verdict: FAIL

review: 1 of 3

# Spec-panel review, round 1: orca-worker-contract-spec.md

- command: `/sc:spec-panel @.dev/orca-command-refactor/specs/orca-worker-contract-spec.md --mode critique --focus requirements,architecture`
- candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`
- candidate sha256: `d3cdbe573e57303b9ce6c93d1fe98ba18fb7cb1a15773d926bf6a0c31425200d`
- baseline: missing (first review, no `--re-review`/`--baseline`)
- reviewer model used: claude-sonnet-5-5
- prompt followed: FIRST-REVIEW prompt, `~/.claude/rules/prompts/document_review_loop_prompts.md:29-36`. This file is one reviewer's report; the three-review MERGE is the coordinator's job.
- Citations: `S:N` = line N of the candidate. `INV-A/INV-B/CAPS:N` = the inventory files under `.dev/orca-command-refactor/inventory/`. Anything I could not check inside the workspace (repo `src/` files, `orca-data.json`, Orca guides) is UNVERIFIED and I rely on the inventories' quotes only.

## Coverage

Read in full: the candidate (285 lines), README, the review-loop prompts. Checked against the inventories: `CAPS:52-80,130,149-151` (ask, report-path, heartbeat), `INV-A:3,35,42,51,53,73,96-98`, `INV-B:3,36,46,52,109,209-215,310`. Not checked (no access): any `src/` file, `CLAUDE.md`, `EVIDENCE.md`, PR #329 files. I did not audit all 43 per-command rows line by line; I read all of sections 2, 3.1, 3.2, 6, 7 and 9 and tested them against each other.

Panel (critique mode, order per command): Wiegers, Adzic, Cockburn, Fowler, Nygard, Whittaker, Newman, Hohpe, Crispin, Gregory, Hightower. Focus requirements (Wiegers lead, Adzic, Cockburn) and architecture (Fowler lead, Newman, Hohpe, Nygard). Findings are grouped by bucket below.

## Guard Condition Boundary Table (hard gate, completed before synthesis)

Guards in the candidate: the WC-4 `status` set, the WC-10 4-minute wait split, WC-5 outcome mapping, the task confidence 0.70 gate (S:121), `--monitor 1` refusal (S:114). Input classes left out are given a one-line reason.

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|---|---|---|---|---|---|---|
| contract `<output-dir>` | S:62 (WC-4) | Zero/Empty | no `--output` passed | contract has no location | WC-4 says output-dir is "the directory the coordinator passed"; nothing for a command with no directory flag (workflow S:92) | GAP (see M1) |
| contract `<output-dir>` | S:62 | Legitimate Edge Case | `--output <file>` (tdd S:90, init-lite S:87, spec-panel S:120) | directory undefined | unspecified | GAP (see M1) |
| WC-5 outcome | S:63 | Typical | `status: partial` | `succeeded` | specified | OK |
| WC-5 outcome | S:63 | Sentinel Value Match | `blocked` | `failed` | specified | OK |
| WC-5 outcome | S:63 | Legitimate Edge Case | `blocked` then WC-3 `ask` answered then re-invoke | first contract is `blocked` | what happens to the first contract and to the already-sent outcome is not stated | GAP (Medium, F2) |
| WC-10 wait split | S:68 | Maximum/Overflow | one tool call > 5 min | split to <= 4 min | specified for cli-eval and pr-submit only; other long commands not named | GAP (minor) |
| confidence gate | S:121 | Sentinel Value Match | exactly 0.70 | not stated | "below 0.70" blocked, at 0.70 unspecified | GAP (minor, boundary copied from inventory) |
| `--monitor` refusal | S:114 | Zero/Empty | `--monitor 0` | not stated | only 1 refused | OK (0 is a documented non-acting level, UNVERIFIED here) |
| WC-4 `status` | S:62 | One/Minimal | contract written before any other output exists | specified ("including stops before any other output") | OK |

Classes omitted: Maximum for the status set (closed enumeration, cannot overflow).

## Blocking findings

### B1 (MAJOR, blocking, Fowler / Wiegers): Phase 1 ships `--unattended` on every command, while the gate and outward-action rules that give the flag its meaning arrive in P2 to P4

Quoted texts:
- S:159 (P1): "the `--unattended` flag accepted by every command in sections 3.1 and 3.2 (a no-op where a command has no gate)".
- S:195 (AC-1.1): the test "asserts that every command in sections 3.1-3.2 has a `## Unattended mode` section naming `return-contract.yaml` and `~/.claude/WORKER-CONTRACT.md`".
- S:60 (WC-2): "Under `--unattended` the command never calls `AskUserQuestion`, never ends its turn on a chat question ...".
- S:67 (WC-9): "Under `--unattended`, any default that pushes ... posts to GitHub ... is off."
- S:100, S:103, S:160: auggie-review's posting-off, cleanup's approval handling and every gate conversion are P2 (S:160: "These changes touch no safety rule ... P2 only turns it off under `--unattended`").

An implementer who follows the stated text as written builds, at the end of P1, an `auggie-review` and a `cleanup` that accept `--unattended`, carry the section AC-1.1 demands, pass AC-1.1, and still post to the PR and still prompt. That is wrong because WC-2 and WC-9 define `--unattended` as never prompting and never acting outward, and the "no-op where a command has no gate" parenthesis does not cover these commands, which do have gates. The coordinator brief (S:73) is told to pass `--unattended` on every worker, so a P1-only install would post PR reviews on a fork PR and stall silently, the failure mode the spec was written to remove (S:44, point 2). The sequencing statement at S:154 ("Phases 1-3 need no user decision") does not resolve it: nothing says gated commands refuse or ignore the flag until their phase.

Reviser brief note: narrow P1 and AC-1.1 to the commands whose rows say "no gate" (and the section-3.1 commands whose row needs no gate conversion), and state that a gated command does not gain `--unattended` before its own phase.

### B2 (MAJOR, blocking, Wiegers / Adzic): WC-4 puts the contract in an "output directory" but the tdd, init-lite and spec-panel rows pass `--output` as a file

Quoted texts:
- S:62 (WC-4): "`<output-dir>/return-contract.yaml`, where `<output-dir>` is the directory the coordinator passed (`--output` / `--output-dir`)".
- S:73 (2.3): the brief states "the output directory, so the report path is known before dispatch (WC-4)".
- S:90 (tdd): brief must pass "`--output <file>`", report "the TDD at `--output`".
- S:87 (init-lite): "`--output <file>`".
- S:120 (spec-panel): "add `--output`; contract".
- S:182 (7.2 step 3): the worker's report path must be "the WC-4 contract path".

An implementer who follows the stated text as written builds, for tdd, init-lite and spec-panel, a contract whose location is either the file's parent directory (a guess) or nowhere, because no directory value exists in the brief. That is wrong because the coordinator cannot know the contract path before dispatch (WC-4, S:73), and AC step 3 (S:182) and AC-2.1 / AC-1.2 cannot be passed for those commands. Corroboration, outside the candidate's evidence: the real `/sc:spec-panel` command definition in this sandbox already says `--output` is file-valued and uses `--report-dir <dir>` for the directory (`command.md:460-461`), which is exactly the collision the spec does not handle.

### B3 (MAJOR, blocking, Cockburn / Wiegers): workflow and adversarial contract paths contradict the WC-4 location, and workflow's path is unknown before dispatch

Quoted texts:
- S:62 (WC-4): contract "known before dispatch", at `<output-dir>/return-contract.yaml`.
- S:92 (workflow): brief passes only `--handoff none`; report `.dev/tasks/to-do/<id>/return-contract.yaml`; resume "Fresh package each run". `INV-B:52` agrees: the id is generated, "never reuses a package" (`SKILL.md:72` via INV-B).
- S:83 (adversarial): fix to `<output>/adversarial/return-contract.yaml` (a subdirectory of the brief's `--output`, not `<output>` itself).
- S:198 (AC-1.4): checks only that "adversarial names one fixed path; workflow states the contract is written for pre-creation STOPs".
- S:194 (AC-0.4): P0 smoke runs use these two commands.

An implementer who follows the stated text as written builds a workflow worker whose contract lands in a directory with a generated id the coordinator cannot know, and whose "pre-creation STOP" contract (S:92, S:198) has no id directory to be written into at all. That is wrong because WC-4 and 2.3 require the path to be known before dispatch, and S:182 step 3 requires `--report-path` to equal it. The adversarial path differs from WC-4's literal `<output-dir>/return-contract.yaml` by one directory level, so a coordinator built from WC-4 looks in the wrong place. The spec never says the 3.1 per-command path overrides WC-4.

### B4 (MAJOR, blocking, Wiegers / Adzic): AC-1.1 requires a contract-naming section in `/sc:load`, which section 3 and the Decisions table say has no report

Quoted texts:
- S:195 (AC-1.1): every command in sections 3.1-3.2 has a `## Unattended mode` section "naming `return-contract.yaml`".
- S:112 (load): Report "none (see note)"; "use it as a step inside another worker's brief, not as its own Task".
- S:265 (Decisions): "a report file would be an unrequested addition. Only its usage-line defect is fixed."
- S:159 (P1): load is "usage line only".

An implementer who follows the stated text as written either adds a contract to `/sc:load` (contradicting S:112 and S:265, and SA-3 at S:148) or leaves it out and fails AC-1.1. The criterion cannot pass with the other stated texts both honoured. Section 3.2 also counts `/sc:load` among "27 needing a change" (S:76) although its only change is a usage-line fix, so the 10 / 27 / 6 split in S:76 and S:128 does not describe the work the P1 test asserts.

## Reviser brief

Blocking finding ids: B1, B2, B3, B4.

Reviser contract (restated; the reviser reads this report, not the command): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id; leave Medium and minor findings alone; do not award yourself a PASS.

- B1: S:159, S:195 (narrow scope to no-gate commands until their gate phase).
- B2: S:62, S:73, S:182 together with S:87, S:90, S:120 (one stated location rule for commands whose `--output` is a file).
- B3: S:62 against S:83, S:92, S:198.
- B4: S:195 against S:112, S:265, S:76.

## Follow-up candidates (Medium and minor; never trigger a revision)

Medium, each a warning (requirement not stated, or needs a guess):
- F1 (Medium, Nygard): SA-4 (S:149) allows "new flags" as additive, but AC-C5 (S:176) fails any removed line; adding a flag to an existing Usage line is a modified line, so AC-C5 would fail the edits SA-4 permits. Needs the guess that flags go on an existing line.
- F2 (Medium, Whittaker, sequence attack): WC-3 (S:61) lets the worker `ask`, then "re-invoke or resume the command with the answer as a flag", while WC-2(c) (S:60) already wrote a `blocked` contract and WC-5 (S:63) maps blocked to `failed`. Not stated: whether the re-run overwrites the contract, and when `worker_done` is sent. Missing rule, not a stated contradiction.
- F3 (Medium, Fowler): tasklist (S:122) and reflect (S:88) make `--unattended` reuse the headless auto-accept rule. `INV-B:215` recommended dropping `--remediate` at Stage 10.5 instead; `INV-B:109` says headless auto-accept "skips the gates". WC-2 lists three gate resolutions and auto-accept-and-skip is not one of them, and the remediation output (a `/sc:workflow` package) is not in the tasklist artifacts list. Also S:122 states tasklist's reflect fan-out is "inside Claude Code's nesting limit", while `INV-B:210` marks nested spawning UNVERIFIED.
- F4 (Medium, Hohpe): WC-10 (S:68) names only cli-eval and pr-submit for the 4-minute split; other long waits (research, tdd builders, roadmap) are not assessed, and S:182 step 2 polls `worker-show` only every 5 minutes. Heartbeat is a worker duty (WC-10) yet WC-3 says none while blocked in `ask` (`CAPS:63-64` quote); the interaction is left implicit.
- F5 (Medium, Newman): AC-C1 (S:172) greps `src/superclaude/core`, where the new `WORKER-CONTRACT.md` is created (S:52, S:158) with a brief template; SA-2 (S:147) allows an Orca mention there, but the grep's pass condition "prints nothing" could fail on that file if it quotes an `orca orchestration` command. Needs a guess about the template text.
- F6 (Medium, Crispin): the per-command resume column (WC-6) uses "fresh dir" for 20+ commands but the coordinator brief (S:73) is not required to pass a new directory on a retry; a retry given the same `--output` reuses the first attempt's directory.
- F7 (Medium, Gregory): UNVERIFIED items 1 and 9 (S:272, S:280) are load-bearing (reflect's headless detection decides F3, and no direct-route run exists), yet P0's smoke set (S:158) does not include a gate-converted command.
- F8 (Medium, Adzic): `/sc:spec-panel`'s own definition in this sandbox already implements `--unattended --report-dir` and `<report-dir>/return-contract.yaml` (`command.md:455-465`), differing from the spec's S:120 row and from the flag names in WC-4. Possibly the spec predates it; UNVERIFIED against the repo. If the spec is meant to match shipped commands, the vocabulary `--output` / `--output-dir` should be reconciled.

Minor notes:
- S:79 says the only command changes for 3.1 are "the small fixes", while S:159 and AC-1.1 add the Unattended section to them too.
- WC-8 (S:66) and S:33 repeat the same UNVERIFIED site list; harmless.
- The confidence boundary exactly at 0.70 is not defined (S:121; copied from INV-B).
- Section 3 headline "27 needing a change" includes `/sc:load`, whose change is a usage-line fix (S:76, S:112).

## Strengths worth keeping

Evidence-stated gaps in section 1.4 (S:41-45) are honest, and the rejected alternative (S:28-39) is argued from checkable inventory lines (`CAPS:97-103,145-150`). Phase ordering by risk is sound once B1 is fixed.

verdict: FAIL

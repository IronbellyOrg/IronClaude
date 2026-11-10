review: 1 of 3

# Spec-panel critique, round 1: orca-worker-contract-spec.md

- command: `/sc:spec-panel @.dev/orca-command-refactor/specs/orca-worker-contract-spec.md --mode critique --focus requirements,architecture`
- candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`, sha256 `d3cdbe573e57303b9ce6c93d1fe98ba18fb7cb1a15773d926bf6a0c31425200d` (282 lines, 57763 bytes)
- baseline: none given (first review of the full document; `--re-review` and `--baseline` absent)
- lint file: `.dev/orca-command-refactor/review/lint-1.md`, sha256 `6a70e9a1255ee5d4652078e22f1d02b3383feeb5af682b9017b29610cb1b420a`
- reviewer model actually used: claude-sonnet-5-5
- prompt followed: FIRST-REVIEW prompt of `~/.claude/rules/prompts/document_review_loop_prompts.md` (read in full)
- panel (fixed order, critique mode, focus requirements + architecture, Whittaker always active): Wiegers, Adzic, Cockburn, Fowler, Nygard, Whittaker, Newman, Hohpe

## Lint evidence
`lint-1.md:1-5`: checks REF, 0 findings, no lint ids. Nothing to confirm or dismiss. Its header hash equals the candidate hash above, so it was produced on this exact file.

## Coverage
Read all of the candidate (`spec:1-282`) and the README (`README.md:1-38`). Checked the inventory cross-references the spec relies on for its counts and its load-bearing claims: `INV-A:3,14,35,39,53,55,60-62,76-83,90,94-98,106,113,118,120`, `INV-B:31,36,52,65,105,107-115,268-275,285-299,301,311,320,323`, and `CAPS:44-47,52,58-61,64,66-68,72-79,84-92,97-103,107-116,128-130,145-151,155-161,178-188`. Count check: 21 + 22 = 43; 10 ready + 27 needs-change + 6 coordinator-only = 43; the 27 rows of section 3.2 match INV-A's 13 and INV-B's 14 needs-change lists (`INV-A:75-83`, `INV-B:289-299`).

UNVERIFIED (cannot be checked inside this workspace, which holds only `.dev/orca-command-refactor/`): every `CLAUDE.md:N`, `src/superclaude/...:N`, `cmd/...:N`, `sk/...:N`, `pyproject.toml:38`, `Makefile:68-74`, `.dev/codegraph-migration/...`, `.dev/evals/...` and `/opt/Orca/...` citation, and the grep results in E5 (`spec:25`). Where the inventories quote those sources, the quote was used and is marked "via inventory". The claims that 11 locations were re-read and that an independent validator re-checked about 340 citations (`spec:11`, `spec:282`) are likewise UNVERIFIED.

## Panel summary
The decision (Orca coordinates, commands stay units of work) is well argued and consistent with the inventories. The defects are in the contract mechanics: where the report file lives, and which phase makes a command accept `--unattended`. Two blocking findings, both stated-text contradictions. Everything else is Medium or minor.

=== REQUIREMENTS ANALYSIS ===

### REQ-1 (CRITICAL as labelled; graded BLOCKING) WC-4 says the contract path is known before dispatch, but the workflow row puts it at a command-chosen path and gives pre-creation stops no location
- Expert: Wiegers (traceability of the requirement to its rows), Adzic (the 7.2 example cannot be run for workflow)
- Texts that contradict:
  - WC-4 (`spec:62`): the report is `<output-dir>/return-contract.yaml`, "known before dispatch", "written on success, failure, blocked and partial outcomes, including stops before any other output exists". Section 2.3 (`spec:73`): the brief states "the output directory, so the report path is known before dispatch (WC-4)".
  - Section 3.1 workflow row (`spec:92`): "Brief must pass: `--handoff none`" (no output flag), report today `.dev/tasks/to-do/<id>/return-contract.yaml`, small fix "Write the contract for pre-creation STOPs too". The inventory confirms the path embeds a command-generated `<id>` and that the skill "never overwrites or reuses an existing package" (`INV-B:272-273`). AC-1.4 (`spec:198`) only checks that "workflow states the contract is written for pre-creation STOPs", with no location.
- Grading sentence: An implementer who follows the stated text as written builds a `/sc:workflow` that writes its contract into an `<id>` directory the command picks, which the coordinator's brief cannot name, and, for a stop before any package directory exists, to no stated location; that is wrong because WC-4 requires a single report file at a coordinator-passed directory, known before dispatch, on every outcome including pre-output stops, and 7.2 steps 3-4 (`spec:182-183`) require `worker_done`'s report path to equal that WC-4 contract path.
- Recommendation: Narrow WC-4 or the workflow row so they agree. Either give workflow an output-directory flag used for the contract on every outcome, or state in WC-4 that for commands that mint their own package directory the contract path is the one the command prints, and name where a pre-creation STOP writes it.
- Priority: High. Quality impact: workflow is one of the three P0 smoke runs (`spec:194`), so the first live check hits this.

### REQ-2 (MAJOR as labelled; graded BLOCKING) P1 and AC-1.1 require `--unattended` and its section on every command in 3.1/3.2, but the rows place the gate resolutions and WC-9 off-switches in P2 and P4
- Expert: Wiegers (phase traceability), Nygard (safety boundary between phases), Whittaker (sequence attack)
- Texts that contradict:
  - P1 scope (`spec:159`): "the `--unattended` flag accepted by every command in sections 3.1 and 3.2 (a no-op where a command has no gate)". AC-1.1 (`spec:195`): the test asserts every command in sections 3.1-3.2 has a `## Unattended mode` section naming `return-contract.yaml` and `~/.claude/WORKER-CONTRACT.md`. Section 2.1 (`spec:52`): that section "lists only its own gate resolutions and report file".
  - Gate resolutions and outward-default switches are scheduled later: auggie-review P2 (`spec:100`), cli-eval P2 (`spec:104`), task P2 (`spec:121`), implement P4 (`spec:109`), post-release P4 (`spec:113`), pr-submit P4 (`spec:114`); P4 "waits for answers to D2-D4" (`spec:154,162`).
  - WC-9 (`spec:67`): "Under `--unattended`, any default that pushes, opens a PR, posts ... installs, provisions ... is off."
  - `/sc:load` (`spec:112`): report "none (see note)", "use it as a step inside another worker's brief, not as its own Task"; AC-1.1 still requires its section to name `return-contract.yaml`.
- Grading sentence: An implementer who follows P1 and AC-1.1 as written ships `--unattended` and a contract-naming section on auggie-review, post-release, pr-submit and task in P1, and the parenthesis "no-op where a command has no gate" does not cover them, so between P1 and P2/P4 `--unattended` is accepted while these commands still post to GitHub or run outward steps by default, and that is wrong because WC-9 says no outward default stays on under `--unattended` and the P4 commands are deliberately held until the user decides D2-D4; the same reading makes AC-1.1 demand a `return-contract.yaml` section for `/sc:load`, which section 3.2 says has no report.
- Recommendation: Narrow P1 and AC-1.1 to the commands whose rows are P1 (plus the ready commands needing no gate change), and have each later phase add the flag and section together with its gate resolutions. Exempt `/sc:load` from the contract-section assertion.
- Priority: High. Quality impact: avoids a half-wired flag that looks safe.

=== ARCHITECTURE ANALYSIS ===

No blocking architecture finding. The core decision holds: nesting depth 1 refuses a command that starts workers (`CAPS:97-99`, `spec:33`), Agent-tool subagents are outside that fence (`CAPS:155`, `spec:24`), `worker_done` is bound to the dispatched pane (`CAPS:76`, `spec:35`), and the six coordinator-only commands match both inventories (`INV-A:87-92`, `INV-B:282-287`, `spec:130-137`). The Medium items below are listed under follow-up candidates.

=== ADVERSARIAL ANALYSIS (Whittaker) ===

Attack results: sequence attack produced REQ-2; divergence attack on the contract path produced REQ-1. Remaining attacks produced Medium items only (M-3, M-5, M-6 below). Sentinel collision: `partial` maps to `succeeded` (`spec:63,263`), so a coordinator that keys on `--outcome` alone cannot tell a partial run from a full one; the spec covers this with the body's first sentence and the contract (WC-5), so it is OK.

## Guard Condition Boundary Table
Triggered: the spec contains thresholds and guards. One line per left-out class is given in the "Reason left out" list below the table.

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|---|---|---|---|---|---|---|
| nested worker depth | `spec:33,214,251` (`CAPS:97-101`) | Zero/Empty | depth 0 (coordinator) | may dispatch | coordinator dispatches workers (`CAPS:97`) | OK |
| nested worker depth | `spec:33` | Typical | worker at depth 1 calls `worker-start` | refused | `nested_worker_depth_exceeded`, "Do the work in this terminal" (`CAPS:99`) | OK |
| nested worker depth | `spec:33,252` | Legitimate Edge Case | user raises the setting (D5 b) | allowed | spec says it breaks R1's protection, recommends keep 1 | OK |
| nested worker depth | `spec:33` | Sentinel Value Match | malformed setting | falls back to 1 | `CAPS:100` | OK |
| heartbeat vs wait size | WC-10 `spec:68` | Typical | one blocking call 2 min | no split needed | heartbeat between calls | OK |
| heartbeat vs wait size | WC-10 `spec:68`, AC-4.3 `spec:210` | Legitimate Edge Case | single call 4.5 min | 4.5 is not "longer than 5" and not "at most 4" | WC-10 is silent; AC-4.3 fails any call over 240 s | GAP (M-4) |
| heartbeat vs wait size | WC-10 | Maximum/Overflow | single call 60 min (eval timeouts up to 3600 s, `spec:68`) | must split into waits of at most 4 min | stated | OK |
| task confidence gate | `spec:121` | Typical/Maximum | confidence >= 0.90 | proceed | unchanged (SA-1) | OK |
| task confidence gate | `spec:121` | Legitimate Edge Case | confidence 0.70 to 0.89 (the band that presents alternatives) | unspecified under `--unattended` | row only handles "below 0.70" | GAP (M-4) |
| task confidence gate | `spec:121` | Zero/Empty | confidence 0 or missing | below 0.70 | blocked | OK |
| WC-5 outcome mapping | `spec:63` | Sentinel Value Match | contract `status: partial` | -> succeeded | stated, body names `partial` | OK |
| WC-5 outcome mapping | `spec:62-63` | Zero/Empty | no contract file or an empty file | -> failed ("no report exists") | stated for missing; empty or unparseable file not stated | GAP (M-4) |
| readiness limit | WC-1 `spec:59` | Maximum/Overflow | launch prompt falls back at 45 s or more | start fails | stated (`EVIDENCE.md:45,56` via inventory) | OK |
| circuit breaker | `spec:263` (`CAPS:80,116`) | Typical | worker reports `failed` three times | no breaker trip | `CAPS:80`: a worker's own failed report does not count | OK |
| `--monitor` ordinal | `spec:114` | Legitimate Edge Case | `--monitor 1` | refused under `--unattended` | stated | OK |
| `--monitor` ordinal | `spec:114` | Zero/Empty | `--monitor 0`, `2` | not addressed | UNVERIFIED which prompts exist at 0 and 2 (`INV-B:89` names only 1) | GAP (M-4) |

Reason left out: nesting depth and `--monitor` have no one/minimal input class distinct from the typical one; the readiness and circuit-breaker guards are Orca-side and take no value from the spec; WC-10 and the confidence gate have no sentinel value.

## Quantity Flow Diagram (Pipeline Dimensional Analysis)
Triggered by the multi-stage partition from inventories to phases. Counts reconcile; no mismatch that a downstream consumer relies on.

```text
[Commands in cmd/: 43] --> [Inventory split: A 21 + B 22 = 43] --> [Spec verdicts: ready 10, needs-change 27, coordinator-only 6 = 43]
                                                                     |
                                                                     v
                                          [Worker-capable: 37] --> [Phases name 35 commands]   <-- 2 not named (brainstorm, init-lite)
                                                                     |  P1: 9 + 4 fixes = 13   P2: 11 + 4 ready = 15   P3: 4   P4: 3
                                                                     v
                                          [Consumer: P1 text "every command in 3.1 and 3.2" covers the 2 by the generic clause]
```
No finding: the generic clause at `spec:159` assigns both. Noted as M-7.

## Follow-up candidates (Medium and minor; none triggers a revision)
Medium (warnings; each needs a reader guess or is an unstated requirement):
- M-1 Usage-line edits versus the additive check. SA-4 (`spec:149`) says new flags are additive and AC-C5 (`spec:176`) requires no deleted lines; adding a flag to a command's one-line `Usage` block normally replaces a line, and `/sc:load`'s usage-line fix is exempted only because it is a named defect. Whether a new flag goes on a new line is not said.
- M-2 AC-C1 greps `src/superclaude/core` for `orca orchestration|worktree|terminal|agent` (`spec:172`), but P0 adds an Orca section to `HOW-WE-WORK.md` and a contract file in `core` (`spec:158`) whose natural wording names Orca commands (WC-3, WC-12, section 4's `task-create`). Passes only if both are written without those literal strings; SA-2 (`spec:147`) allows a contract-file mention without saying how it is worded.
- M-3 "Fresh dir" retry (WC-6, `spec:64`, used by about 20 rows of section 3) versus a fixed coordinator-passed output directory (WC-4) and the same brief on `--retry-of`: the spec does not say whether the command makes a sub-directory (then the contract path moves) or the coordinator passes a new directory per attempt (not in section 2.3).
- M-4 Unspecified edges from the table above: the 4 to 5 minute call (WC-10 versus AC-4.3's stricter 240 s), the task 0.70-0.89 band under `--unattended`, an empty or unparseable contract under WC-5, `--monitor 0` and `2`.
- M-5 Contract location for commands whose output is a file, not a directory: tdd (`spec:90`, `--output <file>`), init-lite (`spec:87`), spec-panel after the added `--output` (`spec:120`). WC-4's `<output-dir>` is undefined for them; 7.2 steps 3-4 and AC-2.2's tdd example (`spec:200`) need it.
- M-6 Brief-time `--unattended`: section 2.3 and 7.2 step 1 (`spec:73,180`) put `--unattended` in every command line, while the ready commands "run as workers now" without it (`spec:79`) and the P0 smoke commands omit it (`spec:194`). What an unmodified command does with an unknown `--unattended` flag is not stated.
- M-7 P1 names 13 commands and covers brainstorm and init-lite only through the generic clause (`spec:159`); say so explicitly.
- M-8 Reflect defaults not covered by WC-9/WC-11: default-on Wave 7 folder move and a tracked file `docs/memory/reflect/deviation-patterns-<slug>.md` written outside the output directory (`INV-B:109-114` region, reflect bullets (f)); the 3.1 row mentions only `--no-promote`.
- M-9 SA-3 (`spec:148`) allows the contract "when the caller passes the new output flag", WC-4 (`spec:62`) says only in unattended mode.
- M-10 Evidence consistency: E3 (`spec:23`) cites `invocation_method: "skill-direct"` as proof it worked, while section 1.4 (1) (`spec:43`) says the PR #329 run proves only the Agent-tool route. `INV-A:11` and `INV-A:35` read it as direct; the spec should reconcile one way.
- M-11 Tasklist (`spec:122`) says its reflect fan-out is "inside Claude Code's nesting limit"; tasklist -> reflect -> Tier 2 reviewers -> adversarial is up to three layers below a worker (`INV-B:110`, `INV-A:14`), untraced and UNVERIFIED (INV-B's UNVERIFIED item 1 says nested-subagent behaviour is not stated in any file read).
- M-12 7.2 step 2 (`spec:181`) passes when `agentWait` is "never non-null"; `CAPS:129` says an absent field means Orca never looked, so the check can pass vacuously, and sampling every 5 minutes can miss a short wait.

Minor notes:
- n-1 The decisions table cites `INV-B:112` for the reflect contract; the reflect contract bullet (d) is at `INV-B:111` (off by one).
- n-2 Section 2.1 (`spec:51`) calls unattended mode "the only command-side change ... besides report files and resume", yet section 3 lists reconciliations and tool changes; SA-4 names them, so this is wording only.
- n-3 Citations to files outside the workspace are UNVERIFIED (see Coverage); the spec's own re-check claims cannot be confirmed here.

Issue question: per the command's Review Loop (bullet 3) the session that ran the review asks the user once per loop whether to open an issue for the follow-up candidates above and creates none without the answer. This run is unattended inside a sandbox: no question was asked and no issue was created. The coordinator should ask.

## Reviser brief
Blocking finding ids: REQ-1, REQ-2. Only these. The reviser reads this report, not the command, so the contract of `/sc:spec-panel` Review Loop bullet 6 is restated:
- revise only text a blocking finding names;
- add no rule, mechanism or section that no blocking finding calls for;
- each added paragraph or table cites its finding id;
- prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id;
- leave Medium and minor findings (M-1 to M-12, n-1 to n-3) alone; do not award yourself a PASS.

verdict: FAIL

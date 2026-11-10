review: 1 of 3

# Spec-panel critique: orca-worker-contract-spec, round 1

## Header
- Command: `/sc:spec-panel @.dev/orca-command-refactor/specs/orca-worker-contract-spec.md --mode critique --focus requirements,architecture` (first review, no `--re-review`, no `--baseline`; `baseline: not applicable`).
- Candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`
- Candidate SHA-256: `d3cdbe573e57303b9ce6c93d1fe98ba18fb7cb1a15773d926bf6a0c31425200d`
- Reviewer model actually used: `claude-haiku-5-5`
- Panel: Wiegers (lead), Adzic, Cockburn (requirements); Fowler (lead), Newman, Hohpe, Nygard (architecture); Whittaker (active in every panel review, `command.md:83`).

## Citation shorthand
- `spec:N` = `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md` line N.
- `INV-A:N`, `INV-B:N`, `CAPS:N` = `.dev/orca-command-refactor/inventory/commands-a.md`, `commands-b.md`, `orca-capabilities.md` line N.
- `README:N` = `.dev/orca-command-refactor/README.md` line N.
- `cmd:N` = the `/sc:spec-panel` definition, `command.md` in the review sandbox, line N.
- `prompts:N` = `home/.claude/rules/prompts/document_review_loop_prompts.md` (sandbox home) line N.
- UNVERIFIED: a citation to a file outside the workspace (`src/superclaude/...`, `.dev/evals/...`, `.dev/codegraph-migration/...`, `CLAUDE.md`, the Orca app) cannot be checked here, so it is UNVERIFIED. The spec's own statement that a fresh validator checked citations (`spec:11`, `spec:285`) is not evidence for this review.

## Coverage
- Read in full: `command.md`, `prompts:1-56`, `README.md`, `spec` (all 285 lines), `INV-A` (120 lines), `INV-B` (323 lines), `CAPS` (188 lines).
- `~/.claude/WORKER-CONTRACT.md` is not present in the sandbox. It is not needed: the brief does not pass `--unattended`, so `cmd:457` does not apply.
- Spec citations to `INV-A`, `INV-B` and `CAPS` that I checked matched their target lines (for example `spec:83` to `INV-A:35`, `spec:111` to `INV-A:54`, `spec:46` to `CAPS:46`, `spec:62` to `CAPS:79`, `spec:68` to `CAPS:130`, `spec:197` to `INV-B:323`). `spec:39` cites `CAPS:158` for a point that line only partly states (finding m-04).
- Not reviewed: anything outside the sandbox. No Orca command was run.

## Decisions
- D-1: Panel is the focus panel plus Whittaker, who is active in every review (`cmd:83`).
- D-2: Grading follows `cmd:259` and `prompts:31`. A finding is blocking only when a stated text causes harm, when two stated texts contradict each other, or when an acceptance criterion cannot pass. A finding that needs a guess is Medium and goes to follow-up candidates.
- D-3: The Guard Condition Boundary Table is produced because the spec has conditional logic (`cmd:309-317`). Pipeline Dimensional Analysis is not triggered: no multi-stage data flow changes counts. The counts reconcile instead (see Count check below).
- D-4: Medium and minor findings are not in the Reviser brief (`cmd:260`, `cmd:263`).

=== REQUIREMENTS ANALYSIS ===

### F-01 BLOCKING: AC-C1 cannot pass as written (Wiegers)
- Locations: `spec:172` (AC-C1 greps `src/superclaude/core`), `spec:158` (P0 adds an Orca section to `core/HOW-WE-WORK.md`), `spec:150` (SA-5 says the routing guide gains an Orca section), `spec:147` (SA-2 allows an Orca mention in the core contract file), `spec:52` (contract file lives in `core`).
- Sentence: An implementer who follows P0 and SA-2 writes Orca commands into the core guide and the contract file, AC-C1 then prints those lines, and the P0 check cannot pass.
- Evidence: AC-C1 excludes only `skills/ccsession-tag/` (`spec:172`).
- Recommendation: Narrow AC-C1 to commands, skills and agents, which is the scope SA-2 uses (`spec:147`), or list the core lines that are allowed to name Orca.
- Priority: High.

### F-02 BLOCKING: WC-4 and WC-6 disagree on where a re-run writes its contract (Fowler)
- Locations: `spec:62` (WC-4: the contract goes to `<output-dir>`, "the directory the coordinator passed", and the path is known before dispatch), `spec:64` (WC-6: the command "writes each run into a fresh output directory so a re-run starts clean"), `spec:73` (the coordinator's brief carries the output directory), `spec:91` (troubleshoot row: resume is "Fresh dir").
- Sentence: An implementer who follows WC-6 writes a retry into a new directory, and WC-4 says the coordinator reads the contract where it passed the directory, so the coordinator opens the first attempt's contract (for example `status: failed`) and never sees the retry's result.
- Recommendation: Choose one owner for the directory. Either the coordinator passes a fresh directory for each attempt (`--retry-of`, `CAPS:116`), which makes WC-6 a coordinator duty, or the command writes the retry under a subdirectory and WC-4 names the pointer file the coordinator reads.
- Priority: High.

### F-03 BLOCKING: AC-1.1 contradicts the scope of section 3 and the load row (Cockburn)
- Locations: `spec:76` ("Every changed command also gains the `## Unattended mode` section"), `spec:79` (3.1 "Ready today": "The only command changes are the small fixes"), `spec:84` (brainstorm, small fix "None"), `spec:87` (init-lite, small fix "None"), `spec:159` (P1 requires `--unattended` on every 3.1 command), `spec:195` (AC-1.1 requires the section in every 3.1 and 3.2 command, naming `return-contract.yaml`), `spec:112` (load: report "none (see note)"), `spec:265` (Decisions: a report file for load "would be an unrequested addition").
- Sentence: An implementer who follows `spec:79` and the "None" cells leaves brainstorm and init-lite without the section and the flag, and AC-1.1 fails for both; an implementer who follows AC-1.1 gives load a `return-contract.yaml` that `spec:265` says must not exist.
- Recommendation: State the exact list of commands that gain the section and the flag, and either give load a contract or remove load from AC-1.1. Make `spec:79` say that ready commands still gain the flag.
- Priority: High.

### M-01 Medium: Headless auto-accept trigger for reflect is ambiguous (Nygard)
- Locations: `spec:88` (3.1 reflect: under `--unattended`, make `--remediate` "follow the existing headless auto-accept rule"), `spec:122` (tasklist Stage 10.5 "passes `--unattended` to each reflect so the headless rule applies"), `spec:151` (SA-6: the headless rule keys on `claude --print`; "`--unattended` reuses it and does not replace it"), `INV-B:109` (an Orca worker is an interactive terminal session, not `--print`, so the prompt would fire).
- Gap: `spec:151` keeps the `--print` trigger, but `spec:88` and `spec:122` need `--unattended` to trigger auto-accept. An implementer has to guess which, and the guess decides whether a worker stalls at "[yes / no]". AC-2.2 (`spec:200`) does not test reflect.
- Recommendation: Say in SA-6 that `--unattended` is a trigger for the auto-accept rule, and add an acceptance check for reflect `--remediate` under `--unattended`.

### M-02 Medium: a blocked gate's answer has no defined flag, and the worker's path is optional (Whittaker, Adzic)
- Locations: `spec:60-61` (WC-2 and WC-3), `spec:64` (WC-6), `spec:97` and rows `spec:99-125` (the "Blocked" gate resolutions have no answer flag, except where noted), `spec:121` (task confidence gate).
- Sentence: I can break this specification by **Sequence Attack**. The invariant at **WC-3 (`spec:61`)** fails when a worker answers a blocked gate on a command whose resume is "fresh dir" (`spec:121`, `spec:91`). Concrete attack: `/sc:task` blocks at confidence 0.65; the coordinator answers through `ask`; the worker re-invokes with the answer as a flag, which the row does not name; the command starts from zero in a new directory, and the first contract is left orphaned.
- Also: WC-3 says the worker "may" ask the coordinator or stop. The spec does not say which path a coordinator should expect, so the same blocked contract can lead to either outcome.
- Recommendation: Require each blocked gate to name its answer flag in its section 3 row, and make the ask path mandatory or forbidden in WC-3.

### M-03 Medium: `--unattended` without an output directory has no defined behavior (Cockburn)
- Locations: `spec:62` (the contract is written to `<output-dir>`), `spec:148` (SA-3: the contract is written "in unattended mode or when the caller passes the new output flag"), `spec:73` (the coordinator owes the directory).
- Gap: SA-3 says the contract is written in unattended mode, but `spec:62` gives no place to write it when no directory was passed. WC-4 says the contract is written "including stops before any other output exists", so the gap also affects an early stop.
- Recommendation: Make `--unattended` without an output directory an explicit blocked outcome, or give it a default.

### M-04 Medium: `/sc:index` knowledge-base mode is described two ways (Wiegers)
- Locations: `spec:111` (index row: "state that knowledge-base mode does not wait"), `spec:277` (UNVERIFIED 6: "section 3 refuses or pins them under `--unattended` regardless"), `INV-A:54` (whether knowledge-base mode waits is unknown), `INV-A:113`.
- Gap: `spec:277` says section 3 refuses or pins the mode, but the index row only says to state a fact the spec itself lists as UNVERIFIED. An implementer cannot tell whether to refuse the mode.
- Recommendation: Refuse or pin the mode in the row, and remove the claim from the row, or move the claim to a check.

### M-05 Medium: Rejected alternative's benefit depends on a handoff that is not in the brief (Newman)
- Locations: `spec:39` (the coordinator gets per-unit records by splitting work into several Tasks, for example several `/sc:troubleshoot` workers and then one `/sc:adversarial` worker on their reports), `spec:73` (the brief lists the command line, output directory and outward actions, but no upstream report paths), `spec:21`, `CAPS:86` (the wave pattern).
- Gap: The design that replaces the rejected alternative needs the downstream worker to receive the upstream report paths. Section 2.3 does not list them, and no check covers the handoff.
- Recommendation: Add "upstream report paths, taken from the contracts of the Tasks in `--deps`" to the brief list in 2.3, and add a check that a downstream brief names them.

### M-06 Medium: tasklist's nested reflect fan-out is marked "none" by the spec, but the inventory says needs-change (Newman, Hohpe)
- Locations: `spec:122` (tasklist: "Other required change: none", "its reflect fan-out runs one layer below the worker, inside Claude Code's nesting limit, `INV-A:14`"), `INV-B:210` (nested spawning "UNVERIFIED"), `INV-B:295` (inventory B lists tasklist under "Remove a nested fan-out ... inside subagents"), `INV-B:314` (UNVERIFIED 1: whether a subagent can spawn agents).
- Gap: The spec gives a verdict that the inventory reversed, and its only support is a web-doc claim (`INV-A:14`, external URL, not checkable here). The spec does not record the disagreement.
- Recommendation: Record the disagreement in the spec, and either add a check that Stage 10.5 nested reflect runs (with `--unattended`) or move the fan-out to the coordinator as B suggests.

### M-07 Medium: several requirements have no owner or acceptance check (Wiegers)
- Locations: WC-1 (`spec:59`, owner "Launch setup, not commands"), WC-3 (`spec:61`), WC-10 (`spec:68`), WC-11 (`spec:69`), WC-12 (`spec:70`). Acceptance checks are at `spec:191-211`.
- Gap: No phase (`spec:158-162`) owns the launch-setup change in WC-1. WC-3 has no check, WC-11 has a check only for `save` (AC-3.4, `spec:207`), WC-12 has none, and WC-10 is checked only for pr-submit (AC-4.3, `spec:210`), not cli-eval, which section 3 splits (`spec:104`).
- Recommendation: Assign WC-1 to a phase and add one check each for WC-3, WC-10 (cli-eval), WC-11 and WC-12.

### M-08 Medium: AC-C5 forbids edits that the gate conversions need (Fowler)
- Locations: `spec:176` (AC-C5: edits to commands without a named defect fix must be additive, "prints nothing" for removed lines), `spec:149` (SA-4: existing lines change only for named defect fixes), `spec:103` (cleanup: "Other required change: none"), `spec:110` (improve: "none"), `spec:121` (task: "none", though its TFEP report step must stop being committed).
- Gap: Gate conversions in section 3 that change existing "Approval Required" or "ask the user" lines are not named defect fixes, so AC-C5 and SA-4 require them to be additive. The spec does not say that a later "## Unattended mode" section may override an earlier line.
- Recommendation: State the override rule, or allow named gate conversions in SA-4.

=== ARCHITECTURE ANALYSIS ===

- The core decision (Orca coordinates, commands stay the units of work, `spec:16-26`) is well supported. Its strongest evidence is `CAPS:161` (a worker is a top-level Claude session) and `CAPS:97-101` (depth 1). Its weakest point is R1 (`spec:33`), which states that a nested command "would be refused" while the enforcing call sites are UNVERIFIED (`spec:276`, `CAPS:103`). The cell does carry the UNVERIFIED mark, so this is not a separate finding.
- Interface design: WC-4 (`spec:62`) and WC-5 (`spec:63`) define one contract file and a fixed status set. F-02 and M-03 show where the interface does not say who owns the directory.
- Boundaries: the Phase plan (`spec:158-162`) keeps each phase independently useful, which fits SA-1 (`spec:146`). M-08 shows that the boundary between additive edits and gate conversions is not stated.
- Count check (Pipeline Dimensional Analysis not triggered): 10 ready + 27 needing change + 6 coordinator-only = 43 (`spec:76`). Inventory A: 5 + 13 + 3 = 21 (`INV-A:73`). Inventory B: 5 + 14 + 3 = 22 (`INV-B:278`). Ready: 5 + 5 = 10; needs change: 13 + 14 = 27; coordinator-only: 3 + 3 = 6. Phase rows in section 3.2 sum to 9 (P1) + 11 (P2) + 4 (P3) + 3 (P4) = 27 (`spec:99-125`, `spec:159-162`). The counts reconcile.

## Guard Condition Boundary Table (cmd:309-317)

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|---|---|---|---|---|---|---|
| WC-5 outcome mapping | spec:63 | Zero/Empty: no report file | report path absent | true | `--outcome failed` | OK |
| WC-5 outcome mapping | spec:63 | Typical: status `partial` | `partial` | true (success set) | `--outcome succeeded` | OK |
| WC-5 outcome mapping | spec:63 | Sentinel: audit verdict FAIL, status `succeeded` | verdict `FAIL` | true | `--outcome succeeded` | OK |
| WC-4 output directory | spec:62, spec:73 | Zero/Empty: `--unattended` with no output directory | no directory passed | true | not stated | GAP (M-03) |
| WC-6 re-run | spec:64 | One/Minimal: retry with `--retry-of` and the same directory | same directory | true | command writes a fresh directory, which conflicts with WC-4 | GAP (F-02, blocking) |
| WC-2 / WC-3 gate | spec:60-61 | Typical: gate blocks, preamble present | `blocked_question` set | true | worker "may" ask, or stop | GAP (M-02) |
| SA-3 file write | spec:148 | Zero: standalone run, no flag | no `--unattended`, no output flag | false | no contract written | OK |
| WC-12 check | spec:70 | Legitimate edge: `check` returns `consumer_fenced` | fenced | true | stop without `worker_done` | OK |
| WC-10 wait size | spec:68 | Maximum: single tool call over 5 minutes | 5 minutes or more | true | split into waits of 4 minutes or less | OK |
| Reflect headless rule | spec:88, spec:122, spec:151 | Typical: `--unattended` under a worker terminal (not `--print`) with `--remediate` | not `--print` | unclear | auto-accept per 3.1, but SA-6 keys on `--print` | GAP (M-01) |
| index knowledge-base mode | spec:111, spec:277 | Typical: knowledge-base mode under `--unattended` | not stated | unclear | "state it does not wait" versus "refused or pinned" | GAP (M-04) |

Every GAP row has a finding. FR-10 (table complete) is NOT met: the table lists only the input classes that matter for each guard, and it gives no one-line reason for each omitted class (`cmd:317`, `cmd:334`). Under `cmd:334` this blocks synthesis output, so the Consensus and Priority sections below are provisional until the table is completed. The findings and the verdict do not depend on that completion.

## Whittaker probes (active in every review)
- Sequence (M-02) and the zero-directory case (M-03) are the two probes that produced findings. The sentinel probe on `partial` (`spec:63`) gives a clean mapping, because `partial` and FAIL-audit both map to `succeeded` and their content is carried in the contract body.

=== CONSENSUS AND DISAGREEMENT ===
- Consensus: the core decision and the evidence for it hold (Fowler, Newman, Nygard). The count reconciliation holds (Wiegers). The UNVERIFIED marks are used honestly in most cells.
- Disagreement: on tasklist's nested reflect fan-out (M-06), the spec and the inventory disagree. The panel does not resolve it; the spec must record it.

## Priority-ranked improvements
1. Fix the output-directory owner (F-02). It decides whether a coordinator reads the right contract.
2. Reconcile section 3 scope with AC-1.1 and the load row (F-03).
3. Narrow AC-C1 to the scope SA-2 uses (F-01).
4. Name the answer flag for each blocked gate and make the ask path definite (M-02).
5. Define the headless trigger for reflect (M-01) and the missing-directory case (M-03).
6. Resolve the index knowledge-base mode (M-04) and the tasklist disagreement (M-06).
7. Add owners and checks for WC-1, WC-3, WC-10, WC-11 and WC-12 (M-07), state the override rule (M-08), and add upstream report paths to the brief (M-05).

## Follow-up candidates (Medium and minor; not in the Reviser brief)
- M-01 to M-08 as above.
- m-01: `spec:25` (E5) and `spec:34` (R2, `CLAUDE.md:74`) rely on files outside the workspace. UNVERIFIED here.
- m-02: `spec:240` (D3 option a: "no pr-submit changes in Phase 4") does not match `spec:162` (P4 scope includes pr-submit). It reads as conditional, but say so.
- m-03: `spec:79` says the 3.1 changes are "only the small fixes", but the reflect row (`spec:88`) in the same list has a P2 gate change.
- m-04: `spec:39` cites `CAPS:158` for "Orca keeps those records only for workers the coordinator starts". `CAPS:158` states only that per-unit records need fan-out from the coordinator.
- m-05: `spec:43` (1.4 item 1) and `spec:45` (item 3) are the spec's own honest gaps. They should be linked from the Phase 0 gate (`spec:158`).

Per `prompts:31` and `cmd:259`, the coordinator asks the user once per loop whether to open issues for these follow-up candidates. No issue has been created.

## Reviser brief
Blocking finding ids: F-01, F-02, F-03.

Restated bullet 6 (`cmd:263`): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, and the bytes added and deleted per finding id. Medium and minor findings are not revised here. Do not award a PASS.

verdict: FAIL

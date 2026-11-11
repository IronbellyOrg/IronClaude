review: 1 of 3

# Whole-document audit: orca-worker-contract-spec.md

- command: `/sc:spec-panel @.dev/orca-command-refactor/specs/orca-worker-contract-spec.md --mode critique --focus requirements,architecture` (labelled whole-document audit, a first review of the full document; no `--re-review`, no `--baseline`)
- candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`, 285 lines, sha256 `eb7a9219ddeed9546c90120ee7c914556a7d57ba7d99b5a503bf74f7881bf609`
- baseline: not applicable (first review)
- reviewer model used: Sonnet 5.5 (`claude-sonnet-5-5`)
- prompt followed: FIRST-REVIEW prompt, `~/.claude/rules/prompts/document_review_loop_prompts.md:27-32`; shared context read first: `.dev/orca-command-refactor/README.md:1-38`
- panel (fixed order, requirements focus then architecture focus, plus the always-on adversarial expert): Wiegers, Adzic, Cockburn, Fowler, Nygard, Whittaker, Newman, Hohpe
- unattended: no; follow-up candidates are recorded below and no issue is opened (the user was not asked, because this sandbox has no user channel)
- brief clauses overridden: none

## What was covered

- The whole spec, sections 1-9, the Decisions table and the UNVERIFIED list (`spec:1-285`).
- Arithmetic of the 43-command split: 10 ready rows (`spec:83-92`), 27 needs-change rows (`spec:99-125`), 6 coordinator-only rows (`spec:132-137`); the phase cells at `spec:159-162` sum to the same 27 + 10 + 4 (P1: 14 + `load`, P2: 15, P3: 4, P4: 3). Inventory scope lines give 21 and 22 commands (`INV-A:3`, `INV-B:3`). No mismatch found.
- Cross-section consistency of WC-1..WC-12 (`spec:57-70`), SA-1..SA-6 (`spec:146-151`), the phase table (`spec:156-162`), the acceptance checks (`spec:169-210`) and D1-D5 (`spec:227-253`).
- Citations to the three inventories were spot-checked against the files: `CAPS:44,45,46,52,58,64,66,72,73,76,79,80,86,92,97,98,99,103,107,116,129,130,145,147,148,149,150,155,156,158,159,178,180,186,187,188`, `INV-A:3,14,76-83,90,94-98,106`, `INV-B:3,285-292,311,320,323`. Citations into `src/`, `CLAUDE.md`, `Makefile`, `pyproject.toml`, `.dev/evals/...`, `.dev/codegraph-migration/...` and `~/.claude/...` are not present in this workspace and are UNVERIFIED here, except where an inventory quotes them.
- Not covered: the truth of any Orca behaviour beyond what `orca-capabilities.md` quotes; any command or skill file; the two statements that the spec author or an `evidence-validator` re-read citations (`spec:11`, `spec:285`), which I cannot reproduce.

## Pipeline Dimensional Analysis

Not triggered: the spec describes no data pipeline whose stage counts diverge (the only counted flow is the command split, which reconciles, see above). No Quantity Flow Diagram is required.

## Guard Condition Boundary Table

Guards identified: the `--unattended` switch (`spec:51`, `spec:60`), the `--report-dir` flag (`spec:62`, `spec:148`), the outcome mapping (`spec:63`), the 4-minute wait split (`spec:68`), nesting depth 1 (`spec:33`), confidence below 0.70 (`spec:121`), the Orca-terminal detection (`spec:229`). One row per class that can occur; classes left out are named with a reason.

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|---|---|---|---|---|---|---|
| `--unattended` AND `--report-dir` | WC-4 `spec:62` | Zero/Empty | `--unattended` given, `--report-dir` absent | true / unset | not stated: `spec:62` says the command writes `<report-dir>/return-contract.yaml`, §2.3 (`spec:73`) says the brief passes it; the refusal case is never written | GAP |
| `--unattended` AND `--report-dir` | SA-3 `spec:148` | Legitimate Edge Case | `--report-dir` given, `--unattended` absent | false / set | SA-3 says the contract is written "when the caller passes `--report-dir`"; WC-4 says "In unattended mode ... writes"; the two texts differ | GAP |
| `--unattended` AND `--report-dir` | WC-4 `spec:62` | Typical | both given | true / set | contract written on every outcome | OK |
| outcome mapping | WC-5 `spec:63` | Sentinel Value Match | contract `status: partial`, or audit verdict FAIL | n/a | `--outcome succeeded`, first sentence names the status | OK |
| outcome mapping | WC-5 `spec:63` | Zero/Empty | no report file exists | n/a | `--outcome failed` | OK |
| wait split | WC-10 `spec:68` | Maximum/Overflow | one tool call above 5 minutes (pr-submit poll plus sleep of at least `--poll-interval`, cli-eval up to 3600 s) | true | split into waits of at most 4 minutes; pr-submit poll-script runtime and default `--poll-interval` stated as UNVERIFIED (`spec:114`, `spec:283`) | OK (flagged UNVERIFIED by the spec) |
| gate to blocked | WC-2(c) `spec:60`, cli-portify row `spec:105` | Legitimate Edge Case | re-invocation after a cli-portify approval gate blocked | gate re-evaluated | not stated: the row defines `--resume` but no input that records the approval, so the same gate blocks again | GAP |
| nesting depth | R1 `spec:33` | Maximum/Overflow | worker calls `worker-start` | refused | `nested_worker_depth_exceeded`; enforcing call sites UNVERIFIED and marked so | OK |
| confidence gate | task row `spec:121` | One/Minimal | confidence exactly 0.70 | not stated at the boundary | follows the command's existing threshold; this spec does not restate it | OK (inherited) |
| Orca detection | D1(b) `spec:229` | Sentinel Value Match | `ORCA_TERMINAL_HANDLE` set in a person's own Orca tab | maybe | spec records the risk and recommends (a) | OK |
| retry | WC-6 `spec:64` | Legitimate Edge Case | `worker-start --retry-of` re-runs the same brief | true | "fresh output directory" is required but nothing says who chooses it when the brief fixes `--report-dir` and `--output` | GAP |

Classes left out: Zero/Empty for the wait split (a zero wait cannot occur, waits are task-defined); Maximum/Overflow for the outcome mapping (two-valued).

## REQUIREMENTS ANALYSIS

### R-1 (blocking) AC-0.4 cannot pass as written; it gates every later phase
- Expert: Wiegers (testability), Adzic (example), Whittaker (sequence attack).
- Severity: CRITICAL, priority High.
- Grading sentence: an implementer who follows the stated text as written builds a Phase 0 check that cannot pass, and that is wrong because the spec makes a failed or unpassable P0 gate block all later phases.
- Quoted texts that contradict each other:
  - `spec:194` (AC-0.4): "steps 1-3 and 5-7 pass; step 4 uses the command's existing report file, since the contract arrives in P1."
  - `spec:182` (7.2 step 3): "**Pass:** exactly one `worker_done`; its `--outcome` matches the contract's `status` under WC-5; its report path is `<report-dir>/return-contract.yaml` (WC-4)."
  - `spec:83-92` (section 3.1 "Report today"): the three P0 smoke commands report elsewhere today (adversarial: "contract, but filename not fixed"; troubleshoot: `REPORT.md`; workflow: `.dev/tasks/to-do/<id>/return-contract.yaml`), and WC-4 text at `spec:79` says the brief omits `--report-dir` before its phase.
  - The carve-out in AC-0.4 names step 4 only. Step 3 still demands a contract `status` and the `<report-dir>/return-contract.yaml` path, which no P0 command writes. Gate: `spec:154` ("Later phases do not start until the earlier phase's checks in section 7 pass"), `spec:194` ("a failure here reopens section 1").
- Attack (sequence): run the three P0 smoke workers exactly as AC-0.4 says. Each sends `worker_done --report-path REPORT.md` (or the workflow path). Step 3's third clause fails, so P0 fails, so section 1 reopens, with no defect in the decision itself.
- Recommendation: extend the AC-0.4 carve-out to step 3 ("its report path is the command's existing report file from section 3.1, and `--outcome` matches that report's own status"). One sentence, no new mechanism.

## ARCHITECTURE ANALYSIS

No blocking architecture finding. The decision (Orca on top, commands stay units; `spec:16`, `spec:29-37`) is consistent with the quoted capabilities: depth 1 (`CAPS:97-99`), worker_done bound to the dispatched pane (`CAPS:76`, `CAPS:150`), no scheduling by a Run (`CAPS:92`), no lifecycle messages without a preamble (`CAPS:148`). Fowler: the shared-contract-file placement (`spec:52`) is a clean single point of change. Nygard: the 4-minute wait rule and the stall-visibility rule (WC-2, `spec:60`, `CAPS:52`) address the real failure mode honestly (`spec:44`).

## Medium findings (warnings; none blocks)

Each is a requirement the document never states, or a reading the text allows; none is a stated text that does harm without a guess.

- **M-1 `--unattended` and `--report-dir` interaction undefined.** `spec:62` ("In unattended mode ... `--report-dir <dir>`"), `spec:148` (SA-3: "or when the caller passes `--report-dir`"), `spec:73` (the brief passes it). Missing: what a command does with `--unattended` and no `--report-dir`; whether `--report-dir` alone triggers the contract. Add one sentence to WC-4. Expert: Whittaker (zero/empty attack), Wiegers.
- **M-2 cli-portify has no continuation input.** `spec:105` makes each of the three approval gates blocked and adds `--resume <contract>`, but no input carries the approval, and WC-3 (`spec:61`) re-invokes "with the answer as a flag". AC-2.3 (`spec:201`, "every required flag in the brief" gives `--outcome succeeded") has no flag for this command. `INV-A:79` offered an "explicit auto-approve flag" and the spec chose not to name one. An implementer must guess. Expert: Cockburn (goal reaches completion), Adzic.
- **M-3 WC-9 relies on explicit flags that the inventories do not show.** `spec:67` ("the command's own explicit flag"), `spec:100` ("posting returns only with an explicit `--post-pr`"). The inventory shows only `--no-post-pr` (`INV-A:38`, `INV-A:78`); `--post-pr` is not listed as a new flag in the "Other required change" column (`spec:100` says "none"). Same question for post-release, task `commit`/`push` and pr-submit (`spec:113`, `spec:121`). Expert: Wiegers (traceability).
- **M-4 WC-6 does not say who picks the fresh directory on retry.** `spec:64` requires fresh output on re-run for 21 rows; `spec:73` fixes `--report-dir` before dispatch; a `--retry-of` worker (`CAPS:116`) re-runs the same brief and therefore the same `--report-dir`/`--output`. Result: the second attempt overwrites the first attempt's contract. Add "the coordinator passes a new directory on a retry". Expert: Nygard, Whittaker (sequence attack).
- **M-5 AC-C5 can fail for a flag-only edit.** `spec:176` requires `git diff -U0 ... | grep -E '^-[^-]'` to print nothing, while SA-4 (`spec:149`) allows only additive edits and every changed command gains `--unattended` and `--report-dir` (`spec:76`). If the flags are added by editing the existing Usage or `argument-hint` line, that line shows as a removal and the check prints it. The spec never says the flags go on a new line. Expert: Crispin.
- **M-6 AC-C1 scans `src/superclaude/core`, where P0 adds the contract file and the routing-guide Orca section.** `spec:172` (greps `core`, filters only `ccsession-tag`), `spec:158` and `spec:150` (P0 writes `WORKER-CONTRACT.md` and an Orca section in `HOW-WE-WORK.md`). If either text quotes an `orca orchestration ...` command, AC-C1 fails; SA-2 (`spec:147`) permits only "an example of a caller's question channel". The wording limit is not stated for the routing-guide section. Expert: Fowler.
- **M-7 Citation defects in the spec's own evidence column** (checkable against the inventory):
  - E2 (`spec:22`) cites `CAPS:161` for "`[H:worker-start]` line 38, `--agent claude`". `CAPS:161` is the pr-submit top-level-rule line; no capabilities line quotes `[H:worker-start]` line 38 for `--agent claude` (`CAPS:49` and `CAPS:137` mention the flag in other contexts).
  - WC-11 (`spec:69`) and §2.3 (`spec:73`) cite `CAPS:115` for "`[G:placement]` lines 8-11: workers share the current worktree by default". `CAPS:115` says worktrees are never deleted by the verbs; I found no inventory line quoting `[G:placement]` lines 8-11 (a search for those words returned only `CAPS:115` for the placement tag area). Treat that claim as UNVERIFIED.
  - All citations into `CLAUDE.md`, `Makefile`, `pyproject.toml` (`spec:183`), `install_core.py` (`spec:52`), `EVIDENCE.md` (`spec:22`, `spec:59`) and the command and skill files are UNVERIFIED in this workspace. The 11-location re-read at `spec:11` and the "about 340 citations" check at `spec:285` could not be reproduced here.
- **M-8 Adzic: AC-2.2 and AC-4.1 each prove only the blocked path.** Only AC-2.3 (`spec:201`) covers the happy path, with one sentence for 15 commands. No per-command example flag set is given in section 3 for the P2 happy path beyond the "Brief must pass" column of 3.1. This is a testability gap, not a wrong outcome.

## Minor notes
- `spec:76` says every changed command gains the flags "in the phase its row names", while section 3.1 (`spec:79`) says ready commands gain them in P1/P2; both agree, but the 3.1 intro and the 3.2 intro are phrased differently. Cosmetic.
- The Decisions table (`spec:255-269`) and UNVERIFIED list (`spec:271-285`) are candid and consistent with the body; item 14 (`spec:285`) is a claim about a process, not about the design.
- Pipeline of phases: P2's tasklist row (`spec:122`) depends on reflect's `--unattended` in the same phase; ordering inside P2 is not stated. No wrong outcome follows because the whole phase must pass.

## follow-up candidates
M-1, M-2, M-3, M-4, M-5, M-6, M-7, M-8 above, and the three minor notes. None is blocking; none appears in the Reviser brief.

## Reviser brief
Blocking finding ids: R-1.

Restated from the command's Review Loop, bullet 6: revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id. Leave minor and Medium findings alone.

verdict: FAIL

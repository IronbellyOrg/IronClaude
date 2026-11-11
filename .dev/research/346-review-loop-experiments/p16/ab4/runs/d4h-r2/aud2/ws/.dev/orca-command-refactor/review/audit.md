review: 1 of 3

# Spec-panel audit: orca-worker-contract-spec.md

- command: `/sc:spec-panel @.dev/orca-command-refactor/specs/orca-worker-contract-spec.md --mode critique --focus requirements,architecture`
- label: whole-document audit of the final spec; first review of the full document (no `--re-review`, no `--baseline`)
- candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`
- candidate sha256: `24e411dcd5b98e3947b103fd3ff76a76e2a8ddec93e2c6e4f42c03d1f20513c9`
- baseline: none given (not a re-review)
- reviewer model actually used: claude-sonnet-5-5
- prompt followed: FIRST-REVIEW prompt in `~/.claude/rules/prompts/document_review_loop_prompts.md:27-32`
- binding context read first: `.dev/orca-command-refactor/README.md:1-38`
- brief clauses overridden: none
- notation: `S:N` = line N of the candidate; `INV-A:N`, `INV-B:N`, `CAPS:N` = lines of `inventory/commands-a.md`, `commands-b.md`, `orca-capabilities.md` (the same keys the spec uses, `S:8-9`)

## Coverage

Read in full: the candidate (all 285 lines), the README, and the three inventories (the only checkable evidence in this sandbox).

Citation check. Every `INV-A:N`, `INV-B:N` and `CAPS:N` the spec cites was compared with the inventory line (E1-E6, R1-R5, WC-1 to WC-12, every row of sections 3.1, 3.2, 4, the Decisions table and the UNVERIFIED list). Each cited line exists and says what the spec attributes to it. `README.md:12` and `README.md:31` also hold (`S:23`, `S:67`).

Arithmetic and consistency check.
- 43 = 10 + 27 + 6. Section 3.1 lists 10 commands (`S:83-92`), section 3.2 lists 27 (`S:99-125`), section 4 lists 6 (`S:132-137`). The inventories give 5+5, 13+14 and 3+3 (`INV-A:73`, `INV-B:278`).
- The phase assignment totals 37 phased commands: P1 15, P2 15, P3 4, P4 3 (`S:159-162`), and every 3.1/3.2 row's phase tag matches section 6.
- 21 + 22 = 43 (`INV-A:3`, `INV-B:3`).

UNVERIFIED (cannot be checked in this sandbox, no source files, no `CLAUDE.md`, no `EVIDENCE.md`):
- every `cmd/...` and `sk/...` line cited directly, for example `S:11`, `S:83-125`, `S:132-137` (the spec itself says only 11 of these were re-read, `S:11`);
- `CLAUDE.md:16,50,72-83,157,334,408` (`S:34,52,150,239`);
- `src/superclaude/cli/install_core.py:4,13-24,33` (`S:52`);
- `src/superclaude/core/HOW-WE-WORK.md:22,171,249,254` (`S:146,164`);
- `.dev/evals/ccsession-orca-e2e-20261026/EVIDENCE.md:39,45,56` and `.dev/codegraph-migration/...` (`S:23,43,59`), except where the inventories quote them (`CAPS:49`, `INV-A:13`);
- `pyproject.toml:38` (`S:183`);
- the E5 grep result (`S:25`).

Not covered: whether the proposed phases are the best order; Orca internals beyond what `CAPS` records; the real behaviour of any `/sc:` command.

## Expert panel (critique mode, focus requirements + architecture)

Panel per command.md: Wiegers (lead) with Adzic and Cockburn for requirements; Fowler (lead) with Newman, Hohpe and Nygard for architecture; Whittaker active in every review. Order: Wiegers, Adzic, Cockburn, Fowler, Nygard, Whittaker, Newman, Hohpe.

Grading follows command.md Review Loop bullet 2 and the FIRST-REVIEW grading check. Findings that need a guess about which reading an implementer picks, or that are requirements the document never states, are Medium and sit under follow-up candidates.

### === REQUIREMENTS ANALYSIS ===

#### F1 [MAJOR, blocking] The contract location is defined as a directory the brief passes, but three P1 commands have no such directory
- Experts: Wiegers (traceability and testability), Adzic (the acceptance check has no concrete example that passes), Cockburn (the coordinator cannot know where to look).
- Stated texts that conflict:
  - WC-4 defines the contract as `<output-dir>/return-contract.yaml`, where `<output-dir>` is "the directory the coordinator passed (`--output` / `--output-dir`)" (`S:62`). Section 2.3 repeats that the brief carries "the output directory, so the report path is known before dispatch" (`S:73`).
  - init-lite's `--output` takes a file: brief must pass `--output <file>`, report at `.dev/superclaude/context-audit.md` or `--output` (`S:87`; `INV-A:55`).
  - index-repo's brief passes nothing (`S:86`) and cleanup-audit's output directory is fixed (`.claude-audit/`, `S:85`; `INV-A:42`).
  - All three are P1 commands that must gain the contract in unattended mode (`S:159`; AC-1.1 `S:195` requires each P1 command except `load` to have a `## Unattended mode` section naming `return-contract.yaml`).
  - AC-1.2 requires a live check on each P1 command except `load` "with `--unattended --output <dir>`" (`S:196`), and 7.2 step 4 requires `test -s <contract>` (`S:183`).
- Grading sentence: an implementer who follows the stated text as written builds, for init-lite, a contract at `<file passed as --output>/return-contract.yaml` (a path under a file name) or runs AC-1.2 with a directory where init-lite expects a file, and for index-repo and cleanup-audit a contract with no stated location. That is wrong because WC-4 requires the path to be known before dispatch (`S:62`), and AC-1.2 step 4 cannot be evaluated for these three commands as written.
- Not covered by the M-ids: the same location gap for later-phase commands is M2 (follow-up).
- Recommendation: state one rule for where the contract goes when the output input is a file or absent (for example the file's parent directory, or a stated flag), and make AC-1.2 name the output input per command. Priority High. Quality impact: Completeness 8 to 9, Testability 7 to 9.

### === ARCHITECTURE ANALYSIS ===

No blocking architecture finding. The decision itself (Orca on top, commands as units) is supported: E1-E6 and R1-R5 hold against `CAPS:86,92,97-103,145-150,155-161` and `INV-A:90`, `INV-B:285-286`; section 1.4 states the evidence gaps plainly (`S:41-45`). Phase 0 tests the decision before anything depends on it (`S:158`, `S:194`). See Fowler/Newman/Hohpe/Nygard notes under follow-up candidates.

### === ADVERSARIAL ANALYSIS (Whittaker) ===

Attacks that produced a finding are listed first; the rest found the text sound.

1. I can break this specification by **Divergence Attack**. The invariant at **S:62 (WC-4 `<output-dir>` is the `--output`/`--output-dir` directory)** fails when **a command's `--output` is a file (init-lite `S:87`, tdd `S:90`)**. Concrete attack: brief `/sc:init-lite --unattended --output .dev/x/audit.md`. Before: no contract. After (as written): the contract path is `.dev/x/audit.md/return-contract.yaml`, impossible to create next to a file. State trace: output-dir = `.dev/x/audit.md`; parent is a regular file; write fails; WC-4 requires a contract on every outcome (`S:62`), so the failure itself cannot be reported. Severity: MAJOR, blocking. This is F1.
2. I can break this specification by **Sequence Attack**. The invariant at **S:159 (P1: `--unattended` accepted by every command in sections 3.1 and 3.2 that has no outward default)** fails when **the phase column defers the command's gate to P2 or later (`S:97-125`, `S:160`)**. Concrete attack: after P1, a coordinator briefs `/sc:cleanup <dir> --unattended` (cleanup edits code locally, no outward default; gate conversion is P2, `S:103`). Before: flag unknown. After P1: flag accepted, but the "Approval Required" prompt still fires, which WC-2 forbids under `--unattended` (`S:60`). The worker stalls with `agentWait` set (`CAPS:129`). Severity: Medium (the phase table and the P1 commands list at `S:159` can be read as excluding cleanup; see M1).
3. I can break this specification by **Sentinel Collision Attack**. The invariant at **S:63 (WC-5 maps any status outside the four values to `--outcome failed`)** fails when **a command's existing contract already carries a status word outside the four values**. Concrete attack: workflow's existing `return-contract.yaml` (`S:92`, `INV-B:272`) and adversarial's (`S:83`) keep their fields (`S:62`), and their status vocabulary is not recorded in the inventories (UNVERIFIED). If either uses a word such as `success`, a clean run maps to `failed`. Severity: Medium (needs the unverified vocabulary; see M4).
4. **Zero/Empty Attack** on `--unattended` without an output input: only post-release and cli-eval say what happens (`S:104,113`); no general rule (see M2).
5. **Accumulation Attack** on retries: blocked and failed worker reports do not trip the circuit breaker (`CAPS:80`, spec decision at `S:263`); the spec relies on the coordinator choosing `--retry-of` with a changed brief. Sound as written.

### Guard Condition Boundary Table

Guards found: `--unattended` presence (`S:51`), contract path input (`S:62`), status vocabulary (`S:63`), readiness limit (`S:59`), heartbeat and wait thresholds (`S:68`, `S:210`), nesting depth (`S:66`), confidence gate (`S:121`), `ask` timeout (`S:61`). Classes left out are given a one-line reason.

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|-------|----------|-----------------|----------------|--------------|-------------------|--------|
| `--unattended` present | S:51, S:146 (SA-1) | Zero/Empty | flag absent | false | behaviour identical to today (SA-1) | OK |
| `--unattended` present | S:159 | Legitimate Edge Case | flag passed to a command whose gate converts in P2+ (cleanup, improve, cli-portify, implement, roadmap) | true | P1 text accepts the flag; the gate stays as is until its phase (S:97-125) | GAP (M1) |
| `--unattended` present | S:159 | Sentinel Value Match | auggie-review, task, cli-eval, pr-submit, post-release | true | rejected until their phase | OK |
| output input (`<output-dir>`) | S:62, S:73 | Zero/Empty | none passed under `--unattended` | n/a | only post-release and cli-eval say "else blocked" (S:104,113); no general rule | GAP (M2) |
| output input | S:62 | Typical | directory | true | `<output-dir>/return-contract.yaml` | OK |
| output input | S:62, S:87, S:90 | Legitimate Edge Case | `--output` is a file (init-lite, tdd, spec-panel) | true | undefined | GAP (F1, blocking) |
| output input | S:86, S:85 | Legitimate Edge Case | command has no output input (index-repo; cleanup-audit fixed dir) | false | undefined | GAP (F1, blocking) |
| contract `status` | S:63 | Zero/Empty | file absent, empty, unparseable | true | `--outcome failed` | OK |
| contract `status` | S:63 | Sentinel Value Match | `blocked` | true | `--outcome failed`, question in file | OK |
| contract `status` | S:62, S:63 | Legitimate Edge Case | existing contract with its own status words | unknown | "keep their fields" vs "one of four values"; not reconciled | GAP (M4) |
| contract `status` | S:63, S:263 | Legitimate Edge Case | `partial`, or audit verdict FAIL | true | `--outcome succeeded`, body states status/verdict | OK |
| readiness limit 60 s | S:59 | Maximum/Overflow | prompt above ~45 s fallback | true | start fails again; fallback must be "well inside" | OK |
| wait split (5 min cadence, 4 min waits) | S:68, S:210 | Maximum/Overflow | one tool call of 4 to 5 min | WC-10 false, AC-4.3 true | WC-10 allows it; AC-4.3 fails any call over 240 s | GAP (minor note) |
| nesting depth 1 | S:33, S:66 | One/Minimal | worker calls `worker-start` | true | refused; WC-8 forbids the call | OK |
| confidence gate (task) | S:121 | Sentinel Value Match | exactly 0.70 | "below 0.70" false | proceeds (consistent with the stated threshold) | OK |
| `ask` timeout | S:61 | Zero/Empty | timeout, no answer | n/a | resume the same message ID; the default timeout is UNVERIFIED (S:281) | OK |

Left out and why: a "Maximum/Overflow" row for `--unattended` (a boolean has no overflow); a "Typical" row for the status guard (covered by `succeeded` in the WC-5 text, `S:63`).

All cells are populated, every guard is enumerated, and every input class has a row or a stated reason, so FR-10 is met. The GAP rows are graded under FR-8 and FR-9: those that name a concrete wrong outcome are blocking (F1); the rest are Medium (below).

### Quantity flow (pipeline dimensional analysis)

Triggered only loosely (the spec has no data pipeline, but its phase and verdict counts divide a population). No mismatch.

```text
[43 commands] --> [Verdict split] --> [10 ready] + [27 needs change] + [6 coordinator-only]   (43 = 10+27+6)
[10 + 27 = 37 phased] --> [P1 15] + [P2 15] + [P3 4] + [P4 3]                                   (37 = 15+15+4+3)
```

## Follow-up candidates (Medium and minor; none blocks, none enters the Reviser brief)

Medium (warnings):

- **M1** The P1 scope sentence says `--unattended` is accepted by every command in 3.1/3.2 "that has no outward default (a no-op where a command has no gate)" (`S:159`), but the explicit P1 command list omits cleanup, improve, cli-portify, implement, roadmap and others whose gates convert in P2 to P4 (`S:97-125`, `S:160-162`). The reader can choose either; one reading yields a flag that is accepted while the gate still stalls. Same for the ready commands whose gate fix is P2 (troubleshoot, tdd, release-split, reflect, `S:88-91`). Suggest stating that the flag is accepted for a command only in its own phase.
- **M2** Contract location for later phases and for omitted output (Wiegers, Whittaker): research (`S:116`), save (`S:119`), recommend (`S:115`), implement (`S:109`, "beside the ledger"), review-translation (`S:117`) and index-repo have "Other required change: none" and no output input, so "known before dispatch" (`S:62`) is not met; `--unattended` with no output input has no general behaviour. Several of these also fall under WC-11 if the default location is shared (`S:69`). The new output flags in rows such as "add a report path" (`S:99,101,106,108,111,123`) are unnamed, so file versus directory is open.
- **M3** AC-2.2 expects a blocked-gate worker to end `--outcome failed` with `agentWait` never set (`S:200`), but WC-3 lets the worker `ask` instead and continue (`S:61`), and the brief contents in 2.3 (`S:73`) do not forbid it. An `ask`-then-succeed worker fails the AC. The brief for AC-2.2 runs should say not to ask.
- **M4** WC-4 says commands with a contract "keep their fields" (`S:62`) while WC-5 treats any status outside four words as `failed` (`S:63`). The existing status vocabularies of workflow, adversarial, brainstorm and reflect are not recorded in `INV-A` or `INV-B` (UNVERIFIED). Suggest recording each and stating the mapping or the field to add.
- **M5** P0 smoke runs (`S:194`): troubleshoot's `REPORT.md` is not a machine file with a status (`INV-B:242`, only `return-contract.yaml` under `--caller task-unified`), so "outcome matches that report's status under WC-5" has no value to compare for it, and WC-5 reads an unparseable report as `failed`. The P0 result for troubleshoot would be vacuous or a false failure. Suggest naming what WC-5 reads in P0.
- **M6** WC-3 states that an answer relayed through `ask` "is never a Ruling" (`S:61`), while D2 option (b) lets the coordinator relay the person's exact words as a Ruling (`S:235`). If the user picks (b), WC-3 must change; the spec does not say so (AC-4.1 does, `S:208`).
- **M7** Carrier of the worker-session duties (Fowler, Cockburn): WC-3, WC-5, WC-7 and WC-12 are owned by "Worker session" (`S:61,63,65,70`), but section 2.3's list of what the brief carries (`S:73`) does not include an instruction to load `~/.claude/WORKER-CONTRACT.md`, and in P0 no command has changed to point at it (`S:158`). Suggest adding it to the brief template list.
- **M8** tasklist (`S:122`): the spec says the Stage 10.5 reflect fan-out "runs one layer below the worker, inside Claude Code's nesting limit" and needs no further change, citing `INV-A:14`. `INV-B:210,215,322` recorded the same fan-out as an unresolved nesting and "who answers" question and recommended running it at top level. The spec does not say why it set that recommendation aside. Marked UNVERIFIED either way.
- **M9** No propagation rule: a command invoked under `--unattended` that itself invokes other `/sc:` commands (brainstorm to adversarial, release-split to brainstorm and adversarial, cli-eval create to adversarial and spec-panel, workflow to reflect) has no stated rule for passing the mode down; only tasklist to reflect (`S:122`) and tdd's nested `/task` (`S:90`) are covered.
- **M10** Roadmap writes memory through `sc:save` at every wave (`INV-B:154`) while WC-11 bars writing single-owner keys in unattended mode (`S:69`); the roadmap row (`S:118`) does not say which keys it uses.
- **M11** AC-C1 as written (`S:172`) uses `\|` inside the ERE group and before `grep -v`. Rendered in a table it is a pipe, but copied raw the alternation matches a literal `orchestration|worktree|terminal|agent`, never matches, and prints nothing (tested: the raw pattern exits 1 on `orca orchestration x`; the unescaped pattern matches). The check then passes vacuously. Suggest giving it outside a table.
- **M12** WC-6 allows the brief to take the fresh-directory branch with a per-attempt unique `--output` (`S:64`), but for commands whose `--output` is a file (init-lite `S:87`) or whose directory is fixed (cleanup-audit `S:85`, index-repo `S:86`), a fresh output cannot be passed; the 3.1 rows only partly cover this (init-lite does).

Minor (notes):

- Nygard: WC-10 splits waits of more than 5 minutes into waits of at most 4 (`S:68`), but AC-4.3 fails any call over 240 s (`S:210`); a 4 to 5 minute call passes the requirement and fails the check.
- Section 3.1 gives brainstorm and init-lite no phase tag (`S:84,87`); section 6 adds them to P1 (`S:159`), so a test built from section 3 phase tags (AC-1.1, `S:195`) would miss them.
- 7.2 step 5 says "check that the command's skill is the first tool call" (`S:184`) but the preamble may require an earlier `check` or heartbeat Bash call; the pass condition ("no Agent or Task call precedes the command") is the sound one.
- AC-C5 (`S:176`) fails if a command's existing `Usage` line is edited to add `--unattended`; the spec does not say whether the usage line may change.
- P0 says the routing guide has "two mirrored copies" (`S:158`, `S:150`); the repo rule describes one byte-copy and one level-table copy (UNVERIFIED, `CLAUDE.md` not in sandbox).
- The `reply --body \"<answer>\"` escaping (`S:182`) is shown with backslashes in a list item; harmless.

Issue offer: command.md asks the session once per loop whether to open an issue for the follow-up candidates. No user is reachable in this sandbox; none was asked and none was created. The coordinator should ask.

## Quality scores (0-10)

Clarity 8; Completeness 7 (location of the contract, M2); Testability 7 (F1, M3, M5, M11); Consistency 7 (F1, M1, M4, M6).

## Summary

The decision, evidence handling and counts hold. One blocking contradiction: the contract's location rule (WC-4) cannot be applied to three P1 commands and the P1 acceptance check cannot pass as written for them (F1). Twelve Medium warnings and a few minor notes are listed above for the coordinator's follow-up list.

## Reviser brief

Blocking finding ids: F1

Reviser contract (restated from the command's Review Loop, bullet 6):
- Revise only text a blocking finding names.
- Add no rule, mechanism or section that no blocking finding calls for; each added paragraph or table cites its finding id.
- Prefer deleting or narrowing to adding.
- Report the byte size of the candidate before and after, and the bytes added and deleted per finding id.
- Leave minor and Medium findings alone.
- Return the candidate once and do not award yourself a PASS.

Scope of F1: the WC-4 contract-location sentence (`S:62`), the section 3.1 rows for init-lite (`S:87`), index-repo (`S:86`) and cleanup-audit (`S:85`), and the AC-1.2 text (`S:196`). Do not touch M1 to M12.

verdict: FAIL

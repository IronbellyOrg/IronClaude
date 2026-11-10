review: 1 of 3

# /sc:spec-panel critique: orca-worker-contract-spec.md (first review, 1 of 3 reviewers)

- candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`
- candidate sha256: `d3cdbe573e57303b9ce6c93d1fe98ba18fb7cb1a15773d926bf6a0c31425200d`
- baseline: not given (first review of the full document; `--re-review` and `--baseline` absent)
- reviewer model used: claude-sonnet-5-5
- mode: critique; focus: requirements, architecture
- coverage: whole document (sections 1-9, Decisions, UNVERIFIED), checked against `inventory/commands-a.md`, `commands-b.md`, `orca-capabilities.md` and `README.md`. Not covered: anything outside the workspace.

Citation keys: `SPEC:N` = line N of the candidate; `A:N`, `B:N`, `CAPS:N` = lines of `inventory/commands-a.md`, `commands-b.md`, `orca-capabilities.md`; `README:N` = `.dev/orca-command-refactor/README.md`; `CMD:N` = line N of the `/sc:spec-panel` command definition `command.md` in the run folder (not an inventory file; used only as a cross-check). Any citation to a file outside the workspace (`src/`, `CLAUDE.md`, `EVIDENCE.md`, the codegraph README, `pyproject.toml`, Orca internals) is UNVERIFIED unless an inventory line quotes it.

## Citation spot check

I opened these `A:`/`B:`/`CAPS:` targets and each says what the spec uses it for: A:13, 14, 35, 36, 45, 73, 76-83, 90-98, 106, 113, 118, 120; B:65, 105, 272, 285-286, 289-301, 311, 314, 320, 323; CAPS:44-52, 58-68, 72-80, 84-92, 97-103, 107-116, 129-130, 145-151, 155-161, 178-188. Section 3 counts reconcile: 10 + 27 + 6 = 43, and the 27 split P1 9 / P2 11 / P3 4 / P4 3 plus 4 ready commands in P2 equals the lists at SPEC:159-162. `SPEC:214` states as fact that tasklist's reflect fan-out sits inside the nesting limit; B:314 lists the same point as UNVERIFIED (minor note n1).

## Mandatory artifacts

### Guard Condition Boundary Table (triggered: the spec contains thresholds, sentinels and boolean guards)

Guards: G1 readiness limit (`SPEC:59`), G2 wait split (`SPEC:68`), G3 outcome mapping (`SPEC:63`), G4 the `--unattended` switch (`SPEC:51,228`), G5 contract location (`SPEC:62`).
Classes left out, one line each: G1 Maximum (upper bound of `--timeout-ms` is UNVERIFIED, CAPS:54); G2 Zero/Empty (a wait of 0 is a no-op); G3 Maximum (no counter); G4 Maximum and Legitimate Edge (covered by Sentinel); G5 Typical is the normal case.

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|---|---|---|---|---|---|---|
| G1 prompt-before-ready | SPEC:59 | Typical | fallback 30 s | true | passes (cited run) | OK |
| G1 | SPEC:59 | Legitimate Edge Case | fallback 45-60 s | true/false | "well inside" the limit, no number given; the 45 s in the cited run was the `--timeout-ms` given then (CAPS:49) | GAP (M9) |
| G2 wait split | SPEC:68 | One/Minimal | a 1-minute wait | n/a | no split needed | OK |
| G2 | SPEC:68 | Typical | 4 min | true | split into waits <= 4 min | OK |
| G2 | SPEC:68 | Maximum/Overflow | one call of 3600 s (cli-eval, A:65) | true | split (cli-eval row, SPEC:104) | OK |
| G3 outcome | SPEC:63 | Zero/Empty | no report file | true | `--outcome failed` | OK |
| G3 | SPEC:63 | Zero/Empty | report exists but is empty, unparseable, or `status` outside the four values | unspecified | not stated (7.2 step 4 only tests it, SPEC:183) | GAP (M7) |
| G3 | SPEC:63 | Sentinel Value Match | `partial` with no usable deliverable | true | mapped to `succeeded` regardless (SPEC:263) | OK (deliberate) |
| G3 | SPEC:63 | Legitimate Edge Case | verdict FAIL audit | true | `succeeded` | OK |
| G4 `--unattended` | SPEC:51 | Zero/Empty | flag absent | false | today's behaviour (SA-1, SPEC:146) | OK |
| G4 | SPEC:51 | Sentinel Value Match | the text `--unattended` inside a quoted argument; `--unattended` together with `--interactive` on a command the spec does not list | unspecified | not stated; the command being run here defines a token rule (CMD:459) | GAP (M8) |
| G5 contract location | SPEC:62 | Typical | `--output <dir>` passed | true | `<dir>/return-contract.yaml` | OK |
| G5 | SPEC:62 | Zero/Empty | no output flag, or dir missing/unwritable under `--unattended` | unspecified | "written on every outcome" cannot hold; no refusal rule | GAP (M3) |
| G5 | SPEC:62 | Legitimate Edge Case | `--output` is a file (tdd, init-lite, SPEC:87,90) | unspecified | "the directory the coordinator passed" does not exist | GAP (M3) |

### Quantity Flow Diagram (count check of section 3)

```text
[43 commands] --> [10 ready (3.1)]  --> P1 fixes 4 (adversarial, cleanup-audit, index-repo, workflow); P2 4 (reflect, release-split, tdd, troubleshoot)
              --> [27 change (3.2)] --> P1 9 | P2 11 | P3 4 | P4 3
              --> [6 coordinator-only (4)]
P1 scope text (SPEC:159): "--unattended accepted by every command in 3.1 and 3.2" = 37 commands
P1 command list (SPEC:159): 9 + 4 fixes = 13   <-- MISMATCH (see M2)
AC-1.1 (SPEC:195): section required on all 37 at P1  <-- MISMATCH with P2-P4 gate work and with load (F1)
```

## === REQUIREMENTS ANALYSIS === (Wiegers, Adzic, Cockburn)

### F1 - CRITICAL (blocking) - Wiegers - load: acceptance check and phase scope contradict the load row
- Texts: AC-1.1 requires "every command in sections 3.1-3.2" to have a `## Unattended mode` section "naming `return-contract.yaml`" (`SPEC:195`); section 3 says every changed command gains that section (`SPEC:76`); P1 lists "load (usage line only)" (`SPEC:159`) and the load row says report "none (see note)", "use it as a step inside another worker's brief, not as its own Task", change is the usage line only (`SPEC:112`); the Decisions row says "a report file would be an unrequested addition. Only its usage-line defect is fixed" (`SPEC:265`). WC-4 says the contract is written on every outcome (`SPEC:62`).
- Grading sentence: An implementer who follows the stated text as written builds, for /sc:load, either a usage-line fix only (`SPEC:112,159,265`), which fails AC-1.1 (`SPEC:195`), or an `## Unattended mode` section naming `return-contract.yaml` (`SPEC:195`, `SPEC:62`), which adds the report file that `SPEC:265` rules out; one of the two stated texts must lose, and the phase check cannot pass while both stand.
- Recommendation: narrow AC-1.1 to "every command whose section 3 row names a report", with load listed as the exception; or delete load from the 3.1-3.2 list the test iterates. Prefer the narrowing (no new text elsewhere).
- Priority: High. Quality impact: Testability +1.

### F2 - CRITICAL (blocking) - Crispin/Wiegers - AC-0.4 requires a step-3 condition that Phase 0 cannot meet
- Texts: AC-0.4 says "steps 1-3 and 5-7 pass; step 4 uses the command's existing report file, since the contract arrives in P1" (`SPEC:194`); step 3 passes only if "its `--outcome` matches the contract's `status` under WC-5; its report path is the WC-4 contract path" (`SPEC:182`); P0 contains "no command edits" (`SPEC:158`) and the WC-4 contract is a P1 deliverable (`SPEC:159`). The three P0 commands: troubleshoot reports `REPORT.md` with no `status` (B:242, `SPEC:91`), workflow's contract sits at `.dev/tasks/to-do/<id>/` (`SPEC:92`), adversarial's filename is not fixed until P1 (`SPEC:83`).
- Grading sentence: An implementer who follows the stated text as written runs the P0 smoke runs and applies step 3 to them, and the run cannot pass, because no P0 command writes a WC-4 contract at the WC-4 path; the phase gate "later phases do not start until the earlier phase's checks pass" (`SPEC:154`) then blocks the whole rollout, and the sentence at `SPEC:194` ("a failure here reopens section 1") would reopen the decision on a defect of the check.
- Recommendation: in AC-0.4 replace "steps 1-3" with "steps 1-2" plus "step 3 with the pass condition 'exactly one `worker_done`; its report path is the command's existing report file'" (narrowing, no new mechanism).
- Priority: High. Quality impact: Testability +2.

### F3 - CRITICAL (blocking) - Adzic - cli-portify: the happy-path check cannot pass, because every gate resolves only as blocked
- Texts: cli-portify row: "each of the three approval gates resolves as blocked", resume via `--resume <contract>` (`SPEC:105`); the gates are always on (A:45); WC-2 allows three resolutions (default, caller flag, blocked) (`SPEC:60`), but the row picks only the third and lists no flag that carries an approval; AC-2.3: "Happy-path run per P2 command with every required flag in the brief ... 7.2 passes with `--outcome succeeded`" (`SPEC:201`) and P2 contains cli-portify (`SPEC:160`).
- Grading sentence: An implementer who follows the stated text as written builds a cli-portify that stops as blocked at the first approval gate on every unattended run and, on resume, reaches the same gate again, because no listed flag or contract field records an approval; AC-2.3 requires a `succeeded` run, which that build can never produce.
- Recommendation: either name the approval input (one flag, resolution (b) of WC-2) in the cli-portify row, or narrow AC-2.3 to say cli-portify's expected unattended result is `blocked` / `failed` at the first gate. Prefer the AC-2.3 narrowing.
- Priority: High. Quality impact: Completeness +1, Testability +2.

### Medium findings (follow-up candidates, not blocking)

- **M1 (WC-3 versus D2 and Non-goal 6)** - Wiegers. WC-3 lets any worker with a preamble ask the coordinator and "re-invoke ... with the answer as a flag" for every gate that resolves as blocked (`SPEC:61`); implement's gate resolves as blocked (`SPEC:109`) while D2(a) recommends that the worker stop and end `failed` and Non-goal 6 keeps the Ruling rule (`SPEC:234,218`). Medium because the text says "may"; the worse reading is a coordinator reply fed back as a Ruling, which the rule quoted at `SPEC:233` rejects. Recommend scoping WC-3 with "except where the command's own rule names who may answer (implement, D2)".
- **M2 (P1 scope versus list and the interim state)** - Cockburn. P1 says `--unattended` is accepted by "every command in sections 3.1 and 3.2 (a no-op where a command has no gate)" (`SPEC:159`) but names 13 commands in the same row; the gate resolutions land in P2-P4 (`SPEC:160-162`), and section 2.3 tells the coordinator to put `--unattended` in every brief (`SPEC:73`). After P1 a brief for auggie-review or post-release can carry a flag that is accepted while the post and install defaults are still on (`SPEC:100,113`; WC-9 `SPEC:67`). The text never says which commands may be dispatched with the flag before their phase lands. Recommend one sentence: dispatch a command with `--unattended` only after its phase.
- **M3 (WC-4 location for file-valued `--output`, and absent or unwritable directory)** - Wiegers. WC-4 puts the contract in "the directory the coordinator passed (`--output` / `--output-dir`)" (`SPEC:62`) and 2.3 requires the brief to give "the output directory" (`SPEC:73`), but tdd and init-lite take `--output <file>` (`SPEC:87,90`; AC-2.2 uses `--output <file>`, `SPEC:200`). The command definition used for this review separates a file-valued `--output` from a directory flag `--report-dir` and refuses without it (CMD:23,460). The spec names no directory flag for those commands and no refusal rule when the directory is missing or unwritable (guard table G5). SA-3 also allows the contract "when the caller passes the new output flag" while WC-4 says "in unattended mode" (`SPEC:148,62`).
- **M4 (WC-6 "fresh output directory" versus WC-4 "known before dispatch")** - Fowler. For the 17+ commands with resume "fresh dir" (`SPEC:99-125`), WC-6 says the command writes each run into a fresh directory (`SPEC:64`), while WC-4 and 2.3 say the report path is fixed before dispatch (`SPEC:62,73`). It does not say who creates the fresh directory or what the retry brief passes, so the first attempt's path and the retry's path can differ.
- **M7 (contract status vocabulary)** - Adzic. WC-4 fixes `status` to four values and tells commands that already write a contract to "keep their fields" (`SPEC:62`); the existing contracts' `status` values are not shown in the inventories (B:272 gives only that `failed` exists), and 7.2 step 4 asserts the four-value set (`SPEC:183`). No contract version field is required, though workflow's contract is versioned (B:272). Whether brainstorm, reflect, workflow and adversarial already pass step 4 is UNVERIFIED. Also unspecified: a report that exists but is empty or invalid (guard table G3).
- **M8 (switch token rules)** - Cockburn. `--unattended` is defined only by D1(a) (`SPEC:51,228`). Missing: text inside a quoted argument (a rule the command being run here already has, CMD:459), and the case `--unattended` plus `--interactive` on commands whose rows do not refuse it (`SPEC:84,146`).
- **M9 (WC-1 has no number)** - Wiegers. "Well inside the readiness limit (default 60 s)" (`SPEC:59`); the cited 45 s figure was the limit supplied to that run (CAPS:49), so "above about 45 s it fails again" is not a property of the 60 s default. An implementer cannot test the criterion as written.
- **M11 (AC-1.1 and pr-submit)** - Wiegers. AC-1.1 runs at P1 for every 3.2 command including pr-submit (`SPEC:195`), while D3(a), the recommendation, makes "no pr-submit changes" (`SPEC:240`) and section 4 treats it as a worker only under D3(b) (`SPEC:139`). Same cure as F1: scope the test to commands that have been changed in that phase.

## === ARCHITECTURE ANALYSIS === (Fowler, Newman, Hohpe, Nygard)

- Sound: the decision itself (Orca above, commands as units; `SPEC:16`, rejected alternative R1-R5 `SPEC:31-37`) is backed by CAPS:97-103, 145-150, and the gaps are stated (`SPEC:41-45`). The shared contract file keeps the rules in one place (`SPEC:52`). Interface segregation is good: no command touches Orca (SA-2).
- **M5 (additive-edit check misses deletions)** - Fowler. AC-C5 and AC-0.3 use `grep -E '^-[^-]'` on `git diff -U0` and say "prints nothing: edits are additive" (`SPEC:176,193`). A deleted markdown bullet or frontmatter line appears in a diff as `-- text` or `----`, which that pattern does not match; I ran the pattern on sample diff lines and `-- Will Not item` and `----` were not printed while `-| row` and `-plain` were. Most lines in command files are bullets, so a removed bullet passes the check and SA-1/SA-4 are not enforced where it matters most. Recommend `grep -E '^-' | grep -vE '^---'`.
- **M6 (AC-C1)** - Nygard. AC-C1 scans `src/superclaude/core` and requires empty output (`SPEC:172`), but P0 adds an Orca section to `HOW-WE-WORK.md` and a contract file in `core/` (`SPEC:158`), and SA-2 allows an Orca mention "as an example of a caller's question channel inside the contract file" (`SPEC:147`); if that mention is written as `orca orchestration ask` the check fails the phase. Also the pattern is written with `\|` inside a grep -E expression (`SPEC:172`); copied from the raw file, `\|` is a literal pipe in ERE, and my run of that exact pattern matched nothing, so the check passes vacuously. (A rendered table would show `|`; the source does not.)
- Reliability (Nygard): liveness is covered (WC-10, WC-12). Not covered: the contract written first as `blocked` and then overwritten after an `ask` round trip (WC-3 with WC-4); see M4.
- Integration (Hohpe): the report handoff is by file pointer only and Orca is not known to check the file (`SPEC:62`, CAPS:79); the spec handles this by making the coordinator open it. Adequate.

## === ADVERSARIAL ANALYSIS === (Whittaker)

- Zero/Empty attack: I can break this specification by **Zero/Empty**. The invariant at **WC-4 (`SPEC:62`) "written on every outcome"** fails when **the output directory is absent or unwritable**. Concrete attack: before = brief omits `--output`; run with `--unattended`; no directory, so no contract; WC-5 then maps "no report" to `failed` (`SPEC:63`); after = a `failed` worker with no reason on disk. See M3, guard table G5.
- Sequence attack: I can break this specification by **Sequence**. The invariant at **AC-0.4 (`SPEC:194`)** fails when **step 3 runs before the contract exists**. Concrete attack: before = P0 start; troubleshoot runs, writes `REPORT.md`; step 3 compares `--report-path` to the WC-4 path; after = the check fails on a correct run. See F2.
- Divergence attack: I can break this specification by **Divergence**. The invariant at **WC-2 (`SPEC:60`)** fails when **a gate has only the blocked branch** (cli-portify). Concrete attack: run 1 blocks at the Phase 1/2 gate; resume reads the contract and reaches the same gate; state = unchanged. See F3.
- Sentinel collision: see M8 (a quoted `--unattended` token).
- Accumulation attack: no counter in the spec reaches a bound that the text leaves open, except the review loop's own cap, which the spec does not use.

## Follow-up candidates (Medium and minor; never trigger a revision)

Medium: M1, M2, M3, M4, M5, M6, M7, M8, M9, M11 (above).
Minor notes:
- n1: `SPEC:214` states tasklist's reflect fan-out is inside the nesting limit; B:210 and B:314 call nested spawning UNVERIFIED.
- n2: E5 (`SPEC:25`) rests on a grep run outside the workspace; UNVERIFIED here, as are `install_core.py:13-24`, `pyproject.toml:38`, `CLAUDE.md` lines, `HOW-WE-WORK.md` lines and the `.dev/codegraph-migration` and `EVIDENCE.md` lines (the latter are quoted at CAPS:49 only in part).
- n3: AC-0.2 compares one mirrored copy of `HOW-WE-WORK.md` but P0 says "two mirrored copies" (`SPEC:158,192`).
- n4: the spec-panel row says "add `--output`" (`SPEC:120`) while the command used for this review already lists `--output <file>` (CMD:23); the inventory was taken from an earlier read (B:182).
- n5: E3 cites a `skill-direct` contract as evidence that the direct route works (`SPEC:23`) while 1.4(1) says that run was subagent-wrapped (`SPEC:43`); the spec states the gap itself, so only the table row overstates.

The question whether to open an issue for these follow-up candidates was not put to a user (this review ran as one reviewer of a coordinated loop); no issue was created. The coordinator owns that question.

## Reviser brief

Repair only the blocking findings F1, F2, F3 in the candidate `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`, and nothing else. Rules from the Review Loop (reviser contract), restated because the reviser reads this report and not the command: revise only text a blocking finding names; add no rule, mechanism or section that no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id. Leave Medium and minor findings alone. Return the candidate once and do not award yourself a PASS.

Findings (id, texts, stated wrong outcome):
- F1: `SPEC:195` (AC-1.1, "every command in sections 3.1-3.2 has a `## Unattended mode` section naming `return-contract.yaml`"), `SPEC:76`, `SPEC:159` ("load (usage line only)"), `SPEC:112` (load report "none"), `SPEC:265` ("a report file would be an unrequested addition"). Wrong outcome: the P1 check cannot pass for /sc:load without adding the report file the spec rules out.
- F2: `SPEC:194` (AC-0.4, "steps 1-3 and 5-7 pass"), `SPEC:182` (step 3, "its report path is the WC-4 contract path"), `SPEC:158` (P0 has no command edits). Wrong outcome: the P0 gate fails on correct runs because no WC-4 contract exists in P0.
- F3: `SPEC:105` (cli-portify gates "resolve as blocked"), `SPEC:201` (AC-2.3 requires `--outcome succeeded`), `SPEC:160` (cli-portify in P2). Wrong outcome: the happy-path check cannot pass; every unattended run stops at the first approval gate.

verdict: FAIL

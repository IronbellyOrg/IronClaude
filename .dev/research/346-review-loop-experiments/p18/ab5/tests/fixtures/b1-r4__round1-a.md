review: 1 of 3

# Spec-panel critique: orca-worker-contract-spec.md (first review)

- Command: `/sc:spec-panel @.dev/orca-command-refactor/specs/orca-worker-contract-spec.md --mode critique --focus requirements,architecture`
- Candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`
- Candidate sha256: `d3cdbe573e57303b9ce6c93d1fe98ba18fb7cb1a15773d926bf6a0c31425200d`
- Baseline: none given (first review of the full document)
- Reviewer model actually used: claude-sonnet-5-5
- Prompt followed: FIRST-REVIEW prompt in `~/.claude/rules/prompts/document_review_loop_prompts.md:29-36`, read in full (hard gate, `command.md:266-268`).
- Citation key: `SPEC:N` = line N of the candidate. `INV-A:N`, `INV-B:N`, `CAPS:N` = lines of `.dev/orca-command-refactor/inventory/commands-a.md`, `commands-b.md`, `orca-capabilities.md`. `CMD:N` = line N of the `/sc:spec-panel` definition (`command.md`) in this sandbox. Anything not in the workspace (`src/`, `CLAUDE.md`, `EVIDENCE.md`, the codegraph README, Orca's own files) is UNVERIFIED unless an inventory line quotes it; the inventory line is then the evidence.

## Coverage

- Read in full: README, candidate (285 lines), the three inventories where the candidate cites them, and the review-loop prompts.
- Checked against the inventories: the 10 / 27 / 6 split (it adds up to 43: SPEC:76, rows SPEC:81-92 and SPEC:97-125, SPEC:130-137; 5 ready in `INV-A:35-55` and 5 in `INV-B:31-52`), about 40 `CAPS:` quotes (all matched the claim they support, for example `CAPS:97-101` for R1, `CAPS:58-64` for WC-3, `CAPS:73` for WC-5), and the verdicts in `INV-A:76-83` and `INV-B:289-299`.
- Not checkable here (UNVERIFIED): every `cmd/` and `sk/` line number that the inventories did not also quote, `CLAUDE.md:N`, `pyproject.toml:38`, `src/superclaude/cli/install_core.py`, the PR #329 run, and the claim at SPEC:11 that 11 locations were re-read.
- Experts applied (fixed order, `CMD:99-113`): Wiegers, Adzic, Cockburn (requirements); Fowler, Nygard, Newman, Hohpe (architecture); Whittaker (adversarial, always active). Crispin, Gregory, Hightower were not used, since `--focus` was requirements,architecture.
- Pipeline Dimensional Analysis: not triggered. The only counted flow is the 43-command split, and it has no stage whose output count differs from its input (see Coverage). Correctness focus is off, so no State Variable Registry.

## Blocking findings

### F1 (blocking, Wiegers / Adzic): AC-1.1 requires a contract-naming `## Unattended mode` section on `/sc:load`, which the spec says gets no report

- Texts that conflict:
  - AC-1.1 (SPEC:195): the test "asserts that every command in sections 3.1-3.2 has a `## Unattended mode` section naming `return-contract.yaml` and `~/.claude/WORKER-CONTRACT.md`".
  - `/sc:load` is in section 3.2 and its Report cell is "none (see note)", Resume "n/a", and "use it as a step inside another worker's brief, not as its own Task" (SPEC:112).
  - Decisions (SPEC:265): "a report file would be an unrequested addition".
  - WC-4 (SPEC:62) makes the contract the thing an unattended command writes; P1 scope for load is "usage line only" (SPEC:159).
- Grading sentence: An implementer who follows SPEC:112 and SPEC:265 gives `/sc:load` only a usage-line fix and no contract section, and that implementation fails AC-1.1 at SPEC:195. Following AC-1.1 instead makes the implementer add a contract-naming section to a command the spec says writes no report, which contradicts SPEC:265. Both builds are wrong because the spec says both are right.
- Why blocking: two stated texts contradict, and an acceptance criterion cannot pass under the other text.

### F2 (blocking, Adzic / Wiegers): AC-0.4 step 3 cannot pass in P0 for the commands it names

- Texts: AC-0.4 (SPEC:194) says "steps 1-3 and 5-7 pass; step 4 uses the command's existing report file, since the contract arrives in P1". Step 3 of the live check (SPEC:182) requires "its `--outcome` matches the contract's `status` under WC-5; its report path is the WC-4 contract path".
- Facts the spec itself states: in P0 no command has the WC-4 contract or `--unattended` (the contract is added in P1, SPEC:159; SPEC:79 says the worker "reports the named file until Phase 1 adds the contract"). The `/sc:troubleshoot` row names `REPORT.md` as its report (SPEC:91). The inventory confirms troubleshoot writes `return-contract.yaml` only with `--caller task-unified` (`INV-B:242`), so it has no contract `status` to match.
- Grading sentence: An implementer who runs AC-0.4 as written on `/sc:troubleshoot "<symptom>"` finds no contract file, so "the contract's `status`" and "the WC-4 contract path" in step 3 do not exist, and the check cannot pass. The same holds for `/sc:adversarial`, whose contract filename is not fixed until P1 (SPEC:83; `INV-A:60`). AC-0.4 exempts only step 4, not step 3.
- Why blocking: an acceptance criterion cannot pass as written. The fix is narrow (step 3 in P0 compares the outcome with the command's existing report, as step 4 already does).

## Follow-up candidates (Medium and minor, not blocking, not in the Reviser brief)

Each Medium needs a guess about which reading the implementer picks, or is a requirement the spec never states.

- FU-1 (Medium, Wiegers/Fowler): the contract path is undefined for file-valued `--output`. WC-4 (SPEC:62) puts the contract at `<output-dir>/return-contract.yaml`, "the directory the coordinator passed (`--output` / `--output-dir`)". But `/sc:tdd` and `/sc:init-lite` take `--output <file>` (SPEC:87, SPEC:90) and `/sc:spec-panel` gets `--output` (SPEC:120). `CMD:460` shows the same command treats `--output` as file-valued and needs a separate `--report-dir`. The spec does not say where the contract goes for these. An implementer may write `<file>/return-contract.yaml`.
- FU-2 (Medium, Nygard/Whittaker, sequence attack): between P1 and P2/P3/P4 the spec says nothing about what `--unattended` does on a gated command. P1 makes every command in 3.1-3.2 accept the flag, "a no-op where a command has no gate" (SPEC:159), and AC-1.1 requires each to carry the section (SPEC:195). The gate resolutions for auggie-review, task, post-release and pr-submit land in P2 or P4 (SPEC:100, SPEC:113, SPEC:114, SPEC:121). A coordinator that follows SPEC:73 and passes `--unattended` after P1 gets a command that still posts to GitHub or waits. The spec has no per-phase list of which commands are safe to dispatch. This is close to the safety line; it is Medium only because the text allows the safe reading.
- FU-3 (Medium, Wiegers): SPEC:73 says the brief states the output directory "so the report path is known before dispatch", but the "Brief must pass" column for reflect, troubleshoot, workflow, index-repo and cleanup-audit omits an output flag (SPEC:85-86, SPEC:88, SPEC:91-92). Troubleshoot's default directory has a timestamp (`INV-B:242`) and reflect's default is `.dev/reflect/<mode>-<slug>-<ts>/` (`INV-B:112`), so the path is not known before dispatch.
- FU-4 (Medium, Fowler): the tasklist row (SPEC:122) has Stage 10.5 pass `--unattended` to each reflect "so the headless rule applies", while the reflect row says the brief passes no `--remediate` (SPEC:88). The inventory's verdict was to drop `--remediate` in Stage 10.5 so no offer can fire (`INV-B:46`, `INV-B:210-215`), and `INV-B:107` says the headless rule auto-accepts remediation for auto-fixable registers. The spec departs from the inventory without a Decisions row, and its claim that the fan-out is "inside Claude Code's nesting limit" rests on `INV-A:14`, while `INV-B:46` and `INV-B:210` mark the nested spawning UNVERIFIED. Stage 10.5 under `--unattended` may therefore start remediation inside nested subagents.
- FU-5 (Medium, Fowler): WC-3 (SPEC:61) lets any worker ask the coordinator and "re-invoke or resume the command with the answer as a flag". For `/sc:implement`, D2(a) (SPEC:234) says the worker ends `failed` and no relayed Ruling is accepted, because `qa.md:238` excludes "another agent's message" (`INV-A:66`). WC-3 has no exception for it, and `/sc:implement` has no Ruling flag to carry the answer.
- FU-6 (Medium, Whittaker, divergence attack): the heartbeat thresholds differ. WC-10 (SPEC:68) splits a blocking call "longer than 5 minutes" into waits "of at most 4 minutes". AC-4.3 (SPEC:210) and the pr-submit row (SPEC:114) require no single call over 240 s. A 270 s call is allowed by WC-10 and fails AC-4.3.
- FU-7 (Medium, Nygard): WC-6 (SPEC:64) says a re-run command "writes each run into a fresh output directory", yet the caller supplies the directory (SPEC:62, SPEC:73). A retry worker given the same `<output-dir>` overwrites the first attempt's contract and report. SPEC:73 does not say a retry brief needs a new directory.
- FU-8 (Medium, Whittaker, sequence attack): stale contract. WC-3 has the worker re-invoke the command after a `blocked` run (SPEC:61) and WC-4 writes `<output-dir>/return-contract.yaml` (SPEC:62). If the second run dies before it writes, the old `status: blocked` file stays. WC-5 maps "no report exists" to `failed` (SPEC:63) but does not cover a leftover report from an earlier run. A coordinator reading it sees a stale question.
- FU-9 (Medium, Whittaker, sentinel collision attack): the spec says `--unattended` is a flag the coordinator writes into the command line (SPEC:51, SPEC:228) but gives no parse rule. `CMD:459` shows the rule other text uses: a standalone token outside quoted content. Without it, `/sc:tdd "explain the --unattended flag"` could switch mode.
- FU-10 (Medium, Whittaker, zero/empty attack): `--unattended` with no output directory is undefined. WC-4 needs the directory (SPEC:62) and the brief should carry it (SPEC:73), but the spec does not say whether the command refuses or picks a default. `CMD:460` refuses before any work and prints the refusal in chat only.
- FU-11 (Medium, Fowler): WC-11 (SPEC:69) says two workers in one worktree must never write the same file. `/sc:cleanup-audit` (fixed output directory, SPEC:85) and `/sc:index-repo` (`PROJECT_INDEX.md`, SPEC:86) are listed "ready today" and keep fixed paths; the cleanup-audit row concedes "one audit per worktree at a time". No acceptance check covers it.
- FU-12 (Medium, Newman): WC-4 says commands that already write a contract "keep their fields and add the missing ones" (SPEC:62), while the Decisions row fixes a four-value `status` set (SPEC:262). Existing contracts already carry a version (`contract 1.1`, `INV-B:272`) and their own status values. The spec does not say what happens to a command whose existing `status` vocabulary differs, and the new file has no schema-version field.
- FU-13 (Medium, Fowler): SA-2 and AC-C1 (SPEC:147, SPEC:172) forbid `orca orchestration|worktree|terminal|agent` text under `src/superclaude/core`, but P0 adds an Orca section to `core/HOW-WE-WORK.md` and a coordinator brief template to `core/WORKER-CONTRACT.md` (SPEC:158). E5 (SPEC:25) records `grep -ci orca HOW-WE-WORK.md` as `0` today. Whether those new texts name Orca commands is not stated, so AC-C1 may fail on the spec's own P0 output.
- FU-14 (Medium, Cockburn): `/sc:pr-submit` is listed as "Will Not: run headless" (`INV-B:90`, quoting `cmd/pr-submit.md:85`), and the pr-submit row (SPEC:114) and D3(b) (SPEC:241) add an unattended mode without addressing that line. D3(a) leaves pr-submit unchanged, yet it stays counted among the 27 commands that need a change (SPEC:76, SPEC:114).
- FU-15 (Medium, Nygard): no operational rule for a stalled worker. SPEC:44 admits a prompt-parked worker is "healthy" to Orca and invisible without `worker-show` (`CAPS:129`). SPEC:181 only tests that `agentWait` stays null; SPEC:73 does not say what the coordinator does when it is not null (reply, send, stop).
- FU-16 (Medium, Wiegers): AC-C5 (SPEC:176) fails on any deleted line, but P1 adds flags (`--unattended`, `--output`, SPEC:159) that appear on Usage lines. Adding a flag to an existing Usage line deletes the old line. The spec does not say new flags go on a new line.
- FU-17 (Medium, Cockburn): SA-3 (SPEC:148) allows the contract "when the caller passes the new output flag", WC-4 (SPEC:62) writes it only "in unattended mode". The two disagree for a person who passes `--output` without `--unattended`.
- FU-18 (minor): SPEC:16 says the changes in commands are "limited to" the worker contract, but section 3 and SA-4 (SPEC:149) also list drift fixes (roadmap, validate-roadmap, validate-tests, explain tools, business-panel frontmatter).
- FU-19 (minor): the top-level rule is cited as `sk/sc-pr-submit-protocol/SKILL.md:37-39` (SPEC:65) while `CAPS:161` quotes the installed copy at `:47-49`. The copies may differ by 10 lines; UNVERIFIED.
- FU-20 (minor): the P1 "Ready today" intro (SPEC:79) says the only changes are small fixes, but reflect, release-split, tdd and troubleshoot get P2 gate conversions (SPEC:88-91), and brainstorm and init-lite (small fix "None") still need the P1 section under AC-1.1.

Question on follow-up candidates: this run is a single reviewer that cannot ask the user. The coordinator session asks once per loop whether to open an issue for FU-1 to FU-20 and creates none without an answer (`CMD:260`).

## === REQUIREMENTS ANALYSIS ===

Experts: Wiegers (lead), Adzic, Cockburn, Whittaker.

Strengths (evidence): every WC row names an owner and evidence (SPEC:57-70); the three evidence gaps are stated plainly (SPEC:42-45); UNVERIFIED items are listed (SPEC:271-285) and match `CAPS:177-188` (for example `CAPS:180`, `CAPS:186-188`).

| id | issue | severity | expert | recommendation | priority |
|---|---|---|---|---|---|
| F1 | AC-1.1 vs load (SPEC:195, SPEC:112, SPEC:265) | blocking | Wiegers, Adzic | exclude load from the AC-1.1 set or give it a contract | High |
| F2 | AC-0.4 step 3 needs a contract that P0 lacks (SPEC:194, SPEC:182) | blocking | Adzic | let step 3 use the existing report in P0 | High |
| FU-1, FU-3, FU-10 | contract path and output-dir rules incomplete | Medium | Wiegers | state the path for file-valued `--output`; refuse when no directory is given | Medium |
| FU-2 | no per-phase availability of `--unattended` on gated commands | Medium | Cockburn | add a "safe to dispatch after phase N" column | Medium |
| FU-9 | no parse rule for the flag | Medium | Whittaker | standalone token outside quotes | Low |
| FU-17 | SA-3 vs WC-4 | Medium | Wiegers | one rule for when the contract is written | Low |

Quality-impact estimate: fixing F1 and F2 moves the acceptance section from partly unpassable to passable for P0 and P1.

## === ARCHITECTURE ANALYSIS ===

Experts: Fowler (lead), Nygard, Newman, Hohpe, Whittaker.

Assessment: the central decision (Orca on top, commands stay units of work, no Orca calls in commands) is consistent with its evidence (`CAPS:97-101` for R1, `CAPS:145-150` for R2-R4, `INV-B:285-287` for R5). The rejected alternative is argued from facts, not taste. The weak points are at the seams: the contract file (path, version, staleness: FU-1, FU-8, FU-12), retries (FU-7), and the one place where the spec departs from the inventory (tasklist and reflect, FU-4).

| id | issue | severity | expert | recommendation | priority |
|---|---|---|---|---|---|
| FU-4 | tasklist Stage 10.5 vs reflect and `INV-B:46` | Medium | Fowler | record a Decisions row or follow the inventory | Medium |
| FU-5 | WC-3 vs D2(a) | Medium | Fowler | exempt `/sc:implement` from the ask-and-reinvoke step | Medium |
| FU-7, FU-8 | retry and stale contract | Medium | Nygard | require a fresh directory per attempt; delete or stamp the contract at start | Medium |
| FU-12 | status vocabulary and no schema version | Medium | Newman | add `schema_version`; say how existing statuses map | Medium |
| FU-15 | stalled-worker policy | Medium | Nygard | state the coordinator's action on `agentWait` | Medium |
| FU-13 | AC-C1 vs P0 core text | Medium | Fowler | say that core text names no Orca commands, or narrow the grep | Low |

## Whittaker adversarial findings

Format per `CMD:82`.

1. I can break this specification by the **Sequence Attack**. The invariant at **WC-3 with WC-4 (SPEC:61-62)** fails when **a blocked run is re-invoked and the second run dies before writing**. Concrete attack: state before: `<dir>/return-contract.yaml` has `status: blocked`, question Q. The coordinator answers Q, the worker re-invokes, and the command is killed. State after: the old file is unchanged, the worker has no new report, WC-5 sees a report and maps `blocked` to `failed` with a stale question. Severity: MAJOR, graded Medium (FU-8), because the text allows a safe reading.
2. I can break this specification by the **Divergence Attack**. The invariant at **WC-10 (SPEC:68) vs AC-4.3 (SPEC:210)** fails when **a single tool call lasts 270 s**. Concrete attack: WC-10 requires no split (270 s is under 5 minutes), AC-4.3 fails the run (over 240 s). Severity: MAJOR, graded Medium (FU-6).
3. I can break this specification by the **Zero/Empty Attack**. The invariant at **WC-4 (SPEC:62)** fails when **the brief gives no output directory**. Concrete attack: command runs under `--unattended` with no `--output`; the spec defines no refusal and no default, so the contract path is whatever the implementer chooses. Severity: MAJOR, graded Medium (FU-10).
4. I can break this specification by the **Sentinel Collision Attack**. The invariant at **SPEC:51 / SPEC:228** fails when **quoted content contains the text `--unattended`**. Concrete attack: `/sc:tdd "document the --unattended flag"` is read as the switch, prompts vanish for a person. Severity: MAJOR, graded Medium (FU-9).
5. I can break this specification by the **Accumulation Attack**. The invariant at **WC-6 (SPEC:64)** fails when **a Task is retried up to the circuit-breaker limit (three, `CAPS:80`, `CAPS:116`) with the same output directory**. Concrete attack: attempts 1 to 3 write to one `<output-dir>` for a "fresh dir" command; attempt 3 starts from the leftovers of attempt 2. Severity: MAJOR, graded Medium (FU-7).

## Guard Condition Boundary Table

Guards found: the wait-split threshold, the outcome mapping, the unattended switch, the nesting depth, and the confidence band. Input classes left out are named in the last column of the row.

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|---|---|---|---|---|---|---|
| wait split (blocking call > 5 min) | WC-10, SPEC:68 | Zero/Empty | 0 s wait | false | none stated; no split needed | OK (nothing to wait for) |
| wait split | WC-10, SPEC:68 | Typical | 2 min | false | no split | OK |
| wait split | WC-10 vs AC-4.3, SPEC:68, SPEC:210 | Legitimate Edge Case | 270 s | false (WC-10) / fail (AC-4.3) | WC-10 allows it, AC-4.3 rejects it | GAP (FU-6) |
| wait split | WC-10, SPEC:68 | Maximum/Overflow | 3600 s eval | true | split into waits of at most 4 min (SPEC:104) | OK |
| outcome mapping | WC-5, SPEC:63 | Zero/Empty | no report exists | n/a | `failed` | OK |
| outcome mapping | WC-5, SPEC:63 | Legitimate Edge Case | report left over from an earlier run | n/a | not specified | GAP (FU-8) |
| outcome mapping | WC-5, SPEC:63 | Sentinel Value Match | `status` outside the four values (existing contracts) | n/a | not specified | GAP (FU-12) |
| `--unattended` switch | SPEC:51 | Zero/Empty | flag absent | false | today's behaviour (SA-1, SPEC:146) | OK |
| `--unattended` switch | SPEC:51 | Sentinel Value Match | the text inside quoted content | unspecified | not specified | GAP (FU-9) |
| `--unattended` switch | WC-4, SPEC:62 | Zero/Empty | flag present, no output directory | unspecified | not specified | GAP (FU-10) |
| nesting depth (1) | R1, SPEC:33 | Typical | worker starts a worker | true | refused with `nested_worker_depth_exceeded` (`CAPS:99`) | OK |
| nesting depth (1) | D5, SPEC:249-253 | Legitimate Edge Case | user raises the depth | n/a | keep depth 1 (recommendation) | OK |
| confidence < 0.70 | task row, SPEC:121 | Zero/Empty | confidence 0 | true | blocked | OK |
| confidence < 0.70 | task row, SPEC:121 | Legitimate Edge Case | exactly 0.70, or 0.70-0.89 band | false | not stated for the 0.70-0.89 "present alternatives" band (`INV-B:199`) | GAP (follow-up; same class as FU-2) |

Classes left out: One/Minimal for the wait guard (no distinct behaviour from Typical); Maximum for the outcome mapping and the confidence guard (no upper bound exists).

Consistency check: the 10 / 27 / 6 totals add up to 43 (SPEC:76; `INV-A:3`, `INV-B:3`). No count mismatch was found.

## Downstream integration

GAP rows above are the entries for `sc:adversarial` AD-1 (`CMD:342`). No `sc:roadmap` hand-off is needed (no Quantity Flow Diagram was produced).

## Reviser brief

Blocking finding ids: F1, F2. The reviser reads this report, not the command.

- Revise only text a blocking finding names: for F1, the AC-1.1 set at SPEC:195 and, if needed, the `/sc:load` row at SPEC:112; for F2, step 3 of the live check at SPEC:182 or the P0 line at SPEC:194.
- Add no rule, mechanism or section that no blocking finding calls for.
- Each added paragraph or table cites its finding id.
- Prefer deleting or narrowing text to adding text.
- Report the byte size of the candidate before and after, and the bytes added and deleted per finding id.
- Leave the Medium and minor items (FU-1 to FU-20) alone. They are not blocking and no "apply all findings" instruction applies.

Brief clauses overridden: none (the task brief only set the focus, mode, and the output file).

verdict: FAIL

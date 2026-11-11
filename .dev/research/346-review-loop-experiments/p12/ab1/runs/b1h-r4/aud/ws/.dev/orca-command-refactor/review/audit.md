review: 1 of 3

# Spec-panel audit: orca-worker-contract-spec.md (whole document, first review)

- candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md` (309 lines)
- candidate sha256: `005c14750dde7985fd4ffcf42529a7b23cc2ca06ed4169b3ad679316a9e00f9a`
- baseline: not given (first review of the whole document, not a re-review). No `--re-review` or `--baseline` was passed, so no `baseline: missing` note applies.
- reviewer model actually used: claude-sonnet-5-5
- command: `/sc:spec-panel @.dev/orca-command-refactor/specs/orca-worker-contract-spec.md --mode critique --focus requirements,architecture`
- label: whole-document audit of the final spec. Per the brief, review followed the FIRST-REVIEW prompt of `~/.claude/rules/prompts/document_review_loop_prompts.md` (read in full, lines 27-32). The Improve step was skipped and no revised specification was written. The only file written is this report.
- Citation convention: `SPEC:N` is line N of the candidate. `INV-A:N`, `INV-B:N`, `CAPS:N` are lines of `inventory/commands-a.md`, `commands-b.md`, `orca-capabilities.md` in the workspace. `CMD:N` is line N of the `/sc:spec-panel` definition `command.md` in the audit sandbox. A citation to a `src/...` file, `EVIDENCE.md`, `CLAUDE.md` or the Orca guides cannot be checked in this workspace and is marked UNVERIFIED.

## Coverage

Read in full: the candidate, `README.md`, the three inventories (spot-checked at every inventory line the candidate cites for counts, verdicts and Orca facts), and the review-loop prompts file. Panel experts applied in the fixed order: Wiegers, Adzic, Cockburn (requirements); Fowler, Nygard, Whittaker, Newman, Hohpe (architecture). Crispin, Gregory and Hightower sit outside the two focus areas and were not run.

Inventory arithmetic checks, all passing:
- 21 + 22 = 43 commands (`INV-A:3`, `INV-B:3`).
- Inventory verdicts are 10 ready (5 in `INV-A` summary, 5 in `INV-B:276-ff`), 27 needs-change (13 + 14), 6 coordinator-only (3 + 3). The candidate's 9 / 27 / 6 plus `/sc:load` reconciles with them (`SPEC:76`, `SPEC:292`).
- Section 3.1 has 9 rows, section 3.2 has 27 rows, section 4 has 6 rows.
- Phase assignment is complete for the 27 section-3.2 rows (P1 9, P2 11, P3 4, P4 3) and for the 9 section-3.1 rows, except for finding M-6.

Citations checked against the workspace and found as cited: `INV-A:3,14,35,53,55,62,65,90,94-98,106,113,118,120`; `INV-B:3,31,36,52,65,105,272,285-286,292,294,296,301,311,320,323`; `CAPS:44-47,52,58-61,64,66-67,72-74,76-77,79-80,86,92,97-103,107,115-116,128-130,145,147-151,155-161,177-188`. UNVERIFIED (outside the workspace): every `src/superclaude/...` line citation in section 3, `EVIDENCE.md`, `CLAUDE.md`, `pyproject.toml:38`, `install_core.py`, the grep run claimed at `SPEC:25`, and the "about 340 citations re-read" claim at `SPEC:309`.

## === REQUIREMENTS ANALYSIS ===

### Blocking findings

**B-1. Phase 1 acceptance requires the `## Unattended mode` section on commands that other stated text says must not change in Phase 1.** (CRITICAL by label; blocking.) Experts: Wiegers, Cockburn. Priority High.
- Stated text A: AC-1.1 passes only if "every command in sections 3.1-3.2 has a `## Unattended mode` section naming `return-contract.yaml` and `~/.claude/WORKER-CONTRACT.md`" (`SPEC:219`). P1 also requires "the `--unattended` flag accepted by every command in sections 3.1 and 3.2" (`SPEC:160`).
- Stated text B: Phase 4 (implement, post-release, pr-submit) "waits for the user's decision" (`SPEC:155`, `SPEC:163`). D3(a), the recommended option, says "no pr-submit changes in Phase 4" and that pr-submit is "Coordinator or person only" (`SPEC:264`). `SPEC:140` says pr-submit is a worker candidate only if D3 is accepted. Section 4 says commands that are not workers "get no `--unattended` mode" (`SPEC:129`). Gate resolutions for the 15 P2 commands, 4 P3 commands and 3 P4 commands are scheduled after P1 (`SPEC:161-163`).
- Grading sentence: an implementer who follows the stated text as written adds an unattended section and flag to pr-submit, implement and post-release in P1 so that AC-1.1 passes, and X is wrong because D3(a) says pr-submit stays out of the worker set, and the P4 commands have no decided gate resolution to write. If the implementer instead skips them, AC-1.1 fails. The two texts cannot both hold. Between P1 and P2 a gated command (for example `cleanup`) would also accept `--unattended` (required in every brief, `SPEC:73`) while still prompting, which breaks WC-2 (`SPEC:60`) with a silent stall (`CAPS:52`, `CAPS:129`).
- Recommendation: scope AC-1.1 and the P1 flag line to the commands whose rows say P1 (plus the 3.1 commands), and state that a command is dispatchable under `--unattended` only after its own phase passes.

**B-2. WC-3 lets a worker obtain a blocked Ruling or authorization from the coordinator, which D2(a) and D4(a) say must not happen.** (CRITICAL by label; blocking.) Experts: Nygard, Fowler, Whittaker. Priority High.
- Stated text A (WC-3, `SPEC:61`): when a gate "would resolve as blocked" and the worker holds a preamble, "the session may instead ask the coordinator once ... then re-invoke or resume the command with the answer as a flag". It has no exception.
- Stated text B: the `/sc:implement` halt row resolves `E-HALT-QA` and `E-NO-RULING` as blocked (`SPEC:108`). The Ruling rule says "another agent's message" is not acceptance (`sk/sc-implement-protocol/refs/qa.md:232,238`, quoted at `SPEC:257`, UNVERIFIED in this workspace; the same rule is quoted at `INV-A:66`). D2(a), the recommended option, says the worker "stops ... and ends `failed`" and a person rules (`SPEC:258`). AC-4.1 requires "the ledger records no Ruling unless D2 allows a relayed one" (`SPEC:232`). D4(a) allows an outward action only when the user's own instruction names it (`SPEC:269`), and WC-9 resolves those gates as off (`SPEC:67`).
- Grading sentence: an implementer who follows WC-3 as written builds a worker that, at a halt, asks the coordinator and resumes with the coordinator's answer as the Ruling. X is wrong because an Orca coordinator is "another agent" (`SPEC:257`), so the worker approves its own work, which is the safety boundary D2 and the Ruling rule exist to hold. WC-3 sits in Phase 0 (`SPEC:159`), before D2 and D4 are decided (`SPEC:155`).
- Recommendation: add to WC-3 that it does not apply to a gate whose open decision (D2, D3, D4) is unresolved, or to any gate the rule file says only a person may clear.

**B-3. The cli-portify row makes every unattended run end blocked, but AC-2.3 requires a happy-path `succeeded`.** (MAJOR by label; blocking.) Experts: Adzic, Wiegers. Priority High.
- Stated text A: "each of the three approval gates resolves as blocked with the artifact to review named in the contract" (`SPEC:104`). Resume is a new `--resume <contract>` flag over `resume_phase` and `resume_substep`. The row does not say that passing `--resume` counts as the approval, and WC-2's option (b), a caller-supplied flag, is not used for any gate.
- Stated text B: AC-2.3: "Happy-path run per P2 command with every required flag in the brief" passes with "`--outcome succeeded`" (`SPEC:225`). WC-5 maps `blocked` to `--outcome failed` (`SPEC:63`).
- Grading sentence: an implementer who follows the cli-portify row builds a command whose first unattended run always stops at gate 1 with `status: blocked`, so WC-5 sends `--outcome failed`, and X is wrong because no set of flags in the brief lets AC-2.3 reach `succeeded` for cli-portify. The acceptance criterion cannot pass.
- Recommendation: state whether `--resume` after the person or coordinator reviews the artifact counts as the approval, or give each gate a caller-supplied approval flag, and say how AC-2.3 is exercised for cli-portify (three chained runs).

### Medium findings (warnings; listed under follow-up candidates)

See the follow-up list below. Findings M-1 to M-3 and M-6 are also requirement defects. They are graded Medium because each needs the implementer to choose the worse of two readings, or the document never states the requirement.

## === ARCHITECTURE ANALYSIS ===

Fowler (interfaces and bounded contexts): the split is sound. Commands stay units of work, Orca owns orchestration, and the shared rules sit in one installed core file (`SPEC:52`, `SPEC:288`). The single `return-contract.yaml` boundary is the right seam. The R1 to R5 rejection of the alternative design is backed by `CAPS:97-103,145-150,155-161`, all of which check out in the workspace. Weak points are the file-valued `--output` mismatch (M-2) and the missing contract version (M-11).

Nygard (failure modes): the spec handles the stall case well (`SPEC:44`, `CAPS:52`). It leaves three failure paths unspecified: a stale contract left by an earlier attempt (M-3), a worker that dies after writing its contract and before `worker_done` (M-9), and an unbounded `ask` resume loop (M-8).

Whittaker (adversarial). Attacks by methodology, with graded outcomes:
- Zero/Empty: output directory missing or unwritable, so "written on every outcome" (`SPEC:62`) cannot hold (M-3).
- Divergence: `--output` is a file for tdd, init-lite and spec-panel but a directory elsewhere (`SPEC:62`, `SPEC:86`, `SPEC:89`, `SPEC:119`) (M-2).
- Sentinel Collision: `status: blocked` versus a command's own statuses. The fixed four-value set is explicit (`SPEC:286`), so no gap. A specification text containing `--unattended` as quoted content is handled in `CMD:459` but not by the spec's D1 (`SPEC:251-254`) (minor N-3).
- Sequence: WC-12 requires `check` before `worker_done` (`SPEC:70`), and WC-5 requires exactly one `worker_done` (`SPEC:63`). They are consistent. AC-0.4 says no contract exists before P1 although adversarial and workflow already write one (M-6).
- Accumulation: WC-6 fresh directories per run accumulate with no cleanup rule (minor N-4).

Newman (evolution): the contract has no schema version, although the workflow contract already carries "contract 1.1" (`INV-B:272`). Adding fields in later phases is therefore unversioned (M-11).

Hohpe (delivery semantics): `worker_done` is exactly-once from the dispatched pane (`SPEC:63`, `CAPS:76`). The contract file and the message are two separate signals with no stated ordering or recovery rule (M-9).

### Guard Condition Boundary Table (hard gate completed before synthesis)

Experts: Nygard (construction), Crispin's completeness duty folded in, Whittaker (attack). One row per applicable input class; classes that cannot occur are left out with a one-line reason.

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|---|---|---|---|---|---|---|
| WC-4 write on every outcome | SPEC:62 | Zero/Empty | output directory missing or not creatable | cannot write | not specified | GAP (M-3) |
| WC-4 write on every outcome | SPEC:62 | Legitimate Edge Case | contract from an earlier attempt already in the directory | file exists | not specified; WC-5 treats "no report exists" as `failed` (SPEC:63) so a stale file reads as a result | GAP (M-3) |
| WC-4 `<output-dir>` | SPEC:62 | Legitimate Edge Case | `--output` is a file path (tdd, init-lite, spec-panel) | not a directory | not specified for tdd or spec-panel; init-lite defined at SPEC:86 | GAP (M-2) |
| WC-5 outcome mapping | SPEC:63 | Zero/Empty | contract exists but `status` missing or not in the four values | no match | not specified (only "no report exists" is mapped) | GAP (minor; folded into M-3) |
| WC-5 outcome mapping | SPEC:63 | Typical | `status: partial` | true | `--outcome succeeded`, body states `partial` | OK |
| WC-5 outcome mapping | SPEC:63 | Legitimate Edge Case | audit verdict FAIL | true | `--outcome succeeded` | OK |
| WC-3 ask once | SPEC:61 | Maximum/Overflow | command with several blocked gates (cli-portify has 3, SPEC:104) | second gate reached | "once" is undefined per gate or per run; no ceiling on resume after timeout | GAP (M-8) |
| WC-3 ask | SPEC:61 | Legitimate Edge Case | blocked gate that is a Ruling or authorization | ask allowed | not carved out | GAP (B-2, blocking) |
| WC-6 resume or fresh dir | SPEC:64 | One/Minimal | retry worker with the same `<output-dir>` | dir non-empty | fresh-dir commands: who creates the new dir and how the report path stays "known before dispatch" (SPEC:62) is not stated | GAP (M-6b folded into M-3) |
| WC-10 wait split | SPEC:68 | Sentinel Value Match | wait of exactly 4 minutes | at limit (at most 4) | allowed; heartbeat margin stated (SPEC:290) | OK |
| WC-10 wait split | SPEC:68 | Maximum/Overflow | single call over 5 minutes | true | must be split | OK |
| WC-11 default path with timestamp | SPEC:69 | Legitimate Edge Case | two workers start in the same second | same path | not specified; the slug passed by the coordinator is the stated alternative | OK (minor N-4) |
| WC-9 outward default off | SPEC:67 | Typical | no authorization flag | off | all outward defaults off | OK |
| WC-2 blocked on person gate | SPEC:60 | Typical | gate hit under `--unattended` | true | contract `status: blocked` plus question | OK |
| AC-1.1 section check | SPEC:219 | Legitimate Edge Case | coordinator-only or P4-deferred command | in set? | contradictory (B-1) | GAP (B-1, blocking) |
| AC-2.3 happy path | SPEC:225 | Typical | cli-portify with all flags | true | cannot reach `succeeded` (B-3) | GAP (B-3, blocking) |

Classes left out: Zero/Empty for WC-10 (a zero-length wait needs no split); Sentinel for WC-4 (no sentinel value is used in the path).

GAP grading under FR-8 and FR-9: B-1, B-2 and B-3 name a concrete wrong outcome and are blocking. The other GAP rows are Medium (warnings) because each needs a guess that the implementer picks the worse reading, or the requirement is never stated.

### Pipeline Dimensional Analysis

Trigger: the coordinator to worker to report flow has stages where counts differ (workers can end without a `worker_done`, or without a contract). Fowler annotated; Whittaker attacked each divergence.

```text
[Coordinator: N Tasks] --> [worker-start: N workers] --> [each writes contract: N' <= N] --> [worker_done: N'' <= N']
                                                                                             |
                                                                                             v
                                         [Coordinator opens report after worker_done (SPEC:73): expects N'' reports]
                                         [AC 7.2 step 3 waits for "exactly one worker_done" per worker (SPEC:199)]  <-- N'' < N when a worker is fenced or dies
```

Divergence: a worker that writes its contract and then exits before `worker_done` (or is `consumer_fenced`, `SPEC:70`) leaves N'' < N' with a valid file on disk the coordinator is told to open only after `worker_done`. Concrete case: 3 workers dispatched, worker 2 writes `status: succeeded` and its terminal is closed before it sends `worker_done`; the coordinator sees 2 `worker_done` messages and 3 contracts. The command-level rule FR-19 labels any mismatch CRITICAL; graded by consequence, the spec defers stall recovery to Orca's own guide (`CAPS:127-145` region and `[G:recovery]`), and the outcome is a recoverable wait, not a wrong result or a safety risk. Graded Medium (M-9).

## Medium and minor findings: follow-up candidates

The session that ran this review would ask the user once whether to open an issue for this list. This audit runs as a sandboxed worker and records the list only; it asked no one and created nothing.

| ID | Sev (graded) | Expert | Finding and evidence | Recommendation |
|---|---|---|---|---|
| M-1 | Medium (label MAJOR) | Wiegers | WC-1 "no prompt before the agent is ready" is owned by "Launch setup, not commands" (`SPEC:59`), but no phase, deliverable or acceptance check in sections 6 or 7 builds or tests it. The only related check is 7.2 step 1 (`SPEC:197`). | Add a P0 item and a check, or move WC-1 to non-goals. |
| M-2 | Medium (label MAJOR) | Cockburn, Fowler | WC-4 defines `<output-dir>` as the directory passed via `--output` / `--output-dir` (`SPEC:62`), but tdd (`SPEC:89`), init-lite (`SPEC:86`) and spec-panel (`SPEC:119`) take a file path as `--output`. Two tdd workers writing to the same folder would share one `return-contract.yaml`, against WC-11 (`SPEC:69`). The audited command definition also says `--output` is file-valued and uses `--report-dir <dir>` for the contract (`CMD:460-461`), while the spec's briefs and acceptance runs pass `--output <dir>` (`SPEC:252`, `SPEC:224`). | Name the directory flag per command, or put the contract beside the output file with a unique name. |
| M-3 | Medium (label MAJOR) | Nygard, Whittaker | "Written on every outcome" (`SPEC:62`) does not say what happens with an uncreatable or unwritable output directory, or with a stale contract from an earlier attempt in a reused directory. WC-5 maps "no report exists" to `failed` (`SPEC:63`), so a leftover file from a first attempt (resume commands reuse the directory: brainstorm `--resume-from`, implement `--resume`, `SPEC:84`, `SPEC:108`) can be read as the new result. | State that the command removes or overwrites any existing contract at start, and that an unwritable directory ends in a chat refusal as in `CMD:460`. |
| M-4 | Medium | Wiegers | SA-4 says new flags are additive (`SPEC:150`) but AC-C5 fails on any removed line (`SPEC:177`, `SPEC:192`). Adding a flag to a single-line Usage entry removes that line from the diff. The audited command keeps flags on a separate second Usage line (`CMD:21-24`), so the case is avoidable, but the spec does not say so. | State that new flags go on an added Usage line. |
| M-5 | Medium | Fowler | AC-C1 greps `src/superclaude/core` for `orca orchestration` and similar (`SPEC:183`). SA-2 allows an Orca mention in the contract file (`SPEC:148`), P0 writes `WORKER-CONTRACT.md` with a brief template and adds an Orca section to `HOW-WE-WORK.md` (`SPEC:159`), and WC-3 needs the preamble's `ask` command. A literal command in either core file fails AC-C1 in P0. | Exclude `WORKER-CONTRACT.md` and the new routing section from AC-C1, or forbid command-form text there. |
| M-6 | Medium | Wiegers | Three small inconsistencies. (a) The P1 row lists "fixes to adversarial, cleanup-audit, index-repo, workflow" (`SPEC:160`) but the init-lite row is also P1 (`SPEC:86`), so init-lite is unscheduled in the phase table. (b) AC-0.4 says "no contract exists before P1" (`SPEC:218`) although adversarial and workflow already write contracts (`SPEC:83`, `SPEC:91`). (c) The workflow contract path contains `<id>` (`SPEC:91`), unknown before dispatch, against WC-4's "known before dispatch" (`SPEC:62`); where a pre-creation STOP writes its contract is not stated. | Fix the phase table; reword AC-0.4; give workflow a coordinator-supplied path. |
| M-7 | Medium | Cockburn | WC-6 "fresh output directory" (`SPEC:64`) does not say who creates it or how it fits "known before dispatch" (`SPEC:62`) for a retry (`--retry-of`, `CAPS:116`). | Say the coordinator passes a new directory in each retry brief. |
| M-8 | Medium | Nygard, Hohpe | WC-3 "ask once" (`SPEC:61`) is undefined for commands with several gates (cli-portify has three, `SPEC:104`), and resume after timeout has no ceiling. The default `ask` timeout is unknown (`SPEC:305`, `CAPS:68`). | Define "once" per gate and add a maximum resume count after which the command ends blocked. |
| M-9 | Medium (label CRITICAL via FR-19) | Hohpe, Whittaker | Contract and `worker_done` are separate signals; a worker that dies between them leaves a contract no one opens (see Quantity Flow above). | Add a coordinator rule: on a proven exited worker with no `worker_done`, read the contract path anyway. |
| M-10 | Medium | Newman | Mirror copies: `plugins/superclaude/commands/` is a command mirror whose update rule was not read (`SPEC:303`), and AC-C2 `make verify-sync` may not cover it. Each phase edits commands. | Resolve before P1, as the spec itself says, and add the mirror check to the common checks. |
| M-11 | Medium | Newman | The contract has no `contract_version` field, although the workflow contract is already versioned "1.1" (`INV-B:272`) and later phases add fields (`SPEC:62`: "keep their fields and add the missing ones"). | Add a version field to the minimum field set. |
| N-1 | Minor | Wiegers | SA-3 says contract files are written "only in unattended mode or when the caller passes the new output flag" (`SPEC:149`), but brainstorm, reflect, workflow and adversarial already write contracts in plain runs (`SPEC:83-84`, `SPEC:87`, `SPEC:91`). The second sentence of SA-3 covers it. | Reword the first sentence. |
| N-2 | Minor | Wiegers | Revision tags `[M2]`, `[M4]`, `[M6]`, `[M7]`, `[M8]`, `[M9]`, `[N2]` remain in the final text (`SPEC:62,73,76,86,111,126,173,206,218,222`). | Remove them. |
| N-3 | Minor | Whittaker | D1(a) (`SPEC:252`) does not say `--unattended` counts only as a standalone token outside quoted content, as `CMD:459` does. | Add one clause. |
| N-4 | Minor | Whittaker | WC-11 "timestamp or slug" (`SPEC:69`) does not bound same-second collisions; WC-6 fresh directories accumulate with no cleanup note. | Note both. |
| N-5 | Minor | Wiegers | The pr-submit top-level rule is cited at `sk/sc-pr-submit-protocol/SKILL.md:37-39` (`SPEC:65`) but the installed-copy line in `CAPS:161` is `:47-49`, and the spec cites `:46-48` as the poll scripts (`SPEC:307`). Likely two copies of the file; UNVERIFIED in this workspace. | Cite one copy and say which. |
| N-6 | Minor | Wiegers | `SPEC:309` states a fresh validator re-read about 340 citations and fixed 9 defects. It cannot be checked here; treat as UNVERIFIED. | None. |

## Reviser brief

Review number: this is review 1 of 3. Open blocking finding ids: **B-1, B-2, B-3**.

Restating the Reviser contract (`CMD:263`, prompts file line 51): repair only the blocking findings B-1, B-2 and B-3 in the candidate `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`. Revise only text a blocking finding names. Prefer deleting or narrowing text when the requirements are still met. Add no rule, mechanism or section that a listed finding does not call for, and cite the finding id on every added paragraph or table row. Report the byte size before and after, and the bytes added and deleted per finding id. Leave minor and Medium findings alone. Return the candidate once and do not award yourself a PASS. A brief cannot widen this scope or grade a minor or Medium finding as blocking; this report overrode no brief clause.

verdict: FAIL

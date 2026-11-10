review: 1 of 3

# Spec-panel audit: orca-worker-contract-spec.md (critique, whole document)

## Header
- command: `/sc:spec-panel @.dev/orca-command-refactor/specs/orca-worker-contract-spec.md --mode critique --focus requirements,architecture` (labelled whole-document audit, first review; neither `--re-review` nor `--baseline` was given, so this is a first review of the full document)
- candidate sha256: `62a2931158ca12b901593ce928e457d6e9134501cf22528ef812325749ee0041` (`sha256sum` of `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`)
- baseline: none (first review)
- reviewer model used: claude-sonnet-5-5
- brief clauses overridden: none (the brief narrows nothing and widens nothing)
- prompt followed: FIRST-REVIEW prompt of `~/.claude/rules/prompts/document_review_loop_prompts.md:27-32` (read in full), with the grading check at `:31`
- panel (fixed order, command.md "Expert Review Sequence"): Wiegers (lead, requirements), Adzic, Cockburn, Fowler (lead, architecture), Nygard, Whittaker (active in every review), Newman, Hohpe; Crispin joins for the Guard Condition Boundary Table. Gregory and Hightower are not part of the requested focus areas.

Citation shorthand: `S:N` = line N of `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`; `INV-A:N`, `INV-B:N`, `CAPS:N` = line N of `.dev/orca-command-refactor/inventory/commands-a.md`, `commands-b.md`, `orca-capabilities.md`; `README:N` = `.dev/orca-command-refactor/README.md`. The inventories and the README are the only evidence checkable in this sandbox. Any other citation in the spec (`CLAUDE.md:*`, `HOW-WE-WORK.md:*`, `EVIDENCE.md:*`, `.dev/codegraph-migration/*`, `install_core.py:*`, `pyproject.toml:38`, `Makefile:68-74`, and every `cmd/` or `sk/` line not quoted in an inventory) is UNVERIFIED here. Findings below that rest only on inventory lines say so.

Coverage: all of sections 1 to 9, the Decisions table and the UNVERIFIED list. Cross-checked: the 43 / 10 / 27 / 6 totals and the phase assignment counts, every section-3 and section-4 evidence pointer against the inventory line it names, and the capability citations in sections 1 and 2 against `CAPS`. Not covered: any claim about files absent from the sandbox (see the UNVERIFIED list in the follow-up section).

## Grading summary
Blocking: 2 (B1, B2). Medium: 13 (M1 to M13) and minor: 6 (N1 to N6), all under follow-up candidates. Each blocking finding passed the grading check "an implementer who follows the stated text as written builds X, and X is wrong because Y".

=== REQUIREMENTS ANALYSIS ===

### B1 (CRITICAL, blocking) Phase 1 ships `--unattended` on 25 commands whose gates and outward defaults are converted only in later phases
- Experts: Whittaker (Sequence Attack), Wiegers, Nygard. Priority High.
- Attack: I can break this specification by **Sequence Attack**. The invariant at **WC-2 and WC-9 (`S:60`, `S:67`)** fails when **Phase 1 is shipped and Phase 2 is not yet shipped**. WC-2 says "Under `--unattended` the command never calls `AskUserQuestion`, never ends its turn on a chat question"; WC-9 says that under `--unattended` every default that pushes, posts to GitHub, installs or calls a paid run "is off". Both are stated without a phase qualifier.
- Stated text that conflicts: Phase 1 adds "the `--unattended` flag accepted by every command in sections 3.1 and 3.2 except load (M3) (a no-op where a command has no gate)" and the contract (`S:159`); AC-1.1 asserts the `## Unattended mode` section for all of them (`S:195`). Gate conversion for those commands belongs to Phase 2, 3 or 4 (`S:160-162`; per-command phase column `S:99-125`). The spec also says each phase is "independently useful" (`S:154`) and that a later phase starts only when the earlier one passes (`S:154`), so the state "P1 shipped, P2 not" is a defined state.
- State trace (counts from the spec): flag accepted and section asserted for 36 commands (10 ready in `S:81-92` plus 27 changed in `S:99-125`, minus load, `S:159`, `S:195`). Live checks in AC-1.2 cover the P1 commands only: 8 (analyze, build, business-panel, design, document, explain, index, test) plus the 3 fixed ready commands (adversarial, cleanup-audit, index-repo), `S:159`, `S:196`, so 11. The remaining 25 get the flag with no live check and, for 22 of them, with the gate or outward default still in place (P2: 15, P3: 4, P4: 3 per `S:160-162`; the other 3 are brainstorm, init-lite, workflow which have no gate).
- Concrete wrong outcome: after Phase 1, a coordinator writes `/sc:auggie-review <PR> --unattended` into a worker brief, as `S:73` tells it to. The command accepts the flag, AC-1.1 passes (the section exists), and the command still posts a PR review and inline comments with "No confirmation prompt" and still ends on the remediation offer (`INV-A:38`; spec row `S:100`: the `--no-post-pr --no-remediation-offer` implication is Phase 2). That is an outward GitHub action under a flag WC-9 says switches such actions off, and a stalled worker under a flag WC-2 says removes every wait. The same holds after Phase 1 for cleanup and improve approval prompts (`S:103`, `S:110`), cli-eval's suite menu (`S:104`) and task's tier prompt (`S:121`).
- Why blocking: two stated texts contradict (WC-2/WC-9 unconditional versus the P1/P2 split) and an outward-action boundary is crossed (`INV-A:38`).
- Fix direction (repair only, no new mechanism): either make P1 add the flag only to the commands whose gate conversion is in the same phase, or state that `--unattended` on a command is not usable until that command's own phase has passed and make the P0 brief template list the commands that are usable.

### B2 (CRITICAL, blocking) cli-portify cannot pass its own happy-path acceptance check
- Experts: Wiegers (testability), Adzic (examples), Whittaker (Zero/Empty Attack). Priority High.
- Attack: I can break this specification by **Zero/Empty Attack** on the approval input. The invariant at **cli-portify row (`S:105`) with WC-2 (`S:60`) and AC-2.3 (`S:201`)** fails when **the coordinator supplies every flag the row lists**.
- Stated text: the row resolves "each of the three approval gates ... as blocked with the artifact to review named in the contract", and adds only a `--resume <contract>` flag that "uses the existing `resume_phase`/`resume_substep` fields" (`S:105`). WC-2 allows three resolutions per gate: a default, a caller-supplied flag, or blocked (`S:60`); the row picks only the third for all three gates. AC-2.3 requires, for every P2 command, "Happy-path run ... with every required flag in the brief" that ends `--outcome succeeded` (`S:201`). WC-3's route (ask the coordinator, then "re-invoke or resume the command with the answer as a flag", `S:61`) names no flag by which an approval can be passed.
- State trace: run 1 reaches the first approval gate (after Phases 1 and 2, `INV-A:45`) and ends `status: blocked`, `--outcome failed` (`S:63`). Run 2, `--resume <contract>`, restarts at the saved phase and meets the same gate, because no input carries the approval. Any number of resumes ends the same way. The three gates sit at `INV-A:45` (before Phase 3, before delivery).
- Concrete wrong outcome: an implementer follows the row exactly and builds a command that can never end `succeeded` under `--unattended`; AC-2.3 cannot pass for it; Phase 2 cannot be declared done (`S:154`).
- Why blocking: a stated text that an acceptance criterion cannot pass (FIRST-REVIEW grading check, `document_review_loop_prompts.md:31`).
- Fix direction: give the row a caller-supplied approval input for the three gates (WC-2 option b), or exclude cli-portify from AC-2.3 and say that it is a human-in-the-loop command.

=== ARCHITECTURE ANALYSIS ===

Architecture verdict (Fowler, Newman, Hohpe, Nygard): the central decision is sound and well evidenced. Orca coordinates and commands stay units of work (`S:16`); no Orca call in a command (`S:213`, SA-2 `S:147`); the rejected alternative is argued from the depth fence (`CAPS:97-101`), standalone use (`CAPS:147-149`), completion ownership (`CAPS:76`, `CAPS:150`) and the executable name (`CAPS:145`); the evidence-strength limits are stated honestly (`S:41-45`). The shared-contract-file design (one document, per-command section, `S:52`) keeps the write-once rule. The interface between the coordinator and a worker is one file plus one flag, which is a narrow, stable seam (Newman). The report-file seam has the following gaps, none blocking on its own: M2, M3, M13 below.

Fowler (interface and boundaries): the six coordinator-only commands (`S:130-137`) track the inventories (`INV-A:36,49,50`; `INV-B:32,42,44`). Totals reconcile: 43 = 10 + 27 + 6 (`S:76`; `INV-A:73`; `INV-B:278`). Nygard (failure modes): see M4 (liveness), M3 (retry), M13 (blocked-then-failed). Hohpe (message flow): the lifecycle messages are correctly confined to the top-level session (`S:65`); the ask / reply / check loop is consistent with `CAPS:58-67`.

### Pipeline Dimensional Analysis (triggered: the command set passes through a multi-stage classification and rollout with count changes)
Quantity Flow Diagram (counts from `S:76`, `S:81-125`, `S:159-162`, `S:195-196`):

```text
[Source: 43 commands in src/superclaude/commands/ (INV-A:3 + INV-B:3 = 21 + 22)]
   --> [Stage 1: split by worker suitability] --> 37 worker-capable, 6 coordinator-only
        |                                             (coordinator-only: no --unattended, S:128)
        v
   [Stage 2: split by readiness] --> 10 ready (S:81-92) | 27 need a change (S:99-125)
        |
        v
   [Stage 3: P1 "--unattended accepted" (S:159)]  --> 36 commands (37 minus load)    <-- consumer AC-1.1 expects 36 (S:195)
        |
        v
   [Stage 4: P1 live check AC-1.2 (S:196)]        --> 11 commands                     <-- consumer expects 11
                                                      |
                                                      +-- 25 accept the flag with no live check
                                                          22 of them still have the gate / outward default until P2 (15), P3 (4), P4 (3)   <-- MISMATCH (see B1)
```

Consistency check: the totals reconcile at every stage (43 = 10 + 27 + 6; 36 = 11 + 25; 27 changed = 9 P1 + 11 P2 rows + 4 P3 + 3 P4, plus the 4 fixed-ready commands in P2 giving 15 P2; the per-row phase column at `S:99-125` sums to P1 9, P2 11, P3 4, P4 3). The only dimensional mismatch is the 36-versus-11 divergence in Stages 3 and 4, reported as B1.

## Whittaker adversarial analysis (five attack methodologies against the stated invariants)
Invariants attacked: WC-2 (no wait on a person), WC-4 (one report on every outcome), WC-5 (one outcome), WC-6 (retry safe), WC-9 (no outward action), WC-10 (heartbeat).

| # | Methodology | Invariant | Result |
|---|---|---|---|
| W1 | Zero/Empty | WC-4 `<output-dir>`: the coordinator passes no directory (or the command has none) | Open: M2 |
| W2 | Zero/Empty | WC-2 option (b): a gate with no caller flag defined (cli-portify, post-release pre-tag) | Open: B2, M5 |
| W3 | Divergence | WC-5: contract `status` is `partial` versus `failed`, audit verdict FAIL versus `succeeded` | Holds: the mapping is explicit (`S:63`, Decisions `S:263`) |
| W4 | Divergence | WC-3 (optional ask) versus AC-2.2 (blocked ends `failed`) | Open: M12 |
| W5 | Sentinel Collision | contract `status: blocked` versus Orca Task status `blocked` (`CAPS:89`) | Open: M13 (a `blocked` contract settles the Task as `failed`, `S:63`, and failed Tasks keep dependents blocked, `CAPS:90`) |
| W6 | Sentinel Collision | `return-contract.yaml` filename shared by 4 commands that already write one with their own fields (`S:62`, Decisions `S:261`) | Holds: "keep their fields and add the missing ones" (`S:62`) |
| W7 | Sequence | phases P1 before P2 | Open: B1 |
| W8 | Sequence | `--resume` ordering for roadmap and a pre-existing `.session-memory.md` | Open: M6 |
| W9 | Accumulation | three failed worker-starts trip the circuit breaker (`CAPS:80`, `CAPS:116`) | Holds: a worker's own `failed` report does not count (`CAPS:80`); spec relies on it at Decisions `S:263` |
| W10 | Accumulation | repeated retries into one output directory | Open: M3 |

## Guard Condition Boundary Table (hard gate; the spec contains threshold and conditional guards, so the table is produced)
Responsibility: Nygard (construction), Crispin (completeness), Whittaker (attack). Classes not applicable to a guard are omitted with a one-line reason under the table.

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|-------|----------|-----------------|----------------|--------------|--------------------|--------|
| `unattended_active` | WC-2 `S:60` | Zero/Empty | `--unattended` absent | false | SA-1: every prompt, default and output path as today (`S:146`) | OK |
| `unattended_active` | WC-2 `S:60` | Typical | flag present, command in its phase | true | gates resolve per row (`S:99-125`) | OK |
| `unattended_active` | WC-2/WC-9 `S:60`, `S:67` | Legitimate Edge Case | flag present, command's phase not yet shipped | true | not specified; P1 accepts the flag before P2-P4 convert gates (`S:159-162`) | GAP (B1) |
| `output_dir_known` | WC-4 `S:62` | Zero/Empty | no `--output` / `--output-dir` passed under `--unattended` | n/a | not specified; text says the report is "written on every outcome, including stops before any other output exists" | GAP (M2) |
| `output_dir_known` | WC-4 `S:62` | Legitimate Edge Case | `--output` is a file path (tdd `S:90`, init-lite `S:87`, spec-panel `S:120`) | n/a | not specified; WC-4 says `<output-dir>/return-contract.yaml` | GAP (M2) |
| `output_dir_known` | WC-4 `S:62` | Legitimate Edge Case | directory chosen by the command (implement ledger `S:109`, pr-submit `S:114`, cli-portify `S:105`) | n/a | exceptions list names 4 commands only (`S:62`); these 3 are not in it | GAP (M2) |
| `contract_status` | WC-5 `S:63` | Typical | `succeeded`, `partial`, `failed`, `blocked` | per value | mapped to `--outcome` (`S:63`) | OK |
| `contract_status` | WC-5 `S:63` | Sentinel Value Match | file present but `status` missing or not one of the four | n/a | "no report exists" covers a missing file only | GAP (minor, N3) |
| `report_exists` | WC-5 `S:63` | Zero/Empty | no contract written (workflow stop before the package exists, `S:62`) | false | `--outcome failed`, no `--report-path` | OK |
| `heartbeat_wait_limit` | WC-10 `S:68` | Typical | one call of 6 minutes | true | split into waits of at most 4 minutes | OK |
| `heartbeat_wait_limit` | WC-10 `S:68` | Legitimate Edge Case | one call of 4.5 minutes; or a foreground Agent-tool call of 10 minutes | false / true | the 4.5-minute case is neither required to split nor within the 4-minute target; the Agent-tool case cannot be split by the command | GAP (M4) |
| `nesting_depth` | R1 `S:33`; D5 `S:249-253` | Maximum/Overflow | worker calls `worker-start` at depth 1 | refused | `nested_worker_depth_exceeded` (`CAPS:99`); WC-8 forbids the call (`S:66`) | OK |
| `confidence_below_070` | task row `S:121` | One/Minimal | confidence exactly 0.70 | false | "below 0.70" resolves as blocked, 0.70 proceeds; consistent with the command's `< 0.70` (`INV-B:199`) | OK |
| `monitor_level_ok` | pr-submit row `S:114` | Legitimate Edge Case | `--monitor 0` or `--monitor 2` under `--unattended` | n/a | only `--monitor 1` is refused; levels 0 and 2 not described (`INV-B:89` describes levels 1 and 3 only) | GAP (M11, Medium) |
| `retry_dir_fresh` | WC-6 `S:64` | Legitimate Edge Case | retry worker reuses the Task spec with the same `--output` | n/a | "fresh output directory" required, but the directory is supplied by the coordinator (`S:62`, `S:73`) | GAP (M3) |
| `phase_gate` | `S:154` | Sentinel Value Match | AC-C3 baseline already has failures | n/a | "no test that passed in the baseline fails" (`S:174`) | OK |

Classes left out: Maximum/Overflow for `unattended_active`, `output_dir_known`, `contract_status` and `report_exists` (booleans or enumerations, cannot overflow); One/Minimal for the same guards (no meaningful minimal value); Zero/Empty for `heartbeat_wait_limit` (a zero-length wait has no guard effect); Sentinel Value Match for `nesting_depth` and `confidence_below_070` (no reserved value).

Gate result (FR-8, FR-9, FR-10): the table is complete. GAP rows were graded by consequence: the `unattended_active` GAP is B1 (blocking); the `output_dir_known` and `retry_dir_fresh` GAPs name no wrong outcome that follows from the stated text without a guess about the implementer's choice, so they are Medium (M2, M3); `heartbeat_wait_limit` is Medium (M4); `monitor_level_ok` is Medium (M11); `contract_status` is minor (N3). No row has a blank Specified Behavior (FR-9) except where the cell says "not specified", which is the GAP itself and is graded above.

## Panel commentary by expert (critique mode)
- **Wiegers (requirements):** the requirement table is the strongest part: each WC row names owner and evidence (`S:57-70`). Two requirements are not testable as written: WC-4's "written on every outcome" has no location when no directory is given (M2), and WC-10's "heartbeat every 5 minutes" has no check except in AC-4.3, which covers pr-submit alone (M4). B1 and B2 are the traceability breaks between requirement and acceptance check.
- **Adzic (examples):** D1 gives a concrete example line (`S:228`); the per-gate AC-2.2 examples are good (`S:200`). Missing example: what the `--unattended` brief for cli-portify looks like when it succeeds (B2).
- **Cockburn (goals and actors):** the primary actor is the coordinator; its obligations are in section 2.3 (`S:72-73`). That list omits two duties the other requirements rely on: pass a fresh output directory per retry (M3) and pass the authorization flags WC-9 names (M5).
- **Fowler (architecture):** boundaries are clean. One smell: three different mechanisms decide where the report lives (a shared rule at `S:62`, four listed exceptions at `S:62`, and "beside the ledger" or "beside the log" in rows at `S:109`, `S:114`); consolidating them into one table would remove M2.
- **Nygard (reliability):** the failure-path design (blocked, failed, `consumer_fenced`) is thorough; gaps are M3, M4, M13.
- **Whittaker (adversarial):** see the table above; two open attacks reach blocking (W2 to B2, W7 to B1).
- **Newman (API evolution):** one shared contract file with a per-command section keeps the interface versionable; no version field is specified in the contract (`S:62`), which is acceptable for a 4-value status set but noted as N5.
- **Hohpe (integration and data flow):** ask, reply and check are used as Orca intends (`CAPS:58-67`); the free-text `blocked_question` field is the only structured carrier of the question (`S:62`), fine.
- **Crispin (testing):** 7.2 is a strong reusable procedure (`S:178-186`); gaps are the AC-0.4 comparison for troubleshoot (M10), AC-C5 (M7), and the missing negative cases noted in M4.

## Follow-up candidates (Medium and minor; never trigger a revision; not in the Reviser brief)
Whether to open an issue for these was not asked: this run is a single audit worker with a fixed final reply and no user turn. No issue was created.

### Medium (warnings)
- **M1. SA-2 versus AC-C1.** SA-2 permits one Orca mention, "as an example of a caller's question channel inside the contract file" (`S:147`), and Phase 0 puts the contract in `src/superclaude/core/` and adds an Orca section to `HOW-WE-WORK.md` in the same directory (`S:158`). AC-C1 greps `src/superclaude/core` for `orca(-ide) (orchestration|worktree|terminal|agent)` and requires no output, excluding only `skills/ccsession-tag/` (`S:172`). An example written as `orca orchestration ask` fails AC-C1 at Phase 0. Medium because the implementer can choose different words (needs a guess); add the contract file to the exclusion or narrow SA-2.
- **M2. Contract location is under-specified.** WC-4 fixes `<output-dir>/return-contract.yaml` from a directory "the coordinator passed" (`S:62`) and says the file is written on every outcome. Open cases: no directory passed under `--unattended`; commands whose `--output` is a file (tdd `S:90`, init-lite `S:87`, spec-panel `S:120`); commands with a derived directory that are not in the four-item exception list (implement ledger `.dev/implement/<slug>/` `INV-A:51`, pr-submit `.dev/pr-monitor/pr-<N>-<ts>/` `INV-B:92`, cli-portify `INV-A:45`, troubleshoot `.dev/troubleshoot/<slug>-<timestamp>/` `INV-B:242`). Section 2.3 promises the path is "known before dispatch" (`S:73`). Medium: a requirement the document never states.
- **M3. WC-6 versus WC-4 on retry.** WC-6 asks the command to write "each run into a fresh output directory" (`S:64`) while WC-4 and section 2.3 have the coordinator supply the directory (`S:62`, `S:73`). Orca's retry re-dispatches a known Task (`CAPS:116`); whether it reuses the same brief is the implementer's or coordinator's choice. 20 rows rely on "fresh dir" (for example `S:99`, `S:101`, `S:106`). Add to section 2.3: "pass a new output directory on each retry".
- **M4. WC-10 covers poll waits and evals, not Agent-tool fan-out.** The heartbeat cadence comes from the dispatch preamble (`CAPS:130`) and Orca's use of heartbeat age is UNVERIFIED (`CAPS:182`). A foreground Agent-tool call (adversarial, tdd, cleanup-audit waves, `INV-A:35,42`; `INV-B:47`) can block the top-level session beyond 5 minutes and cannot be split by the command. AC-4.3 checks heartbeat spacing for pr-submit only (`S:210`); the P0 smoke runs (`S:194`) do not. Also the 4 to 5 minute band is neither required to split nor inside the 4-minute target (`S:68`).
- **M5. WC-9 names a flag that several commands do not have.** WC-9 turns an outward action on "only through the command's own explicit flag written in the brief" (`S:67`). For post-release the inventory shows a conversational confirmation, not a flag ("unless the user pre-authorized them this session", `INV-B:79`); the row asks for "an explicit pre-tag choice" without naming one (`S:113`). Task's `commit` / `push` row says "refused unless authorized" without a flag (`S:121`). D4 option (a) is thereby built into WC-9 before the user decides (`S:244-247`), while `S:154` says Phases 1-3 need no user decision and auggie-review and task (P2) depend on D4 (`S:244`).
- **M6. Roadmap unattended default changes the existing default.** The inventory shows the prompt as "Resume? [Y/n]" (`INV-B:149`), so the interactive default is resume. The row makes `--unattended` resume only on an explicit flag (`S:118`), and AC-3.2 expects a fresh start in a directory that holds a prior `.session-memory.md` (`S:205`), which overwrites the prior session's artifacts in that directory. The loss is not stated as accepted. Medium: the harm depends on the coordinator reusing the directory.
- **M7. AC-C5 versus new flags.** SA-4 says edits are additive: "a new `## Unattended mode` section and new flags" (`S:149`). AC-C5 requires `git diff -U0 ... | grep -E '^-[^-]'` to print nothing (`S:176`). Adding a flag to an existing Usage line is a changed line and prints a `-` line. Say where flags are documented (the new section only, or a new Usage line).
- **M8. Tasklist remedy departs from the inventory without a Decisions entry.** The inventory recommends dropping `--remediate` at Stage 10.5 and running the reflect fan-out at the worker's top level (`INV-B:215`); the spec instead passes `--unattended` to each reflect and relies on the nesting limit (`S:122`, citing `INV-A:14`). The inventory itself marks nested spawning UNVERIFIED (`INV-B:210`, `INV-B:314`). Decisions says no verdict was contradicted (`S:268`); the remedy differs and the reason is not recorded.
- **M9. P1 is described as "commands with no gate", but three P1 rows carry a gate refusal.** business-panel refuses `--mode socratic`, explain refuses `--format interactive`, test refuses `--watch` (`S:102`, `S:108`, `S:123`; phase `S:159` header "no gate"; P2 owns "gate conversion", `S:160`). Move the refusals to P2 or relabel P1.
- **M10. AC-0.4 steps 3 and 4 for troubleshoot.** The step compares `--outcome` with "that file's own status" (`S:194`). Troubleshoot's report is `REPORT.md` with `report_path`; a `return-contract.yaml` exists only with `--caller task-unified` (`INV-B:242`). Whether REPORT.md carries a status field to compare is not shown.
- **M11. pr-submit `--monitor` levels.** Only `--monitor 1` is refused (`S:114`); the inventory describes levels 1 and 3 (`INV-B:89`). Level 0 and level 2 behaviour under `--unattended` is not stated. Low impact while D3 recommends no worker use (`S:240-242`).
- **M12. WC-3 versus AC-2.2.** WC-3 lets the worker ask the coordinator instead of ending blocked (`S:61`); AC-2.2 requires the blocked case to end `--outcome failed` with `status: blocked` (`S:200`). A worker that follows WC-3 fails the check. State that tests forbid `ask`, or that `ask` is allowed only after the contract is written.
- **M13. Blocked outcome and Task state.** A blocked contract maps to `--outcome failed` (`S:63`); a failed Task keeps dependents blocked until a `--retry-of` replacement completes (`CAPS:90`); the spec does not say how the coordinator supplies the missing answer on retry (a new brief with the same Task spec?). The contract status `blocked` also shares its name with the Orca Task status `blocked` (`CAPS:89`).

### Minor (notes)
- N1. UNVERIFIED in this sandbox, rely on the spec's own claim only: `CLAUDE.md` lines 16, 50, 65, 72-83, 157, 334, 408; `HOW-WE-WORK.md` lines 22, 171, 249, 254, and the `grep -ci orca` count of 0 (`S:25`); `EVIDENCE.md` lines 39, 45, 56; `.dev/codegraph-migration/orchestration/README.md` lines 31, 33, 42 and the `return-contract.yaml:10` line; `install_core.py:4,13-24,33`; `pyproject.toml:38`; `Makefile:68-74`; the `grep -rlni orca` result (`S:25`). The inventory lines that quote some of these (for example `EVIDENCE.md:39,45,56` at `CAPS:49`, `return-contract.yaml:10` at `INV-A:13`) agree with the spec.
- N2. Citation check result for what is checkable: every `INV-A:N`, `INV-B:N` and `CAPS:N` pointer I opened in sections 1 to 4 and in the Decisions table matched its stated content (for example `CAPS:92`, `CAPS:155`, `CAPS:161`, `INV-A:106`, `INV-B:320`, `INV-B:323`, `INV-A:13`).
- N3. WC-5 treats a missing report as `failed`; a present file with a missing or unknown `status` is not covered (`S:63`; AC step 4 only checks it after the fact, `S:183`).
- N4. Phase 0 adds `tests/skills/test_worker_contract.py` (`S:158`) but AC-0.x never runs it; its content is first checked in AC-1.1 (`S:195`).
- N5. The contract has no version field (`S:62`); acceptable for now.
- N6. The spec's own UNVERIFIED list item 14 records a prior independent citation check of about 340 citations (`S:285`); this audit could confirm only the inventory-backed subset (N2).

## Reviser brief
Blocking finding ids: B1, B2. The reviser reads this report, not the command, so the rules of the command's Review Loop bullet 6 are restated here:
- Revise only text a blocking finding names (B1: `S:159`, `S:195` and the P1/P2 split they depend on; B2: the cli-portify row `S:105` and AC-2.3 `S:201`).
- Add no rule, mechanism or section that no blocking finding calls for; each added paragraph or table cites its finding id.
- Prefer deleting or narrowing to adding.
- Report the byte size of the candidate before and after, and the bytes added and deleted per finding id.
- Leave the Medium and minor findings (M1 to M13, N1 to N6) alone.
- Return the candidate once and do not award yourself a PASS.

verdict: FAIL

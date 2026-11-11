review: 1 of 3

# Spec panel audit: orca-worker-contract-spec.md (labelled whole-document audit, first review)

## Header

| Field | Value |
|---|---|
| Command | `/sc:spec-panel @.dev/orca-command-refactor/specs/orca-worker-contract-spec.md --mode critique --focus requirements,architecture` |
| Review prompt followed | FIRST-REVIEW prompt, `~/.claude/rules/prompts/document_review_loop_prompts.md` (read in full) |
| Candidate | `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`, 285 lines |
| Candidate SHA-256 | `f42ebd1cb0922207da16c10e49e26f992ea80bee8c020e73ba1dacefbcfd5f95` |
| Baseline / prior | none given (no `--re-review`, no `--baseline`): first review of the full document |
| Reviewer model actually used | `claude-sonnet-5-5` (Sonnet 5.5) |
| Review date | 2026-11-10 |
| Format | critique mode, findings grouped by analysis bucket; markdown (no `--format` given) |
| Unattended | not passed; no `return-contract.yaml` written |

Citation shorthand. `S:N` = line N of the candidate. `INV-A:N`, `INV-B:N`, `CAPS:N` = line N of `.dev/orca-command-refactor/inventory/commands-a.md`, `commands-b.md`, `orca-capabilities.md`. `RM:N` = line N of `.dev/orca-command-refactor/README.md`. `CMD:N` = line N of the sandbox copy of the `/sc:spec-panel` command definition (`command.md`). Everything under `src/`, `CLAUDE.md`, `~/.claude`, `EVIDENCE.md`, the codegraph README, `Makefile` and `pyproject.toml` is not in the workspace: any citation that reaches only those is UNVERIFIED here and is marked so.

## Expert panel

Active, in the command's fixed order: Wiegers (1), Adzic (2), Cockburn (3), Fowler (4), Nygard (5), Whittaker (6, always active), Newman (7), Hohpe (8), Crispin (9, guard-table completeness). Focus `requirements` brings Wiegers, Adzic, Cockburn; focus `architecture` brings Fowler, Newman, Hohpe, Nygard. Gregory and Hightower are not in either focus and were not run. `--focus correctness` is not active, so no State Variable Registry is produced. Advisory only: the spec describes 3+ mutable states (Task status, Dispatch state, contract `status`) and numeric thresholds (60 s, 4 min, 5 min, depth 1, 3 failures), so `--focus correctness` would be worth a later pass.

## Verdict summary

Two blocking findings (F-1, F-2). Both are cases where two statements in the candidate cannot both be followed. 13 Medium and 9 minor items are listed under follow-up candidates. They are not blocking and do not appear in the Reviser brief.

| Quality metric (0-10) | Score | Note |
|---|---|---|
| Clarity | 7 | Requirement IDs, owner and evidence columns are precise; the path rule (F-2) and phase rule (F-1) are not. |
| Completeness | 7 | Strong on gates and outward actions; thin on retries, nesting propagation and versioning. |
| Testability | 6 | Most requirements have a named check; AC-1.1 and the live check cannot pass as written for some commands. |
| Consistency | 5 | Row-level data matches the inventories; the cross-section rules in WC-4, P1 and AC-1.1 contradict the rows. |

## Evidence block (what was checked against the inventories)

- Counts reconcile. S:76 says 43 commands split 10 / 27 / 6. INV-A:3 gives 21 and INV-B:3 gives 22. INV-A:73 gives 5 ready / 13 needs-change / 3 coordinator-only; INV-B:278 gives 5 / 14 / 3. 5+5 = 10, 13+14 = 27, 3+3 = 6, total 43. The ten names in S:83-92 are exactly the ten ready names in INV-A:73 and INV-B:280; the 27 rows in S:99-125 are exactly the 13 names of INV-A:76-83 plus the 14 names of INV-B:289-299; the six names in S:132-137 match INV-A:87-92 and INV-B:282-287.
- Phase counts reconcile. Non-ready rows by phase column: P1 = 9 (S:99,101,102,106,107,108,111,112,123), P2 = 11 (S:100,103,104,105,110,115,116,117,120,121,122), P3 = 4 (S:118,119,124,125), P4 = 3 (S:109,113,114), total 27. Ready-command fixes: P1 = 4 (adversarial, cleanup-audit, index-repo, workflow; S:83,85,86,92), P2 = 4 (reflect, release-split, tdd, troubleshoot; S:88-91), none = 2 (brainstorm, init-lite; S:84,87). The command lists in S:159-162 match these.
- About 60 `INV-A:`, `INV-B:` and `CAPS:` citations in S:21-285 were opened and each line says what the spec says it says. No wrong inventory line was found. The spec's 11 "re-read" locations (S:11) and every `src/` citation are UNVERIFIED here.

---

=== REQUIREMENTS ANALYSIS ===

### F-1  CRITICAL (FR-19 count mismatch), blocking. Phase 1 scope and AC-1.1 require the `--unattended` section on 36 commands; the per-command rows schedule it for 12.
- Experts: Wiegers (consistency of requirements), Fowler (count annotation), Whittaker (divergence attack).
- Where: S:159 (P1 scope), S:195 (AC-1.1), S:76 (section intro), the Phase column of S:98-125, S:154 and S:162 (P4 waits for D2-D4), S:240 and S:139 (D3 and pr-submit).
- The texts that conflict.
  - S:159 says the P1 scope includes "the `--unattended` flag accepted by every command in sections 3.1 and 3.2 except `/sc:load`".
  - S:195 says AC-1.1 asserts that "every command in sections 3.1-3.2 except `/sc:load`" has a `## Unattended mode` section.
  - S:154 says later phases do not start until the earlier phase's checks pass.
  - Against that, S:98-125 gives each command's gate resolution, report and section in a row with its own phase. 18 non-ready rows carry P2, P3 or P4 (S:100,103-105,109,110,113-122,124,125), and S:162 says P4 needs the answers to D2-D4 first.
  - S:240 says that under the recommended D3(a) there are "no pr-submit changes in Phase 4", and S:139 says pr-submit is a worker candidate only if D3 is accepted.
- Count scenario (Quantity Flow Diagram below). 10 ready + 27 needing a change - 1 (`/sc:load`) = 36 commands must carry the section when P1 ends. P1 itself schedules 8 non-load rows (analyze, build, business-panel, design, document, explain, index, test) + 4 ready-command fixes = 12. The other 24 are 11 P2 rows, 4 P3 rows, 3 P4 rows, 4 ready commands whose fix is P2 (reflect, release-split, tdd, troubleshoot) and 2 ready commands with no fix (brainstorm, init-lite). 12 + 24 = 36.
- Grading sentence. An implementer who follows the stated text as written builds, in Phase 1, an `--unattended` flag and `## Unattended mode` section on auggie-review, cleanup, task, implement, post-release, pr-submit and the other 18 gated commands. That is wrong because WC-2 requires each gate to resolve "per command in section 3" (S:60), and those resolutions, the WC-9 outward-off defaults and the D2-D4 decisions are scheduled in P2-P4 rows, and under D3(a) pr-submit never receives them. If the implementer instead follows the row phases, AC-1.1 cannot pass by construction, and S:154 then blocks Phase 2.
- Concrete attack (state trace). Before: `/sc:pr-submit` has no worker mode. P1 done per AC-1.1: it has `--unattended` and a section that names only `return-contract.yaml` and the contract path. D3(a) chosen, so no P4 row ever runs. State after: a coordinator brief following S:73 passes `--unattended`; nothing in the command text says what the `--monitor 1` y/n, the HALTs or the push, reply and resolve steps do (S:114 holds those answers and is not applied).
- Recommendation: narrow AC-1.1 and the S:159 scope to the commands whose own row or fix is scheduled in P1 (12 commands), and say in S:76 that every other command gets its flag and section in the phase shown on its row. Delete the "every command ... except /sc:load" wording; add nothing.

=== ARCHITECTURE ANALYSIS ===

### F-2  MAJOR, blocking. WC-4 places the contract at `<output-dir>/return-contract.yaml` where `<output-dir>` is the value of `--output` / `--output-dir`; the rows give commands whose `--output` is a file, whose contract sits one level lower, or whose directory is not chosen by the coordinator.
- Experts: Wiegers, Fowler (interface consistency), Hohpe (the report channel to the coordinator).
- Where: S:62 (WC-4), S:73 and S:62 ("known before dispatch"), S:87, S:90, S:83, S:92, S:183, S:201.
- The texts that conflict.
  - S:62: "`<output-dir>` is the directory the coordinator passed (`--output` / `--output-dir`)", and the worker passes that contract path as `--report-path`.
  - S:90: tdd is briefed with `--output <file>` (INV-B:222: the TDD is written at `--output`). S:87: init-lite is briefed with `--output <file>` (INV-A:55).
  - S:83: the adversarial contract is `<output>/adversarial/return-contract.yaml`, not `<output>/return-contract.yaml`.
  - S:92: the workflow contract is `.dev/tasks/to-do/<id>/return-contract.yaml`, where the package id is made at run time ("Fresh package each run", INV-B:273), and the workflow brief names no output flag, so the coordinator cannot know the path before dispatch.
- Grading sentence. An implementer who follows the stated text as written builds, for `/sc:tdd --output docs/x/TDD_FOO.md`, a contract path `docs/x/TDD_FOO.md/return-contract.yaml`. That path cannot exist because the `--output` value is a file. Reading it as the parent directory instead puts `return-contract.yaml` in `docs/x/`, where two parallel tdd workers overwrite each other's file and break WC-11. For adversarial the same reading yields `<output>/return-contract.yaml`, which the row in S:83 says is not where the file goes. In every case `test -s <contract>` (S:183) checks a path that holds no contract, so AC-2.3 (S:201) fails for tdd.
- Concrete attack (state trace). Brief: `/sc:tdd "<component>" --unattended --output docs/auth/TDD_AUTH.md`. WC-4 path = `docs/auth/TDD_AUTH.md/return-contract.yaml`. The file `docs/auth/TDD_AUTH.md` exists after the run, so creating that path fails with "Not a directory". The worker has no valid `--report-path`; WC-5 then maps "no report exists" to `--outcome failed` for a run that produced a good TDD.
- Recommendation: replace the parenthetical in S:62 with one rule that holds for every row, for example "the contract path is the one the row states; where a command's `--output` is a file, the brief names a separate contract directory", and state the exact contract path in the S:83, S:87, S:90 and S:92 rows. Delete the "`--output` / `--output-dir`" wording rather than adding a new flag section.

---

## Expert commentary by sequence position (critique-mode attribution of the findings above and the follow-ups below)

1. Wiegers: F-1 and F-2 are consistency defects between a general requirement and its own rows. M-2 (status vocabulary) and M-3 (AC-0.4) are testability gaps: the pass condition names a value that is not defined for the command.
2. Adzic: the examples in S:228 and S:208 are concrete. The missing example is the one in F-2: a file-valued `--output` with `--unattended`. M-1 is the second missing example: a retry into a directory that already holds the first attempt's contract.
3. Cockburn: actors and goals are clear (coordinator, worker session, command, person; S:50-51, S:72). The weak point is the worker session as actor: WC-3, WC-5, WC-7, WC-10 and WC-12 bind it, and nothing says how it receives them (M-9).
4. Fowler: the interface is one general rule plus per-command rows. Where they disagree (F-2) the general rule is the one that is wrong. The count funnel 43 → 10 / 27 / 6 and the phase funnel are conservative except in F-1.
5. Nygard: failure paths for readiness, ask timeouts, `consumer_fenced`, missing reports and outcome mapping are covered (S:59, 61, 63, 70). Unbounded: ask resumption and the blocked-answer-reinvoke loop (M-11), long single tool calls (M-7), stale contract after a retry (M-1).
6. Whittaker: attacks below.
7. Newman: the contract is installed as a shared core file read by commands from `~/.claude/` (S:52). The return contract has no schema version, and installed command text and the installed contract file can be at different versions (M-12).
8. Hohpe: one message channel carries the result: `worker_done` plus a path (S:62-63). Delivery is once-only and pull-based follow-ups are covered (S:70). Not covered: nested invocations that would write their own `return-contract.yaml` (M-6).
9. Crispin: guard table below; the live check at S:179-186 is thorough, with the two defects in M-3 and N-2.

## Whittaker adversarial analysis (FR-3 format)

1. I can break this specification by **Sentinel Collision Attack**. The invariant at **S:62 (WC-4) with S:262 (Decisions, status vocabulary) and S:183 (check 4)** fails when **an existing contract already uses a `status` value that is not one of `succeeded|partial|failed|blocked`**. Concrete attack: `/sc:workflow` writes `status: <its own value>` in contract 1.1 (INV-B:272). WC-4 says commands that already write a contract "keep their fields"; check 4 asserts the four-value set. Before: contract `status` = workflow's value. After P1 either the value is kept (check 4 fails) or replaced (the "keep their fields" rule fails). Severity MAJOR by label, graded Medium (M-2): the actual values are not in the inventories, so the wrong outcome needs a fact the document does not state.
2. I can break this specification by **Sentinel Collision Attack**. The invariant at **S:51 and S:228 (D1(a))** fails when **the text `--unattended` appears inside a free-text prompt**. Concrete attack: `/sc:tdd "explain why --unattended must never prompt" --output f.md`; the topic text contains the switch. The spec defines the switch as "a flag" and gives no token rule. Before: standalone behaviour. After: the command may switch off every gate for a person (M-10).
3. I can break this specification by **Sequence Attack**. The invariant at **S:61 (WC-3), S:64 (WC-6), S:62 (WC-4)** fails when **a command stops as `blocked`, the worker asks, then re-invokes the command with the answer**. Concrete attack: attempt 1 writes `out/return-contract.yaml` with `status: blocked` and artifacts; the worker re-invokes with the answer as a flag and the same `out/`. The "fresh dir" rows (most of S:99-125) say a re-run writes a fresh directory, but WC-4 fixes the report path before dispatch. Either the first attempt's files are overwritten (WC-6 broken) or the contract moves (WC-4 broken). If the retry writes nothing, `test -s out/return-contract.yaml` (S:183) still passes on the stale `blocked` file (M-1).
4. I can break this specification by **Accumulation Attack**. The invariant at **S:61 (WC-3)** fails when **no one ever answers**. Concrete attack: the worker resumes the same message id after each timeout with no limit and sends no heartbeat while blocked (S:61). The spec itself says a waiting worker is healthy (S:44, CAPS:129), so the stall that S:44 calls the real failure mode becomes an unbounded `ask` loop with no escalation rule (M-11).
5. I can break this specification by **Zero/Empty Attack**. The invariant at **S:62 (WC-4)** fails when **`--unattended` is passed with no output location**. Concrete attack: `/sc:analyze src --unattended`. The analyze row (S:99) says "add `--output`" and does not say it is required; post-release alone says "require an explicit `--output`" (S:113). Before: no contract path. After: unspecified (M-5).
6. I can break this specification by **Divergence Attack**. The invariant at **S:68 (WC-10)** fails when **a single tool call is a sub-agent fan-out that runs longer than 5 minutes**. Concrete attack: a cleanup-audit wave of 7-8 concurrent agents (INV-A:42) or a tdd research wave (INV-B:47) blocks the worker session in one Task call; the worker cannot heartbeat. WC-10 names only "a poll wait, a long eval". Whether missing heartbeats have any effect is itself UNVERIFIED (CAPS:182 item 7), so the rule is neither testable nor shown to matter (M-7).

## Guard Condition Boundary Table (Nygard builds, Crispin checks completeness, Whittaker attacks the entries)

Trigger: the spec has conditional logic, thresholds and sentinels. Six input classes are the menu, not a quota; a class that cannot occur for a guard is left out with one line of reason, shown under the table.

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|---|---|---|---|---|---|---|
| G1 `--unattended` switch | S:51, S:60, S:228 | Zero/Empty | flag absent | false | standalone behaviour unchanged (S:146, SA-1) | OK |
| G1 | S:60 | One/Minimal | flag is the only extra argument | true | WC-2: no prompt, gates resolve (a)-(c) | OK |
| G1 | S:73 | Typical | brief carries flag + output + authorizations | true | WC-2, WC-4, WC-9 | OK |
| G1 | S:51, S:228 | Sentinel Value Match | `--unattended` inside a quoted prompt | unspecified | no token rule | GAP (M-10) |
| G1 | S:217, S:228 | Legitimate Edge Case | a person types the flag | true | opt-in; "a person never types it" | OK |
| G2 WC-5 outcome map | S:63 | Zero/Empty | no report file | n/a | `--outcome failed` | OK |
| G2 | S:63 | One/Minimal | `status: succeeded` | true | `--outcome succeeded` | OK |
| G2 | S:63, S:200 | Typical | `partial`, `blocked`, `failed` | mapped | partial → succeeded; blocked, failed → failed | OK |
| G2 | S:62, S:262 | Sentinel Value Match | existing contract `status` outside the four values | unspecified | "keep their fields" vs fixed set | GAP (M-2) |
| G2 | S:63 | Legitimate Edge Case | report exists but is unreadable or has no `status` | unspecified | only "no report exists" is mapped | GAP (M-2) |
| G3 WC-10 wait size | S:68, S:210 | Zero/Empty | no blocking step | n/a | no requirement | OK |
| G3 | S:68 | Typical | a 3-minute poll | true | heartbeat between waits | OK |
| G3 | S:68, S:210 | Maximum/Overflow (boundary) | a wait of exactly 240 s | true | "at most 4 minutes"; AC-4.3 "no call exceeds 240 s" | OK |
| G3 | S:68 | Maximum/Overflow | one Task fan-out call over 5 minutes | unspecified | not covered | GAP (M-7) |
| G3 | S:283 (#12) | Legitimate Edge Case | pr-submit poll script runtime | unknown | declared UNVERIFIED | GAP (M-7) |
| G4 nested depth | S:33, S:66 | Zero/Empty | depth 0 (coordinator) | allowed | coordinator starts workers | OK |
| G4 | S:33, S:66 | One/Minimal | depth 1 (a worker) | refused | WC-8: no `worker-start`, `dispatch`, `task-create` | OK |
| G4 | S:252 (D5) | Maximum/Overflow | user raises the depth | n/a | D5(b), non-goal 2 (S:214) | OK |
| G4 | S:122, S:65 | Legitimate Edge Case | Agent-tool nesting at Claude Code's depth limit | unspecified | asserted "inside the limit" for tasklist | GAP (M-13) |
| G5 WC-3 ask | S:61 | Zero/Empty | no preamble | false | command stops `blocked` (WC-2 c) | OK |
| G5 | S:61 | Typical | answer arrives | true | re-invoke or resume with answer flag | OK |
| G5 | S:61 | Typical | ask times out | true | resume the same message id | OK |
| G5 | S:61 | Maximum/Overflow | repeated timeouts; or re-invoked command hits the next gate | unspecified | no bound, no escalation | GAP (M-11) |
| G6 WC-6 retry | S:64 | Typical | retry with the command's resume flag | true | resumes from disk | OK |
| G6 | S:64, S:62 | Legitimate Edge Case | retry or re-invoke into the same output dir | unspecified | "fresh dir" vs fixed path | GAP (M-1) |
| G6 | S:263 | Maximum/Overflow | repeated worker-reported `failed` | not counted by Orca (CAPS:80) | no bound stated | GAP (M-11) |
| G7 WC-4 output location | S:62, S:99 | Zero/Empty | `--unattended`, no output location | unspecified | rows say "add `--output`", not "required" (except S:113) | GAP (M-5) |
| G7 | S:62, S:90 | Legitimate Edge Case | file-valued `--output` | unspecified / contradicted | see F-2 | GAP (F-2) |
| G8 refusal rows (`--monitor 1`, `--watch`, `--interactive`, `--mode socratic`, `--format interactive`) | S:102,103,108,110,114,123 | Legitimate Edge Case | refused flag combination | "refused" | contract `status` for a refusal is not given; `blocked_question` is "when blocked" (S:62) | GAP (M-5) |
| G9 task confidence | S:121 | Typical | confidence 0.85 | false | proceeds (unchanged) | OK |
| G9 | S:121 | Legitimate Edge Case | exactly 0.70 / 0.69 | false / true | "below 0.70" → blocked | OK |
| G9 | S:121 | Zero/Empty | no confidence value produced | unspecified | not stated | GAP (minor, N-9) |
| G10 WC-12 `check` | S:70 | Zero/Empty | empty `check` result | continue | an empty check never means replaced (CAPS:67) | OK |
| G10 | S:70 | Typical | `consumer_fenced` | true | stop; send no `worker_done` | OK |

Left out, with reason: G1 Maximum (a boolean has no capacity); G2 Maximum (a closed set of four values); G3 Sentinel (no sentinel value); G4 Sentinel (the malformed-setting fallback is Orca behaviour, CAPS:100, not a spec rule); G5 One/Minimal (a single question has no distinct behaviour from Typical); G6 Zero (a first attempt has no retry); G9 Maximum (a ratio has no overflow); G10 Maximum and Sentinel (no capacity or reserved value). Every GAP row above is graded in the finding it points to. FR-8 and FR-9 gaps are Medium where no concrete wrong outcome follows from stated text (M-1, M-2, M-5, M-7, M-10, M-11, M-13) and blocking only for F-2, where the stated text produces an impossible path.

## Pipeline Dimensional Analysis (FR-17 to FR-21)

Triggered for the classification and rollout funnel (two stages where counts change: classification, then phase assignment). The Task fan-out of a coordinator run (N Tasks → N Dispatches → N `worker_done`) was also annotated: S:182 requires exactly one `worker_done` per Dispatch and S:70 lets a fenced worker send none, so N Tasks can yield fewer than N `worker_done`; the spec handles this through WC-12 and the live check, no mismatch.

```text
[Source: 43 commands (21 INV-A + 22 INV-B)] --> [Stage 1: classify] --> [10 ready | 27 need change | 6 coordinator-only]   (10+27+6 = 43, conserved)
                                                                           |
                                                                           v
                                                  [Stage 2: assign phase, S:158-162]
                                                  P0: 0 command edits (3 smoke runs)
                                                  P1: 12 commands change (8 rows + 4 ready fixes)
                                                  P2: 15 (11 rows + 4 ready fixes)
                                                  P3: 4        P4: 3      none: 2 (brainstorm, init-lite)
                                                  (12 + 15 + 4 + 3 + 2 = 36 = 10 + 27 - 1 for /sc:load, which is excluded)
                                                                           |
                                                                           v
                                      [Consumer: AC-1.1 expects the section on 36 commands at end of P1]  <-- MISMATCH (12 scheduled vs 36 expected), F-1
                                      [Consumer: S:159 expects the flag on 36]                            <-- MISMATCH, F-1
```

The load row is P1 (S:112) but is excluded from the flag and section (S:112, S:159, S:195), which is why the P1 count is 8 rows plus the 4 ready fixes = 12, and the funnel adds up to the 36 non-load commands once the two untouched ready commands are counted.

---

## Follow-up candidates (Medium and minor; none blocks the verdict, none is in the Reviser brief)

The grading check for Medium: each needs a guess that the implementer picks the worse of two readings the text allows, or is a requirement the document never states.

### Medium (warnings)
- M-1. Retry or re-invocation into the same output directory. S:62 and S:73 fix the contract path before dispatch; S:64 and most "fresh dir" rows in S:99-125 say a re-run writes a fresh directory; S:61 says the worker re-invokes after an answer. Nothing says who creates the fresh directory or that the retry brief must carry a new one, so a stale `blocked` contract can satisfy `test -s` (S:183). Add one sentence in WC-6 that the coordinator passes a new output location per attempt.
- M-2. Status vocabulary against "keep their fields". S:62 keeps existing contract fields; S:262 and S:183 fix the set of four values. The existing `status` values of workflow, brainstorm, reflect and adversarial are not in the inventories (INV-B:272 says only that a `failed` value exists for workflow). A bad or missing `status` also has no mapping in WC-5.
- M-3. AC-0.4 (S:194) requires the outcome to match "the status in the command's existing report". For troubleshoot the existing report is REPORT.md with `report_path` (S:91, INV-B:242); no `status` field is cited, so the check has no value to compare. Name the field or the rule per smoke command.
- M-4. SA-2 (S:147) allows an Orca mention "inside the contract file" as an example of a caller's question channel; AC-C1 (S:172) greps `src/superclaude/core`, where the contract file lives, for `orca (orchestration|worktree|terminal|agent)` and fails on any hit except under `skills/ccsession-tag/`. A natural example, `orca orchestration ask`, fails the common check in every phase from P0.
- M-5. No rule for `--unattended` without an output location, and no `status` for a refused combination. Only post-release is told to require `--output` (S:113); the analyze, build, design, document, explain, index and test rows say "add `--output`" (S:99,101,106-108,111,123). "Refused" appears in S:102,103,108,110,114,123, while `blocked_question` is defined only "when blocked" (S:62).
- M-6. Nested invocations. The spec does not say whether `--unattended` and the output location pass to the commands a command invokes (brainstorm → adversarial, INV-A:39; workflow → reflect, INV-B:271; release-split → brainstorm and adversarial, INV-B:121; tdd → task, INV-B:219; roadmap → adversarial, INV-B:151). Only tasklist (S:122) and tdd (S:90) state a propagation or a gate. A child that writes its own `return-contract.yaml` in a shared directory overwrites the parent's.
- M-7. WC-10 covers "a poll wait, a long eval" (S:68) but not a sub-agent fan-out in a single Task call (examples in attack 6), and whether a missed heartbeat has any effect is UNVERIFIED (CAPS:182 item 7; CAPS:125 says absence never authorizes stop or retry). The requirement may be impossible to meet for fan-out commands and is checked only for pr-submit (S:210).
- M-8. WC-11 (S:69) says default paths carry "a timestamp or the slug the coordinator passes". The `save` per-session key is `<key>-<session-or-timestamp>.md` (INV-B:165). Two workers started in the same second or minute with a timestamp-only name can collide; the check in S:207 uses two workers and would pass only by luck of timing. State "session id" or "coordinator slug" as the required discriminator.
- M-9. Delivery of worker-session rules. WC-3, WC-5, WC-7, WC-10 and WC-12 (S:61, 63, 65, 68, 70) bind the worker session. S:73 lists what the brief states (command line, output directory, authorizations, placement) and does not list "read `~/.claude/WORKER-CONTRACT.md`" or the outcome mapping. In P0 no command has the section yet (S:158), so the three smoke runs rely on a brief template whose contents S:158 describes only as "listing the section 3.1 flags".
- M-10. No token rule for `--unattended` (attack 2). The matching rule belongs in section 2.1.
- M-11. No bound on `ask` resumption, on the blocked → answer → re-invoke loop (cli-portify has three gates, S:105), or on retries of worker-reported failures, which do not trip Orca's circuit breaker (S:263, CAPS:80). Orca's own guidance treats a waiting worker as healthy (CAPS:129).
- M-12. No version field in the return contract (S:62) and no rule for a command built against one version of `~/.claude/WORKER-CONTRACT.md` running beside another (S:52). The existing workflow contract already carries "contract 1.1" (INV-B:272). S:279 (UNVERIFIED 8) leaves the plugin copies open.
- M-13. tasklist (S:122). The row resolves the reflect offer but not the `needs_human_decision` HALT of Stage 10.5 (INV-B:209), and says the reflect fan-out is "inside Claude Code's nesting limit" (INV-A:14) while INV-B:210 and INV-B:215 call nested spawning UNVERIFIED and ask for the fan-out at the worker's top level. The two inventories disagree and the spec states one side as fact.

### Minor notes
- N-1. `(B-1)` and `(B-2)` at S:112, S:159, S:194, S:195 and S:196 are labels from an earlier report; they are defined nowhere in the candidate.
- N-2. Live-check step 5 (S:184) searches the transcript for `AskUserQuestion`; the text of loaded command and skill files also contains that word, so the check can fail on a mention. Say "a tool call named".
- N-3. AC-C5 (S:176) fails on any changed old line; adding a flag to an existing `Usage` line is a changed line. S:149 (SA-4) lists the allowed exceptions without naming "Usage line".
- N-4. S:154 says Phases 1-3 need no user decision; S:244 lists auggie-review and task (P2 rows, S:100,121) as consumers of D4. S:225 resolves it ("proceed on the recommendations"); one sentence would align them.
- N-5. S:23 (E3) says "It has worked before"; S:43 (1.4 item 1) says only the nested route is proven. Both are correct as qualified; E3 reads stronger than the evidence.
- N-6. S:16 says the command changes are "limited to the worker contract"; SA-4 (S:149) and rows such as explain, validate-tests and business-panel (S:102,108,125) add defect fixes.
- N-7. WC-1 (S:59) has an owner ("Launch setup, not commands") but no phase deliverable; only live-check step 1 (S:180) would catch a regression.
- N-8. AC-2.4 (S:202) compares PR review and comment counts before and after; bot reviewers on the same PR can change the counts and cause a false failure.
- N-9. G9 (S:121): behaviour when no confidence value is produced is not stated.
- Cross-note (UNVERIFIED relation, not graded). The sandbox `/sc:spec-panel` definition already has `--unattended`, `--report-dir` and a `<report-dir>/return-contract.yaml` rule (CMD:22-23, CMD:455-465) and points to `~/.claude/WORKER-CONTRACT.md` (CMD:457), which is not in the sandbox home. The spec's spec-panel row (S:120) says to "add `--output`". Whether the command file is a later state or an independent edit cannot be told from the workspace.

## Coverage

Read in full: the candidate (285 lines), `README.md`, `inventory/commands-a.md`, `inventory/commands-b.md`, `inventory/orca-capabilities.md`, the sandbox command definition, and the review-loop prompts file. Checked: the 43 / 10 / 27 / 6 reconciliation, the phase-count reconciliation, about 60 inventory citations, the internal consistency of WC-1 to WC-12, SA-1 to SA-6, sections 3, 4, 6, 7 and 9, the guard conditions listed above, and the five Whittaker attack methodologies. Not covered: every `src/`, `CLAUDE.md`, `~/.claude`, `EVIDENCE.md`, codegraph README, `Makefile` and `pyproject.toml` citation (not in the workspace), the claim that a fresh evidence-validator re-read about 340 citations (S:285), and the prior review and disposition files (not present, so nothing here compares against an earlier report). No file other than this report was written.

Issue question for the follow-up candidates: not asked in this run (the worker's final reply is fixed to `DONE <path>`); no issue was created. The coordinator asks the user once for this loop.

## Reviser brief

Blocking finding ids: F-1, F-2.

Restated rules for the reviser (command bullet 6): revise only text a blocking finding names; add no rule, mechanism or section that no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size of the candidate before and after, and the bytes added and deleted per finding id. Leave Medium and minor findings alone, return the candidate once and do not award yourself a PASS.

- F-1 (S:76, S:159, S:195): limit the Phase 1 flag-and-section scope and AC-1.1 to the commands whose own row or fix is P1, and let each other command receive its flag and section in the phase on its row.
- F-2 (S:62, S:83, S:87, S:90, S:92): replace the `<output-dir>/return-contract.yaml` rule with a rule that holds for file-valued `--output`, the adversarial subdirectory and the workflow run-time id, and state the exact contract path in those four rows.

verdict: FAIL

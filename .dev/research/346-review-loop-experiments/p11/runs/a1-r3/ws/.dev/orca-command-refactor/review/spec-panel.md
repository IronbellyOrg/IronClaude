# Spec panel review: orca-worker-contract-spec.md

review: 1 of 3

| Field | Value |
|---|---|
| Command | `/sc:spec-panel @.dev/orca-command-refactor/specs/orca-worker-contract-spec.md --mode critique --focus requirements,architecture` |
| Spec under review | `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md` (286 lines), not edited by this review |
| Review type | First review of the full document. `--re-review` and `--baseline` were not given, so no `baseline: missing` note applies |
| Review date | 2026-11-10 |
| Panel (review order) | Wiegers (lead), Adzic, Cockburn, Fowler, Nygard, Whittaker, Newman, Hohpe, Crispin (guard-table completeness) |
| Active focus | requirements, architecture. `--focus correctness` is not active, so no State Variable Registry is produced. The Guard Condition Boundary Table is produced because the spec contains guards (see below) |

Citation shorthand: `SPEC:N` = line N of `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`. `INV-A:N`, `INV-B:N`, `CAPS:N` = line N of `.dev/orca-command-refactor/inventory/commands-a.md`, `commands-b.md`, `orca-capabilities.md`. `README:N` = `.dev/orca-command-refactor/README.md`. `CMD:N` = line N of `command.md` in the review sandbox (the `/sc:spec-panel` definition).

Verification scope. Only the spec, the README, the three inventories and `command.md` exist in the workspace. I spot-checked about 40 `INV-A`, `INV-B` and `CAPS` line citations in the spec (for example `CAPS:97-103`, `CAPS:145-151`, `INV-A:76-83`, `INV-B:289-299`, `INV-B:323`); each pointed at text that supports the claim it is cited for. I also re-counted the command split (see Quantity Flow Diagram). Every citation to `src/`, `CLAUDE.md`, `~/.claude`, `.dev/evals/...`, `.dev/codegraph-migration/...` and `orca-ide` output is UNVERIFIED here, because none of those exist in the workspace. The spec's own claim that it re-read 11 locations and that an evidence-validator re-read about 340 citations (`SPEC:11`, `SPEC:285`) is likewise UNVERIFIED.

## Standard-format summary

```yaml
specification_review:
  original_spec: .dev/orca-command-refactor/specs/orca-worker-contract-spec.md
  review_date: 2026-11-10
  expert_panel: [wiegers, adzic, cockburn, fowler, nygard, whittaker, newman, hohpe, crispin]
  focus_areas: [requirements, architecture]
quality_assessment:
  overall_score: 5.8
  clarity: 7        # tables, evidence column and UNVERIFIED marking are strong
  completeness: 6   # contract location, propagation, version skew and retry are missing
  testability: 5    # several acceptance checks are wrong or absent (F8, F9, F15)
  consistency: 5    # counts and phase scopes contradict each other (F1, F2, F4)
critical_issues:
  blocking: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
  non_blocking: [15, 16, 17, 18, 19, 20, 21, 22, 23, 24]
expert_consensus:
  - The decision itself (Orca coordinates, commands stay units of work) is well argued and the rejected alternative is fairly treated (SPEC:28-39).
  - The worker contract (WC-1..WC-12) is a sound skeleton, but its two load-bearing mechanisms, the report file and the unattended switch, are not specified tightly enough to implement the same way twice.
  - The phase plan and its acceptance checks disagree with section 3 and with each other.
improvement_roadmap:
  immediate: [1, 2, 3, 4, 5, 8, 9]
  short_term: [6, 7, 10, 11, 12, 13, 14]
  long_term: [15, 16, 17, 18, 19, 20, 21, 22, 23, 24]
adversarial_analysis: see === ADVERSARIAL ANALYSIS === (findings 2, 3, 10, 11, 12, 14)
```

Grading used (Review Loop bullet 2): CRITICAL and FR-8/FR-9 findings are blocking; MINOR is minor; a MAJOR is blocking only if it names a concrete wrong outcome an implementer would produce, otherwise it is graded minor. Findings 10 to 14 are blocking because they come from GAP rows of the Guard Condition Boundary Table (FR-8).

## Guard Condition Boundary Table

Trigger: the spec contains conditional logic, thresholds and flag guards. Five cross-cutting guards are enumerated; the per-command gate resolutions in section 3 are instances of guard G5 and are not repeated. Construction: Nygard. Completeness validation: Crispin. Attacks on entries: Whittaker. All 30 rows are populated, so the FR-10 synthesis gate is satisfied. Each GAP row generates a finding of MAJOR severity or higher (FR-8); the finding id is shown in the Status column. Where the spec is silent the Specified Behavior cell says "unspecified" (FR-9).

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|---|---|---|---|---|---|---|
| G1 unattended switch | SPEC:51, SPEC:60, SPEC:227-230 | Zero/Empty | flag absent | false | Standalone behavior unchanged (SPEC:146 SA-1) | OK |
| G1 unattended switch | SPEC:62, SPEC:73 | One/Minimal | `--unattended` alone, no output directory or output flag | true | unspecified: WC-4 writes `<output-dir>/return-contract.yaml` but nothing says what happens when the caller passed no directory | GAP (F11) |
| G1 unattended switch | SPEC:62, SPEC:73 | Typical | `--unattended --output <dir>` | true | Contract written in `<dir>`, gates resolve per section 3 | OK |
| G1 unattended switch | SPEC:90, SPEC:83-84, SPEC:89 | Maximum/Overflow | `--unattended` together with `--interactive`, `--watch`, `--mode socratic` or `--format interactive` | true | Refused only for the commands whose row says so (cleanup, improve, test, business-panel, explain, roadmap, pr-submit monitor 1). For adversarial, brainstorm and release-split the brief merely "never" passes `--interactive`; the command's behavior if both appear is unspecified | GAP (F11) |
| G1 unattended switch | SPEC:51 | Sentinel Value Match | the text `--unattended` inside a quoted topic or file content, for example `/sc:tdd "explain the --unattended flag"` | ambiguous | unspecified: no rule that the switch counts only as a standalone argument token | GAP (F11) |
| G1 unattended switch | SPEC:128, SPEC:132-137, SPEC:159 | Legitimate Edge Case | flag passed to a section-4 command, or to an install that predates the flag | unknown | Section 4 says these "get no `--unattended` mode" but not what they do when given the flag; no version or capability check exists. Old installs treat the text as free-form arguments | GAP (F6) |
| G2 outcome mapping | SPEC:63 | Zero/Empty | report file absent | failed | `--outcome failed` (WC-5 "or no report exists") | OK |
| G2 outcome mapping | SPEC:62-63 | One/Minimal | report file present, zero bytes or not parseable YAML | unknown | unspecified: WC-5 says only "no report exists" | GAP (F12) |
| G2 outcome mapping | SPEC:63 | Typical | `status: succeeded` or `partial` | succeeded | `--outcome succeeded`, first sentence states the status (decision SPEC:263) | OK |
| G2 outcome mapping | SPEC:62 | Maximum/Overflow | `status: blocked` with a missing or empty `blocked_question` | failed | WC-4 requires the field "when blocked" but states no non-empty rule; only the P2 live check asserts it (SPEC:200) | GAP (F12) |
| G2 outcome mapping | SPEC:62, SPEC:195, SPEC:183 | Sentinel Value Match | existing contract whose `status` value is outside the fixed set, such as a command's own legacy vocabulary | unknown | WC-4 says existing commands "keep their fields"; the check at SPEC:183 asserts the fixed set. The two collide and the legacy values were never inventoried | GAP (F12) |
| G2 outcome mapping | SPEC:62, SPEC:64, SPEC:73 | Legitimate Edge Case | a retry runs in the directory of the first attempt and dies before writing; an old `return-contract.yaml` is still there | stale | unspecified: nothing requires the command to remove or overwrite the contract at start | GAP (F3) |
| G3 wait and heartbeat | SPEC:68 | Zero/Empty | wait of 0 s, no blocking call | n/a | No heartbeat issue | OK |
| G3 wait and heartbeat | SPEC:68 | One/Minimal | single tool call of 1 minute | below threshold | No split needed | OK |
| G3 wait and heartbeat | SPEC:68 | Typical | one call of 2 minutes | below threshold | No split needed | OK |
| G3 wait and heartbeat | SPEC:68, SPEC:210, SPEC:266 | Maximum/Overflow | single call of 4.5 minutes | WC-10 false (not longer than 5), decision true (waits must be at most 4) | WC-10 requires a split only above 5 minutes; the Decisions row and AC-4.3 require at most 4 minutes (240 s). A 4.5-minute call passes one and fails the other | GAP (F10) |
| G3 wait and heartbeat | SPEC:68, SPEC:65 | Sentinel Value Match | a parallel Agent-tool batch that blocks the top-level session for more than 5 minutes (cleanup-audit waves, tdd research, post-release scanners) | true | unspecified: WC-10 names poll waits and evals only, and a parallel batch cannot be split into 4-minute waits (E4 keeps fan-out as is) | GAP (F10) |
| G3 wait and heartbeat | SPEC:68, SPEC:104 | Legitimate Edge Case | cli-eval job of up to 3600 s | true | Split into waits of at most 4 minutes (SPEC:104) | OK |
| G4 outward-action authorization | SPEC:67 | Zero/Empty | no authorizing flag in the brief | off | Every outward default is off (WC-9) | OK |
| G4 outward-action authorization | SPEC:67, SPEC:245 | One/Minimal | explicit flag present, no quoted user instruction in the brief | on | unspecified: D4(a) wants the quote, but a command sees only the flag and cannot check the brief | GAP (F13) |
| G4 outward-action authorization | SPEC:67, SPEC:245 | Typical | explicit flag plus quoted instruction | on | Action runs | OK |
| G4 outward-action authorization | SPEC:113, SPEC:244 | Maximum/Overflow | post-release with VM, install, commit and PR all in play | partial | "the command's own explicit flag" is singular; no per-action flags are defined, and D4 is left open | GAP (F13) |
| G4 outward-action authorization | SPEC:122, SPEC:121 | Sentinel Value Match | a nested skill the command invokes (task to troubleshoot, tdd to task, brainstorm to adversarial, workflow to reflect) | unknown | unspecified: only tasklist passes `--unattended` to reflect (SPEC:122); no general propagation rule | GAP (F7) |
| G4 outward-action authorization | SPEC:100 | Legitimate Edge Case | auggie-review on a PR target with `--unattended` and `--post-pr` | on | Posting returns only with the explicit flag | OK |
| G5 gate resolution | SPEC:60 | Zero/Empty | gate with no default and no caller flag | blocked | Contract `status: blocked`, then stop (WC-2 c) | OK |
| G5 gate resolution | SPEC:60 | One/Minimal | caller supplies the flag that answers the gate | resolved | WC-2 b | OK |
| G5 gate resolution | SPEC:60, SPEC:116 | Typical | documented default exists (research pins `--strategy planning`) | resolved | WC-2 a | OK |
| G5 gate resolution | SPEC:60 | Maximum/Overflow | a run with several blocking gates (cli-portify has three, cli-eval has suite choice, safety flags and a confirmation) | blocked | One contract carries one `blocked_question`; which gate is reported first, and whether later gates are listed, is unspecified | GAP (F14) |
| G5 gate resolution | SPEC:60 | Sentinel Value Match | caller flag and documented default both present and different | unknown | unspecified: WC-2 lists (a) default, (b) flag, (c) blocked without a precedence rule | GAP (F14) |
| G5 gate resolution | SPEC:105, SPEC:61 | Legitimate Edge Case | gate that can only be answered after seeing a mid-run artifact (cli-portify approvals) | blocked | Stop and name the artifact; the answer returns by a new `--resume` flag that does not exist yet | OK |

Table result: 30 rows, 15 GAP (G1 four, G2 four, G3 two, G4 three, G5 two), mapped to findings 3, 6, 7, 10, 11, 12, 13 and 14. G5 row 6 is OK only because the spec adds the resume flag in P2 (SPEC:105).

## Quantity Flow Diagram (Pipeline Dimensional Analysis)

Trigger: the spec describes a multi-stage flow where the count changes at a stage (43 commands are filtered into groups, then into phases, then into acceptance checks). Fowler annotated the counts; Whittaker attacked each divergence. I re-counted section 3 and section 4 rows myself: ready 10 (SPEC:83-92), needs-change 27 (SPEC:99-125), coordinator-only 6 (SPEC:132-137). Inventory totals agree: 5 + 5 ready, 13 + 14 needs-change, 3 + 3 coordinator-only (INV-A:73, INV-B:278).

```text
[Source: 43 commands = 21 INV-A + 22 INV-B]   (SPEC:76)
   --> [Stage 1: section 4 filter] --> 6 coordinator-only (agent, git, help, pm, spawn, swarm-wizard)
   --> 37 worker-capable                                   (N=43 in, M=37 out, divergence 6)
         |-- 10 ready today (SPEC:83-92)
         `-- 27 needs a change (SPEC:99-125)
   --> [Stage 2: phase assignment]
         P0: 3 smoke runs drawn from the 10 ready (SPEC:158)
         P1: 9 needs-change (analyze, build, business-panel, design, document, explain, index, load, test)
             + 4 small fixes on ready (adversarial, cleanup-audit, index-repo, workflow)   (SPEC:159)
         P2: 11 needs-change + 4 ready (reflect, release-split, tdd, troubleshoot) = 15    (SPEC:160)
         P3: 4 (roadmap, save, validate-roadmap, validate-tests)                           (SPEC:161)
         P4: 3 (implement, post-release, pr-submit)                                        (SPEC:162)
         check: 9 + 11 + 4 + 3 = 27 needs-change, and 4 + 4 = 8 ready small fixes + 2 ready with none = 10   OK
   --> [Consumer A: P1 scope "flag accepted by every command in 3.1 and 3.2"]   expects 37, receives 13 command edits   (SPEC:159)
   --> [Consumer B: AC-1.1 "every command in 3.1-3.2 has a section naming return-contract.yaml"]  expects 37   <-- MISMATCH (SPEC:195)
         supply: load defines no contract (SPEC:112)                              -> 36
                 pr-submit leaves the worker set if D3(a) is chosen (SPEC:139, 240-242) -> 35
                 implement and post-release (and pr-submit) wait for D2-D4 (SPEC:154)  -> 33 writable in P1
   --> [Consumer C: AC-1.1 "no section-4 command has one"]   expects 6 absent; pr-submit would make it 7 under D3(a)   <-- MISMATCH
```

Divergence result: the 43 to 37 to phase counts conserve. Consumers B and C do not: AC-1.1 assumes 37 workers with a contract section and 6 without, while section 3 itself gives 36 with a contract and the recommended D3(a) moves pr-submit into the "without" group. Finding 1 (CRITICAL under FR-19).

=== REQUIREMENTS ANALYSIS ===

Each finding: issue, severity, expert, recommendation with rationale, priority, quality-impact estimate. "Blocking" follows the grading rule above.

**F1. AC-1.1 and the P1 scope count commands the spec itself excludes or defers.** Severity CRITICAL (FR-19 count mismatch), blocking. Expert: Wiegers (traceability), with Fowler's count annotation. Spec: section 6 P1, section 7.3 AC-1.1, section 3.2 load and pr-submit, section 4 closing paragraph, section 9 D3.
Issue: AC-1.1 (SPEC:195) requires all 37 commands of sections 3.1 and 3.2 to carry a `## Unattended mode` section that names `return-contract.yaml`, and no section-4 command to carry one. But `/sc:load` gets no contract (SPEC:112, decision SPEC:265), `/sc:pr-submit` leaves the worker set under the recommended D3(a) (SPEC:139, SPEC:240-242), and `/sc:implement`, `/sc:post-release` and `/sc:pr-submit` are written in P4 after D2-D4 (SPEC:154, SPEC:162). Concrete count: 37 expected, 36 definable (no `load`), 35 if D3(a) removes pr-submit, and only 33 writable in P1 (implement and post-release also wait for P4).
Recommendation: restate AC-1.1 against an explicit list (the P1 set plus the ready commands), move pr-submit to section 4 or to a "conditional on D3" row with its own count, and say that `load` carries a section that names no contract file. Rationale: a check that cannot pass either blocks the phase gate (SPEC:154) or pushes an implementer to invent a contract for `load`, which the spec rejected.
Priority High. Quality impact: Consistency +2, Testability +1.

**F4. The contract location in WC-4 does not fit the commands it is applied to.** Severity MAJOR, blocking (concrete wrong outcome below). Expert: Wiegers. Spec: section 2.2 WC-4, section 2.3, section 3.1 and 3.2 report columns, section 7.2 step 4, AC-2.2.
Issue: WC-4 fixes the contract at `<output-dir>/return-contract.yaml`, "known before dispatch" (SPEC:62, SPEC:73), where the directory is what the caller passed as `--output` or `--output-dir`. Section 3 then contradicts it in four ways. (1) `--output` is file-valued for tdd, init-lite and, after this change, spec-panel and analyze (SPEC:87, SPEC:90, SPEC:99, SPEC:120); no rule says where the contract goes beside a file. `command.md` itself notes that `--output` is file-valued and uses a separate `--report-dir` (CMD:456). (2) adversarial is told to write `<output>/adversarial/return-contract.yaml` (SPEC:83), not `<output>/return-contract.yaml`. (3) workflow's contract is `.dev/tasks/to-do/<id>/return-contract.yaml` with a generated id (SPEC:92), so it is not known before dispatch, and the "pre-creation STOP" has no `<id>` directory to hold it. (4) troubleshoot's `return-contract.yaml` exists only with `--caller task-unified` (INV-B:242), while its row reports `REPORT.md` (SPEC:91).
Concrete wrong outcome: two implementers read WC-4 differently. One places tdd's contract in the dirname of the TDD file, where two parallel workers writing into `docs/` overwrite one `return-contract.yaml` (a WC-11 violation); the other gives adversarial two contract paths. AC-2.2 (SPEC:200) cannot even name the contract path for its own `/sc:tdd "auth" --unattended --output <file>` example.
Recommendation: add one placement rule to WC-4 that covers file-valued output, generated-id output and fixed subdirectories (for example "next to the main deliverable, named `<deliverable-stem>.return-contract.yaml`, or in the explicit `--report-dir`"), and let the worker, not the coordinator, be the source of the path for generated ids (the `--report-path` it already sends). Priority High. Quality impact: Completeness +1, Testability +1.

**F13. WC-9 authorization cannot be checked where it is applied.** Severity MAJOR, blocking (FR-8 GAP rows G4-2 and G4-4). Expert: Cockburn (who is the actor and what goal authorizes the action). Spec: section 2.2 WC-9, section 3.2 post-release, section 9 D4.
Issue: WC-9 says outward actions turn on "only through the command's own explicit flag written in the brief" (SPEC:67), and D4(a) adds that the coordinator must "quote the user's instruction" (SPEC:245). A command sees the flag, never the brief, so the quote cannot be enforced anywhere; the only mechanical check is "default is off" (AC-2.4, AC-4.2). For post-release, the one command with four outward actions (VM, real-target install, commit, PR; SPEC:113), the spec offers one flag by name-less reference and leaves the decision open (D4).
Concrete wrong outcome: an implementer adds a single `--allow-outward` flag to post-release. A coordinator that was told "install it" then also commits and opens a PR.
Recommendation: require one flag per outward action class in the `## Unattended mode` sections (named in section 3 for post-release, auggie-review `--post-pr`, task `commit`/`push`), and move the "quote the instruction" duty to the coordinator side of section 2.3 where it can be reviewed. Priority High. Quality impact: Testability +1.

**F15. WC-1, WC-3 and WC-12 have no phase owner or acceptance check.** Severity MAJOR, graded minor (no concrete wrong outcome). Expert: Wiegers with Crispin. Spec: section 2.2, section 6, section 7.
Issue: WC-1 names "launch setup" as owner (SPEC:59) but no phase touches the launch path and no check tests it beyond the generic `state: ready` in step 1 (SPEC:180). WC-3 (the `ask` route, SPEC:61) and WC-12 (the `check` before `worker_done`, SPEC:70) are rules for the worker session, yet none of AC-P0 to AC-4.3 exercises either; step 5 only looks for an absent `AskUserQuestion` (SPEC:184). WC-1 also says "well inside" the 60 s limit without a number, although the evidence gives one (30 s works, about 45 s fails; CAPS:49).
Recommendation: add one row per requirement to a small traceability table (requirement, phase, check id) and state the WC-1 fallback as "at most 30 s". Priority Medium. Quality impact: Testability +1.

**F19. "Phases 1-3 need no user decision" is contradicted by D4.** Severity MINOR, not blocking. Expert: Cockburn. Spec: section 6 intro and section 9 D4.
Issue: SPEC:154 says Phases 1-3 need no decision and only Phase 4 waits for D2-D4, but D4 (SPEC:244) lists auggie-review `--post-pr` and task `commit`/`push`, whose rows are in P2 (SPEC:100, SPEC:121, SPEC:160). Section 9 (SPEC:225) softens this by letting phases proceed "on the recommendations". Recommendation: say that P1-P3 proceed on the recommended answers and are re-opened if the user chooses otherwise. Priority Low. Quality impact: Clarity +0.5.

**F22. Existing contract status vocabularies were never inventoried.** Severity MINOR, not blocking (the values are UNVERIFIED). Expert: Adzic. Spec: WC-4 and the decision at SPEC:262.
Issue: WC-4 says commands that already write a contract "keep their fields and add the missing ones" (SPEC:62) while the decision fixes `status` to `succeeded / partial / failed / blocked` (SPEC:262), and the live check asserts exactly that set (SPEC:183). The inventories note that workflow, reflect, brainstorm and adversarial already write a `status` (INV-B:272, INV-B:112, INV-A:39, INV-A:35) but never list its values. If any existing value differs, "keep their fields" and the fixed set collide. This is the GAP row G2-5 and also appears in finding 12. Recommendation: list each existing `status` value in section 3.1 or say that the field is renamed. Priority Medium. Quality impact: Consistency +0.5.

**F23. Brainstorm is rated "ready" without noting that unattended it answers its own questions.** Severity MINOR, not blocking. Expert: Cockburn. Spec: section 3.1 brainstorm.
Issue: the inventory records that the non-interactive Socratic dialogue "answers its own questions using best-available context" (INV-A:39). The spec's row (SPEC:84) lists "None" as the small fix and says nothing about it, yet a coordinator receiving a merged requirements document may take invented stakeholder answers for real ones. Recommendation: add one line to the brainstorm row, or have the contract record "dialogue auto-answered: true". Priority Low. Quality impact: Completeness +0.5.

=== ARCHITECTURE ANALYSIS ===

**F5. The spec never says how a worker starts the command.** Severity MAJOR, blocking (concrete wrong outcome below). Expert: Fowler (interface and boundary), Newman (contract between coordinator and unit of work). Spec: section 1.1, WC-7, section 2.3, AC-0.4, evidence E3.
Issue: the whole design rests on "one worker runs one command" (SPEC:16). The brief carries "the exact command line" (SPEC:73) and WC-7 says the worker "runs the command directly in its own session" (SPEC:65), but the worker's first message is Orca's preamble, with the Task text inside it (`CAPS:47` says Claude gets its task on the command line). A slash command written inside a larger message is, to the best of my knowledge, not expanded by Claude Code; that point is UNVERIFIED here. The only prior proof is ambiguous: the PR #329 brief told workers to run `/sc:adversarial` through an Agent-tool subagent (SPEC:43), while the contract says `invocation_method: "skill-direct"` (SPEC:23). The spec records the contradiction as evidence gap 1 but gives the brief template no instruction. AC-0.4 checks that no Agent wrapper was used and that `AskUserQuestion` never appears (SPEC:184, SPEC:194), not that the command's own skill was loaded.
Concrete wrong outcome: a worker reads "run /sc:troubleshoot ..." as prose and improvises the protocol from memory, which is what the repo's own slash-command rule exists to prevent. The run still ends with a plausible report.
Recommendation: add to section 2.3 the exact invocation the brief must use (for example the Skill tool with the command's skill name and arguments) and add to AC-0.4 a transcript check that the skill was loaded before any output. Priority High. Quality impact: Completeness +1.

**F6. No version or capability check, and no behavior for commands that will never support `--unattended`.** Severity MAJOR, blocking (FR-8 GAP row G1-6). Expert: Newman (backward compatibility and versioning). Spec: section 2.1, section 4, section 6 P1, section 2.3.
Issue: commands install to other projects at whatever version is there (SPEC:34). A coordinator that passes `--unattended` to an older install gets a command that does not know the flag; slash-command arguments are free text, so the command runs attended and prompts, which is the silent stall WC-2 exists to prevent. Likewise section 4 says the six coordinator-only commands "get no `--unattended` mode" (SPEC:128) but not what happens if the flag is passed. Nothing in section 2.3 or section 7 tells the coordinator to confirm support first (for example that `~/.claude/WORKER-CONTRACT.md` exists and that the command's file contains the mode section).
Concrete wrong outcome: a worker dispatched to a project with the pre-change install stalls on `AskUserQuestion` and the coordinator sees `agentWait` only after the fact.
Recommendation: add a pre-dispatch support check to section 2.3 and a required refusal line for section-4 commands. Priority High. Quality impact: Completeness +1.

**F7. No rule that `--unattended` reaches nested skills and commands.** Severity MAJOR, blocking (FR-8 GAP row G4-5). Expert: Hohpe (message and control flow between components). Spec: WC-2, section 3, tasklist row.
Issue: only tasklist is told to pass `--unattended` to the reflect runs it starts (SPEC:122). Other chains that carry gates are not covered: tdd runs a nested `/task` that "asks the user" (the tdd row names this, SPEC:90); task calls troubleshoot (INV-B:201); cli-eval create runs `/sc:spec-panel` and adversarial (INV-A:44); release-split runs brainstorm and adversarial (INV-B:121); workflow runs reflect (INV-B:271). WC-2 says the command "never" asks (SPEC:60), but a command cannot keep that promise for a skill it calls unless the mode is handed on.
Concrete wrong outcome: `/sc:cli-eval create --unattended` reaches Wave 2, `/sc:spec-panel` asks for a target release, and the worker stalls although the top command was converted.
Recommendation: add a WC rule that every nested skill or command invocation inside an unattended command passes `--unattended` (or its documented equivalent) and that a callee without the mode is listed in that command's row. Priority High. Quality impact: Consistency +1.

**F8. The additive-edit check AC-C5 (and AC-0.3) is wrong in both directions.** Severity MAJOR, blocking (concrete wrong outcome below). Expert: Crispin (check validity). Spec: section 7.1 AC-C5, section 7.3 AC-0.3, SA-4.
Issue: the check is `git diff -U0 ... | grep -E '^-[^-]'` and "prints nothing" means additive (SPEC:176, SPEC:193). I ran it on sample diff lines: a removed list item appears in a diff as `-- text` and is not matched, a removed frontmatter fence `---` is not matched, and a removed prose line `-text` is matched. Most lines in these command files are list items or frontmatter, so deleted bullets pass the check. In the other direction, adding `--unattended` to an existing Usage line or `argument-hint` removes and re-adds that line, so it would fail the check, yet SA-4 permits changed existing lines only where section 3 names a defect fix (SPEC:149), and only load's usage line is named. The flag therefore cannot be documented in the place `/sc:help` reads without breaking a gate.
Concrete wrong outcome: an implementer deletes a "Will Not" bullet from a command and AC-C5 reports success.
Recommendation: replace the pattern with `grep '^-' | grep -v '^---'` on the diff body (excluding only the `--- a/path` file header), and add the Usage and `argument-hint` lines to the permitted-change list in SA-4. Priority High. Quality impact: Testability +2.

**F9. AC-C1 contradicts the spec's own P0 deliverables and exception.** Severity MAJOR, blocking (concrete wrong outcome below). Expert: Fowler. Spec: section 7.1 AC-C1, SA-2, section 6 P0.
Issue: AC-C1 scans `src/superclaude/core` (and commands, skills, agents) for `orca orchestration|worktree|terminal|agent` and requires no output (SPEC:172). SA-2 allows Orca to be mentioned "inside the contract file" as an example of a caller's question channel (SPEC:147), and P0 puts the contract file in `src/superclaude/core/WORKER-CONTRACT.md` and adds an Orca section to `HOW-WE-WORK.md`, also in `core` (SPEC:158). The routing guide section and the contract's `ask` example will naturally write `orca orchestration ask`, so the check fails on the first phase's own output. Separately, as written in the raw markdown the alternation uses `\|`, which is a literal pipe in `grep -E`: I ran it and `orca orchestration ask` is not matched, so the check passes vacuously if copied from source (the table escape is only correct if the cell is rendered first).
Concrete wrong outcome: either P0 fails its own common check, or the implementer strips every Orca verb from the contract and routing guide and the coordinator brief template loses the commands it needs.
Recommendation: exclude `core/WORKER-CONTRACT.md` and the Orca section from the scan (or scan only commands, skills and agents), and state the pattern in a code block with plain pipes. Priority High. Quality impact: Testability +1.

**F16. P0 builds before it tests, against its own stated reason.** Severity MINOR, not blocking. Expert: Fowler. Spec: section 6 P0.
Issue: the "why this order" cell says the smoke runs "test the decision before anything is built on it" (SPEC:158), but the same cell lists writing the contract, registering it in `KNOWN_CORE_FILES`, editing the routing guide and its two mirrors, and adding the test file, then "Then run three ready commands". AC-0.4 says a failure "reopens section 1" (SPEC:194), by which time the guide text and install list are already changed. Recommendation: split P0 into P0a (smoke runs, no edits) and P0b (contract file, registration, guide). Priority Medium. Quality impact: Clarity +0.5.

**F17. The tasklist nesting claim is stated as fact but is UNVERIFIED in the inventory.** Severity MINOR, not blocking. Expert: Newman. Spec: section 3.2 tasklist row.
Issue: SPEC:122 says the reflect fan-out "runs one layer below the worker, inside Claude Code's nesting limit" citing INV-A:14. But the inventory states that tasklist Stage 10.5 runs reflect inside N subagents, that reflect itself spawns agents, and that whether this nested spawning works is UNVERIFIED (INV-B:210, INV-B:314, INV-B:322). Tier-2 reflect adds reviewers merged through the adversarial protocol, which spawns advocates, so the stack can reach the three-layer limit quoted at INV-A:14. Recommendation: mark the claim UNVERIFIED and add it to the spec's UNVERIFIED list. Priority Low. Quality impact: Consistency +0.5.

**F18. Mapping `partial` to `succeeded` unblocks dependent Tasks without a stated coordinator step.** Severity MINOR, not blocking. Expert: Hohpe. Spec: WC-5, decisions row "`partial` maps to `succeeded`".
Issue: a `succeeded` report makes dependents appear in `task-list --ready` (CAPS:85-86), while a failed Task keeps them blocked (CAPS:90). Orca does not start Tasks by itself (CAPS:92), and section 2.3 has the coordinator open the report after `worker_done` (SPEC:73), so the risk is small. But 2.3 never says "check `status` before starting dependents", and the decision row (SPEC:263) justifies `partial` by the usable deliverable, not by this effect. Recommendation: add one sentence to 2.3. Priority Low. Quality impact: Completeness +0.5.

**F20. AC-1.3 asks for a scratch worktree.** Severity MINOR, not blocking. Expert: Crispin. Spec: AC-1.3.
Issue: the check runs a plain session "in a scratch worktree" (SPEC:197). The repository rule, quoted in the session instructions rather than in any file in this workspace (so UNVERIFIED here), allows project worktrees only through Orca with an agent, with narrow exceptions for internal temporary checkouts. Recommendation: say "in a temporary copy of the repository (not a project worktree)" or run it in the coordinator's worktree and clean up. Priority Low. Quality impact: Clarity +0.2.

**F21. AC-2.4 counts only the first page of reviews and comments.** Severity MINOR, not blocking. Expert: Crispin. Spec: AC-2.4.
Issue: `gh api .../reviews --jq length` returns the length of one page (30 by default), so on a PR with more than 30 comments the "unchanged" test cannot detect a new comment (SPEC:202). Recommendation: add `--paginate` or compare the newest id before and after. Priority Low. Quality impact: Testability +0.3.

**F24. No coordinator branch for a worker that ends without `worker_done` or without a report.** Severity MINOR, not blocking. Expert: Nygard (failure modes and recovery). Spec: section 2.3, WC-4, WC-5.
Issue: section 2.3 describes the coordinator only "after `worker_done`" (SPEC:73). WC-4 writes the report "on every outcome", but a worker that is killed, runs out of context or loses its terminal cannot write one, and WC-5 covers only a worker that does send `worker_done` (SPEC:63). The capabilities inventory already lists the positive proofs of a stall and warns that silence never authorizes stop, abandon, retry or release (CAPS:125-126). Recommendation: add two sentences to 2.3 pointing the coordinator at that recovery path and saying a missing or stale contract is never read as an outcome. Priority Medium. Quality impact: Completeness +0.5.

=== ADVERSARIAL ANALYSIS (Whittaker) ===

Whittaker scope: specification correctness only; resilience patterns and test strategy are left to Nygard and Crispin. Attacks below used the five methodologies; the Guard Condition Boundary Table above carries the zero/empty, sentinel and divergence probes row by row.

**F2. I can break this specification by Sequence Attack.** The invariant at **section 6 P1 versus section 3 rows (SPEC:159 against SPEC:99-125)** fails when **a command accepts `--unattended` in a phase before its gate rows are converted.** Severity MAJOR, blocking (concrete attack below). Expert: Whittaker.
Concrete attack: before P1, `/sc:auggie-review <PR> --unattended` is an unknown token. P1 says "the `--unattended` flag accepted by every command in sections 3.1 and 3.2 (a no-op where a command has no gate)" (SPEC:159). auggie-review has a gate and a posting default, and its row is delivered in P2 (SPEC:100, SPEC:160). State trace: after P1 the flag is accepted, the row's "implies `--no-post-pr` and `--no-remediation-offer`" does not exist yet, so a coordinator that was told by P0's brief template to pass `--unattended` gets `gh pr review --comment` posted to GitHub and then a plain-chat remediation offer that stalls. The same holds for cleanup, improve, task (commit/push default), cli-eval and every other P2-P4 command, and the stall is silent (CAPS:52, CAPS:129). The spec's own invariant "no outward action unless authorized" (WC-9) is broken by its phase order.
Recommendation: restrict P1 so that a command accepts `--unattended` only in the phase that also converts its gates, or make a command with an unconverted gate refuse the flag, and say which. Priority High. Quality impact: Consistency +1.

**F3. I can break this specification by Sequence Attack and Accumulation Attack on retries.** The invariant at **WC-4 "known before dispatch" with WC-6 "fresh output directory" (SPEC:62, SPEC:64, SPEC:73)** fails when **a retry worker reuses the first attempt's Task.** Severity MAJOR, blocking (FR-8 GAP row G2-6). Expert: Whittaker.
Concrete attack: the coordinator creates Task T with `--output .dev/x/run1/`. Attempt 1 (dispatch D1) writes `run1/return-contract.yaml` with `status: failed` and later dies. The coordinator starts `worker-start --task T --retry-of D1` (CAPS:116). Before: `run1/` holds the old contract. Attempt 2 reuses the same Task text, so the same directory; it crashes before writing. After: `run1/return-contract.yaml` still says `failed` (or `succeeded` from an earlier success when a retry is requested for a different reason) and the coordinator reads a stale outcome. For commands with no resume flag WC-6 prescribes a "fresh output directory", but that directory is part of the Task spec and is fixed (SPEC:73); the spec never says the coordinator may change it for a retry, and whether it can is UNVERIFIED (not in CAPS). Commands with fixed output (cleanup-audit `.claude-audit/`, index-repo `PROJECT_INDEX.md`, init-lite, SPEC:85-87) cannot take a fresh directory at all.
Recommendation: require each unattended command to delete or overwrite its contract with `status: running` before doing anything else, state how the coordinator gives a retry a new output path (a new Task or a changed brief), and list the fixed-output commands as "one attempt at a time per worktree". Priority High. Quality impact: Testability +1.

**F10. I can break this specification by Divergence Attack on the wait thresholds.** The invariant at **WC-10 (SPEC:68) against the decision row (SPEC:266) and AC-4.3 (SPEC:210)** fails when **a single call lasts between 4 and 5 minutes, or is a parallel Agent-tool batch.** Severity MAJOR, blocking (FR-8 GAP rows G3-4 and G3-5). Expert: Whittaker, with Nygard.
Concrete attack: WC-10 requires a split only for a call "longer than 5 minutes", into waits "of at most 4 minutes". Take a poll iteration of 4.5 minutes: WC-10 says no split is needed; the decision row says 4 minutes is the maximum (margin below the 5-minute cadence); AC-4.3 says "no single tool call exceeds 240 s" and fails. Second attack: cleanup-audit runs waves of 7-8 concurrent Task agents (INV-A:42), tdd runs 2-10 research agents (INV-B:47), post-release runs scanner teams (INV-B:81). While such a batch runs, the top-level session is blocked in one tool call for longer than 5 minutes and cannot send the heartbeat WC-10 demands; the batch cannot be cut into 4-minute waits, and E4 says fan-out stays as it is (SPEC:24). The 5-minute cadence itself comes from this dispatch's preamble only, and whether Orca uses heartbeat age at all is UNVERIFIED (CAPS:130), so the requirement may be both unsatisfiable and unnecessary.
Recommendation: use one number everywhere (240 s), state that Agent-tool batches are exempt from WC-10, and say what the coordinator does with a long silent but healthy worker (the existing rule: silence alone authorizes nothing, CAPS:125). Priority Medium. Quality impact: Consistency +1.

**F11. I can break this specification by Zero/Empty Attack and Sentinel Collision Attack on the switch.** The invariant at **section 2.1 and D1(a) (SPEC:51, SPEC:227-230)** fails when **the flag is given without an output location, together with a person-mode flag, or only as text inside a quoted argument.** Severity MAJOR, blocking (FR-8 GAP rows G1-2, G1-4, G1-5). Expert: Whittaker.
Concrete attack: (1) `/sc:analyze src --unattended` with the new output flag omitted: WC-4 needs `<output-dir>`, the analyze row says only "add `--output`" (SPEC:99); the run either writes nothing the coordinator can find or invents a path. (2) `/sc:adversarial a.md b.md --unattended --interactive`: the brief "never" passes `--interactive` (SPEC:83) but nothing makes the command refuse; four `AskUserQuestion` checkpoints (INV-A:35) fire in a worker. (3) `/sc:tdd "document the --unattended flag"`: if the command matches the substring it switches mode for a person; `command.md` shows the intended rule (a standalone argument token outside any quoted argument, CMD:455) which this spec lacks. D1(a) is called "testable by grep and cannot misfire on a person" (SPEC:228), and case (3) is the misfire.
Recommendation: add to WC-2 or section 2.1: the switch is recognized only as a standalone unquoted argument; `--unattended` without the output location the command needs is refused with a written report if a report directory is known, otherwise in chat; and the person-mode flags are refused for every command, not just the rows that happen to say so. Priority High. Quality impact: Completeness +1.

**F12. I can break this specification by Zero/Empty Attack and Sentinel Collision Attack on the report.** The invariant at **WC-4 and WC-5 (SPEC:62-63) and the check at SPEC:183** fails when **the report exists but is empty, unparseable, blocked without a question, or uses a status value outside the fixed set.** Severity MAJOR, blocking (FR-8 GAP rows G2-2, G2-4, G2-5). Expert: Whittaker.
Concrete attack: the command crashes while writing and leaves a zero-byte `return-contract.yaml`. WC-5 sends `--outcome failed` only if "no report exists" (SPEC:63); the file exists, so the rule gives no answer. Second: `status: blocked` with an empty `blocked_question`; WC-4 requires the field "when blocked" but gives no non-empty rule, and only AC-2.2 asserts one (SPEC:200). Third: an existing contract that already uses another status word (finding 22) makes the assertion at SPEC:183 fail on a healthy run.
Recommendation: in WC-5 replace "no report exists" by "no parseable report with a `status` in the fixed set and, if blocked, a non-empty question", and move the non-empty-question assertion into the common live check (7.2 step 4). Priority High. Quality impact: Testability +1.

**F14. I can break this specification by Divergence Attack on gate resolution.** The invariant at **WC-2 (SPEC:60)** fails when **several gates block one run, or a caller flag and a documented default disagree.** Severity MAJOR, blocking (FR-8 GAP rows G5-4 and G5-5). Expert: Whittaker.
Concrete attack: `/sc:cli-eval run --unattended` with no `--suite`: the suite menu, the safety-flag confirmation and the W0 "confirm with the user" are three gates (INV-A:44, SPEC:104). The contract has a single `blocked_question`, so the coordinator answers one, re-invokes, and meets the next; with no resume ("fresh dir", SPEC:104) each round restarts from zero. For precedence: research pins `--strategy planning` as the documented default (SPEC:116) and the caller passes `--strategy intent`; WC-2 lists "(a) a documented default; (b) a value the caller supplied" with no order, so an implementer may let the default win and ignore the caller.
Recommendation: state precedence (caller flag, then documented default, then blocked) and let `blocked_question` hold a list of all unresolved gates found at the point of stopping. Priority Medium. Quality impact: Completeness +1.

=== CONSENSUS AND DISAGREEMENTS ===

Consensus points:
- The central decision, the rejected alternative and the honest statement of evidence gaps (section 1.4) are the strongest parts of the spec. No expert asks to reopen the decision.
- The decisive weaknesses are in the mechanisms that make the decision usable: where the report goes (F4, F3, F12), how the switch is recognized and passed on (F11, F6, F7), how the worker starts the command (F5), and whether the acceptance checks can pass or detect failure (F1, F8, F9).
- Phases and checks need to be reconciled with section 3 before the phases can be gated on them (F1, F2, F16).

Disagreements:
- Nygard would also require a heartbeat rule for fan-out batches; Whittaker argues the heartbeat rule should be dropped if Orca does not use heartbeat age (UNVERIFIED, CAPS:130). Left as finding 10 with both options.
- Wiegers wants the F15 traceability table to be mandatory; Crispin would accept the test file alone. Graded minor, so it does not block.

Positive checks (nothing to fix): the 10 / 27 / 6 split re-counts correctly from the rows; the phase column of section 3 sums to the P1-P4 lists; the inventory citations I spot-checked match; the open decisions D1-D5 each carry options and a recommendation; Decisions and UNVERIFIED sections exist as the README requires (README:36, README:32).

## Numbered findings list

Path expansion for the Evidence column: `SPEC:N` = `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md:N`; `INV-A:N` = `.dev/orca-command-refactor/inventory/commands-a.md:N`; `INV-B:N` = `.dev/orca-command-refactor/inventory/commands-b.md:N`; `CAPS:N` = `.dev/orca-command-refactor/inventory/orca-capabilities.md:N`; `README:N` = `.dev/orca-command-refactor/README.md:N`; `CMD:N` = `command.md:N` in the review sandbox. Findings 5 and 20 also rest on instructions not present in the workspace (UNVERIFIED).

| # | Finding | Severity | Blocking | Spec section | Evidence path:line |
|---|---|---|---|---|---|
| 1 | AC-1.1 and the P1 scope count 37 commands with a contract section, but load has no contract, pr-submit leaves the worker set under recommended D3(a), and three commands wait for P4 (37 expected, 33 writable) | CRITICAL | yes | 6 P1; 7.3 AC-1.1; 3.2; 4; 9 D3 | SPEC:112, SPEC:139, SPEC:154, SPEC:159, SPEC:162, SPEC:195, SPEC:240-242, SPEC:265 |
| 2 | P1 makes commands accept `--unattended` before their gate rows exist (P2-P4), so a coordinator's flag is accepted while posting and prompts still happen | MAJOR | yes | 6 P1 vs 3.2 | SPEC:100, SPEC:159, SPEC:160, CAPS:52, CAPS:129 |
| 3 | Retry reuses the Task and its fixed output directory; WC-6 "fresh dir" conflicts with WC-4 "known before dispatch"; a stale contract can be read as the retry's outcome; fixed-output commands cannot take a fresh dir | MAJOR | yes (FR-8 GAP G2-6) | 2.2 WC-4, WC-6; 2.3; 3.1 | SPEC:62, SPEC:64, SPEC:73, SPEC:85-87, CAPS:116 |
| 4 | WC-4 contract placement does not fit file-valued `--output`, adversarial's subdirectory, workflow's generated id and pre-creation STOP, or troubleshoot's conditional contract | MAJOR | yes | 2.2 WC-4; 3.1; 7.2 step 4; AC-2.2 | SPEC:62, SPEC:73, SPEC:83, SPEC:87, SPEC:90-92, SPEC:99, SPEC:120, SPEC:200, INV-B:242, CMD:456 |
| 5 | The spec never says how the worker starts the command (Skill tool versus text in the preamble); evidence E3 is internally ambiguous; AC-0.4 does not check that the skill loaded | MAJOR | yes | 1.1; 2.2 WC-7; 2.3; AC-0.4; E3 | SPEC:16, SPEC:23, SPEC:43, SPEC:65, SPEC:73, SPEC:184, SPEC:194, CAPS:47 |
| 6 | No version or capability check before dispatch, and no defined behavior for section-4 commands or older installs given `--unattended` | MAJOR | yes (FR-8 GAP G1-6) | 2.1; 2.3; 4; 6 P1 | SPEC:34, SPEC:73, SPEC:128, SPEC:132-137, SPEC:159 |
| 7 | No rule that `--unattended` is passed to nested skills and commands; only tasklist to reflect is specified | MAJOR | yes (FR-8 GAP G4-5) | 2.2 WC-2; 3.1; 3.2 | SPEC:60, SPEC:90, SPEC:104, SPEC:122, INV-B:121, INV-B:201, INV-B:271, INV-A:44 |
| 8 | AC-C5 and AC-0.3 regex `^-[^-]` misses deleted bullets and frontmatter fences, and wrongly fails a Usage-line edit that SA-4 does not permit | MAJOR | yes | 7.1 AC-C5; 7.3 AC-0.3; 5 SA-4 | SPEC:149, SPEC:176, SPEC:193 |
| 9 | AC-C1 scans `core/` where P0 puts the contract and the routing-guide Orca section, contradicting SA-2; the escaped `\|` is a literal pipe in `grep -E` | MAJOR | yes | 7.1 AC-C1; 5 SA-2; 6 P0 | SPEC:25, SPEC:147, SPEC:158, SPEC:172 |
| 10 | WC-10 threshold (over 5 min, waits of at most 4) disagrees with AC-4.3 (240 s); a 4.5-minute call passes one and fails the other; parallel agent batches cannot be split; the 5-minute heartbeat has no verified effect | MAJOR | yes (FR-8 GAP G3-4, G3-5) | 2.2 WC-10; 7.3 AC-4.3; Decisions | SPEC:24, SPEC:68, SPEC:210, SPEC:266, INV-A:42, INV-B:47, INV-B:81, CAPS:130 |
| 11 | `--unattended` semantics are open: no output location, combination with person-mode flags on ready commands, and the token appearing inside a quoted argument | MAJOR | yes (FR-8 GAP G1-2, G1-4, G1-5) | 2.1; 2.2 WC-2, WC-4; D1 | SPEC:51, SPEC:83, SPEC:99, SPEC:227-230, INV-A:35, CMD:455 |
| 12 | WC-5 treats only a missing report as failure; empty or unparseable files, blocked without a question, and out-of-set status values are unspecified | MAJOR | yes (FR-8 GAP G2-2, G2-4, G2-5) | 2.2 WC-4, WC-5; 7.2 step 4 | SPEC:62, SPEC:63, SPEC:183, SPEC:200 |
| 13 | WC-9 and D4 require the coordinator to quote the user, which no command can check; post-release has four outward actions and one unnamed flag | MAJOR | yes (FR-8 GAP G4-2, G4-4) | 2.2 WC-9; 3.2 post-release; 9 D4 | SPEC:67, SPEC:113, SPEC:244-247 |
| 14 | WC-2 lists default, flag and blocked with no precedence, and one `blocked_question` for runs with several gates (cli-portify three, cli-eval three) | MAJOR | yes (FR-8 GAP G5-4, G5-5) | 2.2 WC-2; 3.2 cli-eval, cli-portify | SPEC:60, SPEC:104, SPEC:105, SPEC:116, INV-A:44, INV-A:45 |
| 15 | WC-1, WC-3 and WC-12 have no phase owner or acceptance check; WC-1 says "well inside" the limit without a number | MAJOR graded minor | no | 2.2; 6; 7 | SPEC:59, SPEC:61, SPEC:70, SPEC:180, SPEC:184, CAPS:49 |
| 16 | P0 says its smoke runs come before anything is built, but its cell lists the edits first | MINOR | no | 6 P0 | SPEC:158, SPEC:194 |
| 17 | Tasklist reflect "inside the nesting limit" is asserted while the inventory marks nested spawning UNVERIFIED | MINOR | no | 3.2 tasklist | SPEC:122, INV-A:14, INV-B:210, INV-B:314, INV-B:322 |
| 18 | `partial` mapped to `succeeded` makes dependents appear ready; section 2.3 has no "check status before starting dependents" step | MINOR | no | 2.2 WC-5; Decisions | SPEC:63, SPEC:73, SPEC:263, CAPS:85-86, CAPS:90, CAPS:92 |
| 19 | "Phases 1-3 need no user decision" while D4 covers P2 rows (auggie-review, task) | MINOR | no | 6 intro; 9 D4 | SPEC:100, SPEC:121, SPEC:154, SPEC:160, SPEC:244 |
| 20 | AC-1.3 runs in a "scratch worktree", which the repository's Orca-only worktree rule (UNVERIFIED here) does not allow | MINOR | no | 7.3 AC-1.3 | SPEC:197 |
| 21 | AC-2.4 `--jq length` reads one page (30) of reviews and comments | MINOR | no | 7.3 AC-2.4 | SPEC:202 |
| 22 | Existing contract `status` vocabularies were never inventoried; "keep their fields" and the fixed set may collide | MINOR | no | 2.2 WC-4; Decisions | SPEC:62, SPEC:183, SPEC:262, INV-A:35, INV-A:39, INV-B:112, INV-B:272 |
| 23 | Brainstorm is rated ready with no note that unattended it answers its own Socratic questions | MINOR | no | 3.1 brainstorm | SPEC:84, INV-A:39 |
| 24 | No coordinator branch for a worker that ends without `worker_done` or without a report | MINOR | no | 2.3; 2.2 WC-4, WC-5 | SPEC:62, SPEC:63, SPEC:73, CAPS:125-126 |

Totals: 1 CRITICAL, 13 MAJOR blocking, 1 MAJOR graded minor, 9 MINOR. Blocking findings open: 1 to 14.

Reviser brief

Blocking finding ids: 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14. Findings 15 to 24 are notes and never trigger a revision. The reviser reads this report, not the command, so the rules are restated here. Revise only text a blocking finding names. Add no rule, mechanism or section that no blocking finding calls for. Each added paragraph or table cites its finding id. The reviser reports the byte size of the spec before and after. A brief may narrow this scope but may not widen it past the changed lines and the prior blocking findings, and may not grade a minor finding as blocking. At most 2 fix cycles remain (this is review 1 of 3); at review 3 with a FAIL verdict the run escalates to the user instead of revising.

verdict: FAIL

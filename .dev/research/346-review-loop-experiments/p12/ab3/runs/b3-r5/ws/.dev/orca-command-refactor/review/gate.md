review: 1 of 3

# Gate review: Orca worker contract spec

| Field | Value |
|---|---|
| Command | `/sc:spec-panel @.dev/orca-command-refactor/specs/orca-worker-contract-spec.md --mode critique --focus requirements,architecture` |
| Review kind | GATE review (first review of a complete document, no prior rounds; numbers its own loop `review: 1 of 3`) |
| Prompt followed | GATE prompt and FIRST-REVIEW grading check, `~/.claude/rules/prompts/document_review_loop_prompts.md:57-64` and `:35-36`, read in full before reviewing |
| Candidate | `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md` |
| Candidate sha256 | `a836576df87b59b039072268c20705696ba11a57c7fd7ec19d1e677d12268487` |
| Baseline / prior report | none given (first review, not `--re-review`); no `baseline: missing` applies |
| Reviewer model | `claude-sonnet-5-5` (Sonnet 5.5) |
| Date | 2026-11-10 |
| Citation notation | `SPEC:N` = line N of the candidate. `INV-A:N`, `INV-B:N`, `CAPS:N` = lines of `inventory/commands-a.md`, `commands-b.md`, `orca-capabilities.md`. `README:N` = `.dev/orca-command-refactor/README.md`. |
| Evidence limit | Only the five files under `.dev/orca-command-refactor/` and the prompt file were readable. Every `cmd/`, `sk/`, `CLAUDE.md`, `HOW-WE-WORK.md`, `EVIDENCE.md`, codegraph-migration and Orca-source citation is UNVERIFIED here (checkable only through the inventory line that quotes it). |

## Verdict summary

1 blocking finding (B-01), 13 Medium warnings and 7 minor notes. The spec's decision (Orca coordinates, commands stay units of work) is well supported and honest about its evidence gaps (`SPEC:41-45`). The blocker is one contradiction in the central worker contract: the path of the report file a coordinator is told to open.

Counts and cross-reference checks that passed:
- 21 + 22 = 43 commands, split 5+5 ready, 13+14 needs-change, 3+3 coordinator-only = 10 / 27 / 6 (`INV-A:73`, `INV-B:278`, `SPEC:76`). The 27 rows of section 3.2 and the 6 rows of section 4 were counted and match.
- Phase coverage conserves: P1 13 (9 in 3.2 + 4 fixes in 3.1), P2 15, P3 4, P4 3, unchanged 2 (brainstorm, init-lite), coordinator-only 6 = 43 (`SPEC:159-162`).
- All sampled `INV-A:N`, `INV-B:N` and `CAPS:N` cites in the spec point at text that supports the claim (about 60 checked, including every per-command evidence cite in sections 3 and 4, E1 to E6, R1 to R5, and UNVERIFIED items 1 to 13).

## Mandatory artifacts

### Guard Condition Boundary Table

Guards are the spec's conditional rules. Classes that cannot occur for a guard are left out with a one-line reason under the table. Status GAP rows are graded under FR-8/FR-9: a GAP is blocking only if it names a concrete wrong outcome or a security, data-loss or safety-boundary risk; otherwise Medium (`follow-up candidates`). None of the GAP rows below is graded blocking on its own; B-01 comes from the document's stated texts, not from this table.

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|---|---|---|---|---|---|---|
| `--unattended` switch | WC-2, D1 (`SPEC:60`, `:227-230`) | Zero/Empty | flag absent | false | today's behaviour, SA-1 (`SPEC:146`) | OK |
| `--unattended` switch | WC-4, §2.3 (`SPEC:62`, `:73`) | One/Minimal | flag present, no output dir passed | true | unspecified (WC-4 defines the contract path only from a coordinator-passed dir) | GAP (M-11) |
| `--unattended` switch | D1 (`SPEC:228`) | Sentinel Value Match | the token inside quoted user content, e.g. `/sc:tdd "x --unattended"` | ambiguous | unspecified; D1 claims it "cannot misfire on a person" | GAP (M-11) |
| `--unattended` switch | §2.3 vs §4 and §3.1 (`SPEC:73`, `:128`, `:84`, `:87`) | Legitimate Edge Case | flag passed to a command with no unattended section (brainstorm, init-lite, a section-4 command) | unspecified | §2.3 says always pass it; §4 says section-4 commands get no mode; §3.1 lists no flag for brainstorm or init-lite | GAP (M-06) |
| Outcome mapping | WC-5 (`SPEC:63`) | Zero/Empty | no report exists | true | `--outcome failed` | OK |
| Outcome mapping | WC-5 | Typical | `status: succeeded` / `failed` | true | succeeded / failed | OK |
| Outcome mapping | WC-5, Decisions (`SPEC:63`, `:263`) | Legitimate Edge Case | `partial`, `blocked`, audit verdict FAIL | true | succeeded, failed, succeeded | OK |
| Outcome mapping | WC-4 (`SPEC:62`) | Sentinel Value Match | existing contract whose own `status` vocabulary differs (workflow, `INV-B:272`) | unspecified | "keep their fields and add the missing ones" but no mapping for a foreign status value or an unparseable file | GAP (M-13) |
| Wait size | WC-10 (`SPEC:68`) | Typical | one call of 3 minutes | false | no split needed | OK |
| Wait size | WC-10 | Legitimate Edge Case | one call of 4.5 minutes | false (trigger is "longer than 5") | allowed by the trigger, but the cap for split waits is 4 minutes, and the heartbeat is every 5 minutes | GAP (M-04, minor part) |
| Wait size | WC-10 vs WC-7 (`SPEC:68`, `:65`) | Maximum/Overflow | foreground Agent-tool fan-out lasting over 5 minutes | true | cannot be split; WC-7 says fan-out "stays as it is" | GAP (M-04) |
| Resume flag | WC-6 (`SPEC:64`) | Zero/Empty | retry worker, same output dir, resume flag not passed (roadmap: "starts fresh", `SPEC:205`) | false | not specified; WC-6 only covers commands with no resume flag | GAP (M-05) |
| Resume flag | WC-6 | Typical | flag passed, state present | true | resumes | OK |
| Outward action | WC-9 (`SPEC:67`) | Zero/Empty | no authorizing flag | false | action off | OK |
| Outward action | WC-9, D4 (`SPEC:67`, `:244-247`) | Typical | explicit flag in the brief (auggie-review `--post-pr`) | true | on | OK |
| Outward action | WC-9 vs §3.2 task, post-release (`SPEC:113`, `:121`) | Legitimate Edge Case | command has no authorizing flag (task `commit`/`push`, post-release commit and PR) | unspecified | "authorized" is not defined for these; D4 is answered only in P4, task is in P2 | GAP (M-08) |
| Outward action | WC-3 vs WC-9 (`SPEC:61`, `:67`) | Sentinel Value Match | authorization arrives as a coordinator `reply` to a worker `ask` | unspecified | WC-3 lets the answer become a flag; WC-9 says only a flag "written in the brief" | GAP (M-01) |
| `ask` wait | WC-3 (`SPEC:61`) | Typical | timeout | true | resume the same message ID | OK |
| `ask` wait | WC-3 | Maximum/Overflow | coordinator never answers | true | unspecified upper bound (no heartbeat while blocked; `CAPS:64`) | GAP (minor, N-08) |
| Nesting depth | R1, WC-8 (`SPEC:33`, `:66`) | Typical / Edge | depth 1; depth raised (D5 b) | true / true | command never calls `worker-start`/`dispatch`/`task-create` either way | OK |

Left out, with reason: Outcome mapping and Outward action Maximum/Overflow (no capacity is involved); Wait size Zero/Empty (a zero-length wait cannot trigger the guard); Nesting depth One/Minimal and Zero (depth 0 is the coordinator and is not a worker, `CAPS:97`); `ask` One/Minimal (same as Typical).

The table is complete under FR-10; synthesis follows.

### Quantity Flow Diagram (Pipeline Dimensional Analysis)

The only count-bearing pipeline is the classification and phase funnel. The coordinator to worker to report flow is 1 Task to 1 worker to 1 contract by design; retries (`--retry-of`) add dispatches, covered in M-05.

```text
[Source: 43 commands in cmd/ (INV-A:3 =21, INV-B:3 =22)]  (completeness of 43 unchecked: M-10)
   |--> [Classify] --> 10 ready (5+5) | 27 needs-change (13+14) | 6 coordinator-only (3+3)   10+27+6 = 43  OK
   |
   |--> [Phase assignment, SPEC:159-162]
        P0 0 commands edited (3 smoke runs of ready commands)
        P1 13 = 9 (3.2) + 4 (3.1 fixes)      consumer: AC-1.1 asserts all except load -> 12 expected   <-- see M-06
        P2 15 = 11 (3.2) + 4 (3.1: reflect, release-split, tdd, troubleshoot)
        P3 4      P4 3      unchanged 2 (brainstorm, init-lite)      coordinator-only 6
        13+15+4+3+2+6 = 43   conserved
```

No dimensional mismatch found. The one consumer that assumes a different count than the producer states is AC-1.1 (12 asserted of 13, with `load` excepted, while 3.1 says 4 of those 13 only get "small fixes"), recorded as M-06.

## Grading check for the blocking finding

An implementer who follows the stated text as written builds a contract writer that puts `return-contract.yaml` at `<output-dir>/return-contract.yaml` (WC-4, `SPEC:62`), where `<output-dir>` is "the directory the coordinator passed (`--output` / `--output-dir`)", and builds the coordinator checks of section 7.2 (`SPEC:182`) to open exactly that path. For `/sc:adversarial` the same document requires the contract at `<output>/adversarial/return-contract.yaml` (`SPEC:83`, `:198`), and for `/sc:tdd` and `/sc:init-lite` it makes `--output` a file (`SPEC:87`, `:90`, `:200`). X is wrong because the coordinator opens a path where no contract exists (adversarial), no directory exists at all (tdd, init-lite), or no path can be known before dispatch (workflow, whose package id does not exist yet). Each check in 7.2 steps 3 and 4 then fails on a correct implementation of the other text. This holds with no further assumption: it is two stated texts that contradict each other.

## === REQUIREMENTS ANALYSIS ===

Experts: Wiegers (lead), Adzic, Cockburn, with Whittaker's attacks.

### B-01 (BLOCKING) The report-file path is defined three incompatible ways

- Severity: CRITICAL (the specification contradicts itself at its central requirement). Expert: Wiegers, confirmed by Whittaker (Divergence Attack) and Adzic (no single example satisfies all rows). Priority: High.
- Issue. WC-4 says the contract is `<output-dir>/return-contract.yaml`, "where `<output-dir>` is the directory the coordinator passed (`--output` / `--output-dir`)", and section 2.3 says the coordinator passes "the output directory, so the report path is known before dispatch" (`SPEC:62`, `:73`). Three places break that:
  1. `--output` is a file for some commands. tdd: "`--output <file>`" and the report is "the TDD at `--output`" (`SPEC:90`); init-lite: "`--output <file>`" (`SPEC:87`); AC-2.2 runs `/sc:tdd "auth" --unattended --output <file>` and expects a contract with `status: blocked` (`SPEC:200`). `<file>/return-contract.yaml` cannot exist. (The command definition run for this review keeps the two apart: `--output` is file-valued and the contract lives under a separate `--report-dir`, `command.md:460`. This is corroboration only, not evidence the spec cites.)
  2. adversarial. The small fix puts the contract at `<output>/adversarial/return-contract.yaml` (`SPEC:83`; AC-1.4 `SPEC:198`), while the brief passes `--output <dir>` and WC-4 puts it at `<dir>/return-contract.yaml`. The inventory records the same two real locations on disk (`INV-A:35`, `INV-A:60`).
  3. workflow. The contract lives at `.dev/tasks/to-do/<id>/return-contract.yaml` (`SPEC:92`), where `<id>` is created by the command, so it is not known before dispatch; the fix "write the contract for pre-creation STOPs too" names no location, and none can exist because the package directory is not created for those stops (`INV-B:272`: "Not written for pre-creation STOPs"). cleanup-audit has the same shape: a fixed `.claude-audit/` directory and no `--output` (`SPEC:85`, `INV-A:42`).
- Concrete attack (Divergence, state trace). Brief: `/sc:adversarial --compare a.md b.md --output .dev/x/ --unattended`. Coordinator (per 2.3 and 7.2 step 3) expects `.dev/x/return-contract.yaml`. After P1 the command writes `.dev/x/adversarial/return-contract.yaml`. `test -s .dev/x/return-contract.yaml` (7.2 step 4) exits 1; AC-1.2 fails for a correct implementation of 3.1. Repeat for tdd: the coordinator passes a file; there is no directory to hold the contract.
- Recommendation (narrow, do not add a mechanism). Make the contract path a per-command value in the existing "Report (WC-4)" column of section 3 and say in WC-4 and 2.3 that the coordinator computes it from that column; delete the `<output-dir>` generalisation in WC-4. For file-valued `--output` commands (tdd, init-lite) state the exact contract path rule in their rows (for example the file's directory) or take a directory flag. For adversarial keep `<output>/adversarial/`; for workflow and cleanup-audit state where the pre-creation or fixed-directory contract goes and whether the brief supplies it. Make 7.2 step 3 read the path from the same column. Quality impact: removes the defect that makes AC-1.2, AC-2.2 and AC-2.3 unpassable for at least four ready commands; estimated +2 on Testability and +1 on Consistency.

### Medium warnings (requirements)

**M-01 WC-3 lets a coordinator's answer become the command's input, with no carve-out for safety-rule or outward-action gates.** WC-3 says that when a gate would resolve as blocked the worker "may instead ask the coordinator once ... then re-invoke or resume the command with the answer as a flag" (`SPEC:61`). The same document says the `/sc:implement` Ruling must not come from "another agent's message" and recommends keeping that (D2 a, `SPEC:233-236`; `INV-A:66`), and that outward actions turn on only through a flag "written in the brief" (WC-9, `SPEC:67`) and only on the user's own instruction (D4 a, `SPEC:245`). WC-3 is in the P0 contract, before D2 and D4 are answered in P4 (`SPEC:162`). No wrong outcome follows without a guess (the implement Ruling has no answer flag; the outward gates are default-off rather than blocked), so Medium. Expert: Nygard, Whittaker (Sequence Attack: ask, reply, re-invoke). Recommendation: one sentence in WC-3 that gates guarded by a safety rule or an outward-action authorization are never resolved by a coordinator answer unless D2/D4 allow it. Priority: High among follow-ups.

**M-02 `--unattended` has no propagation rule for nested command and skill calls.** The only stated propagation is tasklist Stage 10.5 to reflect (`SPEC:122`). Others the inventories show: roadmap calls `sc:save` at every wave (`INV-B:154`), so two roadmap workers still clobber single-owner memory keys even after the P3 save fix, which applies only to `/sc:save --unattended` (`SPEC:119`); pr-submit runs one `/sc:auggie-review` fallback (`INV-B:91`), and auggie-review posts to GitHub by default with no prompt (`SPEC:100`); cli-eval create runs `/sc:spec-panel` and adversarial (`INV-A:44`); brainstorm and release-split call adversarial and brainstorm. The document never states whether the flag is passed down, so WC-2, WC-9 and WC-11 are unenforced across those calls. Missing requirement, so Medium. Expert: Fowler, Newman (interface contract between composed units). Recommendation: one rule in WC-2 (pass `--unattended` to every nested `/sc:` call a command makes, or list the exceptions per command).

**M-03 The tasklist row reverses its inventory verdict without recording the decision.** `INV-B:215` and `INV-B:295` require that Stage 10.5 drop `--remediate` and that the reflect fan-out run at the worker's top level, and `INV-B:210`, `INV-B:322` mark nested spawning and who answers the offer UNVERIFIED. The spec instead passes `--unattended` to each reflect so "the headless rule applies" and says the fan-out is "inside Claude Code's nesting limit" (`SPEC:122`), with no depth count. The headless rule "auto-accepts for auto-fixable registers and skips the gates" (`INV-B:109`), so each phase now auto-accepts a remediation handoff, an effect on N phases that is not stated, and `needs_human_decision` HALTs (`INV-B:209`) get no resolution under WC-2. The Decisions table says no inventory verdict was changed (`SPEC:268`). Medium: the outcome depends on how the headless rule treats those HALTs, which is not readable here. Expert: Fowler (count divergence N phases), Nygard. Recommendation: record the choice in Decisions, state the nesting depth count, state the `needs_human_decision` resolution, and add the nested-spawn question to the UNVERIFIED list.

**M-04 WC-10 cannot be met by the fan-out WC-7 preserves, and its premise is unverified.** WC-10 requires any command step that blocks one tool call longer than 5 minutes to be "split into waits of at most 4 minutes" (`SPEC:68`); WC-7 keeps each command's Agent-tool fan-out unchanged (`SPEC:65`). A foreground fan-out (tdd, cleanup-audit waves, adversarial, `INV-A:42`) cannot be split. AC-4.3 demands "no single tool call exceeds 240 s" for pr-submit, whose troubleshoot and adversarial fan-out per finding is also a blocking call (`SPEC:210`, `INV-B:91`). The reason for the rule is that heartbeats keep the worker alive, but "whether Orca uses heartbeat age in the liveness verdict" is UNVERIFIED (`CAPS:130`, `CAPS:182`) and that item is missing from the spec's own UNVERIFIED list (`SPEC:271-285`); absence of a heartbeat "never authorizes stop, abandon, retry, or release" (`CAPS:125`). The thresholds also leave a gap: a 4.5-minute call is neither split nor heartbeat-safe. Medium: the harm depends on how Orca treats a late heartbeat. Expert: Nygard, Whittaker (Accumulation). Recommendation: narrow WC-10 to poll and eval waits, add the CAPS:182 item to UNVERIFIED, and align the 5- and 4-minute figures.

**M-05 Retry and re-run semantics conflict with the report path and can overwrite the first attempt.** WC-6 says a command with no resume flag "writes each run into a fresh output directory" (`SPEC:64`), but WC-4 and 2.3 fix the report path before dispatch from the coordinator's directory, so who creates the fresh directory is unstated. For a command that has a resume flag the flag-less case is not covered: AC-3.2 runs roadmap with an existing `.session-memory.md` and no flag and expects it to "start fresh" in the same directory (`SPEC:205`, `SPEC:118`), which silently replaces the first attempt's output on a `--retry-of` re-run with an unchanged brief. Section 2.3 does not say a retry brief must add the resume flag or a new directory. Local-file overwrite, no outward effect, so Medium. Expert: Nygard, Whittaker (Sequence Attack). Recommendation: one sentence in 2.3 that a retry brief names a new output directory or the resume flag, and a clarifying clause in WC-6.

**M-06 The unattended scope for ready commands is stated two ways.** §2.3 says every brief passes `--unattended` (`SPEC:73`); §3.1 says ready commands run "now" with the listed flags, which for brainstorm and init-lite do not include it, and "the only command changes are the small fixes" (`SPEC:79`, `:84`, `:87`); the P1 row says the flag is accepted by adversarial, cleanup-audit, index-repo and workflow, and AC-1.1 asserts an `## Unattended mode` section on all P1 commands except load, which includes those four (`SPEC:159`, `:195`); AC-1.2 runs every P1 command with `--unattended --output <dir>`, but index-repo has no output flag and cleanup-audit a fixed directory (`SPEC:196`, `:85-86`). A reading that makes all of it consistent exists (a "changed command" gains the section, `SPEC:76`) but needs a guess about brainstorm and init-lite. Medium. Expert: Wiegers, Cockburn. Recommendation: one line in 3.1 stating per row whether the command gains `--unattended`, and what the brief passes in the meantime.

**M-07 §1.4 point 2 states an unproven timing as fact.** It says a command's own `AskUserQuestion` "comes after readiness, so it does not fail `worker-start`" (`SPEC:44`). The evidence is a shell-wrapper prompt before Claude's input box (`CAPS:49`) and "waiting is healthy once `input_accepted`" (`CAPS:52`). For Claude the task is passed on the command line (`CAPS:47`), so a command can ask its first question before the readiness check sees a fresh input box; the README states the principle in general terms (`README:13`) and `INV-A:17` repeats it. The design survives either way because AC-2.2 would observe it, but the claim should be UNVERIFIED. Medium. Expert: Nygard. Recommendation: mark it UNVERIFIED and add it to the list at `SPEC:271-285`.

**M-08 "Authorized" has no mechanism for task and post-release, and task is in a phase that precedes D4.** WC-9 turns an outward action on only through "the command's own explicit flag" (`SPEC:67`); the task row refuses `commit`/`push` "unless authorized" and post-release turns VM, install, commit and PR off "unless the brief authorizes them" (`SPEC:113`, `:121`), but neither command has such a flag in the spec. Task is in P2 (`SPEC:160`) while D4 is answered before P4 (`SPEC:162`), yet §6 says P1 to P3 need no decision (`SPEC:154`). A P2 implementer must invent a flag or refuse always. Medium (missing requirement). Expert: Wiegers, Cockburn. Recommendation: state "always refuse until D4" for task in P2, or name the flag.

**M-09 AC-C1 conflicts with the P0 deliverables and SA-2.** AC-C1 greps `src/superclaude/core` as well as commands, skills and agents and must print nothing (`SPEC:172`); P0 adds an Orca section to `HOW-WE-WORK.md` and a new `WORKER-CONTRACT.md`, both under `core/` (`SPEC:158`), while SA-2 allows an Orca mention only "inside the contract file" and speaks only of "command, skill or agent" files (`SPEC:147`). The baseline E5 count was 0 for HOW-WE-WORK (`SPEC:25`). Whether P0 fails depends on whether the new text contains `orca orchestration` or similar lowercase strings. Medium. Expert: Crispin. Recommendation: align the AC-C1 path list or its exclusions with SA-2.

**M-10 The "43 commands" completeness claim is not evidenced.** Each inventory names its scope in a task line (`INV-A:3`, `INV-B:3`); neither records a directory listing of `src/superclaude/commands/`, and the spec states the total as fact (`SPEC:76`). The host session's installed command list also names `/sc:graph`, `/sc:impact` and `/sc:issue`, which appear in neither inventory. That list is not inside the workspace and cannot be checked against this repo state, so this is UNVERIFIED, but if those files exist in `cmd/` the 10/27/6 split and the phase table are short by three. Medium. Recommendation: add the `ls` result to the inventories or a citation for the count.

**M-11 `--unattended` parsing and its missing-output case are undefined.** D1 says the flag "cannot misfire on a person" (`SPEC:228`), but the spec does not say the flag counts only as a standalone argument token. A topic or spec text containing the token (`/sc:tdd "build X --unattended"`) can drop every gate in a person's own session, an SA-1 violation. It also does not say what happens when `--unattended` is passed without an output location, though WC-4 says the contract is "written on every outcome" (`SPEC:62`). The command definition run here resolves both (standalone token outside quotes; refuse in chat when no report directory is known, `command.md:459-460`), as corroboration only. Missing requirement, so Medium. Expert: Whittaker (Sentinel Collision, Zero/Empty). Recommendation: two sentences in section 2.1.

**M-12 §4's "workers make no commits or pushes" contradicts D4 and rests on a run-local rule.** The `/sc:git` row says "workers make no commits or pushes" and cites `README:31` (`SPEC:133`); that README line is a rule for the workers of this planning run, not product policy (`README:29-31`). WC-9 and D4 (a) allow a worker to commit or push when the user's instruction names it (`SPEC:67`, `:245`), and P4 may make pr-submit a worker (`SPEC:242`). No behaviour changes because `/sc:git` stays coordinator-only, so Medium. Recommendation: reword the row to "the coordinator runs git unless D4 authorizes a worker".

**M-13 Smaller stated-text gaps.** (a) Nothing says what the coordinator does with a `blocked` report (read `blocked_question`, get the answer, start a new Task with the flag), although §2.3 stops at "opens the report file, then releases" (`SPEC:73`). (b) The shared rules are in `~/.claude/WORKER-CONTRACT.md`, installed by `superclaude install` (`SPEC:52`); no phase says the install must be re-run on the worker host before P1 live checks, and nothing says what a command does if the file cannot be read under `--unattended` (it should fail closed as blocked). (c) WC-4 keeps foreign `status` vocabularies untouched (`SPEC:62`) without a mapping to the four values WC-5 consumes (`INV-B:272`). (d) The brief invokes a `/sc:` command inside an Orca preamble; how a slash command embedded after a preamble is recognised is not stated (P0 AC-0.4 would test it, `SPEC:194`) and is absent from the UNVERIFIED list. Medium, none a wrong outcome without a guess.

## === ARCHITECTURE ANALYSIS ===

Experts: Fowler (lead), Newman, Hohpe, Nygard.

- Fowler (boundaries). The split is sound: commands expose a single unit-of-work interface (flag, report file, resume), and orchestration stays above them. The count-conservation check passed. B-01 and M-02 are the interface-definition defects: the report location and the flag propagation are what a coordinator depends on.
- Newman (evolution). Putting shared rules in one installed file with a short per-command section is the right dependency direction (`SPEC:52`, Decisions `SPEC:264`). The unresolved items are version and install coupling (M-13 b) and the P3 reconciliation of command and skill drift, which is correctly ordered before relying on report paths (`SPEC:161`).
- Hohpe (message flow). The completion path (`worker_done` once, from the top-level session, with a file pointer, WC-5, WC-7, WC-12) is consistent with the Orca facts cited (`CAPS:73`, `CAPS:76`, `CAPS:150`, `CAPS:159`). The risk is the ask/reply loop in WC-3 without a carve-out (M-01) and without a bound (N-08).
- Nygard (failure modes). The rejection of commands calling Orca (R1 to R5) is well argued and traced to `CAPS:97-103`, with the untraced call sites marked UNVERIFIED. Failure modes still open: heartbeat consequence (M-04), retry overwrite (M-05), tasklist remediation fan-out (M-03). Phase 0 smoke runs are the right mitigation for the evidence gap in §1.4(1).
- Whittaker (attacks, all five run):
  - Zero/Empty: `--unattended` without an output location (M-11). Divergence: path of the report (B-01). Sentinel Collision: the `--unattended` token inside user text (M-11); `blocked` also used for refusals (N-04). Sequence: ask, reply, re-invoke (M-01); retry without resume flag (M-05). Accumulation: N tasklist phases each auto-accepting remediation (M-03); fan-out longer than the heartbeat budget (M-04).
- Crispin (guard table completeness). The table above covers every conditional rule the spec states; the GAP rows map to M-01, M-04, M-05, M-06, M-08, M-11 and M-13 and are Medium.
- Adzic, Cockburn, Gregory, Hightower: no further finding beyond the above; Adzic notes that the acceptance checks are concrete (7.2 steps 1 to 7) but that AC-0.4 step 4 and step 5 do not fit the commands under test (N-02).

## Minor notes (never fail the review)

- N-01 Unverifiable citations. All `cmd/`, `sk/`, `CLAUDE.md:N`, `HOW-WE-WORK.md:N`, `install_core.py`, `Makefile`, `pyproject.toml:38`, `EVIDENCE.md:N`, codegraph-migration, `core/CLAUDE.md:65` and Orca-source cites in the spec are UNVERIFIED here. The spec's own statements that 11 locations were re-read and that an independent check re-read about 340 citations and fixed 9 defects (`SPEC:11`, `:285`) cannot be checked either; the inventories' equivalents are at `INV-A:106` and `INV-B:320`.
- N-02 AC-0.4 says the no-wrapper property is "verified in the step-5 transcript", but step 5 only searches for `AskUserQuestion` (`SPEC:194`, `:184`). Step 4's YAML assertion of `status` and `command` cannot apply to troubleshoot's markdown `REPORT.md` (`SPEC:91`, `:183`) though AC-0.4 says step 4 uses the existing file.
- N-03 §6 says P1 to P3 need no user decision (`SPEC:154`); §9 says P0 to P3 proceed on the recommendations (`SPEC:225`); D4 also affects P2 commands (M-08).
- N-04 Several rows use "refused under `--unattended`" (`SPEC:102`, `:108`, `:114`, `:123`), which is not one of WC-2's three resolutions (`SPEC:60`); WC-4 implies a blocked or failed contract for them.
- N-05 P1's rationale says "no person gate is involved" (`SPEC:159`) though explain, business-panel and test each add a refusal.
- N-06 E2 says the worker "answered" and cites `EVIDENCE.md:45` (`SPEC:22`); the inventory quote supports only "ready" (`CAPS:49`).
- N-07 `tasklist` and `reflect` are both P2 and the tasklist change depends on the reflect change (`SPEC:122`, `:88`); the order inside P2 is not stated.
- N-08 No upper bound on a worker's wait in `ask` (WC-3 plus no heartbeat while blocked, `CAPS:64`); the coordinator's behaviour on a long-pending question is not specified.

## Expert panel sequence and coverage

Review order: 1 Wiegers, 2 Adzic, 3 Cockburn, 4 Fowler, 5 Nygard, 6 Whittaker, 7 Newman, 8 Hohpe, 9 Crispin, 10 Gregory, 11 Hightower (simulated, native reasoning). Focus `requirements,architecture` selected Wiegers/Adzic/Cockburn and Fowler/Newman/Hohpe/Nygard as leads; Whittaker, Crispin (guard table) and the remaining experts ran as described above.

What was covered:
- Read in full: the command definition, the review-loop prompts file, `README.md`, the candidate (all 285 lines), `inventory/commands-a.md` (121 lines), `inventory/commands-b.md` (324 lines), and `inventory/orca-capabilities.md` lines 40 to 189 in full plus lines 25 and 37 by search.
- Checked: every section-1 evidence cite, every per-command row in sections 3 and 4 against its inventory rows, the 10/27/6 and phase counts, the WC, SA, AC and D cross-references (WC to AC, SA to AC-C1 and C5, D1 to D5 to phases), the Orca fact claims against `CAPS`, and the Decisions and UNVERIFIED lists against the inventories' own UNVERIFIED lists.
- Not covered: any claim whose only source is outside the five readable files (N-01); the correctness of the Orca guide quotes themselves (taken from `CAPS`); no command was run.
- Guard Condition Boundary Table, Quantity Flow Diagram: produced above. State Variable Registry: not required (`--focus correctness` not active). Auto-suggestion for `--focus correctness`: not triggered (the spec introduces no mutable state variables, only phase counts and file state).

## Follow-up candidates (Medium and minor, none blocking, none enters the Reviser brief)

M-01 WC-3 carve-out for safety-rule and outward-action gates; M-02 `--unattended` propagation to nested calls; M-03 tasklist reversal of the inventory verdict and auto-accepted remediation; M-04 WC-10 versus WC-7 fan-out and the unverified heartbeat premise; M-05 retry and fresh-directory semantics; M-06 which ready commands gain `--unattended`; M-07 readiness-timing claim in 1.4(2); M-08 "authorized" mechanism for task and post-release; M-09 AC-C1 versus P0 deliverables; M-10 completeness of the 43-command count; M-11 `--unattended` parsing and missing output location; M-12 `/sc:git` row rationale; M-13 blocked-report handling, install step, status mapping, slash-command invocation. N-01 to N-08 as listed.

Issue offer: this run is a coordinator-driven gate review whose reply is limited to the output path, so the user was not asked once per loop whether to open an issue for the list above, and none was created. The coordinator should put that question to the user.

## Reviser brief

Blocking finding ids: B-01.

Restated rules for the reviser (the reviser reads this report, not the command): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size of the candidate before and after, with the bytes added and deleted per finding id; leave minor and Medium findings alone; return the candidate once and do not award yourself a PASS. B-01 touches WC-4 (`SPEC:62`), section 2.3 (`SPEC:73`), the adversarial, tdd, init-lite, workflow and cleanup-audit rows (`SPEC:83`, `:90`, `:87`, `:92`, `:85`), 7.2 steps 3 and 4 (`SPEC:182-183`) and AC-1.4 and AC-2.2 (`SPEC:198`, `:200`) only.

verdict: FAIL

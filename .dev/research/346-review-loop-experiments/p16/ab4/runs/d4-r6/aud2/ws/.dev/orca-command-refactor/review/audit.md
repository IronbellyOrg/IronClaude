review: 1 of 3

# Spec-panel audit: orca-worker-contract-spec.md (labelled whole-document audit, first review)

Command run: `/sc:spec-panel @.dev/orca-command-refactor/specs/orca-worker-contract-spec.md --mode critique --focus requirements,architecture` (acted as the command definition, `command.md`). Prompt followed: FIRST-REVIEW prompt of `~/.claude/rules/prompts/document_review_loop_prompts.md` (read in full, lines 1-55).

| Header field | Value |
|---|---|
| candidate | `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md` |
| candidate sha256 | `969ea3c660a240d980e47aa21c5b87e0ebbb7ea61cb15bc2f7483d1290dc6ad5` |
| baseline / prior | none given: this is a first review of the full document (`command.md:258`) |
| reviewer model used | claude-sonnet-5-5 (the model named in my environment) |
| mode / focus / format | critique / requirements, architecture / standard (YAML block at the end) plus bucketed findings (`command.md:123,274`) |
| iterations | 1 (every run is one review, `command.md:261`) |

Citation keys: `SPEC:N` = line N of the candidate; `INV-A:N`, `INV-B:N`, `CAPS:N` = lines of `inventory/commands-a.md`, `commands-b.md`, `orca-capabilities.md`; `README:N` = `.dev/orca-command-refactor/README.md`; `CMD:N` = `command.md`. The inventories are the only evidence I could check. Any citation to a file outside the workspace (`EVIDENCE.md`, `src/superclaude/**`, `CLAUDE.md`, `install_core.py`, `pyproject.toml`, the PR #329 files) is UNVERIFIED except where an inventory quotes it.

## What was covered

- Whole document: sections 1-9, the Decisions table and the UNVERIFIED list (`SPEC:1-285`).
- Every citation of the form `INV-A:`, `INV-B:`, `CAPS:` was compared with the inventory line. All the row-level pointers in section 3 (3.1 rows `SPEC:82-92`, 3.2 rows `SPEC:99-125`) and section 4 (`SPEC:132-137`) land on the matching inventory rows. The counts hold: 43 = 21 + 22 (`INV-A:3`, `INV-B:3`), 10 + 27 + 6 = 43, and the phase lists add up (Quantity Flow Diagram below).
- Internal consistency of requirements WC-1..WC-12, SA-1..SA-6, phases P0-P4, acceptance checks AC-C1..AC-4.3, open decisions D1-D5.
- Not covered: whether the cited `src/` lines say what the inventories report (not in the sandbox); the unreviewed `review/disposition.md` (does not exist in the sandbox, so the revision tags `M1..M7` in the candidate could not be resolved, see N-1).

## Expert panel (review sequence per `CMD:99-113`, filtered by focus)

Wiegers (lead, requirements), Adzic, Cockburn, Fowler (lead, architecture), Nygard, Whittaker (always active), Newman, Hohpe. Crispin, Gregory, Hightower are not in the requested focus areas and were not seated.

## Grading summary

No finding below passes the grading check for blocking: each needs the implementer to pick the worse of two readings the text allows, or concerns a requirement the document never states. By `CMD:259` and the FIRST-REVIEW grading check (`PROMPTS:31`) they are Medium and are listed under follow-up candidates, not as blocking.

Blocking findings: 0. Medium: 11 (F-01 to F-11). Minor notes: 6 (N-1 to N-6).

Grading check (one sentence per finding, written before grading; the sentence for each Medium is in its entry).

=== REQUIREMENTS ANALYSIS ===

### F-01 (Medium, MAJOR label) Output location per Task and per attempt is not fixed
- Experts: Wiegers (testability), Cockburn (actor: coordinator vs command), Whittaker (sentinel collision, sequence).
- Location: WC-4 `SPEC:62` (contract is `return-contract.yaml` "in the directory the coordinator passed"), WC-6 `SPEC:64` (a command with no resume flag "writes each run into a fresh output directory"; owner is "Command"), WC-11 `SPEC:69`, 2.3 `SPEC:73` (brief states "the output path").
- Grading sentence: An implementer who follows the stated text as written builds a command that, on a retry or on a re-invoke after `blocked` (`SPEC:61`), either creates its own fresh subdirectory (so the contract is no longer at the path the coordinator fixed before dispatch, `SPEC:62,73`) or reuses the passed directory (so the first attempt's output and an old `status` contract stay in place, against `SPEC:64`); which one is right is not stated, so the grade is Medium.
- Attack: the coordinator splits work into two Tasks (the example at `SPEC:39`: several `/sc:troubleshoot` workers, then one `/sc:adversarial`) and gives them the same `--output D`. Both write `D/return-contract.yaml`; the second overwrites the first and the coordinator reads the wrong `status`. 2.3 never says one output path per Task and per attempt.
- Recommendation: in 2.3 and WC-6, state that "fresh dir" means a new output path chosen by the coordinator for each Task and each attempt, and that a command never creates its own sub-run directory under WC-4; this is a narrowing, not a new mechanism. Priority: Medium. Quality impact: raises Consistency and Testability by about 1 point each.

### F-02 (Medium) Status vocabulary and "keep their fields" can contradict; brainstorm gets no contract work; WC-5 has no row for an unknown or empty status
- Experts: Wiegers, Adzic (state-annotated examples missing), Whittaker (zero/empty, sentinel).
- Location: WC-4 `SPEC:62` ("Commands that already write a contract keep their fields and add the missing ones"; `status` is one of four values), Decisions `SPEC:262` (a fixed four-value set; copying each command's statuses rejected), check `SPEC:183` (asserts the four values), WC-5 `SPEC:63`; existing contracts `INV-B:272` (workflow: `status`, `plan_path`, `reflect_report_path`; contract 1.1), `INV-A:97`, `INV-B:112`. Neither inventory records the values existing contracts use for `status`.
- Grading sentence: An implementer who follows "keep their fields" for workflow, reflect, adversarial or brainstorm keeps whatever `status` values they have today, and the `SPEC:183` check then fails on a value outside the four; if the implementer instead rewrites the values, "keep their fields" is broken; the document does not say which, and the existing values are unknown, so the grade is Medium.
- Also: brainstorm is "ready today" with `<output>/return-contract.yaml` and "None" as its small fix (`SPEC:84`) and appears in no phase (`SPEC:158-162`), so nothing ever adds the WC-4 fields `command` and `status` to it. init-lite is excepted explicitly (`SPEC:62`); brainstorm is not.
- Also: WC-5 (`SPEC:63`) maps four statuses and "no report exists"; a contract file that exists but is empty, unparseable, or holds a value outside the four has no mapping.
- Recommendation: add one sentence to WC-4: existing contracts keep their other fields, and `status` is mapped to the four-value set by a table the contract file carries per command; add "a missing, empty or unparseable contract counts as no report" to WC-5; name brainstorm in the same exception as init-lite. Priority: Medium.

### F-03 (Medium) The `--unattended` switch is specified as a bare flag with no parsing rule
- Experts: Whittaker (sentinel collision), Adzic, Wiegers.
- Location: D1(a) `SPEC:228` ("cannot misfire on a person"), `SPEC:51`, the free-text commands in section 3 (tdd `SPEC:90`, troubleshoot `SPEC:91`, research `SPEC:116`, recommend `SPEC:115`).
- Grading sentence: An implementer who follows D1(a) as written recognizes the flag by finding the string, and a person who runs `/sc:troubleshoot "login fails when --unattended is set"` gets an unattended run (gates resolved, a contract written); this is wrong because D1(a) claims the flag cannot misfire on a person, but the claim needs a rule for quoted text that the document does not state, so the grade is Medium.
- Evidence that the rule is known and is not in this spec: the current command definition says the switch applies only when `--unattended` is a standalone argument token outside any quoted argument (`CMD:459`).
- Recommendation: add to WC-2 and the contract-file description: the mode switches on only when `--unattended` is a standalone argument token outside any quoted argument. Priority: Medium.

### F-04 (Medium) WC-10 leaves a gap between its trigger and its cap, and has no acceptance check outside pr-submit
- Experts: Nygard (reliability), Whittaker (divergence, accumulation), Wiegers (measurability).
- Location: WC-10 `SPEC:68` (a step "longer than 5 minutes" must be "split into waits of at most 4 minutes"), Decisions `SPEC:266`, cli-eval row `SPEC:104`, pr-submit row `SPEC:114`, AC-4.3 `SPEC:210` (240 s, only under D3(b)), P2 checks `SPEC:199-203` (no wait-length check).
- Grading sentence: An implementer who follows WC-10 as written leaves a single 4.5-minute blocking call alone (it is not "longer than 5 minutes") although the cap in the same row is 4 minutes, so a heartbeat due every 5 minutes (`CAPS:130`) can be missed; whether a missed heartbeat harms anything depends on whether Orca uses heartbeat age (`CAPS:182` item 7, UNVERIFIED), so the grade is Medium.
- Also: the cli-eval wait split (a P2 deliverable, `SPEC:160`) has no check in P2; only pr-submit's 240 s check exists, and only if D3(b) is chosen.
- Recommendation: make the trigger and the cap the same number (any single blocking call over 4 minutes is split) and add one P2 check for cli-eval. Priority: Medium.

### F-05 (Medium) Requirements without an owner phase or an acceptance check
- Experts: Wiegers (traceability), Adzic.
- Location: WC-1 `SPEC:59` (owner "Launch setup, not commands"; no phase in `SPEC:158-162` delivers it, and non-goal 2 `SPEC:214` forbids changing Orca; the only check is 7.2 step 1, `SPEC:180`, which observes `state: ready`); WC-3 `SPEC:61` (no check that a blocked worker asks once and resumes by message ID); WC-12 `SPEC:70` (no check); WC-10 for cli-eval (F-04); WC-11 `SPEC:69` checked only for `save` (AC-3.4, `SPEC:207`).
- Grading sentence: An implementer who follows the phases builds P0-P4 and passes every check while WC-1 (the readiness-limit cause the spec itself cites as the real failure, `SPEC:59`) was never assigned to a deliverable, so the spec's own motivating failure can recur; this is a requirement with no stated owner, not a stated text that does harm, so the grade is Medium.
- Recommendation: add a one-line owner and check per requirement (a traceability column), or mark WC-1/WC-3/WC-12 as "coordinator or worker-session behaviour, checked by the 7.2 steps listed". Priority: Medium.

### F-06 (Medium) No coordinator rule for a `blocked` report
- Experts: Cockburn (primary actor's goal after the block), Nygard.
- Location: WC-3 `SPEC:61` (worker-side `ask`), WC-5 `SPEC:63` (blocked is reported as `--outcome failed`), 2.3 `SPEC:73` (after `worker_done` the coordinator "opens the report file, then releases or reuses"). Orca facts: a cancelled or failed Task keeps its dependents blocked until a `--retry-of` replacement completes it (`CAPS:90`); a worker's own `failed` report does not count toward the three-failure breaker (`CAPS:80,116`).
- Grading sentence: An implementer who writes the brief template (P0, `SPEC:158`) from 2.3 gives the coordinator no step for `blocked`, so a blocked Task stays failed, its dependents stay blocked, and nothing tells the coordinator to answer and start a `--retry-of` worker, or to stop after N blocked retries (the breaker does not count them); this is a missing procedure, not a stated text that does harm, so the grade is Medium.
- Recommendation: add to 2.3: on `blocked`, answer the question, start a `--retry-of` worker in a new output path (F-01) with the answer as a flag, and cap blocked retries per Task. Priority: Medium.

### F-07 (Medium) `task` commit/push refusal depends on a mechanism and a decision the spec places after P2
- Experts: Wiegers, Cockburn.
- Location: task row `SPEC:121` ("EXEMPT `commit`/`push` refused unless authorized (WC-9)"), WC-9 `SPEC:67` (an outward default turns on "only through the command's own explicit flag"), `INV-B:204` (the EXEMPT keywords `commit` and `push` run immediately with no skill, no flag), D4 `SPEC:244` (names task `commit`/`push` as affected), `SPEC:154` ("Phases 1-3 need no user decision"), P2 `SPEC:160`.
- Grading sentence: An implementer who follows the task row in P2 must make commit/push "authorized" through "the command's own explicit flag", but `/sc:task` has no such flag today (`INV-B:204`) and D4 (which defines who may authorize) is answered only before P4 (`SPEC:154`), so the implementer invents the flag name and the rule; the text allows more than one reading, so the grade is Medium.
- Recommendation: either name the flag in the task row (and say P2 turns the action off with no way to turn it on until D4), or move the `commit`/`push` clause to P4. Priority: Medium.

### F-08 (Medium) The index row contradicts UNVERIFIED item 6
- Experts: Wiegers, Whittaker (zero/empty).
- Location: index row `SPEC:111` ("state that knowledge-base mode does not wait (whether it does is UNVERIFIED)"), UNVERIFIED 6 `SPEC:277` ("section 3 refuses or pins them under `--unattended` regardless"), `INV-A:54,113`. The business-panel row (`SPEC:102`) and explain row (`SPEC:108`) do refuse the interactive mode; the index row does not.
- Grading sentence: An implementer who follows the index row writes the sentence "knowledge-base mode does not wait" without changing behaviour; if the mode does wait (the inventory could not tell, `INV-A:113`), the unattended index worker stalls silently, which is the failure WC-2 (`SPEC:60`) forbids; the harm depends on an unverified fact, so the grade is Medium.
- Recommendation: make the index row match the other two: refuse the interactive knowledge-base mode under `--unattended` until it is verified not to wait. Priority: Medium.

### F-12 (Medium) WC-3 is generic; implement's Ruling rule needs an explicit carve-out
- Experts: Wiegers, Nygard.
- Location: WC-3 `SPEC:61` (any blocked gate: the session "may instead ask the coordinator once ... then re-invoke or resume the command with the answer as a flag"), implement row `SPEC:109`, D2 `SPEC:232-236`, `INV-A:66` (a Ruling needs the person's confirmation; "another agent's message" does not count), P0 installs the contract file before P4 (`SPEC:158,162`).
- Grading sentence: An implementer who follows WC-3 for an `E-NO-RULING` halt lets the worker ask the coordinator and resume with the coordinator's answer, which D2(a) and the rule at `INV-A:66` say must not become a Ruling; the command itself should still reject it, so the harm depends on the model relaying the answer anyway, and the grade is Medium.
- Recommendation: add to WC-3 "except gates that require a person's own confirmation (implement Ruling) unless D2(b) is chosen". Priority: Medium.

=== ARCHITECTURE ANALYSIS ===

### F-09 (Medium) Two common acceptance checks conflict with the spec's own deliverables
- Experts: Fowler (interface and boundary), Newman (evolution, backward compatibility), Nygard.
- Location: AC-C1 `SPEC:172` (grep over `src/superclaude/core` for `orca orchestration|worktree|terminal|agent` must print nothing, every phase), SA-2 `SPEC:147` ("the only allowed mention of Orca in a changed command is as an example of a caller's question channel inside the contract file"), SA-5 `SPEC:150` and P0 `SPEC:158` (an Orca section is added to `HOW-WE-WORK.md` and the contract file is written, both under `src/superclaude/core`). AC-C5 `SPEC:176` (no `-` line in a command diff unless a named defect fix) against SA-4 `SPEC:149` (additive edits include "new flags").
- Grading sentence: An implementer who follows SA-2 writes the example `orca orchestration ask` into `WORKER-CONTRACT.md` and a worked coordinator example into the `HOW-WE-WORK.md` Orca section, and then P0 fails its own AC-C1 (the pattern matches and the scope includes `core`); likewise, an implementer who adds `--unattended` to a command's Usage line (a single line, as `load` shows, `SPEC:112`, `INV-B:63`) produces a `-` line and fails AC-C5; the text allows a reading that avoids both, so the grade is Medium.
- Recommendation: exclude `WORKER-CONTRACT.md` and the one Orca section of `HOW-WE-WORK.md` from AC-C1 (or forbid literal commands there), and state in SA-4/AC-C5 whether a new flag goes on the Usage line (and then exempt that line). Priority: Medium.

### F-10 (Medium) Where the contract lands is unspecified in three cases
- Experts: Fowler (interface consistency), Hohpe (data flow to the consumer), Whittaker (zero/empty).
- Location: (a) the brief omits the output path under `--unattended`: WC-4 `SPEC:62` and 2.3 `SPEC:73` require the path in the brief, and only post-release says "else blocked" (`SPEC:113`); the other rows say "add a report path" (`SPEC:99-125`) without the no-path case; (b) workflow pre-creation stops: the P1 fix `SPEC:92` asks for a contract on those stops, but the contract lives in `.dev/tasks/to-do/<id>/` (`INV-B:272`: "Not written for pre-creation STOPs") and no `<id>` exists then, so no path is given; AC-1.4 `SPEC:198` checks only that the ref "states" it; (c) research: the row `SPEC:116` has a contract "naming the generated `claudedocs/research_*.md` path", but research has no output flag (`INV-B:132`), so the contract's own location is not given.
- Grading sentence: An implementer who follows WC-4 for workflow's pre-creation STOP writes a contract nowhere definable, and for research writes it at an unspecified place, so the worker cannot pass `--report-path` and the coordinator sees "no report" (`SPEC:63`) and an outcome of `failed` with no reason; the text allows several locations, so the grade is Medium.
- Recommendation: one rule for all three: with no output path in the brief, a command resolves as `blocked` (chat-only refusal), and workflow's pre-creation contract goes under the `--output`-style path from the brief, not under `<id>`. Priority: Medium.

=== ADVERSARIAL ANALYSIS (Whittaker, review order 6) ===

Each finding follows `CMD:82`. Severity uses the grading above.

1. I can break this specification by **Zero/Empty Attack**. The invariant at **WC-4 / 2.3 (`SPEC:62,73`: the contract path is known before dispatch)** fails when **the brief omits the output path under `--unattended`**. Concrete attack: coordinator dispatches `/sc:analyze src/x.py --unattended` with no `--output`. State before: no known contract path. The analyze row (`SPEC:99`) says "add `--output`" and says nothing about the absent case; the command writes its report at today's default (SA-3, `SPEC:148`), or nowhere. State after: worker reports no `--report-path`; WC-5 (`SPEC:63`) gives `--outcome failed` with no reason. See F-10. Severity: Medium (specification is incomplete under attack).
2. I can break this specification by **Divergence Attack**. The invariant at **WC-10 (`SPEC:68`)** fails when **a single blocking call runs between 4 and 5 minutes**. Concrete attack: cli-eval waits 4.5 minutes in one call after a heartbeat 1 minute earlier. Before: last heartbeat at t=0. After: next heartbeat at t=5.5 minutes, past the 5-minute cadence (`CAPS:130`); WC-10 says nothing is wrong (not longer than 5 minutes). See F-04. Severity: Medium.
3. I can break this specification by **Sentinel Collision Attack**. The invariant at **D1(a) (`SPEC:228`)** fails when **user content contains the literal `--unattended`**. Concrete attack: `/sc:tdd "add an --unattended mode to the CLI" --output t.md`. Before: attended run, topic-only prompt gate (`SPEC:90`) asks. After: a naive parse treats the topic text as the switch, resolves the gate as blocked, writes `t.return-contract.yaml`, and the person never sees the question. See F-03. Second collision: two Tasks sharing one `--output` both write `return-contract.yaml` (F-01). Severity: Medium for both.
4. I can break this specification by **Sequence Attack**. The invariant at **WC-3 + WC-5 + WC-6 (`SPEC:61,63,64`)** fails when **the worker re-invokes a command after `blocked` into the same output path, and the re-run dies before writing**. Concrete attack: run 1 writes `status: blocked` and the worker, after the coordinator's answer, re-invokes; the process is killed at 2 minutes. State after: `D/return-contract.yaml` still says `blocked`; no new contract; the worker's `worker_done` follows WC-5 from a stale file. Nothing requires a command to remove or overwrite an old contract at start. See F-01. Second sequence: P0 installs the generic WC-3 before P4 decides D2 (F-12). Severity: Medium.
5. I can break this specification by **Accumulation Attack**. The invariant at **WC-5 + Orca breaker (`SPEC:63`; `CAPS:80,116`)** fails when **a Task is retried after every `blocked`**. Concrete attack: a coordinator answers, retries with `--retry-of`, the command blocks on a second question, repeat. Each report is a worker's own `failed`, which does not count toward the three-failure breaker (`CAPS:80`), so the loop has no bound. Second accumulation: AC-2.4 (`SPEC:202`) compares `gh api ... --jq length` counts without `--paginate`; on a PR with 30 or more comments page 1 keeps the same length after a new comment (see N-5). See F-06. Severity: Medium for the first; Minor for the second.

## Guard Condition Boundary Table

Guards were identified in the spec text (thresholds, switches, branches). Classes that cannot occur for a guard are left out with a one-line reason.

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|---|---|---|---|---|---|---|
| WC-10 wait split | `SPEC:68` | Zero/Empty | 0 s wait | false | no wait, nothing to split | OK |
| WC-10 wait split | `SPEC:68` | Typical | 2 min call | false | no split needed | OK |
| WC-10 wait split | `SPEC:68` | Legitimate Edge Case | 4.5 min call | false (trigger is >5 min) | none stated; cap says 4 min | GAP (F-04) |
| WC-10 wait split | `SPEC:68` | Maximum/Overflow | 3600 s eval (`SPEC:68`, cli-eval) | true | split into waits of at most 4 min | OK |
| WC-10 wait split | `SPEC:68` | Sentinel Value Match | pr-submit "600 s" | n/a | cumulative budget, not one call (`SPEC:68,114`) | OK |
| WC-5 outcome map | `SPEC:63` | Zero/Empty | no file, or empty file | no report | missing file: `failed`; empty/unparseable: unspecified | GAP (F-02) |
| WC-5 outcome map | `SPEC:63` | Typical | `succeeded` / `partial` | true | `--outcome succeeded` | OK |
| WC-5 outcome map | `SPEC:63` | One/Minimal | `blocked` or `failed` | true | `--outcome failed` | OK |
| WC-5 outcome map | `SPEC:63` | Sentinel Value Match | audit verdict FAIL | true | still `succeeded` | OK |
| WC-5 outcome map | `SPEC:63` | Legitimate Edge Case | `status` value outside the four (existing contract vocabulary) | unknown | unspecified | GAP (F-02) |
| `--unattended` switch | `SPEC:51,228` | Zero/Empty | flag absent | false | today's behaviour (SA-1, `SPEC:146`) | OK |
| `--unattended` switch | `SPEC:51,228` | Typical | standalone flag | true | unattended mode | OK |
| `--unattended` switch | `SPEC:51,228` | Sentinel Value Match | literal `--unattended` inside quoted content | unknown | unspecified | GAP (F-03) |
| Output path in brief | `SPEC:62,73` | Zero/Empty | no `--output` under `--unattended` | unknown | only post-release says "else blocked" (`SPEC:113`) | GAP (F-10) |
| Output path in brief | `SPEC:62,73` | Typical | directory passed | true | contract at `<dir>/return-contract.yaml` | OK |
| Output path in brief | `SPEC:62,73` | Legitimate Edge Case | `--output` names a file (tdd, init-lite) | true | `<file-stem>.return-contract.yaml` beside it (`SPEC:62`) | OK |
| Output path in brief | `SPEC:62,64` | Maximum/Overflow | same directory reused by a second Task or attempt | true | unspecified | GAP (F-01) |
| task confidence guard | `SPEC:121` | Typical | 0.50 | true (below 0.70) | blocked | OK |
| task confidence guard | `SPEC:121` | Legitimate Edge Case | exactly 0.70 | false ("below 0.70") | proceeds, as `INV-B:199` states "< 0.70" | OK |
| Nested depth guard | `SPEC:33`, `CAPS:97-101` | One/Minimal | depth 1 worker calls `worker-start` | true | refused `nested_worker_depth_exceeded` | OK |
| Nested depth guard | `SPEC:33`, `CAPS:100` | Zero/Empty | malformed or missing setting | true | falls back to 1 (`CAPS:100`) | OK |
| WC-1 readiness fallback | `SPEC:59` | Typical | 30 s fallback | passes | `EVIDENCE.md:45` via `CAPS:49` (UNVERIFIED as a file) | OK |
| WC-1 readiness fallback | `SPEC:59` | Legitimate Edge Case | 45-60 s fallback | unknown | requirement says "well inside"; the 45 s failure point is only in the evidence cell | GAP (N-3, minor) |
| pr-submit `--monitor` | `SPEC:114` | One/Minimal | `--monitor 1` | true | refused | OK |
| pr-submit `--monitor` | `SPEC:114` | Typical | `--monitor 3` | false | no y/n gate (`INV-B:89`) | OK |
| pr-submit `--monitor` | `SPEC:114` | Legitimate Edge Case | `--monitor 0` or `2` | unknown | not stated; P4 only, behind D3(a) | GAP (N-4, minor) |
| Retry breaker | `CAPS:80,116` | Maximum/Overflow | repeated `blocked` retries | not counted | no bound in the spec | GAP (F-06) |

Left out with reasons: Sentinel and Maximum classes for the depth guard (a number, no sentinel; raising it is D5, not a behaviour of this spec); One/Minimal for WC-1 (a timing guard has no count form).

Completion check (FR-10, `CMD:334`): all guards that the spec states were enumerated, every cell is populated, and every class is either a row or has a reason; synthesis may proceed. FR-8/FR-9 findings from the GAP rows are graded as the findings listed: F-01, F-02, F-03, F-04, F-06, F-10 (Medium) and N-3, N-4 (minor). None names a concrete wrong outcome without an assumption, so none is blocking.

## Quantity Flow Diagram (pipeline dimensional analysis: command classification and phase assignment)

```text
[43 commands: INV-A 21 + INV-B 22]  --> [Classify: SPEC:76]
    |-- [10 ready (3.1)] --> P1 small fixes 4 (adversarial, cleanup-audit, index-repo, workflow)
    |                    --> P2 small fixes 4 (reflect, release-split, tdd, troubleshoot)
    |                    --> no phase 2 (brainstorm, init-lite)           [4+4+2 = 10]
    |-- [27 needs change (3.2)] --> P1 9 (8 + load usage line) | P2 11 | P3 4 | P4 3   [9+11+4+3 = 27]
    |-- [6 coordinator-only (4)] --> no phase
    [10 + 27 + 6 = 43]
Consumers: "## Unattended mode" sections: 27 - load = 26, + 4 (reflect, release-split, tdd, troubleshoot) = 30
           = P1 8 + P2 15 + P3 4 + P4 3 = 30                                [AC-1.1 covers the P1 eight only]
           AC-2.2 enumeration: 9 blocked + 6 default = 15 = P2 count         [SPEC:200]
```

No count mismatch found (no CRITICAL under FR-19). The one under-covered consumer is brainstorm: it is in the 10 but reaches no phase, so it never gets the WC-4 fields (F-02).

## Follow-up candidates (Medium and minor; none triggers a revision)

Medium: F-01, F-02, F-03, F-04, F-05, F-06, F-07, F-08, F-09, F-10, F-12 (each above).

Minor notes:
- N-1: The tags `(M1)` to `(M7)` appear 19 times (`SPEC:62,73,76,79,89-91,159-160,182-183,194-196,198,200`) and are defined nowhere in the document. They look like revision markers from the disposition file, which is not in the sandbox (UNVERIFIED). The text stands without them; a reader cannot resolve them. Suggest dropping or defining them.
- N-2: Self-description drift. 1.1 says command changes are "limited to" the section 2 contract (`SPEC:16`) while SA-4 lists drift and defect fixes (`SPEC:149`: roadmap, validate-roadmap, validate-tests target, explain tools, business-panel frontmatter). The citation conventions say all other lines are carried from the inventories without a second read (`SPEC:11`) while UNVERIFIED 14 says an independent agent re-read about 340 citations (`SPEC:285`); both can be true but are not tied together. `SPEC:154` says phases 1-3 need no user decision while D1 is a user decision all phases use (`SPEC:227`). pr-submit is counted among the "27 needing a change" (`SPEC:76`) while D3(a), the recommendation, makes no pr-submit change (`SPEC:240`).
- N-3: WC-1 gives no number (`SPEC:59`): "well inside" the 60 s limit; the 30 s pass and the roughly 45 s failure sit in the evidence cell (via `CAPS:49`). Put the safe value (30 s) in the requirement.
- N-4: pr-submit under `--unattended` refuses `--monitor 1` only (`SPEC:114`); `--monitor 0` and `2` are not described in the inventory either (`INV-B:89`). UNVERIFIED; only matters if D3(b) is chosen.
- N-5: AC-2.4 (`SPEC:202`) compares `gh api ... --jq length`; without `--paginate` a PR with 30 or more comments reports the same page length after a new comment, so the check can pass falsely. Add `--paginate`.
- N-6: The spec-panel row (`SPEC:120`) says to "add `--output`", and WC-4 (`SPEC:62`) names `--output` / `--output-dir` as the directory flag. The command definition supplied for this audit already has `--output <file>`, `--report-dir`, `--unattended`, a `return-contract.yaml` under `<report-dir>`, and a blocked outcome for a TDD input without a release (`CMD:22-23,455-465`), and `INV-B:182` says no such flag exists. Either the inventory predates the command text or the audit supplied a newer file; I could not check `cmd/spec-panel.md` (UNVERIFIED). If the newer text is the target, the spec-panel row and the `--report-dir` naming need to follow it.

Per `CMD:260`, the session that ran this review asks the user once per loop whether to open an issue for the Medium and minor items and creates none without an answer. I am a sandboxed worker with no way to ask; this list is recorded only. No issue was created.

## Quality assessment (0-10)

Clarity 8, Completeness 7, Testability 7, Consistency 7. Overall 7.25. The design decision, evidence base and inventory cross-references are strong; the weak points are contract-location rules, acceptance-check scope and a few unowned requirements.

```yaml
specification_review:
  original_spec: .dev/orca-command-refactor/specs/orca-worker-contract-spec.md
  review_date: 2026-11-10
  expert_panel: [Wiegers, Adzic, Cockburn, Fowler, Nygard, Whittaker, Newman, Hohpe]
  focus_areas: [requirements, architecture]
quality_assessment:
  overall_score: 7.25
  clarity: 8
  completeness: 7
  testability: 7
  consistency: 7
critical_issues: []   # blocking findings: none
medium_findings:
  - {id: F-01, category: requirements, expert: Wiegers, issue: output path per Task/attempt not fixed, recommendation: coordinator supplies a new path per Task and attempt}
  - {id: F-02, category: requirements, expert: Wiegers, issue: status vocabulary vs keep-their-fields; brainstorm uncovered; unknown status unmapped}
  - {id: F-03, category: requirements, expert: Whittaker, issue: --unattended parsing rule missing}
  - {id: F-04, category: architecture, expert: Nygard, issue: WC-10 4-5 minute gap and no cli-eval check}
  - {id: F-05, category: requirements, expert: Wiegers, issue: WC-1, WC-3, WC-12 have no owner phase or check}
  - {id: F-06, category: architecture, expert: Cockburn, issue: no coordinator rule for blocked reports}
  - {id: F-07, category: requirements, expert: Wiegers, issue: task commit/push mechanism and D4 timing}
  - {id: F-08, category: requirements, expert: Wiegers, issue: index row contradicts UNVERIFIED 6}
  - {id: F-09, category: architecture, expert: Fowler, issue: AC-C1 and AC-C5 conflict with SA-2, SA-4, P0}
  - {id: F-10, category: architecture, expert: Fowler, issue: contract location unspecified in three cases}
  - {id: F-12, category: requirements, expert: Nygard, issue: WC-3 needs a carve-out for the implement Ruling}
expert_consensus:
  - The decision (Orca on top, commands as units) is supported by the cited inventories; counts and phase assignment reconcile.
  - The remaining gaps are missing rules (where the contract lands, how a block is answered), not wrong stated text.
improvement_roadmap:
  immediate: [F-01, F-03, F-10]
  short_term: [F-02, F-04, F-06, F-09, F-12]
  long_term: [F-05, F-07, F-08, N-1..N-6]
adversarial_analysis: see the Whittaker section above (5 attacks, all Medium or Minor)
```

Reviser brief: no blocking finding is open, so there is nothing to revise. Restated contract for any later reviser: revise only text a blocking finding names; add no rule, mechanism or section that no blocking finding calls for; cite the finding id on each added paragraph or table; prefer deleting or narrowing to adding; report the byte size before and after and the bytes added and deleted per finding id. Medium and minor findings are not part of this brief and must not be edited under it.

verdict: PASS

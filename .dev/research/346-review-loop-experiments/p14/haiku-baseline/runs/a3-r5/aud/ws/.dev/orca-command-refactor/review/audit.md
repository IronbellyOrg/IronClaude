review: 1 of 3

# /sc:spec-panel audit: Orca worker-contract spec (whole-document first review)

## Header

| Field | Value |
|---|---|
| command | `/sc:spec-panel @.dev/orca-command-refactor/specs/orca-worker-contract-spec.md --mode critique --focus requirements,architecture` |
| candidate | `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md` (59413 bytes, 291 lines) |
| candidate sha256 | `5dc5c21ad2cf82fb9524020aa4cd5b0bc6a285be451e62fe6377194b27c70222` |
| baseline / prior report | none given. This is a first review of the whole document (no `--re-review`, no `--baseline`). |
| reviewer model actually used | claude-sonnet-5-5 (simulated 11-expert panel, native reasoning; no MCP used) |
| prompt followed | FIRST-REVIEW prompt, `~/.claude/rules/prompts/document_review_loop_prompts.md` (sandbox copy, read in full) |
| coverage | whole document, all 291 lines, unscoped first review. Every `INV-A:N`, `INV-B:N` and `CAPS:N` citation I traced (about 90) was compared with the inventory line it names. All matched the claim. |
| not checkable here | Every `cmd/`, `sk/`, `ag/`, `CLAUDE.md`, `install_core.py`, `Makefile`, `pyproject.toml`, `EVIDENCE.md` and `.dev/codegraph-migration/` line, and the spec's own greps, are outside the sandbox. They are UNVERIFIED here except where an inventory quotes them. |
| `--iterations` | ignored: every run is one review (Review Loop bullet 4). The Improve step was not run and no revised specification was written. |

Citation shorthand: `SPEC:N` is line N of the candidate. `INV-A`, `INV-B` and `CAPS` are the spec's own shorthands for `inventory/commands-a.md`, `commands-b.md` and `orca-capabilities.md`. Finding ids are `AUD-n` so they cannot be confused with the `F-01` to `F-04` tags already inside the spec text (`SPEC:62`, `SPEC:85`, `SPEC:188`). Those tags point at an earlier review trail that is not in the sandbox, so they are UNVERIFIED.

```yaml
specification_review:
  original_spec: .dev/orca-command-refactor/specs/orca-worker-contract-spec.md
  review_date: 2026-11-10
  expert_panel: [wiegers, adzic, cockburn, fowler, nygard, whittaker, newman, hohpe, crispin, gregory, hightower]
  focus_areas: [requirements, architecture]
quality_assessment:   # 0-10, advisory
  overall_score: 6.5
  clarity: 7.5
  completeness: 7
  testability: 6
  consistency: 5.5
blocking_findings: [AUD-1, AUD-2]
medium_findings: [AUD-3, AUD-4, AUD-5, AUD-6, AUD-7, AUD-8, AUD-9, AUD-10, AUD-11, AUD-12]
```

## What holds up (checked, no defect)

- The partition is conserved. INV-A has 5 ready, 13 needs-change and 3 coordinator-only (`INV-A:73`). INV-B has 5, 14 and 3 (`INV-B:278`). The spec has 10, 27 and 6 (`SPEC:76`). I counted the rows: 3.1 has 10 (`SPEC:83-92`), 3.2 has 27 (`SPEC:99-125`), section 4 has 6 (`SPEC:132-137`). Every command appears once, and the 43 names equal INV-A's 21 plus INV-B's 22.
- Every per-command row's inventory citation (`INV-A:35-55`, `INV-B:31-52` and the note ranges) points at the matching command row or note.
- The core decision (Orca on top, commands unchanged inside) is argued from CAPS facts that match: depth 1 (`CAPS:97-101`), the preamble-only lifecycle (`CAPS:148-150`) and `worker_done` bound to the dispatched pane (`CAPS:76`). Section 1.4 (`SPEC:41-45`) openly states that no direct-route run exists, and `SPEC:278` repeats it. That is honest, and AC-0.4 (`SPEC:200`) tests it.
- The `gh` forms in AC-2.4, AC-4.2 and AC-4.3 (`SPEC:208,215,216`) all name `IronbellyOrg/IronClaude`.

---

## === REQUIREMENTS ANALYSIS ===

### AUD-1 [BLOCKING] P1 scope, AC-1.1 and the per-phase plan disagree on which commands gain `--unattended`

- **Severity**: CRITICAL (a dimensional mismatch, FR-19). Graded blocking by consequence (below).
- **Experts**: Wiegers (traceability), Fowler (count annotation), Whittaker (divergence attack).
- **Where**: `SPEC:159` (P1 scope: "the `--unattended` flag accepted by every command in sections 3.1 and 3.2"), `SPEC:201` (AC-1.1: "every command in sections 3.1-3.2 has a `## Unattended mode` section naming `return-contract.yaml` and `~/.claude/WORKER-CONTRACT.md`"), `SPEC:76` ("Every changed command also gains the `## Unattended mode` section"), `SPEC:62` (WC-4: "Exempt: `load`"), `SPEC:112` (`load`: "none ... use it as a step ... not as its own Task"), `SPEC:267` (Decisions: a `load` report file "would be an unrequested addition"), `SPEC:154,231` (P4 waits for D2-D4), `SPEC:246` (D3 recommendation (a): "no pr-submit changes in Phase 4"), `SPEC:139` (pr-submit is a worker candidate "only if the user accepts D3").
- **Grading sentence**: An implementer who follows SPEC:159 and AC-1.1 as written adds the `## Unattended mode` section, with a flag that is accepted, to all 37 commands of sections 3.1 and 3.2 during P1. That includes `load` (which WC-4 exempts from the contract), `pr-submit` (which D3(a) says to leave unchanged), and 15 commands whose gates are not converted until P2 to P4. The result is wrong because `--unattended` is then accepted by `/sc:cleanup`, `/sc:cli-portify`, `/sc:task`, `/sc:roadmap` and others that still call `AskUserQuestion` or end on a chat offer. That breaks the WC-2 rule ("never calls `AskUserQuestion`") and gives a coordinator a flag that looks safe and stalls with no `worker_done`. AC-1.1 passes while WC-2 fails. It also contradicts the WC-4 and `load` exemption, and it settles D3 before the user decides.
- **Quantity Flow Diagram** (FR-21; see the end of the report): 37 worker-capable commands are asserted by AC-1.1, 17 are named in the P1 Commands column, so 20 are unscheduled by P1 (brainstorm and reflect from 3.1, plus 18 from 3.2).
- **Recommendation**: narrow SPEC:159 and AC-1.1 to the 17 commands the P1 Commands column names. State that each remaining command gains its section in its own phase. Exempt `load` from the section and from the `return-contract.yaml` assertion. Say where `brainstorm` (3.1, no phase row) is covered.
- **Priority**: High. **Quality impact**: Consistency +2, Testability +1.

### AUD-2 [BLOCKING] `--output <dir>` is applied to commands whose `--output` is a file, and the fixed contract name collides in a shared directory

- **Severity**: MAJOR. Graded blocking (two stated texts contradict).
- **Experts**: Adzic (example), Cockburn (primary actor: the coordinator's brief), Wiegers.
- **Where**: `SPEC:62` (WC-4: `<output-dir>/return-contract.yaml`, "the directory the coordinator passed (`--output` / `--output-dir`)"), `SPEC:202` (AC-1.2: "each P1 command with `--unattended --output <dir>`"), `SPEC:87` (`init-lite`: `--output <file>`), `SPEC:90` (`tdd`: `--output <file>`, contract "beside the TDD at `--output`"), `SPEC:69` (WC-11: two workers in one worktree never write the same file).
- **Grading sentence**: An implementer or tester who follows AC-1.2 as written runs `/sc:tdd ... --unattended --output <dir>` and `/sc:init-lite ... --output <dir>`. Those two commands take a file at `--output` (`SPEC:87,90`; `INV-A:55`, `INV-B:47`), so the TDD or audit report is aimed at a directory path and the check cannot pass. Separately, WC-4 gives one fixed contract name. For `tdd` and `init-lite` the contract goes "beside" a file, so two such workers whose output files share a directory (the default is `docs/[domain]/`, `INV-B:222`) write the same `return-contract.yaml`. That breaks WC-11.
- **Recommendation**: in AC-1.2, replace the generic `--output <dir>` with "the output flag listed for that command in section 3". In WC-4, say that for a file-valued output flag the contract is written in that file's directory under a name that includes the output file's stem. If the stem rule is too much to add, narrow instead and require the brief to give each file-valued worker its own directory.
- **Priority**: High. **Quality impact**: Testability +1.5, Consistency +1.

---

## === ARCHITECTURE ANALYSIS ===

Architecture findings below are Medium (follow-up candidates). None names a concrete wrong outcome on the stated text alone.

### AUD-3 [MEDIUM] The unattended switch has undefined edges: a quoted `--unattended`, no output flag, a section-4 command, and "refused" outcomes

- **Severity label**: MAJOR. **Graded**: Medium (needs a reading guess). **Experts**: Whittaker (sentinel collision, FR-2.3), Fowler.
- **Where**: `SPEC:51` ("when its caller passes `--unattended`"), `SPEC:128` (section-4 commands "get no `--unattended` mode"), `SPEC:60` (WC-2 allows only three resolutions, (a) to (c)), and the "refused under `--unattended`" rows at `SPEC:102,103,108,114,123`.
- I can break this specification by **Sentinel Collision Attack**. The invariant at **SPEC:51** fails when **`--unattended` appears inside a quoted topic or prompt**. Concrete attack: `/sc:tdd "document the --unattended flag" --output x.md` has a quoted argument containing the sentinel. Before: standalone mode, topic-only so it asks. After: a naive token match switches to unattended and resolves the topic-only gate as blocked. The spec never says the switch is a standalone, unquoted token (the sibling `/sc:spec-panel` definition does say it).
- Related cases the spec leaves open: `--unattended` with no output flag (WC-4 has no directory to write to); `--unattended` passed to a section-4 command (ignored or refused?); a "refused" row (for example `--monitor 1`, `--watch`) is not one of the WC-2 resolutions, and WC-4 says the contract is written on every outcome, so its `status` is undefined.
- **Recommendation**: add one sentence defining the token rule, one stating that a missing output flag resolves as blocked, and one mapping "refused" to `blocked`. **Priority**: Medium.

### AUD-4 [MEDIUM] WC-10 cannot be met by the fan-out commands that are most of the set, and its threshold differs from the stated margin and AC-4.3

- **Severity label**: MAJOR. **Graded**: Medium (the effect depends on whether Orca uses heartbeat age, UNVERIFIED at `CAPS:130,182`). **Experts**: Nygard, Whittaker (accumulation attack, FR-2.5).
- **Where**: `SPEC:68` (WC-10), `SPEC:272` (the 4-minute margin), `SPEC:216` (AC-4.3: no call over 240 s), `SPEC:24` (E4: commands keep their Agent-tool fan-out).
- I can break this specification by **Accumulation Attack**. The invariant at **SPEC:68** fails when **one tool call blocks longer than 5 minutes and cannot be split**. Concrete attack: `/sc:tdd` dispatches 6 to 10 codebase agents in one message (`INV-B:221`); the top-level session is inside one Agent-tool call for, say, 9 minutes. Heartbeats due at minutes 5 and 10 are not sent, because only the top-level session may send them (WC-7). WC-10 only tells commands to split waits such as polls and evals, and an Agent-tool call is not splittable.
- Threshold mismatch: WC-10 splits only calls "longer than 5 minutes" into waits "of at most 4 minutes", so a 4:30 call is unsplit and legal under WC-10. AC-4.3 and the pr-submit row (`SPEC:114`) require under 4 minutes.
- **Recommendation**: state what the worker does when a fan-out call outlasts the cadence (accept the gap, or heartbeat from a background step). Align the trigger with the margin (split at 4 minutes). **Priority**: Medium.

### AUD-5 [MEDIUM] WC-9's "paid external run" is ambiguous and could disable the web search that `research` and `review-translation` exist to do

- **Severity label**: MAJOR. **Graded**: Medium (two readings). **Experts**: Nygard, Hightower.
- **Where**: `SPEC:67` (WC-9 turns off "any default that ... calls a paid external run"), `SPEC:116` (`research`: web search is its purpose, `INV-B:134`), `SPEC:117` (`review-translation`: Tavily evidence search, `INV-B:144`), `SPEC:104` (`cli-eval`: real-model runs).
- If web search counts as a paid external run, the rows for `research` and `review-translation` produce no research. If it does not, WC-9 names the wrong thing for `cli-eval` and swarm. The rows themselves keep search on without saying so.
- **Recommendation**: list the outward actions WC-9 covers (push, PR, GitHub post, install, VM, real-model eval run) and say that read-only web search is not one. **Priority**: Medium.

### AUD-6 [MEDIUM] Gates that resolve as `blocked` have no stated way to be satisfied on the retry (cli-portify, and WC-3's "answer as a flag")

- **Severity label**: MAJOR. **Graded**: Medium (the requirement is missing, not contradicted). **Experts**: Whittaker (sequence attack, FR-2.4), Cockburn.
- **Where**: `SPEC:105` (`cli-portify`: each of the three approval gates "resolves as blocked ... with the artifact to review named"; adds `--resume <contract>`), `SPEC:61` (WC-3: re-invoke "with the answer as a flag").
- I can break this specification by **Sequence Attack**. The invariant at **SPEC:105** fails when **the person approves and the coordinator re-runs with `--resume`**. Concrete attack: Phase 2 ends at the approval gate, contract `status: blocked`, `resume_phase: 3` (`INV-A:45`). The re-run with `--resume <contract>` reaches the same gate. In unattended mode the gate always resolves as blocked, and the row defines no approval input, so the run blocks again and Phase 3 is never entered. The same shape exists for any other row that gives an answer flag only for some gates.
- **Recommendation**: name the approval flag for `cli-portify` (or treat resume from a blocked-at-gate contract as approval, with the coordinator's quoted instruction recorded), and add to WC-3 that a blocked gate row must name the flag that answers it. **Priority**: Medium.

### AUD-7 [MEDIUM] The acceptance checks AC-C1, AC-C4 and AC-C5 can pass while the rule they guard is broken

- **Severity label**: MAJOR. **Graded**: Medium. **Experts**: Crispin (boundary cases), Gregory, Whittaker.
- **Where**: `SPEC:172,178-182` (AC-C1), `SPEC:175` (AC-C4), `SPEC:176` (AC-C5), `SPEC:147` (SA-2), `SPEC:158` (P0 adds an Orca section to `HOW-WE-WORK.md` and the contract file, both under `src/superclaude/core`).
- AC-C1 is case-sensitive and matches only `orchestration|worktree|terminal|agent`. The guide's own notation `ORCA orchestration` (the spec uses it at `SPEC:167,186`), `orca-ide status` and `orca open` are not matched. The grep also scans `src/superclaude/core`, where P0 adds the contract file and the routing-guide Orca section. SA-2 allows one Orca mention "as an example of a caller's question channel inside the contract file", so the one permitted mention can fail the check.
- AC-C4 reads `git diff --cached`, so after a commit it prints nothing and the check passes vacuously. AC-C5 uses `grep -E '^-[^-]'`, which skips a deleted line that starts with `--` or `---` (a flag line, a frontmatter delimiter).
- **Recommendation**: use `master...HEAD` in AC-C4 as AC-C5 does, make AC-C1 case-insensitive with the broader verb list, and say whether the contract and routing guide are exempt from it. **Priority**: Medium.

### AUD-8 [MEDIUM] "Known before dispatch" (WC-4) is not true for three ready commands, and retry (WC-6) can reuse or leave a stale contract

- **Severity label**: MAJOR. **Graded**: Medium. **Experts**: Hohpe (message correlation), Nygard, Newman.
- **Where**: `SPEC:62` (WC-4 title and text), `SPEC:64` (WC-6), `SPEC:92` (`workflow`: contract at `.dev/tasks/to-do/<id>/`, id chosen at run time, `INV-B:272`), `SPEC:88,91` (`reflect` and `troubleshoot` default to timestamped directories, `INV-B:112,242`), `SPEC:204` (AC-1.4).
- The "Brief must pass" column for these three lists no output flag, so the path is learned only from `worker_done --report-path`. The P1 fix for `workflow` writes the contract on "pre-creation STOPs" (`SPEC:92`) and does not say where, because no `<id>` directory exists then.
- WC-6 tells a command with no resume flag to use "a fresh output directory", but a `--retry-of` worker is handed the same Task spec, so it gets the same directory. Either the first attempt's contract is overwritten (WC-6 broken), or the command picks a new subdirectory (WC-4's path is no longer known). The contract also carries no dispatch id or start time, so a coordinator cannot tell a stale file from a current one (the ids exist only in the preamble, `SPEC:35`).
- **Recommendation**: add an output-flag column to 3.1 for these three, say where a pre-creation `workflow` contract goes, and say who makes the retry directory fresh (the brief) and that the coordinator checks file time against dispatch time. **Priority**: Medium.

### AUD-9 [MEDIUM] P0 builds on the decision before the live runs that test it

- **Severity label**: MINOR to MAJOR. **Graded**: Medium. **Experts**: Fowler, Wiegers.
- **Where**: `SPEC:43` (1.4 (1): "Phase 0 therefore starts with live smoke runs"), `SPEC:158` (P0 scope writes the contract, the installer entry, the routing-guide section and the test file "Then run three ready commands"; "Why this order": the smoke runs test the decision "before anything is built on it"), `SPEC:200` ("a failure here reopens section 1").
- The scope text orders the build before the runs, which contradicts both quoted claims. If a smoke run fails, the routing-guide section and the installed contract file already exist.
- **Recommendation**: order the smoke runs first within P0, or drop the two claims. **Priority**: Medium.

### AUD-10 [MEDIUM] The `tasklist` row drops the inventory's required change without saying so, and leaves the `needs_human_decision` halt open

- **Severity label**: MAJOR. **Graded**: Medium. **Experts**: Newman, Nygard, Hohpe.
- **Where**: `SPEC:122`, `INV-B:46,209-210,215,314,322`, `INV-A:14`, `SPEC:274` (Decisions: the inventory verdicts are kept).
- INV-B (g) requires that "the per-phase reflect fan-out must run at the worker's top level, not inside subagents" (`INV-B:215`) and lists whether nested spawning works as UNVERIFIED (`INV-B:210,314`). The spec instead keeps Stage 10.5 in subagents and justifies it with the Claude Code nesting limit at `INV-A:14`. It gives no reasoning for overriding INV-B and does not carry the UNVERIFIED mark. It also does not say what happens when reflect halts on `needs_human_decision` items (`INV-B:209`) once `--unattended` is passed down. WC-2 would need a blocked outcome, which the row does not give. The row depends on a reflect `--unattended` that is itself a P2 change (`SPEC:88`), and both commands are in P2 with no order between them.
- **Recommendation**: record the departure from INV-B:215 in Decisions with its evidence, give the `needs_human_decision` resolution, and order reflect before tasklist inside P2. **Priority**: Medium.

### AUD-11 [MEDIUM] Two "defect fixes" widen what a plain, non-Orca run can do or how it loads

- **Severity label**: MAJOR. **Graded**: Medium. **Experts**: Newman (compatibility), Hightower.
- **Where**: `SPEC:108` (`explain`: "add Write to its tools"), `SPEC:102` (`business-panel`: move the frontmatter out of its code block, effect UNVERIFIED), `SPEC:146,149` (SA-1, SA-4).
- Adding Write to a command that today only has Read, Grep, Glob, TodoWrite and Task (`INV-A:48`) gives every standalone `/sc:explain` run a write capability, which SA-1 ("exactly today's behaviour") does not allow. The inventory could only infer that the output is chat (`INV-A:48`, UNVERIFIED). Moving the `business-panel` frontmatter changes how Claude Code loads it, which the spec itself marks UNVERIFIED.
- **Recommendation**: either make the explain change conditional on `--unattended` with a stated note about the tool grant, or move both rows out of the "defect fixes" list of SA-4. **Priority**: Medium.

### AUD-12 [MEDIUM] AC-2.2 cannot pass deterministically because WC-3 lets the worker ask instead, and `ask` has no bound

- **Severity label**: MAJOR. **Graded**: Medium. **Experts**: Crispin, Nygard.
- **Where**: `SPEC:61` (WC-3: the session "may instead ask the coordinator once ... wait"), `SPEC:206` (AC-2.2: gate-trigger run must end `--outcome failed` with `status: blocked`), `SPEC:187`, `CAPS:64,68`.
- A worker that follows the optional WC-3 asks and waits, so no `worker_done failed` arrives. The brief template in 2.3 (`SPEC:73`) does not say whether `ask` is allowed. There is also no cap on repeated `ask` timeouts: the worker resumes the same message id indefinitely and sends no heartbeat while blocked, so a coordinator that has gone away leaves it parked as "healthy" (`CAPS:52,129`).
- **Recommendation**: add to 2.3 whether the brief permits `ask`, and say that AC-2.2 runs with `ask` disallowed. State a maximum number of resumes. **Priority**: Medium.

---

## === ADVERSARIAL ANALYSIS (Whittaker) ===

Attacks that produced the findings above are recorded under AUD-3 (sentinel collision), AUD-4 (accumulation), AUD-6 (sequence). Two more attacks, with the state trace the template asks for:

1. I can break this specification by **Divergence Attack**. The invariant at **SPEC:159 / SPEC:201** fails when **the phase table's command list and the acceptance test's command list diverge**. Concrete attack: before, 43 commands, 37 worker-capable. P1 Commands column names 17. AC-1.1 asserts over 37. After P1 is "complete" per the Commands column, AC-1.1 fails for 20 commands. If the implementer instead satisfies AC-1.1, 15 gated commands accept a flag whose gates still prompt. Maps to AUD-1 (CRITICAL).
2. I can break this specification by **Zero/Empty Attack**. The invariant at **SPEC:63 (WC-5)** fails when **`return-contract.yaml` exists but is empty or lacks `status`**. Concrete attack: the command is killed after creating the file. WC-5 says failed only if "no report exists"; a file is present, `status` is absent, and the mapping is undefined. The 7.2 check (`SPEC:189`, `test -s`) catches this in tests, not in the worker's runtime rule. Severity MAJOR, graded Medium (a one-line fix: "empty, unparseable or unknown status counts as no report"). Recorded as a GAP in the table below and listed under follow-up candidates.

## Guard Condition Boundary Table (mandatory artifact)

Trigger: the spec contains thresholds and conditional mappings (WC-1, WC-3, WC-5, WC-10, the mode switch, the confidence rule, the acceptance greps). The table is complete: each guard has a row per applicable class, and omitted classes are listed under the table with their reason (FR-10). Every GAP is graded per FR-8/FR-9: none names a concrete wrong outcome on the stated text alone, so all are Medium and appear under follow-up candidates.

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|---|---|---|---|---|---|---|
| GC-1 outcome mapping | SPEC:63 (WC-5) | Zero/Empty | contract file present, 0 bytes or no `status` | "no report exists" unclear | not specified | GAP |
| GC-1 outcome mapping | SPEC:63 | One/Minimal | `status: succeeded`, `artifacts: []` | true | maps to `succeeded` (WC-4 permits `[]`) | OK |
| GC-1 outcome mapping | SPEC:63 | Typical | `status: failed` | true | `--outcome failed` | OK |
| GC-1 outcome mapping | SPEC:63,269 | Sentinel Value Match | `status: partial` | true | maps to `succeeded`, body states partial | OK |
| GC-1 outcome mapping | SPEC:62 | Sentinel Value Match | `status` outside the four values (for example `completed`) | unclear | not specified | GAP |
| GC-1 outcome mapping | SPEC:63 | Legitimate Edge Case | audit that ends with verdict FAIL | true | `succeeded` (stated) | OK |
| GC-2 wait split | SPEC:68 (WC-10) | One/Minimal | 1 s poll | false | unsplit | OK |
| GC-2 wait split | SPEC:68,114 | Typical | 600 s budget as poll-then-sleep iterations | false per iteration | heartbeat between iterations | OK |
| GC-2 wait split | SPEC:68 | Maximum/Overflow | one Agent-tool call of 9 min | true | "must be split", but cannot be | GAP |
| GC-2 wait split | SPEC:68,216,272 | Legitimate Edge Case | one call of 4 min 30 s | false (not over 5 min) | unsplit, but AC-4.3 demands 240 s or less | GAP |
| GC-3 readiness | SPEC:59 (WC-1) | Zero/Empty | `--timeout-ms` absent or not positive | true | Orca default 60 s (`CAPS:44`) | OK |
| GC-3 readiness | SPEC:59 | Typical | wrapper prompt falls back at 30 s | true | passes (`CAPS:49`) | OK |
| GC-3 readiness | SPEC:59 | Maximum/Overflow | wrapper fallback at 45 s or more | false | fails again (`CAPS:49`) | OK |
| GC-4 mode switch | SPEC:51 | Zero/Empty | no `--unattended` | false | standalone, unchanged (SA-1, `SPEC:146`) | OK |
| GC-4 mode switch | SPEC:51,62 | One/Minimal | `--unattended`, no output flag | true | no contract location defined | GAP |
| GC-4 mode switch | SPEC:51 | Typical | `--unattended --output <dir>` | true | unattended | OK |
| GC-4 mode switch | SPEC:51 | Sentinel Value Match | `--unattended` inside a quoted topic | unclear | not specified | GAP |
| GC-4 mode switch | SPEC:128 | Legitimate Edge Case | `--unattended` on a section-4 command | unclear | "no mode", effect not specified | GAP |
| GC-5 ask | SPEC:61 (WC-3) | Typical | one question answered | true | resume or re-run with the answer as a flag | OK |
| GC-5 ask | SPEC:61 | Maximum/Overflow | repeated timeouts, coordinator gone | true | resume same id, no upper bound | GAP |
| GC-5 ask | SPEC:60,61 | Legitimate Edge Case | no preamble | false | gate resolves as blocked (WC-2 (c)) | OK |
| GC-6 task confidence | SPEC:121 | Zero/Empty | confidence 0.0 | true | blocked | OK |
| GC-6 task confidence | SPEC:121 | Sentinel Value Match | exactly 0.70 | false | proceeds ("below 0.70" blocks) | OK |
| GC-7 grep AC-C1 | SPEC:172,178-182 | Sentinel Value Match | `ORCA orchestration`, `orca-ide status`, `orca open` | false | not matched | GAP |
| GC-7 grep AC-C1 | SPEC:147,158,181 | Legitimate Edge Case | the one Orca mention SA-2 allows, inside `src/superclaude/core` | true | check prints it, so it fails | GAP |
| GC-8 staged check AC-C4 | SPEC:175 | Zero/Empty | nothing staged because already committed | true | passes vacuously | GAP |
| GC-9 diff check AC-C5 | SPEC:176 | Legitimate Edge Case | deleted line starting `--` or `---` | false | not detected | GAP |

Omitted classes: GC-1 Maximum (no size or count dimension). GC-2 Zero (a zero-length wait never blocks) and Sentinel (no reserved value). GC-3 Sentinel and Edge (no reserved value; the one edge is the Maximum row). GC-4 Maximum (no capacity). GC-5 Zero, One and Sentinel (a question cannot be empty by construction; no reserved value). GC-6 One, Maximum and Edge (a continuous score, covered by the Zero and Sentinel rows). GC-7 to GC-9 Zero, One, Typical, Maximum (the acceptance checks have no numeric input beyond the rows shown).

## Quantity Flow Diagram (FR-21; Pipeline Dimensional Analysis, triggered by the inventory, phase and test chain)

```text
[Inventories: 43 commands (21 + 22)] --> [Partition 3.1 / 3.2 / 4] --> [10 ready + 27 changed = 37 worker-capable; 6 coordinator-only]
                                                                        |
                                                                        v
                                         [Phase table P1 Commands column: 17 named]   (SPEC:159)
                                         [P2 15, P3 4, P4 3 named (overlaps: init-lite, tdd, troubleshoot, release-split in P1 and P2)]
                                                                        |
                                                                        v
                                         [P1 scope sentence: expects 37]          <-- MISMATCH (SPEC:159)
                                         [AC-1.1 asserts a section on 37]         <-- MISMATCH (SPEC:201)
                                         [load exempt from contract (WC-4)]       <-- MISMATCH (SPEC:62 vs 201)
```

Conservation holds at the partition (43 = 10 + 27 + 6; distinct commands touched by a phase = 36, plus `brainstorm`, which has no change and no phase, plus 6 coordinator-only = 43). It breaks at P1 versus AC-1.1: 37 asserted, 17 scheduled, 20 unscheduled.

## === Roles of the other experts (consensus and disagreements) ===

- **Consensus**: the architecture decision (commands stay whole, Orca on top) is sound and well evidenced; the contract vocabulary (four statuses mapped to two Orca outcomes) is a good, small design; section 1.4 states the evidence gaps honestly.
- **Gregory (quality conversation)**: the spec says who should decide D1 to D5, but D1 and D4 are decisions that P1 and P2 depend on (`SPEC:154` says phases 1 to 3 need none; `SPEC:231` says phases 0 to 3 proceed on recommendations). The two statements differ and should be unified.
- **Hightower (operations)**: no worker has a stated total run-time bound (`SPEC:288`, UNVERIFIED 11), and there is no stated recovery for a worker killed mid-write; both are covered only by the coordinator opening the report (WC-4). Accepted as a stated non-goal, not a finding.
- **Disagreement noted**: Nygard and Whittaker rate AUD-4 and AUD-6 as MAJOR on label; Wiegers and Crispin grade them Medium because each needs a guess about the implementer or about Orca internals. Graded Medium here by the consequence rule.

---

## Follow-up candidates (Medium and minor; never trigger a revision)

Medium: AUD-3, AUD-4, AUD-5, AUD-6, AUD-7, AUD-8, AUD-9, AUD-10, AUD-11, AUD-12, plus the GAP rows of the Guard Condition Boundary Table (all Medium).

Minor notes:

- MIN-1 `SPEC:200` cites `SPEC:91` and `SPEC:267` cites "ladder rung 2". Neither shorthand is defined in the Citation conventions (`SPEC:7-11`).
- MIN-2 The `F-01` to `F-04` tags at `SPEC:62,85,159,172,178,188,200` refer to an earlier review that is not in this sandbox, so those tags cannot be checked. They are left in the final spec text as review-trail noise.
- MIN-3 `SPEC:62` states "Orca does not check the file" as fact; `CAPS:79,178` and `SPEC:280` say this is UNVERIFIED and only assumed.
- MIN-4 `SPEC:291` is numbered as UNVERIFIED item 14 but is a process note about the citation check, not an unverified fact. The "11 locations re-read" claim at `SPEC:11` and the "about 340 citations" claim at `SPEC:291` cannot be checked here.
- MIN-5 `SPEC:139` says `/sc:recommend` is better used on the coordinator side, yet `SPEC:115` and phase P2 schedule changes to it as a worker.
- MIN-6 `SPEC:100` introduces a positive `--post-pr` flag for `auggie-review`. Only `--no-post-pr` appears in the inventory (`INV-A:38`). The flag's existence is UNVERIFIED, and it is also named in D4 (`SPEC:250`).
- MIN-7 `partial` is one of the four statuses (`SPEC:62`) but no text says when a command reports it instead of `failed`.
- MIN-8 `SPEC:73` says the brief carries "the exact command line including `--unattended`", but the P0 smoke commands (`SPEC:200`) omit the flag because it does not exist yet in P0.
- MIN-9 `AC-C5` (`SPEC:176`) checks only `commands/<name>.md`, while most gate changes land in the skill files (`SPEC:88-92`), which no check covers. SA-1 for those is checked only by the manual AC-2.5 (`SPEC:209`).
- MIN-10 `SPEC:187` passes when `agentWait` is "never non-null". `CAPS:129` says an absent field means Orca never looked, so an absent field also passes.
- MIN-11 `SPEC:69` allows timestamp-only names for `save`'s per-session keys. Two workers writing in the same second would collide; AC-3.4 does not test it.

Follow-up issue question: the Review Loop asks the session that ran the review to ask the user once whether to open an issue for these follow-ups. This run is a worker whose final reply is restricted to the output path, so the question was not asked and no issue was created. The coordinator should ask.

## Brief clauses overridden

None. The brief narrowed nothing and widened nothing; it asked for a labelled whole-document first review, which is what this is.

## Reviser brief

Applies to the blocking finding ids AUD-1 and AUD-2 only. The reviser reads this report, not the command.

- Revise only text a blocking finding names. Leave minor notes and Medium findings alone, including AUD-3 to AUD-12 and the MIN items.
- Add no rule, mechanism or section that a blocking finding does not call for. Each added paragraph or table cites its finding id.
- Prefer deleting or narrowing text to adding. Report the byte size of the candidate before and after, and the bytes added and deleted per finding id.
- AUD-1: narrow `SPEC:159` and AC-1.1 (`SPEC:201`) to the commands the P1 Commands column names, exempt `load`, and say where `brainstorm` is covered. Do not add new phases or commands.
- AUD-2: in AC-1.2 (`SPEC:202`) replace `--output <dir>` with the output flag section 3 lists for each command, and make WC-4 (`SPEC:62`) state where a contract goes when the output flag is a file. Do not add new flags.
- Return the candidate once. Do not award yourself a PASS.

verdict: FAIL

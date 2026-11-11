review: 1 of 3

# Spec-panel audit: orca-worker-contract-spec.md (first review, whole document)

| Item | Value |
|---|---|
| Command | `/sc:spec-panel @.dev/orca-command-refactor/specs/orca-worker-contract-spec.md --mode critique --focus requirements,architecture` |
| Candidate | `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md` (285 lines) |
| Candidate SHA-256 | `e08236b563e957f919d430bee09f668cc4d154a475a77554660dd7026ed73de4` |
| Baseline | none (first review, whole-document audit; neither `--re-review` nor `--baseline` given) |
| Reviewer model actually used | claude-sonnet-5-5 |
| Prompt followed | FIRST-REVIEW prompt, `~/.claude/rules/prompts/document_review_loop_prompts.md` (read in full before reviewing) |
| Brief clauses that narrowed the command | "Write only your output file" and "Do not edit anything else": the Improve step (Behavioral Flow step 6) is not run and no improved spec is written. No brief clause widened scope or regraded a finding. |
| Panel seated | Wiegers (lead), Adzic, Cockburn (requirements); Fowler (lead), Nygard, Newman, Hohpe (architecture); Whittaker (always active). Crispin, Gregory and Hightower are not seated for these focus areas. |

## What was covered

Read in full: the README (binding context), the spec (285 lines), `inventory/commands-a.md`, `inventory/commands-b.md`, `inventory/orca-capabilities.md`.

Checked against the inventories: every `INV-A:N`, `INV-B:N` and `CAPS:N` citation in sections 1, 3 and 4 (each pointed at content that supports the claim, including all 43 per-command row ranges); the 10 / 27 / 6 split and that the 27 rows of 3.2 and 10 rows of 3.1 add up; the phase command lists in section 6 against the per-row phase tags; the acceptance checks in section 7 against the requirements they test; internal consistency of WC-1..WC-12, SA-1..SA-6, D1..D5.

UNVERIFIED (not checkable in this sandbox; the workspace holds only `.dev/orca-command-refactor/`): every citation to `src/superclaude/...` (`cmd/`, `sk/`), `CLAUDE.md`, `.dev/evals/...`, `.dev/codegraph-migration/...`, `pyproject.toml`, `Makefile`, `install_core.py`, and the claim that `grep -ci orca HOW-WE-WORK.md` printed 0 (spec line 25). Where a finding below relies on such text, it relies on the inventory's quotation of it. `[M2]`..`[M7]` tags in the spec (lines 62, 76, 83-86, 92, 112, 120, 158-159, 194-200) point at a revision log that is not in the workspace; I treated them as unexplained labels.

## Findings summary

| Id | Severity | Blocking | Bucket | One line |
|---|---|---|---|---|
| F-1 | CRITICAL (graded on consequence) | yes | Requirements | WC-4 promises a report path known before dispatch, but 8 section-3 rows give no way to know it, so AC-2.3 / 7.2 steps 3-4 cannot be applied to them |
| M-1 | Medium | no | Requirements | WC-6 "fresh output directory" contradicts WC-4 "directory fixed in the brief" on retry |
| M-2 | Medium | no | Architecture | WC-3 "ask once" is wrong for multi-gate commands and quietly pre-empts decision D2 |
| M-3 | Medium | no | Requirements | `--unattended` plus a person-mode flag is refused for some commands and unspecified for others |
| M-4 | Medium | no | Requirements | Claude Code tool-permission prompts are never addressed; they stall a worker the same way a command gate does |
| M-5 | Medium | no | Requirements | Phase 1 scope text, its Commands column, AC-1.1 and "Phases 1-3 need no user decision" disagree |
| M-6 | Medium | no | Requirements | WC-9 lets any brief authorize an outward action; D4(a) (still open) requires the user's own instruction |
| M-7 | Medium | no | Requirements | `/sc:workflow --output <file>` has no stated meaning; two contracts per run with no rule for which is reported |
| M-8 | Medium | no | Architecture | WC-11 covers output paths only; two ready commands have fixed output paths; source-editing workers in one worktree are not addressed |
| M-9 | Medium | no | Architecture | `partial` maps to `--outcome succeeded`, which settles the Task and releases dependents (CAPS:88, CAPS:90) |
| M-10 | Medium | no | Requirements | "Require an explicit output, else blocked" has no place to write the blocked contract |
| M-11 | Medium | no | Requirements | The fixed four-value `status` set is not checked against the statuses existing contracts already use |
| M-12 | Medium | no | Requirements | Acceptance checks: AC-C1 scope vs P0 deliverables, AC-2.4 can pass falsely, AC-C5 vs usage-line edits |
| M-13 | Medium | no | Architecture | No coordinator procedure for a `blocked` worker (retry with the answer) |
| N-1..N-5 | minor | no | both | Notes under follow-up candidates |

## === REQUIREMENTS ANALYSIS ===

Karl Wiegers (lead): "How would you validate compliance in production?" WC-4 is the load-bearing requirement of the whole spec (a report path the coordinator can name before dispatch and test in 7.2). It holds for the commands that already own an `--output` or `--output-dir` and fails for the rest. Several requirements are stated with an owner but without a test: WC-1 (no acceptance check except 7.2 step 1), WC-6, WC-12.

Gojko Adzic: "Can you provide concrete examples?" Section 7.2 gives one example per phase but none for the cases where the contract path is not derivable (research, recommend, save, task) or where a retry reuses a directory (WC-6).

Alistair Cockburn: "Who is the primary actor and what is the goal?" Two actors are conflated. The coordinator session and the worker session both appear as "the worker session" in WC-3, WC-5, WC-7, WC-10 and WC-12, but the spec never says how the worker session learns those rules (see M-4 and N-3).

### F-1 (blocking): WC-4 "known before dispatch" is unmet by 8 rows of section 3

Grading check: an implementer who follows WC-4 (line 62) and the section-3 rows as written builds, for `/sc:research`, `/sc:recommend`, `/sc:save`, `/sc:task`, `/sc:review-translation`, `/sc:cli-portify`, `/sc:cli-eval run` and `/sc:implement`, a return contract at a location the brief cannot state, and that is wrong because WC-4 and 2.3 require the report path to be known before dispatch ("The brief states the path", line 62; "so the report path is known before dispatch (WC-4)", line 73), and AC-2.3 / 7.2 step 3 ("its report path is the WC-4 contract path", line 182) and step 4 (`test -s <contract>` "the WC-4 path", line 183) have no path to test.

Evidence:
- WC-4 (line 62) defines exactly three path rules: `<dir>/return-contract.yaml` when the coordinator passed `--output` / `--output-dir` as a directory; `<file>.return-contract.yaml` when `--output` names a file; a fixed path "its section 3 row names". Line 76 repeats: "Contract means the WC-4 file at the path WC-4 gives".
- These rows pass none of the three:
  - research (line 116): "contract naming the generated `claudedocs/research_*.md` path"; no `--output` added; the report name is generated at run time (INV-B:132).
  - recommend (line 115): "write the handoff envelope to a file; contract"; no flag, no path.
  - save (line 119): "contract naming the file written"; no flag, no path.
  - task (line 121): "contract on every tier"; no flag, no path (today the only report is `tfep-incident-report.md` on TFEP, INV-B:202).
  - review-translation (line 117): "contract pointing at the `reports/localization/` files"; names carry a run-time suffix (INV-B:142); no flag.
  - cli-portify (line 105): "contract (fields already defined; file location unnamed)", the spec's own words.
  - cli-eval (line 104): "contract for both pipelines"; run output goes to `.dev/eval-runs/<date>/<run-id>/` (INV-A:44), `run-id` unknown before dispatch.
  - implement (line 109): "contract beside the ledger `progress.md`"; the ledger path is `.dev/implement/<slug>/progress.md` (INV-A:51), `<slug>` unknown before dispatch.
- Rows that do work: analyze, build, business-panel, cleanup, design, improve, index, test, spec-panel add an output path, and AC-1.2 pins the form (`--output <dir>`, line 196).

Why it is blocking and not a missing detail: the spec itself says the path must be known before dispatch, then supplies 8 rows where it cannot be, and its own live check (7.2 steps 3-4, run for every P2 and P4 command by AC-2.3 and AC-4.1) tests "the WC-4 path".

Alternative reading considered: the worker passes the contract path as `worker_done --report-path`, so the coordinator learns it afterwards. That reading contradicts line 73 and gives 7.2 step 4 nothing to check independently of the worker's own claim.

Recommendation (Wiegers, Fowler): for each of the 8 rows add the output flag (or a stated fixed location) that makes WC-4 rule 1, 2 or 3 apply, or relax WC-4 and 2.3 to say the path is read from `worker_done` for those commands and change step 4 accordingly. Priority: High. Quality impact: restores the testability of the core requirement.

## === ARCHITECTURE ANALYSIS ===

Martin Fowler (lead): The decision itself (Orca coordinates, commands stay units of work; section 1) is well argued: the rejection of commands calling Orca (R1-R5) is supported by `CAPS:97-103,145-150`, and the gaps are stated plainly in 1.4. The concern is the seam between the three roles: command (writes files), worker session (sends lifecycle messages), coordinator (reads files). Requirements WC-3, WC-5, WC-7, WC-10, WC-12 are owned by the worker session, a plain Claude session, and the spec names no mechanism that puts those rules in front of it except a core file the commands point to (line 52, P0 line 158). See N-3.

Michael Nygard: "What happens when this fails?" Failure paths covered: blocked gates, `consumer_fenced`, retry via `--retry-of`, circuit breaker (decisions line 263). Not covered: what the coordinator does with a `failed`/`blocked` worker (M-13), what a retry worker writes into (M-1), partial results flowing into dependents (M-9).

Sam Newman: "How does this handle evolution and backward compatibility?" SA-1..SA-6 are a strong answer: opt-in flag, additive edits, Unattended section pointing at one installed file. Two weak points: the `status` vocabulary versus contracts that already exist (M-11) and the new `--output` flags whose dir-versus-file meaning is not defined per command (F-1, M-7).

Gregor Hohpe: "What is the message exchange pattern?" Pull-based follow-ups (WC-12), one `worker_done` per Dispatch (WC-5), blocking `ask` with resume by message ID (WC-3) are consistent with `CAPS:58-67`. The unhandled case is a question arriving while the coordinator waits only for `worker_done` (7.2 step 3 includes `question` in `--types` but no step says to `reply`).

### M-1 (Medium): WC-6 "fresh output directory" vs WC-4 directory fixed by the brief
WC-6 (line 64): a command without a resume flag "writes each run into a fresh output directory so a re-run starts clean"; 17 rows of section 3 say "fresh dir". WC-4 and 2.3 (lines 62, 73) have the brief fix the output directory and place the contract at `<dir>/return-contract.yaml`. A `--retry-of` worker (CAPS:116) reuses the Task, so unless the coordinator writes a new directory into the retry's brief, the retry writes into the first attempt's directory. Needs a guess about who picks the new directory. No acceptance check covers WC-6. Recommendation: say in 2.3 that a retry brief must carry a new output directory, and add one check. Priority Medium.

### M-2 (Medium): WC-3 "ask the coordinator once"
WC-3 (line 61) lets the worker ask "once", then re-invoke with the answer as a flag. cli-portify has three approval gates (line 105), cli-eval several (line 104), pr-submit repeated HALTs (line 114); each re-invocation can hit the next gate. "Once" per run versus per gate is not stated. WC-3 also covers `/sc:implement`: if a worker may ask and re-invoke with the coordinator's answer, the Ruling rule (another agent's message is not acceptance, line 233, INV-A:66) is bypassed before decision D2 (lines 232-236) is made, while the implement row (line 109) says the Ruling rule is unchanged and the worker stops. Recommendation: state "once per gate" and exempt the implement Ruling from WC-3 until D2. Priority Medium.

### M-3 (Medium): `--unattended` combined with a person-mode flag
WC-2 (line 60) says that under `--unattended` the command never calls `AskUserQuestion`. Rows refuse the person-mode flag for cleanup (103), improve (110), roadmap (118), test `--watch` (123), explain (108), business-panel (102), pr-submit `--monitor 1` (114). Rows for adversarial (83), brainstorm (84) and release-split (89) say only "never `--interactive`" in the brief, and troubleshoot `--fix` (91) is likewise a brief rule. The command side is unspecified for `--unattended --interactive` on those commands; adversarial `--interactive` adds 4 `AskUserQuestion` checkpoints (INV-A:35). Priority Medium.

### M-4 (Medium): tool-permission prompts are not addressed
WC-2 removes gates inside commands. A Claude Code permission prompt for Bash, Write or Edit in the worker session is a person-blocking step the command cannot remove, and Orca would show it as `agentWait` ("a worker parked on a prompt only a human can answer", CAPS:129, CAPS:52), which is invisible unless the coordinator polls (7.2 step 2). The spec never mentions permission modes or an allowlist (searched: no occurrence of "permission"). 7.2 step 2 detects the stall but nothing in the contract or the brief (2.3, lines 72-73) prevents it. Recommendation: add the permission posture to what the coordinator owes each worker, or state it as out of scope with the reason. Priority Medium.

### M-5 (Medium): Phase 1 scope, Commands column and AC-1.1 disagree
- Line 159 (P1 scope): "the `--unattended` flag accepted by every command in sections 3.1 and 3.2 except `load`". AC-1.1 (line 195) asserts the `## Unattended mode` section on all of them. That is 36 commands.
- The P1 Commands column (line 159) names 13 (9 listed plus the four fixes adversarial, cleanup-audit, index-repo, workflow). Section 3.1 says brainstorm and init-lite need "None" (lines 84, 87); init-lite is then named in AC-1.2 (line 196) with a new `<file>.return-contract.yaml`, which is a change. Brainstorm and init-lite appear in no phase row.
- 3.1 intro (line 79): "The only command changes are the small fixes in the last column", contradicting AC-1.1.
- P1 therefore adds the section to implement, post-release and pr-submit, whose gate resolutions depend on D2-D4 (line 154 says "Phases 1-3 need no user decision; Phase 4 waits"), and D3(a) says "no pr-submit changes in Phase 4" (line 240). D1 (flag name, line 227) is also needed for P1 while line 154 says no decision is needed.
Quantity flow in the Pipeline Dimensional Analysis below shows the count mismatch (43 -> 37 -> 36 -> 13 named in P1). The command labels this class CRITICAL (FR-19); graded on consequence per the Review Loop, the effect is an inconsistent phase plan the first P1 check (AC-1.1) will expose, not a wrong shipped behavior, so Medium. Recommendation: list the P1 set from AC-1.1 and mark which sections are stubs until P4. Priority Medium.

### M-6 (Medium): who may authorize an outward action
WC-9 (line 67): off by default, "turns on only through the command's own explicit flag written in the brief". 2.3 (line 73): the brief states which outward actions are authorized. D4(a) (lines 244-247), still open, requires the user's own instruction naming the action. P2 (line 160) turns auggie-review posting and task commit/push off under `--unattended` and keeps the explicit-flag path, before D4 is decided (D4 itself lists auggie-review `--post-pr` and task `commit`/`push` as affected, line 244; line 154 and 225 say P1-P3 need no decision). Following WC-9 as written, a coordinator may write `--post-pr` into a brief on its own initiative. "A paid external run" in WC-9 is not defined (research web search, cli-eval real runs, swarm). Recommendation: put the D4(a) condition into WC-9 or make the explicit-flag path wait for D4. Priority Medium.

### M-7 (Medium): `/sc:workflow --output <file>`
Row 92 adds `--output <file>` and writes the contract at `<file>.return-contract.yaml` "because the package `<id>` is not known before dispatch", while the package contract `.dev/tasks/to-do/<id>/return-contract.yaml` "stays". The spec never says what `<file>` is (the command produces a package directory, INV-B:272), so the new contract sits next to a file that may not exist, and no rule says which of the two contracts is passed to `--report-path` or that they must agree. AC-0.4 (line 194) uses the package contract; AC-1.2 (line 196) the `--output` form. Priority Medium.

### M-8 (Medium): WC-11 scope
WC-11 (line 69) says two workers in one worktree must never write the same file and default output paths carry a timestamp or slug. Rows 85-86 keep fixed paths (`.claude-audit/`, `PROJECT_INDEX.md`) and answer with "one audit per worktree at a time", a coordinator constraint that appears in no brief rule (2.3). WC-11 is also silent on source files: cleanup, improve, build, document, test `--fix`, implement all edit the worktree (INV-A:43, 47, 51, 52; INV-B:234), and Orca shares the worktree by default (CAPS:115). Two such workers dispatched in parallel can overwrite each other's edits. Priority Medium.

### M-9 (Medium): `partial` maps to `--outcome succeeded`
WC-5 (line 63) and the decision at line 263. Orca settles the Task as completed on `succeeded`, and dependents become startable (CAPS:88, CAPS:90, CAPS:77). A partial deliverable then satisfies `--deps` of a following Task (for example `/sc:adversarial` on partial troubleshoot reports, line 39). The coordinator is told to open the report (line 73), but the Orca-level gate is open. Recommendation: map `partial` to `failed` or require the coordinator to hold dependents on `partial`. Priority Medium.

### M-10 (Medium): blocked because the output path is missing
document and post-release resolve "require an explicit output, else blocked" (rows 107, 113); WC-4 says the contract is written "including stops before any other output exists" (line 62) at a path derived from `--output`. When `--output` is the missing input there is no path. No fallback location is given. Priority Medium (see Guard table rows G-A1).

### M-11 (Medium): status vocabulary versus existing contracts
WC-4 requires `status` in `succeeded|partial|failed|blocked` and says commands with a contract "keep their fields and add the missing ones" (line 62). The decision at line 262 chose the fixed set instead of "copy each command's own statuses" without recording what the existing contracts (workflow `refs/return-contract.md`, brainstorm, reflect, adversarial) use. If any uses another value, "keep their fields" and the 7.2 step 4 assertion (line 183) cannot both hold. UNVERIFIED (those files are not in the workspace). Priority Medium.

### M-12 (Medium): acceptance checks that can mislead
- AC-C1 (line 172) scans `src/superclaude/core` and must "print nothing", while P0 (line 158) adds an Orca section to `core/HOW-WE-WORK.md` and a coordinator brief template to `core/WORKER-CONTRACT.md`, and SA-2 (line 147) allows an Orca mention in the contract file. Whether AC-C1 passes depends on wording the spec does not fix. Raw text also shows `\|` inside the commands (markdown-table escaping); copied literally the pipeline does not work.
- AC-2.4 (line 202) compares `gh api .../reviews --jq length` and `.../comments --jq length` before and after. Without `--paginate` each call returns at most one page (default 30), so a PR with 30 or more existing comments passes even if the command posted. This is the only check protecting WC-9 for auggie-review.
- AC-C5 (line 176) fails on any removed line, but the `## Usage` block of a command is a single line per form (for example the spec-panel Usage line); adding `--unattended` to it rewrites a line unless a new line is added. The spec does not say to add rather than edit.
Priority Medium.

### M-13 (Medium): the coordinator's side of `blocked`
WC-2(c) and WC-5 end a blocked worker `failed`. 2.3 (line 73) says what the coordinator does after `worker_done` only in the success case (open the report, release or reuse). Nothing says: read `blocked_question`, answer the person or decide, start `worker-start --retry-of` with the answer as a flag, expect a new output directory (M-1). Without it, WC-2(c) and the AC-2.2 checks leave the blocked task in `failed` with dependents stuck (CAPS:90). Priority Medium.

## === ADVERSARIAL ANALYSIS (Whittaker) ===

Review order note: Whittaker follows Fowler and Nygard in the sequence. Each finding uses the FR-3 template; severity is graded on consequence under the Review Loop.

W-1. I can break this specification by **Zero/Empty Attack**. The invariant at **WC-4 / line 62 and rows 105, 115, 116, 119, 121** fails when **`--unattended` is passed without any `--output` / `--output-dir` to a command with no fixed path**. Concrete attack: brief = `/sc:research "x" --unattended`; before: no directory, no flag in the row; after: research writes `claudedocs/research_x_<ts>.md` and a contract nobody can locate in advance; 7.2 step 4 has no `<contract>` argument. Severity: this is F-1 (blocking).

W-2. I can break this specification by **Sentinel Collision Attack**. The invariant at **WC-4 rule 2 / line 62** fails when **`--output` is a bare name such as `out` (no extension, not yet existing)**. Concrete attack: `/sc:tdd ... --output out` gives `out.return-contract.yaml` if read as a file, `out/return-contract.yaml` if read as a directory; two commands in the same repo (tdd `--output <file>`, spec-panel `--output <dir>`, lines 90, 120) disagree. Severity: Medium (the text allows the worse of two readings); see Guard table G-A2.

W-3. I can break this specification by **Sequence Attack**. The invariant at **WC-5 and WC-3 / lines 61, 63** (worker_done exactly once, from the top-level session) fails when **a gate blocks, the worker `ask`s, receives the answer, re-invokes, and the second run hits another gate**. Concrete attack: cli-portify gate 1 blocked -> `ask` -> `--resume` with approval -> gate 2 blocked -> "ask once" already spent (line 61) -> worker must end `failed` although the coordinator is available. Before: 0 asks used; after: 1 used, 2 gates open. Severity: Medium (M-2).

W-4. I can break this specification by **Divergence Attack**. The invariant at **WC-6 / line 64 against WC-4 / line 62** fails when **a retry is dispatched with the original brief**. Concrete attack: attempt 1 writes `D/REPORT.md` and dies; `worker-start --retry-of` re-runs with `--output D`; the command is told both to write into D (contract at `D/return-contract.yaml`) and into a fresh directory; either the partial `D/REPORT.md` is overwritten (first attempt corrupted) or the contract moves and 7.2 step 4 reads a stale file. Severity: Medium (M-1).

W-5. I can break this specification by **Accumulation Attack**. The invariant at **WC-10 / line 68** (heartbeat at most 5 minutes apart) fails when **a single wait is between 4 and 5 minutes and follows other work**. Concrete attack: 2 minutes of tool work, then a 4.5-minute wait (allowed: "longer than 5 minutes" must be split, a 4.5-minute call is not), 6.5 minutes between heartbeats. Severity: minor (N-4; the preamble cadence is itself stated from the worker's own preamble, CAPS:130).

## Guard Condition Boundary Table (hard gate FR-10: completed before synthesis)

Trigger: the spec contains conditional logic and thresholds (path selection, outcome mapping, 60 s / 5 min / 4 min limits, depth 1, confidence < 0.70, flag combinations). Lead: Nygard; completeness: Crispin (not seated, completeness validated by the lead against the six-class menu); attacks: Whittaker (W-1..W-5). Status GAP is graded under FR-8 / FR-9: blocking only with a concrete wrong outcome or safety risk; the only blocking one is the F-1 row.

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|---|---|---|---|---|---|---|
| G-A WC-4 path selection | line 62, rows 105/115/116/119/121 | Zero/Empty | no `--output`, no fixed row path | no rule applies | unspecified (F-1) | GAP |
| G-A WC-4 path selection | line 62, rows 107, 113 | Zero/Empty (the required output is the missing input) | `--output` absent where "else blocked" | no path to write the blocked contract | unspecified (M-10) | GAP |
| G-A WC-4 path selection | line 62 | One/Minimal | `--output out` (no extension, not existing) | dir or file | unspecified (W-2) | GAP |
| G-A WC-4 path selection | line 62 | Typical | `--output .dev/x/` existing dir | rule 1 | `<dir>/return-contract.yaml` | OK |
| G-A WC-4 path selection | line 62, rows 83-86 | Sentinel Value Match | fixed row path (adversarial `<output>/adversarial/...`) | rule 3 overrides rules 1-2 | stated | OK |
| G-A WC-4 path selection | line 62 | Legitimate Edge Case | `--output <file>` for workflow | contract beside a file that may not exist | unspecified (M-7) | GAP |
| G-B WC-5 outcome map | line 63 | Zero/Empty | report file present but zero bytes | "no report exists"? | unspecified | GAP |
| G-B WC-5 outcome map | line 63 | One/Minimal | `status` outside the four values | none of the branches | unspecified (M-11) | GAP |
| G-B WC-5 outcome map | line 63 | Typical | `succeeded` / `failed` / `blocked` | `succeeded` or `failed` | stated | OK |
| G-B WC-5 outcome map | line 63 | Legitimate Edge Case | `partial`; audit verdict FAIL | `succeeded` | stated, but see M-9 for `partial` | OK (M-9 note) |
| G-C WC-10 wait size | line 68 | Zero/Empty | no long wait | no split needed | not needed | OK |
| G-C WC-10 wait size | line 68 | Typical | 2 min call | no split | stated | OK |
| G-C WC-10 wait size | line 68 | Legitimate Edge Case | single call 4-5 min after other work | no split, heartbeat gap above 5 min | unspecified (W-5) | GAP (minor) |
| G-C WC-10 wait size | line 68, row 104 | Maximum/Overflow | eval up to 3600 s | split into waits of at most 4 min | stated | OK |
| G-D WC-3 ask | line 61 | Zero/Empty | session holds no preamble | ask not available | blocked only | OK |
| G-D WC-3 ask | line 61 | One/Minimal | first blocked gate | ask once, resume by message ID on timeout | stated | OK |
| G-D WC-3 ask | line 61, row 105 | Maximum/Overflow | second blocked gate after the answer | "once" spent | unspecified (M-2, W-3) | GAP |
| G-D WC-3 ask | line 61, row 109 | Legitimate Edge Case | implement Ruling question | answer from another agent | row 109 and D2 say the Ruling rule holds; WC-3 allows ask | GAP (M-2) |
| G-E `--unattended` x person-mode flag | rows 83, 84, 89, 91 | Sentinel Value Match | `--unattended --interactive` (or `--fix`) | prompts return | unspecified (M-3) | GAP |
| G-E `--unattended` x person-mode flag | rows 102, 103, 108, 110, 114, 118, 123 | Sentinel Value Match | `--unattended` with the flag | refused | stated | OK |
| G-F WC-9 outward default | line 67 | Typical | no flag | action off | stated | OK |
| G-F WC-9 outward default | line 67, line 244 | Legitimate Edge Case | flag written by the coordinator without a user instruction | action on | WC-9 allows; D4(a) forbids; D4 open (M-6) | GAP |
| G-F WC-9 outward default | line 67 | Sentinel Value Match | "paid external run" | undefined set | unspecified | GAP (minor) |
| G-G confidence < 0.70 (task) | row 121 | Typical | 0.65 | blocked | stated | OK |
| G-G confidence < 0.70 (task) | row 121 | Legitimate Edge Case | exactly 0.70 | not below, proceeds | inherited from `cmd/task.md:93` via INV-B:199 | OK |
| G-H depth 1 | lines 33, 66 | Typical | worker calls `worker-start` | refused | WC-8 forbids; refusal code cited | OK |
| G-H depth 1 | lines 33, 250-253 | Legitimate Edge Case | depth raised (D5 option b) | commands could call Orca | WC-8 still forbids | OK |
| G-I readiness 60 s | line 59 | Typical | fallback 30 s | passes | EVIDENCE.md:45 via CAPS:49 | OK |
| G-I readiness 60 s | line 59 | Maximum/Overflow | fallback near 45 s | fails again | "well inside" not quantified, the 45 s result is in CAPS:49 only | GAP (minor) |

Classes left out, with the one-line reason: G-D Maximum row for first ask (only one ask is possible per gate); G-G Zero/Empty (confidence is always computed by the command, UNVERIFIED); G-H Zero/Empty and Maximum (the setting is a whole number >= 1, malformed values fall back to the default, CAPS:100); G-E Zero/Empty (absence of the flag is the standalone case, SA-1). The table is complete.

## Pipeline Dimensional Analysis (triggered: multi-stage flow where counts change)

Quantity Flow Diagram (stage input N -> output M):

```text
[Source: 43 commands in cmd/ (INV-A 21 + INV-B 22)] --> [Stage 1: verdict split] --> [37 worker-capable (10 ready + 27 needs-change) | 6 coordinator-only]
                                                              |
                                                              v
[Stage 2: phase assignment, section 6 Commands column] --> [P1 13 named | P2 15 | P3 4 | P4 3 = 35 named]   <-- 2 unnamed (brainstorm, init-lite: "None")
                                                              |
                                                              v
[Consumer A: P1 scope text line 159 + AC-1.1 line 195: 36 (37 minus load) need the section] <-- MISMATCH with the 13 named in P1
[Consumer B: AC-1.2 line 196: "each P1 command except load" = 12 named]
[Consumer C: WC-4 contract path: 37 - (commands with an output flag or fixed path) = 8 undetermined (F-1)]
```

Stage 1 conserves the count (10 + 27 + 6 = 43; verified against the row lists). Stage 2 does not: 35 named of 37. The mismatch is recorded as M-5 (consequence-graded Medium) and F-1 (Consumer C).

State Variable Registry: not produced, `--focus correctness` is not active.

## Standard-format summary (YAML)

```yaml
specification_review:
  original_spec: .dev/orca-command-refactor/specs/orca-worker-contract-spec.md
  review_date: 2026-11-10
  expert_panel: [wiegers, adzic, cockburn, fowler, nygard, whittaker, newman, hohpe]
  focus_areas: [requirements, architecture]
quality_assessment:
  overall_score: 7.0
  clarity: 8
  completeness: 6
  testability: 6
  consistency: 7
critical_issues:
  - {category: requirements, severity: CRITICAL, expert: wiegers, issue: "F-1 WC-4 path unknowable for 8 rows", recommendation: "add output flag or fixed path per row, or relax WC-4/2.3 and 7.2 step 4"}
expert_consensus:
  - "The decision (Orca on top, commands as units) is sound and its evidence gaps are stated honestly (1.4)."
  - "The contract is not yet implementable as one uniform rule: report location, retry and blocked handling need closing."
improvement_roadmap:
  immediate: [F-1]
  short_term: [M-1, M-2, M-3, M-4, M-5, M-6, M-7, M-13]
  long_term: [M-8, M-9, M-10, M-11, M-12]
adversarial_analysis: see W-1..W-5
```

## Consensus and disagreements

Consensus: keep the architecture; fix the report-path rule first. Open point: Fowler and Nygard weigh M-9 (`partial` -> `succeeded`) higher than Wiegers, who accepts it because the body and contract still say `partial`; recorded as Medium.

## follow-up candidates (Medium and minor; none triggers a revision, none appears in the Reviser brief)

Medium: M-1, M-2, M-3, M-4, M-5, M-6, M-7, M-8, M-9, M-10, M-11, M-12, M-13 (details above).

Minor notes:
- N-1: 1.1 (line 16) says command changes are "limited to the worker contract"; SA-4 (line 149) and section 3 add drift fixes (roadmap, validate-roadmap, validate-tests, explain tools, business-panel frontmatter, load usage line). Adding Write to explain (row 108) changes standalone behavior and is not an obviously "documented defect" (INV-A:48 calls its output location an inference).
- N-2: the session's own command list shows `sc:graph`, `sc:impact`, `sc:issue` and `sc:index-repo`, which are not in either inventory (INV-A:3, INV-B:3 list 43). UNVERIFIED whether they exist at the spec's commit; the "43 commands" count is only as good as the two scope lines.
- N-3: WC-3, 5, 7, 10, 12 are owned by "the worker session", but 2.3 (lines 72-73) does not require the brief to point the worker at `~/.claude/WORKER-CONTRACT.md`; only the commands' Unattended sections do (line 52), so a worker running a command with no such section (a ready command before P1) has no source for the rules except this spec.
- N-4: WC-10 boundary for waits between 4 and 5 minutes (W-5); WC-1 "well inside" the readiness limit is unquantified (CAPS:49 holds the 30 s / 45 s evidence).
- N-5: P0 "its two mirrored copies" (line 158, SA-5 line 150): the second target in `CLAUDE.md` is a level-table copy into `core/CLAUDE.md`, not a mirror; and the UNVERIFIED list item 14 (line 285) says about 340 citations were re-read while the conventions block (line 11) says only 11 were re-read by this worker; both can hold but the sentences read as a conflict.
- Dangling labels `[M2]`..`[M7]` (see "What was covered").

Issue question for follow-up candidates: not asked and no issue created; this run cannot reach the user (final reply is fixed by the brief). The session that owns the loop asks once.

## Reviser brief

Blocking finding ids: F-1 only.

Rules for the reviser (restated from the Review Loop; the reviser reads this report, not the command):
- Revise only text finding F-1 names: WC-4 (line 62), the section-3 rows 104, 105, 109, 115, 116, 117, 119, 121, section 2.3 line 73, and 7.2 steps 3-4 only if WC-4 is relaxed instead.
- Add no rule, mechanism or section that F-1 does not call for; each added paragraph or table cell cites F-1.
- Prefer deleting or narrowing to adding (for example relax "known before dispatch" for the eight commands rather than adding eight flags, if that meets the requirement).
- Report the byte size of the spec before and after, and the bytes added and deleted per finding id.
- Leave Medium (M-1..M-13) and minor (N-1..N-5) findings alone; do not award yourself a PASS.

verdict: FAIL

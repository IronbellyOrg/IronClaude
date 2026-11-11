review: 1 of 3

# Spec-panel review, round 1: Orca worker contract spec

## Header

| Item | Value |
|---|---|
| command | `/sc:spec-panel @.dev/orca-command-refactor/specs/orca-worker-contract-spec.md --mode critique --focus requirements,architecture` |
| candidate | `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md` |
| candidate sha256 | `d3cdbe573e57303b9ce6c93d1fe98ba18fb7cb1a15773d926bf6a0c31425200d` |
| baseline | none (first review of the full document; no `--re-review`, no `--baseline`) |
| reviewer model | `claude-sonnet-5-5` (Sonnet 5.5) |
| review date | 2026-11-10 |
| prompt followed | FIRST-REVIEW prompt, `~/.claude/rules/prompts/document_review_loop_prompts.md` (read in full) |
| brief clauses overridden | none |
| `--iterations` | not given; this run is one review |

Citation keys. `SPEC:N` = line N of the candidate. `INV-A:N`, `INV-B:N`, `CAPS:N` = line N of `.dev/orca-command-refactor/inventory/commands-a.md`, `commands-b.md`, `orca-capabilities.md`; I read all three in full. `README:N` = `.dev/orca-command-refactor/README.md`. Every candidate quote below was re-found with `grep -nF` in the candidate. Citations that the spec or the inventories make to files outside the workspace (`src/`, `EVIDENCE.md`, `.dev/codegraph-migration/...`, `/opt/Orca/...`, `orca-ide` output) cannot be checked in this sandbox and are UNVERIFIED here. This includes the spec's self-attested checks at `SPEC:11` and `SPEC:285`, and its claim at `SPEC:25` that a grep over `src/` printed nothing for Orca.

Issue question: this worker has no user channel, so it does not ask whether to open an issue for the follow-up candidates and creates none. The coordinator asks once per loop.

## Grading summary

| Class | Count | Ids |
|---|---|---|
| Blocking (CRITICAL or concrete-wrong-outcome MAJOR) | 2 | F-1, F-2 |
| Medium (warning, under follow-up candidates) | 13 | M-1 to M-13 |
| Minor (note) | 4 | n-1 to n-4 |

Quality metrics (0 to 10): Clarity 7, Completeness 7, Testability 6, Consistency 6. The architecture decision (SPEC:13-45) is well supported by the inventories. The defects are in the contract's path rule and in the acceptance gates.

## Grading check for each blocking finding

**F-1.** An implementer who follows WC-4 as written for `/sc:tdd "auth" --unattended --output <file>` (the brief shape at SPEC:90 and in AC-2.2 at SPEC:200) builds a contract writer aimed at `<file>/return-contract.yaml`, and that is wrong because `<file>` is the TDD deliverable (a file, not a directory), so the `blocked` contract that AC-2.2 requires has no creatable path and `test -s <contract>` (SPEC:183) cannot pass. The same rule applied to `/sc:adversarial` gives `<output>/return-contract.yaml` while SPEC:83 fixes `<output>/adversarial/return-contract.yaml`, and for `/sc:workflow` the path holds a runtime `<id>` (SPEC:92) that cannot be "known before dispatch" (SPEC:73).

**F-2.** An implementer who follows SPEC:159 and AC-1.1 (SPEC:195) as written adds the WC-4 contract and an `## Unattended mode` section naming `return-contract.yaml` to `/sc:load`, and that is wrong because SPEC:112 and the Decision at SPEC:265 say `/sc:load` gets no report file ("a report file would be an unrequested addition"); an implementer who follows SPEC:112 instead cannot pass AC-1.1, and SPEC:154 makes P1's checks the gate for starting P2.

## === REQUIREMENTS ANALYSIS ===

Experts in order: Wiegers (lead), Adzic, Cockburn. Whittaker's attacks that bear on requirements are in the adversarial section below.

### F-1 (blocking, CRITICAL). WC-4's contract path rule contradicts the briefs and fixes that the spec itself gives
- Expert: Wiegers (consistency and testability), Adzic (the AC-2.2 example cannot be run as written).
- Stated texts that disagree:
  - SPEC:62: "where `<output-dir>` is the directory the coordinator passed (`--output` / `--output-dir`)".
  - SPEC:73: "the output directory, so the report path is known before dispatch (WC-4)".
  - SPEC:87 and SPEC:90: init-lite and tdd briefs pass "`--output <file>`" (a file). SPEC:200 (AC-2.2) runs `/sc:tdd "auth" --unattended --output <file>` and requires "contract `status: blocked` with a non-empty `blocked_question`".
  - SPEC:83: adversarial contract fixed to `<output>/adversarial/return-contract.yaml`, but WC-4 says `<output-dir>/return-contract.yaml`.
  - SPEC:92: workflow contract is `.dev/tasks/to-do/<id>/return-contract.yaml`, and the row passes no output directory. INV-B:272 says that contract is not written for pre-creation stops (`refs/return-contract.md:39`), so the spec's own fix "Write the contract for pre-creation STOPs too" (SPEC:92) has no `<id>` directory to write it into.
  - SPEC:182 and SPEC:183: step 3 requires "its report path is the WC-4 contract path"; step 4 runs `test -s <contract>`.
- Recommendation: state per command where the contract goes, as a table column, instead of one pattern; for commands whose `--output` is a file, name the contract path (for example a sibling `<file>.return-contract.yaml`, or a required `--report-dir`). For workflow, say where a pre-creation stop writes. Rationale: SPEC:73 promises the coordinator a path known before dispatch, and three of the ten "ready" commands cannot supply one under the current rule.
- Priority: High. Quality impact: raises Consistency and Testability by about 2 points each.

### F-2 (blocking, MAJOR with concrete wrong outcome). AC-1.1 and the P1 scope require a contract for `/sc:load`, which the spec says gets none
- Expert: Wiegers (traceability), Cockburn (the coordinator's goal for `/sc:load` is context, not a report).
- Stated texts that disagree:
  - SPEC:159 (P1 scope): "the `--unattended` flag accepted by every command in sections 3.1 and 3.2"; same row: "The WC-4 contract in unattended mode".
  - SPEC:195 (AC-1.1): "every command in sections 3.1-3.2 has a `## Unattended mode` section naming `return-contract.yaml` and `~/.claude/WORKER-CONTRACT.md`".
  - SPEC:76: "Every changed command also gains the `## Unattended mode` section".
  - SPEC:112 (load row): report "none (see note)"; "use it as a step inside another worker's brief, not as its own Task".
  - SPEC:265 (Decision): "a report file would be an unrequested addition".
  - SPEC:154: "Later phases do not start until the earlier phase's checks in section 7 pass."
- Recommendation: exclude `/sc:load` from AC-1.1 and from the WC-4 scope (say so in WC-4), or drop the Decision at SPEC:265. Rationale: the AC is a gate for starting P2 (SPEC:154), so the contradiction stalls the rollout or forces the file the Decision rejects.
- Priority: High. Quality impact: raises Consistency by about 1 point.

### M-1 (Medium; label MAJOR). Phase table, P1 scope and AC-1.1 do not line up, and a flag accepted as a no-op breaks WC-2 and WC-9 in the meantime
- Expert: Wiegers.
- Evidence: SPEC:159 scope says every command in 3.1 and 3.2, but its Commands column names 13 of the 37 worker candidates (analyze, build, business-panel, design, document, explain, index, test, load, plus fixes to adversarial, cleanup-audit, index-repo, workflow). Brainstorm and init-lite appear in no phase (SPEC:84, SPEC:87). Eighteen 3.2 commands are P2, P3 or P4 (SPEC:97-125). If P1 adds the flag to all of them, then `/sc:cleanup --unattended` (gates convert in P2, SPEC:103) and `/sc:pr-submit --unattended` / `/sc:post-release --unattended` (P4, SPEC:113-114; under D3 (a) pr-submit is never changed, SPEC:240) accept a flag whose WC-2 and WC-9 promises (SPEC:60, SPEC:67) they do not yet keep. A brief built per SPEC:73 would then run outward actions with a flag that says they are off.
- Why Medium: the sentence needs the guess that a coordinator dispatches a P2-P4 command before its phase lands; the text allows the reading "P1 adds stubs only".
- Recommendation: either make the stub explicit (an unconverted command refuses `--unattended` with a blocked contract until its phase lands) or limit P1 and AC-1.1 to the commands named in the P1 Commands column. Priority: High.

### M-2 (Medium; label MAJOR). WC-5 maps an existing but invalid report to `succeeded`
- Evidence: SPEC:63: "`--outcome failed` when the report says `failed` or `blocked`, or no report exists; `--outcome succeeded` otherwise". An empty file, unparseable YAML or a `status` outside the four values (SPEC:62 lets existing contracts "keep their fields", and INV-A:35 / INV-B:272 show their own field sets) falls into "otherwise". CAPS:77 says a valid `worker_done` settles the Task automatically, so a false success cannot be corrected by retry of that Task.
- Why Medium: it is an undefined state the document never states, not a text that does harm in a stated case. The check at SPEC:183 runs after `worker_done`.
- Recommendation: add "report missing, empty, unparseable, or status not in the four-value set: `failed`". Priority: High.

### M-3 (Medium; label MAJOR). WC-10 covers splittable waits only; fan-out waits cannot heartbeat
- Evidence: SPEC:68 splits a "single tool call" longer than 5 minutes into waits of at most 4 minutes. SPEC:65 (WC-7) forbids subagents from sending `heartbeat`. Most long steps are Task waves (INV-A:35, :42; INV-B:47), which block the top-level session for the whole wave and cannot be split. AC-4.3 (SPEC:210) checks heartbeats for pr-submit only. The 4-to-5-minute band is also uncovered: WC-10 triggers at "longer than 5 minutes", but SPEC:210 requires "no single tool call exceeds 240 s". CAPS:130 says it is UNVERIFIED whether Orca uses heartbeat age in the liveness verdict, so the consequence of a missed heartbeat is unknown.
- Recommendation: say what the worker does while blocked in a Task wave (accept the gap, or split the wave), and use one threshold (240 s) in both places. Priority: Medium.

### M-4 (Medium; label MAJOR). No behavior when `--unattended` has no usable output directory
- Evidence: SPEC:62 and SPEC:73 assume a coordinator-passed directory. Missing, unwritable, or inside `.git` or a distributable `.claude/` folder is not addressed; "written on every outcome, including stops before any other output exists" (SPEC:62) has no location to write when the directory is the thing that is missing. 3.2 rows only "add `--output`" (SPEC:99-108).
- Recommendation: define the refusal (chat only) and the unwritable-directory outcome. Priority: Medium.

### M-5 (Medium; label MAJOR). The `--unattended` switch is not defined as a token
- Evidence: D1 (SPEC:228) and SPEC:51 say "when its caller passes `--unattended`". A quoted topic such as `/sc:research "explain the --unattended flag"` is not distinguished from the flag, and passing it to a section 4 command (SPEC:128: "get no `--unattended` mode") is undefined. A wrong match in a person's session removes their prompts and breaks SA-1 (SPEC:146).
- Recommendation: define it as a standalone argument token outside quoted content, and say what a section 4 command does when given it (refuse). Priority: Medium.

### M-6 (Medium; label MAJOR). WC-3 allows "once", with no carve-out for gates that must come from a person
- Evidence: SPEC:61: "ask the coordinator once". cli-portify has three approval gates and no approve input (SPEC:105; INV-A:45), so after one `ask` and a re-invocation the next gate is undefined, and AC-2.3 (SPEC:201, "Happy-path run per P2 command") cannot show `succeeded` for it. WC-3 also has no carve-out for the `/sc:implement` Ruling that D2 (a) keeps person-only (SPEC:109, SPEC:233-236); a worker could ask, then re-invoke "with the answer as a flag". Step 2 of 7.2 (SPEC:181) requires `agentWait` never non-null, while CAPS:129 says a worker parked on a prompt shows `agentWait`; whether a worker blocked in `ask` sets it is UNVERIFIED.
- Recommendation: say "once per gate", add an approved-gate input for cli-portify, and list gates that `ask` may not satisfy. Priority: Medium.

### M-7 (Medium; label MINOR-to-MAJOR). WC-6 "fresh dir" has no owner, and two ready commands do neither option
- Evidence: SPEC:64 says a command either resumes or "writes each run into a fresh output directory". Whether the coordinator passes a new directory per attempt or the command mints one is not stated; the second breaks "known before dispatch" (SPEC:73), and WC-11 says default paths carry a timestamp (SPEC:69). init-lite "Re-run overwrites its marked report" and index-repo uses `mode=update` (SPEC:86-87), which overwrites the first attempt, the thing WC-6 says must not happen.
- Recommendation: state that the coordinator passes a distinct directory per attempt, and justify the two exceptions. Priority: Low.

### M-8 (Medium; label MAJOR). WC-9 uses terms the rows do not define
- Evidence: SPEC:67 turns off "a paid external run" and enables outward actions "through the command's own explicit flag". The spec does not say whether web search (research via Tavily, INV-B:134; review-translation, INV-B:144; recommend `--plugin`, INV-B:104) counts, yet the P2 happy-path check (SPEC:201) expects them to succeed. auggie-review needs a "`--post-pr`" flag (SPEC:100), but the inventory documents only `--no-post-pr` (INV-A:38), and post-release/task name no flag (SPEC:113, SPEC:121).
- Recommendation: list the outward actions per command with the exact enabling flag, new flags marked as new. Priority: Medium.

### M-9 (Medium; label MAJOR). The "additive edit" gates miss deleted bullets and skill files
- Evidence: AC-C5 (SPEC:176) and AC-0.3 (SPEC:193) pass when `grep -E '^-[^-]'` prints nothing. A removed line that begins with `-` (a markdown bullet, or a frontmatter `---`) appears in `git diff` as `--...` or `----`, and the pattern skips it. AC-C5 also covers `src/superclaude/commands/<name>.md` only, but most gates live in skills (for example SPEC:100, SPEC:104, SPEC:121 cite `sk/` files), so SA-1 (SPEC:146) is enforced only by AC-C3 and a manual step (AC-2.5, SPEC:203).
- Why Medium: the sentence needs an implementer who deletes a bullet that matters.
- Recommendation: use `git diff -U0 --diff-filter=M` with a count of removed lines (`^-` excluding the `---` header) and extend the path to the skill folders. Priority: Medium.

### M-10 (Medium; label MINOR). WC-11 omits other shared writers
- Evidence: SPEC:69 names memory keys overwritten whole. INV-B:154 says roadmap writes memory through `sc:save` at every wave, and INV-B:253 lists `.superclaude/memory/validate-roadmap/`; the roadmap row (SPEC:118) does not apply WC-11. Priority: Low.

### M-11 (Medium; label MAJOR). The tasklist row departs from the inventory and leaves a HALT
- Evidence: SPEC:122 passes `--unattended` to each reflect "so the headless rule applies". INV-B:215 recommended dropping `--remediate` in Stage 10.5; the spec's choice makes reflect auto-accept remediation inside every unattended tasklist run (INV-B:109). INV-B:209 notes that `needs_human_decision` items HALT; the row does not say how that halt resolves, so a WC-2 stall remains possible. UNVERIFIED whether the headless rule skips that halt. Priority: Medium.

### M-12 (Medium; label MINOR). Requirement traceability and decision gating
- Evidence: WC-1 (SPEC:59, owner "Launch setup, not commands") and WC-12 (SPEC:70) have no phase deliverable or acceptance check in section 6 or section 7. SPEC:154 says "Phases 1-3 need no user decision", but D4 (SPEC:244) lists auggie-review `--post-pr` and task `commit`/`push`, which are P2 rows (SPEC:100, SPEC:121); SPEC:225 says "Phases 0-3 can proceed on the recommendations". SPEC:16 says command changes are "limited to the worker contract in section 2", yet SPEC:149 (SA-4) and the "Other required change" column list defect fixes. Priority: Low.

### M-13 (Medium; label MINOR). Shared contract file availability and mirrors
- Evidence: each command depends on `~/.claude/WORKER-CONTRACT.md` for the shared rules (SPEC:52), but the spec does not say what `--unattended` does when that file is missing or older than the command. UNVERIFIED item 8 (SPEC:279) leaves the `plugins/superclaude/commands/` mirrors unresolved, and AC-C2 (`make verify-sync`, SPEC:173) checks `.claude/` only. The P0 "Orca section" in `HOW-WE-WORK.md` (SPEC:158) has no stated content, and AC-C1 (SPEC:172) scans `src/superclaude/core`, so natural content that names Orca verbs would fail P0. Priority: Low.

### Minor notes
- n-1. E3 (SPEC:23) is cited as "it has worked before", while SPEC:43 says the run proves the nested route; INV-A:14 records a routing quirk in that run that the spec does not mention.
- n-2. 7.2 step 6 (SPEC:185) expects only the brief's files in `git status --short`, but workers share a worktree by default (CAPS:115, SPEC:69), so parallel runs make it noisy.
- n-3. AC-1.3 (SPEC:197) uses "a scratch worktree" without saying how it is made; the project CLAUDE.md rules for worktree creation are not in this sandbox, so any conflict is UNVERIFIED.
- n-4. The 4-minute choice in the Decisions table (SPEC:266) restates SPEC:68; no conflict.

## === ARCHITECTURE ANALYSIS ===

Experts in order: Fowler (lead), Nygard, Newman, Hohpe.

- Fowler. The decision (Orca above, commands as units; SPEC:13-45) is sound and its rejection reasons R1 to R5 match CAPS:97-103, CAPS:145-150 and INV-A:90, INV-B:285-286. The interface is one flag, one report file, one resume rule; the seams that do not fit are in F-1 (path rule) and M-7. The 43 = 10 + 27 + 6 split is conserved against INV-A:73 (5/13/3) and INV-B:278 (5/14/3).
- Nygard. Failure modes: a missed heartbeat during a Task wave has no stated remedy (M-3); an invalid report is mapped to success (M-2); the contract file being absent is not handled (M-13). The `blocked` path through `failed` outcome (SPEC:63) is coherent with CAPS:90 (a failed Task keeps dependents blocked until `--retry-of` completes it).
- Newman. Versioning: the contract is shared by 37 commands but carries no version field and no rule for a command older than the contract (M-13). The status vocabulary (SPEC:262) is fixed while existing contracts keep their own fields (M-2).
- Hohpe. Message flow: `ask` (WC-3), `worker_done` (WC-5), `check` (WC-12) match CAPS:58-67 and CAPS:73-77. Gaps: "once" with several gates (M-6), and no statement of who mints the per-attempt output directory (M-7).

## Adversarial analysis (Whittaker, five attacks)

- Zero/Empty Attack. I can break this specification by **zero/empty input**. The invariant at **WC-4 and WC-5 (SPEC:62-63)** fails when **the output directory is absent or the report file is empty**. Concrete attack: `/sc:analyze src --unattended` with no `--output` has no contract location (M-4); a zero-byte `return-contract.yaml` left by a killed run exists, so WC-5 sends `--outcome succeeded` (M-2). Severity: Medium (undefined state).
- Divergence Attack. I can break this specification by **divergence at a boundary**. The invariant at **WC-10 (SPEC:68) versus AC-4.3 (SPEC:210)** fails when **a single wait lasts 4.5 minutes**. Concrete attack: before: last heartbeat at t=0; a poll of 4.5 minutes is allowed by "longer than 5 minutes" but fails "no single tool call exceeds 240 s"; after: the two texts disagree about pass or fail (M-3). Also, WC-4's pattern and SPEC:83 give two different paths for one adversarial run (F-1).
- Sentinel Collision Attack. I can break this specification by **sentinel collision**. The invariant at **D1 (SPEC:228) and SA-1 (SPEC:146)** fails when **user content contains `--unattended`**. Concrete attack: `/sc:tdd "add --unattended to tdd"` in a person's session; if the match is substring-based the command switches mode and drops the topic clarification (M-5). A second sentinel: `status: blocked` is both a report value and the WC-5 trigger for `failed`.
- Sequence Attack. I can break this specification by **sequence**. The invariant at **section 6 (SPEC:154) and AC-1.1 (SPEC:195)** fails when **P1's check needs files that later phases create**. Concrete attack: P1 completes the 13 named commands; AC-1.1 asserts all 37; P2 cannot start (F-2, M-1). Also: block, `ask`, re-invoke with the same output directory (WC-3 then WC-6) leaves the first contract overwritten or a nested directory, undefined (M-7).
- Accumulation Attack. I can break this specification by **accumulation**. The invariant at **WC-3 "once" (SPEC:61)** fails when **a command has more than one gate**. Concrete attack: cli-portify gate 1 answered, gate 2 reached, the one allowed ask is used, the run ends `blocked` and `failed`; AC-2.3 can never pass for it (M-6). Heartbeat gaps also accumulate across consecutive Task waves (M-3).

## Mandatory output: Guard Condition Boundary Table

Guards were found (thresholds, boolean switches, mapping rules), so the table is produced. Classes left out are listed in the one-line notes under the table. GAP rows each map to a finding id above (FR-8 and FR-9 grading: F-1 is blocking; the others are Medium because they name an undefined state, not a stated text that does harm).

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|---|---|---|---|---|---|---|
| unattended-switch | SPEC:51, SPEC:228 | Zero/Empty | flag absent | false | today's behavior (SA-1, SPEC:146) | OK |
| unattended-switch | SPEC:51, SPEC:228 | One/Minimal | `--unattended` as its own token | true | unattended mode on | OK |
| unattended-switch | SPEC:228 | Sentinel Value Match | quoted topic containing `--unattended` | not specified | none | GAP (M-5) |
| unattended-switch | SPEC:128 | Legitimate Edge Case | `/sc:git ... --unattended` (section 4 command) | not specified | none (only "get no `--unattended` mode") | GAP (M-5) |
| output-dir | SPEC:62, SPEC:73 | Zero/Empty | no output flag | not specified | none | GAP (M-4) |
| output-dir | SPEC:62 | One/Minimal | existing writable directory | true | contract at `<dir>/return-contract.yaml` | OK |
| output-dir | SPEC:62, SPEC:87, SPEC:90 | Sentinel Value Match | value is a file (`--output <file>`) | `<file>/return-contract.yaml` | not creatable; no alternative given | GAP (F-1) |
| output-dir | SPEC:83, SPEC:92 | Legitimate Edge Case | contract elsewhere (`<output>/adversarial/`, `<id>/`) | rule and row disagree | two paths for one run | GAP (F-1) |
| output-dir | SPEC:62 | Maximum/Overflow | unwritable, nonexistent, or inside `.git`/`.claude` | not specified | none | GAP (M-4) |
| outcome-map | SPEC:63 | Zero/Empty | no report file | failed | `--outcome failed` | OK |
| outcome-map | SPEC:63 | One/Minimal | report exists, zero bytes or unparseable | "otherwise" = succeeded | `--outcome succeeded` | GAP (M-2) |
| outcome-map | SPEC:63 | Typical | `status: succeeded` / `failed` / `blocked` | succeeded / failed / failed | as WC-5 | OK |
| outcome-map | SPEC:63, SPEC:262 | Sentinel Value Match | `status` outside the four values | "otherwise" = succeeded | `--outcome succeeded` | GAP (M-2) |
| outcome-map | SPEC:63 | Legitimate Edge Case | `status: partial`; audit verdict FAIL | succeeded | first sentence states the status | OK |
| wait-split | SPEC:68 | Typical | single wait up to 4 min | no split | none needed | OK |
| wait-split | SPEC:68, SPEC:210 | Legitimate Edge Case | wait of 4.5 min | WC-10 false, AC-4.3 false | texts disagree | GAP (M-3) |
| wait-split | SPEC:65, SPEC:68 | Maximum/Overflow | Task wave over 5 min | not splittable | none; subagents may not heartbeat | GAP (M-3) |
| ask-once | SPEC:50, SPEC:61 | Zero/Empty | no preamble | no lifecycle messages | resolve as blocked | OK |
| ask-once | SPEC:61 | Typical | one gate, one answer | true | re-invoke with the answer as a flag | OK |
| ask-once | SPEC:61, SPEC:105 | Maximum/Overflow | second gate after the allowed ask | not specified | none | GAP (M-6) |
| ask-once | SPEC:61, SPEC:233 | Legitimate Edge Case | gate that rejects agent answers (implement Ruling) | not specified | none | GAP (M-6) |
| outward-default | SPEC:67, SPEC:100 | Typical | explicit enabling flag in the brief | true | action on | OK |
| outward-default | SPEC:67, SPEC:113, SPEC:121 | Sentinel Value Match | no documented enabling flag; "paid external run" undefined | not specified | none | GAP (M-8) |
| task-confidence | SPEC:121 | Zero/Empty | confidence 0 or not computed | below 0.70 | blocked | OK |
| task-confidence | SPEC:121; INV-B:199 | Legitimate Edge Case | exactly 0.70 | not below | proceeds (the command gates only "< 0.70") | OK |
| additive-edit-grep | SPEC:176, SPEC:193 | Typical | removed prose line | matches | check prints, fails | OK |
| additive-edit-grep | SPEC:176, SPEC:193 | Legitimate Edge Case | removed bullet or `---` line | `--...` not matched | check prints nothing, passes | GAP (M-9) |
| fresh-or-resume | SPEC:64, SPEC:86-87 | Legitimate Edge Case | command with neither (init-lite, index-repo) | overwrite | not stated as allowed | GAP (M-7) |
| ac-1.1-scope | SPEC:195, SPEC:112 | Legitimate Edge Case | command in 3.2 with no report (`/sc:load`) | AC requires `return-contract.yaml` | row says no report | GAP (F-2) |

Left out with reasons: unattended-switch Maximum (a boolean has no overflow); output-dir Typical beyond the One/Minimal row (same case); outcome-map Maximum (the status set is closed); wait-split Zero (a zero-length wait needs no split) and One/Minimal (covered by Typical); ask-once One/Minimal (same as Typical); outward-default Zero and Maximum (the default is off, binary); task-confidence Maximum (1.0 is above the threshold, same behavior); additive-edit-grep Zero (an empty diff prints nothing, which is the intended pass); fresh-or-resume Zero (a first run has no prior output).

## Quantity Flow Diagram (Pipeline Dimensional Analysis)

Trigger: the spec filters 43 commands to 37 workers and then spreads them over phases (N differs from M at two stages). No count mismatch: the numbers conserve against SPEC:76 and the phase rows.

```text
[43 commands: INV-A:3 (21) + INV-B:3 (22)] --> [Classify: 10 ready / 27 change / 6 coordinator-only, SPEC:76]
    |--> [6 coordinator-only: SPEC:128-137]                    (no phase)
    |--> [37 worker candidates = 10 + 27]
            |--> [Phase assignment, SPEC:156-162 vs SPEC:81-125]
                    P1: 13 named (9 from 3.2, 4 fixes from 3.1)
                    P2: 15 named (11 from 3.2, 4 from 3.1)
                    P3: 4   P4: 3
                    no phase: brainstorm, init-lite (2)
                    13 + 15 + 4 + 3 + 2 = 37
    [Consumer AC-1.1 (SPEC:195): expects 37 at P1]   <-- MISMATCH with 13 (see F-2, M-1)
```

## Coverage

Covered: the whole candidate (SPEC:1-285), its three inventories (all lines), and the README. The panel ran in the fixed order Wiegers, Adzic, Cockburn, Fowler, Nygard, Whittaker, Newman, Hohpe, Crispin (acceptance checks: M-9, n-2), Gregory (workshop and quality conversation: no finding), Hightower (operational: M-3, M-13). Not covered: any file outside the workspace; the spec's citations to such files, to `orca-ide` output, and to `/opt/Orca/...` are UNVERIFIED here. Not run: the spec's own commands (greps over `src/`, `make`, `uv run`); they need the live repository. The command's `--focus correctness` outputs (State Variable Registry) are not produced because that focus was not requested; the spec introduces no mutable state variable beyond the status fields reviewed above. `--format` was not given; the report uses the critique-mode bucket layout.

## follow-up candidates

Medium (warnings): M-1, M-2, M-3, M-4, M-5, M-6, M-7, M-8, M-9, M-10, M-11, M-12, M-13.
Minor (notes): n-1, n-2, n-3, n-4.
These never trigger a revision, never fail a review and are not in the Reviser brief.

## Reviser brief

Blocking finding ids: F-1, F-2.

Findings, copied from this report:

- **F-1.** Texts: SPEC:62 "where `<output-dir>` is the directory the coordinator passed (`--output` / `--output-dir`)"; SPEC:73 "so the report path is known before dispatch"; SPEC:90 "a precise component prompt, not a bare topic; `--output <file>`" and SPEC:87 (init-lite, `--output <file>`); SPEC:200 "`/sc:tdd "auth" --unattended --output <file>`" with "contract `status: blocked` with a non-empty `blocked_question`"; SPEC:83 "Fix the contract filename to `<output>/adversarial/return-contract.yaml`"; SPEC:92 ".dev/tasks/to-do/<id>/return-contract.yaml"; SPEC:182 "its report path is the WC-4 contract path"; SPEC:183 "`test -s <contract>`". Wrong outcome: An implementer who follows WC-4 as written for `/sc:tdd "auth" --unattended --output <file>` builds a contract writer aimed at `<file>/return-contract.yaml`, and that is wrong because `<file>` is the TDD deliverable (a file, not a directory), so the `blocked` contract that AC-2.2 requires has no creatable path and `test -s <contract>` cannot pass; the same rule gives adversarial a different path from SPEC:83 and workflow a path with a runtime `<id>` that is not known before dispatch.
- **F-2.** Texts: SPEC:159 "the `--unattended` flag accepted by every command in sections 3.1 and 3.2"; SPEC:195 "every command in sections 3.1-3.2 has a `## Unattended mode` section naming"; SPEC:112 "use it as a step inside another worker's brief, not as its own Task"; SPEC:265 "a report file would be an unrequested addition"; SPEC:154 "Later phases do not start until". Wrong outcome: An implementer who follows SPEC:159 and AC-1.1 as written adds the WC-4 contract and an `## Unattended mode` section naming `return-contract.yaml` to `/sc:load`, and that is wrong because SPEC:112 and SPEC:265 say `/sc:load` gets no report file; an implementer who follows SPEC:112 instead cannot pass AC-1.1, which gates the start of P2.

Reviser contract (restating Review Loop bullet 6 of the command): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id. Leave minor and Medium findings alone.

verdict: FAIL

review: 1 of 3

# Spec-panel review, round 1: Orca worker-contract spec

- Command: `/sc:spec-panel @.dev/orca-command-refactor/specs/orca-worker-contract-spec.md --mode critique --focus requirements,architecture`
- Review prompt followed: FIRST-REVIEW prompt of `~/.claude/rules/prompts/document_review_loop_prompts.md` (read in full). Values: candidate = `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`.
- Candidate sha256: `d3cdbe573e57303b9ce6c93d1fe98ba18fb7cb1a15773d926bf6a0c31425200d`
- Baseline: none (first review; no `--re-review` / `--baseline` given, so no `baseline: missing` note is needed).
- Reviewer model used: Sonnet 5.5 (`claude-sonnet-5-5`). Review date 2026-11-10.
- Citation shorthand: `SPEC:N` = line N of `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`; `INV-A:N`, `INV-B:N`, `CAPS:N` = line N of `inventory/commands-a.md`, `commands-b.md`, `orca-capabilities.md`; `README:N` = `.dev/orca-command-refactor/README.md`.
- Brief clauses overridden: none. The brief asked for the FIRST-REVIEW prompt and asked nothing the command forbids.

## What I covered

- Read in full: the candidate (285 lines), README, all three inventories, command.md and the review-loop prompts file.
- Checked every `INV-A:N`, `INV-B:N`, `CAPS:N` and `README:N` citation in SPEC sections 1-4 against the inventory files. Each line holds what the spec says it holds. The exceptions are the overstated or reinterpreted items in M-9.
- Citations to files outside the sandbox cannot be checked and are **UNVERIFIED** here. That covers the whole `cmd/`, `sk/`, `ag/` set, `CLAUDE.md`, `Makefile`, `pyproject.toml`, `install_core.py`, `EVIDENCE.md`, the codegraph `orchestration/README.md` and `return-contract.yaml`, and the Orca guide text. It also covers the spec's own claims that 11 locations were re-read (`SPEC:11`), that the E5 greps were run (`SPEC:25`), and that a validator checked about 340 citations (`SPEC:285`).
- Focus: requirements (Wiegers, Adzic, Cockburn) and architecture (Fowler, Nygard, Newman, Hohpe), with Whittaker, Crispin and Gregory/Hightower reviewing in the fixed order. `--focus correctness` is not active, so no State Variable Registry is produced.
- The Guard Condition Boundary Table is produced (the spec has thresholds and guards). The Quantity Flow Diagram is produced because the phase rollout is a staged flow.
- Not covered: the content of the 43 command files, because they are outside the sandbox. Every claim about their text rests on the inventories.

## Findings table

| id | Severity as graded | Blocking? | Title | Expert |
|---|---|---|---|---|
| B-1 | CRITICAL | yes | AC-1.1 and the P1 scope contradict the per-command rows, the phase assignments and open decision D3 | Wiegers, Fowler |
| B-2 | CRITICAL | yes | WC-3 lets a coordinator answer unlock a gate that D2(a), D4(a) and WC-9 say only a person or the brief can unlock | Nygard, Whittaker |
| B-3 | MAJOR | yes | WC-4's `<output-dir>/return-contract.yaml` has no valid meaning where `--output` is a file path | Wiegers, Adzic |
| M-1 | MAJOR (graded Medium) | no | AC-0.4 requires a WC-4 contract path that does not exist in Phase 0 | Crispin |
| M-2 | MAJOR (graded Medium) | no | WC-6 "fresh output directory" conflicts with a coordinator-fixed output dir, and nothing guards a stale contract | Nygard, Whittaker |
| M-3 | MAJOR (graded Medium) | no | Contract location is not one rule: workflow pre-creation STOPs and adversarial differ from WC-4 | Fowler, Hohpe |
| M-4 | MAJOR (graded Medium) | no | WC-10 covers only Bash-style waits and leaves a 4-5 minute gap that AC-4.3 does not share | Nygard |
| M-5 | MAJOR (graded Medium) | no | `--unattended` with no output location is undefined | Whittaker |
| M-6 | MINOR-to-MAJOR (graded Medium) | no | AC-C1 and AC-C5 may fail on the spec's own deliverables | Crispin |
| M-7 | MAJOR (graded Medium) | no | auggie-review "explicit `--post-pr`" is a flag the inventory does not show exists | Wiegers |
| M-8 | MAJOR (graded Medium) | no | Rollout window: P1 accepts `--unattended` on gated commands before P2 converts the gates | Newman, Whittaker |
| M-9 | MAJOR (graded Medium) | no | Stated-as-fact claims that the spec's own UNVERIFIED list or the inventories do not support | Wiegers |
| M-10 | MAJOR (graded Medium) | no | Requirements WC-1, WC-3, WC-6, WC-12 and WC-10 (non-pr-submit) have no acceptance check | Crispin, Gregory |
| M-11 | MAJOR (graded Medium) | no | "Ask once" in WC-3 against cli-portify's three gates | Cockburn |
| M-12 | MAJOR (graded Medium) | no | The plugin mirror's update rule is deferred to each phase plan | Newman |
| N-1 | MINOR | no | E2 says the worker "answered"; the inventory line shows only `ready` | Wiegers |
| N-2 | MINOR | no | AC-C1 text carries `\|` table escapes inside the command | Crispin |

## === REQUIREMENTS ANALYSIS ===

### B-1 (CRITICAL, blocking): AC-1.1 and the P1 scope contradict the rows, the phases and D3

Grading check. An implementer who follows the stated text as written builds an `## Unattended mode` section naming `return-contract.yaml` in all 37 commands of sections 3.1 and 3.2 during Phase 1. That includes `load`, `implement`, `post-release` and `pr-submit`. This is wrong because the spec's own text says otherwise for each of them.

Evidence:
- `SPEC:159` (P1): "the `--unattended` flag accepted by every command in sections 3.1 and 3.2".
- `SPEC:195` (AC-1.1): the test "asserts that every command in sections 3.1-3.2 has a `## Unattended mode` section naming `return-contract.yaml` and `~/.claude/WORKER-CONTRACT.md`". It passes only at that completeness.
- `SPEC:112` (the `load` row): Report is "none (see note)", resume "n/a", and the note says to use it as a step inside another worker's brief. `SPEC:265` (Decisions): "a report file would be an unrequested addition". The AC requires the section to name `return-contract.yaml` for `load`, so the AC and the row contradict each other.
- `SPEC:162` and `SPEC:154`: `implement`, `post-release` and `pr-submit` belong to P4, and "Phases 1-3 need no user decision". Their unattended sections depend on D2, D4 and D3 (`SPEC:109`, `SPEC:113`, `SPEC:114`, `SPEC:232-247`). P1 cannot write them without the answers.
- `SPEC:139` and `SPEC:240`: under the recommended D3(a), `pr-submit` is "coordinator or person only", with "no pr-submit changes". AC-1.1 still requires its section in P1.
- `SPEC:160`: 15 commands get their gate resolutions in P2, so their P1 sections cannot yet say what the AC wants them to say (see M-8).

A reader cannot satisfy P1 as written without either breaking the `load` decision or pre-empting D2-D4. Recommendation (Reviser): restrict the P1 flag and AC-1.1 scope to the P1 rows of section 3 (the 9 P1 commands in section 3.2 plus the 4 named fixes in section 3.1), or move the assertion to each command's own phase. Delete `load` from the assertion.

### B-3 (MAJOR graded blocking): WC-4's contract path has no valid meaning where `--output` is a file

Grading check. An implementer who follows the stated text as written writes the contract at `<value of --output>/return-contract.yaml` for `/sc:tdd ... --output docs/x/TDD_FOO.md --unattended`, so at `docs/x/TDD_FOO.md/return-contract.yaml`. That is wrong because `TDD_FOO.md` is the TDD file, not a directory. The spec names no other location.

Evidence:
- `SPEC:62` (WC-4): "`<output-dir>/return-contract.yaml`, where `<output-dir>` is the directory the coordinator passed (`--output` / `--output-dir`)".
- `SPEC:90` (tdd row): "`--output <file>`; the TDD at `--output`" (INV-B:222). `SPEC:87` (init-lite): `--output <file>` (INV-A:55). `SPEC:120` (spec-panel): "add `--output`" with no kind given (INV-B:182 shows no flag today).
- `SPEC:200` (AC-2.2): `/sc:tdd "auth" --unattended --output <file>`, expecting "contract `status: blocked`". The AC cannot say where to read the contract.
- `SPEC:73` (2.3): the brief gives "the output directory, so the report path is known before dispatch". A file-valued `--output` cannot serve as that directory.

The spec never defines a contract location for a command whose `--output` is a file. Recommendation: define one rule, for example a separate directory flag or "the directory containing the file", and apply it to tdd, init-lite and spec-panel.

### M-1 (Medium): AC-0.4 requires a WC-4 contract path that does not exist in Phase 0

`SPEC:194` says "steps 1-3 and 5-7 pass; step 4 uses the command's existing report file". `SPEC:182` (step 3) passes only if "its report path is the WC-4 contract path" and `--outcome` matches "the contract's `status` under WC-5". `SPEC:79` says that until P1 "the worker reports the named file". For `troubleshoot` that file is `REPORT.md` (`SPEC:91`), which is markdown, not a WC-4 contract. Step 4's `yaml.safe_load` also cannot pass on it. The intended reading is clear, but the literal text is not passable, and a failure "reopens section 1" (`SPEC:194`). Medium because it needs the reader to guess the intended reduction.

### M-5 (Medium): `--unattended` with no output location is undefined

WC-4 and 2.3 assume the brief supplies a location (`SPEC:62`, `SPEC:73`). Several rows add `--output` as new (`SPEC:99`, `SPEC:101`, `SPEC:106`, `SPEC:120`). No text says what a command does when `--unattended` arrives without it: refuse, default, or write nowhere. WC-2 requires a report on "every outcome" (`SPEC:60`, `SPEC:62`), so silence is a gap. Not a stated text that does harm, so Medium.

### M-7 (Medium): `--post-pr` as an enabling flag

`SPEC:100` has posting "return only with an explicit `--post-pr` in the brief", and D4(a) depends on it (`SPEC:245`). INV-A:38 shows `--no-post-pr` (C:52) and a default-on posting, but no positive flag. The spec does not list `--post-pr` as new, so an implementer could miss it. With no such flag, D4(a) cannot be honoured for auggie-review.

### M-10 (Medium): requirements with no acceptance check

Section 7 covers WC-2, WC-4, WC-5, WC-7, WC-8, WC-9 and WC-11 (save only) and WC-10 for pr-submit only. These have no check: WC-1's fallback value (`SPEC:59` says "well inside"), WC-3 (the `ask` and `reply` path), WC-6 (`--retry-of`, `SPEC:64`), WC-12 (`consumer_fenced`, `SPEC:70`), and WC-10 for cli-eval (`SPEC:104`). Missing coverage, not a text that does harm.

### M-11 (Medium): "ask once" against several gates

WC-3 allows the session to "ask the coordinator once" (`SPEC:61`). cli-portify has three approval gates (`SPEC:105`, INV-A:45). It is not stated whether "once" is per gate or per invocation. Whether the worker may block at a later gate after a re-invoke is not stated either.

### N-1 (MINOR): E2 wording

`SPEC:22` says the worker "reached `state: ready, stage: input_accepted` and answered". The inventory line CAPS:49 quotes only the ready state. The word "answered" is not shown at that line.

## === ARCHITECTURE ANALYSIS ===

### B-2 (CRITICAL, blocking): WC-3 against D2(a), D4(a) and WC-9

Grading check. An implementer who follows the stated text as written builds a worker that, when `/sc:implement` halts with `E-HALT-QA` (a gate that "resolves as blocked", `SPEC:109`), asks the coordinator and re-invokes the command "with the answer as a flag". This is wrong because the Ruling rule rejects "another agent's message" (INV-A:51 and INV-A:66, citing `refs/qa.md:238`; UNVERIFIED at source). The spec's own D2(a) and AC-4.1 require the worker to end `failed`. That is a safety-boundary risk, because the rule exists to stop an agent approving its own work (`SPEC:236`).

Evidence:
- `SPEC:61` (WC-3): "When a gate would resolve as blocked and the worker session holds a preamble, the session may instead ask the coordinator once ... then re-invoke or resume the command with the answer as a flag".
- `SPEC:234` (D2(a), recommended): "The worker stops, writes the halt to its ledger and contract, and ends `failed`." `SPEC:208` (AC-4.1) tests exactly that.
- `SPEC:67` (WC-9): outward defaults turn on "only through the command's own explicit flag written in the brief". `SPEC:245` (D4(a)): only when "the user's own instruction to the coordinator names that action".
- WC-3 is generic and has no carve-out for the Ruling, for outward-action flags, or for any gate whose answer must come from a person.

Concrete state trace. Before: `implement` halted, ledger records `E-HALT-QA`, contract `status: blocked`. Worker `ask`s, the coordinator replies "approved", the worker re-invokes with the reply. After: a Ruling recorded from an agent's message, against `qa.md:238`. The same path would let a coordinator reply switch on a post-release install flag that no user instruction named (`SPEC:113`).

Recommendation: restrict WC-3 so that the answer may supply only values no safety rule or outward-action rule reserves, and name `implement`'s Ruling and every WC-9 flag as excluded.

### M-2 (Medium): fresh output dir against a coordinator-fixed dir, and a stale contract

- WC-6 says that without a resume flag a command "writes each run into a fresh output directory" (`SPEC:64`). WC-4 and 2.3 fix the directory in the brief (`SPEC:62`, `SPEC:73`). A retry started with `worker-start --task ... --retry-of` reuses the Task spec and so the same directory (`CAPS:116`). The text does not say who picks the fresh directory.
- WC-4's required fields have no run identifier or timestamp. A retry worker that dies before writing leaves the first attempt's `return-contract.yaml` in place. WC-5 maps "no report exists" to `failed` (`SPEC:63`), but a stale file does exist and the coordinator may read it as the current result.
- Medium because it needs the guess that the coordinator reuses the directory.

### M-3 (Medium): the contract location is not one rule

- `SPEC:83` puts adversarial's contract at `<output>/adversarial/return-contract.yaml` (WC-4 says `<output-dir>/return-contract.yaml`).
- `SPEC:92` puts workflow's contract in `.dev/tasks/to-do/<id>/`, where `<id>` is generated by the command, so it is not "known before dispatch". The same row asks for the contract on pre-creation STOPs. At a pre-creation STOP no package directory exists (INV-B:272-273: the contract is not written there today), and the spec names no location.
- `worker_done --report-path` carries whatever path the worker reports (`SPEC:62`), so the coordinator can still find the file. The "known before dispatch" claim is what fails.

### M-4 (Medium): WC-10 scope and a 4-5 minute gap

- `SPEC:68` requires splitting "a single tool call for longer than 5 minutes" into waits of at most 4 minutes. A call of 4 to 5 minutes is therefore legal under WC-10. `SPEC:210` (AC-4.3) fails any "single tool call exceed[ing] 240 s", and `SPEC:266` (Decisions) says 4 minutes is the margin. A 270 s wait passes WC-10 and fails AC-4.3.
- WC-10 names a "poll wait, a long eval". An Agent-tool fan-out call also blocks the top-level session for the whole fan-out (adversarial Mode B with up to 10 agents, cleanup-audit waves, tdd research, `SPEC:24`, INV-A:35, INV-A:42, INV-B:221). WC-10 does not mention it, and the 5-minute heartbeat is a worker duty (`CAPS:130`). Whether heartbeat age matters to liveness is itself UNVERIFIED (`CAPS:182`, item 7), so the harm is not shown.

### M-6 (Medium): AC-C1 and AC-C5 against the spec's own deliverables

- AC-C1 (`SPEC:172`) greps `src/superclaude/core` and requires no output. P0 adds `WORKER-CONTRACT.md` and an Orca section to `HOW-WE-WORK.md`, both under `core/` (`SPEC:158`). SA-2 (`SPEC:147`) allows an Orca example in the contract file. If either file writes `orca orchestration ...` the check fails. The spec does not say they must avoid it.
- AC-C5 (`SPEC:176`) requires no removed line (`^-[^-]`) in command edits without a named defect fix. Adding `--unattended` or `--output` to a command's Usage line replaces that line, which shows up as a `-` line. SA-4 (`SPEC:149`) calls such flags additive. Medium because it depends on how the flag is documented.

### M-8 (Medium): P1 flag on gated commands

`SPEC:159` accepts `--unattended` on every command in P1, "a no-op where a command has no gate". For gated commands, gate resolution comes in P2 (`SPEC:160`). Between P1 and P2, a brief per `SPEC:73` passes `--unattended` to, for example, auggie-review (`SPEC:100`, P2), whose default still posts to GitHub with no prompt (INV-A:38) and which WC-9 says must be off. Medium because it needs a coordinator to dispatch in that window.

### M-9 (Medium): claims stronger than their evidence

- `SPEC:114`: pr-submit's wait "can already heartbeat between iterations". The same row, `SPEC:283` (UNVERIFIED #12) and `SPEC:95` read of INV-B:95 ("up to `--timeout` 600 s per wait") disagree on whether one wait is a single call. The spec reinterprets the inventory's reading on lines read only in `sk/sc-pr-submit-protocol/SKILL.md:46-64`, which is outside the sandbox (UNVERIFIED).
- `SPEC:122`: the tasklist reflect fan-out "runs one layer below the worker, inside Claude Code's nesting limit". The source is INV-A:14, which cites an external docs page fetched only in part (INV-A:112), and INV-B:314 and INV-B:210 mark nested spawning UNVERIFIED.
- The E5 grep results, the 11 re-read locations and the validator claims (`SPEC:11`, `SPEC:25`, `SPEC:285`) are not checkable here (UNVERIFIED).

### M-12 (Medium): plugin mirror

`SPEC:279` (UNVERIFIED #8) leaves open how `plugins/superclaude/commands/` is kept in step with a command edit, and says each phase's plan must resolve it. AC-C2 (`make verify-sync`, `SPEC:173`) covers `.claude/` only. A phase could pass every check and leave the plugin copies stale.

### N-2 (MINOR): AC-C1 escape

The command in `SPEC:172` contains `\|` escapes that exist for the Markdown table. Copied raw into `grep -E` they match a literal pipe in the pattern.

## === ADVERSARIAL ANALYSIS (Whittaker) ===

- **Zero/Empty attack.** I can break this specification by **Zero/Empty Attack**. The invariant at **WC-4 / 2.3 (`SPEC:62`, `SPEC:73`)** fails when `--unattended` is passed with no output location. Concrete attack: coordinator dispatches `/sc:analyze src/x.py --unattended` (the row adds `--output`, `SPEC:99`, but nothing makes it required). Before: no report path known. After: the command either refuses, defaults, or writes nowhere, and the spec does not say which (M-5). A zero-byte or malformed `return-contract.yaml` is also unaddressed: WC-5 covers only "no report exists" (`SPEC:63`).
- **Divergence Attack.** I can break this specification by **Divergence Attack**. The invariant at **WC-4 (`SPEC:62`)** fails when the `--output` value is a file (tdd, init-lite, spec-panel). Concrete attack: `--output docs/x/TDD_FOO.md`. WC-4 says the contract goes to `docs/x/TDD_FOO.md/return-contract.yaml`; the tdd row says `docs/x/TDD_FOO.md` is the TDD (B-3). A second divergence: WC-3's answer-as-flag path against D2(a), D4(a) and WC-9 (B-2). Both branches could apply at once for `implement`.
- **Sentinel Collision Attack.** I can break this specification by **Sentinel Collision Attack**. The invariant at **WC-5 (`SPEC:63`)** fails when a contract carries a `status` outside the four values (a command's own `PASS`, `COMPLETED`, or reflect's verdict words). Concrete attack: contract `status: PASS`. WC-5 sends `succeeded` or `failed` by value of status; an unknown value maps to neither, and the spec has no default. The word `blocked` is also reused by the Orca Task status vocabulary (`CAPS:89`: `pending, ready, dispatched, completed, failed, blocked`), which the spec does not confuse but never distinguishes.
- **Sequence Attack.** I can break this specification by **Sequence Attack**. The invariant at **WC-6 / section 6 (`SPEC:64`, `SPEC:154-162`)** fails when steps run out of order or repeat. Concrete attack 1: attempt 1 writes `status: succeeded` into `<dir>`; attempt 2 (`--retry-of`, same Task spec) dies before writing; the coordinator reads attempt 1's file (M-2). Concrete attack 2: P1 is merged, P2 not; a brief passes `--unattended` to auggie-review and a PR gets reviewed-and-commented (M-8).
- **Accumulation Attack.** I can break this specification by **Accumulation Attack**. The invariant at **WC-3 (`SPEC:61`)** fails at several gates in one run. Concrete attack: cli-portify blocks at gate 1, the worker asks once and re-invokes, the command blocks at gate 2. "Once" is ambiguous (M-11), and no cap on ask cycles is stated. Long Agent-tool waits (M-4) accumulate past the 5-minute heartbeat cadence.

## Guard Condition Boundary Table

Classes left out, with the reason: "One/Minimal" is folded into "Typical" for every guard (the guards are thresholds or set membership, not counts), and "Maximum/Overflow" is left out for the WC-5 status guard (a status is not a quantity).

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|-------|----------|-----------------|----------------|--------------|-------------------|--------|
| WC-10 split rule (call longer than 5 min) | SPEC:68 | Zero/Empty | 0 s, no wait | false | no split needed | OK |
| WC-10 split rule | SPEC:68 | Typical | 12 min poll | true | split into waits of at most 4 min | OK |
| WC-10 split rule | SPEC:68, SPEC:210 | Maximum/Overflow | exactly 300 s | false (not "longer than") | unsplit call allowed; AC-4.3 fails any call over 240 s | GAP (M-4, Medium) |
| WC-10 split rule | SPEC:68, SPEC:210 | Legitimate Edge Case | 270 s | false | same as above | GAP (M-4, Medium) |
| WC-5 outcome mapping | SPEC:63 | Zero/Empty | contract file missing | true ("no report exists") | `--outcome failed` | OK |
| WC-5 outcome mapping | SPEC:63 | Zero/Empty | contract file present, 0 bytes or unparseable | unspecified | unspecified | GAP (Medium; FR-9, names no wrong outcome an implementer must produce) |
| WC-5 outcome mapping | SPEC:63 | Typical | `status: partial` | true | `--outcome succeeded`, first sentence states `partial` | OK |
| WC-5 outcome mapping | SPEC:63 | Sentinel Value Match | `status` outside the four values | unspecified | unspecified | GAP (Medium) |
| WC-4 location | SPEC:62, SPEC:73 | Zero/Empty | `--unattended`, no output flag | unspecified | unspecified | GAP (M-5, Medium) |
| WC-4 location | SPEC:62, SPEC:90 | Legitimate Edge Case | `--output` is a file (`TDD_FOO.md`) | true | contract at `<file>/return-contract.yaml` | GAP (B-3, blocking: concrete wrong outcome) |
| WC-4 location | SPEC:62, SPEC:83 | Legitimate Edge Case | adversarial contract under `<output>/adversarial/` | true | row and WC-4 give different paths | GAP (M-3, Medium) |
| WC-1 prompt fallback | SPEC:59 | Typical | 30 s fallback | n/a | passes (EVIDENCE per CAPS:49) | OK |
| WC-1 prompt fallback | SPEC:59 | Maximum/Overflow | above about 45 s | n/a | "well inside" the limit, no number given | GAP (Medium; FR-8, no wrong outcome named) |
| WC-3 ask-once | SPEC:61, SPEC:105 | Maximum/Overflow | 3 gates in one run (cli-portify) | unspecified | "once" ambiguous | GAP (M-11, Medium) |
| WC-3 answer-as-flag | SPEC:61, SPEC:234 | Legitimate Edge Case | `E-HALT-QA` halt | true | WC-3 allows ask and re-invoke; D2(a) says end `failed` | GAP (B-2, blocking: safety boundary) |
| Nesting depth fence | SPEC:66, CAPS:97-98 | Typical | worker calls `worker-start` at depth 1 | true | refused, `nested_worker_depth_exceeded` | OK |
| `--unattended` with opt-in interactive flags | SPEC:103, SPEC:110, SPEC:114 | Legitimate Edge Case | cleanup/improve `--interactive`; pr-submit `--monitor 1` | true | refused | OK |
| `--unattended` with opt-in interactive flags | SPEC:84, SPEC:89, SPEC:118 | Legitimate Edge Case | brainstorm, release-split, roadmap `--interactive` | unspecified | only the 3.1 column "never --interactive" | GAP (Medium; brief-level rule, no combined-flag behavior) |

FR-10 check: every guard is enumerated, every cell is populated, and omitted classes carry a reason. The table is complete. Entries with Status = GAP are the priority candidates for `sc:adversarial` AD-1 invariant probing.

## Quantity Flow Diagram (phase rollout)

```text
[43 commands in cmd/] --> [classify: 10 ready / 27 needs-change / 6 coordinator-only]   (SPEC:76; sum 43, conserved)
        |                              |
        |                              v
        |                [P0: 3 smoke runs, 0 command edits]
        |                              |
        v                              v
[37 worker-capable: 10 + 27] --> [P1: 9 (3.2) + 4 fixes (3.1) = 13 edited; flag on "every command in 3.1 and 3.2" = 37]   <-- MISMATCH (B-1, M-8)
        |--> [P2: 11 (3.2) + 4 (3.1: reflect, release-split, tdd, troubleshoot) = 15]
        |--> [P3: 4]   [P4: 3]
Per-phase 3.2 split: 9 + 11 + 4 + 3 = 27 (matches); 3.1 split: 4 (P1) + 4 (P2) + 2 (none: brainstorm, init-lite) = 10 (matches)
[AC-1.1 asserts a section on 37 commands at the end of P1]   <-- consumer expects N=37, P1 produces 13 edited (B-1)
```

Counts are conserved across the classification and the phase assignment. The mismatch is only between the P1 scope text and AC-1.1 on one side and the phase assignments on the other.

## Follow-up candidates (Medium and minor findings)

These never trigger a revision. The session that ran this review has no user channel in this sandbox, so the once-per-loop question about opening an issue was not asked and no issue was created. The list is recorded here.

- M-1 AC-0.4 step 3 and step 4 against Phase 0 report files.
- M-2 WC-6 fresh directory against the coordinator-fixed directory; stale-contract guard.
- M-3 Contract location rule: workflow pre-creation STOPs, adversarial path.
- M-4 WC-10 4-5 minute gap and Agent-tool fan-out waits.
- M-5 `--unattended` with no output location.
- M-6 AC-C1 scope and AC-C5 against Usage-line edits.
- M-7 `--post-pr` enabling flag for auggie-review.
- M-8 P1 acceptance of `--unattended` on gated commands before P2.
- M-9 Claims stronger than their evidence (pr-submit heartbeat, tasklist nesting limit, unreproducible checks).
- M-10 Requirements with no acceptance check (WC-1, WC-3, WC-6, WC-12, WC-10 outside pr-submit).
- M-11 "Ask once" against cli-portify's three gates.
- M-12 Plugin mirror update rule deferred.
- GAP rows of the boundary table not tied to a numbered finding: WC-5 empty or unparseable contract; WC-5 unknown `status`; WC-1 numeric fallback; `--unattended` with brainstorm/release-split/roadmap `--interactive`.
- N-1 E2 "and answered".
- N-2 AC-C1 `\|` escapes.

## Reviser brief

Blocking finding ids: B-1, B-2, B-3. Rules for the reviser:

- Revise only text a blocking finding names.
- Add no rule, mechanism or section that no blocking finding calls for.
- Each added paragraph or table cites its finding id.
- Prefer deleting or narrowing to adding.
- Report the byte size of the candidate before and after, and the bytes added and deleted per finding id.
- Leave Medium and minor findings alone, including the follow-up candidates above.
- Return the candidate once and do not award yourself a PASS.

What each blocking finding names:
- B-1: `SPEC:159` (P1 scope "every command in sections 3.1 and 3.2") and `SPEC:195` (AC-1.1), which contradict `SPEC:112` and `SPEC:265` (`load`), `SPEC:154` and `SPEC:162` (P4 commands wait for D2-D4), and `SPEC:139` and `SPEC:240` (D3).
- B-2: `SPEC:61` (WC-3), which contradicts `SPEC:234` and `SPEC:208` (D2(a), AC-4.1), `SPEC:67` (WC-9) and `SPEC:245` (D4(a)).
- B-3: `SPEC:62` (WC-4 `<output-dir>`), which has no valid reading for the file-valued `--output` of `SPEC:87`, `SPEC:90` and `SPEC:120`, and `SPEC:200` (AC-2.2).

verdict: FAIL

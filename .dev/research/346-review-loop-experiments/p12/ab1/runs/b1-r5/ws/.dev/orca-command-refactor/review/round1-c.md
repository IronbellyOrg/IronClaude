review: 1 of 3

# Spec-panel report: orca-worker-contract-spec.md (critique, focus requirements,architecture)

## Header
- candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md` (285 lines)
- candidate sha256: `d3cdbe573e57303b9ce6c93d1fe98ba18fb7cb1a15773d926bf6a0c31425200d`
- baseline: none given (first review of the full document)
- reviewer model used: claude-sonnet-5-5
- command: `/sc:spec-panel @.dev/orca-command-refactor/specs/orca-worker-contract-spec.md --mode critique --focus requirements,architecture`
- procedure: FIRST-REVIEW prompt of `~/.claude/rules/prompts/document_review_loop_prompts.md` (read in full first), Review Loop section and Mandatory Output Artifacts of `command.md`. This report is ONE first review. The prompt asks the coordinator for three independent first reviews and a MERGE; this worker can run only this one, so the three-review merge is left to the coordinator.
- panel order used: Wiegers, Adzic, Cockburn, Fowler, Newman, Hohpe, Nygard, Whittaker (Whittaker's order is fixed by the command, which this report follows loosely; see the command's sequence table).

## Evidence base and its limits
- Checkable in the workspace: the spec (cited `spec:N`), `.dev/orca-command-refactor/README.md` (`README:N`), and the three inventories (`INV-A:N`, `INV-B:N`, `CAPS:N`). Spec citations to INV-A, INV-B and CAPS line numbers were spot-checked against those files: about 40 of them (for example `CAPS:44-45`, `CAPS:97-103`, `CAPS:148-150`, `INV-A:76-83`, `INV-B:272,289-299,311,320,323`) match the cited content.
- UNVERIFIED (the file is not in the workspace): every `src/superclaude/...` citation (`cmd/`, `sk/`), `EVIDENCE.md`, `.dev/codegraph-migration/...`, `CLAUDE.md` line cites, `Makefile`, `pyproject.toml`, the E5 grep results (`spec:25`) and the "this worker re-read 11 locations" claim (`spec:11`). They are accepted only as far as the inventories quote them.
- No finding below depends on an UNVERIFIED citation.

## === REQUIREMENTS ANALYSIS ===

### Blocking findings

**B1. WC-4 puts the contract file in a directory the brief cannot name for several commands (CRITICAL, High)**
Experts: Wiegers (traceability), Adzic, Whittaker (sentinel/divergence).
- Stated text 1, `spec:62` (WC-4): "One report file, known before dispatch ... the command writes `<output-dir>/return-contract.yaml`, where `<output-dir>` is the directory the coordinator passed (`--output` / `--output-dir`) ... It is written on success, failure, blocked and partial outcomes, including stops before any other output exists."
- Stated text 2, `spec:90` (tdd, section 3.1): "Brief must pass ... `--output <file>`"; `spec:87` (init-lite): "`--output <file>`"; `spec:200` (AC-2.2): "`/sc:tdd "auth" --unattended --output <file>` ... contract `status: blocked` with a non-empty `blocked_question`".
- Stated text 3, `spec:92` (workflow): report is `.dev/tasks/to-do/<id>/return-contract.yaml`, and the small fix is "Write the contract for pre-creation STOPs too"; `spec:85` (cleanup-audit): "output dir is fixed" with no contract path.
- Grading sentence: An implementer who follows WC-4 as written builds, for `/sc:tdd`, a contract at `<value of --output>/return-contract.yaml`, which is `docs/x/TDD.md/return-contract.yaml`; that cannot be created because the value is a file, so the blocked status in AC-2.2 cannot be written and the check cannot pass. For `/sc:workflow` the path contains a package id the command generates, so it is not "known before dispatch" (WC-4), and a pre-creation STOP has no package directory in which to write it. This follows from the stated texts with no further assumption.
- Wrong outcome: the one mechanism the coordinator relies on to detect a blocked or failed worker (`spec:62`, WC-5 at `spec:63`, step 4 at `spec:183`) has no resolvable location for tdd, init-lite, workflow pre-creation stops and cleanup-audit.
- Recommendation: narrow WC-4 to one stated rule that works for file-valued flags (for example, "contract directory = the directory of `--output` if it is a file, else the directory itself"), or name the contract directory per command in sections 3.1 and 3.2.

**B2. AC-1.1 cannot pass for `/sc:load` as the spec itself specifies it (CRITICAL, High)**
Experts: Wiegers (testability), Crispin (acceptance criteria).
- Stated text 1, `spec:195` (AC-1.1): "the test asserts that every command in sections 3.1-3.2 has a `## Unattended mode` section naming `return-contract.yaml` and `~/.claude/WORKER-CONTRACT.md`".
- Stated text 2, `spec:112` (load row): report "none (see note)", resume "n/a", "use it as a step inside another worker's brief, not as its own Task"; `spec:159` (P1): "load (usage line only)"; `spec:265`: "a report file would be an unrequested addition".
- Grading sentence: An implementer who follows P1 and the load row adds only the usage-line fix and no contract or `## Unattended mode` section, and then AC-1.1, which includes load in "every command in sections 3.1-3.2", fails; if the implementer instead adds the section to make AC-1.1 pass, it contradicts the load row and Decisions (`spec:265`). Both stated texts cannot hold together.
- Recommendation: exclude load (and any other command not dispatched as its own Task) from the AC-1.1 assertion, or delete the "none" decision. Prefer the narrower edit.

**B3. P1 and AC-1.1 require unattended sections for the P4 commands, which depend on decisions P1 is said not to need (CRITICAL, High)**
Experts: Fowler (phase boundaries), Nygard, Cockburn.
- Stated text 1, `spec:154`: "Phases 1-3 need no user decision; Phase 4 waits for answers to D2-D4."
- Stated text 2, `spec:159` (P1): "the `--unattended` flag accepted by every command in sections 3.1 and 3.2"; `spec:195` (AC-1.1) as quoted above. Section 3.2 includes implement (`spec:109`), post-release (`spec:113`) and pr-submit (`spec:114`), all assigned to P4 (`spec:162`).
- Stated text 3, `spec:241`: D3 recommended option (a) "Coordinator or person only ... no pr-submit changes in Phase 4"; `spec:139`: "`/sc:pr-submit` stays a worker candidate only if the user accepts open decision D3".
- Grading sentence: An implementer who follows P1/AC-1.1 writes a `## Unattended mode` section for pr-submit, implement and post-release before D2-D4 are answered, and the gate resolutions in those sections (implement's Ruling halt, post-release authorization, pr-submit as worker) are exactly what D2-D4 decide; with the recommended D3 (a) the pr-submit section the check demanded is the "pr-submit change" D3 (a) says does not happen. The stated texts contradict.
- Recommendation: limit the P1 flag and AC-1.1 to P1-P3 commands, and test the P4 sections in P4.

### Medium findings (warnings; not blocking; listed under follow-up candidates)

**M1. The `--unattended` flag lands before gate conversion, and nothing tells the coordinator not to use it yet (Medium).**
`spec:159` ships the flag on gated commands in P1, `spec:160` converts auggie-review, task, cleanup and others only in P2, and `spec:228` (D1 a) has the coordinator write `--unattended` into every worker's command line. Between P1 and P2 a brief that follows `spec:73` for `/sc:auggie-review <PR> --unattended` would still post to GitHub and wait on a person (WC-9, `spec:67`). This needs a guess that a coordinator dispatches mid-rollout, and the spec states "each phase is independently useful" (`spec:154`), so it is a missing requirement (a rule that a coordinator dispatches a command unattended only after the phase in its row has landed), not a stated text that does harm. Medium.

**M2. AC-C5's regex cannot detect a deleted bullet (Medium).**
`spec:176`: `git diff -U0 ... | grep -E '^-[^-]'` must print nothing "edits are additive". A deleted line `- Will Not: x` appears in the diff as `-- Will Not: x`, which the pattern `^-[^-]` does not match, so deleting a bullet passes the check. SA-4 and SA-1 (`spec:146,149`) rely on this check. The trace needs no assumption, but the loss is of a check strength, not of a stated requirement, so Medium.

**M3. AC-0.4 and 7.2 step 1 disagree on `--unattended` in Phase 0 (Medium).**
`spec:180` and `spec:73` require the brief's command line to include `--unattended`; `spec:194` (AC-0.4) lists P0 smoke commands without it, before any command accepts it (`spec:158`: P0 "no command edits"). The implementer must guess which text wins; the harm depends on how an unrecognised flag is read. Medium.

**M4. AC-C1 scans `src/superclaude/core`, where P0 adds the contract file and a HOW-WE-WORK Orca section (Medium).**
`spec:148` (SA-2) allows an Orca example "inside the contract file"; `spec:158` adds `WORKER-CONTRACT.md` and "an Orca section to HOW-WE-WORK.md"; `spec:172` (AC-C1) greps `src/superclaude/core` for `orca(-ide)? orchestration|worktree|terminal|agent` and requires nothing. If either file names `orca orchestration ask` as the example, AC-C1 fails. Whether it does depends on the wording written later. Medium. (Minor note: in the table cell the pattern is written with `\|`; copied literally into `grep -E` it matches a literal `|`, not alternation.)

**M5. No rule for a single non-splittable tool call longer than 5 minutes (Medium).**
`spec:68` (WC-10) splits poll waits and evals into waits of at most 4 minutes, but `/sc:build`, `/sc:test` and `/sc:analyze` (`spec:99,101,123`) run one project command whose runtime the command cannot split. The spec does not say what the worker does (heartbeat from a background shell, or accept silence). Missing requirement, so Medium.

### Notes (minor)
- N1. `spec:154` ("Phases 1-3 need no user decision") and `spec:225` ("Phases 0-3 can proceed on the recommendations") differ on whether D1 and D5 need an answer; D1 (`spec:227`) selects the flag P1 adds.
- N2. WC-4 (`spec:62`) fixes the `status` vocabulary to four values while "commands that already write a contract keep their fields". The existing statuses of workflow, reflect and brainstorm are not read in this sandbox (UNVERIFIED), so a value conflict cannot be ruled out.
- N3. `spec:174` (AC-C3) correctly avoids assuming a clean test suite; no issue.
- N4. 7.2 step 5 (`spec:184`) searches the transcript for the string `AskUserQuestion`; the string can also appear in a quoted command definition. A tool-call-specific match would be sharper.

## === ARCHITECTURE ANALYSIS ===

Fowler (boundaries) and Newman (evolution): the decision itself is coherent. The evidence table (`spec:19-26`) and the rejected alternative (`spec:29-37`) hold together with CAPS: R1 matches `CAPS:97-103`, R2 `CAPS:147-149`, R3 `CAPS:76,150`, and the three stated evidence gaps (`spec:43-45`) are honest. The coordinator-only list (`spec:130-137`) agrees with `INV-A:90-92` and `INV-B:285-287`, and the counts 10 + 27 + 6 = 43 are consistent with section 3 (10 rows in 3.1, 27 in 3.2, 6 in section 4). The phase list in section 6 matches the "Phase" column of 3.2 (P1: 9 commands, P2: 11 plus 4 ready commands, P3: 4, P4: 3).

Hohpe (integration): the contract is a file hand-off (`return-contract.yaml`) plus the Orca `worker_done` message; the mapping rule WC-5 is complete for the four statuses. The only integration defect found is B1 (unresolvable file location), which is a requirement defect, not an architecture defect.

Nygard (failure modes): WC-2 (c), WC-3 and WC-5 cover the stall case (`spec:60-63`); the gap in WC-10 is M5; the dependency on an unproven direct-route run is stated and gated by AC-0.4 (`spec:43`, `spec:194`).

No blocking architecture finding beyond B3 (phase ordering vs decision dependency).

## === ADVERSARIAL ANALYSIS (Whittaker) ===

- I can break this specification by the **Divergence Attack**. The invariant at **WC-4 / AC-2.2 (`spec:62`, `spec:200`)** fails when **the brief passes a file path as `--output`**. Concrete attack: brief `/sc:tdd "auth" --unattended --output docs/auth/TDD.md`; the command must write `docs/auth/TDD.md/return-contract.yaml`; the path's parent is a file, so no contract exists; the worker finds "no report" and sends `--outcome failed` (WC-5, `spec:63`) with no `blocked_question`. (Basis of B1.)
- I can break this specification by the **Sequence Attack**. The invariant at **section 6 order (`spec:154-162`)** fails when **P1 is done and P4 is not**. Concrete attack: P1 lands the AC-1.1 test; the test requires sections in implement, post-release and pr-submit; D2-D4 are unanswered; the P1 author invents gate rules that D2-D4 later overturn. (Basis of B3.)
- I can break this specification by the **Zero/Empty Attack**. The invariant at **AC-1.1 (`spec:195`)** fails when **a command has no report (load)**; the assertion "every command ... naming `return-contract.yaml`" has no empty case. (Basis of B2.)
- I can break this specification by the **Accumulation Attack**. The invariant at **WC-10 (`spec:68`)** fails when **a single tool call runs 20 minutes** (a build); the 4-minute wait split does not apply. (Basis of M5.)
- I can break this specification by the **Sentinel Collision Attack**. The invariant at **WC-5 (`spec:63`)** treats `partial` as `succeeded`; the Orca outcome field then cannot distinguish a partial run from a full one, so the first body sentence is the only signal (spec accepts this explicitly at `spec:263`; noted only).

## Guard Condition Boundary Table (Nygard construction, Crispin completeness, Whittaker attack)

Guards found: WC-10 wait cap, WC-2/task confidence gate, nesting depth fence, readiness limit, WC-5 outcome mapping, AC-C5 additive-edit check. Classes left out are named with a reason.

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|-------|----------|-----------------|----------------|--------------|-------------------|--------|
| WC-10 wait cap | spec:68 | Zero/Empty | wait of 0 s (no wait) | no split needed | no heartbeat needed | OK |
| WC-10 wait cap | spec:68 | Typical | 3 min wait | within 4 min | heartbeat between waits | OK |
| WC-10 wait cap | spec:68 | Maximum/Overflow | one tool call of 20 min that cannot be split (build, test) | exceeds 5 min | not specified | GAP (M5) |
| WC-10 wait cap | spec:68 | Legitimate Edge Case | wait of exactly 4 min and exactly 5 min | 4 min allowed, 5 min is the cadence | "longer than 5 minutes" must split, "at most 4 minutes" waits: the 4-5 minute band is allowed but not stated as allowed | OK |
| task confidence gate | spec:121 | Typical | confidence 0.50 | below 0.70 | blocked, contract with question | OK |
| task confidence gate | spec:121 | Legitimate Edge Case | confidence exactly 0.70 | not below 0.70 | proceeds (implied by "below 0.70") | OK |
| nesting depth | spec:33 (R1) | Sentinel Value Match | depth 1 | worker may not start workers | refused, `nested_worker_depth_exceeded` | OK |
| nesting depth | spec:33 | Zero/Empty | depth 0 / setting unreadable | not stated for Orca fallback | covered by CAPS:100 (malformed falls back to 1); not restated in spec | OK (outside spec scope, one line: spec relies on CAPS) |
| readiness limit | spec:59 (WC-1) | Typical | prompt with 30 s fallback | passes | passes | OK |
| readiness limit | spec:59 | Maximum/Overflow | fallback above about 45 s | fails | fails (cited `EVIDENCE.md:56`, UNVERIFIED here) | OK |
| WC-5 outcome mapping | spec:63 | Zero/Empty | no report file | not a report | `--outcome failed` | OK |
| WC-5 outcome mapping | spec:63 | Typical | status `succeeded` | succeeded | `--outcome succeeded` | OK |
| WC-5 outcome mapping | spec:63 | Legitimate Edge Case | status `partial` / audit verdict FAIL | succeeded | `--outcome succeeded`, status in first sentence | OK |
| WC-5 outcome mapping | spec:63 | Sentinel Value Match | status value outside the four | not stated | not specified | GAP (N2, Medium: depends on existing contract vocab, UNVERIFIED) |
| WC-4 contract location | spec:62 | Legitimate Edge Case | `--output` is a file; generated id dir; fixed output dir | none resolvable | not specified | GAP (B1, blocking) |
| AC-C5 additive check | spec:176 | Legitimate Edge Case | deleted bullet line `- x` | diff line `-- x` | not detected | GAP (M2, Medium) |

Classes left out: "One/Minimal" for all guards (no distinct behavior from Typical); "Sentinel Value Match" for WC-10 and AC-C5 (no sentinel value in the guard).
FR-8 and FR-9 grading: the WC-4 location GAP names a concrete wrong outcome (B1), so it is blocking; the WC-10, WC-5-vocabulary and AC-C5 GAPs name no outcome that follows with no assumption, so they are Medium and listed under follow-up candidates.

## Pipeline Dimensional Analysis
Triggered on the phase pipeline P0 -> P4 (stages with a changing command set). Quantity flow: 43 commands -> 10 ready (3.1) + 27 changed (3.2) + 6 coordinator-only (section 4). P1 takes 9 commands + 4 fixed ready commands; P2 takes 11 + 4 ready; P3 takes 4; P4 takes 3. The 3.2 total of 27 = 9 + 11 + 4 + 3 holds. No count mismatch found. The AC-1.1 consumer assumes all 37 commands of 3.1-3.2 in P1 (a count mismatch with the P1 scope of 13), which is the substance of B2 and B3.

```text
[Source: 43 commands] --> [3.1 ready: 10] --> [P1 fixes 4: adversarial, cleanup-audit, index-repo, workflow]
                      --> [3.2 changed: 27] --> [P1: 9] [P2: 11] [P3: 4] [P4: 3]
                      --> [section 4 coordinator-only: 6]
[AC-1.1 consumer: expects 37 sections in P1] <-- MISMATCH with P1 scope (13 commands)
```

## Coverage statement
Covered: all 285 lines of the candidate; sections 1-9, Decisions and UNVERIFIED; the Orca facts (CAPS) and both inventories for every cited INV/CAPS line I checked; README rules (planning only, `path:line` for every claim). Not covered: any `src/superclaude/` file (absent), `EVIDENCE.md`, `.dev/codegraph-migration/` evidence (absent), Orca's live behavior. No file was edited other than this report.

## Follow-up candidates
Medium and minor findings, not blocking and not in the Reviser brief: M1, M2, M3, M4, M5, N1, N2, N3, N4. The session that runs this review asks the user once per loop whether to open an issue for them and creates none without the user's answer; this worker cannot ask (final reply is restricted), so the coordinator carries that question.

## Reviser brief
Blocking finding ids: **B1, B2, B3**. Rules for the reviser (restated from the command's Review Loop, bullet 6; the reviser reads this report, not the command):
- Revise only text a blocking finding names: B1 (`spec:62` WC-4, and the rows at `spec:85,87,90,92` and AC-2.2 at `spec:200` only as far as needed), B2 (`spec:195` AC-1.1 and the load row at `spec:112`), B3 (`spec:154`, `spec:159`, `spec:195`).
- Add no rule, mechanism or section that no blocking finding calls for; each added paragraph or table cites its finding id.
- Prefer deleting or narrowing over adding.
- Report the byte size of the candidate before and after, and the bytes added and deleted per finding id.
- Leave Medium and minor findings (M1-M5, N1-N4) alone.
- Return the candidate once and do not award yourself a PASS.

verdict: FAIL

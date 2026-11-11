review: 1 of 3

# Whole-document audit: orca-worker-contract-spec.md

- Command: `/sc:spec-panel @.dev/orca-command-refactor/specs/orca-worker-contract-spec.md --mode critique --focus requirements,architecture`
- Candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md` (285 lines)
- Candidate sha256: `39bbe6871713a48397dee32c0a486174eebbc1b08a14833316eed1593df495bb`
- Baseline: none given, none needed (first review of the whole document; `--re-review` not used)
- Reviewer model actually used: claude-sonnet-5-5
- Label: whole-document audit of the final spec, per the FIRST-REVIEW prompt of `~/.claude/rules/prompts/document_review_loop_prompts.md:27-32`
- Panel: Wiegers (lead), Adzic, Cockburn (requirements); Fowler (lead), Newman, Hohpe, Nygard (architecture); Whittaker (adversarial, always active). Crispin/Gregory/Hightower not selected by the focus.
- Coverage: all 285 lines of the candidate read; `README.md` (binding context) read; inventory lines checked against the claims listed under "Citation check". Everything under `src/`, `~/.claude/` skills and the Orca guides is outside the sandbox, so a citation to those is UNVERIFIED unless an inventory line quotes it. Section 7 acceptance checks and the 3.1/3.2 tables were checked for internal consistency; no command was run.

## Citation check (inventory-backed, what could be verified)

| Claim in candidate | Checked against | Result |
|---|---|---|
| 21 + 22 = 43 commands (spec:76) | `inventory/commands-a.md:3`, `commands-b.md:3` (21 and 22 names) | holds |
| 10 ready / 27 needs-change / 6 coordinator-only (spec:76) | spec tables 3.1 (10 rows), 3.2 (27 rows), section 4 (6 rows) counted; inventory A 5 ready + 13 needs-change + 3 coordinator-only, B 5 + 14 + 3 (`commands-b.md:289`, `:285-287`) | holds |
| Every one of the 37 worker-capable commands lands in exactly one phase (spec:156-162) | counted P1 (9 + 5 fixes), P2 (11 + 4 ready-command fixes + 4), P3 (4), P4 (3) | holds, with no command missing or repeated |
| WC-3 ask/resume text (spec:61) | `orca-capabilities.md:58-61`, `:64` | holds |
| R1 nesting depth 1 (spec:33) | `orca-capabilities.md:97-103`; "enforcing call sites unverified" is carried honestly | holds, UNVERIFIED flag kept |
| WC-5 `worker_done` outcome vocabulary (spec:63) | `orca-capabilities.md:72-73` | holds |
| WC-4 report-path not checked by Orca (spec:62, UNVERIFIED 3) | `orca-capabilities.md:79`, `:178` | holds |
| spec-panel has no output flag (spec:120) | `commands-b.md:177-185` | holds for the inventory snapshot; see N-5 for the command version in this sandbox |
| E5 grep result, "re-read 11 locations", "340 citations re-read" (spec:11, :25, :285) | no `src/` tree in the workspace | UNVERIFIED |
| All `sk/...` and `cmd/...` path:line citations in sections 3-4 | not in the workspace; only the inventories that carry them are readable | UNVERIFIED except where an inventory line quotes the text |

## === REQUIREMENTS ANALYSIS ===

### B-1 (MAJOR, blocking, High) Wiegers, Adzic: AC-0.4 requires a step-3 condition that cannot pass in Phase 0

- Stated text: `spec:194` says the three smoke runs pass when "steps 1-3 and 5-7 pass; step 4 uses the command's existing report file, since the contract arrives in P1". Step 3 (`spec:182`) passes only if "its report path is the WC-4 contract path" and "`--outcome` matches the contract's `status` under WC-5". WC-4 (`spec:62`) defines that path as `<output-dir>/return-contract.yaml`, and the spec says the contract is added in P1 (`spec:159`). Section 3.1 confirms none of the three commands has it in P0: troubleshoot reports `REPORT.md` (`spec:91`), adversarial's contract filename is "not fixed" (`spec:83`), workflow writes `.dev/tasks/to-do/<id>/return-contract.yaml` at a path not known before dispatch (`spec:92`).
- Wrong outcome: An implementer who follows the stated text as written builds a P0 gate that no smoke run can pass, and the gate is wrong because AC-0.4 exempts only step 4 while step 3 still demands the P1 artifact. Section 6 (`spec:154`) says later phases "do not start until the earlier phase's checks in section 7 pass", and `spec:194` says a failure "reopens section 1", so the rollout stalls on a self-contradiction, or the team reads a failed step 3 as evidence against the decision.
- Recommendation: narrow step 3 for P0 to "exactly one `worker_done`; its `--outcome` matches the command's existing report file; its report path is that file". Delete text, add nothing.
- Quality impact: unblocks the only phase that tests the decision (spec:43).

## === ARCHITECTURE ANALYSIS ===

The decision (Orca coordinates, commands stay units of work, section 1.1) is sound and the rejected alternative is argued from checked inventory lines (R1-R5, spec:31-37; `orca-capabilities.md:97-103`, `:145-150`). Fowler and Newman find the boundaries clean: the contract file is the single interface between a command and any caller; the six coordinator-only commands are separated by role, not by effort. Findings below are all Medium or minor.

### M-1 (MAJOR label, graded Medium) Fowler: AC-C1 may fail on the P0 deliverables, and SA-2 gives it no exemption
- `spec:172` pass condition is "prints nothing" over `src/superclaude/core`, minus only `skills/ccsession-tag/`. P0 adds `src/superclaude/core/WORKER-CONTRACT.md` and "an Orca section" in `HOW-WE-WORK.md` (`spec:158`), and SA-2 (`spec:147`) allows an Orca mention "inside the contract file". Whether those texts contain `orca orchestration ...` is not stated; the Section 1.2 E5 baseline is `0` mentions (`spec:25`). If either does, AC-C1 fails in P0. Needs a guess about the content, so Medium.
- Recommendation: state in AC-C1 which core files are exempt (the contract file and the routing-guide Orca section), or say those texts name no `orca` subcommand.

### M-2 Wiegers: WC-4 says the contract is written "in unattended mode", SA-3 says "unattended mode or when the caller passes the new output flag"
- `spec:62` versus `spec:148`; the 3.2 rows say "add `--output`; contract" (for example `spec:99`). A run with the new `--output` and no `--unattended` writes a contract under SA-3 and not under WC-4. AC-1.3 (`spec:197`) tests only "neither flag", so it does not resolve it. Which reading is intended needs a guess. Recommendation: one sentence in SA-3 or WC-4 choosing one.

### M-3 Cockburn: AC-1.2 applies "each P1 command" to `/sc:load`, which AC-1.1 excludes
- `spec:196` runs the 7.2 live check on every P1 command with `--unattended --output <dir>`; `/sc:load` is a P1 command (`spec:159`), has "none" under Report (`spec:112`) and is excluded in AC-1.1 (`spec:195`, "F-04"). Step 4 of 7.2 (`spec:183`) then cannot pass for it. Also WC-4 (`spec:62`) has no exemption for `load`. Reading the exclusion into AC-1.2 is a guess, hence Medium. Recommendation: say "each P1 command except `load`" in AC-1.2.

### M-4 Nygard: WC-5's contract parse check and 7.2 step 4 disagree on a missing `command` field
- WC-5 (`spec:63`) treats a contract as unparseable only for zero bytes, truncation or no `status` key from the four values. 7.2 step 4 (`spec:183`) also asserts `d['command']`. A contract with a valid `status` and no `command` passes WC-5 (worker sends `succeeded`) and fails the coordinator's step 4. Which wins needs a guess. Recommendation: align WC-5 and step 4 on the same required keys.

### M-5 Adzic, Whittaker: the Phase 0 `workflow` run cannot satisfy WC-4 "known before dispatch"
- `spec:62` says the path is known before dispatch and that the workflow `<id>` is passed "by a flag the P1 plan names"; `spec:92` repeats this. The flag does not exist, is not named, and the P0 smoke run (`spec:194`) uses `/sc:workflow "<small change>" --handoff none` with no id flag. So in P0 the coordinator cannot learn the report path before `worker_done`. P0 step 4 uses "the existing report file", so the check would still run, but section 2.3 (`spec:73`) promises the path in the brief. Recommendation: in P0 let the coordinator read the path from the worker's `--report-path`, and say so.

### M-6 Fowler: ordering inside P2 and across D2-D4 is under-specified
- tasklist (P2) passes `--unattended` to reflect (`spec:122`), but reflect's `--unattended` rule lands in P2 as well (`spec:88`, `spec:160`); no order is given. P1 says no user decision is needed (`spec:154`), yet AC-1.1 (`spec:195`) requires an `## Unattended mode` section in `implement`, `post-release` and `pr-submit`, whose gate resolutions wait for D2-D4 (`spec:109,113,114`), and D3 (a) recommends no pr-submit change (`spec:240`) while pr-submit still counts among the 27 (`spec:76`). Recommendation: say that the P1 section for those three commands only states "blocked pending D2-D4", and that reflect precedes tasklist in P2.

## Whittaker adversarial findings (all Medium or minor)

I can break this specification by **Sequence Attack**. The invariant at **WC-3 versus AC-2.2 (spec:61, spec:200)** fails when **a worker whose gate resolves as blocked uses the allowed `ask` instead of stopping**. Concrete attack: tdd gets a bare topic (`spec:200`); the worker asks the coordinator, receives an answer, re-invokes with the flag and succeeds. Before: AC-2.2 expects `worker_done --outcome failed` and `status: blocked`. After: `succeeded`, no blocked contract, the check fails although the behaviour is the contract's own WC-3. Medium: the brief can forbid `ask`, but the spec does not say so. Fix: AC-2.2 should state "brief says do not use `ask`".

I can break this specification by **Divergence Attack**. The invariant at **WC-10 versus AC-4.3 (spec:68, spec:210)** fails when **a single tool call runs between 4 and 5 minutes**. WC-10 requires splitting only above 5 minutes while AC-4.3 fails any call above 240 s. Minor: only pr-submit is checked and the note in the `pr-submit` row (`spec:114`) already says 4 minutes.

I can break this specification by **Sentinel Collision Attack**. The invariant at **WC-5 (spec:63)** fails when **a `status: partial` contract is read as `succeeded` by a coordinator that only looks at `worker_done --outcome`**. `partial` maps to succeeded (`spec:263`); the first body sentence carries the word, but only a coordinator that opens the contract (WC-4 last sentence) sees it. Minor: the spec requires the coordinator to open the file (`spec:62`, `spec:73`).

I can break this specification by **Zero/Empty Attack**. The invariant at **AC-2.4 (spec:202)** fails when **the PR already has 30 or more reviews or comments**. `gh api ... --jq length` returns one page (default 30 items), so "counts unchanged" holds even if a post happened beyond the first page. Minor: add `--paginate`.

I can break this specification by **Accumulation Attack**. The invariant at **AC-C1/C4/C5/AC-0.3 (spec:172,175,176,193)** fails when **the commands are copied from the raw markdown**: the pattern is written with `\|` inside table cells, which in `grep -E` means a literal pipe and in the shell is not a pipeline. Rendered, the cell shows `|`. Minor note: copying raw text makes AC-C1 match nothing and "pass" vacuously. Fix: give the commands in a fenced block.

Pipeline Dimensional Analysis is not triggered: the phase and wave structure is process flow, not a data pipeline with count divergence (Fowler/Whittaker concur). State Variable Registry: not required, `--focus correctness` is not active.

## Guard Condition Boundary Table

Guards found: nesting depth (spec:33), readiness 60 s (spec:59), contract validity (spec:63), heartbeat 5 min / wait 4 min (spec:68), confidence 0.70 (spec:121), `--monitor 1` refusal (spec:114). Classes that cannot occur for a guard are left out with a one-line reason.

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|---|---|---|---|---|---|---|
| nested-depth fence | spec:33, spec:97-103 via CAPS | Typical | depth 1, command calls `worker-start` | refused | WC-8 forbids the call | OK |
| nested-depth fence | spec:249-252 (D5) | Legitimate Edge Case | user raises depth to 2 | not refused | stays forbidden by WC-8 | OK |
| readiness 60 s | spec:59 (WC-1) | Maximum/Overflow | prompt fallback 45 s | readiness fails | "well inside" the limit; evidence says 30 s passes, 45 s fails | GAP (Medium: "well inside" has no number) |
| contract parse | spec:63 (WC-5) | Zero/Empty | zero-byte file | not parseable | `--outcome failed` | OK |
| contract parse | spec:63 vs spec:183 | Sentinel Value Match | valid `status`, no `command` | WC-5 true, step 4 false | unspecified which wins | GAP (M-4) |
| contract parse | spec:63 | Legitimate Edge Case | `status: partial` | true | `succeeded`, status in body | OK |
| wait split | spec:68 vs spec:210 | Maximum/Overflow | single call of 270 s | WC-10 not triggered, AC-4.3 fails | differs | GAP (minor, only pr-submit) |
| confidence gate | spec:121 | Typical | confidence 0.50 | below 0.70 | blocked | OK |
| confidence gate | spec:121 | Legitimate Edge Case | exactly 0.70, or 0.70-0.89 band | not below | spec silent; inventory only covers below 0.70 (`commands-b.md:199`) | GAP (minor: no person gate hit in the 0.70-0.89 band is stated; `commands-b.md:199` lists only the below-0.70 gate) |
| `--monitor 1` | spec:114 | Zero/Empty | `--unattended` with no monitor flag | n/a | default not stated in the spec | GAP (minor, UNVERIFIED against `cmd/pr-submit.md`) |

Left out: "One/Minimal" for all guards, because none takes a count; "Sentinel" for the depth fence, because depth is a plain integer.

## Follow-up candidates (Medium and minor, never trigger a revision)

- Medium: M-1 (AC-C1 vs P0 deliverables), M-2 (contract trigger SA-3 vs WC-4), M-3 (AC-1.2 vs `load`), M-4 (WC-5 vs step 4 keys), M-5 (workflow id flag in P0), M-6 (P2 order, D2-D4 vs AC-1.1), Whittaker Sequence Attack (WC-3 vs AC-2.2).
- Minor: "well inside" the readiness limit has no number (`spec:59`); AC-2.4 pagination (`spec:202`); the `\|` escaping in AC commands (`spec:172-176,193`); WC-10 5 min vs AC-4.3 240 s; 0.70 confidence band (`spec:121`); E3 (`spec:23`) is listed as support although section 1.4 (`spec:43`) says that run proves only the Agent-tool route that WC-7 forbids, so E3 is overstated as evidence; N-5 below.
- N-5 (minor, UNVERIFIED): the `/sc:spec-panel` definition used for this audit already carries an `## Unattended mode` section with `--report-dir`, `<report-dir>/return-contract.yaml` and a read of `~/.claude/WORKER-CONTRACT.md` (`command.md:455-465`). The candidate's spec-panel row (`spec:120`) says "add `--output`" and WC-4 names `--output` / `--output-dir` (`spec:62`). Either the repo has moved since the inventory (`commands-b.md:185`), or the candidate's flag naming differs from the one in use. Section 2.1's `## Unattended mode` convention and section 3.2 should be checked against this before P2.
- Process note: the session that ran the review asks the user once per loop whether to open an issue for these follow-up candidates, and creates none without an answer; this run is non-interactive, so it only records the list.

## Reviser brief

Brief clauses overridden: none. Blocking finding ids: **B-1** only.

Reviser contract (restated from the Review Loop, bullet 6, since the reviser reads this report and not the command): revise only text a blocking finding names; add no rule, mechanism or section that no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with bytes added and deleted per finding id. Do not touch the Medium and minor items above.

- B-1: in `spec:182` and `spec:194`, narrow the P0 reading of step 3 so it does not require the WC-4 contract path.

coverage: whole document, first review, requirements and architecture focus; repo-side `src/` and Orca guide citations UNVERIFIED

verdict: FAIL

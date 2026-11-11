review: 1 of 3

# Gate review: orca-worker-contract-spec.md (`/sc:spec-panel --mode critique --focus requirements,architecture`)

## Header
- candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`
- candidate sha256: `fd9020aeb88b0fd3aa673b34de70465e3d6d2d18a0ec0245de39c5d2383e536b` (58573 bytes)
- baseline: not given (first review, gate prompt). baseline: missing is not an error here; no `--re-review` was passed.
- prior report: none. This is a first review of a complete document; no earlier report of this loop was seen.
- reviewer model actually used: Sonnet 5.5 (`claude-sonnet-5-5`)
- mode / focus: critique; requirements, architecture. `--focus correctness` is not active, so no State Variable Registry is produced.
- prompt followed: GATE prompt in `~/.claude/rules/prompts/document_review_loop_prompts.md` (read in full), graded with the FIRST-REVIEW grading check.
- brief clauses overridden: none.
- Citation shorthand: `SPEC:N` = line N of the candidate; `INV-A:N`, `INV-B:N`, `CAPS:N` = line N of `.dev/orca-command-refactor/inventory/commands-a.md`, `commands-b.md`, `orca-capabilities.md`; `README:N` = `.dev/orca-command-refactor/README.md`; `CMD:N` = line N of `command.md` (the `/sc:spec-panel` definition).
- Evidence limit: the workspace holds only the README, the three inventories and the candidate. Every citation to `src/`, `CLAUDE.md`, `tests/`, `.dev/codegraph-migration/`, `.dev/evals/` and Orca files outside the inventories is UNVERIFIED by me; where an inventory quotes it, I checked the quote, not the source.

## Prior blocking findings
None (first review).

## Coverage
Whole document read: sections 1-9, Decisions, UNVERIFIED items (SPEC:1-285). Cross-checked against the inventories: the 10 / 27 / 6 split and phase lists (SPEC:76-125, 156-162 against INV-A:73, INV-B:278), the CAPS and INV citations in sections 1-2 and 5, the acceptance checks in section 7 against the rows they test. Not checked: any `src/` line citation, the "re-read 11 locations" claim (SPEC:11), the "340 citations / 9 defects" claim (SPEC:285). Both claims are self-reports; UNVERIFIED.

Counts verified: 10 ready rows (SPEC:83-92) + 27 change rows (SPEC:99-125) + 6 coordinator-only rows (SPEC:132-137) = 43, matching INV-A:73 (5 / 13 / 3) plus INV-B:278 (5 / 14 / 3). Phase lists in SPEC:159-162 cover every command row exactly once (P1 9 + 4 fixes, P2 15, P3 4, P4 3).

=== REQUIREMENTS ANALYSIS ===

### BLK-1 (CRITICAL, expert: Wiegers, traceability; Whittaker, sequence attack) - `/sc:load` is required both to gain and not to gain an Unattended mode, and AC-1.1 cannot pass
- Grading sentence: An implementer who follows the stated text as written builds `/sc:load` with only a usage-line fix (SPEC:112, SPEC:159 "load (usage line only)", Decisions SPEC:265 "a report file would be an unrequested addition"), and P1's own acceptance test AC-1.1 then fails, because AC-1.1 asserts that every P1 command has a `## Unattended mode` section naming `return-contract.yaml` (SPEC:195), and X is wrong because the P1 gate can never pass for load, or passes only if the implementer adds the section and a contract that SPEC:112 and SPEC:265 say must not exist.
- Evidence of the contradiction:
  - SPEC:154 says a command gains `--unattended` and its section in the phase of its 3.2 row; the only exceptions listed are brainstorm, init-lite and a P4 command left unchanged by D2-D4. load is none of these, and its 3.2 row phase is P1 (SPEC:112).
  - SPEC:112: report "none (see note)", resume "n/a", "use it as a step inside another worker's brief, not as its own Task".
  - SPEC:195 (AC-1.1) names the P1 set by section 6, and SPEC:159 puts load in that set.
  - SPEC:196 (AC-1.2) runs the live check on each P1 command with `--unattended --output <dir>` and requires a contract with `status` and `command` (SPEC:183); load has no output flag and writes no file (INV-B:31, INV-B:62-65).
- Not a guess: the two readings are both stated, and each one breaks the other text.
- Recommendation: state load as an explicit exception in SPEC:154 and in AC-1.1/AC-1.2 (same wording used for brainstorm and init-lite), or give load a contract. Prefer the exception: it is a deletion of a test obligation, not new text.
- Priority: High. Quality impact: restores a passable P1 gate.

### BLK-2 (CRITICAL, expert: Wiegers; Whittaker, divergence attack) - WC-4 and the adversarial row name two different contract paths for the same flag value
- Grading sentence: An implementer who follows the stated text as written builds adversarial writing its contract at `<output>/adversarial/return-contract.yaml` (SPEC:83, "Small fix"), while the coordinator brief template and the acceptance checks expect `<output-dir>/return-contract.yaml` with `<output-dir>` being the `--output` directory (SPEC:62, SPEC:73 "report path is known before dispatch (WC-4)", SPEC:182-183), and X is wrong because the coordinator looks for a file that is not there and AC-1.2 steps 3 and 4 (`test -s <contract>`, "report path is the WC-4 contract path") fail for adversarial.
- Evidence:
  - SPEC:62 (WC-4): `<output-dir>/return-contract.yaml`, "`<output-dir>` is the directory the coordinator passed (`--output` / `--output-dir`)".
  - SPEC:83: adversarial brief passes `--output <dir>`, and the fix names `<output>/adversarial/return-contract.yaml`. INV-A:35 confirms the artifacts live under `<output>/adversarial/`, one level below the flag value, and INV-A:60 confirms real runs wrote the file in two different depths.
  - SPEC:198 (AC-1.4) only says "adversarial names one fixed path"; it does not say which, so it does not reconcile the two texts.
  - SPEC:73 promises the coordinator a path before dispatch; for adversarial that promise is false under SPEC:83.
- Recommendation: make WC-4 say the contract sits in the directory the command writes its artifacts to, and name that directory per command; or change SPEC:83 to `<output>/return-contract.yaml`. Narrowing one line is enough.
- Priority: High.

### MED-1 (MAJOR, graded Medium, expert: Wiegers) - `--unattended` with no output directory is undefined
- A requirement the document never states: WC-4 needs a coordinator-supplied directory (SPEC:62), SA-3 writes the new files "only in unattended mode or when the caller passes the new output flag" (SPEC:148), but no line says what a command does when `--unattended` arrives with no directory. The implementer must guess between refusing, using a default, and writing nothing. Contrast the command under review, which refuses before any work and prints the refusal in chat only (CMD:460). Not blocking: needs a guess.
- Recommendation: one sentence in WC-4: refuse in chat, no contract, exit.

### MED-2 (MAJOR, graded Medium, expert: Wiegers/Cockburn) - the "output directory" is a file for several commands
- SPEC:90 (tdd) and SPEC:87 (init-lite) pass `--output <file>`; SPEC:120 adds `--output` to spec-panel, while WC-4 puts the contract in `<output-dir>/` (SPEC:62) and AC-2.2 runs `/sc:tdd "auth" --unattended --output <file>` and then expects a contract with `blocked_question` (SPEC:200). Where the contract goes for a file-valued flag is not stated. The command definition itself already separates a file flag (`--output`) from a directory flag (`--report-dir`) (CMD:22, CMD:460-461); the spec has no such rule. Needs a guess about the location.
- Related: workflow's contract directory is derived from a generated id (`.dev/tasks/to-do/<id>/`, SPEC:92, INV-B:272), so it cannot be "known before dispatch" (SPEC:73), and the "pre-creation STOP" fix (SPEC:92) names no location because no package directory exists yet. cleanup-audit has a fixed output directory (SPEC:85), so a coordinator-passed directory does not exist there either.

### MED-3 (Medium, expert: Adzic) - `--unattended` propagation to nested command calls is stated for one case only
- Only tasklist Stage 10.5 passes `--unattended` to reflect (SPEC:122). Other commands invoke further commands: roadmap writes memory through `sc:save` at every wave (INV-B:154); brainstorm and release-split invoke adversarial and brainstorm (INV-B:119-121); tdd drives `/task` (INV-B:219-221); cli-eval create runs `/sc:spec-panel` and adversarial (INV-A:44). A roadmap worker in unattended mode that calls `sc:save` without the flag would hit the single-owner clobbering that WC-11 and the P3 save row exist to prevent (SPEC:69, SPEC:119). No requirement covers this; the wrong outcome needs the assumption that the nested call omits the flag.
- Recommendation: a one-line rule in the contract file: a command that calls another command passes `--unattended` when it calls one that supports it.

### MED-4 (Medium, expert: Nygard) - WC-10 trigger and the acceptance bound disagree
- WC-10 requires splitting only a step that blocks "longer than 5 minutes", into waits of "at most 4 minutes" (SPEC:68). AC-4.3 requires "no single tool call exceeds 240 s" (SPEC:210) and the pr-submit row requires each iteration under 4 minutes (SPEC:114). A 4.5-minute call passes WC-10 and fails AC-4.3. AC-4.3 is conditional on D3(b), whose recommendation is (a) (SPEC:240-242), and CAPS:182 says Orca's use of heartbeat age is UNVERIFIED, so no concrete wrong outcome follows. Align the trigger to 4 minutes.

### MED-5 (Medium, expert: Wiegers) - `--monitor 0` and `--monitor 2` are unspecified for pr-submit
- The row refuses `--monitor 1` only (SPEC:114); INV-B:89 names a y/n gate at `--monitor 1` and none at the default 3, and says nothing about 0 or 2 (UNVERIFIED). Matters only under D3(b).

### MED-6 (Medium, expert: Nygard) - WC-3 "re-invoke" and WC-6 "fresh directory" combine badly
- WC-3 lets the worker ask once and "re-invoke or resume the command with the answer as a flag" (SPEC:61); for most rows WC-6 resolves resume as "fresh dir" (SPEC:99-125), so a re-invocation redoes the whole run. Wasteful, not wrong; state that a re-invoked command with no resume flag starts fresh.

=== ARCHITECTURE ANALYSIS ===

### Decision soundness (Fowler, Newman, Nygard): no blocking finding
- The decision (Orca above, commands as units) is backed by checkable lines: depth 1 refusal and wording (CAPS:97-101), `worker_done` bound to the dispatched pane (CAPS:76, CAPS:150), commands run in other projects without Orca (CAPS:147-149), the second-orchestrator argument (INV-A:90, INV-B:285-286). The honest gap statement in SPEC:41-45 matches CAPS:156, CAPS:159-160, CAPS:186-187 and INV-B:323.
- Boundary check: Orca names stay out of the commands (WC-8, SA-2, SPEC:213); the contract file is the single shared interface (SPEC:52). Interface segregation is respected: the contract names no Orca command, so the same mode serves any caller (SPEC:51).

### MED-7 (Medium, expert: Fowler) - AC-C1 and SA-2 disagree about what the contract file may mention
- SA-2 allows Orca mentions "as an example of a caller's question channel inside the contract file" (SPEC:147); AC-C1 greps `src/superclaude/core` for `orca(-ide) orchestration|worktree|terminal|agent` and demands no output at every phase, `src/superclaude/skills/ccsession-tag/` excepted (SPEC:172). P0 adds `WORKER-CONTRACT.md` and an Orca section to `HOW-WE-WORK.md`, both under `core/` (SPEC:52, SPEC:158). If either text spells a literal `orca orchestration ...` command, AC-C1 fails on text SA-2 allows. Whether it does depends on how the author words the example. Needs a guess; Medium. Fix by excluding those two files from AC-C1 or by banning the literal form in SA-2.

### MED-8 (Medium, expert: Hohpe) - `blocked` is used in two vocabularies
- The contract status `blocked` (SPEC:62) shares a name with the Orca Task status `blocked` (CAPS:89), but WC-5 maps it to `--outcome failed` (SPEC:63), which makes the Task `failed` and keeps dependents blocked (CAPS:90). The mapping is stated, so nothing breaks; a coordinator that reads `blocked` as "Task blocked" would mis-wait. Add one sentence to the brief template.

### MED-9 (Medium, expert: Newman) - D3(b) meets a stated pr-submit "Will Not"
- INV-B:90 records that pr-submit lists "Will Not: run headless / imply a daemon" (`cmd/pr-submit.md:85`, `SKILL.md:225`; UNVERIFIED by me). SPEC:114 and D3(b) (SPEC:241) do not say whether a worker run counts as headless. The rule is only reached if the user chooses D3(b).

=== ADVERSARIAL ANALYSIS (Whittaker) ===
- Sequence attack, by-phase gating: "Later phases do not start until the earlier phase's checks pass" (SPEC:154) combined with AC-1.1 (SPEC:195) and the load row (SPEC:112). Concrete attack: finish all P1 edits exactly as section 3 says; run AC-1.1; load has no `## Unattended mode` section; AC-1.1 fails; P2 never starts. State trace: P1 done -> AC-1.1 red -> P2 blocked. See BLK-1.
- Divergence attack, one flag two paths: `--output D` for adversarial. WC-4 path `D/return-contract.yaml`; SPEC:83 path `D/adversarial/return-contract.yaml`. Both rules apply at once. See BLK-2.
- Zero/Empty attack: `--unattended` with no directory (MED-1); `--unattended` on a command with no output flag yet (SPEC:99-125 rows that "add `--output`" in the same phase as the flag, so no gap inside a phase).
- Sentinel collision: `blocked` (MED-8). `partial` maps to `succeeded` (SPEC:63, SPEC:263), a user-visible choice that is recorded, not hidden: no finding.
- Accumulation attack: two workers in one worktree each writing a fixed directory (`.claude-audit/`, SPEC:85) is acknowledged under WC-11 (SPEC:69). Counter: the circuit breaker counts failed starts, not a worker's own `failed` reports (CAPS:80), so repeated `blocked` retries never trip it; the spec does not cap retries of a `blocked` Task. Note only; the coordinator owns retries (SPEC:64).
- Attacks that failed: count conservation of the 43 commands (verified above); phase coverage (verified above).

## Guard Condition Boundary Table
Guards found: the 60 s readiness limit, the 5-minute heartbeat and 4-minute wait split, the nesting depth, the task confidence 0.70 gate, the `--monitor` ordinal gate, the outcome mapping, the circuit breaker. Classes not shown for a guard are left out for the stated reason (FR-10).

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|---|---|---|---|---|---|---|
| readiness limit | SPEC:59 (WC-1) | Zero/Empty | `--timeout-ms` 0 or absent | default 60 s | falls to the default (CAPS:44-45) | OK |
| readiness limit | SPEC:59 | Typical | wrapper fallback 30 s | pass | passes at 34 s (CAPS:49) | OK |
| readiness limit | SPEC:59 | Maximum/Overflow | `--timeout-ms` above the accepted bound | unknown | upper bound UNVERIFIED (CAPS:54, CAPS:176) | GAP (Medium: WC-1 never relies on raising the limit) |
| readiness limit | SPEC:59 | Legitimate Edge Case | fallback just over 45 s | fail | stated: fails again above about 45 s (SPEC:59) | OK |
| heartbeat / wait split | SPEC:68 (WC-10) | Typical | 3-minute wait | no split | no split needed | OK |
| heartbeat / wait split | SPEC:68 | Legitimate Edge Case | 4.5-minute single call | trigger ">5 min" false | passes WC-10, fails AC-4.3 (SPEC:210) | GAP (MED-4) |
| heartbeat / wait split | SPEC:68 | Maximum/Overflow | 3600 s eval (INV-A:65) | split | split into at most 4-minute waits (SPEC:104) | OK |
| nesting depth | SPEC:33, SPEC:66 | Typical | depth 1, worker calls `worker-start` | refused | `nested_worker_depth_exceeded` (CAPS:99) | OK |
| nesting depth | SPEC:66 | Legitimate Edge Case | `task-create` from depth-1 worker | unknown | forbidden anyway by WC-8 (SPEC:66, SPEC:276) | OK |
| task confidence gate | SPEC:121 | Zero/Empty | confidence 0 | below 0.70 | blocked | OK |
| task confidence gate | SPEC:121 | Legitimate Edge Case | exactly 0.70 | not below | proceeds (INV-B:199 "< 0.70") | OK |
| `--monitor` gate | SPEC:114 | Typical | `--monitor 1` | refused | refused under `--unattended` | OK |
| `--monitor` gate | SPEC:114 | Legitimate Edge Case | `--monitor 0`, `--monitor 2` | unknown | not specified | GAP (MED-5) |
| outcome mapping | SPEC:63 | Zero/Empty | no report exists | failed | `--outcome failed` | OK |
| outcome mapping | SPEC:63 | Sentinel Value Match | `status: blocked` | failed | `--outcome failed` | OK (MED-8 is a note) |
| outcome mapping | SPEC:63 | Legitimate Edge Case | `status: partial`, audit verdict FAIL | succeeded | `--outcome succeeded`, body states status | OK |
| circuit breaker | SPEC:64 | Typical | three failed starts | trips | counted across `--retry-of` (CAPS:80, CAPS:116) | OK |
| circuit breaker | SPEC:64 | Sentinel Value Match | worker's own `failed` x3 | does not trip | CAPS:80 | OK |

Classes left out: One/Minimal for every guard (no input of size one changes any branch; all are thresholds or enumerations); Maximum/Overflow for the confidence gate, the outcome mapping and the `--monitor` gate (bounded enumerations or a score capped at 1.0); Sentinel Value Match for the readiness limit, depth, heartbeat and confidence gate (no sentinel values in their texts). The table is complete; no blank Specified Behavior cell. FR-8 GAP entries are all graded Medium (no concrete wrong outcome follows from the stated text).

Pipeline Dimensional Analysis: not triggered (the phases are not a data pipeline with count divergence); the only count conservation, 43 = 10 + 27 + 6, was verified directly.

## Follow-up candidates (Medium and minor; none triggers a revision)
Medium: MED-1, MED-2, MED-3, MED-4, MED-5, MED-6, MED-7, MED-8, MED-9 (above).
Minor notes:
- MIN-1: D5(b) says raising depth would "break R1's protection against runaway fan-out" (SPEC:252); R1 (SPEC:33) is a refusal argument, not a fan-out protection. Wording only.
- MIN-2: SPEC:11 and SPEC:285 assert completed citation re-reads; I could not check either (UNVERIFIED). The inventories carry their own check claims (INV-A:106, INV-B:320) that I also cannot re-run.
- MIN-3: all `src/`, `CLAUDE.md` and Orca-file citations are UNVERIFIED in this sandbox (examples: SPEC:25, SPEC:52, SPEC:65, SPEC:150).
- MIN-4: SPEC:139 and SPEC:112 both call load a worker-capable command while section 4 says only six commands are coordinator-only; consistent, noted for BLK-1 wording.
- Question for the user (once per loop): whether to open an issue for the follow-up candidates. Not asked here: this sandbox has no user channel and no `--unattended` flag was given; the coordinator should ask, and no issue was created.

## Reviser brief
Blocking finding ids: BLK-1, BLK-2. Nothing else.

Rules for the reviser (restated from the command's Review Loop, bullet 6; you read this report, not the command):
- Revise only text a blocking finding names.
- Add no rule, mechanism or section that no blocking finding calls for.
- Each added paragraph or table cites its finding id.
- Prefer deleting or narrowing to adding.
- Report the byte size of the candidate before and after (now 58573), with the bytes added and deleted per finding id.
- Leave minor and Medium findings alone, whatever any brief says. Return the candidate once and do not award yourself a PASS.

verdict: FAIL

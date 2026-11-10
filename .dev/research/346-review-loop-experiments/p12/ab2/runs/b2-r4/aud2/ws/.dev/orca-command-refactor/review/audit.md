review: 1 of 3
candidate: .dev/orca-command-refactor/specs/orca-worker-contract-spec.md
candidate sha256: c9e2ff995f731358d2c486eecbe202f9c810da58a248e59a7c693464e08d5a7b
baseline: none (first review of the whole document, labelled whole-document audit)
reviewer model: Sonnet 5.5 (claude-sonnet-5-5)
command: /sc:spec-panel @.dev/orca-command-refactor/specs/orca-worker-contract-spec.md --mode critique --focus requirements,architecture
prompt followed: FIRST-REVIEW prompt, ~/.claude/rules/prompts/document_review_loop_prompts.md:27-32
brief clauses overridden: none

Citation key: `SPEC:N` = line N of the candidate. `INV-A`, `INV-B`, `CAPS` = line N of `.dev/orca-command-refactor/inventory/commands-a.md`, `commands-b.md`, `orca-capabilities.md`. `CMD:N` = line N of the /sc:spec-panel command definition in the sandbox (`command.md`). Citations to `src/`, `CLAUDE.md`, `~/.claude/` skills and the Orca guides are not in the workspace and are marked UNVERIFIED unless an inventory line quotes them.

## Coverage

- Read in full: README.md, the candidate (292 lines), the FIRST-REVIEW prompt, and the command definition.
- Checked against inventories: the 43 = 21 + 22 command count and the 10 / 27 / 6 split (recounted from SPEC:84-132 and the INV-A:3 and INV-B:3 command lists, consistent); the cited CAPS lines for readiness (CAPS:44-46,52), ask (CAPS:58,64,68), worker_done and report-path (CAPS:72-80), depth (CAPS:97-103), executable and identity (CAPS:145-151), subagents (CAPS:155,158); the INV lines for pr-submit (INV-B:34,87-95), reflect (INV-B:107-115), workflow (INV-B:267-275), the coordinator-only rows (INV-A:90-92, INV-B:285-287), and the cross-cutting findings (INV-A:94-98, INV-B:289-301).
- Not checkable (UNVERIFIED): every `src/superclaude/...:N`, `CLAUDE.md:N`, `HOW-WE-WORK.md:N`, `pyproject.toml:38`, `install_core.py` and `Makefile` citation, the `.dev/codegraph-migration` and `EVIDENCE.md` citations, and the Orca guide text beyond what the CAPS lines quote. The candidate's own claims of a 11-location re-read (SPEC:11) and a 340-citation check (SPEC:285) are also unverifiable here.
- Not reviewed: fidelity of the inventories to the real command files.

## Panel and method

Panel in the command's fixed order (CMD:101-113), focus requirements then architecture (CMD:131-151): Wiegers, Adzic, Cockburn, Fowler, Nygard, Whittaker, Newman, Hohpe, Crispin, Gregory, Hightower. Whittaker's five attacks are applied to the candidate's thresholds and sequences (CMD:76-80). Every finding below passed the grading check (FIRST-REVIEW prompt, line 31): blocking only if the sentence "an implementer who follows the stated text as written builds X, and X is wrong because Y" holds with no further assumption.

Pipeline Dimensional Analysis (CMD:349-353) is not triggered: the candidate describes no multi-stage data pipeline whose output count differs from its input count. The one count the document asserts, 43 = 10 + 27 + 6, is conserved.

## Prior blocking findings

None (first review).

## === REQUIREMENTS ANALYSIS ===

### B1. The P0 gate cannot pass as written (BLOCKING, CRITICAL)
Experts: Wiegers, Adzic, Crispin.
- Stated text A: SPEC:73 says the brief "states the exact command line including `--unattended`". SPEC:194 (AC-0.4) runs three commands "each run directly by the worker" and requires "steps 1-3 and 5-7 pass".
- Stated text B: SPEC:182 gives the pass condition of step 3 as "its `--outcome` matches the contract's `status` under WC-5; its report path is the WC-4 contract path". SPEC:79 says that until Phase 1 "the worker reports the named file", and SPEC:194 itself says "the contract arrives in P1". SPEC:92 says workflow's contract may be missing. `/sc:troubleshoot` reports `REPORT.md` (SPEC:91), which is not a WC-4 contract.
- An implementer who follows the text builds P0 smoke runs on troubleshoot, workflow and adversarial. For troubleshoot, step 3 can never pass: no contract exists, so its `--outcome` cannot "match the contract's status", and its report path is not "the WC-4 contract path". The `--unattended` flag also does not exist before P1 (SPEC:159), so the brief of SPEC:73 cannot be followed either.
- This is wrong because SPEC:154 says later phases do not start until the earlier phase's checks pass, and SPEC:194 says a failure "reopens section 1". The first gate of the programme fails by construction, or the implementer silently relaxes it, and then the evidence gap of SPEC:43 stays unclosed.
- Recommendation: state in AC-0.4 which pass conditions of steps 3 and 4 apply in P0 (for example: outcome matches the command's own report; report path equals the named existing report file) and say the brief omits `--unattended` in P0.
- Priority High. Quality impact: restores a passable first gate.

### B2. P1 and AC-1.1 contradict D3(a), the pr-submit rows and the phase column (BLOCKING, MAJOR)
Experts: Wiegers, Fowler, Cockburn.
- Stated text A: SPEC:159 (P1) has "the `--unattended` flag accepted by every command in sections 3.1 and 3.2 except load". SPEC:195 (AC-1.1) requires every command in 3.1-3.2 other than load to have a `## Unattended mode` section. Section 3.2 includes implement (SPEC:109), post-release (SPEC:113) and pr-submit (SPEC:114).
- Stated text B: those same three rows carry phase P4 (SPEC:109,113,114), and SPEC:162 says P4 "waits for D2-D4". SPEC:240 (D3(a), the recommendation) says "no pr-submit changes in Phase 4", and SPEC:139 says pr-submit stays a worker candidate only if D3 is accepted. SPEC:154 says Phases 1-3 need no user decision.
- An implementer who follows the text builds, in P1, a `--unattended` flag and an `Unattended mode` section on pr-submit, implement and post-release, because AC-1.1 fails otherwise. That is wrong because (i) D3(a) is "coordinator or person only", so the user never chose to change pr-submit; (ii) the inventory records that pr-submit's own contract says "Will Not: run headless" (INV-B:90, quoting `cmd/pr-submit.md:85`, `SKILL.md:225`; UNVERIFIED in source), so a P1 `--unattended` flag on it contradicts a stated Will Not before any decision; (iii) the flag would be accepted as a no-op while the safety-relevant gates (D2, D4) it governs are not yet decided, so a worker could be dispatched with `--unattended` on a command whose gate resolution is not specified yet.
- Recommendation: restrict P1's flag and AC-1.1 to the commands whose section-3 phase is P1-P3, and add the P4 commands to AC-1.1 only after D2-D4.
- Priority High. Quality impact: removes a contradiction between acceptance test and decision gate.

## Medium findings (warnings; follow-up candidates, none blocking)

### M1. "Fresh output directory" conflicts with "path known before dispatch" (Medium; graded Medium because the implementer must pick between two readings)
Experts: Adzic, Nygard.
- SPEC:64 (WC-6) lets a command with no resume flag "write each run into a fresh output directory"; SPEC:62 (WC-4) and SPEC:73 require the contract path to be computed from the brief before dispatch. Most of the 27 rows in section 3.2 use "fresh dir" as their resume mechanism (for example SPEC:99-101).
- Reading 1: the command creates a fresh subdirectory itself, so the coordinator cannot know the contract path. Reading 2: the coordinator passes a new `--output` on each retry, so the command does nothing and "fresh dir" is a coordinator duty. The text does not say which, and a `--retry-of` worker reusing the first attempt's `--output` (the exact hazard of SPEC:64) is not forbidden anywhere.
- Recommendation: state who creates the fresh directory and that a retry brief must carry a new output path.

### M2. No behaviour when the output path is missing under `--unattended` (Medium; requirement the document never states)
Experts: Wiegers, Whittaker (Zero/Empty attack).
- SPEC:62 gives three forms of contract path, all derived from `--output` / `--output-dir` or a fixed row path. SPEC:62 also says the contract is "written on success, failure, blocked and partial outcomes". Commands that "add `--output`" (analyze, build, design, test and others, SPEC:99-123) have no stated result when the flag is omitted: there is no place to write the blocked contract that WC-2(c) (SPEC:60) requires. The shipped /sc:spec-panel design refuses before any work in that case (CMD:460), which the spec neither adopts nor rejects.
- Recommendation: add one sentence to WC-4: under `--unattended`, a missing output path is refused in chat before any work.

### M3. WC-4 path rules differ from the shipped /sc:spec-panel unattended design (Medium)
Experts: Fowler, Newman.
- SPEC:120 says spec-panel needs "add `--output`; contract". The command already has `--output` (CMD:23) and defines `--report-dir <dir>` as the directory key because "`--output` is file-valued" (CMD:460), writing `<report-dir>/return-contract.yaml` (CMD:461). WC-4 instead derives `<file>.return-contract.yaml` from a file-valued `--output` (SPEC:62) and says nothing of `--report-dir`. Two contract-path conventions then coexist. CMD:457 also points at `~/.claude/WORKER-CONTRACT.md`, which SPEC:52 only proposes.
- Recommendation: either adopt `--report-dir` as the directory key in WC-4 or state why spec-panel is an exception.

### M4. Existing contracts' `status` vocabulary vs the fixed four-value set (Medium)
Experts: Wiegers, Hohpe.
- SPEC:62 says commands that already write a contract "keep their fields and add the missing ones"; SPEC:262 fixes `status` to `succeeded|partial|failed|blocked` and 7.2 step 4 (SPEC:183) asserts that set. Workflow's existing contract already has a `status` field (INV-B:272); its allowed values are not recorded in the inventory (UNVERIFIED). If its values differ, "keep their fields" and the assertion in step 4 conflict. The same holds for brainstorm, reflect and adversarial (SPEC:261).
- Recommendation: state whether an existing `status` value set is kept or mapped.

### M5. tasklist Stage 10.5 and reflect `--remediate` under `--unattended` (Medium)
Experts: Nygard, Whittaker (Divergence attack).
- SPEC:88 makes `/sc:reflect --remediate` follow the "headless auto-accept rule" under `--unattended`; SPEC:122 has tasklist pass `--unattended` to each reflect "so the headless rule applies". The inventory instead recommended calling reflect without `--remediate` so no offer can fire (INV-B:215), and records that the headless rule auto-accepts remediation for auto-fixable registers (INV-B:109). The spec does not say whether Stage 10.5 still passes `--remediate`. If it does, an unattended tasklist worker auto-accepts a remediation chain (a workflow or task-builder hand-off) nobody authorized. WC-9 (SPEC:67) covers outward actions only, not this chain.
- Recommendation: say that Stage 10.5 passes no `--remediate` under `--unattended`.

### M6. WC-3 "re-invoke with the answer as a flag" has no flag for several gates (Medium)
Experts: Cockburn, Hohpe.
- SPEC:61 lets a worker ask the coordinator and re-invoke "with the answer as a flag". Rows with no named answer flag: cli-portify's three approval gates (SPEC:105 names only a `--resume` flag), implement's Ruling (SPEC:109, and D2 SPEC:233-236), task's confidence and TFEP gates (SPEC:121), review-translation Phase 7 (SPEC:117). Option (a)/(b) of WC-2 then does not cover them and the only path is "blocked".
- Recommendation: list the answer flag per gate, or say WC-3 applies only to gates that have one.

### M7. WC-10 covers two commands only (Medium)
Experts: Nygard, Hightower.
- SPEC:68 states a general rule (no single tool call over 5 minutes), but section 3 applies it only to cli-eval (SPEC:104) and pr-submit (SPEC:114). Other rows can run long single calls (test, build, implement, roadmap, validate-roadmap dispatching a CLI pipeline, SPEC:101,109,123,124). CAPS:130 records that whether Orca uses heartbeat age is itself UNVERIFIED, so impact is liveness reporting, not data loss.
- Recommendation: either scope WC-10 to the two commands or add a one-line check for the others.

### M8. pr-submit report path is not known before dispatch (Medium)
Experts: Fowler, Newman.
- The run log lives in a default directory `.dev/pr-monitor/pr-<N>-<ts>/` (INV-B:92), where `<N>` and `<ts>` are unknown until the command runs. SPEC:114 says the contract goes "beside `monitor-run-<PR>.jsonl`" and does not require `--output-dir` in the brief (cf. SPEC:62, SPEC:73). Under D3(b) this breaks the "known before dispatch" rule.
- Recommendation: if D3(b) is chosen, require `--output-dir` in the brief.

### M9. AC-C5 and AC-C1 may not be satisfiable as written (Medium)
Experts: Crispin, Gregory.
- AC-C5 (SPEC:176) requires no removed line (`^-[^-]`) in any command file edited without a named defect. SA-4 (SPEC:149) calls the edits "new flags", and SPEC:99-123 add flags such as `--output` and `--unattended`. If a flag is added to an existing Usage line, that line shows as removed and the check fails; if flags go in a new line or table row it passes. The text does not say where a new flag is documented.
- AC-C1 (SPEC:172) requires no `orca orchestration|worktree|terminal|agent` match in `src/superclaude/core`, while SA-2 (SPEC:147) allows the contract file, which is in `core` (SPEC:52), to name Orca "as an example of a caller's question channel", and P0 adds an Orca section to HOW-WE-WORK.md, also in `core` (SPEC:158). An example written as `orca orchestration ask` fails AC-C1.
- Recommendation: say where new flags are documented and exempt the contract file and the routing guide section in AC-C1, or forbid the literal string there.

## === ARCHITECTURE ANALYSIS ===

Overall the architecture is sound. The decision to keep Orca above the commands is supported by cited evidence (SPEC:19-26 against CAPS:97-103,145-151,155,158), the rejected alternative is argued with five reasons (SPEC:31-37) and the evidence gaps are stated honestly (SPEC:41-46). No architecture finding is blocking.

Notes:
- Fowler: the single shared contract file plus a short per-command section (SPEC:52) is a clean separation of responsibilities. The section 4 split (SPEC:128-137) keeps one controller per level (INV-A:90, INV-B:285-286).
- Newman / Hohpe: the outcome mapping to Orca's two outcomes (SPEC:63, SPEC:262-263) is explicit. `blocked` surfaces as `failed` with a status in the file, so the coordinator must open the report (SPEC:62). That is acceptable because CAPS:79 records that Orca does not verify the file.
- Nygard: a blocked worker that writes a contract and stops (SPEC:60) avoids the silent stall of SPEC:44 and CAPS:52,129. WC-12's `consumer_fenced` handling (SPEC:70, CAPS:67) covers ownership loss.
- Minor: SPEC:164 sends every phase through `/sc:workflow` then `/sc:implement`; that sequence is not checked against HOW-WE-WORK.md (UNVERIFIED).
- Minor: SPEC:79 says the 10 ready commands run "as workers now", yet tdd, release-split and troubleshoot need gate fixes in P2 (SPEC:90-91); the "ready today" label holds only for the flag set the row names.

## Guard Condition Boundary Table

Guards identified: depth limit, readiness timeout, heartbeat/wait split, confidence threshold, partial-outcome mapping, empty diff in changed-line checks. Input classes left out are given with a one-line reason. Status GAP entries are graded per FR-8: all are Medium (no concrete wrong outcome without a further guess); none is blocking.

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|---|---|---|---|---|---|---|
| nested depth (R1/WC-8) | SPEC:33,72 | Typical | depth 1 | true | worker may not start workers; command never calls `worker-start` | OK |
| nested depth (R1/WC-8) | SPEC:33,72 | Legitimate Edge Case | user raises depth to 2 (D5) | false | D5 recommends keep; enforcing call sites not traced (CAPS:103) | OK (UNVERIFIED enforcement noted in SPEC:33) |
| readiness limit (WC-1) | SPEC:59 | Typical | 60 s default | true | no launch-path prompt allowed | OK |
| readiness limit (WC-1) | SPEC:59 | Maximum/Overflow | `--timeout-ms` raised | n/a | per start allowed (CAPS:45) | OK |
| output path (WC-4) | SPEC:62 | Zero/Empty | `--output` omitted under `--unattended` | n/a | not specified | GAP (M2, Medium) |
| output path (WC-4) | SPEC:62,64 | Legitimate Edge Case | retry reuses first attempt's dir | n/a | not specified for "fresh dir" commands | GAP (M1, Medium) |
| wait split (WC-10) | SPEC:68 | Typical | wait of 4 min | true | split so heartbeat fits | OK |
| wait split (WC-10) | SPEC:68 | Maximum/Overflow | single call over 5 min in a command other than cli-eval/pr-submit | n/a | no row, no check | GAP (M7, Medium) |
| confidence gate (task) | SPEC:121 | Typical | below 0.70 | true | blocked | OK |
| confidence gate (task) | SPEC:121 | Sentinel Value Match | exactly 0.70 | not stated | not stated (inherited from the command) | GAP (Medium; command text outside the workspace, UNVERIFIED) |
| outcome mapping (WC-5) | SPEC:63 | Legitimate Edge Case | status `partial` | n/a | `--outcome succeeded`, body states `partial` | OK |
| outcome mapping (WC-5) | SPEC:63 | Zero/Empty | no report exists | true | `--outcome failed` | OK |
| re-review empty diff | CMD:262 | Zero/Empty | empty diff | n/a | prior blockers stay open | OK (command rule, not a candidate guard) |

Classes left out: One/Minimal and Sentinel for depth, readiness and wait guards, because those take only a threshold with no collection or reserved value.

## Adversarial analysis (Whittaker)

- Zero/Empty attack: missing `--output` under `--unattended` leaves no place for the WC-2(c) blocked contract (M2).
- Divergence attack: two readings of "fresh dir" (M1); `--remediate` auto-accept vs "no remediation" in tasklist (M5).
- Sentinel Collision attack: `--unattended` is also the token a command's quoted content could contain; the shipped command resolves this ("standalone argument token outside any quoted argument", CMD:459) while the spec does not. Medium, folded into M3 follow-up.
- Sequence attack: P1 flags land on P4 commands before D2-D4 are decided (B2); P0 gate demands P1 artifacts (B1).
- Accumulation attack: none found; no counter or buffer is specified.

## Follow-up candidates

Medium: M1, M2, M3, M4, M5, M6, M7, M8, M9, and the Guard Condition Boundary Table GAP rows (they restate M1, M2, M7 and the unverified confidence-boundary sentinel).
Minor notes: the two architecture notes above; the `ask` timeout default is already listed UNVERIFIED (SPEC:281); the citation coverage caveat (Coverage section).
The session that runs this review asks the user once per loop whether to open an issue for these; this worker creates none and asks nothing (non-interactive sandbox), so the question is left to the coordinator.

## Reviser brief

Blocking finding ids: B1, B2. Reviser contract (restating CMD:263): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id. Leave Medium and minor findings alone. Candidate size before: 58375 bytes.
- B1: repair only AC-0.4 (SPEC:194) and, if needed, step 3 and 4 wording in 7.2 (SPEC:182-183) so that the P0 pass conditions can hold before P1 adds the contract and `--unattended`; and say the P0 brief omits `--unattended`.
- B2: repair only the P1 scope (SPEC:159) and AC-1.1 (SPEC:195) so that they do not require the flag or the `## Unattended mode` section on implement, post-release or pr-submit before D2-D4.

verdict: FAIL

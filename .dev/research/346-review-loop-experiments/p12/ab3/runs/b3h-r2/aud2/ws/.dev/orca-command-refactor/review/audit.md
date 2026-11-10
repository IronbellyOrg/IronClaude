review: 1 of 3

# Spec-panel audit: orca-worker-contract-spec.md (labelled whole-document audit, first review)

- command: `/sc:spec-panel @.dev/orca-command-refactor/specs/orca-worker-contract-spec.md --mode critique --focus requirements,architecture`
- candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`, 290 lines, sha256 `d33b89a08efc2ef08e5a0449828d8b35251424cc7d54958dac98f929b1383529`
- baseline: none given; this is a first review of the full document (no `--re-review`, no `--baseline`)
- reviewer model actually used: claude-sonnet-5-5 (Sonnet 5.5)
- review date: 2026-11-10
- prompt followed: FIRST-REVIEW prompt of `~/.claude/rules/prompts/document_review_loop_prompts.md` (read in full before reviewing)
- brief clauses overridden: none
- citation convention: `S:N` = line N of the candidate spec; `INV-A:N`, `INV-B:N`, `CAPS:N` = lines of `inventory/commands-a.md`, `commands-b.md`, `orca-capabilities.md` (the only checkable evidence). Any citation to a file outside the workspace (`src/`, `CLAUDE.md`, `EVIDENCE.md`, `orca-data.json`, Orca source) is UNVERIFIED.

## Coverage

Whole spec read: sections 1-9, Decisions, UNVERIFIED items. Checked: every `INV-A`, `INV-B` and `CAPS` citation in sections 1-4, 8 and 9 against the three inventory files (about 90 citations, all land on the claimed content; none wrong); the 10 / 27 / 6 split (INV-A:73 gives 5 / 13 / 3, INV-B:278 gives 5 / 14 / 3; sums to 10 / 27 / 6 = 43, and the section 3.1, 3.2 and 4 tables list exactly 10, 27 and 6 commands); the phase table (S:158-162) against the section 3 rows (every command appears in exactly one phase); acceptance checks (S:169-215) against requirements WC-1..WC-12 and SA-1..SA-6. Not checked (UNVERIFIED, outside workspace): all `cmd/`, `sk/`, `src/` path:line citations the spec carries from the inventories, `CLAUDE.md:*`, `EVIDENCE.md:*`, `.dev/codegraph-migration/*`. Not covered: the correctness focus (not requested), so no State Variable Registry.

## Expert panel (critique mode)

Panel for the focus: Wiegers (lead), Adzic, Cockburn (requirements); Fowler (lead), Newman, Hohpe, Nygard (architecture); Whittaker active in every review. Order followed: Wiegers, Adzic, Cockburn, Fowler, Nygard, Whittaker, Newman, Hohpe. Crispin, Gregory and Hightower are outside the two focus panels and raised nothing separate.

Grading note: each finding below was graded by consequence with the FIRST-REVIEW grading check. Two findings pass it (blocking). Everything else needs a guess between two allowed readings, or is a requirement the document never states, so it is Medium whatever its label.

=== REQUIREMENTS ANALYSIS ===

### AUD-B1 (BLOCKING) | label CRITICAL | Wiegers, Adzic | priority High

Issue: the P0 acceptance check AC-0.4 cannot pass for two of its three commands, and P0 gates the whole rollout.

Grading sentence: an implementer who follows AC-0.4 as written (S:199) runs step 4 of the live check (S:188), a YAML parse asserting `d['status']` and `d['command']`, on "the same existing report file". For `/sc:troubleshoot` the existing report is `REPORT.md` (S:91; INV-B:242), a markdown file with no `status` or `command` key, so step 4 and the step 3 comparison "against that file's status under WC-5" (S:199) cannot pass. For `/sc:adversarial` the "Report today" cell is "contract, but filename not fixed" (S:83) and the real runs wrote it to two different places (INV-A:60), so no existing report path can be named in the brief. The spec says a phase passes only when every check in its block passes (S:167) and that a failure of AC-0.4 "reopens section 1" (S:199), so P0 fails, and the decision (section 1) is reopened for a defect in the check, not in the decision.

Third command: for `/sc:workflow` the existing contract's fields are listed as `status`, `plan_path`, `reflect_report_path` (INV-B:272), and `command` is not among them; whether it is present is UNVERIFIED, so the same step 4 may also fail there.

Recommendation: narrow AC-0.4 step 4 for P0 to "the file named by `--report-path` exists and is non-empty"; take the outcome check from the report's own stated result, not from a `status` key that REPORT.md does not have; for adversarial, pass a fixed `--output` and read the path from `worker_done --report-path`. Rationale: the YAML assertion belongs to the WC-4 contract that arrives in P1 (S:199 says so itself).
Quality impact: Testability 4 -> 8.

### AUD-B2 (BLOCKING) | label CRITICAL | Wiegers, Fowler | priority High

Issue: P1 ships a `--unattended` flag on commands whose unattended behaviour, including the outward-action defaults WC-9 requires off, lands in P2 or P4, or never.

Grading sentence: an implementer who follows P1 (S:159: "the `--unattended` flag accepted by every command in sections 3.1 and 3.2 (a no-op where a command has no gate)") and AC-1.1 (S:200: every command in 3.1-3.2 has an `## Unattended mode` section) builds, after P1, an `--unattended` flag on auggie-review, task, post-release, pr-submit and implement that is accepted but leaves their defaults on. Those defaults are posting review comments to a PR (S:100, phase P2), `commit`/`push` and a committed TFEP report (S:121, P2), installs, VM, commit and PR (S:113, P4), push/PR/thread resolution (S:114, P4), and the implement Ruling halt (S:109, P4). That is wrong because WC-9 says "Under `--unattended`, any default that pushes, opens a PR, posts to GitHub, installs, provisions or calls a paid external run is off" (S:67), and the spec says each phase stands alone and leaves the system consistent (S:154). A coordinator that follows D1(a) (S:233) and writes `--unattended` into the brief of a P1-era auggie-review gets a GitHub post and a remediation wait, the two things the flag is documented to prevent. AC-1.1 and AC-1.2 (S:200-201) pass on the section's presence and a happy path, so nothing in P1 catches it.

Second contradiction in the same text: D3(a), the recommended option, says "no pr-submit changes in Phase 4" and section 4 says commands outside the worker set "get no `--unattended` mode" (S:128, S:139, S:245), but pr-submit is in the 27 that "gain the `## Unattended mode` section" (S:82) and AC-1.1 (S:200) requires it in P1. Under D3(a) an implementer still adds the flag to pr-submit.

Recommendation: narrow P1 and AC-1.1 to the commands whose section 3 phase is P1 (and the ready commands whose small fix is P1); every other command gains `--unattended` in the phase that lands its row, and pr-submit only if D3(b) is chosen. This is a deletion from S:159 and S:200, not a new mechanism.
Quality impact: Consistency 5 -> 8; removes a safety-boundary window.

### Medium findings (follow-up candidates, not blocking)

**AUD-M1 | label MAJOR, graded Medium | Wiegers, Adzic | priority Medium.** Several requirements have no acceptance check: WC-3 (ask, blocked, resume by message ID; S:61), WC-6 (retry and resume; S:64), WC-12 (S:70), WC-10 for cli-eval (S:68; only pr-submit has a check, AC-4.3, S:215, and only under D3(b)), WC-11 for index-repo, init-lite and cleanup-audit (S:69; only `save` has a check, AC-3.4, S:212). The P1 refusals (business-panel `--mode socratic`, explain `--format interactive`, test `--watch`; S:102, S:108, S:123) have no gate-trigger run: AC-2.2 (S:205) covers P2 commands only and AC-1.2 (S:201) is a happy path. Why Medium: a requirement left unverified, no stated text does harm. Recommendation: one check per requirement, in the phase that implements it.

**AUD-M2 | label MAJOR, graded Medium | Fowler, Hohpe | priority Medium.** Contract location is under-determined. (a) research: the row gives "contract naming the generated `claudedocs/research_*.md` path" and no flag or directory (S:116; INV-B:132 says the file name is generated at run time), yet WC-4 needs the path in the brief before dispatch (S:62). (b) tdd: `--output` is a file (S:90), WC-4's default is `<output-dir>/return-contract.yaml` (S:62), and only the init-lite row says `<output-dir>` is the file's directory and requires a unique directory per worker (S:87); two tdd workers whose `--output` files share a directory share one contract path, against WC-11 (S:69). (c) The live definition of `/sc:spec-panel` in this sandbox (`command.md:23`, `command.md:460-461`) already has file-valued `--output` and a separate `--report-dir` for the contract, and `--unattended` is refused without it, while the spec row says "add `--output`" (S:120) and the inventory says the flag does not exist (INV-B:182). Either the inventory is stale against the live command or the spec row is; which is newer is UNVERIFIED. Recommendation: state in WC-4 which flag names the contract directory per command, and give research, tdd and spec-panel a row entry.

**AUD-M3 | label MAJOR, graded Medium | Nygard, Cockburn | priority Medium.** WC-3 says a human-Ruling gate "never takes a coordinator answer" (S:61) while D2(b) lets the coordinator relay the person's words (S:240) and non-goal 6 allows it if the user picks (b) (S:223). Only one option can hold, and it is open until D2 is answered. Also WC-3 says the session may "ask the coordinator once" (S:61); cli-portify has three approval gates (S:105) and review-translation two (S:117), so "once" is per run or per gate, unstated. Recommendation: make WC-3's Ruling clause conditional on D2 and say "once per gate".

**AUD-M4 | label MAJOR, graded Medium | Whittaker (Sequence attack) | priority Medium.** Live-check step 2 passes when "`observation.agentWait` is never non-null" (S:186). CAPS:129 says null means Orca looked and found no wait, and an absent field means it never looked. An absent field satisfies "never non-null", so a worker parked on a prompt can pass step 2. Step 3 (exactly one `worker_done`, S:187) would still catch a stall at the end, so no wrong build follows, but the early-stall detector the step exists for does not detect. Recommendation: require an observed `null`.

**AUD-M5 | label MAJOR, graded Medium | Adzic, Whittaker (Zero/Empty attack) | priority Medium.** AC-C5 (S:176) and AC-0.3 (S:198) use `grep -E '^-[^-]'` on `git diff -U0`. A deleted or changed markdown bullet line `- x` appears in the diff as `-- x`, which that pattern excludes, and command files are mostly bullets. The check prints nothing when bullets are removed, so it does not enforce SA-4 ("edits are additive", S:149) for them. Routing-table rows start with `|`, so AC-0.3 is sound for `HOW-WE-WORK.md` table rows only. Recommendation: count deletions with `git diff --numstat` (second column must be 0) instead.

**AUD-M6 | label MAJOR, graded Medium | Whittaker (Divergence attack), Fowler | priority Medium.** See the Pipeline Dimensional Analysis below. WC-4 and section 2.3 fix one output directory per Task in the brief (S:62, S:73), while WC-6 says a non-resumable command "writes each run into a fresh output directory" (S:64) and about 20 rows say "fresh dir". A retry (`worker-start --retry-of`, CAPS:116) re-runs the same Task brief. Reading A: the command creates a fresh subdirectory, so the contract path is not known before dispatch (against WC-4/F-01). Reading B: the brief reuses the directory and the retry overwrites the first attempt (against WC-6). Only the init-lite row (S:87) says the coordinator passes a new directory per attempt. FR-19 would label this CRITICAL; graded Medium because the failure needs the implementer to pick the worse reading. Related: AC-3.2 (S:210) runs roadmap with an existing `<dir>/.session-memory.md` and expects "starts fresh" in that same directory, which overwrites the earlier attempt's artifacts rather than blocking. Recommendation: say in WC-6 that the coordinator supplies a new directory per attempt for non-resumable commands.

**AUD-M7 | label MAJOR, graded Medium | Nygard (Accumulation attack) | priority Medium.** WC-10 (S:68) applies to any step that blocks a single tool call for more than 5 minutes, but names only cli-eval and pr-submit. A foreground Agent-tool fan-out (tdd, adversarial, cleanup-audit, troubleshoot Tier 2; S:90, S:83, S:85, S:91) also blocks the session, and the command text cannot split it. Whether Orca uses heartbeat age at all is UNVERIFIED (CAPS:182, item 7, and CAPS:130). The requirement is unmeasurable for these commands. Recommendation: scope WC-10 to the two named commands, or say what a long foreground fan-out must do.

**AUD-M8 | label MAJOR, graded Medium | Wiegers | priority Medium.** Provenance of the scope claims. The "43 commands in `cmd/`" (S:76) is the sum of the two inventories' scope lists (INV-A:3, INV-B:3); neither inventory says it listed the directory, and no directory listing is cited. E5 (S:25) rests on a `grep` over `src/` that is not checkable here. The invoking environment's skill list describes `sc:issue` as creating an Orca worktree and launching an agent in it; that is outside the workspace so UNVERIFIED, but if such a command file exists in `cmd/` it contradicts E5 and the count of 43, and it would make AC-C1 ("prints nothing", S:172) fail at the P0 baseline. Recommendation: cite a directory listing and the grep output.

**AUD-M9 | label MINOR, graded Medium | Newman | priority Low.** WC-4 says commands that already write a contract "keep their fields and add the missing ones" (S:62) while the Decisions table fixes the status set to four values (S:267). The statuses existing contracts use (workflow, reflect, brainstorm, adversarial) are not shown in the inventories (INV-B:272 lists field names only), so a conflict between "keep" and the fixed set is UNVERIFIED.

**AUD-M10 | label MAJOR, graded Medium | Hohpe, Nygard | priority Medium.** (a) pr-submit's own file says "Will Not: run headless / imply a daemon" (INV-B:90), and the spec's 3.2 row and D3(b) turn it into an unattended worker without addressing that line (S:114, S:246); it matters only if D3(b) is chosen. (b) tasklist under `--unattended` passes the flag to each reflect so reflect's headless auto-accept applies to `--remediate` (S:122, S:88; INV-B:109). That hands remediation to workflow or task-builder, which writes a package, and no WC-9 or WC-11 clause bounds those writes in parallel reflects; the spec's own item 9 (S:285) says an Orca worker is not headless, so what the flag reuses is only by definition. Recommendation: state the bound or turn auto-accept off for the tasklist path.

### Minor notes

- AUD-N1 (Wiegers): WC-1 says a fallback "well inside" the 60 s limit (S:59) with no number; the evidence gives 30 s passing and about 45 s failing (CAPS:49).
- AUD-N2 (Wiegers): E3 "It has worked before" (S:23) is stronger than section 1.4 (1), which says the PR #329 run proved only the nested route (S:43).
- AUD-N3 (Adzic): an empty value for a required flag (for example `--target-release ""`, S:120) is not covered by the "else blocked" wording.
- AUD-N4 (Adzic): step 3 of the live check waits "until `worker_done` arrives" with no overall bound (S:187), and no worked example brief exists for any section 3 row beyond D1's one line (S:233).

=== ARCHITECTURE ANALYSIS ===

The decision itself (Orca coordinates, commands stay units of work, S:16-17) is supported by the checkable evidence: R1 (depth 1 refuses `worker-start` inside a worker, CAPS:97-101), R2 (CAPS:147-149), R3 (CAPS:76, CAPS:150), E2 and E4 (CAPS:155, CAPS:161) all land on the lines cited. The honest weakness is gap 1 in section 1.4 (no direct end-to-end run), which the spec states (S:43) and turns into P0; that is why AUD-B1 matters: the check that is supposed to test the decision cannot pass as written.

Fowler (interfaces): the shared contract file plus per-command `## Unattended mode` sections is a clean split (S:58). The seam that leaks is the output-directory contract (AUD-M2, AUD-M6). Newman (evolution): phases are additive and mostly independent, except the P1 flag scope (AUD-B2). Hohpe (message exchange): the worker_done once-per-dispatch rule, pull-only follow-ups (WC-12) and ask resume by message ID (WC-3) are consistent with the capabilities inventory (CAPS:60, CAPS:66-67, CAPS:76).

Whittaker attack findings (template FR-3):

- I can break this specification by **Sequence attack**. The invariant at **AC-0.4 / 7.2 step 4 (S:188, S:199)** fails when **the command's existing report is not a YAML contract**. Concrete attack: run `/sc:troubleshoot "x"` as a P0 worker; it writes `REPORT.md`; step 4 calls `yaml.safe_load` on markdown and indexes `d['status']`; the check fails; P0 fails; section 1 is "reopened". Severity: blocking (AUD-B1).
- I can break this specification by **Sequence attack**. The invariant at **WC-9 (S:67) versus P1 (S:159)** fails when **P1 is released alone**. Concrete attack: state after P1 = auggie-review accepts `--unattended`; a coordinator brief says `/sc:auggie-review 123 --unattended`; the P2 row that turns off `--post-pr` (S:100) has not shipped; the command posts to the PR. Severity: blocking (AUD-B2).
- I can break this specification by **Divergence attack**. The invariant at **WC-4 versus WC-6 (S:62, S:64)** fails when **a non-resumable command is retried with the same brief**. Concrete attack: Task T, dir D, attempt 1 fails after writing D/return-contract.yaml (`status: partial`); `worker-start --retry-of` re-sends the same brief; attempt 2 writes D/return-contract.yaml; attempt 1's record is gone. Severity: Medium (AUD-M6).
- I can break this specification by **Zero/Empty attack**. The invariant at **AC-C5 (S:176)** fails when **the edit deletes a markdown bullet**. Concrete attack: remove line `- Will Not: x` from a command file; diff shows `-- Will Not: x`; the grep prints nothing; the check passes. Severity: Medium (AUD-M5).

=== GUARD CONDITION BOUNDARY TABLE ===

Trigger met: the spec contains thresholds and conditionals (4 and 5 minute waits, 60 s readiness, 0.70 confidence, status mapping, acceptance pass conditions). Hard gate FR-10: table completed before synthesis. Classes omitted per guard are named in the line under the table.

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|-------|----------|-----------------|----------------|--------------|-------------------|--------|
| WC-10 wait split | S:68 | Zero/Empty | no blocking call | not triggered | nothing to split | OK |
| WC-10 wait split | S:68 | Typical | poll plus sleep under 4 min | satisfied | worker heartbeats between waits | OK |
| WC-10 wait split | S:68 | Maximum/Overflow | one foreground Agent-tool fan-out above 5 min | triggered | none: command text cannot split it | GAP (AUD-M7) |
| WC-10 wait split | S:68 | Legitimate Edge Case | cli-eval single eval up to 3600 s (INV-A:65) | triggered | split into waits of at most 4 min | OK |
| WC-5 outcome map | S:63 | Zero/Empty | no report file | true | `--outcome failed` | OK |
| WC-5 outcome map | S:63 | Zero/Empty | report file exists, 0 bytes | unclear | not stated (step 4 `test -s` would fail, S:188) | GAP (minor) |
| WC-5 outcome map | S:63 | Sentinel Value Match | `status` not in the four values | unclear | not stated; an existing contract's own value (AUD-M9) | GAP |
| WC-5 outcome map | S:63 | Legitimate Edge Case | `partial`, or audit verdict FAIL | true | `--outcome succeeded` | OK |
| WC-1 readiness | S:59 | Typical | fallback 30 s | passes | start passes (CAPS:49) | OK |
| WC-1 readiness | S:59 | Legitimate Edge Case | fallback near 45 s | unclear | "well inside" with no number | GAP (AUD-N1) |
| WC-3 ask once | S:61 | One/Minimal | one gate | true | ask, resume by message ID | OK |
| WC-3 ask once | S:61 | Legitimate Edge Case | command with 3 gates (cli-portify, S:105) | unclear | "once" per run or per gate not stated | GAP (AUD-M3) |
| WC-3 Ruling clause | S:61 vs S:240 | Legitimate Edge Case | D2 option (b) chosen | true | contradicts "never takes a coordinator answer" | GAP (AUD-M3) |
| task confidence | S:121 | Typical | 0.50 | true | blocked | OK |
| task confidence | S:121 | Legitimate Edge Case | exactly 0.70 | false | proceeds ("below 0.70" is blocked) | OK |
| 7.2 step 2 agentWait | S:186 | Zero/Empty | field absent | true (passes) | passes, though Orca never looked (CAPS:129) | GAP (AUD-M4) |
| AC-C5 additive edit | S:176 | Legitimate Edge Case | deleted bullet `- x` | false (not caught) | check prints nothing | GAP (AUD-M5) |
| AC-C3 baseline | S:174 | Zero/Empty | baseline run has 0 passing tests | false | nothing can regress | OK |
| AC-C3 baseline | S:174 | Legitimate Edge Case | a flaky test passes in baseline, fails after | true | phase fails; no re-run rule stated | GAP (minor) |
| P1 flag scope | S:159, S:200 | Legitimate Edge Case | command whose gate row is P2/P4 (auggie-review) | true | flag accepted, defaults still on | GAP (AUD-B2) |

Classes left out: WC-10 One/Minimal and Sentinel (a wait is either present or not; there is no sentinel); WC-5 One/Minimal and Typical other than the rows shown (the four named statuses map one to one, S:63); WC-1 Zero/Empty (a zero-second fallback is the same as no prompt); task-confidence Zero/Empty (confidence is always computed, INV-B:199 gives no empty case) and Maximum (1.0 is above the threshold, no special case); AC-C3 Maximum (no capacity bound); P1 flag scope Zero/Empty (a command with no gate and no outward default is the "no-op" case S:159 already covers). GAP rows were graded in the findings above; none is blocking unless marked B.

## Pipeline Dimensional Analysis

Trigger (FR-17): met. The spec describes a multi-stage flow (Tasks -> dispatches -> `worker_done` -> report read) where count can diverge: retries add dispatches for one Task (`--retry-of`, CAPS:116). Fowler annotated, Whittaker attacked. The 43 -> 10 / 27 / 6 classification conserves count (checked above).

```text
[Coordinator: N Tasks, one brief and one output dir each (S:73)]
        |
        v
[worker-start: N first dispatches + R retries, R >= 0 per Task]  --> N+R dispatches
        |
        v
[Command run per dispatch: N+R runs, each writes <dir>/return-contract.yaml (WC-4)]
        |
        v
[worker_done: exactly 1 per dispatch (WC-5) -> N+R messages]
        |
        v
[Coordinator opens the report: expects 1 contract per Task]  <-- MISMATCH when R > 0 and the dir is shared (non-resumable "fresh dir" commands, WC-6)
```

Step 4 (consistency): the spec handles the divergence for init-lite only (S:87, new directory per attempt) and for resumable commands (resume flag); it does not for the roughly 20 "fresh dir" rows. Recorded as AUD-M6 (Medium: two allowed readings).

## Dispositions and follow-up candidates

Blocking, open: AUD-B1, AUD-B2.

follow-up candidates (Medium and minor, no revision triggered, none appears in the Reviser brief): AUD-M1, AUD-M2, AUD-M3, AUD-M4, AUD-M5, AUD-M6, AUD-M7, AUD-M8, AUD-M9, AUD-M10, AUD-N1, AUD-N2, AUD-N3, AUD-N4.

Issue question: the loop asks the user once whether to open an issue for the follow-up candidates. This run's final reply is limited to the output path, so the question was not asked, and no issue was created. The list is recorded here for the session that owns the loop.

Citation check result: no wrong `INV-A`, `INV-B` or `CAPS` line found. Everything else cited by the spec is UNVERIFIED in this sandbox.

## Reviser brief

Blocking finding ids: AUD-B1, AUD-B2.

Reviser contract (restated from the command, bullet 6): revise only text a blocking finding names; add no rule, mechanism or section that no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size of the candidate before and after, and the bytes added and deleted per finding id; leave minor and Medium findings alone; return the candidate once and do not award yourself a PASS.

- AUD-B1: edit only S:188 / S:199 (AC-0.4 step 4 and its step 3 clause). Narrow step 4 for P0 to an existence and non-empty check on the file given to `--report-path`, and take the outcome comparison from the report's stated result. Delete the YAML assertion for P0.
- AUD-B2: edit only S:159 (P1 scope sentence), S:200 (AC-1.1) and, if needed, S:82. Limit the `--unattended` flag and the `## Unattended mode` section in P1 to the commands whose section 3 phase is P1; the others gain them in their own phase; pr-submit only under D3(b).

verdict: FAIL

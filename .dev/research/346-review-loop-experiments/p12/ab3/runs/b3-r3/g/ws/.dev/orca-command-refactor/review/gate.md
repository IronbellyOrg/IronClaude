review: 1 of 3

# Gate review: orca-worker-contract-spec.md (`/sc:spec-panel --mode critique --focus requirements,architecture`)

- candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`
- candidate sha256: `e40e99ee4052bc08befc7a5c553a10250f30eed258a771b80b4e6936f8bf5bff`
- baseline: none (first review of the complete document; no `--re-review`, no `--baseline`)
- prompt followed: GATE prompt of `~/.claude/rules/prompts/document_review_loop_prompts.md:57-64`, graded with the FIRST-REVIEW grading check (`:35`); read in full before reviewing
- reviewer model actually used: claude-sonnet-5-5 (Sonnet 5.5)
- panel: Wiegers, Adzic, Cockburn (requirements); Fowler, Newman, Hohpe, Nygard (architecture); Whittaker (always active, review order 6)
- fresh context: this reviewer saw no earlier report of the loop
- citation key: `S:N` = line N of the candidate; `INV-A:N` / `INV-B:N` / `CAPS:N` = line N of `inventory/commands-a.md`, `commands-b.md`, `orca-capabilities.md`
- Citation status: inventory and spec lines below were opened and compared in this sandbox. Anything that points at `src/`, `CLAUDE.md`, `EVIDENCE.md`, `.dev/codegraph-migration/...` or `~/.claude/...` is UNVERIFIED because those files are not in the workspace; the spec's own claim of a re-read (S:11) cannot be confirmed here.

## What was covered

Whole document, S:1-285. Section 1 decision and evidence; section 2 requirements WC-1..WC-12; section 3 per-command tables (counts re-derived); section 4; section 5 SA-1..SA-6; section 6 phases; section 7 acceptance checks; section 8; section 9 D1-D5; the Decisions and UNVERIFIED lists. The Orca claims cited through `CAPS:` lines were compared with those lines (CAPS:44-46, 52, 58-61, 64, 66-68, 72-80, 92, 97-103, 107, 115-116, 129-130, 145-150, 155, 159-161, 178-188): each one says what the spec says it does. Command-side claims were compared with the inventory lines (INV-A:35, 39, 53, 55, 60-62, 65, 76-83, 90-98, 106, 113, 118, 120; INV-B:3, 31-36, 43, 52, 272, 285-299, 311, 320, 323). Command and skill source files were not checked (not in the workspace).

Counts conserved: 43 commands = 21 (INV-A:3) + 22 (INV-B:3). Ready 10 = 5 (adversarial, brainstorm, cleanup-audit, index-repo, init-lite) + 5 (reflect, release-split, tdd, troubleshoot, workflow); needs-change 27 = 13 + 14 (INV-B:289 gives 14); coordinator-only 6 = 3 + 3 (INV-A:90-92, INV-B:285-287). The 27 section 3.2 rows split by phase as P1 9, P2 11, P3 4, P4 3; with the four ready commands changed in P2 the P2 list at S:160 has 15 names, and they match. No count mismatch found.

## Requirements analysis (Wiegers lead, Adzic, Cockburn)

=== REQUIREMENTS ANALYSIS ===

### GF-01 (blocking, MAJOR) - the P0 gate cannot pass as written
- Expert: Wiegers (testability), Adzic (concrete example fails)
- Stated texts: S:158 says P0 makes "no command edits" and runs `/sc:troubleshoot`, `/sc:workflow --handoff none`, `/sc:adversarial --output <dir>` as workers; S:154 says later phases "do not start until the earlier phase's checks in section 7 pass"; S:194 (AC-0.4) says "steps 1-3 and 5-7 pass; step 4 uses the command's existing report file, since the contract arrives in P1"; S:182 (7.2 step 3) says the pass condition includes "its `--outcome` matches the contract's `status` under WC-5; its report path is the WC-4 contract path"; S:73 (2.3) requires the brief to carry "the exact command line including `--unattended`"; S:159/S:160 introduce `--unattended` only in P1 and P2; S:79 says ready commands report "the named file until Phase 1 adds the contract".
- Wrong outcome: An implementer who follows the stated text as written builds P0 with unmodified commands (no contract, no `--unattended` flag), and then AC-0.4 requires 7.2 step 3 to pass. Step 3 demands a worker_done report path equal to the WC-4 contract path and an outcome that matches the contract's `status`; no contract exists in P0, and the text itself says so in step 4. AC-0.4 therefore cannot pass, so P0 cannot pass, and S:154 plus the S:194 clause "a failure here reopens section 1" make the failure stop the rollout. Step 1's brief (S:73) also requires `--unattended` on a command line whose command rejects or ignores it until P1/P2.
- Recommendation: narrow AC-0.4 so that for P0 step 3 requires only the exactly-one `worker_done` and an outcome matching the command's existing report, with `--report-path` set to that existing file, and say the P0 brief omits `--unattended`.
- Priority: High. Quality impact: restores the only live test of the decision in section 1.4 (S:43).

### Medium findings (follow-up candidates; none blocks)
- GM-01 (Medium) - **Contract path missing for two P1 commands.** S:85 (cleanup-audit) and S:86 (index-repo) give a small fix only ("name the `--pass all` final report", "state the output location"). S:76 says every changed command gains the `## Unattended mode` section, S:195 (AC-1.1) tests a section naming `return-contract.yaml` for every P1-row command, and S:196 (AC-1.2) runs the live check "with its `--output` as WC-4 gives it". WC-4 (S:62) gives a path rule for the directory/file cases, adversarial, cli-eval and workflow only, and says "a row in section 3 states any other path"; neither row does, and index-repo has no output flag (INV-A:53). The implementer must guess a path. Needs a guess about the worse of two readings, so Medium. Recommendation: one path per command in the row.
- GM-02 (Medium) - **`--unattended` without `--output` is unspecified (FR-9 blank behavior).** S:62 defines the contract path only where "the brief passes a directory"; S:148 (SA-3) says files appear "only in unattended mode or when the caller passes the new output flag". Nothing says what an unattended run with no output flag does (block, or default to a path). S:62 also requires a contract "including stops before any other output exists", which has no location in that case. Only post-release and document state a requirement for an explicit output (S:107, S:113).
- GM-03 (Medium) - **Contract name derivation for file-valued `--output`.** S:62: `.dev/tdd/auth.md` gives `.dev/tdd/auth.return-contract.yaml`, "with `.return-contract.yaml` in place of its extension". An output with no extension, or two outputs differing only in extension (`auth.md`, `auth.txt`) leaves the name undefined or colliding.
- GM-04 (Medium) - **Retry versus fixed contract path (Whittaker sequence attack).** WC-4 (S:62) fixes the contract path before dispatch; WC-6 (S:64) says a retry worker either resumes or "writes each run into a fresh output directory". If the command creates the fresh directory itself, the contract moves and `--report-path` (S:62) points at the old file; if the brief reuses the same `--output`, a retry that dies before writing leaves the first attempt's contract, and WC-5 (S:63) reads "no report exists" as failed when a stale report does exist. The text does not say who picks the fresh path or that a stale contract is removed first.
- GM-05 (Medium) - **WC-3 re-invocation "with the answer as a flag" has no flag for several gates.** S:61 lets the worker ask the coordinator and "re-invoke or resume the command with the answer as a flag". The gates in S:109 (implement Ruling), S:105 (cli-portify approvals), S:114 (pr-submit HALTs) and S:121 (task confidence) list no such flag. For implement it also sits against the Ruling rule the spec keeps (S:233-238: "another agent's message does not count"), because WC-3 reads as permitting the relay that D2 option (b) would make an explicit decision. The command's own rule would still refuse, so the harm is an unspecified path, not a bypass.
- GM-06 (Medium) - **WC-9 lets the brief authorize outward actions without the user.** S:67 turns an outward default on "only through the command's own explicit flag written in the brief"; D4 (S:244-247) recommends "only when the user's own instruction to the coordinator names that action", but S:225 says phases 0-3 proceed on the recommendations without waiting, and S:160 puts auggie-review `--post-pr` and task `commit`/`push` in P2. Until D4 is answered, WC-9 as written lets a coordinator write the flag itself.
- GM-07 (Medium) - **Thresholds without a sharp boundary.** WC-10 (S:68) triggers at a call "longer than 5 minutes" but requires waits "at most 4 minutes": a 4.5 minute call is neither required to split nor within the 4 minute limit, while AC-4.3 (S:210) tests 240 s only for pr-submit. WC-1 (S:59) says a fallback "well inside" the 60 s limit; the only number is 30 s in the evidence column.
- GM-08 (Medium) - **WC-5 on a malformed contract.** S:63 maps `failed`/`blocked`/no report to failed and everything else, including `partial`, to succeeded. A contract that exists but has a `status` outside the four values (S:62) or no parseable YAML is not covered; AC step 4 (S:183) only checks that a valid one passes.
- GM-09 (Medium) - **WC-4 keeps existing fields but fixes the status vocabulary.** S:62 says commands that already write a contract "keep their fields and add the missing ones", and requires `status` to be one of four values. The workflow contract already has a `status` field (INV-B:272) whose values the inventories do not list; S:262 considered "copy each command's own statuses" and rejected it without saying how existing values map.
- GM-10 (Medium) - **E3 versus section 1.4 (1).** S:23 cites the PR #329 run and the `skill-direct` contract line as evidence it worked; INV-A:35 calls adversarial "proven as a direct Orca-worker skill call"; S:43 says that same run "proves the nested route, not the direct route". The spec chose the cautious reading and Phase 0 tests it (S:158), but E3 and INV-A:35 still read as proof. Align the wording of E3.
- GM-11 (Medium) - **WC-1 has no deliverable.** S:59 assigns it to "launch setup, not commands" and S:214 forbids changing Orca settings, but no phase in S:156-162 and no check in S:171-210 owns the launch-wrapper fallback. 7.2 step 1 (S:180) detects a failure only after the fact.
- GM-12 (Medium) - **WC-11 versus fixed output files.** S:69 forbids two workers writing the same file; index-repo writes `PROJECT_INDEX.md` at a fixed location (INV-A:53) and S:86 only asks to "state the output location"; cleanup-audit is excused by "one audit per worktree" (S:85). The index-repo clobber is not addressed.

## Architecture analysis (Fowler lead, Newman, Hohpe, Nygard)

=== ARCHITECTURE ANALYSIS ===

Sound: the decision (Orca on top, commands unchanged units) is consistent with the Orca facts: depth 1 (CAPS:97-101), `worker_done` bound to the dispatched pane (CAPS:76, CAPS:150), standalone failure without a runtime (CAPS:147), and workers as top-level sessions (CAPS:161). One shared contract file referenced by installed path follows the repo rule (S:52, S:264). Pipeline Dimensional Analysis (FR-17): not triggered; the rollout is a coordinator-to-worker fan-out with no filter, aggregate or dedupe stage, and the only count identities (43 = 10+27+6, and the per-inventory splits) hold. No Quantity Flow Diagram required.

- GM-13 (Medium, Nygard) - **No coordinator-side deadline for a silent worker.** S:44 says the real failure for a command prompt is a silent stall seen only through `worker-show` or a missing report; S:73 lists what the coordinator owes but not a stall limit or action; S:182 step 3 waits "until `worker_done` arrives" with a 900000 ms window and no rule for what follows; Orca's bound on dispatch time is UNVERIFIED (S:282, CAPS:188). Detection exists (agentWait, S:181), the response is unspecified.
- GM-14 (Medium, Fowler) - **Two meanings of "contract".** S:52 defines "Contract file" as `WORKER-CONTRACT.md`; S:76 defines "Contract" as the WC-4 return file. SA-2 (S:147) allows a mention of Orca "inside the contract file" and AC-C1 (S:172) greps `src/superclaude/core`, which would hold `WORKER-CONTRACT.md` and the Orca section of `HOW-WE-WORK.md` that P0 adds (S:158). If either text carries an `orca orchestration ...` command form, AC-C1 fails against SA-2's own permission; E5 records zero mentions in `HOW-WE-WORK.md` today (S:25).
- GM-15 (Medium, Newman) - **AC-C5 versus SA-4.** S:149 allows "new flags" as additive; S:176 requires that `git diff -U0 ... | grep -E '^-[^-]'` print nothing for a command without a named defect fix. A new flag added by editing the Usage line produces a `-` line and fails AC-C5; the text does not say flags are appended on new lines. A reviser who reads SA-4 naturally edits the Usage line (the `load` row at S:112 names that as a defect fix, which shows the normal route is editing that line).
- GM-16 (Medium, Nygard) - **D3 option (b) omits the command's own "run headless" prohibition.** INV-B:90 quotes "Will Not: run headless / imply a daemon" (`cmd/pr-submit.md:85`, `SKILL.md:225`, UNVERIFIED here). S:238-242 and S:114 present pr-submit as a worker with an `--unattended` mode and do not mention it, so the user choosing D3 is not shown the conflict.
- GM-17 (Medium, Nygard) - **Unattended cleanup and improve and the unverified rollback.** S:103 and S:110 apply "only items the file already allows without approval" and call the rollback mechanism UNVERIFIED (INV-A:118), covering the loss risk only by listing changed files. That is not new risk (the allowance is the command's own), so not blocking, but a worker deleting files has no stated recovery.

## Adversarial analysis (Whittaker)

=== ADVERSARIAL ANALYSIS ===

- **Sequence attack:** I can break this specification by the Sequence Attack. The invariant at **WC-4/WC-5/WC-6 (S:62-64)** fails when **a retry reuses the brief's `--output` and dies before writing**. Concrete attack: attempt 1 writes `<dir>/return-contract.yaml` with `status: failed`; the retry crashes at step 2; before: file = attempt 1, `check` shows no `worker_done`; after the coordinator's recovery session reads the file it sees attempt 1's failure and attributes it to the retry. Severity: Medium (see GM-04).
- **Zero/Empty attack:** I can break it by the Zero/Empty Attack at **S:62** when `--unattended` is passed with no `--output`: the contract has no path, the "stop before any output" case (S:62) has nowhere to write, and `--report-path` cannot be supplied (S:74). Medium (GM-02).
- **Sentinel collision attack:** at **S:62** the `.return-contract.yaml` extension substitution collides for `a.md`/`a.txt` or extensionless names. Medium (GM-03).
- **Divergence attack:** at **S:68** a call of exactly 4.5 minutes sits between the 5 minute trigger and the 4 minute cap. Medium (GM-07).
- **Accumulation attack:** at **S:162/S:182** an unbounded wait for `worker_done` with no deadline (GM-13); WC-10's 3600 s cli-eval runs (INV-A:65) are covered by the splitting rule, which is OK.
- Divergence and sentinel attacks on the blocking path itself produced GF-01, not an additional finding.

## Guard Condition Boundary Table (complete before synthesis)

Classes left out are given with a one-line reason in the notes under each guard.

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|-------|----------|-----------------|----------------|--------------|-------------------|--------|
| readiness fallback (WC-1) | S:59 | Typical | fallback 30 s | true | passes (EVIDENCE.md:45, UNVERIFIED) | OK |
| readiness fallback (WC-1) | S:59 | Maximum/Overflow | fallback above ~45 s | false | fails again, stated only as evidence, requirement says "well inside" | GAP (GM-07) |
| `--unattended` + output (WC-4/SA-3) | S:62, S:148 | Zero/Empty | no `--output` | n/a | not specified | GAP (GM-02) |
| `--unattended` + output (WC-4) | S:62 | Legitimate Edge Case | extensionless or same-stem file `--output` | n/a | not specified | GAP (GM-03) |
| heartbeat wait split (WC-10) | S:68 | Typical | 10 min call | true | split to waits of at most 4 min | OK |
| heartbeat wait split (WC-10) | S:68 | Legitimate Edge Case | 4.5 min call | false | not required, but cap says 4 min | GAP (GM-07) |
| status mapping (WC-5) | S:63 | Typical | `partial` | true | outcome succeeded, body states partial | OK |
| status mapping (WC-5) | S:63 | Zero/Empty | no report file | true | outcome failed | OK |
| status mapping (WC-5) | S:63 | Sentinel Value Match | `status` outside the four values or unparseable file | n/a | not specified | GAP (GM-08) |
| retry (WC-6) | S:64 | Legitimate Edge Case | retry with same `--output`, crash before write | n/a | stale contract not addressed | GAP (GM-04) |
| nesting depth (R1/WC-8) | S:33, S:66 | Typical | depth 1 | true | worker-start refused | OK |
| nesting depth (R1/WC-8) | S:33 | Maximum/Overflow | depth raised by user (D5) | n/a | D5 recommends keeping 1 | OK |
| task confidence (3.2) | S:121 | Typical / Edge | below 0.70 | true | blocked | OK |
| task confidence (3.2) | S:121 | Legitimate Edge Case | exactly 0.70 to 0.89 | n/a | not stated (cmd/task.md:93 UNVERIFIED; the agent command prompts in that band, INV-A:36) | GAP (UNVERIFIED, noted under follow-ups) |
| `--monitor 1` (pr-submit) | S:114 | Typical | `--monitor 1` | true | refused under `--unattended` | OK |

Left-out classes: readiness fallback "Zero/Empty" and "One/Minimal" (a zero or non-positive `--timeout-ms` falls back to the 60 s default, CAPS:44, outside the spec); heartbeat split "Zero/Empty" (no wait, nothing to split); nesting depth "Zero/Empty" (root coordinator, depth 0, is not a worker, CAPS:97); WC-5 "Maximum/Overflow" (no count involved); confidence "Zero/Empty" (a missing score is the command's own case, UNVERIFIED). Hard gates: FR-8/FR-9 were graded by consequence: none of the GAP rows names a concrete wrong outcome or a security, data-loss or safety-boundary risk on its own, so they are Medium, listed above and not blocking. FR-10: the table is complete.

## Quality assessment (0-10)

Clarity 7; Completeness 7; Testability 6 (blocked by GF-01 and the AC-C5 / AC-C1 conflicts); Consistency 6.

## Follow-up candidates

Medium: GM-01 to GM-17 above. Minor notes:
- MN-1: AC-C5's `grep -E '^-[^-]'` (S:176) cannot see a removed line that itself begins with `-`.
- MN-2: the refusal of `--interactive` under `--unattended` is stated for cleanup, improve, test, business-panel, roadmap (S:102-103, S:110, S:118, S:123) and left to "never `--interactive`" in the brief for adversarial, brainstorm, release-split (S:83-84, S:89); one rule would remove the difference.
- MN-3: the business-panel frontmatter fix is in scope (S:102) although its effect is UNVERIFIED (S:278) and non-goal 8 (S:220) limits scope to defects that stop worker use.
- MN-4: the pr-submit top-level rule is cited at `SKILL.md:37-39` for the repo copy (S:65, INV-B:90) and at `:47-49` for the installed copy in CAPS:161; both are UNVERIFIED here and refer to different copies.
- MN-5: S:11 reports a re-read of 11 locations and S:285 a 340-citation check; neither can be reproduced from the workspace (UNVERIFIED).
- The question about opening an issue for the follow-up candidates is left to the coordinator: this run had no user to ask, and no issue was created.

## Reviser brief

Blocking finding ids: GF-01.

Brief (restated from the command's Review Loop, bullet 6): Revise only text that GF-01 names (the AC-0.4 row at S:194, and where needed the 7.2 step 3 pass condition at S:182 and the P0 brief wording that carries `--unattended`). Add no rule, mechanism or section that GF-01 does not call for. Each added paragraph or table row cites GF-01. Prefer deleting or narrowing to adding. Report the byte size of the candidate before and after, and the bytes added and deleted per finding id. Leave every Medium and minor finding (GM-01 to GM-17, MN-1 to MN-5) alone. Return the candidate once; do not award yourself a PASS.

verdict: FAIL

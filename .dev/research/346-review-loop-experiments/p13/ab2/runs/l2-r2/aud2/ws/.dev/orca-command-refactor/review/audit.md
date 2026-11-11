review: 1 of 3

# Spec-panel audit: orca-worker-contract-spec.md (labelled whole-document audit, first review)

- command: `/sc:spec-panel @.dev/orca-command-refactor/specs/orca-worker-contract-spec.md --mode critique --focus requirements,architecture`
- candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md` (285 lines)
- candidate sha256: `0686b734a23ad02747840178fa995a98e02d1dad4e7ef5e12322d1cb7ce8879d`
- baseline: none given (first review, whole document)
- reviewer model used: claude-sonnet-5-5
- prompt followed: FIRST-REVIEW prompt, `~/.claude/rules/prompts/document_review_loop_prompts.md:27-32` (read in full)
- panel: Wiegers (lead), Adzic, Cockburn (requirements); Fowler (lead), Newman, Hohpe, Nygard (architecture); Whittaker (adversarial, active in every review, `command.md:83`)
- citation convention: `SPEC:N` = line N of the candidate; `CAPS:N`, `INV-A:N`, `INV-B:N` = the three files under `.dev/orca-command-refactor/inventory/`; `README:N` = `.dev/orca-command-refactor/README.md`.

## Coverage statement

Covered: the whole candidate (sections 1-9, Decisions, UNVERIFIED list), read line by line. I read the README and checked citations against the only checkable evidence: the three inventory files.

Checked and found as cited: CAPS:44-47, 52, 58, 64, 66, 72, 76, 79, 86, 92, 98-99, 103, 107, 113, 115-116, 129-130, 147-151, 155-156, 158-161, 178, 180, 186-188; INV-A:14, 35, 62, 95, 106, 113, 118, 120; INV-B:289, 311, 320, 323. I also recounted the 10 / 27 / 6 split: INV-A has 5 ready, 13 needs-change and 3 coordinator-only (21); INV-B has 5, 14 and 3 (22); SPEC:76 matches, and the SPEC:81-92 and SPEC:97-125 rows match those counts (10 and 27).

UNVERIFIED (cannot be checked inside the workspace): every `cmd/…`, `sk/…`, `CLAUDE.md:…`, `src/…`, `pyproject.toml:…`, `Makefile:…`, `EVIDENCE.md:…`, `.dev/codegraph-migration/…` and `HOW-WE-WORK.md:…` citation in the candidate (these files are not in the sandbox). That includes the grep results in SPEC:25 (E5), the "11 re-read locations" in SPEC:11 and the "about 340 citations" claim in SPEC:285. I take them as stated and mark them UNVERIFIED.

Not applicable to this run: `--focus correctness` is not active, so no State Variable Registry is produced. The spec has no data pipeline whose output count differs from its input count (its P0-P4 phases are an ordered rollout), so Pipeline Dimensional Analysis does not trigger. `--re-review` and `--baseline` were not given, so there is no evidence block.

## Findings

Grade rule applied: a finding is blocking only when "an implementer who follows the stated text as written builds X, and X is wrong because Y" holds with no extra assumption. Otherwise it is Medium or minor.

### BLOCKING

**B-1 (MAJOR, blocking; Wiegers, Adzic): AC-0.4 requires a step that cannot pass in Phase 0.**
- Stated texts: SPEC:194 says the three P0 smoke runs must have "steps 1-3 and 5-7 pass; step 4 uses the command's existing report file, since the contract arrives in P1". Step 3 of the live check (SPEC:182) passes only if "its `--outcome` matches the contract's `status` under WC-5; its report path is the WC-4 contract path".
- An implementer who follows this builds a P0 gate that demands a WC-4 contract report path from `/sc:troubleshoot`. That command writes `REPORT.md` and has no contract until P2 (SPEC:91, SPEC:160), so the gate cannot pass. Step 4 was relaxed for this reason; step 3 was not. The adversarial run is also affected: its contract filename is not fixed until P1 (SPEC:83, SPEC:198).
- Consequence: the phase that exists "to close evidence gap 1.4 (1)" (SPEC:158) fails its own acceptance check, and SPEC:194 says a failure "reopens section 1".
- Recommendation: state that for P0 step 3 compares `--outcome` and `--report-path` with the command's existing report file (as step 4 already does). Priority High.

**B-2 (MAJOR, blocking; Wiegers, Fowler): WC-4's contract location contradicts the file-valued `--output` of several commands and of AC-2.2.**
- Stated texts: WC-4 (SPEC:62) writes `<output-dir>/return-contract.yaml`, where `<output-dir>` is "the directory the coordinator passed (`--output` / `--output-dir`)". Section 3 gives `--output <file>` to tdd (SPEC:90) and init-lite (SPEC:87); the spec-panel, explain and document rows (SPEC:107-108, SPEC:120) also say "add `--output`" or "explicit output" without saying whether it is a file or a directory.
- An implementer who follows WC-4 literally for tdd builds the path `<TDD-file>/return-contract.yaml`, which cannot exist beside the TDD file. AC-2.2 then runs exactly `/sc:tdd "auth" --unattended --output <file>` and requires a contract with `status: blocked` (SPEC:200). Step 4 of SPEC:183 runs `test -s <contract>` on a path the spec never defines for file-valued outputs.
- Consequence: the coordinator cannot know the report path "before dispatch" (WC-4's own requirement) for these commands, and AC-2.2 cannot pass as written.
- Recommendation: add one sentence to WC-4 that fixes the contract path when `--output` is a file (for example the file's parent directory, or a named sibling), or make the brief pass a separate directory flag. Priority High.

### Medium (warnings, `follow-up candidates`; never trigger a revision)

**M-1 (MAJOR label, graded Medium; Cockburn): `--unattended` is required in the brief for six commands that never get it.** SPEC:73 says the brief states "the exact command line including `--unattended`". SPEC:83-87 and SPEC:92 (adversarial, brainstorm, cleanup-audit, index-repo, init-lite, workflow) list no `--unattended` and no `## Unattended mode` section. SPEC:159 gives them only "small fixes", and tdd, troubleshoot, release-split and reflect get the flag only in P2. It needs a guess to say which reading an implementer picks (pass a flag the command does not define, or omit it), so it is Medium. Fix: say that 3.1 commands in P0/P1 are briefed without `--unattended`.

**M-2 (Medium; Fowler, Nygard): AC-C1 can fail on the spec's own required content.** AC-C1 (SPEC:172) greps `src/superclaude/core` and the commands for `orca (orchestration|worktree|terminal|agent)`. P0 adds `WORKER-CONTRACT.md` to core and "an Orca section" to `HOW-WE-WORK.md` (SPEC:158); SA-2 allows an Orca mention only "inside the contract file" (SPEC:147). Whether those files will contain the literal command text is a guess. Fix: scope the AC-C1 exclusion to the two files named in SA-2, or state that they use no literal command lines.

**M-3 (Medium; Wiegers): dangling labels.** `F-1` and `F-2` are cited at SPEC:76, 154, 159, 195 and 196 but are not defined anywhere in the candidate, and `ladder rung 2` (SPEC:261) is also undefined. The meaning can be inferred (load gets no section; pr-submit gets neither flag nor section under D3(a)), but the labels point at a document the spec does not include (probably `review/spec-panel.md`, README:23). Fix: inline the meaning or drop the labels.

**M-4 (Medium; Adzic): WC-4's "known before dispatch" fails for workflow.** The workflow contract path is `.dev/tasks/to-do/<id>/return-contract.yaml` (SPEC:92), and the id is generated at run time. SPEC:62 requires the report path to be known before dispatch. The worker can still report the path in `worker_done`, so this is not a wrong build. Fix: add an exception for commands that generate their own package id.

**M-5 (Medium; Fowler): D4 reaches phases the spec says need no decision.** SPEC:154 says "Phases 1-3 need no user decision", yet D4 (SPEC:244) affects auggie-review `--post-pr` and task `commit`/`push`, and both are P2 rows (SPEC:100, SPEC:121). Under D4(b) ("never") the `--post-pr` path in the auggie-review row would not exist. SPEC:225 does say phases 0-3 may proceed on the recommendations. Fix: say in the P2 row that it assumes D4(a).

**M-6 (Medium; Newman): command count depends on D3.** pr-submit is one of the 27 "needing a change" (SPEC:76, SPEC:114), but under the recommended D3(a) it gets no change and no flag (SPEC:154, SPEC:240). The count of changed commands under the recommended decisions is therefore 26. Fix: footnote the count.

**M-7 (Medium; Cockburn): the PR #329 evidence is described two ways.** E3 (SPEC:23) cites the return contract `invocation_method: "skill-direct"` as support for the decision, and INV-A:35 calls it "Proven as a direct Orca-worker skill call". SPEC:43 says the same run proves "the nested route, not the direct route" because the brief told workers to spawn an Agent-tool subagent (CAPS:156). The codegraph README itself is not in the sandbox, so I cannot say which reading is right (UNVERIFIED). The conclusion (Phase 0 smoke runs) holds either way. Fix: reword E3 so it does not imply direct-route proof.

**M-8 (Medium; Whittaker): sentinel and contradiction on the pr-submit top-level rule.** WC-7 (SPEC:65) cites `sk/sc-pr-submit-protocol/SKILL.md:37-39`; INV-A:14 cites the same lines, but CAPS:161 quotes the same rule at `~/.claude/skills/.../SKILL.md:47-49`. The two copies may differ, or one citation is stale. UNVERIFIED; no file to read. Fix: confirm the line numbers in the source copy.

**M-9 (Medium; Whittaker, Crispin-style completeness): WC-11 versus fixed output paths.** WC-11 (SPEC:69) says two workers in one worktree "must never write the same file". Rows SPEC:85-86 accept cleanup-audit's fixed output directory (`.claude-audit/…`) and index-repo's `PROJECT_INDEX.md`, and handle it only by "one audit per worktree at a time". The coordinator is the only party who can enforce that, and the contract (section 2.3) does not say so. Fix: add a line to 2.3 that the coordinator serializes workers that share a fixed path.

**M-10 (Medium; Nygard): refusal semantics.** Several rows say a flag is "refused" under `--unattended` (SPEC:102, SPEC:103, SPEC:108, SPEC:110, SPEC:114, SPEC:123), while WC-2 defines only three resolutions (default, caller flag, blocked). WC-4 says the contract is written on every outcome, but a refusal's `status` (`failed` or `blocked`) is not named. Fix: add one line mapping "refused" to `failed` with the reason.

### Minor notes

- N-1: SPEC:25, SPEC:11 and SPEC:285 state grep results and re-read counts that I cannot reproduce (UNVERIFIED).
- N-2: SPEC:79 calls the ten commands "ready today" yet tdd, troubleshoot, release-split and reflect each need a P2 gate change (SPEC:88-91); the label is the inventories' verdict rule (INV-A:104), not a claim that no change is needed.
- N-3: SPEC:63 maps a FAIL audit verdict to `--outcome succeeded`; this is deliberate and explained, but a coordinator reading only `worker_done` sees success. The first-sentence rule covers it.
- N-4: SPEC:260 says `--non-interactive` "reads as the opposite" of `--interactive`; a naming preference, not a defect.
- N-5: the UNVERIFIED list (SPEC:271-285) is honest and useful; items 1 and 12 are the ones with consequence for the plan.

## === REQUIREMENTS ANALYSIS ===
Strengths (Wiegers, Adzic, Cockburn): requirements WC-1 to WC-12 each name an owner and evidence (SPEC:57-70); the three-way gate resolution (SPEC:60) is testable; the acceptance checks in section 7 are concrete and mostly runnable. Weaknesses: B-1, B-2, M-1, M-3, M-4, M-10 above.

## === ARCHITECTURE ANALYSIS ===
Strengths (Fowler, Newman, Hohpe, Nygard): the decision (SPEC:13-17) is argued against a named alternative with five reasons (SPEC:31-37), and R1 matches CAPS:97-103. The boundary between coordinator, worker session and command is explicit (SPEC:55, SPEC:65-66). Weaknesses: M-2, M-5, M-6, M-9; the single shared contract file for all 27 commands is a sound design (one change point) but its path rule is the weak part (B-2).

## === ADVERSARIAL ANALYSIS (Whittaker) ===
- I can break this specification by **Divergence Attack**. The invariant at **WC-4 / SPEC:62** ("`<output-dir>` is the directory the coordinator passed") fails when **`--output` is a file**. Concrete attack: brief passes `/sc:tdd "auth" --unattended --output .dev/x/auth-tdd.md`; WC-4 yields `.dev/x/auth-tdd.md/return-contract.yaml`; before: no file, after: write fails or the TDD is shadowed; AC-2.2 step `test -s` cannot find a contract. Severity: MAJOR (B-2).
- I can break this specification by **Sequence Attack**. The invariant at **AC-0.4 / SPEC:194** fails when **step 3 runs before the contract exists**. Concrete attack: P0 runs `/sc:troubleshoot`; it writes `REPORT.md`, the worker reports it, and step 3 compares against a WC-4 contract path that does not exist, so the check fails before P1 starts. Severity: MAJOR (B-1).
- Zero/Empty, Sentinel Collision and Accumulation attacks found no stated-text contradiction. One near miss: `blocked_question` is "non-empty" in AC-2.2 (SPEC:200) but WC-4 does not say it is mandatory when `status: blocked` (SPEC:62 says "when blocked"); consistent enough, noted only.

## Guard Condition Boundary Table

Guards found: the 60 s readiness limit (WC-1), the 4-minute wait split (WC-10), the 5-minute heartbeat cadence, confidence below 0.70 (task row, SPEC:121), nesting depth 1 (R1, D5), and the `--outcome` mapping (WC-5). Classes left out are given a one-line reason.

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|-------|----------|-----------------|----------------|--------------|-------------------|--------|
| readiness limit 60 s | SPEC:59, CAPS:44-45 | Zero/Empty | no prompt at launch | pass | worker-start reaches `ready` | OK |
| readiness limit 60 s | SPEC:59 | Typical | 30 s fallback | pass (34 s observed) | passes (SPEC:59, `EVIDENCE.md:45` UNVERIFIED here) | OK |
| readiness limit 60 s | SPEC:59 | Maximum/Overflow | fallback above about 45 s | fail | worker-start fails again (SPEC:59) | OK |
| readiness limit 60 s | SPEC:59 | Legitimate Edge Case | `--timeout-ms` raised per start | pass | allowed (CAPS:45) | OK |
| wait split 4 min | SPEC:68 | Zero/Empty | wait of 0 | n/a | not stated; a zero wait never blocks, so the class cannot cause a stall | OK (reason given) |
| wait split 4 min | SPEC:68 | Typical | 60 s poll plus sleep | pass | heartbeat possible between waits | OK |
| wait split 4 min | SPEC:68 | Maximum/Overflow | single call above 5 min | fail | must be split into at most 4 min; AC-4.3 checks 240 s | OK |
| wait split 4 min | SPEC:68, SPEC:114 | Legitimate Edge Case | pr-submit poll script runtime unknown | unknown | left UNVERIFIED (SPEC:283) and tested by AC-4.3 | OK (documented) |
| `--outcome` mapping | SPEC:63 | Zero/Empty | no report file | n/a | `failed` | OK |
| `--outcome` mapping | SPEC:63 | Typical | status `succeeded` | true | `succeeded` | OK |
| `--outcome` mapping | SPEC:63 | Legitimate Edge Case | status `partial`, or audit verdict FAIL | true | `succeeded`, body states status | OK |
| `--outcome` mapping | SPEC:63 | Legitimate Edge Case | command refuses a flag (`--watch`, `--interactive`) | n/a | not specified (M-10) | GAP (Medium) |
| contract path (WC-4) | SPEC:62 | Typical | `--output <dir>` | true | `<dir>/return-contract.yaml` | OK |
| contract path (WC-4) | SPEC:62 | Legitimate Edge Case | `--output <file>` (tdd, init-lite) | n/a | not specified (B-2) | GAP (blocking) |
| contract path (WC-4) | SPEC:62, SPEC:92 | Legitimate Edge Case | generated package id (workflow) | n/a | path not known before dispatch (M-4) | GAP (Medium) |
| confidence gate | SPEC:121 | Zero/Empty | confidence 0 | below 0.70 | blocked | OK |
| confidence gate | SPEC:121 | Sentinel Value Match | exactly 0.70 | not below | not stated; the source text says "below 0.70" (`cmd/task.md:80`, UNVERIFIED), so 0.70 proceeds | OK (inferable) |
| nesting depth 1 | SPEC:33 | Typical | worker calls `worker-start` | refused | `nested_worker_depth_exceeded` (CAPS:99) | OK |
| nesting depth 1 | SPEC:33, SPEC:66 | Legitimate Edge Case | worker calls `task-create` | unknown | WC-8 forbids it either way; UNVERIFIED (CAPS:103, CAPS:180) | OK (documented) |

Classes not given a row for every guard: "One/Minimal" and "Maximum/Overflow" for the confidence gate and the depth guard cannot occur beyond the rows above (a score has no overflow; depth is a fixed setting).

FR-10 check: the table is complete (every guard listed, every omitted class has its reason). GAP rows: the `--outcome`/refusal row (Medium, M-10), contract path for file output (blocking, B-2), contract path for generated ids (Medium, M-4).

## Follow-up candidates

Medium: M-1, M-2, M-3, M-4, M-5, M-6, M-7, M-8, M-9, M-10. Minor: N-1 to N-5. The session that ran the review asks the user once whether to open an issue for these; none was created (this run is a labelled audit with no user prompt available).

Overrides: no brief clause was overridden. The brief asked for a whole-document first review per the FIRST-REVIEW prompt; that matches the command.

## Reviser brief

Blocking finding ids: B-1, B-2. Rules (restating `command.md` Review Loop bullet 6):
- Revise only text a blocking finding names (B-1: SPEC:182 and SPEC:194; B-2: SPEC:62 and, if needed, SPEC:200).
- Add no rule, mechanism or section that no blocking finding calls for; each added paragraph or table cites its finding id.
- Prefer deleting or narrowing to adding.
- Report the byte size of the candidate before and after, with the bytes added and deleted per finding id.
- Leave Medium and minor findings (M-1 to M-10, N-1 to N-5) alone.
- Return the candidate once and do not award yourself a PASS.

verdict: FAIL

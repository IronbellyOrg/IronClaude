review: 1 of 3

# Spec-panel audit: orca-worker-contract-spec.md

- command: `/sc:spec-panel @.dev/orca-command-refactor/specs/orca-worker-contract-spec.md --mode critique --focus requirements,architecture`
- label: whole-document audit of the final spec, a first review of the full document (no `--re-review`, no `--baseline`; neither was given, so no `baseline: missing` note applies)
- prompt followed: FIRST-REVIEW prompt in `~/.claude/rules/prompts/document_review_loop_prompts.md:27-32`
- candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md` (285 lines)
- candidate sha256: `520642eef4a21c603b07d310309b173eed3bbf84e2a66e5c9d61cdc65c86fe24`
- reviewer model: claude-sonnet-5-5
- format: critique buckets, with the standard-format quality scores in section 6
- citation key: `SPEC:N` = line N of the candidate; `INV-A:N`, `INV-B:N`, `CAPS:N` = line N of `.dev/orca-command-refactor/inventory/commands-a.md`, `commands-b.md`, `orca-capabilities.md`; `README:N` = `.dev/orca-command-refactor/README.md`. Every citation in this report was checked against those five files. A citation the candidate makes to any other file (`src/`, `.dev/evals/`, `.dev/codegraph-migration/`, `CLAUDE.md`, `HOW-WE-WORK.md`, `pyproject.toml`, Orca guides) cannot be checked in this sandbox and is UNVERIFIED unless an inventory line quotes it.

## 1. Coverage

Read in full: the README, the candidate, and the three inventories. Checked:
- The 10 / 27 / 6 split. SPEC:78-92 lists 10 ready, SPEC:97-125 lists 27 needs-change, SPEC:132-137 lists 6 coordinator-only. These match INV-A:73 (5 / 13 / 3) plus INV-B:278 (5 / 14 / 3). All 43 commands are placed once and the phase lists at SPEC:159-162 partition them with no loss (see section 5).
- Every `INV-*` and `CAPS:*` citation in the candidate's requirement, evidence, section 3 and section 4 tables, against the inventory line it points at. No wrong line was found. The candidate's wording of each carried verdict matches its inventory row.
- Internal consistency between the requirements (WC-1 to WC-12, SPEC:57-70), the per-command rows (SPEC:81-125), the standalone rules (SA-1 to SA-6, SPEC:146-151), the phases (SPEC:156-162) and the acceptance checks (SPEC:170-210).

Not covered, because the files are not in the sandbox: all `src/superclaude/...` line citations the inventories carry (the candidate's own re-read at SPEC:11 and its validator note at SPEC:285 cannot be reproduced here), `HOW-WE-WORK.md`, `install_core.py`, `pyproject.toml`, `CLAUDE.md`, `.dev/evals/...` and `.dev/codegraph-migration/...`. Behaviour of the commands themselves was not run.

Grading used: each finding was graded with the FIRST-REVIEW grading check (an implementer who follows the stated text builds X and X is wrong because Y). Blocking needs a sentence that holds with no further assumption. Missing requirements and guesses are Medium.

## 2. Panel summary (expert order per the command)

- Wiegers (requirements lead): the requirement set is mostly testable and well cited. One direct contradiction about which ready commands get a contract (B-1). Four requirements (WC-1, WC-3, WC-6, WC-12) have no phase deliverable or acceptance check (M-6).
- Adzic: the live check at SPEC:179-186 is a good concrete scenario. Happy-path and gate-trigger examples exist for most gates; cli-portify has no passable happy path (M-2).
- Cockburn: actors and goals are clear (coordinator plans, worker runs one command, person decides outward actions). The person-as-actor is thin for "refused" and "blocked then re-invoked" flows (M-4).
- Fowler (architecture lead): the decision "Orca on top, commands as units" (SPEC:16, rejected alternative SPEC:28-39) is well argued and consistent with INV-A:90 and CAPS:97-103. The contract interface is under-specified in three places: path derivation, status vocabulary, and the fresh-directory rule (M-3, M-5).
- Nygard: the failure paths for a stalled worker are covered (blocked contract, `ask`). The long-wait rule and stale-contract case are not (M-1, M-3).
- Whittaker: attacks in section 7.
- Newman: the contract has no version field and "keep their fields and add the missing ones" (SPEC:62) is untested against the existing contracts (M-5).
- Hohpe: the report-file hand-off is a pull model (coordinator opens the file, SPEC:62, SPEC:73), consistent with CAPS:79. No finding.
- Crispin, Gregory, Hightower: covered only through the acceptance-check findings (M-6, M-8); `--focus` did not include testing or compliance.

## 3. === REQUIREMENTS ANALYSIS ===

### B-1 (BLOCKING, MAJOR): which ready commands gain a contract and an `## Unattended mode` section is stated three incompatible ways

Expert: Wiegers (lead), Adzic. Priority: High. Quality impact: Consistency 8 to 6 if left.

Stated texts that disagree:
1. WC-4 (SPEC:62) says that in unattended mode the command writes a contract on every outcome, and names a path for each fixed-output command: "`<output-file>.return-contract.yaml`" for tdd and init-lite, "`.claude-audit/return-contract.yaml`" for cleanup-audit, "`PROJECT_INDEX.return-contract.yaml`" for index-repo.
2. SPEC:76 says only commands "whose row names an unattended-mode change in P1-P3" gain the section, and that "brainstorm and init-lite (no change)" do not. The init-lite row (SPEC:87) says small fix "None", and the cleanup-audit and index-repo rows (SPEC:85-86) name only a report-name or location fix. INV-A:55 confirms init-lite writes a markdown report and no contract.
3. SPEC:79 says the worker reports the named file "until Phase 1 adds the contract". P1 (SPEC:159) adds contracts only to the fixes for adversarial, cleanup-audit, index-repo. No phase gives init-lite a contract, so the "until" never ends for it.
4. AC-1.1 (SPEC:195) requires every command in 3.1-3.2 "whose row names a P1 change" to have a `## Unattended mode` section naming `return-contract.yaml`. The adversarial, cleanup-audit and index-repo rows each end in "(P1)" (SPEC:83, 85, 86), so the test sweeps them in, against SPEC:76 and the rows' "small fix" wording. AC-1.2 (SPEC:196) then runs each of them with `--unattended`, a flag that SPEC:76 says they do not gain.

An implementer who follows the rows and SPEC:76 builds init-lite, cleanup-audit and index-repo with no `--unattended` and no contract. That build is wrong because (a) WC-4 requires the contract at the paths it names, (b) the coordinator brief (SPEC:73) tells the worker to pass that contract path, and WC-5 (SPEC:63) sets `--outcome failed` when "no report exists", so a successful init-lite run is reported failed, and (c) AC-1.1 and AC-1.2 fail for the three P1-labelled commands.

Recommendation: state one rule. Either every ready command gets the section and its contract in the phase its row names (and the init-lite row, SPEC:76, SPEC:79 and the AC-1.1 exclusion list are changed), or WC-4 names a markdown-report fallback for init-lite and the three P1 fixes, and AC-1.1/AC-1.2 are narrowed to commands that gain the section. Prefer narrowing WC-4 and AC-1.1 (a deletion) over adding a new init-lite contract.

## 4. === ARCHITECTURE ANALYSIS ===

No blocking architecture finding. The Medium findings below are listed under follow-up candidates (section 8) with their evidence.

## 5. Quantity flow check (Pipeline Dimensional Analysis)

The heuristic's trigger (a data pipeline whose stage output count may differ from input count) is not met by this document: the phase plan is a partition, not a filter. A conservation check was still run, because three places state the totals.

```text
[43 commands in cmd/ (SPEC:76; INV-A:3 21 + INV-B:3 22)]
  --> [classification] --> 10 ready (SPEC:78) + 27 needs-change (SPEC:94) + 6 coordinator-only (SPEC:127) = 43  (conserved)
  ready 10   --> P1 fixes 3 (adversarial, cleanup-audit, index-repo; SPEC:159) + P2 gates 4 (reflect, release-split, tdd, troubleshoot; SPEC:160) + no change 3 (brainstorm, init-lite, workflow) = 10  (conserved)
  needs-change 27 --> P1 9 (analyze, build, business-panel, design, document, explain, index, test, load) + P2 11 + P3 4 (roadmap, validate-roadmap, validate-tests, save) + P4 3 (implement, post-release, pr-submit) = 27  (conserved)
  consumer note: under recommended D3(a) (SPEC:240) pr-submit is run by the coordinator, so the effective split becomes 26 / 7 while SPEC:76 keeps 27 / 6. Stated conditionally at SPEC:139; not a defect.
```

## 6. Quality assessment (0-10)

| Dimension | Score | Basis |
|---|---|---|
| Clarity | 8 | One decision, one contract, per-command rows. "fresh dir", "refused" and "precise component prompt" are undefined (M-4, M-7). |
| Completeness | 7 | Strong coverage of gates and outward actions. Gaps: nested gates in tasklist (M-1), long waits (M-3), traceability (M-6). |
| Testability | 7 | A concrete 7-step live check exists (SPEC:179-186). Four requirements have no check (M-6). |
| Consistency | 6 | One direct contradiction (B-1) plus smaller conflicts (M-5, M-8). |

## 7. Whittaker adversarial analysis (all five attacks applied to the stated invariants)

I can break this specification by **Sequence Attack**. The invariant at **WC-4 and WC-5 (SPEC:62-63)**, "the report is written on every outcome and `--outcome failed` follows when no report exists", fails when **a command with a fixed contract path is re-run after an earlier success and the second run dies before writing anything**. Concrete attack: run 1 of index-repo writes `PROJECT_INDEX.return-contract.yaml` with `status: succeeded`. Run 2 starts in a retry worker (WC-6, SPEC:64), is killed at startup, and writes nothing. State before: contract = succeeded (run 1). State after: contract = succeeded (stale). The worker or coordinator finds a report, so WC-5's "no report exists" branch does not fire and the failed run reads as succeeded. Nothing in SPEC:62-64 requires the contract to be removed or stamped at start. Severity: MAJOR (missing requirement), graded Medium by the grading check (M-1).

I can break this specification by **Sentinel Collision Attack**. The invariant at **SA-1 and D1(a) (SPEC:146, SPEC:228)**, "without `--unattended` every behaviour is today's", fails when **the literal text `--unattended` appears inside a quoted prompt argument** (for example `/sc:tdd "document the --unattended flag"`). The candidate defines the switch only as "the flag in the brief" and does not say it must be a standalone token outside quoted text. Concrete attack: a person's tdd topic contains the word; a prefix match turns on unattended mode and the topic-only clarification (SPEC:90) resolves as blocked. Severity: MINOR (inferrable, easy to fix in the contract file), recorded in the guard table and M-4.

I can break this specification by **Zero/Empty Attack**. The invariant at **WC-4 (SPEC:62)**, `blocked_question` is carried "when blocked", fails when **status is `blocked` and the question is empty**. AC-2.2 (SPEC:200) requires a non-empty question but WC-4 does not, so the stated requirement and its check disagree. Concrete attack: cli-portify gate 1 writes `status: blocked`, `blocked_question: ""`; the coordinator has nothing to relay to the person. Severity: MINOR (the AC catches it).

I can break this specification by **Divergence Attack**. The invariant at **WC-5 (SPEC:63)** fails when **a contract is `partial`**: the worker sends `succeeded`, Orca settles the Task `completed`, and dependent Tasks become startable (CAPS:34, CAPS:90 say a failed Task keeps dependents blocked). The candidate justifies this by "a partial run left a usable deliverable" (SPEC:263) but no command defines `partial`. Concrete attack: a cleanup run applies 3 of 9 auto-approved items and records `partial`; a dependent `/sc:test` Task is created ready. The coordinator is told to open the report first (SPEC:73), so this is a risk, not a wrong stated outcome. Severity: MAJOR to Medium (M-5).

I can break this specification by **Accumulation Attack**. The invariant at **WC-10 (SPEC:68)**, "a step that blocks a single tool call for longer than 5 minutes must be split into waits of at most 4 minutes", fails when **the blocking call is one Agent-tool fan-out or one foreground build/test run that cannot be split**. Concrete attack: cleanup-audit dispatches a wave of 7-8 concurrent agents (INV-A:42) and the session waits on one tool result for 12 minutes; no heartbeat can be sent. Severity: MAJOR to Medium (M-3).

## 8. Guard Condition Boundary Table

Guards were taken from the candidate's conditional rules. Classes left out are named with one line each below the table.

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|-------|----------|-----------------|----------------|--------------|-------------------|--------|
| `--unattended` switch | SPEC:51, SPEC:60, SPEC:146 | Zero/Empty | flag absent | false | Today's behaviour unchanged (SA-1, SPEC:146); no new file (SA-3, SPEC:148) | OK |
| `--unattended` switch | SPEC:62, SPEC:148, SPEC:99 | One/Minimal | flag present, no output flag (for example `/sc:analyze x --unattended`) | true | WC-4 derives the contract path from the output flag; SA-3 allows the file "when the caller passes the new output flag"; nothing says where the contract goes with neither a directory nor a file given | GAP |
| `--unattended` switch | SPEC:60, SPEC:90 | Typical | flag present, all required flags in the brief | true | Gate resolves per the row; contract written (WC-2, WC-4) | OK |
| `--unattended` switch | SPEC:103, SPEC:110, SPEC:123, SPEC:114 | Legitimate Edge Case | flag together with `--interactive` / `--watch` / `--monitor 1` | true | "refused" for cleanup, improve, test, pr-submit; the exit status and the contract content of a refusal are not stated. For adversarial, brainstorm, release-split "never `--interactive`" is a brief rule only (SPEC:83, 84, 89) | GAP |
| `--unattended` switch | SPEC:228 | Sentinel Value Match | the text `--unattended` inside a quoted prompt | unspecified | Token rule not stated in the candidate | GAP |
| contract status to outcome | SPEC:63 | Zero/Empty | no contract file | no report | `--outcome failed` (WC-5) | OK |
| contract status to outcome | SPEC:63 | Zero/Empty | file present but empty or not parseable | unspecified | not stated | GAP |
| contract status to outcome | SPEC:62-63 | One/Minimal | `status: partial` | true | `succeeded`, body says partial (WC-5, SPEC:263); meaning of `partial` per command not defined | GAP |
| contract status to outcome | SPEC:62, SPEC:183 | Sentinel Value Match | `status` value outside the four allowed (an existing contract's own vocabulary) | unspecified | Existing contracts "keep their fields" (SPEC:62) while 7.2 step 4 asserts the four values; existing vocabularies not shown in INV-A:35, INV-A:39, INV-B:112, INV-B:272 | GAP |
| contract status to outcome | SPEC:62, SPEC:200 | Legitimate Edge Case | `status: blocked`, empty `blocked_question` | true | AC-2.2 requires non-empty; WC-4 does not | GAP |
| WC-10 wait size | SPEC:68 | Zero/Empty | no long wait | false | no change | OK |
| WC-10 wait size | SPEC:68, SPEC:114 | Typical | poll plus sleep iteration under 4 min | false | worker heartbeats between iterations (pr-submit row) | OK |
| WC-10 wait size | SPEC:68, SPEC:114 | Legitimate Edge Case | iteration = 4 min wait plus poll-script runtime | unspecified | row asks to confirm runtime; runtime UNVERIFIED (SPEC:283, item 12) | GAP |
| WC-10 wait size | SPEC:68 | Maximum/Overflow | one unsplittable call over 5 min (Agent fan-out, build, test run) | true | splitting is stated only for cli-eval and pr-submit (SPEC:104, 114); build/test/cleanup-audit/tdd rows are silent | GAP |
| readiness fallback | SPEC:59 | Typical | 30 s fallback | true | start passes (34 s; CAPS:49) | OK |
| readiness fallback | SPEC:59 | Maximum/Overflow | fallback above about 45 s | false | start fails (CAPS:49); requirement says only "well inside" the 60 s limit, no number | GAP |
| nested depth | SPEC:66, SPEC:33 | Typical | worker calls `worker-start` at depth 1 | true | forbidden by WC-8; Orca refuses (CAPS:99) | OK |
| nested depth | SPEC:252 | Legitimate Edge Case | user raises depth (D5 b) | true | stated as breaking R1's protection | OK |
| task confidence | SPEC:121, INV-B:199 | Zero/Empty | confidence 0 | true | blocked | OK |
| task confidence | SPEC:121, INV-B:199 | Legitimate Edge Case | confidence exactly 0.70 | false | proceeds ("below 0.70" blocks) | OK |
| AC-2.4 counts | SPEC:202 | Maximum/Overflow | 30 or more reviews or comments on the PR | counts unchanged | `gh api ... --jq length` reads one page; a new post can leave the length at the page cap | GAP |

Left out, with reason: Maximum/Overflow for `--unattended`, depth and task confidence (no capacity exists for a boolean, a fixed limit or a score capped at 1.0); One/Minimal for the contract status, readiness, WC-10 and depth rows beyond those shown (they collapse into the rows given); Sentinel Value Match for WC-10, readiness, depth, confidence and AC-2.4 (no reserved value is defined for them).

FR-8/FR-9 grading: no GAP row names a wrong outcome an implementer produces from stated text with no further assumption, and none names a security, data-loss or safety-boundary risk. All GAP rows are Medium and appear under follow-up candidates.

## 9. Follow-up candidates (Medium and minor; none blocks)

Medium (warnings):

- **M-1 (Nygard, Whittaker).** Stale contract is read as current: fixed contract paths (`.claude-audit/return-contract.yaml`, `PROJECT_INDEX.return-contract.yaml`, SPEC:62) can hold an earlier run's `succeeded`, and no requirement removes or stamps the file at start. The same two commands also break WC-11 (SPEC:69, "two workers must never write the same file"); SPEC:85 answers with "one audit per worktree at a time", a coordinator-side rule that the brief duties (SPEC:73) never list. Recommend: one line in SPEC:73 (serialize fixed-path commands) and one in WC-4 (contract is replaced at start). Priority Medium.
- **M-2 (Adzic, Cockburn).** cli-portify (SPEC:105): all three approval gates "resolve as blocked" and the only added flag is `--resume <contract>`. The candidate never says that resuming counts as approving the gate it stopped at. AC-2.3 (SPEC:201) requires a happy-path run with `--outcome succeeded` for every P2 command; for cli-portify that run exists only if the resume is read as approval. INV-A:79 offered an auto-approve flag, which the candidate did not take. Recommend: one sentence stating the approval semantics, or an exclusion in AC-2.3. Priority Medium.
- **M-3 (Nygard).** WC-10 (SPEC:68) is applied to cli-eval and pr-submit only. A top-level session waiting on an Agent-tool result or a foreground build/test run cannot heartbeat (INV-A:42 shows 7-8 concurrent agents; test and build rows, SPEC:101, 123, name only a report path). Whether Orca uses heartbeat age is UNVERIFIED (CAPS:130, CAPS:182), so the consequence may be limited to coordinator doubt. Recommend: say that WC-10 binds only splittable waits and name how a fan-out wait is handled, or drop it from the requirement text. Priority Medium.
- **M-4 (Cockburn, Fowler).** Undefined terms that rows depend on: "fresh dir" (about 20 rows, from WC-6, SPEC:64) does not say whether the command creates a new subdirectory (which moves the contract off the path WC-4 gives) or refuses a non-empty directory (which breaks WC-3's re-invoke after `ask`, SPEC:61); "refused" has no exit status or contract content (guard table); the `--unattended` token rule is not stated; for flags the spec adds, such as `--output` on analyze (SPEC:99), it is not said whether the value is a file or a directory, which WC-4 needs. Recommend: define each in WORKER-CONTRACT.md in one line. Priority Medium.
- **M-5 (Newman, Fowler).** The status vocabulary `succeeded / partial / failed / blocked` (SPEC:262) is applied to contracts that already exist and "keep their fields" (SPEC:62). The existing status values of adversarial, brainstorm, reflect and workflow are not shown in the inventories (INV-A:35, INV-A:39, INV-B:112, INV-B:272), so 7.2 step 4 (SPEC:183) may fail for the "None"-change commands (workflow, brainstorm). UNVERIFIED. The contract has no version field, and WC-5 reads a "verdict" (SPEC:63) that is not in WC-4's field list. Recommend: check the four existing contracts and add a `contract_version` and `verdict` field to WC-4. Priority Medium.
- **M-6 (Wiegers, Crispin).** Traceability: WC-1 has "Launch setup" as owner (SPEC:59) but no phase, deliverable or Non-goal covers it; WC-3 (ask path), WC-6 (retry does not corrupt the first attempt) and WC-12 (`check` before `worker_done`, `consumer_fenced`) have no acceptance check in section 7. Recommend: a one-row traceability table WC-n to phase to check, with "not tested" stated where true. Priority Medium.
- **M-7 (Fowler, Wiegers).** tasklist row (SPEC:122) passes `--unattended` to Stage 10.5 reflect only. INV-B:211 shows Stage 9 also invokes `sc:task --compliance strict`, whose confidence and TFEP gates (SPEC:121) are not resolved there, and INV-B:209 says reflect's `needs_human_decision` items HALT, with no unattended resolution given. The row says the reflect fan-out sits "inside Claude Code's nesting limit, INV-A:14", while INV-B:210 and INV-B:220 mark nested spawning UNVERIFIED and note tdd avoids it. The spec's rule WC-2 (SPEC:60) covers a command's own gates, not gates of commands it calls. Recommend: one sentence that `--unattended` is passed to every nested `/sc:` call, and a statement of the HALT outcome. Priority Medium.
- **M-8 (Crispin).** Checks that conflict with other text. AC-C1 (SPEC:172) must print nothing across `src/superclaude/core` in every phase, but P0 adds an Orca section to HOW-WE-WORK.md and a contract file to core (SPEC:158), and SA-2 (SPEC:147) allows an Orca mention in the contract file; any wording that matches the grep pattern fails P0. AC-C5 (SPEC:176) forbids any removed line, while SA-4 (SPEC:149) allows new flags, which edit the existing Usage line. AC-0.4 (SPEC:194) takes the adversarial report path from a column that says "filename not fixed" (SPEC:83). AC-2.4 (SPEC:202) counts `gh api` list lengths, which read one page. tdd's "precise component prompt" (SPEC:90) has no test other than the one example at SPEC:200. Recommend: reword each pass condition so it can be met. Priority Medium.
- **M-9 (Wiegers).** D4 (SPEC:244) lists auggie-review `--post-pr` and task `commit`/`push` as affected by the user's answer, yet SPEC:154 says phases 1-3 need no user decision and P2 (SPEC:160) builds those flags. D4(b) "Never" would remove them. Recommend: state that P2 builds only the "off under `--unattended`" half and leaves the authorization flag to P4. Priority Medium.
- **M-10 (Wiegers).** Evidence that cannot be checked here: SPEC:11 and SPEC:285 report an independent re-read of about 340 citations; the sandbox has no copy of that check. E5's `grep` result (SPEC:25) and the command count 43 describe the repo on 2026-11-02. The session's own list of available `/sc:` skills also names `sc:graph`, `sc:impact` and `sc:issue`, and describes `sc:issue` as creating an Orca worktree; none of these appear in the inventories (INV-A:3, INV-B:3). UNVERIFIED, since the session list is not a workspace file. If it is accurate, E5 and the AC-C1 baseline (SPEC:172) are false for that command. Recommend: re-run the E5 grep and the command listing on the current branch before the plan is executed. Priority Medium.
- **M-11 (Wiegers).** WC-3 (SPEC:61) says "may instead ask the coordinator once" and AC-2.2 (SPEC:200) expects `worker_done --outcome failed` for every blocked gate; the two paths are not reconciled for a worker that asked and then received an answer. Priority Medium.

Minor notes (no action required):
- SPEC:76 states the counts 27 / 6, which change under the recommended D3(a); already conditional at SPEC:139.
- SPEC:263 and SPEC:262 decisions are well reasoned; they only need the vocabulary check in M-5.
- WC-12 (SPEC:70) says commands need no change, which matches CAPS:66-67.

Issue offer: this audit ran under a coordinator brief, so the question "open an issue for the follow-up candidates?" is left to the coordinator; no issue was created.

## 10. Reviser brief

Blocking finding ids: B-1.

Rules for the reviser (restated from the command, bullet 6 of the Review Loop): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id. Leave Medium and minor findings alone.

B-1 targets: SPEC:62 (WC-4 contract paths for init-lite, cleanup-audit, index-repo), SPEC:76, SPEC:79, SPEC:85-87, SPEC:195-196 (AC-1.1, AC-1.2). Make the rule for which ready commands gain a contract and a `## Unattended mode` section the same in all of these places.

Brief clauses overridden: none. The brief asked for a whole-document audit; it did not widen the scope past the document or regrade a minor finding.

verdict: FAIL

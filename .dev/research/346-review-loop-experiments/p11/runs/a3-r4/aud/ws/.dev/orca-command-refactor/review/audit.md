review: 1 of 3

# Spec-panel audit: orca-worker-contract-spec.md

Command: `/sc:spec-panel @.dev/orca-command-refactor/specs/orca-worker-contract-spec.md --mode critique --focus requirements,architecture` (labelled whole-document audit of the final spec; a first review of the full document).

| Header field | Value |
|---|---|
| candidate | `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md` (285 lines, 57873 bytes) |
| candidate sha256 | `92073bce9aa934458a66ff79344ce2e439141e3c08d2246944949c626f472a09` |
| baseline / prior | none given (`--re-review` and `--baseline` both absent); first review of the whole document, so no `baseline: missing` note applies |
| reviewer model actually used | `claude-sonnet-5-5` |
| prompt followed | FIRST-REVIEW prompt, `~/.claude/rules/prompts/document_review_loop_prompts.md:27-32` (read in full before reviewing; `~` = sandbox `home/`) |
| brief clauses overridden | none. The brief only narrows (output path, evidence list); it asks for no minimum finding count and no regrade of minor findings |
| improve step | not run. The brief assigns only this file, the candidate is not edited, and no revised specification is written |

Citation shorthand (every path is inside the sandbox workspace):
- `SPEC:N` = line N of `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`
- `README:N` = `.dev/orca-command-refactor/README.md`
- `INV-A:N`, `INV-B:N`, `CAPS:N` = `.dev/orca-command-refactor/inventory/commands-a.md`, `commands-b.md`, `orca-capabilities.md`
- `LOOP:N` = `~/.claude/rules/prompts/document_review_loop_prompts.md`
- Quotations from Orca guide output are cited only through the `CAPS:` line that quotes them. Any citation to a file that is not in the workspace is marked UNVERIFIED.

## What was covered
- All 285 lines of the spec, `README` in full, and all three inventories in full.
- Every `INV-A:N`, `INV-B:N` and `CAPS:N` citation in section 3, section 4, section 1.2/1.3 and the UNVERIFIED list was matched to its line. All matched: the 27 rows of section 3.2 and the 10 rows of section 3.1 point to the right inventory rows (for example `SPEC:99-125` against `INV-A:37-54` and `INV-B:31-51`). The command tally holds: 10 ready + 27 needing a change + 6 coordinator-only = 43 (`INV-A:73`, `INV-B:278`; `SPEC:76`), and the phase tally holds: P1 9 + P2 11 + P3 4 + P4 3 = 27 rows of section 3.2, plus 4 + 4 ready-command fixes in P1/P2, plus brainstorm and init-lite in no phase (see M-01).
- UNVERIFIED (not checkable in the sandbox; none is treated as a finding on its own): all `src/superclaude/...` path:line citations in sections 2 and 3 (`SPEC:11`), `CLAUDE.md:*` citations (`SPEC:52,147,150,162,175,192`), `pyproject.toml:38` (`SPEC:183`), `Makefile:68-74` (`SPEC:279`), `.dev/codegraph-migration/...` (`SPEC:23,43`), `EVIDENCE.md:*` except as quoted in `CAPS:49`, and the grep and fresh-agent check claims at `SPEC:25` and `SPEC:285`. The spec cites a prior finding id `F-01` at `SPEC:195`; no prior-findings file is in the sandbox, so this run is a first review.
- Panel order (fixed): Wiegers, Adzic, Cockburn, Fowler, Nygard, Whittaker, Newman, Hohpe, Crispin, Gregory, Hightower. Focus panels in play: requirements (Wiegers lead, Adzic, Cockburn) and architecture (Fowler lead, Newman, Hohpe, Nygard); Whittaker runs in every review; Crispin validates the guard table. Gregory and Hightower raised nothing beyond the items below.

## Grading summary

| Id | Section | Label | Grade | One line |
|---|---|---|---|---|
| A-01 | Requirements | MAJOR | **BLOCKING** | AC-2.2 demands `failed` + `status: blocked` from every P2 command, but 6 of 15 P2 gate resolutions are not "blocked" |
| A-02 | Requirements | MAJOR | **BLOCKING** | WC-4 contract path needs a coordinator-passed output directory; AC-1.2 runs commands with a flag the spec says they do not take |
| M-01 .. M-20 | both | MAJOR/MINOR | Medium | see `follow-up candidates` |
| N-01 .. N-05 | both | MINOR | note | see `follow-up candidates` |

Blocking findings open: 2 (A-01, A-02).

=== REQUIREMENTS ANALYSIS ===

### A-01 (blocking) Acceptance criterion AC-2.2 cannot pass for the P2 commands that do not resolve to "blocked"
- Expert: Wiegers (testability), Adzic (the scenario cannot be executed as written). Severity label: MAJOR. Priority: High. Quality impact: Testability -2, Consistency -1.
- Stated text A: WC-2 defines three gate resolutions (a) default, (b) caller flag, (c) blocked, and only (c) writes `status: blocked` (`SPEC:60`).
- Stated text B: AC-2.2 says, for "each P2 command", run an input that hits the gate and pass only if `worker_done --outcome failed` and the contract has `status: blocked` with a non-empty `blocked_question` (`SPEC:200`). P2 contains 15 commands (`SPEC:160`).
- Six of those 15 resolve their gate by (a) or (b), never by "blocked":
  - auggie-review: `--unattended` implies `--no-post-pr` and `--no-remediation-offer` (`SPEC:100`);
  - cleanup: apply the auto-allowed items, list the "Approval Required" items unapplied (`SPEC:103`);
  - improve: "as cleanup" (`SPEC:110`);
  - research: pins `--strategy planning`, so no gate exists (`SPEC:116`);
  - tasklist: passes `--unattended` to reflect (`SPEC:122`);
  - reflect: follows the headless auto-accept rule (`SPEC:88`).
- Grading sentence: An implementer who follows the stated rows builds cleanup that applies auto-fix items, lists the rest and reports `partial` or `succeeded` (WC-5, `SPEC:63`), and that build is wrong, because AC-2.2 (the phase check that gates P3 at `SPEC:154`) requires `failed` plus `blocked` from the same run, so the correct implementation fails the phase check, or the implementer is pushed to change the specified resolution to "blocked", which removes the listed behaviour.
- Recommendation: restrict AC-2.2 to the P2 commands whose row resolves as "blocked" (cli-eval, cli-portify, recommend, review-translation, spec-panel, task, release-split, tdd, troubleshoot), and give the other six their own pass condition (for example the report lists the deferred items and no outward action occurred, as AC-2.4 does for auggie-review).

### A-02 (blocking) The contract location rule and the acceptance checks that use it contradict the commands' own flag lists
- Expert: Wiegers (traceability), Cockburn (the coordinator's goal "know the report path before dispatch" is not achievable for these commands). Severity label: MAJOR. Priority: High. Quality impact: Testability -2, Completeness -2.
- Stated text A: WC-4 puts the contract at `<output-dir>/return-contract.yaml`, "the directory the coordinator passed (`--output` / `--output-dir`)", and says the path is known before dispatch (`SPEC:62`; same promise at `SPEC:73`).
- Stated text B: AC-1.2 runs "each P1 command" with `--unattended --output <dir>` (`SPEC:196`), and AC-1.1 defines the P1 commands as every command named in the P1 row (`SPEC:195`). The P1 row names the four fix-targets adversarial, cleanup-audit, index-repo and workflow (`SPEC:159`). Section 3.1 gives their briefs as: cleanup-audit `--pass <N>` with a fixed output directory (`SPEC:85`); index-repo "none" (`SPEC:86`); workflow `--handoff none` with its contract inside a generated package `.dev/tasks/to-do/<id>/` (`SPEC:92`; `INV-B:272`). None is given an `--output` directory flag, and the P1 fixes listed for them (state the location, name the final report, write the contract for pre-creation STOPs) add none (`SPEC:85,86,92`). Workflow's contract for a pre-creation STOP has no package directory at all, which is why the inventory records it as not written (`INV-B:272`).
- The same location rule is also unusable for commands whose `--output` is a file, not a directory: tdd and init-lite take `--output <file>` (`SPEC:87,90`), and AC-2.2's own example is `/sc:tdd "auth" --unattended --output <file>` (`SPEC:200`); and for research, whose file name is generated at run time with no flag (`SPEC:116`; `INV-B:132`).
- Grading sentence: An implementer who follows WC-4 and AC-1.2 builds `<output-dir>/return-contract.yaml` for workflow, index-repo and cleanup-audit, and that build is wrong because these commands receive no output-directory argument in the spec's own briefs, so AC-1.2 invokes flags the spec never adds and its step 4 (`test -s <contract>`, `SPEC:183`) has no path to test.
- Recommendation: state, per command, either the added directory flag or the exact contract path derivable from the brief (for example "workflow: the package directory is created first and the contract path is returned to the worker before any STOP"), and say what `<output-dir>` means when `--output` is a file. Remove `--output <dir>` from AC-1.2 for commands that do not take it.

## Medium and minor findings (requirements)

### M-01 Which commands get the WC-4 contract and the `## Unattended mode` section is not assigned for 6 commands (Medium; label MAJOR)
- Expert: Wiegers. Priority: Medium. The brief template says every brief includes `--unattended` (`SPEC:73`), P1 says every command in sections 3.1 and 3.2 accepts it (`SPEC:159`), and WC-4 says the contract is written "in unattended mode" (`SPEC:62`). Yet brainstorm and init-lite have "None" as their small fix and are in no phase (`SPEC:84,87`; `SPEC:159-162`), and troubleshoot, tdd and release-split get only a gate fix in P2 (`SPEC:89-91`), while troubleshoot writes a contract only under a caller flag (`INV-B:242`). AC-2.3 (`SPEC:201`) requires 7.2 step 4 (a contract) for these. An implementer must guess whether a contract is added. Recommendation: add one sentence saying which phase adds the contract for each of the six.

### M-02 P1 says gated commands accept `--unattended` before their gates are converted (Medium; label MAJOR)
- Expert: Cockburn, Nygard. `SPEC:159` has every 3.1/3.2 command accept the flag "(a no-op where a command has no gate)", but the gate conversions land in P2/P3/P4 (`SPEC:160-162`). Between phases auggie-review would accept `--unattended` and still post to GitHub by default (`SPEC:100`; WC-9 `SPEC:67`), and implement, pr-submit and post-release would accept it and still stop for a person (`SPEC:109,113,114`). The phase text "leaves standalone behaviour unchanged" (`SPEC:154`) is met, but the unattended promise of WC-2 is not. Two readings exist (flag only added together with its gate fix, or flag added in P1); the worse reading is plausible. Recommendation: say that a command refuses `--unattended` until its gate row is implemented.

### M-03 "Refused" has no defined outcome (Medium; label MAJOR)
- Expert: Adzic. Seven rows say a flag is "refused" under `--unattended`: `--mode socratic` (`SPEC:102`), `--interactive` (`SPEC:103,110,118`), `--format interactive` (`SPEC:108`), `--monitor 1` (`SPEC:114`), `--watch` (`SPEC:123`). WC-2 lists only three resolutions (`SPEC:60`) and "refused" is none of them; WC-4 requires a contract "on every outcome" (`SPEC:62`) but no status, message or exit behaviour is given. Recommendation: define "refused" as a contract with `status: failed` and a one-line reason, and name it in WC-2.

### M-04 A stale contract from an earlier attempt is read as the new attempt's result (Medium; label MAJOR)
- Expert: Whittaker (sequence attack, see W-2), Nygard. WC-5 sends `--outcome failed` only "when no report exists" (`SPEC:63`); WC-6 lets a retry resume in the same directory (`SPEC:64`); WC-4 writes the contract only at the end of a run (`SPEC:62`). A retry that crashes before writing leaves the first attempt's `status: succeeded` file, which the worker would report. Recommendation: the command removes or overwrites the contract at start (for example `status: running`), and WC-5 treats `running` as no report.

### M-05 Outward-action authorization has no channel for the commands that need it (Medium; label MAJOR)
- Expert: Nygard. WC-9 turns an outward default on "only through the command's own explicit flag written in the brief" (`SPEC:67`) and D4(a) says the coordinator "passes the command's explicit flag" (`SPEC:245`). The rows give no such flag for task `commit`/`push` and the committed TFEP report (`SPEC:121`) or for post-release VM, install, commit and PR (`SPEC:113`); only auggie-review has one (`--post-pr`, `SPEC:100`). The safe default (off) holds, so no wrong action follows, but D4(a) cannot be carried out for these commands. Recommendation: list the flag to be added, or say these stay coordinator-side under D4(a) too.

### M-06 After a worker ends `blocked`, the coordinator's next step is not specified, and Orca's circuit breaker is not a backstop (Medium; label MAJOR)
- Expert: Hohpe, Nygard. A blocked report maps to `--outcome failed` (`SPEC:63`); a failed Task keeps its dependents blocked until a `--retry-of` replacement completes it (`CAPS:90`), and "a worker's own `failed` report does not" count toward the three-failure circuit breaker (`CAPS:80`; spec relies on this at `SPEC:263`). Section 2.3 says only that the coordinator opens the report and releases the worker (`SPEC:73`). Nothing says "answer the question, then `worker-start --retry-of` with the answer as a flag", and nothing bounds repeated block-retry cycles. Recommendation: one sentence in 2.3 for the follow-up and a cap on cycles.

### M-07 cli-portify and the release-split custom scope have no input that carries the answer (Medium; label MAJOR)
- Expert: Cockburn. WC-3 says the session re-invokes "with the answer as a flag" (`SPEC:61`). cli-portify resolves its three approval gates only as "blocked", adding just `--resume <contract>` (`SPEC:105`); a resume that skips no gate re-hits the same approval. release-split `--r1-scope custom` also resolves as blocked with no flag for the scope (`SPEC:89`). Whether `resume_phase` implies approval is not said. Recommendation: name the approval or scope input for each, or say resume at phase N counts as approval of the earlier gate.

### M-08 Several requirements have no acceptance check (Medium; label MINOR)
- Expert: Wiegers, Crispin. WC-3 (ask and resume by id), WC-12 (`check` and `consumer_fenced`) and WC-1 have no AC in section 7.3; WC-10 is checked only for pr-submit (`SPEC:210`) although cli-eval is also assigned wait splitting (`SPEC:104`, P2); WC-11 is checked only for save (`SPEC:207`). `SPEC:68-70`. Recommendation: add a check, or mark them "design rule, not tested".

### M-09 The contract status vocabulary is fixed, but "keep their fields" for existing contracts is not reconciled (Medium; label MINOR)
- Expert: Newman, Wiegers. WC-4 says commands that already write a contract keep their fields and add the missing ones (`SPEC:62`); the Decisions table fixes the four-value status set (`SPEC:262`); 7.2 step 4 asserts it (`SPEC:183`). The workflow contract is a versioned format ("contract 1.1", `INV-B:272`); its existing status values are not in the sandbox (UNVERIFIED). If any existing status value differs, step 4 fails for that command. WC-4 also has no schema version field, so a coordinator cannot detect which layout it reads. Recommendation: say whether the four values are added as a new `unattended_status` field or replace the existing one, and add `contract_version`.

### M-10 WC-11 states an absolute that three rows break (Medium; label MINOR)
- Expert: Fowler. WC-11 says two workers in one worktree "must never write the same file" (`SPEC:69`), yet cleanup-audit keeps a fixed `.claude-audit/` (`SPEC:85`: "one audit per worktree at a time (WC-11)"), index-repo writes a fixed `PROJECT_INDEX.md` (`SPEC:86`), and init-lite without `--output` writes a fixed file (`SPEC:87`). The rows treat WC-11 as a coordinator scheduling rule, the requirement text treats it as a command rule. Recommendation: say WC-11 is met by the brief (serialise or pass a distinct path) for these three.

### M-11 Phase text says "Phases 1-3 need no user decision" while D1 and D4 touch them (Medium; label MINOR)
- Expert: Cockburn. `SPEC:154` versus D4 listing auggie-review and task, both P2 (`SPEC:244`; `SPEC:160`), and D1 (`SPEC:227`) which every phase depends on. `SPEC:225` says instead that phases 0-3 "can proceed on the recommendations". Recommendation: use the second wording in section 6.

### M-12 Scope statements conflict (Medium; label MINOR)
- Expert: Wiegers. `SPEC:16` says command changes are "limited to the worker contract" (unattended mode, report file, resume), and `SPEC:220` limits scope to defects that stop a command working as a worker. Section 3 also requires a new `--resume <contract>` flag for cli-portify (`SPEC:105`), tool additions for explain (`SPEC:108`), a frontmatter move whose effect is UNVERIFIED (`SPEC:102`), and a usage-line fix for load that does not stop a worker (`SPEC:112`; `INV-B:63`). SA-4 lists the exceptions (`SPEC:149`) but not the non-goal. Recommendation: reword `SPEC:16` and `SPEC:220` to point at SA-4.

### M-13 pr-submit's own "Will Not: run headless" and "attended" nature is not reconciled with `--unattended` (Medium; label MINOR)
- Expert: Cockburn. The inventory records `Will Not: run headless / imply a daemon` and an "attended poll loop" (`INV-B:90`, `INV-B:95`). The spec lists pr-submit among the 27 commands that get the flag (`SPEC:114,159`) and offers it as a worker under D3(b) (`SPEC:241`) without addressing that statement. Only D3(a) (recommended) avoids the issue. Recommendation: say D3(b) must also amend that Will Not, or drop pr-submit from the P1 flag list until D3 is answered.

### M-14 `README:31` is cited as a general authorization rule (Medium; label MINOR)
- Expert: Adzic. `README:31` is "No git commits, pushes, PRs or GitHub comments" in the "Rules for every worker" of this planning run (`README:29-31`). The spec uses it as evidence for WC-9 (`SPEC:67`) and for the claim that git operations need user authorization "in this repo" (`SPEC:133`). It supports only the planning-run rule. The repo-wide rule is in `CLAUDE.md` (UNVERIFIED here). Recommendation: cite the repo rule.

=== ARCHITECTURE ANALYSIS ===

### A-A1 The decision (Orca on top, commands unchanged inside) is supported by the evidence cited
- Expert: Fowler, Newman. Sections 1.2 and 1.3 check out against the capability inventory: R1 against `CAPS:97-103`, R2 against `CAPS:145-149`, R3 against `CAPS:76,148,150`, R4 against `CAPS:145`, R5 against `INV-A:90`/`INV-B:285-286`. The three evidence gaps in 1.4 are stated and carried into Phase 0 (`SPEC:43-45,158`). No finding.

### M-15 Section 1.4 (2) states as fact that a command's own prompt comes after readiness, against the launch mode in the capability inventory (Medium; label MINOR)
- Expert: Nygard. `SPEC:44` says a command's `AskUserQuestion` "comes after readiness, so it does not fail `worker-start`". For Claude the task, including the slash command, is passed on the command line (`CAPS:47`), so the command can start before Orca sees the input box; whether readiness is declared first is not established (`CAPS:49` shows only a shell-wrapper prompt failing, before Claude). This should be marked UNVERIFIED. The consequence is limited, because WC-2 removes the prompts in unattended mode and AC-0.4 runs live. Recommendation: mark UNVERIFIED and let AC-0.4 observe it.

### M-16 WC-10 uses three different thresholds (Medium; label MINOR)
- Expert: Nygard, Whittaker (see W-5). WC-10 triggers splitting for a call "longer than 5 minutes" and splits into waits of "at most 4 minutes" (`SPEC:68`); AC-4.3 fails any single call over 240 s (`SPEC:210`); the Decisions table keeps a 4-minute margin (`SPEC:266`). A 4.5-minute call needs no split under the trigger and fails the check. Recommendation: trigger at "longer than 4 minutes".

### M-17 AC-0.4 cannot be passed literally in Phase 0 (Medium; label MINOR)
- Expert: Crispin. AC-0.4 requires steps 1-3 and 5-7 of the 7.2 check and replaces only step 4 (`SPEC:194`). Step 3's pass condition compares `--outcome` with "the contract's status" and expects the report path to be "the WC-4 contract path" (`SPEC:182`); in P0 no command except adversarial/workflow/reflect/brainstorm has a contract, and adversarial's is at `<output>/adversarial/return-contract.yaml` (`INV-A:35`), not the WC-4 path. Recommendation: say step 3's contract comparison also uses the existing report file in P0.

### M-18 AC-C1 scans `src/superclaude/core` while SA-2 allows an Orca mention in the contract file (Medium; label MINOR)
- Expert: Crispin. SA-2 allows Orca to be named "as an example of a caller's question channel inside the contract file" (`SPEC:147`). The contract file lives under `src/superclaude/core` (`SPEC:52`), which AC-C1 greps with only `ccsession-tag` excluded (`SPEC:172`). A literal `orca orchestration ask` example in `WORKER-CONTRACT.md` makes AC-C1 fail in P0. The P0 plan also adds an Orca section to `HOW-WE-WORK.md`, also in `core` (`SPEC:158`). Recommendation: exclude the two files, or forbid the command form there.

### M-19 No contract schema version, and the shared document is the only place the rule is written (Medium; label MINOR)
- Expert: Newman. Folded into M-09 for the field; separately, every changed command file points to one shared `WORKER-CONTRACT.md` (`SPEC:52`), so the document is the interface. No rule says what happens when a command is installed from an older version than the contract file (installed files can drift). Recommendation: one sentence on version tolerance.

### M-20 After `partial`, the coordinator cannot tell a usable partial from an interrupted one by outcome alone (Medium; label MINOR)
- Expert: Hohpe. `partial` maps to `--outcome succeeded` (`SPEC:63,263`) and the coordinator must open the file to learn it. This is stated and accepted in the Decisions table (`SPEC:263`); the only gap is that 2.3 does not tell the coordinator to read `status` first (`SPEC:73`). Recommendation: one sentence in 2.3.

=== ADVERSARIAL ANALYSIS (Whittaker, review order 6) ===

Template used for each: "I can break this specification by [attack]. The invariant at [location] fails when [condition]. Concrete attack: [state trace]." Labels: CRITICAL (provably wrong), MAJOR (ambiguous or incomplete under attack), MINOR (inferrable). Grades follow the Review Loop, not the label.

- **W-1 Sentinel Collision Attack (label MAJOR, grade Medium).** I can break this specification by passing the sentinel as data. The invariant at D1(a) (`SPEC:228`) and `SPEC:51` ("the behaviour a command switches to when its caller passes `--unattended`") fails when the text `--unattended` appears inside a quoted topic. Concrete attack: before: a person runs `/sc:tdd "explain the --unattended flag"`; the spec does not say the flag is recognised only as a standalone token outside quoted text, so after: the command may enter unattended mode, drop its topic-only clarification and write a contract (`SPEC:90`), breaking SA-1 (`SPEC:146`). Recommendation: define the token rule in 2.1.
- **W-2 Sequence Attack (label MAJOR, grade Medium; same defect as M-04).** Attack: attempt 1 writes `status: succeeded`, the Task is reopened with `--retry-of` (`CAPS:116`), attempt 2 is killed before writing; state after: the old file remains and WC-5 reports `succeeded`.
- **W-3 Divergence Attack (label MAJOR, grade blocking; same defect as A-01).** The invariant at AC-2.2 (`SPEC:200`) fails at the boundary where a gate resolves as (a) or (b) instead of (c): cleanup with one "Approval Required" item ends `partial`, the check demands `failed`.
- **W-4 Zero/Empty Attack (label MAJOR, grade blocking; same defect as A-02).** The invariant at WC-4 "written on every outcome, including stops before any other output exists" (`SPEC:62`) fails when no output directory exists yet: workflow stopped before package creation (`INV-B:272`) has no `<output-dir>`.
- **W-5 Accumulation Attack (label MINOR, grade Medium; same defect as M-06 and M-16).** Each blocked run counts as the worker's own `failed`, which Orca does not count toward its three-failure breaker (`CAPS:80`); a coordinator that retries after every block has no bound. Separately, a 4.5-minute single call is within WC-10 and outside AC-4.3.
- **W-6 Divergence Attack on refused flags (label MINOR, grade Medium; same defect as M-03).** `--monitor 1` is refused (`SPEC:114`); `--monitor 0` and `--monitor 2` are not mentioned, and the inventory records the y/n gate only at ordinal 1 (`INV-B:89`), so the boundary values 0 and 2 are inferrable but unconfirmed.

## Guard Condition Boundary Table (Nygard builds, Crispin checks completeness, Whittaker attacks)

Guards were found in the spec: the `--unattended` switch, the status-to-outcome mapping, the wait thresholds, the 0.70 confidence rule, the refused flags, the outward-action default, and the retry rule. One row per input class that applies; omitted classes carry a one-line reason (FR-10).

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|-------|----------|-----------------|----------------|--------------|-------------------|--------|
| `unattended_switch` | `SPEC:51,146,228` | Zero/Empty | flag absent | false | standalone behaviour unchanged (SA-1) | OK |
| `unattended_switch` | `SPEC:128` | One/Minimal | flag passed to a section-4 coordinator-only command | n/a | "get no `--unattended` mode"; whether the command rejects, ignores or writes a contract is not stated | GAP |
| `unattended_switch` | `SPEC:73,84` | Typical | flag in a brief for a section-3 command | true | contract, no prompts (WC-2, WC-4) | OK |
| `unattended_switch` | `SPEC:51,90` | Sentinel Value Match | the text `--unattended` inside a quoted topic | ? | token rule not stated (W-1) | GAP |
| `unattended_switch` | `SPEC:103,110,118` | Legitimate Edge Case | `--unattended` together with `--interactive` | true | refused, outcome undefined (M-03) | GAP |
| `contract_status_to_outcome` | `SPEC:63` | Zero/Empty | no report file | true | `--outcome failed` | OK |
| `contract_status_to_outcome` | `SPEC:63` | Typical | `status: succeeded` | false | `--outcome succeeded` | OK |
| `contract_status_to_outcome` | `SPEC:63,263` | Sentinel Value Match | `status: partial` | false | `--outcome succeeded`, first body sentence says partial | OK |
| `contract_status_to_outcome` | `SPEC:63` | Legitimate Edge Case | report left by an earlier attempt, or `status` outside the four values, or `blocked` with empty `blocked_question` | ? | not stated (W-2, M-04, M-09) | GAP |
| `wait_split` (WC-10) | `SPEC:68,210` | Typical | single call under 4 minutes | false | no change | OK |
| `wait_split` (WC-10) | `SPEC:68,210` | Maximum/Overflow | single call of 4.5 minutes | false under WC-10, true under AC-4.3 | the two texts disagree (M-16) | GAP |
| `wait_split` (WC-10) | `SPEC:68` | Legitimate Edge Case | single call over 5 minutes | true | split into waits of at most 4 minutes | OK |
| `confidence_below_0.70` (task) | `SPEC:121` | One/Minimal | confidence `0.69` | true | resolves as blocked | OK |
| `confidence_below_0.70` (task) | `SPEC:121` | Sentinel Value Match | confidence exactly `0.70` | false | proceeds (inferred from "below 0.70"; the inventory states `< 0.70`, `INV-B:199`) | OK |
| `confidence_below_0.70` (task) | `SPEC:121` | Zero/Empty | confidence `0` or not computable | true / ? | `0` is below the threshold and resolves as blocked; "not computable" is not stated | GAP |
| `refused_flags` | `SPEC:102,103,108,110,114,118,123` | Typical | any refused flag with `--unattended` | true | "refused", no status or message defined (M-03) | GAP |
| `refused_flags` (`--monitor`) | `SPEC:114` | Legitimate Edge Case | `--monitor 0` and `--monitor 2` | false (inferred) | not mentioned; gate known only at 1 (`INV-B:89`) | GAP |
| `outward_default_off` (WC-9) | `SPEC:67,100` | Typical | auggie-review with no `--post-pr` | true | no posting | OK |
| `outward_default_off` (WC-9) | `SPEC:67,113,121` | Legitimate Edge Case | brief authorizes a task commit or a post-release install, but the command has no explicit flag | ? | channel not defined (M-05) | GAP |
| `retry_resume_or_fresh` (WC-6) | `SPEC:64` | Typical | command with a resume flag | true | resumes from on-disk state | OK |
| `retry_resume_or_fresh` (WC-6) | `SPEC:62,64` | Legitimate Edge Case | command with no resume flag and a fixed `--output` | false | "writes each run into a fresh output directory", which moves the contract path the coordinator was told | GAP |
| `circuit_breaker` (Orca) | `SPEC:263`; `CAPS:80` | Maximum/Overflow | third consecutive block-then-retry | false (worker's own `failed` is not counted) | no bound in the spec (M-06) | GAP |

Classes left out, with reason: Zero/Empty and Maximum/Overflow for `refused_flags` and `outward_default_off` (a flag is either present or absent; no collection or counter is involved); One/Minimal for `contract_status_to_outcome` and `wait_split` (no single-item case differs from typical); Sentinel Value Match for `wait_split` and `retry_resume_or_fresh` (no sentinel value exists); Typical for `circuit_breaker` (Orca-owned, spec only relies on it); Zero/Empty for `circuit_breaker` (no failures means no breaker action).

FR-8 / FR-9 grading of the GAP rows: `unattended_switch` sentinel and `contract_status_to_outcome` edge are Medium (they need a guess about intent: W-1, M-04); `wait_split` maximum is Medium (M-16); `refused_flags` is Medium (M-03); `outward_default_off` edge is Medium (the safe default holds); `retry_resume_or_fresh` edge is Medium (M-04, M-06 area); `confidence` not computable and `--monitor 0/2` are minor. The two blocking findings come from the acceptance criteria (A-01, A-02), not from the table.

## Other mandatory artifacts and heuristics
- State Variable Registry: not produced (`--focus correctness` not requested). Advisory only: the spec has numeric thresholds (0.70, 5 minutes, 4 minutes, 60 s, depth 1), a retry counter and a status state machine, so `--focus correctness` would be worth a later run.
- Pipeline Dimensional Analysis: not triggered. The spec describes no multi-stage data flow whose item count changes (its Tasks map one to one to workers and one to one to a `worker_done`, `SPEC:63`; the only counts are the command tallies, which were checked and conserve: 43 = 10 + 27 + 6). No Quantity Flow Diagram is produced.
- Downstream propagation: the GAP rows above are the priority invariant candidates for `sc:adversarial` AD-1 if the coordinator chooses to run it.

## Follow-up candidates (Medium and minor; none triggers a revision or fails this review)

Medium (warnings): M-01 contract assignment for six commands; M-02 flag accepted before its gate is converted; M-03 "refused" outcome undefined; M-04 stale contract on retry; M-05 no authorization flag for outward actions; M-06 coordinator follow-up after `blocked` and no bound on cycles; M-07 cli-portify and release-split custom scope lack an answer input; M-08 missing acceptance checks (WC-1, WC-3, WC-10 for cli-eval, WC-11, WC-12); M-09 status vocabulary and contract version vs existing contracts; M-10 WC-11 absolute vs fixed output paths; M-11 "Phases 1-3 need no user decision" vs D1/D4; M-12 conflicting scope statements; M-13 pr-submit "run headless" Will Not not reconciled; M-14 `README:31` cited as a general rule; M-15 section 1.4 (2) stated as fact against `CAPS:47`; M-16 WC-10 thresholds; M-17 AC-0.4 step 3 in Phase 0; M-18 AC-C1 scope vs SA-2; M-19 contract version tolerance; M-20 `partial` reading order in 2.3; W-1 token rule for `--unattended` in quoted text.

Minor notes:
- N-01 `SPEC:11` still says every other section-3 line is "carried from the inventories without a second read", while `SPEC:285` reports a later fresh-agent check of about 340 citations; the header was not updated.
- N-02 `SPEC:252` calls R1 a "protection against runaway fan-out"; R1 (`SPEC:33`) is a refusal rule, and the protection language is the Orca setting's (`CAPS:99`).
- N-03 AC-C1 and AC-C4 are written with `\|` escapes for table rendering (`SPEC:172,175`); copied raw into a shell, AC-C1's alternation becomes literal pipes and prints nothing (a vacuous pass). AC-C4 also passes when nothing is staged.
- N-04 7.2 steps 2 and 3 run a `worker-show` poll at least every 5 minutes while step 3 is a blocking `check --wait` with a 900 s timeout (`SPEC:181-182`); the interleaving is not described.
- N-05 `load` is told to accept `--unattended` in P1 (`SPEC:159`) but is excluded from the AC-1.1 assertion and has no `## Unattended mode` section (`SPEC:112,195`).

Issue offer: the session that ran this review has no user channel in this sandbox run, so the once-per-loop question about opening an issue for the Medium and minor findings was not asked and no issue was created. The list above is the record.

## Reviser brief
Blocking finding ids: A-01, A-02. Rules for the reviser (restated from the Review Loop, because the reviser reads this report and not the command): revise only text a blocking finding names; add no rule, mechanism or section that no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, and the bytes added and deleted per finding id; leave Medium and minor findings alone, including the follow-up candidates above; do not award yourself a PASS.
- A-01: repair `SPEC:200` (AC-2.2) so that it applies only to P2 commands whose gate row resolves as "blocked", and give the other P2 commands (auggie-review, cleanup, improve, research, tasklist, reflect) a pass condition that matches their row.
- A-02: repair the contract-location text in `SPEC:62` (WC-4) and the checks that use it (`SPEC:196` AC-1.2, `SPEC:200` AC-2.2's `--output <file>` example, 7.2 step 4 at `SPEC:183`) so that each command's contract path is derivable from its stated brief.

verdict: FAIL

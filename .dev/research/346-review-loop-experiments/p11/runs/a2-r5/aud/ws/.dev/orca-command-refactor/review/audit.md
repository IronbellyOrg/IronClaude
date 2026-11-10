review: 1 of 3

# Spec-panel audit: orca-worker-contract-spec.md (labelled whole-document first review)

- command: `/sc:spec-panel @.dev/orca-command-refactor/specs/orca-worker-contract-spec.md --mode critique --focus requirements,architecture`
- candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`, 285 lines
- candidate sha256: `7cfc46955e89212267b7b42612208b7b453942bd61bda42b47e3e96f605b89ff`
- baseline / prior report: not provided. This is a first review of the full document, so the Review Loop first-review default applies.
- reviewer model actually used: claude-sonnet-5-5
- prompt followed: FIRST-REVIEW prompt, `~/.claude/rules/prompts/document_review_loop_prompts.md` (read in full)
- brief clauses overridden: none
- citation shorthand: `SPEC:N` = line N of the candidate. `INV-A:N`, `INV-B:N` and `CAPS:N` = lines of `.dev/orca-command-refactor/inventory/commands-a.md`, `commands-b.md` and `orca-capabilities.md`. `README:N` = `.dev/orca-command-refactor/README.md`.
- coverage:
  - I read all 285 candidate lines, the README, the three inventories (every line) and the command and prompt files.
  - I checked every `INV-A`, `INV-B` and `CAPS` citation in the candidate for range (none out of range) and spot-checked the content of about 60 of them against the cited line. All matched, except where a finding below says otherwise.
  - UNVERIFIED: every citation to a file outside the workspace (`cmd/`, `sk/`, `ag/`, `CLAUDE.md`, `HOW-WE-WORK.md`, `install_core.py`, `Makefile`, `pyproject.toml`, `EVIDENCE.md`, the codegraph `README.md` and `return-contract.yaml`, the `orca-ide` guides and the Orca JS files). I could check these only as quoted by the inventories.
  - Not checked: the live repo, git history and the actual command files. The candidate's grep and `ls` results (E5, `tests/sc-task/`) are UNVERIFIED.

## Panel (fixed review order; focus: requirements + architecture; Whittaker is always active)

| # | Expert | Lens applied | Result |
|---|---|---|---|
| 1 | Wiegers | testability and traceability of WC-1..WC-12, SA-1..SA-6 to AC checks | F-1 (blocking); F-8, F-9, F-10 |
| 2 | Adzic | examples versus the rows (brainstorm, init-lite, load, cli-portify, tasklist) | F-1, F-5 |
| 3 | Cockburn | actors: person, coordinator, worker session, command | F-2 |
| 4 | Fowler | interface and boundary: `--unattended`, `--contract-dir`, contract file; count flow | F-1, F-2, F-4, F-7 |
| 5 | Nygard | failure modes: blocked with no answer channel, ask loop, retry, heartbeat | F-5, F-6, F-12 |
| 6 | Whittaker | five attacks (see Adversarial Analysis) | F-1, F-3, F-4, F-6, F-10 |
| 7 | Newman | evolution and mirrors: the P1 flag before P2 gates; the plugin mirror (UNVERIFIED #8) | F-3 |
| 8 | Hohpe | message flow: `ask`, `check`, `worker_done`, `escalation` | F-5, F-12 |
| 9 | Crispin | acceptance checks per requirement | F-8, F-9 |
| 10 | Gregory | shared understanding: undefined ids (B-1, B-2), overloaded word "contract" | M-1, M-6 |
| 11 | Hightower | operations: heartbeat cadence, long waits, AC-C1 baseline | F-6, F-11 |

## Grading rule applied (Review Loop bullet 2 and FIRST-REVIEW grading check)

A finding is blocking only when this sentence holds with no further assumption: "An implementer who follows the stated text as written builds X, and X is wrong because Y." Two stated texts that contradict each other, a stated text that breaks a security or safety boundary, or a stated text that an acceptance criterion cannot pass all qualify. A finding that needs a guess about which of two allowed readings the implementer picks, or that is a requirement the document never states, is Medium and goes under follow-up candidates, even when its label is MAJOR. Minor findings are notes.

Result: 1 blocking finding (F-1, MAJOR). 12 Medium findings (F-2 to F-13). 8 minor notes (M-1 to M-8).

## Guard Condition Boundary Table (Nygard builds, Crispin checks completeness, Whittaker attacks the entries)

Trigger met: the candidate contains switches, thresholds and sentinel comparisons. The table is complete for the guards below. Classes left out are named in the "Classes left out" list under the table. The table was completed before the synthesis sections.

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|-------|----------|-----------------|----------------|--------------|-------------------|--------|
| `--unattended` switch | SPEC:51, SPEC:60 (WC-2), SPEC:228 (D1) | Zero/Empty | flag absent | false | today's behaviour unchanged (SA-1, SPEC:146) | OK |
| `--unattended` switch | SPEC:51, SPEC:228 | One/Minimal | standalone token present | true | unattended mode (D1 option a) | OK |
| `--unattended` switch | SPEC:228 (D1 a) | Sentinel Value Match | the token `--unattended` appears inside a quoted free-text argument (tdd/troubleshoot/research topic or symptom text) | ambiguous | D1 says "explicit flag in the brief" and never says whether the token is parsed inside quoted text | GAP, see F-10 |
| `--unattended` switch | SPEC:60, SPEC:100, SPEC:102, SPEC:103, SPEC:110, SPEC:114, SPEC:118, SPEC:123 | Legitimate Edge Case | `--unattended` together with `--interactive`, `--mode socratic`, `--format interactive`, `--watch` or `--monitor 1` | true | rows say "refused", but not what a refusal writes (contract `status`, `--outcome`, exit) | GAP, see F-4 |
| `--contract-dir` | SPEC:62 (WC-4, B-1) | Zero/Empty | flag absent and `--output` is file-valued, absent or generated | true | "the brief must pass" it; what the command does when the brief did not is not stated, so a `blocked` report has no known place | GAP, see F-4 |
| `--contract-dir` | SPEC:62, SPEC:73 | One/Minimal | flag absent and `--output` is a directory | true | that directory is the contract directory | OK |
| `--contract-dir` | SPEC:62, SPEC:64 (WC-6) | Typical | writable directory the brief passes | true | `<dir>/return-contract.yaml` written on every outcome | OK |
| `--contract-dir` | SPEC:62, SPEC:64 | Legitimate Edge Case | directory reused by a `--retry-of` worker (holds the first attempt's contract), missing, unwritable, or inside `.git/` | true | not stated; WC-6 forbids corrupting the first attempt's output but does not say where the retry's contract goes | GAP, see F-4 |
| contract `status` to `--outcome` mapping | SPEC:63 (WC-5) | Zero/Empty | report file exists but is empty or unparsable | n/a | WC-5 covers only "no report exists" (gives `--outcome failed`) | GAP, see F-10 |
| contract `status` to `--outcome` mapping | SPEC:63, SPEC:263 | Typical | `succeeded`, `partial` | true | `--outcome succeeded` | OK |
| contract `status` to `--outcome` mapping | SPEC:63 | Legitimate Edge Case | `failed`, `blocked`, audit verdict FAIL | true | `failed`, `failed`, `succeeded` respectively | OK |
| contract `status` to `--outcome` mapping | SPEC:62, SPEC:63, SPEC:183 | Sentinel Value Match | an existing contract (workflow, reflect, adversarial, brainstorm) whose `status` value is outside the four-value set, or a pre-P1 report with no `status` at all (REPORT.md, the TDD file, SPEC:194) | n/a | WC-4 says "keep their fields"; AC step 4 asserts `status` is in the four-value set; AC-0.4 says "WC-5 applied to that report" with no `status` to apply it to | GAP, see F-10 |
| WC-10 wait size | SPEC:68 (WC-10), SPEC:210 (AC-4.3), SPEC:114 | Typical | single tool call under 4 minutes | false | no split needed | OK |
| WC-10 wait size | SPEC:68, SPEC:210 | Maximum/Overflow | single tool call between 4 and 5 minutes (for example 280 s) | false | WC-10 splits only calls "longer than 5 minutes"; AC-4.3 fails any call over 240 s; the pr-submit row says 4 minutes | GAP, see F-6 |
| WC-10 wait size | SPEC:68 | Sentinel Value Match | exactly 5 minutes, equal to the heartbeat cadence | false | "longer than 5 minutes" is not met, so no split, but the heartbeat is due | GAP, see F-6 |
| `ask` timeout (WC-3) | SPEC:61 | One/Minimal | one timeout | true | resume the same message ID | OK |
| `ask` timeout (WC-3) | SPEC:61 | Maximum/Overflow | repeated timeouts, or the coordinator is gone | true | no cap, no escalation, no `blocked` fallback, and no worker_done path | GAP, see F-12 |
| task confidence guard | SPEC:121 | Legitimate Edge Case | confidence 0.70 and 0.69 | false / true | "below 0.70 resolves as blocked": 0.69 blocks, 0.70 proceeds | OK |
| P1 flag acceptance (phase guard) | SPEC:159, SPEC:160, SPEC:162 | Legitimate Edge Case | command with a gate (auggie-review, cleanup, cli-eval, cli-portify, post-release, pr-submit) between P1 and its gate phase | true | P1 says "accepted ... (a no-op where a command has no gate)"; behaviour for a gated command before its phase is not stated | GAP, see F-3 |
| AC-1.1 universal assertion | SPEC:195, SPEC:84, SPEC:87, SPEC:112 | Legitimate Edge Case | commands whose own row says no change (brainstorm, init-lite) or no contract (load) | true | AC-1.1 requires a section naming `return-contract.yaml` in all of them | GAP, see F-1 |
| readiness fallback (WC-1) | SPEC:59 | Typical | 30 s fallback | false | passes (`EVIDENCE.md:45` via `CAPS:49`) | OK |
| readiness fallback (WC-1) | SPEC:59 | Maximum/Overflow | fallback near or over the limit | true | text says "well inside" with no number; its evidence of 45 s was measured against a 45 s limit, not the 60 s default | GAP, see M-5 |
| nesting depth | SPEC:33 (R1), SPEC:66 (WC-8) | Zero/Empty | invalid or zero setting | true | falls back to 1 (`CAPS:100`); WC-8 holds at any depth | OK |

Classes left out, with the reason:
- One/Minimal and Maximum for `--unattended`: it is a boolean.
- Maximum for `--contract-dir`: a path has no capacity bound that matters here.
- Zero/Empty for WC-10: a zero-length wait needs no split.
- Zero/Empty for the task confidence guard: an undetermined confidence is not described by the spec or by INV-B:45.

GAP entries propagate as priority invariant candidates to `sc:adversarial` AD-1. They are GAP-1 `--unattended` in quoted text, GAP-2 refusal output, GAP-3 missing `--contract-dir`, GAP-4 retry contract dir, GAP-5 empty report, GAP-6 foreign `status`, GAP-7 the 4 to 5 minute call, GAP-8 the exact 5 minute call, GAP-9 ask loop, GAP-10 P1 gated flag, GAP-11 AC-1.1 universal, GAP-12 readiness number. FR-8 and FR-9 grading: only GAP-11 is blocking (F-1). The rest are Medium or minor.

## Quantity Flow Diagram (Pipeline Dimensional Analysis, Fowler counts, Whittaker attacks the divergence points)

Trigger: the candidate describes a classify, then assign-to-phase, then check flow with counts that change at each stage. Fowler lists each stage's count. Whittaker's consistency check found one mismatch, F-1.

```text
[Source: 43 commands = INV-A 21 + INV-B 22 (SPEC:76)]
   --> [Classify: 10 ready (SPEC:78-92) + 27 needs-change (SPEC:94-125) + 6 coordinator-only (SPEC:127-137) = 43]   (verified: INV-A:73 = 5/13/3, INV-B:278 = 5/14/3)
        |
        +--> [Section 4: 6 coordinator-only; no --unattended; AC-1.1 asserts 0 sections]   consistent
        |
        v
   [Workers-capable: 37]
        |
        +--> [P1 generic clause (SPEC:159): flag accepted by "every command in 3.1 and 3.2" = 37]
        |        |
        |        +--> [AC-1.1 (SPEC:195) expects 37 commands with an "Unattended mode" section naming return-contract.yaml]
        |        +--> [AC-1.2 (SPEC:196) 7.2 live check, step 4 `test -s <contract>`, on "each P1 command"]
        |
        +--> [Per-phase command lists: P1 13 + P2 15 + P3 4 + P4 3 = 35 named; brainstorm and init-lite unnamed]
        +--> [Rows that change a command: 35 (3.1 "Small fix" is "None" for brainstorm and init-lite, SPEC:84, SPEC:87)]
        +--> [Rows that give a contract: 36 of 37 (load: "none (see note)", SPEC:112)]   <-- MISMATCH: consumer AC-1.1 expects 37
```

Divergence points: 37 expected at AC-1.1 versus 35 changed commands (brainstorm, init-lite) versus 36 contract-bearing commands (load). Every other count conserves. The concrete scenario is F-1.

## === REQUIREMENTS ANALYSIS ===

### F-1 [blocking] MAJOR, High priority. Expert: Wiegers, Adzic, Whittaker (divergence attack), Fowler (count flow)
Issue: AC-1.1 asserts a universal that three rows of the same document contradict.

Quotes:
- SPEC:195 (AC-1.1): "every command in sections 3.1-3.2 has a `## Unattended mode` section naming `return-contract.yaml` and `~/.claude/WORKER-CONTRACT.md`"
- SPEC:196 (AC-1.2): "7.2 live check on each P1 command with `--unattended --contract-dir <dir>`"
- SPEC:183 (7.2 step 4): requires `test -s <contract>`
- SPEC:159 (P1): the flag is "accepted by every command in sections 3.1 and 3.2"

Contradicting texts:
- SPEC:79: "The only command changes are the small fixes in the last column."
- SPEC:84: brainstorm "Small fix: None".
- SPEC:87: init-lite "Small fix: None".
- SPEC:112: load has "Report: none (see note)", "Resume: n/a" and "use it as a step inside another worker's brief, not as its own Task". SPEC:265 gives the reason: "a report file would be an unrequested addition."

Grading sentence: An implementer who follows SPEC:79 and the brainstorm, init-lite and load rows leaves those three command files without an `## Unattended mode` section and gives load no contract, and that is wrong because the P1 gate AC-1.1 requires the section, naming `return-contract.yaml`, in every 3.1 and 3.2 command, and AC-1.2 step 4 requires a contract file for load. The implementer cannot satisfy both texts. If the implementer instead adds the sections to pass AC-1.1, load gets a contract that its own row and the Decisions table (SPEC:265) say must not exist.

Why blocking: two stated texts contradict, and the P1 acceptance criterion cannot pass if the rows are followed.

Recommendation (rationale: narrowing is cheaper than adding): restrict AC-1.1, AC-1.2 and the P1 generic clause to the commands whose row changes them. Alternatively, change the three rows to say what P1 does to them.

Quality impact: Testability 6 to 8, Consistency 6 to 8.

## === ARCHITECTURE ANALYSIS ===

No blocking architecture finding. The decision itself (Orca on top, commands as units of work, SPEC:13-39) holds against the evidence: I found no passage in the candidate or the inventories that contradicts it, and the candidate states its three evidence gaps itself (SPEC:41-45).

## Follow-up candidates (Medium findings; none triggers a revision, none appears in the Reviser brief)

Each Medium finding names the guess or the missing requirement that keeps it from being blocking.

### Requirements (Wiegers, Adzic, Cockburn, Crispin, Gregory)

- **F-4 [Medium; label MAJOR] Unspecified behaviour at the `--unattended` and `--contract-dir` edges** (GAP-2, GAP-3, GAP-4; SPEC:62, SPEC:73, SPEC:228).
  - What is open: what a "refused" flag writes (rows at SPEC:100, 102, 103, 110, 114, 118, 123), what the command does when `--contract-dir` is missing, and where a retry's contract goes. SA-3 (SPEC:148) says the contract is written "only in unattended mode or when the caller passes the new output flag". WC-4 (SPEC:62) says "In unattended mode". A standalone run with only the new `--output` writes a contract under SA-3 and none under WC-4.
  - Why Medium: the document never states the missing rule, and the SA-3 versus WC-4 conflict needs a guess about which reading the implementer picks. AC-1.3 (SPEC:197) tests only the no-flag case.
  - Recommendation: one sentence for each of the four cases: refusal gives `blocked` with the refused flag as `blocked_question`; a missing `--contract-dir` falls back to the output directory or the current directory; a retry gets a fresh directory; SA-3 follows WC-4.

- **F-5 [Medium; label MAJOR] A `blocked` gate has no stated answer channel for several rows** (SPEC:61, SPEC:105, SPEC:109, SPEC:114, SPEC:121).
  - WC-3 says the worker asks the coordinator and then re-invokes "with the answer as a flag". The cli-portify row (SPEC:105) lists three approval gates that resolve as `blocked`, and a `--resume <contract>` flag that "uses the existing `resume_phase`/`resume_substep` fields". It names no approval flag. A resume that re-enters at the gate blocks again forever, and a resume that skips the gate turns "resume" into silent approval.
  - The task TFEP review, the pr-submit HALTs and the cli-eval confirmation have the same shape, with no flag defined.
  - Why Medium: this needs a guess about which of two readings the implementer picks (loop or silent approval); the document never states the approval input.
  - Recommendation: for each such gate, name the flag the answer comes back as, or say the gate always ends `blocked` and a person finishes the work.

- **F-6 [Medium; label MAJOR] WC-10 and AC-4.3 disagree, and the pr-submit loop structure is asserted against the inventory** (GAP-7, GAP-8; SPEC:68, SPEC:114, SPEC:210).
  - WC-10 splits only calls "longer than 5 minutes" into waits of at most 4 minutes. AC-4.3 and the pr-submit row use 4 minutes. A conforming 280 s call passes WC-10 and fails AC-4.3. A call of exactly 5 minutes is as long as the heartbeat cadence.
  - SPEC:68 and SPEC:114 say pr-submit's 600 s is a cumulative budget over "one foreground poll, then a sleep" iterations. INV-B:95 and INV-B:299 describe "waits up to `--timeout` 600 s per wait over several rounds". The candidate's reading is not in any inventory (it cites `SKILL.md:46-64`, which is UNVERIFIED here). If INV-B:95 is right, the row's "confirm each iteration stays under 4 minutes" under-specifies a required split.
  - Why Medium: pr-submit is behind D3, whose recommendation is "coordinator only", and the row plus AC-4.3 point the implementer at 4 minutes.
  - Recommendation: use one number (4 minutes) in WC-10 and say which of the two readings of the poll loop was read.

- **F-8 [Medium; label MAJOR] Several requirements have no acceptance check, or one that covers one command out of many** (SPEC:61, 64, 68, 69, 70; SPEC:186-210).
  - WC-3 (ask), WC-6 (retry) and WC-12 (`check`) have no AC. WC-10 is checked for pr-submit only (AC-4.3), while cli-eval, a P2 target, carries the same requirement (SPEC:104). WC-11 is checked for save only (AC-3.4).
  - WC-6's "fresh output directory" does not make a retry clean for the in-place editors (cleanup, improve, document inline mode, test `--fix`, SPEC:103, 107, 110, 123): a retry re-edits the partly edited files. The rows say "fresh dir" for them.
  - Why Medium: the document never states the check or the in-place retry rule.
  - Recommendation: add one AC line each for WC-3, WC-6 and WC-12; for in-place editors, make the contract list changed files and say a retry starts from the report's file list.

- **F-9 [Medium; label MINOR] Existing-contract vocabulary is not reconciled** (SPEC:62, SPEC:183, SPEC:194, SPEC:262).
  - WC-4 says commands with a contract "keep their fields". Step 4 asserts every contract's `status` is one of four values, and the Decisions row picks a fixed four-value set. No inventory records the status values of the adversarial, brainstorm, reflect and workflow contracts (INV-B:272 lists workflow fields `status`, `plan_path`, `reflect_report_path` without values). If their enums differ, "keep" and "assert" conflict. AC-0.4 (SPEC:194) applies WC-5 to a REPORT.md or TDD file that has no `status`.
  - Recommendation: say how an existing `status` value maps, and say that pre-P1 outcome is "failed if the report file is missing or empty, otherwise succeeded".

- **F-10 [Medium; label MINOR] Quoted-text collision on `--unattended`, and the empty report case** (GAP-1, GAP-5, GAP-6; SPEC:63, SPEC:228).
  - D1 recommends an explicit flag "testable by grep and cannot misfire on a person". A topic or symptom string for tdd, troubleshoot or research can contain the same token. Nothing says it is ignored inside a quoted argument.
  - WC-5 covers "no report exists" but not an empty or unparsable report.
  - Recommendation: one sentence in WORKER-CONTRACT.md: the switch counts only as a standalone argument token; an empty or unparsable report counts as no report.

- **F-12 [Medium; label MAJOR] No bound on the `ask` loop** (GAP-9; SPEC:61, SPEC:63).
  - "On an `ask` timeout it resumes the same message ID" and "No heartbeat is sent while blocked in `ask`". If the coordinator is gone or never answers, the worker loops forever, never writes `blocked` and never sends `worker_done`. `CAPS:188` marks any Orca run-time bound UNVERIFIED.
  - Why Medium: an unspecified edge case, not a stated text that does harm.
  - Recommendation: cap resumes (for example three), then write `blocked` and end `failed`.

### Architecture (Fowler, Nygard, Newman, Hohpe, Hightower)

- **F-2 [Medium; label MAJOR] The worker-session duties have no stated delivery channel** (SPEC:52, SPEC:61, SPEC:63, SPEC:65, SPEC:68, SPEC:70, SPEC:73).
  - WC-3, WC-5, WC-7, WC-10 and WC-12 are owned by "Worker session". Per SPEC:52 the shared rules live in `~/.claude/WORKER-CONTRACT.md`, which a worker reads only when a command's `## Unattended mode` section points to it. Section 2.3 (SPEC:73) lists what the brief carries (command line, contract directory, authorized outward actions, worktree) and does not say the brief tells the worker to read the contract or follow these duties. In P0 (SPEC:158) no command section exists yet, so the three smoke runs execute without the `partial` to `succeeded` rule, the one-`worker_done` rule or the no-subagent rule.
  - Why Medium: needs the guess that the brief template carries a pointer; SPEC:158 says only "a coordinator brief template listing the section 3.1 flags".
  - Recommendation: one line in 2.3 and in the P0 brief template: "read `~/.claude/WORKER-CONTRACT.md` and follow its worker duties".

- **F-3 [Medium; label MAJOR] Phase order leaves a window where `--unattended` is accepted but not honoured** (GAP-10; SPEC:154, SPEC:159, SPEC:160, SPEC:162, SPEC:225, SPEC:244).
  - P1 adds the flag to "every command in sections 3.1 and 3.2". The gate resolutions arrive in P2 (for example auggie-review, whose default posts to GitHub, SPEC:100) and P4. In between, `/sc:auggie-review <PR> --unattended` is accepted, writes a contract, and still posts and offers remediation, which WC-2 and WC-9 forbid. SPEC:154 says each phase is "independently useful".
  - SPEC:154 says "Phases 1-3 need no user decision". SPEC:225 says only that they "can proceed on the recommendations". D4 (SPEC:244) names auggie-review `--post-pr` and task `commit`/`push`, which are P2 rows.
  - Why Medium: harm needs a coordinator that dispatches a gated command before its phase, against SPEC:154's "later phases do not start until".
  - Recommendation: in P1, accept the flag on a gated command only together with an explicit refusal (`blocked`) until its gate row lands; say P2 depends on D4's recommendation.

- **F-7 [Medium; label MAJOR] WC-11 conflicts with fixed output locations, and roadmap's shared memory writes are not covered** (SPEC:69, SPEC:85, SPEC:86, SPEC:118).
  - WC-11: "Two workers in one worktree must never write the same file. Default output paths carry a timestamp or the slug the coordinator passes". The cleanup-audit row (SPEC:85) accepts a fixed `.claude-audit/` and answers with "one audit per worktree at a time (WC-11)", which is a coordinator rule, not a command change. index-repo writes a fixed `PROJECT_INDEX.md` (SPEC:86).
  - INV-B:154 records that roadmap "writes memory through `sc:save` at every wave". The roadmap row (SPEC:118) and the save row (SPEC:119) do not stop an unattended roadmap worker from writing the single-owner keys that WC-11 forbids.
  - Why Medium: the rows refine WC-11; which text wins is a guess.
  - Recommendation: list the fixed-path exceptions in WC-11 and add roadmap to the "no single-owner keys" rule.

- **F-11 [Medium; label MINOR] AC-C1 has no baseline and conflicts with the SA-2 allowance; the 43-command scope is asserted, not verified** (SPEC:25, SPEC:76, SPEC:147, SPEC:172).
  - AC-C1 requires the grep over `src/superclaude/{commands,skills,agents,core}` (minus `ccsession-tag`) to print nothing. That depends on E5's dated grep (SPEC:25), which is UNVERIFIED here. AC-C3 (SPEC:174) uses a before and after baseline; AC-C1 does not.
  - SA-2 (SPEC:147) allows an Orca mention as an example inside the contract file, which lives in `src/superclaude/core/`, a directory AC-C1 scans. An example written as `orca orchestration ask` fails AC-C1. The P0 Orca section in HOW-WE-WORK.md (SPEC:158) is in the same directory.
  - SPEC:76 says "The 43 commands in `cmd/`". INV-A:3 and INV-B:3 list 21 and 22 names as their scope; neither says `cmd/` holds only these. UNVERIFIED observation: the skill list available in this review session also shows `sc:graph`, `sc:impact` and `sc:issue`, and describes `sc-issue-protocol` as creating an Orca worktree. I could not check this against the workspace. If it holds, E5, SA-2 and AC-C1 start from a false baseline.
  - Recommendation: make AC-C1 "no new match against the pre-phase baseline", exclude `core/WORKER-CONTRACT.md`, and say whether the 43 is all of `cmd/`.

- **F-13 [Medium; label MINOR] Tasklist row picks a design the inventory advised against without recording why, and leaves a HALT unresolved** (SPEC:122).
  - INV-B:215 and INV-B:295 recommend "drop `--remediate` in 10.5; ready with `--no-reflect`". The row instead passes `--unattended` to each reflect "so the headless rule applies". INV-B:209 records that Stage 10.5 "`needs_human_decision` items HALT" (`SKILL.md:1631`). Neither the row nor the headless rule as quoted (INV-B:109: "auto-accepts for auto-fixable registers and skips the gates") says whether a `needs_human_decision` HALT ends `blocked`.
  - Why Medium: needs the guess that the headless rule covers the HALT; the Decisions row at SPEC:268 says "nothing read contradicted a verdict".
  - Recommendation: state that a `needs_human_decision` item resolves as `blocked`; add one Decisions row for the divergence from INV-B:215.

## Adversarial Analysis (Whittaker; template: "I can break this specification by [attack]...")

1. I can break this specification by **Divergence Attack**. The invariant at **AC-1.1 (SPEC:195)** fails when **a command's row says no change or no contract**. Concrete attack: before state, 37 workers-capable commands and AC-1.1 requires 37 sections. Follow SPEC:79 and the brainstorm, init-lite and load rows: 34 files edited plus 3 untouched. After state: the AC-1.1 test fails on 3 files. (F-1, blocking)
2. I can break this specification by **Sequence Attack**. The invariant at **P1 then P2 ordering (SPEC:159-160)** fails when **a gated command is dispatched between phases**. Concrete attack: P1 ships `--unattended` on auggie-review; the P2 gate row (SPEC:100) has not landed; a coordinator runs `/sc:auggie-review 12 --unattended`; the review posts to the PR and offers remediation. (F-3)
3. I can break this specification by **Sentinel Collision Attack**. The invariant at **D1 (SPEC:228)** fails when **free text contains the token `--unattended`**. Concrete attack: `/sc:troubleshoot "does --unattended skip prompts" ` run in a person's session. Before: standalone. After: if the token is parsed anywhere, the person's session loses its gates, which breaks SA-1. (F-10)
4. I can break this specification by **Zero/Empty Attack**. The invariant at **WC-4 (SPEC:62)** fails when **`--unattended` is passed with no `--contract-dir` and a file-valued `--output`**. Concrete attack: `/sc:tdd "auth component" --unattended --output docs/TDD.md`; the command hits a topic gate and must write `status: blocked`; no directory is known; no report exists; WC-5 turns that into `--outcome failed` with no `blocked_question`. (F-4)
5. I can break this specification by **Accumulation Attack**. The invariant at **WC-3 (SPEC:61)** fails when **ask timeouts repeat**. Concrete attack: cli-portify blocks at gate 1; the worker asks; the coordinator is gone; the worker resumes the same message ID every 600 s with no bound and no heartbeat. Before: Task `dispatched`. After: Task `dispatched` indefinitely. (F-12)
6. I can break this specification by **Divergence Attack** (second). The invariant at **WC-10 (SPEC:68)** fails when **a call lasts 280 s**. Concrete attack: the pr-submit poll waits 280 s; WC-10 passes it, AC-4.3 fails it. (F-6)

## Cross-expert consensus and disagreements

- Consensus: the architectural decision and the 10/27/6 partition (checked against INV-A:73 and INV-B:278) are sound; the weak points are in the rollout and the acceptance checks, not in the decision.
- Wiegers and Crispin disagree with Fowler on one point. Wiegers and Crispin want an AC per WC row (F-8). Fowler would rather narrow WC rows that only restate Orca's own rules (WC-12 restates `CAPS:66-67`) than add checks for them.
- Auto-suggestion: the specification has numeric thresholds (60 s, 4 and 5 minutes, depth 1, 0.70) and a classify-then-assign flow. The panel recommends a follow-up `--focus correctness` pass after F-1 is fixed. This is advisory and was not activated.

## Quality metrics (0-10)

| Dimension | Score | Note |
|---|---|---|
| Clarity | 8 | rows are short and cited; the word "contract" names three things (M-6) |
| Completeness | 7 | gaps in edge behaviour (F-4, F-5, F-12) and acceptance coverage (F-8) |
| Testability | 6 | AC-1.1 cannot pass as written (F-1); four WC rows lack a check (F-8) |
| Consistency | 6 | F-1; the SA-3 versus WC-4, WC-10 versus AC-4.3 and WC-11 versus row conflicts |

## Minor notes (never fail the review)

- M-1: `B-1` (nine uses) and `B-2` (two uses, SPEC:182, SPEC:194) are never defined in the candidate or the README. They look like finding ids from an earlier review. A reader of this document alone cannot resolve them.
- M-2: SPEC:16 says command changes are "limited to the worker contract in section 2". Section 3 adds changes outside it: explain's Write tool (SPEC:108), the business-panel frontmatter move (SPEC:102), the validate-tests default target (SPEC:125), cli-portify's `--resume` (SPEC:105), the load usage line (SPEC:112). SA-4 (SPEC:149) lists most of them.
- M-3: E2 (SPEC:22) says a command run by a worker "has the same tools as a command a person runs". The cited `EVIDENCE.md:45` shows only that a worker reached `state: ready` and answered. SPEC:43 correctly says no direct-route run exists.
- M-4: UNVERIFIED item 14 (SPEC:285) is a statement that a check was done, not an unverified item, and I cannot check it from the workspace.
- M-5: WC-1 (SPEC:59) says a fallback "well inside" 60 s. `EVIDENCE.md:56` (via `CAPS:49`) gives about 45 s, measured against a 45 s `--timeout-ms`, not the 60 s default. No number is stated for the fallback.
- M-6: "contract" names three things: `WORKER-CONTRACT.md`, `return-contract.yaml` and `--contract-dir`. The status `blocked` also matches Orca's Task status `blocked` (`CAPS:89`), which means unmet dependencies; a contract `blocked` ends as Task `failed` (WC-5).
- M-7: SPEC:133 justifies `/sc:git` as coordinator-only partly with `README:31`. That is a rule for the workers of this planning run, not a standing repository rule. The reason given in the same row (git mutations need the user's authorization) stands without it.
- M-8: D3 (SPEC:238-242) does not mention that pr-submit lists "Will Not: run headless / imply a daemon" (INV-B:90). The auggie-review row (SPEC:100) and D4 use an explicit `--post-pr` flag that no inventory shows exists (INV-A:38 lists only `--no-post-pr`). Under D3 option (a), P1 would still add an `## Unattended mode` section to pr-submit through AC-1.1.

## Issue question

Per Review Loop bullet 3 the session that ran the review asks the user once per loop whether to open an issue for the follow-up candidates (F-2 to F-13, M-1 to M-8). This worker's final reply is restricted to `DONE <path>`, so the question is not asked here. No issue was created. The coordinator relays the question.

## Reviser brief (blocking finding ids only; the reviser reads this report, not the command)

- Blocking finding ids: **F-1**
- Revise only the text F-1 names: SPEC:79, SPEC:84, SPEC:87, SPEC:112, SPEC:159, SPEC:183, SPEC:195, SPEC:196.
- Add no rule, mechanism or section that F-1 does not call for.
- Each added paragraph or table cites its finding id.
- Prefer deleting or narrowing to adding. For F-1 the preferred repair is to narrow AC-1.1, AC-1.2 and the P1 generic clause to the commands whose row changes them.
- Report the byte size of the candidate before and after, and the bytes added and deleted per finding id.
- Leave minor findings and Medium findings alone (F-2 to F-13, M-1 to M-8). Do not award a PASS.

verdict: FAIL

review: 1 of 3

# Spec-panel audit: Orca worker contract spec

- Command acted as: `/sc:spec-panel @.dev/orca-command-refactor/specs/orca-worker-contract-spec.md --mode critique --focus requirements,architecture`
- Prompt followed: FIRST-REVIEW prompt, `~/.claude/rules/prompts/document_review_loop_prompts.md` (read in full).
- Label: whole-document audit of the final spec, a first review of the whole document (not a scoped re-review).
- Candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`, sha256 `9bf4886e4a47262c5cf9c862441589e93e25942e3132e8035b411d7bd0318c5f`
- Baseline: none given (first review; `--re-review` and `--baseline` not passed).
- Reviewer model actually used: Sonnet 5.5 (`claude-sonnet-5-5`).
- Mode of run: attended single review. `--unattended` not passed, so no `return-contract.yaml` is written. The Improve step (step 6) was not run: the brief assigns one output file and says edit nothing else; the Boundaries section forbids modifying a specification without consent.
- Brief clauses overridden: none. The brief neither widened the scope nor graded a minor finding as blocking.
- Citation key: `SPEC:N` = line N of the candidate. `INV-A:N`, `INV-B:N`, `CAPS:N` = lines of `inventory/commands-a.md`, `commands-b.md`, `orca-capabilities.md`. `README:N` = `.dev/orca-command-refactor/README.md`. `CMD:N` = line N of `command.md` (the spec-panel definition I was given).

## Coverage

Read in full: the candidate (285 lines), `README.md`, all three inventory files, `command.md`, and the review-loop prompt file.

Checked against workspace files: every `INV-A:N`, `INV-B:N` and `CAPS:N` citation the candidate uses for a count, verdict or quote (about 120 spot checks, all matched), and the arithmetic: 43 commands = 10 ready + 27 needing change + 6 coordinator-only. The 3.1 table has 10 rows, the 3.2 table has 27 rows, and the phase lists in SPEC:159-162 together name 35 of the 37 worker-capable commands (`brainstorm` and `init-lite` appear in no phase row; see B-02).

UNVERIFIED (cannot be checked inside this sandbox, the file is outside the workspace): every `src/...`, `CLAUDE.md:N`, `Makefile:N`, `pyproject.toml:38`, `tests/...`, `HOW-WE-WORK.md:N`, `.dev/codegraph-migration/...`, `.dev/evals/...` and `~/.claude/...` line the candidate cites directly (for example SPEC:11, 25, 52, 146, 150, 164, 183). The candidate's `cmd/` and `sk/` lines are checked only to the extent the inventories quote them. The claim "43 commands in `cmd/`" (SPEC:76) is UNVERIFIED as a count of the directory; the inventories list 43 names by hand (INV-A:3, INV-B:3) and show no directory listing.

Expert panel (fixed order, focus requirements + architecture): Wiegers (lead, requirements), Adzic, Cockburn, Fowler (lead, architecture), Nygard, Whittaker (active in every panel review), Newman, Hohpe. Crispin, Gregory and Hightower were not needed: `--focus testing` and `--focus compliance` are not active; testability points were raised by Wiegers and Adzic.

`--focus correctness` is not active, so the State Variable Registry is not produced. The Guard Condition Boundary Table is produced because the candidate has thresholds and guards (SPEC:59, 61, 68, 121, 114).

Auto-suggestion: not recommended. The candidate introduces no 3+ mutable state variables and no numeric-threshold pipeline.

## Prior findings

None (first review).

## Grading check for each blocking finding

Each sentence below holds without further assumption.

- B-01: An implementer who follows AC-0.4 as written (SPEC:194) must make 7.2 step 3 pass (SPEC:182) for `/sc:troubleshoot`, and builds a check that no Phase 0 run can satisfy, because step 3 requires the outcome to match "the contract's status" and the report path to be "the WC-4 contract path", while SPEC:194 itself says the contract arrives in P1 and troubleshoot's report is `REPORT.md` with no status (SPEC:91). The gate in SPEC:154 then blocks every later phase.
- B-02: An implementer who follows AC-1.1 and AC-1.2 and the P1 scope (SPEC:159, 195-196) builds an `## Unattended mode` section naming `return-contract.yaml` in every one of the 37 commands of 3.1-3.2, including `/sc:load` (which the spec says writes no report, SPEC:112, 265) and `/sc:pr-submit` (a P4 command, SPEC:114, 162, whose D3 recommended option is "no pr-submit changes", SPEC:240). The two stated texts contradict.
- B-03: An implementer who follows WC-4 (SPEC:62) writes the adversarial contract at `<output>/return-contract.yaml`; one who follows SPEC:83 writes it at `<output>/adversarial/return-contract.yaml`; for workflow WC-4 and SPEC:73 say the path is known before dispatch from the directory the brief passes, while SPEC:92 puts it under a generated `<id>`. The coordinator then opens a path that does not exist and, by WC-5 (SPEC:63), treats the worker as having no report. Two stated texts contradict.

## === REQUIREMENTS ANALYSIS ===

### B-01 (CRITICAL, blocking, priority High) Phase 0 acceptance check cannot pass
- Expert: Wiegers, with Adzic.
- Location: AC-0.4, SPEC:194; 7.2 step 3 and step 4, SPEC:182-183; WC-4, SPEC:62; phase gate, SPEC:154; P0 row, SPEC:158.
- Issue: AC-0.4 says "steps 1-3 and 5-7 pass; step 4 uses the command's existing report file". Step 3 passes only if "its `--outcome` matches the contract's `status` under WC-5; its report path is the WC-4 contract path". In Phase 0 no command writes a WC-4 contract (SPEC:194 says so: "the contract arrives in P1"). Troubleshoot's existing report is `REPORT.md`, which has no `status` field (INV-B:242, SPEC:91); adversarial's contract filename is "not fixed" (SPEC:83, INV-A:35, INV-A:60); workflow's contract has `status`, `plan_path`, `reflect_report_path` and no `command` (INV-B:272). The carve-out covers only step 4, and the step 4 assertion (`yaml.safe_load` and `d['command']`, SPEC:183) is also undefined for a markdown `REPORT.md`.
- Consequence: the one check that "closes evidence gap 1.4 (1)" (SPEC:43, 158) fails by construction, and "later phases do not start until the earlier phase's checks pass" (SPEC:154).
- Recommendation: narrow AC-0.4 step 3 to what P0 can show (exactly one `worker_done`; `--outcome` set; `--report-path` names the command's existing report; no `AskUserQuestion`), and state what step 4 requires of a markdown report (`test -s` only). Delete rather than add; no new mechanism is needed.
- Quality impact: restores the only live proof the decision rests on.

### B-02 (CRITICAL, blocking, priority High) P1 acceptance scope contradicts the per-command rows
- Expert: Wiegers, with Cockburn.
- Location: AC-1.1 and AC-1.2, SPEC:195-196; P1 row, SPEC:159; 3.1 intro, SPEC:79; 3.2 header, SPEC:76; `/sc:load` row, SPEC:112; Decisions, SPEC:265; `/sc:pr-submit` row, SPEC:114; D3, SPEC:238-242; phase intro, SPEC:154.
- Issue (three conflicts):
  1. AC-1.1 asserts that "every command in sections 3.1-3.2" has a section "naming `return-contract.yaml`". `/sc:load` is in 3.2 with "Report: none" and the Decision at SPEC:265 rejects a report file for it. `/sc:load` is also in the P1 list (SPEC:159), so AC-1.2 ("7.2 live check on each P1 command") requires a contract that step 4 (SPEC:183) tests for and the command never writes.
  2. P1 requires "the `--unattended` flag accepted by every command in sections 3.1 and 3.2" (SPEC:159), which includes the P4 commands `/sc:implement`, `/sc:post-release`, `/sc:pr-submit`. D3's recommended option (a) is "no pr-submit changes" (SPEC:240) and SPEC:154 says only P4 waits on D2-D4. A P1 section for pr-submit would define gate resolutions (SPEC:114) that the spec schedules for P4 after a user decision.
  3. 3.1 says the ready commands' "only command changes are the small fixes in the last column" (SPEC:79), and `brainstorm` and `init-lite` have "None" there and appear in no phase row (SPEC:159-162), yet AC-1.1 requires both to carry the new section and a `--unattended` flag. In P1 the flag is "a no-op where a command has no gate" (SPEC:159), which does not say what the flag does on a gated command (auggie-review posts, cleanup prompts) until P2, although SPEC:73 tells coordinators to pass `--unattended` "from Phase 1 on".
- Recommendation: restrict AC-1.1 and AC-1.2 to the commands whose phase row is P1 (plus the 3.1 commands the spec chooses to touch), exclude `load` from the contract assertion, and state in one line which phase adds the flag to each gated command.
- Quality impact: removes a P1 gate that cannot be passed and a hidden decision on D3.

### B-03 (MAJOR, blocking, priority High) The contract path is stated two ways
- Expert: Wiegers, with Adzic.
- Location: WC-4, SPEC:62; 2.3, SPEC:73; 3.1 adversarial row, SPEC:83; 3.1 workflow row, SPEC:92; AC-1.4, SPEC:198; 7.2 step 4, SPEC:183.
- Issue: WC-4 fixes the contract at `<output-dir>/return-contract.yaml`, "the directory the coordinator passed", so "the report path is known before dispatch" (SPEC:73). The adversarial fix is `<output>/adversarial/return-contract.yaml` (SPEC:83; INV-A:60 records the on-disk variants `.../adversarial/return-contract.yaml` and `.../adversarial/adversarial/return-contract.yaml`). The workflow contract sits at `.dev/tasks/to-do/<id>/return-contract.yaml` (SPEC:92), where `<id>` is generated at run time and the brief names no output directory (SPEC:92 "Brief must pass: `--handoff none`"). The workflow fix, "write the contract for pre-creation STOPs too" (SPEC:92), names no location, and a pre-creation STOP has no package directory (INV-B:272).
- Recommendation: pick one rule (for example, WC-4 places the file in the coordinator-passed directory, and a command that writes elsewhere also copies or points to it via `report_path`), and make SPEC:83 and SPEC:92 and AC-1.4 follow it. State the pre-creation location for workflow.
- Quality impact: one checkable path per worker.

## === ARCHITECTURE ANALYSIS ===

The decision itself (Orca on top, commands stay units of work, SPEC:13-45) is supported by the evidence checked: the rejected alternative's reasons R1-R5 match CAPS:97-103, 145-150 and INV-A:90 / INV-B:285-286. The architecture findings below are all Medium or minor; none names a concrete wrong outcome under the stated text without a further guess.

Expert notes (non-finding): Fowler finds the single shared contract file plus a short per-command section a sound separation of concerns (SPEC:52). Newman asks about versioning of `WORKER-CONTRACT.md` against already-installed commands: the candidate says nothing about a contract-version field or about a command running against an older installed contract file. That is a requirement the document never states, so it is listed under follow-up candidates (M-11).

## === ADVERSARIAL ANALYSIS (Whittaker) ===

- I can break this specification by **Sequence Attack**. The invariant at **AC-0.4 / 7.2 step 3 and the P0 gate (SPEC:154, 182, 194)** fails when **a Phase 0 run is executed in the only order the spec allows (contract arrives in P1)**. Concrete attack: before = P0 complete, `/sc:troubleshoot` succeeded, `worker_done --outcome succeeded --report-path .../REPORT.md` sent, one message; step 3 requires "the contract's status" and "the WC-4 contract path"; after = no such file exists, check = fail, P1 may not start. Maps to B-01.
- I can break this specification by **Divergence Attack**. The invariant at **WC-4 (SPEC:62) vs SPEC:83** fails when **the command is `/sc:adversarial --output D`**. Concrete attack: WC-4 writes `D/return-contract.yaml`; SPEC:83 writes `D/adversarial/return-contract.yaml`; the coordinator tests the WC-4 path (SPEC:183), file absent, outcome mapping (SPEC:63) says "no report exists" so `--outcome failed` on a worker that did succeed. Maps to B-03.
- I can break this specification by **Zero/Empty Attack**. The invariant at **WC-5 (SPEC:63)** fails when **the report file exists but is empty or does not parse, or carries a `status` outside the four values (WC-4 says existing contracts "keep their fields", SPEC:62)**. Concrete attack: workflow writes its own `status` value; the coordinator's mapping has no row for it; the spec says nothing (SPEC:63, 262). Maps to M-08.
- I can break this specification by **Sentinel Collision Attack**. The invariant at **D1(a) "cannot misfire on a person" (SPEC:228)** fails when **free text given to a command contains the token `--unattended`**. Concrete attack: `/sc:troubleshoot "install fails after --unattended flag"`; the spec defines no token rule (CMD:459 shows the real command definition requires a "standalone argument token outside any quoted argument"; the candidate's contract file design has no equivalent). Maps to M-09.
- I can break this specification by **Accumulation Attack**. The invariant at **WC-3 (SPEC:61)** fails when **the coordinator never answers**. Concrete attack: gate resolves blocked; worker asks; `ask` times out; worker resumes the same message ID (SPEC:61, CAPS:60); the loop has no cap and no fall-back to `status: blocked`, and a waiting worker reads as "healthy, not failed" (SPEC:44, CAPS:129), so the stall WC-2 was written to remove returns, one layer up. Maps to M-04.
- I can break this specification by **Sequence Attack**. The invariant at **D2(a) "the worker ends failed" (SPEC:234) vs WC-3 (SPEC:61)** fails when **`/sc:implement` halts with a Ruling question and the session holds a preamble**. Concrete attack: row SPEC:109 says stop and write `blocked`; WC-3 says the session "may instead ask the coordinator once" and "re-invoke or resume the command with the answer as a flag". The coordinator is "another agent" (INV-A:66); no flag for a Ruling exists in the spec. Whether the answer counts is left to the implementer. Maps to M-04.

Whittaker's attacks that found no gap: nested-depth guard (WC-8 holds at depth 1 and under D5(b)); WC-7 (subagents may not send lifecycle messages; holds whichever way the UNVERIFIED subagent-`send` question resolves, SPEC:275).

## Guard Condition Boundary Table

All guards that carry a threshold, a flag or an enumerated value in the candidate. One row per input class that applies; classes left out are named with a one-line reason below the table.

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|-------|----------|-----------------|----------------|--------------|-------------------|--------|
| WC-5 outcome mapping | SPEC:63 | Zero/Empty | report absent | true (no report) | `--outcome failed` | OK |
| WC-5 outcome mapping | SPEC:63 | Zero/Empty | report present, zero bytes or unparseable | unknown | not stated (only "no report exists") | GAP (M-08) |
| WC-5 outcome mapping | SPEC:63 | One/Minimal | `status: failed` | true | `--outcome failed` | OK |
| WC-5 outcome mapping | SPEC:63 | Typical | `status: succeeded` | true | `--outcome succeeded` | OK |
| WC-5 outcome mapping | SPEC:63 | Sentinel Value Match | `status: blocked` / `partial` | true | blocked to failed; partial to succeeded | OK |
| WC-5 outcome mapping | SPEC:62-63 | Sentinel Value Match | an existing contract's own `status` word outside the four values | unknown | not stated ("keep their fields" vs fixed set) | GAP (M-08) |
| WC-5 outcome mapping | SPEC:63 | Legitimate Edge Case | audit verdict FAIL, run completed | true | `--outcome succeeded`, body says FAIL | OK |
| WC-10 wait size | SPEC:68 | One/Minimal | single wait of 240 s | true | allowed; heartbeat between waits | OK |
| WC-10 wait size | SPEC:68 | Typical | wait of 4 min (checked at AC-4.3, SPEC:210) | true | allowed | OK |
| WC-10 wait size | SPEC:68 | Maximum/Overflow | one blocking call over 5 min that cannot be split (Agent-tool fan-out, foreground test run, a long `uv run` step) | true | "must be split into waits of at most 4 minutes" but no split exists for such a call | GAP (M-06) |
| WC-10 wait size | SPEC:68, 283 | Legitimate Edge Case | poll-plus-sleep iteration of unknown length | unknown | flagged UNVERIFIED by the spec (item 12) | OK (self-flagged) |
| WC-1 launch prompt | SPEC:59 | Zero/Empty | no startup prompt | false | passes | OK |
| WC-1 launch prompt | SPEC:59 | Typical | fallback at 30 s | true | passes (CAPS:49) | OK |
| WC-1 launch prompt | SPEC:59 | Maximum/Overflow | fallback at 45-60 s | true | "well inside" with no number; CAPS:49 shows about 45 s fails | GAP (M-02) |
| WC-3 ask | SPEC:61 | Zero/Empty | `--timeout-ms` omitted | n/a | resumes by message ID; default UNVERIFIED (SPEC:281) | OK (self-flagged) |
| WC-3 ask | SPEC:61 | Maximum/Overflow | coordinator never answers; repeated timeouts | true | no cap, no fall-back to `blocked` | GAP (M-04) |
| WC-3 ask | SPEC:61 | Legitimate Edge Case | re-invoked command hits a second gate | true | "ask the coordinator once": per gate or per run, not stated | GAP (M-04) |
| nested depth | SPEC:33, 66 | Typical | depth 1 | true | commands do not call Orca (WC-8) | OK |
| nested depth | SPEC:66, 252 | Legitimate Edge Case | depth raised (D5 option b) | true | WC-8 still forbids | OK |
| `--unattended` | SPEC:51, 228 | Zero/Empty | flag absent | false | today's behaviour (SA-1) | OK |
| `--unattended` | SPEC:51, 228 | Typical | flag as standalone token | true | unattended mode | OK |
| `--unattended` | SPEC:228 | Sentinel Value Match | token inside free-text or quoted argument | unknown | not stated | GAP (M-09) |
| `--unattended` | SPEC:128 | Legitimate Edge Case | passed to a section-4 coordinator-only command | n/a | "get no unattended mode"; ignore, refuse or run is not stated | GAP (minor, N-06) |
| `--unattended` in P1 | SPEC:159 | Legitimate Edge Case | passed to a gated command before its P2 row | true | "no-op where a command has no gate"; gated case not stated | GAP (inside B-02) |
| task confidence gate | SPEC:121 | Zero/Empty | confidence 0.0 | true (< 0.70) | blocked | OK |
| task confidence gate | SPEC:121 | Typical | 0.85 | false | proceeds | OK |
| task confidence gate | SPEC:121 | Legitimate Edge Case | exactly 0.70 | false (inventory wording "< 0.70", INV-B:199) | proceeds | OK |
| pr-submit `--monitor` | SPEC:114 | One/Minimal | `--monitor 1` | true | refused | OK |
| pr-submit `--monitor` | SPEC:114 | Typical | `--monitor 3` | n/a | default; no y/n gate (INV-B:89) | OK |
| pr-submit `--monitor` | SPEC:114 | Zero/Empty | `--monitor 0` and `--monitor 2` | n/a | not stated by the spec or by INV-B:89 | GAP (minor, N-06) |

Classes left out: WC-5 Maximum/Overflow (a status field has no capacity); WC-10 Zero/Empty (a zero-length wait needs no split); WC-1 One/Minimal and Sentinel (no value to collide); WC-3 One/Minimal and Sentinel (no numeric input other than the timeout); nested depth Zero/Empty (a setting below 1 falls back to the default, CAPS:100); task confidence null (the checker always returns a number); `--unattended` Maximum/Overflow (a flag has no capacity); `--monitor` Maximum/Overflow (a fixed ordinal set).

FR-8 / FR-9 grading: every GAP above is Medium or minor under the grading rule (a requirement the document never states, or a reading the implementer must guess), except the P1 gated-command GAP, which is part of B-02. FR-10: the table is complete (all cells filled, every guard listed, every omitted class named above), so synthesis is not blocked.

## Pipeline Dimensional Analysis (FR-17 to FR-21)

Trigger: the candidate describes one multi-stage count-changing flow, the command inventory to worker-capable set to phase schedule to acceptance check (the coordinator-to-worker flow itself is 1 Task to 1 worker to 1 report and does not change counts).

Quantity Flow Diagram:

```text
[Commands in cmd/: 43 (UNVERIFIED as directory count)]
   --> [Triage: 10 ready + 27 needs-change + 6 coordinator-only = 43 (checked, SPEC:76)]
          |
          v
   [Worker-capable: 37 (10 + 27)]
          |--> [Phase rows name: 35 (P1 13, P2 15, P3 4, P4 3); brainstorm + init-lite in no row]
          |--> [AC-1.1 asserts a section + return-contract.yaml: 37]  <-- consumer expects 37, one of them (load) writes no contract: MISMATCH (B-02)
          |--> [Phase P4 commands needing a D2-D4 answer: 3]
          |         [P1 flag/section scope "every command in 3.1 and 3.2": 37]  <-- includes the 3 P4 commands: MISMATCH (B-02)
```

Consistency check: the 43 = 10 + 27 + 6 conservation holds. The 37 vs 35 gap is handled by the "every command in sections 3.1 and 3.2" clause (SPEC:159), so it is not a mismatch. The 37 (AC-1.1) vs 36 contract writers (load writes none) and the 37 (P1 scope) vs 34 commands scheduled in P1 to P3 are the mismatches recorded as B-02.

## Traceability (Wiegers): requirement to phase to acceptance check

| Req | Phase | Acceptance check | Note |
|-----|-------|------------------|------|
| WC-1 | none (owner "Launch setup", SPEC:59) | none beyond 7.2 step 1 | M-02 |
| WC-2 | P1-P4 | AC-2.2, AC-4.1 | M-01 |
| WC-3 | none | none | M-02, M-04 |
| WC-4 | P1 | AC-1.1, AC-1.2, AC-1.4 | B-02, B-03 |
| WC-5 | P1 | 7.2 step 3 | B-01, M-08 |
| WC-6 | P1-P3 per row | none (no retry test) | M-02 |
| WC-7 | P0 | AC-0.4 step 5 | OK |
| WC-8 | all | AC-C1 | M-10 |
| WC-9 | P2, P4 | AC-2.4, AC-4.2 | M-05 |
| WC-10 | P2 (cli-eval), P4 (pr-submit) | AC-4.3 only | M-06 |
| WC-11 | P3 (save) | AC-3.4 only | OK |
| WC-12 | none | none | M-02 |

## Follow-up candidates (Medium warnings and minor notes; none triggers a revision)

These never fail the review and are not in the Reviser brief. The session that ran this review should ask the user once whether to open an issue for them; this audit creates none (an unattended-style run only records the list).

### Medium

- M-01 (Adzic): AC-2.2 (SPEC:200) applies one pass condition, "contract `status: blocked` with a non-empty `blocked_question`", to "each P2 command", but several P2 rows resolve a gate by default or by switch, not by blocking: research pins a strategy (SPEC:116), auggie-review turns posting off (SPEC:100), cleanup and improve defer items (SPEC:103, 110), tasklist passes a flag (SPEC:122). A tester following the pass condition cannot make those commands end `blocked`. Needs the guess that the tester restricts the check to commands with a `blocked` row.
- M-02 (Wiegers): five requirements have no acceptance check or no phase: WC-1 (no phase; "well inside" the 60 s limit has no number, while CAPS:49 shows about 45 s already fails; the only Orca-aware primitive, the `ccsession-tag` launcher, SPEC:25, is not named in any phase), WC-3 (the `ask` route is never exercised by section 7), WC-6 (no retry test with `--retry-of`), WC-12 (no check), WC-10 and WC-11 (one command each). Requirements owned by "Worker session" (WC-3, 5, 7, 12; SPEC:61, 63, 65, 70) have no stated mechanism that makes the worker session follow them (the brief template is only listed as a P0 deliverable, SPEC:158).
- M-03 (Fowler): no general rule for a command that invokes another command or skill while unattended. Only tasklist-to-reflect is covered (SPEC:122). Others: workflow runs reflect (INV-B:271), release-split runs brainstorm and adversarial (INV-B:119), tdd runs `/task` (INV-B:219), task calls troubleshoot (INV-B:201), cli-eval create runs spec-panel (INV-A:44), roadmap and troubleshoot call adversarial. WC-2 says "the command never calls `AskUserQuestion`" (SPEC:60); whether a nested command's prompt counts, and whether the flag is passed down, is not stated. (CMD:464 shows the real spec-panel definition carries a "Nested invocations" field; the candidate's contract design has none.)
- M-04 (Nygard, Whittaker): WC-3 (SPEC:61) is generic. (a) It is not limited by D2(a) (SPEC:234), D4 or WC-9 (SPEC:67): an `ask` answer passed back "as a flag" could stand in for a Ruling, which INV-A:66 says another agent's message cannot be, or for an outward-action authorization. (b) It has no cap on resumes and no fall-back to `blocked`. (c) "once" is per gate or per run, unstated. Each needs the guess that the implementer picks the unsafe reading.
- M-05 (Wiegers): WC-9 (SPEC:67) says an outward default "turns on only through the command's own explicit flag written in the brief". No such flag exists in the inventories for post-release, pr-submit or task `commit`/`push` (INV-B:85, 95, 205), and the spec never says P4 adds them, yet AC-4.2 (SPEC:209) says "with no authorization flags" and AC-4.3 expects pushes and a PR (SPEC:210). D4(a) (SPEC:245) names "the command's explicit flag" without defining it.
- M-06 (Nygard): WC-10 (SPEC:68) cannot be met by command text for a call that blocks the top-level session for longer than 5 minutes without a splittable wait: an Agent-tool fan-out (cleanup-audit waves, tdd research agents, brainstorm advocates; INV-A:35, 39, 42, INV-B:221), a foreground test or build run. Whether a missed heartbeat matters is itself UNVERIFIED (CAPS:182 item 7). Only pr-submit is tested (AC-4.3).
- M-07 (Cockburn): `--output` has two meanings. In 3.1 and 3.2 it is a file for tdd (SPEC:90), init-lite (SPEC:87) and spec-panel (SPEC:120), while WC-4 (SPEC:62) places the contract in "the directory the coordinator passed (`--output` / `--output-dir`)". WC-6 says a command without resume "writes each run into a fresh output directory" (SPEC:64), which reads as the command creating a subdirectory, whereas WC-4 and 7.2 step 4 test the coordinator-passed directory. The rows "add `--output`" (analyze, build, design, test, etc., SPEC:99-123) do not say file or directory. Needs a guess.
- M-08 (Wiegers): WC-5 and WC-4 do not define a report that is empty, unparseable, or carries a `status` outside the four values although WC-4 says existing contracts "keep their fields" (SPEC:62-63). Decisions (SPEC:262) fix the four-value set without saying how existing values map.
- M-09 (Whittaker): the `--unattended` switch has no token rule (quoted free text, a flag inside a prompt), so D1(a)'s claim "cannot misfire on a person" (SPEC:228) is untested; the real spec-panel definition carries such a rule (CMD:459).
- M-10 (Fowler): AC-C1 (SPEC:172) and SA-2 (SPEC:147) disagree on scope. SA-2 allows an Orca mention "as an example of a caller's question channel inside the contract file", and AC-C1 greps `src/superclaude/core` (where the contract file lives) for `orca orchestration ...` and expects no output; a contract example written in command form prints and the check fails. The regex also misses `orca status`, `orca open`, `orca-ide skills get` and `orca worktree` variants spelled without the listed words. The baseline "prints nothing" depends on E5's grep (SPEC:25, UNVERIFIED here). Separately, this session's own command list includes `/sc:issue`, whose description says it creates an Orca worktree and launches an agent, and `/sc:graph` and `/sc:impact`; none is in either inventory and none is covered by "43 commands" (SPEC:76). If they are in `cmd/`, E5, SA-2's baseline, AC-C1 and the 43 count are wrong. UNVERIFIED: not checkable inside the workspace.
- M-11 (Newman): no contract-version field and no statement of what a command does when the installed `WORKER-CONTRACT.md` is older or missing. The commands' sections "point to the installed contract path" (SPEC:52) only.
- M-12 (Fowler, Nygard): the tasklist row (SPEC:122) says Stage 10.5 passes `--unattended` to each reflect and that "its reflect fan-out runs one layer below the worker, inside Claude Code's nesting limit". (a) INV-B:215 recommended "drop `--remediate` in 10.5", and the spec changes that without a Decisions entry; under reflect's headless rule auto-accept applies to auto-fixable registers (INV-B:109), so an unattended tasklist would start a remediation handoff nobody requested. (b) INV-B:210 and INV-B:322 mark nested spawning inside those subagents UNVERIFIED; reflect's own agents are a second layer (and Tier 2 adversarial advocates a third), against INV-A:14's "three layers below the main conversation". The candidate's UNVERIFIED list (SPEC:271-285) omits the question.
- M-13 (Cockburn): rows that say "refused" under `--unattended` (SPEC:102, 108, 114, 123, plus `--interactive` on cleanup/improve/roadmap) are not one of WC-2's three resolutions (SPEC:60) and WC-4 gives no contract status for a refusal; by WC-5 both `blocked` and `failed` map to `--outcome failed`, so the effect is limited to the report.

### Minor notes

- N-01: SPEC:73 cites "B1, SPEC:158-159" for why Phase 0 briefs omit the flag; "B1" is not defined anywhere in the candidate.
- N-02: SPEC:16 says the command changes are "limited to the worker contract"; section 3 also carries drift and defect fixes (SPEC:112, 118, 124-125) acknowledged in SA-4 (SPEC:149) and section 8 item 8 (SPEC:220). Wording overclaim only.
- N-03: AC-C5 (SPEC:176) checks command files only, while most gate logic lives in skill files (for example SPEC:100, 105, 109, 114, 122), so the "additive edits" guarantee is unchecked where most edits land.
- N-04: 7.2 step 2 (SPEC:181) samples `worker-show` once per 5 minutes and passes if `agentWait` is "never non-null"; a short wait between samples is missed.
- N-05: mapping `partial` to `--outcome succeeded` (SPEC:63, 263) marks the Task completed, so a coordinator following the ready-wave pattern (CAPS:86) sees dependents as ready; SPEC:73 says the coordinator opens the report, but no rule says to hold dependents on `partial`.
- N-06: `--monitor 0` and `--monitor 2` under `--unattended`, and a section-4 command that receives `--unattended`, have no stated behaviour (guard-table rows).
- N-07: E4 (SPEC:24) says Agent-tool subagents "are not counted by Orca's nesting limit" as evidence, while the cited CAPS:155 marks "Orca never limits them" UNVERIFIED; the candidate's own 1.4 item 3 (SPEC:45) states the gap correctly.
- N-08: the "11 load-bearing locations re-read" statement (SPEC:11) and the 340-citation check (SPEC:285) cannot be re-run here; they are UNVERIFIED and affect no finding.

## Verdict basis

Three blocking findings are open (B-01, B-02, B-03). The 43 = 10 + 27 + 6 split, the evidence for the decision (E1-E6, R1-R5) and the citation spot checks held; the blockers are in the acceptance and report-path layer, not in the decision.

## Reviser brief

Blocking finding ids: B-01, B-02, B-03. Only these.

Rules for the reviser (restated from the Review Loop section, bullet 6; the reviser reads this report, not the command):
- Revise only text a blocking finding names.
- Add no rule, mechanism or section that no blocking finding calls for.
- Each added paragraph or table cites its finding id.
- Prefer deleting or narrowing to adding.
- Report the byte size of the candidate before and after, and the bytes added and deleted per finding id.
- Leave Medium and minor findings (M-01 to M-13, N-01 to N-08) alone.
- Return the candidate once and do not award yourself a PASS.

Where the blockers sit: B-01 at SPEC:182-183 and SPEC:194; B-02 at SPEC:159 and SPEC:195-196 (and the rows at SPEC:112, 114); B-03 at SPEC:62, SPEC:83, SPEC:92 and SPEC:198.

verdict: FAIL

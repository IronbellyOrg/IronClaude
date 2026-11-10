review: 1 of 3

# Spec-panel review, round 1: Orca worker-contract spec

| Field | Value |
|---|---|
| Command | `/sc:spec-panel @.dev/orca-command-refactor/specs/orca-worker-contract-spec.md --mode critique --focus requirements,architecture` |
| Candidate | `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md` |
| Candidate sha256 | `d3cdbe573e57303b9ce6c93d1fe98ba18fb7cb1a15773d926bf6a0c31425200d` (57763 bytes) |
| Baseline sha256 | not applicable (first review, no `--re-review` and no `--baseline`) |
| Reviewer model actually used | claude-sonnet-5-5 (Sonnet 5.5) |
| Review prompt followed | FIRST-REVIEW prompt, `~/.claude/rules/prompts/document_review_loop_prompts.md` (read in full before the review) |
| Input type | Neither TDD nor PRD: the spec has 9 numbered `## N.` headings (fewer than 10), no `parent_doc`/`coordinator` frontmatter and no PRD headings, so no `target_release` question and no downstream-roadmap frontmatter apply |
| Improve step | Not run. The brief says write only this report, and "Modify specifications without explicit user consent" is a Will Not (command.md Boundaries). No revised specification was written |

Citation shorthand: `SPEC:N` = line N of the candidate. `INV-A:N`, `INV-B:N`, `CAPS:N` = line N of `.dev/orca-command-refactor/inventory/commands-a.md`, `commands-b.md`, `orca-capabilities.md`. `README:N` = `.dev/orca-command-refactor/README.md`. A citation to a file outside `.dev/orca-command-refactor/` (`src/...`, `CLAUDE.md`, `EVIDENCE.md`, `.dev/codegraph-migration/...`) could not be checked in this sandbox and is marked UNVERIFIED.

## What this review covered

- Read in full: the candidate (285 lines), `README`, all three inventories, the review-loop prompts file, and the command definition.
- Checked against the inventories: every `INV-A`/`INV-B` line the spec cites in section 3 (all 37 rows) and section 4 (all 6 rows) points at the row or note for that command; the `CAPS` lines cited in sections 1.2-2.2 say what the spec says they say. The 10 / 27 / 6 split adds up against `INV-A:73` (5 / 13 / 3) and `INV-B:278` (5 / 14 / 3), and the 27 rows of section 3.2 carry phases 9 + 11 + 4 + 3 = 27.
- Not checkable here, left UNVERIFIED: every `src/superclaude/...` line, `CLAUDE.md:N`, `EVIDENCE.md:N` (other than as quoted in `CAPS`), the `.dev/codegraph-migration/` return contract, the "11 locations re-read" claim at SPEC:11, and the "about 340 citations re-read" claim at SPEC:285.
- Behavior and dependencies inspected: the worker contract (WC-1 to WC-12), the per-command rows, the standalone rules (SA-1 to SA-6), the phase plan, the acceptance checks, and the five open decisions, against the Orca facts in `CAPS` and the command facts in `INV-A`/`INV-B`.
- Not done: no Orca command was run (none exists in this sandbox); no source file was read.
- Focus areas: `requirements` (Wiegers lead, Adzic, Cockburn) and `architecture` (Fowler lead, Newman, Hohpe, Nygard). Whittaker is active in every review. Crispin, Gregory and Hightower reviewed in sequence; their points are folded into the buckets below.
- `--focus correctness` is not active, so no State Variable Registry is produced. Advisory only: the spec has numeric thresholds (60 s, 5 min, 4 min, 240 s, 3 failures) and a multi-stage rollout, so a later run may add `--focus correctness`.

## Guard Condition Boundary Table (hard gate, completed before synthesis)

Guards found: G1 the contract location rule (WC-4), G2 the outcome mapping (WC-5), G3 the wait-splitting rule (WC-10), G4 the retry rule (WC-6), G5 the `--unattended` switch (WC-2, SA-1), G6 the readiness rule (WC-1). The depth-1 rule (R1, WC-8), the `consumer_fenced` rule (WC-12) and the 3-failure circuit breaker are stated by Orca facts the spec quotes and are each given one class below where they could fail. Input classes that cannot occur for a guard are left out with a one-line reason under the table. A GAP is graded by FR-8/FR-9: blocking only when it names a concrete wrong outcome, otherwise Medium.

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|---|---|---|---|---|---|---|
| G1 contract location `<output-dir>/return-contract.yaml` | SPEC:62 | Zero/Empty | no output flag exists or none passed (cleanup-audit, index-repo: SPEC:85-86 "Brief must pass: none"/"`--pass <N>`") | undefined | none; SPEC:62 defines `<output-dir>` only as "the directory the coordinator passed" | GAP (Medium, M-2) |
| G1 | SPEC:62, SPEC:90, SPEC:87 | Sentinel Value Match | `--output` carries a file path (tdd, init-lite) | false (a file is not a directory) | contradiction: SPEC:62 says directory, SPEC:87 and SPEC:90 pass `--output <file>`, SPEC:200 expects a tdd contract | GAP (blocking, B-1) |
| G1 | SPEC:62, SPEC:92 | Legitimate Edge Case | workflow stops before its package exists (no `<id>` directory) | undefined | SPEC:92 says "write the contract for pre-creation STOPs too" with no location | GAP (Medium, M-2) |
| G1 | SPEC:62, SPEC:83 | Typical | adversarial: `--output <dir>` | true, but path is `<dir>/adversarial/return-contract.yaml` | SPEC:83 gives a path that differs from the SPEC:62 template; both stated | GAP (Medium, M-2) |
| G1 | SPEC:62, SPEC:84 | Typical | brainstorm: `--output <dir>` | true | `<output>/return-contract.yaml`, matches | OK |
| G2 outcome mapping | SPEC:63 | Zero/Empty | no report file | failed | `--outcome failed` | OK |
| G2 | SPEC:63 | Zero/Empty | report file exists but is empty, unparsable or has no `status` | undefined | not specified (SPEC:63 handles only "no report exists") | GAP (Medium, M-1) |
| G2 | SPEC:63 | Sentinel Value Match | `status` outside the four values (existing contracts' own vocabulary, SPEC:62 "keep their fields") | undefined | AC step 4 (SPEC:183) asserts the four values for every command's contract | GAP (Medium, M-3) |
| G2 | SPEC:63, SPEC:262-263 | Legitimate Edge Case | `partial`; audit with verdict FAIL | true | `--outcome succeeded`, body states status | OK |
| G2 | SPEC:63 | Maximum/Overflow | stale report from an earlier attempt present in a reused directory | "report exists" is true | not specified; the "no report exists" branch cannot fire | GAP (Medium, M-1) |
| G3 wait split (WC-10) | SPEC:68 | One/Minimal | a single blocking call of 250 s | false (trigger is "longer than 5 minutes") | allowed by SPEC:68; refused by SPEC:210 ("no single tool call exceeds 240 s") | GAP (Medium, M-5) |
| G3 | SPEC:68 | Sentinel Value Match | a call of exactly 300 s | false | not specified (trigger "longer than 5 minutes"; heartbeat "every 5 minutes") | GAP (minor, n-1) |
| G3 | SPEC:68, SPEC:104 | Maximum/Overflow | eval wait up to 3600 s | true | split into waits of at most 4 minutes | OK |
| G3 | SPEC:65, SPEC:68 | Legitimate Edge Case | long Agent-tool/Task fan-out wait inside the command (cleanup-audit, tdd) | not a poll wait, cannot be split | not specified; subagents may not heartbeat (SPEC:65) | GAP (Medium, M-4) |
| G4 retry (WC-6) | SPEC:64, SPEC:72-73 | Typical | resume flag exists (brainstorm `--resume-from`, implement `--resume`) | true | resumes from disk | OK |
| G4 | SPEC:64, SPEC:62 | Legitimate Edge Case | retry worker given the same brief and `<output-dir>` as the failed attempt, command has "fresh dir" | undefined | SPEC:64 says "fresh output directory"; SPEC:62 says the coordinator passes the directory; SPEC:73 does not require a new one | GAP (Medium, M-1) |
| G4 | SPEC:64, SPEC:87 | Legitimate Edge Case | init-lite re-run overwrites its report | true | SPEC:87 lists "Re-run overwrites" as its resume, a third mechanism not in SPEC:64 | GAP (minor, n-2) |
| G5 `--unattended` switch | SPEC:51, SPEC:146 | Zero/Empty | flag absent | false | today's behavior unchanged (SA-1) | OK |
| G5 | SPEC:60, SPEC:100, SPEC:103 | One/Minimal | flag present, no person-gate | true | gates resolve per row | OK |
| G5 | SPEC:60, SPEC:83-84, SPEC:89 | Legitimate Edge Case | `--unattended` together with `--interactive` on adversarial, brainstorm, release-split | both | rows say "never `--interactive`" only as a brief rule; cleanup, improve, roadmap refuse it (SPEC:103, 110, 118) | GAP (Medium, M-9) |
| G5 | SPEC:128 | Legitimate Edge Case | `--unattended` passed to a section-4 command | undefined | "get no `--unattended` mode", behavior when passed not stated | GAP (minor, n-3) |
| G6 readiness (WC-1) | SPEC:59 | Typical | startup prompt with a fallback | true | "well inside the readiness limit" (default 60 s) | GAP (minor, n-4): no number, though SPEC:59 cites a 30 s pass and a roughly 45 s fail |
| Depth guard | SPEC:33, SPEC:66 | Legitimate Edge Case | depth-1 worker calls `task-create` | unknown | WC-8 forbids it; Orca behavior UNVERIFIED at SPEC:276 | OK (spec says UNVERIFIED and forbids it) |
| `consumer_fenced` | SPEC:70 | Zero/Empty | `check` returns nothing | not fenced | continue; stop only on `consumer_fenced` | OK |

Classes left out: G1 Maximum/Overflow (a path has no capacity bound that the spec relies on); G3 Zero/Empty (a zero-length wait needs no split); G5 Maximum/Overflow and Sentinel (the switch is a single boolean token); G6 Zero/Empty and Maximum (the limit is an Orca constant, not a spec input).

FR-10 completion: every guard found is enumerated and every applicable class has a row or a reason. The table is complete and does not block synthesis.

## Pipeline Dimensional Analysis (triggered: inventory, then verdicts, then phase assignment, with count changes)

Quantity Flow Diagram (counts from SPEC:76, SPEC:83-92, SPEC:99-125, SPEC:128-137, SPEC:159-162, SPEC:195):

```text
[Source: 43 commands (INV-A 21 + INV-B 22)] --> [Verdict split] --> [37 worker-capable (10 ready, 27 needs-change)]
                                                               \--> [6 coordinator-only]  (section 4, no --unattended)
[37 worker-capable] --> [Phase assignment by "Commands" column]
        P1: 9 needs-change + 4 ready (adversarial, cleanup-audit, index-repo, workflow) = 13
        P2: 11 needs-change + 4 ready (reflect, release-split, tdd, troubleshoot)       = 15
        P3: 4 needs-change                                                                =  4
        P4: 3 needs-change                                                                =  3
        listed total = 35                      <-- MISMATCH: brainstorm and init-lite appear in no phase
[Consumer P1 scope, SPEC:159]  expects flag on 37 ("every command in sections 3.1 and 3.2")
[Consumer AC-1.1, SPEC:195]    expects 37 sections naming return-contract.yaml
[Consumer 3.1 intro, SPEC:79]  says the only changes are the "Small fix" column; brainstorm and init-lite say "None"
[Contract writers]             load has none (SPEC:112) --> 36 of 37 can satisfy AC-1.1 as written (see B-2)
```

The divergence is graded by consequence (finding M-6 below). FR-19 labels a dimensional mismatch CRITICAL; the Review Loop says grade by consequence, not by label. The FIRST-REVIEW grading check does not hold here without a guess, because P1's scope sentence at SPEC:159 names all 37 and the Commands column is the only place that omits two, so an implementer can read either way. It is listed as Medium. The load count is a blocking finding on its own terms (B-2).

## === REQUIREMENTS ANALYSIS === (Wiegers lead, Adzic, Cockburn)

### B-1 (CRITICAL as labelled, blocking): WC-4 defines the contract location as a directory, but the briefs for tdd and init-lite pass a file

- **Quoted texts.** SPEC:62: "`<output-dir>` is the directory the coordinator passed (`--output` / `--output-dir`)" and "known before dispatch". SPEC:90 (tdd): "Brief must pass: a precise component prompt, not a bare topic; `--output <file>`". SPEC:87 (init-lite): "Brief must pass: `--output <file>`". SPEC:200: "`/sc:tdd "auth" --unattended --output <file>` with a bare topic" must end with "contract `status: blocked` with a non-empty `blocked_question`". SPEC:183: step 4 runs `test -s <contract>`.
- **Grading check.** An implementer who follows the stated text as written builds a tdd (and init-lite) `## Unattended mode` that writes `<output-dir>/return-contract.yaml`, but for these two commands the coordinator passes no directory, only a file, so the text gives no contract path; the only literal reading puts it at `<file>/return-contract.yaml`, a path below a regular file (or, if the writer creates parents before the TDD exists, a directory at the TDD's own path, which then blocks writing the TDD). That is wrong because WC-4 requires a path "known before dispatch", and AC-2.2 (SPEC:200) and step 4 (SPEC:183) cannot pass for tdd when its blocked contract has no defined path. Two stated texts contradict each other (a directory versus a file), so no further assumption is needed.
- **Expert attribution.** Wiegers (requirement not testable as written), Adzic (no example of the contract path for a file-valued `--output`), Whittaker (Zero/Empty attack, A-1).
- **Recommendation.** State one rule that covers file-valued `--output`: for example, the contract path is a separate coordinator-passed value, or it is beside the file under a stated name. Rationale: the AC cannot be run until the path is unambiguous. Delete or narrow before adding.
- **Priority.** High. **Quality-impact estimate.** Testability +1.5, Consistency +1.

### B-2 (CRITICAL as labelled, blocking): load is a P1 command that AC-1.2 must run live with a contract, but its row says it has no report and must not be its own Task

- **Quoted texts.** SPEC:112 (load): Report "none (see note)", "use it as a step inside another worker's brief, not as its own Task", Phase "P1 (usage line only)". SPEC:265: "a report file would be an unrequested addition". SPEC:159: P1 includes "load (usage line only)". SPEC:196 (AC-1.2): "7.2 live check on each P1 command with `--unattended --output <dir>`". SPEC:182: step 3 passes only if "its report path is the WC-4 contract path". SPEC:183: step 4 `test -s <contract>`. SPEC:195 (AC-1.1): every command in sections 3.1-3.2 has a section "naming `return-contract.yaml`".
- **Grading check.** An implementer who follows the stated text as written builds load with no contract and no report (SPEC:112, SPEC:265) and dispatches it as no Task of its own, and then runs AC-1.2, which includes load as a P1 command and requires a `worker_done` report path equal to a WC-4 contract and `test -s <contract>` to succeed. That is wrong because those steps can never pass for load; if the implementer instead adds a contract to satisfy AC-1.2, they break SPEC:112 and SPEC:265. Two stated texts contradict each other, so the sentence holds without a guess.
- **Expert attribution.** Wiegers (traceability: a requirement row and an acceptance check disagree), Cockburn (the actor for load is the coordinator's own session, not a worker; the live check assumes a worker goal), Fowler (a context loader mixed into a worker-contract set).
- **Recommendation.** Exclude load from AC-1.1/AC-1.2 and from the "every command" wording at SPEC:159 and SPEC:195, or give it the contract; pick one and make SPEC:112, SPEC:159, SPEC:195-196 and SPEC:265 agree. Rationale: narrowing to the stated decision (SPEC:265) is the smaller change.
- **Priority.** High. **Quality-impact estimate.** Consistency +1.5, Testability +1.

### M-1 (MAJOR as labelled, graded Medium): the retry and stale-report rules are not stated for reused or fixed output locations

- Texts: SPEC:64 (WC-6: "writes each run into a fresh output directory so a re-run starts clean"), SPEC:62 (WC-4: the coordinator passes `<output-dir>`), SPEC:72-73 (section 2.3: the brief states the output directory; no "new directory per attempt" duty), SPEC:63 (WC-5: "or no report exists").
- Why Medium: the sentence needs a guess that the coordinator reuses the same brief and the implementer writes into it; the text allows a fresh directory per attempt. No stated text forces the harm. Missing restriction: nothing says a command removes or overwrites a prior `return-contract.yaml` at start, or that the retry brief carries a new directory. Fixed-location commands (cleanup-audit `.claude-audit/`, index-repo `PROJECT_INDEX.md`, init-lite default) cannot be given a fresh directory at all.
- Wrong outcome if guessed badly: a coordinator reads the first attempt's `blocked` or `succeeded` contract after a crashed retry, and WC-5's "no report exists" branch never fires.
- Expert: Nygard, Whittaker (Sequence attack, A-4). Recommendation: add one sentence to section 2.3 that a retry brief names a new output directory and that a command overwrites any prior contract in its directory before other work. Priority: Medium.

### M-2 (MAJOR as labelled, graded Medium): WC-4's location rule has no answer for four more row shapes

- Texts: SPEC:85-86 (cleanup-audit, index-repo: no output flag, fixed locations), SPEC:92 (workflow: pre-creation STOP, contract path depends on a package `<id>` that does not yet exist), SPEC:83 (adversarial: `<output>/adversarial/return-contract.yaml`, not `<output-dir>/return-contract.yaml`), SPEC:115-116 (recommend, research: "contract" with no directory stated).
- Why Medium: each is a missing statement, not a stated text that does harm; the implementer would pick a path and the coordinator would find it only by looking. B-1 is the one pair where two stated texts contradict.
- Recommendation: one table column "contract path" in sections 3.1/3.2 rather than the single template at SPEC:62. Priority: Medium.

### M-3 (MAJOR as labelled, graded Medium): the fixed four-value `status` set may collide with the status values existing contracts already use

- Texts: SPEC:62 ("Commands that already write a contract keep their fields and add the missing ones"; `status` one of `succeeded`, `partial`, `failed`, `blocked`), SPEC:262 (Decision: fixed set), SPEC:148 (SA-3: a standalone run "writes the same files it writes today"), SPEC:183 (step 4 asserts the four values for every command).
- The existing `status` values of the workflow, brainstorm, reflect and adversarial contracts are not stated anywhere in the inventories (`INV-B:272` names the `status` field only). UNVERIFIED whether they equal the four values.
- Why Medium: harm exists only if the existing values differ, which cannot be checked here. Recommendation: list the existing values in a single table in section 2 or say which contracts get a mapping. Priority: Medium.

### M-6 (MAJOR as labelled, graded Medium): brainstorm and init-lite appear in no phase

- Texts: SPEC:159-162 (Commands columns list 35 of 37), SPEC:159 (scope: flag accepted by "every command in sections 3.1 and 3.2"), SPEC:79 ("The only command changes are the small fixes"), SPEC:84 and SPEC:87 ("Small fix: None"), SPEC:195 (AC-1.1 covers all of 3.1).
- Why Medium: the scope sentence at SPEC:159 names all 37, so one reading adds them in P1; the Commands column and SPEC:79 point the other way. See the Quantity Flow Diagram. Recommendation: add the two names to the P1 Commands column. Priority: Medium.

### M-10 (MAJOR as labelled, graded Medium): several contract requirements have no acceptance check

- WC-3 (`ask` route, SPEC:61) is never exercised: AC-2.2 (SPEC:200) tests a blocked contract and `agentWait`, not the `ask` and reply path. WC-12 (SPEC:70, `check` before `worker_done`, `consumer_fenced`) has no check. WC-1 (SPEC:59) is covered only by the `state: ready` pass at SPEC:180. WC-7 (SPEC:65, no subagent wrapper) is checked only in P0 (SPEC:194), not in P1-P4's 7.2 loop. WC-11 (SPEC:69) is checked only for save (SPEC:207).
- Why Medium: a missing test, not a stated text that does harm. Wiegers/Crispin. Recommendation: add one 7.2 step per untested WC, or say which are review-only. Priority: Medium.

## === ARCHITECTURE ANALYSIS === (Fowler lead, Newman, Hohpe, Nygard)

### M-4 (MAJOR as labelled, graded Medium): heartbeat duty versus Agent-tool fan-out waits

- Texts: SPEC:68 (WC-10: heartbeat "every 5 minutes"; split only "a single tool call" longer than 5 minutes, "a poll wait, a long eval"), SPEC:65 (WC-7: lifecycle messages "only by that top-level session, never by a subagent"), SPEC:24 (E4: a command's Agent-tool fan-out stays as it is), `INV-A:42` (cleanup-audit: waves of 7-8 Task agents per pass).
- A top-level session blocked in one Task call for a long wave cannot heartbeat and cannot be split into 4-minute waits. Whether a missing heartbeat changes Orca's liveness is itself UNVERIFIED (`CAPS:182` item 7, `CAPS:130`), and absence of signal never authorizes stop (`CAPS:125`). So the harm is a coordinator that sees silence and may mis-act, which needs a guess.
- Recommendation: say how long fan-out commands are covered (for example, the coordinator treats Task-wave silence as normal up to a stated bound). Nygard/Hohpe. Priority: Medium.

### M-5 (MAJOR as labelled, graded Medium): three different thresholds for the same wait rule

- Texts: SPEC:68 (trigger "longer than 5 minutes", waits "at most 4 minutes"), SPEC:114 (pr-submit: each iteration "stays under 4 minutes"), SPEC:210 (AC-4.3: "no single tool call exceeds 240 s"), SPEC:266 (Decision: 4 minutes "leaves a margin").
- A call of 250 s is permitted by the trigger and rejected by AC-4.3. Why Medium: an implementer following WC-10 could fail AC-4.3 only for waits between 240 s and 300 s, and the harm is a failed check, not a wrong outcome. Recommendation: state the trigger as 240 s. Priority: Medium.

### M-7 (MAJOR as labelled, graded Medium): section 1.4 point 2 is stated as fact but rests on an inference that `CAPS:47` weakens

- Texts: SPEC:44 ("A command's own `AskUserQuestion` or chat question comes *after* readiness, so it does not fail `worker-start`"). `CAPS:47`: for Claude the task "is passed on the command line, not typed" (`promptInjectionMode: 'argv'`), and readiness waits for a fresh input box or idle TUI (`CAPS:47`). With an argv prompt, the command may start before Orca sees the box idle. `CAPS:49` and `CAPS:52` show a pre-readiness question failing and a post-`input_accepted` `ask` being healthy; neither shows a command prompt on the first argv turn.
- UNVERIFIED: whether a first-turn gate fails `worker-start`. If it does, AC-2.2's "worker-start exit 0" (SPEC:180, SPEC:200) fails for gate-trigger runs. Why Medium: the spec elsewhere handles the stall case (SPEC:44 last sentence), so no stated text builds a wrong thing. Recommendation: mark the sentence UNVERIFIED and let AC-0.4 test it. Priority: Medium.

### M-8 (MAJOR as labelled, graded Medium): P0 checks use features that only arrive in P1

- Texts: SPEC:73 (brief includes "the exact command line including `--unattended`"), SPEC:180 (step 1 task brief "per section 2.3"), SPEC:182 (step 3: "its report path is the WC-4 contract path"), SPEC:194 (AC-0.4 command lines have no `--unattended`; "step 4 uses the command's existing report file, since the contract arrives in P1"), SPEC:159 (P1 adds the flag and the contract).
- AC-0.4 says steps 1-3 and 5-7 pass, but step 3's last clause names a WC-4 contract that does not exist yet. The obvious reading drops the clause; one more sentence would remove the doubt. Also, for adversarial the existing contract filename is not fixed (SPEC:83, `INV-A:60`), so the P0 report path is not predictable. Priority: Medium.

### M-9 (MAJOR as labelled, graded Medium): `--unattended` next to a person-mode flag is refused for some commands and silent for others

- Texts: SPEC:60 (WC-2: under `--unattended` the command never calls `AskUserQuestion`), SPEC:83-84 and SPEC:89 (adversarial, brainstorm, release-split: "never `--interactive`" is a brief rule), SPEC:103, SPEC:110, SPEC:118 (cleanup, improve, roadmap: `--interactive` refused).
- WC-2's general sentence already settles the winner, so this is a missing per-command line, not a contradiction. Priority: Medium.

### M-11 (MAJOR as labelled, graded Medium): "new flags" versus the additive-diff check

- Texts: SPEC:149 (SA-4: edits are "a new `## Unattended mode` section and new flags"), SPEC:176 (AC-C5: `git diff -U0 ... | grep -E '^-[^-]'` must print nothing). Adding `--unattended` or `--output` to an existing Usage line deletes the old line in the diff and trips AC-C5. The text allows keeping flags only in the new section, so an implementer may avoid it. Priority: Medium. Recommendation: say where new flags are documented.

### M-12 (MAJOR as labelled, graded Medium): the shared contract file is a single point of failure with no stated fallback

- Texts: SPEC:52 (each command "points to the installed contract path"; shared rules written once), SPEC:158 (the file also carries the brief template and the 3.1 flag list).
- If `~/.claude/WORKER-CONTRACT.md` is absent (a dev checkout without a reinstall, or an older install), the command has only its own short section and no WC-2/WC-4 rules; no text says what it does then. Also the per-command flag list is kept in both the contract's brief template and each command's section (Fowler: two sources for one fact). Priority: Medium. Recommendation: say that a command which cannot read the contract falls back to `status: blocked` with that reason, and keep the flag list in one place.

### M-13 (MAJOR as labelled, graded Medium): the live check waits without an upper bound

- Texts: SPEC:182 (step 3: `check --wait ... --timeout-ms 900000` "until `worker_done` arrives"). `CAPS:125-126` say leave a wait only on positive proof; SPEC:282 records that Orca's total Dispatch time is UNVERIFIED. A hung command makes the acceptance run unbounded. Priority: Medium. Recommendation: add a stated maximum wall-clock and what to record when it is hit.

### M-14 (MAJOR as labelled, graded Medium): three evidence claims go further than their cited lines

- SPEC:67 and SPEC:133 cite `README:31` as the reason outward actions are off and for "need the user's authorization in this repo"; `README:31` is a rule for workers in this run only. `INV-A:91` itself words it as "this run forbids commits/pushes".
- SPEC:23 (E3) cites `invocation_method: "skill-direct"` as support for "it has worked before"; SPEC:43 says the same run "proves the nested route, not the direct route". Which route "skill-direct" denotes cannot be checked here (UNVERIFIED).
- SPEC:76 says "The 43 commands in `cmd/`". Both inventories scope themselves by an explicit brace list (`INV-A:3`, `INV-B:3`), not by a directory listing. The skill roster visible to this reviewer also includes /sc:graph, /sc:impact and /sc:issue, which neither inventory covers. UNVERIFIED whether they exist in `cmd/`; if they do, they have no verdict, no phase and no AC-1.1 coverage.
- Why Medium: each is an overstatement that a reader could mis-take, not a requirement that builds the wrong thing. Priority: Medium.

### M-15 (MAJOR as labelled, graded Medium): auggie-review needs a `--post-pr` flag the inventories do not show

- Texts: SPEC:100 ("posting returns only with an explicit `--post-pr` in the brief"; "Other required change: none"), SPEC:67 (WC-9: outward actions turn on "through the command's own explicit flag"). `INV-A:38` lists only `--no-post-pr` and `--no-remediation-offer`; it shows no positive `--post-pr`. If the flag does not exist, "other required change: none" is wrong. UNVERIFIED (the command file is not in this sandbox). Priority: Medium.

## === ADVERSARIAL ANALYSIS (Whittaker) ===

Review order: after Fowler and Nygard. Scope: specification correctness only. Each finding uses the required template.

- **A-1 (Zero/Empty Attack), CRITICAL as labelled, same defect as B-1.** I can break this specification by **Zero/Empty Attack**. The invariant at **SPEC:62** ("known before dispatch", `<output-dir>` is a directory) fails when **the brief passes a file-valued `--output` or no directory at all**. Concrete attack: **before: brief `/sc:tdd "auth" --unattended --output docs/TDD_AUTH.md`, no directory exists; after: the command resolves `<output-dir>` = `docs/TDD_AUTH.md`, writes `docs/TDD_AUTH.md/return-contract.yaml` (parents created), the directory now occupies the TDD's own path, the later TDD write fails, and the coordinator opens a path it never computed.** Graded blocking as B-1.
- **A-2 (Zero/Empty Attack), MAJOR, graded Medium (M-12).** I can break this specification by **Zero/Empty Attack**. The invariant at **SPEC:52** (shared rules live in `~/.claude/WORKER-CONTRACT.md`) fails when **the file is not installed**. Concrete attack: **before: command updated, contract file not yet installed; after: the command reads only its short section, has no WC-4 field list, writes a contract with wrong or missing fields, and AC step 4 (SPEC:183) fails or passes on a malformed file.**
- **A-3 (Divergence Attack), MINOR (n-5).** I can break this specification by **Divergence Attack**. The invariant at **SPEC:63** (`partial` maps to `succeeded`) fails when **the partial run left an unusable deliverable (for example a half-applied cleanup)**. Concrete attack: **before: cleanup applies 3 of 7 items then stops with status `partial`; after: `worker_done --outcome succeeded`, the coordinator releases the worker and proceeds on a half-applied tree.** Mitigated by SPEC:73 (the coordinator opens the report) and the first-sentence rule, so MINOR.
- **A-4 (Sequence Attack), MAJOR, graded Medium (M-1).** I can break this specification by **Sequence Attack**. The invariant at **SPEC:63** ("no report exists" means failed) fails when **a retry worker runs in a directory that already holds the first attempt's contract**. Concrete attack: **before: attempt 1 wrote `status: blocked`; retry crashes at start; after: no new contract is written, `test -s` passes on the old file, and the coordinator reads `blocked` for a retry that never ran.**
- **A-5 (Sentinel Collision Attack), MINOR (n-6).** I can break this specification by **Sentinel Collision Attack**. The invariant at **SPEC:63** (contract `blocked` becomes Orca `--outcome failed`) fails when **a coordinator reads `blocked` as Orca's own Task status**. `CAPS:89` lists `blocked` as a Task status meaning unmet dependencies, while the spec's `blocked` means "waiting for an answer"; after `worker_done --outcome failed` the Task shows `failed` and its dependents stay blocked (`CAPS:90`). Concrete attack: **`task-list --status blocked` returns none of the workers that need answers, which sit under `failed`.**
- **A-6 (Accumulation Attack), MAJOR, graded Medium (M-4).** I can break this specification by **Accumulation Attack**. The invariant at **SPEC:68** (heartbeat every 5 minutes) fails when **Task-call waits accumulate past 5 minutes**. Concrete attack: **cleanup-audit runs 4 waves of about 3 minutes each inside one Task-heavy turn; no heartbeat is possible (SPEC:65); the coordinator sees 12 minutes of silence.**
- **A-7 (Accumulation Attack), MINOR (n-7).** The invariant at **SPEC:69** (default paths "carry a timestamp or the slug") fails when **two workers start in the same second with the same slug**. Concrete attack: **two `/sc:analyze` workers with a second-resolution timestamp name the same report path.**

## Quality scores (0-10)

| Dimension | Score | Why |
|---|---|---|
| Clarity | 7 | Terms, ID scheme and rationale are clear; the contract location is not (B-1, M-2) |
| Completeness | 7 | All 43 commands get a verdict; two commands are missing from the phase list (M-6), several requirements have no check (M-10) |
| Testability | 6 | Most requirements have a runnable check; B-1 and B-2 make two checks unrunnable |
| Consistency | 5 | Two direct contradictions (B-1, B-2) and several smaller thresholds and counts that disagree |

## Expert consensus and disagreements

- Consensus: the decision (Orca coordinates, commands stay units of work), the rejection of commands calling Orca (R1-R5), the `--unattended` flag, and the standalone-unchanged rule (SA-1) are well supported by `CAPS` and the inventories. No expert found a defect in them.
- Consensus: the blocking problems are in the contract's own wording (WC-4) and in the acceptance set, not in the architecture.
- Disagreement: Fowler would move the coordinator brief template out of the core file (M-12); Hohpe would accept it there for discoverability. Left to the author.
- Sequence: Wiegers (B-1, B-2, M-3, M-10), Adzic (no concrete sample of a contract; n-8), Cockburn (B-2), Fowler (M-12, M-6), Nygard (M-1, M-4, M-13), Whittaker (section above), Newman (no `contract_version` field in WC-4, n-8), Hohpe (M-4, `ask` answer-to-flag mapping is free text, n-9), Crispin (M-10), Gregory (README:31 reuse, M-14), Hightower (no new finding).

## Follow-up candidates (Medium and minor; never trigger a revision)

Medium (warnings): M-1, M-2, M-3, M-4, M-5, M-6, M-7, M-8, M-9, M-10, M-11, M-12, M-13, M-14, M-15 (each described above, with its recommendation).

Minor notes:

- n-1: a call of exactly 300 s is neither split nor heartbeat-covered (SPEC:68).
- n-2: init-lite and index-repo re-runs overwrite in place, a third resume mechanism not in WC-6 (SPEC:64, SPEC:86-87).
- n-3: behavior when `--unattended` is passed to a section-4 command is not stated (SPEC:128).
- n-4: WC-1 says "well inside" the readiness limit with no number (SPEC:59), though its own evidence shows a 30 s fallback passing and about 45 s failing (`CAPS:49`).
- n-5: `partial` maps to `succeeded` (A-3).
- n-6: contract `blocked` and Orca Task `blocked` share a word (A-5).
- n-7: same-second timestamp collisions (A-7).
- n-8: WC-4 has no `contract_version` field and no sample YAML, which would have exposed B-1.
- n-9: the coordinator's `reply` text is free form; how it becomes a flag value at SPEC:61 is not stated.
- n-10: "Phases 1-3 need no user decision" (SPEC:154) next to D1 and D4 being open decisions that touch P1 and P2 commands (SPEC:51, SPEC:244); SPEC:225 resolves it by "proceed on the recommendations".
- n-11: AC step 5 (SPEC:184) searches a transcript for `AskUserQuestion`, which the skill text a worker reads also contains (for example `INV-B:239` quotes "never AskUserQuestion"); the pass condition says "no call", so read it as a tool call.
- n-12: review-translation's "pre-confirmed context input" (SPEC:117) has no flag name.

The session that ran this review asks the user once per loop whether to open an issue for the follow-up candidates and creates none without the answer. This run cannot ask; the coordinator should put the question.

## Brief clauses overridden

None. The brief narrowed the scope to this report file and to `inventory/` as the checkable evidence; this review followed both. No brief clause graded a minor finding as blocking or authorized an edit.

## Reviser brief

Blocking finding ids: **B-1, B-2**. Nothing else may be revised.

Reviser contract (restated from the command's Review Loop, bullet 6): revise only text a blocking finding names; add no rule, mechanism or section that no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id. Leave Medium and minor findings alone. Return the candidate once and do not award yourself a PASS.

Findings, copied from this report:

- **B-1.** Texts: SPEC:62 ("`<output-dir>` is the directory the coordinator passed (`--output` / `--output-dir`)", "known before dispatch"); SPEC:87 (init-lite brief: `--output <file>`); SPEC:90 (tdd brief: `--output <file>`); SPEC:200 (tdd gate-trigger check with `--output <file>` expecting a blocked contract); SPEC:183 (`test -s <contract>`). Stated wrong outcome: for tdd and init-lite no directory is passed, so the contract path is undefined or lands below a regular file, and AC-2.2 and step 4 cannot pass.
- **B-2.** Texts: SPEC:112 (load: report "none", "not as its own Task", P1); SPEC:265 ("a report file would be an unrequested addition"); SPEC:159 (P1 includes load); SPEC:196 (AC-1.2 runs each P1 command live); SPEC:182-183 (steps 3-4 need the WC-4 contract path and `test -s <contract>`); SPEC:195 (AC-1.1). Stated wrong outcome: AC-1.2's live check cannot pass for load as specified, and giving load a contract breaks SPEC:112 and SPEC:265.

verdict: FAIL

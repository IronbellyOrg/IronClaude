review: 1 of 3

# Spec-panel report, round 1: orca-worker-contract-spec

- command: `/sc:spec-panel @.dev/orca-command-refactor/specs/orca-worker-contract-spec.md --mode critique --focus requirements,architecture`
- candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md` (285 lines)
- candidate sha256: `d3cdbe573e57303b9ce6c93d1fe98ba18fb7cb1a15773d926bf6a0c31425200d`
- baseline: none (first review of the full document; no `--re-review` and no `--baseline` given)
- reviewer model actually used: claude-sonnet-5-5
- format: standard (default); input type: neither TDD nor PRD (9 numbered headings, no TDD frontmatter), so no `target_release` question applies
- prompt followed: FIRST-REVIEW prompt of `~/.claude/rules/prompts/document_review_loop_prompts.md` (read in full, lines 1-68), with its grading check applied to every finding below

## Citation legend

All paths are relative to the workspace root. A citation of a file that is not in the workspace is marked UNVERIFIED.

- `SPEC:N` = `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md` line N
- `README:N` = `.dev/orca-command-refactor/README.md` line N
- `INV-A:N` = `.dev/orca-command-refactor/inventory/commands-a.md` line N
- `INV-B:N` = `.dev/orca-command-refactor/inventory/commands-b.md` line N
- `CAPS:N` = `.dev/orca-command-refactor/inventory/orca-capabilities.md` line N
- `CMD:N` = `command.md` (the `/sc:spec-panel` definition) line N

## Findings index

| id | grade | label | bucket | lead expert | SPEC location |
|---|---|---|---|---|---|
| B-1 | blocking | CRITICAL | requirements | Wiegers / Fowler | SPEC:159, 195, 112, 240, 84, 87 |
| B-2 | blocking | MAJOR | requirements | Adzic / Whittaker | SPEC:62, 73, 83, 87, 90, 92, 120, 182, 198 |
| B-3 | blocking | MAJOR | requirements | Nygard / Whittaker | SPEC:64, 62, 205, 100-125 |
| M-1 | Medium | MAJOR | architecture | Nygard | SPEC:68 |
| M-2 | Medium | MAJOR | requirements | Wiegers | SPEC:62-63, 262-263 |
| M-3 | Medium | MAJOR | architecture | Newman / Hohpe | SPEC:122, 51 |
| M-4 | Medium | MAJOR | requirements | Whittaker | SPEC:51, 228 |
| M-5 | Medium | MAJOR | requirements | Adzic / Whittaker | SPEC:60, 62, 102-123 |
| M-6 | Medium | MAJOR | architecture | Nygard | SPEC:61, 200 |
| M-7 | Medium | MAJOR | architecture | Newman | SPEC:44 |
| M-8 | Medium | MAJOR | requirements | Crispin | SPEC:172, 176, 193 |
| M-9 | Medium | MAJOR | architecture | Fowler | SPEC:159-160, 67 |
| M-10 | Medium | MAJOR | requirements | Wiegers | SPEC:88, 67, 69 |
| M-11 | Medium | MINOR | requirements | Whittaker | SPEC:69, 85-87 |
| N-1 | minor | MINOR | requirements | Cockburn | SPEC:23, 43 |
| N-2 | minor | MINOR | requirements | Wiegers | SPEC:67, 133 |
| N-3 | minor | MINOR | requirements | Crispin | SPEC:172 |
| N-4 | minor | MINOR | requirements | Crispin | SPEC:202 |
| N-5 | minor | MINOR | requirements | Crispin | SPEC:184 |
| N-6 | minor | MINOR | architecture | Fowler | SPEC:252 |
| N-7 | minor | MINOR | architecture | Newman | SPEC:122, 271-285 |

Blocking findings: B-1, B-2, B-3. Medium and minor findings are listed again under `follow-up candidates`.

## Panel

Seated by the focus areas: Wiegers (lead), Adzic, Cockburn (requirements); Fowler (lead), Newman, Hohpe, Nygard (architecture). Whittaker is active in every review (CMD:83). Crispin is seated only for the Guard Condition Boundary Table (CMD:315). Reviewed in the fixed order of CMD:101-113: Wiegers, Adzic, Cockburn, Fowler, Nygard, Whittaker, Newman, Hohpe, Crispin. Gregory and Hightower are not seated: neither is named by the focus areas or by a mandatory artifact.

What the panel agrees on:

- The decision (Orca coordinates, commands stay units of work, SPEC:16, 28-39) is consistent with the evidence in the inventories, and section 1.4 states its own evidence gaps honestly (SPEC:41-45).
- The counts reconcile: 10 ready + 27 needs-change + 6 coordinator-only = 43 (SPEC:76) matches INV-A:73 (5/13/3) plus INV-B:278 (5/14/3). Section 3.2 has 27 rows, section 4 has 6, section 3.1 has 10.
- The inventory and Orca-fact citations in SPEC:21-45 and 59-70 that were spot-checked against the inventories (`INV-A:13,35,60,62,65,76-83,90,94-98`, `INV-B:272,285-286,289-299,323`, `CAPS:44-45,52,58-61,64,66-67,72-77,79,86,92,97-103,107-116,129-130,145-150,155-161,186-188`, `README:12,30,31`) were all found as cited.
- Disagreement: none recorded among the panel on the three blocking findings.

## === REQUIREMENTS ANALYSIS ===

### B-1 (blocking, CRITICAL). The Phase 1 acceptance check AC-1.1 cannot pass as scoped, and two ready commands sit in no phase

Experts: Wiegers (traceability), Fowler (count annotation, Pipeline Dimensional Analysis).

Grading check. An implementer who follows the stated text as written builds Phase 1 as the row at SPEC:159 lists it (nine no-gate commands plus fixes to adversarial, cleanup-audit, index-repo, workflow), and then runs AC-1.1 (SPEC:195), which asserts that every command in sections 3.1-3.2 has a `## Unattended mode` section naming `return-contract.yaml`. That is wrong because AC-1.1 cannot pass: 37 commands are asserted, and these are among them although Phase 1 does not give them the section or cannot give it one:

- `/sc:load` gets no report file at all (SPEC:112, "Report: none", "use it as a step inside another worker's brief"), so its section cannot name `return-contract.yaml`.
- `/sc:pr-submit` is Phase 4 (SPEC:114, 162), and D3 option (a), the recommendation, says "no pr-submit changes in Phase 4" (SPEC:240) while "Phases 0-3 can proceed on the recommendations" (SPEC:225).
- The Phase 2, 3 and 4 commands (SPEC:160-162) are not edited in Phase 1.
- `/sc:brainstorm` and `/sc:init-lite` appear in section 3.1 with "Small fix: None" (SPEC:84, 87) and in no phase row (SPEC:158-162), yet AC-1.1 asserts they carry the section.

SPEC:154 ("Later phases do not start until the earlier phase's checks in section 7 pass") then stops Phase 2 from starting. The sentence at SPEC:159 ("the `--unattended` flag accepted by every command in sections 3.1 and 3.2") and the command list in the same row (SPEC:159) also disagree, so no reading makes AC-1.1 and the phase table both true.

Quantity Flow Diagram (Pipeline Dimensional Analysis, triggered by the 43 -> classification -> phase flow; FR-19 mismatch):

```text
[Inventories: 21 (INV-A:3) + 22 (INV-B:3)] --> [43 commands, SPEC:76]
   |--> [3.1 ready: 10, SPEC:81-92]  --> P1 fixes 4 (adversarial, cleanup-audit, index-repo, workflow; SPEC:159)
   |                                 --> P2 4 (reflect, release-split, tdd, troubleshoot; SPEC:160)
   |                                 --> NO PHASE 2 (brainstorm SPEC:84, init-lite SPEC:87)  <-- MISMATCH 10 in, 8 out
   |--> [3.2 needs change: 27, SPEC:97-125] --> P1 9 + P2 11 + P3 4 + P4 3 = 27 (consistent)
   |--> [section 4: 6, SPEC:130-137] (no mode, SPEC:128)
[AC-1.1 consumer, SPEC:195: expects section in 37 commands at the end of P1]  <-- MISMATCH vs at most 13 edited in P1 (9 + 4)
```

Recommendation and rationale. Narrow AC-1.1 so it asserts only the commands that the Phase column assigns to the phase being checked or an earlier one, excluding `/sc:load` (no contract) and `/sc:pr-submit` until D3 is answered, and give `brainstorm` and `init-lite` a phase (or state that they receive the section in P1). Narrowing removes the deadlock without adding a mechanism. Priority: High. Quality impact: Testability +2.

### M-2 (Medium, MAJOR). `partial` is undefined and it decides the Orca outcome; "keep their fields" can conflict with the fixed status set

Expert: Wiegers. WC-4 fixes four statuses (SPEC:62) and WC-5 maps `partial` to `--outcome succeeded` (SPEC:63, 263), but no text says when a run is `partial` rather than `blocked` or `failed`. The `cleanup` row has deferred "Approval Required" items listed unapplied (SPEC:103) and does not say which status that is; a `partial` there makes the Task `completed` and unblocks dependents (CAPS:142-144), a `blocked` makes it `failed`. WC-4 also says commands with an existing contract "keep their fields" (SPEC:62) while 7.2 step 4 asserts `status` is one of the four values (SPEC:183); the status vocabularies of the existing contracts (workflow, brainstorm, reflect, adversarial) are not read in the evidence (INV-B:272 lists only `status`, `plan_path`, `reflect_report_path`). This is a requirement the document never states, so it is Medium. Recommendation: define `partial` in one sentence and state whether an existing `status` field is replaced or mapped. Priority: Medium.

### M-4 (Medium, MAJOR). No rule for how `--unattended` is recognised when the same text can appear in free-text input

Expert: Whittaker (Sentinel Collision Attack). I can break this specification by **Sentinel Collision**. The invariant at **SPEC:51 and SPEC:228 (explicit `--unattended` flag "cannot misfire on a person")** fails when **the token appears inside the free-text argument of a command that takes a prompt**. Concrete attack: before state, a person runs `/sc:troubleshoot "login fails when --unattended is set"` in a plain session, expecting SA-1 behaviour (SPEC:146); after state, a command that scans its argument string for `--unattended` switches to the no-prompt mode, resolves its gates by default (SPEC:60) and applies WC-9 defaults. The same collision runs the other way for a coordinator that quotes a user request containing the word. The text does not say the flag must be a standalone token outside any quoted argument (the command definition under review does say so, CMD:459). Medium because it needs the implementer to pick a naive parse. Recommendation: add the one-line token rule to D1(a). Priority: Medium.

### M-5 (Medium, MAJOR). Outcome of a "refused" option and of a missing output directory is not specified

Experts: Adzic, Whittaker (Zero/Empty Attack). WC-2 lists three resolutions (default, caller flag, blocked; SPEC:60) but section 3 also uses "refused" for `--interactive`, `--mode socratic`, `--format interactive`, `--watch`, `--monitor 1` (SPEC:102-103, 108, 110, 114, 118, 123), and nothing says whether a refusal writes a contract (WC-4 says every outcome, SPEC:62) or only prints. The Zero/Empty case is also open: `--unattended` without an output directory. I can break this specification by **Zero/Empty Attack**. The invariant at **SPEC:62 (the contract is written on every outcome into the directory the coordinator passed)** fails when **the brief omits `--output`** (SPEC:73 makes the brief responsible but no command rule exists). Concrete attack: `/sc:cleanup <dir> --unattended` without `--output`: the command applies its auto-fix edits (SPEC:103), has nowhere to write the contract, the worker finds no report and sends `--outcome failed` (SPEC:63) after the edits are already in the tree. Medium because it needs a coordinator error. Recommendation: one sentence that a command in unattended mode with no output directory stops before any change, and that a refusal writes `status: failed` with the reason. Priority: Medium.

### M-10 (Medium, MAJOR). `/sc:reflect` keeps two default-on writes under `--unattended`

Expert: Wiegers. The reflect row passes `--no-promote` only "when the coordinator owns folder moves" (SPEC:88), but the inventory shows a default-on UC-2 folder move and a write to the tracked file `docs/memory/reflect/deviation-patterns-<slug>.md` (INV-B:114). WC-9 turns off pushes, PRs, posts, installs, provisioning and paid runs (SPEC:67) and WC-11 bars two workers writing one file (SPEC:69); a folder move of a tracked work unit is neither listed nor excluded, so an unattended worker moves it by default. The harm needs the brief to omit the flag, so Medium. Recommendation: say whether `--unattended` implies `--no-promote`. Priority: Medium.

### N-1 (minor). E3 cites `invocation_method: "skill-direct"` as support while section 1.4 says the PR #329 run proves only the nested route

Expert: Cockburn. SPEC:23 uses the return contract (`skill-direct`, INV-A:13, UNVERIFIED file) as evidence that workers ran the command, and SPEC:43 says the brief told workers to use an Agent-tool subagent (CAPS:156). The two readings of the same run are not reconciled. No consequence for the decision because section 1.4 names the gap and Phase 0 tests it. Note only.

### N-2 (minor). A run-specific rule is cited as general policy

Expert: Wiegers. `README:31` ("No git commits, pushes, PRs or GitHub comments") applies to workers of this planning run (README:29-31). SPEC:67 and SPEC:133 cite it for the permanent WC-9 and for `/sc:git` being coordinator-only. The conclusions are supported by other evidence (the repo's PR rule, SPEC:239 and `CLAUDE.md:50`, UNVERIFIED), so a note only.

### N-3 (minor). AC-C1 as written in a markdown table

Expert: Crispin. SPEC:172 shows the alternation as `\|` and the pipes as `\|`, which are table escapes; copied raw, `grep -E` treats `\|` as a literal pipe and the check prints nothing for every input.

### N-4 (minor). AC-2.4 counts only the first page and only two comment kinds

Expert: Crispin. `gh api ... --jq length` (SPEC:202) counts one page (default 30 items) and ignores plain issue comments on the PR.

### N-5 (minor). Step 5 of the live check can match its own brief

Expert: Crispin. SPEC:184 searches the transcript for `AskUserQuestion`; a brief that tells the worker never to call it (SPEC:60, 73) puts the word in the transcript.

## === ARCHITECTURE ANALYSIS ===

### B-2 (blocking, MAJOR). WC-4's contract location contradicts the rows and checks that depend on it

Experts: Adzic (concrete examples), Whittaker (Divergence Attack).

Grading check. An implementer who follows the stated text as written builds, for `/sc:adversarial --output <dir>`, a contract at `<dir>/return-contract.yaml` (WC-4: `<output-dir>/return-contract.yaml`, SPEC:62), while the section 3.1 row and AC-1.4 put it at `<output>/adversarial/return-contract.yaml` (SPEC:83, 198), and the live check requires the `worker_done --report-path` to equal "the WC-4 contract path" (SPEC:182). One run cannot satisfy both texts. Three more instances of the same contradiction:

- `/sc:workflow` writes `.dev/tasks/to-do/<id>/return-contract.yaml` (SPEC:92), an id generated at run time, so the path is not "known before dispatch" (WC-4 title; SPEC:73).
- `/sc:init-lite`, `/sc:tdd` and `/sc:spec-panel` take `--output` as a file (SPEC:87, 90; spec-panel's new `--output`, SPEC:120). WC-4 defines `<output-dir>` as "the directory the coordinator passed (`--output` / `--output-dir`)" (SPEC:62), so read literally the contract path is `<file>/return-contract.yaml`, which cannot exist. The P2 check that exercises it (`/sc:tdd "auth" --unattended --output <file>`, SPEC:200) has no defined contract path to test.
- `/sc:cleanup-audit` and `/sc:index-repo` write fixed locations (SPEC:85-86).

Recommendation and rationale. Narrow WC-4 to "at `<output-dir>/return-contract.yaml` unless the command's row names another path", add a "Contract path" cell to the rows that differ (adversarial, workflow, cleanup-audit, index-repo), and for the three file-valued `--output` commands state one rule (for example a named report directory flag). Narrowing keeps the one-name decision (SPEC:261) and removes the contradiction. Priority: High. Quality impact: Consistency +2, Testability +1.

### B-3 (blocking, MAJOR). WC-6's "fresh output directory" contradicts WC-4 and the Phase 3 check AC-3.2

Experts: Nygard (failure and recovery), Whittaker (Sequence Attack).

Grading check. An implementer who follows the stated text as written builds `/sc:roadmap` so that, given `--output <dir>` where `<dir>/.session-memory.md` already exists and no resume flag, it "starts fresh" in `<dir>` (AC-3.2, SPEC:205). That is wrong because WC-6 says a retry worker must not corrupt the first attempt's output and offers only two ways: resume, or write each run into a fresh output directory (SPEC:64). A fresh start inside the same `<dir>` overwrites the first attempt's `roadmap.md`, `extraction.md` and session memory, and WC-4 forbids the command from choosing a different directory because the coordinator passed it and the report path must be known before dispatch (SPEC:62, 73). Section 2.3 does not tell the coordinator to pass a new directory on `--retry-of` (SPEC:72-73), and 22 rows say "fresh dir" (SPEC:99-125) without saying who makes it fresh.

I can break this specification by **Sequence Attack**. The invariant at **SPEC:64 (WC-6)** fails when **a Task is retried with the same brief**. Concrete attack: before, `<dir>` holds attempt 1's `roadmap.md` and a contract with `status: blocked`; the coordinator reuses the brief with `--retry-of` (CAPS:116) and the same `--output <dir>`; the command starts fresh as AC-3.2 requires; after, attempt 1's deliverable and contract are replaced, and if attempt 2 also stops, no output of attempt 1 survives.

Recommendation and rationale. Add one sentence to section 2.3 that a retry brief must pass a new output directory, and change AC-3.2 to use a new `<dir>` for the fresh-start case (or a copy of the old one). This deletes the conflict without a new mechanism. Priority: High. Quality impact: Completeness +1.

### M-1 (Medium, MAJOR). WC-10 cannot be met for Agent-tool fan-out calls and has a gap between its two numbers

Expert: Nygard. WC-10 says a step that blocks one tool call longer than 5 minutes "must be split into waits of at most 4 minutes" (SPEC:68), and AC-4.3 tests only pr-submit (SPEC:210). The commands whose main time is spent in one Agent-tool fan-out call (tdd, adversarial, cleanup-audit, reflect Tier 2; SPEC:24) block the top-level session in a single call that cannot be split, so the worker cannot heartbeat. Whether a missed heartbeat changes Orca's liveness verdict is UNVERIFIED (SPEC:282, CAPS:130, CAPS:188). Also a wait of 4.5 minutes is not required to split (trigger "longer than 5") yet exceeds the "at most 4 minutes" rule. Medium because no stated text yields a known wrong build. Recommendation: say that fan-out calls are exempt (or what the worker does), and use one number in both places. Priority: Medium.

### M-3 (Medium, MAJOR). `--unattended` is passed down only for tasklist to reflect

Experts: Newman, Hohpe. The tasklist row says Stage 10.5 passes `--unattended` to each reflect (SPEC:122), but no general rule says a command in unattended mode passes the mode to every `/sc:` command or skill it invokes. The inventories show the nesting: brainstorm to adversarial (INV-A:39), release-split to brainstorm and adversarial (INV-B:119, 121), tdd to task (INV-B:219), workflow to reflect (INV-B:269), roadmap to adversarial and `sc:save` (INV-B:151, 154), task to troubleshoot (INV-B:201). `/sc:roadmap` writes memory through `sc:save` at every wave (INV-B:154), and WC-11 says single-owner memory keys are not written in unattended mode (SPEC:69); only the save row (SPEC:119) fixes that, and only if roadmap's internal call carries the mode. Medium because the harm needs the implementer to omit the propagation. Recommendation: one sentence in section 2.1 that a nested invocation inherits `--unattended`. Priority: Medium.

### M-6 (Medium, MAJOR). `ask` retries are unbounded and AC-2.2 contradicts the optional `ask` path

Expert: Nygard (Accumulation Attack). WC-3 lets the worker ask once and, on timeout, resume the same message ID (SPEC:61) with no cap and no rule for a coordinator that never answers, and the blocked Task then waits forever. AC-2.2 requires `worker_done --outcome failed` with `status: blocked` for a gate-hit run (SPEC:200), but WC-3 lets the worker ask instead, which ends differently; the brief template (SPEC:73) does not say whether `ask` is allowed. Medium: needs a guess about which reading the worker takes. Recommendation: state in the brief template whether `ask` is permitted and the maximum number of resumes. Priority: Medium.

### M-7 (Medium, MAJOR). The claim that a command's own question comes "after readiness" ignores argv prompt injection

Expert: Newman. SPEC:44 says a command's `AskUserQuestion` "comes after readiness, so it does not fail `worker-start`". CAPS:47 records that for Claude the task is passed on the command line (`promptInjectionMode: 'argv'`), so the command runs while Orca is still waiting for the input box; whether a command whose first action is a prompt reaches `input_accepted` is not shown, and it is not on the UNVERIFIED list (SPEC:271-285). The conclusion does not change under `--unattended` (no prompts), so Medium. Recommendation: mark the claim UNVERIFIED and add it to the Phase 0 smoke run. Priority: Medium.

### M-9 (Medium, MAJOR). After Phase 1, commands accept `--unattended` while their gates and outward defaults are still unconverted

Expert: Fowler. SPEC:159 has every command accept the flag in Phase 1 ("a no-op where a command has no gate") and SPEC:160 converts the gates in Phase 2. Between the two phases `/sc:auggie-review <PR> --unattended` is accepted and, per its row, still posts to GitHub and then offers remediation (SPEC:100, WC-9 at SPEC:67), so a coordinator that trusts the flag gets a stall or an outward post. AC-1.2 tests only gate-free commands (SPEC:196). Medium because it needs a coordinator to dispatch between phases. Recommendation: have Phase 1 accept the flag only on gate-free commands, or refuse it on gate-bearing ones until their phase. Priority: Medium.

### N-6 (minor). Wording in D5

Expert: Fowler. SPEC:252 says raising depth would "break R1's protection against runaway fan-out", but R1 (SPEC:33) is a reason against the rejected design, not a protection. No effect on the decision.

### N-7 (minor). Tasklist nesting claim drops its UNVERIFIED flag

Expert: Newman. The tasklist row says its reflect fan-out is "inside Claude Code's nesting limit, `INV-A:14`" (SPEC:122), while the inventory marks nested spawning there UNVERIFIED (INV-B:210, 314, 322) and the spec's own UNVERIFIED list (SPEC:271-285) has no entry for it.

## === ADVERSARIAL ANALYSIS (Whittaker) ===

Attacks used: Zero/Empty (M-5), Divergence (B-2), Sentinel Collision (M-4), Sequence (B-3), Accumulation (M-6, M-1). Findings B-2, B-3, M-4 and M-5 carry the full attack text in the buckets above. One further attack found no wrong outcome:

- Divergence at the status boundary: `status: blocked` maps to `--outcome failed` (SPEC:63) and a failed Task keeps its dependents blocked until a `--retry-of` replacement completes it (CAPS:142-144); a worker's own `failed` does not count toward the circuit breaker (CAPS:80, SPEC:263). The mapping holds, but no cap exists on blocked-then-retry cycles; it is a coordinator choice and is recorded only as part of M-6.

## === GUARD CONDITION BOUNDARY TABLE ===

Triggered: the specification contains thresholds and guards (CMD:313). Constructed by Nygard, completeness checked by Crispin, attacked by Whittaker. Guards enumerated: GC-1 `--unattended` switch; GC-2 gate resolution (default / caller flag / blocked); GC-3 contract location and output directory; GC-4 status to outcome mapping; GC-5 wait and heartbeat limits; GC-6 `ask` timeout and resume; GC-7 task confidence below 0.70; GC-8 nested-worker depth; GC-9 readiness limit; GC-10 additive-edit check regex. Classes left out are named with a reason in the "Left out" lines below.

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|---|---|---|---|---|---|---|
| GC-1 `--unattended` | SPEC:51, 146 | Zero/Empty | flag absent | false | SA-1: today's behaviour unchanged | OK |
| GC-1 `--unattended` | SPEC:51, 228 | Typical | standalone token in the brief | true | no-prompt mode (SPEC:60) | OK |
| GC-1 `--unattended` | SPEC:128 | Legitimate Edge Case | flag passed to a section-4 command | true | not stated | GAP (minor; folded into M-4) |
| GC-1 `--unattended` | SPEC:228 | Sentinel Value Match | `--unattended` inside a quoted prompt | ambiguous | not stated | GAP (M-4) |
| GC-2 gate resolution | SPEC:60 | Zero/Empty | caller flag given with an empty value | unknown | not stated | GAP (M-5) |
| GC-2 gate resolution | SPEC:60 | Typical | documented default exists | (a) | default applied | OK |
| GC-2 gate resolution | SPEC:121 | Legitimate Edge Case | task `--compliance` override supplied with confidence below 0.70 | unknown | row says blocked regardless | GAP (minor; part of M-5) |
| GC-3 contract location | SPEC:62 | Zero/Empty | no output directory in the brief | unknown | not stated | GAP (M-5) |
| GC-3 contract location | SPEC:62, 87, 90, 120 | Maximum/Overflow (value is a file, not a directory) | `--output <file>` | undefined path | not stated | GAP (B-2) |
| GC-3 contract location | SPEC:62, 83, 92 | Legitimate Edge Case | command with its own fixed contract path | conflicts | WC-4 vs row | GAP (B-2) |
| GC-3 contract location | SPEC:62, 64 | One/Minimal | retry reuses the same directory | overwrite | WC-6 vs AC-3.2 conflict | GAP (B-3) |
| GC-4 status to outcome | SPEC:63 | Zero/Empty | no report file | no report | `--outcome failed` | OK |
| GC-4 status to outcome | SPEC:63 | Typical | `succeeded` | true | `--outcome succeeded` | OK |
| GC-4 status to outcome | SPEC:62-63 | Legitimate Edge Case | `partial` | maps to succeeded | when `partial` applies not defined | GAP (M-2) |
| GC-4 status to outcome | SPEC:62, 183 | Sentinel Value Match | existing contract with a different status word | unknown | not stated | GAP (M-2) |
| GC-5 wait limits | SPEC:68 | Typical | wait of 3 minutes | within limit | no split needed | OK |
| GC-5 wait limits | SPEC:68 | One/Minimal | wait of 4.5 minutes | between "at most 4" and "longer than 5" | not stated | GAP (M-1) |
| GC-5 wait limits | SPEC:68, 24 | Maximum/Overflow | one fan-out call over 5 minutes | unsplittable | not stated | GAP (M-1) |
| GC-6 `ask` | SPEC:61 | Maximum/Overflow | no answer after repeated timeouts | resumes same id | no cap | GAP (M-6) |
| GC-6 `ask` | SPEC:61, 200 | Legitimate Edge Case | gate hit with `ask` allowed vs AC-2.2 | differs | not stated in brief | GAP (M-6) |
| GC-7 confidence | SPEC:121 | Zero/Empty | confidence 0.0 | below 0.70 | blocked | OK |
| GC-7 confidence | SPEC:121 | Legitimate Edge Case | confidence exactly 0.70 | not below | proceeds (follows INV-B:199 "< 0.70") | OK |
| GC-8 depth | SPEC:33, 252 | One/Minimal | worker at depth 1 | refused | `nested_worker_depth_exceeded` (call sites UNVERIFIED) | OK |
| GC-9 readiness | SPEC:59 | Typical | fallback after 30 s | passes | WC-1 | OK |
| GC-9 readiness | SPEC:59 | Maximum/Overflow | prompt wait above about 45 s | fails again | WC-1 (EVIDENCE.md:56, UNVERIFIED file) | OK |
| GC-10 additive-edit regex | SPEC:176, 193 | Legitimate Edge Case | a deleted markdown bullet (`- text` shows as `-- text` in a diff) | not matched | check passes; deletion goes undetected (reproduced here with `diff -U0` and `grep -E '^-[^-]'`, printed nothing) | GAP (M-8) |
| GC-10 additive-edit regex | SPEC:176 | Typical | deleted table row | matched | check fails as intended | OK |

Left out, with the reason: GC-1 One/Minimal (a boolean has no minimal value); GC-2 Maximum (count of gates is not bounded by a guard); GC-5 Zero/Empty (a zero-length wait never reaches a threshold); GC-6 Zero/Empty (a zero timeout is not a spec input; it is Orca's flag); GC-7 Maximum (confidence is bounded at 1.0 and behaves like typical); GC-8 Maximum (a raised depth is D5 option (b), SPEC:252); GC-9 Zero/Empty (a zero readiness limit is Orca's flag; a non-positive `--timeout-ms` falls back to 60 s, CAPS:44); sentinel values in GC-3, GC-5 to GC-9 (no sentinel exists).

Note: the GC-1 row for a section-4 command records that the document does not say what a section-4 command does with an unexpected `--unattended` (SPEC:128). It is minor and is handled as part of M-4's follow-up fix.

FR-8, FR-9, FR-10: every GAP above is tied to a finding id; those that name a concrete wrong outcome are B-1 to B-3, the rest are graded Medium or minor by the grading check. The table is complete under FR-10 for the ten guards listed.

## Standard-format summary

```yaml
specification_review:
  original_spec: .dev/orca-command-refactor/specs/orca-worker-contract-spec.md
  review_date: 2026-11-10
  expert_panel: [Wiegers, Adzic, Cockburn, Fowler, Nygard, Whittaker, Newman, Hohpe, Crispin]
  focus_areas: [requirements, architecture]
  review: "1 of 3"
quality_assessment:
  overall_score: 5.8
  clarity: 7
  completeness: 6
  testability: 5
  consistency: 5
critical_issues:
  - {id: B-1, category: requirements, severity: CRITICAL, expert: Wiegers/Fowler, issue: "AC-1.1 asserts a section in 37 commands at the end of Phase 1; load, pr-submit, brainstorm and init-lite cannot satisfy it", recommendation: "scope AC-1.1 per phase and place brainstorm and init-lite in a phase"}
  - {id: B-2, category: requirements, severity: MAJOR, expert: Adzic/Whittaker, issue: "WC-4 contract path contradicts adversarial, workflow and file-valued --output rows and the live check", recommendation: "WC-4 default path plus a per-row contract-path cell"}
  - {id: B-3, category: requirements, severity: MAJOR, expert: Nygard/Whittaker, issue: "WC-6 fresh directory conflicts with WC-4 and AC-3.2 (retry overwrites attempt 1)", recommendation: "retry brief passes a new directory; AC-3.2 uses a new directory"}
expert_consensus:
  - "Coordinator-on-top decision is supported by the inventories and states its own evidence gaps."
  - "Counts reconcile (10 + 27 + 6 = 43)."
  - "The weakness is the acceptance layer and the report-path rule, not the decision."
improvement_roadmap:
  immediate: [B-1, B-2, B-3]
  short_term: [M-1, M-2, M-3, M-5, M-6, M-9]
  long_term: [M-4, M-7, M-8, M-10, M-11]
adversarial_analysis:
  - {methodology: Divergence, severity: MAJOR, invariant_location: "SPEC:62", triggering_condition: "command with its own contract path", scenario: "B-2"}
  - {methodology: Sequence, severity: MAJOR, invariant_location: "SPEC:64", triggering_condition: "retry with same brief", scenario: "B-3"}
  - {methodology: Sentinel Collision, severity: Medium, invariant_location: "SPEC:228", triggering_condition: "flag text inside a quoted prompt", scenario: "M-4"}
  - {methodology: Zero/Empty, severity: Medium, invariant_location: "SPEC:62", triggering_condition: "no output directory", scenario: "M-5"}
  - {methodology: Accumulation, severity: Medium, invariant_location: "SPEC:61", triggering_condition: "unanswered ask", scenario: "M-6"}
```

## Remaining Medium findings (stated once, for the follow-up list)

### M-8 (Medium, MAJOR). Two common checks do not check what they claim

Expert: Crispin. AC-C5 and AC-0.3 use `grep -E '^-[^-]'` on `git diff -U0` (SPEC:176, 193); a deleted markdown bullet appears as `-- text`, so the check passes while an existing line was removed (reproduced with `diff -U0` and the same pattern; nothing printed). AC-C1 greps `src/superclaude/core` for `orca orchestration|worktree|terminal|agent` (SPEC:172), but Phase 0 adds an Orca section to `src/superclaude/core/HOW-WE-WORK.md` and a brief template in `src/superclaude/core/WORKER-CONTRACT.md` (SPEC:158, 150), whose wording is unspecified; if either quotes an Orca command, AC-C1 fails in Phase 0, and SA-2 allows only "an example of a caller's question channel" (SPEC:147). Medium: the checks are weak or may misfire, but no stated text yields a wrong build. Recommendation: use a diff pattern that also matches `--` bullets (`^-([^-]|-[^-])` plus the header filter) and state that the core Orca wording avoids the matched command forms.

### M-11 (Medium, MINOR). WC-11 versus fixed-output commands

Expert: Whittaker. WC-11 says default output paths carry a timestamp or slug (SPEC:69); `/sc:index-repo` writes a fixed `PROJECT_INDEX.md` with no output flag (SPEC:86; INV-A:53) and the init-lite default is a fixed path (SPEC:87). Two such workers in one worktree write the same file. Cleanup-audit acknowledges the limit (SPEC:85); the others do not. Medium: the effect needs two concurrent workers on one command.

## Coverage

Covered: the whole candidate (SPEC:1-285), `README:1-38`, `INV-A:1-120`, `INV-B:1-323`, `CAPS:1-188`, the command definition `CMD:1-491`, and the review-loop prompts file (lines 1-68). Inspected: behaviour of the contract (section 2), the per-command changes (section 3), phases and acceptance checks (sections 6-7), and the dependencies each touches (install list, mirrors, routing guide), by cross-reading the inventory rows each cites. The `diff -U0` regex claim in M-8 was reproduced in the sandbox.

Not covered, so UNVERIFIED: every citation of a file outside the workspace (`src/superclaude/...`, `CLAUDE.md`, `.dev/evals/ccsession-orca-e2e-20261026/EVIDENCE.md`, `.dev/codegraph-migration/...`, `/opt/Orca/...`, `pyproject.toml`, `Makefile`); the spec's statements that its author re-read 11 locations and that a validator re-read about 340 citations (SPEC:11, 285). The claims in the inventories themselves were taken as written; only the spec's reading of them was checked.

Steps not run: the Improve step (Behavioral Flow step 6) and TDD/PRD scoping (6a-6d) were not run, because the brief assigns this single output file and forbids editing anything else. `--iterations` was not given; this run is one review. No Reviser step was run.

Brief clauses overridden: none. The follow-up question (whether to open an issue for the Medium and minor findings) was not asked in this worker run, and no issue was created.

## Follow-up candidates

Medium: M-1, M-2, M-3, M-4, M-5, M-6, M-7, M-8, M-9, M-10, M-11.
Minor: N-1, N-2, N-3, N-4, N-5, N-6, N-7.

Medium and minor findings never trigger a revision and are not in the Reviser brief.

## Reviser brief

Blocking finding ids: B-1, B-2, B-3.

Repair only the blocking findings B-1, B-2, B-3 in the revised candidate `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`. Revise only text a blocking finding names. Prefer deleting or narrowing text when the requirements are still met. Add no rule, mechanism or section that a listed finding does not call for, and cite the finding id on every added paragraph or table. Report the byte size before and after, and the bytes added and deleted per finding id. Leave minor and Medium findings alone. Return the candidate once and do not award yourself a PASS.

verdict: FAIL

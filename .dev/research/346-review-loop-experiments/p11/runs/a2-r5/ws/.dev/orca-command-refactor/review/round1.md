review: 1 of 3

# Spec-panel review, round 1: Orca worker contract spec

Command: `/sc:spec-panel @.dev/orca-command-refactor/specs/orca-worker-contract-spec.md --mode critique --focus requirements,architecture`
Candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`, 57763 bytes, 285 lines, sha256 `d3cdbe573e57303b9ce6c93d1fe98ba18fb7cb1a15773d926bf6a0c31425200d`.
Review type: first review, full document. No `--re-review` or `--baseline` was given, so there is no prior-findings table. The candidate was not edited and no other review was started.

Citation keys. `SPEC:N` = line N of the candidate. `README:N` = `.dev/orca-command-refactor/README.md`. `INV-A:N`, `INV-B:N`, `CAPS:N` = lines of `.dev/orca-command-refactor/inventory/commands-a.md`, `commands-b.md`, `orca-capabilities.md`. These four files are the only evidence checked against files. Every claim that rests on a file outside the workspace (`src/...`, `CLAUDE.md`, `EVIDENCE.md`, the codegraph README, Orca's installed files) is marked UNVERIFIED unless one of the four files quotes it, in which case the quoting line is cited.

## What was covered

- Read in full: the candidate (285 lines), `README` (38 lines), `INV-A` (120), `INV-B` (323), `CAPS` (188).
- Checked the candidate's `INV-*`/`CAPS:*` citations against the inventory lines. In sections 1.2, 1.3, 1.4, 2.2, 3.1, 3.2 and 4 every `INV-A`/`INV-B` row reference and every `CAPS` reference I traced points at the cited content. The `README:12` and `README:31` citations also hold. No citation defect was found.
- Checked counts. SPEC:76 says 10 ready, 27 needing a change, 6 coordinator-only, 43 in total. The section 3.1 table has 10 rows (SPEC:83-92), the 3.2 table has 27 (SPEC:99-125), the section 4 table has 6 (SPEC:132-137). The inventories give 5+5 ready, 13+14 needs-change, 3+3 coordinator-only (INV-A:73, INV-B:278). The phase lists at SPEC:159-162 cover the 31 changed commands and fixes. The counts are conserved. Pipeline Dimensional Analysis was therefore not triggered: the rollout phases are not a data pipeline with a count mismatch.
- Traced behavior: each requirement WC-1 to WC-12 to its acceptance check; each phase to its checks; the `--unattended` flag from first mention (SPEC:51) through D1 (SPEC:227), section 3, section 5, section 6 and section 7.
- Dependencies touched: the Orca facts the requirements rely on (`CAPS`), and the command rows (`INV-A`, `INV-B`).
- Not covered, UNVERIFIED because no file in the workspace holds them: every `src/superclaude/...` citation (for example `SPEC:11`, `SPEC:52`, `SPEC:83-125`), `CLAUDE.md:*`, `pyproject.toml:38`, `EVIDENCE.md` read directly, the codegraph README read directly, and the self-reported checks at SPEC:11 and SPEC:285. All inputs the brief names were readable, so the result is not `incomplete`.
- Not active: `--focus correctness` was not passed, so the State Variable Registry is not produced. Advisory: the spec contains numeric guard thresholds (SPEC:59, 68, 121, 33), so the panel recommends `--focus correctness` for a later round.

## Grading notes

1. Every finding below was graded with the sentence "An implementer who follows the stated text as written builds X, and X is wrong because Y." Only findings where the sentence holds without a further assumption are blocking.
2. Review Loop bullet 2 calls FR-8/FR-9 findings blocking. The brief's grading check says an undefined state or unspecified edge case is Medium and belongs under follow-up candidates even when labelled MAJOR. This review applies the brief's check (it narrows the blocking set and never grades a minor finding as blocking): a GAP row from the table below is blocking only if its finding also passes the grading sentence, otherwise it is carried as a Medium follow-up candidate. The coordinator should confirm this reading before round 2.
3. Minor findings are notes and never fail the review.

## Quality assessment (0-10)

| Dimension | Score | Basis |
|---|---|---|
| Clarity | 7 | Per-command rows are precise; the contract-location rule (B-1) and the phase/flag sequencing (M-3) are not. |
| Completeness | 6 | Blocked-gate lifecycle, nested propagation and failure paths are absent (M-2, M-6, M-9). |
| Testability | 5 | Two acceptance checks cannot pass as written (B-1, B-2); WC-3, WC-6, WC-12 have no check (M-5). |
| Consistency | 6 | Citations and counts are consistent; a few stated texts contradict (B-2, M-3, M-14). |

## Mandatory artifact: Guard Condition Boundary Table

Triggered: the spec contains threshold checks and boolean guards (SPEC:59, 63, 68, 60, 33, 121). The table is complete (all cells populated, all guards enumerated) before the synthesis below, as FR-10 requires. Responsibility: Nygard builds, Crispin validates completeness, Whittaker attacks the entries.

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|---|---|---|---|---|---|---|
| GC-1 outcome mapping: "report says failed or blocked, or no report exists" | SPEC:63 | Zero/Empty | report file absent | true | `--outcome failed` | OK |
| GC-1 | SPEC:63 | Zero/Empty | report file present, 0 bytes | false (nothing says failed or blocked; a file exists) | falls to "succeeded otherwise"; the check at SPEC:183 is coordinator-side only | GAP |
| GC-1 | SPEC:63, 62 | One/Minimal | contract holding only `status: succeeded` (no `command`, `report_path`) | false | maps to succeeded; the worker is never told to validate the required fields that SPEC:183 asserts later | GAP |
| GC-1 | SPEC:63 | Typical | `status: partial` | false | `--outcome succeeded`, body's first sentence says partial | OK |
| GC-1 | SPEC:63, 76 (via CAPS:76-77) | Maximum/Overflow | second `worker_done` after the first (retry, `consumer_fenced`) | n/a | "exactly once"; `consumer_fenced` means stop without sending (SPEC:70) | OK |
| GC-1 | SPEC:62 | Sentinel Value Match | `status: blocked` with `blocked_question` empty or missing | true (blocked) | outcome failed; the content of a missing question is not specified, AC-2.2 later asserts non-empty (SPEC:200) | GAP |
| GC-1 | SPEC:62-63, 183 | Sentinel Value Match | `status: success` or `error` (a command's own word, kept because commands "keep their fields") | false | falls to "succeeded otherwise" | GAP |
| GC-1 | SPEC:63 | Legitimate Edge Case | audit verdict FAIL with `status: succeeded` | false | `--outcome succeeded` | OK |
| GC-2 wait split: single blocking step longer than 5 minutes | SPEC:68 | Zero/Empty | wait of 0 s | false | no split | OK |
| GC-2 | SPEC:68 | One/Minimal | wait of 1 s | false | no split, heartbeat unaffected | OK |
| GC-2 | SPEC:68 | Typical | 3 minutes | false | no split; heartbeat between steps | OK |
| GC-2 | SPEC:68 vs 210 | Maximum/Overflow | exactly 300 s | false (not "longer than 5") | not split, yet heartbeat cadence is 5 minutes (CAPS:130) and AC-4.3 allows at most 240 s | GAP |
| GC-2 | SPEC:104 | Maximum/Overflow | one eval of 3600 s | true | split into waits of at most 4 minutes | OK |
| GC-2 | SPEC:114, 283 | Sentinel Value Match | pr-submit `--timeout` 600 (a cumulative budget per the spec) | per iteration | each poll-plus-sleep iteration must stay under 4 minutes; runtime UNVERIFIED but flagged and checked by AC-4.3 | OK |
| GC-2 | SPEC:68 | Legitimate Edge Case | one Agent-tool fan-out call (tdd 10+ agents, INV-B:221) blocking over 5 minutes | the rule names only "a poll wait, a long eval" | not specified | GAP |
| GC-3 unattended gate: flag `--unattended` present | SPEC:60, 146 | Zero/Empty | flag absent | false | every prompt and default unchanged (SA-1) | OK |
| GC-3 | SPEC:99 | One/Minimal | flag present, command has no gate (analyze) | true | no-op | OK |
| GC-3 | SPEC:116 | Typical | flag present, gate with a documented default (research pins `--strategy planning`) | true | default used | OK |
| GC-3 | SPEC:60, 62 | Maximum/Overflow | gate fires and the output directory is unwritable or invalid | true | "blocked" requires writing the contract; nowhere to write it | GAP |
| GC-3 | SPEC:228 | Sentinel Value Match | the token `--unattended` appears inside a quoted topic or prompt | unknown | parsing rule not stated | GAP |
| GC-3 | SPEC:83-84, 89 vs 60 | Legitimate Edge Case | `--unattended` together with `--interactive` (adversarial, brainstorm, release-split) | conflict | only cleanup, improve, roadmap, explain, test say the person-mode flag is refused; for the three named, the brief is told "never `--interactive`" | GAP |
| GC-3 | SPEC:128 vs 51 | Legitimate Edge Case | `--unattended` passed to a section 4 command | unknown | "get no `--unattended` mode"; accept, ignore or refuse is not specified | GAP |
| GC-4 nesting fence: worker calls `worker-start` | SPEC:33, 66 | Zero/Empty | caller is the coordinator (depth 0) | false | allowed (CAPS:97) | OK |
| GC-4 | SPEC:33 | One/Minimal | caller is a depth-1 worker | true | refused `nested_worker_depth_exceeded` (CAPS:99) | OK |
| GC-4 | SPEC:33, 214 | Typical | setting 1, new Run | true | depth not reset (CAPS:101) | OK |
| GC-4 | SPEC:252 | Maximum/Overflow | setting raised to 2 (D5 b) | false | rejected by D5 recommendation | OK |
| GC-4 | CAPS:100 | Sentinel Value Match | setting 0, negative or non-integer | n/a | Orca falls back to 1; spec does not restate it, no impact | OK |
| GC-4 | SPEC:24, 66, 276 | Legitimate Edge Case | `task-create` from a depth-1 worker; Agent-tool subagent | UNVERIFIED / not counted | WC-8 forbids `task-create` regardless; subagents are not counted (CAPS:155) | OK |
| GC-5 `/sc:task` confidence below 0.70 resolves as blocked | SPEC:121 (INV-B:199) | Zero/Empty | confidence 0.0 | true | blocked | OK |
| GC-5 | SPEC:121 | One/Minimal | 0.69 | true | blocked | OK |
| GC-5 | SPEC:121 | Typical | 0.85 | false | proceeds (tier handling is the command's own) | OK |
| GC-5 | SPEC:121 | Maximum/Overflow | 1.0 | false | proceeds | OK |
| GC-5 | SPEC:121 | Sentinel Value Match | exactly 0.70 | false ("below 0.70") | proceeds | OK |
| GC-5 | SPEC:121, 60(b) | Legitimate Edge Case | confidence below 0.70 and the existing override `--compliance [tier]` supplied (INV-B:199) | unknown | not stated whether the override counts as a caller-supplied value (WC-2 b) or still blocks | GAP |
| GC-6 readiness: prompt falls back "well inside" the 60 s limit | SPEC:59 | Zero/Empty | no prompt at all | n/a | passes | OK |
| GC-6 | SPEC:59 | One/Minimal | fallback at 1 s | inside | passes | OK |
| GC-6 | SPEC:59 (CAPS:49) | Typical | fallback at 30 s | inside | worker-start returned after 34 s and passed | OK |
| GC-6 | SPEC:59 (CAPS:49) | Maximum/Overflow | fallback above about 45 s | outside in practice | the evidence says it fails again; the spec states no number | GAP |
| GC-6 | SPEC:59 | Sentinel Value Match | fallback exactly 60 s | at the limit | fails; "well inside" not quantified | GAP |
| GC-6 | SPEC:59, CAPS:45 | Legitimate Edge Case | `--timeout-ms` raised per start | n/a | permitted, upper bound UNVERIFIED (CAPS:54) | OK |

GAP rows and the findings they feed: GC-1 rows 2, 3, 6, 7 feed M-1 and M-12; GC-2 rows 4 and 7 feed M-15; GC-3 row 4 feeds M-9, row 5 feeds M-8, rows 6 and 7 feed M-7; GC-5 row 6 feeds M-2; GC-6 rows 4 and 5 feed M-21. Under grading note 2 none of these GAP rows is blocking by itself.

## === REQUIREMENTS ANALYSIS ===

### B-1 Contract location rule cannot be satisfied for most of the commands it covers (BLOCKING)

- Severity: MAJOR, graded blocking. Experts: Wiegers (lead), Adzic, Crispin. Priority: High. Quality impact: Testability 5 to 8, Completeness +1.
- Issue. WC-4 says the contract is `<output-dir>/return-contract.yaml`, "where `<output-dir>` is the directory the coordinator passed (`--output` / `--output-dir`)" and that the path is "known before dispatch" (SPEC:62; SPEC:73 repeats "the output directory, so the report path is known before dispatch"). The rows then fail the rule in three ways:
  - The brief passes a file, not a directory: `/sc:tdd` takes `--output <file>` (SPEC:90) and `/sc:init-lite` takes `--output <file>` (SPEC:87).
  - The brief passes no output flag and the location is generated or fixed: workflow's contract lives in `.dev/tasks/to-do/<id>/` with a generated id (SPEC:92; INV-B:272), and its brief passes only `--handoff none`; tasklist writes into `TASKLIST_ROOT` (SPEC:122; INV-B:212); research names a generated `claudedocs/` file (SPEC:116; INV-B:132); implement writes beside a ledger under a derived slug (SPEC:109; INV-A:51); index-repo writes a fixed root file (SPEC:86; INV-A:53); cleanup-audit uses a fixed `.claude-audit/` (SPEC:85; INV-A:42); review-translation names run-time-suffixed files (SPEC:117; INV-B:142).
  - Existing contracts live elsewhere: adversarial's fix is `<output>/adversarial/return-contract.yaml` (SPEC:83), not `<output>/return-contract.yaml`.
- Grading sentence. An implementer who follows the stated text as written builds, for `/sc:tdd` whose brief passes `--output <file>` (SPEC:90), a contract at `<file>/return-contract.yaml` (a path under a regular file) or none at all, and that is wrong because AC-2.2 (SPEC:200) runs exactly `/sc:tdd "auth" --unattended --output <file>` and requires a contract with `status: blocked`, and live-check step 4 (SPEC:183) runs `test -s <contract>` on a path no stated text yields. The same holds for workflow, where "known before dispatch" (SPEC:62) contradicts a generated `<id>` (SPEC:92), and the P1 fix "write the contract for pre-creation STOPs too" (SPEC:92) has no stated directory to write into, because no package exists yet (INV-B:272).
- Recommendation and rationale. Give every command an explicit, coordinator-supplied directory-valued input for the contract (distinct from file-valued `--output`), or state per command the exact contract path as a function of the brief. A "Contract path given the brief" column in sections 3.1 and 3.2 would make step 4 of the live check runnable. A directory-valued flag is not needed for commands whose `--output` is already a directory (reflect, brainstorm, release-split, roadmap, post-release); it is needed for the rest.

### B-2 P0 acceptance check requires a contract that P0 does not build (BLOCKING)

- Severity: MAJOR, graded blocking. Experts: Crispin (lead), Wiegers, Gregory. Priority: High. Quality impact: Consistency 6 to 8, Testability +1.
- Issue. P0 makes no command edit (SPEC:158). AC-0.4 (SPEC:194) says the three smoke runs must pass "steps 1-3 and 5-7" of the live check, and only "step 4 uses the command's existing report file, since the contract arrives in P1". Step 3 (SPEC:182) requires that "its `--outcome` matches the contract's `status` under WC-5" and that "its report path is the WC-4 contract path". Neither exists in P0: troubleshoot writes `return-contract.yaml` only with `--caller task-unified` (INV-B:242), adversarial's contract path is inconsistent on disk (INV-A:35, INV-A:60), and WC-4 is built in P1 (SPEC:159).
- Grading sentence. An implementer who follows the stated text as written runs P0 and requires step 3 to pass for `/sc:troubleshoot`, and that is wrong because step 3 compares against a WC-4 contract and path that P0 does not create, so the check cannot pass; its stated consequence ("a failure here reopens section 1", SPEC:194) then fires on a failure the spec built in, and the 1.4(1) evidence gap (SPEC:43) is never closed by P0.
- Recommendation and rationale. Say which step 3 conditions apply in P0 (for example: exactly one `worker_done`, outcome matches the command's own report, report path is the existing report file). Phase 0 is the test of the central decision, so its pass condition has to be satisfiable by what P0 builds.

## Follow-up candidates (Medium) in this bucket

### M-1 WC-5 sends an unreadable or unrecognised report to `succeeded`

- Severity label MAJOR, graded Medium (undefined state). Experts: Nygard, Whittaker. Priority: High. Impact: Completeness.
- Issue. WC-5 maps `failed`/`blocked`/"no report exists" to failed and "`succeeded` otherwise" (SPEC:63). A zero-byte file, a truncated YAML file, or a `status` word outside the four (a command keeps its own fields, SPEC:62) is none of the named failure cases, so it lands in "otherwise" (GC-1 rows 2, 3, 6, 7). The Task would settle succeeded and dependents become startable (CAPS:90, CAPS:92). The checks that would catch it (SPEC:183) run on the coordinator side after `worker_done`.
- Grading. The sentence needs the assumption that a malformed report occurs, and the text never states what a malformed report is, so Medium.
- Recommendation. Make the default the failure case: succeeded only when a parseable contract carries one of `succeeded`/`partial`; anything else is failed.

### M-2 The `blocked` lifecycle has no input path and no coordinator-side path

- Severity label MAJOR, graded Medium. Experts: Cockburn (lead), Adzic, Hohpe. Priority: High. Impact: Completeness.
- Issue. Gates "resolve as blocked" and the worker ends `--outcome failed` (SPEC:60, 63). The spec does not say how the coordinator turns a `blocked_question` into a new run. A failed Task keeps its dependents blocked (CAPS:90); a retry reuses the Task (`--retry-of`, CAPS:116), so where the answer goes (a new Task spec, or a flag) is undefined. Some rows define no input that could ever satisfy the gate: cli-portify's three approval gates "resolve as blocked" and the only added input is `--resume <contract>` (SPEC:105), with no statement that resuming at a later phase counts as approval of the earlier gate; review-translation needs "a pre-confirmed context input" and a "resume input", both unnamed (SPEC:117); post-release needs "an explicit pre-tag choice" (SPEC:113); `/sc:task` blocked at confidence below 0.70 does not say whether its existing `--compliance` override counts (GC-5 row 6).
- Grading. For cli-portify the happy path of AC-2.3 (SPEC:201) passes under one reading (resume skips earlier gates) and cannot pass under the other (every gate re-fires), so the finding needs a guess between two readings the text allows: Medium.
- Recommendation. State for each blocked gate the input that satisfies it, and add one lifecycle paragraph to section 2.3 for the coordinator: read `blocked_question`, obtain the answer, start a replacement run with the answer in the brief.

### M-3 `--unattended` is accepted in P1 before its gate behavior exists

- Severity label MAJOR, graded Medium. Experts: Nygard, Fowler. Priority: High. Impact: Consistency, safety margin.
- Issue. P1 adds "the `--unattended` flag accepted by every command in sections 3.1 and 3.2 (a no-op where a command has no gate)" (SPEC:159). Gate conversion for the commands that have gates lands in P2 to P4 (SPEC:160-162; rows SPEC:100, 103-105, 109-110, 113-122). AC-1.1 requires the section in every 3.1/3.2 command at P1 (SPEC:195). §2.3 tells every coordinator brief to carry `--unattended` (SPEC:73). Between P1 and P2 a brief for `/sc:auggie-review` with `--unattended` is accepted, and the command still posts to the PR and offers remediation (SPEC:100; INV-A:38), against WC-2 and WC-9 (SPEC:60, 67). Nothing says a coordinator checks the phase column first.
- Grading. The sentence needs a coordinator that dispatches in the gap, which the text neither forbids nor requires: Medium.
- Recommendation. Until a command's gates are converted, its `--unattended` must refuse, or the brief template must list the phase in which each command becomes dispatchable.

### M-4 WC-6 "fresh output directory" conflicts with WC-4 "directory passed, known before dispatch"

- Severity label MAJOR, graded Medium. Experts: Nygard, Hohpe, Crispin. Priority: Medium. Impact: Consistency, Testability.
- Issue. Twenty or so 3.2 rows give resume as "fresh dir" (SPEC:99-125). A retry starts with the same Task spec (CAPS:116), so the same brief and the same directory. If the command writes into a new directory, `--report-path` is not the path fixed before dispatch (SPEC:62, 73); if it reuses the directory, the first attempt's output is overwritten, which WC-6 forbids (SPEC:64). Who creates the fresh directory (the command or the coordinator's brief) is not stated. Section 7 has no check for WC-6 at all.
- Grading. Two readings of who creates the directory; the implementer picks one: Medium.
- Recommendation. State that the coordinator passes a new directory per attempt, or that the command writes a per-attempt subdirectory and returns its path inside the contract at a fixed parent path; add one retry check.

### M-5 Several requirements have no acceptance check

- Severity label MAJOR, graded Medium. Experts: Crispin (lead), Gregory, Wiegers. Priority: Medium. Impact: Testability.
- Issue. No check in section 7 exercises WC-3 (ask path), WC-6 (retry), WC-12 (`check`/`consumer_fenced`), WC-10 outside pr-submit (cli-eval has a row, SPEC:104, and no check), or WC-11 outside save (AC-3.4, SPEC:207). Step 5 of the live check searches the transcript for `AskUserQuestion` only (SPEC:184). WC-2 also bans ending a turn on a chat question or `[yes / no]` offer (SPEC:60); INV-A:62 describes that stall as a silent no-`worker_done` and `agentWait` is defined as a prompt "only a human can answer" (CAPS:129), so step 2 may not flag it (UNVERIFIED), leaving only the 900000 ms wait in step 3 (SPEC:182) to notice it.
- Grading. This is a requirement without a stated check, not a stated text that does harm: Medium.
- Recommendation. Add one check per unchecked requirement and one for the chat-question case (for example a transcript search for a trailing question mark or `[yes / no]`).

### M-6 Unattended mode is not propagated to nested invocations, and nested contracts can collide

- Severity label MAJOR, graded Medium. Experts: Fowler (lead), Hohpe, Whittaker. Priority: Medium. Impact: Completeness.
- Issue. Only tasklist to reflect is specified (SPEC:122). Other nested calls with their own gates or writes are not: roadmap calls `sc:save` at every wave (INV-B:154; save writes single-owner keys, SPEC:119), pr-submit may call `/sc:auggie-review` as a fallback (INV-B:91), tdd calls the `task` skill whose "ask the user" lines are named only as tdd's gates (SPEC:90), release-split calls brainstorm (INV-B:119), workflow calls reflect (INV-B:269). WC-2 says the command never prompts under `--unattended` (SPEC:60); a nested call made without the flag may. Nested contract-writers also share the name `return-contract.yaml` (INV-B:112, INV-A:35): tasklist runs N reflects in parallel (INV-B:211), each writing `<output>/return-contract.yaml`, while WC-4 puts the tasklist's own contract at the same name (SPEC:62).
- Grading. The text never states a propagation rule: Medium.
- Recommendation. State that a nested `/sc:` call inherits `--unattended` and is given a subdirectory of the caller's directory.

### M-7 `--unattended` with person-mode flags, and with section 4 commands

- Severity label MAJOR, graded Medium. Experts: Whittaker, Wiegers. Priority: Medium. Impact: Consistency.
- Issue. WC-2 has the command never prompt under `--unattended` (SPEC:60). Only cleanup, improve, roadmap, explain, test and business-panel say the person-mode flag is refused (SPEC:102-103, 108, 110, 118, 123). For adversarial, brainstorm and release-split the protection is a brief-side "never `--interactive`" (SPEC:83-84, 89), so `--unattended --interactive` is undefined (GC-3 row 6). A section 4 command "gets no `--unattended` mode" (SPEC:128), so what happens when one is given the flag is undefined (GC-3 row 7).
- Recommendation. One sentence in WC-2: under `--unattended` every person-mode flag is refused, and section 4 commands refuse `--unattended`.

### M-8 No parsing rule for the `--unattended` token

- Severity label MINOR to MAJOR, graded Medium. Experts: Whittaker. Priority: Low. Impact: Clarity.
- Issue. D1 says the flag "cannot misfire on a person" (SPEC:228). A quoted topic containing the token (for example `/sc:research "what does --unattended do"`) is a sentinel collision (GC-3 row 5), and the spec never says the token counts only as a standalone argument outside quotes.
- Recommendation. Define the token match in the contract.

### M-9 Unwritable output directory, process death, and contract schema details

- Severity label MAJOR, graded Medium. Experts: Nygard (lead), Newman, Hightower. Priority: Medium. Impact: Completeness.
- Issue. WC-4 says the contract is written "on success, failure, blocked and partial outcomes, including stops before any other output exists" (SPEC:62). Two cases cannot hold: an output directory that cannot be created or written (GC-3 row 4), and a session that dies or is killed before writing. §1.4(2) concedes a silent stall is visible only through `agentWait` or a missing report (SPEC:44), yet no requirement says what the coordinator does after a time limit with no `worker_done`; CAPS:162 and CAPS:188 record that Orca has no known total-run bound (UNVERIFIED). The schema is also loose: path base for `report_path` and `artifacts` (absolute or relative to which directory), no `contract_version`, no field types (SPEC:62). The existing workflow contract carries a version (`contract 1.1`, INV-B:272), so the precedent exists.
- Recommendation. Add a refusal rule for an unusable directory, one coordinator-side stall rule, and a minimal schema (types, path base, version).

### M-10 WC-9 authorization has no mechanism for commands that lack a flag

- Severity label MAJOR, graded Medium. Experts: Nygard, Fowler. Priority: Medium. Impact: Completeness.
- Issue. WC-9: outward defaults turn on "only through the command's own explicit flag written in the brief" (SPEC:67); D4(a) repeats "passes the command's explicit flag" (SPEC:245). The inventories describe such a flag for auggie-review (`--no-post-pr`, INV-A:38) but for post-release only a session-level "pre-authorized this session" (INV-B:79), for `/sc:task` the EXEMPT keywords `commit`/`push` and a committed TFEP report (INV-B:204), and for pr-submit no pre-authorization flag at all. No flag name is given for any of them, so WC-9 and D4(a) cannot be implemented for those commands without inventing flags.
- Recommendation. Name the authorization input for each outward action in section 3.2, or state that no such input exists and the action stays off.

### M-11 WC-11 "must never" versus ready rows, and parallel source-editing workers

- Severity label MAJOR, graded Medium. Experts: Newman, Nygard. Priority: Medium. Impact: Consistency.
- Issue. WC-11 says two workers in one worktree must never write the same file (SPEC:69). Ready rows write fixed paths: cleanup-audit `.claude-audit/` (SPEC:85, which admits "one audit per worktree at a time"), index-repo `PROJECT_INDEX.md` (SPEC:86), init-lite's default report (SPEC:87). The brief template does not tell the coordinator to serialise them. The live check starts workers with `--worktree current` (SPEC:180) and workers share the worktree by default (CAPS:115). WC-11 covers output files, not source edits: cleanup, improve, document (inline mode), implement and test `--fix` edit product files (SPEC:103, 107, 109, 110; INV-A:47, INV-B:234), and two such workers on one tree can overwrite each other, with rollback UNVERIFIED (SPEC:103).
- Recommendation. State a coordinator rule for serialising or separating fixed-path and source-editing workers.

### M-12 Status vocabulary versus "keep their fields"

- Severity label MINOR to MAJOR, graded Medium. Experts: Newman, Adzic. Priority: Medium. Impact: Consistency.
- Issue. WC-4 requires `status` in a fixed set and also says commands that already write a contract "keep their fields" (SPEC:62). Check step 4 asserts the fixed set on every contract (SPEC:183). The existing contracts' status words are not given in any inventory (workflow's contract has a `status` field, INV-B:272); the vocabulary is UNVERIFIED. If any differs, AC-1.2 (SPEC:196) fails for that command.
- Recommendation. State the mapping from each existing vocabulary or require the fixed set to replace it.

### M-14 Load: the P1 checks cannot be met as the row is written

- Severity label MINOR, graded Medium. Experts: Wiegers, Crispin. Priority: Low. Impact: Consistency.
- Issue. The load row says no report, no resume, use it inside another worker's brief, fix only the usage line (SPEC:112; SPEC:265 "a report file would be an unrequested addition"), and P1 lists "load (usage line only)" (SPEC:159). AC-1.1 requires a section naming `return-contract.yaml` in every 3.1/3.2 command (SPEC:195) and AC-1.2 runs the full live check, including `test -s <contract>`, on each P1 command (SPEC:196). §3's preamble also says every changed command gains the section (SPEC:76).
- Grading. Whether load counts as a "P1 command" for AC-1.2 needs a guess: Medium.
- Recommendation. Exclude load from AC-1.1/AC-1.2 explicitly, or give it a contract.

### M-20 WC-3 does not limit who may answer an approval-type gate

- Severity label MINOR to MAJOR, graded Medium. Experts: Nygard, Cockburn. Priority: Low. Impact: Completeness.
- Issue. WC-3 lets the worker ask the coordinator and "re-invoke the command with the answer as a flag" (SPEC:61). The coordinator is another agent. D2 closes this only for `/sc:implement` (SPEC:232-236, rule at INV-A:51), and D4 only for outward actions (SPEC:244-247). Approval-type gates elsewhere (cli-portify approvals SPEC:105, cleanup and improve "Approval Required" items SPEC:103, 110) have no statement that the answer must come from a person.
- Recommendation. State which gates need a person's own words relayed, and which a coordinator may decide.

### M-21 WC-1 states no number

- Severity label MINOR, graded Medium. Experts: Wiegers, Crispin. Priority: Low. Impact: Testability.
- Issue. "Well inside the readiness limit (default 60 s)" (SPEC:59) has no number, while the evidence gives one: a 30 s fallback passed and a value above about 45 s fails again (CAPS:49). An implementer choosing 40 s or 50 s has no stated way to know which side of 45 s is acceptable (GC-6 rows 4, 5).
- Recommendation. State a maximum fallback in seconds (the evidence supports 30).

## === ARCHITECTURE ANALYSIS ===

No blocking architecture finding. Fowler's check: the central decision (Orca on top, commands unchanged units of work, SPEC:13-45) is supported by the checked evidence. The rejected alternative's reasons R1 to R5 (SPEC:33-37) each trace to `CAPS` lines that say what is claimed. The honest statement of evidence strength (SPEC:41-45) is correct on the lines I could check (INV-B:323, CAPS:156, CAPS:187). The findings below are Medium or minor.

- **M-13 (Medium; Fowler, Hohpe).** AC-C1 greps `src/superclaude/core` for `orca(-ide)? (orchestration|worktree|terminal|agent)` and must print nothing for every phase (SPEC:167, 172), but SA-2 permits an Orca mention "as an example of a caller's question channel inside the contract file" (SPEC:147), and the contract file is a core file (SPEC:52). An `orca orchestration ask` example in that file, written in lowercase, fails the check in every phase. The grep also leaves out `hooks`, `templates`, scripts and the `plugins/superclaude/` mirror, whose update rule is UNVERIFIED (SPEC:279). Whether the example is written in a form that matches is a guess: Medium.
- **M-15 (Medium; Nygard, Hightower).** WC-10 splits only "a poll wait, a long eval" (SPEC:68). A single Agent-tool fan-out call (tdd 10+ agents, INV-B:221; adversarial up to 10 generators, INV-A:35) can block longer than 5 minutes with no step to split, and exactly 300 s is neither split nor within AC-4.3's 240 s (SPEC:210). Heartbeat age is not known to affect liveness (CAPS:130, CAPS:182 item 7, UNVERIFIED), so the impact may be small.
- **M-16 (Medium; Newman, Fowler).** `/sc:pr-submit` is in section 3.2 with an `--unattended` row (SPEC:114) and counted in AC-1.1 (SPEC:195), while D3(a), the recommendation, says "no pr-submit changes in Phase 4" (SPEC:240) and §4 says pr-submit stays a worker candidate only under D3 (SPEC:139). INV-B:90 records a stated "Will Not: run headless / imply a daemon" for pr-submit (cited there as `cmd/pr-submit.md:85`, `SKILL.md:225`, UNVERIFIED in the workspace) that the spec does not reconcile with an unattended mode. Whether P1 changes pr-submit before D3 is answered is a guess: Medium.
- **M-17 (Medium; Hohpe, Nygard).** Outcome and report are two messages with no ordering rule: nothing says the contract must be fully written before `worker_done` (write, then notify), and WC-12 allows `consumer_fenced` after the contract is written (SPEC:70). A fenced attempt's contract in a reused directory (M-4) is then read as the current attempt's.
- **Minor notes (architecture).**
  - n-1. One flag carries five behaviors (no prompts, contract writing, outward defaults off, person-mode refusal, per-command resolutions). Fowler would split "write the contract" from "no person"; SA-3 already allows writing the contract on the output flag alone (SPEC:148), so the trigger rules differ between SPEC:60 and SPEC:148.
  - n-2. E2 says a worker has "the same tools as a command a person runs" (SPEC:22); the evidence cited shows the worker reached a ready input (CAPS:49), not that MCP, Monitor or AskUserQuestion behave identically (INV-A:112 lists these as UNVERIFIED).
  - n-3. SPEC:122 states that tasklist's nested reflect "runs inside Claude Code's nesting limit" (INV-A:14, from an external page fetched by that worker, UNVERIFIED here), while INV-B:314 marks nested spawning UNVERIFIED and the spec's own UNVERIFIED list (SPEC:271-285) omits it.
  - n-4. Explain gains the Write tool for every run (SPEC:108), a capability change that is not gated by `--unattended`, against SA-1 (SPEC:146); SA-4 names the fix (SPEC:149).
  - n-5. §1.1 says command changes are "limited to the worker contract" (SPEC:16), but P3 repairs interface drift that exists "regardless of Orca" (SPEC:161); §3.1 says "the only command changes are the small fixes" (SPEC:79), but P1 adds the flag and section to all of them (SPEC:159).
  - n-6. E3 cites `invocation_method: "skill-direct"` as support (SPEC:23) while §1.4(1) says that run "proves the nested route, not the direct route" (SPEC:43); the two sentences read as opposed.
  - n-7. AC-1.3 proposes a "scratch worktree" (SPEC:197); the repo's worktree rule is in `CLAUDE.md`, UNVERIFIED here.
  - n-8. Validate-tests: the fix for the missing default target does not say whether to create the directory or change the default (SPEC:125, AC-3.3 SPEC:206).
  - n-9. The self-reported checks at SPEC:11 and SPEC:285 (11 locations re-read, about 340 citations validated) cannot be checked from the workspace.

## Adversarial analysis (Whittaker, review order 6)

Findings use the panel template. Severity: CRITICAL provably wrong, MAJOR ambiguous or incomplete under attack, MINOR inferrable.

1. I can break this specification by **Zero/Empty Attack**. The invariant at **WC-5 (SPEC:63)** fails when **the contract exists but is 0 bytes or truncated**. Concrete attack: before: Task `dispatched`, contract file empty after a crash mid-write; step: the worker evaluates "report says failed or blocked, or no report exists", both false; after: `--outcome succeeded`, Task `completed`, dependents ready (CAPS:90, CAPS:92). Severity MAJOR (M-1).
2. I can break this specification by **Divergence Attack**. The invariant at **WC-6 against WC-4 (SPEC:64, 62)** fails when **a retry needs a fresh directory and the brief fixes the directory**. Concrete attack: attempt 1 writes `<dir>/return-contract.yaml` with `status: failed`; the retry (`--retry-of`, same Task spec, CAPS:116) must not overwrite it, yet its report path was fixed before dispatch as the same path; after: either attempt 1's output is overwritten or the coordinator reads attempt 1's contract as attempt 2's. Severity MAJOR (M-4).
3. I can break this specification by **Sentinel Collision Attack**. The invariant at **D1 (SPEC:228)** fails when **a legitimate input contains the sentinel**. Concrete attack: `/sc:research "behaviour of --unattended in the contract" --strategy intent` is typed by a person; a plain token search enables unattended mode and the clarification gate is silently skipped. Severity MINOR (M-8).
4. I can break this specification by **Sequence Attack**. The invariant at **WC-12 against WC-5 (SPEC:70, 63)** fails when **`consumer_fenced` arrives after the contract is written and before `worker_done`**. Concrete attack: before: attempt 1 holds the dispatch and writes `status: succeeded`; step: Orca fences it, a replacement attempt starts in the same directory; after: attempt 1's contract sits at the known path with no worker_done behind it, and attempt 2 overwrites or is confused with it. Severity MAJOR (M-4, M-17).
5. I can break this specification by **Accumulation Attack**. The invariant at **WC-11 (SPEC:69)** fails when **fixed-path and source-editing workers accumulate in one worktree**. Concrete attack: three workers started with `--worktree current` (SPEC:180): `/sc:index-repo`, `/sc:index-repo` and `/sc:cleanup-audit --pass 1`; step: both index-repo workers write `PROJECT_INDEX.md`, both audits write `.claude-audit/`; after: the last writer wins and each worker reports `succeeded`. Severity MAJOR (M-11).

## Expert panel notes (review order)

1. Wiegers: the per-command rows are specific and measurable; the contract-location rule is not (B-1), and WC-1 has no number (M-21).
2. Adzic: the examples (SPEC:200-202) are good; the tdd example fails its own contract rule (B-1); no example shows the blocked-then-answered flow (M-2).
3. Cockburn: actors and goals are clear for the coordinator and worker; the person is absent from the blocked flow (M-2, M-20).
4. Fowler: the decision and its boundaries are sound; one flag bundles five behaviors (n-1); propagation to nested calls is missing (M-6).
5. Nygard: failure modes of the contract are mostly missing (M-1, M-9); the stall is conceded but not specified (SPEC:44).
6. Whittaker: five attacks above.
7. Newman: contract evolution (version, status vocabulary) is unspecified (M-9, M-12).
8. Hohpe: ordering of contract write and `worker_done`, and repeat delivery on retry (M-17, M-4); `ask` resume by message ID is handled well (SPEC:61).
9. Crispin: B-2 and M-5; the boundary table above lists 13 GAP rows.
10. Gregory: the quality expectations for the coordinator (what it opens, SPEC:73) are stated; the transcript checks cover only one stall type (M-5).
11. Hightower: operational detail is thin on observability: no requirement that the contract carry timings or the `audit.log` path (UNVERIFIED value); M-9 covers the rest.

## Consensus and disagreements

- Consensus: the decision, the rejected alternative, the phase order and the coordinator-only list are supported by the inventories; the open decisions D1 to D5 are well framed.
- Consensus: two stated texts cannot be satisfied as written (B-1, B-2).
- Disagreement: Cockburn and Nygard would grade M-2 (the blocked lifecycle) blocking; Crispin and Wiegers hold it at Medium because the text allows a reading under which AC-2.3 passes. It is Medium under the brief's grading check.

## Summary of grading

| ID | Label | Graded | Reason |
|---|---|---|---|
| B-1 | MAJOR | blocking | Stated rule yields a path no check can read for named commands (SPEC:62, 90, 200, 183). |
| B-2 | MAJOR | blocking | AC-0.4 requires a contract P0 cannot produce (SPEC:158, 182, 194). |
| M-1 to M-12, M-14, M-20, M-21 | MAJOR/MINOR | Medium | Undefined state or a guess between two allowed readings. |
| M-13, M-15 to M-17 | MAJOR/MINOR | Medium | As above. |
| n-1 to n-9 | MINOR | minor | Notes only. |

## Follow-up candidates

Medium: M-1, M-2, M-3, M-4, M-5, M-6, M-7, M-8, M-9, M-10, M-11, M-12, M-13, M-14, M-15, M-16, M-17, M-20, M-21.
Minor: n-1 to n-9.
None of these blocks the verdict.

## Reviser brief

Blocking finding ids: B-1, B-2.

Restated reviser contract (Review Loop bullet 6; the reviser reads this report, not the command):
- Revise only text a blocking finding names: B-1 names SPEC:62 (WC-4), SPEC:73, the 3.1/3.2 rows that give no contract location, and SPEC:92; B-2 names SPEC:182 and SPEC:194.
- Add no rule, mechanism or section that no blocking finding calls for.
- Each added paragraph or table cites its finding id.
- Report the byte size of the candidate before and after (before this review: 57763 bytes).
- Do not act on the Medium or minor items; they stay as follow-up candidates.

verdict: FAIL

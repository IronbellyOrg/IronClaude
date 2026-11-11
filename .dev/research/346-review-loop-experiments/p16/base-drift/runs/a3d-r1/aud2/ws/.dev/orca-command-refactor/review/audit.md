review: 1 of 3

# Spec-panel audit: Orca worker contract spec (whole-document, first review)

- command: `/sc:spec-panel @.dev/orca-command-refactor/specs/orca-worker-contract-spec.md --mode critique --focus requirements,architecture`
- candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`, sha256 `0d7786a334196b491d4a4779d2dbbc71fedd95552ea14ed522742fd98a72bf68`
- baseline: none given (first review of the whole document; no `--re-review`, so no `baseline: missing` note is needed)
- reviewer model used: claude-sonnet-5-5 (Sonnet 5.5)
- prompt followed: FIRST-REVIEW prompt, `~/.claude/rules/prompts/document_review_loop_prompts.md` (read in full, sandbox copy)
- coverage: the whole candidate (286 lines), the README, and the three inventories. Mode critique; focus requirements + architecture; Whittaker active in every review. Crispin, Gregory and Hightower are outside this focus and were not run. This is a labelled whole-document audit.
- citation shorthand: `SPEC:N` = line N of the candidate; `README:N`; `INV-A:N`, `INV-B:N`, `CAPS:N` = lines of `inventory/commands-a.md`, `commands-b.md`, `orca-capabilities.md`; `PROMPTS:N` = the review-loop prompts file; `CMD:N` = `command.md`.
- UNVERIFIED rule: the sandbox holds no `src/`, `CLAUDE.md`, `.claude/`, `pyproject.toml`, `Makefile`, Orca install or live Orca. Every claim about those is checkable only through the inventories' own quotes. I mark a citation UNVERIFIED when the candidate cites such a file directly and no inventory line repeats it. Citations of the form `INV-x:N` and `CAPS:N` were checked against the files and found as cited (all ~60 I opened).
- Medium/minor handling: findings graded Medium or minor are listed under `follow-up candidates`. The question "open an issue for them?" is not asked here: this sandbox worker has no user channel. No issue was created.

## Result in one paragraph

No finding passes the grading check for blocking. The decision (Orca coordinates, commands stay units of work), the 10/27/6 split (checked: 5+5 ready, 13+14 needs-change, 3+3 coordinator-only against `INV-A:73` and `INV-B:278`; the 27 rows of section 3.2 and the 15 + 9 + 4 + 3 phase assignments reconcile with SPEC:97-125 and SPEC:156-162) and the citation to the capabilities inventory hold. Fifteen Medium findings and five minor notes remain (F-21 is informational). The most consequential Mediums are F-01 (contract path depends on a dir-or-file choice the spec never makes), F-02 (authorization flags that WC-9 requires do not exist for the commands that need them), F-12 (retry/fresh-directory versus a path fixed before dispatch, with a stale-contract risk) and F-08 (an acceptance check that fails a worker which obeys WC-3).

## Expert panel sequence used

Wiegers, Adzic, Cockburn (requirements); Fowler, Nygard (architecture, reliability); Whittaker (adversarial, after Fowler and Nygard); Newman, Hohpe (architecture focus: API evolution, message flow).

## Grading note

Each finding below was graded with the FIRST-REVIEW check: "An implementer who follows the stated text as written builds X, and X is wrong because Y." Where that sentence needed a guess about which of two allowed readings the implementer picks, or the finding is a requirement the document never states, it is Medium even when its label is MAJOR. The `blocking` column below is therefore `no` throughout.

=== REQUIREMENTS ANALYSIS ===

### F-01 Contract path is a function of an undefined dir-or-file choice
- severity label: MAJOR; graded: Medium (missing requirement); priority High; expert: Wiegers (lead), Adzic
- issue: WC-4 puts the contract at `<dir>/return-contract.yaml` when `--output`/`--output-dir` is a directory and at `<file>.return-contract.yaml` when it is a file, and requires the path to be "known before dispatch" (SPEC:62, SPEC:73). Section 3.2 adds a new `--output` (or "a report path") to analyze, build, business-panel, design, document, explain, index, test, recommend, spec-panel and others (SPEC:99, 101, 102, 106, 107, 108, 111, 115, 120, 123) without saying whether the new flag is directory-valued or file-valued. Only commands that already have `--output` have a known kind (adversarial dir, tdd file: SPEC:83, SPEC:90).
- why not blocking: the text never states a kind, so a wrong build needs the guess that the implementer picks the kind the coordinator does not expect.
- concrete trace: the brief passes `--output .dev/x/` (a directory) to `/sc:analyze`; the implementer made the flag file-valued; the contract lands at `.dev/x.return-contract.yaml` or the command errors, and the coordinator opens `.dev/x/return-contract.yaml` and finds nothing, so WC-5 reports `failed`.
- recommendation: one sentence per new flag, or a rule "a newly added output flag is directory-valued". Quality impact: Completeness -1, Testability -1.

### F-02 WC-9 needs "the command's own explicit flag" that the spec never names for the commands that need it
- severity label: MAJOR; graded: Medium; priority High; expert: Wiegers, Cockburn
- issue: WC-9 says outward defaults turn on "only through the command's own explicit flag written in the brief" (SPEC:67). The rows that rely on it give no flag: post-release "VM, real-target install, commit and PR off unless the brief authorizes them" (SPEC:113), task "EXEMPT commit/push refused unless authorized" (SPEC:121), pr-submit under D3(b) (SPEC:114, SPEC:241), D4(a) "passes the command's explicit flag" (SPEC:245). The inventories show these confirmations are conversational ("unless the user pre-authorized them this session": INV-B:79) and task's commit/push have no flag at all (INV-B:204). Only auggie-review has a named flag (`--post-pr`, SPEC:100; its existence is UNVERIFIED because INV-A:38 names only `--no-post-pr`). AC-4.2 tests "with no authorization flags" (SPEC:209) as if they existed.
- consequence: safe by default (nothing authorizes), but D4(a) cannot be carried out, and an implementer must invent flag names, which breaks the "known before dispatch" brief template in SPEC:73.
- recommendation: name the flags or state that D4(a) needs them designed in P4. Quality impact: Completeness -1.

### F-03 Fixed four-value status set versus "existing contracts keep their fields"
- severity label: MAJOR; graded: Medium; priority Medium; expert: Wiegers, Adzic
- issue: WC-4 says commands with a contract "keep their fields and add the missing ones" (SPEC:62); Decisions fixes `status` to `succeeded|partial|failed|blocked` (SPEC:262); WC-5 and check 7.2-3/4 map and assert that set (SPEC:63, SPEC:182-183). The inventories name `status` for workflow (INV-B:272) and `report_path` for troubleshoot/reflect, but no inventory line lists any existing command's status values. Workflow, brainstorm and adversarial get "None" or filename-only fixes (SPEC:83, 84, 92), so their existing vocabulary is never reconciled; AC-0.4 skips the contract check for P0 for that reason (SPEC:194) and no later check covers workflow.
- recommendation: add one inventory-backed line per existing contract giving its status values, or an UNVERIFIED item. Quality impact: Consistency -1.

### F-04 WC-10 threshold disagrees with the check that tests it
- severity label: MINOR-MAJOR; graded: Medium; priority Medium; expert: Whittaker (FR-2.2 divergence), Wiegers
- issue: WC-10 splits a blocking tool call only when it is "longer than 5 minutes" into waits of at most 4 minutes (SPEC:68). The pr-submit row requires each iteration under 4 minutes (SPEC:114) and AC-4.3 requires "no single tool call exceeds 240 s" (SPEC:210). A 4.5-minute call passes WC-10, fails AC-4.3, and with a heartbeat every 5 minutes can still miss one.
- recommendation: one threshold (240 s) in WC-10. Quality impact: Consistency -1.

### F-05 `index` row and UNVERIFIED item 6 contradict each other
- severity label: MINOR-MAJOR; graded: Medium; priority Medium; expert: Wiegers, Adzic
- issue: item 6 says section 3 "refuses or pins" business-panel socratic, explain interactive and index's knowledge-base mode "regardless" of whether they wait (SPEC:277). The index row instead says "state that knowledge-base mode does not wait (whether it does is UNVERIFIED)" (SPEC:111). Following the row writes a possibly false statement into the command; following item 6 would refuse or pin. The live check would catch a wait only via `agentWait` or `AskUserQuestion` (SPEC:181, 184), and `INV-A:54` says the file describes no gate.
- recommendation: make index consistent with the other two (refuse the mode under `--unattended`). Quality impact: Consistency -1.

### F-06 Capability and structure changes to standalone commands sit outside SA-1/SA-4's stated tests
- severity label: MAJOR; graded: Medium; priority Medium; expert: Wiegers, Fowler
- issue: SA-1 says standalone behaviour is unchanged (SPEC:146). The explain row adds Write to its allowed tools unconditionally (SPEC:108), and business-panel moves frontmatter out of a code block "effect on loading UNVERIFIED" (SPEC:102). SA-4 lets such edits through as "documented defects" (SPEC:149), but `INV-A:48` calls explain's output location UNVERIFIED and describes no defect, so a read-only explainer gains write capability for every person. No acceptance check covers either edit (AC-1.3 samples only two commands run without `--unattended`, SPEC:197).
- recommendation: scope the Write grant to unattended mode or add a standalone check. Quality impact: Consistency -1, Testability -1.

### F-07 `--unattended` together with `--interactive` (or `--yes`) is undefined for most commands
- severity label: MINOR-MAJOR; graded: Medium; priority Medium; expert: Whittaker (FR-2.2, FR-2.3), Adzic
- issue: refusal under `--unattended` is specified for cleanup, improve, roadmap, business-panel, explain, pr-submit and test (SPEC:102, 103, 108, 110, 114, 118, 123). For adversarial, brainstorm, release-split, reflect and the others, "never `--interactive`" is a brief rule (SPEC:83-84, 89), not a command rule. A person or brief that passes both flags gets whichever of the two the implementer coded.
- recommendation: one general sentence in the contract file: `--unattended` wins and any person-facing flag is refused. Quality impact: Completeness -1.

### F-08 Acceptance check AC-2.2 disagrees with the optional `ask` path of WC-3
- severity label: MAJOR; graded: Medium; priority Medium; expert: Adzic, Wiegers
- issue: WC-3 lets the worker session "ask the coordinator once" instead of ending blocked (SPEC:61). AC-2.2 passes only on `worker_done --outcome failed` with contract `status: blocked` (SPEC:200), and check 7.2-3 waits for `worker_done` (SPEC:182). A conforming worker that takes the `ask` route sends a `question` message and no `worker_done`, so the check hangs or fails although the worker obeyed WC-3. Orca returns `question` from `check --wait` (CAPS:63).
- recommendation: AC-2.2's brief says "do not use ask", or the check accepts a `question` and replies. Quality impact: Testability -1.

### F-09 Briefs for some ready commands omit the output the spec says every brief carries
- severity label: MINOR; graded: minor note; expert: Cockburn
- issue: SPEC:73 says every brief states the output directory or file "so the report path is known before dispatch (workflow excepted)". The 3.1 "Brief must pass" cells for troubleshoot and reflect name no output (SPEC:88, SPEC:91), and their default directories carry a timestamp (INV-B:112, INV-B:242), so the path is learnt only from `worker_done --report-path`. The same reading applies to research (`claudedocs/research_*_[timestamp].md`, INV-B:132). The workflow exception is named; these are not.

### F-10 Phase 0 order is stated two ways
- severity label: MINOR; graded: minor note; expert: Cockburn, Fowler
- issue: section 1.4 says "Phase 0 therefore starts with live smoke runs" (SPEC:43). The P0 row writes the contract file, `KNOWN_CORE_FILES` entry, routing-guide section and tests first, "Then" runs the smoke runs, and the row's own reason says they "test the decision before anything is built on it" (SPEC:158). AC-0.4 says a failed smoke run "reopens section 1" (SPEC:194).

### F-11 Section 1.4(2) states as fact something the evidence only suggests
- severity label: MAJOR; graded: Medium; priority Medium; expert: Wiegers, Nygard
- issue: the spec says a command's own `AskUserQuestion` or chat question "comes after readiness, so it does not fail `worker-start`" (SPEC:44). CAPS:47 shows the Claude task is passed on the command line and readiness waits for a fresh composer or an idle TUI; a command whose first step is a person gate (for example `/sc:tdd "auth"`, INV-B:219) is therefore executing while Orca is still waiting for readiness. The inventory's only proof (CAPS:49) is a launch wrapper, not a command gate, and `CAPS:52` ("healthy, not failed") applies "once `input_accepted`". The consequence is that a stall may surface as a failed start at `agent_readiness` instead of as `agentWait`, which changes which signal the coordinator looks for. Under `--unattended` the gate is gone, which limits the impact to briefs without the flag.
- recommendation: soften to "probably" and add it to the UNVERIFIED list, or test it in AC-0.4. Quality impact: Clarity -1.

=== ARCHITECTURE ANALYSIS ===

### F-12 Retry with a "fresh output directory" collides with a path fixed in the brief, and a stale contract is possible
- severity label: MAJOR; graded: Medium; priority High; expert: Nygard (lead), Hohpe, Whittaker (FR-2.4 sequence)
- issue: WC-6 says a command without a resume flag "writes each run into a fresh output directory" (SPEC:64); 20+ rows say "fresh dir". WC-4 and SPEC:73 make the coordinator pass the directory, and `worker-start --retry-of` reuses the Task (CAPS:116), so the retry gets the same directory unless the coordinator rewrites the brief, which the spec never says. Nothing tells a command to remove or overwrite a pre-existing `return-contract.yaml` at start. Attack: attempt 1 ends `status: failed` and leaves its contract in `<dir>`; attempt 2 is killed before it writes anything; the coordinator opens `<dir>/return-contract.yaml`, reads attempt 1's stale `failed` (or a stale `succeeded` from an earlier success), and WC-5's "no report means failed" never fires because a file exists.
- why not blocking: the failing sequence needs attempt 2 to die before its first write, and the text does not say the file is kept.
- recommendation: one sentence: a command deletes or truncates its contract path at start, or the retry brief gets a new directory. Quality impact: Completeness -1, Reliability -1.

### F-13 Shared paths remain for commands marked "ready today"
- severity label: MAJOR; graded: Medium; priority Medium; expert: Whittaker (FR-2.3 sentinel collision, FR-2.5 accumulation), Nygard
- issue: WC-11 forbids two workers writing one file (SPEC:69). cleanup-audit writes a fixed `.claude-audit/` and the row only says "one audit per worktree at a time" (SPEC:85; INV-A:42); index-repo writes the fixed `PROJECT_INDEX.md` (SPEC:86; INV-A:53); both are "ready today" with the fix pending in P1. The spec has no coordinator rule (in 2.3 or the brief template) that stops two such Tasks sharing a worktree. save's per-session key is `<key>-<session-or-timestamp>` (SPEC:119), so two workers started in the same timestamp tick can collide when the session id is not used (AC-3.4 passes two workers started apart, SPEC:207).
- recommendation: add to section 2.3 "never run two Tasks that name the same fixed output path in one worktree" and prefer the session id for save. Quality impact: Reliability -1.

### F-14 Under `--unattended`, tasklist's reflect fan-out starts a remediation hand-off the spec never describes
- severity label: MAJOR; graded: Medium; priority Medium; expert: Fowler, Hohpe
- issue: reflect under `--unattended` makes `--remediate` "follow the existing headless auto-accept rule" (SPEC:88), and tasklist Stage 10.5 passes `--unattended` to each reflect while keeping `--remediate` (SPEC:122). The headless rule auto-accepts auto-fixable registers and skips the gates (INV-B:109), and `--remediate` hands off to sc:workflow or task-builder (INV-B:109, INV-B:36). So a tasklist worker can start extra remediation packages, with their own writes, with no mention in the tasklist row, its contract, or any acceptance check. INV-B:215 recommended dropping `--remediate` in Stage 10.5. Both rows are P2 and no order between them is stated.
- recommendation: say what the auto-accept does for tasklist or drop `--remediate` as INV-B:215 advised. Quality impact: Completeness -1.

### F-15 `blocked` always maps to a failed Orca Task, so a human-gated pause blocks the DAG until a retry
- severity label: MINOR-MAJOR; graded: Medium; priority Medium; expert: Hohpe, Fowler
- issue: WC-5 maps `blocked` to `--outcome failed` (SPEC:63). A failed Task keeps its dependents blocked until a `--retry-of` replacement completes (CAPS:90), and Orca has a `blocked` Task status and decision gates for coordinator-owned decisions (CAPS:89, CAPS:91, CAPS:65). The spec chooses `ask` or failure and never considers the gate route or states the consequence for the DAG. This is a design choice with a cost the spec does not state, not an error.
- recommendation: add one line in Decisions. Quality impact: Clarity -1.

### F-16 Undefined behaviour for a missing, malformed or self-contradicting contract
- severity label: MAJOR; graded: Medium; priority Medium; expert: Nygard (FR-14.3 zero/empty), Whittaker (FR-2.1)
- issue: WC-5 covers "no report exists" only (SPEC:63). A zero-byte file, invalid YAML, a `status` outside the set, `status: succeeded` with a non-empty `blocked_question`, or `status: blocked` with an empty question (AC-2.2 requires non-empty, SPEC:200) are unspecified. Check 7.2-4 catches the first three in tests only (SPEC:183); at run time the coordinator has no rule.
- recommendation: "an unreadable or invalid contract is treated as no report". Quality impact: Completeness -1.

### F-17 Coordinator procedure for a parked or blocked worker is thin
- severity label: MINOR; graded: minor note; expert: Nygard, Newman
- issue: section 1.4(2) says a command prompt "stalls silently" and shows only through `agentWait` or a missing report (SPEC:44); 7.2 tests for it (SPEC:181) but section 2.3 gives the coordinator no runtime steps for a non-null `agentWait` (reply, stop, retry) or for a `blocked` contract beyond "open the report" (SPEC:73). The Orca guide owns recovery (CAPS:123-126), and the spec's non-goal 3 excludes a coordinator program (SPEC:215).

### F-18 Coupling of 27 command edits to one flag name, with deviating semantics per command
- severity label: MINOR; graded: minor note; expert: Fowler, Newman
- issue: `--unattended` is one name carrying four meanings (refuse a mode, pin a value, resolve blocked, imply other flags: SPEC:100-125). Interface segregation would give the shared contract file a table of the five resolution kinds. Section 2.1 already centralizes the rules; this is a readability note only. API evolution (Newman): no version field is required in the contract (WC-4 lists no `schema_version`), though existing contracts carry versions (workflow "contract 1.1", INV-B:272).

### F-19 Detail notes on text that depends on unreadable files
- severity label: MINOR; graded: minor note; expert: Fowler
- tasklist row says its reflect fan-out "runs one layer below the worker" (SPEC:122), but INV-B:210 shows worker, then N reflect subagents, then reflect's own agents: two layers below, still inside the three-layer figure of INV-A:14, whose nested-spawn behaviour INV-B:314 marks UNVERIFIED.
- SPEC:76 and SPEC:139-140 treat pr-submit as one of the 27 and as a coordinator-side command at once; with the recommended D3(a) the 27/6 counts effectively become 26/7.
- AC-1.1 ("every P1 command ... not `load`", SPEC:195) does not say whether the ready commands that get small P1 fixes (adversarial, cleanup-audit, index-repo: SPEC:159) also need the `## Unattended mode` section; SPEC:76 and 79 imply they do.
- The candidate states 43 commands (SPEC:76). The sandbox has no `cmd/` folder, so this is UNVERIFIED here. This session's own skill list also names `/sc:graph`, `/sc:impact` and `/sc:issue`, which appear in neither inventory (INV-A:3, INV-B:3); I could not check them in the sandbox and make no claim about them.

=== CROSS-CUTTING ANALYSIS ===

### F-20 Acceptance check AC-C1 versus SA-2 and SA-5
- severity label: MAJOR; graded: Medium; priority Medium; expert: Wiegers, Adzic
- issue: SA-2 allows an Orca mention "as an example of a caller's question channel inside the contract file" (SPEC:147); SA-5 and P0 add an Orca section to the routing guide (SPEC:150, SPEC:158). AC-C1 greps `src/superclaude/core` as well, excluding only `ccsession-tag`, and its pass condition is "prints nothing" (SPEC:172, SPEC:167 "every check must pass"). If the allowed example is written as `orca orchestration ask`, or the routing section names an `orca worktree` or `orca orchestration` command, AC-C1 fails Phase 0 even though SA-2 and SA-5 permit the text. E5 records that the routing guide holds zero mentions today (SPEC:25).
- recommendation: exclude `WORKER-CONTRACT.md` and the routing guide from AC-C1, or limit SA-2's example wording. Quality impact: Consistency -1.

### F-21 Counts check (informational, no defect)
- 21 + 22 = 43 commands; 10 + 27 + 6 = 43; the 27 rows of SPEC:97-125 equal the 13 (INV-A:75-83) + 14 (INV-B:289-299) needs-change commands; phase rows P1 (9), P2 (15), P3 (4), P4 (3) cover them, with P2 including four ready commands. All reconcile.

## Whittaker attack summary (FR-3 template)

- I can break this specification by **Sequence Attack (FR-2.4)**. The invariant at **WC-4/WC-5/WC-6** ("a report exists exactly when the run produced it") fails when **a retry reuses the brief's directory and dies before writing**. Concrete attack: before: `<dir>/return-contract.yaml` holds `status: failed` from attempt 1; attempt 2 starts, is killed; after: the file is unchanged and the coordinator reads `failed` as attempt 2's result. See F-12. Severity: MAJOR (ambiguous under attack); graded Medium.
- I can break this specification by **Divergence Attack (FR-2.2)**. The invariant at **WC-10** fails when **a tool call lasts 4.5 minutes**. Concrete attack: WC-10 allows it (not longer than 5 minutes), AC-4.3 rejects it (above 240 s). See F-04. MAJOR/Medium.
- I can break this specification by **Sentinel Collision Attack (FR-2.3)**. The invariant at **WC-4** (one `return-contract.yaml` name for all commands) fails when **a nested command writes the same filename in the same directory**. Checked: adversarial uses `<output>/adversarial/` (SPEC:62) and tasklist's reflects use timestamped directories (INV-B:112), so no collision was found; a nested command called with the parent's `--output` would collide, and the spec does not forbid passing the parent's directory down. MINOR.
- I can break this specification by **Zero/Empty Attack (FR-2.1)**. The invariant at **WC-5** fails when **the contract is empty or its `status` is missing**. See F-16.
- I can break this specification by **Accumulation Attack (FR-2.5)**. The invariant at **WC-11** fails when **two workers share a fixed path**. See F-13.

## Guard Condition Boundary Table (Nygard builds, Crispin validates, Whittaker attacks; FR-10 completeness)

Guards found in the spec: G1 WC-10 wait split; G2 WC-5 outcome mapping; G3 WC-4 path rule (dir or file); G4 WC-2 gate resolution under `--unattended` (including `--monitor 1` refusal); G5 WC-1 readiness fallback; G6 WC-6 resume or fresh run. Classes left out are named in the line under the table. The Status column uses GAP only where a stated behaviour is missing; per FR-8/FR-9 each GAP is graded by consequence (all Medium here, see the finding in the last column of the notes).

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|---|---|---|---|---|---|---|
| G1 split-wait | SPEC:68 | Zero/Empty | wait of 0 s | false | none needed, no wait | OK |
| G1 split-wait | SPEC:68 | One/Minimal | wait of 1 s | false | not split | OK |
| G1 split-wait | SPEC:68 | Typical | 3 min wait | false | not split, heartbeat unaffected | OK |
| G1 split-wait | SPEC:68, SPEC:210 | Maximum/Overflow | 3600 s eval (INV-A:65) | true | split into waits of at most 4 min | OK |
| G1 split-wait | SPEC:68 vs SPEC:210 | Legitimate Edge Case | 4.5 min call | false (WC-10) / fail (AC-4.3) | WC-10 allows, AC-4.3 rejects (F-04) | GAP |
| G2 outcome | SPEC:63 | Zero/Empty | no report file | n/a | `--outcome failed` | OK |
| G2 outcome | SPEC:63 | Zero/Empty | zero-byte or invalid YAML file | unspecified | not specified (F-16) | GAP |
| G2 outcome | SPEC:63 | One/Minimal | `status: succeeded` | true | `--outcome succeeded` | OK |
| G2 outcome | SPEC:63 | Typical | `status: partial` | true | `succeeded`, first sentence says partial | OK |
| G2 outcome | SPEC:63 | Sentinel Value Match | `status: blocked` | true | `failed`; Task failed, dependents blocked (F-15) | OK |
| G2 outcome | SPEC:63 | Legitimate Edge Case | `status` outside the four values (existing contracts, F-03) | unspecified | not specified | GAP |
| G3 path rule | SPEC:62 | Zero/Empty | empty `--output` | unspecified | not specified | GAP |
| G3 path rule | SPEC:62 | Typical | `--output <dir>` | true | `<dir>/return-contract.yaml` | OK |
| G3 path rule | SPEC:62 | Legitimate Edge Case | new `--output` flag of unspecified kind (F-01) | unspecified | not specified | GAP |
| G3 path rule | SPEC:62 | Sentinel Value Match | file name already ends `.return-contract.yaml` or exists (F-12) | unspecified | not specified | GAP |
| G4 gate resolution | SPEC:60 | Typical | gate hit with documented default | true | default applied | OK |
| G4 gate resolution | SPEC:60 | Maximum/Overflow | two person-facing flags together (`--unattended --interactive`, F-07) | unspecified | stated for 7 commands, not the rest | GAP |
| G4 gate resolution | SPEC:114 | Legitimate Edge Case | `--monitor 0`, `2`, `3` with `--unattended` | not stated | only `--monitor 1` is refused | GAP |
| G5 readiness | SPEC:59 | Typical | fallback at 30 s | true | passes (EVIDENCE via CAPS:49) | OK |
| G5 readiness | SPEC:59 | Maximum/Overflow | fallback above ~45 s | false | fails again (CAPS:49) | OK |
| G5 readiness | SPEC:59 | Legitimate Edge Case | "well inside" the limit | unspecified | no number in the requirement itself | GAP |
| G6 resume | SPEC:64 | Zero/Empty | no prior state | n/a | fresh run | OK |
| G6 resume | SPEC:64 | Typical | resume flag with state | true | resumes (per-command column) | OK |
| G6 resume | SPEC:64 | Legitimate Edge Case | retry with the same brief directory (F-12) | unspecified | "fresh directory" conflicts with SPEC:73 | GAP |

Classes left out: Sentinel Value Match for G1 (no sentinel in a duration), for G5 and G6 (no magic value); One/Minimal for G3 to G6 (one value and the typical value coincide); Maximum/Overflow for G2, G3 and G6 (a status or path has no capacity; a path longer than the filesystem limit is not a spec concern).

GAP entries are Medium unless they name a concrete wrong outcome; none does (see findings F-01, F-04, F-07, F-12, F-16). They propagate as priority invariant candidates to `sc:adversarial` AD-1 if the spec is revised.

## Pipeline Dimensional Analysis (Fowler leads, Whittaker attacks)

Trigger: the spec describes a multi-stage flow where the count may diverge: N planned Tasks, M ≤ N reports usable by a consumer (SPEC:39 splits work into several troubleshoot workers, then one adversarial worker on their reports).

```text
[Coordinator: N Tasks] --> [Workers run: N workers] --> [worker_done: N messages]
                                                          |
                                                          v
                                  [Contract outcomes: S succeeded/partial, F failed/blocked, S + F = N]
                                                          |
                                                          v
                                  [Consumer (e.g. adversarial): expects S usable reports]  <-- divergence N -> S
                                  [Orca dependents: stay blocked while any dependency Task is failed (CAPS:90)]
```

Result: no mismatch of the FR-19 kind. The spec does not say the consumer processes "all N"; Orca keeps dependents of a failed Task blocked (CAPS:90) and the coordinator starts each ready Task itself (CAPS:92). Two notes: `partial` counts as `succeeded` (SPEC:63, SPEC:263), so a consumer sees a Task as done with fewer deliverables; and the consumer's input list on partial or blocked inputs is not defined (F-15, F-16). No CRITICAL finding.

## Quality metrics (0-10)

- Clarity 8, Completeness 7, Testability 7, Consistency 7.
- The strong parts: the decision is argued against a rejected alternative with evidence, evidence gaps are stated (SPEC:41-45), every changed command has a row, and the acceptance checks are executable.

## Follow-up candidates (Medium and minor, no revision triggered)

Medium: F-01, F-02, F-03, F-04, F-05, F-06, F-07, F-08, F-11, F-12, F-13, F-14, F-15, F-16, F-20.
Minor notes: F-09, F-10, F-17, F-18, F-19. F-21 is informational.
No issue has been opened; the question to the user is not asked in this sandbox.

## Brief clauses overridden

None. The brief narrowed nothing and widened nothing; it asked for a whole-document first review, which this is.

## Reviser brief

None: no blocking finding is open. (A Reviser brief lists only blocking ids; the list is empty.)

verdict: PASS

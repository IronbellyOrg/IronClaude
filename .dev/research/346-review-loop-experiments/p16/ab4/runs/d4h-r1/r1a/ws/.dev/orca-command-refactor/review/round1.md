review: 1 of 3

# /sc:spec-panel critique, round 1

- Candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md` (285 lines)
- Candidate SHA-256: `d3cdbe573e57303b9ce6c93d1fe98ba18fb7cb1a15773d926bf6a0c31425200d` (matches the hash in lint-1.md)
- Baseline: none (first review). Prior report: none.
- Mode: critique. Focus: requirements, architecture.
- Brief: FIRST-REVIEW prompt, `~/.claude/rules/prompts/document_review_loop_prompts.md` (read in full, step by step).
- Reviewer model: claude-haiku-5-5.
- Coordinator steps not performed here: the second first-review, the MERGE rule and the VERIFY prompt.

## Citation legend and check scope

- `SPEC:n` = line n of the candidate. `INV-A:n` = `inventory/commands-a.md:n`. `INV-B:n` = `inventory/commands-b.md:n`. `CAPS:n` = `inventory/orca-capabilities.md:n`. All paths are relative to `.dev/orca-command-refactor/`.
- Checked: every SPEC line cited here; every INV-A, INV-B and CAPS citation below (the inventory files are the only evidence available in this sandbox); the spec's internal references (WC, SA, AC, D, P and section numbers).
- UNVERIFIED: every citation into `src/`, `.dev/` outside this run folder, `~/.claude/`, `CLAUDE.md`, or Orca's bundled files. Where I say "as cited", I did not re-read the source.

## Lint evidence

`review/lint-1.md` reports `Checks: REF. Findings: 0.` and "No findings." It names no lint id, so there is none to confirm or dismiss. It is bound to the candidate SHA-256 above.

## Coverage

I read the whole candidate (SPEC:1-285), all of SPEC section 2 (WC-1 to WC-12), section 3.1 and 3.2 (every row), section 4, section 5 (SA-1 to SA-6), section 6 phases, section 7 checks (AC-C1 to AC-4.3), section 8 and section 9 (D1 to D5), and the three inventories in full. I applied the Whittaker attack methodologies to the contract and to the acceptance checks. I did not open the Orca guides or any source file.

## Guard Condition Boundary Table (mandatory; triggered by the contract's conditional rules)

Enumerated guards: G1 WC-2 gate resolution; G2 WC-3 ask; G3 WC-4 contract path; G4 WC-5 outcome mapping; G5 WC-9 outward flag; G6 WC-10 wait size; G7 WC-12 consumer_fenced; G8 WC-1 readiness fallback; G9 unattended switch (D1 and SA-1); G10 WC-11 default output paths; G11 AC 7.2 step 2 agentWait pass condition. The per-command gate rows of SPEC:97-125 are instances of G1; each row names a WC-2 resolution (a), (b) or (c), so none is blank.

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|---|---|---|---|---|---|---|
| G4 WC-5 | SPEC:63 | Zero/Empty | contract file exists, 0 bytes | falls under "otherwise" | `succeeded`; SPEC:183 (`test -s`) treats the same file as a failure | GAP (F3, blocking) |
| G4 WC-5 | SPEC:63 | One/Minimal | `status: partial` | "otherwise" | `succeeded` (SPEC:263) | OK |
| G4 WC-5 | SPEC:63 | Typical | `status` succeeded / failed / blocked | direct map | succeeded / failed / failed | OK |
| G4 WC-5 | SPEC:63 | Maximum/Overflow | `status: done` (outside the four values) | "otherwise" | `succeeded`; SPEC:62 says "one of" four but gives no rule for other values | GAP (F3, blocking) |
| G4 WC-5 | SPEC:63 | Sentinel Value Match | audit verdict FAIL inside `status: succeeded` | verdict not read | `succeeded` (stated) | OK |
| G4 WC-5 | SPEC:63 | Legitimate Edge Case | no file at the contract path after a pre-creation STOP | "no report exists" | `failed`; depends on F1 for the path | OK (conditional on F1) |
| G3 WC-4 | SPEC:62 | Typical | adversarial, `--output D` | required `D/return-contract.yaml` | SPEC:83 requires `D/adversarial/return-contract.yaml` | GAP (F1, blocking) |
| G3 WC-4 | SPEC:62 | Sentinel Value Match | `--output` is a file (init-lite SPEC:87, tdd SPEC:90) | `<output-dir>` undefined | no rule | GAP (F1, blocking) |
| G3 WC-4 | SPEC:62 | Zero/Empty | command with no output flag (workflow SPEC:92) | no output dir | contract under `.dev/tasks/to-do/<id>/` | GAP (F1, blocking) |
| G1 WC-2 | SPEC:60 | Typical | gate with a documented default, no flag | default applies | (a) | OK |
| G1 WC-2 | SPEC:60 | Zero/Empty | gate with no default, no flag | blocked | (c) | OK |
| G1 WC-2 | SPEC:60 | Legitimate Edge Case | outward default (auggie-review posting), no flag | off | WC-9, SPEC:67 | OK |
| G2 WC-3 | SPEC:61 | Typical | coordinator answer with a value | re-invoke with the answer as a flag | SPEC:61 | OK |
| G2 WC-3 | SPEC:61 | Zero/Empty | empty answer, or no answer | unspecified | no rule | GAP (M5, Medium) |
| G2 WC-3 | SPEC:61 | Maximum/Overflow | ask times out | resume same message ID | SPEC:61; default timeout UNVERIFIED (CAPS:68) | OK (UNVERIFIED) |
| G5 WC-9 | SPEC:67 | Sentinel Value Match | outward flag written without a user instruction | honored | D4 open, SPEC:245 | GAP (M17, Medium) |
| G5 WC-9 | SPEC:67 | Zero/Empty | no outward flag | off | SPEC:67 | OK |
| G6 WC-10 | SPEC:68 | Maximum/Overflow | one tool call of 4 min 1 s | must split | SPEC:68 | OK |
| G6 WC-10 | SPEC:68 | Legitimate Edge Case | wait in standalone mode | scope not stated | SPEC:146 says standalone is unchanged | GAP (M10, Medium) |
| G7 WC-12 | SPEC:70 | Sentinel Value Match | `check` returns consumer_fenced | stop, no worker_done | SPEC:70 | OK |
| G7 WC-12 | SPEC:70 | Legitimate Edge Case | empty `check` | not replaced; continue | CAPS:67 | OK |
| G7 WC-12 | SPEC:70 | Zero/Empty | Orca runtime unreachable mid-run | unspecified | no rule | GAP (M15, Medium) |
| G8 WC-1 | SPEC:59 | Maximum/Overflow | prompt fallback "well inside" the 60 s limit | threshold undefined | none | GAP (M7, Medium) |
| G8 WC-1 | SPEC:59 | Typical | fallback at 30 s | passes | CAPS:49 (EVIDENCE:45) | OK |
| G9 SA-1 | SPEC:51, :146 | Zero/Empty | flag absent | standalone | SA-1 | OK |
| G9 D1 | SPEC:228 | Sentinel Value Match | the text `--unattended` inside quoted user content | switches mode | not stated | GAP (M6, Medium) |
| G10 WC-11 | SPEC:69 vs SPEC:146 | Typical | standalone `index-repo`, no flag | default stays `PROJECT_INDEX.md` (SA-1) | WC-11 timestamps default output paths | GAP (F4, blocking) |
| G11 AC 7.2-2 | SPEC:181 | Sentinel Value Match | worker parked in `ask` | `agentWait` may be non-null | pass condition fails it | GAP (M14, Medium) |

Classes left out, with the one-line reason: G1 and G5 Maximum/Overflow (the number of gates and outward flags has no bound the text states; the row set is the list in SPEC:97-125). G4 One/Minimal for `blocked` (same result as `failed`, covered by the Typical row). G7 One/Minimal (one check call, no state). G11 Legitimate Edge Case (no spec-stated edge beyond the Sentinel row). Pipeline Dimensional Analysis (FR-17) is not triggered: no data flow in the spec changes item counts through filtering or aggregation; fan-out is per command and is not a data pipeline. Pipeline Flow Diagram and State Variable Registry are not required (focus is not correctness).

## Findings

Severity follows the critique scale (CRITICAL, MAJOR, MINOR). Grade follows the consequence rule. Blocking findings are F1 to F4. Medium findings and minor notes are listed under follow-up candidates and do not feed the Reviser brief.

### === REQUIREMENTS ANALYSIS ===

**F1. The contract path rule in WC-4 cannot be followed by the commands the spec lists.** Severity MAJOR. Grade: blocking. Expert: Wiegers (lead), Cockburn.
- WC-4 says the contract is `<output-dir>/return-contract.yaml` where `<output-dir>` is the directory passed as `--output`/`--output-dir` (SPEC:62). SPEC:73 says the coordinator's brief gives the report path "so the report path is known before dispatch".
- SPEC:83 (adversarial) requires `<output>/adversarial/return-contract.yaml`, a subfolder. SPEC:87 (init-lite) takes `--output <file>`, not a directory. SPEC:90 (tdd) takes `--output <file>`. SPEC:92 (workflow) has no output flag; its contract lives under `.dev/tasks/to-do/<id>/`. SPEC:85 (cleanup-audit) uses a fixed `.claude-audit/` path. SPEC:105 (cli-portify) leaves the location unnamed.
- Grading sentence: an implementer who follows WC-4 and SPEC:73 has the coordinator open `<output-dir>/return-contract.yaml` for adversarial, but SPEC:83 makes the file `<output-dir>/adversarial/return-contract.yaml`, so the coordinator opens a path that does not exist.
- Recommendation: state one rule per command in a table (path, and whether it is file-valued or directory-valued), or make every command take `--output-dir` and write the contract at its root. Priority: high. Quality impact: consistency.

**F2. The P0 smoke runs use a brief that the contract says must carry `--unattended`, but P0 is before any command accepts that flag.** Severity MAJOR. Grade: blocking. Expert: Cockburn, Adzic.
- SPEC:73 says each Task's brief carries "the exact command line including `--unattended`". SPEC:180 says step 1 uses "the brief per section 2.3".
- SPEC:158 (P0) is "no command edits"; the flag is added in P1 (SPEC:159). AC-0.4 (SPEC:194) runs "the 7.2 live check" on `/sc:troubleshoot`, `/sc:workflow` and `/sc:adversarial` with command lines that have no `--unattended`.
- Grading sentence: an implementer who follows AC-0.4 runs the P0 evidence with briefs that SPEC:73 forbids, so the P0 result, which section 1.4 (SPEC:43-44) treats as the test of the decision, is not a test of the contract's briefs.
- Recommendation: say that P0 briefs omit `--unattended` and that P0 evidence tests the Orca launch only, or move the `--unattended` requirement to P1 in SPEC:73 and SPEC:180. Priority: high. Quality impact: consistency, testability.

**F3. WC-5 maps an empty or malformed contract to `succeeded`.** Severity MAJOR. Grade: blocking (FR-8 GAP with a concrete wrong outcome). Expert: Whittaker (FR-2.1 Zero/Empty), Wiegers.
- SPEC:63: `--outcome failed` only "when the report says failed or blocked, or no report exists"; `--outcome succeeded` "otherwise". SPEC:183 (step 4) treats an empty contract (`test -s`) as a failed check.
- Grading sentence: an implementer who follows SPEC:63 as written sends `--outcome succeeded` for a zero-byte contract or for `status: done`, because neither is "failed", "blocked" or "no report"; SPEC:183 says the same file must not pass.
- Recommendation: `succeeded` only for a parsed contract whose status is `succeeded` or `partial`; every other case (missing, empty, unparseable, unknown status) is `failed`. Priority: high. Quality impact: completeness.

**F4. WC-11 changes default output paths without limiting the change to unattended runs, which contradicts SA-1.** Severity MAJOR. Grade: blocking. Expert: Wiegers (traceability), Fowler.
- WC-11 (SPEC:69): "Default output paths carry a timestamp or the slug the coordinator passes". Only its second clause is scoped to unattended mode.
- SA-1 (SPEC:146): without `--unattended`, "every ... output path ... stays as it is today". The section 3.1 row for index-repo (SPEC:86) uses the fixed `PROJECT_INDEX.md` and resumes with `mode=update`.
- Grading sentence: an implementer who follows SPEC:69 gives standalone `/sc:index-repo` a timestamped default name, which breaks SA-1 as written, and the text does not say that WC-11 is limited to unattended runs.
- Recommendation: scope the first clause of WC-11 to unattended runs with a coordinator-passed slug, and state that standalone defaults are unchanged. Priority: high. Quality impact: consistency.

**M1. Section 3.1 says the ten commands "run as workers now", but eight of them name a phase-numbered fix.** Severity MAJOR. Grade: Medium. Expert: Wiegers.
- SPEC:79 ("These run as workers now ... The only command changes are the small fixes in the last column") against SPEC:83, :85, :86, :88, :90, :91, :92 (P1 or P2 fixes in the same rows). Two of these, tdd (SPEC:90) and troubleshoot (SPEC:91), keep a stall path that the "ready" label does not show: INV-B:219 (nested `/task` asks the user on several matching files) and INV-B:239 (`--depth deep` STOP).
- Recommendation: rename the heading to "ready after the named fixes", or list each row's stall paths and the flag that avoids them. Quality impact: consistency.

**M2. AC-C1 is weaker than SA-2 and scans the directory that the spec asks to change.** Severity MINOR. Grade: Medium. Expert: Wiegers (testability).
- SPEC:172 matches only lowercase `orca` or `orca-ide` followed by a space and a subcommand name. It misses `orca-cli`, uppercase `ORCA` (the spec's own placeholder, SPEC:180, :182) and `$ORCA`. It scans `src/superclaude/core`, where P0 adds an Orca section to HOW-WE-WORK (SPEC:158). SPEC:147 permits an Orca mention in the contract file, which AC-C1 would fail.
- Recommendation: case-insensitive `\b(orca|orca-ide|orca-cli)\b` over commands, skills and agents only, with the ccsession-tag exclusion. Quality impact: testability.

**M3. Partial maps to `succeeded`, and Orca unblocks dependents on `succeeded`.** Severity MAJOR. Grade: Medium. Expert: Fowler (dependencies), Hohpe.
- SPEC:63 and the Decisions row at SPEC:263 map `partial` to `succeeded`. CAPS:77 says a valid `worker_done` settles the Task automatically. CAPS:86 and CAPS:88 say the coordinator starts ready Tasks, and a Task whose dependencies are unmet is refused.
- Grading sentence: a coordinator that starts `task-list --ready` after `worker_done` starts the dependent on a partial deliverable, but the spec does not say to read the contract first; SPEC:73 orders reading after `worker_done` only for release.
- Recommendation: state that the coordinator reads `status` before any dependent start, or map `partial` to `failed` for Tasks that have dependents. Quality impact: completeness.

**M4 (Whittaker FR-2.4, Sequence Attack). Retry can start while the first attempt is still live.** Severity MAJOR. Grade: Medium. Expert: Whittaker, Nygard.
- I can break this specification by **sequence (retry while live)**. The invariant at **SPEC:64 (WC-6)** fails when **the coordinator retries a worker whose state is not settled**. Concrete attack: **worker A on `tdd --resume <task-file>` is reported `unverifiable` (CAPS:125 says absence never authorizes retry, CAPS:37 says the same for retry). The coordinator runs `worker-start --retry-of A --resume <task-file>`. A and B both write the same resume file. The first attempt's output is overwritten, which WC-6 forbids.**
- Recommendation: retry only after the first Dispatch is `exited` or settled; a resume directory held by a live Dispatch is never reused. Quality impact: completeness.

**M5. Nothing says who answers a worker's `ask`, or what happens when the answer is empty.** Severity MAJOR. Grade: Medium. Expert: Wiegers, Hohpe.
- WC-3 (SPEC:61) lets the worker ask the coordinator. SPEC:182 (step 3) loops on `worker_done,escalation,question` "until worker_done arrives" and does not reply to a `question`. CAPS:62 and CAPS:63 show the coordinator must answer with `reply`.
- Recommendation: add a coordinator duty to answer or escalate every `question`, and a rule that the coordinator never answers a clarification from its own judgment (it relays the person's answer or fails the Task). Quality impact: completeness.

**M6 (Whittaker FR-2.3, Sentinel Collision). The `--unattended` switch can be triggered by text that is not a control signal.** Severity MINOR. Grade: Medium. Expert: Whittaker, Wiegers.
- I can break this specification by **sentinel collision**. The invariant at **SPEC:228 (D1)** fails when **the string `--unattended` appears in user content that is passed as an argument (a spec or a brief that quotes the flag)**. Concrete attack: **a person pastes a brief quoting the flag inside quoted content; the command reads it as a control token and resolves its gates as blocked, against SA-1 (SPEC:146).**
- D1 also says the flag "cannot misfire on a person" (SPEC:228). Nothing in the spec supports that claim. Recommendation: require the flag as a standalone token outside quoted content, or pass the mode through a brief file the command reads; drop the unsupported claim. Quality impact: testability.

**M7. "well inside the readiness limit" has no number.** Severity MINOR. Grade: Medium. Expert: Wiegers (measurability).
- WC-1 (SPEC:59). The only measured points are a 30 s fallback that passed and a 45 s limit that failed (CAPS:49, which cites EVIDENCE:45 and :56). Recommendation: give a numeric ceiling, for example at most 30 s, and state how it relates to a raised `--timeout-ms`. Quality impact: testability.

**M10. WC-10 has no scope.** Severity MINOR. Grade: Medium. Expert: Wiegers.
- WC-10 (SPEC:68) is not limited to unattended mode, while SA-1 (SPEC:146) says standalone behavior is unchanged. Recommendation: state that wait splitting is behavior-preserving in both modes, or scope it. Quality impact: consistency.

**M13. Traceability gaps.** Severity MINOR. Grade: Medium. Expert: Wiegers (traceability).
- WC-1 (SPEC:59), WC-7 (SPEC:65), WC-11 (SPEC:69) and WC-12 (SPEC:70) have no section 7 check. WC-11 is checked only for `save` (AC-3.4, SPEC:207). AC-0.4 (SPEC:194) says "no Agent-tool wrapper, verified in the step-5 transcript", but step 5 (SPEC:184) searches only for `AskUserQuestion`, not for an Agent call. Recommendation: add checks for these rows and a transcript check for Agent calls. Quality impact: testability.

**M11. The evidence statement in E3 conflicts with section 1.4.** Severity MINOR. Grade: Medium. Expert: Adzic (evidence), Fowler.
- SPEC:23 (E3) cites a P3 return contract with `invocation_method: "skill-direct"`. INV-A:13 and INV-A:35 describe that as a direct-route Orca-worker run.
- SPEC:43 (section 1.4, gap 1) says the only end-to-end proof is PR #329, which proves only the nested route, and that no direct run exists.
- Recommendation: reconcile the two. Either cite the P3 run as partial direct-route evidence and say whether it ran as a top-level worker, or cite the conflict as UNVERIFIED. Quality impact: consistency.

**M17 (Adzic). WC-9 and D4 disagree about who may set an outward flag.** Severity MINOR. Grade: Medium. Expert: Adzic.
- WC-9 (SPEC:67) turns the flag on "through the command's own explicit flag written in the brief". D4(a) (SPEC:245) requires that the user's own instruction name the action. D4 is open. Recommendation: say which rule binds until D4 is decided.

### === ARCHITECTURE ANALYSIS ===

**M12. The tasklist row says "none" by relying on nesting that the spec itself calls unproven.** Severity MAJOR. Grade: Medium. Expert: Fowler, Nygard.
- SPEC:122 says the reflect fan-out of tasklist "runs one layer below the worker, inside Claude Code's nesting limit", with no change needed. SPEC:45 (section 1.4, gap 3) says Agent-tool fan-out inside a worker "has no proven limit". INV-B:210 and INV-B:215 say reflect should run at the top level, and INV-B:314 (UNVERIFIED 1) asks whether nested spawning works at all.
- Recommendation: mark tasklist "needs change" until the nested route is shown to work, or run Stage 10.5 reflect at top level. Quality impact: consistency.

**M8. The contract is an open interface with no schema.** Severity MAJOR. Grade: Medium. Expert: Newman.
- WC-4 (SPEC:62) requires "at least" four fields. Section 7 step 4 (SPEC:183) checks two of them. Commands "add the missing ones" with no version key, types or allowed-value table. Recommendation: add a field table with types, enumerations and a schema version, and check it in `tests/skills/test_worker_contract.py`. Quality impact: completeness.

**M9. "Exactly once" has no retry identity for a lost `worker_done`.** Severity MAJOR. Grade: Medium. Expert: Hohpe.
- WC-5 (SPEC:63) and step 3 (SPEC:182) require exactly one `worker_done`. CAPS:117 says every orchestration mutation accepts `--retry-request <id>` so a lost response does not duplicate the mutation. The spec does not mention it. Recommendation: state that a lost `worker_done` is re-sent with the same retry identity. Quality impact: completeness.

**M14. A worker parked in `ask` may fail the step 2 pass condition.** Severity MINOR. Grade: Medium. Expert: Nygard.
- SPEC:181 passes only if `observation.agentWait` is never non-null. CAPS:52 and CAPS:129 describe `agentWait` as a prompt only a human can answer. Whether an open `ask` sets it is UNVERIFIED. Recommendation: exclude an open `ask` addressed to the coordinator, or verify the behavior first. Quality impact: testability.

**M15. The contract is silent when Orca becomes unreachable mid-run.** Severity MINOR. Grade: Medium. Expert: Nygard.
- WC-12 (SPEC:70) covers only `consumer_fenced`. CAPS:147 gives `runtime_unavailable` for an unreachable runtime. Recommendation: state that the worker keeps its local writes, sends no lifecycle message until the runtime is reachable, and reports the contract on return. Quality impact: completeness.

**M16. The plugin mirror rule is deferred to each phase plan.** Severity MINOR. Grade: Medium. Expert: Fowler.
- SPEC:279 (UNVERIFIED 8) leaves the `plugins/superclaude/` mirror rule open, and P1 edits about 37 commands. AC-C2 (SPEC:173) checks only `.claude/` sync. Recommendation: settle the mirror rule in the spec before P1, or add a check. Quality impact: consistency.

**M4 (see above)** and **F1 to F4** also have architectural consequences: the contract location (F1) and output-path defaults (F4) are interface decisions.

### Minor notes (follow-up candidates only)

- N1. SPEC:22 says the Orca session reached `input_accepted` "and answered". The cited EVIDENCE:45 quote (CAPS:49) supports only `state: ready, stage: input_accepted`. Recommendation: drop "and answered" or cite the answer.
- N2. SPEC:111 (index row) tells the command to "state that knowledge-base mode does not wait". INV-A:113 lists this as UNVERIFIED. Recommendation: name the mode as an open question instead of asserting it.
- N3. SPEC:112 (load) sits under "Needs a change" with only a usage-line defect, while its own verdict says it should be a brief step, not a Task. Recommendation: move it to its own label.

## Whittaker attack findings (section 3 of the critique format)

- I can break this specification by **FR-2.1 Zero/Empty Attack**. The invariant at **SPEC:63 (WC-5)** fails when **the contract file is empty or has a status outside the four values**. Concrete attack: **the worker writes a zero-byte contract after a crash; step 4 of the check (SPEC:183) fails, but the coordinator's worker_done is `--outcome succeeded` because "otherwise" catches the empty file.** Severity MAJOR. Covered by F3.
- I can break this specification by **FR-2.3 Sentinel Collision Attack**. The invariant at **SPEC:228 (D1)** fails when **the flag string appears in quoted content**. Severity MINOR. Covered by M6.
- I can break this specification by **FR-2.4 Sequence Attack**. The invariant at **SPEC:64 (WC-6)** fails when **a retry starts while the first Dispatch is live**. Severity MAJOR. Covered by M4.

## Follow-up candidates (Medium and minor; not in the Reviser brief)

The coordinator asks the user once whether to open issues for these. This report creates none.

- M1 to M17 and N1 to N3, as listed above.

## Reviser brief

Blocking finding ids: F1, F2, F3, F4.

Restated rule (bullet 6 of the review loop): revise only text that a blocking finding names; add no rule, mechanism or section that no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after and the bytes added and deleted per finding id. Medium and minor findings do not trigger a revision, and no Medium or minor finding may be edited under this brief.

Named texts: F1 names SPEC:62, :83, :87, :90, :92, :85, :105, :73. F2 names SPEC:73, :158, :159, :180, :194. F3 names SPEC:63 and :183. F4 names SPEC:69 and :146 (with SPEC:86 as the example row).

Lines this brief does not reach: section 3.1 and 3.2 labels (M1), AC-C1 (M2), and the other follow-up items.

verdict: FAIL

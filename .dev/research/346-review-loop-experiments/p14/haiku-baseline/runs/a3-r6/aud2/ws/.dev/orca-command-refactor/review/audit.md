review: 1 of 3

# Spec-panel critique: orca-worker-contract-spec.md (labelled whole-document audit)

- Command: `/sc:spec-panel @.dev/orca-command-refactor/specs/orca-worker-contract-spec.md --mode critique --focus requirements,architecture` (first review, FIRST-REVIEW prompt of `~/.claude/rules/prompts/document_review_loop_prompts.md:27-32`, read in full).
- Candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`, sha256 `f8f6302199d147a422c4ace828ab0a5bd64e8d93cc92412e2478d4460e7d27ae`.
- Baseline: none given and none needed (first review; `--re-review` not used).
- Reviewer model actually used: Sonnet 5.5 (`claude-sonnet-5-5`).
- Coverage: the whole candidate (286 lines, sections 1-9, Decisions, UNVERIFIED), checked against the only checkable evidence, the three inventories (`inventory/commands-a.md`, `commands-b.md`, `orca-capabilities.md`) and `README.md`. Panel order: Wiegers, Adzic, Cockburn, Fowler, Nygard, Whittaker, Newman, Hohpe, Crispin, Gregory, Hightower. Hohpe, Gregory and Hightower raised nothing the other experts had not.
- Brief clauses overridden: none.
- Not covered: every citation to a path outside the workspace is UNVERIFIED (not checkable here): `CLAUDE.md:*`, `src/superclaude/**` (including `install_core.py`, `HOW-WE-WORK.md`, all `cmd/` and `sk/` lines), `.dev/evals/.../EVIDENCE.md`, `.dev/codegraph-migration/**`, `pyproject.toml:38`, `Makefile:68-74`, the `grep` results at spec:25, the 11 re-read locations at spec:11, and the 340-citation check at spec:285. The review labels F-01..F-03, N-01, N-02 and SA-1 used in the spec (for example spec:64, spec:79) point at an earlier review whose files are not in the sandbox; UNVERIFIED.
- Citation spot check done: every `INV-A:N`, `INV-B:N` and `CAPS:N` line the spec cites that I tested lands on the row or note it names (for example `INV-A:35-55`, `INV-B:31-52`, `INV-B:289-299`, `INV-A:94-98`, `CAPS:97-103`, `CAPS:145-151`). Counts agree: 21+22=43 (`INV-A:3`, `INV-B:3`); 10 ready + 27 changed + 6 coordinator-only (spec:76, rows at spec:83-92, 99-125, 132-137); the phase column covers all 37 worker commands (13 in P1 with the 4 ready-command fixes, 15 in P2, 4 in P3, 3 in P4, plus brainstorm and init-lite with no edit beyond the P1 section).

## Findings

Grading check (FIRST-REVIEW prompt, `document_review_loop_prompts.md:31`): each finding below carries the sentence "An implementer who follows the stated text as written builds X, and X is wrong because Y." Only B-1 holds with no further assumption. The others need a guess, or are requirements the spec never states, so they are Medium and sit under `follow-up candidates`.

=== REQUIREMENTS ANALYSIS ===

### B-1 (CRITICAL by consequence: blocking) Contract location is undefined for file-valued and command-fixed output rows
- Expert: Wiegers (lead), Adzic, Whittaker (zero/empty attack).
- Location: WC-4 (spec:62), WC-6 (spec:64), 2.3 (spec:73), 7.2 steps 3-4 (spec:182-183), AC-2.2 (spec:200), rows spec:85-92 and 99-125.
- Grading sentence: An implementer who follows WC-4 as written puts the contract at `<output-dir>/return-contract.yaml`, where `<output-dir>` is "the directory the coordinator passed (`--output` / `--output-dir`)" (spec:62), and X is wrong because for `/sc:tdd`, `/sc:init-lite` and the `--output` the spec adds to `/sc:spec-panel` the value passed is a file (the TDD itself, spec:90; "`--output <file>`", spec:87; "add `--output`", spec:120), so the contract path is `<file>/return-contract.yaml`, which cannot be created. AC-2.2 itself runs `/sc:tdd "auth" --unattended --output <file>` and requires a contract with `status: blocked` (spec:200); 7.2 step 4 does `test -s <contract>` (spec:183). The acceptance criterion cannot pass as written.
- Same root defect, other rows: WC-4/WC-6/F-02 say the coordinator passes the directory and "the command never chooses its own output directory" (spec:62, 64), and 2.3 says the report path is "known before dispatch" (spec:73). The rows say otherwise: cleanup-audit's directory "is fixed" (spec:85); index-repo's location is only "implied" (spec:86, `INV-A:117`); workflow's package directory is `.dev/tasks/to-do/<id>/` with the brief passing only `--handoff none` and "Fresh package each run" (spec:92, `INV-B:272`), and its pre-creation STOP has no directory at all (spec:92, `INV-B:272`); implement's ledger path is chosen by the command (spec:109, `INV-A:51`); research writes a run-time `claudedocs/research_*.md` (spec:116, `INV-B:132`); review-translation writes `reports/localization/` (spec:117, `INV-B:142`). For each of these WC-4 gives no contract path and WC-6 gives the coordinator no directory to pass for a retry (spec:64).
- Recommendation: state one rule that covers all three cases, for example "the contract path is `<report-dir>/return-contract.yaml` where `--report-dir` is a directory flag separate from any file-valued `--output`, or, for a row that fixes its own directory, the path that row names", and list that path per row in 3.1/3.2. Narrow rather than add: fix the WC-4 sentence and name the path in the affected rows.
- Priority: High. Quality impact: Testability 3 to 8 (the coordinator cannot locate the report it is told to open).

=== ARCHITECTURE ANALYSIS ===

No architecture finding reaches blocking. The decision itself (Orca on top, commands as units, section 1) matches the evidence: `CAPS:92`, `CAPS:97-103`, `CAPS:145-149`, `INV-A:90`, `INV-B:285-286`. The Medium items below are architecture follow-ups.

## Medium findings (follow-up candidates, never block, never in the Reviser brief)

- **M-1 (MAJOR label, Medium) Flag accepted before its gates are converted.** Expert: Fowler, Nygard. P1 adds `--unattended` to "every command in sections 3.1 and 3.2 (a no-op where a command has no gate)" (spec:159, spec:79); 2.3 tells the coordinator to put `--unattended` in briefs "from P1 on" (spec:73); gate resolutions for auggie-review, cli-eval, task and others arrive in P2-P4 (spec:100, 104, 121, 160). Between P1 and P2 `/sc:auggie-review <PR> --unattended` could post to GitHub and offer remediation, against WC-9 (spec:67). Needs the guess that a coordinator dispatches an unconverted command. Recommendation: say in 2.3 or section 6 that a needs-change command is not dispatched until its phase has passed. Priority: Medium.
- **M-2 (FR-8 GAP, Medium) Token rule for `--unattended` is undefined.** Expert: Whittaker (sentinel collision). Spec:51 and D1 (spec:227-230) never say whether `--unattended` inside quoted free text switches the mode. A person's prompt that contains the string could drop every gate and violate SA-1 (spec:146). Recommendation: one sentence: standalone token outside quotes only. Priority: Medium.
- **M-3 (FR-9 GAP, Medium) `--unattended` with no output location.** Expert: Whittaker (zero/empty attack). WC-2(c) requires a blocked contract (spec:60) but nothing says where it goes when the caller omitted the flag (spec:62). Recommendation: refuse in chat before any work. Priority: Medium.
- **M-4 (Medium) Status vocabulary versus "keep their fields".** Expert: Wiegers, Newman. WC-4 says existing contracts "keep their fields and add the missing ones" (spec:62) and fixes `status` to four values (spec:62, spec:262). If an existing contract (workflow, reflect, adversarial; `INV-B:272`, `INV-B:112`, `INV-A:35`) uses other values, the two texts conflict and 7.2 step 4 fails (spec:183). The existing vocabularies are not in the inventories, so UNVERIFIED. WC-5 also gives no outcome for a contract whose `status` is missing or not one of the four (spec:63). Recommendation: record each existing vocabulary and the mapping. Priority: Medium.
- **M-5 (Medium) WC-3 "re-invoke with the answer as a flag".** Expert: Adzic, Cockburn. For tdd's topic clarification, cli-portify's three approval gates, implement's Ruling and cli-eval's menu no answer flag exists (spec:90, 104, 105, 109), and the output directory of an in-session re-invocation is undefined (WC-6 covers only `worker-start --retry-of`, spec:64). The blocked path is the fallback, so no wrong outcome is forced. Recommendation: limit WC-3 to gates that have a flag, and say which directory a re-invocation uses. Priority: Medium.
- **M-6 (Medium) Worker-session requirements have no delivery mechanism.** Expert: Fowler, Hohpe. WC-3, WC-5, WC-7 and WC-12 are owned by "Worker session" (spec:61, 63, 65, 70), but 2.3 lists what the brief carries and omits all four (spec:73), and the command-side `## Unattended mode` section cannot bind the session that runs the command. Recommendation: add them to the brief template that P0 writes (spec:158). Priority: Medium.
- **M-7 (Medium) WC-9 "command's own explicit flag" for `/sc:task`.** Expert: Nygard. `commit`/`push` and the committed TFEP report (spec:121, `INV-B:204`) have no such flag, and D4(a) relies on one (spec:245). Recommendation: say the action stays off in unattended mode. Priority: Medium.
- **M-8 (Medium) Tasklist Stage 10.5 `needs_human_decision` HALT.** Expert: Whittaker (sequence). Spec:122 passes `--unattended` to reflect so the headless auto-accept rule applies, but `INV-B:209` says `needs_human_decision` items HALT and that who answers is UNVERIFIED. WC-2 resolves no gate for this one. Priority: Medium.
- **M-9 (Medium) AC-2.4 can pass after a post.** Expert: Crispin. `gh api .../reviews --jq length` and `.../comments --jq length` without `--paginate` count one page of 30 (spec:202), so a PR already at the page size shows unchanged counts after a post. Recommendation: add `--paginate`. Priority: Medium.
- **M-10 (Medium) Untested requirements.** Expert: Crispin, Gregory. No AC exercises WC-1, WC-3 (the `ask` path) or WC-12 (sections 7.1-7.3, spec:169-210); WC-10 is gated only for pr-submit (AC-4.3, spec:210), not cli-eval (spec:104). AC-0.4 says step 4 "use[s] the command's existing report file" (spec:194), but step 4 is a YAML status assertion (spec:183) that a markdown REPORT.md cannot satisfy. Priority: Medium.
- **M-11 (Medium) Evidence strength stated unevenly.** Expert: Fowler. E3 cites `invocation_method: "skill-direct"` as evidence the route "has worked" (spec:23) while 1.4(1) says that run used the Agent-tool route and proves only the nested one (spec:43); `INV-A:35` and `INV-A:13` call the same run a proven direct call, and the Decisions row says nothing contradicted the inventories (spec:268). The tasklist row asserts its reflect fan-out is "inside Claude Code's nesting limit" (spec:122) while `INV-B:210` and `INV-B:314` mark nested spawning UNVERIFIED. Recommendation: reconcile the wording. Priority: Medium.
- **M-12 (Medium) Architecture notes.** Expert: Nygard, Newman. (a) D3(a) has the coordinator run pr-submit's attended loop itself (spec:240), during which it cannot service `check`/`ask` from other workers; not discussed. (b) The contract carries no version field, though workflow's has one (`INV-B:272`, "contract 1.1"). (c) Nothing says the contract is written atomically or last, so a worker that dies mid-write leaves YAML that fails 7.2 step 4. Priority: Low to Medium.

## Minor notes (never fail the review)
- Spec:79 says "every one of them except `load`" under 3.1, but `load` is in 3.2 (spec:112).
- AC-C1 (spec:172) shows `\|` for alternation and pipes; copied raw into `grep -E` it matches a literal `|`. It also checks only command-form text (`orca <verb>`), not "names Orca" as SA-2 words it (spec:147).
- P0 adds `tests/skills/test_worker_contract.py` (spec:158) but gives its P0 content no check; AC-1.2 does not name brainstorm or init-lite (spec:159, 196).
- WC-1's "well inside" the 60 s limit (spec:59) is not a number; the evidence supports 30 s (`CAPS:49`). Owner is launch setup, so out of the command scope.
- The spec has no concrete example contract file; `report_path`/`artifacts` are not said to be repo-relative or absolute (spec:62).

## Guard Condition Boundary Table (hard gate; completed before synthesis)

Guards found: G1 `--unattended` switch; G2 contract output location; G3 WC-5 status-to-outcome mapping; G4 WC-10 wait size; G5 retry and circuit breaker; G6 `/sc:task` confidence 0.70. Classes left out are named under the table.

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|-------|----------|-----------------|----------------|--------------|-------------------|--------|
| G1 `--unattended` | spec:51, 60, D1 spec:227-230 | Zero/Empty | flag absent | false | today's behaviour, SA-1 (spec:146) | OK |
| G1 | spec:51 | Typical | standalone token | true | WC-2 gate resolution (spec:60) | OK |
| G1 | spec:51 | Sentinel Value Match | string inside quoted topic text | unspecified | not stated | GAP (M-2, Medium) |
| G1 | spec:138, 217 | Legitimate Edge Case | section-4 command given the flag | n/a | "no `--unattended` mode" (spec:128); AC-1.1 checks no section (spec:195) | OK |
| G2 contract location | spec:62 | Zero/Empty | no output flag given | unspecified | not stated | GAP (M-3, Medium) |
| G2 | spec:62, 90 | One/Minimal | `--output` is a file | unspecified | `<file>/return-contract.yaml` implied | GAP (B-1, blocking) |
| G2 | spec:62 | Typical | `--output <dir>` | true | `<dir>/return-contract.yaml` | OK |
| G2 | spec:85, 86, 92, 109 | Legitimate Edge Case | command fixes its own directory | unspecified | no contract path named | GAP (B-1, blocking) |
| G3 status mapping | spec:63 | Typical | `succeeded` / `partial` | true | outcome succeeded (spec:63, 263) | OK |
| G3 | spec:63 | Typical | `failed` / `blocked` / no report | true | outcome failed | OK |
| G3 | spec:63, 183 | Sentinel Value Match | `status` absent or outside the four values | unspecified | not stated | GAP (M-4, Medium) |
| G4 wait size | spec:68 | Typical | call under 5 min | false | no split | OK |
| G4 | spec:68, 104 | Maximum/Overflow | 3600 s eval | true | split into waits of at most 4 min | OK (no AC for cli-eval, M-10) |
| G4 | spec:68 | Legitimate Edge Case | call of 4 to 5 min | false | not split; next heartbeat still within 5 min | OK |
| G5 retry | spec:64, `CAPS:80` | Maximum/Overflow | third consecutive failed start | unspecified | spec says nothing about the breaker | GAP (Medium, minor: Orca's rule, `CAPS:116`, `CAPS:80`) |
| G6 task confidence | spec:121 | Legitimate Edge Case | confidence exactly 0.70 | false | "below 0.70 resolves as blocked" | OK |
| G6 | spec:121 | Zero/Empty | confidence 0 | true | blocked | OK |

Left out, with reason: G1 One/Minimal and Maximum (a flag has no size); G3 Zero/Empty and Maximum (a status is one enum value); G4 Zero/Empty and Sentinel (a wait of zero or a sentinel length cannot occur); G5 Zero/Empty, One and Typical (the breaker concerns only repeated failure); G6 Maximum and Sentinel (confidence is bounded 0 to 1; no sentinel is named).

FR-8/FR-9/FR-10: every GAP above is graded under the Review Loop (`command.md` Review Loop bullet 2). Only the G2 rows that restate B-1 are blocking. The table is complete, so synthesis is not blocked.

## Pipeline Dimensional Analysis (FR-17 to FR-21)

Trigger met loosely: the classification pipeline in section 3 has stages whose output count differs from input. No dimensional mismatch found.

```text
[43 commands: INV-A:3 (21) + INV-B:3 (22)] --> [exclude coordinator-only: 6, spec:132-137] --> [37 worker commands]
   37 --> [ready today: 10, spec:83-92] + [needs change: 27, spec:99-125]
   37 --> P1 flag + section on all 37 (spec:79, 159)
         edits by phase: P1 13 | P2 15 | P3 4 | P4 3 | none beyond the P1 section: brainstorm, init-lite (13+15+4+3+2 = 37)
   Consumer: AC-1.1 asserts a section on every one of the 37 except load's contract wording (spec:195): count 37 matches
```

## Expert consensus and disagreements
- Consensus: the decision and the rejection of commands calling Orca (spec:28-39) are well evidenced; the 10/27/6 split matches both inventories.
- Single open point of disagreement: none among the panel; Adzic and Whittaker both converge on B-1.

## Follow-up candidates
Medium and minor findings, none blocking: M-1 to M-12 and the minor notes above. Issue question: not asked in this run (no user channel in the sandbox); recorded only, no issue created.

## Reviser brief
Repair only the blocking finding B-1 in the revised candidate `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`. Revise only text a blocking finding names; add no rule, mechanism or section that no blocking finding calls for; each added paragraph or table cites its finding id (B-1); prefer deleting or narrowing to adding; report the byte size before and after and the bytes added and deleted per finding id. Leave minor and Medium findings alone. Return the candidate once and do not award yourself a PASS.

verdict: FAIL

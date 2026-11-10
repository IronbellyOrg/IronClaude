review: 1 of 3

# /sc:spec-panel critique report: orca-worker-contract-spec.md (first review)

- Command: `/sc:spec-panel @.dev/orca-command-refactor/specs/orca-worker-contract-spec.md --mode critique --focus requirements,architecture` (run as a worker; the command was applied by reading its definition file in the sandbox)
- Candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md` (285 lines)
- Candidate SHA-256: `d3cdbe573e57303b9ce6c93d1fe98ba18fb7cb1a15773d926bf6a0c31425200d`
- Baseline: missing (first review; no `--re-review`)
- Reviewer model: claude-haiku-5-5, single reviewer. `superclaude review panel resolve` was not run, so this is one reviewer, not a panel. The panel lenses applied were the requirements set (Wiegers, Adzic, Cockburn) and the architecture set (Fowler, Newman, Hohpe, Nygard), with Whittaker's attack pass on the guard conditions.
- Review date: 2026-11-10

## Citation key

- `SPEC:N` = line N of `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`
- `README:N` = line N of `.dev/orca-command-refactor/README.md`
- `INV-A:N` = line N of `.dev/orca-command-refactor/inventory/commands-a.md`
- `INV-B:N` = line N of `.dev/orca-command-refactor/inventory/commands-b.md`
- `CAPS:N` = line N of `.dev/orca-command-refactor/inventory/orca-capabilities.md`

The spec cites many files outside this run's workspace: `src/superclaude/...`, `~/.claude/...`, `.dev/evals/...`, `.dev/codegraph-migration/...`, `pyproject.toml`, `CLAUDE.md`, and the Orca binary files. None of them exists in the workspace, so each claim that rests only on one of them is marked UNVERIFIED here. The checks below were run against the three inventory files and the README, which are in the workspace.

## Coverage

What I covered:
1. The command definition (`command.md`), including the Review Loop, Mandatory Output Artifacts, Guard Condition Boundary Table, and Pipeline Dimensional Analysis sections.
2. The FIRST-REVIEW prompt in `home/.claude/rules/prompts/document_review_loop_prompts.md`.
3. The full spec, the README, all three inventories.
4. Cross-checks of every `INV-A`, `INV-B` and `CAPS` citation in the spec's section 1.2, section 2.2, section 3 and section 9 against the inventory line it names. The lines I checked matched their quotes, with the exceptions noted in F10.
5. Internal consistency of the spec: the section 3 row counts (10 ready, 27 needs change, 6 coordinator-only, 43 total), the phase lists in section 6 against the section 3 phase column, the acceptance checks in section 7 against the requirements in section 2 and section 5, and the decisions in section 9 against the rows they affect.

What I did not cover: any claim that rests only on a file outside the workspace (UNVERIFIED, listed under follow-up candidates).

## Grading check notes

Each blocking finding below carries the sentence the grading check requires. Findings that need a guess about what the implementer does are graded Medium.

## Findings

### Blocking findings

**F1 (CRITICAL, blocking, contradiction). The brief must carry `--unattended`, but the ready commands do not accept it until Phase 1, and the section 3.1 brief flags omit it.**
- SPEC:73 says each brief states "the exact command line including `--unattended` and every flag section 3 lists as required".
- SPEC:79-84 and SPEC:88-92 give the brief flags for the ten ready commands, for example brainstorm: "`--output <dir>`; never `--interactive`" (SPEC:84). None of those flag lists contains `--unattended`.
- SPEC:158 (P0) runs `/sc:troubleshoot`, `/sc:workflow --handoff none` and `/sc:adversarial --output <dir>` as live workers before any command accepts `--unattended`. SPEC:159 (P1) is the phase that adds the flag ("the `--unattended` flag accepted by every command in sections 3.1 and 3.2").
- SPEC:180 (step 1 of the live check) builds the brief "per section 2.3", so it too requires `--unattended`.
- An implementer who follows section 2.3 in P0 passes a flag the command does not accept. An implementer who follows section 3.1 and P0 omits the flag, which breaks section 2.3. Either way the P0 smoke runs cannot test the unattended path the phase is meant to validate, and the spec does not say which of the two is intended.
- Evidence: SPEC:73, SPEC:79-92, SPEC:158-159, SPEC:180. The one-line decision the spec needs is whether P0 runs ready commands with or without `--unattended`.

**F2 (CRITICAL, blocking, contradiction). The section 3.1 text says the ready commands change only through small fixes, but AC-1.1 requires every section 3.1 and 3.2 command to have an `## Unattended mode` section in Phase 1.**
- SPEC:79: "The only command changes are the small fixes in the last column."
- SPEC:195 (AC-1.1, Phase 1): "every command in sections 3.1-3.2 has a `## Unattended mode` section naming `return-contract.yaml`".
- Ten of the section 3.1 rows have no fix that would add a section (for example brainstorm, SPEC:84, whose fix column is "None"). AC-1.1 still requires the section in Phase 1.
- AC-1.1 also requires the section in commands whose gate behavior is converted only in Phases 2 to 4 (for example `cli-eval`, SPEC:104, Phase 2). The section would then describe gate resolutions the command does not yet perform. SPEC:73 and SPEC:161-162 make those phases later, so this is a wrong outcome of the phasing: documented behavior that is not implemented.
- The check and the text cannot both be followed. Evidence: SPEC:79, SPEC:195, SPEC:84, SPEC:104.

**F3 (CRITICAL, blocking, unpassable-check). AC-0.4 step 4 cannot pass for `/sc:troubleshoot`.**
- SPEC:194 (AC-0.4): "step 4 uses the command's existing report file, since the contract arrives in P1". SPEC:183 (step 4) requires `yaml.safe_load` of the file, with `d['status']` and `d['command']` present.
- For `/sc:troubleshoot` the existing report file is `REPORT.md` (INV-B:49, INV-B:242: "`report_path` REPORT.md, `audit.log`"). A Markdown report has no YAML `status` or `command` keys, so the assertion fails for the one P0 command that has no contract file.
- P0 therefore cannot pass as written. The fix is to give step 4 a per-command fallback or to drop the YAML assertion for P0. Evidence: SPEC:183, SPEC:194; INV-B:49, INV-B:242.

### Medium findings (follow-up candidates; not blocking)

**F4 (MAJOR, not blocking, contradiction). `pr-submit` is listed as a needs-change row in Phase 4, but the recommended D3 option changes nothing.**
- SPEC:114 (section 3.2 row) and SPEC:162 (P4 scope) list `pr-submit` as a Phase 4 change. SPEC:139 says it "stays a worker candidate only if the user accepts open decision D3".
- SPEC:240 (D3, recommended option a): "no pr-submit changes in Phase 4."
- The section 3.2 count of 27 includes pr-submit, and section 4 does not list it. Under the recommendation the spec has 26 changes, not 27, and the section 3.2 row describes work the recommendation rules out. Evidence: SPEC:114, SPEC:139, SPEC:162, SPEC:240.

**F5 (MAJOR, not blocking, contradiction). WC-2 says each gate resolves one of three ways, but the `reflect` row adds a fourth resolution: auto-accept.**
- SPEC:60 (WC-2): "Each gate resolves one of three ways ... (a) a documented default; (b) a value the caller supplied as a flag; (c) blocked".
- SPEC:88 (reflect): "Under `--unattended`, make `--remediate` follow the existing headless auto-accept rule instead of the `[yes / no]` prompt (P2)". SPEC:122 (tasklist) relies on the same rule.
- Auto-accept may be read as a documented default, so the reading is a guess. It is also a remediation that runs `sc:workflow` or `task-builder` with no person, which WC-2 does not name. Evidence: SPEC:60, SPEC:88, SPEC:122, and SPEC:151 (SA-6, which says `--unattended` "reuses" the headless rule).

**F6 (MAJOR, not blocking, other). WC-4 places the contract in `<output-dir>`, but several commands take `--output <file>`.**
- SPEC:62: "`<output-dir>` is the directory the coordinator passed (`--output` / `--output-dir`)".
- SPEC:90 (tdd): "a precise component prompt, not a bare topic; `--output <file>`". SPEC:87 (init-lite) also takes `--output <file>`.
- For these commands the directory WC-4 names does not exist as passed, so the contract location must be guessed. Evidence: SPEC:62, SPEC:87, SPEC:90.

**F7 (MAJOR, not blocking, contradiction). WC-11 forbids two workers writing one file, but the `index-repo` row keeps its fixed default output path and stays "ready".**
- SPEC:69 (WC-11): "Default output paths carry a timestamp or the slug the coordinator passes".
- SPEC:86 (index-repo): `PROJECT_INDEX.md` (location implied), brief "none". Its fix is only to state the output location. init-lite (SPEC:87) has the same shape: "`.dev/superclaude/context-audit.md` or `--output`".
- Two workers in one worktree would write the same file under the brief SPEC:86 describes. The spec does not say the coordinator must serialize them. Evidence: SPEC:69, SPEC:86, SPEC:87. Cleanup-audit (SPEC:85) is acknowledged in the same way, which makes the silence on index-repo more visible.

**F8 (MAJOR, not blocking, unpassable-check). AC-0.4 says the no-Agent-wrapper rule is "verified in the step-5 transcript", but step 5 checks only for `AskUserQuestion`.**
- SPEC:194 (AC-0.4): "each run directly by the worker (no Agent-tool wrapper, verified in the step-5 transcript)".
- SPEC:184 (step 5): "search the transcript for `AskUserQuestion`. **Pass:** no `AskUserQuestion` call."
- The rule WC-7 (SPEC:65) that AC-0.4 claims to verify has no check in section 7. Evidence: SPEC:65, SPEC:184, SPEC:194.

**F9 (MAJOR, not blocking, contradiction). AC-C1 scans `src/superclaude/core`, where the spec both requires an Orca section and permits Orca mentions.**
- SPEC:172 (AC-C1) scans `src/superclaude/core` and requires no `orca orchestration|worktree|terminal|agent` match ("prints nothing (SA-2, WC-8)").
- SPEC:147 (SA-2) allows "the only allowed mention of Orca in a changed command ... inside the contract file". SPEC:52 places the contract file in `src/superclaude/core/`.
- SPEC:150 and SPEC:158 (P0) require an Orca section in `src/superclaude/core/HOW-WE-WORK.md`, which is in the same scanned directory. A routing section that names `orca-ide orchestration` commands, as a routing guide would, fails AC-C1 in P0 on every run.
- Whether the implementer names those commands is a guess, so this is Medium. The check needs its scope or its pattern changed to match SA-2. Evidence: SPEC:52, SPEC:147, SPEC:150, SPEC:158, SPEC:172.

**F10 (MINOR, not blocking, other). E4 states as established that Agent-tool subagents are not counted by the depth fence; the cited evidence does not show it.**
- SPEC:24 (E4): "Agent-tool subagents inside a worker are not Orca workers and are not counted by Orca's nesting limit."
- CAPS:155 says the only basis is the depth fence's wording and records "UNVERIFIED that Orca never limits them". SPEC:45 (section 1.4, gap 3) concedes the point: "has no proven limit, but no proof of none either". The E4 row should carry the same UNVERIFIED mark.
- I checked the other `CAPS` and `INV` citations in section 1.2 and section 2.2 against their lines and they match. CAPS:155 is the only one whose quoted claim is stronger than its source. Evidence: SPEC:24, SPEC:45; CAPS:155.

**F11 (MAJOR, not blocking, missing-requirement). WC-6 requires a retry not to corrupt the first attempt's output, but nothing requires a retry to get a new output directory.**
- SPEC:64 (WC-6): "A retry worker (`worker-start --retry-of`) must not corrupt the first attempt's output." The remedy in the same row is that a command "writes each run into a fresh output directory so a re-run starts clean".
- SPEC:73 says the brief states the output directory but does not say retries get a new one. A coordinator that reuses the original `--output` on a retry gets the outcome WC-6 forbids for every "fresh dir" command. Evidence: SPEC:64, SPEC:73.

**F12 (MAJOR, not blocking, missing-requirement). WC-5 maps everything "otherwise" to `succeeded`, so a `status` outside the four-value set is reported as success.**
- SPEC:62: "`status` (one of `succeeded`, `partial`, `failed`, `blocked`)".
- SPEC:63 (WC-5): "`--outcome succeeded` otherwise".
- A contract with `status: ok`, or with no `status` key, reaches the coordinator as a succeeded worker. The spec states the vocabulary and the failure mapping but not the out-of-set case. Evidence: SPEC:62, SPEC:63.

**F13 (MAJOR, not blocking, contradiction). WC-10 and AC-4.3 set different limits on a single tool call.**
- SPEC:68 (WC-10): a call "longer than 5 minutes must be split into waits of at most 4 minutes".
- SPEC:210 (AC-4.3): "no single tool call exceeds 240 s".
- A 4.5-minute call passes WC-10 and fails AC-4.3. Evidence: SPEC:68, SPEC:210.

**F14 (MINOR, not blocking, other). SA-3 turns on "the new output flag", which the spec never defines.**
- SPEC:148: "The new contract file and report files are written only in unattended mode or when the caller passes the new output flag."
- Many commands already have `--output`, and the spec does not say whether passing it alone is "the new output flag" (SPEC:87, SPEC:83 and others). AC-1.3 (SPEC:197) tests only the no-flag case. Evidence: SPEC:148, SPEC:197.

### Blocking count

3 blocking findings (F1, F2, F3). The verdict is FAIL.

## Guard Condition Boundary Table

This table is mandatory because the spec has conditional logic (WC-2, WC-4, WC-5, WC-6, WC-10, SA-3). Focus is requirements and architecture, not correctness, so the State Variable Registry is not required.

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|---|---|---|---|---|---|---|
| outcome mapping (WC-5) | SPEC:63 | Zero/Empty | no report file at the report path | true | `--outcome failed` (SPEC:63) | OK |
| outcome mapping (WC-5) | SPEC:63 | One/Minimal | `status: partial` | false | `--outcome succeeded` (SPEC:63) | OK |
| outcome mapping (WC-5) | SPEC:63 | Typical | `status: succeeded` | false | `--outcome succeeded` (SPEC:63) | OK |
| outcome mapping (WC-5) | SPEC:62-63 | Sentinel Value Match | `status: ok`, or any value outside the four | not in set | "otherwise" clause gives `--outcome succeeded` (SPEC:63) | GAP (F12) |
| outcome mapping (WC-5) | SPEC:63 | Legitimate Edge Case | audit verdict FAIL with `status: succeeded` | false | `--outcome succeeded` (SPEC:63) | OK |
| outcome mapping (WC-5) | n/a | Maximum/Overflow | left out: the guard tests an enum value, with no count or capacity input | n/a | n/a | n/a |
| gate resolution (WC-2) | SPEC:60, SPEC:104 | Zero/Empty | cli-eval `run` with no `--suite` | true (blocked) | (c) blocked, SPEC:104 | OK |
| gate resolution (WC-2) | SPEC:60, SPEC:90 | Typical | gate whose flag is in the brief | resolves as (b) | per row | OK |
| gate resolution (WC-2) | SPEC:88, SPEC:60 | Legitimate Edge Case | reflect `--remediate` offer under `--unattended` | auto-accept, not one of (a)(b)(c) | SPEC:88 | GAP (F5) |
| gate resolution (WC-2) | n/a | One/Minimal | left out: a gate is binary (present or absent) | n/a | n/a | n/a |
| wait split (WC-10) | SPEC:68, SPEC:104 | Maximum/Overflow | 3600 s eval wait | true (split) | waits of at most 4 min (SPEC:104) | OK |
| wait split (WC-10) | SPEC:68, SPEC:210 | Legitimate Edge Case | single call of 4.5 min | false under WC-10, true under AC-4.3 | WC-10 splits only calls over 5 min | GAP (F13) |
| resume (WC-6) | SPEC:64 | Legitimate Edge Case | retry with the same output directory | none stated | "fresh dir" per row, no retry rule | GAP (F11) |
| resume (WC-6) | SPEC:64, SPEC:197 | Typical | roadmap with `.session-memory.md` and no resume flag | fresh | fresh start (AC-3.2) | OK |
| contract location (WC-4) | SPEC:62, SPEC:90 | Sentinel Value Match | `--output <file>` where a directory is required | ambiguous | no rule | GAP (F6) |

Left-out classes are explained in the rows that say n/a. Every GAP row is carried into the findings block.

## Pipeline Dimensional Analysis

Not triggered. The spec's coordinator-to-worker-to-report chain has no stage whose output count differs from its input count. FR-17 excludes it.

## Reviser brief

Blocking finding ids: F1, F2, F3.

Revise only text a blocking finding names. Add no rule, mechanism or section that a blocking finding does not call for. Prefer deleting or narrowing to adding. Each added paragraph or table cites its finding id. Medium and minor findings are not part of this brief.

## Follow-up candidates

Medium and minor findings, not blocking, not part of the Reviser brief: F4, F5, F6, F7, F8, F9, F10, F11, F12, F13, F14.

Open question for the coordinator, asked once per loop: open an issue for these follow-up candidates? No issue has been created. The run is unattended and this report records the list only.

## Findings block

```findings-v1
{"id": "F1", "severity": "CRITICAL", "blocking": true, "category": "contradiction", "anchor": "the exact command line including `--unattended` and every flag section 3 lists as required", "anchor2": "`--output <dir>`; never `--interactive`", "refs": ["2.3", "3.1", "P0", "7.2"], "claim": "A brief built per section 2.3 passes --unattended to ready commands that do not accept it until P1, so the P0 smoke runs cannot follow both section 2.3 and section 3.1."}
{"id": "F2", "severity": "CRITICAL", "blocking": true, "category": "contradiction", "anchor": "The only command changes are the small fixes in the last column.", "anchor2": "every command in sections 3.1-3.2 has a `## Unattended mode` section naming `return-contract.yaml`", "refs": ["3.1", "AC-1.1", "P1"], "claim": "Section 3.1 says the ready commands change only by small fixes, but AC-1.1 requires every section 3.1 and 3.2 command, including Phase 2 to 4 commands, to have an Unattended mode section in Phase 1."}
{"id": "F3", "severity": "CRITICAL", "blocking": true, "category": "unpassable-check", "anchor": "step 4 uses the command's existing report file, since the contract arrives in P1.", "anchor2": "`test -s <contract>` and `uv run python -c", "refs": ["AC-0.4", "7.2 step 4"], "claim": "For /sc:troubleshoot the existing report is REPORT.md, which has no YAML status or command keys, so the step 4 assertion cannot pass as AC-0.4 requires."}
{"id": "F4", "severity": "MAJOR", "blocking": false, "category": "contradiction", "anchor": "outward actions per open decision D3", "anchor2": "no pr-submit changes in Phase 4.", "refs": ["3.2", "4", "6 P4", "D3"], "claim": "pr-submit is a needs-change row in P4 and in the count of 27, but the recommended D3 option makes no pr-submit change."}
{"id": "F5", "severity": "MAJOR", "blocking": false, "category": "contradiction", "anchor": "Each gate resolves one of three ways, listed per command in section 3", "anchor2": "make `--remediate` follow the existing headless auto-accept rule", "refs": ["WC-2", "3.1 reflect", "3.2 tasklist"], "claim": "WC-2 allows three gate resolutions, while reflect's auto-accept is a fourth, and the spec does not say whether it counts as a documented default."}
{"id": "F6", "severity": "MAJOR", "blocking": false, "category": "other", "anchor": "where `<output-dir>` is the directory the coordinator passed (`--output` / `--output-dir`)", "anchor2": "a precise component prompt, not a bare topic; `--output <file>`", "refs": ["WC-4", "3.1 tdd", "3.2 init-lite"], "claim": "WC-4 places the contract in a directory the coordinator passed, but tdd and init-lite take --output as a file, so the contract location is undefined."}
{"id": "F7", "severity": "MAJOR", "blocking": false, "category": "contradiction", "anchor": "Default output paths carry a timestamp or the slug the coordinator passes", "anchor2": "`PROJECT_INDEX.md` (location implied)", "refs": ["WC-11", "3.1 index-repo", "3.1 init-lite"], "claim": "WC-11 forbids two workers writing one file, but index-repo and init-lite keep fixed default output paths and stay ready with no brief flags."}
{"id": "F8", "severity": "MAJOR", "blocking": false, "category": "unpassable-check", "anchor": "each run directly by the worker (no Agent-tool wrapper, verified in the step-5 transcript)", "anchor2": "search the transcript for `AskUserQuestion`", "refs": ["AC-0.4", "7.2 step 5", "WC-7"], "claim": "AC-0.4 says the no-wrapper rule is verified in step 5, but step 5 only searches for AskUserQuestion, so the WC-7 rule has no check."}
{"id": "F9", "severity": "MAJOR", "blocking": false, "category": "contradiction", "anchor": "prints nothing (SA-2, WC-8)", "anchor2": "The only allowed mention of Orca in a changed command is as an example", "refs": ["AC-C1", "SA-2", "P0", "SA-5"], "claim": "AC-C1 scans src/superclaude/core, where P0 must add an Orca section and where SA-2 permits Orca mentions, so the common check can fail on text the spec requires or allows."}
{"id": "F10", "severity": "MINOR", "blocking": false, "category": "other", "anchor": "Agent-tool subagents inside a worker are not Orca workers and are not counted by Orca's nesting limit.", "anchor2": "has no proven limit, but no proof of none either", "refs": ["1.2 E4", "1.4 gap 3", "CAPS:155"], "claim": "E4 states as established a fact that CAPS:155 marks UNVERIFIED and section 1.4 concedes."}
{"id": "F11", "severity": "MAJOR", "blocking": false, "category": "missing-requirement", "anchor": "A retry worker (`worker-start --retry-of`) must not corrupt the first attempt's output.", "anchor2": "the output directory, so the report path is known before dispatch (WC-4)", "refs": ["WC-6", "2.3"], "claim": "No requirement gives a retry a new output directory, so a coordinator that reuses --output on retry can corrupt the first attempt's output."}
{"id": "F12", "severity": "MAJOR", "blocking": false, "category": "missing-requirement", "anchor": "`status` (one of `succeeded`, `partial`, `failed`, `blocked`)", "anchor2": "`--outcome failed` when the report says `failed` or `blocked`, or no report exists", "refs": ["WC-4", "WC-5"], "claim": "WC-5 maps any status outside the four-value set to succeeded, which the spec never states as intended."}
{"id": "F13", "severity": "MAJOR", "blocking": false, "category": "contradiction", "anchor": "must be split into waits of at most 4 minutes", "anchor2": "no single tool call exceeds 240 s", "refs": ["WC-10", "AC-4.3"], "claim": "WC-10 splits only calls longer than 5 minutes, but AC-4.3 forbids any call over 240 s, so a 4.5-minute call passes one and fails the other."}
{"id": "F14", "severity": "MINOR", "blocking": false, "category": "other", "anchor": "written only in unattended mode or when the caller passes the new output flag", "refs": ["SA-3", "AC-1.3"], "claim": "SA-3 depends on a new output flag that the spec never defines, so it is unclear whether a standalone --output run writes the contract."}
```

verdict: FAIL
